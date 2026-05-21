# Code Review: PR #62 — fix(prd): align gates.py research-notes schema with upstream prompt

**Target**: PR #62 (IronbellyOrg/IronClaude) — MERGED 2026-05-20T06:25:20Z
**Reviewer**: /sc:auggie-review (depth=standard, focus=all)
**Generated**: 2026-05-20 17:50 UTC
**Source PR**: https://github.com/IronbellyOrg/IronClaude/pull/62
**Base ↔ Head**: master ↔ fix/prd-gates-schema-divergence (HEAD f4d5df19)
**Stats**: 21 files in PR (4 code + 17 task-artifacts), 212 code-diff lines, 6 findings (1 dropped during grounding)

---

## Summary

The PR is a tight, well-scoped fix that aligns three places where the PRD pipeline's research-notes schema must agree: the prompt instructions, the gate's required-section list, and the upstream SKILL.md source of truth. The fix itself is correct and the new round-trip integration test closes a real structural blind spot. The remaining concerns are architectural (the underlying schema-duplication-across-files pattern that allowed this drift is not eliminated by the PR — only realigned) and a subtle test-coverage gap around the regex-widening half of the fix. **Recommendation: Approve with comments** — no merge blockers; the medium-severity items are worth follow-up tickets rather than re-opening the merged PR.

## Findings

### 🔴 Critical (block merge)

_None._

### 🟠 High (should fix before merge)

_None._

### 🟡 Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. Schema duplication still present after fix — three sources of truth, no single owner

- **File**: `src/superclaude/cli/prd/gates.py:102-110`
- **Category**: architecture
- **Source**: auggie
- **In diff**: yes (Edit A targets these lines)
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
- **Why this matters**: The PR re-aligns the three places that all encode the same 7-name schema — `gates.py` (the constant above), `prompts.py:226-254` (heading-by-heading in the prompt string), and `skills/prd/SKILL.md:280-303` (the documented contract). The realignment closes the immediate divergence but the structural cause — three independent copies — is unchanged. The same drift can recur on the next edit. The PR body explicitly names SKILL.md as the source of truth, but no module in `src/superclaude/cli/prd/` imports from or references that document; instead `gates.py` re-asserts the list as a local constant.
- **Recommendation**: Centralize the 7-name section list in a single Python constant (e.g. `src/superclaude/cli/prd/schema.py` exporting `RESEARCH_NOTES_SECTIONS`) and have both `gates.py` and the prompt-builder in `prompts.py` consume it. The prompt-builder can interpolate the headings from the constant rather than hard-coding them. SKILL.md remains the human-readable spec, but it should reference the constant by symbol path so editors know where the canonical list lives.

#### M2. Round-trip test does not actually exercise the regex-widening fix (Edit B)

- **File**: `tests/cli/prd/test_research_notes_roundtrip.py:63-76`
- **Category**: tests
- **Source**: auggie
- **In diff**: yes (NEW file)
- **Evidence**:
  ```python
  def test_prompt_conforming_output_passes_gate(minimal_config: PrdConfig) -> None:
      """A research-notes.md that follows the prompt's instructions MUST pass the gate."""
      prompt = build_research_notes_prompt(minimal_config)
      instructed = _extract_h2_sections_from_prompt(prompt)
      fake_research_notes = "---\nDate: 2026-05-20\nScenario: B\nTier: standard\n---\n\n"
      for section in instructed:
          fake_research_notes += f"## {section}\n- detail\n\n"
      fake_research_notes += "1. Phase one detail\n"

      assert _check_research_notes_sections(fake_research_notes) is True
      assert _check_suggested_phases_detail(fake_research_notes) is True
  ```
- **Why this matters**: The PR body's test plan says "Reviewer to confirm round-trip test fails meaningfully if either Edit A or Edit B is reverted." Edit A (the section list) is genuinely exercised: reverting it puts the old 7-name list back and the first assertion fails. Edit B (the regex widening from `\s+` to `[\s_]+`) is **not** actually exercised, because the original regex `(?:Suggested\s+)?Phases` ALSO matches `## SUGGESTED_PHASES` — the `(?:...)?` group is optional and the trailing `.*Phases` matches `Phases` as a substring within `PHASES`. Verified empirically: both pre-fix and post-fix regexes return a match on the canonical input. Reverting Edit B would NOT break this test.
- **Recommendation**: Add a test case that specifically targets the regex's tolerance — feed it a fixture using literal `## Suggested Phases` (with space) AND a fixture using `## SUGGESTED_PHASES` (with underscore) and assert both pass. Then confirm by mutation that narrowing the regex back to `\s+` fails the space-form test. This makes Edit B a real regression guard rather than an unverified cleanup.

#### M3. Architectural cross-cut — no centralized schema constants module for PRD pipeline

- **Files**: `src/superclaude/cli/prd/gates.py`, `src/superclaude/cli/prd/prompts.py` (and `src/superclaude/skills/prd/SKILL.md`)
- **Category**: architecture (cross-cutting)
- **Source**: auggie
- **Why this matters**: This is the broader form of M1 and is included separately because the cure is broader than a single-file edit. The PRD pipeline has at least three section-list contracts (research-notes, PRD-critical-sections at `gates.py:215-221`, and likely the per-phase contracts the executor enforces). Each currently lives as a hardcoded list next to the function that checks it. As the pipeline matures, this pattern will keep producing the exact class of bug PR #62 fixed.
- **Recommendation**: Open a follow-up ticket to introduce `src/superclaude/cli/prd/schema.py` housing the canonical section lists. Migrate `_RESEARCH_REQUIRED_SECTIONS`, `_PRD_CRITICAL_SECTIONS`, and any analogous per-phase contracts there. Have the prompt builders import the same constants when assembling instruction text. This is not in scope for the current PR (which was correctly minimal) but is the natural next step.

