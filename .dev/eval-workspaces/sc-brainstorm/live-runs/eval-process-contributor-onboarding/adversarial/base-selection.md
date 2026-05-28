---
phase: base-selection
created: 2026-05-27T00:00:00Z
---

# Base Selection

## Scoring Rubric

Variants scored on five axes (1-5 scale):

| Axis | Variant 1 (Scribe) | Variant 2 (PM) | Variant 3 (Architect) |
|------|--------------------|----------------|------------------------|
| Sprint-shippability | 5 | 3 | 4 |
| Independence from volume | 5 | 2 | 5 |
| Coverage of pain points | 3 | 4 | 4 |
| Composability with other variants | 4 | 4 | 4 |
| Measurable success metrics | 4 | 4 | 5 |
| **Total** | **21** | **17** | **22** |

## Decision

**Base = Variant 3 (Architect / Haiku — Tooling-First).** Highest total, strongest on the agile constraint (sprint-shippable, volume-independent, measurable). Tooling fixes (hooks, `make onboard`, doctor, smoke tests) are the most leveraged single bet for a constrained sprint.

## Rationale

- Tooling is durable: docs decay, process needs participants, but a fixed hook UX or a `make onboard` target keeps paying off without ongoing care.
- Tooling unblocks the other two: Scribe's failure-mode appendix becomes unnecessary if hooks self-explain; PM's PR-template prompts can recommend `make onboard` instead of a 5-step manual.
- Architect's variant has the lowest implementation risk — every proposed improvement is a small additive change to existing infrastructure.

## What the base does NOT cover (gap → refactor plan)

- No QUICKSTART.md or glossary (Scribe's contribution).
- No PR template auto-comment with shepherd ping (PM's contribution).
- No worked-example skill PR (deferred to Phase 2).
- No cohort cadence (deferred to Phase 2 pending volume signal).

These gaps will be filled in by the refactor-plan layering Variant 1 and Variant 2 elements on top of Variant 3.
