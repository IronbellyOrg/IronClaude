# Phase 7 -- ToolOrchestrator Plugin

Implement the AST analyzer plugin for the `ToolOrchestrator` injection seam, improving data quality for orphan detection via the dual evidence rule. This phase is conditional: if not complete before Phase 8 begins, defer to v2.1 per section 5.3.1 cut criteria. Milestone M5: `FileAnalysis.references` populated for files with imports.

### T07.01 -- Implement AST Plugin for ToolOrchestrator in cli/audit/wiring_analyzer.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038 |
| Why | G-008 requires an AST analyzer plugin that integrates with ToolOrchestrator to populate FileAnalysis.references, improving orphan module detection accuracy |
| Effort | M |
| Risk | Medium |
| Risk Drivers | audit (plugin integration), multi-file (analyzer + orchestrator interaction) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0033/spec.md

**Deliverables:**
- AST analyzer plugin class/function in `src/superclaude/cli/audit/wiring_analyzer.py` that hooks into the `ToolOrchestrator` plugin seam and populates `FileAnalysis.references` with import-derived cross-file references

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/audit/tool_orchestrator.py` to understand the `ToolOrchestrator` plugin interface and `FileAnalysis` type
2. **[PLANNING]** Read section 5.3 for AST plugin specification and integration requirements
3. **[EXECUTION]** Implement plugin that registers with `ToolOrchestrator` using the existing plugin seam
4. **[EXECUTION]** Plugin processes each file using `ast_analyze_file()` and populates `FileAnalysis.references` with resolved import targets
5. **[EXECUTION]** Handle circular imports and missing modules gracefully (return partial results)
6. **[VERIFICATION]** Run `uv run pytest tests/audit/test_wiring_analyzer.py -k "plugin" -v` to validate plugin integration
7. **[COMPLETION]** Document plugin registration and lifecycle in module docstring

**Acceptance Criteria:**
- Plugin registers with `ToolOrchestrator` without modifying the orchestrator's existing interface
- `FileAnalysis.references` is populated with import-derived references for files with `import` statements
- Plugin handles circular imports and missing modules without raising exceptions
- No imports from `pipeline/*` in `wiring_analyzer.py` (NFR-007)

**Validation:**
- `uv run pytest tests/audit/test_wiring_analyzer.py -k "plugin" -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0033/spec.md

**Dependencies:** T02.06 (ast_analyze_file utility)
**Rollback:** Remove plugin class/function from wiring_analyzer.py
**Notes:** Conditional phase: defer to v2.1 if not complete before Phase 8 begins per section 5.3.1 cut criteria.

---

### T07.02 -- Wire Dual Evidence Rule Using Plugin Output in cli/audit/wiring_analyzer.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Section 5.2.2 dual evidence rule requires both import-graph and AST-reference evidence before confirming a module as orphaned, reducing false positives |
| Effort | S |
| Risk | Medium |
| Risk Drivers | audit (evidence rule logic), compliance (section 5.2.2) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0034 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0034/spec.md

**Deliverables:**
- Dual evidence rule implementation in `wiring_analyzer.py` that combines import-graph evidence (from orphan analyzer) with `FileAnalysis.references` evidence (from AST plugin) before confirming orphan status

**Steps:**
1. **[PLANNING]** Read section 5.2.2 for dual evidence rule specification
2. **[PLANNING]** Identify integration point between `analyze_orphan_modules()` and AST plugin output
3. **[EXECUTION]** Modify orphan detection to require both import-graph absence AND `FileAnalysis.references` absence before flagging as orphan
4. **[EXECUTION]** When plugin data is unavailable (plugin not loaded), fall back to import-graph-only evidence with a note in findings
5. **[VERIFICATION]** Run `uv run pytest tests/audit/ -k "dual_evidence" -v` with fixtures that have references but no imports (should not flag as orphan)
6. **[COMPLETION]** Document dual evidence rule and fallback behavior in docstring

**Acceptance Criteria:**
- Orphan detection requires both import-graph and FileAnalysis.references evidence when plugin is loaded
- Modules with FileAnalysis.references but no imports are NOT flagged as orphans (dual evidence prevents false positive)
- When plugin is not loaded, orphan detection falls back to import-graph-only with a note in finding evidence text
- Dual evidence rule reduces false positive rate for orphan detection

**Validation:**
- `uv run pytest tests/audit/ -k "dual_evidence" -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0034/spec.md

**Dependencies:** T07.01 (AST plugin for FileAnalysis.references), T02.04 (orphan analyzer)
**Rollback:** Revert orphan detection to import-graph-only evidence

---

### T07.03 -- Implement Unit Tests for AST Plugin Integration in tests/audit/

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | SC-013 requires test evidence for ast_analyze_file() plugin integration, and section 10.1 mandates >=3 tests for this function |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0035 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0035/evidence.md

**Deliverables:**
- >=3 unit tests in `tests/audit/test_wiring_analyzer.py` for AST plugin: (1) plugin registers with ToolOrchestrator, (2) FileAnalysis.references populated for files with imports, (3) dual evidence rule reduces orphan false positives

**Steps:**
1. **[PLANNING]** Review SC-013 and section 10.1 test requirements (3 tests for ast_analyze_file)
2. **[PLANNING]** Design test fixtures with files that have imports and files without
3. **[EXECUTION]** Write test_plugin_registration: verify plugin registers with ToolOrchestrator and is callable
4. **[EXECUTION]** Write test_references_populated: verify FileAnalysis.references contains import targets for a file with imports (SC-013)
5. **[EXECUTION]** Write test_dual_evidence_reduces_fps: verify module with references but no imports is NOT flagged as orphan
6. **[VERIFICATION]** Run `uv run pytest tests/audit/test_wiring_analyzer.py -k "plugin" -v` and verify >=3 tests pass
7. **[COMPLETION]** Record test results in evidence artifact

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_wiring_analyzer.py -k "plugin" -v` exits 0 with >=3 tests passing
- Plugin registration test confirms successful hookup with ToolOrchestrator
- References populated test confirms FileAnalysis.references is non-empty for files with imports (SC-013)
- Dual evidence test confirms false positive reduction for orphan detection

**Validation:**
- `uv run pytest tests/audit/test_wiring_analyzer.py -k "plugin" -v` exits 0 with >=3 tests passing
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0035/evidence.md

**Dependencies:** T07.01, T07.02
**Rollback:** Remove plugin-related test functions

---

### Checkpoint: End of Phase 7

**Purpose:** Validate milestone M5: FileAnalysis.references populated for files with imports. Evaluate cut criteria.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P07-END.md
**Verification:**
- AST plugin registers with ToolOrchestrator and populates FileAnalysis.references
- Dual evidence rule reduces orphan detection false positives
- Plugin handles circular imports and missing modules gracefully
**Exit Criteria:**
- `uv run pytest tests/audit/test_wiring_analyzer.py -k "plugin" -v` exits 0 with >=3 tests passing (SC-013)
- Cut criteria evaluation: if Phase 8 has not begun, this phase is complete; if Phase 8 has begun, defer remaining work to v2.1
- No imports from `pipeline/*` in `wiring_analyzer.py` (NFR-007)
