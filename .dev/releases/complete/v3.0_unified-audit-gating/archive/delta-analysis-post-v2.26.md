# v1.2.1 Spec Delta Analysis — Post-v2.26 Implementation Survey

**Produced by**: 3-agent parallel research + synthesis
**Date**: 2026-03-17
**Scope**: Compare `unified-audit-gating-v1.2.1-release-spec.md` against actual state of
`src/superclaude/cli/roadmap/`, `src/superclaude/cli/sprint/`, `src/superclaude/cli/tasklist/`,
`src/superclaude/cli/pipeline/`, and `.dev/releases/complete/v2.26-roadmap-v5/` amendment artifacts.

---

## 1. Resolved Blockers (M1 Items Now Answerable from Implemented Code)

The spec listed 4 blocking decisions in §12.3 as NO-GO conditions. Below is the status of each
against what v2.26 implementation provides.

### D1.1 — Retry/backoff/timeout values not finalized

**Status: PARTIALLY RESOLVED**

v2.26 implemented code now provides concrete numbers that answer these TBD values:

| Parameter | Source | Value |
|---|---|---|
| Claude subprocess timeout | `sprint/process.py:112-116`, `sprint/executor.py:476-480` | `max_turns * 120 + 300 s` |
| Sprint remediation step timeout | `sprint/executor.py:73-79` | `max_turns * 60 s` |
| Roadmap step timeouts (fixed) | `roadmap/executor.py:345-439` | Per-step: 300–900 s |
| Default max_turns | `pipeline/models.py:175`, `sprint/config.py` | 100 |
| Step retry_limit | `roadmap/executor.py:345-439` | 1 (= 2 total attempts) |
| Roadmap remediation max_attempts | `roadmap/executor.py:677-723` | 2 |
| Spec-patch auto-resume cycle bound | `roadmap/executor.py:1216-1223` | 1 (legacy, to be retired) |
| Stall/watchdog threshold | `sprint/models.py:452-463` | 120 s since last event |

**What remains TBD for spec compliance:**
- `audit_*_running` lease duration (no lease model exists yet; see D1.4 below)
- Per-scope audit attempt budget (spec §4.4: distinct from subprocess retries)
- Backoff function (exponential vs linear) for audit retry — not yet defined
- `reimbursement_rate = 0.8` (`sprint/models.py:482-487`) exists in TurnLedger model but is
  **unused in any formula** — the spec must either adopt, document, or discard it

**Verdict**: The subprocess-level numbers are now answerable from code. The audit-specific
lease/retry budget values remain TBD and are a spec update target.

---

### D1.2 — Profile thresholds and task-tier major-severity behavior not finalized

**Status: STILL OPEN**

No `profile` model (`strict | standard | legacy_migration`) exists anywhere in sprint, roadmap, or
tasklist code. The tasklist uses STRICT/STANDARD/LIGHT/EXEMPT for verification tiers, but this is
an orthogonal concept (task compliance, not audit gating profile).

**Evidence of absence**: No grep hits for `profile=strict`, `profile=standard`,
`legacy_migration`, or `--profile` flag in any sprint/roadmap/pipeline Python file.

**What this means for spec**: §3.1, §3.2, §7 (rollout phases), and §11 checklist sections 2 and 5
all depend on the profile model. These remain fully blocked on a user decision.

---

### D1.3 — Rollback/safe-disable triggers not finalized

**Status: STILL OPEN**

No rollback/safe-disable contract exists in any sprint or roadmap executor. The roadmap executor
has `--resume` (checkpoint-based restart), and rollback of remediation file groups
(`remediate_executor.py:257-327`), but neither is a deployment-rollout rollback mechanism.

v2.26 does add `REMEDIATION_ATTEMPTS_EXCEEDED` terminal halt as a bounded stopping condition
(`roadmap/executor.py:677-723`), which is structurally analogous but scoped to roadmap generation,
not audit gate enforcement.

---

### D1.4 — Open blocking decisions not yet assigned owner+deadline

**Status: STILL OPEN**

No owner/deadline assignments appear in any v2.26 artifact. The spec's §9.3 requires:
> "No GO decision without all three assigned [owner, UTC deadline, effective phase]."

This remains a governance gap independent of implementation state.

---

