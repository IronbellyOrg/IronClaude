# trace.md — authoring + validating `doc_flag_parity` cliEval suite

Task: author a new eval suite that checks the documented `superclaude eval run`
flags stay in sync with `superclaude eval run --help`, set it up properly, and
verify it is actually valid.

Working dir: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
All `uv run` lines emit a benign `VIRTUAL_ENV=/lsiopy ... ignored` warning (harness env), omitted below.

---

## Step 1 — Survey the eval suite surface

```
ls -la src/superclaude/cli/eval/suites/          # exit 0 — 15 manifests + schema + README
find src/superclaude/cli/eval -type f            # exit 0 — loader.py, expect.py, commands.py, etc.
```

Read for the contract:
- `suites/suite.schema.json` — manifest schema (required keys: name, version, description, defaults, required_binaries, optional_capabilities, evals).
- `suites/README.md` — filename rules: stem `[a-z][a-z0-9_]*`, stem == `name:`, `.yaml` only; authoring checklist says validate via `eval describe --suite <stem>`.
- `suites/installer_sync_drift.yaml` — closest precedent: a "drift guard" suite that drives Claude to run a command and asserts on stdout/exit_code.
- `suites/audit_wiring_guard.yaml` + `suites/eval_smoke.yaml` — confirm the prompt→Bash→`stdout: contains`/`exit_code: equals` pattern and the `no_pty: skip` convention.
- `expect.py` — the 7 declarative primitives (file, jsonl, settings_json, exit_code, stderr, stdout, duration); stdout supports `contains` / `regex` / `not_contains`.

## Step 2 — Pin the two parity surfaces

```
grep -n '@eval_group.command("run")' ... commands.py     # eval_run at line 1553
Read commands.py:1553-1668                                # 12 @click.option flags on eval_run
grep -n '--flag tokens' docs/user-guide/eval-pipeline.md  # flag table at lines 162-174
```

Authoritative `eval run` flag set (both sources agree): `--suite --parallel --eval
--no-mcp --no-pty --output-dir --keep-home --timeout-mult --max-disk-mb --json
--verbose --junit` (12 flags; `--help` is universal and excluded).

```
uv run superclaude eval run --help        # exit 0 — all 12 flags present verbatim in Options:
```

## Step 3 — Author the suite (source of truth)

Wrote `src/superclaude/cli/eval/suites/doc_flag_parity.yaml`:
- name/stem `doc_flag_parity` (snake_case, stem == name → README filename rules satisfied).
- DP1: prompts Claude to run `eval run --help`; asserts `exit_code == 0` and one
  `stdout: contains "<flag>"` per documented flag (12 rows). Catches DOC→CLI drift
  (a documented flag removed/renamed in the CLI).
- DP2: prompts Claude to diff the `--help` flag set against the doc table in BOTH
  directions and emit a single verdict line; asserts `stdout: contains
  "FLAG_PARITY: IN_SYNC"` and `stdout: not_contains "FLAG_PARITY: DRIFT"`. Closes
  the CLI→DOC gap that `contains` alone cannot express.
- `home_strategy: shared` (DP2 reads the working-tree doc; both evals read-only),
  `no_pty: skip` (matches inventory convention).

## Step 4 — Validate

```
uv run superclaude eval describe --suite doc_flag_parity      # DESCRIBE_EXIT=0 — schema-valid, full render
uv run superclaude eval list | grep doc_flag_parity           # LIST_EXIT=0 — "doc_flag_parity (version 1.0, 2 evals)"
```

Defence-in-depth via the loader directly:

```
uv run python -c "loader.validate_manifest(path); Expect.from_mapping(each expects row)"
# VALIDATE_EXIT=0
# validate_manifest: OK -> 2 EvalSpec(s): ['DP1', 'DP2']
# Expect.from_mapping: OK (16 assertion rows resolved to real primitives)
```

End-to-end runnable check via the `--no-pty` skip path (as `eval_smoke` ES3 does):

```
uv run superclaude eval run --suite doc_flag_parity --no-pty --no-mcp --json --output-dir /tmp/tmp.XXXX
# RUN_EXIT=2 — rejected: --output-dir escaped AC12 scratch-root allowlist (operator error, not suite)

uv run superclaude eval run --suite doc_flag_parity --no-pty --no-mcp --json --junit --verbose \
  --output-dir /tmp/eval-runs/doc_flag_parity_validate
# RUN_EXIT=2 — "eval doctor: coverage gate FAILED — uncovered matcher patterns: PostToolUse: mcp__auggie__.*"
```

Isolated whether the gate is host-level or suite-level:

```
uv run superclaude eval run --suite eval_smoke --no-pty --no-mcp --output-dir /tmp/eval-runs/smoke_probe
# SMOKE_EXIT=2 — SAME FR-G5 coverage-gate failure on the SHIPPED eval_smoke suite
```

→ Conclusion: the FR-G5 matcher-coverage preflight (eval-pipeline.md:251-252) fires
on this host's settings.json for EVERY `eval run` before any suite is reached. It is
a host-environment condition, identical for the shipped `eval_smoke` suite, NOT a
defect in `doc_flag_parity`. The manifest's validity is fully established by the
schema/discovery/loader/expect layers above, which do not depend on the host gate.

## Step 5 — Place + sync

```
cp src/superclaude/cli/eval/suites/doc_flag_parity.yaml <outputs>/doc_flag_parity.yaml   # exit 0
grep sync-dev Makefile; sed -n '109,130p' Makefile
# sync-dev mirrors only skills/agents/commands/templates → .claude/.
# cli/eval/suites/ is part of the Python package, read directly from src/ by the loader,
# NOT mirrored to .claude/ → no sync step needed; verify-sync unaffected.
```

The suite lives in the single source of truth (`src/superclaude/cli/eval/suites/`)
and is discovered there directly. No `.claude/` copy exists or is required.
