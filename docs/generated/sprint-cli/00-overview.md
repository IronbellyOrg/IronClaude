---
title: Sprint CLI Pipeline - Complete Architecture Overview
generated: 2026-04-03
scope: src/superclaude/cli/sprint/, src/superclaude/cli/pipeline/, src/superclaude/execution/
---

# Sprint CLI Pipeline - Architecture Overview

## Executive Summary

The Sprint CLI (`superclaude sprint run`) is a hybrid deterministic-inference pipeline that orchestrates multi-phase task execution by spawning Claude Code subprocesses. It combines a Python-based executor with inference-layer slash commands and skills to achieve autonomous, gate-validated task completion.

**Key architectural insight**: The sprint runner is a *process orchestrator*, not a task executor. It launches Claude CLI subprocesses with `/sc:task-unified` prompts and monitors their NDJSON output streams, classifying results via exit codes, checkpoint files, and output parsing.

## System Layers

```
+------------------------------------------------------------------+
|                    USER INVOCATION LAYER                          |
|  superclaude sprint run <tasklist-index.md> [options]             |
+------------------------------------------------------------------+
         |
         v
+------------------------------------------------------------------+
|                    CLI COMMAND LAYER                              |
|  commands.py -> config.py -> load_sprint_config()                |
|  Click group registration, arg parsing, tmux routing             |
+------------------------------------------------------------------+
         |
         v
+------------------------------------------------------------------+
|                    EXECUTION ORCHESTRATOR                         |
|  executor.py::execute_sprint(config)                             |
|  Phase loop -> Task loop -> Subprocess management                |
|  Signal handling, TUI, monitoring, diagnostics                   |
+------------------------------------------------------------------+
         |                              |
         v                              v
+-------------------------+  +---------------------------+
| PYTHON-MODE PREFLIGHT   |  | CLAUDE-MODE EXECUTION     |
| preflight.py            |  | process.py::ClaudeProcess |
| Direct subprocess.run() |  | claude --print -p <prompt>|
| of parsed commands      |  | /sc:task-unified ...      |
+-------------------------+  +---------------------------+
                                        |
                                        v
+------------------------------------------------------------------+
|                    INFERENCE LAYER                                |
|  /sc:task-unified -> sc:task-unified-protocol SKILL              |
|  Tier classification, verification routing, agent spawning       |
+------------------------------------------------------------------+
         |
         v
+------------------------------------------------------------------+
|                    VALIDATION & GATES                             |
|  pipeline/gates.py + roadmap/gates.py                            |
|  Tiered enforcement: EXEMPT < LIGHT < STANDARD < STRICT          |
|  Blocking gates halt; trailing gates log asynchronously           |
+------------------------------------------------------------------+
         |
         v
+------------------------------------------------------------------+
|                    ARTIFACT GENERATION                            |
|  logging_.py, diagnostics.py, kpi.py, trailing_gate.py           |
|  execution-log.{jsonl,md}, phase results, KPI reports            |
+------------------------------------------------------------------+
```

## Pipeline Flow Visualization

```
superclaude sprint run index.md
        |
        +-> load_sprint_config()
        |     +-> discover_phases(index_path)     # Parse index for phase files
        |     +-> _resolve_release_dir()           # Find release root
        |     +-> validate files/gaps/range        # Pre-flight checks
        |     +-> Build SprintConfig               # Hydrate all runtime config
        |
        +-> Dispatch decision
        |     +-> tmux available? -> launch_in_tmux(config)
        |     +-> else            -> execute_sprint(config)
        |
        +-> execute_sprint(config)
              |
              +-> Initialize systems
              |     +-> SignalHandler              # Graceful shutdown
              |     +-> SprintLogger               # JSONL + MD logging
              |     +-> SprintTUI                  # Rich terminal UI
              |     +-> OutputMonitor              # NDJSON stream parser
              |     +-> TurnLedger                 # Budget/economics
              |     +-> ShadowGateMetrics          # Gate telemetry
              |     +-> DeferredRemediationLog     # Trailing gate findings
              |
              +-> execute_preflight_phases()       # Python-mode phases first
              |
              +-> FOR EACH phase IN config.active_phases:
              |     |
              |     +-> Mode routing:
              |     |     python -> already preflighted, skip
              |     |     skip   -> synthesize SKIPPED result
              |     |     claude -> execute below
              |     |
              |     +-> CLAUDE MODE:
              |     |     |
              |     |     +-> _parse_phase_tasks() -> TaskEntry[]
              |     |     |
              |     |     +-> Tasks exist?
              |     |     |   YES -> execute_phase_tasks()
              |     |     |          FOR EACH task:
              |     |     |            spawn ClaudeProcess
              |     |     |            monitor NDJSON stream
              |     |     |            classify task result
              |     |     |          Post-phase wiring hook
              |     |     |
              |     |     |   NO  -> Freeform phase execution
              |     |     |          spawn single ClaudeProcess
              |     |     |          poll until exit
              |     |     |          classify via exit code + checkpoint
              |     |     |
              |     |     +-> _determine_phase_status()
              |     |     +-> _write_executor_result_file()
              |     |     +-> On failure: diagnostics + halt
              |     |
              |     +-> Append PhaseResult
              |
              +-> Merge preflight + main results
              +-> Compute SprintOutcome
              +-> build_kpi_report()
              +-> Cleanup + write .sprint-exitcode
```

