# Variant 3: Spec Quality Engineer Review

**Reviewer persona**: Spec quality engineer — evaluating `delta-analysis-post-v2.26.md` purely as a specification input artifact.
**Source spec**: `unified-audit-gating-v1.2.1-release-spec.md`
**Delta document**: `delta-analysis-post-v2.26.md`
**Review date**: 2026-03-17

---

## 0. Executive Summary (Pre-Read)

The delta analysis document is well-structured and shows real investigative depth against the codebase. However, as a spec update input artifact it has three systemic problems:

1. **Replacement language is implementation-annotated, not spec-normative.** Both §4.4 and §10.2 replacement texts embed source-file line references (`sprint/monitor.py:255-260`, `executor.py:677-723`). A spec is not a code map. When those line numbers shift, the spec becomes stale immediately.
2. **NR-1 through NR-7 are presented as "new requirements" but several are already implied by the existing spec's existing normative language.** Redundancies inflate the change surface and risk contradicting settled decisions.
3. **The §10.2 replacement text blurs spec-level contracts with implementation-level construction orders.** Phase sequencing in a spec should express dependency constraints, not task assignments to specific source files at specific line ranges.

The following sections evaluate each focus area in detail.

---

## 1. Finding Accuracy — Spec Gap Claims vs. Existing Spec Language

This section asks: does each delta finding describe a genuine spec gap, or does the spec already cover it through existing normative language?

### 1.1 Delta 2.5 (STRICT/STANDARD axis collision) — Partially misread

**Delta claim**: §3.1 must clarify that three distinct STRICT/STANDARD axes coexist (pipeline gate validation depth, tasklist compliance tier, audit gating profile enforcement level) and that the spec's profile model must use distinct naming.

**Spec reality**: §3.1 of the existing spec already gives canonical terms:

> Profile: `strict | standard | legacy_migration`

And §3.2 normatively resolves the `--strictness` vs `--profile` contradiction. The spec does *not* use the term "STRICT/STANDARD" for the profile axis — it uses lowercase `strict | standard`. The delta finding conflates the spec's term with the pipeline implementation's uppercase enum. This is a real implementation risk but it is not a spec gap in §3.1; it is a gap in §3.1 not having an explicit "these terms must not collide with other system nomenclature" advisory. The finding is accurate in spirit but overstates the spec's omission.

**Severity adjustment**: The delta rates this MEDIUM. From a spec-update perspective it is LOW — the spec's naming is already distinct (lowercase `strict | standard | legacy_migration` vs implementation uppercase). The needed update is an advisory annotation, not a normative change.

### 1.2 Delta 2.7 (GateResult model absent) — Accurate

**Delta claim**: §6.1 specifies a full `GateResult` with 13+ fields; `GateDisplayState` in the codebase is not that.

**Spec reality**: §6.1 lists required fields as normative. The delta correctly identifies that no implementation satisfies this spec yet. This is a genuine implementation gap, not a spec gap. From a spec-update perspective, the only change needed in §6.1 is a clarifying note distinguishing the contract (normative) from the rendering model (implementation detail). The delta's recommended spec change is accurate.

### 1.3 Delta 2.8 (audit workflow states absent from sprint) — Accurate but scope-incomplete

**Delta claim**: §4.1 requires 12 audit states; none exist in PhaseStatus.

**Spec reality**: §4.1 defines these states clearly. This is an implementation gap. However, the delta recommends: "§10.2 item 1 must spell out that the `audit_*` states... are **new states to be added**, not renamings." This is unnecessary spec elaboration — the spec already says what must exist. The implementation mapping in §10.2 is the right place for the clarification, but the spec text itself does not need to say "not renamings." That is implementation guidance, not a normative spec requirement.

### 1.4 Delta 2.1 (spec-patch auto-resume still present) — Finding is accurate; spec update recommendation is unnecessary

**Delta claim**: §10.2 should note that `executor.py:1193-1322` must be removed, as a Phase 0 prerequisite.

