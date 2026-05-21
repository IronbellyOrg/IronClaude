# Code Review: PR #62 (MERGED)

**Target**: PR #62 — `fix(prd): align gates.py research-notes schema with upstream prompt`
**Reviewer**: /sc:auggie-review (depth=standard, focus=all)
**Generated**: 2026-05-20 17:18 UTC
**Source PR**: https://github.com/IronbellyOrg/IronClaude/pull/62
**Base ↔ Head**: `master` ↔ `fix/prd-gates-schema-divergence`
**Merge commit**: `f333cdf107405939cec92247b527012314f6d3fe`
**Stats**: 21 files (4 code, 17 MDTM artifacts), 5633 diff lines (code subset ≈ 144 lines), 9 findings (0 dropped during grounding)

> **Note**: This is a post-merge advisory review (PR already merged 2026-05-20). No PR comment was posted (`--no-post-pr`).

---

## Summary

The PR is a correct, narrow fix for a real schema-divergence bug between `gates.py` and `prompts.py`. The four edits (A–E) cleanly align the gate's required-section list with what the prompt instructs the agent to emit, and the new round-trip integration test (`test_research_notes_roundtrip.py`) is the right structural mitigation — it would have caught the original bug and will catch future drift. **Verdict: Approve with comments** — no Critical or High findings. The architectural smell that allowed the bug to land (hardcoded section list duplicated across `gates.py`, `prompts.py`, and `SKILL.md`) persists for at least one other constant (`_PRD_CRITICAL_SECTIONS`) and would benefit from the same round-trip-test treatment in a follow-up.

**Recommendation: Approve with comments** (Medium=2, Low=4, Nit=3)

---

## Findings

### 🔴 Critical (block merge)

_None._

### 🟠 High (should fix before merge)

_None._

### 🟡 Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. Edit B widens regex without a dedicated unit test for the new pattern surface

- **File**: `tests/cli/prd/test_gates.py:47-86`
- **Category**: tests
- **Source**: auggie
- **Evidence** (current state of `test_gates.py`):
  ```python
  class TestCheckResearchNotesSections:
      """Validate all 7 required research sections."""
      def test_check_research_notes_sections(self) -> None:
          content = """
  ## EXISTING_FILES
  ...
  ## SUGGESTED_PHASES
  1. Phase one detail
  ...
  """
          assert _check_research_notes_sections(content) is True
  ```
- **Why this matters**: Edit B modified the regex at `gates.py:135` from `\s+` to `[\s_]+` specifically to accept both `## SUGGESTED_PHASES` (underscore form, what the prompt actually emits) and `## Suggested Phases` (space form, the pre-PR test fixture). The round-trip test at `test_research_notes_roundtrip.py` exercises the underscore form end-to-end, but no test asserts the regex still accepts the space form, and no test asserts the regex correctly rejects malformed variants. If a future edit narrows the regex back to `\s+`, only the round-trip test would catch it — and the failure mode would look like a section-name mismatch, not a regex regression. A dedicated unit test pinpoints the regression cause faster.
- **Recommendation**: Add a `TestCheckSuggestedPhasesDetail` class with four cases: (a) `## SUGGESTED_PHASES` + list passes; (b) `## Suggested Phases` + list passes; (c) `## SUGGESTED_PHASES` without list fails with "no detail items"; (d) entirely missing heading fails with "No 'Suggested Phases' section found".

#### M2. Hardcoded section list pattern repeats in `_PRD_CRITICAL_SECTIONS` without round-trip coverage

- **File**: `src/superclaude/cli/prd/gates.py:215-221`
- **Category**: architecture (cross-cutting)
- **Source**: auggie
- **Evidence**:
  ```python
  _PRD_CRITICAL_SECTIONS = [
      "Executive Summary",
      "Problem Statement",
      "Technical Requirements",
      "Implementation Plan",
      "Success Metrics",
  ]
  ```
- **Why this matters**: This is the same architectural pattern that produced the bug this PR fixes. `_PRD_CRITICAL_SECTIONS` (`gates.py:215`) feeds `_check_prd_template_sections` (`gates.py:224`) which presumably validates the assembled PRD against what `build_assembly_prompt` or the PRD template specifies — but no round-trip test verifies the two sides agree. The PR introduces the right mitigation pattern (Edit D); applying it once more would close the remaining structural blind spot. Out-of-scope for this PR's commit but a natural follow-up.
- **Recommendation**: File a follow-up task to add `test_prd_assembly_roundtrip.py` mirroring `test_research_notes_roundtrip.py`: extract the H2 sections from `build_assembly_prompt(...)` (or the assembled-PRD template) and assert they equal `_PRD_CRITICAL_SECTIONS`. Optionally, in a separate refactor, consolidate both constants into `src/superclaude/cli/prd/schemas.py` and import them where consumed.

