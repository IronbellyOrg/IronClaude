---
name: sc-validate-roadmap-protocol
description: "Full behavioral protocol for sc:validate-roadmap — multi-agent roadmap-to-spec fidelity validation with adversarial review, coverage matrix, gap registry, and remediation planning. Use this skill whenever verifying roadmap completeness against specifications, auditing coverage before tasklist generation, or checking for requirement gaps between specs and roadmaps."
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
argument-hint: "<roadmap-path> --specs <spec1.md,...> [--output dir] [--depth quick|standard|deep] [--exclude domains] [--max-agents N]"
---

# /sc:validate-roadmap — Roadmap-to-Spec Fidelity Validator

<!-- Extended metadata (for documentation, not parsed):
category: analysis
complexity: advanced
mcp-servers: [sequential]
personas: [analyzer, architect, qa]
version: 2.0.0
-->

## Triggers

sc-validate-roadmap-protocol is invoked ONLY by the `sc:validate-roadmap` command via `Skill sc-validate-roadmap-protocol` in its `## Activation` section. It is never invoked directly by users.

Activation conditions:
- User runs `/sc:validate-roadmap <roadmap-path> --specs <spec-paths>` in Claude Code
- All flags are passed through from the command

Do NOT invoke this skill directly. Use the `sc:validate-roadmap` command.

## 1. Purpose & Identity

Prove — or disprove — that a roadmap covers 100% of the requirements from its source specifications. The validator is **adversarial by default**: the roadmap is incomplete until proven otherwise.

**Domain-agnostic**: Works for any roadmap format (phases, milestones, epics, sprints) and any spec format (PRD, tech spec, release spec, RFC, ADR).

**Success condition**: A consolidated report with per-domain coverage scores, an itemized gap registry sorted by severity, an adversarial review, and a GO / NO-GO verdict.

**Pipeline Position**: `spec(s) → sc:roadmap → roadmap.md → **sc:validate-roadmap** → validation report → (user fixes gaps) → sc:tasklist`

The validation is a **read-only audit**. It never modifies the roadmap or specs. It produces artifacts that inform human decisions about whether the roadmap is ready for tasklist generation.

## 2. Required Input

**MANDATORY**: A roadmap file path AND one or more spec file paths.

```
/sc:validate-roadmap <roadmap-path> --specs <spec1.md,spec2.md,...>
```

## 3. Flags & Options

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<roadmap-path>` | | Yes | - | Path to roadmap under validation |
| `--specs` | `-s` | Yes | - | Comma-separated spec file paths (1-10) |
| `--output` | `-o` | No | `{roadmap-dir}/validation/` | Output directory for artifacts |
| `--exclude` | `-x` | No | - | Comma-separated domains to exclude |
| `--depth` | `-d` | No | `standard` | Analysis depth: quick, standard, deep |
| `--max-agents` | | No | `20` | Maximum parallel agents (4-20) |
| `--skip-adversarial` | | No | `false` | Skip Phase 4 adversarial pass |
| `--skip-remediation` | | No | `false` | Skip Phase 5 remediation plan |
| `--report` | `-r` | No | - | Also write summary to specified path |

**Depth profiles**:

| Depth | Extraction | Agents | Adversarial | Freshness Check |
|-------|-----------|--------|-------------|-----------------|
| `quick` | Explicit requirements only | Max 6 | Abbreviated (Steps 4.1-4.3 only) | Skip |
| `standard` | Full 7-category extraction | Max 12 | Full pass | HIGH + CRITICAL only |
| `deep` | Full extraction + one-hop references | Max 20 | Full pass + silent assumption audit | All VALID findings |

## 4. Execution Vocabulary

Every verb maps to exactly one Claude Code tool. Never use bare verbs without this binding.

| Verb | Tool | Scope |
|------|------|-------|
| Read document | `Read` | Spec files, roadmap file, referenced docs |
| Search content | `Grep` | Pattern matching across files |
| Find files | `Glob` | Discover files by pattern |
| Write artifact | `Write` | Creating new output files |
| Append to artifact | `Edit` | Incremental writes to existing files |
| Dispatch agent | `Task` | Parallel sub-agent validation work |
| Track progress | `TodoWrite` | Phase completion tracking |
| Run validation | `Bash` | File existence checks, line counts |

**Rule**: All verbs in phase instructions MUST resolve to an entry in this glossary.

## 5. Phase Architecture

### Phase 0: Document Ingestion & Requirement Extraction

**Executor**: Orchestrator (you). No agents spawned.

#### Step 0.1 — Read All Documents

Read every file in `--specs` and the roadmap at `<roadmap-path>` in their entirety using `Read`. If any spec references other documents (tech specs, investigation artifacts, ADRs), follow ONE hop — read the referenced file. Do not recursively spider.

#### Step 0.2 — Extract the Requirement Universe

Parse each spec and extract ALL requirements into a structured registry. Apply the following extraction algorithm in order:

1. **Explicit requirements**: Requirement tables, numbered lists, "shall/must/will" statements, acceptance criteria, user stories, feature descriptions.
2. **Implicit requirements**: Architectural decisions, constraints, risk mitigations, data model definitions, API contracts, config specs, migration procedures, deployment steps. These generate derived requirements.
3. **Test requirements**: Every test case becomes a requirement with matching scope, inputs, and assertions.
4. **Non-functional requirements**: Performance targets, security controls, compatibility guarantees, scalability constraints, observability.
5. **Integration requirements**: System boundaries, API contracts, data flows, hook points, wiring specs, startup/shutdown sequences.
6. **Process requirements**: Migration procedures, rollback plans, verification gates, deployment sequences, one-way-door procedures.
7. **Cross-cutting requirements**: Requirements referencing multiple systems/components/layers. Tag with `cross_cutting: true`.

For each requirement, record:

```yaml
- id: "REQ-{sequential}"
  text: "exact requirement statement from spec"
  source: "{file}:{section or line range}"
  type: FUNCTIONAL | NON_FUNCTIONAL | CONSTRAINT | DECISION | RISK_MITIGATION | INTEGRATION | DATA_MODEL | CONFIG | TEST | ACCEPTANCE_CRITERION | DEPENDENCY | PROCESS | QUALITY_GATE | INTER_RELEASE_CONTRACT | SUCCESS_CRITERION | SEQUENCING | LOC_BUDGET
  priority: P0 | P1 | P2 | P3
  domain: "primary domain tag"
  cross_cutting: true | false
  related_reqs: ["REQ-xxx", ...]
