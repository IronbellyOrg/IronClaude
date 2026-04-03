# BUILD REQUEST: Deep Investigation of Sprint Task Execution Flow

## Goal

Comprehensive technical investigation of the IronClaude sprint task execution pipeline — specifically how individual tasks within a tasklist phase are fed to worker agents, executed, verified, and tracked. We need to determine whether there are verification, QA, or behavioral governance layers that were missed in preliminary analysis, or whether the gaps identified are real.

## Context

IronClaude has a sprint execution system (`superclaude sprint run`) that processes tasklist phase files containing structured task items (`### T<PP>.<TT> -- Title`). Each task item contains extensive metadata: acceptance criteria, verification steps, deliverables, tier classification, dependencies, and artifact paths.

There are two code paths in the sprint executor:
- **Path A** (per-task): `_run_task_subprocess()` in `src/superclaude/cli/sprint/executor.py:1053` — runs when the phase file has properly formatted `### T<PP>.<TT>` headings
- **Path B** (whole-phase fallback): `ClaudeProcess.build_prompt()` in `src/superclaude/cli/sprint/process.py:123` — runs when the phase file has NO task headings

Path B invokes `/sc:task-unified` which triggers the full `sc-task-unified-protocol` skill with tier-based verification, TFEP, forensic escalation, and adversarial review. Path A sends a 3-line prompt and bypasses all of that.

The system's architect (Ryan) states there is "a very extensive system in place" for task verification. We need to find it — whether it's wired into the execution path, exists but is disconnected, or lives in a layer we haven't examined.

## Preliminary Findings (Verify or Correct These)

### Finding 1: Worker prompt is minimal (Path A)
**File**: `src/superclaude/cli/sprint/executor.py:1064-1068`
**Claim**: The per-task worker gets only:
```
Execute task {task_id}: {title}
From phase file: {phase.file}
Description: {deliverables_text}
```
No behavioral instructions, no `/sc:task-unified`, no scope constraints, no instruction to read the phase file.
**Status**: Verified against code. Need to determine if there's another layer (CLAUDE.md, skills auto-loading, etc.) that adds governance to the worker session.

### Finding 2: Description is only Deliverables text
**File**: `src/superclaude/cli/sprint/config.py:362-380`
**Claim**: The `description` field in `TaskEntry` is extracted only from the `**Deliverables:**` section. Acceptance criteria, steps, tier, verification method, artifacts, dependencies are NOT included.
**Status**: Verified against code.

### Finding 3: Task completion judged by CLI exit code only
**File**: `src/superclaude/cli/sprint/executor.py:999-1005`
**Claim**: `exit_code == 0` → PASS, `124` → INCOMPLETE, else → FAIL. No output parsing, no result file reading, no deliverable checking in the per-task path.
**Status**: Verified against code. Need to check if there's a downstream consumer that checks deliverables.

### Finding 4: Post-task gates are structural, not semantic
**File**: `src/superclaude/cli/sprint/executor.py:1027-1038`
**Claim**: Two hooks run after each task — wiring analysis (unwired callables, orphan modules) and anti-instinct gate (file exists, frontmatter fields, line count). Neither checks acceptance criteria or task-specific deliverables.
**Status**: Verified against code. Need to check if there are additional gates that could be registered or if the gate criteria could include task-specific checks.

### Finding 5: No post-phase QA
**File**: `src/superclaude/cli/sprint/executor.py:1214-1233`
**Claim**: After all tasks in a phase complete, the code tallies pass/fail, runs post-phase wiring hook, logs, and continues. No QA subprocess, no acceptance criteria verification.
**Status**: Verified against code.

### Finding 6: No post-sprint QA
**File**: `src/superclaude/cli/sprint/executor.py:1501-1521`
**Claim**: After all phases complete: KPI report (metrics), log summary, desktop notification. No QA process.
**Status**: Verified against code.

### Finding 7: `build_task_context()` is dead code
**File**: `src/superclaude/cli/sprint/process.py:245`
**Claim**: Function exists to inject prior task results into subsequent prompts. Grep across all of `src/superclaude/` shows zero callers.
**Status**: Verified. Need to check if it was recently disconnected or never connected.

