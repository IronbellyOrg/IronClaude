---
name: sc:release-split-protocol
description: "Neutral two-phase release split analysis with adversarial validation and fidelity verification. Use this skill when analyzing whether a planned release should be split into two sequential releases, evaluating release scope for natural seams, or verifying fidelity between original and split release specs."
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
argument-hint: "<spec-file-path> [--output dir] [--depth quick|standard|deep] [--interactive] [--resume-from path] [--no-split] [--r1-scope fidelity-schema|minimal-viable|custom] [--smoke-gate r1|r2] [--agents agent-specs]"
---

# /sc:release-split — Release Split Analysis & Execution Protocol

<!-- Extended metadata (for documentation, not parsed):
category: planning
complexity: advanced
mcp-servers: [sequential, context7, serena]
personas: [architect, analyzer, scribe]
version: 1.0.0
-->

## Triggers

sc:release-split-protocol is invoked ONLY by the `sc:release-split` command via `Skill sc:release-split-protocol` in the `## Activation` section. It is never invoked directly by users.

Activation conditions:
- User runs `/sc:release-split <spec-file>` in Claude Code
- Any flags are passed through from the command

Do NOT invoke this skill directly. Use the `sc:release-split` command.

## 1. Purpose & Identity

Evaluate whether a planned release should remain intact or be split into two sequential releases, then execute and verify the decision. The protocol is **explicitly neutral** — splitting is not assumed to be beneficial. In some cases, the correct answer is to keep the release intact.

**Core Objective**: Identify whether a small, low-lift, high-leverage subset of work exists that can (a) provide real value on its own, (b) improve confidence in the second half, (c) be tested in real-world usage, and (d) allow iteration based on those results.

**Pipeline Position**: `release artifact → sc:release-split → split specs/tasklists + fidelity audit → (user decides) → sc:roadmap / sc:tasklist`

**What "split" means here**: Not dividing a sprint by size or effort. It means finding a natural seam where Release 1 delivers independently testable, independently valuable functionality that Release 2 builds on.

**Output Artifacts** (varies by outcome):

If split approved:
1. `split-proposal.md` — Initial discovery proposal
2. `split-proposal-final.md` — Adversarially validated proposal
3. `release-1-spec.md` — Release 1 specification
4. `release-2-spec.md` — Release 2 specification
5. `fidelity-audit.md` — Auditable coverage verification
6. `boundary-rationale.md` — Split boundary documentation

If no split:
1. `split-proposal.md` — Discovery analysis (recommending no split)
2. `split-proposal-final.md` — Adversarially confirmed no-split
3. `release-spec-validated.md` — Updated single-release spec
4. `fidelity-audit.md` — Validation of intact release

## 2. Global Constraints

These constraints apply across ALL four parts of the protocol. They are non-negotiable.

1. **Neutrality**: Both "split" and "no split" must remain valid outcomes until justified by evidence. Do not bias toward splitting.
2. **Not a size split**: Splitting is about finding a natural seam, not dividing effort in half.
3. **Release 1 scope default**: Unless compelling evidence says otherwise, Release 1 focuses on **planning fidelity and schema hardening only**.
4. **Smoke gate default**: Smoke gate belongs in Release 2 by default, unless earlier analysis proves it is necessary and low-risk for Release 1.
5. **Release 2 planning gate**: Release 2 roadmap/tasklist generation may proceed ONLY after Release 1 has passed real-world validation and results have been reviewed.
6. **Real-world testing only**: ALL tests must use actual functionality in real usage patterns. No mocks, no simulated tests, no fake harnesses, no synthetic validation may be treated as sufficient.
7. **Traceability**: Every deliverable in split outputs must map back to the original release scope. No orphan scope, no invented scope.

## 3. Required Input

**MANDATORY**: A release artifact file path. The artifact must contain identifiable requirements, deliverables, or scope items.

```
/sc:release-split <spec-file-path> [options]
```

**Supported artifacts**: Release specs, roadmaps, tasklists, refactor plans (`.md`, `.yaml`, `.yml`)

**STOP conditions**:
- No file path provided
- File does not exist or is empty
- File contains no identifiable scope items (< 3 extractable requirements)

