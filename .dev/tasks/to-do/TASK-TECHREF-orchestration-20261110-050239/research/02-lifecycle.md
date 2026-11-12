# Research 02: Coordinator lifecycle, monitoring, retries and messages

**Topic:** Coordinator lifecycle, monitoring, retries and messages in `src/superclaude/core/WORKER-CONTRACT.md` section 4
**Investigation type:** Code tracer (normative contract text traced to implementing code/tests where they exist)
**Scope:** `src/superclaude/core/WORKER-CONTRACT.md` section 4 (lines 67-282) plus the section 1-3 rules it cites (WC-3, WC-5, WC-9, WC-10, WC-11, WC-12, WC-13); tests under `tests/skills/test_worker_contract.py`; hooks that touch the lifecycle.
**Date:** 2026-11-11
**Status:** Complete

Evidence classes used below: NORMATIVE (instruction text in the contract; not proof of execution), CHECKOUT-SOURCE (code or tests in this worktree), ORCA-CHECKOUT (the Orca development checkout `/home/coder/workspaces/IronOrca`, branch `main`, commit `dc57b3d6e81c9825446a520bf0aee8600a2f5586`, version 1.4.214 at `package.json:3`), ORCA-INSTALLED-FILES (read-only reads of the installed build files under `/opt/Orca/resources/app.asar.unpacked/out/`; compiled-output metadata `out/package.json` says version `1.4.245-aidev02.9cfecdd30b2a`, commit `9cfecdd30b2a90c06e5178b1245cb31a97d11bac`; file contents are not the running process), HISTORICAL (earlier reports), UNVERIFIED-DEPLOYED (the running Orca build, its stored settings, other hosts). Subordinate/sub-orchestrator mode is deferred and not implemented.

Provenance of the two Orca sources (added in fix cycle 1, read-only `git` in `/home/coder/workspaces/IronOrca`): the installed build's recorded commit `9cfecdd30b2a...` exists in that repository on `remotes/origin/aidev02`, the checkout HEAD `dc57b3d6e` is an ancestor of it, and `git rev-list --count dc57b3d6e..9cfecdd30b2a...` printed 1048. So the checkout is an older snapshot of the same repository, not the installed build, and a checkout-only fact is not a statement about the installed files (and neither is a statement about the running process). Every Orca claim below carries its source: checkout, installed files, or both.

---

## 1. Source: `src/superclaude/core/WORKER-CONTRACT.md` (structure and evidence class)

Evidence class: NORMATIVE. Every coordinator duty below is an instruction to an LLM session. No code in this checkout executes the coordinator loop (see section 6).

- File is 327 lines (`wc -l`), last touched in commit `6782eee10` (2026-11-07). The research notes (`research-notes.md:9`) say 273 lines: [CODE-CONTRADICTED] stale count; section 4 now spans `WORKER-CONTRACT.md:67-282`, section 5 (brief template) starts `:283`.
- Installed copy `~/.claude/WORKER-CONTRACT.md` is byte-identical to the checkout file at the time of this run (`diff -q` printed nothing). This is file parity only; it says nothing about what a running coordinator session has loaded. The packaged copy at `.venv/lib/python3.11/site-packages/superclaude/_src/superclaude/core/WORKER-CONTRACT.md` is 210 lines and differs: stale venv build, not used by this run.
- Section 4 map (all line numbers re-read in this run):

| Lines | Heading | Content |
|---|---|---|
| 67-69 | `## 4. Coordinator rules` | Coordinator = "an Orca coordinator session the person opened" |
| 71-79 | `### WC-6. Every retry is a new Task` | No `--retry-of`; new Task per retry; settlement rules |
| 81-93 | `### What the coordinator owes each worker` | Seven brief contents |
| 95-200 | `### Liveness supervision` | Wait command, sweep, deadline W, S0-S11 table, ack timeline A1-A4, ladder L0-L5, restart budget, nudge text, resume note, never-on-silence, 5 UNVERIFIED points |
| 202-216 | `### Brief layout` | Guard line, Chain line, `--unattended` decision test |
| 218-225 | `### Feature worktree and child worktrees` | Orca-only worktrees, `--setup skip`, placement map, merge-back |
| 227-235 | `### Git and GitHub ownership` | Coordinator owns all outward actions |
| 237-246 | `### Reading a result before anything depends on it` | succeeded/partial/failed/blocked handling, guard refusals, `--deps` timing |
| 248-269 | `### After an /sc:implement stop (decision D2)` | Freeze, lift, 7-condition resume check, placement |
| 271-273 | `### Fan-in rule` | N inputs, at most 10, at least 2 admitted |
| 275-281 | `### Worked example` | Gate hit, answer, new Task (tdd) |

Lifecycle as the contract defines it (normative; each step is a coordinator instruction, not a code path):
1. Plan and create Tasks (`task-create --spec`), one brief per Task, report dir unique per Task (`:83-91`, template at `:283+`).
2. Start the worker with `worker-start` (never `--retry-of`, `:73`); the worker sends heartbeats, `status`, `question`, `escalation`, `handoff`, `worker_done` (`:101`, `:108`).
3. Wait with `orca orchestration check --wait --types <9 types> --timeout-ms 300000` (`:101`); handle the whole batch, write one run-notes line per message ID, then `--ack` (`:104`).
4. Sweep at most every 5 minutes (`:110`) and drive the S0-S11 state table (`:116-129`) through the L0-L5 ladder (`:148-155`).
5. On `worker_done`, open the contract, then admit or reject per `worker_status` (`:93`, `:239-246`).
6. Retry only as a new Task, only after the old attempt is settled (`:73-79`); L4 restart carries a resume note (`:167-180`).
7. Merge children, stage `.dev/tasks`, commit and publish only on the person's instruction (`:220-235`).

Subordinate/sub-orchestrator mode: not present in section 4. `:69` says the coordinator is person-opened, `:62` (WC-13) forbids the worker from starting Orca work. Not presented as shipped.

## 2. Retries: WC-6 (`WORKER-CONTRACT.md:71-79`) traced against the Orca development checkout

Evidence class: NORMATIVE rule; its premises about Orca are checked against the Orca development checkout `/home/coder/workspaces/IronOrca/src/` (ORCA-CHECKOUT, a different repository; not the installed build). In fix cycle 1 each row was also re-checked against the installed build files (ORCA-INSTALLED-FILES, see the table after the rule list below). A row tagged "(dev checkout)" is verified for the checkout only; the installed-file result is stated in the re-check table; the running build stays UNVERIFIED-DEPLOYED.

| Contract claim | Where stated | Orca dev-checkout evidence | Tag |
|---|---|---|---|
| "`task-update` changes only `--status` and `--result`" (brief cannot change after creation) | `:73` | `IronOrca/src/cli/specs/orchestration.ts:166-174`: usage `task-update --id <task_id> --status <status> [--result <text>] [--run] [--from] [--retry-request]`; no spec/brief flag. Valid statuses: pending, ready, dispatched, completed, failed, blocked | [CODE-VERIFIED] (dev checkout) |
| Contract never uses `worker-start --retry-of` | `:73` | Flag exists: `IronOrca/src/cli/specs/orchestration-worker-specs.ts:8,28,47` (needs `--task` naming the failed Task; `--spec` creates a new one; placement not inherited). Orca's own guide recommends it for `failed`/`stopped` workers (`IronOrca/src/cli/bundled-skill-guides.ts:4455`). The contract therefore deliberately diverges from Orca's documented retry path; this is a policy choice, not an Orca limitation | [CODE-VERIFIED] flag exists; divergence is intentional per `:73` rationale (brief immutable, directories could mix) |
| Orca counts circuit-breaker failures per Task, trips at three | `:75` | `IronOrca/src/main/runtime/orchestration/db/dispatch-context/dispatch-circuit-breaker.ts:1` `DISPATCH_CIRCUIT_BREAK_FAILURES = 3`; `IronOrca/src/main/runtime/orchestration/db/worker-dispatch/worker-dispatch-start.ts:94-134`: the refusal "failed N times, so Orca will not retry it again" (`:99-107`, `prior.status === 'circuit_broken'`) sits INSIDE `if (params.retryOf) {` (`:95`); the `else if (task.status !== 'ready')` branch (`:128`) has no breaker check, and the comment at `:126` says "Only a retry chain inherits failures; a fresh start after a worker exit keeps its own count" (`priorFailures = prior.failure_count` is set only inside the `retryOf` branch, `:127`). Failure counting: `IronOrca/src/main/runtime/orchestration/db/worker-dispatch/worker-terminal-recovery.ts:57-59` and `.../worker-dispatch-outcome.ts:64` (`failureCount >= DISPATCH_CIRCUIT_BREAK_FAILURES ? 'circuit_broken' : 'failed'`) | [CODE-VERIFIED] (dev checkout) for the count and for the `retryOf` gating. Consequence for the contract: WC-6 forbids `--retry-of` (`:73`), so a coordinator that follows WC-6 never starts through the `retryOf` branch and Orca's breaker refusal is never reached by the contract's own retry flow; the only guard is the coordinator's own three-failed-starts comparison (`:75`). See 6.3 |
| "`task-update ... failed --result cancelled`" to settle a stopped attempt | `:77` | `orchestration.ts:174`: "To cancel a Task, stop or abandon its worker, then set --status failed --result cancelled; a later worker-start --retry-of reopens it." | [CODE-VERIFIED] (dev checkout) |
| Follow-up `send --to dispatch:<id>` unsuitable for carrying a retry brief | `:78` | `orchestration.ts:51` shows `send --to <run:id\|dispatch:id\|legacy_handle>` exists. The timing argument (Dispatch ID known only after ready; Claude worker already has its task on the command line) was not traced to launch code | [UNVERIFIED] rationale |

