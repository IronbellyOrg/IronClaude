# Tasklist: Spec Corrections F-01 through F-11
# Target: unified-audit-gating-release-spec.md (via spec-refactor-plan-merged.md)
# Compliance: strict (sc:task-unified)
# Generated: 2026-03-18
# Source: Expert Panel Review findings F-01 through F-11

---

## Metadata

```yaml
schema_version: 1
tasklist_id: spec-corrections-f01-f11
target_spec: .dev/releases/current/v3.0_unified-audit-gating/spec-refactor-plan-merged.md
compliance_tier: STRICT
total_tasks: 11
phases: 3
estimated_effort: 8-12 hours (spec document edits only)
blocking_gate: All F-01 through F-11 corrections MUST be applied before any implementation work begins
```

---

## Phase 1: CRITICAL Corrections (Blocks All Implementation)

These corrections fix provably wrong spec content. No implementation task may begin until Phase 1 is complete.

---

### T-01: Rewrite SS10.2 Phase 0 Spec-Patch Retirement as Migration [F-01, F-02]
**Severity**: CRITICAL
**Compliance**: STRICT
**Depends on**: None
**Blocks**: T-02, T-03, T-04, T-05, T-06, T-07, T-08, T-09, T-10, T-11

#### Context
The spec (SS10.2 Phase 0, line 689) says:
> `roadmap/executor.py -- remove _apply_resume_after_spec_patch() and _find_qualifying_deviation_files() (spec-patch auto-resume retirement)`

**This is provably wrong.** Both functions are ACTIVELY CALLED:
- `_apply_resume_after_spec_patch()` defined at `executor.py:1236`, called at `executor.py:1147`
- `_find_qualifying_deviation_files()` defined at `executor.py:1189`, called at `executor.py:1269`
- 20+ test call sites in `tests/roadmap/test_spec_patch_cycle.py`

The spec's evidence citation (line 597) references `execute_phase_tasks()` as confirmed dead code — that is a DIFFERENT function. The two spec-patch functions were incorrectly conflated with it during the Plan A/B merge.

#### Instructions

**Step 1**: Open `spec-refactor-plan-merged.md` and locate these three sections:
- Line 625: `Code: retire _apply_resume_after_spec_patch() (roadmap executor)`
- Line 689: `roadmap/executor.py -- remove _apply_resume_after_spec_patch() and _find_qualifying_deviation_files()`
- Line 597: `Evidence basis: execute_phase_tasks() confirmed dead code`

**Step 2**: Replace line 625 with:
```
Code: MIGRATE spec-patch auto-resume path to deviation-analysis step (3-step migration):
  Step M1: Wire deviation-analysis step into _build_steps() (includes _get_all_step_ids() and build_deviation_analysis_prompt())
  Step M2: Rewrite _apply_resume_after_spec_patch() call site (executor.py:1147) to use deviation-analysis path
  Step M3: Migrate tests/roadmap/test_spec_patch_cycle.py to test the new path with equivalent coverage
  Step M4: Only after M1-M3 pass CI, retire _apply_resume_after_spec_patch() and _find_qualifying_deviation_files()
  ORDERING CONSTRAINT: M1 → M2 → M3 → M4 (strict sequential, no parallelism)
```

**Step 3**: Replace line 689 with:
```
- `roadmap/executor.py` -- MIGRATION (not removal): wire deviation-analysis step (M1), migrate spec-patch call site at line 1147 (M2), retire old functions only after replacement path passes CI (M4). See Phase 0 migration steps M1-M4.
```

**Step 4**: Add after line 597:
```
> - **Correction (2026-03-18 panel review)**: The dead code evidence applies to `execute_phase_tasks()` only. The functions `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()` are NOT dead code — they have active production call sites (executor.py:1147, executor.py:1269) and 20+ test references. These require a migration path, not retirement.
```

