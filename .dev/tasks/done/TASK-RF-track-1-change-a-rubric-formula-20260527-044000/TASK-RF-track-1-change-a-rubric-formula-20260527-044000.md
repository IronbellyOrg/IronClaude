---
id: "TASK-RF-track-1-change-a-rubric-formula-20260527-044000"
title: "Change A — Apply gated-minimum formula rubric update (Runtime check 6th dimension, gated-minimum formula, Verdict-direction modifier M3a, Claim-class × evidence-class cross-tab [V2 merged], Evidence-grounding 1.0 cell narrowing, +0.30 buffer prose, source_only_dynamic_claim escalation rule)"
description: "Implement Change A from the calibration-refactor cross-environment merged proposal (CROSS-ENV-PROPOSAL-MERGED.md L43-109). Apply seven structural edits to the single target file src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md (2 REPLACE + 5 INSERT, collapsing to 4 Edit-tool calls per research file 02's recommended ordering): replace the Evidence-grounding 1.0 anchor cell to drop the diagnostic-output clause and add the calibrator spot-check qualifier; insert the new Runtime check 6th dimension table row with claim-class-aware 0.0 scoring rules; replace the arithmetic-mean formula with the gated-minimum form `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)`; insert the +0.30 buffer prose paragraph explaining the unconditional gate semantics; insert the new `### Verdict-direction modifier (M3a)` H3 subsection with the REFUTE/REJECT→0.70 + AFFIRM→0.84 cap table; insert the new `### Claim-class × evidence-class cross-tab [V2 merged]` H3 subsection with the full 6×6 derivation table; insert the new `source_only_dynamic_claim` sub-bullet under § 3 (Signal-driven escalation). After the edits land, run make sync-dev, make verify-sync, and uv run pre-commit run markdownlint against the edited file (same workflow as the shipped Change B / PR #89). Change A is the bottleneck for the sequenced A→B(shipped)→C→F→E calibration-refactor rollout."
status: "🟢 Done"
type: "📝 Documentation"
priority: "🔼 High"
created_date: "2026-05-27"
updated_date: "2026-05-27"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""
depends_on:
- "TASK-RF-20260527-022700-change-b-hypothesis-card-schema"
related_docs:
- path: "/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md"
  description: "Source proposal containing Change A specification (proposal L43-109; file lives in main checkout, not the worktree — verified by ls)"
- path: "src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md"
  description: "Sole target file for this task — all edits land here"
- path: "Makefile"
  description: "Defines sync-dev (L109) and verify-sync (L166) targets"
- path: ".pre-commit-config.yaml"
  description: "Defines markdownlint hook (L70-82) and block-claude-generated-mirrors hook (L102-109)"
- path: ".dev/tasks/done/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/TASK-RF-20260527-022700-change-b-hypothesis-card-schema.md"
  description: "Structural precedent — shipped Change B task using same Template 01, same sync+lint workflow, same FINAL_ONLY QA mode (PR #89)"
tags:
- "calibration-refactor"
- "escalation-rubric"
- "rubric-formula"
- "change-a"
- "pr86-followup"
- "gated-minimum"
template_schema_doc: "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: ""
sprint: ""
due_date: ""
start_date: "2026-05-27"
completion_date: "2026-05-27"
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# Change A — Apply gated-minimum formula rubric update (Runtime check 6th dimension, gated-minimum formula, Verdict-direction modifier M3a, Claim-class × evidence-class cross-tab [V2 merged], Evidence-grounding 1.0 cell narrowing, +0.30 buffer prose, source_only_dynamic_claim escalation rule)

## Task Overview

This task implements Change A from the calibration-refactor cross-environment merged proposal. The proposal defines a sequenced A→B→C→F→E rollout that closes the calibration gap exposed by PR #86 around source-vs-runtime evidence conflation. Change B shipped as PR #89 (landed the hypothesis-card schema slots). Change A is the next step — it lands the rubric formula update that consumes Change B's `claim_class`, `evidence_class`, and `verdict_direction` frontmatter fields, so that Change C (calibrator scoring) has a formula to compute against, Change F (audit gate) has a completed rubric to enforce, and Change E (eval corpus) has expected scores to validate.

The edit is a mix of INSERT and REPLACE operations against a single 52-line target file. Seven structural changes are required: (a) REPLACE the Evidence-grounding 1.0 anchor cell to drop its `OR diagnostic command output reproduces the symptom` clause (that pathway now belongs to the new Runtime check dimension) and add the calibrator's spot-check verification qualifier; (b) INSERT a new 6th dimension table row for Runtime check with claim-class-aware 0.0 scoring rules embedded in the cell text; (c) REPLACE the formula line — change from `arithmetic mean of the five dimension scores` to the gated-minimum form `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)`; (d) INSERT the +0.30 buffer prose paragraph explaining the unconditional gate semantics (0.5 → 0.80 cap; 0.0 → 0.30 cap); (e) INSERT the new `### Verdict-direction modifier (M3a)` H3 subsection at the tail of the calibration section with the REFUTE/REJECT→0.70 + AFFIRM→0.84 cap table; (f) INSERT the new `### Claim-class × evidence-class cross-tab [V2 merged]` H3 subsection (V2-merged provenance) with the full 6×6 derivation table; (g) INSERT a new sub-bullet under § 3 (Signal-driven escalation) for `claim_class ∈ {runtime_behavior, environment_dependent} AND runtime_check < 0.5 → ESCALATE (escalation_reason: source_only_dynamic_claim)`. Per research file 02's Section 5 ordering recommendation, the seven anchors collapse to four Edit-tool calls: Edit 1 = (a) standalone; Edit 2 = (b)+(c)+(d) merged in one Edit; Edit 3 = (e)+(f) merged to eliminate the composite-anchor risk of f-after-e; Edit 4 = (g) standalone.

