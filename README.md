# x402 market gaps: what sells elsewhere, what we list, and what nobody lists

Data pulled 2026-10-23 from four independent sources. Every number below is reproducible with the URLs given.

## 1. What actually earns (agent402 leaderboard, 7-day window, read from Base event logs)

`GET https://agent402.tools/api/leaderboard`

- 3.222 sellers scanned, **2.769 with any payment** in 7 days.
- Top 50 = **$10.941**, median of those 50 = **$39,44/week**, rank 50 = **$16,75/week**.
- Top 12 by money, with buyer counts:

| Seller | USD/week | unique buyers | What it sells |
|---|---|---|---|
| X Pay | 2.850,87 | 176 | payments |
| AX1 Console | 2.393,08 | **795** | console / keys |
| x402.dtelecom.org | 1.282,50 | 7 | telecom data |
| api.surplusintelligence.ai | 835,25 | 9 | market intelligence |
| claw402.ai | 354,04 | 80 | agent infra |
| keyring-agent | 353,10 | 53 | wallet / keys |
| StableEnrich | 320,68 | 117 | data enrichment |
| BlockRun.AI | 288,76 | 225 | compute / inference |
| BotPay NFT Mint | 256,13 | 325 | NFT minting |
| OnchainPulse | 211,60 | 27 | on-chain data |
| Pocket Network | 152,92 | 64 | RPC |
| Exa | 110,05 | 64 | web search |

**Pattern:** the money is in *inputs an agent consumes repeatedly* — payments, keys, compute, search, data feeds, on-chain intelligence. Every top seller is called by another machine, many times, with a small price.

## 2. What the directories are stuffed with (supply, 402index health)

`GET https://402index.io/api/v1/health` → 164.032 x402 endpoints, 6.861 services, 4.836 providers; **63.292 down**, 16.800 degraded, 84.058 healthy.

Keyword supply (`GET /api/v1/services?q=<kw>&limit=1` → `total`):

| keyword | services | keyword | services |
|---|---|---|---|
| search | 7.687 | verify | 1.389 |
| price | 5.959 | gas | 1.060 |
| wallet | 3.286 | monitor | 917 |
| llm | 3.055 | rpc | 731 |
| image | 2.401 | enrich | 664 |
| health | 1.442 | **uptime** | **141** |
| scrape | 1.400 | | |

## 3. The asymmetry that matters

- **Over-supplied, low-yield:** "search" (7.687 services) and "price" (5.959) are the two most crowded words in the index, yet the sellers that earn from them are the ones with a *dataset* behind them (Exa, surplusintelligence), not a wrapper.
- **Verification is a rounding error:** of the top 50 earners, exactly one is a checker (ClearCheck, $21,79/week, 1.019 calls, 3 buyers). Ours is in the most crowded niche with the lowest ticket.
- **Under-supplied, provably needed:** `uptime` has **141 services** while **63.292 endpoints are down and 16.800 degraded** — a 448:1 ratio of broken endpoints to vendors selling uptime checks. `monitor` has 917.
- **Nobody sells the truth about listings.** No service in the top 50 sells "does the 402 charge what the catalog advertises, is the endpoint alive, is the seller real". That is the content gap, and we already compute it.

## 4. Our own sample: 25 services checked against their advertised price

`check.py` in this repo fetches each listing's live 402 and compares it to what 402index advertises for the same URL.

| verdict | count |
|---|---|
| MATCH | 18 |
| 402 without an amount field | 4 |
| no paywall at all (free, but listed as paid) | 1 |
| 404 | 1 |
| live price 2x the advertised price | 1 |

So ~28% of a random slice of listings is wrong in a way that costs a buyer money or a seller credibility. That is a product, and it is not in any listing we have.

## 5. Gap list: content present elsewhere but missing from our listings

1. **Recurring data feed** (the top earners' shape). We have Bright Data Web Unlocker and a scraper that already works; we list none of it.
2. **Uptime / health monitoring for x402 sellers** — 141 vendors for 63k dead endpoints. Price per check is tiny, volume is huge, and it is called by machines.
3. **Listing truth / price-mismatch audit** — no competitor in the top 50; 28% error rate in our sample.
4. **Wallet/key or compute** — biggest earners, but we cannot ship them credibly today; skip.

## 6. What we list that is missing elsewhere (our actual edge)

- A **`convention: verification` file** with recomputed bytes and a chain-read receipt — a *record* other agents can cite in a claim. The directories sell "a check"; almost nobody sells "a citable verdict file" plus a free trial.
- Our verification is the only one in the hashn store that comes with a public reconciler (`github.com/ciperx`) a stranger can re-run.

## 7. Decision

Keep the verification file as the *fulfilment*, but stop selling it as the headline. Sell the two things the market is missing and we can produce today:

1. **x402 listing truth check** — "is this endpoint alive, does its 402 match its advertised price, is the payTo the seller's own address" — priced per call, with a free daily public report.
2. **Daily x402 market gap report** — the table in §1–§3 refreshed from the APIs, published free, with the paid API as the upsell. The report itself is the marketing, and nobody else publishes it from chain data with reproducible queries.