**WARN conditions**:
- File is very large (> 500 lines) — chunked analysis will be used
- File appears to be a tasklist rather than a spec — confirm with user

**`--agents` handling**: Optional. Comma-separated agent specs in `model[:persona[:"instruction"]]` format.
- Default: `opus:architect,haiku:analyzer`
- Minimum 2 agents, maximum 10
- When present, Part 2 uses sc:adversarial Mode B (generate + compare) instead of Mode A (compare)
- Agent spec parsing follows the canonical algorithm defined in sc:adversarial-protocol SKILL.md "Dual Input Modes > Mode B" section

## 4. Phase Architecture

The protocol executes 4 sequential parts. Each part has entry criteria, delegates to an appropriate command/skill, and produces documented artifacts. Parts execute sequentially because each depends on the previous output.

```
Prerequisites: Validate inputs           → (inline)
Part 1: Discovery & Proposal             → /sc:brainstorm
Part 2: Adversarial Variant Generation   → /sc:adversarial (Mode B)
Part 3: Execution                        → /sc:design | /sc:workflow | /sc:tasklist
Part 4: Fidelity Verification            → /sc:analyze
```

**Execution Vocabulary** (every verb maps to exactly one tool):

| Verb | Tool | Scope |
|------|------|-------|
| Invoke Skill | `Skill` | Cross-skill invocation for delegated commands |
| Read artifact | `Read` | File reads, ref loading, artifact inspection |
| Write artifact | `Write` | Creating new output files |
| Validate | `Read` + `Bash` | File existence checks, prerequisite validation |
| Parse | (inline) | In-memory parsing of flags, proposals — no tool |
| Dispatch Task agent | `Task` | Parallelized sub-agent work (agent variant generation) |

**`--resume-from` handling**: If `--resume-from` is provided, skip Parts 1-2 entirely. Read the specified file as the validated proposal and proceed directly to Part 3.

**`--no-split` handling**: If `--no-split` is provided, skip Parts 1-2. Produce a single-release validation spec in Part 3 and run fidelity verification in Part 4.

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

### Part 1: Discovery & Proposal

**Purpose**: Socratic exploration of whether a split is justified.

**Entry Criteria**: Spec file validated, output directory created.

**Delegation**: Invoke Skill `sc:brainstorm` with structured context.

**Behavioral Instructions**:

1. Read the release artifact (Read tool). Extract a summary of scope, requirements, and dependency structure.
2. Build the brainstorm context incorporating these mandatory discovery questions:
   - What are the dependency chains? Which items are prerequisites for others?
   - Are there components that deliver standalone value and can be validated through real-world use before the rest ships?
   - What is the cost of splitting: integration overhead, context switching, release-management burden, potential rework?
   - What is the cost of NOT splitting: delayed feedback, big-bang risk, harder root-cause isolation if something fails?
   - Is there a natural **foundation vs. application** boundary where Release 1 lays groundwork that Release 2 consumes?
   - Could splitting INCREASE risk by shipping an incomplete mental model, a misleading intermediate state, or a half-baked experience?
3. Invoke Skill `sc:brainstorm` with the context above and `--interactive` if the user requested it.
4. The brainstorm must produce a proposal with:
   - **Recommendation**: Split or Do Not Split (with confidence level)
   - If split:
     - Release 1 scope, objective, and what's testable
     - Release 2 scope, objective, and what depends on Release 1
     - The seam: why THIS is the right split point
     - Real-world test plan for Release 1 (specific scenarios, not abstractions)
     - Risks of the split and mitigations
     - Explicit justification that Release 1 is not just "the easiest work" but work that creates meaningful value for the second half
   - If no split:
     - Why the release is better kept intact
     - What risks remain and how to mitigate them without splitting
     - Alternative strategies for early validation without splitting
5. Apply `--r1-scope` flag: if `fidelity-schema` (default), bias Release 1 toward planning fidelity and schema hardening. If `minimal-viable`, bias toward smallest independently valuable subset. If `custom`, prompt user for Release 1 scope guidance.
6. Apply `--smoke-gate` flag: if `r2` (default), place smoke gate in Release 2 unless analysis proves it necessary and low-risk for Release 1.

**Output**: Write proposal to `<output>/split-proposal.md`

