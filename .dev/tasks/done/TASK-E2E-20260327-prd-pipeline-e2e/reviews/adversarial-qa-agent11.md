# Adversarial QA Report -- Round 6, Agent 11

**Date:** 2026-03-28
**Phase:** TDD/PRD pipeline E2E qualitative review
**Fix cycle:** N/A (report only)
**Scope:** Focused review of PRD supplementary blocks, auto-wire chain, extract prompt divergence, state schema, skill layer consistency, fidelity_checker.py, test correctness, and convergence flag interaction.

---

## Overall Verdict: FAIL

## Findings

### C-90 [TDD/PRD] IMPORTANT -- Merge step has no PRD context, breaking enrichment chain

**File:** `src/superclaude/cli/roadmap/executor.py:974-982`
**File:** `src/superclaude/cli/roadmap/prompts.py:505-534`

`build_merge_prompt()` accepts only 4 positional args (base_selection, variant_a, variant_b, debate) and has no `prd_file` parameter. The merge step in `_build_steps()` passes no PRD/TDD in its `inputs` list either. This means the final `roadmap.md` -- the document consumed by all downstream steps (spec-fidelity, test-strategy, tasklist) -- is produced by an LLM that never sees the PRD content.

The PRD enrichment chain is: extract (has PRD) -> generate (has PRD) -> diff (NO PRD) -> debate (NO PRD) -> score (has PRD) -> **merge (NO PRD)** -> spec-fidelity (has PRD). The merge step is the bottleneck: it produces the roadmap without PRD context, so any PRD-derived improvements from the generate/score steps can only survive if the LLM happened to embed them in the variant text. PRD-specific scoring dimensions (business value delivery, persona coverage, compliance alignment) evaluated in the score step cannot influence the merge if the merge LLM doesn't know they exist.

**Required fix:** Add `prd_file: Path | None = None` parameter to `build_merge_prompt()`. When present, append a PRD supplementary block instructing the merge to preserve PRD-derived prioritization, persona coverage, and compliance gates from the scored variants. Add `prd_file` to the merge step's `inputs` list in `_build_steps()`.

---

### C-91 [TDD/PRD] IMPORTANT -- _restore_from_state does not restore input_type on --resume

**File:** `src/superclaude/cli/roadmap/executor.py:1680-1766`

`_restore_from_state()` restores `agents`, `depth`, `tdd_file`, and `prd_file` from `.roadmap-state.json` but does NOT restore `input_type`. On `--resume`, `config.input_type` defaults to `"auto"`, which triggers re-detection in `execute_roadmap` (line 1821). While auto-detection is deterministic on the same file, this creates an asymmetry: every other config parameter is restored from state to ensure consistency, but `input_type` is re-derived. If the user edited the spec file between runs (e.g., to fix a fidelity deviation), the auto-detection score could change, causing the resume to use a different extraction prompt than the original run.

**Required fix:** Add `input_type` restoration to `_restore_from_state()`:
```python
if config.input_type == "auto":
    saved_input_type = state.get("input_type")
    if saved_input_type in ("tdd", "spec"):
        config = dataclasses.replace(config, input_type=saved_input_type)
```

---

### C-92 [TDD/PRD] IMPORTANT -- Double auto-detect: _build_steps re-detects after execute_roadmap already resolved

**File:** `src/superclaude/cli/roadmap/executor.py:852-859` and `1821-1823`

`execute_roadmap()` at line 1821 resolves `auto` to `tdd`/`spec` and replaces config via `dataclasses.replace()`. Then at line 1825, it calls `_build_steps(config)` which checks `config.input_type == "auto"` again at line 854. Since `execute_roadmap` already resolved it, the check in `_build_steps` is always False when called from `execute_roadmap`. However, `_build_steps` is also called directly in tests (e.g., `test_spec_fidelity.py:129`) where `config.input_type` is the default `"auto"` from `_make_config()`. In those test calls, `_build_steps` detects "auto" and calls `detect_input_type()` on the test spec, which is a 2-line stub that scores 0 and returns "spec". This means the auto-detect code path in `_build_steps` is only exercised from tests with trivial inputs -- the real auto-detect logic at line 1821 is never tested through `_build_steps`.

Additionally, `_build_steps` mutates its `config` argument by assigning to `config = dataclasses.replace(config, input_type=effective_input_type)` at line 859, but this local reassignment does not propagate to the caller. When called from `execute_roadmap` this doesn't matter (already resolved), but when called from `_apply_resume_after_spec_patch` (line 2040-2043), the same double-detect pattern exists.

**Required fix:** Remove the auto-detect block from `_build_steps()` entirely. It is dead code in production and misleading in tests. If `_build_steps` is called with `input_type="auto"`, it should raise a `ValueError("input_type must be resolved before calling _build_steps")`.

---

