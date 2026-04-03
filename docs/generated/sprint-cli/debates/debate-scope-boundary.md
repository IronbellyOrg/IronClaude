# Adversarial Debate: Scope Boundary Instructions in Path A Per-Task Prompt

---
generated: 2026-04-03T00:00:00Z
depth: quick
variants: 2
convergence_threshold: 0.80
status: success
---

## Metadata

- **Debate topic**: Should explicit scope boundary instructions be added to Path A's per-task subprocess prompt?
- **Depth**: quick (1 round, no rebuttals)
- **Variants**: 2 (Position FOR vs. Position AGAINST)
- **Total diff points**: 6
- **Convergence**: 83% (5 of 6 points resolved)

## Variant Definitions

### Variant A: Add Scope Boundaries (Position FOR)

Add explicit scope boundary language to the per-task prompt at `executor.py:1064-1068`, modeled on the existing language in `process.py:187-195`.

### Variant B: Keep Implicit Scoping (Position AGAINST)

Retain the current minimal 3-line prompt. The single-task naming and subprocess isolation provide sufficient scoping.

---

## Step 1: Diff Analysis

### Code Evidence

**Path A** (`src/superclaude/cli/sprint/executor.py:1064-1068`):
```python
prompt = (
    f"Execute task {task.task_id}: {task.title}\n"
    f"From phase file: {phase.file}\n"
    f"Description: {task.description}\n"
)
```

**Path B** (`src/superclaude/cli/sprint/process.py:187-195`):
```python
f"## Scope Boundary\n"
f"- After completing all tasks, STOP immediately.\n"
f"- Do not read, open, or act on any subsequent phase file.\n"
...
f"- Do not re-execute work from prior phases\n"
f"- Focus only on the tasks defined in the phase file\n"
```

### Content Differences

| # | Topic | Variant A (Add Boundaries) | Variant B (Keep Implicit) | Severity |
|---|-------|---------------------------|--------------------------|----------|
| C-001 | Worker drift risk | Workers can read phase file, see 10 tasks, do all of them | Workers only see one task ID; low drift probability | High |
| C-002 | Prompt cost | Extra ~50 tokens per subprocess; negligible | Zero added cost | Low |
| C-003 | Defensive consistency | Both paths use same discipline; easier to audit | Two different prompt philosophies require separate reasoning | Medium |
| C-004 | Paradoxical attention | N/A (dismisses this concern) | "Don't do X" may teach the model X exists | Medium |
| C-005 | Subprocess lifecycle | Excess work is wasted tokens and wall-clock time even if not destructive | Subprocess is killed after task; excess work is discarded | Medium |
| C-006 | Phase file visibility | Worker has `--dangerously-skip-permissions` and the phase file path in the prompt | Phase file path is already in the prompt; model can already read it | High |

### Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Does naming one task ID reliably prevent multi-task execution? | No -- the model receives the phase file path and has full filesystem access | Yes -- LLMs follow the instruction given; naming one task is sufficient direction | High |

### Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|----------------|------------|---------------|----------|
| A-001 | Both variants | The subprocess has `--dangerously-skip-permissions` and can read any file | STATED | No |
| A-002 | Both variants | The phase file path is included in both prompts (Path A line 1066, Path B line 170) | STATED | No |
| A-003 | Both variants | The orchestrator will eventually kill/replace the subprocess regardless of what it does | STATED | No |
| A-004 | Both variants | Claude models generally follow single-task instructions without needing negative constraints | UNSTATED | Yes |

**Promoted Shared Assumption (A-004)**: Neither side presented evidence for how reliably Claude models restrict themselves to a single named task when they have filesystem access to a file listing additional tasks. This assumption underpins Variant B's entire position but is never explicitly validated.

---

## Step 2: Adversarial Debate (Round 1)

### Advocate for Variant A (Add Scope Boundaries)

**Position summary**: The 3-line prompt hands the worker a loaded gun (phase file path + skip-permissions) with no safety. Adding scope boundaries is cheap insurance.

**Steelman of Variant B**: Variant B correctly identifies that (a) the prompt names only one task, which is strong implicit direction, (b) adding "don't do X" instructions can paradoxically surface the idea of doing X, and (c) the subprocess is ephemeral -- any excess work is wasted rather than destructive. These are genuine considerations.

**Strengths claimed**:
1. **C-006 is the critical point**: Line 1066 says `f"From phase file: {phase.file}"`. The worker literally receives the path to a file containing 10 tasks. With `--dangerously-skip-permissions`, it can read that file. Nothing in the prompt says "only do YOUR task." The model must infer single-task scope from the absence of instruction, which is fragile.
2. **C-003 (consistency)**: Path B already has scope boundaries (process.py:187-195). Having two prompt strategies in the same codebase -- one defensive, one not -- is a maintenance hazard. Anyone reading Path A will assume it was deliberate, not an oversight.
3. **C-001 (drift risk)**: If a worker does drift, the consequences are not just "wasted tokens." The orchestrator tracks per-task results and gate outcomes. A worker that completes tasks 2-5 creates file artifacts that may collide with later subprocesses spawned for those same tasks.
4. **A-004 (unstated assumption)**: The claim that "the model understands single-task focus" is an empirical claim with no evidence presented. Frontier models are instruction-following but also context-hungry; receiving a phase file path is an implicit instruction to read it.

**Concessions**: The paradoxical attention argument (C-004) has some merit. A well-scoped positive instruction ("Execute ONLY task {task_id}. Do not execute any other tasks.") avoids the "don't think of an elephant" framing while achieving the same goal.

