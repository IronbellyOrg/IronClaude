# Variant 2 (sonnet:analyzer): HYBRID, fix the publish-path gaps, accept the rest by ruling

## Verdict
HYBRID. Remediate G2, G7, G9. Accept G1, G3, G4, G5, G6, G8, G10 by written ruling. Optional add-on G0: assert the seven A1-A7 Condition cells verbatim (A7 "no blocking entry" is not enforced by J3 for single records; J8 covers groups only).

## Gap table
| Gap | What breaks | Reaches | Backstop | Sev | Action |
|---|---|---|---|---|---|
| G1 | narrow rule widened / anchors swapped | local ledger fields | "Protocol and instruction claims" defs and "Both anchors must be verified" asserted; J3 needs non-empty entrypoint | Low | ACCEPT |
| G2 | unsupported consequences stay in published harm/severity; defect without other conditions; no-support listing lost | publish (a,c), local (b) | neighbour sentences asserted, none says what harm holds; no jq on harm content; oracle never reads prose | High | REMEDIATE |
| G3 | missing jq reported partial | status, hosts without jq | SKILL step 6b (asserted): missing jq_exit => failed; "failed otherwise" asserted | Low | ACCEPT |
| G4 | out-of-diff routed to cross-cutting | none | both arrays carry claim and go through admission; Wave 0/3 in_diff:false sentences asserted | Low | ACCEPT |
| G5 | uncommitted edits used as evidence | local (PR posting is PR-only) | core "git show HEAD:<path>, not the working tree" asserted; J13 PR mode | Low | ACCEPT |
| G6 | wrong non-defect group disposition / count votes | local | ranking and strict dominance asserted; J3 bans speculative defect | Low | ACCEPT |
| G7 | rubric cap inverted | publish (severity): qualified security/data-integrity capped at Medium loses inline comment and remediation | gate copy asserted so copies only conflict; J14 catches only uncapped non-security direction, misses over-cap | Med-High | REMEDIATE |
| G8 | "top to bottom", row-id recording, "Verified" def | local | row order/dispositions asserted; J4/J5 need reason ids; Verified also defined at gate line 5 | Low | ACCEPT |
| G9 | head-mismatch context rows not forced unproven | publish (defect admitted on unverifiable context) | A6 "not verified"; head_object_check==match rule asserted; location-grounding sentence covers cited lines only; J13 cannot detect false diff_new_side | Medium | REMEDIATE |
| G10 | ungrounded line becomes unproven not dropped | local; status could go partial->success | SKILL line 22 byte-identical to baseline (AT-21/Task 13); Error handling and Output Contract partial rows | Low | ACCEPT |

## Concrete assertion changes (4-5 mutation rows, ~15 lines)
1. G2 in check_at04 Claim scope: assert in full "The admitted record keeps only supported consequences in `claim.harm`." and "A candidate is a `defect` when at least one consequence is supported and every other table condition holds."; extend the "When no consequence is supported..." needle with ", and all consequences are listed in `excluded_consequences[]`".
2. G7 in check_at10: assert "whose category is not `security` or `data-integrity` and whose harm does not meet a Critical definition (including the regulatory or compliance definition), is capped at Medium".
3. G9 in check_at07 Attribution: assert "Otherwise the source is `diff_new_side`, and any row that needs the head object is `unproven` with `head_mismatch_context_unavailable`."
4. G0 optional: assert seven Condition cells of A1-A7 verbatim, one mutation row.

## Ruling for accepted seven
"G1, G3, G4, G5, G6, G8 and G10 are accepted as residuals. Mutating the unasserted sentence changes only local records, or is contradicted by another asserted sentence, a jq invariant (J2-J5, J13, J14) or the SKILL.md:22 byte-identity check. Semantic compliance is verified by the spec 11.3 live evaluation, not by these tests."

## Definition of done
1. Every AT clause has a needle. 2. Every publish-path sentence (mutation can change published content, published severity, remediation scope or run status) is asserted in full or has a named independent backstop recorded. 3. A fixed mutation probe shows zero survivors in the publish-path class; survivors only on the accepted list. 4. Operator signs the ruling. "Mutate any AT-demanded sentence" is unbounded: probe shows 81% of 467 flips and 81% of 1,112 deletions survive.

## Cost
~30-45 min, 15 lines, 4-5 rows, no src/plan/spec change.

## Residual risk
Sentence pinning proves wording, not model obedience. Task 12 binds only the table (AT-16); Task 13 reads no rule prose; 11.3 is the only semantic gate.

## Top 3 risks
1. New round names fresh survivors (S2 "then A7", S4, S6) and operator reads as failure. 2. Verbatim sentences are change detectors; golden snapshot collides with AT-20 (#### C1. at SKILL:215, gate:224). 3. Acceptances lean on backstops outside the contract module (G10 on Task 13 line-22 check; G3 on step 6b staying asserted).