**Spec reality**: The existing spec's §10.1 Phase 0 is: "design/policy lock and owner/date assignments." Adding a code-removal task to Phase 0 changes Phase 0's definition. More importantly, the approved-immediate amendment (cited by the delta as already documenting the retirement) is the correct place for this — not the release spec. A release spec should say what must be true after the phase, not which lines to delete. The recommendation as written would embed a mutable implementation detail into a normative artifact.

### 1.5 Delta 2.3 (max_turns formula) — Finding is accurate; update target is correct

The delta correctly notes that §4.4 and §12.3 treated timeout values as TBD, and that post-v2.26 code provides concrete formulas. This is a genuine spec update opportunity. The update recommendation (reference the formula as the existing baseline) is appropriate.

### 1.6 Summary of Finding Accuracy

| Delta | Gap Type | Spec Already Covers? | Delta Accuracy |
|---|---|---|---|
| D2.1 (spec-patch auto-resume) | Implementation residue | Not a spec gap | Accurate finding, wrong fix |
| D2.2 (DEVIATION_ANALYSIS_GATE unwired) | Implementation gap | Not a spec gap | Accurate |
| D2.3 (max_turns formula) | TBD now answerable | Partial spec gap | Accurate |
| D2.4 (reimbursement_rate dead field) | Dead code | Not a spec gap | Accurate finding, scope debate |
| D2.5 (STRICT/STANDARD axis) | Naming collision risk | Spec already uses distinct names | Overstated |
| D2.6 (trailing gate unwired) | Implementation gap | Not a spec gap | Accurate |
| D2.7 (GateResult absent) | Implementation gap | Spec is clear; impl missing | Accurate |
| D2.8 (audit states absent) | Implementation gap | Spec is clear; impl missing | Accurate |
| D2.9 (no lease model) | Implementation gap | Spec is clear; impl missing | Accurate |
| D2.10 (TUI guard absent) | Implementation gap | Not a spec gap | Accurate |
| D2.11 (tasklist no audit metadata) | Missing spec requirement | Genuine spec gap | Accurate |

---

## 2. Severity Classification — Spec-Update Perspective

Several severity ratings are calibrated to implementation risk rather than spec-update priority. From a spec-update standpoint:

### 2.1 Reclassifications warranted

| Item | Delta Severity | Spec-Update Severity | Reason |
|---|---|---|---|
| Spec-patch auto-resume still present | HIGH — Phase 0 blocker | LOW | Not a spec language problem; it's a code removal task. The spec does not need new language. |
| STRICT/STANDARD axis collision | MEDIUM — spec clarity | LOW | Spec uses distinct lowercase terms already. Advisory annotation only needed. |
| TUI completion guard absent | MEDIUM — Phase 3 | LOW | The spec's §10.2 item 2 already targets `tui.py`. No new spec language needed; only the phase mapping needs precision. |
| Trailing gate not wired into sprint | MEDIUM — Phase 2 | LOW | Implementation gap. No spec text change required beyond adding a file to §10.2. |
| Tasklist schema versioning (NR-2) | LOW — correctness risk | MEDIUM | This *is* a genuine spec addition: NR-2 introduces a new schema contract not implied anywhere in the existing spec. |
| Sprint mainline vs helper path (NR-7) | HIGH — integration target | MEDIUM | Accurate but this is implementation guidance. A spec-level statement of "audit hooks must live in the mainline phase loop" suffices; line references do not belong in the spec. |

### 2.2 Items that are HIGH from spec perspective but are not called HIGH

**D1.2 (Profile thresholds still open)** is listed as "STILL OPEN" with no severity rating in the summary table. This is the most spec-critical blocker: §3.1, §3.2, §7, and §11 sections 2 and 5 all depend on the profile model. It should appear in the summary table as HIGH.

**D1.3 (Rollback triggers still open)** similarly has no summary-table entry despite being a §12.1 GO criterion. This is a spec gap that affects the GO/NO-GO contract directly.

---

## 3. Spec Update Language — Primary Evaluation

### 3.1 §4.4 Replacement Text — Detailed Critique

**Proposed §4.4 item 1:**

