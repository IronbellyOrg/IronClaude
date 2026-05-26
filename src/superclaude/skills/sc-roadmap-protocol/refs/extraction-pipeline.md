# Extraction Pipeline Reference

Reference document for Wave 1B (Detection & Analysis). Documents the canonical CLI **single-pass extraction step** built by `build_extract_prompt` / `build_extract_prompt_tdd`, the eight aspects the single prompt instructs the LLM to cover, the additional TDD aspects emitted by the TDD-specific builder, the PRD/TDD supplementary context blocks, the LLM-advisory domain keyword dictionaries, and the inference-only chunked-extraction algorithm and 4-pass completeness verification.

---

## Single-Pass Extraction (CLI Canonical Behavior)

> **CLI parity (B-7, VERIFIED).** The roadmap CLI executes extraction as a **single `Step(id="extract", ...)`** built by one of two prompt-builder functions. There is **no** sequential 8-step pipeline in the CLI today, no per-aspect retry, no chained intermediate outputs between aspects, and no inter-aspect ordering gate. The eight subsections below capture the **aspects the single prompt instructs the LLM to cover**, not chained phases.

### CLI prompt builders

| Builder | Source | When used |
|---|---|---|
| `build_extract_prompt` | `src/superclaude/cli/roadmap/prompts.py:180` | Default extraction path (`config.input_type` is `spec`, or omitted). Produces the 8 standard body sections described below. |
| `build_extract_prompt_tdd` | `src/superclaude/cli/roadmap/prompts.py:328` | Selected when `--input-type tdd` is passed (the CLI uses an **explicit flag**, not the 4-signal inference heuristic in `scoring.md`). Produces the 8 standard body sections plus 6 TDD-specific aspects (see "TDD-Extended Aspects" below). |

Both functions return one prompt string. The executor wires it into a single step at `src/superclaude/cli/roadmap/executor.py:2001-2025`:

```python
Step(
    id="extract",
    prompt=(
        build_extract_prompt_tdd(...) if config.input_type == "tdd"
        else build_extract_prompt(...)
    ),
    output_file=extraction,
    gate=EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE,
    timeout_seconds=1800 if config.input_type == "tdd" else 300,
    inputs=...,
    retry_limit=1,
)
```

The LLM receives one prompt and writes one `extraction.md` file with YAML frontmatter plus eight standard body sections (fourteen in the TDD path). The only mechanical gate is `EXTRACT_GATE` (or `EXTRACT_TDD_GATE`) against the single emitted file; there is no per-aspect validation, no inter-aspect handoff, and the single step has `retry_limit=1` for transport-level retry only.

### Eight-aspect coverage inside the single prompt

The eight aspects below capture **what the single CLI prompt instructs the LLM to extract**. They are *coverage rationale*, not a required execution sequence — the LLM is free to address them in any order that produces the required body sections of `extraction.md`. ID assignment (Aspect 8) is a coordination concern that runs implicitly as the LLM emits each section. The CLI prompt instructs the LLM to **preserve spec/TDD requirement identifiers verbatim** (e.g., `FR-EVAL-001.1` stays `FR-EVAL-001.1`) rather than re-numbering as `FR-001, FR-002, ...`; the synthetic numbering described in Aspect 8 is the fallback path when the source document has no identifiers of its own (`prompts.py:219-227`, `:386-393`).

### Aspect 1: Title & Overview Extraction

Extract the project title, version, and high-level summary from the spec's opening sections (typically H1 heading, metadata block, and executive summary).

**Output**: `project_title`, `project_version`, `summary` (1-3 sentences)

### Aspect 2: Functional Requirements (FRs)

Scan the spec for functional requirements. Look for:

- Explicit requirement sections (headings containing "requirement", "feature", "capability")
- Behavioral statements ("shall", "must", "will", "should")
- User stories ("As a...", "I want...", "So that...")
- Acceptance criteria blocks

For each FR, extract:
| Field | Description |
|-------|-------------|
| `id` | Source-document ID verbatim; falls back to `FR-NNN` per Aspect 8 |
| `description` | Clear statement of the requirement |
| `domain` | Classified per Aspect 4 |
| `priority` | P0 (must-have), P1 (should-have), P2 (nice-to-have), P3 (future) |
| `source_lines` | Line range in original spec (e.g., L12-L18) |

**Priority assignment heuristic**:

- "must", "required", "critical", "blocking" → P0
- "should", "important", "expected" → P1
- "nice to have", "optional", "could" → P2
- "future", "planned", "roadmap", "v2", "later" → P3
- No explicit signal → P1 (default)

### Aspect 3: Non-Functional Requirements (NFRs)

Scan for non-functional requirements:

- Performance constraints (latency, throughput, load)
- Security requirements (auth, encryption, compliance)
- Scalability targets (user count, data volume)
- Reliability (uptime, recovery time)
- Maintainability (code coverage, documentation)

For each NFR, extract:
| Field | Description |
|-------|-------------|
| `id` | Source-document ID verbatim; falls back to `NFR-NNN` per Aspect 8 |
| `description` | Clear statement |
| `category` | performance, security, scalability, reliability, maintainability |
| `constraint` | Measurable threshold (e.g., "<200ms response time") |
| `source_lines` | Line range in original spec |

### Aspect 4: Scope & Domain Classification

Classify every extracted requirement into one or more domains using the domain keyword dictionaries (see below). Compute domain distribution as percentages.

**Classification algorithm**:

1. For each requirement, tokenize the description into words
2. Match tokens against each domain's keyword dictionary
3. Apply keyword weights (primary keywords weight 2.0, secondary keywords weight 1.0)
4. Assign requirement to the domain with highest weighted score
5. If multiple domains score within 15% of each other, assign to all qualifying domains (split attribution)
6. Compute domain distribution: `domain_percentage = (weighted_requirements_in_domain / total_weighted_requirements) * 100`

### Aspect 5: Dependency Extraction

Identify dependencies between requirements and external dependencies:

- Inter-requirement dependencies ("requires", "depends on", "after", "before", "blocks")
- External dependencies (third-party services, libraries, infrastructure)
- Implicit ordering (sequential spec sections often imply order)

For each dependency:
| Field | Description |
|-------|-------------|
| `id` | `DEP-NNN` synthetic; see Aspect 8 |
| `description` | What depends on what |
| `type` | `internal` (between requirements) or `external` (third-party) |
| `affected_requirements` | List of requirement IDs affected |
| `source_lines` | Line range in original spec |

### Aspect 6: Success Criteria Extraction

Extract measurable success criteria from the spec:

- Explicit success criteria sections
- Acceptance criteria attached to requirements
- KPIs, metrics, and targets mentioned anywhere in the spec

For each criterion:
| Field | Description |
|-------|-------------|
| `id` | `SC-NNN` synthetic; see Aspect 8 |
| `description` | Measurable criterion |
| `derived_from` | Requirement IDs this criterion validates |
| `measurable` | Yes/No — is it objectively testable? |
| `source_lines` | Line range in original spec |

### Aspect 7: Risk Identification

Extract risks mentioned in the spec and infer risks from requirement complexity:

**Explicit risks**: Sections mentioning "risk", "concern", "challenge", "constraint", "limitation"

**Inferred risks** (generate if not explicit):

- High-complexity requirements (many dependencies) → integration risk
- External dependencies → availability risk
- Security requirements → compliance risk
- Performance constraints → scalability risk

For each risk:
| Field | Description |
|-------|-------------|
| `id` | `RISK-NNN` synthetic; see Aspect 8 |
| `description` | Risk statement |
| `probability` | Low, Medium, High |
| `impact` | Low, Medium, High |
| `affected_requirements` | List of requirement IDs |
| `source_lines` | Line range (or "inferred" if generated) |

### Aspect 8: ID Assignment

> **CLI parity note.** The CLI prompt instructs the LLM to **preserve source-document identifiers verbatim** (`prompts.py:219-227`, `:386-393`). The synthetic `FR-NNN` / `NFR-NNN` numbering below is the **fallback** path when the source document has no identifiers; do not renumber existing IDs.

Assign deterministic IDs to extracted items that lack source-document identifiers:

| Entity | Format | Sequence |
|--------|--------|----------|
| Functional Requirements | `FR-{3digits}` | FR-001, FR-002, ... ordered by `source_lines` |
| Non-Functional Requirements | `NFR-{3digits}` | NFR-001, NFR-002, ... ordered by `source_lines` |
| Dependencies | `DEP-{3digits}` | DEP-001, DEP-002, ... ordered by `source_lines` |
| Success Criteria | `SC-{3digits}` | SC-001, SC-002, ... ordered by `source_lines` |
| Risks | `RISK-{3digits}` | RISK-001, RISK-002, ... (explicit first, then inferred) |

