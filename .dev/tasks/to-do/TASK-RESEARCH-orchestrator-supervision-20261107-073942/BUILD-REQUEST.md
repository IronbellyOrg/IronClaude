# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation on orchestrator mode for GitHub issue #339 ("Orchestrator - To Run and manage ALL sessions within a worktree"): how a coordinator session can supervise every Orca worker and ccsession in a worktree through a read-only `/sc:sweep` that classifies sessions (waiting on a person, working, stalled, could not determine, finished, idle) over a default 6-hour window and writes one dated static report on the #409 layout, plus the coordinator-loop rules in WORKER-CONTRACT.md, and produce a structured research report with findings, gap analysis, options, and implementation recommendations. The report will be written to `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`.

WHY: The report is the `--research deep` enrichment of `/sc:brainstorm` for issue #339. Its findings feed the brainstorm's adversarial requirements merge, then `/sc:design` (docs/designs/orchestrator-mode.md) and a Phase 1 implementation: a read-only `/sc:sweep` command, its protocol skill or CLI piece, a static report on the #409 layout, and coordinator-loop rules in WORKER-CONTRACT.md. Later phases (`/sc:close`, resume, the cross-session trust layer, orchestrator of orchestrators, the management-server relay) are recorded only. SCOPE GUARD: no live sweep, close, Orca or ccsession launch, and no change to user settings; every source is read-only (files, git history, `--help` text, existing captures).

TASK_ID_PREFIX: TASK-RESEARCH

TEMPLATE: 02 (needs discovery, review gates, conditional fix loops and aggregation)

DOCUMENTATION STALENESS WARNINGS:
Scope discovery found 12 contradictions between documents and code, listed as C1-C12 in the AMBIGUITIES_FOR_USER section of the research notes (`research/research-notes.md`). Phase 2 verify items and the Phase 3 gate must carry them forward with CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED tags. In particular, extending `sc-crash-recovery` as the sweep's home (option A4) is CODE-CONTRADICTED by scope-03; do not build task items on it.
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to ${TASK_DIR}research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only). Serialized fix: consolidate findings → single fix agent → verification round. Partitioning >6 files.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce report sections. Then spawn 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only). Serialized fix: consolidate → fix → verify. Partitioning >4 files.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final report. Then lens-based multi-agent QA: 3-5 rf-qa (structural lenses) + 3-5 rf-qa-qualitative (content lenses) + 3 domain-specific lenses (recommendation feasibility, finding reproducibility, implementation plan concreteness). All report-only. Serialized fix: consolidate → single fix agent → verification. Then source-document fidelity gate: 2-4 rf-qa fidelity agents reading codebase source files + full report. Then the anti-omission gate (Step 6.7b): 2-4 rf-analyst agents that exhaustively enumerate every distinct finding in the research + synthesis files and verify each is represented in the report (source→output completeness, the inverse of the fidelity gate).

QA_INTENSITY: full  (Deep tier, per I22)
QA_GATE_REQUIREMENTS: PER_PHASE
  **NOTE: Gate descriptions below specify FULL intensity agent counts. When QA_INTENSITY is lite or standard, the rf-task-builder applies I22 reductions via the QA Intensity Adaptation table in the Agent Prompt Templates section.**
  Gate 1: Research Completeness (Phase 3)
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >6 files (this task has 8 research files after Phase 2: scope-01..04, 05, 06, plus research-notes.md is input only, so partition).
  Gate 2: Synthesis Quality (Phase 5)
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >4 files (this task has 6 synthesis files, so partition).
  Gate 3: Report Validation (Phase 6)
    - full: 3-5 rf-qa + 3-5 rf-qa-qualitative (scaled by report size per I19) + 3 domain lenses (recommendation-feasibility, finding-reproducibility, implementation-plan-concreteness) = 9-13 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, after Gate 3)
    - full: 2 rf-qa fidelity agents (partition to 3-4 if source >1000 lines). Max 2 fix cycles. HALT after max cycles exceeded.
  Gate 5: Anti-Omission (Phase 6, after Gate 4): MANDATORY at every intensity
    - full: 2 rf-analyst anti-omission agents (partition to 3-4 if research+synthesis >1000 lines). Max 2 fix cycles. HALT after max cycles exceeded.
    - Method (all intensities): exhaustive enumeration (not spot-check); judge coverage by MEANING, never by ID/reference-citation; every omission is recovered or explicitly justified as dedup/out-of-scope, never silently dropped. This gate is the inverse of Gate 4 and is never skipped at any intensity.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All report sections must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.