**Step 5**: Add a new acceptance criterion to Phase 0 go/no-go gate (after line 630):
```
  - Migration criterion: All existing test_spec_patch_cycle.py tests must either pass against the replacement deviation-analysis path OR be explicitly superseded by equivalent new tests with equal or greater coverage. test_spec_patch_cycle.py is NOT deleted; it is migrated.
```

#### Acceptance Criteria
- [ ] Lines 625, 689, 597 are corrected per instructions
- [ ] Migration steps M1-M4 are present with explicit ordering constraint
- [ ] Phase 0 go/no-go gate includes migration acceptance criterion
- [ ] No remaining "retire" or "remove" language for spec-patch functions without migration prerequisite
- [ ] Grep for `_apply_resume_after_spec_patch` in the spec confirms all references use "migrate" not "retire/remove"

---

### T-02: Add Audit State Persistence Schema to SS6.1 [F-03]
**Severity**: CRITICAL → MAJOR
**Compliance**: STRICT
**Depends on**: T-01
**Blocks**: T-04, T-07

#### Context
The spec (line 655) says `_save_state(): add audit block for gate result persistence` but provides NO schema. The existing `.roadmap-state.json` has 5 top-level blocks each with different schemas, and a pre-existing bug where `remediation_attempts` is read but never written. Adding another unspecified block repeats this failure pattern.

#### Instructions

**Step 1**: Locate SS6.1 in the spec (around line 461). Find the `AuditGateResult` dataclass description.

**Step 2**: After the `AuditGateResult` field listing, add a new subsection:

```markdown
#### Audit State Persistence Schema

The `audit` block in `.roadmap-state.json` MUST conform to this schema:

\`\`\`json
{
  "audit": {
    "workflow_state": "<AuditWorkflowState enum value>",
    "gate_results": [
      {
        "gate_id": "<string, e.g. 'G-012'>",
        "scope": "<'milestone' | 'release'>",
        "status": "<'passed' | 'failed' | 'skipped' | 'timeout'>",
        "failure_class": "<string | null, e.g. 'policy.silent_success'>",
        "failure_sub_type": "<string | null>",
        "evidence_artifacts": ["<path>"],
        "evaluated_at": "<ISO-8601 UTC>",
        "attempt": "<int>",
        "evaluator_version": "<string>"
      }
    ],
    "lease": {
      "lease_id": "<uuid | null>",
      "owner": "<string | null>",
      "acquired_at": "<ISO-8601 UTC | null>",
      "expires_at": "<ISO-8601 UTC | null>",
      "renewed_at": "<ISO-8601 UTC | null>"
    },
    "attempts": "<int, total audit attempts for current entity>",
    "last_audit_at": "<ISO-8601 UTC | null>"
  }
}
\`\`\`

**Round-trip invariant**: `_save_state()` MUST preserve all fields in the `audit` block. `read_state()` MUST treat a missing `audit` key as `null` (not-yet-evaluated), never as `passed`.

**Schema version**: Adding the `audit` block increments `schema_version` from 1 to 2. Loading a v1 state file in v2 code MUST treat the missing `audit` block as `audit: null`.
```

**Step 3**: Update the Phase 3 `_save_state()` entry (line 655/733) to reference the schema:
```
- `_save_state()`: add `audit` block per SS6.1 Audit State Persistence Schema. MUST include round-trip serialization test.
```

#### Acceptance Criteria
- [ ] SS6.1 contains a concrete JSON schema for the audit block
- [ ] Round-trip invariant is stated as a normative requirement
- [ ] Schema version migration rule (v1 → v2) is specified
- [ ] Phase 3 _save_state() entry references the SS6.1 schema

---

### T-03: Fix Pre-Existing remediation_attempts Persistence Bug [F-04]
**Severity**: MAJOR
**Compliance**: STRICT
**Depends on**: T-01
**Blocks**: T-02 (schema formalization depends on fixing the pattern)

