# Phase 3 -- Deviation Registry & Run-to-Run Memory

Implement the persistent deviation registry with cross-run identity tracking and run-to-run memory. The registry serves convergence, remediation (SC-3), run-to-run memory (FR-10), and regression detection (FR-8). Exit when FR-6 and FR-10 are integrated with stable IDs and persistence verified (Gate C).

### T03.01 -- Extend DeviationRegistry with source_layer and Stable IDs (FR-6)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032, R-033, R-034 |
| Why | The registry is the single source of truth for gate pass/fail in convergence mode. Split structural/semantic tracking enables correct monotonic progress enforcement. |
| Effort | L |
| Risk | High |
| Risk Drivers | data (registry schema change), migration (pre-v3.05 compatibility), cross-cutting (FR-7, FR-8, FR-10 all consume registry) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0017, D-0018 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0017/spec.md`
- `TASKLIST_ROOT/artifacts/D-0018/spec.md`

**Deliverables:**
1. Extended `DeviationRegistry` in `convergence.py` with `source_layer` field (`"structural"` | `"semantic"`), stable ID computation `(dimension, rule_id, spec_location, mismatch_type)`, cross-run comparison matching by stable ID, FIXED status when finding not reproduced
2. Run metadata dataclass (`RunMetadata`) with `run_number`, `timestamp`, `spec_hash`, `roadmap_hash`, `structural_high_count`, `semantic_high_count`, `total_high_count`

**Steps:**
1. **[PLANNING]** Read existing `DeviationRegistry` in `convergence.py:50-225` and identify extension points
2. **[PLANNING]** Design stable ID computation to avoid collisions (Risk #2)
3. **[EXECUTION]** Add `source_layer` field to finding tracking; implement stable ID from `(dimension, rule_id, spec_location, mismatch_type)`
4. **[EXECUTION]** Implement cross-run comparison: match by stable ID, mark FIXED when not reproduced
5. **[EXECUTION]** Add `RunMetadata` with split HIGH counts to registry run tracking
6. **[VERIFICATION]** Test stable IDs are collision-free on test corpus; FIXED transitions are correct
7. **[COMPLETION]** Document registry extensions in `TASKLIST_ROOT/artifacts/D-0017/spec.md`

**Acceptance Criteria:**
- Each finding has a `source_layer` field: `"structural"` or `"semantic"`
- Stable IDs computed from `(dimension, rule_id, spec_location, mismatch_type)` tuple
- Cross-run comparison correctly matches findings by stable ID and marks unmatched as FIXED
- Run metadata includes `structural_high_count`, `semantic_high_count`, `total_high_count`

**Validation:**
- `uv run pytest tests/roadmap/test_convergence.py -v -k "registry"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0017/spec.md` documents registry extension design

**Dependencies:** T01.05
**Rollback:** TBD
**Notes:** Critical Path Override: Yes -- models path, data integrity. Risk #2 (stable ID collisions) is MEDIUM severity.

---

### T03.02 -- Implement Spec Version Detection and Pre-v3.05 Compatibility (FR-6)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035, R-036 |
| Why | Registry must reset on spec version change and handle pre-v3.05 registries missing `source_layer` field. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | migration (backward compat), data (registry reset logic) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0019/evidence.md`

**Deliverables:**
1. Spec version change detection via `spec_hash` comparison triggering registry reset; pre-v3.05 registries load with `source_layer` defaulting to `"structural"` and `ACTIVE` accepted as valid status

**Steps:**
1. **[PLANNING]** Identify `spec_hash` computation and comparison points in existing registry code
2. **[EXECUTION]** Implement registry reset when `spec_hash` changes between runs
3. **[EXECUTION]** Implement backward-compatible loading: missing `source_layer` defaults to `"structural"`
4. **[EXECUTION]** Ensure `ACTIVE` status is accepted alongside `PENDING` as valid initial status
5. **[VERIFICATION]** Test registry reset on spec hash change; test loading pre-v3.05 registry JSON
6. **[COMPLETION]** Document compatibility behavior in `TASKLIST_ROOT/artifacts/D-0019/evidence.md`

**Acceptance Criteria:**
- Registry resets (clears all findings) when `spec_hash` changes between runs
- Pre-v3.05 registries (without `source_layer`) load with `source_layer` defaulted to `"structural"`
- Findings with `status="ACTIVE"` accepted without error
- Registry serialization preserves all new fields in JSON format