## 2. Implementation Deltas (Spec Says X, Reality Is Now Y)

### Delta 2.1 — Spec-patch auto-resume cycle: assumed retired, still present

| | Detail |
|---|---|
| **Spec assumption** | §1.2 and v2.26 approved-immediate explicitly retire the one-shot spec-patch auto-resume cycle |
| **Current reality** | `roadmap/executor.py:1193-1322` still implements `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()`, bounded to 1 cycle (`executor.py:1216-1223`) |
| **Spec update required** | §10.2 file-level change map should note that `executor.py:1193-1322` must be removed. No new spec language is needed — approved-immediate already documents the retirement — but the spec should reference that this is not yet complete and is a Phase 0 prerequisite. |

---

### Delta 2.2 — DEVIATION_ANALYSIS_GATE: defined but not wired into execution

| | Detail |
|---|---|
| **Spec assumption** | v2.26 approved-immediate treats DEVIATION_ANALYSIS_GATE as the new authoritative recovery gate replacing the spec-patch cycle |
| **Current reality** | `DEVIATION_ANALYSIS_GATE` is fully defined (`roadmap/gates.py:712-758`) with strong semantic checks, but `_build_steps()` (`roadmap/executor.py:343-440`) does not include a `deviation-analysis` step in the execution graph. The gate exists in `ALL_GATES` (`roadmap/gates.py:760-774`) but has no wiring. |
| **Spec update required** | §10.2 item 1 should explicitly call out that `_build_steps()` needs a new `deviation-analysis` step inserted after `spec-fidelity`. This is a Phase 1 prerequisite for the audit gate design. |

---

### Delta 2.3 — max_turns=100 changes timeout budget arithmetic

| | Detail |
|---|---|
| **Spec assumption** | §4.4 and §12.3 (D1.2) treated retry/backoff/timeout as TBD. The spec did not know the formula. |
| **Current reality** | Formula is `max_turns * 120 + 300` for subprocess timeout. At default 100: **12,300 s (3h 25m)** per roadmap step subprocess. Remediation step: `max_turns * 60 = 6,000 s (1h 40m)`. |
| **Spec update required** | §4.4 item 3 ("Retry is bounded by per-scope attempt budget") and §9 ("Reliability owner") should reference these formulas as the existing sprint/roadmap baseline. The audit gate lease timeout budget for `audit_*_running` should be specified as a fraction or multiple of these values. |

---

### Delta 2.4 — reimbursement_rate=0.8 is a dead model field

| | Detail |
|---|---|
| **Spec assumption** | The spec did not mention `reimbursement_rate` — it was never in scope. |
| **Current reality** | `sprint/models.py:482-487` defines `reimbursement_rate = 0.8` in `TurnLedger` but it is **unused in any formula** in executor, process, trailing-gate, or monitor code. |
| **Spec update required** | The spec should explicitly state in §4.4 or §10.2 that `reimbursement_rate` must either be (a) wired into turn budget recovery for audit retry/requeue semantics, or (b) documented as deprecated/removed. Leaving it as dead model state is an implementation correctness risk. |

---

### Delta 2.5 — STRICT/STANDARD gate tier semantics differ from spec's STRICT/STANDARD

| | Detail |
|---|---|
| **Spec assumption** | §3.1 defines STRICT vs STANDARD as enforcement level for audit gating (STRICT blocks, STANDARD warns). |
| **Current reality** | In the pipeline and roadmap (`pipeline/gates.py:20-69`), STRICT/STANDARD controls *validation depth* (STRICT adds semantic checks), not *blocking behavior*. Both tiers block execution equally in the current roadmap because `grace_period=0` by default. The tasklist uses STRICT/STANDARD/LIGHT/EXEMPT as *compliance tier* for task verification method, not gate enforcement level. |
| **Spec update required** | §3.1 must clarify that these are three distinct STRICT/STANDARD axes that coexist: (1) pipeline gate validation depth, (2) tasklist task compliance tier, (3) audit gating profile enforcement level. The spec's "profile" model must use distinct naming (e.g., `strict | standard | legacy_migration` as already specified) and must not collide with the existing pipeline tier nomenclature. |

---

### Delta 2.6 — Trailing gate framework exists in pipeline but is NOT wired into sprint

