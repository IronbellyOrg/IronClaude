---
title: "Design: Tasklist CLI Pipeline"
version: v4.xx
status: draft
generated: 2026-03-25
source: prd-tasklist-cli-port.md
pattern: follows src/superclaude/cli/roadmap/ architecture
---

# Design: Tasklist CLI Pipeline

## 1. Architecture Overview

The tasklist CLI pipeline follows the exact pattern established by `src/superclaude/cli/roadmap/`:

```
User invokes CLI
  -> commands.py (Click entrypoint, arg parsing, config construction)
    -> executor.py (_build_steps() constructs Step list, tasklist_run_step dispatches)
      -> pipeline/executor.py (execute_pipeline() generic sequencer)
        -> pipeline/gates.py (gate_passed() validates each step output)
```

The pipeline reuses the shared `pipeline/` base layer (`Step`, `StepResult`, `GateCriteria`, `GateMode`, `execute_pipeline()`, `gate_passed()`). Domain logic lives in `src/superclaude/cli/tasklist/`.

## 2. Module Layout

```
src/superclaude/cli/tasklist/
  __init__.py
  commands.py            # Click group: superclaude tasklist run
  executor.py            # _build_steps(), tasklist_run_step(), _get_all_step_ids()
  gates.py               # 13 GateCriteria constants + semantic checks + ALL_GATES
  models.py              # TasklistConfig(PipelineConfig), RoadmapItem, Phase,
                         #   TaskStub, EnrichedTask, DecisionRecord, Decision,
                         #   ComplexityScore, AdversarialVerdict
  parser.py              # Stage 2: parse_roadmap_items(text) -> list[RoadmapItem]
  bucketer.py            # Stage 2: bucket_into_phases(items) -> list[Phase]
  converter.py           # Stage 3: convert_to_tasks(phases, decisions?) -> list[TaskStub]
  enricher.py            # Stage 4: enrich_tasks(stubs, decisions?) -> list[EnrichedTask]
  renderer.py            # Stage 5: render_index(), render_phase(), render_json_sidecar()
  self_check.py          # Stage 6: run_self_check(bundle) -> list[CheckResult]
  code_reader.py         # Stage 0: read_codebase(), build_decision_record()
  adversarial.py         # Stage 6.5: run_inline_review(), spawn_adversarial_agent()
  prompts.py             # Prompt builders for LLM-only stages (7, 9, certify-like)
  validator.py           # Stage 7: spawn_validation_agents()
  patcher.py             # Stage 8: generate_patch_plan()
  verifier.py            # Stage 10: run_spot_check()
```

No new modules added to `pipeline/`. Zero reverse imports (tasklist never imported by pipeline).

## 3. Data Models (`models.py`)

### 3.1 Pipeline Config

```python
@dataclass
class TasklistConfig(PipelineConfig):
    """Extends PipelineConfig with tasklist-specific fields.

    Inherits from PipelineConfig (pipeline/models.py:170):
        work_dir, dry_run, max_turns, model, permission_flag, debug, grace_period
    """

    roadmap_file: Path = field(default_factory=lambda: Path("."))
    spec_file: Path | None = None
    output_dir: Path = field(default_factory=lambda: Path("."))
    codebase_paths: list[Path] = field(default_factory=list)
    skip_adversarial: bool = False
    gate_mode: str = "full"  # "shadow" | "soft" | "full"

    @property
    def code_aware(self) -> bool:
        """True when Stage 0 should run (codebase paths provided)."""
        return bool(self.codebase_paths)
```

### 3.2 Domain Data Models

