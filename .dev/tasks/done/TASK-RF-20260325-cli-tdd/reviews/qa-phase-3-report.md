# QA Report — Phase 3 Gate (TDD Extract Prompt — Critical Path)

**Topic:** CLI TDD Integration — Dual Extract Prompt
**Date:** 2026-03-26
**Phase:** phase-gate
**Fix cycle:** N/A

---

## Overall Verdict: PASS

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Function signature exists | PASS | Line 161: `def build_extract_prompt_tdd(spec_file: Path, retrospective_content: str \| None = None) -> str:` — exact match to required signature |
| 2 | Placement after `build_extract_prompt()`, before `build_generate_prompt()` | PASS | `build_extract_prompt()` ends line 158, `build_extract_prompt_tdd()` starts line 161, `build_generate_prompt()` starts line 288 |
| 3 | Neutralized source framing | PASS | Line 181: "requirements and design extraction specialist"; lines 182-183: "source specification or technical design document" — NOT "specification file" |
| 4 | 13 original + 6 new frontmatter fields | PASS | Lines 185-203: all 13 original fields (spec_source through extraction_mode) present, plus 6 new fields (data_models_identified, api_surfaces_identified, components_identified, test_artifacts_identified, migration_items_identified, operational_items_identified) each with "(integer) count ... or 0 if section absent" |
| 5 | Broadened identifier language | PASS | Lines 205-208: "Preserve exact identifiers from the source document including requirement IDs (FR-xxx, NFR-xxx), interface names, endpoint identifiers, component names, migration phase names, and test case IDs." — all 6 identifier types present |
| 6 | 8 standard body sections present with instruction text | PASS | Lines 216-240: Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions — all with full instruction text |
| 7 | 6 new TDD-specific body sections present | PASS | Lines 242-270: Data Models and Interfaces, API Specifications, Component Inventory, Testing Strategy, Migration and Rollout Plan, Operational Readiness — all present |
| 8 | Each new section has specific extraction instructions | PASS | Every new section has detailed, domain-specific extraction instructions (e.g., API Specs: "HTTP method, URL path, auth requirements, rate limits..."; Testing Strategy: "test pyramid breakdown with coverage levels/tooling/targets/ownership...") — no generic placeholders |
| 9 | `_OUTPUT_FORMAT_BLOCK` appended via `return base + _OUTPUT_FORMAT_BLOCK` | PASS | Line 285: `return base + _OUTPUT_FORMAT_BLOCK` — exact match to required pattern |
| 10 | Retrospective content block matches `build_extract_prompt()` pattern | PASS | Lines 274-283 are character-identical to lines 147-156 in the original function: same advisory heading, same disclaimer text, same `base += advisory` pattern |
| 11 | `spec_source` instruction says "Set spec_source to the filename of the input document" | PASS | Line 204: `"Set \`spec_source\` to the filename of the input document.\n\n"` — exact match |
| 12 | Original `build_extract_prompt()` COMPLETELY UNMODIFIED | PASS | Verified via `git diff HEAD -- prompts.py`: diff shows ONLY additions after line 158 (the new function insertion). Zero changes to lines 1-158. Runtime check confirms original still contains "specification file" language and lacks TDD sections |
| 13 | Function says "14 structured sections" | PASS | Line 214: `"After the frontmatter, provide the following 14 structured sections:\n\n"` — correct (8 standard + 6 new = 14) |

## Summary
- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Issues Found
None.

## Actions Taken
None required — all criteria met.

## Verification Method

Three independent verification approaches were used:

1. **Static code review** — Read the full `prompts.py` file (614 lines) and verified each criterion against specific line numbers
2. **Git diff analysis** — Ran `git diff HEAD -- prompts.py` to confirm the original `build_extract_prompt()` is completely unmodified (only additions after line 158)
3. **Runtime import test** — Executed Python verification that confirmed: all 6 new TDD sections present in output, `_OUTPUT_FORMAT_BLOCK` included, neutralized framing language present, and original function unchanged

## Recommendations
- Green light to proceed to Phase 4.

## QA Complete
