| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "Refactor IronClaude to Orca's default worktree paths" | source.md:1 | containment, Task 1 (0.8571) |
| INF-002 | "replace the .dev/worktrees rule in CLAUDE.md" | source.md:1 | containment, Task 3 (1.0) |
| INF-003 | "every tracked file that encodes .dev/worktrees or git worktree add (git grep -E '\.dev/worktrees\|git worktree add' -- ':!.dev')" | source.md:1 | containment, Task 3 (0.7) |
| INF-004 | "Classify each hit as project worktree (move to Orca-created worktrees at Orca's default location) or internal temporary checkout used by a CLI or test (keep working without Orca)." | source.md:1 | containment, Task 1 (0.8421) |
| INF-005 | "project worktree (move to Orca-created worktrees at Orca's default location)" | source.md:1 | containment, Task 1 (0.8889) |
| INF-006 | "internal temporary checkout used by a CLI or test (keep working without Orca)" | source.md:1 | containment, Task 1 (0.7778) |
| INF-007 | "Also tighten the CLAUDE.md rule: SuperClaude upstream is never pushed to or interacted with." | source.md:1 | containment, Task 4 (0.9) |
| INF-008 | "Source of truth is src/superclaude" | source.md:1 | containment, Task 6 (1.0) |
| INF-009 | "run make sync-dev" | source.md:1 | containment, Task 7 (1.0) |
| INF-010 | "never stage .claude mirrors" | source.md:1 | none lexically (best Task 4, 0.5); content-level COVERED: plan lines 21, 160, 179 |
| INF-011 | "This revision supersedes plan .dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md" | source.md:1 | none lexically (best Task 1, 0.4545); content-level COVERED: plan line 19 |
| INF-012 | "must resolve all 14 deviations in its advisory reflect report .dev/reflect/pre-refactorIronClau-20261102175540/REPORT.md" | source.md:1 | none lexically (best Task 1, 0.2727); content-level COVERED: every D-id named across Tasks 1-8 and Constraints line 24 |
| INF-013 | "Owner decision (2026-11-02): rewrite scripts/eval_runner.py so it creates its master checkout in a temporary directory and removes it when done, making it an internal temporary checkout that works without Orca." | source.md:1 | containment, Task 2 (0.7727) |
| INF-014 | "Owner decision: keep POST-REFLECT-TASK.md unchanged as a third class, Historical record." | source.md:1 | containment, Task 1 (0.75) |
| INF-015 | "D-001 scripts/eval_runner.py:138-147 list-argument git worktree add, never removed, invisible to the spec grep (apply the owner decision" | source.md:1 | containment, Task 2 (0.8095) |
| INF-016 | "add a list-argument search to the inventory and the final residual check" | source.md:1 | none lexically (best Task 2, 0.5); content-level COVERED: plan lines 20, 35, 172, 177 |
| INF-017 | "D-002 Task 3 must name and rewrite CLAUDE.md pre-PR check 1 (bare gh repo view, CLAUDE.md:64)" | source.md:1 | containment, Task 4 (0.9412) |
| INF-018 | "check 3 (close it immediately, CLAUDE.md:66) so the agent stops and reports and the user closes a misrouted PR" | source.md:1 | containment, Task 4 (0.7143) |
| INF-019 | "must list the allowed forms for gh commands that take a positional repo" | source.md:1 | containment, Task 4 (1.0) |
| INF-020 | "D-003 nine list-argument worktree add lines (8 plus eval_runner.py:143) need their own search total" | source.md:1 | containment, Task 1 (0.6316) |
| INF-021 | "a class per file without breaking the count check" | source.md:1 | containment, Task 1 (0.6667) |
| INF-022 | "D-004 the repository has only an origin remote, so word the upstream rule without depending on a remote named upstream" | source.md:1 | containment, Task 4 (0.8182) |
| INF-023 | "record the source of Orca's project id as unverified" | source.md:1 | containment, Task 4 (0.8571) |
| INF-024 | "D-005 narrow 'no tool call or link' to tool calls and gh or Orca link flags" | source.md:1 | containment, Task 4 (0.8) |
| INF-025 | "state that static references in docs and test fixtures are out of scope" | source.md:1 | containment, Task 4 (0.875) |
| INF-026 | "decide the CLAUDE.md:251 issue link explicitly" | source.md:1 | containment, Task 4 (0.8571) |
| INF-027 | "D-006 note in the inventory that POST-REFLECT-TASK.md is Blocked and its paths are intentionally stale" | source.md:1 | containment, Task 1 (1.0) |
| INF-028 | "reported first in the summary" | source.md:1 | containment, Task 1 (0.6667) |
| INF-029 | "D-007 label the .gitignore row rewrite comment only" | source.md:1 | containment, Task 1 (0.875) |
| INF-030 | "keep the entry as a retired-path guard" | source.md:1 | containment, Task 1 (1.0) |
| INF-031 | "D-008 prove internal checkouts still work by running their tests with -rs and requiring zero skips or a recorded reason" | source.md:1 | containment, Task 8 (0.75) |
| INF-032 | "a rerun in a full-depth, non-root checkout" | source.md:1 | containment, Task 8 (0.8333) |
| INF-033 | "D-009 the fetch and pull ban is a literal reading" | source.md:1 | containment, Task 4 (1.0) |
| INF-034 | "the dated Orca project-id note is an authorized addition" | source.md:1 | containment, Task 4 (0.8571) |
| INF-035 | "D-010 add the Orca flags --json, --issue and --pr to the confirmed command list" | source.md:1 | containment, Task 4 (0.8182) |
| INF-036 | "D-011 add tests/skills/test_sc_recommend_routing_contract.py to the sync and parity test run" | source.md:1 | containment, Task 7 (0.9286) |
| INF-037 | "D-012 describe the /sc:post-release tag checkout as an optional read-only checkout removed after the scan" | source.md:1 | containment, Task 3 (1.0) |
| INF-038 | "D-013 say in the new worktree rule what happens to the two existing checkouts under the retired .dev/worktrees location" | source.md:1 | containment, Task 3 (0.9333) |
| INF-039 | "(do not move or remove them in this plan)" | source.md:1 | none lexically (best Task 1, 0.5); content-level COVERED: plan line 27 (now stale, see D-012 below) |
| INF-040 | "D-014 note docs/swarm/runbook.md:34's .claude/worktrees path" | source.md:1 | containment, Task 1 (1.0) |
| INF-041 | "The eval_runner.py rewrite is a behaviour change and needs a regression test." | source.md:1 | containment, Task 2 (0.7778) |
