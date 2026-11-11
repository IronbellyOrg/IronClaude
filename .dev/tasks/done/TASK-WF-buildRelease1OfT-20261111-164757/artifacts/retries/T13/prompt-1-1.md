116a2a4e121f95fda44ba831abb06d209769926d
Review one task for spec compliance.

Task brief: 
## Task 13: Record redacted golden samples and per-call timing from one live read

Depends on: Task 12

Create `tests/observe/record_golden.py` (a developer tool, not shipped), the four golden fixture files `src/superclaude/cli/observe/fixtures/golden-success.json`, `golden-missing.json`, `golden-stale.json` and `golden-contradictory.json`, `tests/observe/test_golden_contract.py`, and `./artifacts/t13-timing.md`. Follow `release-gates.md` (data-gate rule: samples of four kinds each pinned in a contract test) and T32 in `acceptance-tests.md`. `record_golden.py` discovers Orca with `_find_orca()`, makes exactly one read-only `worker-list --json --limit 100` call through the production runner from `adapter.py` (repeated at most 5 times only to measure duration), pipes the decoded JSON straight into a redaction step so the raw output never touches disk or a log, replaces every identifier with stable placeholders (`w-001`, `run-a`), drops or replaces absolute paths, terminal handles, tokens and credential-like strings, and writes the four files: success is the redacted sample; missing is the sample with `result.scope`, `page.total` and one inner `projection.*` key removed; stale is the sample read once successfully and then followed by failing cycles while a fake monotonic clock is advanced 45 s or more past the last success (STALE comes from monotonic time since the last successful poll, not from sample timestamps); contradictory is the sample with a duplicate `dispatchId` and a backward timestamp. If no Orca CLI validates, or the call fails, this task is blocked and reported, never completed with an invented sample. If the slowest measured call exceeds 3 s the per-call timeout constant in `adapter.py` is raised to three times that value, at most 14 s and never below 5 s; otherwise the 10 s default stays and is recorded as unmeasured-beyond-this-run.

Acceptance criteria:
- [T13.AC1] `uv run pytest tests/observe/test_golden_contract.py -v` passes: the success sample parses and renders at 160, 116 and 80 columns; the missing sample gives `scope unknown`, `reported unknown` and `unknown` for the removed inner key; the stale sample yields STALE once the fake monotonic clock is 45 s past the last success and not at 44 s, and a fresh poll that returns old evidence timestamps is not STALE; the contradictory sample shows `k duplicate rows ignored` and `conflict (time went back)`; removing `result`, `result.workers` or `result.page.hasMore` from the success sample gives `FAILED (shape)` with the last good snapshot kept (T32).
- [T13.AC2] A test scans the four committed files and shows no absolute path, `term_` handle, token-like string, URL with credentials or raw ESC byte.
- [T13.AC3] `./artifacts/t13-timing.md` records the number of calls, each call's duration, the redaction rules applied, the Orca version string if the CLI reports one, and the per-call timeout decision, and states which parts were not measured.
- [T13.AC4] `git status` shows no file containing raw Orca output was created anywhere in the repository or the package folder.
- [T13.AC5] The final report states whether the live read succeeded, and if it was blocked, says exactly why.

Global constraints: 
## Constraints

