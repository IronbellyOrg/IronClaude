# TDD Artifact Containment — Path Reference Index

**Release:** `tdd-artifact-containment`
**Date:** 2026-05-14
**Phase:** Analysis (read-only)
**Scope:** `/sc:tdd` command + `tdd` skill package (source-of-truth: `src/superclaude/`)

This index catalogs every path/output reference in the `/sc:tdd` command and `tdd` skill package that writes artifacts **outside** the per-release directory `.dev/releases/<bucket>/<release-name>/`. It is the evidence base for the spec at `spec.md`.

**Files surveyed:**

- `src/superclaude/commands/tdd.md` (the `/sc:tdd` command — note: NOT under `commands/sc/`)
- `src/superclaude/skills/tdd/SKILL.md`
- `src/superclaude/skills/tdd/refs/agent-prompts.md`
- `src/superclaude/skills/tdd/refs/build-request-template.md`
- `src/superclaude/skills/tdd/refs/operational-guidance.md`
- `src/superclaude/skills/tdd/refs/synthesis-mapping.md`
- `src/superclaude/skills/tdd/refs/validation-checklists.md`

**Note on command path divergence:** The user prompt referenced `src/superclaude/commands/sc/tdd.md`, but the file actually lives at `src/superclaude/commands/tdd.md`. Sync mapping: `src/superclaude/commands/tdd.md` -> `.claude/commands/sc/tdd.md` (the `sc/` subfolder is applied during sync, not at source).

---

## Section A — References to `.dev/tasks/to-do/` path

Every reference that anchors persistent artifacts under `.dev/tasks/to-do/TASK-TDD-*/` instead of a release directory.

