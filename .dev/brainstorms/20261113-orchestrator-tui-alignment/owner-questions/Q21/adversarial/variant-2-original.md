# Proposal B: yes, in Phase 2, reading Orca's agent rows, and only after FU-1 shows what they hold

## Answer

Yes. In Phase 2 of the sweep, the sweep may label a session as machine-started by reading Orca's `worktree ps` agent rows (the `prompt` and `paneKey` fields), but only in the exact shape that the watcher's first live test (FU-1) records, and only with commands already on the owner-signed allow-list.

## What happens next if the owner picks it

1. The follow-up table in issue #534 (work item SW-06) gets a row "machine-started label" with an owner and a trigger "after FU-1".
2. FU-1 (work item WA-04) runs when its own questions are answered and records item (e): one `worktree ps --json` agent row after a real launch, whether `prompt` holds `/sc:issue --claim N`, and whether `paneKey` equals a tab-map name (merged-requirements.md line 306). That record settles open item D-B.
3. When FU-1 is recorded and PR #539 has merged, SW-10 starts in wave W4: a supervised worker adds the label from the recorded shape, with a test built from the FU-1 fixture showing a watcher-launched session is not labelled person-started. If the recorded shape gives no usable signal, SW-10 records "no reliable signal" and stops; the label is not guessed.
4. The PR session opens the PR with `/sc:pr-submit --monitor 3` under its own permission row.

## What it unlocks

- SW-10 and, through it, one of the gates of the later watcher handoff WA-07 (dependency row 74).
- Readers of the sweep can tell a watcher's session from a person's session, which matters because the worker contract says person-started sessions are never messaged (WC-16) and the later course-correction design treats the two classes differently (ADJ line 714).
- No widening of the allow-list: `worktree ps --json` is already one of the sweep's ten allowed Orca command templates (`src/superclaude/cli/sweep/probes.py:55`); SW-10 item (4) forbids any new verb without a new owner signature.

## What it costs or risks

- The label depends on Orca's free-form fields. On 27 live rows `prompt` was empty or not a slash command (ADJ line 162); one FU-1 row may not represent every launch, and a later Orca build can change these fields (A-009, two builds of Orca 1.4.245 on record).
- Waits on FU-1, which itself waits on Q2 (claim level and permission acceptance) and Q20 (who owns the watcher's agent). If those stay unanswered, SW-10 never starts.
- A false negative (a watcher session still shown as a person's) stays possible; the direction of that error is the safer one, because person sessions are never messaged.

## What stays unresolved

- Whether `prompt` or `paneKey` actually carries a usable signal (D-B), until FU-1.
- Whether `agent launch` creates a Run (D-A); if it does, the session might be visible as a worker and need no label at all.
