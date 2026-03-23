---
type: reusable-prompt
name: roadmap-spec-fidelity-validator
version: 1.0.0
domain: generic
max_agents: 20
inputs:
  - roadmap_path: "path to roadmap.md or equivalent planning artifact"
  - spec_paths: "one or more spec file paths (comma-separated)"
output: "consolidated validation report with coverage matrix, findings, and remediation plan"
---

# Roadmap-to-Spec Fidelity Validator — Full-Surface Parallel Validation Prompt

## Purpose

Validate that a roadmap artifact covers 100% of its source specification(s). This prompt decomposes the validation surface into up to 20 parallel agent workstreams, each responsible for proving coverage of a specific spec section or cross-cutting concern. The result is a consolidated fidelity report with evidence-backed findings, coverage scores, and a dependency-ordered remediation plan.

This prompt is domain-agnostic. It works for any roadmap/spec pair regardless of subject matter — backend, frontend, infrastructure, AI/ML, game systems, security, or any other domain.

---

## Inputs

You will be given two inputs:

1. **ROADMAP_PATH**: `{ROADMAP_PATH}` — the roadmap file to validate
2. **SPEC_PATHS**: `{SPEC_PATHS}` — one or more specification files (comma-separated if multiple)

If multiple specs are provided, treat them as a unified specification surface. Requirements from all specs must be covered.

---

## Execution Protocol

Execute the following phases in strict order. Do not skip phases. Do not begin a phase until the prior phase is complete and its output file exists on disk.

### Phase 0: Reconnaissance

**You (the orchestrator) perform this phase directly. No agents are spawned.**

#### Step 0.1 — Read All Inputs

Read every file in ROADMAP_PATH and SPEC_PATHS completely. If any file exceeds 2000 lines, read in chunks but ensure full coverage.

#### Step 0.2 — Build the Spec Requirement Inventory

Extract every requirement, system, subsystem, component, behavior, constraint, integration point, data flow, API surface, configuration, migration step, rollout rule, NFR, and success criterion from the spec(s).

For each item, record:

```yaml
- id: "REQ-{sequential}"
  type: FR | NFR | SYSTEM | INTEGRATION | CONSTRAINT | BEHAVIOR | CONFIG | MIGRATION | ROLLOUT
  description: "exact description from spec"
  source_file: "path"
  source_lines: "L{start}-L{end}"
  domain: "classified domain (backend, frontend, infra, AI, security, data, UX, ops, testing, docs, etc.)"
  priority: P0 | P1 | P2 | P3
  dependencies: ["REQ-xxx", ...]
```

**Priority heuristic**:
- "must", "required", "critical", "blocking", "shall" → P0
- "should", "important", "expected" → P1
- "nice to have", "optional", "could" → P2
- "future", "planned", "v2", "later" → P3
- No signal → P1

Write this inventory to: `{OUTPUT_DIR}/00-spec-inventory.md`

Count the total requirements. This count is the denominator for all coverage calculations.

#### Step 0.3 — Build the Roadmap Inventory

Extract every milestone, deliverable, task, dependency, risk, success criterion, and integration point from the roadmap.

For each item, record:

```yaml
- id: "RM-{roadmap's own ID or sequential}"
  type: MILESTONE | DELIVERABLE | TASK | RISK | DEPENDENCY | SUCCESS_CRITERION
  description: "exact description from roadmap"
  source_lines: "L{start}-L{end}"
  domain: "classified domain"
```

Write this inventory to: `{OUTPUT_DIR}/00-roadmap-inventory.md`

#### Step 0.4 — Compute Decomposition Strategy

Based on the spec inventory, determine how to partition the validation surface into parallel agent workstreams. The goal is maximum parallelism with zero coverage gaps and minimal overlap.

**Decomposition algorithm** (apply in order, stop when agent count reaches 20 or all requirements are assigned):

