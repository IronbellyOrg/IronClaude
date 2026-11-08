# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation on the exact semantics of git's pre-push hook (stdin records for every push form, arguments, empty stdin; bypass paths; hook lookup in linked worktrees incl. core.hooksPath, rev-parse --git-path, extensions.worktreeConfig; hook process ancestry and environment; Linux no-replace atomic publication and the executable bit; the git version that introduced each behaviour and the installed git 2.47.3) as they bear on an L2 guard that refuses a governed AI agent's push to refs/heads/main or refs/heads/master, and produce a structured research report with findings, gap analysis, options, and implementation recommendations. The report will be written to `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/RESEARCH-REPORT-pre-push-guard.md`.

WHY: Input to a /sc:brainstorm (issue #441) that will spec the L2 pre-push layer of the launch-level guard and the IR-7 W-L2-ABSENT refusal. The brainstorm needs cited facts (official git docs URLs or commands run against real git 2.47.3 in /tmp) about what the hook receives, what can skip it, where git looks for it from a linked worktree, how it can identify the pushing process, and how to install it without replacing an existing file.

TASK_ID_PREFIX: TASK-RESEARCH

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
None found during scope discovery. Phase 2 agents will perform full documentation cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags. Design doc §19 statements about git behaviour (dry-run, bypasses, hooks lookup) are UNVERIFIED until confirmed by the empirical agent or official docs.
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED] or [UNVERIFIED].

SAFETY CONSTRAINTS (embed in every relevant item):
- No source file is edited. Research agents READ code and run experiments only.
- Any git experiment runs only inside a fresh `mktemp -d` directory under /tmp, using a local bare repository as the remote. Never run git push against any real remote (no origin, no network URL). Clean up the temp directory afterwards.
- Use only `uv` for Python (`uv run python ...`), never bare python/pip.
- Post nothing anywhere (no gh, no comments, no issues).

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase / run experiments and write findings files to research/
- Phase 3 (Completeness Verification): L4 Review/QA — standard intensity: 1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative (all report-only). Serialized fix: consolidate → single fix agent → verification round.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — synthesis agents, then standard gate 1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative. Serialized fix.
- Phase 6 (Assembly & Validation): rf-assembler, then standard lens QA (3 rf-qa structural: template-conformance, internal-consistency, evidence-quality; 3 rf-qa-qualitative content: actionability, domain-accuracy, crossref-chain; 1 domain lens: finding-reproducibility = 7 agents). Serialized fix. Then fidelity gate (2 rf-qa). Then anti-omission gate (2 rf-analyst).

QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: PER_PHASE
  Gate 1: Research Completeness (Phase 3) — standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
  Gate 2: Synthesis Quality (Phase 5) — standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
  Gate 3: Report Validation (Phase 6) — standard: 3 rf-qa structural + 3 rf-qa-qualitative content + 1 domain lens (finding-reproducibility) = 7 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity — standard: 2 rf-qa fidelity agents. Max 2 fix cycles.
  Gate 5: Anti-Omission — standard: 2 rf-analyst anti-omission agents (partition the research+synthesis files). Max 2 fix cycles. Judge coverage by MEANING, never by ID citation; exhaustive enumeration; every omission recovered or explicitly justified.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All report sections must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths/line numbers, an official documentation URL, or the exact command run (with its output) in a /tmp experiment.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.

TESTING_REQUIREMENTS: N/A — documentation-only (research report), no code produced. Temp-dir git experiments are research evidence, not tests.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/research/research-notes.md
Read this file FIRST: existing files, patterns, the four Phase 2 assignments, two web topics, synthesis mapping and output paths.

SKILL CONTEXT FILE:
~/.claude/skills/tech-research/SKILL.md (project copy .claude/skills/tech-research/SKILL.md if present)
Read the "Agent Prompt Templates" section (Codebase Research, Web Research, Synthesis, analyst, QA, lens, fidelity, anti-omission, assembler prompts), "Report Structure", "Synthesis Mapping Table", "Synthesis Quality Review Checklist", "Assembly Process", "Validation Checklist" and "Content Rules". Embed them in the relevant checklist items per B2. Apply the "QA Intensity Adaptation" standard row.

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 and A4, create individual checklist items for EVERY research agent (4), web research topic (2), synthesis file (4), and every QA/validation agent. No batch items.

SKILL PHASES TO ENCODE IN TASK FILE:
Phase 1 — Preparation: status to Doing; confirm task folder and subfolders exist (they already do).
Phase 2 — Deep Investigation: 4 parallel items from research notes SUGGESTED_PHASES (01 identity selector, 02 L1 coverage, 03 design/claim cross-validation, 04 empirical real-git experiments in /tmp). Embed full Codebase Research Agent Prompt with Incremental File Writing Protocol and Documentation Staleness Protocol. Agent 04 records every command and its output verbatim (bounded) and uses only a mktemp -d directory.
Phase 3 — Research gate (standard, 3 agents) + serialized fix + verification; compile gaps-and-questions.md.
Phase 4 — Web research: 2 parallel items (web-01 official git docs and release notes; web-02 Linux link/open/rename man pages and git's hook executable check in source).
Phase 5 — Synthesis: 4 parallel items (synth-01 S1-S2, synth-02 S3-S5, synth-03 S6-S8, synth-04 S9-S10), then standard synthesis gate (3 agents) + serialized fix + verification.
Phase 6 — Assembly (single rf-assembler), standard lens QA (7 agents), consolidate + single fix agent + verification (2 agents), fidelity gate (2 agents) + fix cycle, anti-omission gate (2 agents) + fix cycle.
Phase 7 — Present summary, write Task Log, set status Done with completion_date, NON-BLOCKING suggestion of /tech-reference.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/TASK-RESEARCH-pre-push-guard-20261108-095046.md

ESCALATION:
You are a subagent with no team context. Do NOT broadcast TASK_READY, use TaskCreate, or SendMessage. Return the task file path as your final output. If blocked, create the best task file you can and note gaps in the Task Log.

STEPS:
1. Read the research notes file (MANDATORY)
2. Read the SKILL.md sections listed above (MANDATORY)
3. Read the MDTM template 02: ~/.claude/templates/workflow/02_mdtm_template_complex_task.md (or .claude/templates/workflow/02_mdtm_template_complex_task.md)
4. Follow PART 1 instructions (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. Create the task file at the TASK FILE LOCATION using PART 2 structure
6. Return the task file path