- Shorthand used in the tasks below. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`; it holds the canonical contract: `SPEC.md` and its companions `ARCHITECTURE-SPINE.md` (decisions AD-1 to AD-20 and conditional decisions CD-1 to CD-16), `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md` (tests T1 to T51), `release-gates.md`, `snapshot-export-schema.md` and `unverified-register.md`. SNAPSRC is `.dev/issues/409/tuibbs-review/architecture-options.md` (last section, the frozen snapshot fields). The package is `src/superclaude/cli/observe/` and its tests are `tests/observe/`. Where SPECDIR and the older `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` differ, SPECDIR wins.
- Scope is release 1 (R1: live `worker-list`, COUNTS and freshness strips, worker ledger with the verbatim `projection.nextAction.kind` column, capped paging, STALE after 45 s, changes since last look, the one-line question-source notice, the JSON snapshot) plus the offline R0 pieces R1 needs (key-reader spike, sanitizer, cell-width truncation, NO_COLOR and ASCII, fixture variants, text export, fixture mode). The owner chose the staged direction and confirmed Python + Rich with snapshot export in `.dev/issues/409/owner-decisions-20261108.md` (items 1 and 5), so the side-by-side R0 renders of the Attention Ledger and Decision Desk that were only input to that choice are not built.
- Out of scope, not built even as stubs: question rows and any `check`, `inbox` or message read (R2), the SEEN IS NOT RESOLVED and RETAIN CONTEXT panels, the Decision Desk (R3), `--include-remote` (R4), every write path into Orca (approve, retry, terminate, spawn, merge, reply, instruct), persisting the last-look baseline, the `read k of N Runs since start` header token and its collector counters (CD-10 default places it in the Attention Ledger header only), any Go or TUIBBS code, and moving `_find_orca()`.
- Acceptance tests not built because they serve only the excluded views: T7, T10, T17, T19, T45, T46, T50 and T51, and the question half of T12 and T47. Every other test in `acceptance-tests.md` that applies to the ledger view is mapped to a task below, plus the snapshot schema test (no ID assigned in the spec).
- Authorization evidence. The owner's message of 2026-11-11, "Proceed with building the first release", is taken as the go for R0 and R1, including registering `superclaude observe` (reading 1 of "production integration" in `release-gates.md`) and live read-only `worker-list` calls. Caveat: `release-gates.md` says the owner's own dated selection record (check AC-S) states the confirmed reading and the direction. No task here writes that record, and it stays a reviewer-checked item. The final report must say it was not seen.
- Live Orca calls. Only two kinds are ever made, both read-only, both through `adapter.py`: `worker-list --json --limit 100` polling (optional `--run <runId>`, optional `--cursor <value>`, no shell) and the one startup discovery through `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (runs `skills list --json`, at most two candidates, 10 s each, once per process, outside the 15 s cycle budget and the 5-call cap). No key maps to an Orca call. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) is checked before every call and is never shortened.
- Defaults taken for open owner questions (SPECDIR `ARCHITECTURE-SPINE.md` CD table), changeable by the owner: CD-2 change flags use `stage.worker`, `stage.dispatch`, `nextAction.kind`, `liveness.verdict` and `stage.detail` and `stage.activity` stay inspector-only; CD-3 snapshot rows use timestamp order; CD-4 only the spec-fixed height rules; CD-5 truncation glyph `>`; CD-6 `--once` prints the record text to stdout, `--snapshot PATH` sets the snapshot file, the default directory is `~/.local/state/superclaude/observe/`, files are 0600 and replaced atomically; CD-8 empty palette (plain text, meaning in words); CD-16 a ledger row does not name a shared `worktreeId`.
- Plan-author rules that close gaps in the spec (PROPOSED, the owner may change them). The state directory honours `XDG_STATE_HOME` when set so tests stay out of the real home folder. `--once` with a live source writes a snapshot only when `--snapshot` is given. Fixture mode (`--fixture <variant>`) never calls Orca and never writes a snapshot unless `--snapshot` is given. A failed key-reader spike blocks the interactive tasks and is reported to the owner; the Textual switch in AD-14 is applied only on the owner's say-so, and both toolkits are never built.
- Data handling. Raw Orca output is never logged, committed, or kept in fixtures; committed fixtures hold only redacted identifiers (no absolute path, terminal handle, token or credential). Worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown after control-character sanitizing, labelled `worker-reported`; they are not redacted and no credential or terminal-handle field is exported.
- No code is copied from TUIBBS-scp (AGPL-3.0); the design prototype `canvas.py` is never imported. Python 3.10 compatible, no new dependency (`rich`, `click`, `jsonschema` and `pexpect` are already dependencies in `pyproject.toml`), UV only (`uv run pytest tests/observe -v`, `uv run ruff check src/superclaude/cli/observe tests/observe`), and nothing is written under `.claude/`. Every task leaves ruff clean for the files it touches.
- A fact the source does not give is the single `UNKNOWN` sentinel (never `None`, `0`, `False`, `""`) and renders as the word `unknown`. Facts with no verified source render `unavailable (no source)`. Worker text always renders as literal text, never parsed as Rich markup.

