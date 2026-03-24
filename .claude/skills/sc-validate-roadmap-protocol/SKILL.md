---
name: sc-validate-roadmap-protocol
description: "Full behavioral protocol for sc:validate-roadmap — multi-agent roadmap-to-spec fidelity validation with adversarial review, coverage matrix, gap registry, and remediation planning. Use this skill whenever verifying roadmap completeness against specifications, auditing coverage before tasklist generation, or checking for requirement gaps between specs and roadmaps."
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__search_for_pattern, mcp__serena__activate_project
argument-hint: "<roadmap-path> --specs <spec1.md,...> [--output dir] [--depth quick|standard|deep] [--exclude domains] [--max-agents N]"
---

# /sc:validate-roadmap — Roadmap-to-Spec Fidelity Validator

<!-- Extended metadata (for documentation, not parsed):
category: analysis
complexity: advanced
mcp-servers: [sequential, auggie, serena]
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
| `--prior-taxonomy` | | No | - | Path to a prior `00-domain-taxonomy.md` to seed domain clustering for cross-run stability |

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
| Query codebase (semantic) | `mcp__auggie-mcp__codebase-retrieval` | Codebase-grounded enrichment (Steps 0.2b, 5.1b) — orchestrator only, fail-open |
| Read session memory | `mcp__serena__read_memory` | Load validation ledger, terminology, patterns (Pre-Phase 0) — fail-open |
| Write session memory | `mcp__serena__write_memory` | Persist ledger, terminology, patterns (Post-Phase 6) — fail-open |
| Activate project | `mcp__serena__activate_project` | Initialize Serena project context (Pre-Phase 0, Step 0.5) — fail-open |
| Find symbol | `mcp__serena__find_symbol` | Symbol lookup for context supplement (Step 0.5, deep only) — fail-open |
| Get symbols overview | `mcp__serena__get_symbols_overview` | File-level symbol map (Step 0.5, deep only) — fail-open |

**Rule**: All verbs in phase instructions MUST resolve to an entry in this glossary. MCP tools marked "fail-open" are optional — their unavailability never blocks validation.

## 5. Phase Architecture

### Pre-Phase 0: Session Context Loading (Optional, Fail-Open)

**Requires**: `mcp__serena__read_memory`, `mcp__serena__activate_project` (fail-open — skip all pre-phase hooks if Serena is unavailable).

Before document ingestion, load cross-session context from Serena memory. Each hook is independent — failure in one does not block others.

#### Hook 0a — Load Validation Ledger Baseline

Load the most recent validation ledger entry for this project to enable delta tracking in Phase 3.

1. Call `mcp__serena__activate_project` for the current repository.
2. Call `mcp__serena__read_memory` with key `validation-ledger-{project-slug}`.
3. If found: parse the ledger JSON and store in orchestrator context as `ledger_baseline`. Extract the most recent entry's gap IDs and severities for delta comparison in Step 3.10.
4. If not found or error: set `ledger_baseline = null`. Continue without delta tracking.

#### Hook 0b — Load Terminology Map

Load the project's accumulated terminology map as advisory context for requirement extraction.

1. Call `mcp__serena__read_memory` with key `terminology-map-{project-slug}`.
2. If found: parse terminology entries (max **200 entries**). Terms older than **90 days** are marked `low_confidence: true`. Store as `prior_terminology` in orchestrator context.
3. If not found or error: set `prior_terminology = null`. Extraction uses cold-start terminology only.

**Constraint**: Prior terminology is **advisory** — the current spec text always wins (R4 compliance). Prior terms serve as hints for extraction, not authoritative definitions.

#### Hook 0c — Load Adversarial Pattern History

Load historical adversarial pattern effectiveness data for Phase 4 pattern ordering.

1. Call `mcp__serena__read_memory` with key `adversarial-patterns-{project-slug}`.
2. If found: parse pattern entries. Filter to patterns with ≥3 historical hits and false-positive rate <40%. Rank by `(hit_count * (1 - fp_rate))`. Store top 20 as `historical_patterns`.
3. If not found or error: set `historical_patterns = null`. Phase 4 uses default patterns only.

