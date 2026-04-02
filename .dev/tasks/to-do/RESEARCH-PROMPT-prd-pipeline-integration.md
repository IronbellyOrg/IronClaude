# Tech Research: PRD as Supplementary Pipeline Input

## WHAT to investigate

Investigate how to add the PRD (Product Requirements Document) as a **supplementary input** to the roadmap and tasklist CLI pipelines — following the exact pattern established by the TDD integration work on branch `feat/tdd-spec-merge`.

The TDD was recently integrated as a first-class input to the roadmap pipeline (`--input-type auto|tdd|spec`) and as supplementary validation context to the tasklist pipeline (`--tdd-file`). That work revealed that the pipeline's extraction step is the critical chokepoint — content not captured there is permanently lost downstream.

The PRD carries business and product context that is systematically filtered out during TDD authoring. The TDD skill's PRD extraction agent only extracts 5 of ~28 PRD sections (epics, user stories + ACs, success metrics, technical requirements, scope boundaries). Additionally, 5 of 9 TDD synthesis files never read the PRD extraction at all. The roadmap extraction pipeline has zero steps for business rationale, personas, stakeholder needs, market context, or product-level success metrics.

This means the following PRD content is lost in the current PRD -> TDD -> roadmap path and would benefit the pipeline as supplementary input:

- **Business rationale / strategic fit / "why now"** — informs roadmap prioritization and phasing
- **User personas and stakeholder segments** — shapes acceptance criteria completeness
- **Jobs To Be Done (JTBD)** — grounds roadmap phases in user outcomes
- **Success metrics in original business form** — before TDD converts them to engineering proxies
- **Scope boundaries with rationale** — prevents scope creep during phased planning
- **Compliance / legal / policy constraints** — ensures roadmap accounts for regulatory work
- **Customer journey / UX-critical flows** — identifies user-facing validation requirements
- **Product edge cases and error scenarios** — drives test strategy completeness

The PRD is NOT a replacement for the TDD as primary input. The TDD remains the engineering driver. The PRD is supplementary enrichment that provides product-level grounding to roadmap and tasklist output.

## WHY / what problem to solve

The roadmap pipeline currently produces implementation-oriented output that can be technically faithful to the TDD but product-wrong — missing business justification, user context, and outcome alignment. A roadmap that phases work purely by technical dependency without considering user value, stakeholder needs, or business priority is less useful for planning.

We want roadmap output that retains product-level intent alongside engineering structure. Feeding the PRD directly gives the pipeline access to "what matters and why" (PRD) alongside "what exists and how to build it" (TDD).

This is lighter work than the TDD integration because:
- PRD is supplementary only, not a new `input_type` mode
- The pattern is already established (optional file flag, conditional prompt blocks, model field)
- No new extraction mode needed — PRD enriches existing extraction, not replaces it
- No gate redesign needed — PRD enhances fidelity report content, not gate logic

The investigation should produce a concrete implementation plan that can be executed as a single task file.

## WHERE to look

### Primary investigation targets (CLI layer)

These are the files that will need changes, mirroring exactly what the TDD integration touched:

**Roadmap CLI:**
- `src/superclaude/cli/roadmap/commands.py` — add `--prd-file` flag (pattern: how `--input-type` and `--retrospective` were added)
- `src/superclaude/cli/roadmap/models.py` — add `prd_file: Path | None = None` to `RoadmapConfig` (pattern: how `tdd_file` and `input_type` were added)
- `src/superclaude/cli/roadmap/executor.py` — wire `prd_file` into step inputs conditionally (pattern: how `detect_input_type()` and TDD extraction branching work)
- `src/superclaude/cli/roadmap/prompts.py` — add supplementary PRD blocks to prompt builders (pattern: how `build_extract_prompt_tdd()` and TDD-aware fidelity dimensions were added)
- `src/superclaude/cli/roadmap/gates.py` — document PRD compatibility, no structural gate changes expected

**Tasklist CLI:**
- `src/superclaude/cli/tasklist/commands.py` — add `--prd-file` flag (pattern: how `--tdd-file` was added)
- `src/superclaude/cli/tasklist/models.py` — add `prd_file: Path | None = None` (pattern: how `tdd_file` was added)
- `src/superclaude/cli/tasklist/executor.py` — wire `prd_file` into validation inputs (pattern: how `tdd_file` is wired)
- `src/superclaude/cli/tasklist/prompts.py` — add supplementary PRD validation block (pattern: how TDD supplementary validation was added to `build_tasklist_fidelity_prompt()`)

### Secondary investigation targets (skill/reference layer)

These encode the protocol-level behavior that Claude follows during roadmap/tasklist generation:

- `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` — add conditional PRD-supplementary extraction steps (pattern: how TDD-conditional steps 9-15 were added)
- `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` — add PRD-derived scoring factors if applicable (pattern: how TDD detection rule and 7-factor formula were added)
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — document PRD supplementary context usage (pattern: how TDD supplementary context was documented)
- `src/superclaude/commands/spec-panel.md` — check if PRD-aware behavior is needed for spec-panel

### Reference materials (read-only, for context)

