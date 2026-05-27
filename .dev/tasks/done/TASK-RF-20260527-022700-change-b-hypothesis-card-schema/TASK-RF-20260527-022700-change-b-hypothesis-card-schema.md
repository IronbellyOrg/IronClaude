---
id: "TASK-RF-20260527-022700-change-b-hypothesis-card-schema"
title: "Change B — Apply additive hypothesis-card schema (Claim class, Evidence class, Verdict direction, Runtime check, Falsification standard, Evidence classification, optional Recommended evidence shape)"
description: "Implement Change B from the calibration-refactor cross-environment merged proposal. Apply five additive schema insertions to the single target file src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md (three frontmatter fields, one per-dimension Runtime check row, two new sections plus one optional preview section), then sync src/ → .claude/ via make sync-dev, verify via make verify-sync, and confirm pre-commit markdownlint passes. No behavior change — schema slots are additive and downstream consumers (Changes A rubric, C calibrator, F audit gate) are deferred to follow-up task builds."
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
depends_on: []
related_docs:
- path: ".dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md"
  description: "Source proposal containing Change B specification (L110-186)"
- path: "src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md"
  description: "Sole target file for this task — all edits land here"
- path: "Makefile"
  description: "Defines sync-dev (L109) and verify-sync (L166) targets"
- path: ".pre-commit-config.yaml"
  description: "Defines markdownlint hook (L70-82) and block-claude-generated-mirrors hook (L102-109)"
tags:
- "calibration-refactor"
- "hypothesis-card"
- "schema-additive"
- "change-b"
- "pr86-followup"
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

# Change B — Apply additive hypothesis-card schema (Claim class, Evidence class, Verdict direction, Runtime check, Falsification standard, Evidence classification, optional Recommended evidence shape)

## Task Overview

This task implements Change B from the calibration-refactor cross-environment merged proposal. The proposal defines a four-change loop (A, B, C, F) that closes a calibration gap exposed by PR #86 around source-vs-runtime evidence conflation. Change B is the second step in the sequenced rollout — it lands the additive schema slots in the canonical hypothesis-card template so that Changes A (rubric formula), C (calibrator scoring), and F (audit gate) can be built on top of a stable card shape.

The edit is fully additive: three new frontmatter fields are inserted as a contiguous group inside the existing frontmatter block, one new per-dimension self-assessment row is inserted between two existing rows, two new required sections are appended after the existing "If I'm wrong" section but before "Alternatives considered", and one optional-but-recommended preview section is appended in the same region. No existing field, row, or section is replaced or removed. The worked example near the end of the file is intentionally left untouched per the proposal's Migration note (v1.0 cards remain valid via calibrator defaults).

After the edits land, the task runs `make sync-dev` to mirror `src/` into `.claude/`, `make verify-sync` to confirm zero drift, and the pre-commit markdownlint hook against the single edited file to confirm it passes the lint gate. The expected final state is the source file grown from 108 lines to approximately 138-153 lines (Insertion Block 1 adds ~16, Block 2 adds 1, Block 3 adds ~3, Block 4 adds ~8, Block 5 adds ~13), the `.claude/` mirror reflecting the new content, and a clean lint pass.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Apply five additive insertions to the target file:** insert three frontmatter fields (Claim class, Evidence class, Verdict direction) as a contiguous group after `**Cause class**` and before `**Consistency with docs**`; insert one Runtime check row after `- Evidence grounding:` and before `- Symptom coverage:`; insert two required new sections (`## Falsification standard`, `## Evidence classification [V2 merged]`) and one optional preview section (`## Recommended evidence shape (v2.0 preview)`) after the "If I'm wrong" body and before `## Alternatives considered`. All five blocks must be pasted verbatim from the research spec including the off-by-one prose defect (`<one of the seven above>`) which is flagged as a known prose defect to carry forward.
2. **Sync `src/` → `.claude/` cleanly:** run `make sync-dev` and confirm the success path; run `make verify-sync` and confirm exit 0 with no drift reported.
3. **Pass the markdownlint gate on the edited file:** run `pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` and confirm exit 0; if the hook's `--fix` flag modifies the file, re-run `make sync-dev` and `make verify-sync` so the `.claude/` mirror stays consistent.
4. **Preserve invariants:** the template code-fence boundaries (open fence at the schema region's leading boundary, close fence at the schema region's trailing boundary) remain intact; the worked example block remains untouched; the file's total line count lands in the expected 138-153 range (baseline 108 + roughly 30-45 added lines).

