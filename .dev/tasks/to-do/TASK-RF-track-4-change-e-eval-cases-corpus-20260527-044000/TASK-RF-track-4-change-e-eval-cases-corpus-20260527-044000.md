---
id: "TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000"
title: "Change E — Create calibrator-eval-cases.md pin-test corpus (Track 4)"
description: "Create a new refs file at src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md containing the calibrator pin-test corpus per CROSS-ENV-PROPOSAL-MERGED.md L298-370 verbatim: 9 fixtures (6 synthetic V1 base + 3 real-card V2 merged inline-only), 5 property tests (P1-P4 hard + P5 soft), suite integrity with 5 trigger files, and a deferred implementation hook section. After file creation, run make sync-dev, make verify-sync, and markdownlint, then perform a final structural verification of all 5 H2 sections, all 9 fixtures with correct asymmetric structure, all 5 property tests, suite integrity bullets, the deferred-hook section, and byte-level preservation of the U+27F9 ⟹ Unicode character in P1/P2/P3."
status: "🟢 Done"
type: "📝 Documentation"
priority: "🔼 High"
created_date: "2026-05-27"
updated_date: "2026-05-27"
assigned_to: "orchestrator"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: "calibration-source-runtime-gap"
depends_on:
- "Change A (escalation-rubric.md gated-min formula + M3a caps) — corpus file content does NOT depend on A landing first, but expected scores only validate post-A"
- "Change C (confidence-calibrator.md applies A) — same; corpus file content is independent, expected scores validate post-C"
related_docs:
- path: "/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md"
  description: "Source proposal; Change E specified at L290-372; file content verbatim at L298-370"
- path: "src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md"
  description: "Sibling refs/ file (Change B output, shipped PR #89); already pre-references the new corpus file at L105"
- path: "src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md"
  description: "Change A target; one of the 5 suite-integrity trigger files"
- path: ".dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md"
  description: "Full verbatim extraction of proposal L298-370 with structured per-fixture/per-property fields"
- path: ".dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/02-refs-conventions.md"
  description: "refs/ directory conventions (H1/intro/section/table/code-fence/Unicode); flags U+27F9 ⟹ as novel to refs/"
- path: ".dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/03-t4-cards-and-template.md"
  description: "T4 directory absence (conclusive) + inline-content fallback for Fixtures 7-9 + Template 01 fit"
tags:
- "change-e"
- "calibrator"
- "pin-test-corpus"
- "track-4"
- "sc-troubleshoot-protocol"
- "refs"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "~30 min (single new file, fully-specified content, 5 deterministic phases)"
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

# Change E — Create calibrator-eval-cases.md pin-test corpus (Track 4)

## Task Overview

This task creates a single new refs/ file at `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` containing the pin-test corpus that gates all future changes to the calibrator subsystem (Changes A, B, C, F). The file content is fully specified inline in the source proposal at L298-370 and must be reproduced verbatim. The new file ships ~70-90 lines containing five H2 sections: (1) Synthetic fixtures (V1 base) with 6 fixtures, (2) Real-card replay fixtures (V2 merged) with 3 fixtures, (3) Property tests with a 5-row table (P1-P4 hard + P5 soft), (4) Suite integrity with the 5 trigger files and merge-blocking rule, (5) Implementation hook (deferred to follow-up commit — pytest harness OUT OF SCOPE).

Note an asymmetric fixture structure: Fixtures 1, 2, 3, 4, 6, 7, 8, 9 use the `**Expected calibrated**:` field, while Fixture 5 alone uses `**Expected behavior**:` (because Fixture 5 tests a default-and-proceed behavior for v1.0 cards missing claim_class, not a calibrated-score range). The U+27F9 (`⟹`) Unicode character used in P1/P2/P3 assertions is novel to `refs/` and must be preserved byte-exactly. Fixtures 7-9 ship with proposal-described properties only (no real-card text or path references) because the T4 source directory `t4-pane-title-20260526-101500` does not exist anywhere in this filesystem (researcher 03 verified conclusively with find at depth 10). After file creation, the task runs `make sync-dev` to mirror the new file into `.claude/`, runs `make verify-sync` to confirm the mirror is clean, runs the project pre-commit `markdownlint` against the new file, and performs a final structural verification.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Create the new file at the canonical src/ path:** Produce `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` containing the verbatim content of CROSS-ENV-PROPOSAL-MERGED.md L298-370 — H1 + intro paragraph + 5 H2 sections + 9 fixtures (asymmetric structure — Fixture 5 uses Expected-behavior) + 5 property tests + suite integrity + deferred implementation hook.
2. **Preserve all 7 provenance markers verbatim:** H1 intro, `(V1 base)` in Section 3 H2, `(V2 merged)` in Section 4 H2, `[V2 merged]` suffix on Fixtures 7/8/9, and `(V2-merged Change F)` on suite-integrity bullet 5 — all must land byte-exactly.
3. **Preserve U+27F9 (`⟹`) byte-exactly in P1/P2/P3 assertions:** This Unicode character is novel to `refs/` per researcher 02; mojibake or HTML-entity substitution is a regression.
4. **Mirror the file into .claude/ via make sync-dev and verify the mirror:** `make sync-dev` must exit 0; `make verify-sync` must exit 0 (confirms src/ and .claude/ match).
5. **Pass the project's markdownlint pre-commit hook on the new file:** `uv run pre-commit run markdownlint --files <new-file>` returns Passed (or No-op for unchanged staged state).
6. **Final structural verification:** Confirm all 5 H2 sections present, all 9 fixtures present with correct asymmetric Expected-calibrated vs Expected-behavior structure, all 5 property test rows present, all 5 suite-integrity trigger files listed, deferred implementation hook section present, and U+27F9 byte-preserved.

