# TFEP Sprint Runner Architecture Design

**Version**: 1.0.0
**Date**: 2026-03-21
**Type**: Component Architecture
**Source**: sprint-runner-tfep-handoff.md
**Scope**: `src/superclaude/cli/sprint/tfep.py` + integration points in executor, process, monitor, models, commands, diagnostics

---

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Data Flow Diagram](#2-data-flow-diagram)
3. [Escalation State Machine](#3-escalation-state-machine)
4. [ForensicOrchestrator Class](#4-forensicorchestrator-class)
5. [Subprocess Lifecycle Management](#5-subprocess-lifecycle-management)
6. [Rollback Mechanism](#6-rollback-mechanism)
7. [Remediation Task Injection](#7-remediation-task-injection)
8. [Resume Prompt Construction](#8-resume-prompt-construction)
9. [Monitor Integration](#9-monitor-integration)
10. [Executor Phase Loop Integration](#10-executor-phase-loop-integration)
11. [Models Changes](#11-models-changes)
12. [CLI Commands Changes](#12-cli-commands-changes)
13. [Diagnostics Changes](#13-diagnostics-changes)
14. [Interface Contracts](#14-interface-contracts)
15. [Test Strategy](#15-test-strategy)

---

## 1. Module Overview

### Module Map

```
src/superclaude/cli/sprint/
├── tfep.py              ← NEW: ForensicOrchestrator, rollback, injection, prompts, incident reports
├── executor.py          ← MODIFIED: phase loop TFEP branch, git baseline capture
├── process.py           ← MODIFIED: ForensicProcess subclass, resume prompt builder
├── monitor.py           ← MODIFIED: TFEP marker detection patterns
├── models.py            ← MODIFIED: PhaseStatus enum, MonitorState fields, SprintConfig fields
├── commands.py          ← MODIFIED: --tfep-* Click options
└── diagnostics.py       ← MODIFIED: FailureCategory.TFEP
```

### Dependency Direction (imports flow downward only)

```
commands.py
    │
    ▼
executor.py ──────► tfep.py
    │                 │
    ▼                 ▼
process.py    pipeline/process.py (ClaudeProcess base)
    │
    ▼
monitor.py
    │
    ▼
models.py
```

`tfep.py` imports from:
- `models.py` (SprintConfig, Phase, PhaseStatus)
- `pipeline/process.py` (ClaudeProcess base class)
- `monitor.py` (OutputMonitor — for forensic subprocess liveness)
- Standard library only (subprocess, pathlib, dataclasses, logging, re)

`tfep.py` does NOT import from:
- `executor.py` (no circular dependency)
- `commands.py` (no CLI dependency)
- `diagnostics.py` (no diagnostic dependency)

---

## 2. Data Flow Diagram

### Phase-Level TFEP Flow

```
                    ┌────────────────────────────────────────┐
                    │          execute_sprint() loop          │
                    │              [executor.py]              │
                    └──────────┬─────────────────────────────┘
                               │
                         launch phase
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ClaudeProcess      │
                    │   (phase subprocess) │
                    │   [process.py]       │
                    └──────────┬───────────┘
                               │
                          exit code + result file
                               │
                               ▼
                    ┌──────────────────────┐
                    │ _determine_phase_    │
                    │ status()             │
                    │ [executor.py]        │
                    └──────┬──────┬────────┘
                           │      │
              PhaseStatus  │      │ PhaseStatus
              .PASS etc    │      │ .TFEP_HALT
                           │      │
                           ▼      ▼
                    continue   ┌──────────────────────────┐
                    sprint     │ _handle_tfep_halt()      │
                               │ [executor.py]             │
                               └──────────┬───────────────┘
                                          │
                                          ▼
                               ┌──────────────────────────┐
                               │ ForensicOrchestrator     │
                               │ .run()                   │
                               │ [tfep.py]                │
                               └──────────┬───────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
          ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
          │ RCA subprocess  │  │ RCA subprocess   │  │ (wait for both) │
          │ alpha [Sonnet]  │  │ bravo [Sonnet]   │  │                 │
          └────────┬────────┘  └────────┬─────────┘  └────────┬────────┘
                   │                    │                      │
                   └─────────┬──────────┘                      │
                             ▼                                 │
                   ┌──────────────────┐                        │
                   │ Judge subprocess │                        │
                   │ /sc:adversarial  │                        │
                   │ --depth quick    │                        │
                   └────────┬─────────┘                        │
                            │                                  │
                            ▼ rca-verdict.md                   │
                            │                                  │
              ┌─────────────┼──────────────┐                   │
              │             │              │                   │
              ▼             ▼              ▼                   │
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
    │ Sol alpha    │ │ Sol bravo    │ │ (wait)       │         │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘         │
           └────────┬───────┘                │                 │
                    ▼                        │                 │
          ┌──────────────────┐               │                 │
          │ Judge subprocess │               │                 │
          └────────┬─────────┘               │                 │
                   │                         │                 │
                   ▼ solution-verdict.md      │                 │
                   │                         │                 │
                   ▼                         ▼                 ▼
          ┌──────────────────────────────────────────────────────┐
          │ ForensicOrchestrator returns ForensicResult          │
          └──────────┬─────────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────────────────────┐
          │ _handle_tfep_halt() continued        │
          │ 1. perform_rollback() if needed      │
          │ 2. inject_remediation_tasks()        │
          │ 3. build_tfep_resume_prompt()        │
          │ 4. re-launch phase subprocess        │
          │ 5. write incident report             │
          └──────────────────────────────────────┘
```

### File I/O Contract

```
INPUTS (read by ForensicOrchestrator):
  {isolation_dir}/failure_context.yaml     ← written by phase Claude subprocess
  {work_dir}/ (git state)                  ← code changes from phase subprocess

OUTPUTS (written by ForensicOrchestrator):
  {results_dir}/phase-{N}-tfep/
    rca-alpha-output.txt                   ← RCA agent A NDJSON output
    rca-alpha-errors.txt                   ← RCA agent A stderr
    rca-alpha.md                           ← RCA agent A findings
    rca-bravo-output.txt                   ← RCA agent B NDJSON output
    rca-bravo-errors.txt                   ← RCA agent B stderr
    rca-bravo.md                           ← RCA agent B findings
    rca-judge-output.txt                   ← Judge NDJSON output
    rca-verdict.md                         ← Adjudicated RCA
    solution-alpha.md                      ← Solution agent A proposal
    solution-bravo.md                      ← Solution agent B proposal
    solution-judge-output.txt              ← Judge NDJSON output
    solution-verdict.md                    ← Adjudicated solution
  {results_dir}/phase-{N}-tfep-rollback.patch  ← git patch of rolled-back work
  {results_dir}/phase-{N}-tfep-incident.md     ← incident report
  {isolation_dir}/{phase_file}             ← modified with injected remediation tasks
```

---

## 3. Escalation State Machine

```
                    ┌────────────────┐
                    │   MONITORING   │ ◄──── phase subprocess running
                    └───────┬────────┘
                            │
                      phase exits with
                      TFEP_HALT
                            │
                            ▼
                    ┌────────────────┐
          ┌────────│   ESCALATION   │────────┐
          │        │   EVALUATOR    │        │
          │        └───────┬────────┘        │
          │                │                 │
     count == 1       count == 2        count >= 3
          │                │                 │
          ▼                ▼                 ▼
  ┌───────────────┐ ┌──────────────┐ ┌──────────────┐
  │  LIGHT TIER   │ │ STANDARD     │ │  HARD HALT   │
  │  FORENSIC     │ │ TIER         │ │  (sprint     │
  │  (4-step)     │ │ FORENSIC     │ │   stops)     │
  │               │ │ (2-step)     │ │              │
  └───────┬───────┘ └──────┬───────┘ └──────────────┘
          │                │
          ▼                ▼
  ┌───────────────┐ ┌──────────────┐
  │   ROLLBACK    │ │   ROLLBACK   │
  │   (if needed) │ │   (if needed)│
  └───────┬───────┘ └──────┬───────┘
          │                │
          ▼                ▼
  ┌───────────────┐ ┌──────────────┐
  │   RELAUNCH    │ │   RELAUNCH   │
  │   (1.5x turns)│ │   (2.0x turns│
  └───────┬───────┘ └──────┬───────┘
          │                │
     ┌────┴────┐      ┌────┴────┐
     │ success │      │ success │
     │  TFEP_  │      │  TFEP_  │
     │ RESOLVED│      │ RESOLVED│
     └─────────┘      └─────────┘
          │                │
   if TFEP_HALT again:     │
   increment count,        │
   return to EVALUATOR     │
```

### State Machine Implementation

```python
@dataclass
class EscalationState:
    """Per-phase TFEP escalation tracking."""
    phase_number: int
    trigger_count: int = 0
    failing_tests: set[str] = field(default_factory=set)
    tier: str = "light"  # "light" | "standard"

    def advance(self, new_failing_tests: set[str]) -> str:
        """Advance escalation. Returns action: 'light' | 'standard' | 'halt'."""
        if new_failing_tests != self.failing_tests:
            # Different tests failing → treat as new TFEP, reset
            self.trigger_count = 0
            self.failing_tests = new_failing_tests

        self.trigger_count += 1

        if self.trigger_count == 1:
            self.tier = "light"
            return "light"
        elif self.trigger_count == 2:
            self.tier = "standard"
            return "standard"
        else:
            return "halt"

    @property
    def budget_multiplier(self) -> float:
        if self.trigger_count == 1:
            return 1.5
        elif self.trigger_count == 2:
            return 2.0
        return 1.0
```

---

## 4. ForensicOrchestrator Class

### Class Design

```python
@dataclass
class ForensicResult:
    """Return value from ForensicOrchestrator.run()."""
    status: str                    # "success" | "partial" | "failed"
    rca_verdict_path: Path | None
    solution_verdict_path: Path | None
    rollback_needed: bool
    causal_files: list[str]        # files identified as causing the failure
    remediation_tasks: str         # markdown block ready for injection
    tier: str                      # "light" | "standard"
    agent_outputs: dict[str, Path] # name → output path for all agents
    incident_summary: str          # one-paragraph summary for incident report


class ForensicOrchestrator:
    """Orchestrates parallel forensic investigation subprocesses.

    Owns the entire TFEP forensic lifecycle:
    1. Parse failure context
    2. Spawn parallel investigation agents
    3. Spawn adversarial judge
    4. (Light tier only) Spawn parallel solution agents + second judge
    5. Produce ForensicResult with remediation tasks

    Does NOT own: rollback, task injection, phase re-launch, escalation decisions.
    Those are handled by the caller (_handle_tfep_halt in executor.py).
    """

    def __init__(
        self,
        config: SprintConfig,
        phase: Phase,
        failure_context_path: Path,
        tier: str,                    # "light" | "standard"
    ):
        self._config = config
        self._phase = phase
        self._context_path = failure_context_path
        self._tier = tier
        self._tfep_dir = config.results_dir / f"phase-{phase.number}-tfep"
        self._context: dict = {}

    def run(self) -> ForensicResult:
        """Execute the forensic pipeline. Blocking call."""
        self._tfep_dir.mkdir(parents=True, exist_ok=True)
        self._context = self._load_context()

        if self._tier == "light":
            return self._run_light_pipeline()
        else:
            return self._run_standard_pipeline()
```

### Light Tier Pipeline (4-step)

```python
    def _run_light_pipeline(self) -> ForensicResult:
        """Light tier: RCA×2 → judge → Solution×2 → judge."""
        # Step 1: Parallel RCA agents
        rca_outputs = self._spawn_parallel_agents(
            role="rca",
            prompt_builder=self._build_rca_prompt,
            names=["alpha", "bravo"],
        )

        # Step 2: RCA judge
        rca_verdict = self._spawn_judge(
            input_files=[rca_outputs["alpha"], rca_outputs["bravo"]],
            output_name="rca-verdict",
        )

        # Step 3: Parallel solution agents
        sol_outputs = self._spawn_parallel_agents(
            role="solution",
            prompt_builder=lambda name: self._build_solution_prompt(name, rca_verdict),
            names=["alpha", "bravo"],
        )

        # Step 4: Solution judge
        sol_verdict = self._spawn_judge(
            input_files=[sol_outputs["alpha"], sol_outputs["bravo"]],
            output_name="solution-verdict",
        )

        return self._build_result(rca_verdict, sol_verdict, rca_outputs | sol_outputs)
```

### Standard Tier Pipeline (2-step)

```python
    def _run_standard_pipeline(self) -> ForensicResult:
        """Standard tier: Full×2 → judge."""
        full_outputs = self._spawn_parallel_agents(
            role="full",
            prompt_builder=self._build_full_investigation_prompt,
            names=["alpha", "bravo"],
        )

        verdict = self._spawn_judge(
            input_files=[full_outputs["alpha"], full_outputs["bravo"]],
            output_name="verdict",
        )

        return self._build_result(verdict, verdict, full_outputs)
```

### Internal Methods

```python
    def _load_context(self) -> dict:
        """Load and validate failure_context.yaml."""
        import yaml
        content = self._context_path.read_text()
        ctx = yaml.safe_load(content)
        # Validate required fields
        required = ["test_names", "test_files", "error_output",
                     "expected_behavior", "actual_behavior",
                     "changes_made", "task_description"]
        for field in required:
            if field not in ctx:
                raise ValueError(f"failure_context.yaml missing required field: {field}")
        return ctx

    def _spawn_parallel_agents(
        self,
        role: str,
        prompt_builder: Callable[[str], str],
        names: list[str],
    ) -> dict[str, Path]:
        """Spawn N parallel Claude subprocesses, wait for all, return output paths."""
        ...  # See Section 5

    def _spawn_judge(
        self,
        input_files: list[Path],
        output_name: str,
    ) -> Path:
        """Spawn adversarial judge subprocess, return verdict path."""
        ...  # See Section 5

    def _build_result(
        self,
        rca_verdict: Path,
        sol_verdict: Path,
        all_outputs: dict[str, Path],
    ) -> ForensicResult:
        """Parse verdicts and build ForensicResult."""
        ...  # Parse rca_verdict for causal_files
        ...  # Parse sol_verdict for remediation tasks
        ...  # Determine rollback_needed from causal_files
```

---

## 5. Subprocess Lifecycle Management

### ForensicProcess (extends pipeline ClaudeProcess)

```python
# In tfep.py

from superclaude.cli.pipeline.process import ClaudeProcess as _PipelineClaudeProcess


class ForensicProcess(_PipelineClaudeProcess):
    """Claude subprocess for forensic investigation agents.

    Thin wrapper around pipeline ClaudeProcess with forensic-specific
    defaults (model, max_turns, timeout). Does not subclass sprint's
    ClaudeProcess to avoid coupling to sprint prompt structure.
    """

    def __init__(
        self,
        *,
        prompt: str,
        output_file: Path,
        error_file: Path,
        model: str = "",         # empty = config default (Sonnet)
        max_turns: int = 50,
        timeout_seconds: int = 300,
        permission_flag: str = "--dangerously-skip-permissions",
        env_vars: dict[str, str] | None = None,
    ):
        super().__init__(
            prompt=prompt,
            output_file=output_file,
            error_file=error_file,
            max_turns=max_turns,
            model=model,
            permission_flag=permission_flag,
            timeout_seconds=timeout_seconds,
            output_format="stream-json",
            env_vars=env_vars,
        )
```

### Parallel Spawning Pattern

```python
    def _spawn_parallel_agents(
        self,
        role: str,
        prompt_builder: Callable[[str], str],
        names: list[str],
    ) -> dict[str, Path]:
        """Spawn N agents in parallel, wait for all, return {name: output_md_path}."""
        import concurrent.futures

        processes: dict[str, ForensicProcess] = {}
        output_paths: dict[str, Path] = {}

        # Build and start all processes
        for name in names:
            prompt = prompt_builder(name)
            output_file = self._tfep_dir / f"{role}-{name}-output.txt"
            error_file = self._tfep_dir / f"{role}-{name}-errors.txt"
            md_path = self._tfep_dir / f"{role}-{name}.md"

            proc = ForensicProcess(
                prompt=prompt,
                output_file=output_file,
                error_file=error_file,
                model=self._config.tfep_model,
                max_turns=self._config.tfep_max_turns,
                timeout_seconds=self._config.tfep_agent_timeout,
                permission_flag=self._config.permission_flag,
            )
            proc.start()
            processes[name] = proc
            output_paths[name] = md_path

        # Wait for all processes (parallel waiting via threads)
        results: dict[str, int] = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(names)) as pool:
            futures = {
                pool.submit(proc.wait): name
                for name, proc in processes.items()
            }
            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                results[name] = future.result()

        # Validate: at least one agent must succeed
        successes = [n for n, rc in results.items() if rc == 0]
        if len(successes) == 0:
            _log.error("All forensic agents failed: %s", results)
            # Return whatever outputs exist (may be partial)

        return output_paths

    def _spawn_judge(
        self,
        input_files: list[Path],
        output_name: str,
    ) -> Path:
        """Spawn adversarial judge, return verdict path."""
        file_list = ",".join(str(f) for f in input_files)
        prompt = (
            f"/sc:adversarial --compare {file_list} --depth quick\n"
            f"\n"
            f"Compare the forensic investigation outputs and produce an adjudicated verdict.\n"
            f"Write the merged verdict to: {self._tfep_dir / f'{output_name}.md'}\n"
        )

        output_file = self._tfep_dir / f"{output_name}-judge-output.txt"
        error_file = self._tfep_dir / f"{output_name}-judge-errors.txt"
        verdict_path = self._tfep_dir / f"{output_name}.md"

        proc = ForensicProcess(
            prompt=prompt,
            output_file=output_file,
            error_file=error_file,
            model=self._config.tfep_model,
            max_turns=self._config.tfep_max_turns,
            timeout_seconds=self._config.tfep_agent_timeout,
            permission_flag=self._config.permission_flag,
        )
        proc.start()
        exit_code = proc.wait()

        if exit_code != 0:
            _log.warning("Judge subprocess exited %d for %s", exit_code, output_name)

        return verdict_path
```

### Subprocess Cleanup

All `ForensicProcess` instances use the inherited `terminate()` from `pipeline/process.py` which:
1. Sends SIGTERM to the process group
2. Waits 10s
3. Escalates to SIGKILL

The `ForensicOrchestrator` wraps all subprocess work in try/finally to ensure cleanup:

```python
    def run(self) -> ForensicResult:
        try:
            ...  # pipeline execution
        except Exception:
            # Ensure all running subprocesses are terminated
            self._cleanup()
            raise

    def _cleanup(self):
        """Terminate any still-running forensic subprocesses."""
        for proc in self._active_processes:
            try:
                proc.terminate()
            except Exception:
                pass
```

---

## 6. Rollback Mechanism

### Interface

```python
@dataclass
class RollbackResult:
    """Result of a rollback operation."""
    performed: bool
    patch_path: Path | None       # path to saved .patch file
    files_reverted: list[str]     # files that were git-checkout'd
    scope: str                    # "full" | "selective" | "none"


def perform_rollback(
    config: SprintConfig,
    phase: Phase,
    forensic_result: ForensicResult,
    git_baseline: str,            # commit SHA at phase start
) -> RollbackResult:
    """Save patch and revert phase changes if forensic says prior work was wrong.

    Algorithm:
    1. Compute files changed during this phase: git diff --name-only {baseline}
    2. If forensic_result.rollback_needed is False → return scope="none"
    3. Save full patch: git diff {baseline} > results/phase-N-tfep-rollback.patch
    4. Determine scope:
       a. If ALL changed files are in forensic_result.causal_files → scope="full"
       b. If SOME are causal → scope="selective"
    5. Revert:
       a. Full: git checkout {baseline} -- .
       b. Selective: git checkout {baseline} -- {causal_files}
    6. Return RollbackResult
    """
```

### Implementation Detail

```python
def perform_rollback(
    config: SprintConfig,
    phase: Phase,
    forensic_result: ForensicResult,
    git_baseline: str,
) -> RollbackResult:
    import subprocess as _sp

    results_dir = config.results_dir
    patch_path = results_dir / f"phase-{phase.number}-tfep-rollback.patch"

    if not forensic_result.rollback_needed:
        return RollbackResult(performed=False, patch_path=None, files_reverted=[], scope="none")

    # 1. Get files changed during this phase
    diff_result = _sp.run(
        ["git", "diff", "--name-only", git_baseline],
        capture_output=True, text=True, timeout=10,
    )
    phase_changed_files = set(diff_result.stdout.strip().splitlines())

    if not phase_changed_files:
        return RollbackResult(performed=False, patch_path=None, files_reverted=[], scope="none")

    # 2. Save patch (always, regardless of scope)
    patch_result = _sp.run(
        ["git", "diff", git_baseline],
        capture_output=True, text=True, timeout=30,
    )
    patch_path.write_text(patch_result.stdout)

    # 3. Determine scope
    causal_set = set(forensic_result.causal_files)
    causal_in_phase = causal_set & phase_changed_files

    if causal_in_phase == phase_changed_files:
        scope = "full"
        revert_files = list(phase_changed_files)
    else:
        scope = "selective"
        revert_files = list(causal_in_phase)

    # 4. Revert
    if scope == "full":
        _sp.run(["git", "checkout", git_baseline, "--", "."], timeout=10)
    else:
        for f in revert_files:
            _sp.run(["git", "checkout", git_baseline, "--", f], timeout=10)

    return RollbackResult(
        performed=True,
        patch_path=patch_path,
        files_reverted=revert_files,
        scope=scope,
    )
```

### Git Baseline Capture

In `executor.py`, capture the git baseline at phase start:

```python
# Inside execute_sprint(), before launching phase subprocess:
git_baseline = ""
try:
    _git_result = _subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, timeout=5,
    )
    if _git_result.returncode == 0:
        git_baseline = _git_result.stdout.strip()
except (FileNotFoundError, _subprocess.TimeoutExpired):
    pass  # Not a git repo or git unavailable
```

---

## 7. Remediation Task Injection

### Interface

```python
def inject_remediation_tasks(
    phase_file: Path,
    phase_number: int,
    remediation_markdown: str,
    last_completed_task_id: str,
) -> Path:
    """Inject remediation tasks into a phase tasklist file.

    Inserts remediation_markdown AFTER the last completed task
    and BEFORE any test/verification tasks.

    Remediation tasks use T{XX}.50+ IDs to avoid collision with
    original tasks (which use T{XX}.01-T{XX}.20 typically).

    Args:
        phase_file: Path to the phase tasklist file (in isolation dir).
        phase_number: Phase number (for task ID prefix).
        remediation_markdown: Pre-formatted markdown block with ### headers.
        last_completed_task_id: e.g., "T03.04" — insertion point marker.

    Returns:
        Path to the modified phase file (same path, modified in-place).
    """
```

### Algorithm

```python
def inject_remediation_tasks(
    phase_file: Path,
    phase_number: int,
    remediation_markdown: str,
    last_completed_task_id: str,
) -> Path:
    content = phase_file.read_text()
    lines = content.splitlines(keepends=True)

    # Find insertion point: after the last completed task's section
    # A task section ends when the next ### heading appears or EOF
    task_heading_pattern = re.compile(rf"^###\s+T{phase_number:02d}\.\d{{2}}")
    insertion_line = len(lines)  # default: end of file

    in_completed_task = False
    for i, line in enumerate(lines):
        if task_heading_pattern.match(line):
            if last_completed_task_id in line:
                in_completed_task = True
            elif in_completed_task:
                # Next task after the completed one — insert BEFORE this
                insertion_line = i
                break

    # Build injection block
    injection = (
        f"\n---\n\n"
        f"## Failure Remediation Plan (Adjudicated)\n\n"
        f"<!-- Injected by TFEP sprint runner. Tasks T{phase_number:02d}.50+ "
        f"are remediation tasks. -->\n\n"
        f"{remediation_markdown}\n\n"
        f"---\n\n"
    )

    # Insert
    lines.insert(insertion_line, injection)
    phase_file.write_text("".join(lines))

    return phase_file
```

### Remediation Task Format

The `ForensicOrchestrator._build_result()` method parses `solution-verdict.md` and formats remediation tasks as:

```markdown
### T{XX}.50 -- {Remediation title from verdict}

**Dependencies:** none
**Deliverables:**
- [ ] {implementation step 1}
- [ ] {implementation step 2}
- [ ] {implementation step 3}

**Expected outcome**: {from solution verdict}
**Test criteria**: {from solution verdict}
```

This format matches the existing `parse_tasklist()` regex: `^###\s+(T\d{2}\.\d{2})\s*(?:--|-—|—)\s*(.+)`

---

## 8. Resume Prompt Construction

### Interface

```python
# In process.py

def build_tfep_resume_prompt(
    config: SprintConfig,
    phase: Phase,
    rollback_result: RollbackResult,
    last_completed_task_id: str,
    remediation_start_id: str,      # e.g., "T03.50"
    git_diff_summary: str,
) -> str:
    """Build prompt for re-launching a phase after TFEP remediation."""
```

### Implementation

```python
def build_tfep_resume_prompt(
    config: SprintConfig,
    phase: Phase,
    rollback_result: RollbackResult,
    last_completed_task_id: str,
    remediation_start_id: str,
    git_diff_summary: str,
) -> str:
    pn = phase.number
    phase_file = phase.file

    # Rollback context
    if rollback_result.performed:
        rollback_block = (
            f"## Rollback Notice\n"
            f"Prior implementation through task {last_completed_task_id} was ROLLED BACK.\n"
            f"Scope: {rollback_result.scope} ({len(rollback_result.files_reverted)} files)\n"
            f"Reason: Forensic analysis determined prior work caused test failures.\n"
            f"Patch saved to: {rollback_result.patch_path}\n"
            f"The remediation plan below SUPERSEDES the original task approach.\n"
        )
    else:
        rollback_block = (
            f"## Prior Work Notice\n"
            f"Tasks through {last_completed_task_id} completed successfully.\n"
            f"Remediation tasks address test failures without rolling back prior work.\n"
        )

    return (
        f"/sc:task-unified Execute remediation tasks in @{phase_file} "
        f"--compliance strict --strategy systematic\n"
        f"\n"
        f"## TFEP Remediation Re-launch — Phase {pn}\n"
        f"\n"
        f"This is a TFEP remediation re-launch. Do NOT re-execute prior tasks.\n"
        f"\n"
        f"{rollback_block}\n"
        f"\n"
        f"## Execution Scope\n"
        f"- SKIP tasks {phase.file.stem} T{pn:02d}.01 through {last_completed_task_id} "
        f"— they are {'rolled back' if rollback_result.performed else 'already complete'}.\n"
        f"- EXECUTE remediation tasks starting from {remediation_start_id}.\n"
        f"- After remediation tasks, re-run ALL verification/test tasks.\n"
        f"- Do NOT re-execute earlier implementation tasks.\n"
        f"\n"
        f"## Git Changes Since Phase Start\n"
        f"```\n{git_diff_summary}\n```\n"
        f"\n"
        f"## Result File\n"
        f"- Write result to: `{config.result_file(phase).as_posix()}`\n"
        f"- On success: `EXIT_RECOMMENDATION: CONTINUE`\n"
        f"- On failure: `EXIT_RECOMMENDATION: TFEP_HALT` (if tests still fail)\n"
        f"  or `EXIT_RECOMMENDATION: HALT` (if non-TFEP failure)\n"
    )
```

---

## 9. Monitor Integration

### New Patterns (monitor.py)

```python
# Add to monitor.py, near existing pattern definitions:

TFEP_TRIGGERED_PATTERN = re.compile(r"TFEP_TRIGGERED")
TFEP_RESOLVED_PATTERN = re.compile(r"TFEP_RESOLVED")
TFEP_ESCALATED_PATTERN = re.compile(r"TFEP_ESCALATED")
```

### MonitorState Extensions

```python
# Add to MonitorState dataclass in models.py:

    tfep_triggered: bool = False
    tfep_trigger_count: int = 0
    tfep_status: str = ""  # "" | "triggered" | "resolved" | "escalated"
```

### Signal Extraction Update

```python
# Add to _extract_signals_from_text() in monitor.py:

    # TFEP markers
    if TFEP_TRIGGERED_PATTERN.search(text):
        self.state.tfep_triggered = True
        self.state.tfep_trigger_count += 1
        self.state.tfep_status = "triggered"
        debug_log(_dbg, "signal_extracted", signal_type="tfep", value="TRIGGERED")

    if TFEP_RESOLVED_PATTERN.search(text):
        self.state.tfep_status = "resolved"
        debug_log(_dbg, "signal_extracted", signal_type="tfep", value="RESOLVED")

    if TFEP_ESCALATED_PATTERN.search(text):
        self.state.tfep_status = "escalated"
        debug_log(_dbg, "signal_extracted", signal_type="tfep", value="ESCALATED")
```

---

## 10. Executor Phase Loop Integration

### _determine_phase_status() Change

```python
# In executor.py, update _determine_phase_status():
# Add BEFORE the existing result_file.exists() block (before line 1470):

    if result_file.exists():
        content = result_file.read_text(errors="replace")
        upper = content.upper()

        # TFEP_HALT check — BEFORE generic HALT (higher priority)
        if "EXIT_RECOMMENDATION: TFEP_HALT" in upper:
            return PhaseStatus.TFEP_HALT

        # ... existing HALT/CONTINUE checks follow unchanged ...
```

### Phase Loop TFEP Branch

```python
# In execute_sprint(), after status = _determine_phase_status(...):
# Replace the existing `if status.is_failure:` block with:

                if status == PhaseStatus.TFEP_HALT:
                    # TFEP triggered — orchestrate forensic analysis
                    tfep_outcome = _handle_tfep_halt(
                        config=config,
                        phase=phase,
                        escalation_states=escalation_states,
                        git_baseline=git_baseline,
                        monitor_state=monitor.state,
                        logger=logger,
                        tui=tui,
                        signal_handler=signal_handler,
                    )
                    if tfep_outcome == "resolved":
                        # Re-launched phase succeeded
                        phase_result.status = PhaseStatus.TFEP_RESOLVED
                        sprint_result.phase_results.append(phase_result)
                        logger.write_phase_result(phase_result)
                        continue  # next phase
                    elif tfep_outcome == "escalated":
                        # Re-launched phase triggered TFEP again → loop back
                        # (escalation_states tracks count; _handle_tfep_halt
                        #  will return "halt" on 3rd trigger)
                        continue  # re-enter the TFEP branch
                    else:
                        # "halt" — 3rd trigger or forensic failure
                        sprint_result.outcome = SprintOutcome.HALTED
                        sprint_result.halt_phase = phase.number
                        break

                elif status.is_failure:
                    # ... existing non-TFEP failure handling unchanged ...
```

### _handle_tfep_halt() Function

```python
def _handle_tfep_halt(
    config: SprintConfig,
    phase: Phase,
    escalation_states: dict[int, EscalationState],
    git_baseline: str,
    monitor_state: MonitorState,
    logger: SprintLogger,
    tui: SprintTUI,
    signal_handler: SignalHandler,
) -> str:
    """Handle TFEP_HALT: orchestrate forensic, rollback, re-launch.

    Returns: "resolved" | "escalated" | "halt"
    """
    from .tfep import (
        ForensicOrchestrator,
        EscalationState,
        perform_rollback,
        inject_remediation_tasks,
        write_incident_report,
    )

    # 1. Get or create escalation state for this phase
    if phase.number not in escalation_states:
        escalation_states[phase.number] = EscalationState(phase_number=phase.number)
    esc = escalation_states[phase.number]

    # 2. Read failure context to get failing test names
    context_path = _find_failure_context(config, phase)
    if context_path is None:
        _log.error("TFEP_HALT but no failure_context.yaml found")
        return "halt"

    import yaml
    ctx = yaml.safe_load(context_path.read_text())
    failing_tests = set(ctx.get("test_names", []))

    # 3. Advance escalation state
    action = esc.advance(failing_tests)
    if action == "halt":
        write_incident_report(config, phase, esc, None, None, outcome="hard_halt")
        return "halt"

    # 4. Run forensic orchestrator
    orchestrator = ForensicOrchestrator(
        config=config,
        phase=phase,
        failure_context_path=context_path,
        tier=action,
    )
    forensic_result = orchestrator.run()

    if forensic_result.status == "failed":
        write_incident_report(config, phase, esc, forensic_result, None, outcome="forensic_failed")
        return "halt"

    # 5. Rollback if needed
    rollback_result = perform_rollback(config, phase, forensic_result, git_baseline)

    # 6. Inject remediation tasks
    isolation_dir = config.results_dir / ".isolation" / f"phase-{phase.number}"
    phase_file_copy = isolation_dir / phase.file.name
    last_task = monitor_state.last_task_id or f"T{phase.number:02d}.01"
    inject_remediation_tasks(
        phase_file=phase_file_copy,
        phase_number=phase.number,
        remediation_markdown=forensic_result.remediation_tasks,
        last_completed_task_id=last_task,
    )

    # 7. Build resume prompt and re-launch
    git_diff = _get_git_diff_stat(git_baseline)
    resume_prompt = build_tfep_resume_prompt(
        config=config,
        phase=phase,
        rollback_result=rollback_result,
        last_completed_task_id=last_task,
        remediation_start_id=f"T{phase.number:02d}.50",
        git_diff_summary=git_diff,
    )

    # 8. Re-launch with extended budget
    extended_turns = int(config.max_turns * esc.budget_multiplier)
    extended_timeout = extended_turns * 120 + 300 + 600  # +600s for TFEP

    relaunch_proc = _PipelineClaudeProcess(
        prompt=resume_prompt,
        output_file=config.output_file(phase),  # overwrite original output
        error_file=config.error_file(phase),
        max_turns=extended_turns,
        model=config.model,
        permission_flag=config.permission_flag,
        timeout_seconds=extended_timeout,
        output_format="stream-json",
        env_vars={"CLAUDE_WORK_DIR": str(isolation_dir)},
    )
    relaunch_proc.start()
    relaunch_exit = relaunch_proc.wait()

    # 9. Determine re-launch outcome
    relaunch_status = _determine_phase_status(
        exit_code=relaunch_exit,
        result_file=config.result_file(phase),
        output_file=config.output_file(phase),
        config=config,
        phase=phase,
        started_at=time.time(),
        error_file=config.error_file(phase),
    )

    # 10. Write incident report
    outcome = "resolved" if relaunch_status.is_success else (
        "escalated" if relaunch_status == PhaseStatus.TFEP_HALT else "failed"
    )
    write_incident_report(config, phase, esc, forensic_result, rollback_result, outcome=outcome)

    if relaunch_status.is_success:
        return "resolved"
    elif relaunch_status == PhaseStatus.TFEP_HALT:
        return "escalated"
    else:
        return "halt"
```

---

## 11. Models Changes

### PhaseStatus Enum

```python
class PhaseStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASS = "pass"
    PASS_NO_SIGNAL = "pass_no_signal"
    PASS_NO_REPORT = "pass_no_report"
    PASS_RECOVERED = "pass_recovered"
    PREFLIGHT_PASS = "preflight_pass"
    TFEP_HALT = "tfep_halt"            # NEW
    TFEP_RESOLVED = "tfep_resolved"    # NEW
    INCOMPLETE = "incomplete"
    HALT = "halt"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"

    @property
    def is_success(self) -> bool:
        return self in (
            PhaseStatus.PASS,
            PhaseStatus.PASS_NO_SIGNAL,
            PhaseStatus.PASS_NO_REPORT,
            PhaseStatus.PASS_RECOVERED,
            PhaseStatus.PREFLIGHT_PASS,
            PhaseStatus.TFEP_RESOLVED,     # NEW — success after remediation
        )

    @property
    def is_failure(self) -> bool:
        return self in (
            PhaseStatus.INCOMPLETE,
            PhaseStatus.HALT,
            PhaseStatus.TIMEOUT,
            PhaseStatus.ERROR,
            # Note: TFEP_HALT is NOT in is_failure.
            # It triggers the TFEP branch, not the generic failure branch.
        )

    @property
    def is_tfep(self) -> bool:            # NEW
        return self in (PhaseStatus.TFEP_HALT, PhaseStatus.TFEP_RESOLVED)
```

### SprintConfig Extensions

```python
@dataclass
class SprintConfig(PipelineConfig):
    # ... existing fields ...

    # TFEP configuration (all optional with sensible defaults)
    tfep_model: str = ""                    # empty = Sonnet (via --model sonnet on subprocess)
    tfep_agents: int = 2                    # parallel agents per step (2-4)
    tfep_budget_multiplier: float = 1.5     # turn multiplier for re-launched phases
    tfep_max_turns: int = 50               # max turns per forensic agent
    tfep_agent_timeout: int = 300          # seconds per forensic agent
```

### MonitorState Extensions

```python
@dataclass
class MonitorState:
    # ... existing fields ...

    # TFEP tracking
    tfep_triggered: bool = False
    tfep_trigger_count: int = 0
    tfep_status: str = ""    # "" | "triggered" | "resolved" | "escalated"
```

---

## 12. CLI Commands Changes

### New Click Options (commands.py)

```python
@click.option("--tfep-model", default="", help="Model for TFEP forensic agents (default: Sonnet)")
@click.option("--tfep-agents", default=2, type=click.IntRange(2, 4),
              help="Parallel agents per TFEP forensic step (default: 2)")
@click.option("--tfep-budget-multiplier", default=1.5, type=click.FloatRange(1.0, 3.0),
              help="Turn budget multiplier for re-launched phases (default: 1.5)")
```

These are threaded through to `SprintConfig` in `load_sprint_config()`.

---

## 13. Diagnostics Changes

### FailureCategory Extension

```python
class FailureCategory(Enum):
    STALL = "stall"
    TIMEOUT = "timeout"
    CRASH = "crash"
    ERROR = "error"
    UNKNOWN = "unknown"
    CONTEXT_EXHAUSTION = "context_exhaustion"
    TFEP = "tfep"                    # NEW
```

### FailureClassifier Update

```python
# In classify(), before the fallback return:

    # TFEP detection: phase exited with TFEP_HALT marker
    if bundle.phase_result and bundle.phase_result.status == PhaseStatus.TFEP_HALT:
        return FailureCategory.TFEP
```

---

## 14. Interface Contracts

### Contract 1: Phase Subprocess → Runner (TFEP Signal)

Claude writes to result file:
```
EXIT_RECOMMENDATION: TFEP_HALT
```

Claude writes `failure_context.yaml` to working directory with schema from forensic spec Section 9.4b.

Claude emits `TFEP_TRIGGERED` in NDJSON output stream.

### Contract 2: Runner → Forensic Agents (Prompt)

RCA prompt includes:
- `/sc:troubleshoot` prefix
- Full `failure_context.yaml` content inline
- Instruction to write findings to specific path
- No `--fix` flag (diagnosis only)

Solution prompt includes:
- `/sc:brainstorm` prefix
- `rca-verdict.md` content inline
- Instruction to write solution to specific path
- Instruction to format as tasklist-compatible remediation block

### Contract 3: ForensicOrchestrator → Executor (ForensicResult)

```python
@dataclass
class ForensicResult:
    status: str                    # "success" | "partial" | "failed"
    rca_verdict_path: Path | None
    solution_verdict_path: Path | None
    rollback_needed: bool
    causal_files: list[str]
    remediation_tasks: str         # pre-formatted markdown
    tier: str
    agent_outputs: dict[str, Path]
    incident_summary: str
```

### Contract 4: Executor → Phase Subprocess (Resume Prompt)

Resume prompt includes:
- `/sc:task-unified` prefix with `--compliance strict`
- TFEP re-launch header
- Rollback notice (performed or not)
- Execution scope (skip prior tasks, execute remediation + verification)
- Git diff summary
- Result file path

### Contract 5: Incident Report Format

Written to `results/phase-{N}-tfep-incident.md` per FR-TFEP-08.

---

## 15. Test Strategy

### Unit Tests (tfep.py)

```python
# tests/sprint/test_tfep.py

class TestEscalationState:
    def test_first_trigger_returns_light(self): ...
    def test_second_trigger_returns_standard(self): ...
    def test_third_trigger_returns_halt(self): ...
    def test_new_failure_resets_counter(self): ...
    def test_same_failure_increments_counter(self): ...
    def test_budget_multiplier_by_tier(self): ...

class TestPerformRollback:
    def test_no_rollback_when_not_needed(self): ...
    def test_full_rollback_saves_patch(self): ...
    def test_selective_rollback_reverts_causal_only(self): ...
    def test_patch_preserved_on_selective(self): ...
    def test_no_git_repo_graceful_skip(self): ...

class TestInjectRemediationTasks:
    def test_inserts_after_last_completed_task(self): ...
    def test_uses_t50_id_range(self): ...
    def test_preserves_original_content(self): ...
    def test_format_matches_parse_tasklist_regex(self): ...

class TestBuildTfepResumePrompt:
    def test_includes_rollback_notice(self): ...
    def test_includes_skip_instruction(self): ...
    def test_includes_git_diff(self): ...
    def test_result_file_path_correct(self): ...
```

### Integration Tests (executor TFEP branch)

```python
# tests/sprint/test_tfep_integration.py

class TestTfepPhaseLoop:
    def test_tfep_halt_triggers_forensic(self, mock_subprocess): ...
    def test_tfep_resolved_continues_sprint(self, mock_subprocess): ...
    def test_tfep_third_trigger_halts_sprint(self, mock_subprocess): ...
    def test_tfep_rollback_then_relaunch(self, mock_subprocess): ...

class TestDeterminePhaseStatus:
    def test_tfep_halt_from_result_file(self): ...
    def test_tfep_halt_before_generic_halt(self): ...
    def test_generic_halt_unchanged(self): ...
```

### Monitor Tests

```python
# tests/sprint/test_monitor_tfep.py

class TestTfepSignalDetection:
    def test_detects_tfep_triggered(self): ...
    def test_detects_tfep_resolved(self): ...
    def test_detects_tfep_escalated(self): ...
    def test_increments_trigger_count(self): ...
```

### All tests use `_subprocess_factory` injection

Forensic subprocess tests use the existing `_subprocess_factory` pattern from `execute_phase_tasks()` — a callable that simulates subprocess behavior without actually spawning Claude:

```python
def mock_forensic_subprocess(prompt, output_file, **kwargs):
    # Write expected output files
    output_file.write_text('{"type":"result"}')
    # Write expected .md artifacts
    return 0  # exit code
```

---

## Appendix A: File-by-File Change Summary

| File | Lines Added (est.) | Lines Modified (est.) | Risk |
|------|-------------------|----------------------|------|
| `tfep.py` (NEW) | ~450 | 0 | Medium — new module, isolated |
| `executor.py` | ~80 | ~15 | High — core phase loop |
| `process.py` | ~60 | 0 | Low — additive |
| `monitor.py` | ~15 | ~5 | Low — pattern additions |
| `models.py` | ~20 | ~10 | Medium — enum changes |
| `commands.py` | ~10 | 0 | Low — additive |
| `diagnostics.py` | ~5 | ~3 | Low — enum addition |
| **Total** | **~640** | **~33** | |

---

*End of architecture design.*