### 🟢 Low (nice-to-have)

#### L1. Schema list still hardcoded in `gates.py` — drift can recur

- **File**: `src/superclaude/cli/prd/gates.py:102-110`
- **Category**: architecture
- **Source**: auggie
- **Evidence**:
  ```python
  _RESEARCH_REQUIRED_SECTIONS = [
      "EXISTING_FILES",
      "PATTERNS_AND_CONVENTIONS",
      "FEATURE_ANALYSIS",
      "RECOMMENDED_OUTPUTS",
      "SUGGESTED_PHASES",
      "TEMPLATE_NOTES",
      "AMBIGUITIES_FOR_USER",
  ]
  ```
- **Why this matters**: The bug fixed by this PR was caused by this list silently diverging from `prompts.py:226-255` and `SKILL.md:267-305`. Edit D's round-trip test now detects future drift, but the underlying source-of-truth duplication persists (three locations: gates, prompt builder, skill ref). If `SKILL.md` (the documented authority) is updated to add an 8th section but `prompts.py` isn't, the round-trip test still passes (it only compares prompt ↔ gate). Confidence the test catches the most-common drift mode is high; the remaining blind spot (skill ↔ implementation) is intentional per PR scope.
- **Recommendation**: Consider in a follow-up refactor: derive `_RESEARCH_REQUIRED_SECTIONS` from a single shared constants module (or parse the H2 headings out of the prompt template at import time). Not blocking — PR-as-merged is correct.

#### L2. `(?:Suggested[\s_]+)?Phases` regex is broader than the two documented forms

- **File**: `src/superclaude/cli/prd/gates.py:134-138`
- **Category**: correctness
- **Source**: auggie
- **Evidence**:
  ```python
  phases_match = re.search(
      r"(?:^|\n)\s*#{1,4}\s+.*(?:Suggested[\s_]+)?Phases",
      content,
      re.IGNORECASE,
  )
  ```
- **Why this matters**: The `(?:Suggested[\s_]+)?` group is optional, which means the regex matches any heading ending in "Phases" — `## Implementation Phases`, `## Other Phases`, `## Phases`, etc. It also matches `## Suggested___Phases` (multiple underscores) and `## Suggested_  Phases` (mixed). This is benign in the happy path because research-notes only emit one such heading, but if a future authored research-notes uses a different "...Phases" heading first, the gate would attach detail-checking to the wrong section. Auggie's claim that "zero separators match" is incorrect (`+` requires ≥1) but the over-permissive prefix is real.
- **Recommendation**: Tighten to `(?:Suggested\s+Phases|SUGGESTED_PHASES)` so only the two documented forms match. Minor — current regex is functional given the prompt's single-`...Phases`-heading guarantee.

#### L3. No update to skill-reference sufficiency checklist to reference the 7-section schema

- **File**: `src/superclaude/skills/prd/SKILL.md:307-320`
- **Category**: docs
- **Source**: auggie
- **Evidence**:
  ```
  ### A.5: Review Research Sufficiency (MANDATORY GATE)
  ...
  1. Is the product scope clearly bounded?
  2. Are all major subsystems identified?
  ...
  8. If any doc-sourced claims appear in the research notes ...
  ```
- **Why this matters**: The skill's sufficiency checklist (8 conceptual questions) does not explicitly reference the 7 schema sections that `gates.py` now enforces. A human reviewer applying the checklist could pass a research-notes that fails the automated gate, or vice-versa. The schema definition at `SKILL.md:267-305` (which the PR cites as source of truth) is correct, so the gap is paper-only; not blocking.
- **Recommendation**: Optionally add a 9th item: "Do all 7 required H2 sections (EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER) contain non-trivial content?" Out of scope for this PR.

#### L4. e2e fixtures cover only the underscore heading form

- **File**: `tests/cli/prd/test_e2e.py:120-148`
- **Category**: tests
- **Source**: auggie
- **Evidence**: All 5 e2e scenarios consuming `_make_passing_output(step_id="research-notes", ...)` now emit `## SUGGESTED_PHASES` (underscore form). No scenario uses the space form `## Suggested Phases`.
- **Why this matters**: Edit B's regex widening allows both forms, but Edit E updated only the underscore-form fixture. If Edit B is reverted, the e2e tests will continue to pass (they use the form the prompt actually emits), but the regression that broke the *original* production output (mixed forms in legacy or human-edited notes) would be undetected. Confidence low because the prompt builder never emits the space form, so in practice this is speculative.
- **Recommendation**: Optional — parameterize one e2e scenario to use the space form as a defense-in-depth check, or accept that Edit B is covered by `test_research_notes_roundtrip.py` + the suggested M1 unit tests.

