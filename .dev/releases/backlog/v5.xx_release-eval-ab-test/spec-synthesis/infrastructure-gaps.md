---
title: "Infrastructure Gap Analysis: Eval CLI Tool"
date: 2026-03-19
source_documents:
  - src/superclaude/cli/roadmap/executor.py
  - src/superclaude/cli/roadmap/models.py
  - src/superclaude/cli/roadmap/gates.py
  - src/superclaude/cli/sprint/executor.py
  - src/superclaude/cli/sprint/models.py
  - src/superclaude/cli/pipeline/models.py
  - src/superclaude/cli/pipeline/process.py
  - src/superclaude/cli/pipeline/executor.py
  - src/superclaude/cli/pipeline/gates.py
  - src/superclaude/cli/pipeline/trailing_gate.py
  - src/superclaude/cli/main.py
  - scripts/eval_runner.py
  - .dev/releases/backlog/v5.xx_release-eval-ab-test/conversation-decisions.md
extraction_type: infrastructure_gap
---

# Infrastructure Gap Analysis: Eval CLI Tool

## 0. Methodology

This analysis compares the seven-module layout specified in conversation-decisions.md section 5 (`models.py`, `rubric.py`, `judge.py`, `runner.py`, `isolation.py`, `aggregator.py`, `reporter.py`) against every existing pattern, reusable function, and integration point in the codebase. Each claim cites exact file paths and line ranges. No module is marked "simple" without justification.

---

## 1. Existing Patterns the Eval CLI Should Follow

### 1.1 Step Execution: `roadmap_run_step` (roadmap/executor.py:219-353)

**Pattern**: A `StepRunner` callable conforming to the `StepRunner` Protocol defined in `pipeline/executor.py:25-43`. The protocol signature is `(step: Step, config: PipelineConfig, cancel_check: Callable[[], bool]) -> StepResult`. Each step has a `Step` dataclass (pipeline/models.py:78-89) with `id`, `prompt`, `output_file`, `gate`, `timeout_seconds`, `inputs`, `retry_limit`, `model`, `gate_mode`. The runner launches a subprocess, waits with timeout, and returns a `StepResult` with status/timing.

The generic `execute_pipeline()` in `pipeline/executor.py:46-137` handles step ordering (sequential and parallel groups via threading), retry logic (retry_limit+1 attempts), gate checking (blocking and trailing modes), cancellation propagation, and state update callbacks.

**How eval should mirror it**: The eval tool does NOT execute Claude subprocesses -- it runs `uv run pytest` via `subprocess.run()`. The `StepRunner` protocol is too tightly coupled to Claude CLI semantics. However, the eval tool should adopt:

1. The `Step`/`StepResult`/`StepStatus` vocabulary for structuring eval phases (setup, structural tests, functional tests, quality scoring, comparison, reporting).
2. The execution-loop pattern from `execute_pipeline()`: iterate steps, check gates between steps, halt on failure (fail-fast for structural layer, per conversation-decisions.md section 3).
3. The parallel dispatch pattern from `_run_parallel_steps()` (pipeline/executor.py:263-313) for running multiple eval variants concurrently.

**Key divergence**: Eval steps invoke `uv run pytest` (as the prototype in scripts/eval_runner.py:46-78 already does), not `claude -p` via `ClaudeProcess`. The subprocess interface is fundamentally different -- no `--max-turns`, `--output-format`, or `--model` flags; instead `--junit-xml`, `--tb`, `-q`.

### 1.2 Gate Checking: `gate_passed` + `GateCriteria` (pipeline/gates.py:20-74)

**Pattern**: `gate_passed(output_file: Path, criteria: GateCriteria) -> tuple[bool, str | None]` validates file content against tier-proportional checks:
- EXEMPT: always passes
- LIGHT: file exists + non-empty
- STANDARD: + min_lines + YAML frontmatter field presence
- STRICT: + semantic checks (pure `content -> bool` functions via `SemanticCheck` dataclass at pipeline/models.py:59-65)

Gate criteria are pure data definitions (no logic, no imports from consumer modules). The `GateCriteria` dataclass (pipeline/models.py:68-74) holds `required_frontmatter_fields`, `min_lines`, `enforcement_tier`, and `semantic_checks`.

Frontmatter validation uses `_check_frontmatter()` (pipeline/gates.py:83-116) with a regex `_FRONTMATTER_RE` (line 77-80) that discovers frontmatter anywhere in the document, rejecting horizontal rules.

**How eval should mirror it**: Define eval-specific `GateCriteria` instances to validate:
- JUnit XML output files (file exists, parses as valid XML, contains `<testsuite>` elements with non-zero `tests` attribute)
- Comparison report files (YAML frontmatter with required fields like `consistency_identical`, `regressions_count`, `verdict`)
- Scores JSONL files (each line parses as valid JSON with required keys)

The semantic check pattern is directly reusable: define pure functions like `_xml_has_testcases(content: str) -> bool` and register them on `GateCriteria` instances.

### 1.3 State Management: `read_state`/`write_state` (roadmap/executor.py:1151-1171)

**Pattern**: `write_state(state: dict, path: Path)` writes JSON atomically via `tmp = path.with_suffix(".tmp")` then `os.replace(str(tmp), str(path))`. `read_state(path: Path) -> dict | None` handles missing files (returns None), empty files (returns None), and malformed JSON (returns None via `json.JSONDecodeError` catch). State schema includes `schema_version`, step statuses, timestamps, and pipeline-specific metadata.

State is persisted to `.roadmap-state.json` at `config.output_dir / ".roadmap-state.json"` (roadmap/executor.py:907). State merging logic (lines 969-974) preserves steps from previous runs that were not re-executed in the current run.

**How eval should mirror it**: An `.eval-state.json` file tracking:
- `schema_version`: integer for forward compatibility
- `eval_files`: list of test file paths
- `variants`: list of variant configs (name, branch, worktree_path)
- `runs`: dict of run_id -> {status, passed, failed, skipped, errors, duration, xml_path, started_at, finished_at}
- `comparison`: latest comparison result
- `last_run`: ISO timestamp