**Ordering rule**: Items are assigned IDs in order of their `source_lines` position in the original spec. This ensures deterministic ID assignment across runs. Inferred items (no source line) are appended after explicit items.

**Cross-reference resolution**: After ID assignment, update all `affected_requirements`, `derived_from`, and `affected_requirements` fields with the assigned IDs.

---

## TDD-Extended Aspects (covered by `build_extract_prompt_tdd`)

When `--input-type tdd` is passed, the executor swaps `build_extract_prompt` for `build_extract_prompt_tdd` (`prompts.py:328`). The TDD-specific prompt still produces one `extraction.md` file in one step, but instructs the LLM to cover six additional aspects on top of the eight standard ones, for **fourteen body sections total** (`prompts.py:383-466`). The CLI's `--input-type` flag is an **explicit operator choice**; the 4-signal inference scoring described in `scoring.md` is an inference-only heuristic and is **not** what the CLI dispatches on.

**CLI canonical TDD body sections** (`prompts.py:411-465`):

| CLI section | Source line | Frontmatter counter |
|---|---|---|
| Data Models and Interfaces | `prompts.py:411` | `data_models_identified` |
| API Specifications | `prompts.py:420` | `api_surfaces_identified` |
| Component Inventory | `prompts.py:429` | `components_identified` |
| Testing Strategy | `prompts.py:437` | `test_artifacts_identified` |
| Migration and Rollout Plan | `prompts.py:445` | `migration_items_identified` |
| Operational Readiness | `prompts.py:454` | `operational_items_identified` |

> **CLI parity (B-7, partial).** The seven sub-aspects below (originally labelled Steps 9-15) describe an **inference-only TDD aspect taxonomy** that is finer-grained than the six CLI body sections above. Aspects 11 (Release Criteria) and 12 (Observability) split out into the CLI's "Operational Readiness" and may overlap with "Success Criteria" / "Open Questions" in the standard 8. Use the table above for **what the CLI prompt actually instructs**; treat the sub-aspects below as advisory coverage notes that the LLM may consult while filling those six CLI sections.

Each aspect stores `null` for its storage key if the corresponding TDD section is absent or empty.

### Aspect 9: Component Inventory Extraction

Extract new/modified/deleted component tables from `## 10. Component Inventory`.

| Storage Key | Structure |
|-------------|-----------|
| `component_inventory` | `{ new: [{name, purpose}], modified: [{name, change}], deleted: [{name, migration_target}] }` |

### Aspect 10: Migration Phase Extraction

Extract rollout stage table from §19.3 and rollback steps from §19.4.

| Storage Key | Structure |
|-------------|-----------|
| `migration_phases` | `{ stages: [{stage, environment, criteria, rollback_trigger}], rollback_steps: [string] }` |

### Aspect 11: Release Criteria Extraction

Extract Definition of Done checklist from §24.1 and release checklist from §24.2. Independent of Aspect 6 (Success Criteria) — Aspect 6 captures behavioral success criteria from spec language; Aspect 11 captures structured checklists from TDD sections.

| Storage Key | Structure |
|-------------|-----------|
| `release_criteria` | `{ definition_of_done: [string], release_checklist: [string] }` |

### Aspect 12: Observability Extraction

Extract metrics table from §14.2, alerts table from §14.4, and dashboard names/links from §14.5.

| Storage Key | Structure |
|-------------|-----------|
| `observability` | `{ metrics: [{name, description, type, target}], alerts: [{name, condition, severity}], dashboards: [{name, link}] }` |

### Aspect 13: Testing Strategy Extraction

Extract test pyramid from §15.1, unit/integration/E2E test case tables from §15.2, and environments from §15.3.

| Storage Key | Structure |
|-------------|-----------|
| `testing_strategy` | `{ test_pyramid: [{level, coverage_target, tools}], unit_tests: [...], integration_tests: [...], e2e_tests: [...], environments: [...] }` |

### Aspect 14: API Surface Extraction

Extract endpoint count from the endpoint summary table in `## 8. API Specifications` §8.1 (API Overview).

| Storage Key | Structure |
|-------------|-----------|
| `api_surface` | `{ endpoint_count: N }` |

### Aspect 15: Data Model Complexity Extraction

Extract entity count and relationship count from `## 7. Data Models` §7.1 Data Entities.

