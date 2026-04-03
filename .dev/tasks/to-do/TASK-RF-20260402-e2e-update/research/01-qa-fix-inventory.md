# Research: QA Fix Inventory
**Topic type:** File Inventory + Doc Cross-Validator
**Scope:** QA findings and fix documentation
**Status:** Complete
**Date:** 2026-04-02
---

## CRITICAL FIXED (3 findings)

| Finding ID | What Was Broken | Fix Applied | Source Files Changed | E2E Behavior Change |
|---|---|---|---|---|
| C-04 | `build_generate_prompt` ignored TDD extraction sections entirely — no body section descriptions, no TDD supplementary block | Added 8 standard body section descriptions (always present) + TDD supplementary block with 6 frontmatter fields and 6 body section descriptions (conditional on `tdd_file`) | `src/superclaude/cli/roadmap/prompts.py` | **Phase 4 (TDD+PRD pipeline):** Generate step now produces TDD-aware prompts with section descriptions. Extraction output quality changes. |
| C-12 | Detection rule divergence between CLI (weighted 4-signal scoring, threshold >= 5) and skill layer docs (different/vague rules) | Updated 3 skill docs to match CLI weighted scoring algorithm: full algorithm in scoring.md, summary with cross-ref in extraction-pipeline.md, inline algorithm in spec-panel.md | `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`, `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`, `src/superclaude/commands/spec-panel.md`, `.claude/` copies via sync | **Phase 2 (PRD fixture):** Detection behavior unchanged (CLI was already correct), but skill docs now match — affects any agent-layer detection reasoning. |
| C-62 | `input_type` value "auto" was written to state file instead of the resolved value ("spec" or "tdd") | Resolved `input_type` in `execute_roadmap()` before `_build_steps()`, so state file always stores resolved value | `src/superclaude/cli/roadmap/executor.py` | **Phase 6 (auto-wire):** State file now contains resolved `input_type` ("spec" or "tdd"), not "auto". Resume and auto-wire read correct type. |

## IMPORTANT FIXED (16 findings)

