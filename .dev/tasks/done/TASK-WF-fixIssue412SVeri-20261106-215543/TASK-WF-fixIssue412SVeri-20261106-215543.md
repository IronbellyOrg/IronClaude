---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-fixIssue412SVeri-20261106-215543
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Correct Claude CLI session launch guidance

Source: ./source.md
Goal: New ccsession-backed Claude sessions are explicitly directed to Orca's Claude (CLI) agent route, and forced IronClaude setup requests a safe refresh of existing Orca guides.

## Constraints

- Fix only issue #412. Its existing issue body already references verified IronClaude refresh-introducing PR #245 and intentional Orca CLI-label PR #29074. Do not create another issue or claim that the label PR changed shell startup. Runtime incident causation remains UNDETERMINED; diagnostic closure remains advisory.
- No commit, push, PR, global install or other-repository mutation. Orca source/history stays read-only. No new dependency or launch wrapper.
- Canonical edits are under src/superclaude and tests. Run make sync-dev and make verify-sync after changes. Never stage generated .claude mirrors. Always stage .dev/tasks packages and artifacts.
- Supervised workers keep the dispatch preamble and worker-start authority. Internal Agent-tool subagents remain internal. Ordinary agent launch is not a substitute for supervised worker dispatch.
- IronClaude force means request Orca's normal safe installation. Never pass Orca --force, replace edited guides, change Claude executable settings or make plain shell terminals start an agent.
- Installed Orca help defines update behavior; existing owned unmodified copies may update, edited or foreign copies may be skipped. Meaningful installer output must remain visible. Do not treat a safe skip as proof that the guide refreshed.

## Phase 1: Explicit session selection

## Task 1: Add canonical launch instructions and a regression check

Inputs: the explicit launch requirement in source.md, src/superclaude/core/CLAUDE.md, src/superclaude/skills/ccsession-tag/README.md, and the current installed orca-cli guide. Add a concise global selection rule and matching launcher README passage. Add tests/core/test_orca_session_launch_guidance.py using existing pytest static-document conventions. Test the absence before editing the two instruction files, then apply the instructions. Preserve Settings > Agents > Claude > Command configuration of ccsession-orca and distinguish a Claude CLI agent from an ordinary shell.

Outputs: the two canonical instruction files and runnable guidance checks; save observed failing/passing output under ./artifacts/t1-tests.log. No runtime Orca change is authorized.

Acceptance criteria:
- Both instruction surfaces explicitly distinguish Claude (CLI) for ccsession-backed Claude sessions from New Terminal and terminal create for shells, and identify agent launch and worktree create --agent as programmatic agent creation routes after loading the version-matched Orca guide. Explicit terminal surface is named only when a CLI session is required.
- Both surfaces preserve supervised worker-start/preamble authority and internal Agent-tool subagents. README retains the ccsession-orca executable configuration prerequisite rather than claiming every agent launch automatically uses ccsession.
- The new guidance tests are observed failing against the original instruction files and passing after the bounded edit. They check the shell/CLI distinction and supervised/internal-agent boundaries, not UI runtime success. Evidence records that scope honestly.

## Phase 2: Safe guide refresh

## Task 2: Propagate forced setup refresh with regression checks

Depends on: Task 1

Inputs: source.md's safe-refresh requirement, src/superclaude/cli/install_user_setup.py helper and caller, tests/cli/test_install_user_setup.py, and installed orca-ide skills install --help. Add a backward-compatible force argument to install_orca_skills and pass the enclosing install_user_setup force intent. Existing files may short-circuit only when force is false. A forced request uses the normal safe Orca install command, without external --force. Preserve the current executable identification, deadline, absent/failed-Orca nonfatal behavior and three-skill list. Relay meaningful Orca stdout/stderr so edited/foreign guide skips cannot be hidden by an unconditional success summary; reuse existing result fields without a new parser. Add minimal tests for helper refresh, top-level propagation, safe default skip, surfaced skip/failure output and nonfatal absence/failure with existing guides.

Outputs: the canonical helper/caller and matching tests; observed red/green and wider regression output under ./artifacts/t2-tests.log. Run synchronization and record its output in ./artifacts/sync.log as part of delivering the changed skill README, without staging mirrors.

Acceptance criteria:
- A forced user-setup request reaches normal Orca guide installation even with all three files present, and top-level force propagation is covered. Nonforce repeated setup still skips existing guides with no Orca calls. The external command never gains --force and existing edited-guide contents are not rewritten by IronClaude.
- Absent Orca, timeout, nonzero installation result or incomplete installation remains nonfatal and accurately reported. Meaningful skipped/warning output from Orca is surfaced, including when files already exist; tests cover those cases without network or global writes.
- New refresh regression checks fail before the implementation and pass afterwards. The related installer tests, tests/unit/test_cli_install.py, guidance tests and tests/core/test_claude_md_routing_block.py pass. Ruff on changed Python files and make sync-dev plus make verify-sync succeed. Logs distinguish mocked installer checks from actual Orca dry-run evidence; no live guide refresh or UI reproduction is claimed.
