# Tasklist: Add `--agents` Mode B to sc:release-split

> **Source**: `docs/generated/release-split-agents-refactor-plan.md`
> **Compliance**: STRICT (`sc:task-unified --compliance strict`)
> **Date**: 2026-03-17
> **Branch**: `v3.0-AuditGates` (current) — implement on a feature branch if merging to master

---

## Context

Refactor `sc:release-split` Part 2 from `sc:adversarial` Mode A (compare two documents) to Mode B (generate independent agent variants then merge). Adds `--agents` flag with default `opus:architect,haiku:analyzer`. Six reflection findings have been incorporated into the plan; all changes must be applied together for coherence.

**Files touched**:
- `src/superclaude/commands/release-split.md`
- `src/superclaude/skills/sc-release-split-protocol/SKILL.md`
- `src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md` *(new)*
- `src/superclaude/skills/sc-release-split-protocol/refs/phase-templates.md`
- `.claude/` (via `make sync-dev`)

---

## Phase 1 — Command File (`release-split.md`)

### Task 1.1 — Add `--agents` flag to Options table

**File**: `src/superclaude/commands/release-split.md`

**Action**: Insert the following row after the `--smoke-gate` row in the Options table:

```markdown
| `--agents` | `-a` | No | `opus:architect,haiku:analyzer` | Agent specs for variant generation in Part 2. Format: `model[:persona[:"instruction"]]`, comma-separated. Minimum 2 agents. |
```

**Verification**: Options table contains `--agents` row with correct default and format description.

---

### Task 1.2 — Add `--agents` usage examples

**File**: `src/superclaude/commands/release-split.md`

**Action — Usage section**: Insert after the `--no-split` example:

```bash
# Custom agents for adversarial variant generation
/sc:release-split path/to/release-spec.md --agents opus:architect,sonnet:security

# With custom instructions per agent
/sc:release-split path/to/release-spec.md \
  --agents opus:architect:"Focus on dependency isolation",haiku:analyzer:"Prioritize testability"
```

**Action — Examples section**: Add new example block at the end:

```markdown
### Multi-Agent Split Analysis
```bash
/sc:release-split .dev/releases/current/v4.0/spec.md \
  --agents opus:architect,sonnet:security --depth deep
```
```

**Verification**: Both usage section and examples section contain `--agents` demonstrations.

---

### Task 1.3 — Update Behavioral Summary

**File**: `src/superclaude/commands/release-split.md`

**Action**: Replace in the Behavioral Summary paragraph:

- **Find**: `Part 2 (adversarial validation via \`/sc:adversarial\` — stress-test the proposal)`
- **Replace**: `Part 2 (adversarial variant generation and validation via \`/sc:adversarial\` Mode B — independent agents generate competing split proposals, then debate and merge)`

**Verification**: Behavioral Summary no longer mentions "stress-test the proposal" for Part 2.

---

### Task 1.4 — Update Related Commands table

**File**: `src/superclaude/commands/release-split.md`

**Action**: In the Related Commands table, find the `/sc:adversarial` row and change the Integration cell from:

- **Find**: `Stress-test split proposal`
- **Replace**: `Generate competing split variants and merge via adversarial debate`

**Verification**: `/sc:adversarial` row description updated.

---

## Phase 2 — SKILL.md

### Task 2.1 — Add `--agents` to argument-hint frontmatter

**File**: `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

**Action**: In the YAML frontmatter, change `argument-hint` value by appending ` [--agents agent-specs]` to the end of the existing string.

**Before** (end of string): `[--smoke-gate r1|r2]"`
**After** (end of string): `[--smoke-gate r1|r2] [--agents agent-specs]"`

**Verification**: `argument-hint` in frontmatter ends with `[--agents agent-specs]`.

---

### Task 2.2 — Add `--agents` handling block to Section 3