### 💬 Nits (style, naming, comments)

- **N1.** `tests/cli/prd/test_research_notes_roundtrip.py:73` — The numbered `1. Phase one detail` line is redundant because the preceding loop already appends `- detail` under `## SUGGESTED_PHASES`, which satisfies the `[\d.|[-*]]` list-pattern regex in `_check_suggested_phases_detail`. The accompanying comment (lines 70–72) acknowledges this. Either drop the extra line or trim the comment to a single sentence.
- **N2.** `src/superclaude/skills/prd/SKILL.md:307-320` — Minor: the sufficiency-review checklist phrases are conceptual ("are all major subsystems identified?") while the schema requires named sections ("PATTERNS_AND_CONVENTIONS"). Bridging the two with a parenthetical (e.g., "(see `## PATTERNS_AND_CONVENTIONS`)") would tighten the mapping. Not blocking.
- **N3.** `tests/cli/prd/test_e2e.py:131-147` — The fixture literal could be a constant or fixture function to reduce duplication if any future test re-uses the same passing-research-notes shape; not worth doing today.

---

## Architectural / Cross-Cutting Observations

### CC1. Hardcoded schema constants persist as a systemic SoT-divergence risk (Medium)

- **Affected files**: `src/superclaude/cli/prd/gates.py`, `src/superclaude/cli/prd/prompts.py`, `src/superclaude/skills/prd/SKILL.md`
- **Source**: auggie
- **Why this matters**: This PR fixes one instance (`_RESEARCH_REQUIRED_SECTIONS`) of a pattern — hardcoded section lists duplicated across the prompt builder, the gate, and the skill reference — that produced the bug it fixes. The codebase contains at least one more such constant (`_PRD_CRITICAL_SECTIONS`, `gates.py:215`), unverified against the assembly prompt or PRD template. The round-trip test pattern (Edit D) is the right mitigation and should be applied systematically.
- **Recommendation**: Two-stage follow-up. (1) Add round-trip tests for every other gate that validates section presence (start with `_check_prd_template_sections`). (2) In a separate refactor, centralize section names in `src/superclaude/cli/prd/schemas.py` and import them from both `gates.py` and `prompts.py`, replacing string-list duplication with shared identifiers.

### CC2. Gate-regex edge cases lack systematic test coverage (Low)

- **Affected files**: `tests/cli/prd/test_gates.py`, `tests/cli/prd/test_research_notes_roundtrip.py`, `tests/cli/prd/test_e2e.py`
- **Source**: auggie
- **Why this matters**: `gates.py` contains ~10 semantic check functions with multiple regex patterns. Test coverage focuses on happy-path validation; no systematic edge-case matrix exists. Edit B widened one regex without explicit before/after tests for the widening.
- **Recommendation**: Build out a regex edge-case test matrix for each `_check_*` function — happy path, case variation, whitespace variation, EOF boundary, double match. Not blocking; opportunistic hygiene that would have caught the original bug independently.

---

## Audit

- **Auggie chunks**: 1 (succeeded: 1, retried: 0, skipped: 0)
- **Auggie raw output**: `/tmp/eval-pr62/auggie-raw-main.json` (14,691 bytes)
- **Findings dropped during grounding**: 0 — every cited `file:line` was validated against the live repo via `Read` (the regex line `gates.py:135` differs from Auggie's "line 135" by 0; `test_gates.py:47-86` matches exactly; `test_research_notes_roundtrip.py:69-73` matches; `test_e2e.py:131-145` matches; `gates.py:215-221` matches; `SKILL.md:307-320` matches).
- **Persona cross-check**: disabled (`--depth standard`)
- **Severity remap**: all 7 findings + 2 cross-cutting observations were remapped via `refs/severity-rubric.md`. Auggie hinted High×1, Medium×2, Low×4 + cc Medium×2; final after remap was Medium×2, Low×4, Nit×3. Detailed reasoning in `audit.log`.
- **Token cost (est.)**: Claude orchestration ≈ 6k; Auggie deep pass ≈ 15-20k.
- **Protocol notes**:
  - Auggie CLI flag was `--output-format json` (skill ref says `--output-format json`; an initial invocation with `--json` failed and was retried per skill error-handling guidance).
  - Diff size (5633 lines) exceeded the standard-mode WARN threshold (1500 lines), but the code-file subset is ~144 lines (the bulk is MDTM markdown audit artifacts). Single-pass review was appropriate; no chunking needed.
  - `--no-post-pr` honored — nothing was posted to the PR.

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 0 medium: 2 low: 4 nit: 3
dropped: 0
auggie_chunks: 1
duration_sec: ~120
-->
