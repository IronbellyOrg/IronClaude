# PRD Skill Refactoring — Brainstorm Prompt

> **Usage**: Run this as `/sc:brainstorm --seq --ultrathink` with the content below as your input.

---

## Brainstorm Request

Perform a deep architectural analysis of the PRD skill at `.claude/skills/prd/SKILL.md` (1,373 lines) and design its refactoring into the mandatory three-tier architecture (Command → Skill → Agents with refs/).

### Context

Read these files before beginning analysis:

1. **The PRD skill** — `.claude/skills/prd/SKILL.md` (all 1,373 lines — read in chunks)
2. **The Developer Guide** — `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (focus on: Three-Tier Architecture, Activation Pattern, Section 5 Skills Deep Dive, Section 5.10 Skill-Authoring Checklist, Section 9.3 Skill Design, Section 9.7 Anti-Patterns)
3. **The adversarial command** — `.claude/commands/sc/adversarial.md` (167 lines — the gold-standard thin command layer)
4. **The adversarial protocol skill** — `.claude/skills/sc-adversarial-protocol/SKILL.md` (first 100 lines for structural pattern)
5. **The adversarial refs/** — all files in `.claude/skills/sc-adversarial-protocol/refs/` (for decomposition pattern)
6. **The existing spec** — `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec.md` (current refactoring spec — decomposed SKILL.md into refs/ but MISSED the thin command layer entirely)
7. **The fidelity index** — `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` (32 content blocks mapped)

### Analysis Dimensions

Brainstorm across these six dimensions. For each, generate multiple options, assess trade-offs, and recommend a path.

#### Dimension 1: Thin Command Layer Design

The current PRD skill has NO command file in front of it — it's a standalone skill invoked directly. The Developer Guide now mandates every skill has a thin command layer. Design `commands/sc/prd.md`:

- What flags/options does the PRD skill actually support? (Scan the SKILL.md for input parameters, tier selection, scenario A vs B, output paths)
- What goes in Usage examples? (Map the "Effective Prompt Examples" from SKILL.md Input section)
- What goes in Boundaries (Will/Will Not)? (Extract from the skill's behavioral scope)
- What belongs in the command's Behavioral Summary vs what stays in the skill?
- How does the Activation section hand off? (`Skill prd` or `Skill prd-protocol`? Naming convention analysis needed)
- Should there be explicit flags for tier selection (`--tier lightweight|standard|heavyweight`)?
- Should there be a `--resume` flag for resuming from an existing task file?

#### Dimension 2: Skill Body Decomposition 

The existing spec decomposes SKILL.md into SKILL.md (~430-480 lines) + 4 refs/ files. Validate or challenge:

- Is 4 refs files the right number? Should the BUILD_REQUEST be a separate ref or merged with agent-prompts?
- Are the groupings optimal? (agent-prompts.md has 8 templates at ~415 lines — should it split into codebase-prompts.md + qa-prompts.md?)
- The spec keeps Stage A (scope discovery, ~330 lines) entirely in SKILL.md. Is this correct? Stage A is behavioral protocol (WHAT/WHEN), but at 330 lines it dominates the 500-line budget. Should any of Stage A move to refs/?
- What content currently in SKILL.md should move to the command file instead? (Input section, Tier Selection table, Effective Prompt Examples)
- With the command file now handling interface concerns, does the SKILL.md line budget math still work? (Original: ~430-480 for SKILL.md, but now some content moves to command → SKILL.md could be even leaner)

#### Dimension 3: Naming Convention

Analyze the naming patterns across existing skills and recommend:

- `prd/SKILL.md` (current — standalone skill, no `sc-` prefix)
- `sc-prd-protocol/SKILL.md` (matches `sc-adversarial-protocol/` pattern)
- `prd-protocol/SKILL.md` (hybrid)
- What does the `sc-` prefix convention in Section 5.7 of the Developer Guide actually require?
- If we rename, what files need updating? (Spec, fidelity index, any cross-references)

#### Dimension 4: What Can Move to the Command Layer

The current SKILL.md contains content that belongs in a command file per the three-tier architecture:

- **Input section** (lines 33-73) — "Effective Prompt Examples", "What to Do If the Prompt Is Incomplete" — these are user-facing interface concerns
- **Tier Selection table** (lines 79-92) — user-facing option documentation
- **Output Locations table** (lines 95-126) — could be a brief summary in the command with full detail in SKILL.md

For each: should it move to the command, stay in the skill, or appear in both (brief in command, detailed in skill)?

#### Dimension 5: Complexity & Risk Rating

Rate the overall refactoring on these scales:

**Complexity** (0.0-1.0):
- How many files change?
- How many cross-references need updating?
- How complex is the content migration (word-for-word copy vs restructuring)?
- How many new files are created?
- Is there any behavioral change risk?

**Risk** (Low/Medium/High per category):
- Content loss risk — dropping words during migration
- Cross-reference breakage — BUILD_REQUEST still pointing to old locations
- Naming collision — `sc-prd-protocol` conflicting with existing conventions
- Regression risk — refactored skill behaving differently
- Scope creep — refactoring turning into a rewrite
- Fidelity drift — "improving" content instead of moving it verbatim

**Effort estimate**:
- How many files in the final state?
- Estimated total lines across all files?
- Can this be done in a single session?
- What's the optimal implementation order?

#### Dimension 6: Gaps in the Existing Spec

The spec at `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec.md` was written WITHOUT the thin command layer. Identify:

- Which functional requirements need revision? (FR-PRD-R.1 line counts change if content moves to command)
- Which acceptance criteria are invalidated?
- What new FRs are needed? (FR-PRD-R.0 for the command file?)
- Does the fidelity index need new block entries for content that moves to the command?
- Does the test plan need new tests? (command → skill activation test, flag parsing test)
- Does the architecture section need a new file in 4.1?

### Output Format

For each dimension, produce:

1. **Options** — 2-4 distinct approaches with trade-offs
2. **Recommendation** — Your pick with rationale
3. **Confidence** — How confident you are (High/Medium/Low) and what would raise it
4. **Impact on existing spec** — What changes in the current spec if this recommendation is adopted

End with a **Consolidated Recommendation** section that synthesizes all six dimensions into a single coherent refactoring plan, and a **Complexity/Risk Scorecard** with final ratings.