1. **Domain-based partitioning**: Group requirements by domain. Each domain with >= 3 requirements gets its own agent. Domains with < 3 requirements are merged into the nearest related domain.

2. **Size-based splitting**: If any domain has > 30 requirements, split it into sub-domains by type (FRs in one agent, NFRs in another) or by subsystem.

3. **Cross-cutting agents** (always allocate these, they do NOT count toward the domain limit):
   - **Agent: Internal Consistency** — validates the roadmap is internally self-consistent (IDs, counts, cross-references, tables vs prose)
   - **Agent: Internal Consistency (Spec)** — validates each spec is internally self-consistent
   - **Agent: Dependency & Ordering** — validates milestone ordering respects spec dependency chains
   - **Agent: Completeness Sweep** — final catch-all that scans for any requirement not claimed by another agent

4. **Agent ceiling**: Maximum 20 agents total. If decomposition produces more than 20, merge the smallest domain groups until at or below 20.

5. **Agent floor**: Minimum 5 agents. If decomposition produces fewer than 5, split the largest domain groups or add additional cross-cutting agents (risk coverage, NFR coverage, integration point coverage).

Write the decomposition plan to: `{OUTPUT_DIR}/00-decomposition-plan.md`

Format:

```markdown
# Decomposition Plan

Total spec requirements: {N}
Total roadmap items: {M}
Agent count: {K}

| Agent # | Name | Type | Requirement IDs Assigned | Count | Focus |
|---------|------|------|-------------------------|-------|-------|
| 1 | {name} | domain | REQ-001 through REQ-015 | 15 | {description} |
| 2 | {name} | domain | REQ-016 through REQ-028 | 13 | {description} |
| ... | | | | | |
| K-3 | Internal Consistency (Roadmap) | cross-cutting | ALL | - | Self-consistency of roadmap |
| K-2 | Internal Consistency (Spec) | cross-cutting | ALL | - | Self-consistency of spec(s) |
| K-1 | Dependency & Ordering | cross-cutting | ALL | - | Milestone ordering vs spec deps |
| K | Completeness Sweep | cross-cutting | ALL | - | Catch any uncovered requirements |
```

**Coverage guarantee**: The union of all domain-agent requirement assignments must equal the full spec inventory. Verify this before proceeding. If any requirement is unassigned, assign it to the Completeness Sweep agent.

---

### Phase 1: Parallel Validation (Spawn Up to 20 Agents)

**Spawn all agents in parallel using the Task tool.** Each agent receives its own prompt with its assigned requirements and the full roadmap. Agents are read-only — they do not modify any files. Each agent writes its findings to its own output file.

#### Agent Prompt Template

Each agent receives the following prompt. Replace placeholders with agent-specific values.

