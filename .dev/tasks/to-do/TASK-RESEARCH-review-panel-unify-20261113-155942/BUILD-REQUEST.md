# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation comparing three Review Panel efforts (E1 = this session's reflect Tier 2 panel kernel, shadow mode and model-combination experiment on branch ironbelly/shadow-runs; E2 = the other session's tasklist review-panel evaluation study on origin/ironbelly/eval-tasklist-review-panel at commit 4a22d74213f93837d00c2c314075dd967b9a98e3; E3 = the #346 review-loop infrastructure on master: findings-v1, ledger, review merge/ledger/panel/telemetry CLI, spec-panel Review Loop and the installed-only experiment variants) and recommend one unified central Review Panel design. Produce a structured research report with findings, gap analysis, options, and implementation recommendations. The report will be written to `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md`.

The report MUST contain: (a) a component-by-component overlap matrix across E1/E2/E3 (same purpose, same data contract, same code, divergent choices); (b) a value inventory: every finding, lesson, strategy, defect, script, test and artifact from all three, each mapped to a destination in the unified design or an explicit drop with a reason; (c) a conflict log: every disagreement (finding schema and severities, anchor handling at merge, model and tier configuration, who judges, calibration, how runs are recorded, the 200-character anchor drop and the other defects D1-D16), the options, and a recommended resolution with evidence; (d) the target architecture: a shared core (finding contract, panel resolution, run manifest, clustering and citation checks, calibration, merge, telemetry) with thin per-use-case modules (sc:reflect, sc:workflow tasklist review, spec review for sc:brainstorm and sc:design, PR code review, rf-qa / rf-qa-qualitative replacement); (e) a future-use-case check: for PR code review and rf-qa replacement, what the core must expose (lenses, categories, roles, templates, model-role mapping) so adding them needs no core change, and anything in today's designs that would block them.

WHY: The owner wants one central Review Panel serving sc:reflect (Tier 2 shadow, then panel), sc:workflow tasklist review, spec review from sc:brainstorm and sc:design, and later PR code review and replacement of rf-qa style agents, such that ALL value from both sessions and master is captured, overlap is evaluated, merged and de-duplicated, conflicts are resolved, and future use cases are not hindered by the final shape. OWNER SCOPE CHANGE (2026-11-13): this task produces the REPORT ONLY. It must NOT run /sc:workflow and must NOT build a roadmap. The report will later be merged with the other session's second tech-research report via /sc:adversarial --compare --merge, and only then will a roadmap be built. Section 8 is therefore a value-capture and migration plan (value inventory mapping, migration path for reflect shadow and the tasklist panel onto the core, no-regression gate list, branch-structure options including the git constraint that feat/review-panel and feat/review-panel/<name> cannot both exist), not a roadmap.

TASK_ID_PREFIX: TASK-RESEARCH

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
Found during scope discovery (details in research-notes.md AMBIGUITIES_FOR_USER and scope slices):
- [CODE-CONTRADICTED] E2 hand-off says the experiment variants (sc-review-ledger, stoprule, finding-grader, diffgate, fix-audit, spec-panel-* variants) exist only in `.dev/experiments/346-validation/phase5/final-bundle/`; they are also installed globally in `~/.claude/` (not in `src/` and not in project `.claude/`).
- [CODE-CONTRADICTED] E2 hand-off cites audits B, C, E, F; only audits A and D have `summary.md` at 4a22d742; audit D names 3 verdict flips, not 4; the once-found issue is alias GT1 (B6), not alias GT3.
- [CODE-CONTRADICTED, minor] stale line numbers in the hand-off: D11 is now `panel.py:536-543`, D12 `panel.py:485-494`, D7 `telemetry.py:22`; behaviour unchanged.
- [CODE-CONTRADICTED] `ledger.merge_round` docstring (`ledger.py:112`) says an invalid reviewer is skipped for clearing; the clearing loop (:254-258) does not check validity (this is D2).
- [CODE-CONTRADICTED within docs] reflect SKILL.md §7 calls `reflect-reviewer` a UC-2 reviewer while §7.1 uses it for all Tier 2 reviewers including UC-1 shadow; calibrator agent is written for a 6-dimension troubleshoot rubric while reflect uses a 5-dimension rubric.
Phase 2 agents will perform full documentation cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags.
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only). Serialized fix: consolidate findings → single fix agent → verification round. Partitioning >6 files.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce report sections. Then spawn 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only). Serialized fix: consolidate → fix → verify. Partitioning >4 files.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final report. Then lens-based multi-agent QA: 3-5 rf-qa (structural lenses) + 3-5 rf-qa-qualitative (content lenses) + 3 domain-specific lenses (recommendation feasibility, finding reproducibility, implementation plan concreteness). All report-only. Serialized fix: consolidate → single fix agent → verification. Then source-document fidelity gate: 2-4 rf-qa fidelity agents reading codebase source files + full report. Then the anti-omission gate (Step 6.7b): 2-4 rf-analyst agents that exhaustively enumerate every distinct finding in the research + synthesis files and verify each is represented in the report (source→output completeness, the inverse of the fidelity gate).

