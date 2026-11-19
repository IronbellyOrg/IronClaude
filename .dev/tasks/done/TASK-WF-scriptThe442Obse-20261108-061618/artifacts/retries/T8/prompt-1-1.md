13ed148d783a90f2b81912b67370f1371efd856a
Review one task for spec compliance.

Task brief: Task 8 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 205-230). Deliverable: .dev/issues/442/scripts/cleanup.sh, which does steps 1 to 8 of runbook section 5.2 (.dev/issues/442/observation-runbook.md lines 785-835) in that order; by default it prints the plan and deletes nothing; with --apply it does each step and prints one line per step; it refuses --apply while .dev/issues/442/observation-results.md is missing. AC ids: T8.AC1 = "With the stub commands, the self-test shows the default run calling no `rm`, `pkill`, `orca worktree rm` or `gh` write command, and the `--apply` run calling them in the section 5.2 order."; T8.AC2 = "The self-test shows step 2 skipping a new store entry that is not a recorded `GSID`, and step 7 refusing while `$PKG_ART/ob-logs/` is missing and while the pre-step-7 diff still shows a `>` line."; T8.AC3 = "The self-test shows step 3 unsetting `extensions.worktreeConfig` only when the state recorded `worktreeConfigPre=unset`, and step 5 listing `SKIP` for a pull request and issues the state file does not record."; T8.AC4 = "A self-test case covers the gated run: issues and worktrees recorded, no PR URL in the state, no governed launch; cleanup still completes every step, skipping step 5's PR close and reporting step 2 as nothing to remove."; T8.AC5 = "Every `gh` call in the stub log carries `--repo IronbellyOrg/IronClaude`."

Global constraints: plan lines 17-27 (read them). Key: nothing in this task may run live (the self-test uses stub pgrep, pkill, rm, orca and gh in temp directories and temp git repositories; it must never delete anything real or touch /tmp/ob); every gh call via gh_fork (--repo pinned); nothing targets SuperClaude-Org; no Orca --issue/--pr link flags; every external call timeout-bounded; set -u -o pipefail umask 077; scratch under /tmp/ob (OB overridable); no src/ or tests/ changes; the script itself never deletes anything without --apply.

Start sha: 13ed148d783a90f2b81912b67370f1371efd856a

Diff against the start snapshot: new files, read in full: .dev/issues/442/scripts/cleanup.sh and .dev/issues/442/scripts/cleanup-selftest.sh; changed: .dev/issues/442/scripts/selftest.sh (one registration line). Helpers you may read for grounding: .dev/issues/442/scripts/lib.sh. The saved run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t8-selftest.txt (read it). Runbook grounding: .dev/issues/442/observation-runbook.md lines 785-835 and the plan text of Task 8.

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
