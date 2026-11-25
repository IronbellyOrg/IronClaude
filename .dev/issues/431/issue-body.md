<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Bug Summary

The orchestrator waits on workers that have gone quiet because its alive check relies on weak signals. In the observed run, stalled, idle or blocked workers and missed messages went unnoticed for extended periods.

## Environment (OS, version)

- OS: Linux 6.8.0
- Version: branch `docs/409-orca-dashboard-designs`; run `run_93bfa00cae2b`; 2026-11-07.

## Current Behavior

In a run with six parallel workers, the coordinator relied on timer heartbeats with an unchanged “implementing” status, one file's mtime, a helper agent name visible on screen, or the absence of a failure message. Cases were found late, by chance or by reading the worker's screen:

1. Issue #339's first session was stuck about 07:49–11:33, roughly four hours, with a full context window and thrashing autocompact. Timer-based “implementing” heartbeats continued every few minutes; the coordinator kept waiting until a screen read at 11:33.
2. Issue #339's replacement was idle about 12:08–16:07, roughly four hours, at an input prompt after finishing a turn, with no heartbeat or message and a last file change at 12:07. A terminal nudge restarted it; it stopped again between 17:00 and 18:00 and needed another nudge.
3. Issue #331's worker was silent from 17:10; its last file change was 18:17. At 18:19 the coordinator judged it alive based on that file, but found it idle at 18:38.
4. Issue #361's worker finished at 08:22 and sent its closing report as `status`; the wait listened only for `worker_done`, `escalation` and `question`. The report remained unread about four hours; the filter was widened afterwards.
5. Answers to two worker questions (#331 Gate 3 and #375 task 1 decision) were sent by mailbox reply, but the workers waited 35–40 minutes until the same answers were typed into their terminals. The cause is not established.
6. Issue #394's worker was blocked on a permission prompt for up to about 20 minutes, without sending a message; it was found by reading the screen.
7. Workers on #339 and #331 stopped between chain steps without a message. Silence could mean a long step was in progress or that a turn had ended and the worker was idle.
8. Issue #339's replacement worker hit the same "Autocompact is thrashing" failure again at 18:11 and sat stuck until 18:57 (about 46 minutes) before a sweep found it. The coordinator's earlier "alive" check at 18:19 had missed it. The session was cleared and restarted from the files on disk with a note to read reports in small pieces.

## Expected Behavior

The coordinator detects a stalled, idle, blocked or unreachable worker within a bounded time and acts by nudging, asking, restarting or reporting, using stronger signals. Closing reports of every message type are seen, and an answer is confirmed read rather than merely sent.

## Steps to Reproduce

1. Run a long worker chain until its context window is full, or a worker ends its turn between steps.
2. Wait using a filter that listens to only some message types, or send an answer by mailbox only.
3. Observe whether the coordinator keeps waiting or the worker fails to see the answer. Exact reproduction: Not known yet.

## Impact Assessment (Severity, Blast Radius)

- Severity: high — hours were lost, including roughly four hours in two cases.
- Blast Radius: every supervised worker run.

## Error Messages

```text
Autocompact is thrashing: the context refilled to the limit within 3 turns of the previous compact, 3 times in a row
This shell script runs rm and could not be checked. Do you want to proceed?
ask unanswered 40 min
```

## Codebase Context (from `/sc:analyze`)

- `src/superclaude/core/WORKER-CONTRACT.md:5-7` describes a top-level worker reporting with `worker_done` and makes the dispatch preamble authoritative for heartbeat cadence.
- `src/superclaude/core/WORKER-CONTRACT.md:56-61` says heartbeats are not sent while blocked in `ask` or `check --wait`; workers pull follow-ups at checkpoints and before `worker_done`.
- `src/superclaude/core/WORKER-CONTRACT.md:88` says the coordinator opens the contract after `worker_done`.
- `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:972-981` describes coordinator and worker roles and identifies the orchestration skill as a discovery stub.
- `~/.claude/skills/orchestration/SKILL.md:20-27` describes supervised coordination, heartbeats and message waits.
- Quick static analysis used Grep and Read because codegraph and auggie tools were unavailable; no runtime reproduction was performed.

## Related Issues

- #423 — orchestrator v2; the design is intended to feed this work.
- #339 — v1 orchestrator and the affected worker in two observed cases.
- #409 — TUI dashboard for managing orchestration at scale; possibly related.
- #331 — task watcher and routing service; its worker appeared in observed cases.
- #394 — launch-level enforcement; its worker encountered the observed permission prompt.
- #315 — closed issue about a launch-time session-name prompt, a different cause.
- #412 — closed issue about choosing the wrong session launch action; possibly related, but a different launch-time cause, not a demonstrated prompt.

## Testing Notes

A design-only `/sc:brainstorm` session should evaluate progress-bound heartbeats with step IDs, changing counters and deadlines; whole-worktree activity excluding caches and virtualenvs; terminal states; transcript timestamps for last tool call or model turn; expected-message deadlines; coverage of all message types; and acknowledgement that answers were read. Its result should feed orchestrator v2 (#423). This issue requests design first, not implementation; exact verification procedure: Not known yet.

<!-- sc:issue:create template=issue-bug-simple -->
