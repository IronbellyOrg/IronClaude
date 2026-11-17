# Plan input for the blocker-classification change (issue #552)

Status: input only. No plan has been written and no file under `src/`, `tests/`, `.claude/` or `plugins/` has changed. Run the command below only when the owner asks for the plan.

## Command to run

```text
/sc:workflow "Loosen blocker classification across the review loops as specified in .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md (issue IronbellyOrg/IronClaude#552). Record non-blocking findings in a follow-up ledger and offer to file them as issues, instead of halting and forcing re-reviews. Apply the reconciliation in 09-plan-input.md. Code and text: the review-loop skills and agents listed in section 10 of the spec (task, tech-research, rf-qa family, pragmatic output style) plus WORKER-CONTRACT.md." --depth standard --handoff none
```

## Reconciliation the plan must carry (found while checking the spec against the program results)

1. **Table size.** The spec assumes 30 to 40 scored rows and an empty table at writing time (sections 7.4 and 7.6, `seed-brief.md:25`). The table now exists: 318 rows in `04-historical/master-table.md`, scored in `05-scoring/consensus.md` (82 blockers at a mean of 4.0 or higher; three scorers all proposed threshold 4). Stage 0 steps 0a and 0c are therefore not skipped. The held-out half for thresholds is about 159 rows, not 15 to 20.
2. **Stage 0a already has a result, from a stand-in judge.** Five runs with a Claude judge on a text-only variant (`08-test/results.md`): agreement with the panel 58.5% (Cohen's kappa 0.27), precision 37.6%, recall 92.7%, 41.5% of findings change call between runs. This is not a Jev run and not the full classifier. The spec's own rule stands: no classifier authority in version 1 (G5, REQ-22, OD4). The result supports it.
3. **M, C and E need code-supplied inputs.** In the text-only variant they were at chance (AUC 0.53 to 0.55). The spec already lists their code inputs in section 7.2; the plan must make the classifier run those questions only when code supplies the required-item list, the constraint lines and the verified evidence, and report how many rows had each. The "M or C is Y means BLOCKING" row of the truth table must not be enabled for any gate until a run with those inputs has been measured.
4. **The result is partly circular.** The test questions were finalised after reading the scored table (`07-classifier/questions.md` says so). The plan's second test round needs fresh findings that were not in the 318, plus findings a reviewer called minor that later proved real (selection bias, spec section 7.6 weakness 2).
5. **The same defect repeats.** Six defects account for about 43 of the 82 blockers (`06-blocker-characteristics.md`). The held-out set must not be split so that repeats of one defect fall on both sides.
6. **Confidence is not a gate.** BLOCKING verdicts at stated confidence 0.7 to 0.9 matched the panel 22% to 38% of the time. Keep the spec's ordinal bands (section 7.4) and do not publish the weakest-link number as a probability.

## Facts checked on 2026-11-15 for the five debate points the brainstorm agent flagged as agreed without a checked reason

| Point | Claim in the refactoring plan | Check |
|---|---|---|
| C-017 | label-max merging occurs on 13 lines in 10 files plus `sc-auggie-review-protocol/SKILL.md:228` | Reproduced: a Grep for the plan's phrases finds those 14 lines. Two extra hits are unrelated (`sc-pr-submit-protocol/refs/severity-routing.md:65` is a category clamp). Holds. |
| A-006 | two readers split on every bare pipe, so a `\|` cell codec is unsafe | `card_convert.py:250` and `telemetry.py:162` read as `split("\|")`. Holds. |
| C-010 | `WORKER-CONTRACT.md:33` lists the keys, so each added key is a contract edit | Line 33 enumerates the top-level keys. Holds. |
| X-003 | no final gate reads a ledger today | `task/SKILL.md:290-292` and `tech-research/SKILL.md:415-419` read no ledger; neither file contains the words "follow-up ledger". Holds. |
| S-009 | the stage 3 entry condition needs the scored table for 0c | True at writing time; now out of date because the table exists (point 1 above). |

## Open decisions for the owner (unchanged from the spec)

Owner decisions OD1 to OD17 in section 15 of the spec still stand; the spec's own work order for the plan is its section 16. The ones this program touches: OD4 (classifier authority: none in version 1) and the Jev key and privacy decision (J1 and J2 in `02-brainstorm/jev-uses.md` section 8).