```

**Priority heuristic**: "must/required/critical/blocking/shall" = P0. "should/important/expected" = P1. "nice to have/optional/could" = P2. "future/planned/v2/later" = P3. No signal = P1.

**Extraction checklist** — capture items from ALL applicable categories:

| Category | What to Extract |
|----------|----------------|
| Functional Requirements | Every FR with ID, description, acceptance criteria |
| Non-Functional Requirements | Every NFR with target metrics and measurement method |
| Acceptance Criteria | Every AC attached to any FR/NFR — the atomic unit of verification |
| Architectural Decisions | Numbered decisions, technology choices, pattern selections |
| Open Questions / Spikes | Questions the spec says must be resolved |
| Risks | Named risks with mitigation strategies and contingency plans |
| Test Plan | Every test case with ID, description, type, validation target |
| Data Models | Tables, columns, types, constraints, indexes, migrations |
| API Contracts | Endpoints, methods, request/response schemas, error codes |
| Integration Points | Cross-system hooks, wiring, dependency flows |
| Configuration | Config keys, defaults, environment variables, constants |
| File Changes | Specific files the spec says must be modified |
| Quality Gates | Phase gates, stop conditions, exit criteria |
| Inter-Release Contracts | What this release promises to future releases |
| Success Criteria | Numbered SC items serving as release acceptance checklist |
| Sequencing Constraints | Explicit ordering requirements (must-before relationships) |
| LOC / Effort Budgets | Size estimates the spec declares as authoritative |

Write artifact: `{OUTPUT_DIR}/00-requirement-universe.md`

#### Step 0.3 — Parse Roadmap Structure

Extract from the roadmap:

1. **Sections**: Top-level organizational units (phases, milestones, epics) with line ranges
2. **Tasks**: All tasks with ID, description, parent section, line range, dependencies, deliverables, acceptance criteria, and any spec requirement IDs referenced
3. **Gates**: Quality gates / decision points with pass criteria and stop conditions
4. **Integration points**: Where systems connect or are wired together
5. **Test assignments**: Which tests are placed in which sections
6. **Risk mitigations**: How risks are addressed

Write artifact: `{OUTPUT_DIR}/00-roadmap-structure.md`

#### Step 0.4 — Build Domain Taxonomy

From the extracted requirements AND roadmap structure, identify all distinct domains.

**Detection algorithm**:

1. **Cluster by domain signal**: File paths, technology references, requirement type, section headers, system boundaries.
2. **Merge small clusters**: If a domain has fewer than 3 requirements, merge into nearest related domain.
3. **Split oversized clusters**: If a domain has more than 20 requirements, split along natural sub-boundaries.
4. **Ensure non-overlapping coverage**: Every requirement belongs to exactly one primary domain. Cross-cutting requirements are assigned to primary domain but flagged for secondary review.
5. **Cap at `max-agents - 4`**: Reserve 4 slots for mandatory cross-cutting agents.

Write artifact: `{OUTPUT_DIR}/00-domain-taxonomy.md`

---

### Phase 1: Agent Decomposition

**Executor**: Orchestrator. No agents spawned yet.

#### Step 1.1 — Create Domain Agent Assignments

For each domain from Step 0.4, create one agent spec:

```
AGENT-D{N}:
  - domain: {name}
  - requirements: [REQ-xxx, ...]
  - requirement_count: N
  - spec_sections: [sections to read]
  - cross_cutting_reqs: [REQ-xxx from other domains touching this one]
  - output: {OUTPUT_DIR}/01-agent-D{N}-{domain-slug}.md