#### Context
`_check_remediation_budget()` at `executor.py:720-759` reads `remediation_attempts` from state. Tests at `test_executor.py:429-506` construct state files with this key. But `_save_state()` at `executor.py:823-890` never writes or preserves `remediation_attempts`. This is a pre-existing bug that silently resets remediation budget tracking across pipeline restarts.

#### Instructions

**Step 1**: Add a new P0 prerequisite item to SS10.2 Phase 0 (after the migration steps from T-01):

```markdown
**P0-D (State schema formalization, prerequisite for Phase 1 and Phase 3)**:
- `src/superclaude/cli/roadmap/executor.py` -- Fix `_save_state()` to persist `remediation_attempts` field. Currently `_check_remediation_budget()` reads this field but `_save_state()` never writes it, causing silent budget reset on pipeline restart.
- `tests/roadmap/test_executor.py` -- Add round-trip persistence test: write state with `remediation_attempts=N`, call `_save_state()`, reload, assert `remediation_attempts==N`.
- Formalize `.roadmap-state.json` as a documented schema (dataclass or JSON Schema) with round-trip test coverage for ALL top-level keys before adding the audit block.
```

**Step 2**: Add to the Phase 0 go/no-go gate:
```
  - State schema criterion: `_save_state()` round-trip test passes for ALL existing fields including `remediation_attempts`.
```

#### Acceptance Criteria
- [ ] P0-D is present in SS10.2 Phase 0 with the remediation_attempts fix
- [ ] Round-trip test requirement is specified
- [ ] Phase 0 go/no-go gate includes state schema criterion

---

## Phase 2: MAJOR Corrections (Blocks Specific Implementation Phases)

These corrections fix architectural ambiguities and missing specifications.

---

### T-04: Move AuditGateResult to pipeline/models.py [F-05]
**Severity**: MAJOR
**Compliance**: STRICT
**Depends on**: T-01, T-02
**Blocks**: None (but affects all Phase 1+ implementation)

#### Context
The spec (line 462, 708) places `AuditGateResult`, `AuditWorkflowState`, and `AuditLease` in `sprint/models.py`. But these are cross-cutting: used by sprint, cli_portify, and roadmap executors. The codebase already has `pipeline/models.py` as the shared base layer (containing `GateCriteria`, `GateMode`, `StepStatus` etc.). Placing cross-cutting models in sprint creates an import inversion: cli_portify would need to import from sprint.

Current import pattern:
- `sprint/models.py` imports from `pipeline/models.py` ✓
- `roadmap/models.py` imports from `pipeline/models.py` ✓
- `cli_portify/models.py` is standalone (does NOT import from sprint) ✓
- **Proposed**: cli_portify importing from sprint/models.py ✗ (inversion)

#### Instructions

**Step 1**: Locate SS3.1 (around line 461) where the spec says:
> `AuditGateResult is a new dataclass to be added to src/superclaude/cli/sprint/models.py`

Replace with:
> `AuditGateResult is a new dataclass to be added to src/superclaude/cli/pipeline/models.py, alongside existing shared types (GateCriteria, GateMode, StepStatus). This placement avoids import inversion: cli_portify and roadmap can import from pipeline/ without depending on sprint/.`

**Step 2**: Locate SS10.2 Phase 1 (line 708) where the spec says:
> `src/superclaude/cli/sprint/models.py -- add AuditWorkflowState enum ... add AuditGateResult dataclass ... add AuditLease dataclass ... add profile enum`

Replace with:
> `src/superclaude/cli/pipeline/models.py -- add AuditWorkflowState enum (milestone + release scopes only), AuditGateResult dataclass (SS6.1, disambiguated from existing cli/audit/ GateResult), AuditLease dataclass`
> `src/superclaude/cli/sprint/models.py -- add profile enum (strict | standard | legacy_migration). Import AuditWorkflowState, AuditGateResult, AuditLease from pipeline.models.`

**Step 3**: Search the entire spec for "sprint/models.py" referencing audit types and update any remaining references to point to `pipeline/models.py`.

