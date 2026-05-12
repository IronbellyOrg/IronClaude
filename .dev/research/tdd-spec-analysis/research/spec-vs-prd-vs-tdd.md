# Analysis: IronClaude Spec vs PRD vs TDD

**Date**: 2026-03-24
**Scope**: Comparative analysis of IronClaude release spec format, PRD template, TDD template, and the full pipeline that consumes them
**Question**: What does each do well, what's missing, and how should IronClaude's flow evolve?

---

## Understanding of Document Scope

**PRD** — per-product or per-feature. Created once and lives for the entire life of that feature, spanning many releases. Defines the *what* and *why*: user needs, business context, personas, success metrics, scope boundaries.

**TDD** — per-feature or per-component. Also long-lived, not per-release. Translates the PRD into a detailed engineering design: data models, API contracts, state management, security, observability, testing strategy, architecture decisions. Significantly more information-dense than anything per-release.

**Spec** — per-release. Scoped to a specific version increment. Describes what portion of the TDD gets built *this sprint/release*.

The correct hierarchy is:

```
PRD (feature-level, long-lived — "what and why")
  → TDD (feature-level, long-lived — "how to build it, in full detail")
    → Spec (release-scoped — "build these parts of the TDD in this increment")
      → sc:roadmap → sc:tasklist → sprint executor
```

---

## IronClaude's Actual Current State

**IronClaude has no automated spec creation skill.** The planned `/sc:spec` command in `.dev/releases/backlog/v5xx-Spec-generator-framework/` was researched and designed but never built.

**IronClaude has no TDD** for any of its own features. Features like spawn, forensic, task-unified, and the roadmap pipeline have no persistent technical design document. Each new release spec re-explains context and re-discovers design decisions the prior spec already worked out.

**IronClaude has used PRDs inconsistently** — at least twice for sc:cleanup-audit, archived with the release rather than maintained as living documents.

**The spec is the only input to the pipeline.** The spec is point-in-time and abandoned after the release moves to archive.

**The actual current pipeline:**

```
Spec created (see two paths below)
  → /sc:roadmap <spec-file>
    → /sc:tasklist <roadmap>
      → superclaude sprint run
```

### How the spec gets created — two paths

**Path A: Manual creation from the template**
The user copies `src/superclaude/examples/release-spec-template.md`, fills in all `{{SC_PLACEHOLDER:*}}` fields, and optionally runs `/sc:spec-panel @spec.md` to review and improve it. The template's usage note explicitly names spec-panel as the quality gate. When created this way, the spec contains the YAML frontmatter fields (`spec_type`, `complexity_score`, `complexity_class`, `quality_scores`) — however, sc:roadmap does not currently consume these values. The pipeline validates YAML syntax and computes all values from scratch regardless of what the frontmatter contains.

**Path B: Does not currently exist**
`/sc:spec-panel` accepts `[specification_content|@file]`, but **spec-panel cannot create specs from raw instructions**. Its Boundaries section explicitly states "Will Not: Generate specifications from scratch without existing content or context." Passing raw instructions or a description will not produce a full structured spec — spec-panel will attempt a review or critique of that description but will not generate a spec. Confirmed: no protocol skill exists for spec-panel, and the command file contains no reference to `release-spec-template.md`, `spec_type`, `complexity_score`, `complexity_class`, `quality_scores`, `SC_PLACEHOLDER`, or the sentinel system. The only "sentinel" references in spec-panel are Whittaker's *Sentinel Collision Attack* — an adversarial testing methodology, unrelated to `{{SC_PLACEHOLDER:*}}`.

**Path B must be built.** It requires wiring spec-panel to the `release-spec-template.md` and adding creation-mode logic. Until that work is done, there is no automated path from raw instructions to a structured spec.

