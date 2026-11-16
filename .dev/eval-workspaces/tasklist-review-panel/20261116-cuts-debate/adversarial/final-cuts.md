# Final list of cuts after the adversarial debate (2026-11-16, depth quick)

Context for a reader with no history: see `../source-proposed-cuts.md` (the nine proposed cuts) and `diff-analysis.md`. Two variants (Sonnet analyzer, Haiku architect), one round of advocate statements (`debate/round1-advocate-1.md`, `round1-advocate-2.md`), then this merge. Quick depth skips the rebuttal round and the invariant probe; two missed invariants raised by the advocates are included below. Advocate agents were Sonnet and Haiku-alias only (no Opus); the Haiku alias may have been served by another model, which was not checked. Scoring and merge were done by the orchestrating session in a condensed form (not the skill's 30-criterion dual-pass rubric), so the convergence figure is not an independent score.

## Result

Convergence: 12 of 12 points agreed on direction (9 cut verdicts, 3 shared assumptions) after advocate 1 conceded C2, C4, C6 and C9. Same-direction agreement after concession is weaker evidence than independent agreement. Status: success with the caveats above.

## Survivors: executed in this session (documentation only, nothing deleted)

| ID | Cut | What is done | Condition checked first |
|---|---|---|---|
| C1 | Trim the master open lists | Add a dated row-status table at the top of `OPEN-QUESTIONS-20261115.md` and `OPEN-DECISIONS-20261115.md` mapping every row to void, settled, deferred or live. Rows, numbers and anchors stay intact. | `freeze.json` hashes neither file (verified by both advocates). RL's amendments (hold-out documents HO-2, HO-3, HX-1, HX-3 chosen; HO-1, HO-4, HX-2 dropped) are reflected. RL's freeze and maintainer-test questions stay live. |
| C2 (reduced) | Hook design: header plus coverage proposal, no replacement | A non-authoritative header under the title of `merged-requirements.md`, and a proposed coverage table appended to the hook `OPEN-QUESTIONS.md` mapping each retained owner behaviour to the smaller reporting design as retained, deferred or unresolved. All 63 requirements, original questions and owner answers stay. | The owner's 2026-11-16 answers are not paraphrased away. The table states that incident reporting is separate from run eligibility. |
| (correction) | Correct the audit claims in `TRIAGE-20261116.md` | A dated correction box: analyze.py is 1,587 lines and holds the D1 to D7 gates, non-test RL code is about 7,200 lines, the RL freeze exists, re-ask and spikes are frozen files. | Evidence from advocate reads and the RL session. |

## Deferred with a condition (not executed)

| ID | Cut | Condition before it can happen |
|---|---|---|
| C3 | Build `model-report` | Owner order; a rule that allows the blind Opus judge by role; verified output-file layouts; a checked plan through `/sc:workflow`. |
| C4 (fragments only) | Archive `analysis/ran_check.py`, `bin/ran-audit.py`, `analysis/g0.py`, `bin/open-manual-checks.sh` | Stage 1 and judging finished; invalid-run handling confirmed not to need the "ran" audit; reference audit; the RL session idle; one `git mv` commit with explicit paths. |
| C6 | Archive the Sweep Sheet and collaboration folders | Same, plus migrate `RL/bin/copy-shared.sh` line 18 and the reading lists that cite them, and leave forwarding indexes. `20261114-collab-process/with-slot.sh` is live and is excluded. |
| C9 | Label the unbuilt forgiveness plan package cancelled | The owner's word. Never move an unexecuted plan to `done/`. It is untracked; the `.dev/tasks/` staging rule applies when it is committed. |

## Rejected (removed from the proposal)

C5 (re-ask and spikes are frozen and called by the launcher), C7 (tracked, cited, keep-intermediates rule), C8 (the format allowances are registered and the result depends on them). C4 as proposed ("cut about 18,000 lines") is rejected: the audit overstated it.

## Invariants raised and kept

- **HIGH.** Warn-and-report for model usage is not permission to count invalid experimental data as valid: keep incident reporting separate from run eligibility (addendum 1 invalidates model-label mismatches).
- **MEDIUM.** The freeze does not cover `scaffold/` (the allowances), `bin/`, `analysis/` or the config files; the RL session added run-time hashes and a check script (its report, not independently verified). Freeze success alone does not show unchanged machinery.
- **LOW.** An untracked plan package breaks the `.dev/tasks/` staging rule.

## What was not checked

The hook requirement count, who calls `check-order.sh`, whether `rl/*.py` imports `scaffold/` at runtime, the live state of the running hold-out, and the Haiku-alias model identity. No tests were run. Nothing was committed.