TESTING_REQUIREMENTS: N/A — documentation-only skill (research reports), no code produced, no tests applicable.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/research/research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments, synthesis mapping, and output paths. Its sections RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, SOLUTION_RESEARCH and AMBIGUITIES_FOR_USER drive the phases below.

SKILL CONTEXT FILE:
~/.claude/skills/tech-research/SKILL.md (the project `.claude/skills/tech-research/SKILL.md` copy may be absent in this worktree; use the installed path)
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Report Structure" section for final report format (includes full sub-section scaffolding). Read the "Synthesis Mapping Table" section for the standard synth-file-to-report-section mapping. Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for report assembly steps. Read the "Validation Checklist" section for Phase 6 validation criteria. Read the "Content Rules" section for writing standards. These must be embedded in the relevant checklist items per B2 self-contained pattern.

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
- The task folder ALREADY EXISTS at .dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/ with `research/`, `synthesis/`, `qa/`, `reviews/` subfolders. Do NOT create a new folder. The item only verifies the four subfolders exist (create any that is missing) and that research/research-notes.md plus the four scope files exist.

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
The four scope files were already written during scope discovery and are marked Status Complete. Phase 2 therefore has two parts (see research notes SUGGESTED_PHASES):
- Verify-only items 2.1-2.4, one per existing scope file (`research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`). Each item spawns one agent that re-checks the file's file:line citations against the current code, adds CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED tags where missing, and appends a `## Summary` section if the file lacks one (scope-01 and scope-03 have none). The agent edits only its assigned file and does not rewrite findings from memory.
- Gap-fill items 2b.1 and 2b.2, spawned in parallel, each a full codebase research agent prompt from SKILL.md (Incremental File Writing Protocol + Documentation Staleness Protocol embedded):
  - 2b.1 → `research/05-orca-row-schema.md` (gap G-A, Critical): the exact row schema of Orca `worker-list` / `worker-show` (fields such as attention, nextAction, liveness verdicts). Sources: `orca-ide worker-list --help`, `orca-ide worker-show --help`, `.dev/orca-command-refactor/inventory/orca-capabilities.md` lines 110-130, and the installed Orca guide. Read-only: help text and existing captures only; never run a command that changes Orca state.
  - 2b.2 → `research/06-orca-open-questions.md` (gap G-B, Critical): the open Orca questions. Sources: `.dev/orca-command-refactor/inventory/orca-capabilities.md` lines 56-68 and 148-151; `src/superclaude/core/WORKER-CONTRACT.md` WC-3 and lines 133-136; `git show 495eb96d:<path>/integration-gaps.md` line 11 (read-only git). Read-only.
- The four important-but-not-critical gaps (pane-key to transcript join; `bootstrap_scan.sh` lines 31 and 73 versus a new scanner; `uv run superclaude` outside a uv project; lazy versus eager init of the Orca client) get NO agent: they are written into `${TASK_DIR}gaps-and-questions.md` in Phase 3.
- All Phase 2 agents in the phase are spawned in parallel using multiple Agent tool calls in a single message.

Phase 3 — Research Completeness Verification (5-AGENT GATE + SERIALIZED FIX):