| | Detail |
|---|---|
| **Spec assumption** | §10.2 targets `sprint/models.py` and `sprint/tui.py` as primary integration points, implying sprint would consume trailing gate machinery. |
| **Current reality** | `pipeline/trailing_gate.py` provides `TrailingGateRunner`, `DeferredRemediationLog`, `attempt_remediation()`, and `resolve_gate_mode()` — all audit gate relevant. But sprint's `execute_sprint()` never calls any of them. `SprintGatePolicy` exists (`sprint/executor.py:47-90`) as a stub but is unwired. `tui.gate_states` exists but is never populated by executor. |
| **Spec update required** | §10.2 should list `pipeline/trailing_gate.py` integration as a Phase 2 prerequisite — specifically: `SprintGatePolicy` must be completed and wired into `execute_sprint()`, and `tui.gate_states` must be driven by executor gate outcomes. |

---

### Delta 2.7 — GateDisplayState is a UI ornament, not a GateResult model

| | Detail |
|---|---|
| **Spec assumption** | §6.1 specifies a rich `GateResult` with 13+ required fields including `gate_run_id`, `score`, `threshold`, `checks[]`, `drift_summary`, `override`, `timing`, `artifacts`, `failure_class`. |
| **Current reality** | `sprint/models.py:70-149` defines `GateDisplayState` with 7 symbolic states and display metadata (color, icon, label). It has no gate_run_id, no score, no evidence, no timing. `TaskResult.gate_outcome` (`models.py:153-170`) captures only `PASS/FAIL/DEFERRED/PENDING` enum. |
| **Spec update required** | §10.2 item 1 must add that `sprint/models.py` needs a new `GateResult` dataclass implementing §6.1 alongside the existing `GateDisplayState` (which can remain for TUI rendering). The two should be separate concerns. |

---

### Delta 2.8 — Sprint has no audit workflow states

| | Detail |
|---|---|
| **Spec assumption** | §4.1 requires explicit states: `ready_for_audit_task`, `audit_task_running`, `audit_task_passed`, `audit_task_failed`, plus milestone and release variants (12 states total). |
| **Current reality** | `PhaseStatus` (`sprint/models.py:206-249`) has 12 states but none are audit workflow states. All are execution outcome states (`PASS`, `HALT`, `TIMEOUT`, `ERROR`, etc.). `TaskStatus` has 4 states (`PASS/FAIL/INCOMPLETE/SKIPPED`). Neither enum contains any `audit_*` state. |
| **Spec update required** | §10.2 item 1 must spell out that the `audit_*` states from §4.1 are **new states to be added**, not renamings of existing `PhaseStatus` or `TaskStatus` values. They live in a parallel audit workflow layer, not replacing the execution outcome layer. |

---

### Delta 2.9 — No lease/heartbeat mechanism for audit_*_running

| | Detail |
|---|---|
| **Spec assumption** | §4.4 item 1: `audit_*_running` uses lease + heartbeat. Missing heartbeat past timeout causes `audit_*_failed(timeout)`. |
| **Current reality** | Sprint has a heartbeat-*like* output event monitor (`sprint/monitor.py:255-260`, `sprint/models.py:452-463`) that detects stalled subprocesses (120 s threshold). But there is no lease token, no lease owner, no lease expiry field, no `audit_*_failed(timeout)` transition, and no per-scope attempt budget bound to lease expiry. The stall monitor operates on the entire subprocess, not on the audit evaluation phase. |
| **Spec update required** | §4.4 must reference the existing stall monitor as the *implementation basis* for the heartbeat component, while noting that a distinct `lease` model (with `acquired_at`, `expires_at`, `renewed_at`, and owner) must be built for the audit state machine. §10.2 Phase 2 should list this as the primary new construction. |

---

### Delta 2.10 — TUI completion guard does not exist in current form

| | Detail |
|---|---|
| **Spec assumption** | §10.2 item 2: `sprint/tui.py` — "completion/release guards and operator guidance." |
| **Current reality** | The TUI has no audit-aware completion guard. Current blocking is done by `executor.py:764-810`: any failure `PhaseStatus` halts the sprint. The TUI renders `SprintOutcome.SUCCESS/HALTED` but never checks audit states, override records, or release guard conditions. The "completion guard" the spec assumes does not exist yet. |
| **Spec update required** | §10.2 item 2 should be scoped more precisely: the TUI needs (a) display of `audit_*` states in the phase table, (b) an operator guidance panel when `audit_*_failed` is displayed, and (c) a release guard that prevents showing "Sprint Complete" unless `audit_release_passed`. This is primarily a Phase 3 deliverable. |

