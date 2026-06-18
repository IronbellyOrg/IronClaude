# Design Spec — `eval_cli_doc_parity` suite

## Guard target
The documented `superclaude eval run` flag surface must stay in sync with the
flags the CLI actually exposes via `superclaude eval run --help`. `eval run`'s
own docstring (commands.py) advertises "the twelve FR-CLI1 flags"; the
suites-guide.md operator doc references each of them (`--suite`, `--no-pty`,
`--no-mcp`, `--json`, `--eval`, `--parallel`, `--keep-home`, `--timeout-mult`,
`--max-disk-mb`, `--output-dir`, `--junit`, `--verbose`). If a flag is renamed,
removed, or dropped from `--help` (e.g. a refactor of the Click option block),
the docs silently drift and operators paste invocations that error out. A
recurring eval that diffs the live `--help` text against the documented flag
names catches that drift on PR.

## Why a recurring eval (not a one-off unit test)
The flag surface is a doc⇆CLI contract that spans two artifacts (Click options
in `commands.py` and the `docs/eval/suites-guide.md` flag references). It is
exactly the doc-parity class flagged in memory `feedback_doc_fanout_facts_sheet`
("CLI docs get a doc⇆CLI parity test"). Running it through the eval harness
(rather than pytest) keeps it in the same on-PR / nightly cadence as the rest of
the cliEval inventory and exercises the real installed CLI entry point.

## Scenarios → evals
All evals shape a Claude prompt that drives `superclaude eval run --help` (or a
plain `--help`) through Bash and asserts on captured stdout. `--help` exits 0 and
needs no MCP/HOME state, so the suite is host-agnostic.

- **DP1 — core safety flags present.** Drive `superclaude eval run --help`; assert
  the four most operator-load-bearing flags appear: `--suite`, `--no-pty`,
  `--no-mcp`, `--json`. exit_code == 0.
- **DP2 — full twelve-flag surface present.** Drive the same `--help`; assert the
  remaining documented flags appear: `--eval`, `--parallel`, `--keep-home`,
  `--timeout-mult`, `--max-disk-mb`, `--output-dir`, `--junit`, `--verbose`.
  exit_code == 0. (Split from DP1 so a failure localizes which half drifted.)
- **DP3 — `--suite` is marked required (contract guard).** Drive `--help`; assert
  the help renders the `--suite` option as `[required]`. Catches the regression
  where `--suite` loses its `required=True` (which would change the documented
  contract). exit_code == 0.

## Isolation
`ephemeral` — `eval run --help` reads nothing from HOME or the working tree; the
default ephemeral HOME is correct and keeps the suite host-independent.

## Capabilities
- `required_binaries`: `claude` (PTY harness driver, house-style), `git`.
  `superclaude` itself is invoked inside the prompt via the installed console
  script; the harness already guarantees the package is importable.
- `optional_capabilities`: none.

## Cadence (operator metadata, not enforced)
on-PR (any change to `src/superclaude/cli/eval/commands.py` `eval run` options or
`docs/eval/suites-guide.md`) + nightly.

## PTY
Every eval carries `no_pty: skip` to match the rest of the inventory (uniform
`--no-pty` semantics).

## Assertion strategy
Positive substring (`stdout.contains: "--<flag>"`) per documented flag +
`exit_code.equals: 0`. Substring on the long-name string is the minimal,
drift-sensitive contract: any rename/removal in the Click block changes `--help`
output and fails the contains assertion. Multiple flags split across DP1/DP2 so a
failure pinpoints the drifted half rather than reporting one opaque fail.

## Fresh-context citations (Wave 0)
- `superclaude eval run --help` (live, exit 0): twelve options enumerated —
  `--suite/--parallel/--eval/--no-mcp/--no-pty/--output-dir/--keep-home/`
  `--timeout-mult/--max-disk-mb/--json/--verbose/--junit`. Docstring: "the twelve
  FR-CLI1 flags".
- `suite.schema.json`: top-level required keys = name, version, description,
  defaults, required_binaries, optional_capabilities, evals; `additionalProperties:false`.
  eval entry requires `id`+`title`; optional `category/requires/timeout_sec/`
  `isolation/inputs/expects/parameterize/no_pty`. eval id regex
  `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. version regex `^[0-9]+\.[0-9]+(\.[0-9]+)?$`.
  `no_pty` enum: only `"skip"`. `isolation.home_strategy`: ephemeral|seeded|shared.
- `eval_smoke.yaml`: house style — `inputs[].prompt` carries the Claude prompt;
  `expects[]` is a list of single-key objects (`{stdout:{contains:...}}`,
  `{exit_code:{equals:0}}`). `# yaml-language-server` schema header line.
- `installer_sync_drift.yaml`: house style — `inputs[].prompt` + optional
  `expect_tool_call: Bash`; `expects[]` supports `{stdout:{not_contains:...}}`.
- `suites/README.md`: filename rules — `.yaml`, snake_case stem, stem == `name:`.
