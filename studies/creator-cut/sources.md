# creator-cut: sources, method, assumptions

Checked 2026-10-28 unless the row says otherwise. Pages fetched with User-Agent `the-actuals-research/0.1`, at least 3 s apart per host. Raw copies are in `_raw/`.

## Method
- One row per platform (Apple has two rows: standard and small business).
- `kept_from_100` = what a US creator or seller keeps from $100 of gross revenue on that platform, after the platform's fee and any processing fee the platform passes on. It does **not** include payout or withdrawal fees, income tax, currency conversion or optional ads.
- For fan-payment platforms (Patreon, Substack, Kickstarter, Gumroad, Etsy), the $100 is **one** transaction. Fixed per-payment fees ($0.25 to $0.80) would weigh more if the $100 came as many small payments. Example: Patreon on 20 x $5 pledges = $100 - $10 - 20 x ($0.145 + $0.30) = $81.10 (worked example, not in the CSV).
- For ad-share and revenue-share platforms (YouTube, Shorts, Twitch, Steam, app stores), the $100 is $100 of the revenue base the platform splits (net ad revenue, Creator Pool allocation, net sub revenue, net game revenue, price minus tax).
- `kept_range` is filled only where an official alternative path changes the number a lot (Etsy Offsite Ads, Gumroad Discover, Upwork's variable fee).
- Standard plans only, no promos, US seller, US card buyer, no sales tax counted.

## Sources
| Platform | Source | What it says |
|---|---|---|
| YouTube | https://support.google.com/youtube/answer/72902 | 55% of net revenues from watch-page ads |
| YouTube Shorts | https://support.google.com/youtube/answer/12504220 | Creators keep 45% of allocated Creator Pool revenue; music split first; new 10M-view threshold from 2027-02-01 |
| Twitch | https://blog.twitch.tv/en/2024/01/24/an-update-to-several-streamer-payout-programs/ | Standard rate 50%; Plus levels 60/40 and 70/30; $100K cap removed. The help article (help.twitch.tv/s/article/partner-program-overview) is JavaScript-only and did not render; search index text says "baseline revenue share of 50/50 on the net revenue" |
| Patreon | https://web.archive.org/web/20261022193332/https://support.patreon.com/hc/en-us/articles/11111747095181-Creator-fees-overview (snapshot 2026-10-22; live page returns 403 to automated fetchers) | Standard 10% plan after 2025-08-04; USD card processing 2.9% + $0.30 for all payment sizes; $0.25 direct-deposit payout fee |
| Patreon pricing | https://www.patreon.com/pricing | 10% of income, plus processing, payout fees and taxes |
| Substack | https://support.substack.com/hc/en-us/articles/360037607131-How-much-does-Substack-cost | 10% + Stripe 2.9% + $0.30 + Stripe Billing 0.7% |
| OnlyFans | https://onlyfans.com/terms | "Our Fee is calculated as 20% of the total Fan Payment" |
| Apple standard | https://developer.apple.com/app-store/subscriptions/ | 70% of price in subscriber's first year, 85% after one year |
| Apple small business | https://developer.apple.com/app-store/small-business-program/ | 15% on paid apps and IAP, up to $1M proceeds |
| Google Play | https://support.google.com/googleplay/android-developer/answer/112622 | US/EEA/UK from 2026-06-30: first $1M of annual earnings = 10% + 5% billing fee (the table cell spans all three transaction-type columns; checked in the raw HTML because a summarizer misread it as 20% + 5%) |
| Etsy fees | https://web.archive.org/web/20261024151150/https://www.etsy.com/legal/fees/ (snapshot 2026-10-24; live page 403) | $0.20 listing, 6.5% transaction fee on price + shipping + gift wrap (not US sales tax), Offsite Ads 15%/12% |
| Etsy processing | https://web.archive.org/web/20261011064314/https://www.etsy.com/legal/etsy-payments/ (snapshot 2026-10-11) | United States: 3% + 0.25 USD |
| Kickstarter | https://web.archive.org/web/20261014055650/https://www.kickstarter.com/help/fees (snapshot 2026-10-14; live page 403) | 5% fee; 3% + $0.30 per pledge; pledges under $10 = 5% + $0.08 |
| Gumroad | https://gumroad.com/help/article/66-gumroads-fees and https://gumroad.com/pricing | 10% + $0.50 direct, excludes card processing (2.9% + $0.30); Discover 30% flat incl. processing; 5% + $0.50 after $20k/month; merchant of record since 2025-01-01 |
| Fiverr | https://help.fiverr.com/hc/en-us/articles/9234443621137-Your-earnings-page | Seller earns 80% of the purchase amount incl. extras and tips (Fiverr payment terms page returned 403) |
| Upwork | https://support.upwork.com/hc/en-us/articles/211062538-Freelancer-Service-Fees | Freelancer Service Fee 0% to 15% per contract |
| Uber | https://www.uber.com/us/en/newsroom/uber-comment-consumer-reports/ (dated 2026-06-16) | US take rate around 20% after adjusting for insurance; insurance 14% to 31% of an average fare by state. No driver-share figure published |
| Steam (tiers) | https://steamcommunity.com/groups/steamworks/announcements/detail/1697191267930157838 | From 2018-10-01: 75/25 on earnings beyond $10M, 80/20 beyond $50M |
| Steam (base) | https://www.quinnemanuel.com/the-firm/news-events/quinn-emanuel-secures-class-certification-seeking-billions-in-damages-for-wolfire-games-and-a-class-of-game-publishers-in-in-wolfire-games-llc-et-al-v-valve-corp-2-21-cv-00563/ | "Valve charges a typical commission of 30% per sale" (plaintiffs' counsel, secondary) |
| Steam (basis) | https://partner.steamgames.com/doc/finance/payments_salesreporting/faq | Share is applied to net revenue (gross less returns, chargebacks, taxes) |

## Calculations
- Patreon: 100 - 10 - 2.90 - 0.30 = 86.80
- Substack: 100 - 10 - 2.90 - 0.30 - 0.70 = 86.10
- Etsy: 100 - 0.20 - 6.50 - 3.00 - 0.25 = 90.05; with Offsite Ads 15%: 75.05
- Kickstarter: 100 - 5 - 3 - 0.30 = 91.70
- Gumroad: 100 - 10 - 0.50 - 2.90 - 0.30 = 86.30
- Google Play: 100 - 10 - 5 = 85.00
- Others: 100 x (1 - fee %)

## Not verified / left blank
- Uber driver share: not officially published, so left blank (see row note).
- Steam base 30%: no public Valve page states it; it comes from plaintiffs' counsel. The tier structure is official.
- Twitch: the official help page did not render; the rate comes from Twitch's own blog.
- Etsy one-time set-up fee: Etsy's policy confirms the fee exists but publishes no amount.
