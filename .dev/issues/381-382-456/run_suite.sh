#!/usr/bin/env bash
# Runs the CI commands of .github/workflows/test.yml (test, swarm lanes, lint steps) in this worktree.
# Usage: run_suite.sh <label>   (label = baseline | after). Output goes to .dev/issues/381-382-456/runs/<label>/.
# Differences from CI, on purpose: no --maxfail (see every failure); a temporary HOME so nothing touches
# the real one; the local interpreter (see python.txt) instead of CI's Python 3.10.
set -u
LABEL="${1:?label}"
ROOT="$(git rev-parse --show-toplevel)"
OUT="$ROOT/.dev/issues/381-382-456/runs/$LABEL"
mkdir -p "$OUT"
export HOME="$(mktemp -d)"
export PATH="$ROOT/.venv/bin:$PATH"
cd "$ROOT"
{ git rev-parse HEAD; git status --short | head -50; "$ROOT/.venv/bin/python" -V; } > "$OUT/source-state.txt" 2>&1

run() { # name, command...
  local name="$1"; shift
  "$@" > "$OUT/$name.log" 2>&1
  echo "$name exit=$?" | tee -a "$OUT/exits.txt"
}
: > "$OUT/exits.txt"
run sync-dev make sync-dev
run test pytest -v --tb=short -n auto -p no:cacheprovider --ignore=tests/cli/test_verify_sync_hooks.py -rA
run swarm-imm pytest tests/swarm/ -m imm -v --tb=short -p no:cacheprovider -rA
run swarm-inv pytest tests/swarm/ -m inv -v --tb=short -p no:cacheprovider -rA
run ruff-check ruff check src/ tests/
run ruff-format ruff format --check src/ tests/
run plugin-loaded bash -c 'pytest --trace-config 2>&1 | grep -q superclaude'
run fixtures bash -c 'pytest --fixtures | grep -E "(confidence_checker|self_check_protocol|reflexion_pattern|token_budget|pm_context)"'
run verify-deps env UV_PROJECT_ENVIRONMENT="$(mktemp -d)/verify-deps-venv" make verify-deps
run verify-sync make verify-sync
run lint-architecture make lint-architecture
run verify-sync-hooks pytest -v --tb=short -p no:cacheprovider -rA tests/cli/test_verify_sync_hooks.py
run git-diff-check git diff --check
echo done > "$OUT/DONE"
