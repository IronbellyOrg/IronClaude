4d868f8ad2058aff1ca8574217dff6a87b96467e
Review one task for spec compliance.

Task brief: Task 1 of the plan /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/TASK-WF-spec-20261108-181543.md, lines 41-58 (read them verbatim; the parent spec is source.md in the same folder, sections 2.1 steps 0-2, 2.3 exit codes, 3.3). AC ids, in order of the "Acceptance criteria:" bullets at lines 55-58: T1.AC1 = line 55 (hash digest test, importlib load, isolated uv subprocess); T1.AC2 = line 56 (listed input-error, GRADE-CONFLICT, lookup and snapshot tests); T1.AC3 = line 57 (imports are standard library only); T1.AC4 = line 58 (`uv run pytest tests/skills/test_sc_fixcheck.py -v` passes). The task body bullets at lines 43-52 are part of the brief.
Global constraints: the "## Constraints" section of the same plan file, lines 17-37 (read them verbatim).
Start sha: 4d868f8ad2058aff1ca8574217dff6a87b96467e
Diff against the start snapshot: `git diff 4d868f8ad2058aff1ca8574217dff6a87b96467e` over tracked files is empty. The task's touched set is two new untracked files; each whole file is its diff (read the current contents): /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py and /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/tests/skills/test_sc_fixcheck.py. You may run `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_sc_fixcheck.py -v -p no:cacheprovider` from /home/coder/workspaces/worktrees/IronClaude/bs346-minfix to reproduce; do not edit any file.
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
