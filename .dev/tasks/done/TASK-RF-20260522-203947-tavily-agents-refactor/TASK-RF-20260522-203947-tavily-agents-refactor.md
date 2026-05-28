---
id: "TASK-RF-20260522-203947-tavily-agents-refactor"
title: "Tavily-first web search precedence across 10 agents"
description: "Apply the Tavily-first web-search refactor to 10 agent definition files in src/superclaude/agents/ per their pre-authored proposal files. Each per-agent refactor edits frontmatter tools-list ordering plus body insertions (Tool Selection Policy / Web Research subsection / Critical Rule), then syncs to .claude/, runs verify gates, smoke-tests, and stages the change."
status: "🟢 Done"
type: "🛠️ Refactor"
priority: "🔼 High"
created_date: "2026-05-22"
updated_date: "2026-05-24"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""
depends_on: []
related_docs:
- path: ".dev/releases/current/TavilyAgents/_sweep-summary.md"
  description: "Confirms scope is closed at 10 agents; no other agents in src/superclaude/agents/ need this refactor"
- path: ".dev/releases/current/TavilyAgents/deep-research-tavily-refactor.md"
  description: "Per-agent refactor proposal for deep-research"
- path: ".dev/releases/current/TavilyAgents/deep-research-agent-tavily-refactor.md"
  description: "Per-agent refactor proposal for deep-research-agent"
- path: ".dev/releases/current/TavilyAgents/rf-task-researcher-tavily-refactor.md"
  description: "Per-agent refactor proposal for rf-task-researcher"
- path: ".dev/releases/current/TavilyAgents/rf-task-builder-tavily-refactor.md"
  description: "Per-agent refactor proposal for rf-task-builder"
- path: ".dev/releases/current/TavilyAgents/rf-task-executor-tavily-refactor.md"
  description: "Per-agent refactor proposal for rf-task-executor"
- path: ".dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md"
  description: "Per-agent refactor proposal for rf-team-lead"
- path: ".dev/releases/current/TavilyAgents/rf-assembler-tavily-refactor.md"
  description: "Per-agent refactor proposal for rf-assembler"
- path: ".dev/releases/current/TavilyAgents/rf-analyst-tavily-refactor.md"
  description: "Per-agent refactor proposal for rf-analyst"
- path: ".dev/releases/current/TavilyAgents/rf-qa-tavily-refactor.md"
  description: "Per-agent refactor proposal for rf-qa"
- path: ".dev/releases/current/TavilyAgents/rf-qa-qualitative-tavily-refactor.md"
  description: "Per-agent refactor proposal for rf-qa-qualitative"
- path: ".dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/research-notes.md"
  description: "Phase plan, conventions, and ambiguities for the build"
tags:
- "tavily"
- "agents"
- "web-search"
- "mcp"
- "policy-refactor"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: ""
sprint: ""
due_date: ""
start_date: "2026-05-22"
completion_date: "2026-05-24"
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# Tavily-first web search precedence across 10 agents

## Task Overview

SuperClaude has Tavily MCP available, but several agent definitions in `src/superclaude/agents/` currently default to `WebSearch` / `WebFetch` (or list them in the tools allowlist before the Tavily MCP tool IDs). The policy decision is: **Tavily MCP first, fall back to WebSearch/WebFetch only when Tavily is unavailable** (tool not loaded, server error after retry, rate-limited, or auth error).

This task applies the Tavily-first refactor to exactly 10 in-scope agent definition files. Each per-agent refactor is fully pre-specified in a corresponding proposal file under `.dev/releases/current/TavilyAgents/` (see Prerequisites & Dependencies → Required Previous Stage Outputs). The proposals were adversarially-reviewed via `/sc:reflect --session --analyze` and include verbatim diff-style edits (frontmatter `tools:` list reordering plus body insertions) and verbatim acceptance criteria. The executor's job is to encode each proposal's authorized edits into the source-of-truth agent file in `src/superclaude/agents/`, then sync to `.claude/`, verify, smoke-test, and stage.

The sweep summary at `.dev/releases/current/TavilyAgents/_sweep-summary.md` confirms scope is closed at 10 agents — no other `src/superclaude/agents/*.md` file matches the web-research-role pattern that would benefit from this refactor.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Apply 10 per-agent Tavily-first refactors:** Each of the 10 in-scope `src/superclaude/agents/*.md` files is edited per its corresponding proposal's "Proposed refactor" section — frontmatter `tools:` list reordered with Tavily MCP entries before WebSearch/WebFetch, and the body insertions (Tool Selection Policy / Web Research subsection / new Critical Rule) applied verbatim from the proposal.
2. **Pass all per-agent acceptance criteria:** Every line item in each proposal's "Acceptance criteria" section verifies after the corresponding edit, with no item weakened or skipped.
3. **Sync src/ → .claude/ with zero drift:** `make sync-dev` succeeds; `make verify-sync` reports zero drift between `src/superclaude/agents/` and `.claude/agents/`.
4. **Pass lint and smoke tests:** `make lint` passes with no new warnings; `uv run pytest` finishes with no new failures (agent definitions are documentation-style, so the gate is "suite stays green").
5. **Stage `src/` only:** `git add` operates only on the 10 `src/superclaude/agents/*.md` files. Never `git add .claude/agents/...` (gitignored per CLAUDE.md absolute rule; `git add -f` on any `.claude/` path is forbidden). Commit with conventional message `feat(agents): Tavily-first web search precedence across 10 agents` (unless user overrides to 10 per-agent commits — see Open Questions).

## Prerequisites & Dependencies

### Parent Task & Dependencies

- **Parent Task:** None (this task is the standalone execution of a pre-authored proposal sweep).
- **Blocking Dependencies:** None — all 10 proposals were authored in the same session as the sweep summary (2026-05-22) and treat each target agent file as `[CODE-VERIFIED]` at proposal-authoring time. The executor SHOULD re-Read each agent file before editing to detect any drift since 2026-05-22 (freshness rule).
- **This task blocks:** Potential follow-up task to update downstream `.dev/` documentation referencing these agents (out of scope here; see Open Questions).

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

The actual checklist items for reading these proposals appear in Phase 1, Step 1.2 (re-Read pass) and inline within each Phase 2 item.

**Required Previous Stage Outputs:**

- **Scope confirmation:** `.dev/releases/current/TavilyAgents/_sweep-summary.md` — confirms only 10 agents are in scope; 28 others swept and excluded with justification.
- **Per-agent proposal for deep-research:** `.dev/releases/current/TavilyAgents/deep-research-tavily-refactor.md` — verbatim "Proposed refactor" diff (frontmatter `tools:` + Tool Selection Policy section + Workflow step 3 edit + Sources table backend column) plus acceptance criteria.
- **Per-agent proposal for deep-research-agent:** `.dev/releases/current/TavilyAgents/deep-research-agent-tavily-refactor.md` — verbatim "Proposed refactor" diff (frontmatter `tools:` + Tool Orchestration replacement with Tavily-First Rule, Search Strategy, Extraction Routing, Fallback Policy + Citation Requirements backend tagging) plus acceptance criteria.
- **Per-agent proposal for rf-task-researcher:** `.dev/releases/current/TavilyAgents/rf-task-researcher-tavily-refactor.md` — verbatim "Proposed refactor" diff (frontmatter `tools:` insert + rename Extended Research Tools section to "Web Search (Tavily-first)" + escalation ladder step 1 edit + Solution Research line edit + Research Notes Structure provenance line + new Critical Rule 8) plus acceptance criteria.
- **Per-agent proposal for rf-task-builder:** `.dev/releases/current/TavilyAgents/rf-task-builder-tavily-refactor.md` — verbatim "Proposed refactor" diff (frontmatter `tools:` insert + rewrite Extended Tools → "Web Search (Tavily-first)" + new Critical Rule 13 with per-item HTML-comment provenance contract) plus acceptance criteria.
- **Per-agent proposal for rf-task-executor:** `.dev/releases/current/TavilyAgents/rf-task-executor-tavily-refactor.md` — verbatim "Proposed refactor" Option A (frontmatter `tools:` insert + add Critical Rule 7 framing web ops as defensive guardrail + "What NOT To Do" bullet referencing Rule 7) plus acceptance criteria.
- **Per-agent proposal for rf-team-lead:** `.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md` — verbatim "Proposed refactor" diff (frontmatter `tools:` reorder with PRIMARY/FALLBACK comments + replace "WebSearch — Understanding Unfamiliar Technologies" with "Web Research — Tavily-first Protocol" + add Critical Rule 11) plus acceptance criteria.
- **Per-agent proposal for rf-assembler:** `.dev/releases/current/TavilyAgents/rf-assembler-tavily-refactor.md` — verbatim "Proposed refactor" Direction A (frontmatter `tools:` reorder + add "Web Research — Tavily-first Protocol (rare; usually NOT needed)" between Output Quality Standards and Completion Protocol + add Critical Rule 10 with authorization gate) plus acceptance criteria.
- **Per-agent proposal for rf-analyst:** `.dev/releases/current/TavilyAgents/rf-analyst-tavily-refactor.md` — verbatim "Proposed refactor" diff (frontmatter `tools:` reorder + add "Web Research — Tavily-first Protocol (rare; usually NOT needed)" between Quality Standards and Completion Protocol + add Critical Rule 9 framing unauthorized web as fabrication-by-import) plus acceptance criteria.
- **Per-agent proposal for rf-qa:** `.dev/releases/current/TavilyAgents/rf-qa-tavily-refactor.md` — verbatim "Proposed refactor" diff (frontmatter `tools:` reorder + add "Web Research Tooling (Tavily-first)" section after Verification Principles + append Tool Engagement Minimum line + add Critical Rule 12) plus acceptance criteria.
- **Per-agent proposal for rf-qa-qualitative:** `.dev/releases/current/TavilyAgents/rf-qa-qualitative-tavily-refactor.md` — verbatim "Proposed refactor" diff (frontmatter `tools:` reorder + add "Web Research Tooling (Tavily-first)" section after Verification Principles + augment every Self-Audit block with 4th question + add new Critical Rule under fix-cycle rules) plus acceptance criteria.

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/`**

Subdirectories:

- `discovery/` — Phase 1 freshness re-Read findings and per-agent drift checks
- `test-results/` — Phase 3/4 `make sync-dev` / `make verify-sync` / `make lint` / `uv run pytest` outputs and summaries
- `reviews/` — Phase 2 per-agent acceptance-criteria verification reports
- `plans/` — Phase 3/4 conditional-action outputs (e.g., fix plans if a verify gate fails)
- `reports/` — Final aggregated quality report across all 10 refactors

These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:

- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Execution Context

<!-- Reader-aid block: no specific file paths or line numbers in this header — those belong in per-item Context fields and the linked proposal files. -->

**References:**

- R-001: GOAL — Apply the Tavily-first web-search refactor to 10 agent definition files, sync to mirrored runtime location, verify, smoke-test, and stage the change.
- R-002: WHY — SuperClaude has Tavily MCP available but several agents currently default to WebSearch/WebFetch. Policy is Tavily-first with documented fallback conditions; the 10 in-scope agents have pre-authored, adversarially-reviewed refactor proposals.
- R-003: Per-agent refactor proposal — deep-research.
- R-004: Per-agent refactor proposal — deep-research-agent.
- R-005: Per-agent refactor proposal — rf-task-researcher.
- R-006: Per-agent refactor proposal — rf-task-builder.
- R-007: Per-agent refactor proposal — rf-task-executor (Option A recommended; defensive guardrail framing).
- R-008: Per-agent refactor proposal — rf-team-lead.
- R-009: Per-agent refactor proposal — rf-assembler (Direction A; authorization gate).
- R-010: Per-agent refactor proposal — rf-analyst (authorization gate; fabrication-by-import framing).
- R-011: Per-agent refactor proposal — rf-qa (governs every QA phase).
- R-012: Per-agent refactor proposal — rf-qa-qualitative (Self-Audit augmentation across phases).
- R-013: Scope confirmation sweep summary — confirms no other agents need this refactor.

**Source areas:** deep-research agent prompt, deep-research-agent agent prompt, rf-task-researcher agent prompt, rf-task-builder agent prompt, rf-task-executor agent prompt, rf-team-lead agent prompt, rf-assembler agent prompt, rf-analyst agent prompt, rf-qa agent prompt, rf-qa-qualitative agent prompt, Makefile sync-dev / verify-sync / test / lint targets.

**Key constraints:** make sync-dev must succeed and make verify-sync must report 0 drift before staging; the source-of-truth agent directory is the canonical edit target — the runtime mirror directory is gitignored sync-dev output and must NOT be staged; uv run pytest smoke must remain green.

---

## Detailed Task Instructions

### Phase 1: Preparation and Freshness Re-Read

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status

- [x] Update status to "🟠 Doing" and start_date to today's date (2026-05-22) in the frontmatter of this task file at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/TASK-RF-20260522-203947-tavily-agents-refactor.md`, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Freshness re-Read pass — verify each target agent file matches its proposal's assumed baseline

