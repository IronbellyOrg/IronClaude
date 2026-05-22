# QA Report -- Research Gate

**Topic:** PRD as Supplementary Pipeline Input
**Date:** 2026-03-27
**Phase:** research-gate
**Fix cycle:** N/A
**Analyst report:** None (full independent verification)

---

## Overall Verdict: FAIL

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | FAIL | 5/5 research files exist. File 04 has contradictory status headers (line 4: "In Progress", line 315: "Complete"). Files 01, 02, 03, 05 have Status: Complete and Summary sections. |
| 2 | Evidence density | PASS | Sampled 3-5 claims per file (see Section A below). All cited file paths verified via Glob (16/16 exist). Line number claims spot-checked against source code -- all verified accurate. Evidence density rating: Dense (>80% evidenced across all 5 files). |
| 3 | Scope coverage | PASS | All 16 EXISTING_FILES entries from research-notes.md are discussed in at least one research file. Roadmap CLI files covered by 01+02. Tasklist CLI files covered by 03. Skill/reference layer files covered by 04. PRD/TDD reference materials covered by 05. Prior research reports cited as context in research-notes but not re-audited (correctly -- per research-notes instruction). |
| 4 | Documentation cross-validation | PASS | Doc-sourced claims properly tagged. [CODE-VERIFIED] claims spot-checked: (a) `tdd_file` on `RoadmapConfig` at line 115 -- verified at actual line 115. (b) `--tdd-file` flag in tasklist commands at lines 62-66 -- verified at actual lines 61-66 (off by 1, acceptable). (c) `detect_input_type()` at lines 59-117 -- verified at actual lines 59-119 (close). (d) TDD supplementary block in tasklist prompts at lines 110-123 -- verified at actual lines 110-123 (exact). 2 [UNVERIFIED] tags found (04: scoring formula, PRD template path). 1 [CODE-CONTRADICTED] finding verified (stale RoadmapConfig docstring). |
| 5 | Contradiction resolution | FAIL | CRITICAL contradiction between file 04 and files 01/02/03/research-notes regarding `detect_input_type()`. See Issue #2 below. |
| 6 | Gap severity | FAIL | 19 gaps identified across all 5 files. Multiple gaps would cause synthesis to hallucinate if unresolved. See Issue #3 below. |
| 7 | Depth appropriateness | PASS | Standard tier requires file-level coverage of each component. All 5 research files provide file-level analysis with function signatures, line numbers, and specific change proposals. Depth is appropriate and thorough for Standard tier. |
| 8 | Integration point coverage | PASS | Integration points documented: CLI flag -> model field -> executor wiring -> prompt builder parameter -> conditional prompt block. Flow traced end-to-end for both roadmap (01) and tasklist (03) pipelines. Cross-pipeline interaction (PRD+TDD together) explicitly addressed in 03 Section 3 and 02 gap #2. |
| 9 | Pattern documentation | PASS | TDD supplementary input pattern documented comprehensively in research-notes.md PATTERNS_AND_CONVENTIONS section (5-layer pattern with code references). File 03 traces the full 4-layer flow with code-verified line numbers. Pattern is clear and replicable. |
| 10 | Incremental writing compliance | PASS | Files show iterative structure with section numbering, progressive depth, and growing gap/question sections. File 04 has dual status headers suggesting iterative updates (started as "In Progress", later marked "Complete"). No signs of one-shot generation. |

---

## Summary

