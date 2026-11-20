persona: qa
model_class: haiku (requested; runtime class not verified)

(Persisted by the orchestrator from the reviewer's returned text, condensed; the reviewer agent has no Write tool. Plan = `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md`, source = `source.md` in the same folder. Line numbers are as the reviewer cited them.)

Verdict by the reviewer: FAIL. It labelled QA-1 to QA-3 Blocking and QA-4 Medium, but its own severity column says MEDIUM for QA-1 to QA-3; the grade is decided in the merge.

## Findings

QA-1 (labelled Blocking, Missing), Task 27 (plan:356-363). The Coder handoff lists names, paths and the cron entry but omits the lifecycle instructions of R6 and R9: install cron, start its daemon, restore exactly one entry on every boot; check the coordinator at boot and on every watcher run, create missing parts and restart a stopped session (source.md:36 and :40). It is the only handoff for R6 and R9. Fix: add those instructions and content checks to Task 27's acceptance.

QA-2 (labelled Blocking, Decision), Task 11 (plan:173-176). The acceptance requires a claim-time event to be refused as plan approval, but no implementation or provenance input distinguishes that event. The existing helper accepts a valid hash and syntactically valid label evidence once an adoption row exists (`src/superclaude/cli/issue_pipeline/approval_record.py:313-359`). A missing-hash test would pass without proving the claim-event refusal (R29, source.md:55). Fix: name the enforcement point and its work, and test claim evidence versus genuine plan approval under otherwise valid conditions.

QA-3 (labelled Blocking, Decision), Task 13 (plan:202-207). Every new guard alternative requires `issue-pipeline` or `issue_pipeline`, so none matches the required refusal case `p.complete.run()` when that text stands alone. The coordinator-only matcher is at guard line 444 and the tamper refusal at 763-802. Fix: align the matcher with the literal case while keeping the test-command allowances, or drop that case from the acceptance and state it is best effort.

QA-4 (Medium), Task 24 (plan:323-328). R14's pre-child Project checks are in the instructions but not in the acceptance cases (source.md:34). Task 19 lets a configured Project mapping allow several Projects, while Task 24 says exactly one. Fix: add existing-config cases for zero and several Projects (reported refusal, no child launch) and settle the mapping rule.

## Remediation recheck (reviewer's result)
Q-1 PARTIAL (QA-3 remains). Q-2 to Q-10 FIXED (plan lines 137-143, 61-89, 123-129, 188-192, 125-130, 227-231, 25 and 206, 30 and 82 and 270). All six owner decisions are represented; the matcher gap in QA-3 keeps the last decision's acceptance from being fully resolved.

## Coverage
33 of 33 requirements map to a task. Reviewer marks R6, R9, R14, R29 and R33 as partial (R33 partial through the items above). No orphan tasks. Every explicit dependency names an earlier task; no cycle.

Checked: all 33 requirements, 28 task bodies and acceptance sections, Q-1 to Q-10, six owner decisions, dependency order, and the relevant guard, watcher, approval, worker-contract and test sources.
Not checked: live GitHub timestamp behaviour, cron authentication, Orca runtime behaviour, executed tests. No commands run.
