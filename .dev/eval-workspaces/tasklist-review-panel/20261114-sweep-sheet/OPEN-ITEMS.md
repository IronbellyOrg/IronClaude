# Sweep Sheet: open items and decisions left (2026-11-15, about 13:55 UTC)

> **STATUS UPDATE 2026-11-16: STOPPED by the owner ("stop sweep sheet").** Reason: the freeze gate (extractor recall of at least 0.8 on plans seeded by someone who had not read the extractors) failed twice, before and after the fixture repair: 7 of 34 gated seeds located (21%); E1 2/11, E2 3/6, E3 1/5, E4 1/5, E7 0/7 (`results/freeze-check-20261115.md` and `results/freeze-check-20261115-rerun.md`). No extractor was tuned, no tag, hash list or freeze exists, no live panel run or control was ever done with this design. Everything below this box is the state at 13:55 UTC on 2026-11-15 and is kept for the record; items about the freeze, the hold-out author, the parity test and the shared control are void for the Sweep Sheet. Not built, by the owner's decision: the format-forgiveness plan `.dev/tasks/to-do/TASK-WF-addOwnerApproved-20261115-210227/` (plan written and reviewed, one blocking review finding resolved by a plan edit, not re-reviewed). The Recipe Ledger (`../20261114-recipe-ledger/`) continues and needs no extractor. The shared-control arrangement in `../20261114-collab-process/PROCESS.md` now concerns Recipe Ledger against Z0 only.

## Context for someone arriving with no history

**What the Sweep Sheet is.** A redesign of how the tasklist review panel works (the panel = a group of cheap AI reviewer models that review an implementation plan before it is built). Today each reviewer reads the whole plan and writes free-form findings, and cheap panels miss many real defects. The Sweep Sheet adds a **script pre-pass** (no model) that reads the plan and pulls out up to 12 typed "items" (for example a sentence that claims "every X" with a list that leaves one out, or a search pattern that does not match the text the plan orders written). Each item goes to cheap reviewers one at a time with a narrow question (OK, PROBLEM, UNSURE plus a quote). Findings flow into the normal review merge. The whole point is that a missed defect becomes a pointed question. The measure is: how many known real defects a cheap panel reports, compared with the plain panel (**Z0**) and a plain-words control (**K**), without raising run time by more than 35%.

**Where it comes from.** The brainstorm `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (Redesign 1). The design is `DESIGN.md` (822 lines, then edited), tests are `TESTING.md`, the build order is `IMPLEMENTATION.md`. A sibling redesign, the Recipe Ledger (`../20261114-recipe-ledger/`), is built by another session; the two are compared against one shared control. How the two sessions cooperate, and the owner-decision table, is `../20261114-collab-process/PROCESS.md`. The wider picture and shared rules (models, push rule, slot lock, what not to read) are in `../OPEN-QUESTIONS-20261115.md`: read its preamble first.

**Rules you must follow here (short form).** Push only to the fork `origin`, only when the owner asks; never touch `SuperClaude-Org`. Do not stage `.claude/`. `.dev/tasks/` stays staged. Python through `uv`. Sonnet or Haiku for all sessions; Opus only for the blind judge; at most 2 `claude` sessions at once via `../20261114-collab-process/with-slot.sh`. Never open `ground-truth*.json` or score files unless your task says so. Write only under this folder unless told otherwise.

## State on disk (verified 2026-11-15)

| Item | State |
|---|---|
| Build | 33 of 33 plan tasks complete; the build's own ledger says every task compliant and the final review passed. Not independently verified by this note's author. |
| Tests | I re-ran them: `uv run --frozen --project <repo> pytest -p no:cacheprovider tests -q -m "not freeze"` gives 749 passed, 4 deselected (the "freeze" tests). They use a fake `claude`; **no live model run has ever been done** with this launcher, so its live behaviour is unverified. |
| Plan package | `.dev/tasks/done/TASK-WF-implementHomeCod-20261114-200449/`, staged, not committed. A second package, `...implementRedesig-20261114-231318`, belongs to the Recipe Ledger session. |
| Commit | Nothing in this folder is committed. `freeze.sh` refuses to run until the frozen files are committed. |
| Owner values | `config/owner-values.json` (floor 0.45 and eight act bands) exists, not committed. `config/prereg.json` does not exist yet (written at the freeze). Decisions are recorded in `results/owner-decisions.md`. |
| Debates | `results/debate/1-act-bands`, `2-cb2-verbatim`, `3-k-lead` (VERDICT.md in each). `DESIGN.md` section 15.1a holds the new act-band registration text. |
| Second author | A fresh Sonnet session was started 2026-11-15 13:45 UTC (`launch-second-author.sh`, report in `second-author-report/REPORT.md` when it ends). It signs the card `swap_test` records and writes the recall fixtures. It is a session, not a person, by owner order. Result unknown at the time of writing. |

## The freeze (plan step 14): what is left

| Step | What | Who | State |
|---|---|---|---|
| 14.1 | Recall fixtures `fixtures/recall/` (3 or more real plans, defects seeded, `seeds.json`, `AUTHORS.md`) | second-author session | running |
| 14.2 | `swap_test` record of each of the 8 cards | second-author session | running |
| 14.3 | Owner values | owner | decided; `config/owner-values.json` written |
| 14.4 | `uv run ... pytest tests -q -m freeze` plus checks B1 and B3 of `TESTING.md` section 5 | maintainer | not run. Two of these tests need `LINT_REAL_GT_GLOB` (the real ground-truth files, read by a lint only) and the recall fixtures. Decide who runs them. |
| 14.5 | Commit the frozen files, `bash bin/freeze.sh`, review, run the printed `git tag` | a person by design; the owner said "go" | blocked on 14.1, 14.2, 14.4 and a commit order |
| 14.6 | Hold-out author writes `holdout-gt/`, commits it, then checks B6 to B9 | author session, then maintainer | not started; must follow the tag |

`bash bin/open-manual-checks.sh` prints the open manual records (19 at 13:00 UTC): swap tests for C1 to C8; recall authors; second reader of the cards README table; owner values (`config/prereg.json`); the spike record in `config/values.json`; the ground-truth attestation `config/attestation.md`; five `ATTEST` lines in `results/attestations.md` (freeze order, prereg order, report measured values, report headline, report claims); and the model-stage ablation (8 extra arms, 96 panel runs, not run: owner decision DD-13).

## Open decisions for the owner

1. **Who writes the hold-out ground truth** and signs `config/attestation.md`? A session is allowed by the owner's "use sessions" order for the freeze helpers; the owner has not yet said it also covers the hold-out author. The hold-out documents (HO-1 to HO-5) are not listed in any file I checked.
2. **Model-stage ablation** (DD-13): 8 extra arms and 96 panel runs. Run it or accept "not run"?
3. **Live spikes** (compliance, timing; `TESTING.md` section 5, step C): the owner must approve each live part. None has been approved for the Sweep Sheet.
4. **Commit order**: commit this folder and the plan package, then freeze, in that order. Needs an order from the owner. Pushing needs a separate order.
5. **The "owner decision if above 0" rule for CB-2** (found by the CB-2 debate): the count of `## Ledger` headings in Z0 and K reports has no rule for what the owner decides if it is above zero. Decide the rule before the first run or accept post-hoc discretion.

