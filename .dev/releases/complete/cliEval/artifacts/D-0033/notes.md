# D-0033 — Implementation notes

## Why the wrapper branches on `HomeContainmentViolation`

The first cut of T02.13 wrapped `containment_guard` with a single
`except Exception` that wrote the tag for **every** post-`mkdtemp`
exception. The cumulative phase-2 isolation regression caught the
defect immediately:

```
FAILED tests/cli/eval/test_hard_guard_real_home.py::
  test_per_eval_home_is_empty_when_setup_refuses
FAILED tests/cli/eval/test_hard_guard_real_home.py::
  test_setup_refuses_when_per_eval_home_symlinks_into_real_dot_claude
FAILED tests/cli/eval/test_hard_guard_real_home.py::
  test_setup_refuses_when_scratch_root_symlinks_into_real_dot_claude
3 failed, 148 passed
```

All three failures cited the same invariant: the leaked per-eval HOME
under real `~/.claude/` was no longer empty after a refused setup,
because the wrapper wrote `setup_failed` under it.

The architectural tension is real: T02.13 wants the tag for forensics;
T02.10 forbids any write under refused HOMEs. The resolution is the
asymmetric wrapper documented in `spec.md` §3 — containment violations
get a `raise` (no tag), non-containment exceptions get a `raise` after
a best-effort tag write.

The forensic information is not lost for the containment case:
`HomeContainmentViolation` already carries `check`, `home_path`,
`scratch_root`, `eval_id`, and `detail`. The reporter sees the
exception object directly and can bucket the eval as ERRORED without
needing the disk tag at all. The tag is only needed for **harness
bugs** — exceptions that would otherwise leave the operator with a
naked stack trace and no on-disk crumb.

## Why the tag is best-effort

The per-eval HOME may have been made unwritable by a future hardening
step (e.g., `chmod 0500` after hook deploy). A tag-write failure in
that case is non-fatal — the orchestrator still has the original
exception in hand. The wrapper swallows secondary exceptions so the
caller's `except` block sees the underlying setup failure, not the
tag-write `OSError`.

`TestTagWriteBestEffort::test_secondary_tag_failure_does_not_mask_original`
pins the contract by monkeypatching `_write_setup_failed_tag` to raise
`OSError` and asserting the original `RuntimeError` surfaces.

## Test seam — monkeypatched `containment_guard`

Phase-2 isolation tests deliberately reach into `containment_guard`
via `monkeypatch.setattr(iso_module, "containment_guard", ...)` to
inject synthetic exceptions inside the wrapper without smuggling a
real FR-ISO2 violation. The seam is acceptable because:

1. The wrapper is module-local; the monkeypatch targets the **name**
   `containment_guard` inside `isolation.py`, not a global registry.
2. The synthetic exception types (`RuntimeError`, `SyntheticBug`) are
   chosen to be `Exception` subclasses but **not**
   `HomeContainmentViolation` subclasses, so the wrapper takes the
   tag-write branch deterministically.
3. The injected behavior models the **future** T02.14 hook-deploy call
   site — that call lands inside the same wrapper and produces the
   same tag for any failure.

A cleaner long-term alternative would be a private
`_post_containment_setup_hook` no-op method that lives inside the
wrapper and can be subclassed/mocked. That refactor is deferred to
T02.14 (where the second call site lands) so this deliverable does
not invent surface that has no production consumer yet.

## What deliberately does NOT live in this module

* **Subprocess wiring** — owned by T03.x EvalRunner (Phase 3). The
  mock `_MockEvalRunner` in the test module is a stub for that
  consumer.
* **Hook deploy** — owned by T02.14 / D-0034. T02.13 reserves the
  wrapper's `except Exception` branch for that future call site but
  does not implement it.
* **`setup_failed` tag forensic schema** — only the first line
  (exception class name) is pinned by AC. The traceback body is
  human-readable, not machine-parsed.
* **Real `~/.claude/` refusal tests** — owned by T02.10 / D-0031. The
  T02.13 wrapper's `HomeContainmentViolation` carve-out is what keeps
  those tests passing; the carve-out itself is exercised by
  `TestContainmentViolationDoesNotWriteTag`.

## Decisions

1. **Asymmetric wrapper** — `HomeContainmentViolation` branch
   re-raises without tag-write; all other `Exception`s take the
   tag-write branch. Justified by NFR-SEC3 (see `spec.md` §3).
2. **Slot-after-failure invariant kept from T02.07** — the
   `_home_path` slot stays populated on any setup exception so
   `teardown(keep=True)` works without re-resolving from disk. The
   T02.07 implementation already handled this; T02.13 only confirms
   the invariant survives the new wrapper.
3. **No exception re-wrapping** — the wrapper does not introduce
   a `SetupError` umbrella type. Callers branch on the original
   exception class. `HomeContainmentViolation` stays the loudly
   typed surface for containment-related refusals.
4. **Constant exported** — `SETUP_FAILED_TAG_RELPATH` is exported
   from `superclaude.cli.eval.__all__` so the future `EvalRunner` and
   forensics tooling can locate the tag without re-deriving the path.
