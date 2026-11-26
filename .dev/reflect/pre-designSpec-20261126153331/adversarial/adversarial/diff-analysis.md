# Diff Analysis: three reviewer cards on the same plan

## Metadata

- Mode A, 3 variants: `variant-1-original.md` (reviewer 1, lens analyzer, sonnet), `variant-2-original.md` (reviewer 2, lens qa, haiku), `variant-3-original.md` (reviewer 3, lens refactorer, opus). Each is a card of findings about one plan (`.dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md`, cited as "plan") against its spec (`source.md`, same folder; its "Revision 1" section wins over sections 3 to 8).
- Calibrated confidence C of the cards: see the `-calibration.yaml` files in `reviewer-cards/` (reviewer 2: 0.82, reviewer 3: 0.89; reviewer 1 as recorded there).
- Grade rule used by the reviewers: Blocking only when correcting it changes a decision, a required behaviour or acceptance check the plan rests on (Decision), a required item is absent in substance (Missing), or following the plan loses data, exposes a key or breaks the spend cap (Safety). Medium is a real weakness nothing rests on. Note is wording only.

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Size and focus | 8 findings, 2 Blocking | 4 findings, all Blocking | 6 findings, 3 Blocking | Low |
| S-002 | Does Medium and Note carry a `blocking_reason` field | yes (null) | no | yes (null) | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 6 requires exactly one post for every systemic stop, but `KeyMissing` is raised before transport and `refused`/`budget_exhausted` is returned before transport (client.py:114-117, 133-135); after the whole-run reservation a draw cannot run short (budget.py:72-78) (plan:165, 152) | clean (found the stop classes correct) | F-1 Blocking (Decision) | F-1 Blocking (Decision) | High |
| C-002 | The `jev-rows.jsonl` and `run-record.md` formats are defined in Task 6 but consumed by Task 5, which does not depend on it; no test scores rows written by `execute` (plan:123, 125, 129, 138, 155, 156) | none | none | F-2 Blocking (Decision) | Medium |
| C-003 | Gate 2's `spend_bound` needs the frozen prompts but gates never call the corpus loader; no stated input; the ledger cannot be read without `Budget.__init__` rewriting it (plan:106, 108, 115) | F-3 Medium | none | F-3 Blocking (Decision) | High |
| C-004 | A zero-post `run_end` (spend refusal, missing key) uses up the go through Gate 2's `prior_run`; an unset `TYPESAFE_API_KEY` is unspecified (plan:106, 152, 156, 159) | F-4 Medium | none | F-4 Medium | Medium |
| C-005 | The human reading of the six definitions before the freeze (source.md:142, M-5) has no task, README step or check | F-1 Blocking (Missing) | F-4 Blocking (Missing) | none | Medium |
| C-006 | Only `freeze-corpus` refuses an existing manifest key; `freeze-table` and `freeze-rule` do not, and no test covers it (plan:101 to 115; source.md:144) | none | F-2 Blocking (Missing) | none | Medium |
| C-007 | The real-state fixture records only the metadata of `runs/` itself, so an edit of an existing nested file need not be seen (plan:41 to 46; source.md:150) | none | F-3 Blocking (Decision) | none | Medium |
| C-008 | The T-06 check for a twice-failed prompt does not say the label is `ambiguous` or `none-fit`, where an unset answer would count as right (plan:77, 127, 138) | F-2 Blocking (Decision) | none | none | Medium |
| C-009 | `sign_test_passes(b, c)` has no rule parameter, so the factor 20 from `alpha_inverse` cannot be read; the reference-loop check cannot fail if it is the same formula (plan:79, 85) | F-5 Medium | none | F-6 Note | Low |
| C-010 | "Answered" is not defined, so the T-08 median population cannot be pinned (plan:26, 81) | F-6 Medium | none | none | Medium |
| C-011 | The `exp` fixture does not say it supplies code files and a `jevlib` folder, so `hash_code` has no inputs (plan:59, 94, 105, 112) | F-7 Medium | none | none | Medium |
| C-012 | Notes: "31 importers" does not match a count; the `ok`-rows model check cannot fail; `load_rule` does not say it converts numbers (plan:129, 173) | F-8 Note | none | F-5 Note | Low |

## Contradictions (same defect, different grade, or opposite readings)

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Grade of C-003 | Medium | none | Blocking (Decision) | High |
| X-002 | Grade of C-005 | Blocking (Missing) | Blocking (Missing) | none (hash and cue list found clean) | Medium |
| X-003 | Grade of C-009 | Medium | none | Note | Low |
| X-004 | Whether C-001 is a defect: V1 found the stop classes correct but did not read the post count | clean | Blocking | Blocking | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V3 | C-002: row and run-record format ordering, plus a test that scores rows from `execute` | High |
| U-002 | V2 | C-006 write-once for all three freeze commands, and C-007 descendant coverage of the real-state fixture | Medium |
| U-003 | V1 | C-008, C-010, C-011 test-surface gaps | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The spec's "Revision 1" section is the authority wherever the plan and the earlier design sections differ | all three | Medium | UNSTATED, promoted |
| A-002 | `jevlib` is correct and unchanged, so every claim about its behaviour is a fixed fact | all three | Low | UNSTATED, promoted |
| A-003 | The Blocking test (Decision, Missing, Safety) is applied the same way by each reviewer; the calibrators flagged several Blocking grades as over-graded | all three | High | UNSTATED, promoted |

## Summary

- Total structural differences: 2
- Total content differences: 12
- Total contradictions: 4
- Total unique contributions: 3
- Total shared assumptions surfaced: 3 (UNSTATED: 3)
- Highest-severity items: C-001, C-003, X-001, X-004, A-003
- Diff points counted for convergence: 21 (structural 2, content 12, contradictions 4, shared assumptions 3)
- Taxonomy tags: L1 surface: S-001, S-002, C-012, X-003. L2 structural: C-002, C-005, C-006, C-007, C-008, C-009, C-010, C-011, A-001, A-002. L3 state mechanics: C-001, C-003, C-004, X-001, X-004, A-003.
- Similarity check: not triggered; the cards differ in what they raise and in how they grade it.
