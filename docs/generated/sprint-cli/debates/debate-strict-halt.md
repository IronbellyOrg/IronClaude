# Adversarial Debate: Should Stop-on-STRICT-Fail Be Added to Path A Worker Prompts?

## Metadata
- Generated: 2026-04-03
- Depth: quick (1 round)
- Variants: 2 (Position FOR vs Position AGAINST)
- Mode: Inline adversarial debate (no external files)
- Topic: Whether per-task subprocess prompts (Path A) should include halt-on-STRICT-fail instructions

---

## 1. Diff Analysis

### Structural Context

The Sprint CLI has two execution paths for task phases:

| Aspect | Path A (per-task subprocess) | Path B (freeform phase) |
|--------|------------------------------|-------------------------|
| **Location** | `executor.py:1064-1068` (`_run_task_subprocess`) | `process.py:183-185` (`build_prompt`) |
| **Prompt** | 3-line minimal: task ID, phase file, description | Full `/sc:task-unified` prompt with execution rules |
| **Halt instruction** | None | "If a STRICT-tier task fails, STOP and report -- do not continue to next task" |
| **Isolation** | One subprocess per task; orchestrator loop decides continuation | Single subprocess executes all tasks; worker decides continuation |
| **Tier awareness** | `TaskEntry` has no `enforcement_tier` field | Prompt includes per-tier behavior rules (STRICT/STANDARD/LIGHT/EXEMPT) |

### Key Diff Points

| ID | Area | Description | Severity |
|----|------|-------------|----------|
| C-001 | Worker halt semantics | Path A workers have zero halt instruction; Path B workers have explicit tier-conditional halt | High |
| C-002 | Tier awareness | `TaskEntry` dataclass lacks `enforcement_tier`; tier info is not parsed or passed to Path A | High |
| C-003 | Error-handling behavior | Path A worker may attempt workarounds vs. clean exit; no instruction constrains this | Medium |
| S-001 | Orchestrator control | Path A orchestrator classifies exit codes externally (`classify_phase_status`); Path B relies on worker-written result files | Medium |
| A-001 | [SHARED-ASSUMPTION] Both paths assume that exit code 0 = success and non-zero = failure is sufficient signal | Medium |

### Contradiction

| ID | Point of Conflict | Path A Position | Path B Position | Impact |
|----|-------------------|-----------------|-----------------|--------|
| X-001 | Worker responsibility for halt decisions | Worker has no halt instruction; orchestrator handles externally | Worker is explicitly told to halt on STRICT failure | High -- inconsistent mental model across paths |

---

## 2. Adversarial Debate -- Round 1

### Advocate FOR Adding Halt Instruction to Path A

**Position Summary**: Path A workers should receive tier-aware halt instructions because the current information asymmetry produces unpredictable worker behavior on failure, and structural isolation alone is insufficient to guarantee correct error-handling semantics inside the session.

**Steelman of AGAINST position**: The AGAINST position correctly identifies that subprocess isolation is a powerful structural guarantee. When each task runs in its own process, "stopping" is inherent -- a failed process cannot start the next one. The orchestrator's exit-code-based classification (`classify_phase_status` at line 1774) is the authoritative decision point, and adding redundant halt logic to the worker prompt risks conflating responsibilities. This is a clean separation of concerns.

**Strengths claimed**:

1. **Worker behavior on failure is currently unguided (C-003)**. The Path A prompt at `executor.py:1064-1068` is:
   ```
   Execute task {task_id}: {title}
   From phase file: {phase.file}
   Description: {description}
   ```
   There is no instruction about failure severity. A worker encountering a failing test might spend 20+ turns attempting workarounds, retries, or alternative approaches before eventually exiting non-zero. With a STRICT halt instruction, the worker would know to exit immediately and cleanly, saving significant token budget.

2. **The `TaskEntry` dataclass has no tier field (`models.py:26-38`)**. Even if we wanted to add halt instructions, the infrastructure does not currently propagate tier information to Path A. This is a data model gap that should be addressed regardless of the prompt debate -- the orchestrator itself has no programmatic way to distinguish STRICT from STANDARD task failures.

3. **Budget efficiency**. The `TurnLedger` (line 960-976) pre-debits a minimum allocation per task. A worker that wastes turns on retry attempts for a STRICT task burns budget that could go to subsequent tasks. Telling the worker "this is STRICT; if you fail, exit immediately" constrains wasteful behavior.

