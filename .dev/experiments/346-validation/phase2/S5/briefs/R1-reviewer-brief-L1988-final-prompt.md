You are the independent FINAL reviewer for a managed /sc:implement package (archive gate). Do not trust the implementer's report. Start from the position that mistakes exist and look for them.

Package root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902
- Plan (read it all, including `## Constraints`): <package root>/TASK-WF-writeTheP0LivePl-20261103-215902.md
- Ledger (read it all): <package root>/progress.md
- Delivery files (read the ones you need; the full list is the `files` array of the JSON in /tmp/ironclaude-p0live/state1.json, repo-relative to /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs). Every `./artifacts/...` token in the ledger means <package root>/artifacts/....
- The package also holds, under <package root>/artifacts/retries/T<id>/, the notes file (T2/notes.md) and the saved reviewer prompts (prompt-<k>-<j>.md, line 1 is the task's start sha). For this FINAL review you are allowed and expected to read those folders.
- Static report the plan relies on: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md
- The workers' own session files (what Step 5 of each live check was verified on) are under /home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-p0-live-{troubleshoot,workflow,adversarial}/ ; the disposable worktrees were removed by the run, so their contents survive only as the copies and logs in artifacts/.

Task: verify, at the END STATE, that every AC of every task T1 to T5 in the plan is met by the real current files. For each task AC return met or unmet with a `path:line` citation taken from the CURRENT files and logs (not copied from the ledger; a per-task `evidence=` line number is only a pointer and a moved line number alone is not an issue). Also check:
1. every plan `## Constraints` item (read them one by one; quote the text of any item you find violated);
2. a log cited on a task's latest `complete` line shows no failure at its outcome line;
3. the notes entries in artifacts/retries/T2/notes.md: apply the severity test below;
4. each saved prompt artifacts/retries/T<id>/prompt-<k>-<j>.md against the reviewer template in /home/coder/.claude/skills/sc-implement-protocol/refs/qa.md (section "Subagent prompt", the fenced template): they must be identical outside the slots (task brief, global constraints, start sha, diff, delta diff, prior findings, recheck list). Report any difference outside the slots;
5. the phase report ./artifacts/p0-phase-report.md: every verdict and number in it must match its source (lc1-result.md, lc2-result.md, lc3-result.md, ac-0.5.md, ac-0.6.md, lc<N>-step5.md, lc<N>-step6.md, branch-after and index-after files, the static report), and its P0 verdict must be consistent with every row;
6. whether anything the live checks recorded as PASS is contradicted by a raw evidence file (spot-check at least: lc1/lc2/lc3 step1 timing, step2 samples, step3 worker_done payloads, step4, step7, head-after, branch-after, worktree-list-after; ac-0.5 arithmetic; the AC-0.4 outcome rule applied to each report's status line).

Severity test (from /home/coder/.claude/skills/sc-implement-protocol/refs/qa.md, "Severity model" and "FINAL derived test"): return `issues` ONLY for a blocking defect. A defect is blocking only if at least one of these is `yes`, with one anchor: (a) ac-outcome-missing: output an AC requires is absent, or contradicts the AC text, or an evidence claim you could not verify has no evidence row (anchor: the quoted AC words); (b) false-claim: a claim in delivered text is false against live source (anchor: the live-source path:line holding the contradicting text; a citation or copied value that only drifted is not false); (c) harmful-effect: the run wrote, deleted or chmodded tracked or production data or mutated state outside the task's declared outputs (anchor: the line that is the write); (d) quoted-constraint-breach: a plan Constraint or explicit task instruction is violated (anchor: the quoted text). Notes entries whose four answers are all `no` are cited as `noted` and are not an unmet AC. A blocking line in history that a later status or repair marks resolved is history. Minor wording, cosmetic and "consider changing" items are not `issues`; list them separately as non-blocking.

Known facts you should judge for yourself, not take on trust: the run records that `worker-read --source transcript` returned only a window of each worker's transcript (contentComplete false) and that Step 5 was therefore verified on each worker's session file; that one extra `worker-read --limit 1000` read was made in check 1; that heartbeat condition WC-10 was passed on the reading that subagent time does not count. Decide whether any of these breaks a plan Constraint or an AC at the end state, and say why or why not. Do not decide on the phase verdict beyond checking it is consistent with the rows.

Return exactly:
- Line 1: `FINAL: pass` or `FINAL: issues`.
- Then one line per task AC: `T<i>.AC<k> met|unmet <path:line>`.
- Then the numbered checks 1 to 6 above, each with its result and evidence.
- Then findings, one per line: `F<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n>: <text>`, blocking ones first, then a separate list `non-blocking:`.
- A short self-audit naming what you actively checked.
Do not edit, stage, unstage, move or delete any file, and do not start, stop or release any Orca object.
