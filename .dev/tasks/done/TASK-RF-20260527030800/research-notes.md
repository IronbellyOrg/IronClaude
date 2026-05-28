# Research Notes: Hybrid cosmetic-remediator fix (C12 H2 parenthetical strip + gap-driven H3 repair)

**Date:** 2026-05-27
**Scenario:** A (Explicit) — goal, scope, deliverables all named upfront
**Depth Tier:** Quick (single subsystem, <5 files modified, single concern: cosmetic remediator coverage)
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

Primary surface (the hybrid fix touches these):

- `src/superclaude/cli/roadmap/cosmetic_remediator.py` (831 lines) — auto-remediation lane source. Key existing functions:
  - `_detect_cosmetic_violations` (line 270) — emits C1-C11 CosmeticViolation records; H2-level detection currently absent
  - `_detect_semantic_violations` (line 245) — only flags unreplaced `{{SC_PLACEHOLDER:...}}` and `OQ-xxx` in deliverable IDs; missing-required-section is NOT semantic
  - `_apply_milestone_h3_rewrites` (line 545) — C1-C4 transforms; pattern for C12 to follow
  - `_apply_resource_subsection_rewrites` (line 722) — C11 transforms under `## Resource Requirements and Dependencies`
  - `apply_cosmetic_remediations` (line 767) — orchestrator; transform-class dispatcher (extend dispatcher to call new C12 + gap-repair)
  - `classify_gate_failure` (line 501) — returns Classification with is_pure_cosmetic flag
  - `_REQUIRED_STEMS_ORDER` (line 49), `_REQUIRED_STEMS_LOWER` (line 57), `_RESOURCE_SUBSECTION_ALIASES` (line 81), `_RESOURCE_PARENT_NORMALIZED` (line 91) — canonical sets the new code references
- `src/superclaude/cli/roadmap/gates.py` (1441 lines) — gate definitions. Read-only for this task. Key references:
  - `_REQUIRED_H2_SECTIONS` (line 891-902) — the 8-entry canonical H2 set that C12 must match against
  - `_REQUIRED_MILESTONE_SUBSECTIONS` (line 907-911) — H3 stems
  - `_REQUIRED_RESOURCE_SUBSECTIONS` (line 914-916) — canonical H3s under Resource Requirements
  - `_normalize_heading` (line 919-924) — strips numbering only; does NOT strip parentheticals (this is the divergence the fix exploits)
  - `_template_sections_present` (line 927-1015) — the gate the fix unblocks
- `tests/roadmap/test_cosmetic_remediator.py` — existing test patterns (TestClassifierBasics, TestMilestoneH3Defects classes). New tests follow the `_content_with_milestone` helper pattern.

Out-of-scope (read for context but NOT modified):

- `src/superclaude/cli/pipeline/executor.py` (lines 275-373) — the post-remediation re-gate path that fall-throughs to FAIL when residual drift remains. The fix removes that fall-through on the .bak class of artifacts but does NOT change executor logic.
- `src/superclaude/cli/roadmap/prompts.py` — architect prompt; Path C territory, deferred.

## PATTERNS_AND_CONVENTIONS

Established patterns observed in `cosmetic_remediator.py` that the new code MUST follow:

- **Detector / transformer split**: every C-class has a detector in `_detect_cosmetic_violations` emitting CosmeticViolation records, and a separate `_apply_<thing>_rewrites()` transformer dispatched from `apply_cosmetic_remediations` based on the `klasses` set. C12 and gap-repair MUST follow the same split.
- **Idempotency**: every transformer is idempotent — re-running on canonical content is a no-op (line 13). New transforms MUST be idempotent.
- **Fenced-block guard**: every line-level detector / transformer skips lines in `_compute_fenced_indices` to avoid mangling code blocks (lines 204-228). New code MUST honor this.
- **Section-numbering strip**: headings pass through `_strip_section_numbering` before comparison (line 155). Apply this to candidate H2 / H3 bodies before parenthetical strip.
- **Substring match for resource aliases (C11)**: `_RESOURCE_SUBSECTION_ALIASES` uses lowercased substring containment with most-specific-first ordering (line 81-88). The gap-driven approach is an ADDITION to this layer, not a replacement.
- **`__all__` export contract** at line 826-831: public surface is `Classification`, `CosmeticViolation`, `apply_cosmetic_remediations`, `classify_gate_failure`. New helpers stay private (underscore prefix).
- **Test pattern** from `tests/roadmap/test_cosmetic_remediator.py`: hermetic inline markdown via `_content_with_milestone` helper (lines 23-39); classes grouped by C-class (`TestMilestoneH3Defects` etc.); hermetic, no fixture files.

## GAPS_AND_QUESTIONS

Gaps the researchers must close (NOT pre-answered here):

