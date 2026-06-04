# QA Report — Task Integrity Check

**Topic:** Durable fix for ID_PATTERNS ↔ tool-write schema drift (MD family + per-step SoT + assembler + arm-level guard tests)
**Date:** 2026-06-02
**Phase:** task-integrity
**Fix cycle:** N/A (initial pass)
**Task file:** `.dev/tasks/to-do/TASK-RF-20260602-162259/TASK-RF-20260602-162259.md`
**Template:** 02 (complex task)
**Fix authorization:** true (fixed in-place)

---

## Overall Verdict: PASS (2 issues found and FIXED in-place)

Adversarial stance held throughout: every structural claim and every correctness claim was verified against the ACTUAL source files (contracts/__init__.py, the four schema JSONs, the four guard tests, tool_writer.py, the template, the BUILD_REQUEST), not against agent narration. Two genuine defects were found and fixed. Final state PASSES.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS | id/title/status/created_date/type/template_schema_doc/tags/task_type all present + non-empty (L1-51). No checklist items before Phase 1 (D3): Phase 1 @L132, first `- [ ]` @L138 — INFORMATIONAL-ONLY note @L82 confirms no items in Prereqs. |
| 2 | All mandatory template-02 sections present | PASS | Compared task headers vs template PART 2 skeleton: Task Overview, Key Objectives, Prerequisites & Dependencies, Execution Context, Detailed Task Instructions, Post-Completion Actions, Task Log/Notes, Execution Log, per-phase Findings, Phase Gate Findings — all present. |
| 3 | Items self-contained (context+action+output+verification+completion gate, B2) | PASS | Every `- [ ]` item carries embedded context (research §/file:line), action, output path, verification, and the closing "Once done, mark this item as complete." gate. Spot-checked Steps 1.4, 2.1, 3.1, 4.1, 5.5, 6.3, PG.2. |
| 4 | Granularity: contracts / 4 schema regens / 4 guard rebuilds / MD regression / verify each its own item (no batching) | PASS | 4.1 contracts; 4.3/4.4/4.5/4.6 = one schema each; 5.1/5.2/5.3/5.4 = one guard test each; 5.5 = MD regression; 4.2/4.7/5.7/6.1/6.2/6.3 = discrete verifications. No batching. Step 4.1 is the largest (~2923 chars) but is ONE atomic change to ONE module (interdependent registry+map+assembler) — borderline but acceptable, not a violation. |
| 5 | Evidence-based: re-anchor by symbol, reference verified paths | PASS | Phase 2/4/5 headers explicitly instruct "RE-ANCHOR BY SYMBOL/grep ... line numbers may have drifted." Items cite historical lines as advisory (e.g. extract:134, guard 130-143) + symbol re-anchor. All cited paths verified to exist. |
| 6 | No items based on contradicted/unverified findings | PASS | All claims independently re-verified against live source (see Correctness Checks below). Research-gate QA report (PASS 10/10) exists at qa/qa-research-gate-report.md. |
| 7 | Open Questions documented (extract DM keep; widen-map-if-future-fixture) | PASS | Follow-Up Items section L368 records BOTH: extract DM-arm-is-fixture-backed→KEEP, AND widen-map-if-future-fixture-exercises-new-family. |
| 8 | Phase deps logical: Phase 4 gated on Phase 3 decision artifact; no circular | PASS | All 7 Phase 4 items open with "Read the decision artifact ... IF `decision: HALT` ... IF `decision: PROCEED`". 3.1 writes the artifact; Phase 4 consumes it. DAG, no cycle. |
| 9 | Reasonable item count | PASS | 31 checklist items across 6 phases + Phase Gate + Post-Completion. Well within Template-02 complex bounds. |
| TB-Add-1 | Placeholder scan (TBD/TODO/FIXME, title-only) | PASS | 0 TBD/TODO/FIXME in any checklist line. No title-only items. |
| TB-Add-2 | Item count bounds (ADVISORY) | PASS (advisory) | 31 items — within 3..50. Advisory per uncalibrated bounds; no block. |
| TB-Add-3 | Clarification adjacency | PASS (N/A) | No frontmatter Open Questions block; the single Follow-Up note is advisory, no item is blocked-pending-question. |
| TB-Add-4 | Circular dependency (DAG) | PASS | 3.1→4.1→4.2→{4.3,4.4,4.5,4.6}→4.7→Phase5→Phase6→PhaseGate→Post-Completion. Acyclic. |
| TB-Add-5 | Granularity / XL splitting | PASS | Largest item 4.1 is single-file/single-logical-change with rationale (interdependent additions). Others well-scoped. |
| TB-Add-6 | Verify-form consistency | PASS | Every item ends with the "Once done, mark this item as complete." gate; verification embedded as capture-to-file + assertion. Consistent. |
| TB-Add-7 | Exec-Context source-areas-reappear + no file:line in header | **FIXED** | Header had 0 file:line leak (PASS). BUT "the roadmap executor wiring" was named as a Source area and does NOT reappear in any checklist item (executor is BUILD_REQUEST runtime *context* only, never edited). Was header drift. FIXED: removed "executor wiring" from Source areas line (now names tool-writer's `load_schema`/`validate_tool_output` instead). All 5 remaining source areas reappear in items. |
| TB-Add-8 | Per-item Context evidence binding | PASS | Items naming code surfaces carry file:line/symbol anchors (research §1-§4, `:64-77`, historical guard lines, symbol re-anchor). New-surface item 5.5 uses research §4a + "re-anchor by reading existing test functions" — appropriate for new code. |
| C1 | Design is PER-STEP, NOT flat | PASS | Task explicitly requires `roadmap_ids_pattern(step)` keyed on `TOOL_WRITE_ROADMAP_ID_FAMILIES[step]`; 3 occurrences of "per-step-aware / flat pattern REJECTED". extract={COMP,DM}, extract_tdd adds {DM,API,COMP,TEST,MIG,OPS}, generate/merge add OQ. Matches live schemas. |
| C2 | MD added to ALL FOUR schemas | PASS | MD arm `M\\d+-D-?\\d+` required in exactly the 4 Phase 4 schema items (4.3-4.6). Verified live: all four schemas currently OMIT MD (grep confirmed lines 134/218/140/156). |
| C3 | Contract #8: assembler READS ID_PATTERNS, never re-inlines; new names in `__all__` | PASS | Step 4.1 instructs "read the bodies from `ID_PATTERNS`, DO NOT re-inline the literal regex strings" + append 3 names to `__all__`. Verified ID_PATTERNS @L64-77 with MD@L71; `__all__`@L209-217 currently 7 names; assembler names absent (grep=0). Step 6.1 gates on `make lint-architecture` exit 0. |
| C4 | Guard tests use EXACT ARM-LEVEL (split on `\|`), NOT substring; + MD-as-own-arm regression | PASS | Verified live tests use the broken `ID_PATTERNS[family] in pattern` substring + frozen tuple `("FR","NFR","SC","G","D")` + frozen prefix tuple. Task Steps 5.1-5.4 require `arms = pattern[2:-2].split("\|")` + `body in arms` (exact) + keys-driven from live SoT; 5.5 adds parametrized `ID_PATTERNS["MD"] in pattern[2:-2].split("\|")` + behavioral `re.match(pattern,"M1-D01")` + negative `XYZ-1` + positive bare-`D-1`. MD⊂D trap addressed. |
| C5 | 55 extra-family fixtures preserved; verify runs `-k tool_write` vs 157p/1s baseline | PASS | Step 1.4 captures baseline (expects 157p/1s/1808 deselected); Step 6.3 re-runs `uv run pytest tests/roadmap/ -k tool_write -q` and asserts 0 failures + passed >= baseline. (Live grep found 92 extra-family token occurrences across tests/roadmap; the 55 figure is roadmap_ids-usage-specific per BUILD_REQUEST — the preservation intent is correctly encoded.) |
| C6 | Positive check validate_tool_output accepts M1-D01 per schema | PASS | Step 5.7 runs `validate_tool_output({'roadmap_ids':['FR-1','M1-D01']}, load_schema(...))` expecting `[]` per schema; Step 4.7 runs the on-disk `re.match` probe expecting True. Verified `validate_tool_output` returns `list[str]` (tool_writer.py:94). |
| C7 | ID_PATTERNS NOT modified (extras NOT promoted) | PASS | Every Phase 4 item + Step 4.1 + the Overview state "ID_PATTERNS UNTOUCHED"; the REJECTED-promote rationale (would pollute spec_parser.extract_requirement_ids) is recorded in Step 3.1(c) + Overview. |
| C8 | never-stage-.claude + UV-only + branch discipline embedded | PASS | 18 occurrences of never-stage-.claude / UV / branch phrases. Step 1.3 verifies origin=IronbellyOrg + branch=refactor/roadmap-pipeline-r0-r1-rewrite; Step 6.2 + Post-Completion re-assert the .claude/ staging prohibition; all commands UV-only single-line. |
| 10 | Intra-phase dependency ordering | PASS | 3.1 writes artifact before all Phase 4 reads; 4.1 creates assembler before 4.2 verifies before 4.3-4.6 call it before 4.7 verifies on-disk; Step 1.4 baseline captured before Step 6.3 delta. |
| 11 | Duplicate operation detection | PASS | `-k tool_write` appears at 1.4 (baseline) + 6.3 (final delta) + conditional post-completion re-run — each has intervening source changes justifying re-run. Step 5.7 uses a narrower `-k` filter. No redundant duplicates. |
| 12 | Completion-criteria honesty | PASS | Final "Done" item (L296) explicitly gates: "must not be marked complete until all preceding items (including the Phase Gate) are complete." Phase Gate PG.3 converts only after-cap residuals to Open Questions. |
| 13 | Carry-forward Phase-4 item numbering accuracy (cross-ref) | **FIXED** | Step 3.1(e) carry-forward list mis-numbered the Phase 4 items: said "4.2–4.5 regenerate ... 4.6 verify merge≡generate" but actual layout is 4.2 verify-assembler / 4.3-4.6 regenerate / 4.7 verify-on-disk. Would generate a decision artifact with a wrong carry-forward map. FIXED to "4.2 verify assembler; 4.3–4.6 regenerate ...; 4.7 verify on-disk". |

---

## Summary

- Checks passed: 28 / 28 (after fixes)
- Checks failed (pre-fix): 2 (TB-Add-7 header drift; carry-forward mis-numbering)
- Critical issues: 0
- Issues fixed in-place: 2

## Issues Found (and Fixed)

| # | Severity | Location | Issue | Fix Applied |
|---|----------|----------|-------|-------------|
| 1 | MINOR | Execution Context `**Source areas:**` line (L125) | Header named "the roadmap executor wiring" as a source area, but the executor is BUILD_REQUEST runtime *context* only (executor.py:1288 wires the render) and no checklist item references or edits it — TB-Add-7 header-vs-item drift. | Removed "the roadmap executor wiring" from the Source areas line; replaced with an explicit tool-writer surface (`load_schema` / `validate_tool_output`) that genuinely reappears in items (10x). |
| 2 | IMPORTANT | Step 3.1 carry-forward list (item (e)) | The decision-artifact carry-forward map mis-numbered Phase 4 items: "4.2–4.5 regenerate ... 4.6 verify merge≡generate". Actual layout: 4.2=verify-assembler, 4.3-4.6=regenerate four schemas, 4.7=verify-on-disk. Executor would emit a schema-sot-decision.md whose carry-forward references the wrong items. | Corrected to "4.2 verify the assembler imports/emits per-step patterns; 4.3–4.6 regenerate the four schemas respectively; 4.7 verify the on-disk schemas accept M1-D01 and merge≡generate holds". |

## Actions Taken

- Fixed Issue 1 (TB-Add-7) by Edit on the Source areas line; re-verified: 0 file:line leak in header, executor no longer named, all 5 remaining source areas (contracts 4x, schemas 13x, tool-writer 10x, arch-lint 11x, test-suite 21x) reappear in item bodies.
- Fixed Issue 2 by Edit on Step 3.1(e); re-verified the corrected string is present and matches the real Phase 4 numbering.

## Correctness Verification (against live source — the critical-checks the spawn brief demanded)

| Live source | Verified |
|---|---|
| `src/superclaude/contracts/__init__.py` ID_PATTERNS (L64-77): MD,FR,NFR,SC,G,D; MD=`r"M\d+-D-?\d+"` ordered before D | matches task claim exactly |
| `__all__` (L209-217) = 7 names; no assembler/registry/map present yet | confirms new-additions framing |
| 4 schema patterns (extract L134, extract_tdd L218, generate L140, merge L156) all OMIT MD; generate≡merge byte-identical; extract has COMP-before-DM | matches task claim exactly |
| extract.schema.json has `component_inventory` but NO `data_models` array | confirms "extract DM is fixture-backed" subtlety |
| generate.schema.json `milestones[].open_questions[].id` is a string property | confirms OQ-family source claim |
| 4 guard tests: frozen tuple `("FR","NFR","SC","G","D")` + substring `ID_PATTERNS[family] in pattern`; extract_tdd/merge add frozen prefix tuple + `prefix in pattern`; merge-pin `merge_pattern == generate_pattern` @L271-279 | matches task's "broken structure" description exactly |
| `tool_writer.load_schema(name)` takes full `"x.schema.json"`; `validate_tool_output` returns `list[str]` | confirms probe-command correctness |
| `make lint-architecture` + `make verify-sync` targets exist (Makefile L362, L166) | confirms Phase 6 commands valid |

## Confidence Gate

- **Confidence:** Verified: 28/28 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Bash (incl. batched grep/ls): 9 | Glob: 0 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- No external lookup required (all claims source-truth-local). No Tavily fallback engaged.
- Tool-engagement note: 16 tool calls (7 Read + 9 Bash). Each Bash call batched several grep verifications against live source (e.g. one call verified all 4 schema patterns + entity arrays + make targets). Every one of the 28 checks maps to a specific tool output cited in the evidence column above — no padding.

## QA Complete

VERDICT: PASS (2 issues found and FIXED in-place; no unfixable issues; final task-file state passes all 28 checks)
