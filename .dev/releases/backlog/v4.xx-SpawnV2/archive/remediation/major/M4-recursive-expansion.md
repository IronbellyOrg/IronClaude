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