The atomic write pattern should be reused directly. These functions should be extracted to `pipeline/state.py` since both roadmap and eval need them, and they have zero consumer-specific logic.

### 1.4 Subprocess Management: `ClaudeProcess` (pipeline/process.py:24-203)

**Pattern**: Manages lifecycle of a `claude -p` subprocess:
- `build_command()` (line 71-91): constructs argv with `--print`, `--verbose`, `--no-session-persistence`, `--tools default`, `--max-turns`, `--output-format`, `-p <prompt>`
- `build_env()` (line 93-108): copies `os.environ`, strips `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` to prevent nested-session detection, merges caller-provided `env_vars`
- `start()` (line 110-137): opens stdout/stderr file handles, Popen with `stdin=DEVNULL`, optional `preexec_fn=os.setpgrp` for process group management, lifecycle hook `on_spawn`
- `wait()` (line 139-151): waits with `timeout_seconds`, returns 124 on `TimeoutExpired`, lifecycle hook `on_exit`
- `terminate()` (line 153-192): SIGTERM to process group, wait 10s, then SIGKILL; lifecycle hook `on_signal`

**How eval should mirror it**: The eval tool runs `uv run pytest`, not `claude -p`. `ClaudeProcess` is too specialized -- its `build_command()` produces Claude-specific flags. Options:

1. **For pytest runs**: Use `subprocess.run()` directly (as scripts/eval_runner.py:48-56 already does). The call is simple enough that a wrapper class adds unnecessary abstraction.
2. **For judge agent runs**: `ClaudeProcess` is directly usable. The judge is a single `claude -p` invocation with `output_format="text"` (per conversation-decisions.md section 5, `judge.py`).

### 1.5 Convergence and Reporting: `AggregatedPhaseReport` (sprint/executor.py:189-293)

**Pattern**: Runner-constructed reports (not agent self-reported) with `to_yaml()` and `to_markdown()` methods. YAML frontmatter with status/counts/duration, followed by markdown tables and summary statistics. `aggregate_task_results()` function (sprint/executor.py:295-334) computes counts from raw `TaskResult` lists.

**How eval should mirror it**: The eval `reporter.py` should follow this exact pattern:
- Accept raw `RunResult` lists
- Compute aggregate statistics (mean, stddev, min, max per scoring dimension)
- Produce YAML frontmatter + markdown body
- Include per-run detail tables and per-model breakdowns

### 1.6 Resume/Skip Logic: `_apply_resume` (roadmap/executor.py:1782-1874)

**Pattern**: On `--resume`, iterates all steps and checks each step's output against its gate criteria via `_step_needs_rerun()` (lines 1725-1779). Steps whose outputs already pass gates are skipped. Dependency tracking via `dirty_outputs: set[Path]` ensures that if any step is re-run, all downstream steps depending on its output are also re-run. Parallel groups are treated atomically: if any member needs re-run, the entire group re-runs.

**How eval should mirror it**: Eval runs are inherently idempotent (running pytest again produces new results). Resume logic is less relevant -- instead, the eval tool should support `--reuse-runs` to skip re-execution when JUnit XML files already exist and are fresh (mtime check against eval config mtime). This is simpler than the roadmap pattern but follows the same "check output freshness, skip if valid" principle.

---

## 2. Existing Code That Can Be Directly Reused

### 2.1 Base Types from `pipeline/models.py`

| Symbol | Lines | Reuse Strategy |
|--------|-------|----------------|
| `PipelineConfig` | 170-180 | Inherit: `EvalConfig(PipelineConfig)` adds eval-specific fields |
| `StepStatus` | 17-44 | Direct import: PENDING, PASS, FAIL, TIMEOUT, CANCELLED, SKIPPED |
| `StepResult` | 93-105 | Direct import: timing, status, gate_failure_reason |
| `GateCriteria` | 68-74 | Direct import: define eval-specific gate criteria instances |
| `SemanticCheck` | 59-65 | Direct import: register eval-specific content validators |
| `GateMode` | 46-55 | Direct import: BLOCKING for fail-fast structural gates |

### 2.2 Gate Validation from `pipeline/gates.py`

| Symbol | Lines | Reuse Strategy |
|--------|-------|----------------|
| `gate_passed()` | 20-74 | Direct import: validate eval output files against criteria |
| `_check_frontmatter()` | 83-116 | Internal use via `gate_passed()` |
| `_FRONTMATTER_RE` | 77-80 | Internal use via `gate_passed()` |

### 2.3 State Persistence from `roadmap/executor.py`

| Symbol | Lines | Reuse Strategy |
|--------|-------|----------------|
| `write_state()` | 1151-1158 | Extract to `pipeline/state.py` for shared use |
| `read_state()` | 1161-1171 | Extract to `pipeline/state.py` for shared use |

These functions are generic (dict -> JSON -> file, file -> JSON -> dict) with zero roadmap-specific logic. Extraction is a pure mechanical move with import path updates in `roadmap/executor.py`.

### 2.4 Frontmatter Parsing from `roadmap/gates.py`

| Symbol | Lines | Reuse Strategy |
|--------|-------|----------------|
| `_parse_frontmatter()` | 139-160 | Consider extracting to `pipeline/gates.py` or a shared utility |
| `_strip_yaml_quotes()` | 121-136 | Used by `_parse_frontmatter()` |

The roadmap-level `_parse_frontmatter()` is more featureful than the pipeline-level `_check_frontmatter()` -- it returns a `dict[str, str]` of key-value pairs instead of just checking field presence. The eval comparator and reporter may need to read values from frontmatter, not just check for field presence.

### 2.5 Atomic File Write Pattern

