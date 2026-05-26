# Adversarial Integration Reference

Reference document for the adversarial-debate behavior within sc:roadmap. Documents the canonical CLI **inline debate prompt flow** built by `build_debate_prompt` with depth control via `_DEPTH_INSTRUCTIONS`, plus the inference-only `Skill sc:adversarial-protocol` delegation mode (mode detection, agent-spec parsing, invocation patterns, return-contract consumption, frontmatter population, divergent-specs heuristic, and error handling) retained for skill-mode operators.

**Loaded in**: Wave 1A (when `--specs` present) and Wave 2 (when `--multi-roadmap` present).

---

## CLI Canonical Debate Prompt Flow (B-8, VERIFIED)

> **CLI parity.** The roadmap CLI does **not** delegate to a separate `sc:adversarial-protocol` skill. The "adversarial debate" inside `superclaude roadmap run` is a single LLM step built by `build_debate_prompt`, embedded as one entry in the flat 14-step pipeline. There is no Skill-to-skill invocation, no return contract YAML on disk, no separate consolidation pass, and no separate `--compare` / `--generate roadmap` sub-skill. Source: `src/superclaude/cli/roadmap/prompts.py:878-902` (`build_debate_prompt`), `:18-37` (`_DEPTH_INSTRUCTIONS`), `src/superclaude/cli/roadmap/executor.py:2076-2084` (Step wiring), `src/superclaude/cli/roadmap/gates.py:1155-1166` (`DEBATE_GATE`).

### CLI prompt builder

| Builder | Source | Signature |
|---|---|---|
| `build_debate_prompt` | `src/superclaude/cli/roadmap/prompts.py:878-902` | `build_debate_prompt(diff_path: Path, variant_a_path: Path, variant_b_path: Path, depth: Literal["quick", "standard", "deep"]) -> str` |

The builder returns one prompt string. It opens with `"You are a structured debate facilitator."`, instructs the LLM to read the diff analysis and both roadmap variants, then embeds the depth-specific debate-round instructions from `_DEPTH_INSTRUCTIONS`. There is no `Skill sc:adversarial-protocol` invocation, no sub-agent dispatch, and no protocol forwarding.

### Depth control via `_DEPTH_INSTRUCTIONS`

`_DEPTH_INSTRUCTIONS` is a module-level dict at `src/superclaude/cli/roadmap/prompts.py:18-37` keyed by the same `--depth` values exposed on the CLI:

| `--depth` | Rounds | `_DEPTH_INSTRUCTIONS` content (summary) |
|---|---|---|
| `quick` | 1 | "Conduct a single focused debate round. Each perspective states its position on the key divergence points, then provide a convergence assessment." |
| `standard` | 2 | "Conduct two debate rounds: Round 1 initial positions; Round 2 rebuttals. Then provide a convergence assessment." |
| `deep` | 3 | "Conduct three debate rounds: Round 1 initial positions; Round 2 rebuttals; Round 3 final synthesis (concessions + remaining disagreements). Then provide a convergence assessment." |

The selected depth string is interpolated directly into the prompt template at the `Debate format:\n{depth_instruction}` slot. The CLI does not run separate Python rounds — the entire debate, including all rounds, is one LLM call against one prompt with one output file.

### Single-step pipeline wiring

`cli/roadmap/executor.py:2076-2084` constructs **one** `Step(id="debate", ...)` that fires after the `diff` step and before the `score` step:

```python
Step(
    id="debate",
    prompt=build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth),
    output_file=debate_file,                  # out / "debate-transcript.md"
    gate=DEBATE_GATE,
    timeout_seconds=600,
    inputs=[diff_file] + _llm_inputs_for(config, roadmap_a, roadmap_b),
    retry_limit=1,
)
```

The `debate_file` is `<output_dir>/debate-transcript.md` (`executor.py:1962`). The single transport-level `retry_limit=1` is **not** a per-round retry — the entire embedded debate (whatever round count `_DEPTH_INSTRUCTIONS` produced) is treated as one LLM call.

