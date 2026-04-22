# BUILD_REQUEST Template

> Loaded by the orchestrator during A.7 and passed as the subagent prompt to `rf-task-builder`.

---

BUILD_REQUEST:
==============
GOAL: Create a comprehensive Product Requirements Document (PRD) for [GOAL] following the project template at docs/docs-product/templates/prd_template.md. The PRD will be written to [OUTPUT_PATH].

WHY: [WHY — what this PRD is for and how it will be used]

TASK_ID_PREFIX: TASK-PRD

TEMPLATE: [01 or 02 — skill selects:
  01 = simple PRD update, straightforward execution
  02 = needs discovery, parallel research, web research, synthesis, quality gates, assembly]

PRD_SCOPE: [Product PRD / Feature PRD]
If Feature PRD, the following sections are affected:
- S2 Problem Statement: Do NOT include a "Market Opportunity" subsection with TAM/SAM/SOM.
  Instead include "Why This Feature is Required" explaining criticality to the platform.
  Reference Platform PRD for market context.
- S3 Background & Strategic Fit: Focus on why THIS FEATURE is needed now (what enablers
  exist, what dependencies are ready, what bets it makes). Do NOT repeat platform-level
  market trends, company revenue projections, or competitive moat. Reference Platform PRD.
- S5 Business Context: Skip market sizing, revenue projections, and KPI tables. Include
  business justification (why this feature matters, cost drivers, strategic value) and a
  forward reference to S19 for all KPIs. Do NOT duplicate metrics here — S19 is the
  single source of truth for KPIs.
- S8 Value Proposition Canvas: N/A — reference Platform PRD.
- S9 Competitive Analysis: N/A unless the feature competes directly with a standalone
  product category. Reference Platform PRD.
- S16 User Experience Requirements: Include only feature-specific user flows (S16.2).
  Onboarding (S16.1), accessibility (S16.3), and localization (S16.4) are platform-level
  concerns — mark N/A and reference Platform PRD.
- S17 Legal & Compliance: Include only feature-specific data handling requirements.
  Reference Platform PRD for SOC 2, GDPR, CCPA, EU AI Act.
- S18 Business Requirements: N/A — feature has no independent pricing or GTM.
  Include brief note on feature-specific cost drivers only.
Synthesis agents MUST check this field and skip platform-level content for Feature PRDs.
Do NOT hardcode specific person names (Product Owner, Engineering Lead, etc.) — use TBD.

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference product capabilities marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 1 (Preparation): Update task status, confirm scope from research notes, read the template, select depth tier, create task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to ${TASK_DIR}research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn rf-analyst (completeness-verification) then rf-qa (research-gate) as parallel quality gate. Both write reports. QA verdict gates progression.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources (market data, competitive landscape, industry trends) and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce PRD template sections. Then spawn rf-analyst (synthesis-review) and rf-qa (synthesis-gate) as parallel quality gate. QA can fix issues in-place.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final PRD, then spawn rf-qa (report-validation) for structural quality check, then spawn rf-qa-qualitative (prd-qualitative) for content/scope/logic quality check. Both QA agents have in-place fix authorization.
- Phase 7 (Present to User & Complete Task): ANTI-ORPHANING — task-completion items are WITHIN this phase, not in a separate Post-Completion section.

RESEARCH NOTES FILE:
${TASK_DIR}research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments, synthesis mapping, and output paths.

