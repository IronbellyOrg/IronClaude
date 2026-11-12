# Gap fill P3-G06: what happens when a guard hook is killed at its timeout (hook timeouts, the design's fail-open rows, the speed tests)

- Topic: the research states "fail-closed for governed, fail-open for ordinary" (`research/03-guards.md` C.3) and never says what happens when the host stops a hook at its configured timeout. This file traces the configured timeouts, the design's statements about a timeout, what the tests assert about speed, and what the scripts do when killed.
- Origin: Phase 3 executor gate, fix cycle 1, blocker P3C-11 (depth reviewer finding 1, `qa/phase-3-consolidated.md`). Added after the five original fills P3-G01 to P3-G05.
- Investigation type: read-only trace of the repository (hooks.json, design, merged requirements, tests, the recorded speed results) plus one probe batch on the guard script with fixed input in a private temporary directory (no repository file written, no Orca CLI or app started, no pytest run).
- Scope: `src/superclaude/hooks/hooks.json`, `plugins/superclaude/hooks/hooks.json`, `src/superclaude/hooks/scripts/launch-level-guard.sh`, `docs/designs/sc-issue-launch-level-hook.md`, `.dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md`, `tests/hooks/test_launch_level_guard.py`, `tests/hooks/test_launch_level_guard_registration.py`, the recorded results `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/speed-results.md`.
- Date: 2026-11-11
- Status: Complete

Tag legend: [CODE-VERIFIED] [CODE-CONTRADICTED] [UNVERIFIED]. Paths are relative to the repository root unless absolute. Subordinate or sub-orchestrator mode is deferred and is not described here as shipped.

---

## 1. Configured timeouts (hooks.json)

Source `src/superclaude/hooks/hooks.json` (192 lines, read in full). Timeouts are in seconds. [CODE-VERIFIED]

| Event | Matcher | Hook | Timeout | Lines |
|---|---|---|---|---|
| SessionStart | none | `session-init.sh` | 10 | `:5-10` |
| SessionStart | `*` | `freshness-session-start.sh` | 5 | `:13-21` |
| SessionStart | `startup` | `codegraph-session-start.sh` | 5 | `:23-31` |
| SessionStart | `startup\|resume` | ccsession `session-start.sh` | 5 | `:33-42` |
| UserPromptSubmit | none | `freshness-user-prompt.sh` | 3 | `:45-52` |
| UserPromptSubmit | none | ccsession `session-name.sh` | 5 | `:54-62` |
| UserPromptSubmit | none | `launch-level-guard.sh` | 5 | `:63-71` |
| SessionEnd | none | ccsession `session-name.sh` | 5 | `:73-82` |
| PreToolUse | `Edit\|Write` | `freshness-pre-edit.sh` | 1 | `:85-94` |
| PreToolUse | `Bash` | `block-bare-python.sh` | 3 | `:95-104` |
| PreToolUse | `Bash` | `require-orca-worktree-agent.sh` | 3 | `:105-114` |
| PreToolUse | the guarded-tool regex (Bash, Skill, Agent, Task, Edit, Write, NotebookEdit, Monitor, Workflow, RemoteTrigger, SendMessage, Cron\*, Schedule\*, and `mcp__` merge/push tools) | `launch-level-guard.sh` | 5 | `:115-124` |
| PreToolUse | `Bash` | `launch-job-identity.sh` | 5 | `:125-134` |
| PostToolUse | `Read` | `freshness-post-read.sh` (async) | 1 | `:137-147` |
| PostToolUse | auggie tools | `auggie-flag-clear.sh` | 1 | `:148-157` |
| SubagentStart | none | `freshness-subagent-start.sh` | 1 | `:160-167` |
| SubagentStart | none | `pragmatic-subagent.js` | 5 | `:169-176` |
| SubagentStop | none | `freshness-subagent-stop.sh` (async) | 1 | `:180-188` |

