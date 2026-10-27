# Spec Refactoring Plan — Unified Audit Gating v1.2.1
## Incorporating Top-3 Validated Improvements

**Date**: 2026-03-17
**Target document**: `unified-audit-gating-v1.2.1-release-spec.md`
**Plan type**: Document refactoring plan only — no files modified here
**Source authority**: Proposals P05, P04, P02 (D-03/D-04) + their adversarial debate transcripts
**Persona**: Architect

---

## Contradiction Check Against §2.1 Locked Decisions

Before section-by-section changes, all three improvements are checked against the five locked
decisions. **No contradiction proceeds silently.**

| Locked Decision | P05 | P04 | P02 (D-03/D-04) | Verdict |
|----------------|-----|-----|-----------------|---------|
| LD-1: Configurable strictness/profile behavior | No conflict — `SilentSuccessConfig` is an additional config, not a profile replacement | No conflict | No conflict | CLEAR |
| LD-2: Tier-1 gate required even for LIGHT/EXEMPT flows | ⚠️ TENSION: P05 proposes EXEMPT-tier exemptions for individual steps. If all steps are EXEMPT, the detector's denominator is zero and it passes trivially. | No conflict — G-012 is a STRICT/RELEASE gate, not a replacement for Tier-1 | No conflict | **RESOLVE BELOW (C-1)** |
| LD-3: Overrides allowed only task/milestone, never release | P05 §4.2: hard-fail at release scope has no override — compliant. Soft-fail follows governance. | P04: no override path at release tier — compliant | No conflict | CLEAR |
| LD-4: Single primary command interface (`/sc:audit-gate`) | P04 proposes a `superclaude cli-portify smoke-test` standalone command — potential interface proliferation | Same | No conflict | **RESOLVE BELOW (C-2)** |
| LD-5: Explicit `audit_*` states are required | P05 integrates as a `GateResult` in Phase 2 — compliant when wired. Phase 1 (executor hook only) precedes `audit_*` state integration — not a violation, just pre-integration. | P04 occupies `audit_release_running` state — compliant | No conflict | CLEAR |

### C-1 Resolution: EXEMPT Step Denominator Edge Case

**Problem**: If a pipeline's `STEP_REGISTRY` marks all steps as EXEMPT, `SilentSuccessDetector`
evaluates against a zero denominator and produces `suspicion_score = 0` (false pass).

**Resolution for spec**: Add to §5.2 (pass/fail rules) a new normative invariant:
> "SilentSuccessDetector MUST treat a pipeline with zero non-EXEMPT, non-SKIPPED steps as a
> `policy` failure — not a pass — unless `--dry-run` was explicitly invoked and all steps are
> legitimately dry-run-excluded."

This closes the gap without modifying LD-2. EXEMPT classification still applies per-step; the
system-level guard prevents EXEMPT from being used to bypass detection at aggregate level.

### C-2 Resolution: Interface Proliferation

**Problem**: P04's `superclaude cli-portify smoke-test` is a new top-level command that conflicts
with LD-4's single primary interface.

**Resolution for spec**: The standalone `smoke-test` subcommand is scoped under `cli-portify`, not
under the audit gate namespace — it is a developer utility, not an audit gate command. Spec §2.2
(non-goals) should note:
> "Developer utility subcommands (`cli-portify smoke-test`) are not audit gate commands and do not
> replace or extend `/sc:audit-gate`."

The release-tier gate invocation still flows through the sprint executor's `audit_release_running`
state, which calls the smoke gate internally. The standalone command is a convenience wrapper.

---

## Change Map Overview

| § | Change | Type | Priority | Source |
|---|--------|------|----------|--------|
| §1.1 | Add three new implementation targets to scope | EXTEND | High | P05, P04, P02 |
| §1.3 | Clarify scope boundary re: standalone dev utilities | ADD | Low | C-2 resolution |
| §2.2 | Add `SilentSuccessDetector` EXEMPT edge case normative invariant | ADD | High | C-1 resolution |
| §2.3 | New contradiction row: LD-2 vs. EXEMPT denominator | ADD | Medium | C-1 resolution |
| §5.1 | Extend failure class taxonomy | EXTEND | High | P05 |
| §5.2 | Add normative rule for zero-denominator EXEMPT case | ADD | High | C-1 resolution |
| §6.1 | Extend GateResult with `silent_success_audit` block | EXTEND | High | P05 |
| §6.1 | Add `SmokeTestResult` as a named GateResult subtype | ADD | Medium | P04 |
| §8.3 | Add provisonal KPI for smoke test duration | ADD | Low | P04 |
| §10.1 | Insert Phase 0 prerequisites | EXTEND | High | P05, P04, P02 |
| §10.2 | Add seven new entries to file-level change map | ADD | High | P05, P04, P02 |
| §10.3 | Add acceptance criteria per improvement | EXTEND | High | P05, P04, P02 |
| §11 | Update checklist closure matrix | MODIFY | Medium | P05, P04, P02 |
| §12.3 | Update current blocker list | MODIFY | Medium | All three |
| New §13 | New section: Behavioral Gate Extensions | NEW_SECTION | High | P05, P04, P02 |
| Top 5 Actions | Add immediate actions for three improvements | EXTEND | High | All |

---

## Section-by-Section Changes

---

### §1.1 — Scope

**Current text** (excerpt):
> Implement a unified audit-gating capability that blocks completion/release transitions unless
> the corresponding gate passes at three scopes:
> 1. Task gate
> 2. Milestone gate
> 3. Release gate

**Change type**: EXTEND

**Proposed addition** (append after the three-scope list):