| Storage Key | Structure |
|-------------|-----------|
| `data_model_complexity` | `{ entity_count: N, relationship_count: N }` |

Entity count = number of distinct entity/interface definitions in §7.1. Relationship count = number of foreign key, reference, or association declarations across all entities.

---

## PRD-Supplementary Extraction Context

When `--prd-file` is provided alongside the primary input (spec or TDD), the extraction step receives supplementary business context from the PRD. This is NOT a new input mode -- PRD content is injected as conditional prompt enrichment blocks that activate only when the PRD file is present. The primary extraction mode (`spec` or `tdd`) is unchanged.

The following storage keys enrich the extraction output when PRD context is available:

| Storage Key | Source PRD Section | Structure |
|-------------|-------------------|-----------|
| `user_personas` | S7 User Personas | `[{ name: str, needs: str, primary_workflow: str }]` |
| `user_stories` | S6 JTBD / S7 Personas | `[{ actor: str, goal: str, acceptance_criteria: str }]` |
| `success_metrics` | S19 Success Metrics | `[{ metric: str, target: str, measurement: str }]` |
| `market_constraints` | S17 Legal/Compliance | `[{ constraint: str, regulatory_body: str, compliance_deadline: str }]` |
| `release_strategy` | S12 Scope Definition | `{ in_scope: [str], out_of_scope: [str], deferred: [str] }` |
| `stakeholder_priorities` | S5 Business Context | `[{ stakeholder: str, priority: str, success_criterion: str }]` |
| `acceptance_scenarios` | S22 Customer Journey Map | `[{ journey: str, critical_path: str, validation_approach: str }]` |

These keys are advisory -- they inform prioritization, scope validation, and test strategy without overriding technical extraction from the primary document. Downstream consumers (generate, score, spec-fidelity, test-strategy) use them to produce roadmaps with product-level grounding alongside engineering structure.

**State file persistence:** `.roadmap-state.json` now stores supplementary file paths (`tdd_file`, `prd_file`, `input_type`) alongside the existing `spec_file` and `spec_hash` fields. This enables downstream pipeline consumers (e.g., `superclaude tasklist validate`) to auto-wire supplementary files without requiring the user to re-pass `--tdd-file` and `--prd-file` flags. Explicit CLI flags always override auto-wired values from state.

---

## Domain Keyword Dictionaries (LLM-advisory)

> **Scope.** These dictionaries are **advisory inputs for the LLM** classifying requirements into the `domains_detected` frontmatter list (`prompts.py:213`, `:362`). The CLI does not tokenise the spec, does not apply the weights, and does not enforce the classification algorithm — the LLM does whatever its prompt asks. Reframed under B-7: dictionaries below remain useful as a vocabulary cheat-sheet for the LLM but are not canonical CLI behaviour.

Seven domain dictionaries for requirement classification. Each keyword has a weight: **primary** (2.0) keywords are strong domain indicators, **secondary** (1.0) keywords are weaker signals.

### Frontend Domain

**Primary** (weight 2.0): component, UI, UX, responsive, accessibility, WCAG, layout, CSS, styling, viewport, animation, render, DOM, browser, SPA, SSR, hydration

**Secondary** (weight 1.0): button, form, input, modal, dropdown, navigation, menu, page, screen, view, display, theme, dark mode, mobile, tablet, desktop, interaction, click, hover, scroll, toast, notification, badge

### Backend Domain

**Primary** (weight 2.0): API, endpoint, server, database, schema, migration, query, ORM, REST, GraphQL, microservice, service, controller, middleware, route, handler, CRUD, transaction, model

**Secondary** (weight 1.0): request, response, payload, JSON, HTTP, status code, webhook, queue, worker, job, cache, session, cookie, rate limit, pagination, filter, sort, batch, bulk, seed, fixture

### Security Domain

**Primary** (weight 2.0): authentication, authorization, encryption, vulnerability, threat, compliance, OWASP, CVE, token, JWT, OAuth, RBAC, ACL, XSS, CSRF, injection, sanitize, hash, salt, certificate

**Secondary** (weight 1.0): password, credential, permission, role, access control, audit log, security header, CORS, CSP, HTTPS, TLS, firewall, rate limit, brute force, session hijack, privilege escalation, data protection, GDPR, PCI, SOC2, secret, key rotation

### Performance Domain

