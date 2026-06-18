# Sprint CLI Tools — Release Guide

This guide summarizes the sprint CLI tooling completed in this release, including:

- what each tool does,
- when to use it,
- how to run it,
- practical examples,
- and how it fits into the **spec → roadmap → tasklist → execution** workflow.

---

## 1) Release Summary (What was finalized)

### Core command surface

The `superclaude sprint` command group provides 5 subcommands:

1. `run`
2. `attach`
3. `status`
4. `logs`
5. `kill`

Implemented contract and options are defined in `src/superclaude/cli/sprint/commands.py`.

### Reliability and behavior updates included in this release

- **Canonical phase filename discovery** for 4 naming conventions (strict/near-match-safe)
- **Validation buckets** separated into `errors` and `warnings`
- **Executor timeout contract** hardened (`_timed_out` => `exit_code=124`)
- **Logging severity routing** made explicit (DEBUG/INFO/WARN/ERROR behavior)
- **Non-Unix process fallbacks** added (no unconditional `os.setpgrp`/`os.killpg`)
- **tmux graceful handling** improved when tmux is missing
- **tmux non-force kill escalation**: SIGTERM → wait → SIGKILL
- **CLI help contract hardening** (internal hidden options not exposed)
- **Auto-resume as default (v4.3.5)** for bare `sprint run` and `sprint rerun-tasks`, with explicit-flag opt-out, `--fresh`/`--restart`, `--yes`/`-y`, boundary integrity checks, and drift assessment
- **E2E brittleness removal** by patching `executor.shutil.which("claude")` in tests

---

## 2) Command Reference — When and How to Use

## `superclaude sprint run`

### What it does

Loads a tasklist index, discovers phases, validates phase files, and executes phases sequentially (usually in tmux unless `--no-tmux`). With no explicit `--start`/`--end` window, it now auto-resumes from the interrupted phase detected from on-disk sprint state.

Pre-flight behavior: execution fails fast if the `claude` binary is not in `PATH`.

### Use when

- You have a phase-based tasklist release package ready.
- You want deterministic, resumable execution over multiple phase files.
- You want strict task execution posture (`/sc:task-unified ... --compliance strict --strategy systematic`).

### Syntax

```bash
superclaude sprint run <index_path> [options]
```

### Key options

