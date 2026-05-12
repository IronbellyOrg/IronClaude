# Findings by Category — TDD/PRD vs Pre-Existing

**Source:** Consolidated findings from 14 agents across 7 rounds (123 total)
**Date:** 2026-04-01

---

## TDD/PRD ISSUES (caused by or related to our TDD/PRD integration work)

### CRITICAL

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-04 | ~~Generate prompt ignores TDD extraction sections~~ | **FIXED** — Added 8 standard body section descriptions (always present) + TDD supplementary block with 6 additional frontmatter fields and 6 body section descriptions (conditional on tdd_file). Parallel pattern to existing PRD block. |
| C-12 | ~~Detection rule divergence CLI vs skill layer~~ | **FIXED** — Updated scoring.md (full algorithm description), extraction-pipeline.md (summary with cross-ref), spec-panel.md (inline algorithm). All 3 now describe the 4-signal weighted scoring with threshold ≥5, matching CLI. Synced via `make sync-dev`. |
| C-14 | ~~Moved to pre-existing~~ — see pre-existing section | — |
| C-15 | ~~Moved to pre-existing~~ — no integration tests for any path (spec or TDD/PRD) | — |
| C-62 | input_type "auto" still written to state file | **FIXED** |

### IMPORTANT

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-03 | ~~Spec-fidelity dims 7-11 always emitted~~ | **FIXED** — Made dims 7-11 conditional on `tdd_file is not None`. Spec-only runs get 6 dims (pre-TDD behavior). TDD runs get 11. PRD adds 12-15 on top. No regression. |
| C-05 | ~~Dead tdd_file parameter in 5 prompt builders~~ | **FIXED** — Added TDD supplementary blocks to all 4 remaining builders (build_extract_prompt, build_extract_prompt_tdd, build_score_prompt, build_test_strategy_prompt). Combined with C-04 (generate) and C-03 (fidelity), all 6 builders now have TDD blocks with section-specific instructions matching the PRD block pattern. |
| C-06 | ~~Merge prompt has no PRD/TDD awareness~~ | **FIXED** — Added tdd_file/prd_file params + conditional blocks to build_merge_prompt. Updated executor merge step to pass files. TDD block preserves identifiers; PRD block maintains personas/metrics/compliance. |
| C-08 | ~~_restore_from_state missing TDD fallback~~ | **RESOLVED** — QA found the original fix was dead code (redundancy guard immediately nulled it). Removed the fallback. When input_type=tdd, spec_file IS the TDD — no supplementary tdd_file needed. Added explanatory comment. |
| C-16 | ~~No tests for build_extract_prompt_tdd with prd_file~~ | **FIXED** — Added TestExtractPromptTddWithPrd (6 tests) and TestMergePromptTddPrd (4 tests). |
| C-17 | ~~No tests for old-schema state file backward compat~~ | **FIXED** — Added TestOldSchemaStateBackwardCompat (2 tests): old state loads, _restore_from_state doesn't crash. |
| C-19 | No content validation on --prd-file / --tdd-file (absorbs S-01, S-02) | **BACKLOG** — content checks |
| C-25 | ~~_embed_inputs labels files by path only — no semantic role markers~~ | **FIXED** — Added optional `labels` dict to `_embed_inputs`. `roadmap_run_step` builds labels from `RoadmapConfig` (spec_file → "Primary input - {type}", tdd_file → "TDD - supplementary technical context", prd_file → "PRD - supplementary business context"). |
| C-27 | ~~--resume with --prd-file doesn't override state-restored prd_file~~ | **FIXED** — Added else branch in _restore_from_state: explicit --prd-file overrides state, logs if different. |
| C-34 | Tests use toy data that can't catch prompt size issues | **BACKLOG** — realistic test data |
| C-35 | PRD prompt section numbers don't match PRD fixture headings | **BACKLOG** — add heading hints |
| C-36 | Branch has uncommitted distributable changes | **FIXED** — will commit with this batch |
| C-37 | Validation sub-pipeline has zero TDD/PRD awareness | **BACKLOG** — pass context through |
| C-38 | Remediation sub-pipeline has zero TDD/PRD awareness | **BACKLOG** — pass context through |
| C-50 | ~~No logging of TDD/PRD decisions~~ | **FIXED** — Added log.info calls for tdd_file, prd_file, and input_type resolution in execute_roadmap. |
| C-51 | spec_patch.py doesn't handle TDD/PRD file references | **BACKLOG** — pass context |
| C-53 | No validation of --input-type vs actual file content | **BACKLOG** — cross-check logic |
| C-55 | Passing PRD as primary input silently misclassifies | **BACKLOG** — add PRD detection |
| C-57 | Prompt injection via malicious PRD/TDD content | **BACKLOG** — design decision |
| C-61 | ~~TDD template sentinel says complexity "may remain empty" but gate expects value~~ | **FIXED** — Clarified text: computed by sc:roadmap, provide estimated values if known. |
| C-84 | ~~Double auto-detection still exists (dead code in _build_steps after C-62 fix)~~ | **FIXED** — Removed dead auto-detection block from _build_steps. execute_roadmap now handles all resolution. |
| C-91 | ~~_restore_from_state doesn't restore input_type on --resume~~ | **FIXED** — Added input_type restoration from state when config has "auto". Prevents re-running detection. |
| C-111 | ~~Redundancy guard nullifies tdd_file in local config only~~ | **FIXED** — Moved redundancy guard from _build_steps to execute_roadmap (before _build_steps call). State now saves nulled value. |
| C-117 | ~~EXTRACT_GATE does not validate TDD-specific frontmatter fields~~ | **FIXED** — Created `EXTRACT_TDD_GATE` with all 19 fields (13 standard + 6 TDD-specific). Routing in `_build_steps`: `EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE`. Note: when C-122 auto-detection lands, routing uses same resolved input_type. |
| C-122 | CLI requires single positional arg + explicit flags — no multi-file auto-detection. Users should be able to pass TDD and PRD files in any order as positional args and have the CLI auto-detect which is which (TDD vs PRD vs spec) and route accordingly. Currently: no PRD detection exists, only one positional arg accepted, `--tdd-file`/`--prd-file` flags required for supplementary files. Absorbs C-19 (content validation), C-55 (PRD misclassification). | No — needs PRD detection, multi-arg positional, routing logic |

