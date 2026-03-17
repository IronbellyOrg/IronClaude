# Variant 1: Skeptical Architect Review

**Reviewer persona**: Skeptical systems architect
**Source document**: `delta-analysis-post-v2.26.md`
**Date**: 2026-03-17
**Method**: Independent codebase verification of every file:line citation, severity rating, and proposed spec change

---

## 1. Finding Accuracy

### Delta 2.1 -- Spec-patch auto-resume still present

**Original claim**: `roadmap/executor.py:1193-1322` still implements `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()`, bounded to 1 cycle (`executor.py:1216-1223`).

**Challenge**: Verified. `_apply_resume_after_spec_patch()` exists at lines 1193-1322. The recursion guard at line 1217 (`if cycle_count >= 1`) confirms the 1-cycle bound. The function is functional code, not dead code -- it reads state, rewrites spec_hash, rebuilds steps, and re-executes the pipeline. However, the delta says "assumed retired" based on "v2.26 approved-immediate" language. I have not been given the approved-immediate document to verify that it "explicitly retire[s]" this cycle. The function could be intentionally preserved as a transitional mechanism rather than forgotten code. The delta conflates "spec says retire" with "code is wrong" -- but if the retirement is scheduled for a future phase, the code's presence is expected, not a delta.

**Verdict**: OVERSTATED. The code exists as described, but calling it a "Phase 0 blocker" assumes the retirement was supposed to happen already. Without the approved-immediate document's exact language, this could be planned-but-not-yet-executed rather than a forgotten artifact.

---

### Delta 2.2 -- DEVIATION_ANALYSIS_GATE defined but not wired

**Original claim**: `DEVIATION_ANALYSIS_GATE` is fully defined at `roadmap/gates.py:712-758` with strong semantic checks, but `_build_steps()` at `roadmap/executor.py:343-440` does not include a `deviation-analysis` step. The gate exists in `ALL_GATES` at `roadmap/gates.py:760-774` but has no wiring.

**Challenge**: Verified with one correction. The gate is defined at lines 712-758 and is listed in `ALL_GATES` at line 771 as `("deviation-analysis", DEVIATION_ANALYSIS_GATE)`. The `_build_steps()` function at lines 343-440 builds 8 steps (extract through spec-fidelity) and does not include deviation-analysis. Furthermore, the roadmap executor's imports at lines 27-38 import 10 gate constants but NOT `DEVIATION_ANALYSIS_GATE`. This confirms unwired status.

However, the `_check_annotate_deviations_freshness()` function at executor.py:588-675 does reference `deviation-analysis` as a gate_pass_state key (line 669), meaning the executor is already aware of the gate conceptually -- it resets the deviation-analysis gate state on hash mismatch. This partial awareness was not noted by the delta analysis. The gate is not fully unwired; it is partially anticipated but not yet given a step.

**Verdict**: ACCURATE. The finding is factually correct that the gate has no execution step, though it understates the partial wiring that already exists in the freshness check.

---

### Delta 2.3 -- max_turns=100 changes timeout budget arithmetic

**Original claim**: Formula is `max_turns * 120 + 300` for subprocess timeout. At default 100: 12,300 s (3h 25m). Remediation step: `max_turns * 60 = 6,000 s (1h 40m)`.

**Challenge**: Verified. `sprint/process.py:115` uses `timeout_seconds=config.max_turns * 120 + 300`. `sprint/executor.py:479` uses the same formula. `SprintGatePolicy.build_remediation_step()` at executor.py:78 uses `timeout_seconds=self._config.max_turns * 60`. `pipeline/models.py:175` sets `max_turns: int = 100`, and `sprint/models.py:294` also defaults to `max_turns: int = 100`. The arithmetic checks out: 100 * 120 + 300 = 12,300 s = 3h 25m; 100 * 60 = 6,000 s = 1h 40m.

The claim that "the spec did not know the formula" is reasonable -- this is reporting a concrete value that was previously TBD.

**Verdict**: ACCURATE.

---

### Delta 2.4 -- reimbursement_rate=0.8 is a dead model field

**Original claim**: `sprint/models.py:482-487` defines `reimbursement_rate = 0.8` in `TurnLedger` but it is unused in any formula.