#### Acceptance Criteria
- [ ] SS3.1 specifies pipeline/models.py as the target for AuditGateResult
- [ ] SS10.2 Phase 1 splits the addition: shared types → pipeline/models.py, sprint-specific → sprint/models.py
- [ ] No reference in the spec places AuditWorkflowState, AuditGateResult, or AuditLease in sprint/models.py
- [ ] Profile enum remains in sprint/models.py (sprint-specific)

---

### T-05: Clarify G-012 Registry Target [F-06]
**Severity**: MAJOR
**Compliance**: STRICT
**Depends on**: T-01
**Blocks**: None

#### Context
The codebase has THREE incompatible gate registry patterns:
| Subsystem | Variable | Shape |
|-----------|----------|-------|
| `roadmap/gates.py` | `ALL_GATES` | `list[(name, GateCriteria)]` |
| `cli_portify/gates.py` | `GATE_REGISTRY` | `dict[str, GateCriteria]` |
| `cleanup_audit/gates.py` | `ALL_GATES` | `dict[str, GateCriteria]` |

The spec (line 722) correctly says `Add GATE_REGISTRY["smoke-test"] = SMOKE_TEST_GATE` targeting cli_portify, but never acknowledges the three-registry landscape. An implementer could confuse which registry G-012 belongs to.

#### Instructions

**Step 1**: After line 722, add a normative note:
```markdown
> **Registry clarification (panel review 2026-03-18)**: G-012 is registered ONLY in `cli_portify/gates.py:GATE_REGISTRY`. The roadmap pipeline uses a separate `ALL_GATES` list (no G-ID numbering). The cleanup_audit pipeline uses a separate `ALL_GATES` dict (keyed by G-ID). These are three independent registries with incompatible data structures. Unification of gate registries across subsystems is NOT in scope for v1.2.1 and is recorded as deferred technical debt.
```

**Step 2**: Add to SS12.3 (blockers) or the deferred items list:
```markdown
> - **Deferred**: Gate registry unification across subsystems (roadmap list, cli_portify dict-by-name, cleanup_audit dict-by-ID). Current inconsistency is manageable but increases onboarding cost.
```

#### Acceptance Criteria
- [ ] Normative note after line 722 specifies G-012 belongs to cli_portify GATE_REGISTRY only
- [ ] Three-registry landscape is documented
- [ ] Registry unification is recorded as deferred technical debt

---

### T-06: Fix 7 Guard Condition Boundary Gaps [F-07]
**Severity**: MAJOR
**Compliance**: STRICT
**Depends on**: T-01
**Blocks**: None

#### Context
The panel's Guard Condition Boundary Table identified 7 GAP entries where the spec does not define behavior at boundary conditions. Each GAP is a MAJOR finding.

#### Instructions

**Step 1 — C-1 All-SKIPPED gap (SS5.2, line 50)**: The C-1 resolution covers all-EXEMPT but not all-SKIPPED-without-dry-run. After the C-1 resolution text, add:
```markdown
> **Extended guard**: SilentSuccessDetector MUST also treat a pipeline with zero non-SKIPPED steps as a `policy` failure unless:
> (a) `--dry-run` was explicitly invoked, OR
> (b) the pipeline is in a resume state where SKIPPED steps represent already-completed work with verified output artifacts (artifact existence check required).
```

**Step 2 — C-1 Resume-skip gap (SS5.2)**: Covered by Step 1(b) above.

**Step 3 — SMOKE_NOOP_CEILING_S boundary (SS13.3)**: In the smoke gate constant definitions (line 721 area), add:
```markdown
> **Boundary semantics**: All timing thresholds use strict inequality. `execution_time < SMOKE_NOOP_CEILING_S` triggers WARN. `execution_time >= SMOKE_MIN_REAL_EXECUTION_S` is considered real execution. Exactly-at-boundary values are treated as NOT triggering the lower threshold (i.e., 5.0s exactly does NOT trigger the noop warning; 10.0s exactly IS considered real execution).
```