```python
@dataclass
class RoadmapItem:
    """A single parsed item from the roadmap. Assigned in Stage 2."""
    id: str                          # R-001, R-002, ...
    text: str                        # Raw text content
    source_heading: str              # Parent heading if any
    line_number: int                 # Source line in roadmap

@dataclass
class Phase:
    """A phase bucket containing roadmap items. Assigned in Stage 2."""
    number: int                      # 1-indexed, contiguous
    name: str                        # Phase name (from heading or generated)
    items: list[RoadmapItem]         # Items assigned to this phase

@dataclass
class TaskStub:
    """A task skeleton before enrichment. Produced in Stage 3."""
    id: str                          # T01.03 format
    title: str
    roadmap_item_id: str             # R-### traceability
    phase_number: int
    deliverables: list[str]          # D-#### IDs
    steps: list[str]                 # Numbered imperative steps
    acceptance_criteria: list[str]   # Exactly 4
    # Mode B fields (populated from decision record, empty in Mode A)
    mechanical_spec: MechanicalSpec | None = None

@dataclass
class MechanicalSpec:
    """Pre-populated from decision record. Mode B only."""
    file: str
    symbol: str
    current_state: str
    target_state: str
    verification_command: str

@dataclass
class EnrichedTask(TaskStub):
    """Fully enriched task with all metadata. Produced in Stage 4."""
    effort: str = "M"               # XS|S|M|L|XL
    risk: str = "Low"               # Low|Medium|High
    risk_drivers: list[str] = field(default_factory=list)
    tier: str = "STANDARD"          # STRICT|STANDARD|LIGHT|EXEMPT
    tier_confidence: float = 0.5
    complexity: ComplexityScore | None = None
    verification_method: str = ""
    mcp_tools: list[str] = field(default_factory=list)
    sub_agent: str | None = None
    critical_path_override: bool = False
    adversarial_review: str = "none"  # "none"|"inline"|"adversarial_quick"

@dataclass
class ComplexityScore:
    """Complexity assessment for adversarial routing."""
    score: int                       # 1-5
    file_count: int
    state_touching: bool
    cross_step_coupling: int
    review_tier: str                 # "none"|"inline"|"adversarial_quick"

@dataclass
class AdversarialVerdict:
    """Result of adversarial review for a single task."""
    task_id: str
    review_tier: str                 # "inline"|"adversarial_quick"
    verdict: str                     # "ACCEPT"|"REFACTOR"|"WARNING"
    concerns: list[str]
    alternative_spec: MechanicalSpec | None = None  # Populated on REFACTOR
```

### 3.3 Decision Record (extends DeviationRegistry pattern)

```python
@dataclass
class Decision:
    """A single locked architectural decision."""
    id: str                          # D-001, D-002, ...
    category: str                    # canonical_name, execution_model, data_format, etc.
    file: str
    symbol: str
    current_state: str
    target_state: str
    rationale: str

@dataclass
class DecisionRecord:
    """Stage 0 output. Extends DeviationRegistry schema."""
    schema_version: int = 1
    files_read: list[str] = field(default_factory=list)
    decisions: list[Decision] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)

    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> DecisionRecord: ...
    def to_json(self, path: Path) -> None: ...
    @classmethod
    def load(cls, path: Path) -> DecisionRecord: ...
```

## 4. Step Pipeline Wiring (`executor.py`)

### 4.1 `_build_steps(config: TasklistConfig) -> list[Step | list[Step]]`

Returns a list of `Step` objects in execution order. All steps are sequential (no parallel groups in the core pipeline; Stage 7 parallel agents are spawned inside the step runner, not as parallel Step entries).

