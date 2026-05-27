---
title: "Phase 2 — Protocol Contract Change Summary"
task: TASK-RF-20260526-183300
phase: 2
created: 2026-05-26
status: complete
---

# Phase 2 — sc-brainstorm Protocol Contract Change Summary

This report maps each required Phase 2 contract fix to the actual file sections changed during Steps 2.1-2.4, with evidence of coverage and any unresolved blockers. All edits were applied only to source-of-truth files under `src/superclaude/skills/sc-brainstorm-protocol/`; no generated `.claude/skills/` mirror was modified.

## Scope

Phase 2 covered four source-of-truth files:

- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` (Step 2.1)
- `src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md` (Step 2.2)
- `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` (Step 2.3)
- `src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md` (Step 2.4 — no-edit decision with scope note)

## Coverage Matrix

| # | Required contract fix | File · Section changed | Evidence of coverage | Unresolved blocker |
|---|----------------------|------------------------|---------------------|-------------------|
| 1 | Deterministic context-anchor extraction before seed brief synthesis | `SKILL.md` Wave 1 step 5 (new) · `refs/socratic-templates.md` §Context-Anchor-Extraction (new) | SKILL.md adds a numbered step 5 with structured-object anchor schema (type/value/source/confidence) and 4-source extraction rule before step 6 synthesis; socratic-templates.md adds full §Context-Anchor-Extraction section with 12-type taxonomy table, verbatim rule, dedup priority (topic>dialogue>enrichment), empty-extraction WARN handling, and forbidden-transformations list | None |
| 2 | Mandatory dedicated `## Provenance` section in merged-requirements (not inline comments, not frontmatter-only) | `SKILL.md` Wave 3 step 5 · `refs/handoff-routing.md` §Merged-Requirements-Normalization (new) | Both files list `## Provenance` as one of the SIX required sections with explicit "dedicated section (NOT inline comments, NOT frontmatter-only)" wording; section-empty rule permits "(none identified)" only when both adversarial output and seed brief contain no items of that kind; Wave 4 pre-handoff validation rejects empty/placeholder Provenance | None |
| 3 | Canonical merged-requirements section list (Functional Requirements, Non-Functional Requirements, Acceptance Criteria, Risks, Open Questions, Provenance) | `SKILL.md` Wave 3 step 5 · `refs/handoff-routing.md` §Merged-Requirements-Normalization | Both files enumerate the six required sections in the same order with the same names; Risks may be rendered as list OR table; Wave 4 canonical-contract validation gate in `refs/handoff-routing.md` §Handoff-Routing checks "all six required sections are present" before any handoff invocation | None |
| 4 | Canonical merged-requirements frontmatter schema + return contract schema | `SKILL.md` Wave 3 step 5 (frontmatter) · `SKILL.md` §4 Return Contract · `refs/handoff-routing.md` §Merged-Requirements-Normalization (frontmatter) · §Adversarial-Invocation return contract consumption section | Frontmatter contract is identical across SKILL.md Wave 3 step 5 and handoff-routing §Merged-Requirements-Normalization (schema_version, source_seed_brief_path, domain, strategy, adversarial_status, convergence_score, fit_to_intent, unresolved_conflicts). Return contract in SKILL.md §4 extended with `seed_schema_version`, `merged_requirements_schema_version`, `context_anchors_count`, `fit_to_intent`, `fit_to_intent_issues`, `blind_mode`, `source_of_truth_paths`, plus dry-run null specifics paragraph. Handoff-routing return-consumption section documents the same brainstorm-owned fields | None |
| 5 | Fit-to-intent gate comparing seed-brief.md to merged-requirements.md (pass/partial/failed routing) | `SKILL.md` Wave 3 step 6 (new) · `refs/handoff-routing.md` §Fit-to-Intent-Gate (new) | Both files define identical gate criteria (problem-statement preservation, must_preserve retention, out_of_scope non-promotion, constraint representation, success-criterion representation, conflict surfacing) and identical pass/partial/failed verdict computation. Routing: pass→normal Wave 4; partial→Wave 4 with caution metadata + visible warning; failed→SKIP handoff and return artifacts for review. Side effect appends `## Fit-to-Intent Issues` subsection (rendered as `(none)` on pass) | None |
| 6 | Concrete-over-generic threshold and anchor preservation | `SKILL.md` Wave 3 step 5 (concrete-over-generic clause + dropped-anchor rationale) · `refs/socratic-templates.md` §Synthesis-Rules anchor-preservation contract · §Context-Anchor-Extraction anchor-type taxonomy (includes `threshold`, `date`, `acceptance_target`, `rollback_bound`, `compliance`) · `refs/handoff-routing.md` §Merged-Requirements-Normalization concrete-over-generic preservation clause | Threshold/anchor types are first-class in the anchor taxonomy (12 types including `threshold`, `date`, `compliance`, `acceptance_target`, `rollback_bound`). Synthesis rules state every Wave 3 proposal MUST preserve-or-explicitly-challenge anchors; silent omission routes to fit-to-intent failure. Wave 3 normalization requires preserved anchors carried through and dropped anchors documented in `## Provenance` with rationale. Live-governance/safety improvements explicitly noted as augmentation rather than replacement of concrete anchors | None |
| 7 | Source-of-truth sync discipline (src/→make sync-dev→make verify-sync; no-stage-mirror) | `refs/handoff-routing.md` §Source-of-Truth / Sync Discipline (new) · `refs/socratic-templates.md` §Source-of-Truth / Sync Discipline (new) | Both files add a §Source-of-Truth / Sync Discipline section stating: edit `src/superclaude/skills/sc-brainstorm-protocol/` first; regenerate `.claude/skills/` mirrors with `make sync-dev`; verify with `make verify-sync` before commit; do NOT stage generated `.claude/skills/...` mirrors; if `git add` needs `-f` on a `.claude/` mirror path, STOP. handoff-routing.md adds a joint-update contract table covering seed-brief schema, canonical merged-requirements, fit-to-intent gate, return contract, and Domain-Template-Mapping — each row lists every file that must stay in sync | None |
| 8 | Live-improvement preservation (governance/safety/lifecycle/policy/proof-gate as augmentation) | `SKILL.md` Wave 3 step 5 (live-governance augmentation clause) · `SKILL.md` §6 Will/Will Not (preserved sanitization + no-silent-downgrade + empty/partial/missing-file guards + new Will rows asserting anchor preservation + dedicated Provenance) · `refs/handoff-routing.md` §Merged-Requirements-Normalization concrete-over-generic preservation clause | All existing live governance/safety constructs preserved: Wave 0 prereq validation no-silent-downgrade, Wave 2B sanitization, Wave 3 empty-response/partial-parse/missing-file guards, Wave 3 F1-F3 fallback protocol. Wave 3 step 5 explicitly states "Live governance/safety improvements (lifecycle taxonomies, policy framing, proof gates, rollback/purge/disablement controls) augment — never replace — concrete anchors." Will/Will Not section adds matching rows | None |

