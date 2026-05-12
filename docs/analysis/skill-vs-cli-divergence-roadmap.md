# SKILL.md vs CLI Port: Divergence Analysis — sc:roadmap

**Date**: 2026-04-16
**Skill**: `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` (v2.0.0)
**CLI Port**: `src/superclaude/cli/roadmap/` (25 files, ~13,166 lines)
**Branch**: `feat/tdd-spec-merge`

---

## Executive Summary

The CLI port is **not a 1:1 translation** of the skill — it is a significantly evolved, opinionated reimplementation. The skill defines a 5-wave LLM-orchestrated pipeline using Claude Code tools (Skill, Task, Read, Write). The CLI port replaces that with a deterministic Python subprocess pipeline with 12-14 steps, adversarial dual-agent generation, structural checkers, semantic debate layers, convergence engines, and remediation loops.

The divergences fall into 5 categories:
1. **Missing from CLI** — Skill features with no CLI equivalent
2. **Reimagined in CLI** — Same concept, fundamentally different implementation
3. **CLI-only additions** — Features in CLI with no skill equivalent
4. **Scoring/formula mismatches** — Algorithms defined in refs/ but not ported
5. **Prompt/template drift** — Content differences in what the LLM is asked to do

---

## Category 1: Missing from CLI (Skill features not ported)

These are features explicitly defined in SKILL.md + refs/ that have **zero implementation** in the CLI port.

### D-001: Multi-spec consolidation (Wave 1A) — NOT PORTED

**Skill**: Wave 1A invokes `Skill sc:adversarial-protocol --compare <spec-list>` to merge 2-10 specs into a unified spec. Includes convergence routing (>=0.6 PASS, >=0.5 PARTIAL, <0.5 FAIL).

**CLI**: The `--specs` flag does not exist in `commands.py`. The CLI accepts 1-3 positional `INPUT_FILES` but routes them via `_route_input_files()` into `spec_file` / `tdd_file` / `prd_file` slots — this is **supplementary input classification**, not spec consolidation.

**Fix**: Either:
- (a) Add `--specs` flag that invokes an adversarial consolidation step before extraction, OR
- (b) Document that multi-spec consolidation is skill-only and out of CLI scope, remove from any CLI-facing docs

**Effort**: Large (if implementing), Small (if documenting as out-of-scope)

---

### D-002: Multi-roadmap adversarial generation via sc:adversarial — NOT PORTED

**Skill**: Wave 2 invokes `Skill sc:adversarial-protocol --source <spec> --generate roadmap --agents <list>` for competing roadmap variant generation with sc:adversarial orchestration.

**CLI**: The CLI has its OWN adversarial pipeline (generate-A + generate-B → diff → debate → score → merge) built directly into `executor._build_steps()` and `prompts.py`. This is a **self-contained dual-agent pipeline**, not a delegation to sc:adversarial-protocol.

**Key difference**: The skill delegates to a separate skill (sc:adversarial) which handles F1-F5 stages. The CLI inlines a 5-step adversarial cycle (generate → diff → debate → score → merge) with its own prompts and gates.

**Fix**: This is an intentional architectural decision (CLI must work without skill system). Document the equivalence mapping:
- Skill's `sc:adversarial F1` (variant generation) ≈ CLI's `generate-A` + `generate-B` parallel steps
- Skill's `sc:adversarial F2/F3` (diff + debate) ≈ CLI's `diff` + `debate` steps
- Skill's `sc:adversarial F4/F5` (base selection + merge) ≈ CLI's `score` + `merge` steps

**Effort**: None (document only)

---

### D-003: Return contract consumption (9-field schema) — NOT PORTED

**Skill**: Consumes a structured return contract from sc:adversarial with 9 fields: `status`, `convergence_score`, `merged_output_path`, `artifacts_dir`, `base_variant`, `unresolved_conflicts`, `fallback_mode`, `failure_stage`, `invocation_method`.