---

### Phase 0: Document Ingestion & Requirement Extraction

**Executor**: Orchestrator (you). No agents spawned.

#### Step 0.1 — Read All Documents

Read every file in `--specs` and the roadmap at `<roadmap-path>` in their entirety using `Read`. If any spec references other documents (tech specs, investigation artifacts, ADRs), follow ONE hop — read the referenced file. Do not recursively spider.

#### Step 0.1.5 — Spec File Reference Verification

After reading all documents, verify that file paths referenced in specs actually exist in the project. This catches stale references (renamed/deleted files) before they corrupt requirement extraction.

1. Scan spec text for file path patterns in backtick or inline-code context: anything matching `.py`, `.ts`, `.md`, `.yaml`, `.json`, `.toml`, or paths containing `src/`, `tests/`, `config/`.
2. For each unique path found, check existence:
   - Use `Glob` with the exact path first.
   - If not found, use `Glob` with `**/{basename}` to search for relocated files.
3. Write a "File Reference Status" section at the top of `{OUTPUT_DIR}/00-requirement-universe.md` (created in Step 0.2):

```markdown
## Spec File Reference Status (Step 0.1.5)

| Referenced Path | Source | Status | Notes |
|----------------|--------|--------|-------|
| `src/auth/token_manager.py` | spec.md:L42 | FOUND | — |
| `src/pipeline/hooks.py` | spec.md:L88 | NOT FOUND | Basename match: `src/superclaude/cli/pipeline/trailing_gate.py` |

**Note**: NOT FOUND paths may reference files to be created. This table is informational — it does not change coverage scoring.
```

4. Annotate requirements whose source sections contain NOT FOUND references with `file_ref_stale: true` (informational only — no scoring changes, no adjudication rule modifications).

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

#### Step 0.2b — Codebase-Grounded Requirement Enrichment (Optional)

**Requires**: `mcp__auggie-mcp__codebase-retrieval` (fail-open — skip entirely if Auggie is unavailable).

After building the requirement universe, scan it for code references that would benefit from codebase context. This step enriches requirements with advisory structural information — it never creates new requirements or changes coverage calculations.

**Procedure**:

1. **Identify code-referencing requirements**: Scan requirement text for backtick-wrapped identifiers (class names, function names, file paths), import paths, API endpoint paths, and technology-specific keywords (e.g., database table names, config keys).
2. **Triage references by resolution method**:
   - **Simple references** (file paths, exact symbol names): Resolve with `Grep`/`Glob` first. Do NOT use Auggie for lookups that a pattern search can answer.
   - **Semantic references** (architectural concepts, integration patterns, "the auth subsystem"): Query Auggie's `codebase-retrieval` with a focused natural-language query.
3. **Query Auggie** for each semantic reference (hard cap: **15 queries maximum**):
   - Query format: `"What code implements {concept}? Include callers, related tests, and file paths."`
   - For each response, extract: relevant file paths, function/class names, test file references.
4. **Annotate requirements** with an advisory `codebase_context` field:

```yaml
- id: "REQ-042"
  text: "JWT token rotation must occur every 24 hours"
  codebase_context:  # ADVISORY — does not affect coverage scoring
    files: ["src/auth/token_manager.py", "tests/test_token_rotation.py"]
    symbols: ["TokenManager.rotate()", "test_rotation_interval"]
    source: "auggie"  # or "grep" for pattern-resolved refs
```

5. **Bail-out rule**: If 5 consecutive Auggie queries return no relevant file paths, stop querying and proceed. Remaining requirements get no `codebase_context` annotation.

**Constraints**:
- `codebase_context` is **advisory only** — no new requirements generated, no changes to requirement universe count, no changes to coverage calculations.
- Token cost acknowledgment: ~200-500 tokens per annotated requirement.
- Orchestrator-only: agents spawned in Phase 2 do NOT call Auggie.

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

**Taxonomy seeding** (when `--prior-taxonomy` is provided): Read the prior taxonomy file and extract domain names and boundary descriptions. Use these as initial cluster centers — new requirements are assigned to existing domains by affinity. Genuinely new domains are created. Dead domains (zero requirements) are pruned. Append a delta section to the new taxonomy artifact showing what changed vs. the prior taxonomy.

