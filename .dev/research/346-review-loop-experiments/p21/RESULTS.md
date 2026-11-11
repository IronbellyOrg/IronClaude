# p21: three offline Jev tests (2026-11-11)

These are three proposed new uses of Jev (TypeSafe System One, `jev-1.14.0`), each tested offline against ground truth we already had or built here. The Jev calls are made through `jrun.py`, which wraps the p15 `jevlib` client (budget ceiling, journal, privacy filter, answer validation). Jev cost for all three tests: about $0.107 (2.55M input tokens, 2,016 calls). Model-side cost: 24 blind Sonnet scorers for test 2 (about 4M subagent tokens) and one Sonnet agent for the test 3 baseline.

| Test | Question to Jev | Result | Verdict |
|---|---|---|---|
| 1 Duplicate findings | "Do these two findings describe the same defect?" | AUC 0.99; at P(same) >= 0.9, precision 0.83 (0.88 counting partial overlaps), recall 0.65 | Strong signal. Below the 95% precision bar; worth a merge-step pilot |
| 2 Stop before the second revision | "Will one more revise + re-review help?" | AUC 0.30 (worse than chance); the second cycle helped in 19 of 24 runs | No role. Keep the cycle |
| 3 Issue mode (bug / feature) | "Is this request a bug or a feature?" | 96% on title + excerpt; 100% on the 69% it answers with p >= 0.9; Sonnet 98 to 100% | Works, and cheap. Small saving: the worker still does the rest of the job |

## Test 1: duplicate findings (dedup before adjudication)

**Data.** All 932 pairs of first-review findings inside the same run (70 runs), from `p17/findings.jsonl`. The labels come from the p17 ledger mapping (finding -> chunk defect -> ledger defect D01-D44). A pair is `same` when both findings map to the same defect set: 31 pairs (3.3%). Another 23 pairs partly overlap, and 878 map to different defects. The question was asked in both orders (1,864 calls). Order agreement was 923 of 932 pairs.

| Rule | vs `same`: TP / FP / FN, precision, recall | flagged |
|---|---|---|
| Jev, both orders say `same_defect` | 26 / 17 / 5, 0.60, 0.84 | 43 |
| Jev, min P(same) >= 0.7 | 23 / 12 / 8, 0.66, 0.74 | 35 |
| Jev, min P(same) >= 0.9 | 20 / 4 / 11, 0.83, 0.65 | 24 |
| Code: shared section reference (what the PN1 merge does) | 31 / 428 / 0, 0.07, 1.00 | 459 |
| Code: any shared spec line | 28 / 278 / 3, 0.09, 0.90 | 306 |
| Code: line Jaccard >= 0.3 (best code rule) | 23 / 21 / 8, 0.52, 0.74 | 44 |

- **Separation:** AUC 0.992 for Jev's min P(same), against 0.927 for line Jaccard. The median P(same) is 0.92 for true duplicates, 0.09 for partial overlaps and 0.00 for different defects. Of the 261 "hard negatives" (different defects citing a shared line), Jev called 10 the same.
- **Errors at P >= 0.9:** all 4 false positives are neighbouring ledger defects (D01/D02, D11/D12, D09 vs D06-D08, and D22 vs D21+D22). A human merge might plausibly group them too. The misses are mostly broad findings that map to five defects at once.
- **Context:** the PN1 merge groups findings by shared section references. Run d2-r1's L1 row merges findings from all 7 reviewers with 31 refs. That rule's precision on these pairs is 0.07, so it over-merges heavily. Duplicates are rare in 1-3 reviewer arms (0.4 duplicate pairs per run). The data has no labelled 7-reviewer panel findings, so the headroom for the live panel is unmeasured.
- **Verdict:** this is the first placement where Jev beats a code rule on our own data, and it does so clearly. It does not reach the 95% precision bar, so it should not merge on its own. Next step: use it to split or confirm the merge's groups, never to drop a finding (both texts are kept). Label one panel run's per-reviewer findings against the ledger to measure the real headroom.

