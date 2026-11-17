# Round 2: Variant 2 advocate rebuttal (opus:qa; agent id adacfb32b110f8b15)

Persisted by the orchestrator from the hand-back.

## Criticisms of Variant 2
- C-001, rf-qa.md:548 "When in doubt, fail it": held. SPEC:201 and :211 only keep the reviewer's label on a `consumer-unknown` row; line 548 fails the whole review on any doubt, even about a Note. SPEC:853 assigns 548 to stage 3 and PLAN:140 leaves it out. Concede qualitative:810 is weak (:805 limits FAIL to an open blocking finding). :796 is real but minor (picks re-verify items by label).
- U-006 (quota sentence): partly conceded. PLAN:192 catches a dropped sentence at Task 10, so the result is a late failure; PLAN:134 does not run test_review_prompt_overrides.py:244. Minor.
- U-011: conceded. PLAN:28 needs an end point only for an acceptance line a later task makes false; PLAN:143-148 stay true. The X-002 hash-description error stands (`## Critical Rules` starts at qualitative:983, after the verdict pairs).
- S-001 and first-review F3 "fixed": conceded (see X-001).

## Testing Variant 1's retreats
X-001: retreat rejected. Task 5 changes pragmatic.md and the registry row to v2 at Q1 (PLAN:125); the gate is reviewed at Q3 (SKILL.md:131, :140). SKILL.md:129 loads PLAN:20, which only says no later task starts. When PLAN:128 fails, the one fix pass (SKILL.md:145) has no legal fix (PLAN:21 forbids editing the result file or ledger); the Repair round reverts nothing (retry.md:135). Every exit leaves the edit in place: a halt after the second attempt with no revert (retry.md:44); an adviser dispute where "nothing has been reverted" (retry.md:107-109); or attempts 3 to 5 which revert and re-apply the same edit (retry.md:11-13) until "the A5 tree stays" (retry.md:158). Repository state: pragmatic.md holds digest v2 and the registry row reads v2, uncommitted; Tasks 6 to 13 not started; installed style unchanged (hook reads ~/.claude copy, pragmatic-subagent.js:7; sync-dev does not copy output styles), so nothing ships. The halt can still spend up to three adviser rounds on a gate no edit can fix, and its `ruling` option (qa.md:247-248) can complete Task 5 with the edit kept on a ruling that need not meet PLAN:94's hash rule. Blocking.

U-004: downgrade accepted. The hook injects the whole installed old file, so reviewers in the new arm hold lines 221 to 231 anyway. What remains: neither arm contains the REQ-04 brief (SPEC:214) or the once-per-run wording that Task 5 ships; the test does not test the text that ships. Minor.

U-008: upgrade to blocking rejected. SPEC:274 adds "does not reopen" and "the only ways a recorded row becomes blocking", which SPEC:203 does not say. But rf-qa.md:393 and qualitative:800 keep "Do not recheck minor findings from the previous report"; Tasks 6 and 7 replace only S1, S2, S5 near line 108. M1 and M12 gates unaffected. Minor; keep the sentence where the spec puts it.

## Final assessment
| Point | Superior | Conf % | Merged grade | Evidence |
|---|---|---:|---|---|
| S-001 | 1 | 70 | minor | Category plus blocking field helps. |
| C-001 | 2 | 85 | blocking | rf-qa.md:100 and :548, SPEC:853; drop :810. |
| C-002 | 2 | 85 | minor | zero-trust :95 and :118-119 still grade by label. |
| C-003 | 2 | 85 | minor | S2:138 produces M6. |
| X-001 | 1 | 75 | blocking | retry.md:109 and :158 leave the edit in the tree. |
| X-002 | 2 | 90 | minor | verdict pairs sit before qualitative:983. |
| A-001 | QUALIFY | 80 | n/a | producers named, not executed (PLAN:41). |
| A-002 | REJECT | 90 | n/a | rf-qa.md:548 outside the S0:34 patterns. |
| A-003 | REJECT | 85 | n/a | a halt leaves the edited source in the tree. |
| U-001 | 1 | 75 | blocking | as X-001. |
| U-002 | 1 | 85 | blocking | PLAN:78 gives two variants, PLAN:82 needs one outcome. |
| U-003 | 1 | 90 | minor | PLAN:214 vs PLAN:25 and revision2-brief:16. |
| U-004 | 2, qualified | 75 | minor | shipped REQ-04 brief in neither arm. |
| U-005 | 2 | 75 | minor | PLAN:144 checks only the frozen inventory. |
| U-006 | 2, qualified | 60 | minor | caught late at PLAN:192. |
| U-007 | 2 | 60 | minor | PLAN:43 does not cover the "> " markers. |
| U-008 | 2 | 70 | minor | rf-qa.md:393 and qualitative:800 keep the rule. |
| U-009 | 2 | 85 | minor | as C-003. |
| U-010 | 2 | 85 | minor | fold into C-002. |
| U-011 | 1 | 85 | drop | keep the X-002 part. |
| U-012 | 2 | 80 | minor | README:11 omits what SRC:41 requires. |

Not checked: whether qa.md's ruling path overrides PLAN:94's hash rule; U-002 scoring past PLAN:78-82.