Used in multiple locations:
- `roadmap/executor.py:112-114` (`_sanitize_output`): `tmp_file.write_text(); os.replace(tmp_file, output_file)`
- `roadmap/executor.py:1156-1158` (`write_state`): `tmp.write_text(); _os.replace(str(tmp), str(path))`

Pattern: `path.with_suffix(path.suffix + ".tmp")` or `path.with_suffix(".tmp")`, write to tmp, then `os.replace(tmp, path)`. This ensures no partial file states on crash.

### 2.6 Prototype Code from `scripts/eval_runner.py`

| Symbol | Lines | Reuse Strategy |
|--------|-------|----------------|
| `RunResult` dataclass | 34-43 | Refactor into `eval/models.py` as `EvalRunResult` with additional fields |
| `run_pytest()` | 46-78 | Refactor into `eval/runner.py` with isolation integration and error handling |
| `run_local()` | 81-85 | Absorb into `eval/runner.py:execute_eval()` |
| `run_global()` | 88-112 | Absorb into `eval/runner.py:execute_eval()` with worktree management |
| `compare_runs()` | 115-163 | Refactor into `eval/aggregator.py` with richer statistics |
| `print_report()` | 166-197 | Refactor into `eval/reporter.py` with YAML frontmatter and markdown output |
| `EVAL_FILES` list | 22-28 | Move to config parameter (not hardcoded) |
| `RESULTS_DIR` | 31 | Derive from config `output_dir` |

### 2.7 Statistical Analysis from `scripts/ab_test_workflows.py`

