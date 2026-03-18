# Refactoring Tasklist: Overlap Analysis Alignment

## Goal

Implement the validated corrections and coordination notes across the overlap analysis document and the three related specs, in a format optimized for `/sc:task-unified` execution.

## Scope

Target files:
- `.dev/releases/backlog/v3.0_fidelity-refactor_/overlap-analysis-consolidated.md`
- `.dev/releases/backlog/v3.0_fidelity-refactor_/wiring-verification-gate-v1.0-release-spec.md`
- `.dev/releases/backlog/v3.05_Anti-instincts_/anti-instincts-gate-unified.md`
- `.dev/releases/backlog/v3.1_unified-audit-gating-v1.2.1/spec-refactor-plan-merged.md`

## Prerequisites

- All 4 target files are present at the paths above
- Branch: `v3.0-AuditGates`
- This is a documentation/spec refactor only; no executable code changes are required

---

## Phase 1: Fix the Analysis Document

All edits in this phase target:
`/config/workspace/IronClaude/.dev/releases/backlog/v3.0_fidelity-refactor_/overlap-analysis-consolidated.md`

### Task 1.1 — Normalize path and fix orphan-detection precision

```text
/sc:task-unified Edit overlap-analysis-consolidated.md:
  E1 (line 9): Ensure v3.1 source path reads exactly:
    "v3.1_unified-audit-gating-v1.2.1/spec-refactor-plan-merged.md"
  E2 (line 68, OL-1.3): Replace "Python files in steps/, handlers/,
    validators/ with zero importers" with "exported functions in Python
    files within steps/, handlers/, validators/, checks/ directories
    with zero importers"
```

- Expected tier: LIGHT
- Inputs: `overlap-analysis-consolidated.md`
- Outputs: Same file with 2 precision fixes
- Verify:
  - v3.1 path matches filesystem path exactly
  - `checks/` is included
  - wording describes exported functions, not files

### Task 1.2 — Fix forensic attribution of `step_runner=None`

```text
/sc:task-unified Edit overlap-analysis-consolidated.md OL-1.4:
  The current text attributes "step_runner=None" as shared forensic
  evidence across both Wiring Verification and Anti-Instincts.
  Anti-Instincts does NOT reference step_runner=None — only the
  cli-portify no-op bug generally.

  Replace the OL-1.4 verdict text with:
  "Both cite the cli-portify no-op bug and the orphaned-steps evidence.
  Wiring Verification additionally references the step_runner=None
  default. If both ship, the same root defect class is prevented by
  multiple redundant mechanisms."
```

- Expected tier: LIGHT
- Inputs:
  - `overlap-analysis-consolidated.md`
  - `anti-instincts-gate-unified.md` for verification
- Outputs: Corrected forensic attribution
- Verify:
  - `step_runner=None` is no longer attributed to Anti-Instincts
  - cli-portify no-op bug remains referenced

### Task 1.3 — Fix G-012 misidentification

```text
/sc:task-unified Edit overlap-analysis-consolidated.md OL-2.5:
  G-012 is currently called "Silent Success Detection" — this is
  incorrect. G-012 is the Smoke Test Gate. SilentSuccessDetector is a
  separate post-execution hook.

  Replace the OL-2.5 content with:
  "Unified Audit Gating defines two behavioral protections: G-012
  (Smoke Test Gate — a release-tier blocking gate validating real
  artifact production) and SilentSuccessDetector (a post-execution
  hook detecting no-op pipeline runs). Wiring Verification catches
  the same defect class statically. These complement each other —
  G-012 + SilentSuccessDetector are symptom detection; Wiring
  Verification is root-cause detection. Low redundancy."
```

- Expected tier: LIGHT
- Inputs:
  - `overlap-analysis-consolidated.md`
  - `spec-refactor-plan-merged.md` for verification
- Outputs: Corrected G-012 identification
- Verify:
  - G-012 is described as Smoke Test Gate
  - SilentSuccessDetector is named separately

### Task 1.4 — Apply wording corrections

```text
/sc:task-unified Edit overlap-analysis-consolidated.md:
  E5 (line 134): Replace:
    "D-03/D-04 are a strict subset of Anti-Instincts' fingerprint +
    integration contract modules."
  With:
    "D-03/D-04 materially overlap with a narrower subset of
    Anti-Instincts' fingerprint and integration-contract coverage."

  E6 (lines 152-155): Replace:
    "All three analysts independently confirmed: **none of the three
    specs contradict each other.** They define separate gates, target
    different pipeline positions, and use the same
    GateCriteria/SemanticCheck infrastructure without modifying it.
    All three can coexist."
  With:
    "No direct contradictions were identified among the three base
    specs at the gate-definition level; the main concerns are overlap,
    merge-conflict risk, and duplicated governance patterns. They
    define separate gates, target different pipeline positions, and
    use the same GateCriteria/SemanticCheck infrastructure. All three
    can coexist with coordination."
```

- Expected tier: LIGHT
- Inputs: `overlap-analysis-consolidated.md`
- Outputs: Two wording replacements
- Verify:
  - "strict subset" no longer appears in this claim
  - unscoped "none of the three specs contradict each other" no longer appears

