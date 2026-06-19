# Research: Test & Verification

**Status:** Complete
**Date:** 2026-06-18

> **Headline verdict (highest-risk claim #5):** [CODE-VERIFIED] The `stub` transport
> DOES emit `worker_start`/`worker_done` events to `<output>/execution-log.jsonl` on a
> fresh `--lens bare-review --transport stub --output <tmp>` run. An existing test
> (`test_run_cmd_stub_transport_dispatches_workers_not_noop`, test_commands_run.py:507)
> already proves exactly 3 `worker_done` lines land in the log — I re-ran it green
> (0.18s). FR-7's "≥1 worker row" is therefore satisfiable purely from the tailed
> log with NO live-proxy and NO `TUI.update` proxy. **The FR-7 test is essentially a
> variant of test_commands_run.py:507 that ALSO drives `--tui` through a forced-TTY seam.**

---

## TL;DR for the builder

- **FR-1 (tighten vacuous audit):** The only TUI-reachability audit in
  `test_inv012_tui_opt_in.py` is `test_commands_module_does_not_construct_tui_outside_gate`
  (line 543). It is **vacuous today** because it `return`s early when `"TUI(" not in source`
  (line 575-578) — and `commands.py` contains **zero** `TUI(`/`should_enable_tui`/`Live`
  references right now ([CODE-VERIFIED] via grep), so the assert at line 579 never runs.
  Tighten by adding an **AST import-graph audit** mirroring the existing
  `_ShellDispatchVisitor` pattern in `test_concurrency_python_only.py:191` (INV-002),
  asserting `tui`/`TUI`/`Live`/`rich.console.Console`/`rich.live.Live` symbols are NOT
  imported/referenced by `dispatch.py`, `parallel.py`, or `_run_worker` — plus a runtime
  `threading.get_ident()` main-thread assertion on `TUI.update` (tui.py:236).
- **FR-7 (forced-TTY integration test):** Adapt `test_commands_run.py:507`. Drive
  `run_cmd` via `CliRunner` with `--lens bare-review --transport stub --target <f> --output <dir>`,
  monkeypatch the deferred `should_enable_tui` import to return `True` (seam recommended
  in §4), read `<dir>/execution-log.jsonl`, project via `_project_workers` (tui.py:145),
  assert ≥1 non-vacuous worker row, **plus** an INV-012 companion assertion that
  `result.output` (CliRunner stream is non-TTY) carries zero ANSI.

---

## 1. `test_inv012_tui_opt_in.py` vacuity analysis (FR-1)

### The vacuous audit test

`test_commands_module_does_not_construct_tui_outside_gate` —
`tests/swarm/test_inv012_tui_opt_in.py:543-583`. The load-bearing body:

```python
source = commands_path.read_text(encoding="utf-8")
if "TUI(" not in source:
    # No wiring yet: audit is vacuously satisfied. Test stays green
    # so the wiring task can land without re-editing this file.
    return                                          # <-- line 578: EARLY RETURN
assert "should_enable_tui" in source, (             # <-- line 579: NEVER REACHED today
    "commands.py constructs TUI(...) without referencing should_enable_tui ..."
)
```

**Why it is vacuous (the spec's "vacuous grep audit"):**

1. **The guard never fires today.** [CODE-VERIFIED]
   `grep -n "TUI(\|should_enable_tui\|Live\|rich.console\|rich.live" src/superclaude/cli/swarm/commands.py`
   returns only one hit — an unrelated `"Live-tail the log file"` docstring at
   commands.py:2904. There is **no** `TUI(` substring, so line 578 `return`s and the
   assert at 579 is dead code. The test passes by doing nothing.
2. **Even once wiring lands, the substring check is weak.** It only verifies the two
   strings `TUI(` and `should_enable_tui` **co-occur anywhere in the module file** — it
   does NOT prove they are paired in the same function body (the docstring at 543-557
   explicitly admits "same function body" is the intent but the implementation only does
   a module-wide substring scan). A wiring that constructs `TUI(...)` in `run_cmd` while
   `should_enable_tui` is referenced in some unrelated helper would pass.
3. **It audits only `commands.py`, not the reachability surface FR-1 demands.** FR-1
   requires asserting TUI symbols are unreachable from `dispatch.py` / `parallel.py` /
   `_run_worker`. The current test never looks at those files at all. A regression that
   imported `Live` into `dispatch.py` (the INV-012 "no Rich on worker threads" violation)
   would not be caught here.

The `test_pty_invocation_with_tui_flag_when_wired` test (line 436) is **also currently a
skip** — `_run_cmd_has_tui_flag()` (line 416) returns False because `--tui` isn't wired,
so it `pytest.skip`s (line 453). [CODE-VERIFIED] — once `--tui` lands this activates, but
it requires a real subprocess + PTY and is slow; it is NOT the FR-7 integration test
(FR-7 wants an in-process CliRunner test against real dispatch with a forced seam).

### Recommended tightening (concrete)

**Reuse the existing AST visitor pattern.** `tests/swarm/test_concurrency_python_only.py`
(INV-002) is the canonical analog and the best thing to copy:

- `import ast` + `from pathlib import Path` (test_concurrency_python_only.py:41-42).
- `_iter_swarm_py_sources() -> list[Path]` (line 145) — already enumerates swarm `.py`
  sources; reuse or narrow to `{dispatch.py, parallel.py}`.
- `class _ShellDispatchVisitor(ast.NodeVisitor)` (line 191) with `visit_Import` /
  `visit_ImportFrom` collecting `(lineno, name)` hits (lines 194-211), `_resolve_attribute_chain`
  for `module.attr` call detection (line 171).
- `_scan_module(path) -> (import_hits, call_hits)` (line 224) — `ast.parse(source, filename=...)`
  then `visitor.visit(tree)`.
- **Mutation guard tests** (lines 341, 357) that feed a synthetic source with the forbidden
  import and assert the visitor flags it — FR-1 should include the equivalent so the audit
  is provably non-vacuous (assert a synthetic `import rich.live` IS caught).

**Static reachability assertion for FR-1** (new `_TuiSymbolVisitor` mirroring the above):

For each of `dispatch.py`, `parallel.py` (and, since `_run_worker` lives in `dispatch.py`,
that file covers the `_run_worker` requirement), assert the AST contains:

- No `Import`/`ImportFrom` of `rich`, `rich.console`, `rich.live`, `rich.panel`,
  `rich.table`, or `superclaude.cli.swarm.tui`.
- No `Name`/`Attribute` reference to `TUI`, `Live`, `Console`, or `should_enable_tui`.

Note the AST walk gives true reachability over the **module's own** symbol table, but it
does NOT transitively follow into callees in OTHER modules. The spec phrase "or any callable
they invoke" is best satisfied two ways: (a) the AST import audit on each of the 3 files
guarantees none of them can NAME a TUI symbol, and (b) the **runtime main-thread assertion**
below proves that even if some callee did touch the TUI, it could only do so on the main
thread. Recommend documenting that the AST audit is per-file (not whole-program) and that
the runtime probe is the transitive backstop — do not over-claim whole-program reachability
from a single-file AST walk [UNVERIFIED that a pure-AST whole-program walk is feasible here;
the per-file + runtime-probe combination is the pragmatic FR-1 contract].

**Runtime `threading.get_ident()` main-thread assertion on `TUI.update`** (FR-1 second half):
`TUI.update` is at `src/superclaude/cli/swarm/tui.py:236`. The cleanest test-only approach
(no production change required if the test owns the probe):

```python
import threading
from superclaude.cli.swarm.tui import TUI

def test_tui_update_only_runs_on_main_thread(monkeypatch):
    main_ident = threading.get_ident()
    seen_idents = []
    real_update = TUI.update
    def _probe(self, state, events):
        seen_idents.append(threading.get_ident())
        return real_update(self, state, events)
    monkeypatch.setattr(TUI, "update", _probe)
    # ... drive a forced-TTY run (see FR-7 §4) so the dispatch loop calls update ...
    assert seen_idents, "TUI.update was never invoked — assertion is vacuous"
    assert all(i == main_ident for i in seen_idents), (
        f"TUI.update ran off the main thread: {seen_idents} vs main {main_ident}"
    )
```

The vacuity guard (`assert seen_idents`) is mandatory — without it the all() passes
trivially over an empty list. Mirror the "content sanity" guards the existing file already
uses (e.g. test_inv012_tui_opt_in.py:160-162, 348-352) so the reviewer recognizes the idiom.

**No existing AST-walk helper is shared/importable** — each audit file defines its own
visitor locally ([CODE-VERIFIED] — `test_concurrency_python_only.py`, `test_inv_suite.py`,
`test_output_confinement.py`, `test_no_scoring_engine.py`, `test_no_response_cache.py`,
`test_parallel_executor_routing.py` each `import ast` independently). Copy the visitor
shape locally into the FR-1 test; do not try to import across test modules.

---

## 2. `test_tui.py` reusable patterns (FR-7 building blocks)

File `tests/swarm/test_tui.py` — every FR-7 building block is here.

### `_FakeTTY` (the forced-TTY stream fixture)

`tests/swarm/test_tui.py:41-45` (an identical copy also lives in
test_inv012_tui_opt_in.py:209-213):

```python
class _FakeTTY(io.StringIO):
    """In-memory stream that claims to be a TTY (for the on-path test)."""
    def isatty(self) -> bool:  # type: ignore[override]
        return True
```

This is the in-memory positive-path stream: `should_enable_tui(True, _FakeTTY())` is True
([CODE-VERIFIED] test_tui.py:98-100). FR-7 can pass `_FakeTTY()` to `should_enable_tui`
directly in a unit-level assertion, but the **integration** test (§4) needs the seam to be
reachable from inside `run_cmd`, where the stream is `sys.stdout` (CliRunner pipes it).

### EventRecord construction helper + worker projection

`_render_to_string` (test_tui.py:48-79) builds a representative `EventRecord` stream
covering `worker_start` + `worker_done` and renders through a captured `Console`. The
`EventRecord` shape (constructed verbatim, test_tui.py:58-77):

```python
EventRecord(
    event_type="worker_start",
    timestamp="2026-06-01T15:00:00+00:00",
    worker_index=0,
    payload={"model_label": "alpha-7b", "timeout_sec": 180},
)
EventRecord(
    event_type="worker_done",
    timestamp="...",
    worker_index=0,
    payload={"status": "success", "elapsed_ms": 3210},
)
```

`_project_workers(events)` (tui.py:145, exercised in test_tui.py:117-196) is the
projection FR-7 should call to turn the tailed log into worker rows:

- `_project_workers` returns `dict[int, WorkerSnapshot]` keyed by `worker_index`
  ([CODE-VERIFIED] test_tui.py:133-134 `set(projected) == {2}`).
- `WorkerSnapshot` carries `.status` / `.model_label` / `.elapsed_seconds`
  (test_tui.py:136-139). `worker_done.payload['elapsed_ms']` → `elapsed_seconds`
  (4200ms → 4.2s, test_tui.py:139).
- A lone `worker_start` projects to `status="running"` (test_tui.py:142-156).
- `wave_transition` / `terminal` events (worker_index=None) are skipped — NOT per-worker
  rows (test_tui.py:159-175 → `{}`).

**FR-7 "≥1 non-vacuous worker row" recipe:** read `execution-log.jsonl`, parse each line
via `from_json(EventRecord, line)` (see §5/§6), call `_project_workers(records)`, assert
`len(projected) >= 1` AND each row's `.model_label`/`.status` is populated (non-vacuous).
The stub run produces `model_label="stub-model-00"` and `status="success"` ([CODE-VERIFIED]
stub.py:67/146-153 + dispatch.py:316-328 stamp `model_id`/`model_label`/`status` into the
`worker_done` payload).

### Render no-ANSI / ANSI control helpers

`_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")` (test_tui.py:38). The richer two-pattern
form `_ANSI_CSI_RE` + `_ANY_ESC_RE` and `_assert_no_ansi(payload, source=...)` live in
test_inv012_tui_opt_in.py:69-88 — **reuse `_assert_no_ansi` for the FR-7 INV-012 companion
assertion** (zero ANSI on the non-TTY CliRunner stream). It checks both CSI and bare-ESC.

---

## 3. `test_commands_run.py` scaffolding (FR-7 invocation pattern)

The FR-7 test should be modeled directly on
`test_run_cmd_stub_transport_dispatches_workers_not_noop`
(`tests/swarm/test_commands_run.py:507-568`) — the existing **real-dispatch, no-monkeypatch**
stub test. Representative invocation (test_commands_run.py:520-560), verbatim shape:

```python
from click.testing import CliRunner
from superclaude.cli.swarm.commands import run_cmd, EXIT_OK

def test_xxx(tmp_path):
    target = tmp_path / "target.py"
    target.write_text(
        "# regression target\n"
        + "def hello() -> str:\n    return 'real stub dispatch'\n"
        + "# padding to clear the IMM-4 non-whitespace byte floor\n" * 6,
        encoding="utf-8",
    )
    output_dir = tmp_path / "out"
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        ["--lens", "bare-review", "--transport", "stub",
         "--target", str(target), "--output", str(output_dir)],
    )
    assert result.exit_code == EXIT_OK, f"...{result.stdout}\n{result.stderr}"
    assert "workers=3" in result.stdout
    assert "results=3" in result.stdout
    jsonl = output_dir / "execution-log.jsonl"          # <-- the FR-7 event source
    assert jsonl.is_file()
    log_body = jsonl.read_text(encoding="utf-8")
    assert log_body.count("worker_done") == 3
```

Key scaffolding facts ([CODE-VERIFIED]):

- **tmp dir + minimal spec**: the `--lens bare-review` shortcut needs NO spec file — just
  `--target` + `--output` (run_cmd lens path, commands.py:729 `_lens_to_jobspec`). The
  `--target` file must clear the **IMM-4 byte floor (≥50 non-whitespace bytes)** — that's
  why the fixture pads with repeated comment lines (test_commands_run.py:520-526).
- **Spec-file mode alternative** (test_commands_run.py:149-173, `_runnable_spec`): writes a
  full JobSpec JSON, sets `spec["transport"]["kind"] = "stub"`, `target.path`/`output.dir`
  under `tmp_path`. Use lens mode for FR-7 (less boilerplate).
- **Artifact assertions**: read `output_dir / "execution-log.jsonl"`, count `worker_done`
  (test_commands_run.py:559-568). `bare-review` default_workers=3 → 3 `worker_done` lines.
- **`tmp_path`** is the standard pytest fixture; CliRunner captures `result.stdout` /
  `result.stderr` / `result.output` (combined) and `result.exit_code`.
- **Exit constants** import from `superclaude.cli.swarm.commands`: `EXIT_OK`,
  `EXIT_INVALID`, `EXIT_USAGE` (test_commands_run.py:41-46).

---

## 4. Forced-TTY seam for FR-7 (making `should_enable_tui` return True under CliRunner)

**Problem:** CliRunner pipes stdout to an in-memory buffer whose `isatty()` is False, so
`should_enable_tui(flag, sys.stdout)` returns False and the dashboard never starts — even
if `--tui` is wired and passed. FR-7 needs the gate to open inside `run_cmd`.

**The seam depends on how `run_cmd` will import the helper.** R1 (commands.py seam research)
and the deferred-import note establish that `run_cmd` will import `should_enable_tui` via a
**deferred (function-local) import** `from superclaude.cli.swarm.tui import should_enable_tui`
(mirroring the existing deferred imports inside `run_cmd` — e.g. `from ...logging_ import
Logger as _Logger` at commands.py:1728, `from ...transports.openai_compat import
TransportEnvError` at 1757, `from ...models import from_dict as _from_dict` at 1800).
[CODE-VERIFIED that run_cmd uses function-local deferred imports for its collaborators.]

### Recommended option: monkeypatch `should_enable_tui` on the SOURCE module

Because the import is deferred (resolved at call time from the source module), the correct
monkeypatch target is the **source module**, not a `commands` re-export:

```python
import superclaude.cli.swarm.tui as tui_mod
monkeypatch.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)
```

**Rationale:** A deferred `from ...tui import should_enable_tui` binds the name fresh from
`tui_mod` each time `run_cmd` executes, so patching `tui_mod.should_enable_tui` is picked up.
This is the SAME idiom test_commands_run.py:322-324 already uses for `dispatch_wave1`:
> "The run_cmd body does a lazy import; patch the source module so the lazy import inside
> the function picks up the fake."
There, `monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _fake_dispatch)` patches the
source `superclaude.cli.swarm.dispatch` module. The TUI seam follows the same rule.

**Caveat for the builder — coordinate with R1:** IF R1 finds `run_cmd` instead does a
**module-top import** (`from .tui import should_enable_tui` at the top of `commands.py`),
the bound name lives on the `commands` module and the target becomes
`monkeypatch.setattr("superclaude.cli.swarm.commands.should_enable_tui", lambda *a, **k: True)`.
The task file should make the monkeypatch target conditional on the actual import style the
implementation track chooses, and the builder must verify it against the landed `run_cmd`
(grep for `should_enable_tui` import location after wiring lands). Recommend the **deferred
import + source-module patch** because it matches every other collaborator in `run_cmd`.

### Rejected alternative: monkeypatch the stream

Patching `sys.stdout` to a `_FakeTTY()` is fragile under CliRunner (CliRunner installs its
own captured stream and Click reads `ctx.obj` / its own stdout proxy). It also wouldn't make
Rich emit ANSI into a StringIO that CliRunner can read back. Patching the gate boolean is
cleaner and isolates the test from Rich/Click TTY-autodetect plumbing. (The real PTY path
is already covered by the slow `test_pty_invocation_with_tui_flag_when_wired`, line 436.)

### INV-012 companion in the SAME FR-7 test

After the forced-TTY run, FR-7 must also assert the **non-TTY** output is ANSI-free. Under
CliRunner the captured stream is non-TTY regardless of the gate monkeypatch (the gate is
faked, but the actual Rich Console writes to a non-terminal buffer → Rich suppresses ANSI).
Assert with the existing helper: `_assert_no_ansi(result.output, source="FR-7 run_cmd --tui")`.
This pins that opening the gate via the flag does NOT leak escapes when the real stream is a
pipe — the core INV-012 contract.

---

## 5. Stub-transport event-emission trace (CRITICAL — claim #5)

**VERDICT: [CODE-VERIFIED] — stub DOES emit `worker_start`/`worker_done` to
`execution-log.jsonl`. FR-7's "≥1 worker row" is satisfiable from the tailed log alone.**

Full call chain traced through real source (not assumption):

1. **`run_cmd` constructs the Logger** when `--output` is in play —
   `commands.py:1727-1740`: `logger = _Logger(jsonl_path=manifest_dir / "execution-log.jsonl",
   md_path=manifest_dir / "execution-log.md", output_dir=manifest_dir)`. `manifest_dir` is
   the parent of `preflight_result.manifest_path` (commands.py:1730), i.e.
   `<output>/execution-log.jsonl` (filename const `EXECUTION_LOG_JSONL_FILENAME =
   "execution-log.jsonl"`, commands.py:99). [Matches R2's resolved filename.]
2. **`run_cmd` calls `dispatch_wave1(..., logger=logger)`** — commands.py:1807-1813, passing
   the real logger and a concrete `transport_for_slot` factory (stub branch shares one
   `StubTransport`, test_commands_run.py:344-361).
3. **`dispatch_wave1` → `_make_callable` → `_run_worker`** — dispatch.py:443-461. Each slot
   calls `_run_worker(slot_index, slot_transport, prompt, effective_spec, logger)`.
4. **`_run_worker` emits the paired events** — dispatch.py:279-331. **Exact log_event call
   sites:**
   - `worker_start`: **dispatch.py:302-308** —
     `logger.log_event(EventRecord(event_type="worker_start", worker_index=index,
     payload={"timeout_sec": spec.timeout_sec}))`.
   - `worker_done`: **dispatch.py:311-330** —
     `logger.log_event(EventRecord(event_type="worker_done", worker_index=index,
     payload={"status": result.status, "http_code": ..., "attempts": ..., "elapsed_ms": ...,
     "model_id": result.model_id, "model_label": result.model_label}))`.
5. **Stub returns `status="success"` with `model_id`/`model_label`** — stub.py:146-153
   (`status="success"`, `http_code=200`, `model_id`/`model_label = self._model_id` which
   defaults to `"stub-model-00"`, stub.py:67). So the `worker_done` payload carries
   non-empty `status` and `model_label` → `_project_workers` yields a **non-vacuous** row
   (`WorkerSnapshot(status="success", model_label="stub-model-00")`).
6. **Wave-bracket events**: `dispatch_wave1` also emits `wave_transition` before/after the
   fan-out (dispatch.py:431-441 and 494-506) — these have `worker_index=None` and are
   correctly skipped by `_project_workers` (test_tui.py:159-175).

**Live-proof:** `uv run pytest
tests/swarm/test_commands_run.py::test_run_cmd_stub_transport_dispatches_workers_not_noop`
→ **1 passed in 0.18s** — and that test asserts
`log_body.count("worker_done") == 3` (test_commands_run.py:566). So a fresh stub run writes
exactly N=3 `worker_done` lines for `bare-review`. **No CRITICAL gap.** FR-7 does NOT need a
live proxy or a `TUI.update` interception to source worker rows; the durable JSONL is the
source of truth.

> **Note on the projection input:** `_project_workers` needs `EventRecord` instances. Parse
> each JSONL line with `from_json(EventRecord, line)` (models.py:1820, module-level
> function — there is NO `EventRecord.from_json` instance/classmethod; the dataclass
> round-trips via the module-level `from_json`/`to_json`). Usage precedent:
> test_logging.py:57,83 `restored = from_json(EventRecord, lines[0])`. Import:
> `from superclaude.cli.swarm.models import EventRecord, from_json`.

---

## 6. Partial-line / exactly-once fixture for FR-4 acceptance

**`from_json` on a truncated line raises `json.JSONDecodeError`** — [CODE-VERIFIED] by
direct probe: `from_json(EventRecord, '{"event_type":"worker_do')` → `json.JSONDecodeError`.
So a naive tailer that feeds every raw read to `from_json` WILL raise on a mid-line
truncation. The FR-4 reader contract (R2's track) must therefore: buffer until a newline,
parse only complete (newline-terminated) lines, and carry the trailing partial fragment to
the next poll — never `from_json` a fragment.

### Test recipe for FR-4 (append + mid-line truncation + exactly-once)

Closest existing analog: `tests/swarm/test_nfr002_atomicity.py:222-302` — the T03.16
"exactly-once delivery, no partial line" validation. It builds the JSONL with concurrent
writers, then asserts:
- `lines = raw.splitlines()` then `for line in lines: json.loads(line)` raises on no line
  (nfr002:276-284) — proves no interleaved/partial line is observable.
- each `(thread_id, step)` coordinate appears **exactly once** (nfr002:235, the
  exactly-once invariant).

For the FR-4 tailer test (incremental append with a deliberate partial), recommend a
self-contained `tmp_path` fixture (no concurrency needed — determinism is easier):

```python
def test_tailer_handles_partial_line_exactly_once(tmp_path):
    log = tmp_path / "execution-log.jsonl"
    rec1 = '{"event_type":"worker_start","timestamp":"...","worker_index":0,"payload":{}}\n'
    rec2 = '{"event_type":"worker_done","timestamp":"...","worker_index":0,"payload":{"status":"success"}}\n'
    # 1) write rec1 + a PARTIAL rec2 (no trailing newline)
    log.write_text(rec1 + rec2[:20], encoding="utf-8")
    reader = <FR-4 reader>(log)           # the COMP component R2 specifies
    batch1 = list(reader.poll())
    assert [e.event_type for e in batch1] == ["worker_start"]  # partial NOT delivered, NO raise
    # 2) complete rec2 by appending the remainder
    with log.open("a", encoding="utf-8") as fh:
        fh.write(rec2[20:])
    batch2 = list(reader.poll())
    assert [e.event_type for e in batch2] == ["worker_done"]    # delivered exactly once now
    # 3) exactly-once: a third poll with no new bytes yields nothing
    assert list(reader.poll()) == []
```

The three assertions pin: (a) no parse error on the partial line, (b) the completed line is
delivered on the next poll, (c) no re-delivery of already-emitted records (exactly-once).
Use `log.open("a")` for the incremental append (mirrors the production `O_APPEND` logger,
logging_.py:32,156). `tmp_path` gives an isolated jsonl per test.

> Coordinate with R2: the reader class/offset-tracking contract (what `<FR-4 reader>` is,
> whether it tracks byte offset via `tell()`/`seek()` or line count) is R2's deliverable.
> This section provides the **test shape**; R2 provides the **reader API** the test targets.
> No incremental tailer currently exists in `logging_.py` ([CODE-VERIFIED] — grep found no
> `tail`/`seek`/`tell`/partial-line reader in logging_.py; the existing readers
> `splitlines()` a fully-written file, e.g. test_logging.py).

---

## 7. Test execution commands

UV-only (project rule). The active venv is `.venv`; ignore the `VIRTUAL_ENV=/lsiopy`
warning (harmless — UV uses the project `.venv`).

```bash
# All swarm tests
uv run pytest tests/swarm/ -q

# Just the two TUI test files (FR-1 + FR-7 land here)
uv run pytest tests/swarm/test_tui.py tests/swarm/test_inv012_tui_opt_in.py -q

# The exact stub-dispatch precedent for FR-7 (verified green, 0.18s)
uv run pytest tests/swarm/test_commands_run.py::test_run_cmd_stub_transport_dispatches_workers_not_noop -q

# A single new test by node id once authored
uv run pytest tests/swarm/test_inv012_tui_opt_in.py::test_<new_name> -x -q
```

**Markers:** `pyproject.toml` registers `imm` and `inv` markers (pyproject.toml:138-139) but
**NOT a `tui` marker**. `--strict-markers` is on (pyproject.toml:111), so the FR-1/FR-7 tests
must **NOT** add an unregistered marker or collection fails. [CODE-VERIFIED] —
`test_inv012_tui_opt_in.py` and `test_tui.py` set **no** `pytestmark` (they are not in the
`-m inv` subset; conftest.py's `INV_COVERAGE_MAP` does not list INV-012). Leave the new tests
unmarked, matching the two existing TUI files. If a `tui` marker is desired, register it in
`pyproject.toml` markers first — but that is out of scope; the existing convention is unmarked.

---

## Final Summary

### FR-1 — tighten the vacuous INV-012 audit

- The vacuous test is `test_commands_module_does_not_construct_tui_outside_gate`
  (test_inv012_tui_opt_in.py:543). It `return`s at line 578 because `commands.py` has zero
  `TUI(` substring today → the reachability assert (line 579) is dead code. [CODE-VERIFIED]
- **Tighten:** add an AST import-graph audit (copy `_ShellDispatchVisitor` /
  `_scan_module` / `_iter_swarm_py_sources` from `test_concurrency_python_only.py:145-230`,
  INV-002) asserting NO import/reference of `rich`/`rich.console.Console`/`rich.live.Live`/
  `TUI`/`should_enable_tui` in `dispatch.py`, `parallel.py`, `_run_worker`. Include a
  mutation guard (synthetic `import rich.live` IS flagged) so the audit is provably
  non-vacuous.
- **Plus:** a runtime `threading.get_ident()` probe on `TUI.update` (tui.py:236) with a
  mandatory `assert seen_idents` vacuity guard, asserting all calls are on the main thread.
- **No shared AST helper exists** — define the visitor locally (every audit file does).

### FR-7 — forced-TTY run→tui integration test

- **Model on test_commands_run.py:507** (real stub dispatch, no monkeypatch on dispatch).
  Invoke `run_cmd` via `CliRunner` with `--lens bare-review --transport stub --target <f>
  --output <dir>` (target must clear the ≥50-byte IMM-4 floor — pad it).
- **Forced-TTY seam:** monkeypatch `should_enable_tui` to `True` on the **source module**
  (`superclaude.cli.swarm.tui`) because `run_cmd` resolves it via a deferred function-local
  import (same idiom as test_commands_run.py:322-324 for `dispatch_wave1`). Verify the import
  style against the landed wiring (coordinate with R1); if it becomes a module-top import,
  patch `superclaude.cli.swarm.commands.should_enable_tui` instead.
- **≥1 worker row:** read `<dir>/execution-log.jsonl`, parse lines via
  `from_json(EventRecord, line)` (models.py:1820), call `_project_workers` (tui.py:145),
  assert `len(projected) >= 1` and rows carry non-empty `status`/`model_label`
  (stub → `status="success"`, `model_label="stub-model-00"`).
- **INV-012 companion:** `_assert_no_ansi(result.output, source=...)`
  (helper at test_inv012_tui_opt_in.py:73) — CliRunner's stream is non-TTY so the real Rich
  Console must suppress ANSI even with the gate forced open.

### Stub-emission verdict (highest-risk claim, called out explicitly)

**[CODE-VERIFIED] — NO GAP.** The `stub` transport emits `worker_start` (dispatch.py:302)
and `worker_done` (dispatch.py:311) per slot into `<output>/execution-log.jsonl`, driven by
the Logger `run_cmd` wires at commands.py:1727-1740 and passes to `dispatch_wave1(...,
logger=logger)` at commands.py:1807. A fresh `--lens bare-review --transport stub` run
writes exactly 3 `worker_done` lines (verified: `test_run_cmd_stub_transport_dispatches_
workers_not_noop` passes in 0.18s, asserting `count("worker_done") == 3`). FR-7 sources its
worker rows from this durable JSONL — no live proxy, no `TUI.update` interception required.
