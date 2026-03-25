# Technical Research Report: IronClaude PRD/TDD/Spec Pipeline
## Sections 6, 7, and 8 — Options Analysis, Recommendation, and Implementation Plan

**Report:** TASK-RESEARCH-20260324-001
**Date:** 2026-03-24
**Status:** Complete
**Synthesis file:** synth-03-option3-implementation-plan.md
**Evidence base:** Research files 01–06 + gaps-and-questions.md

---

## Section 5 — External Research Findings

**N/A — Codebase-scoped investigation.**

This investigation was scoped entirely to verification of existing source files in the IronClaude repository. No external competitive analysis, standards research, or industry benchmarking was required or performed. All research files (01–06) are code-tracer audits of specific pipeline components. No `web-NN` research files were produced during Phase 4.

If future work requires external research (e.g., evaluating alternative extraction pipeline architectures, reviewing industry standards for spec-to-task pipelines), that research should be added as a separate investigation and this section updated.

---

## Section 6 — Options Analysis

Three approaches for achieving TDD-to-pipeline compatibility are examined. All evidence references are to the research files in this task directory.

### Option 1: Status Quo (No Changes)

**Description:** Continue using `release-spec-template.md` manually to author specs. The TDD template exists as a standalone engineering artifact with no integration into sc:roadmap, sc:tasklist, or sc:spec-panel. All pipeline inputs continue to be hand-authored specs.

| Criterion | Assessment |
|-----------|------------|
| Effort | None |
| Risk | None — no changes, no regressions |
| Maintainability | Low — two parallel document families with no shared source of truth |
| Integration complexity | None |
| Reuse potential | High — nothing to break; pipeline remains stable |
| Data richness | Low — pipeline only sees what is manually written into the spec; TDD's §10 Component Inventory, §15 Testing Strategy, §19 Migration Plan, §14 Observability content are invisible to all pipeline tools |
| Single source of truth | No — TDD and spec are independently authored; drift between them is undetected and unenforceable |

**Pros:** No disruption, no migration risk, no implementation cost.

**Cons:** The TDD's rich structured content (component inventories, migration phases, observability specs, testing strategy, release criteria) produces no pipeline benefit. The five confirmed analysis-document errors (spec-panel cannot create specs; frontmatter fields are all ignored; quality_scores field bridges nothing) persist indefinitely. The `--spec` flag in sc:tasklist remains a declared-but-dead interface.

---

### Option 2: Create a Spec-Generator Step from TDD (sc:spec-panel reads TDD, outputs spec-template-formatted spec)

**Description:** Wire sc:spec-panel to accept a TDD as input and instruct it to output a `release-spec-template.md`-formatted spec scoped to a single release increment. The resulting spec feeds the existing sc:roadmap and sc:tasklist pipeline unchanged. TDD and spec remain separate documents.

| Criterion | Assessment |
|-----------|------------|
| Effort | Medium — sc:spec-panel command file must be edited; release-spec-template.md path must be added to Tool Coordination; TDD-detection logic must be added to Behavioral Flow |
| Risk | Medium — spec-panel output quality from a TDD input is untested; the spec-panel Boundaries constraint ("Generate specifications from scratch without existing content or context") creates an ambiguous interpretation edge: a TDD is "existing content" but it is not a spec |
| Maintainability | Low — two documents to maintain; spec is derived but not live; TDD changes require re-running spec generation manually |
| Integration complexity | Low — only one file modified; pipeline downstream unchanged |
| Reuse potential | High — existing pipeline tools are reused as-is |
| Data richness | Low-to-medium — derived spec will be shallower than the TDD; structured tables in §10, §14, §15, §19 are prose-converted rather than natively extracted |
| Single source of truth | No — spec is a derivative of TDD; two documents, one upstream; synchronization is a manual or repeated-invocation concern |

**Pros:** Minimal pipeline changes. Only one file (spec-panel command file) requires modification. Existing sc:roadmap and sc:tasklist tools are untouched.

**Cons:** sc:spec-panel's `Boundaries > Will Not` section explicitly states "Generate specifications from scratch without existing content or context." A TDD is not a spec; wiring this requires working around a hard constraint (file 01, Section 3.5). The derived spec will omit TDD-native structure that has no spec-template analog. The pipeline remains blind to TDD-rich data: sc:roadmap still cannot extract §10 Component Inventory, sc:tasklist still ignores migration phases, the 5-domain keyword gap persists. The `--spec` flag in sc:tasklist remains unimplemented. The gap confirmed in file 06 (Claim B1, B3, B4) — that frontmatter fields in the spec are ignored by the pipeline anyway — means the derived spec's frontmatter provides no incremental benefit without pipeline changes.

---

### Option 3: Modify TDD Template + Upgrade Pipeline Tools

**Description:** Add pipeline frontmatter to the TDD template to make TDDs self-describing to pipeline tools. Simultaneously upgrade sc:roadmap's extraction pipeline to natively consume TDD-specific sections (§7/§8/§10/§14/§15/§19). Upgrade sc:tasklist to implement the declared-but-dead `--spec` flag and consume TDD structured sections for richer task generation. Upgrade sc:spec-panel to accept TDD as input and produce scoped release specs. Fix the PRD→TDD handoff gaps in `tdd/SKILL.md`. All changes are backward-compatible with existing spec-template-based inputs.

