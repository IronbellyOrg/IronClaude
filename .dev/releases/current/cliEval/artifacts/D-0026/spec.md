# D-0026 — HomeIsolation dataclass spec

**Task:** T02.04 (Phase 2, Roadmap DM-006 / R-026)
**Module:** `src/superclaude/cli/eval/isolation.py`
**Status:** Implemented 2026-05-20

## Field schema (4-field contract)

| # | Field             | Type   | Default | Purpose |
|---|-------------------|--------|---------|---------|
| 1 | `eval_id`         | `str`  | required | FR-SCH2-validated eval identifier; flows into `home_root / eval_id / home` by COMP-006 (T02.07/T02.11). Re-validated in `__post_init__` so loader bypass cannot smuggle in an unsafe id. |
| 2 | `home_root`       | `pathlib.Path` | required | Scratch root directory under which the per-eval HOME will be mkdtemp'd. Stored verbatim; FR-ISO2 path containment (T02.08) is the consumer's responsibility. |
| 3 | `session_id`      | `str`  | required | Value the eval HOME stamps into `CLAUDE_SESSION_ID` for the spawned `claude` subprocess (FR-ISO1). Allocation lives in the orchestrator (FR-G2 / T03.16). |
| 4 | `time_offset_sec` | `int`  | `0`     | Optional simulated wall-clock offset in whole seconds. `CLAUDE_FAKE_TIME_OFFSET` env wiring is gated on OQ-8 (DOC-OQ8 / T06.03); the field stays here regardless so the record contract is stable across the OQ resolution. |

Field-declaration order in the dataclass matches the table above so
`dataclasses.fields(HomeIsolation)` returns the four fields in DM-006
order. The type annotations are `str`, `Path`, `str`, `int` exactly as
declared by DM-006 (roadmap row 26).

## Invariants

- `@dataclass(frozen=True)` — mutation of any field raises
  `dataclasses.FrozenInstanceError` (locked by
  `test_home_isolation_is_frozen[…]` parameterised across all four fields).
- Frozen + hashable, so instances are safe to share across threads inside
  the parallel orchestrator (R-058 / T03.16) without locking
  (`test_home_isolation_is_hashable`).
- `__post_init__` calls `validate_eval_id(self.eval_id)` so the FR-SCH2
  regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` is re-enforced inside
  the constructor; any unsafe value raises `InvalidEvalId` BEFORE any
  consumer can derive a filesystem path from the record. Verified for
  traversal, leading-digit, lowercase-start, template-token, NUL, and
  separator-bearing payloads (`test_home_isolation_rejects_unsafe_eval_id`).
- Non-string `eval_id` is rejected by the inherited `validate_eval_id`
  type-check (`test_home_isolation_rejects_non_string_eval_id`).
- Default `time_offset_sec=0` matches DM-006 verbatim
  (`test_home_isolation_default_time_offset_is_zero`).
- Structural equality across all four fields via the dataclass-generated
  `__eq__` (`test_home_isolation_equal_when_fields_match` /
  `test_home_isolation_unequal_when_field_differs`).
- `home_root` is stored as-is — no resolution, no normalisation, no
  containment check inside the dataclass (`test_home_isolation_stores_home_root_verbatim`).

## Caller contract (downstream consumers)

- **COMP-006 `HomeIsolation` extension (T02.07 FR-ISO1 / T02.11)** —
  builds a `HomeIsolation` per eval, then layers `setup()`, `env()`,
  `teardown(keep)`, `state_path(suffix)` on top. The record is the
  immutable handle threaded through the orchestrator → runner → reporter
  pipeline.
- **FR-ISO2 `containment_guard` (T02.08)** — consumes `home_root` and
  `eval_id` to enforce the three-check sequence (regex re-check, prefix
  containment, post-creation symlink resolution). The record's
  `__post_init__` already guarantees the regex check passes; the guard
  layers the path-relativity and symlink checks on top.
- **FR-G2 parallel orchestrator (T03.16)** — relies on the frozen +
  hashable property so per-eval `HomeIsolation` records can be carried as
  dict keys in the `ThreadPoolExecutor` bookkeeping without locking.

## Acceptance criteria → implementation map

| AC bullet (T02.04)                                                                          | Implementation site                                                                                       |
|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `HomeIsolation` in `cli/eval/isolation.py` is a frozen dataclass with the 4 DM-006 fields.   | `isolation.py` — `@dataclass(frozen=True) class HomeIsolation` (covered by `test_home_isolation_has_four_fields`, `test_home_isolation_field_types`, `test_home_isolation_is_frozen[…]`). |
| Construction with an unsafe `eval_id` raises `InvalidEvalId` (delegated to `validate_eval_id`). | `__post_init__` calls `validate_eval_id` (covered by `test_home_isolation_rejects_unsafe_eval_id`, `test_home_isolation_rejects_post_expansion_unsafe_id`, `test_home_isolation_rejects_non_string_eval_id`). |
| Default `time_offset_sec=0` matches DM-006 spec.                                            | Dataclass default; covered by `test_home_isolation_default_time_offset_is_zero` and `test_home_isolation_accepts_explicit_time_offset`. |
| `spec.md` documents the 4-field contract.                                                   | This file.                                                                                                |

## Out of scope for T02.04

- `setup() / env() / teardown(keep) / state_path(suffix)` methods —
  COMP-006 (T02.07 / T02.11).
- Path containment guard (`containment_guard`) — FR-ISO2 / T02.08.
- Real `CLAUDE_FAKE_TIME_OFFSET` env wiring — gated on OQ-8 (DOC-OQ8 /
  T06.03).
- Per-eval HOME mkdtemp under `home_root`, hook deploy, state seeding —
  COMP-006 (T02.07 / T02.11).
- Session id allocation strategy — FR-G2 orchestrator (T03.16).