## Component File Map

| Component | File | Key Entry Point |
|-----------|------|-----------------|
| CLI entry | `cli/main.py:356` | `main.add_command(sprint_group)` |
| Command group | `cli/sprint/commands.py:15` | `sprint_group` Click group |
| Run handler | `cli/sprint/commands.py:174` | `run()` Click command |
| Config loader | `cli/sprint/config.py:202` | `load_sprint_config()` |
| Phase discovery | `cli/sprint/config.py:29` | `discover_phases()` |
| Task parser | `cli/sprint/config.py:306` | `parse_tasklist()` |
| Sprint executor | `cli/sprint/executor.py:1112` | `execute_sprint()` |
| Phase task executor | `cli/sprint/executor.py:912` | `execute_phase_tasks()` |
| Status classifier | `cli/sprint/executor.py:1765` | `_determine_phase_status()` |
| Claude subprocess | `cli/sprint/process.py:88` | `ClaudeProcess` |
| Prompt builder | `cli/sprint/process.py:123` | `build_prompt()` |
| Base process | `cli/pipeline/process.py:71` | `build_command()` |
| Pipeline executor | `cli/pipeline/executor.py:46` | `execute_pipeline()` |
| Gate evaluator | `cli/pipeline/gates.py:20` | `gate_passed()` |
| Sprint models | `cli/sprint/models.py:297` | `SprintConfig` |
| Pipeline models | `cli/pipeline/models.py:77` | `Step`, `StepResult` |
| Output monitor | `cli/sprint/monitor.py:144` | `OutputMonitor` |
| Sprint logger | `cli/sprint/logging_.py:12` | `SprintLogger` |
| TUI | `cli/sprint/tui.py:59` | `SprintTUI` |
| Diagnostics | `cli/sprint/diagnostics.py:72` | `DiagnosticCollector` |
| KPI report | `cli/sprint/kpi.py:148` | `build_kpi_report()` |
| Preflight | `cli/sprint/preflight.py:90` | `execute_preflight_phases()` |
| Tmux launcher | `cli/sprint/tmux.py:50` | `launch_in_tmux()` |
| Notifications | `cli/sprint/notify.py:34` | `notify_phase_complete()` |
| Debug logger | `cli/sprint/debug_logger.py:69` | `setup_debug_logger()` |
| Classifiers | `cli/sprint/classifiers.py:19` | `empirical_gate_v1()` |

## Cross-Document Index

| Document | Contents |
|----------|----------|
| [01-entry-points.md](01-entry-points.md) | CLI registration, argument parsing, dispatch routing |
| [02-data-models.md](02-data-models.md) | All dataclasses, enums, model relationships |
| [03-execution-engine.md](03-execution-engine.md) | Phase loop, task execution, wave pattern, error handling |
| [04-gates-validation.md](04-gates-validation.md) | Gate system, semantic checks, enforcement tiers |
| [05-pm-agent.md](05-pm-agent.md) | Confidence, self-check, reflexion integration |
| [06-artifacts-output.md](06-artifacts-output.md) | All generated files, formats, and producers |
| [07-skills-commands.md](07-skills-commands.md) | Slash command and skill integration bridge |
| [08-test-coverage.md](08-test-coverage.md) | Test suite inventory and coverage analysis |
| [09-wiring-validation.md](09-wiring-validation.md) | Cross-system connectivity verification |
