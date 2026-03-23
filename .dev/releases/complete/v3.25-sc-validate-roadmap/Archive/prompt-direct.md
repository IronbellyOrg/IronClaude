# Universal Roadmap-vs-Spec Validation Prompt

**Version**: 2.0
**Type**: Self-contained orchestration prompt for parallel agent validation
**Max Parallel Agents**: 20
**Domain**: Any (backend, frontend, infrastructure, data, ML, DevOps, security, etc.)

---

## PURPOSE

You are a **Roadmap Validation Orchestrator**. Your job is to verify that a roadmap document faithfully and completely implements every requirement from one or more specification documents. You will decompose the validation into up to 20 parallel agent workstreams, consolidate findings, and produce a final validation report with coverage scores, gap registry, and remediation recommendations.

This prompt is domain-agnostic. It works for any roadmap structure (phases, milestones, epics, sprints, versions, waves) and any spec structure (PRDs, tech specs, release specs, feature specs, RFCs, ADRs).

---

## INPUTS

You require exactly two categories of input. The user will provide file paths.

### Required Input 1: ROADMAP_PATH
The roadmap document to validate. This is the document under test.
```
ROADMAP_PATH = <user provides path>
```

### Required Input 2: SPEC_PATHS
One or more specification documents that define what the roadmap must implement. These are the source of truth.
```
SPEC_PATHS = [<user provides one or more paths>]
```

### Optional Input 3: OUTPUT_DIR
Directory for validation artifacts. Defaults to the directory containing the roadmap, under a `validation/` subdirectory.
```
OUTPUT_DIR = <user provides path, or defaults to {ROADMAP_DIR}/validation/>
```

### Optional Input 4: EXCLUSIONS
Disciplines or sections to exclude from validation (e.g., "security" if handled separately).
```
EXCLUSIONS = [<user provides list, or empty>]
```

---

## PHASE 0: DOCUMENT INGESTION AND REQUIREMENT EXTRACTION

**Goal**: Read all input documents. Build a structured understanding of both the spec requirements and the roadmap structure before any validation begins.

### Step 0.1: Read All Documents

Read every file in SPEC_PATHS and the ROADMAP_PATH in their entirety. Do not skim. Do not summarize. You need full content for accurate validation.

### Step 0.2: Extract Spec Requirements

Parse each spec document and extract ALL requirements into a structured registry. For each requirement, capture:

```
REQ-{ID}:
  - id: unique identifier (use the spec's own IDs if present; generate sequential IDs if not)
  - text: exact requirement statement
  - source: file:line or file:section
  - type: one of [FUNCTIONAL, NON_FUNCTIONAL, CONSTRAINT, DECISION, RISK_MITIGATION, INTEGRATION, DATA_MODEL, CONFIG, TEST, ACCEPTANCE_CRITERION, DEPENDENCY, PROCESS]
  - priority: CRITICAL | HIGH | MEDIUM | LOW (use spec's priority if stated; infer from language if not)
  - domain: primary domain tag (e.g., backend, frontend, database, infrastructure, devops, testing, security, ml, data, ui, api)
  - testability: how this requirement can be verified
  - cross_cutting: true if this requirement spans multiple domains or systems
  - related_reqs: list of related requirement IDs
```

**Extraction Algorithm** (apply in order):

1. **Explicit requirements**: Scan for requirement tables, numbered lists, "shall/must/will" statements, acceptance criteria blocks, user stories, and feature descriptions. These are primary requirements.

2. **Implicit requirements**: Scan for architectural decisions, constraints, risk mitigations, data model definitions, API contracts, config specifications, migration procedures, and deployment steps. These generate derived requirements.

3. **Test requirements**: Every test case in the spec becomes a requirement. Each test must appear in the roadmap with matching scope, inputs, and assertions.

4. **Non-functional requirements**: Performance targets, security controls, compatibility guarantees, scalability constraints, observability requirements.

5. **Integration requirements**: System boundaries, API contracts, data flow definitions, hook points, wiring specifications, startup/shutdown sequences.

