# Research Completeness Verification

**Topic:** task-builder — PRD pipeline document-step gate-failure hotfix (single track)
**Date:** 2026-06-06
**Files analyzed:** 6 (01-prompts, 02-executor, 03-gates, 04-test-patterns, 05-design-crossval, 06-mdtm-template)
**Depth tier:** Deep (hotfix with 10 ACs across 3 source + 5 test files)

---

## Independent source spot-check (analyst-run, not just trusting research files)

Verified live against `src/superclaude/cli/prd/` this analysis turn:

| Anchor | Research-file claim | Live source | Match |
|---|---|---|---|
| `_STEP_ARTIFACT_FILES` | executor.py:252 | 252 | YES |
| `_resolve_step_content` def | executor.py:266 | 266 | YES |
| `_determine_status` def | executor.py:645 | 645 | YES |
| `_evaluate_gate` def | executor.py:678 | 678 | YES |
| `_persist_step_artifact` def | executor.py:1145 | 1145 | YES |
| `build_scope_discovery_prompt` | prompts.py:110 | 110 | YES |
| `build_research_notes_prompt` | prompts.py:194 | 194 | YES |
| `build_sufficiency_review_prompt` | prompts.py:269 | 269 | YES |
| `build_preparation_prompt` | prompts.py:516 | 516 | YES |
| `build_task_file_prompt` def | prompts.py:359 (pin at 439) | 359 | YES |
| `_today` (helper insertion ref) | prompts.py:50-52 | 50 | YES |
| `OUTPUT FORMAT:` (scope-discovery anchor) | prompts.py:154 | 154 | YES |
| `_check_no_placeholders` | gates.py:64 | 64 | YES |
| `_check_research_notes_sections` | gates.py:121 | 121 | YES |
| research-notes STRICT block | gates.py:331/333 | 331/333 | YES |
| File lengths | 1454 / 1197 / 514 | 1454 / 1197 / 514 | YES |

All independently-checked anchors match the research files exactly. The research is grounded in real current source, not hallucinated line numbers. Live grep also shows gates.py STRICT blocks at L314 and L351 with `required_frontmatter_fields=[]` — consistent with file 02/05's INV-001 evidence that the field is populated-but-dead.

---

## Coverage Audit (11 spawn-prompt criteria)

| # | Criterion | Verdict |
|---|---|---|
| 1 | Source files: current line numbers, signatures, quoted code | PASS |
| 2 | 4 builder pin targets + helper insertion + already-pinned idiom | PASS |
| 3 | `_resolve_step_content` body / len() tiebreak / special cases / anti-widening / zero-match | PASS |
| 4 | `_STEP_ARTIFACT_FILES` quoted + confirmed vs merged-solution mirror (AC2) | PASS |
| 5 | output_text↔gate_content split (INV-010) with exact lines | PASS |
| 6 | INV-001 (`_evaluate_gate` never reads required_frontmatter_fields) | PASS |
| 7 | gates.py `_check_*` convention + wiring + truncation wire/no-wire (INV-002) | PASS |
| 8 | Test patterns: subprocess mocking, fixtures, AC→file→pattern for ALL 10 ACs | PASS |
| 9 | Design cross-validation: code blocks tagged + line-drift table | PASS (one self-status inconsistency, non-blocking) |
| 10 | MDTM Template 02 rules (A3/A4/B2, frontmatter, order, anti-orphaning, L1-L6) | PASS |
| 11 | Surfaced ambiguities specific & actionable for the builder | PASS |

---

## Per-Criterion Findings (with evidence)