---

### Delta 2.11 — Tasklist generates no audit metadata

| | Detail |
|---|---|
| **Spec assumption** | §1.1 requires gating at three scopes: task, milestone, release. Tasklist bundles are the primary input to sprint runs. |
| **Current reality** | Tasklist phase files emit rich task metadata (Tier, Risk, MCP Requirements, Sub-Agent Delegation, etc.) but **zero audit-awareness fields**. No `audit_gate_required`, no `audit_scope`, no `gate_override_allowed`. The tasklist generator (`sc-tasklist-protocol/SKILL.md:622-637`) has no audit derivation logic. |
| **Spec update required** | §10.2 should add entry: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — add `audit_gate_required: bool` derivation rules and emit field in generated phase files. Without this, the sprint runner has no declarative signal from the bundle about which tasks require audit gates. |

---

## 3. New Integration Opportunities

The following v2.26+ features are now available as leverage points for the audit gate implementation
that were not anticipated during v1.2.1 planning.

### 3.1 Existing gate infrastructure (GateCriteria, STRICT/STANDARD enforcement)

`pipeline/gates.py:20-69` provides `GateCriteria` with `mode`, `min_lines`, `required_fields`,
`semantic_checks`, and a two-tier validation dispatch. Any roadmap audit gate can be registered
in `ALL_GATES` (`roadmap/gates.py:760-774`) using this exact pattern — no new gate evaluation
infrastructure needed.

**Audit gate leverage**: define an `AUDIT_GATE` in `GateCriteria(mode=GateMode.STRICT, ...)` and
register it. The pipeline executor handles blocking semantics automatically.

---

### 3.2 Trailing gate pattern for task-scope gates

`pipeline/trailing_gate.py` provides a complete async non-blocking evaluation loop with:
- `TrailingGateRunner` (submit/wait async pattern)
- `DeferredRemediationLog` (collect and retry failures)
- `attempt_remediation()` (retry-once semantics with snapshot/rollback)
- `resolve_gate_mode()` — already says release-scope should always be BLOCKING

**Audit gate leverage**: task-scope gates (`audit_task_*`) are natural candidates for TRAILING
mode (non-blocking during task execution, evaluated before milestone transition). The infrastructure
is built; it only needs to be wired into `execute_sprint()` via `SprintGatePolicy`.

---

### 3.3 Tasklist compliance tier classification

The tasklist protocol already computes a deterministic tier (STRICT/STANDARD/LIGHT/EXEMPT) per task
using keyword scoring, compound-phrase overrides, and context boosters
(`sc-tasklist-protocol/SKILL.md:336-407`). The `Tier` field is already emitted in every generated
task.

**Audit gate leverage**: `audit_gate_required` derivation can consume the already-computed `Tier`
and `Risk` fields as primary signals (e.g., `Tier=STRICT or Risk=High` => `audit_gate_required=true`)
with no new classification logic beyond what already exists.

---

### 3.4 Remediation cycle bounded model

`roadmap/executor.py:677-723` implements a `max_attempts=2` remediation budget enforcer that reads
from `.roadmap-state.json` and terminates with a structured halt when exhausted.
`remediate_executor.py:50-75` implements per-file-group retry-once with snapshot/rollback.

**Audit gate leverage**: the audit gate's per-scope attempt budget (spec §4.4 item 3) can reuse
this pattern — store `audit_attempts` in state, enforce `max_attempts`, emit structured halt on
exhaustion. The bounded model is already proven.

---

### 3.5 Stall monitor as heartbeat basis

`sprint/monitor.py:255-260` already tracks `last_event_time` and `events_received`. The 120 s
stall detection already triggers `STALLED` status and can trigger watchdog kill
(`sprint/executor.py:620-653`).

**Audit gate leverage**: this is the heartbeat *substrate* for the lease model. The audit lease
heartbeat can be implemented as a specialized event type emitted by the audit gate evaluator,
monitored by the existing `OutputMonitor` with an audit-specific timeout threshold.

