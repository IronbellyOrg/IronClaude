# Research: sc:roadmap Pipeline Full Audit

**Investigation type:** Code Tracer
**Scope:** sc-roadmap-protocol SKILL.md + all refs/
**Status:** Complete
**Date:** 2026-03-24

---

## Section 5: validation.md Findings

**File**: `.claude/skills/sc-roadmap-protocol/refs/validation.md`

### Wave 4 Validation — Two Parallel Agents

Both agents run in parallel (read-only, no artifact modification):

**Quality-Engineer Agent** — 4 dimensions:
| Dimension | Weight | What It Checks |
|-----------|--------|----------------|
| Completeness | 0.35 | Every FR/NFR has a deliverable; every risk in Risk Register; every SC traceable |
| Consistency | 0.30 | ID schemas, frontmatter values match body content, domain distribution matches extraction |
| Traceability | 0.20 | Milestones trace to requirements, deliverables have ACs, source lines are valid |
| Test Strategy | 0.15 | Interleave ratio matches complexity class, validation milestones reference real work milestones, stop-and-fix thresholds defined |

**Self-Review Agent** — 4 questions:
| Question | Weight |
|----------|--------|
| Q1: Does roadmap faithfully represent the spec? | 0.30 |
| Q2: Are milestones achievable and well-ordered? | 0.25 |
| Q3: Does risk assessment match actual risks? | 0.25 |
| Q4: Is the test strategy actionable? | 0.20 |

### Score Aggregation Formula

```
final_score = (quality_engineer_weighted_score * 0.55) + (self_review_weighted_score * 0.45)
```

**Decision thresholds**:
- >= 85%: PASS
- 70-84%: REVISE (up to 2 iterations, then PASS_WITH_WARNINGS)
- < 70%: REJECT

### REVISE Loop

Max 2 iterations. Each iteration: collect recommendations → re-run Wave 3 → re-run Wave 4. After 2 REVISE cycles without PASS: set `PASS_WITH_WARNINGS`.

### No-Validate Behavior

`--no-validate`: Skip Wave 4 entirely, set `validation_status: SKIPPED`, `validation_score: 0.0`.

### Validation Does NOT Read Input Spec Frontmatter

Validation reads output artifacts (roadmap.md, extraction.md, test-strategy.md) and the source spec body content. There is no step that reads or validates YAML frontmatter fields from the INPUT spec.

---

## Section 6: adversarial-integration.md Findings (First 120 Lines)

**File**: `.claude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`

### Mode Detection

4-way detection from flags:
1. `--specs` + `--multi-roadmap` → Combined mode
2. `--specs` alone → Multi-spec consolidation
3. `--multi-roadmap` alone → Multi-roadmap generation
4. Neither → Standard single-spec pipeline

**Implicit `--multi-roadmap` inference**: If `--agents` is present without `--multi-roadmap`, auto-enable `--multi-roadmap`.

### Agent Specification Parsing Algorithm

Format: `model[:persona[:"instruction"]]`, comma-separated list.

Parsing:
1. Split `--agents` on `,`
2. Per agent: split on `:` (max 3 segments)
   - Segment 1: model (required)
   - Segment 2: persona OR instruction if quoted
   - Segment 3: instruction string (quoted)

Model-only agents inherit the primary persona from Wave 1B domain analysis.

### Invocation Patterns

Multi-spec (Wave 1A): `Skill sc:adversarial-protocol --compare <spec-files> --depth <depth> --output <dir> [--interactive]`

Multi-roadmap (Wave 2): `Skill sc:adversarial-protocol --source <spec> --generate roadmap --agents <expanded-specs> --depth <depth> --output <dir> [--interactive]`

Depth propagates directly: quick→1 round, standard→2 rounds, deep→3 rounds.

---

## Section 4: templates.md Findings

**File**: `.claude/skills/sc-roadmap-protocol/refs/templates.md`

### 4-Tier Template Discovery Algorithm

Templates are discovered in strict priority order — first match wins, lower tiers not searched:

| Tier | Search Path | Status |
|------|-------------|--------|
| 1 (Local) | `.dev/templates/roadmap/` in current project | Active |
| 2 (User) | `~/.claude/templates/roadmap/` | Active |
| 3 (Plugin) | `~/.claude/plugins/*/templates/roadmap/` | Future v5.0 — always a no-op currently |
| 4 (Inline) | Algorithmic generation from extraction data | Fallback |

**Validation**: Templates must have YAML frontmatter with at least `name`, `type`, and `domains` fields.

**Template file required fields**: `name`, `type` (feature|quality|docs|security|performance|migration), `domains`
**Optional fields**: `target_complexity` (default 0.5), `min_version` (default "1.0.0"), `milestone_count_range`

### How `spec_type` Is Used in Template Selection

There is **no `spec_type` field** explicitly referenced as a frontmatter input from the spec. Template matching uses:
1. **Candidate filter**: Template's `type` field must match the spec's "dominant requirement type" OR the user's `--template` flag value.
2. "Dominant requirement type" = derived from domain distribution (e.g., backend-dominant spec → type "feature" or closest backend category). This is computed, not read from frontmatter.
3. If `--template` flag is provided, scoring is bypassed entirely and the specified type is used directly.

**There is no path where a `spec_type` YAML frontmatter field from the input spec influences template selection.** The type comes from computed domain distribution or the command-line flag.

### What Happens With No `spec_type` Frontmatter?

Nothing different — there is no `spec_type` frontmatter being read in any case. Template selection always derives the spec type from the extraction's domain distribution.

### Inline Generation Fallback

Triggered when:
- No templates exist in Tiers 1-3
- No template scores >= 0.6
- `--template` flag specifies a type with no matching file

Milestone count formula: `base + floor(domain_count / 2)`
- LOW: base=3, MEDIUM: base=5, HIGH: base=8
- `domain_count` = domains with >= 10% representation

Milestone generation order:
1. M1: Foundation (always, P0)
2. Domain milestones: one per domain with >= 10%, ordered by percentage descending
3. Integration milestone: if domain_count >= 2 (P1)
4. Validation milestone: always last (P3)
Plus interleaved validation milestones per complexity class ratio.

### Output Artifact YAML Frontmatter Schemas (Key Fields)

**roadmap.md frontmatter key fields**: `spec_source`/`spec_sources`, `generated`, `generator`, `complexity_score`, `complexity_class`, `domain_distribution`, `primary_persona`, `consulting_personas`, `milestone_count`, `milestone_index`, `total_deliverables`, `total_risks`, `estimated_phases`, `validation_score`, `validation_status`, `adversarial` (conditional block).

**extraction.md frontmatter key fields**: `spec_source`/`spec_sources`, `generated`, `generator`, `functional_requirements`, `nonfunctional_requirements`, `total_requirements`, `domains_detected`, `complexity_score`, `complexity_class`, `risks_identified`, `dependencies_identified`, `success_criteria_count`, `extraction_mode`, `pipeline_diagnostics` (with `prereq_checks`, `contract_validation` if adversarial, `fallback_activated`).

**test-strategy.md frontmatter key fields**: `spec_source`/`spec_sources`, `generated`, `generator`, `validation_philosophy`, `validation_milestones`, `work_milestones`, `interleave_ratio`, `major_issue_policy`, `complexity_class`.

---

## Section 3: scoring.md Findings

**File**: `.claude/skills/sc-roadmap-protocol/refs/scoring.md`

### Complete Complexity Scoring Formula

Five-factor weighted sum, all factors normalized to [0, 1]:

```
complexity_score = (requirement_count_norm * 0.25)
                 + (dependency_depth_norm  * 0.25)
                 + (domain_spread_norm     * 0.20)
                 + (risk_severity_norm     * 0.15)
                 + (scope_size_norm        * 0.15)
```