### 🟢 Low (nice-to-have)

#### L1. Regex's optional-prefix shape is more permissive than the prompt schema

- **File**: `src/superclaude/cli/prd/gates.py:135`
- **Category**: api-contract (defensive permissiveness)
- **Source**: auggie
- **In diff**: yes (Edit B)
- **Evidence**:
  ```python
  phases_match = re.search(
      r"(?:^|\n)\s*#{1,4}\s+.*(?:Suggested[\s_]+)?Phases",
      content,
      re.IGNORECASE,
  )
  ```
- **Why this matters**: The prompt schema instructs `## SUGGESTED_PHASES` (underscore form), and SKILL.md uses the same. The regex tolerates a number of variants the schema does not actually emit (e.g. `## Suggested Phases`, `## Phases` alone). This is fine as defensive permissiveness — agents drift in heading capitalization — but if the gate is meant to enforce schema conformance, accepting heading shapes the schema does not produce is a slight contract weakening.
- **Recommendation**: If the intent is "be lenient" — document it with a one-line comment ("Accept space/underscore variants and bare `Phases` headings to tolerate agent drift"). If the intent is "match the schema exactly" — tighten to `^\s*#{1,4}\s+SUGGESTED_PHASES\s*$` and add a separate, weaker check for variant forms behind a warning rather than a gate-pass.

#### L2. Test fixture's trailing numbered list lands outside the SUGGESTED_PHASES section

- **File**: `tests/cli/prd/test_research_notes_roundtrip.py:73`
- **Category**: tests (clarity)
- **Source**: auggie
- **In diff**: yes (NEW file)
- **Evidence**: The fixture loop emits `## SECTION\n- detail\n\n` for each of the 7 sections, then appends `"1. Phase one detail\n"` AFTER the final section (AMBIGUITIES_FOR_USER). The test passes because the loop's per-section `- detail` bullet already satisfies `_check_suggested_phases_detail`'s list-pattern search — but the trailing numbered item is misleading: a reader inspecting the fixture would assume the numbered list is what makes the SUGGESTED_PHASES check pass, when in fact it is the unrelated `- detail` immediately under that heading.
- **Recommendation**: Either drop the trailing `1. Phase one detail` line (it's load-bearing for nothing) or move the per-agent list into the SUGGESTED_PHASES section block so the fixture reads as an honest minimal example. The accompanying comment at lines 70-72 already acknowledges this confusion; rewriting the fixture is cleaner than a comment justifying it.

#### L3. No test asserts the gate's section list matches the upstream SKILL.md source-of-truth

- **File**: `tests/cli/prd/test_research_notes_roundtrip.py:53-60`
- **Category**: tests (coverage gap)
- **Source**: auggie
- **In diff**: yes (NEW file)
- **Why this matters**: The PR body identifies SKILL.md as the authoritative source. The new round-trip test asserts `prompt ↔ gate` parity, but not `SKILL.md ↔ gate` parity. If a future edit changes SKILL.md (the upstream contract) without touching gates.py, the test still passes — the same blind spot the PR set out to close, just relocated by one level.
- **Recommendation**: Add a third assertion that parses the 7 `## SECTION` headings out of the relevant block of `src/superclaude/skills/prd/SKILL.md` (lines 280-303) and asserts they equal `_RESEARCH_REQUIRED_SECTIONS`. This is structurally identical to the prompt-extraction helper already in the file and would cost ~15 lines.

### 💬 Nits

_None._

## Architectural / Cross-Cutting Observations

- **Prompt-gate contract validation is test-only, not runtime**. The new round-trip test catches schema drift at test time. There is no startup-time or invocation-time assertion in `src/superclaude/cli/prd/executor.py` that the prompts and gates currently in scope agree on their schemas. For a pipeline whose value proposition includes "halt before producing a bad PRD," a one-time assertion at executor construction (or a `@pytest`-style invariant check) would shift detection from "next CI run" to "next CLI run." Confidence: low — this is a design call rather than a defect, and may be intentional.
- See M3 above — schema-as-data-not-code is the broader pattern that would prevent recurrence.

## Audit

- Auggie chunks: 1 (succeeded: 1, retried: 0, skipped: 0)
- Findings produced by Auggie: 6 anchored + 2 cross-cutting = 8 total
- Findings dropped during grounding: 1 (F3 — docstring "Suggested Phases" judged not actually stale; see `audit.log`)
- Findings promoted to report: 6 (3 Medium + 3 Low + 2 cross-cutting observations folded into M3 and the architectural section)
- Persona cross-check: disabled (depth=standard)
- Auggie wall clock: 112s; orchestration: ~3 min Claude time
- Recommendation per rubric: **Approve with comments** (`critical == 0 && high == 0 && medium > 0`)

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0
high: 0
medium: 3
low: 3
nit: 0
dropped: 1
auggie_chunks: 1
duration_sec: 112
-->