---

### 3.6 `spec_hash` invalidation pattern for audit freshness

`roadmap/executor.py:1495-1511` invalidates cached step outputs when `spec_hash` changes on
`--resume`. `_check_annotate_deviations_freshness()` (`executor.py:588-675`) detects stale
downstream artifacts by comparing stored hashes.

**Audit gate leverage**: audit gate results reference specific artifact versions. When upstream
artifacts (roadmap.md, phase files) change, the audit gate result should be invalidated. The
freshness-check pattern is ready to be applied to audit gate results.

---

### 3.7 State persistence in `.roadmap-state.json`

`roadmap/executor.py:786-847` (`_save_state()`) already persists structured sections: `validation`,
`fidelity_status`, `remediate`, `certify`. It is trivially extensible.

**Audit gate leverage**: add an `audit` block to the state JSON following the same pattern.
No new persistence infrastructure needed.

---

## 4. Spec Sections Requiring Updates

| Section | Status | Notes |
|---|---|---|
| §0. Evidence Model | UNCHANGED | Methodology unchanged |
| §1.1 Scope | MINOR_UPDATE | Add: tasklist bundle (`sc-tasklist-protocol/SKILL.md`) to file-level change map |
| §1.2 Primary goals | UNCHANGED | Goals remain valid |
| §1.3 Out-of-scope | UNCHANGED | Constraints unchanged |
| §2.1 Locked decisions | UNCHANGED | All 5 decisions remain valid |
| §2.3 Contradictions table | MINOR_UPDATE | Row 3 (retry/backoff TBD): update with concrete formula from `process.py:112-116`; add new row for `reimbursement_rate` dead field |
| §3.1 Canonical terms | MINOR_UPDATE | Add clarification: spec's `strict/standard` profile != pipeline `STRICT/STANDARD` gate validation depth != tasklist `STRICT/STANDARD/LIGHT/EXEMPT` tier. Three distinct axes. |
| §3.2 Strictness vs profile | UNCHANGED | Resolution direction remains valid |
| §4.1 Legal transitions | UNCHANGED | State machine design remains valid |
| §4.2 Illegal transitions | UNCHANGED | Remains valid |
| §4.3 Override rules | UNCHANGED | Policy unchanged |
| §4.4 Timeout/retry/recovery | MAJOR_REWRITE | See replacement language below |
| §5.1 Failure classes | UNCHANGED | Taxonomy unchanged |
| §5.2 Pass/fail rules | UNCHANGED | Rules unchanged |
| §5.3 Evidence requirements | UNCHANGED | Requirements unchanged |
| §6.1 GateResult | MINOR_UPDATE | Note: existing `GateDisplayState` is rendering-only; `GateResult` is a new dataclass to be added |
| §6.2 OverrideRecord | UNCHANGED | Unchanged |
| §6.3 Transition event schema | UNCHANGED | Unchanged |
| §6.4 Versioning policy | UNCHANGED | Unchanged |
| §7. Rollout contract | UNCHANGED | Still valid pending profile decisions |
| §8. KPI/SLO framework | UNCHANGED | Still valid |
| §9.1 Override approval model | UNCHANGED | Unchanged |
| §9.2 Owner responsibilities | MINOR_UPDATE | Add: "Tasklist owner: `audit_gate_required` derivation rules" |
| §9.3 Decision deadlines | UNCHANGED | Still applies |
| §10.1 Phase plan | MINOR_UPDATE | Phase 0 now has prerequisite: retire `_apply_resume_after_spec_patch()` and wire `deviation-analysis` step |
| §10.2 File-level change map | MAJOR_REWRITE | See replacement language below |
| §10.3 Acceptance criteria | UNCHANGED | Criteria remain valid |
| §11. Checklist closure matrix | MINOR_UPDATE | Update D1.1 (partially resolved); D1.2–D1.4 remain NO-GO |
| §12.1–12.3 GO/NO-GO | MINOR_UPDATE | D1.1 reduced from fully-blocked; add `reimbursement_rate` resolution to blocker list |
| §12.4 Required user decisions | UNCHANGED | All 5 still required |
| Top 5 immediate actions | MINOR_UPDATE | Add: "Wire DEVIATION_ANALYSIS_GATE into `_build_steps()`" |