```python
def _build_steps(config: TasklistConfig) -> list[Step | list[Step]]:
    out = config.output_dir

    # Output paths (canonical, locked)
    decision_record = out / "decision-record.md"
    parsed_input    = out / "parsed-input.md"
    phase_buckets   = out / "phase-buckets.md"
    task_skeletons  = out / "task-skeletons.md"
    enriched_tasks  = out / "enriched-tasks.md"
    # Phase files: out / "phase-N-tasklist.md" (dynamic count)
    tasklist_index  = out / "tasklist-index.md"
    self_check_out  = out / "self-check.md"
    adversarial_out = out / "adversarial-review.md"
    validation_out  = out / "validation" / "ValidationReport.md"
    patch_plan      = out / "validation" / "PatchChecklist.md"
    spot_check_out  = out / "validation" / "SpotCheckResults.md"

    steps = []

    # Stage 0: Code-Read + Decision Lock (conditional)
    if config.codebase_paths:
        steps.append(Step(
            id="code-read",
            prompt="",  # non-LLM, dispatched by step.id
            output_file=decision_record,
            gate=CODE_READ_GATE,
            timeout_seconds=60,
            inputs=[config.roadmap_file],
            retry_limit=0,
        ))

    # Stage 1: Input Ingest
    steps.append(Step(
        id="input-ingest",
        prompt="",  # non-LLM
        output_file=parsed_input,
        gate=INPUT_INGEST_GATE,
        timeout_seconds=10,
        inputs=[config.roadmap_file],
        retry_limit=0,
    ))

    # Stage 2: Parse + Phase Bucketing
    steps.append(Step(
        id="parse-bucket",
        prompt="",  # non-LLM
        output_file=phase_buckets,
        gate=PARSE_BUCKET_GATE,
        timeout_seconds=10,
        inputs=[parsed_input],
        retry_limit=0,
    ))

    # Stage 3: Task Conversion
    stage3_inputs = [phase_buckets]
    if config.codebase_paths:
        stage3_inputs.append(decision_record)
    steps.append(Step(
        id="task-convert",
        prompt="",  # non-LLM
        output_file=task_skeletons,
        gate=TASK_CONVERT_GATE,
        timeout_seconds=30,
        inputs=stage3_inputs,
        retry_limit=0,
    ))

    # Stage 4: Enrichment
    steps.append(Step(
        id="enrich",
        prompt="",  # non-LLM
        output_file=enriched_tasks,
        gate=ENRICH_GATE,
        timeout_seconds=30,
        inputs=[task_skeletons],
        retry_limit=0,
    ))

    # Stage 5: File Emission
    steps.append(Step(
        id="emit-files",
        prompt="",  # non-LLM
        output_file=tasklist_index,
        gate=EMIT_FILES_GATE,
        timeout_seconds=30,
        inputs=[enriched_tasks],
        retry_limit=0,
    ))

    # Stage 6: Self-Check
    steps.append(Step(
        id="self-check",
        prompt="",  # non-LLM
        output_file=self_check_out,
        gate=SELF_CHECK_GATE,
        timeout_seconds=30,
        inputs=[tasklist_index],
        retry_limit=0,
    ))

    # Stage 6.5: Complexity-Gated Review (conditional)
    if not config.skip_adversarial:
        steps.append(Step(
            id="adversarial-review",
            prompt="",  # mixed: inline Python + LLM for high complexity
            output_file=adversarial_out,
            gate=ADVERSARIAL_GATE,
            timeout_seconds=600,
            inputs=[enriched_tasks, tasklist_index],
            retry_limit=0,
        ))

    # Stage 7: Roadmap Validation (LLM agents)
    stage7_inputs = [config.roadmap_file, tasklist_index]
    if not config.skip_adversarial:
        stage7_inputs.append(adversarial_out)  # dirty_outputs: re-validate after adversarial changes
    steps.append(Step(
        id="roadmap-validate",
        prompt="",  # dispatched: spawns 2N parallel agents
        output_file=validation_out,
        gate=ROADMAP_VALIDATE_GATE,
        timeout_seconds=900,
        inputs=stage7_inputs,
        retry_limit=1,
    ))

    # Stage 8: Patch Plan Generation
    steps.append(Step(
        id="patch-plan",
        prompt="",  # non-LLM
        output_file=patch_plan,
        gate=PATCH_PLAN_GATE,
        timeout_seconds=30,
        inputs=[validation_out],
        retry_limit=0,
    ))

    # Stage 9: Patch Execution (LLM)
    steps.append(Step(
        id="patch-execute",
        prompt="",  # dispatched: delegates to patch executor
        output_file=out / "patch-execution-log.md",
        gate=PATCH_EXECUTE_GATE,
        timeout_seconds=600,
        inputs=[patch_plan],
        retry_limit=1,
    ))

    # Stage 10: Spot-Check Verification
    steps.append(Step(
        id="spot-check",
        prompt="",  # mixed: targeted re-read + verification
        output_file=spot_check_out,
        gate=SPOT_CHECK_GATE,
        timeout_seconds=300,
        inputs=[validation_out, patch_plan],
        retry_limit=0,
    ))

    return steps
```

### 4.2 Step Runner Dispatch (`tasklist_run_step`)

Follows the roadmap pattern (executor.py:381-539): dispatch by `step.id`, non-LLM steps return `StepResult` directly, LLM steps invoke `ClaudeProcess` via `_run_llm_step()` shared helper.