| Factor | Raw Value Source | Normalization | Weight |
|--------|-----------------|---------------|--------|
| `requirement_count` | Total FRs + NFRs from extraction | `min(count / 50, 1.0)` | 0.25 |
| `dependency_depth` | Max chain in dependency graph | `min(depth / 8, 1.0)` | 0.25 |
| `domain_spread` | Distinct domains with ≥10% representation | `min(domains / 5, 1.0)` | 0.20 |
| `risk_severity` | `(high*3 + medium*2 + low*1) / total_risks` | `(weighted_avg - 1.0) / 2.0` | 0.15 |
| `scope_size` | Total line count of specification | `min(lines / 1000, 1.0)` | 0.15 |

**Classification thresholds**:
- LOW (< 0.4): 3-4 milestones, 1:3 interleave
- MEDIUM (0.4-0.7): 5-7 milestones, 1:2 interleave
- HIGH (> 0.7): 8-12 milestones, 1:1 interleave

### Does It Read `complexity_score` or `complexity_class` FROM Frontmatter?

**No.** The formula is always computed from scratch using extracted data (requirement counts, dependency depth, domain spread, risks, scope size). There is no conditional like "if spec frontmatter contains `complexity_score`, use that value." The formula reads from extraction outputs, not from any YAML frontmatter field in the input spec.

### Does `spec_type` from Frontmatter Influence Template Selection?

Not explicitly. The `type_match` factor in template compatibility scoring uses the "spec's dominant requirement type." This is computed from the extraction's domain distribution (backend-dominant → backend type, security-dominant → security type), not from a `spec_type` frontmatter field. The `--template` flag bypasses scoring entirely. There is no stated logic that reads `spec_type` from the input spec's YAML frontmatter.

### Template Compatibility Scoring

4-factor formula for selecting among discovered templates:

```
template_score = (domain_match * 0.40)
               + (complexity_alignment * 0.30)
               + (type_match * 0.20)
               + (version_compatibility * 0.10)
```

- `domain_match`: Jaccard similarity between template's `domains` and spec's detected domains
- `complexity_alignment`: `1.0 - abs(template.target_complexity - spec.complexity_score)`
- `type_match`: 1.0 exact, 0.5 related, 0.0 unrelated (per type_match lookup table)
- `version_compatibility`: 1.0 if template min_version ≤ current version, else 0.0

**Selection rule**: Use highest-scoring template with score ≥ 0.6. Fall back to inline generation below 0.6. If `--template` flag set, skip scoring entirely.

### Persona Selection

Confidence formula: `confidence = base_confidence (0.7) * domain_weight * coverage_bonus`

- Primary persona: highest confidence (min 0.3; default "architect" if none qualify)
- Consulting personas: 2nd and 3rd highest (min 0.2)
- Override: `--persona` flag sets primary persona to 1.0 confidence, skips calculation

---

## Section 2: extraction-pipeline.md Findings

**File**: `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`

### The Complete 8-Step Extraction Pipeline

| Step | Name | What It Extracts |
|------|------|-----------------|
| 1 | Title & Overview | `project_title`, `project_version`, `summary` (1-3 sentences) from opening H1 / metadata / executive summary |
| 2 | Functional Requirements (FRs) | Behavioral statements ("shall", "must", "will", "should"), user stories, acceptance criteria. Fields: `id`, `description`, `domain`, `priority` (P0-P3), `source_lines` |
| 3 | Non-Functional Requirements (NFRs) | Performance, security, scalability, reliability, maintainability constraints. Fields: `id`, `description`, `category`, `constraint` (measurable threshold), `source_lines` |
| 4 | Scope & Domain Classification | Classifies every requirement into one or more domains using keyword dictionaries. Computes domain distribution percentages. Five domains: Frontend, Backend, Security, Performance, Documentation |
| 5 | Dependency Extraction | Inter-requirement and external dependencies. Looks for: "requires", "depends on", "after", "before", "blocks". Fields: `id`, `description`, `type` (internal/external), `affected_requirements`, `source_lines` |
| 6 | Success Criteria | Explicit criteria sections, acceptance criteria, KPIs, metrics. Fields: `id`, `description`, `derived_from`, `measurable`, `source_lines` |
| 7 | Risk Identification | Explicit risks + inferred risks from requirement complexity. Fields: `id`, `description`, `probability`, `impact`, `affected_requirements`, `source_lines` (or "inferred") |
| 8 | ID Assignment | Assigns deterministic IDs by `source_lines` order: `FR-{3digits}`, `NFR-{3digits}`, `DEP-{3digits}`, `SC-{3digits}`, `RISK-{3digits}` |

