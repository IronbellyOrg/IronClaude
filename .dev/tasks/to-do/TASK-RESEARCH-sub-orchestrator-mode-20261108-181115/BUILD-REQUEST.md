# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation on whether and how the proposed /sc:orchestrator should support a sub-orchestrator or coordinator mode (possibly selected with --sub): a session that delegates work to its own sessions inside a worktree while taking orders from, and reporting to, an orchestrator above. Produce a structured research report with findings, gap analysis, options, and a decision recommendation (value, implications, unlocks, rethinks, especially of rule WC-13, decision D5 and the role "a coordinator under another orchestrator" named by PR #449). The report will be written to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md`.

WHY: GitHub issue #444 asks for this evaluation before anyone builds it; issues #339 (v1) and #423 (v2) of /sc:orchestrator depend on the answer; PR #449 named the role without defining it and deferred WC-13 to this issue (INF-027). The user wants a decision report and explicitly does NOT want an implementation plan or any implementation started.

TASK_ID_PREFIX: TASK-RESEARCH

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
Found during scope discovery (the research notes list them with tags). Do NOT build task items on these claims as if current:
- `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:985` says no command accepts `--unattended` and `UNATTENDED_COMMANDS` is empty: [CODE-CONTRADICTED] (31 commands have an `## Unattended mode` section; `UNATTENDED_COMMANDS = frozenset(UNATTENDED_EXPECT)` at `tests/skills/test_worker_contract.py:746`).
- `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md:3,64` ("spec is not edited", "none of these edits is applied yet") and `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:3` ("not yet applied"): [CODE-CONTRADICTED] (the spec at `specs/orca-worker-contract-spec.md:405,386,81,98,276,315,88` has applied them). Line citations inside D5 RECOMMENDATION.md to the spec (for example SPEC:79) have drifted.
- `.dev/orca-command-refactor/decisions/D5/option-a.md:19` ("P0 smoke runs" revisit wording) is superseded by the two-part trigger at D5 RECOMMENDATION.md:49 and SPEC:405.
- The #339 accuracy-check comment says PR #422 is open: [CODE-CONTRADICTED] (merged). Issue #446 cites WC-9 at `WORKER-CONTRACT.md:44`: it is at :45 after PR #434.
- Scope researchers' line numbers are second-hand: Phase 2 agents must re-read before citing. Prior #444 findings F1-F7 (`.dev/issues/444/analysis/analyze-orchestration.md`) are documentation, not evidence.
Phase 2 agents will perform full documentation cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags.
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED] or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid building on obviously stale foundations.

TASK-SPECIFIC CONSTRAINTS (apply to every agent prompt embedded in the task file):
1. READ-ONLY investigation. No agent edits any source, doc, test, hook or config file outside its own output file. No GitHub writes: only read-only `gh` calls, always with `--repo IronbellyOrg/IronClaude`, never the upstream SuperClaude-Org repo. No Orca state changes: only `--help`, `skills get`, list/show/read-style commands and file reads; never `worker-start`, `dispatch`, `task-create`, `worktree create`, `agent launch`, `run-create` or any setting change.
2. Do NOT pass the `model` parameter on any Agent call and do not run `/model`: the user asked that no model tier be switched.
3. Section 8 of the report (Implementation Plan) is decision-only: the report keeps all 10 sections, but Section 8 is marked N/A as an implementation plan with the rationale "the requester asked for a decision report, not a plan", and instead carries a "Change surface per option" table (files, tests, docs and installed copies each option would touch, from research file 07). No phases, no step ordering, no effort schedule. The Phase 6 domain lens "implementation-plan-concreteness" is applied to that change-surface table (every row names real files).
4. Section 7 (Recommendation) must be a decision with explicit gates (what must be true before a `--sub` mode is built).
5. Options to evaluate in Section 6 (working labels; synthesis may refine): O1 keep two tiers and no sub mode; O2 peer coordinators opened by the person; O3 supervised sub-orchestrator as a worker with helpers (D5 option b, depth 2, scoped brief, WC-13 relaxed); O4 handoff-owner sub-orchestrator via `worktree create --agent` / `agent launch` with a new upward channel; O5 in-session sub-orchestration via Agent-tool subagents; O6 defer with explicit gates. Each option is judged against the evidence in the research files.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only). Serialized fix: consolidate findings → single fix agent → verification round. Partitioning >6 files.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce report sections. Then spawn 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only). Serialized fix: consolidate → fix → verify. Partitioning >4 files.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final report. Then lens-based multi-agent QA: 3-5 rf-qa (structural lenses) + 3-5 rf-qa-qualitative (content lenses) + 3 domain-specific lenses (recommendation feasibility, finding reproducibility, implementation plan concreteness). All report-only. Serialized fix: consolidate → single fix agent → verification. Then source-document fidelity gate: 2-4 rf-qa fidelity agents reading codebase source files + full report. Then the anti-omission gate (Step 6.7b): 2-4 rf-analyst agents that exhaustively enumerate every distinct finding in the research + synthesis files and verify each is represented in the report (source→output completeness, the inverse of the fidelity gate).

