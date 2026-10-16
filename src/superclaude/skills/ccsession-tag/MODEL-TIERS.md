# Model Tiers, Scores and Prices

One place to see which model sits in which tier, and the evals and prices that put it there.

- **Scores and prices checked:** 2026-09-30 (Muse Wonder rows: 2026-10-14).
- **Tiers last changed:** 2026-10-16 (Muse Wonder Full into Tier 1, Muse Wonder into Tier 2).
- **Where tiers actually take effect:** the Coder workspace env, `IronbellyOrg/Coder` file
  `templates/VSCode-AIDev02/aienv.d/defaults.sh` (`T<N>Model0<M>` slots). ccsession profiles live
  in `ccsession-models.json` next to this file. This page is the reasoning behind both; when a tier
  changes, update all three together.

## Contents

1. [Tiers at a glance](#1-tiers-at-a-glance)
2. [Full scoreboard](#2-full-scoreboard)
3. [By provider](#3-by-provider)
4. [Removed and excluded models](#4-removed-and-excluded-models)
5. [How models are placed](#5-how-models-are-placed)
6. [How to update this page](#6-how-to-update-this-page)
7. [Column meanings and footnotes](#7-column-meanings-and-footnotes)

## 1. Tiers at a glance

Tier numbers match the Coder env slots (`T0Model01` is Tier 0). Prices are USD per million tokens
(input / cached input / output). ccsession's default tier is Tier 2 (`CCSESSION_DEFAULT_TIER=tier2`).

| Tier | Role | Models (gateway id) | Intelligence | Price range | Context window | ccsession profile |
|---|---|---|---|---|---|---|
| **Tier 0** | Premium. Top-priced reasoning, used on purpose, never by default. | Claude Fable 5.1 (`claude-fable-5-1`), GPT-6 Astra (`gpt-6-astra`) | 52.7-53.4 | $10.00 / $0.25-1.00 / $50.00 | Tier 850K; Fable 1M, Astra 850K | none |
| **Tier 1** | Frontier. Best capability per dollar. | Claude Opus 5.5 (`claude-opus-5-5`), GPT-6.1 Sol (`gpt-6.1-sol`), Claude Sonnet 5.5 (`claude-sonnet-5-5`), Muse Wonder Full 1.0 (`muse-wonder-full-1.0`) | 51.8-57.6 | $2.00-4.00 / $0.10-0.20 / $10.00-20.00; Muse Wonder Full on subscription | Tier 850K; Opus 1M, Sol 850K, Sonnet 1M, Wonder Full 1M | `claude` (Opus), `gpt` (6.1 Sol), `wonderfull` |
| **Tier 2** | Strong and cheap. One capability band with different strengths. Default tier. | Grok 4.7 (`grok-4.7`), Qwen3.8 Max (`Qwen3.8-max`), GLM-5.3 (`glm-5.3`), Muse Spark 1.3 (`muse-spark-1.3`), Muse Wonder 1.0 (`muse-wonder-1.0`) | 44.8-52 | $1.25-2.00 / $0.15-0.50 / $4.25-6.00; Muse Wonder on subscription | Tier 500K; Grok 500K, Qwen 1M, GLM 1M, Muse Spark 950K, Muse Wonder 1M | `grok`, `qwen`, `glm`, `muse`, `wonder` |
| **Tier 3** | Budget. Bulk and low-stakes work. | GPT-6 Luna (`gpt-6-luna`) | 38.1 | $0.10 / $0.01 / $0.50 | 850K | none |

**Note on Tier 0 versus Tier 1.** Tier 0 is a price category, not a capability step: Opus 5.5 and
Sonnet 5.5 outscore both Tier 0 models on overall intelligence. Tier 0 is kept for the cases where
its specific strengths (Fable's HLE score, Astra's terminal score) are worth 2.5-5x the price.

**Candidates not yet placed** (scored, would fit, but not served by the company gateway on
2026-10-14): Xiaomi MiMo-V2.6-Pro (Tier 2 fit), Z AI GLM-5.3-Flash and DeepSeek V4.1 Flash (a
budget-strong band between Tier 2 and Tier 3), Xiaomi MiMo-V2.6-Flash (Tier 3 fit), Google Gemini 4
Argon (Tier 1 watchlist, limited access). See section 2.

**Subscription models.** Muse Wonder Full and Muse Wonder are covered by the Muse Code
subscription, so their per-token price does not count against them. Muse Wonder sits in Tier 2
rather than Tier 1 even though it scores 52: Tier 1 already has GPT-6.1 Sol at the same level.

**Label history.** The original research labelled these tiers X, 0, 1, 3 (premium, frontier,
strong, budget) plus an empty "2". The deployed numbering above is what the env and ccsession use.

## 2. Full scoreboard

Every model scored, highest intelligence first. Status: **Tier N** (in use), **Candidate** (fits a
tier, waiting on gateway access), **Removed** (superseded by a newer model from the same provider),
**Excluded** (beaten on both score and price). Gateway = served by the company gateway on 2026-10-14.

| Model | Provider | Status | Intelligence | HLE % | Terminal-Bench 4.0 % | Input | Cached input | Output | AA $/task | Gateway |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 [a] | Anthropic | **Tier 1** | 57.6 | 61.4 | 59.6 | $4.00 | $0.20 | $20.00 | $5.98 | yes |
| Claude Sonnet 5.5 [a] | Anthropic | **Tier 1** | 56.0 | 55.0 | 63.6 | $2.00 | $0.20 | $10.00 | $7.62 | yes |
| Muse Wonder Full (Max) [h] | Meta | **Tier 1** | 56 | 54 | 57.1 | subscription | subscription | subscription | n/a | yes |
| Claude Fable 5.1 [a] | Anthropic | **Tier 0** | 53.4 | 59.1 | 52.0 | $10.00 | $0.25 | $50.00 | $7.63 | yes |
| GPT-6 Astra | OpenAI | **Tier 0** | 52.7 | 54.7 | 59.1 | $10.00 | $1.00 | $50.00 | $3.26 | yes |
| Gemini 4 Argon (High) [b] | Google | Candidate (Tier 1 watchlist) | 52.6 | 57.1 | 57.1 | $2.00 | $0.10 | $10.00 | n/a | no |
| Muse Wonder (Max) [h] | Meta | **Tier 2** | 52 | 50 | 52.0 | $4.00 | $0.20 | $20.00 | $4.52 | yes |
| GPT-6.1 Sol | OpenAI | **Tier 1** | 51.8 | 52.9 | 56.1 | $2.00 | $0.10 | $10.00 | $0.72 | yes |
| Muse Spark 1.3 | Meta | **Tier 2** | 48.1 | 48.7 | 33.3 | $1.25 | $0.15 | $4.25 | $1.60 | yes |
| GPT-6 Sol | OpenAI | Removed | 47.5 | 47.9 | 43.9 | $2.00 | $0.20 | $10.00 | $1.05 | yes |
| GPT-5.6 Sol | OpenAI | Removed | 47.0 | 49.5 | 39.9 | $4.00 | $0.40 | $20.00 | $1.99 | yes |
| Grok 4.7 [c] | xAI | **Tier 2** | 46.4 | 43.1 | 25.8 | $2.00 | $0.50 | $6.00 | $3.74 | yes |
| MiMo-V2.6-Pro | Xiaomi | Candidate (Tier 2) | 46.3 | 49.4 | 34.8 | $0.435 | $0.0036 | $0.87 | n/a | no |
| Qwen3.8 Max (0902) [d] | Alibaba | **Tier 2** | 45.4 | 43.1 | 38.9 | $1.65 | $0.206 | $4.951 | $5.41 | yes |
| GLM-5.3 | Z AI | **Tier 2** | 44.8 | 42.3 | 41.9 | $1.40 | $0.26 | $4.40 | $2.01 | yes |
| Step 5 Preview | StepFun | Excluded | 43.7 | 46.5 | 33.3 | $1.00 | $0.05 | $2.70 | n/a | no |
| Kimi K3 (Max) | Moonshot | Excluded | 43.6 | 46.9 | 12.6 | $3.00 | $0.30 | $15.00 | n/a | no |
| GPT-5.6 Terra | OpenAI | Removed | 42.1 | 42.9 | 35.4 | $2.00 | $0.20 | $12.00 | $1.40 | yes |
| Claude Opus 4.8 | Anthropic | Removed | 41.8 | 48.7 | 21.7 | $5.00 | $0.50 | $25.00 | $4.08 | yes |
| GLM-5.3-Flash | Z AI | Candidate (between Tier 2 and 3) | 41.8 | 39.9 | 32.8 | $0.15 | $0.03 | $0.50 | n/a | no |
| Claude Opus 4.7 | Anthropic | Removed | 40.7 | 42.3 | n/a | $5.00 | $0.50 | $25.00 | n/a | yes |
| DeepSeek V4.1 Flash (Max) [e] | DeepSeek | Candidate (between Tier 2 and 3) | 39.5 | 39.2 | 26.8 | $0.15 | $0.003 | $0.60 | n/a | no |
| GPT-6 Luna [f] | OpenAI | **Tier 3** | 38.1 | 38.5 | 12.6 | $0.10 | $0.01 | $0.50 | $0.07 | yes |
| MiMo-V2.6-Flash | Xiaomi | Candidate (Tier 3) | 37.9 | 35.1 | 22.7 | $0.14 | $0.0028 | $0.28 | n/a | no |
| GPT-5.6 Luna | OpenAI | Removed | 37.3 | 39.5 | 11.6 | $0.20 | $0.02 | $1.20 | $0.18 | yes |
| MiniMax M3 [g] | MiniMax | Excluded | 29.2 | 39.0 | 2.0 | $0.30 | $0.06 | $1.20 | n/a | no |
| Claude Haiku 4.5 (reasoning) | Anthropic | Excluded | 16.9 | 10.4 | 0.0 | $1.00 | $0.10 | $5.00 | n/a | yes |

## 3. By provider

Same numbers as section 2, grouped so newer and older models from one provider sit side by side.
Only providers with a model in a tier are shown; candidates and excluded providers are in section 2.

**OpenAI**

| Model | Status | Intelligence | HLE % | Terminal 4.0 % | Input | Cached | Output | AA $/task |
|---|---|---|---|---|---|---|---|---|
| GPT-6 Astra | **Tier 0** | 52.7 | 54.7 | 59.1 | $10.00 | $1.00 | $50.00 | $3.26 |
| GPT-6.1 Sol | **Tier 1** | 51.8 | 52.9 | 56.1 | $2.00 | $0.10 | $10.00 | $0.72 |
| GPT-6 Sol | Removed | 47.5 | 47.9 | 43.9 | $2.00 | $0.20 | $10.00 | $1.05 |
| GPT-5.6 Sol | Removed | 47.0 | 49.5 | 39.9 | $4.00 | $0.40 | $20.00 | $1.99 |
| GPT-5.6 Terra | Removed | 42.1 | 42.9 | 35.4 | $2.00 | $0.20 | $12.00 | $1.40 |
| GPT-6 Luna | **Tier 3** | 38.1 | 38.5 | 12.6 | $0.10 | $0.01 | $0.50 | $0.07 |
| GPT-5.6 Luna | Removed | 37.3 | 39.5 | 11.6 | $0.20 | $0.02 | $1.20 | $0.18 |

**Anthropic**

| Model | Status | Intelligence | HLE % | Terminal 4.0 % | Input | Cached | Output | AA $/task |
|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 [a] | **Tier 1** | 57.6 | 61.4 | 59.6 | $4.00 | $0.20 | $20.00 | $5.98 |
| Claude Sonnet 5.5 [a] | **Tier 1** | 56.0 | 55.0 | 63.6 | $2.00 | $0.20 | $10.00 | $7.62 |
| Claude Fable 5.1 [a] | **Tier 0** | 53.4 | 59.1 | 52.0 | $10.00 | $0.25 | $50.00 | $7.63 |
| Claude Opus 4.8 | Removed | 41.8 | 48.7 | 21.7 | $5.00 | $0.50 | $25.00 | $4.08 |
| Claude Opus 4.7 | Removed | 40.7 | 42.3 | n/a | $5.00 | $0.50 | $25.00 | n/a |
| Claude Haiku 4.5 (reasoning) | Excluded | 16.9 | 10.4 | 0.0 | $1.00 | $0.10 | $5.00 | n/a |

**Meta**

| Model | Status | Intelligence | HLE % | Terminal 4.0 % | Input | Cached | Output | AA $/task |
|---|---|---|---|---|---|---|---|---|
| Muse Wonder Full (Max) [h] | **Tier 1** | 56 | 54 | 57.1 | subscription | subscription | subscription | n/a |
| Muse Wonder (Max) [h] | **Tier 2** | 52 | 50 | 52.0 | $4.00 | $0.20 | $20.00 | $4.52 |
| Muse Spark 1.3 | **Tier 2** | 48.1 | 48.7 | 33.3 | $1.25 | $0.15 | $4.25 | $1.60 |

**xAI, Alibaba, Z AI**

| Model | Status | Intelligence | HLE % | Terminal 4.0 % | Input | Cached | Output | AA $/task |
|---|---|---|---|---|---|---|---|---|
| Grok 4.7 [c] | **Tier 2** | 46.4 | 43.1 | 25.8 | $2.00 | $0.50 | $6.00 | $3.74 |
| Qwen3.8 Max (0902) [d] | **Tier 2** | 45.4 | 43.1 | 38.9 | $1.65 | $0.206 | $4.951 | $5.41 |
| GLM-5.3 | **Tier 2** | 44.8 | 42.3 | 41.9 | $1.40 | $0.26 | $4.40 | $2.01 |
| GLM-5.3-Flash | Candidate | 41.8 | 39.9 | 32.8 | $0.15 | $0.03 | $0.50 | n/a |

## 4. Removed and excluded models

| Model | Decision | Why |
|---|---|---|
| GPT-6 Sol | Removed | GPT-6.1 Sol scores higher on every eval at the same input and output price and half the cached-input price ($0.72 vs $1.05 per AA task). |
| GPT-5.6 Sol | Removed | Beaten by GPT-6.1 Sol on intelligence and terminal score at half the price or less on every token type. |
| GPT-5.6 Terra | Removed | Lower scores than GPT-6.1 Sol and a higher output price. |
| GPT-5.6 Luna | Removed | Same model line as GPT-6 Luna, which matches its intelligence at half the input and under half the output price. |
| Claude Opus 4.8, 4.7 | Removed | Opus 5.5 scores far higher and is cheaper on every token type. |
| Claude Haiku 4.5 | Excluded | Against GPT-6 Luna it costs 10x more on every token type and loses all three evals; GLM-5.3-Flash also beats it on all three and is cheaper. |
| MiniMax M3 | Excluded | GPT-6 Luna scores 38.1 vs 29.2 and is cheaper on every token type. |
| Step 5 Preview, Kimi K3 | Excluded | MiMo-V2.6-Pro beats both on all three evals and is cheaper on every token type. |

A removed model can still be reachable on the gateway; it just never gets a tier slot or a fallback
position, because the newer model wins on both score and price.

## 5. How models are placed

1. **Prune first.** Drop any model that a newer model from the same provider ties or beats on
   score while costing the same or less on input, cached input and output. Never tier a superseded
   model, not even as a fallback.
2. **Drop dominated models.** Exclude a model when another model beats it on all three evals and
   costs less on all three token prices.
3. **Group by intelligence.** Models within a few points of each other share a tier; a cheaper
   model joins a tier when its score is close enough.
4. **Check real spend, not only rates.** AA $/task includes reasoning tokens, so a model with lower
   rates can cost more per task (Sonnet 5.5 at $7.62 vs Opus 5.5 at $5.98).
5. **Tier 0 is a price category.** It holds the $10 / $50 premium models, even where a Tier 1 model
   scores higher overall.
6. **Subscription models.** A model already paid for by a subscription is placed by score alone;
   its token price is ignored.
7. **Gateway first.** A model goes into a tier only when the company gateway serves it; until then
   it stays a Candidate.

## 6. How to update this page

1. Re-check the numbers on Artificial Analysis (intelligence, HLE, Terminal-Bench, $/task) and the
   provider's pricing page; update section 2, then the matching rows in section 3.
2. Change the "checked" date at the top, or note a per-row date when only a few rows change.
3. If a tier changes, update section 1 and also:
   - the `T<N>Model0<M>` and `_WINDOW` lines in the Coder repo's `aienv.d/defaults.sh`;
   - `ccsession-models.json` here (profiles, `pinned`, `one_million_context`, `display_overrides`).
4. Record every removal or exclusion in section 4 with its reason.

## 7. Column meanings and footnotes

- **Intelligence:** Artificial Analysis Intelligence Index v4.3.2, out of 100, at maximum
  reasoning effort where available.
- **HLE %:** Humanity's Last Exam, text only, no tools.
- **Terminal-Bench 4.0 %:** agentic terminal and coding tasks.
- **Input / Cached input / Output:** standard short-context USD per million tokens. Cached input
  means cache reads; cache writes, fast mode and long-context premiums are extra.
- **AA $/task:** what Artificial Analysis spent per attempted benchmark task at the listed
  settings, including cache writes and reasoning tokens. Best single measure of real cost.
- **n/a:** no published result.

Footnotes:

- **[a]** Starred Claude results include Anthropic's default fallback behaviour.
- **[b]** Gemini 4 Argon access is limited; prices are announced introductory rates that Google
  says will rise to $4 input / $20 output.
- **[c]** Grok 4.7 scored at xhigh effort.
- **[d]** Qwen prices are US (Virginia) rates with implicit caching. International (Singapore)
  rates are $2.00 / $0.25 / $6.00.
- **[e]** DeepSeek prices are off-peak; peak rates are double.
- **[f]** GPT-6 Luna's index was updated to 38.1 from an earlier 37.3.
- **[g]** MiniMax prices cover standard requests up to 512K input tokens.
- **[h]** Muse Wonder rows checked 2026-10-14. Intelligence, HLE and Terminal-Bench from
  Artificial Analysis (HLE published as whole numbers; Terminal-Bench decimals from Meta's launch
  table, labelled as AA-run). Muse Wonder Full has no public API or per-token price; both Muse Wonder
  models are covered by the Muse Code subscription. Muse Wonder's listed prices are Meta's public
  API rates, shown for comparison only. Gateway ids: `muse-wonder-full-1.0`, `muse-wonder-1.0` (each also
  has a `-contributor` copy). Both have 1M context.
- **Unscored:** the gateway also serves `claude-haiku-5-5`, which this page has no scores for yet.