> Additionally, this release incorporates three validated behavioral gate extensions from the
> forensic analysis of the cli-portify no-op incident (2026-03-17):
>
> 4. **Silent Success Detection** — A mandatory post-execution hook (`SilentSuccessDetector`)
>    that runs inside `executor.run()` before `_emit_return_contract()`, detecting pipeline
>    runs where no real work was performed despite `outcome: SUCCESS` being reported.
>
> 5. **Smoke Test Gate (G-012)** — A release-tier blocking gate that invokes the CLI against a
>    minimal test fixture and validates that real artifacts with substantive content are produced.
>    Gate ID: G-012, enforcement tier: STRICT, scope: RELEASE.
>
> 6. **Spec Fidelity Deterministic Checks (D-03, D-04)** — Two new semantic check functions
>    added to `SPEC_FIDELITY_GATE` that deterministically verify named dispatch tables and
>    pseudocode dispatch function names are preserved from spec to roadmap. These supplement
>    (do not replace) the existing LLM-generated fidelity report.

**Rationale**: The three improvements address distinct detection points (execution time, release
gate, spec transition) and are normative additions to the release scope.

**Dependencies**: None — this is a scope declaration.

---

### §1.3 — Out-of-Scope for v1.2.1

**Current text** (excerpt):
> - New non-gating product features unrelated to transition control
> - Security hardening expansions not required for correctness of gate transitions
> - Full auto-tuning of profiles during rollout (deferred)

**Change type**: ADD

**Proposed addition** (append to the out-of-scope list):

> - **Developer utility subcommands** (`superclaude cli-portify smoke-test`) — these are
>   convenience wrappers over release-tier gate logic, not audit gate commands. They do not
>   extend or replace `/sc:audit-gate` and are not subject to the single-interface constraint
>   of LD-4.
> - **D-01 (FR-NNN identifier coverage)** and **D-05 (stub sentinel detection)** from the
>   spec fidelity hardening proposal — D-01 is non-load-bearing for specs using prose/pseudocode
>   rather than formal identifier notation; D-05 requires section-scope filtering before it is
>   safe to ship (high false positive risk in TDD workflows). Both are deferred post-v1.2.1.

**Rationale**: C-2 resolution requires an explicit scope boundary for the standalone command.
Explicit exclusion of D-01 and D-05 from scope prevents scope creep during implementation.

**Dependencies**: None.

---

### §2.2 — Non-Goals

**Current text**:
> - Release-level override capability
> - LLM/agent heuristics as source of truth for pass/fail

**Change type**: ADD

**Proposed addition** (append to non-goals):

> - **EXEMPT-tier classification as aggregate bypass** — individual steps may be classified as
>   EXEMPT (excluded from SilentSuccessDetector signal denominators) per §5.2 normative rule
>   C-1, but a pipeline where all steps are EXEMPT does not thereby achieve a pass; it produces
>   a `policy` failure unless `--dry-run` was explicitly invoked.
> - **Smoke test as bug fix substitute** — G-012 is a regression guard, not a replacement for
>   the wiring fix (Defect 1: `run_portify()` missing `step_runner`) or the validation fix
>   (Defect 2: `validate_portify_config()` not called). Both fixes are prerequisites for G-012
>   to pass a legitimate run.

**Rationale**: C-1 resolution; P04 Appendix B explicitly requires this distinction.

**Dependencies**: §5.2 addition (C-1 rule must be consistent with this non-goal).

---

### §2.3 — Contradictions and Winning Decisions

**Current text** (table excerpt):
> | Contradiction | Evidence | Winner in v1.2.1 | Rationale |
> |---|---|---|---|
> | `--strictness standard|strict` vs profile set... | ... | Canonical model is `--profile`... | ... |
> | ... | ... | ... | ... |

**Change type**: ADD

**Proposed addition** (append new row to contradictions table):

> | EXEMPT step denominator vs. Tier-1 gate requirement | `SilentSuccessDetector` EXEMPT classification (P05 §3.1) vs. LD-2 (Tier-1 gate required even for LIGHT/EXEMPT flows) | **C-1 resolution**: individual step EXEMPT exemptions are permitted; aggregate pipeline EXEMPT bypass is forbidden. A pipeline with zero non-EXEMPT, non-SKIPPED steps fails with `policy` failure class unless `--dry-run` was explicitly invoked. | Ensures EXEMPT classification cannot be used as an aggregate bypass of behavioral detection (§5.2 normative rule) |
> | Standalone `cli-portify smoke-test` command vs. single primary interface (LD-4) | P04 §6.3 proposes `superclaude cli-portify smoke-test` as standalone CLI; LD-4 mandates single primary interface `/sc:audit-gate` | **C-2 resolution**: `smoke-test` is scoped as a `cli-portify` utility subcommand, not an audit gate command. Release-tier gate invocation remains through sprint executor's `audit_release_running` state. | Preserves LD-4 intent; the utility command wraps gate logic rather than replacing the interface |

**Rationale**: Explicit contradiction documentation per spec methodology.

**Dependencies**: §2.2 non-goal additions; §5.2 normative rule.

---

### §5.1 — Failure Classes

**Current text**:
> - `policy`: rule/threshold violation
> - `transient`: recoverable execution issue
> - `system`: non-recoverable runner/system error
> - `timeout`: stale/expired running state
> - `unknown`: unmapped condition (fail-safe)

**Change type**: EXTEND

**Proposed addition** (append sub-classifications to `policy`):

> The `policy` failure class has three named sub-types for behavioral gate failures:
>
> - `policy.silent_success` — `SilentSuccessDetector` composite suspicion score ≥ soft-fail
>   threshold (0.50). Signals that the pipeline completed with `outcome: SUCCESS` but produced
>   no observable evidence of real work (no artifacts, near-zero timing, no fresh output files).
>
> - `policy.smoke_failure` — G-012 smoke gate blocked the release. Sub-types:
>   - `policy.smoke_failure.timing` — execution completed under `SMOKE_NOOP_CEILING_S` (5s)
>   - `policy.smoke_failure.artifact_absence` — fewer than minimum intermediate artifacts present
>   - `policy.smoke_failure.content_evidence` — artifact lacks fixture-specific content anchors
>
> - `policy.fidelity_deterministic` — `SPEC_FIDELITY_GATE` blocked by a deterministic check
>   (D-03 or D-04) independent of the LLM-generated severity counts.
>
> For the smoke test gate specifically, `transient` is used (not `policy`) when the gate cannot
> complete due to API unavailability, network failure, or HTTP 4xx/5xx from the LLM API. This
> enables retry without constituting a release block.

