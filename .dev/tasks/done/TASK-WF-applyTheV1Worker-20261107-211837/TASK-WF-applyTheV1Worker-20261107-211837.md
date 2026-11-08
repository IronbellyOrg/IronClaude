---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-applyTheV1Worker-20261107-211837
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# Apply the v1 worker-liveness contract text (issue #431)

Source: ./source.md

Goal: `src/superclaude/core/WORKER-CONTRACT.md` carries every v1 liveness row (C-1 to C-8 and C-15 to C-17) from section 10 of `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md`, and `tests/skills/test_worker_contract.py` pins the key sentence of each new rule, with `make lint`, `make verify-sync` and `uv run pytest tests/skills` passing.

## Constraints

- Edit only `src/superclaude/core/WORKER-CONTRACT.md` and `tests/skills/test_worker_contract.py`. No code beyond tests; nothing for the v2 monitor, adapters, hooks or dashboard.
- The contract has no other copy in the repo (no `plugins/superclaude/core/` copy, no level-table copy in `HOW-WE-WORK.md`), and `make sync-dev` / `make verify-sync` do not cover `core/`; both still run before the PR.
- Use the exact wording of section 10.2 of the design (read it in pieces of at most 80 lines). One adaptation: C-2's "in the preamble command's payload or phase text" becomes "in the heartbeat's subject or phase text, or a `status` body line", because the heartbeat verb takes typed flags (`--type heartbeat --subject alive --task-id --dispatch-id --phase`) and has no custom payload field.
- Every new pin is a `RULE_PHRASES` entry `"<name>": (<ident or None>, [<phrases>])` whose phrases appear verbatim in the contract; when an ident is given, one contract line must hold both the ident and the first phrase. `test_contract_states_rule` and `test_rule_check_fails_when_rule_removed` then cover it with no new test function.
- Existing pins must keep passing: WC-10 ("at the cadence its preamble sets", "split into waits of at most 4 minutes"), WC-5, WC-7, WC-12, WC-3, WC-6, heartbeats, brief-layout, brief-template, and the guard-before-`Command:` check.
- Statements the design marks unverified are written as UNVERIFIED in the contract text, never as fact: what `check --wait` wakes on without `--types`; the cause of case 5, answers not seen (lead: `orca orchestration reply` stores type `status` with subject "Re: Question", so a narrow `--types` waiter may miss it); whether a permission-prompt or compact-thrashing attention category exists; what Claude Code does with text typed while a tool call runs; whether two consumers on one mailbox both get a batch.
- Owner decisions of 2026-11-07 are binding: never resend a mailbox copy of an answer; the worker confirms an answer with an ack; with no ack after 5 minutes and a probe that positively shows an empty idle prompt, the coordinator types ONE copy into the terminal; at 15 minutes it reports to the person. A person-directed cancellation with confirmed quiescence settles a live attempt; context exhaustion alone is not proof.
- `unverifiable` liveness is absence and never authorizes stop, abandon, retry or release.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `./artifacts/` included. Never stage `.claude/` mirrors.
- Evidence logs go under `./artifacts/`.

## Phase 1: Command-side rules (contract section 2)

## Task 1: Replace the WC-10 closing sentence (C-1) and extend WC-11 (C-17)

In `src/superclaude/core/WORKER-CONTRACT.md` section 2, replace the last sentence of WC-10 ("The coordinator therefore treats a missing heartbeat as absence, never as death: it never stops, retries or releases a worker because a heartbeat is late, and it acts only on Orca's stall proofs.") with the C-1 wording from design section 10.2: absence is never death; stop, retry or release only on Orca's stall proofs or the person's recorded stop under WC-6; absence past the deadline in "Liveness supervision" (section 4) authorizes only read-only probes, a typed nudge and a direct question to the worker, in that order; a worker that announced a long step with `expect_silence_min` gets no nudge or typed text before that window ends, while read-only probes still run. Append the C-17 sentence to WC-11: "The coordinator's liveness `stat` reads only the worker's own contract path and report directory." Add `RULE_PHRASES` pins in `tests/skills/test_worker_contract.py` for both.

Acceptance criteria:
- WC-10 keeps its first three sentences unchanged and ends with the C-1 text; the old phrase "it acts only on Orca's stall proofs" is gone.
- WC-11 ends with the C-17 sentence.
- `RULE_PHRASES` gains a WC-10 absence pin (for example "never as death" and "authorizes only read-only probes, a typed nudge and a direct question") and a WC-11 liveness-stat pin; `uv run pytest tests/skills/test_worker_contract.py -q` passes.

