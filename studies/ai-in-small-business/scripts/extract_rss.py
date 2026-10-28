"""Parse top-of-year Atom feeds into JSONL (title, url, rank, published, plain text) + AI keyword flag.
Usage: python3 -I extract_rss.py RAWDIR OUTDIR sub1 sub2 ..."""
import sys, re, json, html, xml.etree.ElementTree as ET
raw, out = sys.argv[1], sys.argv[2]
NS = {'a': 'http://www.w3.org/2005/Atom'}
KW = re.compile(r"\b(ai|a\.i\.|llms?|gpt|chatgpt|claude|gemini|copilot|openai|anthropic|agents?|agentic|automat\w*|n8n|zapier|make\.com|voice ?bot|chatbot|bots?|cursor|lovable|bolt|replit|vibe ?cod\w*|midjourney|perplexity|grok|deepseek|machine learning|prompt\w*|artificial intelligence)\b", re.I)
def strip(h):
    h = re.sub(r'(?s)<!-- SC_OFF -->|<!-- SC_ON -->', '', h)
    h = re.sub(r'(?s)&#32; submitted by.*$', '', html.unescape(h)) if False else h
    t = re.sub(r'(?s)<[^>]+>', ' ', h)
    t = html.unescape(t)
    t = re.sub(r'submitted by\s+/u/\S+.*$', '', t, flags=re.S)
    return re.sub(r'\s+', ' ', t).strip()
summary = {}
for sub in sys.argv[3:]:
    try:
        root = ET.parse(f'{raw}/{sub}.rss').getroot()
    except Exception as e:
        summary[sub] = f'ERROR {e}'; continue
    rows = []
    for i, e in enumerate(root.findall('a:entry', NS), 1):
        title = e.findtext('a:title', '', NS)
        link = e.find('a:link', NS).get('href')
        pub = e.findtext('a:published', '', NS)
        body = strip(e.findtext('a:content', '', NS))
        txt = title + ' ' + body
        kws = sorted(set(m.lower() for m in KW.findall(txt)))
        rows.append(dict(sub=sub, rank=i, title=title, url=link, published=pub[:10], words=len(body.split()), kw=kws, ai_hits=len(KW.findall(txt)), text=body[:6000]))
    with open(f'{out}/{sub}.jsonl', 'w') as f:
        for r in rows: f.write(json.dumps(r) + '\n')
    summary[sub] = (len(rows), sum(1 for r in rows if r['ai_hits']), rows[0]['published'] if rows else None, min((r['published'] for r in rows), default=None), max((r['published'] for r in rows), default=None))
for k, v in summary.items(): print(k, v)
