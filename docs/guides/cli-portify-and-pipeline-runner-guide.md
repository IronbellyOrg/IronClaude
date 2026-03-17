# CLI Portify & Pipeline Runner Guide

## Table of Contents

1. [What is CLI Portify?](#1-what-is-cli-portify)
2. [Architecture Overview](#2-architecture-overview)
3. [The Three Layers](#3-the-three-layers)
4. [Shared Pipeline Foundation](#4-shared-pipeline-foundation)
5. [Anatomy of a Portified CLI Runner](#5-anatomy-of-a-portified-cli-runner)
6. [Existing Runners Reference](#6-existing-runners-reference)
7. [Using the CLI Portify Runner](#7-using-the-cli-portify-runner)
8. [How to Port `sc:tasklist` to a CLI Runner](#8-how-to-port-sctasklist-to-a-cli-runner)

---

## 1. What is CLI Portify?

CLI Portify is a **workflow-to-pipeline compiler**. It takes an inference-driven SuperClaude workflow (a slash command + skill + agents) and converts it into a **deterministic CLI pipeline** where:

- **Python controls flow** — step ordering, retry, resume, parallelism
- **Claude fills structured artifacts** — each step is an isolated `claude -p` subprocess
- **Gates validate outputs** — pure Python checks (no LLM) between steps
- **Claude never decides "what runs next"** — the executor does

The core value proposition: **repeatability and reliability**. An inference-based workflow like `/sc:roadmap` might produce different results each run and can't be resumed. A portified CLI runner like `superclaude roadmap run spec.md` produces consistent artifacts, validates them with gates, and supports `--resume` and `--dry-run`.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  SLASH COMMAND LAYER                      │
│  /sc:cli-portify  — triggers the portification process   │
│  /sc:roadmap      — inference-based workflow (source)     │
│  /sc:tasklist     — inference-based workflow (source)     │
└───────────────────────────┬─────────────────────────────┘
                            │ portifies into
┌───────────────────────────▼─────────────────────────────┐
│                  SKILL PROTOCOL LAYER                     │
│  sc-cli-portify-protocol — 4-phase spec generation       │
│    Phase 1: Workflow Analysis                             │
│    Phase 2: Pipeline Specification                        │
│    Phase 3: Release Spec Synthesis                        │
│    Phase 4: Spec Panel Review                             │
└───────────────────────────┬─────────────────────────────┘
                            │ produces release spec, which guides
┌───────────────────────────▼─────────────────────────────┐
│                  CLI RUNNER LAYER                         │
│  src/superclaude/cli/roadmap/    — 9-step pipeline       │
│  src/superclaude/cli/tasklist/   — 1-step validator       │
│  src/superclaude/cli/sprint/     — phase-based executor   │
│  src/superclaude/cli/cli_portify/— meta-pipeline itself   │
│                                                           │
│  All built on: src/superclaude/cli/pipeline/ (shared)     │
└─────────────────────────────────────────────────────────┘
```

---

## 3. The Three Layers

### Layer 1: Slash Command (`src/superclaude/commands/cli-portify.md`)

The command definition handles:
- Input validation (workflow path, ambiguity, output writability)
- CLI name derivation (strips `sc-` and `-protocol`)
- Activating the skill protocol

### Layer 2: Skill Protocol (`src/superclaude/skills/sc-cli-portify-protocol/`)

A 4-phase process that produces a reviewed release specification:

| Phase | Name | Output |
|-------|------|--------|
| 1 | Workflow Analysis | `portify-analysis.md` — component inventory, step decomposition, programmatic spectrum |
| 2 | Pipeline Specification | `portify-spec.md` — step graph, models, prompts, gates, executor design |
| 3 | Release Spec Synthesis | `portify-release-spec.md` — full release spec with zero placeholders |
| 4 | Spec Panel Review | Reviewed spec + `panel-report.md` — convergence loop until score >= 7.0 |

Key reference files:
- `refs/analysis-protocol.md` — discovery rules, step decomposition, programmatic spectrum
- `refs/pipeline-spec.md` — gate tiers, prompt patterns, executor design, resume semantics

### Layer 3: CLI Runner (`src/superclaude/cli/cli_portify/`)

The actual Python implementation that orchestrates the above phases as a CLI pipeline:

```
superclaude cli-portify run sc:roadmap
superclaude cli-portify run sc:roadmap --dry-run
superclaude cli-portify run sc:roadmap --output ./out --max-turns 100
superclaude cli-portify run sc:roadmap --resume step-graph-design
```

---

## 4. Shared Pipeline Foundation

All CLI runners are built on `src/superclaude/cli/pipeline/`. This is the most important module to understand.

### Core Data Models (`pipeline/models.py`)

```python
class StepStatus(Enum):
    PENDING, PASS, FAIL, TIMEOUT, CANCELLED, SKIPPED

class GateMode(Enum):
    BLOCKING   # Step must pass before next step begins (default)
    TRAILING   # Step runs but doesn't block; failures evaluated later

@dataclass
class SemanticCheck:
    name: str                              # Human-readable check name
    check_fn: Callable[[str], bool]        # Pure Python check on file content
    failure_message: str                   # Message on failure

@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str] # YAML frontmatter keys to require
    min_lines: int                         # Minimum output line count
    enforcement_tier: "STRICT"|"STANDARD"|"LIGHT"|"EXEMPT"
    semantic_checks: list[SemanticCheck]   # Additional pure-Python checks

@dataclass
class Step:
    id: str                    # Unique step identifier
    prompt: str                # Full prompt text sent to Claude
    output_file: Path          # Where Claude writes its output
    gate: GateCriteria | None  # Validation criteria (None = no gate)
    timeout_seconds: int       # Subprocess timeout
    inputs: list[Path]         # Input files to embed in prompt
    retry_limit: int           # Number of retries on gate failure (default: 1)
    model: str                 # Model override (empty = default)
    gate_mode: GateMode        # BLOCKING or TRAILING

@dataclass
class PipelineConfig:
    work_dir: Path             # Working directory
    dry_run: bool              # Skip subprocess execution
    max_turns: int             # Max Claude agent turns per subprocess
    model: str                 # Default model
    permission_flag: str       # Default: --dangerously-skip-permissions
    debug: bool
    grace_period: int          # Trailing gate grace period (0 = force BLOCKING)
```

### Gate Enforcement Tiers (`pipeline/gates.py`)

```
EXEMPT   → always passes (no checks)
LIGHT    → file exists + non-empty
STANDARD → + min lines + YAML frontmatter field validation
STRICT   → + semantic checks (custom Python functions)
```

Gate validation is **pure Python** — no LLM invocation. It reads the output file and checks:
1. File exists and is non-empty
2. Line count meets minimum
3. Required YAML frontmatter fields present
4. Semantic check functions return `True`

### Pipeline Executor (`pipeline/executor.py`)

```python
def execute_pipeline(
    steps: list[Step | list[Step]],     # Sequential steps OR parallel groups
    config: PipelineConfig,
    run_step: StepRunner,               # Callable that runs one subprocess
    on_step_start: Callable,            # Callback: step starting
    on_step_complete: Callable,         # Callback: step finished
    on_state_update: Callable,          # Callback: state changed
    cancel_check: Callable,             # External cancellation signal
    trailing_runner: TrailingGateRunner, # For TRAILING mode gates
) -> list[StepResult]:
```

The executor handles:
- **Sequential steps**: Execute one at a time, halt on failure
- **Parallel groups**: `list[Step]` items run concurrently via threads, cross-cancel on failure
- **Retry logic**: On gate failure, retry up to `retry_limit` times
- **Trailing gates**: Submit to background runner, sync at pipeline end
- **State tracking**: Build state dict after each step for persistence

### Claude Process (`pipeline/process.py`)

```python
class ClaudeProcess:
    def __init__(self, *, prompt, output_file, error_file, max_turns,
                 model, permission_flag, timeout_seconds, output_format,
                 extra_args, env_vars):
        ...

    def build_command(self) -> list[str]:
        # Returns: claude --print --verbose --dangerously-skip-permissions
        #          --no-session-persistence --tools default
        #          --max-turns N --output-format text -p "prompt"
        ...

    def start(self) -> subprocess.Popen:  # Launch subprocess
    def wait(self) -> int:                 # Wait with timeout, return exit code
    def terminate(self):                   # Graceful SIGTERM → SIGKILL
```

Key design decisions:
- `--no-session-persistence` — each step is isolated
- `--output-format text` — plain text for gate-compatible output
- `stdout` → output file, `stderr` → error file
- Process groups via `os.setpgrp` for clean tree kills
- Strips `CLAUDECODE` env var to prevent nested session detection

---

## 5. Anatomy of a Portified CLI Runner

Every portified CLI runner follows this 7-module pattern:

```
src/superclaude/cli/<runner>/
├── __init__.py          # Package init, exports command group
├── commands.py          # Click command definitions (CLI surface)
├── models.py            # Config dataclass extending PipelineConfig
├── prompts.py           # Pure functions returning prompt strings
├── gates.py             # GateCriteria + SemanticCheck definitions
├── executor.py          # Builds Step list, defines StepRunner, calls execute_pipeline
└── (optional extras)    # process.py, monitor.py, tui.py, etc.
```

### Module Responsibilities

| Module | Purpose | Rules |
|--------|---------|-------|
| `commands.py` | Click command group + options | Lazy-imports executor; no business logic |
| `models.py` | `@dataclass` extending `PipelineConfig` | Add workflow-specific fields (paths, flags) |
| `prompts.py` | Pure functions → `str` | No I/O, no subprocess, no side effects (NFR-004) |
| `gates.py` | `GateCriteria` constants | Pure data + check functions; no pipeline imports (NFR-005) |
| `executor.py` | Step graph + `StepRunner` + orchestration | Imports from `pipeline/`; calls `execute_pipeline()` |

### Step-by-Step: How to Build a Runner

**1. Define your Config** (`models.py`):
```python
from ..pipeline.models import PipelineConfig

@dataclass
class MyConfig(PipelineConfig):
    input_file: Path = field(default_factory=lambda: Path("."))
    output_dir: Path = field(default_factory=lambda: Path("."))
    # ... workflow-specific fields
```

**2. Write your Prompts** (`prompts.py`):
```python
def build_step_one_prompt(input_file: Path) -> str:
    return (
        "You are a specialist...\n\n"
        "## Instructions\n\n"
        "Read the input and produce...\n\n"
        "## Output Requirements\n\n"
        "Your output MUST begin with YAML frontmatter:\n"
        "- field_a: ...\n"
        "- field_b: ...\n"
    )
```

**3. Define your Gates** (`gates.py`):
```python
from ..pipeline.models import GateCriteria, SemanticCheck

def _check_custom_field(content: str) -> bool:
    """Return True if content passes the semantic check."""
    return "expected_pattern" in content

MY_GATE = GateCriteria(
    required_frontmatter_fields=["field_a", "field_b"],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="custom_check",
            check_fn=_check_custom_field,
            failure_message="field_a must contain expected_pattern",
        ),
    ],
)
```

**4. Build the Step Graph and StepRunner** (`executor.py`):
```python
from ..pipeline.executor import execute_pipeline
from ..pipeline.models import Step, StepResult, StepStatus, PipelineConfig
from ..pipeline.process import ClaudeProcess

def my_run_step(step, config, cancel_check) -> StepResult:
    """Execute a single step as a Claude subprocess."""
    # Embed inputs into prompt
    embedded = _embed_inputs(step.inputs)
    effective_prompt = step.prompt + "\n\n" + embedded if embedded else step.prompt

    proc = ClaudeProcess(
        prompt=effective_prompt,
        output_file=step.output_file,
        error_file=step.output_file.with_suffix(".err"),
        max_turns=config.max_turns,
        model=step.model or config.model,
        permission_flag=config.permission_flag,
        timeout_seconds=step.timeout_seconds,
        output_format="text",
    )
    proc.start()
    # ... wait loop with cancel_check ...
    exit_code = proc.wait()
    # ... return StepResult based on exit_code ...

def _build_steps(config: MyConfig) -> list[Step | list[Step]]:
    """Build the step graph."""
    return [
        # Sequential step
        Step(
            id="step-one",
            prompt=build_step_one_prompt(config.input_file),
            output_file=config.output_dir / "step-one.md",
            gate=MY_GATE,
            timeout_seconds=600,
            inputs=[config.input_file],
        ),
        # Parallel group (list of Steps)
        [
            Step(id="step-two-a", ...),
            Step(id="step-two-b", ...),
        ],
        # Sequential step that depends on parallel group
        Step(id="step-three", ...),
    ]

def execute_my_pipeline(config: MyConfig) -> bool:
    steps = _build_steps(config)
    results = execute_pipeline(
        steps=steps,
        config=config,
        run_step=my_run_step,
    )
    return all(r.status == StepStatus.PASS for r in results)
```

**5. Wire up the CLI** (`commands.py`):
```python
import click

@click.group("my-runner")
def my_group():
    """My pipeline runner."""
    pass

@my_group.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "output_dir", type=click.Path(path_type=Path))
@click.option("--model", default="")
@click.option("--max-turns", type=int, default=100)
@click.option("--dry-run", is_flag=True)
@click.option("--debug", is_flag=True)
def run(input_file, output_dir, model, max_turns, dry_run, debug):
    """Run the pipeline on INPUT_FILE."""
    from .executor import execute_my_pipeline
    from .models import MyConfig

    config = MyConfig(
        input_file=input_file.resolve(),
        output_dir=(output_dir or input_file.parent).resolve(),
        max_turns=max_turns,
        model=model,
        dry_run=dry_run,
        debug=debug,
    )
    passed = execute_my_pipeline(config)
    sys.exit(0 if passed else 1)
```

**6. Register in `main.py`**:
```python
from superclaude.cli.my_runner.commands import my_group
main.add_command(my_group, name="my-runner")
```

---

## 6. Existing Runners Reference

### Roadmap Runner (`superclaude roadmap run`)

The most complete example. 9-step pipeline with parallel groups:

```
extract → [generate-A, generate-B] → diff → debate → score → merge
→ test-strategy → spec-fidelity → (certify)
```

- **Parallel generation**: Two agents generate roadmaps concurrently
- **Adversarial pipeline**: diff → debate → score → merge
- **Validation**: test-strategy and spec-fidelity gates
- **Resume**: `.roadmap-state.json` tracks step completion; `--resume` skips passing steps
- **10 gate definitions** in `gates.py`
- **8 prompt builders** in `prompts.py`

CLI surface:
```bash
superclaude roadmap run spec.md
superclaude roadmap run spec.md --agents opus:architect,haiku:security
superclaude roadmap run spec.md --depth deep --resume
superclaude roadmap run spec.md --dry-run
superclaude roadmap validate ./output
superclaude roadmap accept-spec-change ./output
```

### Tasklist Validator (`superclaude tasklist validate`)

The simplest example. Single-step validation pipeline:

```
tasklist-fidelity (STRICT gate)
```

- **One step**: Compares roadmap against tasklist files
- **Inline embedding**: Reads all input files and embeds them directly in the prompt
- **STRICT gate**: Requires YAML frontmatter with severity counts + semantic checks
- **Exit code**: 0 = no HIGH severity, 1 = HIGH severity found

CLI surface:
```bash
superclaude tasklist validate ./output
superclaude tasklist validate ./output --roadmap-file roadmap.md
```

### Sprint Runner (`superclaude sprint run`)

Phase-oriented execution with TUI monitoring:

- **Discovers phases** from `tasklist-index.md` file
- **Phase-based execution** rather than flat step list
- **TUI dashboard** for live monitoring
- **tmux support** for parallel sessions

### CLI Portify Runner (`superclaude cli-portify run`)

Meta-pipeline — portifies other workflows:

```
validate-config → discover-components → analyze-workflow → design-pipeline
→ synthesize-spec → brainstorm-gaps → panel-review
```

- **7 concrete steps** mapping to the 4-phase protocol
- **Convergence engine** for panel review loops
- **Resume support** via step IDs

---

## 7. Using the CLI Portify Runner

### Basic Usage

```bash
# Portify a workflow by skill name
superclaude cli-portify run sc:roadmap

# Portify by skill directory path
superclaude cli-portify run ~/.claude/skills/sc-roadmap-protocol

# Dry run (analysis + specification only, no synthesis/review)
superclaude cli-portify run sc:tasklist --dry-run

# Custom output directory
superclaude cli-portify run sc:tasklist --output ./portify-output

# Resume from a specific step
superclaude cli-portify run sc:tasklist --resume synthesize-spec

# Debug mode
superclaude cli-portify run sc:tasklist --debug --max-turns 150
```

### Options Reference

| Option | Default | Description |
|--------|---------|-------------|
| `WORKFLOW` | (required) | Skill name, `sc:name`, or path to skill directory |
| `--name` | auto-derived | Override CLI name for the portified pipeline |
| `--output` | alongside workflow | Output directory for generated artifacts |
| `--max-turns` | 200 | Maximum Claude agent turns per step |
| `--model` | env default | Claude model override |
| `--dry-run` | false | Execute only prereq/analysis/review/spec steps |
| `--resume STEP_ID` | none | Resume from a specific pipeline step |
| `--debug` | false | Enable debug logging |

### What It Produces

The pipeline generates these artifacts in the output directory:

1. **`portify-analysis.md`** — Component inventory, step decomposition, programmatic spectrum
2. **`portify-spec.md`** — Pipeline specification with step graph, models, prompts, gates
3. **`synthesized-spec.md`** / **`portify-release-spec.md`** — Full release specification
4. **`brainstorm-gaps.md`** — Gap analysis across architect/analyzer/backend perspectives
5. **`panel-review.md`** / **`panel-report.md`** — Reviewed spec with quality scores

### What to Do With the Output

The portify runner produces a **release specification**, not code. To implement the actual CLI runner:

1. Read `portify-release-spec.md` for the complete design
2. Create `src/superclaude/cli/<runner>/` following the 7-module pattern
3. Implement each module per the spec: models, prompts, gates, executor, commands
4. Register in `main.py`
5. Add tests

---

## 8. How to Port `sc:tasklist` to a CLI Runner

The `sc:tasklist` skill (`src/superclaude/skills/sc-tasklist-protocol/`) is a deterministic roadmap-to-tasklist generator. Here's how to port it using the CLI portify runner.

### Step 1: Run CLI Portify Against sc:tasklist

```bash
# Create output directory
mkdir -p docs/generated/portify-tasklist

# Run the portification pipeline
superclaude cli-portify run sc:tasklist \
  --output docs/generated/portify-tasklist \
  --name tasklist-generate \
  --max-turns 200
```

This will:
1. Discover the `sc-tasklist-protocol` skill, its templates, rules, and referenced agents
2. Analyze the workflow into discrete steps on the programmatic spectrum
3. Design a pipeline spec with step graph, gates, and prompts
4. Synthesize a reviewed release specification

### Step 2: Review the Release Spec

```bash
# Read the output
cat docs/generated/portify-tasklist/portify-release-spec.md
```

The spec will identify steps like:
- **Validate roadmap input** (programmatic — Python)
- **Generate phase files** from roadmap items (Claude subprocess)
- **Generate index file** from phase files (Claude subprocess)
- **Validate tier classification** (gate — Python)
- **Validate file emission rules** (gate — Python)

### Step 3: Implement the Runner

Create `src/superclaude/cli/tasklist_generate/` with:

```
src/superclaude/cli/tasklist_generate/
├── __init__.py
├── commands.py         # superclaude tasklist generate <roadmap> [options]
├── models.py           # TasklistGenerateConfig(PipelineConfig)
├── prompts.py          # build_phase_generation_prompt(), build_index_prompt()
├── gates.py            # PHASE_GATE, INDEX_GATE with tier classification checks
└── executor.py         # Step graph + tasklist_generate_run_step + execute_tasklist_generate
```

### Step 4: Alternative — Use Dry Run First

If you want to see what the portification would look like before committing:

```bash
# Dry run — produces analysis + spec only, no synthesis/review
superclaude cli-portify run sc:tasklist --dry-run --output /tmp/portify-preview
```

Review `portify-analysis.md` and `portify-spec.md` to validate the pipeline design before running the full portification.

### Step 5: Register the New Runner

After implementation, add to `src/superclaude/cli/main.py`:

```python
from superclaude.cli.tasklist_generate.commands import tasklist_generate_group
main.add_command(tasklist_generate_group, name="tasklist-generate")
```

Or extend the existing `tasklist` group:

```python
# In src/superclaude/cli/tasklist/commands.py
@tasklist_group.command()
@click.argument("roadmap_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output", ...)
def generate(roadmap_file, output, ...):
    """Generate tasklist from a roadmap."""
    ...
```

### Quick Reference: The Pattern

```
1. superclaude cli-portify run sc:tasklist --output ./portify-out
2. Review portify-out/portify-release-spec.md
3. Create src/superclaude/cli/tasklist_generate/ (7 modules)
4. Build Step objects in executor.py using prompts from the skill's templates
5. Define gates using the skill's rules (tier classification, file emission)
6. Wire up Click commands
7. Register in main.py
8. Test: superclaude tasklist generate roadmap.md --dry-run
```

---

## Appendix: Key File Locations

| Component | Path |
|-----------|------|
| Shared pipeline models | `src/superclaude/cli/pipeline/models.py` |
| Shared pipeline executor | `src/superclaude/cli/pipeline/executor.py` |
| Shared Claude process | `src/superclaude/cli/pipeline/process.py` |
| Shared gate validation | `src/superclaude/cli/pipeline/gates.py` |
| CLI Portify command | `src/superclaude/commands/cli-portify.md` |
| CLI Portify skill | `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` |
| CLI Portify runner | `src/superclaude/cli/cli_portify/` |
| Roadmap runner | `src/superclaude/cli/roadmap/` |
| Tasklist validator | `src/superclaude/cli/tasklist/` |
| Sprint runner | `src/superclaude/cli/sprint/` |
| CLI registration | `src/superclaude/cli/main.py` |
| sc:tasklist skill | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` |
| sc:tasklist templates | `src/superclaude/skills/sc-tasklist-protocol/templates/` |
| sc:tasklist rules | `src/superclaude/skills/sc-tasklist-protocol/rules/` |
