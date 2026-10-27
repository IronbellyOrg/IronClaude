# Phase 1 -- Architecture Confirmation and Scope Lock

Confirm design assumptions before any code is written. Resolve open questions that materially affect interfaces and establish the architecture baseline. This phase is a gate: Phase 2 cannot begin until all 5 blocking OQs are resolved and framework base types are verified stable.

---

### T01.01 -- Validate Architecture Against SuperClaude CLI Framework

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | Prevent rework on contract-critical areas by confirming the cli_portify design aligns with the existing framework before any coding begins |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0001/spec.md`

**Deliverables:**
- Architecture decision notes confirming `src/superclaude/cli/cli_portify/` design aligns with existing framework

**Steps:**
1. **[PLANNING]** Load context from `src/superclaude/cli/` package structure and existing pipeline conventions
2. **[PLANNING]** Identify the key design decisions: sequential executor, domain model inheritance, gate enforcement layer
3. **[EXECUTION]** Confirm `cli_portify/` subpackage fits within the `src/superclaude/cli/` namespace without collision
4. **[EXECUTION]** Confirm CLI registration pattern from `src/superclaude/cli/main.py` is suitable for `cli_portify_group`
5. **[EXECUTION]** Document architectural baseline: package layout, import graph, framework coupling points
6. **[COMPLETION]** Write architecture decision notes to `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0001/spec.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0001/spec.md` exists with architectural baseline documented
- No unresolved structural conflicts between `cli_portify/` design and existing `cli/` package layout
- Registration pattern for `cli_portify_group` in `main.py` identified and documented
- Framework coupling points (base type imports, executor patterns) recorded

**Validation:**
- Manual check: architecture notes cover package layout, import strategy, and `main.py` registration pattern
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0001/spec.md` produced

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)

---

### T01.02 -- Verify Framework Base Type Import Stability (D-008)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | All domain models extend framework base types; if these types are unstable or at unexpected import paths, all Phase 3 domain model work will need rework |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0002/evidence.md`

**Deliverables:**
- Import verification report confirming stable locations for `PipelineConfig`, `Step`, `StepResult`, `GateCriteria`, `GateMode`, `SemanticCheck`

**Steps:**
1. **[PLANNING]** Identify expected import paths from roadmap: `superclaude.cli.pipeline.models` and `superclaude.cli.pipeline.process`
2. **[PLANNING]** Note that GateCriteria/GateMode/SemanticCheck live in `pipeline.models` NOT `sprint.models`
3. **[EXECUTION]** Run: `uv run python -c "from superclaude.cli.pipeline.models import PipelineConfig, Step, StepResult, GateCriteria, GateMode, SemanticCheck; print('OK')"`
4. **[EXECUTION]** Run: `uv run python -c "from superclaude.cli.pipeline.process import ClaudeProcess; print('OK')"`
5. **[EXECUTION]** Confirm `PortifyProcess` inherits from `ClaudeProcess` and thus gets `--tools default` from `build_command()`
6. **[COMPLETION]** Record confirmed import paths and inheritance chain in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0002/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0002/evidence.md` exists with all 6 import paths confirmed
- All 6 types (`PipelineConfig`, `Step`, `StepResult`, `GateCriteria`, `GateMode`, `SemanticCheck`) confirmed importable from `superclaude.cli.pipeline.models`
- `ClaudeProcess` confirmed importable from `superclaude.cli.pipeline.process`
- `--tools default` inheritance chain documented: `ClaudeProcess.build_command()` → `PortifyProcess.build_command()` via `super()`
- Current API interface contract for all 6 base types documented in D-0002 (key field names, signatures, inheritance hierarchy) confirming stability assumption

**Validation:**
- Manual check: all import commands exit 0 without error
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0002/evidence.md` produced

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** GateCriteria/GateMode/SemanticCheck are in `pipeline.models`, not `sprint.models` — confirmed by pre-resume verification (oq-resolutions.md D-008)

---

### T01.03 -- Resolve 5 Blocking Open Questions (OQ-001, OQ-003, OQ-004, OQ-009, OQ-011)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | These 5 OQs affect contract-critical interfaces; resolving them before Phase 2 coding prevents mid-implementation rework on executor, models, and error handling |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0003/spec.md`

**Deliverables:**
- OQ resolution list with blocking/non-blocking classification for all 14 OQs; all 5 blocking OQs resolved

