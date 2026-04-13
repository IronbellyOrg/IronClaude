# PRD Skill Refactoring — Master Prompt for /skill-creator

> **Purpose**: This prompt drives the `/skill-creator` pipeline to deeply analyze the monolithic PRD skill and produce a comprehensive release spec for its refactoring into a best-practice-aligned, multi-file skill architecture.
>
> **Output**: A release spec at `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec.md` using the template at `src/superclaude/examples/release-spec-template.md`
>
> **Constraint**: The PRD skill's pipeline logic, strategy, agent prompts, validation checklists, and all instructional content MUST be preserved word-for-word. This is an architectural refactoring, NOT a content rewrite.

---

## Context for /skill-creator

I have an existing skill at `.claude/skills/prd/SKILL.md` (1,373 lines) that needs to be refactored from a monolithic single-file skill into a properly architected multi-file skill that follows SuperClaude best practices.

### Reference Architecture

The Developer Guide at `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` defines the three-tier architecture (Command → Skill → Agents) and the following critical patterns:

1. **SKILL.md stays under ~500 lines** — behavioral intent only (WHAT and WHEN)
2. **refs/ directory** — algorithms, formulas, prompts, templates (HOW) — loaded per wave on demand
3. **Lazy loading** — SKILL.md declares when to load each ref; at most 2-3 refs loaded at any point
4. **Token budget**: Skill name+desc ~50 tokens at session start; full SKILL.md ~2000 tokens on invocation; each ref ~500-1500 tokens per wave
5. **Extended metadata comment** for documentation (category, complexity, mcp-servers, personas)
6. **Input/output contracts** with STOP/WARN conditions
7. **Will Do / Will Not Do** boundaries
8. **sc- prefix convention** for command-backing skills

### Reference Implementation: sc-adversarial-protocol

The adversarial skill is the gold-standard example of a properly decomposed complex pipeline:

```
sc-adversarial-protocol/
  SKILL.md              (2,935 lines — protocol, but uses refs/ for HOW details)
  refs/
    agent-specs.md      (229 lines — agent specification format and templates)
    artifact-templates.md (378 lines — output artifact templates)
    debate-protocol.md  (258 lines — detailed debate rules)
    scoring-protocol.md (230 lines — hybrid scoring algorithm)
```

**Pattern**: The SKILL.md contains the behavioral protocol and flow, while the `refs/` files contain the detailed HOW content that gets loaded per-wave.

### Current PRD Skill Problems

The current `prd/SKILL.md` at 1,373 lines is monolithic. It contains:
- Stage A scope discovery protocol (~330 lines)
- Stage B execution delegation (~30 lines)
- Full agent prompt templates: Codebase Research (~140 lines), Web Research (~40 lines), Synthesis (~35 lines), Research Analyst (~40 lines), Research QA (~50 lines), Synthesis QA (~40 lines), Report Validation QA (~50 lines), Assembly (~70 lines)
- Synthesis Mapping Table (~20 lines)
- Synthesis Quality Review Checklist (~30 lines)
- Assembly Process steps (~65 lines)
- Validation Checklist (~55 lines)
- Output Structure reference (~115 lines)
- Content Rules (~15 lines)
- Tier Selection (~20 lines)
- Input specification (~75 lines)

All loaded into context simultaneously — wasting tokens on sections only needed during specific phases.

---

## Your Task: Analyze & Produce a Release Spec

**DO NOT modify any files.** Your job is analysis and spec creation only.

### Phase 1: Deep Analysis (READ-ONLY)

Read and deeply analyze these files to understand the full picture:

1. **The PRD skill** — `.claude/skills/prd/SKILL.md` (read the ENTIRE file, all 1,373 lines)
2. **The Developer Guide** — `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (focus on Sections 5 Skills Deep Dive, 6 Multi-Phase Architecture, 9 Best Practices)
3. **The adversarial protocol** — `.claude/skills/sc-adversarial-protocol/SKILL.md` (read first 200 lines for structural pattern), plus ALL files in `.claude/skills/sc-adversarial-protocol/refs/` (for the refs/ decomposition pattern)
4. **The release spec template** — `src/superclaude/examples/release-spec-template.md`

During analysis, build an inventory of:

**A. Content Blocks** — Every discrete logical block in the PRD SKILL.md:
- Exact line ranges (start-end)
- Block purpose (behavioral protocol vs reference detail vs agent prompt vs validation checklist)
- Which execution phase needs this block (Stage A, Phase 1, Phase 2, Phase 3, Phase 4, Phase 5, Phase 6, Phase 7)
- Whether it's WHAT/WHEN (stays in SKILL.md) or HOW (moves to refs/)

**B. Cross-Reference Map** — Every place in SKILL.md that references another block:
- The BUILD_REQUEST references to "Agent Prompt Templates section", "Synthesis Mapping Table section", "Assembly Process section", "Validation Checklist section", "Content Rules section", "Tier Selection section"
- Phase-to-block dependencies

**C. Fidelity Inventory** — A word-for-word preservation manifest:
- Every agent prompt template (exact content that MUST be preserved verbatim)
- Every numbered checklist (exact items and numbering)
- Every validation criterion
- Every content rule
- Every table structure

### Phase 2: Architectural Design

Design the decomposed file structure. The refactored skill MUST:

1. **Keep SKILL.md under 500 lines** containing:
   - Frontmatter with proper fields
   - Extended metadata comment
   - Purpose and Input sections
   - Tier Selection (brief — needed for initial invocation)
   - Stage A protocol (scope discovery + task file creation) — this IS behavioral flow
   - Stage B delegation protocol (brief — just the delegation to /task)
   - Will Do / Will Not Do boundaries
   - Explicit refs/ loading declarations per phase

2. **Move HOW content to refs/** with clear per-wave loading:
   - `refs/agent-prompts.md` — All 8 agent prompt templates (Codebase Research, Web Research, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly)
   - `refs/validation-checklists.md` — All validation checklists (18-item validation, 9-item synthesis quality, content quality checks)
   - `refs/synthesis-mapping.md` — Synthesis Mapping Table + Output Structure
   - `refs/build-request-template.md` — The complete BUILD_REQUEST format (the largest single block, currently embedded in A.7)

3. **Preserve every word** of instructional content — agent prompts, checklists, rules, tables move verbatim; only their location changes

4. **Add explicit loading instructions** in SKILL.md:
   ```
   ## Stage A Phase A.7: Build Task File
   Load `refs/agent-prompts.md` and `refs/build-request-template.md` before spawning the builder.
   ```

### Phase 3: Release Spec Generation

Produce the release spec at `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec.md` using the template at `src/superclaude/examples/release-spec-template.md`.

**Spec metadata:**
- `spec_type: refactoring`
- `feature_id: FR-PRD-REFACTOR`
- `target_release: v3.8`
- `complexity_class: MEDIUM`

**Populate ALL sections including:**

**Section 1 (Problem Statement):**
- The 1,373-line monolithic skill wastes ~5,000+ tokens loading content only needed in specific phases
- Violates the Developer Guide's 500-line SKILL.md guidance
- No lazy-loading of reference material
- Inconsistent with the pattern established by sc-adversarial-protocol

**Section 2 (Solution Overview):**
- Decompose into SKILL.md (~400-500 lines) + refs/ directory (4 files)
- Preserve all pipeline logic, agent prompts, validation checklists word-for-word
- Add per-wave loading declarations
- Maintain Stage A / Stage B execution flow

**Section 3 (Functional Requirements):**
- FR-PRD-R.1: Decomposed SKILL.md under 500 lines with behavioral protocol only
- FR-PRD-R.2: refs/agent-prompts.md with all 8 agent templates (word-for-word)
- FR-PRD-R.3: refs/validation-checklists.md with all checklists (word-for-word)
- FR-PRD-R.4: refs/synthesis-mapping.md with mapping table + output structure (word-for-word)
- FR-PRD-R.5: refs/build-request-template.md with BUILD_REQUEST format (word-for-word)
- FR-PRD-R.6: Explicit per-phase loading declarations in SKILL.md
- FR-PRD-R.7: Fidelity verification — zero content loss, zero semantic drift

**Section 4 (Architecture):**
- New files: 4 refs/ files with exact line counts and content mapping
- Modified files: SKILL.md (reduced from 1,373 to ~400-500 lines)
- Removed files: None (content moves, nothing deleted)
- Include file-by-file content mapping with source line ranges → destination file

**Section 5 (Interface Contracts):**
- Phase contracts showing which refs/ file loads at which phase
- Loading budget: max 2 refs loaded at any phase

**Section 7 (Risk Assessment):**
- Risk: Content loss during decomposition → Mitigation: word-for-word fidelity audit
- Risk: Cross-reference breakage (BUILD_REQUEST references) → Mitigation: ref path update verification
- Risk: Loading order wrong → Mitigation: phase-to-ref dependency matrix

**Section 8 (Test Plan):**
- Fidelity audit: diff every agent prompt, checklist, and table against original
- Structural test: SKILL.md line count < 500
- Loading test: each phase's referenced refs/ file exists
- Token budget test: no phase loads more than 2 refs simultaneously
- Functional test: invoke the refactored skill end-to-end on a test product

**Section 9 (Migration & Rollout):**
- No breaking changes — the skill's external interface is unchanged
- Rollback: revert to the monolithic SKILL.md (preserved in git)
- Migration: single commit, `make sync-dev` to propagate

**Section 12 (Gap Analysis):**
- Include the content block inventory from Phase 1 as an appendix
- Include the cross-reference map showing BUILD_REQUEST → refs/ path updates
- Include the fidelity manifest listing every verbatim block with its source and destination

### Critical Quality Requirements

1. **ZERO placeholder sentinels** — every `{{SC_PLACEHOLDER:*}}` must be replaced with actual content
2. **ZERO content loss** — every line of instructional content from the original must appear in the spec's file mapping
3. **Word-for-word fidelity** — agent prompts, checklists, validation criteria, content rules appear EXACTLY as in the original
4. **Architectural consistency** — the decomposition follows the same pattern as sc-adversarial-protocol
5. **The spec is the source of truth** — an implementer should be able to execute the refactoring from this spec alone without reading the original SKILL.md

---

## Output

Write the completed release spec to: `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec.md`

Also write a fidelity index to: `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` containing:
- Every content block from the original with its line range
- The destination file in the refactored structure
- A checksum-style marker (first 10 words + last 10 words of each block) for verification

When complete, report: spec file path, fidelity index path, total line counts, and any gaps found.