QA_INTENSITY: full  (per I22: Deep tier default; no user override)
QA_GATE_REQUIREMENTS: PER_PHASE
  **NOTE: Gate descriptions below specify FULL intensity agent counts. When QA_INTENSITY is lite or standard, the rf-task-builder applies I22 reductions via the QA Intensity Adaptation table in the Agent Prompt Templates section.**
  Gate 1: Research Completeness (Phase 3)
    - lite: 1 rf-qa (evidence + gaps) + 1 rf-qa-qualitative (depth + completeness) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >6 files.
  Gate 2: Synthesis Quality (Phase 5)
    - lite: 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >4 files.
  Gate 3: Report Validation (Phase 6)
    - lite: 1 rf-qa (combined structural) + 1 rf-qa-qualitative (combined content) + 1 domain lens (finding-reproducibility) = 3 agents. Max 1 fix cycle.
    - standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (finding-reproducibility) = 7 agents. Max 2 fix cycles.
    - full: 3-5 rf-qa + 3-5 rf-qa-qualitative (scaled by report size per I19) + 3 domain lenses (recommendation-feasibility, finding-reproducibility, implementation-plan-concreteness) = 9-13 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, after Gate 3)
    - lite: 1 rf-qa fidelity agent (combined semantic-coverage + phantom-detection lenses). Max 1 fix cycle.
    - standard: 2 rf-qa fidelity agents. Max 2 fix cycles.
    - full: 2 rf-qa fidelity agents (partition to 3-4 if source >1000 lines). Max 2 fix cycles. HALT after max cycles exceeded.
  Gate 5: Anti-Omission (Phase 6, after Gate 4): MANDATORY at every intensity
    - lite: 1 rf-analyst anti-omission agent (enumerate every distinct research+synthesis finding, verify each is represented in the report). Max 1 fix cycle.
    - standard: 2 rf-analyst anti-omission agents (partition the research+synthesis files). Max 2 fix cycles.
    - full: 2 rf-analyst anti-omission agents (partition to 3-4 if research+synthesis >1000 lines). Max 2 fix cycles. HALT after max cycles exceeded.
    - Method (all intensities): exhaustive enumeration (not spot-check); judge coverage by MEANING, never by ID/reference-citation; every omission is recovered or explicitly justified as dedup/out-of-scope, never silently dropped. This gate is the inverse of Gate 4 and is never skipped at any intensity.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All report sections must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.

TESTING_REQUIREMENTS: N/A — documentation-only skill (research reports), no code produced, no tests applicable.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/research/research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments (8 codebase agents 01-08, 4 web agents web-01..04), synthesis mapping (6 synth files), and output paths. The four scope-discovery files under `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/research/scope/` hold the detailed scope findings; Phase 2 agents may be pointed at them as starting hypotheses (never as evidence).

SKILL CONTEXT FILE:
.claude/skills/tech-research/SKILL.md
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
- Create the task folder at .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/ with `research/`, `synthesis/`, `qa/`, `reviews/` subfolders (they already exist: verify, do not recreate)

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (from research notes SUGGESTED_PHASES: agents 01 to 08)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type, files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2, plus the TASK-SPECIFIC CONSTRAINTS above (read-only, no model parameter)
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 8 research assignments: spawn all 8 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.

Phase 3 — Research Completeness Verification (5-AGENT GATE + SERIALIZED FIX):

