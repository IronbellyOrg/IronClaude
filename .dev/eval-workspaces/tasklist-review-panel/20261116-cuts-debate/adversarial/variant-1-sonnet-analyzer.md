# Variant 1 (analyzer, cut aggressively where evidence supports it)

Paths are under `.dev/eval-workspaces/tasklist-review-panel/` (W). RL = `W/20261114-recipe-ledger`. All checks were read-only (git ls-files, git grep, grep, wc, jq).

Facts that change the debate: (a) the freeze already happened: tag `rl-freeze-1553f5dd29b1`, commit `4d4449928`, `RL/config/freeze.json` (32 files, includes every `rl/*.py`). (b) The hold-out folder `W/20261116-holdout/` holds only two author launch scripts and their output; neither names any RL script (they call `W/20261114-collab-process/with-slot.sh` and `claude -p`). The RL machinery is invoked from the RL folder later, per `RL/config/PREREG-ADDENDUM-20261116.md`.

## C1 CUT NOW
Evidence: documentation only, no code reads it. But `OPEN-QUESTIONS-20261115.md` is cited by `PREREG-ADDENDUM-20261116.md`, `POST-BUILD-LOG-20261115.md` and `collab-process/PROCESS.md`, so keep file and numbering. Risk if wrong: a dropped item was needed; citations break if renumbered. Change my mind: a live script that parses item numbers (git grep found only prose citations). Reversible form: add a "Voided 2026-11-16" section in place (items copied, not removed), or move to `W/archive/20261116/`.

## C2 CUT NOW
Evidence: `model-report` exists nowhere in `src/` or `tests/` (git grep empty), so replacing the 63-requirement design is a pure document swap; owner's warn-and-report decision supersedes it. Risk: later enforcement needs the cut parts. Change my mind: the owner reversing to halt-on-infraction. Reversible: keep old design file, add a "SUPERSEDED by smallest version" header; no deletion.

## C3 CUT LATER
Evidence: nothing exists; `install_hooks.py` `_SEED_FILES` is at line 104, so the seed point is real. But the hold-out plan uses Opus on purpose as blind judge (addendum item 4), so a restricted-id scan would flag every judge output unless it can allow by role. That design question is unanswered. Also the two-session cap and a running hold-out. Risk if built now: false incidents on legitimate judging. Change my mind: a one-line allow-by-role rule in the policy file. Reversible: a new command is additive; delete the plan, not code.

## C4 CUT LATER (only fragments CUT NOW-able)
Evidence against "18,000 lines": non-test code in RL is about 7,200 lines (analysis 2,231, bin 1,894, rl 1,791, scaffold 1,292); tests are 9,797. `analysis/analyze.py` is 1,587 lines, not about 450, and implements `prereg` and gates D1 to D7 that addendum item 6 says govern the hold-out. `analysis/judge_audit.py` (291) is called by `bin/judge-batch.sh` lines 47, 64, 79, 87. `bin/freeze.sh` was used. Unreferenced by the run path: `analysis/ran_check.py` (278), `bin/ran-audit.py` (85), `analysis/g0.py` (75), `bin/open-manual-checks.sh` (73); they appear only in each other, tests, docs and the shared manifest. Risk: addendum item 9 (invalid runs) may need the "ran" audit. Change my mind: `grep` showing the schedule or judge scripts never call `check-order.sh`. Reversible: `git mv` to `RL/_archive-unused/` with its tests; do it after the hold-out result.

## C5 KEEP
Evidence: `rl/reask.py` and `rl/spike.py` are both in `freeze.json`; `bin/run-panel.sh` lines 166 to 187 call `reask`; `config/lenses.json` has `"reask": true` for one lens; 96 run folders hold 50 `*.reask.json` records, 1 with `asked: true`. Removing a frozen file makes `freeze.sh --check` report REMOVED and voids the tag. `bin/run-schedule.sh` refuses (E_NO_SPIKE) without `values.json` spike record; that record exists (runs 5, c_luna 2.278). Risk if cut: invalid frozen comparison. Change my mind: the owner agreeing to refreeze. Reversible: after the hold-out, archive `bin/run-spike.sh` (119, not frozen) first.

## C6 CUT LATER (collab half: CUT NOW)
Evidence: no reference to either folder from `src`, `tests`, `.claude`, `plugins`, `Makefile`, `pyproject.toml`. Sweep Sheet: one live code hit, `RL/bin/copy-shared.sh` line 18 (hard-coded sibling path; no caller in bin, rl, scaffold, analysis), plus `RL/tests/test_shared_manifest.py` and 22-plus tracked `.dev/tasks/done` files that cite it. `20261113-collab`: code hits are only a negative assertion (`test_analyze.py:704`), a path string (`test_paths.py:21`) and `launch-build.sh` prose. `20261114-collab-process` (3 tracked files, `with-slot.sh`) is LIVE and is not part of this cut. Risk: a rename of 1,620 files in the shared worktree index while the hold-out session commits. Change my mind: the hold-out session being idle. Reversible: `git mv` to `W/_archive/`, one commit, `git mv` back.

## C7 KEEP
Evidence: the folder is tracked (not foreign); its README says verbatim copies from /tmp of files referencing this eval; 8+ brainstorm files cite `tmp-scripts`. Owner: keep intermediates. Gain is zero. Change my mind: owner calling them unwanted. Reversible: n/a; drop the open question (C1) instead.

## C8 KEEP
Evidence: the allowances are `scaffold/ledgerv1.py` lines 70 to 224 (fence_label, heading_between, heading_style, json_line_slack); addendum item 5 says they stay on; strict fails 47 of 81, lenient 1 of 81. Cutting them predetermines a failed gate. Risk if cut: invalidates the arm. Change my mind: owner choosing strict as the decision reading. Reversible: n/a. Side finding: `freeze.sh` hashes `rl/*.py`, not `scaffold/`, so the allowances are not covered by the freeze.

## C9 CUT LATER
Evidence: `.dev/tasks/to-do/TASK-WF-addOwnerApproved-20261115-210227/` is UNTRACKED (`??`, 0 tracked files), has no `progress.md` (never started), and is cited only by `sweep-sheet/OPEN-ITEMS.md` and `option1-report/forgive-plan.json`. Project rule: `.dev/tasks/` is always staged, never left untracked, so deleting is wrong. Risk: losing a reviewed plan. Change my mind: owner declaring forgiveness work dead. Reversible: add a SUPERSEDED note inside, then `git add .dev/tasks`; archive only on the owner's word.

## Ranked list
1. C1 and C2 as document edits (zero code risk).
2. Take C5, C7, C8 off the list.
3. Stage the C9 package (`git add .dev/tasks`); do not delete.
4. After the hold-out result: C4 fragments, the Sweep Sheet half of C6, then C3.
5. Collab-folder move only when the hold-out session is idle.

## Not checked
Did not open any ground-truth, score or judge file. Did not locate the model-policy hook design file or count its requirements. Did not find an "ablation" script (not searched inside `analyze.py`). Did not verify the audit's "3,679 JSON files" (tracked JSON with `modelUsage`: 35). Did not check whether `rl/*.py` imports `scaffold/` at runtime. Did not check who calls `check-order.sh`. Did not run any test or inspect the hold-out session's live state.
