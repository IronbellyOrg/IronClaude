# Diff Analysis: three reviewer cards on the same plan

## Metadata

- Mode A, 3 variants: `variant-1-original.md` (reviewer 1, lens analyzer), `variant-2-original.md` (reviewer 2, lens qa), `variant-3-original.md` (reviewer 3, lens refactorer). Each is a card of findings about one plan (`.dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md`, cited as "plan") against its spec (`source.md`, same folder).
- Calibrated confidence C of the cards: 0.77, 0.79, 0.82. All cited lines were confirmed by the calibrators (32, 10 and 43 citations; none unfounded).
- Points counted for convergence: structural 2, content 16, contradictions 6, shared assumptions 4 = 28.
- Grade rule used by the reviewers: Blocking only when correcting it changes a decision, a required behaviour or acceptance check the plan rests on (Decision), a required item is absent in substance (Missing), or following the plan loses data, exposes a key or breaks the spend cap (Safety). Medium is a real weakness nothing rests on. Note is wording only.

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Size and focus | 10 findings, 2 Blocking | 4 findings, all Blocking, all about Task 6 | 11 findings, 5 Blocking | Low |
| S-002 | Does every Blocking carry a reason, and do Medium and Note carry one | Reason on Blocking only | Reason on Blocking only | `blocking_reason` field on every finding (null on Medium and Note) | Low |

## Content Differences

Each row is one topic. Cards that raise it, with their grade, are shown.

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | The whole-run spend estimate that the design wants before the first request (source.md:82) has no task; Gate 2's "per-request spend bound" has no stated inputs (plan:103,119,124) | F-5 Medium | F-4 Blocking (Missing) | F-2 Blocking (Missing), cites `Budget.reserve_phase` (budget.py:63-70) | High |
| C-002 | Task 6 says `BudgetExhausted` stops the run and any non-ok status gets one rerun, but `ask` catches that exception and returns `refused`/`budget_exhausted` (client.py:114-117); `model_mismatch` returns `invalid` (validate.py:32-33); a dry run returns `refused`/`dry_run` (client.py:127-131); so the stop signals are results, and refusals would be rerun (plan:119) | F-3 Medium | F-2 Blocking (Decision) | F-1 Blocking (Decision) | High |
| C-003 | Task 6 says the CLI refuses to start without `--live` and also runs a dry run without `--live`; whether a dry run needs the gates is not stated (plan:119) | F-4 Medium | F-3 Blocking: the design wants a dry run against the mock transport (source.md:82), and the plan's `live=False` yields only `dry_run` refusals | F-10 Medium | Medium |
| C-004 | Task 6 says the runner imports names "from `jevlib`", but the package exports only MODEL, API_URL, KEY_ENV (jevlib/__init__.py:5); `KeyMissing` and `KeyRejected` are not in the list (plan:117) | in F-3, Medium | F-1 Blocking (Decision) | F-11 Note | Low |
| C-005 | Task 1's check `grep -n "keyword" questions.py` cannot detect the cue words it names (plan:47); the required type names `build` and `deployment` themselves contain cues (SKILL.md:154,156) | F-1 Blocking (Decision) | none | F-8 Medium | Medium |
| C-006 | Task 8's check that `git status --short` shows changes only under the experiment folder "and the package folder" cannot pass: other untracked work folders exist (plan:159) | F-2 Blocking (Decision) | none | F-5 Blocking (Decision) | Medium |
| C-007 | No `gate.py` command writes the manifest or runs the gates; no command records `owner_input_received`, `freeze`, `rule_freeze`; `tests_passed` carries one hash but Gate 2 checks several; the manifest holds the table-answers hash, which does not exist at Gate 1 (plan:101-103,156) | F-6 Medium | none | F-3 Blocking (Missing) | High |
| C-008 | The plan's Gate 1 refuses any `UNSET` value, but the design ties `UNSET` only to the scorer (source.md:70,72), so Gate 1 cannot pass and the table answers are blocked on items that do not affect the table (plan:61,103) | F-8 Medium | none | none | Medium |
| C-009 | `runs/<run-id>/run-record.md` is in the design (source.md:42) but no task creates it; `report.md` is at the experiment root in the design and under `runs/<run-id>/` in Task 4; `decision-record.md` is scorer-made in the design and a hand template in Task 8 (source.md:44) | none | none | F-9 Medium | Medium |
| C-010 | README's job "how to rescore" (source.md:34) is missing from Task 8's README contents and acceptance criteria | none | none | F-4 Blocking (Missing) | Medium |
| C-011 | The design says the story's pull request "must say `Refs #611` and list B to E as left" (source.md:104); no task covers it | F-9 Medium | none | coverage note only | Low |
| C-012 | Task order: Task 4's verdict needs the manifest and events formats that Task 5 builds; Task 5 depends on Task 4 only to hash a file (plan:82,84,97) | none | none | F-6 Medium | Medium |
| C-013 | `events.py` and `gate.py` compute SHA-256 without using the loader's helper (source.md:68), and `events.py` rebuilds an append writer that `jevlib.Journal` provides (journal.py:16-33) | none | none | F-7 Medium | Low |
| C-014 | `jev_answer` is described by operators only; which band side gives a type, `none-fit` or `not-settled` is not said, so T-05 has no expected values (plan:71,76; source.md:77) | F-7 Medium | none | none | Medium |
| C-015 | The plan cites the cue rows as SKILL.md "lines 152 to 159"; the rows are 153-158 (plan:137,141) | F-10 Note | none | none | Low |
| C-016 | The 'Reuse by import', 'nothing under src' and 'no prompt sent' requirements have no task by word overlap but are in the Constraints (plan:19,21) | acknowledged | acknowledged | acknowledged | Low |

