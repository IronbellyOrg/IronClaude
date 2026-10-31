# Phase 3 Task 13: full verification and live smoke (source §5 row T11 checks 0-9)

Worktree: `/home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption`, branch `feat/codegraph-adoption`. Each check lists the exact command and its real result.

## (0) Changelog and user-doc entries

Command: `rg -q 'sc:impact' CHANGELOG.md && rg -q 'sc:graph' CHANGELOG.md && rg -q 'SUPERCLAUDE_CODEGRAPH_PRIMITIVES' docs/user-guide/mcp-installation.md && rg -q 'SUPERCLAUDE_CODEGRAPH_AUTOINIT' docs/user-guide/mcp-installation.md`

Result: PASS (exit 0). New CHANGELOG section "Added: codegraph in commands, skills and agents; `/sc:impact` and `/sc:graph` (#323)"; new subsection "Commands and skills that use codegraph" at the end of the codegraph section of `docs/user-guide/mcp-installation.md`.

## (1) Sync dev copies

Command: `make sync-dev && make verify-sync`.

`make` is not installed on this host (`/bin/bash: make: command not found`, exit 127). The two recipes were run as written instead, with `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py`, which reads the target's recipe from `Makefile`, runs each logical line in the Makefile's `SHELL` (`/bin/bash`) like GNU make, turns `$$` into `$`, stops at the first failing line, and refuses targets with prerequisites or make variables (neither target has any).

Result: PASS. `sync-dev` exit 0 ("Sync complete": 38 skill directories, 45 agents, 45 commands, 12 hooks, 52 templates); `verify-sync` exit 0, last line "All components in sync." Log: `artifacts/t13-sync.log`. `git status` shows no `.claude/` path (gitignored).

## (2) Installed-path count against baseline (a)

Command: `grep -rIn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks} | grep -v 'src/superclaude/core/CODEGRAPH.md' | wc -l`

Result: PASS. Count 157, baseline (a) 157 (no change).

## (3) Zero old tool names in primitives

Command: the `rg -n -i --pcre2 'mcp__serena|mcp__codebase-memory|\b(find_symbol|...|index_repository)\b' src/superclaude/{skills,commands,agents,core,hooks,modes,mcp} plugins/superclaude` command of source §5 row T11.

Result: PASS. No output (rg exit 1, no match).

## (4) Mutating-verb check

Command: `rg -n 'Bash\(codegraph (init|index|sync|uninit|unlock|upgrade|install|uninstall|telemetry (on|off))' src/superclaude/{commands,skills,agents} plugins/superclaude/{commands,skills,agents} | rg -v '^src/superclaude/commands/graph.md:'`

Result: PASS. No output. The guide part (mutating verbs only inside "Never") is pinned by `tests/core/test_codegraph_guide.py`, which passed in check (8).

## (5) No wildcard

Command: `rg -n 'Bash\(codegraph \*\)|mcp__codegraph__\*' src/superclaude/{commands,skills,agents,core,hooks,modes} plugins/superclaude -g '!**/core/CODEGRAPH.md'`

Result: PASS. No output.

## (6) No explore

Command: `rg -n 'codegraph_explore|codegraph explore|codegraph context' src/superclaude/{commands,skills,agents,hooks,modes} plugins/superclaude -g '!**/core/CODEGRAPH.md'`

Result: PASS. No output.

## (7) Pin parity

Command: `test "$(sed -n 's/^Pinned codegraph version: //p' src/superclaude/core/CODEGRAPH.md)" = "$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import VERSION; print(VERSION)')"`

Result: PASS. Guide 1.6.2, code 1.6.2. `cmp src/superclaude/core/CODEGRAPH.md plugins/superclaude/core/CODEGRAPH.md`: identical.

## (8) Targeted tests against baseline (b)

Commands: `$TESTSET` in two invocations (the Task 1 split; group 2 is `tests/roadmap/test_threshold_registry.py`), each `uv run pytest <paths> -q -p no:cacheprovider -rfE --tb=no`, through the Constraints failing-id pipeline into `.dev/codegraph-migration/experiments/P3-T11-failures.txt`; then `comm -13 .dev/codegraph-migration/experiments/P3-baseline-failures.txt .dev/codegraph-migration/experiments/P3-T11-failures.txt`. Every test file Tasks 3-12 created lies inside a `$TESTSET` directory (`tests/core/test_codegraph_guide.py`, `tests/agents/test_codegraph_rosters.py`, `tests/troubleshoot/test_codegraph_grounding.py`, `tests/skills/test_codegraph_adoption.py`, `tests/commands/test_graph_command.py`, `tests/commands/test_impact_command.py`; Task 11 added a test to the existing `tests/cli/reflect/test_verdict_mapping.py`).

Result: PASS. Group 1: 2081 passed, 86 skipped, 1 xpassed; group 2: 23 passed (baseline (b): 1897 passed, 0 failed). `P3-T11-failures.txt` is empty; `comm -13` prints nothing. Logs: `artifacts/t13-testset-g1.log`, `artifacts/t13-testset-g2.log`.

## (9) Live smoke in a fresh session

Setup: G3 holds (seven-tool branch). After the sync of check (1), each command ran in a new headless session started in the worktree: `claude -p "<command>" --permission-mode dontAsk --setting-sources user,project --output-format json --allowedTools "Skill Read Grep Glob"` (scripts `/tmp/impl-review/t13-smoke.sh` and `t13-smoke2.sh`; raw JSON, stderr and exit codes in `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-smoke/`). Each session's init event lists the `codegraph` MCP server as `connected`. `~/.claude/CODEGRAPH.md` does not exist (no `superclaude install`); every run recorded that it read the labelled fallback `src/superclaude/core/CODEGRAPH.md`.

