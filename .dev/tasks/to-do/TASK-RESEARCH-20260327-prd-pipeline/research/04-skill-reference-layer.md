# 04 — Skill & Reference Layer: PRD-Aware Updates

**Status:** Complete
**Investigator:** Doc Analyst
**Date:** 2026-03-27
**Files Investigated:**
- `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` (441 lines)
- `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` (196 lines)
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (599+ lines)
- `src/superclaude/commands/spec-panel.md` (638 lines)

**Cross-validation sources:**
- `src/superclaude/cli/roadmap/executor.py` (detection logic)
- `src/superclaude/cli/roadmap/prompts.py` (TDD extraction prompt)
- `src/superclaude/cli/roadmap/commands.py` (CLI flags)
- `src/superclaude/cli/roadmap/models.py` (data models)
- `src/superclaude/cli/tasklist/commands.py` (tasklist CLI flags)
- `src/superclaude/cli/tasklist/prompts.py` (validation prompts)
- `src/superclaude/cli/tasklist/models.py` (tasklist models)

---

## 1. extraction-pipeline.md — Current TDD Structure & PRD Proposal

### 1.1 Current TDD-Conditional Content (Lines 143-207)

**Section: "TDD-Specific Extraction Steps (Steps 9-15)"**

Structure:
- **Conditional gate** (L145): Three-part detection rule — `## 10. Component Inventory` heading OR YAML frontmatter `type` containing "Technical Design Document" OR 20+ `## N. Heading` sections. [CODE-VERIFIED: `executor.py` L60-117 implements equivalent heuristic-based detection with a scoring system rather than exact boolean OR. The code uses a weighted score threshold (>=5) with signals for heading count, exclusive frontmatter fields (`parent_doc`, `coordinator`), and TDD-specific section names. The doc's three-rule detection is a simplified description of the actual code behavior.]
- **Skip rule**: When NOT detected, Steps 9-15 are skipped entirely. [CODE-VERIFIED: `executor.py` L884-892 routes TDD vs spec extraction to different prompt builders.]
- **Null default**: Each step stores `null` for its storage key if corresponding TDD section is absent.

Seven extraction steps (9-15):
| Step | Storage Key | TDD Section Source |
|------|-----------|-------------------|
| 9 | `component_inventory` | `## 10. Component Inventory` |
| 10 | `migration_phases` | §19.3 rollout stages, §19.4 rollback |
| 11 | `release_criteria` | §24.1 DoD checklist, §24.2 release checklist |
| 12 | `observability` | §14.2 metrics, §14.4 alerts, §14.5 dashboards |
| 13 | `testing_strategy` | §15.1 test pyramid, §15.2 test cases, §15.3 environments |
| 14 | `api_surface` | §8.1 API Overview endpoint count |
| 15 | `data_model_complexity` | §7.1 entity count + relationship count |

### 1.2 Proposed PRD-Specific Extraction Steps (Steps 16-22)

**Gate structure (mirroring TDD pattern):**

PRD-format detection: Input spec is classified as PRD-format if it contains a heading matching `## Product Overview` OR `## User Personas` OR YAML frontmatter with `type` field containing "Product Requirements Document" OR the document body contains sections named "Market Analysis", "User Stories", "Success Metrics", and "Go-to-Market".

When PRD-format is NOT detected, Steps 16-22 are skipped entirely.

Proposed extraction steps:

| Step | Storage Key | PRD Section Source | Rationale |
|------|-----------|-------------------|-----------|
| 16 | `user_personas` | User Personas / Target Audience section | Maps personas to requirement priorities for roadmap weighting |
| 17 | `user_stories` | User Stories / Use Cases section | Supplements FR extraction with actor-goal-outcome triples |
| 18 | `success_metrics` | Success Metrics / KPIs section | Enriches success criteria with business-level OKRs |
| 19 | `market_constraints` | Market Analysis / Competitive Landscape section | Informs risk identification with market-driven urgency |
| 20 | `release_strategy` | Go-to-Market / Release Strategy section | Provides phasing guidance for roadmap milestone planning |
| 21 | `stakeholder_priorities` | Stakeholder Requirements / Priority Matrix section | Maps stakeholder weighting to P0-P3 priority assignments |
| 22 | `acceptance_scenarios` | Acceptance Criteria / Validation Scenarios section | Enriches success criteria with concrete scenario-based validation |

**Key design question:** PRDs are less structurally standardized than TDDs (which follow a numbered 28-section template). The PRD template in `src/superclaude/skills/prd/SKILL.md` would need to be the canonical section reference, similar to how TDD extraction references specific `## N.` sections. [UNVERIFIED: The PRD template file was not read during this investigation; its actual section structure needs confirmation.]

### 1.3 Detection Rule Code Impact

**CORRECTION (QA fix-cycle 1):** Per the research-notes.md design decision (lines 90-97), PRD is a **supplementary input only**, NOT a new input mode. The `detect_input_type()` function in `executor.py` (L57-117) does NOT need changes. No `--input-type prd` mode, no `build_extract_prompt_prd()`, no detection signals. PRD content is injected via `--prd-file` flag as conditional prompt enrichment blocks, mirroring the tasklist `--tdd-file` pattern.

[CODE-VERIFIED: `models.py` L114 defines `input_type: Literal["auto", "tdd", "spec"]` — this remains unchanged for PRD integration.]

---

## 2. scoring.md — Current TDD Structure & PRD Proposal

### 2.1 Current TDD-Conditional Content

**TDD-Format Detection Rule (L7-13):** Restates the same three-rule detection gate. [CODE-VERIFIED: This matches the extraction-pipeline.md gate description; both are protocol docs consumed by the inference-based skill, not by the CLI code. The CLI code in `executor.py` implements its own detection logic.]

**Standard 5-factor formula (L16-67):** Applies to non-TDD inputs. Factors: `requirement_count` (0.25), `dependency_depth` (0.25), `domain_spread` (0.20), `risk_severity` (0.15), `scope_size` (0.15). [UNVERIFIED against CLI code: scoring is currently performed by the inference-based roadmap skill, not by deterministic CLI code. No `scoring.py` or equivalent was found in the CLI.]

**TDD 7-factor formula (L70-108):** Adds `api_surface` (0.10) and `data_model_complexity` (0.10) factors derived from Steps 14 and 15. Redistributes weights to accommodate. [UNVERIFIED: Same — inference-based only.]

### 2.2 Proposed PRD Scoring Formula

**Option A: PRD 7-factor formula** (mirroring TDD approach — add 2 new factors, redistribute weights):

| Factor | Raw Value Source | Normalization | Weight |
|--------|-----------------|---------------|--------|
| `requirement_count` | Total FRs + NFRs | `min(count / 50, 1.0)` | 0.20 |
| `dependency_depth` | Max chain in dependency graph | `min(depth / 8, 1.0)` | 0.20 |
| `domain_spread` | Distinct domains >= 10% | `min(domains / 5, 1.0)` | 0.15 |
| `risk_severity` | Weighted risk score | `(weighted_avg - 1.0) / 2.0` | 0.10 |
| `scope_size` | Total line count | `min(lines / 1000, 1.0)` | 0.15 |
| `stakeholder_count` | Distinct personas/stakeholders from Step 21 | `min(count / 8, 1.0)` | 0.10 |
| `business_alignment` | Success metrics with measurable targets from Step 18 / total success metrics | direct ratio [0,1] | 0.10 |

**Rationale:** PRDs surface complexity through stakeholder breadth (more stakeholders = more competing priorities = harder coordination) and business alignment maturity (vague success metrics = higher implementation risk).

**Option B: No PRD-specific formula** — use the standard 5-factor formula for PRDs since PRDs are less technical and the standard formula captures document complexity adequately. PRD-extracted data (personas, stories, metrics) would enrich extraction output without affecting scoring.

**Recommendation:** Option B is safer for initial implementation. PRD data enriches the roadmap content but doesn't fundamentally change how complexity is scored. Stakeholder count and business alignment are harder to normalize reliably. Revisit Option A after PRD pipeline has production usage data.

### 2.3 Template Compatibility Scoring Impact

The Type Match Lookup table (L144-151) currently maps spec dominant types: `feature`, `security`, `migration`, `docs`, `performance`, `quality`. A PRD input would likely map to `feature` or a new `product` type.

**Proposed addition to Type Match Lookup:**

| Spec Dominant Type | Exact Match (1.0) | Related (0.5) | Unrelated (0.0) |
|--------------------|-------------------|---------------|------------------|
| product | product, feature | improvement | docs, security, migration |

---

## 3. tasklist SKILL.md — Current TDD Structure & PRD Proposal

### 3.1 Current TDD-Conditional Content

**Section 4.1a "Supplementary TDD Context" (Lines 140-153):**

Structure:
- Conditional on `--spec <spec-path>` flag
- Three-part TDD detection rule (same as extraction-pipeline.md)
- Six extraction keys: `component_inventory`, `migration_phases`, `testing_strategy`, `observability`, `release_criteria`, `api_surface`
- Fallback: if not TDD-format, log warning and continue with roadmap-only generation
- Error: if file doesn't exist, abort

[CODE-VERIFIED: `tasklist/commands.py` L62-65 defines `--tdd-file` flag (not `--spec`). The SKILL.md describes the inference-based protocol using `--spec`, while the CLI uses `--tdd-file`. These are different interfaces for the same concept — the SKILL.md protocol is consumed by Claude during inference-based `/sc:tasklist` execution, while the CLI code is the programmatic `superclaude tasklist` pipeline.]

[CODE-VERIFIED: `tasklist/prompts.py` L110-123 appends supplementary TDD validation text checking three things: testing strategy coverage (§15), rollback procedures (§19), and component inventory (§10). This is a simpler set than the SKILL.md's six extraction keys.]

**Section 4.4a "Supplementary Task Generation" (Lines 182-196):**

Structure:
- Runs after standard task conversion step
- Seven task generation patterns from TDD context keys:
  - `component_inventory.new` -> `Implement [component_name]` tasks
  - `component_inventory.modified` -> `Update [component_name]` tasks
  - `component_inventory.deleted` -> `Migrate [component_name]` tasks
  - `migration_phases.stages` -> Deployment & Rollout phase
  - `testing_strategy.test_pyramid` -> `Write [level] test suite` tasks
  - `observability.metrics/alerts` -> Instrumentation tasks
  - `release_criteria.definition_of_done` -> `Verify DoD` tasks
- Merge-rather-than-duplicate rule for overlapping tasks
- Tier assignment rules per pattern (STRICT for auth/security/crypto/etc.)

[UNVERIFIED against CLI code: The tasklist CLI (`tasklist/executor.py`, `tasklist/prompts.py`) handles TDD as a validation input only (via `--tdd-file` flag). The supplementary task generation described in SKILL.md Section 4.4a is an inference-based protocol behavior, not currently implemented in the programmatic CLI pipeline.]

### 3.2 Proposed PRD-Conditional Additions

**Section 4.1b "Supplementary PRD Context" (new, parallel to 4.1a):**

If `--spec <spec-path>` was provided and the file is PRD-format (detected by presence of `## Product Overview` OR `## User Personas` OR YAML frontmatter `type` containing "Product Requirements Document"):

Extract the following content and store as `prd_supplementary_context`:
- `user_personas`: scan for User Personas section; extract persona names, roles, and primary goals
- `user_stories`: scan for User Stories section; extract actor-goal-outcome triples
- `success_metrics`: scan for Success Metrics / KPIs section; extract metric definitions with targets
- `release_strategy`: scan for Go-to-Market / Release Strategy section; extract phasing preferences
- `stakeholder_priorities`: scan for Priority Matrix section; extract stakeholder-weighted priorities
- `acceptance_scenarios`: scan for Acceptance Criteria section; extract scenario-based validations

**Section 4.4b "Supplementary PRD Task Generation" (new, parallel to 4.4a):**

| Context Key | Task Pattern | Tier | Phase Assignment |
|-------------|-------------|------|-----------------|
| `user_stories` entries | `Implement user story: [actor] [goal]` | STANDARD | Phase matching roadmap feature coverage |
| `success_metrics` with measurable targets | `Validate metric: [metric_name] meets [target]` | STANDARD | Final phase |
| `acceptance_scenarios` entries | `Verify acceptance: [scenario_name]` | STANDARD | Same phase as related feature |
| `release_strategy.phases` | Inform phase bucket naming and ordering (enrichment, not new tasks) | N/A | N/A |
| `stakeholder_priorities` | Adjust task ordering within phases by stakeholder weight (enrichment, not new tasks) | N/A | N/A |

**Key difference from TDD pattern:** PRD supplementary content generates fewer mandatory tasks. PRDs describe *what* and *why*, not *how*. The primary value is enrichment (better task descriptions, better priority ordering) rather than task generation. TDD content generates concrete implementation tasks because TDDs describe *how*.

### 3.3 CLI Code Changes Needed

The tasklist CLI currently accepts `--tdd-file` only. Extending to support PRD requires:
- Add `--prd-file` flag in `tasklist/commands.py` (parallel to `--tdd-file`)
- Add `prd_file: Path | None = None` in `tasklist/models.py` (parallel to `tdd_file`)
- Add PRD supplementary validation block in `tasklist/prompts.py` (parallel to TDD block at L110-123)
- Update `tasklist/executor.py` to pass `prd_file` through to validation inputs

---

## 4. spec-panel.md — Current TDD Structure & PRD Proposal

### 4.1 Current TDD-Conditional Content

**Step 6a "TDD Input Detection" (L32):**

Structure:
- Conditional on TDD detection (same three-rule gate: `## 10. Component Inventory`, `type: "Technical Design Document"` in frontmatter, or 20+ TDD section headings)
- Behavior: scope improved output to a single release increment using `target_release` from TDD frontmatter
- If `target_release` is empty/absent, ask user to specify before proceeding

**Step 6b "Downstream Roadmap Frontmatter" (L33):**

Structure:
- Conditional on user intent to feed output into `sc:roadmap` (indicated by `--downstream roadmap` flag)
- Ensures output document contains frontmatter fields: `spec_type`, `complexity_score`, `complexity_class`, `target_release`, `feature_id`
- Fields sourced from TDD frontmatter or computed from TDD content analysis

**"Output -- When Input Is a TDD" section (L399-405):**

Two output modes:
- (a) Review document (default): structured review in selected format, covering TDD §5, §6, §7, §8, §13, §15, §20
- (b) Scoped release spec (when `--downstream roadmap`): document in `release-spec-template.md` format extracting FRs from §5.1, NFRs from §5.2, architecture from §6.4, risks from §20, test plan from §15, migration from §19

[UNVERIFIED against CLI code: spec-panel is an inference-based command (`.claude/commands/sc/spec-panel.md`), not a CLI pipeline. There is no `spec_panel.py` in the CLI codebase. The behavior described here is protocol for Claude to follow during `/sc:spec-panel` execution.]

### 4.2 Proposed PRD-Conditional Additions

**Step 6c "PRD Input Detection" (new, parallel to 6a):**

If the input document is a PRD (detected by presence of `## Product Overview` OR `## User Personas` OR `type: "Product Requirements Document"` in YAML frontmatter), scope the improved output to cover product-level requirements. The panel should:
- Validate completeness of user personas, stories, and acceptance criteria
- Assess business alignment between stated success metrics and functional requirements
- Verify traceability from stakeholder needs to specific requirements

Unlike TDD input, PRD input does NOT require `target_release` scoping (PRDs describe the full product scope, not a single release increment).

**Step 6d "Downstream Roadmap Frontmatter for PRD" (new, parallel to 6b):**

If `--downstream roadmap` flag is set and input is PRD-format, ensure the output document contains:
- `spec_type`: "product-requirements" (or copy from PRD frontmatter)
- `complexity_score`: compute from requirement count + stakeholder count (or leave as placeholder)
- `complexity_class`: derive from complexity_score (or leave as placeholder)
- `target_audience`: copy from PRD personas section
- `success_metrics_count`: count of measurable success metrics in PRD

**"Output -- When Input Is a PRD" section (new, parallel to L399-405):**

(a) Review document (default): Expert analysis covers PRD sections: Product Overview, User Personas, User Stories, Functional Requirements, Non-Functional Requirements, Success Metrics, Market Analysis, Risks & Assumptions.

(b) Scoped release spec (when `--downstream roadmap`): Document in `release-spec-template.md` format extracting FRs from PRD requirements section, NFRs from quality/performance sections, risks from Risks & Assumptions, acceptance criteria from User Stories, priority ordering from Stakeholder Priority Matrix.

**Expert Panel Behavior Adjustments for PRD Input:**
- **Wiegers**: Focuses on requirement-to-persona traceability. Every FR should trace to at least one persona.
- **Cockburn**: Validates user stories follow actor-goal-outcome structure. Flags stories missing "So that..." clauses.
- **Adzic**: Checks success metrics have concrete, measurable acceptance examples.
- **Fowler/Newman**: Assess whether PRD architectural implications are sufficient for TDD derivation.

---

## 5. PRD Detection Rule Design

A unified PRD detection rule is needed across all four files (mirroring the TDD detection rule pattern). Proposed:

**PRD-format detection:** Input is classified as PRD-format if it contains `## Product Overview` heading OR `## User Personas` heading OR YAML frontmatter with `type` field containing "Product Requirements Document" OR the document body contains 3 or more of the following section headings: "Market Analysis", "User Stories", "Success Metrics", "Go-to-Market", "Stakeholder Requirements", "Competitive Landscape".

**Code implementation (CORRECTED — QA fix-cycle 1):** Per the design decision, PRD does NOT use `detect_input_type()`. No three-way classification is needed. PRD is passed via `--prd-file` flag and injected as supplementary context blocks in prompts, not as an input mode. Detection rules above are documented for future reference only if PRD-as-mode is ever reconsidered.

---

## 6. Gaps and Questions

1. **PRD template structure undefined for extraction mapping.** The TDD extraction steps reference specific numbered sections (`## 10.`, `## 15.`, etc.). PRD extraction needs an equivalent canonical section reference. The PRD template at `src/superclaude/skills/prd/SKILL.md` was not read during this investigation — its section structure must be confirmed before finalizing extraction step design.

2. **Detection disambiguation: PRD vs generic spec.** TDDs have strong structural signals (28 numbered sections, unique frontmatter fields). PRDs may be harder to distinguish from generic specification documents. The detection rule needs testing against real PRD examples to calibrate false positive rates.

3. **Scoring formula decision deferred.** Whether PRDs need a custom scoring formula (Option A) or can reuse the standard 5-factor formula (Option B) depends on whether PRD-specific factors materially change complexity classification. Recommend starting with Option B.

4. **Supplementary task generation is weaker for PRDs.** TDD content maps directly to implementation tasks (components -> implement tasks, test strategy -> test tasks). PRD content is higher-level — user stories and personas inform task descriptions but don't generate 1:1 tasks as cleanly. The PRD task generation patterns in Section 3.2 are less deterministic than TDD patterns.

5. **CLI flag naming (RESOLVED — QA fix-cycle 1).** Per design decision, the flag is `--prd-file` (parallel naming with `--tdd-file`). No generalization to `--supplementary-file` — that would require detection logic which contradicts the supplementary-only design.

6. **spec-panel is inference-only.** Unlike extraction-pipeline.md and scoring.md (which have partial CLI implementations in `cli/roadmap/`), spec-panel.md is a pure inference-based command with no programmatic CLI backing. PRD additions to spec-panel.md only need to update the protocol doc, not any Python code.

7. **Circular dependency risk.** The PRD skill (`src/superclaude/skills/prd/SKILL.md`) creates PRDs. The roadmap pipeline would then consume PRDs. If the PRD skill outputs don't conform to the expected structure, the extraction pipeline will fail silently. A validation step or schema contract between PRD output and roadmap input is needed.

---

## 7. Stale Documentation Found

1. **extraction-pipeline.md TDD detection rule vs actual code.** [CODE-CONTRADICTED] The doc describes a simple three-rule boolean OR detection. The actual code (`executor.py` L57-117) uses a weighted scoring system with different thresholds and different signal categories. The doc's `## 10. Component Inventory` rule is a subset of the code's `tdd_sections` list. The doc should be updated to reflect the scoring-based approach, or the code should be updated to match the doc.

2. **tasklist SKILL.md `--spec` flag vs CLI `--tdd-file` flag.** [CODE-CONTRADICTED] The SKILL.md (Section 4.1a) describes a `--spec <spec-path>` flag with TDD auto-detection. The actual CLI (`tasklist/commands.py` L62-65) has a `--tdd-file` flag with no auto-detection. These are different interfaces for inference-based vs programmatic execution, which is expected, but the naming divergence could cause confusion.

3. **tasklist SKILL.md Section 4.4a supplementary task generation vs CLI implementation.** [CODE-CONTRADICTED] The SKILL.md describes seven task generation patterns from TDD context. The CLI (`tasklist/prompts.py` L110-123) only implements three validation checks (testing §15, rollback §19, components §10) and does so as part of validation prompts, not as task generation. The SKILL.md describes intended inference-based behavior that the CLI has not yet fully ported.

4. **scoring.md detection rule duplication.** The TDD detection rule is stated in extraction-pipeline.md (L145), scoring.md (L7-13), tasklist SKILL.md (L142-144), and spec-panel.md (L32). These should reference a single canonical definition to prevent drift. Currently they are all textually similar but not identical.

---

## 8. Summary

### Files Needing PRD Updates (by priority)

| File | Priority | Scope of Change | Complexity |
|------|----------|----------------|------------|
| extraction-pipeline.md | HIGH | New Steps 16-22 + PRD detection gate | Medium — requires PRD template analysis |
| tasklist SKILL.md | HIGH | New Sections 4.1b + 4.4b | Medium — task generation patterns less deterministic than TDD |
| spec-panel.md | MEDIUM | New Steps 6c, 6d + output section | Low — inference protocol additions only |
| scoring.md | LOW | PRD detection rule + optional scoring formula + type match entry | Low — recommend standard formula initially |

### Key Design Decisions Needed Before Implementation

1. Confirm PRD template section structure (read `src/superclaude/skills/prd/SKILL.md`)
2. RESOLVED: Use `--prd-file` (parallel naming with `--tdd-file`)
3. Decide: PRD-specific scoring formula vs standard 5-factor formula
4. Define PRD detection signals and test against real PRD examples
5. Establish schema contract between PRD skill output and roadmap pipeline input

---

**Status:** Complete
