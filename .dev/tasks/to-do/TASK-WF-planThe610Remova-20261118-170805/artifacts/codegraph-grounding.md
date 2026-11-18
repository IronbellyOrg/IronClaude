# Codegraph grounding

## Run state

- index_state: fresh (codegraph_status at 2026-11-18T16:5x UTC: 3429 files, 46775 nodes, 0 changes since index; the index was built before any edit, so it describes the pre-removal tree)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/ic61-part-b-bundle (the checkout this plan was written in)
- projectPath: the same path
- access mode: MCP
- tokens: none

## Resolved symbols

- ReflectRunner._apply_remediation: src/superclaude/cli/reflect/runner.py:583 (verb `/task` or `/sc:implement`)
- ReflectRunner.run: src/superclaude/cli/reflect/runner.py:642 (the only caller of _apply_remediation, codegraph_callers)
- ReflectRunner._build_prompt: runner.py:452; _claude_argv_preview: runner.py:484
- reflect result fields remediation_task_path and remediation_plan_path: models.py:148-151, contract.py:126-128, panel_lint.py:114-115, runner.py:769-771 (grep; codegraph has no symbol for the dataclass fields)
- install retire step: src/superclaude/cli/install_retired_files.py, install_retired_data.py (generated), scripts/gen_retired_install_data.py (generator; `--tag` repeatable)

## Dependents

- The bundle is Markdown copied by the installers; no Python module imports a bundle item (map section 6). The dependents are text references listed per file in .dev/cleanup/bundle/dependency-map.md and .dev/cleanup/bundle/reference-index.md.
- runner.py users (codegraph_node file mode): 13 files, all under tests/cli/reflect/ and related tests.

## Pre-check

Checked with grep and ls (Glob floor) against the pre-removal tree: every repo-relative file path in the plan exists except files the plan creates (docs/releases/v6.1.0.md) and short names written relative to a folder named earlier in the same task (refs/*.md, rf-*.md, test_*.py). Symbols: `_apply_remediation` (runner.py:583) has one caller, `run` (runner.py:642), as Task 9 states. Dependents that no task names: none found; the tests under tests/cli/reflect/ that use runner.py are named in Task 9. 19 tasks checked.