```
You are validation agent #{AGENT_NUMBER}: "{AGENT_NAME}".

Your task: Validate that the roadmap fully covers every requirement assigned to you. You must prove coverage or prove absence for each requirement.

## Your Assigned Requirements

{PASTE THE FULL REQUIREMENT LIST FOR THIS AGENT FROM 00-spec-inventory.md}

## Source Documents

- Spec(s): {SPEC_PATHS}
- Roadmap: {ROADMAP_PATH}

Read the spec(s) and roadmap completely before beginning validation.

## Validation Protocol

For DOMAIN agents (assigned specific requirements):

For each assigned requirement (REQ-xxx), determine its coverage status:

### Coverage Statuses

| Status | Definition | Evidence Required |
|--------|-----------|-------------------|
| COVERED | Roadmap explicitly addresses this requirement with a milestone, deliverable, or task | Cite roadmap line(s) + deliverable/task ID |
| PARTIAL | Roadmap addresses some aspects but misses specific sub-requirements or details | Cite what IS covered (with lines) AND what is MISSING (with spec lines) |
| MISSING | No roadmap item addresses this requirement | Cite spec lines where requirement is defined; confirm absence by searching roadmap for key terms |
| DISTORTED | Roadmap addresses this but with incorrect/changed semantics | Cite both spec lines (original) and roadmap lines (distorted version); explain the semantic difference |
| IMPLICIT | Requirement would be satisfied as a side-effect of other roadmap items, but is not explicitly tracked | Cite the roadmap items that implicitly cover it; note the risk of implicit coverage |

### For CROSS-CUTTING agents:

**Internal Consistency (Roadmap)**: Check these dimensions:
- ID schema consistency (milestone IDs, deliverable IDs, task IDs follow a pattern)
- Count consistency (frontmatter counts match body counts)
- Table-to-prose consistency (summary tables match detailed sections)
- Cross-reference validity (dependency references point to real items)
- No duplicate IDs
- No orphaned items (deliverables not under any milestone, tasks not under any deliverable)

**Internal Consistency (Spec)**: Check these dimensions:
- Section cross-references are valid
- Requirement counts in summary match detailed sections
- No contradictory statements within the spec
- File/component inventories are consistent across sections
- Numeric values (counts, thresholds, percentages) are consistent

**Dependency & Ordering**: Check these dimensions:
- Spec defines or implies dependency chains — does roadmap milestone ordering respect them?
- Are there spec requirements that must precede others (e.g., "database before API") where the roadmap orders them incorrectly?
- Are there circular dependencies in the roadmap?
- Are infrastructure/foundation requirements scheduled before features that depend on them?

**Completeness Sweep**: Check these dimensions:
- Re-scan the FULL spec for any requirement, system, behavior, or constraint not captured in 00-spec-inventory.md
- For every requirement in 00-spec-inventory.md, verify at least one domain agent has claimed it as COVERED, PARTIAL, or MISSING
- Flag any requirement with no agent coverage claim
- Check for implicit systems: does the spec describe systems that must exist for other systems to work, even if not explicitly listed as requirements?

## Evidence Standards

Every finding MUST include:
- **Spec evidence**: File path + line number(s) + direct quote (max 2 sentences)
- **Roadmap evidence**: File path + line number(s) + direct quote (max 2 sentences), OR explicit statement of absence with search terms attempted
- **Confidence**: HIGH (direct textual match), MEDIUM (semantic match requiring interpretation), LOW (inferential — flagged for orchestrator review)

Findings without evidence are INVALID and will be rejected during consolidation.

Do NOT:
- Infer coverage from vague roadmap language that could mean anything
- Accept boilerplate roadmap text as covering specific technical requirements
- Mark something COVERED just because the roadmap mentions the same domain
- Fabricate line numbers or quotes

DO:
- Be aggressive about finding gaps — false negatives are more costly than false positives
- Check that the roadmap covers the SPECIFIC details, not just the general topic
- Verify that integration points between systems are planned, not just the systems themselves
- Flag when the roadmap uses different terminology than the spec (possible distortion or possible synonym)

## Output Format

Write your findings to: {OUTPUT_DIR}/01-agent-{AGENT_NUMBER}-{AGENT_SLUG}.md

Use this structure:

```markdown
---
agent_number: {AGENT_NUMBER}
agent_name: "{AGENT_NAME}"
agent_type: domain | cross-cutting
requirements_assigned: {COUNT}
covered: {COUNT}
partial: {COUNT}
missing: {COUNT}
distorted: {COUNT}
implicit: {COUNT}
coverage_score: {PERCENTAGE}
finding_count: {COUNT}
---

# Agent {AGENT_NUMBER}: {AGENT_NAME} — Validation Report

## Coverage Matrix

| REQ ID | Description (truncated) | Status | Roadmap Item | Evidence | Confidence |
|--------|------------------------|--------|-------------|----------|------------|
| REQ-001 | ... | COVERED | D2.3 | roadmap.md:L45 | HIGH |
| REQ-002 | ... | MISSING | - | spec.md:L120-125 | HIGH |
| ... | | | | | |

