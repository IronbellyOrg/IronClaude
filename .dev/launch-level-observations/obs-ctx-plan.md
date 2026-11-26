# Plan: OB-CTX observation (B-CTX feasibility gate, design section 14 step 0)

- Status: complete draft for owner review (2026-11-25); no observation has been run, no /sc: command run, nothing staged or committed
- Author: worker task_92e3314dcb94 (planning only)
- Worktree: /home/coder/workspaces/worktrees/IronClaude/obsctx-plan (branch ironbelly/obsctx-plan)
- Repository for every GitHub action: IronbellyOrg/IronClaude only. The upstream SuperClaude-Org is never touched. This plan needs no GitHub write at all.
- Sources read (2026-11-25): docs/designs/sc-issue-launch-level-hook.md lines 76-83 (binding, resolution, identity loss), 207-222 (failure table), 308-320 (observed checks), 339-370 (registration, order of work), 493-508 (19.1), 520-561 (19.3), 569-579 (19.5), 590-629 (19.7, 19.8); /home/coder/.claude/hooks/launch-job-identity.sh (lines 71-80, 177-256, 430-582); tests/hooks/fixtures/launch_level/live_probe.py (all); tests/hooks/fixtures/launch_level/ob_h1/README.md (1-25); tests/hooks/test_launch_level_observations.py (all 110 lines); tests/hooks/test_launch_job_identity.py (test names only); ~/.claude/settings.json (hook registration lines 222-245; probe lines found by grep); src/superclaude/hooks/hooks.json (matcher, by grep); the sibling plan /home/coder/workspaces/worktrees/IronClaude/obs-plan/.dev/launch-level-observations/plan.md (lines 1-140, 183-215); the sibling evidence folder /home/coder/workspaces/worktrees/IronClaude/obs-plan/.dev/launch-level-observations/evidence/ (counted with jq, not copied); the live probe log of issue 842, /tmp/ll-obs-h23.qJA6WFwb/logs/ob-h3.tsv (782 lines when last read, still growing).
- Names used here: OB-CTX is the live observation; B-CTX is the open blocking question it answers (can the hook tell a governed call from a human or ordinary one). "Governed" means a session whose launch-level record exists in `~/.claude/state/launch-level/sessions/<session id>`. A "documented limit" (LIM-n) is a row of the table in design section 19.3.

## 1. Summary
**Answer first.** OB-CTX can be finished with 3 short paid sessions and no GitHub write. The narrow check (typed ids and events on every supported governed call) needs 1 session; resume and fork need 1 short session each. Everything else in the table below is LOCAL, except the optional S9.

- **What it is.** In the code OB-CTX is one skipped test: `test_pending_live_observation[OB-CTX]` (tests/hooks/test_launch_level_observations.py:108-110, name listed at line 79). In the design it has two sizes: the narrow check of section 11 line 320, "valid top-level event/id types on every supported governed leaf call", and the wide lifecycle list of section 19.1. This plan finishes the narrow check in full, takes from the wide list only what one cheap run can show (resume, fork, a human shell beside a live governed job), and records the rest as not observed (section 3).
- **What is already covered.** Four real governed sessions (issues 827, 829, 841 and the running 842) show valid string ids on main-thread and one-level-subagent calls of Bash, Skill, Agent, Edit, Write, SendMessage (before-event only), one MCP tool and UserPromptSubmit. No governed session has shown Monitor, a nested subagent, a background Bash or background Agent, or the selector's verdict on a call. The ungoverned OB-H1 logs do show Monitor, a nested subagent and background calls, with valid string ids (section 5).
- **What is missing, and how.** One synthetic governed session (Run A) that calls each missing tool and asks the selector for its verdict inside every call; then resume (Run B) and fork (Run C). The synthetic session uses a hand-written level file with a fresh UUID in the real store and no launch marker, so it needs no GitHub issue (section 6).
- **LIM-1 to LIM-3.** They stay open as documented limits (owner decision OD-1, design 19.3 and 19.8); they are not named as prerequisites of the gate anywhere in the design. OB-CTX adds a live observation of LIM-1 and LIM-2 and cites the existing real-process tests for LIM-3 (section 9). Open question Q4 asks the owner to confirm in writing.
- **Gate.** OB-CTX is not in `_GATE_ITEMS` (test file line 82), so un-skipping it does not by itself change the ship gate. Recommendation: add it in the flipping commit (Q3).

| Step | Section | Class | Paid sessions | GitHub writes | Un-skips |
|---|---|---|---|---|---|
| S1 coverage checker over existing evidence | 6 | LOCAL | 0 | none | none |
| S2 disposable setup (temp dir, probe, settings, prompts) | 6 | LOCAL | 0 | none | none |
| S3 baseline: installed vs repo selector, existing selector tests | 6 | LOCAL | 0 | none | none |
| S4 Run A: synthetic governed session, all tools | 6 | OUTWARD (paid session, one file in the shared state store) | 1 | none | part of `[OB-CTX]` |
| S5 Run B: resume in a new process | 6 | OUTWARD (paid session) | 1 short | none | part of `[OB-CTX]` |
| S6 Run C: fork | 6 | OUTWARD (paid session) | 1 short | none | part of `[OB-CTX]` |
| S7 read logs, run checker, copy reviewed excerpts | 6 | LOCAL | 0 | none | none |
| S8 un-skip edit in this worktree (no commit) | 8 | LOCAL | 0 | none | `[OB-CTX]` |
| S9 `/clear` in an interactive session (optional) | 6 | OUTWARD (paid session, person types) | 1 | none | none |

Totals (estimates; the design gives no cost figure): 3 paid sessions (4 with S9), 0 GitHub writes, 0 edits of `~/.claude/settings.json`, 1 temporary file in `~/.claude/state/launch-level/sessions/` that is removed afterwards.

