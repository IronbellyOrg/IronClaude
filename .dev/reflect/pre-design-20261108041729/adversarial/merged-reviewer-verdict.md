<!-- provenance: merged review card; base = variant 3 (variant-3-original.md, reviewer 3, opus); merged from variant 1 (sonnet) and variant 2 (haiku) per refactor-plan.md changes 1-8; merge date 2026-11-08 -->
reviewer: merged
model_class: "opus (base) + sonnet + haiku"
persona: "refactorer (base) + analyzer + qa"
self_confidence: null
note: "Merged by merge-executor from the three condensed reviewer cards. Not re-scored: reviewers reported 0.86 (R3), 0.86 (R1), 0.95 (R2). Every file:line citation comes from the three variant files."
notes:
  source: "plan change 8 (debate; V2 advocate concession)"
  severity_policy: "Exactly one blocking finding (M-F1, debate C-001). Every other finding is minor."
  severity_disagreement:
    - "R2-F1 and R2-F2 were filed as blocking by reviewer 2; the debate (C-002 75%) settled them as minor-to-medium because Task 8 copies design tests 4 and 6 (source.md:114, :116), so the gap is inherited from the design. Merged as M-F3, minor."
    - "R3-F7 was argued down to Low because the ambiguity at SKILL.md:107 vs the later lines pre-dates the plan. Kept as minor (M-F8)."
