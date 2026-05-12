# Release Split Pipeline — Reusable 4-Phase Prompt

> **Purpose**: Evaluate whether a release should be split into two sequential releases to enable earlier real-world testing and faster iteration. Produces an auditable fidelity-verified result.
>
> **Usage**: Replace `{SPEC_PATH}` with the path to your release spec/roadmap. Run phases sequentially.

---

## Phase Sequence

| Phase | Command | Purpose |
|-------|---------|---------|
| 1 | `/sc:brainstorm` | Socratic discovery — find the natural split point (or confirm there isn't one) |
| 2 | `/sc:adversarial` | Debate the proposal — validate, refute, or refactor |
| 3 | `/sc:tasklist` | Execute the split — produce two spec-aligned tasklist bundles |
| 4 | `/sc:adversarial` | Fidelity audit — 100% coverage verification between original and split specs |

**Smart Flags**: `--seq --ultrathink --evidence --validate`

---

## PHASE 1 — Discovery & Proposal

**Command**: `/sc:brainstorm --interactive --seq`

```
CONTEXT:
I have a release spec at {SPEC_PATH}. I need to evaluate whether this
release should be split into two sequential releases (Release A →
Release B) to enable earlier real-world testing and faster iteration.

IMPORTANT CONSTRAINTS:
- Splitting is NOT assumed to be the right answer. Keeping the release
  intact is equally valid. The analysis must be unbiased.
- "Split" does NOT mean cutting the sprint in half by effort. It means
  identifying a natural seam where Release A delivers independently
  testable, independently valuable functionality that Release B builds on.
- ALL testing must be real-world usage in production-like conditions.
  No mocks, no simulated tests, no synthetic validation. If a split
  point doesn't enable real-world testability, it's not a valid split.

DISCOVERY QUESTIONS TO EXPLORE:
1. What are the dependency chains in this spec? Which features are
   prerequisites for others?
2. Are there components that deliver standalone value and could be
   validated through real-world use before the rest ships?
3. What is the cost of splitting? (integration overhead, context
   switching, release management burden, potential rework)
4. What is the cost of NOT splitting? (delayed feedback, big-bang
   risk, harder root-cause isolation if something fails)
5. Is there a natural "foundation vs. application" boundary — where
   Release A lays infrastructure that Release B consumes?
6. Could splitting actually INCREASE risk by shipping an incomplete
   mental model to users or creating a half-baked intermediate state?

DELIVERABLE:
Produce a PROPOSAL document with:
- RECOMMENDATION: Split or Don't Split (with confidence level)
- If Split:
  - Release A scope (what ships, what's testable, what value it delivers)
  - Release B scope (what depends on A, what new value it adds)
  - The seam: why THIS is the right split point
  - Real-world test plan for Release A (specific scenarios, not abstractions)
  - Risks of the split and mitigations
- If Don't Split:
  - Why the release is better kept intact
  - What risks remain and how to mitigate them without splitting
  - Alternative strategies for early validation without splitting

Save the proposal to: {SPEC_PATH}/../split-proposal.md
```

---

## PHASE 2 — Adversarial Validation

**Command**: `/sc:adversarial --seq --ultrathink`

```
ARTIFACTS:
1. Original release spec: {SPEC_PATH}
2. Split proposal: {SPEC_PATH}/../split-proposal.md

DEBATE STRUCTURE:
- Variant 1 (Advocate): Argues FOR the proposal as written
- Variant 2 (Skeptic): Argues AGAINST the proposal — specifically:
  - If the proposal recommends splitting: argue that the split is
    artificial, adds overhead, doesn't enable meaningfully earlier
    testing, or creates a worse intermediate state
  - If the proposal recommends NOT splitting: argue that there IS a
    valid split point that was missed, and that the risks of a
    monolithic release are being underestimated
- Variant 3 (Pragmatist): Evaluates both positions against these
  hard criteria:
  - Does Release A (if split) enable REAL-WORLD tests that couldn't
    happen without shipping it? Not unit tests. Not integration tests.
    Actual usage by actual users or realistic user-proxy scenarios.
  - Is the overhead of two releases justified by the feedback velocity
    gained?
  - Are there hidden coupling risks where Release A without B creates
    a misleading validation signal?

CRITICAL RULE: The debate MUST genuinely consider that the split was
a mistake. This is not a rubber-stamp exercise. If the skeptic wins,
the output should be "Don't Split" with reasoning.

DELIVERABLE:
- Debate transcript
- Merged verdict: SPLIT / DON'T SPLIT / SPLIT-WITH-MODIFICATIONS
- If SPLIT or SPLIT-WITH-MODIFICATIONS: revised proposal incorporating
  debate findings, saved to: {SPEC_PATH}/../split-proposal-final.md
- If DON'T SPLIT: explanation of why, with alternative validation
  strategies, saved to same path
```

---

## PHASE 3 — Execution

**Command**: `/sc:tasklist --validate`

```
INPUT: {SPEC_PATH}/../split-proposal-final.md

CONDITIONAL EXECUTION:
- If Phase 2 verdict was DON'T SPLIT: Generate a single tasklist from
  the original spec as-is. Skip to Phase 4 for baseline fidelity check.
- If Phase 2 verdict was SPLIT or SPLIT-WITH-MODIFICATIONS:

  Generate TWO tasklist bundles:

  BUNDLE 1 — Release A:
  - Scope: Only items assigned to Release A in the final proposal
  - Must include: real-world validation tasks (not test stubs — actual
    scenarios to execute post-deploy)
  - Output: {SPEC_PATH}/../release-a/tasklist-index.md

  BUNDLE 2 — Release B:
  - Scope: Only items assigned to Release B in the final proposal
  - Must include: dependency declarations on Release A deliverables
  - Must include: validation that Release A's real-world test results
    were reviewed before Release B begins
  - Output: {SPEC_PATH}/../release-b/tasklist-index.md

CROSS-REFERENCE REQUIREMENT:
Every task in both bundles must trace back to a specific requirement
in the original spec. No orphan tasks. No invented scope.
```

---

## PHASE 4 — Fidelity Audit

**Command**: `/sc:adversarial --seq --ultrathink --evidence`

```
ARTIFACTS:
1. Original release spec: {SPEC_PATH}
2. Release A tasklist: {SPEC_PATH}/../release-a/tasklist-index.md
3. Release B tasklist: {SPEC_PATH}/../release-b/tasklist-index.md
   (If not split: single tasklist vs original spec — 2 artifacts only)

PURPOSE: Auditable verification of 100% fidelity between the original
spec and the split outputs.

AUDIT PROTOCOL:
- Variant 1 (Enumerator): Extracts EVERY discrete requirement, feature,
  acceptance criterion, constraint, and non-functional requirement from
  the original spec. Produces a numbered checklist.
- Variant 2 (Mapper): For each item on the checklist, identifies WHERE
  it appears in Release A or Release B tasklists. Flags any item that:
  - Is missing entirely (CRITICAL — fidelity breach)
  - Is partially covered (WARNING — scope drift risk)
  - Is duplicated across both releases (INFO — potential rework)
  - Was added but doesn't trace to original spec (WARNING — scope creep)
- Variant 3 (Auditor): Reviews the mapping for accuracy. Challenges
  any "covered" claims that look like stretches. Produces final verdict.

DELIVERABLE — Fidelity Report:
  Save to: {SPEC_PATH}/../fidelity-audit.md

  Contents:
  - Coverage matrix: original requirement → Release A/B location
  - PASS/FAIL verdict (PASS = 100% coverage, zero CRITICAL flags)
  - List of all findings by severity (CRITICAL / WARNING / INFO)
  - If FAIL: specific items that need to be added to which release
  - Sign-off statement: "All {N} requirements from {SPEC_PATH} are
    represented across Release A and Release B with full fidelity"
    OR "Fidelity gaps found — {N} items require remediation"
```

---

## Quick-Start

Run each phase sequentially. Each phase depends on the previous output.

```bash
# Phase 1: Discovery
/sc:brainstorm    # paste Phase 1 prompt with your {SPEC_PATH}

# Phase 2: Debate
/sc:adversarial   # paste Phase 2 prompt

# Phase 3: Execute
/sc:tasklist      # paste Phase 3 prompt

# Phase 4: Verify
/sc:adversarial   # paste Phase 4 prompt
```

## Key Design Decisions

- **No bias**: Every phase explicitly considers "don't split" as a valid outcome
- **Real-world only**: Phase 1 constraints and Phase 3 validation tasks enforce no-mock testing
- **Auditable**: Phase 4 produces a numbered, traceable coverage matrix — not a summary judgment
- **Reusable**: Replace `{SPEC_PATH}` for any release; the logic is spec-agnostic
- **Iterative**: If Phase 4 fails, fix the gaps and re-run Phase 4 until PASS