**File**: `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

**Action**: After the WARN conditions block in Section 3 (Required Input), insert:

```markdown
**`--agents` handling**: Optional. Comma-separated agent specs in `model[:persona[:"instruction"]]` format.
- Default: `opus:architect,haiku:analyzer`
- Minimum 2 agents, maximum 10
- When present, Part 2 uses sc:adversarial Mode B (generate + compare) instead of Mode A (compare)
- Agent spec parsing follows the canonical algorithm defined in sc:adversarial-protocol SKILL.md "Dual Input Modes > Mode B" section
```

**Verification**: Section 3 documents `--agents` flag with default and parsing reference.

---

### Task 2.3 — Add `Dispatch Task agent` to Execution Vocabulary

**File**: `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

**Action**: In the Execution Vocabulary table (Section 4), add a new row:

```markdown
| Dispatch Task agent | `Task` | Parallelized sub-agent work (agent variant generation) |
```

**Verification**: Execution Vocabulary table contains `Task` tool row.

---

### Task 2.4 — Add Prerequisites phase before Part 1

**File**: `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

**Action**: Insert the following block between the Execution Vocabulary table and `### Part 1: Discovery & Proposal`:

```markdown
### Prerequisites (before Part 1)

**Purpose**: Validate environment and inputs before expensive work begins. Fail fast before any delegation occurs.

**Behavioral Instructions**:

1. Validate spec file exists and is readable (Read tool). If empty (0 bytes), STOP: "Specification file is empty." If < 5 lines, WARN but proceed.
2. Validate output directory is writable; create if needed.
3. If `--agents` provided:
   - Parse agent specs using the canonical algorithm from sc:adversarial-protocol SKILL.md
   - Validate agent count: 2-10. If out of range, STOP: "Agent count must be 2-10. Provided: N"
   - Validate model identifiers are recognized. If unknown, STOP: "Unknown model '<model>' in --agents."
4. Verify `sc:adversarial-protocol` SKILL.md exists at `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`. If not found, STOP: "sc:adversarial skill not installed. Required for Part 2. Install via: superclaude install"
5. If `--resume-from` provided: validate the file exists and is readable.
6. Log all validation results.

**Exit Criteria**: All prerequisites validated. Emit: "Prerequisites validated."
```

Also update the Phase Architecture diagram (the code block listing the 4 parts) to include the new phase:

```
Prerequisites: Validate inputs           → (inline)
Part 1: Discovery & Proposal             → /sc:brainstorm
Part 2: Adversarial Variant Generation   → /sc:adversarial (Mode B)
Part 3: Execution                        → /sc:design | /sc:workflow | /sc:tasklist
Part 4: Fidelity Verification            → /sc:analyze
```

**Verification**: Prerequisites phase block present before Part 1. Phase diagram shows 5 lines including Prerequisites.

---

### Task 2.5 — Rewrite Part 2 section (Mode B)

**File**: `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

**Action**: Replace the entire `### Part 2: Adversarial Validation` section (from the `### Part 2` heading through its `**Checkpoint**` line, inclusive) with:

```markdown
### Part 2: Adversarial Variant Generation & Validation

**Purpose**: Generate independent competing split proposals from different analytical perspectives, then debate and merge them. This is not a rubber-stamp exercise.

**Entry Criteria**: `split-proposal.md` exists in output directory. Prerequisites phase has validated agent specs and sc:adversarial availability.

**Delegation**: Invoke Skill `sc:adversarial-protocol` in Mode B (generate + compare).

**Refs Loaded**: Read `refs/phase-templates.md` for debate structure guidance. Read `refs/adversarial-integration.md` for invocation pattern and return contract consumption.

**Agent Default**: If `--agents` not provided, use `opus:architect,haiku:analyzer`.

**Behavioral Instructions**:

1. Read the proposal from Part 1 (Read tool). Extract a concise summary (the "prior analysis context").
2. Agent specs were already parsed and validated in Prerequisites. Retrieve the parsed result.
3. Build agent instructions incorporating Part 1 context. For each agent, prepend the context injection template from `refs/adversarial-integration.md` to any user-provided instruction.
4. Invoke Skill `sc:adversarial-protocol` with:
   - `--source <original-spec-path>`
   - `--generate spec`
   - `--agents <parsed-agent-specs-with-instructions>`
   - `--depth` propagated from command
   - `--interactive` propagated if set
5. The adversarial pipeline executes:
   - **Variant generation** (parallel): Each agent independently analyzes the source spec and generates a split proposal
   - **Diff analysis**: Structural and content differences between variants
   - **Debate**: Agents debate their positions (rounds based on `--depth`)
   - **Scoring & merge**: Best elements selected and merged into final proposal
6. Parse the adversarial return contract for all 9 fields (see `refs/adversarial-integration.md` Return Contract Consumption):
   - `status` — success/partial/failed
   - `merged_output_path` — the merged split proposal
   - `convergence_score` — agent agreement level
   - `artifacts_dir` — location of debate artifacts
   - `base_variant` — which agent's proposal was selected as base
   - `unresolved_conflicts` — count of unresolved disagreements
   - `fallback_mode` — whether adversarial used its own fallback
   - `failure_stage` — where failure occurred (if failed)
   - `invocation_method` — how adversarial was invoked
7. Apply convergence routing (aligned with sc:roadmap thresholds):
   - `convergence_score >= 0.6` → PASS: proceed with merged proposal
   - `convergence_score 0.5-0.59` → PARTIAL: if `--interactive`, prompt user to confirm or abort. If not `--interactive`, abort: "Adversarial convergence XX% is below 60% threshold. Use --interactive to approve low-convergence results."
   - `convergence_score < 0.5` → FAIL: abort with "Adversarial pipeline failed (convergence: X.XX). Agent proposals too divergent for reliable merge."
8. If `fallback_mode == true`: emit warning in `split-proposal-final.md`: "Adversarial result produced via fallback path. Review merged output manually."
9. If `unresolved_conflicts > 0`: log warning: "Adversarial merge produced N unresolved conflicts. Review artifacts at <artifacts_dir>."
10. Route on verdict from merged output:
    - If merged proposal recommends **SPLIT**: Write as `split-proposal-final.md`
    - If merged proposal recommends **SPLIT-WITH-MODIFICATIONS**: Write with modifications as `split-proposal-final.md`
    - If merged proposal recommends **DON'T SPLIT**: Write no-split recommendation as `split-proposal-final.md`
11. Record adversarial metadata in `split-proposal-final.md` frontmatter:
    ```yaml
    adversarial:
      agents: [<expanded-agent-specs>]
      convergence_score: <score>
      base_variant: <model:persona>
      artifacts_dir: <path>
      unresolved_conflicts: <count>
      fallback_mode: <bool>
    ```

**Fallback** (Mode B invocation failure):
- If sc:adversarial Mode B fails, retry once with `--depth quick`.
- If retry also fails, fall back to Mode A:
  - `--compare split-proposal.md,<original-spec>`
  - Emit warning: "Agent variant generation failed. Falling back to document comparison mode."
  - Resume Mode A behavior (conceptual roles, not agent-backed)

**Output**: Write verdict and final proposal to `<output>/split-proposal-final.md`

**Exit Criteria**: Final proposal written with adversarial verdict, convergence score, and frontmatter metadata.

**Checkpoint**: If `--interactive`, present the verdict and ask: "The adversarial review concluded [VERDICT] (convergence: X.XX). Should I proceed to execution, or would you like to discuss the findings?"
```

**Verification**: Part 2 section title reads "Adversarial Variant Generation & Validation". Mentions `--generate spec`. Lists 11 behavioral instructions. Contains 9-field return contract parse. Convergence thresholds are 0.6/0.5/0.5. Fallback includes retry step.

