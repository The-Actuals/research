"""Merge coded batches into reddit_posts.csv and print summary stats.
Run: python3 -I scripts/merge_reddit.py STUDYDIR"""
import sys, csv, json, glob, collections, re
D = sys.argv[1]
CHECKED = '2026-10-28'
FEED = 'https://www.reddit.com/r/{}/top/.rss?t=year&limit=100'
FOUNDER_SUBS = {'Entrepreneur', 'EntrepreneurRideAlong', 'smallbusiness', 'solopreneur', 'SideHustleGold', 'youngentrepreneur',
                'indiehackers', 'microsaas', 'startups', 'Entrepreneurs', 'growmybusiness'}
TASKS = ['customer support', 'lead gen/outreach', 'content/marketing', 'sales calls', 'bookkeeping/admin',
         'coding/building the product', 'research', 'operations/scheduling', 'other']
# all posts in feeds (denominators)
feed = {}
for r in csv.DictReader(open(D + '/work/feed_index.csv', newline='')):
    feed[r['url']] = r
rows = []
for f in sorted(glob.glob(D + '/work/coded_g*.csv')):
    rows += list(csv.DictReader(open(f, newline='')))
OV = list(csv.DictReader(open(D + '/work/overrides.csv', newline='')))
for r in rows:
    for o in OV:
        if o['url_contains'] in r['url']:
            r[o['field']] = o['value']
            if o['field'] == 'category' and o['value'] not in ('own_ops', 'client_deploy'):
                for k in ['business_type', 'task', 'tasks_all', 'tool_named', 'claimed_result', 'result_metric', 'result_value', 'result_unit', 'result_period', 'sentiment']: r[k] = ''
seen = set(); out = []
for r in rows:
    if r['url'] in seen: continue
    seen.add(r['url'])
    r = {k: (v or '').strip() for k, v in r.items()}
    r['task'] = r['task'].lower()
    if r['category'] in ('own_ops', 'client_deploy') and r['task'] not in TASKS:
        print('BAD TASK', r['url'], r['task'])
    r['self_reported'] = 'yes'
    r['sub_group'] = 'founder_subs' if r['sub'] in FOUNDER_SUBS else 'AI_Agents'
    r['source_url'] = r['url']
    r['feed_url'] = FEED.format(r['sub'])
    r['checked_on'] = CHECKED
    m = re.search(r'/comments/[^/]+/([^/]+)/', r['url']); r['story_key'] = m.group(1) if m else r['url']
    out.append(r)
first = {}
for r in sorted(out, key=lambda r: (r['sub'], int(r['rank']))):
    k = r['story_key']
    r['duplicate_of'] = first.get(k, '')
    first.setdefault(k, r['url'])
cols = ['sub', 'sub_group', 'rank', 'published', 'url', 'title_short', 'category', 'business_type', 'task', 'tasks_all', 'tool_named',
        'claimed_result', 'result_metric', 'result_value', 'result_unit', 'result_period', 'sentiment', 'skeptical', 'promo_suspect',
        'self_reported', 'duplicate_of', 'notes', 'source_url', 'feed_url', 'checked_on']
out.sort(key=lambda r: (r['sub'], int(r['rank'])))
with open(D + '/reddit_posts.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(out)
print('coded rows', len(out), 'feed posts', len(feed))
cand = sum(1 for r in feed.values() if r['ai_keyword_hit'] == 'yes')
print('candidates', cand)
C = collections.Counter
use = [r for r in out if r['category'] in ('own_ops', 'client_deploy')]
for grp in ['founder_subs', 'AI_Agents', 'all']:
    sel = [r for r in out if grp == 'all' or r['sub_group'] == grp]
    u = [r for r in sel if r['category'] in ('own_ops', 'client_deploy')]
    nfeed = sum(1 for x in feed.values() if grp == 'all' or (('founder_subs' if x['sub'] in FOUNDER_SUBS else 'AI_Agents') == grp))
    print(f'\n== {grp}: feed posts {nfeed}, keyword candidates {len(sel)}, use posts {len(u)}')
    print(' categories', C(r['category'] for r in sel).most_common())
    print(' primary task', C(r['task'] for r in u).most_common())
    at = C(t.strip().lower() for r in u for t in r['tasks_all'].split(';') if t.strip())
    print(' any-mention task', at.most_common())
    print(' sentiment', C(r['sentiment'] for r in u).most_common())
    print(' result_metric', C(r['result_metric'] for r in u).most_common())
    print(' skeptical (all candidates)', C(r['skeptical'] for r in sel).most_common())
    print(' promo_suspect among use', C(r['promo_suspect'] for r in u).most_common())
    print(' by sub use', C(r['sub'] for r in u).most_common())
    print(' business_type', C(r['business_type'] for r in u).most_common(15))
print('\n per-task sentiment (all use):')
for t in TASKS:
    s = C(r['sentiment'] for r in use if r['task'] == t)
    if s: print(' ', t, dict(s))

uniq = [r for r in use if not r['duplicate_of']]
print('\nunique use stories', len(uniq), 'dupes', len(use) - len(uniq))
fu = [r for r in uniq if r['sub_group'] == 'founder_subs']
print('founder unique', len(fu), C(r['task'] for r in fu).most_common())
print('founder unique sentiment', C(r['sentiment'] for r in fu).most_common())
np_ = [r for r in fu if r['promo_suspect'] == 'no']
print('founder unique non-promo', len(np_), C(r['sentiment'] for r in np_).most_common(), C(r['task'] for r in np_).most_common())
au = [r for r in uniq if r['sub_group'] == 'AI_Agents']
print('AI_Agents unique', len(au), C(r['task'] for r in au).most_common(), C(r['sentiment'] for r in au).most_common())
sk = [r for r in out if r['skeptical'] == 'yes' and not r['duplicate_of']]
print('skeptical unique', len(sk), C(r['sub_group'] for r in sk), C(r['category'] for r in sk).most_common())
fc = [r for r in out if r['sub_group']=='founder_subs' and not r['duplicate_of']]
print('founder unique candidates', len(fc), C(r['category'] for r in fc).most_common())
# summary table for the chart
with open(D + '/reddit_task_summary.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['sub_group', 'task', 'posts_primary', 'posts_any_mention', 'worked', 'mixed', 'failed', 'unclear', 'promo_suspect', 'base_unique_use_posts', 'source_url', 'checked_on'])
    for grp, sel in [('founder_subs', fu), ('AI_Agents', au), ('all', uniq)]:
        for t in TASKS:
            pr = [r for r in sel if r['task'] == t]
            am = sum(1 for r in sel if t in [x.strip().lower() for x in r['tasks_all'].split(';')])
            sc = C(r['sentiment'] for r in pr)
            w.writerow([grp, t, len(pr), am, sc['worked'], sc['mixed'], sc['failed'], sc['unclear'], sum(1 for r in pr if r['promo_suspect'] == 'yes'), len(sel), 'reddit_posts.csv (see url column)', CHECKED])
