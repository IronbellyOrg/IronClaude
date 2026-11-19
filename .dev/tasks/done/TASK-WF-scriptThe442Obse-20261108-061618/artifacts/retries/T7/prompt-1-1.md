55748bc9c1a8c925093d8afc7a84700ab26b235a
Review one task for spec compliance.

Task brief: Task 7 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 175-201). Deliverable: .dev/issues/442/scripts/evidence.sh <item|all>, which runs each item's evidence command from the runbook (.dev/issues/442/observation-runbook.md: section 2.1 lines 230-439, item 7 in section 2.1b, filters F1 to F8 in section 2.2.0 lines 475-535, the OB-H2, OB-H3 and OB-CTX rules at lines 582, 641 and 696) against /tmp/ob/logs (OB overridable) and drafts .dev/issues/442/observation-results.md in the section 4.1 template (lines 734-758) with exactly 12 item blocks; parts that need a reading are marked `needs reading` and keep the item pending; a rerun replaces the file; it also copies logs, screens and the state file to $PKG_ART/ob-logs after a secret scan. AC ids: T7.AC1 = "With a synthetic log built from `tests/hooks/fixtures/launch_level/ob_h1/*.json`, the self-test produces a results file with exactly 12 item blocks. An item whose log is missing reads `Result: pending`."; T7.AC2 = "The self-test classifies synthetic evidence, not only structure: a fixture-variant log where the self-started turn carries a bare `Approved!` yields FAIL for item 5, and a payload whose parent session id is missing or wrong yields FAIL for item 1; neither can produce PASS."; T7.AC3 = "The self-test shows each F1 to F8 filter in the script equal to its runbook text (a diff against the extracted block)."; T7.AC4 = "The self-test shows the secret scan stopping the copy for a planted `ghp_` line and for a planted `Bearer ` line, and the report not containing the planted value."; T7.AC5 = "Running the script twice yields the same file (a `cmp` of two runs)."

Scope note for this task: the plan's OB-H2 rule (runbook line 582) needs the session file's inode compared with the number in the claim's release text before the session is released, and Task 6's session b did not record it. This task therefore also added `inode_record` to .dev/issues/442/scripts/session-gov.sh (run_b calls it right after launch_real) and two self-test cases in session-gov-selftest.sh (OK on a matching inode, FAIL on a mismatch). That is an intended part of this task; judge it for correctness, not as scope creep.

Global constraints: plan lines 17-27 (read them). Key: nothing in this task may run live; every gh call via gh_fork; nothing targets SuperClaude-Org; uv only; every external call timeout-bounded; set -u -o pipefail umask 077; scratch under /tmp/ob (OB overridable); no src/ or tests/ changes; the secret scan must never print a matched value; never stage the project-root artifacts/.

Start sha: 55748bc9c1a8c925093d8afc7a84700ab26b235a

Diff against the start snapshot: new files, read in full: .dev/issues/442/scripts/evidence.sh and .dev/issues/442/scripts/evidence-selftest.sh; changed: .dev/issues/442/scripts/session-gov.sh (inode_record function and its call in run_b), .dev/issues/442/scripts/session-gov-selftest.sh (claim_json now prints "this launch's record has inode number N"; new cases b-inode-ok and b-inode-mismatch), .dev/issues/442/scripts/selftest.sh (one registration line). Helpers you may read for grounding: .dev/issues/442/scripts/lib.sh and session-gov.sh. The saved run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t7-selftest.txt (read it). Runbook grounding: the line ranges above; the payload shapes are in tests/hooks/fixtures/launch_level/ob_h1/.

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
