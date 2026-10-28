import json,csv,re,collections,os
exec(open('scripts/merge.py').read().split("json.dump(dict(rows")[0])  # reuse merge logic -> rows, exrows
amap=json.load(open('work/authors.json'))
# manual overrides (documented in sources.md)
FORCE_EXCLUDE={}
for r in rows:
    a=amap.get(r['c']['id'],'')
    if 'heikka' in a.lower():
        FORCE_EXCLUDE[r['c']['id']]='team_not_solo: same author/family accounts state a co-founder (brother) in other posts'
OVR=json.load(open('work/overrides.json')) if os.path.exists('work/overrides.json') else {}
FORCE_EXCLUDE.update(OVR.get('exclude',{}))
out=[];
for r in rows:
    cid=r['c']['id']
    if cid in FORCE_EXCLUDE:
        exrows.append(dict(id=cid,source_url=r['src']['source_url'],exclude_reason='manual: '+FORCE_EXCLUDE[cid])); continue
    if r['m'] is None or r['m']<10000:
        exrows.append(dict(id=cid,source_url=r['src']['source_url'],exclude_reason=f"normalization: monthly={r['m']} below 10000 or unparseable")); continue
    out.append(r)
# dedupe: same author => same business group unless override says distinct
DISTINCT=set(OVR.get('distinct',[]))
groups=collections.defaultdict(list)
for r in out:
    a=amap.get(r['c']['id'],'') or r['c']['id']
    key=a if r['c']['id'] not in DISTINCT else r['c']['id']
    groups[key].append(r)
final=[]
gid=0
for k,g in groups.items():
    g.sort(key=lambda r:r['src']['date'])
    gid+=1
    for i,r in enumerate(g):
        r['dup_group']=f"g{gid:03d}" if len(g)>1 else ''
        r['in_stats']=1 if i==len(g)-1 else 0
        final.append(r)
final.sort(key=lambda r:(r['src']['source'],r['src']['date']))
def q(s): 
    s=(s or '').strip()
    return s if len(s.split())<=15 else ''
cols=['row_id','source','venue','post_date','claim_year','business_name','business_url','description','category','pricing_model','entry_price','entry_price_period','monthly_revenue_usd','revenue_metric','revenue_normalization','revenue_lower_bound','revenue_timing','revenue_verification','team_size','solo_basis','side_or_fulltime','founded_year','founded_basis','months_to_10k','months_to_10k_basis','growth_channels','primary_channel','tech','detail_level','dup_group','included_in_stats','notes','source_url','checked_on']
with open('data.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(cols)
    for i,r in enumerate(final,1):
        c=r['c'];s=r['src']
        notes=[]
        if q(c.get('revenue_quote')): notes.append('revenue: "'+q(c['revenue_quote'])+'"')
        if q(c.get('solo_quote')): notes.append('solo: "'+q(c['solo_quote'])+'"')
        if c.get('months_to_10k_note'): notes.append('clock: '+c['months_to_10k_note'])
        if c.get('notes'): notes.append(c['notes'])
        venue=s['context'].split(' | title:')[0] if s['source']=='reddit' else s['context'].replace('HN thread: ','HN: ').replace('HN comment on: ','HN: ')
        thin = (not c.get('category')) or len(s['text'])<300
        gc=';'.join(x.strip() for x in re.split(r'[;,]',c.get('growth_channels') or '') if x.strip())
        w.writerow([i,s['source'],venue,s['date'],s['date'][:4],c.get('business_name',''),c.get('business_url',''),c.get('description',''),c.get('category') or 'unclear',c.get('pricing_model',''),c.get('entry_price_usd',''),c.get('entry_price_period',''),r['m'],c.get('revenue_metric',''),r['basis'],c.get('revenue_lower_bound',''),c.get('revenue_timing',''),'self_reported',1,c.get('solo_basis',''),c.get('side_or_fulltime',''),c.get('founded_year',''),c.get('founded_basis',''),c.get('months_to_10k',''),c.get('months_to_10k_basis',''),gc,c.get('primary_channel',''),c.get('tech',''),'thin' if thin else 'detailed',r['dup_group'],r['in_stats'],' | '.join(notes),s['source_url'],'2026-10-28'])
with open('excluded.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['candidate_id','exclude_reason','source_url','checked_on'])
    for e in exrows: w.writerow([e['id'],e['exclude_reason'],e['source_url'],'2026-10-28'])
print('rows',len(final),'in_stats',sum(r['in_stats'] for r in final),'excluded',len(exrows))
