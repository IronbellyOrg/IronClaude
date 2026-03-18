# Phase Templates — Release Split Protocol

> Loaded by Parts 2 and 3 of sc:release-split-protocol. Do NOT pre-load during Part 1.

## Purpose

Output templates and structural guidance for the adversarial debate (Part 2) and execution (Part 3) phases.

---

## Part 2: Adversarial Debate Structure

### Debate Framing

The adversarial debate for release splitting is structurally different from a typical artifact comparison. The debate is about a **decision** (split vs. no-split), not about which of several artifacts is "best." Frame accordingly.

### Role Mapping (Mode B)

With Mode B variant generation, the debate roles map differently than in Mode A:

| Concern | How It's Addressed |
|---------|-------------------|
| Advocacy | Each agent's generated variant IS its advocacy — the variant embodies the agent's best analysis |
| Skepticism | The adversarial pipeline's diff analysis and debate rounds surface disagreements between variants |
| Pragmatism | The scoring and merge phase evaluates variants against hard criteria (real-world testability, overhead justification, coupling risks) |

The three conceptual roles (Advocate, Skeptic, Pragmatist) are now **emergent properties** of the adversarial pipeline rather than explicitly assigned positions. This produces more genuine disagreement because each agent commits to its full analysis rather than arguing a pre-assigned position.

### Agent-Specific Guidance

When building agent instructions, bias each agent toward its persona's strength:

| Agent Persona | Bias Toward | Key Questions to Emphasize |
|--------------|-------------|---------------------------|
| architect | Structural analysis | "Where are the natural module boundaries? What are the dependency chains? Is there a foundation-vs-application seam?" |
| analyzer | Risk and feasibility | "What are the real costs of splitting? Does Release 1 actually enable tests that matter? What coupling risks exist?" |
| security | Trust boundaries | "Does the split create new attack surfaces? Are auth/access changes atomic or split across releases?" |
| qa | Validation quality | "Can Release 1 be meaningfully tested in isolation? Are the test scenarios real-world or synthetic?" |

### Fallback Role Specifications (Mode A)

If Mode B fails and the skill falls back to Mode A, use these conceptual roles:

**Advocate** (argues FOR the proposal):
- Present the strongest case for the proposed decision
- Identify concrete benefits with evidence from the spec
- Address risks proactively rather than waiting for the skeptic
- If the proposal says "split": demonstrate that Release 1 enables real-world validation that wouldn't otherwise happen
- If the proposal says "don't split": demonstrate that the release is coherent and the risks of splitting outweigh the benefits

**Skeptic** (argues AGAINST the proposal):
- The skeptic's job is to find the strongest counterargument, not to nitpick
- If the proposal recommends splitting:
  - Is the split boundary artificial? Does it create a seam where none naturally exists?
  - Does Release 1 actually enable meaningful testing, or just "we shipped something"?
  - Is the coordination overhead of two releases justified?
  - Could Release 1 create a false sense of confidence (tests pass, but the hard parts are all in Release 2)?
  - Would users or operators encounter a confusing intermediate state?
- If the proposal recommends NOT splitting:
  - Is there a valid split point that was missed or dismissed too quickly?
  - Are the risks of a monolithic release being underestimated?
  - Could earlier feedback on a subset prevent costly rework in the full release?
  - Is "keep it together" actually just risk-avoidance masquerading as good engineering?

**Pragmatist** (evaluates against hard criteria):
- Does Release 1 enable REAL-WORLD tests that couldn't happen without shipping it?
- Is the overhead of two releases justified by the feedback velocity gained?
- Are there hidden coupling risks where Release 1 without Release 2 creates a misleading validation signal?
- What is the blast radius if the split decision is wrong?
- What would it take to reverse the decision later?

### Debate Output Template