**Cold-start algorithm** (when `--prior-taxonomy` is absent or first run):

1. **Cluster by domain signal**: File paths, technology references, requirement type, section headers, system boundaries.
2. **Merge small clusters**: If a domain has fewer than 3 requirements, merge into nearest related domain.
3. **Split oversized clusters**: If a domain has more than 20 requirements, split along natural sub-boundaries.
4. **Ensure non-overlapping coverage**: Every requirement belongs to exactly one primary domain. Cross-cutting requirements are assigned to primary domain but flagged for secondary review.
5. **Cap at `max-agents - 4`**: Reserve 4 slots for mandatory cross-cutting agents.

Regardless of seeding mode, evidence-based requirement assignment is required (R3 compliance) — seeded domain names are suggestions, not mandates.

Write artifact: `{OUTPUT_DIR}/00-domain-taxonomy.md`

#### Step 0.5 — Symbol Context Supplement (`--depth deep` only)

**Requires**: `mcp__serena__find_symbol`, `mcp__serena__get_symbols_overview` (fail-open — skip entirely if Serena is unavailable or depth is not `deep`).

**Gate**: Skip this step unless `--depth deep` is set.

At deep depth, produce a supplemental artifact documenting the structural context of code-referenced requirements. This provides human reviewers and the Phase 4 adversarial reviewer with codebase architecture context.

**Procedure**:

1. **Identify code-referenced requirements**: From the requirement universe, collect requirements whose text contains backtick-wrapped identifiers (class names, function names, module paths).
2. **Activate Serena project**: Call `mcp__serena__activate_project` (if not already activated in Pre-Phase 0).
3. **Look up symbols** (hard cap: **30 symbol lookups**):
   - For each code identifier, call `mcp__serena__find_symbol` with `include_body=False` to locate the symbol's file, type (class/function/method), and parent hierarchy.
   - For files with multiple related symbols, call `mcp__serena__get_symbols_overview` once per file to capture the structural context.
4. **Write supplemental artifact**: `{OUTPUT_DIR}/00-symbol-context-supplement.md`

```markdown
# Symbol Context Supplement (Step 0.5, deep only)

**INFORMATIONAL ONLY** — this artifact does not modify requirement records, generate derived sub-requirements, or affect coverage scoring. It is referenced as background reading by the Phase 4 adversarial reviewer.

| Requirement | Symbol | File | Type | Parent | Notes |
|-------------|--------|------|------|--------|-------|
| REQ-012 | `TokenManager` | src/auth/token_manager.py | class | — | 8 methods |
| REQ-012 | `rotate()` | src/auth/token_manager.py | method | TokenManager | — |
| REQ-045 | `PipelineExecutor` | src/cli/pipeline.py | class | — | NOT_FOUND |

Symbols found: {N} / {N} attempted
```

5. **Failure handling**: If Serena is unavailable or no symbols are found, skip entirely — write no artifact. This is non-blocking.

**Constraints**:
- Does NOT modify requirement records or generate derived sub-requirements.
- Does NOT affect coverage scoring or agent assignments.
- Referenced as **background reading** in Phase 4 adversarial review only.

---

### Phase 1: Agent Decomposition

**Executor**: Orchestrator. No agents spawned yet.

#### Step 1.1 — Create Domain Agent Assignments

For each domain from Step 0.4, create one agent spec. **All agents use the `haiku` model** (see Spawn Protocol).

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

1. Dispatch ALL agents in a single message using parallel `Task` calls. **All agents MUST use the `haiku` model** — set `model: "haiku"` on every `Task` invocation (domain agents and cross-cutting agents alike). The orchestrator remains on the parent model; only spawned agents use haiku.
2. Each agent prompt includes the FULL text of its assigned requirements — paste the content, do not reference a file path.
3. If an agent fails, retry ONCE. If retry fails, log failure — CC4 and the adversarial pass will catch gaps.
4. Wait for ALL agents to complete before proceeding to Phase 3.

---

### Phase 3: Consolidation

