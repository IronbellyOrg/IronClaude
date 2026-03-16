# Phase 3 -- New Pipeline Steps and Prompts

Implement the two new steps (`annotate-deviations`, `deviation-analysis`) with their prompts, step definitions, artifact output contracts, and the remediation module updates. This phase adds `build_annotate_deviations_prompt()` and `build_deviation_analysis_prompt()` to `prompts.py`, wires both steps into `executor.py`, and implements `deviations_to_findings()` in `remediate.py`.

### T03.01 -- Implement build_annotate_deviations_prompt() in prompts.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | Prompt builder for annotate-deviations step; must enforce anti-laundering rules with D-XX + round citation requirements |
| Effort | L |
| Risk | Medium |
| Risk Drivers | Security (anti-laundering), system-wide (pipeline prompt) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0018/spec.md`

**Deliverables:**
1. `build_annotate_deviations_prompt()` function in `prompts.py` with inputs (`spec_file`, `roadmap.md`, `debate-transcript.md`, `diff-analysis.md`), classification taxonomy (INTENTIONAL_IMPROVEMENT, INTENTIONAL_PREFERENCE, SCOPE_ADDITION, NOT_DISCUSSED), anti-laundering rules, and output contract for `spec-deviations.md` with `schema_version: "2.25"` first

**Steps:**
1. **[PLANNING]** Review existing prompt builder pattern in `prompts.py`
2. **[PLANNING]** Review FR-005 through FR-012 requirements for prompt content and output contract
3. **[EXECUTION]** Implement `build_annotate_deviations_prompt()` with correct input parameters
4. **[EXECUTION]** Include classification taxonomy (FR-006): INTENTIONAL_IMPROVEMENT, INTENTIONAL_PREFERENCE, SCOPE_ADDITION, NOT_DISCUSSED
5. **[EXECUTION]** Include anti-laundering rules: INTENTIONAL_IMPROVEMENT requires D-XX + round citation (FR-007, FR-008, FR-009, FR-010); missing citation defaults to NOT_DISCUSSED
6. **[EXECUTION]** Define output contract for `spec-deviations.md` with YAML frontmatter (FR-011) and body format (FR-012), `schema_version: "2.25"` as first frontmatter field (NFR-023)
7. **[VERIFICATION]** Review prompt text for unambiguous anti-laundering wording; verify output contract matches spec
8. **[COMPLETION]** Document prompt structure in `D-0018/spec.md`

**Acceptance Criteria:**
- `build_annotate_deviations_prompt()` exists in `prompts.py` with 4 required input parameters
- Prompt text contains all 4 classification taxonomy values
- Anti-laundering rules explicitly state: architectural-quality inference is not proof of intentionality; missing citation defaults to NOT_DISCUSSED
- Output contract specifies complete YAML frontmatter per FR-011, with `schema_version: "2.25"` as first field, and body format per FR-012

**Validation:**
- Manual check: Prompt text reviewed for anti-laundering completeness and output contract accuracy
- Evidence: linkable artifact produced at `D-0018/spec.md`

**Dependencies:** T02.08 (Phase 2 exit)
**Rollback:** Remove function from `prompts.py`

---

### T03.02 -- Implement build_deviation_analysis_prompt() in prompts.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | Prompt builder for deviation-analysis step; produces routing table and blast radius analysis for classified deviations |
| Effort | L |
| Risk | Medium |
| Risk Drivers | System-wide (pipeline prompt), multi-file |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0019/spec.md`

**Deliverables:**
1. `build_deviation_analysis_prompt()` function in `prompts.py` with 6 inputs, classification taxonomy (PRE_APPROVED, INTENTIONAL, SLIP, AMBIGUOUS), routing table output (fix_roadmap, update_spec, no_action, human_review), blast radius analysis, routing_intent sub-field, Spec Update Recommendations subsection, flat routing fields with comma-separated DEV-\d+ IDs, and `schema_version: "2.25"` first