**The critical implication:** Path B does not currently exist. The YAML frontmatter fields in the spec template (`spec_type`, `complexity_score`, `complexity_class`, `quality_scores`) are validated for YAML syntax by sc:roadmap but **none of their values are consumed by any extraction step, scoring formula, or template selection algorithm**. sc:roadmap ignores those field values regardless of how the spec was created — it computes all values from scratch. This means the frontmatter advantage does not exist in either path. Even a fully-populated Path A spec produces identical pipeline behavior to a spec with no frontmatter at all. Adding these fields to the TDD template is still the right direction, but the reason is forward-looking: they need to exist so that future pipeline upgrades can read them — not because the current pipeline uses them.

---

## What the IronClaude Spec Does Well That PRD/TDD Do Not

### 1. YAML frontmatter — *not currently consumed by sc:roadmap*
The spec template has machine-readable fields (`spec_type`, `complexity_score`, `complexity_class`, `quality_scores`) that are intended for pipeline consumption, but **sc:roadmap does not read these field values**. The pipeline validates that the YAML parses correctly (malformed YAML aborts the run), but no extraction step, scoring formula, or template selection algorithm consumes the values.

- `spec_type` — sc:roadmap does NOT use this field for template selection. Template type is computed entirely from body-text domain keyword analysis using a 5-domain keyword dictionary. Adding `spec_type` to the TDD or spec frontmatter has zero effect on the current pipeline.
- `complexity_score` / `complexity_class` — the relationship between `complexity_class` and milestone count (LOW=3-4, MEDIUM=5-7, HIGH=8-12) is real, but the pipeline computes `complexity_class` from scratch using its 5-factor formula. It does not read the value from spec frontmatter.
- `quality_scores` (clarity, completeness, testability, consistency) — not read by sc:roadmap. The field is entirely ignored. sc:spec-panel produces its own quality metrics under a different schema (`overall_score`, `requirements_quality`, `architecture_clarity`, `testability_score`) and does not write back to the `quality_scores` field.

**The frontmatter advantage does not exist in either path.** Even when a spec is manually created from the template with all frontmatter fields fully populated (Path A), sc:roadmap ignores those values and computes everything from scratch. The argument for adding these fields to the TDD is forward-looking: they should be used, and adding them now enables future pipeline upgrades to read them without changing the document structure.

### 2. Sentinel system with quality gate
The `{{SC_PLACEHOLDER:*}}` sentinel pattern enforces completeness — `grep -c '{{SC_PLACEHOLDER:'` must return 0 before the spec is considered done. sc:spec-panel is explicitly named as the quality gate in the template header. Nothing equivalent exists in the TDD.

### 3. Scope boundary in pipeline-parseable format
The spec's "In scope / Out of scope" is a two-field section extraction can directly parse. The TDD's non-goals table is richer but not in the same format.

### 4. Concise, release-scoped document
The spec is scoped to a single increment. It's fast to write and fast to parse. The TDD describes the entire feature — passing it whole to sc:roadmap would work but is architecturally heavier than needed for a single release.

---

## What the PRD Does Well That the Spec Does Not

The spec is missing this layer entirely. Because IronClaude has no PRD for its features, none of this feeds the pipeline:

- **Business intelligence**: TAM/SAM/SOM, revenue projections, KPIs with measurement methods
- **JTBD framework**: User motivation modeling — prevents building the right solution to the wrong problem
- **User personas**: Goals, pain points, technical proficiency
- **Competitive analysis**: Why existing solutions fall short
- **Customer journey map**: End-to-end user experience
- **Strategic fit and "Why Now"**: Market timing, company objective alignment, strategic bets
- **Document lifecycle governance**: Approval chains, review cadence, maintainers
- **Living document model**: Requirements evolve; the spec is point-in-time

---

## What the TDD Does Well That the Spec Does Not

The TDD is significantly more information-dense. This is what the spec is missing — and what the pipeline is currently flying blind on:

### Rich content sc:roadmap currently does NOT extract

