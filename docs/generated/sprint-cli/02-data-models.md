---
title: Sprint CLI - Data Models & Type System
generated: 2026-04-03
scope: cli/pipeline/models.py, cli/sprint/models.py, cli/roadmap/models.py
---

# Data Models & Type System

## Model Inheritance Hierarchy

```
PipelineConfig (pipeline/models.py:169)
  +-> SprintConfig (sprint/models.py:297)
  +-> RoadmapConfig (roadmap/models.py:95)
  +-> ValidateConfig (roadmap/models.py:120)
  +-> TasklistValidateConfig (tasklist/models.py)
  +-> CleanupAuditConfig (cleanup_audit/models.py)

Step (pipeline/models.py:77)
  +-> SprintStep (sprint/models.py:420)
  +-> CleanupAuditStep (cleanup_audit/models.py)

StepResult (pipeline/models.py:92)
  +-> PhaseResult (sprint/models.py:430)
  +-> CleanupAuditStepResult (cleanup_audit/models.py)
```

## Pipeline Base Models (`cli/pipeline/models.py`)

### StepStatus (line 17)

```python
class StepStatus(Enum):
    PENDING   # Not yet started
    PASS      # Completed successfully
    FAIL      # Failed execution or gate
    TIMEOUT   # Exceeded time limit
    CANCELLED # Cancelled (e.g., parallel sibling failed)
    SKIPPED   # Intentionally skipped
```

Helpers:
- `is_terminal` (line 27): PASS, FAIL, TIMEOUT, CANCELLED, SKIPPED
- `is_success` (line 37): PASS only
- `is_failure` (line 41): FAIL or TIMEOUT

### GateMode (line 46)

```python
class GateMode(Enum):
    BLOCKING  # Gate failure halts pipeline
    TRAILING  # Gate runs async, failures logged but don't halt
```

### SemanticCheck (line 58)

```python
@dataclass
class SemanticCheck:
    name: str                              # Human-readable check name
    check_fn: Callable[[str], bool | str]  # Validator function
    failure_message: str                   # Message on failure
```

### GateCriteria (line 67)

```python
@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
```

Enforcement tier progression: `EXEMPT < LIGHT < STANDARD < STRICT`
- EXEMPT: always pass
- LIGHT: file exists + non-empty
- STANDARD: + min line count + required frontmatter
- STRICT: + semantic check functions

### Step (line 77)

```python
@dataclass
class Step:
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

### StepResult (line 92)

```python
@dataclass
class StepResult:
    step: Optional[Step] = None
    status: StepStatus = StepStatus.PENDING
    attempt: int = 1
    gate_failure_reason: str | None = None
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    # Property: duration_seconds (line 103)
```

### DeliverableKind (line 108)

```python
class DeliverableKind(Enum):
    implement        # Feature implementation
    verify           # Verification task
    invariant_check  # Invariant validation
    fmea_test        # Failure mode analysis
    guard_test       # Guard condition test
    contract_test    # Contract compliance test
```

### Deliverable (line 130)

```python
@dataclass
class Deliverable:
    id: str
    description: str
    kind: DeliverableKind = DeliverableKind.IMPLEMENT
    metadata: dict = field(default_factory=dict)
    # Serialization: to_dict() (148), from_dict() (158)
```

### PipelineConfig (line 169)

```python
@dataclass
class PipelineConfig:
    work_dir: Path = Path(".")
    dry_run: bool = False
    max_turns: int = 100
    model: str = ""
    permission_flag: str = "--dangerously-skip-permissions"
    debug: bool = False
    grace_period: int = 0
```

## Sprint Models (`cli/sprint/models.py`)

### TaskStatus (line 40)

```python
class TaskStatus(Enum):
    PASS       # Task completed successfully
    FAIL       # Task failed
    INCOMPLETE # Task did not finish (context exhaustion)
    SKIPPED    # Task intentionally skipped
```

### GateOutcome (line 57)

```python
class GateOutcome(Enum):
    PASS      # Gate passed
    FAIL      # Gate failed
    DEFERRED  # Gate evaluation deferred (trailing mode)
    PENDING   # Not yet evaluated
```

### GateDisplayState (line 70)

```python
class GateDisplayState(Enum):
    NONE          # No gate configured
    CHECKING      # Gate evaluation in progress
    PASS          # Gate passed
    FAIL_DEFERRED # Failed but deferred
    REMEDIATING   # Remediation in progress
    REMEDIATED    # Remediation complete
    HALT          # Gate failure halted pipeline
```

### PhaseStatus (line 212)

Extended status enum with multiple pass/fail variants:
- `PENDING`, `RUNNING`
- `PASS`, `PASS_RECOVERED` (via checkpoint), `PASS_FREEFORM`
- `FAIL`, `INCOMPLETE`, `HALT`, `TIMEOUT`, `ERROR`, `SKIPPED`

### SprintOutcome (line 265)

```python
class SprintOutcome(Enum):
    SUCCESS      # All phases passed
    HALTED       # Pipeline halted on failure
    INTERRUPTED  # User/signal interrupt
    ERROR        # Unexpected error