---

### Task 2.6 — Add Mode B error rows to Section 7

**File**: `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

**Action**: In Section 7 (Error Handling), add these rows to the existing error handling table:

```markdown
| Agent model unavailable | Retry with --depth quick, then fall back to Mode A with warning |
| Agent count out of range (< 2 or > 10) | STOP in Prerequisites: "Agent count must be 2-10. Provided: N" |
| Mode B generation failure | Retry once with --depth quick. If retry fails, fall back to Mode A |
| Low convergence (0.5-0.59) without --interactive | STOP: "Convergence XX% below threshold. Use --interactive to approve." |
| Low convergence (< 0.5) | STOP regardless of --interactive: "Agent proposals too divergent." |
| Return contract unparseable | Use fallback convergence_score: 0.5, route to PARTIAL path |
| Merged output file missing on disk | Treat as failed, fall back to Mode A |
```

**Verification**: Error handling table contains all 7 new rows.

---

## Phase 3 — New ref file (`refs/adversarial-integration.md`)

### Task 3.1 — Create `refs/adversarial-integration.md`

**File**: `src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md` *(create new)*

**Action**: Write the following content:

```markdown
# Adversarial Integration Reference — Release Split Protocol

Reference document for sc:adversarial integration within sc:release-split.
Contains invocation patterns, return contract consumption, convergence routing,
and error handling specific to the release-split context.

**Loaded in**: Part 2 (when adversarial variant generation executes).

---

## Agent Specification Parsing

Follow the canonical Agent Specification Parsing algorithm defined in
sc:adversarial-protocol SKILL.md under "Dual Input Modes > Mode B".

The format is `model[:persona[:"instruction"]]`:
- Split `--agents` value on `,` for individual specs
- Per agent: split on `:` (max 3 segments) → model, persona, instruction
- Quoted second segment = instruction (no persona)
- Validation: 2-10 agents, all models recognized

For full parsing rules, edge cases, and validation error messages, refer to
the canonical source. Do NOT duplicate the algorithm here.

## Default Agent Configuration

When `--agents` is not provided:

| Agent | Model | Persona | Analytical Focus |
|-------|-------|---------|-----------------|
| 1 | opus | architect | Structural boundaries, dependency chains, foundation-vs-application seams, integration points |
| 2 | haiku | analyzer | Risk assessment, cost-benefit analysis, validation feasibility, coordination overhead |

These defaults are chosen because:
- **opus:architect** brings deep structural reasoning — it excels at identifying
  natural seams in complex systems and evaluating dependency chains
- **haiku:analyzer** brings fast, focused risk analysis — it challenges assumptions
  and evaluates whether the split actually enables better testing

## Invocation Pattern

Mode B invocation for split proposal generation:

```
Invoke Skill `sc:adversarial-protocol` with args:
  --source <original-spec-path>
  --generate spec
  --agents <agent-spec-1>,<agent-spec-2>[,...]
  --depth <propagated>
  --interactive <propagated if set>
```

**Important**: Use `--generate spec` (not `--generate split-proposal`). The artifact
type `spec` is a recognized sc:adversarial type. The agent instruction context
(below) shapes the output as a split proposal — the `--generate` value only
controls artifact labeling.

## Context Injection Template

Each agent receives this preamble prepended to their instruction:

```
You are analyzing a release spec to determine if and where it should
be split into two sequential releases. A prior discovery analysis
produced this proposal:

---
[Part 1 proposal summary]
---

You may agree or disagree. Generate your own independent analysis.
Your output MUST include:
1. Recommendation: Split or Don't Split (with confidence 0.0-1.0)
2. If split: Release 1 scope, Release 2 scope, seam rationale,
   real-world validation plan
3. If don't split: rationale, alternative strategies
4. Risks of your recommendation

Global constraints that apply regardless of your recommendation:
- Release 1 defaults to planning fidelity and schema hardening
  unless you provide compelling evidence otherwise
- Smoke gate belongs in Release 2 by default
- All validation must be real-world (no mocks, no synthetic tests)
- "Don't split" is always a valid conclusion
```

