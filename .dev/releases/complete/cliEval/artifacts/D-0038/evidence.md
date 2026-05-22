# D-0038 — Verification Evidence

**Task:** T02.19
**Date:** 2026-05-20
**Verifier:** automated (pytest + ruff)

---

## Evidence index

| File | What it proves | Location |
|------|---------------|----------|
| `pytest.log` | All 13 adapter-contract tests pass (4 spawn-mode tests + 9 unit/lint tests). | `.dev/releases/current/cliEval/evidence/T02.19/pytest.log` |
| `ruff-adapter.log` | The adapter module introduces **zero** new ruff violations. | `.dev/releases/current/cliEval/evidence/T02.19/ruff-adapter.log` |
| `ruff-probe.log` | A synthetic `import anthropic` line under `cli/eval/` produces **3 × TID251** ruff errors, proving the ban is wired and active. | `.dev/releases/current/cliEval/evidence/T02.19/ruff-probe.log` |
| `grep-no-anthropic.log` | `grep -rE '^(from anthropic|import anthropic)' src/superclaude/cli/eval/` exits 1 (no matches). | `.dev/releases/current/cliEval/evidence/T02.19/grep-no-anthropic.log` |

## Acceptance-criterion ↔ evidence map

### AC1 — `ClaudeProcessAdapter` spawns real claude with `cwd` pinned, `HomeIsolation.env()` injected, stdout/stderr separated.

`pytest.log` shows the four spawn-mode tests passing:

```
tests/cli/eval/test_claude_process_adapter.py::test_spawn_invokes_real_subprocess_not_anthropic_sdk PASSED
tests/cli/eval/test_claude_process_adapter.py::test_spawn_separates_stdout_and_stderr_to_distinct_files PASSED
tests/cli/eval/test_claude_process_adapter.py::test_spawn_pins_child_cwd_to_adapter_cwd PASSED
tests/cli/eval/test_claude_process_adapter.py::test_spawn_injects_home_isolation_env_into_child PASSED
```

Each test maps to one AC1 sub-claim:

- *"spawns real claude"* → `test_spawn_invokes_real_subprocess_not_anthropic_sdk`
  asserts `isinstance(adapter.spawn(), ClaudeProcess)` — no anthropic-SDK
  wrapper anywhere in the return path.
- *"cwd pinned"* → `test_spawn_pins_child_cwd_to_adapter_cwd` reads back
  the bash shim's recorded cwd from a marker file and compares against
  `adapter.cwd.resolve()` (symlink-tolerant for macOS).
- *"`HomeIsolation.env()` injected"* → `test_spawn_injects_home_isolation_
  env_into_child` reads back `printenv HOME` from a marker file written
  by the shim and asserts it equals `home_iso.home_path.resolve()`.
- *"stdout/stderr separated"* → `test_spawn_separates_stdout_and_stderr_
  to_distinct_files` confirms `__OK__` is in `output_file` only,
  `__ERR__` in `error_file` only, with no cross-leak.

The merge-order invariant is additionally pinned by
`test_build_env_isolation_keys_win_over_extra_env` (`extra_env={"HOME":
"/should/be/overridden"}` → final `env["HOME"]` is `home_iso.home_path`).

### AC2 — `uv run ruff check src/superclaude/cli/eval/` flags any `anthropic` SDK import under that subtree.

`ruff-probe.log` (truncated for readability — full file in evidence/):

```
TID251 `anthropic` is banned: FR-G1: in-process anthropic SDK imports are banned...
 --> src/superclaude/cli/eval/_probe_anthropic_ban.py:2:8
TID251 `anthropic` is banned: FR-G1: in-process anthropic SDK imports are banned...
 --> src/superclaude/cli/eval/_probe_anthropic_ban.py:3:1
TID251 `anthropic.Anthropic` is banned: FR-G1: in-process anthropic SDK imports are banned...
 --> src/superclaude/cli/eval/_probe_anthropic_ban.py:3:23
Found 3 errors.
exit=1
```

The probe file was created, ruff-checked, and **deleted** by the same
shell pipeline that wrote the log — the synthetic file no longer
exists in the working tree. The pytest equivalent
(`test_ruff_flags_synthetic_anthropic_import_under_cli_eval`) does
the same dance inside a `try/finally` so a test crash cannot leave
the probe behind.

### AC3 — No `from anthropic` or `import anthropic` import exists anywhere under `src/superclaude/cli/eval/`.

`grep-no-anthropic.log`:

```
exit=1
```

`grep -rE '^(from anthropic|import anthropic)' src/superclaude/cli/eval/`
returns no matches (exit code 1). The pytest equivalent
(`test_no_anthropic_imports_anywhere_under_cli_eval`) runs the same
grep at test time and walks `os.walk` for belt-and-suspenders coverage.

### AC4 — `TASKLIST_ROOT/artifacts/D-0038/spec.md` documents the adapter and lint rule.

`.dev/releases/current/cliEval/artifacts/D-0038/spec.md` exists and
contains:

- §3 Adapter contract (signature, invariants, public surface).
- §5 Ruff lint rule (canonical `pyproject.toml` block).

## Reproduction commands

```bash
# Run the full T02.19 test suite
uv run pytest tests/cli/eval/test_claude_process_adapter.py -v

# Confirm the adapter module is ruff-clean (zero new violations)
uv run ruff check src/superclaude/cli/eval/claude_process.py

# Confirm no anthropic imports anywhere under cli/eval/
grep -rE '^(from anthropic|import anthropic)' src/superclaude/cli/eval/ ; echo "exit=$?"
# expected: exit=1 (no matches)

# Reproduce the synthetic-probe demo
cat > src/superclaude/cli/eval/_probe.py <<'EOF'
import anthropic  # noqa: F401
from anthropic import Anthropic  # noqa: F401
_ = anthropic; _ = Anthropic
EOF
uv run ruff check src/superclaude/cli/eval/_probe.py    # expected: 3 × TID251
rm -f src/superclaude/cli/eval/_probe.py
```

## Test session summary (pytest)

```
13 passed in 0.21s
```

Full log: `.dev/releases/current/cliEval/evidence/T02.19/pytest.log`.