**Rationale**: P05 §4.2, P04 §5.2 and AC-005, P02 debate synthesis. Sub-type taxonomy enables
precise incident triage.

**Dependencies**: §6.1 GateResult extension (the `failure_class` field carries these sub-types).

---

### §5.2 — Pass/Fail Rules

**Current text**:
> 1. Any blocking check failure => gate `failed`.
> 2. Unknown/missing deterministic inputs => `failed`.
> 3. Missing evidence for failed check => `failed` and non-completable.
> 4. Completion/release transitions require latest gate `passed` except approved task/milestone
>    override path.

**Change type**: ADD

**Proposed addition** (append as rule 5):

> 5. **EXEMPT aggregate bypass prohibition (C-1 normative rule)**: A `SilentSuccessDetector`
>    evaluation where all evaluated steps have been classified as EXEMPT or SKIPPED produces a
>    `failed(policy.silent_success)` result — not a pass — unless:
>    (a) `--dry-run` was explicitly passed to the CLI invocation, OR
>    (b) the pipeline has zero registered steps (empty `STEP_REGISTRY`).
>    This rule prevents EXEMPT classification from being used as an aggregate gate bypass.
>    Individual step EXEMPT classification remains valid per-step for signal denominator exclusion.

**Rationale**: C-1 resolution. Enforces LD-2 (Tier-1 gate required even for LIGHT/EXEMPT flows)
against the SilentSuccessDetector's per-step EXEMPT exemption mechanism.

**Dependencies**: §2.2 non-goal and §2.3 contradiction row (must be consistent).

---

### §6.1 — GateResult

**Current text** (required fields list):
> Required fields:
> - `version`
> - `gate_run_id`
> - `scope`, `entity_id`, `profile`
> - `status`, `score`, `threshold`
> - `checks[]` (includes severity + evidence)
> - `drift_summary` (`edited`, `non_edited`)
> - `override` block
> - `timing` block
> - `artifacts` block
> - `failure_class` (v1.2 addition)

**Change type**: EXTEND

**Proposed addition** (append after the required fields list):

> #### v1.2.1 Behavioral Gate Extensions to GateResult
>
> **Silent success audit block** (required when `SilentSuccessDetector` ran):
> ```yaml
> silent_success_audit:
>   suspicion_score: float          # 0.0–1.0; higher = more suspicious
>   s1_artifact_coverage: float     # S1 score (before inversion)
>   s2_execution_activity: float    # S2 score (before inversion)
>   s3_output_freshness: float      # S3 score (before inversion)
>   band: pass|warn|soft_fail|hard_fail
>   diagnostics: list[str]          # per-signal failure messages with evidence
>   gate_decision: str              # PASS | SUSPICIOUS_SUCCESS | SILENT_SUCCESS_SUSPECTED
>   thresholds:                     # all thresholds that were applied (no magic numbers)
>     soft_fail: float
>     hard_fail: float
>     s2_suspicious_ms: float
>     s2_noop_ms: float
> ```
> This block MUST be written even when `suspicion_score = 0.0` (pass case), so that audit trails
> can confirm the detector ran and found no issues. Absence of the block is itself a `failed`
> condition at STRICT tier.
>
> **Smoke test result block** (required when G-012 ran):
> ```yaml
> smoke_test_result:
>   gate_id: G-012
>   fixture_path: str
>   elapsed_s: float
>   artifacts_found: list[str]      # relative paths of artifacts discovered
>   checks_passed: list[str]
>   checks_failed: list[GateFailure]
>   failure_class: transient|policy.smoke_failure.timing|policy.smoke_failure.artifact_absence|policy.smoke_failure.content_evidence
>   tmpdir_cleaned: bool            # AC-006 compliance evidence
> ```
>
> **Fidelity deterministic check block** (required when D-03/D-04 ran):
> ```yaml
> fidelity_deterministic:
>   dispatch_tables_found: list[str]     # named constants matching _DISPATCH_TABLE_PATTERN
>   dispatch_tables_preserved: bool      # false => gate blocked regardless of LLM severity counts
>   dispatch_functions_found: list[str]  # function name patterns matching _STEP_DISPATCH_CALL
>   dispatch_functions_preserved: bool   # false => gate blocked regardless of LLM severity counts
>   checks_run: [D-03, D-04]
>   checks_excluded: [D-01, D-05]        # explicitly deferred per §1.3
> ```
> **Critical invariant**: A fidelity report with `dispatch_tables_preserved: false` OR
> `dispatch_functions_preserved: false` MUST produce `gate failed` even when the LLM report
> has `high_severity_count: 0`. The deterministic checks are not overridable by LLM output.

**Rationale**: P05 §5.4 (return contract schema), P04 §6.2 (GateFailure dataclass), P02 §5
(acceptance criteria AC-02 and AC-07). The invariant for fidelity deterministic checks is the
most security-critical addition — it prevents LLM leniency from bypassing deterministic findings.

**Dependencies**: §5.1 failure class taxonomy (sub-types referenced here must be defined there).

---

### §8.3 — KPI/SLO: Warning/Fail Bands

**Current text**:
> - Runtime bands M1–M3 as defined in KPI table
> - Determinism floor M4 strict by tier
> - Evidence completeness M5 has no warning band (any miss is fail)

**Change type**: ADD

**Proposed addition** (append as new bullet):

> - **Smoke test gate duration M13** (provisional in shadow mode):
>   - Warning band: elapsed > 300s (5 minutes) for a minimal fixture run
>   - Fail band: elapsed > 600s (`SMOKE_TIMEOUT_S` ceiling; hard timeout)
>   - Note: the SMOKE_NOOP_CEILING_S (5s) is a *minimum* threshold, not a KPI target — runs
>     completing under 5s are failures, not acceptable fast results.
>   - Calibration owner: Reliability Owner (§9.2) must establish baseline from shadow-mode smoke
>     runs before M13 is normative.
>
> - **Silent success suspicion rate M14** (provisional):
>   - Warning band: > 5% of production runs produce `suspicion_score` in warn range (0.30–0.49)
>   - Fail band: > 1% of production runs produce soft-fail or hard-fail
>   - Indicates either threshold miscalibration (see C-1) or recurring no-op patterns
>   - Calibration owner: Reliability Owner; S2 thresholds require documented recalibration
>     protocol before M14 is normative (debate finding: timing thresholds lack methodology).