**Challenge**: Partially verified. The field is at line 485 (not 482-487; the range 482-487 covers `initial_budget` through `minimum_remediation_budget`). Grep confirms `reimbursement_rate` appears only in `sprint/models.py:485` as a definition. However, `reimbursement_amount` (a different field on `TaskResult` at line 169) IS used in `sprint/process.py:290` and `sprint/models.py:199-200`. The delta correctly identifies `reimbursement_rate` as unused, but the naming similarity with `reimbursement_amount` (which IS used) suggests an intentional but incomplete design: the rate was meant to compute the amount. The delta calls this "an implementation correctness risk" -- but unused fields in dataclasses are not correctness risks; they are technical debt. No code path reads this field, so no computation can be wrong because of it.

**Verdict**: OVERSTATED. The field is indeed unused, but calling it a "correctness risk" overstates the impact. Dead fields cannot produce incorrect results. The real risk is confusion during future implementation, which is a maintainability concern, not a correctness concern.

---

### Delta 2.5 -- STRICT/STANDARD gate tier semantics differ from spec's STRICT/STANDARD

**Original claim**: In `pipeline/gates.py:20-69`, STRICT/STANDARD controls validation depth, not blocking behavior. Both tiers block equally because `grace_period=0` by default.

**Challenge**: Verified. `pipeline/gates.py:20-69` implements tiered validation where EXEMPT always passes, LIGHT checks existence, STANDARD adds frontmatter and min_lines, and STRICT adds semantic checks. The enforcement_tier field in `GateCriteria` (`pipeline/models.py:73`) is a `Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"]`. The blocking behavior is controlled by `GateMode` (BLOCKING vs TRAILING), which is separate from the tier.

However, the delta claims "three distinct STRICT/STANDARD axes that coexist" -- this is imprecise. There are only two axes in the codebase: (1) pipeline gate validation depth (enforcement_tier) and (2) tasklist task compliance tier. The spec's "profile" model does not yet exist, so it is not a "coexisting axis" -- it is a proposed future axis. Framing it as three existing collisions is misleading.

**Verdict**: OVERSTATED. The finding is correct that the naming collision exists between two implemented systems, but inflates it to three by counting a spec proposal that does not exist in code.

---

### Delta 2.6 -- Trailing gate framework exists but NOT wired into sprint

**Original claim**: `pipeline/trailing_gate.py` provides full infrastructure but sprint's `execute_sprint()` never calls it. `SprintGatePolicy` at `sprint/executor.py:47-90` is a stub. `tui.gate_states` is never populated.

**Challenge**: Mostly verified. `SprintGatePolicy` at executor.py:47-90 is NOT a stub -- it is a fully implemented class with working `build_remediation_step()` (lines 57-79) and `files_changed()` (lines 81-90) methods. It is a concrete implementation, not a stub. However, it is true that `execute_sprint()` (line 491) never instantiates or calls `SprintGatePolicy`.

The sprint executor imports `TrailingGatePolicy` and `TrailingGateResult` from `pipeline.trailing_gate` (line 36), but never imports `TrailingGateRunner` or `DeferredRemediationLog`. The TUI's `gate_states` dict (tui.py:72) is initialized empty and confirmed never populated by the executor.

The `_show_gate_column` flag at tui.py:73 is `getattr(config, "grace_period", 0) > 0`, and `grace_period` defaults to 0 in both `PipelineConfig` and `SprintConfig`, so the gate column is never shown by default.

**Verdict**: ACCURATE with correction: `SprintGatePolicy` is implemented, not a stub. It is unwired, but calling it a "stub" understates the work already done.

---

### Delta 2.7 -- GateDisplayState is a UI ornament, not a GateResult model

**Original claim**: `sprint/models.py:70-149` defines `GateDisplayState` with 7 symbolic states and display metadata. Has no gate_run_id, no score, no evidence, no timing. `TaskResult.gate_outcome` at `models.py:153-170` captures only PASS/FAIL/DEFERRED/PENDING.

**Challenge**: Verified. `GateDisplayState` (lines 70-150) has 7 enum values with color, icon, and label properties. It includes transition validation via `GATE_DISPLAY_TRANSITIONS` (lines 107-114) and `is_valid_gate_transition()` (lines 117-119). This is more than a "UI ornament" -- it has a formal state machine with valid transition constraints. But it is true that it lacks the 13+ fields the spec's GateResult requires.