### Criterion 1 — Source files: line numbers, signatures, quoted code — PASS
- **File 01** quotes the full signatures of all 4 builders (prompts.py:110-114, 194-198, 269-273, 516-520) with verbatim `def ... -> str:` blocks, plus def/close line ranges and the module-head imports (L13-32). Independently confirmed against live source.
- **File 02** re-confirms every executor anchor with a reconciliation table flagging that BUILD_REQUEST estimates were off ~10-15 lines, and quotes `_resolve_step_content` (266-365), `_STEP_ARTIFACT_FILES` (252-263), `_determine_status` (645-676), `_evaluate_gate` (678-715), `_persist_step_artifact` (1145-1173) verbatim with line prefixes.
- **File 03** quotes gates.py research-notes block (329-346), `_check_research_notes_sections` (110-134), `_check_suggested_phases_detail` (137-154), the convention docstring (14-21).
- All three files explicitly call out that BUILD_REQUEST line estimates were STALE and supply corrected current numbers — exactly what the builder needs.

### Criterion 2 — 4 builder pin targets + helper insertion + already-pinned idiom — PASS
- **Helper insertion point** precisely located: file 01 §3 puts `_artifact_path_for_step` at blank L53 (after `_today()` ends L52, before Stage A banner L55-57); file 05 Claim 1 confirms feasibility under `TYPE_CHECKING` + `from __future__ import annotations` with NO runtime import / no circular import.
- **4 pin injection anchors** given exactly: scope-discovery before `OUTPUT FORMAT:` @L154; research-notes before "Produce a research-notes.md … 7 sections" @L222 (explicitly NOT between frontmatter L224-228); sufficiency-review before `Return JSON:` @L301; preparation before `PREPARATION STEPS:` @L539.
- **Already-pinned idiom** located twice: `Write ... to:` @prompts.py:439 and the cleaner `Output path: {config.<dir> / "<file>.md"}` @prompts.py:887; plus a DO-NOT-TOUCH list of 8 already-pinned builders (439/887/956/1064/1109/1267/1321/1451). This prevents the builder from double-pinning.

### Criterion 3 — `_resolve_step_content` body, tiebreak, special cases, anti-widening, zero-match — PASS
- File 02 §2 quotes the FULL current body 266-365 in four parts: docstring (267-278), anti-widening comment + build-task-file block (288-304), assembly block (306-337), generic dict-keyed path (339-365).
- **`len()` tiebreak** identified in all THREE sites (298-299 build-task-file, 329-330 assembly, 360-361 generic) — file 02 explicitly notes the generic 360-361 is the primary replacement target and flags that the design must clarify whether the special-case copies also migrate (they do NOT, per merged-solution backward-compat + file 05 Claim 6/10).
- **Anti-widening guard** quoted verbatim (289-292) with explanation of what it narrows (task_dir-only glob, no parent.rglob).
- **Zero-match fallback** confirmed: returns `ndjson_text` @365, plus the EARLY fallback @341 when step_id has no dict entry.

### Criterion 4 — `_STEP_ARTIFACT_FILES` quoted + confirmed vs merged-solution mirror (AC2) — PASS
- File 02 §1 quotes the dict verbatim (252-263), enumerates all 8 keys→filenames, and confirms the 8 keys match the merged-solution mirror exactly.
- File 05 Claim 1 provides a key-for-key, value-for-value comparison table vs merged-solution.md:44-53 — **ZERO DRIFT**, so AC2's `test_prompt_executor_mapping_sync` can assert exact equality.
- Both files flag the load-bearing caveat: build-task-file/assembly are DELIBERATELY ABSENT (dynamic filenames; adding them would clobber the authored file) — the AC2 sync test must NOT expect them.

### Criterion 5 — output_text↔gate_content split (INV-010) with exact lines — PASS
- File 02 §3 quotes executor.py:602-637 and gives a precise variable-provenance table: `output_text` from `_extract_text_from_stream_json` @609 → `_determine_status` @618 (sentinel/verdict); `gate_content` from `_resolve_step_content` @613-615 → `_evaluate_gate` @623 AND `_persist_step_artifact` @637.
- File 05 Claim 8 independently corroborates with exact line cites (609/613-615/618/623/645-676), all confirmed CORRECT, and adds the QA-verdict-on-NDJSON detail (669-673) as a second reason the NDJSON channel must survive.
- Both correctly frame the hotfix job as adding a *guard comment/assertion* binding INV-010, not changing behavior.