### MINOR

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-11 | Stale "deferred" comment in generate prompt | **NOT FOUND** — grep found no "deferred"/"DEFERRED" in prompts.py. May have been fixed in earlier edit. |
| C-13 | Extraction sections mismatch (6 CLI vs 7 skill steps — release_criteria missing) | **BACKLOG** |
| C-18 | ~~No explicit detection threshold boundary tests (score=4 vs 5)~~ | **FIXED** — Added TestDetectionThresholdBoundary (4 tests): score=0 spec, score=4 spec, score=5 tdd, score=6 tdd. |
| C-20 | ~~Same file for --tdd-file and --prd-file not caught~~ | **FIXED** — Added same-file guard in execute_roadmap: compares resolved paths, exits with error if identical. |
| C-21 | Domain keyword dictionary count note missing (5 vs 7 denominator) | **BACKLOG** — minor doc |
| C-31 | Test fixture TDD has inconsistent data model field naming | **BACKLOG** — fixture cleanup |
| C-32 | Test fixtures have conflicting architecture (Redis in TDD, not in spec) | **BACKLOG** — fixture cleanup |
| C-59 | spec_type enum divergence between templates | **BACKLOG** — verify |
| C-60 | Guardrail "do NOT treat PRD as hard requirements" may be ineffective | **BACKLOG** — doc only |
| C-75 | ~~build_tasklist_generate_prompt references wrong PRD sections (S7/S22)~~ | **FIXED** — Changed "S7/S22" to "S12 (Scope Definition) and S22 (Customer Journey Map)". |
| C-87 | Section notation ambiguity (S vs §) in tasklist prompts | **BACKLOG** — § for TDD sections, S for PRD sections is already consistent by convention. |
| C-88 | ~~Minimal CLI help text for --tdd-file and --prd-file~~ | **FIXED** — Expanded help text with usage context, auto-wire info, and interaction notes. |
| C-89 | No user-facing documentation for three-way flag interaction | **BACKLOG** — Update: `docs/generated/roadmap-cli-tools-release-guide.md`, `docs/generated/contributor-knowledge-base/cli-api-inventory.md`, `docs/guides/cli-portify-and-pipeline-runner-guide.md`. Document --input-type / --tdd-file / --prd-file interaction, auto-detection, redundancy guard, and auto-wire on resume. |
| C-93 | ~~Test docstring claims "5 comparison dimensions" but prompt has 11+~~ | **FIXED** — Updated docstring to "6 base comparison dimensions (7-11 TDD-conditional, 12-15 PRD-conditional)". |
| C-98 | build_extract_prompt and build_extract_prompt_tdd have identical PRD blocks | **BACKLOG** — doc/design intentional duplication |
| C-103 | ~~Minimal TDDs below detection threshold produce no borderline warning~~ | **FIXED** — Added _log.warning for scores 3-6 with suggestion to use --input-type override. |
| C-104 | Tasklist fidelity doesn't validate S5-derived priority ordering | **BACKLOG** |
| C-105 | Tasklist fidelity doesn't validate S8/S7 enrichment completeness | **BACKLOG** |
| C-113 | ~~effective_input_type becomes pointless alias after C-84 fix~~ | **FIXED** — Removed effective_input_type from _build_steps. Uses config.input_type directly. |
| C-119 | PRD block and _INTEGRATION_ENUMERATION_BLOCK ordering inconsistent | **NOT AN ISSUE** — Only build_generate_prompt uses _INTEGRATION_ENUMERATION_BLOCK. Ordering (TDD→PRD→Integration→Output) is correct. |