## Findings

### FIND-{AGENT_NUMBER}-001: {Title}

- **Severity**: CRITICAL | HIGH | MEDIUM | LOW | INFO
- **Type**: missing-coverage | partial-coverage | distorted-requirement | internal-inconsistency | ordering-violation | implicit-only
- **Spec Evidence**: `{file}:L{n}-L{m}` — "{quote}"
- **Roadmap Evidence**: `{file}:L{n}-L{m}` — "{quote}" | ABSENT (searched: "{terms}")
- **Confidence**: HIGH | MEDIUM | LOW
- **Impact**: {What breaks or is at risk if this gap remains}
- **Suggested Remediation**: {Minimal fix}

### FIND-{AGENT_NUMBER}-002: ...

## Summary

- Requirements validated: {N}
- Coverage: {COVERED + PARTIAL} / {TOTAL} = {PERCENTAGE}%
- Full coverage: {COVERED} / {TOTAL} = {PERCENTAGE}%
- Findings requiring action: {COUNT}
- Critical/High findings: {COUNT}
```

Return the file path when complete.
```

#### Spawning Rules

1. Spawn ALL agents in a single message using parallel Task tool calls. Do not spawn sequentially.
2. Each agent prompt must include the FULL text of its assigned requirements from `00-spec-inventory.md` — do not reference the file; paste the content.
3. Each agent prompt must include the full paths to spec(s) and roadmap so it can Read them.
4. If an agent fails (tool error, timeout), retry ONCE. If retry fails, log the failure and continue — the Completeness Sweep agent will catch any gaps.
5. Wait for ALL agents to complete before proceeding to Phase 2.

---

### Phase 2: Consolidation

**You (the orchestrator) perform this phase directly. No new agents are spawned.**

#### Step 2.1 — Collect All Agent Reports

Read every file matching `{OUTPUT_DIR}/01-agent-*.md`. Parse each report's frontmatter and findings.

#### Step 2.2 — Build Unified Coverage Matrix

Merge all agent coverage matrices into a single matrix. For each requirement:

- If multiple agents assessed the same requirement (cross-cutting + domain), use the MOST SPECIFIC assessment (domain agent overrides cross-cutting unless cross-cutting found something domain agent missed).
- If two domain agents conflict on the same requirement, flag it for manual review.

Write to: `{OUTPUT_DIR}/02-unified-coverage-matrix.md`

```markdown
# Unified Coverage Matrix

Total spec requirements: {N}
Covered: {C} ({C/N * 100}%)
Partial: {P} ({P/N * 100}%)
Missing: {M} ({M/N * 100}%)
Distorted: {D} ({D/N * 100}%)
Implicit: {I} ({I/N * 100}%)

Full coverage score: {(C) / N * 100}%
Effective coverage score: {(C + P + I) / N * 100}%
Gap score: {(M + D) / N * 100}%

| REQ ID | Description | Status | Roadmap Item | Agent | Confidence |
|--------|------------|--------|-------------|-------|------------|
| ... | | | | | |
```

#### Step 2.3 — Deduplicate and Consolidate Findings

Merge findings from all agents. Deduplicate by:
1. Same spec evidence pointing to same gap → merge into one finding, keep strongest evidence
2. Overlapping concerns from different angles → merge, noting both perspectives
3. Conflicting findings (one agent says COVERED, another says MISSING) → flag for adversarial review

Assign unified finding IDs: `FIND-{sequential:3digits}`

#### Step 2.4 — Adversarial Adjudication

For each consolidated finding, assign a verdict:

| Verdict | Definition | Action |
|---------|-----------|--------|
| VALID-CRITICAL | Fundamental system or requirement completely absent from roadmap | Must fix before roadmap is usable |
| VALID-HIGH | Significant gap — requirement partially covered or distorted | Must fix before implementation begins |
| VALID-MEDIUM | Non-trivial gap but workaround exists or risk is bounded | Should fix; can proceed with caution |
| VALID-LOW | Minor gap — formatting, terminology, or low-priority requirement | Fix during cleanup; does not block |
| REJECTED | Finding is incorrect — evidence review shows coverage exists | Remove from remediation plan |
| STALE | Finding references content that has changed since assessment | Re-verify against current files |
| NEEDS-SPEC-DECISION | Spec is ambiguous or contradictory — roadmap cannot be validated until spec clarifies | Escalate to spec owner |

**Adjudication rules**:
- LOW confidence findings → re-verify evidence before accepting. If evidence does not hold, REJECT.
- Findings about "implicit" coverage → default to VALID-MEDIUM unless the implicit coverage chain is explicitly documented in the roadmap.
- Contradictory findings between agents → re-read both cited locations; the text on disk is authoritative.
- Quote-based findings → verify the quoted text still exists at the cited line numbers. If not, mark STALE.

#### Step 2.5 — Freshness Verification

For every finding rated VALID-HIGH or VALID-CRITICAL:
1. Re-read the cited spec lines. Confirm the requirement text matches the quote.
2. Re-read the cited roadmap lines (if any). Confirm the text matches.
3. If either quote is stale, downgrade to STALE and note the discrepancy.

This step prevents the "fix-and-fail" loop where remediation targets stale findings.

#### Step 2.6 — Build Consolidated Findings Report

Write to: `{OUTPUT_DIR}/02-consolidated-findings.md`

```markdown
---
total_findings: {N}
valid_critical: {count}
valid_high: {count}
valid_medium: {count}
valid_low: {count}
rejected: {count}
stale: {count}
needs_spec_decision: {count}
roadmap_path: "{ROADMAP_PATH}"
spec_paths: ["{SPEC_PATHS}"]
validation_timestamp: "{ISO-8601}"
---

# Consolidated Validation Findings

## Summary

| Metric | Value |
|--------|-------|
| Total Requirements | {N} |
| Covered | {C} ({%}) |
| Partial | {P} ({%}) |
| Missing | {M} ({%}) |
| Distorted | {D} ({%}) |
| Implicit | {I} ({%}) |
| Full Coverage Score | {%} |
| Effective Coverage Score | {%} |
| Gap Score | {%} |
| Total Findings | {count} |
| Actionable Findings (VALID-*) | {count} |
| Blocking Findings (CRITICAL + HIGH) | {count} |

## Verdict: {PASS | PASS_WITH_WARNINGS | NEEDS_REMEDIATION | FAIL}

Verdict logic:
- PASS: 0 CRITICAL, 0 HIGH, effective coverage >= 95%
- PASS_WITH_WARNINGS: 0 CRITICAL, <= 2 HIGH, effective coverage >= 85%
- NEEDS_REMEDIATION: any CRITICAL or > 2 HIGH or effective coverage < 85%
- FAIL: > 3 CRITICAL or effective coverage < 60%

## Findings by Severity

### CRITICAL

#### FIND-001: {Title}
- **Verdict**: VALID-CRITICAL
- **Owner**: spec | roadmap | both | needs-decision
- **Type**: {type}
- **Spec Evidence**: ...
- **Roadmap Evidence**: ...
- **Confidence**: HIGH
- **Impact**: ...
- **Remediation**: ...
- **Dependencies**: [FIND-xxx, ...]

### HIGH
...

### MEDIUM
...

### LOW
...

### NEEDS-SPEC-DECISION
...

### REJECTED (for audit trail)
...
```

---

### Phase 3: Remediation Plan

**You (the orchestrator) perform this phase directly.**

If the verdict is PASS, skip this phase. Write a brief summary to `{OUTPUT_DIR}/03-remediation-plan.md` stating no remediation is needed.

Otherwise, build a dependency-ordered remediation plan.

#### Remediation Ordering Rules