**Primary** (weight 2.0): latency, throughput, optimization, benchmark, profiling, bottleneck, cache, CDN, load balancing, scaling, horizontal, vertical, memory, CPU, concurrent, parallel, async, lazy load

**Secondary** (weight 1.0): response time, load time, bundle size, compression, minification, tree shaking, code splitting, prefetch, preload, connection pooling, query optimization, index, denormalization, batch processing, pagination, infinite scroll, virtual scroll, web worker, service worker

### Documentation Domain

**Primary** (weight 2.0): documentation, README, guide, tutorial, reference, API docs, changelog, release notes, specification, wiki, onboarding, glossary

**Secondary** (weight 1.0): comment, docstring, type annotation, schema description, example, sample, walkthrough, FAQ, troubleshooting, architecture decision record, ADR, diagram, flowchart, sequence diagram

### Testing Domain

**Primary** (weight 2.0): unit test, integration test, e2e test, coverage, test suite, test plan, assertion, mock, fixture, test case, test strategy, test pyramid, qa gate, acceptance test

**Secondary** (weight 1.0): smoke test, regression test, spec file, test runner, test environment, test data, test coverage, test report, snapshot test, contract test, load test, stress test, fuzz test, property-based test

### DevOps/Ops Domain

**Primary** (weight 2.0): runbook, on-call, monitoring, alerting, dashboard, metric, SLO, SLA, deployment, rollout, rollback, feature flag, observability, tracing, capacity planning, incident, escalation

**Secondary** (weight 1.0): canary, blue-green, log level, health check, readiness probe, liveness probe, circuit breaker, failover, disaster recovery, backup, restore, uptime, availability, page, alert threshold, mean time to recovery, MTTR, mean time to detect, MTTD, SRE

---

## Chunked Extraction Protocol (Non-Canonical — Inference-Only)

> **Scope.** The CLI represents chunking only as an **LLM-populated frontmatter flag** — `extraction_mode: (string) one of: standard, chunked` (`prompts.py:217`, `:366`). The CLI does **not** build a section index, does not assemble multi-section chunks, does not run a per-chunk extraction loop, does not perform deduplication merges, and does not execute the 4-pass completeness verification described below. The single `Step(id="extract", ...)` runs the single prompt regardless of spec length; chunking, if it happens, happens entirely inside the LLM's own reasoning over the one prompt. The protocol below is **inference-only guidance** for a skill-mode operator orchestrating extraction by hand, kept here for historical continuity and so the bullet rationale (section index, deduplication, cross-reference resolution, 4-pass verification) is not lost. None of this section should be cited as CLI behaviour.

### Activation

**Threshold**: 500 lines. Below this, use the single-pass extraction described in the canonical section above (no inference-side chunking needed).

### Algorithm

#### 1. Section Index

Scan the spec for headings (H1-H3, detected by `#`, `##`, `###` prefixes) to build a structural map.

For each section, record:

- `heading`: The heading text
- `level`: 1, 2, or 3
- `start_line`: First line of the section (the heading line)
- `end_line`: Last line before the next same-or-higher-level heading (or EOF)
- `line_count`: `end_line - start_line + 1`
- `relevance_tag`: One of `FR_BLOCK`, `NFR_BLOCK`, `SCOPE`, `DEPS`, `RISKS`, `SUCCESS`, `OTHER`

**Relevance tagging heuristic**:

- Heading contains "requirement", "feature", "capability", "functional" → `FR_BLOCK`
- Heading contains "non-functional", "performance", "security", "scalability" → `NFR_BLOCK`
- Heading contains "scope", "boundary", "in scope", "out of scope" → `SCOPE`
- Heading contains "dependency", "dependencies", "integration" → `DEPS`
- Heading contains "risk", "concern", "constraint" → `RISKS`
- Heading contains "success", "criteria", "acceptance", "KPI" → `SUCCESS`
- All other headings → `OTHER`

#### 2. Chunk Assembly

Group sections into chunks targeting ~400 lines per chunk (hard maximum 600 lines).

**Rules**:

- Never split a section across chunks — sections are atomic units
- If a single section exceeds 600 lines, split at paragraph boundaries (blank lines)
- Pack sections sequentially until adding the next section would exceed 600 lines
- The title/overview section (first H1 + its content, up to 50 lines) is prepended as a **context header** to every chunk
- Context header lines do NOT count toward the 400/600 target — they are overhead
- Prefer grouping sections with the same `relevance_tag` together when possible