### C-93 [TDD/PRD] MINOR -- Test docstring claims "5 comparison dimensions" but prompt now has 11

**File:** `tests/roadmap/test_spec_fidelity.py:102-111`

`test_spec_fidelity_prompt_comparison_dimensions` docstring says "Prompt includes all 5 comparison dimensions" but `build_spec_fidelity_prompt` now defines 11 dimensions (Signatures, Data Models, Gates, CLI Options, NFRs, Integration Wiring, API Endpoints, Component Inventory, Testing Strategy, Migration & Rollout, Operational Readiness). The test only checks the original 5. The 6 new TDD-derived dimensions are untested.

**Required fix:** Update the docstring to "Prompt includes all 11 comparison dimensions" and add assertions for the 6 new dimensions: `"Integration Wiring"`, `"API Endpoints"`, `"Component Inventory"`, `"Testing Strategy"`, `"Migration"`, `"Operational Readiness"`.

---

### C-94 [TDD/PRD] IMPORTANT -- diff and debate steps do not embed PRD/TDD content

**File:** `src/superclaude/cli/roadmap/executor.py:943-960`

The diff step (line 943-951) and debate step (line 953-962) neither pass PRD/TDD files as `inputs` nor pass them to their prompt builders. This means the comparative analysis and adversarial debate happen without access to the original business context. When the two roadmap variants disagree on prioritization (which PRD persona-based or compliance-based sequencing should break), the debate facilitator has no access to the PRD to resolve the disagreement.

Combined with C-90 (merge has no PRD), this means PRD context is entirely absent from the diff->debate->merge pipeline segment. Only extract, generate, score, spec-fidelity, and test-strategy see PRD content.

**Required fix:** At minimum, add `prd_file` to the debate step's `inputs` list and extend `build_debate_prompt()` with a conditional PRD block instructing the facilitator to use persona/compliance/business-value context when resolving disputes. The diff step is less critical since it only identifies differences, not resolves them.

---

### C-95 [PRE-EXISTING] IMPORTANT -- fidelity_checker.py scans only Python files, misses JS/TS/Go/Rust

**File:** `src/superclaude/cli/roadmap/fidelity_checker.py:121-143`

`_scan_codebase()` only searches `*.py` files via `self.source_dir.rglob("*.py")`. The fidelity checker verifies that spec FRs have corresponding implementation evidence in the codebase, but any project using JavaScript, TypeScript, Go, Rust, or other languages will report 100% gaps. The TDD template explicitly supports multi-language projects (API Specifications can be REST/GraphQL in any language, Component Inventory includes React/Vue components).

The AST-based extraction at line 126-129 is Python-specific (`ast.parse`), but the regex fallback at line 136 (`_CODE_DEF_RE = r"(?:def|class)\s+(\w{4,})"`) is also Python-specific and won't match JS `function`, `const`, Go `func`, or Rust `fn`/`struct` patterns.

**Required fix:** Either extend `_scan_codebase()` to glob for common file types (`*.js`, `*.ts`, `*.go`, `*.rs`, `*.java`) with language-appropriate name extraction regexes, or clearly document that the fidelity checker is Python-only and surface this limitation in the convergence report.

---

### C-96 [PRE-EXISTING] IMPORTANT -- fidelity_checker: partial-match FR marked as found=True silently swallows gaps

**File:** `src/superclaude/cli/roadmap/fidelity_checker.py:253-270`

When a FR has 3 expected names and only 1 is found in the codebase, the checker marks `found=True` with `ambiguous=True` (line 255-269). The `check_as_findings()` method at line 300 then skips it entirely (`if r.found: continue`). This means a FR with 33% implementation evidence is reported as fully implemented. The fail-open policy (line 19-20) is appropriate for genuinely ambiguous FRs (no extractable names), but extending it to partial matches silently swallows real gaps.

**Required fix:** Distinguish between "no extractable names" (legitimate ambiguity, fail-open correct) and "partial evidence" (real gap). Partial-evidence FRs should be reported as findings with MEDIUM severity, not silently passed.

---

### C-97 [PRE-EXISTING] MINOR -- fidelity_checker: _STOP_WORDS contains "sets" but not "set"

**File:** `src/superclaude/cli/roadmap/fidelity_checker.py:57-66`

The stop words list includes `"sets"` (plural) but not `"set"` (singular). A function named `set` would be filtered, but `set` as a Python built-in is 3 characters and would be caught by the `\w{3,}` regex minimum. However, `"sets"` being a stop word while `"set"` is not is inconsistent. More importantly, the stop words include `"file"`, `"path"`, `"data"`, `"name"` -- all of which are legitimate Python function/class name components (e.g., `filepath`, `dataset`). But these are only matched as exact whole words, so compound names are safe. The stop word `"function"` could suppress a legitimate class named `Function`.

