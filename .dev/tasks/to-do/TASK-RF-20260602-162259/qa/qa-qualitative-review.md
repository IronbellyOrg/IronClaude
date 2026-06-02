# QA Report — task-qualitative

**Topic:** ID_PATTERNS ↔ tool-write schema drift durable fix (PER-STEP family SoT + roadmap_ids_pattern(step) assembler)
**Date:** 2026-06-02
**Phase:** task-qualitative
**Fix cycle:** N/A (initial)

---

## Overall Verdict: PASS

BUILD_REQUEST.GOAL verbatim (drift baseline captured): "durable fix for ID_PATTERNS ↔ tool-write schema drift — add MD to 4 schemas via a PER-STEP family SoT + `roadmap_ids_pattern(step)` assembler in contracts, rebuild 4 broken guard tests (arm-level keys-driven + MD-arm regression), verify. Tool-write is non-default." AX-1 Drift axis is ACTIVE.

The plan would SUCCEED if executed. I empirically simulated the planned assembler, traced the JSON-escaping round-trip end-to-end (the #1 operational risk), confirmed the live drift exists and is rejected at `validate_tool_output`, confirmed arm-level split-on-`|` is safe (no arm body contains a literal `|`), and confirmed arch_lint Rule 2 cannot fire. One MINOR observational note (Step 5.7 inline command output) — does not block; the prose acceptance criterion is correct and the executor has the documented escape hatch.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | Baseline `uv run pytest tests/roadmap/ -k tool_write -q` = 157 passed/1 skipped/1808 deselected — exact match to task's stated baseline. `make lint-architecture`/`verify-sync`/`sync-dev` targets all exist (Makefile:362/166/109). Assembler/schema-regen/probe commands all syntactically valid and run. |
| 2 | Project convention compliance | none | PASS | sync-dev (Makefile:109-130) globs ONLY `src/superclaude/skills/*` + `agents/*.md`; `cli/.../tool_schemas/*.json` is NOT a sync-dev target → no `.claude/` mirror, verify-sync stays clean. Edits target `src/superclaude/` + `tests/` only. never-stage-.claude embedded in 6.2/Post-Completion. |
| 3 | Intra-phase execution order | none | PASS | 4.1 (assembler) precedes 4.2-4.7 (consume it); Phase 5 guard tests import the new SoT names 4.1 adds; verify last. Phase 4 gated on Phase 3 artifact (rf-qa confirmed DAG). No item reads a symbol a later item creates. |
| 4 | Function signature verification | none | PASS | Read `contracts/__init__.py`: ID_PATTERNS has MD=`M\d+-D-?\d+` ordered before D; `__all__` exists. `roadmap_ids_pattern(step)` is a NEW function (no signature conflict). `load_schema`/`validate_tool_output` in tool_writer.py:67,94 unchanged and compatible. |
| 5 | Module context analysis | none | PASS | Assembler reads `ID_PATTERNS.values()` (Contract #8); new constants `ROADMAP_ENTITY_ID_FAMILIES`/`TOOL_WRITE_ROADMAP_ID_FAMILIES` + 3 `__all__` appends. arch_lint `_load_canonical_constants` (arch_lint.py:80-91) reads `__all__` + ID_PATTERNS.values() — new names picked up; entity bodies NOT in ID_PATTERNS so no Rule-2 literal collision. |
| 6 | Downstream consumer analysis | none | PASS | Consumers of the schema patterns: `validate_tool_output` (runtime) + the 4 guard tests + merge≡generate pin. Task updates ALL of them (Phase 4 regen + Phase 5 rebuild). No consumer left stale. tool_writer.py runtime path reads on-disk JSON via load_schema — picks up regenerated patterns automatically. |
| 7 | Test validity | none | PASS | Guard rebuild uses LIVE SoT (`ID_PATTERNS.items()`, `TOOL_WRITE_ROADMAP_ID_FAMILIES[step]`) — not frozen literals, not stubs. MD regression asserts BOTH structural (`ID_PATTERNS["MD"] in arms`) AND behavioral (`re.match(pattern,"M1-D01")`) plus negative `XYZ-1`/positive bare-`D-1`. Exercises real behavior. |
| 8 | Test coverage primary use case | none | PASS | Step 5.7 runs guard+pin+MD-regression then a positive `validate_tool_output(M1-D01)` per schema (the runtime acceptance path). Step 6.3 runs full tool-write suite incl 55 extra-family fixtures. End-to-end M1-D01 acceptance covered. |
| 9 | Error path coverage | none | PASS | Assembler raises KeyError/ValueError for unknown step (Step 4.1). Phase 4.2/4.7 probes have fix-loops on import failure / False match. JSON-escaping uncertainty has a logged-blocker path. Adapted: edge cases (MD⊂D trap, OQ-not-in-extract) explicitly handled. |
| 10 | Runtime failure path trace | none | PASS | Data flow: ID_PATTERNS → roadmap_ids_pattern(step) → `python -c print(...)` (single-backslash) → JSON file with `\\` double-backslash → load_schema/json.loads → single-backslash regex → jsonschema. Traced empirically: readback == assembler output for all 4 steps. No step breaks. |
| 11 | Completion scope honesty | none | PASS | Open Question (extract's DM arm fixture-backed) is RESOLVED in-plan: map keeps DM for extract (Step 4.1 `extract→(DM,COMP)`); Follow-Up note (L368) flags future-fixture widening. Decision artifact (Phase 3) records PROCEED/HALT honestly; HALT branch skips Phase 4 cleanly. |
| 12 | Ambient dependency completeness | none | PASS | 3 new names appended to `__all__` (Step 4.1) → importable + arch_lint discovery. Guard tests import them from `superclaude.contracts`. No CLI/registry/init touchpoints needed (pure contracts additions + schema/test edits). |
| 13 | Kwarg sequencing | none | PASS | No "add kwarg before add param" pattern. Assembler defined (4.1) before any caller (4.2-4.6, 5.x). New SoT constants defined before guard tests import them. |
| 14 | Function/value existence verification | none | PASS | Grep/Read verified: ID_PATTERNS["MD"] EXISTS (contracts:71); 4 schema patterns EXIST and OMIT MD (extract:134, extract_tdd:218, generate:140, merge:156 — verbatim); guard tests EXIST with frozen tuples + substring (extract:130-143, extract_tdd:206-222, generate:219-233, merge:250-279). roadmap_ids_pattern does NOT yet exist (to be created) — confirmed absent. |
| 15 | Template/cross-reference accuracy | none | PASS | Adapted: research-file §-citations re-anchored by symbol per task instructions. Schema JSON-key path `properties.roadmap_ids.items.pattern` verified live on all 4. Historical line numbers in task match current tree (no drift this session). |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (observational, non-blocking)
- Issues fixed in-place: 0 (no operational defect found requiring a fix)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | Step 5.7 | The literal inline command `[print(n, validate_tool_output({**base}, load_schema(n+'.schema.json'))) for n in [...]]` with `base={'roadmap_ids':['FR-1','M1-D01']}` will NOT print `[]` — it prints non-empty error lists for the OTHER `required` top-level keys (frontmatter, milestones, etc.). Verified empirically: feeding only `roadmap_ids` yields missing-required errors. | NONE required — the item ALREADY documents this ("if a given schema requires additional mandatory top-level keys... adjust the minimal object... but the `roadmap_ids` pattern element MUST not be the source of any error"). The prose acceptance criterion is correct (no roadmap_ids PATTERN error), and the executor has the documented escape hatch. Left as-is; flagged so the executor reads the full item and does not misread `!= []` as failure. |

## Actions Taken
None. No operational defect requiring an in-place fix was found. The single MINOR is already self-documented in the task item; editing it would risk over-correcting a correctly-bounded instruction.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for Check 4 (granularity), Check 8 (Phase 4 gated on Phase 3 decision artifact / DAG), Check 9 (item count 31), TB-Add-1..8 (placeholder/bounds/adjacency/DAG/XL/verify-form/exec-context/evidence-binding).
- Relied on rf-qa PASS for C1 (PER-STEP design), C2 (MD in 4 schemas — as a structural claim), C5 (55 fixtures preserved), C8 (never-stage/.claude + UV + branch).

**(b) Independent semantic checks (≥1 required, INV-019) — where rf-qa PASS was insufficient and my own tool work was required:**
- **JSON-escaping correctness (rf-qa cannot verify this — it's an operational regex/serialization concern):** simulated the planned assembler in `uv run python`, traced contracts body (`M\d+-D-?\d+`) → assembler Python string → `json.dumps` (auto-doubles to `\\d`) → `json.loads` readback. Verified `readback == assembler_output` for all 4 steps and `re.match(pattern,'M1-D01') == True`. This is the #1 risk the task names; rf-qa's "C2: MD added" is a presence check, not a round-trip-correctness check.
- **Live drift confirmation (semantic):** ran `validate_tool_output({'roadmap_ids':['M1-D01']}, schema)` against all 4 CURRENT on-disk schemas — confirmed `M1-D01` is rejected today with a roadmap_ids pattern error. rf-qa cannot run the runtime validator.
- **Arm-level split safety (semantic):** verified no `ID_PATTERNS` body or entity body contains a literal `|`, so `pattern[2:-2].split("|")` yields clean arms and `ID_PATTERNS["MD"] in arms` is exact-membership-true and distinct from the `D` arm (MD⊂D trap defeated). rf-qa's C4 asserts the design intent; I verified the live regex bodies make it mechanically sound.
- **arch_lint Rule-2 non-collision (semantic):** Read arch_lint.py:80-209 — confirmed `canonical_pattern_bodies = set(ID_PATTERNS.values())` excludes entity bodies, AND the canonical contracts file is skipped entirely (line 126-127), so neither the entity registry literals nor the assembler can trip Rule 2.

## Recommendations
- PROCEED. The plan is operationally sound and would succeed if executed.
- When executing Step 5.7, read the full item: the inline `validate_tool_output(...)` print will show non-empty lists for missing required top-level keys — that is EXPECTED; assert only that no `roadmap_ids`/`does not match` pattern error appears for `M1-D01` (or build a schema-complete minimal object per each step's fixture).

## Confidence Gate
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 6. Total tool calls (12) >= checklist items (15)? Several Bash calls each verified multiple checklist items via batched probes (assembler simulation covered checks 1,3,4,7,10,14; arch_lint read covered 5,12; schema-grep covered 6,14,15). Each call maps to specific verifications; none are padding.

## Self-Audit
1. Factual claims independently verified against source: ID_PATTERNS MD body + ordering + __all__ (Read contracts:64-217); 4 schema patterns verbatim + MD omission (Bash grep); guard-test frozen-tuple+substring structure for all 4 (Read + Bash grep); tool_writer load_schema/validate_tool_output signatures (Read); arch_lint Rule-2 logic (Read:80-209); live drift + JSON round-trip + arm-split + merge==generate (3 Bash python simulations). 9+ distinct claims.
2. Files read: contracts/__init__.py, tool_writer.py, arch_lint.py, test_tool_write_step_extract.py, test_tool_write_step_merge.py, the task file (full); grep over the 4 schema JSONs + extract_tdd/generate test files + Makefile.
3. Why trust the near-zero-defect verdict: I did not confirm by inspection alone — I EXECUTED the planned assembler, serialized it through json.dumps/loads, and ran the actual jsonschema validator against the live schemas to prove (a) the bug exists today and (b) the planned fix mechanically closes it with correct escaping. The single MINOR I surfaced is evidence I was looking adversarially at the inline command output, not rubber-stamping.
4. Web research: none performed (all checks local-file/runtime-bound). Tavily not invoked; no fallback occurred.

## QA Complete