**Rationale**: P04 §5.2 (timeout budgets), debate-05 Round 2 (S2 calibration methodology gap).
Both metrics are provisional; they require shadow-mode data collection per §8.1/§8.2 before
becoming normative.

**Dependencies**: §8.1 (provisional vs. normative threshold rule applies here too).

---

### §10.1 — Phase Plan

**Current text**:
> - **Phase 0**: design/policy lock and owner/date assignments
> - **Phase 1**: deterministic contracts + evaluator + transition validator
> - **Phase 2**: runtime controls (lease/heartbeat/retry/recovery)
> - **Phase 3**: sprint CLI integration + override governance flow + report persistence
> - **Phase 4**: rollout execution + KPI gates + rollback drills

**Change type**: EXTEND

**Proposed addition** (replace Phase 0 description):

> - **Phase 0**: design/policy lock and owner/date assignments.
>   Phase 0 prerequisites for the three behavioral gate extensions:
>   - **P0-A (Defect fixes, prerequisite for G-012)**: Fix Defect 1 (`run_portify()` must pass
>     `step_runner` to `PortifyExecutor`) and Fix Defect 2 (`commands.py` must call
>     `validate_portify_config()` before `run_portify()`). These are independent of v1.2.1 spec
>     infrastructure and must be in production before G-012 can pass a legitimate run.
>   - **P0-B (SilentSuccessDetector Phase 1 deployment)**: `silent_success.py` module, executor
>     instrumentation, and `test_no_op_pipeline_scores_1_0` test. This is deployable in parallel
>     with the v1.2.1 Phase 1 spec work and has no dependency on `AuditWorkflowState` or
>     `GateResult` — in Phase 1, `SilentSuccessResult` emits to the `return-contract.yaml`
>     `silent_success_audit` block as a standalone artifact.
>   - **P0-C (D-03 + D-04 deployment)**: `fidelity_inventory.py` helper, two new semantic check
>     functions in `SPEC_FIDELITY_GATE`, and test `test_run_deterministic_inventory_cli_portify_case`.
>     Independently deployable in ~6 hours; no dependency on Phase 1 spec infrastructure.

**Proposed addition** (extend Phase 2 description):

> - **Phase 2**: runtime controls (lease/heartbeat/retry/recovery).
>   Phase 2 additionally integrates:
>   - G-012 smoke test gate (`smoke_gate.py`) — operational after P0-A fixes are in production.
>   - `SilentSuccessDetector` promoted from executor hook to `GateResult` entry — integrates with
>     the `AuditWorkflowState` and `SprintGatePolicy` wiring completed in Phase 2.
>   - S2 calibration protocol must be documented and approved by Reliability Owner before G-012
>     and M14 metrics are activated at Soft enforcement phase.

**Rationale**: P05 §8.4 (phasing), P04 §9 (sequencing), P02 §7 (independently deployable).
P0-B and P0-C can ship before v1.2.1 Phase 1 completes — this is the fastest value path.

**Dependencies**: §10.2 file-level change map entries must align with these phase assignments.

---

### §10.2 — File-Level Change Map

**Current text** (Phase 1 entries):
> #### Phase 1: Deterministic contracts
> - `src/superclaude/cli/sprint/models.py` — add 12 audit workflow states...
> - `src/superclaude/cli/sprint/models.py:482-487` — resolve `reimbursement_rate` fate
> - `src/superclaude/skills/sc-audit-gate-protocol/SKILL.md` — deterministic evaluator...

**Change type**: ADD

**Proposed additions** (insert before Phase 1 as new "Phase 0 Prerequisites" subsection):

> #### Phase 0 Prerequisites — Behavioral Gate Extensions
>
> **P0-A: Defect fixes (prerequisite for G-012; independent of spec infrastructure)**
> - `src/superclaude/cli/cli_portify/executor.py:1395-1401` — pass `step_runner` to
>   `PortifyExecutor` in `run_portify()`. Create `STEP_DISPATCH` mapping from step IDs to
>   imported step functions from `steps/*.py`.
> - `src/superclaude/cli/cli_portify/commands.py:95-109` — add `validate_portify_config()`
>   call between `load_portify_config()` and `run_portify()`. Exit non-zero on validation errors.
>
> **P0-B: Silent Success Detection (deployable immediately; no Phase 1 dependency)**
> - `src/superclaude/cli/cli_portify/silent_success.py` [NEW, ~300 lines]
>   `FileSnapshot`, `StepTrace`, `SilentSuccessConfig`, `SilentSuccessDetector`,
>   `SilentSuccessResult`, `SilentSuccessError` dataclasses and detector implementation.
> - `src/superclaude/cli/cli_portify/executor.py` [ADDITIVE, ~20 lines]
>   Change A: `_step_traces: list[StepTrace]` field + initialization.
>   Change B: `time.monotonic()` wrap around `_step_runner` call; append `StepTrace`.
>   Change C: Post-loop detector invocation before `_emit_return_contract()`.
>   Change D: `pipeline_start_time = time.time()` + `snapshot_pre_run()` call before step loop.
> - `src/superclaude/cli/cli_portify/models.py` [ADDITIVE, ~10 lines]
>   Add `PortifyOutcome.SILENT_SUCCESS_SUSPECTED` and `PortifyOutcome.SUSPICIOUS_SUCCESS` enums.
>   Add `silent_success_config: SilentSuccessConfig` field to `PortifyExecutor` (default instance).
>   Add `_pipeline_start_time: float` field.
> - `tests/cli_portify/test_silent_success.py` [NEW, ~200 lines]
>   7 tests including `test_no_op_pipeline_scores_1_0` (AC-10: must pass against current broken
>   executor) and `test_override_blocked_at_release_scope`.
>
> **P0-C: Spec Fidelity Deterministic Checks D-03 + D-04 (deployable in ~6h; no dependency)**
> - `src/superclaude/cli/roadmap/fidelity_inventory.py` [NEW, ~150 lines]
>   `SpecInventory` dataclass; `build_spec_inventory(spec_text: str) -> SpecInventory`;
>   `_DISPATCH_TABLE_PATTERN` regex; `_STEP_DISPATCH_CALL` regex; `_DEP_ARROW_PATTERN` regex.
>   **Scope note**: D-01 (FR-NNN) and D-05 (stub sentinels) are explicitly excluded from this
>   module per §1.3. Only D-03 and D-04 are implemented.
> - `src/superclaude/cli/roadmap/gates.py` [EXTEND, ~80 lines at lines 633-656]
>   Add `_check_dispatch_tables_preserved(content: str, inventory: SpecInventory) -> bool`.
>   Add `_check_dispatch_functions_preserved(content: str, inventory: SpecInventory) -> bool`.
>   Extend `SPEC_FIDELITY_GATE.semantic_checks` to include both new check functions.
>   Add enforcement: if `dispatch_tables_preserved: false` OR `dispatch_functions_preserved: false`
>   in frontmatter, gate fails regardless of `high_severity_count`.
> - `tests/roadmap/test_fidelity_inventory.py` [NEW, ~200 lines]
>   10 tests including `test_run_deterministic_inventory_cli_portify_case` which uses the actual
>   v2.25 spec and roadmap artifacts from `.dev/releases/complete/v2.25-cli-portify-cli/`.