**Steps:**
1. **[PLANNING]** List all 5 blocking OQs: OQ-001 (TurnLedger semantics), OQ-003 (phase_contracts schema), OQ-004 (api_snapshot_hash algorithm), OQ-009 (failure_type enum values), OQ-011 (--debug flag behavior)
2. **[PLANNING]** Note OQ-008 (--file) and OQ-013 (PASS_NO_SIGNAL) are already CLOSED per oq-resolutions.md
3. **[EXECUTION]** Resolve OQ-001: define "one turn" as one complete Claude subprocess invocation (input prompt → output completion)
4. **[EXECUTION]** Resolve OQ-003: define `phase_contracts` schema as mapping of phase_type → list of required artifact paths
5. **[EXECUTION]** Resolve OQ-004: define `api_snapshot_hash` as SHA-256 of sorted serialized interface contract fields
6. **[EXECUTION]** Resolve OQ-009: define `failure_type` enum as `NAME_COLLISION | OUTPUT_NOT_WRITABLE | AMBIGUOUS_PATH | INVALID_PATH | DERIVATION_FAILED`
   - Note: `CONTENT_TOO_LARGE` is NOT part of Phase 1's 5-error spec. It is added in Phase 7 (T07.04) as a Phase 6 amendment for the release-spec synthesis embed guard.
7. **[EXECUTION]** Resolve OQ-011: `--debug` enables verbose subprocess output capture and writes raw stdout/stderr to execution log
8. **[COMPLETION]** Write full OQ resolution list to `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0003/spec.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0003/spec.md` exists with all 14 OQs classified
- All 5 blocking OQs (OQ-001, OQ-003, OQ-004, OQ-009, OQ-011) have explicit resolutions recorded
- OQ-008 and OQ-013 marked CLOSED with reference to `oq-resolutions.md`
- No blocking unknown remains that would prevent Phase 2 implementation

**Validation:**
- Manual check: each of the 5 blocking OQs has a one-sentence actionable resolution
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0003/spec.md` produced

**Dependencies:** T01.02 (framework base types must be confirmed before OQ-001 TurnLedger semantics can be finalized)
**Rollback:** TBD (if not specified in roadmap)

---

### T01.04 -- Assess OQ-002 and OQ-013 as Potential Phase 2 Blockers

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | OQ-002 (kill signal SIGTERM→SIGKILL) and OQ-013 (PASS_NO_SIGNAL retry) affect executor and process.py in Phase 3; early assessment prevents late-phase surprises |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0004/spec.md`

**Deliverables:**
- Blocker assessment for OQ-002 and OQ-013 with blocking/non-blocking determination

**Steps:**
1. **[PLANNING]** Review OQ-013 resolution already in `oq-resolutions.md`: PASS_NO_SIGNAL → retry; PASS_NO_REPORT → no retry
2. **[EXECUTION]** Classify OQ-013 as NON-BLOCKING: resolution is documented; T03.08 (`_determine_status()`) implements it (output Phase 3 = roadmap Phase 2)
3. **[EXECUTION]** Assess OQ-002 (SIGTERM grace period then SIGKILL): determine whether to use `os.kill(pid, SIGTERM)` + wait(5s) + `os.kill(pid, SIGKILL)` or direct SIGKILL. Choose SIGTERM→wait(5s)→SIGKILL as reversible pattern
4. **[EXECUTION]** Classify OQ-002 as NON-BLOCKING: resolution chosen (SIGTERM grace period)
5. **[COMPLETION]** Write assessment to `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0004/spec.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0004/spec.md` exists with blocker classification for OQ-002 and OQ-013
- OQ-013 classified NON-BLOCKING with reference to `oq-resolutions.md`
- OQ-002 classified NON-BLOCKING with chosen signal pattern documented (SIGTERM→5s→SIGKILL)
- Output Phase 3 (= roadmap Phase 2) executor implementation notes updated with these decisions

**Validation:**
- Manual check: both OQs have explicit blocking/non-blocking determination and rationale
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0004/spec.md` produced

**Dependencies:** T01.03
**Rollback:** TBD (if not specified in roadmap)

---

### T01.05 -- Confirm Prompt Splitting Threshold Location

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Prompt splitting at 300 lines must be implemented in one consistent location; choosing wrong location risks duplication or missed splitting |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0005/spec.md`

**Deliverables:**
- Prompt split threshold decision: location (executor or prompt builder) and 300-line threshold confirmed

