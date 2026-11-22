# Worker Supervision Through Evidence and Idempotent Recovery

## Overview and Goals

**Recommendation:** use an evidence ledger and a bounded probe loop, not a heartbeat-expiry restart policy. Keep progress, process reachability, human attention, delivery and outcome as separate facts. The coordinator is the only authority allowed to settle an attempt or authorize its replacement.

This is a proposed design, not implementation or a claim of runtime validation. Source citations are repository-relative to `/home/coder/workspaces/IronClaude`. `E` below abbreviates `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/enrichment/codebase-context.md`; `I` abbreviates `.dev/issues/431/issue-body.md`; `C` abbreviates `src/superclaude/core/WORKER-CONTRACT.md`. Citations such as `E:14-23` name those exact files and lines. Enrichment is secondary evidence from documented command help, not a live-worker test (`E:12-23`); unspecified Orca runtime behavior remains **UNVERIFIED**.

The observed failures include misleading continuing heartbeats, idle sessions, missed closing messages, unseen answers, permission prompts and repeated context exhaustion (`I:14-23`). Current safety rules require top-level lifecycle messages, prohibit command-side Orca fan-out, accept heartbeat gaps during Agent-tool fan-out, and require settled prior attempts before retries (`C:38`, `C:44`, `C:58-61`, `C:69-74`). These are constraints, not defects to remove.

- **FR-001:** classify every active attempt and unresolved reply within a bounded supervision cycle; surface unknown rather than manufacturing healthy state.
- **FR-002:** detect idle, person-blocked and context-thrashing conditions within 15 minutes when required adapters are available; surface adapter/host failure within 5 minutes otherwise. Detection and a report are bounded; recovery and human decisions are not.
- **FR-003:** consume every message type and confirm answer reading at application level, independently of mailbox acknowledgement.
- **FR-004:** preserve on-disk work and single-attempt ownership through nudges, coordinator restarts and replacement Tasks. No destructive action on elapsed time alone.
- **NFR-001:** no inferred success, permission grant, cancellation or duplicate execution from silence, file activity or UI text alone. Default toward preserving work.
- **NFR-002:** start with existing read/probe surfaces and contract wording; add only the durable supervisor state, adapter normalization and acknowledgement conventions needed for enforceable bounds. No dashboard, new messaging broker or custom Orca message type is required.

## Worker State Model

**FR-005:** key all state by `(run_id, task_id, dispatch_id)` and a supervisor-owned `attempt_epoch`. Epoch is a proposed local fencing value, not an Orca field. A replacement gets a new Task and Dispatch, and an old sender can never advance its replacement. Retain old evidence for audit.

The following names are harness-neutral **derived supervision states**, not Orca enums. Maintain separate `reachability`, `attention`, `last_progress`, `delivery` and `outcome` facts underneath them. Missing or conflicting evidence makes state `unknown`, with last-known state shown separately. Person-blocked and ask-blocked take precedence over apparent idle; an explicit context error takes precedence over apparent activity; accepted settlement takes precedence over all nonterminal states. Preserve concurrent facts instead of discarding them.

| State | Entry evidence | Exit condition / allowed transitions |
|---|---|---|
| `starting` | Dispatch is assigned; worker evidence not yet confirmed | Fresh worker evidence → progressing or a blocked state; boot budget expires → unknown/probe, never automatic failure |
| `progressing` | New semantic checkpoint, completed tool/step evidence or worker progress claim with changed revision | Long operation declaration → long-step-in-progress; idle/prompt/context/exit evidence → corresponding state; stale evidence → unknown |
| `long-step-in-progress` | Top-level session declares an active operation and finite inspection deadline, or adapter confirms active tool/child execution | Completed operation → progressing; deadline → probe/unknown unless renewed with evidence; explicit blocker/exit overrides declaration |
| `idle-at-prompt` | Two prompt-idle observations, unfinished assigned work, no person-only prompt or pending ask | Observed turn starts → progressing/long-step; discovered completion claim → finished-unreported; disappearance → unknown |
| `blocked-on-person-prompt` | Fresh person-only prompt evidence associated with this dispatch | Person resolves prompt and adapter observes continuation → progressing; exit → unreachable/exited. Never auto-approve |
| `blocked-in-ask` | Durable pending question associated with this attempt; worker or transcript confirms waiting | Read-ack of answer → progressing only after continuation evidence; answer without ack leaves delivery pending; timeout retains same question |
| `context-exhausted/compact-thrashing` | Explicit fatal context/thrashing message, or repeated compaction-loop suspicion confirmed by bounded transcript/screen inspection | Evidence of useful resumed work → progressing; positive stall proof plus settled old attempt → replacement starting; unresolved → person |
| `unreachable/exited` | Reachability dimension distinguishes fresh positive exit proof from failed/unsupported observations | Unreachable → unknown until refreshed; exit → settled failure only through settlement gate; reappearance without new assignment restores observations, not replacement authority |
| `finished-unreported` | Final worker text/closing message claims completion without accepted worker_done | Contract validated and top-level worker_done received → settled; claim retracted or missing output → probe/failed through authorized path, never inferred success |
| `settled` | Valid worker_done and coordinator result disposition, or positive stall proof and confirmed cancellation settlement | Terminal for attempt; late messages recorded, never reopen it |
| `unknown` | Stale, missing, conflicting or unsupported probes | Fresh confirming evidence → any applicable state; report lack of coverage after bound |

**FR-006:** classify from current evidence, not cumulative activity counts. A timer heartbeat can coexist with context exhaustion. `unreachable/exited` is not a combined kill permission: only the exited branch supplies exit proof. Documented Orca liveness distinguishes `live`, `unverifiable` and `exited`; a live terminal need not contain a working agent (`E:18-20`).

## Signals and Adapters

**FR-007:** normalize evidence before classification; distinguish `unsupported`, `probe_failed`, `absent` and `present`. Never turn missing evidence into false. Documented Orca surfaces and their limitations are recorded in `E:14-24`, `E:58`, `E:64-72`.

