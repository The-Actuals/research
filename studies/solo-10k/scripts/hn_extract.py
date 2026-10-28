import json,glob,re,html,sys,csv,os
base=sys.argv[1]; out=sys.argv[2]
def clean(t):
    t=t or ''
    t=re.sub(r'<p>','\n',t); t=re.sub(r'<a [^>]*href="([^"]+)"[^>]*>.*?</a>',r'\1',t,flags=re.S)
    t=re.sub(r'<[^>]+>','',t); return html.unescape(t).strip()
rows=[]
def walk(n,thread,ttitle,depth):
    for c in n.get('children') or []:
        if c.get('type')=='comment' and c.get('text'):
            rows.append(dict(thread_id=thread,thread_title=ttitle,comment_id=c['id'],date=c['created_at'][:10],depth=depth,text=clean(c['text'])))
        walk(c,thread,ttitle,depth+1)
for f in sorted(glob.glob(os.path.join(base,'*.json'))):
    d=json.load(open(f)); walk(d,d['id'],d.get('title'),0)
# money prefilter
num=r'(\d{1,3}(?:[,.]\d{3})+|\d+(?:\.\d+)?)\s*(k|K|m|M|mm|MM|million|thousand)?'
cur=re.compile(r'(?:[$€£]|USD|EUR|GBP)\s*'+num+r'|'+num+r'\s*(?:USD|EUR|GBP|usd|eur|dollars|euros|bucks)')
def big(t):
    hits=[]
    for m in re.finditer(r'(?:[$€£]|USD ?|EUR ?|GBP ?)\s*(\d{1,3}(?:[,.]\d{3})+|\d+(?:\.\d+)?)\s*(k|K|m|M|mm|MM|million|thousand)?|(\d{1,3}(?:[,.]\d{3})+|\d+(?:\.\d+)?)\s*(k|K|m|M|million|thousand)?\s*(?:USD|EUR|GBP|usd|eur|dollars|euros|bucks|MRR|ARR|mrr|arr|/mo|/month| ?per month| a month| monthly|/yr|/year| per year| a year)',t):
        n=(m.group(1) or m.group(3)); u=(m.group(2) or m.group(4) or '')
        try: v=float(n.replace(',','')) if not re.match(r'^\d{1,3}\.\d{3}$',n) else float(n.replace('.',''))
        except: continue
        u=u.lower()
        if u in('k','thousand'): v*=1e3
        elif u in('m','mm','million'): v*=1e6
        hits.append(v)
    return hits
cand=[]
for r in rows:
    t=r['text']; h=big(t)
    flag = any(v>=8000 for v in h) or re.search(r'(?i)six[- ]figure|seven[- ]figure|7[- ]figure|6[- ]figure|full[- ]time income|ramen',t)
    if flag: cand.append(r)
print(len(rows),'comments;',len(cand),'candidates')
with open(out,'w') as f:
    for r in cand: f.write(json.dumps(r)+'\n')