```

#### Step 1.2 — Create Mandatory Cross-Cutting Agents

Always allocate these four agents regardless of domain count:

| Agent | Scope | Purpose |
|-------|-------|---------|
| **CC1: Internal Consistency (Roadmap)** | Full roadmap | ID schema consistency, count consistency (frontmatter vs body), table-to-prose consistency, cross-reference validity, no duplicate IDs, no orphaned items |
| **CC2: Internal Consistency (Spec)** | Full spec(s) | Section cross-references valid, requirement counts match, no contradictory statements, numeric values consistent |
| **CC3: Dependency & Ordering** | Roadmap + spec | Spec dependency chains respected in roadmap ordering, no circular dependencies, infrastructure before features, irreversible operations properly gated |
| **CC4: Completeness Sweep** | Everything | Re-scan full spec for requirements missed by extraction, verify every REQ has at least one agent's coverage claim, check for implicit systems required by explicit ones |

#### Step 1.3 — Build Cross-Cutting Concern Matrix

```markdown
| Requirement | Primary Agent | Secondary Agents | Integration Risk |
|-------------|--------------|------------------|-----------------|
| REQ-xxx | D3 | D1, D7 | HIGH/MEDIUM/LOW |
```

#### Step 1.4 — Verify Complete Assignment

The union of all agent requirement assignments MUST equal the full requirement universe. Any unassigned requirement goes to the Completeness Sweep agent. Any requirement with multiple primary agents: resolve by domain affinity.

Write artifact: `{OUTPUT_DIR}/00-decomposition-plan.md`

---

### Phase 2: Parallel Agent Execution

**Goal**: Dispatch all agents simultaneously via `Task`. Each validates its assigned requirements against the roadmap.

#### Domain Agent Instructions

Each domain agent receives this prompt template (populated by orchestrator):

```
You are Agent D{N}, validating the "{DOMAIN}" domain.

INPUTS:
- Spec files: {SPEC_PATHS}
- Roadmap: {ROADMAP_PATH}
- Your assigned requirements (pasted in full below)
- Cross-cutting requirements to check: {CROSS_CUTTING_REQ_IDS}

TASK: For EVERY assigned requirement, determine whether the roadmap fully covers it.

PROCEDURE:

1. Read the spec sections for your assigned requirements. Extract exact text,
   acceptance criteria, and sub-requirements.

2. Read the ENTIRE roadmap — requirements may appear in unexpected locations.

3. For each requirement, produce a coverage assessment:

   ### REQ-{ID}: {title}
   - Spec source: {file}:{line or section}
   - Spec text: "{exact quote}"
   - Status: COVERED | PARTIAL | MISSING | CONFLICTING | IMPLICIT
   - Match quality: EXACT | SEMANTIC | WEAK | NONE
   - Evidence:
     - Roadmap location: {file}:{line range} or ABSENT (searched: "{terms}")
     - Roadmap text: "{exact quote}" or ABSENT
   - Sub-requirements: (if applicable)
     - {sub-req-1}: COVERED | PARTIAL | MISSING — evidence: {quote}
   - Acceptance criteria: (if applicable)
     - {AC-1}: COVERED | MISSING — roadmap task: {task ID}
   - Finding: (only if status is not COVERED)
     - Severity: CRITICAL | HIGH | MEDIUM | LOW
     - Gap description: {what is missing or wrong}
     - Impact: {what breaks if this gap reaches implementation}
     - Recommended correction: {specific roadmap edit}
   - Confidence: HIGH | MEDIUM | LOW