| Signal / source | Proves / does not prove | Cost and brittleness | Core vs adapter |
|---|---|---|---|
| Progress-bound heartbeat from top-level session | A session claims a specific revision of completed progress; does not prove acceptance, output correctness or current activity | Low bandwidth; model can repeat or fabricate counters. Validate against referenced checkpoints on escalation | Core revision semantics; Orca heartbeat `--payload <json>` carrier |
| Whole-worktree activity, file metadata/change inventory | Something changed in the worktree; not necessarily this worker, not useful progress, not proof of no blocker | Moderate initial scan, incremental afterward; large trees and remote mounts costly; shared writers confound attribution | Optional filesystem adapter, never sole evidence |
| Terminal classification | Rendered prompt/error was observed; not inherently authoritative completion or exit proof | Bounded screen read; high sensitivity to localization, stale scrollback and harness versions | Claude Code/terminal adapter; core receives typed observations |
| Transcript timestamps and semantic entries | New timestamped records exist; semantic completion may prove tool or turn completion; timestamp growth alone can be loop activity | Incremental bounded tail; parsing/version drift, missing metadata timestamps, indexing lag | Harness adapter; never infer a transcript path; use resolved worker source |
| Per-step deadline | An expected checkpoint is overdue; not proof of deadlock or exit | Cheap local timer; poor estimates produce false alarms | Core, supervisor-owned inspection deadlines, not kill leases |
| All-type wait and periodic non-wait drain | Delivered batch was read by coordinator; not proof worker read a reply | Cheap, subject to queue volume; explicit list can miss future types unless unconditional drain exists | Orca adapter; core catch-all routes unknown values |
| Explicit read acknowledgement | The assigned top-level worker parsed a named answer and durably recorded its disposition; not proof it completed the action | Small message and durable dedup entry; worker may be unable to emit during blocking work | Core protocol in heartbeat payload; transport ack remains separate |
| Process / ask / person-prompt observations | Exit proof, pending ask, or person attention as individually observed | Cheap fleet read plus targeted probes; host gaps, null-vs-absent differences | Orca projection/agentWait adapter; core preserves evidence freshness |

**FR-008: proposed heartbeat payload.** Use only the existing heartbeat `--payload <json>` field; task/dispatch identity also uses the existing heartbeat `--task-id` and `--dispatch-id` where the preamble provides them (`E:14`). No new CLI flags are proposed. Heartbeat transport cadence remains entirely the preamble's decision. New revisions are emitted at the next allowed top-level checkpoint/cadence opportunity; a timer may repeat the payload, but must never increment progress solely because time passed.

```json
{
  "schema": "ironclaude.supervision.v1",
  "kind": "progress",
  "run_id": "run-example",
  "task_id": "task-example",
  "dispatch_id": "dispatch-example",
  "attempt_epoch": 1,
  "seq": 7,
  "step_id": "stage-2",
  "progress_rev": 3,
  "mode": "long_step",
  "operation": "review fan-out",
  "inspect_after_seconds": 600,
  "checkpoint_path": "stages/stage-1.json",
  "checkpoint_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "pending_question_id": null
}
```

All fields required. `schema` and `kind` are literal strings; IDs/step/operation are bounded strings; `attempt_epoch` is positive integer; `seq` is an increasing positive integer per attempt and payload emission; `progress_rev` is a nonnegative integer increasing only after new completed work; `mode` is `working|long_step|blocked_ask|finished`; `inspect_after_seconds` is integer 60..900, measured from coordinator receipt, not permission to extend an absolute stage budget; checkpoint fields are both strings or both null; digest is 64 lowercase hex characters; question ID is string or null. `seq` measures message revision, not progress. Epoch is copied from the brief; workers cannot mint one. Bind payload IDs to authenticated transport assignment, reject mismatches, preserve unknown schema as diagnostic rather than accepting progress.

**FR-009:** allow long-step evidence to postpone an intrusive nudge, never the five-minute observation sweep. Repeating a long-step declaration cannot extend a deadline: an extension needs a new semantic child/tool observation and coordinator-recorded reason. Commands and child agents write ordinary checkpoint files, never heartbeats; only the top-level worker reads those files and reports them. Existing WC-7 and fan-out exception remain intact (`C:44`, `C:58-61`).

**NFR-003:** inventory the entire assigned worktree incrementally, including untracked output, bounded to 100 ms normally and 2 seconds for a targeted probe. Exclude `.git`, caches, virtual environments, dependencies and supervisor telemetry by explicit configuration. Track creation, deletion and rename; mtime alone misses some changes. Report incomplete scans as partial. Hash only a small referenced checkpoint on confirmation; never rescan all contents every cycle. In shared worktrees, label changes `unattributed`. These are new adapter requirements; their availability is UNVERIFIED.

## Detection Rules and Time Bounds

**FR-010:** run supervision independently of message traffic: unconditional mailbox drain at least every 1 minute; full active-attempt sweep every 5 minutes; per-worker probe timeout 30 seconds; confirmation within 1 minute of suspicion. Waits must yield to the earliest due timer, so frequent heartbeats cannot starve sweeps. Do not perform worker probes serially across the whole fleet. The mailbox wait wake set includes all nine known types, with unconditional drains providing future-type safety.

**NFR-004:** use coordinator monotonic time for elapsed budgets and UTC for audit. Persist original due times and action counters before acting. After restart or host suspension, immediately sweep overdue attempts; do not reset deadlines from replayed messages. The bounds below assume the supervisor is scheduled, can finish each sweep inside its five-minute budget and has a functioning relevant adapter. If it cannot, emit `coverage_degraded` within one sweep and report to the person by minute 10. Never promise to identify a remote worker's exact state during host loss.

| State | Trigger | Confirming probe | Maximum detection / first response, minutes |
|---|---|---|---|
| starting | No first worker evidence by minute 5 | Assignment, fleet liveness, terminal/transcript if present | 6 to classify unknown and report startup concern; no automatic retry |
| progressing | No semantic revision for 10 minutes, even with heartbeats | Current screen/transcript plus worktree attribution | 11 to classify concern; if still opaque report by 15. Quiet reasoning may remain unknown, not falsely stalled |
| long-step-in-progress | Declared inspection deadline or absolute stage budget expires | Tool/child evidence and screen/transcript; worktree secondary | Deadline + 1; default inspection at 10, hard maximum inspection at 15. Long stages remain allowed with evidence and recorded renewals |
| idle-at-prompt | First fresh prompt-idle sample with unfinished assignment | Second sample within 1 minute; exclude person prompt/ask | 6 from onset; one continuation nudge by 7, report recurrence/no continuation by 10 |
| blocked-on-person-prompt | Positive person-only prompt sample | Refresh agentWait or bounded rendered prompt read | 6 to classify and notify person; no automated approval; unresolved age continues |
| blocked-in-ask | Question delivery; or adapter sees active wait | Correlate original question ID, answer state and final worker text | 1 from message enqueue, otherwise 6 via sweep; unanswered question gets coordinator disposition/person report by 10, not forced resolution |
| context-exhausted/compact-thrashing | Explicit current error; or 3 compaction starts in 10 minutes without semantic progress | Current screen and timestamped transcript; repeated-loop heuristic alone remains suspicion | Explicit error ≤6; heuristic ≤11; response/report ≤12. No kill from heuristic |
| unreachable/exited | Failed fleet probe, unverifiable observation or positive exit | Independent reachability refresh; distinguish process exit evidence from transport failure | ≤6 to classify exit/unknown, ≤10 to report uncovered host; replacement needs settlement gate |
| finished-unreported | Closing claim on any type, or final transcript turn | Read known contract and ask top-level session for canonical completion if still available | Message ≤1, transcript-only ≤6; correction nudge by 7, report by 10 |
| unknown | Unsupported/stale/conflicting observation | One alternative source, then preserve unknown | ≤6 to surface; person report ≤10; no repeated silent waiting |