4. **Alignment with Path B behavior**. Path B explicitly says "If a STRICT-tier task fails, STOP and report -- do not continue to next task" (line 183). Consistency across paths reduces cognitive load for maintainers and ensures predictable system behavior.

**Weaknesses identified in AGAINST**:

1. The AGAINST position assumes exit codes are a sufficient communication channel. But exit code 0 vs non-zero is a binary signal -- it carries no information about *why* the worker exited or *how much effort* it spent before exiting. A STRICT task that fails after 1 turn (clean exit) and a STRICT task that fails after 30 turns (exhausted retries) both produce exit code 1, but the latter wasted significant budget.

2. The "separation of concerns" argument is valid in principle but ignores that the worker's *internal* behavior still matters. Subprocess isolation controls what happens *between* tasks; it does not control what happens *within* a task execution.

**Concessions**: The AGAINST position is correct that adding halt semantics to per-task prompts does introduce some responsibility overlap. The orchestrator remains the authoritative decision-maker. The instruction to the worker is advisory/behavioral, not a control-flow mechanism.

---

### Advocate AGAINST Adding Halt Instruction to Path A

**Position Summary**: Path A's structural isolation already provides the correct halt behavior. Adding prompt-level halt instructions conflates worker and orchestrator responsibilities, introduces a redundant control channel, and solves a problem that does not exist in the current architecture.

**Steelman of FOR position**: The FOR position correctly identifies that Path A workers currently operate without tier awareness. A worker that does not know a task is STRICT may indeed spend more turns attempting workarounds before failing. The budget efficiency argument has merit -- if we could reduce wasted turns on doomed STRICT tasks, that would be valuable. The data model gap (no `enforcement_tier` on `TaskEntry`) is a legitimate observation.

**Strengths claimed**:

1. **Subprocess isolation is the halt mechanism (S-001)**. In Path A, each task runs in its own `ClaudeProcess` (`_run_task_subprocess`, line 1053). When the process exits, the orchestrator loop at line 956 evaluates whether to continue. The worker literally *cannot* "continue to the next task" -- it has no access to the next task. This is a stronger guarantee than a prompt instruction, which relies on the LLM following the instruction correctly.

2. **The orchestrator is the authoritative decision-maker**. `classify_phase_status` (line 1774) and the main loop at line 1456 (`if status.is_failure: break`) make the halt decision. Adding a redundant halt instruction to the worker prompt creates two sources of truth for the same decision. When there are two sources of truth, they will eventually disagree.

3. **Path B needs halt instructions because Path B is structurally different**. In Path B (`build_prompt`, line 169-204), a *single* subprocess executes *all* tasks in a phase. The worker must be told when to stop because it is the only entity that can stop mid-execution. Path A does not have this problem because the worker only sees one task. The halt instruction in Path B is not a design pattern to replicate -- it is a necessity specific to Path B's architecture.

4. **Adding tier awareness to the prompt adds complexity without clear benefit to the orchestrator**. The orchestrator classifies task outcomes via exit codes and result files. If we add tier awareness to the worker, the worker might write "EXIT_RECOMMENDATION: HALT" in its output, but the orchestrator already decides this based on exit code. The worker's halt recommendation would be redundant at best and contradictory at worst.

5. **The "wasted turns" concern is better addressed by turn limits**. If the concern is that workers spend too many turns on doomed tasks, the correct solution is per-task `max_turns` or a tighter `minimum_allocation` in the `TurnLedger` -- not a prompt-level instruction that the LLM may or may not follow reliably.

**Weaknesses identified in FOR**:

1. The FOR position conflates "the worker should know about severity" with "the worker should make halt decisions." These are different things. Even if we wanted the worker to behave differently for STRICT tasks (e.g., skip retry attempts), that is a turn-budget concern, not a halt-semantics concern.

2. The budget efficiency argument is real but overstated. A worker that encounters a genuine failure (test fails, build breaks) will typically exit within a few turns regardless of prompt instructions. The scenario of "30 turns of retry attempts" requires the worker to repeatedly try and fail -- which is itself a signal that `max_turns` should be lower, not that the prompt needs halt instructions.

**Concessions**: The FOR position is correct that `TaskEntry` lacks `enforcement_tier`, and this is a genuine data model gap. Having tier information available to the orchestrator (not the worker) would improve classification decisions. The budget concern is valid in principle, even if the solution should be structural (turn limits) rather than prompt-based.

---