`GateOutcome` (lines 57-68) is a 4-value enum (PASS/FAIL/DEFERRED/PENDING) used in `TaskResult.gate_outcome`. The delta's line reference `models.py:153-170` for `TaskResult` is slightly off -- `TaskResult` starts at line 153, but `gate_outcome` is at line 168. Minor.

The delta undervalues `GateDisplayState` by calling it an "ornament." It has formal transition rules and was clearly designed with gate lifecycle semantics in mind. The gap is real (no evidence, no timing, no run_id), but the characterization as "ornament" is dismissive of existing design work.

**Verdict**: OVERSTATED. The structural gap is real, but the characterization of GateDisplayState as mere "UI ornament" ignores its transition state machine, which is a meaningful design artifact that the new GateResult could extend rather than replace.

---

### Delta 2.8 -- Sprint has no audit workflow states

**Original claim**: `PhaseStatus` at `sprint/models.py:206-249` has 12 states but none are audit workflow states. Neither `PhaseStatus` nor `TaskStatus` contains any `audit_*` state.

**Challenge**: Verified. `PhaseStatus` has 12 values: PENDING, RUNNING, PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED, PREFLIGHT_PASS, INCOMPLETE, HALT, TIMEOUT, ERROR, SKIPPED. `TaskStatus` has 4: PASS, FAIL, INCOMPLETE, SKIPPED. No `audit_*` states exist in any enum in the sprint module. Grep for `audit_gate|audit_task|audit_milestone|audit_release` across all cli code returns zero matches.

This is an absence finding. The delta correctly identifies it but does not consider whether audit states SHOULD be in PhaseStatus/TaskStatus at all, or whether they belong in a completely separate concern. The spec's 12 audit states are a parallel lifecycle, not execution outcome states. The delta does note this ("live in a parallel audit workflow layer"), which is a reasonable recommendation.

**Verdict**: ACCURATE.

---

### Delta 2.9 -- No lease/heartbeat mechanism for audit_*_running

**Original claim**: Sprint has a heartbeat-like monitor at `sprint/monitor.py:255-260` and `sprint/models.py:452-463` with 120s stall detection, but no lease token, no lease owner, no audit_*_failed(timeout).

**Challenge**: Verified with line-number correction. The output event liveness tracking is at `monitor.py:255-260` (confirmed: lines 255-260 update `last_event_time` and `events_received`). The `stall_status` property is at `models.py:449-463` (not 452-463 as claimed; the property definition starts at line 449 with the decorator, line 450 with `def stall_status`). The 120s threshold is hardcoded at lines 454 and 459.

The delta correctly notes the stall monitor operates on subprocess output, not on audit evaluation. This is an accurate assessment.

**Verdict**: ACCURATE (minor line offset: 449 not 452).

---

### Delta 2.10 -- TUI completion guard does not exist

**Original claim**: The TUI has no audit-aware completion guard. Blocking is done by `executor.py:764-810`. The TUI renders SUCCESS/HALTED but never checks audit states.

**Challenge**: Verified. The TUI's `_build_terminal_panel()` at tui.py:254-273 renders "Sprint Complete" or "Sprint Halted" based solely on `SprintOutcome.value`. There is no audit state check. The executor at lines 764-787 halts on `status.is_failure` but has no audit gate check.

However, the delta's characterization of `executor.py:764-810` as the blocking mechanism is slightly imprecise. The halt decision is at line 765 (`if status.is_failure:`) through line 787 (`break`). Lines 788-810 do not exist in the executor as halt logic -- line 789 starts `finally: shutil.rmtree(isolation_dir)`, and lines 792+ are the post-loop merge of preflight results.

**Verdict**: ACCURATE (line range for "764-810" is imprecise; actual halt logic is 764-787).

---

### Delta 2.11 -- Tasklist generates no audit metadata

**Original claim**: Tasklist phase files emit rich task metadata but zero audit-awareness fields. No `audit_gate_required`, no `audit_scope`, no `gate_override_allowed`.

**Challenge**: I cannot directly verify the tasklist generator skill file (`sc-tasklist-protocol/SKILL.md:622-637`) as it is a markdown skill definition, not Python code. The tasklist Python module at `src/superclaude/cli/tasklist/` exists but its models do not contain audit fields. Grep confirms no `audit_gate` references anywhere in the cli codebase.

