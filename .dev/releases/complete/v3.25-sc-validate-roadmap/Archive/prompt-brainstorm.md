# Universal Roadmap-vs-Spec Validation Prompt

> **Usage**: Copy this entire file as a prompt. Provide two inputs when invoking:
> - `ROADMAP_PATH` — path to the roadmap file under validation
> - `SPEC_PATHS` — one or more paths to authoritative specification files (release spec, tech spec, PRD, etc.)
>
> Example invocation context:
> ```
> ROADMAP_PATH=".dev/releases/current/feature-X/roadmap.md"
> SPEC_PATHS=[".dev/releases/current/feature-X/release-spec.md", ".dev/releases/current/feature-X/tech-spec.md"]
> OUTPUT_DIR=".dev/releases/current/feature-X/validation/"
> ```

---

## 0. Mission

You are a **Roadmap Completeness Validator**. Your mission is to prove — or disprove — that the roadmap at `ROADMAP_PATH` covers 100% of the requirements, acceptance criteria, architectural decisions, risk mitigations, test plans, integration contracts, and operational concerns defined in the specifications at `SPEC_PATHS`.

You are adversarial. You assume the roadmap is incomplete until proven otherwise. Every requirement is guilty of being missing until evidence places it in the roadmap with sufficient specificity.

**Success condition**: A consolidated report with per-discipline coverage scores, an itemized gap list sorted by severity, and a binary GO / NO-GO recommendation for whether the roadmap is ready to generate tasklists from.

---

## 1. Inputs and Bootstrapping

### 1.1 Read All Source Documents

Before ANY analysis, read the following files completely:

1. **All spec files** at `SPEC_PATHS` — read each one end-to-end.
2. **The roadmap** at `ROADMAP_PATH` — read end-to-end.
3. **Any files referenced by the specs** (e.g., tech specs referenced from a release spec, investigation artifacts cited as evidence). Follow one level of references. Do NOT recursively spider — one hop only.

### 1.2 Extract the Requirement Universe

From the spec files, build a **Requirement Universe** — the complete set of items the roadmap must cover. Extract ALL of the following categories. Not every spec will have every category; extract what exists.

| Category | What to Extract | Example |
|----------|----------------|---------|
| **Functional Requirements (FR)** | Every FR with its ID, description, and acceptance criteria | FR-R1.2: AsyncPostgresSaver replaces MemorySaver; AC7: restart persistence |
| **Non-Functional Requirements (NFR)** | Every NFR with target metrics and measurement method | NFR-R1.1: 50 concurrent conversations without pool exhaustion |
| **Acceptance Criteria (AC)** | Every AC attached to any FR/NFR — these are the atomic unit of verification | AC7: 4th message after restart retrieves all 3 prior messages |
| **Architectural Decisions** | Numbered decisions, technology choices, pattern selections | Decision 1: Pure AsyncPostgresSaver (not hybrid) |
| **Open Questions / Spikes** | Questions the spec says must be resolved, with expected resolution location | OQ-1 (F6): Verify AsyncPostgresSaver API surface |
| **Risks** | Named risks with mitigation strategies and contingency plans | Risk 2: Docker image swap — ONE-WAY DOOR |
| **Test Plan** | Every individual test case with its ID, description, type, and validation target | Test 7: Cross-process checkpoint sharing |
| **Data Models** | Tables, columns, types, constraints, indexes, migrations | cross_session_context: 9 columns, nullable vector(768), (user_id, project_id) index |
| **API Contracts** | Endpoints, methods, request/response schemas, error codes | PATCH /conversations/{id}/status — 200 on valid, 400 on invalid |
| **Integration Points** | Cross-system hooks, wiring, dependency flows between components | Checkpointer factory consumed by BaseAgent and SwarmOrchestrator |
| **Configuration** | Config keys, defaults, environment variables, constants | CHECKPOINT_POSTGRES_DSN default, Redis namespace prefixes |
| **File Changes** | Specific files the spec says must be modified, with line references if given | base_agent.py:30, swarm_orchestrator.py:99, 6 compose files |
| **Quality Gates** | Phase gates, stop conditions, exit criteria | Gate B: Infrastructure Readiness — 6 pass criteria, 4 stop conditions |
| **Inter-Release Contracts** | What this release promises to deliver for future releases | R1 delivers nullable vector(768) column; R2 populates it |
| **Success Criteria** | Numbered SC items that serve as the release acceptance checklist | SC-1 through SC-15 |
| **Sequencing Constraints** | Explicit ordering requirements (must-before relationships) | Task 3 (regression canary) BEFORE Task 4 (Docker image swap) |
| **LOC / Effort Budgets** | Size estimates the spec declares as authoritative | 250-350 LOC budget for R1 production code |