OUTPUT: Write report to {OUTPUT_DIR}/01-agent-D{N}-{domain-slug}.md
Include summary statistics at the end.
```

#### Coverage Status Definitions

Agents apply these strictly:

| Status | Definition |
|--------|-----------|
| COVERED | Roadmap contains task(s) that fully satisfy the requirement. ALL sub-requirements and acceptance criteria addressed. Evidence cites exact roadmap lines. |
| PARTIAL | Roadmap addresses some aspects but omits specific sub-requirements, acceptance criteria, or details the spec mandates. |
| MISSING | No roadmap item addresses this requirement. |
| CONFLICTING | Roadmap contains coverage that contradicts the spec. Both quotes provided. |
| IMPLICIT | Requirement would be satisfied as a side-effect of other tasks but is not explicitly tracked. Fragile — flag for review. |

#### Specific Validation Checks

Every agent applies these checks to its domain:

- **Acceptance Criteria Atomicity**: If an FR has 3 ACs, all 3 must appear — not just the FR header.
- **Test Identity Preservation**: Spec Test N must match roadmap Test N in description, not just number.
- **Sequencing Fidelity**: Spec-defined A-before-B ordering must be preserved in roadmap placement.
- **Data Model Completeness**: Every column, type, constraint, index, migration detail must appear.
- **Contract Precision**: API endpoints must match method, path, schemas, error codes.
- **Gate Completeness**: Every gate needs both pass criteria AND stop conditions.
- **Risk Coverage**: Every spec risk must have a roadmap mitigation.
- **Configuration Exactness**: Config keys, defaults, env var names must match exactly.
- **File Change Coverage**: If spec says "modify file X", roadmap must include a task targeting file X.
- **Inter-Release Contracts**: Promises to future releases must be explicitly preserved.

#### Evidence Standards

- Every COVERED claim cites a specific roadmap line range with exact quote.
- Every non-COVERED finding quotes both spec requirement and roadmap text (or absence with search terms attempted).
- Do NOT infer coverage. Vague roadmap language does not satisfy precise spec language.
- A task mentioning a requirement by ID without specificity about HOW is PARTIAL, not COVERED.
- Matching IDs is necessary but not sufficient — the SUBSTANCE must match.

#### Cross-Cutting Agent Instructions

Cross-cutting agents receive the same evidence standards but apply the specific checks from Step 1.2. Each writes to its own output file.

#### Spawn Protocol

1. Dispatch ALL agents in a single message using parallel `Task` calls.
2. Each agent prompt includes the FULL text of its assigned requirements — paste the content, do not reference a file path.
3. If an agent fails, retry ONCE. If retry fails, log failure — CC4 and the adversarial pass will catch gaps.
4. Wait for ALL agents to complete before proceeding to Phase 3.

---

### Phase 3: Consolidation

**Executor**: Orchestrator. No new agents spawned.

#### Step 3.1 — Collect Agent Reports

Read every file matching `{OUTPUT_DIR}/01-agent-*.md`. Verify each agent completed (check for summary statistics). Note any failed agents and list unvalidated requirements.

#### Step 3.2 — Build Unified Coverage Matrix

Merge all agent coverage assessments. Conflict resolution:
- Domain agent assessment overrides cross-cutting agent for the same requirement (unless cross-cutting found something domain missed).
- Two domain agents conflicting on same requirement: flag for adversarial review.

Write artifact: `{OUTPUT_DIR}/02-unified-coverage-matrix.md`

#### Step 3.3 — Deduplicate and Consolidate Findings

Merge findings from all agents into a unified gap registry:
1. Same spec evidence pointing to same gap from different agents → merge, keep strongest evidence, cite both agents.
2. Different aspects of the same underlying issue → keep separate but link them.
3. Contradictory findings (one says COVERED, another says MISSING) → escalate to adversarial pass.

Assign unified IDs: `GAP-{SEVERITY_PREFIX}{sequential}` (C=critical, H=high, M=medium, L=low).

#### Step 3.4 — Adjudicate Findings

For each consolidated finding, assign a verdict:

| Verdict | Definition | Action |
|---------|-----------|--------|
| VALID-CRITICAL | Core deliverable or acceptance test missing; spec contradicted | Must fix before roadmap is usable |
| VALID-HIGH | Spec requirement absent or materially misrepresented | Must fix before tasklist generation |
| VALID-MEDIUM | Partially covered; implementation might be correct if developer reads spec, but roadmap doesn't guarantee it | Should fix before tasklist generation |
| VALID-LOW | Minor wording, ordering, or precision gap; intent captured | Fix during cleanup; does not block |
| REJECTED | Evidence review shows coverage exists — finding is incorrect | Remove from remediation plan |
| STALE | Finding references content that has changed since assessment | Re-verify against current files |
| NEEDS-SPEC-DECISION | Spec is ambiguous or contradictory — cannot validate until spec clarifies | Escalate to spec owner |

**Adjudication rules**:
- LOW confidence findings → re-verify evidence. If evidence doesn't hold, REJECT.
- IMPLICIT coverage → default to VALID-MEDIUM unless the implicit chain is documented in the roadmap.
- Contradictory findings → re-read both cited locations; text on disk is authoritative.

#### Step 3.5 — Freshness Verification

For every finding rated VALID-HIGH or VALID-CRITICAL:
1. Re-read the cited spec lines. Confirm the requirement text matches the quote.
2. Re-read the cited roadmap lines (if any). Confirm the text matches.
3. If either quote is stale, downgrade to STALE and note discrepancy.

This prevents the fix-and-fail loop where remediation targets stale findings.

#### Step 3.6 — Cross-Cutting Concern Validation

For each cross-cutting concern from the matrix (Step 1.3):
1. Verify primary agent validated the core requirement.
2. Verify secondary agents validated their domain's portion.
3. If any portion is uncovered, add a gap.
4. Verify integration between domains is explicitly addressed.

#### Step 3.7 — Integration Wiring Audit

For every integration point in the requirement universe or roadmap:

```
INTEGRATION-{N}:
  - system_a: {component/service}
  - system_b: {component/service}
  - interface: {contract, format, protocol}
  - system_a_side: COVERED | MISSING — {evidence}
  - system_b_side: COVERED | MISSING — {evidence}
  - wiring_task: COVERED | MISSING — {evidence}
  - error_handling: COVERED | MISSING — {evidence}
  - initialization_sequence: COVERED | MISSING — {evidence}
  - verdict: FULLY_WIRED | PARTIALLY_WIRED | UNWIRED