## 3. Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| C-001 | AGAINST | 72% | Halt semantics are structurally unnecessary in Path A due to subprocess isolation; Path B's instruction exists because its architecture requires it |
| C-002 | FOR | 80% | `TaskEntry` genuinely lacks tier info; this is a data model gap regardless of prompt debate |
| C-003 | SPLIT | 55% | Worker retry behavior is a real concern but better addressed by turn limits than prompt instructions |
| S-001 | AGAINST | 78% | Orchestrator-based control is the architecturally correct decision point for Path A |
| A-001 | ADDRESSED | 65% | Exit code as signal is sufficient for orchestrator decisions; richer signals add complexity without proportional benefit |
| X-001 | AGAINST | 68% | The inconsistency between paths is *justified* by their different architectures, not a bug to fix |

**Convergence**: 4/6 points resolved (67%). Below 80% threshold but acceptable for quick depth.

---

## 4. Base Selection

### Quantitative Assessment

| Metric | FOR | AGAINST |
|--------|-----|---------|
| Architectural alignment | 0.60 | 0.85 |
| Evidence specificity | 0.80 | 0.75 |
| Addresses root cause | 0.55 | 0.80 |
| Internal consistency | 0.70 | 0.85 |
| Risk awareness | 0.75 | 0.70 |

### Qualitative Assessment

**FOR** makes a compelling budget-efficiency argument and correctly identifies the `TaskEntry` data model gap. However, it proposes solving an architectural concern (budget waste) with a prompt-level intervention (halt instruction), which is a category mismatch.

**AGAINST** correctly identifies that Path A's subprocess isolation *is* the halt mechanism, and that Path B's instructions exist because of Path B's fundamentally different architecture (single subprocess, multiple tasks). The separation-of-concerns argument is architecturally sound.

### Combined Score

| Variant | Quant (50%) | Qual (50%) | Combined |
|---------|-------------|------------|----------|
| FOR | 0.68 | 0.60 | 0.64 |
| AGAINST | 0.79 | 0.80 | 0.795 |

**Selected Base: AGAINST** (margin: 15.5%)

---

## 5. Ruling

### Decision: DO NOT add stop-on-STRICT-fail instructions to Path A worker prompts.

### Rationale

Path A's per-task subprocess architecture already provides structural halt guarantees that are *stronger* than prompt instructions. Each worker sees exactly one task and cannot proceed to the next -- the orchestrator loop (`executor.py:956`, `executor.py:1456`) is the decision-maker. Adding halt instructions would create a redundant control channel that conflates worker and orchestrator responsibilities.

The inconsistency between Path A and Path B is **justified by their different architectures**, not a defect:
- **Path B** (single subprocess, all tasks): Worker *must* know about tier severity because it is the only entity that can halt mid-execution
- **Path A** (one subprocess per task): Worker *cannot* proceed to the next task; the orchestrator decides continuation

### Recommendations (non-prompt changes)

The debate surfaced two legitimate concerns that should be addressed through structural means:

1. **Add `enforcement_tier` to `TaskEntry`** (`sprint/models.py:26`). The orchestrator currently has no programmatic tier awareness for per-task classification. Adding this field enables the orchestrator to make tier-informed halt decisions (e.g., treat STRICT failures as PhaseStatus.HALT vs STANDARD failures as PhaseStatus.ERROR with potential recovery).

2. **Consider per-task `max_turns` scaling by tier**. If STRICT tasks should fail fast, enforce this via turn budget constraints in `TurnLedger`, not prompt instructions. STRICT tasks could receive a lower `max_turns` multiplier, ensuring workers exit quickly on failure without requiring prompt-level awareness.

3. **Leave Path B's halt instruction unchanged**. It is architecturally necessary for the freeform-phase execution model and correctly placed.

### Unresolved Items

| ID | Description | Severity |
|----|-------------|----------|
| C-003 | Worker retry behavior on failure (turns wasted before exit) | Medium -- addressable via turn limits |
| C-002 | `TaskEntry` lacks `enforcement_tier` field | Medium -- data model gap for orchestrator-level decisions |

---

## Return Contract

```yaml
return_contract:
  merged_output_path: "docs/generated/sprint-cli/debates/debate-strict-halt.md"
  convergence_score: 0.67
  artifacts_dir: "docs/generated/sprint-cli/debates/"
  status: "success"
  base_variant: "AGAINST"
  unresolved_conflicts: 2
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```
