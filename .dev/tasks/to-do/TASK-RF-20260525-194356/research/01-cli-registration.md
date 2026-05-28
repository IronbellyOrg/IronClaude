# CLI Registration Research: init-lite --context-optimized

Status: Complete

## Initial Inventory

Evidence tags: `[CODE-VERIFIED]` means the claim is verified against repository files cited on the same bullet; `[TASK-DECISION]` means a design/task choice derived from the critiqued feature design rather than pre-existing code.

- [CODE-VERIFIED] `src/superclaude/cli/` contains existing command modules including `main.py`, command packages (`sprint`, `roadmap`, `cleanup_audit`, `tasklist`, `cli_portify`, `prd`, `eval`) and installer/support modules (`install_*`, `doctor.py`, `vocabulary.py`). Evidence: `ls /config/workspace/IronClaude/src/superclaude/cli` output in this research turn.
- [CODE-VERIFIED] `tests/cli/test_cli_registration.py` is the current top-level Click registration regression suite. Auggie retrieved its `EXPECTED_TOP_LEVEL_COMMANDS` snapshot at lines 32-48 and tests around lines 62-118, showing it is intentionally updated when top-level commands are added.
- [CODE-VERIFIED] `src/superclaude/cli/main.py` is the top-level Click entrypoint. Auggie retrieved the `main` Click group at lines 18-26 and additive group registrations at lines 400-426.

## CLI Source Inventory

- [CODE-VERIFIED] `src/superclaude/cli/main.py` top-level symbols are `main`, `install`, `mcp`, `update`, `install_skill`, `doctor`, and `version` (Serena overview for `src/superclaude/cli/main.py`). This means existing inline command functions live in `main.py`, while later command groups are imported and registered near file end.
- [CODE-VERIFIED] `tests/cli/test_cli_registration.py` top-level symbols are constants `EXPECTED_TOP_LEVEL_COMMANDS`, `EXPECTED_EVAL_SUBCOMMANDS_M1`, fixture `runner`, and tests `test_top_level_help_lists_eval_group`, `test_top_level_command_roster_unchanged`, `test_eval_group_help_lists_m1_subcommands`, `test_eval_group_registers_m1_subcommands_in_click`, `test_pre_existing_command_help_still_invokable` (Serena overview for `tests/cli/test_cli_registration.py`).
- [CODE-VERIFIED] Command implementation precedent under `src/superclaude/cli/` uses both inline commands in `main.py` and subpackages with `commands.py`; the file inventory shows command packages `cleanup_audit/commands.py`, `cli_portify/commands.py`, `eval/commands.py`, `prd/commands.py`, `roadmap/commands.py`, `sprint/commands.py`, and `tasklist/commands.py`.

## `src/superclaude/cli/main.py` Integration Points

- [CODE-VERIFIED] The root CLI group is `main` decorated with `@click.group()` and `@click.version_option(version=__version__, prog_name="SuperClaude")` at `/config/workspace/IronClaude/src/superclaude/cli/main.py:18-20`; its docstring/help body is at lines 21-25.
- [CODE-VERIFIED] Existing simple top-level commands can be implemented inline in `main.py`: `install` is registered by `@main.command()` at `/config/workspace/IronClaude/src/superclaude/cli/main.py:29` and accepts Click options at lines 30-45 before function signature line 46.
- [CODE-VERIFIED] Existing `version` is another inline `@main.command()` at `/config/workspace/IronClaude/src/superclaude/cli/main.py:394-397`.
- [CODE-VERIFIED] Existing command groups are registered additively at file end. The current imports/additions are `sprint` at lines 400-402, `roadmap` at lines 404-406, `cleanup-audit` at lines 408-410, `tasklist` at lines 412-414, `cli-portify` at lines 416-418, `prd` at lines 420-422, and `eval` at lines 424-426.
- [TASK-DECISION] Exact registration hook for a new top-level command can therefore be either inline `@main.command("init-lite")` in `main.py`, or a new subpackage command imported near lines 400-426 and registered via `main.add_command(init_lite_command, name="init-lite")`. Existing `prd` exports its group from `/config/workspace/IronClaude/src/superclaude/cli/prd/__init__.py:10-14`; existing `eval` exports `eval_group` from `/config/workspace/IronClaude/src/superclaude/cli/eval/__init__.py:13-26`.

## `tests/cli/test_cli_registration.py` Integration Points

- [CODE-VERIFIED] `tests/cli/test_cli_registration.py` imports `main` from `superclaude.cli.main` at `/config/workspace/IronClaude/tests/cli/test_cli_registration.py:26`, so tests exercise the live Click object in-process.
- [CODE-VERIFIED] The top-level command roster is a frozen snapshot in `EXPECTED_TOP_LEVEL_COMMANDS` at `/config/workspace/IronClaude/tests/cli/test_cli_registration.py:32-48`; adding `init-lite` requires adding the string `"init-lite"` to this set or `test_top_level_command_roster_unchanged` will report it as unexpected.
- [CODE-VERIFIED] The roster assertion computes `actual = frozenset(main.commands.keys())` at `/config/workspace/IronClaude/tests/cli/test_cli_registration.py:75` and compares missing/unexpected at lines 76-82; this directly validates command registration, not only help text.
- [CODE-VERIFIED] The existing smoke loop invokes `--help` for every top-level command except `eval` at `/config/workspace/IronClaude/tests/cli/test_cli_registration.py:115-118`; after adding `init-lite` to the expected set, `superclaude init-lite --help` must exit 0 or this existing test fails.
- [TASK-DECISION] Existing help-specific test `test_top_level_help_lists_eval_group` at `/config/workspace/IronClaude/tests/cli/test_cli_registration.py:62-70` is eval-specific. A new analogous CLI-focused test should assert `runner.invoke(main, ["--help"])` contains `init-lite`, and another should assert `runner.invoke(main, ["init-lite", "--help"])` contains required flags `--context-optimized`, `--dry-run`, `--output`, `--project-root`, `--scaffold`, and `--force`.

## Summary

The CLI implementation should add a top-level `init-lite` Click command, preferably in a focused module registered from `src/superclaude/cli/main.py`, then update `tests/cli/test_cli_registration.py` so the frozen command roster and existing help smoke test intentionally cover the new command. Focused init-lite tests should exercise the live `superclaude.cli.main:main` Click object via `CliRunner`.
