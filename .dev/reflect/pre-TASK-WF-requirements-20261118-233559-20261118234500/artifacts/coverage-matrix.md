# Coverage matrix (UC-1, Tier 1 card)

Spec: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261118-233559/source.md
Tasklist: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261118-233559/TASK-WF-requirements-20261118-233559.md

## Pass 1 (parsed rows, source.md table lines 27-49)

| Row | Source line | Mapped task(s) | Match |
|---|---|---|---|
| R1 central config in Coder template | source.md:27 | T9 (reads it), T19 (hands over content) | covered (Coder part is handoff only, by design) |
| R2 gh api user | source.md:28 | T11 | covered |
| R3 Project looked up per repo | source.md:29 | T11 | covered |
| R4 approvers + maintainers | source.md:30 | T11 | covered |
| R5 one entry point, per-project instances | source.md:31 | T15, T16, T17 | covered |
| R12 explicit state_dir | source.md:32 | T11 | covered |
| R13 thread repo through github.py / launch.py | source.md:33 | T7, T8 | covered |
| R14 pre-child checks | source.md:34 | T16 | covered |
| R15 failed orca list is an error | source.md:35 | T10, T15 | covered |
| R6 cron scheduler | source.md:36 | T19 | covered (Coder part is handoff only) |
| R16 one cron entry, one dispatcher | source.md:37 | T15, T17, T19 | covered |
| R7 three first-time commands automatic | source.md:38 | T13 | covered |
| R8 sweep lists Orca repos, writes configs | source.md:39 | T10, T11, T15 | covered |
| R9 coordinator branch/worktree/session | source.md:40 | T16 (check only), T19 | covered as handoff; IronClaude side only checks |
| R10 Coordinator worktree is the watcher worktree | source.md:41 | T11, T16, T19 | covered |
| R11 labels exist | source.md:42 | T12, T16 | covered |
| R17 duties from launch prompt | source.md:43 | T6, T19 | covered |
| R18 enabled true after first-run check | source.md:44 | T13 | covered (see conflict C1) |
| R19 approval record automatic | source.md:45 | T4, T6 | covered |
| R22 Status allow-list | source.md:46 | T1, T2 | covered |
| R23 per-status commands + Pipeline field | source.md:47 | T3, T4, T5, T6 | covered |
| R20 use existing remote branch (verify) | source.md:48 | T19 (records the question only) | WEAK: source says "must be verified"; no task verifies |
| R21 cron environment tests (open) | source.md:49 | T19 (gh auth status under env -i) | covered |

Parsed: 23 rows, 22 covered, 1 weak (R20). coverage_pct = 22/23 = 0.957.

## Pass 2 (inferred rows, each with a verbatim quote)

| Id | Quote | Citation | Match |
|---|---|---|---|
| INF-001 | "must be done once before the first real cycle; the sprint decides which of them can be automated and which stay an owner check." | source.md:62 | UNMAPPED: T13 automates config check, init-state and dry-run only; the lock test, restart test and live-test record are neither automated nor assigned to the owner in any task |

inferred_count 1 <= parsed_count 23, so no parse-density degrade.
coverage_pct_union = 22/24 = 0.917. unmapped_requirements_union = [R20, INF-001].

## Spec-internal conflict (not a coverage row)

C1: source.md:60 says "Switching the watcher on is the owner's decision (`enabled`), kept separate from creating the configuration." R18 (source.md:44) says a generated config is created with `enabled: true` after an automatic first-run check, and the plan (Task 13) follows R18. The later decision (R18, owner 2026-11-18, "every manual thing should be automatic") wins, but the stale line 60 still says the opposite.

## Ordering observation

Task 18 (documents per-status commands and the Pipeline field) depends only on Task 17. Task 4 and Task 6 are not in Task 17's dependency chain, so nothing forces them to land before the docs are written.
