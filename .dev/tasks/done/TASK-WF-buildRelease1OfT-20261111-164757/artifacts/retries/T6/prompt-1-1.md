635f7a4d45c4158cfed22e55ae7441ed8d2ed533
Review one task for spec compliance.

Task brief: 
## Task 6: Build the read-only adapter `adapter.py`

Depends on: Task 2, Task 4, Task 5

Create `src/superclaude/cli/observe/adapter.py` and `tests/observe/test_adapter.py`, following `ARCHITECTURE-SPINE.md` AD-3, AD-4 and AD-5 and `adapter-contract.md` sections "Argv allow-list", "Bounds per cycle" and "Paging, errors, sanitizing". Contents: `Runner = Callable[[list, float], tuple]` and `Discover = Callable[[], str | None]` (default `_find_orca` imported from `superclaude.cli.install_user_setup`, unchanged); `build_argv(orca, run_id=None, cursor=None)` built only from the literal tuple `(orca, "orchestration", "worker-list", "--json", "--limit", "100")` plus optional `("--run", run_id)` and `("--cursor", cursor)` as separate argv items (never `--opt=value`); a `runId` format check (PROPOSED regex `^[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}$`); a cursor guard that rejects a leading `-`, a NUL byte or more than 2048 bytes (PROPOSED bound) and otherwise passes the cursor through unchanged; a `FORBIDDEN_PREFIXES` set checked before every call; `production_runner(argv, timeout)` that uses `subprocess.Popen` with no shell, `stdin=DEVNULL`, `start_new_session=True`, reads stdout in chunks and kills the process group once 8 MiB is exceeded, drains stderr on a separate thread into a 2 KiB buffer, and on timeout or overflow kills the process group (`os.killpg(SIGKILL)` on POSIX, `proc.kill()` elsewhere) and reaps it; a frozen `SourceResult` (state `OK`, `FAILED` or `PARTIAL`, decoded JSON of the pages read, a sanitized diagnostic, and a code from the closed set `exit:<n>`, `timeout`, `spawn-error`, `output-cap`, `json`, `shape`, `not-found`, `overrun`, `cursor-rejected`, `cursor-stalled`, `empty-page`); and `LiveSource(runner, discover, per_call_timeout)` that runs discovery once (`None` means not available, no cycle starts), derives `source.namespace` from the resolved absolute path of the validated Orca CLI, and has `read_pages(clock, budget_deadline, run_id=None)` which pages by `result.page.nextCursor` for at most 5 subprocesses, gives each call the smaller of the per-call timeout (a named constant, 10 s, UNVERIFIED until Task 13) and the time left in the budget, stops with `cursor-stalled` when `hasMore` is true and the cursor is absent, empty or already used, with `cursor-rejected` when the guard refuses it, and with `empty-page` when a page has no workers while its total is above 0. It peeks only at `hasMore`, `nextCursor` and `total`; strict validation stays in `parse.py`. It imports `subprocess` here and nowhere else in the package, and imports `sanitize` but not `parse` or `collector`.

Acceptance criteria:
- [T6.AC1] `uv run pytest tests/observe/test_adapter.py -v` passes.
- [T6.AC2] T1: every argv the fake runner and fake `Discover` receive across all adapter code paths equals the worker-list template (with its optional pairs) or the discovery argv `(<binary>, "skills", "list", "--json")`; discovery is intercepted by patching the `subprocess.run` that `_find_orca()` calls.
- [T6.AC3] T2: a static test asserts the strings `--ack`, `--wait` and `--retry-request` appear in `adapter.py` only inside the forbidden set, and that `check` is not a template.
- [T6.AC4] T36 and T37: with the real subprocess calls patched to raise, an unlisted argv fails loudly; a value starting with `-`, a malformed `runId`, a NUL or oversized cursor and every forbidden prefix are rejected before any call.
- [T6.AC5] T4 (adapter half): a fake that always answers `hasMore=true` with advancing cursors makes exactly 5 calls and returns state `PARTIAL`.
- [T6.AC6] Tests marked `observe_real_process` show the production runner kills a child that sleeps past the timeout and reaps it, kills a child that writes more than 8 MiB, keeps at most 2 KiB of stderr, and returns `spawn-error` when the binary does not exist.
- [T6.AC7] A test shows `Discover` returning `None` yields not-available with zero worker-list calls.

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

