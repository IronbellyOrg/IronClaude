# Validation Report
Generated: 2026-03-20
Roadmap: `.dev/releases/current/v3.05_DeterministicFidelityGates/roadmap.md`
Phases validated: 6
Agents spawned: 12 (10 completed, 2 timed out)
Total findings: 14 (High: 2, Medium: 8, Low: 4)

## Findings

### High Severity

#### H1. T01.06 missing ParseWarning population test
- **Severity**: High
- **Affects**: phase-1-tasklist.md / T01.06
- **Problem**: Task omits roadmap exit criterion requiring `ParseWarning` list to be correctly populated. Without this test, parser degradation behavior is untested.
- **Roadmap evidence**: Phase 1 exit criteria: "ParseWarning list correctly populated for malformed inputs"
- **Tasklist evidence**: T01.06 acceptance criteria list tests for extraction types and round-trip but not ParseWarning population
- **Exact fix**: Add acceptance criterion: "`ParseWarning` entries produced and correctly populated for malformed YAML, irregular tables, and missing language tags"

#### H2. T04.03 missing token budget and YAML parse failure requirements
- **Severity**: High
- **Affects**: phase-4-tasklist.md / T04.03
- **Problem**: Task omits FR-4.1 token budget (~3,800 per finding, cap 5,000) and YAML parse failure fallback (scores default to 0). These are explicitly required by the spec.
- **Roadmap evidence**: "Token budget: ~3,800 per finding (hard cap: 5,000)" and "YAML parse failure: all rubric scores default to 0 for that side"
- **Tasklist evidence**: T04.03 deliverable text does not mention token budget cap or YAML parse failure behavior
- **Exact fix**: Add to T04.03 acceptance criteria: "Token budget per finding ~3,800 (hard cap 5,000)" and "YAML parse failure defaults all rubric scores to 0 for that side"

### Medium Severity

#### M1. T01.05 weakened backward-compat mechanism
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.05
- **Problem**: Task mentions Finding extension but doesn't explicitly require default values as the backward-compat mechanism, and doesn't enumerate RegressionResult/RemediationPatch field contracts.
- **Roadmap evidence**: "all defaulted for backward compat" and specific field lists for RegressionResult and RemediationPatch
- **Tasklist evidence**: T01.05 deliverable says "rule_id: str = '', spec_quote: str = '', roadmap_quote: str = ''" (actually present in acceptance criteria)
- **Exact fix**: Already addressed in acceptance criteria. No change needed — agent finding was based on summary text, not full task body.

#### M2. T03.01 under-specifies RunMetadata fields
- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.01
- **Problem**: RunMetadata deliverable says "split HIGH counts" but omits explicit mention of `run_number`, `timestamp`, `spec_hash`, `roadmap_hash`.
- **Roadmap evidence**: "run_number, timestamp, spec_hash, roadmap_hash, structural_high_count, semantic_high_count, total_high_count"
- **Tasklist evidence**: D-0018 says "Run metadata with structural_high_count, semantic_high_count, total_high_count"
- **Exact fix**: Expand D-0018 to: "RunMetadata with run_number, timestamp, spec_hash, roadmap_hash, structural_high_count, semantic_high_count, total_high_count"

#### M3. T03.03 missing prior findings summary field names
- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.03
- **Problem**: Summary text says "prior findings summary" without specifying required fields (ID, severity, status, run_number).
- **Roadmap evidence**: "Prior findings summary for semantic prompts: ID, severity, status, run_number"
- **Tasklist evidence**: T03.03 deliverable mentions "prior findings summary (max 50, oldest-first truncation)"
- **Exact fix**: Expand to "prior findings summary (ID, severity, status, run_number; max 50, oldest-first truncation)"

#### M4. T05.03 missing explicit SPEC_FIDELITY_GATE exclusion
- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.03
- **Problem**: Task mentions convergence branch but doesn't explicitly state that SPEC_FIDELITY_GATE is excluded in convergence mode and DeviationRegistry is sole authority.
- **Roadmap evidence**: "Convergence mode: DeviationRegistry authoritative, SPEC_FIDELITY_GATE excluded"
- **Tasklist evidence**: T05.03 acceptance criteria says "convergence result mapped to StepResult" but doesn't mention SPEC_FIDELITY_GATE exclusion
- **Exact fix**: Add acceptance criterion: "In convergence mode, SPEC_FIDELITY_GATE is NOT invoked; DeviationRegistry is sole pass/fail authority"

#### M5. T06.01 missing cross-file coherence check
- **Severity**: Medium
- **Affects**: phase-6-tasklist.md / T06.01
- **Problem**: Task omits roadmap's "Post-execution cross-file coherence check" requirement.
- **Roadmap evidence**: "Post-execution coherence check: if a file's patches succeed but shares cross-file findings with a failed file, coherence pass evaluates rollback"
- **Tasklist evidence**: T06.01 steps mention "per-file rollback" but not cross-file coherence
- **Exact fix**: Add step: "Post-execution cross-file coherence check: evaluate whether successful-file patches should be rolled back when related files fail"

