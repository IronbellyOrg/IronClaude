# Refactor Plan: Add `--agents` Mode B Generation to sc:release-split

> **Status**: Proposed — not yet implemented
> **Author**: Claude (from /sc:brainstorm analysis)
> **Date**: 2026-03-17
> **Reviewed**: 2026-03-17 via /sc:reflect — 6 findings addressed (see Appendix A)
> **Scope**: Command + SKILL.md + refs/phase-templates.md + new ref file + prerequisites phase

---

## 1. Problem Statement

Part 2 of sc:release-split currently uses `sc:adversarial` in **Mode A** (`--compare`), passing the split proposal and original spec as two existing files. The three debate roles (Advocate, Skeptic, Pragmatist) are described conceptually but not mapped to actual sc:adversarial agent specs.

This means:
- The "adversarial" debate is really just comparing two documents, not generating independent competing analyses
- There's no multi-model diversity — the same context produces one perspective
- The debate roles exist only as framing, not as separate agents with distinct reasoning strategies

## 2. Proposed Change

Switch Part 2 from Mode A (`--compare`) to **Mode B** (`--source --generate --agents`). Each agent independently generates a split proposal from the original spec, and the adversarial pipeline diffs, debates, and merges them.

**Default agents**: `opus:architect,haiku:analyzer`
- `opus:architect` — focuses on structural boundaries, dependency chains, foundation-vs-application seams
- `haiku:analyzer` — focuses on risk assessment, cost-benefit analysis, validation feasibility

The Part 1 brainstorm proposal becomes **injected context** for the agents (informing but not constraining their independent analysis), rather than one of the compared files.

## 3. Design Decisions

### D1: Part 2 only, not Part 1

Part 1 (brainstorm) stays unchanged. It provides the neutral "should we split at all?" framing. The agent-generated variants in Part 2 build on that framing but are free to disagree with it.

**Rationale**: Mode B assumes it will generate artifacts — it doesn't naturally produce a "don't split" recommendation. The brainstorm handles the neutral framing, and agents can incorporate the brainstorm's conclusion as context while reaching independent conclusions.

### D2: `--agents` flag with sensible default

The `--agents` flag is optional. When omitted, the skill uses `opus:architect,haiku:analyzer` as the default. This means the current invocation (`/sc:release-split spec.md`) still works without changes — it just produces better adversarial output.

### D3: Agent instructions carry Part 1 context

Each agent receives the Part 1 proposal summary as instruction context. This grounds the agent's analysis without constraining it. The agents may agree or disagree with the brainstorm.

### D4: Fallback to Mode A when agents unavailable

If Mode B invocation fails (e.g., model not available, agent generation errors), fall back to the current Mode A behavior with a warning. This preserves the existing capability as a safety net.

### D5: Parallelism is built-in

Mode B variant generation in sc:adversarial already runs agents as parallel Task calls. No additional parallelism work is needed in sc:release-split.

### D6: Use `--generate spec` not `--generate split-proposal` *(from reflection Finding 3)*

sc:adversarial's `--generate` flag expects recognized artifact types (`roadmap`, `spec`, `design`, etc.). The value `split-proposal` is not a recognized type and may cause runtime failure if sc:adversarial validates against a known list.

**Resolution**: Use `--generate spec` and rely on the agent instruction context to shape the output as a split proposal. The context injection template (Section 4.3) already tells each agent exactly what to produce. The `--generate` type only controls artifact labeling, not content — the agent instructions are what actually determine output structure.

### D7: Align convergence thresholds with sc:roadmap *(from reflection Finding 4)*

The original plan used 0.7/0.5 thresholds. The roadmap uses 0.6/0.5. Using different thresholds across skills creates confusion without justification.

**Resolution**: Adopt the roadmap's thresholds (>= 0.6 PASS, 0.5-0.59 PARTIAL with interactive gate, < 0.5 FAIL/abort). The release-split context does not warrant more lenient thresholds — if anything, a split decision with low agent agreement is riskier than a roadmap with low agreement.

### D8: Reference canonical parsing algorithm, don't duplicate *(from reflection Finding 5)*

The agent specification parsing algorithm is defined in sc:adversarial-protocol's SKILL.md. Duplicating it into a release-split ref creates drift risk.

**Resolution**: The new `refs/adversarial-integration.md` references the canonical parsing algorithm in sc:adversarial-protocol rather than copying it. It documents only release-split-specific behavior (default agents, context injection, convergence routing).

---

## 4. Files to Modify

### 4.1 `src/superclaude/commands/release-split.md`

**Changes**:

#### A. Add `--agents` to Options table

Insert after the `--smoke-gate` row:

```markdown
| `--agents` | `-a` | No | `opus:architect,haiku:analyzer` | Agent specs for variant generation in Part 2. Format: `model[:persona[:"instruction"]]`, comma-separated. Minimum 2 agents. |
```

#### B. Add usage examples

Add to the Usage section:

```bash
# Custom agents for adversarial variant generation
/sc:release-split path/to/release-spec.md --agents opus:architect,sonnet:security

# With custom instructions per agent
/sc:release-split path/to/release-spec.md \
  --agents opus:architect:"Focus on dependency isolation",haiku:analyzer:"Prioritize testability"
```

Add to the Examples section:

```markdown
### Multi-Agent Split Analysis
\```bash
/sc:release-split .dev/releases/current/v4.0/spec.md \
  --agents opus:architect,sonnet:security --depth deep
\```
```

#### C. Update Behavioral Summary

Change:
> Part 2 (adversarial validation via `/sc:adversarial` — stress-test the proposal)

To:
> Part 2 (adversarial variant generation and validation via `/sc:adversarial` Mode B — independent agents generate competing split proposals, then debate and merge)

#### D. Update Related Commands table

Change the `/sc:adversarial` row description from:
> Stress-test split proposal

To:
> Generate competing split variants and merge via adversarial debate

---

### 4.2 `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

**Changes**:

#### A. Add `--agents` to argument-hint (line 5)

Change:
```yaml
argument-hint: "<spec-file-path> [--output dir] [--depth quick|standard|deep] [--interactive] [--resume-from path] [--no-split] [--r1-scope fidelity-schema|minimal-viable|custom] [--smoke-gate r1|r2]"
```

To:
```yaml
argument-hint: "<spec-file-path> [--output dir] [--depth quick|standard|deep] [--interactive] [--resume-from path] [--no-split] [--r1-scope fidelity-schema|minimal-viable|custom] [--smoke-gate r1|r2] [--agents agent-specs]"
```

#### B. Add `--agents` documentation to Section 3 (Required Input)

After the WARN conditions block, add:

```markdown
**`--agents` handling**: Optional. Comma-separated agent specs in `model[:persona[:"instruction"]]` format.
- Default: `opus:architect,haiku:analyzer`
- Minimum 2 agents, maximum 10
- When present, Part 2 uses sc:adversarial Mode B (generate + compare) instead of Mode A (compare)
- Agent spec parsing follows the canonical algorithm defined in sc:adversarial-protocol SKILL.md "Dual Input Modes > Mode B" section
```

#### C. Add Dispatch Task agent to Execution Vocabulary (Section 4)

Add row to the Execution Vocabulary table:

```markdown
| Dispatch Task agent | `Task` | Parallelized sub-agent work (agent variant generation) |
```

#### D. Add Prerequisites Phase (NEW — before Part 1) *(from reflection Finding 2)*

Insert a new section before Part 1 in the Phase Architecture:

```markdown
### Prerequisites (before Part 1)

**Purpose**: Validate environment and inputs before expensive work begins.

**Behavioral Instructions**:

1. Validate spec file exists and is readable (Read tool). If empty (0 bytes), STOP: "Specification file is empty." If < 5 lines, WARN but proceed.
2. Validate output directory is writable; create if needed.
3. If `--agents` provided:
   - Parse agent specs using the canonical algorithm from sc:adversarial-protocol SKILL.md
   - Validate agent count: 2-10. If out of range, STOP: "Agent count must be 2-10. Provided: N"
   - Validate model identifiers are recognized. If unknown, STOP: "Unknown model '<model>' in --agents."
4. Verify `sc:adversarial-protocol` SKILL.md exists. If not found, STOP: "sc:adversarial skill not installed. Required for Part 2. Install via: superclaude install"
5. If `--resume-from` provided: validate the file exists and is readable.
6. Log all validation results.

**Exit Criteria**: All prerequisites validated. Emit: "Prerequisites validated."
```

Update the Phase Architecture diagram:

```
Prerequisites: Validate inputs          → (inline)
Part 1: Discovery & Proposal            → /sc:brainstorm
Part 2: Adversarial Variant Generation   → /sc:adversarial (Mode B)
Part 3: Execution                        → /sc:design | /sc:workflow | /sc:tasklist
Part 4: Fidelity Verification            → /sc:analyze
```

#### E. Rewrite Part 2 Behavioral Instructions (lines 151-189)

Replace the entire Part 2 section with:

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
- If sc:adversarial Mode B fails (tool error, agent unavailable), retry once with `--depth quick`.
- If retry also fails, fall back to Mode A:
  - `--compare split-proposal.md,<original-spec>`
  - Emit warning: "Agent variant generation failed. Falling back to document comparison mode."
  - Resume current Part 2 Mode A behavior (conceptual roles, not agent-backed)

**Output**: Write verdict and final proposal to `<output>/split-proposal-final.md`

**Exit Criteria**: Final proposal written with adversarial verdict, convergence score, and metadata.