SKILL CONTEXT FILES:
- `refs/agent-prompts.md` — Read for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt, Research Analyst Agent Prompt, Research QA Agent Prompt, Synthesis QA Agent Prompt, Report Validation QA Agent Prompt, Assembly Agent Prompt. These must be embedded in the relevant checklist items per B2 self-contained pattern.
- `refs/synthesis-mapping.md` — Read for: the standard synth-file-to-PRD-section mapping and the PRD output structure/skeleton.
- `refs/validation-checklists.md` — Read for: Synthesis Quality Review Checklist (post-synthesis verification), Assembly Process (PRD assembly steps), Validation Checklist (Phase 6 validation criteria), Content Rules (writing standards). These must be embedded in the relevant checklist items per B2 self-contained pattern.
Read the "Tier Selection" section from SKILL.md for depth tier line budgets and agent counts.

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process
Structure), you MUST create individual checklist items for EVERY research agent,
web research topic, synthesis file, and validation step. Do NOT create batch items
like "spawn all 5 research agents" or "run all web research" — each agent gets
its own checklist item. The research notes SUGGESTED_PHASES section contains
per-agent detail specifically to enable this granularity.

TO BUILD A GOOD TASK FILE, YOU NEED:
- Goal and outputs (what to create, where, what format)
- Source files and context (what exists, what to reference) — from the research notes
- Phases and steps (logical breakdown of the work) — from the research notes SUGGESTED_PHASES + SKILL.md phase definitions
- Verification criteria (how to know each step is done)
- Dependencies (what's needed before each step)
The research notes file should cover most of this.

ESCALATION:
Since you are running as a subagent (not a teammate), you have NO team context.
Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
will fail because there is no team. This overrides your agent definition's
Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
Instead, return the task file path as your final output.
- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
- **External docs/syntax** → use WebSearch
- **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.

SKILL PHASES TO ENCODE IN TASK FILE:
The task file MUST encode these phases as sequential checklist items. Each phase maps to a section of the skill's workflow. All items MUST follow the B2 self-contained pattern from the MDTM template.

Phase 1 — Preparation:
- Update task status to "🟠 Doing"
- Confirm scope from research notes (product boundaries, key directories, tier selection)
- Read the PRD template at docs/docs-product/templates/prd_template.md
- Select depth tier (Lightweight / Standard / Heavyweight) based on product scope and complexity
- Create the task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders (if not already created during scope discovery)

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from refs/agent-prompts.md
- Each item specifies: investigation topic, type (Feature Analyst / Doc Analyst / Integration Mapper / UX Investigator / Architecture Analyst), files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from refs/agent-prompts.md) in each checklist item per B2
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 6 research assignments: spawn all 6 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.
- Agent count follows tier guidance: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+