**CLI**: No return contract concept. The adversarial cycle produces `merge.md` directly. Quality is enforced via `MERGE_GATE` (semantic checks) rather than contract routing.

**Fix**: Document as intentional. The CLI's gate system replaces the skill's contract-based routing.

**Effort**: None

---

### D-004: 5-factor complexity scoring formula — NOT PORTED

**Skill** (`refs/scoring.md`): Defines an explicit formula:
```
complexity_score = (req_count_norm * 0.25) + (dep_depth_norm * 0.25)
                 + (domain_spread_norm * 0.20) + (risk_severity_norm * 0.15)
                 + (scope_size_norm * 0.15)
```
With normalization functions: `min(count/50, 1.0)`, `min(depth/8, 1.0)`, etc.

**CLI**: No deterministic complexity scoring function exists. The `build_extract_prompt()` asks the LLM to produce `complexity_class` and `complexity_score` in frontmatter, but there is no Python function computing the score. The LLM infers it.

**Fix**: Add a `compute_complexity_score()` function in a new `scoring.py` that implements the 5-factor formula from `refs/scoring.md`. Use it as a gate check against the LLM's output, or replace LLM inference entirely.

```python
# src/superclaude/cli/roadmap/scoring.py
def compute_complexity_score(req_count, dep_depth, domain_count, risk_weights, scope_lines):
    return (
        min(req_count / 50, 1.0) * 0.25
        + min(dep_depth / 8, 1.0) * 0.25
        + min(domain_count / 5, 1.0) * 0.20
        + ((risk_weights - 1.0) / 2.0) * 0.15
        + min(scope_lines / 1000, 1.0) * 0.15
    )
```

**Effort**: Small

---

### D-005: TDD 7-factor complexity scoring — NOT PORTED

**Skill** (`refs/scoring.md`): TDD specs use a 7-factor formula adding `api_surface_norm` (0.10) and `data_model_complexity_norm` (0.10) with rebalanced weights.

**CLI**: TDD detection exists (`detect_input_type()` in executor.py with weighted signal scoring, threshold >= 5), but no 7-factor complexity scoring function.

**Fix**: Add alongside D-004 in `scoring.py`.

**Effort**: Small

---

### D-006: Template compatibility scoring (4-factor) — NOT PORTED

**Skill** (`refs/scoring.md`): 4-factor template scoring:
```
template_score = (domain_match * 0.40) + (complexity_alignment * 0.30)
               + (type_match * 0.20) + (version_compat * 0.10)
```
With Jaccard similarity for domain_match, lookup table for type_match.

**CLI**: `templates.py` has `get_template_path(name)` which resolves Jinja2 templates via `importlib.resources`. No compatibility scoring. Templates are hardcoded (`roadmap.md.j2`, `tasklist-index.md.j2`, `tasklist-phase.md.j2`).

**Fix**: This is likely acceptable — the CLI uses prompt-based generation rather than template-based assembly, so template "compatibility" is moot. The prompts themselves encode the structure. Document this as an intentional simplification.

**Effort**: None (document)

---

### D-007: 4-tier template discovery — NOT PORTED

**Skill** (`refs/templates.md`): local → user → plugin → inline generation.

**CLI**: Single-tier: `importlib.resources` + source-relative fallback. No user or plugin template directories.

**Fix**: If template customization is desired, add user-tier lookup (`~/.claude/templates/roadmap/`). Otherwise document as intentional.

**Effort**: Small (if implementing), None (if documenting)

---

### D-008: Persona confidence calculation — NOT PORTED

**Skill** (`refs/scoring.md`): Formula:
```
confidence = base_confidence(0.7) * domain_weight * coverage_bonus
```
With 6 persona-domain mappings and min thresholds (primary >= 0.3, consulting >= 0.2).

**CLI**: No persona confidence calculation. The `AgentSpec` dataclass has `model` + `persona` fields, but persona is user-specified or defaults to `"architect"`. No auto-detection from domain distribution.