> `audit_*_running` uses lease + heartbeat. The heartbeat substrate is the existing `OutputMonitor.last_event_time` mechanism (`sprint/monitor.py:255-260`). A new `AuditLease` model must be introduced with fields: `lease_id`, `owner`, `acquired_at`, `expires_at`, `renewed_at`. The audit gate evaluator must emit periodic heartbeat events.

**Issues:**

- **Source-file line citations in normative spec text.** `sprint/monitor.py:255-260` is mutable. When the file is refactored, this citation becomes wrong silently. The spec should say "using the existing subprocess output monitoring mechanism" without pinning a line number.
- **"Must emit periodic heartbeat events"** is not actionable without a frequency specification. What is the heartbeat interval? At what cadence does the evaluator emit? Without this, two implementers will make different choices and both will claim spec compliance.
- **`AuditLease` is a new term introduced here with no definition in §3.1 Canonical Terms.** Any new model introduced in normative spec language must be defined in the terminology section first. This replacement text introduces `AuditLease` without a canonical definition.

**Suggested improved language for item 1:**

> `audit_*_running` uses a lease model with heartbeat renewal. The lease must have: a unique `lease_id`, an `owner` identifier, `acquired_at` (ISO-8601 UTC), `expires_at` (ISO-8601 UTC), and `renewed_at` (ISO-8601 UTC). The audit gate evaluator must emit a heartbeat renewal event at an interval no greater than `audit_lease_timeout / 3`. The lease mechanism builds on the subprocess stall-detection pattern already present in the runner infrastructure.

---

**Proposed §4.4 item 2:**

> Missing heartbeat past `audit_lease_timeout` causes `audit_*_failed(timeout)`. The timeout value must be decided by the Reliability Owner (see §9.2) and is separate from the subprocess stall timeout (currently 120 s). Recommended baseline: `min(step_timeout_seconds, 300)`.

**Issues:**

- **`audit_lease_timeout` is introduced but not defined.** This term appears nowhere in §3.1 or any other spec section. It needs either a canonical definition or a reference to where it will be defined.
- **"currently 120 s"** pins an implementation value into spec text. "Currently" becomes wrong as soon as the implementation changes. If this value is normative, say so and own it. If it is advisory, say "the existing subprocess stall timeout (see Reliability Owner — §9.2)."
- **`min(step_timeout_seconds, 300)`** is a formula referencing `step_timeout_seconds` which is not defined anywhere in the spec. An implementer cannot evaluate this formula without knowing what `step_timeout_seconds` refers to in the audit gate context.
- **"Recommended baseline"** for a timeout in a normative spec section is a contradiction. Either it is normative (and should read "default value") or it is heuristic (and belongs in a non-normative advisory note).

**Suggested improved language for item 2:**

> Missing heartbeat renewal past `audit_lease_timeout` causes `audit_*_failed(timeout)`. `audit_lease_timeout` is a per-scope configurable value; default values must be approved by the Reliability Owner (§9.2) before Phase 2 GO. The `audit_lease_timeout` must be independent of and no greater than the outer subprocess wall-clock timeout for the same scope.

---

**Proposed §4.4 item 3:**

> Retry is bounded by per-scope attempt budget. The bounded model mirrors the roadmap remediation pattern (`roadmap/executor.py:677-723`): a JSON state block stores `audit_attempts` per entity; `max_attempts` is configured per scope (task/milestone/release) with suggested defaults: task=3, milestone=2, release=1.

**Issues:**

- **The "suggested defaults" (task=3, milestone=2, release=1) are not justified.** This is the most consequential gap in the replacement language. A reader cannot determine whether task=3 is safe, conservative, or generous relative to any KPI. No rationale is provided. The spec's §8 KPI framework and §7 rollout contract exist precisely to govern these values. The defaults should be marked as provisional (shadow mode only) and subject to calibration per §8.2, or they should be explicitly justified against a specific KPI threshold.
- **Another line citation** (`roadmap/executor.py:677-723`) embedded in normative language.
- **"a JSON state block"** is an implementation detail. The spec should say what must be tracked (attempt count per scope per entity, bounded by `max_attempts`) without prescribing the storage format.