| Finding ID | What Was Broken | Fix Applied | Source Files Changed | E2E Behavior Change |
|---|---|---|---|---|
| C-03 | `build_spec_fidelity_prompt` always emitted dims 7-11 (TDD-specific) even for spec-only runs | Made dims 7-11 conditional on `tdd_file is not None`. Spec-only: 6 dims. TDD: 11. PRD adds 12-15. | `src/superclaude/cli/roadmap/prompts.py` | **Phase 4/5:** Fidelity scoring now has correct dimension count per input type. Comparison output structure changes. |
| C-05 | `tdd_file` parameter was accepted but unused (dead) in 5 of 6 prompt builders | Added TDD supplementary blocks to `build_extract_prompt`, `build_extract_prompt_tdd`, `build_score_prompt`, `build_test_strategy_prompt` | `src/superclaude/cli/roadmap/prompts.py` | **Phase 4:** All prompt builders now incorporate TDD context when present. Extraction, scoring, and test strategy outputs all change for TDD runs. |
| C-06 | `build_merge_prompt` had no PRD/TDD awareness at all | Added `tdd_file`/`prd_file` params + conditional blocks. Updated executor merge step to pass files. TDD block preserves identifiers; PRD block maintains personas/metrics/compliance. | `src/superclaude/cli/roadmap/prompts.py`, `src/superclaude/cli/roadmap/executor.py` | **Phase 4/5:** Merge step now produces TDD/PRD-aware merged output. |
| C-08 | `_restore_from_state` had incorrect TDD fallback logic (used spec_file as tdd_file) which was also dead code due to redundancy guard | Removed the incorrect fallback. When `input_type=tdd`, `spec_file` IS the TDD — no supplementary tdd_file needed. Added explanatory comment. | `src/superclaude/cli/roadmap/executor.py` | **Phase 6 (auto-wire):** Resume path no longer sets spurious tdd_file. Cleaner state restoration. |
| C-16 | No tests existed for `build_extract_prompt_tdd` with `prd_file`, or for merge prompt with TDD+PRD | Added `TestExtractPromptTddWithPrd` (6 tests) and `TestMergePromptTddPrd` (4 tests) | `tests/cli/test_tdd_extract_prompt.py` (or similar test file) | **No direct E2E behavior change** — test coverage only. Validates Phase 4 prompt correctness. |
| C-17 | No tests for backward compatibility with old-schema state files | Added `TestOldSchemaStateBackwardCompat` (2 tests): old state loads, `_restore_from_state` doesn't crash | Test files | **No direct E2E behavior change** — test coverage for Phase 6 resume robustness. |
| C-25 | `_embed_inputs` labeled files by path only — no semantic role markers (spec vs TDD vs PRD) | Added optional `labels` dict to `_embed_inputs`. `roadmap_run_step` builds labels from `RoadmapConfig`. | `src/superclaude/cli/roadmap/executor.py` | **Phase 3-5:** Embedded input blocks now carry semantic labels ("Primary input - spec", "TDD - supplementary technical context", "PRD - supplementary business context"). LLM sees clearer context. |
| C-27 | `--resume` with `--prd-file` didn't override the state-restored prd_file | Added else branch in `_restore_from_state`: explicit `--prd-file` overrides state, logs if different | `src/superclaude/cli/roadmap/executor.py` | **Phase 6 (auto-wire):** Users can now override PRD file on resume. |
| C-50 | No logging of TDD/PRD decision outcomes during execution | Added `log.info` calls for `tdd_file`, `prd_file`, and `input_type` resolution in `execute_roadmap` | `src/superclaude/cli/roadmap/executor.py` | **Phase 3 (dry-run) and Phase 4/5:** Log output now shows TDD/PRD resolution decisions. Dry-run output more informative. |
| C-61 | TDD template sentinel said complexity fields "may remain empty" but gate expected values | Clarified text: "computed by sc:roadmap, provide estimated values if known" | TDD template file(s) | **Phase 2:** TDD fixture template guidance is clearer. Affects test fixture preparation. |
| C-84 | Dead auto-detection code block remained in `_build_steps` after C-62 moved detection to `execute_roadmap` | Removed dead auto-detection block from `_build_steps` | `src/superclaude/cli/roadmap/executor.py` | **No direct E2E behavior change** — code cleanup. Detection already handled upstream. |
| C-91 | `_restore_from_state` didn't restore `input_type` on `--resume`, causing re-detection | Added `input_type` restoration from state when config has "auto" | `src/superclaude/cli/roadmap/executor.py` | **Phase 6 (auto-wire):** Resume path now preserves original detection result. No re-detection on resume. |
| C-111 | Redundancy guard in `_build_steps` nullified `tdd_file` only in local config — state file saved pre-nullification value | Moved redundancy guard from `_build_steps` to `execute_roadmap` (before `_build_steps` call). State now saves nulled value. | `src/superclaude/cli/roadmap/executor.py` | **Phase 6:** State file correctly reflects nulled tdd_file when redundancy guard fires. |
| C-117 | `EXTRACT_GATE` did not validate TDD-specific frontmatter fields (6 additional fields) | Created `EXTRACT_TDD_GATE` with all 19 fields (13 standard + 6 TDD-specific). Routing: `EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE`. | `src/superclaude/cli/roadmap/gates.py`, `src/superclaude/cli/roadmap/executor.py` | **Phase 4:** TDD extraction now validated against stricter gate (19 fields vs 13). Gate failures will catch missing TDD fields. |
| C-36 | Branch had uncommitted distributable changes (skill/command syncs) | Committed with the batch | Various `.claude/` synced files | **No E2E behavior change** — repo hygiene. |
| C-122 | CLI required single positional arg + explicit `--tdd-file`/`--prd-file` flags; no multi-file auto-detection | This is listed as a separate task (TASK-RF-20260402-auto-detection). The finding triggered a new feature request, not a fix in this QA round. | Pending: `src/superclaude/cli/roadmap/commands.py`, `executor.py` | **Phase 2 future:** Will enable positional multi-file detection. Currently NOT FIXED — drives the auto-detection task. |