### Advocate for Variant B (Keep Implicit Scoping)

**Position summary**: The current design is intentionally minimal. Adding scope boundaries is unnecessary complexity that solves a theoretical problem with no observed evidence.

**Steelman of Variant A**: Variant A correctly identifies that (a) the phase file path is in the prompt and the worker can read it, (b) consistency across both paths is a legitimate maintenance value, and (c) the cost of adding boundaries is genuinely low. These points have real weight.

**Strengths claimed**:
1. **C-004 (paradoxical attention)**: This is well-documented in prompt engineering. Telling a model "do NOT execute tasks T02.02, T02.03, T02.04..." explicitly enumerates the tasks it should avoid, which can increase the probability of it attending to them. The current prompt avoids this entirely by never mentioning other tasks.
2. **C-005 (subprocess lifecycle)**: Even in the worst case where a worker reads the phase file and attempts multiple tasks, the orchestrator controls the lifecycle. The worker writes to a single output file. Subsequent workers for other tasks will overwrite or write to their own output paths. The damage model is "wasted tokens," not "corrupted state."
3. **The prompt is positively scoped**: "Execute task T02.01: [title]" is already a clear, positive instruction. Adding negative constraints ("don't do X") is the weaker form of prompting compared to the positive form ("do exactly this") that already exists.
4. **YAGNI**: There is no reported incident of a Path A worker executing multiple tasks. Adding defensive instructions to prevent an unobserved problem violates scope discipline.

**Concessions**: The consistency argument (C-003) is legitimate. Having two prompt strategies is a code smell. However, the two paths serve different purposes -- Path B handles freeform phases with many tasks in a single process, where scope boundaries are essential. Path A handles one task per process, where the architecture itself provides scoping.

---

## Step 3: Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| C-001 (drift risk) | Variant A | 75% | Phase file path is in the prompt; worker CAN read it and see other tasks. Drift risk is nonzero. |
| C-002 (prompt cost) | Variant A | 90% | Both sides agree cost is negligible. Not a differentiator. |
| C-003 (consistency) | Variant A | 80% | Variant B conceded this is a "code smell." Maintaining two prompt philosophies adds cognitive overhead. |
| C-004 (paradoxical attention) | Variant B | 70% | Variant A conceded this has merit but proposed mitigation (positive framing). Point goes to B for identifying the risk. |
| C-005 (subprocess lifecycle) | Split | 55% | Both sides have valid points. Wasted tokens are not nothing; but not catastrophic either. |
| C-006 (phase file visibility) | Variant A | 85% | The phase file path is literally in the prompt. This is not a theoretical risk; the model is being handed the information needed to drift. |

**Convergence**: 5/6 points resolved (83%), exceeds 80% threshold.

---

## Step 4: Base Selection

### Combined Assessment

| Criterion | Variant A (Add) | Variant B (Keep) |
|-----------|-----------------|-----------------|
| Diff points won | 4 | 1 |
| Key concession received | Variant B conceded C-003 (consistency) | Variant A conceded C-004 (paradoxical attention) |
| Risk profile | Low (adding ~2 lines to a prompt) | Low (no change), but accepts residual drift risk |
| Evidence quality | Grounded in specific code references | Relies on unstated assumption A-004 |

**Selected base**: Variant A (Add Scope Boundaries)

**Rationale**: Variant A wins on 4 of 6 diff points with the decisive factor being C-006: the phase file path is already in the prompt, giving the worker everything it needs to drift. The unstated assumption (A-004) that models reliably self-scope to a single task when given access to a multi-task file is unvalidated. Variant B's strongest point (C-004, paradoxical attention) is mitigated by Variant A's concession to use positive framing.

---

## Step 5: Ruling

### RULING: Add scope boundary instructions to Path A, using positive framing

**What to add** to `executor.py:1064-1068`:

```python
prompt = (
    f"Execute task {task.task_id}: {task.title}\n"
    f"From phase file: {phase.file}\n"
    f"Description: {task.description}\n"
    f"\n"
    f"## Scope\n"
    f"- Execute ONLY task {task.task_id}. No other tasks.\n"
    f"- Do not execute, plan, or prepare any other task from the phase file.\n"
    f"- STOP when {task.task_id} is complete.\n"
)
```

**Design decisions in the ruling**:

1. **Positive framing first** ("Execute ONLY task X") addresses Variant B's C-004 concern. The instruction leads with what TO do, not what to avoid.
2. **Explicit stop** ("STOP when X is complete") mirrors Path B's existing pattern at process.py:188.
3. **No enumeration of other tasks** -- avoids paradoxical attention entirely. The worker is told its scope without being told what exists outside its scope.
4. **Phase file path retained** -- the worker needs it to find its own task definition. Removing it would break functionality.

**Accepted risk**: There remains a small probability that the worker reads the phase file and does extra work despite the boundary instruction. This is mitigated by:
- The subprocess lifecycle (orchestrator kills it after task completion)
- Per-task output isolation (each task writes to tracked paths)
- The boundary instruction itself (reduces probability)

### Unresolved Points

| Point | Status | Resolution |
|-------|--------|------------|
| C-005 (subprocess lifecycle) | Unresolved | Both positions valid; not material to ruling. The boundary instruction reduces wasted work regardless. |

---

## Return Contract

```yaml
return_contract:
  merged_output_path: "docs/generated/sprint-cli/debates/debate-scope-boundary.md"
  convergence_score: 0.83
  artifacts_dir: "docs/generated/sprint-cli/debates/"
  status: "success"
  base_variant: "Variant A (Add Scope Boundaries)"
  unresolved_conflicts: 1
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```