**Steps:**
1. **[PLANNING]** Review FR-021 through FR-025, FR-045, FR-073, FR-078, FR-087, FR-090 requirements
2. **[PLANNING]** Review existing prompt builder pattern for consistency
3. **[EXECUTION]** Implement `build_deviation_analysis_prompt()` with 6 inputs: `spec-fidelity.md`, `debate-transcript.md`, `diff-analysis.md`, `spec-deviations.md`, `roadmap-A.md`, `roadmap-B.md`
4. **[EXECUTION]** Include classification taxonomy (FR-021), normative classification mapping table (FR-078), routing table output (FR-022), blast radius analysis (FR-023)
5. **[EXECUTION]** Include `routing_intent` sub-field (`superior` | `preference`) for INTENTIONAL deviations (FR-090)
6. **[EXECUTION]** Include `## Spec Update Recommendations` subsection for `update_spec` routed deviations (FR-087)
7. **[EXECUTION]** Define output contract for `deviation-analysis.md` with flat routing fields using comma-separated DEV-\d+ IDs (FR-045, FR-073), `schema_version: "2.25"` first (NFR-023)
8. **[VERIFICATION]** Review prompt for routing table completeness and schema compliance
9. **[COMPLETION]** Document prompt structure in `D-0019/spec.md`

**Acceptance Criteria:**
- `build_deviation_analysis_prompt()` exists in `prompts.py` with 6 required input parameters
- Prompt includes normative classification mapping table from spec section 5.3a
- Output contract specifies flat routing fields with comma-separated DEV-\d+ IDs
- Output contract specifies YAML frontmatter per FR-024 and body format per FR-025
- `schema_version: "2.25"` specified as first frontmatter field in output contract
- Prompt includes `routing_intent` sub-field (`superior` | `preference`) for INTENTIONAL deviations (FR-090)
- Prompt includes `## Spec Update Recommendations` subsection requirement for `update_spec` routed deviations (FR-087)
- Prompt requires blast radius analysis for each INTENTIONAL deviation (FR-023)

**Validation:**
- Manual check: Prompt text reviewed for routing table completeness and blast radius requirement
- Evidence: linkable artifact produced at `D-0019/spec.md`

**Dependencies:** T03.01 (prompt pattern established)
**Rollback:** Remove function from `prompts.py`

---

### T03.03 -- Modify build_spec_fidelity_prompt() for Deviation Awareness

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | Existing spec-fidelity prompt must accept spec_deviations_path and adjust behavior: verify citations, exclude verified INTENTIONAL, report invalid as HIGH |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Breaking change (modified existing function signature) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0020/spec.md`

**Deliverables:**
1. Modified `build_spec_fidelity_prompt()` in `prompts.py` with added `spec_deviations_path: Path | None = None` parameter (FR-016) and deviation-aware prompt instructions (FR-017)

**Steps:**
1. **[PLANNING]** Read current `build_spec_fidelity_prompt()` signature and body
2. **[PLANNING]** Review FR-016 and FR-017 requirements
3. **[EXECUTION]** Add `spec_deviations_path: Path | None = None` parameter
4. **[EXECUTION]** When provided: add instructions to VERIFY citations, EXCLUDE verified INTENTIONAL_IMPROVEMENT, REPORT invalid annotations as HIGH, ANALYZE NOT_DISCUSSED independently
5. **[VERIFICATION]** Confirm backward compatibility: existing callers without the new parameter still work
6. **[VERIFICATION]** Review prompt instructions for completeness against FR-017
7. **[COMPLETION]** Document modifications in `D-0020/spec.md`

**Acceptance Criteria:**
- `build_spec_fidelity_prompt()` accepts optional `spec_deviations_path` parameter
- When `spec_deviations_path` is provided, prompt includes citation verification and INTENTIONAL exclusion instructions
- When `spec_deviations_path` is None, behavior is unchanged from v2.24
- Prompt explicitly instructs: REPORT invalid annotations as HIGH severity
- When `spec_deviations_path` is provided, prompt includes instruction to ANALYZE NOT_DISCUSSED deviations independently

**Validation:**
- `uv run pytest tests/sprint/ -v -k "fidelity_prompt"` exits 0 if prompt tests exist
- Evidence: linkable artifact produced at `D-0020/spec.md`

**Dependencies:** T03.01 (prompt pattern)
**Rollback:** Remove `spec_deviations_path` parameter and conditional instructions

---

### T03.04 -- Wire annotate-deviations Step in executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043, R-046 |
| Why | annotate-deviations step must be placed between merge and test-strategy in _build_steps(); spec-deviations.md must be passed to spec-fidelity step |
| Effort | M |
| Risk | High |
| Risk Drivers | Pipeline step ordering, system-wide, multi-file |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0021/spec.md`

