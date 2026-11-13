# PILOT REPORT — tasklist-review-panel eval (EVAL 20261111-a1)

Date: 2026-11-11. Pipeline run through Step 4 (blind scoring) on the 3 pilot packages. Read-only eval; no source edits; nothing staged or committed.

## Setup

- Packages: TASK-WF-designSpec-20261107-075614 (10 GT defects, 5 blocking-in-implement), TASK-WF-makeTheAliasOnly-20261105-051649 (4 GT defects, 3 blocking-in-implement), TASK-WF-design-20261108-041415 (2 GT defects, 0 blocking-in-implement — control).
- Arms (from the same per-package reviewer runs; each reviewer ran once, fresh context, raw model ids via `claude -p`):
  - Arm A = the Tier 1b reviewer alone (claude-sonnet-5-5).
  - Arm B = the @default panel minus Qwen3.8-max slots.
  - Arm C = the @live7 panel minus Qwen3.8-max slots.
- Qwen3.8-max was disqualified by the owner after all 3 of its slots (one per package) timed out (attempts=2, 0 output tokens, meta wall 3000 s each; 9000 s wasted total). Arms B and C are merged without those slots. This is a deviation from the resolved panels, made by owner decision, and it slightly weakens B and C relative to their nominal composition.
- Category-label fix: reviewer reports produced before the fix used `unpassable-ac`; merges used `.catfix.md` copies with that one label changed to `unpassable-check` (9 files; originals unedited). Affected: designSpec t4-1; makeTheAliasOnly t1b-1, t2b-1, t3-2, t4-1, t4-2; design t1b-1, t3-1, t3-2.
- Scoring: 9 blind Opus subagents (one per package x label). Labels X/Y/Z randomly assigned per package (arm-key.json under arms/scoring/<pkg>/). Reviewer ids and file paths in each report were anonymized before scoring. Each judge wrote score.json with GT coverage, blocking coverage, and wrong blockers (blocking ledger rows with no ground-truth correspondence).

## Per-arm results

designSpec (10 GT, defect-rich)

| Arm | Verdict | GT covered any | GT covered blocking | Ledger rows (blocking) | Wrong blockers | Wall s | Output tokens |
|---|---|---|---|---|---|---|---|
| A (sonnet) | PASS | 1/10 (GT3) | 0 | 4 (0) | 0 | 260 | 34,744 |
| B (sonnet, muse-spark, glm) | PASS | 1/10 (GT3) | 0 | 9 (0) | 0 | 1,197 | 90,735 |
| C (sonnet, muse-spark, terra, glm, haiku, grok) | FAIL | 2/10 (GT3, GT7) | 0 | 13 (1) | 1 | 2,355 | 196,357 |

makeTheAliasOnly (4 GT, defect-rich)

| Arm | Verdict | GT covered any | GT covered blocking | Ledger rows (blocking) | Wrong blockers | Wall s | Output tokens |
|---|---|---|---|---|---|---|---|
| A (sonnet) | PASS | 0/4 | 0 | 4 (0) | 0 | 198 | 26,694 |
| B (sonnet, muse-spark, glm) | FAIL | 0/4 | 0 | 7 (1) | 1 | 1,874 | 135,517 |
| C (sonnet, muse-spark, muse-wonder, glm, grok, luna) | FAIL | 0/4 | 0 | 6 (2) | 2 | 2,785 | 200,371 |

design (2 GT, control; neither GT blocking-in-implement)

| Arm | Verdict | GT covered any | GT covered blocking | Ledger rows (blocking) | Wrong blockers | Wall s | Output tokens |
|---|---|---|---|---|---|---|---|
| A (sonnet) | FAIL | 1/2 (GT1) | GT1 | 1 (1) | 0 | 244 | 31,660 |
| B (sonnet, glm, glm) | FAIL | 2/2 | GT1, GT2 | 2 (1) | 0 | 2,547 | 167,953 |
| C (sonnet, glm, glm, haiku, luna) | FAIL | 2/2 | GT1, GT2 | 2 (1) | 0 | 3,367 | 207,368 |