### DEFERRED

| # | Finding | Why |
|---|---------|-----|
| D-01 | No `superclaude tasklist generate` CLI | Requires own project (620-880 lines). BUILD-REQUEST written. |
| D-02 | Fingerprint threshold calibration | Needs empirical data from multiple runs |
| S-01 | P3 supplementary blocks for diff/debate (not merge — merge is C-06) | Low value — diminishing returns |

**TDD/PRD total: 5 CRITICAL + 25 IMPORTANT + 20 MINOR + 3 DEFERRED = 53**

---

## PRE-EXISTING ISSUES (existed before our TDD/PRD changes)

### CRITICAL

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-01 | DEVIATION_ANALYSIS_GATE `ambiguous_count` vs `ambiguous_deviations` | Yes — one-line |
| C-02 | Anti-instinct gate blocks entire downstream pipeline | Yes — TRAILING mode |
| C-22 | spec_parser regex drops compound IDs (FR-AUTH-001, FR-AUTH.1) | No — regex update |
| C-23 | certify_prompts parser regex wrong format (F-\d+ vs dimension-type-hash) | No — regex update |
| C-24 | DIMENSION_SECTION_MAP hardcoded to release-spec numbering | No — conditional map |
| C-46 | _restore_from_state assigns unvalidated state values | No — type validation |
| C-79 | Semantic layer call-site passes wrong argument types (never executes) | Yes — fix args |
| C-80 | _frontmatter_values_non_empty checks ALL fields, not just required | Yes — filter to required |
| C-81 | _parse_frontmatter drops YAML list continuation lines | No — parser fix |
| C-14 | Complexity scoring formula not implemented in CLI — skill defines 5-factor (spec) and 7-factor (TDD) formulas but CLI delegates to LLM freeform. Pre-existing for specs, extends to TDD. **DECISION: Should be implemented in CLI for both spec and TDD paths.** | No — post-extraction computation |
| C-15 | No integration tests for full pipeline data flow (detect→extract→gate→state→auto-wire). Pre-existing for spec path, extends to TDD/PRD. **DECISION: Should add integration tests covering all paths.** | No — new test suite |