**Executor**: Orchestrator. No new agents spawned.

#### Step 3.1 — Collect Agent Reports

Read every file matching `{OUTPUT_DIR}/01-agent-*.md`. Verify each agent completed (check for summary statistics). Note any failed agents and list unvalidated requirements.

#### Step 3.1b — File Path Verification Pass

Extract all file path references from agent reports and `00-requirement-universe.md`. Verify existence against the project filesystem. Write an informational annotation block at the top of the coverage matrix (Step 3.2 output).

**Depth gating**:
- `quick`: Skip file path verification entirely.
- `standard`: Verify file paths (exact match only via `Bash` `test -f`).
- `deep`: Verify file paths with relocation search via `Glob` `**/{basename}`.

**Procedure**:

1. Scan all agent reports and the requirement universe for file path references: anything matching `src/`, `tests/`, or common extensions (`.py`, `.ts`, `.md`, `.yaml`, `.json`, `.toml`).
2. Deduplicate across agents (same path referenced by multiple agents needs one check).
3. For each unique path, check existence:
   - **EXISTS**: File found at the referenced path.
   - **NOT_FOUND**: No file at the referenced path. At `deep` depth, use `Glob` with `**/{filename}` to search for relocated files.
   - **POSSIBLY_MOVED**: File not found at referenced path, but a file with the same basename exists elsewhere.
4. Write a **File Path Verification Table** as an annotation block at the top of `02-unified-coverage-matrix.md`:

```markdown
## File Path Verification (Step 3.1b)

| Referenced Path | Source | Status | Notes |
|----------------|--------|--------|-------|
| `src/superclaude/cli/sprint/executor.py` | REQ-042, Agent D3 | EXISTS | — |
| `src/pipeline/hooks.py` | REQ-061 | POSSIBLY_MOVED | Candidate: `src/superclaude/cli/pipeline/trailing_gate.py` |
| `src/gates/runner.py` | Roadmap Phase 3 | NOT_FOUND | No match in codebase |

**INFORMATIONAL ONLY** — this table does not change any coverage statuses. Agents' assessments stand as-is. The adversarial reviewer (Phase 4) may use this table as evidence when challenging coverage claims.
```

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

**Symbol Spot-Check** (`--depth deep` only): For each integration point where the spec text contains backtick-wrapped identifiers (PascalCase, snake_case, or dotted paths longer than 6 characters), use `Grep` to search the codebase for the symbol:

- If a symbol appears in zero files: flag as `symbol_not_found: true` on the integration entry. Downgrade FULLY_WIRED to PARTIALLY_WIRED with a LOW finding: "Spec references symbol `{X}` which was not found in the codebase — verify it exists or has not been renamed."
- If a symbol appears in files: note `symbol_found: true` with file paths. No further analysis.

This is a spot-check using `Grep` (already an allowed tool), not a full symbol graph analysis. It adds one `Grep` call per backtick-wrapped symbol, bounded by the number of integration points.

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

## Validation Ledger Delta (when baseline available)
{from ledger delta computation — see below}
```

**Validation Ledger Delta** (when `ledger_baseline` is not null): After writing the main report sections, compute a delta between the current findings and the most recent ledger entry:

1. Compare current gap IDs/descriptions against baseline gap IDs/descriptions using semantic matching (same requirement + same gap type = same gap).
2. Classify each gap:
   - **PERSISTENT**: Gap existed in baseline and still exists (same severity or worse).
   - **RESOLVED**: Gap existed in baseline but is no longer present.
   - **NEW**: Gap not present in baseline.
   - **REGRESSION**: Gap was RESOLVED in a prior run but has reappeared.
3. **REGRESSION** findings are auto-escalated by one severity level for **display purposes only** (e.g., MEDIUM → displayed as HIGH). This does NOT change the adjudicated severity or affect the GO/NO_GO verdict calculation.
4. Append the delta table to the consolidated report:

```markdown
## Validation Ledger Delta

Compared against baseline from: {baseline_timestamp}

