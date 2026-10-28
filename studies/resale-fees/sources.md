# resale-fees: sources, method, assumptions

Checked 2026-10-28 unless the row says otherwise. Fetched with User-Agent `the-actuals-research/0.1`, at least 3 s apart per host. Raw copies are in `_raw/`.

## Method and assumptions
- One $100 item sold by a US individual (not a business seller) to a US buyer in October 2026, standard account, no promos, no boosting or ads unless shown in `kept_range`.
- **Shipping assumption:** where the seller sets shipping (eBay, Mercari, Depop, Facebook, Etsy), the seller offers free shipping, so the buyer pays $100 total. The seller's postage cost is not subtracted, because it is the same whatever the app. Where the app always bills the buyer for shipping (Poshmark, Vinted), the $100 is the item price and the buyer pays shipping on top.
- **Sales tax:** not counted in the headline. eBay, Depop and Facebook charge their fee on tax-inclusive totals, and Etsy's processing fee also covers tax. The eBay and Depop rows show an 8% tax example.
- Payout/withdrawal fees are excluded unless stated as free.
- `kept_from_100` = 100 - percentage fees - fixed fees.

## Sources
| Platform | URL | Key text |
|---|---|---|
| eBay | https://www.ebay.com/help/selling/fees-credits-invoices/selling-fees?id=4822 | Most categories: 13.6% on total amount of the sale up to $7,500, 2.35% above; per-order fee $0.30 (orders of $10 or less) / $0.40 (over $10); total includes shipping, handling and sales tax; no third-party processing fees |
| Poshmark | https://blog.poshmark.com/category/for-sellers/seller-updates/ (FAQ block) | "U.S Poshmark charges a flat $2.95 on any sale under $15, and a straightforward 20% commission on sales of $15 or more." Support article https://support.poshmark.com/s/article/297755057 failed TLS verification for both our fetcher and WebFetch |
| Mercari | https://www.mercari.com/us/help_center/article/169/ | Since 2025-01-06: 10% selling fee on item price + buyer-paid shipping; no payment processing fee; buyer pays 3.6% Buyer Protection |
| Depop | https://depophelp.zendesk.com/hc/en-gb/articles/360001791127-Seller-fees-and-charges | No selling fee for UK/US/AUS sellers; US processing 3.3% + $0.45 on price + shipping + tax; boosting fee 12% (UK/US new listings from 2026-03-23) |
| Depop (context) | https://news.depop.com/company-news/depop-removes-selling-fees-in-the-united-states-evolves-fee-structure/ | Announcement of the US selling-fee removal |
| Facebook Marketplace | https://www.facebook.com/legal/checkout_terms (last modified 2026-05-26) | "Marketplace: 10%, with a minimum fee of $0.80"; calculated on the entire transaction; payment-provider fees may be separate |
| Facebook (conflict) | https://www.facebook.com/marketplace/sell-with-shipping/ | "The Marketplace selling fee is only 5%" (undated marketing page) |
| OfferUp shipping | https://help.offerup.com/hc/en-us/articles/41043186552980-Nationwide-shipping-ending (updated 2026-09-22) | Local, in-person only; no new shipped listings from 2025-09-23; shipping removed by 2025-10-21 |
| OfferUp fees | https://help.offerup.com/hc/en-us/articles/360031989092-What-is-OfferUp | Core features free; paid promotions, extra listings, Premium |
| Vinted | https://www.vinted.com/help/373-is-selling-on-vinted-free | No fees for uploading or selling; full price goes to the Vinted Wallet |
| Vinted buyer fee | https://www.vinted.com/help/342-service-fee-on-vinted and https://www.vinted.com/help/1653 | Buyer-paid Vinted fee, typically 5% + $0.70; "There are no selling fees on Vinted" |
| Etsy | https://web.archive.org/web/20261024151150/https://www.etsy.com/legal/fees/ (snapshot 2026-10-24; live page 403) | $0.20 listing; 6.5% transaction fee on price + shipping + gift wrap; Offsite Ads 15%/12% |
| Etsy processing | https://web.archive.org/web/20261011064314/https://www.etsy.com/legal/etsy-payments/ (snapshot 2026-10-11) | United States 3% + 0.25 USD, on the total including tax and shipping |

## Calculations
- eBay: 100 - 13.60 - 0.40 = 86.00; with 8% tax: 100 - 0.136 x 108 - 0.40 = 84.91
- Poshmark: 100 - 20 = 80.00
- Mercari: 100 - 10 = 90.00
- Depop: 100 - 3.30 - 0.45 = 96.25; 8% tax: 100 - 0.033 x 108 - 0.45 = 95.99; boosted: 96.25 - 12 = 84.25
- Facebook shipped: 100 - 10 = 90.00 (95.00 if the 5% marketing figure applies)
- Etsy: 100 - 0.20 - 6.50 - 3.00 - 0.25 = 90.05; Offsite Ads: 75.05

## Not verified / caveats
- Facebook local pickup at $100.00 is inferred from the scope of the Checkout Terms. No page says outright that local sales are fee-free.
- Facebook shipped fee: the legal terms (10%) and the marketing page (5%) disagree.
- OfferUp shipped is blank because the option no longer exists.
- Vinted withdrawal fees and Mercari Instant Pay fees not verified.