## Open work for sessions

- **Wrap launchers in the slot lock** (`PROCESS.md` O3): every `claude -p` in `bin/run-panel.sh`, the judge scripts and anything else must go through `with-slot.sh` before any live run. Not done.
- **Parity test with the Recipe Ledger launcher** (`PROCESS.md` section 4, M1): seven items, recorded in `../20261114-collab-process/parity.tsv`. Not written.
- **Publish the freeze hash list** to the Recipe Ledger session after the tag (it re-copies three files: `bin/common.sh`, `tests/test_briefs.py`, `tests/test_paths.py`).
- **Act-band measure code** (DESIGN 15.2): nothing computes the per-class measure or the "below" flag yet. `analysis/analyze.py` and `prereg()` have no field for the 15.1a text; until a follow-up adds code and tests the rule is applied by hand and the report says so.

## Known limits and risks (from the design and the debates)

- The pre-pass time budget (about 8 s) is a planning value. Measured on one full-size tree with a stand-in scope: the search took 0.9 s (`results/step0.md`).
- The merge accepts the extra `class`, `probe` and `src` keys on findings lines and drops them; telemetry must be read from the checked report, not the merged one. Tested on one report with 4 findings only.
- The design departs from the brainstorm in 15 places (`DESIGN.md` section 1.3), for example: a wider `quote_other` check, one attempt and no model fallback in counted runs, the single-class sheet filling 12 items (the pre-pass attaches evidence to the top 12 then; the time effect of 12 lookups is unmeasured).
- The act-band numbers are unmeasured planning values; the debate's fix and later additions were not re-debated.
- The three debates were scored by one Sonnet session each, and one "Haiku" advocate ran as `gpt-6.1-sol`. The verdicts are not an independent score.
- The selection-recall floor 0.45 is an estimate, not a validated figure: a design whose true recall equals the estimated lower-end mean (0.48) would still fail it 30 to 37% of the time by chance (binomial, assumes 20 to 40 hold-out issues).
- The earlier collaboration experiment found baseline panels near 1 of 14; see `../OPEN-QUESTIONS-20261115.md` question 7 for why the older 1.83 figure is doubtful.

## Where the numbers and decisions are

`results/owner-decisions.md` (decisions), `results/debate/*/VERDICT.md` (debates), `results/step0.md` (the three pre-build checks), `results/open-manual-checks.txt` (open records at build time), `DESIGN.md` section 15 (owner decisions) and 15.2 (open gaps), `TESTING.md` section 5 (the experiment commands: spikes, Stage 1, Stage 2, derivation check, decision), `IMPLEMENTATION.md` steps 14 to 16.