**Deliverables:**
1. `annotate-deviations` step added to `_build_steps()` in `executor.py` between merge and test-strategy (FR-004), with inputs, output `spec-deviations.md`, gate `ANNOTATE_DEVIATIONS_GATE` (STANDARD, timeout 300s, retry_limit=0), and `spec-deviations.md` passed as additional input to spec-fidelity step (FR-018)

**Steps:**
1. **[PLANNING]** Read `_build_steps()` in `executor.py` to understand current step ordering
2. **[PLANNING]** Identify merge and test-strategy step positions for insertion point
3. **[EXECUTION]** Add `annotate-deviations` step with inputs: `spec_file`, `roadmap.md`, `debate-transcript.md`, `diff-analysis.md`
4. **[EXECUTION]** Set output: `spec-deviations.md`, gate: `ANNOTATE_DEVIATIONS_GATE`, timeout: 300s, retry_limit: 0
5. **[EXECUTION]** Pass `spec-deviations.md` as additional input to `spec-fidelity` step (FR-018)
6. **[VERIFICATION]** Verify step ordering: annotate-deviations appears between merge and test-strategy
7. **[COMPLETION]** Document step wiring in `D-0021/spec.md`

**Acceptance Criteria:**
- `annotate-deviations` step exists in `_build_steps()` between merge and test-strategy
- Step inputs: `spec_file`, `roadmap.md`, `debate-transcript.md`, `diff-analysis.md`
- Step output: `spec-deviations.md` with `ANNOTATE_DEVIATIONS_GATE` (STANDARD), timeout 300s, retry_limit=0
- `spec-fidelity` step receives `spec-deviations.md` as additional input

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "step"` exits 0
- Evidence: linkable artifact produced at `D-0021/spec.md`

**Dependencies:** T02.05 (ANNOTATE_DEVIATIONS_GATE defined), T03.01 (prompt builder exists)
**Rollback:** Remove step from `_build_steps()`; revert spec-fidelity input change

---

### Checkpoint: Phase 3 / Tasks 1-5

**Purpose:** Verify all prompt builders are implemented and annotate-deviations step is wired into the pipeline.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P03-T01-T05.md`
**Verification:**
- All 3 prompt functions exist in `prompts.py` with correct signatures
- `annotate-deviations` step wired between merge and test-strategy
- `spec-deviations.md` passed as input to spec-fidelity step
**Exit Criteria:**
- D-0018 through D-0021 artifacts exist and are non-empty
- No import errors or missing function references
- Pipeline step order confirmed via test or manual inspection

---

### T03.05 -- Wire deviation-analysis Step in executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-044 |
| Why | deviation-analysis step must be placed after spec-fidelity in _build_steps() with STRICT gate and 6 inputs |
| Effort | M |
| Risk | High |
| Risk Drivers | Pipeline step ordering, system-wide |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0022/spec.md`

**Deliverables:**
1. `deviation-analysis` step added to `_build_steps()` in `executor.py` after spec-fidelity (FR-020), with 6 inputs, output `deviation-analysis.md`, gate `DEVIATION_ANALYSIS_GATE` (STRICT, timeout 300s, retry_limit=1)

**Steps:**
1. **[PLANNING]** Confirm spec-fidelity step position in `_build_steps()`
2. **[PLANNING]** Review 6 required inputs from roadmap
3. **[EXECUTION]** Add `deviation-analysis` step after spec-fidelity
4. **[EXECUTION]** Set inputs: `spec-fidelity.md`, `debate-transcript.md`, `diff-analysis.md`, `spec-deviations.md`, `roadmap-A.md`, `roadmap-B.md`
5. **[EXECUTION]** Set output: `deviation-analysis.md`, gate: `DEVIATION_ANALYSIS_GATE`, timeout: 300s, retry_limit: 1
6. **[VERIFICATION]** Verify step ordering: deviation-analysis appears after spec-fidelity
7. **[COMPLETION]** Document step wiring in `D-0022/spec.md`

**Acceptance Criteria:**
- `deviation-analysis` step exists in `_build_steps()` after spec-fidelity
- Step has 6 inputs: `spec-fidelity.md`, `debate-transcript.md`, `diff-analysis.md`, `spec-deviations.md`, `roadmap-A.md`, `roadmap-B.md`
- Step output: `deviation-analysis.md` with `DEVIATION_ANALYSIS_GATE` (STRICT), timeout 300s, retry_limit=1
- `uv run pytest tests/sprint/test_executor.py -v -k "step"` exits 0

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "step"` exits 0
- Evidence: linkable artifact produced at `D-0022/spec.md`

