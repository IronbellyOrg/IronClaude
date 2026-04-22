---
pipeline_name: prd
module_path: src/superclaude/cli/prd/
step_count: 15
module_count: 14
status: completed
---

# Pipeline Specification: PRD Creator

## 1. Step Graph

Steps are defined as a list of `Step | list[Step]` objects. Dynamic steps (research agents, web agents, synthesis agents) are generated at runtime by builder functions.

### Static Steps (always present)

```python
# Step definitions in order of execution
STATIC_STEPS = [
    Step(
        id="check-existing",
        prompt="",  # Pure programmatic — no Claude
        output_file=Path("check-existing-result.json"),
        gate=EXEMPT_GATE,
        timeout_seconds=10,
    ),
    Step(
        id="parse-request",
        prompt=build_parse_request_prompt,  # from prompts.py
        output_file=Path("parsed-request.json"),
        gate=PARSE_REQUEST_GATE,
        timeout_seconds=120,
    ),
    Step(
        id="scope-discovery",
        prompt=build_scope_discovery_prompt,
        output_file=Path("scope-discovery-raw.md"),
        gate=SCOPE_DISCOVERY_GATE,
        timeout_seconds=300,
        inputs=[Path("parsed-request.json")],
    ),
    Step(
        id="write-research-notes",
        prompt=build_research_notes_prompt,
        output_file=Path("research-notes.md"),  # In task_dir
        gate=RESEARCH_NOTES_GATE,
        timeout_seconds=180,
        inputs=[Path("scope-discovery-raw.md"), Path("parsed-request.json")],
    ),
    Step(
        id="review-sufficiency",
        prompt=build_sufficiency_review_prompt,
        output_file=Path("sufficiency-review.json"),
        gate=SUFFICIENCY_GATE,
        timeout_seconds=120,
        inputs=[Path("research-notes.md")],
        retry_limit=2,  # Up to 2 gap-fill rounds
    ),
    Step(
        id="template-triage",
        prompt="",  # Pure programmatic
        output_file=Path("template-selection.json"),
        gate=EXEMPT_GATE,
        timeout_seconds=5,
        inputs=[Path("research-notes.md")],
    ),
    Step(
        id="build-task-file",
        prompt=build_task_file_prompt,
        output_file=Path("task-file.md"),  # Actual path is dynamic
        gate=TASK_FILE_GATE,
        timeout_seconds=600,
        inputs=[
            Path("research-notes.md"),
            Path("refs/build-request-template.md"),
            Path("refs/agent-prompts.md"),
            Path("refs/synthesis-mapping.md"),
            Path("refs/validation-checklists.md"),
            Path("refs/operational-guidance.md"),
        ],
    ),
    Step(
        id="verify-task-file",
        prompt=build_verify_task_file_prompt,
        output_file=Path("task-verification.json"),
        gate=VERIFICATION_GATE,
        timeout_seconds=120,
        inputs=[Path("task-file.md")],
        retry_limit=1,
    ),
    Step(
        id="preparation",
        prompt=build_preparation_prompt,
        output_file=Path(".preparation-complete"),
        gate=LIGHT_GATE,
        timeout_seconds=120,
        inputs=[Path("research-notes.md"), Path("task-file.md")],
    ),
    # --- Dynamic steps injected here: investigation, research-qa, web-research, synthesis ---
    # --- Assembly is static (always 3 sequential agents) ---
]

# Step 14: Assembly & Validation — always 3 sequential steps
ASSEMBLY_STEPS = [
    Step(
        id="assembly",
        prompt=build_assembly_prompt,
        output_file=Path("final-prd.md"),  # Actual output path from config
        gate=ASSEMBLY_GATE,
        timeout_seconds=600,
        # inputs: all synth files (populated at runtime)
    ),
    Step(
        id="structural-qa",
        prompt=build_structural_qa_prompt,
        output_file=Path("qa/qa-report-validation.md"),
        gate=STRUCTURAL_QA_GATE,
        timeout_seconds=300,
        inputs=[Path("final-prd.md")],
    ),
    Step(
        id="qualitative-qa",
        prompt=build_qualitative_qa_prompt,
        output_file=Path("qa/qa-qualitative-review.md"),
        gate=QUALITATIVE_QA_GATE,
        timeout_seconds=300,
        inputs=[Path("final-prd.md")],
    ),
]

# Step 15: Present & Complete
COMPLETION_STEP = Step(
    id="present-complete",
    prompt=build_completion_prompt,
    output_file=Path("completion-summary.md"),
    gate=LIGHT_GATE,
    timeout_seconds=60,
)
```

### Dynamic Step Builders

