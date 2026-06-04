# Research 02: Patterns & Conventions

**Status:** Complete
**Researcher:** researcher-2
**Scope:** Extract canonical conventions from `checkpoints.py`, `commands.py`, `models.py`, `executor.py` that `recovery.py` and `rerun_tasks.py` MUST mirror.
**Date:** 2026-06-01

---

## 1. Canonical Module: `checkpoints.py` (408 LOC)

**Path:** `src/superclaude/cli/sprint/checkpoints.py`

### 1.1 Module-level conventions

| Convention | Evidence | Rule |
|---|---|---|
| Module docstring purpose-block | `checkpoints.py:1-7` | First line ends with em-dash phrase; multi-line description explains who consumes it and why the module exists |
| `from __future__ import annotations` | `checkpoints.py:9` | MANDATORY — first import after docstring |
| Stdlib imports grouped | `checkpoints.py:11-14` | `json`, `re`, `datetime`, `pathlib` ordered alphabetically by module |
| Sibling-module imports use relative dot | `checkpoints.py:16` | `from .models import CheckpointEntry` — never `from superclaude.cli.sprint.models` for in-package siblings |
| Module-level constants typed | `checkpoints.py:22-25, 30-33` | `re.Pattern[str]` explicit type annotation on compiled regex constants; UPPER_SNAKE_CASE names |
| Section separator banner | `checkpoints.py:129-131` | `# ---...---\n# Wave 3 — manifest + auto-recovery\n# ---...---\n` (79-char dash rule, surrounded by blank lines) — used to split logical groups within a module |

### 1.2 Public function signature pattern

Public functions are **lowercase_with_underscores**, declared at top-level (no class wrapper for simple stateless ops).

**Signature style (`checkpoints.py:36-39, 97-99, 134-137, 169, 209-213`):**

```python
def extract_checkpoint_paths(
    phase_file: Path,
    release_dir: Path,
) -> list[tuple[str, Path]]:
```

- One parameter per line when >1 param OR >80-char signature.
- Modern generics: `list[...]`, `tuple[...]`, `dict[...]` — NEVER `List`, `Tuple`, `Dict` from `typing` (only `Optional`/`Literal` from typing are used — see `models.py:15`).
- Return type annotation always present.
- Keyword-only arguments separated with `*` — see `_render_recovered_checkpoint(*, entry, verification_block, evidence)` at `checkpoints.py:367-372`.

### 1.3 Docstring style

| Element | Evidence | Rule |
|---|---|---|
| First line: 1-sentence imperative | `checkpoints.py:40, 100, 138, 170, 210` | "Return X.", "Walk every Y and return Z.", "Serialise the manifest to JSON at `output_path`." |
| Blank line then paragraph(s) | All docstrings | Multi-paragraph allowed; explain behavior, not parameters in formal sections |
| Args/Returns style: **PROSE, not Google-style** | `checkpoints.py:40-51, 138-145` | Parameters and return semantics described in flowing prose. Only `models.py` uses formal `Attributes:` for dataclasses (see `models.py:320-332`) |
| Cross-refs via Sphinx `:func:` / `:class:` | `checkpoints.py:101, 142, 315-317` | `:func:\`extract_checkpoint_paths\``, `:class:\`CheckpointEntry\`` |
| Edge cases stated explicitly | `checkpoints.py:50-51, 144-145` | "Returns an empty list if X..." pattern |

### 1.4 Private helper conventions

- Single leading underscore: `_nearest_heading`, `_extract_verification_block`, `_discover_phase_artifacts`, `_render_recovered_checkpoint` (`checkpoints.py:115, 293, 334, 367`).
- Placed AFTER the public functions they support (not before).
- Same docstring style as public, but may be terser.
- Pure helpers — no global state mutation.

### 1.5 Error handling style

