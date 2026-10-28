import csv,statistics as st,collections
R=list(csv.DictReader(open('data.csv')))
P=[r for r in R if r['price_usd'] and r['multiple_recomputed_annual']]
f=lambda r,k: float(r[k])
def summ(name,v):
    mm=sorted(f(r,'multiple_published_annual') for r in v)
    if not v: print(name,0); return
    print(f"{name:28s} n={len(v):3d} median_mult={st.median(mm):.2f} med_price={st.median(f(r,'price_usd') for r in v):,.0f} med_mo_profit={st.median(f(r,'monthly_net_profit_usd') for r in v):,.0f}")
def bins(key,edges,labels,rows=P):
    for (lo,hi),lab in zip(edges,labels):
        summ(lab,[r for r in rows if r[key]!='' and lo<=f(r,key)<hi])
print('== monthly profit bands'); bins('monthly_net_profit_usd',[(0,2000),(2000,5000),(5000,10000),(10000,25000),(25000,1e9)],['<$2k/mo','$2-5k/mo','$5-10k/mo','$10-25k/mo','$25k+/mo'])
print('== price bands'); bins('price_usd',[(0,50000),(50000,100000),(100000,250000),(250000,500000),(500000,1e6),(1e6,1e12)],['<$50k','$50-100k','$100-250k','$250-500k','$500k-1M','$1M+'])
print('== age'); bins('business_age_years',[(0,3),(3,5),(5,8),(8,100)],['<3y','3-5y','5-8y','8y+'])
print('== hours'); bins('owner_hours_per_week',[(0,5),(5,10),(10,20),(20,40),(40,1000)],['<5h','5-9h','10-19h','20-39h','40h+'])
print('== 12m profit trend'); bins('net_profit_trend_pct_12m',[(-1000,-20),(-20,0),(0,20),(20,10000)],['down >20%','down 0-20%','up 0-20%','up 20%+'])
print('== margin'); bins('profit_margin_pct',[(0,20),(20,40),(40,70),(70,101)],['<20%','20-40%','40-70%','70%+'])
print('== sold year'); 
for y in ['2025','2026']: summ(y,[r for r in P if r['sold_month'].startswith(y)])
T=[r for r in P if r['sold_month']>='2025-11']; summ('trailing12m (2025-11..2026-10)',T)
print('== hours by type (median hours)')
g=collections.defaultdict(list)
for r in P: g[r['business_type']+('|'+r['business_subtype'] if r['business_type']=='other' else '')].append(r)
for k,v in g.items(): print(k,len(v),'med hrs',st.median(f(r,'owner_hours_per_week') for r in v),'med age',st.median(f(r,'business_age_years') for r in v if r['business_age_years']),'med margin',st.median(f(r,'profit_margin_pct') for r in v), 'med days',st.median(f(r,'days_on_marketplace') for r in v))
mm=[f(r,'multiple_published_annual') for r in P]
print('min/max',min(mm),max(mm), 'share >=3x',sum(m>=3 for m in mm)/len(mm),'share <2x',sum(m<2 for m in mm)/len(mm))
pr=[f(r,'price_usd') for r in P]; print('price min/max',min(pr),max(pr))
# correlation spearman
def rank(v):
    s=sorted(range(len(v)),key=lambda i:v[i]); rk=[0]*len(v)
    for j,i in enumerate(s): rk[i]=j
    return rk
def sp(k):
    v=[r for r in P if r[k]!='']
    a=rank([f(r,k) for r in v]); b=rank([f(r,'multiple_published_annual') for r in v])
    return round(st.correlation(a,b),2),len(v)
for k in ['monthly_net_profit_usd','business_age_years','owner_hours_per_week','net_profit_trend_pct_12m','profit_margin_pct','days_on_marketplace']: print('spearman',k,sp(k))
print('days on market median',st.median(f(r,'days_on_marketplace') for r in P))
print('US share',sum(r['country']=='US' for r in P)/len(P))
print('months', collections.Counter(r['sold_month'] for r in R))