### Phase 1 Gate

All 4 tasks complete before moving on. The consolidated overlap analysis should be factually aligned with the verified source specs.

---

## Phase 2: Add Cross-References and Coordination Notes to the 3 Specs

### Task 2.1 — Wiring Verification: rollout integration and merge coordination

Target file:
`/config/workspace/IronClaude/.dev/releases/backlog/v3.0_fidelity-refactor_/wiring-verification-gate-v1.0-release-spec.md`

```text
/sc:task-unified Edit wiring-verification-gate-v1.0-release-spec.md:
  E7: In Section 8 (Rollout Plan), add a subsection or note:
    "### Rollout Framework Integration
    This rollout plan SHOULD adopt the Unified Audit Gating rollout
    infrastructure (SS7.1/SS7.2 profiles, override governance,
    rollback triggers) rather than defining independent thresholds.
    The thresholds in this section serve as initial values to be
    configured within that framework."

  E8: In Section 4.6 or as a new "Implementation Coordination"
    section, add:
    "### Implementation Coordination
    When modifying roadmap/gates.py, coordinate with:
    - Anti-Instincts (ANTI_INSTINCT_GATE addition)
    - Unified Audit Gating (D-03/D-04 SPEC_FIDELITY_GATE extensions)
    Preferred approach: single coordinated PR or sequenced PRs with
    explicit rebase points to avoid merge conflicts."
```

- Expected tier: LIGHT
- Inputs: `wiring-verification-gate-v1.0-release-spec.md`
- Outputs: 2 new coordination notes
- Verify:
  - rollout note is present in Section 8
  - merge-coordination note is present

### Task 2.2 — Anti-Instincts: D-03/D-04 coexistence and merge coordination

Target file:
`/config/workspace/IronClaude/.dev/releases/backlog/v3.05_Anti-instincts_/anti-instincts-gate-unified.md`

```text
/sc:task-unified Edit anti-instincts-gate-unified.md:
  E9: Near Section 8 (gate definition area), add:
    "### Coexistence with Unified Audit Gating D-03/D-04
    D-03/D-04 (Unified Audit Gating SS13.4) materially overlap with
    this spec's fingerprint and integration-contract modules. If both
    ship:
    - D-03/D-04 should be made conditional on ANTI_INSTINCT_GATE not
      being active, OR
    - Both coexist as defense-in-depth with documented deduplication
      policy

    When modifying roadmap/gates.py, coordinate with Wiring
    Verification (WIRING_GATE) and Unified Audit Gating (D-03/D-04)
    to avoid merge conflicts."
```

- Expected tier: LIGHT
- Inputs: `anti-instincts-gate-unified.md`
- Outputs: 1 new coordination section
- Verify:
  - overlap/coexistence note is present
  - merge coordination note is present

### Task 2.3 — Unified Audit Gating: conditionality and rollout consumer note

Target file:
`/config/workspace/IronClaude/.dev/releases/backlog/v3.1_unified-audit-gating-v1.2.1/spec-refactor-plan-merged.md`

```text
/sc:task-unified Edit spec-refactor-plan-merged.md:
  E10: In SS13.4 (D-03/D-04 section), add note:
    "**Overlap Note**: D-03/D-04 materially overlap with
    Anti-Instincts' fingerprint and integration-contract modules.
    If Anti-Instincts ships first, D-03/D-04 should be gated behind
    a feature flag or made conditional. D-03/D-04's value proposition
    is rapid independent deployment (~6 hours) as interim protection."

  E11: In SS7.1/SS7.2 or rollout section, add note:
    "**Consumer Note**: The Wiring Verification Gate should consume
    this rollout framework rather than defining independent
    thresholds. Ensure the profile system
    (strict/standard/legacy_migration) accommodates Wiring
    Verification gate parameters."
```

- Expected tier: LIGHT
- Inputs: `spec-refactor-plan-merged.md`
- Outputs: 2 new coordination notes
- Verify:
  - overlap note appears in SS13.4
  - consumer note appears in rollout section

### Phase 2 Gate

All 3 tasks complete. All three specs should explicitly acknowledge overlap, sequencing, or framework-consumer relationships.

---

## Execution Summary

| Phase | Tasks | Expected Tier | Files Modified |
|---|---|---|---|
| 1 | 1.1, 1.2, 1.3, 1.4 | LIGHT | 1 file |
| 2 | 2.1, 2.2, 2.3 | LIGHT | 3 files |
| Total | 7 tasks | LIGHT | 4 files |

## Parallelization Guidance

- Tasks 1.1–1.4 can run in parallel because they touch separate sections of the same analysis doc and are logically independent.
- Tasks 2.1–2.3 can run in parallel because they modify different files.
- Recommended order:
  1. Finish Phase 1
  2. Review consolidated analysis for correctness
  3. Execute Phase 2 in parallel

## Definition of Done

- The consolidated overlap analysis no longer contains the known factual inaccuracies
- The three specs include explicit coordination notes for overlap and rollout governance
- No new contradictions are introduced
- All edits are documentation-only and preserve original intent while improving precision and implementation guidance
