# Assessment of the typesafe-ai skill for the p15 Jev experiments

Source: `/root/.claude/plugins/marketplaces/typesafe-ai/skills/typesafe-ai/SKILL.md` (MIT, third-party guidance data; the only skill in plugin `typesafe@typesafe-ai`), checked against the live docs on 2026-11-10 (snapshot `$SP/p15/_docs/`: models, OpenAPI, jaggedness, errors, primitives, companion-noul and noul-screen patterns). The skill is good integration craft and consistent with the live docs. It is followed where it fits; two of its instructions are overridden by owner rules (below).

## Overrides (owner rules win)

| Skill says | p15 does instead | Why |
|---|---|---|
| use `TYPESAFE_API_KEY`; keep keys on the server | key only in `JEV_API_KEY`, sourced by the coordinator inside the single command that runs a Jev script; never in any worker's environment, file or log (contract J2) | owner rule; workers share the machine |
| "ask the user for permission, get a budget, disclose data" before live tests | permission and the throwaway key are already given by the owner; budget = $5 offline + $1 live per experiment as pre-flight reservations; data classes recorded in a manifest per call (contract J3, J4) | owner authorization; D6 |
| default model alias in examples (`jev-latest`) | pinned `jev-1.14.0`; a returned `model` that differs fails validation (`model_mismatch`) | report + skill's own advice on tuned thresholds; models page confirms the id |

## The parts that shape the design, mapped to plan tasks

| Skill element | Use in p15 | Where |
|---|---|---|
| **Judgments from Jev, decisions in code (truth tables)** | every experiment has `policy.py` with an explicit, exhaustively tested table over answer bands; Jev only supplies judgments; it never closes, rejects, routes or passes on its own | E1/E4 2.3, E3 2.3, E2 4.3, E5 3; contract J7 |
| **One judgment per question; beware "or"; one question per item** | E1 splits defect removal / obligation preservation / one `contradicts_dK` per dependency; E3 splits outcome / conflict / sufficiency; E2 splits same-behavior / incompatibility; tests reject instructions joining two judgments | `questions.py` tests in every plan |
| **State facts code already knows; only relevant fields; named fields; do not truncate silently** | packets carry code facts (verbatim flags, quotes found at lines N, references), exclude reviewer/reviser assertions and severity labels, use fixed descriptive keys, and are refused (never truncated) when oversize | E1 2.1, E3 2.1, E2 4.2; contract J1.6 step 3 |
| **Companion Noul for the null case (beats "none of the above" as of Jev 1.14)** | the report's `uncertain` / `insufficient` options become a companion sufficiency Noul plus the 0.3-0.7 band as its own truth-table row | contract J7; E1 `context_sufficient`, E3 `evidence_sufficient`, E2 `context_sufficient`, E5 `evidence_relevant` |
| **Confidence is rarely the gate; never do math on probabilities in Jev; 0.7/0.3 starting thresholds; beware over-fitting** | `confidence` never read; no products or sums of probabilities (E2 ranks by a lexicographic band key); 0.7/0.3 frozen a priori for E1 smoke and E3; calibrated thresholds fitted on calibration splits only and frozen by sha before held-out | contract J7; E1 3.2; E2 4.3 |
| **Bundle questions that share state; dependent stage = later call** | one request per packet with all its questions; E2's referenced-text retrieval is a later call with a new state | E1 2.2, E2 4.2 |
| **Test with the live API: representative, hard and negative cases; compare wordings in one request; keep exact payloads; check on untuned cases** | PLAN-0 `probe.py` (3 calls: Noul, Choice + companion, reordered Choice); every phase journals the exact request (contract J5); held-out sets never touched while tuning | PLAN-0 6; contract J5; E1/E2 splits |
| **When an answer looks wrong: payload, state (human test), options, scope, wording, then jaggedness** | the order of the "investigate a Jev error" note in each READY report and RESULTS; fixes go to state or decomposition, never to per-case wording | plans' risk sections |
| **Integrate: a failed call is an error, not a "no"** | every non-ok status (invalid, unavailable, refused) routes to the conventional path or keeps the finding open; missing key is a hard MANUAL stop, never a fallback | contract J1.5, J2; mock failure suites |
| **Option names are sent; descriptive names; positional names bias** | builder refuses positional option names (`a`, `option_1`, `left`) | contract J1.2 |
| **Cookbooks: Verify and escalate; Find and judge evidence; Screen with a Noul first** | E1/E4 and E3 are "verify and escalate" (cheap check, generative fallback); E2 is "find and judge evidence" over code-extracted candidates; E3's screen follows the noul-screen pattern but only on the positive side | plan designs |

## Jaggedness entries that bite here (live page)

| Weak spot | Exposure | Mitigation in the plans |
|---|---|---|
| Literal reading | obligations phrased differently after a fix | criteria describe "the same or different words"; paraphrase variants in E1/E3 test it |
| Indirection | reference chains (A -> B -> C) | E2 retrieves the referenced passage by code and asks a later call; E1 retrieves up to 3 dependencies, else not eligible |
| Large irrelevant state | long specs | packets hold excerpts only; E1 v3 distractor variants measure the effect |
| Adversarial content | self-justifying text inside a revised document | E1 v4 source-injection variants; E3 misleading-instruction perturbations |
| Choice option order | Choices | E3/E1 use Nouls (no order); E5 probe and PLAN-0 probe reorder options and require consistency |
| Numbers / counting | count and unit defects (T1, unit changes) | counts and units are code facts in the state (E2 extraction), never asked of Jev |

## Yellow flags (prompt gymnastics) as acceptance checks

Each READY report states that the implementer checked for: criteria naming a specific test item; a clause added per failing case; thresholds fitted to particular cases (only the calibration grid is allowed); tests asserting an exact probability (tests assert routing and validation, never a probability value); code quietly overriding answers (the truth table is the only consumer of answers). A wording change after the first live call bumps `QSET_VERSION` and is re-checked on cases not used for tuning.

## What the skill cannot settle (left to the experiments)

Whether Jev's calibration holds on spec-review judgments (no benchmark in this domain; E1/E3 measure Brier and reliability per question), whether a different model family decorrelates errors from the Sonnet/Haiku labelers and audits (measured, not assumed), and whether default retention is acceptable (zero retention not activated for this key; recorded as a risk).
