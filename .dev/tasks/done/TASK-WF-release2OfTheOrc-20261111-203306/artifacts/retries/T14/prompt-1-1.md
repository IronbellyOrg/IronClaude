0c1cb5dd043b55229c9318ba2c6243906fac0cb4
Review one task for spec compliance.

Task brief: 
## Task 14: Build the 100-row cap fixture and its test

Depends on: Task 10

Create `tests/observe/test_question_cap.py` and the fixture builder `make_question_rows(n)` in `tests/observe/conftest.py`, with a recorded-shape fixture `src/superclaude/cli/observe/fixtures/question-cap-100.json` of exactly 100 redacted `question` rows, newest first, shaped like REPORT evidence file 14 (the 104-message probe Run read: exactly 100 rows, the 4 oldest silently missing, no total or truncation field).

Acceptance criteria:
- `uv run pytest tests/observe/test_question_cap.py -v` passes: a 100-row reply sets `window full` and the panel shows `window full: older questions may be missing` and the disclosure label; a 99-row reply does not; two cycles where the second returns a window that has moved on (newest 100 only) keep the dropped questions retained as `no longer in source window` and the open total does not fall; the panel never prints a total taken from `result.count`.
- The test asserts that no argv in the log contains `--peek` and that every message argv has `--types question`.

Global constraints: 
## Constraints

- Shorthand. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. REPORT is the file `RESEARCH-REPORT-phase2-gate.md` in the folder `TASK-RESEARCH-phase2-gate-20261111-200400` under `.dev/tasks/` (the folder may sit in to-do or done); its recorded evidence is the `research/evidence/` folder next to it, files numbered 01 to 27. OWNER is `.dev/issues/409/owner-decisions-20261111.md`. "The probe shapes" are the recorded outputs in REPORT's evidence folder: envelope `{id, ok, result:{acknowledged, count, messages[], runId}, _meta}`; message row keys `id` (msg_...), `run_id`, `delivery_contract`, `from_handle`, `to_handle`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `created_at`, `delivered_at`; error envelope `{ok:false, error:{code, message}}` with codes `consumer_fenced` (exit status 1) and `no_active_terminal`.
- Scope is release 2 only, as fixed by OWNER and REPORT sections 7 to 9. Decision 8: only messages of type `question`, labelled "coordinator questions", never "human". Decision 6: read permission for one named Run, `--types question`, never `run-use`. The owner has not yet named the Run (open question for the owner; Task 17 is blocked until they do).
- Fixed design basis, not reopened. One named Run only; no rotation across Runs; the observer runs where it already holds the Run. Every read passes `--types question`. Only `check --all` is used: `--peek` hides acked rows so it is not a source. Question identity is `message.id`, labelled UNVERIFIED for any Run other than the probe Runs and the coordinator's own Run; a worker `dispatchId` is never a question identity. The disclosure text, verbatim, is `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.
- UNVERIFIED facts that stay gated risks, each with a named verification task and never an assumption. Q-1: whether an observer terminal that has a handle but holds no Run can read (Task 16). Q-2: the effect of `run-use` on a live coordinator (not tested, forbidden for the observer; Task 6 pins `run-use` as a forbidden argv and Task 2 records Q-2 as never tested). Message rate on a Run other than the coordinator's own, and identity on real traffic (Task 17). Whether `ask` writes type `question` (Q-3) is recorded in the register as UNVERIFIED; no R2 behaviour depends on it because the label says "coordinator questions" and the observer lists type `question` rows however they were written.
- Safety. No consuming read (`check` without `--all` or `--peek`, `check --ack`), no `run-use`, `run-create`, `send`, `ask`, `reply` or `reset` against any Run except where a task names a throwaway probe Run and a non-consuming form. Raw Orca output is never logged, committed or exported; committed samples hold only redacted values (no terminal handle, token, credential or absolute path). Bodies of messages are received by the observer process (acquisition cannot be undone by dropping them at parse time), so the design never claims bodies were not acquired; it only does not keep or show them.
- Rules carried from release 1. UV only (`uv run pytest ...`). Python 3.10 compatible, no new dependency. A fact the source does not give is the `UNKNOWN` sentinel and renders as `unknown`; unknown is never 0, false, blank or `null`. Source loss never closes a question, lowers an open count or turns a value into `failed`. Every source string passes `sanitize` before it reaches the view model; strings render as literal text, never Rich markup; truncation uses cell width. Plan edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Out of scope: R3 links (QUESTION-LINK), `inbox`, closure evidence, history beyond the 100-row window, `--include-remote`, write-back, per-question selection and marking (the `m` key keeps its release 1 meaning), any message call other than the one template.
- Plan-author choices (PROPOSED, the owner may change them). The opt-in flag is `--questions`, valid only with `--run <runId>` and a live source. The message call budget is one call per cycle; when questions are on, worker-list paging is limited to 4 calls so the cycle total stays inside the 5-call cap. The panel shows `subject` and age only, never `body`. The reason column reads `reason unknown` because no verified reason field exists. Retention is in memory for the process, bounded at 1,000 records.
- Gate honesty. QUESTION-OBSERVATION is NOT passed as of this plan: proof (a) failed as worded, proof (b) is partly proven, proof (c) is unmeasured, non-consumption passed only as the Run's owner on a probe Run. The live question read is guarded by one constant that Task 18 may flip only against an owner-written record.