**Fix**: Add `compute_persona_confidence()` in `scoring.py` using the formula from `refs/scoring.md`. Wire into the extraction step to auto-select persona when not explicitly provided.

**Effort**: Medium

---

### D-009: Domain keyword dictionaries (7 domains) — NOT PORTED as deterministic code

**Skill** (`refs/extraction-pipeline.md`): 7 domain keyword dictionaries with primary (weight 2.0) and secondary (weight 1.0) keywords, plus Jaccard-based assignment algorithm.

**CLI**: Domain classification is delegated entirely to the LLM via `build_extract_prompt()`. The extraction prompt asks for `domain_distribution` in frontmatter but provides no keyword dictionaries.

**Fix**: Add a `classify_domains()` function with the keyword dictionaries from the skill. Use it as a post-extraction validation check against the LLM's domain distribution.

**Effort**: Medium

---

### D-010: Chunked extraction protocol (>500 lines) — NOT PORTED

**Skill** (`refs/extraction-pipeline.md`): Multi-step chunking algorithm: section index → chunk assembly (~400 lines, max 600) → per-chunk extraction → merge → deduplication → cross-reference resolution → global ID assignment.

**CLI**: No chunking. The entire spec is embedded inline via `_embed_inputs()` up to `_EMBED_SIZE_LIMIT` (122KB). Specs that exceed this are truncated.

**Fix**: For specs >500 lines, implement the chunking protocol. This is important for large TDD documents.

**Effort**: Large

---

### D-011: 4-pass completeness verification — NOT PORTED

**Skill** (`refs/extraction-pipeline.md`): Source Coverage, Anti-Hallucination, Section Coverage, Count Reconciliation — each with PASS/WARN/FAIL thresholds.

**CLI**: No explicit completeness verification. The `EXTRACT_GATE` validates frontmatter fields and minimum line count, but doesn't verify source coverage or anti-hallucination.

**Fix**: Add completeness verification as post-extraction gate checks in `gates.py`. At minimum, add anti-hallucination (verify requirement source_lines map to real spec content).

**Effort**: Medium

---

### D-012: Session persistence via Serena memory — NOT PORTED

**Skill**: Persists session state to Serena memory using key `sc-roadmap:<spec-name>:<timestamp>` with 12+ fields. Resume protocol checks spec file hash.

**CLI**: Uses file-based `.roadmap-state.json` with atomic writes. No Serena integration. The state schema is different (focuses on step results, agent configs, spec hash, remediation metadata).

**Fix**: This is an intentional difference — CLI uses file-based state, skill uses Serena. The CLI's approach is actually more robust (survives without MCP). Document as intentional.

**Effort**: None

---

### D-013: Validation score aggregation (quality-engineer 0.55 + self-review 0.45) — NOT PORTED

**Skill** (`refs/validation.md`): Two specific agents (quality-engineer, self-review) with weighted aggregation formula and PASS/REVISE/REJECT thresholds.

**CLI**: Validation uses `validate_prompts.build_reflect_prompt()` which dispatches N agents with identical reflection prompts, then merges via `build_merge_prompt()` with agreement categorization (BOTH_AGREE/ONLY_A/ONLY_B/CONFLICT). No weighted score aggregation.

**Fix**: The CLI's approach (agreement-based merge) is arguably more robust than the skill's weighted average. However, the specific agent roles (quality-engineer checks vs self-review 4-question protocol) are lost. Consider:
- (a) Make one agent use the quality-engineer prompt (completeness, consistency, traceability, test-strategy) and the other use the self-review prompt (faithfulness, achievability, risk quality, test actionability)
- (b) Add score aggregation with PASS >= 85% / REVISE 70-84% / REJECT < 70% thresholds

**Effort**: Medium

---

### D-014: REVISE loop (max 2 iterations) — NOT PORTED

**Skill** (`refs/validation.md`): If validation score is 70-84%, collect recommendations, re-run Wave 3 → Wave 4. Max 2 iterations, then PASS_WITH_WARNINGS.