---

### §4.4 MAJOR_REWRITE — Replacement language

**Current text (v1.2.1):**
> 1. `audit_*_running` uses lease + heartbeat.
> 2. Missing heartbeat past timeout causes `audit_*_failed(timeout)`.
> 3. Retry is bounded by per-scope attempt budget.
> 4. Retry exhaustion remains failed and blocks completion/release.
> 5. Requeue allowed only while budget remains.

**Replacement text (post-v2.26):**
> 1. `audit_*_running` uses lease + heartbeat. The heartbeat substrate is the existing
>    `OutputMonitor.last_event_time` mechanism (`sprint/monitor.py:255-260`). A new `AuditLease`
>    model must be introduced with fields: `lease_id`, `owner`, `acquired_at`, `expires_at`,
>    `renewed_at`. The audit gate evaluator must emit periodic heartbeat events.
>
> 2. Missing heartbeat past `audit_lease_timeout` causes `audit_*_failed(timeout)`. The timeout
>    value must be decided by the Reliability Owner (see §9.2) and is separate from the subprocess
>    stall timeout (currently 120 s). Recommended baseline: `min(step_timeout_seconds, 300)`.
>
> 3. Retry is bounded by per-scope attempt budget. The bounded model mirrors the roadmap remediation
>    pattern (`roadmap/executor.py:677-723`): a JSON state block stores `audit_attempts` per
>    entity; `max_attempts` is configured per scope (task/milestone/release) with suggested
>    defaults: task=3, milestone=2, release=1.
>
> 4. Retry exhaustion remains failed and blocks completion/release.
>
> 5. Requeue allowed only while budget remains.
>
> 6. The subprocess turn budget (`max_turns * 120 + 300 s`) is the outer wall-clock ceiling for
>    any sprint phase execution. Audit gate evaluation must complete within this ceiling. For audit
>    gate sub-processes specifically, the turn budget is `max_turns * 60 s` (the remediation step
>    formula, `sprint/executor.py:73-79`), which at the default of 100 gives 6,000 s (1h 40m).
>
> 7. `reimbursement_rate = 0.8` exists in `TurnLedger` (`sprint/models.py:482-487`) but is
>    currently unused. The Reliability Owner must decide before Phase 2 GO: either wire this as a
>    turn-recovery credit for audit retry paths, or remove it from the model to avoid confusion.

---

### §10.2 MAJOR_REWRITE — Replacement language

**Current text (v1.2.1):**
> 1. `src/superclaude/cli/sprint/models.py` — states/enums/constraints/profile fields
> 2. `src/superclaude/cli/sprint/tui.py` — completion/release guards and operator guidance
> 3. `src/superclaude/skills/sc-audit-gate/SKILL.md` — command behavior/profile/output contract
> 4. `src/superclaude/skills/sc-audit-gate-protocol/SKILL.md` — deterministic evaluator and transition legality/recovery flow
> 5. `src/superclaude/agents/*.md` — enrichment-only role clarification
> 6-9. test files

**Replacement text (post-v2.26):**