However, the conclusion that the sprint runner "has no declarative signal from the bundle about which tasks require audit gates" assumes that audit gating should be declared at tasklist generation time. An alternative design would be to derive audit requirements at sprint runtime based on task metadata (tier, risk) that already exists. The delta assumes a specific architectural approach (push audit metadata at generation time) without considering the alternative (pull at runtime). Both are valid; neither is objectively correct.

**Verdict**: OVERSTATED. The absence is real, but presenting it as the only valid approach ignores a legitimate runtime-derivation alternative that avoids coupling the tasklist generator to the audit gate system.

---

### NR-1 -- Tasklist bundle must emit audit_gate_required per task

**Original claim**: The sprint runner needs a declarative signal from the tasklist bundle about which tasks require audit gating. Without this, the runner must infer it at runtime, "which breaks determinism."

**Challenge**: The claim that runtime inference "breaks determinism" is unsupported. If the derivation rule is deterministic (and the proposed rule `Tier==STRICT or Risk==High or Critical Path Override==Yes` is), then computing it at runtime from the same inputs produces the same output as pre-computing it at generation time. Determinism is a property of the function, not when it executes. The real argument for pre-computation is decoupling and auditability (you can inspect the tasklist to see which tasks will be gated), not determinism.

**Verdict**: OVERSTATED. The requirement may be legitimate for auditability/transparency, but the determinism argument is wrong.

---

### NR-2 -- Tasklist schema versioning required

**Original claim**: As audit metadata fields are added to phase files, schema versioning becomes mandatory to prevent the sprint runner from silently accepting old bundles lacking `audit_gate_required`.

**Challenge**: This is a reasonable forward-looking requirement but is not an urgent need. The sprint runner can check for the presence of `audit_gate_required` and default to a safe value (e.g., `true` -- gate everything) when the field is absent. This is the standard approach for backward-compatible schema evolution and does not require a version number. Schema versioning is a nice-to-have, not mandatory.

**Verdict**: OVERSTATED. Backward-compatible defaults are simpler and sufficient for this use case.

---

### NR-3 -- deviation-analysis step must complete before audit gate design finalized

**Original claim**: Until DEVIATION_ANALYSIS_GATE is wired and validated, the roadmap pipeline does not produce `deviation-analysis.md`, which an audit gate might need to inspect.

**Challenge**: The claim that the audit gate design "cannot be finalized" until deviation-analysis is wired makes an unsubstantiated dependency claim. The audit gate operates on sprint execution (task/milestone/release scope), not on roadmap pipeline artifacts. The deviation-analysis gate is a roadmap pipeline gate that validates roadmap generation quality. These are different systems operating at different lifecycle stages. An audit gate could be fully designed without any dependency on the deviation-analysis artifact unless the spec explicitly requires the audit gate to inspect roadmap artifacts -- and the delta does not cite any such spec requirement.

**Verdict**: OVERSTATED. The delta conflates two independent systems. Wiring DEVIATION_ANALYSIS_GATE is a roadmap pipeline completeness issue, not an audit gate prerequisite.

---

### NR-4 -- reimbursement_rate fate must be a spec-level decision

**Original claim**: The field's fate must be decided before Phase 2 because different implementers may inadvertently activate or remove it.

**Challenge**: This is a single-field decision on a single dataclass. It does not warrant a spec-level decision or Phase 2 gate. A code comment (`# TODO: decide whether to wire into audit retry budget or remove`) would suffice. Elevating a dead field to a blocking decision is scope inflation.

**Verdict**: OVERSTATED. This is a code-level housekeeping item, not a spec-level blocking decision.

---

### NR-5 -- Stale audit gate results need freshness invalidation

**Original claim**: If a phase file is edited after an audit gate passes, the gate result must be invalidated.

**Challenge**: This is a legitimate correctness requirement. The existing freshness pattern at `executor.py:588-675` validates this approach. However, the urgency classification ("required for correctness at Phase 1") is questionable. Phase 1 is about defining contracts and data models, not runtime behavior. Freshness invalidation is a Phase 2 (runtime controls) concern.

**Verdict**: ACCURATE in substance, OVERSTATED in phase assignment.

---