Step 3.1: Spawn lens-based research gate agents (PARALLEL, all fix_authorization: false)
  - [ ] Spawn rf-analyst (completeness lens) — reads all research files, applies coverage audit + completeness + cross-reference checks from 8-item checklist. Writes to `${TASK_DIR}qa/analyst-completeness-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (cross-validation lens) — reads all research files, applies contradiction detection + gap compilation + depth assessment checks. Writes to `${TASK_DIR}qa/analyst-cross-validation-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (evidence-quality lens) — reads all research files, applies file inventory + evidence density + scope coverage + doc cross-validation checks from 10-item checklist. Writes to `${TASK_DIR}qa/qa-research-evidence-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (gap-detection lens) — reads all research files, applies gap severity + depth appropriateness + integration points + pattern documentation + incremental writing checks. Writes to `${TASK_DIR}qa/qa-research-gaps-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (research-depth lens) — reads all research files, evaluates whether findings are genuinely deep or superficial. Are key findings actionable or vague? Does analysis go beyond surface-level code reading? Writes to `${TASK_DIR}qa/qa-research-qualitative-report.md`. Embed full prompt per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, EACH of the 5 agent types above gets partitioned into multiple instances with `assigned_files` subsets. This task has research-notes.md plus 6 findings files (scope-01..04, 05, 06); partition each agent type into 2 instances (scope-01, scope-02, 05 / scope-03, scope-04, 06), with numbered reports, merged after completion.

Step 3.2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 3.1, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase3.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated blocking findings (minor findings stay as notes). Fix agent spawns additional targeted research agents for blocking gaps requiring new research (one per gap). Applies all blocking fixes. Read-only sources only (scope guard).
  - [ ] Spawn rf-qa (verification, fix_authorization: false) + rf-qa-qualitative (verification, fix_authorization: false) to confirm fixes applied correctly
  - [ ] If verification finds new blocking issues (new minor findings are notes and do not restart the cycle): repeat Step 3.2 (max 2 cycles total). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log issues in Task Log

