# Diff Analysis: reviewer-card comparison (P1 live plan, round 2)

## Metadata
- Generated: 2026-11-05
- Variants compared: 3 (V1 reviewer-1 analyzer, V2 reviewer-2 qa, V3 reviewer-3 refactorer); files `variant-N-original.md` in this folder
- Total differences found: 3 structural, 13 content, 3 contradictions, 6 unique, 4 shared assumptions
- Categories: structural (3), content (13), contradictions (3), unique (6), shared assumptions (4)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Findings table size | 12 rows | 7 rows | 8 rows | Low |
| S-002 | Regression stance | 1 Regression row | states "No Regression found" | 1 Regression row | Medium |
| S-003 | Advisory section | 2 correctness gaps | 2 flag-table mismatches | 2 gaps + a notes list | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 1 install line `cmp` of "every file under src/superclaude/commands/" includes README.md and __init__.py (installer excludes README.md) | Regression HIGH (#1) | absent | Regression HIGH (#1) | High |
| C-002 | Task 1 clean-tracked-tree check conflicts with the plan's own edit, APPROVED.md and the no-commit rule | Drift MEDIUM (#2) | absent | Drift MEDIUM (#3) | Medium |
| C-003 | Task 23 `find ... return-contract.yaml` can never be empty on a branch checkout; no pre-run baseline | Drift MEDIUM (#7) | absent | Drift MEDIUM (#2) | Medium |
| C-004 | Task 24 owner-instruction substitution (grant file replaced by a Constraints bullet) | Necessary LOW (#4) plus a separate Drift MEDIUM on word-for-word quoting (#3) | Necessary LOW (#1) | Drift LOW (#5, reason weak, collides with C-002) | Medium |
| C-005 | Stale "grant file" wording in Task 25 acceptance | Drift LOW (#5) | absent | Drift LOW (#6) | Low |
| C-006 | Task 24 child worktree created first, synced, no `--setup` | Necessary LOW | Necessary LOW | Necessary LOW | Low |
| C-007 | Tip pin replaced by branch-tip.txt plus ancestor check | Necessary LOW | Necessary LOW | Necessary LOW | Low |
| C-008 | D-P1-5 cited for "worker did not stage .dev/tasks" | Drift LOW (#12) | Drift LOW (#5) | absent | Low |
| C-009 | Task 19 (lc18) vs the brief's phase header (steps 3 and 4 replaced; step 6 empty) | absent | Necessary LOW (#4) | absent | Low |
| C-010 | Coverage-matrix omissions (seven spans of source.md without a row) | absent | Drift LOW (#6) | absent | Low |
| C-011 | Not-invoked check extended to guard cases 1 and 2 | Authorized (#11) | Authorized (in #7) | Authorized (#8) | Low |
| C-012 | Gate line and Section check added | Authorized (#10) | Authorized (in #7) | absent | Low |
| C-013 | Static report covers 7127c247, not the tested tip | Drift LOW (#8) | absent | absent | Low |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | Is there a Regression in the plan? | Yes: Task 1 install line (#1) | "No Regression found" | Yes: Task 1 install line (#1) | High |
| X-002 | Class of the grant-file swap (C-004) | Necessary (swap) + Drift (quoting) | Necessary | Drift (reason does not explain; forces the edit that collides with C-002) | Medium |
| X-003 | Severity of the clean-tree check (C-002) | MEDIUM Drift | not reported | MEDIUM Drift; V3 adds that the plan forbids commits so the check cannot be met | Low |

Evidence: V1 and V3 each cite `src/superclaude/cli/install_commands.py:11` (`_EXCLUDE_FILES = {"README.md"}`) and `:40` (`glob("*.md")`); V2's "No Regression found" paragraph states every command line matches source.md:51-79 and does not mention the install line.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | `--parent-worktree active` may resolve to the Orca UI's active worktree, not the coordinator's | Medium |
| U-002 | V1 | all live tasks depend only on Task 1; concurrent execution would pollute `check --run` and `pgrep` | Low |
| U-003 | V3 | `pgrep -af -- '--watch'` likely matches the Bash tool's own shell | Medium |
| U-004 | V3 | no rule to normalise the worker's `--report-path` against `<R>/return-contract.yaml` (trailing slash, absolute path) | Medium |
| U-005 | V3 | `install_skills.py:88-98` skips sc-* skills served by a same-named command; the skills `cmp` in Task 1 could fail | Medium |
| U-006 | V2 | lc13 and lc15 briefs differ from the WORKER-CONTRACT.md flag table (`--output-dir` / `--output`); spec 2.1 permits both | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The grounding hunks (tip `f0e307eb`, install state, spec lines) were current when each reviewer read them | all three cite G8/G9 | A stale hunk would change C-001 to C-003 | UNSTATED, promoted (state) |
| A-002 | The brief (`source.md`) is the authority when it differs from the plan, although the plan says the plan governs | all three audit plan against source.md | Decides whether C-004 and C-007 are Drift or Necessary | UNSTATED, promoted (invariant) |
| A-003 | Orca 1.4.245 accepts the same flags and selectors as the P0-era help | all three accept `--parent-worktree active` | Affects C-006 and U-001 | STATED (UNVERIFIED) |
| A-004 | Line numbers cited are post-edit (the plan gained one line at 17:26) | all three cite plan:NN | A one-line shift would misplace citations | UNSTATED, promoted (boundary) |

## Summary
- Total structural differences: 3
- Total content differences: 13
- Total contradictions: 3
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001
- Taxonomy tags: L1 surface: S-001, S-003, C-005; L2 structural: S-002, C-004, C-006, C-007, C-008..C-013, U-001, U-002, U-006, X-002; L3 state mechanics: C-001 (guard), C-002 (state), C-003 (boundary), X-001, X-003, U-003, U-004, U-005, A-001, A-002, A-004
