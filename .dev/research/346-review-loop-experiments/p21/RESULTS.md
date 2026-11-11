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

# Part 2: setup or model? Plus the 7-reviewer dedup pilot (2026-11-11)

This part follows the TypeSafe skill and the live docs (`model-jaggedness`, `models`, primitives), read on 2026-11-11. Jev cost for part 2: about $0.50 (A2 diagnostic $0.12, pilot $0.32, Noul variants $0.05). Model-side cost: two Sonnet labelers and one Opus labeler.

## Verdict

| Failure | Our setup | The model | Evidence |
|---|---|---|---|
| A2 "can this check pass?" (precision at the base rate, 88% `cannot_pass`) | **The bias was ours.** The packet failed the docs' "human test": 8 of the 12 checks Opus judged flawed needed spec rows the packet left out. The question was a compound Choice with an "insufficient" none-of-the-above option and asked for a verdict, not a judgment | **The lack of signal is the model's.** With the full spec, the same question flips to 44/46 `can_pass` but still doesn't separate flawed checks (AUC 0.40). Atomic Nouls reach at most 0.65. Running a check in your head against a 60 KB spec is multi-hop System Two work (jaggedness #4 and #5) | `a2diag/analysis.txt` |
| A1 support, A3 revision novelty | Same pattern as A2: four- and five-option compound Choices with a none-of-the-above option | Not re-tested. Both are the same multi-hop kind of task | `p18/seams/a1_support.py`, `a3_novelty.py` |
| E1 fix vs deleted obligation | **Not our setup.** Atomic Nouls, fields named by path, a sufficiency companion question: what the docs recommend | **Not specific to Jev either.** The conventional LLM checker agreed with Jev 97% of the time and made 2 of the same 3 false closures. The zero-false-closure gate stopped both | `p15/e1/offline-results.md` |
| E3 confirmation screen (17.9% automation) | Followed the guidance (decomposed Nouls) | Inconclusive: the 20% gate measures how often Jev may skip the verifier, not accuracy | `p15/e3/questions.py` |
| Test 2 stop rule (AUC 0.30) | **Ours.** It asked Jev to make a decision from counts, which the docs warn against twice | No signal exists to find: no single count predicts the outcome either | part 1 |
| Test 1 dedup (precision 0.6 to 0.8) | **Not our setup.** A Noul matches the two-order Choice (AUC 0.993 vs 0.992) at half the calls | **Not the model either.** At P >= 0.9, 96 to 100% of flagged pairs share a ledger defect. The "errors" are neighbouring ledger defects, a property of how finely the ledger splits defects | below |
| Test 3 issue mode | **Partly ours.** A Noul in place of the three-option Choice lifts title-only accuracy from 0.75 overall (0.91 of answered) to 0.94. Outside 0.3 to 0.7 it is 45/45 on full descriptions, covering 87% vs 69% for the Choice's p >= 0.9 gate. Option order mattered little (50 and 51 of 52 unchanged) | Works | `issues/answers-noul.json` |

**In short:** the client, model id, payload and validation were sound. The response model was always `jev-1.14.0`, and the payloads are logged in the journals. Our failures came from two things. (1) We aimed Jev at System Two tasks: running a check in your head, judging whether a revision fixed a defect, predicting whether a loop would converge. The docs list exactly that as a weak spot, and no change of wording or state rescued it. (2) Some of our questions were built against the docs' advice: compound options, none-of-the-above options, decisions instead of judgments, and state that fails the human test. Those flaws produced the striking negative bias. Fixing them removed the bias but did not add a signal. On System One tasks (are two short findings the same defect? is this request a bug report?), Jev is accurate, and the question format barely matters.

## 7-reviewer dedup pilot

**Data.** Round-1 findings of pn1d2 runs d2-r1 (78 findings) and d2-r2 (92 findings), from 7 reviewers each (1 Sonnet + 6 Haiku). They come from each report's `findings-v1` block, together with the merge's grouping (ledger rows). Sonnet mapped every finding to ledger defects (or NEW / NOT_DEFECT). Opus labelled d2-r1 a second time: it agrees with Sonnet on the main defect for 75/78 findings and on 17 of the 21 "same" pairs. Of 6,090 cross-reviewer pairs, 4,839 have a usable label (56 same, 32 overlap, 4,751 different). The other 1,251 are pairs where neither finding maps to a ledger defect. Jev answered a Noul and the part-1 Choice for every pair (12,180 calls).

| Rule (Sonnet labels, both runs) | flagged | precision (same) | precision (same or overlap) | recall |
|---|---|---|---|---|
| Current merge: same ledger row | 2,133 | 0.02 | 0.04 | 0.88 |
| Jev Noul >= 0.5 | 87 | 0.48 | 0.66 | 0.75 |
| Jev Noul >= 0.7 | 54 | 0.67 | 0.83 | 0.64 |
| Jev Noul >= 0.9 | 23 | 0.78 | 0.96 | 0.32 |
| Same merge row AND Jev Noul >= 0.7 | 52 | 0.67 | 0.85 | 0.62 |

- AUC (same vs different): Noul 0.980 and Choice 0.975 on Sonnet labels; 0.996 and 0.994 on Opus labels. The 7-reviewer panel reproduces the part-1 result.
- **The current merge over-groups by about 25x.** It joins any findings that share a section reference. In these runs 21 and 27 distinct ledger defects were collapsed into 26 and 20 rows: 15 and 22 defects share a row (and so one adjudication verdict and one blocking flag) with a different defect. Run d2-r1's row L1 held 7 reviewers' findings and 36 sub-claims. The reviser saw all of them, but the adjudicator ruled on the row once.
- **Splitting each merge row with Jev** (union of pairs with Noul >= t): at t = 0.7, d2-r1 goes from 26 to 56 rows and the shared-row defects drop from 15 to 2; d2-r2 goes from 20 to 66 rows and from 22 to 6. At t = 0.9 no defect shares a row, but 65 and 80 rows remain for 21 and 27 defects: real duplicates go unmerged (recall 0.32).
- **Cost:** about 3,000 cross-reviewer pairs per run is about $0.05 of Jev with one Noul per pair. Restricting the calls to pairs inside a merge row (35% of pairs; 88% of true duplicates) is about $0.02 per run.
- **Tokens:** splitting does not save tokens. It raises the number of adjudicated rows by about 2 to 3 times, which adds Sonnet adjudicator input. The case for it is quality: one verdict per real defect, and no blocking flag spreading over unrelated sub-claims. Whether that improves the final spec is unmeasured.

## Recommendation

1. **Use Jev for row splitting in the merge**, not for dropping anything: Noul >= 0.7 inside each merge row; both texts stay in every row. Then run a live A/B of PN1 with the Jev-split merge against the current merge. Score both with the 44-defect ledger, as in the replicate (6 runs per arm, blocked randomization).
2. **Keep Jev off System Two placements** (A1/A2/A3, E1/E4 fix verification, loop control). The re-tests show no rescue from better wording or a fuller state.
3. **For any new Jev question:** a Noul per judgment, state that passes the human test, decisions in code, and a check that the option order doesn't change the answer. These rules are in the TypeSafe skill and docs. Test 3 shows the Noul form is the better default for us.
