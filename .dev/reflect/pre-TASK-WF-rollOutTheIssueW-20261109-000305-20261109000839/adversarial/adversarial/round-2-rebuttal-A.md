### Variant A Rebuttal

#### Responses to criticisms

I tested my own Round 1 claims first. I retract the source-contradiction argument and the claim of uniquely deterministic evidence; B is stronger overall on consequential coverage.

1. F1 is small to fix, not small in effect: plan:65 demands zero misses, but docs/designs/issue-watcher.md:163 backticks three states absent from src/superclaude/cli/issue_watch/audit.py:26-102; plan:59 adds `once`. This blocks literal Task 2 acceptance before dependent tasks. I concede B's fixture findings have greater runtime impact, not that repair size discounts F1.
2. I concede F3 should not survive as a defect: plan:96 already specifies one occurrence in 8.7 plus the unchanged FU-2 row, which means two. Writing the numeral is optional clarification.
3. I concede F5 is navigation advice, not a gap: docs/designs/issue-watcher-setup.md:202 is outside Task 4's edits. F4 remains a genuine low-severity omission: setup.md:5 maps only sections 8 to 15, while plan:93 adds section 16 without updating that map. Neither blocks Task 4 acceptance. The "Before cron" title at setup.md:224 can reasonably include the transition to installation.
4. I concede A lacks Task 5 findings and B wins risk coverage. B's claim that A never touches Task 1 is false: variant-1-original.md:41 checks its status-line uniqueness. Conversely B's F2 concerns capture packaging and the Task 5 check, not Task 1's status edit. I accept that Task 5 alone has an explicit fail-and-stop instruction; Task 2 still cannot pass literally.
5. I concede A's self-audit cannot certify Task 5. It remains useful checked-negative evidence, not a completeness guarantee. This supports A on S-001, not a general victory on evidence or coverage.

#### Corrections to own Round 1

- I retract the supposed source contradiction: source.md:22 says "every" and :24 says "about 12+", an effort estimate, not permission to leave fixtures guessed. B also conceded too much here. QA-02 remains a plan inconsistency, not a demonstrated source defect.
- I retract "B has no finding that fails this deterministically". tests/issue_watch/test_github.py:563-568 consumes `raw` and asserts a fixed Date; a capture with a different Date deterministically fails that assertion. A's F1 is simpler to reproduce, not uniquely deterministic.
- QA-04 is an incomplete instruction, not a forbidden-file problem: plan:112 specifies the metadata test, but :120 already allows the whole test_github.py file. B's "no sanctioned way" is too strong. Expected-value updates still need explicit scope.
- I withdraw the implication that F2 is merely optional hardening. Required redaction and verified redaction are different; plan:118 checks only fixtures, leaving retained captures unchecked. No actual leak is established.
- I retain the narrowed QA-03 reading: plan:110 already mentions stderr layout, so counting every non-payload fixture as uncovered overstates it. The `raw` path is enough to sustain B's finding.

#### Final per-point positions

| Diff Point | Superior | Moved? | Reason |
|---|---|---|---|
| S-001 | A | No | Agree with B: checked-negative evidence is useful, but certifies neither completeness nor Task 5. |
| S-002 | A | Yes, from TIE | Agree with B: consistent IDs make merging marginally easier. This is a small presentation advantage only. |
| S-003 | B | No | Agree on consequential findings, not the original high grade for QA-02. A's low grades do not rescue F3 or F5 as defects. |
| C-001 | B | Yes, from TIE | Task 5 coverage addresses tested capture data and expected values; A's Task 2 blocker does not offset that breadth. B's claimed Task 1 coverage is overstated. |
| C-002 | A | No | Disagree with B's TIE: discard F3, but F1 directly makes acceptance impossible; F2 is a missing verification gate, not an established leak. Count alone gives A no advantage. |
| C-003 | B | Yes, from TIE | Both have accurate anchors. B additionally follows the fixture into its consumer and assertion, giving better evidence of implementation consequences. |
| C-004 | A | No | Agree: the cards report gaps of 0.14 versus 0.23 (variant-1-original.md:42-43; variant-2-original.md:44-45). This is relative calibration, not proof A is complete. |
| A-001 | TIE | No, rationale changed | Both use plan-gap appropriately for the verified defects. Retract our shared source-ambiguity argument: an approximate lower-bound effort estimate does not override "every". |
| A-002 | TIE | No | Agree on snapshot-only citations. Plan:23 explicitly anticipates shifted fixture anchors and requires new text to use section and row names. Neither card earns an advantage. |
| A-003 | TIE | No | Agree: plan:20-22 preserves false and reserves live actions and the record to the owner. Neither card changes that boundary. |
| A-004 | TIE | No | Agree only on the common blind spot, not presumed soundness. Task 3's builder and preservation checks deserve separate validation; neither card supplies it. |

Overall: retain A's F1 and low-severity F4, retire F3 and F5 as required fixes, and retain B's verified Task 5 findings with the qualifications above. B is the stronger standalone review; a merge needs both.