- Compile final gaps into ${TASK_DIR}gaps-and-questions.md (merged from all reports, plus the four important-but-not-critical gaps listed under Phase 2 and the AMBIGUITIES_FOR_USER items 1-11 and contradiction table C1-C12 from the research notes)
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (research notes SUGGESTED_PHASES call this "Phase 3"; it is this skill's Phase 4):
  - 4.1 → `research/web-01-agent-supervisor-session-health.md`: supervisor and health-check patterns (Erlang/OTP supervisors, Kubernetes liveness versus readiness probes, phi-accrual failure detection, "unknown" as an explicit health state).
  - 4.2 → `research/web-02-static-status-report-conventions.md`: static status report conventions (SRE status pages, shift handover notes, oldest-first ordering, omission counts).
- Each agent must map every pattern it reports onto WC-10 of WORKER-CONTRACT.md (absence of a signal is never proof of death) and onto the read-only Phase 1 constraint.
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (research notes call this "Phase 4"; it is this skill's Phase 5), with these inputs:
  - 5.1 → `synthesis/synth-01-problem-current-state.md` (report sections 1-2): scope-01..04, 05, 06, gaps-and-questions.md.
  - 5.2 → `synthesis/synth-02-target-gaps.md` (sections 3-4): scope-01..04, 05, 06, gaps-and-questions.md, web-01, web-02.
  - 5.3 → `synthesis/synth-03-external-findings.md` (section 5): web-01, web-02.
  - 5.4 → `synthesis/synth-04-options-recommendation.md` (sections 6-7): scope-01..04, 05, 06, web-01, web-02, gaps-and-questions.md, and research-notes.md SOLUTION_RESEARCH options A-D.
  - 5.5 → `synthesis/synth-05-implementation-plan.md` (section 8): scope-01, scope-03, scope-04, web-01, web-02. MUST keep the phase split: Phase 1 = read-only `/sc:sweep` + static report + coordinator-loop rule in WORKER-CONTRACT.md; `/sc:close`, resume, the trust layer, orchestrator of orchestrators and the management-server relay are later phases, recorded only.
  - 5.6 → `synthesis/synth-06-questions-evidence.md` (sections 9-10): gaps-and-questions.md, all research files, research-notes.md AMBIGUITIES_FOR_USER.
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md
- Each item specifies: research files to read, report sections to produce, output path

Step 5.N+1: Spawn lens-based synthesis gate agents (PARALLEL, all fix_authorization: false)
  - [ ] Spawn rf-analyst (synthesis-accuracy lens) — reads all synth files + corresponding research files. Verifies synthesis claims trace back to research evidence. Applies items 1-5 of 10-item Synthesis Quality Review Checklist. Writes to `${TASK_DIR}qa/analyst-synthesis-accuracy.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (source-tracing lens) — reads all synth files + research files. Traces every synthesis claim to its research source. Verifies no fabrication, no doc-only claims in Sections 2/6/7/8, key findings reflected. Applies items 6-10 of checklist. Writes to `${TASK_DIR}qa/analyst-synthesis-tracing.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (structure lens) — reads all synth files. Applies items 1-6 of 12-item synthesis-gate checklist (section headers, table columns, fabrication, evidence citations, options analysis, implementation plan). Writes to `${TASK_DIR}qa/qa-synthesis-structure.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (content-quality lens) — reads all synth files. Applies items 7-12 of checklist (cross-section consistency, doc-only claims, stale docs, content rules, section completeness, hallucinated paths). Writes to `${TASK_DIR}qa/qa-synthesis-content.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (synthesis-coherence lens) — reads all synth files. Evaluates whether synthesis tells a coherent story from the research: do findings build logically? Are conclusions proportionate to evidence? Are contradictions between research files resolved? Writes to `${TASK_DIR}qa/qa-synthesis-qualitative-report.md`. Embed full prompt per B2.

- **Parallel partitioning for large workloads:** When >4 synthesis files exist, each agent type gets partitioned into multiple instances with `assigned_files` subsets. This task has 6 synthesis files: partition each agent type into 2 instances (synth-01..03 / synth-04..06), numbered reports.

Step 5.N+2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 5.N+1, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase5.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated blocking findings (minor findings stay as notes). Fixes blocking issues in synth files in-place.
  - [ ] Spawn rf-qa (verification) + rf-qa-qualitative (verification) to confirm fixes
  - [ ] If blocking issues remain (minor findings stay as notes): repeat Steps 5.N+2 (consolidate, fix, verify) (max 2 cycles total), then HALT

- Do NOT continue to Phase 6 without PASS verdict.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + LENS-BASED QA + FIDELITY GATE):

Step 6.1: Assembly
  - [ ] Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") — NOT a general-purpose Agent — to assemble the final report. Hand it: the list of synth file paths in order (as component_files), the report output path `${TASK_DIR}RESEARCH-REPORT-orchestrator-mode.md`, the Report Structure template from SKILL.md (as output_format), the Assembly Process steps from SKILL.md (as assembly_rules), and the Content Rules from SKILL.md (as content_rules). The assembler reads each synth file and writes the report incrementally section by section — header first, then sections in order, then Table of Contents, then cross-checks internal consistency (gaps in S4 addressed in S8, options in S6 reference S2, Open Questions in S9 not answered elsewhere, Evidence Trail in S10 lists all files). The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole report. Embed the full assembler prompt (see Assembly Agent Prompt Template below and Assembly Process section in SKILL.md) in the checklist item per B2.

Step 6.2: Spawn lens-based rf-qa agents (PARALLEL, all fix_authorization: false)
  4 structural lens agents (agent count shown is for default 500-1500 line tier; task builder adjusts per BUILD_REQUEST Gate 3 scaling). Each agent reads the FULL report but evaluates ONLY its assigned lens. Prompt includes: "Assume this document has at least N errors. Find them." (N = report_lines / 100, minimum 5).
  - [ ] Spawn rf-qa (template-conformance lens) — all 10 report sections present or N/A, correct ordering, no remaining placeholders/sentinels. Output: `${TASK_DIR}qa/qa-lens-template-conformance.md`
  - [ ] Spawn rf-qa (internal-consistency lens) — IDs match across tables, counts agree, cross-references resolve, no contradictions within document. Output: `${TASK_DIR}qa/qa-lens-internal-consistency.md`
  - [ ] Spawn rf-qa (evidence-quality lens) — all claims cite file paths/line numbers, no unverified assertions, no hallucinated paths (verify parent dirs exist). Output: `${TASK_DIR}qa/qa-lens-evidence-quality.md`
  - [ ] Spawn rf-qa (completeness lens) — every topic from scope discovery appears in output, no gaps, no silently dropped items, evidence trail lists all files. Output: `${TASK_DIR}qa/qa-lens-completeness.md`

Step 6.3: Spawn lens-based rf-qa-qualitative agents (PARALLEL, all fix_authorization: false)
  4 content lens agents (agent count shown is for default 500-1500 line tier; task builder adjusts per BUILD_REQUEST Gate 3 scaling).
  - [ ] Spawn rf-qa-qualitative (actionability lens) — every recommendation is specific enough to execute without interpretation; criteria are testable pass/fail not aspirational. Output: `${TASK_DIR}qa/qa-lens-actionability.md`
  - [ ] Spawn rf-qa-qualitative (numbers-metrics lens) — all quantitative claims internally consistent, realistic, sourced; percentages add up; counts match between sections. Output: `${TASK_DIR}qa/qa-lens-numbers-metrics.md`
  - [ ] Spawn rf-qa-qualitative (crossref-chain lens) — trace end-to-end: gap → implementation step, option → evidence, finding → recommendation. Verify every link exists. Output: `${TASK_DIR}qa/qa-lens-crossref-chain.md`
  - [ ] Spawn rf-qa-qualitative (domain-accuracy lens) — claims about codebase match actual code; claims about product match capabilities; no aspirational features as current. Output: `${TASK_DIR}qa/qa-lens-domain-accuracy.md`

Step 6.4: Spawn domain-specific lens agents (PARALLEL, all fix_authorization: false)
  These 3 lenses are specific to tech-research output:
  - [ ] Spawn rf-qa-qualitative (recommendation-feasibility lens) — is the recommended option actually feasible given the codebase constraints documented in Section 2? Are effort/risk assessments realistic? Does the recommendation account for dependencies identified in gap analysis? Output: `${TASK_DIR}qa/qa-lens-recommendation-feasibility.md`
  - [ ] Spawn rf-qa-qualitative (finding-reproducibility lens) — could another investigator reproduce each finding by following the cited evidence? Are file paths and line numbers sufficient to locate each claim? Are data flow traces complete? Output: `${TASK_DIR}qa/qa-lens-finding-reproducibility.md`
  - [ ] Spawn rf-qa (implementation-plan-concreteness lens) — does the implementation plan specify actual files to create/modify, actual function signatures, actual integration points? Or is it generic ("create a service", "add configuration")? Every step must name specific files. Output: `${TASK_DIR}qa/qa-lens-implementation-concreteness.md`

Step 6.5: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL lens QA reports from Steps 6.2-6.4, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase6.md`. Include: finding description, source lens, severity (CRITICAL/IMPORTANT/MINOR), affected section, proposed fix.
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with the consolidated blocking findings list (minor findings stay as notes). The fix agent reads the report, applies ALL blocking fixes from the consolidated list, and documents each fix applied. Writes fix log to `${TASK_DIR}qa/qa-fix-log.md`.

Step 6.6: Verification round (PARALLEL)
  - [ ] Spawn rf-qa (verification, fix_authorization: false) — verify fixes applied correctly, no new issues introduced. Output: `${TASK_DIR}qa/qa-fix-verification.md`
  - [ ] Spawn rf-qa-qualitative (verification, fix_authorization: false) — verify content quality maintained after fixes. Output: `${TASK_DIR}qa/qa-fix-verification-qualitative.md`
  - [ ] If blocking issues found (new minor findings are notes and do not restart the cycle): repeat Steps 6.5-6.6 (max 2 cycles). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings.

Step 6.7: Source-document fidelity gate (PARALLEL)
  - [ ] Spawn rf-qa (fidelity-agent-1, fix_authorization: false) — reads the first half of codebase source files investigated during Phase 2 (from research file paths) + the FULL assembled report. Checks: semantic coverage (each major code component found in research appears in report), detail preservation (specific function names, line numbers, data types survive into report), phantom finding detection (report claims present in evidence trail but not substantiated by source code). Output: `${TASK_DIR}qa/qa-source-fidelity-report-1.md`
  - [ ] Spawn rf-qa (fidelity-agent-2, fix_authorization: false) — reads the second half of codebase source files + FULL report. Same checks. Output: `${TASK_DIR}qa/qa-source-fidelity-report-2.md`
  - [ ] If source files >1000 lines total: spawn 3-4 fidelity agents instead of 2, partitioning source files across agents.
  - [ ] Consolidate fidelity findings, apply fixes via serialized protocol (same as Step 6.5-6.6). Verification round on fidelity fixes. Max 2 fix cycles.
  - [ ] If fidelity issues persist after max 2 fix cycles: HALT, present to user.

Step 6.7b: Anti-omission gate (source→output completeness, PARALLEL): MANDATORY
  - [ ] Spawn rf-analyst (anti-omission-agent-1, fix_authorization: false): assigned the first half of the research + synthesis files. ENUMERATE every distinct finding/claim/recommendation/item in the assigned files, then verify EACH is represented (semantically) in the final report. CRITICAL METHOD: judge coverage by MEANING, never by ID/reference-citation; the report absorbs findings without citing their source IDs, so an ID-membership test is invalid and both over- and under-reports. A finding whose substance appears nowhere in the report = OMISSION. Rate each omission by importance (a dropped distinct finding/discipline = IMPORTANT or CRITICAL; a legitimately deduped restatement is NOT an omission, note it as covered-by-dedup). Output: `${TASK_DIR}qa/qa-anti-omission-report-1.md`
  - [ ] Spawn rf-analyst (anti-omission-agent-2, fix_authorization: false): assigned the second half of the research + synthesis files; same exhaustive enumerate-and-verify method, same output format. Output: `${TASK_DIR}qa/qa-anti-omission-report-2.md`
  - [ ] If the research + synthesis files exceed ~1000 lines total: spawn 3-4 anti-omission agents instead of 2, partitioning the files across agents so the enumeration is EXHAUSTIVE, never a spot-check.
  - [ ] Consolidate anti-omission findings (each unrecovered, unjustified omission is a blocking finding; minor findings stay as notes). For EACH omission: either RECOVER it (the single fix agent adds the dropped finding to the report) or EXPLICITLY JUSTIFY it as intentional dedup / out-of-scope (recorded in the consolidated findings). NEVER silently drop an omission. Apply via the serialized fix protocol (report-only agents → consolidate → single fix agent → verification round). Max 2 fix cycles, then HALT and present to user.
  - [ ] This gate is the INVERSE of Step 6.7 (fidelity verifies output→source: no fabrication/distortion; anti-omission verifies source→output: no dropped finding). BOTH are mandatory; passing fidelity does NOT imply completeness.

- Every blocking finding must be resolved before Phase 7; minor findings are recorded as notes and do not block.

Phase 7 — Present to User & Complete Task:
- Present summary to user (report location, key findings, recommendation, research file count, open questions)
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- `NON-BLOCKING` Suggest downstream skill: "This research can feed directly into a Technical Reference document. You can create one using `/tech-reference` — the research files are already in place and will accelerate the process." Present the suggestion, mark this item complete immediately, and do NOT wait for a user response. This item does not gate task completion.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/TASK-RESEARCH-orchestrator-supervision-20261107-073942.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, report structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - TEMPLATE: 02 → ~/.claude/templates/workflow/02_mdtm_template_complex_task.md (in-checkout fallback: src/superclaude/templates/workflow/02_mdtm_template_complex_task.md; the project .claude/templates/ copy is missing)
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/TASK-RESEARCH-orchestrator-supervision-20261107-073942.md using PART 2 structure. Every item that writes a file names its exact output path.
7. Return the task file path
