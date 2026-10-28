import sys, openpyxl
f=sys.argv[1]; sheet=sys.argv[2]; qcol=int(sys.argv[3])
wb=openpyxl.load_workbook(f, read_only=True)
rows=list(wb[sheet].iter_rows(values_only=True))
print(rows[0][:qcol+3], '... cols', len(rows[0]), 'first/last period', rows[0][qcol+3], rows[0][-1])
seen=set()
for r in rows[1:]:
    if r[qcol-1] not in seen:
        seen.add(r[qcol-1]); print(r[qcol-1], '|', r[qcol])
