# Major Issues — Consolidated Remediation Proposals

---

## Reflective Analysis Summary

> Added 2026-03-23 — cross-proposal consistency review

### Dependency Order (Apply in This Sequence)

Proposals must be applied in a specific order because later proposals depend on
decisions made by earlier ones. Within a tier, proposals may be applied in any order.

| Tier | Proposals | Rationale |
|---:|---|---|
| 1 | **M7** | Pure numbering fix; prerequisite for all step-number references in other proposals |
| 2 | **M1, M2** | Must be applied together — they co-define prompt resolution and mode selection. M2 refines M1. See contradiction C1 below. |
| 3 | **M4** | Depends on M1/M2 prompt resolution being settled before defining substitution semantics |
| 4 | **M6** | Restructures ref files. Must land before M10 worked example is finalized |
| 5 | **M3, M5** | Independent of each other. M3 fixes task creation ownership; M5 fixes retry scheduling. Both needed before M14 checkpoint schema. |
| 6 | **M8** | Artifact naming convention. Must precede M11, M13, M14 which reference artifact paths and filenames |
| 7 | **M9, M15** | Must be applied together — both modify the return contract and both introduce `mode`. See overlap O4. |
| 8 | **M11** | Extends manifest schema with `skipped_reason`. Depends on M8 artifact naming and M5 retry states being settled. |
| 9 | **M13** | Adds `artifacts_dir` to return contract. Depends on M8 (artifact filenames) and M9 (return contract shape). |
| 10 | **M14** | Checkpoint schema. Depends on M5 (retry model), M8 (artifact paths), M9 (return contract), M11 (manifest schema). Most downstream proposal. |
| 11 | **M10** | Worked example. Should be written last because it must reflect all prior decisions (M6 ref split, M9 return contract, M15 status rules). |
| 12 | **M12** | Validation matrix. Should be finalized last to exercise the full spec surface after all other proposals are applied. |

### Grouping by Spec Section Affected

Proposals that touch the same spec section should be reviewed and applied together
to avoid conflicting edits.

| Spec Section | Proposals | Notes |
|---|---|---|
| `## Execution Mode Selection` | M1, M2 | Both insert conflict-resolution and prompt-resolution rules here |
| `## Options` / `--prompt` row | M1, M2 | Both rewrite the `--prompt` description |
| `## Pipeline Execution` step list | M4, M7 | M7 renumbers steps; M4 rewrites Step 2 bullet |
| `## Return Contract` | M9, M13, M15 | M9 adds `mode` + population matrix; M13 adds `artifacts_dir`; M15 adds status computation + counts |
| `## Wave 3` flow | M3, M6, M10 | M3 rewrites task creation; M6 adds command resolution step; M10 shows worked output |
| `## Wave 2` wording | M6, M10 | M6 changes task assignment wording; M10 must reflect the new wording |
| `refs/decomposition-patterns.md` | M6 | Sole owner of this ref file change |
| `refs/delegation-matrix.md` | M6 | Sole owner of this ref file change |
| Pipeline manifest schema | M8, M11, M14 | M8 adds artifact paths; M11 adds `skipped_reason`; M14 adds checkpoint cross-reference |
| `spawn-orchestrator` agent definition | M3, M5 | M3 removes TaskCreate authority; M5 defines retry scheduling the orchestrator must follow |
| Artifact routing / phase output dirs | M7 (Step 5), M8, M13 | M7 renumbers the step; M8 defines filenames; M13 surfaces them in contract |

### Contradictions Flagged

**C1 — M1 vs M2: `--prompt` in Standard Mode**

M1 does not prohibit `--prompt` in Standard Mode; its case matrix silently handles
the combination by ignoring the positional string when `--prompt` is present in
Pipeline Mode, but says nothing about Standard Mode + `--prompt`.

M2 Step 3 explicitly says: "If `--prompt` is present in Standard Mode, treat it as
an **error**" and adds an ERROR row to the input matrix.

**Resolution required**: Adopt M2's stricter rule. When applying M1, do NOT insert
any text that implies `--prompt` is valid in Standard Mode. Apply M2's Standard Mode
error rule as the normative rule, and ensure M1's case matrix omits Standard Mode
`--prompt` rows or marks them as errors.

---

**C2 — M10 vs M6: Command selection shown in Wave 2**

M10's worked example shows command assignments (e.g., "Command: `/sc:design --type database`")
directly in the Wave 2 hierarchy output. But M6 explicitly moves command selection
to Wave 3, replacing Wave 2's command assignment with normalized `task_type` values.

**Resolution required**: When finalizing M10, the Wave 2 hierarchy output must show
`task_type` (e.g., `schema_design`) instead of delegated commands. The delegation
map table in Wave 3 remains unchanged. Apply M6 before writing the final M10 text.

---

**C3 — M8 vs existing spec: Artifact directory path prefix**

M8 uses `<output_dir>/phases/<phase_id>/` as the canonical path. The existing spec
text (visible in M7 Step 5) uses `<output_dir>/<phase_id>/` without the `phases/`
prefix. M13's example uses `<output_dir>/phases/merge/`.

**Resolution required**: Settle on one canonical form. Recommendation: adopt M8's
`<output_dir>/phases/<phase_id>/` and update M7 Step 5 and all other references
to match.

---

**C4 — M14 wave numbering vs spec wave model**

M14 defines 5 wave checkpoints (Intake, DAG Construction, Dispatch, Artifact Routing,
Completion). The spec's Standard Mode is a 4-wave protocol. Pipeline Mode has 6 steps
per M7. M14 appears to conflate the two models.

**Resolution required**: M14 should define checkpoint boundaries that map cleanly
to both models. For Standard Mode, checkpoints at wave 1-4 boundaries. For Pipeline
Mode, checkpoints at step 1-6 boundaries (per M7). The checkpoint schema itself is
mode-agnostic (it already has `wave_index` and `wave_name`), so this is a documentation
clarification, not a schema change.

### Missing Cross-References (Must Be Added During Application)

| ID | Proposals | Overlap |
|---:|---|---|
| O1 | M1, M2 | Both rewrite `--prompt` option description and Execution Mode Selection. Must be merged into one coherent edit. |
| O2 | M8, M13 | Both enumerate compare-merge artifact filenames. M13 must reference M8's normative table rather than re-listing independently. |
| O3 | M5, M11 | M5 introduces `retry_pending` as a task state; M11 introduces `skipped_reason` as a manifest field. Both affect the phase status model and must share a single coherent status enum. |
| O4 | M9, M15 | Both add `mode` to the return contract. Must be applied as one edit. M15's status computation references M9's mode discriminator. |
| O5 | M9, M13 | Both add fields to the return contract table. M13's `artifacts_dir` should be documented within M9's population matrix as a pipeline-only field. |
| O6 | M11, M14 | Both define resume semantics. M14's resume validator must honor M11's `skipped_reason` re-evaluation rules. |
| O7 | M3, M5 | Both constrain `spawn-orchestrator` behavior. M3 removes task creation; M5 defines retry scheduling. Orchestrator agent definition needs a single coherent responsibility list. |

### Gaps — Issues Not Adequately Addressed

**G1 — Standard Mode `--resume` checkpoint schema**

M14 provides a detailed checkpoint schema heavily oriented toward Pipeline Mode
(phase IDs, phase statuses, DAG snapshots). Standard Mode uses a 4-wave protocol
with task hierarchies, not pipeline phases. M14 should include a Standard Mode
checkpoint variant showing `wave_state` for Standard Mode waves (domain detection,
decomposition, delegation, aggregation) rather than only pipeline-centric examples.

**G2 — M12 does not validate M4 single-pass substitution**

The M12 validation matrix exercises flags, modes, and error paths but does not
include a scenario that verifies single-pass `${prompt}` substitution semantics
(the adversarial case from M4). Add a scenario like:

| ID | Scenario | Invocation | Expected | Pass criteria |
|---|---|---|---|---|
| B06 | Adversarial prompt containing `${prompt}` | `--pipeline @BNM.yaml --prompt 'debug the ${prompt} handler'` | Resolved command contains literal `${prompt}` text, no recursive expansion | Output shows exact text without double-substitution |

**G3 — Unified phase/task status enum**

M5 introduces `retry_pending` for tasks. M11 introduces `skipped` with `skipped_reason`
for phases. M15 references `manual` as a terminal state. No single proposal defines
the complete, canonical status enum shared across tasks, phases, and manifests. A
unified status model should be extracted and placed in a shared location in the spec.

Recommended unified enum:
`pending | running | completed | failed | retry_pending | skipped | manual`

With `skipped_reason` as a companion field per M11.

**G4 — No proposal addresses `--pipeline-seq` interaction with retry scheduling**

M5 defines retry-after-batch-drain semantics for parallel sub-groups. When
`--pipeline-seq` forces sequential execution, every phase becomes its own sub-group
of size 1. M5's model still works but should explicitly state that sequential mode
is the degenerate case (sub-group size = 1, retry pass = at most 1 task). This is
a minor clarification gap.

### Implementation Notes

1. **Apply M7 first** — it is mechanical (renumbering only) and all subsequent proposals
   reference pipeline execution steps by number.

2. **Merge M1+M2 into a single spec edit** — they target the same sections and their
   individual amendment texts will conflict if applied sequentially. Produce one
   unified "Prompt Resolution Rules" section that incorporates both proposals.

3. **M10 must be written after M6** — the worked example currently shows command
   selection in Wave 2, which M6 explicitly forbids. Rewrite M10's Wave 2 output
   to use `task_type` values, and move the command column to the Wave 3 delegation map.

4. **M9 + M13 + M15 should be a single return-contract edit pass** — all three add
   fields or rules to `## Return Contract`. Applying them independently risks
   conflicting table edits. Produce one unified return contract table and one
   unified population matrix.

5. **M14 is the most downstream proposal** — it depends on decisions from M5 (retry
   model), M8 (artifact paths), M9 (return contract shape), and M11 (manifest
   schema). Apply it last among the technical proposals.

6. **M12 should be finalized after all other proposals** — the validation matrix
   exercises the full spec surface and should reflect all changes. Add scenario B06
   for M4 adversarial substitution coverage.

7. **Artifact path prefix** — resolve C3 early (adopt `<output_dir>/phases/<phase_id>/`)
   and propagate to M7, M8, M13, and M14 consistently.

8. **Extract a unified status enum** — after applying M5, M11, and M15, document the
   canonical status model in one spec location and reference it from all three
   proposals' affected sections.

---

# M1 Remediation Proposal — Pipeline vs Task Description Ambiguity

## Issue

The current `/sc:spawn` v2 spec says:
- If `--pipeline` is present, enter Pipeline Mode.
- Standard Mode is triggered by a task description.

But it does not define what happens when both are present, e.g.:

```bash
/sc:spawn "implement auth" --pipeline @dag.yaml
```

That leaves three things ambiguous:
1. Which mode wins
2. What happens to the task description
3. How `generate-parallel` obtains a prompt when Pipeline Mode needs one and no explicit `--prompt` was supplied

---

## Proposed Resolution

### 1. Precedence Rule

**`--pipeline` always wins.**

If the `--pipeline` flag is present, `/sc:spawn` MUST enter **Pipeline Mode** regardless of whether a positional task description is also present.

Rationale:
- This preserves the existing selection rule already stated in the spec.
- Pipeline Mode is the more explicit user instruction because it supplies a concrete execution plan.
- It avoids a split-brain interpretation where the same invocation might partially decompose a task and partially execute a DAG.

---

### 2. Fate of the Losing Argument

If both `--pipeline` and a positional task description are present:

**Treat the task description as an implicit pipeline prompt candidate.**

More precisely:
- If `--prompt` is also present, the positional task description is **ignored for execution** and MUST produce a **WARN** message explaining that Pipeline Mode is active and explicit `--prompt` takes precedence.
- If `--prompt` is absent, the positional task description is **promoted to implicit `--prompt`** for Pipeline Mode.

This gives the positional string a useful meaning instead of silently discarding it, while still keeping mode selection deterministic.

### Why this is the best fit

Compared with the alternatives:

#### Option A — Ignore the task description entirely
Rejected because it is too surprising. A user who writes:

```bash
/sc:spawn "implement auth" --pipeline @dag.yaml
```

would reasonably expect the quoted string to matter.

#### Option B — Hard error on both being present
Rejected because it is unnecessarily strict. The combination can be resolved cleanly and ergonomically.

#### Option C — Convert positional task description into implicit `--prompt`
**Recommended.** This makes the command forgiving while still predictable.

---

## Normative Behavior

### Case Matrix

| Invocation shape | Effective mode | Effective prompt | Behavior |
|---|---|---|---|
| `/sc:spawn "task"` | Standard Mode | N/A | Use positional string as task description |
| `/sc:spawn --pipeline @dag.yaml --prompt "idea"` | Pipeline Mode | `--prompt` | Normal pipeline execution |
| `/sc:spawn "task" --pipeline @dag.yaml` | Pipeline Mode | positional task description | Promote positional string to implicit `--prompt` |
| `/sc:spawn "task" --pipeline @dag.yaml --prompt "idea"` | Pipeline Mode | `--prompt` | Positional task description ignored with warning |
| `/sc:spawn --pipeline @dag.yaml` | Pipeline Mode | none | Valid only if DAG does not require `${prompt}`; otherwise STOP |

---

## 3. Edge Case: `generate-parallel` Needs a Prompt but No Explicit `--prompt`

### Rule

When Pipeline Mode is active, prompt resolution MUST follow this order:

1. **Explicit `--prompt` flag**
2. **Positional task description**, but only when `--pipeline` is present
3. **No prompt available**

### Consequence for `generate-parallel`

If a pipeline phase references `${prompt}` or otherwise declares that it consumes the pipeline prompt:
- Use `--prompt` if provided.
- Else use the positional task description if one was provided alongside `--pipeline`.
- Else STOP with the existing missing-prompt error.

This resolves the exact ambiguity raised by M1:

```bash
/sc:spawn "implement auth" --pipeline @dag.yaml
```

If `@dag.yaml` contains a `generate-parallel` phase such as:

```yaml
- id: branch
  type: generate-parallel
  source: agents
  prompt: prompt
  command_template: "${prompt}"
```

then `"implement auth"` becomes the effective prompt for that phase.

### Important boundary

The positional task description becomes an implicit `--prompt` **only in Pipeline Mode**.
It is **not** dual-purposed in Standard Mode.

That keeps Standard Mode simple:
- In Standard Mode, the trailing/quoted positional string is the task description.
- In Pipeline Mode, the same positional slot may serve as implicit prompt text if `--pipeline` is present.

---

## 4. Spec Amendment Text

Add the following rule to `.dev/releases/backlog/v4.xx-SpawnV2/spec.md` immediately after the current **Selection rule** in `## Execution Mode Selection`.

### Proposed insertion

```md
**Conflict resolution when both task description and `--pipeline` are present**:
If `--pipeline` is present, `/sc:spawn` MUST enter Pipeline Mode even when a positional task description is also provided.

In this situation, resolve the positional task description as follows:
- If `--prompt` is present, `--prompt` is the effective pipeline prompt and the positional task description is ignored for execution. Emit a WARN: "Task description ignored in Pipeline Mode because explicit --prompt was provided."
- If `--prompt` is absent, treat the positional task description as an implicit `--prompt` value for Pipeline Mode.

Prompt resolution order in Pipeline Mode:
1. Explicit `--prompt`
2. Positional task description (only when `--pipeline` is present)
3. None

If the DAG requires `${prompt}` and no effective prompt is available after this resolution, STOP with error: "--prompt required for this DAG".
```

---

## Recommended Companion Edits

To keep the spec internally consistent, also update these sections.

### A. Usage / Options section

Current wording says `--prompt` is also accepted as a trailing quoted string, but does not scope that behavior. Replace with:

```md
| `--prompt` | — | Prompt text passed to Pipeline Mode phases. In Pipeline Mode only, a positional task description may be used as an implicit prompt when `--prompt` is absent. |
```

This avoids implying that Standard Mode has both a task description and a second trailing prompt channel.

### B. Standard Mode trigger text

Clarify that in Standard Mode the positional argument is always interpreted as the task description, never as a prompt.

Suggested line:

```md
Triggered by: `/sc:spawn "task description" [flags]`
In Standard Mode, the positional string is always the task description.
```

### C. Pipeline execution interpolation step

Where the spec currently says:

- `Substitute ${prompt} from --prompt CLI value. STOP if missing.`

replace with:

- `Substitute ${prompt} from the effective pipeline prompt. Resolve in order: (1) explicit --prompt, (2) positional task description when --pipeline is present. STOP if still missing.`

### D. Error table

Add a row:

| Both task description and `--pipeline` provided | Enter Pipeline Mode | Positional task description becomes implicit `--prompt` unless explicit `--prompt` is present |

Optionally add a second row:

| Both task description, `--pipeline`, and `--prompt` provided | Enter Pipeline Mode | WARN that task description is ignored for execution |

---

## User-Facing Behavior Examples

### Example 1 — Positional string becomes implicit prompt

```bash
/sc:spawn "implement auth" --pipeline @dag.yaml
```

Behavior:
- Enter Pipeline Mode
- Effective prompt = `implement auth`
- If DAG uses `${prompt}`, interpolation succeeds
- Standard decomposition is skipped

### Example 2 — Explicit prompt wins

```bash
/sc:spawn "implement auth" --pipeline @dag.yaml --prompt "/sc:brainstorm design a secure auth system"
```

Behavior:
- Enter Pipeline Mode
- Effective prompt = `/sc:brainstorm design a secure auth system`
- Positional task description is ignored for execution
- Emit warning about ignored task description

### Example 3 — No prompt available

```bash
/sc:spawn --pipeline @dag.yaml
```

Behavior:
- Enter Pipeline Mode
- If DAG does not require `${prompt}`, continue
- If DAG requires `${prompt}`, STOP with:
  `--prompt required for this DAG`

---

## Acceptance Criteria

1. `/sc:spawn "task" --pipeline @dag.yaml` always selects Pipeline Mode.
2. In that invocation, the positional string is available as the effective prompt when `--prompt` is absent.
3. `--prompt` always overrides any positional task description in Pipeline Mode.
4. Standard Mode never interprets the positional task description as a prompt.
5. A DAG using `${prompt}` succeeds when either explicit `--prompt` or positional task description is available in Pipeline Mode.
6. A DAG using `${prompt}` stops with a clear error when neither is available.
7. The spec text explicitly documents this precedence and prompt-resolution order.

---

## Final Recommendation

Adopt the following policy:

- **Mode precedence**: `--pipeline` wins.
- **Losing argument behavior**: positional task description becomes implicit `--prompt` in Pipeline Mode, unless explicit `--prompt` is present.
- **Prompt fallback**: `generate-parallel` and any `${prompt}` consumer resolve prompt via `--prompt` first, then positional task description.
- **Spec rule**: add a normative conflict-resolution block under `## Execution Mode Selection` and update all `${prompt}` references to say "effective pipeline prompt," not just `--prompt`.

This is the least surprising, most ergonomic, and most internally consistent resolution for M1.

---

# M2: Prompt Parsing Ambiguity — Remediation Proposal

## Problem
The v2 `sc:spawn` spec says `--prompt` is "also accepted as trailing quoted string" but never defines how that trailing string is resolved across execution modes.

This creates ambiguity in at least four areas:
- In Standard Mode, the trailing quoted string is already the task description.
- In Pipeline Mode, a trailing quoted string could plausibly be the phase prompt.
- The spec does not define whether `--prompt` or the trailing string wins when both are present.
- The spec does not define whether trailing positional text is legal in Pipeline Mode when `--pipeline` is present.

Because mode selection is already explicit (`--pipeline` => Pipeline Mode, otherwise Standard Mode), prompt resolution should also become mode-aware and deterministic.

## Step-by-Step Solution

### Step 1: Define two distinct semantic inputs
Separate the currently overloaded trailing string into two different concepts:

- **Task description**: the primary positional argument for Standard Mode
- **Pipeline prompt**: auxiliary prompt text passed to pipeline phases in Pipeline Mode

This removes the current ambiguity where one quoted string could mean either "the thing to do" or "extra prompt context."

### Step 2: Make mode selection happen before prompt resolution
Use the existing selection rule as the first branch:

- If `--pipeline` is present, enter **Pipeline Mode**
- Otherwise, enter **Standard Mode**

Only after mode is known should the parser decide what any trailing positional string means.

This keeps the grammar simple and prevents "guessing" based on position alone.

### Step 3: Standard Mode rule — trailing positional string is always the task description
In Standard Mode:
- The first trailing positional string is the **task description**
- `--prompt` is **not used for mode input selection** and must not override the task description
- If `--prompt` is present in Standard Mode, treat it as an **error** rather than trying to reinterpret inputs

**Why**:
- Standard Mode is defined as `Task description → domain analysis → decomposition → delegation`
- The user’s trailing quoted string is already the canonical task input
- Reusing `--prompt` in Standard Mode introduces a second competing source of truth for the same concept

**Rule**:
- Standard Mode accepts exactly one semantic task input source: the positional task description
- `--prompt` is reserved for Pipeline Mode

### Step 4: Pipeline Mode rule — `--prompt` is canonical, trailing positional string is fallback only
In Pipeline Mode:
- `--prompt` is the **canonical** source for prompt text passed to DAG phases
- A trailing positional string may be accepted as a **fallback alias** for `--prompt`
- The trailing positional string is only used when `--prompt` is absent

**Precedence in Pipeline Mode**:
1. `--prompt "..."`
2. trailing positional string
3. no prompt provided

**Why**:
- This exactly matches the panel recommendation
- It preserves convenience for shorthand CLI usage
- It avoids conflicting prompt definitions when both forms are supplied

