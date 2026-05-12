# Adversarial Debate: `@{phase_file}` Preloading in Path A Per-Task Subprocess

## Metadata

- **Generated**: 2026-04-03
- **Depth**: quick (1 round, no rebuttals)
- **Debate topic**: Should `@{phase_file}` preloading be integrated into Path A's per-task prompt (programmatic layer) rather than relying on inference to read the file?
- **Variants compared**: 2
- **Source evidence**: `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/process.py`

---

## 1. Diff Analysis

### 1.1 Current System — Two Execution Paths

**Path A** (`_run_task_subprocess`, line 1053-1092 of `executor.py`):
Per-task subprocess. Sends a minimal 3-line prompt:

```python
prompt = (
    f"Execute task {task.task_id}: {task.title}\n"
    f"From phase file: {phase.file}\n"
    f"Description: {task.description}\n"
)
```

The worker receives the file path as a plain-text string (`phase.file`). There is no `@` prefix, no force-loading. The model must infer it should read the file to get acceptance criteria, validation commands, deliverables, dependencies, rollback instructions, and tier classification.

**Path B** (`ClaudeProcess.build_prompt`, line 123-204 of `process.py`):
Freeform phase subprocess. Uses `@{phase_file}` syntax:

```python
f"/sc:task-unified Execute all tasks in @{phase_file} "
```

This force-loads the entire phase file into the Claude context window before execution begins. The worker starts with full visibility into every task.

### Structural Differences

| # | Area | Path A (per-task) | Path B (freeform) | Severity |
|---|------|-------------------|-------------------|----------|
| S-001 | Context injection mechanism | Plain-text path reference | `@{file}` force-load | **High** |
| S-002 | Prompt size | ~3 lines (task_id, title, description) | Full phase file + sprint context + execution rules + scope boundary | **High** |
| S-003 | Task scoping | Implicit (only one task_id mentioned) | Explicit (`Execute tasks in order T01.01, T01.02...`) | **Medium** |

### Content Differences

| # | Topic | Path A | Path B | Severity |
|---|-------|--------|--------|----------|
| C-001 | Acceptance criteria visibility | Worker must read file to see AC | AC force-loaded | **High** |
| C-002 | Tier classification visibility | Worker must read file to see tier | Tier visible in loaded content | **Medium** |
| C-003 | Dependency chain visibility | Worker must read file to see deps | All deps visible in loaded content | **Medium** |
| C-004 | Sprint context | Not injected | Full sprint context header injected | **Medium** |
| C-005 | Scope boundary enforcement | None (no scope rules) | Explicit scope boundary section | **Low** |

### Contradictions

| # | Point of Conflict | Path A Position | Path B Position | Impact |
|---|-------------------|-----------------|-----------------|--------|
| X-001 | Whether the worker needs full file context | Assumes task_id + title + description is sufficient; worker infers to read more | Assumes full file is mandatory; loads it deterministically | **High** |
| X-002 | Context window budget strategy | Minimal prompt = maximum budget for tool use and reasoning | Front-loads context = less budget for tool use and reasoning | **Medium** |

### Shared Assumptions

| # | Assumption | Classification | Impact |
|---|-----------|---------------|--------|
| A-001 | The `description` field in `TaskEntry` contains enough information for the worker to begin execution | **UNSTATED** | High — if `description` is sparse (e.g., just a title restatement), the 3-line prompt gives the worker almost nothing actionable |
| A-002 | Claude reliably reads files referenced by plain-text paths in prompts | **UNSTATED** | High — this is the crux of the inference-dependency argument |
| A-003 | Phase files are small enough that loading them does not cause `prompt-too-long` errors | **UNSTATED** | Medium — the monitor already has `detect_prompt_too_long()` (line 69, monitor.py), which suggests this failure mode is known |

---

## 2. Adversarial Debate — Round 1

### Advocate FOR Programmatic Integration (Position: Add `@{phase_file}` to Path A)

**Position Summary**: The current 3-line prompt in Path A is an unforced error that trades determinism for a marginal context-window savings, creating an asymmetry with Path B that has no engineering justification.

**Steelman of Opposing Position**: The opposition correctly identifies that (a) preloading the full phase file wastes context on sibling tasks, and (b) Claude almost always reads referenced files when prompted. These are real costs. A 10-task phase file loaded 10 times across 10 subprocesses is genuinely wasteful if each subprocess only needs its own task block.

**Strengths of programmatic integration**:

1. **Eliminates inference dependency (A-002)**: The current system works because Claude *usually* reads files mentioned in prompts. But "usually" is not "always." A single failure to read the file means the worker executes blind — no acceptance criteria, no validation commands, no tier classification. The cost of this failure is an entire subprocess budget wasted on incorrect work. Programmatic loading makes the pipeline deterministic: context is *always* present.

2. **Addresses the description sparsity risk (A-001)**: `TaskEntry.description` is a parsed markdown field. Inspecting the model (`models.py` line 26-37), it defaults to empty string. The 3-line prompt degrades to `task_id + title + ""` when description is empty. This is not a theoretical risk — it is the default state.