### Criterion 6 — INV-001 (`_evaluate_gate` never reads required_frontmatter_fields) — PASS
- File 02 §4 quotes `_evaluate_gate` (678-715) verbatim and states grep for `required_frontmatter_fields|frontmatter` returns ZERO hits in executor.py; it reads only `gate.min_lines` + `gate.semantic_checks`.
- File 05 Claim 9 strengthens this with a FULL package grep: definition @ pipeline/models.py:149, 18 population sites in gates.py (3 non-empty), and ZERO read sites anywhere — a confirmed dead constraint. My own live grep corroborates (gates.py L306/312/325/331/349/351 etc.).
- Correctly validates the merged-solution decision to DROP the frontmatter prompt mandate as noise. STRICT-vs-STANDARD clarified as caller HALT-vs-VALIDATION_FAIL response (executor.py:625-628), not a change to what is checked.

### Criterion 7 — `_check_*` convention + wiring + truncation wire/no-wire (INV-002) — PASS
- **Convention** quoted verbatim from gates.py:14-21 module docstring + two signatures (:36, :64) + the `SemanticCheck` dataclass (models.py:82-87); all 10 `_check_*` confirmed as `(content: str) -> bool | str`, return literal `True` / error string, never raise (wrapped by `_safe_check` @257-268). Exactly matches merged-solution's `_check_no_truncation_marker`.
- **Wiring** documented: inline into each gate's `semantic_checks=[...]` via `_make_semantic_check` (271-281); dispatch loop @executor.py:702-712 with `result is not True` → fail; NO per-mode registry; `enforcement_tier` is diagnostics-only.
- **Truncation wire/no-wire (INV-002) RESOLVED-with-flag, not skipped:** file 03 §5 lays out the tension ("STRICT criteria stay UNCHANGED" vs "actually guard at runtime") with evidence on both sides and a clear least-invasive recommendation: define the helper + unit-test it, do NOT mutate any STRICT `semantic_checks` list; if runtime wiring is required the ONLY target is research-notes `semantic_checks` (334-345) and that re-opens the unchanged constraint — surface to design, do not wire silently. This is actionable and correctly flagged. Insertion point also given (Layer 1, between `_check_no_placeholders` end L83 and Layer-2 divider L86).
- **Cross-check:** merged-solution.md does NOT show `_check_no_truncation_marker` being added to any `semantic_checks` list (it only defines the function, §3a) — consistent with file 03's "define but don't wire" reading. The test plan item 3 ("truncation-marker check") is a unit test, reinforcing no-wire. So the conservative reading is well-supported.

### Criterion 8 — Test patterns + AC→file→pattern mapping for ALL 10 ACs — PASS
- File 04 documents: framework (pytest, no unittest), the two PrdConfig construction idioms (direct kwargs @test_prompts.py:107-115; `resolve_config` + patch `.task_dir` @test_executor/test_e2e), `tmp_path` base, the `task_dir` fixture pre-writing parsed-request.json with `"WHERE": ["src/"]`, and the `_isolate_paths` monkeypatch for cwd/home pinning (AC5).
- **Subprocess/stream-json mocking** fully covered: test_executor bypasses subprocess (hand-written output strings); test_e2e patches `PrdClaudeProcess` with a `_mock_process_factory` whose `.wait.side_effect` writes fake output then returns exit code — quoted verbatim (224-253), with `step_overrides` mechanism for forcing per-step output.
- **AC→file→pattern table** present for ALL 10 ACs (§ summary table) mapping each AC to target test file + an existing pattern to mirror (file:line) + notes. Truncation marker string pinned to the real emitted marker `"\n\n[TRUNCATED — file exceeds 50KB inline limit]"` (test_prompts.py:252) for AC9.
- **Critical net-new flag:** file 04 explicitly states `_artifact_path_for_step` (AC2), `_pick_best_candidate` (AC4), `_check_no_truncation_marker` (AC9), and WHERE-recovery/INV-005 DO NOT exist today — these are red-first acceptance tests, not regression guards. This is corroborated by file 05 (net-new symbols) and prevents the builder from mistaking them for existing behavior.

