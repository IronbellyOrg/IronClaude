# Validation Report
Generated: 2026-03-20
Roadmap: `.dev/releases/current/v3.2_fidelity-refactor___/roadmap.md`
Phases validated: 5
Agents spawned: 10
Total findings: 12 (High: 3, Medium: 7, Low: 2)
Dismissed: 6 (false positives — OQ-9 resolution backs whitelist extension to all finding types)

## Findings

### High Severity

#### H1. T02.03 — `wiring_gate_mode` contradicts `resolve_gate_mode()` architecture
- **Severity**: High
- **Affects**: phase-2-tasklist.md / T02.03
- **Problem**: Task adds `wiring_gate_mode` as a SprintConfig field, but the roadmap explicitly states `resolve_gate_mode(scope, grace_period)` replaces string-switch `wiring_gate_mode` (Goal-5d). Adding it as a config field contradicts the architectural decision.
- **Roadmap evidence**: "Architectural note: Mode resolution via `resolve_gate_mode(scope, grace_period)` replaces string-switch `wiring_gate_mode` (Goal-5d)."
- **Tasklist evidence**: T02.03 Step 3: "Add 3 SprintConfig fields: `wiring_gate_mode`, `wiring_analysis_turns`, `remediation_cost`"
- **Exact fix**: Replace `wiring_gate_mode` with the actual config inputs required by `resolve_gate_mode()` (e.g., `wiring_gate_scope`, `wiring_grace_period`). Update acceptance criteria to reference the `resolve_gate_mode()` architecture.

#### H2. T02.08 — Test scope drift from tracking to budget-check API
- **Severity**: High
- **Affects**: phase-2-tasklist.md / T02.08
- **Problem**: The third test validates `can_run_wiring_gate()` (a budget-check API) instead of `debit_wiring`/`credit_wiring` tracking as the roadmap specifies. All 3 tests should be about TurnLedger tracking.
- **Roadmap evidence**: "debit_wiring/credit_wiring tracking | FR: T06 addendum | 3" and "Acceptance: SC-012, SC-013 validated."
- **Tasklist evidence**: T02.08 Step 4: "Write test: `can_run_wiring_gate()` returns False when budget exhausted, True otherwise"
- **Exact fix**: Replace `can_run_wiring_gate()` test with a third `debit_wiring`/`credit_wiring` tracking test (e.g., sequential debit+credit cycle tracking). Change acceptance from "debit/credit/budget-check semantics" to "debit_wiring/credit_wiring tracking semantics with explicit floor-to-zero assertions (SC-012, SC-013)."

#### H3. T05.02 — FPR manageability criterion weakened
- **Severity**: High
- **Affects**: phase-5-tasklist.md / T05.02
- **Problem**: Acceptance says "FPR documented" but the roadmap requires FPR to be shown as "manageable through `wiring_whitelist.yaml`" — the actual promotion criterion.
- **Roadmap evidence**: "Promotion criteria: FPR manageable through wiring_whitelist.yaml; no regression against legacy ledger is None paths"
- **Tasklist evidence**: T05.02 Acceptance: "FPR burden documented: whitelist adequacy assessed against real finding data"
- **Exact fix**: Replace first acceptance bullet with: "False-positive rate shown to be manageable through `wiring_whitelist.yaml` with evidence from real finding data"

### Medium Severity

#### M1. T01.01 — Missing default `provider_dir_names` in acceptance
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.01
- **Problem**: Task omits the roadmap-required conservative defaults for `provider_dir_names`.
- **Roadmap evidence**: "Default `provider_dir_names` set conservatively (`steps/`, `handlers/`, `validators/`, `checks/`)."
- **Tasklist evidence**: T01.01 acceptance mentions `WiringConfig` but not specific defaults.
- **Exact fix**: Add acceptance bullet: "`WiringConfig` provides conservative default `provider_dir_names`: `steps/`, `handlers/`, `validators/`, `checks/`"

#### M2. T01.02 — Parse degradation observability weakened
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.02
- **Problem**: Acceptance mentions "per-file parse error handling" but omits the structured observability event requirement (file path, parse reason, files-skipped count) and `analysis_complete` propagation.
- **Roadmap evidence**: "Degraded analysis state must be treated as an observability event — emit a structured warning with file path, parse reason, and files-skipped count"
- **Tasklist evidence**: T01.02 Acceptance bullet 4 says "Parse errors are caught per-file with structured warning emission; `files_skipped` count is accurate"
- **Exact fix**: Expand to: "Parse errors emit structured warning with file path, parse reason, and files-skipped count; `analysis_complete` reflects whether all files parsed; `files_skipped: N` propagated to report frontmatter"

#### M3. T02.02 — Invented field names without spec traceability
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.02
- **Problem**: Step 3 hard-codes field names (`wiring_turns_used`, `wiring_turns_credited`, `wiring_budget_exhausted`) without roadmap source.
- **Roadmap evidence**: Milestone 2.1 specifies "3 new fields" but does not define their names.
- **Tasklist evidence**: T02.02 Step 3 names specific fields.
- **Exact fix**: Qualify step with "field names to be defined in T02.01 decision record" or soften to "Add 3 new TurnLedger fields per T02.01 resolution"