Step 3.1: Spawn lens-based research gate agents (PARALLEL, all fix_authorization: false)
  - [ ] Spawn rf-analyst (completeness lens) — reads all research files, applies coverage audit + completeness + cross-reference checks from 8-item checklist. Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/analyst-completeness-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (cross-validation lens) — reads all research files, applies contradiction detection + gap compilation + depth assessment checks. Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/analyst-cross-validation-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (evidence-quality lens) — reads all research files, applies file inventory + evidence density + scope coverage + doc cross-validation checks from 10-item checklist. Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-research-evidence-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (gap-detection lens) — reads all research files, applies gap severity + depth appropriateness + integration points + pattern documentation + incremental writing checks. Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-research-gaps-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (research-depth lens) — reads all research files, evaluates whether findings are genuinely deep or superficial. Are key findings actionable or vague? Does analysis go beyond surface-level code reading? Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-research-qualitative-report.md`. Embed full prompt per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, EACH of the 5 agent types above gets partitioned into multiple instances with `assigned_files` subsets. With 8 codebase research files (01-08, the scope files are excluded from this count), partition each agent type into 2 instances (4 files each) or justify in the Task Log why not. Each writes to numbered reports. Merge after completion.

Step 3.2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 3.1, consolidate into `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-consolidated-findings-phase3.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated blocking findings (minor findings stay as notes). Fix agent spawns additional targeted research agents for blocking gaps requiring new research (one per gap). Applies all blocking fixes.
  - [ ] Spawn rf-qa (verification, fix_authorization: false) + rf-qa-qualitative (verification, fix_authorization: false) to confirm fixes applied correctly
  - [ ] If verification finds new blocking issues (new minor findings are notes and do not restart the cycle): repeat Step 3.2 (max 2 cycles total). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log issues in Task Log

- Compile final gaps into .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/gaps-and-questions.md (merged from all reports)
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES: web-01 to web-04)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path
- Web research targets: official Claude Code documentation, Anthropic and other credible engineering write-ups on hierarchical multi-agent systems, the macaroons / Biscuit / CaMeL papers and specs, Orca's public docs and repository, community discussion where it adds evidence. Tavily first; WebSearch/WebFetch only if Tavily is unavailable.

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (from research notes RECOMMENDED_OUTPUTS: synth-01 to synth-06)
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md
- Each item specifies: research files to read, report sections to produce, output path

Step 5.N+1: Spawn lens-based synthesis gate agents (PARALLEL, all fix_authorization: false)
  - [ ] Spawn rf-analyst (synthesis-accuracy lens) — reads all synth files + corresponding research files. Verifies synthesis claims trace back to research evidence. Applies items 1-5 of 10-item Synthesis Quality Review Checklist. Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/analyst-synthesis-accuracy.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (source-tracing lens) — reads all synth files + research files. Traces every synthesis claim to its research source. Verifies no fabrication, no doc-only claims in Sections 2/6/7/8, key findings reflected. Applies items 6-10 of checklist. Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/analyst-synthesis-tracing.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (structure lens) — reads all synth files. Applies items 1-6 of 12-item synthesis-gate checklist (section headers, table columns, fabrication, evidence citations, options analysis, implementation plan; for this task item 6 is applied to the Section 8 change-surface table per TASK-SPECIFIC CONSTRAINTS 3). Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-synthesis-structure.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (content-quality lens) — reads all synth files. Applies items 7-12 of checklist (cross-section consistency, doc-only claims, stale docs, content rules, section completeness, hallucinated paths). Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-synthesis-content.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (synthesis-coherence lens) — reads all synth files. Evaluates whether synthesis tells a coherent story from the research: do findings build logically? Are conclusions proportionate to evidence? Are contradictions between research files resolved? Writes to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-synthesis-qualitative-report.md`. Embed full prompt per B2.

- **Parallel partitioning for large workloads:** When >4 synthesis files exist (there are 6), each agent type gets partitioned into multiple instances with `assigned_files` subsets (for example 3 synth files each).

Step 5.N+2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 5.N+1, consolidate into `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-consolidated-findings-phase5.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated blocking findings (minor findings stay as notes). Fixes blocking issues in synth files in-place.
  - [ ] Spawn rf-qa (verification) + rf-qa-qualitative (verification) to confirm fixes
  - [ ] If blocking issues remain (minor findings stay as notes): repeat Steps 5.N+2 (consolidate, fix, verify) (max 2 cycles total), then HALT

- Do NOT continue to Phase 6 without PASS verdict.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + LENS-BASED QA + FIDELITY GATE + ANTI-OMISSION GATE):