| # | File | Line | Snippet | Intent |
|---|------|------|---------|--------|
| A1 | `src/superclaude/skills/tdd/SKILL.md` | 29 | `The research artifacts persist in the task folder under .dev/tasks/to-do/ so findings survive context compression...` | Establishes `.dev/tasks/to-do/` as the canonical home for ALL persistent research artifacts. Top-level architectural claim. |
| A2 | `src/superclaude/skills/tdd/SKILL.md` | 83 | `All persistent artifacts go into the task folder at .dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/` | Defines the global artifact root for the whole skill. This is the single biggest containment violation: every artifact lands in a task folder, never a release folder. |
| A3 | `src/superclaude/skills/tdd/SKILL.md` | 88 | `TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/` | Hard-coded TASK_DIR variable definition. Every downstream artifact path is derived from this. Changing this single line is the highest-leverage intervention. |
| A4 | `src/superclaude/skills/tdd/SKILL.md` | 89-93 | `TASK_FILE`, `RESEARCH`, `SYNTHESIS`, `QA`, `REVIEWS` all defined as `${TASK_DIR}<subdir>` | Five subordinate variables inherit the violation in A3. Self-correcting once TASK_DIR is rebased onto the release dir. |
| A5 | `src/superclaude/skills/tdd/SKILL.md` | 98-106 | Artifact location table: `${TASK_DIR}${TASK_ID}.md`, `${TASK_DIR}research-notes.md`, `${TASK_DIR}research/00-prd-extraction.md`, `${TASK_DIR}research/[NN]-[topic-name].md`, `${TASK_DIR}research/web-[NN]-[topic].md`, `${TASK_DIR}synthesis/synth-[NN]-[topic].md`, `${TASK_DIR}gaps-and-questions.md`, `${TASK_DIR}qa/analyst-report-[gate].md`, `${TASK_DIR}qa/qa-report-[gate].md` | The canonical artifact table. 9 distinct artifact types, all anchored to TASK_DIR. Drives builder behavior. |
| A6 | `src/superclaude/skills/tdd/SKILL.md` | 112 | `Check for existing task folders matching TASK-TDD-* in .dev/tasks/to-do/ before creating new ones` | Resumption-discovery probe targets `.dev/tasks/to-do/` directly. Must be retargeted to per-release dirs. |
| A7 | `src/superclaude/skills/tdd/SKILL.md` | 153 | `Look in .dev/tasks/to-do/ for any TASK-TDD-*/ folder containing a task file related to this component` | Step A.1 resume logic — same as A6, second occurrence. |
| A8 | `src/superclaude/skills/tdd/SKILL.md` | 157 | `Check for existing task folder at .dev/tasks/to-do/TASK-TDD-*/` | A.1 resume sub-check — same as A6/A7. |
| A9 | `src/superclaude/skills/tdd/SKILL.md` | 230 | `Create the task folder: .dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/ with subfolders research/, synthesis/, qa/, reviews/` | Step A.3 imperative — orchestrator MUST create folder here. Direct write side effect. |
| A10 | `src/superclaude/skills/tdd/SKILL.md` | 383 | `Invoke /task ... args set to the task file path from Stage A (e.g., .dev/tasks/to-do/TASK-TDD-20260309-120000/TASK-TDD-20260309-120000.md)` | Example task-file path handoff to `/task`. Cosmetic but propagates the convention into downstream skill chain. |
| A11 | `src/superclaude/skills/tdd/refs/operational-guidance.md` | 77-86 | Duplicate artifact location table (mirrors A5) | Reference duplicate of A5. Must be edited in lockstep. |
| A12 | `src/superclaude/skills/tdd/refs/operational-guidance.md` | 98 | `read the PRD and extract requirements ... into ${TASK_DIR}research/00-prd-extraction.md` | PRD extraction destination inherits TASK_DIR. |
| A13 | `src/superclaude/skills/tdd/refs/operational-guidance.md` | 114 | `Write new research files for the changes: ${TASK_DIR}research/update-[date]-[topic].md` | Update-protocol write destination. |
| A14 | `src/superclaude/skills/tdd/refs/operational-guidance.md` | 123 | `Task files are located at .dev/tasks/to-do/TASK-TDD-*/TASK-TDD-*.md and research artifacts at ${TASK_DIR}research/` | Session-management text references the path explicitly. |
| A15 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 31 | `Phase 1 ... create task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders` | Builder template instruction — propagates the convention into every generated task file. |
| A16 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 32 | `agents explore codebase and write findings files to ${TASK_DIR}research/. ... ${TASK_DIR}research/00-prd-extraction.md` | Builder Phase 2 instruction. |
| A17 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 40 | `RESEARCH NOTES FILE: ${TASK_DIR}research-notes.md` | Builder input contract. |
| A18 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 84 | `Create the task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders` | Builder Phase 1 imperative. |
| A19 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 87 | `first item extracts PRD context to ${TASK_DIR}research/00-prd-extraction.md` | Builder Phase 2 imperative. |
| A20 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 96 | `The analyst writes to ${TASK_DIR}qa/analyst-completeness-report.md. The QA agent writes to ${TASK_DIR}qa/qa-research-gate-report.md.` | Builder Phase 3 QA-gate destinations. |
| A21 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 97 | `Each partition instance writes to a numbered report (e.g., ${TASK_DIR}qa/analyst-completeness-report-1.md)` | Builder Phase 3 partition reports. |
| A22 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 101 | `Compile final gaps into ${TASK_DIR}gaps-and-questions.md` | Builder Phase 3 gap log. |
| A23 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 115 | `analyst writes to ${TASK_DIR}qa/analyst-synthesis-review.md. The QA agent writes to ${TASK_DIR}qa/qa-synthesis-gate-report.md.` | Builder Phase 5 destinations. |
| A24 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 121 | `QA agent ... writes its report to ${TASK_DIR}qa/qa-report-validation.md` | Builder Phase 6 structural-QA destination. |
| A25 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 123 | `agent writes to ${TASK_DIR}qa/qa-qualitative-review.md` | Builder Phase 6 qualitative-QA destination. |
| A26 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 133 | `TASK FILE LOCATION: .dev/tasks/to-do/TASK-TDD-[YYYYMMDD]-[HHMMSS]/TASK-TDD-[YYYYMMDD]-[HHMMSS].md` | Builder output-spec literal path. |
| A27 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 143 | `Create the task file at .dev/tasks/to-do/TASK-TDD-[YYYYMMDD-HHMMSS]/TASK-TDD-[YYYYMMDD-HHMMSS].md using PART 2 structure` | Builder final-step imperative. |
| A28 | `src/superclaude/commands/tdd.md` | 92 | `/sc:tdd --resume .dev/tasks/to-do/TASK-TDD-20260401-143022/TASK-TDD-20260401-143022.md` | Resume-example path in command doc. |

**Section A total: 28 references.**

---

## Section B — References to `docs/` path

Every reference that anchors the final TDD or related artifacts under `docs/` rather than a release folder.