## 2. Conventions: LOCAL and OUTWARD, probe logs, evidence
Same conventions as the finished sibling plan (obs-plan/.dev/launch-level-observations/plan.md, section 2).
- **LOCAL:** no GitHub write, no push, no paid model run beyond the session already running, nothing outside a disposable temp directory or this worktree.
- **OUTWARD:** a GitHub write, a push, a paid `claude` session, or a change to shared config or shared state. A new `claude` session is OUTWARD even when it writes nothing to GitHub. For each OUTWARD step the plan gives the exact action, the repository, the cost and the rollback. No step here touches a GitHub repository; if a later pull request carries the un-skip, it targets IronbellyOrg/IronClaude only (`/sc:pr-submit --monitor 3`), never SuperClaude-Org.
- **Facts from the sibling observations (2026-11-25), used as given:** `orca terminal create --worktree path:<wt> --title <t> --command <script>` starts a plain terminal where `claude` runs; `claude -p --settings <file>` works there; the global probe in `~/.claude/settings.json` logs only hook inputs whose cwd is listed in /tmp/ll-obs-h23.qJA6WFwb/cwds.txt, so a disposable cwd adds no line to the issue 842 log; a launch marker typed into a session outside a real claim makes the real guard bind it `degraded` and the real job-identity hook then blocks its Bash calls, so no prompt in this plan carries a launch marker.
- **Probe and logs.** The probe is `tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh` (one JSON line per hook input to the file named by `LAUNCH_LEVEL_PROBE_LOG`, exit 0, no output, no timestamp). Raw logs live in `/tmp/ll-obs-ctx.<random>/logs/` (created with `umask 077`). They hold full prompts and tool inputs, so they are read before anything is copied. When a run passes, the reviewed excerpt goes to `.dev/launch-level-observations/evidence/` under the names in section 6, S7. The probe sees the original `tool_input` before any rewrite (the issue 841 log shows no wrapper text in Bash commands), so a rewrite is proven by the selector's verdict printed inside the call, not by the logged command.
- **Claude version:** `claude --version` printed 2.1.332 on 2026-11-25 (the sibling plan recorded 2.1.331). Record the version in every evidence note.

## 3. What OB-CTX must show
**Quotes (design file docs/designs/sc-issue-launch-level-hook.md, read 2026-11-25).**
- Section 14 step 0 (line 361): "**B-CTX / OB-CTX feasibility gate (§19.1).** Validate the process-context candidate and same-worktree concurrent human isolation with a log-only bounded probe. If it cannot distinguish required lifecycle cases, stop the enforcement implementation and report the exact missing launcher/harness integration. Do not weaken isolation, add infrastructure or start another review loop. This is the first required task in downstream workflow planning."
- Section 11, observed checks (line 320): "**OB-CTX** is the first blocking feasibility check described in §19.1. Extend OB-H1/H2 capture to valid top-level event/id types on every supported governed leaf call."
- Section 3, identity loss (line 81): "OB-H1/OB-H2 must show a valid top-level string id and consistent event shape on every supported governed call; otherwise deployment stops." Failure table (line 213): "id missing or invalid, even with nonempty store | identity-loss allow (§3); stop deployment if observed on supported governed calls". Section 14 step 1 (line 362): "Identity loss on a supported governed call stops deployment."
- Section 19.1 invariant (line 495): "a human push in the same worktree that the selector classifies as `ordinary` is never restricted by launch policy, sees no output and has no stdin read."
- Section 19.1 completion evidence (line 506): "a log-only probe must capture the actual main/subagent/nested/background Bash/Monitor-to-Git and hook process trees, same-worktree human terminal, ordinary Claude session, detached/reparented jobs, launch wrapper, process exit/PID reuse, resume in a new process, /clear/fork, and release while a job remains alive. ... In particular, prove how an ordinary new session in a reused Claude process and an old governed background child can be distinguished at the same time."
- Section 19.1 current verdict (line 508): "B-CTX remains **OPEN/BLOCKING for the earlier plan's complete lifecycle coverage**. The owner authorized the new scoped integration; its per-job selector and isolated live Bash evidence are described in §19.7. That is not a retroactive PASS for the old controller-ancestry probe or for unobserved `/clear`, resume, Monitor, nested-subagent and auto-mode variants. ... Keep production activation conditional on the actual supported execution surfaces and their required observations".
- Section 19.7 (line 606): "Actual persistent-cwd tracking, background scheduling, `/clear`, resume, Monitor, auto mode, concurrent-hook composition and nested-subagent payload variants remain unobserved unless later evidence explicitly adds them."

**How this plan reads them (the design does not say which reading is meant; UNVERIFIED reading, see Q1).**
1. *Type layer (required, finished in full).* Line 320 and line 81 ask for one fact: on every supported governed call the hook input carries a top-level string `session_id`, an event name and a tool name of the right type, and the ids the selector reads are valid. This is what the pending test OB-CTX stands for.
2. *Lifecycle layer (taken where one cheap run can show it).* Line 506 lists 12 cases for the old controller-ancestry design that line 497 says is "not the implemented identity contract". The implemented contract is the per-job selector of 19.7, so each case is mapped to how the selector sees it:

| Case in line 506 | Plan for OB-CTX |
|---|---|
| main / subagent / nested / background Bash | Run A, with the selector's verdict printed inside each call |
| Monitor-to-Git | Run A: a Monitor-started command asks for its verdict (LIM-1). The Git part is not run (L2 text in 19.3) |
| same-worktree human terminal, ordinary Claude session | Run A with a concurrent human shell (S4 step H); Run C is the ordinary new session |
| detached/reparented jobs | Run A: one `setsid` child (LIM-2); existing real-process test, see section 9 |
| launch wrapper | already observed through four real claims (827, 829, 841, 842); the wrapper is the claim itself |
| process exit / PID reuse | not run; covered by the stale-record tests and LIM-14. Reusing a PID cannot be forced safely |
| resume in a new process | Run B |
| `/clear` / fork | Run C for fork; `/clear` only in optional S9 (Q6) |
| release while a job remains alive | existing test `test_release_live_job_and_invalid_bound_state` (test_launch_job_identity.py:427); not repeated live |
| hook process trees / kernel ancestry | not run: 19.7 replaced ancestry by per-job kernel-session membership, so no ancestry bound is needed |
| auto mode, persistent cwd, concurrent-hook composition | not run; stay listed as unobserved in 19.7 (Run A runs with the real hooks registered together, which gives some composition evidence but is not claimed as proof) |

## 4. What counts as "every supported governed leaf call"
The design never defines "leaf". This plan reads it as: one hook input about one tool call by one actor (main thread, subagent, nested subagent), plus the prompt event that binds the session. An Agent call that only starts a subagent is also a leaf call (it is a tool call); the calls the subagent makes are separate leaf calls. UNVERIFIED reading, see Q1.

"Supported" is taken from what is installed, not from what would be nice:
- Events: `UserPromptSubmit` and `PreToolUse` (the two registrations of the guard, design section 13 and ~/.claude/settings.json lines 222-245); `PostToolUse` is read only as a diagnostic, because the selector's verdict printed by a Bash call arrives in its `tool_response` (live_probe.py:84-90 does the same).
- Tools: the guard's matcher, `^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file|update_ref|create_ref|create_branch)` (design line 345; identical in src/superclaude/hooks/hooks.json). The job-identity adapter adds only Bash on `PreToolUse` (launch-job-identity.sh:443-444 returns 0 for any other tool name; design 19.7 "Monitor, other shell tools, remote jobs and unmatched execution mechanisms are not silently supported").
- Actors: main thread, subagent (top-level `agent_id` and `agent_type` strings, `session_id` of the parent), nested subagent.

| Row | Tool and event | Actors | Needed for pass | Notes |
|---|---|---|---|---|
| R1 | `UserPromptSubmit` | main | yes | binds the session; no `tool_name`, no `tool_use_id` |
| R2 | `PreToolUse` and `PostToolUse` of Bash, foreground | main, subagent, nested | yes | selector verdict printed inside the call |
| R3 | Bash with `run_in_background: true` | main (and inside a subagent if the model does it) | yes | supervisor waits for background children (19.7) |
| R4 | Monitor, both events | main | yes (id types); its verdict is `ordinary` by LIM-1 | not adapted; recorded, not "fixed" |
| R5 | Agent, both events | main, subagent (nested start), background Agent | yes | `Task` is an older name; only `Agent` has been seen |
| R6 | Skill, Edit, Write, both events | main, subagent | yes | already well covered (section 5) |
| R7 | SendMessage, `PreToolUse` | main, subagent | yes for Pre; Post is a question | no `PostToolUse` has been seen in any log |
| R8 | NotebookEdit, CronCreate, CronDelete, ScheduleWakeup | main | if the session's tool list has them | availability is read from the stream's init event; "not available" is a result, not a failure (Q5) |
| R9 | Task, Workflow, RemoteTrigger, MCP push-class names | main | not producible here | no plan to build a fake MCP server ("do not add infrastructure", line 361) (Q5) |
| R10 | Read, Grep, Glob | main, subagent | no | not in the matcher; seen anyway |

## 5. Evidence already taken, and what is missing
**How the counts were made (read-only, 2026-11-25).** `jq` over the sibling evidence files and over the shared live log of issue 842 (/tmp/ll-obs-h23.qJA6WFwb/logs/ob-h3.tsv, 782 lines at the last read, 3 governed sessions: 841 with 156 lines, 829 with 171, 842 with 455; the log is still growing, so S1 recounts). A line counts as governed when the probe's store column is not `absent`. Nothing was copied.

| Row | Governed evidence now (main / subagent) | Ungoverned OB-H1 evidence (shape only) | Missing for a governed pass |
|---|---|---|---|
| R1 UserPromptSubmit | 10 lines in the live log; also 827, 829, 841 files | 1 to 4 per session | none |
| R2 Bash foreground | Pre 49 / 17, Post 42 / 15; no nested | item 1: Pre and Post by the nested subagent (agent a80fb217c196cb452, started by agent ae48ae90af1269d82) | nested Bash; the selector's verdict on any call (G1) |
| R3 Bash background | none (no `run_in_background: true` in any governed log) | item 5: main Bash Pre and Post with `run_in_background: true` | governed background Bash (G4) |
| R4 Monitor | none | item 5: Pre and Post, `tool_input` keys `command, description, timeout_ms`, string ids | governed Monitor and its verdict (G2) |
| R5 Agent | Pre 20, Post 20 (main); no Agent call by a subagent | item 1: Agent Pre and Post by a subagent (nested start); item 5: background Agent | governed nested start and background Agent (G3, G4) |
| R6 Skill / Edit / Write | Skill 14/14 and 1/1; Edit 15/12 and 10/5; Write 43/43 and 4/4 (Pre/Post) | not run | none (Pre exceeds Post on Edit and Bash; likely blocked, failed or still-running calls, UNVERIFIED, and `PostToolUseFailure` is not logged) |
| R7 SendMessage | Pre 1 / 9; Post none | not run | `PostToolUse` never seen (G5) |
| R8 NotebookEdit, Cron*, Schedule* | none | none | availability and one call each (G5) |
| R9 Task, Workflow, RemoteTrigger, MCP push-class | none (MCP `codegraph_node` and `codegraph_status` seen: 3 Pre, 3 Post, main) | none | not producible, see Q5 |
| R10 Read / Grep / Glob | many | not run | none needed |