**Critical observation**: The pipeline has NO step for extracting YAML frontmatter field values. It extracts body content based on headings, keywords, and patterns. Frontmatter is validated (Wave 1B Step 1) but its values are not listed as extraction outputs.

### TDD Section Capture Analysis

For each TDD section, does the current 8-step pipeline capture it?

**§7 Data Models** (entity definitions, field types, relationships)
- The worked example shows "Data Models" at L581-L700 tagged as `FR_BLOCK` (heading contains no keyword from the relevance-tagging heuristic).
- Wait — actually: the relevance heuristic says headings containing "requirement", "feature", "capability", "functional" → `FR_BLOCK`. "Data Models" contains none of these, so it would be tagged `OTHER`.
- In the worked example, Section 6 "Data Models" is tagged `FR_BLOCK` — this appears to be an error in the example, OR the tagger picks up `FR_BLOCK` from the API Endpoints context. The worked example is internally inconsistent on this point.
- **Verdict**: "Data Models" would likely be tagged `OTHER` under the stated heuristic rules. Step 2 (FRs) would only extract data model requirements IF they contain "shall/must/will/should" language. Entity definitions as structured tables or field listings with no behavioral statements would NOT be extracted. **PARTIAL capture at best — only behavioral data model requirements, not structural definitions.**

**§8 API Specifications** (endpoint definitions, request/response)
- Headings containing "API", "endpoint" → not in the `FR_BLOCK` heuristic keywords. But "integration" maps to `DEPS`.
- Step 2 picks up behavioral requirements ("The API shall...") if they use modal verbs.
- Step 5 picks up integrations ("depends on", "requires").
- Structured endpoint tables (method, path, request body, response schema) with no behavioral language would NOT be extracted.
- **Verdict**: Partial. Behavioral API requirements captured by Step 2. Structured endpoint specs not captured unless phrased as "shall" statements.

**§9 State Management** (state machines, transitions)
- No domain keyword dict includes "state machine", "transition", "FSM", or related terms.
- Heading "State Management" does not match any relevance-tag heuristic → tagged `OTHER`.
- Behavioral statements within the section ("The system shall transition from X to Y") would be captured by Step 2 as FRs.
- State machine diagrams, transition tables as structured content would NOT be captured.
- **Verdict**: Partial. Behavioral statements captured; structural state definitions not captured.

**§10 Component Inventory** (new/modified/deleted components)
- Heading "Component Inventory" → `OTHER` (no heuristic match).
- Component listings as tables or bullet lists with no behavioral language → NOT captured.
- If phrased as "The system shall add component X" → captured by Step 2.
- **Verdict**: Mostly not captured. Inventory-style content (lists of components with status) is not extracted by any step.

**§14 Observability & Monitoring** (metrics, dashboards, alerts)
- No domain keyword dict includes "observability", "monitoring", "metrics", "dashboards", "alerts" as primary keywords.
- Performance domain secondary keywords include no monitoring/observability terms.
- Heading → tagged `OTHER`.
- Behavioral requirements ("The system shall emit metrics for X") captured by Step 2 as FRs/NFRs.
- **Verdict**: Partial. Behavioral observability requirements captured. Metric definitions, dashboard specs, alert thresholds as structured data not captured.

**§15 Testing Strategy** (unit/integration/e2e breakdown)
- Heading "Testing Strategy" → `OTHER` in the worked example (Section 13 explicitly tagged OTHER).
- No heuristic maps "testing", "unit", "integration", "e2e" to an extraction-relevant tag.
- Step 3 picks up "maintainability" NFRs which could include code coverage requirements.
- Test strategy as a structured breakdown (what to test, how, thresholds) → NOT captured.
- **Verdict**: Mostly not captured. Code coverage NFRs captured; test strategy structure not captured.