## Test 2: stop before the second revision

**Ground truth (new).** The intermediate spec (after V1, before V2) of all 24 PN1-family runs (pn1o, pn1d2, pn1d, pn1m) was scored blind with the p17 instrument as s106-s129 (`stop/scores/`). It was compared with the existing final-spec scores s82-s105. Every run went through V2 and round 3 and ended in ESCALATE.

- V2 + round 3 changed the fixed-defect count by a median of +1 (mean +1.4). The weighted residual changed by a mean of -3.5, which is better. It helped in **19 of 24** runs. In 5 it did nothing or made things worse: d1-r5 +3, d2-r1 +1, m1-r4 0, m1-r5 +4 and o2-r1 0. The best run (o2-r5) fixed 5 more defects.
- Jev saw the loop's own state after round 2: round-1 findings and blocking findings, round-2 new findings, refound and reported-resolved counts, blocking findings still open, blockers sent to V2, and the size and growth of the first revision. Asked two ways, Jev said "worth it" on 42 of 48 calls. The AUC of P(help) was **0.30 for both wordings**, worse than chance.
- No single state feature works as a stop rule either. The best is round-2 new findings (AUC 0.21, so fewer new findings means more help), but a threshold that catches 3 of the 5 bad runs also stops 5 good ones.
- **Verdict:** no Jev role, and no stop rule. The second cycle pays off in 79% of runs, so skipping it would cost about 1.4 fixed defects per run to save one revise and one single-reviewer re-review. This repeats E5's pattern: no signal for Jev to use. With n = 24 and 5 bad runs, the feature results are anecdotal.

## Test 3: issue mode for `/sc:issue --create`

**Data.** The repo's issues, with the label (`bug` / `enhancement`) as truth, falling back to the `[BUG]` / `[FEATURE]` title prefix. That gives 52 issues (25 bug, 27 feature) after dropping two disposable test issues that name their own answer. Each issue was given as the title with its prefix removed, alone and with an 800-character body excerpt (headings removed). The excerpt stands in for the user's description. URLs, emails and the org name were redacted after the jevlib privacy filter refused 13 excerpts. Only 5 issues have a Complexity value and 19 an issue type, too few to test.

| Classifier | Title only: decided, accuracy | Title + excerpt: decided, accuracy |
|---|---|---|
| Jev | 43/52, 0.91 | 52/52, 0.96 |
| Jev, only when max p >= 0.9 | 25/52, 1.00 | 36/52, 1.00 |
| Sonnet (one blind agent, same inputs) | 49/52, 1.00 | 50/52, 0.98 |
| Keyword rule | 52/52, 0.62 | 52/52, 0.60 |

- **Verdict:** Jev is nearly as accurate as Sonnet on this question, at about $0.00002 per call. With a 0.9 gate it answered 69% of full descriptions with no errors; the rest would go to the existing worker.
- The saving is small, though. A worker chooses the mode only when `--mode` is missing, and the same worker also chooses the area (`--type`) and, at standard and deep depth, runs `/sc:analyze`. Jev removes the worker only in the case "quick depth, only `--mode` missing". It's a safe, cheap add, but it isn't where the tokens go.
- Caveat: the issues were written through the repo's templates, so even with headings removed, the excerpt reads cleaner than a raw user description.

## Files

- `jrun.py`: the shared runner (resumable answers, budget ledger and journal).
- `build_v2_score.py`: built the blind scoring inputs s106-s129.
- `dedup/`: pair builder, Jev driver, analysis (`analysis.txt`), answers.
- `stop/`: ground truth (`truth.py`, `truth.json`), loop state (`state.py`), Jev driver, scores s106-s129 with `key-v2.json`.
- `issues/`: case builder, Jev driver, Sonnet prompt and answers, analysis.
- Journals (18 MB for test 1) stay in the session scratchpad and are not committed.