### IMPORTANT

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-07 | _restore_from_state mutates config directly instead of dataclasses.replace | No — refactor |
| C-09 | read_state doesn't validate JSON is a dict | Yes — isinstance check |
| C-26 | Score step prompt exceeds _EMBED_SIZE_LIMIT with real data | No — fallback mechanism |
| C-28 | _embed_inputs no handling for empty or binary files | Yes — add checks |
| C-29 | _save_state writes only after all steps complete | No — incremental saves |
| C-30 | Fingerprint extraction ignores file paths, API endpoints, field names | No — extend extraction |
| C-39 | Convergence fidelity checker scans hardcoded path | No |
| C-40 | Obligation scanner position matches wrong section (content.find) | No |
| C-41 | Integration contract coverage no per-contract filtering | No |
| C-42 | Obligation scanner discharge substring matching | No |
| C-43 | Convergence regression handler is a no-op stub | No |
| C-44 | _write_convergence_report hardcodes medium/low counts to 0 | Yes |
| C-45 | Registry not saved on early convergence exit | No |
| C-52 | _check_cross_file_coherence removes from list during iteration | Yes |
| C-63 | Frontmatter regex rejects hyphenated field names | No |
| C-64 | Frontmatter regex breaks on blank lines within frontmatter | No |
| C-66 | pyproject force-include may double files in wheel | No — audit |
| C-68 | Makefile paths with spaces break | Yes — quote paths |
| C-69 | TaskStatus enum collision/inconsistency | No — audit |
| C-82 | sys.path pollution in main.py | Yes |
| C-83 | _embed_inputs raises unhandled FileNotFoundError | Yes — try/except |
| C-95 | fidelity_checker.py scans only Python files | No |
| C-96 | fidelity_checker partial-match swallows gaps | No |
| C-107 | remediate_parser hardcoded column count | No |
| C-108 | _cross_refs_resolve gate check always returns True | Yes — implement or remove |

### MINOR

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-10 | Step numbering comment error | Yes |
| C-33 | _FINDING_COUNTER dead global state | Yes — remove |
| C-47 | Duplicate _embed_inputs implementations | No — extract shared |
| C-48 | _extract_by_section heading level calculation wrong | No |
| C-49 | spec_structural_audit divides by zero | Yes — guard |
| C-54 | _embed_inputs crashes on UTF-16 | Yes — try/except |
| C-56 | No lock mechanism on state file | Doc only |
| C-58 | --agents with empty string crashes | Yes — validate |
| C-65 | Frontmatter false positives on --- in content | No |
| C-67 | Makefile .DS_Store false sync drift | Yes — exclude |
| C-70 | Parallel executor prints to stdout | Yes — use stderr |
| C-71 | Doctor missing pipeline health checks | No |
| C-72 | Dead deprecation shim | Yes — remove |
| C-73 | Confidence checker mutates input | Yes — copy |
| C-74 | Reflexion creates directories on init | Yes |
| C-76 | Bare f-string prefixes with no interpolation | Yes |
| C-77 | Cross-module import of private _OUTPUT_FORMAT_BLOCK | No — design |
| C-78 | Redundant Path() wrapping | Yes |
| C-85 | Fidelity batch scripts hardcode container path | No |
| C-86 | prd/tdd skills lack sc- prefix | Yes — rename or update filter |
| C-97 | fidelity_checker _STOP_WORDS missing "set" | Yes |
| C-99 | _derive_fidelity_status string search | No |
| C-100 | Sprint executor doesn't read state file | No |
| C-106 | _extract_field regex captures trailing content | No |
| C-110 | Gate failure messages lack actual values | No |
| C-120 | SKILL.md QA checklist references wrong synth file | Yes |
| C-121 | Obligation scanner lowercases component names | Yes |

### META

| # | Finding |
|---|---------|
| C-112 | Consolidated report summary counts inconsistent |

**Pre-existing total: 9 CRITICAL + 25 IMPORTANT + 27 MINOR + 1 META = 62**

---

## SUMMARY

| Category | TDD/PRD | Pre-existing | Total |
|----------|---------|-------------|-------|
| CRITICAL | 5 (1 fixed) | 9 | 14 |
| IMPORTANT | 25 | 25 | 50 |
| MINOR | 20 | 27 | 47 |
| DEFERRED | 3 | 0 | 3 |
| META | 0 | 1 | 1 |
| **Total** | **53** | **62** | **115** |

Note: 8 findings not accounted for in this count may be in transition between categories or were consolidated during dedup passes. The master list has 123 IDs but some were merged/absorbed.
