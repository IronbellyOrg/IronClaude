# Research Notes: Change A — Escalation Rubric Formula Update

**Date:** 2026-05-27
**Scenario:** A (Explicit — target file known, spec content in proposal)
**Depth Tier:** Standard
**Track Count:** 1 of 4 (parallel tracks A, C, F, E)
**Template selection:** Template 01 (Generic) — additive edits similar to shipped Change B (PR #89)

---

## EXISTING_FILES

- `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — 52 lines — the canonical rubric file Change A modifies. Currently 5 dimensions in a markdown table (L11-17), simple arithmetic-mean formula (L19), 4-rule Escalation Decision section (L23-43).
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — 152 lines (post PR #89) — the schema that ChangeA's new dimension row + Verdict-direction modifier reference. Read-only for this task.
- `src/superclaude/agents/confidence-calibrator.md` — 118 lines — references the rubric via `rubric_path`; mention the 5-dim count in §Responsibilities §1 (will be updated by Track 2 / Change C). Read-only for this task (cross-reference check only).
- `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` (in MAIN checkout, NOT this worktree) — Change A spec lives at L43-109.

## PATTERNS_AND_CONVENTIONS

- Source-of-truth rule: edit `src/superclaude/skills/...`, NEVER `.claude/skills/...`. `make sync-dev` + `make verify-sync` workflow (same as Change B / PR #89).
- Markdown lint: `markdownlint` hook runs on the file via `pre-commit run markdownlint --files <path>`. Exit 0 required; auto-`--fix` may modify file → re-sync.
- Em-dashes are U+2014 (verified pattern from PR #89). The `≤` (U+2264) and `∈` (U+2208) characters are used in the existing template & calibrator — same characters in the new content.

## GAPS_AND_QUESTIONS

- **Edit shape mix:** Change A is INSERT-AND-REPLACE (not purely additive like Change B). Specifically: the Evidence-grounding 1.0 anchor cell is REPLACED (L57 of proposal diff), the formula line is REPLACED (L64-65), and four blocks are inserted. Researcher must capture both replace anchors AND insert anchors as unique-match `old_string` slices for Edit tool calls.
- **Cross-environment line-number drift:** proposal's "line 19" formula reference and "lines 11-17" table reference are V1 source state. The current file may have drifted. Researcher MUST verify line numbers byte-by-byte against the actual current file.
- **One escalation-rule addition under § 3:** the proposal adds a 5th sub-bullet to the Escalation Decision § 3 (`signal-driven escalation` list). Researcher must confirm exact insertion anchor — after the existing security_caution bullet, before § 4 default.

## RECOMMENDED_OUTPUTS

| # | Researcher | Topic Type | Output File |
|---|------------|-----------|-------------|
| 1 | spec-extraction | Source Spec Extraction | research/01-change-a-spec-extraction.md |
| 2 | target-file-state | File Inventory + Anchor Capture | research/02-target-file-state.md |
| 3 | template-conventions | Template & Examples | research/03-template-and-conventions.md |

## SUGGESTED_PHASES

- **Researcher 1 — Source Spec Extraction (spec-extraction):**
  - Scope: Read proposal L43-109 (Change A spec block).
  - Focus: Extract every `+` line as paste-ready insertion blocks; extract every `-`/`+` pair as REPLACE blocks; classify each as REQUIRED/OPTIONAL; capture the verbatim formula `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)`; capture the verdict-direction cap table (REFUTE/REJECT → 0.70; AFFIRM → 0.84); capture the full cross-tab table (6 claim_class rows × 6 evidence_class cols); capture the new escalation rule for `source_only_dynamic_claim`. Note the V2-merged provenance suffix on cross-tab subsection.
  - Output: research/01-change-a-spec-extraction.md
  - Other researchers covering: target-file-state covers current rubric byte-state; template-conventions covers Makefile/sync rules.

- **Researcher 2 — Target File State (target-file-state):**
  - Scope: Read `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` end-to-end.
  - Focus: byte-level current state; unique-match `old_string` candidates for every insertion AND replacement anchor; specifically (a) the Evidence-grounding row (full table line) for REPLACE; (b) the formula line "**Confidence** = arithmetic mean of the five dimension scores." for REPLACE; (c) end-of-Confidence-calibration section anchor for INSERT of Verdict-direction modifier; (d) anchor for INSERT of cross-tab section; (e) anchor between security_caution bullet and § 4 default for INSERT of new escalation rule.
  - Output: research/02-target-file-state.md
  - Other researchers covering: spec-extraction covers proposal text; template-conventions covers conventions.

- **Researcher 3 — Template & Conventions (template-conventions):**
  - Scope: Read MDTM Template 01 (`.claude/templates/workflow/01_mdtm_template_generic_task.md`); read Makefile sync targets (sync-dev L109, verify-sync L166); read `.pre-commit-config.yaml` markdownlint hook (L70-82) and block-claude-generated-mirrors hook (L102-109).
  - Focus: Confirm Template 01 fits an additive-edit + sync + lint flow (same as Change B which used Template 01); document sync ordering gotcha (sync-dev MUST precede verify-sync); document markdownlint --fix may modify file (re-sync needed).
  - Output: research/03-template-and-conventions.md
  - Other researchers covering: spec-extraction; target-file-state.

## TEMPLATE_NOTES

- Template 01 (Generic) — same as Change B/PR #89. Rationale: additive edits with a sync gate and a lint gate; no discovery phase needed (target file known, spec content fully captured in proposal).
- Tier Standard (3 researchers). Could downgrade to Quick (also 3 researchers) but Standard's gate evaluation rigour is appropriate given the formula change has downstream consumers (Change C reads the formula).
- QA_GATE_REQUIREMENTS: FINAL_ONLY (matches Change B precedent — no per-phase QA agent spawning required since the executor-performed structural check at end is sufficient for this scope).
- VALIDATION_REQUIREMENTS: "make sync-dev pass + make verify-sync exit 0 + markdownlint hook PASS on edited file"
- TESTING_REQUIREMENTS: NONE (documentation-only edit; no source code modified — same as Change B). The calibrator-eval-cases corpus (Track 4) is the eventual regression harness, but it's a separate track and is itself a new file rather than a test of Change A.

## AMBIGUITIES_FOR_USER

None — intent is clear from the proposal spec and the Change B precedent. The proposal explicitly states A→B→C→F→E sequencing; A is the bottleneck for C and F.