| Gap ID | Status | Current Severity | Baseline Severity | Notes |
|--------|--------|-----------------|-------------------|-------|
| GAP-C001 | PERSISTENT | CRITICAL | CRITICAL | Unchanged |
| GAP-H003 | RESOLVED | — | HIGH | Fixed in roadmap v2 |
| GAP-M007 | NEW | MEDIUM | — | First detected |
| GAP-H002 | REGRESSION | HIGH (display: CRITICAL) | HIGH | Was resolved, now back |

Summary: {N} persistent, {N} resolved, {N} new, {N} regressions
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

**Enhancement 4.3a — Systematic Pattern Scan**: Before the free-form orphan search, run `Grep` against each spec file with patterns to find requirement-like statements not captured in the requirement universe.

**Pattern ordering**: If `historical_patterns` is loaded (from Pre-Phase 0, Hook 0c), insert the top-ranked historical patterns **before** the default patterns below. Historical patterns are project-specific patterns that proved effective in prior runs. Default patterns always run regardless.

Default patterns:

```
1. Modal requirements:     (shall|must|required to|needs to) [^.]{10,80}
2. Negation requirements:  (must not|shall not|never|prohibited|forbidden) [^.]{10,80}
3. Quantitative NFRs:      (at least|at most|within|maximum|minimum) \d+
4. Conditional:            (if|when|unless) .{5,40} (must|shall|should)
```

For each match: check against the requirement universe. If not already captured, create an ADV finding of type ORPHAN_REQUIREMENT.

**Filtering rules**: Skip matches in the first 20 lines of each file (preamble/overview). Skip matches that are pure narrative with no concrete noun or measurable target. Negation requirements (pattern 2) are the highest-miss category — prioritize these.

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

**Enhancement 4.6a — Systematic Assumption Detection**: Run `Grep` against the roadmap with these patterns:

```
1. Explicit assumptions:  (assumes|assuming|given that|prerequisite|depends on)
2. Implicit state refs:   (existing|current|already|previously) .{5,40} (service|system|API|database|table|endpoint)
```

For each match: verify the assumed capability appears in the spec. If not specified in spec, create an ADV finding of type SILENT_ASSUMPTION.

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

#### Step 5.1b — Codebase-Grounded Remediation Enrichment (Optional)

**Requires**: `mcp__auggie-mcp__codebase-retrieval` (fail-open — skip entirely if Auggie is unavailable).

Before generating the patch checklist, enrich CRITICAL and HIGH remediation entries with codebase context so that implementers know which files and packages are affected.

**Procedure**:

1. **Filter eligible gaps**: Only process gaps with verdict VALID-CRITICAL or VALID-HIGH that contain concrete code keywords (file paths, class names, function names, API endpoints, config keys). **Hard skip**: NFR/CONSTRAINT-type gaps without file-level specificity are excluded.
2. **Triage by resolution method** (same as Step 0.2b):
   - **Concrete keywords** (file paths, symbol names): Resolve with `Grep`/`Glob` first.
   - **Semantic queries** (architectural concepts, integration patterns): Query Auggie.
3. **Query Auggie** (hard cap: **10 queries maximum**):
   - Query format: `"What files and packages are affected by {gap description}? Include test files."`
   - **Bail-out**: After **3 consecutive** queries returning no relevant results, abandon enrichment for remaining gaps.
4. **Attach advisory context** to each enriched remediation entry:

```markdown
- [ ] **GAP-C001** (CRITICAL, MEDIUM): Missing JWT rotation implementation
  - File: roadmap.md:L142-155
  - Action: ADD
  - **Codebase context** (advisory):
    - Affected files: `src/auth/token_manager.py`, `src/auth/middleware.py`
    - Related tests: `tests/test_token_rotation.py`
    - Package: `superclaude.auth`
    - Source: auggie | grep
```

**Constraints**:
- Codebase context is **advisory** — existing heuristic effort levels (TRIVIAL/SMALL/MEDIUM/LARGE) remain unchanged.
- No backward flow into Phase 3 metrics (R11 compliance).
- Orchestrator-only: no agent-level Auggie access.

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
| 00-symbol-context-supplement.md | 0 | Symbol structural context (deep only) |
| 05-validation-summary.md | 6 | This file |

