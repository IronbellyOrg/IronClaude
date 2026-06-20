# Research: Reader & Consumer Contracts

**Status:** Complete
**Date:** 2026-06-18

---

## TL;DR — Two discrepancies DEFINITIVELY RESOLVED

1. **`from_json` location:** Spec claims `logging_.py:46`. **WRONG.** The TRUE definition is **`src/superclaude/cli/swarm/models.py:1820`** `def from_json(cls: Type[T], payload: str) -> T`. `logging_.py` does NOT define `from_json` at all — it only imports `to_json` (`logging_.py:59`). `logging_.py:46` is a docstring line mentioning the round-trip. **[CODE-CONTRADICTED]** the spec's `logging_.py:46`.
   - **Poll-loop import line:** `from superclaude.cli.swarm.models import from_json, EventRecord`

2. **JSONL filename (fresh-run dispatch target):** Spec mentions `event-log.jsonl` vs `execution-log.jsonl`. **The real fresh-run write path uses `execution-log.jsonl`.** `event-log.jsonl` appears ONLY in stale docstrings (`logging_.py:7,44,92`; `models.py:1219`). The Logger filename is hard-coded at the `run_cmd` call site, NOT inside `logging_.py`. **`_tail_events` and the FR-7 test MUST point at `<manifest_dir>/execution-log.jsonl`.** **[CODE-VERIFIED]**

---

## 1. `should_enable_tui(flag, stream=None) -> bool`

`src/superclaude/cli/swarm/tui.py:74` **[CODE-VERIFIED]**

```python
def should_enable_tui(flag: bool, stream: Optional[IO] = None) -> bool:
```
- **Default stream:** `sys.stdout` (resolved at call: `tui.py:88` `target = stream if stream is not None else sys.stdout`).
- **Return semantics:** `False` if `flag` is falsy (`tui.py:86-87`); else returns `bool(target.isatty())` (`tui.py:88-95`). A stream lacking a callable `isatty` → `False` (`tui.py:90-91`); any exception from `isatty()` → `False` (`tui.py:94-95`).
- **Main-thread requirement:** The module docstring (`tui.py:11-22`) states "the run command MUST consult this helper before instantiating `TUI`" — the gate is two-part: `--tui` passed AND stream is a TTY. So `run_cmd` must call `should_enable_tui(tui_flag)` on the main thread BEFORE constructing `TUI`. **[CODE-VERIFIED]** (docstring + code agree).

## 2. `TUI` lifecycle

`src/superclaude/cli/swarm/tui.py:192` **[CODE-VERIFIED]**

- `__init__(self, *, console: Optional[Console] = None, refresh_per_second: int = 2)` — `tui.py:201-212`. **Default `refresh_per_second = 2`.** Keyword-only (note the `*`).
- `start(self) -> Live` — `tui.py:218-228`. Stamps `self._started_at`, builds + starts a `rich.live.Live` (`screen=False`), returns it. "Caller owns `stop()`."
- `stop(self) -> None` — `tui.py:230-234`. **Idempotent** (docstring line 231 + guard `if self._live is not None:` at `tui.py:232`; sets `self._live = None` after stopping so a second call is a no-op).
- `update(self, state: Optional[SwarmState], events: Iterable[EventRecord]) -> None` — `tui.py:236-245`. **Signature confirmed = `(Optional[SwarmState], Iterable[EventRecord])`.** Stores `state`, materializes `events` to a list (`tui.py:243` `self._events = list(events)`), and if Live is running, re-renders. **[CODE-VERIFIED]**
- `render(self, state, events) -> Panel` — `tui.py:251-270`. Pure; tests assert shape without a Live.

## 3. `_project_workers(events)`

`src/superclaude/cli/swarm/tui.py:145` **[CODE-VERIFIED]**

