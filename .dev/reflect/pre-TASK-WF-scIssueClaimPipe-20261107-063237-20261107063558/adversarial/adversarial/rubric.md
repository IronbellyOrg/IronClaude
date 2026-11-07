# Qualitative rubric for base selection (30 binary criteria, 6 dimensions)

Source: sc-adversarial-protocol Step 3 qualitative layer. Verdict per criterion is MET (1) or NOT MET (0) with Claim-Evidence-Verdict: every MET needs a specific quote or section reference from the variant; if you cannot cite evidence, the verdict is NOT MET. No partial credit.

Adaptation note (orchestrator): the variants are review cards that audit a plan against its design, not roadmaps. Read "requirements" as "the plan and design points the card audits", "risks" as "risks to the plan's delivery that the card names", "document" as "the card".

## Completeness
1. Covers all explicit requirements from the source input (the card audits every part of the plan, not a subset; the card states how many units it audited)
2. Addresses edge cases and failure scenarios of the plan
3. Includes dependencies and prerequisites (task order, test dependencies)
4. Defines success/completion criteria (what a corrected plan would pass)
5. Specifies what is explicitly out of scope or not checked

## Correctness
1. No factual errors or hallucinated claims (spot-check two citations against the repository)
2. Technical approaches are feasible with stated constraints
3. Terminology used consistently and accurately throughout
4. No internal contradictions
5. Claims supported by evidence or rationale within the card

## Structure
1. Logical ordering (most severe first, or plan order, stated)
2. Consistent hierarchy depth (each finding has the same fields)
3. Clear separation of concerns between findings
4. Navigation aids present (numbering, ids, summary counts)
5. Follows conventions of a deviation-audit card (class, location, evidence, severity)

## Clarity
1. Unambiguous language (no 'should consider', 'might', 'as appropriate')
2. Concrete rather than abstract (specific files, lines, actions)
3. Each finding has one clear purpose, summarizable in one sentence
4. Acronyms and domain terms defined or clear from context on first use
5. Actionable next steps or decision points identified

## Risk Coverage
1. Identifies at least 3 risks to delivery with likelihood or impact stated
2. Provides a mitigation or fix for each identified risk
3. Addresses failure modes and recovery (what breaks, how to recover)
4. Considers external dependencies and their failure scenarios (tests, tools, Orca, hook)
5. Includes a way to detect the risk (a test or check that would catch it)

## Invariant and Edge Case Coverage
1. Addresses boundary conditions for collections (empty, single element, maximum size)
2. Handles state interactions across component boundaries
3. Identifies guard-condition gaps (missing validation, unguarded assumptions)
4. Covers count divergence (off-by-one, inclusive or exclusive ranges, expected counts)
5. Considers interaction effects when parts of the plan combine
Floor rule: a variant scoring below 1 of 5 on this dimension is ineligible as base.
