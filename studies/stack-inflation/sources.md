# Sources and method: stack-inflation

Checked on 2026-10-28. All prices are USD list prices for a US buyer, entry paid plan, before tax, with no promos or coupons.

## Method
- **2021 price:** the Wayback Machine snapshot of each vendor's pricing page nearest to mid-October 2021, found with `archive.org/wayback/available?timestamp=20211015` and the CDX API.
  - Many 2021 pricing pages load their prices with JavaScript, so the archived HTML shows no numbers. For those I used an archived official resource the page itself loaded, or the vendor's own archived product page:
    - Semrush: the pricing-page script.
    - Squarespace: the plans API response.
    - Help Scout: the page-data JSON.
    - Canva: the Canva Pro landing page.
  - Every one of those is linked in `data.csv`.
- **2026 price:** the live pricing page, rendered in headless Chromium on 2026-10-28. Billing toggles were clicked so both the monthly and the yearly price were seen. For Webflow, the values were read from the page's HTML data attributes.
- **Comparison basis:** `price_2021` and `price_2026` are both the price **when paying month to month**. The yearly-billed per-month price is kept in its own columns.
  - The exception is Mailchimp, which has no yearly option on either page.
  - The other exception is Shopify 2021: that page listed only $29/month.
- `pct_change` = (price_2026 − price_2021) / price_2021.
- **Stack total:** the sum of month-to-month prices for the 11 tools with a verified, like-for-like price in both years. It excludes Framer (not the same product in 2021) and the three tools without a 2021 price (Zapier, Typeform, Linktree).
- **Inflation benchmark:** US CPI-U, all items, not seasonally adjusted (BLS series CUUR0000SA0), from the BLS public API.
  - October 2021 was 276.589. September 2026, the latest available, was 336.940.
  - That is +21.8%.
  - Responses are saved in `work/bls_cpi_2021.json` and `work/bls_cpi.json`.
- Polite fetching: Wayback requests were spaced 8–15 s apart after a 429. The live vendor pages were fetched once each, about 3.5 s apart.

### User-Agent
The default was "the-actuals-research/0.1".
- For two replays (Canva and Semrush 2021) the Wayback replay's own JavaScript refused a non-browser UA. For those I used a Chrome UA string with "the-actuals-research/0.1" appended.
- Neither of those replays produced prices, so no data relies on them.

