# Sources and method: indie-saas-pricing

Checked on 2026-10-28. Each product's own public pricing page (or the pricing section of its homepage) is its source. The exact URL is in `data.csv` → `source_url`.

## How the product list was built
1. **Reddit feeds.** I parsed the top-of-year Atom feeds in `topyear/raw/` for r/indiehackers, r/microsaas, r/SaaS, r/SideProject and r/buildinpublic.
   - Every external link in a post body was extracted, giving 155 domains.
   - Post text was used only to find links. No post text is copied into outputs; `reddit_post_url` points to the post where the link appeared.
2. **Removed non-products before crawling:**
   - news sites, Kickstarter, Steam, itch.io and image hosts;
   - big or VC-funded platforms (Lovable, Hootsuite, Cloudflare);
   - NSFW sites, personal pages and games.
   - That left 118 domains.
3. **TrustMRR startup pages linked in the feeds.** These resolved to 5 more products: postpeer.dev, launchpanda.dev, socialkit.dev, screencharm.com and opentweet.io.
4. **Crawl.** Each site was crawled with headless Chromium:
   - homepage, then the page its "Pricing / Plans" link points to (or `/pricing`);
   - polite pacing of ≥3.2 s per site and UA "the-actuals-research/0.1".
   - Products whose pages showed any price moved on to extraction. 62 of the 118 feed domains showed no price (dead, 404, free tools, games, apps without a public price page).
5. **Topping up toward ~100.** I added 78 well-known indie / bootstrapped SaaS with public pricing pages, chosen before seeing their prices, across analytics, forms, scheduling, feedback, monitoring, email, affiliate, screenshot/PDF APIs and site builders. `found_via` = "well-known indie (added)".
   - 71 are included.
   - 2 were dropped before extraction as not SaaS: codefa.st (a course) and gamifylist.com (a directory).
   - For 5 the crawler captured no price: typefully.com, potion.so, blackmagic.so, updown.io and lowfruits.io. These were not checked by hand, so they are omissions, not findings.
6. **Extraction.** Pricing pages were re-rendered with the billing toggles clicked, so both the monthly and the yearly price were seen.
   - Where a toggle did not respond, the price was read from the page's HTML data attributes, structured data or pricing JSON on the same site, and the row's `notes` say so.
7. **Inclusion rule:** a software product (SaaS, API, or app) with a public price for at least one paid plan.
   - 132 products were reviewed, 123 are included, and 9 are excluded (list below).

## Field definitions
- `cheapest_paid_monthly_usd`: the lowest recurring paid plan, **paid month to month**, for 1 seat, at the lowest usage tier.
  - Enterprise "contact us" plans, add-ons and one-time credit top-ups are ignored.
  - It is filled only when the page prices in USD. 6 products price in EUR or GBP; their native price is in `cheapest_paid_monthly_native`, with no currency conversion.
  - When a product is sold yearly only, the column is the yearly price ÷ 12, and `cheapest_basis` = `annual-only` (2 products).
- `trial`:
  - `none`: no trial is offered. A free plan is not a trial.
  - `no-card`: the page says no card is needed.
  - `card-required`: the page says a card is needed or captured.
  - `unknown`: a trial exists but the page does not say whether a card is needed.
- `most_popular_tier_usd`: the month-to-month price of the tier the page badges "Most popular", "Popular", "Recommended" or "Best value". Equivalent badges are quoted in `notes`.
- `annual_discount_pct` = 1 − (yearly-billed per-month price ÷ month-to-month price), for the cheapest plan, computed from the two prices that were seen. Where only a stated figure was available, the note says `stated`.
- `lifetime_deal` = y if the product sells a lifetime or one-time licence for the software (including via AppSumo, as stated on the page).

## Headline subset used for statistics
The headline subset is the 104 products with `pricing_model` of `subscription` or `mixed` and a USD `cheapest_paid_monthly_usd`. It leaves out:
- 11 one-time-only apps;
- 3 usage / credit-only products;
- 5 non-USD subscriptions.

## Assumptions
- Prices are list prices shown to a US visitor (en-US locale, US timezone). Tax is excluded and launch promos are ignored. Where a promo was shown, the standard price was used and the promo is noted.
- Per-seat and per-unit pricing is taken at 1 seat or 1 unit.
  - Cronitor is $2 per monitor plus $5 per user, entered as $7 (computed).
- A product's sub-tier at the lowest usage level (e.g. 10k pageviews) counts as its cheapest plan.
- "Indie" is not verified company by company. Feed products are self-described solo or small-team launches. The added list is products widely known as bootstrapped or indie; a few are larger bootstrapped companies (e.g. Publer, YouCanBook.me, Sunsama, ScrapingBee).

## Excluded (reviewed, not in data.csv)
- trusttraffic.co (r/indiehackers): its pricing link is a traffic leaderboard that sells ad slots only.
- trylaunch.ai (r/indiehackers): a launch directory selling listings.
- startupsubmit.app (r/indiehackers): a manual directory-submission service.
- launchpact.io (r/indiehackers): a Product Hunt launch network with a one-time listing fee.
- launchpanda.dev (r/indiehackers, via TrustMRR): a done-for-you launch service.
- envelope.so (r/microsaas): all paid tiers are "Custom / Contact us".
- rankinpublic.xyz (r/microsaas): no prices shown, and /pricing is a 404.
- telic.dev (r/buildinpublic): free app with no paid plan.
- fleetgen.ai (r/buildinpublic): the paid tier is "Book a demo for your price".

## Fetching notes
- Working files are in `work/`:
  - rendered page text: `pages*/`, `tog/`, and the per-batch folders;
  - extraction rows: `rows_batch*.jsonl`;
  - the build script: `build.py`.
- Polite pacing was kept, with one exception: while recovering datafa.st's price from its own JavaScript plan config, about 37 small static JS files were fetched about 0.4 s apart. That is faster than the 3 s rule, and it is disclosed here.
- No logins, no checkout flows, no paywalled pages.