**Note on C-122:** This was identified during QA but scoped as a new feature task (TASK-RF-20260402-auto-detection), not a fix. It is NOT FIXED in the current codebase. Included here for completeness since it appears in the findings with a FIXED-adjacent discussion.

## MINOR FIXED (8 findings)

| Finding ID | What Was Broken | Fix Applied | Source Files Changed | E2E Behavior Change |
|---|---|---|---|---|
| C-18 | No explicit detection threshold boundary tests (score=4 vs 5) | Added `TestDetectionThresholdBoundary` (4 tests): score 0/4 = spec, score 5/6 = tdd | Test files | **No direct E2E change** — validates Phase 2 detection boundary. |
| C-20 | Same file could be passed as both `--tdd-file` and `--prd-file` without error | Added same-file guard in `execute_roadmap`: compares resolved paths, exits with error if identical | `src/superclaude/cli/roadmap/executor.py` | **Phase 1 (CLI verification):** New error message when same file passed for both flags. |
| C-75 | `build_tasklist_generate_prompt` referenced wrong PRD sections (S7/S22 instead of S12/S22) | Changed to "S12 (Scope Definition) and S22 (Customer Journey Map)" | `src/superclaude/cli/tasklist/prompts.py` (or equivalent) | **Phase 7 (validation enrichment):** Tasklist prompt now references correct PRD sections. |
| C-88 | Minimal CLI help text for `--tdd-file` and `--prd-file` | Expanded help text with usage context, auto-wire info, and interaction notes | `src/superclaude/cli/roadmap/commands.py` | **Phase 1 (CLI verification):** `--help` output now has richer descriptions for TDD/PRD flags. |
| C-93 | Test docstring claimed "5 comparison dimensions" but prompt has 11+ | Updated docstring to "6 base comparison dimensions (7-11 TDD-conditional, 12-15 PRD-conditional)" | Test file | **No direct E2E change** — documentation accuracy. |
| C-103 | Minimal TDDs below detection threshold produced no borderline warning (scores 3-6) | Added `_log.warning` for scores 3-6 with suggestion to use `--input-type` override | `src/superclaude/cli/roadmap/executor.py` | **Phase 2 (detection):** Borderline TDD documents now produce a warning in logs. |
| C-113 | `effective_input_type` variable was a pointless alias after C-84 removed the code that needed it | Removed `effective_input_type` from `_build_steps`. Uses `config.input_type` directly. | `src/superclaude/cli/roadmap/executor.py` | **No direct E2E change** — code cleanup. |

## NOT-AN-ISSUE / NOT-FOUND (2 findings)

| Finding ID | Status | Reason |
|---|---|---|
| C-11 | NOT FOUND | Grep found no "deferred"/"DEFERRED" text in prompts.py. Likely fixed in earlier edit or false positive. |
| C-119 | NOT AN ISSUE | Only `build_generate_prompt` uses `_INTEGRATION_ENUMERATION_BLOCK`. Ordering (TDD -> PRD -> Integration -> Output) is correct. |

---

## Backlog Items (NOT FIXED)

These items were reviewed during QA and explicitly deferred. They represent known limitations in the current codebase.

### TDD/PRD IMPORTANT Backlog (10 items)

| Finding ID | What It Affects |
|---|---|
| C-19 | No content validation on `--prd-file` / `--tdd-file` (absorbed by C-122 auto-detection task) |
| C-34 | Tests use toy data that can't catch prompt size issues |
| C-35 | PRD prompt section numbers don't match PRD fixture headings |
| C-37 | Validation sub-pipeline has zero TDD/PRD awareness |
| C-38 | Remediation sub-pipeline has zero TDD/PRD awareness |
| C-51 | `spec_patch.py` doesn't handle TDD/PRD file references |
| C-53 | No validation of `--input-type` vs actual file content |
| C-55 | Passing PRD as primary input silently misclassifies (absorbed by C-122) |
| C-57 | Prompt injection via malicious PRD/TDD content — design decision deferred |