**Checkpoint**: If `--interactive`, present the verdict and ask: "The adversarial review concluded [VERDICT] (convergence: X.XX). Should I proceed to execution, or would you like to discuss the findings?"
```

#### F. Update Error Handling table (Section 7) *(from reflection Finding 6)*

Add these rows to the existing error handling table:

```markdown
| Agent model unavailable | Retry with --depth quick, then fall back to Mode A with warning |
| Agent count out of range (< 2 or > 10) | STOP in Prerequisites: "Agent count must be 2-10. Provided: N" |
| Mode B generation failure | Retry once with --depth quick. If retry fails, fall back to Mode A |
| Low convergence (< 0.6) without --interactive | STOP: "Convergence XX% below threshold. Use --interactive to approve." |
| Low convergence (< 0.5) | STOP regardless of --interactive: "Agent proposals too divergent." |
| Return contract unparseable | Use fallback convergence_score: 0.5, route to PARTIAL path |
| Merged output file missing on disk | Treat as failed, fall back to Mode A |
```

---

### 4.3 `src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md` (NEW FILE)

Create a new ref file. This ref is loaded in Part 2 only. It references the canonical parsing algorithm rather than duplicating it *(per reflection Finding 5)*.

**Contents**:

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

---

### 4.4 `src/superclaude/skills/sc-release-split-protocol/refs/phase-templates.md`

**Changes**:

#### A. Update the Advocate/Skeptic/Pragmatist role descriptions

These roles were designed for Mode A (conceptual framing for comparing two documents). With Mode B, the roles shift: the **agents generate the variants**, and the adversarial pipeline's built-in debate handles the advocate/skeptic dynamic.

Replace the current "Role Specifications" subsection under "Part 2: Adversarial Debate Structure" with:

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

If Mode B fails and the skill falls back to Mode A, use the original conceptual roles:

[Keep the existing Advocate, Skeptic, Pragmatist descriptions as-is, nested under this fallback heading]
```

---

## 5. Migration Path

This is a **backward-compatible enhancement**. The changes do not break any existing invocation:

| Invocation | Before | After |
|-----------|--------|-------|
| `/sc:release-split spec.md` | Mode A compare | Mode B with default agents (opus:architect,haiku:analyzer) |
| `/sc:release-split spec.md --agents opus:security,sonnet:qa` | N/A (flag didn't exist) | Mode B with custom agents |
| Mode B failure | N/A | Falls back to Mode A (current behavior) |

No other commands or skills are affected. The `--agents` flag is scoped entirely to sc:release-split's Part 2.

## 6. Sync Requirements

After implementation:
1. `make sync-dev` — copy changes to `.claude/`
2. `make verify-sync` — confirm sync

## 7. Checklist

- [ ] **Prerequisites phase**: Add to SKILL.md Section 4 before Part 1
- [ ] Add `--agents` flag to command Options table
- [ ] Add usage examples with `--agents`
- [ ] Update Behavioral Summary in command
- [ ] Add `--agents` to SKILL.md argument-hint
- [ ] Add `--agents` handling documentation to SKILL.md Section 3
- [ ] Add Dispatch Task agent to Execution Vocabulary
- [ ] Rewrite Part 2 behavioral instructions for Mode B (using `--generate spec`, not `split-proposal`)
- [ ] Add Mode A fallback within Part 2
- [ ] Create `refs/adversarial-integration.md` (reference canonical parsing, don't duplicate)
- [ ] Update `refs/phase-templates.md` role descriptions
- [ ] **Update SKILL.md Section 7 error handling table** with Mode B failure conditions
- [ ] Align convergence thresholds with sc:roadmap (0.6/0.5 boundaries)
- [ ] Consume full 9-field return contract (not just 4 fields)
- [ ] `make sync-dev && make verify-sync`

---

## Appendix A: Reflection Findings (2026-03-17)

Six findings were identified during /sc:reflect review. All have been incorporated into the plan above.

| # | Finding | Severity | Resolution | Location in Plan |
|---|---------|----------|------------|-----------------|
| 1 | Return contract missing 5 fields vs roadmap precedent | Medium | Expanded to full 9-field consumption with consumer defaults | Section 4.2E step 6, Section 4.3 Return Contract Consumption |
| 2 | No prerequisites/Wave 0 phase for early validation | Medium | Added Prerequisites phase before Part 1 | Section 4.2D (new), Phase Architecture diagram |
| 3 | `--generate split-proposal` may not be a recognized artifact type | High | Changed to `--generate spec`; agent instructions shape output | Design Decision D6, Section 4.2E step 4, Section 4.3 Invocation Pattern |
| 4 | Convergence thresholds differ from roadmap without justification | Low | Aligned to roadmap's 0.6/0.5 boundaries | Design Decision D7, Section 4.2E step 7, Section 4.3 Convergence Routing |
| 5 | Duplicating parsing algorithm instead of referencing canonical source | Low | Reference sc:adversarial-protocol's canonical algorithm | Design Decision D8, Section 4.2B, Section 4.3 Agent Specification Parsing |
| 6 | Error handling table not in checklist | Low | Added to checklist and documented Mode B-specific error rows | Section 4.2F, Checklist items |
