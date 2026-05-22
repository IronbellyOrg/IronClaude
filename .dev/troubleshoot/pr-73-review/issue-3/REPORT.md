# Troubleshoot Report — Issue 3: Wave 1 hypothesis formation references Card before Wave 1.5 produces it

**Target**: auggie review #3290499065 on PR #73
**Tier reached**: 1
**Confidence**: 0.95
**Status**: success

## Root cause

`SKILL.md` Wave Structure code-block at lines 75-84 lists `Wave 1: Tier 1 — Triage` and `Wave 1.5: Documentation Grounding` as fully-sequential sibling waves, but the body of Wave 1 step 3 (line 144) requires the `root-cause-analyst` agent to consume the Documentation Context Card at `<output-dir>/doc-context.md` — a file that is only produced by Wave 1.5 step 4 (line 169). The intended interleaving (Wave 1 step 1 → Wave 1.5 → Wave 1 steps 2-3) is only documented inside Wave 1.5's Goal (line 156) and Preconditions (line 158), which a top-down reader doesn't see before executing Wave 1.

## Proposed Fix (Option B — structurally cleaner)

Split Wave 1 into two waves with Wave 1.5 explicitly between them.

**Edit 1 — `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave Structure block (lines 75-84)**

Replace:
```
Wave 0: Parse + Validate Input
Wave 1: Tier 1 — Triage          ← always; loads refs/triage-checklist.md on demand
Wave 1.5: Documentation Grounding ← always; loads refs/doc-discovery.md on demand; skipped only by --no-doc-discovery
Wave 2: Confidence Gate          ← decides escalation via refs/escalation-rubric.md
```

With:
```
Wave 0: Parse + Validate Input
Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + reproduce only)
Wave 1.5: Documentation Grounding    ← always; loads refs/doc-discovery.md on demand; skipped only by --no-doc-discovery
Wave 1.7: Tier 1 — Hypothesis Formation ← always; consumes Wave 1.5 Documentation Context Card; produces single hypothesis card + calibration
Wave 2: Confidence Gate              ← decides escalation via refs/escalation-rubric.md
```

**Edit 2 — `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 1 body (lines 128-150)**

Rename `### Wave 1: Tier 1 — Triage` to `### Wave 1: Tier 1 — Real-Code Grounding`. Keep only step 1 (real-code grounding via auggie + serena) and step 2 (reproduce/observe). Update **Exit criteria** to "Real-code grounding complete; observation captured. Hand off to Wave 1.5."

**Edit 3 — Insert new `### Wave 1.7: Tier 1 — Hypothesis Formation` section** between Wave 1.5 (ends ~line 188) and Wave 2 (line 192). Section contains the moved step 3 (root-cause-analyst spawn — body byte-identical, but now Card is guaranteed available) and step 3.5 (confidence-calibrator). Exit criteria: "One hypothesis card at `<output-dir>/tier1-hypothesis.md`, a calibration report, and calibrated confidence in audit log. Emit 'Wave 1.7 complete: confidence=<x>'." Token budget line moved from old Wave 1 (line 150) to here.

**Edit 4 — Update Wave 1.5 precondition (line 158)** from "Wave 1 step 1 (real-code grounding) is complete" to "Wave 1 (real-code grounding) is complete".

**Edit 5 — Update Refs loader table (lines 429-435)** to point `refs/triage-checklist.md`, `refs/hypothesis-card-template.md`, and `refs/escalation-rubric.md` references at the new Wave 1.7 instead of Wave 1 where appropriate (triage-checklist stays at Wave 1; hypothesis-card moves to Wave 1.7+Wave 3).

**Edit 6 — Audit emission strings** elsewhere in SKILL.md that say "Wave 1 complete" should be reviewed for whether they refer to grounding-only completion (stay as Wave 1) or hypothesis completion (move to Wave 1.7).

## Files that MUST NOT change

- `src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md` — still loaded by Wave 1 grounding step
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md` — Wave 1.5 internal
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — schema unchanged, only the consumer wave label changes

## Risk + Rollback

Medium-low. Wave-renumbering is more invasive than text-only edits but contained to one skill file. The functional behavior of each step is unchanged — only the wave name/number labels move. Rollback = `git revert`.