| Pattern | Evidence | Rule |
|---|---|---|
| File I/O guarded by `try / except OSError: return []` | `checkpoints.py:52-55, 107-110, 301-304, 362-363` | Read failures degrade to empty-result, NEVER raise from a parse helper |
| Broad `except Exception: # noqa: BLE001` ONLY when crossing module boundaries | `checkpoints.py:152` | `discover_phases` call wrapped with `noqa: BLE001` to suppress lint; pattern reused in commands.py:403 |
| No custom exception classes for parse/IO failures — return empty/None | All of checkpoints.py | New `recovery.py` should follow this — do NOT introduce a `RerunTasksError` for I/O |

### 1.6 File I/O patterns

| Pattern | Evidence | Convention |
|---|---|---|
| Path objects throughout (never `str` for paths in signatures) | `checkpoints.py:36-39, 97-99, 134-137` | All path params typed as `Path` |
| Read with `errors="replace"` | `checkpoints.py:53, 302, 360` | `path.read_text(errors="replace")` to survive encoding glitches |
| Atomic writes via `.tmp` + `.replace()` | `checkpoints.py:203-206` | `output_path.parent.mkdir(parents=True, exist_ok=True); tmp = output_path.with_suffix(output_path.suffix + ".tmp"); tmp.write_text(...); tmp.replace(output_path)` — MUST replicate for any manifest writes in recovery.py |
| `.mkdir(parents=True, exist_ok=True)` before writing | `checkpoints.py:203, 265` | Always defensive — never assume parent exists |
| Trailing newline on JSON output | `checkpoints.py:205` | `json.dumps(payload, indent=2) + "\n"` |
| UTC timestamps | `checkpoints.py:183, 374` | `datetime.now(timezone.utc).isoformat()` — NEVER naive datetime |

### 1.7 Lazy/local imports to avoid cycles

`checkpoints.py:146-148`:

```python
# Local import: ``config`` imports from this module path indirectly via
# ``models`` → avoid cycles at module import time.
from .config import discover_phases
```

The new `recovery.py` and `rerun_tasks.py` MUST do the same — heavy CLI deps (`executor`, `commands`) imported locally inside the functions that need them, with the cycle-avoidance comment explaining why.

### 1.8 Mutation discipline

`recover_missing_checkpoints` (`checkpoints.py:209-290`) returns a NEW list, never mutates input. Docstring explicitly says so (`checkpoints.py:228-230`: "Returns a NEW list — the input `manifest` is not mutated."). New rerun-task functions producing modified state MUST follow.

### 1.9 Idempotency guarantee

`checkpoints.py:227-230` documents idempotency in plain English: "if the expected file already exists on disk... the entry is returned unchanged." The first action in the loop body (`checkpoints.py:237-249`) re-checks `.is_file()` to absorb intra-loop file writes. **rerun-tasks idempotency MUST be expressed and implemented identically.**

---

## 2. Click subcommand conventions: `commands.py` verify-checkpoints

**Path:** `src/superclaude/cli/sprint/commands.py:360-449`

### 2.1 Subcommand decorator pattern

`commands.py:360-376`:

```python
@sprint_group.command("verify-checkpoints")
@click.argument(
    "output_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option(
    "--recover",
    is_flag=True,
    help="Auto-generate missing checkpoint reports from evidence artifacts.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Emit the manifest as machine-readable JSON instead of a table.",
)
def verify_checkpoints(output_dir: Path, recover: bool, as_json: bool):
```

| Rule | Evidence |
|---|---|
| Command name override when func name differs from kebab CLI name | `@sprint_group.command("verify-checkpoints")` then `def verify_checkpoints` |
| `click.argument` for required positional, `click.option` for flags | `commands.py:361-364` (positional) vs `365-374` (flags) |
| `path_type=Path` on every path argument/option | `commands.py:363, 178, 185` |
| `exists=True, file_okay=False` for directory-only paths | `commands.py:362-363` |
| `is_flag=True` on boolean options (default `False` implicit) | `commands.py:367, 373` |
| Second-arg override when CLI flag clashes with Python reserved word | `--json` mapped to `as_json` (`commands.py:371-372`) |
| Help string ends with period | All `help=` strings in the file |
| Type-hinted function params | `commands.py:376` |