```

Any PARTIALLY_WIRED or UNWIRED integration becomes a gap.

#### Step 3.8 — Completeness Boundary Check

1. Sum all requirements across all agent reports.
2. Compare to the total requirement universe count.
3. If mismatch: identify which requirements fell between boundaries.
4. Any requirement not covered by ANY agent is a CRITICAL gap — process failure.

#### Step 3.9 — Compute Aggregate Metrics

| Metric | Formula |
|--------|---------|
| Full Coverage Score | COVERED / TOTAL * 100 |
| Weighted Coverage Score | (COVERED + 0.5*PARTIAL + 0.25*IMPLICIT) / TOTAL * 100 |
| Gap Score | (MISSING + CONFLICTING) / TOTAL * 100 |
| Confidence Interval | Base +/-2%, +1% per 10 reqs, +2% per failed agent, +1% per incomplete cross-cutting check, cap +/-10% |

#### Step 3.10 — Write Consolidated Report

Write artifact: `{OUTPUT_DIR}/02-consolidated-report.md`

```markdown
---
total_requirements: {N}
covered: {N}
partial: {N}
missing: {N}
conflicting: {N}
implicit: {N}
full_coverage_score: "{%}"
weighted_coverage_score: "{%}"
gap_score: "{%}"
confidence_interval: "+/- {%}"
total_findings: {N}
valid_critical: {N}
valid_high: {N}
valid_medium: {N}
valid_low: {N}
rejected: {N}
stale: {N}
needs_spec_decision: {N}
verdict: "GO | CONDITIONAL_GO | NO_GO"
roadmap_path: "{ROADMAP_PATH}"
spec_paths: ["{SPEC_PATHS}"]
timestamp: "{ISO-8601}"
---

# Roadmap Validation Report

## Executive Summary

- **Verdict**: {GO | CONDITIONAL_GO | NO_GO}
- **Weighted Coverage**: {%} (+/- {margin}%)
- **Total Findings**: {N} ({breakdown by severity})
- **Domains Validated**: {N}
- **Cross-Cutting Concerns**: {N} checked, {N} with gaps
- **Integration Points**: {N} checked, {N} fully wired, {N} with gaps

