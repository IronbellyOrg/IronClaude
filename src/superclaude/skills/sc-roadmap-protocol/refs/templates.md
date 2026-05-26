# Templates Reference

Reference document for Wave 2 (Planning & Template Selection) and Wave 3 (Generation). Documents the canonical CLI **single-template resolver** behavior, plus the milestone-structure heuristics, body templates, and YAML frontmatter schemas used when filling in that template.

---

## Single-Template Resolver (CLI Canonical Behavior)

> **CLI parity (B-5, VERIFIED).** The roadmap CLI does **not** perform multi-tier template discovery. It resolves a single bundled template file by name via `get_template_path()` in `src/superclaude/cli/roadmap/templates.py`. There is no Tier 1 (local), Tier 2 (user), Tier 3 (plugin marketplace), or Tier 4 (inline fallback) selection path in the CLI today.

### Named template constants

The CLI exposes three named template constants (`src/superclaude/cli/roadmap/templates.py:14-16`):

| Constant | Value | Used by |
|---|---|---|
| `ROADMAP_TEMPLATE` | `"roadmap_template.compressed.md"` | sc:roadmap (Wave 3 roadmap.md generation) |
| `TASKLIST_INDEX_TEMPLATE` | `"tasklist_index_template.md"` | sc:tasklist (index file generation) |
| `TASKLIST_PHASE_TEMPLATE` | `"tasklist_phase_template.md"` | sc:tasklist (per-phase file generation) |

### Resolution algorithm

`get_template_path(name: str) -> Path` (`src/superclaude/cli/roadmap/templates.py:21-71`) resolves a template filename to an absolute path in two ordered steps:

1. **Installed-package lookup.** Try `importlib.resources.files("superclaude.examples").joinpath(name)`. If the resolved path exists, return it.
2. **Src-relative fallback.** Otherwise compute `<repo>/src/superclaude/examples/<name>` from `__file__` and return it if it exists.
3. **Failure.** If neither method finds the file, raise `FileNotFoundError` naming both searched locations.

This is a single-template resolver — it accepts a known constant name and returns one path. It does **not** glob a directory, validate user-supplied YAML frontmatter, score multiple candidates, or fall back to inline generation.

### What this means for skill behavior

- The skill's Wave 2 "template selection" step is, in CLI terms, "resolve `ROADMAP_TEMPLATE` via `get_template_path()` and load it." There is no user/project/plugin override surface.
- The bundled template file (`src/superclaude/examples/roadmap_template.compressed.md`) is the only canonical input that shapes roadmap.md output structure. Customizing roadmap output today means editing that bundled file inside the source tree.
- Skill prose referencing "Tier 1 local templates," "Tier 2 user templates," or "Tier 3 plugin marketplace" describes **inference-only** behavior that is not implemented in the CLI. See "Non-canonical multi-tier discovery (inference-only)" below for the demoted material.

---

## Non-canonical multi-tier discovery (inference-only)

> **Scope.** The following material describes a multi-tier discovery model that is **not** implemented by the current CLI. It is retained as inference-only guidance for skill-mode operators who want to layer project- or user-level template overrides on top of `get_template_path()` manually. Anything in this section is out of canonical CLI scope and must not be cited as CLI behavior.

A skill-mode operator who wants project/user template overrides can manually:

1. Maintain candidate templates under `.dev/templates/roadmap/` (project) or `~/.claude/templates/roadmap/` (user) with YAML frontmatter (`name`, `type`, `domains`, optional `target_complexity`, `min_version`, `milestone_count_range`).
2. Select a candidate using the compatibility-scoring formula in `refs/scoring.md` (filter by `min_version`, score, require ≥ 0.6, tie-break by location).
3. Use the selected file's body in place of `ROADMAP_TEMPLATE` for that single run.

A future plugin marketplace (`~/.claude/plugins/*/templates/roadmap/`) is design-vision only; no CLI runway is currently implemented. If/when multi-tier discovery is added to the CLI, this section should be promoted back to canonical and the single-template-resolver section above should be updated accordingly.