### 2.2 Command body conventions

`commands.py:386-415`:

```python
from .checkpoints import (
    build_manifest,
    recover_missing_checkpoints,
    write_manifest,
)
from .config import discover_phases

index_path = output_dir / "tasklist-index.md"
if not index_path.is_file():
    raise click.ClickException(f"No tasklist-index.md found in {output_dir}")
```

| Rule | Evidence |
|---|---|
| Imports LOCAL (inside function body), grouped at top | `commands.py:386-391` — pattern is universal in this file (see also `run`, `attach`, `status`, `kill`) |
| Preflight check raises `click.ClickException(msg)` | `commands.py:394-395`; also `commands.py:403-404` (`raise click.ClickException(f"Phase discovery failed: {exc}") from exc`) |
| Exception chaining with `from exc` | `commands.py:404` |
| Output via `click.echo(...)` — never `print()` | `commands.py:412, 426-448` |
| Error output to stderr with `err=True` | `commands.py:274, 278` |
| Process exit via `raise SystemExit(N)`, NEVER `sys.exit(N)` | `commands.py:275` |

### 2.3 Helper presentation function

`commands.py:418-449` defines `_print_checkpoint_table(manifest: list, manifest_path: Path) -> None`.

| Rule | Evidence |
|---|---|
| Private (underscore-prefixed) presentation helpers live BELOW the command function in the same file | `commands.py:418, 452` |
| Empty-state branch first | `commands.py:425-428` |
| Summary line → blank `click.echo()` → header row → ASCII separator `"-" * 80` → rows → blank → tail | `commands.py:430-449` |
| Column widths fixed: `f"{'Phase':>5}  {'Status':<11}  {'Name':<30}  Path"` | `commands.py:437` |

### 2.4 Docstring style for Click commands

`commands.py:377-385`:

```
"""Verify (and optionally recover) checkpoint reports for a sprint.

OUTPUT_DIR is a sprint release directory — the one that contains
`tasklist-index.md`, per-phase tasklists, and the `checkpoints/`
subtree. The command parses every phase tasklist, checks whether each
declared `Checkpoint Report Path:` file exists on disk, and prints a
status table (or JSON with --json). Pass --recover to regenerate
missing reports from evidence artifacts under `artifacts/`.
"""
```

- First line: one-sentence purpose.
- Then ALL CAPS positional arg names referenced (Click renders these in `--help`).
- Then prose explaining behavior + flag interactions.
- No formal Args/Returns sections (Click handles those via `--help`).

---

## 3. `models.py` dataclass + enum conventions

**Path:** `src/superclaude/cli/sprint/models.py`

### 3.1 Module setup

`models.py:1-21`:

- Module docstring identifies role (`"Sprint data models — enums, dataclasses, and pure-data types."`).
- `from __future__ import annotations` (line 8).
- Imports ordered: stdlib (`time`, `dataclasses`, `datetime`, `enum`, `pathlib`, `typing`) → `superclaude.cli.pipeline.models` (cross-package abs import) — NOT relative because it's a parent-package import.
- `typing` imports limited to `Literal, Optional` only. Everything else uses PEP 585 builtins.

### 3.2 `@dataclass` convention

`models.py:24-36, 158-176, 281-308, 311-340, 512-520, 522-555, 558-619`:

```python
@dataclass
class TaskEntry:
    """A single task parsed from a phase tasklist markdown file.

    Represents one ``### T<PP>.<TT> -- Title`` block with its metadata.
    """

    task_id: str
    title: str
    description: str = ""
    dependencies: list[str] = field(default_factory=list)
    command: str = ""
    classifier: str = ""
```