```

### TaskEntry (line 25)

```python
@dataclass
class TaskEntry:
    task_id: str           # e.g., "T01.01"
    title: str
    description: str
    dependencies: list[str]  # Task IDs this depends on
    command: str             # For python-mode execution
    classifier: str          # Task classification
```

### TaskResult (line 160)

```python
@dataclass
class TaskResult:
    task: TaskEntry
    status: TaskStatus
    turns_consumed: int
    exit_code: int
    started_at: datetime
    finished_at: datetime
    output_bytes: int
    gate_outcome: GateOutcome
    reimbursement_amount: int
    output_path: str
    # Properties: duration_seconds, to_context_summary()
```

### Phase (line 274)

```python
@dataclass
class Phase:
    number: int
    file: Path
    name: str
    execution_mode: str  # "claude" | "python" | "skip"
    # Properties: basename, display_name
```

### SprintConfig (line 297, extends PipelineConfig)

Key fields beyond base:
- `index_path`, `release_dir`, `phases: list[Phase]`
- `start_phase`, `end_phase`, `stall_timeout`, `stall_action`
- `shadow_gates`, `wiring_gate_enabled`, `wiring_gate_grace_period`
- `force_fidelity_fail`, `tmux_session_name`

Computed properties:
- `results_dir` (392): `release_dir / "results"`
- `execution_log_jsonl` (396): `release_dir / "execution-log.jsonl"`
- `execution_log_md` (400): `release_dir / "execution-log.md"`
- `active_phases` (404): phases filtered by start/end range
- `output_file(phase)` (409): per-phase output path
- `error_file(phase)` (412): per-phase error path
- `result_file(phase)` (415): per-phase result path

### PhaseResult (line 430, extends StepResult)

```python
@dataclass
class PhaseResult(StepResult):
    phase: Phase
    status: PhaseStatus
    exit_code: int
    started_at: datetime
    finished_at: datetime
    output_bytes: int
    error_bytes: int
    last_task_id: str
    files_changed: int
```

### SprintResult (line 460)

```python
@dataclass
class SprintResult:
    config: SprintConfig
    phase_results: list[PhaseResult]
    outcome: SprintOutcome
    started_at: datetime
    finished_at: datetime
    halt_phase: int | None
    # Properties: duration, pass/fail counts, resume_command()
```

### Economy Models

**TurnLedger (line 546)**: Budget management
- Fields: `budget`, `spent`, `wiring_budget`, `wiring_spent`, `reimbursed`
- Methods: `debit()`, `credit()`, `debit_wiring()`, `credit_wiring()`
- Guards: `can_launch()`, `can_remediate()`, `can_run_wiring_gate()`
- Rejects negative values

**ShadowGateMetrics (line 690)**: Gate telemetry
- Fields: `total_evaluated`, `passed`, `failed`, `latency_ms: list[float]`
- Properties: `pass_rate`, `p50_latency_ms`, `p95_latency_ms`

**MonitorState (line 500)**: Live monitoring
- Real-time telemetry: task progress, stall detection, output sizes

## Roadmap Models (`cli/roadmap/models.py`)

### Finding (line 22)

Rich domain model for roadmap findings:
- Identity: `id`, `stable_id`, `rule_id`
- Classification: `severity`, `dimension`, `deviation_class`, `source_layer`
- Content: `description`, `evidence`, `fix_guidance`, `spec_quote`, `roadmap_quote`
- State: `status` (validated against `VALID_FINDING_STATUSES`)
- Relationships: `files_affected`, `agreement_category`

### AgentSpec (line 64)

```python
@dataclass
class AgentSpec:
    model: str     # e.g., "opus"
    persona: str   # e.g., "architect"
    # Parser: parse("opus:architect") -> AgentSpec
    # Property: id -> "opus-architect"
```

## Pipeline Extension Models

### Trailing Gate Models (`cli/pipeline/trailing_gate.py`)

- `TrailingGateResult` (line 35)
- `RemediationEntry` (line 466)
- `RemediationRetryResult` (line 350)
- Enums: `RemediationRetryStatus` (340), `RemediationStatus` (457), `GateScope` (590)

### Diagnostic Models (`cli/pipeline/diagnostic_chain.py`)

- `DiagnosticStage` enum (line 29)
- `StageResult` (line 39)
- `DiagnosticReport` (line 49)

### Guard Models (`cli/pipeline/guard_resolution.py`)

- `AcceptedRisk` (line 24): validates non-empty owner/rationale
- `ReleaseGateWarning` (line 38)
- `GuardResolutionOutput` (line 63)

### Invariant Models (`cli/pipeline/invariants.py`)

- `MutationSite`
- `InvariantEntry`: validates constrained predicate grammar in `__post_init__`