**CLI**: No REVISE loop in validation. Validation produces a report; remediation is a separate step in the main pipeline (not validation). The convergence engine in `convergence.py` has a similar concept (3 runs with budget) but operates on spec-fidelity, not validation.

**Fix**: Add REVISE loop to `validate_executor.py`. If blocking_issues_count > 0 and <= threshold, trigger remediation and re-validate.

**Effort**: Medium

---

### D-015: Output collision check (append -N suffix) — NOT PORTED

**Skill** (Wave 0 Step 3): If output directory already contains roadmap artifacts, append `-N` suffix to all output filenames.

**CLI**: No collision check. Existing files are overwritten. The `--resume` flag handles re-runs but doesn't protect existing artifacts from new runs.

**Fix**: Add collision detection in `execute_roadmap()` before writing artifacts.

**Effort**: Small

---

### D-016: Milestone count formula — NOT PORTED as deterministic code

**Skill** (`refs/templates.md`): `count = base + floor(domain_count / 2)` where base is 3 (LOW), 5 (MEDIUM), 8 (HIGH).

**CLI**: Milestone count is LLM-inferred from the generate prompt. The prompt says to produce a milestone-based roadmap but doesn't prescribe the formula.

**Fix**: Add as a gate check — verify the LLM's milestone count is within the expected range for the complexity class.

**Effort**: Small

---

### D-017: Effort estimation algorithm — NOT PORTED as deterministic code

**Skill** (`refs/templates.md`): XS/S/M/L/XL effort levels based on deliverable count * risk multiplier.

**CLI**: The generate prompt includes an `Eff` column in the task table format but doesn't prescribe the effort estimation algorithm.

**Fix**: Add as a post-generation validation in gates or as deterministic enrichment.

**Effort**: Small

---

### D-018: Dependency DAG cycle detection — NOT PORTED

**Skill** (Wave 2 Step 5): Validate the dependency graph is acyclic. Abort with specific error message on circular dependency.

**CLI**: The generate prompt asks for dependency columns but no deterministic cycle detection is performed on the output.

**Fix**: Add a `detect_dag_cycles()` function that parses the dependency column from the generated roadmap and validates acyclicity.

**Effort**: Small

---

### D-019: MCP circuit breaker fallbacks — NOT PORTED

**Skill**: Sequential/Context7/Serena unavailable → specific fallback behaviors.

**CLI**: No MCP integration at all. The CLI uses subprocess-based LLM calls via `ClaudeProcess`. No MCP servers are consulted.

**Fix**: Document as intentional — CLI operates independently of MCP.

**Effort**: None

---

### D-020: Compliance tiers (STRICT/STANDARD/LIGHT) — NOT PORTED

**Skill**: Auto-escalation to STRICT when complexity > 0.8, security reqs detected, >3 domains. STRICT requires validation PASS.

**CLI**: No compliance tier system. The `--no-validate` flag is the only validation toggle.

**Fix**: Add compliance tier detection post-extraction. STRICT → require validation pass. LIGHT → allow --no-validate.

**Effort**: Small-Medium

---

## Category 2: Reimagined in CLI (Same concept, different implementation)

### D-021: Wave architecture → 12-step pipeline

**Skill**: 5 waves (0-4), each with entry/exit criteria, ref loading.
**CLI**: 12-14 steps in a linear pipeline with parallel branches: extract → [generate-A, generate-B] → diff → debate → score → merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate → (certify).

**Mapping**:
| Skill Wave | CLI Steps |
|---|---|
| Wave 0 (Prerequisites) | `commands.py` CLI parsing + `_route_input_files()` |
| Wave 1A (Spec Consolidation) | Not ported |
| Wave 1B (Extraction) | `extract` step |
| Wave 2 (Planning + Template) | `generate-A/B` → `diff` → `debate` → `score` → `merge` |
| Wave 3 (Generation) | `test-strategy` + `anti-instinct` + `spec-fidelity` + `wiring-verification` + `deviation-analysis` + `remediate` + `certify` |
| Wave 4 (Validation) | `validate` subcommand (separate entry point) |

