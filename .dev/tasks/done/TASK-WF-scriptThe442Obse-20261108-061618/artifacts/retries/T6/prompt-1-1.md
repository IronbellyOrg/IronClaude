4bf8f84e56b01a644fcb81014084a87af9447026
Review one task for spec compliance.

Task brief: Task 6 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 137-171). Deliverable: .dev/issues/442/scripts/session-gov.sh with subcommands b, c, d and e for runbook section 2.2.1 to 2.2.4 (.dev/issues/442/observation-runbook.md lines 536-697), prompt files copied byte for byte into .dev/issues/442/scripts/prompts/ (g01 to g09), and the self-test .dev/issues/442/scripts/session-gov-selftest.sh registered in selftest.sh. AC ids: T6.AC1 = "With the stub `orca` and `gh` and scripted screens, the self-test shows session `e` refusing the push prompt when the push URL is not `/tmp/ob/bare-push.git`, and refusing a pull request URL outside `IronbellyOrg/IronClaude`."; T6.AC2 = "The self-test shows the release step refusing an `rm` path that is not this run's `GSID` or its `.ok` file, and treating an already-absent target as released."; T6.AC3 = "The self-test shows `b` and `c` refusing to start when item 5 is not PASS, and `d` refusing when item 1 is not PASS."; T6.AC4 = "Every prompt file matches its runbook `text` block byte for byte (a self-test diff over lines 536-697)."

Global constraints: plan lines 17-27 (read them). Key: the owner authorization covers governed claims on the four disposable issues only, and only when a later authorized run executes the scripts; nothing in this task may run live; every gh call via gh_fork (--repo pinned, api path repos/IronbellyOrg/IronClaude/...); nothing targets SuperClaude-Org; no Orca --issue/--pr link flags; uv only; every external call timeout-bounded; set -u -o pipefail umask 077; scratch under /tmp/ob (OB overridable); no src/ or tests/ changes; settings, hook, git config and launch-store changes only from the driving agent's own shell (LL-TAMPER); no prompt starting [sc-launch:v1:.

Start sha: 4bf8f84e56b01a644fcb81014084a87af9447026

Diff against the start snapshot: new files, read in full: .dev/issues/442/scripts/session-gov.sh, .dev/issues/442/scripts/session-gov-selftest.sh, the nine prompt files .dev/issues/442/scripts/prompts/g01-b-implement.txt, g02-commit.txt, g03-approved.txt, g04-gov-bg.txt, g05-gov-det.txt, g06-gov-clear.txt, g07-c-implement.txt, g08-e-push.txt, g09-e-merge.txt; changed: .dev/issues/442/scripts/selftest.sh (one registration line for the new self-test). Helpers it uses and that you may read for grounding: .dev/issues/442/scripts/lib.sh, driver.sh, driver-helpers.sh. The saved run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t6-selftest.txt (read it). Runbook grounding: .dev/issues/442/observation-runbook.md lines 536-697 and 718-726; the claim result shape is in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py (launch_result, session_report, find_handle, record_launch).

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
