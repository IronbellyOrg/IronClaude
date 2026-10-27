# D-0071 — `eval_group` Click group registration (COMP-001)

**Task:** T04.09 (Phase 4, Roadmap R-071 / COMP-001)
**Module:** `src/superclaude/cli/eval/commands.py` — `eval_group`
**Entry-point wiring:** `src/superclaude/cli/main.py` line 424–426
**Tests:** `tests/cli/eval/test_eval_group.py` (5 cases)
**Status:** Implemented 2026-05-21

## Group export

```python
@click.group("eval")
def eval_group() -> None:
    """Run and inspect the cliEval real-eval harness."""
```

The group is declared at `src/superclaude/cli/eval/commands.py:756–758`
and the four subcommands are bolted on with `@eval_group.command(...)`
decorators in the same module:

| Subcommand | Source line | Roadmap anchor | Task |
|---|---|---|---|
| `doctor`   | `commands.py:761` | FR-CLI4 / R-011 | T01.13 |
| `list`     | `commands.py:920` | FR-CLI2 / R-018 | T01.21 |
| `describe` | `commands.py:1207` | FR-CLI3 / R-019 | T01.22 |
| `run`      | `commands.py:1542` | FR-CLI1 / R-072 | T04.10 |

Click sorts subcommands lexicographically in `--help`; the rendered
order is therefore `describe, doctor, list, run` regardless of the
registration order above. The test suite asserts against the sorted
set, not a sequence.

## Entry-point wiring (FR-G3 / T01.26 carry-through)

`src/superclaude/cli/main.py` imports the group and attaches it to the
top-level `superclaude` Click group:

```python
from superclaude.cli.eval.commands import eval_group
main.add_command(eval_group, name="eval")
```

This keeps the FR-G3 registration single-source-of-truth: T01.26
landed the import + `add_command` line, and T04.09 only adds
subcommands to the group. No new wiring is required at the entry
point — the four subcommands ride along for free once attached.

## Acceptance bullets

| AC | How satisfied |
|---|---|
| `superclaude eval --help` lists `run`, `list`, `describe`, `doctor` | Click renders the group surface; captured in `evidence/T04.09/eval-help.txt`. |
| Click group is registered at the superclaude CLI entry point so existing commands remain unaffected | `main.add_command(eval_group, name="eval")` at `main.py:426`; existing commands (`install`, `mcp`, `sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, `doctor`, `version`, `update`, `install-skill`) all remain in the top-level `--help`; captured in `evidence/T04.09/superclaude-help.txt`. |
| `superclaude --help` continues to list the eval group from T01.26 wiring | Same evidence file — the `eval` line appears alphabetically between `doctor` and `install`. |
| `D-0071/spec.md` documents the group export | This file. |

## Scope boundary

T04.09 covers only **registration**. The body of `eval run` (12 flags,
RunOrchestrator wiring, exit-code mapping) lands in T04.10. T04.09's
test only asserts that `eval run --help` resolves without invoking the
body — i.e. that the subcommand is *reachable*, not that it does
anything useful. The `run` body verification belongs to T04.10 /
D-0072.