| TDD Section | Content | Pipeline Value If Extracted |
|-------------|---------|---------------------------|
| **Data Models (§7)** | Entity definitions, field types, relationships, constraints | Complexity signal: entity + relationship count → milestone sizing |
| **API Specifications (§8)** | Endpoint definitions, request/response schemas, status codes | Complexity signal: endpoint count + surface area → milestone sizing |
| **Component Inventory (§10)** | New / modified / deleted components with roles | Direct task generation: one implementation task per new/modified component |
| **State Management (§9)** | State machines, transitions, persistence strategies | Complexity signal: state count → risk register, phase planning |
| **Testing Strategy (§15)** | Unit/integration/e2e breakdown, coverage targets | Dedicated test implementation tasks in correct phase |
| **Migration & Rollout Plan (§19)** | Phases, feature flags, cutover steps, rollback | Direct roadmap phase structure: migration steps map to phases |
| **Release Criteria (§24)** | Explicit Definition of Done per milestone | Milestone exit criteria — currently implicit |
| **Observability & Monitoring (§14)** | Metrics, dashboards, alerting thresholds | Dedicated instrumentation tasks in roadmap |
| **Security Considerations (§13)** | Threat model, auth, RBAC, encryption | Dedicated security work items — currently just NFR keywords |
| **Operational Readiness (§25)** | Runbooks, on-call procedures | Documentation/ops tasks |
| **Alternatives Considered (§21)** | Rejected approaches with rationale | Reduces risk register inflation — known non-starters don't become risks |
| **Cost & Resource Estimation (§26)** | Engineering time estimates | Milestone sizing signal |

### Other TDD strengths over the spec

- **Non-goals with rationale** — not just "out of scope" but *why*, prevents scope creep
- **PRD traceability chain** — `parent_doc` link traces requirements to their origin
- **Business metric bridging** — maps business KPIs to engineering proxy metrics with instrumentation plans
- **Formal API contracts** — binding, not illustrative
- **Binding data model schemas** — implementation contracts, not descriptions
- **Living document** — evolves across releases; the spec is abandoned after each release

---

## What in the Spec Is Worth Adding to the TDD

### YAML frontmatter fields (required for future pipeline compatibility — not consumed by current pipeline)

```yaml
spec_type: new_feature | refactoring | migration | infrastructure | security | performance | docs
complexity_score: 0.0–1.0  # pre-computed or pipeline-computed
complexity_class: LOW | MEDIUM | HIGH
quality_scores:
  clarity: 0.0–10.0
  completeness: 0.0–10.0
  testability: 0.0–10.0
  consistency: 0.0–10.0
feature_id: [identifier]
target_release: [version]
parent_prd: [path or null]
```

### Sentinel system
`{{SC_PLACEHOLDER:*}}` pattern for unfilled fields, with sentinel self-check as a quality gate.

### Quality gate note
Explicit instruction to run `/sc:spec-panel --focus correctness,architecture` before feeding the TDD to sc:roadmap.

---

## The Three Options

### Option 1: TDD → Spec via sc:spec-panel
Generate a release spec FROM the TDD using sc:spec-panel. Note: spec-panel does not currently output in spec template format — it produces a structured review/analysis document in one of three defined formats (`--format standard`, `--format structured`, `--format detailed`). Under `--focus correctness`, three artifact tables are mandatory hard gates. The output is always a review document, not a standalone revised spec file. This option would require wiring spec-panel to output in spec template format first.

**Pros:** Pipeline untouched. Spec template's sentinel system stays intact.

**Cons:**
- Two documents to maintain per feature that can drift (TDD is source of truth but spec feeds the pipeline)
- Content loss risk — spec-panel has no instruction to preserve TDD content depth
- sc:spec-panel doesn't know the spec template exists; needs explicit wiring
- The pipeline remains blind to TDD's rich data — it only sees the thin derived spec
- Per-release spec still gets abandoned after the release

### Option 2: Modify the TDD template only (minimal)
Add the spec's YAML frontmatter fields to the TDD. Note: sc:roadmap does not currently read these field values — it validates YAML syntax and computes all values from scratch. Adding the fields to the TDD has no effect on current pipeline behavior. This option only becomes meaningful if pipeline changes are made simultaneously to actually consume those fields.