Type check already possible by hand: in the 827, 829 and 841 files no `session_id`, `tool_use_id`, `agent_id` or `agent_type` fails the selector's id pattern (`[A-Za-z0-9][A-Za-z0-9_-]{0,127}`, launch-job-identity.sh:72), and all 158 lines of the 841 file carry a string `session_id`. This is a count, not a test; S1 turns it into a checker. Every subagent line in the 841 file carries the parent's `session_id` (29 lines), which is the OB-H1 item 1 fact again.

**Hygiene notes for reusing the existing files.** (1) The 829 file holds 5 lines of the Coordinator session (store column `absent`), not governed. (2) The 841 file holds 2 subagent lines of session dc89127a (issue 829's agent, cwd issue-829). (3) The 827 file predates the store column; its governed status comes from its notes file (session file content `worktree`). The checker filters by session id and store column, never by file name.

**Gaps, named once and used in section 6.**
- G1 The selector's verdict on a governed call in a real harness session. The real sessions never ask: their logged commands are the model's own. Design 19.7 shows one governed and one ordinary Bash call in an isolated run only.
- G2 Monitor on a governed session: id types, and the verdict of a Monitor-started command (LIM-1).
- G3 A nested subagent on a governed session (Agent started by a subagent; Bash at depth 2).
- G4 Background Bash and background Agent on a governed session.
- G5 `PostToolUse` for SendMessage; availability and ids of NotebookEdit and Cron tools.
- G6 A human shell in the same directory while a governed job is alive, read live.
- G7 Resume in a new process; fork. (`/clear` optional.)
- G8 A `setsid` child inside a real governed Bash call (LIM-2).

## 6. Steps to take the missing part
Order: S1, S2, S3 (all LOCAL), then S4. S5 and S6 run only after S4 passes. S7 after each run. S8 last. Nothing below has been run.

### S1 (LOCAL) Coverage checker over the existing evidence
- Write `tests/hooks/fixtures/launch_level/ob_ctx_check.py` (beside `live_probe.py`): pure functions that take probe lines (JSONL, or TSV with the store column) and a set of governed session ids, and return (a) counts per row R1 to R10 of section 4 and (b) the violations of predicates P1 to P6 of section 7. A thin command line prints the table and `OB-CTX-CHECK violations=<n>`, exit 0 only at 0.
- Run it over the sibling evidence and the live log: `mkdir -p .dev/launch-level-observations/evidence` then `uv run python tests/hooks/fixtures/launch_level/ob_ctx_check.py --tsv /home/coder/workspaces/worktrees/IronClaude/obs-plan/.dev/launch-level-observations/evidence/ob-h3-F-issue-841-probe.tsv --governed-store-column > .dev/launch-level-observations/evidence/ob-ctx-existing-coverage.tsv` (one run per file; the exact options are fixed when the checker is written).
- Expected: the counts of section 5 (the live log has grown since), 0 violations. Any violation here is already a finding for the real sessions, before any new run.
- Cost: none. Rollback: delete the two new files.

### S2 (LOCAL) Disposable workspace, probe settings, prompts, wrappers
Only files in a new temp directory and a throwaway git repo inside it; nothing under `~/.claude` is touched.
```bash
umask 077
OBS=$(mktemp -d /tmp/ll-obs-ctx.XXXXXXXX); mkdir -p "$OBS/logs" "$OBS/work"; git init -q "$OBS/work"
cp /home/coder/workspaces/worktrees/IronClaude/obsctx-plan/tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh "$OBS/probe.sh"; chmod 700 "$OBS/probe.sh"
SID=$(cat /proc/sys/kernel/random/uuid); echo "OBS=$OBS SID=$SID"
for r in a b c; do cat > "$OBS/settings-$r.json" <<EOF
{"hooks":{
 "PreToolUse":[{"matcher":".*","hooks":[{"type":"command","command":"LAUNCH_LEVEL_PROBE_LOG=$OBS/logs/run-$r.jsonl $OBS/probe.sh","timeout":5}]}],
 "PostToolUse":[{"matcher":".*","hooks":[{"type":"command","command":"LAUNCH_LEVEL_PROBE_LOG=$OBS/logs/run-$r.jsonl $OBS/probe.sh","timeout":5}]}],
 "UserPromptSubmit":[{"hooks":[{"type":"command","command":"LAUNCH_LEVEL_PROBE_LOG=$OBS/logs/run-$r.jsonl $OBS/probe.sh","timeout":5}]}]
}}
EOF
done
```
The settings file is passed with `--settings`, so the real guard and the real job-identity hook (both in `~/.claude/settings.json`) still run, next to the probe, exactly as in the real claims. UNVERIFIED: the order the three hooks run in; the probe logs the original input either way.

`$OBS/run.sh` (static; arguments are `OBS RUN MODE SID`):
```bash
#!/bin/bash
OBS=$1; R=$2; MODE=$3; SID=$4
case $MODE in new) F=(--session-id "$SID");; resume) F=(--resume "$SID");; fork) F=(--resume "$SID" --fork-session);; esac
cd "$OBS/work" || exit 1
claude -p --settings "$OBS/settings-$R.json" --permission-mode dontAsk \
  --allowedTools "Bash,Monitor,Agent,Edit,Write,NotebookEdit,SendMessage,CronCreate,CronDelete" \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' --max-budget-usd 1.50 \
  --output-format stream-json --include-hook-events --verbose "${F[@]}" \
  "$(cat "$OBS/prompt-$R.txt")" > "$OBS/logs/stream-$R.jsonl" 2> "$OBS/logs/stderr-$R.txt"
echo "exit=$?" > "$OBS/logs/exit-$R.txt"
```
Three one-line wrappers so `orca terminal create --command` needs no arguments: `printf '#!/bin/bash\nexec %s/run.sh %s a new %s\n' "$OBS" "$OBS" "$SID" > "$OBS/run-a.sh"`, the same with `b resume` and `c fork`, then `chmod 700 "$OBS"/run-?.sh`. `dontAsk` plus `--allowedTools` denies every other tool (denied calls are still logged by `PreToolUse`); the session runs in a throwaway repo. Flags are those of `live_probe.py:228-256` plus `--include-hook-events` (which puts the hook outputs, so the rewrite, into the stream). UNVERIFIED: the order of the variadic flags `--allowedTools` and `--mcp-config` before the prompt; the first thing S4 does is look at `stderr-a.txt`.

Prompt A (`$OBS/prompt-a.txt`; no launch marker). `IDENT` is written out in full in the file:
```text
This is a disposable test directory. Do the steps in order. Do not skip a step because an earlier one failed or was blocked: say so and go on.
IDENT means this exact command: /bin/bash /home/coder/.claude/hooks/launch-job-identity.sh identify
1. Bash: echo A1; IDENT
2. Bash with run_in_background true: sleep 61; echo A2; IDENT
3. Bash: setsid sleep 9 </dev/null >/dev/null 2>&1 & P=$!; echo SETSID_PID=$P; /bin/bash /home/coder/.claude/hooks/launch-job-identity.sh identify $P
4. Monitor with command: sleep 4; echo A4; IDENT
5. Write a file a.txt containing hello, then Edit it to say hello world.
6. Agent (general-purpose): tell it to run Bash "echo A6; IDENT", then to start its own subagent with the Agent tool that runs Bash "echo A6N; IDENT", and to report both outputs. If it has no Agent tool it must say so.
7. Agent with run_in_background true (general-purpose): run Bash "echo A7; IDENT".
8. If your tool list has them, call each once and say which are missing: NotebookEdit (a file n.ipynb), CronCreate with a schedule far in the future and then CronDelete, SendMessage.
9. Wait until every background item has reported, then list steps 1 to 8 with the IDENT output of each.
```
Prompt B (`prompt-b.txt`): `Use Bash once: echo B1; /bin/bash /home/coder/.claude/hooks/launch-job-identity.sh identify. Report only the output.` Prompt C: the same with `C1`.
Cost: none. Rollback: `rm -r -- "$OBS"` only after the evidence is committed and only when `$OBS` still begins with `/tmp/ll-obs-ctx.`.

Human-shell script `$OBS/human-check.sh` (LOCAL; run from a separate shell in the background before S4, so it needs no model):
```bash
#!/bin/bash
OBS=$1; cd "$OBS/work" || exit 1
for i in $(seq 1 600); do P=$(pgrep -xf 'sleep 61' | head -1); [ -n "$P" ] && break; sleep 0.5; done
[ -n "$P" ] || { echo "no job found" > "$OBS/logs/human-concurrent.txt"; exit 1; }
{ echo "human shell (cwd $PWD): $(/bin/bash /home/coder/.claude/hooks/launch-job-identity.sh identify)"
  echo "governed job child $P (cwd $(readlink /proc/$P/cwd)): $(/bin/bash /home/coder/.claude/hooks/launch-job-identity.sh identify "$P")"; } > "$OBS/logs/human-concurrent.txt" 2>&1
```
`identify` only reads the store and `/proc`. This shows, in one real process tree, the case of line 506: "an ordinary new session ... and an old governed background child can be distinguished at the same time".

### S3 (LOCAL) Baseline of the selector
- `cmp /home/coder/workspaces/worktrees/IronClaude/obsctx-plan/src/superclaude/hooks/scripts/launch-job-identity.sh /home/coder/.claude/hooks/launch-job-identity.sh` must print nothing (the installed copy is what the sessions run; the two files were byte-identical when read on 2026-11-25). If they differ at run time, the observation is of the installed copy and the difference is recorded.
- Read the `job` fixture of tests/hooks/test_launch_job_identity.py first to confirm it uses a temporary HOME, then run `uv run pytest tests/hooks/test_launch_job_identity.py -k "setsid or killed_supervisor or release_live_job or old_governed_background_human or controlled_resume" -v`. These are real processes and real git in pytest temp directories (test names at lines 427, 1299, 1406, 1437, 1465). They are simulations of lifecycle cases, not observations (design 19.7 says so for resume and `/clear`); they are the baseline that Run A, B and C confirm live.
- Expected: all pass. Cost: none (writes `.pytest_cache` in this worktree only). Rollback: none.

### S4 (OUTWARD) Run A: synthetic governed session
- **Exact actions.** (1) `S=/home/coder/.claude/state/launch-level/sessions; test -d "$S" && test ! -e "$S/$SID" && printf 'full\n' > "$S/$SID"; ls -l "$S/$SID"` writes one level file named by the fresh UUID, content one level word, mode 0600 (this is the same state `live_probe.py:160-165` writes in its isolated HOME, here in the real store). (2) In another shell: `"$OBS/human-check.sh" "$OBS" &`. (3) `orca terminal create --worktree path:/home/coder/workspaces/worktrees/IronClaude/obsctx-plan --title ob-ctx-run-a --command "$OBS/run-a.sh"`. The person or the coordinator runs these after the owner answers Q2 and Q7; the worker does not.
- **Repository:** none; no GitHub write. If a pull request later carries the evidence, it is opened with `/sc:pr-submit --monitor 3` against IronbellyOrg/IronClaude only.
- **Cost:** 1 paid `claude -p` session: about 9 steps, 5 or 6 subagent and nested calls, capped at 1.50 USD by `--max-budget-usd` (a cap, not an estimate; the design gives no cost; the cap's meaning under the ccsession gateway is UNVERIFIED). Runtime a few minutes (step 2 sleeps 61 s).
- **Shared-state effect:** the one level file in `~/.claude/state/launch-level/sessions/`, and job records in `.../jobs/` while a supervisor lives. Every other session sees a store that is not empty, which it already is (13 entries on 2026-11-25).
- **Rollback.** Right after the run: `ls ~/.claude/state/launch-level/jobs/` must hold no file whose content names `$SID` (check with `grep -l "$SID" ~/.claude/state/launch-level/jobs/*.json`; if one remains, a supervisor was killed, this is LIM-14, and that single file is removed by hand); close the Orca terminal. After S6 (or right after S4 if S5 and S6 are not run, because they need the file): `rm -f -- "$S/$SID" "$S/$SID.ok"`, exactly those two names. Claude's own transcript of the session stays in `~/.claude/projects/` (directory named after `$OBS/work`); it is harmless and is removed with `rm -r --` of that exact directory after the evidence is accepted.
- **What to look at first:** `stderr-a.txt` empty, `exit-a.txt` is `exit=0`, `run-a.jsonl` has a first `UserPromptSubmit` line.

### S5 (OUTWARD) Run B: resume in a new process
Only after S4 passes and its jobs are gone. Action: `orca terminal create --worktree path:/home/coder/workspaces/worktrees/IronClaude/obsctx-plan --title ob-ctx-run-b --command "$OBS/run-b.sh"` (a new `claude -p --resume $SID`; the level file of S4 must still exist, so S4's rollback step 1 waits until S5 and S6 are done). Cost: 1 short paid session. Rollback: as S4. Design expectation (line 83): "`--resume` and renames stay governed (V14)".

### S6 (OUTWARD) Run C: fork
Same as S5 with `run-c.sh` (`--resume $SID --fork-session`). Cost: 1 short paid session. Rollback: as S4; the forked session has a new id and no level file, so nothing more is written. Design expectation (line 83): "`/clear` and `--fork-session` are ordinary (R4)".

### S7 (LOCAL) Read and keep the evidence
1. For each run: read `stderr-<r>.txt`, then `jq -c '{e:.hook_event_name,s:.session_id,a:.agent_id,t:.agent_type,tool:.tool_name,id:.tool_use_id}' "$OBS/logs/run-<r>.jsonl"`.
2. The selector verdicts: `jq -r 'select(.hook_event_name=="PostToolUse" and (.tool_name=="Bash" or .tool_name=="Monitor")) | [.agent_id // "main", .tool_name, (.tool_response|tostring|.[0:300])] | @tsv' "$OBS/logs/run-a.jsonl"`. The stream file gives the init tool list (for R8) and the hook outputs (proof of the rewrite).
3. `uv run python tests/hooks/fixtures/launch_level/ob_ctx_check.py --jsonl "$OBS/logs/run-a.jsonl" --session "$SID"` (and runs b, c).
4. Read the raw files for secrets or stray text, then copy the reviewed excerpts to `.dev/launch-level-observations/evidence/`: `ob-ctx-run-a-probe.jsonl`, `ob-ctx-run-b-probe.jsonl`, `ob-ctx-run-c-probe.jsonl`, `ob-ctx-run-a-stream-excerpt.jsonl`, `ob-ctx-human-concurrent.txt`, `ob-ctx-notes.md` (claude version, the SIDs, dates, the verdict table, any deviation, which rollbacks were done). The existing coverage file of S1 is the sixth.
No step deletes a raw log before the owner has accepted the evidence.

### S9 (OUTWARD, optional) `/clear`
A person starts `claude --session-id <SID2>` interactively in `$OBS/work` (a second level file, same rollback), types `/clear`, then asks for one Bash call with IDENT. Read: does `session_id` change at `/clear`? Cost: 1 paid interactive session. Skipped unless the owner answers Q6 with yes.

## 7. Pass and fail criteria
The design gives no measurable PASS wording for OB-CTX. The predicates below are derived from the quoted sentences and from what the installed selector checks; they are marked "derived" and are part of Q1.

| Id | Predicate (derived) | Source of the wording |
|---|---|---|
| P1 | Every line of a governed run has a top-level string `session_id` that matches `[A-Za-z0-9][A-Za-z0-9_-]{0,127}` | line 81 "a valid top-level string id"; pattern at launch-job-identity.sh:72 |
| P2 | Every line has a string `hook_event_name` in {UserPromptSubmit, PreToolUse, PostToolUse}; every tool line has a string `tool_name`, an object `tool_input` and a string `tool_use_id` matching the same pattern; a UserPromptSubmit line has a string `prompt` | line 81 "consistent event shape"; launch-job-identity.sh:442-447, 467-471 |
| P3 | `agent_id` and `agent_type`, when present, are strings, and on every subagent and nested line the top-level `session_id` equals the run's session id | launch-job-identity.sh:464-466 ("unsupported subagent shape"); line 202 "the parent's `session_id` in subagent and nested-subagent payloads" |
| P4 | Zero lines of a governed run lack a valid `session_id` (zero identity-loss lines) | line 213 "stop deployment if observed on supported governed calls" |
| P5 | The selector's verdict printed inside every Bash call of Run A (main, subagent, nested, background) is `governed` with `session_id` equal to the run's session id. Two verdicts are expected to be `ordinary` and are recorded as the live observation of LIM-1 (the Monitor-started command) and LIM-2 (the `setsid` child); any other value there is recorded and the LIM row is updated | line 600 "emits `governed` with the original session ID, `ordinary` for no registered job or explicit release, and `unknown` for malformed/stale/unreadable registered identity. `unknown` is not a trusted-human verdict." |
| P6 | In `human-concurrent.txt` the human shell reads `ordinary` and the child of the live governed job reads `governed` with the run's session id, in the same working directory, at the same time | line 495 invariant; line 506 "prove how an ordinary new session ... and an old governed background child can be distinguished at the same time" |
| P7 | Run B: every line carries the session id of Run A and its Bash verdict is `governed` with that id. Run C: ids are valid (P1, P2), the session id differs from Run A's, its Bash verdict is `ordinary`, nothing is blocked | line 83 "`--resume` and renames stay governed (V14); `/clear` and `--fork-session` are ordinary (R4)" |
| P8 | Completeness: each required row R1 to R7 of section 4 has at least one `PreToolUse` line for every actor named there; R8 has lines or a "not in the tool list" entry from the stream's init event; R9 is written down as not observed with its reason | line 320 "every supported governed leaf call" |

A run is void, not failed, when its probe log is empty (the probe did not fire), when `stderr-<r>.txt` shows an authentication or flag error, or when the level file was missing at start. A void run is repeated once.

**PASS** (quoted frame): the checker prints `violations=0` for P1 to P4 on Runs A, B, C and on the existing governed evidence; P5 to P8 hold; the evidence note states "valid top-level event and id types on every supported governed leaf call that the harness produced in these runs", names R8 and R9 as not observed, and names `/clear`, auto mode and persistent cwd as still unobserved (design 19.7 line 606).

**FAIL** (quoted consequences):
- P1 to P4 broken on a supported governed call: "Identity loss on a supported governed call stops deployment." (line 362) and "stop deployment if observed on supported governed calls" (line 213). Action: stop, write the exact line and call into the notes, do not patch around it.
- A governed Bash call (P5) or the job child (P6) reads `ordinary` or `unknown`, or the human shell reads `governed`: "If it cannot distinguish required lifecycle cases, stop the enforcement implementation and report the exact missing launcher/harness integration. Do not weaken isolation, add infrastructure or start another review loop." (line 361). Action: stop, name the missing integration, no fix in this task.
- Run B changes the session id (resume is then not governed, against V14 at line 83): recorded as a finding for the owner; it is not hidden by a retry.

## 8. Test it un-skips, and the gate coupling
**The test.** `test_pending_live_observation[OB-CTX]` (tests/hooks/test_launch_level_observations.py:108-110; the id comes from `_PENDING` at line 79, which ends `["OB-H2", "OB-H3", "OB-CTX"]`). Today it runs `pytest.skip(f"{item}: needs a real governed session and has not been run")`.

**S8, the un-skip edit (LOCAL, in this worktree, not committed here):**
1. Remove `"OB-CTX"` from `_PENDING` (line 79), so the parametrized skip no longer lists it.
2. Add `test_ob_ctx_evidence_meets_p1_to_p8`, which reads `.dev/launch-level-observations/evidence/ob-ctx-run-{a,b,c}-probe.jsonl`, `ob-ctx-human-concurrent.txt` and `ob-ctx-existing-coverage.tsv` and asserts P1 to P8 through `ob_ctx_check.py`. Removing the name alone would satisfy the coupling test with no evidence (the sibling plan makes the same point, section 8), so the review of the commit checks the evidence, and the new test checks its shape.
3. Add synthetic good and bad lines to the checker's own test (missing `session_id`, `session_id` an integer, an id with a space, `agent_id` an integer, a subagent line with another session id) so the checker fails when it should.
4. Update the status text that says OB-CTX is pending: design lines 6 and 627 (frontmatter `status:` and "Pending, none run"), and line 320 stays as the definition. Edit in the design file only; no `src/superclaude/` path is involved. Nothing under `.claude/` is staged (CLAUDE.md).

**Dependencies.** The test reads the sibling evidence (827, 829, 841 files) through the S1 output, so the sibling observations branch must be merged first or its files copied; both commits touch line 79 of the test file, so the second to land rebases. UNVERIFIED: whether the coordinator wants the existing-coverage file to carry its own copy of the governed lines it counted (it holds counts, not lines).

**Gate coupling.** `_GATE_ITEMS` (line 82) is `("OB-H1 item 1", "OB-H1 item 5", "OB-H2", "OB-H3")`: OB-CTX is not in it. Un-skipping OB-CTX therefore changes nothing for `launch.GOVERNED_LEVELS_ALLOWED`. If the owner wants the gate to wait for OB-CTX (Q3), the flipping commit adds `"OB-CTX"` to `_GATE_ITEMS` and also changes line 94, `assert _gate_may_be_open(True, ["OB-H1 item 2", "OB-CTX"])`, which would fail once OB-CTX is a gate item. The other gate edits (launch.py:48, the closed-gate tests, claim.md:136, the wording of items 1 and 5) are the sibling plan's section 8 and are not repeated.

## 9. LIM-1 to LIM-3: open limits or gate prerequisites
**Answer: they stay open as documented limits. They are not prerequisites of the gate in the design as written.** The owner's confirmation is Q4.

What the design says (read 2026-11-25):
- Section 19.8, line 618: "The B-CTX gaps (Monitor, `setsid`, a killed supervisor) are documented limits LIM-1 to LIM-3 of §19.3, not built coverage."
- Section 19.3, line 536: "**Limits (OD-1).** L2 is a same-user guard for the tested local Bash surface, not a sandbox, and neither layer guarantees universal AC-6." Rows LIM-1 to LIM-3 are at lines 540-542.
- Section 19.7, line 602: "Deliberate `setsid`/daemonization escapes kernel-session selection; supervisor killing leaves stale/unknown state for surviving registered jobs. Monitor, other shell tools, remote jobs and unmatched execution mechanisms are not silently supported."
- Section 19.8, line 627, the gate: "No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed." No LIM row is named there or in section 7 item 4.
- Section 19.1, line 508: "B-CTX remains **OPEN/BLOCKING for the earlier plan's complete lifecycle coverage**" and "Keep production activation conditional on the actual supported execution surfaces and their required observations". The supported surface is Bash; Monitor is outside it. IR-7 (line 357) asks for "the proven B-CTX context contract" before a governed pipeline starts: OB-CTX passing on the supported surface is what proves it, so it must pass; the three limits do not have to close.

| Limit | Design row | What OB-CTX records | Expected | Where |
|---|---|---|---|---|
| LIM-1 | "Monitor tool commands report `ordinary` (B-CTX)"; no identity adapter; impact High ("a governed push from Monitor is allowed") | Run A step 4: Monitor Pre and Post lines (ids valid, P1 to P3) and the verdict of a Monitor-started command | `ordinary` | live (G2) |
| LIM-2 | "A `setsid`/daemonized child escapes the supervisor's kernel session (B-CTX)"; impact High (child reads `ordinary`) | Run A step 3: the verdict for a `setsid` child inside a governed Bash call | `ordinary` | live (G8), plus test `test_real_git_deliberate_setsid_escape_is_unselected_not_retained` (test_launch_job_identity.py:1437) in S3 |
| LIM-3 | "A killed supervisor turns its live child into `unknown` (B-CTX), with reason `orphaned`"; impact Low (still refuses main and master, OD-2) | not run live: killing the supervisor of a tool call ends that call and leaves a stale record (LIM-14) in the real store | `unknown`, reason `orphaned` | test `test_real_git_killed_supervisor_is_unknown_not_proven_human` (line 1465) in S3 |

What changes if the owner wants one closed first: LIM-1 needs an identity adapter for Monitor (can a Monitor command be rewritten the way Bash is? not observed; UNVERIFIED). That is a new design and build, and design step 0 says "Do not weaken isolation, add infrastructure or start another review loop". If OB-CTX fails on the supported surface, step 0 says to stop and "report the exact missing launcher/harness integration"; that report, not a fix, is this task's output.

## 10. Open questions for the owner
Each question: the recommended answer is first, then one line per answer saying what it does.

- **Q1. Scope and criteria.** Do Runs A, B and C (the type check on every producible governed call, resume, fork, and a human shell beside a live governed job), record everything else of line 506 as not observed, and judge it with predicates P1 to P8 of section 7?
  - Yes, as planned (recommended): 3 paid sessions; the pass statement is limited as in section 7; `/clear`, auto mode, persistent cwd and PID reuse stay listed as unobserved in design 19.7.
  - Run A only: 1 paid session; resume and fork stay unobserved, so design lines 506 and 606 keep naming them as open.
  - The full list of line 506: adds `/clear` (S9) and needs a new decision on the process-tree items that 19.7 replaced; larger and not planned here.
- **Q2. Synthetic governed session or a real claim.** May the observation use a hand-written level file with a fresh UUID in the real store (no launch marker, removed afterwards)?
  - Yes, synthetic (recommended): no GitHub write, full control of the calls; same store state that `live_probe.py` writes in its isolated HOME; one shared-state file, removed by the rollback.
  - Real claim on a test issue: needs a new issue, an assignee and a ClickUp touch on IronbellyOrg/IronClaude, plus a launched agent; the tool calls cannot be scripted exactly, so some rows would stay missing.
  - Isolated HOME like `live_probe.py`: touches no shared state, but login and the ccsession gateway under an isolated HOME are UNVERIFIED; it needs one no-op session first to find out.
- **Q3. Does the ship gate wait for OB-CTX?** (`_GATE_ITEMS` omits it.)
  - Yes (recommended): the flipping commit adds `"OB-CTX"` to `_GATE_ITEMS` and changes test line 94; matches design step 0 ("the first required task") and IR-7 ("the proven B-CTX context contract").
  - No: the gate opens on the four items; OB-CTX still un-skips, and 19.1's "OPEN/BLOCKING" is recorded as an accepted risk.
- **Q4. LIM-1 to LIM-3 stay open as documented limits for the flip?** (Section 9.)
  - Yes, and OD-1 covers the flip (recommended): the limits stay in the 19.3 table with the new observations cited; no code change; the owner says so in chat and the agent records it.
  - Close LIM-1 first: needs a Monitor adapter, a separate design and build; the gate waits for it.
  - Close all three first: adds containment for `setsid` and supervisor kill; large, not recommended.
- **Q5. Tools the harness cannot produce here** (Task, Workflow, RemoteTrigger, Schedule*, MCP push-class names, and any of NotebookEdit and Cron* missing from the tool list).
  - Accept "not observed" with the reason in the evidence note (recommended): every other tool in the matcher is observed; the pass sentence names the gap.
  - Require them: needs a fake MCP server and special tool setup, which step 0 calls "infrastructure".
- **Q6. `/clear`.** Observe it in S9?
  - Skip (recommended): `/clear` stays unobserved in 19.7; design R4 already calls a cleared or forked session ordinary.
  - Run S9: 1 more paid interactive session typed by a person; shows whether `session_id` changes at `/clear`.
- **Q7. Spend.** May the coordinator (or a person) launch Run A, then B and C only if A passes, each capped by `--max-budget-usd 1.50`?
  - Yes (recommended): 3 sessions, 0 GitHub writes, rollbacks as written in S4.
  - A different cap: tell me the number; the scripts take it from one line.
  - No: only the LOCAL steps S1 to S3, S7 and S8 run on the existing evidence; OB-CTX stays pending, with the coverage table of section 5 as the record.
