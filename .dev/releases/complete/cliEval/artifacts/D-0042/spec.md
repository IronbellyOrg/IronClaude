# D-0042 — TEST-004 capability gate tests

**Task**: T02.23 (Phase 2 — cliEval harness)
**Tier**: STANDARD
**Risk**: Low
**Roadmap**: R-042 / TEST-004 (HARD / SOFT-SKIP / XFAIL classifications + `--no-mcp` flag + doctor status rendering)
**Cross-links**: D-0008 (`Capability` DM-007, T01.09), D-0009 (`CapabilityReport` DM-008, T01.10), D-0010 (COMP-009 `CapabilityGates`, T01.11), D-0011 (FR-CLI4 `eval doctor`, T01.13)

## Goal

TEST-004 is the **contract-layer readout** for the three-tier capability-gate matrix promised by design-spec §11 "Three tiers of gates". The sibling modules (`test_capability_dataclass.py` pins the `Capability` shape, `test_capability_report.py` pins the `CapabilityReport` shape, `test_capability_gates.py` pins the gate evaluator, `test_doctor.py` pins the FR-CLI4 CLI surface) already exercise the *components*. D-0042 is the *first-class TEST item* the roadmap promises: one targeted pytest module, named after the boundary it pins (`test_capability_classifications.py`), whose every test maps directly to a TEST-004 acceptance-criterion bullet, so that the audit reviewing the M2 exit can read the file top-to-bottom and confirm the three-tier contract without spelunking through four sibling modules.

The module exercises the **default capability roster** (real `_DEFAULT_CAPABILITY_SPECS` from `src/superclaude/cli/eval/capabilities.py`) — not a narrowed test roster — so the test would fail if a future refactor changed the HARD-binary set (`claude / make / jq / git`) or the SOFT-SKIP MCP set (`auggie / auggie-mcp / airis-mcp-gateway`). It also pins `HARD_FAIL_EXIT_CODE` (= 2) end-to-end via `CliRunner` so any drift on the exit-code contract surfaces here first.

## Test matrix

| Slice | TEST-004 AC bullet | Test class | Cases |
|---|---|---|---|
| Missing claude HARD | "missing claude fails HARD" | `TestMissingClaudeHard` | 4 |
| `--no-mcp` SOFT-SKIP | "`--no-mcp` soft-skips MCP evals" | `TestNoMcpSoftSkip` | 4 |
| XFAIL classification | "XFAIL classification supported" | `TestXfailClassification` | 4 |
| Doctor status rendering | "doctor output renders correct status string per classification" | `TestDoctorClassificationRendering` | 7 |
| Coverage pin | (meta) | `test_test_004_slice_coverage_is_complete` | 1 |
| **Total** | | | **20** |

### Slice 1 — `TestMissingClaudeHard` (4 cases)

- `test_missing_claude_lands_in_hard_failures` — `CapabilityGates.check_all()` with `shutil.which("claude")` returning `None` populates `binary.claude` in `hard_failures`; `soft_skips` and `soft_xfails` stay empty.
- `test_missing_claude_row_carries_hard_failure_mode` — same setup; assert the `CapabilityStatus` row carries `failure_mode="hard"`, `passed=False`, `skipped_by_flag=False`, and a "not found"-bearing detail.
- `test_doctor_exits_two_when_claude_missing` — end-to-end via `CliRunner`: doctor exits `HARD_FAIL_EXIT_CODE` (= 2) and the HARD-failure artifact lands on stderr naming `binary.claude`.
- `test_doctor_json_reports_hard_failure_on_missing_claude` — same end-to-end check via `--json`; assert the payload's `hard_failures` includes `binary.claude` and `soft_skips` does not.

### Slice 2 — `TestNoMcpSoftSkip` (4 cases)

- `test_no_mcp_flag_skips_mcp_servers_even_when_probe_passes` — `mcp_probe` injects a passing probe; assert every MCP row lands in `soft_skips`, `skipped_by_flag=True`, and `passed=False` (override semantics).
- `test_no_mcp_flag_skips_mcp_servers_when_probe_fails` — MCP binaries absent; HARD binaries present; assert HARD floor stays green and every default MCP row routes through `soft_skips` with `skip_flags=("--no-mcp",)`.
- `test_no_mcp_flag_does_not_affect_hard_rows` — assert no HARD row gains `skipped_by_flag=True` when the flag is active (HARD descriptors do not declare a `skip_flag`).
- `test_doctor_no_mcp_flag_lands_mcp_rows_in_soft_skips` — end-to-end via `CliRunner` `--json --no-mcp`: assert `payload["skip_flags"] == ["--no-mcp"]` and every default MCP row appears in `soft_skips`.

### Slice 3 — `TestXfailClassification` (4 cases)

- `test_failing_xfail_capability_lands_in_soft_xfails` — inject a custom `_CapabilitySpec(failure_mode="xfail")` via the `capabilities=` constructor hook with the probe target absent from PATH; assert `soft_xfails` contains the row and the HARD / SOFT-SKIP buckets stay empty.
- `test_xfail_row_carries_xfail_failure_mode_when_failing` — same setup; assert the `CapabilityStatus` row's `failure_mode="xfail"`, `passed=False`, `skipped_by_flag=False`.
- `test_passing_xfail_capability_does_not_land_in_failure_buckets` — flip the spec to target a binary that resolves; assert all three failure buckets stay empty and the row's `passed=True`.
- `test_xfail_status_serialises_through_capability_report` — build a `CapabilityReport` carrying an xfail row and assert `to_json()` produces a JSON-serialisable payload with `soft_xfails` containing the row name and `failure_mode="xfail"` preserved.