- `src/superclaude/skills/prd/SKILL.md` — understand full PRD structure, identify which sections are most pipeline-relevant
- `src/superclaude/examples/tdd_template.md` — understand what PRD content the TDD template can hold vs. what it drops
- `src/superclaude/skills/tdd/SKILL.md` — understand the PRD extraction agent (lines ~944-978) to see exactly what is kept vs. lost

### Prior research (verified findings to build on, not re-investigate)

These reports contain verified findings from the TDD integration research. The PRD investigation should reference them as established context, not re-audit the same ground:

- `.dev/tasks/to-do/TASK-RESEARCH-20260324-001/RESEARCH-REPORT-prd-tdd-spec-pipeline.md` — architecture-level findings on PRD/TDD/spec pipeline gaps
- `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/RESEARCH-REPORT-cli-tdd-integration.md` — CLI-level findings on executor, prompts, gates, modules
- `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/TASK-RF-20260325-cli-tdd.md` — implementation task structure to use as template
- `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/reports/final-integration-report.md` — what was completed and what was deferred

## WHAT kind of output you need

**Output type: Implementation plan**

The research report should produce:

1. **Verified current state** — confirm what each target file currently does and where PRD content would slot in (much of this is already known from TDD research, so this should be a lightweight verification pass, not a deep re-audit)

2. **PRD content value mapping** — for each pipeline touchpoint (extraction, generate, diff/debate/score/merge, test-strategy, spec-fidelity, tasklist-fidelity), specify:
   - What PRD sections provide value
   - What supplementary prompt text to add
   - What new extraction/fidelity dimensions to include
   - How PRD and TDD supplementary inputs interact when both are provided

3. **Implementation plan** — specific file changes organized by phase, following the TDD implementation task structure:
   - Phase 1: Config/CLI layer (`--prd-file` flag, model field)
   - Phase 2: Executor wiring (conditional inclusion in step inputs)
   - Phase 3: Extraction prompt enrichment (supplementary PRD context block)
   - Phase 4: Generate prompt enrichment (PRD-aware prioritization instructions)
   - Phase 5: Fidelity prompt enrichment (PRD comparison dimensions)
   - Phase 6: Test-strategy prompt enrichment (persona/KPI/journey-based validation)
   - Phase 7: Tasklist supplementary PRD validation (mirror TDD pattern)
   - Phase 8: Skill/reference layer updates (extraction-pipeline.md, scoring.md, SKILL.md)
   - Phase 9: Integration testing and verification

4. **Interaction model** — how `--prd-file` and `--tdd-file` work together:
   - When only PRD is provided (no TDD)
   - When only TDD is provided (no PRD) — existing behavior, no change
   - When both PRD and TDD are provided — combined enrichment
   - When neither is provided — existing behavior, no change

5. **Risk assessment** — what could go wrong, what's deferred, what needs follow-up

### Mandatory requirements (added post-E2E-testing, 2026-03-27)

These 4 items MUST be included in the implementation plan. They were identified during E2E testing and user review of the TDD integration work:

1. **Fix dead `tdd_file` in roadmap pipeline** — `RoadmapConfig.tdd_file` (models.py:115) exists but has no `--tdd-file` CLI flag in `roadmap/commands.py` and zero references in `roadmap/executor.py`. It's fully wired in tasklist but dead in roadmap. Wire it end-to-end alongside `prd_file` for consistent treatment. Add redundancy guard: when primary input IS a TDD, `--tdd-file` is redundant and should warn/ignore.

2. **Auto-wire supplementary files from `.roadmap-state.json`** — When the tasklist pipeline reads a roadmap output directory, it should auto-detect the source TDD and/or PRD files from `.roadmap-state.json` without requiring the user to re-pass `--tdd-file` and `--prd-file`. Store `tdd_file` and `prd_file` in the state file during roadmap runs. Read them back in tasklist. Explicit CLI flags override auto-wired values.

3. **Auto-wire `prd_file` via the same state file mechanism** — Same pattern as #2 for `prd_file`. Both supplementary file types get stored and auto-wired consistently.

4. **Enrich tasklist GENERATION (not just validation) with TDD/PRD content** — Currently `--tdd-file` only enriches tasklist validation (post-hoc checking). The tasklist *generator* still only reads `roadmap.md`, which loses TDD-specific detail (test cases, API schemas, component props, rollback procedures) and PRD context (personas, metrics, journeys). The full source documents should be read during generation to produce richer task decomposition. This applies to BOTH CLI (`tasklist generate` prompt builder) AND skills (`sc-tasklist-protocol/SKILL.md` generation protocol sections).

### Design constraints for the implementation plan

- PRD is **supplementary only** — no new `--input-type prd` mode, no `detect_input_type()` changes, no `build_extract_prompt_prd()`. PRD content enriches existing extraction, it does not replace it.
- Follow the **exact TDD integration pattern**: optional `Path | None` field, CLI flag, conditional prompt block appended only when file is present.
- **Backward compatible** — zero behavior change when `--prd-file` is not provided.
- PRD content in prompts should be clearly labeled as **"product context for planning enrichment"** not "implementation requirements" — the LLM should use it to inform prioritization, scope, and validation, not treat narrative business sections as direct engineering work items.
- Prompt additions should be **concise supplementary blocks**, not full prompt rewrites. The PRD is context, not the primary input.
