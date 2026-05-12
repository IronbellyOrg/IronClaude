# Adversarial Debate: Sprint Context Injection into Path A

---
generated: 2026-04-03
depth: quick
variants: 2
convergence: 85%
status: CONVERGED
---

## Metadata

- **Debate topic**: Should sprint context (release name, phase number, artifact paths, prior-phase directories) be injected into Path A's per-task subprocess prompt?
- **Depth**: quick (1 round)
- **Variants compared**: 2 (Position A: Inject context; Position B: Rely on filesystem discovery)
- **Total differences found**: 8
- **Categories**: structural (1), content (4), contradictions (1), unique (2), shared assumptions (2)

## Variant Definitions

### Variant 1: Programmatic Injection (PRO)

Inject sprint context (release name, phase number, artifact root, results directory, prior-phase directories) into Path A's per-task prompt at `executor.py:1064-1068`, mirroring what Path B already provides at `process.py:147-167`.

### Variant 2: Filesystem Discovery (CON)

Leave Path A's 3-line prompt unchanged. Workers can discover context from the filesystem, the phase file, and the TASKLIST_ROOT convention.

---

## Step 1: Diff Analysis

### Structural Differences

| # | Area | Variant 1 (PRO) | Variant 2 (CON) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Prompt architecture | Unified context model across Path A and Path B | Two distinct prompt shapes: minimal (Path A) vs. enriched (Path B) | Medium |

### Content Differences

| # | Topic | Variant 1 (PRO) Approach | Variant 2 (CON) Approach | Severity |
|---|-------|--------------------------|--------------------------|----------|
| C-001 | Cross-phase artifact access | Provide resolved absolute paths in prompt text | Worker uses `ls`, `glob`, or reads phase file to discover paths | High |
| C-002 | Path resolution correctness | Eliminates TASKLIST_ROOT placeholder ambiguity by supplying resolved paths | Relies on worker reading TASKLIST_ROOT from tasklist-index.md and resolving relative to cwd | Medium |
| C-003 | Token cost | Adds ~5 lines (~80 tokens) per task prompt | Zero additional prompt tokens | Low |
| C-004 | Worker coupling | Workers may hardcode injected paths instead of resolving dynamically | Workers forced to discover, producing more robust resolution logic | Medium |

### Contradictions

| # | Point of Conflict | PRO Position | CON Position | Impact |
|---|-------------------|--------------|--------------|--------|
| X-001 | Whether per-task workers need cross-phase awareness | "Workers in phase 3 need to know where phase 1-2 artifacts live" | "Per-task workers doing a single focused task rarely need cross-phase artifact awareness" | High |

### Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | PRO | Parity argument: Path B already does this, so Path A divergence is an unnecessary inconsistency | High |
| U-002 | CON | Separation of concerns: per-task workers should not be encouraged to reach outside their task scope | Medium |

### Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|-----------------|------------|----------------|----------|
| A-001 | Both assume task workers receive `phase.file` | The phase file path is sufficient to locate the correct tasklist | STATED | No |
| A-002 | Both assume workers operate in the release directory | Worker cwd is the release directory root or a known relative location | UNSTATED | Yes |

---

## Step 2: Adversarial Debate (Round 1)

### Advocate for Variant 1 (PRO: Inject Context)

**Position Summary**: The per-task prompt at `executor.py:1064-1068` creates an information asymmetry between Path A and Path B workers that is unnecessary, cheap to fix, and creates a real failure mode for cross-phase tasks.

**Steelman of Variant 2 (CON)**: The strongest argument against injection is separation of concerns. Per-task workers have a narrow scope -- execute one task from one phase file. Injecting sprint-wide context could encourage workers to wander beyond their mandate, reading artifacts from prior phases when they should focus on their single deliverable. This is a legitimate design concern; the less context a subprocess receives, the less likely it is to overreach. Furthermore, the TASKLIST_ROOT convention exists precisely to enable discovery when needed.

**Strengths Claimed**:

1. **Evidence of real asymmetry** (citing code): Path B at `process.py:147-167` builds a full `## Sprint Context` header with release name, phase number, artifact root, results directory, and prior-phase directories. Path A at `executor.py:1064-1068` sends only `task_id`, `title`, `phase.file`, and `description`. This is not a theoretical gap -- it is a measured code-level asymmetry.

2. **Prior-phase dependency is real, not hypothetical**: Tasklist phase files routinely contain tasks that reference outputs from earlier phases. A phase-3 task like "Validate the schema generated in phase 1" needs to know where phase-1 artifacts live. Without injected paths, the worker must: (a) read the phase file, (b) find TASKLIST_ROOT, (c) resolve it relative to cwd, (d) navigate to the correct phase-N directory. This is 4 steps of brittle path resolution that could fail at any point.