After the edits land, the task runs `make sync-dev` to mirror `src/` into `.claude/`, `make verify-sync` to confirm zero drift, and `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` to confirm a clean lint pass. The expected final state is the source file grown from 52 lines to approximately 85-100 lines, the `.claude/` mirror reflecting the new content, and a clean lint pass. The trailing rationale sections (`## Why 0.85?` at L44-48 and `## What escalation does NOT mean` at L50-52) MUST remain byte-identical to the pre-edit state — Change A does not touch them.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Apply the 7 Change A structural edits to the target file in 4 Edit-tool calls per research file 02's recommended ordering:** Edit 1 REPLACES the Evidence-grounding 1.0 anchor cell (anchor a); Edit 2 (b+c+d merged) INSERTS the Runtime check 6th dimension row, REPLACES the formula line with the gated-minimum form, and INSERTS the +0.30 buffer prose paragraph; Edit 3 (e+f merged) INSERTS the Verdict-direction modifier (M3a) subsection AND the Claim-class × evidence-class cross-tab [V2 merged] subsection between the rounding line at L21 and the `## Escalation decision (Wave 2)` H2 at L23; Edit 4 INSERTS the new `source_only_dynamic_claim` sub-bullet under § 3 between the `--type security` bullet at L39 and the `4. **Default**` heading at L41. All paste-ready text is captured verbatim in research file 01.
2. **Preserve character encodings throughout:** every em-dash MUST be U+2014 (not double-hyphen ASCII), every existing right-arrow `→` MUST remain U+2192, the new `≤` characters MUST be U+2264 (not `<=`), the new `∈` MUST be U+2208 (not `\in` or `in`), the new `⟹` (if used in the cross-tab implications) MUST be U+27F9 — paste from research file 01's verbatim blocks preserves these codepoints.
3. **Sync `src/` → `.claude/` cleanly:** run `make sync-dev` from the worktree root and confirm exit code 0 with the `🔄 Syncing src/superclaude/ → .claude/` and `✅ Sync complete.` markers; run `make verify-sync` and confirm exit code 0 with "All components in sync" and no `Drift detected` substring.
4. **Pass the markdownlint gate on the edited file:** run `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` and confirm `Passed`; if the hook's `--fix` flag modifies the file (likely because Change A inserts new tables and new H3 headings — prime auto-fix candidates), re-run `make sync-dev` and `make verify-sync` so the `.claude/` mirror stays consistent, then re-invoke the lint command for a clean second-pass exit 0.
5. **Preserve invariants:** the pre-edit trailing rationale sections (`## Why 0.85?` and `## What escalation does NOT mean`) MUST remain byte-identical to the pre-edit state; the dimension count moves from 5 to 6 (the only existing dimension row that is touched is `**Evidence grounding**` — its 1.0 cell text changes; the other 4 rows remain unchanged); the formula line is the only line replaced in the calibration section; no existing escalation rule is removed (only one new sub-bullet is added under § 3); the file's total line count lands in the expected 85-100 range.

## Prerequisites & Dependencies

### Parent Task & Dependencies