**Dependencies:** T03.04 (annotate-deviations step must be wired first), T02.05 (DEVIATION_ANALYSIS_GATE defined)
**Rollback:** Remove step from `_build_steps()`

---

### T03.06 -- Update _get_all_step_ids() for 13-Step Pipeline Order

| Field | Value |
|---|---|
| Roadmap Item IDs | R-045 |
| Why | Step ID registry must reflect the new 13-step pipeline order including both new steps (FR-038) |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Pipeline ordering, system-wide |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0023/evidence.md`

**Deliverables:**
1. Updated `_get_all_step_ids()` in `executor.py` returning 13 steps in correct pipeline order including `annotate-deviations` and `deviation-analysis`

**Steps:**
1. **[PLANNING]** Read current `_get_all_step_ids()` to see existing step list
2. **[PLANNING]** Determine correct 13-step order from roadmap
3. **[EXECUTION]** Add `annotate-deviations` and `deviation-analysis` to step ID list in correct positions
4. **[EXECUTION]** Verify list contains exactly 13 entries
5. **[VERIFICATION]** `_get_all_step_ids()` returns exactly 13 steps in correct order
6. **[COMPLETION]** Document step order in `D-0023/evidence.md`

**Acceptance Criteria:**
- `_get_all_step_ids()` returns exactly 13 step IDs
- `annotate-deviations` appears between merge and test-strategy
- `deviation-analysis` appears after spec-fidelity
- `uv run pytest tests/sprint/test_executor.py -v -k "step_ids"` exits 0

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "step_ids"` exits 0
- Evidence: linkable artifact produced at `D-0023/evidence.md`

**Dependencies:** T03.04, T03.05 (both steps must be wired)
**Rollback:** Remove new step IDs from the list

---

### T03.07 -- Implement roadmap_hash Injection With Atomic Writes

| Field | Value |
|---|---|
| Roadmap Item IDs | R-047, R-048 |
| Why | FR-055: SHA-256 of roadmap.md must be injected into spec-deviations.md frontmatter after annotate-deviations completes; NFR-022: atomic write pattern required |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Security (hash integrity), data (atomic writes) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0024/spec.md`

**Deliverables:**
1. `roadmap_hash` injection logic in `executor.py`: SHA-256 of `roadmap.md` computed and injected into `spec-deviations.md` frontmatter after annotate-deviations subprocess completes, using atomic write (`.tmp` + `os.replace()`)
2. Recording of `started_at`, `completed_at`, `token_count` (best-effort) for new steps in `_save_state()` (NFR-024)

**Steps:**
1. **[PLANNING]** Review `roadmap_run_step()` interface for post-step hook injection point (from T01.03)
2. **[PLANNING]** Review atomic write pattern: `.tmp` + `os.replace()`
3. **[EXECUTION]** Compute SHA-256 of `roadmap.md` at injection time using `hashlib.sha256`
4. **[EXECUTION]** Inject `roadmap_hash` into `spec-deviations.md` frontmatter using atomic write
5. **[EXECUTION]** Add `started_at`, `completed_at`, `token_count` recording for new steps in `_save_state()`
6. **[VERIFICATION]** Verify atomic write: `.tmp` file created then `os.replace()` called
7. **[VERIFICATION]** Verify `roadmap_hash` matches independent SHA-256 computation
8. **[COMPLETION]** Document implementation in `D-0024/spec.md`

**Acceptance Criteria:**
- `roadmap_hash` field present in `spec-deviations.md` frontmatter after annotate-deviations step
- Hash value matches `hashlib.sha256(roadmap_content).hexdigest()`
- Write uses atomic pattern: `.tmp` file + `os.replace()` (no partial writes possible)
- `started_at`, `completed_at` recorded for new steps; `token_count` best-effort

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "hash"` exits 0
- Evidence: linkable artifact produced at `D-0024/spec.md`

**Dependencies:** T03.04 (annotate-deviations step must be wired)
**Rollback:** Remove hash injection logic and state recording additions

---