**Step 4 — SMOKE_MIN_REAL_EXECUTION_S boundary**: Covered by Step 3 above.

**Step 5 — audit_lease_timeout zero (SS4.4, line 292)**: After the lease timeout definition, add:
```markdown
> **Guard**: `audit_lease_timeout` MUST be a positive integer greater than zero. A value of 0 is a configuration error and MUST be rejected at initialization, not at runtime.
```

**Step 6 — Stale lease from crash (SS4.4)**: After the lease heartbeat definition, add:
```markdown
> **Abandoned lease recovery**: A lease whose `expires_at` is in the past MUST be considered abandoned. A new audit run MAY acquire an abandoned lease without owner consent. The abandoned lease's `owner` and `lease_id` are logged for forensic tracing before overwrite.
```

**Step 7 — max_attempts zero (SS4.4, line 296)**: After the max_attempts definition, add:
```markdown
> **Guard**: `max_attempts` MUST be a positive integer ≥ 1. A value of 0 is a configuration error (no attempts means no audit can ever run) and MUST be rejected at initialization.
```

#### Acceptance Criteria
- [ ] C-1 extended to cover all-SKIPPED-without-dry-run and resume-skip scenarios
- [ ] Smoke gate timing thresholds have explicit boundary semantics (strict inequality)
- [ ] audit_lease_timeout has >0 guard
- [ ] Abandoned lease recovery mechanism is specified
- [ ] max_attempts has ≥1 guard
- [ ] All 7 GAP entries from the boundary table are addressed

---

### T-07: Add PortifyOutcome Consumer Impact Analysis [F-08]
**Severity**: MAJOR
**Compliance**: STRICT
**Depends on**: T-01
**Blocks**: None

#### Context
The spec (SS10.2 P0-B, line 699) adds `SILENT_SUCCESS_SUSPECTED` and `SUSPICIOUS_SUCCESS` to `PortifyOutcome` enum. Current enum has: `SUCCESS`, `FAILURE`, `TIMEOUT`, `INTERRUPTED`, `HALTED`, `DRY_RUN`. Any downstream code using exhaustive matching on PortifyOutcome will silently fall through to defaults for the new variants.

#### Instructions

**Step 1**: After line 699 (the PortifyOutcome additions), add:

```markdown
> **Consumer impact analysis (required before implementation)**:
> All consumers of `PortifyOutcome` must be audited for exhaustive handling of new variants. Known consumers (as of 2026-03-18):
> - `cli_portify/executor.py` — outcome classification logic
> - `cli_portify/diagnostics.py` — outcome-to-diagnostic mapping
> - `return-contract.yaml` emission — outcome serialization
> - TUI display — outcome-to-display-state mapping
>
> For each consumer: if the consumer uses `if outcome == SUCCESS` branching, the new variants MUST be handled explicitly. `SILENT_SUCCESS_SUSPECTED` MUST NOT be treated as `SUCCESS` by any consumer. `SUSPICIOUS_SUCCESS` MUST be treated as a warning-level outcome that does not block but does annotate.
>
> **Implementation requirement**: P0-B implementer MUST grep for all `PortifyOutcome` references in `src/superclaude/cli/cli_portify/` and update each switch/branch to handle the new variants before merging.
```

#### Acceptance Criteria
- [ ] Consumer impact analysis section exists after the PortifyOutcome addition
- [ ] Known consumers are listed
- [ ] Handling semantics for SILENT_SUCCESS_SUSPECTED and SUSPICIOUS_SUCCESS are specified
- [ ] Implementation requirement for exhaustive consumer audit is stated

---

### T-08: Add Abandoned Lease Acquisition Rule to SS4.4 [F-09]
**Severity**: MAJOR
**Compliance**: STRICT
**Depends on**: T-06 (the lease boundary fix includes this)
**Blocks**: None

