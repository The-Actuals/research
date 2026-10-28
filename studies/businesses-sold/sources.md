# businesses-sold: sources and method

Checked on 2026-10-28. User-Agent "the-actuals-research/0.1", at least 3 s between requests to the same host. The API's own limit is 1 request per second.

## Source used for rows

**Empire Flippers public Marketplace API**
- Docs: https://empireflippers.com/marketplace-api/
- Endpoint: `GET https://api.empireflippers.com/api/v1/listings/list?listing_status=Sold&sold_at_from=...&sold_at_to=...&limit=100`
- Permission:
  - The docs say "no authentication is required."
  - They describe the API as returning listings that are "publicly visible."
  - Allowed uses include "syndicate those listings on your own website" and "use the data personally as a buyer."
  - robots.txt only disallows `/wp-admin/`.
  - The Terms of Use have no clause on scraping or automated access (https://empireflippers.com/empire-flippers-terms-use-agreement/, effective 2025-11-08; searched for scrape, crawl, robot, automat, spider, data min, harvest).
- Window: 22 monthly queries by `sold_at`, from 2025-01-01 to 2026-11-01. Each month fit on one page (maximum 28 rows).
- Raw JSON: `raw/ef/m_YYYY-MM-01.json`.
- Result: **294 unique sold listings**. 292 have a price. 2 are "unpriced" (#87195, #88520) and are kept with a blank price.
- Per-row link: `https://empireflippers.com/listing/<listing_number>/`. I checked that the format resolves (200, "Listing #94091 | Empire Flippers").
- Per-row API check: `?listing_number=<n>`. I checked #73254 and it returned price 136702, status Sold.

**Aggregate cross-check: Empire Flippers Scoreboard** (https://empireflippers.com/scoreboard/, live page, checked 2026-10-28)
- "Average % of List Price Sold For": **86%**.
- Typical-business trailing-twelve-month (TTM) sold multiple: **2.2x**. This covers all sales except distressed ones.
- Premium: 2.4x. $1M+ premium: 3.2x. Distressed (1.5x or less): 1.1x.
- Average sale duration: 130 days.
- Listings sold: 2,682. This matches the API's sold count of 2,683 on the same day.

## Field definitions and assumptions
- `price_usd` is the **listing price of a deal that closed**.
  - Empire Flippers does not publish the actual sale price in the API. The response has no `sale_price` or `sale_multiple`, although `sale_multiple` exists as a sort key.
  - So **every row has `price_type = asking`**, with `listing_status = Sold`. There are no `price_type = sold` rows.
  - The scoreboard says the average deal closes at 86% of list. Any "sold-for" estimate would be list × 0.86, but that is an average, not a per-deal figure. It is not applied in data.csv.
- Profit (`monthly_net_profit_usd`, `annual_net_profit_usd`):
  - This is Empire Flippers' average net profit. `listing_multiple_type` = "SDE" for all 294 rows.
  - It is averaged over `pricing_period_months`. That period is 12 months for 261 rows, 6 to 11 months for 31 rows, and blank for the 2 unpriced rows.
  - SDE means owner pay is not deducted.
- Multiples:
  - `multiple_published_annual` is the API's `annual_listing_multiple` (price ÷ annual profit).
  - `multiple_published_monthly` is the API's `listing_multiple` (price ÷ monthly profit, the older "35x"-style figure).
  - `multiple_recomputed_annual` = price_usd / annual_net_profit_usd. It matches the published annual figure within 0.02 on all 292 priced rows.
- `business_type` is normalized from the EF `monetizations` list, using the first rule that matches:
  1. SaaS
  2. Application → app
  3. Amazon FBA/FBM → ecommerce/Amazon FBA
  4. eCommerce or DropShipping → ecommerce/Shopify DTC (31 of 35 are on Shopify. The other 4 are DTC stores on other platforms; see `platform`)
  5. YouTube → YouTube/media
  6. Agency, Service or Lead Gen → agency/service
  7. Amazon KDP or Merch with no ad/affiliate income → other (subtype "Amazon KDP/Merch royalties")
  8. Display Advertising, Affiliate or Amazon Associates → content/affiliate site
  9. Newsletter
  10. Anything else → other (digital/info product or subscription)

  The raw monetizations stay in `monetization`.
- `business_age_years` runs from `first_made_money_at` to `first_listed_at`, so it is the age when listed.
- `owner_hours_per_week` is EF's `hours_worked_per_week`, which is self-reported by the seller.
- `traffic_source` is blank. The public API has no traffic-source field; it has only the site platform and optional Semrush data.
- `sold_month`: the month filter is inclusive at both ends.
  - 11 listings showed up in two adjacent months. That means `sold_at` was exactly 00:00 on the 1st, so they are assigned to the later month.
  - The exact sold date isn't exposed, so only the month is given.
- `days_on_marketplace` is the API field as given.

## Sources evaluated and skipped (no rows taken)

| Source | Why skipped | URL |
|---|---|---|
| Flippa | ToS: "you may not utilize any data mining, robots, or similar data gathering and extraction tools…" and may not "create and/or publish your own database" of its content | https://flippa.com/terms |
| Acquire.com | ToS forbids "any robot, spider or other automatic device… including monitoring or copying" and also any manual copying | https://acquire.com/terms/ |
| Microns.io | ToS: "You agree not to crawl, scrape, or spider any page of the Services" | https://www.microns.io/terms |
| FE International | Terms allow personal reference only: "You must not use any part of the materials on the Website for commercial purposes without obtaining a licence" | https://www.feinternational.com/terms |
| Quiet Light | The terms page returned a Cloudflare "Just a moment..." bot challenge, so I couldn't review the terms. Treated as automated access not invited | https://quietlight.com/terms-of-use/ |
| Motion Invest | robots.txt disallows `/marketplace/` and `/marketplace?*`. The terms page is a JavaScript app and returned no readable text | https://motioninvest.com/robots.txt |

Broker annual reports: the only aggregate used is the EF Scoreboard above. Other brokers' reports weren't used, because their sites' terms (above) restrict reuse, or I couldn't read their terms.

## Scripts
- `build.py`: raw JSON → data.csv
- `analyze.py`: banded medians and Spearman correlations used in findings.md
- `txt.py`: HTML-to-text helper used to read the terms pages