### Slice 4 — `TestDoctorClassificationRendering` (7 cases)

- `test_renders_hard_failure_marker` — pin `[XX] <description> (HARD)` for failing HARD rows.
- `test_renders_soft_skip_probe_failure_marker` — pin `[--] <description> (SOFT-SKIP)` for probe-failed SOFT-SKIP rows.
- `test_renders_skipped_by_flag_marker_when_no_mcp_active` — pin `[--] <description> (skipped by flag)` and `skip flags: --no-mcp`. Negative: `(SOFT-SKIP)` MUST NOT appear when the override marker is present.
- `test_renders_xfail_marker` — pin `[??] <description> (xfail)`.
- `test_renders_passing_row_with_ok_marker` — pin `[ok] <description>` with NO trailing tag.
- `test_hard_failure_artifact_names_offending_capability` — `render_hard_failure_artifact` lists the name + description + detail for each HARD failure.
- `test_doctor_cli_emits_distinct_strings_for_each_classification` — end-to-end via `CliRunner`: HARD floor green; MCP probes absent; assert `(SOFT-SKIP)` appears in the default run. Re-invoke with `--no-mcp`; assert `(skipped by flag)` appears AND `skip flags: --no-mcp` appears.

### Coverage pin — `test_test_004_slice_coverage_is_complete`

A meta-test that asserts each TEST-004 AC bullet has at least one corresponding test class in this module. Future drift in the AC list will break this test, forcing a coordinated spec + test update. Mirrors the meta-test in D-0040 (TEST-002) and D-0041 (TEST-003).

## Classification matrix (the contract this module pins)

| `failure_mode` | Bucket on miss          | Doctor marker     | Trailing tag           | Override flag | Aborts run? |
|---------------|-------------------------|-------------------|------------------------|---------------|-------------|
| `hard`        | `hard_failures`         | `[XX]`            | ` (HARD)`              | — none —      | Yes (`exit 2`) |
| `skip`        | `soft_skips`            | `[--]`            | ` (SOFT-SKIP)`         | `--no-mcp` (default roster) | No |
| `skip` (flag-forced) | `soft_skips`     | `[--]`            | ` (skipped by flag)`   | `--no-mcp`    | No |
| `xfail`       | `soft_xfails`           | `[??]`            | ` (xfail)`             | — none in default roster — | No |
| (passing)     | — none —                | `[ok]`            | — none —               | n/a           | No |

The matrix maps 1:1 to the `_row_marker()` helper in `src/superclaude/cli/eval/commands.py` and the bucket-routing logic in `CapabilityGates.check_all()`.

## Acceptance criteria

| AC | Source | Verified by |
|---|---|---|
| AC1 — missing claude fails HARD | TEST-004 | `TestMissingClaudeHard` (all 4 cases) |
| AC2 — `--no-mcp` soft-skips MCP evals | TEST-004 | `TestNoMcpSoftSkip` (all 4 cases) |
| AC3 — XFAIL classification supported | TEST-004 | `TestXfailClassification` (all 4 cases) |
| AC4 — doctor renders correct status string per classification | TEST-004 | `TestDoctorClassificationRendering` (all 7 cases) |
| AC5 — `pytest tests/cli/eval/test_capability_classifications.py -v` exits 0 with all 3+ tests passing | TEST-004 | Evidence log: 20 passed in 0.17s |
| AC6 — `D-0042/spec.md` documents the classification matrix | TEST-004 | this document |

## Why a new module instead of extending an existing one

| Existing module | Purpose | Why it can't be TEST-004 |
|---|---|---|
| `test_capability_gates.py` | COMP-009 unit — `CapabilityGates` mechanics in isolation | Test-class shape is method-oriented (`test_<gate_method>`), not classification-AC-oriented; reads as a unit-test grab-bag, not a tier contract |
| `test_capability_dataclass.py` | DM-007 unit — `Capability` 5-field contract | Scoped to the descriptor shape; doesn't exercise `check_all()` or doctor rendering |
| `test_capability_report.py` | DM-008 unit — `CapabilityReport` 6-field contract + `to_json()` | Scoped to the aggregate report shape; doesn't pin classification routing or doctor marker strings |
| `test_doctor.py` | FR-CLI4 — `eval doctor` CLI surface | Doctor-flag-oriented (one test per CLI flag + helper); doesn't isolate the three-tier matrix |

TEST-004 is the *contract* — one module whose every test maps to an AC bullet, designed to be read by the M2-exit auditor. Folding it into any existing module would dilute the readout and re-introduce the same scattered-coverage problem the TEST-004 deliverable was created to fix.

## Public API touched

None. D-0042 is a test-only deliverable. Production surface was finalized by D-0008, D-0009, D-0010, and D-0011. The default capability roster (`_DEFAULT_CAPABILITY_SPECS`), the `HARD_FAIL_EXIT_CODE` constant, and the `render_checklist` marker strings are now *load-bearing* for this module — any future change to any of them will surface here first.