### Criterion 9 — Design cross-validation: tags + line-drift table — PASS (one self-status inconsistency)
- File 05 tags every claim CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED across 11 claims, plus a comprehensive LINE-NUMBER DRIFT TABLE (Claim 11) covering ~22 anchors with Design-cited vs Actual vs Status (✓ / ⚠ stale / off-by-one).
- Contradictions surfaced and bounded as non-blocking: §2a `_STEP_ARTIFACT_PATTERNS` "~252" should be after L263 (off ~12); §2b bounded-WHERE "~339" is actually 347-349 (off ~8); INV-005 comment "290-292" is actually 289-292 (off-by-one); plus a PRE-EXISTING source staleness (executor.py:290 comment says "prompts.py:381" but real write is :439).
- Soft semantic flags surfaced: `build_preparation_prompt` is the weakest pin target (emits only `.preparation-complete`, gate LIGHT min_lines=0); `task_dir.parent` = output root (`.dev/eval-workspaces/`) not git repo root, so WHERE-widening frequently no-ops but FAILS SAFE.
- **NON-BLOCKING DEFECT (flagged):** file 05 header says `Status: In Progress` (line 6) but the body ends `Status: Complete` (line 187) with a full summary. The content is unambiguously complete and thorough; the header field was simply not updated. This is a cosmetic metadata inconsistency, not a content gap — see Compiled Gaps (Minor).

### Criterion 10 — MDTM Template 02 rules — PASS
- File 06 documents the PART 1 (build instructions, L46-870, fully HTML-commented) vs PART 2 (emittable body, L872-1204) split, and that the YAML frontmatter (L1-44) IS emitted.
- **A3** (complete granular breakdown — atomic per file/component/iteration, no bulk ops) and **A4** (enumerate→per-item→consolidate) quoted verbatim (L91-95, L97-116).
- **B2** 6 mandatory elements quoted verbatim with EXACT template field names (Context Reference with WHY / Action with WHY / Output Specification / Integrated Verification / Evidence on Failure Only / Explicit Completion Gate) — and explicitly corrects the brief's "guessed labels" as inexact. A fully-formed real B2 example is dissected element-by-element (§10).
- **Frontmatter fields**: full 28-field table (L1-44) with template values and enum sets (status/type/priority), explicitly noting the ACTUAL set is LARGER than the brief's subset.
- **Section order** (PART 2) enumerated 1-12 with line anchors.
- **Anti-orphaning** documented at BOTH ends: D3 (no checklist items before Phase 1) + E2/E3 (summaries last, top-to-bottom) + I17/Post-Completion ordering (validation items before the final frontmatter→Done checkbox).
- **L1-L6** handoff patterns tabulated (When / Key rule / output dir) plus L7 selection guide and Section M phase-gate composites (M1/M2). This is the deepest of the 6 files and directly drives correct task-file emission.

### Criterion 11 — Surfaced ambiguities specific & actionable — PASS
All three named ambiguities from the spawn prompt are surfaced specifically and actionably, NOT silently skipped:
1. **4-builders-vs-2-real-producers** — file 01 §5 + Summary cross-cutting finding #1: only scope-discovery + research-notes are genuine free-form markdown doc producers; sufficiency-review returns JSON; preparation writes a `.preparation-complete` dotfile. File 05 RISK FLAG independently calls preparation the weakest pin target. Builder is told to decide whether pinning the latter two is meaningful and to verify against executor `_STEP_ARTIFACT_FILES`.
2. **Truncation wiring (INV-002)** — file 03 §5 (detailed above in Criterion 7): tension named, both-sides evidence, least-invasive recommendation, "do not wire silently / surface to design."
3. **task_dir.parent semantics** — file 05 Claim 4 + soft flag: `task_dir.parent` = output root (`.dev/eval-workspaces/`), not git repo root, so `(repo_root / where)` widening usually no-ops under sandbox but FAILS SAFE. File 04 §0 adds the related ambiguity that WHERE must be read INTERNALLY from `parsed-request.json` (signature stays 3-arg), flagged for R5.