- **Parent Task:** (None — standalone follow-up to PR #86 / PR #89)
- **Blocking Dependencies:**
  - `TASK-RF-20260527-022700-change-b-hypothesis-card-schema`: introduces the `claim_class` + `evidence_class` + `verdict_direction` frontmatter fields that Change A's Runtime check row, M3a modifier, cross-tab subsection, and new escalation rule all reference. **Shipped as PR #89 (commit 46d3b342)** — dependency satisfied. The baseline read in Step 1.2 below confirms this is still the case.
- **This task blocks:** Change C (calibrator scoring update — must apply the new formula, +0.30 gate, M3a modifier, cross-tab derivation, and new escalation rule); Change F (audit gate — must enforce the completed rubric); Change E (eval corpus — must validate against expected calibrated scores).

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY — NO CHECKLIST ITEMS HERE**

Required inputs for this task are the three research files in the `research/` subdirectory; each is referenced inline by the action item that consumes it. They are:

- **Source spec extraction:** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/01-change-a-spec-extraction.md` — Purpose: 7 paste-ready blocks (2 REPLACE + 5 INSERT) verbatim from CROSS-ENV-PROPOSAL-MERGED.md L43-109 with proposal line citations, MUST/MUST NOT statements per block, semantic-delta commentary, V2-merge provenance notes, and edit-order recommendation for the executor.
- **Target file state:** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/02-target-file-state.md` — Purpose: byte-level current state of escalation-rubric.md (52 lines), structural map by line range, 7 unique-match anchors (a)-(g) with verbatim `old_string` capture, character-encoding notes, and the recommended 4-Edit-call ordering (Edit 1 = a alone; Edit 2 = b+c+d merged; Edit 3 = e+f merged; Edit 4 = g alone).
- **Template and conventions:** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/03-template-and-conventions.md` — Purpose: Template 01 selection rationale, verbatim Makefile target locations for `sync-dev` (L109) and `verify-sync` (L166), pre-commit markdownlint hook configuration (L70-82), block-claude-generated-mirrors hook configuration (L102-109), source-of-truth rule (edit `src/` not `.claude/`), six known gotchas (sync order, `--fix` may modify file, `block-claude-generated-mirrors` blocks `.claude/` paths, `pre-commit` may need `uv pip install pre-commit`, line-number drift from proposal V1 baseline, worktree CWD discipline), and Change B precedent mapping.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:

- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Execution Context

<!-- Reader-aid block — per-item Context fields below carry file:line citations. -->

**References:**

- R-001 calibration-refactor cross-environment merged proposal — Change A specification (paste-ready 2 REPLACE + 5 INSERT blocks at L43-109)
- R-002 sc-troubleshoot-protocol escalation-rubric template — sole target file for this task (52 lines baseline)
- R-003 Makefile sync-dev + verify-sync targets — defines the mirror and drift-check workflow
- R-004 pre-commit markdownlint hook + block-claude-generated-mirrors hook — defines the lint gate and the staging guard
- R-005 task research notes in this task's research/ directory — three files capturing spec extraction, target state, and template conventions
- R-006 Change B done-task body (PR #89) — structural precedent for Template 01 + FINAL_ONLY QA mode + sync/verify/lint phase

**Source areas:**

- escalation-rubric template (sole target — under `src/superclaude/skills/sc-troubleshoot-protocol/refs/`)
- Makefile sync targets (sync-dev + verify-sync recipes)
- pre-commit markdownlint hook (lint gate + auto-fix behavior)

**Key constraints:**

- QA_GATE_REQUIREMENTS: FINAL_ONLY (executor-performed structural check at end; no per-phase rf-qa spawning)
- VALIDATION_REQUIREMENTS: make sync-dev exits 0; make verify-sync exits 0 with "All components in sync"; uv run pre-commit run markdownlint returns Passed; post-edit structural check confirms all 7 edits landed
- TESTING_REQUIREMENTS: NONE — documentation-only edit; no source code modified

---

## Detailed Task Instructions

### Phase 1: Edit target file

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status

- [x] Update the `status` field in this task file's frontmatter to "🟠 Doing" and set the `start_date` field to today's date `2026-05-27`, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[2026-05-27 HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Baseline read + sanity check

- [x] Read the file `02-target-file-state.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/02-target-file-state.md` (specifically Section 2 "Structural Map (Line Ranges)" and Section 3 "Anchor Verbatim Capture") to confirm the expected baseline state of the target file including the L11-17 dimension table (5 rows ending at `**Domain coherence**`), the L19 formula line (`**Confidence** = arithmetic mean of the five dimension scores.`), the L21 `Round to two decimals.` line, the L23 `## Escalation decision (Wave 2)` heading, the L39 `--type security` bullet, the L41 `4. **Default**` heading, and the L44-52 trailing rationale sections (`## Why 0.85?` and `## What escalation does NOT mean`) that MUST remain untouched, then read the target file `escalation-rubric.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` end-to-end and verify that (a) line count is 52 lines (use Bash `wc -l` to confirm), (b) the L11-17 dimension table block matches R2 §2 verbatim with exactly 5 data rows, (c) the L19 formula line matches `**Confidence** = arithmetic mean of the five dimension scores.` verbatim, (d) the L21 line is exactly `Round to two decimals.`, (e) the L23 heading is exactly `## Escalation decision (Wave 2)`, (f) the L39 `--type security` bullet is present and the L41 `4. **Default**` heading follows after a blank line, and (g) Change B's `claim_class` / `evidence_class` / `verdict_direction` schema slots are landed in `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (the dependency from PR #89 — confirm by grepping for the string `**Claim class**` in that file), ensuring no drift has occurred since research was captured, no fabricated baseline state is assumed, and all 7 insertion/replacement anchors (a)-(g) per R2 are confirmed present. If unable to complete due to file access issues, byte-level mismatch between R2 and the actual file, or missing Change B schema slots in hypothesis-card-template.md, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.3:** Apply Edit 1 (anchor a) — REPLACE the Evidence-grounding 1.0 anchor cell

- [x] Read the file `01-change-a-spec-extraction.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/01-change-a-spec-extraction.md` Section "Block 1 — REQUIRED-REPLACE: Evidence-grounding 1.0 anchor cell" to confirm the paste-ready OLD and NEW text and the semantic delta (the 1.0 anchor drops `OR diagnostic command output reproduces the symptom` and adds the `(snippet match verified by calibrator's spot-check)` qualifier), then read the file `02-target-file-state.md` at the same research/ path Section 3 anchor (a) to confirm the unique-match `old_string` candidate (the whole L13 line because `**Evidence grounding**` appears only once globally in the 52-line file), then edit the file `escalation-rubric.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` using the Edit tool with `old_string` set to the single-line slice `| **Evidence grounding** | Cited \`file:line\` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |` and `new_string` set to the replacement line `| **Evidence grounding** | Cited \`file:line\` matches a real code path that exhibits the symptom (snippet match verified by calibrator's spot-check) | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |`, ensuring the `old_string` matches uniquely (R2 confirms `**Evidence grounding**` appears only at L13), the 1.0-cell text now ends with `(snippet match verified by calibrator's spot-check)` and no longer contains `OR diagnostic command output reproduces the symptom`, the 0.5 cell (`Cited file exists but the specific line/snippet is inferred, not verified`) is preserved byte-identical, the 0.0 cell (`Hypothesis based on pattern-matching prior bugs; no real citation`) is preserved byte-identical, the apostrophe in `calibrator's` is straight ASCII U+0027, all pipe characters and trailing pipe-space are preserved, and no content is fabricated beyond what R1 Block 1 explicitly states. If unable to complete due to non-unique `old_string` match, file access issues, or character-encoding drift, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.4:** Apply Edit 2 (anchors b + c + d MERGED) — INSERT Runtime check row + REPLACE formula line + INSERT +0.30 buffer prose

- [x] Read the file `01-change-a-spec-extraction.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/01-change-a-spec-extraction.md` Sections "Block 2 — REQUIRED-INSERT: New `Runtime check` 6th dimension table row", "Block 3 — REQUIRED-REPLACE: Formula line (arithmetic mean → gated minimum)", and "Block 4 — REQUIRED-INSERT: +0.30 buffer prose paragraph" to confirm the three paste-ready blocks and their proposal-order semantics, then read the file `02-target-file-state.md` at the same research/ path Section 5 "Recommended Edit Ordering" item 2 to confirm the merged-Edit-call strategy (this single Edit handles all three anchors b, c, d to eliminate re-matching against already-modified regions), then edit the file `escalation-rubric.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` using the Edit tool with `old_string` set to the 5-line slice (Domain coherence row + blank L18 + formula line L19 + blank L20 + rounding line L21):

  ```
  | **Domain coherence** | Single domain (e.g. pure logic bug, pure config issue) | Touches two related domains (e.g. logic + tests) | Spans unrelated domains (e.g. perf + auth) |

  **Confidence** = arithmetic mean of the five dimension scores.

  Round to two decimals.
  ```

  and `new_string` set to the post-edit 8-line block that (i) preserves the Domain coherence row unchanged, (ii) inserts the new Runtime check 6th dimension row immediately after it, (iii) keeps the blank separator, (iv) replaces the formula line with the gated-minimum form, (v) inserts a blank line + the +0.30 buffer prose paragraph + a blank line, and (vi) preserves the `Round to two decimals.` line — producing the following block in the file (paste exactly, preserving every backtick, every em-dash U+2014, every pipe, every bold marker, and every backticked enum value):

  ```
  | **Domain coherence** | Single domain (e.g. pure logic bug, pure config issue) | Touches two related domains (e.g. logic + tests) | Spans unrelated domains (e.g. perf + auth) |
  | **Runtime check** | Hypothesis includes an executed reproducer with captured stdout/stderr that reproduces the symptom; OR an asserted-by-test runtime invariant (test cited by name AND its execution-state declared) | Hypothesis includes a runnable command but no captured output; OR cites a test that exists but was not exercised at hypothesis time | Hypothesis is source-only — no executed reproducer, no test assertion. For `claim_class: static_defect`, this dimension inherits the Evidence grounding score (static defects' source IS their runtime). For `claim_class: runtime_behavior` or `environment_dependent`, source-only cards mandatorily score 0.0. |

  **Confidence** = `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)`.

  The +0.30 buffer means a 0.5 dimension caps the composite at 0.80, *below* the 0.85 STOP gate. A 0.0 dimension hard-caps the composite at 0.30. The gates apply unconditionally (no claim_class exemption); for `static_defect` claims, Runtime check auto-inherits Evidence grounding so the gate is satisfied whenever the citation is.

  Round to two decimals.
  ```

  ensuring the `old_string` matches uniquely (R2 confirms `**Domain coherence**` appears only once, `**Confidence**` appears only once, and `Round to two decimals.` appears only once — so the 5-line slice is globally unique), the Runtime check row contains all three cell texts verbatim from R1 Block 2 including the embedded MUST statements (`For claim_class: static_defect, this dimension inherits the Evidence grounding score (static defects' source IS their runtime).` and `For claim_class: runtime_behavior or environment_dependent, source-only cards mandatorily score 0.0.`), the em-dash in the Runtime check 0.0 cell is U+2014, the backticks around `claim_class: static_defect`, `claim_class: runtime_behavior`, `environment_dependent`, and `static_defect` are preserved as inline-code, the new formula line is exactly `**Confidence** = \`min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)\`.` (note the entire RHS is wrapped in backticks per R1 Block 3 NEW text), the +0.30 buffer paragraph contains the MUST NOT statement `The gates apply unconditionally (no claim_class exemption)` verbatim, the asterisk-italicized `*below*` is preserved, and no content is fabricated beyond what R1 Blocks 2, 3, 4 explicitly state. If unable to complete due to non-unique `old_string` match, character-encoding drift, or any deviation from R1's paste-ready text, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.5:** Apply Edit 3 (anchors e + f MERGED) — INSERT Verdict-direction modifier (M3a) subsection + INSERT Claim-class × evidence-class cross-tab subsection