| Criterion | Assessment |
|-----------|------------|
| Effort | High — 6 files modified across 4 tools; new extraction steps added; new scoring factors added; skill body sections added |
| Risk | Medium — bounded scope; each upgrade is additive (new steps, new flags, new conditionals); existing spec-template pipeline paths are unchanged; highest risk is sc:roadmap scoring formula rebalancing |
| Maintainability | High — TDD becomes the single upstream source; spec is generated from TDD or not needed; pipeline tools read richer content natively |
| Integration complexity | Medium — extraction pipeline, scoring formula, spec-panel behavioral flow, tasklist skill body, tdd skill synthesis mapping all require coordinated changes |
| Reuse potential | High — existing 8-step extraction pipeline extended, not replaced; `--spec` hook already declared in sc:tasklist argument-hint; `00-prd-extraction.md` slot and PRD-to-TDD Pipeline section already exist in tdd skill |
| Data richness | High — sc:roadmap extraction gains §10 Component Inventory, §19 Migration Phases, §24 Release Criteria, §14 Observability; sc:tasklist task generation driven by component inventory, migration phases, testing strategy, release criteria |
| Single source of truth | Yes — TDD serves as living document; sc:roadmap, sc:tasklist, and sc:spec-panel all consume it directly; PRD epics and ACs are formally traced into TDD FRs |

**Pros:** Single source of truth. Richer roadmaps: component inventory, migration phases, observability specs feed directly into roadmap milestones. Richer tasklists: one task per new component, migration-phase-ordered task buckets, verbatim validation commands from testing strategy, DoD items as final-phase verification tasks. TDD becomes a living document across releases. Implements the declared `--spec` interface already visible to users. PRD→TDD traceability is enforced at the QA gate level.

**Cons:** Significant scope — 4 tools require changes across 6 files. Requires thorough testing to verify the scoring formula weights still sum to 1.0 and the backward-compatible extraction path remains stable for spec-template inputs. Implementation must be phased to avoid breaking the existing pipeline mid-flight.

---

### Options Comparison Table

| Criterion | Option 1: Status Quo | Option 2: Spec-Generator Step | Option 3: TDD Template + Pipeline Upgrade |
|-----------|---------------------|-------------------------------|------------------------------------------|
| Effort | None | Medium (1 file) | High (6 files, 4 tools) |
| Risk | None | Medium — Boundaries workaround required | Medium — bounded, backward-compatible |
| Maintainability | Low — two orphaned document families | Low — spec is a manual re-derivation | High — single upstream source |
| Integration complexity | None | Low — pipeline unchanged | Medium — coordinated changes across 4 tools |
| Reuse potential | High — nothing changes | High — pipeline reused as-is | High — builds on existing hooks and slots |
| Data richness | Low — TDD content invisible to pipeline | Low-to-medium — derived spec shallower than TDD | High — structured TDD sections natively extracted |
| Single source of truth | No | No | Yes |

---

## Section 7 — Recommendation

**Recommendation: Option 3 — Modify TDD Template + Upgrade Pipeline Tools.**

### Rationale

**1. The comparison table shows Option 3 is the only path to data richness and a single source of truth.**

Option 1 and Option 2 both score Low on data richness and No on single source of truth. The TDD template contains highly structured content in §10 Component Inventory, §14 Observability, §15 Testing Strategy, §19 Migration & Rollout Plan, and §24 Release Criteria that has direct, one-to-one mappings to roadmap milestones and tasklist items. Options 1 and 2 leave this content permanently inaccessible to pipeline tools. Only Option 3 closes that gap.

**2. The `--spec` flag gap is the most actionable upgrade vector in the entire pipeline.**

Research file 03 (Section 1, Section 8 Q1) confirmed the `--spec <spec-path>` flag is declared in sc:tasklist's argument-hint but has zero body implementation. The interface contract already exists and is visible to users. Implementing it is not a new API decision — it is completing a stated intent. Option 3's Phase 4 work implements exactly this hook. Option 2 does not touch sc:tasklist at all, leaving the ghost interface in place.

**3. Option 2 requires working around a hard Boundaries constraint in sc:spec-panel.**

Research file 01 (Section 3.5) confirmed sc:spec-panel's `Boundaries > Will Not` section explicitly states: "Generate specifications from scratch without existing content or context." Wiring Option 2 requires either (a) reinterpreting "existing content" to include TDDs — a semantic stretch that future maintainers will find confusing — or (b) modifying the Boundaries section to carve out a TDD exception, which is effectively a partial implementation of Option 3's Phase 3 work anyway. Option 3 formalizes this capability cleanly rather than smuggling it in through a Boundaries workaround.

**4. All confirmed frontmatter field gaps make Option 2's pipeline outputs identical to Option 1's.**

Research file 06 (Claims B1, B3, B4 — all CODE-CONTRADICTED) confirmed that `spec_type`, `complexity_score`, `complexity_class`, and `quality_scores` in any input spec's frontmatter are ignored by sc:roadmap. The pipeline validates YAML syntax but extracts zero values from frontmatter. This means a derived spec produced by Option 2 would flow through the pipeline identically to a hand-authored spec: the frontmatter fields sc:roadmap would need to "get the metadata it needs" are ignored unless the pipeline is upgraded to read them. Option 2's sole advantage — providing a structured spec as pipeline input — is neutralized by this confirmed gap. Option 3 addresses the gap at the source: it upgrades the pipeline to actually read those fields.

**5. Option 3's scope is bounded and the extension points already exist.**

