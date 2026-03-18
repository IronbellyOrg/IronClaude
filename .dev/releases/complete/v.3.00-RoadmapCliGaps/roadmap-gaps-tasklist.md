# Roadmap Pipeline Fidelity Gaps — Tasklist

**Purpose**: Fix 5 structural fidelity gaps between the source protocol (`sc-roadmap-protocol`) and the CLI pipeline port (`src/superclaude/cli/roadmap/`).

**Execution**: Each task is designed for `/sc:task-unified`. Tasks specify tier, files, acceptance criteria, and dependencies.

**Branch**: `fix/roadmap-pipeline-fidelity-gaps`

---

## Dependency Graph

```
T1 (Gap #1) ─────┐
T2 (Gap #2) ──────┼──► T4 (Gap #4+6) ──► T5 (Integration test) ──► T6 (Verify)
T3 (Gap #3) ──────┘         ▲
                             │
                    T3.5 (Gap #5) ─┘
```

- **T1, T2, T3**: Independent — execute in parallel
- **T3.5**: Independent — can run parallel with T1-T3
- **T4**: Depends on T1 (reuses `_complexity_class_valid`)
- **T5**: Depends on T1-T4 + T3.5
- **T6**: Depends on T5

---

## T1: Fix `complexity_class` enum mismatch

**Tier**: 2-standard
**Proposal**: `docs/generated/gap-1-complexity-class-enum-proposal.md`
**Depends on**: None
**Files**:
- `src/superclaude/cli/roadmap/prompts.py` — line 88: change `simple, moderate, complex, enterprise` to `LOW, MEDIUM, HIGH`
- `src/superclaude/cli/roadmap/gates.py` — add `_complexity_class_valid` semantic check function; add it to `EXTRACT_GATE.semantic_checks`
- `src/superclaude/examples/release-spec-template.md` — line 28: fix placeholder enum
- `tests/roadmap/test_gates_data.py` — update 3 fixtures from `"moderate"` to `"MEDIUM"`; add `TestComplexityClassValid` test class

**Acceptance criteria**:
- [ ] `prompts.py` line 88 says `LOW, MEDIUM, HIGH` (not `simple, moderate, complex, enterprise`)
- [ ] `EXTRACT_GATE.semantic_checks` contains `complexity_class_valid` check
- [ ] `_complexity_class_valid` accepts `LOW`, `MEDIUM`, `HIGH` (case-insensitive) and rejects `simple`, `enterprise`
- [ ] No remaining occurrences of `simple, moderate, complex, enterprise` in `src/superclaude/cli/`
- [ ] `uv run pytest tests/roadmap/test_gates_data.py -v` passes

---

## T2: Fix `extraction_mode` enum mismatch

**Tier**: 2-standard
**Proposal**: `docs/generated/gap-2-extraction-mode-enum-proposal.md`
**Depends on**: None
**Files**:
- `src/superclaude/cli/roadmap/prompts.py` — line 93: change `full, partial, incremental` to `standard, chunked`
- `src/superclaude/cli/roadmap/gates.py` — add `_extraction_mode_valid` semantic check; add to `EXTRACT_GATE.semantic_checks`
- `tests/roadmap/test_executor.py` — line 107: update `extraction_mode: "full"` to `"standard"`
- `tests/roadmap/test_pipeline_integration.py` — line 91: update fixture
- `tests/roadmap/test_integration_v5_pipeline.py` — line 96: update fixture

**Acceptance criteria**:
- [ ] `prompts.py` line 93 says `standard` or `chunked` (not `full, partial, incremental`)
- [ ] `_extraction_mode_valid` accepts `standard` and values starting with `chunked` (e.g., `chunked (3 chunks)`)
- [ ] `_extraction_mode_valid` rejects `full`, `partial`, `incremental`
- [ ] No remaining occurrences of `full|partial|incremental` as extraction_mode values in `src/` or `tests/`
- [ ] `uv run pytest tests/roadmap/ -v` passes

---

## T3: Change `domains_detected` from integer to array

**Tier**: 2-standard
**Proposal**: `docs/generated/gap-3-domains-detected-type-proposal.md`
**Depends on**: None
**Files**:
- `src/superclaude/cli/roadmap/prompts.py` — `build_extract_prompt`: change `domains_detected` from `(integer) count` to `(list) array of domain name strings, e.g. [backend, security, frontend]`
- `src/superclaude/cli/roadmap/prompts.py` — `build_generate_prompt` line 146: change "number of technical domains" to "list of technical domain names"
- Test fixtures referencing `domains_detected` as integer — update to array format