| Rule | Evidence |
|---|---|
| `@dataclass` bare (no `frozen=True` by default) | `models.py:24, 158, 281, 311, 512, 522, 558` |
| Class docstring: 1-sentence purpose + optional clarifying paragraph | `models.py:26-29, 159-164` |
| Required fields first, defaulted last | All dataclasses |
| Mutable defaults via `field(default_factory=...)` — NEVER `[]` or `{}` literal | `models.py:34, 170, 171, 530, 533, 563, 565` |
| Lambda factory for `datetime.now(timezone.utc)` | `models.py:170-171, 533-534, 565` — `field(default_factory=lambda: datetime.now(timezone.utc))` |
| `Optional[X]` from typing (NOT `X \| None`) | `models.py:340, 566, 567` — established convention; recovery.py MUST follow |
| Properties for derived/display values | `models.py:177-179, 297-308, 546-555, 569-619` |
| `Attributes:` block in docstring when fields warrant explanation | `models.py:320-332` (CheckpointEntry) |

### 3.3 Enum convention

`models.py:39-53, 56-..., 211-269, 272-278`:

```python
class TaskStatus(Enum):
    """Outcome status for a single task within a phase."""

    PASS = "pass"
    FAIL = "fail"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"

    @property
    def is_success(self) -> bool:
        return self == TaskStatus.PASS

    @property
    def is_failure(self) -> bool:
        return self in (TaskStatus.FAIL, TaskStatus.INCOMPLETE)
```

| Rule | Evidence |
|---|---|
| `class XxxStatus(Enum):` — singular noun + `Status`/`Outcome`/`State` suffix | `TaskStatus`, `GateOutcome`, `PhaseStatus`, `SprintOutcome`, `GateDisplayState` |
| Members UPPER_SNAKE_CASE, string values lower_snake_case | All enums |
| Predicate properties grouped at bottom of class | `models.py:47-53, 235-269` — `is_success`, `is_failure`, `is_terminal` |
| Multi-value membership via tuple in `in` | `models.py:53, 237-249, 253-260` — `return self in (X, Y, Z)` |
| Inline comments above values that need explanation | `models.py:219, 220-222, 223-227` |

### 3.4 Dataclass inheritance pattern

`models.py:512-520` (SprintStep extends pipeline.Step) and `models.py:522-555` (PhaseResult extends pipeline.StepResult):

```python
@dataclass
class PhaseResult(StepResult):
    """Outcome of executing a single phase.

    Inherits from pipeline.StepResult for shared timing fields.
    Sprint-specific fields (phase, exit_code, etc.) are defined here.
    """

    phase: Phase = field(default_factory=lambda: Phase(number=0, file=Path(".")))
    status: PhaseStatus = PhaseStatus.PENDING
    ...
```

| Rule | Evidence |
|---|---|
| Inheriting dataclasses still use `@dataclass` decorator | `models.py:512, 522` |
| Docstring explicitly calls out inheritance and what's added | `models.py:524-528` |
| ALL fields in subclass need defaults (Python dataclass inheritance rule) — uses sentinel `default_factory=lambda: Phase(number=0, file=Path("."))` for required-but-defaulted fields | `models.py:530` |

---

## 4. `executor.py` hook insertion conventions

**Path:** `src/superclaude/cli/sprint/executor.py`

### 4.1 Hook function signature

`executor.py:748-754`:

```python
def run_post_phase_wiring_hook(
    phase: Phase,
    config: SprintConfig,
    phase_result: PhaseResult,
    ledger: TurnLedger | None = None,
    remediation_log: DeferredRemediationLog | None = None,
) -> PhaseResult:
    """Run post-phase wiring analysis by delegating to the per-task hook.
    ...
    """
```

| Convention | Evidence | Rule |
|---|---|---|
| Hook fn name pattern `run_post_<scope>_<purpose>_hook` | `run_post_phase_wiring_hook`, `run_post_task_wiring_hook`, `run_post_task_anti_instinct_hook` (`executor.py:748, 803`) | New rerun-tasks hook would be `run_post_phase_rerun_tasks_hook` if needed, OR an inline call from the phase loop |
| Required params first (Phase, SprintConfig, PhaseResult), optional state-carrying params last with `None` default and `X \| None` type | `executor.py:752-753` | NOTE: executor.py DOES use `X \| None` style for OPTIONAL params (in contrast to models.py which uses `Optional[X]`). The split: dataclass fields → `Optional[X]`; function/method signatures → `X \| None`. |
| Returns the (possibly mutated) `PhaseResult` | `executor.py:754, 800` | Pattern: take + return PhaseResult so call sites can rebind |

