# Phase 3 -- KPI and Deviation Reconciliation

Extend reporting with 6 wiring KPI fields in `sprint/kpi.py` and add cross-gate deviation count reconciliation in `roadmap/gates.py`. Phase 3 can run in parallel with Phase 4 integration tests, though Milestone 3.2 (`roadmap/gates.py` modification) should complete before final merge to avoid conflicts with Anti-Instincts and Unified Audit Gating changes.

---

### T03.01 -- Implement KPI Report Extensions

| Field | Value |
|---|---|
| Roadmap Item IDs | R-031, R-032 |
| Why | KPI reporting must include wiring gate metrics so operators can track analysis effectiveness, budget consumption, and finding trends across sprint runs. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0019/spec.md`

**Deliverables:**
1. 6 wiring KPI fields and `build_kpi_report()` signature update in `src/superclaude/cli/sprint/kpi.py` (FR: T07c, SC-015)

**Steps:**
1. **[PLANNING]** Read current `sprint/kpi.py` implementation; identify `build_kpi_report()` signature and return structure
2. **[PLANNING]** Identify the 6 wiring KPI fields from FR: T07c (wiring_findings_total, wiring_findings_by_type, wiring_turns_used, wiring_turns_credited, whitelist_entries_applied, files_skipped)
3. **[EXECUTION]** Add 6 wiring KPI fields to KPI report dataclass/dict
4. **[EXECUTION]** Update `build_kpi_report()` signature to accept TurnLedger and WiringReport data; populate wiring KPI fields
5. **[EXECUTION]** Ensure floor-to-zero credit behavior is surfaced clearly in KPI output (R7 documentation)
6. **[VERIFICATION]** Verify all 6 KPI fields are populated correctly from TurnLedger and WiringReport data (SC-015)
7. **[COMPLETION]** Record implementation details to D-0019/spec.md

**Acceptance Criteria:**
- `sprint/kpi.py` contains 6 wiring KPI fields populated from TurnLedger and WiringReport data
- `build_kpi_report()` signature updated to accept wiring gate data without breaking existing callers
- SC-015 validated: all 6 fields present and correctly populated

**Validation:**
- `uv run pytest tests/sprint/ -k "kpi" -v`
- Evidence: linkable artifact produced at D-0019/spec.md

**Dependencies:** T02.02, T02.08 (TurnLedger extensions must exist)
**Rollback:** Revert KPI field additions and signature change in `sprint/kpi.py`

---

### T03.02 -- Implement Deviation Count Reconciliation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033 |
| Why | Cross-gate deviation count reconciliation detects inconsistencies between reported and actual finding counts, causing deterministic gate failure on mismatch. |
| Effort | L |
| Risk | High |
| Risk Drivers | breaking (gate failure behavior), cross-cutting (shared roadmap/gates.py file), data (deviation count comparison) |
| Tier | STRICT |
| Confidence | [█████████░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0020/spec.md`

**Deliverables:**
1. `_deviation_counts_reconciled()` function in `src/superclaude/cli/roadmap/gates.py` (FR: T08, SC-008) with merge conflict mitigation strategy

**Steps:**
1. **[PLANNING]** Read current `roadmap/gates.py` structure; identify insertion point at file end to minimize diff overlap (Constraint 10)
2. **[PLANNING]** Review Constraint 10 coordination strategy: implement last within Phase 3, isolate at file end, rebase before merge
3. **[EXECUTION]** Implement `_deviation_counts_reconciled()` at end of `roadmap/gates.py`: compare reported vs actual finding counts
4. **[EXECUTION]** Implement deterministic gate failure on deviation count mismatch
5. **[EXECUTION]** Ensure function is isolated at file end with clear comment boundary to minimize merge conflict surface
6. **[VERIFICATION]** Verify deviation mismatch causes deterministic gate failure; verify no behavioral regressions in existing fidelity gate logic
7. **[COMPLETION]** Record implementation details and merge coordination notes to D-0020/spec.md

**Acceptance Criteria:**
- `_deviation_counts_reconciled()` exists in `src/superclaude/cli/roadmap/gates.py` at end of file (Constraint 10 merge mitigation)
- Deviation count mismatch between reported and actual findings causes deterministic gate failure (SC-008)
- Existing fidelity gate logic is behaviorally unchanged (no regressions)
- Function is isolated at file end to minimize diff overlap (Constraint 10)
- SC-008 validated: deviation count reconciliation produces deterministic gate failure on mismatch

**Validation:**
- `uv run pytest tests/roadmap/ -k "deviation" -v`
- Evidence: linkable artifact produced at D-0020/spec.md

**Dependencies:** T03.01 (KPI fields provide finding count data)
**Rollback:** Remove `_deviation_counts_reconciled()` from `roadmap/gates.py`
**Notes:** Coordinate timing with concurrent PRs touching `roadmap/gates.py` (Anti-Instincts, Unified Audit Gating). Rebase onto latest master immediately before merge.

---

### Checkpoint: End of Phase 3

**Purpose:** Gate for Phase 4 entry — verify KPI reporting and deviation reconciliation are complete without regressions.
**Checkpoint Report Path:** `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/CP-P03-END.md`
**Verification:**
- KPI reporting includes all 6 wiring metrics (SC-015)
- Deviation count mismatch causes deterministic gate failure (SC-008)
- No merge conflicts or behavioral regressions in existing fidelity gate logic
**Exit Criteria:**
- Both tasks (T03.01-T03.02) completed with deliverables D-0019 and D-0020 produced
- `roadmap/gates.py` modification isolated at file end per Constraint 10
- All existing gate tests still pass (regression check)