#### M4. T02.04 — Missing helper functions and null-ledger traceability
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.04
- **Problem**: Task omits FR: T07b-f (helper functions) from deliverables and does not cross-reference null-ledger compat split to T02.07.
- **Roadmap evidence**: Milestone 2.2 includes "Helper functions | FR: T07b-f" and "Null-ledger compat | FR: T07b-e, NFR-004"
- **Tasklist evidence**: T02.04 acceptance covers hook, mode resolution, callable interface, budget check, but not helper functions.
- **Exact fix**: Add to deliverables: "Helper functions required by the hook (FR: T07b-f)". Add note: "Null-ledger compatibility split to T02.07 per FR: T07b-e."

#### M5. T02.08 — Invented "reimbursement consumed" terminology
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.08
- **Problem**: Acceptance uses "Reimbursement consumed tracking validated (SC-013)" which is not roadmap terminology.
- **Roadmap evidence**: Roadmap uses `debit_wiring`/`credit_wiring` tracking and SC-013.
- **Tasklist evidence**: T02.08 Acceptance: "Reimbursement consumed tracking validated (SC-013)"
- **Exact fix**: Replace with: "`debit_wiring`/`credit_wiring` tracking validated (SC-013)"

#### M6. T03.02 — Missing explicit SC-008 in acceptance
- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.02
- **Problem**: Acceptance omits "SC-008 validated" which the roadmap explicitly requires.
- **Roadmap evidence**: "Acceptance: SC-008 validated."
- **Tasklist evidence**: T03.02 acceptance lists function placement, gate failure, no regressions, but not SC-008.
- **Exact fix**: Add acceptance bullet: "SC-008 validated: deviation count reconciliation produces deterministic gate failure on mismatch"

#### M7. T05.01 — Weakened baseline evaluation criteria
- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.01
- **Problem**: Acceptance compresses roadmap's 4 evaluation items into abbreviated list.
- **Roadmap evidence**: "Collect and evaluate: Findings volume per analysis run, Whitelist usage and coverage, Zero-findings anomalies (SC-011 warnings), p95 runtime under real workloads"
- **Tasklist evidence**: T05.01 Acceptance: "Findings volume, whitelist usage, and zero-findings anomalies documented"
- **Exact fix**: Expand to explicitly list all 4 evaluation items with "per analysis run" qualifier on findings volume

### Low Severity

#### L1. T03.01 — Invented "floor-to-zero surfaced in KPI"
- **Severity**: Low
- **Affects**: phase-3-tasklist.md / T03.01
- **Problem**: R7 mitigation mentions KPI surfacing but it's in the Phase 2 context, not as a Phase 3 acceptance criterion.
- **Roadmap evidence**: Phase 3 Milestone 3.1 acceptance is only "SC-015 validated"
- **Tasklist evidence**: T03.01 Acceptance: "Floor-to-zero credit behavior surfaced in KPI output"
- **Exact fix**: Remove "floor-to-zero surfaced in KPI" from acceptance; SC-015 validation is sufficient

#### L2. T04.04 — Missing "50-file package" in acceptance
- **Severity**: Low
- **Affects**: phase-4-tasklist.md / T04.04
- **Problem**: Acceptance omits the specific "50-file package" qualifier from the roadmap.
- **Roadmap evidence**: "Benchmark on 50-file package | NFR-001, SC-009 | p95 < 5s"
- **Tasklist evidence**: T04.04 Acceptance: "Benchmark run against 50-file package completes with p95 < 5s"
- **Exact fix**: Already present in acceptance bullet 1 — no fix needed (false positive from agent)

## Verification Results
Verified: 2026-03-20
Findings resolved: 11/11 (1 N/A — false positive)

| Finding | Status | Notes |
|---------|--------|-------|
| H1 | RESOLVED | `wiring_gate_mode` removed from T02.03; replaced with `wiring_gate_scope` + `resolve_gate_mode()` reference |
| H2 | RESOLVED | `can_run_wiring_gate()` test replaced with tracking cycle test in T02.08 |
| H3 | RESOLVED | FPR criterion now requires manageability through `wiring_whitelist.yaml` |
| M1 | RESOLVED | Conservative default `provider_dir_names` added to T01.01 acceptance |
| M2 | RESOLVED | Parse degradation expanded with `analysis_complete` and full observability chain |
| M3 | RESOLVED | Field names qualified with "per T02.01 decision record" |
| M4 | RESOLVED | Helper functions and null-ledger cross-reference added to T02.04 deliverable |
| M5 | RESOLVED | "Reimbursement consumed" replaced with `debit_wiring`/`credit_wiring` tracking |
| M6 | RESOLVED | SC-008 validated added to T03.02 acceptance |
| M7 | RESOLVED | Baseline evaluation expanded to all 4 roadmap items |
| L1 | RESOLVED | "Floor-to-zero surfaced in KPI" removed from T03.01 |
| L2 | N/A | False positive — "50-file package" was already present in acceptance bullet 1 |
