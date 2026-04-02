# Pre-Existing Findings (existed before TDD/PRD changes)

**Source:** Adversarial QA across 14 agents, 7 rounds. Separated from TDD/PRD findings during interactive review.
**Date:** 2026-04-02
**Raw detail:** `consolidated-findings-raw.md` — each finding has full file paths, line numbers, code context, impact analysis, and fix suggestions.
**Agent reports:** `adversarial-qa-agent*.md` (14 files) — original agent analysis with evidence.

> **IMPORTANT:** The descriptions below are summaries only. Full details are in the adversarial QA reports referenced in the Source column. Before fixing any finding, **confirm the issue still exists in the current code** — some may have been resolved by other changes.

---

## CRITICAL (11)

| # | Finding | Source | Raw File Lines | Quick Fix? |
|---|---------|--------|---------------|-----------|
| C-01 | DEVIATION_ANALYSIS_GATE `ambiguous_count` vs `ambiguous_deviations` field mismatch — gate can never pass | Agent2 F-13, TDD E2E B-1 | L13-17 | Yes — one-line rename |
| C-02 | Anti-instinct gate blocks entire downstream pipeline — obligation scanner false positives on "skeleton" descriptions, contract checker matches conceptual mentions | Agent2 F-11/F-17/F-18, TDD E2E #1, PRD E2E #1 | L19-23 | Yes — change to TRAILING mode |
| C-14 | Complexity scoring formula not implemented in CLI — skill defines 5-factor (spec) and 7-factor (TDD) formulas but CLI delegates to LLM freeform | Agent2 F-03 | L93-101 | No — post-extraction computation |
| C-15 | No integration tests for full pipeline data flow (detect→extract→gate→state→auto-wire) for any path | Agent2 F-05 | L103-105 | No — new test suite |
| C-22 | spec_parser requirement ID regex silently drops compound IDs (FR-AUTH-001, FR-AUTH.1) | Agent3 E-01 | L195-199 | No — regex update |
| C-23 | certify_prompts parser regex rejects all structural checker finding IDs (expects F-\d+ but IDs are dimension-type-hash) | Agent3 E-02 | L201-205 | No — regex update |
| C-24 | DIMENSION_SECTION_MAP hardcoded to release-spec numbering — breaks for TDD or non-standard specs | Agent3 E-03 | L207-213 | No — conditional map |
| C-46 | _restore_from_state assigns unvalidated state values to typed fields — malformed state crashes pipeline | Agent5 E-07 | L388-394 | No — type validation |
| C-79 | Semantic layer call-site passes wrong argument types (never executes — dead code path) | Agent9 | L596-600 | Yes — fix args |
| C-80 | _frontmatter_values_non_empty checks ALL fields, not just required — flags optional empty fields as failures | Agent9 | L602-606 | Yes — filter to required |
| C-81 | _parse_frontmatter drops YAML list continuation lines — multi-line lists silently truncated | Agent9 | L608-614 | No — parser fix |

## IMPORTANT (25)

| # | Finding | Source | Raw File Lines | Quick Fix? |
|---|---------|--------|---------------|-----------|
| C-07 | _restore_from_state mutates config directly instead of dataclasses.replace | Agent1 #8 | L49-53 | No — refactor |
| C-09 | read_state doesn't validate JSON is a dict — non-dict JSON causes AttributeError | Agent1 #15 | L61-65 | Yes — isinstance check |
| C-13 | Extraction sections mismatch — CLI has 6 steps, skill layer has 7 (release_criteria missing). Moved from TDD/PRD list — pre-existing parallel implementation divergence. | Agent2 F-02 | L87-91 | No |
| C-26 | Score step prompt exceeds _EMBED_SIZE_LIMIT with real data — warning only, no crash | Agent4 DF-03 | L221-225 | No — fallback mechanism |
| C-28 | _embed_inputs no handling for empty or binary files — crashes on read | Agent4 DF-04 | L233-237 | Yes — add checks |
| C-29 | _save_state writes only after all steps complete — mid-pipeline crash loses all progress | Agent4 DF-06 | L239-245 | No — incremental saves |
| C-30 | Fingerprint extraction ignores file paths, API endpoints, data model field names | Agent3 E-04 | L247-251 | No — extend extraction |
| C-37 | Validation sub-pipeline structural checks only — no source document comparison. Moved from TDD/PRD list — by design, spec-fidelity handles source comparison. | Agent5 E-01 | L328-332 | Not needed |
| C-38 | Remediation sub-pipeline works from deviation report — no direct source file access. Moved from TDD/PRD list — by design, deviation report carries the context. | Agent5 E-02 | L334-338 | Not needed |
| C-39 | Convergence fidelity checker scans hardcoded `src/superclaude` path | Agent5 E-03 | L340-346 | No |
| C-40 | Obligation scanner position calculation matches wrong section (content.find) | Agent5 E-04 | L348-352 | No |
| C-41 | Integration contract coverage has no per-contract filtering | Agent5 E-05 | L354-358 | No |
| C-42 | Obligation scanner discharge check uses substring matching — false positives | Agent5 E-13 | L360-366 | No |
| C-43 | Convergence regression handler is a no-op stub | Agent5 E-06 | L368-372 | No |
| C-44 | _write_convergence_report hardcodes medium/low counts to 0 | Agent5 E-10 | L374-378 | Yes |
| C-45 | Registry not saved on early convergence exit | Agent5 E-24 | L380-386 | No |
| C-51 | spec_patch.py doesn't handle TDD/PRD file references. Moved from TDD/PRD list — spec-patch works from deviation report, not source files. | Agent5 E-09 | L419-423 | Not needed |
| C-52 | _check_cross_file_coherence removes from list during iteration — undefined behavior | Agent5 E-18 | L425-431 | Yes |
| C-57 | Prompt injection via malicious PRD/TDD content. Moved from TDD/PRD list — raw embedding is pre-existing pattern for all inputs. | Agent6 E-07 | L454-457 | Design decision |
| C-63 | Frontmatter regex rejects hyphenated field names (e.g., `success-criteria`) | Agent7 | L515-518 | No |
| C-64 | Frontmatter regex breaks on blank lines within frontmatter | Agent7 | L520-523 | No |
| C-66 | pyproject force-include may double files in wheel | Agent7 | L532-534 | No — audit |
| C-68 | Makefile paths with spaces break | Agent7 | L540-544 | Yes — quote paths |
| C-69 | TaskStatus enum collision/inconsistency | Agent7 | L546-548 | No — audit |
| C-82 | sys.path pollution in main.py | Agent9 I-02 | L616-620 | Yes |
| C-83 | _embed_inputs raises unhandled FileNotFoundError | Agent9 I-03 | L622-626 | Yes — try/except |
| C-95 | fidelity_checker.py scans only Python files — misses non-Python deliverables | Agent11 | L724-728 | No |
| C-96 | fidelity_checker partial-match marks found=True, swallows gaps | Agent11 | L730-733 | No |
| C-107 | remediate_parser overlay regexes hardcode column count | Agent12 | L752-754 | No |
| C-108 | _cross_refs_resolve gate check always returns True — never validates | Agent12 | L756-759 | Yes — implement or remove |

