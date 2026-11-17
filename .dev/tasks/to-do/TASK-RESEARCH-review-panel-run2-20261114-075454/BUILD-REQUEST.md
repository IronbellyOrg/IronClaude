# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation of three overlapping review efforts (E1: reflect Tier 2 panel kernel, shadow mode and the model-combination experiment on branch `ironbelly/shadow-runs`; E2: the tasklist review-panel study, collaboration designs and process-redesign brainstorms on `origin/ironbelly/eval-tasklist-review-panel` at tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`; E3: the #346 review loop on master plus the installed-only experiment variants in `~/.claude/`) and produce a structured research report that recommends ONE unified central Review Panel design: a shared core with thin modules for sc:reflect (Tier 2 shadow, then panel), sc:workflow and tasklist review, spec review from sc:brainstorm and sc:design, and later PR code review and rf-qa / rf-qa-qualitative replacement. The report must contain: (a) an overlap matrix across E1, E2, E3; (b) a value inventory in which every finding, lesson, strategy, defect, script, test, artifact and question is mapped to exactly one destination (core, a named module, evaluation, harness, knowledge, or DROP with the reason); (c) a conflict log in which conflicts the evidence cannot decide are resolved by `/sc:adversarial --compare` debates and conflicts the evidence does decide are decided without a debate; (d) a target architecture (shared core plus thin modules); (e) a future-use-case exposure check showing that the final shape does not block PR code review, rf-qa replacement or later reviewers. The report will be written to `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md`.

OWNER SCOPE CHANGE (binding): REPORT ONLY. Do not build a roadmap, branch plan, PR plan or risk register in this task. Section 8 of the report holds the value inventory (8.1) and the sequence-and-gates inputs for a later plan (8.2: constraints, no-regression gates such as the byte-identical reflect contract 1.8.0 and the git ref constraint that `feat/review-panel` and `feat/review-panel/<name>` cannot both exist), not a roadmap. A later, separate step (`/sc:adversarial --compare --merge` on this report and an independent first report, then `/sc:workflow --depth standard --handoff none`) builds the plan. This task also performs no implementation, merge, worktree creation, branch creation or push.

INDEPENDENCE (binding): this report must stay independent of the first run's report. No agent reads, lists, greps into or cites `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`. Repo-wide searches exclude `.dev/tasks/` (use a `!.dev/tasks/**` glob or an explicit path list); `git log` calls exclude it (`-- ':!.dev/tasks'`). One earlier slip is on record: slice 03 gap 10 (file names printed, no content opened). Embed this rule in every checklist item.

WHY: The owner wants all value from three overlapping efforts captured in one central Review Panel, with overlap evaluated and de-duplicated, conflicts resolved, and future use cases (PR code review, rf-qa replacement) not hindered by the final shape. The findings will feed an adversarial comparison and merge with a second, independent report, and then an implementation plan. The report must therefore be exhaustive (the anti-omission gate is mandatory), faithful to the code, and explicit about what the evidence does not show.

TASK_ID_PREFIX: TASK-RESEARCH

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
Scope discovery found documentation claims that contradict code, or that could not be checked. The full list is in the research notes section AMBIGUITIES_FOR_USER (13 [CODE-CONTRADICTED] rows and a list of [UNVERIFIED] claims). Examples: the E2 hand-off attributes the review-package changes to #519 + #518 although #518 changes no `cli/review` file; E2's `COMBO-REPORT.md:292` says findings are discarded "with no error" and reports "four verdict flips" (code emits a warning with the first error; the audit enumerates 3 flips); the E2 run-2 reflect contrast ("reflect has no panel/tier code") is stale at HEAD. Do NOT create task items that build on these claims. Phase 2 agents perform full cross-validation with CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED tags.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 2 (Deep Investigation): L1 Discovery — 24 agents (18 topic agents + 6 value-ledger agents) explore the code and git history and write findings files to `${TASK_DIR}research/`. The harness refuses more than 20 concurrent subagents: items 01-18 are wave 1; items 19-24 are wave 2 and start when slots free. Do not create an item that spawns all 24 at once.
- Phase 3 (Completeness Verification): L4 Review/QA — 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only), partitioned because there are more than 6 files. Serialized fix: consolidate findings → single fix agent → verification round.
- Phase 4 (Web Research): L1 Discovery — 4 agents write `research/web-01..04-*.md`.
- Phase 5 (Synthesis + QA Gate + conflict adjudication): L2 Build-from-Discovery — 10 synthesis files. Then 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (partition above 4 files), serialized fix. Then a conflict-adjudication step BEFORE assembly: for every conflict in `synth-06-conflict-log.md` that the evidence cannot decide, write `proposal-a.md` and `proposal-b.md` under `${TASK_DIR}reviews/adversarial/<conflict-slug>/` and invoke `/sc:adversarial --compare <a>,<b> --depth standard --focus correctness,risk,test-coverage --output <that folder>` (never `--merge`); fold the winners and any unaddressed invariants back into synth-06 and synth-07.
- Phase 6 (Assembly & Validation): L6 Aggregation — rf-assembler consolidates the synthesis files into the final report. Then lens-based multi-agent QA: 3-5 rf-qa (structural) + 3-5 rf-qa-qualitative (content) + 3 domain lenses (recommendation feasibility, finding reproducibility, implementation plan concreteness; for this report-only task the third lens checks that Section 8.2 names concrete gates, files and constraints), all report-only; if the report exceeds 3000 lines each lens runs as two instances (a and b). Serialized fix. Then the source-document fidelity gate (4 agents, report against the code and the E2 tip). Then the anti-omission gate (4 rf-analyst; exhaustive; by meaning; against research files 01-24 including the six value ledgers, and all synthesis files).