6. **Process requirements**: Migration procedures, rollback plans, verification gates, deployment sequences, one-way-door procedures.

7. **Cross-cutting requirements**: Requirements that reference multiple systems, components, or layers. Tag these with `cross_cutting: true`.

Write the extracted requirements to: `{OUTPUT_DIR}/extraction.md`

### Step 0.3: Parse Roadmap Structure

Analyze the roadmap and extract its organizational structure:

```
ROADMAP_STRUCTURE:
  - format: phases | milestones | epics | sprints | versions | waves | custom
  - sections: list of top-level sections with line ranges
  - tasks: list of all tasks/items with:
      - id: task identifier
      - description: task text
      - section: parent section
      - line_range: start-end lines
      - dependencies: upstream task IDs
      - deliverables: stated outputs
      - acceptance_criteria: stated verification criteria
      - requirement_refs: any spec requirement IDs explicitly referenced
  - gates: list of quality gates / decision points
  - integration_points: where systems connect or are wired together
  - test_plan: testing tasks and their coverage targets
```

Write the parsed structure to: `{OUTPUT_DIR}/roadmap-structure.md`

### Step 0.4: Build Domain Taxonomy

From the extracted requirements AND roadmap structure, identify all distinct domains/disciplines present. A domain is a coherent area of concern where requirements cluster naturally.

**Domain Detection Heuristic**:
1. Group requirements by their `domain` tag
2. If a domain has fewer than 3 requirements, merge it with the closest related domain
3. If a domain has more than 15 requirements, split it by sub-domain (e.g., "backend" into "backend-api", "backend-services", "backend-models")
4. Ensure every requirement belongs to exactly one primary domain (cross-cutting requirements are assigned to their primary domain but flagged for secondary review)
5. Maximum 20 domains (agent limit)
6. Minimum 2 domains (below this, validation is trivial and can be done inline)

**Default Domain Categories** (use as starting vocabulary; adapt to actual content):
- `dependencies` — package management, version pinning, compatibility
- `infrastructure` — Docker, Kubernetes, cloud resources, networking
- `database` — schema, migrations, data models, queries, extensions
- `backend-api` — routes, endpoints, request/response contracts
- `backend-services` — business logic, service layer, orchestration
- `backend-models` — ORM models, data access layer
- `frontend-ui` — components, pages, visual elements
- `frontend-state` — state management, stores, data flow
- `frontend-integration` — API clients, WebSocket connections, streaming
- `ml-models` — model training, inference, evaluation
- `ml-pipeline` — data processing, feature engineering, pipelines
- `ai-agents` — LLM integration, agent orchestration, tools
- `config` — environment variables, settings, feature flags
- `ci-cd` — pipelines, workflows, deployment automation
- `testing` — test plans, test cases, coverage requirements
- `security` — auth, encryption, access control, vulnerability mitigation
- `observability` — logging, metrics, monitoring, alerting
- `performance` — optimization targets, benchmarks, load requirements
- `documentation` — docs, guides, API references
- `integration` — cross-system wiring, contracts, boundaries

Write the domain taxonomy to: `{OUTPUT_DIR}/domain-taxonomy.md`

---

## PHASE 1: AGENT DECOMPOSITION

**Goal**: Assign requirements to agents for parallel validation. Maximize coverage, minimize overlap.

### Step 1.1: Create Agent Assignments

For each domain identified in Step 0.4, create one agent assignment:

```
AGENT-{N}:
  - id: A{N} (e.g., A1, A2, ... A20)
  - domain: domain name
  - requirements: list of requirement IDs assigned to this agent
  - requirement_count: number of requirements
  - spec_sections: which spec sections this agent must read
  - roadmap_sections: which roadmap sections this agent must check
  - cross_cutting_reqs: requirements from other domains that touch this domain
  - expected_output: {OUTPUT_DIR}/agent-{N}-{domain}.md
```

### Step 1.2: Verify Complete Assignment

**Coverage check**: Every requirement ID from the extraction must appear in exactly one agent's primary assignment. Cross-cutting requirements must appear in at least one agent's `cross_cutting_reqs` list in addition to their primary assignment.