```markdown
# Adversarial Review — Release Split Proposal

## Original Proposal Summary
[1-2 paragraph summary of the Part 1 proposal]

## Advocate Position
[Strongest arguments FOR the proposal]

## Skeptic Position
[Strongest arguments AGAINST the proposal]

## Pragmatist Assessment
[Evaluation against hard criteria]

## Key Contested Points
| Point | Advocate | Skeptic | Pragmatist | Resolution |
|-------|----------|---------|------------|------------|
| ... | ... | ... | ... | ... |

## Verdict: [SPLIT / DON'T SPLIT / SPLIT-WITH-MODIFICATIONS]

### Decision Rationale
[Why this verdict was reached]

### Strongest Argument For
[The single most compelling argument for the verdict]

### Strongest Argument Against
[The single most compelling argument against the verdict — what would change the decision]

### Remaining Risks
[Risks that persist regardless of the decision]

### Confidence-Increasing Evidence
[What evidence would most increase confidence in this decision]

### Modifications (if SPLIT-WITH-MODIFICATIONS)
[Specific changes to the original proposal]
```

---

## Part 3: Execution Templates

### Release Spec Template (Split)

```markdown
---
release: [1 or 2]
parent-spec: [path to original spec]
split-proposal: [path to split-proposal-final.md]
scope: [brief scope description]
status: draft
validation-gate: [for R2: "blocked until R1 real-world validation passes"]
---

# Release [N] — [Title]

## Objective
[Single paragraph describing what this release achieves independently]

## Scope

### Included
[Numbered list of requirements/deliverables assigned to this release]
[Each item references its source in the original spec: "From: [original-spec] Section X.Y"]

### Excluded (assigned to Release [other])
[Numbered list of items intentionally NOT in this release]
[Each item references where it went: "Deferred to: Release [other], Section X.Y"]

## Dependencies

### Prerequisites (from Release [other], if R2)
[What must be complete and validated before this release can proceed]

### External Dependencies
[Dependencies outside the release split scope]

## Real-World Validation Requirements
[Specific scenarios to execute post-deploy]
[Each scenario must use actual functionality in production-like conditions]
[No mocks, no simulated tests]

## Success Criteria
[Measurable criteria for this release being "done"]

## Planning Gate (Release 2 only)
> This release's roadmap and tasklist generation may proceed only after Release 1
> has passed real-world validation and the results have been reviewed.
>
> Validation criteria: [specific criteria from Release 1]
> Review process: [who reviews, what they look for]
> If validation fails: [what happens — revision, rollback, merge back to single release]

## Traceability
[Summary table mapping this release's items back to original spec sections]
```

### Boundary Rationale Template

```markdown
# Split Boundary Rationale

## Split Point
[Description of where the boundary falls]

## Why This Boundary
[Evidence-based reasoning for choosing this split point]

## Release 1 Delivers
[What Release 1 provides independently — value, testability, foundation]

## Release 2 Builds On
[What Release 2 adds, and why it depends on Release 1 being validated first]

## Cross-Release Dependencies
| Release 2 Item | Depends On (Release 1) | Type | Risk if R1 Changes |
|----------------|----------------------|------|---------------------|
| ... | ... | hard/soft | ... |

## Integration Points
[Where Release 1 and Release 2 connect — APIs, schemas, contracts, behaviors]

## Handoff Criteria
[What must be true about Release 1 before Release 2 planning begins]

## Reversal Cost
[What it would cost to reverse the split decision and merge back into a single release]
```

### Single Release Validation Template (No Split)

```markdown
---
parent-spec: [path to original spec]
split-analysis: "no-split-recommended"
rationale: [brief rationale]
status: validated
---

# [Release Title] — Validated Spec

## Why This Release Stays Intact
[Evidence from the analysis showing that splitting would not add value]

## Risks Addressed Without Splitting
[How the risks identified during analysis are mitigated within a single release]

## Validation Strategy
[How to get early feedback without splitting — feature flags, staged rollout, canary testing, etc.]

## Original Spec Updates
[Any improvements identified during the analysis, incorporated into the spec]

## Traceability
[Confirmation that all original requirements are preserved]
```