```python
def build_investigation_steps(config: PrdConfig) -> list[Step]:
    """Generate research agent steps from scope discovery.

    Reads research-notes.md SUGGESTED_PHASES section.
    Returns a list of Steps for parallel execution.
    Agent count: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+.
    """
    notes = _parse_research_notes(config.task_dir / "research-notes.md")
    steps = []
    for i, assignment in enumerate(notes.research_assignments, 1):
        steps.append(Step(
            id=f"investigate-{i:02d}",
            prompt=build_investigation_prompt(
                topic=assignment.topic,
                agent_type=assignment.agent_type,
                files=assignment.files,
                product_root=config.product_root,
                output_path=config.task_dir / f"research/{i:02d}-{assignment.slug}.md",
            ),
            output_file=config.task_dir / f"research/{i:02d}-{assignment.slug}.md",
            gate=RESEARCH_FILE_GATE,
            timeout_seconds=600,
        ))
    return steps


def build_research_qa_steps(config: PrdConfig) -> list[Step]:
    """Generate research QA steps (analyst + QA, possibly partitioned).

    If >6 research files, partition into N subsets and spawn N*2 agents.
    Returns a list of Steps for parallel execution.
    """
    research_files = discover_research_files(config.task_dir)
    if len(research_files) > 6:
        return _build_partitioned_qa_steps(
            research_files, config,
            analyst_type="completeness-verification",
            qa_type="research-gate",
            output_prefix="research",
        )
    return [
        Step(
            id="analyst-completeness",
            prompt=build_analyst_completeness_prompt(config),
            output_file=config.task_dir / "qa/analyst-completeness-report.md",
            gate=QA_REPORT_GATE,
            timeout_seconds=300,
        ),
        Step(
            id="qa-research-gate",
            prompt=build_qa_research_gate_prompt(config),
            output_file=config.task_dir / "qa/qa-research-gate-report.md",
            gate=QA_VERDICT_GATE,
            timeout_seconds=300,
        ),
    ]


def build_web_research_steps(config: PrdConfig) -> list[Step]:
    """Generate web research steps from gaps.

    Agent count: Lightweight 0-1, Standard 1-2, Heavyweight 2-4.
    Returns a list of Steps for parallel execution.
    May return empty list if no web research needed.
    """
    notes = _parse_research_notes(config.task_dir / "research-notes.md")
    steps = []
    for i, topic in enumerate(notes.web_research_topics, 1):
        steps.append(Step(
            id=f"web-research-{i:02d}",
            prompt=build_web_research_prompt(
                topic=topic.name,
                context=topic.codebase_context,
                product=config.product_name,
                output_path=config.task_dir / f"research/web-{i:02d}-{topic.slug}.md",
            ),
            output_file=config.task_dir / f"research/web-{i:02d}-{topic.slug}.md",
            gate=WEB_RESEARCH_GATE,
            timeout_seconds=300,
        ))
    return steps


def build_synthesis_steps(config: PrdConfig) -> list[Step]:
    """Generate synthesis steps from the mapping table.

    Standard: 9 synth files per mapping table.
    Returns a list of Steps for parallel execution.
    """
    mapping = load_synthesis_mapping()  # From refs/synthesis-mapping.md
    all_research = discover_research_files(config.task_dir)  # + web research
    steps = []
    for entry in mapping:
        relevant_research = _filter_research_for_sections(
            all_research, entry.source_topics
        )
        steps.append(Step(
            id=f"synth-{entry.number:02d}",
            prompt=build_synthesis_prompt(
                research_files=relevant_research,
                template_sections=entry.sections,
                output_path=config.task_dir / f"synthesis/{entry.filename}",
                template_path=config.template_path,
            ),
            output_file=config.task_dir / f"synthesis/{entry.filename}",
            gate=SYNTH_FILE_GATE,
            timeout_seconds=300,
            inputs=[Path(f) for f in relevant_research],
        ))
    return steps


def build_synthesis_qa_steps(config: PrdConfig) -> list[Step]:
    """Generate synthesis QA steps (analyst + QA, possibly partitioned).

    If >4 synth files, partition into N subsets and spawn N*2 agents.
    """
    synth_files = discover_synth_files(config.task_dir)
    if len(synth_files) > 4:
        return _build_partitioned_qa_steps(
            synth_files, config,
            analyst_type="synthesis-review",
            qa_type="synthesis-gate",
            output_prefix="synthesis",
        )
    return [
        Step(
            id="analyst-synthesis",
            prompt=build_analyst_synthesis_prompt(config),
            output_file=config.task_dir / "qa/analyst-synthesis-review.md",
            gate=QA_REPORT_GATE,
            timeout_seconds=300,
        ),
        Step(
            id="qa-synthesis-gate",
            prompt=build_qa_synthesis_gate_prompt(config),
            output_file=config.task_dir / "qa/qa-synthesis-gate-report.md",
            gate=QA_VERDICT_GATE,
            timeout_seconds=300,
        ),
    ]
```

### Full Step Graph Assembly

```python
def build_pipeline_steps(config: PrdConfig) -> list[Step | list[Step]]:
    """Assemble the complete step graph.

    Static steps + dynamic steps + assembly + completion.
    Dynamic steps are generated after their prerequisites complete.
    """
    steps: list[Step | list[Step]] = [
        # Stage A: Orchestration
        check_existing_step(),       # Step 1: pure programmatic
        parse_request_step(),        # Step 2: claude-assisted
        scope_discovery_step(),      # Step 3: claude-assisted
        write_research_notes_step(), # Step 4: hybrid
        review_sufficiency_step(),   # Step 5: hybrid (with retry loop)
        template_triage_step(),      # Step 6: pure programmatic
        build_task_file_step(),      # Step 7: claude-assisted
        verify_task_file_step(),     # Step 8: hybrid
        preparation_step(),          # Step 9: hybrid
        # Stage B: Execution (dynamic steps built after prerequisites)
        build_investigation_steps(config),     # Step 10: parallel research
        build_research_qa_steps(config),        # Step 11: parallel QA + fix cycle
        build_web_research_steps(config),       # Step 12: parallel web research
        build_synthesis_steps(config),           # Step 13a: parallel synthesis
        build_synthesis_qa_steps(config),        # Step 13b: parallel QA + fix cycle
        # Assembly (always static)
        ASSEMBLY_STEPS[0],           # Step 14a: rf-assembler
        ASSEMBLY_STEPS[1],           # Step 14b: structural QA
        ASSEMBLY_STEPS[2],           # Step 14c: qualitative QA
        COMPLETION_STEP,             # Step 15: present & complete
    ]
    return steps
```

---

## 2. Model Designs

### 2.1 PrdConfig

```python
from superclaude.cli.pipeline.models import PipelineConfig

@dataclass
class PrdConfig(PipelineConfig):
    """Configuration for the PRD pipeline."""

    # --- Input ---
    user_message: str = ""               # Raw user request
    product_name: str = ""               # Extracted from parse step
    product_slug: str = ""               # kebab-case for task folder
    prd_scope: str = "feature"           # "product" or "feature"
    scenario: str = "B"                  # "A" (explicit) or "B" (vague)
    where: list[str] = field(default_factory=list)  # Source dirs to focus on
    why: str = ""                        # Purpose of the PRD
    output_path: Path = field(default_factory=lambda: Path("."))  # Final PRD location

    # --- Tier ---
    tier: str = "standard"               # "lightweight", "standard", "heavyweight"

    # --- Paths ---
    task_dir: Path = field(default_factory=lambda: Path("."))
    template_path: Path = field(
        default_factory=lambda: Path("docs/docs-product/templates/prd_template.md")
    )
    skill_refs_dir: Path = field(
        default_factory=lambda: Path("src/superclaude/skills/prd/refs")
    )

    # --- Budget ---
    max_turns: int = 300                 # PRD pipelines are turn-heavy
    stall_timeout: int = 120             # seconds before stall detection
    stall_action: str = "warn"           # "warn" or "kill"

    # --- Fix cycles ---
    max_research_fix_cycles: int = 3
    max_synthesis_fix_cycles: int = 2

    # --- QA partitioning thresholds ---
    research_partition_threshold: int = 6   # >6 research files u2192 partition
    synthesis_partition_threshold: int = 4  # >4 synth files u2192 partition

    # --- Resume ---
    resume_from: str | None = None       # Step ID to resume from

    # --- Derived paths ---
    @property
    def results_dir(self) -> Path:
        return self.task_dir / "results"

    @property
    def research_dir(self) -> Path:
        return self.task_dir / "research"

    @property
    def synthesis_dir(self) -> Path:
        return self.task_dir / "synthesis"

    @property
    def qa_dir(self) -> Path:
        return self.task_dir / "qa"

    @property
    def execution_log_jsonl(self) -> Path:
        return self.task_dir / "execution-log.jsonl"

    @property
    def execution_log_md(self) -> Path:
        return self.task_dir / "execution-log.md"

    def output_file(self, step_id: str) -> Path:
        return self.results_dir / f"{step_id}-output.txt"

    def error_file(self, step_id: str) -> Path:
        return self.results_dir / f"{step_id}-errors.txt"

    def result_file(self, step_id: str) -> Path:
        return self.results_dir / f"{step_id}-result.md"
```

