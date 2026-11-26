| Status | Result |
|---|---|
| DONE | Debate, scoring, merge and two independent reviews finished. The final review passed. |
| DONE | Both contracts are written (the command's own and the worker's), and both parse as valid YAML. |
| NEXT | Read the merged spec and decide whether to act on the 14 recorded follow-up items. |

**Result:** the merged specification is at `.dev/brainstorms/20261113-223124-panel-process-redesign/nested/adversarial-1/merged-spec.md` (1,248 lines). It keeps the six sections and ends with exactly two redesigns.

- **Redesign 1, Sweep Sheet:** a script extracts at most 12 typed items. Each item goes to 2 of the 3 reviewers, who answer in a written ledger.
- **Redesign 2, Recipe Ledger:** instructions only. Each reviewer runs a few written class recipes and fills the same kind of ledger.

**Debate outcome:**
- The variants agreed on 73% of the 41 diff points after Round 1 and 98% after Round 2 (threshold 75%).
- Variant 2 (analyzer) became the base. Its score trailed Variant 1's by 0.0482, inside the 0.05 tiebreak band, and it won 35 of 41 debated points.
- The fault-finder raised 14 invariant problems, 6 of them HIGH. All 14 are resolved in the merged text.

**Corrections the debate made:**
- **Harness-fix gain:** Variants 1 and 3 guessed +0.2 to +0.9 for the four harness fixes. The first brainstorm's own table gives +0.14 (0.03-0.34), so I used that.
- **Variant 3's time budget:** it mixed two baselines. Recomputed, its verifier design reaches +37.7%, which breaks the 35% limit, so the verifier stays off the critical path.
- **Totals lowered:** the merged totals are lower than any variant claimed. I added a selection factor and a wider displacement range. Found per run out of 14 is now 1.9 / 3.3 / 4.8 for Redesign 1 and 1.6 / 3.0 / 4.5 for Redesign 2 (low / central / high). Both high ends exceed the best run ever recorded (4 of 14), so treat them as optimistic.

**Review:** the first independent review failed with 7 real blocking defects, for example an item-cap mismatch, a wrong token percentage, and a validation gate that could not be evaluated. I fixed all 7 in one cycle, and the second review passed with every number recomputed. It left 3 medium points; the first review's 11 are recorded too. I did not fix any of the 14, per the review rules. Examples: the pass/fail threshold sits above the planned central gain, and the ember re-ask has no working mechanism.

**NOT BUILT:** no model run has tested any probability, time figure or gain here. They are planning values until the validation experiment in section 5 replaces them.

**Recommended action:** read `merged-spec.md` sections 3 and 4, then the follow-up list at the bottom of `adversarial/merge-log.md`. Decide which of the 14 to turn into fixes before you run the validation experiment. Nothing was staged or committed.
