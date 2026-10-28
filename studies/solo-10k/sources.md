# Sources: solo-10k

Checked on: 2026-10-28. User-Agent on every request: `the-actuals-research/0.1`. At least 3 s between requests to the same host.

## Step 1: feasibility check (robots.txt + terms) for every candidate source

| Source | robots.txt | Terms of use | Decision |
|---|---|---|---|
| TrustMRR (Stripe/LemonSqueezy/Polar/Dodo-verified revenue directory), https://trustmrr.com | `Allow: /` for all agents | https://trustmrr.com/terms (last updated 2026-10-09). §9.2: public display, bulk export or republication needs "TrustMRR's prior written permission". §9.3 forbids anyone to "Scrape, harvest, archive, or systematically reconstruct TrustMRR's database". §12.4 also forbids "Scraping TrustMRR, copying startup listings at scale". | **Not collected.** Its terms forbid scraping and reuse. I did not fetch any startup page. I made only 3 requests: robots.txt, the sitemaps (to size it at about 12,093 startup URLs) and /terms. |
| Indie Hackers product directory and interviews, https://www.indiehackers.com | `User-agent: *` allows most paths, but a named block disallows `/` for AI agents (`anthropic-ai`, `ClaudeBot`, `Claude-SearchBot`, `GPTBot`, …). | /terms returned HTTP 403 to our User-Agent, so I could not read it. | **Not collected.** This collector is an AI agent, and the site has explicitly opted out of AI crawlers. |
| Starter Story, https://www.starterstory.com | `Allow: /` | https://www.starterstory.com/terms says "You can only re-publish our data if it's for non-commercial objectives (e.g. not a company/startup)". Most data is also gated behind an email signup. | **Not collected.** The Actuals is a commercial newsletter. |
| Acquire.com public listings, https://acquire.com | `Allow: /` (except buyer pricing) | https://acquire.com/terms/ forbids "Use any robot, spider or other automatic device … including monitoring or copying any of the material", and also any "manual process to monitor or copy". | **Not collected.** |
| Flippa listings, https://flippa.com | Partial disallows | https://flippa.com/terms forbids using "data mining, robots, or similar data gathering and extraction tools", and also forbids creating or publishing a database of its listings. | **Not collected.** |
| StartuPage (Stripe-verified MRR leaderboard), https://startupa.ge | Allows | https://startupa.ge/terms forbids "Scrape, crawl, or data-mine the platform without permission". | **Not collected.** |
| Arrfounder (founder revenue leaderboard), https://arrfounder.com | Allows | https://arrfounder.com/terms forbids "Scrape or harvest data from the Service using automated means without permission". | **Not collected.** |
| VerifyMRR, https://verifymrr.com | Allows | No public directory (sitemap lists the website only), and /terms returned 404. | Nothing to collect. |
| Baremetrics Open Startups, https://baremetrics.com/open-startups | Allows | Allows | Checked. The page lists only about 5 companies, no team sizes, and the revenue is rendered client-side. **Not usable:** no solo businesses could be identified. |
| ProfitWell public pages | n/a | n/a | The product was absorbed into Paddle and its public pages no longer exist. Not used. |
| Product Hunt | n/a | The API needs a token and its terms restrict reuse. | Not used. Launch dates were not needed for the main findings. |
| **Hacker News, via the HN Search API by Algolia**: https://hn.algolia.com/api/v1/search and /items/{id} | news.ycombinator.com/robots.txt asks for `Crawl-delay: 30` and disallows only action URLs. I did not crawl HN pages at all. | YC terms (https://www.ycombinator.com/legal) forbid scraping "except as expressly authorized". YC publishes HN data through an official public API ("we're making the public Hacker News data available", https://github.com/HackerNews/API). The Algolia HN Search API is the public search index linked from HN's own footer. | **Collected.** I made 84 search calls (24 story searches, plus 60 comment searches: 20 queries × 3 pages of 200 hits) and 42 thread-tree calls (one call per thread). Every call was 3 s apart. Comment text is used only as analysis input. Outputs hold derived fields plus the comment URL. |
| **Reddit top-of-year feeds** (73 subreddits × top 100 posts, past year): local copies at `scratchpad/topyear/raw/*.rss` | n/a: I made no new Reddit requests. The orchestrator downloaded these public Atom feeds earlier. | The brief allows public RSS. | **Collected.** Outputs hold derived fields plus the post URL. |
| ECB FX rates via the Frankfurter public API: https://api.frankfurter.dev/v1/latest?from=USD&to=EUR,GBP,CAD,AUD,INR | n/a | Public API | Used to convert non-USD revenue. Rates for 2026-10-28: 1 USD = 0.89823 EUR, 0.75258 GBP, 1.4047 CAD, 1.4219 AUD, 95.22 INR. I used today's rate, not the rate on the post date. |