### NR-6 -- spec_hash-style audit result binding

**Original claim**: Audit gate results must be bound to specific artifact versions via SHA-256 hashing.

**Challenge**: This is a restatement of NR-5 with a specific implementation recommendation (SHA-256 binding). It is not a separate requirement -- it is the implementation mechanism for NR-5. Counting it as a separate new requirement inflates the finding count.

**Verdict**: OVERSTATED. This is an implementation detail of NR-5, not a separate requirement.

---

### NR-7 -- Sprint executor mainline must be extended, not just execute_phase_tasks()

**Original claim**: `TurnLedger` budgeting is wired into `execute_phase_tasks()` but NOT into the mainline `execute_sprint()` Claude-phase loop at `executor.py:574-579`. Audit hooks must live in the mainline.

**Challenge**: Verified. `execute_phase_tasks()` (line 350) accepts `ledger: TurnLedger | None` and uses it for per-task budget tracking. The mainline `execute_sprint()` (line 491) does not create or pass a TurnLedger -- it uses `execute_phase_tasks()` only in certain code paths, and the mainline phase loop (lines 565-787) launches `ClaudeProcess` directly without TurnLedger integration.

However, the claim that "audit hooks must live in the mainline" is an architectural assertion, not a finding. It is one valid approach. An alternative is to add audit hooks as post-phase callbacks, which could work at either level. The delta states this as a fact when it is a design recommendation.

**Verdict**: ACCURATE on the gap identification. The observation that TurnLedger is not in the mainline loop is correct. The architectural prescription is reasonable but presented as fact rather than recommendation.

---

## 2. Severity Classification

### Challenge to Summary Table Severity Ratings

| Item | Assigned | My Assessment | Rationale |
|---|---|---|---|
| Spec-patch auto-resume still present | HIGH -- P0 blocker | **MEDIUM** | Code is functional and bounded. Retirement is cleanup, not a safety concern. No user-facing impact until audit gates are built. |
| DEVIATION_ANALYSIS_GATE unwired | HIGH -- audit prerequisite | **MEDIUM** | The gate definition is complete. Wiring a step is a small code change. Not a prerequisite for audit gates (different system). |
| `audit_*` states absent | HIGH -- P1 core | **HIGH** | Agree. These are foundational data model additions without which nothing audit-related can proceed. |
| GateResult model absent | HIGH -- P1 core | **HIGH** | Agree. The 13-field GateResult is the contract for all downstream consumers. |
| No lease model | HIGH -- P2 core | **HIGH** | Agree. The lease model is the core novelty of the audit system. |
| SprintGatePolicy unwired | HIGH -- P2 core | **MEDIUM** | The policy class is already implemented (not a stub). Wiring it requires adding ~20 lines to execute_sprint(). The delta overstates this as a HIGH risk. |
| TUI completion guard absent | MEDIUM -- P3 | **MEDIUM** | Agree. Display-only concern. |
| Trailing gate not wired into sprint | MEDIUM -- P2 | **MEDIUM** | Agree. Infrastructure exists; wiring is integration work. |
| Tasklist emits no audit metadata | MEDIUM -- P3 | **LOW** | Runtime derivation is a viable alternative. This is a design choice, not a gap. |
| reimbursement_rate dead field | LOW -- P1 | **LOW** | Agree. Housekeeping item. |
| STRICT/STANDARD axis collision | MEDIUM -- P1 | **LOW** | Two existing axes use the same names. A note in the spec is sufficient; no code change needed. |
| deviation-analysis as audit prerequisite | HIGH -- P0 | **LOW** | False dependency. These are separate systems. |
| Freshness invalidation | MEDIUM -- P1 | **MEDIUM** | Legitimate requirement but P2, not P1. |
| spec_hash-style binding | MEDIUM -- P1 | **LOW** | Duplicate of freshness invalidation (NR-5). |
| Sprint mainline vs helper path gap | HIGH -- P2 | **MEDIUM** | Real gap but straightforward integration. Not a novel risk. |

**Summary of severity challenges**: 4 items are rated too HIGH, 2 items are rated correctly HIGH, and 2 items should be rated lower than their current level.

---

## 3. Spec Update Language Evaluation

### 4.4 MAJOR_REWRITE Assessment

The replacement text for 4.4 is well-structured and references concrete code locations. Specific issues:

1. **Item 1**: References `OutputMonitor.last_event_time` at `sprint/monitor.py:255-260` -- this is accurate. The `AuditLease` model definition (fields: `lease_id`, `owner`, `acquired_at`, `expires_at`, `renewed_at`) is reasonable but introduces a new `owner` concept without defining what an owner is in a single-process sprint execution. Who is the lease owner when there is only one executor process? This introduces ambiguity about multi-process vs single-process audit evaluation.

2. **Item 3**: Suggested defaults `task=3, milestone=2, release=1` are asserted without justification. Why 3 for tasks? The existing remediation pattern uses `max_attempts=2`, so why not 2 for tasks as well? The numbers appear arbitrary.

3. **Item 6**: States "the turn budget is `max_turns * 60 s` (the remediation step formula, `sprint/executor.py:73-79`)" -- the line reference is correct (SprintGatePolicy.build_remediation_step at line 78 uses `self._config.max_turns * 60`), but applying the remediation timeout to audit gate evaluation is an assumption, not a fact. The remediation timeout was designed for remediation steps, not audit evaluation. These may have very different time profiles.

4. **Item 7**: Escalates a dead field to a spec-level decision with a "before Phase 2 GO" deadline. This is disproportionate for a single unused float field.

### 10.2 MAJOR_REWRITE Assessment

The replacement text provides a detailed four-phase plan with specific file:line targets. Issues:

1. **Phase 0**: Lists two prerequisites. The `_apply_resume_after_spec_patch()` removal is straightforward. But mandating `deviation-analysis` step wiring as a P0 prerequisite for audit gates is an unsupported dependency (see NR-3 challenge above).

2. **Phase 1**: The instruction to add `AuditWorkflowState` enum "alongside existing PhaseStatus/TaskStatus (NOT replacing them)" is clear and correct. However, adding a profile enum `strict | standard | legacy_migration` to `sprint/models.py` when the profile model is still an "open blocking decision" (D1.2, "STILL OPEN") creates a contradiction -- how can it be a P1 deliverable if the decision is still blocked?

3. **Phase 2**: References `executor.py:668-717` and `executor.py:736-787` as integration hook candidates. These line ranges are approximately correct. Lines 668-717 cover post-subprocess exit code reading through status determination. Lines 736-787 cover PhaseResult construction through halt decision. These are reasonable insertion points, though the exact lines will shift as other changes are made.

4. **Phase 3**: Places tasklist audit metadata at P3, which is late. If the sprint runner needs `audit_gate_required` to decide which tasks to gate, this must be available before the sprint executor can use audit gates (P2). There is a hidden dependency here.

---

## 4. Missing Coverage

The delta analysis has several blind spots:

1. **The `src/superclaude/cli/audit/` module is completely ignored**. There is an entire `audit` subpackage with 40+ Python files including `evidence_gate.py`, `manifest_gate.py`, `validation.py`, `budget.py`, `checkpoint.py`, `batch_retry.py`, and `escalation.py`. These files likely contain audit infrastructure that is directly relevant to the audit gating spec. The delta analysis surveyed `sprint/`, `roadmap/`, `pipeline/`, and `tasklist/` but missed this substantial existing audit infrastructure. This is a significant oversight that could change multiple findings -- existing gate, budget, and checkpoint mechanisms may already partially satisfy spec requirements.

2. **The `cleanup_audit/` module is also ignored**. `src/superclaude/cli/cleanup_audit/` contains `gates.py`, `models.py`, `executor.py`, `monitor.py`, `tui.py`, and `process.py` -- a complete pipeline with gate infrastructure that may demonstrate patterns applicable to audit gating.

3. **ShadowGateMetrics** (`sprint/models.py:571-618`) and `shadow_gates` config flag (`models.py:305`) are not discussed. The sprint already has a shadow gate mode concept that could be the Phase 1 rollout mechanism (shadow mode before enforcement). This is a missed integration opportunity.

4. **The `GateScope` enum** already exists in `pipeline/trailing_gate.py:579-584` with RELEASE, MILESTONE, and TASK values -- these directly correspond to the spec's three audit gate scopes. The delta mentions `resolve_gate_mode()` but does not highlight that `GateScope` itself is already defined and aligned with the spec.