## Verdict Criteria

| Condition | Decision |
|-----------|----------|
| 0 CRITICAL + 0 HIGH + weighted >= 95% | **GO** — ready for tasklist generation |
| 0 CRITICAL + <=3 HIGH + weighted >= 90% | **CONDITIONAL_GO** — targeted corrections needed |
| Any CRITICAL | **NO_GO** — contradictions must be resolved |
| >3 HIGH | **NO_GO** — significant coverage gaps |
| Weighted < 85% | **NO_GO** — substantial revision needed |
| Any boundary gaps (reqs covered by zero agents) | **NO_GO** — decomposition failed |

## Coverage by Domain
{per-domain table: Domain | Total | Covered | Partial | Missing | Conflicting | Implicit | Score}

## Gap Registry
{all VALID-* findings, ordered by severity then domain, with full detail}

## Cross-Cutting Concern Report
{from Step 3.6}

## Integration Wiring Audit
{from Step 3.7}

## Agent Reports Index
{links to each 01-agent-*.md file}
```

---

### Phase 4: Adversarial Pass

**Executor**: Orchestrator performing a dedicated adversarial review. Skip if `--skip-adversarial` is set.

This is the final quality gate before remediation. The orchestrator re-reads source documents with fresh eyes and challenges every COVERED assessment.

#### Step 4.1 — Fresh Re-Read

Read the original spec(s) and roadmap again. Do NOT rely on agent reports for this pass.

#### Step 4.2 — Challenge Every COVERED Assessment

For each requirement marked COVERED by the parallel agents, ask:
- Does the roadmap task actually produce the deliverable the spec requires?
- Is the roadmap's acceptance criterion as strict as the spec's?
- Could a developer execute the roadmap task and still NOT satisfy the spec requirement?
- Are there implicit sub-requirements the agents missed?
- Is sequencing correct (prerequisites before dependents)?

#### Step 4.3 — Search for Orphan Requirements

Requirements that exist in the spec but were not extracted in Phase 0 — buried in prose, footnotes, appendices, examples, or implicit in architecture diagrams.

#### Step 4.4 — Search for Orphan Roadmap Tasks

Tasks in the roadmap with no spec traceability. Report for awareness:
- Scope creep (roadmap adds work not in spec)
- Missing spec requirements (roadmap author added needed work the spec omitted)
- Implementation details that don't need tracing

#### Step 4.5 — Validate Sequencing and Dependencies

- Spec-mandated ordering constraints reflected in roadmap?
- One-way-door procedures properly gated?
- Exit criteria from one phase satisfied before the next begins?
- Any circular dependencies?

#### Step 4.6 — Check Silent Assumptions

- Does the roadmap assume capabilities, services, or infrastructure not in the spec?
- Are there implicit dependencies between tasks that should be explicit?

#### Step 4.7 — Validate Test Coverage Mapping

- Every spec test case appears in roadmap with matching scope?
- Test numbering and descriptions consistent?
- Test prerequisites addressed?
- Total test count consistent?

#### Step 4.8 — Produce Adversarial Findings

For each new finding not already in the gap registry:

```markdown
### ADV-{N}: {title}
- Type: MISSED_GAP | FALSE_COVERAGE | SEQUENCING_ERROR | ORPHAN_REQUIREMENT | ORPHAN_TASK | SILENT_ASSUMPTION | TEST_MISMATCH
- Severity: CRITICAL | HIGH | MEDIUM | LOW
- Description: {what was missed and why}
- Spec evidence: {file}:{line} — "{quote}"
- Roadmap evidence: {file}:{line} — "{quote}" | ABSENT (searched: "{terms}")
- Impact: {consequence}
- Recommended correction: {specific fix}
```

#### Step 4.9 — Update Consolidated Report

If adversarial pass finds new gaps:
1. Add them to gap registry with `[ADV]` prefix.
2. Recalculate coverage scores.
3. Update verdict if severity thresholds change.
4. Document what the parallel agents missed and why.

Write artifact: `{OUTPUT_DIR}/03-adversarial-review.md`
Update: `{OUTPUT_DIR}/02-consolidated-report.md` with final scores and verdict.

---

### Phase 5: Remediation Plan

**Executor**: Orchestrator. Skip if `--skip-remediation` or verdict is GO.

If verdict is GO, write brief summary stating no remediation needed and skip to Phase 6.

#### Step 5.1 — Order Remediations by Blast Radius

Fixes ordered by dependency chain, not severity alone:

```
Phase R1: Spec-internal contradictions (fix source of truth first)
Phase R2: Roadmap-internal contradictions (fix self-consistency)
Phase R3: Missing coverage — CRITICAL + HIGH (add missing tasks)
Phase R4: Conflicting coverage — CRITICAL + HIGH (correct misrepresentations)
Phase R5: Partial coverage gaps — MEDIUM (flesh out vague items)
Phase R6: Ordering and dependency fixes (reorder to respect spec chains)
Phase R7: Implicit-to-explicit promotion (make implicit coverage tracked)
Phase R8: Low-priority and cleanup (terminology, formatting, minor gaps)
Phase R9: Re-validate (rerun this skill after all fixes applied)
```

#### Step 5.2 — Generate Patch Checklist

For each gap:

```markdown
- [ ] **{GAP_ID}** ({severity}, {effort}): {one-line description}
  - File: {roadmap path}:{line range}
  - Action: ADD | EDIT | MOVE | SPLIT | REMOVE
  - Change: "{exact text to add/change}"
  - Verification: {how to confirm the fix is correct}
  - Dependencies: [{other GAP_IDs that must be fixed first}]
