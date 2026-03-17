# Phase 4 -- Gate System

Create the enforcement system that prevents low-quality or structurally invalid artifacts from propagating. Implement all 12 gates with complete per-gate check mapping and semantic validation layer.

---

### T04.01 -- Implement All 12 Gates (G-000 through G-011) in gates.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034 |
| Why | All 12 gates must be implemented before Phase 5 Claude-assisted steps run; a gate that doesn't exist cannot block a bad artifact |
| Effort | XL |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0030/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/gates.py` with all 12 gate implementations (G-000–G-011), frontmatter checks, minimum line counts, tier assignment (STANDARD/STRICT), and `GateMode.BLOCKING` enforcement

**Steps:**
1. **[PLANNING]** Load existing `gates.py` if present; review per-gate check mapping from roadmap Phase 3 table
2. **[PLANNING]** Import `GateCriteria`, `GateMode`, `SemanticCheck` from `superclaude.cli.pipeline.models` (NOT sprint.models)
3. **[EXECUTION]** Implement G-000: `has_valid_yaml_config` — config YAML valid with workflow_path, cli_name, output_dir
4. **[EXECUTION]** Implement G-001: `has_component_inventory` — inventory lists ≥1 component with SKILL.md
5. **[EXECUTION]** Implement G-002: `EXIT_RECOMMENDATION` marker present
6. **[EXECUTION]** Implement G-003: `EXIT_RECOMMENDATION` present + `has_required_analysis_sections` (Source Components, Step Graph, Parallel Groups, Gates Summary, Data Flow, Classifications, Recommendations)
7. **[EXECUTION]** Implement G-004: `has_approval_status` (approved/rejected/pending field present)
8. **[EXECUTION]** Implement G-005: `EXIT_RECOMMENDATION` marker present
9. **[EXECUTION]** Implement G-006: return type pattern check
10. **[EXECUTION]** Implement G-007: `EXIT_RECOMMENDATION` marker present
11. **[EXECUTION]** Implement G-008: `EXIT_RECOMMENDATION` present + step-count consistency (step_mapping count matches declared steps)
12. **[EXECUTION]** Implement G-009: `has_approval_status`
13. **[EXECUTION]** Implement G-010: `EXIT_RECOMMENDATION` + `has_zero_placeholders` (zero `{{SC_PLACEHOLDER:*}}`) + `has_brainstorm_section` (Section 12)
14. **[EXECUTION]** Implement G-011: `has_quality_scores` (clarity, completeness, testability, consistency, overall) + `has_criticals_addressed` (all CRITICAL marked [INCORPORATED] or [DISMISSED])
15. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "gates or gate_" -v` — each gate passes valid input and fails invalid input
16. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0030/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "gates"` exits 0 with all 12 gates covered
- Each gate has at least one passing test (valid artifact) and one failing test (invalid artifact)
- `GateMode.BLOCKING` set on all gates — no gate allows non-blocking continuation on failure
- G-010 correctly rejects any artifact with `{{SC_PLACEHOLDER:*}}` sentinel

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "gates" -v` — all 24+ gate test cases (2 per gate) pass
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0030/spec.md` produced

**Dependencies:** T03.01 (models.py with GateCriteria/GateMode from pipeline.models), T01.02 (import paths confirmed)
**Rollback:** Revert `gates.py` to prior state

---

### T04.02 -- Implement Semantic Check Functions in gates.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035 |
| Why | Semantic checks validate content quality beyond structural presence; they must return `tuple[bool, str]` so callers get both a pass/fail signal and a diagnostic message |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0031/spec.md`

**Deliverables:**
- `gates.py` semantic check helper functions: `has_valid_yaml_config()`, `has_component_inventory()`, `has_required_analysis_sections()`, `has_approval_status()`, `has_zero_placeholders()`, `has_brainstorm_section()`, `has_quality_scores()`, `has_criticals_addressed()` — all returning `tuple[bool, str]` (FR-047, AC-004)

**Steps:**
1. **[PLANNING]** Review roadmap FR-047/AC-004: semantic checks return `tuple[bool, str]`
2. **[EXECUTION]** Implement each helper as a standalone function in `gates.py`
3. **[EXECUTION]** Each returns `(True, "")` on pass or `(False, "<diagnostic message>")` on failure
4. **[EXECUTION]** `has_required_analysis_sections`: check for all 7 required section headers
5. **[EXECUTION]** `has_zero_placeholders`: regex scan for `{{SC_PLACEHOLDER:` pattern
6. **[EXECUTION]** `has_quality_scores`: check for clarity, completeness, testability, consistency, overall fields in frontmatter or body
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "semantic_check" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0031/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "semantic_check"` exits 0
- Each helper returns `tuple[bool, str]` (AC-004 compliance)
- Diagnostic message on failure is non-empty and describes the specific missing element
- `has_zero_placeholders` correctly detects `{{SC_PLACEHOLDER:SECTION_NAME}}`

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "semantic_check" -v` — tuple return type verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0031/spec.md` produced

**Dependencies:** T04.01 (gates.py exists)
**Rollback:** Remove helper functions from `gates.py`

---

### T04.03 -- Implement Gate Diagnostics Formatting

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036 |
| Why | Gate failures must produce actionable diagnostic output; without formatted diagnostics, developers cannot identify which check failed or why |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0032/spec.md`

**Deliverables:**
- `gates.py` `format_gate_failure(gate_id: str, check_name: str, diagnostic: str, artifact_path: str) -> str` producing human-readable gate failure messages

**Steps:**
1. **[PLANNING]** Review gate failure format needed by `diagnostics.py` (output Phase 9 = roadmap Phase 8 observability)
2. **[EXECUTION]** Implement `format_gate_failure(gate_id, check_name, diagnostic, artifact_path) -> str`
3. **[EXECUTION]** Output format: `"Gate {gate_id} FAILED: {check_name}\n  Artifact: {artifact_path}\n  Reason: {diagnostic}\n  Fix: {remediation_hint}"`
4. **[EXECUTION]** Add `GateFailure` dataclass: `{gate_id, check_name, diagnostic, artifact_path, tier}`
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "gate_diagnostics or gate_failure" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0032/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "gate_diagnostics"` exits 0
- `format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "portify-analysis-report.md")` returns multi-line string with all 4 fields
- `GateFailure` dataclass importable from `superclaude.cli.cli_portify.gates`
- Diagnostic string is never empty for a failing gate

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "gate_failure" -v` — format output verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0032/spec.md` produced

**Dependencies:** T04.02 (semantic checks produce diagnostic strings)
**Rollback:** Remove `format_gate_failure()` function

---

### Checkpoint: End of Phase 4

**Purpose:** Verify all 12 gates validate correctly against synthetic test data before Phase 5 Claude-assisted steps produce real artifacts that gates must evaluate.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P04-END.md`

**Verification:**
- `uv run pytest tests/cli_portify/ -k "gates or semantic_check or gate_diagnostics" -v` exits 0
- All 12 gates (G-000–G-011) have passing + failing test cases
- Gate diagnostics produce non-empty, human-readable failure messages

**Exit Criteria:**
- All 3 Phase 4 tasks complete with D-0030 through D-0032 artifacts
- Milestone M3: all 12 gates validate deterministically; gate failures well-diagnosed; BLOCKING enforcement confirmed
- PASS_NO_SIGNAL → retry, PASS_NO_REPORT → no retry distinction implemented in gate retry logic (T03.08/T03.09)
