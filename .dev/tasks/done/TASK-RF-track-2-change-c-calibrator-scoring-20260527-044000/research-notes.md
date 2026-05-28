# Research Notes: Change C — Confidence Calibrator Scoring Updates

**Date:** 2026-05-27
**Scenario:** A (Explicit — target file known, spec content in proposal)
**Depth Tier:** Standard-Deep
**Track Count:** 2 of 4 (parallel tracks A, C, F, E)
**Template selection:** Template 02 (Complex) — agent prompt edits across multiple sections with downstream-consumer verification

---

## EXISTING_FILES

- `src/superclaude/agents/confidence-calibrator.md` — 118 lines — the target agent prompt. Sections affected: `## Independence Instruction` (L23-27), `## Responsibilities` (L48-54), `## Output Format` (L58-93). New subsection `## Claim-class handling` to be inserted between Independence Instruction and Inputs.
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — 52 lines BEFORE Change A; ~80+ lines AFTER Change A. The calibrator reads this via `rubric_path` input. Change C MUST consume Change A's new 6-dim table, gated-min formula, cross-tab, and verdict-direction modifier.
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — 152 lines (post PR #89) — defines the new frontmatter fields (`Claim class`, `Evidence class`, `Verdict direction`) that the calibrator's new Responsibility 2a reads.
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — 456 lines — the troubleshoot orchestrator that dispatches the calibrator agent in Wave 1.7 and Wave 3. Read-only for this task; needed for the downstream-consumer audit (does the new Stage-2 trace output break any consumer?).
- `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` (in MAIN checkout) — Change C spec at L190-255.

## PATTERNS_AND_CONVENTIONS

- Agent prompts live in `src/superclaude/agents/*.md`; `make sync-dev` mirrors to `.claude/agents/`. Same source-of-truth rule as skills.
- Calibrator agent definition follows the standard agent format: frontmatter (name, description, category, tools, model, maxTurns, permissionMode), then Role / Independence Instruction / Safety Constraint / Inputs / Responsibilities / Output Format / Boundaries / Failure Modes.
- Output Format is a Markdown report template embedded in a fenced code block at L58-93. New Stage-2 trace table inserts INSIDE this fenced block.
- Calibrator's `tools: Read` declaration limits the agent to Read-only — relevant for the new "Spot-check evidence" Responsibility #3 which already uses Read; the new WebFetch-detection step in 3a (V2 merged) is a MARK-only (mark spot_check_unverifiable in Notes), NOT an actual WebFetch — so the tools list does NOT need to grow.

## GAPS_AND_QUESTIONS

- **Dependency on Change A:** Change C's Responsibility #1 says "6 dimensions" and §5 says "use the rubric's gated-minimum formula" — both ONLY make sense after Change A lands. The task file MUST document this in Prerequisites and the executor MUST verify Change A has shipped before running Change C. Cross-task ordering is a HARD blocker, not a soft warning.
- **Anchoring scenarios for multi-line REPLACE blocks:** The Responsibilities section has 6 numbered items currently (L49-54); the proposal replaces #1, #4, #5 and inserts new #2a, #3a, #5a between existing items. Researcher must capture each anchor precisely — the existing numbered list re-numbers after insertions which means `old_string` MUST include the surrounding numbered context to be unique.
- **Output Format Stage-2 trace insertion point:** The proposal inserts the new `## Stage-2 trace (REQUIRED)` subsection AFTER the per-dimension table but BEFORE the existing `## Confidence` subsection. The fenced code block at L58-93 contains BOTH subsections — researcher must clarify whether the new Stage-2 trace lands INSIDE the fenced block (rendered as part of the template) or OUTSIDE (as a separate doc section). Reading the existing file structure: it appears to be INSIDE the fenced block (the report output template).
- **No tests exist:** unlike Change A which has no automated harness, Change C does have a future harness (Track 4 / Change E / calibrator-eval-cases.md). The task file SHOULD document that Track 4 is the regression test for Change C but TESTING_REQUIREMENTS in the task is NONE (the corpus is built by a separate track).

## RECOMMENDED_OUTPUTS

| # | Researcher | Topic Type | Output File |
|---|------------|-----------|-------------|
| 1 | spec-extraction | Source Spec Extraction | research/01-change-c-spec-extraction.md |
| 2 | target-file-state | File Inventory + Anchor Capture | research/02-target-file-state.md |
| 3 | template-conventions | Template & Examples | research/03-template-and-conventions.md |
| 4 | downstream-consumers | Integration Points | research/04-downstream-consumers.md |

## SUGGESTED_PHASES

- **Researcher 1 — Source Spec Extraction:**
  - Scope: Read proposal L190-255 (Change C spec block).
  - Focus: Extract the four diff sketches (Responsibilities, new Claim-class handling subsection, Output Format additions, Confidence section); extract REQUIRED MUST statements ("Self-reported confidence ... read but NOT used"; "spot_check_unverifiable"; "default to runtime_behavior fail-safe"); extract the Stage-2 trace table with all 7 rows verbatim; classify each insertion as REQUIRED/REPLACE.
  - Output: research/01-change-c-spec-extraction.md
  - Other researchers covering: target-file-state covers calibrator byte-state; template-conventions covers agent-file patterns; downstream-consumers covers SKILL.md call sites.

- **Researcher 2 — Target File State:**
  - Scope: Read `src/superclaude/agents/confidence-calibrator.md` end-to-end.
  - Focus: byte-level current state; capture every anchor — (a) Independence Instruction L23-27 ending + Inputs L39-45 beginning (for inserting `## Claim-class handling` subsection between them); (b) Responsibilities L48-54 — capture each numbered item line verbatim with enough context to make `old_string` unique for REPLACE of #1 and #4 + #5; (c) Output Format L58-93 — capture the per-dimension table and the Confidence subsection anchors for INSERT of Stage-2 trace + REPLACE of Confidence bullets. Identify the fenced code block boundaries (` ```markdown ` opens at ~L58; closes at ~L93).
  - Output: research/02-target-file-state.md
  - Other researchers covering: spec-extraction; template-conventions; downstream-consumers.

- **Researcher 3 — Template & Conventions:**
  - Scope: Read MDTM Template 02 (`.claude/templates/workflow/02_mdtm_template_complex_task.md`) — confirm fits agent-prompt edit + sync + verify + cross-reference flow; read Makefile sync targets; read agent definition conventions across `src/superclaude/agents/*.md` (3-4 representative agent files).
  - Focus: confirm Template 02 is appropriate (complex because multi-section edits + cross-file consumer verification); document agent-prompt edit conventions (frontmatter immutable except for documented schema changes; agent body sections follow consistent ordering: Role/Independence/Safety/Inputs/Responsibilities/Output/Boundaries/Failure-Modes).
  - Output: research/03-template-and-conventions.md
  - Other researchers covering: spec-extraction; target-file-state; downstream-consumers.

- **Researcher 4 — Downstream Consumers (Integration Points):**
  - Scope: Grep `sc-troubleshoot-protocol/SKILL.md` (456 lines) and other skill files for references to the calibrator agent and its outputs.
  - Focus: identify (a) which Wave dispatches the calibrator (Wave 1.7 line ~190, Wave 3 line ~230 per earlier grep); (b) what fields of the Calibration Report are read by the orchestrator (verdict, calibrated, escalation_reason, etc.); (c) whether the new Stage-2 trace addition breaks any parser (it's an INSERT inside the output template, not a REPLACE of existing fields, so should be additive); (d) whether the new `escalation_reason: source_only_dynamic_claim` value is enumerated anywhere downstream and needs updating.
  - Output: research/04-downstream-consumers.md
  - Other researchers covering: spec-extraction; target-file-state; template-conventions.

## TEMPLATE_NOTES

- Template 02 (Complex) — multi-section agent prompt edits + cross-file consumer verification + reliance on Change A landing first warrants the discovery/verification phase model.
- Tier Standard-Deep (4 researchers). Could be 5 (add a separate Patterns & Conventions researcher) but the agent-file conventions are well-established (Change B used 3 researchers for a similar additive edit; Change C adds the cross-file consumer audit).
- QA_GATE_REQUIREMENTS: FINAL_ONLY (executor-performed structural check at end + executor-performed downstream-consumer verification).
- VALIDATION_REQUIREMENTS: "make sync-dev pass + make verify-sync exit 0 + markdownlint hook PASS on edited file + downstream consumer manual cross-check (no SKILL.md parser breakage)"
- TESTING_REQUIREMENTS: NONE for THIS task (the regression harness is Track 4 / Change E, which is a separate task). Document this explicitly in the task's Risks section so reviewers understand the missing test coverage is intentional and tracked elsewhere.

## AMBIGUITIES_FOR_USER

None — intent clear from proposal. Hard dependency on Change A landing first is explicitly documented per the A→B→C→F→E sequencing in the proposal L488-495.
