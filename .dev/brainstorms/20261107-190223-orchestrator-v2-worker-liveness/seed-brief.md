---
topic: "Best solution to integrate into orchestrator v2 (IronbellyOrg/IronClaude issue #423; v1 is #339) for GitHub issue #431 'Orchestrator waits on workers that went quiet because its alive check relies on weak signals'. Inputs: .dev/issues/431/issue-body.md and .dev/issues/431/description.md (8 observed cases, candidate stronger signals). Design how a coordinator reliably detects a stalled, idle, blocked, context-exhausted or unreachable worker, confirms an answer was read, covers every message type, and what it then does (nudge, ask, restart with a resume note, report). Consider progress-bound heartbeats, whole-worktree activity, terminal state classification (working, idle at prompt, permission prompt, compact thrashing), session transcript timestamps, per-step deadlines, wait filters covering all types, read-acknowledgement of replies, and worker-side fixes (do not end a turn between chain steps; context-safe chunked reads and per-stage handoff files). Keep the architecture portable to other harnesses; follow docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md and src/superclaude/core/WORKER-CONTRACT.md. Say what can be fixed in the v1 contract now versus what belongs in v2. Design only: no implementation, no source edits, no commits, no GitHub writes."
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-11-07T19:02:23Z
---

# Seed Brief: orchestrator-v2-worker-liveness

Dialogue mode: non-interactive (no `--interactive`); the deep question bank (architecture domain, 20 questions in Clarify, Validate and Probe batches) was answered from `.dev/issues/431/issue-body.md`, `.dev/issues/431/description.md` and `src/superclaude/core/WORKER-CONTRACT.md` (read 2026-11-07). Answers that the sources do not settle are listed under Open Questions.

## Problem Statement

An Orca coordinator running several IronClaude workers decides a worker is "alive" from weak signals: timer heartbeats whose status never changes, one file's mtime, a helper agent name on screen, or no failure message. In run `run_93bfa00cae2b` (2026-11-07, six workers) this cost about four hours twice (#339 context-exhausted with autocompact thrashing; #339 replacement idle at its prompt), plus a closing report sent as `status` that the wait filter ignored for about four hours (#361), mailbox answers not seen for 35-40 minutes (#331, #375), a permission prompt unnoticed for about 20 minutes (#394), and workers ending their turn between chain steps (#339, #331). The design must give the coordinator bounded-time detection of each failure state and a defined response, and must feed orchestrator v2 (#423).

## Known Context

- The v1 contract states the dispatch preamble is the authority for heartbeat cadence and verb syntax and is never copied (`WORKER-CONTRACT.md:7`).
- WC-10 (`WORKER-CONTRACT.md:44`): a missing heartbeat is treated as absence, never death; the coordinator never stops, retries or releases a worker because a heartbeat is late and acts only on "Orca's stall proofs". Agent-tool fan-out may hold a session past the cadence with no heartbeat; that gap is accepted.
- WC-3 and the Heartbeats bullet (`:56`, `:61`): no heartbeat while blocked in `ask` or `check --wait`; on `ask` timeout the worker resumes the same message ID.
- WC-12 (`:59`): coordinator follow-ups are pulled with `check` at checkpoints and before `worker_done`; never pushed.
- WC-6 (`:69-74`): every retry is a new Task; after Orca's positive stall proof the coordinator stops the worker and marks the old Task `failed --result cancelled`. Absence never authorizes a retry.
- WC-7 (`:58`): lifecycle messages come only from the top-level worker session; commands contain no Orca calls (`:5`, WC-8).
- The coordinator reads disk (`report_path`, contract) after `worker_done` (`:37`, `:88`).
- Observed failure states: context exhausted / compact thrashing; idle at prompt after a turn ended; blocked on a permission prompt; reply delivered to mailbox but not read; closing message of an unexpected type; quiet between chain steps.
- Mitigations already applied in the run: wait filter widened; terminal nudges typed; one session cleared and restarted from on-disk files with a "read in small pieces" note.

## Constraints

