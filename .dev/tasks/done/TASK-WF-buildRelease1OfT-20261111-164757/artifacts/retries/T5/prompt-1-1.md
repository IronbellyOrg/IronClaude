8bf5fe6cc2ada7c27ec5e6b7c04c6ee32dacf86a
Review one task for spec compliance.

Task brief: 
## Task 5: Add the fixture variants, fixture loader and test support

Depends on: Task 3, Task 4

Create `src/superclaude/cli/observe/fixtures/` (one JSON file per variant), the fixture loader in `src/superclaude/cli/observe/parse.py` (`load_fixture(variant) -> Fixture`, read with `importlib.resources`), `tests/observe/conftest.py` and `tests/observe/test_fixtures.py`. Follow `ARCHITECTURE-SPINE.md` AD-16 and the variant list and meanings in `acceptance-tests.md` (harness and T13, T20, T21, T22, T24, T29, T33). Each variant file is JSON with a list of cycles; each cycle is either a `worker-list` envelope with the key names from `adapter-contract.md` or `{"fail": "<code>"}`. Variants: `base` (80 rows across 8 distinct run IDs, mixed states, two cycles that differ in one row's `nextAction.kind`), `uneven` (one run owns most rows), `shared-unmapped` (two rows share one `resource.worktreeId`, one row has none), `historical` (rows with `terminalState` released and retained plus rows with an absent or other value), `long-identifiers` (60 or more characters, with CJK and emoji), `source-loss` (good cycles then failing cycles), `missing-fields` (rows missing inner fields, one row with no `dispatchId`, one JSON null, no `page.total`, no `scope`), `duplicate-out-of-order` (duplicates, a row with no timestamps, a timestamp that goes backward across cycles), `empty` (`workers=[]`, total 0) and `injection` (CSI, OSC 8, unterminated OSC, `\u009b`, BEL, U+202E, a title sequence and the text `[bold]x[/bold]`, written as JSON escapes). All identifiers are synthetic (`w-001`, `run-a`), and the loader strips an optional fixture-only `fixtureOnly` object (for example `{"frozen": true}` read only for T34) before the live parser sees a row, then sets `fixture_frozen=True` on the parsed `Row` with `dataclasses.replace`, so the flag travels with the row through `merge`, `CycleResult` and `View` (Task 8 renders `FROZEN` from it; the snapshot never carries it). `conftest.py` provides a fake clock (`monotonic()`, `wall()`, local time zone), a fake `Runner` and fake `Discover` that append every argv to one shared log and raise on any argv outside the allow-list, a function `make_rows(n_rows, n_runs)` for the T16 matrix, a console factory using `make_console(policy, file=StringIO(), record=True)`, and an autouse fixture that makes `subprocess.Popen` and `subprocess.run` raise in this package unless a test carries the marker `observe_real_process` (register that marker in `pyproject.toml`).

Acceptance criteria:
- [T5.AC1] `uv run pytest tests/observe/test_fixtures.py -v` passes; it loads every variant through `importlib.resources` and parses each cycle with `parse_page` without exception.
- [T5.AC2] A test shows no committed fixture contains an absolute path, a `term_` handle, a token-like string or a raw ESC byte (the `injection` variant stores escapes as JSON escape sequences only).
- [T5.AC3] A test shows the `base` variant has 80 rows and 8 distinct `runId` values, and `empty` has no rows.
- [T5.AC4] A test shows a fixture row marked frozen comes out of the loader with `fixture_frozen=True`, and that the same JSON fed straight to `parse_page` leaves it False.
- [T5.AC5] `uv run pytest tests/observe -v` shows a test that calls `subprocess.run` fails with the guard's message, and that `pyproject.toml` still passes `--strict-markers` with the new `observe_real_process` marker registered.
- [T5.AC6] Fixture files ship in the package: a test asserts `importlib.resources.files("superclaude.cli.observe.fixtures")` lists all ten variants.

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

Start sha: 8bf5fe6cc2ada7c27ec5e6b7c04c6ee32dacf86a
Diff against the start snapshot: 
diff --git a/pyproject.toml b/pyproject.toml
index 6b21dc8dd..1a09a04c7 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -145,6 +145,7 @@ markers = [
     "recovery: Crash-recovery / resume reconstruction tests (FM-1..12)",
     "p0: P0 priority acceptance tests",
     "regression: Mandatory regression-gate tests (e.g. TM-0 per-phase turn-budget starvation guard)",
+    "observe_real_process: observer test that may start a real child process (lifts the subprocess guard)",
 ]
 
 [tool.coverage.run]
diff --git a/src/superclaude/cli/observe/fixtures/__init__.py b/src/superclaude/cli/observe/fixtures/__init__.py
new file mode 100644
index 000000000..71f561ada
--- /dev/null
+++ b/src/superclaude/cli/observe/fixtures/__init__.py
@@ -0,0 +1 @@
+"""Synthetic fixture variants (JSON) for the observer; read through ``parse.load_fixture``."""
diff --git a/src/superclaude/cli/observe/parse.py b/src/superclaude/cli/observe/parse.py
index 9381a458d..f50dca53a 100644
--- a/src/superclaude/cli/observe/parse.py
+++ b/src/superclaude/cli/observe/parse.py
@@ -7,11 +7,14 @@ keys are read; any other key is counted and dropped (its name and value are neve
 
 from __future__ import annotations
 
+import copy
 import json
 import math
+import re
 from collections.abc import Sequence
 from dataclasses import dataclass, replace
 from datetime import datetime, timezone
+from importlib import resources
 from typing import Any
 
 from superclaude.cli.observe.sanitize import sanitize
@@ -533,3 +536,99 @@ def merge(
         warnings=tuple(warnings[:50]),
     )
     return snapshot, coverage
+
+
+# -- fixture loader (never used by the live parser path) ------------------------------
+
+FIXTURE_PACKAGE = "superclaude.cli.observe.fixtures"
+VARIANTS = (
+    "base",
+    "uneven",
+    "shared-unmapped",
+    "historical",
+    "long-identifiers",
+    "source-loss",
+    "missing-fields",
+    "duplicate-out-of-order",
+    "empty",
+    "injection",
+)
+_VARIANT_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
+
+
+@dataclass(frozen=True)
+class FixtureCycle:
+    """One replayed cycle: a worker-list envelope, or a failure code."""
+
+    fail: str | None = None
+    envelope: dict | None = None
+    frozen: frozenset = (
+        frozenset()
+    )  # positions in result.workers carrying fixtureOnly.frozen
+
+
+@dataclass(frozen=True)
+class Fixture:
+    variant: str
+    cycles: tuple[FixtureCycle, ...]
+
+    def cycle(self, index: int) -> FixtureCycle:
+        """Cycle ``index`` (0-based); past the end the last cycle repeats."""
+        return self.cycles[min(index, len(self.cycles) - 1)]
+
+    def parse(
+        self, index: int, namespace: str, cycle: int, source_rank_base: int = 0
+    ) -> ParsedPage:
+        """Parse a non-failing cycle with ``parse_page``, then mark frozen rows."""
+        entry = self.cycle(index)
+        if entry.envelope is None:
+            raise ValueError(
+                f"fixture cycle {index} is a failure ({entry.fail}), it has no page"
+            )
+        parsed = parse_page(entry.envelope, namespace, cycle, source_rank_base)
+        if not entry.frozen:
+            return parsed
+        rows = tuple(
+            replace(row, fixture_frozen=True)
+            if row.source_rank - source_rank_base in entry.frozen
+            else row
+            for row in parsed.rows
+        )
+        return replace(parsed, rows=rows)
+
+
+def load_fixture(variant: str) -> Fixture:
+    """Load a fixture variant from the package data (``importlib.resources``)."""
+    if not isinstance(variant, str) or not _VARIANT_NAME.match(variant):
+        raise ValueError(f"invalid fixture variant name: {variant!r}")
+    try:
+        text = (
+            resources.files(FIXTURE_PACKAGE)
+            .joinpath(f"{variant}.json")
+            .read_text(encoding="utf-8")
+        )
+    except (FileNotFoundError, OSError) as exc:
+        raise ValueError(f"unknown fixture variant: {variant!r}") from exc
+    data = json.loads(text)
+    cycles: list[FixtureCycle] = []
+    for raw in data["cycles"]:
+        if "result" not in raw and "fail" in raw:
+            cycles.append(FixtureCycle(fail=sanitize(str(raw["fail"]), "line")))
+            continue
+        envelope = copy.deepcopy(raw)
+        frozen: set[int] = set()
+        workers = (
+            envelope.get("result", {}).get("workers")
+            if isinstance(envelope.get("result"), dict)
+            else None
+        )
+        if isinstance(workers, list):
+            for position, worker in enumerate(workers):
+                if isinstance(worker, dict) and "fixtureOnly" in worker:
+                    marker = worker.pop(
+                        "fixtureOnly"
+                    )  # fixture-only: the live parser never sees it
+                    if isinstance(marker, dict) and marker.get("frozen") is True:
+                        frozen.add(position)
+        cycles.append(FixtureCycle(envelope=envelope, frozen=frozenset(frozen)))
+    return Fixture(variant=variant, cycles=tuple(cycles))
diff --git a/tests/observe/conftest.py b/tests/observe/conftest.py
new file mode 100644
index 000000000..f6218a39a
--- /dev/null
+++ b/tests/observe/conftest.py
@@ -0,0 +1,211 @@
+"""Shared support for tests/observe: fake clock, fake runner and discovery, console factory.
+
+Every test in this package runs with ``subprocess.Popen`` and ``subprocess.run`` replaced by a
+function that raises, unless the test carries the marker ``observe_real_process`` (AD-16, T36).
+"""
+
+from __future__ import annotations
+
+import io
+import subprocess
+from datetime import datetime, timedelta, timezone
+
+import pytest
+
+from superclaude.cli.observe.terminal import make_console, resolve_policy
+
+BASE_TIME = datetime(2026, 11, 8, 12, 0, 0, tzinfo=timezone.utc)
+WORKER_LIST_BASE = ["orchestration", "worker-list", "--json", "--limit", "100"]
+DISCOVERY_TAIL = ["skills", "list", "--json"]
+
+
+# -- subprocess guard -------------------------------------------------------------------
+
+
+@pytest.fixture(autouse=True)
+def _subprocess_guard(request, monkeypatch):
+    if request.node.get_closest_marker("observe_real_process"):
+        return
+
+    def refuse(*args, **kwargs):
+        raise AssertionError(
+            "subprocess is blocked in tests/observe; mark the test observe_real_process to lift the guard"
+        )
+
+    monkeypatch.setattr(subprocess, "Popen", refuse)
+    monkeypatch.setattr(subprocess, "run", refuse)
+
+
+# -- fake clock ---------------------------------------------------------------------------
+
+
+class FakeClock:
+    """Monotonic time, wall time and the local time zone, all under the test's control."""
+
+    def __init__(
+        self,
+        monotonic: float = 1000.0,
+        wall: float | None = None,
+        tz: timezone = timezone.utc,
+    ):
+        self._mono = monotonic
+        self._wall = BASE_TIME.timestamp() if wall is None else wall
+        self.tz = tz
+
+    def monotonic(self) -> float:
+        return self._mono
+
+    def wall(self) -> float:
+        return self._wall
+
+    def local_tz(self) -> timezone:
+        return self.tz
+
+    def advance(self, seconds: float) -> None:
+        self._mono += seconds
+        self._wall += seconds
+
+    def jump_wall(self, seconds: float) -> None:
+        """A wall-clock jump that leaves monotonic time alone."""
+        self._wall += seconds
+
+
+@pytest.fixture
+def fake_clock() -> FakeClock:
+    return FakeClock()
+
+
+# -- fake runner and discovery (one shared argv log) ---------------------------------------
+
+
+def argv_allowed(argv) -> bool:
+    """The only argv the observer may ever run: worker-list (with optional pairs) or discovery."""
+    argv = list(argv)
+    if len(argv) < 2 or not all(isinstance(a, str) for a in argv):
+        return False
+    tail = argv[1:]
+    if tail == DISCOVERY_TAIL:
+        return True
+    if tail[:5] != WORKER_LIST_BASE:
+        return False
+    rest = tail[5:]
+    if rest[:1] == ["--run"] and len(rest) >= 2 and not rest[1].startswith("-"):
+        rest = rest[2:]
+    if rest[:1] == ["--cursor"] and len(rest) >= 2 and not rest[1].startswith("-"):
+        rest = rest[2:]
+    return rest == []
+
+
+class FakeRunner:
+    """``Runner`` stand-in: logs every argv, raises on one outside the allow-list.
+
+    ``responses`` holds ``(returncode, stdout)`` pairs, exceptions, or callables
+    ``f(argv, timeout) -> (returncode, stdout)``; the last one repeats when they run out.
+    """
+
+    def __init__(self, log: list, responses: list | None = None):
+        self.log = log
+        self.responses = responses if responses is not None else [(0, "{}")]
+        self.timeouts: list[float] = []
+        self.calls = 0
+
+    def __call__(self, argv, timeout):
+        self.log.append(list(argv))
+        self.timeouts.append(timeout)
+        if not argv_allowed(argv):
+            raise AssertionError(f"argv outside the allow-list: {list(argv)!r}")
+        response = self.responses[min(self.calls, len(self.responses) - 1)]
+        self.calls += 1
+        if isinstance(response, BaseException):
+            raise response
+        if callable(response):
+            return response(argv, timeout)
+        return response
+
+
+class FakeDiscover:
+    """``Discover`` stand-in: logs the discovery argv the real helper would run."""
+
+    def __init__(self, log: list, path: str | None = "/opt/fake/orca"):
+        self.log = log
+        self.path = path
+        self.calls = 0
+
+    def __call__(self):
+        self.calls += 1
+        self.log.append([self.path or "orca", *DISCOVERY_TAIL])
+        return self.path
+
+
+@pytest.fixture
+def argv_log() -> list:
+    return []
+
+
+@pytest.fixture
+def fake_runner(argv_log) -> FakeRunner:
+    return FakeRunner(argv_log)
+
+
+@pytest.fixture
+def fake_discover(argv_log) -> FakeDiscover:
+    return FakeDiscover(argv_log)
+
+
+# -- data and console helpers ----------------------------------------------------------------
+
+
+def make_rows(n_rows: int, n_runs: int) -> list[dict]:
+    """``n_rows`` valid worker rows spread over ``n_runs`` distinct runs (T16 matrix)."""
+    rows = []
+    for i in range(1, n_rows + 1):
+        observed = (BASE_TIME - timedelta(seconds=3 * i)).strftime("%Y-%m-%dT%H:%M:%SZ")
+        rows.append(
+            {
+                "dispatchId": f"w-{i:03d}",
+                "taskId": f"t-{i:03d}",
+                "runId": f"run-{(i - 1) % n_runs}",
+                "workerState": "running" if i % 2 else "idle",
+                "dispatchStatus": "active",
+                "terminalState": "active",
+                "projection": {
+                    "outcome": "none",
+                    "nextAction": {"kind": "wait" if i % 3 else "none"},
+                    "liveness": {
+                        "verdict": "alive",
+                        "source": "terminal",
+                        "observedAt": observed,
+                    },
+                    "evidence": {"lastObservedAt": observed},
+                },
+            }
+        )
+    return rows
+
+
+def make_envelope(
+    rows: list[dict], total: int | None = None, has_more: bool = False
+) -> dict:
+    page = {"hasMore": has_more, "limit": 100}
+    if total is not None:
+        page["total"] = total
+    return {"result": {"workers": rows, "page": page, "scope": {"source": "all"}}}
+
+
+@pytest.fixture(name="make_rows")
+def make_rows_fixture():
+    return make_rows
+
+
+@pytest.fixture
+def console_factory():
+    """``console_factory(width=160, height=40, ascii=False, no_color=False) -> (console, policy)``."""
+
+    def factory(
+        width: int = 160, height: int = 40, ascii: bool = False, no_color: bool = False
+    ):
+        env = {"NO_COLOR": "1"} if no_color else {}
+        policy = resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)
+        return make_console(policy, file=io.StringIO(), record=True), policy
+
+    return factory
diff --git a/tests/observe/test_fixtures.py b/tests/observe/test_fixtures.py
new file mode 100644
index 000000000..dc2878b09
--- /dev/null
+++ b/tests/observe/test_fixtures.py
@@ -0,0 +1,296 @@
+"""Fixture variants, the fixture loader and the shared test support (AD-16; harness of acceptance-tests.md)."""
+
+from __future__ import annotations
+
+import re
+import subprocess
+import sys
+from importlib import resources
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.observe.parse import (
+    FIXTURE_PACKAGE,
+    VARIANTS,
+    load_fixture,
+    parse_page,
+)
+from tests.observe.conftest import FakeClock, argv_allowed
+
+ROOT = Path(__file__).resolve().parents[2]
+
+
+def fixture_files():
+    return [
+        p
+        for p in resources.files(FIXTURE_PACKAGE).iterdir()
+        if p.name.endswith(".json")
+    ]
+
+
+# -- loading ---------------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("variant", VARIANTS)
+def test_every_variant_loads_and_every_cycle_parses(variant):
+    fixture = load_fixture(variant)
+    assert fixture.variant == variant and fixture.cycles
+    for index, cycle in enumerate(fixture.cycles):
+        if cycle.fail is not None:
+            assert cycle.envelope is None and cycle.fail
+            continue
+        page = fixture.parse(index, f"fixture:{variant}", index + 1)
+        assert page.raw_count == len(cycle.envelope["result"]["workers"])
+
+
+def test_importlib_resources_lists_all_ten_variants():
+    names = {
+        p.name for p in resources.files("superclaude.cli.observe.fixtures").iterdir()
+    }
+    assert {f"{v}.json" for v in VARIANTS} <= names
+    assert len(VARIANTS) == 10
+
+
+@pytest.mark.parametrize("bad", ["../base", "nope", "Base", "", "base.json", "a/b"])
+def test_unknown_or_unsafe_variant_names_are_refused(bad):
+    with pytest.raises(ValueError):
+        load_fixture(bad)
+
+
+def test_replay_repeats_the_last_cycle():
+    fixture = load_fixture("source-loss")
+    assert [c.fail for c in fixture.cycles] == [
+        None,
+        None,
+        "timeout",
+        "timeout",
+        "exit:2",
+    ]
+    assert fixture.cycle(99).fail == "exit:2"
+
+
+# -- variant contents ------------------------------------------------------------------------
+
+
+def workers(variant, index=0):
+    return load_fixture(variant).cycle(index).envelope["result"]["workers"]
+
+
+def test_base_has_80_rows_and_8_runs_and_cycle_two_changes_one_next_action():
+    rows = workers("base")
+    assert len(rows) == 80 and len({r["runId"] for r in rows}) == 8
+    changed = [
+        (
+            a["dispatchId"],
+            a["projection"]["nextAction"]["kind"],
+            b["projection"]["nextAction"]["kind"],
+        )
+        for a, b in zip(workers("base", 0), workers("base", 1), strict=True)
+        if a != b
+    ]
+    assert changed == [("w-005", "none", "approve")]
+
+
+def test_empty_has_no_rows_and_total_zero():
+    assert workers("empty") == []
+    assert load_fixture("empty").cycle(0).envelope["result"]["page"]["total"] == 0
+
+
+def test_uneven_shared_historical_and_missing_variants_have_their_shapes():
+    rows = workers("uneven")
+    assert sum(1 for r in rows if r["runId"] == "run-a") == 60
+    shared = workers("shared-unmapped")
+    assert shared[0]["resource"]["worktreeId"] == shared[1]["resource"]["worktreeId"]
+    assert "worktreeId" not in shared[2]["resource"]
+    states = [r.get("terminalState", "<absent>") for r in workers("historical")]
+    assert {"released", "retained", "<absent>", "orphaned", "active"} <= set(states)
+    missing = load_fixture("missing-fields").cycle(0).envelope["result"]
+    assert "scope" not in missing and "total" not in missing["page"]
+    assert any("dispatchId" not in r for r in missing["workers"])
+    assert any(r.get("taskId") is None and "taskId" in r for r in missing["workers"])
+
+
+def test_long_identifiers_are_over_sixty_characters_with_cjk_and_emoji():
+    ids = [r["dispatchId"] for r in workers("long-identifiers")]
+    assert all(len(i) >= 60 for i in ids)
+    assert any(
+        any(0x3040 <= ord(ch) <= 0x30FF or 0x4E00 <= ord(ch) <= 0x9FFF for ch in i)
+        for i in ids
+    )
+    assert any(any(ord(ch) > 0x1F000 for ch in i) for i in ids)
+
+
+def test_duplicate_variant_has_duplicates_untimed_rows_and_a_backward_timestamp():
+    first = workers("duplicate-out-of-order", 0)
+    ids = [r["dispatchId"] for r in first]
+    assert len(ids) != len(set(ids))
+    assert "observedAt" not in first[3]["projection"]["liveness"]
+    old = workers("duplicate-out-of-order", 1)[0]["projection"]["liveness"][
+        "observedAt"
+    ]
+    assert old < first[0]["projection"]["liveness"]["observedAt"]
+
+
+# -- frozen marker (T34) ---------------------------------------------------------------------
+
+
+def test_a_frozen_fixture_row_comes_out_of_the_loader_with_fixture_frozen_true():
+    fixture = load_fixture("base")
+    page = fixture.parse(0, "fixture:base", 1)
+    frozen = [r.dispatch_id for r in page.rows if r.fixture_frozen]
+    assert frozen == ["w-003"]
+    assert "fixtureOnly" not in fixture.cycle(0).envelope["result"]["workers"][2]
+    assert page.rows[2].unrecognised_keys == 0
+    # source-rank offsets are honoured
+    assert [
+        r.dispatch_id
+        for r in fixture.parse(0, "fixture:base", 1, 100).rows
+        if r.fixture_frozen
+    ] == ["w-003"]
+
+
+def test_the_same_json_fed_straight_to_parse_page_leaves_it_false():
+    raw = (
+        resources.files(FIXTURE_PACKAGE)
+        .joinpath("base.json")
+        .read_text(encoding="utf-8")
+    )
+    import json
+
+    envelope = json.loads(raw)["cycles"][0]
+    page = parse_page(envelope, "fixture:base", 1)
+    assert not any(r.fixture_frozen for r in page.rows)
+    assert (
+        page.rows[2].unrecognised_keys == 1
+    )  # fixtureOnly is just an unknown key here
+
+
+# -- nothing sensitive in committed fixtures -------------------------------------------------
+
+SENSITIVE = {
+    "absolute path": re.compile(
+        r"(?<![\w.:/-])/(?:home|Users|tmp|var|etc|usr|opt|root|mnt|srv)/|\b[A-Za-z]:\\\\"
+    ),
+    "terminal handle": re.compile(r"term_"),
+    "token": re.compile(
+        r"sk-[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{16,}|xox[abprs]-|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}"
+        r"|[A-Fa-f0-9]{32,}|Bearer\s+\S+|(?i:secret|password|api[_-]?key)\"?\s*[:=]"
+    ),
+    "credential url": re.compile(r"://[^/\s\"]*:[^/\s\"]*@"),
+}
+
+
+@pytest.mark.parametrize("path", fixture_files(), ids=lambda p: p.name)
+def test_committed_fixtures_hold_no_path_handle_token_or_escape_byte(path):
+    text = path.read_text(encoding="utf-8")
+    assert "\x1b" not in text
+    assert not any(ord(ch) < 0x20 and ch not in "\n" for ch in text)
+    for what, pattern in SENSITIVE.items():
+        assert not pattern.search(text), f"{path.name}: {what}"
+
+
+def test_the_injection_variant_stores_escapes_as_json_escape_sequences_only():
+    text = (
+        resources.files(FIXTURE_PACKAGE)
+        .joinpath("injection.json")
+        .read_text(encoding="utf-8")
+    )
+    assert "\\u001b[31m" in text and "\\u001b]8;;" in text and "\\u009b" in text
+    assert "\\u202e" in text and "\\u0007" in text and "[bold]x[/bold]" in text
+    assert text.isascii()
+
+
+# -- shared test support ---------------------------------------------------------------------
+
+
+def test_subprocess_calls_fail_with_the_guard_message():
+    with pytest.raises(AssertionError, match="subprocess is blocked in tests/observe"):
+        subprocess.run([sys.executable, "-c", "pass"], check=False)
+    with pytest.raises(AssertionError, match="observe_real_process"):
+        subprocess.Popen([sys.executable, "-c", "pass"])
+
+
+@pytest.mark.observe_real_process
+def test_the_marker_lifts_the_subprocess_guard():
+    done = subprocess.run(
+        [sys.executable, "-I", "-c", "print('ok')"],
+        capture_output=True,
+        text=True,
+        check=True,
+    )
+    assert done.stdout.strip() == "ok"
+
+
+def test_pyproject_keeps_strict_markers_and_registers_the_marker():
+    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
+    assert '"--strict-markers"' in text
+    assert '"observe_real_process:' in text
+
+
+def test_fake_runner_and_discover_share_one_log_and_refuse_other_argv(
+    fake_runner, fake_discover, argv_log
+):
+    orca = fake_discover()
+    template = [orca, "orchestration", "worker-list", "--json", "--limit", "100"]
+    fake_runner(template, 10.0)
+    fake_runner([*template, "--run", "run-a", "--cursor", "abc"], 10.0)
+    assert argv_log == [
+        [orca, "skills", "list", "--json"],
+        template,
+        [*template, "--run", "run-a", "--cursor", "abc"],
+    ]
+    for bad in (
+        [orca, "check"],
+        [orca, "orchestration", "check", "--json"],
+        [*template, "--ack"],
+        [*template, "--run", "--evil"],
+        [*template, "--cursor", "-x"],
+        [orca],
+        [],
+    ):
+        assert not argv_allowed(bad)
+        with pytest.raises(AssertionError, match="allow-list"):
+            fake_runner(bad, 1.0)
+
+
+def test_fake_runner_responses_repeat_the_last_and_can_raise(argv_log):
+    from tests.observe.conftest import FakeRunner
+
+    runner = FakeRunner(
+        argv_log, [(0, "a"), TimeoutError("slow"), lambda argv, t: (2, "b")]
+    )
+    argv = ["orca", "orchestration", "worker-list", "--json", "--limit", "100"]
+    assert runner(argv, 1.0) == (0, "a")
+    with pytest.raises(TimeoutError):
+        runner(argv, 1.0)
+    assert runner(argv, 1.0) == (2, "b") and runner(argv, 1.0) == (2, "b")
+
+
+def test_fake_clock_advances_both_clocks_and_wall_jumps_leave_monotonic_alone():
+    clock = FakeClock()
+    mono, wall = clock.monotonic(), clock.wall()
+    clock.advance(5)
+    assert (clock.monotonic() - mono, clock.wall() - wall) == (5, 5)
+    clock.jump_wall(-3600)
+    assert clock.monotonic() - mono == 5 and clock.wall() - wall == 5 - 3600
+
+
+def test_make_rows_spreads_rows_over_distinct_runs(make_rows):
+    rows = make_rows(50, 5)
+    assert len(rows) == 50 and len({r["runId"] for r in rows}) == 5
+    assert len({r["dispatchId"] for r in rows}) == 50
+    for n_rows, n_runs in ((50, 10), (100, 8), (80, 5)):
+        generated = make_rows(n_rows, n_runs)
+        assert (
+            len(generated) == n_rows and len({r["runId"] for r in generated}) == n_runs
+        )
+
+
+def test_console_factory_builds_a_recording_console_through_make_console(
+    console_factory,
+):
+    console, policy = console_factory(width=116, height=30, ascii=True, no_color=True)
+    console.print("hello")
+    assert console.width == 116 and policy.ascii and policy.no_color
+    assert console.export_text().strip() == "hello"

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
