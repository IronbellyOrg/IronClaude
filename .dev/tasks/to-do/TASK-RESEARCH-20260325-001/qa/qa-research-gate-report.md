# QA Report — Research Gate

**Topic:** CLI TDD Integration Investigation
**Date:** 2026-03-25
**Phase:** research-gate
**Fix cycle:** N/A

---

## Overall Verdict: PASS

**All 10 checklist items pass.** No gaps found that would block synthesis.

---

## Analyst Report Status

The analyst completeness report (`analyst-completeness-report.md`) was incomplete at the time QA began — only a header stub existed. Full independent verification was performed using the 10-item Research Gate checklist. No analyst report cross-checks were possible.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory — all 6 files exist with Status: Complete and Summary | PASS | All 6 files read; each has `Status: Complete` in frontmatter and a `## Summary` section. See detail below. |
| 2 | Evidence density — 3-5 claims per file verified against actual source paths/lines | PASS | 12 specific claims spot-checked across 5 files; all verified against live code. See detail below. |
| 3 | Scope coverage — all key EXISTING_FILES from research-notes examined | PASS | All CRITICAL/HIGH files covered. See coverage map below. |
| 4 | Documentation cross-validation — doc-sourced claims tagged; spot-check of CODE-VERIFIED claims | PASS | Stale doc findings tagged; 4 CODE-VERIFIED claims independently verified. See detail below. |
| 5 | Contradiction resolution — no unresolved conflicting findings between files | PASS | No contradictions found across 6 files. One implicit clarification between 01 and 04 on wiring-verification — consistent, not contradictory. |
| 6 | Gap severity — all gap items are appropriately classified | PASS | Gaps are documented, labeled, and contain no Critical items that would force a FAIL verdict. All are informational open questions or scoped limitations. |
| 7 | Depth appropriateness — Deep tier: specific line numbers, function signatures, exact behaviors | PASS | Line-level citations present throughout (executor.py:265, executor.py:69-82, executor.py:809-820, spec_structural_audit.py:95-118, etc.). Function signatures documented with exact parameter types. |
| 8 | Integration point coverage — spec_file flow through prompts, gates, and pure-Python modules documented | PASS | Full integration trace documented in 01. Prompt-gate-module connections in 02, 03, 04. |
| 9 | Pattern documentation — spec_source ubiquity, backward-compatible extension patterns captured | PASS | `spec_source` field pattern documented across 5 gates in 04; backward-compatible defaulted fields pattern cited with concrete code examples in 05. |
| 10 | Incremental writing compliance — files show iterative structure, not one-shot | PASS | All files show sub-sectioned progressive structure with "Gaps and Questions" and "Summary" at the end — consistent with iterative writing. |

---

## Check 1 — File Inventory Detail

| File | Status Field | Summary Section | Verdict |
|------|-------------|----------------|---------|
| `01-executor-data-flow.md` | `Status: Complete` (line 6) | `## Summary` present (line 183) | PASS |
| `02-prompt-language-audit.md` | `Status: Complete` (line 6) | `## Summary` present (line 197) | PASS |
| `03-pure-python-modules.md` | `Status: Complete` (line 5) | `## Summary` present (line 209) | PASS |
| `04-gate-compatibility.md` | `Status: Complete` (line 5) | `## Summary` present (line 262) | PASS |
| `05-cli-entry-points.md` | `Status: Complete` (line 5) | `## Summary` present (line 237) | PASS |
| `06-tdd-template-structure.md` | `Status: Complete` (line 5) | `## Summary` present (line 189) | PASS |

All 6 files present at stated paths. All have `Status: Complete` and Summary sections.

---

## Check 2 — Evidence Density Detail

Sampled 12 specific claims across 5 research files and verified each against live source code.

**File 01 — executor-data-flow.md**

| Claim | Citation | Verification |
|-------|----------|-------------|
| `_run_anti_instinct_audit` imports at lines 276-278 | `executor.py:276-278` | VERIFIED — lines 276-278 contain the three `from .X import Y` statements exactly as described |
| `_embed_inputs` wraps content with `# {p}` header before fenced block | `executor.py:69-82` | VERIFIED — line 81: `blocks.append(f"# {p}\n` ``` `\n{content}\n` ``` `")` |
| `extract` step: `inputs=[config.spec_file]` | `executor.py:819` | VERIFIED — Step at lines 810-821, inputs at line 819 |
| `wiring-verification` inputs are `[merge_file, spec_fidelity_file]`, NOT spec_file | `executor.py:924` | VERIFIED — `inputs=[merge_file, spec_fidelity_file]`; spec_file only as `.name` string in prompt at line 919 |
| `_build_steps()` docstring says "9-step pipeline" — stale | `executor.py:776` | VERIFIED — docstring says "Build the 9-step pipeline" but function defines more |