**§19 Migration & Rollout Plan** (phases, cutover steps)
- Heading "Migration Plan" in the worked example is explicitly tagged `FR_BLOCK` (Section 12, L1151-L1280).
- The relevance heuristic does NOT include "migration" or "rollout" in the `FR_BLOCK` keywords. Yet the worked example tags it `FR_BLOCK`. This is an inconsistency in the ref.
- Assuming the worked example reflects intended behavior: migration requirements ARE extracted by Steps 2/5.
- Cutover phase sequences as structured plans (not behavioral requirements) would still not be captured.
- **Verdict**: Mixed — migration requirements with behavioral language captured; phase plans and cutover steps as procedural content not captured. The worked example behavior and the stated heuristic are inconsistent.

**§24 Release Criteria** (Definition of Done)
- Heading "Release Criteria" → `SUCCESS` tag if contains "criteria" or "acceptance".
- Step 6 (Success Criteria) explicitly extracts "Explicit success criteria sections, acceptance criteria, KPIs".
- **Verdict**: YES, captured by Step 6. Release criteria / Definition of Done content is directly targeted by this step.

**§25 Operational Readiness** (runbooks, on-call)
- Heading "Operational Readiness" → `OTHER` (no heuristic match for "operational", "runbook", "on-call").
- Not targeted by any extraction step.
- **Verdict**: NOT captured. Runbooks, on-call procedures, operational readiness checklists are entirely outside the pipeline's extraction scope.

### Summary Table: TDD Section Capture

| TDD Section | Captured? | By Which Step | Notes |
|-------------|-----------|---------------|-------|
| §7 Data Models | Partial | Step 2 (behavioral only) | Structural definitions missed |
| §8 API Specifications | Partial | Step 2 + Step 5 | Endpoint tables missed |
| §9 State Management | Partial | Step 2 (behavioral only) | State machine structure missed |
| §10 Component Inventory | Mostly No | Step 2 (behavioral only) | Inventory lists missed |
| §14 Observability & Monitoring | Partial | Step 2 + Step 3 | Metric/alert definitions missed |
| §15 Testing Strategy | Mostly No | Step 3 (coverage NFRs only) | Test strategy structure missed |
| §19 Migration & Rollout | Partial | Step 2 + Step 5 | Phase plans missed; worked example inconsistency |
| §24 Release Criteria | YES | Step 6 (Success Criteria) | Directly targeted |
| §25 Operational Readiness | NO | None | Outside extraction scope entirely |

### Domain Keyword Gap

The five domain dictionaries are: Frontend, Backend, Security, Performance, Documentation. There is **no Testing domain, no DevOps/Ops domain, no Data/ML domain**. TDD sections in Observability, Testing Strategy, and Operational Readiness would systematically score poorly against all domains and may be classified as OTHER or Backend/Performance based on incidental keyword overlap.

---

## Section 1: SKILL.md Findings

**File**: `.claude/skills/sc-roadmap-protocol/SKILL.md`

### Wave 0: YAML Frontmatter Fields Read from Input Spec

Wave 0 does **NOT** read any YAML frontmatter fields from the input spec. Its actions are:
- Validate spec file(s) exist and are readable
- Validate output directory is writable
- Check for artifact collisions
- Check template directory availability
- Verify sc:adversarial skill is installed (if `--specs`/`--multi-roadmap`)
- Log fallback decisions

**No frontmatter parsing occurs in Wave 0.** The spec is treated as a file to validate for existence/readability, not content.

### Wave 1B: YAML Frontmatter — Validation vs. Usage

Wave 1B Step 1 states:
> "Parse specification file (single spec or unified spec from Wave 1A). If spec contains YAML frontmatter, **validate it parses correctly**. If malformed YAML, abort..."

This language is **validation-only** — the skill validates that the YAML is syntactically correct but the SKILL.md text does not explicitly state that it reads or uses any specific frontmatter field values. The key behaviors in Wave 1B are:
1. Validate frontmatter is parseable (abort on malformed YAML)
2. Run the 8-step extraction pipeline from `refs/extraction-pipeline.md`
3. Score complexity using the 5-factor formula from `refs/scoring.md`

