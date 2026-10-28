import re
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
