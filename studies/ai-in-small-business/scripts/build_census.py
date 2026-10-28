"""Build tidy Census BTOS AI-use rows from the official download files.
Run: .venv/bin/python -I scripts/build_census.py STUDYDIR"""
import sys, csv, openpyxl, datetime as dt
D = sys.argv[1]
R = D + '/raw/census/'
CHECKED = '2026-10-28'
BASE = 'https://www.census.gov/hfp/btos/downloads/'
URL = {
    'new': BASE + 'National.xlsx',
    'new_size': BASE + 'Employment%20Size%20Class.xlsx',
    'new_sector': BASE + 'Sector.xlsx',
    'new_sxs': BASE + 'Sector%20by%20Employment%20Size%20Class.xlsx',
    'old': BASE + 'AI%20Core%20Questions.xlsx',
    'supp': BASE + 'AI_Supplement_Table_2026.xlsx',
}
SIZE = {'A': '1-4', 'B': '5-9', 'C': '10-19', 'D': '20-49', 'E': '50-99', 'F': '100-249', 'G': '250+'}
SECTOR = {'11': 'Agriculture, Forestry, Fishing and Hunting', '21': 'Mining, Quarrying, and Oil and Gas Extraction',
          '22': 'Utilities', '23': 'Construction', '31': 'Manufacturing', '42': 'Wholesale Trade', '44': 'Retail Trade',
          '48': 'Transportation and Warehousing', '51': 'Information', '52': 'Finance and Insurance',
          '53': 'Real Estate and Rental and Leasing', '54': 'Professional, Scientific, and Technical Services',
          '55': 'Management of Companies and Enterprises', '56': 'Administrative and Support and Waste Management and Remediation Services',
          '61': 'Educational Services', '62': 'Health Care and Social Assistance', '71': 'Arts, Entertainment, and Recreation',
          '72': 'Accommodation and Food Services', '81': 'Other Services (except Public Administration)',
          'XX': 'Multi-sector (multi-unit firms in several sectors)'}
MEAS = {7: 'used_ai_last_2_weeks', 24: 'expect_ai_next_6_months'}

def d(x):
    if x is None: return ""
    if isinstance(x, dt.datetime): return x.date().isoformat()
    m, dd, y = x.split('/'); return f'{y}-{m}-{dd}'

# reference/collection dates (current file covers all smpdt)
wb = openpyxl.load_workbook(R + 'National.xlsx', read_only=True)
dates = {}
for r in list(wb['Collection and Reference Dates'].iter_rows(values_only=True))[1:]:
    if isinstance(r[3], int):
        dates[str(r[3])] = dict(collection_start=d(r[4]), collection_end=d(r[5]), period_start=d(r[6]), period_end=d(r[7]), published=d(r[8]))

def pct(v):
    if v is None or v in ('.', ''): return None, None
    if v == 'S': return '', 'suppressed by Census (S: does not meet publication standards)'
    return str(v).rstrip('%'), ''

rows = []
def emit(smpdt, qid, btype, bval, val, se, version, src, extra_note=''):
    p, note = pct(val)
    if p is None: return
    s, _ = pct(se) if se is not None else ('', '')
    dd = dates[smpdt]
    rows.append(dict(period_start=dd['period_start'], period_end=dd['period_end'], measure=MEAS[qid],
                     breakdown_type=btype, breakdown_value=bval, pct=p, se_pct=s or '', smpdt=smpdt,
                     collection_start=dd['collection_start'], collection_end=dd['collection_end'],
                     question_version=version, source_url=src, checked_on=CHECKED,
                     note='; '.join(x for x in [note, extra_note] if x)))

def sheet_pairs(path, est, se, keycols):
    wb = openpyxl.load_workbook(path, read_only=True)
    E = list(wb[est].iter_rows(values_only=True)); S = list(wb[se].iter_rows(values_only=True))
    hdr = E[0]; k = keycols
    semap = {tuple(r[:k + 4]): r for r in S[1:] if r and r[0] is not None}
    for r in E[1:]:
        if not r or r[k] not in (7, 24) or r[k + 3] != 'Yes': continue
        sr = semap.get(tuple(r[:k + 4]))
        for j in range(k + 4, len(hdr)):
            if hdr[j] is None: continue
            yield r[:k], r[k], str(hdr[j]), r[j], (sr[j] if sr else None)

V_OLD = 'v1 "in producing goods or services" (old series, 2023-09 to 2025-10)'
V_NEW = 'v2 "in any of its business functions" (new series from 2025-11-17 collection)'
# old series (AI Core Questions original)
for keys, q, sm, v, se in sheet_pairs(R + 'AI_Core_Questions.xlsx', 'National Estimates', 'National SE', 0):
    emit(sm, q, 'national', 'all firms', v, se, V_OLD, URL['old'])
for keys, q, sm, v, se in sheet_pairs(R + 'AI_Core_Questions.xlsx', 'Employment Size Estimates', 'Employment Size SE', 1):
    if keys[0] in SIZE: emit(sm, q, 'employment_size', SIZE[keys[0]], v, se, V_OLD, URL['old'])