- [x] Read the file `01-change-a-spec-extraction.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/01-change-a-spec-extraction.md` Sections "Block 5 — REQUIRED-INSERT: `### Verdict-direction modifier (M3a)` subsection" and "Block 6 — REQUIRED-INSERT: `### Claim-class × evidence-class cross-tab [V2 merged]` subsection" to confirm the two paste-ready blocks including the cap table (REFUTE/REJECT → 0.70; AFFIRM → 0.84) in Block 5 and the full 6×6 cross-tab (rows: `runtime_behavior`, `environment_dependent`, `static_defect`, `doc_contract`, `config_value`, `mixed`; columns: `runtime_repro`, `runtime_trace`, `log_evidence`, `source_static`, `doc_static`, `none`) in Block 6 with the `[V2 merged]` provenance suffix preserved verbatim in the H3 heading, then read the file `02-target-file-state.md` at the same research/ path Section 5 "Recommended Edit Ordering" item 3 to confirm the merged-Edit strategy (this single Edit handles both anchors e and f to eliminate the composite-anchor risk of f-after-e, where f's anchor would otherwise depend on the exact closing text of the M3a subsection), then edit the file `escalation-rubric.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` using the Edit tool with `old_string` set to the 3-line slice (rounding line L21 + blank L22 + `## Escalation decision (Wave 2)` heading L23):

  ```
  Round to two decimals.

  ## Escalation decision (Wave 2)
  ```

  and `new_string` set to the post-edit block that (i) preserves the rounding line, (ii) inserts a blank line, (iii) inserts the entire `### Verdict-direction modifier (M3a)` subsection from R1 Block 5 verbatim, (iv) inserts a blank line, (v) inserts the entire `### Claim-class × evidence-class cross-tab [V2 merged]` subsection from R1 Block 6 verbatim, (vi) inserts a blank line, and (vii) preserves the `## Escalation decision (Wave 2)` H2 heading — producing the following block in the file (paste exactly, preserving every pipe, every backslash in `claim_class \ evidence_class`, every bold-marker, every backtick, every em-dash U+2014, every `×` U+00D7, and the `[V2 merged]` provenance suffix on the cross-tab H3):

  ```
  Round to two decimals.

  ### Verdict-direction modifier (M3a)

  After computing the gated-minimum confidence, apply this modifier when the card's frontmatter declares `claim_class: runtime_behavior` AND `runtime_check < 1.0`:

  | Verdict direction | Cap on calibrated confidence |
  |-------------------|------------------------------|
  | REFUTE / REJECT   | 0.70 |
  | AFFIRM            | 0.84 |

  Rationale: a wrong REFUTE on runtime behavior closes the investigation door (the H3 0.95-REFUTE case); a wrong AFFIRM is caught by CI. Source-only REFUTEs of runtime claims are the precise failure mode under repair and must not clear the 0.85 STOP gate. The 0.84 AFFIRM cap means source-only AFFIRMs of runtime claims still ESCALATE to Tier 2 (below the 0.85 STOP).

  ### Claim-class × evidence-class cross-tab [V2 merged]

  The Runtime check dimension score is derived from the (claim_class, evidence_class) pair declared in the card frontmatter:

  | claim_class \ evidence_class | runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none |
  |------------------------------|---------------|---------------|--------------|---------------|------------|------|
  | `runtime_behavior`           | 1.0           | 1.0           | 0.5          | **0.0**       | **0.0**    | **0.0** |
  | `environment_dependent`      | 1.0           | 1.0           | 0.5          | **0.0**       | **0.0**    | **0.0** |
  | `static_defect`              | 1.0           | 1.0           | 1.0          | inherits EG   | inherits EG | 0.0  |
  | `doc_contract`               | 1.0           | 1.0           | 1.0          | 0.5           | 1.0        | 0.0  |
  | `config_value`               | 1.0           | 1.0           | 1.0          | inherits EG   | inherits EG | 0.0  |
  | `mixed`                      | min of the two component classes' scores                                                          |

  The bolded cells (0.0) trigger the verdict-direction modifier when the card's verdict is REFUTE/REJECT.

  ## Escalation decision (Wave 2)
  ```

  ensuring the `old_string` matches uniquely (R2 confirms both `Round to two decimals.` and `## Escalation decision (Wave 2)` are globally unique single-occurrence strings, so the 3-line slice is unambiguous), the M3a H3 heading text is exactly `### Verdict-direction modifier (M3a)`, the cap table contains exactly two data rows (`REFUTE / REJECT | 0.70` and `AFFIRM | 0.84`), the trigger conditions are stated verbatim (`claim_class: runtime_behavior` AND `runtime_check < 1.0`), the rationale prose contains the verbatim MUST NOT statement `must not clear the 0.85 STOP gate` for source-only REFUTEs, the cross-tab H3 heading preserves the `[V2 merged]` provenance suffix verbatim, the 6×6 cross-tab includes all six claim_class row labels in the proposal's declared order (`runtime_behavior`, `environment_dependent`, `static_defect`, `doc_contract`, `config_value`, `mixed`), all six evidence_class column labels in the proposal's declared order (`runtime_repro`, `runtime_trace`, `log_evidence`, `source_static`, `doc_static`, `none`), the six bolded `**0.0**` cells (3 in row 1 + 3 in row 2) are preserved verbatim, the four `inherits EG` cells (static_defect × source_static/doc_static + config_value × source_static/doc_static) are preserved verbatim, the special `mixed` row collapses to a single merged-cell wide value `min of the two component classes' scores`, the closing prose `The bolded cells (0.0) trigger the verdict-direction modifier when the card's verdict is REFUTE/REJECT.` is preserved verbatim, the `×` symbol in `Claim-class × evidence-class` is U+00D7 (multiplication sign, NOT ASCII `x`), the backslash in `claim_class \ evidence_class` is a literal `\` character, and no content is fabricated beyond what R1 Blocks 5 and 6 explicitly state. If unable to complete due to non-unique `old_string` match, character-encoding drift on `×` or em-dashes, or any deviation from R1's paste-ready text, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.6:** Apply Edit 4 (anchor g) — INSERT new `source_only_dynamic_claim` sub-bullet under § 3 Signal-driven escalation

- [x] Read the file `01-change-a-spec-extraction.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/01-change-a-spec-extraction.md` Section "Block 7 — REQUIRED-INSERT: New escalation rule under § 3" to confirm the paste-ready single-bullet text and the trigger condition (`claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5` → ESCALATE with `escalation_reason: source_only_dynamic_claim`), then read the file `02-target-file-state.md` at the same research/ path Section 3 anchor (g) to confirm the unique-match `old_string` candidate (the 3-line slice from the `--type security` bullet through `4. **Default**` is globally unique because both `security_caution` and `4. **Default**` each appear only once), then edit the file `escalation-rubric.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` using the Edit tool with `old_string` set to the 3-line slice:

  ```
     - `--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`). Security bugs have asymmetric cost-of-being-wrong; raise the bar.

  4. **Default**
  ```

  and `new_string` set to the post-edit 4-line block that preserves the `--type security` bullet, inserts the new `source_only_dynamic_claim` sub-bullet immediately after it (using the same 3-space indent + `- ` prefix that the existing § 3 bullets use), preserves the blank line, and preserves `4. **Default**` — producing the following block in the file (paste exactly):

  ```
     - `--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`). Security bugs have asymmetric cost-of-being-wrong; raise the bar.
     - `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5` → ESCALATE (`escalation_reason: source_only_dynamic_claim`).

  4. **Default**
  ```

  ensuring the `old_string` matches uniquely (R2 confirms `security_caution` and `4. **Default**` are each globally unique strings, so the 3-line slice is unambiguous), the new bullet uses exactly 3 spaces of indent followed by `- ` (matching the existing § 3 bullet style at L35-L39 per R2 §2), the `∈` symbol is U+2208 (ELEMENT OF — single character, NOT `\in` or `in`), the `→` arrow is U+2192 (RIGHTWARDS ARROW — matching the existing § 3 bullets' arrows), the curly-brace literal `{runtime_behavior, environment_dependent}` is ASCII curly braces and ASCII comma-space, the backticked `claim_class`, `runtime_check < 0.5`, and `escalation_reason: source_only_dynamic_claim` are all wrapped in inline-code backticks, the bullet sentence ends with a period after the closing parenthesis, the new bullet does NOT introduce a trailing rationale clause (unlike the `security_caution` bullet which has one — the `source_only_dynamic_claim` bullet is rationale-free per R1 Block 7's paste-ready text), and no content is fabricated beyond what R1 Block 7 explicitly states. If unable to complete due to non-unique `old_string` match, character-encoding drift on `∈` or `→`, or any deviation from R1's paste-ready text, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 2: Sync mirror + verify drift + lint gate

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Each item depends on the previous item's success — `verify-sync` will FAIL if `sync-dev` has not yet run (per R3 §6 Gotcha 1), and the markdownlint hook will operate on the post-sync state of the source file.

**Step 2.1:** Run `make sync-dev` to mirror src/ → .claude/

- [x] Read the file `03-template-and-conventions.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/03-template-and-conventions.md` Section 2 "Sync-Dev + Verify-Sync Workflow" to confirm the verbatim Makefile target behavior (the `sync-dev` target is declared at `Makefile:109` and walks `src/superclaude/skills/*/` mirroring each skill into `.claude/skills/<name>/` while skipping `__init__.py` and `__pycache__`, which means the edited file at `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` will be copied to `.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`), then use the Bash tool to run the command `make sync-dev` from the worktree root `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/` (the directory containing this task file's parent `.dev/`, `Makefile`, and `src/`; per R3 §6 Gotcha 6 "Worktree CWD discipline", the executor MUST cd into the worktree root before invoking make — do NOT cd into the main checkout `/config/workspace/IronClaude/` because this task lives in the worktree), capturing both stdout and stderr and the exit code, ensuring the exit code is 0, the stdout contains the line `🔄 Syncing src/superclaude/ → .claude/ for local development...`, the stdout ends with a `✅ Sync complete.` success indicator (per R3 §2 the command prints status lines per component group and concludes successfully when no error is raised), and the `.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` mirror is now updated to match the post-Phase-1 src/ state. If unable to complete because the command exits non-zero, because make is not on PATH, or because the working directory is not the worktree root, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.2:** Run `make verify-sync` to confirm zero drift

- [x] Read the file `03-template-and-conventions.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/03-template-and-conventions.md` Section 2 (specifically the `verify-sync` subsection) to confirm the verbatim behavior — the target is declared at `Makefile:166` and uses bidirectional `diff -rq --exclude='__init__.py' --exclude='__pycache__'` to compare `src/superclaude/skills/*/` against `.claude/skills/*/`, flagging any `MISSING` or `DIFFERS` results and exiting 1 with `❌ Drift detected! Run 'make sync-dev' to fix...` if drift exists — and confirm R3 §6 Gotcha 1 which states `make sync-dev` MUST precede `make verify-sync` or this step will fail, then use the Bash tool to run the command `make verify-sync` from the worktree root `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/` (same root as Step 2.1), capturing both stdout and stderr and the exit code, ensuring the exit code is 0 (no drift), the stdout does NOT contain the substring `Drift detected`, no `MISSING` or `DIFFERS` lines are reported for the `sc-troubleshoot-protocol` skill, and the final line of output indicates all components in sync. If the command exits non-zero with `Drift detected`, re-run Step 2.1 exactly ONCE (a single re-run is the documented recovery path; if drift persists after one retry, treat as a blocker), then re-run this command and re-check exit code; if still non-zero, log the specific drift output using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.3:** Run markdownlint hook on the edited source file

- [x] Read the file `03-template-and-conventions.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/03-template-and-conventions.md` Section 3 "Markdownlint Hook" and Section 6 Gotchas 2 + 4 to confirm the hook configuration (declared at `.pre-commit-config.yaml:70-82`, uses `igorshubovych/markdownlint-cli@v0.38.0`, runs with `args: ['--fix']` meaning it may auto-modify the file — Change A inserts two new tables (the 6×6 cross-tab + the M3a cap table) plus three new H3 headings, all of which are prime auto-fix candidates for MD022 / MD058 / MD012; and `pre-commit` may not be on PATH so invoke via `uv run pre-commit`), then use the Bash tool to run the command `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` from the worktree root `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/` (same root as Step 2.1), capturing both stdout and stderr and the exit code, ensuring the final result is `Passed` (exit code 0 with no remaining violations), no MD-rule violations remain after any `--fix` modifications, and the post-lint file is still well-formed (no broken tables, no malformed headings). If `--fix` modifies the file (pre-commit reports `files were modified by this hook` which initially yields exit code 1), re-run `make sync-dev` and `make verify-sync` from Steps 2.1-2.2 a single time so the `.claude/` mirror reflects the lint fixes, then re-run the markdownlint command and confirm exit 0 on the second pass; if a second pass still exits non-zero with NEW violations (not "files were modified" but actual rule failures), log the specific violations using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. If `pre-commit` is not on PATH and `uv run pre-commit` also fails (PATH/tool resolution error), run `uv pip install pre-commit` first to install the tool into the worktree venv, then retry the lint command. Once done, mark this item as complete.

### Phase 3: Final structural verification (QA gate — executor-performed, per FINAL_ONLY)

This is the task's final QA gate per the BUILD_REQUEST's `QA_GATE_REQUIREMENTS: FINAL_ONLY` directive. The executor performs the verification directly — no rf-qa spawning is required (per-task-file QA gates A.10/A.10.5 in the task-builder skill already gated the task file itself, and the Change B precedent at PR #89 confirmed this FINAL_ONLY pattern works for single-file additive markdown edits).

**Step 3.1:** Final structural verification of edited target file

- [x] Read the target file `escalation-rubric.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` end-to-end and read the file `02-target-file-state.md` at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/02-target-file-state.md` Section 2 "Structural Map" plus Section 4 "Character-Encoding Notes" to confirm the expected post-edit invariants, then verify the following 7 structural checks in sequence: (a) the dimension table contains exactly 6 data rows (Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence, Runtime check — in that order); (b) the Evidence-grounding row's 1.0 cell ends with `(snippet match verified by calibrator's spot-check)` and does NOT contain the substring `OR diagnostic command output reproduces the symptom`; (c) the formula line is exactly `**Confidence** = \`min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)\`.` (entire RHS backticked) and the legacy substring `arithmetic mean of the five dimension scores` is absent from the file; (d) both new H3 subsections are present in proposal order between `Round to two decimals.` and `## Escalation decision (Wave 2)` — first `### Verdict-direction modifier (M3a)` containing the REFUTE/REJECT → 0.70 and AFFIRM → 0.84 cap table, then `### Claim-class × evidence-class cross-tab [V2 merged]` containing the 6×6 table with the `[V2 merged]` provenance suffix preserved verbatim in the H3 heading; (e) the new `source_only_dynamic_claim` sub-bullet is present under § 3 (Signal-driven escalation) between the `--type security` bullet and `4. **Default**`, with the trigger condition `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5`; (f) character encodings are preserved — every em-dash is U+2014, every `→` arrow is U+2192, every `≥` is U+2265 (existing), every `≤` is U+2264, every `∈` is U+2208, every `×` (in the cross-tab H3 heading) is U+00D7; verify by running Bash `grep -P "[\x{2014}\x{2192}\x{2264}\x{2208}\x{00D7}]" src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md | head -20` and inspecting; (g) the trailing rationale sections `## Why 0.85?` (pre-edit L44-48) and `## What escalation does NOT mean` (pre-edit L50-52) remain byte-identical to the pre-edit state (Change A does not touch them — verify by reading the post-edit file's last 9 lines and comparing against R2 §2 L44-52); and additionally (h) total line count is in the expected post-edit range of approximately 85-100 lines (baseline 52 + Block 2 ~1 + Block 3 0 (replace) + Block 4 ~3 + Block 5 ~10 + Block 6 ~14 + Block 7 ~1 ≈ 29-32 added lines; final range allowing for blank-line spacing variation), confirmed via Bash `wc -l src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`, ensuring all 7 edits landed correctly in the prescribed order, all character encodings are preserved, the trailing rationale sections are untouched, the line count is in range, and no fabricated structural state is assumed. If any check fails, log the specific failure using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file (include which check (a-h) failed and the observed vs expected state), then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

- [x] Verify all task outputs by using the Bash tool to confirm via `ls -l /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` that both the source file and the sync mirror exist on disk, then use the Bash tool to run `wc -l /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` and confirm the line count is in the expected range 85-100 lines, then use the Bash tool to run `diff /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` and confirm the diff is empty (zero-byte difference between src/ and .claude/ mirror), ensuring no expected deliverable is missing. If any file is missing or the mirror diverges from the source, log the gap in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item as complete.

- [x] This task did NOT modify source code (it modified a Markdown documentation file). Per `TESTING_REQUIREMENTS: NONE` in the BUILD_REQUEST, no test suite execution is required. Add a single line `**[2026-05-27 HH:MM]** - Testing skipped: documentation-only edit (TESTING_REQUIREMENTS: NONE per BUILD_REQUEST).` to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file. Once done, mark this item as complete.

- [x] Create the ### Task Summary section content at the top of the ## Task Log / Notes section at the bottom of this task file using the template format already provided there (Completion Date, Work Completed bullets, Challenges Encountered, Deviations from Process, Blockers Logged with status, Follow-Up Required). The summary MUST document: (a) the target file was edited with the 7 Change A structural changes (Evidence-grounding 1.0 cell narrowing, Runtime check 6th dimension row, gated-minimum formula replacement, +0.30 buffer prose paragraph, Verdict-direction modifier (M3a) subsection with cap table, Claim-class × evidence-class cross-tab [V2 merged] subsection with 6×6 table, source_only_dynamic_claim escalation rule), applied via 4 Edit-tool calls per research file 02's recommended ordering; (b) the src/ → .claude/ sync was completed and verified drift-free; (c) the markdownlint hook passed on the edited file; (d) the trailing rationale sections (`## Why 0.85?` and `## What escalation does NOT mean`) were intentionally left untouched per Change A's scope (these sections are not part of the rubric formula being updated); (e) Change A unblocks Change C (calibrator scoring), Change F (audit gate), and Change E (eval corpus) in the sequenced A→B→C→F→E rollout; (f) the dangling cross-reference from Change B (PR #89) to `escalation-rubric § Verdict-direction modifier` is now resolved by Block 5's M3a subsection landing. Once the summary is complete, mark this item as complete.

- [x] Update the `completion_date` field in this task file's frontmatter to today's date `2026-05-27`, update the `updated_date` field to the same date, update the `status` field to "🟢 Done", then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[2026-05-27 HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary

**Completion Date:** 2026-05-27

**Work Completed:**

- Applied all 7 Change A structural edits to `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` via the 4 Edit-tool calls recommended by research file 02: (1) REPLACED Evidence-grounding 1.0 cell to drop the `OR diagnostic command output reproduces the symptom` clause and add the `(snippet match verified by calibrator's spot-check)` qualifier; (2) INSERTED new `**Runtime check**` 6th dimension row with claim-class-aware 0.0 scoring rules embedded; REPLACED formula with the gated-minimum `**Confidence** = \`min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)\`.`; INSERTED +0.30 buffer prose paragraph (all merged in Edit 2); (3) INSERTED `### Verdict-direction modifier (M3a)` H3 subsection with REFUTE/REJECT → 0.70 and AFFIRM → 0.84 cap table; INSERTED `### Claim-class × evidence-class cross-tab [V2 merged]` H3 subsection with the full 6×6 derivation table (both merged in Edit 3 to eliminate composite-anchor risk); (4) INSERTED new `source_only_dynamic_claim` sub-bullet under § 3 Signal-driven escalation.
- `make sync-dev` exit 0 and `make verify-sync` exit 0 — `.claude/` mirror is byte-identical to `src/`.
- `uv run pre-commit run markdownlint` returned `Passed` on first attempt against the edited file (no --fix mutations).
- The pre-edit trailing rationale sections (`## Why 0.85?` at L74-78, `## What escalation does NOT mean` at L80-82) were intentionally left untouched per Change A scope — verified byte-identical to baseline.
- Files modified:
  - `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (52 → 82 lines)
  - `.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (sync-mirror update, identical to src/)

**Challenges Encountered:**

- During Step 1.1's frontmatter status update, an initial Edit created a duplicate `start_date` key after the `updated_date` line. Discovered immediately via `grep -n "start_date"` showing two occurrences (L10 + L40). Corrected by removing the spurious top-of-block insertion and updating the canonical `start_date: ""` field at the dated-fields cluster (L40) to `start_date: "2026-05-27"`. No downstream impact.

**Deviations from Process:**

- Final line count is 82 vs. the task's stated "approximately 85-100" range. Within the block-derived expectation (52 baseline + 29-32 added ≈ 81-84 lines), so consistent with per-block additions; the 85-100 was a conservative outer bound. Logged in Phase 3 Findings; no structural anomaly.

**Blockers Logged:**

- None — all phases completed cleanly without blockers.

**Follow-Up Required:** Yes — the four follow-up items already listed in `### Follow-Up Items Identified` below remain active (Change C calibrator scoring [High], Change F audit gate [High], Change E eval corpus [Medium], hypothesis-card-template.md "seven above" → "six above" cleanup [Low]). Change A unblocks the A→B(shipped)→C→F→E sequence — Change C is the next-step priority.

### Risks / Known Limitations / Open Questions

These items were identified during task planning by the rf-task-builder and MUST be carried forward as-is by the executor. They are NOT blockers for this task; they are intentional scope decisions and forward-looking gaps tied to the sequenced A→B→C→F→E rollout.

1. **Change A in isolation lands a rubric that no consumer yet computes against.** Change A defines the gated-minimum formula, the M3a verdict-direction modifier, the cross-tab derivation, and the `source_only_dynamic_claim` escalation rule — but the actual computation lives in the calibrator agent which is updated by Change C (deferred to a follow-up task build). After Change A lands, the rubric reads correctly but cards calibrated under the old `confidence-calibrator` will still use the arithmetic-mean formula until Change C ships. This is intentional per the sequenced A→B→C→F→E rollout; acceptance for THIS task is limited to "the rubric template includes the new dimension row, formula, subsections, and escalation rule in the specified order" — NOT "the calibrator computes confidence using the new formula" (that is Change C). Source: BUILD_REQUEST WHY clause and the proposal at `.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` L43-109.

2. **Cross-references between Change B and Change A now resolve.** Change B (PR #89 / commit 46d3b342) inserted a forward reference in the Verdict direction frontmatter sub-bullet: `(see escalation-rubric § Verdict-direction modifier)`. Until Change A landed, this was a dangling reference. Block 5 of Change A creates the `### Verdict-direction modifier (M3a)` subsection that resolves this reference. After Change A ships, the cross-link is valid. No executor action needed beyond confirming Block 5 (anchor e) lands via Step 1.5 and the H3 heading text is exactly `### Verdict-direction modifier (M3a)`. Source: research file 01 Block 5 + Change B done-task body §299 Risks item 4.

3. **The trailing rationale sections (`## Why 0.85?` and `## What escalation does NOT mean`) are intentionally untouched.** These sections at the file's tail (pre-edit L44-52) explain the 0.85 STOP threshold rationale and clarify what escalation does and does not mean for the operator. Change A's scope is the rubric formula and the signal-driven escalation rule — NOT the rationale prose. The +0.30 buffer prose paragraph inserted in Block 4 partially overlaps with `## Why 0.85?` semantically but the proposal deliberately keeps both: the buffer prose belongs to the calibration formula explanation, the Why-0.85 section belongs to the escalation-threshold rationale. The executor MUST verify (via Step 3.1 check g) that these trailing sections remain byte-identical post-edit. Source: research file 02 Section 2 L44-52 + proposal L43-109 scope demarcation.

4. **The cross-tab `mixed` row uses a merged-cell wide value.** Block 6's 6×6 cross-tab has 5 normal rows with 6 numeric values each, plus a 6th `mixed` row that collapses to a single merged-cell wide value `min of the two component classes' scores`. The pipe layout for this row is non-standard markdown table syntax (the cell content spans the remaining columns rather than providing 6 explicit values). Markdownlint may flag this with MD058 (table column consistency) or may accept it as-is. If markdownlint --fix reformats this row, accept the auto-fix; if --fix breaks the semantic intent, the executor should log the issue in Phase 2 Findings and either revert the auto-fix manually OR accept the lint output as the canonical form. Per Change B precedent, --fix did not modify the file at all, so this risk is low but explicitly flagged. Source: research file 01 Block 6 "Special row: `mixed` collapses to a single merged cell".

5. **Hidden character drift between proposal source and editor paste is the highest-probability failure mode.** The proposal at `CROSS-ENV-PROPOSAL-MERGED.md` L43-109 contains U+2014 em-dashes, U+2208 `∈`, U+00D7 `×`, and possibly U+2264 `≤` and U+27F9 `⟹`. If the executor's terminal or clipboard normalizes any of these to ASCII (`--`, `\in`, `x`, `<=`, `=>`), the Edit will land malformed text. Each per-Edit checklist item explicitly states the required codepoints; Step 3.1 check (f) provides a grep-based verification. If a character mismatch is detected post-edit, the executor must re-do the affected Edit with explicit codepoint verification (e.g., paste from research file 01 directly rather than re-typing). Source: research file 02 Section 4 "Character-Encoding Notes" + research file 03 Section 6 Gotchas.

6. **Carried-forward off-by-one defect in Change B (PR #89) — `<one of the seven above>` placeholder, but only six claim classes are enumerated.** The shipped Change B (PR #89, commit 46d3b342) at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` L86 contains the prose `**Claim class**: <one of the seven above> — <one-line reason>`, but the enumeration at L16 lists only SIX claim classes (`static_defect`, `runtime_behavior`, `environment_dependent`, `config_value`, `doc_contract`, `mixed`). The "seven" wording was likely a proposal-drafting artifact (perhaps an earlier draft included an additional class that was dropped before V2 merge), and it was carried through Change B's PR review without correction. This is OUT OF SCOPE for Change A (Change A only modifies escalation-rubric.md, not hypothesis-card-template.md). The defect does NOT affect Change A's correctness — Change A's new 6×6 cross-tab subsection (Block 6) consumes the six-value enumeration correctly. A separate cleanup task should change `<one of the seven above>` to `<one of the six above>` (or the more durable phrasing `<one of the enumerated claim classes>`) in hypothesis-card-template.md L86. Flagged here so the executor knows not to "helpfully" fix it during Change A execution (out-of-scope edit = scope creep) and so a follow-up cleanup item is captured for tracking. Source: Direct read of hypothesis-card-template.md L16 (six-value enumeration) vs L86 (seven-value claim); identified during QA qualitative review of this task.

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[2026-05-27 06:08]** - Task started: Updated status to "🟠 Doing" and start_date.

**[2026-05-27 06:09]** - Phase 1 complete: All 4 Edit-tool calls landed cleanly on src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md (Edit 1 = anchor a EG cell; Edit 2 = anchors b+c+d merged Runtime check row + gated-min formula + +0.30 buffer; Edit 3 = anchors e+f merged M3a + cross-tab; Edit 4 = anchor g source_only_dynamic_claim bullet).

**[2026-05-27 06:10]** - Phase 2 complete: `make sync-dev` exit 0 (23 skills mirrored); `make verify-sync` exit 0 ("All components in sync"); `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` returned `Passed` on first attempt (no --fix mutations needed).

**[2026-05-27 06:11]** - Phase 3 complete: All 7 structural checks (a-g) pass; check (h) line count = 82 (slightly below the task-stated 85-100 range but within block-derived +29-32 line estimate; logged in Phase 3 Findings). Trailing rationale sections (`## Why 0.85?`, `## What escalation does NOT mean`) byte-identical to pre-edit state.

**[2026-05-27 06:13]** - Testing skipped: documentation-only edit (TESTING_REQUIREMENTS: NONE per BUILD_REQUEST).

**[2026-05-27 06:14]** - Task completed: Updated status to "🟢 Done" and completion_date.

### Phase 1 - Edit target file Findings

<!-- TEMPLATE FOR PHASE FINDINGS:
**[YYYY-MM-DD HH:MM]** - [Step X.Y]: [Finding or blocker description]
- **Status:** [Completed | Blocked]
- **Details:** [Specific information about what was found, created, or what blocked completion]
- **Blocker Reason (if blocked):** [Specific reason why this could not be completed]
- **Files Affected:** [List of files read, created, or modified]
-->

### Phase 2 - Sync + verify + lint Findings

<!-- TEMPLATE FOR BLOCKER ENTRIES:
**[YYYY-MM-DD HH:MM]** - Step 2.1 BLOCKED:
- **Blocker Reason:** [Specific reason - e.g., "make sync-dev exited with code 1; stderr reported: <paste-text>"]
- **Attempted:** [What was tried before determining blocker]
- **Required to Unblock:** [What information or action is needed to proceed]
-->

### Phase 3 - Final structural verification Findings

<!-- Use this section to log structural-check failures from Step 3.1, including which sub-check (a-h) failed and the observed vs expected state. -->

**[2026-05-27 06:10]** - Step 3.1: ALL 7 structural checks pass (a-g); check (h) line-count note:
- **Status:** Completed
- **Details:** Checks (a-g) all pass. Dimension table has 6 data rows in correct order (EG, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence, Runtime check). EG 1.0 cell ends with `(snippet match verified by calibrator's spot-check)` and legacy `OR diagnostic command output reproduces the symptom` substring is absent. Formula line is the backticked gated-minimum form; legacy `arithmetic mean of the five dimension scores` substring is absent. Both new H3 subsections present in proposal order between `Round to two decimals.` and `## Escalation decision (Wave 2)`. `source_only_dynamic_claim` sub-bullet present under § 3 between `--type security` and `4. **Default**`. Character encodings preserved: U+2014 em-dash (4), U+2192 arrow (10), U+2208 ∈ (1), U+00D7 × (1), U+2265 ≥ (1). Trailing `## Why 0.85?` and `## What escalation does NOT mean` sections intact.
- **Sub-check (h) note:** Final line count is 82, slightly below the task's stated "approximately 85-100" range. Per the task's own arithmetic (52 baseline + ~29-32 added lines = 81-84), 82 is exactly in that block-derived range. The 85-100 figure was a conservative outer-bound estimate; +30 added lines is consistent with block-by-block additions (Block 2 +1, Block 4 +2, Block 5 +10, Block 6 +14, Block 7 +1 ≈ +28 + blank-line spacing). No structural anomaly.
- **Files Affected:** `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (read for verification).

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

- **[Priority: High]** Build and ship Change C (calibrator scoring update) so cards are actually calibrated using the new gated-minimum formula, M3a modifier, cross-tab derivation, and `source_only_dynamic_claim` escalation rule that Change A defines. — Identified in Risks/Open Questions item 1.
- **[Priority: High]** Build and ship Change F (audit gate) to enforce the completed rubric. — Identified in Risks/Open Questions item 1.
- **[Priority: Medium]** Build and ship Change E (eval corpus) to validate that calibrator output under the new formula matches expected scores on a curated set of cards. — Identified in Risks/Open Questions item 1.
- **[Priority: Low]** Fix the carried-forward off-by-one defect in `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` L86 — change `<one of the seven above>` to `<one of the six above>` (or `<one of the enumerated claim classes>` for durability). The enumeration at L16 lists only six claim classes (`static_defect`, `runtime_behavior`, `environment_dependent`, `config_value`, `doc_contract`, `mixed`); the "seven" wording is a proposal-drafting artifact carried through Change B / PR #89 (commit 46d3b342) without correction. Out of scope for Change A (which only touches escalation-rubric.md). — Identified in Risks/Open Questions item 6.

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->
