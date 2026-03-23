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