### TDD/PRD MINOR Backlog (11 items)

| Finding ID | What It Affects |
|---|---|
| C-13 | Extraction sections mismatch (6 CLI vs 7 skill steps — release_criteria missing) |
| C-21 | Domain keyword dictionary count note (5 vs 7 denominator) |
| C-31 | Test fixture TDD has inconsistent data model field naming |
| C-32 | Test fixtures have conflicting architecture (Redis in TDD, not in spec) |
| C-59 | `spec_type` enum divergence between templates |
| C-60 | Guardrail "do NOT treat PRD as hard requirements" may be ineffective |
| C-87 | Section notation ambiguity (S vs section symbol) in tasklist prompts |
| C-89 | No user-facing documentation for three-way flag interaction |
| C-98 | `build_extract_prompt` and `build_extract_prompt_tdd` have identical PRD blocks (intentional duplication) |
| C-104 | Tasklist fidelity doesn't validate S5-derived priority ordering |
| C-105 | Tasklist fidelity doesn't validate S8/S7 enrichment completeness |

### Deferred Items (3)

| Finding ID | What It Affects | Why Deferred |
|---|---|---|
| D-01 | No `superclaude tasklist generate` CLI | Requires own project (620-880 lines) |
| D-02 | Fingerprint threshold calibration | Needs empirical data from multiple runs |
| S-01 | P3 supplementary blocks for diff/debate prompts | Low value — diminishing returns |

### Pre-Existing Issues (62 total, NONE fixed in this QA round)

All 62 pre-existing issues remain unfixed. They existed before TDD/PRD integration and were not in scope for this QA round. The consolidated findings file lists them in full. Key categories:
- **9 CRITICAL pre-existing:** Gate field mismatches (C-01, C-80), parser regex bugs (C-22, C-23, C-24, C-81), state validation (C-46), dead semantic layer (C-79), anti-instinct gate blocking (C-02), plus C-14 and C-15 moved from TDD/PRD.
- **25 IMPORTANT pre-existing:** State management, embed size limits, fidelity checker, convergence handler stubs, frontmatter parsing, Makefile, imports.
- **27 MINOR pre-existing:** Dead code, formatting, encoding, test gaps, documentation.

---

## Impact on E2E Test Expectations

### Phase 1 (CLI verification)
- **C-88 FIXED:** `--help` output changed — expanded descriptions for `--tdd-file` and `--prd-file` flags. E2E help text assertions may need updating.
- **C-20 FIXED:** New error case — same file for `--tdd-file` and `--prd-file` now produces an error exit. New negative test case available.

### Phase 2 (PRD fixture / detection)
- **C-12 FIXED:** Skill docs updated but CLI detection logic unchanged. No behavioral change to detection itself.
- **C-103 FIXED:** Borderline scores (3-6) now produce a warning log line. E2E log assertions could check for this.
- **C-61 FIXED:** TDD template sentinel text changed. If E2E uses the template, text differs.

### Phase 3 (dry-run)
- **C-50 FIXED:** Dry-run output now includes `log.info` lines for tdd_file, prd_file, and input_type resolution. Log output has additional lines.
- **C-25 FIXED:** Embedded input blocks carry semantic labels. Dry-run prompt preview (if shown) will include labels.

### Phase 4 (TDD+PRD pipeline)
- **C-04 FIXED (CRITICAL):** Generate prompt now has body section descriptions + TDD supplementary block. Prompt content substantially different from original E2E baseline.
- **C-05 FIXED:** All 4 remaining prompt builders have TDD blocks. Extract, score, test strategy prompts all changed.
- **C-06 FIXED:** Merge prompt now TDD/PRD-aware. Merge step output changes.
- **C-03 FIXED:** Fidelity dimensions conditional. TDD runs: 11 dims. Spec-only: 6 dims.
- **C-117 FIXED:** TDD extraction uses `EXTRACT_TDD_GATE` (19 fields) instead of `EXTRACT_GATE` (13 fields). Gate validation is stricter for TDD path.

