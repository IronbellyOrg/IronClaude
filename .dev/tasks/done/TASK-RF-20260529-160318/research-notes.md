# Research Notes: Implement Wave 1.6 Diagnosability Audit

**Date:** 2026-05-29
**Scenario:** A (explicit — user provided GOAL, WHY, WHERE, all flags, suggested tier/template/track count)
**Depth Tier:** Standard (5 researchers)
**Track Count:** 1 (single track — tightly coupled SKILL.md + 4 ref-file changes that must land together)
**Status:** Complete

---

## EXISTING_FILES

**Source-of-truth (`src/superclaude/skills/sc-troubleshoot-protocol/`):**

- `SKILL.md` — **468 lines** (current), v1.0 of the 7-wave troubleshoot protocol. Brainstorm spec referenced line ranges based on 470-line state; 2-line drift — researchers MUST re-verify every cited line range.
- `refs/triage-checklist.md` — 65 lines. Wave 1 cause-class taxonomy. Not modified by this task.
- `refs/escalation-rubric.md` — 82 lines. Wave 2 + Wave 1.7 confidence-gate rubric. **MODIFIED by this task** (append `## Diagnosability interaction` section, ≤15 lines, per spec §9).
- `refs/doc-discovery.md` — 182 lines. Wave 1.5 documentation-grounding ref. **STRUCTURAL TWIN of the new ref** — its 4-section pattern (queries / currency check / per-branch schemas / context-card template) is the precedent the new `refs/diagnosability-audit.md` must mirror.
- `refs/hypothesis-card-template.md` — 152 lines. **MODIFIED** (one-line addition under `## Grounding gaps`).
- `refs/report-template.md` — 196 lines. **MODIFIED** (add `## Diagnosability Context` section + hard-stop Next Steps + `--depth deep` banner per spec §9 + §7).
- `refs/remediation-handoff.md` — 122 lines. Wave 6 prompt template. Not modified.
- `refs/calibrator-eval-cases.md` — 81 lines. Test fixtures. Not modified.

**To be created:**

- `refs/diagnosability-audit.md` — NEW, ~250-400 lines, 8 sections specified in merged-output.md §9.

**Implementation infrastructure (already present, no edits expected):**

- `Makefile` targets: `lint`, `format`, `sync-dev`, `verify-sync` — verified present via grep.
- `.claude/templates/workflow/02_mdtm_template_complex_task.md` — MDTM template 02 (the one the rf-task-builder agent will read).
- `.claude/skills/sc-troubleshoot-protocol/` — sync-dev mirror; **MUST NOT edit directly** per CLAUDE.md absolute rule. Only stageable file under `.claude/` is `.claude/settings.json` — not expected to need updates for this scope.

**Authoritative design source:**

- `/config/workspace/IronClaude/.dev/brainstorms/20260529-141819-troubleshoot-wave-1-6-diagnosability/merged-output.md` — 768-line spec. Researchers and builder MUST treat as the contract; do NOT re-derive design positions. Settled forks: scope=logging-only-narrow, placement=between-1.5-and-1.7, default=on-with-opt-out.

## PATTERNS_AND_CONVENTIONS

(Researchers will populate per evidence; sketch from initial scope discovery.)

- **Wave-graph pattern in SKILL.md**: each wave has `Goal / Preconditions / Steps (numbered) / Exit criteria / Failure handling table / Token budget`. New Wave 1.6 section MUST follow this pattern.
- **Ref-file pattern in `refs/doc-discovery.md`**: structured 4-section layout — Section 1 query templates, Section 2 currency-check procedure, Section 3 per-branch schemas, Section 4 context-card template. New `refs/diagnosability-audit.md` has 8 sections (spec §9), but should preserve this section-as-self-contained-unit convention.
- **Output Contract table** in `SKILL.md` (lines ~41-57 at brainstorm time, may have drifted): each row is `Field | Type | Description`. 4 new rows to add (per merged-output.md §5).
- **Status emoji convention**: `🟡 To Do`, `🟢 Done` — used in MDTM frontmatter (template 02).
- **No HTML provenance comments**: merged-output.md uses `<!-- Source: Variant N -->` comments; these are brainstorm-artifact metadata only. Do NOT copy into SKILL.md or ref-files.
- **Source-of-truth discipline**: edit `src/superclaude/skills/sc-troubleshoot-protocol/` only; `make sync-dev` copies to `.claude/skills/sc-troubleshoot-protocol/`; `make verify-sync` checks parity. NEVER `git add` `.claude/skills/...` (absolute CLAUDE.md rule).

## GAPS_AND_QUESTIONS

These are the actual research gaps the 5 parallel researchers need to fill:

1. **Stale line ranges (HIGH priority)** — merged-output.md §10 cites SKILL.md line ranges that may have drifted since the brainstorm wrote them (SKILL.md was 470 lines then, now 468). Researcher 5 (Doc Cross-Validator) MUST verify EVERY cited line range and emit `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` per the protocol.

2. **doc-discovery.md structural details** — the new `refs/diagnosability-audit.md` is its structural twin. Researcher 2 (Patterns & Conventions) MUST extract the exact section structure, schema format (JSON-with-fields), placeholder syntax (`<scope>`, `<component_paths>`), and fallback-mechanism conventions.