**FR-011:** an incident's detection timer starts with onset visible to the adapter, not when the coordinator happens to notice it. Tests must insert failures immediately after a sweep to exercise worst-case latency. Optional signals may improve precision but their absence cannot suppress the mandatory sweep. Progress changes clear a suspicion only when they postdate it and actually address its evidence; a new file timestamp cannot clear a prompt or context error.

## Mapping of the 8 Observed Cases

**FR-012:** replay all eight reported cases as independent acceptance scenarios. These are historical reports, not newly reproduced failures (`I:16-23`). Bounds assume adapter availability as defined above.

| Case | State | Detecting signal | Detection bound, minutes | Response |
|---|---|---|---|---|
| 1: #339 initial context saturation; unchanged timer heartbeats (`I:16`) | context-exhausted/compact-thrashing | Current explicit thrash error; semantic revision flat despite timer messages | 6 explicit, 11 heuristic | Save references, inspect final transcript, report; replace only after positive proof and settlement |
| 2: #339 replacement idle for hours, later idle again (`I:17`) | idle-at-prompt | Two prompt-idle samples plus unfinished stage | 6 | One continuation nudge; recurrence consumes retained nudge budget and reports, rather than indefinite nudges |
| 3: #331 judged alive from a recent file change (`I:18`) | idle-at-prompt | Prompt-idle samples override unattributed worktree activity | 6 | Nudge once and require actual continuation evidence; do not reset incident on file mtime |
| 4: #361 closing report sent as status (`I:19`) | finished-unreported | All-type wake and one-minute unconditional mailbox drain | 1 (one wait/drain cycle) | Read report; request canonical worker_done; never treat status as Task settlement |
| 5: #331/#375 answered mailbox, unseen for 35–40 minutes (`I:20`) | blocked-in-ask, answer pending read | Missing exact answer read-ack after durable answer send | 2 to suspect, terminal copy by 5, report by 10 | Probe prompt/ask identity, one exact terminal copy where safe, no new answer or ask ID. Root cause remains UNVERIFIED |
| 6: #394 permission prompt (`I:21`) | blocked-on-person-prompt | Fresh agentWait or current permission screen | 6 | Notify person with prompt evidence; never type an approval |
| 7: #339/#331 turn ended between chain steps (`I:22`) | idle-at-prompt; long-step-in-progress is alternative until confirmed | Turn-boundary/prompt observations versus active tool/child evidence | 6 for idle; default long-step concern 11 | Nudge continuation of existing assignment; correct worker chain duty; do not run a second copy |
| 8: #339 repeated autocompact thrashing (`I:23`) | context-exhausted/compact-thrashing | Current error plus retained incident history and unchanged checkpoint | 6 | Resume note mandates bounded reads; repeated same-checkpoint cause trips restart budget and reports to person |

Detecting case 8 does not authorize the historical clear/restart action automatically. Data preservation and the WC-6 settlement gate still apply. No inference about the actual cause of case 5 is needed for a bounded read-ack timeout.

## Message-Type Coverage

Documented types and wait semantics are in `E:14-17`. **FR-013:** wake on every currently supported type and drain without a type restriction at each one-minute timer. Whether omitting a wake filter itself means all future types is UNVERIFIED; the design therefore does not rely on that interpretation. Process the whole returned FIFO batch, never just the type that woke it. Unknown types remain visible and actionable; do not manufacture an Orca `unknown` type or wildcard flag.

| Existing Orca type | Proposed coordinator handling | What it never implies |
|---|---|---|
| status | Preserve content; inspect for closing/blocker claim; finished-unreported if appropriate | Canonical settlement, progress or read acknowledgement from free text |
| dispatch | Associate with authorized Task/Dispatch; flag unexpected assignment/epoch | Permission to launch work not created/authorized by this coordinator |
| worker_done | Dedup, read contract, apply outcome mapping and admit/discard outputs | Deliverable correctness merely because transport accepted message |
| merge_ready | Read referenced result and surface owner action | Authorization to merge or release resources |
| escalation | Create/refresh attention incident; correlate existing blocker | Permission to bypass a gate |
| handoff | Validate referenced paths and current owner; preserve resume context | Transfer of ownership solely from a message |
| decision_gate | Surface to authorized decision-maker; track original age and disposition | Approval from timeout or another agent |
| question | Bind original question ID and one-answer/read-ack lifecycle | A fresh question every timeout |
| heartbeat | Validate progress/read-ack schema; update corresponding dimension only | Healthy task from repeated heartbeat, or progress from an ack |
| any unknown value | Persist raw bounded message, notify coordinator, surface unsupported semantics within 1 minute | Safe to discard, auto-execute or classify as success |

**FR-014:** canonical outcome remains worker_done from the top-level session under WC-5 (`C:57-59`); a closing status/handoff is an immediate recovery concern, not an alternate completion API. If the worker is available, request its missing canonical report once. If it has exited, preserve its report, settle only through the documented positive-proof route, and require a separate verification/disposition before dependents use outputs. Never impersonate the worker by synthesizing worker_done.

**NFR-005:** durably store the incoming delivery, its constituent messages and pending routing actions before acknowledging the transport batch. Use stable transport message identity when available; exact identity representation and redelivery behavior are UNVERIFIED and require adapter conformance tests. Locally assign observation IDs without claiming they are Orca IDs. If persistence fails, do not acknowledge. After restart, replay unfinished actions idempotently; processing heartbeat floods must not starve blockers or timer work. Coalesce heartbeat display only after durable receipt, never by skipping a mixed FIFO batch.

## Reply Read-Acknowledgement Protocol

**FR-015:** distinguish `answer_pending → answer_enqueued → read_confirmed → continuation_observed → resolved`. Reading is not acceptance, acceptance is not execution, execution is not verified completion. Existing send success proves durable enqueue, not reading; `check --ack` acknowledges the reader's own delivery batch (`E:16`). The reply body carrier is existing `reply --id <msg_id> --body <text>` (`.dev/orca-command-refactor/inventory/orca-capabilities.md:62-66`), also checked with read-only help during this design. New JSON fields below are application conventions, not Orca fields.

