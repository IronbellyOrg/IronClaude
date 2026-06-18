# report.md — `doc_flag_parity` cliEval suite

## What was built
A new cliEval suite that guards documentation/CLI flag parity for `superclaude
eval run`: the documented flag table in `docs/user-guide/eval-pipeline.md`
(lines 162-174) must stay in sync with the live `superclaude eval run --help`
output (the twelve `@click.option` flags on `eval_run`, commands.py:1553-1668).

## Where the suite is
- Source of truth: `src/superclaude/cli/eval/suites/doc_flag_parity.yaml`
- Copy with this report: `<this dir>/doc_flag_parity.yaml`
Discovered directly from src/ (`eval list` → `doc_flag_parity (version 1.0, 2 evals)`).
`cli/eval/suites/` is part of the Python package and is NOT mirrored to `.claude/`
by `make sync-dev` (that target syncs only skills/agents/commands/templates), so
no sync step is needed and `verify-sync` is unaffected.

## How it works (2 evals, both no_pty: skip, home_strategy: shared, read-only)
- DP1 (DOC->CLI): runs `eval run --help`; asserts exit_code==0 plus one
  `stdout: contains "<flag>"` per documented flag (12). Fails if a documented
  flag was removed/renamed in the CLI.
- DP2 (CLI->DOC, bidirectional): diffs the `--help` flag set against the doc
  table both ways and prints one verdict line; asserts `contains
  "FLAG_PARITY: IN_SYNC"` and `not_contains "FLAG_PARITY: DRIFT"`. Closes the
  "CLI gained an undocumented flag" gap that `contains` alone cannot express.
Together: any add/remove/rename on either surface trips DP1 or DP2.

## Verified valid — YES
| Check | Command | Result |
|---|---|---|
| Schema validation | `eval describe --suite doc_flag_parity` | exit 0, full render (validate_manifest ran) |
| Discovery | `eval list` | `doc_flag_parity (version 1.0, 2 evals)`, exit 0 |
| Loader direct | `loader.validate_manifest(path)` | OK -> 2 EvalSpecs ['DP1','DP2'] |
| Assertion rows | `Expect.from_mapping(each row)` | OK -> all 16 rows resolve to real primitives |
| Contract true today | `eval run --help` | exit 0; all 12 flags present; doc table lists exactly those 12 |

Passes every validation layer: JSON-schema, filename rules (stem==name==
`doc_flag_parity`), discovery, and declarative-assertion resolution. The encoded
invariant is also true today (12 flags, both surfaces agree).

## Caveat on the full end-to-end run
`eval run --suite doc_flag_parity --no-pty ...` exits 2 on this host — but at an
FR-G5 matcher-coverage preflight (`coverage gate FAILED — uncovered matcher
patterns: PostToolUse: mcp__auggie__.*`) that fires BEFORE any suite is reached.
Confirmed host-environment condition, not a suite defect: the shipped
`eval_smoke` suite exits 2 with the identical message on the same host. On a host
that passes `eval doctor --check-coverage`, the suite proceeds through the runner
exactly like `eval_smoke`; validity does not depend on that host gate, and every
host-independent layer passes.

## Suggested cadence (encoded in the manifest header)
On every PR touching commands.py (eval_run option block) or eval-pipeline.md
(flag table), and nightly in CI.
