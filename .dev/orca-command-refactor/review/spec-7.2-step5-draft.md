# Draft for owner review: spec section 7.2, step 5 (session file as primary source)

Status: DRAFT. The spec file `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` is NOT edited. Nothing is committed or pushed.
Date: 2026-11-04. Basis: the P0 live checks, `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md` (notes 1 and 2) and the owner's two decisions: (1) the session file is the primary source for the worker-behaviour check, `worker-read` is the end-of-run cross-check, and a missing file is `not verifiable`, never PASS; (2) subagent time does not count toward the heartbeat cadence, with two limits: 5 minutes without a heartbeat after removing subagent time, and a 20-minute raw ceiling.

## A. Replacement for step 5 (spec line 291)

Replace the whole of step 5 with the text between the rules below. It keeps the five conditions of the current step 5 and the "vacuous pass" sentence; it changes the source, the heartbeat rule and the failure mode.

---

5. Check the worker's behaviour over the whole run. The primary source is the worker's own session file; `worker-read` is the cross-check for the end of the run.
   - **Source file.** For a Claude worker started on this machine the file is `~/.claude/projects/<dir>/<session id>.jsonl`, where `<dir>` is the worker's worktree path with each `/` replaced by `-`; each subagent's own file is under `~/.claude/projects/<dir>/<session id>/subagents/`. The disposable worktree is fresh, so `<dir>` must hold exactly one top-level `.jsonl` file; none or several make the source ambiguous. Run the analysis after step 3 and before step 7, with Python under `uv run`. Record the file's path, byte length and sha256 in the phase evidence; the file keeps growing after `worker_done`, so a later re-check uses the first recorded byte length. Do not copy the file into the repo (it holds full prompts and tool output); keep the analysis only.
   - **Cross-check.** `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json`, page 1, then once more with the returned `cursor`. Record `contentComplete`, the time window page 1 covers, and whether the second page is empty. Orca 1.4.237 returns only the last 40 to 50 messages and its cursor never ends (P0, phase report note 1), so this read cannot show the start of a run. It must show the same final `check` call and the same `worker_done` as the session file, and tool calls by name (AC-0.6). If the two sources disagree, step 5 fails.
   - **Pass conditions, all read from the session file:**
     1. No `AskUserQuestion` call, in the top-level session or in any subagent session (WC-2).
     2. The command was run in the worker's top-level session, not inside an Agent-tool call (WC-7): the Skill or command call is a top-level message, not a subagent message.
     3. A `check` call appears after the command finished and before `worker_done` (WC-12).
     4. Heartbeats (WC-10), against the cadence in the worker's own dispatch preamble (5 minutes in Orca 1.4.237). Measure the time between consecutive heartbeats, and from the brief to the first heartbeat and from the last heartbeat to `worker_done`. Both limits must hold: (a) after removing the time during which any subagent of the worker was running, or the worker was blocked in `ask` or `check --wait`, at most the cadence; (b) with nothing removed, at most 20 minutes. A subagent's running time is the interval from the first to the last timestamp in that subagent's own session file. Limit (a) removes legitimate waiting on a command's fan-out (the worker cannot heartbeat while it waits, `WORKER-CONTRACT.md:44`); limit (b) bounds a hung subagent.
     5. No `worker-start`, `dispatch` or `task-create` call and no `worktree create --agent` or `agent launch` call (WC-13), searching every Bash command of the top-level and all subagent sessions under any Orca binary name. Read-only calls through the Orca binary (for example `orca-ide skills get ...`, `orca-ide --version`, `orca-ide orchestration worker-list --json`) are not these calls and are listed in the evidence.
   - **Not verifiable.** If the session file is missing, ambiguous, unreadable or contains no tool calls (it is Claude Code's format, not Orca's), conditions 1, 2, 4 and 5 are recorded `not verifiable`. Step 5 is then not passed, the live check is not recorded as passed, and the phase report lists the gap. Condition 3 may be judged from the `worker-read` page when that page covers the end of the run. A condition that was not checked is never recorded as PASS. For an agent other than Claude no source file is defined here, so step 5 is `not verifiable` until one is specified.
   - A run shorter than the cadence passes condition 4 vacuously, so each phase report names at least one checked run that lasted longer than the cadence.
   - AC-0.6 (P0) confirmed that tool calls appear by name in `worker-read`; the session file records them as `tool_use` blocks with a `name`.

---

## B. One-phrase edit elsewhere in 7.2 / 7.3

- AC-0.4 row (spec line 301), in the Check column: replace "verified in the step-5 transcript" with "verified in step 5 (the worker's session file)".
- No other change to steps 1 to 4, 6 and 7. Step 3 keeps its `worker-read` stall proof: that proof needs only the most recent messages, which the window provides.

## C. Items to add to the spec's UNVERIFIED list (numbers assigned when the spec is edited)

1. The `<dir>` rule is verified only for `/` in the worktree path (P0 paths contained no other special characters). The mapping for `.` and other characters is not verified.
2. The session file's location, format and `tool_use` structure are Claude Code's, not Orca's, and may change with a Claude Code update. The analysis should fail loudly (no tool calls found), which condition "Not verifiable" handles.
3. Whether Claude Code deletes old session files, and after how long. `cleanupPeriodDays` is unset on this machine, so the default applies; its value is not verified here.
4. Remote Orca servers (`--environment`, `--pairing-code`) and non-Claude agents: the session file is not on the coordinator's machine, or has another format.
5. Whether `orca orchestration inbox` keeps the full heartbeat history (only `lastHeartbeatAt`, the latest, was seen), and whether `worker-list --run` shows workers started by workers.
6. The 20-minute raw ceiling is a starting value: the longest raw gap observed in three P0 runs was 14.5 minutes (longest after removing subagent time: 3.3). Review it after P1 with more runs.

## D. Evidence this draft rests on

- P0 runs: 46, 87 and 32 minutes; `worker-read` windows covered the last 8, 3.7 and 6.6 minutes; `contentComplete` false in all three.
- Raw heartbeat gaps up to 7.5, 14.5 and 7.7 minutes; longest stretch after removing subagent time 2.2, 2.0 and 3.3 minutes (`lc<N>-session-analysis.txt`, scripts `session-analysis.py` and `session-hbcover.py` in the P0 package's `artifacts/`).
- Four independent reviewers recomputed the same numbers from the session files.

## E. Decisions the owner still has to make

1. **Effect of `not verifiable` on a phase.** Drafted as: step 5 is not passed and the live check is not recorded as passed, so the phase cannot be reported PASS until the owner accepts the gap in the phase report. Alternative: the phase may close with the gap listed. The owner's instruction fixes only "never PASS".
2. **Where the analysis scripts live.** The two P0 scripts are in the archived P0 package. Options: cite them by that path in 7.2 (no new files), or add a tracked script (a code change, so a separate plan). Not part of this spec edit.
3. **Wording of condition 4(b).** The 20-minute ceiling applies to the raw time between the same points as 4(a). Confirm that reading.
