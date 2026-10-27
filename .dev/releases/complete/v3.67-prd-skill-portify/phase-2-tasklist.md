# Phase 2 -- Prompts + Config

**Goal**: Implement the 19 prompt builder functions and the CLI argument resolution module. These modules depend on Phase 1 models but are independent of the execution engine.

**Files**: `prompts.py`, `config.py` + corresponding unit tests

**Dependencies**: Phase 1 (models.py for type imports)

---

## T02.01: Implement prompts.py

**Effort**: S | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential, Context7
**Sub-Agent Delegation**: None

**Deliverable**: D-0010 u2014 `src/superclaude/cli/prd/prompts.py`
**Roadmap Items**: R-020, R-039, R-043

**Steps**:
1. **[PLANNING]** Read `.dev/portify-workdir/prd/portify-prompts.md` (1,071 lines) for complete prompt builder specifications
2. **[PLANNING]** Read `src/superclaude/skills/prd/refs/agent-prompts.md` for source agent prompt templates
3. **[EXECUTION]** Implement helper functions: `_load_json(path) -> dict`, `_read_file(path, max_bytes=50*1024) -> str` with truncation marker [GAP-010], `_today() -> str`
4. **[EXECUTION]** Implement Stage A prompt builders (7): `build_parse_request_prompt`, `build_scope_discovery_prompt`, `build_research_notes_prompt`, `build_sufficiency_review_prompt`, `build_task_file_prompt`, `build_verify_task_file_prompt`, `build_preparation_prompt`
5. **[EXECUTION]** Implement Stage B prompt builders (8): `build_investigation_prompt`, `build_web_research_prompt`, `build_analyst_completeness_prompt`, `build_qa_research_gate_prompt`, `build_synthesis_prompt`, `build_analyst_synthesis_prompt`, `build_qa_synthesis_gate_prompt`, `build_gap_filling_prompt`
6. **[EXECUTION]** Implement final stage prompt builders (4): `build_assembly_prompt`, `build_structural_qa_prompt`, `build_qualitative_qa_prompt`, `build_completion_prompt`
7. **[EXECUTION]** Enforce 100KB prompt size cap: inline content capped at 50KB per file, larger files passed as `--file` args [NFR-PRD.8/GAP-008]
8. **[VERIFICATION]** Verify all 19 builders are callable and produce non-empty strings; verify `_read_file` truncates at 50KB
9. **[COMPLETION]** Record function count and largest prompt size estimate in evidence

**Acceptance Criteria**:
- [ ] 19 prompt builder functions + 3 helpers implemented (22 functions total)
- [ ] `_read_file()` truncates at 50KB with `[TRUNCATED u2014 file exceeds 50KB inline limit]` marker
- [ ] All prompt builders include `EXIT_RECOMMENDATION: CONTINUE|HALT` instruction in output format spec
- [ ] Context injection supported: builders accepting `inputs` parameter also accept `context_summaries` [NFR-PRD.11/GAP-004]

**Validation**:
- `uv run python -c "from superclaude.cli.prd.prompts import build_parse_request_prompt; print(len(build_parse_request_prompt('test')))"`
- Evidence: 19 prompt builders importable, each produces non-empty string

**Risk Drivers**: None

---

## T02.02: Implement config.py

**Effort**: S | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential, Context7
**Sub-Agent Delegation**: None

**Deliverable**: D-0011 u2014 `src/superclaude/cli/prd/config.py`
**Roadmap Items**: R-021, R-052

**Steps**:
1. **[PLANNING]** Review Section 5.1 (CLI Surface) for all options, flags, defaults
2. **[PLANNING]** Review PrdConfig fields from models.py to understand construction requirements
3. **[EXECUTION]** Implement `resolve_config(request, product, where, output, tier, max_turns, model, dry_run, debug, resume_from) -> PrdConfig`
4. **[EXECUTION]** Implement path resolution: output_path defaults to `.`, task_dir derived from product_slug, skill_refs_dir auto-discovered
5. **[EXECUTION]** Implement tier validation: must be one of "lightweight", "standard", "heavyweight"
6. **[EXECUTION]** Implement resume validation: if resume_from is set, verify the step ID format matches known step patterns
7. **[VERIFICATION]** Verify `resolve_config` produces valid PrdConfig for minimal inputs (request only)
8. **[COMPLETION]** Record config construction paths in evidence

**Acceptance Criteria**:
- [ ] `resolve_config()` constructs PrdConfig from CLI arguments with correct defaults
- [ ] Path resolution handles relative and absolute paths correctly
- [ ] Tier validation rejects invalid tier values with descriptive error
- [ ] Dry-run flag propagated correctly to PrdConfig

**Validation**:
- `uv run python -c "from superclaude.cli.prd.config import resolve_config; c = resolve_config('test PRD'); print(c.tier)"`
- Evidence: resolve_config produces PrdConfig with tier='standard' default

**Risk Drivers**: None

---

## T02.03: Write unit tests for prompts.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0012 u2014 `tests/cli/prd/test_prompts.py`
**Roadmap Items**: R-049

**Steps**:
1. **[PLANNING]** Review Section 8.1 test plan for prompts.py tests (4 tests specified)
2. **[PLANNING]** Prepare test fixtures: synthetic research notes, investigation topics, synthesis mapping entries
3. **[EXECUTION]** Implement `test_build_investigation_prompt_includes_staleness_protocol`: verify Documentation Staleness Protocol markers in output [F-011]
4. **[EXECUTION]** Implement `test_build_synthesis_prompt_includes_template_reference`: verify template path reference in output [F-011]
5. **[EXECUTION]** Implement `test_prompt_size_under_100kb`: all 19 builders produce output < 100KB for synthetic worst-case inputs [F-011]
6. **[EXECUTION]** Implement `test_read_file_truncation_at_50kb`: `_read_file()` truncates large content with marker text [F-011]
7. **[VERIFICATION]** Run `uv run pytest tests/cli/prd/test_prompts.py -v` and verify all 4 tests pass
8. **[COMPLETION]** Record pass count in evidence

**Acceptance Criteria**:
- [ ] 4 test functions implemented matching Section 8.1 specification
- [ ] All tests pass with `uv run pytest tests/cli/prd/test_prompts.py -v`
- [ ] Truncation test verifies 50KB boundary with +/- 1 byte precision
- [ ] Worst-case prompt size test covers heavyweight tier with maximum research file count

**Validation**:
- `uv run pytest tests/cli/prd/test_prompts.py -v --tb=short`
- Evidence: 4 tests passed, 0 failures

**Risk Drivers**: None

---

### Checkpoint: End of Phase 2

**Purpose**: Verify all prompt builders and config resolution are complete before building the execution engine.

**Verification**:
- [ ] `prompts.py` and `config.py` exist and are importable
- [ ] `test_prompts.py` passes with 4/4 tests
- [ ] All 19 prompt builders produce non-empty output for minimal inputs

**Exit Criteria**:
- [ ] 24/24 cumulative unit tests passing (Phase 1: 20 + Phase 2: 4)
- [ ] No import errors across Phase 1 + Phase 2 modules
- [ ] Prompt size cap (100KB) verified for worst-case inputs
