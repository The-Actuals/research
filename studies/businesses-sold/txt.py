import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
if len(sys.argv)>2:
  for k in sys.argv[2].split(','):
    for m in re.finditer(k,t,flags=re.I):
      print('['+k+']',t[max(0,m.start()-int(sys.argv[3] if len(sys.argv)>3 else 300)):m.start()+400]); print('---')
else: print(t)