## Step-by-Step Trace

### Step 2.1 — `SKILL.md`

8 targeted Edits:

1. Wave 1 step 5 (new): deterministic `context_anchors` extraction with structured-object schema.
2. Wave 1 step 6 (renumbered from 5): extended seed-brief frontmatter (`schema_version`, `intent_summary`, `context_anchors`, `must_preserve`, `out_of_scope`, `source_confidence`) + new body sections (`## Intent Summary`, `## Context Anchors`, `## Must Preserve`, `## Out of Scope`) + synthesis rules.
3. Wave 3 step 5 (new): canonical merged-requirements normalization contract (frontmatter + 6 required sections + concrete-over-generic + live-governance-as-augmentation + section-empty rule + normalization-failure handling).
4. Wave 3 step 6 (new): pre-Wave-4 fit-to-intent gate with pass/partial/failed verdict + routing.
5. Wave 4 pre-handoff canonical-contract validation gate (no silent downgrade).
6. §4 Return Contract extended with 7 new fields + dry-run null specifics paragraph.
7. Wave 1 and Wave 3 exit criteria updated.
8. §5 Error Handling Matrix extended with 6 new rows; §6 Will/Will Not rewritten with anchor preservation, dedicated Provenance, no-must-preserve-silent-drops, no-out-of-scope-promotion, no-.claude-mirror-edits, live-governance-augmentation rows.

