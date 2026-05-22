# D-0033 — Evidence (Task T02.13)

## Acceptance-criteria check

| Criterion | Result |
|---|---|
| Inducing an exception inside `HomeIsolation.setup()` after mkdtemp preserves the per-eval HOME on disk | PASS — `TestPartialHomePreservedOnException` (3 tests covering both `HomeContainmentViolation` and monkeypatched non-containment paths) |
| Preserved HOME contains a `setup_failed` artifact tag file with the exception class name | PASS — `TestSetupFailedTagWritten` (5 tests: canonical relpath, first-line class name, custom exception class capture, traceback body, relative-path containment) |
| `HomeContainmentViolation` is exempt from tag write — NFR-SEC3 carve-out | PASS — `TestContainmentViolationDoesNotWriteTag` (3 tests: no tag, no `.eval-meta` dir, forensic payload on the exception itself) |
| Eval status is set to ERRORED (not FAIL) on setup exception (verified by mock EvalRunner) | PASS — `TestMockEvalRunnerBucketsAsErrored` (3 tests: containment ERRORED without tag, injected exception ERRORED with tag, normal-path FAIL) |
| Tag write is best-effort (secondary failures don't mask the original) | PASS — `TestTagWriteBestEffort::test_secondary_tag_failure_does_not_mask_original` |
| `teardown(keep=True)` after failure preserves the partial HOME (and tag, if any) | PASS — `TestTeardownKeepTruePreservesPartialHome` (3 tests) |
| `TASKLIST_ROOT/artifacts/D-0033/spec.md` records the failure-preservation contract | PASS — `.dev/releases/current/cliEval/artifacts/D-0033/spec.md` |

## Test results

`uv run pytest tests/cli/eval/test_atomic_setup.py -v` →
**19 passed in 0.14s** — see `evidence/T02.13/pytest-T02.13.log`.

Cumulative phase-2 isolation regression
(`test_home_isolation_extend.py test_path_containment.py
test_defense_in_depth.py test_hard_guard_real_home.py
test_home_isolation.py test_atomic_setup.py`) →
**156 passed in 0.35s** — no NFR-SEC3 regression (was 3 failed / 148
passed on the first cut of the wrapper; see `notes.md`).

Full `tests/cli/eval/` directory regression →
**520 passed in 1.13s**.

## Manual validation

> Wrap setup() body in try/except after mkdtemp; on exception force keep=True and write `setup_failed` tag with exception class + traceback.

Equivalent tests:

* `TestTeardownKeepTruePreservesPartialHome::test_teardown_keep_true_preserves_home_and_tag_after_injected_exception`
  drives the full round-trip on the tag-write branch:
  1. Monkeypatches `containment_guard` to raise `RuntimeError`.
  2. Calls `iso.setup(config=permissive_config)` and asserts
     `RuntimeError` propagates verbatim.
  3. Records `home = iso.home_path` BEFORE teardown clears the slot.
  4. Calls `iso.teardown(keep=True)` and asserts both the HOME and
     the tag are still on disk.
  5. Reads the tag and confirms line 1 is `"RuntimeError"`.

* `TestContainmentViolationDoesNotWriteTag::test_no_tag_after_containment_violation`
  drives the NFR-SEC3 carve-out:
  1. Builds an `EvalConfig` with an empty allowlist.
  2. Calls `iso.setup(config=restrictive_config)` and asserts
     `HomeContainmentViolation` is raised.
  3. Confirms `<home>/.eval-meta/setup_failed` does **not** exist.
  4. The companion `test_eval_meta_dir_not_created_after_containment_violation`
     additionally asserts the parent `.eval-meta` dir was never
     created — the per-eval HOME is the empty directory NFR-SEC3
     requires.

## Files changed / added

| File | Change |
|------|--------|
| `src/superclaude/cli/eval/isolation.py` | Added `SETUP_FAILED_TAG_RELPATH` constant, `_write_setup_failed_tag(home_path, exc)` private helper, NFR-ISO2 atomic-setup wrapper inside `HomeIsolation.setup()` with `HomeContainmentViolation` carve-out, and the NFR-ISO2 docstring section. Imported `traceback`. |
| `src/superclaude/cli/eval/__init__.py` | Re-exported `SETUP_FAILED_TAG_RELPATH`. |
| `tests/cli/eval/test_atomic_setup.py` | New test module — 19 tests across 7 classes. |
| `.dev/releases/current/cliEval/artifacts/D-0033/{spec,notes,evidence}.md` | This deliverable's artifacts. |
| `.dev/releases/current/cliEval/evidence/T02.13/pytest-T02.13.log` | Captured pytest output. |

## Regression-loop forensics

The cumulative regression on the first cut of the wrapper caught the
NFR-SEC3 conflict — the wrapper wrote `setup_failed` under refused
HOMEs that resolved into real `~/.claude/`. The failure surfaced in
`test_hard_guard_real_home.py` (D-0031) with the diagnostic:

> Leaked per-eval HOME /config/.claude/HardguardevalT0210-<rand> is
> not empty after refused symlink-scratch setup; the guard ran AFTER
> a child write — NFR-SEC3 invariant violated.

Resolution: split the wrapper's `except` into a containment branch
(`raise`, no tag) and a non-containment branch (best-effort tag,
re-raise). `notes.md` records the design rationale.

## Linkable artifacts

* Source module: `src/superclaude/cli/eval/isolation.py`
* Test module: `tests/cli/eval/test_atomic_setup.py`
* Pytest log: `.dev/releases/current/cliEval/evidence/T02.13/pytest-T02.13.log`
* Spec: `.dev/releases/current/cliEval/artifacts/D-0033/spec.md`
* Notes: `.dev/releases/current/cliEval/artifacts/D-0033/notes.md`