**Pros:** Single source of truth. Establishes frontmatter schema for future pipeline upgrades. Lower scope than Option 3.

**Cons:**
- Adding frontmatter fields alone produces no pipeline benefit without the corresponding sc:roadmap changes to read them
- The pipeline still only uses a fraction of what the TDD contains
- Roadmap complexity scoring, milestone planning, and task generation remain as shallow as they are today
- The rich data in the TDD (data models, API specs, component inventory, migration plan) goes completely unused
- Requires at least some of the same pipeline changes as Option 3, making Option 3's incremental cost low once foundational changes are committed

### Option 3: Modify the TDD template AND upgrade the pipeline tools ✅ Recommended

Add frontmatter to the TDD AND upgrade sc:roadmap, sc:spec-panel, and sc:tasklist to actively consume the TDD's rich sections. The TDD becomes the single source of truth for the entire pipeline.

**Pros:**
- Single source of truth — no duplication, no drift
- No content loss
- Dramatically richer roadmaps: complexity scoring uses data model + API surface + component count, not just requirement count
- Dramatically richer task lists: tasks generated from component inventory, migration steps, testing strategy, observability requirements
- Spec-panel provides deeper technical review: experts review actual API contracts, data models, state machines
- TDD evolves across releases; pipeline always has full feature context

**Cons:** Requires changes to sc:roadmap extraction pipeline, sc:roadmap scoring, sc:spec-panel, and sc:tasklist. Significant but well-bounded scope.

---

## Recommended Course: Option 3

**The TDD becomes the input to the pipeline. The spec template is retired or becomes an optional thin wrapper for simple releases.**

---

## What Needs to Change

### 1. TDD Template — Add Pipeline Frontmatter

Add the following to the TDD YAML frontmatter (these are the fields sc:roadmap should read once pipeline changes land — the current pipeline does not consume these values, it computes all of them from scratch):

```yaml
spec_type: {{SC_PLACEHOLDER:new_feature|refactoring|migration|infrastructure|security|performance|docs}}
complexity_score: {{SC_PLACEHOLDER:0.0_to_1.0}}
complexity_class: {{SC_PLACEHOLDER:LOW|MEDIUM|HIGH}}
target_release: {{SC_PLACEHOLDER:version}}
quality_scores:
  clarity: {{SC_PLACEHOLDER:0.0_to_10.0}}
  completeness: {{SC_PLACEHOLDER:0.0_to_10.0}}
  testability: {{SC_PLACEHOLDER:0.0_to_10.0}}
  consistency: {{SC_PLACEHOLDER:0.0_to_10.0}}
```

Add sentinel self-check instruction and quality gate note to the template header.

### 2. sc:roadmap Extraction Pipeline — New Extraction Steps

The current 8-step extraction pipeline needs these additional steps for TDD input:

| New Step | Extracts From | Output | Pipeline Use |
|----------|--------------|--------|--------------|
| **Step 9: Data Model Extraction** | §7 Data Models | Entity count, relationship count, field complexity | New complexity factor |
| **Step 10: API Surface Extraction** | §8 API Specs | Endpoint count, method distribution | New complexity factor |
| **Step 11: Component Inventory Extraction** | §10 Component Inventory | New / modified / deleted component lists | Direct milestone work items |
| **Step 12: Migration Phase Extraction** | §19 Migration & Rollout | Ordered migration phases, rollback points | Maps directly to roadmap phase structure |
| **Step 13: Release Criteria Extraction** | §24 Release Criteria | DoD items per milestone | Milestone exit criteria |
| **Step 14: Observability Extraction** | §14 Observability | Metrics, dashboards, alerts to build | Dedicated instrumentation work items |

**TDD-format detection rule**: If the input document contains `## 7. Data Models` or `## 8. API Specifications` or `## 10. Component Inventory`, activate Steps 9-14.

### 3. sc:roadmap Scoring — Updated Complexity Formula