**Suggested improved language for item 3:**

> Retry is bounded by a per-scope attempt budget. The attempt count for each audited entity (`audit_attempts`) must be persisted in durable state and incremented on each retry. `max_attempts` is configured per scope: task, milestone, and release. Default values for `max_attempts` per scope are provisional during shadow mode and become normative only after calibration per §8.2. Provisional defaults: task=3, milestone=2, release=1. These values must be reviewed and approved by the Reliability Owner (§9.2) before Phase 2 GO.

---

**Proposed §4.4 item 6:**

> The subprocess turn budget (`max_turns * 120 + 300 s`) is the outer wall-clock ceiling for any sprint phase execution. Audit gate evaluation must complete within this ceiling. For audit gate sub-processes specifically, the turn budget is `max_turns * 60 s` (the remediation step formula, `sprint/executor.py:73-79`), which at the default of 100 gives 6,000 s (1h 40m).

**Issues:**

- **Three line citations in one item.** None should be in spec text.
- **`max_turns` is introduced but not defined in the spec.** A reader who has not read the codebase does not know what a "turn" is. This is a critical undefined term.
- **The formula is presented as fact but the spec does not own `max_turns`.** If `max_turns` changes (e.g., default raised from 100 to 200), the spec's arithmetic becomes wrong. The spec should reference the formula pattern, not hard-code the arithmetic result.
- **The selection of the remediation formula (`max_turns * 60`) for audit gates is not justified.** Why should audit gates use the remediation formula rather than the main subprocess formula? The choice is consequential and unexplained.

**Suggested improved language for item 6:**

> The outer wall-clock ceiling for any sprint phase execution is derived from the configured `max_turns` value. Audit gate evaluation must complete within this ceiling. The Reliability Owner (§9.2) must specify the audit gate sub-process time budget as a fraction of the outer ceiling before Phase 2 GO. This value must be documented as a locked decision per §9.3.

---

**Proposed §4.4 item 7 (reimbursement_rate):**

> `reimbursement_rate = 0.8` exists in `TurnLedger` (`sprint/models.py:482-487`) but is currently unused. The Reliability Owner must decide before Phase 2 GO: either wire this as a turn-recovery credit for audit retry paths, or remove it from the model to avoid confusion.

**Issues:**

- **This item is a governance directive embedded in normative spec language.** Items 1–6 of §4.4 are normative contracts. Item 7 is a decision request. It belongs in §12.4 (Required user decisions) or §12.3 (Current blocker list), not in the timeout/retry/recovery semantics section.
- **The line citation** again pins the spec to a specific model location.

**Recommended placement**: Move to §12.3 as a new blocker item or to §12.4 as a new required decision, not §4.4.

---

### 3.2 §10.2 Replacement Text — Detailed Critique

**Overall structural problem**: The current spec's §10.2 is a file-level change map. The proposed replacement adds phase headers (Phase 0, Phase 1, Phase 2, Phase 3, Phase 4) and embeds specific executor line ranges, making it a hybrid of spec contract and implementation task list. This conflation will cause the following problems:

- When implementers refactor the code, the spec becomes factually wrong.
- The Phase labels create ambiguity: §10.1 already defines Phase 0–4 at a higher level. §10.2 should be subordinate to §10.1, but the proposed replacement elevates §10.2 to have its own phase structure that may drift from §10.1.
- §10.3 (acceptance criteria per phase) references phases defined in §10.1. If §10.2 redefines phases with different content, §10.3 becomes inconsistent.

**Phase 0 prerequisites:**

> - `src/superclaude/cli/roadmap/executor.py:1193-1322` — remove `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()`

A spec should not specify what lines to remove from a source file. Phase 0's acceptance criterion in §10.3 is: "all blocking decisions closed with owner/date." The code removal is an implementation action, not a spec requirement. The correct spec-level statement is: "The spec-patch auto-resume cycle must be retired before Phase 1 start. The deviation-analysis gate must be operational in the roadmap pipeline before Phase 1 start."