### 4.2 Hook call-site pattern in the phase loop

There are TWO insertion points — one per phase execution mode. Both look identical:

**Per-task mode (executor.py:1289-1295):**

```python
# v3.2-T02: Run post-phase wiring hook for per-task phases too
phase_result = run_post_phase_wiring_hook(
    phase,
    config,
    phase_result,
    ledger=ledger,
    remediation_log=remediation_log,
)
```

**Claude-mode (executor.py:1568-1574):**

```python
# v3.2-T02: Run post-phase wiring hook for every claude-mode phase
phase_result = run_post_phase_wiring_hook(
    phase,
    config,
    phase_result,
    ledger=ledger,
    remediation_log=remediation_log,
)
```

| Convention | Evidence | Rule |
|---|---|---|
| Leading comment cites the spec/ticket id (e.g. `# v3.2-T02:`) explaining WHY the hook fires here | `executor.py:1288, 1567` | New rerun-tasks hook MUST be tagged with its task id (e.g. `# v4.3.0-Tnn: ...`) |
| Hook call IMMEDIATELY after `PhaseResult` construction (line ~1280, 1550) and BEFORE `sprint_result.phase_results.append(phase_result)` (line 1297, 1576) | `executor.py:1280-1297, 1545-1576` | The new rerun-tasks insertion MUST follow the same ordering: build PhaseResult → mutate via hook → append → log → notify |
| Re-bind to same variable name (`phase_result = run_post_...(...)`) | `executor.py:1289, 1568` | Never store the return in a new variable |
| Hooks chain — multiple hooks may fire in sequence between construction and append | `executor.py:1289-1295` (wiring) then potentially `_summary_worker.submit` at `executor.py:1584-1592` | The rerun-tasks hook should slot into the same window |

### 4.3 Exception isolation around side-effect calls

`executor.py:1584-1592`:

```python
try:
    _summary_worker.submit(phase, phase_result)
except Exception as _sw_exc:  # noqa: BLE001 - must not abort
    debug_log(
        _dbg,
        "summary_worker_submit_error",
        phase=phase.number,
        error=str(_sw_exc),
    )
```

- Side-effect hooks that "must not abort the loop" wrap in broad-except + `debug_log` event.
- `noqa: BLE001` comment includes the reason ("must not abort").
- Event name is snake_case verbose (`summary_worker_submit_error`).

### 4.4 Logging conventions

`executor.py:43-48`:

```python
_wiring_logger = _logging.getLogger("superclaude.sprint.wiring_hook")
_anti_instinct_logger = _logging.getLogger("superclaude.sprint.anti_instinct_hook")
_checkpoint_logger = _logging.getLogger("superclaude.sprint.checkpoint")

# Debug logger name for executor-specific events
_DBG_NAME = "superclaude.sprint.debug.executor"
```

| Rule | Evidence |
|---|---|
| Logger names: `"superclaude.sprint.<hook_name>"` | `executor.py:43-45` |
| Module-private loggers prefixed `_` | `executor.py:43-45` |
| `import logging as _logging` to keep namespace clean | `executor.py:5` |
| Structured debug events via `debug_log(logger, "event_name", k=v, k=v)` | `executor.py:1587-1591, 1594-1601, 1622-1628` |
| Event names: snake_case past-tense or noun (`phase_complete`, `diagnostic_report`) | `executor.py:1596, 1624` |

---

## 5. Test naming patterns

**Path:** `tests/sprint/test_checkpoints.py`