Step 6.1: Assembly
  - [ ] Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") — NOT a general-purpose Agent — to assemble the final report. Hand it: the list of synth file paths in order (as component_files), the report output path `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md`, the Report Structure template from SKILL.md (as output_format), the Assembly Process steps from SKILL.md (as assembly_rules), and the Content Rules from SKILL.md (as content_rules), plus TASK-SPECIFIC CONSTRAINTS 3 and 4 (Section 8 is N/A as an implementation plan and carries the change-surface table; Section 7 carries explicit gates). The assembler reads each synth file and writes the report incrementally section by section — header first, then sections in order, then Table of Contents, then cross-checks internal consistency (gaps in S4 addressed in S7/S8, options in S6 reference S2, Open Questions in S9 not answered elsewhere, Evidence Trail in S10 lists all files). The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole report. Embed the full assembler prompt (see Assembly Agent Prompt Template and Assembly Process section in SKILL.md) in the checklist item per B2.

Step 6.2: Spawn lens-based rf-qa agents (PARALLEL, all fix_authorization: false)
  4 structural lens agents (agent count shown is for default 500-1500 line tier; task builder adjusts per BUILD_REQUEST Gate 3 scaling). Each agent reads the FULL report but evaluates ONLY its assigned lens. Prompt includes: "Assume this document has at least N errors. Find them." (N = report_lines / 100, minimum 5).
  - [ ] Spawn rf-qa (template-conformance lens) — all 10 report sections present or N/A, correct ordering, no remaining placeholders/sentinels. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-template-conformance.md`
  - [ ] Spawn rf-qa (internal-consistency lens) — IDs match across tables, counts agree, cross-references resolve, no contradictions within document. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-internal-consistency.md`
  - [ ] Spawn rf-qa (evidence-quality lens) — all claims cite file paths/line numbers, no unverified assertions, no hallucinated paths (verify parent dirs exist). Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-evidence-quality.md`
  - [ ] Spawn rf-qa (completeness lens) — every topic from scope discovery appears in output, no gaps, no silently dropped items, evidence trail lists all files. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-completeness.md`

Step 6.3: Spawn lens-based rf-qa-qualitative agents (PARALLEL, all fix_authorization: false)
  4 content lens agents (agent count shown is for default 500-1500 line tier; task builder adjusts per BUILD_REQUEST Gate 3 scaling).
  - [ ] Spawn rf-qa-qualitative (actionability lens) — every recommendation is specific enough to execute without interpretation; criteria are testable pass/fail not aspirational. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-actionability.md`
  - [ ] Spawn rf-qa-qualitative (numbers-metrics lens) — all quantitative claims internally consistent, realistic, sourced; percentages add up; counts match between sections. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-numbers-metrics.md`
  - [ ] Spawn rf-qa-qualitative (crossref-chain lens) — trace end-to-end: gap → recommendation gate, option → evidence, finding → recommendation. Verify every link exists. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-crossref-chain.md`
  - [ ] Spawn rf-qa-qualitative (domain-accuracy lens) — claims about codebase match actual code; claims about product match capabilities; no aspirational features as current. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-domain-accuracy.md`

