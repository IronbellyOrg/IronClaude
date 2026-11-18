# Diff Analysis: reviewer-card comparison (plan vs spec, pr-submit merge guard)

## Metadata
- Generated: 2026-11-13
- Variants compared: 3 (variant-1 = reviewer-1 analyzer/sonnet class; variant-2 = reviewer-2 qa/haiku class; variant-3 = reviewer-3 refactorer/opus class)
- Total differences found: 1 structural, 7 content, 3 contradictions, 7 unique, 3 shared assumptions
- Debate denominator (S + C + X + A): 14

Variant paths: variant-1-original.md, variant-2-original.md, variant-3-original.md in this folder. Each is a full reviewer card (verdict, prose findings, findings-v2 block). "Plan" is TASK-WF-designSpec-20261107-075614.md, "spec" is source.md, both under .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Card layout and extras | Verdict, prose, "Checked and found fine" list, block (9 findings) | Verdict, prose with a T1 cross-check paragraph that rejects two T1 findings, block (6 findings) | Verdict, prose, "Checked with no defect found" list, block (10 findings) | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Task 7: static scan "every gh line carries --repo or repos/" vs the `_RESOLUTION_SCRIPTS` tests (T1 F1) | MAJOR, blocking; also notes `command -v gh` lines | MAJOR, blocking; notes spec line 377 repeats the wording | MAJOR, blocking; names `_repo_scoped` as the fix | Low (all agree) |
| C-002 | `resume_decision` row 4 cannot call `release_decision` (missing cycle_id, applied_edits, target_sha; no re-enter action) (T1 F2) | MAJOR, blocking | MAJOR, blocking | MAJOR, NOT blocking; cites later code that added the three arguments | Medium (blocking flag differs) |
| C-003 | Halt `draft_guard_unavailable` reports `released` when no guard record exists (T1 F3) | MAJOR, NOT blocking | MAJOR, blocking | MAJOR, NOT blocking | Medium (blocking flag differs) |
| C-004 | Fold row for `user_override` sets no `disabled_cause` (T1 F4) | MINOR | MINOR (adds: settle, fold, status test) | MINOR | Low |
| C-005 | Task 1 baseline taken before `make sync-dev`, Task 13 subtracts it (T1 F5) | MINOR, confirmed | Not adopted ("stale-environment premise unverified") | MINOR, confirmed | Medium |
| C-006 | Script JSON keys vs `GuardRead` field names, nobody owns the mapping (T1 F6) | MINOR, confirmed | Not adopted (protocol read/decide steps can convert) | MINOR, confirmed | Medium |
| C-007 | Wave 0 bullet must name L3 and `draft`, but its test must reject L3 or `draft` wording (T1 F7) | MINOR | Not raised | MAJOR (widened: criterion cannot pass as written) | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | Is the T1 F5 baseline gap (Task 1 before sync-dev) a real defect? | Yes, MINOR (variant-1 F5) | No: "premise unverified here"; Task 13 re-runs sync checks | Yes, MINOR (variant-3 F5), notes the two sync tests narrow but do not close it | Medium |
| X-002 | Is the missing JSON-to-`GuardRead` conversion (T1 F6) a defect? | Yes, MINOR (variant-1 F6) | No: "different field names alone do not prove an uncovered requirement" | Yes, MINOR (variant-3 F6) | Medium |
| X-003 | Which findings are blocking (F2 and F3 of each card; F7 severity)? | F2 blocking, F3 not, F7 MINOR | F2 and F3 blocking, F7 absent | F2 and F3 not blocking, F7 MAJOR | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | F8: resume row 3 check order (mismatching live state with observed == run_toggles+1 settles `not_applied`; unreadable-timeline reason unstated) | Medium |
| U-002 | 1 | F9: claims Task 5's pytest line over-claims `_NEW_KEY_DEFAULTS` coverage across three files (cites plan:175) | Low (needs checking against plan line 88) |
| U-003 | 2 | F5: no criterion checks the guard-event producer payload (key format, `:a<k>` retries, first-request fields) | Medium |
| U-004 | 2 | F6: the 66-row inferred matrix omits event payload, corrupt-line, one-retry, dependency-declaration units | Low |
| U-005 | 3 | F8: no fold row sets `cycle_id`, engage row 7 NOOPs on a held guard, so a later cycle runs under the earlier id and resume row 4 can release unpushed fixes | High |
| U-006 | 3 | F9: byte-identical checks of pinned sentences use only the literal start text | Low |
| U-007 | 3 | F10: classification steps name only `gh pr` / `gh api`, but `WRITE_VERB_RE` also hits git write verbs and keys multi-verb lines as `a+b` | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | The repo working tree (which already holds the later implementation) shows the same facts as the base commit for names, tests and helpers the plan relies on | All three cite HEAD test and script lines (e.g. test_static_grep.py:545-550) | UNSTATED (the brief's prompt says so, the cards do not) | Medium | Promoted |
| A-002 | A defect copied from the spec into the plan is still a plan-level defect to report | F1 (spec line 377), F2, F3 all trace to the spec | UNSTATED | Low | Promoted |
| A-003 | The plan is built literally, criterion by criterion, with no reconciliation against the tests it names | Needed for F1 and F7 to be defects | STATED in part (variant-2 verdict) | Medium | Not promoted |

## Summary
- Structural: 1; content: 7; contradictions: 3; unique: 7; shared assumptions promoted: 2 (of 3)
- Highest-severity items: U-005
- Taxonomy tags (debate points): S-001 L2; C-001 L2; C-002 L3; C-003 L3; C-004 L3; C-005 L2; C-006 L2; C-007 L2; X-001 L2; X-002 L2; X-003 L3; A-001 L2; A-002 L1; A-003 L3
