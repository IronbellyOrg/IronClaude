# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation on existing solutions and design inputs for a GitHub issue watcher and routing service (GitHub issue #331 of IronbellyOrg/IronClaude: a watcher that finds issues that are tagged, human-approved, in a GitHub Project and in Backlog status, and makes the right developer's Coder workspace start a new session running `/sc:issue --claim <N>`), and produce a structured research report with findings, gap analysis, options (workspace-side poller, GitHub Action plus listener, central microservice, hybrids), and a concrete implementation recommendation that fits this repository (commands, skills, CLI code, docs; no live deployment). The report will be written to `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md`.

WHY: Issue #331 says to research existing solutions first and asks: microservice versus GitHub Action, how to securely tie each workspace to a GitHub account, and what the Coder-side listener is. The findings feed a `/sc:brainstorm` (then spec-panel, design, task list, execution) for the same issue. The report must also let the orchestrator write a condensed copy to `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/research-deep.md`.

TASK_ID_PREFIX: TASK-RESEARCH

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
None found during scope discovery beyond those in `.dev/issues/331/accuracy-check.md` (the issue text expects `/sc:issue --claim` to orchestrate a full pipeline; today it stops after writing next-steps.md; `/sc:issue` cannot run as an Orca worker; `--claim --pipeline` is design-only). Phase 2 agents will perform full documentation cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags. Do NOT create task items that build on the issue's claim that claim orchestrates the pipeline.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 2 (Deep Investigation): L1 Discovery, 3 codebase agents write findings files to the task `research/` folder (see research notes SUGGESTED_PHASES)
- Phase 3 (Completeness Verification): L4 Review/QA, standard intensity, serialized fix
- Phase 4 (Web Research): L1 Discovery, 2 web agents (web-01, web-02)
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery, 4 synth files, then standard-intensity gate, serialized fix
- Phase 6 (Assembly & Validation): L6 Aggregation with rf-assembler, then lens-based QA (standard), fidelity gate, anti-omission gate

QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: PER_PHASE
  Apply the standard-intensity agent counts from the "QA Intensity Adaptation" section of the tech-research SKILL.md:
  Gate 1 Research Completeness (Phase 3): 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
  Gate 2 Synthesis Quality (Phase 5): 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
  Gate 3 Report Validation (Phase 6): 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (finding-reproducibility) = 7 agents. Max 2 fix cycles.
  Gate 4 Source-Document Fidelity: 2 rf-qa fidelity agents. Max 2 fix cycles.
  Gate 5 Anti-Omission: MANDATORY: 2 rf-analyst anti-omission agents (inverse of the fidelity gate; judge coverage by meaning, never by ID/reference-citation; every omission recovered or explicitly justified). Max 2 fix cycles.
  All gate agents are report-only (fix_authorization: false); one fix agent per gate applies blocking findings; a verification round confirms. Minor findings are notes and never fail a gate. A review loop is at most 2 fix cycles (3 reviews), then HALT and escalate with the open blocking findings.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
TESTING_REQUIREMENTS: N/A (documentation-only research, no code produced).

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/research/research-notes.md
Read this file FIRST.

SKILL CONTEXT FILE:
/home/coder/.claude/skills/tech-research/SKILL.md
(The project copy `.claude/skills/tech-research/SKILL.md` does not exist in this checkout; use the installed path above.) Read the "Agent Prompt Templates", "Report Structure", "Synthesis Mapping Table", "Synthesis Quality Review Checklist", "Assembly Process", "Validation Checklist" and "Content Rules" sections; embed them per B2.

MDTM TEMPLATE (TEMPLATE: 02): /home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md (the project path `.claude/templates/workflow/` does not exist in this checkout).

CRITICAL: GRANULARITY REQUIREMENT:
Per MDTM template rules A3 and A4, create individual checklist items for EVERY research agent, web research topic, synthesis file and validation step; no batch items.

CONSTRAINTS FOR ALL AGENTS:
- Read-only on the codebase; do not modify source files; do not run, install or deploy anything.
- Web agents: Tavily or WebSearch/WebFetch are allowed; cite source URLs; mark what is UNVERIFIED when a primary source cannot be found. Today is 2026-11-07; prefer current official documentation.
- Repo and PR target is IronbellyOrg/IronClaude only; never interact with SuperClaude-Org; no secrets in any file.
- All agent output files are written incrementally (header first, then append).

ESCALATION:
Running as a subagent (no team context). Do NOT broadcast TASK_READY, use TaskCreate or SendMessage. Return the task file path as the final output. If blocked, create the best task file you can and note gaps in the Task Log.

SKILL PHASES TO ENCODE IN TASK FILE:
Phase 1 Preparation; Phase 2 Deep Investigation (3 parallel codebase agents, outputs per research notes); Phase 3 Research Completeness Verification (standard gate + serialized fix); Phase 4 Web Research (2 parallel web agents); Phase 5 Synthesis (4 synth files, parallel) + Synthesis QA Gate (standard + serialized fix); Phase 6 Assembly (single rf-assembler) + lens-based QA (Step 6.2-6.4 at standard counts) + serialized fix + verification + source-document fidelity gate (Step 6.7) + anti-omission gate (Step 6.7b); Phase 7 Present to user and complete (write the condensed copy to `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/research-deep.md` as an explicit checklist item: a summary of at most about 5000 tokens that states the recommendation, the options table and a pointer to the full report path).

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/TASK-RESEARCH-issue-watcher-20261107-064950.md

STEPS:
1. Read the research notes file (MANDATORY)
2. Read the SKILL.md file above (MANDATORY)
3. Read the MDTM template above (MANDATORY)
4. Follow PART 1 of the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. Note anything missing in the Task Log section
6. Create the task file at the TASK FILE LOCATION using PART 2 structure
7. Return the task file path