| Symbol | Line | Reuse Strategy |
|--------|------|----------------|
| `ABTestAnalyzer` | 23+ | Extract t-test, effect size (Cohen's d), winner determination into `eval/aggregator.py` |

### 2.8 ClaudeProcess for Judge Agent

| Symbol | Lines | Reuse Strategy |
|--------|-------|----------------|
| `ClaudeProcess` | pipeline/process.py:24-203 | Direct import for judge agent subprocess |

The judge agent is a single `claude -p` call. ClaudeProcess handles the entire lifecycle including timeout, signal handling, and process group management.

### 2.9 Parallel Execution from `pipeline/executor.py`

| Symbol | Lines | Reuse Strategy |
|--------|-------|----------------|
| `_run_parallel_steps()` | 263-313 | Reference pattern for parallel variant execution |

The threading pattern with cross-cancellation via `threading.Event` and `daemon=True` threads is reusable for running multiple eval variants in parallel. However, the eval tool may choose `concurrent.futures.ProcessPoolExecutor` instead for better isolation between pytest processes.

---

## 3. New Modules Required for `src/superclaude/eval/`

The section 5 layout from conversation-decisions.md specifies seven modules. Below is the analysis for each.

### 3.1 `models.py` -- Data Models

**Responsibility**: Define all dataclasses for the eval system. Maps to conversation-decisions.md section 6 data model.

**Interface** (from section 6, adapted to codebase conventions):

```python
@dataclass
class Score:
    dimension: str          # structure|completeness|accuracy|actionability|efficiency
    value: float            # 1.0 - 10.0
    hard_fail: bool         # True = binary failure (structural/functional layers)
    reasoning: str          # Judge's explanation

@dataclass
class RunResult:
    test_id: str
    run_number: int
    model: str
    scores: list[Score]
    exit_code: int
    tokens_used: int
    wall_time_seconds: float
    artifacts: list[str]
    stdout_path: Path       # path, not content (avoid memory bloat)
    stderr_path: Path

@dataclass
class TestVerdict:
    test_id: str
    layer: str              # structural|functional|quality|regression
    passed: bool
    aggregate_scores: dict  # dimension -> {mean, stddev, min, max}
    runs: list[RunResult]

@dataclass
class EvalReport:
    release: str
    timestamp: str
    tests: list[TestVerdict]
    overall_passed: bool
    model_breakdown: dict   # model -> {dimension -> mean_score}
    recommendations: list[str]

@dataclass
class EvalConfig(PipelineConfig):
    eval_suite_path: Path           # path to eval-suite.yaml
    release_dir: Path               # release being evaluated
    output_dir: Path                # where to write results
    runs_per_test: int              # repetitions for variance measurement
    models: list[str]               # models to test against
    judge_model: str                # model for quality scoring
    timeout_per_run: int            # seconds per subprocess invocation
    fail_fast: bool                 # halt on first structural/functional failure
```

**Dependencies**: `pipeline/models.py` (PipelineConfig), dataclasses, pathlib, datetime
**Estimated complexity**: Medium -- many dataclasses but mostly mechanical. The Score/RunResult/TestVerdict/EvalReport hierarchy from section 6 is well-defined. Complexity comes from serialization (to_dict/from_dict) and JSONL round-trip support.
**Blocks**: All other eval modules

### 3.2 `rubric.py` -- Scoring Rubric

**Responsibility**: Define the 5-dimension scoring rubric with anchored definitions. Pure data, no LLM invocation.

**Interface**:

```python
@dataclass
class RubricDimension:
    name: str               # e.g., "completeness"
    description: str        # what this dimension measures
    anchors: dict[int, str] # score -> description (1, 3, 5, 7, 10)
    weight: float           # relative importance (default 1.0)

RUBRIC: list[RubricDimension]  # the 5 dimensions

def render_rubric_for_prompt() -> str:
    """Format rubric as text for judge agent prompt injection."""

def validate_scores(scores: list[Score]) -> list[str]:
    """Return list of validation errors (empty if valid)."""
```

**Dependencies**: models.py (Score)
**Estimated complexity**: Simple -- pure data definitions with string formatting. The rubric dimensions are specified in conversation-decisions.md section 3 (structure, completeness, accuracy, actionability, efficiency). Anchor definitions require domain knowledge but no code complexity.
**Blocks**: judge.py (needs rubric for prompt construction)

### 3.3 `judge.py` -- Judge Agent Integration

**Responsibility**: Invoke a Claude subprocess as a "judge" to evaluate qualitative aspects. Build the prompt, parse the response.

**Interface**:

```python
def build_judge_prompt(
    rubric: list[RubricDimension],
    test_output: str,
    test_context: dict,
) -> str:
    """Build structured prompt for judge scoring."""

def parse_judge_response(response: str) -> list[Score]:
    """Extract Score objects from judge output text."""

def run_judge(
    test_output_path: Path,
    rubric: list[RubricDimension],
    judge_model: str,
    output_file: Path,
    timeout_seconds: int = 300,
) -> list[Score]:
    """Full judge invocation: build prompt, run ClaudeProcess, parse response."""
```

**Dependencies**: `pipeline/process.py` (ClaudeProcess), models.py (Score), rubric.py (RubricDimension, render_rubric_for_prompt)
**Estimated complexity**: Medium -- prompt construction follows the pattern in `roadmap/prompts.py` (pure functions accepting data, returning strings). Response parsing is the tricky part: judge output is semi-structured text. Needs lenient parsing with fallback scores. The ClaudeProcess invocation itself is straightforward (see section 2.8).

Comparison to existing subprocess pattern: In `roadmap/executor.py:281-309`, `ClaudeProcess` is instantiated with prompt, output_file, error_file, max_turns, model, permission_flag, timeout_seconds, output_format. The judge agent follows the exact same pattern but with `output_format="text"` and lower `max_turns` (10-20 vs 100).

**Blocks**: Nothing (optional enhancement, gated behind `--judge` flag per conversation-decisions.md section 3)

### 3.4 `runner.py` -- Multi-Run Parallel Execution Engine

**Responsibility**: Execute eval test suites across multiple runs, models, and variants. Manage subprocess lifecycle for `uv run pytest` and `claude -p` invocations.

**Interface**:

```python
def execute_eval_suite(
    config: EvalConfig,
    on_run_start: Callable[[str, int], None] = lambda test_id, run_num: None,
    on_run_complete: Callable[[RunResult], None] = lambda r: None,
) -> list[RunResult]:
    """Run all tests across all configured models and repetitions."""

def run_single_test(
    test_id: str,
    run_number: int,
    model: str,
    eval_files: list[Path],
    cwd: Path,
    xml_output: Path,
    timeout: int,
    env_overrides: dict[str, str] | None = None,
) -> RunResult:
    """Execute a single pytest run and parse JUnit XML."""

def setup_worktree(branch: str, base_dir: Path) -> Path:
    """Create or reuse a git worktree for baseline evaluation."""

def teardown_worktree(worktree_path: Path) -> None:
    """Remove a git worktree after evaluation."""

def parse_junit_xml(xml_path: Path) -> tuple[int, int, int, int, list[str]]:
    """Parse JUnit XML: (passed, failed, skipped, errors, failure_names)."""
```

**Dependencies**: models.py (RunResult, EvalConfig), isolation.py (eval_isolation_context), subprocess, xml.etree.ElementTree, pathlib, tempfile, threading or concurrent.futures

**Estimated complexity**: Complex -- this is the core orchestration module. It must handle:
1. Parallel pytest invocations across worktrees (prototype exists in scripts/eval_runner.py:81-112)
2. JUnit XML parsing with error recovery (prototype exists in scripts/eval_runner.py:60-77)
3. Timeout enforcement per run (prototype uses `subprocess.run(timeout=120)` at line 55)
4. Integration with isolation.py for variant switching
5. Worktree creation/teardown lifecycle (prototype at scripts/eval_runner.py:93-98)
6. State persistence between runs for `--reuse-runs` support
7. Fail-fast behavior for structural/functional layers (per conversation-decisions.md section 3)

The prototype in scripts/eval_runner.py covers the happy path but lacks: error handling for worktree creation failures, state persistence, isolation integration, multi-model support, and configurable test file lists.

**Blocks**: CLI commands (the `run` subcommand)

### 3.5 `isolation.py` -- .claude/ Directory Toggling

**Responsibility**: Enable or disable `.claude/` directories (commands, skills, agents) to create clean vs enhanced variants for A/B comparison. Provide trap-safe restore on exit/error/SIGINT.

**Interface**:

```python
@dataclass
class EvalIsolation:
    """Manages .claude/ directory state for A/B eval runs."""
    original_path: Path           # ~/.claude or project .claude
    disabled_suffix: str          # ".disabled"
    _was_disabled: bool = False   # track state for restore

    def disable(self) -> None:
        """Rename .claude -> .claude.disabled. Idempotent."""

    def restore(self) -> None:
        """Rename .claude.disabled -> .claude. Idempotent."""

@contextmanager
def eval_isolation_context(
    variant_name: str,
    project_root: Path,
    disable_claude_dir: bool = False,
    env_overrides: dict[str, str] | None = None,
) -> Iterator[dict[str, str]]:
    """Context manager: setup isolation, yield env_vars, restore on exit.

    Uses atexit + signal handlers for trap-safe restore (AC-07).
    """
```

**Dependencies**: pathlib, shutil, contextlib, atexit, signal
**Estimated complexity**: Medium -- the directory rename itself is trivial but safety mechanisms add complexity:
1. **Trap-safe restore** (conversation-decisions.md AC-07): must handle SIGINT, SIGTERM, uncaught exceptions, and `atexit`. The `atexit` module plus `signal.signal()` handlers must all call `restore()`.
2. **Concurrent-access guards**: if two eval processes run simultaneously, both trying to rename `.claude/`, data loss occurs. Need either a lock file (`fcntl.flock`) or env-var-based isolation that avoids filesystem mutation entirely.
3. **Dry-run validation** (AC-08): `--dry-run` should verify isolation setup without executing any runs.

**Comparison to existing `IsolationLayers`** (sprint/executor.py:106-181): `IsolationLayers` uses env var overrides (`CLAUDE_WORK_DIR`, `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`) passed to `subprocess.Popen` via the `env` parameter. This is crash-safe by design -- no filesystem mutation. The eval isolation needs a different target (disabling `.claude/` commands/skills discovery) but should prefer the env-var approach where possible.

**Recommended approach**: Primary mechanism is **worktree isolation** (scripts/eval_runner.py:88-112) -- the "global" variant runs in a clean git worktree on `master` where `.claude/` does not contain SuperClaude-enhanced commands. Secondary mechanism is env-var overrides (set `CLAUDE_COMMANDS_DIR` to an empty directory). Directory rename is the fallback only when env-var overrides are insufficient.

**Blocks**: runner.py (must isolate before running)

### 3.6 `aggregator.py` -- Statistical Aggregation

**Responsibility**: Compute mean, stddev, p-values, effect size (Cohen's d), and within-model consistency metrics from multi-run results.

**Interface**:

```python
def aggregate_scores(
    runs: list[RunResult],
) -> dict[str, dict[str, float]]:
    """Per-dimension {mean, stddev, min, max, cv} across runs."""

def check_consistency(
    runs_a: list[RunResult],
    runs_b: list[RunResult],
) -> dict:
    """Check that repeated runs produce identical pass/fail outcomes.
    Returns {identical: bool, duration_variance_pct: float}."""

def compare_variants(
    variant_a_runs: list[RunResult],
    variant_b_runs: list[RunResult],
) -> dict:
    """A/B comparison: regressions, improvements, new_test_count, p_values, effect_sizes."""

def compute_verdict(
    test_verdicts: list[TestVerdict],
    min_scores: dict[str, float] | None = None,
) -> tuple[bool, list[str]]:
    """Overall PASS/FAIL verdict + list of reasons for failures."""
```

**Dependencies**: models.py (RunResult, TestVerdict, Score), statistics (stdlib), optionally scipy.stats for t-tests
**Estimated complexity**: Medium -- the statistical computations are straightforward (mean, stddev are stdlib; t-test is ~10 lines with scipy or ~30 lines manual). The complexity is in edge cases: zero runs, single run (no variance), identical results (division by zero in CV), and cross-model comparison semantics.

The prototype `compare_runs()` in scripts/eval_runner.py:115-163 covers consistency checking and A/B delta but lacks per-dimension scoring aggregation and statistical significance testing. The `ABTestAnalyzer` class in scripts/ab_test_workflows.py:23+ provides t-test and effect size computation that should be extracted here.

**Blocks**: reporter.py, CLI compare subcommand

### 3.7 `reporter.py` -- Report Generation

**Responsibility**: Produce `report.md` (human-readable summary with YAML frontmatter) and `scores.jsonl` (machine-readable per-run scores).

**Interface**:

```python
def generate_report(
    eval_report: EvalReport,
    output_path: Path,
) -> None:
    """Write report.md with YAML frontmatter + markdown body."""

def write_scores_jsonl(
    runs: list[RunResult],
    output_path: Path,
) -> None:
    """Write one JSON line per run with all scores."""

def format_model_breakdown(
    model_breakdown: dict,
) -> str:
    """Render per-model score table as markdown."""

def format_verdict_summary(
    overall_passed: bool,
    test_verdicts: list[TestVerdict],
    recommendations: list[str],
) -> str:
    """Render verdict section with pass/fail badges and recommendations."""
```

**Dependencies**: models.py (EvalReport, RunResult, TestVerdict, Score), json, pathlib
**Estimated complexity**: Medium -- follows the `AggregatedPhaseReport.to_markdown()` pattern (sprint/executor.py:254-292) with YAML frontmatter and markdown tables. The complexity is in formatting: per-model breakdowns, per-dimension score tables, variance annotations, and the verdict section with recommendations.

The output structure from conversation-decisions.md section 5:
```
<release-dir>/evals/runs/<timestamp>/
  structural/results.jsonl
  functional/<test-id>/run-N/
  quality/<test-id>/scores.jsonl
  regression/comparison.jsonl
  scores.jsonl
  report.md
```

**Blocks**: Nothing (leaf node, consumes aggregated data)

---

## 4. Integration Points

### 4.1 CLI Registration in `main.py`

**Current pattern** (src/superclaude/cli/main.py:354-372):

```python
from superclaude.cli.sprint import sprint_group
main.add_command(sprint_group, name="sprint")

from superclaude.cli.roadmap import roadmap_group
main.add_command(roadmap_group, name="roadmap")
```

Each pipeline is a Click group with subcommands (`run`, `validate`, etc.). Registration is a 2-line import + `add_command()`.

**Required addition**:

```python
from superclaude.cli.eval import eval_group
main.add_command(eval_group, name="release-eval")
```

And separately for A/B testing (conversation-decisions.md section 5 specifies two separate commands):

```python
from superclaude.cli.ab_test import ab_test_group
main.add_command(ab_test_group, name="ab-test")
```

**Effort**: 4 lines total. Trivial, but requires `eval/__init__.py` and `ab_test/__init__.py` to define the Click groups.

### 4.2 Shared Pipeline Infrastructure

The `pipeline/` package (28 files) serves both `sprint/` and `roadmap/` via zero-import-from-consumer design (NFR-007). The eval tool should import from `pipeline/` for:

| Module | What to Import | Used For |
|--------|---------------|----------|
| `pipeline/models.py` | PipelineConfig, StepStatus, GateCriteria, SemanticCheck | Base config, status tracking, gate definitions |
| `pipeline/gates.py` | gate_passed() | Validate eval output files against criteria |
| `pipeline/process.py` | ClaudeProcess | Judge agent subprocess (quality layer only) |
| `pipeline/trailing_gate.py` | (reference only) | Pattern for async eval in future CI integration |

The eval tool does NOT need:
- `pipeline/executor.py` -- eval orchestration is simpler (no retry, no parallel groups with cross-cancellation)
- `pipeline/deliverables.py` -- eval has no deliverable decomposition
- `pipeline/conflict_detector.py`, `dataflow_graph.py`, etc. -- roadmap-specific analysis passes

**Extraction needed**: `write_state()` and `read_state()` must move from `roadmap/executor.py` to `pipeline/state.py` (new file). Current consumers:
- `roadmap/executor.py`: 6 call sites (lines 808, 919, 1001, 1490, 1498, 1579)
- Sprint does not use these functions (it uses its own logging/state mechanisms)
- Eval would be the third consumer

### 4.3 Output Directory Conventions

**Roadmap** writes to `config.output_dir` (default: `.dev/releases/current/<release>/`):
```
<output_dir>/
  extraction.md
  roadmap-opus-architect.md
  roadmap-haiku-architect.md
  diff-analysis.md
  ...
  .roadmap-state.json
```

**Sprint** writes to `config.results_dir` (= `config.release_dir / "results"`):
```
<release_dir>/results/
  phase-1-output.txt
  phase-1-result.md
  ...
  debug.log
```

**Eval** should write to `<release_dir>/evals/` per conversation-decisions.md section 5:
```
<release_dir>/evals/
  eval-suite.yaml
  fixtures/
  runs/<timestamp>/
    structural/results.jsonl
    functional/<test-id>/run-N/
    quality/<test-id>/scores.jsonl
    regression/comparison.jsonl
    scores.jsonl
    report.md
  .eval-state.json
```

This convention keeps eval artifacts colocated with the release they evaluate (NFR-06 from conversation-decisions.md section 8) while avoiding collision with roadmap/sprint output directories.

### 4.4 State File Schema Comparison

**Roadmap state** (`.roadmap-state.json`):
```json
{
  "schema_version": 1,
  "spec_file": "...",
  "spec_hash": "sha256:...",
  "agents": [...],
  "depth": "standard",
  "last_run": "ISO-8601",
  "steps": { "step-id": { "status": "...", "attempt": 1, ... } },
  "validation": { "status": "pass" },
  "fidelity_status": "pass",
  "remediate": { ... },
  "certify": { ... }
}
```

**Eval state** (`.eval-state.json`, proposed):
```json
{
  "schema_version": 1,
  "eval_suite": "eval-suite.yaml",
  "release": "v2.25-cli-portify-cli",
  "last_run": "ISO-8601",
  "runs": {
    "run-id": {
      "variant": "local",
      "model": "claude-sonnet-4-6",
      "status": "PASS",
      "passed": 168,
      "failed": 0,
      "duration": 45.3,
      "xml_path": "runs/2026-03-19T.../local-A.xml"
    }
  },
  "comparison": {
    "consistency_identical": true,
    "regressions": [],
    "improvements": [],
    "verdict": "PASS"
  }
}
```

The schemas are structurally similar (versioned, timestamped, step/run-level detail) but domain-specific. No schema unification is needed.

---

## 5. Isolation Mechanism (.claude/ Toggling)

### 5.1 Existing Precedent: `IsolationLayers` (sprint/executor.py:106-181)

The sprint executor provides 4-layer subprocess isolation via environment variable overrides:

```python
@dataclass
class IsolationLayers:
    scoped_work_dir: Path       # CLAUDE_WORK_DIR
    git_boundary: Path          # GIT_CEILING_DIRECTORIES
    plugin_dir: Path            # CLAUDE_PLUGIN_DIR
    settings_dir: Path          # CLAUDE_SETTINGS_DIR

    @property
    def env_vars(self) -> dict[str, str]: ...
```

`setup_isolation()` (lines 149-181) creates empty directories under `config.results_dir / ".isolation"` and returns an `IsolationLayers` instance. The env_vars dict is merged into `subprocess.Popen` via `ClaudeProcess.build_env(env_vars=...)`.

Cleanup is handled by `shutil.rmtree(isolation_dir, ignore_errors=True)` in a `finally` block (sprint/executor.py:967).

### 5.2 What's Different for Eval Isolation

The eval tool needs a fundamentally different isolation target:

| Sprint Isolation | Eval Isolation |
|-----------------|----------------|
| Prevent cross-phase state leakage | Enable/disable SuperClaude framework |
| Working directory scoping | Branch-level code isolation |
| Plugin/settings isolation | Command/skill/agent discovery toggling |
| Same codebase, different env | Different codebase versions (via worktree) |

### 5.3 Implementation Approach (Three Layers)

**Layer 1 -- Worktree Isolation** (primary, already prototyped):

`scripts/eval_runner.py:88-112` creates a git worktree on `master` for the "global" (baseline) variant. The eval tool should generalize this:

```python
def setup_worktree(branch: str, base_dir: Path) -> Path:
    worktree_path = base_dir.parent / f"{base_dir.name}-eval-{branch}"
    if not worktree_path.exists():
        subprocess.run(
            ["git", "worktree", "add", str(worktree_path), branch],
            cwd=base_dir, check=True,
        )
    return worktree_path
```

This provides clean branch-level isolation: the "local" variant runs in the current repo (with current `.claude/` state), the "global" variant runs in a worktree on `master` (with whatever `.claude/` state exists on master).

**Layer 2 -- Env-Var Override** (supplementary):

For same-branch skill toggling (e.g., "run with SuperClaude skills disabled"), set `CLAUDE_COMMANDS_DIR` and `CLAUDE_SKILLS_DIR` to empty directories:

```python
def isolation_env_vars(disable_superclaude: bool = False) -> dict[str, str]:
    if not disable_superclaude:
        return {}
    empty_dir = Path(tempfile.mkdtemp(prefix="eval-isolation-"))
    return {
        "CLAUDE_COMMANDS_DIR": str(empty_dir),
        # Additional env vars TBD based on Claude Code discovery mechanism
    }
```

This follows the `IsolationLayers.env_vars` pattern and is crash-safe.

**Layer 3 -- Directory Rename** (fallback, high risk):

Only if env-var overrides are insufficient (Claude Code does not respect `CLAUDE_COMMANDS_DIR`):

```python
@contextmanager
def claude_dir_toggle(claude_dir: Path):
    disabled = claude_dir.with_name(claude_dir.name + ".disabled")
    claude_dir.rename(disabled)
    # Register multiple restore mechanisms for trap-safety
    atexit.register(lambda: disabled.rename(claude_dir) if disabled.exists() else None)
    original_sigint = signal.getsignal(signal.SIGINT)
    original_sigterm = signal.getsignal(signal.SIGTERM)
    def _restore_and_raise(signum, frame):
        if disabled.exists():
            disabled.rename(claude_dir)
        if signum == signal.SIGINT:
            signal.signal(signal.SIGINT, original_sigint)
            raise KeyboardInterrupt
        sys.exit(128 + signum)
    signal.signal(signal.SIGINT, _restore_and_raise)
    signal.signal(signal.SIGTERM, _restore_and_raise)
    try:
        yield
    finally:
        if disabled.exists():
            disabled.rename(claude_dir)
        signal.signal(signal.SIGINT, original_sigint)
        signal.signal(signal.SIGTERM, original_sigterm)
```

### 5.4 Safety Concerns

1. **Concurrent access**: If two eval processes both try to rename `.claude/`, the second one will fail because `.claude/` is already renamed. Solution: lock file via `fcntl.flock()` or avoid directory rename entirely (prefer Layer 1/2).

2. **Trap-safe restore** (AC-07 from conversation-decisions.md): Must handle SIGINT (Ctrl+C), SIGTERM, uncaught exceptions, and normal exit. The `atexit` + `signal.signal()` combination covers all cases except SIGKILL (which is unhandleable by design).

3. **Partial rename**: `Path.rename()` is atomic on the same filesystem (POSIX guarantee). Cross-filesystem renames fail atomically (raise `OSError`). No partial state risk.

4. **Stale .claude.disabled**: If the process crashes between rename and restore (e.g., OOM kill), `.claude.disabled` remains on disk. Recovery: check for `.claude.disabled` at eval startup and restore it automatically.

### 5.5 Complexity Assessment

| Approach | Complexity | Crash Safety | Concurrent Safety |
|----------|-----------|-------------|-------------------|
| Worktree isolation | Simple | Full (no mutation) | Full (separate directories) |
| Env-var override | Simple | Full (no mutation) | Full (process-local env) |
| Directory rename | Medium | Needs trap handlers | Needs lock file |

**Recommendation**: Use worktree isolation (Layer 1) as the primary mechanism. Use env-var overrides (Layer 2) for skill-level toggling. Avoid directory rename (Layer 3) unless testing proves the other approaches insufficient.

---

## 6. Judge Agent Integration

### 6.1 Fit with Existing Claude Subprocess Pattern

The judge agent maps directly to `ClaudeProcess` (pipeline/process.py:24-203). Comparison with how `roadmap/executor.py` spawns Claude subprocesses:

**Roadmap step subprocess** (roadmap/executor.py:281-309):
```python
proc = ClaudeProcess(
    prompt=effective_prompt,
    output_file=step.output_file,
    error_file=step.output_file.with_suffix(".err"),
    max_turns=config.max_turns,      # 100
    model=step.model or config.model,
    permission_flag=config.permission_flag,
    timeout_seconds=step.timeout_seconds,  # 300-900s
    output_format="text",
    extra_args=extra_args,
)
proc.start()
# ... poll for cancellation ...
exit_code = proc.wait()
```

**Judge agent subprocess** (proposed):
```python
proc = ClaudeProcess(
    prompt=judge_prompt,
    output_file=judge_output_path,
    error_file=judge_output_path.with_suffix(".err"),
    max_turns=15,                    # judges need few turns
    model=config.judge_model,        # always Opus by default
    permission_flag="--dangerously-skip-permissions",
    timeout_seconds=300,
    output_format="text",
)
proc.start()
exit_code = proc.wait()
```

The invocation is identical in structure. The only differences are:
- Lower `max_turns` (10-15 vs 100) -- judges produce a single scoring response
- Fixed model (`config.judge_model`, defaulting to Opus per conversation-decisions.md section 3)
- No polling loop or cancellation check (single blocking call)
- Prompt contains rubric + test output rather than pipeline context

### 6.2 Prompt Template Pattern

Follows `roadmap/prompts.py` exactly: pure functions that accept structured data and return prompt strings. No side effects, no file I/O.

```python
def build_judge_prompt(
    rubric: list[RubricDimension],
    test_output: str,
    test_context: dict,
) -> str:
    """Build structured prompt for judge scoring.

    Template structure:
    1. Role: "You are a quality judge..."
    2. Rubric: rendered dimensions with anchored definitions
    3. Test output: the artifact being evaluated
    4. Context: what the test was supposed to produce
    5. Instructions: output format (JSON scores array)
    """
```

### 6.3 Response Parsing

Judge output should be semi-structured JSON embedded in text:

```
Based on the rubric evaluation:

```json
[
  {"dimension": "completeness", "value": 8.5, "hard_fail": false, "reasoning": "..."},
  ...
]
```
```

Parsing: scan for JSON array in output via regex `r'\[\s*\{.*?\}\s*\]'` with `re.DOTALL`. Fallback: if no JSON found, return all dimensions with `value=0.0` and `reasoning="Judge output unparseable"`. This is lenient by design -- the judge is advisory (per conversation-decisions.md section 3, quality layer is "Scored", not "Hard PASS/FAIL").

---

## 7. Gap Summary Table

| # | Gap | What's Needed | Effort | Risk | Dependencies | Blocks |
|---|-----|---------------|--------|------|-------------|--------|
| G-01 | `eval/__init__.py` | Package init, Click group | S | Low | click | All eval modules |
| G-02 | `eval/models.py` | Score, RunResult, TestVerdict, EvalReport, EvalConfig | M | Low | pipeline/models.py | All eval modules |
| G-03 | `eval/rubric.py` | 5-dimension rubric, anchor definitions, prompt rendering | S | Low | G-02 | G-06 |
| G-04 | `eval/runner.py` | Multi-run execution, pytest subprocess, worktree, JUnit XML | C | High | G-02, G-08, subprocess | G-09, G-10 |
| G-05 | `eval/isolation.py` | Worktree + env-var isolation, trap-safe restore | M | Medium | pathlib, shutil, signal | G-04 |
| G-06 | `eval/judge.py` | ClaudeProcess invocation, prompt build, response parse | M | Medium | pipeline/process.py, G-02, G-03 | Nothing (optional) |
| G-07 | `eval/aggregator.py` | Mean, stddev, p-values, Cohen's d, consistency check | M | Medium | G-02, statistics | G-10 |
| G-08 | `eval/reporter.py` | report.md + scores.jsonl generation, model breakdown tables | M | Low | G-02, G-07, json | Nothing (leaf) |
| G-09 | Extract `write_state`/`read_state` | Move from roadmap/executor.py to pipeline/state.py | S | Low | None | G-04 (cleaner imports) |
| G-10 | CLI commands (`eval/commands.py`) | Click CLI: run, compare, report subcommands | M | Low | G-02, G-04, G-07, G-08 | G-11 |
| G-11 | CLI registration in main.py | 2-line import + add_command | S | Low | G-01 | CLI availability |
| G-12 | Eval gate criteria instances | GateCriteria for JUnit XML, scores.jsonl, report.md | S | Low | pipeline/models.py | G-04 |
| G-13 | Refactor scripts/eval_runner.py | Move logic into src/superclaude/eval/ | M | Low | G-02, G-04, G-07 | Code hygiene |

---

## 8. Dependency Graph (Build Order)

```
Phase 1 -- No dependencies (foundations):
  G-09  Extract write_state/read_state to pipeline/state.py     [S]
  G-01  eval/__init__.py                                         [S]
  G-12  Eval gate criteria instances                             [S]

Phase 2 -- Depends on Phase 1 (data model):
  G-02  eval/models.py                                           [M]
  G-03  eval/rubric.py                                           [S]

Phase 3 -- Depends on Phase 2 (parallel work):
  G-05  eval/isolation.py                                        [M]
  G-07  eval/aggregator.py                                       [M]

Phase 4 -- Depends on Phase 3 (core engine):
  G-04  eval/runner.py                                           [C]

Phase 5 -- Depends on Phase 4 (reporting + CLI):
  G-08  eval/reporter.py                                         [M]
  G-10  eval/commands.py                                         [M]
  G-11  CLI registration in main.py                              [S]

Phase 6 -- Optional, depends on Phase 2+3:
  G-06  eval/judge.py                                            [M]

Phase 7 -- Cleanup, depends on Phase 5:
  G-13  Refactor scripts/eval_runner.py                          [M]
```

Total: 4 Simple + 7 Medium + 1 Complex = 12 items across 7 phases.

Critical path: G-09 -> G-02 -> G-05 -> G-04 -> G-10 -> G-11 (6 steps, estimated 4 phases of parallel work).

---

## 9. Risk Assessment

### 9.1 Low Risk (G-01, G-02, G-03, G-08, G-09, G-11, G-12)

Pure data definitions, mechanical extraction, and template rendering. No integration complexity, no concurrency, no external system dependencies. These gaps are bounded by their interfaces and can be tested in isolation.

### 9.2 Medium Risk (G-05, G-06, G-07, G-10, G-13)

**G-05 (isolation.py)**: Directory rename has crash-safety concerns, but the recommended worktree + env-var approach avoids this entirely. The risk is that Claude Code may not respect env-var overrides for command/skill discovery, requiring fallback to directory rename.

**G-06 (judge.py)**: Judge quality depends on prompt engineering. Non-deterministic by nature. Mitigated by treating judge scores as advisory, not authoritative.

**G-07 (aggregator.py)**: Statistical edge cases (zero runs, single run, identical results) require careful handling. The prototype in scripts/eval_runner.py and scripts/ab_test_workflows.py provides working references.

**G-10 (commands.py)**: Standard Click CLI work. Risk is scope creep -- keep to three subcommands (run, compare, report) per conversation-decisions.md section 5.

### 9.3 High Risk (G-04)

**G-04 (runner.py)**: The most complex new module. Must orchestrate:
- Parallel subprocess management across multiple worktrees
- JUnit XML parsing with graceful degradation
- Timeout enforcement per individual test run
- Integration with isolation layer
- State persistence for resume support
- Fail-fast behavior across test layers
- Multi-model run matrix

The prototype in scripts/eval_runner.py covers ~40% of the needed functionality. The remaining 60% (multi-model, fail-fast layers, state persistence, robust error handling) is new work.

Mitigation: Build incrementally per conversation-decisions.md section 7 delivery plan. Slice 1 = single-run engine. Slice 2 = multi-run + aggregation. Slice 3 = full A/B comparison.

---

## 10. Reuse Inventory Summary

| Category | Count | Source |
|----------|-------|--------|
| Direct imports from pipeline/ | 6 types | models.py, gates.py, process.py |
| Functions to extract to pipeline/ | 2 functions | write_state, read_state |
| Prototype code to refactor | 5 functions | scripts/eval_runner.py |
| Statistical code to extract | 1 class | scripts/ab_test_workflows.py |
| Patterns to follow (not import) | 6 patterns | step execution, gate checking, state persistence, reporting, isolation, resume |
| Existing eval test files | 5 files (168 tests) | tests/roadmap/test_eval_*.py, tests/audit/test_eval_*.py |

Approximately 30-35% of the eval CLI tool can be built from existing code (direct reuse + refactored prototypes). The remaining 65-70% is new work, concentrated in runner.py (G-04) and the domain-specific modules (rubric.py, judge.py, aggregator.py).
