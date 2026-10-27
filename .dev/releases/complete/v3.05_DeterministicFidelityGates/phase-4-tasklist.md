# Phase 4 -- Semantic Layer & Adversarial Debate

Implement the residual semantic layer for judgment-dependent checks and the adversarial debate protocol for HIGH severity validation. Validate run-to-run memory integration end-to-end. The semantic layer must be validated before the convergence engine consumes its outputs (debate-resolved architectural ordering).

### T04.01 -- Extend semantic_layer.py with Dimension Filtering and Chunked Input (FR-4)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Semantic layer must only process dimensions not covered by structural checkers and use chunked input to avoid attention degradation. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | cross-cutting (feeds convergence engine), dependency (requires structural findings as context) |
| Tier | STRICT |
| Confidence | [████████░░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0022/spec.md`

**Deliverables:**
1. Extended `semantic_layer.py` implementing `run_semantic_layer()` entry point: receives only non-structural dimensions, uses per-section chunked input, includes structural findings as prompt context, tags all findings with `source_layer="semantic"`, prior findings from registry memory included in prompt

**Steps:**
1. **[PLANNING]** Review existing `semantic_layer.py` (337 lines) and identify extension points
2. **[PLANNING]** Define which dimensions/aspects are NOT covered by structural checkers (residual set)
3. **[EXECUTION]** Implement `run_semantic_layer()` entry point with dimension filtering
4. **[EXECUTION]** Implement chunked input: per-section prompt construction, structural findings as context
5. **[EXECUTION]** Tag all semantic findings with `source_layer="semantic"`; include prior findings from registry
6. **[VERIFICATION]** Verify semantic layer only processes non-structural dimensions; no re-checking of structural findings
7. **[COMPLETION]** Document semantic layer extension in `TASKLIST_ROOT/artifacts/D-0022/spec.md`

**Acceptance Criteria:**
- `run_semantic_layer()` receives only dimensions/aspects not covered by structural checkers
- Semantic layer uses per-section chunked input (not full-document inline)
- Structural findings passed as context in prompt to prevent re-reporting
- All semantic findings tagged with `source_layer="semantic"`

**Validation:**
- `uv run pytest tests/roadmap/test_semantic_layer.py -v -k "dimension_filtering or chunked"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0022/spec.md` documents semantic layer extension

**Dependencies:** T02.02, T02.03, T03.03
**Rollback:** TBD

---

### T04.02 -- Implement Prompt Budget Enforcement (FR-4.2)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | NFR-3 requires no prompt >30KB. Budget allocation prevents attention degradation on large specs. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance (prompt size affects LLM quality) |
| Tier | STRICT |
| Confidence | [████████░░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0023/spec.md`

**Deliverables:**
1. Prompt budget enforcement: 30,720 byte total with proportional allocation (60% spec/roadmap, 20% structural context, 15% prior summary, 5% template); truncation markers with section heading `[TRUNCATED: N bytes omitted from '<heading>']`; `ValueError` if template exceeds 5% allocation; `assert` before every LLM call

**Steps:**
1. **[PLANNING]** Review existing budget constants and `_truncate_to_budget()` in `semantic_layer.py`
2. **[EXECUTION]** Ensure truncation markers include section heading per FR-4.2 acceptance criteria
3. **[EXECUTION]** Implement `ValueError` on template exceeding 5% allocation (1,536 bytes)
4. **[EXECUTION]** Implement truncation priority: prior summary -> structural context -> spec/roadmap sections
5. **[VERIFICATION]** Test prompt sizes on large and small inputs; verify `assert len(prompt) <= 30720` fires before LLM call
6. **[COMPLETION]** Document budget enforcement in `TASKLIST_ROOT/artifacts/D-0023/spec.md`

**Acceptance Criteria:**
- Truncation markers include section heading: `[TRUNCATED: N bytes omitted from '<heading>']`
- Template exceeding 5% allocation (1,536 bytes) raises `ValueError`
- Truncation priority: prior summary first, then structural context, then spec/roadmap sections
- `assert len(prompt) <= 30720` precedes every LLM call in semantic layer (SC-6)

**Validation:**
- `uv run pytest tests/roadmap/test_semantic_layer.py -v -k "budget or truncat"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0023/spec.md` documents budget enforcement

**Dependencies:** T04.01
**Rollback:** TBD

---

### T04.03 -- Implement validate_semantic_high() Debate Protocol (FR-4.1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041, R-042 |
| Why | When semantic layer assigns HIGH, adversarial debate validates it. The judge is deterministic Python -- same scores always produce same verdict. |
| Effort | L |
| Risk | High |
| Risk Drivers | cross-cutting (debate verdicts feed registry and convergence), dependency (requires ClaudeProcess) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0024/spec.md`

**Deliverables:**
1. `validate_semantic_high()` in `semantic_layer.py` implementing FR-4.1 protocol steps 1-7: builds prosecutor + defender prompts, executes both via ClaudeProcess in parallel (2 LLM calls), parses YAML responses (default scores 0 on parse failure), scores via 4-criterion rubric (Evidence 30%, Impact 25%, Coherence 25%, Concession 20%), deterministic judge verdict with 0.15 margin threshold and conservative tiebreak (CONFIRM_HIGH)

**Steps:**
1. **[PLANNING]** Review existing debate infrastructure: `score_argument()`, `judge_verdict()`, `wire_debate_verdict()`
2. **[PLANNING]** Design `validate_semantic_high()` parameter list per spec signature
3. **[EXECUTION]** Implement `validate_semantic_high()` with `claude_process_factory` parameter for test injection
4. **[EXECUTION]** Implement parallel prosecutor/defender execution (2 LLM calls)
5. **[EXECUTION]** Implement deterministic judge: 4-criterion rubric, margin computation, conservative tiebreak
6. **[VERIFICATION]** Test with injected `claude_process_factory`: verify deterministic judge produces consistent verdicts
7. **[COMPLETION]** Document debate protocol in `TASKLIST_ROOT/artifacts/D-0024/spec.md`

**Acceptance Criteria:**
- `validate_semantic_high()` exists in `semantic_layer.py` with `claude_process_factory` parameter
- Prosecutor and defender execute in parallel (2 LLM calls, not sequential)
- Deterministic judge: same rubric scores always produce same verdict
- Conservative tiebreak: margin within +/-0.15 always produces CONFIRM_HIGH
- Token budget per finding ~3,800 (hard cap: 5,000); YAML parse failure defaults all rubric scores to 0 for that side

**Validation:**
- `uv run pytest tests/roadmap/test_semantic_layer.py -v -k "debate or validate_semantic_high"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0024/spec.md` documents debate protocol

**Dependencies:** T04.01, T03.01
**Rollback:** TBD
**Notes:** Risk #4 (debate rubric calibration) MEDIUM severity. Ship conservative, tune after real corpus.

---

### T04.04 -- Implement Debate YAML Output and Registry Wiring

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | Debate verdicts must be recorded in YAML per finding and wired into the deviation registry for convergence tracking. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | data (registry mutation from debate verdicts) |
| Tier | STANDARD |
| Confidence | [████████░░] 82% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0025/evidence.md`

**Deliverables:**
1. Debate output YAML written to `output_dir/debates/{finding.stable_id}/debate.yaml` with rubric scores, margin, verdict; registry updated via `wire_debate_verdict()` with `debate_verdict` and `debate_transcript` reference

**Steps:**
1. **[PLANNING]** Define YAML output schema: rubric scores per side, margin, verdict
2. **[EXECUTION]** Implement YAML writing to `output_dir/debates/{stable_id}/debate.yaml`
3. **[EXECUTION]** Call `wire_debate_verdict()` after each debate to update registry
4. **[EXECUTION]** Handle YAML parse failure: all rubric scores default to 0 for that side
5. **[VERIFICATION]** Verify YAML output format and registry update after debate
6. **[COMPLETION]** Document output format in `TASKLIST_ROOT/artifacts/D-0025/evidence.md`

**Acceptance Criteria:**
- Debate output YAML written per finding to `output_dir/debates/{stable_id}/debate.yaml`
- YAML contains rubric scores for prosecutor and defender, margin value, and verdict string
- Registry updated with `debate_verdict` and `debate_transcript` path after each debate
- YAML parse failure for either side defaults all rubric scores to 0

**Validation:**
- `uv run pytest tests/roadmap/test_semantic_layer.py -v -k "debate_output or wire_verdict"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0025/evidence.md` documents YAML output format

**Dependencies:** T04.03, T03.01
**Rollback:** TBD

---

### T04.05 -- Validate Run-to-Run Memory in Semantic Layer End-to-End

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039, R-040 |
| Why | Prior findings from registry must correctly influence semantic layer behavior. This validates the FR-10 integration end-to-end, not just unit-level. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (registry -> semantic layer -> convergence) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0026 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0026/evidence.md`

**Deliverables:**
1. End-to-end test: prior findings from registry memory correctly appear in semantic layer prompt context; fixed findings from prior runs not re-reported; prompt budget respects prior summary allocation (15%)

**Steps:**
1. **[PLANNING]** Design E2E test: seed registry with prior findings, run semantic layer, verify prompt
2. **[EXECUTION]** Seed registry with findings from simulated prior runs
3. **[EXECUTION]** Run semantic layer and capture prompt sent to LLM
4. **[EXECUTION]** Verify prior findings summary present in prompt; verify fixed findings excluded
5. **[VERIFICATION]** Confirm prior summary fits within 15% budget allocation (4,608 bytes)
6. **[COMPLETION]** Document E2E results in `TASKLIST_ROOT/artifacts/D-0026/evidence.md`

**Acceptance Criteria:**
- Semantic layer prompt includes prior findings summary from registry (ID, severity, status, run_number)
- Fixed findings from prior runs do not appear in semantic layer output as new findings
- Prior findings summary fits within 15% budget allocation (4,608 bytes)
- Truncation occurs at 50 findings if more exist in registry

**Validation:**
- `uv run pytest tests/roadmap/test_semantic_layer.py -v -k "memory_integration"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0026/evidence.md` documents E2E memory behavior

**Dependencies:** T04.01, T04.02, T03.03
**Rollback:** TBD

---

### Checkpoint: Phase 4 / Tasks T04.01-T04.05

**Purpose:** Verify semantic layer and debate protocol before SC-4 intermediate check.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md`
**Verification:**
- Semantic layer processes only non-structural dimensions
- No prompt exceeds 30,720 bytes (SC-6 check)
- Debate protocol produces consistent verdicts on identical inputs
**Exit Criteria:**
- Prior findings from registry correctly influence semantic layer
- Debate YAML output written and registry updated for each HIGH finding
- All semantic findings tagged with `source_layer="semantic"`

---

### T04.06 -- SC-4 Intermediate Check: Structural Ratio >= 70%

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | SC-4 requires >=70% of findings from structural rules. This intermediate check validates the architectural goal before convergence integration. |
| Effort | S |
| Risk | Low |
| Risk Drivers | none matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0027 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0027/evidence.md`

**Deliverables:**
1. SC-4 intermediate verification: run structural + semantic on test spec; count findings by `source_layer`; verify structural >= 70% of total

**Steps:**
1. **[PLANNING]** Prepare test spec with known structural and semantic findings
2. **[EXECUTION]** Run all 5 structural checkers and semantic layer on test spec
3. **[EXECUTION]** Count findings by `source_layer`: structural vs semantic
4. **[EXECUTION]** Compute ratio: `structural_count / total_count >= 0.70`
5. **[VERIFICATION]** Confirm SC-4 threshold met
6. **[COMPLETION]** Document ratio in `TASKLIST_ROOT/artifacts/D-0027/evidence.md`

**Acceptance Criteria:**
- Structural findings account for >= 70% of total findings on test spec (SC-4)
- Finding counts documented by source_layer
- If ratio < 70%, identify which dimensions need additional structural rules
- Evidence document shows exact counts and ratio

**Validation:**
- `uv run pytest tests/roadmap/test_structural_checkers.py::test_sc4_ratio -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0027/evidence.md` with structural/semantic ratio

**Dependencies:** T04.01, T02.05
**Rollback:** TBD

---

### Checkpoint: End of Phase 4

**Purpose:** Semantic layer and debate protocol validated. Architectural ordering confirmed: Registry -> Semantic -> Convergence.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`
**Verification:**
- Semantic layer processes only non-structural dimensions
- No prompt exceeds 30,720 bytes (SC-6)
- Debate protocol produces consistent verdicts; >=70% findings structural (SC-4)
**Exit Criteria:**
- Prior findings from registry correctly influence semantic layer behavior
- Run-to-run memory integration validated end-to-end
- All Phase 4 tasks completed with passing validation