```python
# Dispatch table eliminates the if/elif chain and makes step registration declarative.
# Each entry: step_id -> (handler_fn, is_llm)
_STEP_DISPATCH: dict[str, tuple[Callable, bool]] = {
    "code-read":          (_run_code_read, False),
    "input-ingest":       (_run_input_ingest, False),
    "parse-bucket":       (_run_parse_bucket, False),
    "task-convert":       (_run_task_convert, False),
    "enrich":             (_run_enrich, False),
    "emit-files":         (_run_emit_files, False),
    "self-check":         (_run_self_check, False),
    "adversarial-review": (_run_adversarial_review, False),  # mixed: inline Python + LLM spawn
    "roadmap-validate":   (_run_roadmap_validate, True),     # LLM: 2N parallel agents
    "patch-plan":         (_run_patch_plan, False),
    "patch-execute":      (_run_patch_execute, True),        # LLM: delegated
    "spot-check":         (_run_spot_check, False),
}

def tasklist_run_step(
    step: Step,
    config: PipelineConfig,
    cancel_check: Callable[[], bool],
) -> StepResult:
    """Execute a single tasklist step. Conforms to StepRunner protocol."""
    started_at = datetime.now(timezone.utc)

    if config.dry_run:
        return StepResult(
            step=step, status=StepStatus.PASS, attempt=1,
            started_at=started_at, finished_at=datetime.now(timezone.utc),
        )

    entry = _STEP_DISPATCH.get(step.id)
    if entry is None:
        raise ValueError(f"Unknown step id: {step.id!r}")

    handler_fn, is_llm = entry
    if is_llm:
        return _run_llm_step(step, config, cancel_check, handler_fn, started_at)
    return handler_fn(step, config, started_at)


def _run_llm_step(step, config, cancel_check, handler_fn, started_at) -> StepResult:
    """Shared LLM step runner: embed inputs, launch ClaudeProcess, poll for cancel.
    Mirrors roadmap executor.py:450-539 pattern."""
    ...
```

**Design note**: The dispatch table replaces the if/elif chain from the roadmap pattern. This is cleaner for 12 steps and makes step registration visible in one place. The roadmap executor uses if/elif because it grew organically; we have the benefit of designing from scratch.

### 4.3 Non-LLM Step Runner Pattern

Each non-LLM step follows this contract:

```python
def _run_STAGE(step: Step, config: TasklistConfig, started_at: datetime) -> StepResult:
    """Run STAGE deterministically. No LLM. No subprocess."""
    try:
        # 1. Read inputs (from step.inputs or config)
        # 2. Call pure domain function
        # 3. Write output to step.output_file (.md)
        # 4. Write JSON sidecar to step.output_file.with_suffix(".json")
        # 5. Return PASS
        return StepResult(step=step, status=StepStatus.PASS, attempt=1,
                          started_at=started_at, finished_at=datetime.now(timezone.utc))
    except Exception as exc:
        return StepResult(step=step, status=StepStatus.FAIL, attempt=1,
                          gate_failure_reason=str(exc),
                          started_at=started_at, finished_at=datetime.now(timezone.utc))
```

## 5. Gate Criteria (`gates.py`)

### 5.1 Gate Definitions