```

Effort levels: TRIVIAL (wording fix) | SMALL (add task/criterion) | MEDIUM (restructure section) | LARGE (add phase/major rework).

#### Step 5.3 — Compute Remediation Impact

```
If all remediations are applied:
  - Projected coverage: {new_%}%
  - Projected findings: {count} (target: 0 CRITICAL, 0 HIGH)
  - Projected verdict: {GO | CONDITIONAL_GO}
  - Estimated effort: {total}
```

Write artifact: `{OUTPUT_DIR}/04-remediation-plan.md`

---

### Phase 6: Final Summary

Write artifact: `{OUTPUT_DIR}/05-validation-summary.md`

```markdown
# Roadmap Validation Summary

## Inputs
- Roadmap: {ROADMAP_PATH}
- Spec(s): {SPEC_PATHS}
- Validation date: {date}
- Depth: {depth}

## Results
- Agents spawned: {N} ({N} domain + {N} cross-cutting)
- Total requirements: {N}
- Weighted coverage: {%} (+/- {margin}%)
- Findings: {N} total, {N} actionable, {N} blocking
- Verdict: {verdict}

## Output Artifacts
| File | Phase | Content |
|------|-------|---------|
| 00-requirement-universe.md | 0 | Extracted spec requirements |
| 00-roadmap-structure.md | 0 | Parsed roadmap structure |
| 00-domain-taxonomy.md | 0 | Domain decomposition |
| 00-decomposition-plan.md | 1 | Agent assignments + cross-cutting matrix |
| 01-agent-*.md | 2 | Per-agent validation reports |
| 02-unified-coverage-matrix.md | 3 | Merged coverage matrix |
| 02-consolidated-report.md | 3 | Adjudicated findings with verdict |
| 03-adversarial-review.md | 4 | Adversarial pass findings |
| 04-remediation-plan.md | 5 | Dependency-ordered fix plan |
| 05-validation-summary.md | 6 | This file |