- Checks passed: 7 / 10
- Checks failed: 3 (items 1, 5, 6)
- Critical issues: 1
- Important issues: 3
- Minor issues: 2
- Issues fixed in-place: 0

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 04-skill-reference-layer.md:4 | File has contradictory Status headers. Line 4 says "Status: In Progress" but line 315 says "Status: Complete". | Update line 4 to read `**Status:** Complete` to match the final status at line 315. |
| 2 | CRITICAL | 04-skill-reference-layer.md:67-76 | Section 1.3 proposes extending `detect_input_type()` to return `"prd"`, adding `--input-type prd` choice, and creating `build_extract_prompt_prd()`. This DIRECTLY CONTRADICTS the research-notes.md design decision (lines 90-97) which explicitly states: "PRD should follow the simpler tasklist TDD pattern: Optional --prd-file flag, No input_type mode changes, No detect_input_type() changes, No dedicated build_extract_prompt_prd()." Files 01, 02, and 03 all consistently treat PRD as supplementary (not a mode). File 04's Section 1.3 would cause synthesis to produce conflicting implementation guidance. | Remove Section 1.3 entirely from file 04, OR rewrite it to explicitly note that `detect_input_type()` should NOT be changed for PRD (per the established design decision), and that PRD detection is only relevant for the inference-based skill protocol docs (extraction-pipeline.md, scoring.md), NOT for the CLI code. The doc-level detection rule in Section 1.2 is fine for protocol docs, but Section 1.3's code impact claims must be corrected. |
| 3 | IMPORTANT | 04-skill-reference-layer.md:266 | Gap #1 references PRD template at `docs/docs-product/templates/prd_template.md` -- this path does NOT exist. The actual PRD template is at `src/superclaude/examples/prd_template.md` (verified via Glob). File 02 correctly references this path at line 53. | Update all references to the PRD template path in file 04 to use `src/superclaude/examples/prd_template.md`. This includes line 266 and the design decision at line 307. |
| 4 | IMPORTANT | 04-skill-reference-layer.md:273-274 | Gap #5 proposes generalizing `--tdd-file` and `--prd-file` into `--supplementary-file` with auto-detection. This contradicts the research-notes.md design decision (line 92: "Optional --prd-file flag") and introduces scope creep. The research prompt explicitly specifies type-specific flags. | Resolve this gap by documenting the decision: use `--prd-file` (type-specific flag, parallel to `--tdd-file`). Remove the `--supplementary-file` alternative from consideration, or explicitly mark it as "deferred/out-of-scope for this implementation." |
| 5 | IMPORTANT | All files: Gaps and Questions sections | 19 total gaps/questions across 5 research files (01: 6 gaps, 02: 3 gaps, 03: 5 gaps, 04: 7 gaps, 05: 6 gaps). Per research-gate rules, ALL gaps regardless of severity must be resolved before synthesis. Several gaps are decision points that will cause synthesis agents to guess if left unresolved (e.g., "Should PRD flow into spec-fidelity?" in 01 gap #2, "Content embedding vs file reference" in 01 gap #3, "Extraction timing" in 05 gap #2). | Each gap must be resolved with a definitive answer or explicitly deferred as an Open Question for the report. Recommended resolutions for the most impactful gaps: (a) 01 gap #2: YES, PRD flows into spec-fidelity (file 02 already proposes this). (b) 01 gap #3: Use `inputs` file path pattern (per tasklist TDD precedent). (c) 01 gap #4: YES, add to validate command. (d) 04 gap #5: Use `--prd-file` (decided). (e) 05 gap #2: Extract once at pipeline start (efficiency). |
| 6 | MINOR | 02-prompt-enrichment-mapping.md:551-561 | Executor call site line numbers in the "Executor Wiring Changes Required" table are accurate to current code but some are approximate (e.g., line 908 is where `build_generate_prompt` is called, verified). However, the table claims 10 call sites need updating, but actually only the builders that gain `prd_file` parameter need updating. If `build_wiring_verification_prompt` is skipped (as correctly noted), only 9 need updating. The table correctly shows "No change" for wiring-verification. No actual error, just confirming accuracy. | No fix needed -- the table is accurate. Noted for verification completeness. |

---

## Section A: Evidence Density Spot-Checks

### File 01 (Roadmap CLI Integration Points)
| Claim | Source | Verified? |
|-------|--------|-----------|
| `RoadmapConfig` at line 95-115 of `models.py` | `models.py:94-115` | YES -- actual lines 94-115 |
| `tdd_file: Path \| None = None` at line 115 | `models.py:115` | YES -- exact match |
| No `--tdd-file` flag on roadmap `run` command | `commands.py:32-218` (grep) | YES -- no tdd-file option found |
| `_build_steps()` at lines 843-1012 | `executor.py:843-1009` | YES -- close (actual end ~1009) |
| `detect_input_type()` needs NO changes | Design decision in research-notes | YES -- consistent with supplementary approach |

### File 02 (Prompt Enrichment Mapping)
| Claim | Source | Verified? |
|-------|--------|-----------|
| `build_extract_prompt` signature at line 82-85 | `prompts.py:82-85` | YES -- exact match |
| `build_extract_prompt_tdd` at line 161-164 | `prompts.py:161-164` | YES -- exact match |
| PRD template from `src/superclaude/examples/prd_template.md` has 28 sections | Glob confirms file exists; [DOC-SOURCED] | YES (path exists, section count from doc) |
| TDD supplementary block at `tasklist/prompts.py:110-123` | `tasklist/prompts.py:110-123` | YES -- exact match |
| `build_generate_prompt` returns single expression at lines 295-335 | Not separately verified | PLAUSIBLE (file structure supports this claim) |

### File 03 (Tasklist Integration Points)
| Claim | Source | Verified? |
|-------|--------|-----------|
| `--tdd-file` at lines 61-66 of `tasklist/commands.py` | `commands.py:61-66` | YES -- exact match |
| `TasklistValidateConfig.tdd_file` at line 25 | `models.py:25` | YES -- exact match |
| `_build_steps()` TDD wiring at lines 188-211 | `executor.py:188-211` | YES -- exact match |
| `all_inputs.append(config.tdd_file)` at lines 193-194 | `executor.py:193-194` | YES -- exact match |
| `build_tasklist_fidelity_prompt` with `tdd_file` kwarg at line 202 | `executor.py:199-202` | YES -- exact match |

### File 04 (Skill/Reference Layer)
| Claim | Source | Verified? |
|-------|--------|-----------|
| `extraction-pipeline.md` TDD steps 9-15 at lines 143-207 | Not independently verified (large file) | PLAUSIBLE |
| `detect_input_type()` uses weighted scoring with >=5 threshold | `executor.py:59-119` | YES -- verified scoring system with threshold >=5 |
| `tasklist/commands.py` has `--tdd-file` at L62-65 | `commands.py:61-66` | YES -- off by 1 line, acceptable |
| `docs/docs-product/templates/prd_template.md` exists | Glob check | NO -- path does not exist. Actual: `src/superclaude/examples/prd_template.md` |

### File 05 (PRD Content Analysis)
| Claim | Source | Verified? |
|-------|--------|-----------|
| PRD SKILL.md section inventory at lines 996-1085 | [DOC-SOURCED] | PLAUSIBLE (correct file exists) |
| TDD extraction agent at lines 944-978 extracts 5 sections | [DOC-SOURCED] | PLAUSIBLE (correct file exists) |
| `_build_steps()` step definitions at executor lines 882-999 | `executor.py:882-1009` | YES -- verified step definitions in this range |
| TDD `parent_doc` frontmatter field at tdd_template.md line 14 | [DOC-SOURCED] | PLAUSIBLE (file exists) |

---

## Section B: Contradiction Analysis

### CRITICAL: detect_input_type() scope

**File 04 Section 1.3 (lines 67-76)** proposes:
- Extending `detect_input_type()` return type to include `"prd"`
- Adding `--input-type prd` CLI option
- Creating `build_extract_prompt_prd()` function

**Research-notes.md (lines 90-97)** states:
- "No `input_type` mode changes"
- "No `detect_input_type()` changes"
- "No dedicated `build_extract_prompt_prd()`"

**Files 01, 02, 03** all consistently treat PRD as supplementary with no mode changes.

**Verdict:** File 04 Section 1.3 contradicts the established design decision. This is the only cross-file contradiction found. The other files are internally consistent.

### RESOLVED: Step numbering in executor

File 01 (line 258) flags duplicate "Step 8" comments in executor.py. Verified: L977 says "Step 8: Test Strategy" and L987 says "Step 8: Spec Fidelity". This is a genuine stale comment in the source code, correctly identified by the research.

---

## Section C: Gap Inventory and Severity Assessment

### File 01 Gaps (6)
1. Dead `tdd_file` on RoadmapConfig -- MINOR (tech debt, not blocking)
2. PRD scope in downstream steps -- IMPORTANT (decision needed for synthesis)
3. Content embedding vs file reference -- IMPORTANT (architecture decision)
4. `validate` subcommand -- MINOR (can be deferred)
5. State persistence -- MINOR (low priority, correctly identified)
6. Anti-instinct step -- MINOR (optional enhancement)

### File 02 Gaps (3)
1. PRD file embedding scope -- IMPORTANT (token cost decision)
2. PRD+TDD+spec triple input -- MINOR (edge case, recommendation provided)
3. Backward compatibility of refactoring -- MINOR (test guidance, not blocking)

### File 03 Gaps (5)
1. Ordering in all_inputs -- MINOR (cosmetic)
2. Prompt size concern -- MINOR (existing warning handles it)
3. No PRD validation in roadmap pipeline -- Already covered by other files
4. Test coverage -- MINOR (implementation concern, not research gap)
5. PRD section numbering -- MINOR (design preference, recommendation provided)

### File 04 Gaps (7)
1. PRD template structure undefined -- IMPORTANT (wrong path cited; actual template exists and should be read)
2. Detection disambiguation -- MINOR for CLI (only relevant to inference-based protocol)
3. Scoring formula decision -- MINOR (deferred with recommendation)
4. Supplementary task generation weaker for PRDs -- MINOR (correctly identified)
5. CLI flag naming -- IMPORTANT (contradicts design decision; must be resolved as `--prd-file`)
6. spec-panel is inference-only -- MINOR (correctly noted, no code change needed)
7. Circular dependency risk -- MINOR (valid concern, can be Open Question)

### File 05 Gaps (6)
1. PRD file path passing mechanism -- IMPORTANT (overlaps with 01; design decision needed)
2. Extraction timing -- IMPORTANT (architecture decision)
3. Token budget impact -- MINOR (sizing concern)
4. Feature PRD vs Product PRD -- MINOR (graceful handling)
5. PRD staleness -- MINOR (can be Open Question)
6. Tasklist pipeline integration -- Already covered by file 03

**Gaps that would cause synthesis to hallucinate:** Issues #2, #3 from file 01 and #1, #2 from file 05 are decision points. Without resolution, synthesis agents will guess inconsistently. However, the research files DO provide recommendations for each, and the research-notes PATTERNS_AND_CONVENTIONS section provides clear guidance (use `inputs` file path pattern, per tasklist TDD precedent). Synthesis can proceed if it follows the established pattern.

**Revised assessment:** The gaps are predominantly design decisions with clear recommendations provided. The CRITICAL issue is the contradiction in file 04, not the gaps themselves. Most gaps can be carried forward as Open Questions in the report.

---

## Actions Taken

None -- fix_authorization not granted.

---

## Recommendations

Before proceeding to synthesis, the following MUST be resolved:

1. **[CRITICAL] Fix file 04 Section 1.3 contradiction.** Remove or rewrite the `detect_input_type()` extension proposal to align with the established design decision (PRD is supplementary, not a mode). Without this fix, synthesis agents will receive conflicting guidance about whether to propose `detect_input_type()` changes.

2. **[IMPORTANT] Fix file 04 PRD template path.** Change `docs/docs-product/templates/prd_template.md` to `src/superclaude/examples/prd_template.md` throughout file 04.

3. **[IMPORTANT] Resolve file 04 gap #5 (flag naming).** Document the decision: use `--prd-file` (type-specific, parallel to `--tdd-file`). Remove `--supplementary-file` alternative.

4. **[MINOR] Fix file 04 status header.** Change line 4 from "In Progress" to "Complete".

5. **[ADVISORY] Gaps as Open Questions.** The remaining 15 minor gaps across files 01-05 can be carried forward as Open Questions in the synthesis/report. They do not block synthesis because each has a recommended resolution that follows established patterns.

---

## QA Complete