Coordinator writes an immutable answer record before sending its exact JSON serialization in reply `--body`. The reply targets the existing question's ID. Proposed payload:

```json
{
  "schema": "ironclaude.supervision.v1",
  "kind": "answer",
  "run_id": "run-example",
  "task_id": "task-example",
  "dispatch_id": "dispatch-example",
  "attempt_epoch": 1,
  "question_id": "question-example",
  "answer_id": "answer-example",
  "answer_text": "Use the existing documented default.",
  "answer_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
```

All keys required. Schema/kind are literal; identities, question ID and answer ID are nonempty strings of at most 256 UTF-8 bytes; epoch positive integer; answer text string at most 4096 UTF-8 bytes; digest 64 lowercase hex characters, SHA-256 of exact UTF-8 `answer_text`, with no whitespace or newline normalization. Larger answers use a short instruction naming a validated artifact; artifact content is separately checked, not silently treated as hashed answer content. The enclosing assignment/transport identities must match the payload. An answer is immutable once sent: conflicting decisions require explicit review, never replacement under the same ID.

**FR-016:** after the worker's blocking ask returns, the top-level session parses the answer, validates assignment and digest, durably records its input disposition in an attempt-scoped sidecar, and emits this JSON through existing heartbeat `--payload` before re-invoking/resuming command work. The negotiated dispatch preamble must permit this immediate control acknowledgement; normal progress heartbeat cadence still comes only from that preamble. No heartbeat is required or sent while ask is still blocking. If a preamble cannot carry this protocol, record `ack_unsupported` and use the bounded manual fallback; do not claim protocol support. WC-3's single eligible ask, same-message timeout resume and Ruling exclusions are unchanged (`C:53-56`).

```json
{
  "schema": "ironclaude.supervision.v1",
  "kind": "read_ack",
  "run_id": "run-example",
  "task_id": "task-example",
  "dispatch_id": "dispatch-example",
  "attempt_epoch": 1,
  "question_id": "question-example",
  "answer_id": "answer-example",
  "answer_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "disposition": "accepted_input",
  "reason": null
}
```

All keys required; identity/digest types as above. `disposition` is `accepted_input|rejected`; `reason` is string (maximum 512 UTF-8 bytes) or null, mandatory nonempty for rejection. `accepted_input` means parsed and accepted as a permitted command input, not authority to bypass permissions. An ack with a different digest, epoch, question or authenticated sender is rejected and surfaces a conflict. A rejection confirms reading but leaves the task blocked; it does not resolve the question. A duplicate answer returns the exact stored original acknowledgement, including its disposition and reason; there is no ambiguous third disposition for duplicates.

**FR-017: deadlines and terminal fallback.** Start the timer at first confirmed enqueue, not at last resend. After 2 minutes without matching read-ack, probe current ask/prompt and ownership. By minute 5, if a terminal-backed worker is at a confirmed safe agent input prompt, type one literal copy of the original answer JSON plus a fixed instruction to acknowledge that answer ID, never a new decision. Carrier: existing terminal send `--text` with `--enter`; optional `--wait-submit` provides turn-start evidence, not reading (`E:23`). Do not use interrupt. If ask still owns terminal input, a permission prompt is present, input semantics are ambiguous, or no terminal exists, do not type: report that fallback is unsafe/unavailable by minute 5. At minute 10 without read confirmation, notify the person and preserve `answer_enqueued/read_unknown`. Adapter and person availability are not falsely described as delivery success.

**FR-018: idempotency.** Dedup key is `(dispatch_id, attempt_epoch, question_id, answer_id)` and digest is immutable. Replaying identical mailbox/terminal copies returns the stored ack without repeating command invocation. Persist `input_recorded`, then `invocation_started`, then resume checkpoint/outcome; after a crash between start and completion, inspect command resume evidence instead of blindly invoking again. Exactly-once side effects across a process crash are NOT promised. An ambiguous in-flight invocation blocks automatic replay and goes to the coordinator. Duplicate acks are harmless; never acknowledge an acknowledgement. Settled attempts reject new answers; late answers transfer only by a new Task. Acks from an older attempt are audit records only. Terminal copies are data, never shell interpolation or permission approval.

## Response Ladder

**FR-019:** apply the lowest sufficient action, retain incident identity through repeated heartbeat traffic, and persist action intent before external effects. Escalation need not traverse unsafe steps: a permission prompt goes directly to the person; an exited worker skips a meaningless nudge.

1. **Probe:** refresh assignment/ownership, fleet liveness, person-wait/ask and one bounded screen/transcript sample. Maximum two probes per incident, one minute apart; further read-only periodic monitoring continues without repeating intervention.
2. **Nudge:** only at a positively identified agent input prompt, send one idempotent continuation instruction for the existing assignment. No interrupt, shell text, automatic Enter on a permission dialog or second command instance. Wait at most 3 minutes for a real turn/progress observation.
3. **Ask:** request a concise state/checkpoint/blocker description from a safely reachable worker; use the same control envelope with `describe_state`, not a second blocking worker ask. If no safe worker input channel exists, ask the person directly. One such request per incident, report unresolved by minute 10 (or minute 15 for an initially opaque progress concern). Existing worker asks keep WC-3's at-most-one rule (`C:54-56`).
4. **Restart with resume note:** only after a fresh documented positive stall proof, confirming the observed final turn is complete rather than merely a quiet tail, and after ownership reconciliation, output inventory, cancellation/stop confirmation and old-Task settlement. Then create a new Task with a fresh report directory and predecessor link. Never run a replacement while stop/settlement is uncertain or liveness unverifiable. This preserves WC-6 (`C:69-74`); supported proof classes are documented in `E:20`. A context error alone is NOT an additional Orca stall-proof class.
5. **Report to person:** include original incident age, confirmed state versus unknown, evidence timestamps, attempted actions, current owner, preserved checkpoint and the precise decision needed. Human resolution has no automatic timeout. Continue supervision after reporting; do not silently abandon or retry.

**FR-020: caps.** One nudge per incident, no more than two nudges per attempt; one clarification request per incident. New incident IDs cannot reset attempt caps without new semantic progress. Replacement budget: one automatic replacement per logical work item in a rolling 60-minute window, two over that item's entire predecessor lineage. The same context-thrash cause recurring at the same checkpoint after a mitigation gets no second automatic replacement. Retain the existing ceiling of three failed starts for effectively unchanged commands (`C:71`); the stricter limit wins. Person approval to extend a budget does not waive settlement, permission, Ruling or outward-action rules.

