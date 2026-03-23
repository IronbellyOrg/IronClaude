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