#### Context
SS4.4 specifies lease heartbeat renewal but does not define what happens if lease acquisition itself fails due to a stale lease from a crashed prior run. This is already partially covered by T-06 Step 6.

#### Instructions

**Step 1**: Verify T-06 Step 6 (abandoned lease recovery) is complete. If so, this task is satisfied by T-06.

**Step 2**: Additionally, add to SS4.4 after the lease model definition:

```markdown
> **Lease acquisition failure modes**:
> 1. **No existing lease**: Acquire normally. Set `lease_id`, `owner`, `acquired_at`, `expires_at`.
> 2. **Active lease held by another process**: Acquisition MUST fail. Caller retries after backoff or reports `audit_*_failed(lease_contention)`.
> 3. **Abandoned lease** (expires_at in the past): Acquire by overwriting. Log previous `owner` and `lease_id` for forensic tracing.
> 4. **Own stale lease** (same owner, expires_at in the past): Re-acquire with new `lease_id` and fresh timestamps.
```

#### Acceptance Criteria
- [ ] Four lease acquisition failure modes are specified in SS4.4
- [ ] Abandoned lease recovery (mode 3) aligns with T-06 Step 6
- [ ] Lease contention failure class is named

---

### T-09: Document Sprint→cli_portify Cross-Domain Dependency [F-10]
**Severity**: MAJOR
**Compliance**: STRICT
**Depends on**: T-05
**Blocks**: None

#### Context
The smoke gate (`smoke_gate.py`) lives under `cli_portify/` but is invoked during sprint execution as a release-tier gate. The current architecture has sprint importing from `pipeline/` (shared) but NOT from `cli_portify/` (domain-specific). The spec introduces a new cross-domain dependency without acknowledging it.

#### Instructions

**Step 1**: In SS10.2 Phase 2 (around line 720), after the smoke gate file entries, add:

```markdown
> **Architecture note**: The smoke gate introduces a new dependency edge: `sprint/executor.py` → `cli_portify/smoke_gate.py`. This is an intentional exception to the rule that domain packages only import from `pipeline/`. The dependency is acceptable because:
> 1. The smoke gate is a release-tier validation that specifically tests cli_portify pipeline health
> 2. The invocation is mediated through the sprint gate policy, not a direct import
> 3. The gate criteria (`SMOKE_TEST_GATE`) are registered in cli_portify's `GATE_REGISTRY` and looked up by ID, not by direct import
>
> If this pattern repeats for other domain-specific gates, consider elevating the smoke gate interface to `pipeline/` as a shared abstraction. For v1.2.1, the direct dependency is accepted.
```

**Step 2**: Add to the dependency order section at the end of the spec (if a dependency graph exists):
```
sprint/executor.py → cli_portify/smoke_gate.py (new, v1.2.1 exception)
```

#### Acceptance Criteria
- [ ] Architecture note documents the sprint→cli_portify dependency
- [ ] Justification for the exception is provided
- [ ] Escalation path (elevate to pipeline/) is noted for future

---

### T-10: Add State Schema Version Migration Rule [F-11]
**Severity**: MAJOR
**Compliance**: STRICT
**Depends on**: T-02, T-03
**Blocks**: None

#### Context
Current state has `"schema_version": 1`. The spec adds an `audit` block but doesn't specify schema version migration behavior. `read_state()` does no validation.

#### Instructions

**Step 1**: This is partially covered by T-02 (which adds schema version increment to SS6.1). Verify T-02 includes:
- `schema_version` increments from 1 to 2
- Loading v1 state in v2 code treats missing `audit` as `null`

**Step 2**: Add a dedicated migration subsection to SS6.1 (or nearby):