**Phase 1:**

> - `src/superclaude/cli/sprint/models.py:482-487` — resolve `reimbursement_rate` fate

This is a code-modification directive, not a spec requirement. The spec-level requirement is: "The turn recovery credit model must be defined (retained with documented semantics, or removed) before Phase 2 GO." File paths and line numbers should not appear in a normative spec.

**Phase 2:**

> - `src/superclaude/cli/sprint/executor.py:47-90` — complete `SprintGatePolicy` and wire into `execute_sprint()`; integration hook candidates: `executor.py:668-717` (post-subprocess, pre-classification) and `executor.py:736-787` (post-classification, pre-halt decision)

The "integration hook candidates" note is pure implementation guidance. This is developer handoff content, not spec content. The spec should say: "The sprint execution lifecycle must include audit gate evaluation hooks at task completion and phase completion boundaries." Where those hooks live in the source is the implementer's concern.

**Phase 3 (Tasklist derivation rule):**

> `audit_gate_required = true` when any of: `Tier == STRICT`, `Risk == High`, `Critical Path Override == Yes`

This is the strongest normative addition in §10.2, and it is correctly placed. However:

- `Critical Path Override == Yes` — what is `Critical Path Override`? This field is not defined in §3.1 Canonical Terms and does not appear in the existing spec. An implementer cannot apply this rule without knowing its definition and possible values.
- The derivation rule should appear in its own spec section (perhaps §4.5 or a new §3.3) rather than buried in a file-level change map.

**Phase 4 (test files):**

The proposed Phase 4 maps to the existing test file entries 6–9 of the current §10.2, just relabeled. This is unchanged content and does not require a major rewrite designation. However, the existing §10.3 acceptance criterion for Phase 4 is "phase gates pass by KPI criteria and rollback drill success." The §10.2 replacement mentions only test files — it does not mention the rollback drill or KPI gate passage as Phase 4 deliverables. This creates an inconsistency between §10.2 and §10.3.

---

## 4. Redundancy Check — NRs Already Implied by Existing Spec

### NR-1 — Tasklist bundle must emit `audit_gate_required` per task

**Assessment: GENUINE NEW REQUIREMENT.** The existing spec §1.1 describes the three scopes (task, milestone, release) but does not specify how the sprint runner learns which tasks require auditing. NR-1 is a genuine addition.

**However**, the derivation rule proposed (Tier==STRICT or Risk==High or Critical Path Override==Yes) introduces `Critical Path Override` as an undefined term. This must be defined before the derivation rule can be implemented.

### NR-2 — Tasklist schema versioning required

**Assessment: GENUINE NEW REQUIREMENT.** Not implied by any existing spec section. The existing §6.4 versioning policy covers GateResult and data contracts, but does not cover tasklist bundle schema versioning. This is a real addition.

**Severity correction**: The delta rates this LOW. It should be MEDIUM. A sprint runner silently accepting a stale bundle missing `audit_gate_required` would produce incorrect gating behavior — this is a correctness risk that aligns with the §5.2 rule "Unknown/missing deterministic inputs => failed."

### NR-3 — `deviation-analysis` step as audit prerequisite

**Assessment: PARTIALLY REDUNDANT.** The existing spec §10.1 Phase 1 already requires the pipeline to be capable of generating the artifacts the audit gate evaluates. NR-3's requirement that the roadmap pipeline produce a validated `deviation-analysis.md` before audit gate Phase 1 is complete is implied by the spec's general requirement for deterministic inputs (§5.2, item 2). However, naming the specific artifact as a Phase 1 acceptance criterion in §10.3 is a genuinely useful addition. The requirement is implied; the acceptance criterion is new.

### NR-4 — `reimbursement_rate` fate must be a spec-level decision

**Assessment: GENUINE NEW REQUIREMENT** but it belongs in §12.3/§12.4, not §4.4. The existing spec has no awareness of `reimbursement_rate`. Adding it to the blocker list is correct. The delta's placement recommendation (§4.4 item 7) is wrong.