| # | File | Line | Snippet | Intent |
|---|------|------|---------|--------|
| B1 | `src/superclaude/skills/tdd/SKILL.md` | 46 | `If creating from scratch, follow the project convention: docs/[domain]/TDD_[COMPONENT-NAME].md` | Sets the **default output location for the final TDD**. The single biggest `docs/` containment violation — the deliverable itself escapes the release folder. |
| B2 | `src/superclaude/skills/tdd/SKILL.md` | 107 | `\| Final TDD \| docs/[domain]/TDD_[COMPONENT-NAME].md \|` | Artifact-location table reaffirmation of B1. |
| B3 | `src/superclaude/skills/tdd/SKILL.md` | 177 | Example: `The PRD is at docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md` | PRD-reference example — `docs/` as PRD source. Acceptable as INPUT, but signals that the skill assumes PRDs live in `docs/` rather than per-release dirs. |
| B4 | `src/superclaude/skills/tdd/SKILL.md` | 196 | `look for a *_TDD.md or *-TDD.md file at the expected output location or in docs/. Also scan for any existing documentation about this component (READMEs, architecture docs, PRDs in docs/)` | Discovery scans `docs/` for existing stubs and PRDs. Read-only but biases the skill toward `docs/` as the documentation home. |
| B5 | `src/superclaude/skills/tdd/refs/operational-guidance.md` | 87 | `\| Final TDD \| docs/[domain]/TDD_[COMPONENT-NAME].md \|` | Duplicate of B2 in the refs. |
| B6 | `src/superclaude/skills/tdd/refs/build-request-template.md` | 120 | `the TDD output path docs/[domain]/TDD_[COMPONENT-NAME].md` | Builder hands the assembler agent `docs/[domain]/...` as the final output path. Drives actual write behavior. |
| B7 | `src/superclaude/skills/tdd/refs/validation-checklists.md` | 76 | `Archive approved sources to docs/archive/[appropriate-subdir]/` | Archive destination — out-of-release. Validation-checklist-driven write. |
| B8 | `src/superclaude/commands/tdd.md` | 31 | `--output docs/design/` | Synopsis example. |
| B9 | `src/superclaude/commands/tdd.md` | 75 | `--from-prd docs/product/PRD_ROADMAP_CANVAS.md` | PRD input example from `docs/`. |
| B10 | `src/superclaude/commands/tdd.md` | 82 | `--output docs/design/TDD_GPU_POOL.md` | Heavyweight TDD example output to `docs/`. |
| B11 | `src/superclaude/commands/tdd.md` | 97-98 | `--prd docs/product/PRD_WIZARD.md ... --output docs/wizard/TDD_WIZARD_STATE.md` | Wizard example: both input and output in `docs/`. |
| B12 | `src/superclaude/commands/tdd.md` | 108-110 | Strong-prompt example: `--from-prd docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md ... --output docs/agents/TDD_AGENT_ORCHESTRATION.md` | Canonical "strong prompt" example shown in command doc — establishes `docs/` as the modeled output location. |
| B13 | `src/superclaude/commands/tdd.md` | 116 | `--from-prd docs/docs-product/tech/canvas/PRD_ROADMAP_CANVAS.md` | PRD example path. |

**Section B total: 13 references.**

> **Note on `docs/`:** No reference matches the exact string `/docs/` (rooted absolute). All hits are repo-relative `docs/...` paths. The Section B count above is the complete set.

---

## Section C — Out-of-release artifact creation sites

A general review of every place where `/sc:tdd` or the `tdd` skill **creates files** that end up outside a per-release directory. This is the operational consequence of Sections A and B.

