---
title: Sprint CLI - Cross-System Wiring Validation
generated: 2026-04-03
scope: Full pipeline connectivity verification
---

# Cross-System Wiring Validation

## Verification Methodology

This document validates that all sprint pipeline components are connected and functioning as documented, identifying confirmed wiring and gaps.

## Confirmed Wiring: Connected Systems

### 1. CLI Entry -> Config -> Executor

| From | To | Evidence |
|------|----|----------|
| `pyproject.toml:63` | `cli/main.py:20` | `superclaude = "superclaude.cli.main:main"` |
| `cli/main.py:356` | `sprint/commands.py:15` | `main.add_command(sprint_group, name="sprint")` |
| `commands.py:206` | `config.py:202` | `load_sprint_config(...)` call |
| `commands.py:249` | `executor.py:1112` | `execute_sprint(config)` call |

**Status**: FULLY WIRED

### 2. Config -> Phase Discovery -> Task Parsing

| From | To | Evidence |
|------|----|----------|
| `config.py:221` | `config.py:29` | `discover_phases(index_path)` |
| `executor.py:1102` | `config.py:306` | `parse_tasklist(content)` |
| `config.py:306` -> | `models.py:25` | Returns `TaskEntry` objects |

**Status**: FULLY WIRED

### 3. Executor -> Claude Process -> Monitor

| From | To | Evidence |
|------|----|----------|
| `executor.py:1251` | `process.py:88` | `ClaudeProcess(config, phase)` |
| `process.py:123` | `pipeline/process.py:71` | `build_command()` inherited |
| `process.py:170` | inference layer | `/sc:task-unified` prompt injection |
| `executor.py:1265` | `monitor.py:144` | `OutputMonitor` poll loop |

**Status**: FULLY WIRED

### 4. Status Classification -> Result Writing -> Logging

| From | To | Evidence |
|------|----|----------|
| `executor.py:1393` | `executor.py:1765` | `_determine_phase_status()` |
| `executor.py:1403` | `executor.py:1718` | `_write_executor_result_file()` |
| `executor.py:1135` | `logging_.py:12` | `SprintLogger` instance |
| `logging_.py:88` | filesystem | JSONL + MD log writes |

**Status**: FULLY WIRED

### 5. Gate Evaluation -> Pipeline Progression

| From | To | Evidence |
|------|----|----------|
| `pipeline/executor.py:192` | `pipeline/gates.py:20` | `gate_passed()` in retry loop |
| `pipeline/gates.py:20` | `roadmap/gates.py:785+` | `GateCriteria` constants consumed |
| Gate failure | `StepStatus.FAIL` | `pipeline/executor.py:270-283` |

**Status**: FULLY WIRED

### 6. Preflight -> Python-Mode Phases

| From | To | Evidence |
|------|----|----------|
| `executor.py:1173` | `preflight.py:90` | `execute_preflight_phases(config)` |
| `preflight.py:116` | `config.py:306` | `parse_tasklist()` for python tasks |
| `preflight.py:45` | filesystem | Evidence bundle writes |
| `executor.py:1491` | merge | Preflight results merged with main |

**Status**: FULLY WIRED

### 7. Tmux Relay -> Foreground Execution

| From | To | Evidence |
|------|----|----------|
| `commands.py:247` | `tmux.py:50` | `launch_in_tmux(config)` |
| `tmux.py:122` | CLI | `_build_foreground_command()` with `--no-tmux` |
| `tmux.py` reads | `.sprint-exitcode` | Sentinel file for exit status |

**Status**: FULLY WIRED

### 8. Trailing Gate -> Remediation -> KPI

| From | To | Evidence |
|------|----|----------|
| `executor.py:1154` | `trailing_gate.py` | `DeferredRemediationLog` construction |
| `executor.py:1510` | `kpi.py:148` | `build_kpi_report()` with trailing results |
| `kpi.py` | filesystem | `gate-kpi-report.md` write |

**Status**: FULLY WIRED

### 9. Roadmap State -> Sprint Fidelity Check

| From | To | Evidence |
|------|----|----------|
| roadmap executor | `.roadmap-state.json` | State write throughout execution |
| `commands.py:35` | `_check_fidelity()` | Reads state for blocking decision |
| `commands.py:231-240` | fidelity gate | Blocks sprint on unresolved fidelity |

**Status**: FULLY WIRED

### 10. Skill Command -> Skill Protocol -> Agent

| From | To | Evidence |
|------|----|----------|
| `process.py:170` | `/sc:task-unified` | Prompt string |
| `task-unified.md` | `sc-task-unified-protocol` | `> Skill` activation block |
| STRICT tier | `quality-engineer` agent | Skill protocol spawns sub-agent |

