# 30-criterion additive binary rubric (adversarial protocol Step 3, qualitative layer)

Artifact type under evaluation: a reviewer card (a read-only audit of the plan `.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md` against its `source.md`). "The source input" for criterion C1 means the audit task itself: audit the plan against the source and report deviations, gaps and risks.

Each criterion is MET (1) or NOT MET (0), no partial credit. Every MET needs a specific evidence citation (a quote or a finding id from the card). If you cannot cite evidence, the verdict is NOT MET.

## Completeness
- C1 Covers all explicit audit requirements (plan against source; Task acceptance observable; coverage judgement stated)
- C2 Addresses edge cases and failure scenarios of the plan's tasks
- C3 Includes dependencies and prerequisites of the plan (entry checks, ordering, tests that pin the edited files)
- C4 Defines success/completion criteria for its own fixes
- C5 Specifies what is out of scope or authorized (for example items the source authorizes through Revision 4)

## Correctness
- C6 No factual errors or hallucinated claims (check at least two cited file:line against the live repository)
- C7 Technical approaches it recommends are feasible with the stated constraints
- C8 Terminology used consistently and accurately
- C9 No internal contradictions within the card
- C10 Claims supported by evidence or rationale within the card

## Structure
- C11 Logical ordering of findings (blocking first, or grouped)
- C12 Consistent finding format (id, class, severity, location, evidence, fix)
- C13 Clear separation of concerns between findings (no duplicated findings)
- C14 Navigation aids (ids, cross-references, a verdict line)
- C15 Follows the reviewer-card format the brief asked for

## Clarity
- C16 Unambiguous language (no "might", "should consider")
- C17 Concrete rather than abstract (specific files, lines, commands)
- C18 Each finding can be summarized in one sentence
- C19 Terms defined on first use
- C20 Actionable next steps or decision points clearly identified

## Risk Coverage
- C21 Identifies at least 3 risks with impact assessment
- C22 Provides a mitigation (fix) for each identified risk
- C23 Addresses failure modes (what happens if the plan is run as written)
- C24 Considers external dependencies and their failure (existing tests, plugin twins, ledger)
- C25 Includes a validation mechanism for risk detection (a command or check that shows the fix worked)

## Invariant & Edge Case Coverage
- C26 Addresses boundary conditions for collections (empty, single-element, maximum size)
- C27 Handles state variable interactions across component boundaries
- C28 Identifies guard condition gaps (missing validation, unguarded assumptions)
- C29 Covers count divergence scenarios (off-by-one, inclusive and exclusive ranges, counts that do not add up)
- C30 Considers interaction effects when features or components combine

Edge-case floor: a variant scoring less than 1 of 5 in the last dimension is ineligible as base (suspended with a warning when all variants score 0 of 5).
