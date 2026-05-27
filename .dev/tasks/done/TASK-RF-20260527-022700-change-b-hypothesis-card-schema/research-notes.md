# Research Notes: Change B — Additive Schema for hypothesis-card-template.md

**Date:** 2026-05-27
**Scenario:** A (Explicit — user gave full source, target, anchors, tier)
**Depth Tier:** Quick (single file, additive, no behavior change)
**Track Count:** 1

---

## EXISTING_FILES

**Target file (single):**
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — 109 lines. Source-of-truth copy. After edits, must be synced to `.claude/` via `make sync-dev`.

**Source-of-spec file:**
- `.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` — 582 lines. Change B specification lives at L110-186.

**Verified anchors in target file (pre-Read confirmed):**
- L7-9 — `## Template` heading + code-fence opener
- L12-16 — frontmatter block (last line is `**Consistency with docs**:...` at L16; new fields insert between L15 `**Cause class**` and L16 `**Consistency with docs**`)
- L48-53 — `Per-dimension self-assessment:` 5-item list (Runtime check inserts as a new row, immediately after L49 `Evidence grounding`, becoming the new 2nd row)
- L59 — `## If I'm wrong, it's probably because...` heading (new `## Falsification standard` and `## Evidence classification` sections insert AFTER this heading's body block ends, before `## Alternatives considered` at L63)
- L70 — closing code-fence of `## Template` block
- L79-108 — worked example (also inside a code fence). Spec does NOT require updating the worked example; whether to update is an Open Question.

## PATTERNS_AND_CONVENTIONS

- **Source-of-truth rule** (CLAUDE.md): edits land in `src/superclaude/`, then `make sync-dev` copies to `.claude/`. `make verify-sync` is the gate.
- **Template file style:** the entire hypothesis card template is rendered INSIDE a fenced ```markdown code block (lines 9-70). Edits go inside that fence.
- **Frontmatter style:** `**Field name**:` followed by inline value (or enum list). Inline enum values use backticks-pipe-backticks form (`` `value_a` | `value_b` ``) when there are multiple. See target L15-16 for pattern.
- **Per-dimension list style:** 6-item flat bullet list, each ` - <dimension>: <0.0|0.5|1.0> — <one-line reason>`.
- **Section heading style:** `##` level-2 inside the template block.
- **Filling guidance pattern:** the file already has a `## Filling the card` section at L72 outside the template fence. The new "Filling rule" sentence in Change B's `## Evidence classification` block belongs INSIDE the new section, not in the global filling guidance.

## GAPS_AND_QUESTIONS

- **Open question — worked example update:** The worked example at L79-108 uses the v1 frontmatter (no `Claim class`, no `Evidence class`, no `Verdict direction`). Should the example be updated to demonstrate the new fields? The proposal's Migration note says "In-flight cards without `Claim class` frontmatter → Calibrator defaults to `runtime_behavior`" (L557), so legacy cards remain valid. **Resolution policy for this task:** leave the worked example unchanged in this commit; the example is explicitly labeled "illustrative — not a real card" (L79). A follow-up task may update it once Changes A/C land.
- **Open question — `.claude/` sync timing:** The user said "do not auto-execute." The /task executor will perform the actual edits. Should `make sync-dev` + `make verify-sync` be encoded as a phase in this task file? YES — sync-dev is required for the edit to take effect at runtime; verify-sync is the project's gate (Memory: "Never edit `~/.claude/` or `<project>/.claude/` directly").
- **Open question — markdownlint:** the source file is markdown; the project has markdownlint hooks. After edits, lint must pass. Encode as a verification step.

## RECOMMENDED_OUTPUTS

- `research/01-target-file-state.md` — exact byte-level state of the target file (current anchor content, indentation, code-fence boundaries)
- `research/02-change-b-spec-extraction.md` — verbatim extraction of all field enums, anchor language, diff blocks, and the optional/required distinction from the proposal
- `research/03-template-and-conventions.md` — MDTM template 01 vs 02 selection rationale, sync-dev / verify-sync workflow, lint gate, related done-tasks (if any) for additive-frontmatter precedent

## SUGGESTED_PHASES

**Researcher 1 — File Inventory / Target State**
- Scope: `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`
- Focus: document exact L1–L109 structure, anchor lines verbatim, indentation, code-fence boundaries, the worked example content
- Output: `research/01-target-file-state.md`
- Others cover: source-spec extraction (R2), template/conventions (R3) — do NOT extract spec from brainstorm

**Researcher 2 — Source Spec Extraction**
- Scope: `.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` L110-186
- Focus: extract EVERY field, enum value, anchor sentence, diff block verbatim. Distinguish REQUIRED vs OPTIONAL additions. Capture the "Filling rule" sentence. Capture the proposal's claim about implementation order (Change B before A).
- Output: `research/02-change-b-spec-extraction.md`
- Others cover: target file state (R1), template selection (R3) — do NOT touch the target file or MDTM templates

**Researcher 3 — Template Selection + Project Workflow**
- Scope: `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` (Quick-tier candidate); spot-check `02_mdtm_template_complex_task.md` if 01 is insufficient. Verify `make sync-dev` / `make verify-sync` workflow from `Makefile` or top-level docs.
- Focus: which MDTM template (01 vs 02) fits a single-file additive edit + sync + lint task; identify the sync-dev and verify-sync commands; note any markdownlint hook command. Check `.dev/tasks/done/` for any prior additive-frontmatter task as precedent.
- Output: `research/03-template-and-conventions.md`
- Others cover: target file state (R1), source spec (R2) — do NOT extract spec or inspect the target file

## TEMPLATE_NOTES

- **MDTM template selection:** 01 (Generic) — single file, additive, known inputs/outputs, no discovery beyond what is already encoded in the spec, no parallel subagent spawning expected during execution.
- **Tier:** Quick — single target file, no behavior change, fully-specified diff blocks. 3 researchers (the skill's minimum).
- **QA_GATE_REQUIREMENTS:** FINAL_ONLY (Quick + Template 01 default) — one structural verification phase at the end.
- **VALIDATION_REQUIREMENTS:** markdownlint passes on the edited file; `make verify-sync` passes.
- **TESTING_REQUIREMENTS:** NONE — the template file is a markdown document with no runtime behavior. The schema is exercised downstream by Changes A, C, F (deferred). No unit / integration tests apply at this layer.

## AMBIGUITIES_FOR_USER

None — intent is clear from the request and codebase context. The worked-example-update decision (deferred to a follow-up) is a builder-internal call documented above in Open Questions, not a user-intent ambiguity.