QA_INTENSITY: full
QA_GATE_REQUIREMENTS: PER_PHASE
  **NOTE: Gate descriptions below specify FULL intensity agent counts.**
  Gate 1: Research Completeness (Phase 3)
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >6 files.
  Gate 2: Synthesis Quality (Phase 5)
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >4 files.
  Gate 3: Report Validation (Phase 6)
    - full: 3-5 rf-qa + 3-5 rf-qa-qualitative (scaled by report size per I19) + 3 domain lenses (recommendation-feasibility, finding-reproducibility, implementation-plan-concreteness) = 9-13 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, after Gate 3)
    - full: 2 rf-qa fidelity agents (partition to 3-4 if source >1000 lines). Max 2 fix cycles. HALT after max cycles exceeded.
  Gate 5: Anti-Omission (Phase 6, after Gate 4): MANDATORY at every intensity
    - full: 2 rf-analyst anti-omission agents (partition to 3-4 if research+synthesis >1000 lines). Max 2 fix cycles. HALT after max cycles exceeded.
    - Method: exhaustive enumeration (not spot-check); judge coverage by MEANING, never by ID/reference-citation; every omission is recovered or explicitly justified as dedup/out-of-scope, never silently dropped.
  Halt precedence on every gate: regression, then monotonicity (`[HALT-MONOTONICITY] |F|=<n>`), then the hard cap (2 fix cycles = 3 reviews). Minor findings are notes and never fail a review or trigger a fix pass.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All report sections must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.

TESTING_REQUIREMENTS: N/A — documentation-only skill (research reports), no code produced, no tests applicable. Research agents may run read-only recounts with `uv run python` and the reflect and review test suites with `-p no:cacheprovider` only where an item says so.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/research/research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments (SUGGESTED_PHASES lists all 24 Phase 2 agents with inputs, open items and output paths, the 4 web topics, the 10 synthesis files, the Phase 5 conflict-adjudication step, and the shared rules every research agent receives), solution approaches, and output paths. The 12 scope slices in `research/scope/` hold the exact file:line inventories that each Phase 2 agent reads first.

SKILL CONTEXT FILE:
.claude/skills/tech-research/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Report Structure" section for final report format (includes full sub-section scaffolding). Read the "Synthesis Mapping Table" section for the standard synth-file-to-report-section mapping (this task uses the extended 10-file mapping in the research notes). Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for report assembly steps. Read the "Validation Checklist" section for Phase 6 validation criteria. Read the "Content Rules" section for writing standards. These must be embedded in the relevant checklist items per B2 self-contained pattern.

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process
Structure), you MUST create individual checklist items for EVERY research agent,
web research topic, synthesis file, conflict debate, and validation step. Do NOT create batch items
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
- The task folder `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/` already exists with `research/`, `synthesis/`, `qa/`, `reviews/` subfolders and `research/scope/` (12 completed slice files); verify and do not recreate.

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY, in two waves because of the 20-subagent limit):
- One checklist item PER research agent (24 items from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type, slices and files to read, open items to resolve, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) and the shared rules block (read-only, git-only access to the E2 tip, independence rule, stub-first, tags) in each checklist item per B2
- Wave 1 = items 01-18 spawned in parallel using multiple Agent tool calls in a single message; wave 2 = items 19-24 spawned in parallel when slots free. Mark each item complete as it returns; output files persist on disk if context limits are reached.

Phase 3 — Research Completeness Verification (5-AGENT GATE + SERIALIZED FIX):