### `DEBATE_GATE` — only mechanical validation

`cli/roadmap/gates.py:1155-1166`:

| Property | Value |
|---|---|
| `required_frontmatter_fields` | `convergence_score`, `rounds_completed` |
| `min_lines` | `50` |
| `enforcement_tier` | `STRICT` |
| Semantic checks | `convergence_score_valid` — `convergence_score` must parse as `float ∈ [0.0, 1.0]` (`_convergence_score_valid` in `gates.py`). |

There is **no** PASS/PARTIAL/FAIL routing on `convergence_score` inside the CLI debate gate — the gate only validates that the field is a valid float in `[0.0, 1.0]`. Threshold-based routing (`≥ 0.6 PASS`, `≥ 0.5 PARTIAL`, `< 0.5 FAIL`) described elsewhere in this skill is **inference-only**; the canonical CLI consumes the score downstream (in `score` / `merge` / `certify` steps) without imposing a binary cutoff at `debate`.

### Surrounding chain (canonical CLI flow)

The debate step sits in the four-step run of the 14-step pipeline that together perform the adversarial-merge behavior the skill calls "Wave 2 multi-roadmap generation":

| CLI Step | Builder | Gate | Output File | Source |
|---|---|---|---|---|
| `diff` | `build_diff_prompt` | `DIFF_GATE` | `<out>/diff-analysis.md` | `executor.py:2066-2074` |
| `debate` | `build_debate_prompt` | `DEBATE_GATE` | `<out>/debate-transcript.md` | `executor.py:2076-2084` |
| `score` | `build_score_prompt` | `SCORE_GATE` | `<out>/base-selection.md` | `executor.py:2086-2103` |
| `merge` | `build_merge_prompt` | `MERGE_GATE` | `<out>/roadmap.md` | `executor.py:2104-2126` |

Each step is one LLM call wired into the same flat pipeline as `extract`, `generate-{a}`, `generate-{b}`, `anti-instinct`, `test-strategy`, `spec-fidelity`, `wiring-verification`, `deviation-analysis`, `remediate`, and `certify` (see `_get_all_step_ids` at `executor.py:2281-2300`). No sub-skill, no `Task(...)` dispatch, no return-contract YAML on disk.

### What this means for skill behavior

- The skill's Wave 2 sub-step `3d` ("Invoke Skill `sc:adversarial-protocol` directly") describes an **inference-only delegation path** that has no CLI counterpart. In CLI-faithful terms the equivalent is the four-step `diff → debate → score → merge` chain above.
- The skill's "Return Contract Consumption" model (status / convergence_score routing / merged_output_path / fallback_mode etc.) describes a **Skill-mode contract** that is not produced by the CLI. The CLI emits per-step output files (`diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `roadmap.md`) gated by `GateCriteria`, not a unified `return-contract.yaml`.
- The skill's `--resume-from` interaction (consuming a `return-contract.yaml` from a fixture directory) is a **skill-mode resumability path**. The CLI offers its own `--resume` flag in `superclaude roadmap run` (different semantics — resumes the pipeline from a previously written step output file, not from a sub-skill contract).
- Skill prose referencing `Skill sc:adversarial-protocol args: "..."`, `--compare`, `--generate roadmap`, `--agents` (passed through to a sub-skill), `--interactive` propagation to a sub-skill, divergent-specs heuristics on a sub-skill convergence score, or fallback-mode warnings on a sub-skill return value describes **inference-only** behavior that is not implemented in the CLI today. See "Inference-Only Skill-Delegation Mode" below for the demoted material.

---

## Inference-Only Skill-Delegation Mode

> **Scope.** The following material describes an inference-only Skill-to-skill delegation model in which `sc:roadmap-protocol` invokes `Skill sc:adversarial-protocol` directly (the SKILL-DIRECT path per D-0001 reversal) and consumes a structured return contract. This model is **not** implemented by the canonical CLI debate flow above. It is retained as guidance for skill-mode operators running the protocol manually (or under a future CLI that adds protocol forwarding); anything in this section is out of canonical CLI scope and must not be cited as CLI behavior. Where this section's content overlaps the canonical CLI flow above, the canonical flow wins.