for keys, q, sm, v, se in sheet_pairs(R + 'AI_Core_Questions.xlsx', 'Sector Estimates', 'Sector SE', 1):
    c = str(keys[0]); emit(sm, q, 'sector', f'{c} {SECTOR.get(c, c)}', v, se, V_OLD, URL['old'])
# new series
for keys, q, sm, v, se in sheet_pairs(R + 'National.xlsx', 'Response Estimates', 'Response Standard Errors', 0):
    emit(sm, q, 'national', 'all firms', v, se, V_NEW, URL['new'])
for keys, q, sm, v, se in sheet_pairs(R + 'Employment_Size_Class.xlsx', 'Response Estimates', 'Response Standard Errors', 1):
    if keys[0] in SIZE: emit(sm, q, 'employment_size', SIZE[keys[0]], v, se, V_NEW, URL['new_size'])
for keys, q, sm, v, se in sheet_pairs(R + 'Sector.xlsx', 'Response Estimates', 'Response Standard Errors', 1):
    c = str(keys[0])
    if c in SECTOR: emit(sm, q, 'sector', f'{c} {SECTOR[c]}', v, se, V_NEW, URL['new_sector'])
# sector x size: smallest class (1-4 employees) in the latest period only
LATEST = max(r['smpdt'] for r in rows)
for keys, q, sm, v, se in sheet_pairs(R + 'Sector_by_Employment_Size_Class.xlsx', 'Response Estimates', 'Response Standard Errors', 2):
    c = str(keys[0])
    if sm == LATEST and keys[1] == 'A' and c in SECTOR:
        emit(sm, q, 'sector_x_size_1-4', f'{c} {SECTOR[c]}', v, se, V_NEW, URL['new_sxs'])

# AI supplement 2026 (pooled 2025-11-17 to 2026-02-08)
wb = openpyxl.load_workbook(R + 'AI_Supplement_Table_2026.xlsx', read_only=True)
SCOPE = {1: 'all firms', 2: 'firms using AI in any function', 3: 'firms where AI did employee tasks',
         4: 'firms whose employees used generative AI', 5: 'firms planning AI use next 6 months',
         6: 'firms not planning AI use next 6 months'}
SQ = {2: 'supp_function_used_ai_last_6_months', 3: 'supp_ai_vs_employee_tasks', 4: 'supp_tasks_replaced_amount',
      6: 'supp_ai_effect_on_total_employment', 8: 'supp_employees_used_ai_any_task', 9: 'supp_employees_used_genai',
      10: 'supp_genai_task', 12: 'supp_function_plan_next_6_months', 13: 'supp_reason_not_planning_ai',
      1: 'supp_used_ai_last_2_weeks', 11: 'supp_expect_ai_next_6_months', 7: 'supp_changes_made_to_use_ai', 5: 'supp_ai_replaced_software'}
def supp(sheet, sesheet, k, btype, keep):
    E = list(wb[sheet].iter_rows(values_only=True)); S = list(wb[sesheet].iter_rows(values_only=True))
    for r, sr in zip(E[1:], S[1:]):
        if not r or r[k + 1] is None or not isinstance(r[k + 1], int): continue
        key = r[:k]
        if not keep(key): continue
        scope, qid, ans = r[k], r[k + 1], r[k + 4]
        if qid not in SQ: continue
        if r[k + 6] is not None:  # yes/no/dk matrix questions: keep Yes column
            v, s = r[k + 6], sr[k + 6]
        else:
            v, s = r[k + 5], sr[k + 5]
            if qid in (1, 11, 8, 9, 5) and ans != 'Yes': continue
        p, note = pct(v)
        if p is None: continue
        bval = 'all firms' if btype == 'national' else (SIZE[key[0]] if btype == 'employment_size' else f'{key[0]} {SECTOR.get(str(key[0]), key[0])}')
        rows.append(dict(period_start='2025-11-17', period_end='2026-02-08', measure=SQ[qid] + ': ' + str(ans),
                         breakdown_type=btype, breakdown_value=bval, pct=p, se_pct=(pct(s)[0] or ''), smpdt='AI supplement 2026 (pooled 6 panels)',
                         collection_start='2025-11-17', collection_end='2026-02-08',
                         question_version='AI supplement 2026; base = ' + SCOPE.get(scope, str(scope)),
                         source_url=URL['supp'], checked_on=CHECKED,
                         note='; '.join(x for x in [note, 'period = collection window (supplement pooled; questions refer to last 2 weeks / last 6 months / next 6 months as worded)'] if x)))
supp('National Response Estimates', 'National Standard Errors', 0, 'national', lambda k: True)
supp('Employment Response Estimates', 'Employment Standard Errors', 1, 'employment_size', lambda k: k[0] in SIZE)

cols = ['period_start', 'period_end', 'measure', 'breakdown_type', 'breakdown_value', 'pct', 'source_url', 'checked_on',
        'se_pct', 'smpdt', 'collection_start', 'collection_end', 'question_version', 'note']
rows.sort(key=lambda r: (r['measure'].startswith('supp'), r['breakdown_type'], r['breakdown_value'], r['measure'], r['period_start']))
with open(D + '/data.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows), 'rows; latest smpdt', LATEST)