## Contradictions (same defect, different grade, or opposite readings)

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Grade of C-001 | Medium | Blocking (Missing) | Blocking (Missing) | High |
| X-002 | Grade of C-002 | Medium | Blocking (Decision) | Blocking (Decision) | High |
| X-003 | Whether C-003 is a plan defect against the design or a documented departure (plan:30 says why `live=False` is used) | Medium, state the rule | Blocking, restore mock-backed dry run | Medium, state one rule | Medium |
| X-004 | Grade of C-004 | Medium | Blocking (Decision) | Note | Low |
| X-005 | Grade of C-005 | Blocking (Decision) | none | Medium | Medium |
| X-006 | Grade of C-007 | Medium | none | Blocking (Missing) | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | C-008: Gate 1 refuses `UNSET`, stricter than the design, blocking table answers | High |
| U-002 | V1 | C-014: band mapping undefined so T-05 has no expected values | Medium |
| U-003 | V3 | C-010: README "how to rescore" missing | Medium |
| U-004 | V3 | C-012: task order inverted between Tasks 4 and 5 | Medium |
| U-005 | V3 | C-009 (run-record, report and decision-record placement) and C-013 (reuse of Journal and the loader's hashing) | Medium |
| U-006 | V1 | C-015 and C-006's wording of the Task 8 check as "cannot pass" with evidence of other untracked folders | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The design (source.md) is the authority wherever the plan departs from it, even where the plan states a reason for the departure (plan:30 for `live=False`) | V2 and V3 treat the departure as a defect without weighing the stated reason | High | UNSTATED, promoted |
| A-002 | An implementer reads Task 6 literally, for example "imports from `jevlib`" means `from jevlib import ...` and "stops the run" means catching an exception | C-002 and C-004 rest on this | Medium | UNSTATED, promoted |
| A-003 | The Blocking test (Decision, Missing, Safety) is applied the same way by each reviewer; the calibrators found several Blocking grades that were fixable wording or check defects | all three cards | High | UNSTATED, promoted |
| A-004 | `jevlib` is correct and unchanged, so every claim about its behaviour is a fixed fact (client.py, budget.py, validate.py) | all three | Low | UNSTATED, promoted |

## Summary

- Total structural differences: 2
- Total content differences: 16
- Total contradictions: 6
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 4)
- Highest-severity items: C-001, C-002, C-007, X-001, X-002, X-006, A-001, A-003
- Diff points counted for convergence: 28
- Taxonomy tags: L1 surface: S-001, S-002, C-015, X-004. L2 structural: C-003, C-004, C-005, C-006, C-009 to C-014, C-016, X-003, X-005, A-001, A-002, A-004. L3 state mechanics: C-001, C-002, C-007, C-008, X-001, X-002, X-006, A-003.
- Similarity check: not triggered; the cards differ in what they raise and in how they grade it.
