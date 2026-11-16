e204e8b9b1fec9f76fe5beba9e4d54d64bbcec52
Review one task for spec compliance.

Task brief: T1 = item 1.1 of the source file /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md (lines 211-216). Item text:
- [ ] **1.1 — Set task status to Doing**
  - **Context**: This task file at `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` starts at status "🟡 To Do" (frontmatter `status`). The Frontmatter Update Protocol in `## Execution Context` requires the start checkpoint.
  - **Action**: Edit the frontmatter: `status` to "🟠 Doing", `start_date` and `updated_date` to today's date (YYYY-MM-DD).
  - **Output**: Updated frontmatter of this task file.
  - **Verification**: Verify: Read lines 1-20 of this file; `status` is "🟠 Doing" and `start_date` is not empty. If the edit fails, log the blocker in `### Phase 1 Findings` and stop.
  - **Completion gate**: Frontmatter shows "🟠 Doing" with a start date. Once done, mark this item as complete.
AC ids: T1.AC1 = the item title "Set task status to Doing" (no AC block; the title is the AC). The item's own Verification and Completion gate lines above are context for what "done" means. Ticking the item's checkbox is done by the orchestrator after the verdict and is not part of the diff under review.
Global constraints: the `### Key Constraints` section (lines 157-168) of the source file named above; read it from that file.
Start sha: e204e8b9b1fec9f76fe5beba9e4d54d64bbcec52
Diff against the start snapshot: git diff e204e8b9b1fec9f76fe5beba9e4d54d64bbcec52 -- <source file> (two hunks in the frontmatter):
-status: "🟡 To Do"
+status: "🟠 Doing"
-start_date: ""
+start_date: "2026-11-08"
(`updated_date: "2026-11-08"` was already today's date at the start snapshot, so it needed no change. Run the git diff yourself in /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode to confirm; today's date for this session is 2026-11-08.)
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