**Exit Criteria**: Proposal written with clear recommendation. If `--interactive`, user has reviewed and confirmed before proceeding.

**Checkpoint**: If `--interactive`, present the proposal and ask: "This is the discovery proposal. Should I proceed to adversarial validation, or would you like to adjust anything first?"

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

### Part 3: Execution

**Purpose**: Execute the approved proposal using the most appropriate command.

**Entry Criteria**: `split-proposal-final.md` exists with clear verdict.

**Refs Loaded**: Read `refs/phase-templates.md` for output templates.

**Command Selection** (determined by verdict and context):

| Verdict | Next Step | Default Command |
|---------|-----------|-----------------|
| Split approved, need release specs | Design two specs | `/sc:design` |
| Split approved, need execution workflow | Workflow planning | `/sc:workflow` |
| Split approved, need tasklists | Sprint planning | `/sc:tasklist` |
| No split, need updated spec | Single spec update | `/sc:design` |

**Do NOT** use `/sc:roadmap` or `/sc:tasklist` unless the approved proposal explicitly says they are appropriate at this stage. Default to `/sc:design` for producing release specs.

**Behavioral Instructions — Split Approved**:

1. Read the final proposal (Read tool).
2. Select the appropriate command based on the proposal's recommended next step.
3. Produce **Release 1 spec**:
   - Scope limited to items assigned to Release 1 in the proposal
   - Must include real-world validation requirements (specific scenarios, not test stubs)
   - Must scope to `--r1-scope` bias (planning fidelity and schema hardening by default)
   - Smoke gate excluded unless proposal explicitly justifies it for Release 1
4. Produce **Release 2 spec**:
   - Scope limited to items assigned to Release 2 in the proposal
   - Must include dependency declarations on Release 1 deliverables
   - Must include explicit planning gate:
     > Release 2 roadmap/tasklist generation may proceed only after Release 1 has passed real-world validation and the results have been reviewed.
   - Smoke gate included here by default
5. Produce **Boundary rationale**:
   - Why this split point was chosen
   - What each release delivers independently
   - Cross-release dependencies
   - Integration points and handoff criteria
6. Apply traceability: every deliverable in both specs must map back to a specific requirement in the original artifact. No orphan scope. No invented scope.

**Behavioral Instructions — No Split**:

1. Read the original spec and the no-split rationale.
2. Produce an updated single-release spec incorporating any improvements identified during the analysis.
3. Include validation strategy for the intact release.
4. Include rationale for preserving integrity.

**Outputs (split)**:
- `<output>/release-1-spec.md`
- `<output>/release-2-spec.md`
- `<output>/boundary-rationale.md`

**Outputs (no split)**:
- `<output>/release-spec-validated.md`

**Exit Criteria**: All spec files written with traceability annotations.

### Part 4: Deep Fidelity Verification

**Purpose**: Auditable verification that 100% of original scope is preserved across outputs.

**Entry Criteria**: Part 3 outputs exist.

**Delegation**: Invoke appropriate analysis (Skill `sc:analyze` or inline verification).

**Refs Loaded**: Read `refs/verification-protocol.md` for the full verification checklist.

**Behavioral Instructions**:

1. Read the original release artifact.
2. Read all Part 3 outputs.
3. Execute the 6-point verification protocol from `refs/verification-protocol.md`:

   **Check 1 — Coverage Matrix**:
   For every discrete requirement, feature, acceptance criterion, constraint, and non-functional requirement in the original spec:
   - Identify its destination in Release 1 or Release 2 (or the validated single spec)
   - Classify status: PRESERVED / TRANSFORMED / DEFERRED / REMOVED
   - Provide justification for any non-PRESERVED status
   - Verify traceability: every item in the output maps back to an original source item

   **Check 2 — Losslessness**:
   - Identify anything missing from the original
   - Identify anything weakened (scope reduction, relaxed criteria)
   - Identify anything newly introduced (scope creep)
   - Explain whether each change is valid

   **Check 3 — Fidelity Assessment**:
   - Evaluate whether the output spec(s) together achieve 100% fidelity with the original
   - If not, list exact gaps and required remediation

   **Check 4 — Boundary Integrity** (split only):
   - Verify Release 1 contains only what belongs there
   - Verify Release 2 contains what was intentionally deferred
   - Flag misplaced items

   **Check 5 — Release 2 Planning Gate Verification** (split only):
   - Confirm Release 2 spec explicitly blocks roadmap/tasklist generation until Release 1 passes real-world validation

   **Check 6 — Real-World Validation Audit**:
   - Verify Release 1 validation uses real functionality in real-world use cases
   - Reject any mocked or simulated validation as insufficient

