# Common advocate brief (Round 1 and Round 2), written by the orchestrator

Repo root (run everything from here): /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
Output folder: .dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/adversarial/adversarial/   (call it ADV)

Two reviewers each wrote a pre-execution review card against a 39-task implementation plan:
- Variant 1 = ADV/variant-1-original.md  (haiku-class reviewer, 6 findings F1-F6)
- Variant 2 = ADV/variant-2-original.md  (opus-class reviewer, 9 findings F1-F9)
- Diff analysis = ADV/diff-analysis.md  (diff points S-001..S-005, C-001..C-013, X-001, X-002, shared assumptions A-001..A-004)
- Plan under review: .dev/tasks/to-do/TASK-WF-loosenBlockerCla-20261115-133045/TASK-WF-loosenBlockerCla-20261115-133045.md ("plan:NNN" = line number in it)
- Spec: .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md ("spec:NNN"); section 12 (rollout table) is at about line 936; other program files sit in .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/ (09-plan-input.md, 08-test/results.md, 06-blocker-characteristics.md)

You are an ADVOCATE in a structured adversarial debate about which findings in the two cards are correct, verified, and blocking. You MAY Read the plan, the spec and any repo file a finding cites (Read/Grep/Glob only; do not edit any file except your own output file). A claim you cannot verify against a file line MUST be marked [UNVERIFIED].

Blocking rule used for this run (from the requester): a finding blocks when following the plan as written makes an executor reach a wrong or impossible result that no later step in the plan would catch, and it is not wording.

RULES
1. Argue for your variant's strengths with evidence (file:line and a short quote).
2. STEELMAN the other variant before critiquing it: state the strongest version of its argument first.
3. Cite specific lines for every claim; admit genuine weaknesses of your own variant (concessions).
4. For each [SHARED-ASSUMPTION] A-001, A-002, A-003 respond ACCEPT, REJECT or QUALIFY (A-004 is STATED; no response needed). Omitting one is flagged as an omission.
5. For each diff point listed in the TASKS section, state which variant is right, your confidence in percent, and one or two sentences of evidence.