Start sha: 0c1cb5dd043b55229c9318ba2c6243906fac0cb4
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/fixtures/question-cap-100.json b/src/superclaude/cli/observe/fixtures/question-cap-100.json
new file mode 100644
index 000000000..9e83277b6
--- /dev/null
+++ b/src/superclaude/cli/observe/fixtures/question-cap-100.json
@@ -0,0 +1,1520 @@
+{
+ "variant": "question-cap-100",
+ "description": "exactly 100 question rows, newest first: the shape of a read that hit the 100-row bound",
+ "cycles": [
+  {
+   "id": "env-cap",
+   "ok": true,
+   "result": {
+    "acknowledged": null,
+    "count": 100,
+    "messages": [
+     {
+      "id": "msg_000000000001",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 102",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:59:00Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000002",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 101",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:59:00Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000003",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 100",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000004",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 99",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000005",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 98",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000006",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 97",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000007",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 96",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000008",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 95",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:58Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000009",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 94",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:58Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000010",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 93",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:58Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000011",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 92",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:58Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000012",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 91",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:58Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000013",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 90",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:57Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000014",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 89",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:57Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000015",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 88",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:57Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000016",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 87",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:57Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000017",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 86",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:57Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000018",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 85",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:56Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000019",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 84",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:56Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000020",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 83",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:56Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000021",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 82",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:56Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000022",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 81",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:56Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000023",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 80",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:56Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000024",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 79",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:55Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000025",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 78",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:55Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000026",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 77",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:55Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000027",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 76",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:55Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000028",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 75",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:55Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000029",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 74",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:54Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000030",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 73",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:54Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000031",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 72",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:54Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000032",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 71",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:54Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000033",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 70",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:54Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000034",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 69",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000035",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 68",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000036",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 67",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000037",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 66",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000038",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 65",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000039",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 64",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:52Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000040",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 63",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:52Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000041",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 62",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:52Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000042",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 61",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:52Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000043",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 60",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:52Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000044",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 59",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:51Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000045",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 58",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:51Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000046",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 57",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:51Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000047",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 56",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:51Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000048",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 55",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:51Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000049",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 54",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:50Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000050",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 53",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:50Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000051",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 52",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:50Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000052",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 51",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:50Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000053",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 50",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:50Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000054",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 49",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:50Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000055",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 48",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:49Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000056",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 47",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:49Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000057",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 46",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:49Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000058",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 45",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:49Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000059",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 44",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:49Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000060",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 43",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:48Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000061",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 42",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:48Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000062",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 41",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:48Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000063",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 40",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:48Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000064",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 39",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:48Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000065",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 38",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:48Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000066",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 37",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:47Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000067",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 36",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:47Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000068",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 35",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:47Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000069",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 34",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:47Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000070",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 33",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:47Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000071",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 32",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:46Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000072",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 31",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:46Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000073",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 30",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:46Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000074",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 29",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:46Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000075",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 28",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:46Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000076",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 27",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:45Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000077",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 26",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:45Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000078",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 25",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:45Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000079",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 24",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:45Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000080",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 23",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:45Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000081",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 22",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:45Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000082",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 21",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:44Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000083",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 20",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:44Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000084",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 19",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:44Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000085",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 18",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:44Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000086",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 17",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:44Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000087",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 16",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:43Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000088",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 15",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:43Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000089",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 14",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:43Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000090",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 13",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:43Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000091",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 12",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:43Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000092",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 11",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:43Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000093",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 10",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:42Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000094",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 9",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:42Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000095",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 8",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:42Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000096",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 7",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:42Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000097",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 6",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:42Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000098",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 5",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:41Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000099",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 4",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:41Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000100",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "cap probe 3",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:41Z",
+      "delivered_at": null
+     }
+    ],
+    "runId": "run-b"
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  }
+ ]
+}
diff --git a/tests/observe/record_golden_questions.py b/tests/observe/record_golden_questions.py
index de0351709..9567ed2f0 100644
--- a/tests/observe/record_golden_questions.py
+++ b/tests/observe/record_golden_questions.py
@@ -251,6 +251,29 @@ def build(evidence: Path) -> dict[str, dict]:
     }
 
 