**Proposed additions** (insert new Phase 2 entries after existing Phase 2 items):

> **Phase 2 additions — Behavioral Gate Integration**
> - `src/superclaude/cli/cli_portify/smoke_gate.py` [NEW, ~400 lines]
>   `SmokeTestConfig`, `SmokeTestResult` dataclasses; `run_smoke_test(config) -> SmokeTestResult`;
>   `_check_execution_time()`, `_check_intermediate_artifacts()`, `_check_artifact_content()`.
>   `SMOKE_TEST_GATE: GateCriteria` (tier=STRICT, scope=RELEASE).
>   Constants: `SMOKE_NOOP_CEILING_S=5`, `SMOKE_MIN_REAL_EXECUTION_S=10`, `SMOKE_TIMEOUT_S=600`.
>   **Timing check severity**: `WARN` only (not BLOCKING) per debate-04 critical finding.
>   Primary BLOCKING check: `intermediate-artifact-absence`.
>   `--mock-llm` mode required for CI environments without API access.
> - `src/superclaude/cli/cli_portify/gates.py` [EXTEND, ~5 lines]
>   Add `GATE_REGISTRY["smoke-test"] = SMOKE_TEST_GATE` (G-012 in the existing G-000–G-011 sequence).
> - `src/superclaude/cli/cli_portify/commands.py` [EXTEND, ~10 lines]
>   Add smoke gate invocation to release check path (runs once at pipeline completion, not per-step).
> - `tests/fixtures/cli_portify/smoke/sc-smoke-skill/SKILL.md` [NEW]
>   Minimal smoke fixture with component names `InputValidator`, `DataProcessor`, `OutputFormatter`.
>   Must retain these names — they are content evidence anchors in `smoke_gate.py`.
> - `tests/fixtures/cli_portify/smoke/sc-smoke-skill/refs/minimal-protocol.md` [NEW]
>   Minimal ref document (~10-20 lines) for component description.
> - `tests/fixtures/cli_portify/smoke/README.md` [NEW]
>   Stability contract: component names, maintenance rules, CI configuration notes.
> - `tests/cli_portify/test_smoke_gate.py` [NEW, ~200 lines]
>   5 unit tests covering AC-001 through AC-008. Includes `test_transient_failure_on_api_error`
>   and `test_fixture_content_matches_gate_patterns` (prevents fixture drift).
> - `src/superclaude/cli/cli_portify/silent_success.py` (Phase 2 update)
>   Integrate `SilentSuccessResult` into `GateResult` schema (§6.1 `silent_success_audit` block).
>   Gate failure class updated from standalone emission to `failed(policy.silent_success)`.

**Rationale**: P05 §5 (file summary), P04 §6 (implementation plan), P02 §4 (implementation plan).
All Phase 0 entries are independently deployable — no v1.2.1 Phase 1 infrastructure required.

**Dependencies**: Phase 2 G-012 and SilentSuccessDetector GateResult integration depend on
Phase 1 `AuditWorkflowState`, `GateResult` dataclass, and `SprintGatePolicy` completion.

---

### §10.3 — Acceptance Criteria Per Phase

**Current text**:
> - Phase 0: all blocking decisions closed with owner/date
> - Phase 1: deterministic replay stability for same input; fail-safe unknown handling
> - Phase 2: timeout/retry paths terminate deterministically (no deadlocks)
> - Phase 3: transition blocking/override rules enforced per scope
> - Phase 4: phase gates pass by KPI criteria and rollback drill success

**Change type**: EXTEND

**Proposed addition** (replace Phase 0 and Phase 2 criteria):