Normative rules in WC-6 with no code or test enforcement in IronClaude (all are coordinator-session instructions):
- Three-failed-starts comparison: "the coordinator makes this comparison itself" (`:75`). No IronClaude code does it.
- "No retry while the earlier attempt is not settled or reads `unverifiable`" (`:76`).
- Live attempt settles only on person-directed cancellation plus two reads 5 minutes apart that agree (`:79`).
- "A message from a settled or replaced attempt is logged and shown to the person, never applied" (`:79`); the quarantine check against current Task ID and Dispatch ID is repeated at `:106`.

Related: `:244` allows at most 2 brief fixes for the same work (3 attempts) after `guard refused:`; the third escalates to the person. Normative only.

Re-check of the Orca-premise rows of sections 2, 3 and 5.2 against the installed build files (fix cycle 1, read-only; ORCA-INSTALLED-FILES means file contents under `/opt/Orca/resources/app.asar.unpacked/out/`, not the running process). Paths below are relative to that `out/` directory.

| Premise (rows in sections 2, 3, 5.2) | Checkout result | Installed-file result | Verdict |
|---|---|---|---|
| `task-update` flags and the cancel note | `IronOrca/src/cli/specs/orchestration.ts:166-174` | `cli/specs/orchestration.js:163` (usage `--id --status [--result] [--run] [--from] [--retry-request]`) and `:168` (same cancel sentence) | Agree |
| `worker-start --retry-of`, `--worktree`, `--setup`, creation-flag rejection | `orchestration-worker-specs.ts:8,28,40,41,47` | `cli/specs/orchestration-worker-specs.js:9` (usage line), `:41`, `:43`, `:49` (same texts) | Agree |
| Circuit breaker: three failures, refusal only on a `retryOf` start | `worker-dispatch-start.ts:94-134` | `main/chunks/orcad-migration-source-retention-B-HAVPZ-.js:2591` (`if(e.retryOf){...n.status===\`circuit_broken\`` branch) and `:662` (`failure_count+1>=3?\`circuit_broken\`:\`failed\``) (minified bundle; branch read, not every caller) | Agree (and `git diff --quiet dc57b3d6e 9cfecdd30b2a... -- worker-dispatch-start.ts` printed no difference) |
| `check` flags, `--types` is the wake condition, whole-batch replay until `--ack`, repeated `--ack` is a no-op, several waiters get the same Delivery | `orchestration.ts:91,118,120` | `cli/specs/orchestration.js:89` (usage), `:116` (`--types` is the wake condition), `:118` ("Several --wait calls may wait on one Run inbox; waiting reserves nothing, listeners woken together get the same Delivery, and a repeated --ack is a no-op") | Agree |
| `terminal send --text --enter --wait-submit` | `terminal-send.ts:8,22` | `cli/specs/terminal-send.js:8,22` | Agree |
| `worker-list`, `worker-show`, `worker-read`, `agentWait` | `orchestration-worker-specs.ts:54,58,65,124` | `cli/specs/orchestration-worker-specs.js:56,60,66,121` (`agentWait` text at `:60`) | Agree |
| `task-create --deps` | `orchestration.ts:142` | `cli/specs/orchestration.js:138` | Agree |
| `worktree ps --agent-wait` | NOT accepted: `cli/specs/core.ts:152-156` | ACCEPTED: `cli/specs/core.js:157-161` (usage and `allowedFlags` include `agent-wait`), `cli/handlers/worktree.js:52` (`flags.has('agent-wait')`), also `cli/root-help-text-secondary.js:61`, `cli/flag-help-text.js:7`, `cli/bundled-skill-guides.js:482` | DIVERGENCE (see 6.5 SD-1) |
| `Re: Question` reply: subject and mark-read | `questions/question-threads.ts:141,147` | `main/chunks/orcad-migration-source-retention-B-HAVPZ-.js:1000` (`subject:\`Re: Question\`` and a `markAsRead` call) | Agree on subject and mark-read |
| `expect_silence` is an Orca field | zero matches in `IronOrca/src` | zero matches in `out/` (Grep, count 0) | Agree (absent in both) |
| Nested-worker depth default (used by 05, not by 02) | 1 (`shared/nested-worker-depth.ts:4`) | 2 (`shared/nested-worker-depth.js:10`) | DIVERGENCE (see research/05 section 5.2) |

## 3. Monitoring and messages: the wait, per-type handling, sweep (`WORKER-CONTRACT.md:95-114`)

Evidence class: NORMATIVE; Orca verb syntax checked against the Orca development checkout and, in fix cycle 1, the installed build files (the table in section 2 lists where they agree and differ); not the running build.

### 3.1 The wait command (`:99-108`)
Contract command: `orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000` (`:101`).
- [CODE-VERIFIED] (dev checkout) flags exist: `IronOrca/src/cli/specs/orchestration.ts:91` lists `--ack`, `--types`, `--wait`, `--timeout-ms`.
- [CODE-VERIFIED] (dev checkout) `--types` is the wake condition only; a returned Delivery is the whole FIFO batch, replayed until `--ack` (`orchestration.ts:118,120`). This matches `:103`.
- [CODE-VERIFIED] (dev checkout) "A repeated `--ack` is a no-op" (`orchestration.ts:120`); `:104` requires the coordinator to write one run-notes line per message ID before `--ack`. The run-notes write is a coordinator duty with no code behind it in IronClaude.
- Contract UNVERIFIED point "whether two consumers on one mailbox both get a batch" (`:200`): the dev-checkout help text says "Several --wait calls may wait on one Run inbox; waiting reserves nothing, listeners woken together get the same Delivery" (`orchestration.ts:120`). So the dev checkout states an answer; the contract still marks it UNVERIFIED and runs one wait per Run inbox. Not a contradiction (contract is conservative); flag that the UNVERIFIED label may be stale relative to the dev checkout. The installed build's help text carries the same sentence ([CODE-VERIFIED] ORCA-INSTALLED-FILES, `cli/specs/orchestration.js:118`), so the "listeners woken together get the same Delivery" text agrees in both sources. That is documentation text of the CLI help; the delivery behavior of the running build is UNVERIFIED-DEPLOYED.
- Contract UNVERIFIED point "`orca orchestration reply` stores type `status` with subject 'Re: Question'" (`:197`): the subject is [CODE-VERIFIED] at `IronOrca/src/main/runtime/orchestration/db/questions/question-threads.ts:141` (`subject: 'Re: Question'`), and the reply message is marked read at `:146-147` ("ask returns the answer directly; mark it read to prevent replay through check"). The message `type` value was not traced in the first pass; fix cycle 1 traced it: the reply call `insertMessage({from, to, subject: 'Re: Question', body, threadId, runId})` (`question-threads.ts:138-145`) passes no `type`, and `insertMessage` stores `msg.type ?? 'status'` (`IronOrca/src/main/runtime/orchestration/db/messages/message-insert.ts:55`), so the stored type is `status` [CODE-VERIFIED] (dev checkout). The reply is then marked read at `:147`. The contract's lead that a narrow `--types` waiter may miss the answer is consistent with both facts (the answer is a `status` message that is already read), but whether a waiter is woken at all was not traced: that part stays [UNVERIFIED]. The installed bundle has the same subject and a `markAsRead` call (`main/chunks/orcad-migration-source-retention-B-HAVPZ-.js:1000`); its default type was not read.

### 3.2 Per-type handling (`:108`)
| Message type | Contract duty |
|---|---|
| `heartbeat` | update heartbeat record; never a stall proof |
| `status` with ack line | ack rules (WC-12, `:61`, `:131-138`) |
| `status` naming a report path / saying work complete | sets S9 when brief has no later `Command:` line; otherwise logged |
| other `status` | logged |
| `worker_done` | open the contract; a second one for the same dispatch is logged and ignored |
| `question` | answer with `reply --id`, or forward to the person; starts the ack clock |
| `escalation` | L1 then L5 |
| `decision_gate` | goes to the person |
| `handoff` | new work left to coordinator decision (WC-13) |
| `merge_ready` | merge only on the person's instruction |
| `dispatch` | logged as unexpected |
| unknown type | sender goes to S11 and is shown to the person, never silently acked (`:105`) |
The coordinator never sends or synthesizes `worker_done` for a worker (`:108`). Identity check: `worker_done`, `question`, `escalation`, `handoff`, `merge_ready` are checked against the sender's current Task ID and Dispatch ID; mismatch is quarantined (`:106`). No IronClaude code implements this dispatch table.