3. **Path symmetry**: Path B already uses `@{phase_file}` because the system's designers recognized that full context is necessary for correct execution. Path A diverged from this design without documented rationale. The asymmetry is a maintenance hazard: developers modifying the prompt format must remember two different injection strategies.

4. **Failed execution has no retry budget**: Once a subprocess fails because it lacked context, the `TurnLedger` has already debited the allocation (executor.py line 974-976). There is no automatic re-run mechanism. The task is marked FAIL and the sprint continues or halts depending on tier. Prevention is strictly cheaper than recovery.

**Weaknesses acknowledged**:

- Full file preload does waste context on sibling tasks.
- For large phase files, the context window cost is real and non-trivial.

**Proposed mitigation**: Instead of loading the *entire* phase file, extract the specific task block (the `### T<PP>.<TT>` section including all sub-content until the next `###` heading) and inject *only that block* via inline content in the prompt. This gives the worker its full task specification without sibling noise. The `parse_tasklist` function in `config.py` already parses individual task blocks — the extraction infrastructure exists.

---

### Advocate AGAINST Programmatic Integration (Position: Keep inference-dependent)

**Position Summary**: The current design is an intentional optimization that preserves maximum context window budget for tool use and reasoning. The inference dependency is well-tolerated in practice, and the proposed fix creates new problems worse than the one it solves.

**Steelman of Opposing Position**: The opposition correctly identifies that (a) `TaskEntry.description` can be empty, making the 3-line prompt dangerously sparse, and (b) there is no retry mechanism after a subprocess wastes budget on blind execution. These are real risks. A deterministic system is, all else equal, preferable to a probabilistic one.

**Strengths of keeping the current design**:

1. **Context window economics are severe**: Phase files in this codebase are "extremely detailed" (per the debate topic statement) — tier, steps, acceptance criteria, validation commands, deliverables, dependencies, rollback instructions per task. A 10-task phase file could easily be 5,000-15,000 tokens. Loading this 10 times across 10 subprocesses wastes 45,000-135,000 tokens of context budget on sibling tasks that the worker *should not touch*. Claude's context window is finite; every token spent on irrelevant sibling context is a token not available for tool calls, code reads, and reasoning.

2. **Claude reliably reads referenced files**: The `From phase file: {phase.file}` line in the prompt is an explicit, clear instruction. In practice, Claude reads files referenced by path at extremely high rates — well above 95%. The opposition's argument rests on the <5% failure case, which can be addressed without full preloading (e.g., by making the path reference more explicit: `Read @{phase.file} for full task details`).

3. **Scope contamination risk**: Loading the full phase file introduces sibling task content into the worker's context. This actively harms execution: the worker may attempt to execute sibling tasks, reference sibling acceptance criteria, or get confused about its scope boundary. Path B mitigates this with an explicit "## Scope Boundary" section, but that is additional complexity to solve a problem that Path A avoids entirely by not loading the file.

4. **The opposition's mitigation proves the current design is correct**: The "extract only the task block" proposal acknowledges that full-file preloading is wasteful. But per-task block extraction adds parser complexity, introduces a new failure mode (incorrect block extraction), and still loads more content than the current 3-line prompt. If the concern is empty descriptions, the correct fix is to ensure `TaskEntry.description` is never empty — a parser-level fix, not a prompt-level one.

**Weaknesses acknowledged**:

- The 3-line prompt is genuinely too sparse when `description` is empty.
- The plain-text path reference (`From phase file:`) is less reliable than `@{file}` syntax.
- There is no explicit instruction to read the file — only an implicit reference.

---

## 3. Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | FOR (integrate) | 75% | Deterministic context injection is strictly more reliable than inference-dependent |
| S-002 | AGAINST (keep) | 70% | Minimal prompt preserves context budget; valid economic argument |
| S-003 | FOR (integrate) | 65% | Explicit task scoping is better than implicit |
| C-001 | FOR (integrate) | 85% | AC visibility is critical for correct execution; inference failure is catastrophic |
| C-002 | FOR (integrate) | 70% | Tier determines gate behavior; must be visible |
| C-003 | FOR (integrate) | 65% | Dependency visibility prevents ordering errors |
| C-004 | FOR (integrate) | 60% | Sprint context provides useful orientation but is not critical |
| C-005 | AGAINST (keep) | 55% | Scope boundary is more important for multi-task phases |
| X-001 | FOR (integrate) | 80% | The worker DOES need full task context; description field can be empty |
| X-002 | AGAINST (keep) | 70% | Context budget preservation is a real engineering constraint |
| A-001 | FOR (integrate) | 90% | `description` defaults to `""` — this is verified in source (models.py line 34) |
| A-002 | AGAINST (keep) | 55% | Claude usually reads files, but "usually" vs "always" is the key disagreement |
| A-003 | AGAINST (keep) | 60% | `detect_prompt_too_long` exists, confirming large prompts are a real failure mode |

