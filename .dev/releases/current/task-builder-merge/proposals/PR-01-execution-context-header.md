---
proposal_id: PR-01
case: D
source_mechanism: src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md (optional `## Execution Context` section per FINAL-REPORT §7-R2) — task-level header, source areas only, no specific file paths
target_integration_point: src/superclaude/skills/task-builder/SKILL.md:228-238 (Template 01/02 selection) and SKILL.md:1409-1485 (output schema) — add a task-level `## Execution Context` block after frontmatter, before checklist
final_report_citation: FINAL-REPORT §7-R2 (Task Execution Context Block); §6.2 F1 (per-step context references unreliable — task-level + source-areas only); §6.3 (adapt intent, not implementation)
direction_inversion_basis: |
  FINAL-REPORT §7-R2 was conservative-alternative-wins (P1 22/50 → C 34/50) precisely because the OBJECT of context belongs at the task level, not per-step.
  Inverting to task-builder is asymmetric: task-builder already implements per-step self-containment (Bucket C SKILL.md:900, 1452-1457) thoroughly. What it lacks
  is a TASK-LEVEL executor view. The asymmetry is from "we don't have the granular thing" (RF→SC) to "we have the granular thing but no roll-up summary" (SC→TB).
  Risk of over-engineering is LOW because we are NOT re-importing self-containment (already there); we are importing the meta-summary discipline.
conflict_with_task_builder: yes
invariant_protected: evidence-bound-item
complexity_estimate: ~25 lines-of-change
expected_quality_gain: medium — reduces executor confusion on large tasks; provides path-staleness resistance for the readable header; preserves file:line evidence in research/*.md
---

## Mechanism in /sc:tasklist

sc:tasklist's templates/phase-template.md and FINAL-REPORT §7-R2 introduce an OPTIONAL `## Execution Context` block at the task level (not per-step). It contains: roadmap item refs (always — never stale), inferable source areas as named modules ("auth module", "qa pipeline" — not `src/auth/middleware.py`), and key constraints. Per FINAL-REPORT §6.2 F1, per-step path references would force the generator to hallucinate paths that may not exist or change between generation and execution; therefore the block is task-level and uses "source areas" rather than specific paths. The verification clause stays in Acceptance Criteria; the Execution Context block is a READING aid for the executor.

## Proposed adaptation in task-builder

Add to `src/superclaude/skills/task-builder/SKILL.md` instruction set (around SKILL.md:228-238 template-selection and SKILL.md:1409-1485 output schema):
- After the frontmatter table in the generated MDTM task file, insert an optional `## Execution Context` section containing:
  - **References:** BUILD_REQUEST GOAL line (always known), WHY summary, related-doc IDs if BUILD_REQUEST provided them.
  - **Source areas:** named modules or packages inferred from research (e.g., "rf-qa agent prompts", "task-builder skill body") — NEVER specific `path.py:NN` references at this level.
  - **Key constraints:** top 1-3 invariants the executor must not break (lifted from BUILD_REQUEST QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS if present).
- The per-checklist-item self-contained 5-field schema (context+action+output+verification+completion gate) is UNCHANGED. Per-item file:line evidence citations live in `research/[NN]-[topic].md` and in the item's Context field, NOT in the Execution Context header.
- Rule 16/17/18 alignment (SKILL.md:1558-1562) is preserved — BUILD_REQUEST QA/Validation/Testing requirements still become checklist items, in addition to the constraint summary.

## Why this is NOT a 1:1 port

FINAL-REPORT §6.3 says: "4 of 5 proposals directly ported RF mechanisms... the same mechanisms introduced unnecessary complexity. The conservative alternatives succeeded by adapting the intent of each RF mechanism to SC's architectural constraints rather than porting the implementation." Inverting that lesson here: porting sc:tasklist's R2 wholesale would import the "no specific file paths anywhere" rule, which would VIOLATE task-builder's evidence-bound-item invariant (Bucket C SKILL.md:452-454, 1530). The adaptation confines the "no specific paths" rule to the TASK-LEVEL header only; per-item Context fields and research/*.md keep file:line citations intact.

## Invariant analysis

- **evidence-bound-item (PROTECTED, central):** file:line citations remain mandatory in research notes and per-item Context fields. Only the executor-facing roll-up header uses source-area framing.
- **self-contained-item (untouched):** the 5-field schema for each checklist item is unchanged. The new header is task-level, not item-level.
- **persistent .dev/tasks/ artifact (untouched):** research/*.md, qa/*.md continue to persist; this proposal only adds a section to the task file itself.
- **zero-trust QA (untouched):** no gate behavior modified.
- **parallel research (untouched):** generation flow unchanged.

## Failure modes the proposal must handle

1. **Source area cannot be inferred.** rf-task-builder must omit the "Source areas" line (do not invent), per SKILL.md:705-708 codebase-truth rule.
2. **BUILD_REQUEST is minimal (GOAL only).** Header degenerates to References-only, with WHY/source-area lines omitted. Optional behavior preserved.
3. **Executor expects per-step paths.** Mitigated because per-item Context fields still contain specific paths; only the rollup is source-area framed.
4. **Header drifts from the checklist body.** rf-qa task-integrity should re-check that all `## Execution Context` source areas appear in at least one item's Context field.

## Concrete change sketch

- Edit `src/superclaude/skills/task-builder/SKILL.md` step A.9 (rf-task-builder spawning section, near SKILL.md:719) to instruct the builder agent to emit a `## Execution Context` block immediately after frontmatter.
- Add a checklist item to A.10 task-integrity (SKILL.md:898-906) verifying: "(a) Execution Context block present when BUILD_REQUEST has ≥3 source areas inferable; (b) no specific file paths in the block; (c) referenced source areas reappear in at least one item's Context field."
- No template files added/changed — instructions live in SKILL.md only since task-builder's templates are externalized (Bucket C SKILL.md:544, 1420).