### T03.08 -- Implement Graceful Degradation and CLI Routing Output

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049, R-050 |
| Why | FR-089: total_annotated=0 must not halt pipeline; FR-087: routing_update_spec summary must appear in CLI output when non-empty |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0025/evidence.md`

**Deliverables:**
1. Graceful degradation in `executor.py`: `total_annotated: 0` logs INFO and continues pipeline (FR-089); `routing_update_spec` summary printed in CLI output when non-empty (FR-087)

**Steps:**
1. **[PLANNING]** Identify where annotate-deviations result is processed in executor
2. **[PLANNING]** Review FR-089 and FR-087 requirements
3. **[EXECUTION]** Add check for `total_annotated: 0`: log INFO explaining deviation-analysis will act as backstop; continue pipeline
4. **[EXECUTION]** Add `routing_update_spec` summary print to CLI output when non-empty (explicit behavior, not side-effect)
5. **[VERIFICATION]** Test: `total_annotated: 0` produces INFO log and pipeline continues
6. **[VERIFICATION]** Test: non-empty `routing_update_spec` appears in CLI output
7. **[COMPLETION]** Document behavior in `D-0025/evidence.md`

**Acceptance Criteria:**
- `total_annotated: 0` produces INFO-level log message and pipeline continues without halt
- INFO message explains that `deviation-analysis` will act as backstop
- Non-empty `routing_update_spec` is printed to CLI output
- Empty `routing_update_spec` produces no CLI output for that field

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "graceful or routing"` exits 0
- Evidence: linkable artifact produced at `D-0025/evidence.md`

**Dependencies:** T03.04 (annotate-deviations step wired)
**Rollback:** Remove graceful degradation check and CLI output logic

---

### T03.09 -- Implement deviations_to_findings() in remediate.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-051 |
| Why | FR-033: converts classified deviations into Finding objects; only produces findings for fix_roadmap routed deviations |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Data (routing conversion), schema (Finding objects) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0026 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0026/spec.md`

**Deliverables:**
1. `deviations_to_findings()` function in `remediate.py`: converts classified deviations to `Finding` objects, only for `fix_roadmap` routed deviations (FR-035), with severity mapping HIGH->BLOCKING, MEDIUM->WARNING, LOW->INFO (FR-034), `ValueError` if routing empty but `slip_count > 0` (FR-058), WARNING log when routing ID not found in fidelity table (FR-082)

**Steps:**
1. **[PLANNING]** Review `Finding` dataclass constructor from T02.01
2. **[PLANNING]** Review FR-033 through FR-035, FR-058, FR-082 requirements
3. **[EXECUTION]** Implement `deviations_to_findings()`: iterate deviation classifications, filter for `fix_roadmap` routing
4. **[EXECUTION]** Implement severity mapping: HIGH->BLOCKING, MEDIUM->WARNING, LOW->INFO
5. **[EXECUTION]** Add defense-in-depth: `ValueError` if routing is empty but `slip_count > 0`
6. **[EXECUTION]** Add WARNING log when routing ID not found in fidelity table
7. **[VERIFICATION]** Run unit tests for all severity mappings, empty routing with slips, missing routing IDs
8. **[COMPLETION]** Document implementation in `D-0026/spec.md`

**Acceptance Criteria:**
- `deviations_to_findings()` produces `Finding` objects only for `fix_roadmap` routed deviations
- Severity mapping: HIGH->BLOCKING, MEDIUM->WARNING, LOW->INFO verified
- `ValueError` raised when routing is empty but `slip_count > 0`
- WARNING logged when routing ID not found in fidelity table

**Validation:**
- `uv run pytest tests/sprint/test_remediate.py -v -k "deviations_to_findings"` exits 0
- Evidence: linkable artifact produced at `D-0026/spec.md`

**Dependencies:** T02.01 (Finding with deviation_class)
**Rollback:** Remove `deviations_to_findings()` from `remediate.py`

---

### Checkpoint: Phase 3 / Tasks 6-10

**Purpose:** Verify pipeline step ordering complete, hash injection working, and remediation conversion implemented.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P03-T06-T10.md`
**Verification:**
- `_get_all_step_ids()` returns exactly 13 steps in correct order
- `roadmap_hash` injection uses atomic write pattern
- `deviations_to_findings()` passes all severity mapping tests
**Exit Criteria:**
- D-0022 through D-0026 artifacts exist and are non-empty
- `uv run pytest tests/sprint/test_executor.py tests/sprint/test_remediate.py -v` exits 0
- No pipeline step ordering issues detected