Research file 06 (Option 3 Feasibility Assessment) confirmed:
- The TDD template already contains all the rich content sections Option 3 proposes to extract (file 04 confirms §7, §8, §9, §10, §14, §15, §19, §24, §25 are fully structured)
- The `--spec` hook is already declared in sc:tasklist
- The `00-prd-extraction.md` artifact slot and PRD-to-TDD Pipeline section already exist in tdd/SKILL.md
- The 8-step extraction pipeline's gaps are precisely documented (file 02, TDD Section Capture Analysis)

The incremental cost of Option 3's additional scope (Steps 9-14 extraction, scoring formula rebalancing, spec-panel TDD mode, tasklist body implementation) is low once the foundational principle — "pipeline tools should consume TDD natively" — is accepted. Option 2 would require the same foundational work (getting pipeline tools to read TDD content) without delivering the full benefit.

### Recommendation Summary

| Factor | Decision |
|--------|----------|
| Implement Option | 3 |
| Phase order | Template frontmatter → sc:roadmap extraction → sc:roadmap scoring → sc:spec-panel → sc:tasklist → PRD→TDD handoff |
| Backward compatibility required | Yes — all changes additive or conditional on TDD-format detection |
| Breaking change | None — existing spec-template pipeline paths unchanged |
| Risk mitigation | Implement and test each phase independently; verify scoring weights sum to 1.0 before landing Phase 2 |

---

## Section 8 — Implementation Plan

This section is the primary deliverable. All file paths are absolute. All field names, section references, and instruction text are exact. A developer may begin implementation from this section alone without consulting other documents.

---

### Phase 1: TDD Template Frontmatter Additions

**Primary file:** `/Users/cmerritt/GFxAI/IronClaude/src/superclaude/examples/tdd_template.md`
**Secondary sync target:** `.claude/skills/tdd/` templates directory (run `make sync-dev` after editing source)

**What to do:** Add 8 fields to the existing YAML frontmatter block. The current frontmatter ends with the `approvers` block. Insert these fields after the `parent_doc` field and before `depends_on`. All new fields use the same placeholder style as the existing TDD template fields.

**Exact fields to add:**

```yaml
feature_id: "[FEATURE-ID]"
spec_type: "new_feature"  # new_feature | refactoring | migration | infrastructure | security | performance | docs
complexity_score: ""      # 0.0–1.0 — computed by sc:roadmap; provide estimated value if known
complexity_class: ""      # LOW | MEDIUM | HIGH — computed by sc:roadmap; provide estimated value if known
target_release: "[version]"
authors: ["[author1]", "[author2]"]
quality_scores:
  clarity: ""
  completeness: ""
  testability: ""
  consistency: ""
  overall: ""
```

**Note on `spec_type` enum:** The release-spec-template.md uses `new_feature | refactoring | portification | infrastructure`. The TDD template addition expands this to include `migration | security | performance | docs` to cover TDD use cases not covered by the spec template enum. When a TDD with `spec_type: migration` is passed to sc:roadmap, it should map to the `migration` template type. This mapping must be implemented in Phase 2 (scoring.md TDD-format detection rule).

**Sentinel self-check addition:** After the YAML block in the TDD template's usage preamble section (the section that describes how to fill in the template), add:

```
**Sentinel self-check (run before submitting TDD for pipeline consumption):**
Verify all pipeline fields are populated:
- feature_id must not be "[FEATURE-ID]"
- spec_type must be one of: new_feature | refactoring | migration | infrastructure | security | performance | docs
- target_release must not be "[version]"
- complexity_score and complexity_class may remain empty (computed by sc:roadmap)

**Quality gate (run sc:spec-panel on this TDD before pipeline submission):**
/sc:spec-panel @<this-tdd-file> --focus correctness,architecture --mode critique
```

**After editing source:** Run `make sync-dev` to propagate to `.claude/skills/tdd/`.

**Evidence base:** File 04, Section 1.1 "Notable absences vs. pipeline-oriented fields"; File 04, Section 2.1 YAML fields from release-spec-template.md.

---

### Phase 2: sc:roadmap Extraction Pipeline Upgrades

**Phase 2 has two independent sub-steps. Both are in the sc-roadmap-protocol skill package.**

#### Phase 2, Step 1: Extend Domain Keyword Dictionaries

**File:** `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`
**Section to edit:** Step 4 "Scope & Domain Classification" — the keyword dictionaries subsection.

The current five domains are: Frontend, Backend, Security, Performance, Documentation. Two new domains must be added. Insert these after the Documentation domain entry.

**Testing domain — add as a new domain entry:**
```
Testing domain keywords: "unit test, integration test, e2e test, coverage, test suite, test plan, assertion, mock, fixture, spec file, test case, test strategy, test pyramid, qa gate, acceptance test, smoke test, regression test"
```

**DevOps/Ops/Observability domain — add as a new domain entry:**
```
DevOps/Ops domain keywords: "runbook, on-call, monitoring, alerting, dashboard, metric, SLO, SLA, deployment, rollout, rollback, feature flag, canary, blue-green, observability, tracing, log level, capacity planning, incident, escalation"
```

**Why this is required:** Research file 02 (Section 2, Domain Keyword Gap; Section 6 Key Takeaway 5) confirmed the 5-domain classifier has no Testing or DevOps/Ops domain. TDD sections §14 Observability, §15 Testing Strategy, and §25 Operational Readiness systematically score 0 against all 5 domains and are classified as OTHER or miscategorized as Backend. Adding these domains ensures TDD-heavy specifications produce accurate complexity scores and domain distributions rather than systematically undercounting the scope.