Current 5-factor formula covers: requirement_count (0.25), dependency_depth (0.25), domain_spread (0.20), risk_severity (0.15), scope_size (0.15).

Add TDD-specific factors when TDD-format input is detected:

| New Factor | Raw Value | Normalization | Weight |
|-----------|-----------|---------------|--------|
| `api_surface` | Total endpoint count | `min(count / 30, 1.0)` | 0.10 |
| `data_model_complexity` | Entity count + relationship count | `min(count / 20, 1.0)` | 0.10 |

Redistribute existing weights to sum to 1.0: requirement_count (0.20), dependency_depth (0.20), domain_spread (0.15), risk_severity (0.10), scope_size (0.15), api_surface (0.10), data_model_complexity (0.10).

### 4. sc:spec-panel — TDD-Aware Expert Behaviors

When input contains TDD sections (detected by heading patterns), activate enhanced expert behaviors:

| Expert | Standard Behavior | TDD-Enhanced Behavior |
|--------|------------------|----------------------|
| **Fowler** | Reviews requirement text for architecture issues | Reviews actual API contracts for interface design, reviews data models for coupling/cohesion |
| **Nygard** | Reviews NFRs for reliability | Reviews actual state machines for failure modes, reviews migration plan for rollback gaps |
| **Whittaker** | Attacks requirement invariants | Attacks actual data model schemas (null fields, sentinel collisions), attacks API endpoint contracts |
| **Wiegers** | Validates FR completeness | Cross-validates FRs against component inventory — every component should have corresponding FRs |
| **Crispin** | Reviews acceptance criteria | Reviews testing strategy section directly, validates coverage targets are measurable |
| **Newman** | Reviews service boundary text | Reviews actual API specifications for service evolution and backward compatibility |

**TDD detection rule**: If input contains `## 7. Data Models` or `## 8. API Specifications`, activate TDD-enhanced behaviors.

### 5. sc:tasklist — TDD-Aware Task Generation

The tasklist currently generates tasks from roadmap items only (headings, bullets, numbered items). When the roadmap was generated from a TDD, the following additional task generation rules apply:

| Source | Task Generation Rule |
|--------|---------------------|
| **Component Inventory** | One implementation task per new component. One modification task per modified component. One removal + dependency-update task per deleted component. |
| **Migration Plan** | Migration phases map directly to tasklist phases in order. Each migration step becomes an explicit task with rollback criteria. |
| **Testing Strategy** | One test implementation task per test category (unit, integration, e2e) with explicit coverage targets as acceptance criteria. |
| **Observability Plan** | One instrumentation task per metric/dashboard/alert defined in §14. |
| **Operational Readiness** | One documentation task per runbook defined in §25. |
| **Release Criteria** | DoD items become explicit verification tasks at the end of the final phase. |

**Implementation note**: These rules activate when the roadmap's `extraction.md` frontmatter contains `tdd_input: true`, which sc:roadmap sets when TDD-format detection triggers.

---

## The Upgraded Full Pipeline

```
/prd skill                                     ← creates PRD (feature-level, long-lived)
  → /tdd skill (fed the PRD)                   ← creates TDD (feature-level, long-lived)
    → /sc:spec-panel @tdd.md                   ← TDD-aware expert review + quality gate
      → /sc:roadmap @tdd.md                    ← TDD-aware extraction → rich roadmap
        → /sc:tasklist <roadmap>               ← TDD-aware task generation → specific tasks
          → superclaude sprint run             ← executes
```

For follow-on releases of the same feature:
```
TDD updated with new sections/requirements    ← living document, not abandoned
  → /sc:spec-panel @tdd.md --focus [changed sections]
    → /sc:roadmap @tdd.md                     ← extracts only what's new/changed via spec_type + target_release scoping
      → /sc:tasklist <roadmap>
        → superclaude sprint run
```

---

## Summary Table

