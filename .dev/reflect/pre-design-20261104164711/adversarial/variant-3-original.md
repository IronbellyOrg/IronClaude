# Persisted by the orchestrator from the read-only reflect-reviewer return (verbatim content).
reviewer: 3
persona: refactorer
model_class: opus
verdict: ready-with-fixes
self_reported_confidence: 0.82
findings:
  - id: F-1
    severity: medium
    deviation_class: drift
    claim: "Task 4 is too large, and it moves the resume-row tests of test_conflicts_core.py ahead of the run-log fold (Task 7). Spec section 13 puts those tests in step 7, which depends on the fold (step 6); in Task 4 they build `state` dicts by hand that can drift from what rebuild_state actually returns."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:84-100", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1418", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1422", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:594", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:671-678"]
    recommendation: "Split Task 4: 4a = conflict_action, gates, cycle ids, records, message + tests (depends on Task 3); 4b = crash_resume_plan and conflict_resume_plan + Resume tests (depends on 4a and Task 7, between Task 7 and Task 8), state built from RunLog.rebuild_state(). Verify: the 13-step-7 coverage row maps to 4b/Task 8; no Resume test uses a dict literal in place of rebuild_state output."
  - id: F-2
    severity: medium
    deviation_class: drift
    claim: "Task 19 lacks edges: X1 replays steps 3 to 12, and step 11 uses poll-ci-checks.sh --evidence-sha (Task 13) and ci.expect_checks_after_push (Task 6), as written in conflict-mechanical.md (Task 14); spec step 13 depends on all of step 9."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:287-291", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1400", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:303", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1424", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1428"]
    recommendation: "Task 19: 'Depends on: Task 5, Task 6, Task 8, Task 11, Task 12, Task 13, Task 14'. Verify: closure includes Tasks 10-13 and the ref X1 replays."
  - id: F-3
    severity: medium
    deviation_class: drift
    claim: "Task 16 depends only on Task 2, but its ci-poll.md item 4 documents poll-ci-checks.sh --evidence-sha and ci.expect_checks_after_push, created by Tasks 13 and 6 (spec step 10 depends on step 9)."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:248-256", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1063-1080", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1425"]
    recommendation: "Task 16: 'Depends on: Task 2, Task 6, Task 13'. Verify: no ref task runs before the script or function its text names."
  - id: F-4
    severity: medium
    deviation_class: drift
    claim: "tests/pr_submit/test_conflict_scripts.py is created by Task 10 and appended to by Tasks 11, 12, 13; Task 13 has no Depends-on and Tasks 11 and 12 are siblings, so graph-ordered or parallel execution hits a missing file or conflicting appends."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:186", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:196-198", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:207-209", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:215-217", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1424"]
    recommendation: "Chain them: Task 12 'Depends on: Task 11', Task 13 'Depends on: Task 12' (minimum: Task 13 'Depends on: Task 10'). Verify: every task editing test_conflict_scripts.py has a path to every earlier editor."
  - id: F-5
    severity: medium
    deviation_class: drift
    claim: "Task 15's record check calls parse_resolution_record/resolution_record_ok (Task 4) but depends only on Task 12 (chain 12-10-3); Task 20 (spec step 14 depends on all) never reaches Task 6 or Task 9."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:239-245", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:169-171", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:298-300", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1429"]
    recommendation: "Task 15: 'Depends on: Task 4, Task 12'; Task 20: 'Depends on: Task 9, Task 18, Task 19'. Verify: Task 20's closure covers Tasks 1-19."
  - id: F-6
    severity: medium
    deviation_class: authorized
    claim: "Dropping make test is an explicit constraint (TL:28), but the reduced set leaves out src/superclaude/cli/reflect/commands.py:99, which imports superclaude.pr_submit.contract_setup and so runs the package __init__ Task 9 rewrites."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:28", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:173-178", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:306", "src/superclaude/cli/reflect/commands.py:99", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1408"]
    recommendation: "Add tests/cli/reflect/test_contract_status_cli.py to the pytest commands of Task 9 and Task 20. Verify: t9-tests.log and t20-checks.log show it passing."
  - id: F-7
    severity: low
    deviation_class: drift
    claim: "Spec step 9 requires test_skill_forbids_force_push over the new files, but Tasks 11 and 12 run only test_conflict_scripts.py."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:203", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:213", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1424", "tests/pr_submit/test_static_grep.py:773-776"]
    recommendation: "Add tests/pr_submit/test_static_grep.py to Task 11 and Task 12 pytest commands. Verify: logs include test_skill_forbids_force_push."
  - id: F-8
    severity: low
    deviation_class: drift
    claim: "poll-ci-checks.sh:30 exits 2 when --pr is missing; no acceptance criterion runs C1-C4 without --pr, so C4's exit 2 could pass for the wrong reason."
    evidence: ["src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh:30", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:217-220", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1394"]
    recommendation: "Task 13 AC: 'C1-C4 invoke the script with --evidence-sha and --repo only (no --pr); C4 asserts stderr names the invalid SHA'. Verify: C-case argument lists."
  - id: F-9
    severity: low
    deviation_class: necessary
    claim: "E5 and E12 are split between Task 1 and Task 17; after Task 1 the E5 old substring is gone and Task 17 does not name where the operation-check sentence and E12 rows 3-5 go."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:39", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:267", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:901-909", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:961-969"]
    recommendation: "Task 17: E5 sentence goes right after Task 1's text ending 'so report how many commits it is behind instead).'; E12 rows 3-5 after the 'Behind base branch (create path at L1+, or `--pr`)' row; AC: final Wave 0 substring equals the full E5 replacement in source 8.1."
  - id: F-10
    severity: low
    deviation_class: necessary
    claim: "Some edges are stricter than spec section 13 (Task 5 on Task 4, Task 9 on Task 6, Task 8 on Task 4); Task 5's extra edge usefully orders edits to the shared test file."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:106", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:171-173", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1419", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1423"]
    recommendation: "Keep Task 5's edge; optionally drop Task 9's edge on Task 6."
  - id: F-11
    severity: low
    deviation_class: authorized
    claim: "The plan adds light evidence artifacts beyond the spec (Task 15 sample-record check, Task 18 negative check, Task 17 diffstat with 'at most 15 lines')."
    evidence: [".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:31", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:245", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:270", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:285", ".dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:867"]
    recommendation: "No change required; optionally tighten Task 17 to 'net +15' per source 8.1:981."
summary: "Order matches spec section 13; the Depends-on graph misses edges at Tasks 13, 15, 16, 19, 20 and Tasks 11-13 share one test file. Task 4 is oversized and pulls the resume tests ahead of the run-log fold (split 4a/4b). make test drop is authorized but add tests/cli/reflect/test_contract_status_cli.py to Tasks 9 and 20, and the force-push scan to Tasks 11 and 12."
