# Variant 3 (haiku:scribe): ACCEPT all 10 with compensating controls

## Verdict
ACCEPT the 10 token gaps; no fourth needle round. Task 11 acceptance criteria hold; spec section 0 says this layer proves no behaviour.

## Ruling text
`T11: Ruling: Accept the 10 remaining token gaps and stop needle rounds — the three Task 11 acceptance criteria hold, and substring checks cannot converge (81% of untargeted flips and deletions still survive) — cost if wrong is a model following an unpinned paraphrase, which jq, a pinned sibling sentence, or the section 11.3 live evaluation has to catch, not this suite.`

## Compensating controls (as claimed)
| Gap | Claimed holder |
|---|---|
| G1a/b | J3 bans speculative defect; "Both anchors must be verified" asserted |
| G2a-c | neighbour sentences asserted (excluded never contributes; A1-A7 dispositions; first matching row) |
| G3a-e | step 6b asserted (missing jq_exit => failed); Status mapping "failed otherwise"; Wave 4 posts nothing when failed |
| G4 | J17; old "put them in cross-cutting" wording banned |
| G5 | J13 (claimed) |
| G6 | strict dominance and equal-rank asserted (S7 caught) |
| G7 | gate copy asserted and caught |
| G8 | row order and first-match asserted; "Verified" also at file intro |
| G9 | Location grounding copy asserted (AT-05) |
| G10 | `unproven` not posted; line 22 byte-fixed for Task 13; J6 |

## Concessions
Weak for G3 (preflight sentence could say partial; saved only by later step 6b), G7 rubric (J14 does not reject under-capped security), G1a/G5 (jq checks the ledger the model wrote, not that the right evidence/tree was used). Never accept: a gap deleting the last copy of "missing jq_exit means failed", "post nothing when failed", the A1-A7 dispositions, or the gate qualification cap.

## Definition of done
(1) every AT id asserted; (2) deleting an asserted sentence fails a test; (3) a second copy, swap or synonym is written down, not turned into another needle; (4) any rule that changes posting, status or severity is pinned once or enforced by jq. Not "no reviewer can find a survivor": that only ends by snapshotting, which collides with AT-20 (report-template sections) and fights later edits.

## Cost
No edits. Counts 43 -> 9 -> 10 of 179: not converging.

## Residual risk
Model may obey the unpinned sentence and ignore the pinned one; jq will not notice a consistent wrong ledger. Semantic effectiveness unproven until 11.3.

## Top 3 risks
1. G3: preflight says partial, run continues, Wave 4 posts an unchecked review. 2. G7 rubric: security defect graded Medium, J14 allows. 3. G1a/G5: wrong evidence class or tree certified by jq.