## Return Contract Consumption

Parse all 9 fields from the sc:adversarial return contract:

| Field | Type | Consumer Default | Usage in sc:release-split |
|-------|------|-----------------|--------------------------|
| `status` | `success` \| `partial` \| `failed` | `"failed"` | Routes to convergence handling or fallback |
| `merged_output_path` | `string\|null` | `null` | Read merged proposal for verdict extraction |
| `convergence_score` | `float 0.0-1.0\|null` | `0.5` (forces Partial path) | Report in checkpoint; drives convergence routing |
| `artifacts_dir` | `string` | (inferred from `--output`) | Location of debate transcript and scoring artifacts |
| `base_variant` | `string\|null` | `null` | Recorded in split-proposal-final.md frontmatter |
| `unresolved_conflicts` | `integer` | `0` | If > 0, logged as warning |
| `fallback_mode` | `boolean` | `false` | If true, emit differentiated warning |
| `failure_stage` | `string\|null` | `null` | Logged for debugging when status is failed |
| `invocation_method` | `enum` | `"skill-direct"` | Logged for observability |

**Missing-file guard**: After extracting `merged_output_path`, verify the file exists
on disk (Read tool). If missing, treat as `status: failed, failure_stage: transport`.

## Convergence Routing

Thresholds aligned with sc:roadmap for cross-skill consistency:

| Score | Action |
|-------|--------|
| >= 0.6 | PASS — proceed with merged proposal |
| 0.5 - 0.59 | PARTIAL — if `--interactive`, prompt user to confirm or abort. If not `--interactive`, abort: "Convergence XX% below 60% threshold." |
| < 0.5 | FAIL — abort: "Agent proposals too divergent (convergence: X.XX)." |

## Fallback Mode Warning

When `fallback_mode == true` (regardless of status), emit:
```
> **Warning**: Adversarial result produced via fallback path (not primary Skill invocation).
> Quality may be reduced. Review the merged output manually before proceeding.
```

## Error Handling

| Failure | Action |
|---------|--------|
| sc:adversarial Skill tool error | Retry once with --depth quick. If retry fails, fall back to Mode A |
| Agent model unavailable | Fall back to Mode A with warning |
| Return contract unparseable | Use fallback convergence_score: 0.5, route to PARTIAL |
| Merged output file missing | Treat as failed, fall back to Mode A |
| convergence_score < 0.5 | Abort regardless of --interactive flag |
```

**Verification**: File exists. Contains sections: Agent Specification Parsing (with reference, no copy), Default Agent Configuration, Invocation Pattern (uses `--generate spec`), Context Injection Template, Return Contract Consumption (9 fields), Convergence Routing (0.6/0.5 thresholds), Error Handling.

---

## Phase 4 — Update `refs/phase-templates.md`

### Task 4.1 — Replace Role Specifications with Mode B mapping

**File**: `src/superclaude/skills/sc-release-split-protocol/refs/phase-templates.md`

**Action**: In the "Part 2: Adversarial Debate Structure" section, replace the entire "### Role Specifications" subsection (from `### Role Specifications` through the closing Pragmatist description) with:

```markdown
### Role Mapping (Mode B)

With Mode B variant generation, the debate roles map differently than in Mode A:

| Concern | How It's Addressed |
|---------|-------------------|
| Advocacy | Each agent's generated variant IS its advocacy — the variant embodies the agent's best analysis |
| Skepticism | The adversarial pipeline's diff analysis and debate rounds surface disagreements between variants |
| Pragmatism | The scoring and merge phase evaluates variants against hard criteria (real-world testability, overhead justification, coupling risks) |

The three conceptual roles (Advocate, Skeptic, Pragmatist) are now **emergent properties** of the adversarial pipeline rather than explicitly assigned positions. This produces more genuine disagreement because each agent commits to its full analysis rather than arguing a pre-assigned position.

### Agent-Specific Guidance

When building agent instructions, bias each agent toward its persona's strength:

| Agent Persona | Bias Toward | Key Questions to Emphasize |
|--------------|-------------|---------------------------|
| architect | Structural analysis | "Where are the natural module boundaries? What are the dependency chains? Is there a foundation-vs-application seam?" |
| analyzer | Risk and feasibility | "What are the real costs of splitting? Does Release 1 actually enable tests that matter? What coupling risks exist?" |
| security | Trust boundaries | "Does the split create new attack surfaces? Are auth/access changes atomic or split across releases?" |
| qa | Validation quality | "Can Release 1 be meaningfully tested in isolation? Are the test scenarios real-world or synthetic?" |

### Fallback Role Specifications (Mode A)

If Mode B fails and the skill falls back to Mode A, use these conceptual roles:

**Advocate** (argues FOR the proposal): [keep existing Advocate content]

**Skeptic** (argues AGAINST the proposal): [keep existing Skeptic content]

**Pragmatist** (evaluates both positions): [keep existing Pragmatist content]
```

**Verification**: "Role Mapping (Mode B)" table present. "Agent-Specific Guidance" table present. Original Advocate/Skeptic/Pragmatist text preserved under "Fallback Role Specifications (Mode A)".

---

## Phase 5 — Sync & Verify

### Task 5.1 — Sync src/ to .claude/

**Action**: Run `make sync-dev` from the repo root.

**Expected output**: "Sync complete. Skills: 13 directories, Agents: 27 files, Commands: 40 files" (or similar counts — skills count may increase by 1 if new ref is counted).

**Verification**: `.claude/skills/sc-release-split-protocol/refs/adversarial-integration.md` exists. `.claude/skills/sc-release-split-protocol/SKILL.md` is updated.

---

### Task 5.2 — Verify sync

**Action**: Run `make verify-sync` from the repo root.

**Expected output**: No new drift detected beyond the known pre-existing drift (sc-forensic-qa-protocol missing in .claude, skill-creator not in src/).

**Verification**: `make verify-sync` exits without reporting drift for any of the modified files.

---

## Execution Order & Dependencies

```
Phase 1 (Tasks 1.1-1.4)  →  independent, can run in any order within phase
Phase 2 (Tasks 2.1-2.6)  →  2.4 must precede 2.5 (prereqs phase inserted before Part 2 section)
                            2.6 can run in any order relative to 2.1-2.5
Phase 3 (Task 3.1)       →  independent of Phase 2 (new file, no edit dependencies)
Phase 4 (Task 4.1)       →  independent of Phases 2-3
Phase 5 (Tasks 5.1-5.2)  →  must follow ALL of Phases 1-4
```

**Safe parallel execution**: Phases 1, 2, 3, and 4 can run in parallel. Phase 5 gates on all preceding phases.

---

## Acceptance Criteria

All tasks complete when:

1. `/sc:release-split spec.md` (no `--agents`) invokes Mode B with `opus:architect,haiku:analyzer` by default
2. `/sc:release-split spec.md --agents opus:architect,sonnet:security` is accepted and validated in Prerequisites
3. Invalid agent specs (`--agents badmodel:architect`) are caught in Prerequisites with a clear error, before any work runs
4. Part 2 invokes `sc:adversarial-protocol` with `--source`, `--generate spec`, and `--agents`
5. Convergence thresholds match sc:roadmap: PASS ≥ 0.6, PARTIAL 0.5-0.59 (interactive gate), FAIL < 0.5
6. All 9 return contract fields are consumed; `fallback_mode` and `unresolved_conflicts` produce warnings
7. Mode B failure falls back to Mode A with a warning
8. `make verify-sync` passes without new drift