ADDITIONAL OWNER-REQUIRED STEP (encode in Phase 5, between the synthesis agents for synth-04 and synth-05):
- Adversarial conflict resolution. After synth-04 (conflict log) is written, one checklist item reads synth-04 and lists every conflict marked `UNDECIDED-BY-EVIDENCE`. For EACH such conflict, one checklist item: write two design proposals to `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/reviews/adversarial/<conflict-slug>/proposal-a.md` and `proposal-b.md` (each grounded in the research files with citations), then invoke the Skill tool with skill `sc:adversarial` and args `--compare <proposal-a path>,<proposal-b path> --depth standard --focus correctness,risk,test-coverage --output .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/reviews/adversarial/<conflict-slug>/`, then write the debate result (winner, reasons, residual risks, output path) back into that conflict's row in synth-04. Because the number of undecided conflicts is not known until synth-04 exists, encode this as: one item to enumerate conflicts and append one item per conflict to the Task Log as a dynamic sub-checklist, then items that process them in order. If none are undecided, one item records "no adversarial run needed" with the reason. synth-05 must not start until this step is complete.
- Phase 5 synthesis order therefore: synth-01, synth-02, synth-03, synth-04 and synth-07 in parallel; then the adversarial step; then synth-05; then synth-06 (it needs synth-04 and synth-05); then the synthesis QA gate.

QA_INTENSITY: full  (per I22 — Deep tier default)
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
  Anti-omission inputs for this task additionally include the five scope slices `research/scope/01..05-*.md` and `research/scope/00-handoff-copy.md`, because the value inventory (b) must cover every item they list.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All report sections must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  REQUIRED-CONTENT CHECK: the report contains (a) overlap matrix, (b) value inventory with a destination or a drop reason for every row, (c) conflict log with options and a recommended resolution per conflict, (d) target architecture with shared core and thin modules, (e) future-use-case exposure list and blockers. Missing any one is a blocking finding.

TESTING_REQUIREMENTS: N/A — documentation-only skill (research reports), no code produced, no tests applicable. Agents may run read-only commands (`uv run python scripts/reflect_shadow_exit.py`, `uv run pytest --collect-only -q tests/review tests/cli/reflect`) to gather evidence; they must not edit source, tests or `.claude/`.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/research/research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments, synthesis mapping, and output paths.

SKILL CONTEXT FILE:
.claude/skills/tech-research/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Report Structure" section for final report format (includes full sub-section scaffolding). Read the "Synthesis Mapping Table" section for the standard synth-file-to-report-section mapping. Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for report assembly steps. Read the "Validation Checklist" section for Phase 6 validation criteria. Read the "Content Rules" section for writing standards. These must be embedded in the relevant checklist items per B2 self-contained pattern.
NOTE: this task uses a 7-file Deep-tier synthesis mapping (see research notes Phase 5 table), not the 6-file standard table: synth-04 = S6 conflict log, synth-05 = S7 target architecture + exposure list, synth-06 = S8 value inventory + migration plan, synth-07 = S9 + S10.

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
- **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
- **External docs/syntax** → use WebSearch
- **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.

SKILL PHASES TO ENCODE IN TASK FILE:
The task file MUST encode these phases as sequential checklist items. Each phase maps to a section of the skill's workflow. All items MUST follow the B2 self-contained pattern from the MDTM template.