### 2.2 PrdStepStatus

```python
class PrdStepStatus(Enum):
    """Lifecycle status for PRD pipeline steps."""

    PENDING = "pending"
    RUNNING = "running"
    PASS = "pass"
    PASS_NO_SIGNAL = "pass_no_signal"      # Completed but no EXIT_RECOMMENDATION
    PASS_NO_REPORT = "pass_no_report"      # Output exists but no result file
    INCOMPLETE = "incomplete"               # Budget exhausted mid-step
    HALT = "halt"                           # Step recommends stopping
    TIMEOUT = "timeout"                     # Hard timeout exceeded
    ERROR = "error"                         # Process crash
    SKIPPED = "skipped"                     # Skipped by config or resume
    QA_FAIL = "qa_fail"                     # QA gate failed, fix cycle needed
    QA_FAIL_EXHAUSTED = "qa_fail_exhausted" # Max fix cycles reached
    VALIDATION_FAIL = "validation_fail"     # Structural validation failed

    @property
    def is_terminal(self) -> bool:
        return self not in (PrdStepStatus.PENDING, PrdStepStatus.RUNNING)

    @property
    def is_success(self) -> bool:
        return self in (
            PrdStepStatus.PASS,
            PrdStepStatus.PASS_NO_SIGNAL,
            PrdStepStatus.PASS_NO_REPORT,
        )

    @property
    def is_failure(self) -> bool:
        return self in (
            PrdStepStatus.INCOMPLETE,
            PrdStepStatus.HALT,
            PrdStepStatus.TIMEOUT,
            PrdStepStatus.ERROR,
            PrdStepStatus.QA_FAIL_EXHAUSTED,
            PrdStepStatus.VALIDATION_FAIL,
        )

    @property
    def needs_fix_cycle(self) -> bool:
        return self == PrdStepStatus.QA_FAIL
```

### 2.3 PrdStepResult

```python
from superclaude.cli.pipeline.models import StepResult

@dataclass
class PrdStepResult(StepResult):
    """Outcome of executing a single PRD pipeline step."""

    exit_code: int = 0
    output_bytes: int = 0
    error_bytes: int = 0
    artifacts_produced: list[str] = field(default_factory=list)
    agent_type: str = ""                  # e.g. "research", "analyst", "qa"
    fix_cycle: int = 0                    # Which fix cycle (0 = first attempt)
    qa_verdict: str | None = None         # PASS / FAIL / None

    @property
    def duration_seconds(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()

    def to_context_summary(self, *, verbose: bool = True) -> str:
        if not verbose:
            return (
                f"- **{self.step.id}**: {self.status.value} "
                f"| agent: {self.agent_type} | verdict: {self.qa_verdict or 'n/a'}"
            )
        lines = [
            f"### {self.step.id}",
            f"- **Status**: {self.status.value}",
            f"- **Agent**: {self.agent_type}",
            f"- **Duration**: {self.duration_seconds:.1f}s",
            f"- **Exit code**: {self.exit_code}",
        ]
        if self.qa_verdict:
            lines.append(f"- **QA Verdict**: {self.qa_verdict}")
        if self.fix_cycle > 0:
            lines.append(f"- **Fix cycle**: {self.fix_cycle}")
        if self.artifacts_produced:
            lines.append(f"- **Artifacts**: {', '.join(self.artifacts_produced)}")
        return "\n".join(lines)
```

### 2.4 PrdPipelineResult

```python
@dataclass
class PrdPipelineResult:
    """Aggregate result for the entire PRD pipeline."""

    config: PrdConfig
    step_results: list[PrdStepResult] = field(default_factory=list)
    outcome: str = "success"               # success | halted | interrupted | error
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None
    halt_step: str | None = None
    halt_reason: str | None = None

    # --- PRD-specific telemetry ---
    research_agent_count: int = 0
    web_agent_count: int = 0
    synthesis_agent_count: int = 0
    research_fix_cycles: int = 0
    synthesis_fix_cycles: int = 0
    final_prd_lines: int = 0
    final_prd_path: str = ""

    @property
    def duration_seconds(self) -> float:
        end = self.finished_at or datetime.now(timezone.utc)
        return (end - self.started_at).total_seconds()

    @property
    def duration_display(self) -> str:
        s = int(self.duration_seconds)
        if s < 3600:
            return f"{s // 60}m {s % 60}s"
        return f"{s // 3600}h {(s % 3600) // 60}m"

    @property
    def steps_passed(self) -> int:
        return sum(1 for r in self.step_results if r.status.is_success)

    @property
    def steps_failed(self) -> int:
        return sum(1 for r in self.step_results if r.status.is_failure)

    def resume_command(self) -> str:
        if self.halt_step:
            return (
                f"superclaude prd run "
                f"--resume {self.halt_step} "
                f"--max-turns {self.suggested_resume_budget}"
            )
        return ""

    @property
    def suggested_resume_budget(self) -> int:
        remaining = sum(
            1 for r in self.step_results
            if r.status in (PrdStepStatus.PENDING, PrdStepStatus.INCOMPLETE)
        )
        return max(remaining * 25, 50)
```

### 2.5 PrdMonitorState

