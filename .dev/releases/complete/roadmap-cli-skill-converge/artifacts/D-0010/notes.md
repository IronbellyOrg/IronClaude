# D-0010 — Notes: B-10 packaging deferral

**Task:** T04.01
**Roadmap Item:** R-010

## Authorization scope

**No packaging split is authorized by B-10 in this release.**

The following changes are explicitly **not** authorized under this
decision:

- Creating `src/superclaude/skills/sc-validate-roadmap-protocol/refs/`.
- Creating `src/superclaude/skills/sc-validate-roadmap-protocol/rules/`.
- Creating `src/superclaude/skills/sc-validate-roadmap-protocol/templates/`.
- Moving sections of `SKILL.md` (e.g., extraction, decomposition,
  adversarial review, remediation, CC-agent dispatch) into separate
  `refs/*.md` files.
- Any structure-only refactor whose only justification is parity with
  the sibling `sc-roadmap-protocol/` skill, which does carry a `refs/`
  directory.

## Why this is a deferral, not a rejection

B-10 is not refuted. The three solutions in `solutions.md:336-361`
(full factor / leave as-is / lazy-split) remain on the table for a
later release. What is rejected is performing that work **now**, in
this release, without empirical evidence of load or token cost.

## Tier routing

This task is **EXEMPT**: it records a decision rather than editing
implementation code. Per the tier conflict note in
`phase-4-tasklist.md:57`, EXEMPT wins over STANDARD because no
implementation surface is touched.

## Interaction with B-9

B-9 (handled by T03.01/D-0009) chose Option 2 — preserve the deep
protocol, add a Relationship-to-CLI header and crosswalk. With B-9
landed in its preserved form, the case for B-10 Solution 2 ("leave
as-is") is the cheapest correct option for this release per
`solutions.md:343,352`. Factoring (Solution 1) becomes interesting
only if a future review surfaces measured load or token pain — see
`spec.md` for the revisit condition.

## What a future review would need to find

A future review that re-opens B-10 should report at minimum one of:

- Measured on-load token cost of `SKILL.md` that affects skill
  selection or context budget in a reproducible way.
- Maintenance friction (e.g., merge conflicts, drift between
  sub-sections) that a `refs/` split would demonstrably reduce.
- Reuse demand from another skill for a self-contained section of
  `SKILL.md` (the lazy-split case in `solutions.md:354-361`).

Absent any of those, the deferral stands.
