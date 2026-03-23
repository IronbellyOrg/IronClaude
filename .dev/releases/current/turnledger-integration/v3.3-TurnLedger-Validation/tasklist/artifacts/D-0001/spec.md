# D-0001: JSONL Audit Record Writer

## Deliverable
`tests/audit-trail/audit_writer.py` — JSONL audit record writer implementing the FR-7.1 10-field schema.

## Schema (10 fields)

| Field | Type | Source |
|---|---|---|
| `test_id` | str | Caller-provided |
| `spec_ref` | str | Caller-provided |
| `timestamp` | str (ISO-8601 UTC) | Auto-computed |
| `assertion_type` | str (`behavioral`/`structural`/`value`) | Caller-provided |
| `inputs` | dict | Caller-provided |
| `observed` | dict | Caller-provided |
| `expected` | dict | Caller-provided |
| `verdict` | str (`PASS`/`FAIL`/`SKIP`) | Caller-provided |
| `evidence` | str | Caller-provided |
| `duration_ms` | float | Auto-computed from `start_timer()`/`record()` |

## API

- `AuditWriter(output_path)` — constructor, creates parent dirs
- `start_timer()` — marks test start for duration computation
- `record(**fields)` — validates schema, writes one JSONL line, returns the record dict

## Constraints
- stdlib only (`json`, `time`, `datetime`, `pathlib`)
- No `mock.patch` in tests
- Deterministic output for identical inputs (except `timestamp` and `duration_ms`)
