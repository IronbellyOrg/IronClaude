# Codebase Context: worker liveness

## Sources and quality tier

- Tier A (primary, run 2026-11-07): Orca CLI `--help` output and `orca skills get orchestration` guide plus references, from the installed binary `1.4.245-aidev02.780594c521aa`. These are documented behaviour, not observed runtime behaviour; no worker was started or inspected.
- Tier A: repo files read with line numbers (`src/superclaude/core/WORKER-CONTRACT.md`, developer guide, `src/superclaude/cli/**`).
- Tier B: GitHub issue bodies #423, #339 (read-only `gh issue view --repo IronbellyOrg/IronClaude`); `.dev/issues/431/issue-body.md`; `.dev/research/orca-dashboard-20261105/REPORT.md` (earlier research, 2026-11-05).
- codegraph and auggie were not used; searches used Grep.

## Orca CLI liveness and messaging capabilities

Orca `1.4.245-aidev02.780594c521aa` (`orca --version`). Sources: `--help` output and the version-matched guide `orca skills get orchestration` (215 lines; `--full` 890) plus `--reference references/<name>.md`, run 2026-11-07. Guide line numbers refer to that printed output.

- **Message types** (`orca orchestration send --help`): `status, dispatch, worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat`. Heartbeat payload fields: free-text `--phase`, `--task-id`, `--dispatch-id`, raw `--payload <json>`. No step ID, counter or deadline field.
- **Wait filter** (`check --help`): "`--types` is the wake condition for `--wait`; a returned Delivery is always the whole FIFO batch, so it is never filtered by type." A narrow filter delays the wake (case 4) but the message is in the next batch. `--wait` writes a `_keepalive` line to stderr every 15 s (the waiter's own liveness). Guide lines 113 and 142 use `--types "worker_done,escalation,question" --timeout-ms 900000`, which omits `status`, `handoff`, `merge_ready`, `decision_gate`.
- **Read receipts: none for the sender.** `check --ack <delivery_id>` is the reader acknowledging its own batch; `--peek`/`--all` do not mark read. `references/messaging-and-gates.md` lines 6-7: "A successful `send` proves durable enqueue. Wake and nudge are best-effort attention only: neither proves the recipient read the message, began a turn, or accepted steering." Whether `orchestration inbox --full --json` exposes per-message read state is UNVERIFIED (not run).
- **Ask** (`ask --help`): `--timeout-ms` 1..1800000, default 600000; timeout leaves the question pending; resume by message ID.
- **Liveness verdicts.** Guide lines 62-64: `worker-list` `projection.liveness` is the fleet verdict; `worker-show` `observation.status` is PTY liveness only; "A live terminal can still hold a dead or stuck agent." Rows carry `projection.attention.categories`, `requiresAction`, literal `nextAction` argv (`recovery-and-cleanup.md` 25-28). Verdicts `live` / `unverifiable` / `exited`; unverifiable reasons `missing_status`, `stale_status`, `restored_unconfirmed`, `host_unavailable`, `capability_unsupported` (recovery 33-38, 58). The set of attention category values is not documented: UNVERIFIED.
- **Blocked on a prompt** (`worker-show --help`): `observation.agentWait` "names a worker parked on a prompt only a human can answer, with the evidence that proved it (hook, prompt-text, or title)"; null = looked, none; absent = never looked. "A waiting worker is healthy, not failed." `orca worktree ps --agent-wait` adds the same verdict per row. Covers case 6 only if polled.
- **Stall proof** (`recovery-and-cleanup.md` 52-60): leave the wait only on `exited` liveness, the worker's own process-exit observation, "or a transcript whose final agent turn sent no `worker_done`." Null `agentWait` or an unchanged `worker-read` tail is absence; absence never authorizes stop/abandon/retry/release. Guide 150-153: after three consecutive empty waits, run `worker-list --include-remote` and act on `nextAction`.
- **Idle**: `orca terminal wait --for exit|tui-idle [--timeout-ms]`. No "idle since" timestamp is documented.
- **Screen read**: `orchestration worker-read --dispatch <id> --source auto|transcript|terminal` (auto prefers the hook-reported transcript); `orca terminal read --screen` reads the rendered frame.
- **Nudge**: `orca terminal send --text --enter [--interrupt] [--wait-submit <s>]`; for an agent prompt "the result separates input acceptance from observed submission and turn start" — the only verb with an observed-turn-start receipt. Not every worker has a terminal (`worker-start --help` notes).
- **Search**: `orca search <q> --since <iso> --sort newest --agent` over indexed session text; no last-activity field documented.

## Orchestration skill and developer guide

- `~/.claude/skills/orchestration/SKILL.md` (68 lines) is a discovery stub (line 16): it holds no liveness guidance itself and tells the agent to load `ORCA skills get orchestration` (lines 49-61). Lines 34-40: on Linux outside an Orca terminal use `orca-ide`, never bare `orca` (GNOME screen reader). All liveness rules therefore live in the binary's guide (previous section).
- `~/.claude/skills/orca-cli/SKILL.md`: Grep for stall/heartbeat/idle/nudge/agentWait/tui-idle/worker-read found no liveness guidance (only line 45, a sandbox-permission note).
- Developer guide `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` section 7.7 (line 972): coordinator is a hand-opened session that plans, creates one Task per unit, starts one worker per Task, reads reports (line 978); worker is one top-level session running one `/sc:` command, reporting with `worker_done` (979); commands contain no Orca calls (980); orchestration skill is a stub, IronClaude coordinator rules are in WORKER-CONTRACT section 4 (981). Line 1007 restates WC-10 (4-minute blocking limit). Line 1289 lists "one long blocking Bash wait" as an anti-pattern because the worker cannot heartbeat.

## Worker contract hooks (WC rules relevant to liveness)

File: `src/superclaude/core/WORKER-CONTRACT.md`.

- **WC-10 (line 44), liveness during long waits.** Heartbeats at preamble cadence; any single blocking Bash call over 4 minutes must be split. A command's own Agent-tool fan-out may hold the session past the cadence with no heartbeat, and "that gap is accepted". The coordinator "treats a missing heartbeat as absence, never as death ... acts only on Orca's stall proofs." This rule is why a missing heartbeat can never trigger action today.
- **WC-3 (lines 51-56), questions.** Default `report blocked`; with `ask the coordinator` the worker asks once per Task, resumes the same message ID on timeout, sends no heartbeat while blocked in `ask` (56). A second block ends in `worker_done --outcome failed`.
- **WC-12 (line 59), follow-ups are pulled.** The worker runs `check` at natural checkpoints and before `worker_done`. A mailbox `reply`/`send` therefore reaches an idle or busy worker only when it next checks — consistent with case 5 (answers unseen 35-40 minutes until typed into the terminal).
- **Heartbeats bullet (line 61).** Preamble cadence and command; none while blocked in `ask` or `check --wait`; never from a subagent (WC-7).
- **WC-6 (lines 67-74), retry = new Task.** No retry while the attempt is unsettled or `unverifiable` (72); "A crashed or stalled attempt is settled by the coordinator: after Orca's positive stall proof it stops the worker and sets the old Task `failed --result cancelled`" (73). `--retry-of` is never used (69).
- Line 113: workers report progress only through heartbeats and `worker_done`.

## Issue #423 (orchestrator v2) and #339 (v1) scope

- **#423 "[FEATURE] Orchestrator v2 - Proactive Holistic" (OPEN).** Scope is cross-agent knowledge: a catalogue of what all agents across workspaces are doing, refreshed by timers and child-session checkpoint reports, plus regular reviews for duplicate work, shared research, overlapping files and course corrections; suggests cheaper agents "searching sessions or diffing logs and summarizing". Starts with `/sc:brainstorm --depth deep --handoff design` and a `/tech-research` pass; architecture should stay open to non-Claude-Code harnesses. It does not mention liveness, stall or heartbeat explicitly; it names #339 as the v1 prerequisite "covering session supervision, child reporting and session recovery/cleanup".
- **#339 "Orchestrator - To Run and manage ALL sessions within a worktree" (OPEN).** Body line 15: every hour or two run a session sweep to close, resume (timed out, `econnrefused`) or remind the user of needed feedback; line 26: `sc:sweep` — "Sessions go idle and need to be recovered or closed", sweeping the last N hours (default 6) for state, last messages, progress, blockers, next steps. This is the existing scope home for idle/recovery sweeps, at an hourly cadence far coarser than #431 needs.
- **#409 "[FEATURE] TUI Dashboard to Manage Orchestration at Scale" (OPEN)**: title only read. The earlier research `.dev/research/orca-dashboard-20261105/REPORT.md` line 35 notes `worker-list` projections include "liveness observation time/source, evidence freshness"; line 41: keep work status, liveness, observation freshness and message delivery as separate fields, stale source = explicit unknown; line 75: keep "enqueued, delivered, coordinator-processed, human-seen, answered and resolved separate. ... A reply is not proof of resolution"; line 77: collapse heartbeats into last-seen.

## Existing liveness-related code in this repo

None of it touches Orca workers; all of it watches a subprocess the CLI itself launched.

- `src/superclaude/cli/prd/monitor.py:80-112`: NDJSON stdout monitor; every non-empty line updates `last_event_time`; `check_stall(threshold_seconds)` compares monotonic now to it. Config `stall_timeout: int = 120`, `stall_action: str = "warn"` (`src/superclaude/cli/prd/models.py:201-202`). `src/superclaude/cli/prd/process.py:5,10` adds a Popen timeout watchdog (SIGTERM, 5 s, SIGKILL).
- `src/superclaude/cli/cli_portify/monitor.py:84-120`: stall accounting on output growth rate (`stall_threshold_bps` 1.0, `stall_timeout_seconds` 60), accumulating `stall_seconds`; callers decide action.
- `src/superclaude/cli/sprint/diagnostics.py:22,164-218`: failure classifier STALL / timeout / crash from `watchdog_triggered` and `stall_duration > 120`.
- `src/superclaude/cli/eval/pty_stream.py:27,60`: PTY stream stall raises and is treated as a deterministic failure.
- Mtime freshness helpers exist (`src/superclaude/cli/prd/executor.py:282-301`, `prd/inventory.py:52`) but for choosing files, not liveness.
- Claude Code transcripts: `~/.claude/projects/<cwd with / replaced by ->/<session-uuid>.jsonl` (confirmed by `ls`, e.g. `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/*.jsonl`). Entries carry ISO UTC `"timestamp":"2026-11-07T19:05:40.632Z"`; trailing entries can be metadata types without a timestamp (`custom-title`, `agent-name`, `mode`, `permission-mode`, `atis-latch` seen at a file's tail), so a reader must scan back to the last timestamped entry. Orca's `worker-read --source transcript` reads the hook-reported transcript; the guide says never guess a transcript path (`recovery-and-cleanup.md` 71).

## Gaps (what does not exist)

Signals #431 (line 69) proposes, checked against the above:

1. **Progress-bound heartbeats** (step ID, changing counter, deadline): no Orca field; `--phase` is free text and `--payload` raw JSON. No IronClaude convention defines a payload schema.
2. **Read receipt for a reply/send**: none. Only the reader's own `--ack`; Orca states send proves enqueue only. The nearest proof is `terminal send --enter --wait-submit`, which observes submission and turn start — but only for terminal-backed workers and it bypasses the mailbox.
3. **Idle detection with a duration**: `terminal wait --for tui-idle` blocks until idle; no "idle since T" field is documented. Case 2/3 (idle at prompt for hours) is not surfaced unless polled.
4. **Context exhaustion / autocompact thrashing**: no Orca verdict or repo code recognises it; detection would need `worker-read`/`terminal read --screen` text matching ("Autocompact is thrashing"). UNVERIFIED whether `projection.attention` covers it.
5. **Expected-message deadlines**: nothing. WC-10 forbids acting on a late heartbeat; Orca forbids acting on absence.
6. **All-types wait**: Orca supports it (`--types` is only a wake filter), but the guide's canonical filter and this repo's coordinator rules do not list `status`, `handoff`, `merge_ready`, `decision_gate`.
7. **Whole-worktree activity (excluding caches/venvs)** and **last tool call / model turn timestamp**: no tool or repo code; transcript `timestamp` exists but no reader does.
8. **Permission prompt**: Orca has `agentWait` and `worktree ps --agent-wait`, but no repo rule tells the coordinator to poll them on a cadence; the documented trigger is only "after three consecutive empty waits" of up to 15 minutes each.
9. **Policy tension to resolve in design**: Orca and WC-6/WC-10 treat silence as absence that never authorises stop or retry; #431 wants bounded-time action. Nudge or ask are not forbidden by either; stop/retry still need positive stall proof (exited, or transcript final turn without `worker_done`).
