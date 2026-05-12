# 07 - Design Intent and Version History

**Status:** Complete
**Investigator:** Doc Analyst
**Date:** 2026-04-03

## Research Question

What was the INTENDED design for task-level verification in the sprint execution pipeline, based on v3.1 and v3.2 release specs, gap analyses, and outstanding tasklists? Is there a planned but unimplemented verification layer? What do the specs say about per-task execution?

## Context

- Per-task path added in v3.1 (T04 comment at executor.py:1201)
- Post-phase wiring added in v3.2 (T02 comment at executor.py:1222)
- Version tags in executor.py comments confirm this lineage
- Need to compare planned vs implemented verification features

## Source Documents Analyzed

| # | Document | Path |
|---|----------|------|
| 1 | v3.1 Gap Remediation Tasklist | `.dev/releases/complete/v3.1_Anti-instincts__/v3.1/gap-remediation-tasklist.md` |
| 2 | v3.1 Merged Gap Analysis | `.dev/releases/complete/v3.1_Anti-instincts__/v3.1/roadmap-gap-analysis-merged.md` |
| 3 | v3.2 Merged Gap Analysis | `.dev/releases/complete/v3.2_fidelity-refactor___/v3.2/roadmap-gap-analysis-merged.md` |
| 4 | v3.2 Outstanding Tasklist | `.dev/releases/complete/v3.2_fidelity-refactor___/outstanding-tasklist.md` |
| 5 | Sprint CLI Release Guide | `docs/generated/sprint-cli-tools-release-guide.md` |
| 6 | Sprint TUI Reference | `docs/developer-guide/sprint-tui-reference.md` |
| 7 | TurnLedger Cross-Release Summary | `.dev/releases/complete/v3.1_Anti-instincts__/turnledger-integration/cross-release-summary.md` |
| 8 | v3.1 QA Execution Reflection | `.dev/releases/complete/v3.1_Anti-instincts__/v3.1/execution-qa-reflection.md` |
| 9 | v3.2 QA Execution Reflection | `.dev/releases/complete/v3.2_fidelity-refactor___/v3.2/execution-qa-reflection.md` |
| 10 | v3.1 TurnLedger Integration Tasklist | `.dev/releases/complete/v3.1_Anti-instincts__/turnledger-integration/v3.1/tasklist.md` |
| 11 | v3.2 TurnLedger Integration Tasklist | `.dev/releases/complete/v3.1_Anti-instincts__/turnledger-integration/v3.2/tasklist.md` |
| 12 | executor.py (inline comments) | `src/superclaude/cli/sprint/executor.py` |

---

## Finding 1: The Original Sprint Execution Model (Pre-v3.1)

The sprint CLI release guide (`docs/generated/sprint-cli-tools-release-guide.md`) describes the original execution model clearly:

> "For each phase, sprint runtime: (1) launches fresh Claude process, (2) monitors output and updates TUI, (3) enforces timeout/interrupt handling, (4) parses phase result, (5) records dual logs, (6) continues or halts."

This is a **per-phase subprocess model**: one `ClaudeProcess` per phase file, no concept of individual tasks within a phase. The executor launches a Claude process with a prompt like `/sc:task-unified Execute all tasks in @<phase-file>` and monitors it as a single unit.

**Key implication**: Task-level verification was never part of the original design. The executor treated each phase as an opaque unit. Verification happened only at the phase boundary (exit code, EXIT_RECOMMENDATION token, status hints).

---

## Finding 2: v3.1 Planned a Per-Task Execution Layer

### What was planned

The v3.1 gap analysis identified a fundamental architectural mismatch:

- `execute_sprint()` (production) = per-phase subprocess model
- `execute_phase_tasks()` (existed but unreachable) = per-task model with hooks, budget tracking, and gate evaluation

v3.1 Task T04 was the critical architectural fix: "Wire `execute_sprint()` to call `execute_phase_tasks()` for per-task phases." This would add a `_parse_phase_tasks()` helper to detect whether a phase file contains a task inventory, and if so, delegate to the per-task orchestration path.

### What was actually implemented

From the v3.1 QA Execution Reflection:

| Task | Status | Description |
|------|--------|-------------|
| T01 (TurnLedger construction) | [IMPLEMENTED] | Constructed at executor.py:1145 |
| T02 (ShadowGateMetrics construction) | [IMPLEMENTED] | Constructed at executor.py:1151 |
| T03 (DeferredRemediationLog construction) | [IMPLEMENTED] | Constructed at executor.py:1102 |
| T04 (Per-task delegation) | **[DEFERRED]** during v3.1 execution; **[IMPLEMENTED]** later (now at executor.py:1201-1228) |
| T05 (TrailingGateResult wrapping) | **[DEFERRED]** during v3.1 execution; **[IMPLEMENTED]** later (now at executor.py:843) |
| T06 (SprintGatePolicy construction) | [IMPLEMENTED] | Constructed at executor.py:1106 |
| T07 (build_kpi_report call) | [IMPLEMENTED] | Called at executor.py:1416-1423 |
| T08 (attempt_remediation wiring) | [IMPLEMENTED] as Option B (documented deviation, deferred to v3.2) |
| T09-T10 (Documentation) | [IMPLEMENTED] |
| T11 (Integration test) | **[DEFERRED]** | No execute_sprint() integration test exists |
| T12 (Test updates for return types) | **[DEFERRED]** at v3.1 time; status now [UNKNOWN] |
| T13-T14 (Regression + smoke) | **[DEFERRED]** |

### Critical finding: T04 was deferred during v3.1 execution but later implemented

The v3.1 QA reflection from 2026-03-21 shows T04 was SKIPPED. However, executor.py now contains the per-task delegation code at line 1201 with the comment `# v3.1-T04: Per-task delegation`. This means T04 was implemented in a subsequent pass, not during the original v3.1 gap remediation sprint. The `_parse_phase_tasks()` helper also exists at line 1095.

---

## Finding 3: v3.2 Planned Post-Phase Wiring Verification

### What was planned

v3.2 focused on the Wiring Verification Gate -- an analysis engine that detects unwired callables, orphan modules, and registry gaps. Its gap analysis identified 18 gaps across the sprint integration layer.

The v3.2 gap remediation included:

| Task | Description | Status |
|------|-------------|--------|
| T01 (Post-phase wiring hook function) | Create `run_post_phase_wiring_hook()` | [IMPLEMENTED] at executor.py:735-784 |
| T02 (Wire hook into execute_sprint) | Call the hook from the main loop | **[DEFERRED]** during v3.2 execution; **[IMPLEMENTED]** later (now at executor.py:1222, 1432) |
| T03 (Activate `_resolve_wiring_mode()`) | Replace direct field access with scope-based resolution | [IMPLEMENTED] |
| T04 (Shadow findings adapter) | `_log_shadow_findings_to_remediation_log()` | [IMPLEMENTED] at executor.py:614-645 |
| T05 (Wire shadow adapter into hook) | Pass remediation_log through hook chain | [IMPLEMENTED] |
| T06 (`_format_wiring_failure()` helper) | Format wiring failures for remediation prompts | [IMPLEMENTED] at executor.py:653-696 |
| T07 (`_recheck_wiring()` helper) | Post-remediation validation | [IMPLEMENTED] at executor.py:704-727 |
| T08 (BLOCKING remediation lifecycle) | Wire remediation into BLOCKING path | [IMPLEMENTED] with inline approach (Amendment A2 Option B) |
| T09 (SprintConfig scope-based fields) | Replace string mode with scope-based fields | [IMPLEMENTED] |

### Critical finding: T02 was deferred during v3.2 execution but later implemented

The v3.2 QA reflection from 2026-03-21 shows T02 as "PARTIAL / NO -- Critical discrepancy": `run_post_phase_wiring_hook()` was defined but never called. However, executor.py now contains two call sites:
- Line 1222: `# v3.2-T02: Run post-phase wiring hook for per-task phases too`
- Line 1432: `# v3.2-T02: Run post-phase wiring hook for every claude-mode phase`

This means T02 was also implemented in a subsequent pass.

---

## Finding 4: The Outstanding Tasklist Reveals the Remaining Verification Gaps

The outstanding tasklist (`outstanding-tasklist.md`, generated 2026-03-22) consolidates 22 tasks from v3.05, v3.1, and v3.2 gap remediations. Among these are critical verification tasks that were planned but remain unimplemented:

### Blocking verification tasks from the outstanding list

| Outstanding Task | Original | Description | Status |
|-----------------|----------|-------------|--------|
| OT-01 (v3.2-T02) | Wire post-phase hook | 1-line insertion to activate wiring hook | [IMPLEMENTED] (now in executor.py) |
| OT-02 (v3.1-T04) | Per-task delegation | Architectural refactor of execute_sprint() | [IMPLEMENTED] (now in executor.py) |
| OT-03 (v3.1-T05) | TrailingGateResult wrapping | Return type change for gate result accumulation | [IMPLEMENTED] (now in executor.py:843) |

### Integration tests that remain unimplemented

| Outstanding Task | Original | Description | Status |
|-----------------|----------|-------------|--------|
| OT-08 (v3.1-T11) | execute_sprint() integration test | E2E test with mocked ClaudeProcess verifying TurnLedger, ShadowGateMetrics, DeferredRemediationLog, SprintGatePolicy, build_kpi_report | **[DEFERRED]** |
| OT-09 (v3.2-T13) | Budget scenario tests 5-8 | Credit floor, BLOCKING remediation, null-ledger, shadow deferred log | **[DEFERRED]** |
| OT-10 (v3.2-T17) | execute_sprint() TurnLedger threading test | Verify TurnLedger creation, post-phase hook calls, budget debit across phases, shadow findings logged | **[DEFERRED]** |
| OT-11 (v3.2-T18) | `_resolve_wiring_mode()` unit tests | Scope resolution, fallback, grace period, enabled=False | **[DEFERRED]** |
| OT-12 (v3.2-T19) | KPI and contract verification tests | Verify GateKPIReport has all spec fields, net_cost computation, format_report output | **[DEFERRED]** |
| OT-13 (v3.2-T20) | E2E shadow mode pipeline test | Shadow mode -> DeferredRemediationLog -> KPI report chain | **[DEFERRED]** |
| OT-14 (v3.2-T15) | Performance benchmark | p95 < 5s for 50-file packages | **[DEFERRED]** |
| OT-17 (v3.2-T21) | Full regression suite | Run all tests, verify no new failures | **[DEFERRED]** |
| OT-18 (v3.2-T22) | Gap closure audit | Review all 3 gap-remediation tasklists, verify all gaps closed | **[DEFERRED]** |

---

## Finding 5: The TurnLedger Cross-Release Summary Reveals the Intended Architecture

The cross-release summary (`.dev/releases/complete/v3.1_Anti-instincts__/turnledger-integration/cross-release-summary.md`) provides the clearest picture of the intended design. Key architectural decisions:

1. **v3.1 was the prerequisite for everything**: It was supposed to establish:
   - `execute_sprint()` creates a TurnLedger
   - Gate-pass reimbursement activates `reimbursement_rate`
   - `TrailingGateRunner` per-phase in `execute_phase_tasks()`
   - `DeferredRemediationLog` as single failure journal
   - `build_kpi_report()` called at sprint completion
   - `gate_rollout_mode` on SprintConfig

2. **v3.2 was supposed to consume what v3.1 built**:
   - `run_post_task_wiring_hook()` gets `ledger` parameter
   - Wiring gate plugs into same `TrailingGateRunner` + `DeferredRemediationLog`
   - `resolve_gate_mode()` replaces string switches
   - `attempt_remediation()` called from wiring hook

3. **The "dead code" problem was universal**: All 9 adversarial agents across 3 releases independently confirmed that `reimbursement_rate=0.8` was dead code, `SprintGatePolicy` was never instantiated, `attempt_remediation()` was never called from production, `TrailingGateRunner` was disconnected from the sprint loop, and `build_kpi_report()` was never invoked.

4. **The intended verification chain**: `Task execution -> Post-task hook (anti-instinct/wiring) -> TrailingGateResult -> DeferredRemediationLog -> attempt_remediation() -> build_kpi_report()`. This entire chain was designed but the production entry point (`execute_sprint()`) bypassed it.

---

## Finding 6: The Sprint TUI Reference Shows No Task-Level Verification in the UI

