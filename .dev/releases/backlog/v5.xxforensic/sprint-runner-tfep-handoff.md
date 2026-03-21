# Sprint Runner TFEP Integration — Formal Handoff

**Purpose**: Complete requirements specification for integrating the Test Failure Escalation Protocol (TFEP) into the `superclaude sprint run` CLI runner, enabling parallel forensic subprocess orchestration, adversarial adjudication, and phase re-launch with rollback.

**Date**: 2026-03-21
**Source**: Brainstorm session on sprint runner changes needed after TFEP protocol additions to `sc:task-unified` and forensic spec refactoring.
**Prerequisites**: Phase 1-3 of the forensic refactor tasklist (completed 2026-03-19) — TFEP rules in `sc-task-unified-protocol/SKILL.md`, forensic spec quick mode, return contract, and full integration wiring.

---

## 1. Problem Statement

The sprint runner (`superclaude sprint run`) operates as a phase-level sequencer: one Claude subprocess per phase, success/failure classified from exit codes and result files, sprint halts on first failing phase. TFEP changes Claude's behavior *inside* a sprint phase — when tests fail, Claude now halts instead of ad-hoc patching. But the runner has no awareness of TFEP events, cannot orchestrate forensic analysis, and cannot resume a phase after remediation.

### Current Runner Architecture (Key Facts)

- **Phase-oriented, not task-oriented**: One `claude --print --verbose -p <prompt>` subprocess per phase. Claude executes all tasks from the phase file internally.
- **Prompt**: `/sc:task-unified Execute all tasks in @{phase_file} --compliance strict --strategy systematic`
- **Status classification**: Exit code + result file (`EXIT_RECOMMENDATION: CONTINUE|HALT`) + output heuristics + checkpoint recovery.
- **On failure**: Diagnostics → `HALTED` → sprint stops. No retry, no re-launch.
- **Isolation**: Per-phase isolation directory under `results/.isolation/phase-N/`. Phase file copied there; `CLAUDE_WORK_DIR` set to isolation dir.
- **Monitor**: NDJSON sidecar thread extracts task IDs, tool names, file changes via regex. No TFEP awareness.
- **No IPC**: Claude subprocess is batch (`--print`), not interactive. Runner cannot send data to a live subprocess.

### What TFEP Needs From the Runner

1. Detect when Claude triggers TFEP (not just generic failure)
2. Spawn parallel forensic investigation subprocesses with independent context budgets
3. Spawn an adversarial judge subprocess to adjudicate parallel findings
4. Roll back bad prior work when the phase's code changes caused the failure
5. Re-launch the phase with remediation tasks injected and a resume-aware prompt
6. Extend timeout/budget for phases undergoing TFEP
7. Track escalation across re-launches (light → standard → halt)
8. Produce TFEP-specific diagnostics and incident reports

---

## 2. Architectural Decision: Parallel Forensic Subprocesses

### Decision

Forensic analysis runs as **runner-orchestrated parallel Claude subprocesses**, NOT as a skill invocation inside the phase subprocess. Each forensic agent gets its own full context window.

### Rationale

- The phase subprocess may be near context exhaustion when TFEP triggers
- Light-tier forensic is ~5-8K tokens; standard-tier is ~15-20K. Running inside the phase risks context overflow.
- Independent subprocesses enable true parallel investigation with no shared-budget contention
- The runner already knows how to spawn and monitor Claude subprocesses (`ClaudeProcess`)
- The failure context YAML provides all information forensic agents need — they don't need the phase's in-session state

### Execution Pattern

