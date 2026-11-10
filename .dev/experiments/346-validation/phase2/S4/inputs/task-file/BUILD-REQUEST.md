# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation of how a Coder workspace user can get BMAD (BMAD-METHOD 6.9.0) to create the directories it needs the first time it is used in a project that never had it, WITHOUT a global BMAD install and without reversing the unrelated 2026-09-25 owner decision OD-1 (BMad is installed per project). Examine: real BMAD 6.9.0 installer and skill behaviour; the image-wide `bmad` CLI (templates/VSCode-AIDev02/image/Dockerfile.coder:133-144); whether bmad can install skills at user scope (prior report said UNVERIFIED); the user-level hook and skill options in Claude Code; the catalogue bmad install.sh and manifest.yaml; startup.sh; and the tests that pin "no seed means BMAD writes nothing" (.github/contract-tests/test-57-catalogue-configure.sh, test-startup-boot.sh). Produce a structured research report with findings, gap analysis, options with effort and risk, a recommendation, and an implementation plan that names every pinned test and document that must change. The report will be written to `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md`.

WHY: On 2026-11-07 the user decided (AskUserQuestion) that BMAD SHOULD create its needed directories on first use in a project that never had it. This supersedes, for first-use creation only, the 2026-09-25 owner decision OD-1 and related non-goals (_bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md:77, owner-decisions.md:5, .memlog.md:32-33, spec-orca-catalogue-bundle/SPEC.md:141,174). Global installation of BMAD is NOT requested. The findings feed (1) `.dev/issues/478/spec.md` (written by the orchestrator after this research) and (2) `/sc:workflow` to produce an implementation plan. Prior diagnosis: `.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/REPORT.md` (Ponytail: the user confirmed on 2026-11-07 it already installs and works; there is NO Ponytail work, do not research it). If the evidence shows the ask is not feasible without a global BMAD install or a change in another repo (IronClaude or IronOrca), the report must say that plainly in Section 7 and Section 9 so the orchestrator can STOP and re-scope.

TASK_ID_PREFIX: TASK-RESEARCH

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
None found during scope discovery beyond the prior report's own caveat that documentation currency was not checked ("every documentation file except the directly read owner decisions has verdict unknown"). Phase 2 agents will perform full documentation cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags. Known UNVERIFIED items to resolve: whether bmad 6.9.0 has any consumer of `global_target_dir` in platform-codes.yaml (scope discovery Grep found none in tools/**/*.js); whether Claude Code loads project skills created after session start; whether `superclaude install` would overwrite a user-level hook or skill. Do NOT create task items that reference architecture marked [CODE-CONTRADICTED] or [UNVERIFIED].

SCOPE GUARD (binding on every agent, from the coordinator brief): read and research only. NO product-code edits. NO /sc:implement. NO commit, push, PR, GitHub comment or merge. Do not touch or edit any other repo (IronClaude, IronOrca); read /opt/uv/tools/superclaude/... and /opt/nvm/... read-only as evidence. No `cd` (use absolute paths, `git -C`). UV only for Python. No one-off validation scripts. No env captures written to tracked paths. Stage nothing except `.dev/tasks`. Mark unobserved items UNVERIFIED. Worktree root: /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 2 (Deep Investigation): L1 Discovery. Agents explore the codebase and write findings files to .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/research/
- Phase 3 (Completeness Verification): L4 Review/QA. Standard intensity: 1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative (3 agents), report-only. Serialized fix: consolidate findings, single fix agent, verification round.
- Phase 4 (Web Research): L1 Discovery. Agents explore external sources and write findings files.
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery, then 1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative (3 agents), report-only. Serialized fix: consolidate, fix, verify.
- Phase 6 (Assembly & Validation): L6 Aggregation. rf-assembler consolidates synthesis files into the final report. Then lens-based QA (standard intensity): 3 rf-qa structural + 3 rf-qa-qualitative content + 1 domain lens (finding-reproducibility) = 7 agents. Then source-document fidelity gate (2 rf-qa agents). Then anti-omission gate (Step 6.7b, 2 rf-analyst agents, MANDATORY).

QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: PER_PHASE
  NOTE: apply the standard-intensity reductions from the QA Intensity Adaptation table in SKILL.md.
  Gate 1: Research Completeness (Phase 3)
    - standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
  Gate 2: Synthesis Quality (Phase 5)
    - standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
  Gate 3: Report Validation (Phase 6)
    - standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (finding-reproducibility) = 7 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, after Gate 3)
    - standard: 2 rf-qa fidelity agents. Max 2 fix cycles.
  Gate 5: Anti-Omission (Phase 6, after Gate 4): MANDATORY
    - standard: 2 rf-analyst anti-omission agents (partition the research+synthesis files). Max 2 fix cycles. Judge coverage by MEANING, never by ID citation. Every omission recovered or explicitly justified.
  Review loops follow the project rule: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings. Only blocking findings (CRITICAL/IMPORTANT) fail a gate; minor findings are notes.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All report sections must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.

