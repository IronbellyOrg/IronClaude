# C6: `generate` Phase Type Missing from Grammar — Remediation Proposal

## Problem
The `generate-parallel` expansion produces phases with `type: generate` but `generate` is not in the valid phase type list. The grammar, manifest schema, and delegation matrix don't account for it.

## Step-by-Step Solution

### Step 1: Add `generate` as a valid phase type

`generate` is the expanded form of `generate-parallel`. It represents a single agent executing a prompt — fundamentally different from the existing phase types which map to `/sc:*` commands.

**Updated grammar**:
```
type = "analyze" | "design" | "implement" | "test" | "review" | "deploy"
       | "generate-parallel" | "generate" | "compare-merge"
```

Note: `generate-parallel` is a YAML-only directive (expanded at parse time). `generate` is the resulting concrete phase type. `generate-parallel` does NOT appear in the inline shorthand grammar — it only exists in YAML definitions.

### Step 2: Define `generate` phase behavior

Unlike other phase types, `generate` phases:
1. Do NOT map to a `/sc:*` command via the delegation matrix
2. Use the agent spec directly from the `--agents` expansion (model + persona)
3. Execute the `command_template` (resolved `${prompt}`) as the agent's task
4. Always produce `output.md` as primary artifact

```
generate phase dispatch:
  - Agent type: determined by --agents spec (e.g., opus → general-purpose)
  - Model: from agent spec (e.g., opus, sonnet, haiku)
  - Persona: from agent spec (e.g., architect, analyzer)
  - Prompt: resolved command_template value
  - Output: <output_dir>/phases/<phase_id>/output.md
```

### Step 3: Define delegation matrix bypass for `generate` phases

Add to `refs/delegation-matrix.md`:
```
## Special Phase Types

### generate (from generate-parallel expansion)
Generate phases bypass the standard delegation matrix. Agent selection
comes from the `--agents` CLI flag, not from command-to-agent mapping.

| Source | Agent Type | Model | Persona |
|--------|-----------|-------|---------|
| `--agents` spec | general-purpose | from spec | from spec |

The delegation matrix's Command Delegation Targets, Agent Selection,
and Prompt Construction Rules (Rules 1-3) still apply to generate phases:
- Rule 1: File paths resolved before delegation (if applicable)
- Rule 2: Evidence requirements injected (discovery tier)
- Rule 3: Cross-reference counts injected (if available)

### compare-merge (collect-all comparison)
Compare-merge phases use the adversarial command. Agent selection:
| Delegated Command | Agent Type | Model |
|-------------------|-----------|-------|
| `/sc:adversarial` | general-purpose | opus |
```

### Step 4: Update Pipeline Manifest Schema

Current type enum:
```
"type": "analyze|design|implement|test|review|deploy"
```

Updated:
```
"type": "analyze|design|implement|test|review|deploy|generate|compare-merge"
```

Note: `generate-parallel` is NEVER in the manifest — it's expanded before the manifest is created. Only the resulting `generate` phases appear.

### Step 5: Update the expansion output to use `generate` consistently

Current expansion example (already correct but needs explicit validation):
```
Expands to:
  - id: branch-opus-architect
    type: generate          ← now a valid type
    agent: opus:architect
    command: "/sc:brainstorm Think through an ideal solution"
    parallel_group: auto
```

Add to expansion rule documentation:
```
Expansion produces phases with:
  - type: "generate" (NOT "generate-parallel" — the directive is consumed)
  - id: "<parent_id>-<model>-<persona>" (auto-generated)
  - agent: "<model>:<persona>" (from --agents spec)
  - command: resolved command_template with ${prompt} substituted
  - parallel_group: auto (all siblings share same group)
```

### Step 6: Validate inline shorthand does not support generate-parallel

The inline shorthand grammar only supports concrete phase types. `generate-parallel` requires YAML because it needs structured fields (`source`, `command_template`, `output_format`).

Add clarification:
```
Note: `generate-parallel` and `compare-merge` are YAML-only phase types.
They cannot be expressed in inline shorthand because they require structured
configuration fields. Use YAML file input for DAGs that include dynamic phases.
```

If a user tries `--pipeline "generate-parallel -> compare-merge"`, the parser should STOP with:
```
Error: 'generate-parallel' requires YAML definition (--pipeline @file.yaml).
It cannot be used in inline shorthand because it needs 'source' and
'command_template' configuration fields.
```

## Files to Modify
- `refs/dependency-graph.md`: Update grammar to include `generate`
- `refs/dependency-graph.md`: Add parse error for generate-parallel in shorthand
- `refs/delegation-matrix.md`: Add Special Phase Types section
- `SKILL.md`: Update manifest schema type enum
- `SKILL.md`: Clarify expansion output type
- `SKILL.md`: Add inline shorthand restriction note