### Step 2.2 — `refs/socratic-templates.md`

1 Edit replacing §Synthesis-Rules and appending two new sections:

- `§Synthesis-Rules` rewritten with 9-section order (Intent Summary first), Must Preserve / Out of Scope / Context Anchors marked MANDATORY, anchor-preservation contract requiring every Wave 3 proposal to preserve-or-explicitly-challenge anchors.
- `§Context-Anchor-Extraction` (new): deterministic 4-source extraction (topic, dialogue, enrichment, `@file`), structured-object schema (type/value/source/confidence), 12-type taxonomy table (file/symbol/endpoint/component/concept/constraint/threshold/date/stakeholder/rollback_bound/compliance/acceptance_target) with confidence defaults, verbatim rule, priority-based deduplication, empty-extraction handling, forbidden transformations.
- `§Source-of-Truth / Sync Discipline` (new): cross-file sync requirement between SKILL.md seed schema and this file's synthesis rules; src/→make sync-dev→make verify-sync flow; no-stage-mirror rule.

### Step 2.3 — `refs/handoff-routing.md`

5 targeted Edits:

1. §Enrichment-Sources Codebase Tier 1: anchor-driven query template with type-filtering (file/symbol/endpoint/component for query 1; concept/component/compliance/constraint for query 2), raw-topic fallback retained for empty-anchor case, anchor sanitization rule, agent-spec injection prohibition restated.
2. §Adversarial-Invocation return-contract consumption: extended with brainstorm-owned downstream fields and cross-reference to SKILL.md §4.
3. 3-status routing table re-routed PASS/PARTIAL to §Merged-Requirements-Normalization, FAIL skips normalization+gate+Wave 4; NEW §Merged-Requirements-Normalization section; NEW §Fit-to-Intent-Gate section with criteria + verdicts + routing table.
4. §Handoff-Routing: canonical-contract pre-handoff validation gate (schema_version, six sections, non-empty Provenance, fit_to_intent != failed/pending/missing) + rewritten tasklist/task pre-invoke validation (removed legacy "≥3 enumerated requirements" count).
5. §Source-of-Truth / Sync Discipline (new): src/→make sync-dev→make verify-sync, no-stage-mirror with `-f` siren note, joint-update contract table spanning five contracts.

### Step 2.4 — `refs/agent-spec-builder.md`

No edits. Scope note written to `.dev/tasks/to-do/TASK-RF-20260526-183300/phase-outputs/discovery/agent-spec-builder-scope-note.md` documenting that existing guards (raw-topic prohibition at line 52, parameter sanitization rule at lines 70-74, round-trip validation at lines 97-109) already cover the anchor-injection risk surface. Scope preserved — no broadening into persona-selection-from-anchors.

## Verification

- All edits confined to source-of-truth files under `src/superclaude/skills/sc-brainstorm-protocol/`.
- No generated `.claude/skills/` mirror files were modified.
- `grep -E "TODO|FIXME|TBD|XXX"` against the three edited files returns 0 matches.
- `src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md` mtime unchanged after Step 2.4 (verified via `ls -la` and `git status --short`).
- Both tasklist copies (`.dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-tasklist.md` and `.dev/tasks/to-do/TASK-RF-20260526-183300/TASK-RF-20260526-183300.md`) remained byte-identical through every Phase 2 step (verified via `diff -q`).

## Unresolved Blockers

None. All Phase 2 steps completed with full coverage; no items required blocker logging.
