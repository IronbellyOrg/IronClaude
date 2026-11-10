reviewer: 3
model_class: opus
persona: refactorer
self_confidence: 0.86
note: condensed by the orchestrator from the reviewer's returned YAML; claims, severities, evidence and recommendations kept
findings:
  - id: R3-F1
    kind: gap
    severity: blocking
    claim: "tests/skills/test_worker_contract.py stores the exact text of every `gh api`/`gh pr` line in skills, commands and agents (WRITE_VERB_CLASSIFICATION). Tasks 2, 3, 5 rewrite four of those lines and add new ones, so test_every_write_verb_hit_is_classified and test_classification_table_has_no_stale_entries fail; Task 12 runs only test_issue_protocol.py so the plan's own checks never catch it."
    evidence: "tests/skills/test_worker_contract.py:1940-1951, :3006-3013, :3022-3037, :3086-3093, :3129-3138, :3150-3156; SKILL.md:73-74; create.md:9; issue-worker-t3.md:22,27"
    recommendation: "Add a task (or extend Task 7) editing test_worker_contract.py: replace the 4 changed keys with the new verbatim lines, add an entry per new `gh api` line (POST/read-back lines never-worker per the table rules, T3 GET lookups read-only); verify with `uv run pytest tests/skills/test_worker_contract.py -k \"classified or stale or read_only\" -v`."
  - id: R3-F2
    kind: gap
    severity: minor
    claim: "Plan checks run only test_issue_protocol.py; tests/commands/test_issue_command.py, tests/skills/test_issue_worker_agents.py and test_worker_contract.py also read the edited files."
    evidence: "tests/commands/test_issue_command.py:104-107,119-123; tests/skills/test_issue_worker_agents.py:93-105; plan Task 12"
    recommendation: "Task 12 runs `uv run pytest tests/skills/ tests/commands/test_issue_command.py -v` (or make test); Task 6 states only the Meaning column changes and no --repo text is added."
  - id: R3-F3
    kind: contradiction
    severity: minor
    claim: "complexity-field.json has no template, but SKILL.md:52 and create.md:7 say every output file starts from a template (only clickup.json exempt) and commands/issue.md:78 does not list it; no task covers these."
    evidence: "SKILL.md:52; refs/create.md:7; commands/issue.md:78; source.md:38"
    recommendation: "Extend the exception in Tasks 2/3 and the Outputs row in Task 6."
  - id: R3-F4
    kind: contradiction
    severity: minor
    claim: "T1/T2 workers write flags.md from flags-decision.md; nothing tells them to read labels.md for the new Issue type row, and create.md:34 still gives lowercase complexity words."
    evidence: "agents/issue-worker-t2.md:22; agents/issue-worker-t1.md:22; templates/flags-decision.md:8-10; refs/create.md:34,36"
    recommendation: "In Task 2 state the orchestrator fills the Issue type row by rule Q7 and change create.md:34 to option names."
  - id: R3-F5
    kind: gap
    severity: minor
    claim: "Task 10's line list omits docs/designs/sc-issue-command.md lines 34, 330, 331 (B7 'fixed set' row, gh api path rule, orchestrator write list)."
    evidence: "docs/designs/sc-issue-command.md:34,330,331"
    recommendation: "Add them to Task 10; verify grep 'fixed set' returns nothing there."
  - id: R3-F6
    kind: risk
    severity: minor
    claim: "Task 8's orgs/ scanner has no regex; the spelling with spaces breaks `orgs/\\S+`; Task 4 does not forbid naming the orgs path in the scout template, which Task 8 would reject."
    evidence: "plan Task 8 (line 122), Task 4 (line 74), Tasks 2/5"
    recommendation: "Specify the regex and one spelling; keep the orgs/other/issue-fields self-check; state the scout template does not name the API path."
  - id: R3-F7
    kind: risk
    severity: minor
    claim: "SKILL.md:107 says 'Print this block last' for the first return-contract block; a third block makes that wrong, and labels_* narrowing to the mode label is not stated."
    evidence: "SKILL.md:107,116-117; source.md:53"
    recommendation: "Reword in Task 3."
checks_done:
  - "Plan line numbers match the live files; repo-wide grep shows every sc-issue hit assigned to Tasks 1-11 except docs lines in R3-F5."
  - "refs/claim.md, tiers.md and chains.md correctly unchanged; no orgs/, -X PUT, issue-fields or issue-types text exists in src/superclaude today."
  - "test_no_brace_placeholder and gh_lines_missing_repo are not tripped by the planned lines; Task 11 conditional is correct."