4. Produce final verdict:
   - **VERIFIED: Split is lossless and acceptable**
   - **VERIFIED WITH REQUIRED REMEDIATION**: List specific items to fix
   - **NOT VERIFIED: Split should be revised or abandoned**

5. If NOT VERIFIED and `--interactive`: prompt user with remediation options before concluding.

**Output**: Write `<output>/fidelity-audit.md`

**Exit Criteria**: Fidelity audit written with clear verdict and coverage matrix.

## 5. Final Output Assembly

After Part 4 completes, assemble the final summary:

```markdown
# Release Split Analysis — Final Report

## Verdict: [SPLIT / NO SPLIT]

## Part 1 — Discovery Outcome
[Summary of brainstorm recommendation]

## Part 2 — Adversarial Verdict
[Summary of debate outcome and key arguments]

## Part 3 — Execution Summary
[What was produced and where]

## Part 4 — Fidelity Verification
[Verdict and key findings]

## Next Steps
[What must happen before Release 2 planning can begin, if split]

## Artifacts Produced
[List of all output files with paths]
```

Write this to `<output>/release-split-report.md`.

## 6. Return Contract

The skill returns these fields to the calling context:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `split-approved`, `no-split`, `split-with-remediation`, `failed` |
| `verdict` | string | Human-readable verdict summary |
| `output_dir` | string | Path to output directory |
| `release_1_spec` | string | Path to Release 1 spec (null if no split) |
| `release_2_spec` | string | Path to Release 2 spec (null if no split) |
| `fidelity_verdict` | string | `verified`, `verified-with-remediation`, `not-verified` |
| `fidelity_score` | float | 0.0-1.0 coverage completeness |
| `remediation_items` | list | Items requiring remediation (empty if fully verified) |
| `artifacts` | list | Paths to all produced artifacts |

## 7. Error Handling

| Condition | Action |
|-----------|--------|
| Spec file not found | STOP with error message |
| Spec file empty | STOP with error message |
| < 3 extractable requirements | STOP: "Insufficient scope items for split analysis" |
| Brainstorm skill unavailable | Fallback: perform discovery inline without delegation |
| Adversarial skill unavailable | STOP: "sc:adversarial required for Part 2. Install via: superclaude install" |
| Part 3 command unavailable | Fallback: produce specs inline using Write tool |
| Fidelity check fails | If interactive: prompt for remediation. Otherwise: report as NOT VERIFIED |
| User cancels at checkpoint | Write partial results and exit cleanly |
| Agent model unavailable | Retry with --depth quick, then fall back to Mode A with warning |
| Agent count out of range (< 2 or > 10) | STOP in Prerequisites: "Agent count must be 2-10. Provided: N" |
| Mode B generation failure | Retry once with --depth quick. If retry fails, fall back to Mode A |
| Low convergence (0.5-0.59) without --interactive | STOP: "Convergence XX% below threshold. Use --interactive to approve." |
| Low convergence (< 0.5) | STOP regardless of --interactive: "Agent proposals too divergent." |
| Return contract unparseable | Use fallback convergence_score: 0.5, route to PARTIAL path |
| Merged output file missing on disk | Treat as failed, fall back to Mode A |

## 8. Boundaries

**Will:**
- Analyze release artifacts for natural split points with explicit neutrality
- Produce evidence-based split/no-split recommendations
- Delegate to appropriate commands for discovery, validation, execution, verification
- Enforce real-world-only validation throughout
- Gate Release 2 planning on Release 1 validation
- Produce auditable fidelity verification with coverage matrix

**Will Not:**
- Assume splitting is correct
- Produce roadmaps or tasklists directly (delegates to appropriate commands)
- Execute the resulting release plans
- Treat mocked or simulated tests as sufficient evidence
- Allow Release 2 planning before Release 1 real-world validation
- Invent scope not present in the original artifact
- Manage git operations or version control