## Phase 2: Worker-session duties (contract section 3)

## Task 2: Add the heartbeat progress token (C-2)

In `src/superclaude/core/WORKER-CONTRACT.md` section 3, after the first sentence of the **Heartbeats** bullet, insert C-2 from design section 10.2 with the typed-flag adaptation: each heartbeat carries a progress token in the heartbeat's subject or phase text, or a `status` body line: the current `Command:` line index and a count that rises only when on-disk progress rises (WC-15), plus `expect_silence_min` before a step expected to outlast the cadence. Keep the sentence "A heartbeat whose token has not changed is evidence that the process exists, not that the work is progressing." Add a `RULE_PHRASES` pin.

Acceptance criteria:
- The Heartbeats bullet still starts "The worker session sends heartbeats at the cadence its preamble sets" and now carries the progress-token text, naming subject, phase or `status` body line and never a payload field.
- A pin covers "progress token" and "evidence that the process exists, not that the work is progressing"; the existing heartbeats pin still passes.

Depends on: Task 1

## Task 3: Extend WC-12, WC-3, WC-5 and WC-7 (C-3a, C-3b, C-4, C-16)

In `src/superclaude/core/WORKER-CONTRACT.md` section 3, append the design section 10.2 text:
- to WC-12 (C-3a): the worker handles every message in a `check` batch before acknowledging the batch; for each coordinator message that answers or directs it, it first sends `status` with a body starting `ack <message_id> applied|queued|refused`, then acts; a message ID already applied gets only `ack <message_id> applied (duplicate)`;
- to the WC-3 `ask` timeout bullet (C-3b): when `ask` returns, the worker sends one heartbeat at once, and when the answer arrives it sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command;
- to WC-5 (C-4): the closing report is never sent as `status`, `handoff` or a reply, and a coordinator may not read those as completion;
- to WC-7 (C-16): a worker runs each chained `Command:` by invoking its Skill, and reading the command file and following it from memory does not satisfy WC-7.

Add one `RULE_PHRASES` pin per rule.

Acceptance criteria:
- Each of the four rules ends with its new text, and the existing WC-12, WC-3, WC-5 and WC-7 pins still pass.
- Four new pins exist, each carrying a key phrase from the added text (for example "applied (duplicate)", "sends one heartbeat at once", "never sent as `status`, `handoff` or a reply", "does not satisfy WC-7").

Depends on: Task 2

## Task 4: Add WC-14 and WC-15 (C-5, C-6)

