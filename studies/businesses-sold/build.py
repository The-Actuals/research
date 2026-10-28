import json,glob,csv,collections,datetime,statistics as st
R='raw/ef/'
L={}; months={}
for f in sorted(glob.glob(R+'m_*.json')):
    mo=f.split('m_')[1][:7]
    for x in json.load(open(f))['data']['listings']:
        n=x['listing_number']; L[n]=x
        months.setdefault(n,[]).append(mo)
def btype(ms,plat):
    s=set(ms)
    if 'SaaS' in s: return 'SaaS',''
    if 'Application' in s: return 'app',''
    if s&{'Amazon FBA','Amazon FBM'}: return 'ecommerce/Amazon FBA',''
    if s&{'eCommerce','DropShipping'}: return 'ecommerce/Shopify DTC', ('Shopify' if 'Shopify' in plat else 'non-Shopify DTC store')
    if 'YouTube' in s: return 'YouTube/media',''
    if s&{'Agency','Service','Lead Gen'}: return 'agency/service',''
    content=s&{'Display Advertising','Affiliate','Amazon Associates'}
    if s&{'Amazon KDP','Amazon Merch'} and not content: return 'other','Amazon KDP/Merch royalties'
    if content: return 'content/affiliate site',''
    if 'Newsletter' in s: return 'newsletter',''
    return 'other','digital/info product or subscription'
rows=[]
for n,x in sorted(L.items()):
    ms=[m['monetization'] for m in x['monetizations']]
    plat=sorted(set(s['platform'] for s in x['sites']))
    bt,sub=btype(ms,plat)
    mo=sorted(months[n])[-1]  # boundary dupes: sold_at = 1st of later month
    price=x.get('listing_price'); ap=x['average_annual_net_profit']
    fl=x['first_listed_at'][:10] if x.get('first_listed_at') else ''
    fm=x.get('first_made_money_at') or ''
    age=''
    if fl and fm:
        age=round((datetime.date.fromisoformat(fl)-datetime.date.fromisoformat(fm)).days/365.25,1)
    rec=round(price/ap,2) if price and ap and ap>0 else ''
    rows.append(dict(
      source='Empire Flippers public Marketplace API',
      listing_id=n,
      source_url=f'https://empireflippers.com/listing/{n}/',
      api_url=f'https://api.empireflippers.com/api/v1/listings/list?listing_number={n}',
      listing_status='Sold',
      business_type=bt, business_subtype=sub,
      monetization='; '.join(ms), niche='; '.join(m['niche'] for m in x['niches']),
      platform='; '.join(plat),
      price_usd=price if price else '',
      price_type='asking' if price else '',
      price_note='last public listing price of a deal that closed; actual sale price not published (EF scoreboard: sold at 86% of list on average)' if price else 'unpriced listing',
      monthly_net_profit_usd=x['average_monthly_net_profit'],
      annual_net_profit_usd=ap,
      profit_basis=f"{x['listing_multiple_type']} net profit, avg of {x.get('pricing_period_months') or ''} months",
      multiple_published_annual=x.get('annual_listing_multiple') or '',
      multiple_published_monthly=x.get('listing_multiple') or '',
      multiple_recomputed_annual=rec,
      monthly_revenue_usd=x['average_monthly_gross_revenue'],
      profit_margin_pct=x.get('profit_margin'),
      business_age_years=age, age_basis='first_made_money_at to first_listed_at',
      first_made_money_at=fm,
      owner_hours_per_week=x.get('hours_worked_per_week'),
      traffic_source='',
      net_profit_trend_pct_12m=x.get('net_profit_trend_percent'),
      days_on_marketplace=x.get('days_on_marketplace'),
      first_listed_at=fl, sold_month=mo,
      sold_month_note='boundary: appeared in two month filters, sold_at = first day of later month' if len(months[n])>1 else '',
      country=x.get('country'),
      checked_on='2026-10-28'))
with open('data.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
