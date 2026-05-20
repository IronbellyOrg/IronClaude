# Research Notes: PRD pipeline gate-vs-prompt schema-divergence fix (Proposal A)

**Date:** 2026-05-20
**Scenario:** A (explicit)
**Depth Tier:** Quick
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

Verified in the prior adversarial-debate turn (this session, immediately preceding). All citations re-checked against current source.

- `src/superclaude/cli/prd/gates.py` — 506 lines, 16384 bytes (mtime May 17 04:43). PRD pipeline gate criteria module.
  - **Lines 102-110**: `_RESEARCH_REQUIRED_SECTIONS` constant — list of 7 strings the gate requires. EDIT TARGET #1.
  - **Lines 113-126**: `_check_research_notes_sections(content)` — consumes the constant via heading + bold regex with `re.IGNORECASE`. Regex itself is correct; only the input list needs rewriting.
  - **Lines 129-146**: `_check_suggested_phases_detail(content)` — secondary gate check; regex `(?:Suggested\s+)?Phases` fails against `## SUGGESTED_PHASES` because `\s+` does not match underscore. EDIT TARGET #2.
  - **Lines 295-506**: `GATE_CRITERIA` dict. Step 4 (`research-notes`) at lines 322-338 wires both `_check_research_notes_sections` and `_check_suggested_phases_detail` to the same gate (STRICT enforcement, min_lines=100). Confirms both checks must pass for step 4 to advance.

- `src/superclaude/cli/prd/prompts.py` — 1176 lines, 38730 bytes. REFERENCE ONLY (no edits).
  - **Lines 188-260**: `build_research_notes_prompt(config)` instructs the agent to emit `## EXISTING_FILES`, `## PATTERNS_AND_CONVENTIONS`, `## FEATURE_ANALYSIS`, `## RECOMMENDED_OUTPUTS`, `## SUGGESTED_PHASES`, `## TEMPLATE_NOTES`, `## AMBIGUITIES_FOR_USER`. This IS the source-of-truth schema after the fix.
  - **Lines 289, 290, 292**: `build_sufficiency_review_prompt` references `EXISTING_FILES` and `SUGGESTED_PHASES` by string — confirms downstream is already aligned with the EXISTING_FILES schema.
  - **Line 654**: `build_analyst_completeness_prompt` references `EXISTING_FILES, SUGGESTED_PHASES` — same alignment.

