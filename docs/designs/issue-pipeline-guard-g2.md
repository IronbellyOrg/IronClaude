# Issue pipeline guard G2: letting a bound worker ask and be released

**Status:** design note, written 2026-11-17 for Plan B Task 13. No code is changed by this note. Task 14 builds what it chooses.

**This note concerns a security hook.** `src/superclaude/hooks/scripts/launch-level-guard.sh` is a security control. Any change to it (and to its plugin copy `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, which a test requires to be byte-identical) needs its own independent review before it merges, separate from the review of this note.

## 1. Why G2 exists

Under the coordinator handoff (Plan B) the plan-writing worker is started by a coordinator, not launched by the claim script. For the one first test issue the owner accepted that this worker runs without the launch-level guard (G1; recorded in `docs/designs/issue-pipeline-fu1.md`). Before any other issue runs through the flow, the worker must be bound to the guard (G2). Binding a worker exposes two collisions between the guard and the handoff. Both were measured against the live guard on base a98541153.

## 2. The two collisions (live source)

1. **A bound session cannot use the Orca verbs a worker needs.** Any `orca` word is classed ESCAPE (blocked) unless it is one of a short read-only list: `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read` (`launch-level-guard.sh:471-472`) and `orchestration check|inbox|run-current|task-list|worker-show` (`:473`); everything else, `--help` and `-h` aside, adds ESCAPE (`:474`). `orchestration send` (heartbeat, ack, `worker_done`, escalation) and `orchestration ask` are not on the list, so a bound worker could not heartbeat, ask or finish.
2. **The guard lifts its blocks only on a typed user prompt, and route B's approval is not one.** A bound session at the worktree level is released only when the first line of a user prompt, leading whitespace removed, starts `/sc:implement`, `/sc:task` or `/task` as a whole word (`:347-351`); the release is a no-replace create of the session's `.ok` file (`:352-359`), which later reads as level `WA` (`:270-271`). The Plan B source text says the release word is `approved`; the live guard no longer accepts a plain `approved` (it was removed by PR #583), so only the three command forms release. Under the handoff the approval arrives as the result of the worker's own `ask`, so the guard never sees a user prompt and never writes `.ok`.

## 3. How a worker is bound

A worker is bound by the strict launch marker: its first prompt carries `[sc-launch:v1:<32 hex>]` (`:318-319`), and a matching `pending/<nonce>` record exists in the store `~/.claude/state/launch-level/pending/` (`:331-336`). One rename wins the nonce (`:372-376`) and a regular `sessions/<session id>` file appears (`:377-384`). The coordinator creates the `pending` record through the `pending` subcommand Task 15 adds to `orca_worktree.py` (it exposes the existing `publish_pending`), and Task 15 puts the marker line into the brief. A worker whose prompt carries no marker is never bound (`:363-365`). Task 14's hook tests bind their test worker the same way, with a prompt that holds the marker and a pending record written by the test.

## 4. How a coordinator approval releases a bound worker

**Route A: the coordinator writes the worker's `.ok` file.** After the coordinator records the approval row and before it replies to the worker's `ask`, it creates `sessions/<worker session id>.ok` in the store, the file the guard already reads (`:270`). No new release logic is added to the guard. The worker cannot do this itself: a command that names the store path is TAMPER and is blocked for a bound session (`:703`, `LL-TAMPER`). The coordinator's own session is ordinary (not bound), so it can write. **Guard lines changed by route A:** only the `orca` allow-list at `launch-level-guard.sh:471-474` (the `orchestration send` and `ask` entries and the address check of section 5); the release itself changes no guard line, because `:270-271` already read the `.ok` file, and a coordinator-side helper writes it. What route A needs is the worker's session id. How the coordinator learns it is UNVERIFIED: the first live test did not try it (`docs/designs/issue-pipeline-fu1.md`, precondition f).

**Route B: a signed approval file the guard reads.** The coordinator writes a file that carries the issue, the plan hash and a signature, and the guard verifies it before it releases. This adds key handling and a new parsing path inside the security hook, and it still needs the worker's session id to know which session to release. **Guard lines changed by route B:** the same allow-list lines `:471-474` as route A; the release branch `:347-361`, which would gain a case that reads and verifies the signed file instead of (or besides) the `/sc:implement`, `/sc:task` and `/task` first-line test; the level read `:270-271`, which would accept a verified approval as level `WA`; and a new signature-verification block.

**Recommendation: route A**, because it reuses the release the guard already has and adds no new release code to the hook; the only guard change is the allow-list and the address check of section 5. Route B is kept only if the facts below show that a session id cannot be found reliably.

## 5. The address a bound worker may send to

Letting a bound worker run `orchestration send` and `ask` would otherwise let it message another worker or every worker. Orca's own help (`orca orchestration send --help`, 2026-11-17) lists the address forms `run:<id>`, `dispatch:<id>`, a legacy handle and the groups `@all`, `@idle` and `@worktree:<id>`; it says that from an active Dispatch an omitted recipient defaults to the owning Run mailbox, and that `heartbeat` and `worker_done` cannot target groups. `ask` takes only `--to <run:id>`.

**The coordinator-only address rule (Task 14 turns this into tests):** the allow-list admits `orchestration send` and `orchestration ask` for a bound session only when the command has no `--to`, or its `--to` names `run:<id>`; a command with `--to dispatch:<anything>`, `--to @all`, any other group, a legacy handle or any other `--to` value is blocked as ESCAPE. Every other orca word stays blocked.

If the first measurement below shows the guard cannot read the address reliably, Task 14 records the residual risk instead, in one paragraph in this note: a bound worker could message another worker, and the coordinator treats any message it did not ask for as untrusted data.

## 6. Facts to measure before Task 14 chooses

1. How the coordinator can read a worker's session id (the `sessions/<id>` file name, `worker-show`, a transcript or a ccsession file), and that it is the same id the guard uses. UNVERIFIED.
2. That a worker's `orchestration send` and `ask` reach the guard with their full command text, `--to` and `--from` included, so the address can be read at all. UNVERIFIED.
3. That an omitted `--to` really reaches the coordinator's Run mailbox for each verb the worker uses (`heartbeat`, `status` ack, `worker_done`, `escalation`, `ask`). The help text says so; it was not run against a bound worker.
4. That a `.ok` file written by another session changes the bound worker's next `/sc:implement` from blocked to allowed, and that a forged write from the worker's own session is blocked as `LL-TAMPER`.

## 7. What Task 14 adds (tests)

- Hook tests that create the bound worker by the marker path (a prompt holding the marker, a pending record), never a hand-written `sessions/<id>` file.
- One chain test on that worker: bound, `orchestration send` and `ask` allowed, `/sc:implement` blocked, release, `/sc:implement` allowed.
- A bound worker may run `orchestration send` and `ask` to the coordinator address and is still blocked from `git push`, `gh pr create`, `/sc:implement` and every other orca verb.
- Negative tests for the address rule of section 5: `--to dispatch:<other worker>` and `--to @all` are each blocked (or, if the residual risk is recorded instead, a test pins that paragraph).
- A forged release from the worker's own session is blocked as `LL-TAMPER`; all existing launch-level cases and the byte-identity test of the plugin copy keep passing.