Phase 3 — Research Completeness Verification (ANALYST + QA GATE, PARALLEL):
- Spawn `rf-analyst` (subagent_type: "rf-analyst", analysis_type: "completeness-verification") AND `rf-qa` (subagent_type: "rf-qa", qa_phase: "research-gate") IN PARALLEL. Both agents independently read research files and apply their own checklists. The analyst writes to `${TASK_DIR}qa/analyst-completeness-report.md`. The QA agent writes to `${TASK_DIR}qa/qa-research-gate-report.md`. Embed full prompts from respective agent definitions in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst instances and MULTIPLE QA instances in parallel, each with an `assigned_files` subset. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. Each partition instance writes to a numbered report (e.g., `${TASK_DIR}qa/analyst-completeness-report-1.md`). After all instances complete, merge their reports.
- Read ALL reports. Determine verdict from QA report(s) (PASS / FAIL).
- If PASS → proceed to Phase 4. If FAIL → fix ALL findings regardless of severity before proceeding. Spawn additional targeted research agents (one item per gap-filling agent).
- After gap-filling, spawn `rf-qa` with qa_phase: "fix-cycle". Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present findings to user.
- Compile final gaps into ${TASK_DIR}gaps-and-questions.md
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from refs/agent-prompts.md
- Each item specifies: topic, context from codebase findings, output file path
- Web research targets should include (as applicable): competitive landscape analysis, TAM/SAM/SOM market data, industry standards and compliance requirements, technology trend reports, user research findings, pricing model analysis
- Agent count follows tier guidance: Lightweight 0-1, Standard 1-2, Heavyweight 2-4

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (from Synthesis Mapping Table in refs/synthesis-mapping.md)
- Each item spawns an Agent subagent with the synthesis agent prompt from refs/agent-prompts.md
- Each item specifies: research files to read, template sections to produce, output path
- After ALL synthesis agents complete, spawn `rf-analyst` (analysis_type: "synthesis-review") AND `rf-qa` (qa_phase: "synthesis-gate", fix_authorization: true) IN PARALLEL. The analyst writes to `${TASK_DIR}qa/analyst-synthesis-review.md`. The QA agent writes to `${TASK_DIR}qa/qa-synthesis-gate-report.md`. Embed full prompts in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >4 synthesis files exist, spawn multiple analyst and QA instances with `assigned_files` subsets. The threshold is lower than Phase 3 (>4 vs >6) because synthesis QA requires deeper per-file analysis (tracing claims back to research files, verifying cross-section consistency). Same partitioning pattern as Phase 3. Each partition instance writes to a numbered report. Orchestrator merges all partition reports after completion.
- If FAIL → re-run affected synthesis agents, then re-spawn `rf-qa` (fix-cycle). Maximum 2 fix cycles for synthesis — after 2 failed cycles, HALT and present to user.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + Structural QA + Qualitative QA):
- Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") to assemble the final PRD. Hand it: the list of synth file paths in order, the PRD output path, the PRD template structure from refs/synthesis-mapping.md, the Assembly Process steps from refs/validation-checklists.md, and the Content Rules from refs/validation-checklists.md. The assembler reads each synth file and writes the PRD incrementally section by section. The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole document. Embed the full assembler prompt in the checklist item per B2.
- After the assembler returns, spawn `rf-qa` (qa_phase: "report-validation", fix_authorization: true). The QA agent validates the assembled PRD against the Validation Checklist from refs/validation-checklists.md (structural/semantic checks: section numbers, cross-references, evidence citations, template conformance). The QA agent writes to `${TASK_DIR}qa/qa-report-validation.md`. Embed the full QA prompt in the checklist item per B2.
- Read the structural QA report. If issues remain unfixed, address them before proceeding to qualitative QA.
- After structural QA passes, spawn `rf-qa-qualitative` (subagent_type: "rf-qa-qualitative", qa_phase: "prd-qualitative", fix_authorization: true). The qualitative QA agent reads the entire PRD and verifies it makes sense from product and engineering perspectives: correct scoping (feature vs platform content), logical flow, realistic requirements, no contradictions, no red flags, appropriate audience. It applies the 23-item PRD Qualitative Review checklist from its agent definition. The agent writes to `${TASK_DIR}qa/qa-qualitative-review.md`. Embed the full qualitative QA prompt (including document type: Product PRD or Feature PRD, template path, and output path) in the checklist item per B2.
- Read the qualitative QA report. If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly by re-reading the affected sections. If issues remain unfixed, address ALL of them before proceeding to Phase 7. Zero leniency — no severity level is exempt.

Phase 7 — Present to User & Complete Task:
- Present summary to user (PRD location, line count, tier classification, sections populated vs skipped, research/synth artifact locations, gaps needing manual review)
- Ask about downstream documents: "This PRD can feed directly into a Technical Design Document. Would you like me to create a TDD using the `/tdd` skill? The research files are already in place." If yes, invoke the `tdd` skill with the PRD as input.
- If the PRD was created by consolidating existing docs, present source docs to user and ask about archiving (Step 11 from refs/validation-checklists.md)
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date

TASK FILE LOCATION: .dev/tasks/to-do/TASK-PRD-[YYYYMMDD]-[HHMMSS]/TASK-PRD-[YYYYMMDD]-[HHMMSS].md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL CONTEXT FILES specified above for agent prompts, PRD template structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .gfdoc/templates/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .gfdoc/templates/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-PRD-[YYYYMMDD-HHMMSS]/TASK-PRD-[YYYYMMDD-HHMMSS].md using PART 2 structure
7. Return the task file path
