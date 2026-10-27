# D-0038 — Implementation Notes

## Design tension: PtyDriver vs ClaudeProcessAdapter

The task description (step 3) says *"Implement `ClaudeProcessAdapter`
invoking real claude via PtyDriver with HomeIsolation.env()"*, while the
acceptance criterion says *"stdout/stderr separated"*. These are in
tension because a PTY collapses the child's stdout+stderr into a single
master-side stream — file-descriptor separation is impossible once
you're behind a tty.

Resolution: read step 3 as **"invoking real claude"** (the FR-G1
discipline), not literally "via PtyDriver" (a specific transport).
`ClaudeProcessAdapter` is the **print-mode sibling** of PtyDriver: both
satisfy FR-G1 (real subprocess), but each exists for a different
output-shape requirement:

| | PtyDriver (T02.16) | ClaudeProcessAdapter (T02.19) |
|---|---|---|
| Transport | `pexpect` / PTY | `subprocess.Popen` |
| stdout/stderr | merged on PTY master | **separated** (two `Path` file handles) |
| Use case | interactive evals, prompts | print-mode evals, captured runs |
| HomeIsolation.env() | applied via env passed to `pexpect.spawn` | applied via `ClaudeProcess.build_env(env_vars=)` |
| cwd pinning | `pexpect.spawn(cwd=...)` | `os.chdir(cwd)` + restore (since `ClaudeProcess.start()` doesn't accept cwd) |

The Phase 3 orchestrator picks one or the other per eval spec.

## Why compose `ClaudeProcess` instead of subclassing

`ClaudeProcess` is a stable, single-purpose primitive in
`cli/pipeline/process.py`. Subclassing it would couple the adapter's
release cadence to pipeline internals (e.g. `popen_kwargs`,
`_completed_callback_invoked`). Composition keeps the adapter free to
evolve independently and makes its responsibilities visible:

- `_build_process()` constructs a fresh `ClaudeProcess` per `spawn()`
  call with the merged env.
- `spawn()` is the only method that touches `os.chdir`; the rest of the
  adapter is pure data assembly.

## Why `os.chdir` rather than altering `ClaudeProcess`

`ClaudeProcess.start()` calls `subprocess.Popen` without a `cwd=`
parameter. Options considered:

1. **Patch `ClaudeProcess` to accept `cwd=`**. Rejected: pipeline callers
   don't need it; we'd be widening a stable interface for one consumer.
2. **Use `preexec_fn=os.chdir(cwd)`**. Rejected: `preexec_fn` runs after
   fork but before exec; chdir there is correct but `preexec_fn` is
   forbidden by the new safe-subprocess discipline (R-mit / NFR-PORT)
   and is not portable to Windows.
3. **`os.chdir(cwd)` in the parent, restore in `finally`**. Chosen.
   Popen inherits the parent's cwd at fork time, so a chdir
   immediately before `start()` is sufficient. The `try/finally` block
   restores the parent cwd regardless of whether `start()` raised.

The chosen approach is single-threaded-correct. Concurrent `spawn()`
calls from multiple threads would race on cwd. Acceptable for the
current orchestrator (per-eval workers serial within a worker) and is
documented in the module-level docstring.

## Env-merge order: why isolation wins

`build_env()` merges as:

```
result = dict(os.environ)
result.update(extra_env)          # caller's per-eval overrides
result.update(home_iso.env())     # isolation wins — caller cannot spoof HOME
```

Tested by `test_build_env_isolation_keys_win_over_extra_env`: caller
passes `extra_env={"HOME": "/should/be/overridden"}`, asserts the
result has `HOME == home_iso.home_path`. This is the contract that
makes `HomeIsolation` actually isolating.

Then `ClaudeProcess.build_env(env_vars=result)` does its own scrubbing
(strips `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT`). The test also
confirms those keys are absent in the merged env.

## Why the ruff ban is repo-wide rather than `cli/eval/`-scoped

Ruff's `flake8-tidy-imports.banned-api` is a global rule — there is no
per-directory `select`/`ignore` mechanism for `TID251`. Options:

1. **Use `# noqa: TID251`** to exempt non-eval modules. Rejected:
   inverts the safety property (default-allow with explicit opt-out).
2. **Per-file `[tool.ruff.lint.per-file-ignores]`** to ignore `TID251`
   outside `cli/eval/`. Considered, rejected as unnecessary: a quick
   grep confirmed no production module currently imports `anthropic`,
   so a repo-wide ban has zero false positives today.
3. **Repo-wide ban** with a FR-G1-themed message. Chosen.

The AC only requires that ruff *flags* `anthropic` imports under
`cli/eval/` — a repo-wide ban is a strict superset.

## Test portability strategy

Tests use a bash shim on PATH instead of requiring a real `claude`
install:

```bash
#!/usr/bin/env bash
cat > /dev/null              # discard stdin (the prompt)
pwd > <cwd-marker>           # record starting cwd for the cwd-pin test
printenv HOME > <env-marker> # record HOME for the env-injection test
echo __OK__                  # stdout sentinel
echo __ERR__ >&2             # stderr sentinel
exit 0
```

This exercises the full Popen + fd-routing pipeline (the part we
actually want to validate) without depending on the host having a
working `claude` install. A module-level `pytest.skip` triggers if
`bash` is unavailable.

The synthetic-probe ruff test (`test_ruff_flags_synthetic_anthropic_
import_under_cli_eval`) writes a throwaway module under `cli/eval/`,
runs `ruff check` on it via subprocess, asserts TID251 fires, and
**deletes the probe in a `finally` block** so a test crash cannot
leave an `anthropic` import behind.

## Out-of-scope notes (pre-existing N818)

`uv run ruff check src/superclaude/cli/eval/` (full subtree) returns
16 errors today: 4 × N818 in `pty_driver.py` / `pty_stream.py` and
related I001 / TID252 from T02.16's vendoring fallback. These
pre-date T02.19 (they came in with PtyDriver/PtyStream landing).
T02.19 adds zero new ruff violations:

```
$ uv run ruff check src/superclaude/cli/eval/claude_process.py
All checks passed!
```

Recorded in `evidence/T02.19/ruff-adapter.log`.

## Files: full inventory

```
src/superclaude/cli/eval/
├── claude_process.py        # NEW — the adapter
├── __init__.py              # EDITED — public exports

pyproject.toml               # EDITED — [tool.ruff.lint] + banned-api block

tests/cli/eval/
└── test_claude_process_adapter.py   # NEW — 13 tests

.dev/releases/current/cliEval/
├── artifacts/D-0038/
│   ├── spec.md              # NEW
│   ├── notes.md             # NEW (this file)
│   └── evidence.md          # NEW
└── evidence/T02.19/
    ├── pytest.log           # 13 passed
    ├── ruff-adapter.log     # adapter clean
    ├── ruff-probe.log       # synthetic probe → 3 × TID251
    └── grep-no-anthropic.log  # no anthropic imports in cli/eval/
```