**Output**: Ordered list of chunks, each containing:

- `chunk_id`: 1-based index
- `sections`: List of sections included
- `line_range`: Start-end lines from original spec
- `line_count`: Total lines (excluding context header)
- `context_header`: First section content (prepended for context)

#### 3. Per-Chunk Extraction

Process each chunk through the eight standard aspects (Aspects 1-7 only; Aspect 8 ID assignment is deferred to the post-merge global pass).

**Per-chunk template**:

```text
Chunk {chunk_id} of {total_chunks}
Line range: L{start}-L{end}
Sections: {section_list}

Context (from spec overview):
{context_header}

---
Chunk content:
{chunk_content}
```

**Important**:

- Each chunk produces a partial extraction result
- `source_lines` references must point to the ORIGINAL spec line numbers, not chunk-relative numbers
- Global ID counters are passed between chunks: `next_fr`, `next_nfr`, `next_dep`, `next_sc`, `next_risk` — this prevents ID collisions between chunks

#### 4. Merge

Concatenate partial results from all chunks by category in document order:

1. Concatenate all FRs from chunk 1, then chunk 2, etc.
2. Concatenate all NFRs from chunk 1, then chunk 2, etc.
3. Repeat for dependencies, success criteria, risks
4. Domain distribution: recompute from merged requirements (not averaged from chunks)
5. Project title/overview: use from chunk 1 only (which has the true overview section)

**Constraint**: This is a structural combination only — no re-interpretation, re-scoring, or re-classification of requirements during merge.

#### 5. Deduplication

Three deduplication checks on the merged result:

| Check | Condition | Action |
|-------|-----------|--------|
| ID collision | Same ID appears in two chunks | Keep first occurrence, discard second, log as `DEDUP_ID_COLLISION` |
| Exact description match | Normalized descriptions identical (case-insensitive, whitespace-normalized) | Keep first occurrence, discard second, log as `DEDUP_EXACT_MATCH` |
| Substring similarity | Similarity ratio > 0.8 (using normalized descriptions) | Keep BOTH items, flag as `DEDUP_REVIEW_NEEDED` |

**Normalization**: Lowercase, collapse whitespace, strip punctuation, remove articles (a, an, the).

#### 6. Cross-Reference Resolution

After merge, scan for unresolved references (e.g., a dependency referencing a requirement ID from another chunk):

1. For each unresolved reference, search merged results for matching items
2. If found: resolve to the correct ID
3. If not found: log as `UNRESOLVED_XREF` warning — do not invent or guess

#### 7. Global ID Assignment

Apply Aspect 8 (ID Assignment) to the merged, deduplicated, cross-referenced result:

- IDs that were explicitly assigned during per-chunk extraction are preserved
- Items without explicit IDs (implicit items) are assigned sequential IDs ordered by `source_lines`
- This produces the final, deterministic ID scheme for the entire extraction

### 4-Pass Completeness Verification (Inference-Only)

> **CLI parity reminder.** The CLI's only mechanical extraction validation is `EXTRACT_GATE` / `EXTRACT_TDD_GATE` against the single `extraction.md` file emitted by the single step. The four passes below — source coverage, anti-hallucination, section coverage, count reconciliation — are not run by the CLI and have no `cli/roadmap/*` implementation. They remain here as inference-side guidance for a skill-mode operator who is orchestrating chunked extraction by hand.

After merge and ID assignment, run 4 verification passes:

| Pass | Name | Method | PASS | WARN | FAIL |
|------|------|--------|------|------|------|
| 1 | Source Coverage | Grep original spec for requirement-indicating patterns ("shall", "must", "should", "will" + nouns); verify each pattern location appears in an extracted item's `source_lines` range | 100% | >=95% | <95% |
| 2 | Anti-Hallucination | For each extracted item, read the original spec at `source_lines` and verify the extraction accurately represents the spec content. Zero tolerance for fabricated requirements | 100% (any failure = FAIL) | N/A | Any failure |
| 3 | Section Coverage | Verify every section tagged as extraction-relevant (`FR_BLOCK`, `NFR_BLOCK`, `SCOPE`, `DEPS`, `RISKS`, `SUCCESS`) was assigned to at least one chunk | 100% | N/A | Any section missed |
| 4 | Count Reconciliation | `sum(chunk_counts) - dedup_removals = merged_totals` for each category (FRs, NFRs, deps, SCs, risks) | Exact match | N/A | Any mismatch |

