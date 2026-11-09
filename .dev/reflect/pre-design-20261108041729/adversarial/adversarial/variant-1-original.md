reviewer: 1
model_class: sonnet
persona: analyzer
self_confidence: 0.86
note: condensed by the orchestrator from the reviewer's returned YAML; claims, severities, evidence and recommendations kept
findings:
  - id: R1-F1
    kind: gap
    severity: blocking
    claim: "The plan never touches tests/skills/test_worker_contract.py, which stores an exact-line classification table of every `gh api` / `gh pr` line in skills, commands and agents. The plan rewrites four such lines and adds new ones, so test_every_write_verb_hit_is_classified and test_classification_table_has_no_stale_entries fail in the whole-suite run; Tasks 7, 8, 12 run only test_issue_protocol.py and hide it."
    evidence: "tests/skills/test_worker_contract.py:1948-1951, :2005-2012, :3006-3013, :3022-3037, :3086-3093, :3133-3138, :3150-3156; SKILL.md:73-74; create.md:9; issue-worker-t3.md:22,27"
    recommendation: "Add a task (or extend Task 7) updating WRITE_VERB_CLASSIFICATION: replace the four changed keys, add keys for each new `gh api` line (GET lookups read-only, POST writes never-worker); add `uv run pytest tests/skills/test_worker_contract.py -k \"write_verb or classif\" -v` to Task 12."
  - id: R1-F2
    kind: gap
    severity: minor
    claim: "Task 6's `-k command` check runs against test_issue_protocol.py, but the real command-file tests are in tests/commands/test_issue_command.py; tests/skills/test_issue_worker_agents.py pins the T3 read-only wording Task 5 edits."
    evidence: "tests/commands/test_issue_command.py:84-101,152-166,188-189; tests/skills/test_issue_worker_agents.py:93-102"
    recommendation: "Add both files to Task 6/Task 12 test runs."
  - id: R1-F3
    kind: gap
    severity: minor
    claim: "No task names the Complexity request-body file `.dev/issues/<N>/complexity-field.json` or updates the rule that every output file starts from a template (SKILL.md:52 exempts only clickup.json) or the Outputs row of commands/issue.md."
    evidence: "source.md:38,80; SKILL.md:52; commands/issue.md:78"
    recommendation: "Name the file in Tasks 1/2, extend SKILL.md:52 in Task 3, add it to the Outputs row in Task 6, assert it in a Task 8 test."
  - id: R1-F4
    kind: risk
    severity: minor
    claim: "Task 8's orgs/ scanner has no stated regex; Task 2 puts a bare `orgs/` token in prose of the scanned files, so a naive pattern flags the docs themselves."
    evidence: "plan Task 2 acceptance bullet 2; plan Task 8 second test"
    recommendation: "Fix the regex (path needs a character after orgs/), and make the self-check test feed one prose sentence that must not be reported."
  - id: R1-F5
    kind: contradiction
    severity: minor
    claim: "Constraint 'writes exactly two things to a created issue' contradicts the plan, which keeps the mode label and the pushback comment."
    evidence: "plan Constraints bullet 5; source.md:34,39"
    recommendation: "Reword to 'the only new writes are the issue type and the Complexity value'."
  - id: R1-F6
    kind: gap
    severity: minor
    claim: "create.md:36 still says 'not silently relabelled' and no task edits it; no new test pins the flags-decision Issue type row or the 'not reclassified' wording, so Task 8's 'revert any one of Tasks 1-5 turns a test red' does not hold for Task 4."
    evidence: "create.md:36; create-review-comment.md:3"
    recommendation: "Add create.md:36 to Task 2 and one Task 8 test for the two template wordings."
  - id: R1-F7
    kind: ok-check
    severity: minor
    claim: "Matrix spot-check: the 3 unmapped rows are covered by Tasks 1-3 and Constraints; INF-007 and INF-040 matched the wrong task by word overlap (real owners Tasks 2/3/5/8 and Task 5), so per-row task ids are not coverage evidence."
    evidence: "coverage-matrix.json INF-007, INF-040, INF-031, INF-032, INF-045"
    recommendation: "No plan change."
checks_done:
  - "Q1-Q9 each land in a task; sections 2.1-2.5 and 3.1 files have owning tasks; dependency order holds with no cycle."
  - "Plan line numbers match the live files (test_st10 :492-520, Will/Will Not :527, five-ref tests, SKILL/create/T3/command/template lines)."
  - "test_st10 extractor works on a third block; gh_lines_missing_repo only matches gh issue/pr/label lines; no new ref or template added so inventory tests hold."
  - "Task 11 conditional CLAUDE.md step is correct."
