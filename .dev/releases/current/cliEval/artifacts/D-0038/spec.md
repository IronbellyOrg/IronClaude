# D-0038 — COMP-013 `ClaudeProcessAdapter` (real-subprocess claude reuse)

**Task:** T02.19 (Phase 2)
**Roadmap row:** R-038 (COMP-013)
**Tier:** STANDARD
**Date:** 2026-05-20
**Depends on:** T02.11 (HomeIsolation), T02.16 (PtyDriver)

---

## 1. Why this deliverable exists

The cliEval harness's hard FR-G1 invariant is **"real subprocess only"** — Claude
must be reached via the actual `claude` binary, never via an in-process
`anthropic` SDK client. T02.16 lands `PtyDriver`, the interactive-mode
sibling that spawns `claude` under a pseudo-terminal. T02.19 lands the
**print-mode sibling**, `ClaudeProcessAdapter`, which:

1. Wraps the pre-existing `cli/pipeline/process.py:ClaudeProcess` (subprocess.Popen
   with **separated** stdout/stderr file handles — see step 2 below).
2. Injects `HomeIsolation.env()` so each eval gets a per-eval `$HOME` /
   `$CLAUDE_SESSION_ID` and cannot read or pollute the operator's real Claude
   state directory.
3. Pins child `cwd` at fork time so the spawned `claude` runs in the
   isolated workspace, not in the operator's project directory.

The ruff `flake8-tidy-imports.banned-api` rule registered alongside this
adapter is the **static counterpart** of the runtime discipline: even a
well-intentioned future contributor cannot add an `import anthropic`
under `src/superclaude/` without `ruff` failing CI.

## 2. Files touched

| Path | Change | Purpose |
|------|--------|---------|
| `src/superclaude/cli/eval/claude_process.py` | CREATED | `ClaudeProcessAdapter` + `ClaudeProcessAdapterError`. |
| `src/superclaude/cli/eval/__init__.py` | EDITED | Public surface exports `ClaudeProcessAdapter`, `ClaudeProcessAdapterError`. |
| `pyproject.toml` | EDITED | `[tool.ruff.lint]` gains `TID` ruleset; `[tool.ruff.lint.flake8-tidy-imports.banned-api]` registers the `anthropic` ban with a FR-G1 message pointing at PtyDriver / ClaudeProcessAdapter. |
| `tests/cli/eval/test_claude_process_adapter.py` | CREATED | 13 tests pinning all four AC bullets (see §4). |
| `.dev/releases/current/cliEval/artifacts/D-0038/spec.md` | CREATED | This file. |
| `.dev/releases/current/cliEval/artifacts/D-0038/notes.md` | CREATED | Design-decision notes. |
| `.dev/releases/current/cliEval/artifacts/D-0038/evidence.md` | CREATED | Verification evidence pointers. |
| `.dev/releases/current/cliEval/evidence/T02.19/` | POPULATED | pytest.log, ruff-adapter.log, ruff-probe.log, grep-no-anthropic.log. |

## 3. Adapter contract (canonical)

`ClaudeProcessAdapter` is a thin composition wrapper — it does **not**
subclass `ClaudeProcess`. The public surface, as it appears in
`src/superclaude/cli/eval/__init__.py`:

```python
ClaudeProcessAdapter(
    home: HomeIsolation,
    prompt: str,
    output_file: Path,            # MUST be != error_file
    error_file: Path,             # MUST be != output_file
    cwd: Path | None = None,      # defaults to home.home_path
    extra_env: Mapping[str, str] | None = None,
    *,                            # everything below forwards to ClaudeProcess
    timeout_seconds: int = 1800,
    on_complete: Callable[[int], None] | None = None,
    output_format: str = "stream-json",
    model: str | None = None,
    extra_args: list[str] | None = None,
)

  .build_env()      -> dict[str, str]    # merge order: os.environ → extra_env → HomeIsolation.env()
  .build_command()  -> list[str]         # delegates to ClaudeProcess.build_command()
  .spawn()          -> ClaudeProcess     # os.chdir(cwd) → proc.start() → restore old cwd
  .cwd              : Path
  .home             : HomeIsolation
```

**Key invariants:**

1. `output_file != error_file` is enforced at construction (raises
   `ClaudeProcessAdapterError`). This is the static-shape guarantee that
   stdout/stderr separation cannot be silently collapsed by a caller
   passing the same path twice.