```python
@dataclass
class PrdMonitorState:
    """Real-time state extracted by the sidecar monitor thread."""

    output_bytes: int = 0
    last_event_time: float = field(default_factory=time.monotonic)
    phase_started_at: float = field(default_factory=time.monotonic)
    events_received: int = 0
    last_step_id: str = ""
    current_artifact: str = ""
    files_changed: int = 0
    lines_total: int = 0
    growth_rate_bps: float = 0.0
    stall_seconds: float = 0.0

    # PRD-specific signals
    research_files_completed: int = 0
    synth_files_completed: int = 0
    qa_verdict: str | None = None
    current_agent_type: str = ""
    fix_cycle_count: int = 0

    @property
    def stall_status(self) -> str:
        now = time.monotonic()
        if self.events_received == 0:
            if now - self.phase_started_at > 120:
                return "STALLED"
            return "waiting..."
        since_last = now - self.last_event_time
        if since_last > 120:
            return "STALLED"
        if since_last > 30:
            return "thinking..."
        return "active"
```

### 2.6 TurnLedger Integration

Reuse the existing `TurnLedger` from `superclaude.cli.sprint.models`. The PRD pipeline is turn-heavy (many subprocesses), so budget management is critical:

```python
from superclaude.cli.sprint.models import TurnLedger

def create_prd_ledger(config: PrdConfig) -> TurnLedger:
    return TurnLedger(
        initial_budget=config.max_turns,
        minimum_allocation=10,          # Min turns per subprocess launch
        minimum_remediation_budget=5,   # Min turns for QA fix cycles
    )
```

---

## 3. Gate Definitions

```python
from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck

# --- Tier constants ---
EXEMPT_GATE = GateCriteria(
    required_frontmatter_fields=[], min_lines=0, enforcement_tier="EXEMPT"
)

LIGHT_GATE = GateCriteria(
    required_frontmatter_fields=[], min_lines=0, enforcement_tier="LIGHT"
)

# --- Step 2: Parse Request ---
PARSE_REQUEST_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=0,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="required_fields",
            check_fn=_check_parsed_request_fields,
            failure_message="Parsed request missing required fields (GOAL, PRODUCT_SLUG, PRD_SCOPE, SCENARIO)",
        ),
    ],
)

# --- Step 3: Scope Discovery ---
SCOPE_DISCOVERY_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=50,
    enforcement_tier="STANDARD",
)

# --- Step 4: Research Notes ---
RESEARCH_NOTES_GATE = GateCriteria(
    required_frontmatter_fields=["Date", "Scenario", "Tier"],
    min_lines=100,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="seven_sections",
            check_fn=_check_research_notes_sections,
            failure_message="Research notes missing required sections",
        ),
        SemanticCheck(
            name="agent_detail",
            check_fn=_check_suggested_phases_detail,
            failure_message="SUGGESTED_PHASES entries missing (topic, agent_type, files, output_path)",
        ),
    ],
)

# --- Step 5: Sufficiency Review ---
SUFFICIENCY_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=0,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="verdict_present",
            check_fn=_check_verdict_field,
            failure_message="Sufficiency review missing verdict field (PASS or FAIL)",
        ),
    ],
)

# --- Step 7: Task File ---
def build_task_file_gate(tier: str) -> GateCriteria:
    """Tier-dependent gate for task file validation."""
    min_lines = {"lightweight": 200, "standard": 400, "heavyweight": 600}[tier]
    return GateCriteria(
        required_frontmatter_fields=["id", "title", "status", "complexity", "created_date"],
        min_lines=min_lines,
        enforcement_tier="STRICT",
        semantic_checks=[
            SemanticCheck(
                name="phases_present",
                check_fn=_check_task_phases_present,
                failure_message="Task file missing required phase headers",
            ),
            SemanticCheck(
                name="b2_pattern",
                check_fn=_check_b2_self_contained,
                failure_message='Checklist items reference "see above" instead of being self-contained',
            ),
            SemanticCheck(
                name="parallel_instructions",
                check_fn=_check_parallel_instructions,
                failure_message="Phases 2/3/4/5 missing parallel spawning instructions",
            ),
        ],
    )

# --- Step 8: Verification ---
VERIFICATION_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=0,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="verdict_present",
            check_fn=_check_verdict_field,
            failure_message="Task verification missing verdict (PASS or FAIL)",
        ),
    ],
)

# --- Step 10: Research Files (per-file) ---
RESEARCH_FILE_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=50,
    enforcement_tier="STANDARD",
)

# --- Step 11: QA Reports ---
QA_REPORT_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=20,
    enforcement_tier="STANDARD",
)

QA_VERDICT_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="qa_verdict",
            check_fn=_check_qa_verdict,
            failure_message="QA report missing PASS/FAIL verdict",
        ),
    ],
)

# --- Step 12: Web Research Files (per-file) ---
WEB_RESEARCH_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=30,
    enforcement_tier="STANDARD",
)

# --- Step 13: Synthesis Files (per-file) ---
SYNTH_FILE_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=80,
    enforcement_tier="STANDARD",
)

# --- Step 14a: Assembly ---
def build_assembly_gate(tier: str) -> GateCriteria:
    """Tier-dependent gate for assembled PRD."""
    line_budgets = {
        "lightweight": (400, 800),
        "standard": (800, 1500),
        "heavyweight": (1500, 2500),
    }
    min_lines, _max_lines = line_budgets[tier]
    return GateCriteria(
        required_frontmatter_fields=["id", "title", "status", "created_date", "tags"],
        min_lines=min_lines,
        enforcement_tier="STRICT",
        semantic_checks=[
            SemanticCheck(
                name="template_sections",
                check_fn=_check_prd_template_sections,
                failure_message="PRD missing required template sections",
            ),
            SemanticCheck(
                name="no_placeholders",
                check_fn=_check_no_placeholders,
                failure_message="PRD contains placeholder text (TODO, TBD, PLACEHOLDER)",
            ),
        ],
    )

# --- Step 14b: Structural QA ---
STRUCTURAL_QA_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="qa_verdict",
            check_fn=_check_qa_verdict,
            failure_message="Structural QA report missing PASS/FAIL verdict",
        ),
    ],
)

# --- Step 14c: Qualitative QA ---
QUALITATIVE_QA_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="qa_verdict",
            check_fn=_check_qa_verdict,
            failure_message="Qualitative QA report missing verdict",
        ),
    ],
)
```

### Semantic Check Function Implementations

