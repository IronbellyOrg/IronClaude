a4bb361e1c6375fe1dedddd00ccf6192329f8a51
Review one task for spec compliance (attempt 3, rebuilt from the start snapshot).

Task brief: Task 9 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 234-248). Deliverable: edits to .dev/issues/442/observation-runbook.md (replace the two wrong statements about non-representative prompts and the person-only release; update the neighbouring statements the scripted path makes false; record the owner's authorization of 2026-11-08 for T1 to T4 in the "Starting the sessions" bullet; add `## 6. Scripted path` naming each script, the order, the cleanup's --apply rule, and the NEEDS_INPUT and BLOCKED login-isolated-home stops) and a short paragraph in .dev/issues/442/handoff-runbook.md under "What is left". AC ids: T9.AC1 = "The old wording is gone: `grep -n 'not representative' .dev/issues/442/observation-runbook.md` prints nothing (it also prints nothing before the edit, so the real check follows), `grep -n 'must be.*typed by a person' .dev/issues/442/observation-runbook.md` prints nothing, and `grep -c 'orca terminal send' .dev/issues/442/observation-runbook.md` is at least 1; the last two fail before the edit, so the check cannot pass vacuously. Section 6 names every script file that exists in `.dev/issues/442/scripts/` (a self-test case compares the two lists)."; T9.AC2 = "`bash .dev/issues/442/scripts/selftest.sh` still prints `SELFTEST_OK` after the edit, because the prompt and filter diffs read the edited runbook."

Global constraints: plan lines 17-27 (read them). Key: nothing may run live; the runbook must not claim anything the scripts do not do and must not overstate verification (every statement about what a script does has to be true against that script); no src/ or tests/ changes.

Start sha: a4bb361e1c6375fe1dedddd00ccf6192329f8a51

Diff against the start snapshot: the runbook and handoff are untracked in git, so the change is saved as a real tree-to-tree diff at /tmp/t9-a3.diff (read it in chunks of at most 150 lines); it covers .dev/issues/442/observation-runbook.md, .dev/issues/442/handoff-runbook.md, .dev/issues/442/scripts/selftest.sh (one registration line) and the new file .dev/issues/442/scripts/runbook-selftest.sh (read in full). The saved run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t9-selftest.txt (read it). Grounding for the quoted script fragments in sections 4.2 and 6 of the runbook: the scripts in .dev/issues/442/scripts/ (driver.sh, driver-helpers.sh, session-a.sh, session-a2.sh, session-gov.sh, setup.sh, setup-github.sh, evidence.sh, cleanup.sh); check that each quoted fragment is on the line it cites and that every sentence around the quotes is true.

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