### Finding 8: Per-task progress is memory-only
**File**: `src/superclaude/cli/sprint/executor.py:949`
**Claim**: `results: list[TaskResult]` is a local variable never written to disk. If the process crashes mid-phase, there's no per-task resume. Phase-level resume exists via `--start` flag but not task-level.
**Status**: Verified against code.

### Finding 9: Path A bypasses sc:task-unified entirely
**Files**: `executor.py` (no reference to task-unified), `process.py:170` (Path B references it)
**Claim**: The full verification protocol (sc-task-unified-protocol) with tier-based execution, TFEP, forensic escalation, adversarial review is only invoked by Path B (fallback for malformed phase files). Path A (properly formatted tasklists) skips it.
**Status**: Verified via grep. This appears to be the critical gap.

### Finding 10: No scope enforcement for worker
**Claim**: Nothing prevents the worker from reading the phase file and executing multiple tasks, or doing something unrelated. The prompt doesn't say "do only this task." The orchestrator spawns subprocesses for all tasks regardless.
**Status**: Verified — no scope constraint in the prompt.

## Research Questions

### Priority 1: Is there a hidden governance layer?
- Does the worker Claude session automatically load CLAUDE.md, skills, or commands that would add behavioral governance?
- Does `--no-session-persistence` affect skill loading?
- Could the worker's CLAUDE.md instructions compensate for the bare prompt?
- Are there hooks in `.claude/settings.json` that trigger on subprocess execution?
- Does the `--tools default` flag affect what the worker can do?

### Priority 2: Which path is the designed/preferred path?
- The tasklist generation skill (`sc:tasklist-protocol`) produces phase files. Do those phase files contain `### T<PP>.<TT>` headings? If yes, they will ALWAYS hit Path A (the minimal 3-line prompt), never Path B (the rich `/sc:task-unified` prompt).
- Check `src/superclaude/skills/sc-tasklist-protocol/` — templates, rules, and emission logic — to confirm the output format includes `### T<PP>.<TT>` headings.
- Check actual generated phase files in `.dev/releases/` to confirm they match the Path A regex (`_TASK_HEADING_RE` in `config.py:281`).
- If the tasklist builder ALWAYS produces files that trigger Path A, then Path B is effectively dead code for normal operation — the rich verification protocol never fires.
- Was `_run_task_subprocess` designed to eventually call `build_prompt()` or invoke `/sc:task-unified`?
- Is there a task, issue, or TODO referencing this gap?
- Check git history of `executor.py` for the introduction of `_run_task_subprocess` — was it a WIP?
- Check the comment at line 1091: "Turn counting is wired separately in T02.06" — what is T02.06 and is this evidence of incomplete wiring?
- **Critical question**: If the tasklist builder produces `### T<PP>.<TT>` formatted files (triggering Path A), and Path A bypasses `sc:task-unified`, then the entire verification system (tier-based execution, TFEP, forensic escalation) is unreachable during normal sprint execution. Is this the case?

### Priority 3: Is there a verification system outside sprint/?
- Check `src/superclaude/cli/pipeline/` for verification systems that could apply to sprint tasks
- Check `src/superclaude/pm_agent/self_check.py` — is SelfCheckProtocol used in sprint execution?
- Check `src/superclaude/pm_agent/confidence.py` — is ConfidenceChecker used?
- Check `src/superclaude/execution/` — is there a reflection or self-correction system?
- The `pipeline/deliverables.py` has `decompose_deliverables()` with Implement/Verify pairs — is this wired into sprint?
- The `pipeline/executor.py` has a proper gate system with retry — why doesn't sprint use it?

### Priority 4: Task file structure and worker behavior
- When a worker gets the phase file path, does Claude Code's behavior predictably cause it to read the file?
- Do the task items (acceptance criteria, verification steps) function as self-verification instructions IF the worker reads them?
- Is the design intent that verification is embedded in the task definition rather than enforced by the orchestrator?
- If so, is there evidence this works reliably?