```python
import json
import re

def _check_parsed_request_fields(content: str) -> bool | str:
    """Verify parsed-request.json has all required fields."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return "Content is not valid JSON"
    required = {"GOAL", "PRODUCT_SLUG", "PRD_SCOPE", "SCENARIO"}
    missing = required - set(data.keys())
    if missing:
        return f"Missing required fields: {', '.join(sorted(missing))}"
    for field in required:
        if not data.get(field):
            return f"Field '{field}' is empty"
    return True


def _check_research_notes_sections(content: str) -> bool | str:
    """Verify research notes contain all 7 required sections."""
    required_sections = {
        "EXISTING_FILES", "PATTERNS_AND_CONVENTIONS", "FEATURE_ANALYSIS",
        "RECOMMENDED_OUTPUTS", "SUGGESTED_PHASES", "TEMPLATE_NOTES",
        "AMBIGUITIES_FOR_USER",
    }
    found = set()
    for line in content.splitlines():
        stripped = line.strip().lstrip("# ").strip()
        if stripped in required_sections:
            found.add(stripped)
    missing = required_sections - found
    if missing:
        return f"Missing sections: {', '.join(sorted(missing))}"
    return True


def _check_suggested_phases_detail(content: str) -> bool | str:
    """Verify SUGGESTED_PHASES entries have per-agent detail."""
    in_section = False
    has_entries = False
    for line in content.splitlines():
        if "SUGGESTED_PHASES" in line and line.strip().startswith("#"):
            in_section = True
            continue
        if in_section and line.strip().startswith("#") and "SUGGESTED_PHASES" not in line:
            break
        if in_section and line.strip().startswith("-"):
            has_entries = True
    if not has_entries:
        return "SUGGESTED_PHASES section is empty"
    return True


def _check_verdict_field(content: str) -> bool | str:
    """Verify content contains a verdict: PASS or FAIL."""
    content_upper = content.upper()
    if '"VERDICT":' in content_upper or '"VERDICT" :' in content_upper:
        if '"PASS"' in content_upper or '"FAIL"' in content_upper:
            return True
    # Also check markdown format
    if re.search(r"(?:verdict|VERDICT)[:\s]+(PASS|FAIL)", content):
        return True
    return "No verdict field found (expected PASS or FAIL)"


def _check_task_phases_present(content: str) -> bool | str:
    """Verify task file contains all required phase headers."""
    required_phases = {
        "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6", "Phase 7"
    }
    found = set()
    for line in content.splitlines():
        for phase in required_phases:
            if phase.lower() in line.lower() and line.strip().startswith("#"):
                found.add(phase)
    missing = required_phases - found
    if missing:
        return f"Missing phase headers: {', '.join(sorted(missing))}"
    return True


def _check_b2_self_contained(content: str) -> bool | str:
    """Verify checklist items don't reference 'see above' or 'see Phase X'."""
    violations = []
    for i, line in enumerate(content.splitlines(), 1):
        if line.strip().startswith("- [ ]") or line.strip().startswith("- [x]"):
            lower = line.lower()
            if "see above" in lower or "as described above" in lower:
                violations.append(f"Line {i}: references 'see above'")
    if violations:
        return f"B2 violations: {'; '.join(violations[:3])}"
    return True


def _check_parallel_instructions(content: str) -> bool | str:
    """Verify phases 2, 3, 4, 5 mention parallel spawning."""
    parallel_keywords = {"parallel", "concurrent", "simultaneously", "fan-out"}
    phases_needing_parallel = {"Phase 2", "Phase 3", "Phase 4", "Phase 5"}
    missing = []
    for phase_name in phases_needing_parallel:
        # Find the phase section
        phase_pattern = re.compile(
            rf"#{1,3}\s*{re.escape(phase_name)}.*?(?=#{1,3}\s*Phase|\Z)",
            re.DOTALL | re.IGNORECASE
        )
        match = phase_pattern.search(content)
        if match:
            section = match.group(0).lower()
            if not any(kw in section for kw in parallel_keywords):
                missing.append(phase_name)
    if missing:
        return f"Phases missing parallel instructions: {', '.join(missing)}"
    return True


def _check_qa_verdict(content: str) -> bool | str:
    """Verify QA report contains a clear PASS or FAIL verdict."""
    if re.search(r"(?:verdict|VERDICT)[:\s]+(PASS|FAIL)", content):
        return True
    if "**PASS**" in content or "**FAIL**" in content:
        return True
    return "QA report missing PASS/FAIL verdict"


def _check_prd_template_sections(content: str) -> bool | str:
    """Verify PRD contains expected numbered template sections."""
    # Check for key sections (not all 28 u2014 some may be N/A)
    critical_sections = [
        r"##\s*1\.?\s*Executive Summary",
        r"##\s*2\.?\s*Problem Statement",
        r"##\s*14\.?\s*Technical Requirements",
        r"##\s*21\.?\s*Implementation Plan",
    ]
    missing = []
    for pattern in critical_sections:
        if not re.search(pattern, content, re.IGNORECASE):
            missing.append(pattern)
    if missing:
        return f"PRD missing critical sections: {len(missing)} not found"
    return True


def _check_no_placeholders(content: str) -> bool | str:
    """Verify no placeholder text remains."""
    placeholders = ["TODO", "TBD", "PLACEHOLDER", "[INSERT"]
    found = []
    for p in placeholders:
        if p in content:
            count = content.count(p)
            found.append(f"{p} ({count}x)")
    if found:
        return f"Placeholder text found: {', '.join(found)}"
    return True
```

---

## 4. Pure-Programmatic Step Implementations

### 4.1 check_existing_work()

```python
import glob
import json
from pathlib import Path
from enum import Enum

class ExistingWorkState(Enum):
    NO_EXISTING = "no_existing"
    RESUME_STAGE_A = "resume_stage_a"     # research-notes.md exists but incomplete
    RESUME_STAGE_B = "resume_stage_b"     # Task file exists with unchecked items
    ALREADY_COMPLETE = "already_complete"  # All items checked

def check_existing_work(config: PrdConfig) -> ExistingWorkState:
    """Check for existing PRD task work.

    Scans .dev/tasks/to-do/TASK-PRD-*/ for matching product folders.
    Returns the appropriate state for pipeline routing.
    """
    task_dirs = sorted(
        Path(".dev/tasks/to-do").glob("TASK-PRD-*/"),
        key=lambda p: p.name,
        reverse=True,  # Most recent first
    )

    for task_dir in task_dirs:
        # Check if this task relates to the same product
        research_notes = task_dir / "research-notes.md"
        if research_notes.exists():
            content = research_notes.read_text(encoding="utf-8")
            # Simple heuristic: check if product name appears
            if config.product_name.lower() not in content.lower():
                continue

        # Check for task file
        task_files = list(task_dir.glob("TASK-PRD-*.md"))
        if task_files:
            task_file = task_files[0]
            task_content = task_file.read_text(encoding="utf-8")
            unchecked = task_content.count("- [ ]")
            checked = task_content.count("- [x]")

            if unchecked == 0 and checked > 0:
                config.task_dir = task_dir
                return ExistingWorkState.ALREADY_COMPLETE
            if unchecked > 0:
                config.task_dir = task_dir
                return ExistingWorkState.RESUME_STAGE_B

        # Check for research notes without task file
        if research_notes.exists():
            content = research_notes.read_text(encoding="utf-8")
            if "Status: Complete" in content:
                config.task_dir = task_dir
                return ExistingWorkState.RESUME_STAGE_A

    return ExistingWorkState.NO_EXISTING
```

