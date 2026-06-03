# R2 Research: Patterns & Conventions

**Status: In Progress**

**Scope:** `src/superclaude/cli/sprint/{checkpoints.py, logging_.py, models.py, commands.py, config.py}`
**Focus:** Concrete patterns the implementation must FOLLOW (style/conventions), with file:line evidence.

Paths below are relative to worktree root `/config/workspace/IronClaude/.claude/worktrees/SprintCLIWireDead/`.

---

## 1. Atomic temp+replace write idiom (template for FileHandoffStore)

**Source: `src/superclaude/cli/sprint/checkpoints.py:173-210` (`write_manifest`)**

The canonical atomic-write idiom in this codebase. Two distinct sub-patterns appear together:

### 1a. The atomic write idiom itself (checkpoints.py:207-210)

```python
output_path.parent.mkdir(parents=True, exist_ok=True)
tmp = output_path.with_suffix(output_path.suffix + ".tmp")
tmp.write_text(json.dumps(payload, indent=2) + "\n")
tmp.replace(output_path)
```

Exact conventions a `FileHandoffStore` MUST replicate:

1. **mkdir parents first** — `output_path.parent.mkdir(parents=True, exist_ok=True)` (line 207). Always called before the write; never assumes the dir exists.
2. **Temp suffix via `.with_suffix(output_path.suffix + ".tmp")`** (line 208) — appends `.tmp` to the *existing* suffix, so `manifest.json` → `manifest.json.tmp`. NOT a sibling random temp file, NOT `tempfile.mkstemp`. This keeps the temp on the same filesystem as the target so `replace()` is atomic.
3. **`tmp.write_text(...)`** (line 209) — full content written to the temp path in one call.
4. **`tmp.replace(output_path)`** (line 210) — `Path.replace()` (atomic rename, overwrites destination). NOT `tmp.rename()` (which is non-atomic-overwrite on some platforms), NOT `shutil.move`.
5. **Trailing newline on serialized JSON** — `json.dumps(payload, indent=2) + "\n"` (line 209). The `+ "\n"` is a consistent convention (see also §2 JSONL and the recovered-checkpoint render).

The docstring (checkpoints.py:178-180) states the rationale verbatim: *"Written atomically via a temp-file + replace so a partial write cannot corrupt an existing manifest."* A `FileHandoffStore` should carry the same rationale in its docstring.

### 1b. Payload-construction convention (checkpoints.py:181-205)

`write_manifest` computes summary counts first, then builds a single `payload` dict with a `generated_at` ISO-timestamp + a `summary` sub-object + an `entries` list-of-dicts:

```python
payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "summary": {"total": total, "found": found, "missing": missing, "recovered": recovered},
    "entries": [ {... per-entry dict ...} for e in entries ],
}
```

- Timestamps: `datetime.now(timezone.utc).isoformat()` (line 187). UTC, ISO 8601, via the module-level `from datetime import datetime, timezone` (checkpoints.py:13).
- `Path` fields serialized as `str(...)`: `"expected_path": str(e.expected_path)` (line 198).
- Dataclass entries are hand-serialized to dict literals inline (lines 195-203) — NOT via `dataclasses.asdict`. This is the same "explicit dict literal" convention `TaskResult.to_dict()` uses (see §3).

### 1c. Non-atomic write for the recovered-checkpoint body (contrast)

For the *report body* (not the manifest), checkpoints.py:276-277 uses a plain non-atomic write:

```python
entry.expected_path.parent.mkdir(parents=True, exist_ok=True)
entry.expected_path.write_text(report)
```

So the atomic temp+replace is reserved specifically for the **machine-readable JSON state file** that must not be corrupted by a partial write. A handoff *record store* (JSON state) should use the atomic idiom (§1a); a handoff *report markdown* may use the plain idiom.

---

## 2. SprintLogger event-writing pattern

**Source: `src/superclaude/cli/sprint/logging_.py`**

### 2a. The `_jsonl` sink (logging_.py:265-267)

```python
def _jsonl(self, data: dict):
    with open(self.config.execution_log_jsonl, "a") as f:
        f.write(json.dumps(data, default=str) + "\n")
```

