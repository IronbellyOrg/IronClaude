# D-0014 — implementation notes

## Decisions made during build

1. **Module location.** Added `ExpectFailure` to `src/superclaude/cli/eval/models.py` alongside `EvalSpec` and `ExpectResult`. The phase-1 tasklist explicitly names this module as the destination ("`src/superclaude/cli/eval/models.py` with the 8 fields from DM-005"), and T01.15's `Optional["ExpectFailure"]` forward annotation was authored on the assumption the concrete class would land in the same module. Co-locating the pair removes the forward reference at evaluation time without needing a `TYPE_CHECKING` dance.

2. **`expected` / `actual` typed as `Any`.** DM-005 does not constrain payload shape, and primitive Expects (COMP-010.1–6, M4) will populate these with arbitrary JSON-shaped values (int exit codes, regex strings, dict event payloads). Narrower typing now would force a refactor when primitives land. `Any` matches the DM-005 spirit ("assertion failure detail") and keeps the contract permissive.

3. **`message` defaults to `""`.** Symmetric with `ExpectResult.message` from T01.15 — callers should be able to omit the message when the `expected`/`actual` diff is self-explanatory. The Reporter renders the empty string as "no summary message" rather than treating absence as an error.

4. **`artifact_ref` and `traceback` typed as `Optional[str]` with default `None`.** DM-005 does not state these are required. The Reporter generates artifact refs as part of writing the JSON report (post-construction), so the dataclass must accept the missing case at construction time. Same reasoning for `traceback`: only the exception path captures it.

5. **`to_dict()` builds the dict explicitly from `_EXPECT_FAILURE_FIELDS`.** Chose this over `dataclasses.asdict(self)` to guarantee ordering. `asdict` returns insertion order which currently matches field-declaration order, but the spec demands a stable contract for reporter snapshots, and an explicit field tuple makes the guarantee visible. The test `test_expect_failure_to_dict_field_order_matches_dm005` locks this. `test_expect_failure_asdict_matches_to_dict` documents that the two agree on values today (ordering is owned by `to_dict`).

6. **No `__post_init__` validation.** DM-005 does not require value-level checks (unlike DM-007 `Capability.failure_mode` from T01.09 which enumerated literals). Adding validation would risk false negatives — the Reporter is the right layer to decide what "looks empty" means for an `expected` payload of, say, `None` or `0`.

7. **Forward reference resolution for `ExpectResult.failure`.** T01.15 already accommodates an `Optional["ExpectFailure"]` forward annotation via `from __future__ import annotations`. T01.16 lands the concrete class in the same module, so the annotation now resolves to a real type at runtime. No production-code change is needed in `ExpectResult`; the test stand-in from T01.15 is superseded by `test_expect_failure_round_trips_inside_expect_result` here, which exercises the genuine `ExpectFailure` inside an `ExpectResult`.

8. **Package re-export.** Added `ExpectFailure` to `src/superclaude/cli/eval/__init__.py`'s `__all__` so callers can `from superclaude.cli.eval import ExpectFailure` — symmetric with `ExpectResult` and `EvalSpec`. Locked by `test_expect_failure_importable_from_package`.

9. **Module docstring updated.** Listed DM-005 / D-0014 / T01.16 alongside DM-002 / DM-009 and described the 8-field ExpectFailure contract so the file's purpose statement stays accurate.

## Things deliberately NOT in scope of T01.16

- Real `ExpectCallable` primitives that emit populated `ExpectFailure`s — M4 (COMP-010.1–6).
- Reporter side-effects: artifact ref resolution against the run's scratch root, JSONL writes, terminal rendering — COMP-008 / T03.13.
- `EvalOutcome` aggregation of multiple `ExpectFailure`s per eval — T03.01.
- A "two failing Expects in a single eval → two ExpectFailure entries" *integration* test — that lives in the Reporter test set / T03.13. T01.16 covers the per-failure construction pattern (`test_expect_failure_two_per_eval_pattern`).

## Risks observed during build

- **`Any` typing on `expected` / `actual`.** Permissive by design, but a future strict-typing pass may want a generic narrowing once primitive payload shapes are known (M4). The dataclass is frozen, so any tightening will be a non-breaking annotation-only change.
- **`to_dict()` ordering vs. asdict().** Two serialisation paths exist (`to_dict()` and `dataclasses.asdict`). They agree on values today; only `to_dict()` guarantees ordering. The Reporter (T03.13) must call `to_dict()` — `asdict` is acceptable for ad-hoc tests but not for snapshot diffs. The spec.md *Serialisation* section documents this.