| Capability | Spec | PRD | TDD | TDD + Upgrades |
|-----------|------|-----|-----|----------------|
| Pipeline frontmatter (spec_type, complexity_class) | ✅ | ❌ | ❌ add | ✅ |
| Sentinel quality gate | ✅ | ❌ | ❌ add | ✅ |
| FRs/NFRs/risks/deps for roadmap extraction | ✅ | ❌ | ✅ | ✅ |
| Data model complexity → milestone sizing | ❌ | ❌ | ✅ unused | ✅ |
| API surface → milestone sizing | ❌ | ❌ | ✅ unused | ✅ |
| Component inventory → task generation | ❌ | ❌ | ✅ unused | ✅ |
| Migration phases → roadmap phases | ❌ | ❌ | ✅ unused | ✅ |
| Testing strategy → test tasks | ❌ | ❌ | ✅ unused | ✅ |
| Release criteria → milestone exit criteria | ❌ | ❌ | ✅ unused | ✅ |
| Observability → instrumentation tasks | ❌ | ❌ | ✅ unused | ✅ |
| Deep expert review (actual contracts/schemas) | ❌ | ❌ | ✅ unused | ✅ |
| Non-goals with rationale | ⚠️ | ⚠️ | ✅ | ✅ |
| Alternatives considered (ADRs) | ⚠️ rare | ❌ | ✅ | ✅ |
| Living document across releases | ❌ abandoned | ✅ | ✅ | ✅ |
| PRD traceability | ❌ | ✅ origin | ✅ downstream | ✅ |
| Business intelligence (JTBD/personas/KPIs) | ❌ | ✅ | ⚠️ bridged | ⚠️ bridged |
| Document lifecycle governance | ❌ | ✅ | ✅ | ✅ |

---

## Recommended Next Steps (Ordered)

0. **Verify all corrected claims are reflected in this document** — five factual errors were identified by code-level research and corrected here: (1) spec-panel cannot create specs from raw instructions (Path B does not exist), (2) sc:roadmap does not read `spec_type` from frontmatter for template selection, (3) sc:roadmap does not read `quality_scores` from frontmatter, (4) the frontmatter advantage does not exist in either path — pipeline ignores those field values entirely, (5) spec-panel output is constrained to three defined format modes (`standard`, `structured`, `detailed`), always a review document. Full verified findings in `.dev/tasks/to-do/TASK-RESEARCH-20260324-001/RESEARCH-REPORT-prd-tdd-spec-pipeline.md`.

1. **Add pipeline frontmatter to TDD template** — add `spec_type`, `complexity_score`, `complexity_class`, `quality_scores`, `feature_id`, `target_release` fields so the structure exists for future pipeline upgrades. These fields are not currently consumed by sc:roadmap; pipeline changes (step 3 below) are required to make them meaningful.

2. **Build Path B — wire spec-panel for spec creation** — currently no protocol skill exists for spec-panel and it explicitly refuses to generate specs from scratch. To build Path B: create a spec-panel companion skill package, add creation-mode logic, and wire the command to `release-spec-template.md` so it can:
   - When given raw instructions or a TDD: output in `release-spec-template.md` format with all required frontmatter fields populated
   - When given a TDD: preserve all TDD content, scope to the target release, and add the pipeline frontmatter
   - Until this is built, the only path to a structured spec is manual template creation (Path A)

3. **Add TDD-aware extraction steps to sc:roadmap** — Steps 9-14 above. Unlocks richer roadmaps from TDD input.

4. **Update sc:roadmap scoring formula** — add `api_surface` and `data_model_complexity` factors. Unlocks accurate milestone sizing from TDD data.

5. **Add TDD-enhanced behaviors to sc:spec-panel** — expert review against actual API contracts, data models, and state machines — not just requirement text.

6. **Add TDD-aware task generation to sc:tasklist** — component inventory, migration phases, testing strategy, observability as explicit tasks.

7. **Wire PRD → TDD handoff in the tdd skill** — synthesis agents explicitly consume PRD epics, ACs, and success metrics as foundational inputs.

8. **Update the spec template** to reference the TDD as upstream source, or retire it in favor of the enriched TDD for all but the simplest releases.