5. **The `RemediationRetryStatus` and `attempt_remediation()` function** in `pipeline/trailing_gate.py:339-451` implement a complete retry-once state machine with budget integration. This is more directly relevant than the roadmap remediation pattern cited in section 3.4, because it operates on gate results rather than file groups.

6. **No analysis of the `pipeline/executor.py` trailing gate integration**. The pipeline executor at `pipeline/executor.py:82-84` already creates a `TrailingGateRunner` when `grace_period > 0`. This means the sprint executor could activate trailing gates simply by setting `grace_period > 0` in its config -- the infrastructure is already wired in the shared pipeline executor. The delta misses this existing integration path.

---

## 5. Implementation Feasibility

### Phase ordering issues

1. **P0 includes a false prerequisite**: Wiring DEVIATION_ANALYSIS_GATE into `_build_steps()` is a roadmap pipeline improvement that is independent of audit gate design. Making it a P0 prerequisite creates an artificial dependency that could delay audit gate work for no benefit.

2. **P1 includes an unresolved decision**: Adding the profile enum (`strict | standard | legacy_migration`) is listed as P1 work, but D1.2 ("Profile thresholds not finalized") is marked "STILL OPEN." You cannot implement what has not been decided. Either the profile decision must be made before P1 starts (making it a P0 governance item), or the profile enum must be deferred to a later phase.

3. **P2 has a hidden P3 dependency**: The sprint executor audit hooks (P2) need to know which tasks require audit gates. If `audit_gate_required` is not emitted until P3 (tasklist changes), then P2 cannot fully test its integration. The delta places tasklist changes at P3 but sprint integration at P2, creating a chicken-and-egg problem.

4. **P2 scope is too large**: Phase 2 includes completing SprintGatePolicy wiring, extending OutputMonitor for audit lease heartbeats, AND integrating TrailingGateRunner. These are three independent streams of work, each with its own testing requirements. Bundling them as P2 risks schedule overrun.

### Realistic assessment

The four-phase plan is structurally sound but has 2-3 dependency errors that would surface during implementation. A revised ordering would be:

- **P0**: Retire spec-patch cycle (code cleanup only, no design decisions needed)
- **P1**: Profile decision (governance), data model additions (AuditWorkflowState, GateResult, AuditLease)
- **P2a**: Tasklist audit metadata emission (prerequisite for P2b)
- **P2b**: Sprint executor integration (SprintGatePolicy wiring, OutputMonitor extension)
- **P3**: TUI display, release guards, shadow-to-enforcement rollout

---

## Summary

### Finding verdicts

| Rating | Count | Items |
|---|---|---|
| OVERSTATED | 8 | Delta 2.1, 2.4, 2.5, 2.7, NR-1, NR-2, NR-3, NR-4, NR-6 |
| ACCURATE | 7 | Delta 2.2, 2.3, 2.8, 2.9, 2.10, NR-5, NR-7 |
| UNDERSTATED | 0 | |
| WRONG | 0 | |

Note: NR-6 is counted as OVERSTATED because it is a duplicate of NR-5, not a separate requirement. NR-3 is OVERSTATED because it asserts a false dependency between independent systems.

### Overall assessment

The delta analysis is methodologically sound -- its file:line citations are almost all verifiable and accurate (with minor offset errors of 1-3 lines). The factual observations about code state are generally correct. Where the analysis fails is in:

1. **Severity inflation**: 6 of 16 findings have inflated severity ratings, creating a false sense of urgency.
2. **False dependencies**: NR-3 and the P0 DEVIATION_ANALYSIS_GATE wiring create artificial prerequisites between independent systems (roadmap pipeline vs sprint audit gates).
3. **Missing coverage**: The entire `src/superclaude/cli/audit/` module (40+ files) was not surveyed, potentially invalidating several "absence" findings.
4. **Architectural bias**: The analysis assumes push-model audit metadata (generate at tasklist time) without evaluating pull-model alternatives (derive at runtime), then uses this assumption to create new requirements.
5. **Duplicate findings**: NR-5 and NR-6 are the same requirement stated twice with different labels.

The analysis would be significantly strengthened by: (a) surveying the existing `audit/` module, (b) removing the false NR-3 dependency, (c) right-sizing severity ratings, and (d) acknowledging alternative architectural approaches where they exist.