**Key difference**: The skill's Wave 3 is "generation" (write artifacts). The CLI's equivalent steps are much richer — they include spec-fidelity checking, convergence loops, deviation analysis, remediation, and certification. This is a substantial enhancement.

---

### D-022: Validation agents — different prompts and scoring

**Skill**: quality-engineer (4 dimensions: completeness/consistency/traceability/test-strategy) + self-review (4 questions: faithfulness/achievability/risk quality/test actionability). Weighted score aggregation.

**CLI**: N identical reflect agents (7-9 dimensions: schema/structure/traceability/cross-file/parseability + optional coverage/proportionality + warning interleave/decomposition) with agreement-based adversarial merge.

**Fix**: Align validation dimensions. The CLI's dimensions are actually a superset but organized differently.

---

### D-023: Adversarial pipeline — skill delegates vs CLI inlines

**Skill**: Delegates to `sc:adversarial-protocol` skill via Skill tool invocation.
**CLI**: Inlines a complete 5-step adversarial cycle with its own prompts (diff/debate/score/merge).

**Status**: Intentional — CLI must be self-contained.

---

### D-024: ID schema — different formats

**Skill**: `M{digit}` milestones, `D{m}.{seq}` deliverables, `T{m}.{seq}` tasks, `R-{3digits}` risks.
**CLI prompts**: Preserves source IDs verbatim (FR-EVAL-001.1, etc.), uses `DM-xxx`, `COMP-xxx`, `API-xxx` for TDD entities.

**Fix**: The CLI's approach (preserve source IDs) is more faithful to spec fidelity. The skill's approach (generate new IDs) may cause traceability loss. Document as intentional improvement.

---

### D-025: extraction.md — written in Wave 1B (skill) vs extract step (CLI)

**Skill**: extraction.md is written immediately in Wave 1B for resumability, then frontmatter updated in Wave 3.
**CLI**: extraction.md is the output of the `extract` step with `EXTRACT_GATE` validation. `_inject_pipeline_diagnostics()` adds timing metadata post-extraction.

**Status**: Functionally equivalent.

---

## Category 3: CLI-only additions (not in skill)

These are significant features in the CLI with **no skill equivalent**.

### D-026: Structural checkers (5 dimensions)

The CLI has `structural_checkers.py` with 5 deterministic (no-LLM) checkers:
- `check_signatures()` — phantom IDs, missing functions, param arity/type mismatches
- `check_data_models()` — missing files, path prefix mismatches, uncovered enums/fields
- `check_gates()` — missing frontmatter fields, step params, ordering violations
- `check_cli()` — uncovered modes, default mismatches
- `check_nfrs()` — threshold contradictions, security gaps, dependency violations

**Not in skill**. This is a CLI-only innovation.

---

### D-027: Semantic debate layer

The CLI has `semantic_layer.py` with prosecutor/defender adversarial debate for HIGH findings:
- Rubric scoring (evidence_quality, impact_specificity, logical_coherence, concession_handling)
- Verdict thresholds (margin > 0.15 for CONFIRM/DOWNGRADE)
- Full debate transcript recording

**Not in skill**.

---

### D-028: Convergence engine with budget system

The CLI has `convergence.py` with:
- DeviationRegistry (file-backed, stable finding IDs)
- TurnLedger (budget tracking: checker=10, remediation=8, regression_validation=15)
- Up to 3 convergence runs (catch/verify/backup)
- Progress reimbursement when HIGHs decrease
- Regression detection and 3-agent parallel validation

**Not in skill**. This is a substantial CLI-only system.

---

### D-029: Anti-instinct detection (3 modules)