Pre-check: `rg -n 'install_core_files\(' src/superclaude/cli/main.py` prints `178:    core_success, core_message = install_core_files(force=force)` and `365:    core_success, core_message = install_core_files(force=True)`.

### `/sc:graph status`

Run 1, exit 0, no permission denials. Real output:

```text
codegraph 1.6.2 (pin 1.6.2: match)
index: fresh (own), checked 2026-10-31T15:23:21Z
access: mcp; MCP lookup tools listed: yes
counts: 972 files, 8840 nodes, 19711 edges
pending: 0
telemetry: on; opt out: export CODEGRAPH_TELEMETRY=0 (or DO_NOT_TRACK=1) in your shell profile
switch off codegraph in primitives: SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off
next: index ready
```

Result: PASS (`fresh`). "telemetry: on" is what `codegraph telemetry status` reports for the CLI's own config; the MCP registration sets `CODEGRAPH_TELEMETRY=0` for the server only.

### `/sc:impact install_core_files --output-dir .dev/codegraph-migration/experiments/P3-T11-impact`

- Run 1 (exit 0): the lookups were right (`install` at `src/superclaude/cli/main.py:178` and `update` at `:365`, both `resolution: call-site-verified`, `partition: prod`), but the session wrote `impact.md` as a stub and was then denied `Edit` (the skill's `allowed-tools` had `Write` but not `Edit`; dontAsk denies anything not allowed), so the contract ended `status: failed` with an unfilled report. Saved in `artifacts/t13-smoke/run1-impact/`.
- Fix: `Edit` added to the `allowed-tools` of `sc-impact-protocol` and `sc-graph-protocol` (each skill's "Will Not" limits Write and Edit to its own output files), with the pinned sets in `tests/commands/test_impact_command.py` and `tests/commands/test_graph_command.py` updated (123 passed); sync re-run.
- Run 2 (exit 0, no permission denials): `status: success`, `index_state: fresh`, `degraded: []`, `prod 2/2`, `test 0/0`, `transitive 0`; dependents `install` (`src/superclaude/cli/main.py`, `def_line: 46`, `call_site_line: 178`, `resolution: call-site-verified`) and `update` (`def_line: 340`, `call_site_line: 365`, `call-site-verified`). `impact.md` is complete (no placeholder left). The contract's `errors` list holds one line, the failed Read of `~/.claude/CODEGRAPH.md` before the fallback.

Result: PASS after the fix. `/sc:impact` lists `install` in `src/superclaude/cli/main.py` as a production dependent with `resolution: call-site-verified`.

### `/sc:troubleshoot "install_core_files skips files" --depth quick`

- Run 1 (exit 0): the session loaded the installed `~/.claude/skills/sc-troubleshoot-protocol/SKILL.md`, which predates Phase 3 (0 lines mention codegraph; its closed analyst roster is `Read, Grep, Glob, mcp__auggie__codebase-retrieval`). A personal skill takes precedence over the project `.claude/skills/` copy of the same name, and `superclaude install` is forbidden here, so this run exercised the old protocol: `mcps_available: context7,tavily`, the roster check rejected the synced project agent ("tools roster has additional codegraph tools beyond the loaded protocol's closed roster"), and no `tier1-callers.md` was written. Evidence in `artifacts/t13-smoke/run1-troubleshoot/`.
- Run 2 (exit 0): a new headless session told to Read and follow this branch's dev copy `.claude/skills/sc-troubleshoot-protocol/SKILL.md` instead of the Skill tool (same issue text and `--depth quick`, git writes forbidden; allowed tools: Read, Grep, Glob, Write, Edit, Agent, Task, the five codegraph MCP tools and read-only Bash patterns). Audit log: `mcps_available: codegraph|context7|tavily`, "Installed CODEGRAPH.md absent; read labelled in-checkout fallback", `index_state: fresh`, "troubleshoot-analyst: project definition valid; exact closed roster verified", "2/2 caller rows ... confirmed by Read. tier1-callers.md persisted. No graph degraded token." `tier1-callers.md` holds `index_state: fresh` and two rows, `install` (`main.py:46`, call site `main.py:178`, `call-site-verified`) and `update` (`main.py:340`, call site `main.py:365`, `call-site-verified`). The run ended `status: blocked` at Tier 1 because this headless allowlist denied `uv run python .../update-counter.py`, the diagnosability-counter step that predates Phase 3 and is unrelated to codegraph. Evidence in `artifacts/t13-smoke/run2-troubleshoot/`.

Result: PASS for what check (9) asks (`tier1-callers.md` written, with verified caller rows), through the dev skill copy. The installed-skill path cannot show the new behaviour until `superclaude install` runs after merge, which this phase may not run; the run directories under `.dev/troubleshoot/` are left untracked and uncommitted.

## Result

Checks (0)-(8): PASS. Check (9): `/sc:graph status` PASS; `/sc:impact` PASS after one fix (`Edit` added to the two new skills' allowlists); `/sc:troubleshoot` writes `tier1-callers.md` with call-site-verified rows when the session follows this branch's skill copy, while the installed pre-Phase-3 copy shadows it until the next `superclaude install`.
