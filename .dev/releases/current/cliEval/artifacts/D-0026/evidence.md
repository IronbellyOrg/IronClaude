# D-0026 — evidence

## Verification command

```
uv run pytest tests/cli/eval/test_isolation_dataclass.py -v
```

## Result (2026-05-20)

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
configfile: pyproject.toml
collected 32 items

tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_has_four_fields PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_field_types PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_default_time_offset_is_zero PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_accepts_explicit_time_offset PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_stores_home_root_verbatim PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_is_frozen[eval_id-E2] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_is_frozen[home_root-value1] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_is_frozen[session_id-sess-002] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_is_frozen[time_offset_sec-7] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_is_hashable PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[../home] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[/etc] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[..] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[1E] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[e1] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[E1/x] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[E1\x00] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[{{prefix}}] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[E-1] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_unsafe_eval_id[E_1] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_accepts_valid_eval_ids[E1] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_accepts_valid_eval_ids[E2.1] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_accepts_valid_eval_ids[D15] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_accepts_valid_eval_ids[A] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_accepts_valid_eval_ids[Test1] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_accepts_valid_eval_ids[ABC123] PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_non_string_eval_id PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_rejects_post_expansion_unsafe_id PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_equal_when_fields_match PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_unequal_when_field_differs PASSED
tests/cli/eval/test_isolation_dataclass.py::test_home_isolation_importable_from_package PASSED

============================== 32 passed in 0.15s ==============================
```

Full pytest log archived at `TASKLIST_ROOT/evidence/T02.04/pytest.log`.

## Acceptance-criteria evidence map

| AC bullet (T02.04) | Test(s) |
|---|---|
| Frozen dataclass with 4 DM-006 fields (`eval_id`, `home_root`, `session_id`, `time_offset_sec`). | `test_home_isolation_has_four_fields`, `test_home_isolation_field_types`, `test_home_isolation_is_frozen[…]` (parameterised over all 4 fields). |
| Construction with unsafe `eval_id` raises `InvalidEvalId`. | `test_home_isolation_rejects_unsafe_eval_id[…]` (11 negative payloads incl. traversal, leading-digit, lowercase, template, NUL, hyphen, underscore), `test_home_isolation_rejects_post_expansion_unsafe_id`, `test_home_isolation_rejects_non_string_eval_id`. |
| Default `time_offset_sec=0` matches DM-006. | `test_home_isolation_default_time_offset_is_zero`, `test_home_isolation_accepts_explicit_time_offset`. |
| `D-0026/spec.md` documents the 4-field contract. | `artifacts/D-0026/spec.md` (this artifact tree). |

## Validation extras (beyond AC)

- `test_home_isolation_is_frozen[…]` — explicit `FrozenInstanceError` assertion fulfils
  the Validation bullet "build a `HomeIsolation` and assert mutation raises FrozenInstanceError".
- `test_home_isolation_is_hashable` — confirms the record is safe to use as a dict key
  inside the parallel orchestrator (R-058 / T03.16).
- `test_home_isolation_importable_from_package` — confirms `HomeIsolation` is re-exported
  from `superclaude.cli.eval` so downstream consumers can import without a deep path.
