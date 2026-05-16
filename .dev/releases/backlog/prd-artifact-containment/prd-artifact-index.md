# PRD Skill — Artifact Path Index

**Date:** 2026-05-14
**Scope:** `src/superclaude/skills/prd/` (SKILL.md + refs/) — NO `src/superclaude/commands/sc/prd.md` exists. The skill is invoked directly (not via a slash-command wrapper).
**Goal:** Catalogue every place the prd skill currently emits artifacts so the containment redesign can rewire them into `.dev/releases/<bucket>/<release-name>/`.

---

## Section A — References to `.dev/tasks/to-do/` path

The skill anchors ALL working artifacts (task file, research, synthesis, QA reports) inside the rigorflow MDTM task folder. This collides with release-folder containment because the artifacts that justify a PRD live in a separate tree from the spec/roadmap/tasklist for that release.

| # | File | Line | Snippet | Intent |
|---|------|------|---------|--------|
| A1 | `src/superclaude/skills/prd/SKILL.md` | 29 | `The research artifacts persist in the task folder under \`.dev/tasks/to-do/\`...` | Narrative: claims `.dev/tasks/to-do/` is the persistence root. |
| A2 | `src/superclaude/skills/prd/SKILL.md` | 97 | `All persistent artifacts go into the task folder at \`.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/\`.` | Authoritative declaration that the task folder is the artifact root. |
| A3 | `src/superclaude/skills/prd/SKILL.md` | 102 | `TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/` | Variable block defining `TASK_DIR` — referenced everywhere downstream. |
| A4 | `src/superclaude/skills/prd/SKILL.md` | 112 | `\| **MDTM Task File** \| \`.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/TASK-PRD-YYYYMMDD-HHMMSS.md\` \|` | Output table row anchoring the task file. |
| A5 | `src/superclaude/skills/prd/SKILL.md` | 131 | `Check for existing task folders matching \`TASK-PRD-*\` in \`.dev/tasks/to-do/\` before creating new ones...` | Resume-on-restart logic looks in `.dev/tasks/to-do/`. |
| A6 | `src/superclaude/skills/prd/SKILL.md` | 172 | `1. Look in \`.dev/tasks/to-do/\` for any \`TASK-PRD-*/\` folder containing a task file related to this product` | A.1 existing-task-file check. |
| A7 | `src/superclaude/skills/prd/SKILL.md` | 176 | `5. Check for existing task folder at \`.dev/tasks/to-do/TASK-PRD-*/\`:` | A.1 existing-task-folder probe. |
| A8 | `src/superclaude/skills/prd/SKILL.md` | 257 | `Create the task folder: \`.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/\` with subfolders \`research/\`, \`synthesis/\`, \`qa/\`, \`reviews/\`` | A.3 instructs creating the task folder under `.dev/tasks/to-do/`. |
| A9 | `src/superclaude/skills/prd/SKILL.md` | 410 | `args set to the task file path created in Stage A (e.g., \`.dev/tasks/to-do/TASK-PRD-20260309-120000/...\`).` | Stage-B handoff example. |
| A10 | `src/superclaude/skills/prd/refs/build-request-template.md` | 154 | `TASK FILE LOCATION: .dev/tasks/to-do/TASK-PRD-[YYYYMMDD]-[HHMMSS]/TASK-PRD-[YYYYMMDD]-[HHMMSS].md` | BUILD_REQUEST hands the builder a hardcoded location. |
| A11 | `src/superclaude/skills/prd/refs/build-request-template.md` | 164 | `6. Create the task file at .dev/tasks/to-do/TASK-PRD-[YYYYMMDD-HHMMSS]/TASK-PRD-[YYYYMMDD-HHMMSS].md using PART 2 structure` | Builder STEP 6 — concrete write instruction. |
| A12 | `src/superclaude/skills/prd/refs/operational-guidance.md` | 110 | `Task files are located at \`.dev/tasks/to-do/TASK-PRD-*/TASK-PRD-*.md\` and research artifacts at \`${TASK_DIR}research/\`.` | Session-resume documentation. |

**Implication:** Twelve hits. The artifact persistence root is treated as a constant. Containment redesign MUST replace the constant with a resolved release directory.

---

## Section B — References to `docs/` path

The skill writes its **final PRD** into `docs/docs-product/tech/...` and references `docs/` as a place for prior documentation, archived sources, and stub discovery. This conflicts with release containment because the deliverable PRD ends up in a global docs tree rather than the release that produced it.