- The orchestration-relevant Bash PreToolUse group is therefore, in array order, `block-bare-python.sh` 3 s, `require-orca-worktree-agent.sh` 3 s, the launch-level guard 5 s and `launch-job-identity.sh` 5 s (the Phase 3 consolidation's "3/5/5/5" was approximate; these are the values in the file). The worktree gate has the shortest budget of the two orchestration guards, 3 s.
- The plugin tree `plugins/superclaude/hooks/hooks.json` carries the same timeouts for the hooks it lists (grep of the `command`/`timeout` pairs: guard 5 on both events, `require-orca-worktree-agent.sh` 3, `block-bare-python.sh` 3, `launch-job-identity.sh` 5, `freshness-pre-edit.sh` 1); it is a subset of the source file (`tests/hooks/test_launch_level_guard_registration.py:121-123`). [CODE-VERIFIED]
- No registration sets `onFailure`; `tests/hooks/test_launch_level_guard_registration.py:63-65` pins that the key is absent from both files. [CODE-VERIFIED]

### 1.1 What the tests pin about the registrations

- The guard is registered exactly once on UserPromptSubmit and once on PreToolUse in both files, each with `timeout` 5 (`tests/hooks/test_launch_level_guard_registration.py:44-51`), not on other events (`:54-60`), with the PreToolUse matcher equal to the design string (`:68-71`); the Bash registrations are exactly the three scripts, the identity hook last and the guard second to last (`:98-118`). [CODE-VERIFIED]
- Not pinned by any test read: the timeouts of `require-orca-worktree-agent.sh` (3) and `block-bare-python.sh` (3), and any execution order beyond array position (already recorded in `research/03-guards.md:237`). Changing 3 to another value passes the registration tests. [CODE-VERIFIED, negative: the file asserts timeout only for the guard entries]

## 2. What the design says happens at a timeout

| Place | Statement | Class |
|---|---|---|
| `docs/designs/sc-issue-launch-level-hook.md:216` (§8 failure table, row "hook killed at timeout") | "call goes ahead (V8, R2)" | [CODE-VERIFIED] as design text |
| `:219` (§8) | "Timeout: 5 s, both entries (FR-L-58)." | design text; matches `hooks.json:63-71,115-124` |
| `:440` (§16 residual risk R2) | "timeout or crash allows \| 1 s budget at 5 s" (tolerated by a 1 s speed budget under a 5 s timeout) | design text |
| `:206` (§8 first paragraph) | "Ordinary sessions are never blocked by a failure (FR-L-53). Governed: default deny last line; EXIT trap maps other exit codes to LL-BROKEN (LL-NOBIND in the prompt branch); ... no `onFailure` (FR-L-54 to FR-L-57)." | design text |
| `.dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md:87` | "Harness facts relied on: V2 and V3 (a PreToolUse exit 2 blocks, also with permission prompts off), ... V8 (a crashing or timed-out hook does not block)" | the source of V8; "relied on", not an observation recorded in this repository |
| `merged-requirements.md:98,694,701` | R2 "A hook that times out or crashes lets the call go ahead (V8). Why: `onFailure: \"block\"` would also block ordinary sessions."; the failure table row "hook killed at its timeout \| the call goes ahead (V8); residual R2"; "`onFailure: \"block\"` is not set on either registration: it would block ordinary sessions whenever the hook breaks (V8)" | requirement text |
| `merged-requirements.md:195,197` | "X-002 (V8 does not force fail-open; a governance hook that exits 0 when it cannot judge is silent non-enforcement)" | the debate's reading: V8 concerns a hook that is stopped, not a hook that chooses to exit 0 |

- Reading: the design accepts that a governed call is NOT blocked when the host stops the hook at its timeout, and records it as residual risk R2. The "fail-closed for governed" behavior of the script is limited to the script's own failure paths (internal error, `jq` or `sed` failure, bad input), which end in an explicit deny (exit 2). A hook that is killed never reaches its deny. The design's mitigation is a speed budget, not a mechanism: a 1 s target (asserted at 3.5 s, see section 4) under a 5 s timeout. [CODE-VERIFIED as design text]
- The fail-open rows that ARE verified by tests (not timeouts): an ordinary session is never blocked by a failure; "identity loss" (no readable top-level `session_id`) allows the call silently even while the store holds a bound session, a "declared fail-open limit" (`tests/hooks/test_launch_level_guard.py:1606-1611`, `test_identity_loss_allows_silently`); and `require-orca-worktree-agent.sh` and `block-bare-python.sh` "fail open (exit 0) on any input they cannot judge" (`tests/hooks/test_require_orca_worktree_agent.py:5`; `tests/hooks/test_block_bare_python.py:5`). [CODE-VERIFIED]
- What the HOST does at a timeout (signal used, whether the call proceeds, whether the user sees a message) is stated only through V8 and was not observed in this repository: [UNVERIFIED]. The design itself lists it among facts relied on (`merged-requirements.md:87`) and the open live observations (OB-H1 to OB-H3, OB-CTX) are skipped tests (`tests/hooks/test_launch_level_observations.py`, see `research/03-guards.md:239`).

## 3. What the guard script does when it is killed (probe, fixed input)

The script's own failure path is an EXIT trap: `ll_on_exit` (`src/superclaude/hooks/scripts/launch-level-guard.sh:147-163`) lets exit 0 and a deliberate deny (2 with `LL_DENIED=1`) through; any other exit is an internal failure, which becomes LL-BROKEN (LL-NOBIND on the prompt branch, exit 2) when the session is governed (`LL_GOVERNED=1`) and exit 0 otherwise (`:153-155`). The trap is installed at `:163`, before stdin is read (`:166`). [CODE-VERIFIED]

One probe batch (private temporary directory under `/tmp`, removed on exit; `env -i`, a PATH holding only symlinks to `cat sed tr mkdir mv ln rm jq awk sleep wc`; a session bound at level full-submit; the script run as `bash launch-level-guard.sh`; no repository file touched):

| Probe | Result |
|---|---|
| Stdin held open and empty for 0.5 s, then `kill -TERM` | exit 143, nothing on stderr (no allow or deny text) |
| Same, `kill -KILL` | exit 137, nothing on stderr |
| A 65,000-byte governed command of repeated `git status` lines (the T-SPD-5 shape), uninterrupted | exit 0 in about 0.75 s |
| The same input, `kill -TERM` after 0.15 s and after 0.3 s (one run each; timing dependent) | exit 143 both times, empty stderr: no LL-BROKEN deny |
| A completed governed call that must be blocked (`git push --force origin f`), for contrast | exit 2 |

[CODE-VERIFIED, run once; the mid-run rows are single runs] Reading: a script that is stopped by a signal does not reach its deny, so a governed call is not blocked by the script; whether the call then proceeds depends on how the host treats an exit that is neither 0 nor 2 or a stopped hook, which is the V8 premise (section 2) and was not observed [UNVERIFIED]. Not probed: a signal arriving after the script has already printed a deny, and the host's own timeout mechanism (probing it needs a live Claude Code session).

## 4. Speed budgets and what the tests assert

### 4.1 The design budget table (`docs/designs/sc-issue-launch-level-hook.md:219-228`)

The text says the numbers are "acceptance targets, not observed results here; 'reported' means collect/report, not already measured. A failing asserted target cannot be waived silently" (`:221`). Rows (NFR-L-01; 100 runs, `time.monotonic()`): T-SPD-1 and T-SPD-2 ordinary session, empty and 1,050-file store, median 20 ms and p95 50 ms, reported; T-SPD-3 ordinary median at most 1.5 times `block-bare-python.sh` in the same run, asserted; T-SPD-4 governed allow and block p95 60 ms, reported; T-SPD-5 governed 64 KB texts and 1 MB "under 1 s each", asserted (`:223-228`). The design also lists a large non-command-field envelope stress case with no size limit implied (`:221`). [CODE-VERIFIED as design text]

### 4.2 What `tests/hooks/test_launch_level_guard.py` asserts (read, not run)

| Case | Test | Asserted | Reported only | Lines |
|---|---|---|---|---|
| T-SPD-1 empty store | `test_speed_empty_store` | no | median 20 ms, p95 50 ms | `:1172-1184` |
| T-SPD-2 store of 1,050 files | `test_speed_stale_store` | no | same targets | `:1187-1199` |
| T-SPD-3 ratio to `block-bare-python.sh` | `test_speed_ratio_to_block_bare_python` | yes, `ratio <= 1.5` | | `:1203-1231` |
| T-SPD-4 governed `git status` and `git commit -m x` at level F | `test_speed_governed` | no | p95 60 ms | `:1239-1250` |
| T-SPD-5 four large commands at full-submit (heredoc with git words 64 KB, backslash lines 64 KB, `git status` lines 64 KB, 1 MB) | `test_speed_large_commands` | yes: every run under `LARGE_LIMIT_S = 3.5` on every runner, xdist workers included; the 1 MB case also asserts exit 2 ("LL-BIG at once") | the 1 s design target (verdict text "over 1 s design target") | `:1262-1298`, constant `:1021` |
| Negative control for the limit | `test_speed_large_limit_catches_10x_slower_guard` | yes: a deliberately slow wrapper (fixed wall clock 2 x `LARGE_LIMIT_S`) must fail the same comparison | | `:1301-1340` |
| Envelope stress, 32 MiB description field, ordinary and governed | `test_speed_large_envelope` | no limit; a run over `ENVELOPE_TIMEOUT = 30` s is recorded as a TIMEOUT row and the test returns without failing | time, peak RSS, or timeout | `:1025-1027,1363-1409` |
| `launch-job-identity.sh` with a pending-only store | `test_speed_identity_hook_with_pending_only_store` | no | median 20 ms, p95 50 ms (recorded as EXCEEDED, 78.9 ms median) | `:1412-` |

- The asserted limit is therefore 3.5 s, not the design's 1 s: the module header says "T-SPD-5's limit (3.5 s) is asserted everywhere, xdist workers included; the 1 s design target stays a reported figure (#440)" (`:996-1000`) and the comment at `:1008-1020` gives the choice (3.0x over CI's worst observed failing maximum, 1.5 s under "the 5 s hook timeout where the governed call fails open"). The recorded decision and measurements are in `.dev/tasks/done/TASK-WF-remediationSou-20261108-061734/artifacts/limit-selection.md` (decision 2026-11-08, `:38-49`). The design text still says "under 1 s each ... asserted" (`:228`); the test is the later authority (see section 6). [CODE-VERIFIED]
- Measured values, from `.dev/tasks/done/TASK-WF-remediationSou-20261108-061734/artifacts/limit-selection.md:5-14` (maxima of the slowest 64 KB case): idle serial 893.9 ms; full suite under `-n auto` 998.6 ms; a CI job log 1166.0 ms; **56 busy loops (2x CPU oversubscription, "not a CI condition") 5536.1 ms**, which is above the 5 s hook timeout; the document says no limit at or below 5 s can clear that arm and that "a run at 5 s is killed and the governed call goes ahead, design :216" (`:33`). Unmeasured: any run on a host that is not one of those conditions. [CODE-VERIFIED as recorded results; not re-run here]
- Earlier recorded run (before the limit change): `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/speed-results.md` (2026-11-07, 28 CPUs): T-SPD-1 median 2.9 ms; T-SPD-2 8.6 ms; T-SPD-4 14.2 and 14.4 ms; T-SPD-5 medians 495.0 to 735.4 ms for the three 64 KB texts (maxima 568.6 to 869.7 ms) and 436.0 ms for the 1 MB text (exit 2); envelope stress 890.0 and 906.7 ms with peak RSS 162 MiB (`:13-26`). That file's text says T-SPD-5 was asserted "under 1 s" (`:9`), which describes the code of that date, not the current 3.5 s. [CODE-VERIFIED as recorded results]

### 4.3 The cost of the 64 KB branch and the BIG branch

- A governed command of 64 KB or less goes through normalisation (`sed` and four `tr` calls, design `:219`), which costs about 0.5 to 0.9 s per call at idle (`tests/hooks/test_launch_level_guard.py:1005-1006`, "A 64 KB run takes 0.5 to 0.9 s"; the recorded medians above). A command over 65,536 bytes is classed BIG and denied before normalisation (design NM1, `:135`; the 1 MB case is the cheapest of the four, median 436.0 ms, because it stops at the size check). [CODE-VERIFIED]
- So a governed 64 KB command spends 10 to 18 percent of the 5 s timeout at idle (0.5 to 0.9 s) and, per the 2x-oversubscribed measurement, can exceed the whole budget; the ordinary-session path is a few milliseconds (T-SPD-1 and T-SPD-2 above) and cannot. The window in which a governed call goes ahead because the hook was killed is therefore reachable by large commands on a loaded host, not by normal commands. [Inference from the cited numbers; no run of a real killed hook]

## 5. Key takeaways

1. "Fail-closed for governed sessions" holds only for the script's own failure paths. A guard hook stopped at its timeout (5 s for the launch-level guard on both events, 3 s for the worktree gate) is not covered: the design records "call goes ahead" as row `hook killed at timeout` and residual risk R2 (`docs/designs/sc-issue-launch-level-hook.md:216,440`), based on the harness fact V8 that was relied on and not observed here. [CODE-VERIFIED as design text; host behavior UNVERIFIED]
2. The script does not convert a signal into a deny: a TERM mid-run of a governed 64 KB command and a TERM while reading stdin both ended with exit 143 and empty stderr; a KILL ended with 137 (section 3). [CODE-VERIFIED, probe, single runs]
3. The mitigation is a speed budget, not a mechanism. The ordinary path is a few milliseconds; a governed 64 KB command costs 0.5 to 0.9 s at idle, and a recorded 2x CPU-oversubscribed run reached 5536.1 ms, above the 5 s timeout (section 4). The asserted test limit is 3.5 s (since 2026-11-08), not the design's 1 s, which is only reported. [CODE-VERIFIED as recorded results]
4. The registration tests pin the guard's timeout (5 on both events, both trees) but not the timeouts of the worktree gate or `block-bare-python.sh` (3 each) (section 1.1).
5. The reference must not write "governed sessions fail closed" without the qualifier "except when the hook is stopped at its timeout, identity is lost, or the session is not governed". Feeds 10.3, 11 and 14.1.

## 6. Corrections to earlier research

| File and place | Earlier statement | Corrected statement |
|---|---|---|
| `research/03-guards.md` C.3 heading and body (`:163-169`): "Failure behaviour (fail-closed for governed, fail-open for ordinary)" | Fail-closed for governed sessions, fail-open for ordinary sessions | Fail-closed holds for the script's internal failure paths only. A hook killed at its timeout allows the call (design `:216`, R2 `:440`; V8, host behavior UNVERIFIED); a signal does not produce a deny (section 3); identity loss allows silently (`tests/hooks/test_launch_level_guard.py:1606-1611`). |
| `research/03-guards.md:237` (registration test paragraph) | The test pins timeout 5 and does not assert the timeouts of `require-orca` or `block-bare-python` | Accurate; add the values from `hooks.json` (3 and 3) and that the plugin tree carries the same values (section 1). |
| `docs/designs/sc-issue-launch-level-hook.md:228` (T-SPD-5 "under 1 s each", Asserted yes) | The asserted target is 1 s | The test asserts 3.5 s; 1 s is reported only (`tests/hooks/test_launch_level_guard.py:996-1000,1008-1021,1296-1298`; decision in `limit-selection.md:38-49`). |
| `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/speed-results.md:9` | T-SPD-5 asserted "under 1 s" | Describes the run of 2026-11-07; superseded by the 3.5 s limit (2026-11-08). |
| Phase 3 consolidation `qa/phase-3-consolidated.md` P3C-11 ("timeouts 3/5/5/5 s") | 3/5/5/5 | 3 (`block-bare-python.sh`), 3 (`require-orca-worktree-agent.sh`), 5 (guard), 5 (`launch-job-identity.sh`). |

## 7. Remaining gaps

| # | Gap | Why it matters | Closure | Reference wording if it stays a limit |
|---|---|---|---|---|
| R1 | What the host does when a hook exceeds its timeout (signal, whether the call proceeds, any message) | Decides whether R2 is a real window or only a design assumption | A live Claude Code session with a deliberately slow hook (outside this task: no live runs) | "The design assumes a hook stopped at its timeout lets the call go ahead (fact V8); this was not observed." |
| R2 | Behavior of the worktree gate and the guard on a host whose load exceeds the recorded conditions | The 5536.1 ms figure came from a 2x oversubscribed arm only | A timed run on that host (pytest; not run here) | "A governed 64 KB command takes 0.5 to 0.9 s at idle and exceeded 5 s once under heavy CPU oversubscription." |
| R3 | Timings of the worktree gate (3 s timeout) | No speed test exists for `require-orca-worktree-agent.sh` (grep of its test file for `monotonic` and `perf` has no hit) | Not closable by reading; a new speed test would be product work (not created here) | "No timing test exists for the worktree gate." |
| R4 | Whether a TERM or KILL by the host reaches the script at the same point as in the probe | The probe sent signals itself | Same as R1 | "Signal behavior was probed by sending signals from a shell, not by the host." |

## 8. Stale or incomplete documentation

- `research/03-guards.md` C.3 heading (qualify as in section 6).
- `docs/designs/sc-issue-launch-level-hook.md:228` (asserted 1 s, now 3.5 s in the test).
- `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/speed-results.md:9` (dated run).
- The module comment `tests/hooks/test_launch_level_guard.py:1005-1006` says "the four T-SPD-5 cases add about 4 minutes"; that is a runtime estimate, not a defect.

## 9. Feeds

**Feeds (template section numbers of `.claude/templates/documents/technical_reference_template.md`):** 10.3 (graceful degradation: what happens when a guard is stopped at its timeout, identity loss, ordinary sessions), 11.1 and 11.2 (performance profile and the performance-critical normalisation step; sections 3.2 to 4.3), 14.1 (limitations: residual risk R2, the 3.5 s versus 1 s gap, no timing test for the worktree gate), 15.1 (verification log: the probe batch of section 3).

## 10. Summary

The launch-level guard has a 5 s timeout on both events and the worktree gate a 3 s timeout (the other Bash gates 3 s and 5 s); the design records that a hook killed at its timeout lets the call go ahead (residual risk R2, harness fact V8, not observed in this repository), so "fail-closed for governed sessions" holds only for the script's own failure paths. In a probe, a TERM sent while the guard read stdin or while it processed a governed 64 KB command ended with exit 143 and no deny, and a KILL with 137. The speed tests assert a 3.5 s limit for 64 KB and 1 MB commands (the design's 1 s is only reported), the ordinary path costs milliseconds and a governed 64 KB command 0.5 to 0.9 s at idle, and one recorded run on a CPU-oversubscribed host reached 5536.1 ms, above the 5 s timeout. The registration tests pin the guard's timeout but not the gate's, and no timing test exists for the gate. What the host does at a timeout was not observed.

Status: Complete