**Also update domain count normalization in scoring.md** (see Phase 2 Step 2): the `domain_spread` factor currently normalizes against 5 domains (`min(domains / 5, 1.0)`). With 7 domains, update to `min(domains / 7, 1.0)` to maintain the normalization ceiling.

#### Phase 2, Step 2: Add TDD-Specific Extraction Steps (Steps 9–14) and Scoring Formula Update

**File A:** `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`
**Section to edit:** After Step 8 "ID Assignment", add the following new steps. These steps are only executed when TDD-format input is detected (detection rule: input document contains `## 10. Component Inventory` heading OR contains YAML frontmatter with `type: "📐 Technical Design Document"` OR has 20+ of the TDD section headings from the 28-section inventory).

**Step 9: Component Inventory Extraction**
```
Step 9: Component Inventory Extraction
- Trigger: TDD-format input detected
- Scan for heading matching "## 10. Component Inventory" or "## Component Inventory"
- Within that section, identify the three sub-tables: new components, modified components, deleted components
- For each row in the new components table: extract component name and purpose
- For each row in the modified components table: extract component name and change description
- For each row in the deleted components table: extract component name and migration target
- Store as component_inventory: { new: [...], modified: [...], deleted: [...] }
- If section is absent or empty: store component_inventory: null
```

**Step 10: Migration Phase Extraction**
```
Step 10: Migration Phase Extraction
- Trigger: TDD-format input detected
- Scan for heading matching "## 19. Migration & Rollout Plan" or "## Migration & Rollout Plan"
- Within 19.3 "Rollout Stages" or equivalent sub-section, extract each row of the rollout stage table: stage name, target environment, criteria, rollback trigger
- Within 19.4 "Rollback Procedure" or equivalent, extract ordered rollback steps as a list
- Store as migration_phases: { stages: [...], rollback_steps: [...] }
- If section is absent or empty: store migration_phases: null
```

**Step 11: Release Criteria Extraction**
```
Step 11: Release Criteria Extraction
- Trigger: TDD-format input detected
- Scan for heading matching "## 24. Release Criteria" or "## Release Criteria"
- Within 24.1 "Definition of Done": extract each checklist item as a string
- Within 24.2 "Release Checklist": extract each checklist item as a string
- Store as release_criteria: { definition_of_done: [...], release_checklist: [...] }
- Note: §24 Release Criteria is also captured by Step 6 (Success Criteria) for FRs/NFRs; Steps 6 and 11 both run independently
- If section is absent or empty: store release_criteria: null
```

**Step 12: Observability Extraction**
```
Step 12: Observability Extraction
- Trigger: TDD-format input detected
- Scan for heading matching "## 14. Observability & Monitoring" or "## Observability & Monitoring"
- Within 14.2 "Metrics": extract each row of the metrics table (metric name, description, type, labels, target)
- Within 14.4 "Alerts": extract each row of the alert table (alert name, condition, severity, action)
- Within 14.5 "Dashboards": extract dashboard names and links
- Store as observability: { metrics: [...], alerts: [...], dashboards: [...] }
- If section is absent or empty: store observability: null
```

**Step 13: Testing Strategy Extraction**
```
Step 13: Testing Strategy Extraction
- Trigger: TDD-format input detected
- Scan for heading matching "## 15. Testing Strategy" or "## Testing Strategy"
- Within 15.1 "Test Pyramid": extract each row (level, coverage_target, tools)
- Within 15.2 "Test Cases": extract the unit test cases table (test name, what it tests, acceptance criteria), integration test cases table, and E2E test cases table as separate lists
- Within 15.3 "Test Environments": extract each environment row (environment name, purpose, access)
- Store as testing_strategy: { test_pyramid: [...], unit_tests: [...], integration_tests: [...], e2e_tests: [...], environments: [...] }
- If section is absent or empty: store testing_strategy: null
```

**Step 14: API Surface Extraction**
```
Step 14: API Surface Extraction
- Trigger: TDD-format input detected
- Scan for heading matching "## 8. API Specifications" or "## API Specifications"
- Within 8.2 "Endpoint Details": count the total number of endpoint rows across all endpoint tables
- Store as api_surface: { endpoint_count: N }
- If section is absent or empty: store api_surface: { endpoint_count: 0 }
```

**File B:** `.claude/skills/sc-roadmap-protocol/refs/scoring.md`

**TDD-format detection rule — add at the top of the scoring section:**
```
TDD-format detection: Input spec is classified as TDD-format if it contains YAML frontmatter with `type` field containing "Technical Design Document", OR if the document body contains 20 or more section headings matching the TDD section numbering pattern (## N. Heading).

When TDD-format is detected: use the TDD scoring formula below.
When TDD-format is not detected: use the standard 5-factor formula (unchanged).
```

**Updated complexity scoring formula for TDD-format input:**

Replace the current 5-factor formula with the following 7-factor formula when TDD-format is detected:

```
complexity_score = (requirement_count_norm * 0.20)
                 + (dependency_depth_norm  * 0.20)
                 + (domain_spread_norm     * 0.15)
                 + (risk_severity_norm     * 0.10)
                 + (scope_size_norm        * 0.15)
                 + (api_surface_norm       * 0.10)
                 + (data_model_complexity_norm * 0.10)
```

Weight table:

| Factor | Raw Value Source | Normalization | Weight |
|--------|-----------------|---------------|--------|
| `requirement_count` | Total FRs + NFRs from extraction | `min(count / 50, 1.0)` | 0.20 |
| `dependency_depth` | Max chain in dependency graph | `min(depth / 8, 1.0)` | 0.20 |
| `domain_spread` | Distinct domains with ≥10% representation (out of 7) | `min(domains / 7, 1.0)` | 0.15 |
| `risk_severity` | `(high*3 + medium*2 + low*1) / total_risks` | `(weighted_avg - 1.0) / 2.0` | 0.10 |
| `scope_size` | Total line count of specification | `min(lines / 1000, 1.0)` | 0.15 |
| `api_surface` | Endpoint count from Step 14 | `min(count / 30, 1.0)` | 0.10 |
| `data_model_complexity` | Entity count + relationship count from §7 Data Entities table | `min(count / 20, 1.0)` | 0.10 |

**Weights sum verification:** 0.20 + 0.20 + 0.15 + 0.10 + 0.15 + 0.10 + 0.10 = 1.00 ✓

**Standard formula (non-TDD input) — unchanged:**
The original 5-factor formula with weights 0.25/0.25/0.20/0.15/0.15 remains in effect for all non-TDD inputs. The `domain_spread` normalization denominator in the standard formula stays at 5.

**Evidence base:** File 02, Section 3 (scoring.md findings); File 02, Section 6 Key Takeaway 5 (5-domain blind spot); File 06, Option 3 Feasibility "What the research reveals as complications" item 2.

---

### Phase 3: sc:spec-panel Additions

**File:** `.claude/commands/sc/spec-panel.md`

This file is a standalone 624-line command file with no companion skill directory. All additions are insertions into the existing markdown sections.

#### Addition 1: Behavioral Flow — Steps 6a and 6b (insert after existing Step 6 "Improve")

Locate the "Behavioral Flow" section. After the existing Step 6 text, insert:

```markdown
**Step 6a (conditional — TDD input detected):** If the input document is a TDD (detected by presence of `type: "📐 Technical Design Document"` in YAML frontmatter OR 20+ TDD section headings), scope the improved output to a single release increment using `target_release` from TDD frontmatter. If `target_release` is empty or absent, ask the user to specify the target release before proceeding.

**Step 6b (conditional — output intended for sc:roadmap):** If the user's intent is to feed the output into sc:roadmap (indicated by user instruction or by `--downstream roadmap` flag), ensure the output document contains the following frontmatter fields populated from the TDD frontmatter or computed from TDD content analysis:
- `spec_type`: copy from TDD `spec_type` field; if absent, infer from TDD section content
- `complexity_score`: copy from TDD `complexity_score` if populated; else leave as `{{SC_PLACEHOLDER:0.0_to_1.0}}`
- `complexity_class`: copy from TDD `complexity_class` if populated; else leave as `{{SC_PLACEHOLDER:LOW_or_MEDIUM_or_HIGH}}`
- `target_release`: copy from TDD `target_release`
- `feature_id`: copy from TDD `feature_id`
```

#### Addition 2: Output Section (insert after existing Output block)

```markdown
**Output — when input is a TDD:**
The panel may produce either of two output types depending on user intent:

(a) **Review document** (default): A structured review document in the standard `--format standard | structured | detailed` mode. Expert analysis covers TDD sections §5 Technical Requirements, §6 Architecture, §7 Data Models, §8 API Specifications, §13 Security Considerations, §15 Testing Strategy, and §20 Risks & Mitigations. Expert panel applies the same 11-expert review sequence as for specs. Correctness-focus mandatory artifacts (State Variable Registry, Guard Condition Boundary Table) apply.

(b) **Scoped release spec** (when `--downstream roadmap` or when user requests): A document in `release-spec-template.md` format covering the sections relevant to `target_release` from the TDD frontmatter. The scoped spec extracts FRs from TDD §5.1, NFRs from TDD §5.2, architecture decisions from TDD §6.4, risks from TDD §20, test plan from TDD §15, migration plan from TDD §19. YAML frontmatter is populated from TDD frontmatter fields.

Note: spec-panel does not CREATE a spec from raw instructions (Boundaries constraint unchanged). The TDD→spec capability requires an existing, substantially populated TDD as input. Passing a skeletal or incomplete TDD will produce a review document only.
```

#### Addition 3: Tool Coordination Section (insert into existing "Read" tools list)

In the Tool Coordination section, under the "Read" tool entry, add:

```markdown
- `src/superclaude/examples/release-spec-template.md` — read when generating scoped release spec output from TDD input (Step 6b / `--downstream roadmap` mode) to ensure output conforms to the expected spec format
```

**Evidence base:** File 01, Sections 3.5 ("Will Not" boundary), 3.6 (Improve step output), 3.7 (downstream wiring); File 06, Corrections List item 1 and item 5.

---

### Phase 4: sc:tasklist Additions

**File:** `.claude/skills/sc-tasklist-protocol/SKILL.md`

This is the primary deliverable of Phase 4. The `--spec` flag is currently declared in the frontmatter argument-hint at line 9 but has zero body implementation. This phase writes the body implementation.

#### Addition 1: Section 4.1 (Parse Roadmap Items) — supplementary context loading