Conventions:
- **Append mode** (`"a"`) — every event is one appended line; the log is never rewritten.
- **`json.dumps(data, default=str)`** — `default=str` makes datetimes/Paths/enums fall back to `str()` if not pre-serialized. (Most events still pre-serialize datetimes with `.isoformat()` — see below — so `default=str` is a safety net.)
- **`+ "\n"`** — one JSON object per line (JSONL).
- Target file is `self.config.execution_log_jsonl`, a SprintConfig property = `release_dir / "execution-log.jsonl"` (models.py:541-543).

### 2b. The event dict shape — every event has `"event"` first

Every `_jsonl` call passes a dict whose **first key is `"event": "<name>"`**, followed by event-specific fields, and (for events generated at write-time rather than from a result object) a trailing `"timestamp"`. Examples:

- `phase_start` (logging_.py:61-68): `event, phase, phase_name, phase_file, timestamp`.
- `checkpoint_verification` (logging_.py:179-188): `event, phase, expected, found, missing, timestamp`.
- `phase_rerun_start` (logging_.py:194-203): `event, phase, tasks, bundle, source_sha, timestamp`.

Field-value conventions:
- Lists are defensively re-wrapped: `"tasks": list(tasks)`, `"expected": list(expected)` (logging_.py:184-186, 198) — never the raw passed-in sequence.
- Timestamps generated at write-time: `"timestamp": datetime.now(timezone.utc).isoformat()` (logging_.py:186, 201, 217, 241) — via `from datetime import datetime, timezone` (logging_.py:6).
- Enums emitted via `.value`: in `write_phase_result`, `"status": result.status.value` (logging_.py:97).
- Datetimes from a result object emitted via `.isoformat()`: `result.started_at.isoformat()` (logging_.py:99).

### 2c. FULL shape of `write_task_rerun_complete` (logging_.py:205-219)

This is the closest existing analog to a new `write_task_complete`. A new event MUST match/reconcile with this shape:

```python
def write_task_rerun_complete(
    self, phase: int, task_id: str, status: str, turns: int, duration_sec: float
) -> None:
    """Emit a `task_rerun_complete` JSONL event (TDD line 94/95)."""
    self._jsonl(
        {
            "event": "task_rerun_complete",
            "phase": phase,
            "task_id": task_id,
            "status": status,
            "turns": turns,
            "duration_sec": duration_sec,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
```

Exact field schema for `task_rerun_complete`:
| key | type | source/convention |
|-----|------|-------------------|
| `event` | `str` literal | `"task_rerun_complete"` |
| `phase` | `int` | phase number |
| `task_id` | `str` | e.g. `"T07.11"` |
| `status` | `str` | already a string — the **caller** passes `TaskStatus.value` (a string), NOT the enum; the method signature types it as `str`. |
| `turns` | `int` | turns consumed (named `turns`, NOT `turns_consumed` — note divergence from `TaskResult.turns_consumed`) |
| `duration_sec` | `float` | named `duration_sec`, NOT `duration_seconds` |
| `timestamp` | `str` | `datetime.now(timezone.utc).isoformat()` |