```python
# Stage 0
CODE_READ_GATE = GateCriteria(
    required_frontmatter_fields=["schema_version", "files_read", "decision_count", "unresolved_count"],
    min_lines=5,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(name="zero_unresolved",
                      check_fn=_zero_unresolved,
                      failure_message="unresolved_count must be 0"),
    ],
)

# Stage 1
INPUT_INGEST_GATE = GateCriteria(
    required_frontmatter_fields=["source_file", "line_count"],
    min_lines=3,
    enforcement_tier="STANDARD",
)

# Stage 2
PARSE_BUCKET_GATE = GateCriteria(
    required_frontmatter_fields=["item_count", "phase_count"],
    min_lines=5,
    enforcement_tier="STANDARD",
    semantic_checks=[
        SemanticCheck(name="phase_count_positive",
                      check_fn=_phase_count_positive,
                      failure_message="phase_count must be >= 1"),
    ],
)

# Stage 3
TASK_CONVERT_GATE = GateCriteria(
    required_frontmatter_fields=["task_count", "phase_count", "conversion_mode"],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(name="no_id_collisions",
                      check_fn=_no_id_collisions,
                      failure_message="Duplicate task IDs detected"),
        SemanticCheck(name="mode_b_no_vague_language",
                      check_fn=_mode_b_no_vague,
                      failure_message="Mode B task contains 'ensure/align/verify' without mechanical spec"),
    ],
)

# Stage 4
ENRICH_GATE = GateCriteria(
    required_frontmatter_fields=["task_count", "tier_distribution", "complexity_distribution"],
    min_lines=10,
    enforcement_tier="STANDARD",
)

# Stage 5
EMIT_FILES_GATE = GateCriteria(
    required_frontmatter_fields=["phase_count", "file_count"],
    min_lines=20,
    enforcement_tier="STANDARD",
    semantic_checks=[
        SemanticCheck(name="json_sidecars_present",
                      check_fn=_json_sidecars_present,
                      failure_message="JSON sidecar missing for one or more phase files"),
    ],
)

# Stage 6
SELF_CHECK_GATE = GateCriteria(
    required_frontmatter_fields=["checks_run", "checks_passed", "checks_failed"],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(name="all_checks_passed",
                      check_fn=_all_checks_passed,
                      failure_message="checks_failed must be 0"),
    ],
)

# Stage 6.5
ADVERSARIAL_GATE = GateCriteria(
    required_frontmatter_fields=["tasks_reviewed", "accept_count", "refactor_count", "pending_count"],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(name="no_pending_refactors",
                      check_fn=_no_pending_refactors,
                      failure_message="pending_count must be 0; all REFACTOR verdicts must be resolved"),
    ],
)

# Stage 7
ROADMAP_VALIDATE_GATE = GateCriteria(
    required_frontmatter_fields=["agents_completed", "findings_count"],
    min_lines=10,
    enforcement_tier="STANDARD",
)

# Stage 8
PATCH_PLAN_GATE = GateCriteria(
    required_frontmatter_fields=["findings_count", "patches_planned"],
    min_lines=5,
    enforcement_tier="STANDARD",
)

# Stage 9
PATCH_EXECUTE_GATE = GateCriteria(
    required_frontmatter_fields=["patches_applied", "patches_failed"],
    min_lines=5,
    enforcement_tier="STANDARD",
)

# Stage 10
SPOT_CHECK_GATE = GateCriteria(
    required_frontmatter_fields=["findings_checked", "resolved_count", "unresolved_count"],
    min_lines=5,
    enforcement_tier="LIGHT",
)

ALL_GATES = [
    ("code-read", CODE_READ_GATE),
    ("input-ingest", INPUT_INGEST_GATE),
    ("parse-bucket", PARSE_BUCKET_GATE),
    ("task-convert", TASK_CONVERT_GATE),
    ("enrich", ENRICH_GATE),
    ("emit-files", EMIT_FILES_GATE),
    ("self-check", SELF_CHECK_GATE),
    ("adversarial-review", ADVERSARIAL_GATE),
    ("roadmap-validate", ROADMAP_VALIDATE_GATE),
    ("patch-plan", PATCH_PLAN_GATE),
    ("patch-execute", PATCH_EXECUTE_GATE),
    ("spot-check", SPOT_CHECK_GATE),
]
```

## 6. CLI Entrypoint (`commands.py`)

```python
@click.group("tasklist")
def tasklist_group():
    """Generate tasklists from roadmap files."""

@tasklist_group.command()
@click.argument("roadmap_file", type=click.Path(exists=True, path_type=Path))
@click.option("--spec", type=click.Path(exists=True, path_type=Path), default=None)
@click.option("--output", "output_dir", type=click.Path(path_type=Path), default=None)
@click.option("--codebase", multiple=True, type=click.Path(exists=True, path_type=Path))
@click.option("--skip-adversarial", is_flag=True)
@click.option("--gate-mode", type=click.Choice(["shadow", "soft", "full"]), default="full")
@click.option("--resume", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("--debug", is_flag=True)
@click.option("--max-turns", type=int, default=100)
@click.option("--model", default="")
def run(roadmap_file, spec, output_dir, codebase, skip_adversarial,
        gate_mode, resume, dry_run, debug, max_turns, model):
    """Generate a tasklist from a roadmap file."""
    # Auto-derive output_dir if not provided (TASKLIST_ROOT logic)
    if output_dir is None:
        output_dir = _derive_tasklist_root(roadmap_file)

    config = TasklistConfig(
        roadmap_file=roadmap_file,
        spec_file=spec,
        output_dir=output_dir,
        codebase_paths=list(codebase),
        skip_adversarial=skip_adversarial,
        gate_mode=gate_mode,
        dry_run=dry_run,
        debug=debug,
        max_turns=max_turns,
        model=model,
        work_dir=output_dir,
    )

    tasklist_run(config, resume=resume)
```