**Convergence**: 8/13 points won by FOR, 5/13 by AGAINST = 62% alignment (below 80% threshold, but depth=quick limits to 1 round)

---

## 4. Hybrid Scoring

### Quantitative Layer (50% weight)

| Metric | Weight | FOR (integrate) | AGAINST (keep) |
|--------|--------|-----------------|----------------|
| Requirement Coverage | 0.30 | 0.85 (addresses AC visibility, tier, deps) | 0.60 (addresses context budget, scope) |
| Internal Consistency | 0.25 | 0.90 (no contradictions in argument) | 0.80 (mitigation proposal weakens own position) |
| Specificity Ratio | 0.15 | 0.85 (cites line numbers, field defaults) | 0.75 (uses "extremely detailed" without measurement) |
| Dependency Completeness | 0.15 | 0.80 (references parser infrastructure) | 0.70 (assumes description fix without specifying how) |
| Section Coverage | 0.15 | 0.80 | 0.80 |

**FOR quant**: (0.85 x 0.30) + (0.90 x 0.25) + (0.85 x 0.15) + (0.80 x 0.15) + (0.80 x 0.15) = 0.255 + 0.225 + 0.1275 + 0.12 + 0.12 = **0.8475**

**AGAINST quant**: (0.60 x 0.30) + (0.80 x 0.25) + (0.75 x 0.15) + (0.70 x 0.15) + (0.80 x 0.15) = 0.18 + 0.20 + 0.1125 + 0.105 + 0.12 = **0.7175**

### Qualitative Assessment (50% weight)

- FOR demonstrates stronger evidence grounding (cites exact source lines, default values)
- AGAINST makes valid economic arguments but relies on unquantified claims ("extremely detailed")
- FOR's proposed mitigation (extract task block only) addresses AGAINST's strongest objection
- AGAINST's counter-mitigation (fix empty descriptions) is narrower in scope

**FOR qual**: 0.80 | **AGAINST qual**: 0.70

### Combined Score

**FOR**: (0.50 x 0.8475) + (0.50 x 0.80) = 0.4238 + 0.40 = **0.8238**
**AGAINST**: (0.50 x 0.7175) + (0.50 x 0.70) = 0.3588 + 0.35 = **0.7088**

**Winner**: FOR (programmatic integration), margin: 11.5%

---

## 5. Ruling

### Decision: INTEGRATE, with task-block extraction (not full-file preload)

Neither the pure FOR nor the pure AGAINST position survives scrutiny intact. The ruling synthesizes the strongest elements of both:

**What to do**:

1. **Extract the individual task block** from the phase file at prompt construction time in `_run_task_subprocess`. The `parse_tasklist` infrastructure in `config.py` already parses `### T<PP>.<TT>` blocks. Use the same parser to extract the full markdown content for the specific `task.task_id` — including acceptance criteria, validation commands, deliverables, dependencies, tier, and rollback instructions.

2. **Inject the extracted block inline** in the per-task prompt, replacing the current 3-line prompt:

   ```python
   prompt = (
       f"Execute task {task.task_id}: {task.title}\n\n"
       f"## Full Task Specification\n\n"
       f"{task_block_content}\n\n"
       f"From phase file: {phase.file}\n"
       f"Execute ONLY this task. Do not read or act on sibling tasks.\n"
   )
   ```

3. **Do NOT use `@{phase_file}`** for the full file. The AGAINST position is correct that loading sibling tasks is wasteful and creates scope contamination risk.

4. **As a secondary fix**, ensure `TaskEntry.description` is populated by the parser. If the parser produces an empty description, it should fall back to extracting the first non-heading paragraph from the task block.

### Rationale

| Factor | Weight | Ruling |
|--------|--------|--------|
| Determinism over inference | High | Task block extraction is deterministic; no inference dependency |
| Context budget preservation | High | Only the relevant task block is loaded; no sibling waste |
| Scope contamination prevention | Medium | No sibling task content enters the worker context |
| Path A/B symmetry | Low | Paths remain different (block vs file) but both are now deterministic |
| Implementation cost | Low | Parser infrastructure already exists; change is localized to `_run_task_subprocess` |

### Unresolved Items

- **A-003 (prompt-too-long)**: If individual task blocks are very large (>100K tokens), even block-level injection could trigger `prompt-too-long`. This is unlikely for single tasks but should be monitored. No action needed now.
- **Context injection from `build_task_context`**: The `build_task_context` function (process.py line 245) already builds prior-task context. The per-task prompt in `_run_task_subprocess` does not call it. This is a separate gap worth addressing but out of scope for this debate.

---

## Return Contract

```yaml
return_contract:
  merged_output_path: "docs/generated/sprint-cli/debates/debate-file-preloading.md"
  convergence_score: 0.62
  artifacts_dir: "docs/generated/sprint-cli/debates/"
  status: "success"
  base_variant: "FOR:integrate"
  unresolved_conflicts: 2
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```
