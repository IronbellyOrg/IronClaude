# TDD Skill Refactoring — Master Prompt for /skill-creator

> **Purpose**: This prompt drives the `/skill-creator` pipeline to deeply analyze the monolithic TDD skill and produce a comprehensive release spec for its refactoring into a best-practice-aligned, multi-file skill architecture.
>
> **Output**: A release spec at `.dev/releases/backlog/tdd-skill-refactor/tdd-refactor-spec.md` using the template at `src/superclaude/examples/release-spec-template.md`
>
> **Constraint**: The TDD skill's pipeline logic, strategy, agent prompts, validation checklists, and all instructional content MUST be preserved word-for-word. This is an architectural refactoring, NOT a content rewrite.

---

## Context for /skill-creator

I have an existing skill at `.claude/skills/tdd/SKILL.md` (1,387 lines) that needs to be refactored from a monolithic single-file skill into a properly architected multi-file skill that follows SuperClaude best practices.

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

The adversarial skill is the example of a properly decomposed complex pipeline with protocol + refs structure.

**Pattern**: The SKILL.md contains the behavioral protocol and flow, while the `refs/` files contain detailed HOW content that gets loaded per-wave.

### Current TDD Skill Problems

The current `tdd/SKILL.md` at 1,387 lines is monolithic. It contains:
- Stage A scope discovery protocol
- Stage B execution delegation
- Full agent prompt templates: Codebase Research, Web Research, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly, PRD Extraction
- Synthesis Mapping Table
- Synthesis Quality Review Checklist
- Assembly Process steps
- Validation Checklist
- Output Structure reference
- Content Rules
- Tier Selection
- Input specification

All loaded into context simultaneously — wasting tokens on sections only needed during specific phases.

---

## Your Task: Analyze & Produce a Release Spec

**DO NOT modify any files.** Your job is analysis and spec creation only.

### Phase 1: Deep Analysis (READ-ONLY)

Read and deeply analyze these files to understand the full picture:

1. **The TDD skill** — `.claude/skills/tdd/SKILL.md` (read the ENTIRE file, all 1,387 lines)
2. **The Developer Guide** — `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (focus on Sections 5 Skills Deep Dive, 6 Multi-Phase Architecture, 9 Best Practices)
3. **The adversarial protocol** — `.claude/skills/sc-adversarial-protocol/SKILL.md`, plus any files under `.claude/skills/sc-adversarial-protocol/refs/` if present
4. **The release spec template** — `src/superclaude/examples/release-spec-template.md`
5. **The PRD refactor artifacts for pattern parity** —
   - `.dev/releases/backlog/prd-skill-refactor/00-master-prompt.md`
   - `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec.md`
   - `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`

During analysis, build an inventory of:

**A. Content Blocks** — Every discrete logical block in the TDD SKILL.md:
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
   - `refs/agent-prompts.md` — All agent prompt templates (word-for-word)
   - `refs/validation-checklists.md` — All validation checklists (word-for-word)
   - `refs/synthesis-mapping.md` — Synthesis Mapping Table + Output Structure (word-for-word)
   - `refs/build-request-template.md` — Complete BUILD_REQUEST format from Stage A.7 (word-for-word)
   - If needed for line-budget/fidelity, split further while preserving verbatim content and preserving cross-reference clarity

3. **Preserve every word** of instructional content — agent prompts, checklists, rules, tables move verbatim; only their location changes

4. **Add explicit loading instructions** in SKILL.md for each phase that consumes refs content

### Phase 3: Release Spec Generation

Produce the release spec at `.dev/releases/backlog/tdd-skill-refactor/tdd-refactor-spec.md` using the template at `src/superclaude/examples/release-spec-template.md`.

**Spec metadata:**
- `spec_type: refactoring`
- `feature_id: FR-TDD-REFACTOR`
- `target_release: v3.8`
- `complexity_class: MEDIUM`

**Populate ALL sections including:**

**Section 1 (Problem Statement):**
- The 1,387-line monolithic skill loads content only needed in specific phases
- Violates the Developer Guide's SKILL.md size and decomposition guidance
- No lazy-loading of reference material
- Inconsistent with modern command/skill/pipeline architecture expectations

**Section 2 (Solution Overview):**
- Decompose into SKILL.md (~400-500 lines) + refs/ directory
- Preserve all pipeline logic, agent prompts, validation checklists word-for-word
- Add per-wave loading declarations
- Maintain Stage A / Stage B execution flow and all quality-gate semantics

**Section 3 (Functional Requirements):**
- FR-TDD-R.1: Decomposed SKILL.md under 500 lines with behavioral protocol only
- FR-TDD-R.2: refs/agent-prompts.md with all agent templates (word-for-word)
- FR-TDD-R.3: refs/validation-checklists.md with all checklists (word-for-word)
- FR-TDD-R.4: refs/synthesis-mapping.md with mapping table + output structure (word-for-word)
- FR-TDD-R.5: refs/build-request-template.md with BUILD_REQUEST format (word-for-word)
- FR-TDD-R.6: Explicit per-phase loading declarations in SKILL.md
- FR-TDD-R.7: Fidelity verification — zero content loss, zero semantic drift

**Section 4 (Architecture):**
- New files: refs/ files with exact line counts and content mapping
- Modified files: SKILL.md (reduced from 1,387 to target range)
- Removed files: None (content moves, nothing deleted)
- Include file-by-file content mapping with source line ranges → destination file

**Section 5 (Interface Contracts):**
- Phase contracts showing which refs/ file loads at which phase
- Loading budget and ordering constraints

**Section 7 (Risk Assessment):**
- Risk: Content loss during decomposition → Mitigation: word-for-word fidelity audit
- Risk: Cross-reference breakage (BUILD_REQUEST references) → Mitigation: ref path update verification
- Risk: Loading order wrong → Mitigation: phase-to-ref dependency matrix
- Risk: Semantics drift in quality gates → Mitigation: checklist and prompt diff validation

**Section 8 (Test Plan):**
- Fidelity audit: diff every agent prompt, checklist, and table against original
- Structural test: SKILL.md line count under target
- Loading test: each phase's referenced refs/ file exists
- Functional parity test: stage and phase behavior preserved
- Command-level test: run /sc:spec-panel and reflection passes on resulting spec

**Section 9 (Migration & Rollout):**
- No breaking changes — skill interface unchanged
- Rollback: revert to monolithic SKILL.md from git
- Migration: staged refactor with validation gates

**Section 12 (Gap Analysis):**
- Include content block inventory from Phase 1 as appendix
- Include cross-reference map showing BUILD_REQUEST → refs/ path updates
- Include fidelity manifest listing every verbatim block with source and destination

### Critical Quality Requirements

1. **ZERO placeholder sentinels** — every `{{SC_PLACEHOLDER:*}}` must be replaced with actual content
2. **ZERO content loss** — every line of instructional content from the original must appear in the spec's file mapping
3. **Word-for-word fidelity** — agent prompts, checklists, validation criteria, content rules appear EXACTLY as in the original
4. **Architectural consistency** — decomposition aligns with best-practice command/skill/pipeline patterns
5. **Spec executability** — an implementer should be able to execute the refactoring from this spec alone

---

## Output

Write the completed release spec to: `.dev/releases/backlog/tdd-skill-refactor/tdd-refactor-spec.md`

Also write a fidelity index to: `.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md` containing:
- Every content block from the original with its line range
- The destination file in the refactored structure
- A checksum-style marker (first 10 words + last 10 words of each block) for verification

When complete, report: spec file path, fidelity index path, total line counts, and any gaps found.