Control envelope, carried as JSON in existing terminal send `--text` only at a safe prompt (`E:23`):

```json
{
  "schema": "ironclaude.supervision.v1",
  "kind": "control",
  "run_id": "run-example",
  "task_id": "task-example",
  "dispatch_id": "dispatch-example",
  "attempt_epoch": 1,
  "action_id": "incident-example:nudge:1",
  "action": "continue_assignment"
}
```

All fields required; identities and action ID are nonempty strings ≤256 UTF-8 bytes; epoch positive integer; action enum `continue_assignment|describe_state|report_completion`. Worker dedups `action_id` within its attempt. These actions cannot change the immutable brief or rerun a completed command. A state description is reported by the next valid progress heartbeat (`operation` describes the blocker) or canonical completion; no new transport type is introduced.

**FR-021: resume note.** Coordinator writes immutable `resume-note.json` inside the new report directory and names its absolute path in the new Task brief, not in a follow-up to the old dispatch. This is a proposed local artifact, not an Orca payload field. It uses this complete shape:

```json
{
  "schema": "ironclaude.resume.v1",
  "logical_work_id": "work-example",
  "previous_task_id": "task-old",
  "previous_dispatch_id": "dispatch-old",
  "proof_ref": "evidence/exit-1.json",
  "settlement_ref": "evidence/settlement-1.json",
  "worktree_path": "/absolute/assigned-worktree",
  "command": "/sc:example <unchanged permitted arguments>",
  "completed_steps": ["stage-1"],
  "next_step_id": "stage-2",
  "checkpoint_refs": [
    {"path": "/absolute/preserved-checkpoint", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
  ],
  "pending_answer_ids": [],
  "uncertain_effects": [],
  "reason": "Context thrashing confirmed; original attempt settled.",
  "mitigation": "Read at most 80 lines per call; resume from stage-1 summary.",
  "replacement_count": 1
}
```

Required fields; schema literal, remaining scalar text strings (IDs/step ≤256 bytes; paths ≤4096; command/reason/mitigation ≤4096), arrays of bounded strings, checkpoint refs array of `{path:string, sha256:64-hex-string}`, replacement count nonnegative integer. `next_step_id` may be null if only result verification remains. Proof and settlement refs must resolve to actual recorded observations; no invented proof document suffices. Nonempty `uncertain_effects` forbids automatic replay until reconciled. Pending answers are historical references, not transferable authorization. Resume uses only the command's verified existing resume interface; an unsupported command requires person guidance, not an invented flag.

**NFR-006: durable action safety.** A local transactional ledger owned by one supervisor stores observations, message dedup, timers, immutable answers, predecessor mapping and action intent/result. Use atomic transactions and unique keys for `(attempt, action_id)` and `(attempt, answer_id)`. An external request and a local transaction cannot be assumed atomic: after timeout/crash, reconcile the recorded target and current Orca assignment before another call. Uncertain Task creation or worker start means stop automatic replacement and report, not create another Task. No claim of existing Orca exactly-once API semantics is made.

**What never happens on silence alone:** stop, clear, kill, cancel, retry, release, mark success, admit a dependency, approve a permission, write a Ruling or delete work. A nudge is never permission to cross a blocked gate.

## Worker-Side Rules