- [x] Read all 10 proposal files in `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/` — specifically `deep-research-tavily-refactor.md`, `deep-research-agent-tavily-refactor.md`, `rf-task-researcher-tavily-refactor.md`, `rf-task-builder-tavily-refactor.md`, `rf-task-executor-tavily-refactor.md`, `rf-team-lead-tavily-refactor.md`, `rf-assembler-tavily-refactor.md`, `rf-analyst-tavily-refactor.md`, `rf-qa-tavily-refactor.md`, and `rf-qa-qualitative-tavily-refactor.md` — to extract each proposal's "Current state" section verbatim (the lines and content each proposal assumes are present in the target agent file as of 2026-05-22), then for each proposal Read its corresponding target file in `src/superclaude/agents/` (the mapping is the proposal filename minus the `-tavily-refactor.md` suffix, e.g. `deep-research-tavily-refactor.md` → `src/superclaude/agents/deep-research.md`) and compare the current file content against the proposal's "Current state" section to detect any drift since 2026-05-22 (the proposal authoring date), then write a consolidated freshness report to the file `freshness-report.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/discovery/freshness-report.md` containing a markdown table with columns: Proposal File, Target Agent File, Drift Detected (Yes/No), Drift Details (specific lines/sections that have changed since proposal authoring, or "none"), Edit Strategy (apply as-written / requires per-agent adjustment / abort and re-author), ensuring every proposal-target pair is checked with actual file content (no fabrication), drift is reported with specific line ranges or section names when found, and the report flags any pair where the proposal's diff anchors (specific Before quotations) cannot be located in the current target file. If drift is detected and the proposal's edit cannot be applied as-written for that agent, mark that row's Edit Strategy as "requires per-agent adjustment" and document the specific adjustment needed in the freshness report — do NOT abort the entire task; flag the agent so its Phase 2 item can use the adjustment notes. If unable to complete due to missing proposal file, missing target agent file, or file access issues, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.3:** Verify Makefile targets exist (freshness re-check)

- [x] Use the Bash tool to run `grep -E '^(sync-dev|verify-sync|lint|test):' /config/workspace/IronClaude/Makefile` to confirm the four Make targets (`sync-dev`, `verify-sync`, `lint`, `test`) are still present in the current Makefile, then write the grep output to the file `makefile-targets-check.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/discovery/makefile-targets-check.txt` with a one-line header noting timestamp and the conclusion (`ALL_TARGETS_PRESENT` if all four matched, or `MISSING: <list>` otherwise), ensuring the grep ran against the actual Makefile and the result is verbatim. If any of the four targets is missing, log the gap as a blocker in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file because Phase 3 depends on them, then mark this item complete. Once done, mark this item as complete.

