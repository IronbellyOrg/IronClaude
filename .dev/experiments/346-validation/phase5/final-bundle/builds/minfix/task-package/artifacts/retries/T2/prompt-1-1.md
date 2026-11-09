0ca44cafe2eeaebbeeff497a38edb74a24688843
Review one task for spec compliance.

Task brief: Task 2 of the plan /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/TASK-WF-spec-20261108-181543.md, lines 60-82 (read them verbatim; the parent spec is source.md in the same folder, sections 2.1 step 2 item 5 and step 3, 2.2, 2.3, 3.3). AC ids, in order of the "Acceptance criteria:" bullets at lines 78-82: T2.AC1 = line 78 (the listed one-test-each behaviours); T2.AC2 = line 79 (carried-open test); T2.AC3 = line 80 (plain check writes nothing); T2.AC4 = line 81 (hash mismatch exit 4, delete over 80 words, short partial quote); T2.AC5 = line 82 (pytest passes). The task body bullets at lines 62-75 are part of the brief.
Global constraints: the "## Constraints" section of the same plan file, lines 17-37 (read them verbatim).
Start sha: 0ca44cafe2eeaebbeeff497a38edb74a24688843
Diff against the start snapshot: the start snapshot is a git tree that already holds the Task 1 versions of the two touched files (both untracked). The diff of the two touched files from that tree to the reviewed tree 211349e5f797278b0e5386e8e6d9f4cd99bb7b77 is saved at /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/t2-review-diff.patch (reproduce with `git diff 0ca44cafe2eeaebbeeff497a38edb74a24688843 211349e5f797278b0e5386e8e6d9f4cd99bb7b77 -- src/superclaude/skills/sc-fixcheck tests/skills/test_sc_fixcheck.py`). Current files: /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py and /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/tests/skills/test_sc_fixcheck.py. You may run `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_sc_fixcheck.py -v -p no:cacheprovider` and ad-hoc `uv run --no-project python` probes of the script on temporary files from /home/coder/workspaces/worktrees/IronClaude/bs346-minfix; do not edit any repository file.
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