The CLI has a 3-module anti-instinct system:
1. `obligation_scanner.py` — detects scaffold terms (mock, stub, placeholder, skeleton, etc.)
2. `integration_contracts.py` — detects integration wiring patterns (dispatch tables, registries, DI, etc.)
3. `fingerprint.py` — code identifier coverage check (min 0.7 ratio)

**Not in skill**.

---

### D-030: Remediation subsystem (4 files)

`remediate.py`, `remediate_prompts.py`, `remediate_parser.py`, `remediate_executor.py` — complete remediation pipeline with:
- Snapshot/rollback safety
- File allowlist enforcement
- Diff-size guard (30% threshold)
- Cross-file coherence checking
- Parallel agent execution with retry

**Not in skill**.

---

### D-031: Certification step

`certify_prompts.py` — per-finding verification with PASS/FAIL judgment and NFR-012 (no automatic remediation loop).

**Not in skill**.

---

### D-032: Spec-patch resume cycle

When subprocess deviations modify the spec during pipeline execution, the CLI detects spec hash changes and triggers a re-run cycle (FR-2.24.1.9-11).

**Not in skill**.

---

### D-033: Wiring verification

`build_wiring_verification_prompt()` — static analysis for unwired callables, orphan modules, unregistered dispatch entries.

**Not in skill**.

---

### D-034: TDD/PRD multi-input routing

`_route_input_files()` classifies 1-3 positional inputs + explicit flags into spec/tdd/prd slots with conflict detection, auto-detection, and enrichment.

**Skill**: Only supports single spec or multi-spec consolidation. No TDD/PRD supplementary input concept.

---

### D-035: Decomposition pass

`apply_decomposition_pass()` — post-generation decomposition of deliverables into Implement/Verify pairs.

**Not in skill**.

---

## Category 4: Actionable Fix Plan

Prioritized by impact and effort.

### Priority 1 — High impact, small effort

| # | Divergence | Fix | File to modify |
|---|---|---|---|
| 1 | D-004 | Add `compute_complexity_score()` with 5-factor formula | New: `scoring.py` |
| 2 | D-005 | Add `compute_tdd_complexity_score()` with 7-factor formula | `scoring.py` |
| 3 | D-015 | Add output collision check before writing artifacts | `executor.py` |
| 4 | D-016 | Add milestone count range validation to `MERGE_GATE` | `gates.py` |
| 5 | D-018 | Add `detect_dag_cycles()` on dependency graph post-generation | New: `scoring.py` or `gates.py` |

### Priority 2 — Medium impact, medium effort

| # | Divergence | Fix | File to modify |
|---|---|---|---|
| 6 | D-008 | Add `compute_persona_confidence()` with 6-domain mapping | `scoring.py` |
| 7 | D-009 | Add `classify_domains()` with keyword dictionaries as gate check | `scoring.py` |
| 8 | D-011 | Add anti-hallucination check to `EXTRACT_GATE` | `gates.py` |
| 9 | D-013 | Differentiate reflect agent prompts (quality-engineer vs self-review) | `validate_prompts.py` |
| 10 | D-014 | Add REVISE loop to validation (re-run on 70-84% score) | `validate_executor.py` |
| 11 | D-020 | Add compliance tier detection and enforcement | `executor.py`, `gates.py` |

### Priority 3 — Large effort or intentional divergences (document only)

| # | Divergence | Action |
|---|---|---|
| 12 | D-001 | Document: multi-spec consolidation is skill-only |
| 13 | D-002 | Document: CLI uses inline adversarial, not sc:adversarial delegation |
| 14 | D-003 | Document: gate system replaces return contract routing |
| 15 | D-006 | Document: prompt-based generation replaces template compatibility scoring |
| 16 | D-007 | Document: single-tier template discovery is intentional |
| 17 | D-010 | Implement chunked extraction for specs >500 lines (large effort) |
| 18 | D-012 | Document: file-based state replaces Serena persistence |
| 19 | D-019 | Document: CLI operates without MCP |
| 20 | D-024 | Document: preserve-source-IDs is intentional improvement over new-ID generation |