### 3.3 Sweep and deadlines (`:110-114`)
- Sweep (at most every 5 minutes): one `worker-list`, one `worktree ps --agent-wait`, one `stat` per worker contract path (`:110`).
- [CODE-VERIFIED] (dev checkout) `worker-list` exists with `--run`, `--terminal-state`, `--limit` (`IronOrca/src/cli/specs/orchestration-worker-specs.ts:124`); `worker-show`, `worker-read --source <auto|transcript|terminal>` exist (`:54`, `:65`); `observation.agentWait` is described at `:58`.
- [CODE-CONTRADICTED] by the Orca development checkout only; [CODE-VERIFIED] by the installed build files: `worktree ps --agent-wait` is a state divergence between two Orca sources, not a contract defect (corrected in fix cycle 1; the first pass called it a defect candidate).
  - Development checkout (`/home/coder/workspaces/IronOrca`, `main`, commit `dc57b3d6e81c9825446a520bf0aee8600a2f5586`): the spec is `orca worktree ps [--limit <n>] [--json]` with `allowedFlags: [...GLOBAL_FLAGS, 'limit']` (`IronOrca/src/cli/specs/core.ts:152-156`; help text `IronOrca/src/cli/root-help-text-secondary.ts:58`). A search of `IronOrca/src` found `agent-wait` only in `src/shared/agent-status-child-work-legacy-golden.test.ts`.
  - Installed build files on this host (`/opt/Orca/resources/app.asar.unpacked/out/`, metadata version `1.4.245-aidev02.9cfecdd30b2a`): the spec is `usage: 'orca worktree ps [--limit <n>] [--agent-wait] [--json]'` with `allowedFlags: [...args_1.GLOBAL_FLAGS, 'limit', 'agent-wait']` (`cli/specs/core.js:157-158`, note at `:161`: "pass --agent-wait to add the `terminal show` wait verdict to each terminal-backed agent row"), and the handler reads `flags.has('agent-wait')` (`cli/handlers/worktree.js:52`). The flag also appears in `cli/root-help-text-secondary.js:61`, `cli/flag-help-text.js:7` and `cli/bundled-skill-guides.js:482`.
  - Why they differ: the installed build's recorded commit `9cfecdd30b2a...` is on `origin/aidev02` and is 1048 commits ahead of the checkout HEAD; `git grep agent-wait 9cfecdd30b2a... -- src/cli/specs/core.ts src/cli/handlers/worktree.ts` prints `core.ts:158,159,162` and `worktree.ts:97`. So the flag exists in the newer source and in the installed files; the checkout is an older snapshot.
  - Consequence: the sweep's "prompt-wait listing (`worktree ps --agent-wait`)" at `WORKER-CONTRACT.md:110` names a flag the installed build files accept. It is NOT shown wrong against the installed build, and no defect and no remediation task follow (BUILD-REQUEST C8: not an in-scope shipped-but-unwired capability against the installed build). What stays UNVERIFIED: the running Orca process, and other hosts' installed builds; and the checkout `main` is not a valid reference for this verb. A technical reference must say "accepted by the installed build files read on this host; not in the development checkout `main` at `dc57b3d6e`".
  - Also: `agentWait` is the per-row field `worktree ps --agent-wait` adds, and `worker-show` exposes `observation.agentWait` in both sources (checkout `orchestration-worker-specs.ts:58`; installed `cli/specs/orchestration-worker-specs.js:60`). The contract text `agent-wait` appears once in section 4, at `:110`.
- Deadline W = `max(10 min, 2 x observed median heartbeat interval)` or the worker's declared `expect_silence_min`, capped at 45 minutes (`:112`). Starting values stated as "not a measured one" (`:97`). No code computes W.
- [CODE-VERIFIED] (absence, both Orca sources) `expect_silence_min` is a contract-defined token carried in heartbeat/status text (`:65`, `:46`). A search of `IronOrca/src` for `expect_silence` returned no match, and a Grep of the installed `out/` tree (all files) found no file, so it is an IronClaude convention interpreted by the coordinator's LLM, not an Orca field in either source. (Closed in fix cycle 1; first pass tagged it [UNVERIFIED] with the checkout only.)

## 4. Liveness states, answers/acks, ladder and restart (`WORKER-CONTRACT.md:116-200`)

Evidence class: NORMATIVE. All thresholds are declared "a starting value, not a measured one" (`:97`); a brief may override them, a worker may not.

### 4.1 State table S0-S11 (`:116-129`), reduced to trigger and response
| State | Trigger (abridged) | Response |
|---|---|---|
| S0 starting | no progress token or transcript 10 min after start | L1, L2 "begin your brief", L5 by 15 min |
| S1 progressing | token changed within W and semantic change within 10 min | L0 |
| S2 long step | declared window, or transcript activity under 5 min old | L1 at 10 min even inside window; past window L1, L3, L5 by 15 min |
| S3 idle at prompt | no token change for W and last transcript entry >= 5 min old with no `worker_done`, empty prompt, no pending ask | L1, L2, L3; L4 only with a stall proof; third idle episode goes to L5 |
| S4 blocked on person prompt | `agentWait` non-null | capture screen; L5 at 5 min plus Orca delay, re-reported every 15 min; never answer |
| S5 blocked in ask | open `question` | answer, then ack timeline |
| S6 context exhausted | token unchanged for W while heartbeats arrive, or S3 trigger; screen text such as `Autocompact is thrashing` confirmed by a second read 5 min later | interrupt with handoff request (WC-14 exception); if turn ends without `worker_done`, L4 within budget else L5 |
| S7 unreachable | liveness `unverifiable` | L5 after 10 min; never L4 |
| S8 exited | liveness `exited` | settle under WC-6, then L4 or L5 |
| S9 finished but unreported | contract present, no later `Command:` line, no `worker_done` within one sweep | L1, L2 "send `worker_done` per WC-5", L5 by 10 min after nudge |
| S10 settled | `worker_done` received | none |
| S11 unknown | deciding evidence stale or unknown | L1, then as resulting state; no typed input |

Observations:
- "Liveness `unverifiable` / `exited`" are named as Orca-produced values (`:76`, `:125-126`, `:157`). Dev-checkout evidence: the PTY liveness verdict has statuses `live`, `exited` and `unverifiable` (`IronOrca/src/main/runtime/unstopped-pty-verification.ts:44,50`; consumers `session-tabs/explicit-terminal-close-pty-stops.ts:33,40`). The CLI spec for `worker-show`/`worker-list` (`orchestration-worker-specs.ts:54-124`) contains neither word as a liveness field (only `--terminal-state <active|reclaimable|retained|release_pending|release_unknown|released>` at `:124`, and the word "unverifiable" in a note about worker identity at `:58`). So the words exist in Orca runtime code, but the path by which `worker-show` surfaces them to the coordinator was not traced: [UNVERIFIED] surface; partial [CODE-VERIFIED] vocabulary.
- `Autocompact is thrashing` is a screen string the coordinator reads (`:124`); `:198` labels the attention category UNVERIFIED. Consistent with its own caveat.
- S6 is the only place the contract depends on a worker-side behavior (write handoff file, end turn without `worker_done`). Worker side: WC-14 exception (`:63`) and WC-15 handoff files (`:64`). Both normative.

### 4.2 Answers and acks (`:131-144`), WC-12 (`:61`)
- Timeline: A1 record `pending_ack`; A2 at 5 min with no ack or heartbeat: L1 probe; A3 at 5 min only on a positively idle empty prompt: type ONE copy with `orca terminal send --text "<copy>" --enter --wait-submit <s>`, at most one per message ID; A4 at 15 min: L5 report.
- [CODE-VERIFIED] (dev checkout) `terminal send` accepts `--text`, `--enter`, `--wait-submit <seconds>` (`IronOrca/src/cli/specs/terminal-send.ts:8`). Note `:22`: "`--wait-submit` only observes the accepted prompt ... timeout returns the queued/input-accepted receipt and never resends"; consistent with the contract's one-copy-per-message-ID cap.
- The typed copy text is a fixed one-liner (`:143`) and the nudge text a fixed one-liner (`:164`). These are string templates inside the Markdown contract; no code emits them.
- `pending_ack` (`:133`) and `unacked-at-settlement` (`:138`) are the contract's own labels for coordinator run-notes. A search of the checkout (excluding `.dev/`, `docs/`, `.venv/`) found them only at `WORKER-CONTRACT.md:133` and `:138`: not in any code and not pinned by `tests/skills/test_worker_contract.py`.

### 4.3 Ladder L0-L5 and caps (`:146-159`)
- Caps: L1 at most 2 costly probes per triggered worker per sweep; L2 1 per incident, 2 per lineage (a nudge with no turn start still counts); L3 1 per incident; L4 1 per rolling 60 min, 2 per lineage, and WC-6's three-failed-starts rule, whichever is stricter; L5 S4 re-reported every 15 min.
- L4 allowed only on Orca positive stall proofs (`exited`, process exit, or a transcript whose final agent turn sent no `worker_done`) or a person's recorded stop (`:157`). Not stall proofs: nudges, asks, heartbeats, repeated identical reads, context exhaustion. Cross-ref `:79`, `:46`.
- Restart cause classes: `idle`, `context-exhausted`, `exited`, `unreachable-then-exited`; same class twice means no plain restart; for `context-exhausted` the next Task reduces load or goes to L5 (`:159`).
- Tension to record (not a defect, a drafting note): `:77` lets the coordinator stop the worker and set the old Task `failed --result cancelled` "after Orca's positive stall proof"; `:79` requires a person-directed cancellation for a live attempt; `:154` L4 permits "an Orca stall proof, or a person-directed cancellation with confirmed quiescence". Together they are consistent, but the S6 row (`:124`) says "L4 within the budget" after a turn ended without `worker_done`, which relies on the third stall proof (transcript whose final agent turn sent no `worker_done`) and on screen text confirmed twice. The contract itself says screen text alone is not authorization (`:182`). Interpretation, not verified by any test.

### 4.4 Resume note (`:167-180`)
Fields: replaced Task, cause class and evidence, lineage id and attempt, replaced Task/Dispatch IDs, completed `Command:` lines, last progress token, handoff file path (read at most 80 lines at a time), answered message IDs, uncertain effects, load rule, `Start at: Command: line <k>`. Placed after the guard line and before the `Command:` lines of the new Task's brief. For `/sc:implement`, its own `E-RESUME-NEEDED` re-run takes priority (`:167`; see section 5).
- Note the template is not emitted by code. `tests/skills/test_worker_contract.py:235` pins only the sentence "An L4 restart puts this note in the new Task's brief, after the guard line and before the `Command:` lines".

