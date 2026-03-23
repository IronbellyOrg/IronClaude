# Merged Roadmap Gap Analysis: v3.2 Wiring Verification Gate

**Date**: 2026-03-21
**Source**: Agent A (code-level verification) + Agent B (phase-by-phase comparison)
**Method**: Adversarial compare-and-merge with disagreement resolution

---

## Agreement Summary

Both agents independently confirmed the following:

1. **Phase 1 (Core Analysis Engine) is fully implemented** — all three analyzers, data models, report emission, and gate definition are present and functional. The implementation exceeds spec in several areas (dual evidence rule, suppression, 16-field frontmatter vs spec's 12).

2. **`_resolve_wiring_mode()` is dead code** — defined at executor.py:420-446 but never called. Production path reads `config.wiring_gate_mode` directly at line 473.

3. **DeferredRemediationLog is not used in shadow mode** — shadow branch only logs via `_wiring_logger.info()`, does not construct `TrailingGateResult` or append to `DeferredRemediationLog`.

4. **Remediation lifecycle is unimplemented** — BLOCKING path debits budget but does not call `SprintGatePolicy.build_remediation_step()`, `_format_wiring_failure()`, `_recheck_wiring()`, or `attempt_remediation()`.

5. **KPI field names diverge from spec** — only ~2 of 6 names match; `wiring_net_cost`, `wiring_analyses_run`, `wiring_remediations_attempted` are missing.

6. **TurnLedger field names diverge from spec** — `wiring_turns_used` vs `wiring_gate_cost`, etc.

7. **SprintConfig scope-based fields not adopted** — `wiring_gate_enabled`, `wiring_gate_grace_period`, `SHADOW_GRACE_INFINITE` are all absent.

8. **`check_wiring_report()` convenience wrapper absent** — spec OQ-10 / Section 6.1.

9. **Frontmatter contract diverges** — 16-field implementation vs 12-field spec, with different names for overlapping fields.

---

## Disagreements & Resolutions

### D1: Is `_resolve_wiring_mode()` PASS or dead code?

- **Agent A**: Flagged as **CRITICAL dead code** — never called, Goal-5d not active.
- **Agent B**: Listed as **PASS** in Phase 2 table ("exists at executor.py:420-446, uses resolve_gate_mode()"), then later flagged as TL-1 gap ("never called from production path").

**Resolution**: Agent A is correct. Existence without invocation is dead code, not PASS. The function was written but never wired in. **Disposition: DEAD CODE (Critical).**

### D2: `execute_sprint()` not threading TurnLedger — Critical or not mentioned?

- **Agent A**: Flagged as **CRITICAL gap #5** — `execute_sprint()` never instantiates a `TurnLedger`, never calls `execute_phase_tasks()`. Production path runs phases as monolithic subprocesses, making all per-task hooks (wiring, anti-instinct) unreachable.
- **Agent B**: Did not identify this gap.

**Resolution**: Agent A identified a structural gap that Agent B missed. The production entry point (`execute_sprint()`) operates at phase granularity and never calls the per-task loop where all TurnLedger hooks live. This is a **fundamental architecture gap** — the wiring gate works in test mode but not in production sprint execution. **Disposition: CRITICAL — Agent A's finding stands.**

### D3: `TrailingGateRunner` not used in `execute_sprint()` — Critical or not mentioned?

- **Agent A**: Flagged as **CRITICAL gap #3** — spec dependency map shows `executor.py` consuming `TrailingGateRunner`, but `execute_sprint()` never instantiates it; gate evaluation is synchronous.
- **Agent B**: Did not independently flag this.

**Resolution**: Related to D2. The synchronous evaluation in `run_post_task_wiring_hook()` is functionally adequate for per-task hooks, but the daemon-thread `TrailingGateRunner` was designed for the production sprint loop. Since `execute_sprint()` does not use per-task hooks at all (D2), this gap is subsumed by D2. **Disposition: MODERATE — secondary to the execute_sprint architecture gap.**

### D4: Migration shim — correct or targeting wrong fields?

- **Agent A**: Flagged as **MODERATE gap #9** — shim migrates `wiring_budget_turns`, `wiring_remediation_cost`, `wiring_scope` instead of spec's `wiring_gate_mode` deprecation path.
- **Agent B**: Listed as **PASS** ("alias mapping exists").

**Resolution**: The migration shim exists but migrates different fields than the spec requires. This is a naming/contract divergence, not a functional failure. **Disposition: MODERATE — migration targets differ from spec.**

### D5: Phase 4/5 — PASS or PARTIAL/MISSING?

- **Agent A**: Marked Phases 4 and 5 as **PRESENT (assumed)** based solely on execution log showing PASS.
- **Agent B**: Marked Phase 4 as **PARTIAL** (missing retrospective validation T11, performance benchmark SC-009, budget scenarios 5-8 not clearly labeled) and Phase 5 as **N/A** (operational, not code artifacts).

**Resolution**: Agent B's analysis is more rigorous. Execution log PASS does not guarantee spec compliance — it means the tests that exist passed, not that all required tests exist. **Disposition: Phase 4 = PARTIAL (Agent B correct), Phase 5 = N/A (operational).**

### D6: `--skip-wiring-gate` CLI flag

- **Agent A**: Not mentioned.
- **Agent B**: Flagged as Low gap #13 — deferred per OQ-5 but still in Phase 2 rollout plan.

**Resolution**: Valid low-priority gap. **Disposition: LOW — deferred per OQ-5.**

---

## Merged Findings

### Confirmed Present (deduplicated)

| # | Feature | Evidence | Notes |
|---|---------|----------|-------|
| 1 | Three analyzers (unwired callables, orphan modules, registries) | `wiring_gate.py:313-665` | AST-based, whitelist-aware |
| 2 | Data models: WiringFinding, WiringReport, WiringConfig, WhitelistEntry | `wiring_gate.py:44-135`, `wiring_config.py:47-71` | Superset of spec |
| 3 | Report emission: `emit_report()` | `wiring_gate.py:715-866` | 16-field frontmatter, yaml.safe_dump(), 7 Markdown sections |
| 4 | Gate definition: `WIRING_GATE` constant | `wiring_gate.py:973-1026` | 5 semantic checks (mode-aware, evolved from spec) |
| 5 | Sprint hook: `run_post_task_wiring_hook()` | `executor.py:449-582` | Shadow/soft/full branches, debit-before-analysis, credit-on-pass |
| 6 | TurnLedger extensions: `debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()` | `models.py:565-599` | Floor-to-zero arithmetic confirmed |
| 7 | TurnLedger fields: 3 wiring tracking fields | `models.py:537-539` | Names differ from spec |
| 8 | SprintConfig wiring fields: mode, scope, analysis_turns, remediation_cost | `models.py:321-329` | Mode string-switch instead of spec's bool+scope pattern |
| 9 | Migration shim | `models.py:340-355` | Targets differ from spec |
| 10 | Null-ledger compatibility | `executor.py:479-484` | All ledger ops guarded |
| 11 | KPI reporting: `GateKPIReport` with wiring fields, `build_kpi_report()` | `kpi.py:47-52, 137-144` | 6 fields, names differ from spec |
| 12 | Deviation reconciliation: `_deviation_counts_reconciled()` | `roadmap/gates.py:702` | Wired into SPEC_FIDELITY_GATE |
| 13 | Safeguard checks: `run_wiring_safeguard_checks()` | SC-010, SC-011 | Pre-activation validation |
| 14 | SprintGatePolicy class | Concrete TrailingGatePolicy implementation | Present but not used in remediation path |
| 15 | Three-type whitelist | `wiring_config.py:74-151` | All finding types, mode-aware validation |
| 16 | Dual evidence rule in orphan analysis | `wiring_gate.py:393-516` | Beyond spec |
| 17 | Test suite | `tests/audit/test_wiring_gate.py`, `test_wiring_analyzer.py`, `test_wiring_integration.py`, `test_eval_wiring_multifile.py` | Plus fixtures directory |

### Confirmed Missing/Bugs (deduplicated, severity-rated)

| # | Gap | Severity | Both Agents? | Notes |
|---|-----|----------|-------------|-------|
| 1 | `execute_sprint()` does not create or thread a TurnLedger — production path never calls `execute_phase_tasks()`, making all per-task hooks unreachable | **CRITICAL** | A only | Architectural: two execution models, only the test-mode one has hooks |
| 2 | `_resolve_wiring_mode()` is dead code — never called from `run_post_task_wiring_hook()` | **CRITICAL** | Both | Goal-5d (scope-based mode resolution) is specced but not active |
| 3 | DeferredRemediationLog not used in shadow mode — findings invisible to trailing gate pipeline | **CRITICAL** | Both | Breaks evidence-driven rollout chain (Gamma IE-4) |
| 4 | Remediation lifecycle unimplemented — BLOCKING path debits budget but performs no actual remediation | **CRITICAL** | Both | `_format_wiring_failure()`, `_recheck_wiring()`, `SprintGatePolicy.build_remediation_step()` all absent |
| 5 | `attempt_remediation()` from trailing_gate.py not called — full retry-once semantics unused | **CRITICAL** | A only (explicit) | Subsumes gap #4; existing infrastructure disconnected |
| 6 | SprintConfig scope-based fields not adopted — `wiring_gate_enabled`, `wiring_gate_grace_period`, `SHADOW_GRACE_INFINITE` absent | **HIGH** | Both | Old `wiring_gate_mode` string-switch persists |
| 7 | KPI: 3 spec fields missing — `wiring_net_cost`, `wiring_analyses_run`, `wiring_remediations_attempted` | **MEDIUM** | Both | Plus naming divergence on remaining fields |
| 8 | TurnLedger field naming mismatch — `wiring_gate_cost`/`wiring_gate_credits`/`wiring_gate_scope` not used | **MEDIUM** | Both | Functionally equivalent but contract-breaking |
| 9 | WIRING_GATE frontmatter contract divergence — 16 fields with different names vs spec's 12 | **MEDIUM** | Both | Implementation is richer; recommend updating spec |
| 10 | Migration shim targets wrong fields — migrates internal renames, not spec's deprecation path | **MEDIUM** | A only | B marked PASS incorrectly |
| 11 | `_format_wiring_failure()` helper absent | **MEDIUM** | Both | Required for remediation prompt formatting |
| 12 | `_recheck_wiring()` helper absent | **MEDIUM** | Both | Required for post-remediation validation |
| 13 | Budget Scenarios 5-8 not clearly mapped to dedicated test cases | **MEDIUM** | B only | Credit floor, BLOCKING remediation, null-ledger, shadow deferred log |
| 14 | Retrospective validation artifact (T11) missing | **LOW** | B only | No report confirming detection of original cli-portify bug |
| 15 | Performance benchmark (SC-009) missing | **LOW** | B only | p95 < 5s for 50-file packages not tested |
| 16 | `check_wiring_report()` convenience wrapper absent | **LOW** | Both | Spec Section 6.1 / OQ-10 |
| 17 | `--skip-wiring-gate` CLI flag absent | **LOW** | B only | Deferred per OQ-5 |
| 18 | `TrailingGateRunner` not used in `execute_sprint()` | **LOW** | A only | Subsumed by gap #1; synchronous eval adequate if hooks fire |

### TurnLedger Wiring Status (merged)

| ID | Gap | Status | Impact |
|----|-----|--------|--------|
| TL-0 | `execute_sprint()` never creates a TurnLedger or calls per-task hooks | **OPEN — CRITICAL** | All TurnLedger integration is unreachable in production |
| TL-1 | `_resolve_wiring_mode()` is dead code | **OPEN — CRITICAL** | Scope-based mode resolution never executes |
| TL-2 | Shadow mode does not log to DeferredRemediationLog | **OPEN — CRITICAL** | Shadow findings invisible to remediation pipeline |
| TL-3 | BLOCKING remediation is debit-only (no subprocess, no recheck) | **OPEN — CRITICAL** | Budget consumed but no remediation occurs |
| TL-4 | TurnLedger field naming mismatch (3 fields) | **OPEN — MEDIUM** | Contract divergence, not functional failure |
| TL-5 | GateKPIReport missing 3 of 6 spec fields | **OPEN — MEDIUM** | Incomplete KPI surface area |

### Root Cause Analysis (merged)

**RCA-1: Two execution models, one integration point** (Agent A primary, Agent B silent)
The codebase has a phase-level production path (`execute_sprint()`) and a task-level test path (`execute_phase_tasks()`). The v3.2 wiring gate was designed for the task-level path. The production entry point runs monolithic Claude subprocesses per phase and never enters the per-task loop where TurnLedger hooks live. This is the root cause of TL-0 and cascades into all other TurnLedger gaps.

**RCA-2: Spec evolution not propagated to call sites** (Both agents)
`_resolve_wiring_mode()` was written as a bridge from old string-switch to new scope-based resolution, but the call site in `run_post_task_wiring_hook()` was never updated to use it. Classic "wrote the function, forgot to wire it" pattern.

**RCA-3: Remediation path stubbed, not implemented** (Both agents)
The BLOCKING path implements the economic model (debit budget) without the behavioral model (spawn remediation, recheck, credit on success). The spec's `_format_wiring_failure()`, `_recheck_wiring()`, and `SprintGatePolicy.build_remediation_step()` are all unwritten. Given the 24-minute sprint execution, the implementer prioritized analysis engine + shadow integration over full remediation.

**RCA-4: Naming divergence cascaded from OQ decisions** (Agent B primary)
The roadmap's OQ resolutions (extended whitelist, added `files_skipped`, etc.) were implemented but not reconciled back to formal spec contracts. This created a naming drift across frontmatter, KPI, TurnLedger, and SprintConfig fields.

**RCA-5: DeferredRemediationLog integration overlooked** (Both agents)
Shadow mode was implemented as a logging-only path, missing the spec's explicit adapter (Gamma IE-4) that feeds findings into the trailing gate pipeline via `DeferredRemediationLog`. This breaks the evidence chain for rollout promotion decisions.

---

## Recommendations (priority-ordered)

### P0 — Blocking for v3.2 release

1. **Wire `execute_sprint()` to TurnLedger** — Either (A) refactor to call `execute_phase_tasks()` for per-task execution, or (B) create a TurnLedger and call post-phase hooks after each subprocess completes. Without this, the entire wiring gate is test-only.

2. **Activate `_resolve_wiring_mode()`** — Replace `mode = config.wiring_gate_mode` at executor.py:473 with `mode = _resolve_wiring_mode(config)`. One-line fix that enables Goal-5d.

3. **Wire DeferredRemediationLog into shadow mode** — Construct synthetic `TrailingGateResult` from wiring findings and append to `DeferredRemediationLog`. Required for rollout validation evidence chain.

4. **Fix BLOCKING remediation: implement or remove debit** — Either (A) implement `_format_wiring_failure()` + `_recheck_wiring()` + `SprintGatePolicy.build_remediation_step()`, or (B) remove the `ledger.debit(config.remediation_cost)` call to stop debiting for non-existent remediation. Option (B) is safer for v3.2; option (A) can defer to v3.3.

### P1 — Should fix

5. **Add SprintConfig scope-based fields** — `wiring_gate_enabled: bool`, `wiring_gate_grace_period: int`, `SHADOW_GRACE_INFINITE = 999_999`. Add `__post_init__` deriving `wiring_gate_mode` for backward compatibility.

6. **Add missing KPI fields** — `wiring_net_cost` (computed), `wiring_analyses_run` (counter), `wiring_remediations_attempted` (counter).

7. **Align frontmatter contract** — Recommend updating spec to match implementation's richer 16-field schema, since the implementation is a functional superset.

### P2 — Nice to have

8. **Add `check_wiring_report()` convenience wrapper** — Single function calling all 5 semantic checks.

9. **Add labeled budget scenario tests 5-8** — Explicit test methods for credit floor, BLOCKING remediation, null-ledger, shadow deferred log.

10. **Add retrospective validation artifact (T11)** — Run wiring gate against actual `cli_portify/` to confirm original bug detection.

11. **Add performance benchmark test (SC-009)** — Assert p95 < 5s for 50-file packages.

12. **Fix migration shim targets** — Align with spec's deprecation path or document intentional divergence.

---

## Final Verdict

- **Implementation completeness**: **62%**
  - Core analysis engine: ~95% (fully working, naming deviations only)
  - Sprint integration: ~45% (hooks exist but unreachable in production; dead code; remediation unimplemented)
  - KPI/deviation reconciliation: ~70% (functional but naming mismatches, missing 3 fields)
  - Integration testing: ~60% (tests exist but specific scenarios missing, no benchmark)
  - Rollout validation: N/A (operational, not code)

- **Critical bugs**: **4**
  1. `execute_sprint()` does not thread TurnLedger (production path bypasses all hooks)
  2. `_resolve_wiring_mode()` is dead code (scope-based resolution never executes)
  3. DeferredRemediationLog not used in shadow mode (findings invisible to pipeline)
  4. BLOCKING remediation debits budget but performs no remediation (debit without delivery)

- **Blocking gaps**: **4** (same as critical bugs — all must be resolved before v3.2 can ship with TurnLedger integration claims)