3. **MDTM template 02 specifics** — the rf-task-builder agent will follow template 02 to produce the task file; Researcher 4 (Template & Examples) MUST extract: required frontmatter fields, Section A-K + L rules, the 5-field self-contained-item pattern (Context/Action/Output/Verification/Completion gate), granularity rule A3.

4. **Cross-references in SKILL.md affected by the new wave** — adding Wave 1.6 requires updating the wave-graph ASCII (line ~75-85), updating Wave 1.7 preconditions (~194-196), updating Wave 5 step 2 (~331-342). Researcher 3 (Integration Points) MUST trace these cross-references in the CURRENT SKILL.md state (not the brainstorm-era state) and identify ALL hook points.

5. **Existing audit-log emission convention** — Wave 1.5 emits to the audit log; new Wave 1.6 must emit similarly. Researcher 1 (File Inventory) MUST extract the audit-log emission pattern from each existing wave.

6. **Markdownlint rules in this repo** — `make lint` runs markdownlint; what rules apply (line length, heading levels, code fence languages)? Researcher 1 will check pyproject.toml / `.markdownlint*` config or grep Makefile for the linter invocation.

7. **Prior task-builder examples involving skill-protocol edits** — Researcher 4 will check `.dev/tasks/done/` for any prior skill-protocol modification tasks to learn from their phase structure.

## RECOMMENDED_OUTPUTS

5 research files at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260529-160318/research/`:

- `01-file-inventory.md` — current state of SKILL.md + all 7 ref files; exports/sections per file; line counts; audit-log emission patterns; markdownlint configuration
- `02-patterns-conventions.md` — doc-discovery.md structural twin extraction + SKILL.md wave-structure pattern + Output Contract row format + status-emoji + source-of-truth discipline
- `03-integration-points.md` — cross-references in SKILL.md affected by Wave 1.6 insertion; wave-graph hook points; how Output Contract is consumed downstream (Tier 3 task-builder, Wave 5 REPORT.md composition)
- `04-template-examples.md` — MDTM template 02 Section A-K+L extraction; granularity rule A3; prior `.dev/tasks/done/` task-builder examples for skill-protocol edits
- `05-doc-cross-validator.md` — verify EVERY merged-output.md §10 line-range claim against the actual SKILL.md (current 468-line state); tag with [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED]; flag any sections that have moved since the brainstorm

## SUGGESTED_PHASES

Researcher assignments (all spawned in a single Agent-tool message for parallel execution):

| # | Topic Type | Specific Scope | Output File |
|---|------------|----------------|-------------|
| 1 | File Inventory | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` + all 7 `refs/*.md` files + `Makefile` (lint/sync targets) + markdownlint config (if any) | `research/01-file-inventory.md` |
| 2 | Patterns & Conventions | `refs/doc-discovery.md` (deep read — structural twin) + SKILL.md wave-pattern + Output Contract row format + MDTM template 02 frontmatter pattern + status-emoji conventions | `research/02-patterns-conventions.md` |
| 3 | Integration Points | SKILL.md wave-graph ASCII (line ~75-85), Wave 1.5 step 5 → Wave 1.7 preconditions, Wave 5 step 2 REPORT.md composition (~331-342), Output Contract consumer locations | `research/03-integration-points.md` |
| 4 | Template & Examples | `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (Sections A-K + L) — extract rules A3, A4, B2 self-contained-item pattern. Check `.dev/tasks/done/` for prior skill-protocol task examples (e.g., RF-tasks that modified SKILL.md files) | `research/04-template-examples.md` |
| 5 | Doc Cross-Validator | merged-output.md §10 line-range claims (75-85, 41-57, 91-126, insert after 187, 194-196, 331-342, 391-403, 404-425, 446-454, 428-444, 458-466) verified against CURRENT SKILL.md state | `research/05-doc-cross-validator.md` |

Each researcher knows the others' coverage to prevent duplication. Researcher 5 (Doc Cross-Validator) is the most critical — its `[CODE-CONTRADICTED]` flags drive any line-range updates the builder must apply.

## TEMPLATE_NOTES

- **MDTM template**: 02 (Complex Task) — multi-phase work with QA gates, verification steps, conditional flows (e.g., if `make verify-sync` fails, revert and re-sync).
- **Tier rationale**: Standard. Scope is well-bounded (~9 files in research scope; 5 modifications + 1 creation in implementation scope). Not Deep because the design spec eliminates most ambiguity; not Quick because per-file/per-section granularity demands real exploration.
- **MDTM features needed in generated task file**:
  - Phase structure (Discovery / Implementation / Validation / Completion)
  - Granular per-file-and-per-change items (per A3 — e.g., 11 separate items for the 11 SKILL.md change-points, NOT a single "apply diff" item)
  - Per-phase QA gates (PER_PHASE per BUILD_REQUEST)
  - Validation phase: `make verify-sync`, `make lint`, `make format`
  - No testing items (TESTING_REQUIREMENTS=NONE — skill protocol edit, not code)
  - Source-of-truth discipline encoded in every edit item: "edit `src/superclaude/skills/sc-troubleshoot-protocol/...`, then `make sync-dev`, then `make verify-sync`"
  - Final phase: manual merged-SKILL.md read-through + completion gate

## AMBIGUITIES_FOR_USER

None — intent is clear from the user's BUILD_REQUEST. The merged-output.md spec is authoritative; the implementation question is purely how to break it into executable atoms. Line-range drift (SKILL.md 468 vs spec's 470) is resolvable via Researcher 5; this is not a user-intent question.
