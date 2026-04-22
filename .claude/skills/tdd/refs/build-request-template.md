# BUILD_REQUEST Template

> Loaded by the orchestrator during A.7 and passed as the subagent prompt to `rf-task-builder`.

---

BUILD_REQUEST:
==============
GOAL: Create a comprehensive Technical Design Document (TDD) for [COMPONENT] by researching the actual codebase, synthesizing findings into template-aligned sections, and assembling the final document. The TDD will be written to [OUTPUT_PATH].

WHY: [WHY — what prompted this TDD and what the design document will be used for]

PRD_REF: [path to PRD, or "None"]

TASK_ID_PREFIX: TASK-TDD

TEMPLATE: [01 or 02 — skill selects:
  01 = simple file creation, straightforward execution
  02 = needs discovery, testing, review, conditional flows, or aggregation]

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 1 (Preparation): Update task status, confirm scope from research notes, read the TDD template, select depth tier, create task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to ${TASK_DIR}research/. If PRD provided, first item extracts PRD context to ${TASK_DIR}research/00-prd-extraction.md.
- Phase 3 (Completeness Verification): L4 Review/QA — spawn rf-analyst (completeness-verification) AND rf-qa (research-gate) IN PARALLEL. Both write reports. QA verdict gates progression.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce template-aligned sections. Then spawn rf-analyst (synthesis-review) AND rf-qa (synthesis-gate, fix_authorization: true) IN PARALLEL. QA can fix issues in-place.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final TDD, then spawn rf-qa (report-validation) for structural quality check, then spawn rf-qa-qualitative (tdd-qualitative) for content/logic quality check. Both QA agents have in-place fix authorization.
- Phase 7 (Present to User & Complete Task): ANTI-ORPHANING — task-completion items are WITHIN this phase, not in a separate Post-Completion section.

RESEARCH NOTES FILE:
${TASK_DIR}research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, PRD context, planned investigation assignments, synthesis mapping, and output paths.

SKILL CONTEXT FILES:
- `refs/agent-prompts.md` — Read for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt, Research Analyst Agent Prompt, Research QA Agent Prompt, Synthesis QA Agent Prompt, Report Validation QA Agent Prompt, Assembly Agent Prompt. These must be embedded in the relevant checklist items per B2 self-contained pattern.
- `refs/synthesis-mapping.md` — Read for: the standard synth-file-to-TDD-section mapping and the TDD output structure/skeleton.
- `refs/validation-checklists.md` — Read for: Synthesis Quality Review Checklist (post-synthesis verification), Assembly Process (TDD assembly steps), Validation Checklist (Phase 6 validation criteria), Content Rules (writing standards). These must be embedded in the relevant checklist items per B2 self-contained pattern.
- `refs/operational-guidance.md` — Read for: Critical Rules, Research Quality Signals, Artifact Locations, PRD-to-TDD pipeline, and Session Management guidance.
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
- Confirm scope from research notes (component boundaries, key directories, tier selection)
- Read the TDD template at src/superclaude/examples/tdd_template.md
- Select depth tier (Lightweight / Standard / Heavyweight) based on component count and complexity
- Create the task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders (if not already created during scope discovery)

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- If PRD provided: first item extracts PRD context to ${TASK_DIR}research/00-prd-extraction.md
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from refs/agent-prompts.md
- Each item specifies: investigation topic, type (Architecture Analyst / Code Tracer / Data Model Analyst / API Surface Mapper / Integration Mapper / Doc Analyst), files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from refs/agent-prompts.md) in each checklist item per B2
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 6 research assignments: spawn all 6 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.
- Agent count follows tier guidance: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+