3. **Cost is trivially low**: The sprint context is ~5 lines of text, approximately 80 tokens. Against a per-task budget of 100+ max_turns (each turn is thousands of tokens), this is noise-level overhead -- less than 0.01% of the task's total token budget.

4. **TASKLIST_ROOT is a placeholder, not a resolved path**: The tasklist files use `TASKLIST_ROOT/phase-1-tasklist.md` as a convention. But `TASKLIST_ROOT` is never resolved to an absolute path inside the phase file. The worker must infer what it resolves to. `SprintConfig` already has `release_dir` computed; passing it costs nothing and eliminates ambiguity.

**Weaknesses Acknowledged**: Injecting paths does create a mild coupling -- if the directory structure changes, the injected paths become stale. However, the same config object that builds the prompt also computes these paths, so they are always consistent within a single run.

**Shared Assumption Response**:
- A-001: ACCEPT -- phase file path is provided by both variants.
- A-002: REJECT -- worker cwd is not guaranteed. `ClaudeProcess` spawns a subprocess; the cwd depends on how `subprocess.Popen` is invoked. This is exactly why explicit paths are safer than relative discovery.

### Advocate for Variant 2 (CON: Filesystem Discovery)

**Position Summary**: The minimal prompt is a deliberate design choice that keeps per-task workers focused on their single responsibility. Sprint context injection is a solution looking for a problem that rarely exists in practice.

**Steelman of Variant 1 (PRO)**: The strongest argument for injection is the parity argument. Path B already injects sprint context, so Path A's omission is an inconsistency that could confuse maintainers and cause subtle bugs when tasks are moved between execution paths. The cost argument is also strong -- 80 tokens is genuinely negligible. If you accept that the information is occasionally useful and the cost is near-zero, the expected-value calculation favors injection.

**Strengths Claimed**:

1. **Per-task scope is narrow by design**: The per-task subprocess exists precisely because the task is self-contained enough to run independently. `executor.py` decomposes phase files into individual `TaskEntry` objects (line 1095-1099: phases with `### T<PP>.<TT>` headings get per-task treatment; freeform phases use Path B). This decomposition is evidence that per-task workers are NOT expected to need full sprint awareness.

2. **TASKLIST_ROOT is an established convention**: The tasklist generator (sc-tasklist-protocol) emits `TASKLIST_ROOT` as a standardized placeholder in every index and phase file. Workers that need cross-phase references are expected to resolve this convention, which is documented and consistent. Injecting resolved paths creates a second resolution mechanism that must be kept in sync with the convention.

3. **Discovery promotes robustness**: Workers that discover paths via filesystem exploration (`ls`, `glob`, `Read`) build more resilient resolution logic than workers that consume injected absolute paths. If the directory structure evolves (e.g., artifact subdirectories are reorganized), discovery-based workers adapt; injection-based workers break.

4. **The cross-phase dependency claim is overstated**: Looking at real tasklist files, the majority of per-task entries are self-contained: "implement function X", "write test Y", "update config Z". Tasks that genuinely need prior-phase artifacts are rare and typically live in later phases that are more likely to be freeform (Path B) anyway.

**Weaknesses Acknowledged**: The parity argument is valid -- having two different prompt shapes for what are conceptually similar worker processes is a maintenance burden. If a future change adds context to Path B, someone must remember to update Path A as well.

**Shared Assumption Response**:
- A-001: ACCEPT.
- A-002: QUALIFY -- cwd is typically the project root, but this is a subprocess implementation detail. Workers should not depend on cwd for path resolution regardless of whether context is injected.

---

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | PRO | 70% | Unified prompt architecture is simpler to maintain; two shapes create maintenance burden |
| C-001 | PRO | 82% | Resolved absolute paths prevent a real class of path-resolution errors; CON's 4-step discovery is fragile |
| C-002 | PRO | 78% | TASKLIST_ROOT is a placeholder, not a resolved path; ambiguity is real |
| C-003 | CON | 65% | Zero-cost is better than near-zero-cost, but the margin is trivial |
| C-004 | CON | 60% | Discovery does promote more robust worker logic, though the risk of hardcoding is manageable |
| X-001 | PRO | 72% | Cross-phase dependency exists in real tasklists even if uncommon; absence of context forces brittle workarounds |
| A-001 | Tie | 50% | Both agree |
| A-002 | PRO | 75% | Worker cwd is not guaranteed; explicit paths are defensive |

**Convergence**: 6/8 points resolved (75% raw). Excluding the agreed tie (A-001), 6/7 = 85%. PRO wins 5 points, CON wins 2.

---

## Step 3: Base Selection

### Quantitative Assessment