## Prerequisites & Dependencies

### Parent Task & Dependencies

- **Parent Task:** calibration-source-runtime-gap (worktree-scoped multi-track refactor; this task is Track 4 of 4).
- **Blocking Dependencies (for content creation):** NONE. The corpus file content is deterministic from proposal L298-370 and does NOT require Changes A, B, C, or F to have landed before THIS file can be created.
- **Operational dependency (for executing the corpus):** Changes A (gated-min formula + M3a caps) and C (calibrator computes against A) MUST land before the corpus's expected-score assertions can validate against the actual calibrator. This task creates the corpus file; it does NOT execute it. The pytest harness at `tests/troubleshoot/test_calibrator_eval_cases.py` is explicitly deferred per proposal L367-370 — that harness is the venue where A+C dependency becomes hard.
- **This task blocks:** Future calibrator refactors (Change A/C/F follow-ups, any subsequent calibrator changes) — once the corpus exists, it gates merge on the 5 trigger files listed in Section 4.

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

**Required Previous Stage Outputs:**

- **Source proposal:** `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` (L290-372 contains the Change E section; the file content lives inline at L298-370 between a `\`\`\`markdown` opener at L298 and a closing `\`\`\`` at L370). Used by Phase 2 and Phase 3 as the verbatim source of truth.
- **Research 01:** `.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md` — full verbatim extraction + structured per-fixture/per-property fields + 16-item acceptance checklist + Section 9 HARD A+C dependency documentation. Used by Phase 2 and Phase 3 as the authoritative content reference.
- **Research 02:** `.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/02-refs-conventions.md` — refs/ directory conventions (H1/intro/section/table/code-fence/Unicode/bold conventions) + explicit U+27F9 novelty flag. Used by Phase 2 to confirm conventions and by Phase 5 to verify Unicode preservation.
- **Research 03:** `.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/03-t4-cards-and-template.md` — conclusive T4 directory absence finding + inline-content fallback recommendation for Fixtures 7-9 + Template 01 fit confirmation + Makefile + pre-commit conventions. Used by Phase 2 (Fixture 7-9 strategy) and Phase 4 (lint command).

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:

- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Execution Context

<!-- Task-level reading aid. Per-item Context fields below carry the file:line citations — this header is a roll-up only. -->

- **References:** R-001: Change E creates `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` per CROSS-ENV-PROPOSAL-MERGED.md L298-370 verbatim — 9 fixtures (6 synthetic V1 + 3 real-card V2 inline-only), 5 property tests, suite integrity, deferred implementation hook; R-002: gates all future changes to escalation-rubric.md (Change A), confidence-calibrator.md (Change C), hypothesis-card-template.md (Change B shipped), confidence-check skill, and sc-troubleshoot-protocol SKILL.md (Change F); without the corpus, subsequent calibrator refactors have no regression-test harness; R-003: research file 01 (full verbatim extraction); R-004: research file 02 (refs conventions + U+27F9 novelty); R-005: research file 03 (T4 directory absence + inline-content fallback).
- **Source areas:** sc-troubleshoot-protocol refs directory, cross-env-compare brainstorm proposal, project Makefile sync targets, project pre-commit markdownlint configuration.
- **Key constraints:** make sync-dev exits 0 AND make verify-sync exits 0; markdownlint pre-commit hook returns Passed on the new file; final structural check confirms 5 H2 sections + 9 fixtures with asymmetric Expected-calibrated vs Expected-behavior structure + 5 property tests + 5 suite-integrity trigger files + deferred implementation hook + U+27F9 ⟹ byte-preserved.

---

## Detailed Task Instructions

### Phase 1: Preparation and Setup

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status

