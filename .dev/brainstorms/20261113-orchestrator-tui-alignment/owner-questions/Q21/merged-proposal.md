<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->
<!-- Plan: adversarial/refactor-plan.md (4 changes planned; Variant 1: 1 change, Variant 3: 3 changes) -->
<!-- Executor: merge-executor -->

# Proposal B: yes, in Phase 2, reading Orca's agent rows, and only after FU-1 shows what they hold

<!-- Source: Base (Variant 2), unchanged -->
## Answer

Yes. In Phase 2 of the sweep, the sweep may label a session as machine-started by reading Orca's `worktree ps` agent rows (the `prompt` and `paneKey` fields), but only in the exact shape that the watcher's first live test (FU-1) records, and only with commands already on the owner-signed allow-list.

<!-- Source: Base (Variant 2); step 1 extended by Change 2 (Variant 3); step 3 extended by Change 3 (Variant 3) and Change 1 (Variant 1) -->
## What happens next if the owner picks it

<!-- Source: Base (Variant 2) + Change 2 (Variant 3, step 2): blind-spot sentence appended -->
1. The follow-up table in issue #534 (work item SW-06) gets a row "machine-started label" with an owner and a trigger "after FU-1". Until SW-10 lands, the sweep design and the contract-note draft (XC-05) say that a Run-less session may have been started by the watcher and the sweep cannot tell (ADJ lines 227, 242).
<!-- Source: Base (Variant 2), unchanged -->
2. FU-1 (work item WA-04) runs when its own questions are answered and records item (e): one `worktree ps --json` agent row after a real launch, whether `prompt` holds `/sc:issue --claim N`, and whether `paneKey` equals a tab-map name (merged-requirements.md line 306). That record settles open item D-B.
<!-- Source: Base (Variant 2) + Change 3 (Variant 3, round1-advocate-V3.md Weaknesses 1 and 2) + Change 1 (Variant 1, Answer; round1-advocate-V1.md Strength 1 and Concession 1) -->
3. When FU-1 is recorded and PR #539 has merged, SW-10 starts in wave W4: a supervised worker adds the label from the recorded shape, with a test built from the FU-1 fixture showing a watcher-launched session is not labelled person-started. The label may only move a row from "unknown" to "machine-started"; a row whose signal is missing or unrecognised stays "could not determine", never person-started. The fixture test also covers an empty `prompt`. If the recorded shape gives no usable signal, SW-10 records "no reliable signal" and stops; the label is not guessed. In that case the reopen option is a label from the watcher's versioned store `dispatch.json` (`operation_id`, `launch_cwd`, checked `schema_version`: `record.py:69-95`), which would need its own owner approval of a file read. It is not the watcher's `status --json`, which lacks the launched sessions' ids (`cycle.py:1308-1323`), and there is no worktree-path fallback.
<!-- Source: Base (Variant 2), unchanged -->
4. The PR session opens the PR with `/sc:pr-submit --monitor 3` under its own permission row.

<!-- Source: Base (Variant 2); last bullet added by Change 4 (Variant 3) -->
## What it unlocks

- SW-10 and, through it, one of the gates of the later watcher handoff WA-07 (dependency row 74).
- Readers of the sweep can tell a watcher's session from a person's session, which matters because the worker contract says person-started sessions are never messaged (WC-16) and the later course-correction design treats the two classes differently (ADJ line 714).
- No widening of the allow-list: `worktree ps --json` is already one of the sweep's ten allowed Orca command templates (`src/superclaude/cli/sweep/probes.py:55`); SW-10 item (4) forbids any new verb without a new owner signature.
<!-- Source: Change 4 (Variant 3, round1-advocate-V3.md Concession 1; route wording from Variant 3 step 4) -->
- If SW-10 ends in "no reliable signal", WA-07 item (3) uses its other route ("bound to a Run", merged-requirements.md line 309); the dependency row is updated then.

<!-- Source: Base (Variant 2), unchanged -->
## What it costs or risks

- The label depends on Orca's free-form fields. On 27 live rows `prompt` was empty or not a slash command (ADJ line 162); one FU-1 row may not represent every launch, and a later Orca build can change these fields (A-009, two builds of Orca 1.4.245 on record).
- Waits on FU-1, which itself waits on Q2 (claim level and permission acceptance) and Q20 (who owns the watcher's agent). If those stay unanswered, SW-10 never starts.
- A false negative (a watcher session still shown as a person's) stays possible; the direction of that error is the safer one, because person sessions are never messaged.

<!-- Source: Base (Variant 2); last bullet added by Change 1 (Variant 1) -->
## What stays unresolved

- Whether `prompt` or `paneKey` actually carries a usable signal (D-B), until FU-1.
- Whether `agent launch` creates a Run (D-A); if it does, the session might be visible as a worker and need no label at all.
<!-- Source: Change 1 (Variant 1, Answer; round1-advocate-V1.md Strength 1 and Concession 1) -->
- If FU-1 shows no usable signal: whether the owner approves the sweep reading the watcher's `dispatch.json` (step 3), which is a separate owner approval of a file read and is not given by this answer.