| Metric | Weight | PRO (Inject) | CON (Discover) |
|--------|--------|--------------|----------------|
| Requirement coverage (addresses the asymmetry) | 0.30 | 0.90 | 0.60 |
| Internal consistency | 0.25 | 0.85 | 0.80 |
| Specificity (concrete implementation path) | 0.15 | 0.95 | 0.70 |
| Dependency completeness | 0.15 | 0.80 | 0.75 |
| Scope coverage | 0.15 | 0.85 | 0.80 |
| **Weighted total** | | **0.874** | **0.715** |

### Qualitative Assessment (Key Criteria)

| Dimension | PRO | CON |
|-----------|-----|-----|
| Completeness | 4/5 | 3/5 |
| Correctness | 4/5 | 4/5 |
| Risk coverage | 4/5 | 3/5 |
| Clarity | 5/5 | 4/5 |
| **Total** | 17/20 | 14/20 |

### Combined Score

| Variant | Quant (50%) | Qual (50%) | Combined |
|---------|-------------|------------|----------|
| PRO (Inject) | 0.437 | 0.425 | **0.862** |
| CON (Discover) | 0.358 | 0.350 | 0.708 |

**Selected Base**: Variant 1 (PRO: Inject Context) -- margin 15.4%, no tiebreaker needed.

---

## Step 4: Refactoring Plan (Ruling)

### Decision: INJECT sprint context into Path A

**Ruling**: Sprint context SHOULD be injected into Path A's per-task prompt at `executor.py:1064-1068`. The change mirrors what Path B already provides at `process.py:147-167`.

### Rationale

1. **Parity wins decisively**: Path B already injects this context. The asymmetry is not a deliberate design choice -- it is an omission from when per-task decomposition was added. Maintaining two different prompt shapes creates a maintenance trap.

2. **Cost-benefit is overwhelmingly positive**: ~80 tokens of context prevents a real class of path-resolution failures for cross-phase tasks. The downside risk (workers hardcoding paths) is manageable with review discipline and is dwarfed by the upside (workers never failing to find prior-phase artifacts).

3. **The CON's strongest argument (narrow scope) is addressed by optional use**: Injecting context does not force workers to use it. A task that implements a single function will ignore the sprint context header. A task that needs to validate phase-1 output will use it. The context is informational, not directive.

4. **TASKLIST_ROOT is insufficient alone**: The placeholder convention works for human readers but creates an unnecessary resolution step for automated workers. The `SprintConfig` object already has `release_dir` resolved; not passing it is leaving value on the table.

### Concession to CON (Incorporated)

- **U-002 (separation of concerns)**: The injected context should be clearly labeled as informational. Use the same `## Sprint Context` header as Path B, with a note: "Reference these paths only when your task requires cross-phase artifacts."

### Concrete Change

The prompt at `executor.py:1064-1068` should be updated from:

```python
prompt = (
    f"Execute task {task.task_id}: {task.title}\n"
    f"From phase file: {phase.file}\n"
    f"Description: {task.description}\n"
)
```

To include sprint context (matching `process.py:147-167` structure):

```python
sprint_name = getattr(config, "release_name", None) or config.release_dir.name
total_phases = len(config.phases) if config.phases else phase.number
artifact_root = config.release_dir / "artifacts"
results_dir = config.results_dir

context_lines = [
    f"Execute task {task.task_id}: {task.title}",
    f"From phase file: {phase.file}",
    f"Description: {task.description}",
    "",
    "## Sprint Context",
    f"- Sprint: {sprint_name}",
    f"- Phase: {phase.number} of {total_phases}",
    f"- Artifact root: {artifact_root}",
    f"- Results directory: {results_dir}",
]
if phase.number > 1:
    prior_dirs = [config.release_dir / f"phase-{i}" for i in range(1, phase.number)]
    context_lines.append(
        "- Prior-phase directories: " + ", ".join(str(d) for d in prior_dirs)
    )
prompt = "\n".join(context_lines) + "\n"
```

### Changes NOT Being Made

| Diff Point | Rejected Approach | Rationale |
|------------|-------------------|-----------|
| C-004 | Remove TASKLIST_ROOT convention entirely | TASKLIST_ROOT remains useful for human-readable documentation and as a fallback discovery mechanism. Injection supplements it; does not replace it. |
| U-002 | Keep Path A minimal to enforce narrow scope | Workers can ignore context they do not need. The cost of providing it is negligible. |

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Workers hardcode injected absolute paths | Low | Medium | Code review; TASKLIST_ROOT convention still available as relative alternative |
| Injected paths stale within a run | Near-zero | Low | Paths computed from same SprintConfig that drives execution |
| Prompt size increase causes token pressure | Near-zero | None | ~80 tokens against 100+ turn budget is negligible |

---

## Return Contract

```yaml
return_contract:
  merged_output_path: "docs/generated/sprint-cli/debates/debate-sprint-context.md"
  convergence_score: 0.85
  artifacts_dir: "docs/generated/sprint-cli/debates/"
  status: "success"
  base_variant: "PRO (Inject Context)"
  unresolved_conflicts: 0
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```