Additional actionable ambiguities surfaced beyond the three required: AC10 "no variant files left in WHERE dir" implies recovery MOVES/cleans the variant (file 04 §7 flags confirm-cleanup-semantics); the special-case `len()` loops at 298/329 do NOT migrate to `_pick_best_candidate` (file 02 §2 + file 05 Claim 6/10).

---

## Evidence Quality

| Research File | Evidence quality | Notes |
|---|---|---|
| 01-prompts-builders-inventory | Strong | Every claim cites prompts.py:LINE with quoted signatures; injection anchors exact; DO-NOT-TOUCH list. |
| 02-executor-resolve-and-split | Strong | Full verbatim bodies with line prefixes; reconciliation table; grep-backed INV-001/INV-010. |
| 03-gates-strict-criteria | Strong | Verbatim checks + docstring convention; INV-002 tension explicitly reasoned, not hand-waved. |
| 04-test-patterns-prd | Strong | Copy-ready templates per AC; net-new vs existing table; subprocess mock quoted. |
| 05-design-codeblock-crossvalidation | Strong | Per-claim CODE-VERIFIED tags + 22-row drift table; contradictions bounded as non-blocking. |
| 06-mdtm-template-examples | Strong | Verbatim template rules with line anchors; real example dissected against B2. |

Zero unsupported/vague claims found across all six files. No fabrication detected — every load-bearing claim independently spot-checks against live source.

## Documentation Staleness
The research files THEMSELVES are the cross-validation layer here (file 05 is a dedicated doc cross-validator). All doc-sourced design claims (merged-solution.md code blocks) carry explicit `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` tags. No untagged doc-sourced architectural claim reported as current fact. The four `[CODE-CONTRADICTED — line number]` items are cosmetic line-drift, correctly NOT reported as current fact (they are flagged as needing correction). PASS.

## Completeness (per-file)

| Research File | Status field | Summary | Gaps/Flags | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01 | Complete | Y | Y (cross-cutting findings) | Y | Complete |
| 02 | Complete | Y | Y | Y | Complete |
| 03 | Complete | Y | Y (AMBIGUITY FLAGGED) | Y | Complete |
| 04 | Complete | Y | Y (net-new flags) | Y | Complete |
| 05 | **In Progress (header) / Complete (body)** | Y | Y | Y | Complete-in-content (header stale) |
| 06 | Complete | Y | Y (14 pitfalls) | Y | Complete |

## Contradictions Found (between research files)
**None.** The six files are mutually consistent. Where they overlap (e.g. file 02 and file 05 both cover INV-001/INV-010/the dict mirror; file 01 and file 05 both cover the 4 builders), they agree on line numbers, conclusions, and flags. File 02 §4 even proactively cross-references gates.py for R3, and file 03 §5 cross-references executor.py for R2 — and those cross-references are consistent with the owning files.

## Depth Assessment
**Expected:** Deep (layered hotfix, 3 source + 5 test files, 10 ACs, multiple invariants).
**Achieved:** Deep. Full data-flow traces (INV-010 split provenance table), invariant verification with grep evidence (INV-001), design-vs-code cross-validation with a drift table, per-AC test templates, and complete template-emission rules. Exceeds Standard tier.
**Missing depth elements:** None material.

## Compiled Gaps