- [x] Update status to "🟠 Doing" and start_date to 2026-05-27 in the frontmatter of this file (path `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000.md`), then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[2026-05-27 HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Baseline existence checks

- [x] Run `ls /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md 2>&1` to confirm the target file does NOT yet exist (expected: "No such file or directory" / exit code 2) — this is the baseline that proves Phase 2's Write call creates a new file rather than overwriting, then run `ls -la /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/` to confirm the parent `refs/` directory exists and contains the 6 existing ref files (`doc-discovery.md`, `escalation-rubric.md`, `hypothesis-card-template.md`, `remediation-handoff.md`, `report-template.md`, `triage-checklist.md`), ensuring the parent directory is in the expected state from researcher 02 so the Write call in Phase 2 will land in the correct location with the correct sibling context. If either check produces unexpected output (e.g., the target file ALREADY exists, or the refs/ directory is missing, or sibling file inventory diverges from the 6-file list), log the specific finding using the templated format in the ### Phase 1 - Preparation Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 2: Initial File Creation (Header + H1 + Intro)

This phase uses the Write tool to create the new file IMMEDIATELY with only the H1 title and the intro paragraph. All 5 H2 sections are appended in Phase 3 with one Edit per section. NEVER attempt to write the entire file content in a single Write call — incremental writing is mandatory.

**Step 2.1:** Write the initial file content (H1 + intro paragraph only)

- [x] Read the source proposal file `CROSS-ENV-PROPOSAL-MERGED.md` at `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` lines 298-301 to extract the H1 and intro paragraph verbatim (or use research file 01 Section 2 at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md` which already extracts L299-301 verbatim), then use the Write tool to create the new file at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` containing EXACTLY the H1 `# Calibrator Eval Cases`, a blank line, the intro paragraph reading "Golden hypothesis cards + expected calibrated scores. Run before any change to `escalation-rubric.md`, `confidence-calibrator.md`, `hypothesis-card-template.md`, or `sc-troubleshoot-protocol/SKILL.md` ships. A regression on any fixture or property test blocks merge." (each of the four trigger filenames wrapped in single backticks), and a single trailing newline, ensuring the H1 has no trailing punctuation, the four trigger files appear in the exact order escalation-rubric.md, confidence-calibrator.md, hypothesis-card-template.md, sc-troubleshoot-protocol/SKILL.md (matching proposal L301), the closing sentence reads "A regression on any fixture or property test blocks merge." verbatim, no H2 sections are written yet (those are appended in Phase 3), no content is fabricated beyond what proposal L299-301 explicitly states, no placeholder or TODO text remains, and the file is written with a single trailing newline (no trailing blank bullets, no spurious whitespace). If unable to complete due to file write failure, source-file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 - Initial File Creation Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 3: Append H2 Sections One at a Time (5 Sections, 5 Edit Appends)

This phase appends the five H2 sections to the file created in Phase 2, ONE H2 section per Edit call. NEVER batch multiple H2 sections into a single Edit operation — incremental writing per A3/A4 granularity is mandatory. Each fixture and property-test row is part of its parent H2 section (no per-fixture Edit). The reading sequence is: read research file 01 (which has the full extracted verbatim content) → identify the exact lines for the section → use Edit to append. The `old_string` for each Edit is the last line of the file as it currently stands (the end of the previously-appended section, OR the intro paragraph line for the first append); the `new_string` is that same anchor line PLUS the new section content. Verify each Edit succeeded by re-reading the affected portion of the new file before moving to the next section.

**Step 3.1:** Append H2 Section 1 — "## Synthetic fixtures (V1 base)" (Fixtures 1-6)

- [x] Read research file 01 at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md` Section 3 (lines 50-176) to extract the verbatim content of the `## Synthetic fixtures (V1 base)` H2 section including its 6 Fixture H3 subsections (Fixture 1 verbatim at research L64-69 / proposal L305-308; Fixture 2 verbatim at research L86-90 / proposal L310-313; Fixture 3 verbatim at research L106-110 / proposal L315-317; Fixture 4 verbatim at research L126-130 / proposal L319-321; Fixture 5 verbatim at research L146-150 / proposal L323-326 — NOTE Fixture 5 uses `**Expected behavior**:` not `**Expected calibrated**:`; Fixture 6 verbatim at research L162-166 / proposal L328-330), then use the Edit tool against `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to append (after the trailing newline of the existing intro paragraph) the verbatim H2 heading `## Synthetic fixtures (V1 base)` followed by a blank line followed by all 6 Fixture H3 subsections in order (each H3 separated from the next by a blank line per the proposal's formatting at L303-330), ensuring all 6 fixture H3 headings preserve their exact verbatim form including parenthetical descriptors, all bold field labels render as `**Expected calibrated**:` (Fixtures 1/2/3/4/6) or `**Expected behavior**:` (Fixture 5 ONLY) and `**Asserts**:` exactly as in the proposal, all backtick code-spans around frontmatter field names (`claim_class: runtime_behavior`, `evidence_class: source_static`, etc.) preserve single-backtick wrapping, the asymmetric structure between Fixture 5 (Expected-behavior) and Fixtures 1/2/3/4/6 (Expected-calibrated) is preserved, all 6 fixtures' descriptive paragraph + field-bullets land in correct order, no fixture is reordered or omitted, no content is fabricated beyond what proposal L303-330 states, and no placeholder text remains. If unable to complete due to file edit failure, source-file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 3 - Section Append Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.2:** Append H2 Section 2 — "## Real-card replay fixtures (V2 merged)" (Fixtures 7-9, inline-only)

- [x] Read research file 01 at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md` Section 4 (lines 180-249) to extract the verbatim content of the `## Real-card replay fixtures (V2 merged)` H2 section including its 3 Fixture H3 subsections (Fixture 7 verbatim at research L196-199 / proposal L334-336; Fixture 8 verbatim at research L216-219 / proposal L338-340; Fixture 9 verbatim at research L236-239 / proposal L342-344), then use the Edit tool against `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to append (after the trailing content of the previously-appended Synthetic fixtures section) the verbatim H2 heading `## Real-card replay fixtures (V2 merged)` followed by a blank line followed by all 3 Fixture H3 subsections in order (Fixtures 7, 8, 9 with `[V2 merged]` suffix in each H3 heading exactly as in proposal L334/L338/L342), ensuring each H3 heading preserves the exact `[V2 merged]` provenance suffix (square brackets verbatim), the proposal-described properties land verbatim per researcher 03's inline-only fallback decision (no real-card text and no path references to the missing T4 directory `t4-pane-title-20260526-101500` are added — only the proposal's own description of what each fixture replays), all three fixtures use `**Expected calibrated**:` and `**Asserts**:` field labels with exact wording per proposal L334-344 (including Fixture 7's dual-bound "≤ 0.65 (per V2 rule 1) or ≤ 0.70 (per V1 M3a)", Fixture 8's "≤ 0.70" + WebFetch unverifiability side-note, and Fixture 9's "0.70-0.85 range; NO hard cap fires"), the H2 heading carries the `(V2 merged)` provenance label verbatim, no real-card text or path references beyond what proposal L334-344 contains are added, no content is fabricated beyond what the proposal states, and no placeholder text remains. If unable to complete due to file edit failure, source-file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 3 - Section Append Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.3:** Append H2 Section 3 — "## Property tests" (5-row table with U+27F9 ⟹)

- [x] Read research file 01 at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md` Section 5 (lines 253-267) to extract the verbatim content of the `## Property tests` H2 section including the 5-row markdown table (header row `| ID | Property | Assertion |` + separator `|----|----------|-----------|` + P1/P2/P3/P4/P5 rows verbatim from proposal L348-354), AND read research file 02 at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/02-refs-conventions.md` for the U+27F9 (`⟹`) novelty flag confirming this character is new to `refs/` and must be byte-preserved (NOT substituted with `=>`, `==>`, `→`, or any HTML entity), then use the Edit tool against `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to append (after the trailing content of the previously-appended Real-card replay fixtures section) the verbatim H2 heading `## Property tests` followed by a blank line followed by the 5-row markdown table EXACTLY as in proposal L348-354 (header, separator, P1, P2, P3, P4, P5 rows in order), ensuring all 5 rows preserve their verbatim assertion text, the U+27F9 (`⟹`) character is byte-preserved in P1/P2/P3 assertion cells (NOT substituted), the `±` (U+00B1) characters in P4 and P5 assertion cells are byte-preserved, the `≤` (U+2264) characters throughout P1/P2/P3 are byte-preserved, P5's row ends with the literal `**Soft assertion** (warn-only in CI).` annotation (bold `**Soft assertion**` then space then parenthetical), the table alignment uses the verbatim pipe-and-dash form from the proposal, no row is reordered or omitted, no content is fabricated beyond what proposal L348-354 states, and no placeholder text remains. If unable to complete due to file edit failure, Unicode encoding issues (mojibake / HTML-entity substitution), or unclear requirements, log the specific blocker using the templated format in the ### Phase 3 - Section Append Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.4:** Append H2 Section 4 — "## Suite integrity" (5 trigger files + merge-blocking rule)

- [x] Read research file 01 at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md` Section 6 (lines 288-302) to extract the verbatim content of the `## Suite integrity` H2 section including the 5-bullet trigger-file list (`escalation-rubric.md`, `confidence-calibrator.md`, `hypothesis-card-template.md`, `confidence-check/SKILL.md`, `sc-troubleshoot-protocol/SKILL.md (V2-merged Change F)`) and the merge-blocking rule sentence "A regression on any fixture or hard property (P1-P4) blocks merge. P5 warnings surface for triage." (verbatim from proposal L356-365), then use the Edit tool against `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to append (after the trailing content of the previously-appended Property tests section) the verbatim H2 heading `## Suite integrity` followed by a blank line followed by the "Run on every PR that touches:" lead-in line followed by the 5-bullet trigger-file list (each bullet using `- ` markdown bullet form with the filename in single backticks) followed by a blank line followed by the merge-blocking rule sentence, ensuring all 5 trigger files appear in the exact order escalation-rubric.md, confidence-calibrator.md, hypothesis-card-template.md, confidence-check/SKILL.md, sc-troubleshoot-protocol/SKILL.md, the 5th bullet preserves its parenthetical `(V2-merged Change F)` annotation verbatim (the only bullet with a parenthetical), the merge-blocking sentence reads "A regression on any fixture or hard property (P1-P4) blocks merge. P5 warnings surface for triage." byte-exactly (note "P1-P4" with hyphen, not en-dash), no trigger file is reordered or omitted, no content is fabricated beyond what proposal L356-365 states, and no placeholder text remains. If unable to complete due to file edit failure, source-file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 3 - Section Append Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.5:** Append H2 Section 5 — "## Implementation hook (deferred to follow-up commit)"

- [x] Read research file 01 at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md` Section 7 (lines 321-329) to extract the verbatim content of the `## Implementation hook (deferred to follow-up commit)` H2 section including the deferral paragraph "Pytest harness invoking this corpus is OUT OF SCOPE for this brainstorm proposal. Expected landing path: `tests/troubleshoot/test_calibrator_eval_cases.py`." (verbatim from proposal L367-370), then use the Edit tool against `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to append (after the trailing content of the previously-appended Suite integrity section) the verbatim H2 heading `## Implementation hook (deferred to follow-up commit)` followed by a blank line followed by the deferral paragraph followed by a single trailing newline, ensuring the H2 heading preserves the parenthetical `(deferred to follow-up commit)` verbatim, the deferral paragraph capitalizes `OUT OF SCOPE` exactly (all-caps), the expected landing path `tests/troubleshoot/test_calibrator_eval_cases.py` is wrapped in single backticks, the paragraph reads as one sentence (NOT split into multiple paragraphs), this section does NOT actually create the pytest harness file (the harness is explicitly deferred per the proposal — Track 4 creates ONLY the markdown corpus, not the pytest file), no content is fabricated beyond what proposal L367-370 states, and no placeholder text remains. If unable to complete due to file edit failure, source-file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 3 - Section Append Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.6:** Read-back verification of the assembled file

- [x] Use the Read tool to read the full contents of `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to confirm the in-flight assembly is complete and well-formed before moving on to Phase 4 sync + lint, then run `wc -l /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` and confirm the line count is in the ~70-90 range stated in the BUILD_REQUEST (significantly fewer lines indicates a missing section; significantly more lines indicates fabricated content), ensuring (a) the file begins with `# Calibrator Eval Cases`, (b) the intro paragraph is present immediately under the H1, (c) all 5 H2 sections are present in order (`## Synthetic fixtures (V1 base)`, `## Real-card replay fixtures (V2 merged)`, `## Property tests`, `## Suite integrity`, `## Implementation hook (deferred to follow-up commit)`), (d) all 9 Fixture H3 headings are present (Fixtures 1-9 in numeric order with Fixtures 7/8/9 carrying the `[V2 merged]` suffix), (e) the Property tests table has 5 data rows (P1 through P5), (f) the Suite integrity bullet list has exactly 5 bullets, (g) the Implementation hook section is the final section, and (h) the file ends with a single trailing newline. If the read-back reveals a missing section, missing fixture, missing property-test row, structural issue, or any unexpected content, log the specific finding using the templated format in the ### Phase 3 - Section Append Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 4: Sync + Verify + Lint

This phase runs the project's sync target to mirror the new file from `src/superclaude/` into `.claude/`, runs the verify-sync check to confirm the mirror is clean, and runs the project's pre-commit markdownlint hook on the new file. Per CLAUDE.md and research 03, `src/superclaude/` is the source of truth — `make sync-dev` copies `src/superclaude/skills/{commands,skills,agents}` into `.claude/`.

**Step 4.1:** Run make sync-dev

- [x] Run `make sync-dev` from the worktree root `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/` (Bash tool, use the absolute working-directory approach: `cd /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap && make sync-dev`) to mirror the newly-created `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` into `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` per the project's sync convention documented in CLAUDE.md and in research file 03's Makefile-conventions section, ensuring the make command exits with status 0, the mirrored file `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` exists after the sync, and the mirrored file's content matches the src/ original byte-for-byte (use `diff /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to confirm — expected output is empty / exit 0). If `make sync-dev` exits non-zero, the mirrored file is missing, or the diff reveals byte-level divergence, log the specific failure (capture stderr, exit code, and any diff output) using the templated format in the ### Phase 4 - Sync and Lint Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.2:** Run make verify-sync

- [x] Run `make verify-sync` from the worktree root `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/` (Bash tool: `cd /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap && make verify-sync`) to confirm `src/superclaude/skills/` and `.claude/skills/` are in sync (per CLAUDE.md: "make verify-sync — Confirm src/ and .claude/ match (run before committing)"), ensuring the make target exits with status 0, no "src/ and .claude/ are out of sync" error is reported, and no orphan files (files in `.claude/` without a `src/` counterpart) or missing files (files in `src/` not yet mirrored) are flagged. If `make verify-sync` exits non-zero, the output reports out-of-sync directories, or the output reports orphan/missing files involving the new refs/ file, log the specific failure (capture stderr, exit code, and any sync-divergence summary lines) using the templated format in the ### Phase 4 - Sync and Lint Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.3:** Run pre-commit markdownlint on the new file

- [x] Run the project's pre-commit markdownlint hook against the new src/ file by executing (Bash tool: `cd /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap && uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`) per the project's pre-commit convention documented in research file 03's pre-commit-conventions section, ensuring the markdownlint hook reports `Passed` (or, on a fully-clean staged state, "no files to check" / hook skipped — per pre-commit's behavior when no staged changes match; in that case re-run with `--all-files` scoped to the new file is acceptable but the primary expectation is Passed against the explicit `--files` target), no MD-rule violations are reported, no AUTO-FIX edits are applied that change the file's content (markdownlint's auto-fix on this corpus is benign and acceptable if it triggers, but the post-fix content MUST still match the verbatim proposal content — if auto-fix triggers, re-run Phase 4 from Step 4.1 to re-sync; flag this in the findings log). If `uv run pre-commit run markdownlint` returns a non-Passed verdict, reports rule violations (e.g., MD013 line-length, MD024 duplicate headings, MD031 fenced-code-spacing), or auto-fixes content in a way that diverges from the proposal text, log the specific failures (capture the hook output verbatim, including rule IDs and line numbers) using the templated format in the ### Phase 4 - Sync and Lint Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 5: Final Structural Verification (FINAL_ONLY QA gate per BUILD_REQUEST)

