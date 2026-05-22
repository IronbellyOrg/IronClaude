# D-0033 — Spec: NFR-ISO2 atomic-setup wrapper

**Task:** T02.13 — Wrap `HomeIsolation.setup()` with atomic try/except contract.
**Component:** COMP-006 `HomeIsolation` (`src/superclaude/cli/eval/isolation.py`).
**Requirement:** NFR-ISO2 (atomic per-eval HOME with `setup_failed` forensic tag).
**Adjacent invariants:** FR-ISO2 (`containment_guard`, D-0029); NFR-SEC3 (no FS writes under refused HOMEs, D-0031).

## 1. Scope

The atomic-setup wrapper sits inside `HomeIsolation.setup()` between the
`tempfile.mkdtemp` call and the `return home` line. Its job is to make
`setup()` an **all-or-nothing** primitive at the eval level:

* On success — return the per-eval HOME, slot populated, no
  `setup_failed` tag.
* On failure — the per-eval HOME is preserved on disk, the
  `_home_path` slot stays populated (so `teardown(keep=True)` can be
  called without re-resolving), the original exception propagates
  unchanged, and (conditionally) a `setup_failed` artifact tag is
  dropped at `<home>/.eval-meta/setup_failed` so a downstream
  `EvalRunner` (T03.x) can bucket the eval as **ERRORED**, not FAIL.

## 2. Failure-preservation contract

| Concern                              | Behavior                                                                                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Per-eval HOME on disk after failure  | Preserved as a directory under `home_root`.                                                                                                |
| `_home_path` slot after failure      | Populated with the partial HOME so `teardown(keep=True)` can preserve it without a re-resolve.                                             |
| Exception type after failure         | Propagated **verbatim**. The wrapper never re-wraps, never re-classifies.                                                                  |
| `setup_failed` tag for non-containment failures | Written at `<home>/.eval-meta/setup_failed`. Line 1 = exception class name; body = `traceback.format_exception` output.          |
| `setup_failed` tag for `HomeContainmentViolation` | **Not written.** See §3.                                                                                                          |
| Tag-write helper raises              | Secondary exception is swallowed; the **original** exception propagates. Best-effort by design.                                            |
| Slot after successful `setup()`      | Populated with the freshly-created HOME (unchanged from the COMP-006 contract).                                                            |
| Tag after successful `setup()`       | Absent.                                                                                                                                    |

## 3. Tag-write asymmetry — the NFR-SEC3 carve-out

`HomeContainmentViolation` is the **deliberate** exception to the
tag-write rule. The carve-out exists because writing under a HOME the
FR-ISO2 guard just refused can land under real `~/.claude/`:

* When `scratch_root` is (or `Path.resolve`-s into) real
  `~/.claude/`, the scratch-root allowlist check fails AFTER
  `mkdtemp` has already created `<real-~/.claude>/<eval_id>-XXXX/`.
  Writing the tag now drops a file under real `~/.claude/`.
* When the `mkdtemp` result itself contains a symlinked component
  that resolves outside `scratch_root` (NFR-SEC3 attack matrix #3),
  the per-eval HOME path points outside the allowlisted scratch root.
  Writing the tag now drops a file outside policy.

Both of these are explicitly the behaviors `test_hard_guard_real_home.py`
(D-0031) pins as **forbidden** — the NFR-SEC3 invariant is "the per-eval
HOME directory contains zero post-`mkdtemp` writes when the guard
refuses." T02.13 honors that invariant by routing containment
violations through `raise` without the tag-write branch.

The `HomeContainmentViolation` exception itself carries the full
forensic payload — `check`, `home_path`, `scratch_root`, `eval_id`,
`detail` — so a reporter can bucket the eval as ERRORED without the
tag. The tag is redundant for this case; the exception is the
structured signal.

## 4. Wrapper structure (final)

```python
home = Path(
    tempfile.mkdtemp(prefix=f"{self.eval_id}-", dir=str(self.home_root))
)
object.__setattr__(self, "_home_path", home)

try:
    containment_guard(
        home_path=home,
        scratch_root=self.home_root,
        eval_id=self.eval_id,
        config=config,
    )
except HomeContainmentViolation:
    # NFR-SEC3: no FS writes under a refused HOME.
    raise
except Exception as exc:
    try:
        _write_setup_failed_tag(home, exc)
    except Exception:
        pass
    raise
return home
```

Today the only exception source inside the wrapper is
`containment_guard`. T02.14 (hook adapter, D-0034) will add a second
post-containment call site inside the wrapper. Any post-containment
exception lands in the `except Exception` branch and produces a tag.

## 5. Constants & public surface

| Symbol                          | Purpose                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `SETUP_FAILED_TAG_RELPATH`      | `".eval-meta/setup_failed"` — exported in `superclaude.cli.eval.__all__` so reporters can locate it.   |
| `_write_setup_failed_tag(home, exc)` | Private helper writing `<home>/.eval-meta/setup_failed` with class name + traceback. Idempotent.   |

## 6. Acceptance-criteria mapping

| AC bullet (phase-2-tasklist.md L597-L644)                                                                | Test(s)                                                                                            |
| -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Inducing an exception inside `HomeIsolation.setup()` after mkdtemp preserves the per-eval HOME on disk   | `TestPartialHomePreservedOnException` (3 tests, both containment & injected exception paths)       |
| Preserved HOME contains a `setup_failed` artifact tag file with the exception class name                 | `TestSetupFailedTagWritten` (5 tests; containment-exempt case asserted in `TestContainmentViolationDoesNotWriteTag`) |
| Eval status is set to ERRORED (not FAIL) on setup exception (verified by mock EvalRunner)                | `TestMockEvalRunnerBucketsAsErrored` (3 tests)                                                     |
| `TASKLIST_ROOT/artifacts/D-0033/spec.md` records the failure-preservation contract                       | This file.                                                                                         |

## 7. Cross-deliverable links

* `artifacts/D-0029/spec.md` — `containment_guard` contract (FR-ISO2).
* `artifacts/D-0031/notes.md` — NFR-SEC3 invariants (`test_hard_guard_real_home.py`).
* `artifacts/D-0032/spec.md` — COMP-006 integrated contract (T02.11).
* `artifacts/D-0034/*` (pending — T02.14) — hook adapter, the second
  post-containment call site that will use the wrapper's tag branch.
