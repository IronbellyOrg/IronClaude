d40de5d8517f4334e2af00f760cb95a873f0246f
Review one task for spec compliance.

Task brief: 
## Task 13: Record the four redacted message-read samples and pin them in contract tests

Depends on: Task 9, Task 10

Create `src/superclaude/cli/observe/fixtures/golden-question-success.json`, `golden-question-missing.json`, `golden-question-stale.json`, `golden-question-contradictory.json` and extend `tests/observe/test_golden_contract.py` and `tests/observe/test_fixtures.py` (data-gate rule in `release-gates.md`: four kinds, each pinned in a contract test). Build them from the already recorded probe outputs in REPORT's evidence folder (success from files 03 and 24; missing from file 03 with `messages` removed and from the `no_active_terminal` file 17; contradictory from a success envelope carrying a status-type row and a row from another Run, and from the `consumer_fenced` file 01 read by a bound Run; stale from the success envelope replayed after the clock advances beyond 45 s). Do not make any new Orca call. Redact before saving: replace `from_handle`, `to_handle`, Run ids and message ids with synthetic stable values, remove `body`, keep key names and types. Mirror how the existing four `golden-*` worker-list samples are loaded and tested in `tests/observe/test_golden_contract.py`, and write `./artifacts/t13-redaction.md` listing each field replaced.

Acceptance criteria:
- `uv run pytest tests/observe/test_golden_contract.py tests/observe/test_fixtures.py -v` passes: success parses to the expected question count and ids; missing gives `FAILED (shape)` or `no-active-terminal` with retained questions kept; stale shows `STALE` after the monotonic clock passes 45 s with the questions kept; contradictory rows are dropped and counted and `consumer-fenced` is shown.
- The sensitive-string scan used by `test_fixtures.py` (`SENSITIVE`) finds no `term_` handle, token, credential or absolute path in the four files.

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