If any requirement is unassigned, assign it to the closest domain agent. If any requirement is assigned to multiple primary agents, resolve the conflict by domain affinity.

### Step 1.3: Identify Cross-Cutting Concerns

Build a cross-cutting concern matrix:

```
CROSS_CUTTING_MATRIX:
  - concern: description of the cross-cutting requirement
  - primary_agent: agent with primary responsibility
  - secondary_agents: agents that must also validate their portion
  - integration_risk: HIGH | MEDIUM | LOW
```

Write agent assignments and cross-cutting matrix to: `{OUTPUT_DIR}/agent-assignments.md`

---

## PHASE 2: PARALLEL AGENT EXECUTION

**Goal**: Spawn up to 20 parallel agents. Each agent validates its assigned requirements against the roadmap.

### Agent Execution Protocol

Each agent receives the following instruction set. Spawn all agents simultaneously using parallel tool calls.

---

#### BEGIN AGENT INSTRUCTION SET

**You are Agent {AGENT_ID}, validating the `{DOMAIN}` domain.**

**Your inputs:**
- Spec files: {SPEC_PATHS}
- Roadmap: {ROADMAP_PATH}
- Your assigned requirements: {REQUIREMENT_IDS}
- Cross-cutting requirements to check: {CROSS_CUTTING_REQ_IDS}
- Output file: {OUTPUT_FILE}

**Your task**: For EVERY requirement in your assignment, determine whether the roadmap fully covers it. Produce a per-requirement coverage assessment with evidence.

**Procedure**:

1. **Read** the spec sections relevant to your assigned requirements. Extract the exact text of each requirement, its acceptance criteria, and any sub-requirements.

2. **Read** the roadmap sections where these requirements should appear. Search the ENTIRE roadmap, not just the sections you expect — requirements may be addressed in unexpected locations.

3. **For each requirement**, produce a coverage assessment:

```
### REQ-{ID}: {requirement title}

- **Spec source**: {file}:{line or section}
- **Spec text**: "{exact quote from spec}"
- **Status**: COVERED | PARTIAL | MISSING | CONFLICTING
- **Evidence**:
  - Roadmap location: {file}:{line range} or [MISSING]
  - Roadmap text: "{exact quote from roadmap}" or [MISSING]
  - Match quality: EXACT | SEMANTIC | WEAK | NONE
- **Sub-requirements**: (if applicable)
  - {sub-req-1}: COVERED | PARTIAL | MISSING — evidence: {quote}
  - {sub-req-2}: COVERED | PARTIAL | MISSING — evidence: {quote}
- **Acceptance criteria coverage**: (if applicable)
  - {AC-1}: COVERED | MISSING — roadmap task: {task ID}
  - {AC-2}: COVERED | MISSING — roadmap task: {task ID}
- **Finding**: (only if status is not COVERED)
  - Severity: CRITICAL | HIGH | MEDIUM | LOW
  - Gap description: {what is missing or wrong}
  - Impact: {what happens if this gap is not addressed}
  - Recommended correction: {specific fix with roadmap locations}
```

4. **Coverage status definitions** (apply strictly):
   - **COVERED**: The roadmap contains a task or set of tasks that, when executed, will fully satisfy the requirement. All sub-requirements and acceptance criteria are addressed. Evidence includes exact roadmap line references.
   - **PARTIAL**: The roadmap addresses some aspects of the requirement but omits specific sub-requirements, acceptance criteria, or implementation details that the spec mandates. The gap must be precisely identified.
   - **MISSING**: The requirement has no corresponding roadmap coverage. No task, gate, or verification step addresses it.
   - **CONFLICTING**: The roadmap contains coverage that contradicts the spec. The roadmap says one thing; the spec says another. Both quotes must be provided.