```markdown
#### State Schema Migration: v1 → v2

| Field | v1 behavior | v2 behavior |
|-------|-------------|-------------|
| `schema_version` | `1` | `2` |
| `audit` | Not present | Required (nullable) |
| `remediation_attempts` | Read by `_check_remediation_budget()` but NOT persisted by `_save_state()` (BUG) | Persisted by `_save_state()` (fixed in P0-D) |

**Migration rule**: When `read_state()` loads a file with `schema_version: 1`:
1. Set `audit = null` (not-yet-evaluated)
2. Set `remediation_attempts = 0` if not present
3. Continue execution — do not reject v1 state files
4. On next `_save_state()`, write `schema_version: 2` with all fields

**Invariant**: A missing `audit` block MUST NEVER be interpreted as `audit: passed`. It is always `null` (unknown/not-evaluated).
```

#### Acceptance Criteria
- [ ] v1→v2 migration table exists in SS6.1
- [ ] Migration rule for read_state() is specified
- [ ] Invariant: missing audit ≠ passed is stated
- [ ] remediation_attempts persistence fix is cross-referenced

---

## Phase 3: MINOR Corrections (Polish Before Implementation)

---

### T-11: Add New Symbol Index Appendix [F-12, F-13, F-14]
**Severity**: MINOR
**Compliance**: STANDARD (not blocking)
**Depends on**: T-01 through T-10
**Blocks**: None

#### Context
The spec's file-level change map (SS10.2) mixes `[NEW]` files with `[ADDITIVE]` changes to existing files. Symbols like `_step_traces`, `snapshot_pre_run()`, `SILENT_SUCCESS_SUSPECTED` are new additions to existing files but could be mistaken for existing code. Additionally, `--mock-llm` mode is an open decision that blocks G-012 CI integration, and the test migration strategy for `test_spec_patch_cycle.py` needs documentation.

#### Instructions

**Step 1**: Add a new appendix section at the end of the spec:

```markdown
## Appendix A: New Symbol Index

All symbols introduced by this spec, organized by target file.

### New Files (do not exist yet)
| File | Key Symbols | Phase |
|------|-------------|-------|
| `cli_portify/silent_success.py` | `FileSnapshot`, `StepTrace`, `SilentSuccessConfig`, `SilentSuccessDetector`, `SilentSuccessResult`, `SilentSuccessError` | P0-B |
| `cli_portify/smoke_gate.py` | `SmokeTestConfig`, `SmokeTestResult`, `run_smoke_test()`, `SMOKE_TEST_GATE`, `SMOKE_NOOP_CEILING_S`, `SMOKE_MIN_REAL_EXECUTION_S`, `SMOKE_TIMEOUT_S` | Phase 2 |
| `roadmap/fidelity_inventory.py` | `SpecInventory`, `build_spec_inventory()`, `_DISPATCH_TABLE_PATTERN`, `_STEP_DISPATCH_CALL`, `_DEP_ARROW_PATTERN` | P0-C |
| `tests/cli_portify/test_silent_success.py` | 7 test functions | P0-B |
| `tests/roadmap/test_fidelity_inventory.py` | 10 test functions | P0-C |
| `tests/cli_portify/test_smoke_gate.py` | 5 test functions | Phase 2 |
| `tests/fixtures/cli_portify/smoke/` | Smoke fixture directory | Phase 2 |

### New Symbols in Existing Files
| File | New Symbol | Type | Phase |
|------|-----------|------|-------|
| `pipeline/models.py` | `AuditWorkflowState` | enum | Phase 1 |
| `pipeline/models.py` | `AuditGateResult` | dataclass | Phase 1 |
| `pipeline/models.py` | `AuditLease` | dataclass | Phase 1 |
| `sprint/models.py` | profile enum (`strict\|standard\|legacy_migration`) | enum | Phase 1 |
| `cli_portify/models.py` | `PortifyOutcome.SILENT_SUCCESS_SUSPECTED` | enum value | P0-B |
| `cli_portify/models.py` | `PortifyOutcome.SUSPICIOUS_SUCCESS` | enum value | P0-B |
| `cli_portify/executor.py` | `_step_traces` | field | P0-B |
| `cli_portify/executor.py` | `_pipeline_start_time` | field | P0-B |
| `cli_portify/executor.py` | `snapshot_pre_run()` | method | P0-B |
| `cli_portify/gates.py` | `GATE_REGISTRY["smoke-test"]` | dict entry | Phase 2 |
| `roadmap/gates.py` | `_check_dispatch_tables_preserved()` | function | P0-C |
| `roadmap/gates.py` | `_check_dispatch_functions_preserved()` | function | P0-C |
| `roadmap/executor.py` | `audit` block in `_save_state()` | state block | Phase 3 |
| `tasklist/` | `audit_gate_required` field | field | Phase 1 |
```

