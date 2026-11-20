persona: qa
model_class: haiku

# Reviewer 2 card (summary of the agent's return; verdict FAIL, 6 findings, all labelled Blocking by the reviewer)

QA-1 Task 13 / R18 (plan:163-168, source.md:44,62): activation check omits the lock and restart tests and the live-test record. Severity MEDIUM per reviewer.
QA-2 Task 4 / R23 (plan:63-67, source.md:47): Pipeline-to-launch-level mapping and empty-Pipeline default are stated as settled though the source reserves both for owner confirmation. A design note is not that confirmation. Fix: owner-decision gate before Tasks 5-6.
QA-3 Tasks 14-15 / R5 (plan:183-188, source.md:31; cycle.py:1099-1109): stopping only after a `launched:` line does not enforce one launch per sweep when a launch outcome is unknown; launched_issue is set only on confirmed success, so another repo could launch. HIGH. Fix: stop rule for uncertain launch, plus crash and uncertain-launch tests.
QA-4 Task 5 / R23 (plan:72-79; cycle.py:1012-1016, 1053-1058): the prompt carries the Status and Pipeline first examined, with no comparison against the final Project reread; revalidation checks only eligibility, so Research changed to Debug before launch still launches the old command. HIGH. Fix: refresh-or-refuse rule and tests.
QA-5 Tasks 19-20 / R20 (plan:226-237, source.md:48): the verification of existing-remote-branch reuse becomes only an open question. MEDIUM.
QA-6 Task 13 / R18 vs source.md:44,60: automatic activation conflicts with the retained owner-only activation line; the source gives no precedence. The reviewer disputes that R18 simply wins. MEDIUM.

Adherence: 26 spec units audited (R1-R23 plus three manual-gate bullets); 20 adherent, 6 partial or conflicted.
Note: Task 18 dependency gap confirmed but not independently blocking.
Not done by the reviewer: no commands run; snapshot isolation not established.
