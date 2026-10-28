import json,glob,csv,re,os,sys,collections
W='work'
FX={'USD':1,'EUR':1/0.89823,'GBP':1/0.75258,'CAD':1/1.4047,'AUD':1/1.4219,'INR':1/95.22}
PER={'month':1,'year':1/12,'week':52/12,'day':365/12,'quarter':1/3}
inp={}
for f in sorted(glob.glob(W+'/batch_*.jsonl')):
    for l in open(f):
        x=json.loads(l); inp[x['id']]=x
coded=[];missing=[]
for f in sorted(glob.glob(W+'/coded_*.jsonl')):
    for l in open(f):
        l=l.strip()
        if l: coded.append(json.loads(l))
ids={c['id'] for c in coded}
missing=[i for i in inp if i not in ids]
print('input',len(inp),'coded',len(coded),'missing',len(missing))
def num(v):
    try: return float(str(v).replace(',','').replace('$',''))
    except: return None
rows=[];excl=collections.Counter();exrows=[]
for c in coded:
    src=inp.get(c['id'])
    if not src: continue
    if str(c.get('include'))!='1':
        excl[(c.get('exclude_reason') or '').split()[0] if c.get('exclude_reason') else 'blank']+=1
        exrows.append(dict(id=c['id'],source_url=src['source_url'],exclude_reason=c.get('exclude_reason','')))
        continue
    amt=num(c.get('revenue_amount')); cur=(c.get('revenue_currency') or 'USD').upper(); per=(c.get('revenue_period') or '').lower()
    m=None;basis=''
    if amt is not None and cur in FX and per in PER:
        m=round(amt*FX[cur]*PER[per]); basis=f"{c.get('revenue_metric','')} {amt:g} {cur}/{per}"+(' ->USD@ECB 2026-10-28' if cur!='USD' else '')+('' if per=='month' else f' normalized x{PER[per]:.4g}')
    rows.append(dict(c=c,src=src,m=m,basis=basis))
print('included raw',len(rows)); print('excluded',sum(excl.values()),excl.most_common())
json.dump(dict(rows=rows,exrows=exrows),open(W+'/merged.json','w'))