Fixes are ordered by blast radius, not by severity alone:

```
Phase 1: Spec-internal contradictions
  → Fix the source of truth first. Any spec contradiction will cause downstream
    roadmap contradictions and validation noise.

Phase 2: Roadmap-internal contradictions
  → Fix self-consistency before cross-document comparison.

Phase 3: Missing coverage (CRITICAL + HIGH)
  → Add missing milestones/deliverables/tasks to the roadmap.

Phase 4: Distorted coverage (CRITICAL + HIGH)
  → Correct roadmap items that misrepresent spec requirements.

Phase 5: Partial coverage gaps (MEDIUM)
  → Flesh out roadmap items that are too vague or incomplete.

Phase 6: Ordering and dependency fixes
  → Reorder milestones to respect spec dependency chains.

Phase 7: Implicit-to-explicit promotion
  → Make implicit coverage explicit with tracked deliverables.

Phase 8: Low-priority and cleanup
  → Terminology alignment, formatting, minor gaps.

Phase 9: Re-validate
  → Rerun this prompt after all fixes are applied.
```

Write to: `{OUTPUT_DIR}/03-remediation-plan.md`

```markdown
---
total_remediations: {N}
blocking_count: {critical + high count}
estimated_phases: {phase count}
verdict: {current verdict}
target_verdict: PASS
---

# Remediation Plan

## Phase Execution Order

### Phase 1: Spec-Internal Contradictions ({count} items)

| # | Finding | Target File | Action | Depends On |
|---|---------|------------|--------|------------|
| 1 | FIND-xxx | spec.md:L{n} | {action} | - |

### Phase 2: Roadmap-Internal Contradictions ({count} items)
...

[Continue through all phases]

## Revalidation Checklist

After completing all phases:
- [ ] All Phase 1-8 items marked complete
- [ ] No spec-internal contradictions remain
- [ ] No roadmap-internal contradictions remain
- [ ] Rerun this validation prompt with same inputs
- [ ] Target: PASS verdict with 0 CRITICAL, 0 HIGH findings
```

---

### Phase 4: Final Summary

Write to: `{OUTPUT_DIR}/04-validation-summary.md`

```markdown
# Roadmap Validation Summary

## Inputs
- Roadmap: {ROADMAP_PATH}
- Spec(s): {SPEC_PATHS}
- Validation date: {date}

## Results
- Agents spawned: {N}
- Total requirements validated: {N}
- Coverage score: {%}
- Findings: {N} total, {N} actionable
- Verdict: {verdict}

## Output Artifacts
| File | Purpose |
|------|---------|
| 00-spec-inventory.md | Extracted spec requirements |
| 00-roadmap-inventory.md | Extracted roadmap items |
| 00-decomposition-plan.md | Agent decomposition strategy |
| 01-agent-*.md | Individual agent validation reports |
| 02-unified-coverage-matrix.md | Merged coverage matrix |
| 02-consolidated-findings.md | Deduplicated, adjudicated findings |
| 03-remediation-plan.md | Dependency-ordered fix plan |
| 04-validation-summary.md | This file |

## Next Steps
{If PASS: "Roadmap is validated. Proceed to tasklist generation."}
{If PASS_WITH_WARNINGS: "Roadmap is validated with warnings. Review MEDIUM findings before tasklist generation."}
{If NEEDS_REMEDIATION: "Execute remediation plan phases 1-8, then rerun validation."}
{If FAIL: "Significant coverage gaps detected. Review CRITICAL findings with spec owner before proceeding."}
```

---

## Orchestrator Rules (Non-Negotiable)

1. **Write to disk immediately**: Every inventory, plan, report, and finding is written to disk as it is produced. Never accumulate content in context for a single large write.

2. **Incremental file construction**: For any file > 50 lines, create the file with frontmatter/header first, then append sections one at a time using Edit. Never rewrite the entire file from memory.

