# Trace — inspect installer_sync_drift suite + --no-pty safety check

Working dir: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`

## Step 1 — List suites, create output dir
- `ls src/superclaude/cli/eval/suites/` → exit 0. Confirmed `installer_sync_drift.yaml` exists.
- `mkdir -p .dev/eval-workspaces/.../outputs/` → exit 0.

## Step 2 — Read the suite manifest + schema (parallel)
- `Read src/superclaude/cli/eval/suites/installer_sync_drift.yaml` → exit 0.
  - 1 eval: `S1` "make verify-sync — src/ vs .claude/ parity + installer registration".
  - `defaults`: per_eval_timeout_sec 180, capture_tty true, keep_home_on_success false.
  - `required_binaries`: claude (>=0.5.0, hard), make (hard), uv (hard), git (hard).
  - `S1.isolation.home_strategy: shared`; `S1.no_pty: skip`.
  - Header comment (lines 28-31) states `no_pty=skip` rationale: the PTY harness drives a Claude Code subprocess; uniform `--no-pty` semantics across suites.
- `Read suite.schema.json` → exit 0.
  - `no_pty` property (schema lines 153-157): enum `["skip"]`. Doc string: when set to `"skip"`, `superclaude eval run --no-pty` short-circuits the eval → `EvalOutcome` status `SKIPPED`, `skip_reason="--no-pty"`, `skip_flag_triggered="--no-pty"`, BEFORE any HOME setup. Advisory metadata; does NOT affect runs not invoked with `--no-pty`.

## Step 3 — Locate runner code handling no_pty
- `grep -rln "no_pty|skip_flag_triggered|--no-pty" src/superclaude/cli/eval/*.py`
  → run_report.py, commands.py, models.py, runner.py, orchestrator.py.
- `grep -n "no_pty" src/superclaude/cli/eval/*.py` → real short-circuit lives in `commands.py`:
  - `commands.py:1894`: `if no_pty and spec.no_pty == "skip":`
  - `models.py:101-143`: `EvalSpec.no_pty: str | None`, parsed from manifest `data.get("no_pty")`.

## Step 4 — Read the short-circuit implementation
- `Read commands.py:1880-1920` → exit 0. Confirmed `run_one()` returns an
  `EvalOutcome(status="SKIPPED", skip_reason="--no-pty", skip_flag_triggered="--no-pty", duration_sec=0.0)`
  and RETURNS before calling `_run_one_spec(...)` (no HomeIsolation.setup, no PTY, no `make verify-sync`).

## Step 5 — Confirm eval count + CLI surface
- `grep -c "^  - id:" installer_sync_drift.yaml` → `1` (single eval; the whole suite's only eval is the one tagged skip).
- `uv run superclaude eval run --help` → exit 0. Confirms `--no-pty` flag exists ("Run without the vendored PTY harness (degrades stdout capture)") and `--suite TEXT` accepts name/stem/path.

## Conclusion
S1 is the only eval, it carries `no_pty: skip`, and `commands.py:1894` short-circuits it to SKIPPED under `--no-pty`. Therefore `superclaude eval run --suite installer_sync_drift --no-pty` exercises NOTHING — `make verify-sync` never runs.