---

### T03.10 -- Update Remediation Step Input and Prompt

| Field | Value |
|---|---|
| Roadmap Item IDs | R-052, R-053 |
| Why | Remediation step must use deviation-analysis.md routing table as primary input; prompt must instruct fix only SLIPs, prohibit modification of INTENTIONAL and PRE_APPROVED |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Security (INTENTIONAL/PRE_APPROVED protection), system-wide |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0027 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0027/spec.md`

**Deliverables:**
1. Updated remediation step in `remediate.py` using `deviation-analysis.md` routing table as primary input (FR-036)
2. Updated remediation prompt in `remediate_prompts.py` with deviation-class awareness: fix only SLIPs, explicitly prohibit modification of INTENTIONAL and PRE_APPROVED items (FR-037)

**Steps:**
1. **[PLANNING]** Read current remediation step input configuration
2. **[PLANNING]** Read current remediation prompt in `remediate_prompts.py`
3. **[EXECUTION]** Update remediation step to use `deviation-analysis.md` routing table as primary input
4. **[EXECUTION]** Update remediation prompt: instruct agent to fix only SLIPs
5. **[EXECUTION]** Add explicit prohibition: do not modify INTENTIONAL and PRE_APPROVED items
6. **[VERIFICATION]** Review prompt for explicit SLIP-only instructions and prohibition wording
7. **[COMPLETION]** Document modifications in `D-0027/spec.md`

**Acceptance Criteria:**
- Remediation step uses `deviation-analysis.md` routing table as primary input source
- Remediation prompt explicitly instructs: fix only SLIP-classified deviations
- Prompt explicitly prohibits: modification of INTENTIONAL and PRE_APPROVED items
- `uv run pytest tests/sprint/ -v -k "remediat"` exits 0

**Validation:**
- Manual check: Remediation prompt contains SLIP-only and INTENTIONAL/PRE_APPROVED prohibition instructions
- Evidence: linkable artifact produced at `D-0027/spec.md`

**Dependencies:** T03.09 (deviations_to_findings available)
**Rollback:** Revert input source and prompt changes

---

### T03.11 -- Validate Phase 3 Exit Criteria

| Field | Value |
|---|---|
| Roadmap Item IDs | R-054 |
| Why | Gate check: all Phase 2 (roadmap) exit criteria verified before proceeding to Phase 4 |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0028/evidence.md`

**Deliverables:**
1. Phase 3 exit criteria checklist with all 9 criteria verified

**Steps:**
1. **[PLANNING]** Load Phase 2 (roadmap) exit criteria from roadmap (9 checkboxes)
2. **[PLANNING]** Gather test results and artifact evidence from T03.01-T03.10
3. **[EXECUTION]** Verify each of the 9 exit criteria with specific test output or artifact reference
4. **[EXECUTION]** Confirm FR-089 graceful degradation tested
5. **[EXECUTION]** Confirm FR-087 CLI output tested
6. **[VERIFICATION]** Run `uv run pytest tests/sprint/ -v` to confirm full test suite passes
7. **[COMPLETION]** Write exit criteria verification to `D-0028/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0028/evidence.md` exists with all 9 exit criteria checked
- Pipeline step order matches FR-002 exactly
- `_get_all_step_ids()` returns 13 steps in correct order
- Integration tests for `deviations_to_findings()` sequenced after Phase 4 (tasklist) / Phase 3 (roadmap) completes budget mechanism; may be scaffolded now, completed in Phase 4 (tasklist)

**Validation:**
- `uv run pytest tests/sprint/ -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0028/evidence.md`

**Dependencies:** T03.10
**Rollback:** TBD (validation task; no code changes)

---

### Checkpoint: End of Phase 3

**Purpose:** Confirm all pipeline steps, prompts, and remediation updates are complete; Phase 4 (Resume/Recovery) can begin.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P03-END.md`
**Verification:**
- Both prompt builders produce well-formed output contracts
- Pipeline step order matches FR-002 exactly with 13 steps
- `deviations_to_findings()` unit tests pass for all severity mappings
**Exit Criteria:**
- `uv run pytest tests/sprint/ -v` exits 0 with no regressions
- All 9 Phase 2 (roadmap) exit criteria verified in D-0028
- D-0018 through D-0028 artifacts exist and are non-empty