### Step 5: Define explicit conflict behavior when both exist in Pipeline Mode
When both `--prompt` and a trailing positional string are provided in Pipeline Mode:
- `--prompt` **wins**
- The trailing positional string is **ignored with a warning**
- Do not merge the two strings
- Do not silently choose one without documenting the behavior

**Warning text to specify in the protocol**:
> Both `--prompt` and trailing prompt text were provided in Pipeline Mode. `--prompt` takes precedence; trailing prompt text was ignored.

**Why warning instead of hard error**:
- The panel recommendation already indicates precedence, not rejection
- Warning preserves backward compatibility and CLI convenience
- It avoids surprising failures for users who redundantly specify both forms

### Step 6: Disallow multiple trailing positional strings in both modes
To keep parsing deterministic:
- Allow at most **one** trailing positional string after flags are parsed
- If multiple positional strings remain, STOP with a usage error

**Error condition**:
- Standard Mode: more than one positional argument after command parsing
- Pipeline Mode: more than one fallback prompt positional argument

**Why**:
- The spec only models one task description or one pipeline prompt
- Multiple free-form strings make precedence and tokenization ambiguous

### Step 7: Define the full prompt-resolution algorithm
Add this algorithm to the protocol skill/spec:

```text
1. Parse flags and positional arguments.
2. If `--pipeline` is present, select Pipeline Mode; else select Standard Mode.
3. Count remaining trailing positional strings.
4. If positional_count > 1: STOP with usage error.
5. If Standard Mode:
   - If positional_count == 0: STOP with "task description required"
   - If `--prompt` is present: STOP with "--prompt is only valid in Pipeline Mode"
   - task_description = positional[0]
6. If Pipeline Mode:
   - If `--prompt` is present:
       phase_prompt = value of `--prompt`
       If positional_count == 1: WARN and ignore positional[0]
   - Else if positional_count == 1:
       phase_prompt = positional[0]
   - Else:
       phase_prompt = null
```

This gives deterministic behavior for every input combination.

### Step 8: Document the accepted input matrix
Add a compact truth table so users and implementers do not have to infer behavior.

| Mode | `--pipeline` | `--prompt` | trailing positional string | Result |
|------|--------------|------------|----------------------------|--------|
| Standard | no | no | yes | positional string = task description |
| Standard | no | yes | yes/no | ERROR: `--prompt` invalid in Standard Mode |
| Standard | no | no | no | ERROR: task description required |
| Pipeline | yes | yes | no | `--prompt` = phase prompt |
| Pipeline | yes | no | yes | positional string = phase prompt |
| Pipeline | yes | yes | yes | `--prompt` wins; positional ignored with warning |
| Pipeline | yes | no | no | no phase prompt provided |
| Pipeline/Standard | any | any | >1 positional strings | ERROR: too many positional arguments |

### Step 9: Update usage text so CLI grammar matches the rules
The current usage line implies a single positional `[complex-task]` even though the options table says `--prompt` can also be trailing text.

Replace that ambiguity with mode-specific usage examples.

**Revised usage**:
```text
Standard Mode:
/sc:spawn "<task-description>" [--strategy ...] [--depth ...] [--no-delegate] [--dry-run] [--resume]

Pipeline Mode:
/sc:spawn --pipeline "<shorthand>" [--prompt "<phase-prompt>"] [--agents ...] [--pipeline-seq] [--pipeline-resume]
/sc:spawn --pipeline @path.yaml [--prompt "<phase-prompt>"] [--agents ...] [--pipeline-seq] [--pipeline-resume]
/sc:spawn --pipeline "<shorthand>" "<phase-prompt>"   # fallback alias when --prompt is omitted
```

This makes the overloaded positional grammar explicit instead of implicit.

### Step 10: Update the `--prompt` option description
Replace the current description:
> Prompt text passed to DAG phases (also accepted as trailing quoted string)

With:
> Prompt text passed to DAG phases in Pipeline Mode. If `--pipeline` is present and `--prompt` is omitted, one trailing positional string may be used as a fallback alias. `--prompt` takes precedence over trailing prompt text. `--prompt` is invalid in Standard Mode.

This makes the precedence and mode scoping load-bearing in the flags table itself.

## Recommended Normative Spec Text

Add a new subsection under **Execution Mode Selection** or immediately before **Pipeline Mode**:

```markdown
### Prompt Resolution Rules

Prompt resolution is mode-dependent and occurs only after execution mode is selected.

#### Standard Mode
- The trailing positional string is the required task description.
- `--prompt` is not valid in Standard Mode.
- If no trailing positional string is provided, STOP with a usage error.
- If more than one trailing positional string is provided, STOP with a usage error.

#### Pipeline Mode
- `--prompt` defines the prompt text passed to DAG phases.
- If `--prompt` is omitted, one trailing positional string may be used as a fallback alias for the pipeline prompt.
- If both `--prompt` and a trailing positional string are provided, `--prompt` takes precedence and the trailing positional string is ignored with a warning.
- If more than one trailing positional string is provided, STOP with a usage error.
- Pipeline Mode does not require prompt text; the pipeline may run with no prompt if phase definitions are otherwise sufficient.
```

## Rationale

This solution is preferable because it:
- Preserves the existing Standard Mode mental model: quoted trailing text = task description
- Preserves convenience in Pipeline Mode without making fallback syntax authoritative
- Gives a single canonical winner when both prompt forms are present
- Avoids hidden merging behavior
- Minimizes implementation complexity by branching on mode first
- Matches the expert panel recommendation exactly where it matters

## Example Inputs and Outcomes

### Standard Mode examples
```bash
/sc:spawn "implement OAuth login"
```
Result: Standard Mode, task description = `implement OAuth login`

```bash
/sc:spawn "implement OAuth login" --prompt "extra context"
```
Result: ERROR — `--prompt` is only valid in Pipeline Mode

```bash
/sc:spawn
```
Result: ERROR — task description required

### Pipeline Mode examples
```bash
/sc:spawn --pipeline "analyze>design>implement"
```
Result: Pipeline Mode, no phase prompt

```bash
/sc:spawn --pipeline "analyze>design>implement" --prompt "focus on auth boundary conditions"
```
Result: Pipeline Mode, phase prompt = `focus on auth boundary conditions`

```bash
/sc:spawn --pipeline "analyze>design>implement" "focus on auth boundary conditions"
```
Result: Pipeline Mode, trailing positional string used as fallback phase prompt

```bash
/sc:spawn --pipeline "analyze>design>implement" --prompt "use spec A" "use spec B"
```
Result: Pipeline Mode, phase prompt = `use spec A`; trailing positional string ignored with warning

## Files to Modify
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`
  - Update `## Usage`
  - Update the `--prompt` row in `## Options`
  - Add a new `### Prompt Resolution Rules` subsection under mode selection
  - Add 2-4 examples covering Standard vs Pipeline prompt resolution

## Final Recommendation
Adopt the following policy as the normative rule:

- **Standard Mode**: trailing positional string = task description; `--prompt` is invalid
- **Pipeline Mode**: `--prompt` = canonical phase prompt; trailing positional string = fallback alias only when `--prompt` is absent
- **Conflict rule**: when both are present in Pipeline Mode, `--prompt` wins and trailing positional text is ignored with warning
- **Validation rule**: more than one trailing positional string is always an error

This fully resolves M2 by making prompt parsing explicit, mode-scoped, and deterministic across all input combinations.


---

# Major Issue M3 — Eliminate Duplicate `TaskCreate` Entries

## Problem Statement

The current Spawn V2 spec assigns task creation to two different actors in the same execution path:

1. **Wave 3 Step 1 in the skill** creates one `TaskCreate` entry per task.
2. **`spawn-orchestrator` Responsibility 1** also creates one `TaskCreate` entry per delegated task.

When `tasks_created > 8`, the skill first creates tracked tasks and then dispatches `spawn-orchestrator` for Steps 3-5. Because the orchestrator is also instructed to create task entries, the same delegated tasks receive duplicate tracking records.

## Recommended Fix

Assign **all task creation to the skill**, and make the orchestrator operate only on **pre-created task IDs**.

This is the cleaner contract because:

- the skill already owns hierarchy generation and delegation readiness
- `tasks_created` is already defined as a skill-level return value
- the orchestrator is introduced as a scale-management layer for dispatch/monitoring/aggregation, not as a second planner
- this preserves one canonical source of truth for task identity before orchestration begins

## Decision

**Ownership rule**: The `sc:spawn-protocol` skill is the only component allowed to create `TaskCreate` entries for Wave 3 delegated tasks.

**Orchestrator rule**: `spawn-orchestrator` must consume the existing task records created by the skill and must never create duplicate tracking entries for the same hierarchy tasks.

---

## Exact Spec Changes

### 1. Update Wave 3 flow in `spec.md`

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

#### Replace this current block

```markdown
1. **Task Creation**: For each Task in the hierarchy:
   - `TaskCreate` with description, status `pending`, dependencies noted
2. **Prompt Construction**: For each delegated task, apply prompt
   construction rules (from delegation-matrix ref):
   - Rule 1: Resolve file paths before delegation (Glob/Read)
   - Rule 2: Inject tiered evidence requirements (verification vs discovery)
   - Rule 3: Inject cross-reference counts when available
   - Do NOT override delegated command's output structure
3. **Agent Dispatch**: For each parallel group, dispatch tasks via Task tool:
   - Read the appropriate agent `.md` file from `src/superclaude/agents/`
   - Inject agent definition + enriched prompt into Task prompt
   - Dispatch up to MAX_CONCURRENT (10) tasks per parallel group
   - If group exceeds 10: split into sub-groups, dispatch sequentially
   - Wait for group completion before dispatching dependent groups
4. **Progress Tracking**:
   - `TaskUpdate` as each sub-agent completes
   - `TaskList`/`TaskGet` for status monitoring
   - If a sub-agent fails: retry once, then mark as `manual` and continue
5. **Result Aggregation**: Collect outputs from all completed tasks.
   Compile summary with per-task status.

**Agent delegation**: If tasks_created > 8, dispatch `spawn-orchestrator`
agent to handle steps 3-5 instead of inline execution.
```

#### With this revised block

```markdown
1. **Task Creation**: For each Task in the hierarchy, the skill MUST create exactly one tracked task entry:
   - `TaskCreate` with description, status `pending`, dependencies noted
   - Record the returned task ID in the delegation map
   - This skill is the ONLY component that creates TaskCreate entries for Wave 3 hierarchy tasks
2. **Prompt Construction**: For each delegated task, apply prompt
   construction rules (from delegation-matrix ref):
   - Rule 1: Resolve file paths before delegation (Glob/Read)
   - Rule 2: Inject tiered evidence requirements (verification vs discovery)
   - Rule 3: Inject cross-reference counts when available
   - Do NOT override delegated command's output structure
3. **Dispatch Execution**:
   - If `tasks_created <= 8`: the skill dispatches tasks inline via Task tool
   - If `tasks_created > 8`: dispatch `spawn-orchestrator` and pass the pre-created task IDs, hierarchy, DAG ordering, delegation map, and enriched prompts
4. **Progress Tracking**:
   - Inline mode (`tasks_created <= 8`): the skill performs `TaskUpdate`, `TaskList`, and `TaskGet`
   - Orchestrated mode (`tasks_created > 8`): `spawn-orchestrator` performs `TaskUpdate`, `TaskList`, and `TaskGet` against the pre-created task IDs
5. **Result Aggregation**: Collect outputs from all completed tasks.
   Compile summary with per-task status.

**Agent delegation**: If `tasks_created > 8`, dispatch `spawn-orchestrator`
agent to handle steps 3-5 only. Step 1 remains owned by the skill.
```

### 2. Tighten the agent delegation table wording

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

#### Replace this row

```markdown
| `spawn-orchestrator` | Progress tracking and result aggregation | This skill (Wave 3) | When tasks_created > 8 |
```

#### With this row

```markdown
| `spawn-orchestrator` | Dispatch coordination, progress tracking, and result aggregation over pre-created tasks | This skill (Wave 3) | When tasks_created > 8 |
```

This removes any implication that the orchestrator is responsible for creating tracked tasks.

### 3. Update the orchestrator tools section to remove task creation authority

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

#### Replace this current tools block line

```markdown
- **TaskCreate**: Create tracked tasks for each delegation
```

#### With this line

```markdown
- **TaskCreate**: Not used for Wave 3 hierarchy tasks; task records are pre-created by the skill
```

If you want the cleanest possible spec, an even stronger option is to remove `TaskCreate` from the orchestrator tools list entirely. But if you want to preserve flexibility for future non-hierarchy bookkeeping, the explicit prohibition above is safer and more precise.

### 4. Rewrite orchestrator Responsibility 1

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

#### Replace this current responsibility block

```markdown
1. **Create task entries**: One TaskCreate per delegated task from the hierarchy
2. **Dispatch parallel groups**: Launch concurrent Task agents for each
   parallel group, respecting DAG ordering between groups
3. **Monitor completion**: Poll TaskList/TaskGet for status updates
4. **Handle failures**: Retry failed tasks once, then mark as `manual`
   and continue with remaining tasks
5. **Aggregate results**: Collect outputs from all completed tasks,
   compile summary with per-task status and artifact paths
6. **Produce orchestration report**: Write hierarchy document with final
   status, delegation map, and completion summary
```

#### With this revised responsibility block

```markdown
1. **Consume existing task entries**: Use the pre-created task IDs supplied by the skill as the canonical tracking records for all delegated hierarchy tasks; do NOT create duplicate TaskCreate entries
2. **Dispatch parallel groups**: Launch concurrent Task agents for each
   parallel group, respecting DAG ordering between groups
3. **Monitor completion**: Poll TaskList/TaskGet for status updates on the pre-created task IDs
4. **Handle failures**: Retry failed tasks once, then mark as `manual`
   and continue with remaining tasks
5. **Aggregate results**: Collect outputs from all completed tasks,
   compile summary with per-task status and artifact paths
6. **Produce orchestration report**: Write hierarchy document with final
   status, delegation map, and completion summary
```

### 5. Add an explicit invariant sentence near Wave 3

File:
`/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`

Add this sentence immediately after the Wave 3 delegation rule:

```markdown
**Invariant**: Each hierarchy task maps to exactly one `TaskCreate` entry, created by the skill before any inline or orchestrated dispatch begins.
```

This turns the anti-duplication requirement into a testable contract instead of an implied convention.

---

## Why This Option Is Better Than Making the Orchestrator Own Task Creation

The alternative fix would be: skip Wave 3 Step 1 when `tasks_created > 8`, and let the orchestrator create all task records. That is workable, but weaker.

Reasons to prefer skill-owned task creation:

1. **Stable identity before branching**
   - The skill creates the hierarchy and knows the final task set.
   - Creating task IDs at that point gives a stable record before execution mode splits into inline vs orchestrated.

2. **Single return-contract meaning for `tasks_created`**
   - `tasks_created` continues to mean tasks actually created by the skill.
   - No delayed or mode-dependent semantics.

3. **Cleaner separation of concerns**
   - Skill: decompose, define, create, hand off.
   - Orchestrator: dispatch, monitor, aggregate.

4. **Lower ambiguity for tests and future maintenance**
   - There is one creation site to validate.
   - Duplicate-entry regressions become easy to detect.

---

## Suggested Acceptance Criteria

Add these acceptance criteria to the remediation decision or test plan:

1. When `tasks_created <= 8`, the skill creates exactly one `TaskCreate` entry per hierarchy task and dispatches inline.
2. When `tasks_created > 8`, the skill still creates exactly one `TaskCreate` entry per hierarchy task before dispatching `spawn-orchestrator`.
3. In orchestrated mode, `spawn-orchestrator` does not call `TaskCreate` for any hierarchy task already represented in the delegation map.
4. Across both modes, every hierarchy task corresponds to exactly one tracked task entry.
5. The final orchestration summary reports status against the original task IDs created by the skill.

---

## Final Recommended Wording

If you want the shortest possible governing rule to reuse across the spec, use this exact sentence:

```markdown
Task creation is owned exclusively by the `sc:spawn-protocol` skill; `spawn-orchestrator` may dispatch, monitor, update, and aggregate pre-created tasks, but must not create duplicate `TaskCreate` entries for hierarchy tasks.
```

That sentence captures the entire fix in one normative contract.


---

# Major Issue M4 — Recursive `${prompt}` Expansion

## Issue

If `--prompt` contains the literal text `${prompt}`, a naive implementation of:

```yaml
command_template: "${prompt}"
```

can accidentally recurse, re-expand, or produce ambiguous output.

Example:

```bash
/sc:spawn --pipeline @BranchNMerge.yaml --prompt 'debug the ${prompt} handler'
```

Without explicit rules, an implementation might:
1. repeatedly substitute `${prompt}` until no sentinel remains,
2. accidentally duplicate text during iterative replacement, or
3. leave `${prompt}` in the final command without clarifying whether it is literal text or still a placeholder.

---

## Approved Solution

Define **single-pass substitution semantics** for `command_template` expansion.

`command_template` placeholders are resolved exactly once against a fixed substitution map built from CLI inputs and phase metadata. The result of substitution is treated as final plain text. Placeholder-like text that appears inside substituted values is **not** interpreted again.

For M4 specifically:
- `${prompt}` in `command_template` means "insert the raw `--prompt` string once"
- if the inserted prompt itself contains `${prompt}`, that embedded text remains literal
- no recursive expansion is allowed
- no post-substitution re-scan is allowed

This removes both infinite/iterative expansion risk and ambiguity about the meaning of `${prompt}` after resolution.

---

## Step-by-Step Remediation

### Step 1: Define a substitution model

Add a short normative subsection near the dynamic phase expansion rules defining template substitution.

Required semantics:
1. Build a substitution map from the current CLI invocation and resolved phase context.
2. Scan the original `command_template` string once.
3. Replace each recognized placeholder in that original template with its mapped string value.
4. Return the resulting string as the resolved command.
5. Do not scan the resolved command for placeholders again.

This must explicitly state that substitution is based on the **original template**, not on progressively rewritten output.

### Step 2: Define `${prompt}` precisely

Add language that `${prompt}` resolves to the exact raw bytes/characters of the CLI `--prompt` argument after normal CLI parsing, with no recursive template interpretation.

Required clarification:
- shell parsing happens before Claude sees the argument
- Spawn template substitution operates only on the already-parsed string value
- Spawn does not treat `${...}` sequences inside that value as special

### Step 3: Specify unknown-placeholder behavior

To avoid future ambiguity, define placeholder handling generally:
- recognized placeholders may be substituted
- unrecognized placeholders in `command_template` MUST cause STOP with a clear error

This prevents hidden second-pass behavior such as "leave unknown ones for later."

Suggested error form:

```text
Error: Unknown command_template placeholder '${name}' in phase '<phase_id>'.
Supported placeholders: ${prompt}, ...
```

If the team wants to keep the placeholder surface minimal for now, document only `${prompt}` as supported.

### Step 4: Make escaping optional but explicit

Escaping is not strictly required to solve M4, because single-pass semantics already make embedded `${prompt}` literal after insertion.

However, the spec should still define one of these two positions explicitly:

#### Option A — Minimal rule set (recommended)
Do not introduce template escaping yet.

State:
- placeholder recognition applies only to the original `command_template`
- `${prompt}` inside substituted values is always literal text
- if a user needs literal `${prompt}` in the template itself, they can avoid using that token in `command_template`

This is sufficient for the current SpawnV2 scope and keeps the grammar simple.

#### Option B — Add explicit escaping
If you want future-proofing now, define `\${` as an escape sequence in `command_template`.

State:
- `\${prompt}` in `command_template` emits literal `${prompt}`
- escaped sequences are unescaped after placeholder parsing
- escape processing also occurs only once, on the original template

Recommendation: use **Option A** unless there is already a requirement for literal placeholder syntax inside templates themselves.

### Step 5: Add a worked example covering the attack

Add the exact adversarial example to the spec so implementers cannot miss the intended behavior.

Example:

```yaml
command_template: "${prompt}"
```

CLI input:

```text
--prompt 'debug the ${prompt} handler'
```

Resolved command:

```text
debug the ${prompt} handler
```

Interpretation note:
- the `${prompt}` substring in the resolved command is literal user text
- it is not a variable reference
- no further expansion occurs

### Step 6: Place the rule in the correct spec locations

Update the main execution flow and the dynamic phase section, not just one or the other.

Files/sections to update:
1. `SKILL.md` dynamic phase type section for `generate-parallel`
2. `SKILL.md` Pipeline Execution Step 2 (Expand Dynamic Phases)
3. optionally `refs/dependency-graph.md` if template resolution behavior is described there or if that file becomes the canonical parse/expansion reference

The key is that both the schema example and the execution algorithm must say the same thing.

---

## Exact Spec Text Additions

## A. Add under `generate-parallel` after the expansion example

```markdown
**Command template substitution semantics**:
- `command_template` placeholder substitution is **single-pass only**.
- The implementation MUST evaluate placeholders against the **original template string** and produce one resolved command string.
- The resolved command MUST NOT be scanned again for placeholder expansion.
- `${prompt}` resolves to the exact parsed value of the CLI `--prompt` argument.
- If the `--prompt` value itself contains `${prompt}` or any other `${...}` sequence, that text is treated as **literal content** after substitution, not as a nested placeholder.
- Unknown placeholders in `command_template` MUST cause STOP with a clear error.
```

## B. Replace the current Pipeline Execution Step 2 bullet

Current bullet:

```markdown
- Substitute `${prompt}` from `--prompt` CLI value. STOP if missing.
```

Replace with:

```markdown
- Substitute `command_template` placeholders using **single-pass** resolution against CLI inputs and resolved phase context. STOP if required values are missing.
- `${prompt}` resolves to the exact parsed `--prompt` CLI value.
- Placeholder-like text inside substituted values is literal and MUST NOT be expanded again.
- Unknown placeholders in `command_template` MUST cause STOP with details.
```

## C. Add a normative example immediately after Step 2 or in the dynamic phase section

```markdown
**Single-pass example**:

Given:

```yaml
command_template: "${prompt}"
```

and:

```text
--prompt 'debug the ${prompt} handler'
```

the resolved command is:

```text
debug the ${prompt} handler
```

The `${prompt}` substring in the resolved command is literal user text. It is not re-expanded.
```

## D. Optional escaping text only if escaping is adopted

```markdown
**Escaping**:
- In `command_template`, `\${` emits a literal `${`.
- Escape handling is applied once on the original template before or during placeholder parsing.
- Escaped placeholder syntax is never treated as a substitution target.
```

If escaping is not adopted, add this sentence instead:

```markdown
No escape syntax is defined for `command_template` in SpawnV2; only placeholders present in the original template are substitution candidates.
```

---

## Recommended Final Policy

Use this policy for M4:

1. **Single-pass only**
2. **No recursive expansion ever**
3. **`${prompt}` resolves to raw parsed `--prompt` text**
4. **Placeholder syntax inside substituted values is literal**
5. **Unknown placeholders are errors**
6. **No escape syntax for now unless another issue requires it**

This is the smallest complete fix and is easy for implementers to test.

---

## Acceptance Criteria

The remediation is complete when the spec makes all of the following unambiguous:

- `command_template` substitution is single-pass
- substitution is performed against the original template, not repeatedly against the output
- `${prompt}` inside `--prompt` does not recurse
- the resolved command for the adversarial example is exactly `debug the ${prompt} handler`
- unknown placeholders STOP with an error
- any escaping decision is explicit, even if the answer is "none defined"

---

## Implementation Test Cases To Derive From Spec

1. **Basic substitution**
   - template: `${prompt}`
   - prompt: `/sc:brainstorm solve this`
   - result: `/sc:brainstorm solve this`

2. **Literal sentinel inside prompt**
   - template: `${prompt}`
   - prompt: `debug the ${prompt} handler`
   - result: `debug the ${prompt} handler`

3. **No second pass**
   - template: `prefix ${prompt} suffix`
   - prompt: `contains ${prompt}`
   - result: `prefix contains ${prompt} suffix`

4. **Missing required prompt**
   - template uses `${prompt}`
   - no `--prompt`
   - result: STOP with missing-value error

5. **Unknown placeholder**
   - template: `${unknown}`
   - result: STOP with unknown-placeholder error

6. **If escaping is adopted**
   - template: `\${prompt} ${prompt}`
   - prompt: `run`
   - result: `${prompt} run`

---

## Files to Modify

- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-spawn-protocol/SKILL.md` if/when the implementation spec is materialized from the backlog spec
- `/config/workspace/IronClaude/src/superclaude/skills/sc-spawn-protocol/refs/dependency-graph.md` only if placeholder expansion rules are centralized there


---

# M5: Retry-once vs MAX_CONCURRENT Batch Conflict — Remediation Proposal

## Problem

When a topological level dispatches a full batch of `MAX_CONCURRENT = 10` tasks, the current spec says failed tasks retry once but does not define how that retry interacts with the hard concurrency cap.

This creates an ambiguity:
- If a failed task retries immediately, the system may exceed the cap or consume a slot that was not explicitly reserved.
- If multiple tasks fail in the same full batch, later failures may have no retry slot available.
- The scheduler behavior becomes timing-dependent, which makes execution nondeterministic and harder to reason about.

## Design Decision

**Retries MUST NOT execute immediately when the original batch is still in flight.**

Instead:
1. A full sub-group dispatches up to 10 tasks.
2. Any task that fails on its first attempt is marked `retry_pending`.
3. The orchestrator continues waiting until **all first-attempt tasks in that dispatched sub-group reach a terminal attempt-1 state**:
   - `completed`
   - `failed_retry_pending`
   - `manual` / `timed_out_no_retry` if some other policy makes retry inapplicable
4. Only after the sub-group’s initial pass is fully drained does the orchestrator open a **retry pass** for that same sub-group.
5. Retry tasks run **within the same `MAX_CONCURRENT = 10` cap**.
6. The next sub-group at the same topological level does **not** begin until both the initial pass and retry pass for the current sub-group are complete.

This makes retry scheduling deterministic and keeps concurrency accounting simple: **attempts and retries use the same capped execution window, but never overlap within a sub-group.**

---

## Step-by-Step Execution Model

### Step 1: Split topological level into capped sub-groups

For any topological level:
- If task count `N <= 10`, there is one sub-group.
- If `N > 10`, split into sequential sub-groups of at most 10 tasks each.

Example:
- 23 ready tasks → sub-group A (10), sub-group B (10), sub-group C (3)

### Step 2: Run the sub-group initial pass

For the active sub-group:
- Dispatch all tasks in the sub-group, up to 10 concurrent.
- No retry is dispatched while any first-attempt task from that sub-group is still running.

Task outcomes during initial pass:
- Success → mark `completed`
- First failure eligible for retry → mark `retry_pending`
- Failure not eligible for retry → mark terminal failure state

### Step 3: Drain initial pass before any retry starts

The sub-group initial pass is considered complete only when every task in that sub-group has finished its first attempt.

This is the critical rule that resolves M5:
- A first-attempt failure does **not** immediately consume a new slot.
- The failed task simply joins a retry queue for that sub-group.
- Additional first-attempt failures in the same sub-group also join that retry queue.

So if 3 of 10 tasks fail, the retry queue becomes `[t2, t7, t9]`, but none retries until the other 7 first-attempt executions have finished.

### Step 4: Open a retry pass for the same sub-group

Once the initial pass is fully drained:
- Collect all `retry_pending` tasks from that sub-group.
- Dispatch them as a retry pass, still under the same concurrency cap of 10.

Because only retry-eligible failures are in the retry pass, the retry pass size is always `<= 10`.

Examples:
- 1 failed task → retry pass of 1
- 4 failed tasks → retry pass of 4
- 10 failed tasks → retry pass of 10

### Step 5: Do not retry a retry

Each task gets at most one retry.

Retry-pass outcomes:
- Retry success → mark `completed`
- Retry failure → mark terminal `failed`
- Retry timeout under timeout policy → mark terminal per timeout policy (`manual` or `failed`)

A retry failure never creates another queue entry.

### Step 6: Advance only after sub-group fully settles

A sub-group is complete only when:
- all initial-pass tasks have finished, and
- all retry-pass tasks have finished

Only then may the orchestrator:
- start the next sub-group in the same topological level, or
- if none remain, advance to the next topological level

---

## Retry Slot Management

## Core Rule

**There is no permanently reserved retry slot.**

Instead, retry capacity is created by **phase separation**:
- Initial-pass tasks use up to 10 slots
- After initial pass drains, those same slots are reused for retry-pass tasks

This is preferable to a 9+1 reservation model because:
1. It preserves full throughput for the common case where no task fails.
2. It handles multiple failures naturally.
3. It avoids waste from an idle reserved retry slot.
4. It eliminates timing races around “which failure gets the reserve slot.”

## Scheduler Invariant

At all times within a sub-group:

`running_initial_attempts + running_retries <= MAX_CONCURRENT`

And additionally:
- if any `running_initial_attempts > 0`, then `running_retries = 0`
- retries may run only after `running_initial_attempts = 0` for that sub-group

In plain language: **initial attempts and retries never overlap inside the same sub-group.**

---

## Exact Ordering Rules

The spec should define the following precise ordering:

1. Determine ready tasks for current topological level.
2. Partition into sub-groups of at most 10.
3. For each sub-group, in order:
   1. Dispatch all tasks in initial pass.
   2. Wait until all initial-pass tasks finish.
   3. Build retry queue from first-attempt failures eligible for retry.
   4. If retry queue is non-empty, dispatch retry pass under same cap.
   5. Wait until all retries finish.
   6. Mark sub-group complete.
4. After all sub-groups in the topological level complete, advance to the next topological level.

This means:
- retries happen **after batch completion**, not during batch execution
- retries for sub-group A finish before sub-group B starts
- later topological levels never start while retries from an earlier level remain unresolved

---

## Concrete Example

### Scenario

- `MAX_CONCURRENT = 10`
- Topological level L has exactly 10 tasks: `T1..T10`
- `T3` and `T8` fail on first attempt

### Correct behavior

#### Initial pass
- Dispatch `T1..T10`
- `T3` fails → mark `retry_pending`
- `T8` fails → mark `retry_pending`
- Remaining tasks continue to completion
- No retry starts yet

#### Retry pass
- Initial pass is now drained
- Retry queue = `[T3, T8]`
- Dispatch retry of `T3` and `T8`
- If `T3` succeeds, mark completed
- If `T8` fails again, mark terminal failed

#### Advancement
- Sub-group completes only after `T3` and `T8` retry pass settles
- Only then may the scheduler move to the next sub-group or topological level

### Why this solves M5

At no point does the system need an 11th slot.
At no point does one failed task block another failed task from receiving its retry.
The retry queue can hold multiple failed tasks without violating concurrency.

---

## Manifest / Status Model

To make this behavior explicit, add attempt-aware states or fields.

Recommended per-task fields:

```json
{
  "id": "task_7",
  "status": "pending|running|completed|retry_pending|failed|manual",
  "attempt": 1,
  "max_attempts": 2,
  "first_error": "message|null",
  "final_error": "message|null"
}
```

Recommended sub-group runtime bookkeeping:
- `initial_pass_total`
- `initial_pass_completed`
- `retry_queue_count`
- `retry_pass_completed`

Minimum semantic requirements:
- first-attempt failures that will be retried must be distinguishable from terminal failures
- manifest should show that a task is waiting for retry, not silently stuck

---

## Normative Spec Text

Use language like this in the Spawn V2 spec:

### Retry Scheduling

- A task that fails on its first attempt and is eligible for retry MUST be marked `retry_pending`.
- A retry MUST NOT be dispatched while any first-attempt task in the same dispatched sub-group is still running.
- After all first-attempt tasks in the sub-group complete, the orchestrator MUST execute a retry pass containing all `retry_pending` tasks from that sub-group.
- Retry passes MUST execute under the same `MAX_CONCURRENT = 10` limit as initial dispatches.
- A retry failure MUST be terminal unless another policy explicitly overrides it.

### Concurrency Interaction

- The concurrency cap applies to both initial attempts and retries.
- Initial attempts and retries for the same sub-group MUST NOT overlap.
- The next sub-group in the same topological level MUST NOT start until the current sub-group’s retry pass, if any, has completed.
- The next topological level MUST NOT start until all sub-groups and retry passes in the current level have completed.

---

## Rejected Alternative: Reserve 1 Retry Slot

The alternative is to reserve capacity inside the 10-cap, effectively running `9 normal + 1 retry reserve`.

This is weaker than deferred retry because:
- it reduces steady-state throughput even when no failures occur
- it still needs additional policy for multiple simultaneous failures
- it introduces fairness questions about retry ordering
- it complicates batching logic for little benefit

Therefore the recommended approach is:

**Use full-cap initial dispatch, then deferred retry pass after batch drain.**

---

## Final Recommendation

Adopt the following simple rule:

**Retries execute only after the active capped sub-group finishes its first-attempt batch. Failed tasks from that sub-group enter a retry queue, and that queue is drained in a retry pass that reuses the same `MAX_CONCURRENT = 10` slots. No next sub-group or next topological level starts until the retry pass finishes.**

This gives Spawn V2:
- deterministic scheduling
- no cap violations
- support for multiple same-batch failures
- no wasted reserved slot
- clear manifest semantics and easier implementation

## Files to Update

- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec-panel-review.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/remediation/major/M5-retry-batch-conflict.md`


---

# Major Issue M6 Remediation Proposal

## Issue

`refs/decomposition-patterns.md` currently mixes two concerns:
1. Wave 2 decomposition structure and granularity rules
2. Wave 3 task-to-command delegation rules

This violates the SpawnV2 lazy-loading principle because Wave 2 loads delegation information it does not need. The task-to-command mapping is only consumed when preparing delegation behavior in Wave 3.

## Goal

Move the Task-to-Command Mapping Rules out of `refs/decomposition-patterns.md` and into `refs/delegation-matrix.md`, so that:
- Wave 2 loads only decomposition and DAG-shaping guidance
- Wave 3 loads delegation-target selection and prompt-construction guidance together
- each ref cleanly owns one concern

## Proposed Design

### Responsibility split after remediation

#### `refs/decomposition-patterns.md`
Owns only:
- Epic construction rules
- Story granularity by depth
- decomposition-time task shaping rules
- DAG edge rules and parallel grouping constraints

#### `refs/delegation-matrix.md`
Owns only:
- command selection for delegated tasks
- persona and MCP hints by command
- agent selection by delegated command
- prompt construction and dispatch-time enrichment rules

This aligns with the current wave model:
- Wave 2 = decide what tasks exist and how they relate
- Wave 3 = decide how each task is delegated

## Exact Content Changes

---

## 1. Changes to `refs/decomposition-patterns.md`

### A. Remove the entire `## Task-to-Command Mapping Rules` section

Delete this block in full:

```markdown
## Task-to-Command Mapping Rules

Each Task maps to exactly ONE `/sc:*` command. Selection criteria:

| Task Type | Primary Command | Fallback |
|-----------|----------------|----------|
| Schema/model design | `/sc:design --type database` | `/sc:design --type component` |
| API design | `/sc:design --type api` | `/sc:design --type architecture` |
| Architecture decisions | `/sc:design --type architecture` | — |
| Feature implementation | `/sc:implement` | `/sc:build` |
| Bug fix | `/sc:task "fix ..."` | `/sc:troubleshoot` |
| Test creation | `/sc:test` | `/sc:task "test ..."` |
| Documentation | `/sc:document` | — |
| Code cleanup | `/sc:cleanup` | `/sc:improve` |
| Security hardening | `/sc:task --force-strict` | `/sc:analyze --focus security` |
| Infrastructure/DevOps | `/sc:task` with devops persona | `/sc:implement` |
| Research/investigation | `/sc:research` | `/sc:analyze` |
```

### B. Replace it with a decomposition-only task-shaping section

Insert this section in the same location, between `## Story Granularity by Depth` and `## DAG Edge Rules`:

```markdown
## Task Shaping Rules

Wave 2 defines the task hierarchy and dependency structure only.
It does NOT choose the final delegated `/sc:*` command. Command selection
is a Wave 3 concern and lives in `refs/delegation-matrix.md`.

Each Task produced by decomposition MUST include:
- `task_description`: clear unit of work
- `task_type`: normalized category for later delegation
- `target_artifact`: what output the task is expected to produce
- `complexity_hint`: low | medium | high
- `domain`: owning Epic/domain

### Normalized Task Types
Use one of these task types during decomposition:
- `schema_design`
- `api_design`
- `architecture_design`
- `implementation`
- `bug_fix`
- `test_creation`
- `documentation`
- `code_cleanup`
- `security_hardening`
- `infrastructure`
- `research`

These normalized task types are the handoff contract into Wave 3.
Wave 3 resolves them into concrete commands using `refs/delegation-matrix.md`.
```

### C. Keep `## DAG Edge Rules` unchanged

No content move is needed for DAG rules. They are valid Wave 2 logic because they shape dependency structure before delegation.

### D. Expected final structure of `refs/decomposition-patterns.md`

After the change, the file should read structurally like this:

```markdown
# Decomposition Patterns Reference

## Epic Construction Rules
...

## Story Granularity by Depth
...

## Task Shaping Rules
...

## DAG Edge Rules
...
```

### Why this is the right replacement

Wave 2 still needs a way to produce consistent task records. Removing the mapping section entirely without replacement would leave decomposition underspecified. The replacement preserves a clean handoff contract by requiring normalized `task_type` values, while deferring actual command choice until Wave 3.

---

## 2. Changes to `refs/delegation-matrix.md`

### A. Add a new section before `## Agent Selection for Task Dispatch`

Insert this new section immediately after the existing command target tables and before `## Agent Selection for Task Dispatch`:

```markdown
## Task-to-Command Mapping Rules

Wave 3 resolves each decomposed Task into exactly ONE delegated `/sc:*`
command. The input to this mapping is the normalized `task_type` produced
by Wave 2 decomposition.

| Task Type | Primary Command | Fallback |
|-----------|----------------|----------|
| `schema_design` | `/sc:design --type database` | `/sc:design --type component` |
| `api_design` | `/sc:design --type api` | `/sc:design --type architecture` |
| `architecture_design` | `/sc:design --type architecture` | — |
| `implementation` | `/sc:implement` | `/sc:build` |
| `bug_fix` | `/sc:task "fix ..."` | `/sc:troubleshoot` |
| `test_creation` | `/sc:test` | `/sc:task "test ..."` |
| `documentation` | `/sc:document` | — |
| `code_cleanup` | `/sc:cleanup` | `/sc:improve` |
| `security_hardening` | `/sc:task --force-strict` | `/sc:analyze --focus security` |
| `infrastructure` | `/sc:task` with devops persona | `/sc:implement` |
| `research` | `/sc:research` | `/sc:analyze` |

### Resolution Rules
1. Use the Task's normalized `task_type` from Wave 2 as the primary selector.
2. Choose the Primary Command unless the task context clearly requires the fallback.
3. Preserve exactly one delegated command per Task.
4. Do not re-decompose the Task during delegation.
5. If no mapping fits, STOP and report an unmapped `task_type` instead of guessing.
```

### B. Add a bridging note tying command tables to task mapping

Immediately after the existing `## Command Delegation Targets` tables, add this short note if it is not already implicit enough:

```markdown
These command tables describe when each command is appropriate.
The formal Wave 3 selection step is defined in `## Task-to-Command Mapping Rules` below.
```

### C. Expected final structure of `refs/delegation-matrix.md`

After the change, the file should read structurally like this:

```markdown
# Delegation Matrix Reference

## Command Delegation Targets
...

## Task-to-Command Mapping Rules
...

## Agent Selection for Task Dispatch
...

## Prompt Construction Rules
...
```

This keeps all dispatch-time concerns together in one ref.

---

## 3. Required SKILL.md / spec wording updates

The ref move is not fully complete unless the wave instructions are also clarified.

### A. Update Wave 2 wording

Current Wave 2 wording says:

```markdown
3. **Task Assignment**: Each Story becomes one or more Tasks. Each Task
   maps to exactly one `/sc:*` command for delegation.
```

Replace with:

```markdown
3. **Task Assignment**: Each Story becomes one or more Tasks. Each Task
   must include a normalized `task_type` for later command resolution in
   Wave 3 delegation.
```

### B. Update Wave 3 wording

Current Wave 3 already loads `refs/delegation-matrix.md`, but it should explicitly mention command resolution.

Insert this step before Prompt Construction, or merge it into Task Creation:

```markdown
2. **Command Resolution**: For each Task, resolve the normalized
   `task_type` into exactly one delegated `/sc:*` command using the
   task-to-command mapping rules in `refs/delegation-matrix.md`.
```

Then renumber subsequent steps accordingly.

### Why these wording changes matter

Without this wording update, the refs would be corrected but the wave protocol would still describe command selection as a Wave 2 action. That would preserve a conceptual contradiction even after the file move.

---

## 4. Resulting behavior after remediation

### Wave 2 loads only what it needs
Wave 2 uses:
- `refs/decomposition-patterns.md`
- `refs/dependency-graph.md` when needed

Wave 2 outputs:
- Epics
- Stories
- Tasks with normalized `task_type`
- DAG edges
- parallel groups

### Wave 3 loads only what it needs
Wave 3 uses:
- `refs/delegation-matrix.md`

Wave 3 resolves:
- task_type -> delegated command
- persona/MCP hints
- agent type/model hint
- prompt enrichment rules

This cleanly restores lazy-loading alignment.

---

## 5. Benefits

### Fixes the lazy-loading violation
Delegation logic is no longer preloaded during decomposition.

### Improves separation of concerns
- decomposition ref = task structure
- delegation ref = dispatch behavior

### Creates a stronger handoff contract
Normalized `task_type` values make the Wave 2 -> Wave 3 boundary explicit and testable.

### Reduces future drift
If command routing evolves, only `refs/delegation-matrix.md` needs updating.

---

## 6. Risks and mitigation

### Risk 1: Wave 2 becomes too vague after removal
Mitigation: replace the removed mapping with normalized task shaping rules, not a pure deletion.

### Risk 2: Duplicate command-selection logic persists elsewhere
Mitigation: update the wave wording so only Wave 3 is described as resolving commands.

### Risk 3: Task types and mapping table diverge over time
Mitigation: require exact task_type vocabulary in both files and treat unmapped values as STOP conditions.

---

## 7. Acceptance criteria

This remediation is complete when all of the following are true:

- `refs/decomposition-patterns.md` no longer contains a task-to-command mapping table
- `refs/decomposition-patterns.md` contains decomposition-only task shaping rules with normalized `task_type`
- `refs/delegation-matrix.md` contains the task-to-command mapping table
- Wave 2 wording no longer says it selects `/sc:*` commands
- Wave 3 wording explicitly says it resolves `task_type` into one delegated command
- no delegation-target-selection logic remains in Wave 2-only refs

---

## Recommended final verdict

Adopt the move exactly as above.

This is the smallest correct fix because it:
- removes the lazy-loading violation,
- preserves decomposition completeness,
- avoids inventing a new ref,
- and strengthens the Wave 2/Wave 3 contract instead of merely relocating text.


---

# M7 Remediation Proposal — Pipeline Execution Step Numbering

## Issue

The `Pipeline Execution` section in `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md` currently contains duplicate numbering for step `3`:

- `3. DAG Construction`
- `3. Phase Dispatch`

This creates an invalid execution sequence and makes the procedure ambiguous for implementers and reviewers.

## Goal

Restore a single, strictly increasing step sequence for `Pipeline Execution` so the flow reads unambiguously from `1` through `6`.

## Exact Renumbering

The remediation should preserve the existing step names and step content, and only correct the numbering as follows:

1. **Parse**
2. **Expand Dynamic Phases**
3. **DAG Construction**
4. **Phase Dispatch**
5. **Artifact Routing**
6. **Progress & Resume**

## Corrected Pipeline Execution Sequence

### Step 1 — Parse
- Parse inline shorthand or load YAML file
- Validate: no cycles in dependency graph
- Validate: all `depends_on` references exist
- If parse error: STOP with details

### Step 2 — Expand Dynamic Phases
- Before DAG construction
- For each `generate-parallel` phase: expand into N concrete phases from `--agents` list. STOP if `--agents` not provided.
- For each `compare-merge` phase: resolve `depends_on` references to expanded phase IDs (fan-in collection)
- Resolve `inherit` config values from CLI flags (`--depth`, etc.)
- Substitute `${prompt}` from `--prompt` CLI value. STOP if missing.
- Log resolved DAG for debugging (visible in `--dry-run`)

### Step 3 — DAG Construction
- Build execution graph from resolved phases
- Assign auto-IDs to inline phases (`phase_1`, `phase_2`, ...)
- Compute parallel groups from dependency structure
- Apply concurrency cap: `MAX_CONCURRENT = 10` (split oversized groups)
- If `--pipeline-seq`: force all phases into linear chain (one at a time)

### Step 4 — Phase Dispatch
- Execute phases respecting DAG + concurrency cap
- For each phase, construct Task prompt from phase definition
- Use delegation-matrix ref for agent type and model selection
- Dispatch phases in same parallel group concurrently (up to 10)
- Wait for all dependencies before dispatching dependent phases

### Step 5 — Artifact Routing
- Pass outputs between phases
- Each phase writes to `<output_dir>/<phase_id>/`
- Dependent phases receive resolved paths to dependency outputs
- Verify dependency output exists before dispatching consumer

### Step 6 — Progress & Resume
- Write manifest at `<output_dir>/spawn-manifest.json` with phase statuses
- `--pipeline-resume`: Read manifest, skip completed phases, resume from first incomplete phase
- Save checkpoints to Serena memory at phase-group boundaries

## Why This Renumbering Is Correct

- It preserves the existing logical order already implied by the section content.
- `Phase Dispatch` must follow `DAG Construction`, so it must be step `4`, not a second step `3`.
- `Artifact Routing` and `Progress & Resume` are downstream execution concerns and should shift to steps `5` and `6` respectively.
- No semantic redesign is required; this is a numbering correction only.

## Required Spec Change

Update the `Pipeline Execution` block in `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md` so the numbered list reads exactly:

1. **Parse**
2. **Expand Dynamic Phases**
3. **DAG Construction**
4. **Phase Dispatch**
5. **Artifact Routing**
6. **Progress & Resume**

## Acceptance Criteria

- The `Pipeline Execution` section contains exactly six top-level numbered steps.
- Each step number is unique and strictly increasing from `1` to `6`.
- The step names are exactly:
  - `Parse`
  - `Expand Dynamic Phases`
  - `DAG Construction`
  - `Phase Dispatch`
  - `Artifact Routing`
  - `Progress & Resume`
- Only numbering is changed; the existing step body text remains functionally unchanged.
- Reviewers can reference step numbers unambiguously in implementation and remediation work.

## Source References

- Spec section: `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`
- Review note identifying the defect: `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec-panel-review.md`


---

# M8: Artifact Naming Convention Per Phase Type — Complete Proposal

## Problem

The spec defines phase-level directories (`<output_dir>/phases/<phase_id>/`) but does not define a stable contract for what files must exist inside each phase directory. Without a per-phase-type naming convention, downstream phases and external consumers cannot resolve inputs deterministically.

## Proposal Summary

Add a normative artifact naming contract for every concrete phase type. The contract must:

1. Define exactly one primary artifact path for every phase type.
2. Reserve fixed filenames for known supplementary artifacts.
3. Distinguish between files that are guaranteed vs optional.
4. Give consumers a deterministic rule for resolving dependency outputs.
5. Forbid phase implementations from renaming primary artifacts.

## Exact Spec Text to Add

### Artifact Naming Convention

All pipeline phase artifacts MUST be written under:

```text
<output_dir>/phases/<phase_id>/
```

Each phase directory MUST contain exactly one **primary artifact** at a phase-type-specific fixed filename. Consumers resolve dependency outputs by reading the primary artifact for the dependency phase type unless a phase explicitly declares that it needs a named supplementary artifact.

Phase implementations MAY write additional files, but they MUST NOT change or omit the required primary artifact filename for their phase type.

### Primary Artifact Table

| Phase Type | Primary Artifact | Required Supplementary Artifacts | Optional Supplementary Artifacts | Notes |
|---|---|---|---|---|
| `analyze` | `output.md` | None | `notes.md`, `sources.json` | Standard single-document analysis result. |
| `design` | `output.md` | None | `notes.md`, `decision-log.md` | Standard single-document design result. |
| `implement` | `output.md` | None | `changed-files.json`, `notes.md` | `output.md` summarizes implementation work; source code changes occur in-place in the repo and are not copied into the phase directory unless explicitly requested by the phase. |
| `test` | `output.md` | None | `test-results.json`, `notes.md` | `output.md` is the human-readable test summary; structured results may be emitted separately. |
| `review` | `output.md` | None | `findings.json`, `notes.md` | `output.md` is the review report. |
| `deploy` | `output.md` | None | `deployment-log.md`, `deployment-metadata.json` | `output.md` is the deployment summary/report. |
| `generate` | `output.md` | None | `notes.md`, `metadata.json` | `generate` is the concrete expanded form of `generate-parallel`. |
| `compare-merge` | `merged-output.md` | `debate-transcript.md`, `diff-analysis.md`, `base-selection.md`, `merge-log.md` | `refactor-plan.md`, `metadata.json` | `merged-output.md` is the canonical dependency artifact for downstream consumers. |

### Artifact Resolution Rules

1. **Directory rule**: Every concrete phase writes only to `<output_dir>/phases/<phase_id>/` for its owned phase artifacts.
2. **Single primary artifact rule**: Every phase type has exactly one canonical primary artifact filename.
3. **Consumer default rule**: A dependent phase that references another phase without naming a specific artifact MUST consume that phase’s primary artifact.
4. **Filename stability rule**: Primary artifact filenames are fixed by phase type and MUST NOT be customized by user input, prompt text, agent choice, or implementation details.
5. **Existence rule**: A phase is not considered to have produced a consumable output unless its primary artifact exists.
6. **Supplementary artifact rule**: Supplementary artifacts may be used by humans, debugging tools, manifests, or explicitly artifact-aware consumers, but they do not replace the primary artifact.
7. **Unknown extra files rule**: Consumers MUST ignore unrecognized extra files in a phase directory unless explicitly instructed to read them.
8. **Markdown rule**: All required primary and required supplementary artifacts use `.md` filenames unless the spec explicitly defines a structured machine-readable file for that artifact.
9. **Manifest rule**: The pipeline manifest SHOULD record the phase’s `primary_artifact` absolute path and MAY record a list of supplementary artifacts.
10. **Resume rule**: `--pipeline-resume` MUST determine phase output availability using the required primary artifact filename for the phase type.

### Dependency Path Resolution

Consumers resolve dependency paths as follows:

| Dependency Phase Type | Resolved Default Input Path |
|---|---|
| `analyze` | `<output_dir>/phases/<dep_id>/output.md` |
| `design` | `<output_dir>/phases/<dep_id>/output.md` |
| `implement` | `<output_dir>/phases/<dep_id>/output.md` |
| `test` | `<output_dir>/phases/<dep_id>/output.md` |
| `review` | `<output_dir>/phases/<dep_id>/output.md` |
| `deploy` | `<output_dir>/phases/<dep_id>/output.md` |
| `generate` | `<output_dir>/phases/<dep_id>/output.md` |
| `compare-merge` | `<output_dir>/phases/<dep_id>/merged-output.md` |

### Dynamic Phase Rules

#### `generate-parallel`

`generate-parallel` is a YAML expansion directive, not a runtime artifact-producing concrete phase type. After expansion, each generated child phase is of type `generate` and MUST write:

```text
<output_dir>/phases/<generated_phase_id>/output.md
```

If a downstream `compare-merge` phase collects all outputs from a `generate-parallel` expansion, it resolves the set of branch inputs as the `output.md` primary artifact from each expanded `generate` phase.

#### `compare-merge`

A `compare-merge` phase MUST write the following files in its phase directory:

- `merged-output.md` — canonical merged result and primary artifact
- `debate-transcript.md` — adversarial or comparison transcript
- `diff-analysis.md` — structured analysis of branch differences
- `base-selection.md` — rationale for chosen base or synthesis strategy
- `merge-log.md` — merge decisions and notable transformations

A `compare-merge` phase MAY additionally write:

- `refactor-plan.md`
- `metadata.json`

Downstream phases that depend on `compare-merge` without naming a specific artifact MUST consume `merged-output.md`.

### Prohibitions

The spec should state the following explicitly:

- A phase MUST NOT emit its primary content under an arbitrary filename.
- A phase MUST NOT require downstream consumers to inspect directory contents to infer which file is primary.
- A phase MUST NOT use agent-specific or persona-specific primary artifact names.
- A phase MUST NOT overload supplementary artifacts as the only consumable output.

## Why This Convention Is Complete

This convention closes the ambiguity for all concrete phase types currently in scope:

- Static phase types (`analyze`, `design`, `implement`, `test`, `review`, `deploy`) all share the same canonical primary artifact: `output.md`.
- Expanded dynamic generation uses the concrete `generate` type and therefore also resolves to `output.md`.
- Fan-in synthesis uses a distinct primary artifact, `merged-output.md`, because it semantically represents a merged result rather than a simple phase-local report.
- Required compare-merge side artifacts are explicitly named so consumers, manifests, and humans can locate them reliably.

## Recommended Companion Spec Updates

To make the naming convention fully enforceable, also update these sections:

1. **Pipeline Manifest Schema**
   - Extend each phase entry with:
   ```json
   "primary_artifact": "absolute-or-output-dir-relative-path",
   "supplementary_artifacts": ["..."]
   ```

2. **Artifact Routing Section**
   - Replace vague wording like “each phase writes to `<output_dir>/<phase_id>/`” with the exact directory and filename rules above.

3. **Delegation Matrix / Dispatch Rules**
   - State that the dispatcher passes the resolved primary artifact path of each dependency into downstream prompts by default.

4. **Validation / Acceptance Criteria**
   - Add a validation requirement that each completed phase directory contains the correct primary artifact filename for its type.

## Final Recommendation

Adopt the simple invariant:

- **Most phase types write `output.md`.**
- **`compare-merge` writes `merged-output.md` as its primary artifact plus a fixed set of named side artifacts.**

This keeps the contract easy to remember, easy to validate, and deterministic for both routing logic and downstream consumers.


---

# Major Issue M9 — Mode-Discriminated Return Contract

## Problem

The current return contract uses the same top-level schema for both Standard mode and Pipeline mode, but different subsets of fields are meaningful in each mode. The spec currently tells producers to emit `null` for fields that were not reached or cannot be determined, but it does not distinguish between:

1. `null` because the invocation failed before the field could be populated, and
2. `null` because that field is not applicable in the selected execution mode.

This creates an ambiguous consumer contract. Callers cannot safely determine which fields are expected to be populated without separately inferring or re-deriving the invocation mode.

## Why this is a major issue

This ambiguity weakens the core value of a return contract: predictable machine consumption.

Current downstream consumers appear to route primarily on generic fields such as `status`, `convergence_score`, and `merged_output_path` (for example in `/config/workspace/IronClaude/tests/sc-roadmap/integration/test_return_contract_routing.py`), but as Pipeline support expands, consumers will increasingly need to know whether pipeline-only metadata is expected.

Without an explicit discriminator:
- consumers must branch on external knowledge instead of the contract itself,
- validation cannot reliably distinguish malformed output from intentionally inapplicable fields,
- documentation remains underspecified,
- future additions risk deepening the ambiguity.

## Proposed solution

Add an explicit required `mode` field to the return contract and document field population guarantees per mode.

### Required `mode` field

Introduce:

```yaml
mode: "standard" | "pipeline"
```

This field must always be populated, including failure cases.

It is a discriminator, not optional metadata. Consumers should use it as the first branch point when interpreting the contract.

## Revised contract shape

Keep one shared contract family, but make it explicitly mode-discriminated.

### Shared fields

These fields remain available in all modes:

```yaml
return_contract:
  mode: "standard" | "pipeline"
  status: "success" | "partial" | "failed"
  merged_output_path: "<path|null>"
  convergence_score: 0.75
  artifacts_dir: "<path>"
  unresolved_conflicts: 2
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```

### Standard mode fields

Standard mode retains the existing direct-invocation semantics:

```yaml
return_contract:
  mode: "standard"
  status: "success"
  merged_output_path: "<path to merged file>"
  convergence_score: 0.75
  artifacts_dir: "<path to adversarial/ directory>"
  base_variant: "opus:architect"
  unresolved_conflicts: 2
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```

### Pipeline mode fields

Pipeline mode adds explicit pipeline metadata and relaxes expectations for standard-only fields where appropriate:

```yaml
return_contract:
  mode: "pipeline"
  status: "success"
  merged_output_path: "<path to final pipeline output>"
  convergence_score: 0.82
  artifacts_dir: "<path to final phase artifacts or pipeline artifacts root>"
  unresolved_conflicts: 1
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []

  pipeline:
    manifest_path: "<path to manifest.json>"
    phase_count: 3
    phases_succeeded: 3
    phases_failed: 0
    total_agents_spawned: 9
    execution_time_seconds: 142
```

## Population matrix

The documentation should explicitly define which fields are:
- always populated,
- conditionally populated based on execution progress,
- not applicable in a given mode.

Suggested matrix:

| Field | Standard mode | Pipeline mode | Notes |
|---|---|---|---|
| `mode` | always | always | Required discriminator |
| `status` | always | always | Shared status model |
| `merged_output_path` | progress-dependent | progress-dependent | Null only if output not reached |
| `convergence_score` | progress-dependent | progress-dependent | Null only if convergence step not reached |
| `artifacts_dir` | always | always | Should exist from start of execution |
| `unresolved_conflicts` | always | always | Shared consumer-facing signal |
| `fallback_mode` | always | always | Shared execution metadata |
| `failure_stage` | failed only | failed only | Null on non-failure |
| `invocation_method` | always | always | Shared provenance metadata |
| `unaddressed_invariants` | always | always | Empty list if none / skipped |
| `base_variant` | applicable; progress-dependent | not applicable unless explicitly redefined | Do not overload meaning across modes |
| `pipeline.manifest_path` | not applicable | always | Required for pipeline mode |
| `pipeline.phase_count` | not applicable | always | Required for pipeline mode |
| `pipeline.phases_succeeded` | not applicable | always | Required for pipeline mode |
| `pipeline.phases_failed` | not applicable | always | Required for pipeline mode |
| `pipeline.total_agents_spawned` | not applicable | always | Required for pipeline mode |
| `pipeline.execution_time_seconds` | not applicable | always | Required for pipeline mode |

## Critical semantic rule

The contract must define a strict distinction between two concepts:

- `not applicable for this mode`
- `applicable, but unavailable because execution did not reach that stage`

That distinction is what `mode` unlocks.

### Recommended rule set

1. `mode` determines applicability.
2. `null` only means "applicable but not produced yet / not reached / failed before determination".
3. Mode-inapplicable fields should either:
   - live inside a mode-specific nested object, or
   - be explicitly documented as not applicable for that mode.

The cleanest version is to place pipeline-only data under a nested `pipeline` object and avoid flattening pipeline-only fields into the shared top level.

## Recommended structure choice

Use a discriminated-union design in documentation and implementation.

### Option A — Minimal change

Keep the current mostly-flat contract, add `mode`, and document applicability.

Pros:
- lowest implementation churn,
- easiest migration,
- minimal consumer breakage.

Cons:
- top-level namespace stays semantically mixed,
- ambiguous field ownership persists unless docs are extremely precise.

### Option B — Preferred

Add `mode` and group mode-specific fields into nested objects.

Recommended shape:

```yaml
return_contract:
  mode: "standard" | "pipeline"

  common:
    status: "success" | "partial" | "failed"
    merged_output_path: "<path|null>"
    convergence_score: 0.75
    artifacts_dir: "<path>"
    unresolved_conflicts: 2
    fallback_mode: false
    failure_stage: null
    invocation_method: "skill-direct"
    unaddressed_invariants: []

  standard:
    base_variant: "opus:architect"

  pipeline:
    manifest_path: "<path to manifest.json>"
    phase_count: 3
    phases_succeeded: 3
    phases_failed: 0
    total_agents_spawned: 9
    execution_time_seconds: 142
```

Pros:
- applicability becomes structurally obvious,
- schema validation becomes straightforward,
- future mode expansion is cleaner,
- consumers no longer guess from null patterns.

Cons:
- larger breaking change,
- requires consumer migration.

## Recommendation

Implement Option A immediately as the remediation minimum, but document the contract as a discriminated union and reserve Option B as the follow-up hardening path.

That means:
1. add required `mode`,
2. add a field population matrix,
3. explicitly define null semantics,
4. place any new pipeline-only fields under `pipeline`,
5. avoid introducing additional mode-specific top-level fields.

This satisfies the issue with low implementation risk while moving the contract toward a cleaner long-term design.

## Documentation changes required

Update the return-contract spec to include:

### 1. Discriminator requirement

Add a normative statement:

> `mode` is required on every return contract and is the authoritative discriminator for consumer parsing.

### 2. Field applicability table

Document, for every field:
- type,
- whether it is common, standard-only, or pipeline-only,
- whether it is always present, progress-dependent, or failure-dependent,
- what `null` means if allowed.

### 3. Consumer guidance

Document a required parsing order:

1. Read `mode`
2. Validate common fields
3. Validate mode-specific fields for that mode
4. Interpret any `null` values only within that mode's applicability rules

### 4. Producer guidance

Document that producers must never rely on consumers inferring mode from field presence or null patterns.

## Consumer behavior after change

After this remediation, consumers should be able to do:

```text
if contract.mode == "standard":
    parse standard fields
elif contract.mode == "pipeline":
    parse pipeline fields
else:
    treat contract as invalid
```

This is materially better than the current implicit pattern:

```text
if pipeline-looking fields are present or standard-only fields are null in a certain combination:
    guess pipeline
```

## Backward compatibility and migration

### Producer migration

All return-contract producers should start emitting `mode` immediately.

### Consumer migration

Consumers should:
1. prefer `mode` when present,
2. temporarily retain legacy fallback parsing for contracts that predate this change,
3. log or flag legacy contracts that omit `mode`.

### Validation policy

After migration, contract validation should fail if `mode` is missing.

## Test coverage to add

Add contract tests covering:

1. Standard mode success includes `mode: standard`
2. Standard mode failure still includes `mode: standard`
3. Pipeline mode success includes `mode: pipeline`
4. Pipeline mode failure still includes `mode: pipeline`
5. Pipeline-only fields are validated only in pipeline mode
6. Standard-only fields are not required in pipeline mode
7. `null` is accepted only for progress-dependent applicable fields
8. Missing `mode` is rejected by strict validators
9. Legacy contract without `mode` follows temporary compatibility path if needed

## Acceptance criteria

This issue is resolved when:

- the return contract includes a required `mode` discriminator,
- the spec clearly states which fields are populated in Standard vs Pipeline mode,
- `null` semantics are explicitly defined as "applicable but unavailable," not "mode-inapplicable",
- pipeline-only fields are documented as pipeline-only,
- consumers can parse the contract without out-of-band knowledge of invocation mode.

## Final recommendation

Approve a mode-discriminated return contract with a required `mode` field and explicit per-mode population documentation.

This is the smallest change that restores contract clarity, improves machine consumption, and prevents mode inference from leaking into every downstream consumer.

---

# M10: Standard Mode Worked Example — Remediation Proposal

## Problem
The spawn v2 spec explains Standard Mode as a 4-wave protocol, but it does not show what a real decomposition output looks like. Users can see invocation examples, yet implementers still have to guess the concrete shape of:
- domain detection output
- Epic/Story/Task hierarchy
- DAG nodes, edges, and parallel groups
- delegation mapping from Tasks to `/sc:*` commands

This makes the spec harder to implement consistently and harder to validate in tests.

## Step-by-Step Solution

### Step 1: Add a dedicated “Worked Example (Standard Mode)” section to the spec

Insert a new section immediately after `## Standard Mode: 4-Wave Execution Protocol` or after the Standard Mode behavior summary.

Purpose:
- show one end-to-end example from invocation to final hierarchy document
- demonstrate the expected output shape, not just the algorithm
- anchor later test assertions against a concrete reference example

Recommended heading:
```md
## Worked Example — Standard Mode (`/sc:spawn "implement user authentication" --depth normal`)
```

### Step 2: Frame the example as Given / When / Then

Use specification-by-example structure so the example is both readable and testable.

Recommended framing:
```md
Given: `/sc:spawn "implement user authentication" --depth normal`
When: Standard Mode runs through Waves 1-4
Then: spawn produces the following classification, hierarchy, DAG, and delegation map
```

This directly addresses the panel feedback and gives implementers a stable acceptance target.

### Step 3: Include the exact classification header for the example

The worked example should begin with the mandatory machine-readable classification block already defined by the spec.

Recommended example block:
```md
<!-- SC:SPAWN:CLASSIFICATION
strategy: adaptive
depth: normal
domains_detected: 4
estimated_tasks: 8
delegation_mode: active
pipeline_mode: none
-->
```

Rationale:
- `adaptive` is a plausible default for a multi-domain feature
- `normal` matches the user invocation
- `domains_detected: 4` matches the documented auth example
- `estimated_tasks: 8` fits normal-depth granularity without forcing orchestrator escalation (`tasks_created > 8`)
- `pipeline_mode: none` distinguishes Standard Mode from Pipeline Mode

### Step 4: Show the Wave 1 domain detection output explicitly

The example must show what Wave 1 actually discovers before decomposition begins.

Recommended content:
```md
### Wave 1 — Domain Detection

Detected domains:
1. `database`
2. `backend-api`
3. `frontend-ui`
4. `testing`

Domain rationale:
- `database`: user records, credential storage, uniqueness constraints
- `backend-api`: login, logout, session/token handling, auth middleware
- `frontend-ui`: login form, auth state, protected route UX
- `testing`: unit, integration, and end-to-end verification across the auth flow

Cross-domain dependencies identified:
- `database -> backend-api` (backend requires user schema and persistence model)
- `backend-api -> frontend-ui` (frontend depends on auth endpoints/contracts)
- `backend-api -> testing` (integration and e2e tests require runnable auth flow)
- `frontend-ui -> testing` (e2e coverage requires login UI)
```

This makes the transition from analysis to decomposition concrete.

### Step 5: Show the full Epic / Story / Task hierarchy for `--depth normal`

The example should model the exact hierarchy conventions described in the spec:
- one Epic per domain
- 2-5 Stories per Epic for `normal`
- each Task maps to exactly one `/sc:*` command

Recommended worked example:

```md
## Example Output

### Epic 1: DATABASE — Design and implement user schema

**Story 1.1 — Define authentication data model**
- `task_1_1_1`: Design `users` schema with unique email and password-hash fields
  - Command: `/sc:design --type database`
- `task_1_1_2`: Implement migration for `users` table and indexes
  - Command: `/sc:implement`

**Story 1.2 — Define persistence constraints for auth workflows**
- `task_1_2_1`: Add schema support for password reset/session invalidation metadata
  - Command: `/sc:design --type database`

### Epic 2: BACKEND-API — Build authentication endpoints

**Story 2.1 — Implement credential authentication flow**
- `task_2_1_1`: Implement login endpoint and password verification flow
  - Command: `/sc:implement`
- `task_2_1_2`: Implement logout/session invalidation behavior
  - Command: `/sc:implement`

**Story 2.2 — Protect application routes**
- `task_2_2_1`: Add auth middleware/guard for protected endpoints
  - Command: `/sc:implement`

### Epic 3: FRONTEND-UI — Build authentication user experience

**Story 3.1 — Create login interaction surface**
- `task_3_1_1`: Build login form with validation and error states
  - Command: `/sc:build --feature`

**Story 3.2 — Integrate authenticated application state**
- `task_3_2_1`: Wire frontend auth state and protected-route handling
  - Command: `/sc:implement`

### Epic 4: TESTING — Establish authentication coverage

**Story 4.1 — Verify backend auth behavior**
- `task_4_1_1`: Add API/integration tests for login, logout, and access control
  - Command: `/sc:test --coverage`

**Story 4.2 — Verify end-to-end user authentication flow**
- `task_4_2_1`: Add end-to-end test for login success/failure and protected navigation
  - Command: `/sc:test --e2e`
```

This produces 8 Tasks total, which is clean, realistic, and aligned with normal-depth decomposition.

### Step 6: Show the resolved DAG as both edges and parallel groups

The spec already defines nodes, edges, and parallel groups. The worked example should show both representations because they answer different questions:
- edge list explains causality
- parallel groups explain execution scheduling

Recommended DAG section:

```md
### Resolved DAG

#### Nodes
- `task_1_1_1` — Design `users` schema
- `task_1_1_2` — Implement `users` migration and indexes
- `task_1_2_1` — Design reset/session metadata
- `task_2_1_1` — Implement login endpoint
- `task_2_1_2` — Implement logout/session invalidation
- `task_2_2_1` — Add auth middleware/guards
- `task_3_1_1` — Build login form
- `task_3_2_1` — Wire auth state and protected routes
- `task_4_1_1` — Add backend integration tests
- `task_4_2_1` — Add end-to-end auth test

#### Hard dependency edges
- `task_1_1_1 -> task_1_1_2` — migration follows schema design
- `task_1_1_1 -> task_2_1_1` — backend login depends on user schema
- `task_1_2_1 -> task_2_1_2` — logout/session invalidation depends on persistence model
- `task_2_1_1 -> task_2_2_1` — route protection depends on auth flow primitives
- `task_2_1_1 -> task_3_2_1` — frontend auth state depends on backend auth contract
- `task_3_1_1 -> task_3_2_1` — protected-route handling depends on login UI entry point
- `task_2_1_1 -> task_4_1_1` — backend tests require login endpoint
- `task_2_2_1 -> task_4_1_1` — access-control tests require middleware/guards
- `task_3_2_1 -> task_4_2_1` — e2e test requires frontend auth integration
- `task_4_1_1 -> task_4_2_1` — backend verification completes before full e2e validation

#### Parallel groups
- `Group 1`: [`task_1_1_1`, `task_1_2_1`, `task_3_1_1`]
  - Reason: schema design, metadata design, and login-form shell can begin independently
- `Group 2`: [`task_1_1_2`, `task_2_1_1`]
  - Reason: migration and backend login implementation can proceed once core schema is defined
- `Group 3`: [`task_2_1_2`, `task_2_2_1`, `task_3_2_1`]
  - Reason: session invalidation, route protection, and frontend auth wiring depend on backend primitives but are parallel-safe with coordination
- `Group 4`: [`task_4_1_1`]
  - Reason: backend integration tests require completed API behavior
- `Group 5`: [`task_4_2_1`]
  - Reason: end-to-end test depends on completed frontend and backend auth flow
```

Important note: if the spec wants strict consistency between the hierarchy count and DAG node count, the hierarchy above should include 10 Tasks instead of 8. To avoid mismatch, choose one of the following and document it explicitly:
- Option A: keep the hierarchy at 8 Tasks and reduce the DAG node list to those same 8 Tasks
- Option B: keep the richer 10-node DAG and update the classification header to `estimated_tasks: 10`

Recommended choice: **Option B**. It is more concrete and gives a clearer worked example.

### Step 7: Normalize the example to one internally consistent final version

To prevent ambiguity, the final inserted example should use one consistent task count across:
- classification header
- hierarchy
- DAG nodes
- delegation map

Recommended final version:
- `estimated_tasks: 10`
- hierarchy includes all 10 tasks shown above
- DAG node list mirrors the hierarchy exactly

That means the classification header should be:
```md
<!-- SC:SPAWN:CLASSIFICATION
strategy: adaptive
depth: normal
domains_detected: 4
estimated_tasks: 10
delegation_mode: active
pipeline_mode: none
-->
```

### Step 8: Add a compact delegation map table

The example should finish with a delegation map that makes the Task-to-command mapping explicit and testable.

Recommended table:

```md
### Delegation Map

| Task ID | Task | Delegated Command | Why this command |
|---|---|---|---|
| `task_1_1_1` | Design `users` schema | `/sc:design --type database` | Schema and persistence design task |
| `task_1_1_2` | Implement migration and indexes | `/sc:implement` | Concrete code/database change |
| `task_1_2_1` | Design reset/session metadata | `/sc:design --type database` | Persistence design extension |
| `task_2_1_1` | Implement login endpoint | `/sc:implement` | Backend feature implementation |
| `task_2_1_2` | Implement logout/session invalidation | `/sc:implement` | Backend behavior implementation |
| `task_2_2_1` | Add auth middleware/guards | `/sc:implement` | Cross-cutting backend code change |
| `task_3_1_1` | Build login form | `/sc:build --feature` | UI component creation |
| `task_3_2_1` | Wire auth state/protected routes | `/sc:implement` | Frontend integration logic |
| `task_4_1_1` | Add backend integration tests | `/sc:test --coverage` | Verification and regression coverage |
| `task_4_2_1` | Add end-to-end auth test | `/sc:test --e2e` | Full user-flow validation |
```

This gives implementers a precise reference for Wave 3 behavior.

### Step 9: Add one short “Why this example matters” note

Close the section with a brief clarification that the example is illustrative, not prescriptive.

Recommended wording:
```md
Note: This example is illustrative of the expected Standard Mode output shape. Exact domain names, story boundaries, and delegated commands may vary by codebase context, but all compliant outputs must include the same structural elements: classification header, domain detection summary, Epic/Story/Task hierarchy, resolved DAG, parallel groups, and delegation map.
```

This preserves flexibility while still making the output contract concrete.

### Step 10: Use the worked example as a validation fixture

After adding the example, update validation guidance so implementers can test against it.

Recommended acceptance checks:
- Standard Mode example emits the classification header first
- detected domains include `database`, `backend-api`, `frontend-ui`, and `testing`
- hierarchy contains one Epic per domain
- each Task maps to exactly one delegated `/sc:*` command
- DAG includes explicit dependency edges and parallel groups
- task count is consistent across classification, hierarchy, DAG, and delegation map

## Proposed Final Insert for the Spec

```md
## Worked Example — Standard Mode (`/sc:spawn "implement user authentication" --depth normal`)

Given: `/sc:spawn "implement user authentication" --depth normal`
When: Standard Mode runs through Waves 1-4
Then: spawn produces the following classification, hierarchy, DAG, and delegation map

<!-- SC:SPAWN:CLASSIFICATION
strategy: adaptive
depth: normal
domains_detected: 4
estimated_tasks: 10
delegation_mode: active
pipeline_mode: none
-->

### Wave 1 — Domain Detection

Detected domains:
1. `database`
2. `backend-api`
3. `frontend-ui`
4. `testing`

Cross-domain dependencies identified:
- `database -> backend-api`
- `backend-api -> frontend-ui`
- `backend-api -> testing`
- `frontend-ui -> testing`

### Wave 2 — Hierarchy Output

#### Epic 1: DATABASE — Design and implement user schema

**Story 1.1 — Define authentication data model**
- `task_1_1_1`: Design `users` schema with unique email and password-hash fields
  - Command: `/sc:design --type database`
- `task_1_1_2`: Implement migration for `users` table and indexes
  - Command: `/sc:implement`

**Story 1.2 — Define persistence constraints for auth workflows**
- `task_1_2_1`: Add schema support for password reset/session invalidation metadata
  - Command: `/sc:design --type database`

#### Epic 2: BACKEND-API — Build authentication endpoints

**Story 2.1 — Implement credential authentication flow**
- `task_2_1_1`: Implement login endpoint and password verification flow
  - Command: `/sc:implement`
- `task_2_1_2`: Implement logout/session invalidation behavior
  - Command: `/sc:implement`

**Story 2.2 — Protect application routes**
- `task_2_2_1`: Add auth middleware/guard for protected endpoints
  - Command: `/sc:implement`

#### Epic 3: FRONTEND-UI — Build authentication user experience

**Story 3.1 — Create login interaction surface**
- `task_3_1_1`: Build login form with validation and error states
  - Command: `/sc:build --feature`

**Story 3.2 — Integrate authenticated application state**
- `task_3_2_1`: Wire frontend auth state and protected-route handling
  - Command: `/sc:implement`

#### Epic 4: TESTING — Establish authentication coverage

**Story 4.1 — Verify backend auth behavior**
- `task_4_1_1`: Add API/integration tests for login, logout, and access control
  - Command: `/sc:test --coverage`

**Story 4.2 — Verify end-to-end user authentication flow**
- `task_4_2_1`: Add end-to-end test for login success/failure and protected navigation
  - Command: `/sc:test --e2e`

### Wave 2 — Resolved DAG

#### Nodes
- `task_1_1_1`
- `task_1_1_2`
- `task_1_2_1`
- `task_2_1_1`
- `task_2_1_2`
- `task_2_2_1`
- `task_3_1_1`
- `task_3_2_1`
- `task_4_1_1`
- `task_4_2_1`

#### Hard dependency edges
- `task_1_1_1 -> task_1_1_2`
- `task_1_1_1 -> task_2_1_1`
- `task_1_2_1 -> task_2_1_2`
- `task_2_1_1 -> task_2_2_1`
- `task_2_1_1 -> task_3_2_1`
- `task_3_1_1 -> task_3_2_1`
- `task_2_1_1 -> task_4_1_1`
- `task_2_2_1 -> task_4_1_1`
- `task_3_2_1 -> task_4_2_1`
- `task_4_1_1 -> task_4_2_1`

#### Parallel groups
- `Group 1`: [`task_1_1_1`, `task_1_2_1`, `task_3_1_1`]
- `Group 2`: [`task_1_1_2`, `task_2_1_1`]
- `Group 3`: [`task_2_1_2`, `task_2_2_1`, `task_3_2_1`]
- `Group 4`: [`task_4_1_1`]
- `Group 5`: [`task_4_2_1`]

### Wave 3 — Delegation Map

| Task ID | Delegated Command |
|---|---|
| `task_1_1_1` | `/sc:design --type database` |
| `task_1_1_2` | `/sc:implement` |
| `task_1_2_1` | `/sc:design --type database` |
| `task_2_1_1` | `/sc:implement` |
| `task_2_1_2` | `/sc:implement` |
| `task_2_2_1` | `/sc:implement` |
| `task_3_1_1` | `/sc:build --feature` |
| `task_3_2_1` | `/sc:implement` |
| `task_4_1_1` | `/sc:test --coverage` |
| `task_4_2_1` | `/sc:test --e2e` |

Note: This example is illustrative of the expected Standard Mode output shape. Exact domain names, story boundaries, and delegated commands may vary by codebase context, but compliant outputs must preserve the same structural elements.
```

## Files to Modify
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md` — add the worked example section
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec-panel-review.md` — optionally mark M10 addressed after insertion
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/remediation/major/M10-worked-example.md` — this proposal


---

# Major Issue M11 — Distinguish `skipped` from `not started` in pipeline manifests

## Problem

The current pipeline manifest design uses `status: skipped` for at least one failure mode, but it does not record why the phase was skipped.

That creates an ambiguity during `--pipeline-resume`:

1. **Dependency-blocked skip** — the phase was intentionally skipped because an upstream dependency failed.
2. **Not yet started** — the phase was never dispatched because execution halted or had not reached that phase yet.

Those two states require different resume behavior:

- A dependency-blocked phase should become eligible again if its dependency is now repaired/completed.
- A not-yet-started phase should just enter the normal scheduling flow when its turn arrives.

Without a reason field, resume logic cannot tell whether `skipped` means “do not run until dependency state changes” or merely reflects “execution never got here.”

## Root cause

The manifest currently overloads lifecycle state and causal state into a single field.

- **Lifecycle state** answers: what happened to this phase?
- **Causal state** answers: why did this happen?

`status` alone is insufficient because `skipped` is terminal-looking but not semantically self-contained.

## Proposal

Add a new optional manifest field:

```yaml
skipped_reason: <string|null>
```

Use it only when `status: skipped`.

### Recommended schema

For each phase entry:

```yaml
phases:
  phase-id:
    status: pending|running|completed|failed|skipped
    skipped_reason: null|dependency_failed|manual_exclusion|conditional_false|upstream_cancelled
    dependencies:
      - other-phase-id
    artifacts: []
    artifact_checksums: {}
    last_updated: "2026-03-23T12:00:00Z"
```

## Status model

### Keep `pending` as the only representation of “not started”

This is the most important semantic rule.

- `pending` = phase has not started yet
- `running` = phase is currently executing
- `completed` = phase finished successfully
- `failed` = phase ran and failed
- `skipped` = scheduler deliberately decided not to run it for a known reason

That means **not started must never be encoded as `skipped`**.

If a phase has not yet been evaluated by the scheduler, it stays `pending`.

## Allowed `skipped_reason` values

Start narrow. Avoid an open-ended free-text field as the only source of truth.

Recommended initial enum:

- `dependency_failed`
  - One or more required upstream phases failed, so this phase could not run.
- `upstream_cancelled`
  - One or more upstream phases were cancelled/aborted, so this phase could not run.
- `manual_exclusion`
  - Operator or configuration explicitly excluded this phase.
- `conditional_false`
  - Phase was valid in the graph, but runtime conditions evaluated false.

For M11 specifically, `dependency_failed` is the critical value.

### Optional companion detail field

If the implementation wants richer debugging without weakening machine semantics, add:

```yaml
skipped_details:
  blocked_by:
    - validate
    - analyze
  message: "Skipped because validate failed"
```

But the core fix should not depend on this. The minimum viable change is still `skipped_reason`.

## Resume semantics

## Rule 1: `pending` phases are normal candidates

On resume, any phase with `status: pending` should be considered not yet attempted.

Behavior:
- Evaluate dependencies normally.
- If dependencies are satisfied, dispatch it.
- If dependencies are still unsatisfied because an upstream phase is incomplete or failed, leave it pending until the scheduler reaches a stable decision point.

## Rule 2: `skipped` + `skipped_reason: dependency_failed` is re-evaluable

On resume, phases previously skipped due to failed dependencies should **not** be treated as permanently skipped.

Behavior:
1. Inspect the current manifest state of dependencies.
2. If blocking dependencies are still failed/not completed, keep the phase skipped.
3. If all required dependencies are now completed, convert the phase back to `pending` and allow dispatch.

This is the core behavioral change needed for M11.

## Rule 3: other skip reasons remain skipped unless explicitly invalidated

Examples:
- `manual_exclusion` should remain skipped on resume.
- `conditional_false` should remain skipped unless the condition is explicitly recomputed and now true.

This prevents resume from unexpectedly reviving phases that were intentionally suppressed.

## Proposed resume algorithm

### Phase 1 — Load and normalize manifest

When `--pipeline-resume` starts:

1. Read the manifest.
2. For each phase:
   - If `status == skipped` and `skipped_reason` is absent, treat it as legacy data.
   - If `status == skipped` and `skipped_reason == dependency_failed`, mark it as re-evaluable.
   - If `status == pending`, treat it as not started.

### Phase 2 — Backward-compatibility normalization

To avoid breaking existing manifests:

- Legacy manifest with `status: skipped` and no `skipped_reason` should be interpreted conservatively.

Recommended policy:
1. If all dependencies are currently completed, downgrade legacy `skipped` to `pending`.
2. Otherwise leave it as `skipped` and annotate in memory/logging that the reason was inferred as dependency-related/unknown.

Alternative stricter policy:
- Require operator acknowledgement for legacy ambiguous entries.

Recommendation: use the first policy because it preserves resumability and minimizes operator friction.

### Phase 3 — Recompute eligibility

For every non-completed phase:

1. If `status == failed`, keep it eligible for retry according to existing retry/resume policy.
2. If `status == pending`, evaluate dependency satisfaction.
3. If `status == skipped` and `skipped_reason == dependency_failed`, re-check dependencies.
4. If dependencies are now satisfied, set:

```yaml
status: pending
skipped_reason: null
```

Then include the phase in the dispatchable set.

### Phase 4 — Dispatch by topological order

Run the normal scheduler over:
- all `pending` phases whose dependencies are satisfied
- any reactivated formerly-skipped phases

This keeps resume behavior aligned with fresh-run scheduling instead of inventing a second execution model.

## Write-time manifest rules

The scheduler should update the manifest with stricter invariants.

### When a phase is first created in the manifest

Set:

```yaml
status: pending
skipped_reason: null
```

### When a phase is skipped because dependency failed

Set:

```yaml
status: skipped
skipped_reason: dependency_failed
```

Optionally include which dependency blocked it.

### When a phase is dispatched

Set:

```yaml
status: running
skipped_reason: null
```

### When a phase completes successfully

Set:

```yaml
status: completed
skipped_reason: null
```

### When a phase fails during execution

Set:

```yaml
status: failed
skipped_reason: null
```

## Invariants

The implementation should enforce these invariants:

1. `status != skipped` => `skipped_reason == null`
2. `status == skipped` => `skipped_reason != null`
3. `pending` means no execution attempt has started
4. `completed` means artifact validation/checksum requirements passed
5. `skipped_reason: dependency_failed` means at least one dependency was non-completed at scheduling time

These invariants make the manifest machine-interpretable and testable.

## Why this is the right fix

This proposal is intentionally minimal.

It does not require:
- redesigning the scheduler
- inventing a separate resume-only state machine
- changing artifact checksum behavior
- changing topological execution rules

It only separates:
- **state** (`status`)
- **cause** (`skipped_reason`)

That is enough to make resume correct.

## Example scenarios

### Scenario A — Dependency failed, then later fixed

Initial run:

```yaml
phases:
  A:
    status: failed
    skipped_reason: null
  B:
    status: skipped
    skipped_reason: dependency_failed
    dependencies: [A]
```

Later, operator fixes A or reruns A and it becomes completed:

```yaml
phases:
  A:
    status: completed
    skipped_reason: null
  B:
    status: skipped
    skipped_reason: dependency_failed
    dependencies: [A]
```

On `--pipeline-resume`:
- Resume logic sees B was skipped because of dependency failure.
- It re-checks A.
- A is now completed.
- B is reset to `pending` and dispatched.

### Scenario B — Phase never reached

Initial run stopped early:

```yaml
phases:
  A:
    status: completed
  B:
    status: pending
  C:
    status: pending
```

On resume:
- B and C are simply normal pending phases.
- No special skip logic applies.

### Scenario C — Manual exclusion

```yaml
phases:
  security-review:
    status: skipped
    skipped_reason: manual_exclusion
```

On resume:
- It remains skipped.
- Resume does not silently reactivate it.

## Implementation steps

### 1. Extend manifest schema

Update the pipeline manifest schema/documentation so each phase entry supports:
- `status`
- `skipped_reason`

Document that `pending` is the only valid “not started” state.

### 2. Update manifest writers

Wherever the executor/scheduler marks downstream phases as skipped after dependency failure, write:

```yaml
status: skipped
skipped_reason: dependency_failed
```

Wherever phase entries are initialized, write:

```yaml
status: pending
skipped_reason: null
```

### 3. Update resume loader

When reading the manifest during `--pipeline-resume`:
- recognize `skipped_reason`
- treat `skipped/dependency_failed` as re-evaluable
- convert re-satisfied skipped phases back to `pending`

### 4. Add backward-compatibility handling

For old manifests without `skipped_reason`:
- detect ambiguous `skipped`
- infer eligibility conservatively
- write back normalized entries when safe

### 5. Improve operator visibility

Log decisions like:
- `phase B remains skipped: dependency A still failed`
- `phase B reactivated from skipped -> pending: dependency A now completed`
- `phase C remains skipped: manual_exclusion`

This makes resume behavior explainable.

## Test plan

### Unit tests

1. **Schema round-trip**
   - Manifest with `skipped_reason` serializes/deserializes correctly.

2. **Invariant enforcement**
   - `status=skipped` with null reason is rejected or normalized.
   - non-skipped status with non-null reason is rejected or normalized.

3. **Legacy manifest compatibility**
   - Old manifest lacking `skipped_reason` can still load.

### Resume behavior tests

4. **Pending starts normally**
   - `pending` phase with completed dependencies is dispatched on resume.

5. **Dependency-failed skip reactivates**
   - Phase skipped with `dependency_failed` becomes `pending` once dependencies are completed.

6. **Dependency-failed skip stays skipped when blocker remains**
   - If upstream phase is still failed, the skipped phase is not dispatched.

7. **Manual exclusion stays skipped**
   - `manual_exclusion` never auto-reactivates on resume.

8. **Mixed graph resume**
   - Completed phases remain skipped from execution.
   - Pending phases dispatch normally.
   - Reactivated skipped phases enter dispatch set only after dependencies are satisfied.

### Integration test

9. **End-to-end interrupted pipeline**
   - Run a graph where upstream phase fails.
   - Confirm downstream is written as `skipped + dependency_failed`.
   - Manually repair or update upstream manifest/state to completed.
   - Resume.
   - Confirm downstream phase is dispatched and eventually completed.

## Risks and mitigations

### Risk: legacy manifests remain ambiguous

Mitigation:
- add compatibility normalization on load
- emit clear logs when inference occurs

### Risk: too many skip reasons too early

Mitigation:
- start with a small enum
- only make `dependency_failed` special in resume logic initially

### Risk: scheduler writes inconsistent combinations

Mitigation:
- centralize manifest updates behind helper functions rather than ad hoc writes
- validate invariants before persisting

## Recommended acceptance criteria

1. Manifest schema includes `skipped_reason` for phase entries.
2. `pending` is the sole representation of “not started.”
3. Downstream phases skipped because an upstream dependency failed are persisted as:
   - `status: skipped`
   - `skipped_reason: dependency_failed`
4. On `--pipeline-resume`, a phase with `status: skipped` and `skipped_reason: dependency_failed` is re-evaluated against current dependency state.
5. If all blocking dependencies are now `completed`, that phase is reset to `pending` and becomes eligible for dispatch.
6. Phases skipped for other reasons do not auto-reactivate.
7. Legacy manifests without `skipped_reason` still resume without crashing.
8. Tests cover both dependency-blocked skip and genuine not-started cases.

## Final recommendation

Implement M11 as a schema-and-resume correction, not as a broad scheduler redesign.

The cleanest solution is:

- keep `pending` for not started
- keep `skipped` for deliberate scheduler decisions
- add `skipped_reason` to explain why skipping happened
- teach `--pipeline-resume` that `skipped + dependency_failed` is a re-checkable state, not a permanent terminal state

That change is small, explicit, backward-compatible, and directly solves the ambiguity called out in M11.


---

# M12 Remediation Proposal — Expanded Validation Matrix for `/sc:spawn`

## Goal

Replace the current 2-item manual checklist with a validation matrix that exercises the command surface area implied by the spec: Standard Mode, Pipeline Mode, BranchNMerge dynamic expansion, error handling, and resume behavior.

## Validation Scope

This matrix covers:
- Standard Mode flags: `--dry-run`, `--no-delegate`, `--strategy`, `--depth`, `--resume`
- Pipeline Mode flags: `--pipeline`, `--pipeline-seq`, `--pipeline-resume`, `--prompt`, `--agents`
- Dynamic phase types: `generate-parallel`, `compare-merge`
- Error paths called out in review findings and boundary analysis
- Resume behavior for both Serena checkpoints and pipeline manifests

## Assumptions / Test Fixtures

Use the following test assets during manual validation:
- A small repo or sandbox task that is safe to plan against
- A valid linear pipeline YAML fixture
- A valid BranchNMerge YAML fixture
- An invalid cyclic pipeline YAML fixture
- A writable output directory for manifests/artifacts
- A prior interrupted run for resume scenarios

Where the spec is still ambiguous, pass criteria below are written to force the intended contract to become explicit.

---

## Expanded Validation Matrix

### Standard Mode

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| S01 | Standard dry-run baseline | `/sc:spawn "audit auth flow" --dry-run` | Enters Standard Mode, performs decomposition/planning preview, does not create tasks or delegate work. | Output clearly shows preview/plan-only behavior; no spawned tasks; no side effects beyond preview artifacts/logging. |
| S02 | Plan-only without delegation | `/sc:spawn "audit auth flow" --no-delegate` | Produces hierarchy/plan in Standard Mode without delegating to sub-agents. | Task hierarchy is produced; no delegation occurs; result is explicitly marked as plan-only. |
| S03 | Dry-run plus no-delegate | `/sc:spawn "audit auth flow" --dry-run --no-delegate` | Safest preview path; should show decomposition intent without execution. | No task creation, no delegation, and no execution side effects; output reflects combined preview semantics without contradiction. |
| S04 | Strategy override: wave | `/sc:spawn "migrate legacy auth" --strategy wave --dry-run` | Uses wave coordination path instead of adaptive default. | Output/preview explicitly reflects wave-based grouping or staged orchestration rather than default adaptive behavior. |
| S05 | Depth shallow | `/sc:spawn "stabilize CI pipeline" --depth shallow --dry-run` | Produces coarse decomposition with limited granularity. | Preview shows fewer/larger work units than deep mode; no evidence of deep decomposition detail. |
| S06 | Depth deep | `/sc:spawn "stabilize CI pipeline" --depth deep --dry-run` | Produces more granular decomposition and richer planning detail. | Preview is materially more detailed than shallow mode; deeper hierarchy or more phases/tasks are visible. |
| S07 | Resume from Serena checkpoint | `/sc:spawn "continue migration" --resume` | Reads saved checkpoint and resumes from last incomplete Standard-Mode boundary. | Prior completed work is not re-run; resumed output identifies continuation point; resumed plan/execution proceeds from first incomplete checkpointed stage. |
| S08 | Both task description and pipeline provided | `/sc:spawn "legacy text prompt" --pipeline "analyze -> test" --dry-run` | Must follow the defined precedence rule: pipeline mode wins, and task description is either ignored or treated as prompt per remediation decision. | Behavior is deterministic and documented in output; no ambiguous mixed-mode execution; the precedence rule is observable and repeatable. |

### Pipeline Mode

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| P01 | Inline pipeline shorthand baseline | `/sc:spawn --pipeline "analyze -> design | implement -> test" --dry-run` | Parses inline DAG correctly, preserving serial and parallel relationships. | Preview shows analyze first, design+implement parallel second, test last; no parse errors. |
| P02 | Pipeline from YAML file | `/sc:spawn --pipeline @/ABS/PATH/pipeline-valid.yaml --dry-run` | Loads DAG from YAML and previews executable phases. | YAML is accepted; phases and dependencies match fixture definition; preview is structurally correct. |
| P03 | Force sequential pipeline execution | `/sc:spawn --pipeline "analyze -> design | implement -> test" --pipeline-seq --dry-run` | Converts or schedules the pipeline as sequential execution despite parallel-capable structure. | Preview/execution order shows no parallel dispatch; all phases are serialized deterministically. |
| P04 | Pipeline prompt injection | `/sc:spawn --pipeline "analyze -> test" --prompt "Focus on auth regressions" --dry-run` | Prompt text is propagated to pipeline phases according to spec. | Preview or generated phase commands visibly include the supplied prompt exactly once in the intended place. |
| P05 | Pipeline resume from manifest | `/sc:spawn --pipeline @/ABS/PATH/pipeline-valid.yaml --pipeline-resume` | Reads manifest, skips completed phases, resumes from first incomplete phase. | Manifest is loaded; completed phases are skipped rather than repeated; resumed phase is the first incomplete one. |
| P06 | Pipeline YAML with parallel fan-out and join | `/sc:spawn --pipeline @/ABS/PATH/pipeline-parallel-join.yaml --dry-run` | Preserves many-to-one dependency structure through preview. | Output shows fan-out phases blocked on the predecessor and join phase blocked on all required inputs. |

### BranchNMerge / Dynamic Expansion

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| B01 | BranchNMerge with 2 agents | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents opus:architect,haiku:analyzer --prompt "compare remediation options" --dry-run` | Expands `generate-parallel` into 2 concrete agent phases, then routes outputs to merge. | Preview shows exactly 2 generated phases; downstream compare/merge phase expects 2 artifacts. |
| B02 | BranchNMerge with 3 agents | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents opus:architect,sonnet:backend,haiku:qa --prompt "compare remediation options" --dry-run` | Expands to 3 concrete agent branches and one merge path. | Preview shows exactly 3 generated phases; merge stage consumes all 3 outputs. |
| B03 | BranchNMerge with 10+ agents / batching | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents a1:architect,a2:architect,a3:architect,a4:architect,a5:architect,a6:architect,a7:architect,a8:architect,a9:architect,a10:architect,a11:architect --prompt "stress test fanout" --dry-run` | Applies concurrency cap behavior to oversized parallel group. | Preview or execution plan shows sub-batching/splitting at the defined cap instead of a single oversubscribed dispatch group. |
| B04 | Agent spec with persona and instruction | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents 'opus:architect:"focus on migration risk"',haiku:qa --prompt "compare remediation options" --dry-run` | Parser accepts full `model[:persona[:"instruction"]]` shape and preserves embedded instruction. | Expanded branch definition preserves model, persona, and custom instruction without mangling quotes or truncating fields. |
| B05 | Compare-merge artifact routing | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents opus:architect,haiku:analyzer,sonnet:backend --prompt "merge best plan"` | Collects branch outputs and runs merge/comparison stage with all expected artifacts surfaced or locatable. | Merge completes; merged output path is exposed; supplementary artifacts are discoverable via manifest/output directory contract. |

### Error Paths

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| E01 | Missing task description in Standard Mode | `/sc:spawn --dry-run` | Stops immediately because neither task description nor pipeline was provided. | Command fails fast with explicit actionable error; no planning, no task creation, no hidden default behavior. |
| E02 | Invalid empty `--agents` value | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents "" --prompt "x" --dry-run` | Rejects empty parsed agent set rather than continuing with zero branches. | Clear validation error states that at least one valid agent spec is required; no phase expansion occurs. |
| E03 | Invalid malformed agent spec | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents "not:a:valid:spec:extra" --prompt "x" --dry-run` | Rejects malformed agent grammar. | Error message identifies invalid spec format and points to accepted grammar; no partial execution. |
| E04 | Missing `--agents` for generate-parallel pipeline | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --prompt "x" --dry-run` | Stops because dynamic parallel generation lacks required agent definitions. | Clear validation error mentions missing `--agents`; no fallback to empty/default agent list. |
| E05 | Cyclic YAML pipeline | `/sc:spawn --pipeline @/ABS/PATH/pipeline-cycle.yaml --dry-run` | Detects cycle and refuses execution. | Cycle is detected before dispatch; error identifies dependency cycle or invalid DAG; nothing runs. |
| E06 | Compare-merge with fewer than 2 artifacts | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents haiku:analyzer --prompt "x" --dry-run` | Expansion may produce one branch, but compare/merge must stop because merge requires at least 2 inputs. | Validation/preflight clearly states merge requires >=2 artifacts; no invalid merge stage execution. |
| E07 | Missing pipeline file | `/sc:spawn --pipeline @/ABS/PATH/does-not-exist.yaml --dry-run` | Fails with file resolution/loading error. | Error explicitly names missing file path; no fallback or misleading parse failure. |

### Resume / Recovery

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| R01 | Standard resume after interrupted run | Step 1: run a long Standard Mode orchestration and interrupt after checkpoint. Step 2: `/sc:spawn "continue migration" --resume` | Resumes Standard Mode from latest checkpoint boundary without redoing completed work. | Previously completed wave/group is not repeated; resumed output references recovered checkpoint state. |
| R02 | Pipeline resume after partial completion | Step 1: run pipeline until one later phase remains incomplete. Step 2: `/sc:spawn --pipeline @/ABS/PATH/pipeline-valid.yaml --pipeline-resume` | Loads manifest and restarts from first incomplete phase only. | Completed phases remain marked completed; only pending/failed incomplete work is re-entered. |
| R03 | Resume with no checkpoint available | `/sc:spawn "continue migration" --resume` in a clean environment | Fails cleanly or reports that no resumable checkpoint exists. | User receives explicit "no checkpoint/manifest found" guidance; command does not invent state or silently start a fresh unrelated run. |
| R04 | Resume preserves output/manifest continuity | Resume a previously interrupted pipeline run using the same output location. | Resumed run appends/updates the existing manifest rather than replacing history incoherently. | Manifest remains internally consistent, phase statuses are preserved, and new completion timestamps/results continue the same pipeline record. |

---

## Recommended Replacement Checklist Text

Replace the current migration checklist validation section with a requirement like:

- [ ] Execute and record the M12 validation matrix covering Standard Mode, Pipeline Mode, BranchNMerge, error handling, and resume behavior (minimum 20 scenarios: S01-S08, P01-P06, B01-B05, E01-E07, R01-R04 as applicable to implemented scope)
- [ ] Confirm every flag in the options table is exercised by at least one validation scenario
- [ ] Confirm every documented STOP/error condition is exercised by at least one negative-path scenario
- [ ] Confirm both resume mechanisms (`--resume`, `--pipeline-resume`) are validated against real interrupted state

## Coverage Crosswalk

| Surface area | Covered by |
|---|---|
| `--dry-run` | S01, S03, S04, S05, S06, P01, P02, P03, P04, B01, B02, B03, E01-E07 |
| `--no-delegate` | S02, S03 |
| `--strategy` | S04 |
| `--depth` | S05, S06, B01-B03 |
| `--resume` | S07, R01, R03 |
| `--pipeline` | S08, P01-P06, B01-B05, E02-E07, R02, R04 |
| `--agents` | B01-B05, E02-E04, E06 |
| `--prompt` | P04, B01-B05, E02-E06 |
| `--pipeline-seq` | P03 |
| `--pipeline-resume` | P05, R02, R04 |
| Standard Mode | S01-S08 |
| Pipeline Mode | P01-P06 |
| BranchNMerge | B01-B05 |
| Error handling | E01-E07 |
| Resume/recovery | R01-R04 |

## Exit Criteria

M12 should be considered resolved only when:
1. The migration checklist references an expanded validation matrix, not 2 ad hoc commands.
2. The implemented/manual test evidence demonstrates coverage across all major execution families.
3. At least one scenario validates each documented flag and each documented failure boundary.
4. Resume behavior is validated using real interrupted state, not only dry-run previews.
5. BranchNMerge is validated at normal scale and concurrency-cap scale.


---

# M13 Remediation Proposal — Surface Adversarial Artifact Directory in Spawn Return Contract

## Issue

In `/sc:spawn` Pipeline Mode, the `compare-merge` phase delegates to `/sc:adversarial --compare`.

That downstream command produces a multi-artifact output set:
- `diff-analysis.md`
- `debate-transcript.md`
- `base-selection.md`
- `refactor-plan.md`
- `merge-log.md`
- `merged-output.md`

But the current `/sc:spawn` return contract only exposes:
- high-level orchestration fields, and
- `pipeline_manifest` for Pipeline Mode

This creates a visibility gap:
- consumers can reliably find the manifest,
- but they cannot reliably discover the full adversarial output bundle from the return contract itself,
- unless they already know the internal phase output layout and then traverse from `pipeline_manifest` to the relevant `compare-merge` phase `output_dir`.

That is the exact divergence called out in the panel review: one fan-in phase produces one primary output plus five supplementary artifacts, but spawn only advertises a single manifest path.

---

## Why This Is a Real Contract Problem

The current spec already treats Pipeline Mode as artifact-driven:
- each phase writes to `<output_dir>/<phase_id>/`
- the manifest records per-phase `output_dir`
- `compare-merge` is explicitly defined as a wrapper around `/sc:adversarial`

So the data exists.

The problem is discoverability and contract ergonomics.

A caller that wants to:
- inspect the debate transcript,
- review the merge rationale,
- archive all comparison evidence,
- or pass the full adversarial bundle to another command,

currently has to do all of the following:
1. read `pipeline_manifest`
2. parse manifest JSON
3. locate the `compare-merge` phase entry
4. extract `output_dir`
5. know that this directory contains the adversarial artifact set

That is too much hidden coupling for something the spec already knows is a first-class phase type.

---

## Proposed Resolution

Add an `artifacts_dir` field to `/sc:spawn`'s return contract and define it as the canonical entry point to the full adversarial artifact bundle when Pipeline Mode includes a `compare-merge` phase.

### Core rule

- `artifacts_dir` points to the directory containing the full artifact set produced by the most relevant pipeline output bundle.
- For M13 specifically, when the pipeline includes a terminal or consumer-relevant `compare-merge` phase, `artifacts_dir` MUST point to that phase's output directory.
- That directory is where consumers can access:
  - `merged-output.md`
  - `diff-analysis.md`
  - `debate-transcript.md`
  - `base-selection.md`
  - `refactor-plan.md`
  - `merge-log.md`

This preserves `pipeline_manifest` for full pipeline introspection while also giving consumers a direct, zero-guess path to the adversarial bundle.

---

## Why `artifacts_dir` Is Better Than Relying on `pipeline_manifest` Alone

### Option A — Keep current contract, document manifest traversal only
Rejected as the primary fix.

Why:
- It preserves unnecessary indirection.
- It forces every consumer to understand manifest internals.
- It leaks pipeline topology concerns into simple output consumption.
- It makes a common use case harder: “give me the compare-merge evidence bundle.”

This is acceptable as a fallback explanation, but not as the main contract.

### Option B — Add `artifacts_dir` and keep `pipeline_manifest`
Recommended.

Why:
- `pipeline_manifest` remains the full-fidelity orchestration record.
- `artifacts_dir` becomes the ergonomic consumption handle.
- The fix is additive and backward-compatible.
- It matches `/sc:adversarial`'s own return contract, which already exposes `artifacts_dir` directly.

### Option C — Replace `pipeline_manifest` with multiple artifact paths
Rejected.

Why:
- It overfits the contract to one phase type.
- It would bloat the spawn return contract with compare-merge-specific fields.
- A single directory handle is simpler and more extensible.

---

## Normative Behavior

### 1. Return contract addition

Add this field to the `/sc:spawn` return contract:

| Field | Type | Description |
|---|---|---|
| `artifacts_dir` | `string|null` | Canonical directory for the primary output artifact bundle. In Pipeline Mode with `compare-merge`, this is the compare-merge phase output directory containing merged output and supplementary adversarial artifacts. `null` when no such bundle exists. |

### 2. Population rule

#### Standard Mode
- `artifacts_dir = null`
- Reason: Standard Mode produces a task hierarchy and orchestration metadata, not a pipeline artifact bundle.

#### Pipeline Mode without `compare-merge`
- `artifacts_dir = null` by default
- `pipeline_manifest` remains the authoritative source for per-phase outputs.

This keeps the field semantically tight for the M13 problem instead of inventing a vague “some directory” meaning.

#### Pipeline Mode with `compare-merge`
- `artifacts_dir` MUST be set to the resolved output directory of the relevant `compare-merge` phase.
- That directory MUST contain the adversarial bundle.
- Consumers MUST be told to treat this directory as the public access point for the phase’s full output set.

### 3. Relevant phase selection rule

If more than one `compare-merge` phase exists, `/sc:spawn` MUST choose one deterministically.

Recommended rule:
- Use the last successfully completed `compare-merge` phase in topological execution order.

Rationale:
- It is deterministic.
- It usually corresponds to the pipeline’s most downstream merged result.
- It avoids returning a list when the contract only needs one canonical consumer entry point.

If no `compare-merge` phase completed successfully but one produced partial artifacts:
- set `artifacts_dir` to the last `compare-merge` phase that produced an output directory,
- and rely on `status` plus manifest phase status for success/failure interpretation.

This aligns with the adversarial protocol’s own “preserve artifacts on partial/failed runs” pattern.

---

## Consumer Access Model

The spec should explicitly document two supported access patterns.

### Fast path: direct bundle access

Use `artifacts_dir` when the caller wants the final compare-merge output bundle.

Example consumer logic:
1. Read spawn return contract.
2. If `artifacts_dir` is non-null, inspect files in that directory.
3. Use:
   - `merged-output.md` for the final merged deliverable
   - `debate-transcript.md` for adversarial reasoning
   - `merge-log.md` for execution provenance
   - `refactor-plan.md` for manual follow-up or audit

### Full-fidelity path: manifest traversal

Use `pipeline_manifest` when the caller needs:
- all phase outputs,
- non-compare-merge phase directories,
- status of failed/skipped phases,
- or complete pipeline reconstruction.

This cleanly separates:
- `artifacts_dir` = consumer-friendly primary bundle handle
- `pipeline_manifest` = orchestration internals and full graph state

---

## Spec Amendment Text

### A. Update the Return Contract section

In `.dev/releases/backlog/v4.xx-SpawnV2/spec.md`, update `## Return Contract` from:

```md
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` \| `partial` \| `failed` |
| `task_hierarchy_path` | string | Path to written hierarchy document |
| `tasks_created` | int | Number of TaskCreate entries |
| `delegation_map` | object | Task ID → delegated `/sc:*` command |
| `parallel_groups` | list | Groups of tasks safe to run concurrently |
| `completion_summary` | object | Per-task status (completed/failed/manual) |
| `pipeline_manifest` | string\|null | Path to manifest (Pipeline Mode only) |
```

to:

```md
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` \| `partial` \| `failed` |
| `task_hierarchy_path` | string | Path to written hierarchy document |
| `tasks_created` | int | Number of TaskCreate entries |
| `delegation_map` | object | Task ID → delegated `/sc:*` command |
| `parallel_groups` | list | Groups of tasks safe to run concurrently |
| `completion_summary` | object | Per-task status (completed/failed/manual) |
| `pipeline_manifest` | string\|null | Path to manifest (Pipeline Mode only) |
| `artifacts_dir` | string\|null | Canonical directory for the primary artifact bundle. In Pipeline Mode with `compare-merge`, this points to the compare-merge output directory containing `merged-output.md` plus supplementary adversarial artifacts. Otherwise null. |
```

### B. Add a consumer guidance note immediately after the table

```md
**Consumer access rule**:
- Use `artifacts_dir` when you want the final compare-merge artifact bundle directly.
- Use `pipeline_manifest` when you need full pipeline execution detail or need to inspect all phase output directories.

For `compare-merge`, `artifacts_dir` contains:
- `merged-output.md`
- `diff-analysis.md`
- `debate-transcript.md`
- `base-selection.md`
- `refactor-plan.md`
- `merge-log.md`
```

### C. Clarify compare-merge output semantics in Pipeline Execution / Artifact Routing

Add a note near the existing artifact routing rules:

```md
**compare-merge output convention**:
A `compare-merge` phase writes the full adversarial output bundle into its phase output directory. This directory contains:
- `merged-output.md` (primary output)
- `diff-analysis.md`
- `debate-transcript.md`
- `base-selection.md`
- `refactor-plan.md`
- `merge-log.md`

When a Pipeline Mode invocation includes a `compare-merge` phase, `/sc:spawn` SHOULD expose that phase directory as `artifacts_dir` in the return contract.
```

### D. Clarify the manifest relationship

Add one sentence to the manifest schema section or immediately after it:

```md
For phases of type `compare-merge`, the phase `output_dir` recorded in the manifest is the same directory surfaced as `artifacts_dir` in the return contract when that phase is selected as the pipeline's canonical output bundle.
```

---

## Recommended Return Contract Example

Add an example contract to the spec:

```yaml
return_contract:
  status: "success"
  task_hierarchy_path: null
  tasks_created: 0
  delegation_map: {}
  parallel_groups: []
  completion_summary: {}
  pipeline_manifest: ".dev/spawn-output/2026-03-23/spawn-manifest.json"
  artifacts_dir: ".dev/spawn-output/2026-03-23/phases/merge/"
```

And document that consumers can then read:

```text
.dev/spawn-output/2026-03-23/phases/merge/merged-output.md
.dev/spawn-output/2026-03-23/phases/merge/diff-analysis.md
.dev/spawn-output/2026-03-23/phases/merge/debate-transcript.md
.dev/spawn-output/2026-03-23/phases/merge/base-selection.md
.dev/spawn-output/2026-03-23/phases/merge/refactor-plan.md
.dev/spawn-output/2026-03-23/phases/merge/merge-log.md
```

---

## Interaction With Existing Adversarial Contract

This change is especially clean because `/sc:adversarial` already defines an `artifacts_dir` field in its own return contract.

That means `/sc:spawn` is not inventing a new concept. It is propagating an existing downstream contract upward.

Recommended implementation policy:
- when `compare-merge` invokes `/sc:adversarial`, capture its returned `artifacts_dir`
- set the phase `output_dir` to that same directory, or validate they match
- surface that directory as spawn-level `artifacts_dir` if this phase is the selected canonical bundle

This avoids duplicating path derivation logic and reduces drift between the two command contracts.

---

## Edge Cases

### 1. Pipeline has no compare-merge phase
- `artifacts_dir = null`
- consumer uses `pipeline_manifest`

### 2. Pipeline has multiple compare-merge phases
- `artifacts_dir` points to the last successfully completed compare-merge phase in topological order
- manifest remains the source of truth for the others

### 3. Compare-merge fails after creating artifacts
- if the phase output directory exists, still surface it as `artifacts_dir`
- `status` and manifest phase status communicate whether the result is partial/failed
- this preserves debuggability and manual recovery value

### 4. Compare-merge is skipped because dependencies failed
- `artifacts_dir = null` unless a previous relevant compare-merge phase produced the canonical bundle

---

## Acceptance Criteria

1. The `/sc:spawn` return contract includes `artifacts_dir`.
2. In Standard Mode, `artifacts_dir` is `null`.
3. In Pipeline Mode without `compare-merge`, `artifacts_dir` is `null`.
4. In Pipeline Mode with one successful `compare-merge` phase, `artifacts_dir` equals that phase’s output directory.
5. That directory is documented as containing:
   - `merged-output.md`
   - `diff-analysis.md`
   - `debate-transcript.md`
   - `base-selection.md`
   - `refactor-plan.md`
   - `merge-log.md`
6. The spec explicitly tells consumers when to use `artifacts_dir` versus `pipeline_manifest`.
7. If multiple `compare-merge` phases exist, the spec defines a deterministic selection rule for `artifacts_dir`.
8. If a compare-merge phase fails after producing artifacts, the directory may still be surfaced via `artifacts_dir` for recovery and inspection.
9. The documented relationship between spawn `artifacts_dir` and adversarial `artifacts_dir` is explicit, so the two contracts do not drift.

---

## Final Recommendation

Adopt the additive contract change:
- keep `pipeline_manifest` for full pipeline introspection,
- add `artifacts_dir` for direct access to the final adversarial artifact bundle,
- and document that consumers should use `artifacts_dir` as the primary entry point to all `compare-merge` outputs.

This is the smallest, clearest, and most backward-compatible fix for M13.

It solves the real problem: making adversarial’s full output visible to consumers without forcing them to reverse-engineer pipeline internals from the manifest.

---

# M14 — Spawn Checkpoint Schema Proposal

## Problem

The current Spawn V2 spec requires `Checkpoint → Serena memory` at every wave boundary, but it does not define:

- what data is persisted
- how checkpoint keys are named
- how concurrent sessions avoid collisions
- how `--resume` determines whether a checkpoint is still valid

This makes resume semantics underspecified and unsafe.

---

## Proposal Summary

Define Spawn checkpoints as **versioned, session-scoped JSON documents** written to Serena memory at every wave boundary.

Design goals:

1. **Deterministic lookup** — every checkpoint has a predictable key.
2. **Session isolation** — concurrent runs never share a memory key.
3. **Resume safety** — `--resume` only accepts checkpoints that match the current run context.
4. **Wave-specific detail** — each wave persists the data needed by the next wave, not just a generic summary.
5. **Staleness detection** — changed inputs, flags, graph shape, or workspace identity invalidate resume.

---

## 1. Key Naming Convention

### Canonical key format

```text
spawn/{workspace_fingerprint}/{pipeline_id}/{session_id}/wave/{wave_index}
```

### Companion alias keys

These are optional convenience pointers for lookup:

```text
spawn/{workspace_fingerprint}/{pipeline_id}/latest
spawn/{workspace_fingerprint}/{pipeline_id}/{session_id}/latest
```

The alias values are small pointer records containing the canonical wave key and metadata, not full checkpoint payloads.

### Field definitions

- `spawn` — fixed namespace prefix
- `workspace_fingerprint` — stable identifier for the repo/worktree
- `pipeline_id` — the manifest-level pipeline identifier, e.g. `spawn-2026-03-23T03-14-55Z`
- `session_id` — unique execution session identifier for this exact invocation
- `wave_index` — zero-based or one-based integer wave number; use one-based for readability

### Required generation rules

#### `workspace_fingerprint`

Use a deterministic, collision-resistant value derived from:

```text
SHA256(realpath(output_root) + "|" + realpath(repo_root) + "|" + git_head_or_detached_state)
```

Truncate to 12-16 hex chars for key readability.

Purpose:
- isolates separate worktrees on the same branch
- distinguishes runs against different repos or detached HEAD states
- prevents collision across parallel Claude sessions sharing Serena memory

#### `pipeline_id`

Reuse the manifest pipeline ID already defined in the spec:

```json
"pipeline_id": "spawn-<timestamp>"
```

Strengthen it to include enough entropy to avoid same-second collisions:

```text
spawn-<UTC timestamp>-<6 char random suffix>
```

Example:

```text
spawn-2026-03-23T03-14-55Z-a91f3c
```

#### `session_id`

Generate a unique per-invocation ID:

```text
sess-<UTC timestamp>-<8 char random suffix>
```

Example:

```text
sess-2026-03-23T03-14-55Z-81c4d2e1
```

This is distinct from `pipeline_id` so retries or manual `--resume` attempts can be traced separately.

### Example keys

```text
spawn/4f2ab9130cd1/spawn-2026-03-23T03-14-55Z-a91f3c/sess-2026-03-23T03-14-55Z-81c4d2e1/wave/1
spawn/4f2ab9130cd1/spawn-2026-03-23T03-14-55Z-a91f3c/sess-2026-03-23T03-14-55Z-81c4d2e1/wave/2
spawn/4f2ab9130cd1/spawn-2026-03-23T03-14-55Z-a91f3c/latest
```

---

## 2. Checkpoint Envelope Schema

Every wave checkpoint MUST use the same top-level envelope.

```json
{
  "schema_version": "1.0",
  "checkpoint_type": "spawn_wave_boundary",
  "pipeline_id": "spawn-2026-03-23T03-14-55Z-a91f3c",
  "session_id": "sess-2026-03-23T03-14-55Z-81c4d2e1",
  "workspace_fingerprint": "4f2ab9130cd1",
  "wave_index": 2,
  "wave_name": "dispatch",
  "created_at": "2026-03-23T03:21:18Z",
  "updated_at": "2026-03-23T03:21:18Z",
  "status": "completed",
  "resume_eligible": true,
  "resume_from": "wave_3",
  "run_context": {},
  "graph_snapshot": {},
  "manifest_snapshot": {},
  "wave_state": {},
  "artifacts": {},
  "validation": {},
  "provenance": {},
  "summary": {}
}
```

### Top-level fields

| Field | Type | Required | Purpose |
|---|---|---:|---|
| `schema_version` | string | yes | Versioned contract for future migrations |
| `checkpoint_type` | string | yes | Fixed discriminator: `spawn_wave_boundary` |
| `pipeline_id` | string | yes | Links checkpoint to manifest/run |
| `session_id` | string | yes | Isolates concurrent sessions |
| `workspace_fingerprint` | string | yes | Isolates repo/worktree identity |
| `wave_index` | int | yes | Boundary number |
| `wave_name` | string | yes | Human-readable wave label |
| `created_at` | ISO-8601 | yes | First write time |
| `updated_at` | ISO-8601 | yes | Last write time |
| `status` | enum | yes | `completed | failed | invalidated` |
| `resume_eligible` | bool | yes | Whether this boundary can be resumed from |
| `resume_from` | string/null | yes | Next wave label or phase entrypoint |
| `run_context` | object | yes | Immutable inputs needed for staleness checks |
| `graph_snapshot` | object | yes | Frozen DAG/parallel-group shape |
| `manifest_snapshot` | object | yes | Manifest status at checkpoint time |
| `wave_state` | object | yes | Wave-specific persisted state |
| `artifacts` | object | yes | Output paths and hashes required by resume |
| `validation` | object | yes | Resume safety checks |
| `provenance` | object | yes | Source, host, branch, commit metadata |
| `summary` | object | yes | Short operator-facing explanation |

---

## 3. Required `run_context` Fields

`run_context` is the immutable identity of the run. `--resume` MUST compare the current invocation against this block.

```json
{
  "task_description": "user prompt or pipeline task",
  "pipeline_mode": true,
  "cli_command": "/sc:spawn --pipeline ...",
  "flags": {
    "depth": "deep",
    "pipeline_seq": false,
    "max_concurrent": 6,
    "agents": ["architect", "backend", "security"],
    "output_dir": "/abs/path",
    "prompt_hash": "sha256:...",
    "config_hash": "sha256:..."
  },
  "repo_root": "/config/workspace/IronClaude",
  "output_root": "/config/workspace/IronClaude/.dev/.../output",
  "git": {
    "branch": "v3.0-v3.2-Fidelity",
    "head": "08fa0d8...",
    "is_dirty": true
  },
  "spec_inputs": {
    "pipeline_definition_hash": "sha256:...",
    "resolved_phase_config_hash": "sha256:..."
  }
}
```

### Notes

- `flags` MUST contain all resume-relevant CLI settings after inheritance/resolution, not just raw user input.
- `prompt_hash` hashes the effective prompt after `${prompt}` substitution.
- `resolved_phase_config_hash` hashes the fully expanded pipeline definition after wildcard expansion, inheritance, and dependency resolution.
- These hashes are the primary defense against stale resumes when the spec or execution plan changes.

---

## 4. Required `graph_snapshot` Fields

`graph_snapshot` captures the execution structure at the wave boundary.

```json
{
  "phase_ids": ["analyze_api", "design_patch", "test_regression"],
  "phase_count": 3,
  "dependency_edges": [
    ["analyze_api", "design_patch"],
    ["design_patch", "test_regression"]
  ],
  "parallel_groups": [
    ["analyze_api"],
    ["design_patch"],
    ["test_regression"]
  ],
  "graph_hash": "sha256:...",
  "dag_version": 1
}
```

### Resume rule

If `graph_hash` differs from the current resolved DAG, `--resume` MUST reject the checkpoint as stale.

---

## 5. Required `manifest_snapshot` Fields

This mirrors the on-disk manifest enough to support a reliable resume decision.

```json
{
  "manifest_path": "/abs/path/spawn-manifest.json",
  "manifest_hash": "sha256:...",
  "phase_statuses": {
    "analyze_api": "completed",
    "design_patch": "completed",
    "test_regression": "pending"
  },
  "completed_phase_ids": ["analyze_api", "design_patch"],
  "failed_phase_ids": [],
  "skipped_phase_ids": [],
  "last_completed_phase": "design_patch"
}
```

### Resume rule

The Serena checkpoint is an accelerator, not the sole source of truth. `--resume` SHOULD cross-check Serena checkpoint data against the manifest on disk. If they disagree, disk manifest wins and the checkpoint is marked suspect.

---

## 6. Wave-Specific `wave_state` Schema

Each wave persists a common block plus wave-specific fields.

### Common fields for every wave

```json
{
  "started_at": "ISO-8601",
  "completed_at": "ISO-8601",
  "duration_ms": 1234,
  "inputs_ready": true,
  "outputs_written": true,
  "errors": [],
  "warnings": [],
  "operator_notes": "short summary"
}
```

### Wave 1 — Intake / Resolution

Purpose: capture normalized inputs before DAG construction.

```json
{
  "task_description": "...",
  "raw_flags": {},
  "resolved_flags": {},
  "resolved_agents": ["architect", "backend"],
  "resolved_prompt": "effective prompt text or omitted if too large",
  "resolved_prompt_hash": "sha256:...",
  "pipeline_definition_source": "/abs/path/or inline",
  "expanded_phases": [
    {
      "id": "analyze_api",
      "type": "analyze",
      "depends_on": [],
      "output_dir": "/abs/path/analyze_api"
    }
  ]
}
```

### Wave 2 — DAG Construction

Purpose: capture the frozen execution plan.

```json
{
  "domain_map": {
    "api": ["analyze_api"],
    "tests": ["test_regression"]
  },
  "dependency_graph": {
    "analyze_api": [],
    "design_patch": ["analyze_api"],
    "test_regression": ["design_patch"]
  },
  "parallel_groups": [
    ["analyze_api"],
    ["design_patch"],
    ["test_regression"]
  ],
  "concurrency_cap": 10,
  "sequential_override": false,
  "delegation_plan": {
    "analyze_api": "/sc:analyze",
    "design_patch": "/sc:design",
    "test_regression": "/sc:test"
  }
}
```

### Wave 3 — Dispatch / Execution

Purpose: capture actual runtime outcomes at the phase-group boundary.

```json
{
  "group_index": 1,
  "dispatched_phase_ids": ["design_patch"],
  "completed_phase_ids": ["design_patch"],
  "failed_phase_ids": [],
  "manual_phase_ids": [],
  "skipped_phase_ids": [],
  "phase_results": {
    "design_patch": {
      "status": "completed",
      "attempts": 1,
      "agent": "architect",
      "command": "/sc:design",
      "started_at": "ISO-8601",
      "completed_at": "ISO-8601",
      "output_dir": "/abs/path/design_patch",
      "output_hash": "sha256:...",
      "error": null
    }
  }
}
```

### Wave 4 — Artifact Routing / Dependency Verification

Purpose: record the handoff state required by downstream consumers.

```json
{
  "routing_map": {
    "design_patch": ["test_regression"]
  },
  "verified_dependency_outputs": {
    "design_patch": {
      "exists": true,
      "path": "/abs/path/design_patch",
      "hash": "sha256:..."
    }
  },
  "consumer_ready": ["test_regression"],
  "consumer_blocked": []
}
```

### Wave 5 — Completion / Resume Handoff

Purpose: persist the minimum complete state for a future `--resume`.

```json
{
  "completion_summary": {
    "total": 3,
    "completed": 2,
    "failed": 0,
    "skipped": 0,
    "pending": 1,
    "manual": 0
  },
  "next_runnable_phase_ids": ["test_regression"],
  "resume_entrypoint": "test_regression",
  "preserved_context_paths": [
    "/abs/path/analyze_api",
    "/abs/path/design_patch"
  ],
  "human_handoff_notes": "Resume at test_regression after verifying unchanged DAG"
}
```

---

## 7. `artifacts` Block

Artifacts required for resume MUST be explicit and hashed.

```json
{
  "required": [
    {
      "phase_id": "design_patch",
      "path": "/abs/path/design_patch/result.md",
      "exists": true,
      "size_bytes": 10240,
      "sha256": "abc123..."
    }
  ],
  "optional": [
    {
      "phase_id": "analyze_api",
      "path": "/abs/path/analyze_api/notes.md",
      "exists": true,
      "size_bytes": 2048,
      "sha256": "def456..."
    }
  ]
}
```

### Resume rule

If any required artifact is missing or hash-mismatched, the checkpoint is not resumable from that boundary.

---

## 8. `validation` Block

This block is computed when the checkpoint is written and re-evaluated on `--resume`.

```json
{
  "staleness_basis": {
    "git_head": "08fa0d8...",
    "resolved_phase_config_hash": "sha256:...",
    "graph_hash": "sha256:...",
    "manifest_hash": "sha256:...",
    "required_artifact_hashes": {
      "design_patch": "sha256:..."
    }
  },
  "resume_checks": {
    "workspace_match": true,
    "pipeline_match": true,
    "flags_match": true,
    "git_head_match": true,
    "graph_match": true,
    "manifest_match": true,
    "artifacts_intact": true
  },
  "invalid_reason": null
}
```

---

## 9. Session Isolation Strategy

### Rule 1 — Never use shared generic keys

Forbidden:

```text
checkpoint
spawn-checkpoint
spawn/wave/1
```

These collide across users, worktrees, and concurrent sessions.

### Rule 2 — Session-scoped canonical keys are mandatory

Every write goes to the canonical key that includes both `pipeline_id` and `session_id`.

### Rule 3 — Aliases must be pointer-only

`latest` keys may exist, but they must only store:

```json
{
  "canonical_key": "spawn/.../wave/3",
  "pipeline_id": "spawn-...",
  "session_id": "sess-...",
  "wave_index": 3,
  "updated_at": "ISO-8601"
}
```

This avoids accidental overwrite of full checkpoint payloads.

### Rule 4 — Worktree-aware workspace identity

Two sessions on the same branch but in different worktrees MUST produce different `workspace_fingerprint` values because `realpath(repo_root)` is included.

### Rule 5 — Resume defaults to current session lineage only

When `--resume` is invoked without an explicit checkpoint key:

1. load `spawn/{workspace_fingerprint}/{pipeline_id}/latest`
2. verify its `workspace_fingerprint` matches current repo/worktree
3. follow `canonical_key`
4. reject if the session belongs to another incompatible run context

This permits recovery from the most recent session while still preventing accidental cross-run adoption.

---

## 10. Staleness Detection for `--resume`

`--resume` MUST reject a checkpoint if any of the following conditions hold.

### Hard invalidation checks

1. **Schema mismatch**
   - `schema_version` unsupported

2. **Workspace mismatch**
   - `workspace_fingerprint` differs from current run

3. **Pipeline mismatch**
   - requested `pipeline_id` differs from checkpoint `pipeline_id`

4. **Resolved config mismatch**
   - `resolved_phase_config_hash` differs

5. **DAG mismatch**
   - `graph_hash` differs

6. **Required artifact missing or hash changed**
   - any required output missing or mutated

7. **Manifest contradiction**
   - manifest marks a phase incomplete that checkpoint claims completed, or vice versa

8. **Checkpoint marked failed or invalidated**
   - `status != completed`

### Soft warning checks

These should warn, not always block:

1. **Git branch changed but HEAD unchanged**
2. **Working tree dirty state changed**
3. **Optional artifact hash changed**
4. **Checkpoint age exceeds freshness threshold**

### Freshness threshold

Add:

```json
"validation": {
  "max_resume_age_hours": 24
}
```

If older than threshold, warn and require explicit confirmation or `--force-resume`.

### Resume decision table

| Condition | Behavior |
|---|---|
| All hard checks pass | Resume allowed |
| Only soft warnings present | Resume allowed with warning |
| Any hard invalidation fails | Resume denied; re-plan from Wave 1 or earliest safe boundary |

---

## 11. Write/Read Semantics

### When to write

Write a checkpoint only at **wave-group boundaries**, after:

1. all phases in the current wave/group have reached terminal status for that boundary
2. manifest has been flushed to disk
3. required artifacts for downstream resume have been verified

### Write ordering

To keep disk and Serena consistent:

1. update `spawn-manifest.json`
2. fsync/atomic replace manifest
3. compute checkpoint payload and hashes
4. write canonical Serena checkpoint
5. update `latest` pointer key

### Read ordering on `--resume`

1. load manifest from disk
2. discover candidate Serena checkpoint
3. validate schema/version
4. compare `run_context`, `graph_snapshot`, and `manifest_snapshot`
5. verify required artifacts on disk
6. resume from `resume_from` only if all hard checks pass

---

## 12. Minimal JSON Example

```json
{
  "schema_version": "1.0",
  "checkpoint_type": "spawn_wave_boundary",
  "pipeline_id": "spawn-2026-03-23T03-14-55Z-a91f3c",
  "session_id": "sess-2026-03-23T03-14-55Z-81c4d2e1",
  "workspace_fingerprint": "4f2ab9130cd1",
  "wave_index": 2,
  "wave_name": "dag-construction",
  "created_at": "2026-03-23T03:21:18Z",
  "updated_at": "2026-03-23T03:21:18Z",
  "status": "completed",
  "resume_eligible": true,
  "resume_from": "wave_3",
  "run_context": {
    "task_description": "Implement Spawn V2 remediation plan",
    "pipeline_mode": true,
    "flags": {
      "depth": "deep",
      "pipeline_seq": false,
      "max_concurrent": 4,
      "output_dir": "/config/workspace/IronClaude/.dev/tmp/spawn-run",
      "prompt_hash": "sha256:111",
      "config_hash": "sha256:222"
    },
    "repo_root": "/config/workspace/IronClaude",
    "output_root": "/config/workspace/IronClaude/.dev/tmp/spawn-run",
    "git": {
      "branch": "v3.0-v3.2-Fidelity",
      "head": "08fa0d8",
      "is_dirty": true
    },
    "spec_inputs": {
      "pipeline_definition_hash": "sha256:333",
      "resolved_phase_config_hash": "sha256:444"
    }
  },
  "graph_snapshot": {
    "phase_ids": ["analyze", "design", "test"],
    "phase_count": 3,
    "dependency_edges": [["analyze", "design"], ["design", "test"]],
    "parallel_groups": [["analyze"], ["design"], ["test"]],
    "graph_hash": "sha256:555",
    "dag_version": 1
  },
  "manifest_snapshot": {
    "manifest_path": "/config/workspace/IronClaude/.dev/tmp/spawn-run/spawn-manifest.json",
    "manifest_hash": "sha256:666",
    "phase_statuses": {
      "analyze": "completed",
      "design": "pending",
      "test": "pending"
    },
    "completed_phase_ids": ["analyze"],
    "failed_phase_ids": [],
    "skipped_phase_ids": [],
    "last_completed_phase": "analyze"
  },
  "wave_state": {
    "started_at": "2026-03-23T03:20:00Z",
    "completed_at": "2026-03-23T03:21:18Z",
    "duration_ms": 78000,
    "inputs_ready": true,
    "outputs_written": true,
    "errors": [],
    "warnings": [],
    "operator_notes": "DAG resolved and frozen",
    "domain_map": {
      "backend": ["analyze", "design"],
      "qa": ["test"]
    },
    "dependency_graph": {
      "analyze": [],
      "design": ["analyze"],
      "test": ["design"]
    },
    "parallel_groups": [["analyze"], ["design"], ["test"]],
    "concurrency_cap": 4,
    "sequential_override": false,
    "delegation_plan": {
      "analyze": "/sc:analyze",
      "design": "/sc:design",
      "test": "/sc:test"
    }
  },
  "artifacts": {
    "required": [],
    "optional": []
  },
  "validation": {
    "staleness_basis": {
      "git_head": "08fa0d8",
      "resolved_phase_config_hash": "sha256:444",
      "graph_hash": "sha256:555",
      "manifest_hash": "sha256:666",
      "required_artifact_hashes": {}
    },
    "resume_checks": {
      "workspace_match": true,
      "pipeline_match": true,
      "flags_match": true,
      "git_head_match": true,
      "graph_match": true,
      "manifest_match": true,
      "artifacts_intact": true
    },
    "invalid_reason": null,
    "max_resume_age_hours": 24
  },
  "provenance": {
    "writer": "superclaude spawn",
    "host": "claude-code",
    "source": "serena-memory",
    "branch": "v3.0-v3.2-Fidelity"
  },
  "summary": {
    "headline": "Wave 2 completed successfully",
    "next_action": "Resume at wave_3 dispatch",
    "completed_count": 1,
    "pending_count": 2
  }
}
```

---

## 13. Normative Rules to Add to the Spec

Add the following requirements to the Spawn V2 spec:

1. **Checkpoint format**: All Serena checkpoints MUST conform to `spawn_wave_boundary` schema version `1.0`.
2. **Keying**: Checkpoints MUST use canonical key format `spawn/{workspace_fingerprint}/{pipeline_id}/{session_id}/wave/{wave_index}`.
3. **Session isolation**: Checkpoints MUST include both `pipeline_id` and `session_id`; generic shared keys are prohibited.
4. **Resume validation**: `--pipeline-resume` MUST validate `workspace_fingerprint`, `resolved_phase_config_hash`, `graph_hash`, manifest consistency, and required artifacts before resuming.
5. **Manifest precedence**: On conflict, on-disk manifest state is authoritative; Serena checkpoint is advisory acceleration data.
6. **Boundary-only writes**: Checkpoints MUST be written only after a wave/group reaches a stable boundary and manifest/artifacts are flushed.
7. **Staleness handling**: Any hard invalidation condition MUST block resume and require re-entry from the earliest safe wave.
8. **Compatibility**: Unsupported `schema_version` MUST be treated as non-resumable.

---

## 14. Recommended Implementation Sequence

1. Extend manifest generation so `pipeline_id` is unique and high-entropy.
2. Define a `SpawnCheckpointState` dataclass/model with the envelope above.
3. Add canonical key builder and `latest` pointer builder helpers.
4. Hash resolved config, DAG, manifest, and required artifacts at each wave boundary.
5. Write manifest first, then Serena checkpoint.
6. Implement `--resume` validator using hard/soft invalidation rules.
7. Add tests for:
   - concurrent sessions in same repo
   - concurrent sessions in different worktrees
   - changed flags
   - changed DAG
   - missing artifacts
   - stale checkpoint age
   - manifest/checkpoint disagreement

---

## Recommendation

Adopt this schema exactly or with only additive changes. The critical point is not the specific field names; it is that Spawn V2 needs a **versioned, session-scoped, hash-validated checkpoint contract**. Without that, `Checkpoint → Serena memory` remains too ambiguous to support safe `--resume` behavior.


---

# M15 Remediation Proposal — Exact Criteria for `status: success | partial | failed`

## Issue

The current `/sc:spawn` v2 spec defines a return contract with:

- `status: success | partial | failed`

but does not define concrete thresholds for when each value applies.

That leaves these questions unresolved:

1. Is one failed task enough to make the run `partial`?
2. When does `partial` become `failed`?
3. How should `manual` tasks be counted?
4. Should Standard Mode and Pipeline Mode use the same rules?
5. How should STOP conditions interact with aggregate counts?

This proposal defines exact, deterministic rules for both modes.

---

## Design Goal

The status field should answer one question consistently:

**How complete was the requested execution, from the orchestrator's point of view?**

That means:

- `success` = everything required by the selected mode completed without unresolved execution debt
- `partial` = some useful work completed, but the requested execution was not fully completed
- `failed` = the requested execution did not produce a sufficiently completed run, or execution hit a blocking stop condition before meaningful completion

The status must be computable from runner-observed outcomes, not agent self-interpretation.

---

## Core Principle

Use **terminal unit accounting**:

- In **Standard Mode**, the counted units are **delegated tasks**.
- In **Pipeline Mode**, the counted units are **pipeline phases**.

Each unit ends in one of these normalized outcomes:

- `completed`
- `failed`
- `manual`
- `skipped`
- `not_started`

For status calculation:

- `completed` counts as successful completion.
- `failed` counts as unsuccessful attempted completion.
- `manual` counts as unsuccessful attempted completion that produced handoff debt.
- `skipped` counts as non-completed and only contributes to `failed` when the skip was caused by upstream failure or STOP logic.
- `not_started` counts as non-completed.

For top-level status, **`manual` is treated as incomplete work, not success**.

---

## Exact Definitions

### `success`

Return `status: success` only when **all required execution units completed successfully**.

#### Standard Mode
Return `success` iff all of the following are true:

1. At least one task was created unless `--dry-run`/`--no-delegate` intentionally prevents execution.
2. `completed_count == total_required_tasks`
3. `failed_count == 0`
4. `manual_count == 0`
5. `not_started_count == 0`
6. No blocking STOP condition occurred at the command level.

Plain language:

- Every delegated task finished.
- Nothing failed.
- Nothing was deferred to manual handling.
- Nothing required by the decomposition was left unfinished.

#### Pipeline Mode
Return `success` iff all of the following are true:

1. At least one phase was scheduled.
2. `completed_phase_count == total_required_phases`
3. `failed_phase_count == 0`
4. `manual_phase_count == 0`
5. `not_started_phase_count == 0`
6. No pipeline-level STOP condition occurred.
7. No downstream phase was skipped because an upstream dependency failed.

Plain language:

- Every phase in the DAG that belongs to the run completed.
- No phase failed.
- No phase ended in manual handoff.
- No dependency break prevented execution.

---

### `partial`

Return `status: partial` when the run produced **some completed useful execution**, but **not full completion**.

This is the mixed-outcome state.

#### Standard Mode
Return `partial` iff all of the following are true:

1. `completed_count >= 1`
2. At least one of the following is true:
   - `failed_count >= 1`
   - `manual_count >= 1`
   - `not_started_count >= 1`
3. No top-level STOP condition invalidated the run before any meaningful completion.

Equivalent threshold:

- **One failed task is enough for `partial` if at least one other task completed.**
- **One manual task is enough for `partial` if at least one other task completed.**

Examples:

- 5 completed, 1 failed → `partial`
- 5 completed, 1 manual → `partial`
- 3 completed, 2 not started due to dependency fallout → `partial`
- 1 completed, 9 manual → `partial`

#### Pipeline Mode
Return `partial` iff all of the following are true:

1. `completed_phase_count >= 1`
2. At least one of the following is true:
   - `failed_phase_count >= 1`
   - `manual_phase_count >= 1`
   - `not_started_phase_count >= 1`
   - one or more downstream phases were skipped because dependencies did not complete
3. The pipeline did not fully collapse before any phase completed.

Equivalent threshold:

- **One failed phase is enough for `partial` if at least one other phase completed.**
- **One manual phase is enough for `partial` if at least one other phase completed.**

Examples:

- analyze completed, design failed, test not started → `partial`
- analyze completed, design manual after retry exhaustion, test blocked → `partial`
- phase group of 4: 3 completed, 1 failed → `partial`

---

### `failed`

Return `status: failed` when the run did **not achieve any completed execution unit**, or when a top-level blocking condition stops the run before meaningful completion can be claimed.

#### Standard Mode
Return `failed` iff either condition set applies:

##### A. Zero-completion failure
1. `completed_count == 0`, and
2. One or more of the following is true:
   - `failed_count >= 1`
   - `manual_count >= 1`
   - `not_started_count == total_required_tasks`
   - decomposition succeeded but delegation/execution never produced a completed task

##### B. Blocking top-level STOP failure
A command-level STOP condition occurs before any task completes, such as:

- missing required input
- decomposition cannot be constructed
- invalid command/agent mapping
- checkpoint resume corruption that prevents execution
- orchestration abort before first task completion

Plain language:

- If nothing completed, the run is `failed`.
- Manual-only outcomes without any completed task are still `failed`, not `partial`.

Examples:

- 0 completed, 2 failed, 4 manual → `failed`
- 0 completed, all tasks manual after retries → `failed`
- no tasks could be executed because setup failed → `failed`

#### Pipeline Mode
Return `failed` iff either condition set applies:

##### A. Zero-completion failure
1. `completed_phase_count == 0`, and
2. One or more of the following is true:
   - `failed_phase_count >= 1`
   - `manual_phase_count >= 1`
   - `not_started_phase_count == total_required_phases`
   - first executable phase failed or went manual, preventing all progress

##### B. Blocking pipeline STOP failure
A pipeline-level STOP condition occurs before any phase completes, such as:

- YAML/shorthand parse failure
- cycle detected in DAG
- missing required `${prompt}` after prompt resolution
- invalid phase type
- `generate-parallel` without `--agents`
- `compare-merge` with fewer than 2 artifacts
- first runnable phase fails in a way that halts all remaining execution

Plain language:

- If no phase completed, the pipeline is `failed`.
- A pipeline that aborts at validation or before first useful phase completion is `failed`.

Examples:

- parse error before execution → `failed`
- first phase failed, all dependents skipped → `failed`
- first phase became manual, no other phase could run → `failed`

---

## Treatment of `manual`

## Normative Rule

A `manual` unit is **not successful completion**.

For top-level contract status:

- `manual` contributes to `partial` when there is also at least one `completed` unit.
- `manual` contributes to `failed` when there are zero `completed` units.

This is the simplest and least ambiguous rule because manual handoff means the orchestrator did not finish the requested work autonomously.

### Why not count `manual` as success?

Because the spec already uses `manual` as a fallback for unresolved execution debt:

- retry exhausted
- sub-agent could not complete
- operator intervention now required

If `manual` counted as success, a run with many unfinished tasks could still claim `success`, which would make the contract misleading.

### Why not make `manual` always `failed`?

Because the run may still have delivered substantial useful output. If some tasks/phases completed and others were handed off, that is exactly what `partial` is for.

---

## Threshold Summary Table

### Standard Mode

| Completed tasks | Failed tasks | Manual tasks | Not started tasks | Top-level status |
|---|---:|---:|---:|---|
| all | 0 | 0 | 0 | `success` |
| >=1 | any >=1 | any | any | `partial` |
| >=1 | any | any >=1 | any | `partial` |
| >=1 | 0 | 0 | any >=1 | `partial` |
| 0 | any >=1 | any | any | `failed` |
| 0 | any | any >=1 | any | `failed` |
| 0 | 0 | 0 | all | `failed` |

### Pipeline Mode

| Completed phases | Failed phases | Manual phases | Blocked/not started phases | Top-level status |
|---|---:|---:|---:|---|
| all | 0 | 0 | 0 | `success` |
| >=1 | any >=1 | any | any | `partial` |
| >=1 | any | any >=1 | any | `partial` |
| >=1 | 0 | 0 | any >=1 | `partial` |
| 0 | any >=1 | any | any | `failed` |
| 0 | any | any >=1 | any | `failed` |
| 0 | 0 | 0 | all | `failed` |

---

## Mode-Specific Clarifications

### Standard Mode Clarification

Standard Mode decomposes a task into delegated work items. Therefore its return status must be based on **delegated task completion**, not on whether decomposition alone succeeded.

So:

- successful planning with zero completed delegated tasks is **not** `success`
- hierarchy document written but no delegated execution completed is **not** `partial`
- it is `failed` unless the command explicitly documents a non-executing mode such as `--dry-run`

### Pipeline Mode Clarification

Pipeline Mode executes an explicit DAG. Therefore its return status must be based on **phase completion across the DAG**, not just manifest creation.

So:

- manifest written but no phase completed is **not** `partial`
- independent branches that complete while one branch fails yield `partial`
- dependency-caused skips count against full completion and therefore prevent `success`

---

## Special Handling for Non-Executing Modes

These cases should not use the normal execution-completeness semantics unless the spec explicitly wants them to.

### `--dry-run`

Recommended rule:

- Return `status: success` only if validation/planning completed as intended.
- Include `execution_performed: false` in the return contract.

Rationale:
A dry run intentionally requests planning, not execution. It should be judged against its own objective.

### `--no-delegate`

Recommended rule:

- Return `status: success` only if the hierarchy/delegation plan was fully produced.
- Include `execution_performed: false` and `delegation_suppressed: true`.

Rationale:
This mode intentionally stops before sub-agent execution.

If the team does not want special-case semantics, then these modes must be documented as planning-only and excluded from the normal execution status contract. But they should not silently reuse the same meanings without documentation.

---

## Recommended Computation Algorithm

### Standard Mode

1. Build the full set of required delegated tasks.
2. Normalize each task to one of: `completed`, `failed`, `manual`, `not_started`, `skipped`.
3. Compute:
   - `completed_count`
   - `failed_count`
   - `manual_count`
   - `not_started_count`
4. If a planning-only mode is active, use planning-only status rules.
5. Else if `completed_count == total_required_tasks` and all other non-complete counts are zero, return `success`.
6. Else if `completed_count >= 1`, return `partial`.
7. Else return `failed`.

### Pipeline Mode

1. Build the full set of required phases from the DAG.
2. Normalize each phase to one of: `completed`, `failed`, `manual`, `not_started`, `skipped_due_to_dependency`, `skipped_by_policy`.
3. Treat `skipped_due_to_dependency` as non-complete for top-level status.
4. Compute:
   - `completed_phase_count`
   - `failed_phase_count`
   - `manual_phase_count`
   - `not_started_phase_count`
5. If `completed_phase_count == total_required_phases` and all other non-complete counts are zero, return `success`.
6. Else if `completed_phase_count >= 1`, return `partial`.
7. Else return `failed`.

---

## Proposed Normative Spec Text

Add this under `## Return Contract` in the v2 spec.

```md
### Status computation

The `status` field reports overall execution completeness.

#### Standard Mode
Evaluate status over delegated tasks.

- `success`: all required delegated tasks completed; zero failed, zero manual, zero not-started.
- `partial`: at least one delegated task completed, but full completion was not achieved because one or more tasks failed, became manual, or did not start.
- `failed`: zero delegated tasks completed, or execution stopped before any task completed.

`manual` counts as incomplete work:
- if at least one task completed, `manual` contributes to `partial`
- if zero tasks completed, `manual` contributes to `failed`

#### Pipeline Mode
Evaluate status over pipeline phases.

- `success`: all required phases completed; zero failed, zero manual, zero dependency-blocked/not-started.
- `partial`: at least one phase completed, but full completion was not achieved because one or more phases failed, became manual, or were blocked/not started.
- `failed`: zero phases completed, or pipeline execution stopped before any phase completed.

A single failed or manual unit is sufficient to prevent `success`.
A single failed or manual unit yields `partial` only when at least one other required unit completed.
Otherwise the run is `failed`.
```

---

## Recommended Companion Schema Change

To make the contract auditable, add explicit counts.

### Standard fields

```yaml
status: success|partial|failed
mode: standard|pipeline
completed_count: <int>
failed_count: <int>
manual_count: <int>
not_started_count: <int>
```

### Pipeline-specific extension

```yaml
dependency_blocked_count: <int>
```

This avoids forcing consumers to infer status from a free-form `completion_summary` object.

---

## Acceptance Criteria

1. The spec states whether one failed task is enough for `partial`.
2. The spec states whether one manual task is enough for `partial`.
3. The spec defines the boundary between `partial` and `failed` using a concrete threshold.
4. Standard Mode uses delegated-task counts as the status basis.
5. Pipeline Mode uses phase counts as the status basis.
6. `success` requires zero failed/manual/unstarted required units.
7. `partial` requires at least one completed required unit.
8. `failed` applies whenever zero required units completed or execution stopped before meaningful completion.
9. `manual` is explicitly documented as incomplete work, not success.
10. The return contract includes enough counts for downstream verification.

---

## Final Recommendation

Adopt the following exact policy:

- **`success` = all required units completed, with zero failed/manual/unstarted units.**
- **`partial` = at least one required unit completed, but at least one other required unit failed/manual/unstarted.**
- **`failed` = zero required units completed, or a blocking STOP condition ended execution before any required unit completed.**
- **`manual` never counts as success.** It contributes to `partial` only when there is also at least one completed unit; otherwise it contributes to `failed`.

This rule is concrete, mode-aware, easy to compute, and directly answers the ambiguity raised in M15.

---

