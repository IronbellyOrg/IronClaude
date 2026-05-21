# D-0042 — Evidence

**Task**: T02.23 (Phase 2 — cliEval harness)
**Deliverable**: TEST-004 capability gate tests (R-042)
**Module**: `tests/cli/eval/test_capability_classifications.py`

## Verification command (T02.23 Steps[5])

```
uv run pytest tests/cli/eval/test_capability_classifications.py -v
```

## Result

**20 passed in 0.14s** — every classification slice green; coverage pin holds.

Full log: `TASKLIST_ROOT/evidence/T02.23/pytest-T02.23.log`

### Per-slice tally (matches the matrix in `spec.md`)

| Slice                                       | Class                             | Cases | Status |
|---------------------------------------------|-----------------------------------|-------|--------|
| Missing claude → HARD                       | `TestMissingClaudeHard`           | 4     | PASS   |
| `--no-mcp` SOFT-SKIP                        | `TestNoMcpSoftSkip`               | 4     | PASS   |
| XFAIL classification                        | `TestXfailClassification`         | 4     | PASS   |
| Doctor renders correct status string        | `TestDoctorClassificationRendering` | 7   | PASS   |
| Coverage pin (meta)                         | `test_test_004_slice_coverage_is_complete` | 1 | PASS |
| **Total**                                   |                                   | **20**| **PASS** |

## Sibling-regression check

Re-ran the full five-module capability family to confirm D-0042 did not break neighbouring deliverables:

```
uv run pytest tests/cli/eval/test_capability_classifications.py \
              tests/cli/eval/test_capability_gates.py \
              tests/cli/eval/test_capability_dataclass.py \
              tests/cli/eval/test_capability_report.py \
              tests/cli/eval/test_doctor.py
```

**92 passed in 0.24s** — no drift in `test_capability_gates.py` (COMP-009),
`test_capability_dataclass.py` (DM-007), `test_capability_report.py`
(DM-008), or `test_doctor.py` (FR-CLI4).

Log: `TASKLIST_ROOT/evidence/T02.23/pytest-capability-family.log`

## Acceptance-criteria coverage

| AC | Status | Evidence |
|---|--------|---------|
| AC1 — missing claude fails HARD | PASS | `TestMissingClaudeHard` (4 cases) — all green |
| AC2 — `--no-mcp` soft-skips MCP evals | PASS | `TestNoMcpSoftSkip` (4 cases) — all green |
| AC3 — XFAIL classification supported | PASS | `TestXfailClassification` (4 cases) — all green |
| AC4 — doctor renders correct status string per classification | PASS | `TestDoctorClassificationRendering` (7 cases) — all marker strings pinned |
| AC5 — pytest exits 0 | PASS | 20 passed in 0.14s |
| AC6 — `D-0042/spec.md` documents the classification matrix | PASS | See `spec.md` (5-row matrix table + per-slice case lists) |

## Files produced

- `tests/cli/eval/test_capability_classifications.py` — 20-test module
- `.dev/releases/current/cliEval/artifacts/D-0042/spec.md` — classification matrix + slice spec
- `.dev/releases/current/cliEval/artifacts/D-0042/notes.md` — design notes
- `.dev/releases/current/cliEval/artifacts/D-0042/evidence.md` — this file
- `.dev/releases/current/cliEval/evidence/T02.23/pytest-T02.23.log` — verification log
- `.dev/releases/current/cliEval/evidence/T02.23/pytest-capability-family.log` — sibling-regression log
