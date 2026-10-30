# T1 reflection card (UC-1, inline orchestrator card)

Mode: pre. Spec: `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md` (860 lines). Tasklist: `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md` (19 tasks, 6 phases).
Card author: inline orchestrator (UC-1 has no `root-cause-analyst` role; `socratic-mentor` is `--depth deep` only). Degraded: serena (not used by run rule), get_current_config.

## Coverage / acceptance section (qa lens)

- Pass 1 (regex `R-|REQ-|SPEC-|T-NNN`, fenced code skipped): 0 parsed IDs. Pass 2 (requirements-analyst): 340 quote-pinned rows, `artifacts/inferred-requirements.yaml`. `coverage_pct: null` (no parsed rows), `coverage_degraded: parsed-sparse` (340 inferred > 0 parsed).
- Deterministic containment match (`artifacts/match.py`, threshold 0.6): 241 of 340 matched, `coverage_pct_union: 0.7088`, 99 unmapped (`artifacts/coverage-matrix.yaml`).
- Triage of the 99 (`artifacts/unmapped-triage.yaml`, script `artifacts/triage.py`): 41 are named by row ID in the plan (for example `C1`-`C12`, `P68-P71`), 55 sit in a source section the plan task cites as "Implements ./source.md §N" (the plan points the executor at `./source.md` instead of copying line ranges, which lowers lexical overlap), 3 have no reference: INF-114 (goal paragraph, `source.md:261`, restated by the plan's `Goal:` line), INF-115 ("Historical `.dev/` artifacts stay untouched.", `source.md:261`) and INF-125 (§2.3 leftovers IronClaude does not own, `source.md:279`).

### F-2 Two scope limits are missing from the plan's Constraints (MINOR)
- Evidence: INF-115 (`source.md:261`) and INF-125 (`source.md:279-291`) are referenced by no task and no Constraint; the plan's Constraints forbid deleting user data and editing other repositories but never say "do not edit historical `.dev/` artifacts" or "do not remove the §2.3 leftovers (Coder image binary, `serena-agent` uv tool, bundle markers, upstream companions)".
- Class: coverage gap (scope boundary).
- Fix: add one Constraint bullet naming both limits with a pointer to `./source.md` §2.1 and §2.3.

## Deviation / root-cause section (analyzer lens)

### F-1 Task 12's repo-wide memory-name search cannot pass at Task 12 (red acceptance)
- Evidence: Task 12 acceptance runs `rg -n --no-ignore 'write_memory|...|get_current_config' src/superclaude plugins/superclaude commands agents` (tasklist Task 12). Two hits survive Task 12: `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127` (contains `get_current_config`; the file is row P84, owned by Task 13, which runs later) and `src/superclaude/cli/reflect/contract.py:30` (comment lists `get_current_config`; Task 7 rewords that comment but its acceptance checks only `serena`).
- Class: plan defect (ordering / acceptance scope), inherited from source §8 T10/T10b.
- Fix: Task 7 also removes `get_current_config` from the `contract.py:28-31` comment and checks `rg -n 'get_current_config' src/superclaude/cli/reflect` prints nothing; Task 12's repo-wide search excludes `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` (Task 13 deletes lines 124-127, and Task 15's `acceptance-search.sh serena src/superclaude ...` covers it, because `SER` contains `get_current_config`).

## Structural section

- Phases: 6 (G0-G5), tasks 1-19 contiguous, every `Depends on` names a lower task; one commit per task; issue-#323 comment at the end of each phase (Tasks 1, 6, 9, 15, 17, 19); decision rules and test baseline rule in Constraints; final full-suite comparison in Task 18.
- Row coverage check (script, this run): every §1.2 row with Task `T9` (33 rows) appears in Task 10; every `T10`/`T11` row appears in Tasks 11-15 (P69, P70 through the `P68-P71` range); `T12` rows C8-C12, S7, S9-S13, S16, S17, S20-S31 appear in Task 16; `T13` rows S1-S5 in Task 17.
- Grounding: every repo path the plan cites exists except files the plan creates (`install_retired_mcp.py`, `test_install_retired_mcp.py`, `test_install_mcp_cli.py`, the two `.dev/codegraph-migration/handoffs/` files). Spot-checked lines match: `src/superclaude/cli/main.py:254`, `install_mcp.py:916`, `hooks/hooks.json:47`, plugin `hooks.json:37`, `tests/cli/test_install_hooks.py:684`, `commands/pm.md:52`, `core/CLAUDE.md:112`, `sc-tasklist-protocol/SKILL.md:683`, `tests/cli/eval/test_coverage_gate.py:127`, `reflect/ensemble.py:824`, `install_mcp.py:1319` ("Unknown MCP server selection").

## Risk register

- R-1 (HIGH, F-1): Task 12 acceptance is red by construction (repo-wide `get_current_config` hits in a Task-13 file and in a comment Task 7 rewrites without checking that token).
- R-2 (MEDIUM): Task 9's acceptance relies on the message at `src/superclaude/cli/install_mcp.py:1319` ("Unknown MCP server selection: ...") surviving Task 5, which rewrites `:1243-1343 (parts)` of the same file; no Task 5 check pins it.
- R-3 (LOW): Task 18's `./update.sh` sandbox run needs network for `pipx install --force ./`; the documented fallback records a deviation, not a pass.
- R-4 (LOW, F-2): without the scope Constraint an executor could "clean up" historical `.dev/` text or Coder-owned leftovers while chasing the residual search.

## Recommendations

- For F-1: in Task 7 add "remove `get_current_config` from the `contract.py:28-31` comment" and the acceptance `rg -n 'get_current_config' src/superclaude/cli/reflect` prints nothing; in Task 12 add `-g '!src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md'` to the repo-wide search with a note that Task 13 deletes those lines and Task 15's `acceptance-search.sh serena src/superclaude ...` covers it.
- For R-2: add to Task 5 acceptance `rg -q 'Unknown MCP server selection' src/superclaude/cli/install_mcp.py`.
- For F-2: add the Constraint bullet (historical `.dev/` artifacts untouched; §2.3 leftovers are handed off, never removed by Phase 1).