## Next Steps
- **GO**: Roadmap validated. Proceed to tasklist generation with `/sc:tasklist`.
- **CONDITIONAL_GO**: Apply targeted corrections from remediation plan, then proceed.
- **NO_GO**: Execute remediation phases R1-R8, then rerun `/sc:validate-roadmap`.
```

If `--report` flag is set, also write summary to the specified path.

---

## 6. Execution Rules

These rules govern all phases. Violations produce incorrect results.

| Rule | Name | Requirement |
|------|------|-------------|
| R1 | Artifact-Based Workflow | Work from files, not memory. Every agent writes findings to its output file. The orchestrator reads files to consolidate. No findings exist only in context. |
| R2 | Incremental Writing | NEVER accumulate content in context and write a large file at once. For any file >50 lines: create with header first, then append sections one at a time using `Edit`. Prevents token-limit truncation. |
| R3 | Evidence-Based Claims | Every coverage claim cites specific file:line references and quotes relevant text. "Implied" or "likely covered" is not evidence. If no explicit roadmap text found, status is MISSING. |
| R4 | Spec is Source of Truth | When roadmap conflicts with spec, spec wins. The roadmap is the document under test. Never adjust a requirement to match the roadmap. |
| R5 | Spec Hierarchy | When specs conflict: Release spec > tech spec > PRD > other. Later-dated > earlier-dated. Code-verified > unverified. Unresolvable → NEEDS-SPEC-DECISION. |
| R6 | No False Positives | Do not invent findings. Equivalent meaning in different words is not a gap. Reorganized phases are not a gap unless they violate sequencing constraints. |
| R7 | No False Negatives | Read the spec literally. Check EVERY acceptance criterion individually. Check EVERY column of every data model. Check stop conditions AND pass conditions on gates. |
| R8 | Quote, Don't Paraphrase | Use exact quotes with line numbers. Paraphrasing introduces interpretation error. |
| R9 | No Domain-Proximity Conflation | A milestone about "authentication" does not automatically cover "JWT token rotation policy." Validate the SPECIFIC requirement, not the general topic. |
| R10 | Parallel Agents Are Independent | Agents do not communicate during Phase 2. Deduplication happens in Phase 3. |
| R11 | Phase Sequencing | Complete each phase before starting the next. Phase N depends on Phase N-1 outputs. |
| R12 | Cross-Cutting Double Coverage | Every cross-cutting requirement is validated by primary agent AND checked by at least one secondary agent. |
| R13 | Integration Requires Both Sides | An integration point is only COVERED if both sides are addressed. |
| R14 | Test Fidelity Is Exact | Test validation requires matching: number, description, scope, assertions, prerequisites. Same number + different description = CONFLICTING. |
| R15 | Report All Uncertainty | If ambiguous or debatable, document explicitly. Do not silently pick one interpretation. |
| R16 | Preserve All Artifacts | Do not delete intermediate files. Agent reports serve as the evidence trail. |

---

## 7. Failure Modes and Recovery

| Failure Mode | Detection | Recovery |
|-------------|-----------|----------|
| Spec too vague | Requirement universe < 10 items for non-trivial feature | META finding: "Spec lacks extractable requirements — confidence LOW" |
| No requirement IDs | Cannot trace coverage | Generate sequential IDs. Use description matching. LOW finding about traceability |
| Different terminology | Agent coverage scores anomalously low | Search for semantic equivalents. Create terminology mapping. If found: COVERED with LOW finding |
| >max-agents disciplines | Cap exceeded | Force-merge smallest clusters. Note lost nuance |
| Agent finds zero gaps | Suspiciously clean | Re-read highest-specificity spec sections. If still zero: report confidently |
| Spec contradictions | Two requirements conflict | NEEDS-SPEC-DECISION with both references. Do not resolve |
| Roadmap longer than spec | Extra content | Normal for good roadmaps. Report extras as INFO. Only flag if they contradict spec |
| Missing referenced file | File not in --specs | Read if accessible. If not, META finding + reduce confidence |
| Overlapping specs | Same requirement defined differently | Flag as spec-level conflict. Don't penalize roadmap |
| Very large spec (>500 reqs) | High count | Increase minimum domain count; split aggressively; spawn max agents |
| Very small spec (<10 reqs) | Low count | Use 2-3 agents. Adversarial pass proportionally more important |
| Agent failure | No output file | Retry once. If still fails: UNVALIDATED requirements. Add to confidence interval |
| Roadmap is a tasklist | Non-traditional format | Treat each task as a roadmap section. Validation still applies |
| Out-of-scope items | "future/v2" requirements | Tag priority P3 and exclude from coverage calculations |

---

## 8. Boundaries

**Will:**
- Extract all requirements from spec files into a structured registry
- Validate every requirement against the roadmap with cited evidence
- Spawn parallel domain agents for independent, thorough validation
- Run adversarial review challenging COVERED assessments with fresh eyes
- Produce consolidated report with quantified coverage and GO/NO_GO verdict
- Generate dependency-ordered remediation plan
- Preserve all intermediate artifacts as evidence trail

**Will Not:**
- Modify the roadmap or spec files (read-only audit)
- Execute remediation — only plans it
- Trigger downstream commands automatically
- Resolve spec-internal contradictions — flags for human decision
- Validate code execution or test results — only document-level coverage

## 9. Return Contract

On completion, return to the invoking command:

```yaml
status: "COMPLETED"
verdict: "GO | CONDITIONAL_GO | NO_GO"
weighted_coverage: "{%}"
total_requirements: N
total_findings: N
blocking_findings: N
output_dir: "{OUTPUT_DIR}"
report_path: "{OUTPUT_DIR}/02-consolidated-report.md"
summary_path: "{OUTPUT_DIR}/05-validation-summary.md"
```