> #### Phase 0 prerequisites (must complete before Phase 1 start)
>
> - `src/superclaude/cli/roadmap/executor.py:1193-1322` — remove `_apply_resume_after_spec_patch()`
>   and `_find_qualifying_deviation_files()` (spec-patch auto-resume retirement, per
>   approved-immediate)
> - `src/superclaude/cli/roadmap/executor.py:343-440` — add `deviation-analysis` step to
>   `_build_steps()` after `spec-fidelity`; `DEVIATION_ANALYSIS_GATE` is already defined at
>   `roadmap/gates.py:712-758`
>
> #### Phase 1: Deterministic contracts
>
> - `src/superclaude/cli/sprint/models.py` — add 12 audit workflow states (§4.1) as a new
>   `AuditWorkflowState` enum alongside existing `PhaseStatus`/`TaskStatus` (NOT replacing them);
>   add `AuditLease` dataclass; add `GateResult` dataclass (§6.1, separate from `GateDisplayState`
>   which remains for rendering); add profile enum (`strict | standard | legacy_migration`)
> - `src/superclaude/cli/sprint/models.py:482-487` — resolve `reimbursement_rate` fate
> - `src/superclaude/skills/sc-audit-gate-protocol/SKILL.md` — deterministic evaluator with
>   legal/illegal transition table; reference `pipeline/gates.py` GateCriteria pattern
>
> #### Phase 2: Runtime controls
>
> - `src/superclaude/cli/sprint/executor.py:47-90` — complete `SprintGatePolicy` and wire into
>   `execute_sprint()`; integration hook candidates: `executor.py:668-717` (post-subprocess,
>   pre-classification) and `executor.py:736-787` (post-classification, pre-halt decision)
> - `src/superclaude/cli/sprint/monitor.py` — extend `OutputMonitor` to support audit lease
>   heartbeat events as a distinct event class from subprocess output events
> - `src/superclaude/cli/pipeline/trailing_gate.py` — use `TrailingGateRunner` for task-scope
>   audit gates; `resolve_gate_mode()` already handles release-scope blocking
>
> #### Phase 3: Sprint CLI integration
>
> - `src/superclaude/cli/sprint/tui.py:174-203` — extend phase table row to display
>   `AuditWorkflowState` values; `tui.py:254-273` — add release guard (block "Sprint Complete"
>   unless `audit_release_passed`)
> - `src/superclaude/skills/sc-audit-gate/SKILL.md` — command surface, profile selection,
>   override governance flow
> - `src/superclaude/cli/tasklist/` and `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:622-637`
>   — add `audit_gate_required: bool` field to generated task metadata; derivation rule:
>   `Tier==STRICT or Risk==High or Critical Path Override==Yes`
> - `src/superclaude/cli/roadmap/executor.py:786-847` — add `audit` block to `_save_state()` for
>   audit gate result persistence
>
> #### Phase 4: Rollout
>
> - `tests/sprint/test_audit_gate_state_machine.py` — legal/illegal transitions + stuck-state
>   recovery
> - `tests/sprint/test_audit_gate_profiles.py` — profile determinism + severity behavior
> - `tests/sprint/test_audit_gate_overrides.py` — scope-limited override governance
> - `tests/sprint/test_audit_gate_rollout.py` — shadow/soft/full + rollback behavior

---

## 5. New Requirements Discovered

The following requirements are missing from the v1.2.1 spec based on what the
roadmap/tasklist/sprint runner now requires that was not anticipated during planning.

### NR-1 — Tasklist bundle must emit `audit_gate_required` per task

The sprint runner needs a declarative signal from the tasklist bundle about which tasks require
audit gating. Without this, the runner must infer it from task content at runtime, which breaks
determinism. The signal must be computed at tasklist generation time when tier/risk context is
available.

**Files affected**: `sc-tasklist-protocol/SKILL.md:622-637`,
`sc-tasklist-protocol/templates/phase-template.md:26-42`

**Derivation rule (proposed)**: `audit_gate_required = true` when any of:
- `Tier == STRICT`
- `Risk == High`
- `Critical Path Override == Yes`
- task description contains audit/compliance/security/schema keywords

---

### NR-2 — Tasklist schema versioning required

v2.26 spec-panel amendments (NFR-023) established `schema_version` as a required frontmatter
field in pipeline artifacts (`spec-deviations.md`, `deviation-analysis.md`). The v1.2.1 spec
does not address tasklist schema versioning. As audit metadata fields are added to phase files,
schema versioning becomes mandatory to prevent the sprint runner from silently accepting old
bundles lacking `audit_gate_required`.

**Proposed addition**: require `schema_version: "1.0"` in generated `tasklist-index.md` and gate
the sprint runner's preflight check on version compatibility.

---

### NR-3 — `deviation-analysis` step must be completed before audit gate design can be finalized

The v1.2.1 spec treats the audit gate as operating on a stable pipeline with known gates. However,
`DEVIATION_ANALYSIS_GATE` (the gate that routes roadmap deviations to remediation vs acceptance)
is defined but not yet wired into roadmap execution. Until it is wired and validated, the roadmap
pipeline does not produce the `deviation-analysis.md` artifact that an audit gate might need to
inspect. The audit gate Phase 1 acceptance criterion must include: "roadmap pipeline produces
validated `deviation-analysis.md` artifact."