**On verification failure**:

1. Identify which chunks failed
2. Re-process failing chunks (max 1 retry per chunk)
3. Re-run verification
4. If still failing: STOP with error. Do not produce partial extraction. Report: which pass failed, which chunks, and what was missing

### Worked Example: 1500-Line Spec

**Input**: A 1500-line security-focused microservice spec.

**Step 1: Section Index** (15 sections found):
| Section | Lines | Relevance |
|---------|-------|-----------|
| 1. Executive Summary | L1-L45 | OTHER |
| 2. Architecture Overview | L46-L120 | OTHER |
| 3. Authentication System | L121-L280 | FR_BLOCK |
| 4. Authorization & RBAC | L281-L420 | FR_BLOCK |
| 5. API Endpoints | L421-L580 | FR_BLOCK |
| 6. Data Models | L581-L700 | FR_BLOCK |
| 7. Performance Requirements | L701-L780 | NFR_BLOCK |
| 8. Security Requirements | L781-L900 | NFR_BLOCK |
| 9. Integration Points | L901-L980 | DEPS |
| 10. Success Criteria | L981-L1050 | SUCCESS |
| 11. Risk Assessment | L1051-L1150 | RISKS |
| 12. Migration Plan | L1151-L1280 | FR_BLOCK |
| 13. Testing Strategy | L1281-L1380 | OTHER |
| 14. Deployment Guide | L1381-L1450 | OTHER |
| 15. Appendix | L1451-L1500 | OTHER |

**Step 2: Chunk Assembly** (4 chunks):
| Chunk | Sections | Lines | Line Count |
|-------|----------|-------|------------|
| 1 | Context(L1-45) + Sections 1-4 | L1-L420 | 375 (excl. context) |
| 2 | Context(L1-45) + Sections 5-8 | L421-L900 | 480 |
| 3 | Context(L1-45) + Sections 9-12 | L901-L1280 | 380 |
| 4 | Context(L1-45) + Sections 13-15 | L1281-L1500 | 220 |

**Step 3: Per-Chunk Extraction** (partial results):

- Chunk 1: 12 FRs (auth + RBAC), 0 NFRs, 3 deps
- Chunk 2: 15 FRs (API + models), 8 NFRs (perf + security), 2 deps
- Chunk 3: 5 FRs (migration), 0 NFRs, 4 deps, 6 SCs, 8 risks
- Chunk 4: 0 FRs, 0 NFRs, 0 deps, 0 SCs, 0 risks (non-extraction sections)

**Step 4: Merge**: 32 FRs, 8 NFRs, 9 deps, 6 SCs, 8 risks

**Step 5: Deduplication**: 1 exact match found (FR about "user login" appeared in both auth section and API endpoints section). Removed duplicate. Final: 31 FRs.

**Step 6: Cross-Reference**: 2 unresolved references from chunk 3 (migration deps referencing auth FRs from chunk 1) — resolved to FR-003 and FR-007.

**Step 7: Global ID Assignment**: All items assigned sequential IDs by source_line position.

**Verification**:

- Pass 1 (Source Coverage): 98% → WARN (2 "should" statements in appendix not extracted — appendix tagged OTHER)
- Pass 2 (Anti-Hallucination): 100% PASS
- Pass 3 (Section Coverage): 100% PASS
- Pass 4 (Count Reconciliation): 32 - 1 = 31, all categories match → PASS

**Result**: extraction.md written with `extraction_mode: chunked (4 chunks)` metadata.

---

*Reference document for sc:roadmap v2.0.0 — loaded on-demand during Wave 1B.*

*CLI parity baseline (B-7, VERIFIED): single-pass extraction via `build_extract_prompt` (`src/superclaude/cli/roadmap/prompts.py:180`) or `build_extract_prompt_tdd` (`:328`), wired by `src/superclaude/cli/roadmap/executor.py:2001-2025`, gated by `EXTRACT_GATE` / `EXTRACT_TDD_GATE`. Eight-aspect coverage (Aspects 1-8) is the body-section taxonomy the single prompt instructs the LLM to fill; TDD-extended aspects (9-15) are an inference-only finer-grained taxonomy that overlaps the CLI's six TDD body sections. Domain keyword dictionaries are LLM-advisory; the chunked-extraction protocol and 4-pass completeness verification are non-canonical inference-only and have no CLI implementation.*
