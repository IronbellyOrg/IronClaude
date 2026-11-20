persona: qa
model_class: haiku

# Reviewer 2 card (v3 plan; summary of the agent's return; verdict FAIL, 3 findings labelled Blocking)

QA-1 (Blocking, Safety, HIGH), Tasks 7 and 10, R24 (plan:158): the proposed guard change blocks the completion verb but leaves direct issue comments allowed at Full Submit; the acceptance check tests comment refusal only at Worktree and Full. launch-level-guard.sh:653 classifies issue comments as SUBMIT and :790 permits SUBMIT at Full Submit. So the claimed coordinator-only write boundary is unenforced at Full Submit. Fix: distinguish coordinator-only issue writes from permitted Full Submit PR actions and test Full Submit refusal too.
QA-2 (Blocking, Decision, MEDIUM), Tasks 4 and 6, R31 (plan:65, 71, 102, 108; source.md:57): Task 4 requires `edited_after_approval` when a reread Project item changed after approval; Task 6 requires `revalidation_failed` whenever Status or Pipeline changed; a real between-read change meets both. Fix: specify precedence, keep R31's reason for post-approval changes, test the overlapping case.
QA-3 (Blocking, Missing, HIGH), Tasks 9 and 10, R24 (plan:141, 146, 209): the completion interface supplies the repo and issue but no configured Project identity, and neither the read instructions nor the acceptance require selecting that Project's live item; an issue can belong to several Projects (predicates.py:268 shows existing selection by configured Project id). Fix: a trusted Project id or config lookup, exact-item selection, tests refusing ambiguous or missing targets before a Status mutation.

Earlier findings P-1 to P-11 checked: all fixed except the open parts noted (P-1: Full Submit direct comment path, QA-1; P-4: refusal precedence, QA-2).
Adherence: 32 requirements audited, 30 covered without defects; R24 and R31 affected. Drift 3, Regression 0. New-row ownership checked: R24 Tasks 5/7/9/10; R25 5-8; R26 18/19; R27 6; R28 17; R29 5/8; R30 2/11/15/20/22-24; R31 3/4/6; R32 5/8/9/11/19/21.
Notes: read-only review, no commands run; the `updatedAt` field availability stays unverified until Task 3's schema check.
