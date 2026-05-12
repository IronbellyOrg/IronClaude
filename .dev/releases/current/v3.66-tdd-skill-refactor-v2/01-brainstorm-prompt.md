# TDD Skill Refactoring — Brainstorm Prompt

> **Usage**: Run this as `/sc:brainstorm --seq --ultrathink` with the content below as your input.

---

## Brainstorm Request

Perform a deep architectural analysis of the TDD skill at `.claude/skills/tdd/SKILL.md` (438 lines) and design the thin command layer required by the mandatory three-tier architecture (Command → Skill → Agents with refs/).

### Context

The TDD skill's refs/ decomposition is COMPLETE — SKILL.md is 438 lines (under the 500-line ceiling) with 5 refs/ files. However, the skill has NO command file at `commands/sc/tdd.md`, violating the Developer Guide's three-tier mandate: "Every skill MUST have a command in front of it."

This is the SAME gap identified in the PRD skill brainstorm analysis (Dimension 1 and Dimension 6). The PRD brainstorm and resulting spec v2 are reference materials for this analysis.

Read these files before beginning analysis:

1. **The TDD skill** — `.claude/skills/tdd/SKILL.md` (all 438 lines)
2. **The TDD refs/** — list all files in `.claude/skills/tdd/refs/` (5 files: agent-prompts.md, build-request-template.md, operational-guidance.md, synthesis-mapping.md, validation-checklists.md)
3. **The Developer Guide** — `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (focus on: Three-Tier Architecture, Activation Pattern, Section 5.10 Skill-Authoring Checklist, Section 9.3 Skill Design, Section 9.7 Anti-Patterns)
4. **The adversarial command** — `.claude/commands/sc/adversarial.md` (167 lines — the gold-standard thin command layer)
5. **The PRD brainstorm output** — `.dev/releases/backlog/prd-skill-refactor/02-brainstorm-output.md` (Dimension 1 analysis for PRD command — use as template for TDD command design)
6. **The PRD spec v2** — `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec-v2.md` (FR-PRD-R.0 for command file — use as pattern for TDD spec)
7. **The existing TDD refactor spec** — `.dev/releases/complete/v3.65-tdd-skill-refactor/tdd-refactor-spec.md` (current spec — covers refs/ decomposition but MISSES the thin command layer)
8. **The TDD fidelity index** — `.dev/releases/complete/v3.65-tdd-skill-refactor/fidelity-index.md`

### Analysis Dimensions

Brainstorm across these five dimensions. For each, generate multiple options, assess trade-offs, and recommend a path.

#### Dimension 1: Thin Command Layer Design

The TDD skill has NO command file. Design `commands/sc/tdd.md`:

- What flags/options does the TDD skill support? (Scan SKILL.md for: input parameters, tier selection, PRD reference, output paths, resume capability)
- What goes in Usage examples? (Map the "Effective Prompt Examples" from SKILL.md Input section — lines 48-63)
- What goes in Boundaries (Will/Will Not)? (Extract from the skill's behavioral scope)
- What belongs in the command's Behavioral Summary vs what stays in the skill?
- How does the Activation section hand off? (`Skill tdd` — naming convention analysis)
- Should there be explicit flags for:
  - `--tier lightweight|standard|heavyweight` (tier selection)?
  - `--prd <path>` (PRD reference)?
  - `--resume` (resume from existing task file)?
  - `--output <path>` (output location)?
  - `--focus <dirs>` (directories to focus on)?
  - `--from-prd` (explicit PRD-to-TDD translation mode)?

#### Dimension 2: Content Migration from SKILL.md to Command

Since SKILL.md is already 438 lines (under 500), the question is ONLY about moving interface content to the command:

- **Input section** (lines 33-76) — "Effective Prompt Examples" (lines 48-63) and "What to Do If Prompt Is Incomplete" template (lines 65-76) — which are user-facing interface concerns
- **Tier Selection table** (lines 80-94) — user-facing option documentation for the `--tier` flag

For each: should it move to the command, stay in the skill, or appear in both? Note: unlike PRD, moving content from SKILL.md is OPTIONAL since it's already under 500 lines. The question is about architectural correctness, not line budget.

#### Dimension 3: Naming Convention

Analyze whether the skill directory should remain `tdd/` or be renamed:
- `tdd/` (current — standalone utility, no `sc-` prefix)
- `sc-tdd-protocol/` (matches `sc-adversarial-protocol/` pattern)
- Keep `tdd/` (matches PRD brainstorm recommendation)

#### Dimension 4: What Changes in the Existing Spec

The existing TDD refactor spec at `.dev/releases/complete/v3.65-tdd-skill-refactor/tdd-refactor-spec.md` was written WITHOUT the thin command layer. Identify:

- Which functional requirements need addition? (New FR for the command file?)
- Which acceptance criteria need updating? (SKILL.md line count if content moves?)
- What new tests are needed? (Command activation test, flag parsing, boundary check)
- Does the architecture section need the three-tier dependency graph?
- Does the fidelity index need updates?

#### Dimension 5: Complexity & Risk Rating

Rate the command-layer addition:

**Complexity** (0.0-1.0):
- How many new files are created? (1 — the command file)
- Is there any behavioral change risk? (No — additive only)
- How much content migrates? (Optional ~22 lines if we follow PRD pattern)

**Risk** (Low/Medium/High):
- Content loss risk (if migrating prompt examples)
- Regression risk (zero — command is additive)
- Scope creep (temptation to also improve TDD skill content)

**Effort estimate**:
- Estimated lines for command file
- Can this be done in a single session?
- What's the implementation order?

### Output Format

For each dimension, produce:

1. **Options** — 2-4 distinct approaches with trade-offs
2. **Recommendation** — Your pick with rationale
3. **Confidence** — How confident you are (High/Medium/Low) and what would raise it
4. **Impact on existing spec** — What changes in the current TDD refactor spec if this recommendation is adopted

End with a **Consolidated Recommendation** section synthesizing all five dimensions into a single coherent plan, and a **Complexity/Risk Scorecard** with final ratings.

Then produce a **Draft Revised Spec** section containing a complete release spec for the TDD command-layer addition, following the template at `src/superclaude/examples/release-spec-template.md`. This should be modeled after the PRD spec v2's FR-PRD-R.0 and FR-PRD-R.8, adapted for TDD-specific flags and content.