| Convention | Evidence |
|---|---|
| Test file per source module: `test_<module>.py` | `tests/sprint/test_checkpoints.py` mirrors `src/superclaude/cli/sprint/checkpoints.py` |
| Class-per-public-function grouping: `class TestExtractCheckpointPaths` | `test_checkpoints.py:42` |
| Test methods snake_case, scenario-named: `test_zero_checkpoints`, `test_single_checkpoint_backticks`, `test_two_checkpoints_mixed_formats` | `test_checkpoints.py:43, 47, 60` |
| `tmp_path: Path` fixture for filesystem tests | `test_checkpoints.py:43, 47, 60` |
| Section banner separators inside test files | `test_checkpoints.py:37-39` |
| Imports from `superclaude.cli.sprint.X` (absolute, NOT relative) | `test_checkpoints.py:20-35` |
| Click subcommand tests use `from click.testing import CliRunner` | `test_checkpoints.py:18` |

For `tests/sprint/test_rerun_tasks.py` (new), structure MUST be: one `Test<PublicFunction>` class per public function in `rerun_tasks.py`, plus a `TestRerunTasksCommand` class for the Click subcommand using `CliRunner`.

---

## 6. Mirroring Summary — what new code MUST look like

### 6.1 What `recovery.py` MUST mirror (from `checkpoints.py`)

1. **Module docstring** — em-dash subtitle + multi-paragraph "who uses this and why".
2. **`from __future__ import annotations`** as first import.
3. **Imports** stdlib → relative `.models`, `.config` (lazy when cycle risk).
4. **`re.Pattern[str]` typed module constants** for any regex matchers.
5. **Public function shape**: `def func_name(arg1: Path, arg2: Path) -> list[tuple[...]]:` — one param per line when multi-arg.
6. **Docstring prose style** — first sentence imperative, edge cases explicit, `:func:` cross-refs.
7. **Private helpers** with `_` prefix, defined BELOW the public functions they support.
8. **File I/O**: `try/except OSError: return []`; `path.read_text(errors="replace")`.
9. **Atomic writes**: `tmp = path.with_suffix(path.suffix + ".tmp"); tmp.write_text(...); tmp.replace(path)`.
10. **`mkdir(parents=True, exist_ok=True)`** before writes.
11. **UTC timestamps** via `datetime.now(timezone.utc).isoformat()`.
12. **Idempotency** — re-check `.is_file()` inside the loop body; document "Returns a NEW list — input not mutated."
13. **Section banners** when the module has multiple logical groups.

### 6.2 What `rerun_tasks.py` MUST mirror

Same as 6.1, PLUS:

1. **Build-manifest pattern** like `checkpoints.build_manifest` — walk phases via `discover_phases`, return list of dataclass entries.
2. **Write-manifest pattern** like `checkpoints.write_manifest` — `{"generated_at", "summary": {...}, "entries": [...]}` JSON shape, atomic write.
3. **Recover pattern** like `checkpoints.recover_missing_checkpoints` — pure function, input untouched, idempotent, refresh check inside loop.
4. **Render helper** like `_render_recovered_checkpoint(*, entry, verification_block, evidence) -> str` — keyword-only params, returns formatted markdown.
5. **Dataclass for entries** added in `models.py` following CheckpointEntry shape (`models.py:311-340`): `phase: int`, `name: str`, `expected_path: Path`, `exists: bool`, optional metadata fields with `Optional[str]` defaults — full `Attributes:` docstring block.

### 6.3 What `commands.py` edits MUST mirror

1. **Decorator stack**: `@sprint_group.command("kebab-name")` → `@click.argument(...)` → `@click.option(...)` ×N → `def func(...)`.
2. **`type=click.Path(exists=True, file_okay=False, path_type=Path)`** for directory args.
3. **`is_flag=True`** for boolean toggles; provide second positional arg to rename when Python-name differs from CLI-name (`--json` → `as_json`).
4. **Help strings end with period**; explain effect, not just name.
5. **Function body**: local imports first, preflight checks raise `click.ClickException(f"...{output_dir}")`, output via `click.echo`.
6. **Exception chaining** with `from exc` when re-raising a wrapped error.
7. **Process exit**: `raise SystemExit(N)` — never `sys.exit`.
8. **Presentation helper** `_print_<thing>_table(manifest: list, manifest_path: Path) -> None` defined directly below the command function.
9. **Table format**: summary line → blank → header → `"-" * 80` → rows → blank → manifest path tail.
10. **Click docstring**: first-line purpose; ALL CAPS positional refs; flag-interaction prose; NO formal Args/Returns.