**Status**: FULLY WIRED (at inference layer)

## Identified Gaps: Disconnected or Partial Wiring

### Gap 1: Shadow Gates — Config Present, Runtime Missing

**Evidence**:
- Defined in models: `sprint/models.py:322`
- CLI option: `commands.py:145-149`
- Config propagation: `config.py:213, 263`
- **No runtime branch** in `execute_sprint()` or `execute_phase_tasks()` reads `config.shadow_gates`

**Impact**: Shadow gate feature is configurable but non-functional in sprint execution.

### Gap 2: Task Dependencies — Parsed but Not Enforced

**Evidence**:
- Parsing: `config.py:342-349, 389-394` extracts `TaskEntry.dependencies`
- Execution: `executor.py:956` iterates tasks in **input order only**
- **No topological sort** or dependency check before task execution

**Impact**: Tasks with dependencies execute regardless of dependency completion status. Order relies on document ordering convention.

### Gap 3: Per-Task Turn Counting — Stub

**Evidence**:
- `_run_task_subprocess()` returns `(exit_code, 0, output_bytes)` at line 1091-1092
- Comment: "Turn counting wired separately"
- **Actual turn count always 0**

**Impact**: TurnLedger budget accounting lacks accurate per-task granularity.

### Gap 4: PM Agent — Not Runtime-Wired to Sprint

**Evidence**:
- `pm_agent/confidence.py`, `self_check.py`, `reflexion.py` exist with full implementations
- **No import** of `pm_agent` in any `cli/sprint/` file
- Confidence behavior achieved via prompt protocol only (`task-unified.md:91`)

**Impact**: PM Agent quality patterns exist for pytest use but are not enforced programmatically in sprint runtime. Relies on Claude's adherence to prompt instructions.

### Gap 5: Execution Engine — Not Wired to Sprint

**Evidence**:
- `execution/parallel.py`, `reflection.py`, `self_correction.py` implement wave-based execution
- `execution/__init__.py:41` exposes `intelligent_execute()`
- **No caller** from `cli/sprint/` to any `execution/` module

**Impact**: Sprint uses its own sequential phase loop rather than the sophisticated parallel execution engine. Two parallel execution patterns exist independently.

## System Health Summary

| Subsystem | Status | Notes |
|-----------|--------|-------|
| CLI registration & dispatch | HEALTHY | Full Click chain wired |
| Config loading & validation | HEALTHY | Robust with fallbacks |
| Phase discovery & task parsing | HEALTHY | Regex + table + directory scan |
| Claude subprocess management | HEALTHY | Base + sprint process classes |
| NDJSON stream monitoring | HEALTHY | Real-time tool/task tracking |
| Status classification | HEALTHY | Multi-fallback decision tree |
| Gate evaluation (pipeline) | HEALTHY | Tiered enforcement + retry |
| Gate catalog (roadmap) | HEALTHY | 14+ gates with semantic checks |
| Artifact generation | HEALTHY | All outputs accounted for |
| Logging (JSONL + MD) | HEALTHY | Dual-format event logging |
| TUI display | HEALTHY | Rich terminal updates |
| Tmux relay | HEALTHY | Bidirectional sentinel protocol |
| Preflight (python-mode) | HEALTHY | Evidence bundles + result merge |
| Diagnostics | HEALTHY | Collector + classifier + reporter |
| KPI reporting | HEALTHY | Multi-section formatted output |
| Trailing gate remediation | HEALTHY | Async evaluation + persistence |
| Shadow gates | PARTIAL | Config exists, no runtime use |
| Task dependency ordering | PARTIAL | Parsed, not enforced |
| Per-task turn counting | STUB | Returns 0, marked "wired separately" |
| PM Agent runtime integration | NOT WIRED | Prompt-driven only |
| Execution engine integration | NOT WIRED | Separate standalone subsystem |

## Architecture Diagram: Full Pipeline Connectivity

```
[User] --superclaude sprint run--> [Click CLI]
                                       |
                        load_sprint_config()
                                       |
                   +---[tmux?]---+-----+-----+---[dry-run?]---+
                   |             |                              |
            launch_in_tmux   execute_sprint                _print_dry_run
                   |             |
            (re-invokes     +----+----+
             with --no-tmux)|         |
                        preflight  main loop
                            |         |
                   python tasks   FOR phase:
                   subprocess.run    |
                            |     mode?
                        evidence  claude -> ClaudeProcess
                        bundle           -> /sc:task-unified
                            |            -> NDJSON monitor
                            |            -> classify status
                            |            -> write result
                            |            -> gate check
                            |     skip -> SKIPPED result
                            |
                            +----merge results----+
                                                  |
                                          compute outcome
                                          build KPI report
                                          write exitcode
                                          cleanup + exit
```
