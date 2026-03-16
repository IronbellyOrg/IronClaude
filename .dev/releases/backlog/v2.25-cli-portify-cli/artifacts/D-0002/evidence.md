# D-0002 — Framework Base Type Import Stability Evidence

**Produced by**: T01.02
**Sprint**: v2.25-cli-portify-cli
**Date**: 2026-03-16

---

## Import Verification Results

### Command 1: Pipeline models

```
$ uv run python -c "from superclaude.cli.pipeline.models import PipelineConfig, Step, StepResult, GateCriteria, GateMode, SemanticCheck; print('OK')"
OK
```

**Exit code**: 0 — PASS

### Command 2: ClaudeProcess

```
$ uv run python -c "from superclaude.cli.pipeline.process import ClaudeProcess; print('OK')"
OK
```

**Exit code**: 0 — PASS

---

## Confirmed Import Paths

| Type | Module | Status |
|------|--------|--------|
| `PipelineConfig` | `superclaude.cli.pipeline.models` | CONFIRMED |
| `Step` | `superclaude.cli.pipeline.models` | CONFIRMED |
| `StepResult` | `superclaude.cli.pipeline.models` | CONFIRMED |
| `GateCriteria` | `superclaude.cli.pipeline.models` | CONFIRMED |
| `GateMode` | `superclaude.cli.pipeline.models` | CONFIRMED |
| `SemanticCheck` | `superclaude.cli.pipeline.models` | CONFIRMED |
| `ClaudeProcess` | `superclaude.cli.pipeline.process` | CONFIRMED |

**Note**: `GateCriteria`, `GateMode`, and `SemanticCheck` live in `superclaude.cli.pipeline.models`, NOT in `superclaude.cli.sprint.models`. Confirmed per oq-resolutions.md (D-008).

---

## API Interface Contract (Key Fields and Signatures)

### PipelineConfig (dataclass)
```python
work_dir: Path = Path(".")
dry_run: bool = False
max_turns: int = 100
model: str = ""
permission_flag: str = "--dangerously-skip-permissions"
debug: bool = False
grace_period: int = 0
```

### Step (dataclass)
```python
id: str
prompt: str
output_file: Path
gate: Optional[GateCriteria]
timeout_seconds: int
inputs: list[Path] = []
retry_limit: int = 1
model: str = ""
gate_mode: GateMode = GateMode.BLOCKING
```

### StepResult (dataclass)
```python
step: Optional[Step] = None
status: StepStatus = StepStatus.PENDING
attempt: int = 1
gate_failure_reason: str | None = None
started_at: datetime
finished_at: datetime
# property: duration_seconds -> float
```

### GateCriteria (dataclass)
```python
required_frontmatter_fields: list[str]
min_lines: int
enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
semantic_checks: list[SemanticCheck] | None = None
```

### GateMode (Enum)
```python
BLOCKING = "BLOCKING"   # step must pass before next step begins
TRAILING = "TRAILING"   # step does not block subsequent steps
```

### SemanticCheck (dataclass)
```python
name: str
check_fn: Callable[[str], bool]
failure_message: str
```

### ClaudeProcess
- Constructor kwargs: `prompt`, `output_file`, `error_file`, `max_turns`, `model`, `permission_flag`, `timeout_seconds`, `output_format`, `extra_args`, `on_spawn`, `on_signal`, `on_exit`, `env_vars`
- `build_command() -> list[str]` — includes `["--tools", "default"]` (lines 79-80 of process.py)
- `start() -> subprocess.Popen`
- `wait() -> int` (respects timeout_seconds)
- `terminate()` — SIGTERM → 10s wait → SIGKILL

---

## --tools default Inheritance Chain

```
ClaudeProcess.build_command()
  → cmd = ["claude", "--print", "--verbose", permission_flag,
           "--no-session-persistence", "--tools", "default",
           "--max-turns", str(max_turns), "--output-format", output_format,
           "-p", prompt]
       ↑ called via super().build_command()
PortifyProcess.build_command()
  → extends result of super() with portify-specific args
```

`PortifyProcess` inherits `--tools default` for free via `super()`. No additional implementation needed per oq-resolutions.md (--tools default / FIX-001).

---

## Stability Assessment

All 7 types confirmed importable as of 2026-03-16. NFR-007 ensures `pipeline.models` and `pipeline.process` have zero imports from `sprint/` or `roadmap/`, making them stable base types for `cli_portify/`.

**Pre-confirmed by**: oq-resolutions.md D-008 (2026-03-16 cross-release conflict analysis)
