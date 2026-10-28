import re,html,sys,json,glob,os
import xml.etree.ElementTree as ET
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
ns={'a':'http://www.w3.org/2005/Atom'}
rows=[]
for f in sorted(glob.glob(os.path.join(sys.argv[1],'*.rss'))):
    sub=os.path.basename(f)[:-4]
    try: root=ET.parse(f).getroot()
    except Exception as e: print('ERR',f,e); continue
    for i,e in enumerate(root.findall('a:entry',ns)):
        c=e.find('a:content',ns); t=html.unescape(c.text or '') if c is not None else ''
        t=re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',r'\2',t,flags=re.S)
        t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t).strip()
        link=e.find('a:link',ns).get('href')
        rows.append(dict(sub=sub,rank=i+1,date=(e.findtext('a:published',default='',namespaces=ns) or e.findtext('a:updated',default='',namespaces=ns))[:10],title=e.findtext('a:title',default='',namespaces=ns),url=link,text=t))
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'moneyre.py')).read())
seen=set();cand=[]
for r in rows:
    if r['url'] in seen: continue
    seen.add(r['url'])
    t=r['title']+' \n '+r['text']; h=big(t)
    if any(v>=8000 for v in h) or re.search(r'(?i)six[- ]figure|seven[- ]figure|[67][- ]figure|\b\d+k\s*(mrr|arr|/mo|a month|per month|month)',t): cand.append(r)
print(len(rows),'posts',len(seen),'unique',len(cand),'candidates')
with open(sys.argv[2],'w') as f:
    for r in cand: f.write(json.dumps(r)+'\n')