| # | Source File | Artifact Pattern | Current Write Location | Per-Run Cardinality | Notes |
|---|-------------|------------------|------------------------|---------------------|-------|
| C1 | `SKILL.md` line 89 (TASK_FILE) | MDTM task file `TASK-TDD-YYYYMMDD-HHMMSS.md` | `.dev/tasks/to-do/TASK-TDD-*/TASK-TDD-*.md` | 1 | The orchestrator + builder agent create this. Survives across sessions. |
| C2 | `SKILL.md` line 99 + `build-request-template.md` line 40 | Scope-discovery research notes | `.dev/tasks/to-do/TASK-TDD-*/research-notes.md` | 1 | Created by the orchestrator before spawning the builder. |
| C3 | `SKILL.md` line 100 + `build-request-template.md` line 87 + `operational-guidance.md` line 98 | PRD extraction | `.dev/tasks/to-do/TASK-TDD-*/research/00-prd-extraction.md` | 0-1 | Only when `--from-prd` is supplied. Created by a Phase 2 subagent. |
| C4 | `SKILL.md` line 101 + `build-request-template.md` line 32 | Codebase research files | `.dev/tasks/to-do/TASK-TDD-*/research/[NN]-[topic].md` | 2-10+ | One per spawned research subagent (per-tier: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+). |
| C5 | `SKILL.md` line 102 + `agent-prompts.md` line 101 | Web research files | `.dev/tasks/to-do/TASK-TDD-*/research/web-[NN]-[topic].md` | 0-4 | Per-tier 0-1 / 1-2 / 2-4. |
| C6 | `operational-guidance.md` line 114 | Update research files | `.dev/tasks/to-do/TASK-TDD-*/research/update-[date]-[topic].md` | 0-N | Only on TDD-update runs. |
| C7 | `SKILL.md` line 103 + `agent-prompts.md` lines 175-177 | Synthesis files | `.dev/tasks/to-do/TASK-TDD-*/synthesis/synth-[NN]-[topic].md` | 4-8 | One per template-section group. Written incrementally. |
| C8 | `SKILL.md` line 104 + `build-request-template.md` line 101 | Interim gaps log | `.dev/tasks/to-do/TASK-TDD-*/gaps-and-questions.md` | 1 | Phase 3 output. |
| C9 | `SKILL.md` line 105 + `build-request-template.md` lines 96, 115 | Analyst reports (3 gates) | `.dev/tasks/to-do/TASK-TDD-*/qa/analyst-completeness-report.md`, `analyst-synthesis-review.md` | 2 (+N partitions) | Plus numbered partition variants when >6 research files. |
| C10 | `SKILL.md` line 106 + `build-request-template.md` lines 96, 115, 121 | QA reports (3 gates) | `.dev/tasks/to-do/TASK-TDD-*/qa/qa-research-gate-report.md`, `qa-synthesis-gate-report.md`, `qa-report-validation.md` | 3 (+N partitions) | Phase 3, 5, 6. |
| C11 | `operational-guidance.md` line 85 + `build-request-template.md` line 123 | Qualitative QA review | `.dev/tasks/to-do/TASK-TDD-*/qa/qa-qualitative-review.md` | 1 | Phase 6 final qualitative gate. |
| C12 | `SKILL.md` line 107 + `operational-guidance.md` line 87 + `build-request-template.md` line 120 + `agent-prompts.md` line 365 | **Final TDD document** (the deliverable) | `docs/[domain]/TDD_[COMPONENT-NAME].md` | 1 | **This is the single most impactful escape — the deliverable itself.** Out of release-folder by default. |
| C13 | `validation-checklists.md` line 76 | Archived sources | `docs/archive/[appropriate-subdir]/` | 0-N | Side-effect when assembler supersedes old TDDs. |
| C14 | `SKILL.md` line 230 + `build-request-template.md` lines 31, 84 | Task subfolders (`research/`, `synthesis/`, `qa/`, `reviews/`) | `.dev/tasks/to-do/TASK-TDD-*/` | 4 directories | Created during Phase 1 / Step A.3 — sets the topology for all C1-C11 writes. |

**Section C total: 14 distinct artifact creation sites; ~12-35 actual files per Standard-tier run, all currently outside the release folder.**

### Concurrency / collision analysis

The current `TASK-TDD-YYYYMMDD-HHMMSS` slug encodes a timestamp, so two parallel sessions on the same minute would collide. Two developers on different releases working on different components on the same day land in the same `.dev/tasks/to-do/` flat namespace — they will not collide on file content, but the namespace is unbounded and grows monotonically. By contrast, anchoring artifacts under `.dev/releases/<bucket>/<release-name>/tdd/<component-slug>/<TASK_ID>/` provides natural per-release isolation, supports concurrent work on the same component across different releases, and aligns with the project discipline that "all development artifacts belong in `.dev/releases/$pathToRelease/`."

### Inputs the skill READS from `docs/` (read-only, not a containment violation but a coupling signal)

- B3, B4, B9, B11, B12, B13 — PRD references and existing-doc scans. These are not artifact-creation sites but they reveal that the skill assumes PRDs live in `docs/`. If PRDs are also being moved into release folders by other releases (likely, given the discipline), the discovery logic in Step A.3 (SKILL.md line 196) needs to scan release folders as well.

---

## Summary

- **A (.dev/tasks/to-do/):** 28 references across 5 files. Driven by the `TASK_DIR` variable defined once in `SKILL.md:88` and propagated through `operational-guidance.md` and `build-request-template.md`.
- **B (docs/):** 13 references across 4 files. The single load-bearing one is `SKILL.md:46`/`107` defining the final-TDD default at `docs/[domain]/TDD_[COMPONENT-NAME].md` — operationalized through `build-request-template.md:120` which hands that path to the `rf-assembler` subagent.
- **C (write sites):** 14 distinct artifact patterns, 12-35 files per Standard run, all currently outside the release folder.

The remediation is concentrated: re-anchor `TASK_DIR` and the final-TDD default to a release-derived path. Sync downstream tables (Section A5 / A11) and the builder template (A15-A27 / B6). Update command examples (A28 / B8-B13) for consistency.
