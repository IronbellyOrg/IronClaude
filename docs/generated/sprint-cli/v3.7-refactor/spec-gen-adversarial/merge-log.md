# Merge Log: Adversarial Spec-Gen Prompt Consolidation

> **Date**: 2026-04-03
> **Input**: 3 variants (Architect, QA, Incremental)
> **Output**: `merged-spec-gen-prompt.md`

---

## Overall Structure Decision

**Selected**: Variant C (Incremental) structure as the skeleton.

**Rationale**: C's flow (assignment -> sources -> decisions -> inventories -> requirements -> anti-patterns -> self-check) is the most logically organized. A reader encounters context before requirements, requirements before quality gates, and anti-patterns as a final guardrail. A's 4-part structure buries template compliance as a separate part. B's 11-step structure is linear but mixes concerns (Step 2 contains both standard FR fields and verification contracts).

**Adaptation**: C's 7 requirements were reorganized into a single "Per-Task Analysis Standard" section (Section 6) that consolidates all per-task obligations from all three variants into one place.

---

## What Was Taken From Each Variant

### From Variant A (Architect)

| Element | Merged Location | Notes |
|---------|----------------|-------|
| Deep code reading discipline (Part 2.1) | Section 6.1 | Preserved verbatim: read source, identify exact lines, grep callers, grep tests |
| Before/after code snippet requirement (Part 2.2) | Section 6.2 | Preserved as mandatory for every task |
| Impact analysis questions (Part 2.3) | Section 6.3 | Merged with C's grep-pattern requirement for verifiability |
| Multi-approach evaluation (Part 2.4) | Section 6.4 | Preserved with C's rejected-approach table format |
| Unintended consequence analysis (Part 2.5) | Section 6.5 | Preserved verbatim (3 specific think-through prompts) |
| Rollback plan requirement (Part 2.7) | Section 6.8 | Preserved with specific-not-generic instruction |
| 9-point quality gate checklist (Part 4) | Section 8 | Expanded to 16 points by adding B and C gates |
| Source code file table (1.4) | Section 1.1 | Merged with B's line ranges for completeness |
| Section-by-section template mapping (Part 3) | Section 7 | Preserved as the template compliance guide |
| Cross-release integration points (1.3) | Section 5 | Preserved all 10 points |
| 4 key design decisions (1.2) | Section 2 | Expanded to 9 decisions by incorporating C's additional rulings |

### From Variant B (QA)

| Element | Merged Location | Notes |
|---------|----------------|-------|
| Verification Contract template (Step 2b) | Section 6.6 | Preserved verbatim: unit tests, edge cases, failure modes, interaction effects, blast radius |
| Minimum test counts (25 R1, 40 R2) | Section 7 (Test Plan) | Preserved as hard minimums |
| Structured edge case taxonomy (empty/boundary/scale) | Section 6.6 | Part of Verification Contract |
| Structured failure mode taxonomy (exception/missing file/None) | Section 6.6 | Part of Verification Contract |
| Measurable NFR table (6 R1, 6 R2) | Section 7 (NFRs) | Preserved all 12 NFRs with targets and measurements |
| Risk sub-items (failure scenario, detection, blast radius, recovery) | Section 7 (Risks) | Preserved as mandatory per-risk structure |
| 10 mandatory gap questions (Step 10) | Section 12 | Preserved all 10 GAP-01 through GAP-10 |
| R1/R2 mandatory risk lists | Section 7 (Risks) | Preserved: 5 R1 risks, 6 R2 risks |
| YAML frontmatter values | Not included | Dropped: frontmatter is template-specific detail; the merged prompt already says "follow template exactly" |
| Detailed FR-by-FR walkthrough (Steps 2c, 2d) | Not included | Dropped as separate section; the per-task analysis standard (Section 6) replaces this with a protocol that applies uniformly. B's specific test questions for each FR (e.g., "What does count_turns_from_output() return on empty file?") are excellent but are implementation-time concerns, not prompt-level requirements. The Verification Contract template already mandates these via "Edge cases tested: Empty input" |
| R1/R2 interface contracts table (Step 4) | Section 5 | Format preserved; content folded into cross-release integration points |
| Regression test matrix (Step 7, 8.4) | Section 7 (Test Plan) | Preserved as a requirement within test plan |
| Manual/E2E test table (Step 7, 8.3) | Not explicitly separated | The per-task Verification Contract captures manual test needs; a separate table added minimal value over the contract |