The sprint TUI reference (`docs/developer-guide/sprint-tui-reference.md`) describes the TUI architecture with 5 layers (TMUX session, Rich TUI, Output Monitor, Executor Orchestration, Subprocess Layer). The TUI displays phase-level status: phase number, status, exit code, timing.

There is no mention of task-level verification results in the TUI. The `MonitorState` tracks task IDs and tool names from NDJSON output, but this is monitoring data, not verification results. The TUI was designed for the per-phase model, not the per-task model.

**Status**: [UNKNOWN] whether per-task verification results are displayed in the TUI after the v3.1-T04 implementation. The TUI may show per-task progress when `execute_phase_tasks()` is used (it accepts optional `tui` and `monitor` params at executor.py:921-924), but this needs code-level verification.

---

## Finding 7: Verification Layers -- Planned vs Implemented

### Layer 1: Phase-Level Verification (Original)

| Feature | Status | Evidence |
|---------|--------|----------|
| Exit code checking | [IMPLEMENTED] | exit_code==124 -> timeout, non-zero -> error |
| EXIT_RECOMMENDATION parsing | [IMPLEMENTED] | HALT wins over CONTINUE |
| Phase status classification | [IMPLEMENTED] | pass, pass_no_signal, pass_no_report, halt, timeout, error |
| Dual logging (JSONL + Markdown) | [IMPLEMENTED] | logging_.py |

### Layer 2: Per-Task Verification via Anti-Instinct Gate (v3.1)

| Feature | Status | Evidence |
|---------|--------|----------|
| Per-task delegation from execute_sprint() | [IMPLEMENTED] | executor.py:1201 `# v3.1-T04` |
| `_parse_phase_tasks()` helper | [IMPLEMENTED] | executor.py:1095 |
| `run_post_task_anti_instinct_hook()` | [IMPLEMENTED] | executor.py, 4-mode rollout matrix |
| TrailingGateResult creation in hook | [IMPLEMENTED] | executor.py:843 `# v3.1-T05` |
| Gate result accumulation in sprint loop | [IMPLEMENTED] | `all_gate_results` list, extended per phase |
| TurnLedger budget tracking | [IMPLEMENTED] | Construction at 1145, passed to execute_phase_tasks |
| ShadowGateMetrics collection | [IMPLEMENTED] | Construction at 1151, passed to execute_phase_tasks |
| DeferredRemediationLog persistence | [IMPLEMENTED] | Construction at 1102, persist_path under results_dir |
| SprintGatePolicy instantiation | [IMPLEMENTED] | Construction at 1106 |
| build_kpi_report() at sprint end | [IMPLEMENTED] | Called at 1416-1423 |
| `attempt_remediation()` integration | **[DEFERRED]** to v3.3 | Inline fail logic used instead (documented deviation) |
| Integration test for execute_sprint() production path | **[DEFERRED]** | OT-08 in outstanding tasklist |

### Layer 3: Post-Phase Wiring Verification (v3.2)

| Feature | Status | Evidence |
|---------|--------|----------|
| `run_post_phase_wiring_hook()` definition | [IMPLEMENTED] | executor.py:735-784 |
| Hook wired into execute_sprint() main loop | [IMPLEMENTED] | executor.py:1222 (per-task path), 1432 (claude-mode path) |
| `_resolve_wiring_mode()` scope-based resolution | [IMPLEMENTED] | executor.py:421-447, activated at line 475 |
| Shadow findings -> DeferredRemediationLog adapter | [IMPLEMENTED] | `_log_shadow_findings_to_remediation_log()` at 614-645 |
| `_format_wiring_failure()` helper | [IMPLEMENTED] | executor.py:653-696 |
| `_recheck_wiring()` post-remediation validation | [IMPLEMENTED] | executor.py:704-727 |
| BLOCKING remediation lifecycle | [IMPLEMENTED] | Inline approach (Amendment A2 Option B) |
| SprintConfig scope-based fields | [IMPLEMENTED] | models.py:335-336, SHADOW_GRACE_INFINITE=999_999 |
| Budget scenario tests (5-8) | **[DEFERRED]** | OT-09 |
| TurnLedger threading integration test | **[DEFERRED]** | OT-10 |
| `_resolve_wiring_mode()` unit tests | **[DEFERRED]** | OT-11 |
| KPI contract verification tests | **[DEFERRED]** | OT-12 |
| E2E shadow mode pipeline test | **[DEFERRED]** | OT-13 |
| Performance benchmark (p95 < 5s) | **[DEFERRED]** | OT-14 |