---

### NR-4 — `reimbursement_rate` fate must be a spec-level decision

The `TurnLedger.reimbursement_rate = 0.8` field in `sprint/models.py:482-487` is a dormant
implementation artifact. The spec currently has no awareness of it. Before Phase 2 implementation,
the spec must explicitly decide its fate because:
- If kept: it should become the turn-recovery credit factor for audit retry paths (e.g., partial
  turn reimbursement when an audit gate fails with `transient` class)
- If removed: it should be explicitly marked as deprecated in both the spec and the model

Leaving it undefined creates an implementation gap where different implementers may inadvertently
activate or remove it with inconsistent results.

---

### NR-5 — Stale audit gate results need freshness invalidation semantics

The roadmap pipeline has a proven freshness invalidation pattern for downstream artifacts
(`executor.py:588-675`, `executor.py:1495-1511`). The audit gate result is a downstream artifact
of the phase files it audits. If a phase file is edited after an audit gate passes, the gate result
must be invalidated and the gate must re-run.

The v1.2.1 spec does not address audit result freshness/staleness. This is required for
correctness at Phase 1.

---

### NR-6 — `spec_hash`-style audit result binding

Audit gate results must be bound to specific versions of the artifacts they audited (similar to
how `spec_hash` binds roadmap resume logic to a specific spec snapshot). The `GateResult.artifacts`
block (§6.1) is the right place, but the spec does not specify how artifact versions are captured
or what triggers invalidation. This should be specified using the `spec_hash` SHA-256 pattern
already established in `roadmap/executor.py:792-806`.

---

### NR-7 — Sprint executor `execute_sprint()` mainline must be extended, not just `execute_phase_tasks()`

The spec's §10.1 Phase 3 targets `sprint/models.py` and `sprint/tui.py`. However, agent research
shows that `TurnLedger` budgeting (which implements task-level turn accounting) is wired into
`execute_phase_tasks()` but **not into the mainline `execute_sprint()` Claude-phase loop**
(`executor.py:574-579`). The primary phase lifecycle — where audit hooks must live — does not use
the task-level turn-ledger path. Any audit gate integration at Phase 3 must extend the mainline
`execute_sprint()` loop around `executor.py:668-787`, not just the `execute_phase_tasks()` helper.

---

## Summary Table

| Item | Type | Severity | Phase |
|---|---|---|---|
| Spec-patch auto-resume still present | Delta | HIGH — Phase 0 blocker | P0 |
| DEVIATION_ANALYSIS_GATE unwired | Delta | HIGH — audit prerequisite | P0 |
| `audit_*` states absent from sprint models | Delta | HIGH — Phase 1 core | P1 |
| GateResult model absent | Delta | HIGH — Phase 1 core | P1 |
| No lease model for `audit_*_running` | Delta | HIGH — Phase 2 core | P2 |
| SprintGatePolicy unwired | Delta | HIGH — Phase 2 core | P2 |
| TUI completion guard absent | Delta | MEDIUM — Phase 3 | P3 |
| Trailing gate not wired into sprint | Delta | MEDIUM — Phase 2 | P2 |
| Tasklist emits no audit metadata | New Requirement | MEDIUM — needed before sprint can declare | P3 |
| `reimbursement_rate` dead field | Delta | LOW — must resolve before P2 GO | P1 |
| STRICT/STANDARD axis collision | Delta | MEDIUM — spec clarity | P1 |
| Tasklist schema versioning | New Requirement | LOW — correctness risk | P3 |
| `deviation-analysis` as audit prerequisite | New Requirement | HIGH — gate dependency | P0 |
| Freshness invalidation for audit results | New Requirement | MEDIUM — correctness | P1 |
| `spec_hash`-style artifact binding | New Requirement | MEDIUM — determinism | P1 |
| Sprint mainline vs helper path gap | New Requirement | HIGH — integration target | P2 |
| Retry/backoff formula now concrete (positive) | Resolved Blocker | — | P1 |
| Bounded remediation model reusable (positive) | Integration Opportunity | — | P2 |
| Trailing gate infrastructure available (positive) | Integration Opportunity | — | P2 |
| Stall monitor as heartbeat substrate (positive) | Integration Opportunity | — | P2 |