This phase performs a single QA-gate-style structural verification that gates task completion. Per the BUILD_REQUEST QA_GATE_REQUIREMENTS = FINAL_ONLY, this verification spawns rf-qa (or, for a structurally-deterministic task like this one, performs the verification inline via grep / od / wc checks) to confirm all VALIDATION_REQUIREMENTS are met before the task marks Done. Because every check in VALIDATION_REQUIREMENTS is a deterministic byte-level / grep-level check against a single file, the verification is performed inline (not via subagent spawn) per researcher 03's recommendation; an rf-qa subagent could be spawned as an alternative for higher assurance, but the inline checks below have the same anti-hallucination property and are faster.

**Step 5.1:** Final structural verification — sections + fixtures + property tests + suite integrity + deferred hook + U+27F9 byte-preservation

- [x] Verify the final structural integrity of `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` by running the following sequence of grep + od + wc checks (Bash tool) and capturing each result: (a) `grep -c "^## " /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `5` (the 5 H2 sections: Synthetic fixtures, Real-card replay fixtures, Property tests, Suite integrity, Implementation hook) — note the BUILD_REQUEST mentioned 6 H2 sections, but the proposal at L298-370 contains 5 H2 sections (the H1 is not an H2); confirm with the actual proposal content via research file 01 Sections 3+4+5+6+7 (those five Sections correspond to the five H2 headings in the file; research file 01 Section 1 is the OUTSIDE-the-fence proposal metadata and Section 2 is the H1+intro pair — neither contributes an H2); if grep returns 6, an extra H2 was added (over-fabrication); if grep returns <5, a section was skipped; (b) `grep -c "^### Fixture" /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `9` (all 9 fixtures); (c) `grep -c "\[V2 merged\]" /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `3` (one per Fixture 7/8/9 H3 heading; note the BUILD_REQUEST allows higher counts only if the `(V2 merged)` H2-section provenance label is rendered with square brackets, which it should NOT be — the section label uses parentheses, the fixture suffixes use square brackets); (d) `grep -c "\*\*Expected calibrated\*\*:" /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `8` (Fixtures 1, 2, 3, 4, 6, 7, 8, 9 use Expected-calibrated); (e) `grep -c "\*\*Expected behavior\*\*:" /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `1` (Fixture 5 alone uses Expected-behavior — this is the asymmetric structure flagged in the BUILD_REQUEST); (f) `grep -c "^| P[1-5] " /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `5` (all 5 property test rows); (g) `grep -c "\*\*Soft assertion\*\*" /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `1` (P5 row); (h) verify U+27F9 (`⟹`) byte-level preservation by running `grep -c "⟹" /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` which MUST return exactly `3` (P1, P2, P3 assertions each contain one `⟹`) AND additionally confirm the byte-encoding via `python3 -c "import sys; data=open('/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md','rb').read(); print(data.count(b'\xe2\x9f\xb9'))"` which MUST print exactly `3` (UTF-8 bytes E2 9F B9 = U+27F9); a mismatch indicates mojibake or HTML-entity substitution; note the byte-level check uses python3 rather than `grep -P "\xE2\x9F\xB9"` because this host's `grep` is `ugrep` which does NOT honor the `\xNN` literal-byte escape inside `-P` patterns (it requires `\x{27F9}` codepoint form, which only counts matching lines not byte occurrences) — the python3 form is portable and counts byte occurrences directly; (i) `grep -c "(V2-merged Change F)" /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `1` (the suite-integrity bullet 5 annotation); (j) `grep -c "^## Implementation hook (deferred to follow-up commit)$" /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` MUST return exactly `1` (deferred hook section heading present), ensuring all 10 deterministic checks (a) through (j) return their expected counts, no check returns an unexpected value, and the file's structural integrity matches the proposal verbatim. If any check (a)-(j) returns an unexpected count, capture the actual count value and the specific check that failed, then log the specific failure using the templated format in the ### Phase 5 - Final Verification Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