### 6.4 What `executor.py` hook-insertion edits MUST mirror

1. **Hook function name**: `run_post_<scope>_<purpose>_hook`.
2. **Signature**: required params (`Phase, SprintConfig, PhaseResult`) first; optional state carriers (`ledger`, `remediation_log`, etc.) as `X | None = None` last.
3. **Returns `PhaseResult`** — caller re-binds.
4. **Insertion point**: BETWEEN `PhaseResult(...)` construction and `sprint_result.phase_results.append(phase_result)` — at BOTH per-task (~line 1289) and claude-mode (~line 1568) sites.
5. **Leading comment**: `# v4.3.0-T<id>: Run post-phase rerun-tasks hook for ...`
6. **Side-effect calls that must not abort**: wrap in `try / except Exception as _exc: # noqa: BLE001 - must not abort` + `debug_log(_dbg, "rerun_tasks_<event>_error", phase=phase.number, error=str(_exc))`.
7. **Logger**: `_rerun_tasks_logger = _logging.getLogger("superclaude.sprint.rerun_tasks")` declared in the module-private logger block (`executor.py:43-48`).

### 6.5 Naming conventions ledger

| Element | Pattern | Source |
|---|---|---|
| Module file | snake_case noun (`checkpoints.py`, `executor.py`) | sprint/ |
| Public function | snake_case verb (`extract_checkpoint_paths`, `build_manifest`) | checkpoints.py |
| Private helper | `_snake_case_verb` | checkpoints.py:115, 293 |
| Dataclass | PascalCase noun (`CheckpointEntry`, `PhaseResult`) | models.py |
| Enum | PascalCase noun + suffix (`TaskStatus`, `GateOutcome`) | models.py:39, 56 |
| Enum member | UPPER_SNAKE_CASE; value lowercase string | models.py:42-45 |
| Constant | UPPER_SNAKE_CASE typed: `NAME: type = ...` | checkpoints.py:22, models.py:344 |
| Module logger | `_<purpose>_logger = _logging.getLogger("superclaude.sprint.<purpose>")` | executor.py:43-45 |
| Debug event name | snake_case noun (`phase_complete`, `diagnostic_report`) | executor.py:1596, 1624 |
| Click CLI name | kebab-case (`verify-checkpoints`, `rerun-tasks`) | commands.py:360 |
| Click Python fn | snake_case mirroring CLI | commands.py:376 |
| Test file | `test_<module>.py` | tests/sprint/ |
| Test class | `Test<PublicFunctionOrClass>` | test_checkpoints.py:42 |
| Test method | `test_<scenario_in_words>` | test_checkpoints.py:43 |

---

## 7. Anti-patterns to AVOID (observed-by-absence)

These do NOT appear in the canonical modules — new code must NOT introduce them:

- `print(...)` in CLI command bodies → use `click.echo`.
- `sys.exit(N)` → use `raise SystemExit(N)` or `raise click.ClickException(...)`.
- `os.path` functions → use `pathlib.Path` exclusively.
- `typing.List/Dict/Tuple/Set` → use PEP 585 builtins.
- Raw string paths in function signatures → always `Path`.
- Mutable default args (`= []`, `= {}`) → always `field(default_factory=...)` for dataclasses, immutable defaults for functions.
- Custom exception classes for parse/IO → return empty/None or raise `click.ClickException`.
- `datetime.now()` (naive) → always `datetime.now(timezone.utc)`.
- Bare `except:` → always `except <Specific>:` or `except Exception: # noqa: BLE001 - <reason>`.
- Module-level mutable state.
- Class wrappers around stateless helper functions.