3. **Evidence or nothing**: Every finding must cite file:line with a direct quote. Findings without evidence are automatically REJECTED during consolidation.

4. **Text on disk is authoritative**: If your memory of a file's content conflicts with what Read returns, the Read result is correct. Re-read before making any claim.

5. **No hallucinated coverage**: The most dangerous error is marking a requirement COVERED when it is not. When in doubt, mark PARTIAL or MISSING — false negatives (missed gaps) are far more costly than false positives (flagged non-gaps).

6. **Freshness verification is mandatory**: Before including any VALID-HIGH or VALID-CRITICAL finding in the remediation plan, re-verify the cited evidence against current file contents. Stale findings cause wasted remediation effort and feed the fix-and-fail loop.

7. **Agents do not modify files**: All agents are read-only validators. Only the orchestrator (you) writes output artifacts.

8. **Full coverage or explicit gap**: After Phase 2, every single requirement from `00-spec-inventory.md` must appear in `02-unified-coverage-matrix.md` with a status. If any requirement has no status, it is a process failure — assign it MISSING and flag the gap in the summary.

9. **Do not conflate domain proximity with coverage**: A roadmap milestone about "authentication" does not automatically cover a spec requirement about "JWT token rotation policy." Validate the SPECIFIC requirement, not the general topic.

10. **Cross-cutting agents are mandatory**: Internal Consistency, Dependency & Ordering, and Completeness Sweep agents must always be spawned regardless of domain count. These catch structural issues that domain agents miss.

---

## Output Directory Convention

All output files are written to `{OUTPUT_DIR}`. If not specified by the user, default to:

```
{directory containing ROADMAP_PATH}/.validation/
```

Create the directory if it does not exist.

---

## Usage Examples

### Single spec, single roadmap
```
ROADMAP_PATH=.dev/releases/current/feature-X/roadmap.md
SPEC_PATHS=.dev/releases/current/feature-X/release-spec.md
OUTPUT_DIR=.dev/releases/current/feature-X/.validation/
```

### Multiple specs consolidated into one roadmap
```
ROADMAP_PATH=.dev/releases/current/platform-v3/roadmap.md
SPEC_PATHS=specs/backend-spec.md,specs/frontend-spec.md,specs/infra-spec.md
OUTPUT_DIR=.dev/releases/current/platform-v3/.validation/
```

### Revalidation after remediation
```
# Same inputs, same output dir — files get -N suffix if collisions exist
ROADMAP_PATH=.dev/releases/current/feature-X/roadmap.md
SPEC_PATHS=.dev/releases/current/feature-X/release-spec.md
OUTPUT_DIR=.dev/releases/current/feature-X/.validation/
```

---

## Design Rationale

This prompt was designed to solve the **fix-and-fail loop** observed in document-fidelity pipelines:

1. **Multi-agent parallelism** prevents the single-pass recall problem. No single LLM pass has perfect recall across a large spec. By decomposing across 5-20 agents with overlapping cross-cutting sweeps, recall approaches completeness.

2. **Adversarial adjudication** prevents false positives from wasting remediation effort. Every finding is challenged before it becomes actionable.

3. **Freshness verification** prevents stale findings from persisting across validation runs. Quoted evidence is re-checked against current files before remediation.

4. **Dependency-ordered remediation** prevents upstream fixes from invalidating downstream fixes. Spec contradictions are fixed before roadmap gaps, which are fixed before traceability cleanup.

5. **Completeness Sweep agent** provides a safety net. Even if domain decomposition misses requirements, the sweep agent catches them.

6. **Evidence standards with confidence tiers** allow aggressive gap detection (LOW confidence) without flooding the remediation plan (only HIGH confidence findings at CRITICAL/HIGH severity drive mandatory action).

7. **Owner classification** (spec / roadmap / both / needs-decision) prevents the common failure mode of forcing roadmap changes when the real issue is spec ambiguity.
