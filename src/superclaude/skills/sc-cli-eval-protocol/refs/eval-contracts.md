# Ref: Eval Contract Surface (re-read targets)

> **This ref is a MAP, not the truth.** The authority for any flag/field this run is the cited
> digest returned by the `eval-docs-loader` agent in Wave 0. The values below are a reading aid and a
> "what to open" checklist — if they disagree with the loader digest, the digest wins, and you should
> re-invoke the loader rather than trust this file. The eval pipeline evolves; this ref can drift.

## What the loader must open (and you cite from)

| Concern | Primary source |
|---|---|
| `eval` subcommands + flag matrix | `src/superclaude/cli/eval/commands.py` (the `@click.group("eval")` group) |
| Suite manifest schema | `src/superclaude/cli/eval/suites/suite.schema.json` |
| Naming rules / inventory | `src/superclaude/cli/eval/suites/README.md` |
| House-style templates | `src/superclaude/cli/eval/suites/{eval_smoke,installer_sync_drift}.yaml` |
| Artifact layout + run-id | `src/superclaude/cli/eval/artifact_layout.py` |
| summary.json schema + status enum | `src/superclaude/cli/eval/{run_report,models}.py` |
| Exit codes | `src/superclaude/cli/eval/exit_codes.py` |
| HOME preservation | `src/superclaude/cli/eval/{runner,isolation}.py` |
| Operator gotchas (FR-G5, --no-pty) | `docs/eval/suites-guide.md` |
| Runtime / validation / retry / scratch | `docs/eval/{runtime,validation-commands,retry,scratch-roots}.md` |

## Reading aid (verify against the digest before use)

- **Subcommands**: `eval doctor`, `eval list`, `eval describe`, `eval run`.
- **`eval list --json`** → JSON array of `{name, version, eval_count}`. Drives the run menu.
- **`eval describe --suite <name> [--eval <id>] [--json]`** → full validated manifest (YAML default).
- **`eval run --suite <name>`** flags to confirm with the user: `--parallel` (default ~8, clamp 1..15),
  `--eval <id>` (repeatable), `--no-mcp`, `--no-pty`, `--output-dir`, `--keep-home`, `--timeout-mult`
  (default 1.0), `--max-disk-mb`, `--json`, `--verbose`, `--junit`.
- **Exit codes**: `0` success · `1` failures · `2` usage/harness/**FR-G5 coverage gate** · `3` interrupted.
- **Artifacts**: `<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` →
  `summary.{md,json,yaml}` (always), `junit.xml` (only `--junit`), `per-eval/<eval_id>/`.
- **summary.json**: top-level `run_id, started_at, finished_at, duration_sec, suite, manifest_version,
  parallel, counts, totals, evals, artifacts`. Per-eval `EvalOutcome`: `eval_id, title, status,
  duration_sec, expects[], skip_reason, skip_flag_triggered, artifacts{name→path}, error_class`.
- **Status enum (8)**: `PASS, FAIL, ERRORED, TIMEOUT, INTERRUPTED, SKIPPED, XFAIL, XPASS`. SKIPPED ≠ PASS.
- **HOME preservation**: every non-PASS eval keeps its HOME by default (forensics); PASS removes it
  unless `--keep-home`. The per-eval HOME path surfaces inside that eval's `artifacts{}` map.

## Schema quick-reference (verify against suite.schema.json via the digest)

Top-level required: `name, version, description, defaults, required_binaries, optional_capabilities,
evals` (top level `additionalProperties:false`). Each `evals[]` entry requires `id` + `title`
(`additionalProperties:false`). Optional eval keys: `category, requires[], timeout_sec, isolation,
inputs[], expects[], parameterize[], no_pty`.

- `version`: `^[0-9]+\.[0-9]+(\.[0-9]+)?$`
- eval `id`: `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` (FR-SCH2)
- `failure_mode`: `hard|skip|xfail`
- `isolation.home_strategy`: `ephemeral|seeded|shared`; `seed_state[]` of `{path, content?}`
- `no_pty`: only `"skip"`.

## FR-G5 empty-HOME workaround (confirm exact form from the digest / suites-guide.md)

```bash
TMPHOME=$(mktemp -d) && HOME=$TMPHOME uv run superclaude eval run \
  --suite <name> --no-mcp; rm -rf "$TMPHOME"
```

The doctor preflight checks every PreToolUse/PostToolUse matcher in `~/.claude/settings.json` against
the suite. An empty `$HOME` has no matchers, so nothing is uncovered → no exit 2.