Start sha: d40de5d8517f4334e2af00f760cb95a873f0246f
Diff against the start snapshot: 
diff --git a/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/t13-redaction.md b/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/t13-redaction.md
new file mode 100644
index 000000000..5d1e00547
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/t13-redaction.md
@@ -0,0 +1,40 @@
+# T13 redaction record: the four message-read samples
+
+Made by `tests/observe/record_golden_questions.py --evidence <REPORT evidence folder>`. No Orca call was made: the input is the already recorded, sanitized probe output in `research/evidence/` next to `RESEARCH-REPORT-phase2-gate.md` (files 01, 03, 17 and 24). Output: `src/superclaude/cli/observe/fixtures/golden-question-{success,missing,stale,contradictory}.json`.
+
+All values below are from the two throwaway probe Runs of 2026-11-11. None is from the coordinator's own Run or any Run the research did not create.
+
+## Fields replaced
+
+| Field | Replaced by | Why |
+|---|---|---|
+| envelope `id` (a UUID) | `env-001` ... `env-005` | not needed; unique per call |
+| `_meta.runtimeId` (a UUID) | `redacted` | host-specific id |
+| message `id` (`msg_` + 12 hex) | `msg_000000000001`, `msg_000000000002`, ... in first-seen order | synthetic stable ids |
+| message `run_id`, `result.runId` | `run-a` (probe Run A), `run-b` (probe Run B) | synthetic Run names |
+| message `to_handle` (`run:<id>`) | `run:run-a` or `run:run-b` | same mapping; a non-`run:` value would become `redacted` |
+| message `from_handle` (a `term_` handle) | `redacted` | terminal handle |
+| message `body` | `redacted` | bodies are never committed |
+| message `payload` | `null` stays `null`; any other value becomes `redacted` | the probes sent none; a real value could hold anything |
+| message `created_at`, `delivered_at` | shifted by one constant so the newest question lands one minute before 2026-11-08T12:00:00Z (the observer tests' base time); `null` stays `null` | stable ages in tests |
+| any message key outside the recorded 13 | `redacted` (name kept) | keys outside the recorded set survive by name only |
+| error `message` text | each `run_<12 hex>` replaced with the same mapping (`run-a`, `run-b`) | the `consumer_fenced` text names both Runs |
+
+## Kept as recorded
+
+Key names and value types; `delivery_contract`, `type`, `priority`, `thread_id` (null), `acknowledged` (null), `count`; `subject` (the synthetic probe strings `probe A question` and `probe self q1`, which the research worker wrote itself); the error `code` values `consumer_fenced` and `no_active_terminal`.
+
+## How each kind was built
+
+| Sample | Built from |
+|---|---|
+| success | file 24 (Run A, `--types question`, 1 row) plus the question row of file 03 (Run B), both re-homed to `run-a`, newest first |
+| missing | file 03 with `result.messages` removed, then the `no_active_terminal` error of file 17 |
+| stale | the success read, then three `{"fail": "timeout"}` cycles; the test moves the fake monotonic clock past 45 s |
+| contradictory | the success read; then the success read plus the status row of file 03 and one question row carrying the other Run; then the `consumer_fenced` error of file 01 |
+
+## Checks
+
+`tests/observe/test_golden_contract.py` (`test_question_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte`) scans the four files with the `SENSITIVE` patterns of `test_fixtures.py`, plus `run_<12 hex>`, `term_` and non-synthetic `msg_` ids, and asserts every message has exactly the recorded key set with `body` and `from_handle` equal to `redacted`. `tests/observe/test_fixtures.py` scans every file in the fixtures folder again.
+
+A first run of the recorder test caught that a non-null `payload` survived redaction; the recorder now redacts it (fixed before the files were committed).
diff --git a/src/superclaude/cli/observe/fixtures/golden-question-contradictory.json b/src/superclaude/cli/observe/fixtures/golden-question-contradictory.json
new file mode 100644
index 000000000..a8af1e801
--- /dev/null
+++ b/src/superclaude/cli/observe/fixtures/golden-question-contradictory.json
@@ -0,0 +1,135 @@
+{
+ "variant": "golden-question-contradictory",
+ "description": "a good read, a read with a status row and a row of another Run, then the consumer_fenced error",
+ "cycles": [
+  {
+   "id": "env-001",
+   "ok": true,
+   "result": {
+    "acknowledged": null,
+    "count": 2,
+    "messages": [
+     {
+      "id": "msg_000000000001",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe A question",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000002",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe self q1",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     }
+    ],
+    "runId": "run-a"
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  },
+  {
+   "id": "env-004",
+   "ok": true,
+   "result": {
+    "acknowledged": null,
+    "count": 4,
+    "messages": [
+     {
+      "id": "msg_000000000001",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe A question",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000002",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe self q1",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000003",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe B status",
+      "body": "redacted",
+      "type": "status",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:59:00Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000004",
+      "run_id": "run-b",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-b",
+      "subject": "probe self q1",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     }
+    ],
+    "runId": "run-a"
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  },
+  {
+   "id": "env-005",
+   "ok": false,
+   "error": {
+    "code": "consumer_fenced",
+    "message": "This caller is bound to Run run-b, not Run run-a. Nothing changed."
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  }
+ ]
+}
diff --git a/src/superclaude/cli/observe/fixtures/golden-question-missing.json b/src/superclaude/cli/observe/fixtures/golden-question-missing.json
new file mode 100644
index 000000000..66a8f9795
--- /dev/null
+++ b/src/superclaude/cli/observe/fixtures/golden-question-missing.json
@@ -0,0 +1,73 @@
+{
+ "variant": "golden-question-missing",
+ "description": "a good read, then an envelope without result.messages, then the no_active_terminal error",
+ "cycles": [
+  {
+   "id": "env-001",
+   "ok": true,
+   "result": {
+    "acknowledged": null,
+    "count": 2,
+    "messages": [
+     {
+      "id": "msg_000000000001",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe A question",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000002",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe self q1",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     }
+    ],
+    "runId": "run-a"
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  },
+  {
+   "id": "env-002",
+   "ok": true,
+   "result": {
+    "acknowledged": null,
+    "count": 2,
+    "runId": "run-b"
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  },
+  {
+   "id": "env-003",
+   "ok": false,
+   "error": {
+    "code": "no_active_terminal",
+    "message": "no_active_terminal"
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  }
+ ]
+}
diff --git a/src/superclaude/cli/observe/fixtures/golden-question-stale.json b/src/superclaude/cli/observe/fixtures/golden-question-stale.json
new file mode 100644
index 000000000..5a7c4bee7
--- /dev/null
+++ b/src/superclaude/cli/observe/fixtures/golden-question-stale.json
@@ -0,0 +1,59 @@
+{
+ "variant": "golden-question-stale",
+ "description": "the good read, then failing reads (the test moves the fake monotonic clock past 45 s)",
+ "cycles": [
+  {
+   "id": "env-001",
+   "ok": true,
+   "result": {
+    "acknowledged": null,
+    "count": 2,
+    "messages": [
+     {
+      "id": "msg_000000000001",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe A question",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000002",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe self q1",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     }
+    ],
+    "runId": "run-a"
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  },
+  {
+   "fail": "timeout"
+  },
+  {
+   "fail": "timeout"
+  },
+  {
+   "fail": "timeout"
+  }
+ ]
+}
diff --git a/src/superclaude/cli/observe/fixtures/golden-question-success.json b/src/superclaude/cli/observe/fixtures/golden-question-success.json
new file mode 100644
index 000000000..72c3aa210
--- /dev/null
+++ b/src/superclaude/cli/observe/fixtures/golden-question-success.json
@@ -0,0 +1,50 @@
+{
+ "variant": "golden-question-success",
+ "description": "a good message read: two question rows of one Run, newest first",
+ "cycles": [
+  {
+   "id": "env-001",
+   "ok": true,
+   "result": {
+    "acknowledged": null,
+    "count": 2,
+    "messages": [
+     {
+      "id": "msg_000000000001",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe A question",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:59Z",
+      "delivered_at": null
+     },
+     {
+      "id": "msg_000000000002",
+      "run_id": "run-a",
+      "delivery_contract": "current_delivery",
+      "from_handle": "redacted",
+      "to_handle": "run:run-a",
+      "subject": "probe self q1",
+      "body": "redacted",
+      "type": "question",
+      "priority": "normal",
+      "thread_id": null,
+      "payload": null,
+      "created_at": "2026-11-08T11:58:53Z",
+      "delivered_at": null
+     }
+    ],
+    "runId": "run-a"
+   },
+   "_meta": {
+    "runtimeId": "redacted"
+   }
+  }
+ ]
+}
diff --git a/tests/observe/record_golden_questions.py b/tests/observe/record_golden_questions.py
new file mode 100644
index 000000000..de0351709
--- /dev/null
+++ b/tests/observe/record_golden_questions.py
@@ -0,0 +1,273 @@
+"""Developer tool (not shipped): build the four redacted message-read samples from recorded probes.
+
+It makes NO Orca call. It reads the already recorded, sanitized probe outputs of the phase 2
+gate research (``research/evidence/`` next to ``RESEARCH-REPORT-phase2-gate.md``, files 01, 03,
+17 and 24) and writes four fixture files:
+
+    golden-question-success.json  golden-question-missing.json
+    golden-question-stale.json    golden-question-contradictory.json
+
+    uv run python tests/observe/record_golden_questions.py --evidence <evidence dir>
+
+Redaction (``redact_envelope``): message ids, Run ids and the Run inside a ``to_handle`` become
+synthetic stable values; ``from_handle`` and ``body`` become ``redacted``; every key outside the
+recorded set becomes ``redacted``; timestamps shift by one constant so the newest lands one
+minute before the anchor; envelope and runtime ids become fixed placeholders. Key names and
+value types are kept. Subjects are kept: they are the synthetic strings of the probes.
+"""
+
+from __future__ import annotations
+
+import argparse
+import copy
+import json
+import re
+import sys
+from pathlib import Path
+
+from superclaude.cli.observe import adapter
+from superclaude.cli.observe.parse import format_utc_iso, parse_timestamp
+
+FIXTURES = Path(adapter.__file__).parent / "fixtures"
+ANCHOR_TIME = 1794139200.0  # 2026-11-08T12:00:00Z (the observer tests' base time)
+NEWEST_OFFSET = 60.0  # the newest recorded question lands one minute before the anchor
+
+MESSAGE_KEYS = (
+    "id",
+    "run_id",
+    "delivery_contract",
+    "from_handle",
+    "to_handle",
+    "subject",
+    "body",
+    "type",
+    "priority",
+    "thread_id",
+    "payload",
+    "created_at",
+    "delivered_at",
+)
+RUN_ID = re.compile(r"run_[0-9a-f]{12}")
+EVIDENCE = {
+    "success_b": "03-all-B.json",
+    "success_a": "24-all-A-types-question.json",
+    "fenced": "01-all-A-read1.json",
+    "no_terminal": "17-unbound-all-A.json",
+}
+
+
+class Names:
+    """Stable synthetic names: the nth distinct original gets the nth placeholder."""
+
+    def __init__(self, fmt: str) -> None:
+        self._fmt = fmt
+        self._seen: dict[str, str] = {}
+
+    def __call__(self, original: str) -> str:
+        if original not in self._seen:
+            self._seen[original] = self._fmt.format(n=len(self._seen) + 1)
+        return self._seen[original]
+
+
+def newest_created(envelopes: list[dict]) -> float:
+    stamps = [
+        parse_timestamp(m.get("created_at"))
+        for env in envelopes
+        for m in (env.get("result") or {}).get("messages") or []
+        if isinstance(m, dict)
+    ]
+    return max(s for s in stamps if s is not None)
+
+
+def redact_envelope(
+    env: dict,
+    *,
+    envelope_id: str,
+    runs: Names,
+    messages: Names,
+    shift: float,
+) -> dict:
+    """One redacted copy of a message-read envelope (success or error)."""
+    if not isinstance(env, dict) or not isinstance(env.get("ok"), bool):
+        raise ValueError("not a message-read envelope")
+    out: dict = {"id": envelope_id, "ok": env["ok"]}
+    if env["ok"]:
+        result = env.get("result")
+        if not isinstance(result, dict) or not isinstance(result.get("messages"), list):
+            raise ValueError("result.messages is not a list")
+        rows = [redact_message(m, runs, messages, shift) for m in result["messages"]]
+        out["result"] = {
+            "acknowledged": result.get("acknowledged"),
+            "count": len(rows),
+            "messages": rows,
+            "runId": runs(result["runId"])
+            if isinstance(result.get("runId"), str)
+            else None,
+        }
+    else:
+        error = env.get("error")
+        if not isinstance(error, dict):
+            raise ValueError("error is not an object")
+        message = RUN_ID.sub(lambda m: runs(m.group(0)), str(error.get("message", "")))
+        out["error"] = {"code": str(error.get("code", "")), "message": message}
+    out["_meta"] = {"runtimeId": "redacted"}
+    return out
+
+
+def redact_message(raw: dict, runs: Names, messages: Names, shift: float) -> dict:
+    if not isinstance(raw, dict):
+        raise ValueError("a message row is not an object")
+    row: dict = {}
+    for key in MESSAGE_KEYS:
+        if key not in raw:
+            continue
+        value = raw[key]
+        if key == "id":
+            row[key] = f"msg_{int(messages(value)):012d}"
+        elif key == "run_id":
+            row[key] = runs(value)
+        elif key == "to_handle":
+            row[key] = (
+                f"run:{runs(value.split(':', 1)[1])}"
+                if value.startswith("run:")
+                else "redacted"
+            )
+        elif key in ("from_handle", "body"):
+            row[key] = "redacted"
+        elif key == "payload":
+            row[key] = None if value is None else "redacted"  # a null stays null
+        elif key in ("created_at", "delivered_at"):
+            epoch = parse_timestamp(value)
+            row[key] = None if epoch is None else format_utc_iso(epoch + shift)
+        else:
+            row[key] = value
+    for key in set(raw) - set(
+        MESSAGE_KEYS
+    ):  # keys outside the recorded set survive by name only
+        row[key] = "redacted"
+    return row
+
+
+def load(evidence: Path) -> dict[str, dict]:
+    return {
+        name: json.loads((evidence / filename).read_text(encoding="utf-8"))
+        for name, filename in EVIDENCE.items()
+    }
+
+
+def build(evidence: Path) -> dict[str, dict]:
+    """The four fixture documents, keyed by variant name."""
+    raw = load(evidence)
+    shift = (
+        ANCHOR_TIME
+        - NEWEST_OFFSET
+        - newest_created([raw["success_b"], raw["success_a"]])
+    )
+    runs = Names("run-{n}")  # run-1, run-2 ...
+    messages = Names("{n}")  # the nth distinct original id becomes msg_<n>, zero padded
+    # Run ids first, so the order is stable: the question Run of the probes is "run-a".
+    letter = {"run_c1badaa6576b": "run-a", "run_14cfcbd8edf2": "run-b"}
+    runs._seen.update(letter)
+
+    def red(env: dict, label: str) -> dict:
+        return redact_envelope(
+            env, envelope_id=label, runs=runs, messages=messages, shift=shift
+        )
+
+    question_b = [
+        m for m in raw["success_b"]["result"]["messages"] if m["type"] == "question"
+    ]
+    status_b = [
+        m for m in raw["success_b"]["result"]["messages"] if m["type"] != "question"
+    ]
+    success = copy.deepcopy(raw["success_a"])
+    success["result"]["messages"] = [
+        *success["result"]["messages"],
+        *[
+            {
+                **m,
+                "run_id": success["result"]["runId"],
+                "to_handle": f"run:{success['result']['runId']}",
+            }
+            for m in question_b
+        ],
+    ]
+    success["result"]["messages"].sort(
+        key=lambda m: m["created_at"], reverse=True
+    )  # newest first
+    success["result"]["count"] = len(success["result"]["messages"])
+    good = red(success, "env-001")
+
+    missing_cycle = red(raw["success_b"], "env-002")
+    del missing_cycle["result"]["messages"]
+    no_terminal = red(raw["no_terminal"], "env-003")
+
+    contradictory_ok = copy.deepcopy(success)
+    contradictory_ok["result"]["messages"] = [
+        *contradictory_ok["result"]["messages"],
+        *[
+            {
+                **m,
+                "run_id": success["result"]["runId"],
+                "to_handle": f"run:{success['result']['runId']}",
+            }
+            for m in status_b
+        ],
+        {
+            **question_b[0],
+            "id": "msg_zzzzzzzzzzzz",
+            "run_id": raw["success_b"]["result"]["runId"],
+        },
+    ]
+    contradictory_ok["result"]["count"] = len(contradictory_ok["result"]["messages"])
+    contradictory = [red(contradictory_ok, "env-004"), red(raw["fenced"], "env-005")]
+
+    return {
+        "golden-question-success": {
+            "variant": "golden-question-success",
+            "description": "a good message read: two question rows of one Run, newest first",
+            "cycles": [good],
+        },
+        "golden-question-missing": {
+            "variant": "golden-question-missing",
+            "description": "a good read, then an envelope without result.messages, then the no_active_terminal error",
+            "cycles": [good, missing_cycle, no_terminal],
+        },
+        "golden-question-stale": {
+            "variant": "golden-question-stale",
+            "description": "the good read, then failing reads (the test moves the fake monotonic clock past 45 s)",
+            "cycles": [
+                good,
+                {"fail": "timeout"},
+                {"fail": "timeout"},
+                {"fail": "timeout"},
+            ],
+        },
+        "golden-question-contradictory": {
+            "variant": "golden-question-contradictory",
+            "description": "a good read, a read with a status row and a row of another Run, then the consumer_fenced error",
+            "cycles": [good, *contradictory],
+        },
+    }
+
+
+def write(documents: dict[str, dict], directory: Path = FIXTURES) -> list[Path]:
+    paths = []
+    for name, document in documents.items():
+        path = directory / f"{name}.json"
+        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
+        paths.append(path)
+    return paths
+
+
+def main(argv: list[str] | None = None) -> int:
+    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
+    parser.add_argument("--evidence", required=True, type=Path)
+    args = parser.parse_args(argv)
+    for path in write(build(args.evidence)):
+        print(f"wrote {path.name}")
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/tests/observe/test_fixtures.py b/tests/observe/test_fixtures.py
index dc2878b09..d9ed6803c 100644
--- a/tests/observe/test_fixtures.py
+++ b/tests/observe/test_fixtures.py
@@ -2,6 +2,7 @@
 
 from __future__ import annotations
 
+import json
 import re
 import subprocess
 import sys
@@ -294,3 +295,30 @@ def test_console_factory_builds_a_recording_console_through_make_console(
     console.print("hello")
     assert console.width == 116 and policy.ascii and policy.no_color
     assert console.export_text().strip() == "hello"
+
+
+# -- R2: the four recorded samples of the message read are shipped and loadable -----------------------------
+
+QUESTION_SAMPLES = (
+    "golden-question-success",
+    "golden-question-missing",
+    "golden-question-stale",
+    "golden-question-contradictory",
+)
+
+
+@pytest.mark.parametrize("name", QUESTION_SAMPLES)
+def test_each_question_sample_is_shipped_loads_and_has_a_description(name):
+    names = {
+        p.name for p in resources.files("superclaude.cli.observe.fixtures").iterdir()
+    }
+    assert f"{name}.json" in names
+    fixture = load_fixture(name)
+    assert fixture.variant == name and len(fixture.cycles) >= 1
+    document = json.loads(
+        resources.files("superclaude.cli.observe.fixtures")
+        .joinpath(f"{name}.json")
+        .read_text(encoding="utf-8")
+    )
+    assert document["variant"] == name and document["description"]
+    assert name not in VARIANTS  # the ten worker-list variants are unchanged
diff --git a/tests/observe/test_golden_contract.py b/tests/observe/test_golden_contract.py
index 3bc0e6f06..4f0f47087 100644
--- a/tests/observe/test_golden_contract.py
+++ b/tests/observe/test_golden_contract.py
@@ -363,3 +363,271 @@ def test_the_four_golden_kinds_are_derived_from_one_sample():
         second["result"]["workers"][0]["projection"]["liveness"]["observedAt"]
         < "2026-11-08T12:00:00Z"
     )
+
+
+# -- R2: the four redacted samples of the message read (data gate; T55) ---------------------------------------------------
+
+from superclaude.cli.observe.adapter import RunnerFailure  # noqa: E402
+from superclaude.cli.observe.view import QUESTIONS_NOT_HELD  # noqa: E402
+from tests.observe import record_golden_questions  # noqa: E402
+from tests.observe.conftest import (  # noqa: E402
+    make_envelope,
+    make_rows,
+    routed_runner_responses,
+)
+
+QUESTION_GOLDEN = (
+    "golden-question-success",
+    "golden-question-missing",
+    "golden-question-stale",
+    "golden-question-contradictory",
+)
+GOLDEN_RUN = "run-a"
+MESSAGE_KEYS = set(record_golden_questions.MESSAGE_KEYS)
+
+
+def golden_cycles(name):
+    """The recorded cycles of one sample as raw runner replies (error envelopes exit 1)."""
+    replies = []
+    for cycle in load_fixture(name).cycles:
+        if cycle.envelope is None:
+
+            def fail(argv, timeout, code=cycle.fail):
+                raise RunnerFailure(code)
+
+            replies.append(fail)
+        else:
+            status = 0 if cycle.envelope.get("ok") is True else 1
+            replies.append((status, json.dumps(cycle.envelope)))
+    return replies
+
+
+def golden_collector(name, clock):
+    worker = (0, json.dumps(make_envelope(make_rows(2, 1), total=2)))
+    runner = FakeRunner([], [routed_runner_responses(worker, golden_cycles(name))])
+    return Collector(
+        LiveSource(runner, FakeDiscover([])),
+        clock,
+        run_id=GOLDEN_RUN,
+        questions=True,
+    )
+
+
+def test_t55_the_success_sample_parses_to_its_two_questions_at_every_width(fake_clock):
+    result = golden_collector("golden-question-success", fake_clock).run_once()
+    assert result.state == "OK" and result.question_state == "OK"
+    state = result.questions
+    assert [r.question.qid for r in state.records] == [
+        "msg_000000000002",
+        "msg_000000000001",
+    ]  # oldest created first
+    assert [r.question.subject for r in state.records] == [
+        "probe self q1",
+        "probe A question",
+    ]
+    assert state.open_total == 2 and state.window_full is False
+    assert result.question_read.raw_count == 2
+    view = view_of(result, fake_clock)
+    for width in (160, 116, 80):
+        lines = screen_lines(view, policy(width))
+        assert all(cell_len(line) <= width for line in lines)
+        assert "COORDINATOR QUESTIONS" in lines
+        assert sum("reason unknown" in line for line in lines) == 2
+
+
+def test_t55_the_missing_sample_fails_by_shape_then_by_no_active_terminal_and_keeps_questions(
+    fake_clock,
+):
+    cycles = load_fixture("golden-question-missing").cycles
+    assert "messages" not in cycles[1].envelope["result"]
+    assert cycles[2].envelope["error"]["code"] == "no_active_terminal"
+    collector = golden_collector("golden-question-missing", fake_clock)
+    good = collector.run_once()
+    shape = collector.run_once()
+    assert (shape.question_state, shape.question_code) == ("FAILED", "shape")
+    assert shape.questions is good.questions and shape.state == "OK"
+    gone = collector.run_once()
+    assert (gone.question_state, gone.question_code) == ("FAILED", "no-active-terminal")
+    assert gone.questions is good.questions
+    panel = view_of(gone, fake_clock).questions
+    assert panel.state == "FAILED" and QUESTIONS_NOT_HELD in panel.state_lines
+    assert panel.counts_line.startswith("observed open: 2 |") and len(panel.lines) == 2
+
+
+def test_t55_the_stale_sample_is_stale_after_45_seconds_with_the_questions_kept(
+    fake_clock,
+):
+    collector = golden_collector("golden-question-stale", fake_clock)
+    good = collector.run_once()
+    fake_clock.advance(44)
+    assert view_of(good, fake_clock).questions.state == "OK"
+    fake_clock.advance(1)
+    stale = view_of(good, fake_clock).questions
+    assert stale.state == "STALE" and stale.state_lines == ("STALE 45s",)
+    assert len(stale.lines) == 2 and stale.counts_line.startswith("observed open: 2 |")
+    fake_clock.jump_wall(-3600)  # wall-clock jumps change nothing
+    assert view_of(good, fake_clock).questions.state == "STALE"
+    failing = [collector.run_once() for _ in range(3)]
+    view = view_of(failing[-1], fake_clock).questions
+    assert [r.question_code for r in failing] == ["timeout"] * 3
+    assert view.state == "FAILED" and len(view.lines) == 2  # FAILED outranks STALE
+    assert failing[-1].questions is good.questions
+
+
+def test_t55_the_contradictory_sample_drops_and_counts_foreign_rows_then_shows_fenced(
+    fake_clock,
+):
+    cycles = load_fixture("golden-question-contradictory").cycles
+    kinds = [m["type"] for m in cycles[1].envelope["result"]["messages"]]
+    assert kinds.count("status") == 1 and len(kinds) == 4
+    assert {m["run_id"] for m in cycles[1].envelope["result"]["messages"]} == {
+        "run-a",
+        "run-b",
+    }
+    collector = golden_collector("golden-question-contradictory", fake_clock)
+    collector.run_once()
+    mixed = collector.run_once()
+    assert mixed.question_state == "OK" and mixed.question_read.contradictory_rows == 2
+    assert mixed.questions.retained == 2  # nothing foreign was retained
+    panel = view_of(mixed, fake_clock).questions
+    assert "2 contradictory rows ignored" in panel.notes
+    fenced = collector.run_once()
+    assert (fenced.question_state, fenced.question_code) == (
+        "FAILED",
+        "consumer-fenced",
+    )
+    assert fenced.questions is mixed.questions
+    assert "Run run-b, not Run run-a" in cycles[2].envelope["error"]["message"]
+
+
+@pytest.mark.parametrize("name", QUESTION_GOLDEN)
+def test_question_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte(
+    name,
+):
+    text = (
+        resources.files(FIXTURE_PACKAGE)
+        .joinpath(f"{name}.json")
+        .read_text(encoding="utf-8")
+    )
+    assert "\x1b" not in text and text.isascii()
+    for what, pattern in SENSITIVE.items():
+        assert not pattern.search(text), f"{name}: {what}"
+    assert not re.search(r"run_[0-9a-f]{12}|term_|msg_[0-9a-f]*[a-f][0-9a-f]*\b", text)
+    for cycle in load_fixture(name).cycles:
+        for message in ((cycle.envelope or {}).get("result") or {}).get("messages", []):
+            assert set(message) == MESSAGE_KEYS  # key names kept, none added
+            assert (
+                message["body"] == "redacted" and message["from_handle"] == "redacted"
+            )
+            assert re.fullmatch(r"msg_\d{12}", message["id"])
+
+
+def synthetic_question_envelope():
+    return {
+        "id": "552b2108-e561-4dd8-abb6-6d64b5c292e0",
+        "ok": True,
+        "result": {
+            "acknowledged": None,
+            "count": 2,
+            "messages": [
+                {
+                    "id": "msg_28c906cf3d97",
+                    "run_id": "run_14cfcbd8edf2",
+                    "delivery_contract": "current_delivery",
+                    "from_handle": "term_a39d3e66-a4f7-481e-bbf2-7f6ec8329e4f",
+                    "to_handle": "run:run_14cfcbd8edf2",
+                    "subject": "probe",
+                    "body": "SECRET text",
+                    "type": "question",
+                    "priority": "normal",
+                    "thread_id": None,
+                    "payload": {"k": "v"},
+                    "created_at": "2026-11-11T20:01:18Z",
+                    "delivered_at": None,
+                    "extra_key": "something",
+                },
+                {
+                    "id": "msg_2d0e7d2264e5",
+                    "run_id": "run_14cfcbd8edf2",
+                    "type": "status",
+                },
+            ],
+            "runId": "run_14cfcbd8edf2",
+        },
+        "_meta": {"runtimeId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f"},
+    }
+
+
+def test_the_recorder_redacts_ids_handles_bodies_and_extra_keys_and_keeps_key_names():
+    runs = record_golden_questions.Names("run-{n}")
+    ids = record_golden_questions.Names("{n}")
+    out = record_golden_questions.redact_envelope(
+        synthetic_question_envelope(),
+        envelope_id="env-001",
+        runs=runs,
+        messages=ids,
+        shift=0.0,
+    )
+    text = json.dumps(out)
+    for leaked in (
+        "run_14",
+        "msg_28",
+        "term_",
+        "SECRET",
+        "a7ee70a1",
+        "552b2108",
+        "something",
+        'k": "v',
+    ):
+        assert leaked not in text, leaked
+    first = out["result"]["messages"][0]
+    assert first["id"] == "msg_000000000001" and first["run_id"] == "run-1"
+    assert first["to_handle"] == "run:run-1" and first["from_handle"] == "redacted"
+    assert first["body"] == "redacted" and first["extra_key"] == "redacted"
+    assert out["result"]["runId"] == "run-1" and out["id"] == "env-001"
+    assert out["_meta"] == {"runtimeId": "redacted"}
+
+
+def test_the_recorder_redacts_the_run_ids_inside_an_error_message_and_shifts_times():
+    error = {
+        "id": "x",
+        "ok": False,
+        "error": {
+            "code": "consumer_fenced",
+            "message": "bound to Run run_14cfcbd8edf2, not Run run_c1badaa6576b. Nothing changed.",
+        },
+    }
+    out = record_golden_questions.redact_envelope(
+        error,
+        envelope_id="env-9",
+        runs=record_golden_questions.Names("run-{n}"),
+        messages=record_golden_questions.Names("{n}"),
+        shift=0.0,
+    )
+    assert out["error"] == {
+        "code": "consumer_fenced",
+        "message": "bound to Run run-1, not Run run-2. Nothing changed.",
+    }
+    envelope = synthetic_question_envelope()
+    shifted = record_golden_questions.redact_envelope(
+        envelope,
+        envelope_id="e",
+        runs=record_golden_questions.Names("run-{n}"),
+        messages=record_golden_questions.Names("{n}"),
+        shift=3600.0,
+    )
+    assert shifted["result"]["messages"][0]["created_at"] == "2026-11-11T21:01:18Z"
+    for bad in (
+        {},
+        {"ok": True},
+        {"ok": True, "result": {"messages": "x"}},
+        {"ok": False, "error": 5},
+    ):
+        with pytest.raises(ValueError):
+            record_golden_questions.redact_envelope(
+                bad,
+                envelope_id="e",
+                runs=record_golden_questions.Names("run-{n}"),
+                messages=record_golden_questions.Names("{n}"),
+                shift=0.0,
+            )


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