## Next Steps
- **GO**: Roadmap validated. Proceed to tasklist generation with `/sc:tasklist`.
- **CONDITIONAL_GO**: Apply targeted corrections from remediation plan, then proceed.
- **NO_GO**: Execute remediation phases R1-R8, then rerun `/sc:validate-roadmap`.
```

If `--report` flag is set, also write summary to the specified path.

---

### Post-Phase 6: Session Context Persistence (Optional, Fail-Open)

**Requires**: `mcp__serena__write_memory` (fail-open — skip all post-phase hooks if Serena is unavailable).

After the final summary is written, persist cross-session context to Serena memory. Each hook is independent — failure in one does not block others or the return contract.

#### Hook 6a — Write Validation Ledger Entry

Persist the current validation results for future delta tracking.

1. Build a ledger entry:

```json
{
  "timestamp": "{ISO-8601}",
  "roadmap_path": "{ROADMAP_PATH}",
  "spec_paths": ["{SPEC_PATHS}"],
  "verdict": "{GO|CONDITIONAL_GO|NO_GO}",
  "weighted_coverage": "{%}",
  "total_requirements": N,
  "gaps": [
    {"id": "GAP-C001", "severity": "CRITICAL", "description": "..."},
    ...
  ]
}
```

2. Call `mcp__serena__read_memory` with key `validation-ledger-{project-slug}` to load existing ledger.
3. Append new entry. **Pruning**: keep only the last **10 entries** or entries from the last **30 days**, whichever is fewer.
4. Call `mcp__serena__write_memory` with the updated ledger.
5. On error: log warning and continue. Ledger loss is acceptable.

#### Hook 6b — Write Terminology Map

Persist the updated terminology map for future extraction hints.

1. Merge the current run's glossary terms (from Phase 0 extraction) with `prior_terminology` (if loaded).
   - New terms are added with `first_seen: {today}`.
   - Existing terms have `last_seen` updated to today.
   - Terms not seen in the current run retain their prior dates.
2. Call `mcp__serena__write_memory` with key `terminology-map-{project-slug}`.
3. **Cross-project contamination prevention**: The project slug is part of the key — terms from project A are never loaded for project B.

#### Hook 6c — Append Pattern Log Entry

Write an append-only pattern log for trend tracking (human review only).

1. Build a log entry summarizing this run:

```json
{
  "timestamp": "{ISO-8601}",
  "verdict": "{verdict}",
  "coverage": "{%}",
  "total_gaps": N,
  "gap_severity_distribution": {"CRITICAL": N, "HIGH": N, "MEDIUM": N, "LOW": N},
  "domains_validated": N,
  "depth": "{depth}"
}
```

2. Call `mcp__serena__read_memory` with key `pattern-log-{project-slug}`. Append entry. Keep last **20 entries**.
3. Call `mcp__serena__write_memory` with the updated log.
4. **Constraint**: The pattern log is **write-only** — the validator never reads it during execution. It exists for human trend review only.

#### Hook 6d — Write Adversarial Pattern Effectiveness Stats

After Phase 4, compute and persist pattern effectiveness data for future pattern ordering.

1. For each pattern used in Step 4.3a (both default and historical):
   - Count hits (matches that became ADV findings).
   - Count false positives (matches that were filtered as non-requirement prose).
   - Record severity distribution of resulting findings.
2. Build stats:

```json
{
  "timestamp": "{ISO-8601}",
  "project_type": "{detected or 'generic'}",
  "patterns": [
    {
      "regex": "(shall|must|required to) ...",
      "hits": N,
      "false_positives": N,
      "fp_rate": 0.XX,
      "severity_distribution": {"CRITICAL": N, "HIGH": N, ...}
    },
    ...
  ]
}
```

3. Call `mcp__serena__read_memory` with key `adversarial-patterns-{project-slug}`. Merge stats (cumulative hit/FP counts). Retain **top 20 patterns** by effectiveness score. Expire entries older than **90 days**.
4. Call `mcp__serena__write_memory` with updated stats.
5. **Project-type segmentation**: If the project type changes between runs, historical patterns from the prior type are retained but ranked lower (0.5x weight multiplier).

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