findings:
  - id: M-F1
    provenance: "R3-F1 + R1-F1"
    source: "plan change 1 (C-001 95%; A-002 QUALIFY)"
    kind: gap
    severity: blocking
    claim: "tests/skills/test_worker_contract.py stores the exact text of every `gh api`/`gh pr` line in skills, commands and agents (WRITE_VERB_CLASSIFICATION). Tasks 2, 3, 5 rewrite four of those lines and add new ones, so test_every_write_verb_hit_is_classified and test_classification_table_has_no_stale_entries fail in the whole-suite run; Tasks 7, 8 and 12 run only test_issue_protocol.py, so the plan's own checks never catch it."
    evidence: "tests/skills/test_worker_contract.py:1940-1951, :2005-2012, :3006-3013, :3022-3037, :3086-3093, :3129-3138, :3150-3156; SKILL.md:73-74; create.md:9; issue-worker-t3.md:22,27"
    recommendation: "Add a task (or extend Task 7) editing test_worker_contract.py: rebuild the 4 changed keys and every new key from the post-edit verbatim line text, not from the current lines; add an entry per new `gh api` line (POST/read-back lines never-worker per the table rules, T3 GET lookups read-only); no `gh api -X POST` line may be classified read-only (rule at :3150-3156); the checker at :2005-2012 must stay green. Verify with `uv run pytest tests/skills/test_worker_contract.py -k \"classified or stale or read_only\" -v`."
  - id: M-F2
    provenance: "R3-F2 + R1-F2 (duplicate, folded in; V3 version kept as more concrete)"
    kind: gap
    severity: minor
    claim: "Plan checks run only test_issue_protocol.py; tests/commands/test_issue_command.py, tests/skills/test_issue_worker_agents.py and test_worker_contract.py also read the edited files."
    evidence: "tests/commands/test_issue_command.py:104-107,119-123; tests/skills/test_issue_worker_agents.py:93-105; plan Task 12"
    recommendation: "Task 12 runs `uv run pytest tests/skills/ tests/commands/test_issue_command.py -v` (or make test); Task 6 states only the Meaning column changes and no --repo text is added."
  - id: M-F3
    provenance: "R2-F1 + R2-F2"
    source: "plan change 2 (C-002 75%; V2 advocate conceded blocking was too strong)"
    kind: false-coverage
    severity: minor
    claim: "Task 8's new tests use prefix checks and check that classification names appear, instead of asserting the exact output formats of specification 2.4 and the Q7 type rules and Q8 depth-to-Complexity pairs. Broken placeholders, separators or failure reasons, reversed type rules or swapped depth mappings can pass. Not blocking: Task 8 copies design tests 4 and 6, so the weakness is inherited from the design."
    evidence: "TASK-WF-design-20261108-041415.md:34,122; source.md:114,116"
    recommendation: "Require complete format assertions in create.md and labels.md including the placeholders and allowed reasons of specification 2.4, and assert the actual mode/area-to-type rules and all three depth-to-Complexity pairs. Verify that changing a separator, removing a reason, swapping Simple and Complex, or making a bug in tests select Test fails a test."
  - id: M-F4
    provenance: "R3-F3 + R1-F3"
    source: "plan change 4 (C-004 85%)"
    kind: contradiction
    severity: minor
    claim: "complexity-field.json has no template, but SKILL.md:52 and create.md:7 say every output file starts from a template (only clickup.json exempt) and commands/issue.md:78 does not list it; no task covers these. The plan also never names the file `.dev/issues/<N>/complexity-field.json` in Tasks 1 and 2."
    evidence: "SKILL.md:52; refs/create.md:7; commands/issue.md:78; source.md:38,80"
    recommendation: "Name the file in Tasks 1 and 2; extend the exception in Tasks 2/3 and the Outputs row in Task 6."
  - id: M-F5
    provenance: "R3-F4 (narrowed: create.md:34 half dropped per plan)"
    kind: contradiction
    severity: minor
    claim: "T1/T2 workers write flags.md from flags-decision.md; nothing tells them to read labels.md for the new Issue type row."
    evidence: "agents/issue-worker-t2.md:22; agents/issue-worker-t1.md:22; templates/flags-decision.md:8-10; refs/create.md:36"
    recommendation: "In Task 2 state the orchestrator fills the Issue type row by rule Q7."
  - id: M-F6
    provenance: "R3-F5 (narrowed: line 330 dropped per plan)"
    kind: gap
    severity: minor
    claim: "Task 10's line list omits docs/designs/sc-issue-command.md lines 34 and 331 (B7 'fixed set' row, orchestrator write list)."
    evidence: "docs/designs/sc-issue-command.md:34,331"
    recommendation: "Add them to Task 10; verify grep 'fixed set' returns nothing there."
  - id: M-F7
    provenance: "R3-F6 + R1-F4"
    source: "plan change 6 (C-002)"
    kind: risk
    severity: minor
    claim: "Task 8's orgs/ scanner has no regex; the spelling with spaces breaks `orgs/\\S+`, and Task 2 puts a bare `orgs/` token in prose of the scanned files, so a naive pattern flags the docs themselves. Task 4 does not forbid naming the orgs path in the scout template, which Task 8 would reject."
    evidence: "plan Task 8 (line 122), plan Task 8 second test, Task 4 (line 74), plan Task 2 acceptance bullet 2, Tasks 2/5"
    recommendation: "Specify the regex and one spelling: it must handle the spaced spelling and require a path character after orgs/. Keep the orgs/other/issue-fields self-check and make the self-check test also feed one prose sentence that must not be reported. State the scout template does not name the API path."
  - id: M-F8
    provenance: "R3-F7"
    kind: risk
    severity: minor
    claim: "SKILL.md:107 says 'Print this block last' for the first return-contract block; a third block makes that wrong, and labels_* narrowing to the mode label is not stated. The ambiguity pre-dates the plan."
    evidence: "SKILL.md:107,116-117; source.md:53"
    recommendation: "Reword in Task 3."
  - id: M-F9
    provenance: "R2-F3"
    source: "plan change 3 (C-009 90%)"
    kind: false-coverage
    severity: minor
    claim: "Task 7 keeps the Will / Will Not agreement test unchanged, but that test reads only SKILL.md and never the command file, so keeping it unchanged proves no agreement between the two."
    evidence: "tests/skills/test_issue_protocol.py:527-541; plan lines 103,111"
    recommendation: "Add assertions that read both files and check shared create guarantees."
  - id: M-F10
    provenance: "R1-F5 + R2-F4"
    source: "plan change 5 (C-005 85%)"
    kind: contradiction
    severity: minor
    claim: "Constraint 5 ('writes exactly two things to a created issue') contradicts the plan, which keeps both the mode label and the conditional pushback comment (Task 2)."
    evidence: "plan Constraints bullet 5; plan lines 23,47; source.md:34,39"
    recommendation: "Scope the restriction to classification writes: 'the only new writes are the issue type and the Complexity value'."
  - id: M-F11
    provenance: "R1-F6 (narrowed to Task 3)"
    source: "plan change 7 (X-001 65%)"
    kind: gap
    severity: minor
    claim: "No new Task 8 test pins what Task 3 adds to SKILL.md, so reverting Task 3 turns only the Task 7 test red; Task 8's claim that reverting any one of Tasks 1-5 turns a new test red does not hold for Task 3."
    evidence: "TASK-WF-design-20261108-041415.md:122; plan Task 3; plan Task 7"
    recommendation: "Add one Task 8 test that asserts the Task 3 SKILL.md wording."
checks_done:
  - "Plan line numbers match the live files; repo-wide grep shows every sc-issue hit assigned to Tasks 1-11 except docs lines in M-F6."
  - "refs/claim.md, tiers.md and chains.md correctly unchanged; no orgs/, -X PUT, issue-fields or issue-types text exists in src/superclaude today."
  - "test_no_brace_placeholder and gh_lines_missing_repo are not tripped by the planned lines; Task 11 conditional is correct."