| # | File | Line | Snippet | Intent |
|---|------|------|---------|--------|
| B1 | `src/superclaude/skills/prd/SKILL.md` | 43 | `If creating from scratch, follow the project convention: \`docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md\`.` | Default OUTPUT location convention (final PRD). |
| B2 | `src/superclaude/skills/prd/SKILL.md` | 48 | Example prompt: `Output to \`docs/docs-product/tech/agents/PRD_MULTI_AGENT_SYSTEM.md\`.` | Sample of the "good" output path. |
| B3 | `src/superclaude/skills/prd/SKILL.md` | 54 | `Create a PRD for the canvas roadmap feature by consolidating the existing docs at \`docs/docs-product/tech/canvas/\`.` | Example of consolidating from `docs/`. |
| B4 | `src/superclaude/skills/prd/SKILL.md` | 126 | `\| Final PRD \| \`docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md\` \|` | Outputs table — final PRD destination row. |
| B5 | `src/superclaude/skills/prd/SKILL.md` | 205 | Example: `Output to \`docs/docs-product/tech/frontend/PRD_WIZARD_SYSTEM.md\`.` | Scenario A example reinforcing `docs/` destination. |
| B6 | `src/superclaude/skills/prd/SKILL.md` | 224 | `look for a \`PRD_*.md\` or \`*-PRD.md\` file at the expected output location or in \`docs/\`.` | A.3 stub discovery scans `docs/`. |
| B7 | `src/superclaude/skills/prd/refs/build-request-template.md` | 9 | `GOAL: Create a comprehensive Product Requirements Document (PRD) for [GOAL] ... The PRD will be written to [OUTPUT_PATH].` | Templated `OUTPUT_PATH` defaults to a `docs/` location per B1. |
| B8 | `src/superclaude/skills/prd/refs/operational-guidance.md` | 13 | `Internal documentation (design docs, architecture docs, READMEs in \`docs/\`) describes intent, history, or planned state...` | Narrative — uses `docs/` as an example of documentation-of-record (read-only mention, not a write site). |
| B9 | `src/superclaude/skills/prd/refs/operational-guidance.md` | 88 | `\| Final PRD \| \`docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md\` \|` | Duplicate of B4 inside operational guidance. |
| B10 | `src/superclaude/skills/prd/refs/validation-checklists.md` | 88 | `Archive approved sources to \`docs/archive/[appropriate-subdir]/\`` | Step 11 (consolidation cleanup) sends archived sources into `docs/archive/`. |

**Implication:** The skill has TWO classes of `docs/` use: (a) **writes** — B1, B4, B7, B9, B10 (final PRD + archive) — must be rerouted; (b) **reads/mentions** — B2, B3, B5, B6, B8 — are example/discovery references and can stay, but the default example paths should be updated to dogfood the new convention.

---

## Section C — Out-of-release artifact creation sites

This section lists every spot in the skill (SKILL.md + refs/) that causes a file to be **created** outside `.dev/releases/<bucket>/<release-name>/`. Hits in Section A and B are summarised here at the artifact level rather than the line level.