### 4.5 Never on silence (`:182-192`)
List: never stop a worker, create a retry Task, release a worker or worktree, mark a Task failed, answer a permission/person-only prompt, write or draft a Ruling, or send a lifecycle message for the worker; silence authorizes only L1, L2, L3. This is the same boundary WC-10 states from the worker side (`:46`).

### 4.6 UNVERIFIED list (`:194-200`) status
| Contract UNVERIFIED point | Status this run |
|---|---|
| what `check --wait` wakes on without `--types` | dev checkout says `--types` "is the wake condition"; without it behavior not read here [UNVERIFIED] |
| case 5 cause (answers a worker did not see; `reply` stores `status`/'Re: Question') | subject confirmed (`question-threads.ts:141`), message marked read (`:147`), type `status` confirmed by default (`message-insert.ts:55`) [CODE-VERIFIED] (dev checkout); whether a `--types` waiter is woken by it not traced [UNVERIFIED] |
| attention category for permission prompt / compact thrashing | not traced; `agentWait` evidence kinds are "hook, prompt-text, or title" (`orchestration-worker-specs.ts:58`) [UNVERIFIED] |
| Claude Code behavior for text typed during a tool call | outside Orca/IronClaude source [UNVERIFIED] |
| two consumers on one mailbox | dev-checkout help text answers yes, same Delivery (`orchestration.ts:120`); installed help text says the same (`cli/specs/orchestration.js:118`); running build UNVERIFIED |

## 5. Brief, result admission, `/sc:implement` freeze, worktrees, git and fan-in (`WORKER-CONTRACT.md:81-93, 202-282`)

Evidence class: NORMATIVE; cross-references into the `sc-implement-protocol` skill are checked against checkout source (`src/superclaude/skills/sc-implement-protocol/`).

### 5.1 Brief contents and layout (`:81-93`, `:202-216`)
- Seven required brief items: exact `Command:` line(s); unique report dir; blocked-gate policy line; local-commit authorization quoting the user; P0-only report-file/outcome rule; statement that no other outward action can be authorized; worktree placement (shared feature worktree, or `worker-start --worktree new-child --base-branch <feature branch>` with `--setup skip`).
- Guard line (`:207`) and Chain line (`:213`) are fixed strings. [CODE-VERIFIED] pinned by `tests/skills/test_worker_contract.py` (`GUARD_LINE` at `:376-380`; Chain at `:371`; guard-before-command check `test_brief_template_puts_guard_line_before_first_command_line`, `:916`). This pins the text in the Markdown file, not the behavior of a coordinator session.
- `--unattended` decision test is "the guard's own test, run on the copies the worker will see" (`:216`): instruction only.
- [CODE-VERIFIED] (dev checkout) `worker-start` accepts `--worktree <current|selector|new-child|new-top-level>`, `--base-branch`, `--comment`, `--setup <run|skip|inherit>` (`IronOrca/src/cli/specs/orchestration-worker-specs.ts:8`); creation flags are rejected for current/existing worktrees (`:41`); new worktrees default `--setup` to run (`:40`). This matches `:91` and `:221`. `--worktree id:<worktree id>` (`:223`) and `path:<absolute worktree path>` (`:269`) selector forms: fix cycle 1 read the installed CLI selector code. `path:<absolute-server-path>` is [CODE-VERIFIED] (installed `cli/selectors.js:24,36,63`; `cli/help.js:166`). The id form is documented there as `id:<repo-id>::<path>` (`cli/selectors.js:63`, `cli/help.js:166`) and a separate `worktree:<worktreeId>` form (`cli/help.js:166`); whether the contract's "`id:<worktree id>`" equals `<repo-id>::<path>` is not shown: [UNVERIFIED] mapping, stale-wording candidate (G7).