### Phase 5 (spec+PRD pipeline)
- **C-03, C-05, C-06:** Same prompt changes apply to spec path when PRD is present. Fidelity has 6 base dims + PRD dims 12-15.

### Phase 6 (auto-wire / resume)
- **C-62 FIXED (CRITICAL):** State file stores resolved input_type, not "auto". State file content changed.
- **C-91 FIXED:** Resume restores input_type from state. No re-detection on resume.
- **C-111 FIXED:** Redundancy guard fires before state save. State file correctly reflects nulled tdd_file.
- **C-08 FIXED:** No spurious tdd_file on resume for TDD input type.
- **C-27 FIXED:** `--prd-file` overrides state-restored value on resume.
- **C-84 FIXED:** Dead code removed from `_build_steps`. No behavior change but code path is cleaner.
- **C-113 FIXED:** `effective_input_type` alias removed. No behavior change.

### Phase 7 (validation enrichment / tasklist)
- **C-75 FIXED:** Tasklist generate prompt references correct PRD sections (S12/S22 instead of S7/S22). Tasklist output quality may differ.

### Phase 8-9 (comparison / baseline)
- **C-03 FIXED:** Comparison dimension count is now conditional (6/11/15). Baseline comparison outputs will differ from pre-fix runs.
- **C-93 FIXED:** Test docstring only — no output change.

### Phase 10-11 (report / completion)
- No direct fixes affecting report generation or completion steps.
- However, upstream changes in Phase 4-6 (prompt quality, gate strictness, state correctness) will cascade to produce different final outputs.

---

## Source File Change Summary

Files modified during QA fix rounds (source of truth locations):

| File | Findings Fixed | Primary Impact |
|---|---|---|
| `src/superclaude/cli/roadmap/prompts.py` | C-04, C-03, C-05, C-06 | All 6 prompt builders now TDD/PRD-aware |
| `src/superclaude/cli/roadmap/executor.py` | C-62, C-08, C-25, C-27, C-50, C-84, C-91, C-111, C-113, C-20, C-103 | Detection, state, resume, logging, guards |
| `src/superclaude/cli/roadmap/gates.py` | C-117 | New EXTRACT_TDD_GATE |
| `src/superclaude/cli/roadmap/commands.py` | C-88 | Help text expansion |
| `src/superclaude/cli/tasklist/prompts.py` | C-75 | PRD section references |
| `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` | C-12 | Detection rule alignment |
| `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | C-12 | Detection rule alignment |
| `src/superclaude/commands/spec-panel.md` | C-12 | Detection rule alignment |
| TDD template file(s) | C-61 | Sentinel text clarification |
| Test files | C-16, C-17, C-18, C-93 | New tests + docstring fixes |

---

## Summary Statistics

| Category | Count | Details |
|---|---|---|
| **CRITICAL FIXED** | 3 | C-04, C-12, C-62 |
| **IMPORTANT FIXED** | 15 | C-03, C-05, C-06, C-08, C-16, C-17, C-25, C-27, C-36, C-50, C-61, C-84, C-91, C-111, C-117 |
| **MINOR FIXED** | 8 | C-18, C-20, C-75, C-88, C-93, C-103, C-113 (C-93 is docstring only) |
| **NOT AN ISSUE** | 2 | C-11, C-119 |
| **TDD/PRD BACKLOG** | 21 | 10 IMPORTANT + 11 MINOR |
| **DEFERRED** | 3 | D-01, D-02, S-01 |
| **PRE-EXISTING (untouched)** | 62 | 9 CRITICAL + 25 IMPORTANT + 27 MINOR + 1 META |
| **Total findings reviewed** | ~115 | From 123 original IDs (some merged/absorbed) |

**Total FIXED in QA rounds: 26 findings** (3 CRITICAL + 15 IMPORTANT + 8 MINOR)

**Highest-impact fixes for E2E:** C-04 (generate prompt), C-62 (state file), C-117 (TDD gate), C-03 (fidelity dims), C-05/C-06 (all prompt builders)