### 4.2 select_template()

```python
def select_template(config: PrdConfig) -> int:
    """Select MDTM template based on request type.

    Returns 2 for PRD creation (complex task, always).
    Returns 1 for simple PRD update (single section edit).
    """
    if config.scenario == "update":
        return 1
    return 2
```

### 4.3 create_task_dirs()

```python
from datetime import datetime

def create_task_dirs(config: PrdConfig) -> Path:
    """Create the task directory structure.

    Returns the task directory path.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    task_id = f"TASK-PRD-{timestamp}"
    task_dir = Path(".dev/tasks/to-do") / task_id

    for subdir in ["research", "synthesis", "qa", "reviews", "results"]:
        (task_dir / subdir).mkdir(parents=True, exist_ok=True)

    config.task_dir = task_dir
    return task_dir
```

### 4.4 discover_research_files()

```python
def discover_research_files(task_dir: Path) -> list[Path]:
    """Find all completed research files in the task directory.

    Returns sorted list of research files (codebase + web).
    Validates each file has Status: Complete.
    """
    research_dir = task_dir / "research"
    files = sorted(research_dir.glob("[0-9]*.md")) + sorted(research_dir.glob("web-*.md"))
    completed = []
    for f in files:
        content = f.read_text(encoding="utf-8", errors="replace")
        if "Status: Complete" in content or "Status: complete" in content:
            completed.append(f)
    return completed
```

### 4.5 discover_synth_files()

```python
def discover_synth_files(task_dir: Path) -> list[Path]:
    """Find all synthesis files in the task directory."""
    return sorted((task_dir / "synthesis").glob("synth-*.md"))
```

### 4.6 partition_files()

```python
def partition_files(files: list[Path], threshold: int) -> list[list[Path]]:
    """Partition files into subsets for parallel QA.

    If len(files) <= threshold, returns [files] (single partition).
    Otherwise, splits into ceil(len/threshold) partitions.
    """
    if len(files) <= threshold:
        return [files]
    partition_size = threshold
    return [
        files[i : i + partition_size]
        for i in range(0, len(files), partition_size)
    ]
```

### 4.7 merge_qa_partition_reports()

```python
def merge_qa_partition_reports(
    report_paths: list[Path], output_path: Path
) -> None:
    """Merge numbered QA partition reports into a single report."""
    merged_lines = ["# Merged QA Report\n\n"]
    overall_verdict = "PASS"
    for path in sorted(report_paths):
        content = path.read_text(encoding="utf-8")
        merged_lines.append(f"## Partition: {path.name}\n\n")
        merged_lines.append(content)
        merged_lines.append("\n---\n\n")
        if "FAIL" in content.upper() and "verdict" in content.lower():
            overall_verdict = "FAIL"
    merged_lines.append(f"\n## Overall Verdict: {overall_verdict}\n")
    output_path.write_text("".join(merged_lines), encoding="utf-8")
```

### 4.8 compile_gaps()

```python
def compile_gaps(task_dir: Path) -> Path:
    """Compile gaps from all research files into gaps-and-questions.md."""
    gaps_path = task_dir / "gaps-and-questions.md"
    lines = ["# Gaps and Questions\n\n"]
    research_files = discover_research_files(task_dir)
    for rf in research_files:
        content = rf.read_text(encoding="utf-8")
        # Extract gaps section
        in_gaps = False
        for line in content.splitlines():
            if line.strip().startswith("## Gaps") or line.strip().startswith("## Stale"):
                in_gaps = True
                lines.append(f"### From {rf.name}\n")
                continue
            if in_gaps and line.strip().startswith("## ") and "Gaps" not in line:
                in_gaps = False
                continue
            if in_gaps:
                lines.append(line + "\n")
    # Deduplicate
    lines.append("\n---\n")
    gaps_path.write_text("".join(lines), encoding="utf-8")
    return gaps_path
```

### 4.9 load_synthesis_mapping()

```python
@dataclass
class SynthMappingEntry:
    number: int
    filename: str
    sections: list[str]
    source_topics: list[str]

def load_synthesis_mapping() -> list[SynthMappingEntry]:
    """Load the standard synthesis mapping table.

    Returns the 9-entry mapping from refs/synthesis-mapping.md.
    """
    return [
        SynthMappingEntry(1, "synth-01-exec-problem-vision.md",
            ["1. Executive Summary", "2. Problem Statement", "3. Background & Strategic Fit", "4. Product Vision"],
            ["product capabilities", "web research (market context)", "existing docs"]),
        SynthMappingEntry(2, "synth-02-business-market.md",
            ["5. Business Context", "6. JTBD", "7. User Personas", "8. Value Proposition Canvas"],
            ["user flows", "web research (market context)", "product capabilities"]),
        SynthMappingEntry(3, "synth-03-competitive-scope.md",
            ["9. Competitive Analysis", "10. Assumptions & Constraints", "11. Dependencies", "12. Scope Definition"],
            ["web research (competitive landscape)", "technical stack", "integration points"]),
        SynthMappingEntry(4, "synth-04-stories-requirements.md",
            ["13. Open Questions", "21.1 Epics Features & Stories", "21.2 Product Requirements"],
            ["per-area research files", "user flows", "gaps log"]),
        SynthMappingEntry(5, "synth-05-technical-stack.md",
            ["14. Technical Requirements", "15. Technology Stack"],
            ["technical stack", "architecture research", "web research (technology trends)"]),
        SynthMappingEntry(6, "synth-06-ux-legal-business.md",
            ["16. UX Requirements", "17. Legal & Compliance", "18. Business Requirements"],
            ["user flows", "product capabilities", "web research (compliance, market)"]),
        SynthMappingEntry(7, "synth-07-metrics-risk-impl.md",
            ["19. Success Metrics", "20. Risk Analysis", "21.3 Implementation Phasing", "21.4 Release Criteria & DoD", "21.5 Timeline & Milestones"],
            ["all research files", "web research", "technical stack"]),
        SynthMappingEntry(8, "synth-08-journey-design-api.md",
            ["22. Customer Journey", "23. Error Handling", "24. User Interaction", "25. API Contracts"],
            ["user flows", "per-area research", "technical stack"]),
        SynthMappingEntry(9, "synth-09-resources-maintenance.md",
            ["26. Contributors", "27. Related Resources", "28. Maintenance & Ownership"],
            ["existing docs", "all research files", "gaps log"]),
    ]
```

