# Task 3: plugin copy of `WORKER-CONTRACT.md`

## Decision

No copy was added. `plugins/superclaude/core/WORKER-CONTRACT.md` does not exist, and `make sync-dev` was not needed for this task.

## Lines that decided it

1. `scripts/build_superclaude_plugin.py:75-76` copies only the `agents`, `commands`, `hooks`, `scripts` and `skills` folders of `plugins/superclaude/` into the plugin build:
   ```
   for folder in ["agents", "commands", "hooks", "scripts", "skills"]:
       copy_tree(PLUGIN_SRC / folder, DIST_ROOT / folder)
   ```
   `core` is not in that list, so nothing in `plugins/superclaude/core/` reaches the built plugin. The build script gives no reason to add a copy there.
2. `plugins/superclaude/core/` (`git ls-files plugins/superclaude/core`, 2026-11-03) holds only 6 of the 11 core files that existed before this plan: `BUSINESS_PANEL_EXAMPLES.md`, `BUSINESS_SYMBOLS.md`, `CODEGRAPH.md`, `PRINCIPLES.md`, `RESEARCH_CONFIG.md`, `RULES.md`. The other five core files (`BASH_INSPECTION_POLICY.md`, `CLAUDE.md`, `HOW-WE-WORK.md`, `ISSUE-BACKLOG.md`, `ISSUE-HANDOFF.md`) have no plugin copy, so the folder is not a full mirror of `src/superclaude/core/`.
3. Three of those six copies are not byte-identical to their `src/superclaude/core/` sources (`cmp` on 2026-11-03: `BUSINESS_PANEL_EXAMPLES.md`, `BUSINESS_SYMBOLS.md` and `RESEARCH_CONFIG.md` differ), so there is no byte-mirror rule for the folder as a whole.
4. The only test that requires a plugin core copy names one file: `tests/core/test_codegraph_guide.py:19` (`_PLUGIN_GUIDE = _REPO / "plugins" / "superclaude" / "core" / "CODEGRAPH.md"`) and `:133-134` (asserts it exists and equals the source). `tests/commands/test_impact_command.py:309` also names only `CODEGRAPH.md`. No test or sync tool (`Makefile` has no `plugins/superclaude/core` target) requires every core file to be copied.

The existing convention is therefore per file, with no rule that covers a new core file, so the convention does not require a copy of `WORKER-CONTRACT.md`. The AC-C1 scan already excludes a plugin copy by name, so adding one later stays possible without changing that check.

## Checks run for this task

- AC-0.1 install check (`./source.md` section 7.3): `uv run python -c "import pathlib, tempfile; from superclaude.cli.install_core import install_core_files; d = pathlib.Path(tempfile.mkdtemp()); ok, msg = install_core_files(target_path=d); assert ok, msg; assert (d / 'WORKER-CONTRACT.md').is_file()"` exited 0.
- `uv run pytest tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py -q -p no:cacheprovider`: `14 passed in 0.30s`.
- No `cmp` check applies, because no copy was added.