- [x] Verify all task outputs by using Glob `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` and Glob `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to confirm BOTH the src/ source-of-truth file AND the .claude/ mirror file exist on disk (both are required deliverables — the src/ file is the deliverable, the .claude/ mirror is the consequence of `make sync-dev`), ensuring both Glob calls return the expected file path. If either file is missing, check the Task Log for blockers explaining the absence (Phase 2 Step 2.1 blocker = src/ file missing; Phase 4 Step 4.1 blocker = .claude/ mirror missing). If files are missing without documented reason, log the gap in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item as complete.

- [x] This task created no source code files (the only deliverable is a markdown corpus file; the pytest harness is explicitly deferred per proposal L367-370) — so no test suite execution is required. Note "No source code modified; no tests required per TESTING_REQUIREMENTS: NONE" in the ### Execution Log of the ## Task Log / Notes section at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file, using the templated format provided there. The summary should document: work completed (the new file `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` and its .claude/ mirror), challenges encountered during execution (e.g., the T4 directory absence finding that forced Fixtures 7-9 to ship with inline-only content, any markdownlint rule violations that required auto-fix), any deviations from the planned 5-phase process and their rationale, and blockers logged during execution with their resolution status. Once the summary is complete, mark this item as complete.

- [x] Update `completion_date` and `updated_date` to today's date (2026-05-27) and update task status to "🟢 Done" in the frontmatter of this task file, then add an entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[2026-05-27 HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary

**Completion Date:** 2026-05-27

**Work Completed:**

- New refs file: `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` (81 lines post-auto-fix; 5 H2 sections, 9 fixtures with asymmetric Expected-calibrated vs Expected-behavior structure, 5 property tests, suite integrity bullets, deferred implementation hook)
- Mirrored to: `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` via `make sync-dev` (byte-for-byte match confirmed by `diff`; `make verify-sync` clean)
- Files created:
  - `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`
  - `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` (sync-dev mirror)
- Files modified: None (task creates a new file only)

**Challenges Encountered:**

- markdownlint MD022 auto-fix on first lint pass added 10 blank lines between H3 fixture headings and their body paragraphs (proposal-style had headings adjacent to body text inside the original code-fence). Addressed by following Step 4.3's explicit instruction "if auto-fix triggers, re-run Phase 4 from Step 4.1 to re-sync" — re-ran `make sync-dev` immediately after; .claude/ mirror now matches the post-fix src/ byte-for-byte; all Phase 5 structural checks re-verified PASS on the 81-line post-fix file (line count remains within BUILD_REQUEST's ~70-90 expected range).
- T4 source directory `t4-pane-title-20260526-101500` does not exist anywhere in the filesystem (researcher 03 verified conclusively); Fixtures 7-9 shipped with proposal-described properties only (no real-card text or path references beyond what proposal L334-344 contains). This was the planned inline-only fallback strategy from research 03 — no deviation required.

**Deviations from Process:**

- None. The Phase 5 inline structural verification (rather than rf-qa subagent spawn) is the task file's explicitly-authored QA gate per BUILD_REQUEST QA_GATE_REQUIREMENTS = FINAL_ONLY; not a deviation. All 10 deterministic checks PASS.

**Blockers Logged:**

- None.

**Follow-Up Required:** Yes — the pytest harness at `tests/troubleshoot/test_calibrator_eval_cases.py` is explicitly deferred per proposal L367-370. That is a separate downstream follow-up task with a HARD prerequisite on Changes A (gated-min formula + M3a caps) and C (calibrator computes against A) landing first; without A+C, the corpus's expected-score assertions cannot validate against the legacy calibrator. Captured in the Follow-Up Items section.

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[2026-05-27 06:09]** - Task started: Updated status to "🟠 Doing" and start_date.

**[2026-05-27 06:13]** - No source code modified; no tests required per TESTING_REQUIREMENTS: NONE.

**[2026-05-27 06:14]** - Task completed: Updated status to "🟢 Done" and completion_date. The only deliverable is a markdown corpus file (`src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` + its .claude/ mirror); the pytest harness `tests/troubleshoot/test_calibrator_eval_cases.py` is explicitly deferred per proposal L367-370 and is captured in the Follow-Up Items list.

### Phase 1 - Preparation Findings

<!-- TEMPLATE FOR PHASE FINDINGS:
**[2026-05-27 HH:MM]** - [Step X.Y]: [Finding or blocker description]
- **Status:** [Completed | Blocked]
- **Details:** [Specific information about what was found, created, or what blocked completion]
- **Blocker Reason (if blocked):** [Specific reason why this could not be completed]
- **Files Affected:** [List of files read, created, or modified]
-->

### Phase 2 - Initial File Creation Findings

<!-- TEMPLATE FOR BLOCKER ENTRIES:
**[2026-05-27 HH:MM]** - Step 2.1 BLOCKED:
- **Blocker Reason:** [Specific reason]
- **Attempted:** [What was tried before determining blocker]
- **Required to Unblock:** [What information or action is needed to proceed]
-->

### Phase 3 - Section Append Findings

<!-- One entry per section-append step (3.1 through 3.6). Capture per-section results, any deviations, any auto-fix triggers, any Unicode-preservation concerns surfaced at read-back. -->

### Phase 4 - Sync and Lint Findings

<!-- Capture make sync-dev exit code, make verify-sync exit code, markdownlint hook output, any rule violations, any auto-fix triggers. -->

**[2026-05-27 06:13]** - Step 4.1 (sync-dev): exit 0; mirrored 23 skills / 38 agents / 41 commands / 11 hooks / 16 templates. Diff src vs .claude/ mirror = byte-for-byte match at first sync.

**[2026-05-27 06:13]** - Step 4.2 (verify-sync): exit 0; "All components in sync."

**[2026-05-27 06:13]** - Step 4.3 (markdownlint): Passed with auto-fix applied. Post-fix file gained 10 blank lines (MD022 — headings surrounded by blank lines). Per Step 4.3 instruction "if auto-fix triggers, re-run Phase 4 from Step 4.1 to re-sync", re-ran sync-dev + verify-sync immediately after; second sync brought .claude/ mirror in line with the post-fix src/ (diff=clean, verify-sync=All components in sync). The auto-fix is benign — content matches proposal verbatim semantically; only blank-line separation between H3 headings and body paragraphs was added (markdown-lint normalization). All 5 H2 sections, 9 fixtures, asymmetric Expected-calibrated vs Expected-behavior structure, 5 property tests, suite integrity bullets, and U+27F9 byte preservation remain intact (re-verified in Step 5.1 against post-fix file).

### Phase 5 - Final Verification Findings

<!-- Capture the 10 deterministic check results (a)-(j) from Step 5.1, with actual counts vs expected counts. -->

**[2026-05-27 06:13]** - Step 5.1 (10 deterministic structural checks against post-auto-fix file): ALL PASS.
- (a) H2 count: 5 (expected 5) ✅
- (b) Fixture H3 count: 9 (expected 9) ✅
- (c) [V2 merged] suffix count: 3 (expected 3) ✅
- (d) Expected calibrated count: 8 (expected 8 — Fixtures 1/2/3/4/6/7/8/9) ✅
- (e) Expected behavior count: 1 (expected 1 — Fixture 5 only, asymmetric structure preserved) ✅
- (f) P[1-5] property test rows: 5 (expected 5) ✅
- (g) Soft assertion count: 1 (expected 1 — P5 row) ✅
- (h) U+27F9 ⟹ grep count: 3; byte-level UTF-8 (E2 9F B9) count via python3: 3 (expected 3 — P1/P2/P3 byte-preserved, no mojibake or HTML-entity substitution) ✅
- (i) (V2-merged Change F) parenthetical: 1 (expected 1 — suite integrity bullet 5) ✅
- (j) Implementation hook H2 heading: 1 (expected 1, deferred-hook section present) ✅

Line count: 81 lines (within the BUILD_REQUEST's ~70-90 expected range; +10 over original 71 from the MD022 blank-line auto-fix).

### Phase Gate Findings

_QA gate verdicts (FINAL_ONLY per BUILD_REQUEST QA_GATE_REQUIREMENTS), fix cycle counts, and unresolved issues are recorded here. For this task the gate is the inline Step 5.1 structural check; no rf-qa subagent spawn unless Step 5.1 fails and a max-2 fix cycle is needed per the task-integrity gate type._

**[2026-05-27 06:13]** - FINAL_ONLY QA gate verdict: **PASS**. Inline Step 5.1 verification: all 10 deterministic checks PASS on the post-auto-fix file. No fix cycle required. markdownlint Passed (with one benign MD022 auto-fix). verify-sync clean (src/ and .claude/ in lock-step). No rf-qa subagent spawn invoked per the task file's explicit FINAL_ONLY + inline-verification authorization.

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

- **[Priority: Medium]** Follow-up commit: create the pytest harness `tests/troubleshoot/test_calibrator_eval_cases.py` that actually executes the corpus (loads each fixture, computes calibrated score, asserts thresholds, runs P1-P5 property tests). Explicitly deferred per proposal L367-370 and the Implementation hook section of the new corpus file. HARD prerequisite: Changes A (gated-min formula + M3a caps) and C (calibrator computes against A) MUST land first — without A+C, every Fixture 1/2/4/7/8 expected-score assertion will fail against the legacy calibrator.

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[2026-05-27 HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->
