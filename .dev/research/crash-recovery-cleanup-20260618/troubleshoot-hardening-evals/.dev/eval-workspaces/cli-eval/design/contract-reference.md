# cliEval Contract Reference (frozen for this build)

> Captured fresh from source on 2026-06-12 per the MANDATORY FRESH-CONTEXT RULE.
> The SKILL itself must RE-READ these at runtime — this file is a build-time aid, not a
> substitute for the runtime fresh-context load. Every row is cited `file:line`.

## `superclaude eval` subcommands + flags (commands.py)

Group `@click.group("eval")` → `eval_group` (commands.py:762). Four subcommands:

| Subcommand | Key flags (cited) |
|---|---|
| `doctor` | `--json`, `--no-mcp`, `--check-coverage`, `--output-dir`, `--parallel`, `--suite` (commands.py:767-820) |
| `list` | `--json` (array of `{name,version,eval_count}`), `--suites-dir` (commands.py:924-971) |
| `describe` | `--suite` (required), `--eval <id>`, `--json` (YAML default), `--suites-dir` (commands.py:1205-1241) |
| `run` | `--suite` (req), `--parallel` (def 8, clamp 1..15), `--eval` (multiple), `--no-mcp`, `--no-pty`, `--output-dir`, `--keep-home`, `--timeout-mult` (def 1.0), `--max-disk-mb`, `--json`, `--verbose`, `--junit` (commands.py:1553-1654) |

`eval list --json` VERIFIED live: returns sorted JSON list of `{eval_count,name,version}`. 14 suites currently on disk (real=17 evals, eval_smoke=3, installer_sync_drift=1, model_capability_matrix=8, frontier_vs_cheap_combo=4, …).

## Exit codes (exit_codes.py:21-24)

| Int | Constant | Meaning |
|---|---|---|
| 0 | SUCCESS | all pass |
| 1 | FAILURES | ≥1 FAIL/ERRORED/TIMEOUT/XPASS |
| 2 | USAGE_ERROR | operator misuse / config / harness contract / **FR-G5 coverage-gate** |
| 3 | INTERRUPTED | SIGINT/SIGTERM cooperative cancel (NOT POSIX 130) |

FR-G5 coverage gate == exit 2 CONFIRMED (commands.py:919-921; suites-guide.md:526-530).

## suite.schema.json (Draft 2020-12, additionalProperties:false top level)

Top-level **required** (schema:7-15): `name, version, description, defaults, required_binaries, optional_capabilities, evals`.

- `name` str minLen1 = filename stem (schema:18-22; README stem==name rule)
- `version` str `^[0-9]+\.[0-9]+(\.[0-9]+)?$` (schema:23-27)
- `defaults` obj: `per_eval_timeout_sec`(int≥1), `per_eval_memory_mb`(int≥1), `capture_tty`(bool), `keep_home_on_success`(bool) (schema:32-42)
- `required_binaries[]`: `{name, min_version?, failure_mode}` — HARD gate (schema:70-79)
- `optional_capabilities[]`: `{name, gate_flag?, failure_mode}` — SOFT gate (schema:80-89)
- `failureMode` enum: `hard|skip|xfail` (schema:60-64)
- `evalEntry` (additionalProperties:false, **required `id,title`**): `id`(evalIdString), `title`(str minLen1), `category?`, `requires?[]`, `timeout_sec?`(int≥1), `isolation?`, `inputs?[]`, `expects?[]`, `parameterize?[]`(minItems1), `no_pty?` (schema:124-159)
- `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` (schema:65-69)
- `isolationBlock`: `home_strategy` enum `ephemeral|seeded|shared`; `seed_state[]` of `{path, content?}` (schema:90-111)
- `no_pty` enum **`["skip"]` only** → with `--no-pty` emits SKIPPED, `skip_reason="--no-pty"` BEFORE HOME setup (schema:153-157)

## Artifact layout (artifact_layout.py)

```
<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/
  summary.md  summary.json  summary.yaml
  junit.xml            # only with --junit
  per-eval/<eval_id>/{logs.jsonl, tty.transcript, artifacts/}
```
- RUN_DIR_PREFIX = `.dev/eval-runs` (artifact_layout.py:76); run-id = `<HHMMSSZ>-<8hex>` (sha256 of suite+started_at) (artifact_layout.py:151-204).
- summary.{md,json,yaml} unconditional (run_report.py:391-397); junit.xml only when emit_junit (run_report.py:405-408).
- `--output-dir` is the OUTPUT ROOT; FR-G4 layout layered underneath (runtime.md:89-96).

## summary.json schema (run_report.py / models.py)

Top-level (models.py:820-832): `run_id, started_at, finished_at, duration_sec, suite, manifest_version, parallel, counts, totals, evals, artifacts`.
- `counts`: `manifest_n, expanded_n_prime, kept_k, skipped_s, kept_plus_skipped_equals_n_prime` (models.py:742-780)
- `totals`: `passed, failed, skipped, errored, interrupted, timeout` (models.py:783-815)
- per-eval `EvalOutcome` (9 fields, models.py:293-381): `eval_id, title, status, duration_sec, expects[], skip_reason, skip_flag_triggered, artifacts{name→path}, error_class`
- **status enum = 8 values**: `PASS, FAIL, ERRORED, TIMEOUT, INTERRUPTED, SKIPPED, XFAIL, XPASS` (NOT SKIP/ERROR). Per-eval HOME path surfaces inside `artifacts{}`.

## HOME preservation (runner.py:444)

`keep = True if status != "PASS" else keep_home_on_pass`. Every non-PASS preserves HOME by default; PASS removes unless `--keep-home`. Failed HOMEs forensic at `.dev/eval-runs/<run>/…` per-eval `artifacts{}` map (suites-guide.md:518-521, 580-582).

## FR-G5 empty-HOME workaround (suites-guide.md:536-537)

```bash
TMPHOME=$(mktemp -d) && HOME=$TMPHOME uv run superclaude eval run \
  --suite <name> --no-mcp; rm -rf "$TMPHOME"
```
The doctor preflight checks every PreToolUse/PostToolUse matcher in `~/.claude/settings.json` against the suite's evals; empty `$HOME` ⇒ no matchers ⇒ nothing uncovered ⇒ no exit 2.

## `*_callbacks.py` sibling (suites/README.md:22, 81-83)

Optional sibling Python module exporting YAML-callback escape-hatch functions; imported lazily by suites naming `callback:` entries. No callback-using suite ships today (forward-looking convention).