**Consequence:** none of the sources that carry payment-provider-verified revenue (TrustMRR, StartuPage, Indie Hackers' Stripe badge) permit collection. Every row in `data.csv` is therefore `revenue_verification = self_reported`, and **zero rows are `verified`**. This is the main limit of the study, and it is stated in findings.md.

## Hacker News threads used (42; thread URL = https://news.ycombinator.com/item?id=<id>)
- One-person businesses: 7367243 (2014), 13326535 (2017), 16482392 (2018), 21332072 (2019), 25614966 (2021), 35333088 (2023), 19701783 ("One-person SaaS apps that are profitable?", 2019)
- Passive or side income: 2358111 (2011), 2795760 (2011), 4639271 (2012), 7094402 (2014), 8107588 (2014), 10258225 (2015), 11898992 (2016), 12274094 (2016), 12798447 (2016), 12997338 (2016), 13150144 (2016), 13514093 (2017), 13669723 (2017), 16815842 (2018), 18479588 (2018), 18906094 (2019), 21389776 (2019), 24859111 (2020), 25316912 (2020), 27747934 (2021), 33923137 (2022)
- "Those making $500/month on side projects" show-and-tell: 38467691 (2023), 38935714 (2024), 39110194 (2024), 42373343 (2024), 46307973 (2025), 49417766 (2026)
- Recent: 39259602 (2024), 40640888 (2024), 44144473 (2025), 45769481 (2025), 46414570 (2025), 48315206 (2026), 48625774 (2026), 49590656 (2026)

The threads were found with Algolia `tags=ask_hn` searches for: solo founder, one-person business, passive income, profitable side project, MRR, bootstrapped, indie, lifestyle business, making money online, and similar terms. The raw JSON is in `raw/hn/`.

## HN comment-search queries (Algolia `tags=comment`, 3 pages × 200 hits each)
These queries were run because the thread-based pass alone yielded few solo businesses at $10K+/month:
"solo founder MRR", "one-person business revenue", "one-man business month", "by myself MRR", "no employees revenue month", "just me MRR", "solo SaaS revenue", "single founder MRR", "I run it alone revenue", "solopreneur revenue", "solo developer revenue month", "one person company revenue", "solo profitable SaaS", "bootstrapped solo MRR", "my side project makes month", "indie hacker MRR", "lifestyle business revenue solo", "I work alone revenue", "one-person SaaS", "solo app revenue month". The raw JSON is in `raw/hn_search/`.

## Method
1. **Scan.**
   - 9,567 comments from the 42 HN threads.
   - 6,301 further HN comments from the comment searches. That makes 15,829 unique HN comments in total.
   - All 7,300 Reddit top-of-year posts (73 subs × 100).
2. **Pre-filter** (`scripts/hn_extract.py`, `scripts/rd_extract.py`, `scripts/moneyre.py`).
   - Keep any item with a money figure of $8K or more (any currency or period), or with "six/seven figures".
   - For the HN comment-search pass, also require a solo keyword: solo, alone, by myself, one-person or one-man, no employees, just me, single founder, solopreneur, myself.
   - Result: **1,616 candidates**: 404 from the HN threads, 796 Reddit posts, and 416 from the HN search.
3. **Read and code.** Every candidate was read in full and coded against the written codebook in `work/CODEBOOK.md`. The coding was split into 27 batches, each done by a separate reader agent working to that codebook. Each reader confirmed that its output line count matched its input and that every quote it used was verbatim.
   **Inclusion** needs all four of these:
   - (a) the author's **own** business;
   - (b) an **internet** business. Excluded: rentals, investing, salaried jobs, hourly freelancing or consulting, and offline local services;
   - (c) a stated revenue or profit figure **≥ $10,000/month**, or ≥ $120,000/year;
   - (d) **one person**. A co-founder, partner or employees means exclusion.
4. **Normalization** (`scripts/merge.py`).
   - Annual figures are divided by 12, weekly × 52/12, and quarterly ÷ 3. A range uses its midpoint.
   - "Six figures/yr" is floored at $100K/yr, which fails the threshold. "X+" uses X and is flagged `revenue_lower_bound=1`.
   - Non-USD amounts use the ECB rate above.
   - MRR, ARR/12, revenue and profit are kept apart in `revenue_metric`.
   - Lifetime totals with no stated period were **excluded**, not averaged.
5. **Manual exclusions** (6 rows):
   - Four Reddit accounts with the same surname post the same app stories.
   - In other posts, one of them names his brother as co-founder, and the others list "having a co-founder" as a lesson.
   - Solo-ness is therefore not established. All six rows were dropped as `team_not_solo`.
6. **De-duplication.**
   - Several rows by the same HN or Reddit author about the same business (e.g. one analytics SaaS reported in 2013, 2015 and 2017) share a `dup_group`.
   - Only the **latest** claim counts (`included_in_stats=1`).
   - Two older rows by the same HN author are about *different* businesses and are kept as separate businesses.
   - Author handles were used only for matching, and are not in any output.
7. **Results.**
   - 101 qualifying claims (`data.csv`), covering **89 unique businesses** (`included_in_stats=1`).
   - The other 1,515 candidates and their reasons are listed in `excluded.csv`. The main reasons:

     | Reason | Candidates |
     |---|---|
     | not own business | 416 |
     | below $10K/mo | 288 |
     | no specific figure | 255 |
     | team, not solo | 170 (incl. the 6 manual) |
     | hypothetical or a question | 124 |
     | freelance or job | 85 |
     | not an internet business | 83 |

## Field definitions and assumptions
- `revenue_verification` is `self_reported` for **every** row (see Step 1). Nothing was verified with a payment provider.
- `team_size` = 1 by construction. `solo_basis` records how it was established:
  - `explicit`: the author says solo, one-person, no employees, just me, etc.;
  - `explicit_with_contractors`: a solo owner who says they use freelancers, VAs or paid writers;
  - `implicit`: first person only, with no team, partner or employee mentioned.
  Only 30 of the 89 are explicit.
- `founded_year` is filled only when stated, or derived from a stated duration plus the post date (`founded_basis`).
- `months_to_10k` is filled only when the founder states it or gives both dates. Only 1 business does, so time-to-$10K **could not be measured**. Instead, findings use business age at the time of the claim (claim year − founded year, n=25), which is an *upper bound* on time-to-$10K.
- `growth_channels` uses a fixed vocabulary, and is filled only where the author says the channel brought customers. 22 of the 89 name one.
- Entry price was stated by only 1 business, so **price points could not be analysed**.
- `detail_level`: `thin` means the category is unclear or the text is under 300 characters (e.g. one-line claims).
- `claim_year` is the post year. The claims cover 2010–2026: 7 from 2016 or earlier, 27 from 2017–2021 and 55 from 2022–2026. A `revenue_timing=current` claim is current **as of the post date**, not as of 2026-10-28.
- `notes` holds verbatim quotes of 15 words or fewer only. No post bodies are copied. Founder names are omitted, and business names and URLs appear only when the author named them in the post.
- `summary.csv` holds the chart-ready aggregates.