```
Phase subprocess exits with TFEP_HALT
         │
         ▼
   ┌─────────────┐
   │ Runner       │ ── reads failure_context.yaml
   │ orchestrates │
   └──────┬──────┘
          │
    ┌─────┴─────┐       (Light tier: 4-step pipeline)
    │           │
    ▼           ▼
  RCA-A       RCA-B      ← 2 parallel Claude subprocesses
  (Sonnet)   (Sonnet)       each runs /sc:troubleshoot
    │           │
    └─────┬─────┘
          ▼
    Judge (adversarial)   ← 1 Claude subprocess
    /sc:adversarial         --compare --depth quick
          │
          ▼
       rca-verdict.md
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
  Sol-A       Sol-B      ← 2 parallel Claude subprocesses
  (Sonnet)   (Sonnet)       each runs /sc:brainstorm
    │           │
    └─────┬─────┘
          ▼
    Judge (adversarial)   ← 1 Claude subprocess
    /sc:adversarial         --compare --depth quick
          │
          ▼
    solution-verdict.md
          │
          ▼
   ┌─────────────┐
   │ Runner       │ ── rollback if needed
   │ re-launches  │ ── inject remediation tasks
   │ phase        │ ── resume-aware prompt
   └─────────────┘
```

For **standard tier** (2nd escalation):
```
Phase subprocess exits with TFEP_HALT (2nd time)
         │
         ▼
    ┌─────┴─────┐       (Standard tier: 2-step pipeline)
    │           │
    ▼           ▼
  Full-A      Full-B    ← 2 parallel Claude subprocesses
  (Sonnet)   (Sonnet)      each does FULL investigation (RCA + solution)
    │           │
    └─────┬─────┘
          ▼
    Judge (adversarial)  ← 1 Claude subprocess
          │
          ▼
   Runner re-launches phase
```

---

## 3. Functional Requirements

### FR-TFEP-01: TFEP Signal Detection (Monitor)

The output monitor SHALL detect TFEP events via two mechanisms:

**Real-time (NDJSON scanning)**:
- Add regex patterns to `monitor.py` for `TFEP_TRIGGERED`, `TFEP_RESOLVED`, `TFEP_ESCALATED`
- Update `MonitorState` with fields: `tfep_triggered: bool`, `tfep_trigger_count: int`, `tfep_status: str`
- Detection drives TUI display and log output

**Post-hoc (file presence)**:
- After phase subprocess exits, check for `failure_context.yaml` in the working directory
- Check result file for `EXIT_RECOMMENDATION: TFEP_HALT` (distinct from generic `HALT`)

**Files to modify**:
- `src/superclaude/cli/sprint/monitor.py` — add TFEP patterns, update `_extract_signals_from_text()`
- `src/superclaude/cli/sprint/models.py` — add TFEP fields to `MonitorState`

### FR-TFEP-02: Phase Status Extension

Add new `PhaseStatus` enum values:

```python
TFEP_HALT = "tfep_halt"          # Phase halted due to TFEP trigger
TFEP_RESOLVED = "tfep_resolved"  # Phase completed after TFEP remediation
```

**Behavior**:
- `TFEP_HALT` → triggers forensic orchestration + one re-launch attempt. If re-launch also fails → true `HALT`, sprint stops.
- `TFEP_RESOLVED` → classified as success (`is_success = True`). Sprint continues.

**Classification rule in `_determine_phase_status()`**:
- If result file contains `EXIT_RECOMMENDATION: TFEP_HALT` → return `PhaseStatus.TFEP_HALT`
- This check must come BEFORE the generic `HALT` check (higher priority)

**Files to modify**:
- `src/superclaude/cli/sprint/models.py` — add enum values, update `is_success`, `is_failure`, `is_terminal`
- `src/superclaude/cli/sprint/executor.py` — update `_determine_phase_status()`, update phase loop to handle `TFEP_HALT`

### FR-TFEP-03: Parallel Forensic Subprocess Orchestration

When the runner detects `TFEP_HALT`:

1. Read `failure_context.yaml` from the phase working directory
2. Determine forensic tier from escalation count (1st = light, 2nd = standard)
3. Spawn N parallel Claude subprocesses (default N=2), each running the forensic investigation task
4. Wait for all parallel agents to complete
5. Spawn adversarial judge subprocess to compare outputs
6. Collect adjudicated verdict

**Subprocess configuration**:
- Model: Sonnet (default). Overridable via `--tfep-model <model>` on the sprint runner.
- Max turns: 50 per forensic agent (configurable)
- Timeout: 300s per forensic agent
- Output format: `stream-json` (consistent with phase subprocesses)
- Output files: `results/phase-{N}-tfep/rca-{alpha|bravo}.md`, `results/phase-{N}-tfep/solution-{alpha|bravo}.md`