- Verify there is no existing C12-named class lurking in another module (the docstring at line 25-39 only lists C1-C11, but grep should confirm).
- Verify `_apply_resource_subsection_rewrites` does NOT already have ANY mechanism for non-aliased rename detection (line 722-764 reads as a strict alias loop, but full read needed).
- Identify the test fixture / pattern for asserting that a transformed artifact passes the gate end-to-end (does any existing test invoke `_template_sections_present` post-remediation? — researcher should locate or note absence).
- Identify whether the `apply_cosmetic_remediations` dispatcher needs a new gate (e.g., only call gap-repair after C11 ran AND a required canonical H3 is still missing) vs. always running.

## RECOMMENDED_OUTPUTS

Research files (3 — Quick tier minimum):

- `research/01-file-inventory.md` — detector / transformer inventory + canonical-set inventory for cosmetic_remediator.py + gates.py
- `research/02-patterns-conventions.md` — extract the detector / transformer / dispatcher / idempotency / fenced-skip pattern with file:line evidence; document test patterns from test_cosmetic_remediator.py
- `research/03-test-verification.md` — enumerate existing test classes, identify the helper pattern, find the closest analogous test (e.g., C11 tests) to model new C12 + gap-repair tests on

## SUGGESTED_PHASES

Researcher assignments — spawn in parallel, all in one message:

- **Researcher 1 (File Inventory) — Scope: `src/superclaude/cli/roadmap/cosmetic_remediator.py` + `src/superclaude/cli/roadmap/gates.py`**
  - Output: `research/01-file-inventory.md`
  - Focus: catalog every detector / transformer / canonical-set / public-surface symbol with file:line; flag any existing C12 / H2-paren / gap-repair code present
  - Other researchers covered: 02 (patterns), 03 (tests)

- **Researcher 2 (Patterns & Conventions) — Scope: `src/superclaude/cli/roadmap/cosmetic_remediator.py`**
  - Output: `research/02-patterns-conventions.md`
  - Focus: extract conventions from existing C1-C11 implementation (detector-emits-CosmeticViolation + transformer-modifies-content + dispatcher-on-klasses pattern, idempotency, fenced-guard, section-numbering strip); quote 2-3 representative code segments with file:line; document the `__all__` contract and naming convention
  - Other researchers covered: 01 (inventory), 03 (tests)

- **Researcher 3 (Test & Verification) — Scope: `tests/roadmap/test_cosmetic_remediator.py`**
  - Output: `research/03-test-verification.md`
  - Focus: enumerate test classes and their patterns; identify the `_content_with_milestone` helper signature + an analogous helper or extension needed for H2-paren / resource-rename test fixtures; locate any test that asserts post-remediation gate passage end-to-end (or note absence); document the pytest invocation pattern from CLAUDE.md (UV-only)
  - Other researchers covered: 01 (inventory), 02 (patterns)

## TEMPLATE_NOTES

- **MDTM Template choice: 02 (Complex Task)** — the work involves discovery (verify no existing C12 / no hidden state), implementation across detector+transformer+dispatcher, hermetic test additions, and a post-remediation gate end-to-end verification phase. Template 01 would be too thin for the test-pass-required structure.
- **Tier choice: Quick** — single subsystem (`cli/roadmap/cosmetic_remediator.py`), 2-3 modified files including tests, single concern (coverage gap), no multi-track signals.
- **QA gate requirements**: PER_PHASE — after each implementation phase (C12 detect+transform, gap-repair detect+transform, dispatcher wiring, tests) run a brief verification gate before proceeding. Final phase runs the `.bak` end-to-end as a smoke check.
- **Testing**: UNIT minimum, plus one INTEGRATION test that runs the actual `.bak` artifact through `classify_gate_failure` + `apply_cosmetic_remediations` + `_template_sections_present` end-to-end. The current end-to-end repro (validation REPORT.md reproducer block) is the integration test in seed form.

## AMBIGUITIES_FOR_USER

- **Naming of the gap-repair C-class**: should the new gap-driven H3 repair be `C12` (alongside H2-paren as `C13`) or should H2-paren be C12 and gap-repair be C13? The validation REPORT.md treats H2-paren as C12 by convention (B.1 in the original RCA). Recommendation: H2-paren = C12 (smaller, deterministic, lands first), gap-driven H3 repair = C13. Surface this in Open Questions of the generated task file and let the executor decide at implementation time — both names work.
- **Token-overlap threshold**: 0.34 (one of two tokens overlap, e.g., "external" in "external library lockset" overlaps "external" in "External Dependencies") is the validation REPORT's suggested floor. Alternative: use a stricter threshold (≥0.5) and refuse-on-ambiguity. Surface as a tunable constant in the task file's design phase.
- **Audit-log surface**: should C13 (gap-repair) emit a single transform record per rename or a structured record showing the overlap score? The existing C1-C11 audit lines are simple strings (line 600-602). Recommendation: stay consistent — simple string with score appended.