Phase 3 — Research Completeness Verification (ANALYST + QA GATE, PARALLEL):
- Spawn `rf-analyst` (subagent_type: "rf-analyst", analysis_type: "completeness-verification") AND `rf-qa` (subagent_type: "rf-qa", qa_phase: "research-gate") IN PARALLEL. Both agents independently read research files and apply their own checklists. The analyst applies its 8-item completeness checklist (coverage audit, evidence quality, doc staleness, completeness, cross-references, contradictions, gap compilation, depth assessment). The QA agent applies its 10-item research-gate checklist (file inventory, evidence density, scope coverage, doc cross-validation, contradiction resolution, gap severity, depth appropriateness, integration points, pattern documentation, incremental writing compliance). The analyst writes to `${TASK_DIR}qa/analyst-completeness-report.md`. The QA agent writes to `${TASK_DIR}qa/qa-research-gate-report.md`. Embed full prompts from respective agent definitions in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst + QA instances with assigned_files subsets. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. Each partition instance writes to a numbered report (e.g., `${TASK_DIR}qa/analyst-completeness-report-1.md`). After all instances complete, merge reports: union of findings, take the more severe rating for any item flagged by multiple partitions, deduplicate gaps.
- Read ALL reports (or merged report). Determine verdict from QA report(s) (PASS / FAIL), cross-referenced with analyst findings.
- If PASS → proceed to Phase 4. If FAIL → fix ALL findings regardless of severity before proceeding. Spawn targeted gap-filling agents, then rf-qa fix-cycle.
- Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed. Do NOT continue to Phase 4 without user approval.
- Compile final gaps into ${TASK_DIR}gaps-and-questions.md
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from refs/agent-prompts.md
- Each item specifies: topic, context from codebase findings, output file path
- Web research is optional — only spawn when codebase research reveals gaps requiring external documentation
- Agent count follows tier guidance: Lightweight 0-1, Standard 1-2, Heavyweight 2-4

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (from Synthesis Mapping Table in refs/synthesis-mapping.md)
- Each item spawns an Agent subagent with the synthesis agent prompt from refs/agent-prompts.md
- Each item specifies: research files to read, template sections to produce, output path
- After ALL synthesis agents complete, spawn `rf-analyst` (analysis_type: "synthesis-review") AND `rf-qa` (qa_phase: "synthesis-gate", fix_authorization: true) IN PARALLEL. The analyst writes to `${TASK_DIR}qa/analyst-synthesis-review.md`. The QA agent writes to `${TASK_DIR}qa/qa-synthesis-gate-report.md`. Embed full prompts in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >4 synthesis files exist, spawn multiple analyst and QA instances with `assigned_files` subsets. The threshold is lower than Phase 3 (>4 vs >6) because synthesis QA requires deeper per-file analysis (tracing claims back to research files, verifying cross-section consistency). Same partitioning pattern as Phase 3. Each partition instance writes to a numbered report. Orchestrator merges all partition reports after completion.
- If FAIL → re-run affected synthesis agents, then re-spawn `rf-qa` (fix-cycle). Maximum 2 fix cycles for synthesis — after 2 failed cycles, HALT and present to user.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + Structural QA + Qualitative QA):
- Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") — NOT a general-purpose Agent — to assemble the final TDD. Hand it: the list of synth file paths in order (as component_files), the TDD output path `docs/[domain]/TDD_[COMPONENT-NAME].md`, the TDD template reference `src/superclaude/examples/tdd_template.md` (as output_format), the Assembly Process steps from refs/validation-checklists.md (as assembly_rules), and the Content Rules from refs/validation-checklists.md (as content_rules). The assembler reads each synth file and writes the TDD incrementally section by section — frontmatter first, then sections in template order, then Table of Contents, then cross-checks internal consistency (requirements in Section 5 trace to architecture in Section 6, risks in Section 20 have mitigations, Open Questions in Section 22 not answered elsewhere, Dependencies in Section 18 complete). The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole document. Embed the full assembler prompt from refs/agent-prompts.md in the checklist item per B2.
- After the assembler returns the TDD path, spawn `rf-qa` (subagent_type: "rf-qa", qa_phase: "report-validation", fix_authorization: true). The QA agent validates the assembled TDD against the 15-item Validation Checklist + 4 Content Quality Checks from refs/validation-checklists.md (structural/semantic checks: section numbers, cross-references, evidence citations, template conformance). The QA agent is authorized to fix issues in-place and writes its report to `${TASK_DIR}qa/qa-report-validation.md`. Embed the full QA prompt in the checklist item per B2.
- Read the structural QA report. If issues remain unfixed, address them before proceeding to qualitative QA.
- After structural QA passes, spawn `rf-qa-qualitative` (subagent_type: "rf-qa-qualitative", qa_phase: "tdd-qualitative", fix_authorization: true). The qualitative QA agent reads the entire TDD and verifies it makes sense from product and engineering perspectives: architecture decisions match PRD requirements, API contracts are internally consistent, implementation details are specific enough to code from, no PRD content repeated verbatim, data models match across diagrams/contracts/migrations, no requirements invented that aren't in the PRD. The agent writes to `${TASK_DIR}qa/qa-qualitative-review.md`. Embed the full qualitative QA prompt (including document_type: "Technical Design Document", template path, and output path) in the checklist item per B2.
- Read the qualitative QA report. If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly by re-reading the affected sections. If issues remain unfixed, address ALL of them before proceeding to Phase 7. Zero leniency — no severity level is exempt.

Phase 7 — Present to User & Complete Task (ANTI-ORPHANING):
- Present summary to user (TDD location, line count, tier, sections populated vs skipped, research artifacts location, gaps)
- Ask about cleanup of consolidation sources (if applicable)
- Suggest downstream workflow: "This TDD can feed directly into implementation task files. Would you like me to create implementation tasks using the `/task` skill? The research files and design specifications are already in place." If yes, invoke the task skill with the TDD as context.
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date

TASK FILE LOCATION: .dev/tasks/to-do/TASK-TDD-[YYYYMMDD]-[HHMMSS]/TASK-TDD-[YYYYMMDD]-[HHMMSS].md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL CONTEXT FILES specified above for agent prompts, TDD template structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-TDD-[YYYYMMDD-HHMMSS]/TASK-TDD-[YYYYMMDD-HHMMSS].md using PART 2 structure
7. Return the task file path
