# D-0056 — Notes (T03.14)

## Design choices

* Modeled on `tests/cli/eval/test_isolation_layers_probe.py` (T02.05 /
  COMP-012). Same probe discipline (no instance construction, no
  subprocesses, `inspect` + `dataclasses` only) so the eval test suite
  has one consistent pattern for "pin upstream shape".
* Field-type assertions use `typing.get_type_hints` so generic aliases
  like `list[TaskResult]` and `list[str]` are compared post-resolution
  (avoids string-vs-class mismatches when annotations are evaluated
  lazily under `from __future__ import annotations`).
* `to_yaml` / `to_markdown` are pinned via `inspect.getattr_static`
  rather than instance binding — keeps the probe usable even if the
  class grows non-`__init__`-safe defaults in the future.
* The factory `aggregate_task_results` is included alongside the class
  because the FR-RPT1 reporter contract treats the runner-constructed
  shape (not the dataclass alone) as the pattern reference.

## What deliberately is **not** pinned

* The literal body of `to_yaml` / `to_markdown` — emitter output is
  governed by COMP-008 tests (T03.13), not this probe.
* The `status` property's branching ("PASS"/"FAIL"/"PARTIAL"). Only the
  return-type annotation is pinned; the algorithm is free to evolve as
  long as the type stays `str`.
* The `TaskResult` shape itself — out of scope here; pinned where
  TaskResult is consumed.

## Risks and mitigations

* **Risk:** future addition of new `AggregatedPhaseReport` fields would
  break `field_names_and_order`. **Mitigation:** intentional — appending
  a field is a contract change that should be re-pinned consciously
  alongside any Reporter update.
* **Risk:** type-hint resolution under future Python versions. The
  probe imports `TaskResult` from the same module to avoid
  string-equality compares; verified on Python 3.12.

## Cross-links

* Sibling probe: `tests/cli/eval/test_isolation_layers_probe.py`
  (T02.05 / COMP-012).
* Downstream consumer: T03.13 (COMP-008 `Reporter` /
  `AggregatedRunReport`).
* Source-of-truth lines: `src/superclaude/cli/sprint/executor.py:190-335`
  (verified 2026-05-20).