### Critical Gaps (block task-file build)
**NONE.** Every spawn-prompt criterion is satisfied with evidence. The three required ambiguities are surfaced and actionable. No fabricated or unverifiable claims. The builder has exact line numbers, verbatim code, injection anchors, an AC→test mapping, and template rules.

### Important Gaps (affect quality — DECISIONS the builder must make, not research failures)
These are correctly-surfaced open decisions the research deliberately defers to the builder/design, not missing research:
- **I-1: Pin sufficiency-review / preparation?** Only 2 of 4 builders are genuine markdown doc producers. Builder must decide whether to pin the JSON producer (sufficiency-review) and the dotfile-marker producer (preparation) at all, or pin a marker path instead. (Source: file 01 §5, file 05 RISK FLAG.)
- **I-2: Wire `_check_no_truncation_marker` or not (INV-002)?** Least-invasive reading = define + unit-test only, do NOT mutate STRICT `semantic_checks`. If runtime wiring is wanted, the only target re-opens the "unchanged" constraint and must be explicitly authorized. (Source: file 03 §5; merged-solution §3a defines-but-does-not-wire.)
- **I-3: WHERE-source for `_resolve_step_content`.** AC3 keeps the 3-arg signature, so WHERE must be read INTERNALLY from `parsed-request.json`, not passed as a 4th arg. (Source: file 04 §0.)
- **I-4: AC10 cleanup semantics.** "No variant files left in WHERE dir" implies recovery MOVES/cleans the variant rather than just reading it — confirm intended semantics; merged-solution's recovery only READS, so this AC may need an explicit cleanup step or a softened assertion. (Source: file 04 §7. **This is the one place where an AC may exceed what the merged-solution design specifies — worth the builder's explicit attention.**)

### Minor Gaps (cosmetic, must still be noted)
- **M-1: File 05 header `Status: In Progress`** while body is `Status: Complete`. Update the header field. Content is complete; this is metadata only.
- **M-2: Design line-drift** (already tabulated in file 05): `_STEP_ARTIFACT_PATTERNS` insert after L263 not ~252; bounded-WHERE at 347-349 not ~339; anti-widening comment 289-292 not 290-292. Builder should use file 05's drift table, not the raw merged-solution line cites.
- **M-3: Pre-existing source staleness** executor.py:290 comment references "prompts.py:381" but the real task-file write is at prompts.py:439. Optional fix; out of strict hotfix scope.

## Recommendations
1. **Proceed to task-file build.** Research is complete, grounded, and mutually consistent. No critical gaps.
2. Carry forward the four Important decisions (I-1..I-4) as explicit Open Questions / decision points in the task file's planning — especially I-4 (AC10 cleanup vs read-only recovery), which is the only spot where an AC may outrun the design.
3. Use file 05's drift table (not merged-solution's raw cites) for all line numbers; the merged-solution code is feasible but its line anchors are stale by ~8-12 lines in two spots.
4. For AC2, assert exact dict equality against `_STEP_ARTIFACT_FILES` (zero drift confirmed) and explicitly exclude build-task-file/assembly.
5. Treat AC2/AC4/AC9 + WHERE-recovery tests as red-first (symbols are net-new) — author tests alongside the impl, not as regression guards over master.
6. (Trivial) Ask file 05's author to flip the header Status field to Complete.

---

## VERDICT: PASS

All 11 spawn-prompt criteria PASS with evidence. Six research files are complete, internally consistent, grounded in current source (independently spot-checked — zero hallucinated anchors), and the merged-solution design is substantially CODE-VERIFIED. No critical gaps block the task-file build.

The only items are: four correctly-surfaced builder DECISIONS (I-1..I-4, not research failures), three cosmetic minors (M-1 file-05 header status, M-2 design line-drift already tabulated, M-3 pre-existing source comment staleness). The single point warranting the builder's explicit attention is **I-4: AC10's "no variant files left" assertion may require cleanup semantics the merged-solution's read-only recovery does not provide** — resolve as an Open Question, do not silently assume cleanup.