## Prerequisites & Dependencies

### Parent Task & Dependencies

- **Parent Task:** (None — standalone follow-up to PR #86)
- **Blocking Dependencies:** None — research is complete; all paste-ready insertion blocks are captured verbatim in the research directory.
- **This task blocks:** Change A (rubric formula update), Change C (calibrator scoring update), Change F (audit gate) — all three deferred to follow-up task builds and all three depend on Change B's schema slots existing in the canonical template.

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY — NO CHECKLIST ITEMS HERE**

Required inputs for this task are the three research files in the `research/` subdirectory; each is referenced inline by the action item that consumes it. They are:

- **Target file state:** `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/01-target-file-state.md` — Purpose: byte-level state of the target file, unique-match `old_string` candidates for all three insertion anchors, code-fence boundary analysis, and the verbatim-captured surrounding context for each anchor.
- **Source spec extraction:** `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/02-change-b-spec-extraction.md` — Purpose: the five paste-ready Insertion Blocks (with leading `+` stripped from the proposal diff) plus REQUIRED/OPTIONAL classification, final ordering rules, enum-count discrepancy note, and verbatim MUST/MUST NOT statements that must land in the target file.
- **Template and conventions:** `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/03-template-and-conventions.md` — Purpose: Template 01 selection rationale, verbatim Makefile target locations for `sync-dev` and `verify-sync`, pre-commit markdownlint hook configuration, source-of-truth rule (edit `src/` not `.claude/`), and known gotchas (sync order, `--fix` may modify file, `block-claude-generated-mirrors` blocks `.claude/` paths from being staged).

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
- R-001 calibration-refactor cross-environment merged proposal — Change B specification (paste-ready insertion blocks)
- R-002 sc-troubleshoot-protocol hypothesis-card template — sole target file for this task
- R-003 Makefile sync-dev + verify-sync targets — defines the mirror and drift-check workflow
- R-004 pre-commit markdownlint hook + block-claude-generated-mirrors hook — defines the lint gate and the staging guard
- R-005 task research notes in this task's research/ directory — three files capturing target state, spec extraction, and conventions

---

## Detailed Task Instructions

### Phase 1: Edit target file

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status

- [x] Update the `status` field in this task file's frontmatter to "🟠 Doing" and set the `start_date` field to today's date `2026-05-27`, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[2026-05-27 HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Baseline read + sanity check

- [x] Read the file `01-target-file-state.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/01-target-file-state.md` (specifically Sections 2 "Structural map", 3 "Anchor verbatim capture", and 4 "Code-fence boundary analysis") to confirm the expected baseline state of the target file including the L9 opening template fence, the L12-16 frontmatter block ending with `**Consistency with docs**`, the L48-53 per-dimension self-assessment block, the L59-61 "If I'm wrong" section, the L70 closing template fence, and the L81-108 worked-example block that MUST remain untouched, then read the target file `hypothesis-card-template.md` at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` end-to-end and verify that (a) line count is 108 lines, (b) the L12-16 frontmatter block matches R1 §3a verbatim, (c) the L48-53 per-dimension self-assessment block matches R1 §3b verbatim, (d) the L59-61 "If I'm wrong" section matches R1 §3c verbatim, (e) the worked example fence opens at L81 and closes at L108, ensuring no drift has occurred since research was captured, no fabricated baseline state is assumed, and the three insertion anchors are confirmed present. If unable to complete due to file access issues, byte-level mismatch between R1 and the actual file, or unclear baseline state, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.3:** Apply Insertion Block 1 — frontmatter additions (Claim class + Evidence class + Verdict direction)

- [x] Read the file `02-change-b-spec-extraction.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/02-change-b-spec-extraction.md` Section 2 "Insertion Block 1 — Frontmatter additions" to confirm the paste-ready text, then read the file `01-target-file-state.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/01-target-file-state.md` Section 6 "Insertion point (a)" to confirm the unique-match `old_string` anchor, then edit the file `hypothesis-card-template.md` at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` using the Edit tool with `old_string` set to the two-line slice `**Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">\n**Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>` and `new_string` set to the same two lines with the three new frontmatter fields inserted between them as a contiguous group, producing the following 18-line block in the file (paste exactly, preserving every backtick, every em-dash U+2014, every pipe, and every bold marker):

  ```
  **Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
  **Claim class**: `static_defect` | `runtime_behavior` | `environment_dependent` | `config_value` | `doc_contract` | `mixed`
    — `static_defect`: source-reading alone is sufficient evidence (typos, missing imports, regex literals, syntax errors)
    — `runtime_behavior`: claim depends on dynamic control flow, side effects, executed semantics, or library call dispatch
    — `environment_dependent`: claim depends on OS / runtime / feature-flag / network / data state
    — `config_value`: claim depends on configuration / settings / env vars
    — `doc_contract`: claim depends on a documented contract (RFC, spec, README)
    — `mixed`: spans more than one class
  **Evidence class**: `runtime_repro` | `runtime_trace` | `log_evidence` | `source_static` | `doc_static` | `none`
    — `runtime_repro`: executed reproducer with captured stdout/stderr
    — `runtime_trace`: live execution trace, debugger output, instrumentation log
    — `log_evidence`: post-hoc log excerpt from the failing run
    — `source_static`: source file Read + cited line (no execution)
    — `doc_static`: documentation citation (no execution, no source)
    — `none`: prose only / no evidence
  **Verdict direction**: `AFFIRM` | `REFUTE` | `REJECT`
    — REFUTE/REJECT verdicts on `runtime_behavior` claims face a higher calibration bar (see escalation-rubric § Verdict-direction modifier).
  **Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>
  ```

  ensuring the `old_string` matches uniquely (R1 confirms this 2-line slice appears only at L15-16 because the worked example at L87 omits `**Consistency with docs**:`), the three new frontmatter fields land as a contiguous group between `**Cause class**` and `**Consistency with docs**`, all six Claim-class enum values are present in the exact order from R2 §2, all six Evidence-class enum values are present, all three Verdict-direction enum values are present, every em-dash is U+2014 (not double-hyphen ASCII), every backtick wraps the enum value literal, no content is fabricated beyond what R2 §2 explicitly states, and no placeholder text remains. If unable to complete due to non-unique `old_string` match, file access issues, or character-encoding drift, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.4:** Apply Insertion Block 2 — Runtime check per-dimension row

- [x] Read the file `02-change-b-spec-extraction.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/02-change-b-spec-extraction.md` Section 3 "Insertion Block 2 — Per-dimension dimension row" to confirm the paste-ready text, then read the file `01-target-file-state.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/01-target-file-state.md` Section 6 "Insertion point (b)" to confirm the unique-match `old_string` anchor, then edit the file `hypothesis-card-template.md` at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` using the Edit tool with `old_string` set to the two-line slice `- Evidence grounding: <0.0|0.5|1.0> — <one-line reason>\n- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>` and `new_string` set to the same two lines with the new Runtime check row inserted between them, producing the following three-line block in the file (paste exactly):

  ```
  - Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
  - Runtime check: <0.0|0.5|1.0> — <derived from (claim_class, evidence_class) cross-tab; cite the executed-reproducer command + captured output, OR cite a runtime-asserting test by name + its execution state. For claim_class=static_defect, mark "inherits Evidence grounding" with no further evidence required.>
  - Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
  ```

  ensuring the `old_string` matches uniquely (R1 confirms these two dimension labels appear only at L49-50), the new Runtime check row lands between `Evidence grounding` and `Symptom coverage`, the em-dash is U+2014, the bullet uses `- ` (hyphen + single space), the parenthetical `(claim_class, evidence_class)` is literal (not curly-quoted), the static_defect fallback clause is preserved verbatim, and no content is fabricated beyond what R2 §3 explicitly states. If unable to complete due to non-unique `old_string` match or character-encoding drift, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.5:** Apply Insertion Block 3 — `## Falsification standard` section

- [x] Read the file `02-change-b-spec-extraction.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/02-change-b-spec-extraction.md` Section 4 "Insertion Block 3 — `## Falsification standard` section" to confirm the paste-ready text, then read the file `01-target-file-state.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/01-target-file-state.md` Section 6 "Insertion point (c)" to confirm the unique-match `old_string` anchor, then edit the file `hypothesis-card-template.md` at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` using the Edit tool with `old_string` set to the three-line slice `One sentence. The agent's best guess at the next-most-likely explanation if this hypothesis is wrong. This is what the Tier 2 fan-out uses to choose complementary agents.\n\n## Alternatives considered` and `new_string` set to the same opening prose sentence, a blank line, the new `## Falsification standard` section (heading + blank + body paragraph), a blank line, and the existing `## Alternatives considered` heading, producing the following block in the file (paste exactly):

  ```
  One sentence. The agent's best guess at the next-most-likely explanation if this hypothesis is wrong. This is what the Tier 2 fan-out uses to choose complementary agents.

  ## Falsification standard

  One sentence. What concrete evidence — an executable command and expected output, a named test outcome, a log assertion, or a measurable observation — would prove this hypothesis WRONG? "Re-reading the source differently" is NOT a falsification standard. If you cannot name a falsification standard, the claim_class is `runtime_behavior` and Runtime check self-scores ≤ 0.5.

  ## Alternatives considered
  ```

  ensuring the `old_string` matches uniquely (R1 confirms the prose sentence appears only at L61), the new section is sandwiched between the "If I'm wrong" body and `## Alternatives considered`, the apostrophe in "agent's" is straight ASCII U+0027, the em-dash in the body is U+2014, the `≤` symbol is U+2264 (single character, not `<=`), the inline backtick wrapping `runtime_behavior` is preserved, the MUST/MUST NOT statements from R2 §10 ("`Re-reading the source differently' is NOT a falsification standard" and "If you cannot name a falsification standard...") are present verbatim, and no content is fabricated beyond what R2 §4 explicitly states. If unable to complete due to non-unique `old_string` match or character-encoding drift, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.6:** Apply Insertion Block 4 — `## Evidence classification [V2 merged]` section

- [x] Read the file `02-change-b-spec-extraction.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/02-change-b-spec-extraction.md` Section 5 "Insertion Block 4 — `## Evidence classification [V2 merged]` section" to confirm the paste-ready text and the explicit cap value 0.65, then edit the file `hypothesis-card-template.md` at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` using the Edit tool with `old_string` set to the three-line slice that now bounds the trailing edge of the Falsification standard section (the post-1.5 state) — specifically `If you cannot name a falsification standard, the claim_class is \`runtime_behavior\` and Runtime check self-scores ≤ 0.5.\n\n## Alternatives considered` — and `new_string` set to the same closing prose sentence, a blank line, the new `## Evidence classification [V2 merged]` section (heading + blank + four-bullet block + blank + Filling-rule prose paragraph), a blank line, and the existing `## Alternatives considered` heading, producing the following block in the file (paste exactly):

  ```
  If you cannot name a falsification standard, the claim_class is `runtime_behavior` and Runtime check self-scores ≤ 0.5.

  ## Evidence classification [V2 merged]

  - **Claim class**: <one of the seven above> — <one-line reason>
  - **Evidence class**: <one of the six above> — <one-line reason>
  - **Runtime check performed?**: yes | no — <if no, one-line reason why not>
  - **If REFUTE verdict, coverage statement**: <which paths/files/conditions were inspected; explicitly name anything not inspected that could flip the verdict>

  Filling rule: an empty or "Not applicable" value on `evidence_class` is a defect; cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale.

  ## Alternatives considered
  ```

  ensuring the `old_string` is now unique because Step 1.5's insertion made the prose sentence end with `≤ 0.5.` immediately followed by a blank line and `## Alternatives considered` (this combination exists only once in the file), the new section's `[V2 merged]` provenance suffix is preserved verbatim per R2 §9, the prose `<one of the seven above>` is pasted VERBATIM despite being a known off-by-one defect (the actual Claim class enum has six values — this defect is documented in R2 §2 as a carry-forward to flag in Risks), the `∈` symbol is U+2208 (single character, not `\in` or `in`), the cap value is exactly `0.65` (not `0.70`, not `0.80`), the MUST statement "MUST self-cap their confidence at 0.65" is present verbatim, the "Not applicable" defect statement is present verbatim, and no content is fabricated beyond what R2 §5 explicitly states. If unable to complete due to non-unique `old_string` match, character-encoding drift, or the prior insertion in Step 1.5 not landing as expected, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.7:** Apply Insertion Block 5 — `## Recommended evidence shape (v2.0 preview)` section

- [x] Read the file `02-change-b-spec-extraction.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/02-change-b-spec-extraction.md` Section 6 "Insertion Block 5 — `## Recommended evidence shape (v2.0 preview)` section" to confirm the paste-ready text and the v1.5-OPTIONAL / v2.0-MANDATORY framing, then edit the file `hypothesis-card-template.md` at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` using the Edit tool with `old_string` set to the trailing edge of the Evidence classification section (the post-1.6 state) — specifically `Filling rule: an empty or "Not applicable" value on \`evidence_class\` is a defect; cards with \`claim_class: runtime_behavior\` AND \`evidence_class ∈ {source_static, doc_static, none}\` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale.\n\n## Alternatives considered` — and `new_string` set to the same Filling-rule prose paragraph, a blank line, the new `## Recommended evidence shape (v2.0 preview)` section (heading + blank + intro paragraph + blank + typed table + blank + Kinds bullet + blank + v1.5-OPTIONAL / v2.0-MANDATORY closing paragraph), a blank line, and the existing `## Alternatives considered` heading, producing the following block in the file (paste exactly, preserving every pipe `|`, every dash in the table separator row, and the bold markers in `**OPTIONAL in v1.5**` and `**MANDATORY in v2.0**`):

  ```
  Filling rule: an empty or "Not applicable" value on `evidence_class` is a defect; cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale.

  ## Recommended evidence shape (v2.0 preview)

  For new cards, the recommended evidence shape is a typed table that makes each item's evidence kind explicit:

  | # | Kind | Source | Content |
  |---|------|--------|---------|
  | E1 | `source_citation` | `path/to/file.py:142` | (verified snippet) |
  | E2 | `executed_reproducer` | `uv run python -c "..."` | (captured stdout/stderr) |
  | E3 | `test_assertion` | `tests/.../test_x::test_y` | (execution state: fails / passes / not-run) |

  Kinds: `source_citation`, `executed_reproducer`, `test_assertion`, `documentation`, `log_artifact`.

  This shape is **OPTIONAL in v1.5** — the existing bulleted-list evidence shape remains valid. The typed table will become **MANDATORY in v2.0** (target: follow-up commit after pin-test corpus in `calibrator-eval-cases.md` confirms v1.5 stability).

  ## Alternatives considered
  ```

  ensuring the `old_string` matches uniquely (the Filling-rule paragraph followed by blank line and `## Alternatives considered` exists only once after Steps 1.5 and 1.6 land), the typed table renders as a proper Markdown table with the separator row `|---|------|--------|---------|`, the five Kinds (`source_citation`, `executed_reproducer`, `test_assertion`, `documentation`, `log_artifact`) are all present and inline-backticked, the bold markers `**OPTIONAL in v1.5**` and `**MANDATORY in v2.0**` are preserved, the apostrophe in "item's" is straight ASCII U+0027, the em-dash separating the OPTIONAL clauses is U+2014, the parenthetical pin-test note references `calibrator-eval-cases.md` inline-backticked, and no content is fabricated beyond what R2 §6 explicitly states. If unable to complete due to non-unique `old_string` match, character-encoding drift, or the prior insertions not landing as expected, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 2: Sync mirror + verify drift + lint gate

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Each item depends on the previous item's success — `verify-sync` will FAIL if `sync-dev` has not yet run, and the markdownlint hook will operate on the post-sync state of the source file.

**Step 2.1:** Run `make sync-dev` to mirror src/ → .claude/

- [x] Read the file `03-template-and-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/03-template-and-conventions.md` Section 2 "Sync-Dev + Verify-Sync Workflow" to confirm the verbatim Makefile target behavior (the `sync-dev` target is declared at `Makefile:109` and walks `src/superclaude/skills/*/` mirroring each skill into `.claude/skills/<name>/` while skipping `__init__.py` and `__pycache__`, which means the edited file at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` will be copied to `.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`), then use the Bash tool to run the command `make sync-dev` from the repository root (the current worktree or main checkout — whichever directory contains this task file's parent `.dev/`, `Makefile`, and `src/`; do NOT hardcode an absolute path because this task may run inside a worktree at `.claude/worktrees/<name>/` or in the main checkout), capturing both stdout and stderr and the exit code, ensuring the exit code is 0, the stdout contains the line `🔄 Syncing src/superclaude/ → .claude/ for local development...`, the stdout ends with a success indicator (per R3 §2 the command prints status lines per component group and concludes successfully when no error is raised), and the `.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` mirror is now updated to match the post-Phase-1 src/ state. If unable to complete because the command exits non-zero, because make is not on PATH, or because the working directory is not the repository root, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.2:** Run `make verify-sync` to confirm zero drift

- [x] Read the file `03-template-and-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/03-template-and-conventions.md` Section 2 (specifically the `verify-sync` subsection) to confirm the verbatim behavior — the target is declared at `Makefile:166` and uses bidirectional `diff -rq --exclude='__init__.py' --exclude='__pycache__'` to compare `src/superclaude/skills/*/` against `.claude/skills/*/`, flagging any `MISSING` or `DIFFERS` results and exiting 1 with `❌ Drift detected! Run 'make sync-dev' to fix...` if drift exists — and confirm R3 §7 Gotcha 2 which states `make sync-dev` MUST precede `make verify-sync` or this step will fail, then use the Bash tool to run the command `make verify-sync` from the repository root (same root as Step 2.1 — the worktree or main checkout containing `Makefile` and `src/`), capturing both stdout and stderr and the exit code, ensuring the exit code is 0 (no drift), the stdout does NOT contain the substring `Drift detected`, no `MISSING` or `DIFFERS` lines are reported for the `sc-troubleshoot-protocol` skill, and the final line of output indicates all components in sync. If the command exits non-zero with `Drift detected`, re-run Step 2.1 exactly ONCE (a single re-run is the documented recovery path; if drift persists after one retry, treat as a blocker), then re-run this command and re-check exit code; if still non-zero, log the specific drift output using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.3:** Run markdownlint hook on the edited source file

- [x] Read the file `03-template-and-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/03-template-and-conventions.md` Section 3 "Markdownlint Gate" and Section 7 Gotcha 3 to confirm the hook configuration (declared at `.pre-commit-config.yaml:70-82`, uses `igorshubovych/markdownlint-cli@v0.38.0`, runs with `args: ['--fix']` meaning it may auto-modify the file, excludes `\.dev/.*` so the task file itself is not linted but the target file under `src/` IS linted), then use the Bash tool to run the command `pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` from the repository root (same root as Step 2.1), capturing both stdout and stderr and the exit code, ensuring the final result is `Passed` (exit code 0 with no remaining violations), no MD-rule violations remain after any `--fix` modifications, and the post-lint file is still well-formed (no broken code fences, no malformed frontmatter). If `--fix` modifies the file (pre-commit reports `files were modified by this hook` which initially yields exit code 1), re-run `make sync-dev` and `make verify-sync` from Steps 2.1-2.2 a single time so the `.claude/` mirror reflects the lint fixes, then re-run the markdownlint command and confirm exit 0 on the second pass; if a second pass still exits non-zero with NEW violations (not "files were modified" but actual rule failures), log the specific violations using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 3: Final structural verification (QA gate — executor-performed, per FINAL_ONLY)

This is the task's final QA gate per the BUILD_REQUEST's `QA_GATE_REQUIREMENTS: FINAL_ONLY` directive. The executor performs the verification directly — no rf-qa spawning is required (per-task-file QA gates A.10/A.10.5 in the task-builder skill already gated the task file itself).

**Step 3.1:** Final structural verification of edited target file

- [x] Read the target file `hypothesis-card-template.md` at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` end-to-end and read the file `01-target-file-state.md` at `.dev/tasks/to-do/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/01-target-file-state.md` Section 4 "Code-fence boundary analysis" plus Section 5 "Worked-example assessment" to confirm the expected post-edit invariants, then verify the following structural checks in sequence: (a) the template code fence still opens correctly near the start of the schema region and closes correctly at the schema region's trailing edge, with all five insertions landing INSIDE the template fence and NONE landing inside the worked-example fence; (b) the five insertion blocks appear in the correct order — frontmatter additions between `**Cause class**` and `**Consistency with docs**`, Runtime check row between `Evidence grounding` and `Symptom coverage`, then `## Falsification standard` then `## Evidence classification [V2 merged]` then `## Recommended evidence shape (v2.0 preview)` all sandwiched between the "If I'm wrong" body and `## Alternatives considered`; (c) the worked example block remains byte-identical to the pre-edit state (frontmatter still shows only Agent/Tier/Timestamp/Cause class without the new fields, per the proposal's Migration note allowing v1 cards); (d) the total line count is in the expected range 138-153 lines (baseline 108 + Block 1 ~16 + Block 2 ~1 + Block 3 ~3 + Block 4 ~8 + Block 5 ~13 ≈ 30-45 added lines); (e) every em-dash is U+2014 (no double-hyphen ASCII), every `≤` is U+2264, every `∈` is U+2208; (f) the proposal off-by-one defect `<one of the seven above>` is present verbatim in the Evidence classification section (this is the documented carry-forward defect — its presence is the CORRECT outcome, NOT a regression); (g) the `[V2 merged]` provenance suffix is preserved on the Evidence classification heading, ensuring all five insertions are correctly placed, all character encodings are preserved, the worked example is untouched, the line count is in range, and no fabricated structural state is assumed. If any check fails, log the specific failure using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file (include which check failed and the observed vs expected state), then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

- [x] Verify all task outputs by using the Bash tool to confirm via `ls -l src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md .claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` that both the source file and the sync mirror exist on disk, then use the Bash tool to run `wc -l src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` and confirm the line count is in the expected range 138-153 lines, then use the Bash tool to run `diff src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md .claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` and confirm the diff is empty (zero-byte difference between src/ and .claude/ mirror), ensuring no expected deliverable is missing. If any file is missing or the mirror diverges from the source, log the gap in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item as complete.

- [x] This task did NOT modify source code (it modified a Markdown documentation file). Per `TESTING_REQUIREMENTS: NONE` in the BUILD_REQUEST, no test suite execution is required. Add a single line `**[2026-05-27 HH:MM]** - Testing skipped: documentation-only edit (TESTING_REQUIREMENTS: NONE per BUILD_REQUEST).` to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file. Once done, mark this item as complete.

- [x] Create the ### Task Summary section content at the top of the ## Task Log / Notes section at the bottom of this task file using the template format already provided there (Completion Date, Work Completed bullets, Challenges Encountered, Deviations from Process, Blockers Logged with status, Follow-Up Required). The summary MUST document: (a) the target file was edited with five additive insertion blocks (frontmatter additions, Runtime check row, Falsification standard section, Evidence classification section, Recommended evidence shape preview section); (b) the src/ → .claude/ sync was completed and verified drift-free; (c) the markdownlint hook passed on the edited file; (d) the worked example was intentionally left untouched per the proposal's Migration note; (e) the proposal off-by-one prose defect `<one of the seven above>` was carried forward verbatim as a known prose defect flagged for upstream follow-up; (f) Change B in isolation produces a template with fields no consumer reads — this is intentional per the sequenced A→B→C→F rollout and is NOT a blocker. Once the summary is complete, mark this item as complete.

- [x] Update the `completion_date` field in this task file's frontmatter to today's date `2026-05-27`, update the `updated_date` field to the same date, update the `status` field to "🟢 Done", then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[2026-05-27 HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary

**Completion Date:** 2026-05-27

**Work Completed:**

- Five additive insertion blocks applied to `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`: (1) three frontmatter fields (Claim class, Evidence class, Verdict direction) inserted between `**Cause class**` and `**Consistency with docs**`; (2) Runtime check per-dimension row inserted between `Evidence grounding` and `Symptom coverage`; (3) `## Falsification standard` section appended after the "If I'm wrong" body; (4) `## Evidence classification [V2 merged]` section appended next, including the 0.65 self-cap Filling rule for runtime_behavior + static-evidence cards; (5) `## Recommended evidence shape (v2.0 preview)` typed-table preview section appended last; all five blocks land between the "If I'm wrong" body and `## Alternatives considered`, all inside the L9-L114 template fence.
- `src/` → `.claude/` sync: `make sync-dev` exit 0 (Skills 23, Agents 38, Commands 41, Hooks 11, Templates 16); `make verify-sync` exit 0 with "✅ All components in sync" — zero drift.
- Markdownlint hook: `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` returned `Passed` (exit 0); no `--fix` modifications applied.
- Final structural verification (Step 3.1): all seven checks (a-g) passed. Template fence intact (L9-L114), worked example fence intact (L125-L152), insertion ordering correct, worked example byte-identical to pre-edit state, total line count 152 (in expected 138-153 range), em-dashes are U+2014, `≤` is U+2264, `∈` is U+2208, off-by-one defect `<one of the seven above>` carried forward verbatim, `[V2 merged]` provenance suffix preserved.
- Files modified: `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (108 → 152 lines, +44 lines); `.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (mirror, populated via `make sync-dev`).
- Files created: none.

**Challenges Encountered:**

- `pre-commit` was not on PATH in this worktree. Resolved by `uv pip install pre-commit` then running via `uv run pre-commit run markdownlint --files ...`. Tool-installation step, not a content blocker.

**Deviations from Process:**

- None. All five insertion blocks pasted character-for-character from `02-change-b-spec-extraction.md`; all three Bash verifications (sync-dev, verify-sync, markdownlint) ran from the worktree repository root as specified.

**Blockers Logged:**

- None.

**Follow-Up Required:** Yes — three follow-up items already documented in the ### Follow-Up Items Identified section (fix the proposal off-by-one defect upstream; refresh the worked example after Change C lands; land Change A to resolve the dangling "escalation-rubric § Verdict-direction modifier" reference). None of these block this task's completion — they are intentional consequences of the sequenced A→B→C→F rollout.

### Risks / Known Limitations / Open Questions

These items were identified during task planning by the rf-task-builder and MUST be carried forward as-is by the executor. They are NOT blockers for this task; they are known prose defects, intentional scope decisions, and forward-looking gaps tied to the sequenced A→B→C→F rollout.

1. **Carry-forward prose defect — proposal off-by-one ("seven above" vs 6 enum values).** Insertion Block 4 contains the literal text `<one of the seven above>` in the Evidence classification section's `**Claim class**` bullet. The Claim class enum at the top of the frontmatter actually declares only 6 values (`static_defect`, `runtime_behavior`, `environment_dependent`, `config_value`, `doc_contract`, `mixed`). Per the BUILD_REQUEST's character-for-character paste mandate and R2 §2's discrepancy resolution, the text MUST be pasted VERBATIM as `seven`. A future commit should correct this to `<one of the six above>` upstream in the proposal source first, then propagate to this template. Source: `02-change-b-spec-extraction.md` §2 and §5.

2. **Worked example intentionally left untouched (v1.0 card style).** The worked example at the target file's lower fence omits the new schema fields (`Claim class`, `Evidence class`, `Verdict direction`, `Runtime check`, `Falsification standard`, `Evidence classification`, `Recommended evidence shape`). The proposal's Migration note treats v1.0 cards as valid via calibrator defaults (claim_class → `runtime_behavior`, evidence_class → `none`, verdict_direction → `AFFIRM`), so the example is internally consistent. A follow-up task may refresh the example once Change C lands the calibrator updates. Source: `01-target-file-state.md` §5 and `02-change-b-spec-extraction.md` §8.

3. **Insertion Block 5 inclusion decision (OPTIONAL in v1.5 → MANDATORY in v2.0).** The proposal labels Insertion Block 5 (`## Recommended evidence shape (v2.0 preview)`) as "OPTIONAL in v1.5". The BUILD_REQUEST resolves this by INCLUDING Block 5 in this commit (rationale: shipping it in v1.5 lets card authors adopt the typed table early; removing it later in v2.0 when it becomes mandatory is a no-op). The task encodes Block 5 as a regular Step 1.7 item, not as a conditional. Source: BUILD_REQUEST "OPEN QUESTIONS" item 3.

4. **Dangling forward reference to escalation-rubric § Verdict-direction modifier.** Insertion Block 1's Verdict direction sub-bullet says `(see escalation-rubric § Verdict-direction modifier)`. The Verdict-direction modifier subsection is owned by Change A (rubric formula update), which is deferred to a follow-up task build. Until Change A lands, this is a dangling reference. This is intentional per the sequenced A→B→C→F rollout and the proposal explicitly accepts forward references between changes. Source: `02-change-b-spec-extraction.md` §10.

5. **Change B in isolation produces a template with fields no consumer reads.** Per the proposal's L421 statement (cited in R2 §9): "Change B alone exposes claim_class + evidence_class + Runtime check field but the rubric still averages it into the old mean; verdict-direction modifier still absent." Acceptance for THIS task is limited to "the template includes the new fields, dimension row, and sections in the specified order, additively" — NOT "calibrator scores cards using new fields" (that is Change C). Source: `02-change-b-spec-extraction.md` §9.

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[2026-05-27 03:57]** - Task started: Updated status to "🟠 Doing" and start_date.

**[2026-05-27 04:01]** - Testing skipped: documentation-only edit (TESTING_REQUIREMENTS: NONE per BUILD_REQUEST).

**[2026-05-27 04:01]** - Task completed: Updated status to "🟢 Done" and completion_date.

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

<!-- Use this section to log structural-check failures from Step 3.1, including which sub-check (a-g) failed and the observed vs expected state. -->

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

- **[Priority: Medium]** Fix the proposal off-by-one (`<one of the seven above>` → `<one of the six above>`) in `CROSS-ENV-PROPOSAL-MERGED.md`, then propagate to `hypothesis-card-template.md` in a follow-up commit. — Identified in Risks/Open Questions item 1.
- **[Priority: Low]** After Change C (calibrator) lands, refresh the worked example to use the v1.5 schema fields. — Identified in Risks/Open Questions item 2.
- **[Priority: Low]** Land Change A (rubric formula) so the dangling reference to "escalation-rubric § Verdict-direction modifier" resolves. — Identified in Risks/Open Questions item 4.

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->