```python
def _project_workers(events: Iterable[EventRecord]) -> dict[int, WorkerSnapshot]:
```
- **Contributing event_types:** ONLY `worker_start`, `worker_progress`, `worker_done` (`tui.py:160-165`). `wave_transition` and `terminal` are skipped (they have `worker_index=None`, dropped at `tui.py:157-159`).
- **What makes a row "non-vacuous" (for the FR-7 test to assert):**
  - A snapshot exists for an index only if at least one `worker_*` event with non-None `worker_index` arrived (`tui.py:167` `workers.setdefault`).
  - `worker_start` flips status `pending → running` and stamps `started_at` (`tui.py:175-179`).
  - `worker_done` sets `status` from `payload["status"]` (fallback `"success"`) and `finished_at`; reads `payload["elapsed_ms"]` when it's a non-negative int (`tui.py:180-187`).
  - `model_label` is taken from `payload["model_label"]` or `payload["model_id"]`, first non-empty wins (`tui.py:171-173`).
  - So a NON-VACUOUS row = at least one entry in the returned dict with a `status` other than the default `"pending"` (i.e. `worker_start` or `worker_done` was folded in) and ideally a populated `model_label`/`elapsed`. The FR-7 test should assert `len(_project_workers(events)) >= 1` AND a row whose `status` ∈ {running, success, ...} (proves the stream was actually projected, not an empty dict).

## 4. `read_state(path) -> Optional[SwarmState]`

`src/superclaude/cli/swarm/state.py:178` **[CODE-VERIFIED]**

```python
def read_state(path: Union[str, os.PathLike[str]]) -> Optional[SwarmState]:
```
- **Returns `None` when the file is missing** (`state.py:190-193` catches `FileNotFoundError`).
- Returns `from_dict(SwarmState, json.loads(raw))` otherwise (`state.py:195-196`).
- Raises `json.JSONDecodeError` on corrupt JSON, `ValueError` on shape-valid-but-invalid `state` enum (`state.py:183-187` docstring + `from_dict`/`__post_init__`).
- **Filename convention:** `.swarm-state.json`. Constant `SWARM_STATE_FILENAME: str = ".swarm-state.json"` at **`commands.py:85`** (NOT in state.py — state.py is filename-agnostic, takes a path). The run path builds `output_dir / SWARM_STATE_FILENAME` (`commands.py:722`, `commands.py:2441`, `commands.py:2665`, `commands.py:2697`). Poll loop should call `read_state(manifest_dir / ".swarm-state.json")` — same dir as the execution log. **[CODE-VERIFIED]**

## 5. `from_json` — DEFINITIVE LOCATION