## 7. Pure Domain Functions (Module Interfaces)

### 7.1 `parser.py`

```python
def parse_roadmap_items(text: str) -> list[RoadmapItem]:
    """Parse roadmap text into ordered RoadmapItem list.
    Deterministic: same text -> same items with same R-### IDs.
    Pure function: no I/O."""
```

### 7.2 `bucketer.py`

```python
def bucket_into_phases(items: list[RoadmapItem], text: str) -> list[Phase]:
    """Assign items to phases using deterministic rules.
    Priority: explicit labels > top-level headings > 3-phase default.
    Renumber contiguously (no gaps).
    Pure function: no I/O."""
```

### 7.3 `converter.py`

```python
def convert_to_tasks(
    phases: list[Phase],
    decision_record: DecisionRecord | None = None,
) -> list[TaskStub]:
    """Convert roadmap items to task stubs.
    Mode A (no decision_record): standard text-based conversion.
    Mode B (decision_record present): pre-populate MechanicalSpec from decisions.
    Pure function: no I/O."""

def insert_clarification_tasks(stubs: list[TaskStub]) -> list[TaskStub]:
    """Insert clarification tasks where info is missing.
    Pure function: no I/O."""
```

### 7.4 `enricher.py`

```python
def compute_effort(text: str, was_split: bool) -> str:
    """Deterministic effort scoring. Returns XS|S|M|L|XL. Pure."""

def compute_risk(text: str) -> tuple[str, list[str]]:
    """Deterministic risk scoring. Returns (Low|Medium|High, drivers). Pure."""

def compute_tier(text: str, file_paths: list[str]) -> tuple[str, float]:
    """Deterministic tier classification. Returns (tier, confidence). Pure."""

def compute_complexity(
    task: TaskStub,
    decision_record: DecisionRecord | None,
    all_tasks: list[TaskStub],
) -> ComplexityScore:
    """Deterministic complexity scoring (1-5). Pure."""

def enrich_tasks(
    stubs: list[TaskStub],
    decision_record: DecisionRecord | None = None,
) -> list[EnrichedTask]:
    """Apply all enrichment to task stubs. Pure."""
```

### 7.5 `renderer.py`

```python
def render_index(tasks: list[EnrichedTask], config: TasklistConfig) -> str:
    """Render tasklist-index.md content. Deterministic. Pure."""

def render_phase(phase_num: int, tasks: list[EnrichedTask]) -> str:
    """Render phase-N-tasklist.md content. Deterministic. Pure."""

def render_json_sidecar(tasks: list[EnrichedTask], phase_num: int | None = None) -> str:
    """Render JSON sidecar for index or phase. Deterministic. Pure."""
```

### 7.6 `self_check.py`

```python
def run_self_check(output_dir: Path) -> list[CheckResult]:
    """Run 17 structural/semantic assertions.
    Returns list of (name, passed, reason).
    Not pure (reads files), but deterministic."""
```

### 7.7 `code_reader.py`

```python
def read_codebase(paths: list[Path]) -> dict[str, str]:
    """Read source files and return {path: content} mapping.
    Uses Auggie MCP for semantic search when available, falls back to direct reads."""

def build_decision_record(
    file_contents: dict[str, str],
    roadmap_text: str,
) -> DecisionRecord:
    """Analyze source files against roadmap items.
    Trace call chains, identify dead code, map producers/consumers.
    Produce locked decisions with file/symbol/change specs."""
```

### 7.8 `adversarial.py`

```python
def run_inline_review(task: EnrichedTask, all_tasks: list[EnrichedTask]) -> AdversarialVerdict:
    """Tier 'inline' (complexity 3): pure Python heuristic checks.
    - Coupling risk: task touches files also touched by other tasks
    - State risk: task modifies shared state keys/config/models
    - Contract risk: input/output contracts not explicitly defined
    Returns WARNING verdict with specific concerns on failure. Pure."""

def spawn_adversarial_agent(task: EnrichedTask) -> AdversarialVerdict:
    """Tier 'adversarial_quick' (complexity 4-5): spawn LLM debate agent.
    2-3 rounds max. Returns ACCEPT or REFACTOR with alternative spec."""
```

