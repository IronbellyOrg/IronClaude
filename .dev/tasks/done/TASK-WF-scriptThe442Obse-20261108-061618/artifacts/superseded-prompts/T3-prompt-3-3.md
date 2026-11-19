e42b6fad93894e7144df9bd08a9a35a06d6c5e93

Task brief: Task 3 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 59-88, including the wait-notice paragraph at line 76). Deliverables: driver.sh with subcommands start/send/screen/adopt/answer/stop; send waits for turn end on three conditions (new Stop event counted before the send; a Blocked: line whose on-screen count is taken before the send so only an increase counts; orca terminal wait --for tui-idle); optional wait-notice flag (after the turn's Stop, keep waiting until a background-completion notice has arrived and been answered: a prompt event after the Stop followed by another Stop; timeout prints TURN_END timeout + PENDING notice-not-arrived); NEEDS_INPUT on a permission dialog or login screen and then sends nothing; every wait bounded, default 600s; answer subcommand sends one key with the same [sc-launch:v1: refusal and appends (name key reason) to the package artifacts t10-run-log.md. AC ids: T3.AC1 = "With a stub `orca` whose `read --screen` output is scripted, the self-test shows each of the four outcomes of `send` (`stop`, `blocked`, `idle`, `timeout`), and `NEEDS_INPUT` for a screen holding a permission dialog."; T3.AC2 = "The self-test shows that `send` refuses a text starting with `[sc-launch:v1:` and exits non-zero without calling `orca`."; T3.AC3 = "The self-test shows two blocked prompts in a row: the second send does not report `blocked` from the first send's still-visible `Blocked:` line; it ends on its own new block or its Stop event."; T3.AC4 = "The self-test shows `wait-notice`: a scripted log where the Stop event precedes the `<task-notification>` prompt keeps `send` waiting until the notice and its answer (a further Stop) appear, and times out to `PENDING` when they never do."; T3.AC5 = "The self-test shows `answer` refusing a key line starting with `[sc-launch:v1:`, appending its line to the run log, and sending nothing else."; T3.AC6 = "The help output of the real `orca` for `terminal send`, `read`, `wait`, `create` and `list` is saved to `./artifacts/t3-orca-help.txt`."

Global constraints: plan lines 17-27 (read them in the plan). Key: every script bash set -u -o pipefail, umask 077, every external call bounded by timeout; scratch under /tmp/ob (OB overridable); no change to src/ or tests/; scripts in .dev/issues/442/scripts/; no prompt starting [sc-launch:v1:; settings/hook/git-config/launch-store changes never from driver.

Start sha: e42b6fad93894e7144df9bd08a9a35a06d6c5e93

Diff against the start snapshot: the A3 tree rebuilds driver.sh, driver-helpers.sh, driver-selftest.sh from the Q0 snapshot per T3_brief-3.md and re-adds the staged-release stub arm to selftest.sh. Read all four files in full, plus the fresh run log .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t3-selftest.txt and the re-captured help at artifacts/t3-orca-help.txt.

Delta diff from the previous reviewed tree: the failed attempt-2 tree was reverted to the Q0 snapshot; A3 is a fresh build from that snapshot, so the full diff against the start snapshot is the review surface.

Earlier blocking findings of this start:
F3.1 sev=blocking trigger=B2 family=screen-shape: screen parsed with .screen//.content but real orca returns lines under result.terminal.tail (resolved at attempt 2).
F3.2 sev=blocking trigger=B2 family=notice-vacuous: notice detection vacuous; at attempt 2 still open at new boundaries (EOF exit-0, stale notice latch). A3 rebuilt the notice logic from the Q0 snapshot per advice-3-a: strict in-order Stop -> <task-notification> prompt -> Stop over the lines added after the send (lines_before baseline), failing by default at END; the stub now releases staged log lines one per terminal-wait poll.

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
