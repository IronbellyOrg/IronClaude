# Description given to /sc:issue --create

User's words (exact):

"Orchestrator waiting on workers that had gone quiet due to alive check relying on weak signals" Fill in the rest of a issue description with the context of this recent issue and then spin up a new session on this branch to run sc:brainstorm to think through the best solution that could be integrated into v2 of our new orchestrator

## Context to put in the issue (observed by the coordinator session on 2026-11-07, run run_93bfa00cae2b, six parallel workers)

The coordinator treated a worker as "alive" from weak signals and so kept waiting on workers that were not making progress. Each case below was found late, by chance or by the coordinator reading the worker's screen.

1. Issue 339 worker, first session (stuck about 07:49 to 11:33, roughly 4 hours). Its context window was full and the screen said "Autocompact is thrashing: the context refilled to the limit within 3 turns of the previous compact, 3 times in a row". Its "implementing" heartbeats kept arriving every few minutes because they came from a timer, not from progress. The coordinator saw "heartbeat received" and kept waiting. Found at 11:33 by reading the terminal screen.
2. Issue 339 worker, replacement session (idle about 12:08 to 16:07, roughly 4 hours). It finished a turn, stopped, and sat at an input prompt. No heartbeat, no message, last file change 12:07. Found at 16:07. A nudge typed into its terminal restarted it. It stopped again between 17:00 and 18:00 and needed a second nudge.
3. Issue 331 worker (silent from 17:10, last file change 18:17, found idle 18:38). The coordinator judged it "alive" at 18:19 because one QA file had been written two minutes earlier. That one file was the last output before it went idle.
4. Closing reports missed. The issue 361 worker finished at 08:22 and sent its closing report as a message of type "status", but the coordinator's wait only listened for the types worker_done, escalation and question. The report sat unread for about 4 hours. The wait filter was widened afterwards.
5. Replies not seen by workers. The coordinator answered two worker questions (issue 331 Gate 3, issue 375 task 1 decision) with the mailbox reply command. Both workers kept waiting 35 to 40 minutes ("ask unanswered 40 min") until the same answer was typed into their terminals. Cause not established.
6. A worker blocked on a permission prompt for up to about 20 minutes (issue 394: "This shell script runs rm and could not be checked. Do you want to proceed?"). No message was sent about it. Found only by reading the screen.
7. Workers stop between chain steps without sending a message (issues 339, 331), so quiet is ambiguous: it can mean "working on a long step" or "ended its turn and is idle".

## Weak signals the coordinator relied on
- Timer heartbeats that say "implementing" and do not change.
- The mtime of a single file.
- A helper agent name visible on the screen.
- The absence of a failure message.

## Stronger signals to evaluate (not decided)
- Progress-bound heartbeats that carry a step id and a changing counter, and a deadline for the next one.
- Activity across the whole worktree (git and file changes, excluding caches and virtualenvs), not one file.
- The worker's terminal state: working, idle at a prompt, permission prompt, context full or compact failing.
- The session transcript: time of the last tool call or model turn.
- Expected-message deadlines per step, so silence past the deadline triggers a check or nudge.
- Message-type coverage: the wait must cover every type a worker can send, including closing reports.
- Confirming that an answer was read (an acknowledgement from the worker), not only that it was sent.

## Request
File this as an issue. Then start a new session on the current branch (docs/409-orca-dashboard-designs, main checkout) to run /sc:brainstorm on the best solution, so it can be integrated into the v2 orchestrator (see #423, "Orchestrator v2 - Proactive Holistic", and the v1 orchestrator #339). The brainstorm must stay design-only: no implementation.

Flags given: none (mode, type and depth are chosen by the workers; depth quick).