| # | Artifact pattern | Created by | Current write site (outside the release folder) | Source declaration |
|---|------------------|-----------|--------------------------------------------------|--------------------|
| C1 | MDTM Task File `TASK-PRD-YYYYMMDD-HHMMSS.md` | `rf-task-builder` subagent in Stage A.7 | `.dev/tasks/to-do/TASK-PRD-*/TASK-PRD-*.md` | SKILL.md L112, build-request-template.md L154/L164 |
| C2 | Task folder skeleton (`research/`, `synthesis/`, `qa/`, `reviews/` subdirs) | Orchestrator during Stage A.3 | `.dev/tasks/to-do/TASK-PRD-*/` | SKILL.md L257 |
| C3 | Research notes file (`research-notes.md`) | Orchestrator in Stage A.4 | `.dev/tasks/to-do/TASK-PRD-*/research-notes.md` | SKILL.md L114, build-request-template.md L62-64 |
| C4 | Per-agent codebase research files (`[NN]-[topic].md`) | Phase 2 codebase research subagents | `.dev/tasks/to-do/TASK-PRD-*/research/` | SKILL.md L115, refs/agent-prompts.md L16 (`[output-path]` placeholder is filled from `${TASK_DIR}research/`) |
| C5 | Per-agent web research files (`web-[NN]-[topic].md`) | Phase 4 web research subagents | `.dev/tasks/to-do/TASK-PRD-*/research/` | SKILL.md L116, refs/agent-prompts.md L97 |
| C6 | Synthesis files (`synth-[NN]-[topic].md`) | Phase 5 synthesis subagents | `.dev/tasks/to-do/TASK-PRD-*/synthesis/` | SKILL.md L117, refs/agent-prompts.md L149 |
| C7 | Gaps log (`gaps-and-questions.md`) | Phase 3 / orchestrator | `.dev/tasks/to-do/TASK-PRD-*/gaps-and-questions.md` | SKILL.md L118, refs/operational-guidance.md L81 |
| C8 | Analyst completeness report | `rf-analyst` (Phase 3) | `.dev/tasks/to-do/TASK-PRD-*/qa/analyst-completeness-report.md` | SKILL.md L120, operational-guidance.md L82 |
| C9 | Analyst synthesis review | `rf-analyst` (Phase 5) | `.dev/tasks/to-do/TASK-PRD-*/qa/analyst-synthesis-review.md` | SKILL.md L121, operational-guidance.md L83 |
| C10 | QA research-gate report | `rf-qa` (Phase 3) | `.dev/tasks/to-do/TASK-PRD-*/qa/qa-research-gate-report.md` | SKILL.md L122, operational-guidance.md L84 |
| C11 | QA synthesis-gate report | `rf-qa` (Phase 5) | `.dev/tasks/to-do/TASK-PRD-*/qa/qa-synthesis-gate-report.md` | SKILL.md L123, operational-guidance.md L85 |
| C12 | QA report-validation | `rf-qa` (Phase 6) | `.dev/tasks/to-do/TASK-PRD-*/qa/qa-report-validation.md` | SKILL.md L124, operational-guidance.md L86 |
| C13 | QA qualitative review | `rf-qa-qualitative` (Phase 6) | `.dev/tasks/to-do/TASK-PRD-*/qa/qa-qualitative-review.md` | SKILL.md L125, operational-guidance.md L87 |
| C14 | Partitioned analyst/QA reports (`-1.md`, `-2.md`) | Multiple analyst/QA instances when workload partitioning kicks in | `.dev/tasks/to-do/TASK-PRD-*/qa/` | build-request-template.md L118 |
| C15 | Update-research files (`update-[date]-[topic].md`) | Update-existing-PRD path | `.dev/tasks/to-do/TASK-PRD-*/research/` | operational-guidance.md L101 |
| C16 | **Final PRD document** | `rf-assembler` (Phase 6) | `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` | SKILL.md L43/L126, operational-guidance.md L88 |
| C17 | Archived consolidation source docs | Phase 7 / orchestrator (only if consolidating) | `docs/archive/[appropriate-subdir]/` | validation-checklists.md L88 |

**Out-of-release summary:**
- **15 artifact classes** land under `.dev/tasks/to-do/TASK-PRD-*/` (C1–C15). None of them carry a binding to the release that produced them.
- **1 artifact class** (the final PRD, C16) lands in the global `docs/` tree.
- **1 artifact class** (archived sources, C17) lands in `docs/archive/`.
- The template path `src/superclaude/examples/prd_template.md` (SKILL.md L127) is a READ-only schema reference, not a write site — out of scope for containment.

**Collision risk for concurrent developers:**
The current path scheme partitions by **timestamp** (`TASK-PRD-YYYYMMDD-HHMMSS`), not by release. Two developers working on different releases at the same minute would collide; more importantly, neither task folder ties back to the release that owns it, so artifact-to-release attribution is lost after the session ends.

---

## Cross-cutting observations

- **No `.dev/releases/` references exist anywhere in the prd skill.** The skill is entirely unaware of the release folder convention. Zero hits across SKILL.md and all four refs files.
- **No `/sc:prd` command file exists.** `src/superclaude/commands/sc/` contains no `prd.md`. The skill is invoked directly by Claude Code's skill auto-detection (via the description field in SKILL.md frontmatter). Any redesign must live entirely inside the skill package; there is no thin command wrapper to amend.
- **Template path `src/superclaude/examples/prd_template.md` is read-only** — it's the PRD schema, not an artifact destination. Out of scope.
- **`docs/` mentions inside `operational-guidance.md` L13 and the example prompts (B2, B3, B5, B6)** are documentation references, not write sites. They should be updated to reflect the new convention but are not direct containment violations.
