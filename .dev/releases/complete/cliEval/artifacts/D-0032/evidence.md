# D-0032 — Evidence (Task T02.11)

## Acceptance-criteria check

| Criterion | Result |
|---|---|
| `HomeIsolation` exposes the 4 methods named in COMP-006 (`setup`, `env`, `teardown(keep)`, `state_path(suffix)`) | PASS — `TestComp006MethodSurface` (5 tests, signature introspection + callability) |
| `state_path(suffix)` returns paths exclusively under the per-eval HOME (`is_relative_to(home_root)`) | PASS — `TestStatePathIsAnchoredUnderHomeRoot::test_state_path_is_relative_to_home_root` (+ 5 sibling tests covering `home_path`, nested suffixes, absolute/.. rejection, pre-setup `RuntimeError`) |
| `teardown(keep=True)` preserves the HOME; `teardown(keep=False)` removes it | PASS — `TestTeardownKeepFlag` (7 tests covering preserve, remove, slot lifecycle, no-op, post-teardown errors) |
| `D-0032/spec.md` records the integrated component contract | PASS — `.dev/releases/current/cliEval/artifacts/D-0032/spec.md` |

## Test results

`uv run pytest tests/cli/eval/test_home_isolation.py -v` →
**27 passed in 0.15s** — see `evidence/T02.11/pytest-T02.11.log`.

Phase-2 isolation suite cumulative (`test_home_isolation_extend.py
test_path_containment.py test_defense_in_depth.py
test_hard_guard_real_home.py test_home_isolation.py`) →
**137 passed in 0.32s** — no regression upstream.

## Manual validation

> Build HomeIsolation, run setup -> env -> state_path -> teardown(keep=False) and verify state.

Equivalent test:
`TestIntegratedLifecycle::test_full_lifecycle_round_trip`
(`tests/cli/eval/test_home_isolation.py`). The test constructs
`HomeIsolation(eval_id="E1", home_root=<scratch>, session_id="sess-rt-001",
time_offset_sec=0)`, then asserts in sequence:

1. `setup(config=<permissive>)` returns a directory whose parent is
   the declared scratch root.
2. `env()` returns exactly `{HOME, CLAUDE_SESSION_ID}` for
   `time_offset_sec=0`.
3. `state_path(".eval-meta/started")` is `is_relative_to(home_path)`,
   the file written through it round-trips on disk.
4. `teardown(keep=False)` removes the directory and clears
   `is_set_up`.

## Files changed / added

* `tests/cli/eval/test_home_isolation.py` — new module (27 tests
  across 7 test classes).
* `.dev/releases/current/cliEval/artifacts/D-0032/{spec,notes,evidence}.md`
  — this deliverable's artifacts.
* `.dev/releases/current/cliEval/evidence/T02.11/pytest-T02.11.log` —
  captured pytest output.

No source code under `src/superclaude/` was modified — COMP-006
finalization is a test-only deliverable; see `notes.md` for rationale.

## Linkable artifacts

* Test module: `tests/cli/eval/test_home_isolation.py`
* Pytest log: `.dev/releases/current/cliEval/evidence/T02.11/pytest-T02.11.log`
* Spec: `.dev/releases/current/cliEval/artifacts/D-0032/spec.md`
* Notes: `.dev/releases/current/cliEval/artifacts/D-0032/notes.md`
