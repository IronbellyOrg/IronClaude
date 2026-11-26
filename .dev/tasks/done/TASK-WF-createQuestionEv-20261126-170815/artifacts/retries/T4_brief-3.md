pick: advice-3-a.md; runner-up: none; reason: only passing answer
## Task 4: Settle how a controlled create run loads the revised skill, observes questions, takes an answer and blocks every write, and stop if it cannot
Acceptance criteria:
- `./artifacts/harness-feasibility.md` exists and answers each bullet above with a command and its real output, not a guess; a bullet the environment cannot answer is written as "not available here" with the reason.
- The decision section either says "proceed" with every control named, or is a stop report with the revised estimate; in the stop case no harness file exists under `./artifacts/harness/` until the lead's reply is recorded in the file.
- The file records the dry-run event log excerpt that shows how a question tool call appears (or that none appeared).
- The file records the dry run's command line, its environment (isolated home and configuration directory, the three unset variables, the shadowed `gh`, the invalid push URL) and its probe prompt, which never invokes `/sc:issue` (B-1).
AC ids in bullet order: T4.AC1, T4.AC2, T4.AC3, T4.AC4
Steps:
1. Leave every existing file in `/tmp/createQuestionEv-scratch` as it is. Do not truncate `gh-stub-dry.log`, and do not delete any file under `home/.claude/projects/`. All new raw output goes in that same scratch directory with an `F2` prefix.
2. Write `/tmp/createQuestionEv-scratch/probe_answer.sh` as a copy of `probe_tmux.sh` with these changes:
   - It reuses the same `env -i` launch line, `--permission-mode manual`, `--strict-mcp-config`, the same `probe-prompt.txt` and the same `probe-clone` cwd.
   - It sets `GH_STUB_LOG=/tmp/createQuestionEv-scratch/gh-F2.log`, a new file.
   - Before launch it records the list of `*.jsonl` files under `home/.claude/projects/-tmp-createQuestionEv-scratch-probe-clone/`. After the run it copies the one new transcript to `dry-F2.transcript.jsonl`.
   - When it sees the question screen (it contains `Enter to select` and `keep my wording`), it saves `dry-F2.question-screen.txt`, waits 2 seconds, then sends Enter.
   - It polls once a second for up to 90 seconds. The run is done only when the new transcript holds a `tool_result` line containing `keep my wording`, followed by an assistant text line, and the screen no longer shows `Enter to select`. If the question screen is still showing 10 seconds after Enter, it sends Enter one more time and logs that.
   - It saves `dry-F2.after-answer-screen.txt` and `dry-F2.final.txt`. Every step goes into `dry-F2.driver.log` with a UTC timestamp and a final `ANSWERED` or `TIMEOUT`.
3. Run `bash /tmp/createQuestionEv-scratch/probe_answer.sh` once. Then grep `dry-F2.transcript.jsonl` for `AskUserQuestion`, `tool_result` and `Bash`, and read `gh-F2.log`.
4. Rebuild `./artifacts/harness-feasibility.md` from scratch, section by section in plan order:
   - (a) The `claude --help` options, quoted from `claude-help.txt`.
   - (b) The loading options considered and the one chosen, with `load-list.txt`.
   - (c) The question section: the print-mode result (no AskUserQuestion offered) quoted from dry-A to D and G. The answered result quoted from `dry-F2.transcript.jsonl` (the `tool_use` line and the `tool_result` line) and `dry-F2.after-answer-screen.txt`. The no-answer behaviour from `dry-H.after-wait-screen.txt` and the H transcript.
   - (d) The write blocks. List all five lines of `gh-stub-dry.log` plus every line of `gh-F2.log`, each marked as the probe's stub self-test or a Claude Code start-up read. A start-up read is a call logged within the launch second with no `Bash` tool_use in the transcript; this includes `issue list -R anthropics/claude-code --author @me ...`. Say that the stub forwarded nothing (it exits 97). Then the fork-activity check, keeping attempt 2's rule that unattributed activity is listed and held for review (F1.3).
   - (e) A fresh listing of `src/superclaude/skills/sc-issue-protocol/scripts/`.
   - (f) Fresh sha256 hashes for all 30 files: the src copy, the seeded copy and the installed copy (F1.1).
   - (g) The dry-run command line, environment and probe prompt.
5. Write the decision section. Widen the known-read rule to name the exact start-up reads: `auth token`, and `issue list -R anthropics/claude-code` with read-only flags. The fake gh logs them, answers them with empty canned output and does not stop. Every other unknown call, any other `-R`/`--repo` target, an uninterceptable write, any fork-activity change a run could have caused, or a read of an installed copy still stops every remaining run (Constraints line 23). If step 3 ended `ANSWERED`, write "proceed" and name every control. If it ended `TIMEOUT`, write "answer supply not evidenced here" and a stop report with the revised estimate, whether Phase 1 can ship alone and the question for the lead, then create nothing under `./artifacts/harness/`.
6. Check the rebuilt file is valid UTF-8 (plain ASCII separators) and grep it for secret patterns, as extras-2.log:2-3 did. Copy no raw scratch file into `./artifacts/`; Task 9 does that after its scan.
7. Do not write to GitHub, edit anything under `src/`, or stage `.claude/` or `.dev/issues/`.
differs-by: The answered probe's success is decided from its own retained transcript (a `tool_result` carrying the answer, followed by an assistant reply), with a gh log, transcript copy and screens that belong to that run alone and are never deleted. Earlier attempts judged success from the tmux screen, shared one gh log, and deleted transcripts.
