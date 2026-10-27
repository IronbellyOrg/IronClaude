# D-0045 — EvalOutcome dataclass spec

**Task:** T03.01 (Phase 3, Roadmap DM-001 / R-045)
**Module:** `src/superclaude/cli/eval/models.py`
**Status:** Implemented 2026-05-20

## Field schema (9-field contract)

| # | Field                 | Type                            | Default                       | Purpose |
|---|-----------------------|---------------------------------|-------------------------------|---------|
| 1 | `eval_id`             | `str`                           | required                      | Id of the expanded eval. Already regex-guarded by FR-SCH2 (T01.05) so the Reporter uses it verbatim in artifact filenames. |
| 2 | `title`               | `str`                           | required                      | Human-readable eval title (copied from `EvalSpec` at runtime so the Reporter does not re-resolve the manifest). |
| 3 | `status`              | `EvalStatus` (Literal of 8)     | required                      | One of `PASS`,`FAIL`,`ERRORED`,`TIMEOUT`,`INTERRUPTED`,`SKIPPED`,`XFAIL`,`XPASS`. Validated in `__post_init__` — invalid values raise `ValueError`. |
| 4 | `duration_sec`        | `float`                         | required                      | Wall-clock seconds from lifecycle start to teardown. |
| 5 | `expects`             | `tuple[ExpectResult, ...]`      | `()`                          | Per-assertion outcomes (DM-009). Tuple keeps the frozen dataclass hashable; empty tuple is the default for `SKIPPED` outcomes. |
| 6 | `skip_reason`         | `Optional[str]`                 | `None`                        | Free-form reason when `status == "SKIPPED"`. No coupling enforced between status and presence per DM-001. |
| 7 | `skip_flag_triggered` | `Optional[str]`                 | `None`                        | Name of the flag/capability that triggered the skip (e.g. `"mcp.tavily"`). `None` when the skip was not flag-driven. |
| 8 | `artifacts`           | `Mapping[str, str]`             | `field(default_factory=dict)` | Artifact-name → path mapping the runner emits. Each instance gets its own mapping via `default_factory`; `to_dict()` returns a shallow-copy to keep the source immutable across mutation by consumers. |
| 9 | `error_class`         | `Optional[str]`                 | `None`                        | Fully-qualified Python exception class name when `status == "ERRORED"` (e.g. `"builtins.RuntimeError"`). |

## Invariants

- `@dataclass(frozen=True)` — mutation raises `dataclasses.FrozenInstanceError` (covered by `test_eval_outcome_is_frozen`).
- Field declaration order matches DM-001 verbatim so `to_dict()` ordering is stable across reporter snapshots (covered by `test_eval_outcome_has_required_fields` and `test_eval_outcome_to_dict_field_order_matches_dm001`).
- `status` membership is enforced at construction time against the module-level `EVAL_STATUSES` tuple derived from `typing.get_args(EvalStatus)`. The 8-value set is exactly `{PASS,FAIL,ERRORED,TIMEOUT,INTERRUPTED,SKIPPED,XFAIL,XPASS}` (covered by `test_eval_outcome_status_literal_set_is_exactly_dm001`, parametrised acceptance, and `test_eval_outcome_rejects_invalid_status` + `test_eval_outcome_rejects_lowercased_status`).
- `artifacts` `default_factory=dict` hands each instance an independent mapping (covered by `test_eval_outcome_artifacts_default_is_independent_per_instance`).
- Two instances built from identical arguments compare equal via the `@dataclass`-generated `__eq__` (covered by `test_eval_outcome_deterministic_equality`).

## Status Literal exports

- `EvalStatus` — `typing.Literal[...]` alias.
- `EVAL_STATUSES` — runtime tuple resolved via `typing.get_args(EvalStatus)`. Single source of truth for membership checks in the Reporter (COMP-008 / T03.13), RunOrchestrator (COMP-003 / T03.15), and JSON-replay paths that build outcomes from dynamic strings.

Both symbols are re-exported from `superclaude.cli.eval` (`__init__.py`) so consumers can import them without reaching into `models`.

## Serialisation

- `to_dict()` builds an explicit ordered `dict` from `_EVAL_OUTCOME_FIELDS` so output ordering is stable regardless of Python version or dataclass internals.
- Nested `ExpectResult` values are unwrapped via their own `to_dict()` so the Reporter never has to recurse manually.
- `artifacts` is shallow-copied into a plain `dict` so callers that mutate the returned mapping do not affect the immutable source (covered by `test_eval_outcome_to_dict_artifacts_is_independent_of_source`).
- Round-trips through `json.dumps(..., sort_keys=True)` cleanly (covered by `test_eval_outcome_to_dict_is_json_serialisable`).

## Caller contract (downstream consumers)

- COMP-004 EvalRunner (T03.04 / T03.05) — emits one `EvalOutcome` per invocation; per-eval JSONL also derives from these fields.
- COMP-008 Reporter (T03.13) — reads `EvalOutcome.to_dict()` to render aggregated summary.md/summary.json and to enforce the `len(evals[]) == counts.expanded_n_prime` invariant (FR-RPT1 / T03.11).
- COMP-003 RunOrchestrator (T03.15) — collects one outcome per expanded spec; relies on `status` membership for routing the partial-summary path on SIGINT.

## Acceptance criteria → implementation map

| AC bullet (T03.01)                                                                                  | Implementation site                                                                                                       |
|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Frozen `EvalOutcome` with the 9 fields named in DM-001.                                             | `models.py` — `@dataclass(frozen=True) class EvalOutcome` (covered by `test_eval_outcome_has_required_fields`, `test_eval_outcome_is_frozen`). |
| Invalid status raises `ValueError`; valid statuses are exactly the 8 listed in DM-001.              | `EvalOutcome.__post_init__` membership check against `EVAL_STATUSES` (covered by `test_eval_outcome_status_literal_set_is_exactly_dm001`, parametrised acceptance, and the two rejection tests). |
| `to_dict()` produces deterministic JSON-serializable output.                                        | `_EVAL_OUTCOME_FIELDS`-driven ordered dict + nested `ExpectResult.to_dict()` + shallow-copied artifacts (covered by `test_eval_outcome_to_dict_field_order_matches_dm001`, `test_eval_outcome_to_dict_is_json_serialisable`, `test_eval_outcome_to_dict_unwraps_nested_expect_results`). |
| `TASKLIST_ROOT/artifacts/D-0045/spec.md` records the field contract.                                | This file.                                                                                                                |

## Out of scope for T03.01

- `EvalResult` (DM-003 / T03.02) — reporter-facing per-eval result record.
- `EvalContext` (DM-010 / T03.03) — runtime context passed to each ExpectCallable.
- FR-LC1 lifecycle skeleton (T03.04) — the EvalRunner emission site for these outcomes.
- Reporter side-effects (summary.md / summary.json writes, JUnit emission) — COMP-008 (T03.13).