Start sha: 635f7a4d45c4158cfed22e55ae7441ed8d2ed533
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/adapter.py b/src/superclaude/cli/observe/adapter.py
new file mode 100644
index 000000000..cc54811dc
--- /dev/null
+++ b/src/superclaude/cli/observe/adapter.py
@@ -0,0 +1,401 @@
+"""The one read-only edge to the Orca CLI (AD-3, AD-4, AD-5).
+
+Only two argv shapes are ever run: the worker-list template (with optional run and cursor
+pairs) and the one-time binary discovery probe that ``_find_orca`` makes. Every argv is
+checked against a forbidden set before any call, and the set only ever grows.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import re
+import signal
+import subprocess
+import threading
+from collections.abc import Callable
+from dataclasses import dataclass
+from typing import Any
+
+from superclaude.cli.install_user_setup import _find_orca
+from superclaude.cli.observe.sanitize import sanitize
+
+Runner = Callable[
+    [list, float], tuple
+]  # (argv, timeout) -> (returncode, stdout[, stderr])
+Discover = Callable[[], "str | None"]
+
+WORKER_LIST_TEMPLATE = ("orchestration", "worker-list", "--json", "--limit", "100")
+DISCOVERY_TEMPLATE = ("skills", "list", "--json")
+# Matched by prefix against every verb and flag position, never against run or cursor values.
+FORBIDDEN_PREFIXES = frozenset(
+    {"check", "--ack", "--wait", "--retry-request", "dispatch", "inbox"}
+)
+
+RUN_ID_PATTERN = re.compile(
+    r"^[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}$"
+)  # PROPOSED, not an Orca format
+CURSOR_MAX_BYTES = 2048  # PROPOSED
+
+MAX_CALLS_PER_CYCLE = 5
+MAX_OUTPUT_BYTES = 8 * 1024 * 1024
+STDERR_KEEP_BYTES = 2048
+PER_CALL_TIMEOUT = (
+    10.0  # seconds; UNVERIFIED until the first permitted live read measures it
+)
+KILL_GRACE_SECONDS = 2.0
+
+# Closed set of source codes besides ``exit:<n>``.
+CODES = frozenset(
+    {
+        "timeout",
+        "spawn-error",
+        "output-cap",
+        "json",
+        "shape",
+        "not-found",
+        "overrun",
+        "cursor-rejected",
+        "cursor-stalled",
+        "empty-page",
+    }
+)
+
+
+class ArgvRejected(ValueError):
+    """An argv or one of its values was refused before any call. ``code`` says why."""
+
+    def __init__(self, code: str, detail: str = ""):
+        super().__init__(f"{code}: {detail}" if detail else code)
+        self.code = code
+
+
+class RunnerFailure(Exception):
+    """A runner could not give a normal (returncode, stdout): ``code`` is a source code."""
+
+    def __init__(self, code: str, stderr: str = ""):
+        super().__init__(code)
+        self.code = code
+        self.stderr = stderr
+
+
+# -- argv construction and checks ------------------------------------------------------------
+
+
+def check_run_id(run_id: object) -> str:
+    if not isinstance(run_id, str) or not RUN_ID_PATTERN.match(run_id):
+        raise ArgvRejected("run-id", "malformed run id")
+    return run_id
+
+
+def check_cursor(cursor: object) -> str:
+    """The cursor is opaque: only its byte bound and its first character are checked."""
+    if not isinstance(cursor, str) or not cursor:
+        raise ArgvRejected("cursor-rejected", "cursor is not a non-empty string")
+    if cursor.startswith("-"):
+        raise ArgvRejected("cursor-rejected", "cursor starts with '-'")
+    if "\x00" in cursor:
+        raise ArgvRejected("cursor-rejected", "cursor holds a NUL byte")
+    if len(cursor.encode("utf-8", errors="replace")) > CURSOR_MAX_BYTES:
+        raise ArgvRejected("cursor-rejected", "cursor is over the byte bound")
+    return cursor
+
+
+def _option_positions(tokens: list[str]) -> set[int]:
+    """Indexes (into ``tokens``) that are verbs or flags rather than option values."""
+    positions = set(range(len(tokens)))
+    if tokens[:5] == list(WORKER_LIST_TEMPLATE):
+        i = 5
+        while i + 1 < len(tokens) and tokens[i] in ("--run", "--cursor"):
+            positions.discard(i + 1)
+            i += 2
+    return positions
+
+
+def assert_allowed(argv: list) -> None:
+    """Refuse any argv that is not one of the two templates; names the forbidden token."""
+    if not argv or not all(isinstance(a, str) for a in argv) or len(argv) < 2:
+        raise ArgvRejected("argv", "not a list of strings")
+    if argv[0].startswith("-") or not argv[0]:
+        raise ArgvRejected("argv", "binary path is empty or starts with '-'")
+    tokens = list(argv[1:])
+    for index in sorted(_option_positions(tokens)):
+        for prefix in FORBIDDEN_PREFIXES:
+            if tokens[index].startswith(prefix):
+                raise ArgvRejected(
+                    "forbidden", f"{tokens[index]!r} is on the forbidden list"
+                )
+    if tokens == list(DISCOVERY_TEMPLATE):
+        return
+    if tokens[:5] != list(WORKER_LIST_TEMPLATE):
+        raise ArgvRejected("argv", "not an allow-listed argv")
+    rest = tokens[5:]
+    seen: list[str] = []
+    while rest:
+        if len(rest) < 2 or rest[0] not in ("--run", "--cursor") or rest[0] in seen:
+            raise ArgvRejected("argv", "unexpected option")
+        flag, value = rest[0], rest[1]
+        if flag == "--run":
+            check_run_id(value)
+        else:
+            check_cursor(value)
+        if value.startswith("-"):
+            raise ArgvRejected("argv", "option value starts with '-'")
+        seen.append(flag)
+        rest = rest[2:]
+    if seen not in ([], ["--run"], ["--cursor"], ["--run", "--cursor"]):
+        raise ArgvRejected("argv", "options out of order")
+
+
+def build_argv(
+    orca: str, run_id: str | None = None, cursor: str | None = None
+) -> list[str]:
+    """The worker-list argv: literal template plus optional separate-item pairs."""
+    argv = [orca, *WORKER_LIST_TEMPLATE]
+    if run_id is not None:
+        argv += ["--run", check_run_id(run_id)]
+    if cursor is not None:
+        argv += ["--cursor", check_cursor(cursor)]
+    assert_allowed(argv)
+    return argv
+
+
+# -- the production runner --------------------------------------------------------------------
+
+
+def _kill_group(proc: subprocess.Popen) -> None:
+    try:
+        if hasattr(os, "killpg"):
+            os.killpg(proc.pid, signal.SIGKILL)
+        else:
+            proc.kill()
+    except (ProcessLookupError, PermissionError):
+        proc.kill()
+    except OSError:
+        pass
+    try:
+        proc.wait(timeout=KILL_GRACE_SECONDS)  # reap, so no zombie is left behind
+    except subprocess.TimeoutExpired:
+        pass
+
+
+def production_runner(argv: list, timeout: float) -> tuple[int, str, str]:
+    """Run ``argv`` with no shell, in its own session; return (returncode, stdout, stderr).
+
+    Raises ``RunnerFailure`` with code ``timeout``, ``output-cap`` or ``spawn-error``. On the
+    first two the whole process group is killed and reaped. stdout over 8 MiB ends the call;
+    stderr is drained on its own thread and only its first 2 KiB is kept.
+    """
+    try:
+        proc = subprocess.Popen(
+            argv,
+            stdin=subprocess.DEVNULL,
+            stdout=subprocess.PIPE,
+            stderr=subprocess.PIPE,
+            start_new_session=True,
+        )
+    except OSError as exc:
+        raise RunnerFailure("spawn-error", str(exc)) from exc
+
+    out_chunks: list[bytes] = []
+    err_chunks: list[bytes] = []
+    state = {"out": 0, "err": 0, "overflow": False}
+    stdout_done = threading.Event()
+
+    def read_stdout() -> None:
+        try:
+            while True:
+                chunk = proc.stdout.read1(65536)
+                if not chunk:
+                    return
+                state["out"] += len(chunk)
+                if state["out"] > MAX_OUTPUT_BYTES:
+                    state["overflow"] = True
+                    _kill_group(proc)
+                    return
+                out_chunks.append(chunk)
+        except (OSError, ValueError):
+            return
+        finally:
+            stdout_done.set()
+
+    def read_stderr() -> None:
+        try:
+            while True:
+                chunk = proc.stderr.read1(4096)
+                if not chunk:
+                    return
+                room = STDERR_KEEP_BYTES - state["err"]
+                if room > 0:
+                    err_chunks.append(chunk[:room])
+                    state["err"] += min(room, len(chunk))
+        except (OSError, ValueError):
+            return
+
+    threads = [
+        threading.Thread(target=read_stdout, daemon=True),
+        threading.Thread(target=read_stderr, daemon=True),
+    ]
+    for thread in threads:
+        thread.start()
+
+    def stderr_text() -> str:
+        return b"".join(err_chunks).decode("utf-8", errors="replace")
+
+    if not stdout_done.wait(timeout):
+        _kill_group(proc)
+        raise RunnerFailure("timeout", stderr_text())
+    if state["overflow"]:
+        raise RunnerFailure("output-cap", stderr_text())
+    try:
+        returncode = proc.wait(timeout=KILL_GRACE_SECONDS)
+    except subprocess.TimeoutExpired:
+        _kill_group(proc)
+        raise RunnerFailure("timeout", stderr_text()) from None
+    for thread in threads:
+        thread.join(timeout=KILL_GRACE_SECONDS)
+    return (
+        returncode,
+        b"".join(out_chunks).decode("utf-8", errors="replace"),
+        stderr_text(),
+    )
+
+
+# -- results and the live source ---------------------------------------------------------------
+
+
+@dataclass(frozen=True)
+class SourceResult:
+    state: str  # "OK" | "FAILED" | "PARTIAL"
+    pages: tuple = ()  # decoded JSON of each page read, in order
+    code: str | None = None  # a code from CODES, or "exit:<n>"
+    diagnostic: str = ""  # sanitized stderr, at most 2 KiB
+    capped: bool = False  # paging stopped at the per-cycle call cap
+    calls: int = 0
+
+
+def _peek(page: Any) -> tuple[Any, Any, Any, Any]:
+    """(hasMore, nextCursor, total, number of workers or None); strict checks live in parse.py."""
+    result = page.get("result") if isinstance(page, dict) else None
+    paging = result.get("page") if isinstance(result, dict) else None
+    workers = result.get("workers") if isinstance(result, dict) else None
+    if not isinstance(paging, dict):
+        return None, None, None, len(workers) if isinstance(workers, list) else None
+    return (
+        paging.get("hasMore"),
+        paging.get("nextCursor"),
+        paging.get("total"),
+        len(workers) if isinstance(workers, list) else None,
+    )
+
+
+class LiveSource:
+    """Pages through ``worker-list`` for one cycle, within the call cap and the time budget."""
+
+    mode = "live"
+
+    def __init__(
+        self,
+        runner: Runner = production_runner,
+        discover: Discover = _find_orca,
+        per_call_timeout: float = PER_CALL_TIMEOUT,
+    ) -> None:
+        self._runner = runner
+        self._discover = discover
+        self.per_call_timeout = per_call_timeout
+        self._discovered = False
+        self.orca: str | None = None
+
+    def discover(self) -> bool:
+        """Run binary discovery once; True when a validated Orca CLI was found."""
+        if not self._discovered:
+            self._discovered = True
+            self.orca = self._discover()
+        return self.orca is not None
+
+    @property
+    def available(self) -> bool:
+        return self.discover()
+
+    @property
+    def namespace(self) -> str:
+        """The resolved absolute path of the validated Orca CLI (observer-derived)."""
+        return os.path.realpath(self.orca) if self.discover() and self.orca else ""
+
+    def _stop(
+        self, pages: list, code: str, diagnostic: str, calls: int
+    ) -> SourceResult:
+        state = "PARTIAL" if pages else "FAILED"
+        return SourceResult(
+            state,
+            tuple(pages),
+            code,
+            sanitize(diagnostic, "block")[:STDERR_KEEP_BYTES],
+            calls=calls,
+        )
+
+    def read_pages(
+        self, clock: Any, budget_deadline: float, run_id: str | None = None
+    ) -> SourceResult:
+        if not self.discover():
+            return SourceResult("FAILED", code="not-found")
+        pages: list = []
+        used: set[str] = set()
+        cursor: str | None = None
+        calls = 0
+        while True:
+            remaining = budget_deadline - clock.monotonic()
+            if remaining <= 0:
+                return self._stop(pages, "overrun", "", calls)
+            try:
+                argv = build_argv(self.orca, run_id, cursor)
+            except ArgvRejected as exc:
+                if cursor is not None and exc.code == "cursor-rejected":
+                    return self._stop(pages, "cursor-rejected", "", calls)
+                raise
+            budget_limited = remaining < self.per_call_timeout
+            calls += 1
+            try:
+                reply = self._runner(argv, min(self.per_call_timeout, remaining))
+            except (TimeoutError, subprocess.TimeoutExpired):
+                return self._stop(
+                    pages, "overrun" if budget_limited else "timeout", "", calls
+                )
+            except RunnerFailure as exc:
+                code = (
+                    "overrun" if exc.code == "timeout" and budget_limited else exc.code
+                )
+                return self._stop(pages, code, exc.stderr, calls)
+            except OSError as exc:
+                return self._stop(pages, "spawn-error", str(exc), calls)
+            returncode, stdout = reply[0], reply[1]
+            stderr = reply[2] if len(reply) > 2 else ""
+            if returncode != 0:
+                return self._stop(pages, f"exit:{returncode}", stderr, calls)
+            try:
+                page = json.loads(stdout)
+            except (ValueError, TypeError):
+                return self._stop(pages, "json", stderr, calls)
+            pages.append(page)
+            has_more, next_cursor, total, worker_count = _peek(page)
+            if (
+                worker_count == 0
+                and isinstance(total, int)
+                and not isinstance(total, bool)
+                and total > 0
+            ):
+                return self._stop(pages, "empty-page", "", calls)
+            if has_more is not True:
+                return SourceResult("OK", tuple(pages), calls=calls)
+            if calls >= MAX_CALLS_PER_CYCLE:
+                return SourceResult("PARTIAL", tuple(pages), capped=True, calls=calls)
+            if next_cursor is None or (
+                isinstance(next_cursor, str) and not next_cursor
+            ):
+                return self._stop(pages, "cursor-stalled", "", calls)
+            if not isinstance(next_cursor, str):
+                return self._stop(pages, "cursor-rejected", "", calls)
+            if next_cursor in used:
+                return self._stop(pages, "cursor-stalled", "", calls)
+            used.add(next_cursor)
+            cursor = next_cursor
diff --git a/tests/observe/test_adapter.py b/tests/observe/test_adapter.py
new file mode 100644
index 000000000..f5b018e9b
--- /dev/null
+++ b/tests/observe/test_adapter.py
@@ -0,0 +1,574 @@
+"""Adapter tests (AD-3, AD-4, AD-5; T1, T2, T4 adapter half, T36, T37 in acceptance-tests.md)."""
+
+from __future__ import annotations
+
+import json
+import os
+import re
+import sys
+import time
+from pathlib import Path
+from types import SimpleNamespace
+
+import pytest
+
+import superclaude.cli.observe.adapter as adapter
+from superclaude.cli.observe.adapter import (
+    CURSOR_MAX_BYTES,
+    FORBIDDEN_PREFIXES,
+    ArgvRejected,
+    LiveSource,
+    RunnerFailure,
+    assert_allowed,
+    build_argv,
+    production_runner,
+)
+from tests.observe.conftest import (
+    FakeDiscover,
+    FakeRunner,
+    argv_allowed,
+    make_envelope,
+    make_rows,
+)
+
+ORCA = "/opt/fake/orca"
+TEMPLATE = [ORCA, "orchestration", "worker-list", "--json", "--limit", "100"]
+
+
+def reply(n=1, has_more=False, cursor=None, total=None, rows=None):
+    envelope = make_envelope(
+        make_rows(n, 1) if rows is None else rows, total=total, has_more=has_more
+    )
+    if cursor is not None:
+        envelope["result"]["page"]["nextCursor"] = cursor
+    return 0, json.dumps(envelope)
+
+
+def source_with(responses, argv_log, **kw):
+    runner = FakeRunner(argv_log, responses)
+    return LiveSource(runner, FakeDiscover(argv_log, ORCA), **kw), runner
+
+
+def read(source, clock, budget=15.0, run_id=None):
+    return source.read_pages(clock, clock.monotonic() + budget, run_id)
+
+
+# -- T1: only the two templates, ever ----------------------------------------------------------
+
+
+def test_every_argv_across_all_adapter_paths_is_a_template(argv_log, fake_clock):
+    scenarios = [
+        [reply(3)],  # one page
+        [
+            reply(2, True, "c1", 5),
+            reply(2, True, "c2", 5),
+            reply(1, False, None, 5),
+        ],  # three pages
+        [(2, "")],  # exit failure
+        [TimeoutError("slow")],
+        [reply(1, True, None)],  # cursor missing
+    ]
+    for responses in scenarios:
+        source, _ = source_with(responses, argv_log)
+        read(source, fake_clock)
+        read(source, fake_clock, run_id="run-a")
+    assert argv_log
+    for argv in argv_log:
+        assert argv_allowed(argv)
+        assert argv == [ORCA, "skills", "list", "--json"] or argv[:6] == TEMPLATE
+    assert sum(1 for a in argv_log if a[1] == "skills") == len(
+        scenarios
+    )  # discovery once per source
+
+
+def test_real_find_orca_probes_with_the_discovery_argv_only(
+    monkeypatch, argv_log, fake_clock
+):
+    import superclaude.cli.install_user_setup as setup
+
+    probes: list[list[str]] = []
+
+    def fake_run(argv, **kwargs):
+        probes.append(list(argv))
+        return SimpleNamespace(
+            returncode=0, stdout=json.dumps({"topics": [{"name": "orca-cli"}]})
+        )
+
+    monkeypatch.setattr(setup.shutil, "which", lambda name: f"/opt/fake/{name}")
+    monkeypatch.setattr(setup.subprocess, "run", fake_run)
+    runner = FakeRunner(argv_log, [reply(1)])
+    source = LiveSource(runner)  # the default Discover is _find_orca
+    result = read(source, fake_clock)
+    assert result.state == "OK"
+    assert len(probes) <= 2 and all(
+        p[1:] == ["skills", "list", "--json"] for p in probes
+    )
+    assert runner.log[-1][1:6] == [
+        "orchestration",
+        "worker-list",
+        "--json",
+        "--limit",
+        "100",
+    ]
+    assert source.namespace == os.path.realpath(probes[0][0])
+
+
+def test_two_failing_candidates_mean_at_most_two_probes_and_not_available(
+    monkeypatch, argv_log, fake_clock
+):
+    import superclaude.cli.install_user_setup as setup
+
+    probes: list[list[str]] = []
+
+    def failing_run(argv, **kwargs):
+        probes.append(list(argv))
+        return SimpleNamespace(returncode=1, stdout="{}")
+
+    monkeypatch.setattr(setup.shutil, "which", lambda name: f"/opt/fake/{name}")
+    monkeypatch.setattr(setup.subprocess, "run", failing_run)
+    runner = FakeRunner(argv_log, [reply(1)])
+    source = LiveSource(runner)
+    assert source.available is False
+    assert read(source, fake_clock).code == "not-found"
+    assert len(probes) <= 2 and runner.calls == 0
+
+
+def test_discover_none_is_not_available_with_zero_worker_list_calls(
+    argv_log, fake_clock
+):
+    runner = FakeRunner(argv_log, [reply(1)])
+    discover = FakeDiscover(argv_log, None)
+    source = LiveSource(runner, discover)
+    assert source.available is False and source.namespace == ""
+    for _ in range(3):
+        result = read(source, fake_clock)
+        assert (result.state, result.code, result.pages) == ("FAILED", "not-found", ())
+    assert runner.calls == 0 and discover.calls == 1  # discovery runs once
+
+
+def test_namespace_is_the_resolved_absolute_path_of_the_orca_cli(argv_log):
+    source, _ = source_with([reply(1)], argv_log)
+    assert source.namespace == os.path.realpath(ORCA)
+
+
+# -- T2: forbidden words only inside the forbidden set ---------------------------------------------
+
+
+def test_forbidden_words_appear_only_inside_the_forbidden_set():
+    text = Path(adapter.__file__).read_text(encoding="utf-8")
+    for word in ("--ack", "--wait", "--retry-request"):
+        assert text.count(word) == 1, word
+    block = re.search(r"^FORBIDDEN_PREFIXES = frozenset\(.*?\)\n", text, re.M | re.S)
+    assert block, "the forbidden set must be one frozenset literal"
+    for word in ("--ack", "--wait", "--retry-request"):
+        assert word in block.group(0)
+    assert text.count('"check"') == 1 and '"check"' in block.group(0)
+    assert (
+        "check" not in adapter.WORKER_LIST_TEMPLATE
+        and "check" not in adapter.DISCOVERY_TEMPLATE
+    )
+    assert FORBIDDEN_PREFIXES >= {
+        "check",
+        "--ack",
+        "--wait",
+        "--retry-request",
+        "dispatch",
+        "inbox",
+    }
+
+
+# -- T36 and T37: argv validation before any call -----------------------------------------------------
+
+
+@pytest.mark.parametrize(
+    "bad", ["-x", "--run", "bad id", "", "a" * 129, "a/b", "x;y", "run\n1", 5]
+)
+def test_malformed_run_ids_are_rejected(bad):
+    with pytest.raises(ArgvRejected) as info:
+        build_argv(ORCA, run_id=bad)
+    assert info.value.code == "run-id"
+
+
+@pytest.mark.parametrize(
+    "bad",
+    [
+        "-x",
+        "--ack",
+        "a\x00b",
+        "x" * (CURSOR_MAX_BYTES + 1),
+        "é" * CURSOR_MAX_BYTES,
+        "",
+        7,
+    ],
+)
+def test_bad_cursors_are_rejected(bad):
+    with pytest.raises(ArgvRejected) as info:
+        build_argv(ORCA, cursor=bad)
+    assert info.value.code == "cursor-rejected"
+
+
+def test_good_values_are_separate_argv_items_and_the_cursor_is_unchanged():
+    cursor = "abc==/+def.ghi_JKL-0"
+    assert build_argv(ORCA) == TEMPLATE
+    assert build_argv(ORCA, "run_A-1.b:2") == [*TEMPLATE, "--run", "run_A-1.b:2"]
+    assert build_argv(ORCA, "run-a", cursor) == [
+        *TEMPLATE,
+        "--run",
+        "run-a",
+        "--cursor",
+        cursor,
+    ]
+    assert build_argv(ORCA, cursor="x" * CURSOR_MAX_BYTES)[-1] == "x" * CURSOR_MAX_BYTES
+    assert not any(
+        "=" in a and a.startswith("--") for a in build_argv(ORCA, "run-a", cursor)
+    )
+
+
+@pytest.mark.parametrize(
+    "argv",
+    [
+        [ORCA, "check"],
+        [ORCA, "check", "--peek"],
+        [ORCA, "check", "--all"],
+        [ORCA, "inbox"],
+        [ORCA, "dispatch"],
+        [ORCA, "orchestration", "dispatch", "--json"],
+        [*TEMPLATE, "--ack"],
+        [*TEMPLATE, "--wait"],
+        [*TEMPLATE, "--wait=5"],
+        [*TEMPLATE, "--retry-request"],
+        [*TEMPLATE, "--include-remote"],
+        [ORCA, "orchestration", "worker-list", "--json"],
+        [ORCA, "orchestration", "worker-stop", "--json", "--limit", "100"],
+        [ORCA, "skills", "install"],
+        [ORCA, "skills", "list"],
+        [*TEMPLATE, "--cursor", "-x"],
+        [*TEMPLATE, "--run", "--evil"],
+        [*TEMPLATE, "--cursor", "c", "--run", "run-a"],
+        [*TEMPLATE, "--run", "a", "--run", "b"],
+        [ORCA],
+        [],
+        ["-evil", "skills", "list", "--json"],
+    ],
+)
+def test_unlisted_argv_is_rejected_before_any_call(argv):
+    with pytest.raises(ArgvRejected):
+        assert_allowed(argv)
+
+
+@pytest.mark.parametrize("prefix", sorted(FORBIDDEN_PREFIXES))
+def test_every_forbidden_prefix_is_rejected_by_name_in_any_verb_or_flag_position(
+    prefix,
+):
+    for argv in (
+        [ORCA, prefix],
+        [ORCA, f"{prefix}-more"],
+        [*TEMPLATE, prefix],
+        [ORCA, "orchestration", prefix],
+    ):
+        with pytest.raises(ArgvRejected) as info:
+            assert_allowed(argv)
+        assert info.value.code == "forbidden"
+
+
+def test_forbidden_words_inside_option_values_are_values_not_verbs():
+    assert_allowed(
+        [*TEMPLATE, "--run", "dispatch-7"]
+    )  # a run id that happens to start like a verb
+
+
+def test_templates_pass_the_check():
+    assert_allowed(TEMPLATE)
+    assert_allowed([ORCA, "skills", "list", "--json"])
+    assert_allowed([*TEMPLATE, "--run", "run-a", "--cursor", "c1"])
+
+
+def test_bad_run_id_fails_before_any_runner_call(argv_log, fake_clock):
+    source, runner = source_with([reply(1)], argv_log)
+    with pytest.raises(ArgvRejected):
+        read(source, fake_clock, run_id="-x")
+    assert runner.calls == 0 and not any(a[1] == "orchestration" for a in argv_log)
+
+
+def test_an_unlisted_argv_fails_loudly_in_the_fake_runner_and_with_real_subprocess_blocked(
+    argv_log, fake_clock
+):
+    with pytest.raises(AssertionError, match="allow-list"):
+        FakeRunner(argv_log)([ORCA, "check"], 1.0)
+    live = LiveSource(production_runner, FakeDiscover(argv_log, ORCA))
+    with pytest.raises(AssertionError, match="subprocess is blocked"):
+        read(live, fake_clock)  # the real runner would spawn; the guard raises instead
+
+
+def test_a_rejected_cursor_stops_paging_with_partial(argv_log, fake_clock):
+    source, runner = source_with([reply(2, True, "-evil", 9)], argv_log)
+    result = read(source, fake_clock)
+    assert (result.state, result.code, len(result.pages), result.calls) == (
+        "PARTIAL",
+        "cursor-rejected",
+        1,
+        1,
+    )
+    assert runner.calls == 1
+
+
+# -- T4 (adapter half) and paging integrity ------------------------------------------------------------
+
+
+def test_a_source_that_always_has_more_stops_at_five_calls_with_partial(
+    argv_log, fake_clock
+):
+    counter = {"n": 0}
+
+    def always_more(argv, timeout):
+        counter["n"] += 1
+        return reply(100, True, f"cursor-{counter['n']}", 9999)
+
+    source, runner = source_with([always_more], argv_log)
+    result = read(source, fake_clock)
+    assert (result.state, result.capped, result.calls, len(result.pages)) == (
+        "PARTIAL",
+        True,
+        5,
+        5,
+    )
+    assert runner.calls == 5 and result.code is None
+    cursors = [a[a.index("--cursor") + 1] for a in argv_log if "--cursor" in a]
+    assert cursors == ["cursor-1", "cursor-2", "cursor-3", "cursor-4"]
+
+
+def test_a_finished_traversal_is_ok_and_follows_next_cursor(argv_log, fake_clock):
+    source, runner = source_with(
+        [reply(2, True, "c1", 3), reply(1, False, None, 3)], argv_log
+    )
+    result = read(source, fake_clock, run_id="run-a")
+    assert (result.state, result.code, result.calls, len(result.pages)) == (
+        "OK",
+        None,
+        2,
+        2,
+    )
+    worker_calls = [a for a in argv_log if a[1] == "orchestration"]
+    assert worker_calls[0][6:] == ["--run", "run-a"]
+    assert worker_calls[1][6:] == ["--run", "run-a", "--cursor", "c1"]
+
+
+@pytest.mark.parametrize(
+    ("second_cursor", "code"),
+    [
+        (None, "cursor-stalled"),
+        ("", "cursor-stalled"),
+        ("c1", "cursor-stalled"),
+        (5, "cursor-rejected"),
+        ({"a": 1}, "cursor-rejected"),
+    ],
+)
+def test_cursor_that_is_missing_empty_repeated_or_not_text_stops_paging(
+    argv_log, fake_clock, second_cursor, code
+):
+    page2 = reply(1, True, None, 9)
+    envelope = json.loads(page2[1])
+    envelope["result"]["page"]["nextCursor"] = second_cursor
+    source, _ = source_with(
+        [reply(1, True, "c1", 9), (0, json.dumps(envelope))], argv_log
+    )
+    result = read(source, fake_clock)
+    assert (result.state, result.code, len(result.pages)) == ("PARTIAL", code, 2)
+
+
+def test_missing_cursor_on_the_first_page_is_partial_with_one_page(
+    argv_log, fake_clock
+):
+    source, _ = source_with([reply(1, True, None, 9)], argv_log)
+    result = read(source, fake_clock)
+    assert (result.state, result.code, len(result.pages)) == (
+        "PARTIAL",
+        "cursor-stalled",
+        1,
+    )
+
+
+def test_an_empty_page_while_total_is_above_zero_is_partial(argv_log, fake_clock):
+    source, _ = source_with([reply(0, False, None, 7, rows=[])], argv_log)
+    assert read(source, fake_clock).code == "empty-page"
+    source, _ = source_with([reply(0, False, None, 0, rows=[])], argv_log)
+    assert read(source, fake_clock).state == "OK"  # total 0: a genuinely empty fleet
+    source, _ = source_with(
+        [reply(2, True, "c1", 5), reply(0, True, "c2", 5, rows=[])], argv_log
+    )
+    result = read(source, fake_clock)
+    assert (result.state, result.code, len(result.pages)) == (
+        "PARTIAL",
+        "empty-page",
+        2,
+    )
+
+
+def test_the_adapter_only_peeks_and_leaves_shape_checks_to_the_parser(
+    argv_log, fake_clock
+):
+    source, _ = source_with([(0, json.dumps({"result": {"workers": "x"}}))], argv_log)
+    result = read(source, fake_clock)
+    assert (
+        result.state == "OK" and len(result.pages) == 1
+    )  # parse.py turns this into FAILED (shape)
+
+
+# -- errors, timeouts and the time budget ----------------------------------------------------------------
+
+
+def test_failures_on_the_first_page_are_failed_with_a_code(argv_log, fake_clock):
+    cases = [
+        ([(2, "", "boom")], "exit:2"),
+        ([(127, "")], "exit:127"),
+        ([TimeoutError("slow")], "timeout"),
+        ([RunnerFailure("output-cap", "big")], "output-cap"),
+        ([RunnerFailure("spawn-error", "no such file")], "spawn-error"),
+        ([FileNotFoundError("gone")], "spawn-error"),
+        ([(0, "not json")], "json"),
+        ([(0, "")], "json"),
+    ]
+    for responses, code in cases:
+        source, _ = source_with(responses, argv_log)
+        result = read(source, fake_clock)
+        assert (result.state, result.code, result.pages) == ("FAILED", code, ()), code
+
+
+def test_a_failure_on_a_later_page_keeps_the_pages_already_read_as_partial(
+    argv_log, fake_clock
+):
+    source, _ = source_with(
+        [reply(2, True, "c1", 9), (3, "", "late failure")], argv_log
+    )
+    result = read(source, fake_clock)
+    assert (result.state, result.code, len(result.pages)) == ("PARTIAL", "exit:3", 1)
+    assert result.diagnostic == "late failure"
+
+
+def test_stderr_is_sanitized_and_kept_to_two_kib(argv_log, fake_clock):
+    noisy = "\x1b[31mred\x1b[0m line\nsecond " + "x" * 5000
+    source, _ = source_with([(1, "", noisy)], argv_log)
+    result = read(source, fake_clock)
+    assert "\x1b" not in result.diagnostic and result.diagnostic.startswith(
+        "red line\nsecond"
+    )
+    assert len(result.diagnostic) <= 2048
+
+
+def test_per_call_timeout_is_passed_and_capped_by_the_time_left(argv_log, fake_clock):
+    source, runner = source_with([reply(1)], argv_log)
+    read(source, fake_clock, budget=15)
+    assert runner.timeouts == [10.0]
+    source, runner = source_with([TimeoutError("slow")], argv_log)
+    result = read(source, fake_clock, budget=3)
+    assert (
+        runner.timeouts == [3.0] and result.code == "overrun"
+    )  # the budget, not the call limit, cut it
+    source, runner = source_with([TimeoutError("slow")], argv_log, per_call_timeout=4.0)
+    assert read(
+        source, fake_clock, budget=15
+    ).code == "timeout" and runner.timeouts == [4.0]
+
+
+def test_the_budget_running_out_between_pages_is_overrun_partial(argv_log, fake_clock):
+    def slow_first_page(argv, timeout):
+        fake_clock.advance(20)
+        return reply(2, True, "c1", 9)
+
+    source, runner = source_with([slow_first_page], argv_log)
+    result = read(source, fake_clock)
+    assert (result.state, result.code, len(result.pages), runner.calls) == (
+        "PARTIAL",
+        "overrun",
+        1,
+        1,
+    )
+    source, runner = source_with([reply(1)], argv_log)
+    result = source.read_pages(fake_clock, fake_clock.monotonic() - 1)  # no time at all
+    assert (result.state, result.code, runner.calls) == ("FAILED", "overrun", 0)
+
+
+def test_a_runner_timeout_failure_cut_by_the_budget_is_overrun(argv_log, fake_clock):
+    source, _ = source_with([RunnerFailure("timeout", "")], argv_log)
+    assert read(source, fake_clock, budget=2).code == "overrun"
+    source, _ = source_with([RunnerFailure("timeout", "")], argv_log)
+    assert read(source, fake_clock, budget=15).code == "timeout"
+
+
+# -- the production runner on real processes ---------------------------------------------------------------
+
+PY = [sys.executable, "-I", "-c"]
+
+
+@pytest.mark.observe_real_process
+def test_production_runner_returns_stdout_stderr_and_returncode():
+    rc, out, err = production_runner(
+        [*PY, "import sys; print('{\"ok\": 1}'); sys.stderr.write('warn')"], 10
+    )
+    assert (rc, out.strip(), err) == (0, '{"ok": 1}', "warn")
+    rc, out, err = production_runner([*PY, "import sys; sys.exit(3)"], 10)
+    assert rc == 3 and out == ""
+
+
+@pytest.mark.observe_real_process
+def test_production_runner_kills_and_reaps_a_child_that_sleeps_past_the_timeout(
+    tmp_path,
+):
+    pidfile = tmp_path / "pid"
+    code = "import os, sys, time; open(sys.argv[1], 'w').write(str(os.getpid())); time.sleep(60)"
+    started = time.monotonic()
+    with pytest.raises(RunnerFailure) as info:
+        production_runner([*PY, code, str(pidfile)], 1.5)
+    assert info.value.code == "timeout" and time.monotonic() - started < 10
+    pid = int(pidfile.read_text())
+    with pytest.raises(ProcessLookupError):
+        os.kill(pid, 0)  # gone, and reaped: not even a zombie is left
+
+
+@pytest.mark.observe_real_process
+def test_production_runner_kills_a_child_that_writes_more_than_8_mib(tmp_path):
+    pidfile = tmp_path / "pid"
+    code = (
+        "import os, sys, time; open(sys.argv[1], 'w').write(str(os.getpid()));"
+        "sys.stdout.buffer.write(b'x' * (9 * 1024 * 1024)); sys.stdout.flush(); time.sleep(60)"
+    )
+    started = time.monotonic()
+    with pytest.raises(RunnerFailure) as info:
+        production_runner([*PY, code, str(pidfile)], 20)
+    assert info.value.code == "output-cap" and time.monotonic() - started < 15
+    with pytest.raises(ProcessLookupError):
+        os.kill(int(pidfile.read_text()), 0)
+
+
+@pytest.mark.observe_real_process
+def test_production_runner_keeps_at_most_2_kib_of_stderr_without_blocking_the_child():
+    code = "import sys; sys.stderr.write('e' * 300000); sys.stdout.write('{}')"
+    rc, out, err = production_runner([*PY, code], 20)
+    assert (rc, out) == (0, "{}")
+    assert 0 < len(err.encode()) <= 2048
+
+
+@pytest.mark.observe_real_process
+def test_production_runner_returns_spawn_error_when_the_binary_does_not_exist():
+    with pytest.raises(RunnerFailure) as info:
+        production_runner(["/nonexistent/dir/binary-xyz", "--json"], 5)
+    assert info.value.code == "spawn-error"
+
+
+@pytest.mark.observe_real_process
+def test_live_source_with_the_production_runner_maps_a_missing_binary_to_a_failed_cycle(
+    argv_log, fake_clock
+):
+    source = LiveSource(production_runner, lambda: "/nonexistent/dir/orca")
+    result = read(source, fake_clock)
+    assert (result.state, result.code) == ("FAILED", "spawn-error")
+
+
+# -- module hygiene (AD-1) ---------------------------------------------------------------------------------
+
+
+def test_adapter_imports_sanitize_but_not_parse_or_collector_and_owns_subprocess():
+    text = Path(adapter.__file__).read_text(encoding="utf-8")
+    assert re.search(r"^from superclaude\.cli\.observe\.sanitize import", text, re.M)
+    assert not re.search(r"observe\.(parse|collector|view|render|export)\b", text)
+    assert re.search(r"^import subprocess$", text, re.M)

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