2. `cwd` must exist at construction time; nonexistent path → `ClaudeProcessAdapterError`.
3. `build_env()` merge order is **os.environ → extra_env → HomeIsolation.env()**.
   Isolation keys (e.g. `HOME`, `CLAUDE_SESSION_ID`) **always win** —
   `extra_env` cannot spoof them.
4. `spawn()` pins `cwd` via `os.chdir(cwd)` immediately before
   `ClaudeProcess.start()` (which calls `subprocess.Popen` — Popen inherits
   the parent's cwd at fork), then restores the previous cwd in a
   `finally` block regardless of outcome.
5. The returned object is a `ClaudeProcess` (real subprocess), never a
   mock or any anthropic-SDK wrapper. (AC1 verified by `isinstance`.)

## 4. Acceptance criteria (per phase-2-tasklist.md §T02.19)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| `ClaudeProcessAdapter` spawns real claude with `cwd` pinned, `HomeIsolation.env()` injected, stdout/stderr separated. | ✅ MET | `test_spawn_invokes_real_subprocess_not_anthropic_sdk`, `test_spawn_separates_stdout_and_stderr_to_distinct_files`, `test_spawn_pins_child_cwd_to_adapter_cwd`, `test_spawn_injects_home_isolation_env_into_child` (4 tests, all PASS). |
| `uv run ruff check src/superclaude/cli/eval/` flags any `anthropic` SDK import under that subtree. | ✅ MET | `evidence/T02.19/ruff-probe.log` — synthetic probe flags 3 × TID251. `test_ruff_flags_synthetic_anthropic_import_under_cli_eval` exercises the same path programmatically. |
| No `from anthropic` or `import anthropic` import exists anywhere under `src/superclaude/cli/eval/`. | ✅ MET | `evidence/T02.19/grep-no-anthropic.log` (exit=1, no matches). `test_no_anthropic_imports_anywhere_under_cli_eval` greps the subtree at test time. |
| `TASKLIST_ROOT/artifacts/D-0038/spec.md` documents the adapter and lint rule. | ✅ MET | This file (§3 adapter contract, §5 lint rule). |

## 5. Ruff lint rule (canonical configuration)

Added to `pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "TID"]   # TID added by T02.19
ignore = ["E501"]

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"anthropic".msg = "FR-G1: in-process anthropic SDK imports are banned. Use the real `claude` subprocess via PtyDriver (cli/eval/pty_driver.py) or ClaudeProcessAdapter (cli/eval/claude_process.py)."
"anthropic.AsyncAnthropic".msg = "FR-G1: in-process anthropic SDK imports are banned. Use the real `claude` subprocess via PtyDriver or ClaudeProcessAdapter."
"anthropic.Anthropic".msg = "FR-G1: in-process anthropic SDK imports are banned. Use the real `claude` subprocess via PtyDriver or ClaudeProcessAdapter."
```

The ban is **intentionally repo-wide**, not scoped to `cli/eval/` only.
Rationale: ruff's `banned-api` is a global rule and the AC only requires
that running ruff over `cli/eval/` *flags* such an import — the broader
scope is a strict superset that also defends `cli/pipeline/`,
`pm_agent/`, and every other module from regressing into in-process SDK
usage. Three keys are registered so all three idioms surface (bare
module, `Anthropic`, `AsyncAnthropic`).

## 6. Out of scope for T02.19

- Replacing existing `ClaudeProcess` callers (`cli/pipeline/*`) with the
  adapter — those run outside the eval harness and intentionally do
  **not** apply HomeIsolation.
- Wiring `ClaudeProcessAdapter` into a runner / orchestrator — that lands
  in subsequent tasks (T02.20+ / Phase 3 orchestrator).
- Pre-existing `N818` exception-naming violations in
  `cli/eval/pty_driver.py` and `cli/eval/pty_stream.py` (introduced in
  T02.16/T02.17). Tracked separately; T02.19 adds no new violations
  (`ruff check src/superclaude/cli/eval/claude_process.py` → `All checks
  passed!`).
- Removing the `pexpect` import-fallback / `ptytest` vendoring path —
  unrelated to FR-G1.

## 7. Dependencies and downstream gates unblocked

- **Depends on:** T02.11 (HomeIsolation.env), T02.16 (PtyDriver — pattern
  reference for the print-mode sibling).
- **Unblocks:** Phase 3 orchestrator wiring (the runner can now choose
  PtyDriver for interactive evals, ClaudeProcessAdapter for print-mode
  evals); R-038 closes for M2 roadmap.
- **FR-G1 reinforcement:** the ban-import rule is the static safety net.
  Any contributor who tries to `import anthropic` from a future module
  fails CI before merge.