+def build_cap(evidence: Path) -> dict:
+    """The 100-row cap sample (evidence file 14: a 104-message probe Run read with ``--all``).
+
+    Exactly 100 question rows, newest first; the 4 oldest messages are silently missing and
+    the reply has no total or truncation field. Rows are redacted like the other samples.
+    """
+    raw = json.loads((evidence / "14-all-B-cap.json").read_text(encoding="utf-8"))
+    shift = ANCHOR_TIME - NEWEST_OFFSET - newest_created([raw])
+    runs = Names("run-{n}")
+    runs._seen.update({"run_14cfcbd8edf2": "run-b"})
+    envelope = redact_envelope(
+        raw, envelope_id="env-cap", runs=runs, messages=Names("{n}"), shift=shift
+    )
+    rows = envelope["result"]["messages"]
+    if len(rows) != 100 or any(r["type"] != "question" for r in rows):
+        raise ValueError("the cap sample must hold exactly 100 question rows")
+    return {
+        "variant": "question-cap-100",
+        "description": "exactly 100 question rows, newest first: the shape of a read that hit the 100-row bound",
+        "cycles": [envelope],
+    }
+
+
 def write(documents: dict[str, dict], directory: Path = FIXTURES) -> list[Path]:
     paths = []
     for name, document in documents.items():
@@ -264,7 +287,8 @@ def main(argv: list[str] | None = None) -> int:
     parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
     parser.add_argument("--evidence", required=True, type=Path)
     args = parser.parse_args(argv)
-    for path in write(build(args.evidence)):
+    documents = {**build(args.evidence), "question-cap-100": build_cap(args.evidence)}
+    for path in write(documents):
         print(f"wrote {path.name}")
     return 0
 
