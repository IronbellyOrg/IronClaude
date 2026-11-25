# Early probe result (issue 442, X10 step 2), 2026-11-22

Owner go: "442 - run probe" (chat, 2026-11-22 12:18 UTC). One real worker, started with `orca-ide orchestration worker-start` into the existing worktree of disposable issue 712 (/home/coder/workspaces/worktrees/IronClaude/issue-712), level worktree, cap 1. Nothing merged, nothing pushed, `WORKER_BINDING_PROVEN` not touched (the constant does not exist on master).

Versions: Claude Code 2.1.330; sha256 (first 12): guard e6fc1470ae82, orca_worktree.py 155ec28960fe, launch-prompt.md 5960e7ceb61d, WORKER-CONTRACT f0b85e7fec01. Files in this folder: ledger.md, pending-out.json, prompt.txt, worker-start-reply.json (the real reply shape), worker-read-1.json, worker-read-final.json, first-user-prompt.txt (the full first message the worker received), worker-stop.json.

## Rows

| Row | Result | Evidence |
|---|---|---|
| R1 marker arrives intact | PASS, with one plan difference | The marker `[sc-launch:v1:<32 hex>]` is in the worker's first message, byte 6036 of 6515 (first-user-prompt.txt). Orca wraps the `--spec` text after its own roughly 6 KB brief, so the marker can never be at position 0 through `worker-start`. The guard accepts a strict marker anywhere in the prompt (launch-level-guard.sh lines 320 to 324, comment "B6: strict marker anywhere"), so binding still works. The worker copied the marker back correctly. The plan's "marker first" wording should be dropped for this route. |
| R2 pending record consumed | PASS (seconds not measured) | pending/<nonce> existed after `orca_worktree.py pending` (12:20:0x), was gone at 12:21:02, 49 s after worker-start (12:20:13). The session record sessions/ae728c49-a2f3-4257-bf6b-13e48f70e37f holds the word `worktree`, written 12:20. Exact seconds and the inode match were not recorded. |
| Guard active in the worker | PASS (side finding) | The worker's own `ls ~/.claude/state/launch-level/pending` was refused by the guard ("this session was started by /sc:issue --claim at level worktree ... Blocked: touching the launch-level state"). So even a read of the state folder is blocked; my probe prompt step 2 could not be done by the worker. |
| worker-start reply shape | Saved | state ready, stage input_accepted, turnStart observed, mode terminal, effects worktree reused, terminal created (background; Orca warned it could not make it discoverable). |

Not run (not part of the early probe): R3 to R9 (release, commit/push/merge blocks, no-marker control, kill and resume, send and ask, limits, hashes of final code).

## Settlement and state
- The worker did not send `worker_done` (the probe prompt did not ask for it). I stopped it with `worker-stop` (state stopped, terminal closed). Dispatch ctx_5f78a1f4eb2c, task task_933b8d9447c6.
- The guard session record for the stopped worker stays in ~/.claude/state/launch-level/sessions/ (harmless; the person may remove it).
- Disposable issues 713, 714 and 715 are unused; 712 has had one probe worker.

## What this does and does not show
It shows the coordinator route (worker-start with the marker inside the spec) binds a worker to the guard on today's installed files. It does not prove the commit, push and merge blocks, the release step, resume behaviour, or anything about stage S14 code (not built). Per the X10 plan these need the final probe on merged S14 code and a second agent re-reading the raw rows before any flip.