**Files to modify/create**:
- `src/superclaude/cli/sprint/executor.py` — add `_orchestrate_tfep()` function
- `src/superclaude/cli/sprint/tfep.py` — NEW file, forensic subprocess orchestration logic
- `src/superclaude/cli/sprint/commands.py` — add `--tfep-model` and `--tfep-agents` flags

### FR-TFEP-04: Configurable Agent Shape

**Light tier** (1st TFEP trigger):
- Step 1: 2 parallel RCA agents, each prompted with `/sc:troubleshoot` + failure context
- Step 2: 1 adversarial judge, `/sc:adversarial --compare rca-alpha.md,rca-bravo.md --depth quick`
- Step 3: 2 parallel solution agents, each prompted with `/sc:brainstorm` + RCA verdict
- Step 4: 1 adversarial judge, `/sc:adversarial --compare solution-alpha.md,solution-bravo.md --depth quick`
- Total invocations: 6

**Standard tier** (2nd TFEP trigger):
- Step 1: 2 parallel full-investigation agents, each does complete RCA + solution
- Step 2: 1 adversarial judge, `/sc:adversarial --compare full-alpha.md,full-bravo.md --depth quick`
- Total invocations: 3

**Configuration**:
- `--tfep-agents N` flag (default: 2, range: 2-4)
- Adversarial judge always uses `--depth quick`

### FR-TFEP-05: Phase Re-launch with Resume

After forensic produces adjudicated remediation:

1. **Insert remediation tasks** into the phase tasklist file (in isolation dir) before test/verification tasks
   - Remediation task IDs use `T{XX}.50+` range to avoid collision with original tasks (T{XX}.01-T{XX}.20)
   - Format matches existing tasklist format: `### T{XX}.50 -- {title}` with `**Deliverables:**` and checklist items
2. **Build resume prompt** (different from `build_prompt()`):
   - "This is a TFEP remediation re-launch for Phase {N}"
   - "Prior work through task T{XX}.{YY} was [completed | rolled back]. See Git Changes below."
   - "Execute ONLY the remediation tasks (T{XX}.50+) and then re-run verification."
   - "Do NOT re-execute earlier tasks."
   - Include `build_task_context()` output with git diff summary
3. **Launch** with extended budget (see FR-TFEP-06)

**Files to modify**:
- `src/superclaude/cli/sprint/process.py` — add `build_tfep_resume_prompt()` method
- `src/superclaude/cli/sprint/tfep.py` — add `inject_remediation_tasks()` function

### FR-TFEP-06: Timeout Extension

When TFEP triggers:
- Extend phase timeout by **+600s (10 minutes)** per TFEP trigger detected
- For re-launched phases, multiply `max_turns` by **1.5x** (configurable)
- The forensic subprocesses have their own independent timeouts (300s each), separate from the phase budget

**Configuration**:
- `--tfep-budget-multiplier` flag (default: 1.5, range: 1.0-3.0)

**Files to modify**:
- `src/superclaude/cli/sprint/executor.py` — apply multiplier when re-launching
- `src/superclaude/cli/sprint/models.py` — add `tfep_budget_multiplier` to `SprintConfig`

### FR-TFEP-07: Escalation Across Re-launches

| Trigger | Action | Budget |
|---------|--------|--------|
| 1st TFEP on phase | Light tier forensic (4-step), re-launch phase | max_turns × 1.5 |
| 2nd TFEP on same phase | Standard tier forensic (2-step), re-launch phase | max_turns × 2.0 |
| 3rd TFEP on same phase | **HALT sprint**. Report to operator. | N/A |

- Escalation counter is per-phase, resets between phases
- "Same failure" = same test function(s) fail after remediation. "New failure" = different tests fail → resets counter to 1 (treated as fresh TFEP trigger)
- Counter stored in executor state, not persisted to disk (resets on sprint resume)

### FR-TFEP-08: TFEP Incident Logging

After each TFEP cycle, write `results/phase-{N}-tfep-incident.md`:

```markdown
# TFEP Incident Report — Phase {N}

## Trigger
- **Rule matched**: {which threshold rule fired}
- **Escalation count**: {1, 2, or 3}
- **Failing tests**: {test names and pre-existing/new classification}

## Forensic Investigation
- **Tier**: {light|standard}
- **Parallel agents**: {N}
- **RCA Agent A**: {path to output}
- **RCA Agent B**: {path to output}
- **Adversarial verdict**: {path to verdict}

## Remediation
- **Root cause**: {summary from rca-verdict.md}
- **Solution**: {summary from solution-verdict.md}
- **Rollback performed**: {yes/no, files rolled back}
- **Rollback patch**: {path to .patch file if applicable}

## Outcome
- **Phase re-launch**: {success|failed|escalated}
- **Tests after remediation**: {pass|fail}
```

### FR-TFEP-09: Protocol Output Markers

Update `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` to require Claude to emit structured markers:

- When TFEP triggers: write `TFEP_TRIGGERED` to stdout (captured in NDJSON output)
- When writing failure context: include path in result file
- Result file must contain `EXIT_RECOMMENDATION: TFEP_HALT` (not generic `HALT`)
- When TFEP resolves within session: write `TFEP_RESOLVED` to stdout
- When TFEP escalates: write `TFEP_ESCALATED` to stdout

These markers enable FR-TFEP-01 (monitor detection).

### FR-TFEP-10: Rollback on Wrong Prior Work

When TFEP forensic determines that the phase subprocess's code changes caused the test failure:

1. **Save patch**: `git diff > results/phase-{N}-tfep-rollback.patch` (audit trail of what was tried and failed)
2. **Clean revert**: `git checkout -- .` to revert all phase changes
3. **Update resume prompt**: "Prior implementation for tasks T{XX}.01-T{XX}.{YY} was rolled back because it caused test failures. The remediation plan below supersedes the original task approach."
4. The re-launched subprocess re-implements the affected tasks using the adjudicated remediation plan instead of the original tasklist instructions

**Rollback scope determination**:
- Read `rca-verdict.md` to identify which files from `changes_made` in the failure context are identified as causal
- If ALL files are causal → full `git checkout -- .`
- If SOME files are causal → selective `git checkout -- <causal_files>`
- The patch file is always saved regardless of scope

**Rollback safety**:
- Only revert files that were changed DURING this phase (tracked by git diff against the phase start commit)
- Never revert files changed by prior phases
- The runner captures `git rev-parse HEAD` at phase start for diff baseline

**Files to modify/create**:
- `src/superclaude/cli/sprint/tfep.py` — add `perform_rollback()` function
- `src/superclaude/cli/sprint/executor.py` — capture git baseline at phase start

---

## 4. Non-Functional Requirements

### NFR-TFEP-01: No Phase Subprocess IPC

The runner does NOT send data back to a live Claude subprocess. The pattern is always:
- Claude exits → runner orchestrates → runner re-launches Claude

This avoids IPC complexity. Claude's work is preserved on disk, and the re-launched subprocess picks up via resume prompt + git diff context.

### NFR-TFEP-02: Forensic Subprocess Isolation

Each forensic subprocess runs in its own isolation directory under `results/phase-{N}-tfep/`:
- `rca-alpha/` — RCA agent A working directory
- `rca-bravo/` — RCA agent B working directory
- `solution-alpha/` — Solution agent A working directory
- `solution-bravo/` — Solution agent B working directory
- `judge/` — Adversarial judge working directory

### NFR-TFEP-03: Backward Compatibility

- Sprints that never trigger TFEP behave identically to today
- The `--no-escalation` flag on `task-unified` bypasses TFEP entirely (Claude never writes `TFEP_HALT`)
- New CLI flags (`--tfep-model`, `--tfep-agents`, `--tfep-budget-multiplier`) are all optional with sensible defaults

---

## 5. Files Requiring Changes

### New Files

| File | Purpose |
|------|---------|
| `src/superclaude/cli/sprint/tfep.py` | TFEP orchestration: parallel subprocess spawning, adversarial judge dispatch, rollback, remediation task injection, incident report generation |

### Modified Files