### From Variant C (Incremental)

| Element | Merged Location | Notes |
|---------|----------------|-------|
| Overall document structure | Sections 1-10 | The backbone of the merged prompt |
| Atomic commit boundary definition (Req 1) | Section 6.7 | Preserved: commit boundary, git diff footprint, test commands, depends-on, blocks |
| Rejected approach documentation (Req 2) | Section 6.4 | Merged with A's multi-approach evaluation |
| Broader impact analysis with grep patterns (Req 3) | Section 6.3 | Merged with A's impact analysis |
| 3 ASCII data flow diagrams (Req 4) | Section 7 (Section 2.2) | Preserved: Diagram A (current/bugs), B (after R1), C (after R2) |
| 6 specific migration scenarios (Req 5) | Section 7 (Section 9) | Preserved all 6: 3 R1 (phase restart, in-flight gate, extract fallback), 3 R2 (pre-R1 data, input precedence, tmux degradation) |
| 6 anti-patterns (end section) | Section 9 | Preserved all 6 verbatim |
| Task inventory tables (R1 phases, R2 waves) | Sections 3-4 | Preserved C's organization as the clearest |
| Source document table | Section 1.2 | Expanded with A's additional references (boundary-rationale.md, existing R1/R2 drafts, checkpoint tasklist) |
| Core constraint (atomic commits) | Prompt header | Elevated to document-level constraint |
| 9 additional design decisions | Section 2 | C had the most complete decision table; expanded with A's formatting |

---

## What Was Dropped and Why

| Element | Source | Reason Dropped |
|---------|--------|---------------|
| B's detailed per-FR walkthrough (FR-37A.1 through FR-37B.15) | QA variant Steps 2c-2d | These are ~150 lines of FR-specific test questions and edge cases. While valuable, they belong in the GENERATED spec, not in the prompt that generates the spec. The Verification Contract template (Section 6.6) already mandates structured edge case, failure mode, and interaction analysis for every FR. Including B's detailed walkthrough would double the prompt length without adding a new structural requirement. |
| B's YAML frontmatter values | QA variant Step 1 | The template already defines frontmatter structure. Hardcoding values in the prompt is redundant with "follow the template exactly." |
| A's execution instructions as a separate "Part" | Architect variant end | Folded into Section 10. Same content, better placement. |
| A's separate "Template Compliance" part (Part 3) | Architect variant | Folded into Section 7 of merged prompt. Same content, integrated into flow. |
| C's separate "Format Requirements" section | Incremental variant | Folded into Quality Gates (Section 8). The 5 format requirements from C are covered by gates 1, 2, 8, 15, 16. |
| B's separate "Interface Contracts" table as a step | QA variant Step 4 | Content preserved but integrated into Section 5 (cross-release integration points) rather than being a standalone step. |

---

## Structural Innovations in the Merge

1. **Unified Per-Task Analysis Standard (Section 6)**: Neither A, B, nor C had a single consolidated section defining all per-task obligations. A had Parts 2.1-2.7, B had the Verification Contract, C had Requirements 1 and 3. The merge combines all into one 8-stage protocol (6.1-6.8) that every task must pass through.

2. **Expanded Quality Gates (Section 8)**: A had 9 gates, B had 5 self-checks, C had 7 self-checks. The merge produces 16 non-redundant gates covering all three perspectives.

3. **Decision Table Consolidation (Section 2)**: A had 4 decisions, B had 7, C had 9. The merge captures all 9 unique decisions in one table with sources.

4. **Source Document Union (Section 1.2)**: A referenced 9 documents, B referenced 16, C referenced 16. The merge includes all 19 unique documents (some overlap between B and C).

---

## Word Count

Merged prompt: approximately 4,200 words (within the 3,000-5,000 target range).