### NR-5 — Stale audit gate results need freshness invalidation semantics

**Assessment: PARTIALLY REDUNDANT.** The existing spec §5.2 item 4 states: "Completion/release transitions require *latest* gate `passed`..." The word "latest" implies that a stale gate result should not satisfy the completion condition. The requirement is implied by "latest." What is *not* specified is the mechanism for invalidation. NR-5's addition is therefore partially redundant as a requirement but genuinely new as an implementation contract. The spec should clarify what "latest" means operationally (i.e., the gate result must be bound to the artifact version it evaluated).

### NR-6 — `spec_hash`-style artifact binding

**Assessment: PARTIALLY REDUNDANT.** NR-6 is the mechanism that implements what "latest" means in §5.2 item 4. It is not redundant as a mechanism but is redundant as a requirement — if the spec already says "latest gate passed," the implementer must find a way to determine latency. The delta's addition to `GateResult.artifacts` block (§6.1) is the right normative location for this.

### NR-7 — Sprint executor mainline must be extended

**Assessment: NOT A SPEC REQUIREMENT — it is an implementation guidance note.** NR-7 tells the implementer *where* in the code to put the audit hooks. A spec requirement would be: "Audit gate evaluation must be invoked as part of the primary phase execution lifecycle, not only within task-level helper functions." The "mainline vs helper" distinction is implementation detail that does not belong in spec text.

### Redundancy Summary

| NR | Redundancy Status | Correct Location |
|---|---|---|
| NR-1 | Genuine new requirement | §10.2 (derivation rule) + new §4.5 (audit signal contract) |
| NR-2 | Genuine new requirement | §6.4 (versioning policy extension) |
| NR-3 | Implied by §5.2 item 2; acceptance criterion is new | §10.3 Phase 1 acceptance criterion |
| NR-4 | Genuine new requirement | §12.3 new blocker or §12.4 new decision item |
| NR-5 | Implied by §5.2 item 4 ("latest"); mechanism is new | §5.2 clarification + §6.1 artifact binding |
| NR-6 | Mechanism for existing §5.2 "latest" requirement | §6.1 GateResult artifacts block |
| NR-7 | Not a spec requirement — implementation guidance | Developer handoff note, not spec text |

---

## 5. Implementation Feasibility — Can an Implementer Produce a Deterministic Implementation?

Evaluating whether the proposed §10.2 and §4.4 texts, taken together, allow an implementer to make all decisions without ambiguity:

### 5.1 Decision points left ambiguous after proposed replacement

| Decision Point | Location of Ambiguity | Status |
|---|---|---|
| Heartbeat emission interval | §4.4 item 1 | UNDEFINED — "periodic" is not actionable |
| `audit_lease_timeout` value | §4.4 item 2 | UNDEFINED — deferred to Reliability Owner with no constraints other than "separate from 120s" |
| `step_timeout_seconds` definition | §4.4 item 2 formula | UNDEFINED — term does not exist in spec |
| Justification for task=3, milestone=2, release=1 | §4.4 item 3 | UNJUSTIFIED — arbitrary without calibration rationale |
| Which formula governs audit gate subprocess timeout | §4.4 item 6 | AMBIGUOUS — remediation formula chosen but not justified |
| `max_turns` definition | §4.4 item 6 | UNDEFINED in spec |
| `Critical Path Override` field definition | §10.2 Phase 3 derivation rule | UNDEFINED in spec |
| How `audit_gate_required` field is read by the sprint runner | §10.2 Phase 3 | NOT SPECIFIED — derivation rules produce the field but runner behavior is not specified |
| What "latest gate passed" means operationally | §5.2 item 4 (unchanged) | AMBIGUOUS — NR-5 and NR-6 partially address this but are not integrated into §5.2 |
| `AuditLease` canonical definition | §4.4 item 1 | UNDEFINED in §3.1 Canonical Terms |

### 5.2 Circular dependency analysis in §10.2 Phase ordering

The proposed phase structure creates the following dependency chain:

- Phase 1 requires adding `AuditWorkflowState` enum to `sprint/models.py`
- Phase 2 requires wiring `SprintGatePolicy` into `execute_sprint()`
- Phase 3 requires `tui.py` to display `AuditWorkflowState` values

This is a clean dependency chain. No circular dependencies are introduced by the Phase 0 through Phase 4 sequence.

**However**, Phase 0 prerequisite 2 (wire `DEVIATION_ANALYSIS_GATE` into `_build_steps()`) depends on Phase 0 prerequisite 1 (retire `_apply_resume_after_spec_patch()`). The document does not note this ordering constraint within Phase 0. If the auto-resume cycle removal is incompletely done, adding the deviation-analysis step may reactivate old recovery paths. This is a Phase 0 internal ordering risk.

### 5.3 Feasibility verdict

An implementer taking the proposed §4.4 and §10.2 replacement texts as written cannot produce a deterministic implementation without making at least 10 independent design decisions that the spec should have locked. The texts are actionable as *implementation guidelines* but fall short of the spec's own standard (§0.1): "Deterministic items are requirements, invariants, contracts, and state/decision rules that are directly specified in source artifacts and are testable/replayable."

The proposed replacements meet the testability criterion only for the state machine additions (Phase 1) and the `audit_gate_required` derivation rule. They do not meet it for lease semantics, timeout values, attempt budgets, or heartbeat frequency.

---

## 6. Missing Coverage — Spec Sections That Should Be Updated But Are Not Mentioned

The delta's Section 4 table covers most spec sections but misses the following:

### 6.1 §8.3 KPI warning/fail bands — Not mentioned

If `audit_gate_required` is added as a new field and `AuditLease` is a new model, both will generate new events that feed into M-series KPIs. The KPI framework (§8) is not mentioned in the delta's update table at all. Specifically:

- The new audit lease heartbeat events affect M7 (stale-running incident metric).
- The per-scope attempt budget affects M1 (runtime) and M4 (determinism).
- The `audit_gate_required` field affects M9 (override governance).

These measurement impacts should be called out in the spec update table.

### 6.2 §7.2 Promotion criteria — Not mentioned

§7.2 requires passing M1, M4, M5, M7, M9 for Shadow-to-Soft promotion. Adding the audit gate state machine (Phase 1) means M7 will now include audit lease staleness incidents. This changes the operational meaning of M7's measurement without a spec update. The delta should note §7.2 as MINOR_UPDATE.

### 6.3 §3.1 Canonical Terms — Marked MINOR_UPDATE but scope is understated

The delta recommends adding a clarification about the three STRICT/STANDARD axes. But the replacement text introduces several entirely new canonical terms (`AuditLease`, `audit_lease_timeout`, `audit_gate_required`, `audit_attempts`, `max_attempts`) that must appear in §3.1. The MINOR_UPDATE label understates the required change.

### 6.4 §5.2 Pass/fail rules — Marked UNCHANGED but NR-5 and NR-6 require an update

If audit gate results must be bound to artifact versions (NR-5, NR-6), then §5.2 item 4 must be updated to say: "Completion/release transitions require the *current* gate result to reference the artifact version under evaluation." The term "latest" is ambiguous without this clarification.

### 6.5 §10.3 Acceptance criteria — Marked UNCHANGED but Phase 1 criterion is now insufficient

The current §10.3 Phase 1 criterion is: "deterministic replay stability for same input; fail-safe unknown handling." NR-3 adds a new Phase 1 criterion: "roadmap pipeline produces validated `deviation-analysis.md` artifact." Without this addition, Phase 1 GO is still achievable even if the prerequisite pipeline artifact does not exist, which would make the audit gate Phase 2 runtime controls non-functional.

---

## 7. Missing Acceptance Criteria

The following items proposed by the delta lack testable acceptance criteria:

| Item | Proposed Change | Missing Criterion |
|---|---|---|
| `AuditLease` model (§4.4 item 1) | Introduce new model with 5 fields | No criterion for: what constitutes a valid lease? What is the lease validation protocol? |
| Heartbeat emission (§4.4 item 1) | Evaluator must emit periodic heartbeat | No criterion for: at what frequency? What constitutes a valid heartbeat event? |
| `audit_lease_timeout` (§4.4 item 2) | Deferred to Reliability Owner | No criterion for: what is the deadline for this decision? |
| task=3, milestone=2, release=1 defaults (§4.4 item 3) | Suggested defaults | No criterion for: at what shadow-mode measurement threshold do these become normative? |
| `audit_gate_required` derivation (§10.2 Phase 3) | Add derivation rule to SKILL.md | No criterion for: what test verifies the derivation rule produces correct output? |
| Tasklist schema versioning (NR-2) | Require `schema_version` in frontmatter | No criterion for: what is the rejection behavior when version is incompatible? What error class? |
| `reimbursement_rate` fate (NR-4) | Must be resolved before Phase 2 GO | No criterion for: what does "resolved" mean as a deliverable? Owner? Spec update? Code removal? |
| Stale audit result invalidation (NR-5) | Freshness invalidation semantics required | No criterion for: what event triggers invalidation? What is the grace period? |
| `spec_hash`-style artifact binding (NR-6) | Bind gate result to artifact version | No criterion for: which hash algorithm? What fields are included in the hash input? |
| Phase 0 prerequisite: wire DEVIATION_ANALYSIS_GATE | Add step to `_build_steps()` | No criterion for: what output does the step produce? What does the gate check? When does it pass? |

---

## 8. Summary

### 8.1 Counts

| Category | Count |
|---|---|
| Total actionable items in delta | 16 (11 deltas + 5 NRs that are genuinely new) |
| Ambiguities found in proposed spec language | 10 |
| Redundancies found (NRs implied by existing spec) | 3 (NR-3 partially, NR-5 partially, NR-7 fully) |
| Items with missing acceptance criteria | 10 |
| Spec sections that should be updated but are not in the table | 4 (§5.2, §7.2, §8, §10.3) |
| Finding severity reclassifications warranted | 6 |

### 8.2 Critical issues requiring correction before spec update

In priority order:

1. **Remove all source-file line citations from normative spec language.** Spec text with line numbers becomes wrong on first refactor. Replace with behavioral descriptions.
2. **Define `AuditLease`, `audit_lease_timeout`, `max_turns`, `Critical Path Override`, `audit_gate_required`, `audit_attempts` in §3.1 Canonical Terms** before those terms appear in normative language.
3. **Justify or defer the task=3, milestone=2, release=1 defaults.** Either reference the calibration process (§8.2) that will determine them, or get explicit owner approval before encoding them as "suggested defaults" in spec text.
4. **Move §4.4 item 7 (reimbursement_rate decision)** to §12.3 or §12.4. It is not a timeout/retry/recovery semantic.
5. **Add `deviation-analysis.md` to §10.3 Phase 1 acceptance criterion** so Phase 1 GO cannot be declared without the prerequisite pipeline artifact.
6. **Update §5.2 item 4** to clarify what "latest" means with respect to artifact version binding (NR-5, NR-6 resolution).
7. **Specify heartbeat emission interval** in §4.4 item 1 replacement language, or explicitly defer it to the Reliability Owner with a deadline.
8. **Add §7.2 and §8 to the spec update table** — KPI measurement coverage and promotion criteria are affected by the new audit state machine and its events.

### 8.3 Items that are well-executed

- Section 3 (New Integration Opportunities) is high-quality implementation context that will genuinely accelerate Phase 2 design.
- The state machine analysis (Deltas 2.7, 2.8, 2.9) is accurate and well-scoped — it correctly identifies what exists, what is needed, and that the two concerns (rendering vs. contract) must remain separate.
- NR-1 (`audit_gate_required` derivation rule with `Tier` and `Risk` fields as inputs) is a clean, implementable addition that builds on existing tasklist infrastructure.
- NR-2 (schema versioning) correctly identifies a correctness risk that the spec did not anticipate.
- The D1.1 partial resolution assessment is honest and specific — it correctly separates what is now answerable from what remains TBD without conflating them.