- Design only: no source edits, commits, pushes, PRs or GitHub comments; outputs only under this brainstorm directory.
- Portable: the core liveness model must not depend on Claude Code internals alone; harness-specific probes (screen text, transcript files) are adapters behind a common state model.
- Must respect the v1 contract: commands contain no Orca calls (WC-8), lifecycle messages only from the top-level session (WC-7), retries are new Tasks (WC-6), preamble owns cadence and syntax (`:7`).
- WC-10's "absence is not death" rule must stay safe: any new rule that lets the coordinator act on silence must act by probing or nudging first, never by killing on silence alone.
- Low false-positive cost: a nudge into a working session must be harmless; a restart must preserve on-disk progress.
- GitHub target only `IronbellyOrg/IronClaude`; no Orca `--issue`/`--pr` link flags.

## Success Criteria

- Each of the 8 observed cases maps to a named state that is detected within a stated bound (target: 15 minutes or less for idle, blocked and thrashing; one wait cycle for missed message types).
- A coordinator wait never filters out a worker message type; any unknown type is surfaced.
- A reply is confirmed read by an explicit worker acknowledgement; an unacknowledged reply escalates to a terminal-typed copy within a stated bound.
- Each detected state has one defined response from a fixed ladder (probe, nudge, ask, restart with resume note, report to person), with a cap on repeats.
- The design separates changes that fit the v1 contract text now from changes that need v2 machinery (#423), and lists each WC rule it amends.
- The core model is harness-neutral, with Claude Code and Orca as the first adapters.

## Open Questions

- Which liveness signals Orca already exposes (terminal state, stall proof, read receipts, idle detection) and which must be built: to be checked in enrichment.
- Should heartbeats move from timer-driven to progress-bound (step id plus changing counter), given that commands may not call Orca (WC-8) and the session may be inside a long tool call?
- Can a worker reliably acknowledge a reply, and why were mailbox replies not seen in cases 5 (cause not established)?
- Is screen-text classification acceptable as a primary signal, or only as a confirming probe, given its brittleness across harness versions?
- Does the "do not end a turn between chain steps" rule belong in the worker contract, the preamble, or each chain-running command?
- What restart budget and resume-note format avoid restart loops when the cause (for example context exhaustion) recurs, as in case 8?
- How should WC-10 be amended so silence past a deadline triggers a probe without contradicting "never act on absence"?

## Enrichment Context

Full artifacts: `enrichment/codebase-context.md` (quality tier primary for Orca `--help` and guide on binary `1.4.245-aidev02`, repo Grep/Read and read-only `gh issue view --repo IronbellyOrg/IronClaude`; codegraph and auggie not used) and `enrichment/research-light.md` (quality tier fallback_1: 12 WebSearch queries plus 3 full page reads, because the research skill was unavailable). Neither ran a live Orca worker; runtime behaviour is documented, not observed.

### What Orca already provides (documented; IronClaude rules do not poll it today)

- Message types (`orca orchestration send --help`): `status, dispatch, worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat`. Heartbeat fields: free-text `--phase`, `--task-id`, `--dispatch-id`, raw `--payload <json>`. No step ID, counter or deadline field.
- `check --types` is only the wake condition for `--wait`; a returned delivery is the whole FIFO batch, never filtered. A narrow filter delays a message rather than losing it. The Orca guide's canonical coordinator filter `worker_done,escalation,question` (15-minute timeout) omits `status`, `handoff`, `merge_ready`, `decision_gate`: the mechanism of case 4.
- No sender-side read receipt. Orca's `references/messaging-and-gates.md` lines 6-7: send proves durable enqueue; wake and nudge prove neither that the recipient read the message nor that it began a turn. `check --ack` is the reader acknowledging its own batch. The only verb with an observed turn-start receipt is `orca terminal send --text --enter --wait-submit`, and only for terminal-backed workers.
- Liveness verdicts: `worker-list` `projection.liveness` (`live` / `unverifiable` / `exited`, with reasons), `projection.attention.categories`, `requiresAction` and a literal `nextAction` argv. The set of attention category values is undocumented (UNVERIFIED whether any covers thrashing). The guide warns that a live terminal can still hold a dead or stuck agent.
- Blocked on a person-only prompt: `worker-show` `observation.agentWait` (evidence: hook, prompt text or title; null = looked and none; absent = never looked) and `orca worktree ps --agent-wait`. "A waiting worker is healthy, not failed." Covers case 6 if polled.
- Idle and screen: `orca terminal wait --for tui-idle`, `orca terminal read --screen`, `orchestration worker-read --source auto|transcript|terminal`. No "idle since" timestamp.
- Stall proof (Orca `recovery-and-cleanup.md`): only `exited` liveness, the worker's own process-exit observation, or a transcript whose final agent turn sent no `worker_done`. Everything else is absence; absence never authorizes stop, retry or release. Nudge and ask are not forbidden. The guide's only sweep trigger is "after three consecutive empty waits" (up to 45 minutes).

### What does not exist anywhere (gaps)

Progress-bound heartbeat schema; idle duration; context-exhaustion or autocompact-thrashing detection; expected-message deadlines; whole-worktree activity; a last-tool-call or last-model-turn timestamp reader; a rule telling the coordinator to poll `agentWait` or `worker-list` on a cadence; an all-types wait in IronClaude coordinator rules. Repo stall code (`src/superclaude/cli/prd/monitor.py`, `cli_portify/monitor.py`, `sprint/diagnostics.py`, `eval/pty_stream.py`) watches only subprocesses the CLI starts itself. Claude Code transcripts live at `~/.claude/projects/<cwd with "/" replaced by "-">/<uuid>.jsonl` with ISO UTC `timestamp` fields (trailing metadata entries lack timestamps); Orca's guide says never guess a transcript path and to use `worker-read --source transcript`.

### Contract facts that shape the design

- WC-12 (`WORKER-CONTRACT.md:59`): follow-ups are pulled at checkpoints. A mailbox reply reaches an idle-at-prompt worker only when it next runs `check`, which an idle worker never does: a probable mechanism for case 5 (UNVERIFIED as the cause).
- WC-10 (`:44`) and WC-6 (`:69-74`) match Orca's stall-proof rule: stop and retry need positive proof; bounded-time probing, nudging and asking are not forbidden by either.
- Scope homes: #423 (v2) is cross-agent knowledge sharing and does not mention liveness; it names #339 as the prerequisite for session supervision, child reporting and session recovery/cleanup. #339 scopes an hourly `sc:sweep` for idle sessions, far coarser than this need. The #409 dashboard research (`.dev/research/orca-dashboard-20261105/REPORT.md`) recommends separate fields for work status, liveness, observation freshness and message delivery, and keeping "enqueued, delivered, processed, seen, answered, resolved" separate.

### Prior art (research-light; URLs in the artifact)

- Temporal: heartbeats carry progress details plus a heartbeat timeout; the heartbeat is also the cancellation channel; resume reads the last details and expects the interrupted step to repeat.
- Kubernetes: liveness (making progress) vs readiness (can take work, never restarted on failure) vs startup (grace period). Mapping: timer heartbeat is a process-exists signal; idle-at-prompt is "ready, not progressing"; resume is "startup".
- Erlang/OTP: restart intensity MaxR in MaxT, then escalate. SQS: dead-letter after repeated failure; visibility extension as a progress heartbeat; consumers must be idempotent.
- MQTT QoS 1: the sender keeps a message until acknowledged; a mailbox delivery is a broker ack, not a reader ack.
- Claude Code hooks: `Notification` with `permission_prompt`, `idle_prompt`, `agent_needs_input`; `Stop` (once per turn, exit 2 keeps working); `PreCompact` (`auto`); `SessionStart` source `resume|clear|compact`. One report says `Notification` did not fire in the VS Code extension. `idle_prompt` timing UNVERIFIED.
- OpenHands StuckDetector: repeated-pattern detection over recent events, one corrective nudge before declaring stuck; early thresholds produced false positives. SWE-agent: context exhaustion is a named exit status (`exit_context`), saving the patch first. LangGraph and AutoGen: checkpoint at step boundaries; termination conditions combine with OR.