Wall seconds are per-reviewer sums (reviewers in an arm ran concurrently), from each reviewer's meta.json.

## Totals and efficiency

| Arm | GT caught (any, all 3 pkgs) | Blocking recall on defect-rich (8 items) | Total wall s | Total tokens | Catches per 100k tokens | Wrong blockers (all pkgs) |
|---|---|---|---|---|---|---|
| A | 2/16 | 0/8 | 702 | 93,098 | 2.15 | 0 |
| B | 3/16 | 0/8 | 5,618 | 394,305 | 0.76 | 1 |
| C | 4/16 | 0/8 | 8,507 | 604,096 | 0.66 | 3 |

Judge cost (Step 3): 9 Opus subagents, 1,034,575 output tokens total, ~139 s summed wall. Judge score.json files are under arms/scoring/<pkg>/<label>/.

## Fixed decision rule

"Recommend a panel only if on defect-rich packages it catches >= 2x arm A's defects at any severity AND averages <= 1 wrong blocker per plan on controls."

- Defect-rich catches: A = 1, B = 1, C = 2. B fails (1 < 2x1). C passes exactly (2 >= 2x1).
- Wrong blockers on the control package: A = 0, B = 0, C = 0. All pass.

Under the rule as written, only Arm C qualifies, and only marginally: the margin is one defect (GT7) on one package, and C's blocking recall on defect-rich packages is 0/8, identical to A. On controls C (and B) both matched their single blocking rows to real GT defects, so nothing was spuriously blocking there; C's 3 wrong blockers all sit on defect-rich packages, where the rule does not penalize them.

## Paired comparisons (descriptive only; n=3, nothing approaches significance)

- B vs A on GT-any per package: tie, tie, B+1. Sign test 1/1, p=0.5.
- C vs A: C+1, tie, C+1. Sign test 2/2, p=0.25.
- Costs are unpaired and large: B costs 4.2x A's tokens, C costs 6.5x A's tokens for +1 and +2 catches respectively.

## Honest read

All three arms missed every ground-truth defect that actually blocked the implement runs (0/8 blocking recall on defect-rich packages). The panels' extra reviewers mostly added non-blocking rows (B: 9 and 7 rows with 0-1 blocking; C: 13, 6, 2 rows) and all of C's blocking rows on defect-rich packages were wrong blockers or non-GT. The one place bigger panels helped is coverage of non-blocking defects (4/4 vs 2/4 GT-any on the control; GT7 on designSpec). Single-reviewer Arm A passed both defect-rich packages — the worst observed outcome for a gate whose job is to fail bad plans.

## Stated limits

- n=3 packages; every comparison is underpowered by design at pilot stage.
- Judge is a single Opus pass per (package, label); judge variance is unmeasured (no double-scoring).
- Qwen removal weakens B and C vs their nominal resolutions; the comparison is of the post-removal panels.
- The `unpassable-ac` category bug invalidated several reviewer findings blocks before the fix; catfix copies restore them for merging, but any reviewer whose block was rejected only by that label is included while c1's designSpec haiku run (missing `## Findings block` heading entirely, 15 findings ignored) is a separate reviewer-side format failure not repairable by catfix — it affected a combo run, not these pilot arms.
- GT items are defects observed in past implement runs; a panel finding a true defect not in GT would be scored as a wrong blocker if blocking. That penalizes genuine novel catches; with only 3 such rows observed, the risk did not materialize, but it is a structural bias of the scoring.

## Next (awaiting coordinator approval)

The 6 remaining packages are staged for the same pipeline only after approval. Separately, the 15 owner-ordered combo runs (5 batch-1 + 10 batch-2 reviewer-model combinations) are running in parallel workers; once all are validated they will be blind-scored with the same procedure and compared against arms A/B/C.
