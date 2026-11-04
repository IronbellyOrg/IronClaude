4749791d049cf2cbaa6b3ca9c2168eb4f7cdd096
Review one task for spec compliance.

Task brief: Task 2 (ids T2.AC1, T2.AC2) of /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md, the section "## Task 2: Add the early section and the Rules bullet to the three issue-worker agent files" through its "Acceptance criteria:" bullets (read it verbatim from that file). T2.AC1 = the first acceptance bullet (each agent file carries the early section and the Rules bullet exactly once, byte-identical across the three files; the diff of each file shows only those additions). T2.AC2 = the second acceptance bullet (the Task 1 agent tests, positive and negative, and every pre-existing test in tests/skills/test_issue_worker_agents.py pass). "./artifacts/" means /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/artifacts/.
Global constraints: the "## Constraints" section of the same plan file (read it verbatim).
Start sha: 4749791d049cf2cbaa6b3ca9c2168eb4f7cdd096
Diff against the start snapshot: the three agent files are untracked, so `git diff` against the start tree cannot show them. Their start-tree copies are saved byte-identical at ./artifacts/pre/issue-worker-t1.md, issue-worker-t2.md and issue-worker-t3.md (they are also readable with `git show 4749791d:src/superclaude/agents/issue-worker-t<N>.md`), and the unified diffs against the current files are ./artifacts/t2-diff-t1.patch, ./artifacts/t2-diff-t2.patch and ./artifacts/t2-diff-t3.patch. Current files: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md. Test log: ./artifacts/t2-green.log (the two SKILL.md spawn-rule tests are Task 3's and are expected to fail until Task 3 runs). Extra check log: ./artifacts/t2-removal-equals-pre.log.
Delta diff from the previous reviewed tree (empty on the first review):
Earlier blocking findings of this start (empty on the first review):
Saved-probe re-check hit locations (may be empty):

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