**Reconciliation notes for a new `write_task_complete`:**
- The method-signature convention is **scalar primitives, not the result object** — `write_task_rerun_complete` takes `phase, task_id, status: str, turns: int, duration_sec: float` rather than a `TaskResult`. (Contrast `write_phase_result(result: PhaseResult)` at logging_.py:89, which DOES take the object.) Either signature style has precedent; the rerun-family methods all take scalars.
- **`status` is passed as a `str`** (the enum's `.value`), so the caller does `result.status.value`.
- Field-name shortenings (`turns`, `duration_sec`) diverge from the dataclass field names (`turns_consumed`, `duration_seconds`). A new `write_task_complete` should decide consciously whether to match `task_rerun_complete`'s short names (for log-analysis symmetry) or the dataclass names — the existing rerun event uses short names.
- Docstring convention: one line citing the spec/TDD source, e.g. `"""Emit a `task_rerun_complete` JSONL event (TDD line 94/95)."""` (logging_.py:208).

### 2d. Companion start/complete event family (logging_.py:190-243)

The rerun family demonstrates the **start → per-item complete → aggregate complete** triad a per-task execution surface should mirror:
- `write_phase_rerun_start` (190) — opens the batch.
- `write_task_rerun_complete` (205) — one per task.
- `write_phase_rerun_complete` (221) — closes the batch with `tasks_rerun`/`tasks_passed`/`tasks_failed` list fields (all `list(...)`-wrapped, logging_.py:238-240).

Note also `write_phase_interrupt` (logging_.py:71-87) exists specifically *"so the JSONL log has a closing event for every opening phase_start event"* (docstring lines 74-76) — the **balanced open/close invariant** is an explicit design rule. A new per-task start event implies a matching per-task complete (or interrupt) event to preserve this.

---

## 3. Dataclass + serialization pattern (`TaskResult`; template for `HandoffRecord`)

**Source: `src/superclaude/cli/sprint/models.py:165-234`**

### 3a. Dataclass definition (models.py:165-182)

```python
@dataclass
class TaskResult:
    """Outcome of executing a single task subprocess. ..."""
    task: TaskEntry
    status: TaskStatus = TaskStatus.SKIPPED
    turns_consumed: int = 0
    exit_code: int = 0
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    output_bytes: int = 0
    gate_outcome: GateOutcome = GateOutcome.PENDING
    reimbursement_amount: int = 0
    output_path: str = ""
```

Conventions:
- **`@dataclass`** plain (no `frozen`, no `slots`) — matches all sibling models (`TaskEntry` models.py:30, `CheckpointEntry` models.py:370, `Phase` models.py:340).
- **Required field first, no default** (`task: TaskEntry`), then **all others have defaults**.
- **Enum defaults** are enum members: `status: TaskStatus = TaskStatus.SKIPPED`, `gate_outcome: GateOutcome = GateOutcome.PENDING`.
- **datetime defaults** use `field(default_factory=lambda: datetime.now(timezone.utc))` (models.py:177-178) — NOT a bare `datetime.now()` default (which would freeze at import time).
- **Mutable defaults** use `field(default_factory=list)` (see `TaskEntry.dependencies` models.py:40; `CheckpointEntry` uses `Optional[str] = None` for its optional, models.py:399).
- **A class-level docstring stating provenance** — `"Constructed by the runner from subprocess output — not agent self-reported."` (models.py:169). A `HandoffRecord` should similarly state who constructs it and from what.

### 3b. `.to_dict()` — explicit dict literal (models.py:184-210)

```python
def to_dict(self) -> dict:
    """Serialize to a JSON-safe dict (v4.3.0 phase-N-result.json payload). ..."""
    return {
        "task": {
            "task_id": self.task.task_id,
            "title": self.task.title,
            "description": self.task.description,
            "dependencies": list(self.task.dependencies),
            "command": self.task.command,
            "classifier": self.task.classifier,
        },
        "status": self.status.value,
        "turns_consumed": self.turns_consumed,
        "exit_code": self.exit_code,
        "started_at": self.started_at.isoformat(),
        "finished_at": self.finished_at.isoformat(),
        "output_bytes": self.output_bytes,
        "gate_outcome": self.gate_outcome.value,
        "reimbursement_amount": self.reimbursement_amount,
        "output_path": str(self.output_path),
    }
```

Serialization conventions a `HandoffRecord.to_dict()` MUST follow:
- **Hand-written dict literal**, NOT `dataclasses.asdict()`. The docstring (models.py:188-190) explicitly cites *"per checkpoints.py:write_manifest convention"* — i.e., this matches §1b.
- **Enums → `.value`**: `self.status.value`, `self.gate_outcome.value` (models.py:201, 207). Comment at models.py:186: *"Enum fields use `.value` (lowercase string)."*
- **datetimes → `.isoformat()`**: lines 204-205. Comment: *"Datetimes use `.isoformat()` for UTC ISO 8601."*
- **`Path` / path-ish → `str(...)`**: `"output_path": str(self.output_path)` (line 209).
- **Lists defensively copied**: `list(self.task.dependencies)` (line 197).
- **Nested dataclass inlined** as a dict literal (the `"task": {...}` block, lines 193-200) rather than calling a nested `.to_dict()` — note `TaskEntry` has no `to_dict`, so the parent serializes its fields directly.

### 3c. `.from_dict()` round-trip (models.py:212-234)

A matching `@classmethod from_dict(cls, data: dict) -> "TaskResult"` is provided and the `to_dict` docstring promises *"Round-trips via from_dict()"* (models.py:191). Conventions:
- **Enums reconstructed via constructor**: `TaskStatus(data["status"])`, `GateOutcome(data["gate_outcome"])` (models.py:225, 231).
- **datetimes via `datetime.fromisoformat(...)`**: lines 228-229.
- **`.get(key, default)` for optional/back-compat fields** but **`data[key]` for required fields**: nested task uses `task_data.get("description", "")` (line 220) while top-level uses `data["turns_consumed"]` (line 226). The forgiving `.get` is applied to fields most likely to be absent in older payloads.
- A `HandoffRecord` that extends `TaskResult`'s schema should add a matching `from_dict` and keep the round-trip property.

### 3d. Other serialization helpers on the dataclass (models.py:236-259+)
- `@property duration_seconds` (models.py:236-238): `(self.finished_at - self.started_at).total_seconds()`.
- `to_context_summary(self, *, verbose: bool = True) -> str` (models.py:240+): a deterministic-markdown serializer for context injection, with a `verbose` keyword-only flag toggling full vs one-line output. If `HandoffRecord` needs a human/markdown form, follow this `to_context_summary` shape (keyword-only `verbose`, returns markdown).

---

## 4. Click option → SprintConfig field mapping pattern (commands.py `run()`)

**Source: `src/superclaude/cli/sprint/commands.py:72-244`; `config.py:281-363`**

### 4a. Click `@click.option` declaration conventions

From the `run()` decorator stack (commands.py:74-189). A new `--task-parallelism` / `--handoff` flag MUST follow these forms:

- **Typed int option with default + help** (commands.py:88-93, the `--max-turns` template):
  ```python
  @click.option(
      "--max-turns",
      type=int,
      default=100,
      help="Max agent turns per phase (default: 100)",
  )
  ```
  → A `--task-parallelism` int flag should mirror this: `type=int, default=<N>, help="... (default: N)"`. Note the convention of repeating the default in the help text. Some newer options instead use `show_default=True` (see `--startup-stall-timeout`, commands.py:140-146) — both styles are present; `show_default=True` is the cleaner newer form.

- **Boolean flag** (commands.py:153-158, the `--shadow-gates` template):
  ```python
  @click.option(
      "--shadow-gates",
      is_flag=True,
      default=False,
      help="Enable shadow mode: ...",
  )
  ```
  → A `--handoff` boolean flag should use `is_flag=True, default=False, help="..."`.

- **Boolean dual-flag (on/off pair)** (commands.py:439-443, the `rerun_tasks` `--merge-back` template):
  ```python
  @click.option(
      "--merge-back/--no-merge-back",
      default=True,
      help="Merge rerun results back ... (default: enabled).",
  )
  ```
  → If `--handoff` should default ON with an explicit opt-out, use `"--handoff/--no-handoff", default=True`.

- **Choice option** (commands.py:147-152, the `--stall-action` template): `type=click.Choice(["warn", "kill"]), default="warn"`. Use this if a handoff mode needs `off/shadow/soft/full`-style values (mirrors the `Literal[...]` SprintConfig fields, §5).

- **Renaming the Python param** via a second positional string to `@click.option` (commands.py:81-87): `@click.option("--end", "end_phase", ...)` maps CLI `--end` to function param `end_phase`. And `@click.option("--debug", "debug_mode", ...)` (commands.py:126-132) maps `--debug` to `debug_mode`. Use this when the CLI flag name and the function/param name should differ.

### 4b. The `run()` function-signature → `load_sprint_config(...)` → `SprintConfig(...)` chain

Three layers must be threaded in lockstep for any new flag:

1. **`run()` parameter** (commands.py:190-208) — every option becomes a typed positional param in `run(...)`. e.g. `shadow_gates: bool` (line 204), `max_turns: int` (line 194). Optional path overrides typed `Path | None` (lines 206-207).

2. **Pass into `load_sprint_config(...)`** (commands.py:230-244) — keyword args, one per option:
   ```python
   config = load_sprint_config(
       index_path=index_path,
       start_phase=start_phase,
       ...
       shadow_gates=shadow_gates,
       state_dir=state_dir,
   )
   ```
   Note env-var fallback convention: `model=model or os.environ.get("CLAUDE_MODEL", "")` (commands.py:235) and the `state_dir` resolution from `$SPRINT_STATE_DIR` (commands.py:224-228). A new flag with an env fallback follows the `flag or os.environ.get("ENV", default)` shape.

3. **`load_sprint_config` signature + forward to `SprintConfig(...)`** (config.py:281-294 signature; 344-363 construction):
   - Add a kwarg with a default to the `load_sprint_config` signature matching the SprintConfig default (config.py:283-294).
   - Forward it into the `SprintConfig(...)` constructor call (config.py:344-363), e.g. `shadow_gates=shadow_gates` (config.py:360).
   - **Pattern: option default in Click, in `load_sprint_config`, AND in `SprintConfig` field must all agree** (or be intentionally layered). Currently all three repeat the same default (e.g. `max_turns=100` in all three places: commands.py:91, config.py:285, models.py:421).

### 4c. Post-construction override pattern (for fields not threaded through the constructor)

commands.py:246-269 shows the alternate path for late overrides: directly mutate the constructed config via `object.__setattr__(config, "field", value)` (e.g. lines 248, 254-255, 265-268). Used for `tmux_session_name` (line 248, plain assignment since not frozen) and `release_dir`/`work_dir` re-derivation. Most new flags should go through the constructor (§4b); use `object.__setattr__` only for overrides that depend on post-`__post_init__` derived state.

---

## 5. SprintConfig dataclass field-definition pattern

**Source: `src/superclaude/cli/sprint/models.py:406-458` (`SprintConfig`)**

### 5a. Inheritance + class docstring
```python
@dataclass
class SprintConfig(PipelineConfig):
    """Complete configuration for a sprint execution. ..."""
```
- Inherits from `PipelineConfig` (models.py:407) — shared fields (`work_dir`, `dry_run`, `max_turns`, `model`, `permission_flag`, `debug`) live on the base; sprint-specific fields are added here (docstring models.py:410-413). A new field goes on `SprintConfig` unless it is genuinely cross-pipeline.

### 5b. Field-definition conventions (models.py:416-458)

| Field-type | Idiom | Example (file:line) |
|---|---|---|
| `Path` with default | `field(default_factory=lambda: Path("."))` | `index_path` (416), `release_dir` (417) |
| `list[...]` | `field(default_factory=list)` | `phases` (418) |
| `int` scalar | bare default | `start_phase: int = 1` (419), `max_turns: int = 100` (421) |
| `str` | bare default, often `""` meaning "use default" | `model: str = ""  # empty = claude default` (422) |
| `bool` | bare default | `dry_run: bool = False` (423), `shadow_gates: bool = False` (433) |
| **bounded string set** | `Literal["off","shadow","soft","full"]` with default | `wiring_gate_mode: Literal[...] = "soft"` (436); `gate_rollout_mode` (440); `checkpoint_gate_mode` (451) |
| sentinel `Path` | `field(default_factory=lambda: Path(""))` (empty-Path sentinel, distinct from `Path(".")`) | `state_dir` (458) |

Conventions to follow for new fields:
- **Every field has a default** (SprintConfig is constructed positionally-by-keyword everywhere; no required fields).
- **Inline `#` comments document semantics**, especially the meaning of sentinel/zero values: `end_phase: int = 0  # 0 = auto-detect (last phase)` (420); `stall_timeout: int = 0  # 0 = disabled` (428).
- **Gate-mode-style fields use `Literal[...]`** with `off/shadow/soft/full` semantics and a comment block enumerating each value's behavior (models.py:434-436, 451). A new `--handoff`-mode field with graduated behavior should use this exact `Literal` + comment-block idiom — and the matching Click option should be `click.Choice([...])` (§4a).
- **A module-level sentinel constant** convention exists: `SHADOW_GRACE_INFINITE: int = 999_999` (models.py:403) for "magic" thresholds, referenced in `__post_init__`.

### 5c. Derived fields go in `__post_init__`, paths go in `@property`
- **`__post_init__`** (models.py:474-530): used for migration shims, cross-field derivation (`wiring_gate_mode` derived from `wiring_gate_enabled`/`wiring_gate_grace_period`, lines 514-520), and sentinel→default resolution (`state_dir`, lines 525-530). Mutation inside `__post_init__` uses `object.__setattr__(self, "field", value)` (e.g. line 479, 518) — the codebase uses this even though the dataclass is not frozen, for consistency.
- **Path accessors are `@property`, not fields** (models.py:532-571): `results_dir`, `execution_log_jsonl`, `execution_log_md`, plus parametrized path-builders `output_file(phase)`, `task_output_file(phase, task)` (561-562), `phase_result_json(phase)` (570-571). A new handoff-file path should be a `@property` (or a `def handoff_file(self, ...)` builder) on `SprintConfig`, NOT a stored field — matching `phase_result_json` (570-571) and `task_output_file` (561-562):
  ```python
  def phase_result_json(self, phase: Phase) -> Path:
      return self.results_dir / f"phase-{phase.number}-result.json"
  def task_output_file(self, phase: Phase, task: "TaskEntry") -> Path:
      return self.results_dir / f"phase-{phase.number}-task-{task.task_id}-output.txt"
  ```

---

## Summary — patterns the implementation MUST follow

1. **Atomic state writes** (`FileHandoffStore`): `parent.mkdir(parents=True, exist_ok=True)` → `tmp = path.with_suffix(path.suffix + ".tmp")` → `tmp.write_text(json.dumps(payload, indent=2) + "\n")` → `tmp.replace(path)`. Reserve atomic write for JSON state; plain `write_text` for markdown bodies. (checkpoints.py:207-210)
2. **JSONL events**: append-mode, `json.dumps(data, default=str) + "\n"`, dict with `"event"` first key + trailing `"timestamp": datetime.now(timezone.utc).isoformat()`, lists `list(...)`-wrapped, enums `.value`, datetimes `.isoformat()`. New `write_task_complete` should mirror `write_task_rerun_complete`'s scalar signature (`phase, task_id, status: str, turns, duration_sec`) and preserve the balanced start/complete-event invariant. (logging_.py:205-219, 265-267)
3. **Dataclass + serialization** (`HandoffRecord`): plain `@dataclass`, required field first then all-defaulted, enum defaults as members, datetime defaults via `field(default_factory=lambda: datetime.now(timezone.utc))`, mutables via `field(default_factory=list)`. Hand-written `to_dict()` (NOT `asdict`) with enums→`.value`, datetimes→`.isoformat()`, paths→`str()`; matching `from_dict` classmethod using `Enum(data[k])` / `datetime.fromisoformat(...)` and `.get(k, default)` for back-compat fields. (models.py:165-234)
4. **Click flags**: int→`type=int, default=N, help` (prefer `show_default=True`); bool→`is_flag=True, default=False`; dual→`"--x/--no-x", default=True`; graduated mode→`click.Choice([...])`. Thread the flag through three layers in lockstep: `run()` param → `load_sprint_config(...)` kwarg → `SprintConfig(...)` constructor arg, with defaults agreeing across all three. (commands.py:88-158, 190-244; config.py:281-363)
5. **SprintConfig fields**: every field defaulted; `Path`→`field(default_factory=lambda: Path("."))`; list→`field(default_factory=list)`; graduated mode→`Literal["off","shadow","soft","full"]` + comment block; document sentinel/zero meanings inline. Derived values in `__post_init__` via `object.__setattr__`; file paths as `@property`/builder methods (e.g. `handoff_file`), not stored fields. (models.py:406-571)

**Status: Complete**
