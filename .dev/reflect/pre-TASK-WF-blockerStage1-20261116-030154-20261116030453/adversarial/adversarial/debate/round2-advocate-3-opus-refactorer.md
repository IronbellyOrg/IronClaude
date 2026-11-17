# Round 2: Advocate for Variant 3 (opus class, refactorer)

## Response to criticisms
- **T3, not T4 (conceded).** "the test never reads `~/.claude`" belongs to T3 (PLAN:209). T4 asks only that each scale-map row "names an existing file and a label present in it". So C-002 rests on PLAN:62 ("exists in the repository") together with PLAN:87 (`grep -rn "\.dev/\|artifacts/"` "prints nothing"). That is V1's argument. New support: SPEC:145 itself calls the stoprule rubric "installed only" [V].
- **C-008 (conceded, and my reason was wrong).** I said T2 is "off in this phase". But SPEC:917 says T2 fails on any file that holds a fence opener and "is not a registry row", strict or not. Non-strict mode does not exempt `doctor.py`. The finding still fails because PLAN:197 asks only to "compare the digest versions". It never requires writing the opener as a literal.
- **C-009 (conceded).** PLAN:139 is a one-off `uv run python -c` check. PLAN:159 never imports the sketch.
- **C-006 (conceded).** PLAN:72 asks for "the location rule (REQ-07)", not the `.dev/pr-monitor/` text.

## Updated assessment
**C-004 and X-001.** An executor following the plan runs the reuse audit (PLAN:110) and builds a separate `follow_ups.py`. Nowhere does it record a mapping to `review-ledger/1`.
- **No check fails.** PLAN:113 limits the test to "each T7 failure condition above", and the SPEC:945 exit tests have no mapping condition.
- **Silence matches the decision the spec points to.** SPEC:404 calls version 1 "a separate, human-readable markdown ledger". The decision the spec points to, "no mapping in version 1", gives exactly the same built result as the plan's silence.
- **No wrong output, no data loss.** Nothing in the spec or in the stage 2–4 requests reads a mapping. `grep` over `stage-requests/` finds nothing.

So the gap is real but not blocking. I am changing my Round 1 grade. A one-sentence decision in Task 7 would remove it completely. Under A-003 that cost is not what sets the grade. The deciding fact is that executing the plan gives no wrong or missing result that anything uses.

## New evidence
1. **The gap is inherited, and no later package picks it up.** The base plan `TASK-WF-loosenBlockerRev…md:210` has the same Task 7 text. stage1-request.md:7 tells the plan to reuse it. Neither the 8-finding review of the base plan nor the stage 2–4 requests mention a mapping. If this plan does not decide it, nothing does. That makes it worth a sentence, but it does not make it blocking.
2. **The reuse audit cannot make the decision.** `agents/reuse-auditor.md:3` says "Detection only". PLAN:110 audits code reuse only. It cannot settle the SPEC:404 decision, so V2 is right that this part is unaddressed.
3. **"Adapter" has a fixed meaning in this spec.** SPEC:733 says "Each own-scale change is a separate adapter approval". SPEC:940, one line above the stage table, says own-scale adapters are "not stages". So "ledger adapters" (SPEC:945) most plausibly means turning a family's own labels into ledger outcomes. The plan builds that in Task 3 (scale map), Task 9 (`ReviewerJudge`, "label read through the scale map") and Task 12.
4. **Only the stoprule row fails C-002.** `git grep` finds the old definition sentence in exactly the 11 digest carriers, so T2 passes at stage 1. The other families' defining files exist: `findings.py`, `validate_prompts.py`, `pr_submit/severity_router.py` and `auggie severity-rubric.md`. Of the 12 rows, only the stoprule row fails.

## Final positions
C-001 | winner: variant 3 | verdict: BLOCKING-REAL | changed from round 1: no | PLAN:115 against PLAN:148 and :171; PLAN:24 and source.md:17 require an end point
C-002 | winner: variant 1 | verdict: BLOCKING-REAL | changed from round 1: no (reason now PLAN:62 + :87, not T4) | the rubric exists only under `.dev/experiments`; SPEC:145 says "installed only"
C-003 | winner: variant 3 | verdict: REAL-NOT-BLOCKING | changed from round 1: no | PLAN:65 says "lists", not "only"; T5 is not in SPEC:945
C-004 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | changed from round 1: yes | no check or consumer needs a mapping; silence builds what "none in version 1" builds (SPEC:404)
X-001 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | changed from round 1: yes | "adapter" means a label translation (SPEC:733, :940); Tasks 3, 9 and 12 build it
C-006 | winner: variant 2 | verdict: NOT-A-DEFECT | changed from round 1: yes | PLAN:72 asks for the rule only
C-008 | winner: variant 2 | verdict: NOT-A-DEFECT | changed from round 1: yes | PLAN:197 needs no literal; my non-strict reasoning was wrong (SPEC:917)
C-009 | winner: variant 2 | verdict: NOT-A-DEFECT | changed from round 1: yes | PLAN:139 is one-off; PLAN:159 has no sketch import
A-003 | winner: tie | verdict: N/A | changed from round 1: no | ACCEPT: once a failure is shown, fix cost does not lower the grade (C-001 shows one; C-004 does not)

Read-only. I ran no tests and changed no files. I did not check whether Tasks 12 and 13 import the Task 7 reader beyond what the plan's text says.