Step 3.1: Spawn lens-based research gate agents (PARALLEL, all fix_authorization: false)
  - rf-analyst (completeness lens) → `${TASK_DIR}qa/analyst-completeness-report.md`
  - rf-analyst (cross-validation lens) → `${TASK_DIR}qa/analyst-cross-validation-report.md`
  - rf-qa (evidence-quality lens) → `${TASK_DIR}qa/qa-research-evidence-report.md`
  - rf-qa (gap-detection lens) → `${TASK_DIR}qa/qa-research-gaps-report.md`
  - rf-qa-qualitative (research-depth lens) → `${TASK_DIR}qa/qa-research-qualitative-report.md`
  - More than 6 research files exist (24 + 4 web later), so EACH of the 5 agent types is partitioned into multiple instances with `assigned_files` subsets and numbered reports; merge after completion. Respect the 20-agent concurrency limit. Embed full prompts per B2.
  - Gate focus for this task: every Phase 2 claim has file:line evidence; every slice gap is resolved or logged; no run-1 contamination (no reference to the run-1 folder or the RUN2-QUEUED note in any research file); every value-ledger row has exactly one destination.

Step 3.2: Consolidate findings and apply fixes (SERIALIZED)
  - Consolidate ALL reports into `${TASK_DIR}qa/qa-consolidated-findings-phase3.md`
  - rf-qa fix agent (fix_authorization: true) with consolidated blocking findings (minor findings stay as notes); it may spawn targeted research agents for blocking gaps (one per gap)
  - rf-qa verification + rf-qa-qualitative verification (fix_authorization: false)
  - If verification finds new blocking issues, repeat Step 3.2 (max 2 cycles total). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings
- Compile final gaps into `${TASK_DIR}gaps-and-questions.md`
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (4 items: W1 multi-model review evidence, W2 Claude Code hooks and headless semantics, W3 git branch hierarchy and stacked PRs, W4 finding schemas and review bots; details in research notes SOLUTION_RESEARCH)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md, specifies topic, context from codebase findings, output file path (`research/web-01..04-*.md`)

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate + Conflict adjudication:
- One checklist item PER synthesis file (10 items from research notes SUGGESTED_PHASES synthesis table; synth-06 and synth-08 are the conflict log and value inventory)
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md and specifies research files to read, report sections to produce, output path
- Synthesis QA gate (5 lens agents, partitioned above 4 files): rf-analyst synthesis-accuracy, rf-analyst source-tracing, rf-qa structure, rf-qa content-quality, rf-qa-qualitative synthesis-coherence; consolidate → `qa/qa-consolidated-findings-phase5.md` → single fix agent → verification (max 2 cycles, then HALT)
- Conflict adjudication step (after the gate passes, before Phase 6): one checklist item PER undecidable conflict, each running `/sc:adversarial --compare` as described in the pattern mapping above; launch in batches within the 20-subagent limit; one consolidation item folds the results into synth-06 and synth-07 and re-checks that no HIGH unaddressed invariant is silently dropped (list remaining ones as open questions)
- Do NOT continue to Phase 6 without PASS verdict

Phase 6 — Assembly & Validation (RF-ASSEMBLER + LENS-BASED QA + FIDELITY GATE + ANTI-OMISSION GATE):
- Step 6.1: single dedicated `rf-assembler` builds `${TASK_DIR}RESEARCH-REPORT-review-panel-unification-run2.md` from the 10 synthesis files in order, using the Report Structure, Assembly Process and Content Rules from SKILL.md
- Step 6.2-6.4: lens agents as in SKILL.md (4 structural, 4 content, 3 domain; scale per Gate 3; two instances per lens if the report exceeds 3000 lines), all report-only, outputs `qa/qa-lens-*.md`
- Step 6.5-6.6: consolidate → `qa/qa-consolidated-findings-phase6.md` → single fix agent (`qa/qa-fix-log.md`) → verification (max 2 cycles, then HALT)
- Step 6.7: source-document fidelity gate (4 agents partitioned across the code, git-tip and research sources) → consolidate, serialized fix, verification (max 2 cycles)
- Step 6.7b: anti-omission gate (4 rf-analyst, exhaustive, by meaning, partitioned over research files 01-24, web files and synthesis files) → consolidate, recover or justify each omission, serialized fix, verification (max 2 cycles, then HALT). Inverse of 6.7; both mandatory.
- Step 6.8: final validation checklist (`qa/final-validation-checklist.md`); every blocking finding resolved before Phase 7

Phase 7 — Present to User & Complete Task:
- Present summary to user (report location, key findings, recommendation, research file count, open questions, the owner decisions the report leaves open)
- Stage the task folder with `git add .dev/tasks` (staging only; do NOT commit and do NOT push; the owner's earlier commit-and-push instruction covered run 1 only) and never stage anything under `.claude/`
- Record in the task file the next steps in order: (1) the owner's word on committing and pushing this run, (2) `/sc:adversarial --compare --merge` on the two reports and duplicate materials, (3) `/sc:workflow "<…>" --depth standard --handoff none` on the merged document
- Write task summary to Task Log / Notes section (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- `NON-BLOCKING` Suggest downstream skill (`/tech-reference`); mark complete immediately; does not gate completion

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, report structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md using PART 2 structure
7. Return the task file path
