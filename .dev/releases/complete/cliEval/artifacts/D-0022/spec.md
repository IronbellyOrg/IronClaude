# D-0022 — `superclaude eval` Click group registration spec

**Task:** T01.26 (Phase 1, Roadmap FR-G3 / R-022)
**Module:** `src/superclaude/cli/main.py`
**CLI surface:** `superclaude eval [list|describe|doctor]`
**Status:** Implemented 2026-05-20

## FR-G3 contract

FR-G3 requires additive CLI integration: the `eval` group must be
registered at the existing `superclaude` entry point without changing the
name, help text, or registration of any pre-existing command. Help text
at the top level must expose the new group; `eval --help` must list the
M1 subcommands.

## Entry-point wiring

The `eval` group is attached to the top-level Click group `main` defined
in `src/superclaude/cli/main.py` via the standard `add_command` pattern
used by every other top-level group in the project:

```python
# src/superclaude/cli/main.py:393-395
from superclaude.cli.eval.commands import eval_group

main.add_command(eval_group, name="eval")
```

The `eval_group` itself is defined in `src/superclaude/cli/eval/commands.py`
as a `@click.group("eval")`-decorated function whose docstring becomes the
top-level help blurb ("Run and inspect the cliEval real-eval harness.").
M1 subcommands (`doctor`, `list`, `describe`) attach to `eval_group` via
`@eval_group.command(...)` in the same module so the group is
self-contained — no further wiring in `main.py` is required when new
`eval` subcommands land (e.g. `run` per FR-CLI1 in M4).

## Acceptance criteria mapping

| AC bullet (T01.26)                                                       | Site / Evidence |
|--------------------------------------------------------------------------|-----------------|
| `superclaude --help` lists `eval` as a subcommand group.                 | `tests/cli/test_cli_registration.py::test_top_level_help_lists_eval_group`. CLI smoke captured in `evidence/T01.26/run.md`. |
| `superclaude eval --help` lists the M1 subcommands (`list`, `describe`, `doctor`); additional subcommands land per their milestones (`run` per FR-CLI1 in M4). | `tests/cli/test_cli_registration.py::test_eval_group_help_lists_m1_subcommands` and `::test_eval_group_registers_m1_subcommands_in_click`. |
| Existing `superclaude` subcommands behave identically (regression test snapshot). | `tests/cli/test_cli_registration.py::test_top_level_command_roster_unchanged` (frozen-set snapshot) and `::test_pre_existing_command_help_still_invokable` (per-command `--help` smoke). |
| `TASKLIST_ROOT/artifacts/D-0022/spec.md` records entry-point wiring.     | This file. |

## Top-level command roster (regression snapshot)

The full set of top-level commands registered on `main` after the `eval`
group lands — this list is also encoded as `EXPECTED_TOP_LEVEL_COMMANDS`
in the regression test and any drift causes a deliberate test update:

```
cleanup-audit, cli-portify, doctor, eval, install, install-skill, mcp,
prd, roadmap, sprint, tasklist, update, version
```

The pre-existing groups (`sprint`, `roadmap`, `cleanup-audit`,
`tasklist`, `cli-portify`, `prd`) and singletons (`install`,
`install-skill`, `mcp`, `update`, `doctor`, `version`) are unchanged. The
only addition is the `eval` group.

## Subcommand floor under `eval`

M1 commands attached to `eval_group`:

| Name      | Source                                  | Milestone | Task    |
|-----------|-----------------------------------------|-----------|---------|
| `doctor`  | `cli/eval/commands.py::doctor`          | M1        | T01.13  |
| `list`    | `cli/eval/commands.py::eval_list`       | M1        | T01.21  |
| `describe`| `cli/eval/commands.py::eval_describe`   | M1        | T01.22  |

Future subcommands (`run` per FR-CLI1) attach to the same `eval_group`
in their landing task; no edits to `main.py` are required.

## Files touched

| Path                                                                  | Action |
|-----------------------------------------------------------------------|--------|
| `src/superclaude/cli/main.py`                                         | Pre-existing — eval group registration was wired at lines 393-395 during T01.13/T01.21/T01.22 sequencing; T01.26 validates and tests the additive contract. |
| `tests/cli/test_cli_registration.py`                                  | Created — 5 regression tests covering the four AC bullets. |
| `.dev/releases/current/cliEval/artifacts/D-0022/spec.md`              | Created (this file). |
| `.dev/releases/current/cliEval/artifacts/D-0022/notes.md`             | Created. |
| `.dev/releases/current/cliEval/artifacts/D-0022/evidence.md`          | Created. |
| `.dev/releases/current/cliEval/evidence/T01.26/run.md`                | Created — captures `pytest` log + `superclaude --help` / `superclaude eval --help` smoke output. |

## Verification

Per task tier (STANDARD, Verification Method: Direct test execution):

```
$ uv run pytest tests/cli/test_cli_registration.py -v
```

5 tests passing on 2026-05-20. The full pre-existing CLI test surface
(`tests/cli/eval/`) is untouched by this task and remains green.

## Out of scope

- Adding `run` or any other post-M1 `eval` subcommand (lands per its
  own task, e.g. FR-CLI1 T04.x).
- Modifying any pre-existing command's behaviour, flags, or help text.
- Distribution/install side effects — registration is at the Click
  decorator level only.