Whether specific frontmatter field values (like `spec_type`, `complexity_score`, `complexity_class`) are consumed depends on what `refs/extraction-pipeline.md` and `refs/scoring.md` specify — the SKILL.md itself only says to "apply" those refs.

### Does SKILL.md Pass Frontmatter Values to Scoring?

Not explicitly stated in SKILL.md. The SKILL.md says to "Score complexity using the 5-factor formula from `refs/scoring.md`" — the formula details and whether it reads from frontmatter are in that ref. **Deferred to scoring.md section below.**

### Does SKILL.md Override Computed Scores with Frontmatter Values?

No override logic is visible in SKILL.md. The skill always scores from scratch ("5-factor formula from `refs/scoring.md`"). No conditional like "if frontmatter contains complexity_score, skip scoring" appears anywhere in the SKILL.md text.

### Key Flags That Reference Frontmatter-Like Fields

From the `--template` flag: `--template feature|quality|docs|security|performance|migration` — this can be provided on the command line. If not provided, it is "auto-detect". The connection to a `spec_type` field in the spec's YAML frontmatter is not stated in SKILL.md — that logic lives in `refs/templates.md`.

### Output Artifacts and Their Frontmatter

The 3 output artifacts all contain YAML frontmatter:
- `roadmap.md` — includes `validation_score`, `validation_status`, `spec_source`/`spec_sources`, `adversarial` block (if adversarial mode)
- `extraction.md` — includes `pipeline_diagnostics` block with `prereq_checks`, optional `contract_validation`
- `test-strategy.md` — schema from `refs/templates.md`

**Critical rule**: "Exactly one of `spec_source` (scalar) or `spec_sources` (list) — never both, never neither"

---

## Summary

The sc:roadmap pipeline is a 5-wave system (Wave 0 through Wave 4) that transforms a specification document into 3 output artifacts: `roadmap.md`, `extraction.md`, and `test-strategy.md`.

**YAML Frontmatter from Input Spec — What Is Actually Used:**

The pipeline reads input spec YAML frontmatter for exactly ONE purpose: **syntax validation** (Wave 1B Step 1). If the YAML is malformed, the pipeline aborts. The field values within that frontmatter are NOT consumed by any extraction step, scoring formula, or template selection algorithm. Specifically:

- `spec_type` / `complexity_score` / `complexity_class` from input spec frontmatter: **ignored by all pipeline logic**
- Complexity is always computed from scratch via the 5-factor formula in scoring.md
- Template type is always derived from computed domain distribution (or `--template` CLI flag)
- Persona is always selected from computed domain distribution (or `--persona` CLI flag)

**The Exact Extraction Pipeline:**

8 steps, executed sequentially in Wave 1B:
1. Title & Overview — extracts `project_title`, `project_version`, `summary`
2. Functional Requirements — behavioral statements ("shall/must/will/should"), user stories, ACs
3. Non-Functional Requirements — performance, security, scalability, reliability, maintainability
4. Scope & Domain Classification — keyword-weighted domain assignment (5 domains)
5. Dependency Extraction — inter-requirement and external dependencies
6. Success Criteria — measurable criteria, KPIs, ACs
7. Risk Identification — explicit + inferred risks
8. ID Assignment — deterministic IDs by source_lines position

**TDD-Structured Input Capture:**

Of the 9 TDD sections examined:
- **Fully captured**: §24 Release Criteria (via Step 6 Success Criteria)
- **Partially captured** (behavioral statements only): §7 Data Models, §8 API Specs, §9 State Management, §10 Component Inventory, §14 Observability, §19 Migration & Rollout
- **Mostly not captured**: §15 Testing Strategy (only coverage NFRs via Step 3)
- **Not captured at all**: §25 Operational Readiness

