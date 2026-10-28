import re,html,sys
t=open(sys.argv[1],errors='ignore').read()
t=re.sub(r'<(script|style).*?</\1>','',t,flags=re.S)
t=re.sub(r'<[^>]+>','\n',t); t=html.unescape(t)
t=re.sub(r'\s*\n\s*','\n',t)
print('LEN',len(t))
seen=set()
for m in re.finditer(r'(?i)scrap|crawl|spider|robot|data min|harvest|automated means|automated (system|tool|software)',t):
  k=m.start()//500
  if k in seen: continue
  seen.add(k)
  print('...',t[max(0,m.start()-400):m.start()+300].replace('\n',' '),'\n')