**Validation:**
- `uv run pytest tests/roadmap/test_convergence.py -v -k "backward_compat or spec_hash"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0019/evidence.md` documents compatibility test results

**Dependencies:** T03.01
**Rollback:** TBD
**Notes:** Critical Path Override: Yes -- models path. Risk #7 (pre-v3.05 migration) MEDIUM severity.

---

### T03.03 -- Implement Run-to-Run Memory (FR-10)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037, R-038 |
| Why | Semantic layer needs prior findings summary to prevent re-discovery of fixed issues and anchor severity. Registry tracks first_seen_run and last_seen_run per finding. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (feeds semantic layer prompts) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0020/spec.md`

**Deliverables:**
1. `first_seen_run` and `last_seen_run` tracking per finding; `get_prior_findings_summary()` returning max 50 prior findings (oldest-first truncation) with ID, severity, status, run_number; fixed findings from prior runs not re-reported as new

**Steps:**
1. **[PLANNING]** Review existing `get_prior_findings_summary()` in `convergence.py:179-188`
2. **[EXECUTION]** Extend finding tracking with `first_seen_run` and `last_seen_run` fields
3. **[EXECUTION]** Implement prior findings summary: max 50, oldest-first truncation
4. **[EXECUTION]** Ensure fixed findings from prior runs are not re-reported as new
5. **[EXECUTION]** Add run metadata with ledger snapshot when convergence mode active
6. **[VERIFICATION]** Test summary truncation at 50 findings; verify FIXED findings excluded from new
7. **[COMPLETION]** Document memory behavior in `TASKLIST_ROOT/artifacts/D-0020/spec.md`

**Acceptance Criteria:**
- Each finding tracks `first_seen_run` and `last_seen_run` integers
- `get_prior_findings_summary()` returns at most 50 findings, oldest first, with ID/severity/status/run_number
- Fixed findings from prior runs do not appear as new findings in subsequent runs
- Run metadata includes ledger snapshot (`budget_consumed`, `budget_reimbursed`, `budget_available`) when convergence active

**Validation:**
- `uv run pytest tests/roadmap/test_convergence.py -v -k "memory or prior_findings"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0020/spec.md` documents memory behavior

**Dependencies:** T03.01
**Rollback:** TBD

---

### T03.04 -- Registry Integration Test: 3-Run Simulation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032, R-037 |
| Why | Registry must correctly track findings across multiple runs with stable IDs. This validates the end-to-end lifecycle before convergence engine depends on it. |
| Effort | S |
| Risk | Low |
| Risk Drivers | none matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0021/evidence.md`

**Deliverables:**
1. Integration test: registry correctly tracks findings across 3 simulated runs; stable IDs collision-free; FIXED transitions correct; run metadata complete

**Steps:**
1. **[PLANNING]** Design 3-run test scenario with known findings, fixes, and regressions
2. **[EXECUTION]** Run 1: seed registry with structural + semantic findings
3. **[EXECUTION]** Run 2: some findings fixed, new findings added; verify FIXED status and new stable IDs
4. **[EXECUTION]** Run 3: verify cumulative state; check run metadata with split HIGH counts
5. **[VERIFICATION]** Confirm no stable ID collisions across 3 runs; all statuses correct
6. **[COMPLETION]** Document test results in `TASKLIST_ROOT/artifacts/D-0021/evidence.md`

**Acceptance Criteria:**
- Registry correctly tracks findings across 3 simulated runs
- Stable IDs are collision-free across all 3 runs on test corpus
- FIXED findings transition correctly (finding present in run 1, absent in run 2 -> FIXED)
- Run metadata includes correct `structural_high_count` and `semantic_high_count` per run

**Validation:**
- `uv run pytest tests/roadmap/test_convergence.py::test_three_run_simulation -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0021/evidence.md` documents 3-run lifecycle

**Dependencies:** T03.01, T03.02, T03.03
**Rollback:** TBD

---

### Checkpoint: End of Phase 3

**Purpose:** Gate C -- Registry Certified. FR-6 and FR-10 integrated with stable IDs and persistence verified.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-END.md`
**Verification:**
- Registry correctly tracks findings across 3 simulated runs
- Stable IDs are collision-free on test corpus (Risk #2 mitigation)
- Pre-v3.05 registries load with backward-compatible defaults
**Exit Criteria:**
- FIXED findings transition correctly across runs
- Run-to-run memory retrieval produces correctly truncated prior findings
- All Phase 3 tasks completed with passing validation
