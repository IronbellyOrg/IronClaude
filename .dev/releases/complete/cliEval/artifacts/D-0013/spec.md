# D-0013 — ExpectResult dataclass spec

**Task:** T01.15 (Phase 1, Roadmap DM-009 / R-013)
**Module:** `src/superclaude/cli/eval/models.py`
**Status:** Implemented 2026-05-20

## Field schema (6-field contract)

| # | Field          | Type                          | Default              | Purpose |
|---|----------------|-------------------------------|----------------------|---------|
| 1 | `name`         | `str`                         | required             | Assertion name; matches the DSL method that emitted the result (e.g. `"exit_code"`, `"file.contains_event"`). Stable per-Expect key for the Reporter (COMP-008). |
| 2 | `passed`       | `bool`                        | required             | `True` when the assertion was satisfied. Rolled up by the Reporter into the per-eval pass/fail bit. |
| 3 | `message`      | `str`                         | `""`                 | Human-readable one-liner for terminal summary; empty when no message is needed. |
| 4 | `details`      | `Mapping[str, Any]`           | `field(default_factory=dict)` | Structured additional info (matched event payload, diff fragments) carried through to the JSON report. Each instance gets its own mapping via `default_factory`. |
| 5 | `duration_sec` | `float`                       | `0.0`                | Wall-clock seconds the assertion took. `float` to capture sub-millisecond resolution. |
| 6 | `failure`      | `Optional["ExpectFailure"]`   | `None`               | DM-005 detail record for a failing assertion. Forward-referenced — see *Forward-reference handling* below. |

## Invariants

- `@dataclass(frozen=True)` — mutation raises `dataclasses.FrozenInstanceError` (covered by `test_expect_result_is_frozen`).
- Field declaration order matches DM-009 verbatim so `to_dict()` output is stable across reporter snapshots.
- `failure` is Optional with **no coupling** to `passed`: a failing result with `failure=None` is well-formed (DM-009 explicit). Tests cover this with `test_expect_result_failing_without_failure_attached_is_allowed`.
- Two instances built from identical arguments compare equal via the `@dataclass`-generated `__eq__`.

## Serialisation

- `to_dict()` delegates to `dataclasses.asdict(self)` which recursively unwraps nested dataclasses. Once T01.16 lands `ExpectFailure`, `result.to_dict()["failure"]` will be a plain dict without additional Reporter-side handling.
- Round-trips through `json.dumps(..., sort_keys=True)` cleanly (covered by `test_expect_result_to_dict_is_json_serialisable`).

## Forward-reference handling

DM-005 `ExpectFailure` lands with T01.16 in this same module. T01.15 declares the field as `Optional["ExpectFailure"]` (string forward annotation). `from __future__ import annotations` defers annotation evaluation, so the module imports cleanly before T01.16 lands. Acceptance is exercised today via:

- The Optional/None path → directly constructible.
- A dataclass stand-in (`_FailureStandIn` in the test) → proves the field accepts a populated dataclass value and that `asdict` recursively unwraps it. T01.16 will replace the stand-in with the real `ExpectFailure` import without changing the production code.

## Caller contract (downstream consumers)

- COMP-010 `ExpectCallable` stubs (T01.14) — every Expect method returns an `ExpectResult`; M4 primitives populate the fields.
- COMP-008 Reporter (T03.13) — reads `ExpectResult.to_dict()` to render per-Expect rows in the JSON report.
- Aggregation: the Reporter does not assume `len(failures) == sum(not r.passed)`; each `ExpectResult` carries (or omits) its own `failure` payload.

## Acceptance criteria → implementation map

| AC bullet (T01.15)                                                                                          | Implementation site                                                                                       |
|-------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Frozen `ExpectResult` with the 6 fields named in DM-009.                                                    | `models.py` — `@dataclass(frozen=True) class ExpectResult` (covered by `test_expect_result_has_required_fields`, `test_expect_result_is_frozen`). |
| `ExpectResult` is JSON-serializable via `dataclasses.asdict()`.                                             | `to_dict()` calls `dataclasses.asdict` (covered by `test_expect_result_to_dict_is_json_serialisable`, `test_expect_result_asdict_matches_to_dict`). |
| Construction with valid field types succeeds; `failure` is Optional with no required-when-failed coupling. | Field default `failure=None`; covered by `test_expect_result_failing_without_failure_attached_is_allowed`.                       |
| `spec.md` documents the field contract.                                                                     | This file.                                                                                                |

## Out of scope for T01.15

- `ExpectFailure` dataclass itself — DM-005 / T01.16.
- Real `ExpectCallable` primitives that emit populated `ExpectResult`s — COMP-010.1–6 (M4).
- Reporter side-effects (JSONL writes, terminal rendering) — COMP-008 (T03.13).