Locate Step 4.1 in the SKILL.md body. After the existing Step 4.1 text (which describes parsing headings and bullets into R-### roadmap items), add the following block:

```markdown
**Step 4.1a — Supplementary TDD Context (conditional on `--spec` flag):**

If `--spec <spec-path>` was provided:
1. Read the file at `<spec-path>`.
2. Detect if the file is TDD-format (YAML frontmatter `type` contains "Technical Design Document" OR 20+ section headings matching TDD numbering pattern).
3. If TDD-format: extract the following content and store as `supplementary_context`:
   - **component_inventory**: scan for `## 10. Component Inventory`; extract new/modified/deleted component tables. Store as `{ new: [{name, purpose}], modified: [{name, change}], deleted: [{name, migration_target}] }`
   - **migration_phases**: scan for `## 19. Migration & Rollout Plan`; extract rollout stage table from §19.3 as ordered list `[{stage, environment, criteria, rollback_trigger}]`
   - **testing_strategy**: scan for `## 15. Testing Strategy`; extract test pyramid table from §15.1 as `[{level, coverage_target, tools}]`; extract unit/integration/E2E test case tables as separate lists
   - **observability**: scan for `## 14. Observability & Monitoring`; extract metrics table from §14.2 as `[{name, description, type, target}]`; extract alerts table from §14.4 as `[{name, condition, severity}]`
   - **release_criteria**: scan for `## 24. Release Criteria`; extract §24.1 Definition of Done checklist items as `[string]`
4. If spec-path file is not TDD-format: log a warning "Spec file does not appear to be TDD-format; --spec enrichment will not be applied." Continue with roadmap-only generation.
5. If spec-path file does not exist: abort with error "Cannot read spec file at <spec-path>."
```

#### Addition 2: Section 4.4 (Convert Roadmap Items into Tasks) — supplementary context task generation

Locate Step 4.4 in the SKILL.md body. After the existing Step 4.4 text (which defines the 1-task-per-roadmap-item default and compound split rules), add:

```markdown
**Step 4.4a — Supplementary Task Generation from TDD Sections (conditional on `supplementary_context`):**

These rules run after the standard Step 4.4 task generation. Each rule generates additional tasks that are appended to the appropriate phase bucket. If a generated task duplicates a task already generated from the roadmap (same component or same test suite name), merge rather than duplicate.

**If `supplementary_context.component_inventory` exists and is non-null:**
- For each entry in `component_inventory.new`: generate one task with title `Implement [component_name]` and Tier STANDARD (override to STRICT if component name matches keywords: auth, security, crypto, database, migration, schema, model). Deliverable: the new component file/module. Acceptance Criteria bullet 1: "[component_name] is importable and passes its unit tests."
- For each entry in `component_inventory.modified`: generate one task with title `Update [component_name]: [change_description]` (truncate change_description to 40 chars). Tier STANDARD or STRICT per keyword rule above. Acceptance Criteria bullet 1: "[component_name] tests pass with no regressions."
- For each entry in `component_inventory.deleted`: if `migration_target` is non-empty, generate one task `Migrate [component_name] to [migration_target]` with Tier STRICT. If migration_target is empty, generate task `Remove [component_name]` with Tier STANDARD.
- Assign all component-inventory-derived tasks to Phase 1 (Foundation) unless migration_phases context exists (see below).

**If `supplementary_context.migration_phases` exists and is non-null:**
- Re-bucket all tasks using migration phase order as the phase structure instead of the roadmap's heading-based phase buckets. Each `stage` in `migration_phases.stages` becomes one phase bucket. Existing tasks are distributed into the nearest-matching migration phase by keyword proximity.
- Add the `rollback_steps` list as a `Rollback:` field on every migration-phase task (replacing the default "TBD").

**If `supplementary_context.testing_strategy` exists and is non-null:**
- For each row in `testing_strategy.test_pyramid`: generate one task `Write [level] test suite ([tools])` where level is the test pyramid level (unit/integration/E2E) and tools is the tools value. Tier STANDARD.
  - Acceptance Criteria bullet 1: "All [level] tests pass with coverage ≥ [coverage_target]."
  - Validation bullet 1: the verbatim test run command from the tools value if it contains a runnable command (e.g., `uv run pytest`); otherwise `Manual check: run [level] test suite and verify coverage ≥ [coverage_target]`.
- Assign testing tasks to the same phase as the feature tasks they test (last task in the feature's phase).

**If `supplementary_context.observability` exists and is non-null:**
- For each entry in `observability.metrics`: generate one task `Instrument metric: [name]`. Tier STANDARD. Deliverable: metric emitted at the defined measurement point. Acceptance Criteria bullet 1: "[name] metric is queryable in the observability dashboard."
- For each entry in `observability.alerts`: generate one task `Configure alert: [name]`. Tier STANDARD. Deliverable: alert rule deployed. Acceptance Criteria bullet 1: "Alert [name] fires on test condition [condition]."
- Assign observability tasks to the last phase (monitoring/stabilization phase).

**If `supplementary_context.release_criteria` exists and is non-null:**
- For each item in `release_criteria.definition_of_done`: generate one EXEMPT (review) task `Verify DoD: [item_text truncated to 60 chars]` at the end of the final phase.
  - Acceptance Criteria bullet 1: "[item_text] is confirmed complete."
  - Verification Method: Manual review.
- These tasks form the final phase's exit verification block.
```

**Note:** This phase implements the `--spec` flag that research file 03 (Section 1, Gaps item 1) confirmed is "declared but dead." The argument-hint signature `<roadmap-path> [--spec <spec-path>] [--output <output-dir>]` remains unchanged. Only the body implementation is added.

**Evidence base:** File 03, Section 1 (`--spec` flag gap), Section 8 Q1, Section 8 "How Could sc:tasklist Generate Tasks from These Sections if Upgraded?"; File 02, TDD Section Capture Analysis.

#### Phase 4 Addition: sc:tasklist validation scope

**File:** `.claude/skills/sc-tasklist-protocol/SKILL.md`
**Section to edit:** `## Post-Generation Roadmap Validation (Stages 7-10, Mandatory)` — specifically the `### Stage 7: Roadmap Validation (2N Parallel Agents)` subsection, which currently instructs validation agents to compare generated tasks against the source roadmap only. Insert the following block after the existing Stage 7 purpose/mechanism text, immediately before the Stage gate line.

**What to add:**

```markdown
**Supplementary spec validation (conditional on `--spec` flag):**

When `--spec <spec-path>` was provided and `supplementary_context` was loaded in Step 4.1a, each Stage 7 validation agent must additionally check the generated tasklist against the supplementary_context content. Specifically, each agent must verify:

1. **component_inventory coverage**: Every entry in `supplementary_context.component_inventory.new` has a corresponding task in the generated tasklist (title contains the component name or the component is referenced in a task's Deliverable or Acceptance Criteria). Flag as HIGH finding: "Missing task for new component [name] from TDD §10."
2. **migration_phases coverage**: If `supplementary_context.migration_phases` is non-null, verify that migration phase stage names from `migration_phases.stages` are reflected in the generated phase bucket names or task titles. Flag as MEDIUM finding: "Migration stage [name] from TDD §19 has no corresponding task bucket or task."
3. **testing_strategy coverage**: If `supplementary_context.testing_strategy` is non-null, verify that each test pyramid level in `testing_strategy.test_pyramid` has at least one generated task covering that level. Flag as MEDIUM finding: "No [level] test task generated despite TDD §15 test pyramid entry."
4. **release_criteria coverage**: If `supplementary_context.release_criteria` is non-null, verify that each item in `release_criteria.definition_of_done` appears as a DoD verification task or in the Acceptance Criteria of the final phase's tasks. Flag as LOW finding: "DoD item '[item_text]' from TDD §24 has no coverage in final phase."

These findings are merged into the same consolidated findings list used by Stage 8 (Patch Plan Generation). The validation scope expansion applies only when `--spec` was provided; the standard roadmap-only validation is unchanged for invocations without `--spec`.
```

**Why this is required:** Research file 03 (Section 9, gaps file [03] item 6) confirmed that Stages 7–10 validate only against the source roadmap; content derived from TDD sections not present in the roadmap would be incorrectly flagged as "invented content" drift. Without this addition, TDD-enriched tasklists cannot pass validation even when they are correct. This closes the gap listed in synth-02 Section 4.3 (High severity, third row).

**Evidence base:** File 03, Section 9; gaps-and-questions.md item [03] item 6.

---

### Phase 5: PRD→TDD Handoff Improvements

**File:** `.claude/skills/tdd/SKILL.md`

Research file 05 (Sections 3.1–3.3) and file 06 (Claim E3) confirmed five gaps in the PRD→TDD handoff. This phase addresses the three highest-priority gaps.

#### Addition 1: PRD Extraction Agent Prompt (insert after existing agent prompt templates)

Locate the `## Agent Prompt Templates` section in SKILL.md (begins at approximately line 525). This section contains the following sub-headings in order: `### Codebase Research Agent Prompt` (~line 529), `### Web Research Agent Prompt` (~line 616), `### Synthesis Agent Prompt` (~line 666), `### Research Analyst Agent Prompt` (~line 701), `### Research QA Agent Prompt` (~line 740), `### Synthesis QA Agent Prompt` (~line 784), `### Report Validation QA Agent Prompt` (~line 826), and `### Assembly Agent Prompt (rf-assembler — TDD Assembly)` (~lines 873–940). After the closing ` ``` ` of the Assembly Agent Prompt block (the last agent prompt template in the section), insert:

```markdown
### PRD Extraction Agent Prompt

This prompt is used for the `00-prd-extraction.md` step (Phase 2, first research item when PRD_REF is provided). The agent reading this prompt should be spawned as a read-only research agent.

---
**PRD Extraction Agent — System Prompt**

You are extracting structured content from a Product Requirements Document to serve as foundational context for a Technical Design Document.

Read the PRD file at: `{{PRD_REF}}`

Extract and write to `${TASK_DIR}research/00-prd-extraction.md` the following sections, each as a clearly labeled markdown section:

**Section 1: Epics**
For each epic in PRD Section 21.1: extract the epic ID, epic title, and 1-sentence description. Format as a table: Epic ID | Title | Description.

**Section 2: User Stories and Acceptance Criteria**
For each user story in PRD Section 21.1: extract the story text (As a / I want / So that format), all acceptance criteria bullets, and the parent epic ID. Format as: `[EPIC-ID] — [story text]` followed by bulleted ACs.

**Section 3: Success Metrics**
From PRD Section 4 (Product Vision) and Section 19 (Success Metrics & Measurement): extract each metric name, baseline value, target value, and measurement method. Format as a table: Metric | Baseline | Target | Measurement Method.

**Section 4: Technical Requirements**
From PRD Section 14 (Technical Requirements): extract all architecture constraints, performance requirements, security requirements, scalability requirements, and data/analytics requirements as a flat list with requirement type labels.

**Section 5: Scope Boundaries**
From PRD Section 12 (Scope Definition): extract the in-scope items as a bulleted list and the out-of-scope items as a separate bulleted list.

Write nothing else. Tag each extracted fact as [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] based on whether you confirmed it against codebase content, found it contradicted by codebase content, or could not verify it against code.
---
```

#### Addition 2: Synthesis Mapping Table Update

Locate the Synthesis Mapping Table in SKILL.md. This table maps synthesis files to their source documents. Update the table to add `00-prd-extraction.md` as a source for synthesis files synth-03 through synth-07.

For each of the following synthesis files, add `00-prd-extraction.md` to the Sources column:
- `synth-03-competitive-scope.md` — add source: `00-prd-extraction.md (Section 5: Scope Boundaries)`
- `synth-04-stories-requirements.md` — add source: `00-prd-extraction.md (Section 1: Epics, Section 2: User Stories)`
- `synth-05-technical-stack.md` — add source: `00-prd-extraction.md (Section 4: Technical Requirements)`
- `synth-06-ux-legal-business.md` — add source: `00-prd-extraction.md (Section 3: Success Metrics)`
- `synth-07-metrics-risk-impl.md` — add source: `00-prd-extraction.md (Section 3: Success Metrics, Section 2: ACs)`

Note: `synth-01`, `synth-02`, `synth-08`, and `synth-09` do not require PRD extraction as a source — they cover executive summary, business context, customer journey, and maintenance sections that have no direct TDD FR mapping.

#### Addition 3: Synthesis Agent Prompt Rules (append to existing rules list)

Locate the Synthesis Agent Prompt rules section in SKILL.md. At the end of the existing rules list, append:

```markdown
Rule 12: "Every FR in TDD Section 5.1 must trace back to a PRD epic or user story. Cite the epic ID in the FR row's 'Source' column. If no PRD epic can be identified for an FR, mark it '[NO PRD TRACE]' and flag it as a gap."

Rule 13: "TDD Section 4.2 (Business Metrics, if included) must include at least one engineering proxy metric for each business KPI listed in the PRD's Section 4 and Section 19. Format as: Business KPI: [PRD KPI name] — Engineering Proxy: [measurable technical metric]."
```

#### Addition 4: Synthesis QA Gate Checklist (append to existing checklist)

Locate the Synthesis QA Gate checklist in SKILL.md. At the end of the existing checklist items, append:

```markdown
Item 13: "FR traceability — spot-check 3 FRs in the synth-04 output: each must cite a PRD epic ID in its Source column. If any FR lacks a PRD epic citation and is not marked '[NO PRD TRACE]', flag as FAIL."
```

**Evidence base:** File 05, Section 2.2 (output file paths), Section 2.6 (PRD extraction instruction), Section 3.1–3.3 (gaps); File 06, Claim E3 (partial wiring confirmed); gaps-and-questions.md items on PRD traceability enforcement.

---

### Integration Checklist

Run these verification steps after all phases are implemented. Each item is a pass/fail gate for that phase.

**Phase 1 — TDD Template:**
- [ ] `grep -c 'feature_id' src/superclaude/examples/tdd_template.md` returns 1
- [ ] `grep -c 'spec_type' src/superclaude/examples/tdd_template.md` returns 1
- [ ] `grep -c 'quality_scores' src/superclaude/examples/tdd_template.md` returns 1
- [ ] `make verify-sync` passes (src/ and .claude/ in sync)

**Phase 2 — sc:roadmap extraction and scoring:**
- [ ] Passing a TDD with a populated `## 10. Component Inventory` section to sc:roadmap produces a roadmap that includes component work items in at least one milestone
- [ ] The TDD scoring formula weights sum to 1.0: `0.20 + 0.20 + 0.15 + 0.10 + 0.15 + 0.10 + 0.10 = 1.00`
- [ ] Passing a standard `release-spec-template.md`-format spec produces identical roadmap output to pre-Phase-2 behavior (backward compatibility check)
- [ ] The extraction-pipeline.md now lists 7 domains (Frontend, Backend, Security, Performance, Documentation, Testing, DevOps/Ops)

**Phase 3 — sc:spec-panel:**
- [ ] Passing a TDD with `target_release` populated produces a scoped release spec with that release version in the spec YAML frontmatter
- [ ] `grep -c 'release-spec-template.md' .claude/commands/sc/spec-panel.md` returns 1 (Tool Coordination updated)
- [ ] Passing raw text instructions with no existing spec content still results in refusal (Boundaries constraint intact)

**Phase 4 — sc:tasklist:**
- [ ] Passing `sc:tasklist <roadmap> --spec <tdd-path>` where the TDD has a populated §10 Component Inventory generates tasks derived from the component inventory (one task per new component)
- [ ] The SKILL.md body now contains an implementation block for `--spec` flag processing (not just the frontmatter argument-hint declaration)
- [ ] Passing `sc:tasklist <roadmap>` with no `--spec` flag produces identical output to pre-Phase-4 behavior (backward compatibility check)

**Phase 5 — tdd skill PRD handoff:**
- [ ] The tdd/SKILL.md Synthesis Mapping Table now lists `00-prd-extraction.md` as a source for synth-03, synth-04, synth-05, synth-06, and synth-07
- [ ] The tdd/SKILL.md Synthesis QA Gate checklist now contains an Item 13 for FR traceability
- [ ] The tdd/SKILL.md contains a named "PRD Extraction Agent Prompt" section with the extraction instructions

---

**Status: Complete**