**Steps:**
1. **[PLANNING]** Review roadmap Phase 9 FR-050/AC-010: "if aggregate prompt length exceeds 300 lines, split to portify-prompts.md"
2. **[EXECUTION]** Determine location: prompt builder (`prompts.py`) is correct — it produces the prompt string; executor only invokes. Splitting in the prompt builder keeps the executor clean
3. **[EXECUTION]** Confirm 300-line threshold applies to the aggregate prompt (all sections combined), not individual sections
4. **[COMPLETION]** Write decision to `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0005/spec.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0005/spec.md` exists with threshold decision
- Location confirmed as `prompts.py` prompt builder
- 300-line aggregate threshold confirmed
- Split output path (`portify-prompts.md`) confirmed

**Validation:**
- Manual check: decision document specifies location, threshold, and output path
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0005/spec.md` produced

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)

---

### T01.06 -- Document Module Overwrite Rules (Generated by / Portified from Markers)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Overwrite rules prevent accidental destruction of hand-written modules; the marker check in `__init__.py` must be defined before Phase 2 collision detection implements it |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0006/spec.md`

**Deliverables:**
- Overwrite rules documentation: exact marker strings, location (`__init__.py` first 10 lines), and allowed-overwrite logic

**Steps:**
1. **[PLANNING]** Review roadmap AC-013: `__init__.py` must contain `Generated by` / `Portified from` marker
2. **[EXECUTION]** Define marker strings: `# Generated by superclaude cli-portify` and `# Portified from <workflow_name>`
3. **[EXECUTION]** Define overwrite rule: scan `src/superclaude/cli/<module_name>/__init__.py` first 10 lines for either marker; if found → allow overwrite; if absent → raise `NAME_COLLISION`
4. **[COMPLETION]** Write overwrite rules to `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0006/spec.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0006/spec.md` exists with exact marker strings defined
- Overwrite logic (scan first 10 lines of `__init__.py`) documented
- `NAME_COLLISION` error path for non-portified modules documented
- Marker placement in generated `__init__.py` (first 2 lines) specified

**Validation:**
- Manual check: overwrite rule is unambiguous and implementable by T02.03
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0006/spec.md` produced

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)

---

### T01.07 -- Document Non-Blocking OQs (OQ-007, OQ-014)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | OQ-007 (agent discovery warning) and OQ-014 (workdir cleanup) must be documented as non-blocking so their respective phases can proceed without waiting for resolution |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0007/spec.md`

**Deliverables:**
- Non-blocking OQ documentation for OQ-007 and OQ-014 with phase assignments

**Steps:**
1. **[PLANNING]** Review OQ-007: agent discovery warning behavior — affects Phase 2 `inventory.py`
2. **[PLANNING]** Review OQ-014: workdir cleanup policy — affects Phase 9 observability
3. **[EXECUTION]** Document OQ-007 as non-blocking: emit `warnings.warn()` for missing agent files; do not suppress silently; Phase 2 implements this
4. **[EXECUTION]** Document OQ-014 as non-blocking: workdir retained after run; cleanup is manual or explicit `--clean` flag (future); Phase 9 documents cleanup expectations
5. **[COMPLETION]** Write to `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0007/spec.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0007/spec.md` exists with OQ-007 and OQ-014 documented
- OQ-007 assigned to Phase 2 with `warnings.warn()` behavior specified
- OQ-014 assigned to output Phase 9 (= roadmap Phase 8 observability completion) with retention-by-default policy specified
- Both classified as NON-BLOCKING with rationale

**Validation:**
- Manual check: both OQs have phase assignment and default behavior documented
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0007/spec.md` produced

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)

---

### Checkpoint: End of Phase 1

**Purpose:** Verify all architecture confirmation tasks are complete and no blocking unknowns remain before Phase 2 implementation begins.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P01-END.md`

**Verification:**
- All 7 Phase 1 artifacts exist under `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0001/` through `D-0007/`
- All 5 blocking OQs (OQ-001, OQ-003, OQ-004, OQ-009, OQ-011) have explicit resolutions in D-0003
- Framework base types confirmed importable from `superclaude.cli.pipeline.models` (D-0002 evidence)

**Exit Criteria:**
- Architecture decision notes (D-0001) approved as baseline for Phase 2 implementation
- Zero blocking unknowns remain per D-0003 OQ resolution list
- Module overwrite rules (D-0006) are unambiguous and ready for T02.03 implementation