---

## 5. Executor Design

The PRD executor follows the sprint-style synchronous supervisor pattern with three specialized execution modes:

### 5.1 Main Execution Loop

```python
def execute_prd_pipeline(config: PrdConfig) -> PrdPipelineResult:
    """Main pipeline entry point."""
    signal_handler = SignalHandler()
    logger = PrdLogger(config)
    tui = PrdTUI(config)
    ledger = create_prd_ledger(config)
    result = PrdPipelineResult(config=config)

    tui.start()
    try:
        # Phase routing based on existing work check
        existing = check_existing_work(config)
        if existing == ExistingWorkState.ALREADY_COMPLETE:
            tui.show_message("PRD already complete")
            result.outcome = "success"
            return result

        start_step = _resolve_start_step(existing, config.resume_from)

        # Build initial static steps
        steps = build_static_steps(config)

        for step in steps:
            if signal_handler.shutdown_requested:
                result.outcome = "interrupted"
                break

            # Skip steps before resume point
            if _should_skip(step, start_step, config):
                continue

            # Budget guard
            if not step.prompt == "" and not ledger.can_launch():
                result.outcome = "halted"
                result.halt_step = step.id
                result.halt_reason = "Budget exhausted"
                break

            # Route to appropriate executor
            if step.prompt == "":
                step_result = _execute_programmatic(step, config)
            elif isinstance(step, list):
                step_result = _execute_parallel_group(step, config, ledger, tui, signal_handler)
            else:
                step_result = _execute_claude_step(step, config, ledger, tui, signal_handler)

            result.step_results.append(step_result)
            logger.write_step_result(step_result)

            # Handle fix cycles for QA steps
            if step_result.status == PrdStepStatus.QA_FAIL:
                step_result = _run_fix_cycle(
                    step, config, ledger, tui, signal_handler, result
                )

            # Halt on failure
            if step_result.status.is_failure:
                result.outcome = "halted"
                result.halt_step = step.id
                result.halt_reason = str(step_result.gate_failure_reason)
                break

            # After key steps, build dynamic steps
            if step.id == "preparation":
                dynamic_steps = _build_dynamic_stage_b(config)
                steps.extend(dynamic_steps)

    finally:
        result.finished_at = datetime.now(timezone.utc)
        tui.stop()
        logger.finalize(result)

    return result
```

### 5.2 Parallel Group Execution

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def _execute_parallel_group(
    steps: list[Step],
    config: PrdConfig,
    ledger: TurnLedger,
    tui: PrdTUI,
    signal_handler: SignalHandler,
) -> list[PrdStepResult]:
    """Execute a group of steps in parallel using ThreadPoolExecutor.

    Each step runs as a separate ClaudeProcess.
    Returns results for all steps.
    """
    results = []
    max_workers = min(len(steps), 10)  # Cap at 10 concurrent agents

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_execute_claude_step, step, config, ledger, tui, signal_handler): step
            for step in steps
        }

        for future in as_completed(futures):
            step = futures[future]
            try:
                step_result = future.result()
                results.append(step_result)
                tui.update_step_complete(step.id, step_result.status)
            except Exception as e:
                results.append(PrdStepResult(
                    step=step,
                    status=PrdStepStatus.ERROR,
                    gate_failure_reason=str(e),
                ))

    return results
```

### 5.3 Fix Cycle Execution

```python
def _run_fix_cycle(
    original_step: Step,
    config: PrdConfig,
    ledger: TurnLedger,
    tui: PrdTUI,
    signal_handler: SignalHandler,
    result: PrdPipelineResult,
) -> PrdStepResult:
    """Run QA fix cycles: spawn gap-filling agents, then re-run QA.

    For research QA (Step 11): max 3 cycles.
    For synthesis QA (Step 13b): max 2 cycles.
    """
    max_cycles = (
        config.max_research_fix_cycles
        if "research" in original_step.id
        else config.max_synthesis_fix_cycles
    )

    for cycle in range(1, max_cycles + 1):
        tui.show_message(f"Fix cycle {cycle}/{max_cycles} for {original_step.id}")

        # 1. Parse the QA report for specific failures
        failures = _parse_qa_failures(original_step, config)

        # 2. Spawn targeted gap-filling agents
        gap_steps = _build_gap_filling_steps(failures, config, cycle)
        if gap_steps:
            gap_results = _execute_parallel_group(
                gap_steps, config, ledger, tui, signal_handler
            )
            result.step_results.extend(gap_results)

        # 3. Re-run QA with fix-cycle mode
        qa_step = _build_fix_cycle_qa_step(original_step, config, cycle)
        qa_result = _execute_claude_step(
            qa_step, config, ledger, tui, signal_handler
        )
        qa_result.fix_cycle = cycle
        result.step_results.append(qa_result)

        if qa_result.qa_verdict == "PASS":
            return qa_result

    # Exhausted all cycles
    return PrdStepResult(
        step=original_step,
        status=PrdStepStatus.QA_FAIL_EXHAUSTED,
        gate_failure_reason=f"Max fix cycles ({max_cycles}) exhausted",
    )
```

### 5.4 Status Classification

```python
def _determine_status(
    exit_code: int,
    step: Step,
    config: PrdConfig,
    output_path: Path,
) -> PrdStepStatus:
    """Map exit conditions to deterministic status."""
    if exit_code == 124:
        return PrdStepStatus.TIMEOUT
    if exit_code != 0:
        return PrdStepStatus.ERROR

    if not output_path.exists():
        return PrdStepStatus.ERROR

    content = output_path.read_text(encoding="utf-8")

    # Check for machine-readable markers
    if "EXIT_RECOMMENDATION: HALT" in content:
        return PrdStepStatus.HALT
    if "EXIT_RECOMMENDATION: CONTINUE" in content:
        return PrdStepStatus.PASS

    # Check for QA verdicts
    if re.search(r"verdict[:\s]+FAIL", content, re.IGNORECASE):
        return PrdStepStatus.QA_FAIL
    if re.search(r"verdict[:\s]+PASS", content, re.IGNORECASE):
        return PrdStepStatus.PASS

    # Check for max-turns exhaustion
    if detect_error_max_turns(output_path):
        return PrdStepStatus.INCOMPLETE

    # Output exists but no signal
    return PrdStepStatus.PASS_NO_SIGNAL
