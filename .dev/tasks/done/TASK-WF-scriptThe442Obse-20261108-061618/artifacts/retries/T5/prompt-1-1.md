6fdae45fcfb2d8f73b7acb9b87a530ab57ee0517
Review one task for spec compliance.

Task brief: Task 5 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 122-146). Deliverables: setup-github.sh for runbook section 1.4 (lines 170-200): four disposable issues (copy ~/.claude/ISSUE-HANDOFF.md to a temp file, fill every section, gh_fork issue create --title ... --body-file <copy>, record each number in the state file); refuses to create issues when the state file already holds numbers; starts the claim session in the main checkout with the driver (start claim path:<main checkout> "env -u CLICKUP_API_TOKEN claude"); for each issue sends /sc:issue --claim <T> --pipeline none, reads "Worktree: <path> (created)" from the screen, records WT_T1..WT_T4; writes each worktree's .claude/settings.local.json with the runbook line-197 generator, labels h2-T1..h2-T4; when that file already exists stops with "EXISTS: merge by hand", never overwrites. AC ids: T5.AC1 = "With the stub `gh`, the self-test shows four `issue create` calls, each carrying `--repo IronbellyOrg/IronClaude` and a `--body-file`, and no second set on a rerun."; T5.AC2 = "The self-test shows the generated `settings.local.json` equal to the output of the runbook's line 197 generator, and the script refusing to overwrite an existing file."; T5.AC3 = "The worktree paths are read from the claim screen, not guessed. A self-test case with a scripted screen records `WT_T1`."

Global constraints: plan lines 17-27 (read them). Key: creating the four issues and the disposable PR is within the owner authorization (plan line 19); every gh call via gh_fork (--repo pinned); nothing targets SuperClaude-Org; no Orca --issue/--pr flags; uv only; every external call timeout-bounded; set -u -o pipefail umask 077; scratch under /tmp/ob (OB overridable); no src/ or tests/ changes; the claim session starts env -u CLICKUP_API_TOKEN claude.

Start sha: 6fdae45fcfb2d8f73b7acb9b87a530ab57ee0517

Diff against the start snapshot: new files — read setup-github.sh and setup-github-selftest.sh in full, plus the changed selftest.sh (gh stub now prints real issue URLs) and lib.sh if changed. The saved run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t5-selftest.txt (read it). Runbook grounding: .dev/issues/442/observation-runbook.md lines 170-200; the template is ~/.claude/ISSUE-HANDOFF.md (4 sections with angle-bracket placeholders).

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