#### M6. T06.01 missing snapshot/restore retention
- **Severity**: Medium
- **Affects**: phase-6-tasklist.md / T06.01
- **Problem**: Task omits explicit requirement to retain existing snapshot/restore mechanism.
- **Roadmap evidence**: "Existing snapshot/restore mechanism retained"
- **Tasklist evidence**: Not mentioned in T06.01
- **Exact fix**: Add acceptance criterion: "Existing snapshot/restore mechanism (create_snapshots/restore_from_snapshots/cleanup_snapshots) retained for per-file rollback"

#### M7. T06.08 OQ numbering mismatch
- **Severity**: Medium
- **Affects**: phase-6-tasklist.md / T06.08
- **Problem**: Task says "OQ-1 through OQ-5" but roadmap Milestone 6.6 lists OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6. The numbering doesn't match.
- **Roadmap evidence**: Milestone 6.6: "OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b (FR-4.1 threshold calibration), OQ-6 (cross-file coherence)"
- **Tasklist evidence**: T06.08 says "OQ-1 through OQ-5"
- **Exact fix**: Replace "OQ-1 through OQ-5" with "OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6" and expand deliverable to cover all 6

#### M8. T06.03 wiring-verification bypass not in roadmap Milestone 6.3
- **Severity**: Medium
- **Affects**: phase-6-tasklist.md / T06.03
- **Problem**: Task adds "wiring-verification bypass preserved" which is not stated in Milestone 6.3 (it's from FR-7 spec, not the roadmap milestone).
- **Roadmap evidence**: Milestone 6.3 says "Wire structural → semantic → convergence → remediation; verify steps 1-7/9 unaffected; convergence result → StepResult"
- **Tasklist evidence**: T06.03 acceptance criteria includes "Wiring-verification bypass preserved in convergence mode"
- **Exact fix**: Acceptable to keep (it's from the spec FR-7, which the roadmap references). Mark as advisory — no change required.

### Low Severity

#### L1. T01.01 summary text weaker than roadmap specifics
- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.01
- **Problem**: Summary uses generic "TurnLedger API verification" instead of naming specific methods. However, the full task body does list all methods explicitly.
- **Exact fix**: No change needed — full task body is specific.

#### L2. T02.02/T02.03 machine keys from spec not roadmap
- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.02, T02.03
- **Problem**: Specific mismatch machine keys (phantom_id, function_missing, etc.) come from the spec FR-3 table, not the roadmap text itself. However, the roadmap references FR-3 and the spec is authoritative.
- **Exact fix**: No change needed — spec is authoritative source for machine keys.

#### L3. T01.07 uses "Gate A" label from roadmap
- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.07
- **Problem**: Agent flagged "Gate A" as invented, but roadmap explicitly says "Gate A — Parser Certified."
- **Exact fix**: No change needed — label is in roadmap.

#### L4. T04.05 "15% budget" constraint
- **Severity**: Low
- **Affects**: phase-4-tasklist.md / T04.05
- **Problem**: Agent flagged "15% budget" as unsupported. However, FR-4.2 spec defines 15% prior summary allocation. The roadmap references FR-4.2.
- **Exact fix**: No change needed — derived from spec FR-4.2.

---

## Verification Results
Verified: 2026-03-20
Findings resolved: 7/7 actionable (H1, H2, M2, M4, M5, M6, M7)

| Finding | Status | Notes |
|---------|--------|-------|
| H1 | RESOLVED | ParseWarning population test added to T01.06 acceptance criteria |
| H2 | RESOLVED | Token budget cap and YAML parse failure added to T04.03 acceptance criteria |
| M1 | RESOLVED | Already addressed in full task body (agent checked summary only) |
| M2 | RESOLVED | D-0018 in tasklist-index.md expanded with all 7 RunMetadata fields |
| M3 | RESOLVED | Already addressed in full task body (ID/severity/status/run_number present) |
| M4 | RESOLVED | SPEC_FIDELITY_GATE exclusion added to T05.03 acceptance criteria |
| M5 | RESOLVED | Cross-file coherence check added to T06.01 acceptance criteria |
| M6 | RESOLVED | Snapshot/restore retention added to T06.01 acceptance criteria |
| M7 | RESOLVED | OQ numbering corrected to OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6 in T06.08 |
| M8 | RESOLVED | Advisory — wiring-verification bypass from spec FR-7, acceptable |
| L1 | RESOLVED | No change needed — full task body is specific |
| L2 | RESOLVED | No change needed — spec is authoritative |
| L3 | RESOLVED | No change needed — "Gate A" is in roadmap |
| L4 | RESOLVED | No change needed — derived from spec FR-4.2 |