Step 6.4: Spawn domain-specific lens agents (PARALLEL, all fix_authorization: false)
  These 3 lenses are specific to tech-research output:
  - [ ] Spawn rf-qa-qualitative (recommendation-feasibility lens) — is the recommended option actually feasible given the codebase constraints documented in Section 2? Are effort/risk assessments realistic? Does the recommendation account for dependencies identified in gap analysis? Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-recommendation-feasibility.md`
  - [ ] Spawn rf-qa-qualitative (finding-reproducibility lens) — could another investigator reproduce each finding by following the cited evidence? Are file paths and line numbers sufficient to locate each claim? Are data flow traces complete? Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-finding-reproducibility.md`
  - [ ] Spawn rf-qa (implementation-plan-concreteness lens, applied to the Section 8 change-surface table per TASK-SPECIFIC CONSTRAINTS 3) — does every row name specific files, tests or docs that would change, or is it generic? Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-lens-implementation-concreteness.md`

Step 6.5: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL lens QA reports from Steps 6.2-6.4, consolidate into `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-consolidated-findings-phase6.md`. Include: finding description, source lens, severity (CRITICAL/IMPORTANT/MINOR), affected section, proposed fix.
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with the consolidated blocking findings list (minor findings stay as notes). The fix agent reads the report, applies ALL blocking fixes from the consolidated list, and documents each fix applied. Writes fix log to `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-fix-log.md`.

Step 6.6: Verification round (PARALLEL)
  - [ ] Spawn rf-qa (verification, fix_authorization: false) — verify fixes applied correctly, no new issues introduced. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-fix-verification.md`
  - [ ] Spawn rf-qa-qualitative (verification, fix_authorization: false) — verify content quality maintained after fixes. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-fix-verification-qualitative.md`
  - [ ] If blocking issues found (new minor findings are notes and do not restart the cycle): repeat Steps 6.5-6.6 (max 2 cycles). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings.

Step 6.7: Source-document fidelity gate (PARALLEL)
  - [ ] Spawn rf-qa (fidelity-agent-1, fix_authorization: false) — reads the first half of codebase source files investigated during Phase 2 (from research file paths) + the FULL assembled report. Checks: semantic coverage (each major code component found in research appears in report), detail preservation (specific function names, line numbers, data types survive into report), phantom finding detection (report claims present in evidence trail but not substantiated by source code). Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-source-fidelity-report-1.md`
  - [ ] Spawn rf-qa (fidelity-agent-2, fix_authorization: false) — reads the second half of codebase source files + FULL report. Same checks. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-source-fidelity-report-2.md`
  - [ ] If source files >1000 lines total: spawn 3-4 fidelity agents instead of 2, partitioning source files across agents. (The sources here exceed 1000 lines: partition to 4 agents.)
  - [ ] Consolidate fidelity findings, apply fixes via serialized protocol (same as Step 6.5-6.6). Verification round on fidelity fixes. Max 2 fix cycles.
  - [ ] If fidelity issues persist after max 2 fix cycles: HALT, present to user.

Step 6.7b: Anti-omission gate (source→output completeness, PARALLEL): MANDATORY
  - [ ] Spawn rf-analyst (anti-omission-agent-1, fix_authorization: false): assigned the first half of the research + synthesis files. ENUMERATE every distinct finding/claim/recommendation/item in the assigned files, then verify EACH is represented (semantically) in the final report. CRITICAL METHOD: judge coverage by MEANING, never by ID/reference-citation; the report absorbs findings without citing their source IDs, so an ID-membership test is invalid and both over- and under-reports. A finding whose substance appears nowhere in the report = OMISSION. Rate each omission by importance (a dropped distinct finding/discipline = IMPORTANT or CRITICAL; a legitimately deduped restatement is NOT an omission, note it as covered-by-dedup). Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-anti-omission-report-1.md`
  - [ ] Spawn rf-analyst (anti-omission-agent-2, fix_authorization: false): assigned the second half of the research + synthesis files; same exhaustive enumerate-and-verify method, same output format. Output: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/qa/qa-anti-omission-report-2.md`
  - [ ] If the research + synthesis files exceed ~1000 lines total: spawn 3-4 anti-omission agents instead of 2, partitioning the files across agents so the enumeration is EXHAUSTIVE, never a spot-check. (They exceed 1000 lines here: partition to 4 agents.)
  - [ ] Consolidate anti-omission findings (each unrecovered, unjustified omission is a blocking finding; minor findings stay as notes). For EACH omission: either RECOVER it (the single fix agent adds the dropped finding to the report) or EXPLICITLY JUSTIFY it as intentional dedup / out-of-scope (recorded in the consolidated findings). NEVER silently drop an omission. Apply via the serialized fix protocol (report-only agents → consolidate → single fix agent → verification round). Max 2 fix cycles, then HALT and present to user.
  - [ ] This gate is the INVERSE of Step 6.7 (fidelity verifies output→source: no fabrication/distortion; anti-omission verifies source→output: no dropped finding). BOTH are mandatory; passing fidelity does NOT imply completeness.

- Every blocking finding must be resolved before Phase 7; minor findings are recorded as notes and do not block.

Phase 7 — Present to User & Complete Task:
- Present summary to user (report location, key findings, recommendation, research file count, open questions)
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- `NON-BLOCKING` Suggest downstream skill: "This research can feed directly into a Technical Reference document. You can create one using `/tech-reference` — the research files are already in place and will accelerate the process." Present the suggestion, mark this item complete immediately, and do NOT wait for a user response. This item does not gate task completion.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, report structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115.md using PART 2 structure
7. Return the task file path
