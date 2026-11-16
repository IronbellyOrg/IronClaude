# Round 1, advocate for variant 1 (analyzer)

Paths under `.dev/eval-workspaces/tasklist-review-panel/` (W). RL = `W/20261114-recipe-ledger`. All checks read-only.

## Steelman

Variant 2's best case: this is a live pre-registered experiment, and a cut is judged by what the run needs now, not by what past runs used. "Never used" expired when the addendum registered D1 to D7 and the freeze tag. The hook cut (C2) is the sharpest point: the 2026-11-16 owner answers require warnings for unknown, out-of-list, wrong-stage and requested-versus-served ids, plus explicit-user and approved-job exceptions. A 10-line policy that flags only restricted Opus ids silently drops owner requirements, and a "smallest version" nobody approved would become the record. Document swaps are cheap to make and costly to unwind, because readers trust the newest file. Provenance for C7 is disputed, so keep.

## Case for variant 1

Variant 1 does not cut the experiment. It keeps C5, C7 and C8, and it demotes C4 and C6 to after the hold-out. What it cuts now is prose only. Its code facts hold: `rl/reask.py` and `rl/spike.py` are listed in `RL/config/freeze.json`, and the freeze covers `briefs/`, `cards/`, `config/lenses.json`, `recipes/` and `rl/*.py` only. It also corrected the audit (analyze.py is far larger than claimed), which variant 2 accepts (X-002).

## Shared assumptions

**A-001 ACCEPT.** The 32 hashed paths in `freeze.json` are the briefs, cards, `config/lenses.json`, recipes and `rl/*.py` files. None of OPEN-QUESTIONS-20261115.md, OPEN-DECISIONS-20261115.md, the hook `OPEN-QUESTIONS.md` or TRIAGE-20261116.md is hashed. The addendum cites `../../OPEN-DECISIONS-20261115.md` once, as "Background and open questions", not as a frozen input. Editing in place is safe for the freeze. The risk is citations, so keep names and numbering.

**A-002 QUALIFY.** The two author launch scripts in `W/20261116-holdout/` read `.dev/tasks/done`, `.dev/reflect` and git history, and call `W/20261114-collab-process/with-slot.sh`. They forbid reading anything under recipe, sweep, collab or brainstorm paths. That matches the claim for the author step. But the later RL run, the gates D1 to D7 and the "ran" checks are invoked from RL per the addendum, so the claim holds only for the author session, not the whole hold-out. It also depends on `20261114-collab-process`, which no cut touches.

**A-003 REJECT.** Not cheap. Right now `git status` shows the RL folder with staged additions and edits (`PREREG-ADDENDUM-2-20261116.md`, `holdout-gt/*`, `config/prereg.json`, `config/packages.json`, `tests/test_prereg.py`; 12 files, 1,165 insertions). They sit in the same shared index. A `git mv` of 1,620 files stages 1,620 renames in that index. If the other session then runs a plain `git commit`, it commits all of them, and `git mv` back would be a second sweep. Nine worktrees share one repository, and about nine `claude` processes are visible. Archive moves need that session idle, with the move done in its own commit by pathspec.

## Disputed points

**C2: CUT NOW as a header only, 70%.** Concede to variant 2 on content. The smallest version drops owner-required behaviours, so replace nothing. Add a dated "proposed smaller version, not approved" section above the intact 63-requirement design, with a coverage map. No deletion, nothing substituted. This keeps variant 1's speed and variant 2's preservation.

**C4: CUT LATER, 80%.** Concede the machinery stays now. Run after the hold-out, then archive only the four unreferenced files (`analysis/ran_check.py`, `bin/ran-audit.py`, `analysis/g0.py`, `bin/open-manual-checks.sh`) with their tests. Variant 2's "KEEP" and my "LATER" differ only in time. Addendum item 9 on invalid runs might need the "ran" audit, so check that first.

**C6: CUT LATER, 85%.** Concede variant 2: migrate the `copy-shared.sh` reference first. The collab half moves only when the other session is idle (A-003).

**C9: CUT LATER (stage, label on owner's word), 65%.** Variant 2 is right that a label is harmless. Rule: `.dev/tasks/` is always staged, and the package is untracked. Stage it first (`git add .dev/tasks`), then add a SUPERSEDED note when the owner says so. Marking it cancelled unprompted is a state change nobody authorised.

## Missed invariants

1. **MEDIUM:** `config/prereg.json`, `config/packages.json` and `tests/test_prereg.py` are staged as modified after the freeze commit, yet the addendum says gates D1 to D7 are "unchanged" and `freeze.json` does not hash `prereg.json` or `packages.json`. Any cut near RL's config is unguarded by the freeze, and the registered gates themselves can drift. Evidence: `git status` in RL, grep of `freeze.json` (0 hits).
2. **MEDIUM:** `scaffold/` (the format allowances) is also outside the freeze. C8 keep is right but the allowances can still be edited unnoticed.
3. **LOW:** `.dev/tasks/` staging applies to every C9-style plan, so "cut" of a plan must not leave it untracked.

## Concessions

Variant 2 is right that C2 must not substitute a narrower hook design, that C4's "never used" argument is dead, that C6 needs reference migration first, and that a label-only C9 is low risk. I concede C1 should keep RL's freeze and maintainer-test questions. Not verified: hook requirement count, who calls `check-order.sh`, live state of the other session.