### Layer 4: Full Retry-Once Remediation (v3.3 planned)

| Feature | Status | Evidence |
|---------|--------|----------|
| `attempt_remediation()` called from sprint execution | **[DEFERRED]** | Cross-release summary Section 2.1; v3.1 T08 chose Option B |
| `SprintGatePolicy.build_remediation_step()` integration | **[DEFERRED]** | v3.2 gap analysis gap #4: "remediation lifecycle unimplemented" |
| Generic `debit_gate()`/`credit_gate()` methods | **[DEFERRED]** to v3.3 | v3.2 TurnLedger integration tasklist T01 note |

---

## Gaps and Questions

### Open Gaps

1. **No integration test for the production sprint path** (OT-08). The entire verification chain (TurnLedger -> per-task delegation -> anti-instinct hook -> TrailingGateResult -> DeferredRemediationLog -> build_kpi_report) has no end-to-end test exercising `execute_sprint()`. This was identified as critical in v3.1 (T11) and consolidated in the outstanding tasklist, but never implemented. This is the most significant verification gap.

2. **No tests for 8 of 18 outstanding tasks**. The outstanding tasklist has 22 tasks total; the 10 test/verification tasks (OT-08 through OT-18) are all marked as deferred.

3. **`attempt_remediation()` is still dead code in production**. The entire retry-once state machine (`attempt_remediation()`, `SprintGatePolicy.build_remediation_step()`) exists in `pipeline/trailing_gate.py` but is never called from the sprint executor. Both v3.1 and v3.2 chose the simpler inline approach and deferred full remediation to v3.3.

4. **TUI integration with per-task verification is unclear**. The `execute_phase_tasks()` function accepts optional `tui` and `monitor` params, but it is unknown whether per-task gate results (anti-instinct, wiring) are surfaced in the TUI dashboard.

5. **KPI report field coverage is incomplete**. v3.2 gap analysis identified 3 missing KPI fields (`wiring_net_cost`, `wiring_analyses_run`, `wiring_remediations_attempted`) and TurnLedger field naming mismatches.

### Open Questions

1. When were T04/T05 (v3.1) and T02 (v3.2) actually implemented? They were SKIPPED in the 2026-03-21 QA reflections but exist in the current codebase. Was this a subsequent sprint execution pass or manual implementation?

2. Does the current `_parse_phase_tasks()` correctly parse all phase file formats? The v3.1 gap analysis flagged this as "HIGH risk" (Amendment A3) and noted it was unspecified.

3. Are there any tests specifically covering the per-task delegation path in `execute_sprint()`? The outstanding tasklist suggests not (OT-08 is deferred), but new tests may have been added since the outstanding tasklist was generated.

---

## Summary

**The intended design** across v3.1 and v3.2 was a layered verification architecture:

1. **Phase-level** (original): Exit code, EXIT_RECOMMENDATION, status classification
2. **Per-task** (v3.1): Budget-tracked task execution with post-task anti-instinct gate evaluation, TrailingGateResult accumulation, and KPI reporting
3. **Post-phase wiring** (v3.2): Wiring analysis after each phase with shadow/soft/full rollout modes, scope-based resolution, and DeferredRemediationLog integration
4. **Full remediation** (v3.3 planned): Retry-once semantics via `attempt_remediation()` with `SprintGatePolicy.build_remediation_step()`

**Current state**: Layers 1-3 are implemented in the production code path. Layer 4 remains deferred. The critical wiring gap (execute_sprint() not calling execute_phase_tasks()) identified in both v3.1 and v3.2 gap analyses has been resolved. The post-phase wiring hook identified as dead code in the v3.2 QA reflection has been wired in.

**The primary remaining gap** is the complete absence of integration tests for the production sprint path. The outstanding tasklist documents 10 test/verification tasks (OT-08 through OT-18) that are all deferred. This means the verification chain works at the code level but has no automated test coverage confirming it fires correctly from `execute_sprint()`.