### Priority 5: What was the intended design?
- Check `PLANNING.md`, `TASK.md`, `KNOWLEDGE.md` for sprint execution design intent
- Check `.dev/` for design docs, specs, or roadmaps describing the sprint verification model
- Check `docs/` for sprint execution documentation
- Look for any spec that describes how task-level QA was supposed to work
- Search for references to "T02.06" (turn counting), "v3.1-T04" (per-task delegation comment at executor.py:1201), "v3.2-T02" (post-phase wiring hook) — these version tags suggest incremental development; what was the full plan?

### Priority 6: Resume and progress tracking
- Is there a planned or partially implemented per-task checkpoint system?
- Check if `execution-log.jsonl` records task-level events (not just phase-level)
- Is the `DeferredRemediationLog` at `remediation.json` intended to serve as progress state?
- Check `.roadmap-state.json` — does it track task-level progress?

## Key Files to Investigate

### Sprint execution core
- `src/superclaude/cli/sprint/executor.py` — orchestration loop, hooks, per-task subprocess
- `src/superclaude/cli/sprint/process.py` — prompt construction, context injection
- `src/superclaude/cli/sprint/config.py` — phase discovery, tasklist parsing
- `src/superclaude/cli/sprint/models.py` — TaskEntry, TaskResult, TurnLedger, SprintConfig
- `src/superclaude/cli/sprint/logging_.py` — what gets logged to disk
- `src/superclaude/cli/sprint/commands.py` — CLI flags, resume capability

### Verification/QA systems
- `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` — the verification protocol Path B uses
- `src/superclaude/cli/pipeline/executor.py` — generic pipeline with gate system
- `src/superclaude/cli/pipeline/gates.py` — gate_passed() implementation
- `src/superclaude/cli/pipeline/deliverables.py` — deliverable decomposition
- `src/superclaude/cli/pipeline/trailing_gate.py` — trailing gate runner
- `src/superclaude/cli/audit/wiring_gate.py` — wiring analysis
- `src/superclaude/pm_agent/self_check.py` — SelfCheckProtocol
- `src/superclaude/pm_agent/confidence.py` — ConfidenceChecker
- `src/superclaude/cli/roadmap/gates.py` — ANTI_INSTINCT_GATE definition

### Tasklist generation (what produces the phase files)
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — the generation algorithm
- `src/superclaude/skills/sc-tasklist-protocol/templates/` — phase file templates
- `src/superclaude/skills/sc-tasklist-protocol/rules/` — emission rules, tier classification
- `src/superclaude/cli/tasklist/` — CLI tasklist commands and executor
- `.dev/releases/complete/` and `.dev/releases/archive/` — actual generated phase files to confirm format

### Design docs and specs
- `PLANNING.md`
- `TASK.md`
- `KNOWLEDGE.md`
- `docs/` — any sprint execution documentation
- `.dev/releases/` — roadmap/tasklist specs that describe sprint verification

### Task file examples (to understand the full structure)
- `.dev/releases/complete/v2.24.5-SpecFidelity/phase-1-tasklist.md`
- Any recent phase files with STRICT tier tasks

## What We Need From This Research

1. **Definitive answer**: Is the per-task execution path (Path A) missing its verification layer, or is verification handled somewhere we haven't found?
2. **If missing**: What was the intended design? Is this a known gap or an accidental omission?
3. **If present**: Where is it? How is it wired? Show the code path.
4. **Path routing**: Does the tasklist builder (`sc:tasklist-protocol`) produce files that trigger Path A or Path B? If Path A, then the `sc:task-unified` verification protocol is unreachable during normal sprint execution — confirm or deny this.
5. **End-to-end format trace**: Trace the format from tasklist generation → phase file on disk → `_TASK_HEADING_RE` regex match → path selection. Show whether the standard pipeline always routes to Path A.
6. **Regardless**: Document the complete task execution flow from tasklist parsing to completion, identifying every programmatic vs inference boundary, every verification checkpoint, and every gap.