**FR-022:** keep lifecycle duties in the top-level worker wrapper, ordinary work/resume duties in commands, and syntax/cadence in the version-matched preamble. Current role separation is explicit (`C:5-7`, `C:58-61`); command sections point to shared rules rather than duplicate them (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:1013-1026`). This proposal does not turn arbitrary chains into one Task or weaken the brief guard.

| Rule | Where it lives | Required behavior |
|---|---|---|
| Do not end a turn between authorized chain/stage steps | Contract worker-session duties; command's own chain logic | If the next authorized step is runnable, continue in the same turn. Before any deliberate yield, have canonical completion, recorded blocker or a declared live long operation. A summary in chat is not a handoff |
| Run the actual command | WC-7; command/skill invocation rules | Invoke the command's required Skill through the Skill tool at top level. Reading its definition alone is not execution. Preserve permitted internal fan-out; never wrap the whole command in a helper |
| Bounded context reads | Shared command execution rule; command's own resume notes identify essential sections | Start with stage summary/index, then read ≤80 lines per file read and bounded log tails. Do not ingest every prior report after compaction. A long physical line still needs byte/token limits and tool-supported extraction; line count alone is insufficient |
| Stage handoff before moving on | Command owns local artifact; contract requires listing it | Write a small complete checkpoint after each durable stage; record next step, outputs, checks and unresolved effects. Never call Orca from command or helper |
| Progress/read-ack transmission | Top-level session and negotiated preamble only | Read command checkpoint, preserve revision, send heartbeat/ack at preamble-authorized opportunities; no background heartbeat impersonating model progress |
| Inbox checks and answer dedup | WC-12 / WC-3 top-level duties | Pull at natural checkpoints, after ask returns and before worker_done. If fenced, stop without further lifecycle messages; never continue using stale ownership (`C:59`) |
| Long calls | WC-10; command implementation | Preserve ≤4-minute single blocking Bash waits; retain accepted longer Agent-tool fan-out, with top-level operation declaration when feasible. A fan-out gap alone is never a violation (`C:44`) |
| Stop/outcome | WC-2 / WC-4 / WC-5 | Command records blocked/failed/partial/succeeded; top-level sends canonical completion. No automatic retry of a frozen implement plan (`C:30-37`, `C:57`, `C:125`, `C:132-142`) |

**FR-023: checkpoint format.** Proposed `stages/<step_id>.json` files live inside the command's own report directory, are listed in `artifacts`, and are published atomically only when complete. Retain previous revisions or digest-addressed copies so a heartbeat reference cannot silently point at rewritten bytes. This is local command data, not a message or a new Orca field.

```json
{
  "schema": "ironclaude.stage.v1",
  "step_id": "stage-1",
  "progress_rev": 3,
  "state": "completed",
  "summary": "Inputs checked; next stage can use the validated report.",
  "artifact_paths": ["report.md"],
  "verification_refs": ["checks/input-check.txt"],
  "next_step_id": "stage-2",
  "resume_instruction": "Read summary, then the requested report sections.",
  "uncertain_effects": []
}
```

All fields required. Schema literal; step IDs strings ≤256 bytes, next step string or null; progress revision nonnegative integer; state `completed|blocked|failed|partial`; summary/resume instruction strings ≤2048 UTF-8 bytes; artifact/verification/effect fields arrays of bounded strings. Artifact and verification paths are relative to the report directory unless explicitly validated against the assignment's permitted source/worktree roots. This checkpoint has no run identity or lifecycle authority: the top-level session wraps it in its assigned heartbeat. A checkpoint with no verification records does not claim tests passed.

**NFR-007:** preserve existing command resume semantics and report status fields. Never overwrite a blocked/halted ledger, rename a command's `status`, manufacture an eligible Ruling, or treat a mitigation note as approval. `worker_contract_version` remains `"1"` for unchanged WC-4 reports; supervision schema versions are independent (`C:32-33`, `C:55`).

## Contract Changes: v1 Now vs v2 (#423)

**FR-024:** ship clarifying policy before claiming machine-enforced deadlines. The v1 contract can require coordinator sweeps and safer worker behavior now; enforceable timers, durable dedup and adapters belong to the v2 supervision workstream. The present contract gives preamble ownership of cadence/syntax (`C:7`, `C:49`), accepted fan-out gaps (`C:44`), top-level lifecycle ownership (`C:58-61`) and new-Task-only retries (`C:69-74`). Preserve all four.

| Concern | v1 contract/policy now | v2 machinery / release gate |
|---|---|---|
| All message types | Coordinator uses all known wake types, inspects whole batch, checks mailbox on bounded waits | Timer-driven unconditional drain, unknown-type handling, durable routing and starvation tests |
| Prompt, idle, context checks | Coordinator reads existing documented probes at least each five-minute sweep; explicit unknown on unavailable probes | Adapter classifiers, repeated evidence, freshness, independent watchdog and measured bounds |
| Read confirmation | Require worker to state which answer it read at first legal checkpoint; coordinator manually tracks pending reading and safe terminal fallback | Negotiated JSON schemas, immediate preamble-authorized read-ack, durable answer IDs/digests and replay suppression |
| No turn-ending gaps | Shared worker continuation duty for already-authorized steps | Resume-aware wrapper, event-backed idle detection; no compulsory hook installed by this design |
| Context safety | Bounded reads and concise stage notes in eligible commands | Standard checkpoint schema and adapter-assisted context-loop detection, rolled out command by command |
| Retry safety | Preserve WC-6; apply manual lineage budget and include resume note | Transactional action ledger, fencing, crash reconciliation and budget enforcement across coordinator resumes |
| Outcome authority | Any closing type triggers report inspection, but only worker_done settles normally | Durable admission and conflict handling, late-message rejection; never synthetic success |

Proposed normative wording, appended to the named rules rather than replacing their safeguards:

| Rule amended | Proposed wording | Delivery |
|---|---|---|
| WC-2 (`C:30`) | “Between runnable authorized stages, continue without ending the turn. A yield for a real blocker records that blocker in the command contract; do not yield merely to announce the next step.” | v1 wording; commands preserve their gate behavior |
| WC-3 (`C:51-56`) | “After an eligible answer returns, the top-level session records the original question and answer identity before re-invocation, confirms reading at its next permitted reporting opportunity, and never applies the same answer twice. Timeouts resume the original question. Reading an answer does not grant a Ruling or person permission.” | v1 duty; v2 exact ack schema and deadline negotiation |
| WC-4 (`C:31-37`) | “A multi-stage command preserves concise stage checkpoints and lists them in artifacts. Checkpoints are not worker completion and do not replace return-contract.yaml. Use only the command's documented resume input.” | v1 principle; v2 opt-in concrete schema, no global command conversion assumed |
| WC-5 (`C:57`) | “The top-level worker sends canonical worker_done before ending its assignment. A closing status, handoff or chat statement is not a substitute. The coordinator treats a missing canonical completion as finished-unreported, reads the report and requests correction once; it never fabricates worker_done.” | v1 wording; v2 dedup/reconciliation |
| WC-6 (`C:69-74`) | “Record the predecessor lineage, proof, settlement and resume note for every replacement. Apply the stricter of failed-start and lineage restart budgets across new Task IDs. Uncertain stop, settlement or creation forbids another automatic attempt.” | v1 policy; v2 durable action ledger |
| WC-7 (`C:58`) | “The top-level session invokes the command's required Skill directly; reading its definition alone is not running it. Progress and read acknowledgements are lifecycle messages and never originate from helper agents, commands or background timers.” | v1 clarification; accepted internal fan-out unchanged |
| WC-10 (`C:44`) | “A missing or unchanged heartbeat triggers bounded observation and, when safe, a nudge or request for state; it never proves death. Preserve the four-minute Bash limit and accepted Agent-tool gaps. Stop, retry and release still require Orca's positive stall proof and WC-6 settlement. Heartbeat cadence and syntax remain preamble-owned.” | v1 clarification; v2 timed probes and semantic revisions |
| WC-11 (`C:45`) | “Telemetry and stage checkpoints have one writer each and live in the assigned report directory. Whole-worktree changes without attribution are supporting observations only and cannot certify worker progress or ownership.” | v1 clarification; v2 inventory attribution |
| WC-12 (`C:59`) | “Pull follow-ups after natural checkpoints, after a blocking ask returns, and before worker_done. Record/read-ack relevant answers before continuing. A safely typed duplicate answer has the same identity and is not applied again. On consumer_fenced stop without further lifecycle sends.” | v1 duty; v2 durable dedup and negotiated ack |

**WC-8, WC-9 and WC-13 are not relaxed or amended**: commands remain free of Orca calls, outward-action restrictions remain, and only the coordinator creates workers/Tasks (`C:5`, `C:38-43`, `C:60`). No hook or helper sends a lifecycle message. Proposed new coordinator subsection “Supervision and recovery” holds sweep cadence, all-type routing, bounds, caps and proof gates; the Heartbeats bullet gains a cross-reference to the negotiated schema, not a copied heartbeat interval or CLI recipe.

Maintenance locations are the contract source and corresponding guide summary in this repository; installed instructions refer to `~/.claude/WORKER-CONTRACT.md` and the project `.claude/` fallback, never assume another project has this repository's source tree. Exact future preamble changes and their Orca integration are **UNVERIFIED**, so strict JSON protocol support is a v2 release gate, not a capability asserted for existing workers.

## Portability and Extension Points

**FR-025:** core code knows only assignment identity, evidence, monotonic deadlines, persisted incidents and allowed transitions. It never matches Claude Code screen strings or constructs an Orca CLI command. Adapters expose the following proposed in-process contracts; these names are NOT existing APIs:

| Adapter method | Request / result contract | Safety |
|---|---|---|
| `capabilities()` | Supported observation kinds and `can_submit_text`, `can_read_transcript`, `can_resolve_exit_proof`, `supports_read_ack`, each boolean | Capability false produces explicit unsupported, not empty healthy state |
| `observe(assignment, cursor)` | Assignment identity plus optional opaque string cursor → bounded list of observations, next cursor string/null, `complete:boolean` | Read-only; ≤30 seconds; partial coverage preserved |
| `receive_messages(deadline)` | Supervisor monotonic due time → delivery identity and messages with raw type, transport sender/target identity, body and optional payload | Whole-batch durable ingestion; no type silently removed |
| `ack_delivery(delivery_id)` | Previously persisted transport delivery identity → acknowledged or uncertain | Does not mark application read; never dashboard-driven consumption |
| `submit_text(assignment, action_id, text)` | Current assignment, persisted action ID, bounded literal text → `accepted|turn_started|rejected|uncertain` | Safe prompt and current ownership preconditions; turn_started is not read_confirmed |
| `reconcile(assignment, action_id)` | Target and action ID → known outcome or uncertain | Mandatory after ambiguous side effects; never assume a timeout failed |

Settlement and creation remain coordinator-authorized actions under the existing Orca preamble/guide, not classifier side effects. A non-Orca adapter must supply equally strong ownership and settlement semantics before automated replacement can be enabled. Unsupported replacement leaves observe/nudge/report available where safe.

**FR-026: normalized observation payload.** This JSON is a proposed internal adapter response stored in the local ledger; it is NOT sent over Orca and has no existing Orca carrier field:

```json
{
  "schema": "ironclaude.observation.v1",
  "observation_id": "observation-example",
  "run_id": "run-example",
  "task_id": "task-example",
  "dispatch_id": "dispatch-example",
  "attempt_epoch": 1,
  "source": "terminal",
  "kind": "person_prompt",
  "availability": "present",
  "source_at": null,
  "observed_at": "2026-11-07T20:00:00Z",
  "fresh_for_seconds": 120,
  "evidence_ref": "evidence/observation-example.json",
  "proof_kind": "none"
}
```

Required fields. Schema literal; IDs bounded strings as above; epoch positive integer; source `orca_projection|terminal|transcript|filesystem|worker_payload`; kind `process_live|process_exit|prompt_idle|person_prompt|ask_pending|tool_active|semantic_progress|compaction|context_error|final_turn_without_done|activity|unknown`; availability `present|absent|unsupported|probe_failed`; source_at UTC string/null; observed_at UTC string assigned by supervisor; freshness integer 0..300; evidence_ref string/null; proof kind `none|positive_exit|final_turn_without_worker_done`. New observation kinds must degrade to unknown unless recognized. Non-present availability requires proof none. A proof must reference timestamped, assignment-bound evidence, not just a classifier label. Core receives monotonic receipt time separately from JSON audit timestamps.

First adapter mapping: `projection.liveness` and `observation.agentWait`; resolved worker transcript; safe terminal screen/submit observations; optional worktree inventory. Documented null agentWait means looked-and-none, absent field means never looked (`E:19`); `unverifiable` remains unknown (`E:18`). No new Orca field is introduced. Timestamps require scanning back past metadata, and transcript discovery uses the worker-reported source rather than guessed paths (`E:58`).

Other harnesses can provide tool-start/end and turn-idle events instead of screen parsing. Exact event availability, terminal submission behavior and permission callbacks for other harnesses are **UNVERIFIED**. Hooks may contribute local observations only after separate approved integration and tests; they never become heartbeat senders. Adding a harness changes adapter code and fixtures, not state safety rules or answer identity.

## Risks, False Positives and Edge Cases

**NFR-008: observation cannot become authority.** Screen/transcript text and worker payloads are untrusted. Validate sender assignment, schema, IDs, enums, size (maximum 16 KiB per supervision payload), JSON depth (maximum 8), paths and digest before state updates. Reject duplicate JSON keys. Unknown fields can be retained as diagnostics but cannot modify actions. A digest proves content equality, not who approved it. Never execute strings read from transcripts, payloads, resume notes or a suggested next action without current ownership and policy checks. This follows the separation recommended by the earlier dashboard research (`.dev/research/orca-dashboard-20261105/REPORT.md:75-77`).

| Risk / edge | Required treatment |
|---|---|
| Long reasoning, tool call or accepted child fan-out | Continue observation; expiry opens concern, not death. Do not inject into an active tool or fabricate child heartbeats |
| Timer heartbeats or compaction generate activity forever | Keep semantic revision separate from message sequence and transcript growth; unchanged revision cannot erase the context/prompt incident |
| Prompt classifier mistakes ordinary text or old scrollback for a prompt | Require current frame, assignment association and confirmation sample. Ambiguous prompt permits report, not typing |
| Normal compaction repeats legitimately | Loop heuristic only raises suspicion. Require explicit current error or further semantic evidence before classifying context exhaustion; no restart on count alone |
| Person-only prompt not visible in adapter | Unsupported/unknown with degraded coverage, not all-clear. Person report remains bounded, exact state is not guaranteed |
| Shared worktree / hook / person writes a file | Attribute if possible, otherwise unattributed support only. Recent mtime never cancels positive idle/blocker evidence |
| Active file changes lack useful progress, or pure research changes no files | Semantic checkpoint/terminal/tool observations remain primary; no required file-churn quota |
| Host loss / partial fleet pagination / stale projection | Retain last-known state and explicit omitted coverage; group one connectivity incident with affected assignments. Never treat remote absence as exit |
| Out-of-order heartbeat, old ack or late worker_done | Dedup by attempt identity/revision; keep old records, never reopen settled attempt or overwrite authoritative replacement. Conflicting outcome is a surfaced integrity incident |
| Ack sent but worker crashes before continuing | Reading remains confirmed; execution is unknown. Recover from invocation/checkpoint evidence, never infer completed action from ack |
| Worker applies input but crashes before ack | Persist input disposition first; duplicate returns prior ack. If actual effect is ambiguous, block automatic replay and reconcile |
| New prompt appears between safety probe and terminal submit | Narrow race remains; if adapter cannot make prompt-bound submission safe, disable automatic typing. Never fall back to interrupt or a permission key |
| Coordinator crashes after start/stop/create succeeded | Replay action intent by reconciliation, not reissuing commands. If target cannot be uniquely found, report uncertain effect and halt replacements |
| Two coordinators supervise the same run | Require exclusive run controller lock plus current Orca ownership validation. Lock/ownership loss pauses all mutation and reports; a local epoch cannot fence an unrelated live remote writer |
| Frozen command plan or uncertain output paths | Preserve worktree and ledger; no replacement that resumes frozen work without existing person hand-back rules. A resume note cannot waive a freeze |
| Unknown message type or malformed payload | Retain bounded raw evidence, surface semantics unknown, route other valid messages; poison input cannot block mailbox drain |

**NFR-009: observability.** Expose last successful sweep, oldest unprocessed delivery age, read-ack age, probe duration/failure count, missing coverage, incident age, action count, replacement lineage budget and settlement ambiguity. Record every state transition with evidence references and policy version. Alert when no sweep completes for 6 minutes or mailbox age exceeds 2 minutes; the watchdog must run outside a blocked coordinator turn. Timer-based watchdog support is proposed, not an existing verified feature.

Use low-cardinality metric labels (state, adapter, action, result); Task/Dispatch IDs belong in audit logs, not metric labels. Persist only bounded sanitized excerpts and evidence references, with restricted local access. Retain supervisor records through active work and at least 7 days after settlement; do not automatically delete worktrees, reports or user artifacts. Retain dedup tombstones until every pending action is reconciled and the lineage is closed, even if ordinary telemetry expires. Redact secrets and permission-dialog sensitive arguments before logging or showing them to another observer.

**NFR-010:** storage-full, ledger corruption, unsupported schema or controller ownership uncertainty fails closed for mutation while read-only observation and person reporting continue. Do not acknowledge unpersisted deliveries, reset restart budgets or invent replacement epochs to escape an integrity error.

## Acceptance Criteria and Open Questions

**FR-027: release acceptance.** The following are required tests for implementation, not tests claimed to have run during this design:

1. Replay all eight historical cases, injected just after a sweep. Record onset, evidence receipt, classification and first response. Meet each table bound; unsupported adapters report unknown/coverage degradation within the stated bound instead of passing a detection test with no evidence.
2. With unchanged timer heartbeats arriving continuously, independently detect a current thrash error and a permission prompt within 6 minutes. Heartbeat volume cannot reset incident age or starve sweeps.
3. Demonstrate a legitimate 30-minute Agent-tool fan-out without top-level heartbeats: sweep/probe/report may occur, but no automatic stop/retry/release or duplicate command. Renewed long-step evidence never disables observations.
4. Enqueue each of the nine known types, an unknown type and mixed FIFO batches. Every message is durably routed within 1 minute; a closing status enters finished-unreported without settling success or starting dependents.
5. Drop read-ack, then show suspicion at minute 2 and one safe terminal copy by minute 5. If prompt safety is unknown, show fallback-unavailable escalation by minute 5 instead. Unresolved reading reaches the person by minute 10. Turn-start receipt alone must not pass read confirmation.
6. Deliver answer duplicates by mailbox and terminal, out of order, across coordinator/worker restart. One stored input disposition and no blind second invocation; conflicting digest/epoch/sender rejected; settled worker rejects late input; ack never generates ack traffic.
7. Crash at every persistence/external-effect boundary: before/after enqueue, delivery ack, input recording, invocation start, stop, Task settlement, Task creation and worker start. Reconcile or report uncertainty; never accidentally create a concurrent authoritative replacement or erase restart counts.
8. Prove safety gates: heartbeat lateness, stale projection, unchanged transcript, ambiguous prompt, context-loop count and remote outage each independently produce zero destructive actions. Valid positive exit/final-turn proof still requires ownership check, stop confirmation and settlement before replacement.
9. Verify budget lineage across new Task IDs: a same-checkpoint thrash recurrence stops automatic recovery; more than one replacement/hour or two/lifetime is refused; unchanged failed-start ceiling remains enforced.
10. Verify no Orca/lifecycle calls in commands/helpers; required Skill invocation occurs at worker top level; no ordinary turn yield between runnable stages; blocked/frozen plans remain stopped. Checkpoints and resume notes retain required files and never overwrite an old attempt's report directory.
11. Run at least two harness-adapter fixtures against the same core state machine, including one with no terminal, transcript or read-ack support. Unsupported features remain explicit; exact-state bounds are claimed only for an adapter that passes conformance.
12. Stress the supervisor at six workers and at the supported fleet limit with host outages and message floods. Sweep duration stays ≤5 minutes, mailbox drain ≤1 minute, targeted probe ≤30 seconds; exceeding capacity produces a watchdog alert and coverage degradation, never silent all-clear. Test storage failure, clock jump, partial paging, corrupt payload, symlink/path escape and controller lock loss.

**NFR-011:** do not enable automatic replacement in production until crash-boundary and ownership tests pass. Enable observing/reporting first, then safe nudges, then proof-gated replacement; collect classification corrections, false-nudge counts, ack delays and preserved-work incidents before broadening permissions. No numeric reliability percentage is asserted without measured data.

Open questions and explicit verification gates:

- **UNVERIFIED:** how the running preamble can advertise protocol version, supervisor epoch and immediate heartbeat-carried read-ack permission. Strict ack support requires that integration; existing progress payload and sender-receipt gaps are documented in `E:64-65`.
- **UNVERIFIED:** whether unfiltered check reliably returns unknown future types, exact message identity persistence/redelivery rules and queue saturation behavior. Require adapter tests rather than assuming broker semantics.
- **UNVERIFIED:** whether a terminal submission can bind input atomically to a proven-safe prompt. Until proven, automatic terminal copying is enabled only for tested adapter/prompt combinations and otherwise replaced by a bounded person report.
- **UNVERIFIED:** which projection attention categories, if any, cover compact thrashing; no classifier may depend on undocumented category names (`E:67`).
- **UNVERIFIED:** durable final-turn boundary and source freshness details needed to establish Orca's final-turn-without-worker_done proof. Never use an arbitrary transcript tail or screen-idle sample as that proof.
- **UNVERIFIED:** available run-controller ownership/fencing and side-effect reconciliation surfaces across remote hosts. A local transactional ledger is not a distributed fencing service; fail closed for automatic replacements if another writer cannot be excluded.
- **UNVERIFIED:** measured fleet size/cost budget and a viable independent watchdog scheduler. Six-worker acceptance is necessary but not a scaling claim.
- **UNVERIFIED:** root cause of the two unseen mailbox answers and availability of all command-specific resume interfaces. The protocol detects missing reading without guessing that cause; unsupported resume remains a person decision.
- Rollout ownership: this design separates v1 supervision policy from v2 durable machinery; maintainers must explicitly allocate the machinery work and review preamble compatibility. No existing field is silently repurposed as ownership, approval or verified completion.

Design confidence is high for the safety invariants and data contracts; actual timing, parsing and transport behavior require the tests above. No live-worker experiment, hook installation, implementation, git mutation or GitHub write is part of this deliverable.