```

---

## 6. Module Plan

### 6.1 Files to Generate

| File | Lines (est.) | Purpose | Dependencies |
|------|-------------|---------|---------------|
| `__init__.py` | 15 | Package exports | u2014 |
| `models.py` | 280 | PrdConfig, PrdStepStatus, PrdStepResult, PrdPipelineResult, PrdMonitorState, ExistingWorkState | `pipeline.models` |
| `gates.py` | 250 | Gate criteria constants + all semantic check functions | `pipeline.models` |
| `prompts.py` | 400+ | Prompt builders for all 8 Claude-assisted step types | `models` |
| `config.py` | 120 | CLI arg resolution, PrdConfig construction, file discovery | `models` |
| `inventory.py` | 150 | `check_existing_work()`, `discover_research_files()`, `discover_synth_files()`, `create_task_dirs()`, `load_synthesis_mapping()` | `models` |
| `filtering.py` | 100 | `partition_files()`, `compile_gaps()`, `merge_qa_partition_reports()`, `_filter_research_for_sections()` | `inventory` |
| `executor.py` | 250 | Main execution loop, parallel dispatch, fix cycles, status classification | `models`, `gates`, `prompts`, `inventory`, `filtering`, `process`, `monitor`, `tui` |
| `process.py` | 80 | `PrdClaudeProcess` extending `pipeline.process.ClaudeProcess` | `pipeline.process`, `models` |
| `monitor.py` | 120 | NDJSON output parser with PRD-specific signals | `models` |
| `tui.py` | 180 | Rich live dashboard with step progress, QA verdicts, fix cycle state | `models` |
| `logging_.py` | 100 | Dual JSONL + Markdown execution logging | `models` |
| `diagnostics.py` | 120 | `DiagnosticCollector`, `FailureClassifier`, resume output | `models` |
| `commands.py` | 80 | Click CLI group: `prd run`, `prd resume` | `config`, `executor` |
| **Total** | **~2,245** | | |

### 6.2 Implementation Order

```
1. models.py          (zero internal deps)
2. gates.py           (depends on: pipeline.models)
3. inventory.py       (depends on: models)
4. filtering.py       (depends on: inventory)
5. prompts.py         (depends on: models; reads ref files)
6. config.py          (depends on: models, inventory)
7. monitor.py         (depends on: models)
8. process.py         (depends on: pipeline.process, models)
9. logging_.py        (depends on: models)
10. diagnostics.py    (depends on: models)
11. tui.py            (depends on: models, monitor)
12. executor.py       (depends on: everything above)
13. commands.py       (depends on: config, executor)
14. __init__.py       (depends on: commands)
```

### 6.3 Integration with main.py

```python
# In src/superclaude/cli/main.py
from superclaude.cli.prd.commands import prd_group
app.add_command(prd_group)
```

### 6.4 Click Command Group

```python
@click.group("prd")
def prd_group():
    """PRD Creator — Generate comprehensive Product Requirements Documents."""
    pass

@prd_group.command("run")
@click.argument("request", required=False)
@click.option("--product", "-p", help="Product name or scope")
@click.option("--where", "-w", multiple=True, help="Source directories to focus on")
@click.option("--output", "-o", type=click.Path(), help="Output path for final PRD")
@click.option("--tier", type=click.Choice(["lightweight", "standard", "heavyweight"]), default="standard")
@click.option("--max-turns", default=300, type=int, help="Turn budget")
@click.option("--model", default=None, help="Claude model to use")
@click.option("--dry-run", is_flag=True, help="Validate config without executing")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def run(request, product, where, output, tier, max_turns, model, dry_run, debug):
    """Create a PRD from a product request."""
    config = build_config(
        request=request, product=product, where=list(where),
        output=output, tier=tier, max_turns=max_turns,
        model=model, dry_run=dry_run, debug=debug,
    )
    result = execute_prd_pipeline(config)
    _print_summary(result)
    sys.exit(0 if result.outcome == "success" else 1)

@prd_group.command("resume")
@click.argument("step_id")
@click.option("--max-turns", default=150, type=int)
@click.option("--debug", is_flag=True)
def resume(step_id, max_turns, debug):
    """Resume a halted PRD pipeline from a specific step."""
    config = build_resume_config(step_id=step_id, max_turns=max_turns, debug=debug)
    result = execute_prd_pipeline(config)
    _print_summary(result)
    sys.exit(0 if result.outcome == "success" else 1)
```

---

## 7. Prompt Builders

Prompts collectively exceed 300 lines. See companion file `portify-prompts.md`.

---

## 8. Phase 0 Prerequisites

### Modified Files (integration only)

| File | Change |
|------|--------|
| `src/superclaude/cli/main.py` | Add `from superclaude.cli.prd.commands import prd_group; app.add_command(prd_group)` |
| `pyproject.toml` | No change needed (cli entry point already registered) |

### Verified Pipeline Primitives

| Primitive | Path | Status |
|-----------|------|--------|
| `PipelineConfig` | `src/superclaude/cli/pipeline/models.py` | Exists, verified |
| `Step` | `src/superclaude/cli/pipeline/models.py` | Exists, verified |
| `StepResult` | `src/superclaude/cli/pipeline/models.py` | Exists, verified |
| `GateCriteria` | `src/superclaude/cli/pipeline/models.py` | Exists, verified |
| `SemanticCheck` | `src/superclaude/cli/pipeline/models.py` | Exists, verified |
| `GateMode` | `src/superclaude/cli/pipeline/models.py` | Exists, verified |
| `gate_passed()` | `src/superclaude/cli/pipeline/gates.py` | Exists, verified |
| `ClaudeProcess` | `src/superclaude/cli/pipeline/process.py` | Exists (sprint extends it) |
| `TurnLedger` | `src/superclaude/cli/sprint/models.py` | Exists, verified |
| `SignalHandler` | `src/superclaude/cli/sprint/process.py` | Exists (sprint-specific) |
