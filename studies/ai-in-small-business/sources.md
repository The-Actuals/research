# Sources and method: ai-in-small-business

Checked on: 2026-10-28. Fetches used User-Agent `the-actuals-research/0.1`, with at least 3 s between requests to census.gov. Raw files are saved in `raw/census/`.

## Part A: US Census Bureau, Business Trends and Outlook Survey (BTOS)

All Part A numbers come from official BTOS download files. No unofficial numbers were used.

| File | URL | What it gave |
|---|---|---|
| National (current series) | https://www.census.gov/hfp/btos/downloads/National.xlsx | Q7 and Q24 national "Yes" shares, collections 202524 to 202621 |
| Employment size class (current) | https://www.census.gov/hfp/btos/downloads/Employment%20Size%20Class.xlsx | Q7 and Q24 for size classes A to G |
| Sector (current) | https://www.census.gov/hfp/btos/downloads/Sector.xlsx | Q7 and Q24 for the 2-digit NAICS sectors |
| Sector by employment size class (current) | https://www.census.gov/hfp/btos/downloads/Sector%20by%20Employment%20Size%20Class.xlsx | 1 to 4 employee firms by sector, latest period only |
| AI Core Questions (Original) | https://www.census.gov/hfp/btos/downloads/AI%20Core%20Questions.xlsx | Old-wording series, collections 202319 to 202520 (Sep 11, 2023 to Oct 5, 2025), national, size and sector |
| AI Supplement Table 2026 | https://www.census.gov/hfp/btos/downloads/AI_Supplement_Table_2026.xlsx | One-time pooled supplement, Nov 17, 2025 to Feb 8, 2026: business functions, generative-AI tasks, employment effects and reasons for not using AI (national and by size) |
| AI Question Wording Updates (PDF, Dec 3, 2025) | https://www.census.gov/hfp/btos/downloads/AI%20Question%20Wording%20Updates.pdf | Exact old and new wording, plus the decision to start a new time series |
| Core instrument, Round 3 and 4 (PDF) | https://www.census.gov/hfp/btos/downloads/BTOS%20Content%20V5%20Core%20Round%203,%204.pdf | "Super Intelligence or SI" wording, used from the Oct 19, 2026 collection |
| BTOS site text (About and Downloads pages, read from the site's app bundle) | https://www.census.gov/hfp/btos/data_downloads | Dates of the wording changes, the shutdown gap and the supplement windows |

The site says the latest release was posted on October 22, 2026. Its latest period is smpdt 202621: collection ran Oct 5 to 18, 2026, and the "last two weeks" reference period was Sep 21 to Oct 4, 2026.

### Exact question wording, and how it changed

1. **v1, Sep 11, 2023 to Oct 5, 2025 collections (old series).**
   - Current use (Q7): "In the last two weeks, did this business use Artificial Intelligence (AI) in producing goods or services? (Examples of AI: machine learning, natural language processing, virtual agents, voice recognition, etc.)"
   - Expected use (Q24): "During the next six months, do you think this business will be using Artificial Intelligence (AI) in producing goods or services? (Examples …same…)"
2. **Gap, Oct 6 to Nov 16, 2025.** The federal funding lapse stopped collection. Cycles 202521 to 202523 have no data.
3. **v2, from the Nov 17, 2025 collection (new series, first released Dec 4, 2025).**
   - "In the last two weeks, did this business use Artificial Intelligence (AI) in any of its business functions? (Examples of AI: machine learning, …)"
   - Q24 changed the same way.
   - Census says it saw a **level shift** with the new wording and started a **new time series**. The old series cannot be joined to the new one.
4. **v3 label, from the Oct 19, 2026 collection (smpdt 202622, not yet published).**
   - The instrument now says "Super Intelligence or SI (formerly referred to as Artificial Intelligence or AI) in any of its business functions", citing Executive Order 14434.
   - The current download files relabel Q7 and Q24 with this SI wording for every period. They also show a different examples list: "SI-powered data analysis; generative SI for marketing, product design, or coding; virtual SI agents for customer service; …".
   - The Data Dictionary says: "As of October 22, 2026, data is published in compliance with Executive Order 14434."
   - Based on the collection dates, every published new-series value (202524 to 202621) was collected **before** the SI wording took effect. Those respondents saw the "AI … any of its business functions" wording. I label these rows `v2` and treat the SI text as a relabel only.
5. **Instrument additions in Round 3 and 4.** The instrument adds new core questions: Q8 asks whether employees use generative SI, and Q9 and Q10 ask how SI affected headcount and hiring. None of these have been published in the download files yet.

### Method (Part A)
- `scripts/build_census.py` reads the xlsx files. For each period it keeps the "Yes" share of Q7 (`used_ai_last_2_weeks`) and Q24 (`expect_ai_next_6_months`), with its standard error (`se_pct`).
- `period_start` and `period_end` are the BTOS **reference period**, the "last two weeks" the question asks about. Collection dates are in separate columns. The supplement rows use the pooled collection window as their period.
- Census marks some cells "S" (they do not meet publication standards). Those rows keep a blank `pct` with a note.
- `question_version` separates v1 from v2. **Never draw v1 and v2 as one continuous line.**
- Sector codes are 2-digit NAICS. The names are the standard NAICS sector titles. The AI_sector.json chart feed on the BTOS site was used to cross-check six of the names.
- Size classes: A = 1–4, B = 5–9, C = 10–19, D = 20–49, E = 50–99, F = 100–249, G = 250+ employees. These come from the BTOS Data Dictionary.
- In the supplement, each block has its own base. Some are shares of all firms; others are shares of AI-using firms, of firms whose employees used generative AI, or of firms not planning to use AI. The base is written in `question_version`.

## Part B: Reddit top-of-year feeds

- Input: `scratchpad/topyear/raw/<sub>.rss`, a saved copy of `https://www.reddit.com/r/<sub>/top/.rss?t=year&limit=100`. These are Atom feeds with up to 100 posts each. The files were fetched on 2026-10-28 and the posts are dated Oct 2025 to Oct 2026.
- Subs used (12 feeds, 1,200 posts): Entrepreneur, EntrepreneurRideAlong, smallbusiness, solopreneur, SideHustleGold, youngentrepreneur, AI_Agents, indiehackers, microsaas, startups, Entrepreneurs, growmybusiness.
- **Missing:** sweatystartup. No feed file existed at analysis time.
- `rank` is the post's position in the feed (1 = first entry in the top-of-year feed). The feed does not include scores.
- Step 1, keyword screen (`scripts/extract_rss.py`): a post goes forward if its title or body mentions any of: AI, LLM, GPT, ChatGPT, Claude, Gemini, Copilot, OpenAI, agent(s), automation, n8n, Zapier, Make.com, chatbot or bot, Cursor, Lovable, Bolt, Replit, vibe coding, Midjourney, Perplexity, Grok, DeepSeek, machine learning, prompt, or artificial intelligence. 484 of the 1,200 posts matched.
- Step 2, manual coding: every candidate was read in full and coded against `work/CODEBOOK.md`.
  - Categories: own_ops, client_deploy, ai_product_only, skeptical_commentary, other_ai_discussion, not_relevant.
  - Fields: task (one primary task from 9 normalized tasks, plus all tasks mentioned), tools named, claimed result (metric, value, unit, period), sentiment (worked, mixed, failed, unclear), a skeptical flag and a promo-suspect flag.
  - The coding was split across five parallel coders who all used the same codebook. I spot-checked the results afterwards.
- "Uses AI in operations" means category own_ops or client_deploy.
- Adjudication: I resolved inconsistent codes in `work/overrides.csv` and applied them in `scripts/merge_reddit.py`. There was one case: a clinic-automation story cross-posted three times, which explicitly used no AI, was set to skeptical_commentary.
- Deduplication: posts with the same URL slug are marked in the `duplicate_of` column. Stats use unique stories.
- Denominators: `work/feed_index.csv` lists all 1,200 feed posts (sub, rank, url, keyword hit) without post bodies. The temporary body-text files were deleted after coding.
- Outputs:
  - `reddit_posts.csv` has 484 coded rows.
  - `reddit_task_summary.csv` is the chart table.
  - The coders' decision scripts are `work/code_g*.py` and their output is `work/coded_g*.csv`.
- Rebuild: create a venv with openpyxl and pypdf, then run `scripts/build_census.py` (writes data.csv) and `python3 -I scripts/merge_reddit.py <studydir>` (writes the Reddit files). The venv was deleted after the run.
- **All Reddit claims are self-reported** and were not verified. Many top posts are disguised promotion, which the `promo_suspect` flag marks.
- No post bodies are copied into the outputs. Only derived fields, URLs and short paraphrases are kept.