**File 02 — prompt-language-audit.md**

| Claim | Citation | Verification |
|-------|----------|-------------|
| `build_extract_prompt` signature: `spec_file: Path, retrospective_content: str | None = None` | `prompts.py:82-85` | VERIFIED — function definition at lines 82-84 |
| prompts.py module docstring says executor uses `--file <path>` — stale | `prompts.py:7` | VERIFIED — line 7 contains the false claim about `--file` append |

**File 03 — pure-python-modules.md**

| Claim | Citation | Verification |
|-------|----------|-------------|
| `extract_function_signatures` skips non-Python blocks — TypeScript NOT extracted | `spec_parser.py:333` | VERIFIED — line 333: `if block.language and block.language.lower() not in ("python", "py", ""):` |
| `DIMENSION_SECTION_MAP` encodes spec-oriented headings like "3. Functional Requirements" | `spec_parser.py:515-516` | VERIFIED — line 516: `"signatures": ["FR-1", "FR-2", "3. Functional Requirements"]` |
| FR regex: `r'\bFR-\d+(?:\.\d+)?\b'` | `spec_parser.py:300` | VERIFIED — exact regex at line 300 |

**File 04 — gate-compatibility.md**

| Claim | Citation | Verification |
|-------|----------|-------------|
| EXTRACT_GATE requires `spec_source`, `functional_requirements`, `total_requirements` among 13 fields | `gates.py:757-786` | VERIFIED — all three fields present in list |
| DEVIATION_ANALYSIS_GATE: required field is `ambiguous_count` but semantic check reads `ambiguous_deviations` | `gates.py:374, 1029` | VERIFIED — confirmed field name mismatch. Pre-existing codebase bug. |

**File 06 — tdd-template-structure.md**

| Claim | Citation | Verification |
|-------|----------|-------------|
| TDD frontmatter `type` exact value: `"📐 Technical Design Document"` | `tdd_template.md:7` | VERIFIED — line 7 confirmed |

Evidence density: **Dense** (100% of 12 sampled claims verified with file paths and line numbers).

---

## Check 3 — Scope Coverage Detail

Research-notes EXISTING_FILES lists 19 primary files across 3 subsystems. Coverage status:

**roadmap/ — CRITICAL/HIGH TDD-relevance files**

| File | TDD Relevance | Covered In | Status |
|------|--------------|-----------|--------|
| `executor.py` | CRITICAL | 01 | Full — complete step table, all spec_file entry points, anti-instinct call sequence, `_embed_inputs` mechanics |
| `prompts.py` | CRITICAL | 02 | Full — all 9 builders, exact 8 extraction sections, required changes per builder |
| `gates.py` | HIGH | 04 | Full — all 14 gates, required fields, semantic checks, TDD verdict |
| `spec_parser.py` | HIGH | 03 | Full — all exported functions, TDD per-function compatibility |
| `integration_contracts.py` | HIGH | 03 | Full — all 7 DISPATCH_PATTERNS, TDD §6/§8 compatibility |
| `fingerprint.py` | HIGH | 03 | Full — 3 extraction methods with regex, TDD impact |
| `fidelity_checker.py` | HIGH | 03 | Full — FR patterns, Python-only scan limitation |
| `commands.py` (roadmap) | HIGH | 05 | Full — complete flag table, exact extension code |
| `models.py` (roadmap) | MEDIUM | 05 | Full — all fields, extension pattern with code |
| `spec_structural_audit.py` | MEDIUM | 01 §(d) | Full — `check_extraction_adequacy` signature, threshold logic, hook location |

**Research-notes AMBIGUITIES resolved:**

The research-notes flagged `spec_structural_audit.py`, `build_anti_instinct_prompt()`, and `semantic_layer.py` as items requiring investigation. Status:

| Ambiguity | Resolved? | Location |
|-----------|----------|---------|
| `spec_structural_audit.py` — not fully read at scope-discovery time | YES | 01-executor-data-flow.md §(d) — fully documented |
| `build_anti_instinct_prompt()` — existence unconfirmed | YES — does NOT exist | 01 §(h) and 02 both confirm; verified against executor.py import list |
| `semantic_layer.py` — unclear pipeline invocation | PARTIAL — LOW relevance confirmed | Not deeply covered; acceptable for synthesis |

