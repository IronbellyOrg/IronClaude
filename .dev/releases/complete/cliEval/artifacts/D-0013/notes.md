# D-0013 — implementation notes

## Decisions made during build

1. **Module location.** Added `ExpectResult` to the existing `src/superclaude/cli/eval/models.py` rather than a sibling module. T01.16 (`ExpectFailure`) lands in the same file per its task spec, so colocating the two avoids a circular import dance later and matches the "models" module purpose declared in the docstring.

2. **Forward reference for `ExpectFailure`.** T01.15 depends on T01.16 per the phase-tasklist dependency map, but the user explicitly requested T01.15 in isolation. Resolution: declare the field as `Optional["ExpectFailure"]` (string forward annotation) — `from __future__ import annotations` (already in the module) makes the annotation a runtime string, so the module imports cleanly today. T01.16 will add the concrete class to the same module and the annotation resolves automatically. No production-code edit needed when T01.16 lands.

3. **`details` defaults to `field(default_factory=dict)`.** `Mapping[str, Any]` is the static type so callers can pass any mapping-shaped payload (dict, MappingProxyType, etc.). `default_factory=dict` gives each instance its own empty mapping — verified by `test_expect_result_details_default_is_independent_per_instance` so a shared mutable default cannot leak between results.

4. **`to_dict()` delegates to `dataclasses.asdict`.** Two reasons: (a) DM-009 explicitly names `dataclasses.asdict` as the serialisation surface in the task acceptance criteria, and (b) `asdict` recursively unwraps nested dataclasses, so once T01.16's `ExpectFailure` is set on `failure`, the Reporter (COMP-008) gets a plain dict without writing bespoke handling. Locked by `test_expect_result_asdict_unwraps_nested_dataclass_failure`.

5. **`duration_sec: float = 0.0`.** Acceptance criterion uses `duration_sec` (not the DM-009 short name `duration`); chose `float` so sub-millisecond assertion timings are not truncated. The default `0.0` lets unit tests construct passing results without supplying timing data.

6. **`failure` is Optional with no required-when-failed coupling.** DM-009 wording is explicit: "failure is Optional per DM-009 (no required-when-failed coupling)". Implementation matches: `passed=False, failure=None` constructs successfully (`test_expect_result_failing_without_failure_attached_is_allowed`). The Reporter is responsible for treating absence-of-failure on a failing result as "no rich diff available", not as a contract violation.

7. **Test using a dataclass stand-in instead of an `ExpectFailure` mock.** Since T01.16 is not yet landed, the failing-with-failure tests construct a local `@dataclasses.dataclass(frozen=True)` stand-in and pass it as the `failure` value. This proves `to_dict()` recurses correctly without preempting T01.16's 8-field shape. When T01.16 lands, a follow-up test can swap in the real type — the contract this test locks (asdict recursion) does not change.

8. **`__init__.py` re-export.** Added `ExpectResult` to the package `__all__` so downstream callers can `from superclaude.cli.eval import ExpectResult` symmetric to `EvalSpec`. Both names ship from the same module.

## Things deliberately NOT in scope of T01.15

- `ExpectFailure` dataclass — DM-005 / T01.16 (separate task).
- Replacing the test stand-in with the real `ExpectFailure` import — defer to T01.16 close-out.
- ExpectCallable primitives that actually populate `ExpectResult` fields — M4 (COMP-010.1–6).
- Reporter integration (`to_dict()` consumer) — COMP-008 / T03.13.
- `eval doctor --json` payload schema update — T01.13 already emits the CapabilityReport; ExpectResult enters the picture only via `eval run` (M3).

## Risks observed during build

- **Forward-reference fragility.** If a future refactor removes `from __future__ import annotations` from `models.py`, the `Optional["ExpectFailure"]` annotation will fail at import time when ExpectFailure isn't defined yet. Mitigation: T01.16 lands ExpectFailure in the same module before any code path actually evaluates the annotation, and the module docstring + this notes file flag the dependency.
- **`Mapping[str, Any]` with `default_factory=dict`.** The static type is broader than the runtime default; that is intentional so callers may pass `MappingProxyType` if they want deep immutability. No tooling complains today but a future strict-typing pass may want to tighten this.