**Required fix:** Review stop words for false-positive risk. At minimum, remove `"function"` (legitimate class name in AST libraries). Add `"set"` for consistency with `"sets"`.

---

### C-98 [TDD/PRD] MINOR -- build_extract_prompt and build_extract_prompt_tdd have identical PRD blocks (copy-paste)

**File:** `src/superclaude/cli/roadmap/prompts.py:160-179` and `310-329`

The PRD supplementary block in `build_extract_prompt` (lines 160-179) and `build_extract_prompt_tdd` (lines 310-329) are nearly identical -- same 5 numbered items, same section references (S19, S7, S12, S17, S6), same advisory disclaimer. The only difference is line 163 says "the specification" while line 313 says "the TDD". This duplication means any future PRD block update must be applied in both places. Since the `tdd_file` parameter is already unused in both functions (C-05), the PRD block is the only conditional block, making the duplication more prominent.

**Required fix:** Extract the PRD supplementary block into a shared `_PRD_SUPPLEMENTARY_BLOCK` constant (similar to `_INTEGRATION_ENUMERATION_BLOCK`) with a `{primary_doc_name}` placeholder. Both functions reference the constant with their appropriate document name.

---

### C-99 [PRE-EXISTING] MINOR -- _derive_fidelity_status uses string search instead of YAML parsing

**File:** `src/superclaude/cli/roadmap/executor.py:1500-1505`

`_derive_fidelity_status()` checks for `"validation_complete: false" in content` using raw string matching instead of parsing the YAML frontmatter. If the markdown body contains the literal text "validation_complete: false" (e.g., in a quote block explaining what degraded mode means -- as `generate_degraded_report` at line 1540 does include prose about `validation_complete=false`), this could produce a false positive. The function at line 1503 reads the entire file and searches the full content, not just the frontmatter section.

**Required fix:** Use `_parse_frontmatter()` (already available in gates.py) to extract the YAML frontmatter, then check the parsed value of `validation_complete`.

---

### C-100 [PRE-EXISTING] MINOR -- Sprint executor does not read .roadmap-state.json

**File:** `src/superclaude/cli/sprint/executor.py`

Grep for `roadmap.state`, `.roadmap-state`, and `read_state` returned no matches in the sprint executor. The sprint runner operates on tasklist bundles generated from roadmaps but does not consult the `.roadmap-state.json` for TDD/PRD context. This means `superclaude sprint run` cannot auto-wire TDD/PRD files for enriched task execution, even though the tasklist protocol (SKILL.md section 3.x) describes source document enrichment. The sprint executor is decoupled from the roadmap state entirely.

**Required fix:** If sprint tasks would benefit from TDD/PRD context (e.g., for acceptance criteria enrichment), add optional `.roadmap-state.json` consumption to the sprint executor. If sprint intentionally operates without this context, document this as a design decision.

---

## Summary

| # | ID | Tag | Severity | Location | Issue |
|---|-----|-----|----------|----------|-------|
| 1 | C-90 | TDD/PRD | IMPORTANT | prompts.py:505, executor.py:974 | Merge step has no PRD context |
| 2 | C-91 | TDD/PRD | IMPORTANT | executor.py:1680-1766 | _restore_from_state ignores input_type |
| 3 | C-92 | TDD/PRD | IMPORTANT | executor.py:852-859, 1821 | Double auto-detect in _build_steps (dead code) |
| 4 | C-93 | TDD/PRD | MINOR | test_spec_fidelity.py:102-111 | Test claims 5 dimensions, prompt has 11 |
| 5 | C-94 | TDD/PRD | IMPORTANT | executor.py:943-960 | Diff/debate steps lack PRD/TDD context |
| 6 | C-95 | PRE-EXISTING | IMPORTANT | fidelity_checker.py:121-143 | Codebase scan Python-only |
| 7 | C-96 | PRE-EXISTING | IMPORTANT | fidelity_checker.py:253-270 | Partial FR match silently passes |
| 8 | C-97 | PRE-EXISTING | MINOR | fidelity_checker.py:57-66 | Stop words inconsistency |
| 9 | C-98 | TDD/PRD | MINOR | prompts.py:160-179, 310-329 | Duplicate PRD blocks |
| 10 | C-99 | PRE-EXISTING | MINOR | executor.py:1500-1505 | String search instead of YAML parse |
| 11 | C-100 | PRE-EXISTING | MINOR | sprint/executor.py | Sprint executor ignores roadmap state |

**Totals:**
- CRITICAL: 0
- IMPORTANT: 6 (C-90, C-91, C-92, C-94, C-95, C-96)
- MINOR: 5 (C-93, C-97, C-98, C-99, C-100)
- TDD/PRD-specific: 6 (C-90, C-91, C-92, C-93, C-94, C-98)
- PRE-EXISTING: 5 (C-95, C-96, C-97, C-99, C-100)

## QA Complete
