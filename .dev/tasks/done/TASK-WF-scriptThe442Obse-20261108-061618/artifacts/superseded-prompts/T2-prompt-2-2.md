c2ca8c108d05aa8e61b3821a29565a1567c92c1b

REVIEW RE-RUN (r2-2) after the A2 fix pass. The task brief, constraints and start sha are unchanged; the diff now includes the fix-pass delta saved at artifacts/retries/T2/delta-2-2.txt (read it). Earlier blocking findings of this start:
Review one task for spec compliance.

Task brief: Task 2 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 48-62): "Create `.dev/issues/442/scripts/setup.sh`. It runs the checks P1 to P8 of runbook section 1.1 (lines 19-28) and records each command's output to `/tmp/ob/preconditions.txt`; writes the baseline files of section 1.2 (lines 34-39); and builds session A's isolated HOME exactly as section 1.3 (lines 43-169) says, including `/tmp/ob/bin/ob-probe.sh`, `/tmp/ob/bin/ob-tree.sh`, the guard copy, the copied commands, skills and agents, and the session A and A2 settings files written there. It refuses to run if `/tmp/ob` already exists, unless `--resume` is given, and never writes under the real `~/.claude`. It then runs one login check in the isolated HOME (open item 5 of `.dev/issues/442/handoff-runbook.md`): `HOME=/tmp/ob/home CLAUDE_CONFIG_DIR=/tmp/ob/home/.claude timeout 120 claude -p "Reply with the word ok"`. If that fails for authentication, the script prints `BLOCKED login-isolated-home` and exits 3; it never copies credential files." AC ids: T2.AC1 = "With stub commands, the self-test shows the script creating the section 1.3 layout under the test `OB` directory, and refusing a second run without `--resume`."; T2.AC2 = "A self-test case confirms the script writes nothing outside `OB` (it compares a listing of a fake `HOME/.claude` before and after)."; T2.AC3 = "The script's probe files match the text of runbook section 1.3 byte for byte (a self-test case diffs them against the blocks extracted from the runbook)." (The byte-for-byte case covers ob-probe.sh, ob-tree.sh and the session A settings.json; the A2 generator case is in the log too.)

Global constraints: plan lines 17-27 (read them in the plan). Key ones for this task: never write under the real ~/.claude; no probe in the real ~/.claude/settings.json; no superclaude install during the run; every gh call via gh_fork (--repo pinned; api paths repos/IronbellyOrg/IronClaude/...); uv only; every script bash set -u -o pipefail, umask 077, every external call bounded by timeout; scripts live in .dev/issues/442/scripts/, scratch under /tmp/ob (OB overridable for the self-test), no change to src/ or tests/; pending never PASS.

Start sha: c2ca8c108d05aa8e61b3821a29565a1567c92c1b

Diff against the start snapshot: new and changed files under .dev/issues/442/scripts/ — read setup.sh, setup-selftest.sh, selftest.sh in full; the saved self-test run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t2-selftest.txt (read it). The runbook itself is .dev/issues/442/observation-runbook.md (read lines 17-30, 34-41, 43-56 for §1.1-§1.3 grounding).

Delta diff from the previous reviewed tree (empty on the first review):

Earlier blocking findings of this start (empty on the first review):

Saved-probe re-check hit locations (may be empty):

F2.1 sev=blocking trigger=B1 family=T2-probe-source: install sources log-only-probe.sh from main_checkout which lacks tests/hooks/fixtures/launch_level/; silent failure.
F2.2 sev=blocking trigger=B2 family=T2-probe-source: runbook:50-51 says the probe comes from this repo at the checkout root.
F2.3 sev=blocking trigger=B1 family=T2-ac2-listing: the writes-nothing-outside-OB case compared one post-run count, not a before/after listing.
F2.4 sev=blocking trigger=B4 family=T2-timeout-wrap: install, cp -r, chmod, mkdir unbounded.
F2.5 sev=blocking trigger=B2 family=T2-p3-label: P3 output appended before its == P3 header; self-test prec loop skipped P2/P3.
Saved-probe re-check hit locations: probe-2-1.md after-lines cover setup.sh ROOT-based fatal install, before/after fake-HOME snapshots, timeout wraps, P3 header order, prec loop P2/P3.

Do not trust the implementer's report.
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
