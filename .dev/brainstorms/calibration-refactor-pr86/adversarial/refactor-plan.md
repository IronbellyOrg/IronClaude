# Refactor Plan

## Overview

- **Base variant**: V1 (opus:analyzer) — surgical 3-file shape
- **Incorporated from**: V3 (haiku:qa) Changes 4+5; V2 (sonnet:architect) U-001 as optional
- **Total in-scope changes**: 5 markdown deliverables (3 core file edits + 1 cultural-prior correction + 1 new pin-test corpus file). The pytest harness invocation (V3's Change 6) is deferred to a follow-up implementation commit.
- **Overall risk**: Low (additive schema, safe defaults, no in-flight card invalidation)

## Planned Changes

### Change A — Rubric (FROM V1)

- **Source**: V1, "Change 1 — escalation-rubric.md"
- **Target**: `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
- **Integration approach**: as authored in V1
- **Rationale**: V1's diff sketch is precise and minimal; V3 adopts by reference; V2's two-stage equivalent is more invasive without additional safety
- **Risk level**: Low — additive 6th dimension row + formula replacement + new modifier subsection + escalation-decision rule extension
- **Debate evidence**: S-002 80% confidence to V1's additive shape; C-001 80% confidence to V1's gated-min formula

### Change B — Card template (FROM V1, with optional U-001 from V2)

- **Source**: V1 "Change 2" + V2's typed evidence-kind table as optional
- **Target**: `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`
- **Integration approach**:
  - V1's mandatory additions: `Claim class` frontmatter, `Runtime check` self-assessment row, `Falsification standard` section
  - V2's typed evidence-kind table presented as a "recommended shape" subsection, NOT replacing the existing bulleted-list format. Cards may use either form in v1.5; v2.0 will make typed-table mandatory.
- **Rationale**: V1's additive shape preserves in-flight card compatibility; V2's typed shape is the cleaner end-state and earns its place as a recommended (not required) enhancement
- **Risk level**: Low — additive frontmatter and sections; no replacement of required fields
- **Debate evidence**: C-002 75% to V1+V2 partial; U-001 70% to optional

### Change C — Calibrator agent (FROM V1)

- **Source**: V1 "Change 3"
- **Target**: `src/superclaude/agents/confidence-calibrator.md`
- **Integration approach**: as authored in V1
- **Rationale**: V1's additive Responsibilities extension preserves the existing agent contract; V2's full rewrite (with Stage 1/2 trace + input-filter pre-step) is the v2.0 end-state, deferred
- **Risk level**: Low — instruction-text edits, no change to allowed-tools, model, or maxTurns
- **Debate evidence**: S-003 75% to V1's additive shape

### Change D — confidence-check SKILL.md scope correction (FROM V3)

- **Source**: V3 "Change 4"
- **Target**: `src/superclaude/skills/confidence-check/SKILL.md`
- **Integration approach**: replace the unqualified "Test Results 1.000/1.000" block at lines 14-18 with a scoped block per V3's diff sketch
- **Rationale**: V1 retracts its "wrong layer" rejection in Round 2; the 5-line scope correction kills the cultural-prior recursion cited in M2 §Evidence
- **Risk level**: Very Low — annotative change to a Test Results block; no behavioral impact
- **Debate evidence**: C-005 85% to V3; X-002 80% to "yes, touch SKILL.md"

### Change E — Pin-test corpus (FROM V3)

- **Source**: V3 "Change 5"
- **Target**: NEW FILE — `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`
- **Integration approach**: as authored in V3, with the addition: a stub note "Fixtures 1-6 cover v1.5 closure. Add fixtures for v2.0 evidence-kind validation when the v2.0 schema ships." (V2's Round 3 contribution)
- **Rationale**: U-003 95% confidence unanimous; this is M4's deliverable and the only mechanism preventing silent regression of Changes A-C
- **Risk level**: Low — new file; no existing-content modification
- **Debate evidence**: U-003 95% unanimous

## Changes NOT Being Made (rejected alternatives)

### Rejected: V2's mandatory `verdict_direction` + reject-malformed (deferred to v2.0)

- **Diff point**: U-002
- **V2 approach**: mandatory frontmatter, calibrator rejects v1.0 cards as `status: malformed`
- **Rationale for rejection**: migration cost (every in-flight pr86-style card invalidates) outweighs the marginal safety over V1's fail-safe default. Reaches the same end-state via a v2.0 follow-up after v1.5 has been live.
- **Debate evidence**: X-001 85% to V1's default-to-runtime_behavior

### Rejected: V2's schema v2.0 redesign (typed evidence-kind table as MANDATORY)

- **Diff point**: U-001 (in mandatory form)
- **V2 approach**: typed evidence-kind table replaces the existing bulleted-list form; calibrator rejects cards without typed kinds
- **Rationale for rejection**: same migration cost concern; the optional-shape variant is sufficient for v1.5
- **Debate evidence**: U-001 70% to optional-shape adoption

### Rejected: V2's structural input-filter for self-reported confidence (M3c)

- **Diff point**: C-004
- **V2 approach**: calibrator's input is preprocessed to byte-strip the `Self-reported confidence:` field
- **Rationale for rejection**: V2 itself flags this as out-of-scope (requires orchestrator-side preprocessing). Defer the structural masking; ship V3's P5 property test (anchoring variance bound) as the prevention mechanism.
- **Debate evidence**: C-004 70% to V3's property-test approach

### Rejected: V3's Change 6 (pytest harness invocation)

- **V3 approach**: add pytest module in `tests/troubleshoot/` that invokes the calibrator against fixtures
- **Rationale for rejection**: brainstorm deliverable is markdown-only; the pytest harness lives in `tests/` and is the implementation commit's responsibility. V3 conceded this in Round 2.
- **Debate evidence**: V3's own Round 2 rebuttal

## Risk Summary

| Change | Risk Level | Impact if wrong | Rollback |
|--------|-----------|------------------|----------|
| A (rubric) | Low | calibration scores wrong on next Tier 1 invocation | revert the dimension table + formula edits |
| B (card) | Low | new cards have a field old calibrator doesn't read | safe — old calibrator ignores unknown frontmatter fields; v1.0 cards still valid |
| C (calibrator) | Low | calibrator instruction conflicts with rubric | revert agent file |
| D (SKILL.md) | Very Low | cosmetic annotation only | trivial revert |
| E (eval cases) | Low | pin tests fail on first run if expectations wrong | adjust expected values until they reflect the correct rubric behavior; this IS the test-of-the-rubric |

## Review Status

Auto-approved (non-interactive brainstorm execution).