---

## Milestone Structure Heuristics

The bundled `ROADMAP_TEMPLATE` carries the structural prompt that the LLM consumes during Wave 3. The heuristics below describe how the LLM is expected to fill in that structure given the extraction.md output. They are not a separate "inline fallback" path — they are the milestone-generation guidance embedded in the single bundled template.

### Milestone Count Selection

| Complexity Class | Milestone Count | Rationale |
|-----------------|----------------|-----------|
| LOW (< 0.4) | 3-4 | Simple scope, few dependencies |
| MEDIUM (0.4-0.7) | 5-7 | Moderate scope, cross-domain work |
| HIGH (> 0.7) | 8-12 | Complex scope, many dependencies |

**Exact count within range**: `base + floor(domain_count / 2)`

- LOW: base = 3
- MEDIUM: base = 5
- HIGH: base = 8
- `domain_count` = number of domains with >= 10% representation

### Domain-Specific Milestone Mapping

Each domain detected with >= 10% representation generates at least one dedicated milestone. The milestone type and focus depends on the domain.

| Domain | Milestone Type | Typical Focus |
|--------|---------------|---------------|
| frontend | FEATURE | UI components, user flows, accessibility |
| backend | FEATURE | API endpoints, data models, service logic |
| security | SECURITY | Authentication, authorization, threat mitigation |
| performance | IMPROVEMENT | Optimization, caching, load testing |
| documentation | DOC | User guides, API docs, architecture docs |

### Milestone Generation Algorithm

1. **Foundation milestone** (always M1): Project setup, dependencies, architecture decisions. Type: FEATURE. Priority: P0.
2. **Domain milestones**: One per domain with >= 10%, ordered by domain percentage (highest first). Type from domain mapping above.
3. **Integration milestone**: If domain_count >= 2, add an integration milestone after domain milestones. Type: TEST. Priority: P1.
4. **Validation milestone**: Final milestone for end-to-end validation and acceptance testing. Type: TEST. Priority: P1.

**Validation milestone interleaving**: Based on interleave ratio from complexity class (see `refs/scoring.md`):

- LOW (1:3): Insert validation milestone after every 3 work milestones
- MEDIUM (1:2): Insert validation milestone after every 2 work milestones
- HIGH (1:1): Insert validation milestone after every work milestone

### Priority Assignment

Milestones are assigned priorities based on dependency depth and domain criticality:

| Priority | Assignment Rule |
|----------|----------------|
| P0 | Foundation milestone (M1); milestones containing security requirements; milestones with no dependencies that other milestones depend on |
| P1 | Domain milestones for dominant domain (highest %); milestones on the critical dependency path |
| P2 | Domain milestones for secondary domains; integration milestones |
| P3 | Documentation milestones; validation milestones (they validate but don't produce features) |

**Tie-breaking**: When multiple rules apply, use the highest priority (P0 > P1 > P2 > P3).

### Dependency Mapping Rules

- M1 (Foundation) has no dependencies
- Domain milestones depend on M1
- Domain milestones for related domains may have inter-dependencies (e.g., backend milestone blocks frontend milestone if frontend requires API endpoints)
- Integration milestones depend on all domain milestones they integrate
- Validation milestones depend on the work milestones they validate
- **Cycle detection**: After mapping, verify no circular dependencies exist. If a cycle is detected, break it by removing the dependency with the weakest relationship (lowest domain overlap between the two milestones).

### Required Sections Per Milestone

Every generated milestone must include these sections (matching the roadmap.md body template):

1. **Objective**: 1-2 sentence goal statement
2. **Deliverables**: Table with ID, description, acceptance criteria
3. **Dependencies**: List of prerequisite milestones or "None"
4. **Risk Assessment**: Table with risk, probability, impact, mitigation

---

## Effort Estimation

Each milestone receives an effort estimate based on its deliverable count, complexity contribution, and risk profile. Effort is expressed as relative levels (not time estimates).

### Effort Levels

| Level | Deliverable Count | Complexity Factor | Typical Scope |
|-------|-------------------|-------------------|---------------|
| XS | 1-2 | < 0.3 | Single-concern, minimal dependencies |
| S | 3-4 | 0.3-0.5 | Focused scope, few dependencies |
| M | 5-7 | 0.5-0.7 | Multi-concern, cross-dependency |
| L | 8-10 | 0.7-0.85 | Broad scope, significant integration |
| XL | 11+ | > 0.85 | System-wide, many dependencies |

### Estimation Algorithm

For each milestone:

1. **Count deliverables**: `deliverable_count` = number of D#.# items in the milestone
2. **Compute complexity contribution**: `complexity_factor` = (milestone's requirements / total requirements) * complexity_score
3. **Assess risk multiplier**:
   - No High risks: multiplier = 1.0
   - 1 High risk: multiplier = 1.2
   - 2+ High risks: multiplier = 1.5
4. **Compute adjusted count**: `adjusted = deliverable_count * risk_multiplier`
5. **Map to effort level** using the table above (use `adjusted` count and `complexity_factor`, whichever maps to the higher effort level)

### Risk Level Assignment

Each milestone's risk level is derived from the risks in extraction.md that map to its requirements:

| Risk Level | Condition |
|------------|-----------|
| Low | No High-probability or High-impact risks associated with milestone requirements |
| Medium | At least 1 Medium-probability AND Medium-impact risk, OR 1 High in either dimension |
| High | At least 1 High-probability AND High-impact risk, OR 2+ High risks in any dimension |

---

## roadmap.md Body Template

This template defines the body structure for the generated roadmap.md (follows the YAML frontmatter). All sections are required.

```markdown
# Roadmap: <Project Title>

## Overview
<1-3 paragraph summary of the roadmap scope, approach, and key decisions made during planning>

## Milestone Summary

| ID | Title | Type | Priority | Effort | Dependencies | Deliverables | Risk |
|----|-------|------|----------|--------|--------------|--------------|------|
| M1 | <title> | FEATURE | P0 | S | None | 3 | Low |
| M2 | <title> | SECURITY | P1 | M | M1 | 5 | Medium |
| ... | | | | | | | |

## Dependency Graph
<Textual representation of milestone dependencies using arrow notation>
<Example: M1 → M2 → M4, M1 → M3 → M4, M5 (independent)>

---

## M1: <Milestone Title>

### Objective
<1-2 sentence clear milestone goal>

### Deliverables
| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D1.1 | <deliverable> | <measurable outcome> |
| D1.2 | <deliverable> | <measurable outcome> |

### Dependencies
- None (first milestone) OR
- M{N}: <what is needed from that milestone>

### Risk Assessment
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| <risk> | Low/Medium/High | Low/Medium/High | <mitigation> |

---

## M2: <Milestone Title>
[Same structure as M1]

---
[Repeat for all milestones]

---

## Risk Register

| ID | Risk | Affected Milestones | Probability | Impact | Mitigation | Owner |
|----|------|---------------------|-------------|--------|------------|-------|
| R-001 | <risk> | M1, M3 | Medium | High | <mitigation> | <persona> |
| R-002 | <risk> | M2 | Low | Medium | <mitigation> | <persona> |

## Decision Summary

Records key decisions made during roadmap generation for auditability and downstream context. **Every row must cite the specific data point that drove the decision — no subjective justifications.**

| Decision | Chosen | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Primary Persona | <persona> | <other candidates with confidence scores> | <highest domain % or --persona override> |
| Template | <template-name or "inline"> | <other templates with compatibility scores> | <best match score or fallback reason> |
| Milestone Count | <N> | <range considered> | <complexity class → count formula result> |
| Adversarial Mode | <mode or "none"> | N/A | <flags present or absent> |
| Adversarial Base Variant | <model:persona or "N/A"> | <other variants with scores> | <highest convergence contribution> |

## Success Criteria
<Derived from spec success criteria in extraction.md, mapped to milestones>

| ID | Criterion | Validates Milestone(s) | Measurable |
|----|-----------|----------------------|------------|
| SC-001 | <criterion> | M1, M2 | Yes |
| SC-002 | <criterion> | M3 | Yes |
```

---

## test-strategy.md Body Template

This template defines the body structure for test-strategy.md (follows the YAML frontmatter). Generated AFTER roadmap.md is complete (sequencing constraint). All sections are required.

```markdown
# Test Strategy: Continuous Parallel Validation

## Validation Philosophy

This test strategy implements **continuous parallel validation** — the assumption that work has deviated from the plan, is incomplete, or contains errors until validation proves otherwise.

**Core Principles**:
1. A validation agent runs in parallel behind the work agent, checking completed work against requirements
2. Major issues trigger a stop — work pauses for refactor/fix before continuing
3. Validation milestones are interleaved between work milestones (not batched at the end)
4. Minor issues are logged and addressed in the next validation pass
5. The interleave ratio is <ratio> (one validation milestone per <N> work milestones), derived from complexity class <class>

## Validation Milestones

| ID | After Work Milestone | Validates | Stop Criteria |
|----|---------------------|-----------|---------------|
| V1 | M<N> (<title>) | <what is validated> | <specific stop condition> |
| V2 | M<N> (<title>) | <what is validated> | <specific stop condition> |
| ... | | | |

**Placement rule**: Validation milestones are placed after every <N> work milestones per the interleave ratio. Each validation milestone references the specific work milestones it validates by M# ID.

## Issue Classification

| Severity | Action | Threshold | Example |
|----------|--------|-----------|---------|
| Critical | Stop work immediately, fix before any further progress | Any occurrence | Breaking dependency, security flaw, data loss risk |
| Major | Stop work, refactor/fix before next milestone | >1 occurrence OR blocking | Missing core requirement, broken integration point |
| Minor | Log, address in next validation pass | Accumulated count > 5 triggers review | Documentation gap, style inconsistency, minor tech debt |
| Info | Log only, no action required | N/A | Optimization opportunity, alternative approach noted |

## Acceptance Gates

Per-milestone acceptance criteria derived from spec requirements and mapped to deliverables.

| Milestone | Gate Criteria | Pass Condition |
|-----------|--------------|----------------|
| M<N> | <specific criteria from deliverable ACs> | All deliverable ACs met, no Critical/Major issues |
| M<N> | <specific criteria> | <specific condition> |

## Validation Coverage Matrix

| Requirement | Validated By | Milestone | Method |
|-------------|-------------|-----------|--------|
| FR-001 | V1 | M<N> | <how validated> |
| FR-002 | V2 | M<N> | <how validated> |
| NFR-001 | V<N> | M<N> | <how validated> |
```

---

## YAML Frontmatter Schemas

All 3 output artifacts include YAML frontmatter as a versioned contract for downstream consumption. **Fields may be added but never removed or renamed** (contract stability per NFR-003).

### Mutual Exclusion Rule

**Exactly one** of `spec_source` or `spec_sources` must be present in each artifact's frontmatter:

- **Single-spec mode**: `spec_source: <path>` (scalar string)
- **Multi-spec mode**: `spec_sources: [<path1>, <path2>, ...]` (list)
- Never include both fields. Never omit both fields.

### roadmap.md Frontmatter

```yaml
---
spec_source: <path-to-source-spec>                  # Single-spec mode (scalar)
# OR
spec_sources: [<path1>, <path2>]                     # Multi-spec mode (list)
generated: <ISO-8601 timestamp>                      # e.g., 2026-02-22T14:30:00Z
generator: sc:roadmap
complexity_score: <0.0-1.0>
complexity_class: <LOW|MEDIUM|HIGH>
domain_distribution:
  frontend: <percentage>
  backend: <percentage>
  security: <percentage>
  performance: <percentage>
  documentation: <percentage>
primary_persona: <persona-name>
consulting_personas: [<persona1>, <persona2>]
milestone_count: <N>
milestone_index:
  - id: M1
    title: <title>
    type: <FEATURE|IMPROVEMENT|DOC|TEST|MIGRATION|SECURITY>
    priority: <P0|P1|P2|P3>
    dependencies: []                                 # Empty list for M1
    deliverable_count: <N>
    risk_level: <Low|Medium|High>
  - id: M2
    title: <title>
    type: <type>
    priority: <priority>
    dependencies: [M1]
    deliverable_count: <N>
    risk_level: <level>
total_deliverables: <N>
total_risks: <N>
estimated_phases: <N>                                # Hint for future tasklist generator
validation_score: <0.0-1.0>                          # From Wave 4 (0.0 if --no-validate)
validation_status: <PASS|REVISE|REJECT|PASS_WITH_WARNINGS|SKIPPED>
adversarial:                                         # Present ONLY if adversarial mode used
  mode: <multi-spec|multi-roadmap|combined>
  agents: [<agent-spec-1>, <agent-spec-2>]
  convergence_score: <0.0-1.0>
  base_variant: <model:persona>
  artifacts_dir: <path-to-adversarial-artifacts>
---
```

### extraction.md Frontmatter

```yaml
---
spec_source: <path>                                  # Single-spec mode
# OR
spec_sources: [<path1>, <path2>]                     # Multi-spec mode
generated: <ISO-8601 timestamp>
generator: sc:roadmap
functional_requirements: <count>
nonfunctional_requirements: <count>
total_requirements: <count>                          # FR + NFR
domains_detected: [<domain1>, <domain2>]
complexity_score: <0.0-1.0>
complexity_class: <LOW|MEDIUM|HIGH>
risks_identified: <count>
dependencies_identified: <count>
success_criteria_count: <count>
extraction_mode: <standard|chunked>                  # "chunked (N chunks)" if chunked
pipeline_diagnostics:
  prereq_checks:
    spec_validated: true                               # Wave 0: spec file(s) exist and readable
    output_collision_resolved: false                    # Wave 0: collision suffix applied
    adversarial_skill_present: true|na                  # Wave 0: sc:adversarial SKILL.md exists (na if not needed)
    tier1_templates_found: 0                            # Wave 2: inference-only counter for non-canonical multi-tier discovery; CLI single-template resolver always emits 0 (see B-5)
  contract_validation:                                  # Present only if adversarial mode used; omit if not
    fields_received: 9                                  # Count of non-null fields in return contract
    fields_defaulted: []                                # List of field names where consumer defaults applied
    convergence_score: 0.72                             # Raw score from return contract
    routing_decision: pass|partial|fail                 # Threshold decision applied
    file_guard_passed: true                             # merged_output_path verified on disk
  fallback_activated: false                             # Any fallback protocol (F1-F5) triggered
---
```

### test-strategy.md Frontmatter

```yaml
---
spec_source: <path>                                  # Single-spec mode
# OR
spec_sources: [<path1>, <path2>]                     # Multi-spec mode
generated: <ISO-8601 timestamp>
generator: sc:roadmap
validation_philosophy: continuous-parallel
validation_milestones: <count>                       # Number of V# milestones
work_milestones: <count>                             # Number of M# work milestones
interleave_ratio: "<validation>:<work>"              # e.g., "1:2" for MEDIUM complexity
major_issue_policy: stop-and-fix
complexity_class: <LOW|MEDIUM|HIGH>
---
```

---

*Reference document for sc:roadmap v2.0.0 — loaded on-demand during Wave 2, available through Wave 3. CLI parity baseline: single-template resolver via `get_template_path()` over `ROADMAP_TEMPLATE = "roadmap_template.compressed.md"` (`src/superclaude/cli/roadmap/templates.py:14-71`). Multi-tier discovery is inference-only and out of canonical CLI scope (B-5).*