| File | Change |
|------|--------|
| `src/superclaude/cli/sprint/models.py` | Add `TFEP_HALT`, `TFEP_RESOLVED` to `PhaseStatus`. Add TFEP fields to `MonitorState`. Add `tfep_model`, `tfep_agents`, `tfep_budget_multiplier` to `SprintConfig`. |
| `src/superclaude/cli/sprint/executor.py` | Update `_determine_phase_status()` for `TFEP_HALT` detection. Update phase loop to call `_orchestrate_tfep()` on TFEP_HALT. Capture git baseline at phase start. Handle re-launch logic. |
| `src/superclaude/cli/sprint/process.py` | Add `build_tfep_resume_prompt()`. Add forensic agent prompt builders (RCA, solution, judge). |
| `src/superclaude/cli/sprint/monitor.py` | Add TFEP marker patterns. Update `_extract_signals_from_text()`. |
| `src/superclaude/cli/sprint/commands.py` | Add `--tfep-model`, `--tfep-agents`, `--tfep-budget-multiplier` Click options. |
| `src/superclaude/cli/sprint/diagnostics.py` | Add `FailureCategory.TFEP` for TFEP-specific diagnostic classification. |
| `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | Add TFEP output marker requirements (`TFEP_TRIGGERED`, `TFEP_HALT` in result file). |

---

## 6. Existing Code to Leverage

| Component | Location | Reuse |
|-----------|----------|-------|
| `ClaudeProcess` | `sprint/process.py` | Base class for forensic subprocesses. Reuse `start()`, `wait()`, `terminate()`. |
| `build_task_context()` | `sprint/process.py:245` | Inject prior-work context into resume prompt. Already handles git diff and task summaries. |
| `OutputMonitor` | `sprint/monitor.py` | Monitor forensic subprocesses for liveness. Reuse NDJSON parsing. |
| `AggregatedPhaseReport` | `sprint/executor.py` | Report template for TFEP incident reports. |
| `_write_executor_result_file()` | `sprint/executor.py` | Write authoritative result file after TFEP re-launch. |
| `DiagnosticCollector` | `sprint/diagnostics.py` | Collect diagnostics for TFEP failures. |
| `IsolationLayers` | `sprint/executor.py` | Per-subprocess isolation for forensic agents. |
| Task parser (`parse_tasklist()`) | `sprint/config.py` | Parse remediation tasks after injection into phase file. |

---

## 7. Design Decisions (Resolved)

| Question | Decision | Rationale |
|----------|----------|-----------|
| Forensic model | Sonnet (default), overridable via `--tfep-model` | Sonnet balances cost/capability for investigation; user may need Opus for complex codebases |
| Adversarial judge depth | Always `--depth quick` | Quick depth is sufficient for 2-variant comparison; saves tokens for the main work |
| Prior work deemed wrong | Save patch + clean revert + re-implement from remediation plan | Patch provides audit trail; clean revert prevents partial-fix interactions; re-implementation uses adjudicated plan |
| Forensic execution model | Runner-orchestrated parallel subprocesses (not in-session skill) | Independent context budgets; no IPC needed; runner already has subprocess infrastructure |
| Phase re-launch approach | Modify tasklist file in isolation dir + resume-aware prompt | Avoids re-executing completed tasks; uses existing `build_task_context()` for context; isolation dir protects original file |
| Agent shape by tier | Light = 4-step pipeline (RCA×2 → judge → Sol×2 → judge), Standard = 2-step (Full×2 → judge) | Light is fast and focused; standard allows agents to develop coherent end-to-end analysis |
| TFEP_HALT vs generic HALT | Distinct PhaseStatus value with distinct result file marker | Enables runner to distinguish "TFEP needs forensic" from "phase genuinely failed" |
| Re-launch on TFEP_HALT | 1 attempt (B behavior), then true HALT (C behavior) | Balances automation with human oversight; 3rd trigger always stops |

---

## 8. Implementation Phasing (Suggested)

### Phase A: Minimal Detection (Low risk, immediate value)
- Add `TFEP_HALT` / `TFEP_RESOLVED` to `PhaseStatus`
- Update `_determine_phase_status()` to detect `EXIT_RECOMMENDATION: TFEP_HALT`
- Add TFEP marker patterns to monitor
- On `TFEP_HALT`: classify as failure with TFEP-specific diagnostic, halt sprint (same as today but with better diagnostics)
- **Value**: Operators see "TFEP triggered" instead of opaque "phase halted"

### Phase B: Parallel Forensic Orchestration
- Create `tfep.py` with parallel subprocess spawning
- Build forensic agent prompts (RCA with `/sc:troubleshoot`, solution with `/sc:brainstorm`)
- Build adversarial judge prompt
- Implement 4-step (light) and 2-step (standard) pipelines
- Implement incident report generation
- **Value**: Automated root-cause analysis and solution proposal on test failure

### Phase C: Re-launch with Rollback
- Implement `perform_rollback()` with patch saving
- Implement `inject_remediation_tasks()` for tasklist modification
- Implement `build_tfep_resume_prompt()` for resume-aware re-launch
- Wire escalation counter and tier progression
- Add timeout extension logic
- **Value**: Fully automated TFEP loop — detect, investigate, remediate, resume

### Phase D: CLI Flags and Polish
- Add `--tfep-model`, `--tfep-agents`, `--tfep-budget-multiplier` to Click commands
- Add `SprintConfig` fields for TFEP configuration
- Update TUI to display TFEP state
- Write tests for TFEP orchestration
- **Value**: User-configurable, production-ready

---

## 9. Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| Forensic subprocesses consume excessive tokens/time | Medium | Medium | Hard timeout per subprocess (300s), total TFEP budget cap (3 attempts max) |
| Rollback reverts correct work along with incorrect | Medium | Low | Selective rollback from RCA verdict; patch preserved for recovery |
| Re-launched phase re-executes tasks despite resume prompt | Medium | Medium | Resume prompt explicitly says "skip T01-T04"; git diff shows what's already done |
| Adversarial judge produces low-quality verdict with `--depth quick` | Low | Low | Quick depth with 2 variants is the adversarial protocol's most common config |
| Multiple TFEP cycles exhaust sprint wall-clock budget | Medium | Low | 3-attempt hard limit; escalation gradient; operator halt on 3rd trigger |
| Phase isolation dir cleanup removes forensic artifacts | Low | Medium | TFEP artifacts written to `results/phase-{N}-tfep/`, not isolation dir |

---

## 10. Cross-References

| Document | Path | Relevance |
|----------|------|-----------|
| TFEP protocol (task-unified) | `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` § 4.5 | TFEP prohibition rules, trigger detection, execution flow, markers |
| Task-unified command | `src/superclaude/commands/task-unified.md` | `--no-escalation` flag |
| Forensic spec | `.dev/releases/backlog/v5.xxforensic/forensic-spec.md` | Quick mode phases, return contract, caller context schema, escalation gradient |
| Sprint executor | `src/superclaude/cli/sprint/executor.py` | Phase loop, status classification, re-launch target |
| Sprint process | `src/superclaude/cli/sprint/process.py` | Prompt builder, subprocess lifecycle |
| Sprint monitor | `src/superclaude/cli/sprint/monitor.py` | NDJSON extraction, signal detection |
| Sprint models | `src/superclaude/cli/sprint/models.py` | PhaseStatus, MonitorState, SprintConfig |
| Sprint diagnostics | `src/superclaude/cli/sprint/diagnostics.py` | Failure classification |
| Adversarial handoff | `.dev/releases/backlog/v5.xxforensic/adversarial/merged-tasklist.md` | Source tasklist for the forensic refactor |
| Forensic refactor handoff | `.dev/releases/backlog/v5.xxforensic/forensic-refactor-handoff.md` | Architectural decisions and constraints |
| TFEP refactoring context | `.dev/releases/backlog/v5.xxforensic/tfep-refactoring-context.md` | Tactical specifications and user decisions |

---

## 11. Suggested Next Step

The next agent should produce either:
- **`/sc:design`** — Architecture document with module boundaries, data flow diagrams, and interface contracts for `tfep.py`
- **`/sc:roadmap`** — Phased implementation roadmap from this specification
- **`/sc:tasklist`** — Sprint-ready tasklist bundle for immediate implementation

The implementation phasing in Section 8 provides a natural 4-phase split. Phase A is low-risk and can ship independently.
