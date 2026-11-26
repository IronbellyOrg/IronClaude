# Diff Analysis: re-review cards of the regenerated plan (reflect UC-1, second run)

## Metadata

- Generated: 2026-11-26T18:40:00Z
- Variants compared: 3 (variant-1 = reviewer 1 analyzer/sonnet, 9 deviation rows; variant-2 = reviewer 2 qa/haiku, 1 deviation row plus a 26-id table; variant-3 = reviewer 3 refactorer/opus, 9 rows plus 1 advisory)
- Subject: the regenerated 38-task plan `TASK-WF-design-20261126-180705.md` against its design, and the 11 blocking findings (M-01 to M-11) of the first review. `PLAN` = the plan file, `DESIGN` = its `source.md`, `REQ` = merged requirements.
- Total diff points (S + C + X + A): 26 (structural 2, content 19, contradictions 3, shared assumptions 2); unique contributions U: 10 (not in the denominator)
- Taxonomy level in brackets: L1 surface, L2 structural, L3 state-mechanics. Variants were not blinded.
- Depth: quick (Round 1 only, no Round 2, no invariant probe); this is the re-review run, see `return-contract.yaml` for the deviation note.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 [L1] | Layout | prior-blocker table, prior-medium paragraph, Deviations table of 9 rows | prior-blocker table, one Deviations row, a 26-id disposition table | prior-blocker table, 9 rows, a separate advisory table | Low |
| S-002 [L2] | Grade vocabulary | grade in the cell text and a label column, consistent | one HIGH row graded Blocking (Decision) | rows graded Blocking/Medium/Note, label HIGH only on the Blocking row | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 [L3] | Task 28 says a reply carrying no key is never a resolution; the design (D:387, FR-122) says it counts when exactly one key was displayed (PLAN:326, 329, 386) | Medium (stricter than the design, fails closed, no override recorded) | Blocking (Decision): changes a required behavior and the acceptance checks of Tasks 28 and 34; marks M-10 regressed | not raised (calls M-10 resolved and cites PLAN:326, 329) | High (grade and existence differ) |
| C-002 [L2] | Task 19 rewrites `git.md` (a plugin twin exists) but the copy waits until Task 25, breaching the new Constraint on plugin twins (PLAN:34) | - | - | Blocking (Decision) | High |
| C-003 [L3] | Task 4's from-scratch child environment drops the config-isolation variables the fixtures use; with git-lfs in `/etc/gitconfig` `snapshot_lossless` is always false here; Task 5's acceptance asserts only the false case | - | - | Medium (could be Blocking with a positive-case test) | Medium |
| C-004 [L2] | Task 32 puts the base-commit comparison into the permanent test file; CI checks out at depth 1 and the base is recorded in a moving artifact | - | - | Medium | Medium |
| C-005 [L2] | The Constraint records the override of T-16 only for Task 32's `_ALLOW` entry; Tasks 26, 30, 31 edit scanned files with no permission | - | - | Medium | Medium |
| C-006 [L1] | Task 31's grep forbids `reason=index-locked` in `SKILL.md`, which also matches the `E-COMMIT-PRECONDITION reason=index-locked` stop of Task 26; same ambiguity in Task 34 | - | - | Medium | Medium |
| C-007 [L2] | The Constraint "tests written first in each task" cannot be followed in Tasks 19 to 23 and 26 to 33, whose static pins arrive at the end of the phase (PLAN:28, 284, 329, 339, 386) | Medium | - | - | Medium |
| C-008 [L2] | `validate_argv(argv)` cannot tell an argv printed for the agent from the runner's private-index call (PLAN:62, 65) | Medium | - | Note | Low |
| C-009 [L3] | Task 17's acceptance lacks FR-109 / T-19 cases (revocation, stale installed copy, changed plan, `git gc --prune=now`, unflagged then flagged, resumed batch, halt gives no commit) | Medium | - | - | Medium |
| C-010 [L3] | `record-skipped` is not tied to the flag: what an unflagged run does for a mixed or empty boundary is undefined (PLAN:158, 161, 216, 316) | Medium | - | - | Medium |
| C-011 [L2] | `version` is described as "the `--version` form, no other option"; the runner's argv shape for it is undefined and untested (PLAN:62, 83) | Medium | - | - | Low |
| C-012 [L2] | Task 13 cites "the `why` the design names" for the `.dev/implement/` skip, but the design names none (`source.md:228`, REQ:475) | Medium | - | - | Low |
| C-013 [L1] | Task 30's `git diff -- archive_workspace.py` is empty compares with the index, not the recorded base commit (PLAN:349) | Note | - | Note | Low |
| C-014 [L2] | The 15-line net growth budget of `SKILL.md` across Tasks 26 and 30 is tight with no fallback | Note | - | - | Low |
| C-015 [L1] | Task 9 says "nine line regexes of lines 44-67" while those lines hold eleven compiled patterns | - | - | Note | Low |
| C-016 [L2] | Checks that read `git ls-files` (banned-wording scan, plugin-twin check) see new files only after commit (open from first-run M-33) | - | - | Note | Low |
| C-017 [L3] | The commit feature cannot commit on machines with git-lfs installed (`snapshot_lossless` false for any `filter.*` entry) | - | - | Advisory correctness gap | Medium |
| C-018 [L3] | NFR-013 (every refusal reports whether HEAD, index and work tree changed) has no acceptance check (first-run M-27) | - | Real gap, carried forward, non-blocking | - | Low |
| C-019 [L1] | Disposition of the 26 design ids the plan text does not name | - | Full table: 17 inactive or historical, 8 covered, 1 gap | - | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|---|---|---|---|
| X-001 [L3] | M-10 status | V2: regressed (Task 28's no-key rule contradicts the design) | V1 and V3: resolved (V1 raises the same rule as a Medium row) | High |
| X-002 [L3] | Grade of the Task 28 rule | V1: Medium | V2: Blocking | High: decides the blocking count |
| X-003 [L2] | Grade of the `validate_argv` interface | V1: Medium | V3: Note | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 3 | Task 19 plugin twin (C-002) | High |
| U-002 | 3 | Task 4 environment and git-lfs (C-003, C-017) | High |
| U-003 | 3 | Task 32 test fixture vs CI depth (C-004) | Medium |
| U-004 | 3 | Constraint override scope (C-005) | Medium |
| U-005 | 3 | Task 31 grep ambiguity (C-006) | Medium |
| U-006 | 1 | Test-first Constraint contradiction (C-007) | Medium |
| U-007 | 1 | Task 17 missing cases (C-009) | Medium |
| U-008 | 1 | `record-skipped` and the flag (C-010) | Medium |
| U-009 | 2 | Task 28 no-key rule against the design (C-001) | High |
| U-010 | 2 | 26-id disposition (C-019) | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 [L3] | All cards grade rows with the review severity rule | A finding the review grades Blocking is one that would halt or mislead `/sc:implement`; the cards check implement's own halt model (`refs/qa.md`) only for quoted Constraints | UNSTATED | Yes |
| A-002 [L3] | V1 and V3 read existing tests and the real machine | The plan's acceptance universe includes every existing test and the facts of this machine (git-lfs in `/etc/gitconfig`, CI depth), not only what the plan names | UNSTATED | Yes |

## Summary

- Total structural differences: 2; content: 19; contradictions: 3; shared assumptions surfaced: 2 (UNSTATED 2, STATED 0, CONTRADICTED 0); unique contributions: 10.
- Highest-severity items: C-001, C-002, X-001, X-002.
