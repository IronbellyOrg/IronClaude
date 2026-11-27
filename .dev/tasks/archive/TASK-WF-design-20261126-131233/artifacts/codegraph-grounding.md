# Codegraph grounding for TASK-WF-design-20261126-131233

## Run state

- index_state: fresh (`codegraph_status`: 0 added, 0 modified, 0 removed since the index)
- checked_at: 2026-11-26T13:13:53Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-599
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-599
- access: mcp (lookup tools listed)
- switch: `SUPERCLAUDE_CODEGRAPH_PRIMITIVES` unset; no init or index build running
- tokens: graph:ambiguous (`_make_result` has four same-named definitions, three of them unrelated audit test helpers; the reflect one was confirmed by search), graph:empty (the field name `remediation_task_path` returned no definition row because dataclass attributes are not indexed; field uses were confirmed with `git grep`). The `derive_verdict` caller list was truncated at 20 of 63 and re-queried once at limit 100 (63 of 63 shown).
- Caller rows give definition lines only. Every call site named below was confirmed by search before it was written as a call.

## Resolved symbols

- `ReflectResult` (class), `src/superclaude/cli/reflect/models.py:126`; field `remediation_task_path` at `models.py:148`, field `remediation_plan_path` at `models.py:151` (Read).
- `_make_result` (function), `src/superclaude/cli/reflect/contract.py:104`; the kwarg to remove is `contract.py:126` (Read).
- `derive_verdict` (function), `src/superclaude/cli/reflect/contract.py:138`; signature unchanged by this plan.
- `_load` helper and the imports of `derive_verdict` and `Verdict` in `tests/cli/reflect/test_verdict_mapping.py` (Read, `:12-19`).
- Helpers and tests in `tests/cli/reflect/test_remediation_route_table.py`: `_ROOT`, `_REF`, `_SKILL`, `_CMD` (`:13-16`), `_PROHIBITION` (`:18`), `_row` (`:21`), and five tests (`:25`, `:36`, `:45`, `:49`, `:57`).
- Markdown anchors (not indexed; Read): `### Phase A` and `### Phase B` in `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` (`:28`, `:77`); the bullets `- **Phase A` and `- **Phase B` in `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (`:374`, `:376`); the `sc:workflow-protocol` delegation row (`SKILL.md:624`); section 7 heading `SKILL.md:610`, section 8 heading `:664`.

## Dependents

- `ReflectResult` constructions (confirmed by `git grep "ReflectResult("`): `src/superclaude/cli/reflect/commands.py` (`:406`, `:448`), `src/superclaude/cli/reflect/contract.py` (`:114`), `src/superclaude/cli/reflect/runner.py` (`:615`, `:652`, `:669`, `:696`), `tests/cli/reflect/test_writeback.py` (`:42`, `:182`). All use keywords; only `contract.py:126` passes the field being removed.
- `ReflectResult` is exported by `src/superclaude/cli/reflect/__init__.py` (`:20`, `:26`); no other indexed file reads `remediation_task_path`.
- `derive_verdict` call sites confirmed by search: `src/superclaude/cli/reflect/runner.py:572` (inside `_audit_once`), `scripts/reflect_verdict_replay.py:83` (reads only `result.verdict.value` and `result.reason`), and 63 callers in total, almost all in `tests/cli/reflect/` (`test_verdict_mapping.py` 46 calls, `test_ensemble_stub_integration.py` 4, `test_contract_fallback_metadata.py` 3, `test_ensemble_fallback_engage.py` 3, `test_ensemble_fallback_stub.py` 2, `test_promote_plumbing.py` 2, `test_classify_fix.py` 1).
- `_make_result` (reflect) call sites: eleven inside `derive_verdict` in `src/superclaude/cli/reflect/contract.py` (`:162` to `:255`); no other file.
- Consumers of the pointer: `src/superclaude/cli/reflect/runner.py:765` reads `result.remediation_plan_path` only; `runner.py:763-764` is a comment naming the retired key and stays.
- Guard dependent: `tests/cli/reflect/test_shadow_skill_contract.py` (`:43-50` pins the 1.9.0 block, `:53-76` diffs `SKILL.md` against `HEAD`).

## Pre-check

Run at Wave 4 before the reflect call; read-only; no new readiness check. Result: 7 tasks checked, 0 problems.

- Files named by the tasks: all 20 exist: 3 test files edited (`test_remediation_route_table.py`, `test_verdict_mapping.py`, `test_fix_loop.py`), 3 test files run unchanged (`test_writeback.py`, `test_panel_contract_lint.py`, `test_shadow_skill_contract.py`), 2 fixtures read, 2 reflect source files edited (`contract.py`, `models.py`) and 3 read (`runner.py`, `commands.py`, `panel_lint.py`), plus `SKILL.md`, the ref, the command file, the guide, the replay script, `Makefile` and `pyproject.toml`.
- Symbols and lines named: `_make_result` (`contract.py:104`), `derive_verdict` (`contract.py:138`), `_halted_reason` (`contract.py:361`), `_audit_once` (`runner.py:511`), the three loop tests (`test_fix_loop.py:92`, `:195`, `:215`), `runner.py:765-767` (reads `result.remediation_plan_path`, breaks on none), the `format`, `sync-dev` and `verify-sync` Makefile targets (`:53`, `:109`, `:166`), `SKILL.md` anchors at lines 374, 376, 574, 576, 581, 588, 595, 598, 600, 610, 624, 664 (re-read).
- Dependents named by the tasks: the seven `ReflectResult` construction sites and the two `derive_verdict` consumers outside the reflect tests (`runner.py:572`, `scripts/reflect_verdict_replay.py:83`).
- Dependents of the touched symbols that no task names, and why none needs an edit: `CHANGELOG.md` (lines 42, 52, 578 to 604: release history and the statement that the key stays in the schema, true after the change); `docs/guides/reflect-cli-tools-guide.md` (lines 48 and 330: "stays in the schema" and "is ignored", true after the change); `docs/user-guide/commands.md` (line 1328, headless description, unchanged by the change). The 8 YAML fixtures keep the key by design.