5. **Evidence standards** (mandatory):
   - Every COVERED claim must cite a specific roadmap line range and quote the relevant text.
   - Every PARTIAL/MISSING/CONFLICTING finding must quote both the spec requirement and the roadmap text (or lack thereof).
   - Do not infer coverage. If a requirement is not explicitly addressed in the roadmap, it is MISSING even if a reasonable developer might implement it during an adjacent task.
   - Semantic equivalence counts as coverage ONLY if the roadmap text clearly addresses the same concern with equivalent specificity. Vague roadmap language does not satisfy precise spec language.

6. **Cross-cutting validation**: For each requirement in your `cross_cutting_reqs` list, verify that YOUR domain's portion of that requirement is covered in the roadmap. Report only the portion relevant to your domain.

7. **Integration point validation**: For requirements that involve connecting to other systems/components, verify:
   - The roadmap specifies HOW the integration is wired (not just WHAT integrates)
   - Interface contracts are defined or referenced
   - Startup/initialization sequences are specified
   - Error handling at boundaries is addressed
   - Both sides of the integration are covered (your side + confirmation the other side is in another agent's scope)

8. **Produce summary statistics**:
```
## Agent {AGENT_ID} Summary — {DOMAIN}
- Total requirements: {N}
- COVERED: {N} ({percentage}%)
- PARTIAL: {N} ({percentage}%)
- MISSING: {N} ({percentage}%)
- CONFLICTING: {N} ({percentage}%)
- Coverage score: {COVERED + 0.5*PARTIAL} / {TOTAL} = {percentage}%
- Findings: {N} CRITICAL, {N} HIGH, {N} MEDIUM, {N} LOW
- Cross-cutting issues: {N}
- Integration concerns: {N}
```

9. **Write your complete report** to your output file using incremental writes: create the file with the header first, then append each requirement assessment one at a time. NEVER accumulate the entire report in context and write it all at once.

#### END AGENT INSTRUCTION SET

---

### Spawn Protocol

Spawn all agents simultaneously. Each agent is independent — they read the same source documents but write to separate output files. There are no dependencies between agents during Phase 2.

**Critical**: If the number of domains exceeds 20, merge the smallest domains until you have exactly 20 agents. If fewer than 20, use fewer agents — do not create artificial splits just to reach 20.

---

## PHASE 3: CONSOLIDATION

**Goal**: After all agents complete, merge their findings into a unified validation report.

### Step 3.1: Collect Agent Reports

Read every agent output file from `{OUTPUT_DIR}/agent-{N}-{domain}.md`. Verify each agent completed its assessment (check for summary statistics at the end of each file).

If any agent failed to complete, note the failure and the unvalidated requirements.

### Step 3.2: Build Unified Gap Registry

Merge all findings from all agents into a single, deduplicated gap registry. For each gap:

```
### GAP-{SEVERITY_PREFIX}{N}: {title}

- **ID**: GAP-{SEVERITY_PREFIX}{N} (C = critical, H = high, M = medium, L = low)
- **Severity**: CRITICAL | HIGH | MEDIUM | LOW
- **Source agent(s)**: {agent IDs that reported this gap}
- **Requirement(s)**: {REQ IDs affected}
- **Spec reference**: {file}:{line/section} — "{quote}"
- **Roadmap reference**: {file}:{line/section} — "{quote}" or [MISSING]
- **Gap description**: {precise description of what is missing, wrong, or conflicting}
- **Impact**: {what happens if this gap is not addressed — be specific about failure modes}
- **Recommended correction**: {exact fix, including which files to edit and what to change}
- **Effort estimate**: TRIVIAL (wording fix) | SMALL (add task/criterion) | MEDIUM (restructure section) | LARGE (add phase/major rework)
```

**Severity Definitions** (apply consistently):

- **CRITICAL**: A requirement is entirely missing from the roadmap AND its absence would cause system failure, data loss, security vulnerability, or render a core feature non-functional. Blocks release.
- **HIGH**: A requirement is missing or materially misrepresented in the roadmap AND its absence would cause incorrect behavior, test gaps for critical paths, or specification non-compliance that would be caught in integration/production. Should block tasklist generation.
- **MEDIUM**: A requirement is partially covered or a verification criterion is missing. The implementation might still be correct if a developer reads the spec, but the roadmap does not guarantee it. Remediation recommended before tasklist generation.
- **LOW**: A minor discrepancy in wording, ordering, or precision. The intent is captured but the specificity is insufficient. Can be remediated during or after tasklist generation.

**Deduplication Rules**:
- If two agents report the same gap from different perspectives, merge into one finding with both agents cited.
- If two findings address different aspects of the same underlying issue, keep them separate but link them.
- If findings contradict each other, escalate to the adversarial pass (Phase 4).

### Step 3.3: Cross-Cutting Concern Validation

For each cross-cutting concern from the matrix (Phase 1, Step 1.3):
1. Check that the primary agent validated the core requirement
2. Check that each secondary agent validated their domain's portion
3. If any portion is uncovered, add a gap to the registry
4. Verify that the integration between domains is explicitly addressed in the roadmap

### Step 3.4: Integration Wiring Audit

Scan the roadmap for all points where systems/components connect. For each integration point:

```
INTEGRATION-{N}:
  - system_a: {component/service name}
  - system_b: {component/service name}
  - interface: {API contract, data format, protocol}
  - roadmap_coverage:
    - system_a_side: COVERED | MISSING — {evidence}
    - system_b_side: COVERED | MISSING — {evidence}
    - wiring_task: COVERED | MISSING — {evidence}
    - error_handling: COVERED | MISSING — {evidence}
    - initialization_sequence: COVERED | MISSING — {evidence}
  - verdict: FULLY_WIRED | PARTIALLY_WIRED | UNWIRED
```

Report any PARTIALLY_WIRED or UNWIRED integrations as gaps.

### Step 3.5: Compute Coverage Scores

**Per-Domain Coverage**:
```
| Domain | Total Reqs | Covered | Partial | Missing | Conflicting | Score |
|--------|-----------|---------|---------|---------|-------------|-------|
| {domain} | {N} | {N} | {N} | {N} | {N} | {pct}% |
```

**Aggregate Coverage**:
```
Total requirements: {N}
Covered: {N} ({pct}%)
Partial: {N} ({pct}%)
Missing: {N} ({pct}%)
Conflicting: {N} ({pct}%)

Weighted coverage score: {(COVERED + 0.5*PARTIAL) / TOTAL * 100}%
Confidence interval: +/- {margin}%
```

**Confidence interval calculation**:
- Start at +/- 2% (base uncertainty from semantic matching)
- Add +1% for every 10 requirements validated (scale factor)
- Add +2% for each agent that failed to complete
- Add +1% for each cross-cutting concern with incomplete secondary validation
- Cap at +/- 10%

### Step 3.6: Generate Consolidated Report

Write the consolidated report to: `{OUTPUT_DIR}/validation-report.md`

**Report structure**:

```markdown
# Roadmap Validation Report

**Generated**: {date}
**Roadmap**: {ROADMAP_PATH}
**Specs**: {SPEC_PATHS}
**Agents**: {N} ({list of domains})
**Method**: Parallel domain-decomposed validation with adversarial consolidation

## Executive Summary

- **Verdict**: PASS | PASS_WITH_REMEDIATION | FAIL
- **Coverage score**: {pct}% (+/- {margin}%)
- **Total findings**: {N} ({breakdown by severity})
- **Domains validated**: {N}/{N}
- **Cross-cutting concerns**: {N} checked, {N} with gaps
- **Integration points**: {N} checked, {N} fully wired, {N} with gaps

## Verdict Criteria
- PASS: 100% coverage, 0 CRITICAL, 0 HIGH findings
- PASS_WITH_REMEDIATION: >=95% coverage, 0 CRITICAL, <=3 HIGH findings (all with clear fixes)
- FAIL: <95% coverage OR any CRITICAL finding OR >3 HIGH findings

## Coverage by Domain
{per-domain table from Step 3.5}

## Gap Registry
{all gaps from Step 3.2, ordered by severity then domain}

## Cross-Cutting Concern Report
{from Step 3.3}

## Integration Wiring Audit
{from Step 3.4}

## Agent Reports Index
{links to individual agent output files}

## Remediation Plan
{ordered list of gaps to fix, grouped by effort level}
```

---

## PHASE 4: ADVERSARIAL PASS

**Goal**: A single adversarial agent reviews the entire validation to catch gaps that the parallel agents missed. This is the final quality gate.

### Step 4.1: Adversarial Agent Instructions

After the consolidated report is written, execute the following adversarial review:

1. **Read the consolidated report** (`{OUTPUT_DIR}/validation-report.md`)
2. **Read the original spec(s)** again — fresh eyes, not relying on agent reports
3. **Read the roadmap** again — fresh eyes

4. **Challenge every COVERED assessment**: For each requirement marked COVERED by the parallel agents, ask:
   - Does the roadmap task actually produce the deliverable the spec requires?
   - Is the roadmap's acceptance criterion as strict as the spec's?
   - Could a developer execute the roadmap task and still not satisfy the spec requirement?
   - Are there implicit sub-requirements the agents missed?
   - Is the sequencing correct (does the roadmap put prerequisite tasks before dependent tasks)?

5. **Search for orphan requirements**: Requirements that exist in the spec but were not extracted in Phase 0 — perhaps buried in prose, footnotes, appendices, or examples.

6. **Search for orphan roadmap tasks**: Tasks in the roadmap that do not trace to any spec requirement. These may indicate:
   - Scope creep (roadmap adds work not in spec)
   - Missing spec requirements (the roadmap author added something the spec should have included)
   - Implementation details that don't need spec tracing

7. **Validate sequencing and dependencies**:
   - Are spec-mandated ordering constraints reflected in the roadmap?
   - Are one-way-door procedures (irreversible operations) properly gated?
   - Are exit criteria from one phase satisfied before the next phase begins?

8. **Check for silent assumptions**:
   - Does the roadmap assume capabilities, services, or infrastructure that the spec does not mention?
   - Does the roadmap assume a development environment or toolchain that isn't specified?
   - Are there implicit dependencies between roadmap tasks that should be explicit?

9. **Validate test coverage mapping**:
   - Does every spec test case appear in the roadmap with matching scope?
   - Are the roadmap's test numbering and descriptions consistent with the spec's?
   - Are test prerequisites (fixtures, data, environments) addressed?
   - Is the total test count consistent between spec and roadmap?

10. **Produce adversarial findings**:

For each new finding not already in the gap registry:
```
### ADV-{N}: {title}

- **Type**: MISSED_GAP | FALSE_COVERAGE | SEQUENCING_ERROR | ORPHAN_REQUIREMENT | ORPHAN_TASK | SILENT_ASSUMPTION | TEST_MISMATCH
- **Severity**: CRITICAL | HIGH | MEDIUM | LOW
- **Description**: {what was missed and why}
- **Evidence**: {spec quote + roadmap quote or lack thereof}
- **Impact**: {consequence of not addressing}
- **Recommended correction**: {specific fix}
```

11. **Update the consolidated report**: If the adversarial pass finds new gaps:
   - Add them to the gap registry with `[ADV]` prefix
   - Recalculate coverage scores
   - Update the verdict if severity thresholds change
   - Document what the parallel agents missed and why

Write adversarial findings to: `{OUTPUT_DIR}/adversarial-review.md`
Update: `{OUTPUT_DIR}/validation-report.md` with final scores and verdict.

---

## PHASE 5: REMEDIATION RECOMMENDATIONS

**Goal**: Produce an actionable remediation plan for all findings.

### Step 5.1: Prioritize Remediations

Order all gaps (from both parallel and adversarial passes) by:
1. Severity (CRITICAL first)
2. Effort (TRIVIAL before LARGE — quick wins first within same severity)
3. Dependency (if fixing gap A makes gap B easier, do A first)

### Step 5.2: Generate Patch Checklist

For each gap, produce a concrete remediation item:

```
- [ ] **{GAP_ID}** ({severity}, {effort}): {one-line description}
  - File: {roadmap path}:{line range}
  - Action: {ADD | EDIT | MOVE | SPLIT | REMOVE}
  - Change: "{exact text to add/change}"
  - Verification: {how to confirm the fix is correct}
```

### Step 5.3: Compute Remediation Impact

```
If all remediations are applied:
  - Projected coverage: {new_pct}%
  - Projected findings: {new_count} (should be 0 CRITICAL, 0 HIGH)
  - Projected verdict: {PASS | PASS_WITH_REMEDIATION}
  - Estimated effort: {total hours/days}
```

Write remediation plan to: `{OUTPUT_DIR}/remediation-plan.md`

---

## OUTPUT FILE MANIFEST

At completion, the following files will exist in `{OUTPUT_DIR}/`:

| File | Phase | Content |
|------|-------|---------|
| `extraction.md` | 0 | Structured requirement registry |
| `roadmap-structure.md` | 0 | Parsed roadmap structure |
| `domain-taxonomy.md` | 0 | Domain decomposition |
| `agent-assignments.md` | 1 | Agent-to-domain mapping with requirement lists |
| `agent-{N}-{domain}.md` | 2 | Per-agent validation report (up to 20 files) |
| `validation-report.md` | 3 | Consolidated validation report |
| `adversarial-review.md` | 4 | Adversarial pass findings |
| `remediation-plan.md` | 5 | Actionable patch checklist |

---

## EXECUTION RULES

These rules govern all phases. Violations produce incorrect results.

### R1: Artifact-Based Workflow
Work from files, not memory. Every agent writes its findings to its output file. The orchestrator reads files to consolidate. No findings exist only in context.

### R2: Incremental Writing
NEVER accumulate content in context and write a large file at once. For any file >50 lines: create with header first, then append sections one at a time using Edit. This prevents token-limit truncation that silently loses findings.

### R3: Evidence-Based Claims Only
Every coverage claim (COVERED, PARTIAL, MISSING, CONFLICTING) must cite specific file:line references and quote the relevant text. "Implied" or "likely covered" is not evidence. If you cannot find explicit roadmap text addressing a requirement, the status is MISSING.

### R4: Spec is Source of Truth
When the roadmap conflicts with the spec, the spec wins. The roadmap is the document under test; the spec defines correctness. Never adjust a requirement to match the roadmap.

### R5: No False Positives
Do not invent findings. If a requirement is genuinely covered, mark it COVERED. Inflating finding counts reduces trust in the validation.

### R6: No False Negatives
Do not overlook gaps to produce a better coverage score. Every gap matters. A missed HIGH finding that reaches implementation costs 10x more to fix than catching it here.

### R7: Quote, Don't Paraphrase
When citing spec or roadmap text as evidence, use exact quotes with line numbers. Paraphrasing introduces interpretation that may be incorrect.

### R8: Parallel Agents Are Independent
Agents do not communicate during Phase 2. Each agent reads source documents independently and writes to its own file. The orchestrator handles deduplication in Phase 3.

### R9: Complete One Phase Before Starting the Next
Do not begin Phase 1 before Phase 0 is complete. Do not begin Phase 2 before Phase 1 is complete. Each phase depends on the outputs of the previous phase.

### R10: Report All Uncertainty
If a requirement is ambiguous, if coverage is debatable, or if a finding could go either way, document the uncertainty explicitly. Do not silently pick one interpretation.

### R11: Cross-Cutting Requirements Get Double Coverage
Every cross-cutting requirement must be validated by its primary agent AND checked by at least one secondary agent. If the secondary agent finds a gap the primary missed, it becomes a finding.

### R12: Integration Points Require Both Sides
An integration point is only COVERED if both sides are addressed in the roadmap. Covering the client but not the server (or vice versa) is PARTIAL at best.

### R13: Test Fidelity Is Exact
Test case validation requires exact matching of: test number, test description, test scope, expected assertions, and test prerequisites. A roadmap test that shares a number but has a different description from the spec is a CONFLICTING finding.

### R14: Sequencing Matters
If the spec mandates ordering (e.g., "do A before B", "gate on A passing before starting B"), the roadmap must reflect that ordering. Correct tasks in wrong order is a finding.

### R15: Preserve All Artifacts
Do not delete intermediate files after the final report is written. The agent reports, extraction, and adversarial review serve as the evidence trail for all claims.

---

## QUICK START

To execute this validation, provide the inputs and run:

```
Inputs:
  ROADMAP_PATH = <path to roadmap>
  SPEC_PATHS = [<path to spec 1>, <path to spec 2 (optional)>, ...]
  OUTPUT_DIR = <path for output> (optional, defaults to {roadmap_dir}/validation/)
  EXCLUSIONS = [] (optional)

Then say: "Execute the roadmap validation using the prompt at {this file's path}"
```

The orchestrator will execute Phases 0-5 automatically, spawning parallel agents in Phase 2, and produce a complete validation report with coverage scores, gap registry, and remediation plan.

---

## APPENDIX A: DOMAIN DETECTION EXAMPLES

These examples show how the domain taxonomy adapts to different project types.

**Example 1: Backend API Feature**
Domains detected: `dependencies`, `database`, `backend-api`, `backend-services`, `config`, `testing`, `ci-cd`

**Example 2: Full-Stack Feature**
Domains detected: `backend-api`, `backend-services`, `database`, `frontend-ui`, `frontend-state`, `frontend-integration`, `config`, `testing`, `ci-cd`, `documentation`

**Example 3: Infrastructure Migration**
Domains detected: `infrastructure`, `database`, `ci-cd`, `config`, `security`, `observability`, `testing`, `documentation`

**Example 4: ML Pipeline Feature**
Domains detected: `ml-models`, `ml-pipeline`, `data`, `backend-api`, `infrastructure`, `config`, `testing`, `performance`, `observability`

**Example 5: Multi-Agent AI System**
Domains detected: `ai-agents`, `backend-services`, `database`, `config`, `ml-models`, `frontend-integration`, `testing`, `performance`, `observability`, `security`

---

## APPENDIX B: HANDLING EDGE CASES

### B1: Spec Has No Explicit Requirement IDs
Generate sequential IDs: `REQ-001`, `REQ-002`, etc. Maintain a mapping table from generated ID to spec location (file:line, section heading, or paragraph).

### B2: Roadmap Uses Different Terminology Than Spec
Create a terminology mapping during Phase 0. If the spec says "checkpoint persistence" and the roadmap says "state durability", document the equivalence and use it consistently during validation.

### B3: Multiple Specs With Overlapping Scope
When two specs define the same requirement differently, flag it as a spec-level conflict (not a roadmap finding). Note it in the extraction but do not penalize the roadmap for spec inconsistency.

### B4: Roadmap Contains Work Not In Any Spec
Document as orphan tasks in the adversarial pass. These are not gaps but may indicate scope creep or missing spec coverage. Report them for the user's awareness without assigning severity.

### B5: Spec References External Documents
If the spec references external standards, RFCs, or other documents that are not provided as inputs, note the dependency and mark requirements derived from those references as "UNVERIFIABLE — external reference not provided."

### B6: Very Large Specs (>500 Requirements)
If total requirements exceed 500, increase the minimum domain count to ensure no agent handles more than 30 requirements. Split large domains aggressively. Consider spawning the maximum 20 agents.

### B7: Very Small Specs (<10 Requirements)
If total requirements are fewer than 10, use 2-3 agents maximum. The adversarial pass becomes proportionally more important for small specs since there is less redundancy in parallel validation.

### B8: Roadmap Is a Tasklist (Not a Traditional Roadmap)
Treat each task as a roadmap section. The validation still applies — each task must trace to spec requirements, and all spec requirements must be covered by tasks.

### B9: Spec Contains "Nice to Have" or "Future" Items
Only validate requirements marked as in-scope for the release/version the roadmap targets. Flag out-of-scope items in the extraction with `in_scope: false` and exclude them from coverage calculations.

### B10: Agent Fails or Times Out
If an agent fails to produce output, its assigned requirements become "UNVALIDATED." Add the count to the confidence interval. The adversarial pass should attempt to cover the failed agent's scope, but at lower depth.
