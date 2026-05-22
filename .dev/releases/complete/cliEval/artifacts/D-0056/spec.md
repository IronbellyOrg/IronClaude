# D-0056 — AggregatedPhaseReport pattern probe (COMP-015)

**Task:** T03.14 (Phase 3, Roadmap COMP-015 / R-056)
**Probe file:** `tests/cli/eval/test_phase_report_probe.py`
**Pinned surface:** `src/superclaude/cli/sprint/executor.py:190-335`
**Status:** Implemented 2026-05-20

## Purpose

COMP-008 `Reporter` / `AggregatedRunReport` (T03.13) uses
`AggregatedPhaseReport` from the sprint runner as its **pattern
reference** for emitter shape (runner-constructed report; not parsed
from agent self-report). This probe pins the upstream surface so any
rename, field reorder, signature drift, or property removal in
`cli/sprint/executor.py` fails the probe before silently invalidating
the eval Reporter's pattern reference.

Sibling to COMP-012 / T02.05 (`test_isolation_layers_probe.py`); both
pin upstream shapes read-only.

## Pinned surface

### Class identity

| Pin | Expected |
|---|---|
| `AggregatedPhaseReport.__module__` | `superclaude.cli.sprint.executor` |
| `dataclasses.is_dataclass(AggregatedPhaseReport)` | `True` |

### Field contract (order and types)

| # | Field | Type |
|---|---|---|
| 1 | `phase_number` | `int` |
| 2 | `tasks_total` | `int` |
| 3 | `tasks_passed` | `int` |
| 4 | `tasks_failed` | `int` |
| 5 | `tasks_incomplete` | `int` |
| 6 | `tasks_skipped` | `int` |
| 7 | `tasks_not_attempted` | `int` |
| 8 | `budget_remaining` | `int` |
| 9 | `total_turns_consumed` | `int` |
| 10 | `total_duration_seconds` | `float` |
| 11 | `task_results` | `list[TaskResult]` |
| 12 | `remaining_task_ids` | `list[str]` |

### Methods and properties

| Symbol | Kind | Signature pin |
|---|---|---|
| `status` | `property` | returns `str` |
| `to_yaml` | method | `(self) -> str` |
| `to_markdown` | method | `(self) -> str` |

### Factory

`aggregate_task_results(phase_number, task_results, remaining_task_ids,
budget_remaining) -> AggregatedPhaseReport`, co-located with
`AggregatedPhaseReport` in `superclaude.cli.sprint.executor`. All four
parameters are `POSITIONAL_OR_KEYWORD`.

## Probe discipline

* No `AggregatedPhaseReport` instance is constructed — all assertions
  go through `dataclasses.fields` and `inspect`.
* No subprocess, no file writes, no env mutation.
* 25 assertions across class identity, field contract (12 fields × type
  parametrize), emitter surface (2 methods × 3 facets), `status`
  property, and the `aggregate_task_results` factory.

## Validation

Run:

```bash
uv run pytest tests/cli/eval/test_phase_report_probe.py -v
```

Reference run on 2026-05-20: **25 passed in 0.14s** (full log in
`evidence/T03.14/pytest.log`).

### Synthetic-rename check (AC requirement)

Renaming `to_yaml` → `to_yaml_RENAMED` in
`src/superclaude/cli/sprint/executor.py` produces **3 failures**
(`emitter_methods_present[to_yaml]`,
`emitter_returns_str[to_yaml]`,
`emitter_takes_only_self[to_yaml]`), confirming the probe is sensitive
to upstream method-name drift. Source is restored after the check.

## Failure semantics

If this probe fails:

1. An upstream refactor of
   `cli/sprint/executor.py:AggregatedPhaseReport` /
   `aggregate_task_results` has occurred.
2. The eval Reporter (COMP-008, T03.13) must be re-validated against
   the new shape before re-pinning.
3. Do **not** edit the probe to silence it without first reconciling
   the Reporter's pattern reference.

## Dependencies

* Upstream: `cli/sprint/executor.py` (read-only).
* Downstream: T03.13 (COMP-008 Reporter) declares this probe as a
  dependency via roadmap `COMP-008 deps FR-RPT1, COMP-015`.