**Acceptance criteria**:
- [ ] Extract prompt requests `domains_detected` as a YAML inline array (e.g., `[backend, security]`)
- [ ] Generate prompt describes `domains_detected` as "list of technical domain names"
- [ ] `_parse_frontmatter` in `gates.py` handles array values without error (no code change needed — verify only)
- [ ] `uv run pytest tests/roadmap/ -v` passes

---

## T3.5: Add provenance field injection for test-strategy

**Tier**: 2-standard
**Proposal**: `docs/generated/gap-5-test-strategy-provenance-proposal.md`
**Depends on**: None (independent of T1-T3)
**Files**:
- `src/superclaude/cli/roadmap/executor.py` — add `_inject_provenance_fields()` function (~25 lines); add call in `roadmap_run_step()` for `step.id == "test-strategy"`
- `src/superclaude/cli/roadmap/gates.py` — add `"spec_source"`, `"generated"`, `"generator"` to `TEST_STRATEGY_GATE.required_frontmatter_fields`

**Acceptance criteria**:
- [ ] `_inject_provenance_fields()` mirrors the pattern of `_inject_pipeline_diagnostics()` (read file, find frontmatter, insert fields, write)
- [ ] Injection happens inside `roadmap_run_step()` before the step result is returned (i.e., before gate check in the caller)
- [ ] `TEST_STRATEGY_GATE.required_frontmatter_fields` includes `spec_source`, `generated`, `generator`
- [ ] `uv run pytest tests/roadmap/ -v` passes

**Note**: When T4 also lands, the final `TEST_STRATEGY_GATE` will have 9 required fields total. Coordinate field list with T4.

---

## T4: Harden test-strategy prompt and gate (merged Gap #4 + #6)

**Tier**: 3-complex
**Proposal**: `docs/generated/gap-4-6-test-strategy-unified-proposal.md`
**Depends on**: T1 (reuses `_complexity_class_valid` from Gap #1)
**Files**:
- `src/superclaude/cli/roadmap/prompts.py` — rewrite `build_test_strategy_prompt` with 6 frontmatter fields, complexity-to-ratio mapping, issue classification table
- `src/superclaude/cli/roadmap/gates.py` — add 4 semantic check functions (`_interleave_ratio_consistent`, `_milestone_counts_positive`, `_validation_philosophy_correct`, `_major_issue_policy_correct`); rewrite `TEST_STRATEGY_GATE` with 6 required fields, 5 semantic checks, STRICT tier
- `tests/roadmap/test_gates_data.py` — replace `test_test_strategy_gate_standard`; add 8 test classes (~35 test cases)

**Acceptance criteria**:
- [ ] `build_test_strategy_prompt` requests: `complexity_class`, `validation_philosophy`, `validation_milestones`, `work_milestones`, `interleave_ratio`, `major_issue_policy`
- [ ] Prompt contains explicit ratio mapping: LOW→1:3, MEDIUM→1:2, HIGH→1:1
- [ ] Prompt says "M# or Phase headings" for `work_milestones` counting
- [ ] Prompt instructs exact values for constants: `continuous-parallel`, `stop-and-fix`
- [ ] `TEST_STRATEGY_GATE.enforcement_tier == "STRICT"`
- [ ] `TEST_STRATEGY_GATE` has 5 semantic checks (after dedup with T3.5's fields)
- [ ] `_complexity_class_valid` is the same function registered on both `EXTRACT_GATE` and `TEST_STRATEGY_GATE` (not a copy)
- [ ] `_interleave_ratio_consistent` rejects LOW+1:1 and HIGH+1:3
- [ ] `_validation_philosophy_correct` rejects `continuous_parallel` (underscore variant)
- [ ] `uv run pytest tests/roadmap/test_gates_data.py -v` passes

---

## T5: Integration test — full gate validation

**Tier**: 2-standard
**Depends on**: T1, T2, T3, T3.5, T4
**Files**:
- `tests/roadmap/test_gates_data.py` — verify ALL_GATES list is consistent
- Run full test suite

**Acceptance criteria**:
- [ ] `uv run pytest tests/roadmap/ -v` — all tests pass
- [ ] `uv run pytest tests/ -v` — full suite passes (no regressions outside roadmap/)
- [ ] Verify `ALL_GATES` list in `gates.py` references the updated gate instances
- [ ] Grep confirms zero occurrences of old enum values (`simple|moderate|complex|enterprise`, `full|partial|incremental`) in `src/superclaude/cli/`

---

## T6: Final verification and cleanup

**Tier**: 1-simple
**Depends on**: T5
**Files**: None (read-only verification)

**Acceptance criteria**:
- [ ] `make lint` passes
- [ ] `make format` produces no changes
- [ ] No TODO stubs or placeholder comments left in changed files
- [ ] Each proposal file in `docs/generated/` can be marked as IMPLEMENTED in its Validation Result section