In `src/superclaude/core/WORKER-CONTRACT.md` section 3, add two new bold rule bullets with the design section 10.2 wording: **WC-14. No turn ends between chain steps.** (the worker session ends its turn only after `worker_done`, while blocked in the preamble's `ask`, or on `consumer_fenced`; when a `Command:` line finishes, the next action in the same turn is the next `Command:` line or the WC-5 steps after the last one) and **WC-15. Context-safe reading and handoff files.** (read files of unknown size and prior reports, logs and transcripts in pieces of at most 80 lines, never reread a whole prior report; after each `Command:` line write `<report-dir>/handoff/<n>-<command>.md`, at most 40 lines, with the command line, Task ID and Dispatch ID, `worker_status`, deliverable paths, decisions, applied message IDs and the next `Command:` line, and list it in `artifacts`). Add pins with idents `WC-14` and `WC-15`.

Acceptance criteria:
- Both bullets exist in section 3 with their bold titles on the same line as the ident.
- Pins with ident `WC-14` and `WC-15` pass, and removing either rule's phrases makes `_check_rule` raise (covered by `test_rule_check_fails_when_rule_removed`).

Depends on: Task 3

## Phase 3: Coordinator rules (contract section 4)

## Task 5: Add the live-attempt settlement bullet to WC-6 (C-15)

In `src/superclaude/core/WORKER-CONTRACT.md` section 4, subsection "WC-6. Every retry is a new Task", add the C-15 bullet from design section 10.2: a live attempt (its terminal still open) settles only when the person directs its cancellation and the coordinator has confirmed quiescence (no tool running, no input accepted, and two reads 5 minutes apart that agree); context exhaustion, heartbeats and the coordinator's own nudges are not stall proofs; a message from a settled or replaced attempt is logged and shown to the person, never applied. Add a pin.

Acceptance criteria:
- The WC-6 list holds the new bullet and the four existing WC-6 phrases still pass.
- A pin covers "person directs its cancellation" and "never applied".

Depends on: Task 4

## Task 6: Add the "Liveness supervision" subsection (C-7)

Add a `### Liveness supervision` subsection to section 4 of `src/superclaude/core/WORKER-CONTRACT.md` (after "What the coordinator owes each worker" or another place that keeps section order readable), summarising design sections 4, 6, 7 and 8:
- the wait: `check --wait` listing all nine types (`status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat`) with `--timeout-ms 300000`; `--types` only decides when a waiter wakes; a Delivery is the whole FIFO batch, replayed until `--ack` and shared by several waits on one Run inbox; every message is handled and a run-notes line is written per message ID before `--ack`; an unknown type is shown, never silently acked; lifecycle messages are checked against the current Task and Dispatch ID and a mismatch is quarantined;
- the sweep after every wake or timeout, at most once every 5 minutes: one `worker-list`, one prompt-wait listing, one `stat` per worker contract path (WC-11), costly probes only for triggered workers, the deadline W, and "after three empty waits, enumerate with `worker-list`";
- the state table (starting, progressing, long step, idle at prompt, blocked on a person prompt, blocked in `ask`, context exhausted, unreachable, exited, finished but unreported, done, unknown) with the coordinator's response for each;
- the ack timeline of owner decision (a): no blind mailbox resend; one typed copy only on a positively identified idle empty prompt after 5 minutes without an ack; report to the person at 15 minutes; never type into a busy, unknown or person-prompt session;
- the response ladder L0 to L5 with its caps and the restart budget, including the C-7 sentence from design section 10.2: "When the ladder is exhausted, the coordinator reports to the person (L5). It restarts a worker (L4) only on one of Orca's positive stall proofs (`exited`, the process exit, or a transcript whose final agent turn sent no `worker_done`), or on the person's recorded stop, and then settles it under WC-6. Nudges, asks, heartbeats, repeated identical reads and context exhaustion are never stall proofs.";
- the nudge text and the resume note placed in the new Task's brief after the guard line and before the `Command:` lines;
- the never-on-silence list (no stop, retry, release, failed mark, answer to a person-only prompt, Ruling, or lifecycle message for the worker on silence, a passed deadline, `unverifiable` or screen text alone);
- the five UNVERIFIED items from the Constraints, each labelled UNVERIFIED.

Text blocks inside fences must contain no line that starts with a number followed by "." or ")". Add pins for the subsection heading, the nine-type wait, the C-7 stall-proof sentence, the never-on-silence rule, the owner-decision ack timeline and the UNVERIFIED label.

Acceptance criteria:
- The subsection exists in section 4 and states every item above, with each of the five unverified points marked UNVERIFIED.
- The nine message types and `--timeout-ms 300000` appear on one `check --wait` line; "Nudges, asks, heartbeats, repeated identical reads and context exhaustion are never stall proofs" appears verbatim.
- The new pins pass and `uv run pytest tests/skills/test_worker_contract.py -q` passes.

Depends on: Task 5

## Phase 4: Brief layout, template and evidence

## Task 7: Add the Chain line to the brief layout and template (C-8), then record the checks

In `src/superclaude/core/WORKER-CONTRACT.md`, add the C-8 line from design section 10.2 to the "Brief layout" subsection right after the guard line fence, and to the section 5 brief template between the guard line and the first `Command:` line:

```text
Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
```

Add a pin for the Chain line. Then run `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check tests/skills/test_worker_contract.py`, `uv run pytest tests/skills -q` and `uv run pytest tests -q -x` (or the widest suite that runs here), and save each output to `./artifacts/`.

Acceptance criteria:
- The Chain line appears in "Brief layout" and in the section 5 template, after the guard line and before any `Command:` line, and `_check_guard_before_command` and the brief-layout and brief-template pins still pass.
- A Chain-line pin passes.
- `./artifacts/` holds the sync-dev, verify-sync, lint, ruff format, `tests/skills` and wider-suite logs, each ending in a pass; any pre-existing failure outside the two edited files is named in `./artifacts/wider-tests.log` with evidence that it also fails on `master`.
- A grep for other copies of `WORKER-CONTRACT.md` text under `plugins/` and `src/superclaude/core/HOW-WE-WORK.md` is saved to `./artifacts/copies-check.log` and shows none to update.

Depends on: Task 6
