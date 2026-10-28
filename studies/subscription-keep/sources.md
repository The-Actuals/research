# subscription-keep: sources, method, assumptions

Checked 2026-10-28. Fetched with User-Agent `the-actuals-research/0.1`, at least 3 s apart per host. Raw copies are in `_raw/`.

## Method and assumptions
- One $24.00 monthly subscription renewal charged to a **US domestic card**. Standard pay-as-you-go plans, no volume discounts, no promos.
- **No sales tax is added** (for example, a buyer in a state that does not tax SaaS). MoR fees apply to the tax-inclusive total (Lemon Squeezy: total order value; Stripe Managed Payments: full amount including indirect tax), so in taxing states the MoR fee is slightly larger.
- `kept_from_24` = 24 - 24 x pct_fee - fixed_fee, rounded to cents. Payout fees, dispute fees, 3DS/Radar per-transaction fees, international and PayPal surcharges are excluded and listed in `extra_fees_note`.
- `handles_sales_tax`: "yes" = provider is merchant of record and registers, collects, files and remits.

## Sources
| Provider | URL | Key text |
|---|---|---|
| Stripe cards | https://stripe.com/pricing | 2.9% + 30c domestic cards; +1.5% international; +1% currency conversion; Managed Payments 3.5% "in addition to Payments fees"; Tax Basic 0.5% per transaction where registered; Tax Complete from $90/mo |
| Stripe Billing | https://stripe.com/billing/pricing | Pay as you go: 0.7% of Billing volume |
| Stripe Managed Payments | https://support.stripe.com/questions/managed-payments-pricing | 3.5% per successful transaction, in addition to standard processing; Billing fees apply separately for subscriptions; calculated on full amount incl. indirect taxes |
| Stripe Managed Payments (scope) | https://docs.stripe.com/payments/managed-payments | Handles sales tax, VAT and GST in 80+ countries, plus fraud, disputes and support |
| Paddle | https://www.paddle.com/pricing | 5% + 50c per checkout transaction; tax compliance, fraud, chargebacks included |
| Lemon Squeezy | https://docs.lemonsqueezy.com/help/getting-started/fees | 5% + 50c; +1.5% international; +1.5% PayPal; +0.5% subscription payments; US Stripe payouts free |
| Polar | https://polar.sh/docs/merchant-of-record/fees (also https://polar.sh/resources/pricing) | Starter 5% + 50c (default for orgs created on/after 2026-05-27); Early Member 4% + 40c + 0.5% subscription; +1.5% international |
| FastSpring | https://fastspring.com/pricing/ | Custom quote only |
| Gumroad | https://gumroad.com/help/article/66-gumroads-fees | 10% + $0.50 per transaction, excluding card processing (2.9% + $0.30); merchant of record since 2025-01-01 (https://gumroad.com/pricing) |
| Whop | https://docs.whop.com/fees | 2.7% + $0.30 domestic card; Billing 0.5% when enabled; tax and remittance 2% when enabled and tax is collected |
| Whop tax | https://docs.whop.com/payments-and-billing/fees/taxes | Managed options cost 2%; "Whop collects and remits" covers US states, EU, UK; seller still responsible for nexus |

## Calculations ($24.00)
| Provider | Fee | Kept | Fee % of price |
|---|---|---|---|
| Stripe + Billing | 0.696 + 0.168 + 0.30 = 1.164 | 22.84 | 4.85% |
| Stripe + Tax Basic | 1.284 | 22.72 | 5.35% |
| Paddle | 1.20 + 0.50 = 1.70 | 22.30 | 7.08% |
| Lemon Squeezy | 1.32 + 0.50 = 1.82 | 22.18 | 7.58% |
| Polar Starter | 1.70 | 22.30 | 7.08% |
| Stripe Managed Payments | 0.84 + 0.696 + 0.168 + 0.30 = 2.004 | 22.00 | 8.35% |
| Gumroad | 2.40 + 0.50 + 0.696 + 0.30 = 3.896 | 20.10 | 16.23% |
| Whop card + Billing | 0.768 + 0.30 = 1.068 | 22.93 | 4.45% |
| Whop + tax remittance | 1.248 + 0.30 = 1.548 | 22.45 | 6.45% |

## Not verified / caveats
- FastSpring publishes no rate, so its row is blank.
- Whop's Billing (0.5%) is labelled "when enabled". Whether recurring memberships can run without it was not confirmed. Without it, Whop keeps $23.05.
- Stripe Managed Payments: we assume a subscription uses Stripe Billing, based on Stripe's note that Billing fees apply separately for subscriptions.