## 8. Data Flow Diagram

```
roadmap.md ─────────────────────────────────────────────────────────┐
                                                                     │
[Stage 0: code-read]  ← --codebase paths                            │
  └─> decision-record.json                                           │
                                                                     │
[Stage 1: input-ingest]  ← roadmap.md + spec.md                     │
  └─> parsed-input.json                                              │
                                                                     │
[Stage 2: parse-bucket]  ← parsed-input.json                        │
  └─> phase-buckets.json  (RoadmapItem[], Phase[])                   │
                                                                     │
[Stage 3: task-convert]  ← phase-buckets.json + decision-record.json?│
  └─> task-skeletons.json (TaskStub[])                               │
                                                                     │
[Stage 4: enrich]  ← task-skeletons.json                             │
  └─> enriched-tasks.json (EnrichedTask[] with complexity scores)    │
                                                                     │
[Stage 5: emit-files]  ← enriched-tasks.json                        │
  └─> tasklist-index.md + phase-N-tasklist.md + .json sidecars       │
                                                                     │
[Stage 6: self-check]  ← all emitted files                          │
  └─> self-check.md (17 assertions)                                  │
                                                                     │
[Stage 6.5: adversarial-review]  ← enriched-tasks.json              │
  ├─> adversarial-review.json (verdicts)                              │
  ├─> enriched-tasks.json (updated with REFACTOR replacements)       │
  └─> RE-EMIT phase-N-tasklist.md if any REFACTOR applied            │
                                                                     │
[Stage 7: roadmap-validate]  ← roadmap.md + phase files  (LLM)      │
  └─> ValidationReport.md                                            │
                                                                     │
[Stage 8: patch-plan]  ← ValidationReport.md                        │
  └─> PatchChecklist.md  (short-circuit if 0 findings)               │
                                                                     │
[Stage 9: patch-execute]  ← PatchChecklist.md  (LLM)                │
  └─> patch-execution-log.md                                         │
                                                                     │
[Stage 10: spot-check]  ← ValidationReport.md + PatchChecklist.md   │
  └─> SpotCheckResults.md                                            │
```

## 9. JSON Sidecar Convention

Every step that writes a `.md` artifact also writes a `.json` sidecar at the same path with `.json` suffix. The sidecar contains the structured data that produced the markdown, enabling downstream steps to consume structured input without parsing markdown.

```python
def _write_step_output(
    output_file: Path,
    markdown: str,
    structured: dict | list,
) -> None:
    """Atomic write of markdown + JSON sidecar pair.

    Uses tmp + os.replace() pattern from roadmap write_state()
    to prevent partial file states.
    """
    import os

    output_file.parent.mkdir(parents=True, exist_ok=True)
    json_file = output_file.with_suffix(".json")

    # Atomic markdown write
    tmp_md = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_md.write_text(markdown, encoding="utf-8")
    os.replace(str(tmp_md), str(output_file))

    # Atomic JSON write
    tmp_json = json_file.with_suffix(".tmp")
    tmp_json.write_text(json.dumps(structured, indent=2), encoding="utf-8")
    os.replace(str(tmp_json), str(json_file))


def _read_step_input(input_file: Path) -> dict | list:
    """Read JSON sidecar for a step input. Raises FileNotFoundError if missing."""
    json_file = input_file.with_suffix(".json")
    return json.loads(json_file.read_text(encoding="utf-8"))
```

Inter-step data flows through JSON sidecars via `_read_step_input()`. No step parses upstream markdown. The `_write_step_output()` helper enforces atomic writes and the sidecar convention in one place — individual `_run_*` handlers never call `write_text` directly.

## 10. Resume + State

Follows roadmap pattern (executor.py:1540, 2433): `.tasklist-state.json` in output directory.

