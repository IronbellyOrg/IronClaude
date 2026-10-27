# D-0072 — Implementation notes

## Why T04.10 lands as a documentation + test-coverage task

The `eval_run` Click command body and its eight module-private helpers
were materialised across the M2/M3 batch alongside the dependencies
T04.10 cites: T03.15 `RunOrchestrator`, T03.19 `DiskBudgetPoller`,
T04.09 `eval_group` registration, T04.15 `coverage_gate` (FR-G5), and
T04.16 `real.yaml` DOC-OQ3 / R-077 exclusion-set scaffolding.

What T04.10 brings to that body is the **acceptance harness**:

1. `tests/cli/eval/test_eval_run.py` — 16 cases pinning the four
   phase-4 AC bullets at the Click `CliRunner` surface.
2. `D-0072/spec.md` — the flag-to-component wiring table, exit-code
   contract, and pipeline ordering. Operators reading
   `commands.py:1542+` get an authoritative narrative of why each
   line exists; future contributors editing the body have a contract
   to keep stable.
3. `D-0072/evidence.md` — pytest + `--help` captures so the smoke
   test can be reproduced from this directory without re-running.

## Decisions

### 1. Use the real orchestrator for end-to-end tests, not a fake

The end-to-end ("AC bullet 3") tests run the *real* `RunOrchestrator`
+ `Reporter` + `DiskBudgetPoller` against the *real* `real.yaml`
suite. They rely on the `--no-pty` short-circuit (DOC-OQ3 /
`run_one` closure at `commands.py:1839`) to keep every eval `SKIPPED`
without invoking the M5 PTY harness. Rationale: exercising the
production path under the documented escape hatch keeps T04.10
covering the wires that ship, not a mock surface.

### 2. Patch RunOrchestrator on the commands module, not the import path

For the clamp tests we monkeypatch `commands.RunOrchestrator` (the
module-local binding) rather than the import path. Two reasons:

* Python's `from .orchestrator import RunOrchestrator` binds the
  class as a module attribute; patching the attribute is what the
  eval_run body actually reads.
* The recording stand-in re-exports `MIN_PARALLEL` / `MAX_PARALLEL`
  from the real class so the clamp branch in `commands.py:1681–1684`
  reads the same band. A future design-spec re-tune flows through
  the real class automatically.

### 3. CliRunner without `mix_stderr`

Click 8.3 dropped the `mix_stderr` kwarg. The tests use a bare
`CliRunner()`; stderr is accessible via `result.stderr` on Click 8.3+
and remains separate from `result.stdout` by default. This matches
the `test_coverage_gate_integration.py` convention.

### 4. `clean_claude_home` fixture for the FR-G5 coverage gate

`eval_run` invokes the FR-G5 hook-matcher coverage gate at the top of
the run (`commands.py:1794`). On a dev host with `mcp__auggie__.*`
matchers configured, the gate FAILS because `real.yaml`'s E1 has no
`inputs:` yet (T05.02 deferred), so no eval covers any matcher.
Pointing `Path.home()` at a `tmp_path` empties the matcher set and
makes the gate pass — without monkeypatching the gate itself, which
would defeat its purpose.

### 5. Defer the `--no-mcp` / `--keep-home` per-flag observations

The current `commands.py:1814` constructs the `CapabilityGates` with
the skip-flag tuple but does NOT call `check_all()` — that's the
doctor subcommand's job. There's no observable side-effect to assert
on at this layer (the gate object is discarded with `del _gates` at
line 1815). The flags' presence is pinned by the `--help` test;
their plumbing-level behaviour is owned by T03.18 (capabilities) and
T03.14 (HomeIsolation respectively).

## Deferred follow-ups

* **M5/M6 PTY wiring** — replace `_NullLifecycleExecutor` with the
  real `ClaudeProcessAdapter` + `PtyDriver`. At that point the
  end-to-end test can be lifted to a real Claude-driven invocation
  without `--no-pty` and `test_single_command.py` un-skips.
* **Expects resolver** — `_run_one_spec` currently passes an empty
  `expect_callables=()` to `EvalRunner` so PASS is determined purely
  by the executor's exit code (= 0 for the null path). The manifest
  `expects:` → callable mapping lands in a follow-up task; until
  then synthetic suites with non-PTY expects fields ignore them.
* **`--no-mcp` integration test** — pinning the gate's
  `skip-by-flag` accounting belongs with the capabilities subsystem
  (T03.18) once the gate emits a structured artifact. The current
  surface only mutates the gate instance, which is dropped.

## Risk notes

* **Coverage-gate dev-host coupling** — without `clean_claude_home`
  any dev host that has a populated `~/.claude/settings.json` will
  see the end-to-end tests fail on the FR-G5 gate (exit 2 + roster).
  Future contributors must keep that fixture wired into every
  end-to-end case. The fixture is local to this test file, not
  shared, to keep the coupling explicit.
* **CliRunner clock determinism** — the `_RecordingOrchestrator`
  returns `tuple()` so the run summary records 0 outcomes. This is
  benign for the clamp tests (they only inspect `last_parallel`) but
  would crater any future assertion that the summary's
  `expanded_n_prime` equals the spec count. If such an assertion is
  added, mint a separate stand-in that returns one outcome per spec.
* **`real.yaml` row count drift** — `test_run_no_pty_full_suite_skips_every_eval`
  asserts `n_prime >= 15`. The current manifest expands to 17 rows
  (E2 parameterised 3× × 1 plus E1, E3-E15). If T05.02 adds more
  parameterisations the threshold still holds; if it removes E2's
  parameterise block the assertion still passes (15 ≥ 15).