## Mode Detection

sc:roadmap supports three adversarial modes. Mode is determined by flag presence:

| Mode | Trigger Flags | Active Wave | Purpose |
|------|--------------|-------------|---------|
| Multi-spec consolidation | `--specs` | Wave 1A | Merge multiple specs into unified spec |
| Multi-roadmap generation | `--multi-roadmap --agents` | Wave 2 | Generate competing roadmap variants, merge best elements |
| Combined | `--specs` AND `--multi-roadmap --agents` | Wave 1A then Wave 2 | Both pipelines sequentially |

**Detection logic**:

1. If `--specs` flag present AND `--multi-roadmap` flag present → Combined mode
2. If `--specs` flag present (without `--multi-roadmap`) → Multi-spec consolidation
3. If `--multi-roadmap` flag present (without `--specs`) → Multi-roadmap generation
4. If neither flag present → No adversarial mode (standard single-spec pipeline)

**Implicit `--multi-roadmap` inference** (Wave 0): If `--agents` flag is present WITHOUT `--multi-roadmap`, auto-enable `--multi-roadmap` and emit info: `"--multi-roadmap auto-enabled (inferred from --agents flag)."` This runs BEFORE mode detection so the correct adversarial path is activated.

**Prerequisite check** (Wave 0): When either `--specs` or `--multi-roadmap` is present, verify `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` exists. If not found, abort: `"sc:adversarial skill not installed. Required for --specs/--multi-roadmap flags. Install via: superclaude install"`

---

## Agent Specification Parsing

The `--agents` flag accepts a comma-separated list of agent specifications. Each agent spec follows the format `model[:persona[:"instruction"]]`.

### Parsing Algorithm

1. **Split agent list**: Split the `--agents` value on `,` to produce individual agent specs
2. **Per-agent parsing**: For each agent spec, split on `:` (max 3 segments):
   - **Segment 1** (required): Model identifier (e.g., `opus`, `sonnet`, `haiku`, `gpt52`, `gemini`)
   - **Segment 2** (optional): If unquoted → persona name. If quoted → instruction (no persona)
   - **Segment 3** (optional): Instruction string (must be quoted)
3. **Quoted-second-segment detection**: If the second segment starts with `"` (quote character), treat it as an instruction, not a persona. The agent has no explicit persona and will inherit the primary persona from Wave 1B.

### Format Examples

| Input | Model | Persona | Instruction |
|-------|-------|---------|-------------|
| `opus` | opus | (inherited from Wave 1B) | none |
| `opus:architect` | opus | architect | none |
| `opus:architect:"focus on scalability"` | opus | architect | "focus on scalability" |
| `opus:"focus on scalability"` | opus | (inherited from Wave 1B) | "focus on scalability" |

### Mixed Format Example

`--agents opus:architect,sonnet,gpt52:security` parses to:

- Agent 1: model=opus, persona=architect
- Agent 2: model=sonnet, persona=(inherited)
- Agent 3: model=gpt52, persona=security

### Validation Rules

- **Agent count**: Must be 2-10 agents. If <2 or >10, abort: `"Agent count must be 2-10. Provided: N"`
- **Model validation**: All model identifiers must be recognized. Unknown models trigger abort: `"Unknown model '<model>' in --agents. Available models: opus, sonnet, haiku, gpt52, gemini, ..."`
- **Agent expansion**: Model-only agents (no explicit persona) inherit the primary persona auto-detected from Wave 1B domain analysis. Example: if Wave 1B detects primary persona "security", then `opus` expands to `opus:security`.

### Orchestrator Addition

When agent count ≥ 3, sc:roadmap automatically adds an orchestrator agent to coordinate adversarial debate rounds and prevent combinatorial explosion. The orchestrator:

- Groups similar variants
- Runs elimination rounds before final merge
- Is not counted toward the 2-10 agent limit (it's infrastructure, not a competing agent)

---

## Invocation Patterns

All invocations use the `Skill` tool (per Execution Vocabulary). Arguments are passed as a string to the Skill tool's `args` parameter.

### Multi-Spec Consolidation (Wave 1A)

**Invocation format**:

```text
Skill sc:adversarial-protocol args: "--compare <spec-files> --depth <roadmap-depth> --output <roadmap-output-dir> [--interactive]"
```

**Parameter mapping**:

- `<spec-files>`: Value of sc:roadmap's `--specs` flag (comma-separated paths)
- `<roadmap-depth>`: Value of sc:roadmap's `--depth` flag (maps directly: quick→quick, standard→standard, deep→deep)
- `<roadmap-output-dir>`: sc:roadmap's resolved output directory
- `--interactive`: Present only when sc:roadmap's `--interactive` flag is set

**Depth mapping** (controls debate rounds):
| sc:roadmap `--depth` | Propagated `--depth` | Debate Rounds |
|----------------------|----------------------|---------------|
| quick | quick | 1 |
| standard | standard | 2 |
| deep | deep | 3 |

**Example invocations**:

```text
# Standard depth, 3 specs
Skill sc:adversarial-protocol args: "--compare spec1.md,spec2.md,spec3.md --depth standard --output .dev/releases/current/auth-system/"

# Deep depth with interactive approval
Skill sc:adversarial-protocol args: "--compare spec1.md,spec2.md --depth deep --output .dev/releases/current/auth-system/ --interactive"
```

### Multi-Roadmap Generation (Wave 2)

**Invocation format**:

```text
Skill sc:adversarial-protocol args: "--source <spec-or-unified-spec> --generate roadmap --agents <expanded-agent-specs> --depth <roadmap-depth> --output <roadmap-output-dir> [--interactive]"
```

**Parameter mapping**:

- `<spec-or-unified-spec>`: Single spec file path, or unified spec from Wave 1A (if combined mode)
- `--generate roadmap`: Fixed value — tells sc:adversarial what artifact type to generate
- `<expanded-agent-specs>`: Agent specs after expansion (model-only agents filled with primary persona)
- `<roadmap-depth>`: Value of sc:roadmap's `--depth` flag
- `<roadmap-output-dir>`: sc:roadmap's resolved output directory
- `--interactive`: Present only when sc:roadmap's `--interactive` flag is set

**Example invocations**:

```text
# 3 agents, standard depth (after persona expansion to "security")
Skill sc:adversarial-protocol args: "--source spec.md --generate roadmap --agents opus:security,sonnet:security,gpt52:security --depth standard --output .dev/releases/current/auth-system/"

# 5+ agents triggers orchestrator (orchestrator added automatically by sc:adversarial)
Skill sc:adversarial-protocol args: "--source spec.md --generate roadmap --agents opus:architect,sonnet:security,gpt52:backend,haiku:frontend,gemini:performance --depth deep --output .dev/releases/current/platform/ --interactive"
```

### Combined Mode

When both `--specs` and `--multi-roadmap --agents` are present:

1. Wave 1A: Invoke Skill `sc:adversarial-protocol` for multi-spec consolidation → produces unified spec
2. Wave 1B: Extract from unified spec (standard pipeline)
3. Wave 2: Invoke Skill `sc:adversarial-protocol` for multi-roadmap generation with unified spec as `--source`

The unified spec from Wave 1A becomes the `--source` input for Wave 2's multi-roadmap invocation.

---

## --resume-from Interaction

The `--resume-from` flag allows sc:roadmap to bypass sc:adversarial Skill invocation and consume a pre-existing return contract from a specified directory. This enables testing of consumer-side error handling without requiring a live adversarial pipeline.

### Flag Validation Rules

Validated in Wave 0 (step 7):

1. **Requires adversarial mode**: `--specs` or `--multi-roadmap` must also be present. If neither: abort with `"--resume-from requires --specs or --multi-roadmap."`
2. **Incompatible with --dry-run**: If `--dry-run` present: abort with `"--resume-from is incompatible with --dry-run."`
3. **Directory must exist**: Specified path must be a valid directory. If not: abort with `"--resume-from directory not found: <path>"`
4. **Contract must exist**: `return-contract.yaml` must exist in the directory. If not: abort with `"return-contract.yaml not found in --resume-from directory: <path>"`

### Consumption Path

When `--resume-from` is active, the return contract is consumed via the **file-fallback path** (same as line 164 of this document). Specifically:

- **Wave 1A** (if `--specs` present): Skip steps 2a-2d (Skill invocation). Read `<resume-from-dir>/return-contract.yaml` via Read tool. Proceed to step 2e with file-based contract.
- **Wave 2** (if `--multi-roadmap` present): Skip steps 3a-3d. Read `<resume-from-dir>/return-contract.yaml` via Read tool. Proceed to step 3e with file-based contract.

The Tier 1 Artifact Existence Gate still applies — all 4 checks are executed against the `--resume-from` directory before contract parsing.

### Session Persistence Behavior

When `--resume-from` is active, skipped waves are not recorded in session persistence. The `last_completed_wave` field reflects only waves that actually executed. This means resuming a `--resume-from` session will re-read the fixture directory (idempotent).

### Incompatibilities

| Flag | Interaction |
|------|------------|
| `--dry-run` | Incompatible — abort in Wave 0 |
| `--interactive` | Compatible — interactive prompts still fire for convergence thresholds |
| `--depth` | Ignored when `--resume-from` active (no Skill invocation to propagate depth to) |
| `--agents` | Parsed and validated but not used for Skill invocation (agents are relevant for frontmatter recording only) |

---

## Post-Adversarial Artifact Existence Gate (Tier 1)

**Position**: Execute this gate BEFORE parsing any return contract data. This ensures the adversarial pipeline produced usable artifacts before attempting YAML consumption.

**Checks** (execute in order; fail-fast on any check failure):

| # | Check | Path | Failure Treatment |
|---|-------|------|-------------------|
| 1 | Adversarial output directory exists | `<artifacts_dir>/` | Treat as `status: failed, failure_stage: transport`. Log: `"Adversarial artifacts directory not found at <artifacts_dir>/"` |
| 2 | diff-analysis.md exists | `<artifacts_dir>/diff-analysis.md` | Treat as `status: partial, failure_stage: debate`. Log: `"diff-analysis.md missing — debate may not have completed."` |
| 3 | merged-output.md exists | `<artifacts_dir>/merged-output.md` | Treat as `status: partial, failure_stage: merge`. Log: `"merged-output.md missing — merge may not have completed."` |
| 4 | return-contract.yaml exists | `<artifacts_dir>/return-contract.yaml` | Treat as `status: failed, failure_stage: transport`. Log: `"return-contract.yaml missing — cannot consume adversarial results."` |

**Path variables**: `<artifacts_dir>` is the adversarial output directory passed via the return contract or inferred from the `--output` flag as `<output_dir>/adversarial/`.

If all 4 checks pass, proceed to Return Contract Consumption below.

---

## Return Contract Consumption

sc:adversarial returns a structured result as an inline Skill response. sc:roadmap reads the return contract and consumes the following fields. The return contract schema is defined in sc:adversarial-protocol SKILL.md "Return Contract (MANDATORY)" section; this section documents how sc:roadmap consumes each field.

**Read instruction**: After the Tier 1 gate passes, read the inline Skill return value. If consuming from a file fallback, read `<artifacts_dir>/return-contract.yaml` via the Read tool.

**Schema version validation**: Verify the return contract contains all 9 expected fields. If any field is missing, apply the consumer defaults below. Log a warning for each missing field.

### Return Fields

| Field | Type | Consumer Default | Usage in sc:roadmap |
|-------|------|-----------------|---------------------|
| `status` | `success` \| `partial` \| `failed` | `"failed"` | Routes to handling branch (see Status Routing below) |
| `merged_output_path` | `string\|null` | `null` | Used as input for subsequent waves |
| `convergence_score` | `float 0.0-1.0\|null` | `0.5` (forces Partial path) | Recorded in roadmap.md frontmatter; used for threshold routing |
| `artifacts_dir` | `string` | (inferred from `--output`) | Recorded in roadmap.md frontmatter for traceability |
| `base_variant` | `string\|null` | `null` | Recorded in roadmap.md frontmatter (multi-roadmap mode only) |
| `unresolved_conflicts` | `integer` | `0` | If >0, logged as warning in extraction.md |
| `fallback_mode` | `boolean` | `false` | If true, emit differentiated warning (see below) |
| `failure_stage` | `string\|null` | `null` | Logged for debugging when status is `failed` |
| `invocation_method` | `enum` | `"skill-direct"` | Logged in extraction.md for observability |

### Status Routing

```text
status == "success"
  → Use merged_output_path as input for subsequent waves
  → Record convergence_score, artifacts_dir, base_variant in frontmatter
  → Proceed normally

status == "partial"
  → Check convergence_score:
    ≥ 0.6 (60%):
      → Proceed with warning logged in extraction.md:
        "Adversarial consolidation partial (convergence: XX%). Some conflicts unresolved."
      → Record convergence_score, artifacts_dir, base_variant in frontmatter
      → Use merged_output_path as input
    < 0.6 (60%):
      → If --interactive flag set:
        → Prompt user: "Adversarial convergence is XX% (below 60% threshold).
           Proceed anyway? [Y/n]"
        → If user approves: proceed as ≥60% path
        → If user declines: abort
      → If --interactive not set:
        → Abort with message: "Adversarial convergence XX% is below 60% threshold.
           Use --interactive to approve low-convergence results, or revise specifications."

status == "failed"
  → Abort roadmap generation
  → Error message includes:
    - "sc:adversarial failed (failure_stage: <failure_stage>). Roadmap generation aborted."
    - unresolved_conflicts count (if present)
    - artifacts_dir (if present, for debugging)
    - Recommendation: "Review adversarial artifacts at <artifacts_dir> for details."
```

### Fallback Mode Warning

When `fallback_mode == true` (regardless of status), emit a differentiated warning:

```text
> **Warning**: Adversarial result was produced via fallback path (not primary Skill invocation).
> Quality may be reduced. Review the merged output manually before proceeding.
```

This warning is additional to any status-based handling and is logged in extraction.md.

### Unresolved Conflicts Handling

When `unresolved_conflicts > 0` (regardless of status), log warning in extraction.md:

```text
> **Warning**: Adversarial consolidation produced N unresolved conflicts.
> Review artifacts at <artifacts_dir> for conflict details.
```

### Example Return Contract

```yaml
# Success case
return_contract:
  merged_output_path: ".dev/releases/current/auth-system/adversarial/merged-output.md"
  convergence_score: 0.82
  artifacts_dir: ".dev/releases/current/auth-system/adversarial/"
  status: "success"
  base_variant: "opus:architect"
  unresolved_conflicts: 0
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
```

```yaml
# Failure case
return_contract:
  merged_output_path: null
  convergence_score: null
  artifacts_dir: ".dev/releases/current/auth-system/adversarial/"
  status: "failed"
  base_variant: null
  unresolved_conflicts: 0
  fallback_mode: false
  failure_stage: "debate"
  invocation_method: "skill-direct"
```

---

## Divergent-Specs Heuristic

**Trigger**: convergence_score < 50% (regardless of status)

**Action**: Emit warning message:

```text
"Specifications may be too divergent for meaningful consolidation.
Consider running separate roadmaps or using --interactive for manual conflict resolution."
```

This warning is in addition to any status-based handling. It fires even if convergence is 50-59% and --interactive is used to proceed — the warning alerts the user that the consolidated result may be low quality.

**Recording**: The warning is logged in extraction.md under a "Consolidation Warnings" section.

---

## Frontmatter Population

When adversarial mode is used, the `adversarial` block in roadmap.md frontmatter is populated from the return contract fields:

```yaml
adversarial:
  mode: <multi-spec|multi-roadmap|combined>    # From mode detection
  agents: [<agent-spec-1>, <agent-spec-2>]     # From --agents flag (expanded form)
  convergence_score: <0.0-1.0>                 # From return contract
  base_variant: <model:persona>                # From return contract (multi-roadmap only)
  artifacts_dir: <path>                        # From return contract
```

**Population rules**:

- `mode`: Set based on mode detection logic (see above)
- `agents`: List of expanded agent specs (after model-only expansion). For multi-spec mode, this is the implicit agents used by sc:adversarial (typically 2 advocate agents)
- `convergence_score`: Direct copy from return contract
- `base_variant`: Present only in multi-roadmap and combined modes. Set from return contract's `base_variant` field (the variant that won the adversarial debate)
- `artifacts_dir`: Direct copy from return contract. Path to directory containing adversarial debate artifacts

**When adversarial mode is NOT used**: The `adversarial` block is completely absent from frontmatter (not present with null values — entirely omitted).

---

## Error Handling

### Adversarial Skill Not Installed

**Condition**: `--specs` or `--multi-roadmap` flag present, but `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` not found.

**Action**: Abort in Wave 0 with:

```text
"sc:adversarial skill not installed. Required for --specs/--multi-roadmap flags.
Install via: superclaude install"
```

### Unknown Model Identifier

**Condition**: `--multi-roadmap` flag present, and a model identifier in `--agents` is not recognized.

**Action**: Abort in Wave 0 with:

```text
"Unknown model '<model>' in --agents. Available models: opus, sonnet, haiku, gpt52, gemini, ..."
```

### Agent Count Out of Range

**Condition**: Agent list has fewer than 2 or more than 10 entries.

**Action**: Abort in Wave 0 with:

```text
"Agent count must be 2-10. Provided: N"
```

### sc:adversarial Invocation Failure

**Condition**: sc:adversarial invocation fails (not a status response, but a skill-level failure).

**Action**: Abort with:

```text
"sc:adversarial invocation failed. Check that the skill is properly installed and configured."
```

---

## --interactive Flag Propagation

The `--interactive` flag on sc:roadmap propagates to sc:adversarial invocations in both adversarial paths:

| sc:roadmap invocation | Propagation |
|----------------------|-------------|
| `--specs` (Wave 1A) | `--interactive` appended to `Skill sc:adversarial-protocol` args for `--compare` invocation |
| `--multi-roadmap` (Wave 2) | `--interactive` appended to `Skill sc:adversarial-protocol` args for `--source --generate` invocation |
| Combined mode | `--interactive` appended to both invocations |

**Behavioral impact**:

- When `--interactive` is set: sc:adversarial prompts for user approval at decision points; sc:roadmap prompts at convergence <60% threshold
- When `--interactive` is NOT set: sc:adversarial uses auto-resolution; sc:roadmap aborts at convergence <60% threshold

**Flag presence rule**: Only append `--interactive` to sc:adversarial invocation when `--interactive` is explicitly set on sc:roadmap. Default (no flag) means no propagation.

---

*Reference document for sc:roadmap v2.0.0 — loaded on-demand during Wave 1A and/or Wave 2.*

*CLI parity baseline (B-8, VERIFIED): the canonical debate behavior is the inline `Step(id="debate", ...)` built by `build_debate_prompt` (`src/superclaude/cli/roadmap/prompts.py:878-902`) with depth control via `_DEPTH_INSTRUCTIONS` (`prompts.py:18-37`), wired at `src/superclaude/cli/roadmap/executor.py:2076-2084` and gated by `DEBATE_GATE` (`src/superclaude/cli/roadmap/gates.py:1155-1166`). The Skill-delegation material from "Mode Detection" through "--interactive Flag Propagation" describes the inference-only delegation mode (SKILL-DIRECT per D-0001 reversal) and is not implemented by the canonical CLI.*