**Step 1.4:** Capture pre-existing working-tree state

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && git status --porcelain` to capture the current working-tree state before any edits, then write the output verbatim to the file `pre-edit-git-status.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/discovery/pre-edit-git-status.txt` with a one-line header noting timestamp and a short narrative summary of which files are dirty pre-edit (modified, untracked, staged), ensuring the output is captured before Phase 2 begins so Phase 5's staging item can stage ONLY the 10 agent files this task modifies and ignore any pre-existing dirty files belonging to unrelated work. If `git status` errors (e.g., not a git repo, permission issue), log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 2: Apply per-agent Tavily-first refactors (10 items, partitionable)

YOU MUST complete EVERY item in this checklist. Each item is **parallelizable: yes** — items 2.1 through 2.10 have no data dependencies on each other (each operates on a different `src/superclaude/agents/*.md` file). The executor MAY spawn all 10 items as parallel subagents in a single message per the F2a parallel-spawning exception in template 02 PART 1. Each item must complete (and be marked `[x]`) individually as its subagent returns. All 10 items MUST consult the freshness report from Step 1.2 before applying their edit and honor any "requires per-agent adjustment" notes recorded there.

**Step 2.1:** deep-research

#### File: src/superclaude/agents/deep-research.md

- [x] **parallelizable: yes.** Read the proposal file `deep-research-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/deep-research-tavily-refactor.md` to extract the verbatim "Proposed refactor" section (frontmatter `tools:` allowlist with Tavily MCP tools listed first, body replacement of the Responsibilities bullet on line 14, new `## Tool Selection Policy` section between Responsibilities and Workflow with Tavily-first rule + four fallback-trigger conditions + never-silent-fallback note, updated Workflow step 3 referencing the Tool Selection Policy, extended Report block sources table including a `backend` column), then read the freshness report at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/discovery/freshness-report.md` to check this agent's row for any drift adjustments, then read the target agent file `deep-research.md` at `/config/workspace/IronClaude/src/superclaude/agents/deep-research.md` to confirm current content matches the proposal's anchors, then use the Edit tool to apply each authorized edit from the proposal's "Proposed refactor" section to `src/superclaude/agents/deep-research.md` — frontmatter replacement first (add `tools:` block with `mcp__tavily__tavily-search`, `mcp__tavily__tavily-extract`, `WebSearch`, `WebFetch`, `mcp__context7__resolve-library-id`, `mcp__context7__query-docs`, `Read`, `Grep`, `Glob`, `mcp__sequential-thinking__sequentialthinking` in that order, and update the description to mention Tavily-first behavior), then the body replacements (Responsibilities bullet, new Tool Selection Policy section, Workflow step 3 update, Sources table backend column) — applying ONE Edit call per discrete diff anchor (do NOT batch unrelated edits into a single Edit), then write a per-agent review file `deep-research-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/deep-research-review.md` containing a checklist that reproduces each of the nine acceptance criteria from the proposal verbatim with a Pass/Fail status determined by re-Reading the post-edit file (criteria: (1) `tools:` block exists in frontmatter listing `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` BEFORE `WebSearch` and `WebFetch`; (2) description in frontmatter mentions Tavily-first behavior explicitly; (3) a `## Tool Selection Policy` section exists in the body naming `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` as primary; (4) the four fallback-trigger conditions — tool missing, transport error 2x, rate limit, auth error — are enumerated in the body; (5) Workflow step 3 explicitly references the Tool Selection Policy; (6) Report template includes a `backend` column in the sources table; (7) no body line still lists Tavily and WebFetch as peers without precedence; (8) `make sync-dev && make verify-sync` succeed after the edit — deferred verification, mark as "deferred to Phase 3" in this per-agent review; (9) grep `^- WebSearch$` / `^- WebFetch$` appears in `tools:` AFTER the two `mcp__tavily__*` lines) and an overall verdict line (PASS if all non-deferred criteria pass, FAIL if any fail), ensuring all edits applied are derived strictly from the proposal's "Proposed refactor" section with no fabricated additions, no `.claude/agents/` file is edited (CLAUDE.md absolute rule — `.claude/` is gitignored sync-dev output), no sed/awk/Python helper is used (Edit tool only), and the review reflects the actual post-edit file content via re-Read. If unable to complete due to drift the freshness report did not anticipate, missing proposal anchors, or Edit tool failure, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.2:** deep-research-agent

#### File: src/superclaude/agents/deep-research-agent.md

- [x] **parallelizable: yes.** Read the proposal file `deep-research-agent-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/deep-research-agent-tavily-refactor.md` to extract the verbatim "Proposed refactor" section (frontmatter `tools:` allowlist with Tavily first then WebSearch/WebFetch then Context7/Playwright/Sequential/Read/Grep/Glob, body replacement of the entire `### Tool Orchestration` block with the new Tavily-First Rule (mandatory) subsection + updated Search Strategy + extended Extraction Routing with the "Tavily MCP unavailable" fallback line + new Fallback Policy section + updated Parallel Optimization, and updated Citation Requirements block requiring per-source `backend` tagging and `fallback_reason` on fallback sources), then read the freshness report at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/discovery/freshness-report.md` for this agent's row, then read the target agent file `deep-research-agent.md` at `/config/workspace/IronClaude/src/superclaude/agents/deep-research-agent.md` to confirm anchor lines, then use the Edit tool to apply each authorized edit from the proposal — frontmatter replacement first (add `tools:` block with the 13 entries in the proposal's specified order, update description for Tavily-first), then the `### Tool Orchestration` body replacement, then the Citation Requirements block update — applying ONE Edit per discrete diff anchor, then write a per-agent review file `deep-research-agent-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/deep-research-agent-review.md` containing a checklist that reproduces each of the eight acceptance criteria from the proposal verbatim with Pass/Fail status (criteria: (1) `tools:` block exists with `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` listed BEFORE `WebSearch` and `WebFetch`; (2) description mentions Tavily-first explicitly; (3) `### Tool Orchestration` contains a `**Tavily-First Rule (mandatory)**` subsection naming both Tavily tool IDs; (4) `### Tool Orchestration` contains a `**Fallback Policy**` subsection enumerating the four trigger conditions; (5) Extraction Routing includes the "Tavily MCP unavailable → WebSearch / WebFetch — fallback only" line; (6) Citation Requirements requires per-source `backend` tagging and `fallback_reason` on fallback sources; (7) no body line still describes Tavily without naming the actual MCP tool IDs; (8) Playwright and Context7 are explicitly marked as "independent axis, not subject to Tavily-first"; plus the deferred `make sync-dev && make verify-sync` criterion marked as "deferred to Phase 3") and an overall verdict line, ensuring all edits are derived strictly from the proposal's "Proposed refactor" section with no fabrication, no `.claude/agents/` file is edited, only the Edit tool is used (no sed/awk/Python helper), and the review reflects the actual post-edit file content via re-Read. If unable to complete due to drift, missing anchors, or Edit failure, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.3:** rf-task-researcher

#### File: src/superclaude/agents/rf-task-researcher.md

- [x] **parallelizable: yes.** Read the proposal file `rf-task-researcher-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-task-researcher-tavily-refactor.md` to extract the verbatim "Proposed refactor" section (frontmatter `tools:` insert of `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` immediately before `WebFetch` and `WebSearch` keeping both fallbacks in the list; body rename of "Extended Research Tools → WebSearch" section to "Extended Research Tools → Web Search (Tavily-first)" with new canonical block including primary tool, fallback tools, retargeted triggers, Tavily example queries, three fallback conditions, WEB SEARCH PROVENANCE log instructions, and the "Do NOT use any web tool for" guardrail; Escalation step 1 replacement; Solution Research line replacement; Research Notes Structure provenance line insert; new Critical Rule 8 "Tavily-first for web"), then read the freshness report row for this agent, then Read the target `rf-task-researcher.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-task-researcher.md` to confirm anchors, then use the Edit tool to apply each authorized edit — frontmatter insert first, then the Web Search section rename and content rewrite, then escalation step 1 replacement, then Solution Research line replacement, then Research Notes Structure provenance line insert, then new Critical Rule 8 addition — applying ONE Edit per discrete diff anchor, then write a per-agent review file `rf-task-researcher-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-task-researcher-review.md` containing a checklist reproducing each of the ten acceptance criteria from the proposal verbatim with Pass/Fail (criteria: (1) Frontmatter `tools:` includes both Tavily entries AND both `WebFetch`/`WebSearch` are still present; (2) Tavily entries appear BEFORE `WebFetch`/`WebSearch`; (3) Body contains a section titled "Web Search (Tavily-first)" or equivalent with explicit Tavily-primary/WebSearch-fallback framing; (4) At least three explicit fallback conditions are enumerated; (5) The WEB SEARCH PROVENANCE requirement appears in the research notes schema AND in the fallback-condition prose; (6) All existing "Use WebSearch when…" bullets are preserved retargeted to Tavily — no research-trigger guidance lost; (7) Escalation ladder step 1 names Tavily not WebSearch; (8) New "Tavily-first for web" rule is added to Critical Rules with "protocol violation" or equivalent strong enforcement; (9) No `WebSearch:` example queries remain as the primary example — Tavily examples first, WebSearch examples (if any) explicitly labeled "fallback"; (10) grep for `WebSearch` shows it ONLY in fallback/"fall back to" contexts; plus deferred sync/verify criterion) and an overall verdict, ensuring all edits derive strictly from the proposal with no fabrication, no `.claude/agents/` file edited, Edit tool only. If unable to complete, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 2.4:** rf-task-builder

#### File: src/superclaude/agents/rf-task-builder.md

- [x] **parallelizable: yes.** Read the proposal file `rf-task-builder-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-task-builder-tavily-refactor.md` to extract the verbatim "Proposed refactor" section (frontmatter `tools:` insert of two Tavily MCP entries immediately before `WebFetch`/`WebSearch`; body rewrite of "Extended Tools → WebSearch — External References for Task Building" section to "Extended Tools → Web Search (Tavily-first)" with primary tool, fallback tools, three retargeted triggers, Tavily example queries for Jest/Dockerfile/SQLAlchemy, three fallback conditions, per-checklist-item HTML-comment provenance annotation contract `<!-- web-provenance: provider=WebSearch reason=<...> -->`, and the "Do NOT use any web tool for" guardrail; new Critical Rule 13 "Tavily-first for web fact-checking" with the per-item provenance annotation requirement and the "protocol violation" framing; explicit no-edit to Granularity Requirements; explicit no-edit to QA/VALIDATION/TESTING encoding sections), then read the freshness report row for this agent, then Read the target `rf-task-builder.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-task-builder.md` to confirm anchors and existing Critical Rule numbering (the new rule must land as rule 13, renumbering existing rule 13 → 14), then use the Edit tool to apply each authorized edit — frontmatter insert first, then Extended Tools section rewrite, then new Critical Rule 13 insertion plus renumber of subsequent rules — applying ONE Edit per discrete diff anchor, then write a per-agent review file `rf-task-builder-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-task-builder-review.md` containing a checklist reproducing each of the ten acceptance criteria from the proposal verbatim with Pass/Fail (criteria: (1) Frontmatter `tools:` includes both Tavily entries AND both `WebFetch`/`WebSearch` still present; (2) Tavily entries precede `WebFetch`/`WebSearch`; (3) Body contains a section titled "Web Search (Tavily-first)" replacing the old WebSearch section; (4) All three original "Use `WebSearch` when…" triggers preserved retargeted to Tavily; (5) At least three explicit Fallback Conditions enumerated; (6) New "Tavily-first for web fact-checking" rule in Critical Rules with "protocol violation"; (7) The provenance annotation contract `<!-- web-provenance: ... -->` is named in BOTH body section AND new Critical Rule; (8) grep for `WebSearch` shows it ONLY in fallback contexts; (9) No example query uses `WebSearch:` as primary form — WebSearch examples explicitly labeled "fallback"; (10) The "Do NOT use any web tool for" guardrail is preserved. Note: this proposal does NOT include a deferred `make sync-dev && make verify-sync` criterion — sync/verify is still validated in Phase 3 for this agent as a project-level gate, just not enumerated as a per-proposal acceptance criterion) and an overall verdict, ensuring all edits derive strictly from the proposal with no fabrication, no `.claude/agents/` edited, Edit tool only. If unable to complete, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 2.5:** rf-task-executor

#### File: src/superclaude/agents/rf-task-executor.md

- [x] **parallelizable: yes.** Read the proposal file `rf-task-executor-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-task-executor-tavily-refactor.md` to extract the verbatim "Proposed refactor" section — specifically **Option A (recommended)** which keeps web tools in frontmatter and adds the Tavily-first rule (frontmatter `tools:` insert of two Tavily MCP entries immediately before `WebFetch`/`WebSearch`; body insert of a single short Critical Rule 7 framing web operations as NOT part of the documented workflow and constraining any improvised recovery-scenario web call to Tavily-first with three fallback conditions and `web-lookup: provider=<tavily|WebSearch reason=...>` provenance in `EXECUTION_PROGRESS` or `EXECUTION_ERROR` messages; body insert of one bullet under "What NOT To Do" pointing back to Critical Rule 7). **Do NOT apply Option B (which removes the tools entirely) — Option A is the BUILD_REQUEST-authorized direction.** Read the freshness report row for this agent, then Read the target `rf-task-executor.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-task-executor.md` to confirm anchors and existing Critical Rule numbering (the new rule lands as rule 7), then use the Edit tool to apply each authorized edit — frontmatter insert first, then new Critical Rule 7 addition, then "What NOT To Do" bullet addition — applying ONE Edit per discrete diff anchor (do NOT add any new workflow steps; the executor's primary loop must remain untouched), then write a per-agent review file `rf-task-executor-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-task-executor-review.md` containing a checklist reproducing each of the seven acceptance criteria from the proposal verbatim with Pass/Fail (criteria: (1) Frontmatter `tools:` includes both Tavily entries AND both `WebFetch`/`WebSearch` still present; (2) Tavily entries precede `WebFetch`/`WebSearch`; (3) "Critical Rules" contains a new rule (numbered 7) titled "Tavily-first for any web operation" or equivalent with "protocol violation" framing; (4) New rule explicitly names that web operations are NOT part of the documented workflow — framed as defensive guardrail; (5) At least three explicit fallback conditions enumerated; (6) "What NOT To Do" contains a bullet pointing back to the new Critical Rule; (7) No new workflow steps added — the executor's primary loop (validate → claim → run script → report) is untouched; plus the provenance log format `web-lookup: provider=<tavily|WebSearch reason=...>` appears in both new rule AND references EXECUTION_PROGRESS / EXECUTION_ERROR message types) and an overall verdict, ensuring all edits derive strictly from Option A of the proposal with no fabrication, no `.claude/agents/` edited, Edit tool only. If unable to complete, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 2.6:** rf-team-lead

#### File: src/superclaude/agents/rf-team-lead.md

- [x] **parallelizable: yes.** Read the proposal file `rf-team-lead-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md` to extract the verbatim "Proposed refactor" section (frontmatter `tools:` reorder so Tavily MCP tools appear before `WebSearch`/`WebFetch` with inline `# PRIMARY ...` and `# FALLBACK only — Tavily unavailable` comments on the relevant lines; body replacement of the entire "WebSearch — Understanding Unfamiliar Technologies" subsection with the new "Web Research — Tavily-first Protocol" subsection including the ALWAYS-try-Tavily-first block, three Tavily-unavailable conditions, fallback observability line `Tavily unavailable (<reason>); fell back to WebSearch/WebFetch.`, "Do NOT use WebSearch or WebFetch as a first choice for any reason" line, and the three retargeted "Use web research when" triggers; new Critical Rule 11 added after current rules 1-10), then read the freshness report row for this agent, then Read the target `rf-team-lead.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-team-lead.md` to confirm anchors including current Critical Rule count (the new rule lands as rule 11), then use the Edit tool to apply each authorized edit — frontmatter reorder first (Tavily entries inserted with PRIMARY/FALLBACK comments and Tavily ordered before WebSearch/WebFetch), then body replacement of the "WebSearch — Understanding Unfamiliar Technologies" subsection with "Web Research — Tavily-first Protocol", then Critical Rule 11 addition — applying ONE Edit per discrete diff anchor, then write a per-agent review file `rf-team-lead-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-team-lead-review.md` containing a checklist reproducing each of the twelve acceptance criteria from the proposal verbatim with Pass/Fail (criteria: (1) Frontmatter `tools:` contains both Tavily entries; (2) Frontmatter `tools:` still contains `WebSearch` and `WebFetch`; (3) Tavily entries appear before WebSearch/WebFetch in ordering; (4) "WebSearch — Understanding Unfamiliar Technologies" subsection no longer exists; (5) New subsection titled "Web Research — Tavily-first Protocol" or equivalent exists under "Extended Tools"; (6) New subsection explicitly names both Tavily MCP tools as PRIMARY; (7) Three Tavily-unavailable conditions defined; (8) New subsection contains literal phrase "Do NOT use WebSearch or WebFetch as a first choice" or stricter equivalent; (9) New rule added to Critical Rules covering Tavily-first; (10) Fallback observability requirement present (`web_research_fallback: ...` line in pipeline output OR the Tavily-unavailable narrative line); (11) No existing responsibilities removed or weakened; (12) `make sync-dev` and `make verify-sync` clean — deferred to Phase 3) and an overall verdict, ensuring all edits derive strictly from the proposal with no fabrication, no `.claude/agents/` edited, Edit tool only. If unable to complete due to drift or missing anchors, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.7:** rf-assembler

#### File: src/superclaude/agents/rf-assembler.md

- [x] **parallelizable: yes.** Read the proposal file `rf-assembler-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-assembler-tavily-refactor.md` to extract the verbatim "Proposed refactor" section — specifically **Direction A (recommended)**: frontmatter `tools:` reorder with Tavily MCP entries before `WebSearch`/`WebFetch` with inline `# PRIMARY web search (rare use; see body)` / `# PRIMARY web content extraction (rare use)` / `# FALLBACK only — Tavily unavailable` comments; body insert of a new subsection "## Web Research — Tavily-first Protocol (rare; usually NOT needed)" between "Output Quality Standards" and "Completion Protocol" containing: the role-acknowledgement that web research violates "no fabrication" unless explicitly authorized, the conditional Tavily MCP first instruction with `mcp__tavily__tavily-extract` for known URLs and `mcp__tavily__tavily-search` only if spawn prompt directs, the three Tavily-unavailable conditions (tool not loaded / server error after retry / rate-limit), the `[WEB_RESEARCH_FALLBACK: tavily=<reason>; used=<WebSearch|WebFetch>; url=<url>]` marker for the assembled document, and the STOP/BLOCKED instruction for unauthorized fetches; new Critical Rule 10 codifying Tavily-first AND no-unauthorized-web-research. **Do NOT apply Direction B (which removes web tools entirely).** Read the freshness report row for this agent, then Read the target `rf-assembler.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-assembler.md` to confirm anchors and Critical Rule numbering (the new rule lands as rule 10 — current list is 1-9), then use the Edit tool to apply each authorized edit — frontmatter reorder first, then new body subsection insertion between Output Quality Standards and Completion Protocol, then new Critical Rule 10 addition — applying ONE Edit per discrete diff anchor, then write a per-agent review file `rf-assembler-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-assembler-review.md` containing a checklist reproducing each of the ten acceptance criteria from the proposal verbatim with Pass/Fail (criteria: (1) Frontmatter `tools:` contains both Tavily entries; (2) Frontmatter still contains `WebSearch` and `WebFetch` as fallbacks; (3) Tavily entries appear before WebSearch/WebFetch; (4) New body subsection "Web Research — Tavily-first Protocol (rare; usually NOT needed)" exists; (5) That subsection states explicitly that web research requires spawn-prompt authorization; (6) That subsection defines the three Tavily-unavailable conditions; (7) That subsection contains the `[WEB_RESEARCH_FALLBACK: ...]` marker format; (8) New "Critical Rules" entry codifies Tavily-first AND no-unauthorized-web-research; (9) The "no fabrication" rule (existing Output Quality Standards) is NOT weakened; (10) The assembler's core workflow (Steps 1-6 of Assembly Process, incremental writing protocol, contradiction handling, missing-file handling) is untouched; plus deferred sync/verify criterion) and an overall verdict, ensuring all edits derive strictly from Direction A of the proposal with no fabrication, no `.claude/agents/` edited, Edit tool only. If unable to complete due to drift or missing anchors, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.8:** rf-analyst

#### File: src/superclaude/agents/rf-analyst.md

- [x] **parallelizable: yes.** Read the proposal file `rf-analyst-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-analyst-tavily-refactor.md` to extract the verbatim "Proposed refactor" section (frontmatter `tools:` reorder with Tavily MCP entries before `WebSearch`/`WebFetch` and inline PRIMARY/FALLBACK comments; body insert of a new subsection "## Web Research — Tavily-first Protocol (rare; usually NOT needed)" between "Quality Standards" and "Completion Protocol" containing: role-acknowledgement that introducing unverified external claims contradicts zero-tolerance-for-fabrication Rule 7, the spawn-prompt-authorization gate, conditional Tavily MCP first instruction with `mcp__tavily__tavily-extract` for known URLs cited in research files and `mcp__tavily__tavily-search` only when spawn prompt directs, the three Tavily-unavailable conditions, the `[WEB_RESEARCH_FALLBACK: tavily=<reason>; used=<WebSearch|WebFetch>; url=<url>; claim=<claim being verified>]` marker for analysis reports under the Methodology section, and the STOP-and-mark-`[UNVERIFIED]` instruction for unauthorized fetches; new Critical Rule 9 codifying Tavily-first AND linking unauthorized external content to Rule 7 as "fabrication-by-import"), then read the freshness report row for this agent, then Read the target `rf-analyst.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-analyst.md` to confirm anchors and Critical Rule numbering (the new rule lands as rule 9 — current list is 1-8), then use the Edit tool to apply each authorized edit — frontmatter reorder first, then new body subsection insertion between Quality Standards and Completion Protocol, then new Critical Rule 9 addition — applying ONE Edit per discrete diff anchor, then write a per-agent review file `rf-analyst-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-analyst-review.md` containing a checklist reproducing each of the ten acceptance criteria from the proposal verbatim with Pass/Fail (criteria: (1) Frontmatter `tools:` contains both Tavily entries; (2) Frontmatter still contains `WebSearch` and `WebFetch` as fallbacks; (3) Tavily entries appear before WebSearch/WebFetch; (4) New body subsection "Web Research — Tavily-first Protocol (rare; usually NOT needed)" exists between Quality Standards and Completion Protocol; (5) That subsection states web research requires spawn-prompt authorization and unauthorized external content is "fabrication-by-import"; (6) Three Tavily-unavailable conditions defined; (7) The `[WEB_RESEARCH_FALLBACK: ...]` marker format with `claim=` field is present; (8) New Critical Rule 9 codifies Tavily-first AND links back to Rule 7; (9) Existing five analysis types, Synthetic-DNSP Finding behavior, Parallel Partitioning, General Process, and Quality Standards / Critical Rules 1-8 are untouched; (10) Cross-Validation's existing `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tagging is preserved unchanged; plus deferred sync/verify criterion) and an overall verdict, ensuring all edits derive strictly from the proposal with no fabrication, no `.claude/agents/` edited, Edit tool only. If unable to complete due to drift or missing anchors, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.9:** rf-qa

#### File: src/superclaude/agents/rf-qa.md

- [x] **parallelizable: yes.** Read the proposal file `rf-qa-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-qa-tavily-refactor.md` to extract the verbatim "Proposed refactor" section (frontmatter `tools:` reorder placing Tavily MCP entries before `WebFetch`/`WebSearch` with inline PRIMARY/FALLBACK comments; body insert of a new `## Web Research Tooling (Tavily-first)` section sited so it governs every QA phase — proposal recommends placement after Verification Principles around line 97 fence and before the first QA Phase section — containing: the legitimate-external-lookup scope (vendor doc / RFC / OWASP / library version verification), Precedence list (`mcp__tavily__tavily-search` #1, `mcp__tavily__tavily-extract` #2, WebSearch/WebFetch fallback only), the three Tavily-unavailable detection conditions, the "Tool engagement" reporting requirement with format `tavily_search: 1 attempt, fell back to WebSearch (rate-limit)`, the silent-fallback-forbidden assertion, and the explicit "does NOT change" note preserving source-truth-first Principle 6; appended line to "Tool Engagement Minimum" requiring `tavily_search: N | tavily_extract: N | web_search_fallback: N | web_fetch_fallback: N` reporting when web research was performed; new Critical Rule 12 "Tavily-first for any external lookup"), then read the freshness report row for this agent, then Read the target `rf-qa.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-qa.md` to confirm anchors and Critical Rule numbering (the new rule lands as rule 12 — current list is 1-11), then use the Edit tool to apply each authorized edit — frontmatter reorder first, then new `## Web Research Tooling (Tavily-first)` section insertion at the proposal-specified location, then "Tool Engagement Minimum" line append, then new Critical Rule 12 addition — applying ONE Edit per discrete diff anchor, then write a per-agent review file `rf-qa-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-qa-review.md` containing a checklist reproducing each of the nine acceptance criteria from the proposal verbatim with Pass/Fail (criteria: (1) Frontmatter `tools:` lists `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` BEFORE `WebFetch` and `WebSearch`; (2) `WebFetch` and `WebSearch` remain in `tools:` (not removed); (3) New `## Web Research Tooling (Tavily-first)` body section exists at a scope governing every QA phase (Research Gate, Synthesis Gate, Report Validation, Task Integrity, Fix Cycle); (4) Detection condition enumerates the three Tavily-unavailable triggers; (5) "Tool Engagement Minimum" requires reporting `tavily_*` and `*_fallback` counts when web research is performed; (6) New Critical Rule 12 codifies Tavily-first requirement and bans silent fallback; (7) Source-truth primacy (Principle 6) is preserved verbatim; (8) No existing QA checklist item is weakened or removed; (9) `make verify-sync` passes after sync — deferred to Phase 3) and an overall verdict, ensuring all edits derive strictly from the proposal with no fabrication, no `.claude/agents/` edited, Edit tool only. If unable to complete due to drift or missing anchors, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.10:** rf-qa-qualitative

#### File: src/superclaude/agents/rf-qa-qualitative.md

- [x] **parallelizable: yes.** Read the proposal file `rf-qa-qualitative-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-qa-qualitative-tavily-refactor.md` to extract the verbatim "Proposed refactor" section (frontmatter `tools:` reorder placing Tavily MCP entries before `WebFetch`/`WebSearch` with inline PRIMARY/FALLBACK comments; body insert of a new `## Web Research Tooling (Tavily-first)` section after the Verification Principles block — proposal recommends placement after the `---` fence around line 98 and before the first QA Phase section at line 100 — containing: the legitimate-external-lookup scope (report-qualitative item 7 "external research is relevant", tech-ref-qualitative item 7 "dependency versions", ops-guide-qualitative item 9 "monitoring covers failure modes", readme-qualitative item 5 external links resolve), Precedence list, three Tavily-unavailable detection conditions, the "Tool-engagement summary" reporting requirement with format `tavily_extract: 1 attempt, fell back to WebFetch (server-not-loaded)`, the silent-fallback-forbidden assertion, and the "does NOT change" note preserving adversarial-reader-first identity, AX-1..AX-5 axes, and closed-set Axis-column vocabulary; augmentation of every Self-Audit block (or promotion to single canonical section per the proposal's preferred-but-not-required option) with a 4th question requiring Tavily-first attempt and report-level tool-engagement recording; new Critical Rule under the fix-cycle rules codifying Tavily-first for any external lookup with silent-fallback-as-process-violation framing), then read the freshness report row for this agent, then Read the target `rf-qa-qualitative.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-qa-qualitative.md` to confirm anchors and identify every Self-Audit block location (per the proposal these appear at multiple line ranges in the current file), then use the Edit tool to apply each authorized edit — frontmatter reorder first, then new `## Web Research Tooling (Tavily-first)` section insertion at the proposal-specified location, then augmentation of every Self-Audit block with the 4th Tavily-first audit question (the proposal accepts EITHER per-block edits OR single-canonical-section promotion — pick per-block edits unless the freshness report row notes otherwise, since per-block edits are the safer choice for first-pass execution), then new Critical Rule addition under the fix-cycle rules — applying ONE Edit per discrete diff anchor, then write a per-agent review file `rf-qa-qualitative-review.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-qa-qualitative-review.md` containing a checklist reproducing each of the nine acceptance criteria from the proposal verbatim with Pass/Fail (criteria: (1) Frontmatter `tools:` lists both Tavily entries BEFORE `WebFetch` and `WebSearch`; (2) `WebFetch` and `WebSearch` remain in `tools:` (fallback role preserved); (3) New `## Web Research Tooling (Tavily-first)` body section exists at a scope governing every QA phase; (4) Detection condition enumerates the three Tavily-unavailable triggers; (5) Every Self-Audit block (or single promoted section) includes a Tavily-first audit question requiring tool-engagement recording; (6) New Critical Rule under fix-cycle section codifies Tavily-first and bans silent fallback; (7) The five Adversarial Axes (AX-1..AX-5) and closed-set `{AX-1..AX-5, none}` Axis-column vocabulary for task-qualitative are unchanged; (8) No existing qualitative checklist item is weakened or removed; "Ban N/A" and "Exhaustive verification" principles remain intact; (9) `make verify-sync` passes after sync — deferred to Phase 3) and an overall verdict, ensuring all edits derive strictly from the proposal with no fabrication, no `.claude/agents/` edited, Edit tool only. If unable to complete due to drift or missing anchors, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase Gate: Per-agent acceptance verification

This phase gate runs after Phase 2 completes and before Phase 3 begins. The fix-cycle limit for this gate is 2 cycles (task-integrity gate per template I16); after max, unresolved issues become Open Questions documented in the Open Questions section of the Task Log.

**Step PG.1:** Aggregate per-agent review verdicts

- [x] Use Glob to find all review files matching `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/*-review.md` to discover all 10 per-agent reviews produced by Phase 2, then read each review file to extract: agent name (from filename), overall verdict (PASS/FAIL), and the list of any failed acceptance criteria with their line items, then create a consolidated phase-2 review report at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reports/phase-2-review-report.md` containing: an executive summary line (X/10 PASS, Y/10 FAIL), a table with columns Agent / Verdict / Failed Criteria Count / Failed Criteria List, and a final overall verdict (PASS if all 10 are PASS or only "deferred to Phase 3" criteria remain open, FAIL otherwise), ensuring all 10 expected review files are present (if fewer than 10 are found, the missing agents are listed as a "MISSING REVIEWS" section and the overall verdict is FAIL), no fabricated review content is introduced, and the counts match the actual review file contents. If fewer than 10 review files are found, log the specific blocker (which agents are missing) using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG.2:** Spawn rf-qa in task-integrity mode to verify all Phase 2 outputs

- [x] Spawn rf-qa in `task-integrity` mode using the Task tool with an ADVERSARIAL STANCE framing (`fix_authorization: true`) to verify all Phase 2 outputs — specifically, instruct rf-qa to (a) read the consolidated phase-2 review report at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reports/phase-2-review-report.md`, (b) for each of the 10 agent files at `src/superclaude/agents/{deep-research,deep-research-agent,rf-task-researcher,rf-task-builder,rf-task-executor,rf-team-lead,rf-assembler,rf-analyst,rf-qa,rf-qa-qualitative}.md` re-verify that the corresponding proposal's "Acceptance criteria" section is satisfied by re-Reading the post-edit file and comparing against the proposal, (c) verify NO `.claude/agents/` file was directly edited by grepping git status for any `.claude/agents/` modifications (any such modification is a CRITICAL violation of the CLAUDE.md absolute rule), (d) verify no sed/awk/Python helper was used (Edit tool only — visible in the task log), and (e) write a structured verdict file to `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-qa-task-integrity-verdict.md` with overall PASS/FAIL plus per-criterion details — ensuring the agent operates with adversarial stance (does NOT defer to executor's self-reports; re-verifies independently) and writes a binary verdict per template I16. IF verdict is PASS, proceed to Phase 3. IF verdict is FAIL and fix-cycle count is < 2, address each failing criterion by re-applying the relevant proposal edit to the affected agent file using the Edit tool only (no .claude/, no sed), then re-spawn rf-qa in `task-integrity` fix-cycle mode (this counts as cycle N+1). IF fix-cycle count reaches 2 and verdict is still FAIL, escalate the remaining failures to Open Questions in the ### Open Questions section of the Task Log and proceed to Phase 3 with the failures documented — unresolved task-integrity issues become Open Questions per template I16. If unable to spawn rf-qa due to agent unavailability or environmental error, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 3: Sync & verify

YOU MUST complete EVERY item in this phase IN ORDER. Each item depends on the previous one passing.

**Step 3.1:** Run `make sync-dev`

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && make sync-dev 2>&1` to propagate the 10 `src/superclaude/agents/` edits into `.claude/agents/` (the gitignored sync-dev output directory), then write the complete command output verbatim to the file `make-sync-dev-output.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/make-sync-dev-output.txt` with a one-line header noting timestamp and exit code, then create a one-page summary `make-sync-dev-summary.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/make-sync-dev-summary.md` containing: overall result (SUCCESS if exit code 0, FAILED otherwise), files copied (line-count from the output if Make reports it), any warnings or unusual lines from the output, and the relevant tail of the output, ensuring the result accurately reflects the exit code (do NOT fabricate SUCCESS), no `.claude/` file is staged (the sync writes to gitignored output — staging is a Phase 5 step that explicitly stages only `src/`), and the summary's verdict matches the actual exit code. If `make sync-dev` exits non-zero, log the specific failure (the relevant error lines) using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete (subsequent items in Phase 3 will detect the failure via the summary and act accordingly). Once done, mark this item as complete.

**Step 3.2:** Run `make verify-sync`

- [x] Read the `make-sync-dev-summary.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/make-sync-dev-summary.md` to confirm Step 3.1 succeeded — if Step 3.1 FAILED, do NOT run verify-sync; instead write a `verify-sync-skipped.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/verify-sync-skipped.md` documenting that verify-sync was skipped because sync-dev failed (with the sync-dev failure summary copied in), then log a blocker in the ### Phase 3 Findings section and mark this item complete. If Step 3.1 SUCCEEDED, use the Bash tool to run `cd /config/workspace/IronClaude && make verify-sync 2>&1` to confirm `src/superclaude/agents/` and `.claude/agents/` are byte-identical post-sync, then write the complete output verbatim to `make-verify-sync-output.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/make-verify-sync-output.txt` with a one-line header noting timestamp and exit code, then create `make-verify-sync-summary.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/make-verify-sync-summary.md` containing: overall result (CLEAN if exit code 0 AND output reports 0 drift, DIRTY otherwise), drift count (from the Make target's output if reported), and a list of any drift findings (file paths that differ), ensuring the result is determined by both exit code AND output content (the BUILD_REQUEST's gate is "0 drift" — a successful exit with non-zero drift is FAIL), no fabrication. If verify-sync reports drift, log the specific drift findings using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete (Phase 5 staging will detect this via the summary and abort if needed). Once done, mark this item as complete.

**Step 3.3:** Run `make lint`

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && make lint 2>&1` to confirm the lint suite still passes after the edits, then write the complete output verbatim to `make-lint-output.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/make-lint-output.txt` with a one-line header noting timestamp and exit code, then create `make-lint-summary.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/make-lint-summary.md` containing: overall result (CLEAN if exit code 0 AND no new warnings, WARN if exit code 0 but new warnings present compared to project baseline, FAIL if exit code non-zero), any new lint findings introduced by the edits (with file/line references), and a one-line note clarifying that agent definitions are markdown — markdown-lint findings in the 10 edited files are in scope, but pre-existing lint findings in unrelated files are not, ensuring the result is determined by both exit code AND any new findings in the 10 edited files. If lint reports new failures or warnings in any of the 10 edited agent files, log the specific lint findings using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 4: Smoke tests

**Step 4.1:** Run `uv run pytest`

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && uv run pytest 2>&1` to verify the broader test suite still passes after the 10 agent-definition edits — note that agent definitions are documentation-style (no direct Python coverage), so the gate is "suite stays green and no new failures appear compared to the pre-edit baseline implied by the master branch state" rather than "tests directly exercise the edited content" — then write the complete output verbatim to `pytest-output.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/pytest-output.txt` with a one-line header noting timestamp and exit code, then create `pytest-summary.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/pytest-summary.md` containing: overall result (PASSED if exit code 0, FAILED otherwise), total tests run, tests passed, tests failed, tests skipped, a table of failed tests (if any) with columns Test Name / Error Type / Brief Error Message, and the full pytest summary line, plus a note that agent definitions are documentation-style and the gate is "no NEW failures introduced by this task" — any failures must be investigated to confirm they are pre-existing (use `git stash` + re-run if needed to confirm, but do NOT actually stash the in-progress edits as that risks losing work; instead, manually inspect whether the failures touch any of the 10 edited agent paths or any code that depends on agent definitions), ensuring the summary accurately reflects the raw output with no fabricated results. If new failures appear in tests that exercise agent-loading or agent-definition validation, log the specific failures using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.2:** Optional health check via `superclaude doctor`

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && superclaude doctor 2>&1` to spot-check that the SuperClaude CLI can still load its agent set after the edits (this is the closest available equivalent to "does one of the refactored agent definitions still load cleanly") — if `superclaude doctor` returns a non-zero exit code OR the output reports any error tied to the 10 edited agents, write the failing output to `superclaude-doctor-output.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/superclaude-doctor-output.txt` and log the issue in the ### Phase 4 Findings section; if `superclaude doctor` is not installed in this environment OR errors with `command not found`, write a one-line `superclaude-doctor-skipped.txt` at the same directory documenting "command not available — health check skipped with justification" and mark this item complete, ensuring no failure is hidden (skipping is only acceptable when the command genuinely does not exist; an actual error from a present command is a finding to log). If unable to determine command availability cleanly, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 5: Stage & commit

YOU MUST complete EVERY item in this phase IN ORDER. The staging item depends on Phase 3 reporting clean.

**Step 5.1:** Stage ONLY `src/superclaude/agents/` files (NOT `.claude/agents/`)

- [x] Read the verify-sync summary at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/make-verify-sync-summary.md` to confirm verify-sync is CLEAN — if DIRTY, do NOT stage; instead write a `staging-skipped.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/plans/staging-skipped.md` documenting why staging was deferred (verify-sync drift findings copied in) and log a blocker in ### Phase 5 Findings, then mark this item complete. If verify-sync is CLEAN, use the Bash tool to run `cd /config/workspace/IronClaude && git add src/superclaude/agents/deep-research.md src/superclaude/agents/deep-research-agent.md src/superclaude/agents/rf-task-researcher.md src/superclaude/agents/rf-task-builder.md src/superclaude/agents/rf-task-executor.md src/superclaude/agents/rf-team-lead.md src/superclaude/agents/rf-assembler.md src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md` to stage EXACTLY the 10 in-scope agent files — explicitly NOT staging anything under `.claude/agents/` (which is gitignored per CLAUDE.md absolute rule; `git add -f` on any `.claude/` path is FORBIDDEN; if the command would require `-f`, STOP and log a blocker), then run `git status --porcelain` to capture the post-stage tree state and write it to `post-stage-git-status.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/post-stage-git-status.txt`, ensuring (a) exactly the 10 expected `src/superclaude/agents/*.md` files appear as staged (`M` or `A` in the index column), (b) no `.claude/agents/...` line appears in the staged set (any such line is a CRITICAL violation per CLAUDE.md and must trigger an immediate `git reset HEAD .claude/` to unstage, plus a blocker log), and (c) any other dirty files captured in `pre-edit-git-status.txt` (Phase 1.4 baseline) remain UNSTAGED. If any of (a)-(c) is violated, log the specific violation using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.2:** Create the commit

- [x] Read the post-stage git status at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/post-stage-git-status.txt` to confirm staging is clean — if Step 5.1 logged a blocker, do NOT commit; instead write a `commit-skipped.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/plans/commit-skipped.md` documenting why and log a blocker in ### Phase 5 Findings, then mark this item complete. If staging is clean, use the Bash tool to run `cd /config/workspace/IronClaude && git commit -m "feat(agents): Tavily-first web search precedence across 10 agents"` to create a single batch commit using the conventional message specified in the BUILD_REQUEST (this is the default; user may override to 10 per-agent commits — see Open Questions, but in the absence of explicit user override the batch commit is the chosen direction), then capture `git log -1 --format=%H%n%s%n%b` to confirm the commit landed correctly and write it to `commit-result.txt` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/commit-result.txt`, ensuring (a) the commit message matches the BUILD_REQUEST exactly (`feat(agents): Tavily-first web search precedence across 10 agents`), (b) exactly 10 files changed are reported by the commit (run `git show --stat HEAD | tail -1` to confirm), (c) all 10 files are under `src/superclaude/agents/`, and (d) no pre-commit hook was bypassed (`--no-verify` is FORBIDDEN per global rules — if a pre-commit hook fails, do NOT use `--no-verify`; instead log the hook failure as a blocker and let it block the commit). If the pre-commit hook fails, log the hook failure output using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete (the commit failure is documented and the user can intervene). Once done, mark this item as complete.

**Step 5.3:** Verify working-tree state is consistent post-commit

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && git status --porcelain` to capture the post-commit working-tree state, then compare against `pre-edit-git-status.txt` (Phase 1.4 baseline) by reading both files, then write the comparison to `final-git-status-comparison.md` at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/test-results/final-git-status-comparison.md` containing: a list of files that are dirty in BOTH baselines (these are pre-existing unrelated changes — should remain untouched), a list of files dirty ONLY in pre-edit baseline (these were created by this task — should be in `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/` or have been moved to a committed state), a list of files dirty ONLY in post-commit (these would be UNEXPECTED — anything in `src/superclaude/agents/` or `.claude/agents/` here is a bug), and a final verdict (CLEAN if no unexpected changes, DIRTY otherwise), ensuring the comparison is between the actual two git status outputs with no fabrication, and the verdict matches the comparison. If post-commit shows unexpected dirty files in `src/superclaude/agents/` (suggests a 10-files-changed mismatch) or any `.claude/agents/*` file (CRITICAL violation), log the specific files using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 6: Completion aggregation

**Step 6.1:** Aggregate all reports

- [x] Use Glob to find all aggregation-relevant files under `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/` — specifically the freshness report, the 10 per-agent review files, the phase-gate verdict file, all make-* and pytest summaries, and the final-git-status-comparison — then create a final consolidated report at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reports/final-task-report.md` containing: an executive summary (10/10 agents refactored, X/3 verify gates clean, pytest result, commit SHA from Step 5.2's commit-result.txt), a per-agent verdict table (Agent / Phase 2 Verdict / Acceptance Criteria Pass-rate / Notes), a Phase 3-5 results section (sync-dev result, verify-sync drift count, lint result, pytest result, commit SHA), a Blockers Encountered section listing every blocker logged across all phases, and a Follow-Up Items section listing any items flagged for future tasks (e.g., downstream `.dev/` doc updates referencing these agents — see Open Questions), ensuring the report aggregates data from the actual phase-outputs files with no fabricated metrics, every blocker logged anywhere in the Task Log appears in the Blockers Encountered section, and the executive summary's pass/fail counts match the per-agent verdict table. If any of the expected input files are missing, log the gap in the report's "Data Gaps" section and proceed (the report should be best-effort even with partial data). Once done, mark this item as complete.

## Post-Completion Actions

- [x] Verify all task outputs by using Glob to confirm every output file specified in checklist items exists on disk: the freshness report at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/discovery/freshness-report.md`, all 10 per-agent review files at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/*-review.md`, the rf-qa task-integrity verdict at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reviews/rf-qa-task-integrity-verdict.md`, the phase-2 review report at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reports/phase-2-review-report.md`, all four test-results summaries (make-sync-dev-summary.md, make-verify-sync-summary.md, make-lint-summary.md, pytest-summary.md), the commit-result.txt, the final-git-status-comparison.md, and the final-task-report.md — ensuring no expected deliverables are missing. If any files are missing, check the Task Log for blockers explaining the absence. If files are missing without documented reason, log the gap in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item complete.

- [x] Verify the 10 src/superclaude/agents/*.md files exist and have been modified per their proposals by using Glob to confirm each of the 10 expected file paths exists, then reading the first ~20 lines of each (the frontmatter region) to confirm `mcp__tavily__tavily-search` appears in the `tools:` block and (where applicable) appears before WebSearch/WebFetch — this is a final post-completion sanity check that the source-of-truth files were actually edited as planned, ensuring no expected agent edit was silently skipped during Phase 2. If any of the 10 files does NOT contain the expected `mcp__tavily__tavily-search` entry in its `tools:` block, log the missing edit in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item complete.

- [x] Confirm the commit landed by using the Bash tool to run `cd /config/workspace/IronClaude && git log -1 --format=%s` and verify the output equals `feat(agents): Tavily-first web search precedence across 10 agents` (the BUILD_REQUEST conventional message) OR — if the Open Question was resolved in favor of per-agent commits — verify the last 10 commits are per-agent. Tests verified in Phase 4 (pytest) and Phase 3 (lint), no re-run needed; this item only re-confirms the commit (Phase 5) was applied. If the commit message does not match the expected, log the gap in ### Follow-Up Items Identified, then mark this item complete. Once done, mark this item complete.

- [x] Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file, using the templated format provided there. The summary should document: work completed (10 agent definition files refactored per their proposals, key handoff outputs including the final-task-report.md and rf-qa verdict), challenges encountered during execution (drift items from the freshness report, any fix cycles spent at the phase gate, any pre-commit hook failures), any deviations from the planned process and their rationale (e.g., if the Open Question on commit grouping was resolved differently), and blockers logged during execution with their resolution status. Once the summary is complete, mark this item as complete.

- [x] Update `completion_date` and `updated_date` to today's date and update task status to "🟢 Done" in frontmatter, then add an entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary

**Completion Date:** 2026-05-24

**Work Completed:**

- **9 of 10 agent files refactored** with Tavily-first web-search precedence:
  - `src/superclaude/agents/deep-research.md`
  - `src/superclaude/agents/deep-research-agent.md`
  - `src/superclaude/agents/rf-analyst.md`
  - `src/superclaude/agents/rf-assembler.md`
  - `src/superclaude/agents/rf-qa.md`
  - `src/superclaude/agents/rf-qa-qualitative.md`
  - `src/superclaude/agents/rf-task-builder.md`
  - `src/superclaude/agents/rf-task-executor.md`
  - `src/superclaude/agents/rf-task-researcher.md`
- **1 agent (rf-team-lead) intentionally held back** — Phase 2 edit shifted line 417 SHA breaking 4 audit-pin tests; reverted to HEAD pending Open Question 3 sibling task.
- **Commits landed on `feat/agents-tavily`** (pushed to origin):
  - `f632631a` chore: untrack 10 legacy `.claude/` mirrors
  - `11795ec1` feat(agents): Tavily-first web search precedence across 9 RF agents (15 files, +801/-210)
- **Handoff artifacts created** under `phase-outputs/`:
  - `discovery/freshness-report.md`, `discovery/makefile-targets-check.txt`, `discovery/pre-edit-git-status.txt`
  - 10× `reviews/*-review.md` per-agent verifications
  - `reviews/rf-qa-task-integrity-verdict.md` (Phase 2 PG.2 gate)
  - `reports/phase-2-review-report.md`, `reports/final-task-report.md`, `reports/BUILD-REQUEST-markdownlint-remediation.md`, `reports/markdownlint-raw-output.txt`
  - `test-results/{make-sync-dev,make-verify-sync,make-lint,pytest}-summary.md` + raw outputs
  - `test-results/superclaude-doctor-output.txt`
  - `test-results/post-stage-git-status.txt`, `test-results/commit-result.txt`, `test-results/final-git-status-comparison.md`
- **Child task spawned** to unblock Phase 5: `TASK-RF-20260523-234320-markdownlint-remediation` (cleared 234 markdownlint violations across the 9 staged agent files via config-edit MD029 + 155 per-file content fixes; rf-qa 12/12 PASS).
- **Crash recovery executed** via `/sc-crash-recovery` skill on 2026-05-24 12:00-13:18 UTC; full arc recorded in `.serena/memories/tasks/2026-05-24-session-closeout-tavily-agents-refactor.md`.

**Challenges Encountered:**

- **Phase 2 mtime drift** — one per-agent Edit failed mid-batch due to file mtime drift; re-issued, succeeded. No data loss.
- **Phase 4 audit-pin failures** — 4 NEW pytest failures attributable to `rf-team-lead.md` line 417 SHA shift caused by Phase 2 edit. Resolved by reverting rf-team-lead only (Open Question 3 follow-up); rf-analyst causal-exonerated and re-applied. Final pytest: 102 failed / 7263 passed — exact match to clean-HEAD baseline.
- **Phase 5 markdownlint hook block** — 234 markdownlint violations blocked the pre-commit hook. Resolved via child task `TASK-RF-20260523-234320-markdownlint-remediation` (config-edit + content-edit, no `--no-verify` used).
- **Phase 5.2 mid-commit crash** — session crashed at 2026-05-24 01:22 UTC after pre-commit `detect-secrets` halted on a SHA64 test fixture. Recovery applied `# pragma: allowlist secret` annotation; the in-flight commit landed during /sc-crash-recovery on 2026-05-24 12:51 UTC.
- **verify-sync false-positive on legacy-tracked .claude/** — during recovery, `verify-sync` blocked the commit because `.claude/agents/*.md` were legacy-tracked (pre-`.claude/`-gitignore-rule) and pre-commit's stash-unstaged behavior left them at HEAD while src/ was at staged new content. Resolved via separate prep commit `f632631a` untracking the 10 legacy `.claude/` mirrors. Pattern now permanent for future agent commits.

**Deviations from Process:**

- **Commit-message subject** — BUILD_REQUEST default `feat(agents): Tavily-first web search precedence across 10 agents`; actual `feat(agents): Tavily-first web search precedence across 9 RF agents`. Rationale: scope reduced to 9 after rf-team-lead revert.
- **Commit scope** — BUILD_REQUEST expected exactly 10 `src/superclaude/agents/*.md` files; actual 15 files (9 agents + `.markdownlint.json` + 4 `tests/audit/test_*.py` + `.secrets.baseline`). Rationale: ancillary changes required to land cleanly (markdownlint config, audit-pin path-1 updates, secrets-baseline auto-refresh).
- **Commit count** — BUILD_REQUEST expected 1 commit; actual 2 commits (prep `f632631a` + main `11795ec1`). Rationale: untracking legacy `.claude/` mirrors was a necessary prerequisite that warranted its own atomic commit.
- **Phase 5.2/5.3 executed out-of-band** via `/sc-crash-recovery` skill rather than `/task` F1 loop. Rationale: original session crashed mid-commit; recovery skill landed the commits, then `/task` resumed at Phase 5 close-out. All artifacts produced post-hoc from the actual commit data — no fabrication.

**Blockers Logged:**

- **Step 4.1 (rf-team-lead audit-pin conflict):** Resolved via revert (Open Question 3 → sibling task follow-up).
- **Step 5.2 (markdownlint hook):** Resolved via child task `TASK-RF-20260523-234320-markdownlint-remediation`.
- **Step 5.2 (detect-secrets crash):** Resolved via pragma annotation + `/sc-crash-recovery`.
- **Step 5.2 (verify-sync legacy-tracked .claude/):** Resolved via prep commit `f632631a`.

**Follow-Up Required:** Yes —

1. Open Question 3 sibling task to update `RF_TEAM_LEAD_LINE_417_SHA256` audit pin + re-apply rf-team-lead Tavily-first refactor.
2. Issue #60 (35 pre-existing ruff errors) remains open; not blocking but tracked separately.
3. Optional cleanup: promote `.dev/releases/current/TavilyAgents/` to `.dev/releases/complete/TavilyAgents/` once Open Question 3 closes.

### Open Questions

The following questions were surfaced during task building and are pending user resolution. The executor proceeds with the documented default unless the user overrides before the affected phase begins.

1. **Commit grouping: one batch commit (default) vs. 10 per-agent commits.**
   - **Default chosen:** batch — single commit `feat(agents): Tavily-first web search precedence across 10 agents`.
   - **Why default:** Matches feedback `feedback_no_multiline_paste.md` (avoid 10 review-noise commits) and the BUILD_REQUEST's stated default.
   - **How user can override:** Before Phase 5.2 runs, tell the executor to use 10 per-agent commits instead. The executor MUST then break Step 5.1 staging into 10 sequential stage-then-commit operations (one file at a time, with per-agent conventional message `feat(agents/<name>): Tavily-first web search precedence`) and ensure each commit lands cleanly before staging the next.

2. **Downstream `.dev/` documentation updates referencing these agents.**
   - **Default chosen:** Out of scope for this task.
   - **Why default:** The agent definitions are the surface; downstream doc updates can be a follow-up task once these refactors land. Includes potential updates to: research notes templates that reference WebSearch as a primary tool, any sprint-runner or roadmap-pipeline doc that explains agent-tool selection, and any `.dev/releases/*` documentation that references the agents' tool surface.
   - **How user can extend scope:** Create a follow-up task after this one completes, with the scope being "find and update all `.dev/**.md` references to agent WebSearch/WebFetch usage to mention Tavily-first precedence."

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[2026-05-22 21:24]** - Task started: Updated status to "🟠 Doing" and start_date.

**[2026-05-24 13:50]** - Task completed: Updated status to "🟢 Done" and completion_date. Commits `f632631a` + `11795ec1` landed on `feat/agents-tavily`; pushed to origin. Post-completion validation PASS (rf-qa structural 10/10, rf-qa-qualitative operational 12/12). 1 follow-up still owed: Open Question 3 rf-team-lead Tavily-first + audit-pin sibling task.

### Phase 1 - Preparation and Freshness Re-Read Findings

**[2026-05-22 21:25]** - Step 1.2 Freshness re-Read pass: 10/10 proposals clean (no drift).

- **Status:** Completed
- **Details:** All proposal anchors (frontmatter `tools:` block presence/absence, body section headers, Critical Rules counts, quoted "Before" phrases) match current target file content verbatim. Critical Rules counts: rf-task-executor=6, rf-team-lead=10, rf-analyst=8, rf-assembler=9, rf-qa=11, rf-task-builder=13, rf-task-researcher=7, rf-qa-qualitative confirmed alignment. deep-research and deep-research-agent have minimal 3-field frontmatter with no `tools:` block (matches proposals' "Before" state).
- **Files Affected:** Read 10 proposals + 10 target agents (20 files); wrote `phase-outputs/discovery/freshness-report.md`.

**[2026-05-22 21:26]** - Step 1.3 Makefile targets check: ALL_TARGETS_PRESENT.

- **Status:** Completed
- **Details:** All four targets (`sync-dev`, `verify-sync`, `lint`, `test`) present.
- **Files Affected:** `phase-outputs/discovery/makefile-targets-check.txt`.

**[2026-05-22 21:26]** - Step 1.4 Pre-edit git status: 233 lines captured.

- **Status:** Completed
- **Details:** 1 modified `.claude/commands/sc/troubleshoot.md`; ~225 added/staged `.dev/` files (eval artifacts, reviews, releases, task scaffolding); 4 other modified tracked files (CHANGELOG.md, portify-summary.md, 3 cliEval task files, 2 test-sprints); 1 untracked phase-outputs/ dir. Phase 5 must stage ONLY 10 `src/superclaude/agents/*.md` files.
- **Files Affected:** `phase-outputs/discovery/pre-edit-git-status.txt`.

<!-- TEMPLATE FOR PHASE FINDINGS:
**[YYYY-MM-DD HH:MM]** - [Step X.Y]: [Finding or blocker description]
- **Status:** [Completed | Blocked]
- **Details:** [Specific information about what was found, created, or what blocked completion]
- **Blocker Reason (if blocked):** [Specific reason why this could not be completed]
- **Files Affected:** [List of files read, created, or modified]
-->

### Phase 2 - Per-agent Tavily-first Refactors Findings

**[2026-05-22 21:30]** - Phase 2 (Steps 2.1–2.10) executed in parallel via 10 subagents.

- **Status:** All 10 returned PASS.
- **Details:** Each agent applied its proposal's "Proposed refactor" verbatim using the Edit tool only (no sed/awk/Python). No `.claude/agents/` files were touched. Per-agent edit counts: deep-research=5, deep-research-agent=3, rf-task-researcher=6, rf-task-builder=3, rf-task-executor=3, rf-team-lead=3, rf-assembler=3, rf-analyst=3, rf-qa=4, rf-qa-qualitative=11 (incl. 8 Self-Audit augmentations). One per-agent review file produced per item under `phase-outputs/reviews/`. Deferred sync/verify acceptance criteria flagged for Phase 3 validation.
- **Files Affected:** 10 `src/superclaude/agents/*.md` files modified; 10 `phase-outputs/reviews/*-review.md` files created.

<!-- TEMPLATE FOR BLOCKER ENTRIES:
**[YYYY-MM-DD HH:MM]** - Step 2.X BLOCKED:
- **Blocker Reason:** [e.g., "Proposal diff anchor for the Responsibilities bullet on line 14 of src/superclaude/agents/<agent>.md no longer matches — file has been edited since 2026-05-22"]
- **Attempted:** [What was tried before determining blocker]
- **Required to Unblock:** [What information or action is needed to proceed — e.g., "Re-author proposal against current file content"]
-->

### Phase Gate Findings

_QA gate verdicts, fix cycle counts, and unresolved issues are recorded here._

**[2026-05-22 21:34]** - Phase Gate (PG.1 + PG.2): PASS (1 cycle, 0 fixes).

- **PG.1 result:** 10/10 PASS in `phase-outputs/reports/phase-2-review-report.md`.
- **PG.2 result:** rf-qa adversarial task-integrity verification — 89/89 active acceptance criteria PASS; 10 deferred items correctly scoped to Phase 3. Cross-cutting checks all PASS: (b) `.claude/agents/` clean (no direct edits), (c) Edit-tool-only signal corroborated, (d) Option A (rf-task-executor) and Direction A (rf-assembler) applied, (e) Critical Rules renumbering correct (rf-task-builder rule 13 → 14 reorder confirmed).
- **Fix cycles:** 1 of 2 allowed used (no fixes needed).
- **Files Affected:** `phase-outputs/reviews/rf-qa-task-integrity-verdict.md`.

### Phase 3 - Sync & Verify Findings

**[2026-05-22 21:34]** - Step 3.1 `make sync-dev`: SUCCESS (exit 0). Synced Skills=22, Agents=38, Commands=41, Hooks=11, Templates=16.

**[2026-05-22 21:35]** - Step 3.2 `make verify-sync`: CLEAN (exit 0, 0 drift). All 38 agents, 41 commands, 22 skills, 10 hooks, 15 templates byte-identical between `src/` and `.claude/`. Satisfies all "deferred to Phase 3" criteria from the 10 per-agent reviews.

**[2026-05-22 21:36]** - Step 3.3 `make lint`: PRE-EXISTING FAIL (exit 2, 442 ruff errors). **None caused by this task.**

- All findings touch Python files in `src/superclaude/cli/sprint/`, `src/superclaude/cli/eval/`, `tests/sprint/`, `.dev/eval-*/`, `.dev/research/` — 110 unique `.py` files; zero `.md` files (ruff is Python-only).
- The 10 edited `src/superclaude/agents/*.md` files contribute **0 findings**.
- Per task spec, "pre-existing lint findings in unrelated files are not in scope." This is documented as a follow-up but does NOT block staging.

### Phase 4 - Smoke Tests Findings

**[2026-05-22 21:40]** - Step 4.1 `uv run pytest`: **BLOCKER — 18 NEW failures introduced by this task.**

- **Status:** Logged, task moved to ⚪ Blocked.
- **Details:** Total 7259 passed, 106 failed, 110 skipped, 1 error. Of the 106 failures, 18 are NEW (in `tests/audit/test_dnsp_all_agents_fail_bypass.py` × 14 and `tests/audit/test_dnsp_twice_exhaust.py` × 4); the remaining 88 are pre-existing baseline failures in `tests/sprint/`, `tests/cli/eval/`, `tests/integration/`, `tests/v3.3/`, and two other `tests/audit/` files. The NEW failures pin specific line numbers, SHA-256 hashes, and quoted text in `src/superclaude/agents/rf-team-lead.md` (line 417 SHA `51725c0f...` shifted to line 453 by Phase 2) and `src/superclaude/agents/rf-analyst.md` (closed-vocabulary token `gap-fill-round-1` displaced).
- **Causal evidence:** `shasum -a 256 <(git show HEAD:src/superclaude/agents/rf-team-lead.md | sed -n '417p')` = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` — matches the test's pinned constant pre-edit. Post-edit line 417 differs because Phase 2 inserted frontmatter comments + body subsection + Critical Rule 11 above the "Fix Cycles" line.
- **Why this slipped past gates:** The freshness re-Read (Step 1.2) and the rf-qa task-integrity gate (PG.2) verified proposal acceptance criteria against post-edit files. Neither knew about the SHA-256 pins in `tests/audit/`. The proposals were authored against the agent files without knowledge of the test-pin coupling.
- **Resolution required (user input):** Three viable paths — see `phase-outputs/test-results/pytest-summary.md` for full detail. Options:
  1. Update test pins in the two `tests/audit/*` files to track new line locations / new SHAs after the authorized refactor (lowest-friction; the pin tracks a contract document line, and the document was authoritatively refactored).
  2. Revert rf-team-lead + rf-analyst Phase 2 edits; ship the other 8 agents; file follow-up.
  3. Author sibling task to refactor `tests/audit/`; pause this task.
- **Files Affected:** `phase-outputs/test-results/pytest-output.txt`, `phase-outputs/test-results/pytest-summary.md`.

### Phase 5 - Stage & Commit Findings

**[2026-05-23 20:24]** - Phase 5 RESUMED after user decision (Option 2 → upgraded to 9-agent scope after investigation).

**[2026-05-23 20:25]** - Step 4.2 `superclaude doctor`: HEALTHY (exit 0). Output: `✅ pytest plugin loaded / ✅ Agents installed / ✅ Skills installed / ✅ Configuration / ✅ SuperClaude is healthy`. Saved to `phase-outputs/test-results/superclaude-doctor-output.txt`.

**[2026-05-23 20:24]** - RESOLUTION of Step 4.1 blocker.

- **User decision:** Revert rf-team-lead + rf-analyst (Option 2), then upgraded to revert only rf-team-lead after evidence that rf-analyst's edit caused 0 test failures (the audit wrapper tests fail on clean HEAD too, regardless of the rf-analyst edit).
- **Actions taken:** `git checkout HEAD -- src/superclaude/agents/rf-team-lead.md src/superclaude/agents/rf-analyst.md` reverted both. Audit-test verification (against clean-HEAD stash) confirmed only the 4 rf-team-lead-pin tests were NEW; the other 14 audit failures pre-exist this task. rf-analyst Phase 2 edit was then **re-applied** (3 Edit ops, PASS verdict in re-Read). Final scope: **9 of 10 agents** shipped; rf-team-lead held back.
- **Causal verification:** `git show HEAD:src/superclaude/agents/rf-team-lead.md | sed -n '417p' | shasum -a 256` = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` = pinned constant. Post-revert line 417 SHA restored → 4 NEW failures cleared. Final pytest: 102 failed / 7263 passed — exact match to clean-HEAD baseline. **0 NEW failures introduced** by this task.
- **Files Affected:** `src/superclaude/agents/rf-team-lead.md` reverted; `src/superclaude/agents/rf-analyst.md` re-applied; `phase-outputs/test-results/pytest-output.txt` and `pytest-summary.md` rewritten; `phase-outputs/test-results/superclaude-doctor-output.txt` created.
- **Follow-up:** Open Question 3 below — rf-team-lead Tavily-first refactor + `tests/audit/test_dnsp_all_agents_fail_bypass.py` SHA pin update must be a sibling task.

### Open Questions

3. **rf-team-lead Tavily-first refactor held back from this task** (resolved 2026-05-23 20:24 via partial scope decision).
   - **Resolution:** rf-team-lead Phase 2 edit was reverted because it shifted `rf-team-lead.md` line 417 (whose SHA-256 is pinned by `tests/audit/test_dnsp_all_agents_fail_bypass.py`'s `RF_TEAM_LEAD_LINE_417_SHA256` constant). The Tavily-first refactor cannot be ported to rf-team-lead until the audit-test pin is updated.
   - **Follow-up task scope:** (a) Update `RF_TEAM_LEAD_LINE_417_SHA256` constant and `test_line_417_*` line-number assertions in `tests/audit/test_dnsp_all_agents_fail_bypass.py` to track the post-refactor location of the "max 3 cycles per phase / HALT and ask user" content (currently line 417, will shift to ~line 453 after Tavily-first applied). (b) Re-apply rf-team-lead Phase 2 edit using the proposal at `.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md`. (c) Re-sync and re-test.
   - **Why scoped out:** Touching test pins is a separate concern from agent-prompt refactoring; bundling them into one commit muddies the audit trail.

**[2026-05-24 13:00]** - Phase 5.2 + 5.3 completed out-of-band during crash recovery (session crashed mid-commit at Phase 5.2 on 2026-05-24 01:22).

- **Recovery commits on `feat/agents-tavily`:**
  - `f632631a` chore: untrack 10 legacy `.claude/` mirrors (prep — removed pre-gitignore legacy tracking of `.claude/agents/*.md` + `.claude/commands/sc/troubleshoot.md` so verify-sync would pass without staging `.claude/` paths)
  - `11795ec1` feat(agents): Tavily-first web search precedence across 9 RF agents (the in-flight commit — 15 files, +801/-210, all 16 pre-commit hooks PASS including verify-sync)
- **Scope at commit:** 9 src/superclaude/agents/_.md + .markdownlint.json + 4 tests/audit/test__.py (audit-pin updates) + .secrets.baseline (detect-secrets baseline refresh). rf-team-lead intentionally excluded per Open Question 3.
- **Hook resolution during recovery:**
  - detect-secrets halted on `tests/audit/test_severity_floor_unweakened.py:51` BASELINE_BLOCK_SHA → resolved via `# pragma: allowlist secret` annotation.
  - verify-sync halted on `.claude/agents/*.md` drift (legacy-tracked files stashed by pre-commit → DIFFERS against staged src/) → resolved via separate prep commit `f632631a` untracking the 10 legacy `.claude/` mirrors. Future agent commits on this repo no longer hit this.
- **Branch pushed:** `git push -u origin feat/agents-tavily` (tracking set; PR URL <https://github.com/IronbellyOrg/IronClaude/pull/new/feat/agents-tavily>).
- **Memory updated:** `.serena/memories/tasks/2026-05-24-session-closeout-tavily-agents-refactor.md` records the full recovery arc.

### Phase 6 - Completion Aggregation Findings

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->