## Per-tool sources
| tool | 2021 source | 2026 source |
|---|---|---|
| Webflow | https://web.archive.org/web/20211021150629/https://webflow.com/pricing (Basic $12 annual, "$15 paid monthly") | https://webflow.com/pricing (Basic `data-monthly-price="25"` `data-yearly-price="15"`) |
| Framer | https://web.archive.org/web/20211016190335/https://www.framer.com/pricing/ (Pro $20/editor annual, $25 when "Bill monthly") | https://www.framer.com/pricing (Basic $10 yearly, $15 monthly after toggling) |
| Mailchimp | https://web.archive.org/web/20211015171648/https://mailchimp.com/pricing/marketing/ (Essentials $9.99 for 500 contacts) | https://mailchimp.com/pricing/marketing/ (Essentials "starts at $13/month", 0–500 contacts) |
| Kit | https://web.archive.org/web/20211016031734/https://convertkit.com/pricing (Creator, 1,000 subs: $29 monthly, $25 yearly, $290/yr) | https://web.archive.org/web/20261026063941/https://kit.com/pricing (live site returned a Vercel bot checkpoint / HTTP 429). Creator, 1,000 subs: $33/mo billed yearly, $390/yr, "Save $78 per year", so monthly = $39 (derived) |
| Zapier | https://web.archive.org/web/20211016080744/https://zapier.com/pricing (price cards empty: prices come from a GraphQL call that was not archived; also checked the archived JS bundle and help-center articles, none state the plan price) | https://zapier.com/pricing (Professional "Starting from" $29.99 on "Pay monthly", $19.99 yearly) |
| Calendly | https://web.archive.org/web/20211011223600/https://calendly.com/pricing (Premium $8/mo with "Save $24 annually", so $10 monthly, derived) | https://calendly.com/pricing (Standard $10/seat/mo yearly, $12 after "Billed monthly") |
| Typeform | none: no Wayback snapshots exist for typeform.com/pricing (availability API empty; CDX 403) | https://www.typeform.com/pricing/ (Basic 39 USD/mo monthly; 28 USD/mo yearly) |
| Notion | https://web.archive.org/web/20211015043600/https://www.notion.so/pricing (FAQ text in page HTML: Personal Pro "$5 monthly or $48 yearly"; Team "$10 monthly or $96 yearly") | https://www.notion.com/pricing (Plus $10/seat yearly, $12 after "Pay monthly") |
| Canva | https://web.archive.org/web/20211008094717/https://www.canva.com/q/pro/ ("$119.99 when paid annually or $12.99 paid monthly, for up to 5 people"). The /pricing/ snapshot of 2021-10-16 renders only a browser-check page | https://www.canva.com/pricing/ (Pro US$144/year, US$18/month after the Monthly switch, "for one person") |
| Plausible | https://web.archive.org/web/20211015204745/https://plausible.io/ (10k pageviews: $6/mo, $60/yr) | https://plausible.io/#pricing (Starter, 10k: $9/month; $90/yr per the yearly toggle) |
| Semrush | https://web.archive.org/web/20211012003557/https://www.semrush.com/static/pricing_spa.878de84dfd5826f4cb6b.js (plan config `pro:{price:{monthly:119.95,annual:99.95}}`); page snapshot https://web.archive.org/web/20211017055128/https://www.semrush.com/prices/ | https://www.semrush.com/pricing/seo-ai-search/ (SEO plan $139.95/mo monthly; $117.33/mo billed annually) |
| Help Scout | https://web.archive.org/web/20211019122920/https://www.helpscout.com/pricing/ (Standard $20/user/mo annual) plus https://web.archive.org/web/20210624135338/https://www.helpscout.com/page-data/pricing/page-data.json (Standard monthly $25, annual $20) | https://www.helpscout.com/pricing/ (Standard $25 annual, $30 after "Monthly", per user) |
| Linktree | none: no Wayback snapshots exist for linktr.ee | https://linktr.ee/s/pricing (Starter "$7/mo billed annually, or $9 monthly") |
| Squarespace | https://web.archive.org/web/20211016055108/https://www.squarespace.com/api/billing/available-plans/product-types/website/current (Business P1M $26.00, P1Y $216.00) | https://www.squarespace.com/pricing (Core $29 annual, $39 after "Pay monthly") |
| Shopify | https://web.archive.org/web/20211015141750/https://www.shopify.com/pricing (Basic Shopify $29 USD per month) | https://www.shopify.com/pricing (Basic $29/mo yearly; $39/mo after selecting monthly) |
| CPI | https://api.bls.gov/publicAPI/v1/timeseries/data/ (CUUR0000SA0, Oct 2021) | same, Sep 2026 |

## Assumptions and choices
- **Entry paid plan.** I used the cheapest self-serve paid plan that a one-person business would buy in each year. Where the vendor renamed the plan, I matched the successor tier:
  - Calendly: Premium → Standard.
  - Semrush: Pro → SEO.
  - Squarespace: Business → Core.
  - Notion: Personal Pro → Plus.
  - ConvertKit → Kit (company rename).
- **Notion is the judgement call that matters most.** Plus did not exist in 2021. A solo user's cheapest paid plan then was Personal Pro at $5, and in 2026 it is Plus at $12 (+140%). Against 2021 Team ($10 monthly), the closest predecessor of Plus, the change is +20%. Both are in the notes.
- **Per-seat tools** (Calendly, Notion, Help Scout) are counted at 1 seat.
- **Tier-based tools are held at the same usage level:**
  - Mailchimp: 500 contacts.
  - Kit: 1,000 subscribers.
  - Plausible: 10k pageviews.
- **Payment processing fees** (Squarespace, Shopify card rates) are excluded. Prices are subscription only.
- **Two monthly prices are derived arithmetic**, not read directly as a monthly figure; both are labelled `derived` in the notes:
  - Calendly 2021: $10 = $8 + $24/12.
  - Kit 2026: $39 = ($390 + $78)/12.
- Canva 2021's yearly per-month figure ($10.00) is $119.99/12, rounded.

## Not verified (left blank)
- Zapier 2021, Typeform 2021 and Linktree 2021: the reasons are in the table above.