TESTING_REQUIREMENTS: N/A. Documentation-only skill (research reports), no code produced, no tests applicable.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/research/research-notes.md
Read this file FIRST for full detail: existing files, patterns, candidate options A-F, planned investigation assignments (5 codebase agents 01-05, 2 web agents web-01 and web-02), synthesis mapping (4 synth files), output paths, and the two ambiguities that must go to Open Questions.

SKILL CONTEXT FILE:
/home/coder/.claude/skills/tech-research/SKILL.md
Read the "Agent Prompt Templates" section for the Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt and QA/analyst prompts. Read "Report Structure", "Synthesis Mapping Table", "Synthesis Quality Review Checklist", "Assembly Process", "Validation Checklist" and "Content Rules". These must be embedded in the relevant checklist items per B2 self-contained pattern. (Note: SKILL.md lives under the user's home, not under the project's .claude/.)

MDTM TEMPLATES: /home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md (TEMPLATE 02) and /home/coder/.claude/templates/workflow/01_mdtm_template_generic_task.md.

CRITICAL - GRANULARITY REQUIREMENT:
Per MDTM template rules A3 and A4, create individual checklist items for EVERY research agent (5), web research topic (2), synthesis file (4), gate agent and validation step. No batch items like "spawn all 5 research agents". The research notes SUGGESTED_PHASES section has per-agent detail.

TO BUILD A GOOD TASK FILE, YOU NEED: goal and outputs; source files and context (research notes); phases and steps (research notes SUGGESTED_PHASES + SKILL.md phases); verification criteria; dependencies.

ESCALATION:
You are running as a subagent (not a teammate) with NO team context. Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage. Instead, return the task file path as your final output. If blocked, create the best task file you can and note gaps in the Task Log section.

SKILL PHASES TO ENCODE IN TASK FILE:
Phase 1 - Preparation: update task status to "Doing"; the task folder .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/ with research/, synthesis/, qa/, reviews/ already exists.
Phase 2 - Deep Investigation (parallel spawning mandatory): one item per research agent 01-05 from the research notes, each embedding the full Codebase Research Agent Prompt (Incremental File Writing Protocol and Documentation Staleness Protocol) plus the SCOPE GUARD.
Phase 3 - Research Completeness Verification (standard 3-agent gate + serialized fix): rf-analyst completeness -> qa/analyst-completeness-report.md; rf-qa evidence-quality -> qa/qa-research-evidence-report.md; rf-qa-qualitative research-depth -> qa/qa-research-qualitative-report.md; consolidate -> qa/qa-consolidated-findings-phase3.md; single fix agent; verification round; compile ${TASK_DIR}gaps-and-questions.md. Do not proceed to Phase 4 until PASS.
Phase 4 - Web Research (parallel): one item per web topic web-01 and web-02 using the Web Research Agent Prompt.
Phase 5 - Synthesis (parallel) + Synthesis QA Gate: one item per synth file (4), then the standard 3-agent gate, consolidate -> qa/qa-consolidated-findings-phase5.md, single fix agent, verification. No Phase 6 without PASS.
Phase 6 - Assembly & Validation: Step 6.1 single rf-assembler to RESEARCH-REPORT-bmad-first-use.md; Steps 6.2-6.4 standard 7 lens agents (template-conformance, internal-consistency, evidence-quality, actionability, domain-accuracy, crossref-chain, finding-reproducibility) with outputs qa/qa-lens-*.md; Step 6.5 consolidate -> qa/qa-consolidated-findings-phase6.md and single fix agent; Step 6.6 verification; Step 6.7 fidelity gate (2 agents); Step 6.7b anti-omission gate (2 agents).
Phase 7 - Present to User & Complete Task: summary; task log; frontmatter status Done and completion_date 2026-11-07; NON-BLOCKING suggestion of /tech-reference (do not wait).

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md

STEPS:
1. Read the research notes file (MANDATORY)
2. Read SKILL.md at /home/coder/.claude/skills/tech-research/SKILL.md (MANDATORY)
3. Read /home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md (MANDATORY)
4. Follow PART 1 of the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. Note anything missing in the Task Log section
6. Create the task file at the TASK FILE LOCATION above using PART 2 structure
7. Return the task file path
