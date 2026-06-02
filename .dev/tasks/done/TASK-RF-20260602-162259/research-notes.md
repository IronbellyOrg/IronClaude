# Research Notes: tool-write schema roadmap_ids ↔ ID family SoT durable fix

**Date:** 2026-06-02
**Scenario:** A (explicit — BUILD_REQUEST with verified analysis)
**Depth Tier:** Deep
**Track Count:** 1
**BUILD_REQUEST:** `.dev/reviews/BUILD-REQUEST-tool-write-schema-id-sot.md`
**Template:** 02 (investigation/decision gate + conditional implementation)

## EXISTING_FILES (re-verified this session)
- `src/superclaude/contracts/__init__.py` — `ID_PATTERNS` (~L64-77; `"MD": r"M\d+-D-?\d+"` present), `__all__` (~L209+ exports ID_PATTERNS). No `roadmap_ids_pattern()` assembler yet.
- `src/superclaude/cli/roadmap/templates/tool_schemas/{generate,extract,extract_tdd,merge}.schema.json` — each has a `roadmap_ids.items.pattern`; family sets differ (generate/merge = full incl OQ; extract = FR/NFR/SC/G/D/COMP/DM only; extract_tdd = full minus OQ); NONE has MD.
- `src/superclaude/cli/roadmap/tool_writer.py` — `load_schema` L67, `validate_tool_output` L94, `validate_id_subset` L344, `render_step_tool_write_with_id_check` L455 (extracts `roadmap_ids` L488, validates subset L489).
- `src/superclaude/cli/roadmap/executor.py` — wires id-checked tool-write render (~L1288 per agent B; re-verify).
- `src/superclaude/tools/arch_lint.py` — enforces no-inline of ID_PATTERNS bodies in `.py` only (Contract #8); does NOT scan JSON.
- Guard tests: `tests/roadmap/test_tool_write_step_{extract,extract_tdd,generate,merge}.py` — `test_*_schema_id_pattern_matches_contracts` (extract L130-141 CONFIRMED: `for family in ("FR","NFR","SC","G","D"): assert ID_PATTERNS[family] in pattern` — frozen tuple + substring; MD absent). `test_merge_schema_matches_generate_id_pattern` pins merge==generate.

## PATTERNS_AND_CONVENTIONS
- Contracts SoT (Contract #8): ID bodies live ONLY in `contracts.ID_PATTERNS`, anchor-free; consumers wrap `\b…\b` or `^(…)$`. arch_lint Rule 2 enforces for `.py`. MD body must NOT be re-inlined.
- The MD⊂D substring trap: `D-?\d+` is a literal substring of `M\d+-D-?\d+` → guard tests MUST use exact/arm-level matching, not `in`.
- Superset relationship: tool-write roadmap_ids families = ID_PATTERNS (FR/NFR/SC/G/D/MD) ∪ tool-write-only (DM/API/COMP/TEST/MIG/OPS/OQ). The latter have 55 real fixture usages — NOT removable.
- Schemas are static JSON read at runtime by `tool_writer.load_schema` (json.loads); NOT a make sync-dev target (under cli/, not skills/agents/commands).

## GAPS_AND_QUESTIONS (for researchers)
- **DESIGN-CRITICAL:** Are the per-schema family differences (extract omits API/TEST/MIG/OPS/OQ; extract_tdd omits OQ) INTENTIONAL per step semantics or DRIFT? Resolve via the schema `$comment` fields + `git blame`/`git show c542b6bf` on each schema. This determines whether the assembler is one global pattern or per-step.
- Where should the tool-write-only family SoT live? (default lean: a new `contracts` constant, e.g. `ROADMAP_ID_FAMILIES` / `TOOL_WRITE_EXTRA_ID_FAMILIES`, + a `roadmap_ids_pattern()` assembler. NOT promoting extras into `ID_PATTERNS` — that would pull them into spec_parser regex extraction.)
- Exact list + bodies of the tool-write-only families (DM/API/COMP/TEST/MIG/OPS/OQ) as they appear in the schemas (regex bodies, e.g. `DM-\w+`).
- Exact structure of all 4 guard tests + the merge==generate pin, to rebuild them keys-driven + exact-arm.
- executor.py exact wiring line for tool-write id-check render (re-verify ~L1288).

## RECOMMENDED_OUTPUTS (research/)
- `01-schema-and-contracts-inventory.md` — the 4 schemas' exact roadmap_ids patterns + family sets, contracts ID_PATTERNS + __all__, tool_writer load_schema/validate_id_subset/render_step_tool_write_with_id_check + executor wiring. (File Inventory + Integration)
- `02-intentional-vs-drift-investigation.md` — schema $comment fields + git blame c542b6bf: are the per-schema differences intentional or drift? Recommendation for per-step vs unified derivation. (the DESIGN-critical research)
- `03-tests-and-fixtures.md` — the 4 guard tests' exact structure, the 55 extra-family usages, tool-write test construction/validation pattern, where the MD-arm regression goes, the merge==generate pin. (Test & Verification)
- `04-template-and-examples.md` — MDTM template 02 rules + decision-gate shape + a prior TASK-RF example. (Template & Examples)

## SUGGESTED_PHASES
- R1 (File Inventory + Integration): contracts + 4 schemas + tool_writer + executor wiring. Output 01.
- R2 (Integration/Doc Cross-Validator): intentional-vs-drift via $comment + git blame. Output 02.
- R3 (Test & Verification): guard tests + 55 fixtures + regression placement. Output 03.
- R4 (Template & Examples): template 02 + decision-gate shape. Output 04.

## TEMPLATE_NOTES
Template 02. Deep tier. The generated task must model: Phase A investigation/decision (intentional-vs-drift + family-SoT location → decision artifact) → Phase B implementation (family-SoT constant + roadmap_ids_pattern() assembler in contracts; regenerate 4 schema patterns from it with MD landing; per-step OR unified per decision) → Phase C test rebuild (4 guard tests keys-driven + exact-arm + MD-arm regression) → Phase D verify (uv run pytest -k tool_write; lint-architecture; verify-sync; positive M1-D01 validates). FINAL_ONLY QA gate. TESTING_REQUIREMENTS=UNIT.

## AMBIGUITIES_FOR_USER
None blocking. The one genuine decision (intentional-vs-drift; family-SoT location) is modeled as an in-task decision gate grounded by the R2 investigation, with a documented default (per-step-aware assembler if intentional; separate contracts constant for the extra families).