- `src/superclaude/skills/prd/SKILL.md` — 32079 bytes. REFERENCE (upstream source of truth).
  - **Lines 267-305**: "A.4: Write Research Notes File (MANDATORY)" defines the research-notes.md schema as exactly the 7 EXISTING_FILES-style sections. This is the upstream's authoritative schema and dissolved the C-proposal in the prior debate.
  - **Lines 307-320**: "A.5: Review Research Sufficiency" — natural-English review questions (e.g., "Are integration points mapped?"). Apparently misread by the port author as heading-name requirements, producing the current gate's fabricated 7-name list.
  - **Zero matches** for `Product Capabilities`, `User Flows`, `Gap Analysis` anywhere in SKILL.md or refs/* (grep'd in prior turn).

- `tests/cli/prd/test_gates.py` — 219 lines. EDIT TARGET #3.
  - **Lines 1-17**: header + imports; uses `from __future__ import annotations`, imports `_check_research_notes_sections` and 7 other check functions from `superclaude.cli.prd.gates`.
  - **Lines 47-86**: `class TestCheckResearchNotesSections` with two methods. Hand-written content uses the OLD gate-schema names (`## Product Capabilities`, `## Technical Architecture`, `## User Flows`, `## Integration Points`, `## Existing Documentation`, `## Gap Analysis`, `## Suggested Phases`). MUST be rewritten in lockstep with the new constant.

- `tests/cli/prd/test_research_notes_roundtrip.py` — DOES NOT EXIST. NEW FILE TO CREATE.
  - Will be the missing round-trip integration test that wires `build_research_notes_prompt` output through `_check_research_notes_sections`. Closes the structural blind spot identified by finding #8 in the validator brief (`test_gates.py` and `test_prompts.py` test each side in isolation; neither verifies prompt-schema == gate-schema).

- `tests/cli/prd/__init__.py` — exists (empty package marker, confirmed by directory listing in this session's first turn).

- `tests/cli/prd/test_prompts.py` — REFERENCE ONLY. Lines 75-88 hand-write a `research-notes.md` fixture in the EXISTING_FILES schema; this test would PASS unchanged after the fix and serves as informal cross-reference for the new round-trip test's expected schema.

## PATTERNS_AND_CONVENTIONS

Verified by reading the existing test files and similar Python source in the package.

- **Module headers**: All Python test files start with a docstring describing the section / test plan reference (e.g., `"""Unit tests for superclaude.cli.prd.gates. Section 8.1 test plan: 8 tests."""` at `test_gates.py:1-4`).
- **Future imports**: All test modules use `from __future__ import annotations` (test_gates.py:6, test_prompts.py:10).
- **Class-based grouping**: Tests are grouped into `class TestCheckXxx` per check function (test_gates.py:20, 47, 88, 106). Each class has a brief docstring.
- **Method signatures**: `def test_xxx(self) -> None:` (no `self`-less, no fixture if not needed). Methods that take fixtures (e.g., the `config` fixture in test_prompts.py) declare them as positional parameters.
- **Assertion style**: `assert x is True` / `assert isinstance(result, str)` / `assert "substring" in result` (test_gates.py:27, 41-44). The True/False checks are explicit `is True` / `is False`, not truthy checks.
- **Fixture style**: `@pytest.fixture()` decorator with parenthesis, returning a `Path` / `PrdConfig` (test_prompts.py:93-115).
- **No emoji**, no docstring on every method (only where helpful).
- **Black/ruff formatting**: trailing commas on multi-line lists, double quotes, 4-space indent.
- **Tests location**: under `tests/cli/prd/` mirroring `src/superclaude/cli/prd/`.

CLAUDE.md project conventions relevant to verification:
- Use `uv run pytest` for all test execution (never bare `pytest` or `python -m pytest`).
- `make lint` runs ruff; `make format` formats with ruff.
- Editable install means edits to `src/superclaude/` take effect on next CLI invocation with no rebuild.

## GAPS_AND_QUESTIONS

None blocking. All edits and the new test file structure were fully verified in the prior adversarial-debate turn. The verbatim edit text and the new test file content are reproduced in this research package below (see `01-file-inventory.md` and `03-edit-specifications.md`).

One residual question that does NOT block this task but should be noted for downstream awareness:

- `_check_prd_template_sections` at `gates.py:215-221` defines `_PRD_CRITICAL_SECTIONS = ["Executive Summary", "Problem Statement", "Technical Requirements", "Implementation Plan", "Success Metrics"]` and is wired to the `assembly` gate (`gates.py:462-466`). These names don't appear as a fixed list in upstream SKILL.md either, but they describe the final PRD (not the research-notes file), and they're standard PRD section names that any reasonable PRD will contain. **Not a bug; flagged for completeness per the validator's "spot-check before closing" caveat.** No action required by this task.

## RECOMMENDED_OUTPUTS

3 file edits + 1 new file:

1. **EDIT** `src/superclaude/cli/prd/gates.py` lines 102-110 — replace the 7-string list literal with the upstream EXISTING_FILES schema.
2. **EDIT** `src/superclaude/cli/prd/gates.py` lines 129-146 (specifically the regex on lines 134-138) — extend `\s+` to `[\s_]+` so `## SUGGESTED_PHASES` (underscore form) matches.
3. **EDIT** `tests/cli/prd/test_gates.py` lines 50-86 — rewrite both `test_check_research_notes_sections` and `test_check_research_notes_sections_missing` fixtures to use the new schema.
4. **CREATE** `tests/cli/prd/test_research_notes_roundtrip.py` — new round-trip integration test that:
   - Asserts `sorted(prompt_h2_sections) == sorted(_RESEARCH_REQUIRED_SECTIONS)` (schemas-must-match invariant).
   - Asserts that a research-notes.md constructed from the prompt's instructed sections passes both `_check_research_notes_sections` and `_check_suggested_phases_detail`.

Verification (no new file produced — informational only):
- Run `uv run pytest tests/cli/prd/test_gates.py tests/cli/prd/test_research_notes_roundtrip.py -v` — must pass.
- Run `uv run pytest tests/cli/prd/ -v` — full PRD test suite must pass (no regressions).
- Run `make lint` — must pass (ruff clean).

## SUGGESTED_PHASES

Quick tier, single track. 4 phases mapped to natural dependency ordering:

- **Phase 1 — Preparation**: Read & re-confirm current source. Bind exact current strings to be replaced. (1 item.)
- **Phase 2 — Source edits**: Two edits to `gates.py` — Edit A (constant list) and Edit B (regex). Sequential within the same file. (2 items.)
- **Phase 3 — Test edits & creation**: Edit C (rewrite test_gates.py fixture) and Edit D (create new round-trip test). Sequential. (2 items.)
- **Phase 4 — Verification & completion**: Run focused pytest invocation, full PRD pytest, ruff lint. Mark task done. (4 items including completion gate.)

Total estimated checklist items: ~9-10 (per-file granularity per template rule A3). Within the Quick tier item-count bounds (≥3, ≤40).

## TEMPLATE_NOTES

- **Template selection**: 02 (Complex Task). Rationale: even though the work is small, it involves build (3 file edits) + create (1 new file) + test (3 pytest invocations) + verification (lint), with phase dependencies and a verification gate. Template 02's discovery-build-test-review structure fits. Template 01 (Generic) would also work but loses the explicit verification-phase structure.
- **Granularity**: Per-edit items, not "edit all of gates.py". Specifically: one item per Edit (A, B, C, D), not bundled.
- **Each item self-contained per template rule B2**: Context (which file, which lines, why), Action (exact text to write — embed the verbatim diff), Output (modified file), Verification (read back / grep / pytest), Completion gate.
- **Evidence anchors**: Every Action must cite the verbatim old text and verbatim new text (no "see above"). Verified strings are reproduced in this research package so the builder has them.
- **No QA-gate items inside the generated task file**: this is a 4-edit job; FINAL_ONLY (pytest + lint at the end) is sufficient. PER_PHASE would be over-engineering.
- **Testing requirements**: UNIT (the new round-trip integration test is a unit-test-shaped file using pytest).
- **Validation requirements**: project-standard lint + pytest.

## AMBIGUITIES_FOR_USER

None — intent is clear from the request and the immediately-preceding adversarial-debate turn:
- Apply the 3 edits A/B/C exactly as specified in the prior turn.
- Create the new round-trip integration test exactly as specified in the prior turn.
- Verify with `uv run pytest tests/cli/prd/ -v` and `make lint`.
- Do NOT touch `prompts.py` (debate verdict A explicitly rejects rewriting the prompt).
- Do NOT touch upstream `SKILL.md` (upstream is correct; the gate was wrong).