### 5.2 Admission of results (`:237-246`)
Dispatch table (all normative):
| Contract `worker_status` | Dependents |
|---|---|
| `succeeded` | may start |
| `partial` | do not start until coordinator read `report_path` and recorded usability in run notes; unusable = treated as `failed` |
| `failed` / `blocked` | do not start; retry per WC-6, answer per worked example, or report; `/sc:implement` excepted (5.3) |
| no contract + body starts `guard refused:` | nothing ran; fix brief in a new Task; at most 2 fixes (3 attempts); third refusal escalates |
Other rules: dependents created only after all inputs settled and admitted, `--deps` naming Tasks that actually succeeded (`:245`); coordinator starts only Tasks it created (`:246`); follow-up Tasks created because a result revealed unplannable work are recorded in run notes with the extra time (feeds decision D5's revisit trigger). [CODE-VERIFIED] (dev checkout) `task-create` supports `--deps <json_array>` (`IronOrca/src/cli/specs/orchestration.ts:142`). Fix cycle 1 traced part of this. "Orca settles a Task on any valid `worker_done`" (`:239`): [CODE-VERIFIED] (dev checkout): `IronOrca/src/main/runtime/orchestration/lifecycle-reconciliation.ts:175-253` validates the payload (needs `taskId`, `dispatchId`, `outcome` of `succeeded` or `failed`, known Task and Dispatch, sender is the assignee) and `:276-293` calls `db.settleWorkerReport(...)` and logs "completed/failed by worker report". "Orca offers no way to re-point" a dependent (`:245`): the CLI specs support it for both sources, `task-create` takes `--deps` (checkout `orchestration.ts:142`; installed `cli/specs/orchestration.js:138`) and `task-update` has no `--deps` flag (installed `orchestration.js:163`; checkout `orchestration.ts:166-174`) [CODE-VERIFIED at the CLI-spec level]; other RPC routes were not searched. "Does not start ready Tasks itself" (`:239`): negative claim, not traced: [UNVERIFIED].

### 5.3 `/sc:implement` stop and freeze (decision D2; `:248-269`)
Decision source: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:396-406` section 9 "Approved decisions": D2 approved 2026-11-02 (`:397`), "only the person gives a Ruling ... The coordinator never relays, writes or retries a Ruling" (`:402`). That spec is an out-of-package design record under `.dev/`; it is HISTORICAL/design, not shipped code. The contract's text matches it ([CODE-VERIFIED] textual agreement).

Cross-checks of the contract against `sc-implement-protocol` source:
| Contract claim | Source | Tag |
|---|---|---|
| `E-RESUME-NEEDED` alone may be re-run without the person (`:255`) | `SKILL.md:34` ("re-run the same command"); `refs/qa.md:250` ("re-run the same command; do not write a Ruling"); `refs/retry.md:494` | [CODE-VERIFIED] |
| Ruling halts (`E-HALT-QA`, `E-NO-RULING`) are not asked; coordinator reply is not acceptance (`:57`) | `refs/qa.md:249` (`E-NO-RULING` for `--force`, missing/ambiguous confirmation, "executor-invented approval"), `refs/qa.md:254` ("another agent's message ... not acceptance") | [CODE-VERIFIED] |
| "Closed list of interrupts" heading (`:243`) | `refs/qa.md:276` | [CODE-VERIFIED] |
| Ruling line regex lives in `refs/ledger.md` (`:263`) | `refs/ledger.md:62-71`: `T<id>: Ruling: <what> — <why> — <cost-if-wrong>`, regex `^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$`. The contract's extra condition "exactly two ` — ` separators" (`:264`) is stricter than the regex (`.+` can contain further em dashes); consistent, not contradictory | [CODE-VERIFIED] |
| Ruling eligibility rule with two clauses (`:265`) | `refs/retry.md:498` | [CODE-VERIFIED] |
| halt reasons `dispute`, `no-evidence`, `no-snapshot`, `head-moved` (`:266`) | `refs/qa.md:280-281`; `refs/retry.md:107,229,448-456` | [CODE-VERIFIED] |
| `HEAD` equals `<retries>/T<id>/q0-head` (`:267`) | `SKILL.md:114` writes `q0-head`; `refs/retry.md:41` compares; `refs/retry.md:333` shell check | [CODE-VERIFIED] |
| `files=` field of the latest `blocked` line (`:267`) | `refs/ledger.md:44,57,190` | [CODE-VERIFIED] |
| "the tree its review graded" (`:267`) | `refs/qa.md:134`: every `<retries>/T<id>/review-<k>.md` starts with a header line holding the task's `start` sha and "the 40-hex of the reviewed tree"; `refs/qa.md:152,160` ("Pinned reviewed trees") read the pinned trees. So a stored artifact exists; that the contract's phrase means this pinned tree is an inference | [CODE-VERIFIED] artifact exists; mapping inferred |
| `E-ARCHIVE-BLOCKED` stop has no halted task (`:260`) | `SKILL.md:42`, `refs/managed-workspace.md:53-54`, `refs/qa.md:286` | [CODE-VERIFIED] |
Freeze state (`:250`): "latest implement contract is `blocked`, or `failed` with any STOP code other than `E-RESUME-NEEDED`" or ledger first non-complete task has `halt`/`blocked` last with no eligible Ruling. The freeze, the "Ruling written" hand-back and the 7-condition check (`:261-268`) are coordinator-session reasoning over the ledger; no script implements them. A related implemented tool: `refs/ledger.md` and `refs/retry.md` implement the executor-side ledger and ladder, not the coordinator-side freeze.
Placement: resume runs in the halted worktree by selector, never in a child (`:269`).

### 5.4 Worktrees (`:218-225`) and the one implemented guard
- Normative: Orca-created worktrees only, `--setup skip` unless the user's live instruction names setup, a placement map in run notes and in each `worker-start --comment`, merge-back then `orca worktree rm`, never remove worktrees holding unmerged work, never run one managed package in two worktrees.
- [CODE-VERIFIED] (checkout) the only code that touches this duty is `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`: registered as a PreToolUse hook at `src/superclaude/hooks/hooks.json:110` (timeout 3). It blocks `orca worktree create` without `--agent` and says so in its own header: "Only the --agent requirement is enforced here; 'no worktree for your own use' and 'the creator owns the agent' are instruction text" (`:7-8`). It fails open on missing `jq`/`awk`, bad JSON or scanner error (`:12-14`). It does not block raw `git worktree add`, `.dev/worktrees/` paths, `--setup run`, or removal of worktrees with unmerged work (no match for `git worktree` or `worktree add` in the script). So those parts of `:220-225` are NORMATIVE with no enforcement, and the hook is not specific to the coordinator role.
- The launch-level guard (`hooks.json:67,120`) governs only sessions "the claim script launched (a valid top-level session_id bound in the store); every other session is ordinary and never blocked" (`launch-level-guard.sh:5-7`). A person-opened coordinator is therefore not governed by it. It does allow read-only orchestration verbs without an escape class: `orchestration check|inbox|run-current|task-list|worker-show` (`launch-level-guard.sh:476`), and every other `orca` subcommand falls to the default branch that adds the ESCAPE class (`launch-level-guard.sh:477`); the tests list `orca orchestration send x`, `orca orchestration dispatch x` and `orca worktree create --name x` in `ESCAPE_BASH` (`tests/hooks/test_launch_level_guard.py:3093`, rows `:3108-3110`) and the five read-only verbs in `NONE_BASH` (`:3122`, rows `:3142-3146`). That concerns launched issue sessions, not supervised workers. A search of the three hook scripts for worker/dispatch/preamble/task-id terms found no worker-run detection; the only worker wording is the block message of `require-orca-worktree-agent.sh:355` ("A supervised coordinator is person-opened; workers cannot create worktrees or dispatch workers"), which is message text, not a predicate.

### 5.5 Git/GitHub ownership (`:227-235`)
Normative duties: coordinator-only outward actions on `IronbellyOrg/IronClaude`; progress posts from read contracts; PRs only via `/sc:pr-submit --monitor 3` in an ordinary top-level session (decision D3 at spec `:403`); show unseen worker commits before any push; commit only when no worker runs in that worktree and no frozen `/sc:implement`; compare `git status --porcelain` with settled contracts; stage explicit paths plus `.dev/tasks`; `git commit --only -- <paths>`; never `--no-verify`. [CODE-VERIFIED] textual agreement with project `CLAUDE.md` (fork-only PR rule, `/sc:pr-submit --monitor 3`, `.dev/tasks` always staged) in this session's loaded instructions. Enforcement of the push/PR parts exists only for sessions launched by the issue claim script (`launch-level-guard.sh`, messages LL-PUSH, LL-SUBMIT, LL-REPO at `:46-77`), not for a coordinator.

### 5.6 Fan-in and worked example (`:271-281`)
Fan-in: wait for all N inputs, admit `succeeded` or usable `partial`, N at most 10 (the merge command's maximum), create the merge Task only with at least 2 admitted, list dropped inputs and reasons in the merge brief. Worked example: tdd gate hit, `blocked_question`, new Task T2 with `replaces T1`, new report dir `auth-2`. Both normative; the 10-input maximum is the merge command's own limit: [CODE-VERIFIED] `src/superclaude/commands/adversarial.md:3,15,39,58,169` say `--compare` takes 2-10 files (closed in fix cycle 1).

## 6. What actually runs: delivery path, tests, and enforcement ceiling

### 6.1 Delivery path of the section 4 rules (CHECKOUT-SOURCE)
- Installed: `src/superclaude/cli/install_core.py:14-29` lists `WORKER-CONTRACT.md` in `KNOWN_CORE_FILES`; the installer copies core `.md` files to `~/.claude/`. [CODE-VERIFIED] distribution wiring. (Installed-copy parity at this run: identical, section 1.)
- Not auto-loaded: the contract is not an `@` import in `src/superclaude/core/CLAUDE.md` (the core CLAUDE.md text read in this session has no `WORKER-CONTRACT` reference). `HOW-WE-WORK.md` is documented as "not loaded automatically" (core `CLAUDE.md` Key Docs) and carries the pointer `HOW-WE-WORK.md:396-406` ("Orca coordination": coordinator is a person-opened session; rules live in `~/.claude/WORKER-CONTRACT.md`). Commands with an `## Unattended mode` section say "read it first" (e.g. `plugins/superclaude/commands/workflow.md:68`). Consequence: a coordinator session obeys section 4 only if it reads the file; no hook, startup step or code verifies it did. [CODE-VERIFIED] absence of an automatic load in the files read; a hook that injects the file at coordinator session start was not searched beyond the three scripts in scope (`launch-level-guard.sh`, `launch-job-identity.sh`, `require-orca-worktree-agent.sh`) and the registration `hooks.json`: [UNVERIFIED] for other hooks and for ccsession.
- `HOW-WE-WORK.md:396-406` summarizes roles, brief, never-as-worker, worktrees and outward actions, but says nothing about retries (WC-6), liveness supervision, the ladder, the resume note, or the `/sc:implement` freeze. Those exist only in `WORKER-CONTRACT.md` section 4.

### 6.2 Test coverage of section 4 (CHECKOUT-SOURCE: `tests/skills/test_worker_contract.py`, 3195 lines)
- The file is a static text pin: `CONTRACT_PATH = src/superclaude/core/WORKER-CONTRACT.md` (`:19`); each rule maps to phrases that must appear in the contract (`RULE_PHRASES`, `:25-374`); `test_contract_states_rule` is parameterized over it (`:907-909`). Negative tests remove a phrase and expect the check to fail (`test_rule_check_fails_when_rule_removed`, `:1045`).
- Section 4 rules pinned (by phrase only): WC-6 (`:181-189`), live-attempt settlement (`:190-198`), wait command and ack rule (`:199-208`), sweep and S6/S9/S10/S11 rows (`:209-219`), acks A4 (`:220-227`), ladder caps, restart budget and resume-note placement (`:228-237`), never-on-silence (`:238-244`), UNVERIFIED list (`:245-254`), brief contents (`:255-262`), worktrees and child setup (`:263-279`), git/GitHub ownership (`:280-288`), read-before-depend and dependents (`:289-299`), implement stop headings (`:300-308`), fan-in max/min (`:309-310`), absence-not-death (`:311-318`), liveness stat (`:319-324`), heartbeat token (`:325-331`), ack batch (`:332-339`), `ask` return (`:340-346`), WC-5 closing report type (`:347-352`), WC-7 Skill invocation (`:353-359`), brief template and chain line (`:360-373`).
- Not pinned by any phrase in `RULE_PHRASES`: S0-S5, S7 and S8 rows; the deadline-W formula (`:112`); starting values (`:114`); the typed-copy and nudge strings (`:143`, `:164`); the resume-note field list (`:169-180`); the seven freeze conditions beyond heading phrases (`:261-268`); the guard-refusal limit of 2 brief fixes (`:244`). Absence from `RULE_PHRASES` was read from the dictionary at `:25-374`; other helpers or tests elsewhere in the 3195-line file were not exhaustively searched for these strings: treat "not pinned" as [UNVERIFIED] beyond the dictionary.
- No test in `tests/` exercises coordinator behavior (state machine, ladder, acks, retries, resume): a search of `tests/` for the Orca verbs `orchestration (check|reply|worker|task|dispatch|send|ask)`, `worker-start` and `worker_done` matched 15 files: hook rows (`tests/hooks/test_launch_level_guard.py:3108-3110, 3142-3146`; `tests/hooks/test_require_orca_worktree_agent.py:37,115`), the text pin `tests/skills/test_worker_contract.py`, a guidance-text check (`tests/core/test_orca_session_launch_guidance.py:27`, the string "`worker-start`"), and 11 files under `tests/swarm/`. The `tests/swarm/` hits were not opened; the swarm CLI has its own in-process `worker_done` event type (`src/superclaude/cli/swarm/models.py:81,1206`, `tui.py:163`), so they are assumed unrelated to Orca messaging: [UNVERIFIED] assumption. Therefore section 4 behavior has no automated runtime check; a passing `test_worker_contract.py` proves the text is present, not that a coordinator follows it.

### 6.3 Enforcement ceiling per duty (summary)
| Duty | Normative location | Code/hook enforcement in checkout |
|---|---|---|
| Orca worktrees must carry an agent | `src/superclaude/core/CLAUDE.md:55-61` and project `CLAUDE.md:312` (the agent rule); `WORKER-CONTRACT.md:220` states only that worktrees are created by Orca at its default location, never with raw `git worktree add` (it does not mention `--agent`) | `require-orca-worktree-agent.sh` blocks `orca worktree create` without `--agent` (fail-open); registered `hooks.json:110`; tests `tests/hooks/test_require_orca_worktree_agent.py`. The Orca-only creation rule of `:220` has no enforcement (the hook does not block raw `git worktree add`) |
| Every retry is a new Task; no `--retry-of` | `:73` | none in IronClaude. Orca side: the circuit-breaker refusal runs only on a `worker-start --retry-of` start (`IronOrca/.../worker-dispatch/worker-dispatch-start.ts:94-134`; installed bundle `main/chunks/orcad-migration-source-retention-B-HAVPZ-.js:2591`), and WC-6 forbids `--retry-of`, so Orca's breaker never guards the contract's retry flow. The only guard is the coordinator's own comparison (`:75`), which no code performs: an enforcement gap to state in the reference |
| Wait with all nine types, ack after notes | `:101-104` | none |
| Sweep, S0-S11, ladder, caps, nudge/ack text | `:110-165` | none |
| Resume note for L4 restart | `:167-180` | none |
| Never act on silence | `:182-192` | none |
| Child worktree setup `--setup skip` | `:221` | none |
| Outward actions only by coordinator | `:229-235` | only for sessions launched by the issue claim script: `launch-level-guard.sh` (LL-PUSH, LL-SUBMIT, LL-REPO, etc.); a person-opened coordinator and a supervised worker are ordinary sessions there (`launch-level-guard.sh:5-7`) |
| Frozen `/sc:implement` plan; Ruling check | `:250-269` | executor side only (ledger and ladder in `sc-implement-protocol`); coordinator-side freeze none |
| Fan-in thresholds | `:273` | none |

### 6.4 Interaction found: launch-level guard allow-list vs the contract's sweep verbs (CHECKOUT-SOURCE)
`launch-level-guard.sh:475-477` allows only these `orca` read verbs without adding the ESCAPE class: `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read`, and `orchestration check|inbox|run-current|task-list|worker-show`. The sweep and ladder verbs `worker-list`, `worker-read`, `worktree ps`, `terminal send`, `orchestration reply`, `task-create`, `worker-start` all fall through to the default and add ESCAPE (`:477`). This binds only a session the claim script launched (`:5-7`). The historical report records the same observation (`.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/research/04-hooks-guards-identity.md:99`, section B2). Re-read in this run against the live script: [CODE-VERIFIED]. It is not a defect for a person-opened coordinator, which the guard does not govern; it is a limit for any future governed supervisor, which is the deferred sub-orchestrator mode and not shipped.

### 6.5 DEFECT register and state divergences
DEFECT register (in-scope capability documented as shipped or enabled but unwired at runtime): no entry. The first pass listed `DC-1` (`worktree ps --agent-wait`) as a defect candidate; fix cycle 1 retagged it as a state divergence (SD-1 below) and removed the "correct the verb" suggestion, because the installed build files accept the flag.

| ID | Scope | Evidence | Status |
|---|---|---|---|
| SD-1 (was DC-1) | `orca worktree ps --agent-wait` in the sweep (`WORKER-CONTRACT.md:110`): the Orca development checkout lacks the flag, the installed build files on this host have it | Checkout `main` `dc57b3d6e`: `worktree ps` accepts only `--limit` and global flags (`IronOrca/src/cli/specs/core.ts:152-156`). Installed files: `cli/specs/core.js:157-161` (usage and `allowedFlags` include `agent-wait`), `cli/handlers/worktree.js:52`, `cli/root-help-text-secondary.js:61`, `cli/flag-help-text.js:7`, `cli/bundled-skill-guides.js:482`. The installed build's recorded commit `9cfecdd30b2a...` has it in source (`git grep` of `src/cli/specs/core.ts:158`, `src/cli/handlers/worktree.ts:97`) and is 1048 commits ahead of the checkout HEAD (section 3.3) | State divergence, no defect, no remediation task. The contract line is not shown wrong against the installed files. UNVERIFIED: the running Orca process and any other host's installed build. Reference wording: "`worktree ps --agent-wait` is accepted by the Orca build files installed on the research host; the Orca development checkout `main` at `dc57b3d6e` does not list it; the running build and other hosts were not checked." |

Historical provenance of the verb (kept from the first pass, minor): a search of `.dev/` for `agent-wait` returned 12 files (one was this research file): the earlier research report and its QA snapshots (`TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/...`), `research/04-hooks-guards-identity.md:99`, two retry prompts of `TASK-WF-applyTheV1Worker-20261107-211837/artifacts/retries/T6/` and the brainstorm `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md:164,210,245`. The brainstorm cites `enrichment/codebase-context.md:19` as the source of the flag (`merged-requirements.md:164`); that file does not exist under the brainstorm directory (Glob of `.dev/` found none there), so that provenance is cited-but-absent. This no longer matters for correctness: the installed files carry the flag.

No other in-scope section-4 capability is documented as shipped-but-unwired as code: the coordinator rules are documented as instructions, and the contract itself marks five points UNVERIFIED (`:194-200`). The gap is that none of them have runtime checks, which is a limitation to state in the technical reference, not a defect against a claim of enforcement. One more enforcement gap found in fix cycle 1: Orca's circuit breaker never guards the contract's retry flow (see 6.3, row "Every retry is a new Task").

## 7. Key takeaways

1. Section 4 (`WORKER-CONTRACT.md:67-282`) is entirely NORMATIVE. It defines a coordinator lifecycle (create Task, start worker, wait, sweep, classify S0-S11, escalate L0-L5, admit result, retry as new Task, merge, stage, publish on instruction) that an LLM coordinator session performs. No IronClaude code implements the loop, the state machine, the ladder, the ack timeline, the retry rule or the resume note.
2. The only automated checks are static: `tests/skills/test_worker_contract.py` asserts that phrases exist in the file; it cannot show a coordinator behaves as written. One related hook (`require-orca-worktree-agent.sh`) enforces only "`orca worktree create` needs `--agent`", fails open, and says the rest is instruction text.
3. Orca-side premises of WC-6 and the wait protocol check out against both the Orca development checkout and the installed build files (task-update flags, `--retry-of` exists but is deliberately not used, circuit breaker = 3 failures per Task, `check --wait --types` wake semantics, whole-batch replay until `--ack`, `terminal send --wait-submit`; table in section 2). The breaker's refusal runs only on a `--retry-of` start, so the contract's WC-6 retry flow never reaches it; only the coordinator's own comparison guards repeated failures. This is file-content evidence, not proof of the running Orca process.
4. One contract verb differs between the two Orca sources: `orca worktree ps --agent-wait` (`:110`) is not in the development checkout `main` (`dc57b3d6e`) and is accepted by the installed build files on this host (`cli/specs/core.js:157-161`, `cli/handlers/worktree.js:52`). Recorded as state divergence SD-1, not a defect; no remediation task. The running build and other hosts are UNVERIFIED.
5. `/sc:implement` freeze and Ruling-eligibility rules cross-check cleanly against `sc-implement-protocol` source (Halt table, eligibility rule, `q0-head`, halt reasons, `E-RESUME-NEEDED`), but the coordinator-side freeze and 7-condition check have no script.
6. The rules reach a coordinator only if it reads `~/.claude/WORKER-CONTRACT.md`: installed by `install_core.py`, pointed to from `HOW-WE-WORK.md:396-406` and command `## Unattended mode` sections, never `@`-imported. `HOW-WE-WORK.md` does not summarize retries or liveness.
7. Subordinate/sub-orchestrator mode is deferred. Section 4 and the hooks contain no such mode; only the guard-governed read-only allow-list gap (6.4) hints at what a future governed supervisor would need.
8. The brief template (`WORKER-CONTRACT.md:283-327`, section 11) carries all seven brief contents of `:83-91` plus the two fixed lines, and its directory-flag cells match the command files; it has no slot for the L4 resume note or the `replaces T1` line, no session-name text, and its slot rules keep P0 wording that tests pin. The rows in sections 1-6 are normative restatements, not runtime proof.

## 8. Gaps (contradicted and unverified claims)

| # | Item | Tag | Detail |
|---|---|---|---|
| G1 | `worktree ps --agent-wait` in the sweep (`WORKER-CONTRACT.md:110`) | [CODE-CONTRADICTED] by the Orca dev checkout `main` (`core.ts:152-156`); [CODE-VERIFIED] by the installed build files (`cli/specs/core.js:157-161`, `cli/handlers/worktree.js:52`); running build UNVERIFIED | State divergence SD-1 (section 6.5), not a defect |
| G2 | Research notes say the contract is 273 lines (`research-notes.md:9`) | [CODE-CONTRADICTED] | file is 327 lines; section 4 is `:67-282` |
| G3 | Orca liveness words `unverifiable`/`exited` as seen by `worker-show` | [UNVERIFIED] surface | vocabulary exists in `IronOrca/src/main/runtime/unstopped-pty-verification.ts:44,50`; CLI field not traced |
| G4 | `expect_silence_min` | [CODE-VERIFIED] absent as an Orca field (closed, fix cycle 1) | zero matches in `IronOrca/src` and in the installed `out/` tree; contract-level convention read by the coordinator LLM |
| G5 | Reply message type `status` and "narrow `--types` may miss it" (`:197`) | type [CODE-VERIFIED] (dev checkout); waiter wake [UNVERIFIED] | subject, mark-read, default type `status`: `question-threads.ts:138-147`, `message-insert.ts:55` |
| G6 | "Orca settles a Task on any valid `worker_done` and does not start ready Tasks itself" (`:239`); "Orca offers no way to re-point" a dependent (`:245`) | settlement [CODE-VERIFIED] (dev checkout); no re-point via CLI specs [CODE-VERIFIED]; "does not start ready Tasks itself" [UNVERIFIED] | `lifecycle-reconciliation.ts:176-293`; `orchestration.js:138,163` (installed) |
| G7 | `--worktree id:` / `path:` selector forms (`:223`, `:269`) | `path:` [CODE-VERIFIED] (installed); `id:<worktree id>` vs installed `id:<repo-id>::<path>` [UNVERIFIED] mapping | `cli/selectors.js:63`, `cli/help.js:166` |
| G8 | Retry-brief timing argument against `send --to dispatch:<id>` (`:78`) | [UNVERIFIED] | rationale not traced to launch code |
| G9 | "the tree its review graded" (`:267`) | [CODE-VERIFIED] artifact exists (closed, fix cycle 1); mapping inferred | `refs/qa.md:134,152,160` pinned reviewed tree in `review-<k>.md` |
| G10 | `/sc:adversarial` 2-10 input maximum for fan-in (`:273`) | [CODE-VERIFIED] (closed, fix cycle 1) | `src/superclaude/commands/adversarial.md:3,15,39,58,169` |
| G11 | UNVERIFIED point "two consumers on one mailbox" (`:200`) | stale-label candidate | dev checkout and installed help text both state listeners get the same Delivery (`orchestration.ts:120`; `cli/specs/orchestration.js:118`); running build UNVERIFIED |
| G12 | Whether any hook or ccsession step injects the contract into a coordinator session | [UNVERIFIED] | only three scripts plus `hooks.json` searched |
| G13 | Deployed Orca build, running coordinator behavior, installed-hook ordering | [UNVERIFIED] | outside observed evidence; no live Orca run was made |
| G14 | `tests/swarm/` hits for `worker_done` assumed unrelated to Orca | [CODE-VERIFIED] unrelated (closed, fix cycle 1) | 0 files in `tests/swarm` match the Orca verbs (`orca orchestration`, `worker-start`, `orca worktree`, `orca terminal`, `orca agent`); the 11 `worker_done` files are the in-process event type (`tests/swarm/test_tail_events.py:39,70,93,117`); `src/superclaude/cli/swarm` has no `orca` text |
| G15 | Several unpinned rows (S0-S5, S7, S8, deadline W formula, nudge strings) | [CODE-VERIFIED] for the tokens searched (closed, fix cycle 1) | a search of all `tests/**/*.py` for `expect_silence`, `S0 `, `S7 `, `S8 `, `starting value`, `2 x observed`, `median`, `Resume note`, `Start at:` found no pin in `test_worker_contract.py`; hits are the S6 nudge phrases (`:162,195,233,316`) and unrelated timing code in `test_launch_level_guard.py` |
| G16 | Contract section 5 (`WORKER-CONTRACT.md:283-327`) had no investigation in the first pass | investigated in section 11 | the first-pass assignment used a stale 273-line count |

### 8.1 Gap fields: why it matters, closure, reference wording (fix cycle 1)

| # | Why it matters | Closure (read-only command or file, or "needs live Orca, out of scope") | Sentence for the reference if it stays an accepted limit |
|---|---|---|---|
| G1 | A reader could copy the verb or call it a bug | Closed as SD-1 with the installed files; remaining: running build, other hosts need live Orca (out of scope) | "`worktree ps --agent-wait` is accepted by the installed Orca build files read on the research host; it is absent from the development checkout `main` at `dc57b3d6e`; the running build was not checked." |
| G2 | A stale line count misleads the next reader and explains why section 5 was missed | Closed: `wc -l src/superclaude/core/WORKER-CONTRACT.md` prints 327; recorded here and in the stale list; `research-notes.md` is an input document and is not edited | n/a (closed) |
| G3 | The S4/S7/S8 rows depend on `exited`/`unverifiable` reaching the coordinator through `worker-show` | Trace the `worker-show` handler and its result type in `IronOrca/src/cli/` and in the installed bundle (read-only), or observe a live worker (needs live Orca, out of scope) | "The contract names the liveness values `unverifiable` and `exited`; the vocabulary exists in Orca runtime code, but the path by which `worker-show` surfaces it was not traced." |
| G4 | Decides whether `expect_silence_min` is an Orca field | Closed: absent in both Orca sources | n/a (closed) |
| G5 | Explains missed answers (contract case 5) | Remaining part: read the `check --wait` wake path for already-read `status` messages in the installed bundle or run live (needs live Orca, out of scope) | "A reply is stored as a `status` message that is already marked read; whether a narrow `--types` waiter is woken by it was not traced." |
| G6 | Dependents rule (`:245`) and "Orca does not start ready Tasks" drive the admission procedure | Settlement and no-re-point closed at CLI level; "does not start ready Tasks itself" needs a search of the Task scheduler in `IronOrca/src/main/runtime/orchestration/` or live Orca | "Orca settles a Task on a valid `worker_done` (development checkout); that it never starts ready Tasks itself was not traced." |
| G7 | A wrong selector breaks a resume (`:223`, `:269`) | Compare "worktree id" with `<repo-id>::<path>` in `IronOrca/src/main/runtime/` selector resolution (read-only) | "`--worktree path:<absolute path>` is accepted by the installed CLI; the `id:` form is documented there as `id:<repo-id>::<path>`, which was not equated with the contract's `id:<worktree id>`." |
| G8 | Underpins WC-6's "brief is immutable" rationale | Trace `send --to dispatch:<id>` delivery timing in the launch code (read-only) or live | "The contract's argument against sending a retry brief by `send` was not traced to launch code." |
| G9 | The resume check (`:267`) needs a stored graded tree | Closed: `refs/qa.md:134` | n/a (closed; mapping of the contract phrase to the pinned tree is an inference) |
| G10 | Fan-in cap (`:273`) | Closed: `commands/adversarial.md:3,15,39,58,169` | n/a (closed) |
| G11 | A stale UNVERIFIED label invites needless caution | Owner decision on whether to drop the contract label; both Orca help texts answer it | "Both Orca sources state that several `--wait` calls on one Run inbox get the same Delivery; the contract still labels it UNVERIFIED." |
| G12 | If no step loads the contract, section 4 has no reader | Read the ccsession hooks and Orca launch path for contract injection (read-only), or observe a coordinator start (needs live session, out of scope) | "No hook or startup step that loads `WORKER-CONTRACT.md` into a coordinator session was found in the three hook scripts and `hooks.json`; other injection paths were not searched." |
| G13 | Deployed behavior decides real enforcement | needs live Orca, out of scope | "Orca deployed behavior, running coordinator behavior and hook ordering were not observed." |
| G14 | Hidden Orca coupling in `tests/swarm` would matter | Closed | n/a (closed) |
| G15 | "Not pinned" must be exact for the reference | Closed for the searched tokens | n/a (closed) |
| G16 | Section 5 holds the brief template every coordinator copies | Closed by section 11 | n/a (closed) |

## 9. Stale-documentation list

- `research-notes.md:9`: "273 lines" for `WORKER-CONTRACT.md` (actual 327, `wc -l` in fix cycle 1; section 5 spans `:283-327`). The assignments in `research-notes.md:31-36` were drawn from the stale count, which is why section 5 was uninvestigated until section 11. `research-notes.md` is an input document and was not edited.
- `WORKER-CONTRACT.md:110`: `worktree ps --agent-wait` is NOT stale against the installed build files (accepted: `cli/specs/core.js:157-161`); it is absent from the Orca development checkout `main` (`dc57b3d6e`, SD-1). Same wording is carried in `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md:164,245` and flagged as a supervision surface in `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/research/04-hooks-guards-identity.md:99` (historical). Any reference that calls the verb wrong would itself be stale.
- `WORKER-CONTRACT.md:303,305,307` (section 5 slot rules): P0 framing ("At P0 no command accepts it", "The `P0 only:` line is used only before P1", "no command accepts it at P0") is stale in practice: 31 commands accept `--unattended` (16 P1 + 15 P2), so the `P0 only:` template line has no live use. The wording is deliberately pinned by `tests/skills/test_worker_contract.py:360-367` (`brief-template` phrases), so it cannot be edited without editing the test (section 11).
- `.venv/lib/python3.11/site-packages/superclaude/_src/superclaude/core/WORKER-CONTRACT.md` (210 lines): stale packaged copy; do not cite it.
- `WORKER-CONTRACT.md:194-200` UNVERIFIED list: item "two consumers on one mailbox" is answered by both Orca help texts (dev checkout `orchestration.ts:120`, installed `cli/specs/orchestration.js:118`) (G11).
- `HOW-WE-WORK.md:396-406` "Orca coordination" omits the WC-6, liveness and `/sc:implement` freeze rules; a reader of that guide alone would not learn them.
- `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 9 decision table is the design record for D1-D5; it is HISTORICAL/design and its section references (for example "section 2.3" for the coordinator at spec `:402`) differ from the contract's current layout, where coordinator rules are section 4.

## 10. Summary

Section 4 of the worker contract describes, in prose, a complete coordinator lifecycle: new-Task-per-retry, a nine-type `check --wait` loop with batch acking, a 5-minute sweep feeding an S0-S11 state table and an L0-L5 ladder with caps, a resume-note restart, brief and worktree rules, result admission, an `/sc:implement` freeze and fan-in. Every one of these is an instruction to an LLM session; the checkout contains no code that runs the loop, and its tests only check that the wording is present. The Orca premises behind retries and waiting match both the Orca development checkout and the installed build files (task-update flags, `--retry-of`, 3-failure circuit breaker, `--types` wake and whole-batch replay); the two sources differ on `worktree ps --agent-wait` (accepted by the installed files, absent from the older checkout, recorded as state divergence SD-1, not a defect), and Orca's breaker refuses only `--retry-of` starts, which WC-6 forbids, so the coordinator's own comparison is the only guard. The `/sc:implement` Ruling and freeze text cross-checks against the executor skill, the brief template in section 5 (`:283-327`, section 11) matches sections 3-4 but still carries P0 wording, and the single real hook only requires `--agent` on `orca worktree create`, failing open. Subordinate mode is deferred and not shipped; the running Orca build is not observed.

## 11. Coordinator brief template (`WORKER-CONTRACT.md:283-327`; added in fix cycle 1)

Why this section exists: the first pass drew its assignments from the stale 273-line count in `research-notes.md:9`; the contract is 327 lines (`wc -l`), so section 5 (45 lines, `:283-327`) fell outside every research file. Evidence class: NORMATIVE (instruction text read by the coordinator LLM), cross-checked against checkout source (`tests/skills/test_worker_contract.py`, `src/superclaude/commands/*.md`) and the `ccsession-tag` README. Read in full in this cycle: `WORKER-CONTRACT.md:53-94, 200-327`.

### 11.1 What the section holds
| Lines | Content |
|---|---|
| 283-285 | Heading "5. Coordinator brief template"; instruction: copy into each Task's spec, one brief per Task, fill every angle-bracket slot; guard line copied word for word and placed before the first `Command:` line |
| 287-297 | The text block: Guard line (`:288`), Chain line (`:289`), `On a blocked gate:` (`:290`), `Local commit:` (`:291`), `Report directory:` (`:292`), `Worktree:` (`:293`), `Outward actions:` (`:294`), `P0 only:` (`:295`), `Command:` (`:296`) |
| 299-305 | Slot rules for blocked-gate, local commit, `--unattended` (P0 / P1 16 commands / P2 15 commands) and the `P0 only:` line |
| 307-327 | Flags the brief must pass: intro sentence (12 ready commands plus 5 P2 rows = 17 rows) and the 17-row table |

### 11.2 Template fields against sections 3-4
| Check | Result | Evidence |
|---|---|---|
| The seven brief contents of section 4 (`:83-91`) each have a template slot | Match. Command lines = `Command:`; report dir = `Report directory:`; gate policy = `On a blocked gate:`; local commit = `Local commit:`; P0-only report file = `P0 only:`; "no other outward action" = `Outward actions: none; ...`; worktree placement = `Worktree:` | `:83-91` vs `:288-296` |
| Guard line text equals `Brief layout` guard line; Chain line equals the layout chain line | Identical strings | `:207` = `:288`; `:213` = `:289`; pinned by `GUARD_LINE` (`test_worker_contract.py:376-380`) and `brief-chain-line` (`:368-373`); guard-before-first-`Command:` pinned by `test_brief_template_puts_guard_line_before_first_command_line` (`:916`) and the mutation tests `:1094-1110` [CODE-VERIFIED] (text pins only) |
| `Worktree:` slot agrees with the child-worktree rules | Agrees: `--worktree new-child --base-branch <feature branch>` with `--setup <skip \| run (only when named in the user's instruction)>` matches `:91` and `:221` | `:293`, `:91`, `:221` |
| `On a blocked gate:` values agree with WC-3 | Agrees: `report blocked` (default) or `ask the coordinator` | `:301` vs `:53-55` |
| `Local commit:` agrees with WC-9 and decision D4 | Agrees: `not authorized`, or `authorized` plus the user's instruction quoted word for word | `:302` vs `:88`, `:42-43` |
| Slots the template lacks but sections 3-4 use | (a) no slot for the L4 resume note, which `:167-180` places "after the guard line and before the `Command:` lines of the new Task's brief"; (b) no `replaces T1` line, used by the worked example (`:280`); (c) no per-Task `--comment` placement text (that is a `worker-start --comment` argument, `:222`, not a brief line). Not defects: the template says "fill every angle-bracket slot", and these lines are specified elsewhere | `:167-180`, `:280`, `:222` |
| Brief tells coordinators to pass a session name (`CCSESSION_NAME`) | NO. `grep -n -i ccsession WORKER-CONTRACT.md` returns nothing (count 0; the case-insensitive search also covers `CCSESSION_NAME`). The ccsession README advises "Orchestrators should always pass the task or a name in the launch" (`src/superclaude/skills/ccsession-tag/README.md:344-347`; table row `:281`). Practical effect is small (inference): a `worker-start` brief is a task on the command line, which the README says starts the worker without the name question (`:344-347`) | Closes the question raised in research/06 F2; see research/06 gap U2 |

### 11.3 Slot rules and the P0 / P1 / P2 wording
- `:303` "At P0 no command accepts it [`--unattended`]. From P1 the 16 commands converted in P1 do (adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test)". The list equals `P1_COMMANDS` (`tests/skills/test_worker_contract.py:395-412`, 16 names, same order) [CODE-VERIFIED].
- `:304` "From P2 the 15 commands converted in P2 accept `--unattended` too (auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot)". Equals `P2_COMMANDS` (`:416-432`, 15 names, same order) [CODE-VERIFIED]. Re-run in this cycle: `grep -l '^## Unattended mode' src/superclaude/commands/*.md | wc -l` printed 31 (16 + 15).
- P0 framing is stale in practice: `:303` "At P0 no command accepts it", `:305` "The `P0 only:` line is used only before P1, when no command writes a worker contract ... From P1 the line is dropped and WC-5 applies", `:307` "`--report-dir` is marked 'from P1': no command accepts it at P0", and `:295` itself. All 31 commands are converted, so the `P0 only:` line has no live use; the table cells "(from P1)" (`:314, :319, :320, :327`) read as historical. The `P0 only:` fragments are pinned by `RULE_PHRASES["brief-template"]` (`:360-367`: `--report-dir is marked "from P1": no command accepts it at P0` and `P0 only: Report file: ...`), so the wording cannot be cleaned up without editing the test. [CODE-VERIFIED] staleness; recorded in the stale list (section 9). Also, `WORKER-CONTRACT.md:89` (section 4) and `:59` (WC-5) carry the same P0 conditionals.

### 11.4 The 17-row flag table against the command files
Read in this cycle: the `Report directory.` bullet of every row's command (`src/superclaude/commands/<name>.md`) and the `Person-mode flags.` bullet of adversarial, brainstorm and release-split.
- Directory-flag cells agree for all rows that name one: `/sc:adversarial` `--output <dir>` (`adversarial.md:158`: exactly one of `--output` or `--report-dir`); `/sc:auggie-review` `--output-dir` (`auggie-review.md:143`); `/sc:brainstorm` `--output` (`brainstorm.md:153`); `/sc:cleanup-audit` `--report-dir` only (`cleanup-audit.md:95`); `/sc:cli-eval` `--output-dir` plus `--report-dir` (`cli-eval.md:82`); `/sc:cli-portify` `--report-dir` (`cli-portify.md:118`); `/sc:graph` `--output-dir` (`graph.md:64`); `/sc:impact` `--output-dir` (`impact.md:60`); `/sc:index-repo` `--report-dir` (`index-repo.md:188`); `/sc:init-lite` `--output <file>` plus `--report-dir` (`init-lite.md:91`); `/sc:review-translation` and `/sc:spec-panel` `--report-dir` (`review-translation.md:91`, `spec-panel.md:456`); `/sc:workflow` `--report-dir`, `--output` retired (`workflow.md:71`).
- Rows whose cell names no directory flag, relying on the general rule at `:307` ("exactly one report directory"): `/sc:tdd` (`tdd.md:165`: `--report-dir` only, `--output` names the TDD file), `/sc:troubleshoot` (`troubleshoot.md:174`: exactly one of `--output-dir` or `--report-dir`), `/sc:reflect` (`reflect.md:263`: exactly one of `--output` or `--report-dir`), `/sc:release-split` (`release-split.md:115`: exactly one of `--output` or `--report-dir`). Consistent, not contradictory.
- "never `--interactive`" in the adversarial, brainstorm and release-split rows matches their `Person-mode flags.` bullets (`adversarial.md:160`, `brainstorm.md:155`, `release-split.md:117`: `--interactive` and `-i` refused). [CODE-VERIFIED]
- Not re-read this cycle (each cell [UNVERIFIED] against its command file): `/sc:graph` "never `init`", `/sc:reflect` `--remediate` allowed and `--no-promote`, `/sc:review-translation` `--context <file>`, `/sc:spec-panel` `--target-release`, `/sc:cleanup-audit` `--pass <N>`, `/sc:cli-portify` `--resume <contract>`, `/sc:workflow` `--handoff none`, `/sc:troubleshoot` no `--fix` and short `--depth deep` input. The command flags are pinned in part by `UNATTENDED_EXPECT` entries (for example `--target-release` at `test_worker_contract.py:577`, `--remediate`/`--no-promote` at `:714`), not by the table.
- The table itself and the slot rules are not pinned by `RULE_PHRASES` (read `:360-373`) nor by the template helpers (`:748-790`, `:916`, `:1094-1110`); a search of `tests/` for table-cell phrases (`handoff none`, `never \`init\``, `--pass <N>`) found only unrelated hits. Other helpers in the 3195-line file were not searched exhaustively: "not pinned" is [UNVERIFIED] beyond those searches.

### 11.5 Result
Section 5 is consistent with sections 3-4 and with the command files read; its weaknesses are P0 wording that tests pin, no resume-note or `replaces` slot, and no session-name advice. Nothing here is a DEFECT: no document claims code enforces the brief, and the guard line and Chain line are pinned as text. Subordinate/sub-orchestrator mode is deferred and absent from section 5.

**Status:** Complete
