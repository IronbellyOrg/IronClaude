7e6f69c5c2938b68f592a8ec66bccfcb44b71815
Review one task for spec compliance.

Task brief: Task 1 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 31-42): "Create `.dev/issues/442/scripts/lib.sh`, sourced by every other script, and `.dev/issues/442/scripts/selftest.sh`. `lib.sh` holds: the paths of runbook sections 1.2 and 1.3 (`OB=/tmp/ob`, `/tmp/ob/bin`, `/tmp/ob/logs`, `/tmp/ob/home`, the baseline files); a state file `/tmp/ob/state.env` that records T1 to T4, `WT_T1` to `WT_T4`, each session's terminal handle and governed session id (`GSID`), and the pull request URL, written by appending `KEY=value` lines and read back without `eval`; a `gh_fork` wrapper that adds `--repo IronbellyOrg/IronClaude` (or checks that a `gh api` path starts with `repos/IronbellyOrg/IronClaude/`) and refuses any argument matching `superclaude-org` case-insensitively; a `step` function that prints `BEGIN <id>` and one of `OK`, `SKIP`, `FAIL`, `PENDING` per step; and `main_checkout`, which reads the main checkout path from the first `worktree` line of `git worktree list --porcelain`. `selftest.sh` puts stub `orca` and `gh` commands first on `PATH` (stubs that log their arguments to a temp file and print canned JSON), sets `OB` to a temp directory, and runs each script's test cases; later tasks add their cases to it." AC ids: T1.AC1 = "bash -n passes on both files, and `bash .dev/issues/442/scripts/selftest.sh` prints `SELFTEST_OK` and exits 0."; T1.AC2 = "A self-test case shows `gh_fork issue list` calling the stub with `--repo IronbellyOrg/IronClaude`, and `gh_fork api repos/SuperClaude-Org/x` exiting non-zero without calling the stub."; T1.AC3 = "A self-test case writes and reads back the state file, including a value containing spaces, with no `eval`."

Global constraints: plan lines 17-27 (read them in the plan): owner authorization T1-T4 only; every gh call passes --repo IronbellyOrg/IronClaude, api paths spell repos/IronbellyOrg/IronClaude/..., nothing targets SuperClaude-Org, no Orca --issue/--pr flags, never gh pr merge; uv only; worktrees only via Orca; runbook 5.1 safety list applies to every script; settings/hook/git-config/launch-store changes from the driving agent's shell only; every script bash set -u -o pipefail, umask 077, every external call bounded by timeout; pending never PASS; scripts live in .dev/issues/442/scripts/, scratch under /tmp/ob, no change to src/ or tests/.

Start sha: 7e6f69c5c2938b68f592a8ec66bccfcb44b71815

Diff against the start snapshot: all three files are new (untracked). Full contents follow, plus the saved self-test run log at .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t1-selftest.txt (read it): lib.sh, selftest.sh, lib-selftest.sh under .dev/issues/442/scripts/ (read all three files).

Delta diff from the previous reviewed tree: the fix-pass diff from tree cc6907c95bedd6a5dae2df566ad70074c45b2df4 is saved at .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/retries/T1/delta-1-2.txt (read it).

Earlier blocking findings of this start (empty on the first review):
F1.1 sev=blocking trigger=B4 ac=scope at=.dev/issues/442/scripts/lib.sh:47 anchor="refuses any argument matching `superclaude-org` case-insensitively" chk=amiss:n,false:n,harm:n,constraint:y family=gh-refuse-case fix="Match with nocasematch or lowercased copy; covers explicit --repo/-R slugs" covers="refuses any argument matching `superclaude-org` case-insensitively" first=A1 origin=new: Glob *[Ss]uper[Cc]laude-[Oo]rg* is not case-insensitive; SUPERCLAUDE-ORG/x, SuperClaude-ORG/x pass through to gh.
F1.2 sev=blocking trigger=B4 ac=scope at=.dev/issues/442/scripts/lib.sh:71 anchor="every external call bounded by `timeout`" chk=amiss:n,false:n,harm:n,constraint:y family=timeout-bound fix="Wrap gh/git and the selftest's external calls with timeout" covers="every external call bounded by `timeout`" first=A1 origin=new: command gh, git worktree list and the selftest's own external calls run unbounded (plan Constraints line 26).

Saved-probe re-check hit locations (may be empty): probe-1-1.md after-lines: lib.sh:46-49 (lowercased match), lib.sh gh_fork timeout wrapper, lib.sh main_checkout timeout wrapper, selftest.sh:46 (timeout 60 bash).

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