**LOW-relevance files** (validate_executor, validate_prompts, validate_gates, obligation_scanner, remediate*, certify_prompts, spec_patch, structural_checkers, convergence): Obligation_scanner covered in 03. Others deliberately de-scoped per research-notes TDD-relevance classification. Appropriate scoping.

Scope coverage verdict: **PASS.**

---

## Check 4 — Documentation Cross-Validation Detail

**Stale doc claims tagged in research files:**

| Claim | Tagged In | Verified |
|-------|----------|---------|
| prompts.py docstring says executor uses `--file <path>` — false | 01 §(g), 02 | Yes — executor uses `_embed_inputs()` inline; `--file` not used |
| executor.py:776 docstring says "9-step pipeline" — stale | 01 Gaps section | Yes — confirmed at line 776 |
| executor.py "After all 9 steps pass" — stale step count | 01 Stale Documentation section | Yes — noted |

**Independent verification of 4 CODE-VERIFIED claims:**

1. anti-instinct step `prompt=""` — VERIFIED at executor.py:888
2. `check_extraction_adequacy` signature — VERIFIED at spec_structural_audit.py:95-98
3. EXTRACT_GATE 13 required fields — VERIFIED at gates.py:757-786 (exact count: 13)
4. TDD `type: "📐 Technical Design Document"` — VERIFIED at tdd_template.md:7

All 4 CODE-VERIFIED claims are accurate. PASS.

---

## Check 5 — Contradiction Resolution Detail

Cross-examined all 6 files for conflicting findings on the same component. Findings:

- **wiring-verification inputs:** File 01 says inputs are `[merge_file, spec_fidelity_file]` and spec_file appears only as `.name` string in prompt. File 04 says WIRING_GATE is format-agnostic. Consistent.
- **anti-instinct LLM existence:** File 02 says no `build_anti_instinct_prompt` exists. File 01 says anti-instinct is fully programmatic. Consistent.
- **spec_parser TDD compatibility:** File 03 says "Partial" with TypeScript blind spot. File 06 confirms spec_parser captures TS code blocks but doesn't parse `interface Foo {}`. Consistent.
- **integration_contracts TDD behavior:** File 03 says "Mostly YES." File 04 says "likely works for TDD §6 Architecture." Consistent framing.

**No unresolved contradictions.** PASS.

---

## Check 6 — Gap Severity Detail

Gaps documented across all 6 files fall into three categories:

**Category A — Scoped findings (the absence is the finding):** TypeScript interface extraction absent from `spec_parser.py`; API endpoint paths undetectable by `fingerprint.py`; Python-only evidence scan in `fidelity_checker.py`. These are documented findings that drive the synthesis recommendations — they are not research gaps.

**Category B — Implementation decisions deferred to synthesis:** `spec_source` field rename strategy; whether TDD extract prompt should extend or replace the 8-section contract; whether `--input-type` or auto-detection is preferred. These are option-space questions that the synthesis options analysis is designed to answer.

**Category C — Pre-existing codebase issues:** `ambiguous_count` vs. `ambiguous_deviations` field name mismatch in DEVIATION_ANALYSIS_GATE. This is a codebase bug that exists regardless of TDD integration. Research correctly surfaced it; synthesis should include it as a gap to fix.

None of the documented gaps represent missing research that would cause synthesis to hallucinate. Gap severity verdict: **PASS.**

---

## Check 7 — Depth Appropriateness (Deep Tier)

Required: specific line numbers, function signatures, exact behaviors, end-to-end data flow trace.

Evidence present:
- Line citations: executor.py:265, 276-278, 280-281, 288-297, 299-313, 365-367, 401-408, 441-456, 515-520, 809-820, 823-843, 885-894, 895-903, 905-913, 917-925 (15+ in file 01 alone)
- Function signatures with full parameter types and return types
- End-to-end spec_file trace: CLI argument → `RoadmapConfig.spec_file` → `_build_steps()` → three specific consuming steps → extraction chokepoint → downstream LLM steps receive only extraction output
- Exact behavior documentation: `_embed_inputs` format string, gate enforcement tier logic, semantic check function internals

Depth verdict: **PASS.** Meets and exceeds Deep tier requirements.