Start sha: 116a2a4e121f95fda44ba831abb06d209769926d
Diff against the start snapshot: 
diff --git a/.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/artifacts/t13-timing.md b/.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/artifacts/t13-timing.md
new file mode 100644
index 000000000..31f63f707
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/artifacts/t13-timing.md
@@ -0,0 +1,24 @@
+# T13: golden worker-list samples and per-call timing
+
+Calls made: 3 (one for the sample, the rest only to time the call). Rows in the sample: 100.
+
+| Call | Duration (s) |
+|---|---|
+| 1 | 0.220 |
+| 2 | 0.197 |
+| 3 | 0.187 |
+
+Slowest: 0.220 s. Decision: keep the 10 s default; it stays unmeasured beyond this run (slowest call 0.22 s).
+
+Redaction rules applied:
+
+- dispatchId, taskId, runId, resource.id, worktreeId, host.id, workspace.id replaced by stable placeholders (w-001, t-001, run-a, res-001, wt-001, host-a, ws-a)
+- resource.ownerDispatchId and originDispatchId mapped to the dispatch placeholder when they name a collected row, else w-ext-N
+- stage.detail and stage.activity replaced by fixed synthetic text (free text is never copied)
+- all timestamps shifted by one constant so the newest lands on 2026-11-08T12:00:00Z; unparsable ones become redacted-time
+- keys outside the verified worker-list set are kept by name only with the value redacted; page.nextCursor becomes cursor-1; warnings become redacted warning
+- any remaining string containing a slash, a terminal handle marker, a URL, an at sign or a 24+ character token is replaced by redacted
+
+Orca version string: not read (only the two allowed read-only calls are made, and neither reports one).
+
+Not measured: behaviour under load, a reply with more than one page, a reply with a non-empty `warnings` list unless the sample had one, any failing call. The fixtures were written to `src/superclaude/cli/observe/fixtures/golden-*.json`.
diff --git a/tests/observe/record_golden.py b/tests/observe/record_golden.py
new file mode 100644
index 000000000..fb14320a0
--- /dev/null
+++ b/tests/observe/record_golden.py
@@ -0,0 +1,385 @@
+"""Developer tool (not shipped): record redacted golden worker-list samples from one live read.
+
+Makes read-only ``worker-list --json --limit 100`` calls through the production runner of
+``adapter.py`` (one for the sample, at most two more only to time the call), pipes the decoded
+JSON straight into the redaction step and writes four fixture files plus a timing note. The raw
+Orca output is never written to disk, logged or printed.
+
+    uv run python tests/observe/record_golden.py --timing-note <path/to/t13-timing.md>
+
+If no Orca CLI validates or the call fails, nothing is written and the exit code is 3.
+"""
+
+from __future__ import annotations
+
+import argparse
+import copy
+import json
+import re
+import sys
+import time
+from pathlib import Path
+
+from superclaude.cli.observe import adapter
+from superclaude.cli.observe.parse import format_utc_iso, parse_timestamp
+
+FIXTURES = Path(adapter.__file__).parent / "fixtures"
+ANCHOR_TIME = 1794139200.0  # 2026-11-08T12:00:00Z: every timestamp is shifted so the newest lands here
+MAX_CALLS = 3  # one sample plus at most two timing repeats (the plan allows five)
+SLOW_SECONDS = 3.0
+
+ROW_KEYS = {
+    "dispatchId",
+    "taskId",
+    "runId",
+    "workerState",
+    "dispatchStatus",
+    "terminalState",
+    "resource",
+    "projection",
+}
+RESOURCE_KEYS = {
+    "id",
+    "ownershipState",
+    "releaseState",
+    "worktreeId",
+    "ownerDispatchId",
+    "originDispatchId",
+    "recoveryAttemptCount",
+}
+PROJECTION_KEYS = {
+    "outcome",
+    "role",
+    "provider",
+    "host",
+    "workspace",
+    "stage",
+    "nextAction",
+    "liveness",
+    "evidence",
+}
+LEAK = re.compile(r"/|\\|term_|://|[A-Za-z0-9_+=-]{32,}|[A-Fa-f0-9]{24,}|@")
+RULES = [
+    "dispatchId, taskId, runId, resource.id, worktreeId, host.id, workspace.id replaced by stable placeholders (w-001, t-001, run-a, res-001, wt-001, host-a, ws-a)",
+    "resource.ownerDispatchId and originDispatchId mapped to the dispatch placeholder when they name a collected row, else w-ext-N",
+    "stage.detail and stage.activity replaced by fixed synthetic text (free text is never copied)",
+    "all timestamps shifted by one constant so the newest lands on 2026-11-08T12:00:00Z; unparsable ones become redacted-time",
+    "keys outside the verified worker-list set are kept by name only with the value redacted; page.nextCursor becomes cursor-1; warnings become redacted warning",
+    "any remaining string containing a slash, a terminal handle marker, a URL, an at sign or a 24+ character token is replaced by redacted",
+]
+
+
+class Placeholders:
+    def __init__(self, prefix: str, width: int = 3, letters: bool = False):
+        self.prefix, self.width, self.letters, self.seen = prefix, width, letters, {}
+
+    def __call__(self, value):
+        if not isinstance(value, str) or not value:
+            return value
+        if value not in self.seen:
+            n = len(self.seen)
+            self.seen[value] = (
+                f"{self.prefix}{chr(ord('a') + n % 26) * (n // 26 + 1)}"
+                if self.letters
+                else f"{self.prefix}{n + 1:0{self.width}d}"
+            )
+        return self.seen[value]
+
+
+def shift_times(obj, delta: float):
+    """Return ``obj`` with every liveness.observedAt and evidence.lastObservedAt moved by ``delta``."""
+
+    def move(value):
+        stamp = parse_timestamp(value)
+        return "redacted-time" if stamp is None else format_utc_iso(stamp + delta)
+
+    for row in obj:
+        projection = row.get("projection") or {}
+        for group, key in (("liveness", "observedAt"), ("evidence", "lastObservedAt")):
+            node = projection.get(group)
+            if isinstance(node, dict) and key in node and node[key] is not None:
+                node[key] = move(node[key])
+
+
+def scrub(value):
+    if isinstance(value, str):
+        return "redacted" if LEAK.search(value) else value
+    if isinstance(value, dict):
+        return {k: scrub(v) for k, v in value.items()}
+    if isinstance(value, list):
+        return [scrub(v) for v in value]
+    return value
+
+
+def redact(raw: dict) -> dict:
+    """Redact one decoded worker-list envelope (a new object; ``raw`` is not kept)."""
+    result = raw.get("result") if isinstance(raw, dict) else None
+    if not isinstance(result, dict) or not isinstance(result.get("workers"), list):
+        raise ValueError("the live reply is not a worker-list envelope")
+    dispatch, task, run = (
+        Placeholders("w-"),
+        Placeholders("t-"),
+        Placeholders("run-", letters=True),
+    )
+    res, wt, host, ws = (
+        Placeholders("res-"),
+        Placeholders("wt-"),
+        Placeholders("host-", letters=True),
+        Placeholders("ws-", letters=True),
+    )
+    workers = [w for w in result["workers"] if isinstance(w, dict)]
+    for w in workers:  # first pass: every dispatch id gets its placeholder, in order
+        dispatch(w.get("dispatchId"))
+    rows = []
+    for w in workers:
+        row = {}
+        for key, value in w.items():
+            if key not in ROW_KEYS:
+                row[key] = "redacted"  # an unknown key survives by name only
+        for key, mapper in (("dispatchId", dispatch), ("taskId", task), ("runId", run)):
+            if key in w:
+                row[key] = mapper(w[key])
+        for key in ("workerState", "dispatchStatus", "terminalState"):
+            if key in w:
+                row[key] = w[key]
+        resource = w.get("resource")
+        if isinstance(resource, dict):
+            out = {k: "redacted" for k in resource if k not in RESOURCE_KEYS}
+            if "id" in resource:
+                out["id"] = res(resource["id"])
+            if "worktreeId" in resource:
+                out["worktreeId"] = wt(resource["worktreeId"])
+            for key in ("ownerDispatchId", "originDispatchId"):
+                if key in resource:
+                    known = (
+                        isinstance(resource[key], str)
+                        and resource[key] in dispatch.seen
+                    )
+                    out[key] = dispatch(resource[key]) if known else "w-ext-1"
+            for key in ("ownershipState", "releaseState", "recoveryAttemptCount"):
+                if key in resource:
+                    out[key] = resource[key]
+            row["resource"] = out
+        projection = w.get("projection")
+        if isinstance(projection, dict):
+            out = {k: "redacted" for k in projection if k not in PROJECTION_KEYS}
+            for key in ("outcome", "role"):
+                if key in projection:
+                    out[key] = projection[key]
+            for group, fields in (
+                ("provider", ("id",)),
+                ("host", ("kind",)),
+                ("workspace", ("kind",)),
+                ("stage", ("worker", "dispatch")),
+                ("nextAction", ("kind",)),
+                ("liveness", ("verdict", "source", "observedAt")),
+                ("evidence", ("durable", "liveStatus", "lastObservedAt")),
+            ):
+                node = projection.get(group)
+                if isinstance(node, dict):
+                    out[group] = {f: node[f] for f in fields if f in node}
+            if isinstance(projection.get("host"), dict) and "id" in projection["host"]:
+                out.setdefault("host", {})["id"] = host(projection["host"]["id"])
+            if (
+                isinstance(projection.get("workspace"), dict)
+                and "id" in projection["workspace"]
+            ):
+                out.setdefault("workspace", {})["id"] = ws(
+                    projection["workspace"]["id"]
+                )
+            stage = projection.get("stage")
+            if isinstance(stage, dict):
+                for key, text in (
+                    ("activity", "redacted activity"),
+                    ("detail", "redacted detail"),
+                ):
+                    if stage.get(key) is not None:
+                        out.setdefault("stage", {})[key] = text
+            row["projection"] = out
+        rows.append(row)
+    stamps = [
+        parse_timestamp(
+            ((r.get("projection") or {}).get("liveness") or {}).get("observedAt")
+        )
+        for r in rows
+    ]
+    stamps += [
+        parse_timestamp(
+            ((r.get("projection") or {}).get("evidence") or {}).get("lastObservedAt")
+        )
+        for r in rows
+    ]
+    known = [s for s in stamps if s is not None]
+    shift_times(rows, ANCHOR_TIME - max(known) if known else 0.0)
+    page = result.get("page") if isinstance(result.get("page"), dict) else {}
+    out_page = {k: page[k] for k in ("hasMore", "total", "limit") if k in page}
+    if page.get("nextCursor"):
+        out_page["nextCursor"] = "cursor-1"
+    new = {"workers": rows, "page": out_page}
+    scope = result.get("scope")
+    if isinstance(scope, dict) and "source" in scope:
+        new["scope"] = {"source": scope["source"]}
+    counts = result.get("counts")
+    if isinstance(counts, dict):
+        new["counts"] = {
+            k: v for k, v in counts.items() if isinstance(v, (int, float, bool))
+        }
+    if isinstance(result.get("warnings"), list):
+        new["warnings"] = ["redacted warning" for _ in result["warnings"]]
+    return {"result": scrub(new)}
+
+
+def variants(sample: dict) -> dict[str, dict]:
+    """The four golden kinds as fixture files: success, missing, stale and contradictory."""
+
+    def wrap(name, description, cycles):
+        return {"variant": name, "description": description, "cycles": cycles}
+
+    missing = copy.deepcopy(sample)
+    missing["result"].pop("scope", None)
+    missing["result"]["page"].pop("total", None)
+    first = missing["result"]["workers"][0] if missing["result"]["workers"] else {}
+    for group, key in (
+        ("liveness", "verdict"),
+        ("evidence", "liveStatus"),
+        ("nextAction", "kind"),
+    ):
+        node = (first.get("projection") or {}).get(group)
+        if isinstance(node, dict) and key in node:
+            del node[key]
+            break
+    contradictory_1 = copy.deepcopy(sample)
+    rows = contradictory_1["result"]["workers"]
+    if rows:
+        rows.append(copy.deepcopy(rows[0]))  # a duplicate dispatchId
+    contradictory_2 = copy.deepcopy(sample)
+    first = (
+        contradictory_2["result"]["workers"][0]
+        if contradictory_2["result"]["workers"]
+        else None
+    )
+    if first is not None:
+        live = (first.get("projection") or {}).get("liveness")
+        if isinstance(live, dict):
+            live["observedAt"] = format_utc_iso(
+                ANCHOR_TIME - 86400
+            )  # a day older than the first cycle
+    fail = {"fail": "timeout"}
+    return {
+        "golden-success": wrap(
+            "golden-success", "one redacted live worker-list read", [sample]
+        ),
+        "golden-missing": wrap(
+            "golden-missing",
+            "the sample without result.scope, page.total and one inner projection key",
+            [missing],
+        ),
+        "golden-stale": wrap(
+            "golden-stale",
+            "the sample, then failing cycles (the test moves the fake monotonic clock past 45 s)",
+            [sample, fail, fail, fail],
+        ),
+        "golden-contradictory": wrap(
+            "golden-contradictory",
+            "a duplicate dispatchId, then a backward timestamp",
+            [contradictory_1, contradictory_2],
+        ),
+    }
+
+
+def write_fixture(name: str, data: dict) -> None:
+    text = (
+        '{\n "variant": '
+        + json.dumps(data["variant"])
+        + ',\n "description": '
+        + json.dumps(data["description"])
+        + ',\n "cycles": [\n'
+    )
+    text += (
+        ",\n".join(
+            "  " + json.dumps(c, ensure_ascii=True, separators=(",", ":"))
+            for c in data["cycles"]
+        )
+        + "\n ]\n}\n"
+    )
+    (FIXTURES / f"{name}.json").write_text(text, encoding="utf-8")
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser()
+    parser.add_argument("--timing-note", required=True)
+    args = parser.parse_args()
+
+    orca = adapter._find_orca()
+    if orca is None:
+        print("BLOCKED: no Orca CLI validated; nothing was recorded", file=sys.stderr)
+        return 3
+    argv = adapter.build_argv(orca)
+    durations: list[float] = []
+    sample = None
+    for call in range(MAX_CALLS):
+        started = time.monotonic()
+        try:
+            returncode, stdout, _stderr = adapter.production_runner(
+                argv, adapter.PER_CALL_TIMEOUT
+            )
+        except adapter.RunnerFailure as exc:
+            print(
+                f"BLOCKED: the live call failed ({exc.code}); nothing was recorded",
+                file=sys.stderr,
+            )
+            return 3
+        durations.append(time.monotonic() - started)
+        if returncode != 0:
+            print(
+                f"BLOCKED: the live call exited {returncode}; nothing was recorded",
+                file=sys.stderr,
+            )
+            return 3
+        if sample is None:
+            try:
+                sample = redact(
+                    json.loads(stdout)
+                )  # the raw text is dropped right here
+            except ValueError as exc:
+                print(f"BLOCKED: {exc}; nothing was recorded", file=sys.stderr)
+                return 3
+        del stdout
+    for name, data in variants(sample).items():
+        write_fixture(name, data)
+
+    slowest = max(durations)
+    if slowest > SLOW_SECONDS:
+        decision = f"raise the per-call timeout to {min(max(3 * slowest, 5.0), 14.0):.1f} s (three times the slowest call, clamped to 5 to 14 s)"
+    else:
+        decision = f"keep the {adapter.PER_CALL_TIMEOUT:.0f} s default; it stays unmeasured beyond this run (slowest call {slowest:.2f} s)"
+    rows = len(sample["result"]["workers"])
+    note = [
+        "# T13: golden worker-list samples and per-call timing",
+        "",
+        f"Calls made: {len(durations)} (one for the sample, the rest only to time the call). Rows in the sample: {rows}.",
+        "",
+        "| Call | Duration (s) |",
+        "|---|---|",
+        *[f"| {i} | {d:.3f} |" for i, d in enumerate(durations, 1)],
+        "",
+        f"Slowest: {slowest:.3f} s. Decision: {decision}.",
+        "",
+        "Redaction rules applied:",
+        "",
+        *[f"- {rule}" for rule in RULES],
+        "",
+        "Orca version string: not read (only the two allowed read-only calls are made, and neither reports one).",
+        "",
+        "Not measured: behaviour under load, a reply with more than one page, a reply with a non-empty `warnings` list unless the sample had one, any failing call. The fixtures were written to `src/superclaude/cli/observe/fixtures/golden-*.json`.",
+        "",
+    ]
+    Path(args.timing_note).write_text("\n".join(note), encoding="utf-8")
+    print(
+        f"recorded {rows} rows; durations {['%.3f' % d for d in durations]}; decision: {decision}"
+    )
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/tests/observe/test_golden_contract.py b/tests/observe/test_golden_contract.py
new file mode 100644
index 000000000..3bc0e6f06
--- /dev/null
+++ b/tests/observe/test_golden_contract.py
@@ -0,0 +1,365 @@
+"""Contract tests over the four redacted golden worker-list samples (release-gates.md data gate; T32)."""
+
+from __future__ import annotations
+
+import copy
+import json
+import re
+from importlib import resources
+
+import pytest
+from rich.cells import cell_len
+
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.parse import FIXTURE_PACKAGE, load_fixture
+from superclaude.cli.observe.render import screen_lines
+from superclaude.cli.observe.terminal import resolve_policy
+from superclaude.cli.observe.view import Session, build_view
+from tests.observe import record_golden
+from tests.observe.conftest import FakeDiscover, FakeRunner
+from tests.observe.test_fixtures import SENSITIVE
+
+GOLDEN = ("golden-success", "golden-missing", "golden-stale", "golden-contradictory")
+
+
+def result_of(name, clock, cycles=1):
+    collector = Collector(FixtureSource(name), clock)
+    for _ in range(cycles):
+        result = collector.run_once()
+    return result
+
+
+def view_of(result, clock, show_historical=True):
+    return build_view(result, Session(show_historical=show_historical), clock)
+
+
+def policy(width, height=40):
+    return resolve_policy({}, "utf-8", {}, width, height)
+
+
+# -- success --------------------------------------------------------------------------------------------------
+
+
+def test_the_success_sample_parses_and_renders_at_160_116_and_80_columns(fake_clock):
+    result = result_of("golden-success", fake_clock)
+    assert (
+        result.state == "PARTIAL" and result.code is None
+    )  # hasMore is true in the live reply
+    view = view_of(result, fake_clock)
+    assert len(view.all_rows) == 100 and result.coverage.reported_total == 428
+    assert any(
+        t.text.startswith("PARTIAL: collected 100 of reported 428")
+        for t in view.counts_tokens
+    )
+    for width in (160, 116, 80):
+        lines = screen_lines(view, policy(width))
+        assert lines and all(cell_len(line) <= width for line in lines)
+        assert any("collected 100 / reported 428" in line for line in lines)
+    assert "scope=all" in view.header1
+
+
+def test_the_success_sample_is_redacted_to_stable_placeholders():
+    data = load_fixture("golden-success").cycle(0).envelope["result"]
+    rows = data["workers"]
+    assert all(re.fullmatch(r"w-\d{3}", r["dispatchId"]) for r in rows)
+    assert all(re.fullmatch(r"run-[a-z]+", r["runId"]) for r in rows)
+    assert all(re.fullmatch(r"t-\d{3}", r["taskId"]) for r in rows)
+    assert all(r["projection"]["stage"]["detail"] == "redacted detail" for r in rows)
+    assert (
+        data["page"]["nextCursor"] == "cursor-1"
+    )  # the opaque live cursor is never kept
+    for row in rows:  # keys outside the verified set survive by name only
+        for key in set(row) - {
+            "dispatchId",
+            "taskId",
+            "runId",
+            "workerState",
+            "dispatchStatus",
+            "terminalState",
+            "resource",
+            "projection",
+        }:
+            assert row[key] == "redacted"
+
+
+# -- missing --------------------------------------------------------------------------------------------------------
+
+
+def test_the_missing_sample_reads_scope_unknown_reported_unknown_and_unknown_for_the_removed_key(
+    fake_clock,
+):
+    result = result_of("golden-missing", fake_clock)
+    view = view_of(result, fake_clock)
+    assert view.scope_text == "scope unknown" and "scope unknown" in view.header1
+    assert view.collected_text.endswith("reported unknown")
+    first = next(rv for rv in view.all_rows if rv.dispatch_id == "w-001")
+    # the recorder removes liveness.verdict from the first row (real rows always carry it)
+    assert "liveness_verdict" in first.raw.absent_fields
+    assert first.liveness.startswith("unknown (")
+    assert (
+        dict(first.inspector)["projection.nextAction.kind"]
+        != "unknown (absent in source)"
+    )
+    assert all(
+        rv.dispatch_id != "unknown" for rv in view.all_rows
+    )  # a missing inner key is not an error
+
+
+# -- stale ---------------------------------------------------------------------------------------------------------------
+
+
+def test_stale_comes_from_monotonic_time_since_the_last_success_not_from_sample_timestamps(
+    fake_clock,
+):
+    collector = Collector(FixtureSource("golden-stale"), fake_clock)
+    good = collector.run_once()
+    fake_clock.advance(44)
+    assert view_of(good, fake_clock).source_state == "OK"
+    fake_clock.advance(1)
+    stale = view_of(good, fake_clock)
+    assert (
+        stale.source_state == "STALE"
+        and stale.freshness_cells[0] == "worker-list STALE 45s"
+    )
+    fake_clock.jump_wall(-3600)  # wall-clock jumps change nothing
+    assert view_of(good, fake_clock).source_state == "STALE"
+    failing = [collector.run_once() for _ in range(3)]
+    view = view_of(failing[-1], fake_clock)
+    assert [r.state for r in failing] == ["FAILED"] * 3
+    assert (
+        view.freshness_cells[0] == "worker-list FAILED (timeout) 45s"
+    )  # FAILED outranks STALE
+    assert failing[-1].snapshot is good.snapshot and len(view.all_rows) == 100
+
+
+def test_a_fresh_poll_with_old_evidence_timestamps_is_not_stale(fake_clock):
+    result = result_of("golden-success", fake_clock)
+    fake_clock.jump_wall(
+        20 * 60
+    )  # the worker evidence is now 20 minutes old; the poll is fresh
+    view = view_of(result, fake_clock)
+    assert view.source_state == "OK" and view.poll_age == "0s"
+    ages = {rv.evidence_age for rv in view.all_rows}
+    assert "20m" in ages  # the newest evidence in the sample
+    assert all(
+        re.fullmatch(r"\d+[mh]|unknown", age) for age in ages
+    )  # none of it is seconds old
+
+
+# -- contradictory ---------------------------------------------------------------------------------------------------------
+
+
+def test_the_contradictory_sample_shows_duplicates_and_a_backward_timestamp(fake_clock):
+    collector = Collector(FixtureSource("golden-contradictory"), fake_clock)
+    first = collector.run_once()
+    assert view_of(first, fake_clock).duplicates_note == "1 duplicate rows ignored"
+    second = collector.run_once()
+    view = view_of(second, fake_clock)
+    row = next(rv for rv in view.all_rows if rv.dispatch_id == "w-001")
+    assert "conflict (time went back)" in row.flags
+    assert (
+        row.raw.liveness_observed_at
+        != load_fixture("golden-contradictory")
+        .cycle(1)
+        .envelope["result"]["workers"][0]["projection"]["liveness"]["observedAt"]
+    )
+
+
+# -- T32: a broken envelope keeps the last good snapshot -------------------------------------------------------------------
+
+
+def broken_copies():
+    base = load_fixture("golden-success").cycle(0).envelope
+    for label, mutate in (
+        ("no result", lambda d: d.pop("result")),
+        ("no workers", lambda d: d["result"].pop("workers")),
+        ("no hasMore", lambda d: d["result"]["page"].pop("hasMore")),
+        ("hasMore string", lambda d: d["result"]["page"].update(hasMore="false")),
+        ("workers not a list", lambda d: d["result"].update(workers={})),
+    ):
+        copied = copy.deepcopy(base)
+        mutate(copied)
+        yield label, copied
+
+
+@pytest.mark.parametrize("label", [label for label, _ in broken_copies()])
+def test_removing_result_workers_or_has_more_gives_failed_shape_with_the_last_good_snapshot(
+    fake_clock, argv_log, label
+):
+    good = json.dumps(load_fixture("golden-success").cycle(0).envelope)
+    broken = json.dumps(dict(broken_copies())[label])
+    runner = FakeRunner(argv_log, [(0, good), (0, broken)])
+    collector = Collector(LiveSource(runner, FakeDiscover(argv_log)), fake_clock)
+    first = collector.run_once()
+    second = collector.run_once()
+    assert (second.state, second.code) == ("FAILED", "shape")
+    assert second.snapshot is first.snapshot and len(second.snapshot.rows) == 100
+    view = view_of(second, fake_clock)
+    assert view.freshness_cells[0].startswith("worker-list FAILED (shape)")
+    assert second.last_success_mono == first.last_success_mono
+
+
+# -- nothing sensitive is committed ---------------------------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("name", GOLDEN)
+def test_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte(name):
+    text = (
+        resources.files(FIXTURE_PACKAGE)
+        .joinpath(f"{name}.json")
+        .read_text(encoding="utf-8")
+    )
+    assert "\x1b" not in text and text.isascii()
+    for what, pattern in SENSITIVE.items():
+        assert not pattern.search(text), f"{name}: {what}"
+    assert not re.search(r"[A-Za-z0-9_+=-]{32,}", text.replace("redacted", ""))
+
+
+# -- the recorder's redaction ------------------------------------------------------------------------------------------------------
+
+
+def synthetic_envelope():
+    return {
+        "result": {
+            "workers": [
+                {
+                    "dispatchId": "disp_9f8e7d6c5b4a39281706",
+                    "taskId": "task_real_1",
+                    "runId": "run_real_9",
+                    "agentTerminalHandle": "term_abcdef0123456789abcdef0123456789",
+                    "workerState": "running",
+                    "dispatchStatus": "dispatched",
+                    "terminalState": "retained",
+                    "resource": {
+                        "id": "res_real",
+                        "worktreeId": "/home/someone/work/tree",
+                        "ownerDispatchId": "disp_9f8e7d6c5b4a39281706",
+                        "originDispatchId": "disp_somebody_else",
+                        "terminalHandle": "term_secret",
+                        "ownershipState": "owned",
+                    },
+                    "projection": {
+                        "outcome": "in_progress",
+                        "host": {"id": "host.example.com", "kind": "local"},
+                        "workspace": {"id": "/home/someone/work", "kind": "worktree"},
+                        "stage": {
+                            "worker": "ready",
+                            "dispatch": "dispatched",
+                            "detail": "editing /etc/passwd with token sk-abcdef0123456789abcdef",
+                            "activity": "x",
+                        },
+                        "nextAction": {"kind": "none"},
+                        "liveness": {
+                            "verdict": "live",
+                            "source": "agent_status",
+                            "observedAt": "2026-01-01T10:00:00Z",
+                        },
+                        "evidence": {
+                            "durable": True,
+                            "liveStatus": "fresh",
+                            "lastObservedAt": "2026-01-01T09:59:00Z",
+                        },
+                        "attention": {"free": "text"},
+                    },
+                },
+                {"dispatchId": "disp_second", "workerState": "idle"},
+                "not an object",
+            ],
+            "page": {
+                "hasMore": True,
+                "total": 9,
+                "limit": 100,
+                "nextCursor": "opaque/cursor==",
+            },
+            "scope": {"source": "bound", "runId": "run_real_9"},
+            "counts": {"released": 3, "note": "text"},
+            "warnings": ["a warning with /home/path"],
+        }
+    }
+
+
+def test_redaction_replaces_identifiers_free_text_paths_handles_and_cursors():
+    out = record_golden.redact(synthetic_envelope())
+    text = json.dumps(out)
+    for leaked in (
+        "disp_",
+        "task_real",
+        "run_real",
+        "term_",
+        "/home",
+        "/etc",
+        "sk-",
+        "someone",
+        "example.com",
+        "opaque",
+        "secret",
+        "text",
+    ):
+        assert leaked not in text, leaked
+    rows = out["result"]["workers"]
+    assert [r["dispatchId"] for r in rows] == ["w-001", "w-002"]
+    first = rows[0]
+    assert (
+        first["taskId"] == "t-001"
+        and first["runId"] == "run-a"
+        and first["agentTerminalHandle"] == "redacted"
+    )
+    assert (
+        first["resource"]["ownerDispatchId"] == "w-001"
+        and first["resource"]["originDispatchId"] == "w-ext-1"
+    )
+    assert (
+        first["resource"]["worktreeId"] == "wt-001"
+        and first["resource"]["terminalHandle"] == "redacted"
+    )
+    assert (
+        first["projection"]["stage"]["detail"] == "redacted detail"
+        and first["projection"]["attention"] == "redacted"
+    )
+    assert first["projection"]["host"] == {"kind": "local", "id": "host-a"}
+    assert out["result"]["page"] == {
+        "hasMore": True,
+        "total": 9,
+        "limit": 100,
+        "nextCursor": "cursor-1",
+    }
+    assert out["result"]["scope"] == {"source": "bound"} and out["result"][
+        "counts"
+    ] == {"released": 3}
+    assert out["result"]["warnings"] == ["redacted warning"]
+
+
+def test_redaction_shifts_every_timestamp_by_one_constant_so_the_newest_lands_on_the_anchor():
+    out = record_golden.redact(synthetic_envelope())
+    live = out["result"]["workers"][0]["projection"]
+    assert live["liveness"]["observedAt"] == "2026-11-08T12:00:00Z"
+    assert (
+        live["evidence"]["lastObservedAt"] == "2026-11-08T11:59:00Z"
+    )  # the one-minute gap survives
+
+
+def test_redaction_refuses_something_that_is_not_a_worker_list_envelope():
+    for bad in ({}, {"result": {}}, {"result": {"workers": "x"}}, [], None):
+        with pytest.raises(ValueError):
+            record_golden.redact(bad)
+
+
+def test_the_four_golden_kinds_are_derived_from_one_sample():
+    kinds = record_golden.variants(record_golden.redact(synthetic_envelope()))
+    assert set(kinds) == set(GOLDEN)
+    assert "scope" not in kinds["golden-missing"]["cycles"][0]["result"]
+    assert "total" not in kinds["golden-missing"]["cycles"][0]["result"]["page"]
+    assert [c.get("fail") for c in kinds["golden-stale"]["cycles"]] == [
+        None,
+        "timeout",
+        "timeout",
+        "timeout",
+    ]
+    first, second = kinds["golden-contradictory"]["cycles"]
+    ids = [w["dispatchId"] for w in first["result"]["workers"]]
+    assert len(ids) == 3 and ids[0] == ids[-1]
+    assert (
+        second["result"]["workers"][0]["projection"]["liveness"]["observedAt"]
+        < "2026-11-08T12:00:00Z"
+    )

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

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
