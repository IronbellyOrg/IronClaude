# Refactoring Plan (merge of three reviewer cards into one verdict)

## Overview

- Base: card 1 (`variant-1-original.md`). Incorporated: card 2 (`variant-2-original.md`), card 3 (`variant-3-original.md`), the debate (`r1-advocate-*.md`, `r2-advocate-*.md`) and the invariant probe (`invariant-probe.md`).
- Output: `../merged-verdict.yaml` (the merged findings with final grades) and `merge-log.md`.
- Grade rule applied to every finding: Blocking only when correcting it changes a decision, a required behaviour or an acceptance check the plan rests on (Decision), a required item is absent in substance (Missing), or following the plan would lose or expose data or a key, or break a safety boundary or the spend cap (Safety). A real weakness nothing rests on is Medium. Wording is Note. A fixable sentence or check is not Decision.
- Evidence for every merged finding is copied from the card or probe that raised it (file:line as written there). Do not invent a citation.

## Planned Changes

1. C-001 (card 1 F-5 Medium; card 2 F-4 and card 3 F-2 Blocking Missing). Final: Blocking, Missing. Claim: the whole-run spend estimate before the first request has no task, and Gate 2's spend bound has no inputs. Use card 3's pointer to `Budget.reserve_phase` (budget.py:63-70) and add the probe's INV-006: release the reservation in a `finally` with `release_phase` (budget.py:98-100).
2. C-008 with INV-001 and INV-013 (card 1 F-8 Medium; debate: Blocking, Decision, three of three). Final: Blocking, Decision. Claim: the plan's Gate 1 refuses any `UNSET` value, stricter than the design (source.md:72), so table answers wait on fields the table never uses; and the fix interacts with the rule-file hash, because filling the fields later changes a frozen hash. Say that a decision is needed: keep the stricter Gate 1 and define a re-freeze, or drop `UNSET` from Gate 1 and keep it in the scorer and Gate 2.
3. C-002 (card 1 F-3 Medium; cards 2 and 3 Blocking Decision; debate: Medium). Final: Medium. Claim: the stop signals are returned results, not exceptions (`refused`/`budget_exhausted`, `invalid`/`model_mismatch`, `refused`/`dry_run`), and the rule "rerun on any non-ok status" would rerun them; plan:125 already requires the stops, so the defect is the sentence at plan:119. Keep the probe's INV-004 as a sub-point: every non-ok result has `model=None`, so the model-pin check must not treat a timeout as a wrong model.
4. C-003 (Medium). Claim: plan:119 says the runner refuses without `--live` and also runs a dry run without it; the plan documents why `live=False` is used (plan:30); state one dry-run rule and whether it checks the gates.
5. C-004 (card 1 Medium, card 2 Blocking, card 3 Note; debate: Note). Final: Note. Imports must come from jevlib submodules; add `KeyMissing` and `KeyRejected` to the list.
6. C-005 (card 1 Blocking; card 3 Medium; debate: Medium). Final: Medium. Grep for the cue words, not "keyword"; exempt the option names `build` and `deployment`; add the probe's INV-007 (a strict cue grep can bias the Jev wording).
7. C-006 (cards 1 and 3 Blocking; debate: Medium). Final: Medium. The Task 8 `git status` check cannot pass as written; compare to a baseline.
8. C-007 (card 1 Medium; card 3 Blocking Missing; debate: Medium). Final: Medium. No `gate.py` command for the manifest or freeze events; `tests_passed` carries one hash while Gate 2 checks several; the table-answers hash does not exist at Gate 1. Use card 3's detail.
9. C-009 (card 3 Medium). Final: Medium. `run-record.md`, `report.md` and `decision-record.md` placement and authorship.
10. C-010 (card 3 Blocking Missing; debate: Medium). Final: Medium. README "how to rescore" missing.
11. C-011 (card 1 Medium). Final: Medium. The pull-request body wording (`Refs #611`, B to E left) has no home.
12. C-014 (card 1 Medium). Final: Medium. `jev_answer` band mapping is undefined, so T-05 has no expected values.
13. C-013 (card 3 Medium; debate: Note). Final: Note. Prefer `loader.sha256_file`; reuse of `Journal` was withdrawn.
14. C-015 (card 1 Note). Final: Note. Cue rows are SKILL.md lines 153 to 158 and the ambiguity rule is line 159.
15. Probe additions, graded by the rule: INV-002 Medium (nothing in the gates refuses a second live run or a reused `lead_go`, though the agreed rule forbids a rerun of the whole run); INV-003 Medium (tests could append to the real `events.jsonl` or ledger; require temporary paths); INV-005 Medium (the cap ceiling comes from jevlib's price constant, and no task feeds a re-confirmed price into it); INV-009 Medium (T-10 scans only the run folder; `events.jsonl`, the ledger and the manifest are unscanned); INV-010 Note (empty-list statistics; "the jevlib files" undefined; `__pycache__` hashing); INV-011 Note (the stubbed environment accessor does not see `privacy_violation`'s direct read).
16. Dropped as not defects: C-012 (Task 4 takes `run_meta` and tests on synthetic inputs, so order is not a defect; only the `score` command's reading of Task 5's events remains, folded into C-007), C-016, INV-008 (a grading-consistency remark about the review itself) and INV-012 (addressed).

## Changes NOT Being Made

| Item | Why |
|---|---|
| Card 2's Blocking grades on C-002, C-003, C-004, C-009 | Conceded in Round 2: plan:125 already requires the stops, the import fix is wording, and a stated departure is not a Blocking defect |
| Card 3's Blocking grades on C-007 and C-010 | Conceded in Round 2: plan:103 supplies a manifest writer; README gap is a fixable sentence |
| Card 1's Blocking grades on C-005 and C-006 | Fixable checks, not decisions |

## Review Status

Auto-approved (non-interactive). Convergence on the 28 diff points: 28 of 28 resolved after Round 2 (100%). Invariant gate: BLOCKED (4 HIGH unaddressed, INV-001, INV-002, INV-003, INV-013); at standard depth there is no Round 3, so they are carried into the merged verdict as findings and the contract status is partial.