```python
def _save_state(config: TasklistConfig, results: list[StepResult]) -> None:
    """Write .tasklist-state.json via atomic tmp + os.replace().

    State schema:
    {
        "schema_version": 1,
        "roadmap_file": str,
        "last_run": ISO-8601,
        "steps": {step_id: {status, attempt, output_file, started_at, completed_at}},
        "gate_mode": str,
        "code_aware": bool,
    }

    Guards (from roadmap pattern):
    - No-progress guard: skip write when no steps passed
    """

def _apply_resume(
    steps: list[Step | list[Step]],
    config: TasklistConfig,
    gate_fn: Callable,
) -> list[Step | list[Step]]:
    """Skip steps whose outputs pass gates.

    Uses dirty_outputs propagation (roadmap pattern):
    1. If input dependency was regenerated -> rerun (output in dirty set)
    2. If own gate fails -> rerun
    3. If gate passes -> skip
    """

def _step_needs_rerun(
    step: Step,
    gate_fn: Callable,
    dirty_outputs: set[Path],
    state_paths: dict[str, Path],
) -> tuple[bool, str]:
    """Determine if a single step needs re-running.
    Lifted directly from roadmap executor.py:2115-2163 pattern.
    Gate-mode agnostic (works for both BLOCKING and TRAILING)."""
```

**Design note**: `read_state()` and `write_state()` are already generic utilities in `roadmap/executor.py`. If this pattern repeats across 3+ pipelines, they should be extracted to `pipeline/state.py`. For now, we duplicate the pattern (same as roadmap duplicates sprint's) to avoid coupling.

## 10.1 Step ID Registry

```python
def _get_all_step_ids(config: TasklistConfig) -> list[str]:
    """All step IDs in pipeline order. Used for diagnostics and state validation."""
    ids = []
    if config.code_aware:
        ids.append("code-read")
    ids.extend([
        "input-ingest", "parse-bucket", "task-convert", "enrich",
        "emit-files", "self-check",
    ])
    if not config.skip_adversarial:
        ids.append("adversarial-review")
    ids.extend([
        "roadmap-validate", "patch-plan", "patch-execute", "spot-check",
    ])
    return ids
```

**Invariant**: `_get_all_step_ids(config)` must return exactly the same IDs as the flattened `_build_steps(config)` output. Both are conditional on `config.code_aware` and `config.skip_adversarial`.

## 10.2 Stage 6.5 Re-Emission Protocol

**Problem**: Stage 5 (emit-files) writes phase files. Stage 6.5 (adversarial-review) may REFACTOR tasks, making the emitted files stale.

**Solution**: When Stage 6.5 produces any REFACTOR verdict:
1. Update `enriched-tasks.json` with the replacement specs
2. Call `render_phase()` and `render_index()` to re-emit affected phase files + index
3. Re-write JSON sidecars for affected phases
4. The re-emission is part of Stage 6.5's `_run_adversarial_review()` handler — it owns the re-write

**If no REFACTOR verdicts**: Stage 6.5 writes only `adversarial-review.md/.json`. No re-emission.

**Gate implication**: Stage 7 (roadmap-validate) consumes the phase files. Because Stage 6.5 re-emits them before Stage 7 runs, Stage 7 always sees the post-adversarial versions. The `inputs` dependency chain ensures this via dirty_outputs propagation: Stage 6.5's output_file is `adversarial-review.md`, and Stage 7's inputs include `tasklist_index` (which is re-written by Stage 6.5 if REFACTOR occurred). However, to be explicit, Stage 7 should also list `adversarial_out` as an input so that dirty_outputs forces re-validation after any adversarial change.

## 11. Stage 8 Short-Circuit

When Stage 7 produces zero findings:
- Stage 8 writes a clean `ValidationReport.md` with `findings_count: 0`
- Stages 9 and 10 are skipped (their Steps remain in the list but `_run_patch_execute` and `_run_spot_check` detect zero findings and return PASS immediately)

## 12. Integration with `superclaude` CLI

Register the tasklist group in `src/superclaude/cli/main.py`:

```python
from .tasklist.commands import tasklist_group
app.add_command(tasklist_group)
```

Update `src/superclaude/commands/tasklist.md` to invoke CLI pipeline:

```markdown
## Activation
**MANDATORY**: Execute via CLI pipeline:
> superclaude tasklist run <roadmap-path> [options]

Do NOT invoke sc:tasklist-protocol skill. The skill has been superseded.
```

## 13. Migration Checklist (Hard Cutover)

1. Implement `src/superclaude/cli/tasklist/` per this design
2. Register in `cli/main.py`
3. Update `commands/tasklist.md` to point to CLI
4. Delete `src/superclaude/skills/sc-tasklist-protocol/`
5. Delete `.claude/skills/sc-tasklist-protocol/`
6. Run `make sync-dev` and `make verify-sync`
