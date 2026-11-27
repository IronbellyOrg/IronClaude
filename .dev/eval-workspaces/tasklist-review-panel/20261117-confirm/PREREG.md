# Confirming test of the wonsol panel: pre-registration (DRAFT, written 2026-11-17 before any run; final when the status line below says FROZEN)

Status: FROZEN (2026-11-17, before any run; the sha256 of this file is in `FROZEN.txt`). The plan numbers below come from the ground-truth authoring result (`author-out/SUMMARY.md`) and nothing else.

## Read this first (context for someone arriving with no history)

The "Review Panel" has cheap reviewer models read an implementation plan and report plan defects; a blind Opus judge scores each run against a hidden list of known defects (the answer key). In the stronger-panel test (`../20261116-stronger-panel/EXPERIMENT-REPORT.md`) one panel, `wonsol` = `muse-wonder-1.0` (seat S) + `gpt-6.1-sol` (L1) + `muse-ember-1.0` (L2), met its registered lever rule against the plain ember panel (found fraction 0.432 against 0.188). The evidence was weak: one hit among six arms compared with one control, a lead that came largely from a plan with 2 known defects (without it +0.091, lower bound below 0), a control run hours before the arm, and a control that scored 0.188, 0.223 and 0.325 on three days. The owner ordered (2026-11-17) a confirming test on NEW plans. This file fixes the design and the decision rule before any run.

## Question

Does `wonsol` find a larger share of the known defects of plans it has never been tuned on than the plain ember panel (control B) run in the same interleaved schedule?

## Design

- **Plans (new):** five plans, 33 known defects, 1 of them blocking: NP-1 `TASK-WF-implementTheDesi-20261031-182028` (8 items, 1 blocking), NP-2 `TASK-WF-detachTheCcsessi-20261102-034618` (9, 0), NP-3 `TASK-WF-authorizedNarrow-20261106-214325` (5, 0), NP-4 `TASK-WF-designOutput-20261111-193642` (6, 0), NP-5 `TASK-WF-analyzeCodegraph-20261111-193557` (5, 0). They were found in two authoring batches (`launch-author.sh`: 1 usable of 8 candidates; `launch-author-2.sh`: 4 usable of 10, 10 candidates in all being plans with an earlier review report that is not about the blocker or severity work); both wrote into `author-out/`, so the second summary replaced the first (the first summary's content is in the run log of this session, NP-1 and its notes are intact). Every quote was checked against its plan (33 of 33 found), every base is a verified commit. None was used in any earlier test of this project and none concerns the blocker or severity work. The answer key was written by a fresh Sonnet session (`launch-author.sh`, output `author-out/`) that had not seen any recipe or earlier result, before any run of this test, and is copied to `confirm-gt/` (never into a sandbox).
- **Arms (plain Z0 prompts, no recipes):** B = control, ember panel `muse-ember-1.0` (S) + 2 x `gpt-6-luna` (L1, L2); W = wonsol, `muse-wonder-1.0` (S) + `gpt-6.1-sol` (L1) + `muse-ember-1.0` (L2). Both defined in the one lens file `../20261114-recipe-ledger/results/stronger-panel/lenses/lenses-wonsol.json` (panel `primary` = B, byte-identical to the frozen panel; panel `sonnet` = W, label only). Seat lenses and table caps exactly as in the stronger-panel test.
- **Runs:** 2 arms x 5 plans x 5 replicates = 50 runs, one block per replicate, arm order inside a block shuffled from the seed (B and W interleaved in the SAME schedule, which removes the control-age problem of the earlier test), one panel at a time under the slot lock, fresh sandbox per run, harness unchanged (`bin/run-schedule.sh`), `NOFALLBACK=1`.
- **Judging:** one blind Opus judge per run (reviewer ids hidden, labels random); a second independent judge on a random 15% sample; any disagreement on the set of found defects is reported.
- **Invalid runs:** a killed reviewer with no output, an observed model different from the label, a launcher-flagged changed tracked file, or a missing Claude Code program: the run is moved aside (never deleted), re-run once with the same seed and block, both reported.
- **Models allowed:** the six the harness allows; Opus only as judge.

## Decision rule (fixed now)

Two measures, both arm W minus arm B, pooled over the plans, bootstrap as before (resample plans with replacement, then runs within each chosen plan, 2,000 draws, seed 20261120, lower bound = 5th percentile):

1. **M1 (the earlier registered metric):** mean over runs of the per-run found fraction (judge credit / items of that plan).
2. **M2 (every defect counts equally):** total defects found / total possible, over all runs of the arm.

**Confirmed** only if BOTH M1 and M2 show a difference of at least +0.10 with a lower bound above 0. **Not confirmed** otherwise; if exactly one of them passes it is reported as "not confirmed, split by weighting". Neither a leave-one-plan-out table nor any other analysis can change the label; they are reported as description. The stop rule (fewer than 3 usable plans or fewer than 25 defects: do not run) was met with 5 plans and 33 defects..

## Descriptive only (no rule)

Wrong blockers per run (blocking rows the judge could not match to a known defect), blocking defects found, rows per run, median and p90 panel seconds and the W/B ratio (earlier test: 1.8x; the +35% time cap of earlier studies is not applied), reviewer kills, found fraction per plan, defects found by no run.

## Pre-registered limits

- Only 1 of the 33 defects is blocking, so blocking findings are descriptive only. Each plan has few defects, so found fractions per plan are coarse (steps of 0.11 to 0.20 per run item).
- The package base for NP-2 to NP-5 is the task-start commit derived from history (the progress files record tree ids, not commits); three plans edit or cite files that exist only in the uncommitted start state (author caveats in `author-out/NP-*/notes.md`), which can make a sandbox lack a file the plan mentions.
- The harness edit to `bin/common.sh` (allow `gpt-6.1-sol` and `muse-wonder-1.0`) was already present locally from the earlier test and is pinned now in `config/runtime-hashes.json` together with the five new entries of `config/packages.json` (file hashes re-pinned 2026-11-17).
- One arm against one control: no multiplicity problem this time, but one test of one panel on 5 small plans (5 to 9 defects each); low power for small gains.
- The answer key is a model's, complete only to its items; a real unlisted defect counts as a wrong blocker.
- Plans only; one model family mix; the Claude Code program may update during the test (invalid-run rule).
- A "not confirmed" result does not show that wonsol is no better; it shows it did not clear this bar on these plans.
- Changing the default panel, pushing results and any follow-up test belong to the owner.
