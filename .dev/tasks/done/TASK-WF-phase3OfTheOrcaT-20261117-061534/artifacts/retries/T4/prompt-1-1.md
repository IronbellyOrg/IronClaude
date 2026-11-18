93f19e01af90faa5fe70a43445d5e7faf7b7834a
Review one task for spec compliance.

Task brief: Task 4 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md ("## Task 4: Build the question lines, the selection and the Decision Desk model in the view", read that section, including the per-focus key table). Acceptance criteria, ids T4.AC1 to T4.AC4 in source order, are the four "Acceptance criteria:" bullets of Task 4 in that order (read them there).
Global constraints: the plan's "## Constraints" and "## Out of scope" content in the plan file above (read that section).
Start sha: 93f19e01af90faa5fe70a43445d5e7faf7b7834a
Diff against the start snapshot: the full diff is in the file /tmp/impl-T4-diff.patch (read it; it covers src/superclaude/cli/observe/view.py, tests/observe/test_view.py, tests/observe/test_session.py, and the new tests/observe/test_linkoff_screen_reference.py with tests/observe/golden_questions_linkoff.json). Nothing is committed in this checkout, so the criterion "which git log shows was added before the first view.py change" cannot be read from git log; check file modification times (`ls -l --time-style=full-iso`) of tests/observe/golden_questions_linkoff.json, tests/observe/test_linkoff_screen_reference.py and src/superclaude/cli/observe/view.py instead, and judge whether the reference was generated from unmodified code by whether the golden's content equals the current link-off output (the test passes). Codegraph context: index_state: fresh; checked_at: 2026-11-17T07:27:40Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp. Call codegraph only when index_state: fresh, never to widen scope. Dependents of the changed symbols (Q2b, Grep floor): QuestionLine, View, Session and QuestionsPanel gained only defaulted fields; build_view and apply_key keep their signatures (callers in commands.py run_loop and the tests work unchanged); _questions_panel gained a defaulted third argument; render.py, export.py and the snapshot read QuestionLine.text only and are untouched in this task.
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
