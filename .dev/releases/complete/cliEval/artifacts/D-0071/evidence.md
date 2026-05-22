# D-0071 — Evidence

## Acceptance criteria coverage

| AC | How verified | Evidence link |
|---|---|---|
| `superclaude eval --help` lists `run`, `list`, `describe`, and `doctor` as subcommands. | `superclaude eval --help` rendered all four subcommands; `test_eval_group_help_lists_all_four_subcommands` asserts each name appears in the output. | `evidence/T04.09/eval-help.txt`, `evidence/T04.09/pytest-output.txt` |
| Click group is registered at the superclaude CLI entry point so existing commands remain unaffected. | `superclaude --help` still lists every previously-registered command (`install`, `mcp`, `sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, `doctor`, `version`, `update`, `install-skill`) alongside the new `eval` group; `test_top_level_main_lists_eval_group` pins the `eval` line. | `evidence/T04.09/superclaude-help.txt`, `evidence/T04.09/pytest-output.txt` |
| `superclaude --help` continues to list the eval group from T01.26 wiring. | Same `superclaude-help.txt` capture: `eval` appears alphabetically between `doctor` and `install`. | `evidence/T04.09/superclaude-help.txt` |
| `D-0071/spec.md` documents the group export. | See `artifacts/D-0071/spec.md`. | `artifacts/D-0071/spec.md` |

## Validation example (from phase-4-tasklist.md)

The task validation step calls for:

> Manual check: run `superclaude eval --help` and confirm all 4 subcommands listed.

```text
$ uv run superclaude eval --help
Usage: superclaude eval [OPTIONS] COMMAND [ARGS]...

  Run and inspect the cliEval real-eval harness.

Options:
  --help  Show this message and exit.

Commands:
  describe  Print a validated, post-parameterize-expansion manifest.
  doctor    Verify host preconditions for ``superclaude eval run``.
  list      Enumerate suite manifests under ``cli/eval/suites/``.
  run       Run a cliEval suite end-to-end (FR-CLI1 / D-0072).
```

All four subcommands present. Full capture: `evidence/T04.09/eval-help.txt`.

## Test run

```text
$ uv run pytest tests/cli/eval/test_eval_group.py -v
============================== 5 passed in 0.16s ==============================
```

Tests:

| Test | What it pins |
|---|---|
| `test_eval_group_registers_four_subcommands` | `eval_group.commands` keys exactly equal `{"describe", "doctor", "list", "run"}`. |
| `test_eval_group_help_lists_all_four_subcommands` | Each of the four names appears in `eval_group, ["--help"]` output. |
| `test_top_level_main_lists_eval_group` | T01.26 / FR-G3 entry-point wiring: `main, ["--help"]` surfaces the word `eval`. |
| `test_eval_invoked_through_main_lists_subcommands` | Dispatch through the entry point reaches the group surface: `main, ["eval", "--help"]` shows all four subcommands. |
| `test_run_help_lists_subcommand` | `eval run --help` resolves (exit 0) without invoking the body. Body verification is T04.10. |

Full output: `evidence/T04.09/pytest-output.txt`.

## Files changed / added

| Path | Change |
|---|---|
| `src/superclaude/cli/eval/commands.py` | Pre-existing — `eval_group` declared at line 756; `doctor` / `list` / `describe` / `run` decorators landed at T01.13 / T01.21 / T01.22 / T04.10. T04.09 makes no source changes. |
| `src/superclaude/cli/main.py` | Pre-existing — `main.add_command(eval_group, name="eval")` line landed at T01.26 / FR-G3. T04.09 makes no source changes. |
| `tests/cli/eval/test_eval_group.py` | Pre-existing 5-case acceptance harness for the group surface (already authored alongside the registration). |
| `.dev/releases/current/cliEval/artifacts/D-0071/spec.md` | **NEW** — group export contract, subcommand → roadmap mapping, entry-point wiring. |
| `.dev/releases/current/cliEval/artifacts/D-0071/notes.md` | **NEW** — why T04.09 is documentation-only, decisions, deferred follow-ups, risk notes. |
| `.dev/releases/current/cliEval/artifacts/D-0071/evidence.md` | **NEW** — this file. |
| `.dev/releases/current/cliEval/evidence/T04.09/pytest-output.txt` | **NEW** — verbatim pytest run. |
| `.dev/releases/current/cliEval/evidence/T04.09/eval-help.txt` | **NEW** — `superclaude eval --help` capture. |
| `.dev/releases/current/cliEval/evidence/T04.09/superclaude-help.txt` | **NEW** — `superclaude --help` capture showing the `eval` group alongside existing commands. |