diff --git a/tests/observe/test_question_cap.py b/tests/observe/test_question_cap.py
new file mode 100644
index 000000000..20008ebc1
--- /dev/null
+++ b/tests/observe/test_question_cap.py
@@ -0,0 +1,152 @@
+"""The 100-row bound of the message read (T54; REPORT evidence file 14: 104 messages, 100 rows).
+
+``check --all`` returns the newest 100 rows with no total and no truncation field, so a read of
+exactly 100 rows may have lost older ones. The observer discloses that, keeps what it saw, and
+never takes a count from ``result.count``.
+"""
+
+from __future__ import annotations
+
+import copy
+import json
+
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector
+from superclaude.cli.observe.export import record_text, snapshot_json
+from superclaude.cli.observe.parse import load_fixture
+from superclaude.cli.observe.render import screen_lines
+from superclaude.cli.observe.terminal import resolve_policy
+from superclaude.cli.observe.view import (
+    QUESTIONS_DISCLOSURE,
+    QUESTIONS_WINDOW_FULL,
+    Session,
+    build_view,
+)
+from tests.observe.conftest import (
+    QRUN,
+    FakeDiscover,
+    FakeRunner,
+    make_envelope,
+    make_question_envelope,
+    make_question_rows,
+    make_rows,
+    routed_runner_responses,
+)
+
+
+def cap_envelope():
+    return copy.deepcopy(load_fixture("question-cap-100").cycle(0).envelope)
+
+
+def collector_for(messages, clock, argv_log, run_id):
+    worker = (0, json.dumps(make_envelope(make_rows(3, 1), total=3)))
+    runner = FakeRunner(argv_log, [routed_runner_responses(worker, messages)])
+    return Collector(
+        LiveSource(runner, FakeDiscover(argv_log)), clock, run_id=run_id, questions=True
+    )
+
+
+def ok(envelope):
+    return 0, json.dumps(envelope)
+
+
+def screen(result, clock, width=160, height=60):
+    view = build_view(result, Session(), clock)
+    return view, screen_lines(view, resolve_policy({}, "utf-8", {}, width, height))
+
+
+def test_the_recorded_shape_fixture_is_exactly_100_question_rows_newest_first():
+    envelope = cap_envelope()
+    rows = envelope["result"]["messages"]
+    assert len(rows) == 100 and all(r["type"] == "question" for r in rows)
+    stamps = [r["created_at"] for r in rows]
+    assert stamps == sorted(
+        stamps, reverse=True
+    )  # newest first, as check --all gives them
+    assert len({r["id"] for r in rows}) == 100
+    # No total, hasMore or truncation field: the loss cannot be seen in the reply itself.
+    assert set(envelope["result"]) == {"acknowledged", "count", "messages", "runId"}
+
+
+def test_a_100_row_reply_sets_window_full_and_the_panel_says_so(fake_clock, argv_log):
+    collector = collector_for(ok(cap_envelope()), fake_clock, argv_log, "run-b")
+    result = collector.run_once()
+    assert result.question_state == "OK" and result.questions.window_full is True
+    view, lines = screen(result, fake_clock)
+    assert view.questions.window_full_text == QUESTIONS_WINDOW_FULL
+    assert "window full: older questions may be missing" in lines
+    flat = " ".join(" ".join(lines).split())
+    assert QUESTIONS_DISCLOSURE in flat
+    assert "bounded best effort; coverage unknown" in flat
+    assert "observed open: 100 |" in flat
+    record = record_text(view)
+    assert "window full: older questions may be missing" in record
+    assert json.loads(snapshot_json(view))["questions"]["windowFull"] is True
+
+
+def test_a_99_row_reply_is_not_window_full(fake_clock, argv_log):
+    envelope = cap_envelope()
+    envelope["result"]["messages"].pop()
+    envelope["result"]["count"] = 99
+    result = collector_for(ok(envelope), fake_clock, argv_log, "run-b").run_once()
+    assert result.questions.window_full is False
+    view, lines = screen(result, fake_clock)
+    assert view.questions.window_full_text is None
+    assert not any("window full" in line for line in lines)
+    assert "observed open: 99 |" in " ".join(lines)
+    # exactly 101 rows (more than the bound) is not "exactly 100" either
+    over = make_question_envelope(make_question_rows(101))
+    again = collector_for(ok(over), fake_clock, argv_log, QRUN).run_once()
+    assert again.questions.window_full is False
+
+
+def test_a_moved_window_keeps_the_dropped_questions_and_the_open_total_does_not_fall(
+    fake_clock, argv_log
+):
+    first = make_question_envelope(make_question_rows(100, start=0))
+    moved = make_question_envelope(make_question_rows(100, start=10))  # newest 100 only
+    collector = collector_for([ok(first), ok(moved)], fake_clock, argv_log, QRUN)
+    one = collector.run_once()
+    two = collector.run_once()
+    assert one.questions.open_total == 100 and two.questions.open_total == 110
+    assert two.questions.window_full is True
+    gone = [r for r in two.questions.records if not r.in_window]
+    assert len(gone) == 10
+    assert {r.question.qid for r in gone} == {f"msg_{i:012x}" for i in range(10)}
+    view, lines = screen(two, fake_clock, height=200)
+    assert view.questions.counts_line.startswith("observed open: 110 |")
+    assert sum("no longer in source window" in line for line in lines) == 10
+    assert "window full: older questions may be missing" in lines
+
+
+def test_the_panel_never_prints_a_total_taken_from_result_count(fake_clock, argv_log):
+    envelope = cap_envelope()
+    envelope["result"]["count"] = 7777  # a reply whose count disagrees with its rows
+    result = collector_for(ok(envelope), fake_clock, argv_log, "run-b").run_once()
+    view, lines = screen(result, fake_clock, height=200)
+    everything = "\n".join([*lines, record_text(view), snapshot_json(view)])
+    assert "7777" not in everything
+    assert view.questions.counts_line.startswith("observed open: 100 |")
+    assert json.loads(snapshot_json(view))["questions"]["observedOpen"] == 100
+
+
+def test_no_message_argv_has_peek_and_every_one_has_types_question(
+    fake_clock, argv_log
+):
+    first = make_question_envelope(make_question_rows(100))
+    collector = collector_for(
+        [ok(first), ok(cap_envelope())], fake_clock, argv_log, QRUN
+    )
+    collector.run_once()
+    collector.run_once()
+    message = [a for a in argv_log if a[1:3] == ["orchestration", "check"]]
+    assert len(message) == 2
+    for argv in message:
+        assert "--peek" not in argv
+        assert argv[argv.index("--types") + 1] == "question"
+        assert argv[argv.index("--all") : argv.index("--all") + 3] == [
+            "--all",
+            "--types",
+            "question",
+        ]
+    assert not any(a for a in argv_log if "--peek" in a or "--ack" in a)


Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