`src/superclaude/cli/swarm/models.py:1820` **[CODE-CONTRADICTED spec's logging_.py:46]**

```python
def from_json(cls: Type[T], payload: str) -> T:
    """Deserialize a swarm dataclass instance from a JSON string."""
    return from_dict(cls, json.loads(payload))
```
- Companion `to_json` at `models.py:1810` (`json.dumps(to_dict(instance), sort_keys=True)`).
- `logging_.py` imports only `to_json` (`logging_.py:59` `from superclaude.cli.swarm.models import EventRecord, to_json`); it has NO `from_json` symbol. `logging_.py:46` is prose inside the module docstring.
- **Exact import line the poll loop should use:**
  ```python
  from superclaude.cli.swarm.models import EventRecord, from_json
  ```
  Usage per-line: `from_json(EventRecord, line)`.
- **Independent corroboration:** `tests/swarm/test_dual_log_emission.py:41,115,215` import `from_json` from `...swarm.models` and call `from_json(EventRecord, line)` on each `execution-log.jsonl` line. **[CODE-VERIFIED]**

## 6. `EventRecord` dataclass

`src/superclaude/cli/swarm/models.py:1209` (decorated `@dataclass`) **[CODE-VERIFIED]**

Fields (`models.py:1284-1287`):
| Field | Type | Default |
|---|---|---|
| `event_type` | `EventType` (Literal: worker_start/worker_progress/worker_done/wave_transition/terminal) | `"worker_start"` |
| `timestamp` | `str` | `""` |
| `worker_index` | `Optional[int]` | `None` |
| `payload` | `dict[str, Any]` | `field(default_factory=dict)` |

- `__post_init__` (`models.py:1289-1295`) raises `ValueError` for an out-of-enum `event_type`.
- `to_json(rec)` → `models.py:1810`; round-trip `from_json(EventRecord, to_json(rec))` is the documented contract (`logging_.py:44-49` docstring; enforced in `tests/swarm/test_logging.py` and `tests/swarm/test_dual_log_emission.py:115,215`). **Round-trip CONFIRMED.** **[CODE-VERIFIED]**

## 7. CRITICAL filename truth — fresh-run dispatch JSONL target

**Answer: `execution-log.jsonl`** (NOT `event-log.jsonl`). **[CODE-VERIFIED]**

(a) **Constant name + value used by run_cmd's Logger:** There is NO shared constant for the *write* path — the filename is a string literal at the `run_cmd` Logger construction site:
- `commands.py:1733` `jsonl_path=manifest_dir / "execution-log.jsonl"`
- `commands.py:1734` `md_path=manifest_dir / "execution-log.md"`
- The matching `swarm logs` *reader* constants are `EXECUTION_LOG_JSONL_FILENAME = "execution-log.jsonl"` and `EXECUTION_LOG_MD_FILENAME = "execution-log.md"` at `commands.py:99-100` (used by `logs_cmd` at `commands.py:3008`).

(b) **Directory it lives in:** `manifest_dir = Path(preflight_result.manifest_path).parent` (`commands.py:1730`) — i.e. a sibling of `manifest.json` inside the job's `--output` directory. This is the SAME directory as `.swarm-state.json` (`commands.py:1731` `state_output_dir = manifest_dir`). So the poll loop reads BOTH `manifest_dir/.swarm-state.json` and `manifest_dir/execution-log.jsonl`.

(c) **Is `event-log.jsonl` real or stale?** STALE — docstrings only. Hits: `logging_.py:7,44,92` (docstrings), `models.py:1219` (docstring). ZERO write-path or constant hits. The Logger class itself is filename-agnostic (takes `jsonl_path`/`md_path` args, `logging_.py:82-115`); its docstring examples just predate the `execution-log` rename.

- `event-log.jsonl` → **[CODE-CONTRADICTED]** as a real write path (docstring-only).
- `execution-log.jsonl` → **[CODE-VERIFIED]** real write path (`commands.py:1733`) + reader constant (`commands.py:99`) + test fixture (`tests/swarm/test_dual_log_emission.py:69,88`).

## 8. C3/AC-004 no-change invariants (record verbatim)

**`dispatch_wave1` — `src/superclaude/cli/swarm/dispatch.py:334-343` [CODE-VERIFIED]:**
```python
def dispatch_wave1(
    preflight_result: PreflightResult,
    transport: Optional[Transport] = None,
    *,
    transport_for_slot: Optional[Callable[[int], Transport]] = None,
    prompt: str = "",
    parallel_executor: Optional[ParallelExecutor] = None,
    worker_spec: Optional[WorkerSpec] = None,
    logger: Optional[Logger] = None,
) -> list[WorkerResult]:
```
The TUI wiring must NOT alter this signature (AC-004). The TUI poll loop lives in `run_cmd` (the caller), not in `dispatch_wave1`.

**`ParallelExecutor` (NFR-001 frozen) — `src/superclaude/execution/parallel.py:80` [CODE-VERIFIED]:**
- `class ParallelExecutor` (`parallel.py:80`)
- `def __init__(self, max_workers: int = 10)` (`parallel.py:100`)
- `def plan(self, tasks: List[Task]) -> ExecutionPlan` (`parallel.py:103`)
- `def execute(self, plan: ExecutionPlan) -> Dict[str, Any]` (`parallel.py:169`)

These must stay frozen; dispatch routes through this executor (`dispatch.py:346-351` docstring AC-004/NFR-001).

## 9. Existing byte-offset / incremental JSONL tail reader to mirror

**FOUND.** `_follow_log_file` at `src/superclaude/cli/swarm/commands.py:2737` (signature starts ~2738; called by `logs_cmd`). **[CODE-VERIFIED]** The reusable byte-offset pattern that `_tail_events` should mirror:
- Tracks `last_pos` (byte position) — seeded as `len(existing.encode("utf-8"))` (`commands.py:2790`).
- Helper `_drain_appended(log_path, start_pos) -> int` at `commands.py:2834`: `open(log_path, "rb")`, `fh.seek(start_pos)`, `fh.read()`, returns `fh.tell()` as the new offset (`commands.py:2844-2847`). **This is the exact byte-offset, exactly-once primitive `_tail_events` needs.**
- **Partial-line tolerance:** on `UnicodeDecodeError` this variant uses `errors="replace"` (`commands.py:2853-2856`); for `_tail_events` the cleaner approach is to track offset only up to the last complete `\n` so a half-written JSON line is re-read next poll (the spec's "partial-line tolerant" requirement). The byte-offset + re-stat + truncation-restart skeleton (`commands.py:2808-2825`) is directly mirrorable.
- Truncation handling: `if size < last_pos: last_pos = 0` (`commands.py:2818-2822`).

**Note:** `_follow_log_file` *prints to stdout* (it's the CLI `logs --follow` surface), so `_tail_events` cannot reuse it as-is — it must be a new helper that yields parsed `EventRecord`s instead of echoing. But the byte-offset bookkeeping (`last_pos` / seek / tell / truncation-restart) is the proven pattern to copy.

---

## Summary table of signatures

| Symbol | File:Line | Signature / Value |
|---|---|---|
| `should_enable_tui` | tui.py:74 | `(flag: bool, stream: Optional[IO] = None) -> bool`; default stream `sys.stdout` |
| `TUI.__init__` | tui.py:201 | `(*, console=None, refresh_per_second: int = 2)` |
| `TUI.start` | tui.py:218 | `() -> Live` |
| `TUI.stop` | tui.py:230 | `() -> None` (idempotent) |
| `TUI.update` | tui.py:236 | `(state: Optional[SwarmState], events: Iterable[EventRecord]) -> None` |
| `_project_workers` | tui.py:145 | `(events: Iterable[EventRecord]) -> dict[int, WorkerSnapshot]`; worker_*-only |
| `read_state` | state.py:178 | `(path) -> Optional[SwarmState]`; None if missing |
| `from_json` | **models.py:1820** | `(cls: Type[T], payload: str) -> T` |
| `to_json` | models.py:1810 | `(instance) -> str` |
| `EventRecord` | models.py:1209 | fields: event_type, timestamp, worker_index:Optional[int], payload:dict |
| `SwarmState` | models.py:1140 | fields: state, job_id, updated |
| `dispatch_wave1` | dispatch.py:334 | (verbatim above) — FROZEN (AC-004) |
| `ParallelExecutor.execute` | parallel.py:169 | `(plan: ExecutionPlan) -> Dict[str, Any]` — FROZEN (NFR-001) |
| `_follow_log_file` / `_drain_appended` | commands.py:2737 / 2834 | byte-offset tail pattern to mirror |
| `SWARM_STATE_FILENAME` | commands.py:85 | `".swarm-state.json"` |
| Logger jsonl write path | commands.py:1733 | `manifest_dir / "execution-log.jsonl"` |

## Two resolved discrepancies (restated)

1. **`from_json` is in `models.py:1820`**, not `logging_.py:46`. Import: `from superclaude.cli.swarm.models import EventRecord, from_json`.
2. **Fresh-run dispatch appends to `execution-log.jsonl`** (sibling of `manifest.json`, `commands.py:1733`), not `event-log.jsonl` (docstring-only/stale). `_tail_events` + FR-7 test → `manifest_dir / "execution-log.jsonl"`.