---

## Category 5: Prompt/Template Drift

### D-036: Extraction prompt vs refs/extraction-pipeline.md

**Skill**: 8-step pipeline (title → FRs → NFRs → scope → deps → success criteria → risks → ID assignment). Priority heuristic: "must"/"required" → P0, "should" → P1, etc.

**CLI**: `build_extract_prompt()` asks for 13 frontmatter fields + 8 body sections. Preserves source IDs verbatim rather than assigning new FR-001/NFR-001 IDs. No explicit priority heuristic keywords.

**Fix**: Add the priority assignment keyword heuristic from the skill to the extraction prompt.

---

### D-037: Generation prompt vs refs/templates.md body template

**Skill**: Body template defines Overview → Milestone Summary table → Dependency Graph → Per-milestone sections → Risk Register → Decision Summary → Success Criteria.

**CLI**: `build_generate_prompt()` uses task table format `| # | ID | Task | Comp | Deps | AC | Eff | Pri |` with granularity floor (40-150+ rows). This is a **task-oriented roadmap**, not the milestone-centric roadmap the skill produces.

**Fix**: This is a fundamental design difference. The CLI produces a more actionable, task-level roadmap. If alignment is needed, the CLI prompt should also include the milestone summary table and dependency graph sections from the skill's template.

---

### D-038: Test-strategy prompt alignment

**Skill**: test-strategy.md body template includes Validation Philosophy, Validation Milestones table, Issue Classification, Acceptance Gates, Validation Coverage Matrix.

**CLI**: `build_test_strategy_prompt()` includes interleave ratio mapping and issue classification table. Missing: Acceptance Gates and Validation Coverage Matrix sections.

**Fix**: Add Acceptance Gates and Validation Coverage Matrix sections to the test-strategy prompt.

---

### D-039: Validation prompt vs refs/validation.md agent prompts

**Skill**: Two distinct agent prompts:
- Quality-engineer: 4 weighted dimensions (completeness 0.35, consistency 0.30, traceability 0.20, test-strategy 0.15)
- Self-review: 4 weighted questions (faithfulness 0.30, achievability 0.25, risk quality 0.25, test actionability 0.20)

**CLI**: Single `build_reflect_prompt()` used for all agents with 7-9 dimensions, no per-dimension weighting. The merge uses agreement categories instead of score aggregation.

**Fix**: Create two prompt variants (`build_quality_engineer_prompt()` and `build_self_review_prompt()`) that match the skill's agent specialization. Route agent-A to quality-engineer, agent-B to self-review.

---

## Summary Matrix

| Category | Count | Action Required |
|---|---|---|
| Missing from CLI | 20 | 5 implement, 8 document, 7 implement-or-document |
| Reimagined | 5 | Document mappings |
| CLI-only additions | 10 | Backport to skill spec or document as extensions |
| Prompt drift | 4 | Align prompts |
| **Total divergences** | **39** | |

---

## Execution Order

When working through the fixes, follow this order to avoid cascading changes:

1. **Create `scoring.py`** — D-004, D-005, D-008, D-009 (new file, no dependencies)
2. **Update `gates.py`** — D-011, D-016, D-018 (add gate checks using scoring.py)
3. **Update `executor.py`** — D-015 (collision check, small change)
4. **Update `prompts.py`** — D-036, D-038 (add priority heuristic, acceptance gates)
5. **Update `validate_prompts.py`** — D-039 (split into two agent-specific prompts)
6. **Update `validate_executor.py`** — D-013, D-014 (route agents to different prompts, add REVISE loop)
7. **Add compliance tiers** — D-020 (touches executor.py + gates.py)
8. **Document intentional divergences** — D-001 through D-003, D-006, D-007, D-012, D-019, D-024
9. **Large items (optional)** — D-010 (chunked extraction), D-017 (effort estimation)

---

*Analysis complete. Each D-xxx item is independently actionable.*