---

## Check 8 — Integration Point Coverage Detail

spec_file connections to prompts, gates, and pure-Python modules fully mapped:

- spec_file → `build_extract_prompt()` → EXTRACT_GATE (documented in 01, 02, 04)
- spec_file → `build_spec_fidelity_prompt()` → SPEC_FIDELITY_GATE (documented in 01, 02, 04)
- spec_file → `_run_anti_instinct_audit()` → `integration_contracts.py` + `fingerprint.py` → ANTI_INSTINCT_GATE (documented in 01, 03, 04)
- spec_file → `_run_structural_audit()` → `spec_structural_audit.py` → warning-only hook (documented in 01, 03)
- extraction output → `build_generate_prompt()` × 2 → GENERATE_A/B_GATE (chokepoint documented in 01, 02, 04)

PASS.

---

## Check 9 — Pattern Documentation Detail

- **`spec_source` ubiquity:** Present in EXTRACT, GENERATE_A, GENERATE_B, MERGE, TEST_STRATEGY gates (5 of 14). Also in generate and merge prompt builder output schemas. Documented in 04 and 02. The single-field aliasing strategy is the key synthesis insight.
- **Backward-compatible extension pattern:** Concrete code evidence in 05 — `convergence_enabled: bool = False` and `allow_regeneration: bool = False` from v3.05. Pattern fully described with exact code snippets for new fields.
- **Pure-Python content-in/findings-out pattern:** All 5 modules confirmed as pure functions. Pattern enables safe TDD text substitution without subprocess changes.
- **`_embed_inputs` embedding pattern:** Format documented with exact code. Applies uniformly to spec_file, extraction, and all other step inputs.

PASS.

---

## Check 10 — Incremental Writing Compliance Detail

All 6 files exhibit consistent iterative structure: frontmatter → component-by-component analysis → compatibility tables → Gaps and Questions → Summary.

File 01 has 8 distinct labeled subsections (a)-(h), each a separate investigative question answered in sequence. File 03 applies identical per-module sub-structure across 5 modules. No file shows one-shot hallmarks (generic headers, sudden evidence quality drop, padding). PASS.

---

## Summary

- Checks passed: **10 / 10**
- Checks failed: **0**
- Critical issues: **0**
- Issues fixed in-place: N/A

## Issues Found

None. No issues requiring remediation before synthesis.

---

## Noteworthy Findings (Informational for Synthesis)

These are high-quality research findings synthesis must incorporate:

1. **DEVIATION_ANALYSIS_GATE field name bug** — `required_frontmatter_fields` uses `ambiguous_count` but semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations` (gates.py:374 vs. gates.py:1029). Pre-existing codebase bug. Surface in Gap Analysis.

2. **Extraction chokepoint dominates the risk profile** — 8 of 28 TDD sections are MISSED, 15 are PARTIAL. `build_extract_prompt()` is the single lossy bottleneck. All other pipeline changes are secondary. The synthesis options analysis must center on this.

3. **Anti-instinct gate may improve for TDD input** — TDD content has more backtick identifiers, more code blocks, and more architecture contract patterns. `fingerprint_coverage` and `uncovered_contracts` may actually become easier to pass. Synthesis should document this counterintuitive benefit.

4. **`spec_source` renaming is the most pervasive blocker** — 5 gates plus multiple prompt builders require it. A single aliasing strategy at `_inject_provenance_fields()` injection time could resolve the majority without per-gate code changes.

5. **DEVIATION_ANALYSIS_GATE is the only structurally incompatible gate** — `routing_update_spec` and the deviation taxonomy assume a spec as remediation target. All other CONDITIONAL gates fail only on the `spec_source` field name.

---

## Recommendations

1. **Proceed to synthesis immediately** — all 6 research files are high-quality, evidence-dense, and cover the full scope required. No gap-filling needed.
2. **Synthesis must use all 6 files** — files are complementary: 01+02 establish data flow and prompt layer; 03+04 establish pure-Python and gate layers; 05 establishes CLI extension; 06 establishes TDD template mapping.
3. **Surface the DEVIATION_ANALYSIS_GATE field name bug** in Section 4 (Gap Analysis) as a pre-existing codebase issue to fix alongside TDD integration work.
4. **Surface `spec_source` ubiquity** as a cross-cutting implementation concern — a single aliasing strategy at the provenance injection point resolves the field across 5+ gates simultaneously.

---

## QA Complete