Phase 1 — Preparation:
- Update task status to "🟠 Doing"
- The task folder already exists at .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/ with `research/`, `synthesis/`, `qa/`, `reviews/` subfolders; verify them (and run `git fetch origin` so E2 files are readable via `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:<path>`)

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (12 agents, from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type, files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.

Phase 3 — Research Completeness Verification (5-AGENT GATE + SERIALIZED FIX):

Step 3.1: Spawn lens-based research gate agents (PARALLEL, all fix_authorization: false)
  - [ ] Spawn rf-analyst (completeness lens) — reads all research files, applies coverage audit + completeness + cross-reference checks from 8-item checklist. Writes to `${TASK_DIR}qa/analyst-completeness-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (cross-validation lens) — reads all research files, applies contradiction detection + gap compilation + depth assessment checks. Writes to `${TASK_DIR}qa/analyst-cross-validation-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (evidence-quality lens) — reads all research files, applies file inventory + evidence density + scope coverage + doc cross-validation checks from 10-item checklist. Writes to `${TASK_DIR}qa/qa-research-evidence-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (gap-detection lens) — reads all research files, applies gap severity + depth appropriateness + integration points + pattern documentation + incremental writing checks. Writes to `${TASK_DIR}qa/qa-research-gaps-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (research-depth lens) — reads all research files, evaluates whether findings are genuinely deep or superficial. Writes to `${TASK_DIR}qa/qa-research-qualitative-report.md`. Embed full prompt per B2.
- **Parallel partitioning for large workloads:** 12 research files > 6, so EACH of the 5 agent types gets partitioned into 2 instances with `assigned_files` subsets (files 01-06 and 07-12) = 10 parallel agents writing numbered reports. Merge after completion.

Step 3.2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 3.1, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase3.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated blocking findings (minor findings stay as notes). Fix agent spawns additional targeted research agents for blocking gaps requiring new research (one per gap). Applies all blocking fixes.
  - [ ] Spawn rf-qa (verification, fix_authorization: false) + rf-qa-qualitative (verification, fix_authorization: false) to confirm fixes applied correctly
  - [ ] If verification finds new blocking issues (new minor findings are notes and do not restart the cycle): repeat Step 3.2 (max 2 cycles total). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log issues in Task Log

- Compile final gaps into ${TASK_DIR}gaps-and-questions.md (merged from all reports)
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (4 topics W1-W4 from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Adversarial step + Synthesis QA Gate:
- One checklist item PER synthesis file (7 files from research notes RECOMMENDED_OUTPUTS), in the order given in ADDITIONAL OWNER-REQUIRED STEP above
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md
- Each item specifies: research files to read, report sections to produce, output path, and which of the required contents (a)-(e) it carries

Step 5.N+1: Spawn lens-based synthesis gate agents (PARALLEL, all fix_authorization: false)
  - [ ] Spawn rf-analyst (synthesis-accuracy lens). Writes to `${TASK_DIR}qa/analyst-synthesis-accuracy.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (source-tracing lens). Writes to `${TASK_DIR}qa/analyst-synthesis-tracing.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (structure lens). Writes to `${TASK_DIR}qa/qa-synthesis-structure.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (content-quality lens). Writes to `${TASK_DIR}qa/qa-synthesis-content.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (synthesis-coherence lens). Writes to `${TASK_DIR}qa/qa-synthesis-qualitative-report.md`. Embed full prompt per B2.
- **Parallel partitioning:** 7 synth files > 4, so each agent type is partitioned into 2 instances (synth 01-04 and 05-07).

Step 5.N+2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 5.N+1, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase5.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated blocking findings (minor findings stay as notes). Fixes blocking issues in synth files in-place.
  - [ ] Spawn rf-qa (verification) + rf-qa-qualitative (verification) to confirm fixes
  - [ ] If blocking issues remain: repeat (max 2 cycles total), then HALT

- Do NOT continue to Phase 6 without PASS verdict.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + LENS-BASED QA + FIDELITY GATE + ANTI-OMISSION GATE): encode Steps 6.1, 6.2 (4 structural lenses), 6.3 (4 content lenses), 6.4 (3 domain lenses), 6.5 (consolidate + single fix agent), 6.6 (verification round, max 2 cycles), 6.7 (fidelity gate: 3-4 rf-qa agents because source > 1000 lines), 6.7b (anti-omission gate: 3-4 rf-analyst agents because research + synthesis + scope slices > 1000 lines) exactly as written in SKILL.md section A.7. Report output path: `${TASK_DIR}RESEARCH-REPORT-review-panel-unification.md`.

Phase 7 — Present to User & Complete Task:
- Present summary to user (report location, key findings, recommendation, research file count, open questions)
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- Do NOT run /sc:workflow, do NOT build a roadmap, and do NOT suggest /tech-reference as a next step. Instead record in the Task Log that the next step owned by the session is: commit and push this task folder (no PR), then wait for the other session's second report and merge the two via /sc:adversarial --compare --merge before any roadmap.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/TASK-RESEARCH-review-panel-unify-20261113-155942.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, report structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/TASK-RESEARCH-review-panel-unify-20261113-155942.md using PART 2 structure
7. Return the task file path
