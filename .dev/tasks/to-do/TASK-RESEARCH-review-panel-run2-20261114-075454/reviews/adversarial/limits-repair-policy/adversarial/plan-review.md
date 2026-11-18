# Plan Review: refactor-plan.md, slot C-06 limits-repair-policy

Plan reviewed: `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/limits-repair-policy/adversarial/refactor-plan.md`

Result: 3 HIGH, 7 MEDIUM, 5 LOW defects. Read-only review; this is the only file written.

Repo cites and figures that hold: `merge_cmd.py:99-118`, `:109-116`; `ledger.py:114-118`, `:128`, `:150-157`; `cluster_cmd.py:151`, `:155-163`; `verify_cmd.py:133`, `:136-138`; `manifest.py:371-383`; the five test pins; `card_convert.py:200-201`; `test_review_ledger.py:352-361`, `:373`; `test_shadow_skill_contract.py:229-232`. Also correct: 10/273, 79/855, 70/70, 89/89, 24/28, 85.7%, 39 (audit-D's 42 minus the 3 wrong PASSes, per `score-reeval.md`), and the 2/3 and 3/4/5 pin-site counts.

## HIGH

1. **Change 1 decides the claim question and contradicts Change 7.** It says "never any other field" and calls both advocates' bullet 1 "identical in substance". A's bullet 1 also cuts `claim` to 297 plus `...`; only B's bullet 2 says "no other field is ever cut". Change 1 also says "A's advocate moved on the claim", but A's Round 1 already offered the claim cut with a falsifier and kept it. Fix: write "no field other than the three location fields is cut by default (claim: unresolved C-001/C-009, see Change 7)". Say B moved on the location fields, not A on the claim.

2. **Change 7 decides C-009 for B.** "Both agree on K2: a claim cut is allowed only if..." and "if K2 is not run, claims stay uncut" are B's reading (bullet 10). A's K2 (bullet 11) is a kill line: the cut stands unless more than 20% fail. The plan also omits A's side of the evidence: anchors-only leaves 2 merges below the floor and 15 merges with a bad block against 4 (B Round 2 E3/E4), and 12 claim-dependent lines (8 blocking). Fix: state both K2 forms and the evidence from both sides, and leave the default to the owner.

3. **Change 14 inverts a figure.** "`refs_norm` unchanged on 0 of 125" should read "changed on 0 of 125" (B Round 2). The cited sources "W1 (B) and W3 (A)" are about stall exposure and `block_ok`, not provenance. The debate did not conclude that the provenance principle is the strongest objection after the merge. B moved C-012 to Variant 1 and kept the byte-copy objection only for the claim cut. Fix the figure, cite the real sources, and present provenance and the eligibility cost (C-002) as the two open objections.

## MEDIUM

4. **Change 6 says "Keep the base's text", but the base says the opposite.** Base 3.3 bullet 2 and the section 2 C-02 row say "because its `block_ok` is False". The rule quoted in Change 6 is B's Round 2 bullet 5. It also states "no `repaired == 0` knob" as fact, but that knob is part of A's bullet 6 and belongs to unresolved C-002. Fix: say "replace" and move the knob into the alternative.

5. **Change 11 INV-I contradicts Change 6.** It calls `block_ok` True "the C-02/C-03 policy of Change 6". Change 6 is the derived eligibility; the bare verdict is A's alternative. Fix: "eligibility per Change 6 (C-002 unresolved)".

6. **Change 10 says "keep the base's table", which retains rows the plan contradicts.**
   - M1 says the refusal fires on exactly 3 merges; Change 5 and K5 say 0 after the cut.
   - M2 re-asks 44 runs; Change 4 re-asks only the residual.
   - M3 raises anchors to 300; Change 8 says anchors are never raised.
   - T-B4 requires byte-equal cluster output; Change 3 adds keys to that output.
   - The v2 loss-unit test must name an over-limit location field, because a claim fault stays invalid under Change 7 (C-003 final).
   Fix: name each base row replaced.

7. **Convergent conclusions are omitted.**
   - C-003 (both Variant 1, 74%): the cut removes the v2 loss unit only for the length share. No change carries it.
   - C-014 (both Hybrid, 63%): the quote prefix passes the `verify_cmd.py:68-72` substring test, the quote limit is a per-profile parameter, and the re-ask is stateless in-session. Base 3.4 (PR row) and section 7 say "not a cut quote", which contradicts Change 1. Neither is targeted.
   - X-003: the reflect residual is non-length.
   - Base section 2 rows are now false and untargeted: C-01 INV-003 "does not arise", INV-004 "not a repair", the "itemise branch" intro, and INV-022.

8. **Change 4 contradicts itself in reflect.** E1 rule "an invalid block gets one re-ask" against "`blocking: false` drops are never re-asked". Scope the second clause to v1. The target "section 3.3 first bullets" is wrong; the trigger is base 3.2 bullet 2 and 3.3 bullets 2-3.

9. **Change 1 sets `repair=True` at the v2 sites unconditionally.** Change 12 makes those sites depend on the owner's reading. Add the condition.

10. **Change 1 over-states the evidence.** 70/70 and 89/89 cover anchor and anchor2 only. The quote cut has no location measurement (C-014 is 63%, no PR-code corpus).

## LOW

11. The Overview names Changes 1, 4 and 6 as High, but Change 4 is Medium in the body and the Risk Summary.

12. Change 9, three wording fixes.
    - The A-001 sentence is garbled. The debate says the populations order the policies but cannot give a recovery percentage.
    - "15-merge difference" does not match 273 - 264 = 9. Say net 9 (B reports 15).
    - "0 of 264" is derived from `flags.tsv` wording, not executed (A N2). Label it.

13. Change 11 INV-G adds "under the reviewer's own tool allowlist". The debate says "no new tool grant".

14. Change 5 never states the firing condition: derived verdict PASS plus an unacknowledged dropped `true` or `unknown` line. It also omits B's recorded price: v1 never recovers a lost blocking line when another blocking row survives (36 of 39 on P273).

15. Template: "modify" is not a template verb (replace, append, insert, restructure).

## Checks

- **Check 1, fidelity:** defects 1, 2, 3, 10, 12, 13.
- **Check 2, completeness:** C-001, C-002, C-009 and C-012 are listed as unresolved, but the policy text decides the first three in B's direction (defects 1, 2, 4). All 4 HIGH and 12 MEDIUM invariants are carried by ID in Change 15 and none is silently resolved. INV-010, INV-016, INV-023, INV-024 and INV-025 appear only in Change 15, which is acceptable. Omitted conclusions: defect 7.
- **Check 3, consistency:** defects 1, 2, 4, 5, 6, 8, 9.
- **Check 4, integration feasibility:** base section 6, section 3.4 and section 7, and the section 2 rows are not feasible as written (defects 6, 7, 8).
- **Check 5, template:** no nonconformity beyond defect 15.

Recommended action: apply fixes 1 to 3 first, then 4 to 8. They stop the merged output from stating an unresolved conflict as settled and from contradicting itself.

END-OF-REVIEW-FILE