## MINOR (27)

| # | Finding | Source | Raw File Lines | Quick Fix? |
|---|---------|--------|---------------|-----------|
| C-10 | Step numbering comment error | Agent1 #9, Agent2 F-22 | L67-70 | Yes |
| C-33 | _FINDING_COUNTER dead global state | Agent3 E-08 | L265-269 | Yes — remove |
| C-47 | Duplicate _embed_inputs and _sanitize_output implementations (roadmap + validate executors) | Agent5 E-08 | L396-400 | No — extract shared |
| C-48 | _extract_by_section heading level calculation wrong | Agent5 E-19 | L402-405 | No |
| C-49 | spec_structural_audit divides by zero on empty spec | Agent5 E-21 | L407-411 | Yes — guard |
| C-54 | _embed_inputs crashes on UTF-16 encoded files | Agent6 E-03 | L439-442 | Yes — try/except |
| C-56 | No lock mechanism on .roadmap-state.json for concurrent runs | Agent6 E-06 | L449-452 | Doc only |
| C-58 | --agents with empty string crashes | Agent6 E-09 | L459-462 | Yes — validate |
| C-65 | Frontmatter regex false positives on `---` in content body | Agent7 | L525-530 | No |
| C-67 | Makefile .DS_Store causes false sync drift | Agent7 | L536-538 | Yes — exclude |
| C-70 | Parallel executor prints to stdout instead of stderr | Agent7 | L550-552 | Yes — use stderr |
| C-71 | Doctor command missing pipeline health checks | Agent7 | L554-556 | No |
| C-72 | Dead deprecation shim | Agent7 | L558-560 | Yes — remove |
| C-73 | Confidence checker mutates input dict | Agent7 | L562-564 | Yes — copy |
| C-74 | Reflexion creates directories on init (side effect in constructor) | Agent7 | L566-570 | Yes |
| C-76 | Bare f-string prefixes with no interpolation (f"literal" with no {}) | Agent8 M-05/M-06 | L576-578 | Yes |
| C-77 | Cross-module import of private _OUTPUT_FORMAT_BLOCK (tasklist imports from roadmap) | Agent8 M-09 | L580-582 | No — design |
| C-78 | Redundant Path() wrapping on values already typed as Path | Agent8 M-03/M-04 | L584-594 | Yes |
| C-85 | Fidelity batch scripts hardcode container path | Agent9 M-01 | L636-639 | No |
| C-86 | prd/tdd skills lack sc- prefix, bypass duplicate skill filter | Agent9 M-02 | L641-644 | Yes — rename or update filter |
| C-97 | fidelity_checker _STOP_WORDS contains "sets" but not "set" | Agent11 | L735-737 | Yes |
| C-99 | _derive_fidelity_status uses string search instead of YAML parsing | Agent11 | L739-741 | No |
| C-100 | Sprint executor doesn't read .roadmap-state.json — can't inherit pipeline state | Agent11 | L743-746 | No |
| C-106 | _extract_field regex may capture trailing content beyond field value | Agent12 | L748-750 | No |
| C-110 | Gate failure messages lack actual values — just say "field missing" not what was expected | Agent12 | L761-797 | No |
| C-120 | TDD SKILL.md QA checklist item 13 references wrong synthesis file | Agent13 | L824-828 | Yes |
| C-121 | Obligation scanner lowercases component names at extraction — loses case for matching | Agent13 | L830-836 | Yes |

## META (1)

| # | Finding | Source | Raw File Lines |
|---|---------|--------|---------------|
| C-112 | Consolidated report summary counts inconsistent | Agent14 | L838-841 |

---

**Pre-existing total: 11 CRITICAL + 30 IMPORTANT + 27 MINOR + 1 META = 69**

Note: Count increased from original 62 because C-13, C-37, C-38, C-51, C-57 were moved here from TDD/PRD list during interactive review session.