> - **Phase 0**: all blocking decisions closed with owner/date. ADDITIONALLY:
>   - **P0-A (Defect fixes)**: `run_portify()` with a test fixture produces at least one
>     intermediate artifact beyond `return-contract.yaml` (Fix 1 verified). `commands.py`
>     exits non-zero when `validate_portify_config()` returns errors (Fix 2 verified).
>   - **P0-B (SilentSuccessDetector)**: `test_no_op_pipeline_scores_1_0` passes against the
>     executor in its current state (no `step_runner` provided) — `suspicion_score = 1.0`,
>     outcome `SILENT_SUCCESS_SUSPECTED`. `return-contract.yaml` includes `silent_success_audit`
>     block. CLI exits non-zero.
>   - **P0-C (D-03/D-04)**: `test_run_deterministic_inventory_cli_portify_case` passes — the
>     actual v2.25 spec/roadmap pair produces `dispatch_tables_preserved: false` and
>     `dispatch_functions_preserved: false`. Gate rejects the roadmap even with
>     `high_severity_count: 0`.
>
> - **Phase 2**: timeout/retry paths terminate deterministically (no deadlocks). ADDITIONALLY:
>   - **G-012 smoke gate**: against the known-bad executor (step_runner not wired), smoke gate
>     fails with `policy.smoke_failure.timing` AND `policy.smoke_failure.artifact_absence`.
>     After P0-A fixes are applied, a real run against the smoke fixture passes all G-012 checks.
>   - **S2 calibration protocol**: documented and approved by Reliability Owner before soft-phase
>     activation of M14 metric.
>   - **SilentSuccessDetector GateResult integration**: `SilentSuccessResult` appears in the
>     unified audit trail with `failure_class: policy.silent_success`; override at release scope
>     is blocked; override at task/milestone scope requires valid `OverrideRecord`.
>   - **EXEMPT aggregate bypass guard (C-1)**: a pipeline with all-EXEMPT step registry
>     (without `--dry-run`) produces `failed(policy.silent_success)`, not pass.

**Rationale**: P05 AC-10 (test against current broken executor), P04 §7.3 (regression check),
P02 §5 AC-01 and AC-02, C-1 normative rule.

**Dependencies**: Phase 0 criteria must be verified before Phase 2 G-012 and GateResult integration
can be tested against real execution.

---

### §11 — Checklist Closure Matrix

**Current text** (excerpt):
> | 7. Sprint CLI integration | PASS (conditional) | Integrate deterministic transition validator before completion transitions | ... |
> | 10. Implementation readiness | NO-GO (current) | Close all 4 blockers with owner/date and reflect in artifacts | ... |

**Change type**: MODIFY

**Proposed changes** (add two new rows and update row 10):

> | **11. Behavioral gate extensions** | **PASS (conditional)** | P0-B and P0-C independently deployable with no spec infrastructure dependency; verify P0-A defect fixes are scheduled before G-012 integration | `proposal-05-silent-success-detection.md`, `proposal-04-smoke-test-gate.md`, `proposal-02-spec-fidelity-hardening.md` |
> | **12. Smoke gate CI prerequisites** | **NO-GO (current)** | `--mock-llm` mode must be specified before CI integration; API key configuration documented in `smoke/README.md`; `test_fixture_content_matches_gate_patterns` unit test must ship with gate on day one | `proposal-04-smoke-test-gate.md` §8.2, `debate-04` Round 2 synthesis |

**Update row 10**:
> | 10. Implementation readiness | **PARTIAL-GO** | Original 4 blockers remain (see §12.3). P0-B and P0-C are GO-eligible independently (no blocked dependencies). P0-A defect fixes must be scheduled. G-012 Phase 2 integration is conditional on Phase 1 completion. | `checklist-outcome-v1.2.md` + behavioral gate analysis |

**Rationale**: The three improvements change implementation readiness — P0-B and P0-C can
proceed now without waiting for the 4 original blockers. This upgrades row 10 from full NO-GO
to PARTIAL-GO.

**Dependencies**: §10.1 phase plan (P0-B, P0-C independence established there).

---

### §12.3 — Current Blocker List

**Current text**:
> 1. Profile thresholds and task-tier major-severity behavior not finalized
> 2. Retry/backoff/timeout values not finalized
> 3. Rollback/safe-disable triggers not finalized
> 4. Open blocking decisions not yet assigned owner+deadline in final artifact set

**Change type**: MODIFY

**Proposed replacement**:

> **Original blockers (still open for core v1.2.1 spec)**:
> 1. Profile thresholds and task-tier major-severity behavior not finalized
> 2. Retry/backoff/timeout values not finalized (partially resolved by v2.26 — see
>    `delta-analysis-post-v2.26.md` §1 for concrete formula; audit-specific lease budget remains TBD)
> 3. Rollback/safe-disable triggers not finalized
> 4. Open blocking decisions not yet assigned owner+deadline in final artifact set
>
> **New blockers introduced by behavioral gate extensions**:
> 5. **S2 calibration methodology** — Silent success detection timing thresholds (50ms suspicious,
>    10ms near-certain no-op) are not derived from benchmarks. Reliability Owner must document
>    calibration methodology and recalibration protocol before M14 metric is normative at soft phase.
>    (Source: `debate-05` Round 2, Devil's Advocate unchallenged finding)
> 6. **`--mock-llm` mode specification** — G-012 smoke gate cannot be safely integrated into CI
>    without a `--mock-llm` mode that validates all non-LLM checks without API calls. Mode must
>    be specified before Phase 2 CI integration. (Source: `debate-04` Round 2 synthesis)
> 7. **P0-A defect fix scheduling** — Defect 1 (`step_runner` wiring) and Defect 2
>    (`validate_portify_config()` call) must be scheduled as separate work items with owner and
>    deadline before G-012 smoke gate integration can begin. (Source: `proposal-04-smoke-test-gate.md` §8.5)

**Rationale**: Blockers 5-7 are actionable and independently scoped from the original 4. Blocker
5 is the highest-priority new item (impacts both M14 and long-term threshold maintenance).

**Dependencies**: §12.4 required user decisions must be extended to include S2 calibration approval.

---

### §12.4 — Required User Decisions

**Current text**:
> 1. Approve canonical profile model and numeric thresholds
> 2. Approve major-severity behavior at task tier under `standard`
> 3. Approve retry/backoff/timeout values and max attempts
> 4. Approve rollback/safe-disable objective triggers
> 5. Approve override governance model (single vs dual approver) and review cadence

**Change type**: EXTEND

**Proposed addition** (append new decisions):

> 6. **Approve S2 calibration methodology** — The Reliability Owner must specify: (a) the
>    measurement protocol for establishing `SUSPICIOUS_MS` and `NOOP_MS` thresholds from observed
>    production run data, (b) the recalibration trigger (e.g., "after major hardware change or
>    infrastructure migration"), and (c) who owns ongoing maintenance of `SilentSuccessConfig`
>    defaults. This decision blocks soft-phase activation of M14.
>
> 7. **Approve smoke gate `--mock-llm` scope** — Define what `--mock-llm` mode validates vs.
>    skips. At minimum: timing check remains active (mock mode must not skip the no-op ceiling
>    check); artifact-absence check must use real subprocess invocation with a stubbed LLM
>    response. Content evidence checks may be relaxed in mock mode. Decision must specify the
>    exact check matrix for `--mock-llm` vs. real mode.
>
> 8. **Approve D-03/D-04 pattern scope** — Confirm that D-03 (`_DISPATCH_TABLE_PATTERN`) and
>    D-04 (`_STEP_DISPATCH_CALL`) regex patterns are sufficiently general for the project's
>    spec authoring conventions, or specify required pattern extensions. This decision gates
>    `test_run_deterministic_inventory_cli_portify_case` becoming a normative regression test.

**Rationale**: S2 calibration was the Devil's Advocate's unchallenged finding in debate-05.
`--mock-llm` scope was debate-04's top recommendation from synthesis round.

**Dependencies**: §12.3 blockers 5-7 are unblocked by these decisions.

---

### New §13 — Behavioral Gate Extensions

**Change type**: NEW_SECTION

**Insert after §12, before "Top 5 Immediate Actions"**:

> ## 13. Behavioral Gate Extensions (v1.2.1 Additions)
>
> ### 13.1 Motivation
>
> Sections 1–12 of this spec address the audit workflow state machine, gate result schemas, and
> rollout mechanics — all operating on the transition layer between task/milestone/release states.
> Three validated improvements from the cli-portify no-op forensic analysis address a distinct
> gap: **the existing gate system validates documents; these extensions validate behavior**.
>
> The behavioral gate extensions are specified here as a unified section because they share a
> common motivation (the no-op anti-pattern), share an implementation wave (Phase 0 prerequisites),
> and have interdependencies (SilentSuccessDetector Phase 2 integration with GateResult).
>
> ### 13.2 Silent Success Detection (P05)
>
> **Gate type**: Post-execution executor hook (Phase 1); GateResult entry (Phase 2)
> **Scope**: Applies to cli-portify executor; generalizes to any executor using the
> `(exit_code, stdout, timed_out)` return pattern
> **Blocking**: soft-fail (0.50–0.74) = overridable at task/milestone; hard-fail (≥0.75) =
> never overridable at release tier (LD-3 compliance)
>
> **Signal suite**:
> | Signal | Measurement | Weight |
> |--------|-------------|--------|
> | S1 — Artifact Content | Per-step output file existence + min lines + section count + non-header ratio | 0.35 |
> | S2 — Execution Trace | `wall_clock_ms` and `stdout_bytes` per step via `time.monotonic()` wrap | 0.35 |
> | S3 — Output Freshness | mtime ≥ pipeline_start_time; content hash change from pre-run snapshot | 0.30 |
>
> **Composite formula**:
> ```
> suspicion_score = ((1-S1) × 0.35) + ((1-S2) × 0.35) + ((1-S3) × 0.30)
> ```
> Bands: 0.0–0.29 pass | 0.30–0.49 warn | 0.50–0.74 soft-fail | 0.75–1.00 hard-fail
>
> **Key constraints**:
> - S2 thresholds (50ms / 10ms) are provisional; Reliability Owner must approve calibration
>   methodology before soft-phase M14 activation (blocker 5, §12.3)
> - EXEMPT step classification excludes individual steps from signal denominators
> - EXEMPT aggregate bypass prohibition: see §5.2 rule 5 and C-1 resolution
> - `SilentSuccessConfig(enabled=False)` must be available for test harnesses
>
> ### 13.3 Smoke Test Gate G-012 (P04)
>
> **Gate ID**: G-012 (follows existing G-000 through G-011 in `cli_portify/gates.py`)
> **Enforcement tier**: STRICT | **Scope**: RELEASE | **Override**: forbidden (LD-3)
> **Prerequisites**: Defect 1 and Defect 2 fixes must be in production (blocker 7, §12.3)
>
> **Check hierarchy**:
> | Check | Severity | Blocks? | No-op failure mode |
> |-------|----------|---------|-------------------|
> | Timing: elapsed < SMOKE_NOOP_CEILING_S (5s) | WARN | No — advisory only | ~0.12s elapsed |
> | Intermediate artifact absence | ERROR | Yes | 0 artifacts beyond return-contract.yaml |
> | Content evidence (fixture proper nouns) | ERROR | Yes | No artifacts to check |
>
> **Critical debate finding**: Timing check is WARN only (not BLOCKING). The artifact-absence
> check is the primary BLOCKING mechanism. Timing as BLOCKING creates systematic CI false positives
> in environments where infrastructure overhead inflates startup time. (Source: debate-04 synthesis)
>
> **Fixture stability contract**: `tests/fixtures/cli_portify/smoke/sc-smoke-skill/SKILL.md`
> must retain component names `InputValidator`, `DataProcessor`, `OutputFormatter`. These are
> content evidence anchors — modifying them without updating `smoke_gate.py` breaks the gate.
>
> **Failure class routing**:
> - API unavailability, network errors, HTTP 4xx/5xx → `transient` (retryable)
> - Timing / artifact absence / content evidence → `policy.smoke_failure.*` (not retryable)
>
> ### 13.4 Spec Fidelity Deterministic Checks D-03 + D-04 (P02 subset)
>
> **Gate**: Extension to existing `SPEC_FIDELITY_GATE` in `roadmap/gates.py:633-656`
> **Deployment**: P0-C, independently deployable (~6h), no Phase 1 dependency
>
> **Check D-03 — Named dispatch table preservation**:
> Input: spec text (post-extraction), roadmap body text
> Detection: `_DISPATCH_TABLE_PATTERN` regex finds `UPPER_CASE_NAME = {` or `dict(` in spec;
> verifies each found name appears anywhere in roadmap text.
> Failure output: `dispatch_tables_preserved: false` in fidelity report frontmatter.
> Incident replay: `PROGRAMMATIC_RUNNERS = {` found in v2.25 spec; absent from roadmap →
> would have produced `dispatch_tables_preserved: false` and blocked the gate.
>
> **Check D-04 — Pseudocode dispatch function name preservation**:
> Input: spec text (code fences only), roadmap body text
> Detection: `_STEP_DISPATCH_CALL` regex finds `_run_*()` or `step_result = ` patterns in spec
> code fences; verifies at least one found function name appears in roadmap.
> Failure output: `dispatch_functions_preserved: false` in fidelity report frontmatter.
> Incident replay: `_run_programmatic_step`, `_run_claude_step` found in v2.25 spec pseudocode;
> absent from roadmap → would have produced `dispatch_functions_preserved: false`.
>
> **Critical invariant** (repeated from §6.1 for emphasis):
> A fidelity report with `dispatch_tables_preserved: false` OR `dispatch_functions_preserved: false`
> MUST produce `gate failed` even when `high_severity_count: 0`. The LLM cannot override these
> deterministic findings.
>
> **Explicitly excluded**:
> - D-01 (FR-NNN coverage): non-load-bearing for informal/prose specs; deferred
> - D-05 (stub sentinel detection): high TDD false positive risk without section-scope filtering;
>   deferred until filtering is implemented

**Rationale**: A single authoritative section documenting all three behavioral gate extensions
with their constraints, failure modes, and interdependencies prevents these from being scattered
across the spec with inconsistent cross-references.

**Dependencies**: §5.1 (failure class sub-types defined there); §6.1 (GateResult blocks defined
there); §10.2 (files defined there); §12.3 (blockers referenced here).

---

### Top 5 Immediate Actions

**Current text**:
> 1. Finalize and sign off profile thresholds + major-severity behavior.
> 2. Finalize retry/backoff/timeout and stale-state budgets.
> 3. Ratify explicit legal/illegal transition table as implementation authority.
> 4. Approve rollback/safe-disable triggers and phase regression policy.
> 5. Assign owner + UTC deadline + effective phase to each blocking decision.

**Change type**: EXTEND

**Proposed replacement** (prepend three highest-ROI actions before existing list):

> **Behavioral gate extension actions (can proceed immediately, no spec blocker dependency)**:
>
> 0a. **Deploy P0-B (SilentSuccessDetector)**: Implement `silent_success.py` + executor
>     instrumentation + `test_no_op_pipeline_scores_1_0`. This alone would have blocked the
>     no-op pipeline across all three v2.24–v2.25 releases. Estimated effort: 2.5 days.
>     Owner: [TBD]. Start: immediately (no dependency).
>
> 0b. **Deploy P0-C (D-03 + D-04)**: Implement `fidelity_inventory.py` + two semantic checks
>     in `SPEC_FIDELITY_GATE` + regression test using v2.25 artifacts. Estimated effort: ~6h.
>     Owner: [TBD]. Start: immediately (no dependency). D-01 and D-05 explicitly excluded.
>
> 0c. **Schedule P0-A defect fixes**: Wire `run_portify()` to step dispatch (Fix 1) and add
>     `validate_portify_config()` call in `commands.py` (Fix 2). These are prerequisites for
>     G-012 smoke gate; they are not v1.2.1 spec items but must be scheduled with owner + deadline
>     before Phase 2 begins. Estimated effort: ~1.5 days total.
>
> **Original actions (renumbered)**:
>
> 1. Finalize and sign off profile thresholds + major-severity behavior.
> 2. Finalize retry/backoff/timeout and stale-state budgets.
> 3. Ratify explicit legal/illegal transition table as implementation authority.
> 4. Approve rollback/safe-disable triggers and phase regression policy.
> 5. Assign owner + UTC deadline + effective phase to each blocking decision (now includes
>    blockers 5-7 from §12.3 and user decisions 6-8 from §12.4).

**Rationale**: Actions 0a and 0b can be executed today without waiting for the four original
blockers (profile thresholds, retry/backoff, rollback triggers, owner assignments). They deliver
immediate protection against the documented incident class.

**Dependencies**: 0a has no dependencies. 0b has no dependencies. 0c must precede Phase 2 G-012
integration.

---

## Implementation Order Summary

```
TODAY (no dependencies):
  ├── 0a: silent_success.py + test_no_op_pipeline_scores_1_0    [2.5 days]
  └── 0b: fidelity_inventory.py + D-03/D-04 + regression test  [6 hours]

PARALLEL (separate work items, prerequisite for G-012):
  └── 0c: Fix 1 (step_runner wiring) + Fix 2 (validation call) [1.5 days]

PHASE 1 (existing v1.2.1 Phase 1 work):
  └── AuditWorkflowState, GateResult dataclass, SprintGatePolicy

PHASE 2 (requires Phase 1 + 0c):
  ├── G-012 smoke_gate.py + smoke fixture + test_smoke_gate.py  [3 days]
  └── SilentSuccessDetector → GateResult integration            [1 day]
```

Total behavioral gate extension effort: ~8 days across two waves.
Core v1.2.1 spec work proceeds on its own timeline in parallel.

---

## Files Referenced but Not Changed by This Plan

The following files are referenced in the proposals but require NO changes to the spec document:
- `src/superclaude/cli/pipeline/trailing_gate.py` — smoke gate does not use TrailingGateRunner
- `src/superclaude/cli/roadmap/prompts.py` — D-03/D-04 are semantic checks, not prompt changes
- `src/superclaude/cli/cli_portify/gates.py` — `GATE_REGISTRY` update is a code change, not a spec change
- Any existing test files — behavioral gate tests are new files only

These are implementation targets, not spec targets. They appear in §10.2 but do not require
additional spec language beyond what is already in this plan.
