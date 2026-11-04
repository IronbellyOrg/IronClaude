# Diff Analysis: reflect reviewer-card comparison

## Metadata
- Generated: 2026-11-04T18:40:00Z
- Variants compared: 3 (variant-1 = sonnet:analyzer, variant-2 = haiku(glm-5.3):qa, variant-3 = opus:refactorer)
- Subject under review: `.dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md` against `source.md`
- Calibrated C (Wave 3C): variant-1 0.75, variant-2 0.76, variant-3 0.75
- Total differences found: 16
- Categories: structural (2), content (4), contradictions (3), unique (6), shared assumptions (1)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Granularity | 4 findings (1 blocking) | 4 findings (0 blocking) + coverage_check line | 9 findings (1 blocking) | Medium |
| S-002 | Coverage evidence | none recorded in card | `coverage_check: 9/9 spans present` | none recorded in card | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Fix for the stale `.claude/skills/sc-issue-protocol/templates/summary.md` mirror | delete the gitignored mirror after `make sync-dev`, amend Constraints line 20, run `make verify-sync` (exit 0) | remove the mirror after the `mv`, record verify-sync output | run `make sync-dev`; remove the mirror **or report it** to the user | Medium |
| C-002 | Fix for `<scope>` double meaning | distinct placeholder (`<target>`) | (not raised) | define once (last segment) in SKILL.md and claim.md, or distinct placeholder | Low |
| C-003 | Depth of Task 3 test-design audit | none beyond R1-F4 (import) | traced helper semantics by hand; finds only chains.md:14 | four test-design findings (F1 helper, F2 empty scan, F3 fences, F7 `<REPORT.md`) | Medium |
| C-004 | Acceptance-criteria strength for the analysis-name rule | not raised | design-doc lines 168/249 unobservable by Task 4 grep (R2-F3); claim.md literal (R2-F2) | claim.md literal (R3-F5) | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Severity and class of the stale-mirror finding | "blocking" / grounding_gap (R1-F1) | "minor (gitignored, CI-safe)" / drift (R2-F1) | "minor" / necessary (R3-F8) | High |
| X-002 | Transient red between Task 2 and Task 3 | "this is not a defect" (card body, verified-adherent list) | not raised | minor drift (R3-F6) | Low |
| X-003 | Is the Task 3 negative test sound as specified? | sound except import (R1-F4) | "specified semantics pass post-fix" | old-path negative case can pass vacuously: blocking (R3-F1) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 3 | R3-F1: require a shared `old_summary_refs` helper so the negative test exercises the real check | Medium |
| U-002 | 3 | R3-F2: positive scan can pass with nothing scanned; assert the collected set is non-empty | Medium |
| U-003 | 3 | R3-F3: names inside fenced blocks are not scanned (chains.md:33 is fenced) | Low |
| U-004 | 2 | R2-F3: Task 4 grep cannot see the analysis-name edits at design-doc lines 168 and 249 | Medium |
| U-005 | 1 | R1-F3: SKILL.md:66 spawn line (pinned by `_SPAWN_PROMPT_LINE`) correctly left unchanged | Low |
| U-006 | 1 | R1-F4: red-evidence import may fail (refuted by calibrator: `tests/__init__.py`, `tests/skills/__init__.py` exist) | Low |

Agreements (no diff point): `<scope>` double meaning (R1-F2 = R3-F4); claim.md needs the exact literal (R2-F2 = R3-F5); chains.md:14 `<REPORT.md` needs a pinning probe case (R2-F4 = R3-F7); R3-F9 probe-source citation (no counter-position).

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Refreshing the project `.claude/` mirror is enough for workers to see the renamed files; all three cards treat the stale-copy problem as a `.claude/` (sync-dev) problem only. Unstated: the installed copy under `~/.claude/skills/sc-issue-protocol/` is refreshed by `superclaude install` only with `--force` (`src/superclaude/cli/install_skills.py:100-110` skips an existing skill without `--force`; with `--force` it runs `rmtree` then `copytree`, `src/superclaude/cli/install_skill.py:46-52`). | X-001 / C-001 | Medium (the coordinator's live run depends on the installed copy; outside this plan's write scope) | UNSTATED, promoted |

## Summary
- Total structural differences: 2
- Total content differences: 4
- Total contradictions: 3
- Total unique contributions: 6
- Total shared assumptions surfaced: 1 (UNSTATED: 1, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: X-001
- Taxonomy pre-tags: L3 (state/guard/boundary): X-001, X-003, U-001, U-002, A-001; L2 (structural): S-001, C-001, C-002, C-003, C-004, X-002, U-003, U-004; L1 (surface): S-002, U-005, U-006