**Step 2**: Add to open decisions (SS12.4 area or R21):
```markdown
> - **`--mock-llm` mode** (ELEVATED from open decision to Phase 1 prerequisite): G-012 smoke gate cannot be safely tested in CI without a `--mock-llm` mode. This mode must be specified and implemented before Phase 2 CI integration begins. Minimum spec: `--mock-llm` flag causes smoke gate to validate all non-LLM checks (artifact existence, content patterns, execution timing) while stubbing LLM API calls with deterministic test fixtures.
```

**Step 3**: Add to Phase 0 migration steps (cross-reference with T-01):
```markdown
> **Test migration note**: `tests/roadmap/test_spec_patch_cycle.py` is NOT deleted during migration. It is rewritten to test the deviation-analysis replacement path. The migrated test file must cover at minimum: qualifying file detection, resume-after-patch behavior, and spec hash validation — matching the existing test scope.
```

#### Acceptance Criteria
- [ ] Appendix A: New Symbol Index exists with both tables (new files, new symbols in existing files)
- [ ] --mock-llm is elevated from open decision to Phase 1 prerequisite
- [ ] Test migration note for test_spec_patch_cycle.py exists
- [ ] All 11 previously-nonexistent module references from Issue 4 are accounted for in the index

---

## Dependency Graph

```
T-01 (CRITICAL: migration rewrite)
 ├── T-02 (audit state schema)
 │    └── T-10 (schema migration)
 ├── T-03 (remediation_attempts fix)
 │    └── T-10 (schema migration)
 ├── T-04 (AuditGateResult location)
 ├── T-05 (G-012 registry clarification)
 │    └── T-09 (cross-domain dependency)
 ├── T-06 (guard boundary gaps)
 │    └── T-08 (lease acquisition modes)
 ├── T-07 (PortifyOutcome impact)
 └── T-11 (symbol index, --mock-llm, test migration)
```

## Execution Order (sc:task-unified --compliance strict)

```
Phase 1 (sequential, blocks all):
  T-01 → [Phase 2 unlocked]

Phase 2 (parallelizable after T-01):
  Wave A: T-02 ∥ T-03 ∥ T-05 ∥ T-06 ∥ T-07
  Wave B (after Wave A): T-04 ∥ T-08 ∥ T-09 ∥ T-10

Phase 3 (after Phase 2):
  T-11
```

## Verification Checklist (Post-Completion)

After all 11 tasks are complete, run this verification:

- [ ] `grep -c "retire.*_apply_resume" spec-refactor-plan-merged.md` returns 0
- [ ] `grep -c "remove.*_apply_resume" spec-refactor-plan-merged.md` returns 0
- [ ] `grep -c "migrate.*_apply_resume" spec-refactor-plan-merged.md` returns ≥2
- [ ] `grep "AuditGateResult" spec-refactor-plan-merged.md | grep "sprint/models.py"` returns 0 hits for placement (profile enum reference is OK)
- [ ] `grep "AuditGateResult" spec-refactor-plan-merged.md | grep "pipeline/models.py"` returns ≥1
- [ ] `grep "schema_version.*2" spec-refactor-plan-merged.md` returns ≥1
- [ ] `grep "abandoned lease" spec-refactor-plan-merged.md` returns ≥1
- [ ] Appendix A: New Symbol Index section exists
- [ ] All 7 boundary GAPs from the panel review have corresponding spec text
