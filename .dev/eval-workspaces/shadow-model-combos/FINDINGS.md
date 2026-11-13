# Findings: 5 model combinations x 3 repeats (descriptive, not scored against ground truth)

Date: 2026-11-13. Input: `TASK-WF-designSpec-20261107-075614`. Skill frozen (hashes in `logs/block-<n>.skill-hash`, unchanged for all three blocks). Data: `results.jsonl`, `results.md` (made by `analysis/extract.py`), stream logs in `logs/`. All 15 runs reached manifest `published` with 3 of 3 reviewers complete. No blind quality scoring was done, so nothing here says which combination finds more REAL defects.

## Did each combination run the models it was meant to? (stream logs: requested class vs served model)

| Combo | Reviewer slots served as | Runs as designed |
|---|---|---|
| A baseline | sonnet-5-5 / gpt-6.1-sol / opus-5-5 | 2 of 3. A3 collapsed: the orchestrator passed no class, so all three reviewers and all calibrators ran on claude-sonnet-5-5 |
| B | same as A | 3 of 3 |
| C | sonnet-5-5 / haiku-5-5 / opus-5-5 | 3 of 3 (the only combination where the "haiku" slot is really Haiku) |
| D | sonnet-5-5 / haiku-5-5 / gpt-6-luna | 3 of 3 |
| E | haiku-5-5 / gpt-6-luna / gpt-6-luna | 3 of 3: the study's best panel; 3 reviewers, 2 distinct models |

The slot called "haiku" in A and B is served by gpt-6.1-sol. The panel record (`panel/resolution.json`, card headers, `panel_parity`) never shows this; only the transcripts do.

## Per combination (median, min to max over 3 runs)

| Combo | Minutes | Calibrated confidence | Clustered findings | First-pass compliance | Output tokens |
|---|---|---|---|---|---|
| A | 64 (19 to 68) | 0.77 (0.75 to 0.84) | 21 (13 to 24) | 0.67, 0.67, 0.67 | 220k (94k to 221k) |
| B | 25 (23 to 39) | 0.71 (0.68 to 0.78) | 12 (11 to 25) | 1.0, 1.0, 1.0 | 241k (200k to 335k) |
| C | 33 (33 to 34) | 0.74 (0.68 to 0.76) | 19 (14 to 27) | 1.0, 1.0, 1.0 | 335k (312k to 363k) |
| D | 27 (18 to 30) | 0.65 (0.62 to 0.66) | 16 (15 to 19) | 1.0, 1.0, 1.0 | 296k (185k to 330k) |
| E | 24 (22 to 30) | 0.59 (0.53 to 0.68) | 19 (15 to 23) | 1.0, 0.67, 0.33 | 321k (299k to 367k) |

## Leads under the pre-set rule (ranges do not overlap, median gap larger than A's own range, 2 of 3 runs as designed)

1. **Orchestrator speed:** A's two runs that dispatched as designed took 64 and 68 minutes; B, which differs only in the orchestrator (tier1b instead of tier3), took 23 to 39. A3, the collapsed run, took 19. Cause not isolated.
2. **Calibrated confidence:** D (0.62 to 0.66) and E (0.53 to 0.68) sit below A (0.75 to 0.84). B and C overlap A. The calibrator's model also differs between combinations, so this may be the calibrator, not the reviewers.
3. **First-pass format compliance:** every A run had one reviewer fail the first parse (0.67 three times); B, C and D were 1.0 in all nine runs; E fell from 1.0 to 0.67 to 0.33 (a trend of three, not a result).

## Not different, or not meaningful at n=3

- Clustered finding counts overlap heavily across all five combinations. Verdict wording is free-form and varies run to run.
- C against B (real Haiku against GPT-6.1-sol in the haiku slot): no separation on any measure here.
- Gateway cost in USD is Claude Code's estimate from model names, not a billed figure; do not compare it. Token ranges overlap.
- Parity and lint problems appear in all combinations (A 3 of 3 parity failures, mostly alias text in the contract and one card header missing fields; C2 lacked the legacy rotation keys). They reflect orchestrator contract-writing lapses more than model choice. I did not extract the lint reasons per run.

## What this does not establish

Whether any combination finds more real defects. That needs the blind scoring against the study's ground truth (10 defects, 5 blocking), which spends extra tokens and was left to a separate approval.