**Write the extracted Requirement Universe to disk** at `OUTPUT_DIR/requirement-universe.md` before proceeding. This file is the source of truth for all subsequent validation.

Format: One section per category. Within each section, one numbered item per requirement. Include the spec source reference (file:section or file:line) for each item.

### 1.3 Extract the Roadmap Structure

From the roadmap, extract:

1. **Phases** — numbered implementation phases with their objectives and exit gates
2. **Tasks** — numbered tasks within each phase, with their requirement tag references
3. **Gates** — verification gates with pass/stop criteria
4. **Milestones** — phase completion markers
5. **Risk mitigations** — how risks are addressed
6. **Integration points** — cross-phase dependencies
7. **Test assignments** — which tests are placed in which phases

**Write the extracted Roadmap Structure to disk** at `OUTPUT_DIR/roadmap-structure.md`.

---

## 2. Discipline Decomposition (Auto-Detection)

You must decompose the validation work into **disciplines** — non-overlapping domains that partition the Requirement Universe. You will spawn one parallel agent per discipline, up to a maximum of 20.

### 2.1 Auto-Detection Algorithm

Do NOT use hardcoded discipline names. Instead, derive them from the actual content:

**Step 1: Cluster requirements by domain signal.**

For each requirement in the Requirement Universe, identify its primary domain using these signals:
- File paths mentioned (e.g., `docker-compose*.yml` → Infrastructure, `base_agent.py` → Agent Core)
- Technology referenced (e.g., Alembic → Database/Migrations, Redis → Caching, CI/CD → DevOps)
- Requirement type (e.g., NFR about latency → Performance, NFR about auth → Security)
- Spec section headers (e.g., "Test Plan" → Testing, "Data Model" → Schema/Data)
- System boundaries (e.g., frontend vs backend vs infrastructure vs external services)

**Step 2: Merge small clusters.**

If a cluster has fewer than 3 requirements, merge it into the most related larger cluster. The goal is disciplines large enough to justify a dedicated agent but small enough for thorough validation.

**Step 3: Split oversized clusters.**

If a cluster has more than 25 requirements, split it along natural sub-boundaries (e.g., "Testing" might split into "Unit Tests" and "Integration Tests & Gates").

**Step 4: Ensure non-overlapping coverage.**

Every requirement in the Universe must belong to exactly one discipline. If a requirement touches multiple disciplines (cross-cutting concern), assign it to the discipline where it has the MOST impact, and add it to the cross-cutting concerns list for the consolidation phase.

**Step 5: Cap at 20 disciplines.**

If you have more than 20 clusters after Steps 1-4, merge the smallest pairs until you reach 20 or fewer.

### 2.2 Output the Discipline Map

**Write to disk** at `OUTPUT_DIR/discipline-map.md`:

```markdown
# Discipline Map

## Discipline Assignments

| # | Discipline Name | Requirement Count | Spec Sections | Key Files |
|---|----------------|-------------------|---------------|-----------|
| D1 | [name] | [N] | [sections] | [files] |
| D2 | ... | ... | ... | ... |

## Cross-Cutting Concerns

| Requirement | Primary Discipline | Also Touches |
|------------|-------------------|--------------|
| [req] | D3 | D1, D7 |

## Unassigned Requirements (MUST BE ZERO)

[If any requirements are unassigned, list them here. This is a validation failure.]
```

---

## 3. Parallel Agent Spawn — Per-Discipline Validation