- Default auto-resume: bare `superclaude sprint run <index_path>` detects the interrupted phase from on-disk state, prints a resume plan + drift + integrity report, asks for confirmation, and resumes there
- `--start N` start from phase N; any explicit `--start` (including `--start 1`) disables auto-detection
- `--end N` stop at phase N (default: last discovered); explicit `--end` also disables auto-detection
- `--fresh` / `--restart` ignore prior on-disk state, disable auto-detection, and run cleanly from phase 1
- `--yes` / `-y` non-interactive assent for auto-resume confirmation; also honored via `SUPERCLAUDE_SPRINT_ASSUME_YES=1` or `CI=1`
- `--max-turns N` max turns per phase
- `--model MODEL` set Claude model
- `--max-session-resets N` max account-rotation re-spawns per phase (a shared budget across the phase's tasks, not per individual task) before a provider-exhaustion halt for a model switch (429 recovery: a fresh subprocess re-routes to a different CLIProxyAPI account). Default: `8`
- `--dry-run` discovery/validation only; with default auto-resume it also prints `ResumePlan`, `DriftAssessment`, and `BoundaryReport` without executing
- `--no-tmux` run in foreground even if tmux is available
- `--permission-flag` permission mode passed to Claude CLI
- `--force-fidelity-fail 'reason'` Bypass spec fidelity check
  - supported values: `--dangerously-skip-permissions` (default) and `--allow-hierarchical-permissions`
- `--ignore-run-lock` reclaim the release-level run-lock even if a live holder exists (loud warning; does NOT kill the other process). Unsafe — use only when a prior `sprint run` crashed and left a stale lock; concurrent runs on the same release dir can corrupt state
  
### Examples

```bash
# Full execution, or auto-resume if prior interrupted state exists (tmux auto if available)
superclaude sprint run .dev/releases/current/tasklist-index.md

# Auto-resume non-interactively after reviewing the printed resume plan
superclaude sprint run .dev/releases/current/tasklist-index.md --yes

# Explicit-window override: re-run phase 4 through phase 8 and bypass auto-detection
superclaude sprint run .dev/releases/current/tasklist-index.md --start 4 --end 8

# Validate discovered phases only; with auto-resume state, also print the resume plan, drift assessment, and boundary report
superclaude sprint run .dev/releases/current/tasklist-index.md --dry-run

# Foreground execution for CI/local debugging
superclaude sprint run .dev/releases/current/tasklist-index.md --no-tmux

# Use Claude hierarchical permissions instead of the default skip-permissions mode
superclaude sprint run .dev/releases/current/tasklist-index.md \
  --permission-flag --allow-hierarchical-permissions
```

---

## `superclaude sprint attach`

### What it does

Attaches to a running `sc-sprint-*` tmux session.

### Use when

- A sprint is already running in tmux and you want live visibility.

### Example

```bash
superclaude sprint attach
```

---

## `superclaude sprint status`

### What it does

Intended to show current sprint status from execution logs.

### Current release note

`status` is wired but currently emits a placeholder message from `logging_.py` (`read_status_from_log`) and is not yet connected to active sprint state parsing.

### Example

```bash
superclaude sprint status
```

---

## `superclaude sprint logs`

### What it does

Intended to tail sprint log output.

### Current release note

`logs` is wired but currently a stub message in `logging_.py` (`tail_log`).

### Example

```bash
superclaude sprint logs -n 100
superclaude sprint logs -f
```

---

## `superclaude sprint kill`

### What it does

Stops running sprint tmux session.

### Modes

- `kill --force`: immediate tmux kill-session
- `kill` (non-force): escalation path
  1. SIGTERM to pane PID (or Ctrl-C fallback)
  2. wait 10 seconds
  3. SIGKILL if still alive
  4. kill tmux session

### Use when

- A sprint is stalled/hung or needs controlled stop.

### Examples

```bash
# Graceful stop with escalation
superclaude sprint kill

# Immediate stop
superclaude sprint kill --force
```

---

## 3) End-to-End Workflow: Spec → Roadmap → Tasklist → Task Execution

This sprint CLI is the execution layer for your release pipeline.

## Stage A: Spec (requirements source)

Create/maintain release spec with acceptance criteria and expected outputs.

## Stage B: Roadmap (phase planning)

Translate spec into phases (delivery order, dependencies, quality gates).

## Stage C: Tasklist Index + Phase Files (execution plan)

Prepare:

- one `tasklist-index.md`
- one or more canonical phase files

Canonical file name patterns recognized by discovery:

1. `phase-<N>-tasklist.md`
2. `p<N>-tasklist.md`
3. `phase_<N>_tasklist.md`
4. `tasklist-p<N>.md`

Near-match forms are intentionally rejected to avoid accidental pickup.

## Stage D: Sprint execution

Run:

```bash
superclaude sprint run <tasklist-index.md>
```

For each phase, sprint runtime:

1. launches fresh Claude process,
2. monitors output and updates TUI,
3. enforces timeout/interrupt handling,
4. parses phase result (`EXIT_RECOMMENDATION`/status),
5. records dual logs (JSONL + Markdown),
6. continues or halts.

## Stage E: Resume on halt

If halted, run the same bare command again:

```bash
superclaude sprint run <tasklist-index.md>
```

By default, sprint auto-detects the interrupted phase from on-disk state, treats atomic `phase-N-result.json` as the truth anchor, prints the `ResumePlan`, `DriftAssessment`, and `BoundaryReport`, asks for confirmation, and resumes there. On the task-level path it re-runs only the unfinished task. The generated `--start <halt_phase>` command still works as an explicit-window override and disables auto-detection; use `--fresh` / `--restart` to discard prior state and run cleanly from phase 1.

## Stage F: Granular per-task rerun (v4.3.0+)

Bare `superclaude sprint rerun-tasks <tasklist-index.md>` now auto-detects the boundary phase and its recoverable failed-task set. Use it when a sprint has enough on-disk state to identify the interrupted task-level seam:

```bash
superclaude sprint rerun-tasks <tasklist-index.md>
```

`--start <halt_phase>` re-runs an **entire** phase, and explicit `--phase`/`--tasks` remain the manual selector override for granular recovery. When only a few tasks in an otherwise-passing phase failed — typically a transient cause such as an API outage or a timeout — use `superclaude sprint rerun-tasks` instead to re-execute **only the detected or named tasks** and merge their results back:

```bash
superclaude sprint rerun-tasks <tasklist-index.md> --phase 7 --tasks T07.11,T07.12
```

This explicit example re-runs just `T07.11` and `T07.12` in an isolated bundle, leaves the
other tasks in phase 7 untouched, and (by default) merges the new results back
into the canonical results directory and tasklist, then runs
`verify-checkpoints --recover` to regenerate any missing checkpoint reports.
See [§6 Use case 5](#use-case-5-recover-a-few-failed-tasks-without-rerunning-the-whole-phase)
for the full option reference.

---

## 4) Behind the Scenes: What the Python sprint runtime actually executes

This section explains what happens inside the Python runtime so users understand exactly what is being launched.

### 4.1 `superclaude sprint run` call path

When you run:

```bash
superclaude sprint run <tasklist-index.md> [flags]
```

the CLI flow is:

1. `commands.py::run()` parses options.
2. If no explicit `--start`/`--end` window and no `--fresh` are present, the auto-resume planner reconstructs the boundary from on-disk state, then the drift assessor and boundary integrity gate validate the seam before execution.
3. `config.py::load_sprint_config()` discovers phases and validates range/files.
4. If `--dry-run`: prints the discovered plan; on the auto-resume path it also prints `ResumePlan`, `DriftAssessment`, and `BoundaryReport`, then exits.
5. If tmux is available and `--no-tmux` is not set: `tmux.py::launch_in_tmux()`.
6. Otherwise: `executor.py::execute_sprint()` in foreground, or the task-level resume dispatches through the existing `rerun-tasks` engine.

### 4.2 What command is run for each phase

For each phase, the runtime spawns a fresh Claude CLI process from `process.py::build_command()`.

Effective command shape:

```bash
claude \
  --print \
  <permission-flag> \
  --no-session-persistence \
  --max-turns <N> \
  --output-format text \
  -p "<generated /sc:task-unified prompt>" \
  [--model <model-if-provided>]
```

Important details:

- `--no-session-persistence` ensures phase isolation.
- The runtime forwards the configured permission flag verbatim; supported choices are `--dangerously-skip-permissions` and `--allow-hierarchical-permissions`.
- `CLAUDECODE=""` is injected into child env to avoid nested session detection behavior.
- stdout/stderr are redirected to per-phase files in `results/`.

### 4.3 What prompt is sent to Claude

The sprint runtime generates a structured prompt (from `process.py::build_prompt()`) that begins with:

```text
/sc:task-unified Execute all tasks in @<phase-file> --compliance strict --strategy systematic
```

It then includes execution rules and completion protocol (including writing phase result file and explicit `EXIT_RECOMMENDATION`).

### 4.3.1 How the prompt builder works (detailed)

`build_prompt()` is deterministic and phase-aware. It composes a single multiline prompt from runtime config + phase metadata.

Inputs used by the builder:

- `phase.number` for task-ID format expectations (`T{phase}XX.*`)
- `phase.file` for `@<phase-file>` inclusion
- `config.result_file(phase)` for the required completion report destination

Prompt structure emitted by the builder:

1. **Command header**
   - `/sc:task-unified ... --compliance strict --strategy systematic`
2. **Execution Rules** block
   - task ordering expectations
   - tier-specific verification expectations
   - halt/continue behavior semantics
3. **Completion Protocol** block
   - exact report destination path
   - required report schema items (frontmatter, status table, evidence, files changed)
   - explicit required literal token:
     - `EXIT_RECOMMENDATION: CONTINUE` or
     - `EXIT_RECOMMENDATION: HALT`
4. **Important** block
   - phase-context boundaries (do current phase only)
   - no re-execution of prior-phase work

Why this matters:

- Keeps each spawned Claude process aligned to the same contract.
- Produces machine-parseable completion artifacts for `_determine_phase_status()`.
- Reduces ambiguity by embedding both policy and output contract in the prompt itself.

Operational consequence:

- If a phase agent does not emit the required recommendation token or valid status hints, executor falls back to `PASS_NO_SIGNAL`, `PASS_NO_REPORT`, or `ERROR` paths based on available artifacts.

### 4.4 tmux mode: what is launched

If tmux mode is selected, runtime creates a deterministic session name (`sc-sprint-<hash>`) and launches a foreground sprint command inside tmux.

Foreground command built by runtime:

```bash
superclaude sprint run <index> --no-tmux --start <N> --max-turns <N> --permission-flag <flag> [--end <N>] [--model <M>] [--tmux-session-name <name>]
```

Then it:

- splits a bottom pane to tail phase output,
- keeps top pane for TUI,
- attaches user to the tmux session.

### 4.5 Stop/kill behavior internals

`superclaude sprint kill` (non-force) performs escalation:

1. target pane PID lookup,
2. SIGTERM,
3. wait 10s,
4. SIGKILL if still alive,
5. kill tmux session.

If pane PID is unavailable, fallback sends Ctrl-C to pane before cleanup.

---

## 5) Runtime Behavior Details (Important)

## Phase status semantics

Phase statuses include:

- success: `pass`, `pass_no_signal`, `pass_no_report`
- failures: `halt`, `timeout`, `error`

Decision highlights:

- `exit_code == 124` => `timeout`
- non-zero exit (except 124 handling) => `error`
- `EXIT_RECOMMENDATION: HALT` wins over `CONTINUE` if both appear
- `status: PARTIAL` => `halt`

## Logging severity routing

- **DEBUG** (`pass_no_signal`): JSONL only
- **INFO** (`pass`, `pass_no_report`): screen + JSONL (+ markdown row)
- **WARN** (`halt`, `timeout`): highlighted stderr + JSONL (+ markdown row)
- **ERROR** (`error`): highlighted stderr + bell + JSONL (+ markdown row)

## Process portability

- Unix process-group operations are used when available.
- Fallback path uses process-level `terminate()/kill()` on non-Unix environments.

## tmux resilience

- If tmux is not installed, discovery returns no session gracefully.
- Non-force kill follows escalation behavior rather than immediate hard kill.

## Auto-resume safety

- Bare `sprint run <index>` and bare `sprint rerun-tasks <index>` are non-destructive by default and plan from on-disk state before mutating anything.
- Atomic `phase-N-result.json` is the truth anchor for completed/interrupted boundary detection.
- The boundary integrity gate doubly-validates the last-completed task before allowing new work to layer onto the resume seam.
- The drift assessor blocks auto-resume if the boundary tasklist was materially edited and confidence falls below `0.8`; choose an explicit window/selector or `--fresh` when you intend to override prior state.

---

## 6) Practical Use Cases

## Use case 1: Normal release execution

```bash
superclaude sprint run .dev/releases/current/tasklist-index.md
```

Best for long-running multi-phase execution with reconnect support via tmux.

## Use case 2: Safe preflight before execution

```bash
superclaude sprint run .dev/releases/current/tasklist-index.md --dry-run
```

Confirms discovery/range before consuming runtime. If prior interrupted state exists and no explicit window is supplied, it also prints the auto-resume `ResumePlan`, `DriftAssessment`, and `BoundaryReport` without executing.

## Use case 3: Recover from mid-release halt

```bash
superclaude sprint run .dev/releases/current/tasklist-index.md
```

Bare `sprint run` auto-resumes from the interrupted phase indicated by on-disk state and asks for confirmation after printing the resume, drift, and integrity reports. If you need to force the old explicit-window behavior, pass `--start 5` (or `--start 5 --end 8`); any explicit `--start`/`--end`, including `--start 1`, disables auto-detection.

## Use case 4: CI/ephemeral shell environment

```bash
superclaude sprint run .dev/releases/current/tasklist-index.md --no-tmux
```

Avoids tmux dependency in constrained runners.

## Use case 5: Recover a few failed tasks without rerunning the whole phase

When a phase mostly passed but a handful of tasks failed (often transiently),
re-running the entire phase with `--start N` wastes runtime and tokens on the
tasks that already passed. Bare `sprint rerun-tasks <index>` now auto-detects
the boundary phase and recoverable failed-task set, then re-executes only those
tasks and merges their results back atomically.

**Motivating example.** In a 21-task phase 7, tasks `T07.11` and `T07.12`
failed on a transient API outage. Rather than re-running all 21:

```bash
# Auto-detect the boundary phase and recoverable failed tasks:
superclaude sprint rerun-tasks .dev/releases/current/tasklist-index.md

# Manual explicit-selector override, preview first (no state mutation):
superclaude sprint rerun-tasks .dev/releases/current/tasklist-index.md \
  --phase 7 --tasks T07.11,T07.12 --dry-run

# Then run the explicit selector for real:
superclaude sprint rerun-tasks .dev/releases/current/tasklist-index.md \
  --phase 7 --tasks T07.11,T07.12
```

By default the rerun results are merged back into the canonical results
directory and the phase tasklist, after which a `verify-checkpoints --recover`
pass regenerates any missing checkpoint reports.

### Options reference

`superclaude sprint rerun-tasks <tasklist-index.md> [OPTIONS]` — `<tasklist-index.md>`
is the same index `sprint run` consumes.

| Option | Purpose |
|--------|---------|
| bare invocation | With no `--phase`/`--tasks`/`--from-reflect-report`, auto-detect the boundary phase and recoverable failed-task set, then proceed as if those selectors were supplied. |
| `--phase N` | The phase number containing the failed tasks; explicit selectors disable auto-detection. |
| `--tasks T07.11,T07.12` | Comma-separated task IDs to re-run; explicit selectors disable auto-detection. |
| `--from-reflect-report PATH` | **Reserved for v4.4.0 (SprintRunReflect).** Intended to let a reflect report nominate the failed tasks; mutually exclusive with `--phase`/`--tasks`. **Not yet functional in v4.3.0** — it aborts with a deferral message. Use `--phase`/`--tasks` for manual nomination. |
| `--merge-back` / `--no-merge-back` | Merge rerun results back into canonical results + tasklist. **Default: merge back.** Use `--no-merge-back` to leave results isolated in the bundle for inspection. |
| `--dry-run` | Print the rerun plan (nominated + dependency-resolved tasks, bundle dir) and exit without mutating anything. |
| `--fresh` / `--restart` | Disable auto-detection and require explicit `--phase`/`--tasks` (or `--from-reflect-report`). |
| `--yes` / `-y` | Non-interactive assent; also honored via `SUPERCLAUDE_SPRINT_ASSUME_YES=1` or `CI=1`. |
| `--include-transitive` | Also re-run tasks that transitively depend on the named tasks. |
| `--ignore-deps` | Skip dependency resolution; re-run exactly the named tasks. |
| `--force-merge` | Escape hatch: merge even if the source tasklist's content changed since the rerun started. Normally the rerun's own provenance write does **not** trip this guard — only a real operator edit does. |
| `--allow-loop` | Bypass the retry-cap-3 guard (a task is normally refused after 3 reruns). |
| `--no-verify-checkpoints` | Skip the post-merge `verify-checkpoints --recover` pass. |
| `--bundle-dir PATH` | Explicit recovery-bundle directory (default: auto-suffixed under `results/`). |
| `--restore` | Restore deliverables and checkboxes from a prior aborted rerun bundle (recover from a botched merge-back). |

**Safety defenses (automatic).** A concurrent-rerun lock prevents two reruns of
the same phase at once; a SHA guard aborts if the source tasklist was edited
mid-rerun (override with `--force-merge`); the retry cap stops runaway loops
after 3 attempts (override with `--allow-loop`); partial deliverables are
stashed and restored on abort; and prior outputs are preserved with a
`.failed-<timestamp>` forensic rename rather than overwritten.

---

## 7) Authoring Checklist for Tasklist Packages

Before running sprint:

- [ ] index file exists and is readable
- [ ] phase files follow one of the 4 canonical names
- [ ] start/end range maps to at least one active phase
- [ ] each phase has clear task IDs and acceptance criteria
- [ ] release directory writable (for `results/` and execution logs)

After run:

- [ ] inspect `execution-log.md` summary
- [ ] inspect `execution-log.jsonl` for machine-readable telemetry
- [ ] use bare `superclaude sprint run <index>` to auto-resume if outcome halted, or an explicit `--start` window when you intentionally want to override auto-detection

---

## 8) Quick Command Cheat Sheet

```bash
# Start sprint, or auto-resume an interrupted sprint by default
superclaude sprint run <index>

# Auto-resume non-interactively after printing the resume/drift/integrity reports
superclaude sprint run <index> --yes

# Ignore prior state and run cleanly from phase 1
superclaude sprint run <index> --fresh

# Start specific range; explicit --start/--end disables auto-detection
superclaude sprint run <index> --start 2 --end 6

# Dry-run only; auto-resume dry-run also prints ResumePlan/DriftAssessment/BoundaryReport
superclaude sprint run <index> --dry-run

# Force foreground
superclaude sprint run <index> --no-tmux

# Run with hierarchical permissions
superclaude sprint run <index> --permission-flag --allow-hierarchical-permissions

# Auto-detect and rerun recoverable failed tasks only
superclaude sprint rerun-tasks <index>

# Explicit granular rerun selector; explicit --phase/--tasks disables auto-detection
superclaude sprint rerun-tasks <index> --phase 7 --tasks T07.11,T07.12

# Attach to running tmux sprint
superclaude sprint attach

# Stop sprint gracefully (with escalation)
superclaude sprint kill

# Stop sprint immediately
superclaude sprint kill --force
```

---

## 9) Notes for the Spec→Roadmap→Tasklist pipeline owners

- Keep roadmap phases aligned to actual canonical file names to guarantee deterministic discovery.
- Treat `status` and `logs` subcommands as placeholders in this release (wired, not fully implemented).
- Prefer explicit acceptance evidence in phase outputs (`EXIT_RECOMMENDATION`, status frontmatter, modified files list) to maximize executor determinism.
- Use `--dry-run` as an automated gate between roadmap generation and execution kickoff.