The core limitation: the extraction pipeline targets text patterns ("shall/must/will/should", heading keywords) and extracts behavioral requirements. It does not extract structured content (tables of entity definitions, endpoint schemas, state machine diagrams, component inventories, runbook procedures) unless that content is phrased as behavioral requirements.

---

## Gaps and Questions

1. [Critical] **Frontmatter field `spec_type` — is it ever read anywhere?** The SKILL.md, extraction-pipeline.md, scoring.md, and templates.md contain no reference to reading a `spec_type` field from input spec frontmatter. But the `--template` flag accepts exactly the same values (`feature|quality|docs|security|performance|migration`). Is there an undocumented convention that `spec_type` in the spec frontmatter should be used to auto-populate `--template`? The pipeline as documented does not do this.

2. [Important] **"Data Models" tagged FR_BLOCK in worked example but heuristic says OTHER** — The worked example in extraction-pipeline.md tags "Data Models" as `FR_BLOCK` (Section 6, L581-L700), but the relevance-tagging heuristic lists no keyword that would match "Data Models". This is an inconsistency in the ref document. TDD §7 Data Models would be tagged `OTHER` under the stated rules, meaning it gets de-prioritized in chunk assembly.

3. [Critical] **No Testing or DevOps domain** — The 5-domain keyword dictionaries (Frontend, Backend, Security, Performance, Documentation) have no Testing or Ops domain. TDD sections for §15 Testing Strategy and §25 Operational Readiness have no matching domain, which means requirements from those sections would be scored as Documentation or miscategorized.

4. [Important] **Complexity frontmatter override path missing** — A spec author who knows their project complexity and puts `complexity_class: HIGH` in the spec frontmatter will have that value silently ignored. The pipeline always recomputes. This could be a design gap if the spec author has domain knowledge the formula cannot capture.

5. [Important] **§19 Migration & Rollout heuristic inconsistency** — The worked example tags "Migration Plan" as `FR_BLOCK` but the heuristic keywords don't include "migration". The actual behavior is ambiguous. If migration sections are tagged `OTHER`, they may be deprioritized in chunk grouping.

6. [Important] **TDD §10 Component Inventory — inventory lists invisible to pipeline** — Component inventory (new/modified/deleted component tables) is a common TDD pattern. None of the 8 extraction steps target inventory-style structured content. Only behavioral requirements extracted from that section would be captured.

---

## Key Takeaways

1. **YAML frontmatter in input spec is validate-only.** The pipeline validates that it parses correctly but extracts zero values from it. `spec_type`, `complexity_score`, `complexity_class`, and any other frontmatter fields in the input spec have no effect on pipeline behavior.

2. **The pipeline is behavioral-requirement-centric.** It targets modal verbs ("shall/must/will/should"), user story patterns, and heading keywords. TDD documents that express requirements in other forms (entity tables, state machine diagrams, component inventories, runbooks) will have significant content missed.

3. **Of the 9 TDD sections examined, only §24 Release Criteria is fully and directly captured.** Six sections are partially captured (behavioral statements only). Two sections — §15 Testing Strategy and §25 Operational Readiness — are largely invisible to the extraction pipeline.

4. **Template selection derives type from computed domain distribution, not from spec frontmatter.** A spec with `spec_type: migration` in its frontmatter will not automatically select the migration template — the type must match through domain keyword scoring or via the `--template` CLI flag.

5. **The 5-domain dictionaries create a structural blind spot for TDD-heavy specs.** TDD specs emphasizing testing strategy, operational readiness, observability, and component inventory will score low on all 5 domains and be classified as low-complexity backend or documentation work, potentially underestimating the actual scope.

6. **The complexity formula inputs are fully derivable from extraction outputs.** All 5 factors (requirement count, dependency depth, domain spread, risk severity, scope size) come from the extraction itself. This means a spec that front-loads most complexity into non-extractable sections (diagrams, tables, runbooks) will produce an understated complexity score.

7. **Validation (Wave 4) checks internal consistency of output artifacts.** It does not re-validate against input spec frontmatter. The quality-engineer agent checks that frontmatter values in output artifacts match body content — not that they match any values the spec author put in the input spec.