Spawn one agent per discipline. All agents run in parallel. Each agent is independent and writes its own output file.

### 3.1 Agent Instructions (applies to every agent)

You are **Agent D[N]: [Discipline Name]**.

**Your inputs:**
- The Requirement Universe (filtered to your discipline's requirements)
- The full roadmap
- The full spec files (for context when tracing references)

**Your task:**
For every requirement assigned to your discipline, determine whether the roadmap covers it. Produce a coverage verdict for each requirement.

#### 3.1.1 Coverage Verdicts

Each requirement gets exactly one verdict:

| Verdict | Symbol | Definition |
|---------|--------|------------|
| **COVERED** | PASS | The roadmap contains a task, gate criterion, or explicit statement that addresses this requirement with sufficient specificity. Evidence must cite roadmap line/section. |
| **PARTIAL** | WARN | The roadmap addresses the requirement but is missing specificity, a sub-criterion, or a detail that the spec explicitly requires. Describe what is missing. |
| **MISSING** | FAIL | The requirement does not appear in the roadmap at all, or the roadmap assigns its slot to a different requirement (substitution). |
| **CONTRADICTED** | CRIT | The roadmap contains content that directly contradicts the spec requirement (wrong value, wrong sequence, wrong file, etc.). |
| **IMPLICIT** | INFO | The requirement is not explicitly stated but would be satisfied as a natural side-effect of a covered task. Flag for human review — implicit coverage is fragile. |

#### 3.1.2 Evidence Standards

Every verdict MUST include:

1. **Spec reference**: File, section, line number, or quote from the spec
2. **Roadmap reference** (if COVERED/PARTIAL/CONTRADICTED): File, section, line number, task ID, or quote from the roadmap
3. **Gap description** (if PARTIAL/MISSING/CONTRADICTED): What specifically is absent or wrong
4. **Impact assessment**: What happens if this gap reaches implementation — will it cause a bug, a missing feature, a test gap, a security hole, or a silent regression?
5. **Confidence**: HIGH (direct textual evidence), MEDIUM (evidence requires inference across sections), LOW (evidence is circumstantial or absent)

#### 3.1.3 Severity Levels for Gaps

| Severity | Criteria | Examples |
|----------|----------|---------|
| **CRITICAL** | Roadmap contradicts spec, or a core deliverable / acceptance test is missing | North Star test absent; wrong sequencing of irreversible operations; security requirement contradicted |
| **HIGH** | A spec-defined requirement or test case is absent from the roadmap entirely | Spec test missing; data model column omitted; required migration absent |
| **MEDIUM** | Requirement is partially covered — present but missing specificity, sub-criteria, or precision | Gate criterion incomplete; LOC estimate inconsistent; timing/sequencing deviation for non-critical tasks |
| **LOW** | Cosmetic, traceability, or documentation gap that does not affect implementation correctness | Requirement ID mapping absent; annotations missing; supplementary tests not labeled |
| **INFO** | Observation that may warrant human review but is not a gap | Roadmap adds coverage beyond spec; implicit coverage noted |

#### 3.1.4 Specific Validation Checks

Beyond simple presence/absence, each agent MUST check:

1. **Acceptance Criteria Atomicity**: If a spec FR has 3 acceptance criteria, all 3 must appear in the roadmap — not just the FR header.
2. **Test Identity Preservation**: If the spec defines Test N with a specific description, the roadmap's Test N must match that description. A substitution (same number, different test) is a HIGH gap.
3. **Sequencing Fidelity**: If the spec defines A-before-B ordering, the roadmap must preserve that order. Phase/task placement that violates sequencing is a CRITICAL gap if the sequence involves irreversible operations, HIGH otherwise.
4. **Data Model Completeness**: Every column, type, constraint, index, and migration detail in the spec must appear in the roadmap. A missing column is HIGH. A wrong type is CRITICAL.
5. **Contract Precision**: API endpoints must match method, path, request schema, response schema, and error codes. Any mismatch is HIGH or CRITICAL depending on whether it changes behavior.
6. **Gate Completeness**: Every spec-defined gate must appear with both pass criteria AND stop conditions. Missing stop conditions are HIGH (you lose the safety net).
7. **Risk Coverage**: Every spec risk must have a corresponding mitigation in the roadmap. Missing mitigation for a CRITICAL risk is CRITICAL; for HIGH risk is HIGH.
8. **Configuration Exactness**: Config keys, defaults, and environment variable names must match exactly. A wrong default is HIGH.
9. **File Change Coverage**: If the spec says "modify file X at line Y", the roadmap must include a task that targets file X. Missing file changes are HIGH.
10. **Inter-Release Contract**: Any promise to a future release must be explicitly preserved in the roadmap. Missing contracts are HIGH (they create invisible debt).

#### 3.1.5 Agent Output Format

Each agent writes its report to `OUTPUT_DIR/agent-D[N]-[discipline-slug].md`:

```markdown
# Agent D[N]: [Discipline Name] — Validation Report

**Generated**: [timestamp]
**Requirements in scope**: [count]
**Verdict summary**: [PASS: N, WARN: N, FAIL: N, CRIT: N, INFO: N]
**Coverage score**: [PASS / (PASS + WARN + FAIL + CRIT)] as percentage
**Confidence**: [HIGH/MEDIUM/LOW — overall confidence in this agent's findings]

## Coverage Matrix

| # | Requirement | Verdict | Severity | Roadmap Ref | Confidence | Notes |
|---|------------|---------|----------|-------------|------------|-------|
| 1 | [requirement ID + brief description] | PASS/WARN/FAIL/CRIT/INFO | -/LOW/MED/HIGH/CRIT | [roadmap task/section] | HIGH/MED/LOW | [brief note] |

## Detailed Findings

### Finding F[N]-[seq]: [short title]

- **Requirement**: [spec requirement ID and description]
- **Spec reference**: [file:section:line or quote]
- **Verdict**: [PASS/WARN/FAIL/CRIT/INFO]
- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW/INFO]
- **Roadmap reference**: [task ID, section, line — or MISSING]
- **Gap description**: [What is missing or wrong — be specific]
- **Impact**: [What happens if this reaches implementation uncorrected]
- **Recommended correction**: [Specific, actionable fix for the roadmap]
- **Confidence**: [HIGH/MEDIUM/LOW with reasoning]

[Repeat for each finding that is not a clean PASS. Clean PASSes are documented in the Coverage Matrix only.]

## Discipline Summary

- **Total requirements**: [N]
- **Fully covered**: [N] ([%])
- **Partially covered**: [N] ([%])
- **Missing**: [N] ([%])
- **Contradicted**: [N] ([%])
- **Implicit only**: [N] ([%])
- **Top risk**: [The single most impactful gap in this discipline]
```

---

## 4. Cross-Cutting Concerns Validation (Sequential — After All Agents Complete)

After all parallel agents have written their reports, perform these additional checks that span discipline boundaries:

### 4.1 Integration Point Tracing

For every integration point identified in the Requirement Universe or the roadmap:
1. Identify the **producing discipline** (where the artifact is created)
2. Identify all **consuming disciplines** (where the artifact is used)
3. Verify that both producer and consumer tasks exist in the roadmap
4. Verify that the producer task is sequenced BEFORE the consumer task
5. Flag any integration point where the contract (interface, schema, protocol) differs between producer and consumer descriptions

### 4.2 Cross-Cutting Requirement Verification

For every requirement flagged as cross-cutting in the Discipline Map:
1. Verify it is fully covered by its primary discipline agent
2. Verify that secondary disciplines that touch it have consistent assumptions
3. Flag any contradictions between how different roadmap phases describe the same shared artifact

### 4.3 Completeness Boundary Check

1. Sum all requirements across all agent reports
2. Compare to the total Requirement Universe count
3. If they do not match: identify which requirements fell between discipline boundaries
4. Any requirement not covered by ANY agent is a CRITICAL gap

### 4.4 Sequencing Consistency

1. Build a dependency graph from all sequencing constraints in the spec
2. Map each constraint to roadmap phase/task ordering
3. Verify no constraint is violated
4. Pay special attention to: irreversible operations, gates that must precede code changes, tests that must precede releases

Write the cross-cutting report to `OUTPUT_DIR/cross-cutting-validation.md`.

---

## 5. Consolidation Phase (Sequential — After Cross-Cutting)

### 5.1 Collect All Agent Reports

Read every file in `OUTPUT_DIR/agent-D*.md` plus `OUTPUT_DIR/cross-cutting-validation.md`.

### 5.2 Compute Aggregate Metrics

| Metric | Formula |
|--------|---------|
| **Overall Coverage Score** | (Total PASS across all disciplines) / (Total requirements in Universe) * 100 |
| **Weighted Coverage Score** | Same but WARN counts as 0.5, IMPLICIT counts as 0.25 |
| **Gap Count by Severity** | Count of CRITICAL, HIGH, MEDIUM, LOW, INFO findings |
| **Discipline Health** | Per-discipline coverage percentage, sorted ascending (worst first) |
| **Cross-Cutting Health** | Number of integration point failures + boundary gaps |

### 5.3 GO / NO-GO Decision Matrix

| Condition | Decision |
|-----------|----------|
| 0 CRITICAL + 0 HIGH + Overall >= 95% | **GO** — roadmap is ready for tasklist generation |
| 0 CRITICAL + <=3 HIGH + Overall >= 90% | **CONDITIONAL GO** — roadmap needs targeted corrections before tasklist generation |
| Any CRITICAL findings | **NO-GO** — roadmap has contradictions that must be resolved |
| >3 HIGH findings | **NO-GO** — roadmap has significant coverage gaps |
| Overall < 85% | **NO-GO** — roadmap needs substantial revision |
| Any cross-cutting boundary gaps (requirements covered by zero agents) | **NO-GO** — discipline decomposition failed |

### 5.4 Write Consolidated Report

Write the final report to `OUTPUT_DIR/spec-roadmap-completeness.md`:

```markdown
# Spec-Roadmap Completeness Report

**Generated**: [timestamp]
**Roadmap**: [ROADMAP_PATH]
**Specs**: [SPEC_PATHS]
**Disciplines**: [count]
**Total Requirements**: [count]

## Executive Summary

**Overall Coverage**: [X]% ([weighted]% weighted)
**Decision**: [GO / CONDITIONAL GO / NO-GO]
**Reason**: [1-2 sentence justification]

## Severity Summary

| Severity | Count | Discipline(s) |
|----------|-------|----------------|
| CRITICAL | [N] | [D1, D5] |
| HIGH | [N] | [D2, D3, D6] |
| MEDIUM | [N] | [D1, D4] |
| LOW | [N] | [D2] |
| INFO | [N] | [D3, D6] |

## Discipline Coverage

| Discipline | Requirements | Covered | Partial | Missing | Contradicted | Score |
|-----------|-------------|---------|---------|---------|-------------|-------|
| D1: [name] | [N] | [N] | [N] | [N] | [N] | [%] |
| ... | | | | | | |
| **TOTAL** | [N] | [N] | [N] | [N] | [N] | [%] |

## All Findings (Sorted by Severity, then Discipline)

### CRITICAL Findings

[List each CRITICAL finding with full detail from agent reports]

### HIGH Findings

[List each HIGH finding with full detail]

### MEDIUM Findings

[List each MEDIUM finding with full detail]

### LOW Findings

[Summary table only — no full detail needed]

### INFO Observations

[Summary table only]

## Cross-Cutting Analysis

### Integration Point Failures
[List any failed integration point traces]

### Boundary Gaps
[List any requirements not covered by any agent — MUST be zero for GO]

### Sequencing Violations
[List any spec sequencing constraints violated by roadmap ordering]

## Remediation Roadmap

For each HIGH+ finding, provide:
1. **Finding ID**: [reference]
2. **Required action**: [specific roadmap edit — not vague guidance]
3. **Effort estimate**: [trivial / small / medium — roadmap edits, not code]
4. **Dependencies**: [other findings that must be fixed first, if any]

## Appendices

### A. Requirement Universe Summary
[Count by category — link to requirement-universe.md]

### B. Discipline Map Summary
[Link to discipline-map.md]

### C. Agent Reports Index
[Link to each agent-D*.md file]
```

---

## 6. Operational Rules

These rules govern the execution of this validation. They are non-negotiable.

### 6.1 Artifact-Based Workflow

ALL work products are written to files on disk. Never hold analysis in context memory alone. Every agent writes its own file. The consolidation phase reads files — it does not rely on memory of what agents found.

### 6.2 Incremental Writing

For any file that will exceed 50 lines: create the file with its header/frontmatter first, then append sections one at a time using Edit. Never accumulate a large file in memory and write it in one shot.

### 6.3 Evidence-Based Claims Only

Every finding must cite specific file paths, section headers, line numbers, task IDs, or direct quotes. No assumptions. No inferences presented as facts. If evidence is circumstantial, mark confidence as LOW and say why.

### 6.4 Adversarial Posture

- Assume the roadmap is incomplete until proven otherwise
- "Implicit" coverage is NOT the same as "covered" — it gets 0.25 weight, not 1.0
- A roadmap task that mentions a requirement by ID but provides no specificity about HOW it addresses the requirement is PARTIAL, not COVERED
- Matching requirement IDs is necessary but not sufficient — the SUBSTANCE must match
- If the roadmap uses a different numbering scheme than the spec, the absence of a mapping table is itself a LOW finding

### 6.5 No False Positives

Do not flag findings that are not real gaps:
- A roadmap adding EXTRA coverage beyond the spec is not a gap (it is an INFO observation)
- A roadmap using different words to describe the same requirement is not a gap if the meaning is equivalent
- A roadmap reorganizing phases differently from the spec is not a gap UNLESS it violates a sequencing constraint
- Formatting, style, or structural differences between spec and roadmap are not gaps

### 6.6 No False Negatives

Do not miss real gaps:
- Read the spec literally. If it says "Test 7 validates X" and the roadmap's Test 7 validates Y, that is a HIGH finding even if Y is also useful
- Check EVERY acceptance criterion individually — do not assume an FR is covered just because its header appears
- Check EVERY column of every data model — do not assume a table is covered just because the table name appears
- Check stop conditions on gates, not just pass conditions
- Check contingency plans on risks, not just mitigation strategies

### 6.7 Parallelism

- All discipline agents are independent and MUST be spawned in parallel
- The cross-cutting phase MUST wait for all agents to complete
- The consolidation phase MUST wait for the cross-cutting phase to complete
- Within an agent, work sequentially through requirements — do not skip around

### 6.8 Spec Hierarchy

When specs conflict with each other:
1. Release spec > tech spec > PRD > any other document
2. Later-dated spec > earlier-dated spec (check frontmatter dates)
3. Code-verified claims > unverified claims
4. If conflict cannot be resolved: flag it as a finding with severity MEDIUM and let humans decide

### 6.9 Domain Agnosticism

This prompt works for ANY domain:
- Backend, frontend, infrastructure, security, ML/AI, DevOps, mobile, embedded
- Any spec format: PRD, tech spec, release spec, RFC, ADR, design doc
- Any roadmap format: phased, kanban, milestone-based, sprint-based
- The discipline decomposition adapts to the content — it is not hardcoded

If the spec covers frontend components, the disciplines will include UI/UX, state management, etc. If it covers infrastructure, the disciplines will include networking, compute, storage, etc. The algorithm in Section 2.1 handles this automatically.

---

## 7. Quick Reference: Execution Flow

```
START
  |
  v
[1] Read all specs + roadmap + one-hop references
  |
  v
[2] Extract Requirement Universe → write to disk
  |
  v
[3] Extract Roadmap Structure → write to disk
  |
  v
[4] Auto-detect disciplines → write Discipline Map to disk
  |
  v
[5] PARALLEL: Spawn N agents (one per discipline, max 20)
  |     Each agent:
  |       - Reads its assigned requirements + full roadmap
  |       - Validates each requirement against roadmap
  |       - Writes agent report to disk
  |
  v  (barrier — wait for all agents)
  |
[6] Cross-cutting validation (integration points, boundaries, sequencing)
  |     → write cross-cutting report to disk
  |
  v
[7] Consolidation: collect all reports, compute metrics, render final report
  |     → write consolidated report to disk
  |
  v
[8] Return: summary + GO/NO-GO + link to consolidated report
  |
END
```

---

## 8. Example Invocation

To validate an OntRAG roadmap against its specs:

```
ROADMAP_PATH=".dev/releases/current/feature-Ont-RAG/r0-r1/roadmap.md"
SPEC_PATHS=[
  ".dev/releases/current/feature-Ont-RAG/r0-r1/release-spec-ontrag-r0-r1.md",
  ".dev/releases/current/feature-Ont-RAG/r0-r1/implementation-artifacts/tech-spec-ontrag-r0-r1-prerequisites-memory.md"
]
OUTPUT_DIR=".dev/releases/current/feature-Ont-RAG/r0-r1/validation/"
```

To validate a frontend wizard redesign:

```
ROADMAP_PATH="docs/releases/wizard-v2/roadmap.md"
SPEC_PATHS=["docs/releases/wizard-v2/prd-wizard-redesign.md"]
OUTPUT_DIR="docs/releases/wizard-v2/validation/"
```

To validate an infrastructure migration:

```
ROADMAP_PATH="infra/migrations/k8s-v2/roadmap.md"
SPEC_PATHS=[
  "infra/migrations/k8s-v2/rfc-k8s-migration.md",
  "infra/migrations/k8s-v2/adr-007-eks-to-gke.md"
]
OUTPUT_DIR="infra/migrations/k8s-v2/validation/"
```

The prompt handles all three identically — discipline detection adapts to the domain.

---

## 9. Failure Modes and Recovery

| Failure Mode | Detection | Recovery |
|-------------|-----------|----------|
| Spec is too vague to extract requirements | Requirement Universe has <10 items for a non-trivial feature | Report as META finding: "Spec lacks extractable requirements — validation cannot achieve HIGH confidence" |
| Roadmap references requirements by ID but spec has no IDs | Cannot trace coverage | Use description matching. Flag as LOW finding: "No requirement IDs in spec — traceability is manual" |
| Spec and roadmap use completely different terminology | Agent coverage scores are anomalously low | Before flagging MISSING, search roadmap for semantic equivalents. If found, verdict is COVERED with a LOW finding about terminology mismatch |
| More than 20 disciplines detected | Section 2.1 Step 5 cap exceeded | Force-merge smallest clusters. Note in discipline map which clusters were merged and what nuance may be lost |
| Agent finds zero gaps | Suspiciously clean | Re-read spec section with highest specificity (e.g., test plan, data model). If still zero gaps, report confidently — not every roadmap has gaps |
| Spec contains internal contradictions | Two requirements conflict | Flag as META finding with both references. Do not try to resolve — let humans decide which takes priority |
| Roadmap is significantly longer than spec | Roadmap adds substantial content beyond spec | This is normal for good roadmaps. Report extra coverage as INFO observations. Only flag if extras contradict spec |
| One spec file references another that is not in SPEC_PATHS | Missing context | Read the referenced file if accessible. If not accessible, note it as a META finding and reduce confidence for affected requirements |

---

## 10. Output Files Summary

At completion, the following files will exist in `OUTPUT_DIR`:

| File | Contents | Phase |
|------|----------|-------|
| `requirement-universe.md` | All extracted requirements from specs | Bootstrap |
| `roadmap-structure.md` | Extracted roadmap phases, tasks, gates | Bootstrap |
| `discipline-map.md` | Discipline assignments + cross-cutting concerns | Decomposition |
| `agent-D01-[slug].md` | Discipline 1 validation report | Parallel |
| `agent-D02-[slug].md` | Discipline 2 validation report | Parallel |
| ... (up to D20) | ... | Parallel |
| `cross-cutting-validation.md` | Integration points, boundaries, sequencing | Cross-cutting |
| `spec-roadmap-completeness.md` | **Final consolidated report with GO/NO-GO** | Consolidation |
