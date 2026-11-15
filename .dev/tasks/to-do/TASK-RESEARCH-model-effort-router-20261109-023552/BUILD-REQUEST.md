# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Investigate issue #463's intelligent model-plus-effort routing feasibility, including the public alex4o/cliproxy-effort-router source, relevant alternatives, unresolved Jev identity, session selection versus per-request decisions, decision-model overhead/privacy, effort/provider contracts and actual local integration/caller/test boundaries. Produce `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/RESEARCH-REPORT-model-effort-router.md` with verified findings, gaps, options and proportionate recommendations. No architecture is preselected.
WHY: The owner needs evidence before deciding what to build. Preserve explicit user choices and issue #462's user's configured Coder-role default, not a universal Tier1b product default. This task ends with completed independently gated research; a later ordinary checked implementation plan is conditional on supported findings, and no implementation is authorized.
TASK_ID_PREFIX: TASK-RESEARCH
TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
Scope03 flags README's unconditional-looking 500 passthrough wording: overload-body errors are a switch exception. Scope02/04 flag fixed role-to-Tier1b prose if interpreted universally: actual policy is parameterized and eligible inherited named models may precede default-tier. Live Coder policy, provider capabilities/prices/scores and real client merge/resume/version behavior remain UNVERIFIED. Do not use these claims as known architecture; encode investigations that resolve them. Every doc-sourced claim needs CODE-VERIFIED, CODE-CONTRADICTED or UNVERIFIED labeling against direct source evidence.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
Phase 2: L1 Discovery, five independent deeper local investigations specified in research notes, concurrently.
Phase 3: L4 Review/QA, independent full research completeness gate, partitioned workloads and serialized blocking fixes.
Phase 4: L1 Discovery, three gap-driven external investigations, concurrently after local gate PASS.
Phase 5: L2 Build-from-Discovery, four synthesis outputs, then independent full synthesis gate and serialized blocking fixes.
Phase 6: L6 Aggregation, dedicated rf-assembler, structural/content/domain lenses, source fidelity and exhaustive meaning-based anti-omission gates.
The installed tech-research Skill defines exact full prompts and checklist bodies; read and embed those, not a summary of them. Coordinator-owned Orca workers implement every specified role at verified claude-gw-tier1b. This dispatched worker cannot create children and must request each wave from its coordinator, never use native Agent aliases or change definitions/settings.

QA_INTENSITY: full
QA_GATE_REQUIREMENTS: PER_PHASE
Gate 1: Research completeness, 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative minimum. When >6 research input files, partition EACH lens into bounded subsets and numbered outputs, then merge. Preserve coverage of all relied-on scope inputs.
Gate 2: Synthesis quality, same five independent role/lens minimum; partition EACH lens when >4 synthesis files.
Gate 3: Final report, default 4 rf-qa structural lenses (template, consistency, evidence, completeness), 4 rf-qa-qualitative content lenses (actionability, numbers, cross-reference chain, domain accuracy), 3 domain lenses (recommendation feasibility, finding reproducibility, implementation concreteness). Apply source Skill's size scaling without dropping mandatory dimensions.
Gate 4: Source fidelity after Gate 3; four independent rf-qa workers for >1000 source lines, partition actual source files/ranges, each reads full report.
Gate 5: Exhaustive anti-omission after fidelity; two rf-analyst workers, partition to three or four if research+synthesis exceed about 1000 lines. Enumerate EVERY distinct finding, judge by meaning, recover omissions or explicitly justify dedup/out-of-scope.
All reviewers start adversarial, report-only with fix_authorization false, binary PASS/FAIL and blocking/minor classification; zero findings requires a self-audit. Consolidate all reports BEFORE a single serialized fix writer; independently verify fixes. At most two fix cycles per gate, then HALT/escalate unresolved blocking findings. Minor notes do not fail or trigger a fix cycle. No gate replaced by producer self-review. The actual task executor adds its own phase gates.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
All ten report sections present or N/A with reason. Every technical claim cites current local source or pinned public source; scope notes are discovery leads, not substitute final proof. Separate source-inspected assertions from executed behavior. Explicitly retain UNVERIFIED gateway/client/live deployment and unmeasured quality/cost/latency. Preserve intermediates and the installation incident. Reports read governing templates, stub full skeleton first, then populate in place. Read chunks under 100 lines and tool output under 40 lines. No tests, paid calls, installs, package commands, configuration or source/test mutations, cleanup, commits, pushes, PRs, merge, Slack posts or unrelated GitHub writes. Public research must never interact with SuperClaude-Org. This repo's gh calls always name IronbellyOrg/IronClaude. Stage `.dev/tasks`, never `.dev/issues` or generated `.claude` mirrors.
TESTING_REQUIREMENTS: N/A - research documentation only. No test execution authorized.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/research/research-notes.md

SKILL CONTEXT FILE:
/home/coder/.claude/skills/tech-research/SKILL.md

CRITICAL - GRANULARITY REQUIREMENT:
One self-contained template B2 checklist item for EACH of five local investigators, three web topics, four synthesis files, every independent lens reviewer, each consolidation/fix/verification step, assembler, fidelity partition and anti-omission partition. Do not collapse a wave into one batch item. Embed COMPLETE applicable prompts, source/output paths, verification clauses, incremental-writing and staleness protocols from the installed tech-research Skill. Parallel waves remain concurrent through the coordinator's verified Tier1b worker-start launches; encode the owner override rather than an unusable native Agent fallback.

ESCALATION:
No nested workers or native aliases. Independent roles are launched by coordinator terminal term_4db4c124-3b58-4b9e-be54-c53aed3ceac8 through Orca worker-start at verified claude-gw-tier1b; this worker requests exact role/input/output briefs through its existing dispatch. Do not edit installed agents or global model settings. On missing required template/source, record blocker and ask coordinator, never fabricate. On blocked source access, distinguish evidence limitation from user intent. Preserve all intermediate outputs and do not broadcast native TASK_READY or use nonexistent team machinery. Return the actual task file path through the supervising workflow.

Owner execution constraint: these issues and ALL subsequent sessions/helpers run Tier1b, NOT Opus 5.5 or Tier1a. Scope03 accidentally used project-aware UV to inspect transcript metadata, creating `.venv`, building the project and installing 27 dependencies. Preserve environment/disclosure, no cleanup or further package commands. Do not claim no installs occurred.

SKILL PHASES TO ENCODE IN TASK FILE:
Read the complete installed tech-research A.7 phase definitions and Agent Prompt Templates before drafting. Encode every required step, prompt and output, without reducing the process to the phase labels below.

1. Preparation: mark Doing, reuse this existing package, create required research/synthesis/qa/reviews subfolders without duplicating or deleting existing artifacts.
2. Deep investigation: five concurrent separate assignments from research-notes SUGGESTED_PHASES; full Codebase Research Agent Prompt and per-agent evidence/output criteria. Scope files are inputs, not a replacement for deeper investigation.
3. Completeness: separate completeness/cross-validation analysts, evidence/gap QA and depth qualitative lens, partition each as required. Read all reports; consolidate; single authorized blocking fix agent with any needed targeted researchers through coordinator; independent structural/qualitative recheck, maximum two cycles. Compile gaps-and-questions. PASS before web.
4. Web: three separate concurrent gap-driven assignments from notes, each with full Web Research Agent Prompt. Primary/pinned source review, no installs/execution/paid calls. Explicit Jev identity uncertainty if unresolved.
5. Synthesis: four separate files mapped in notes, full Synthesis Agent Prompt. Then accuracy/tracing analysts, structure/content QA, coherence qualitative reviewers, full corresponding checklists, partition if required, consolidated serialized blocking fixes and independent verification. PASS before assembly.
6. Assembly: single dedicated rf-assembler reads all four synth files in order, full Report Structure, Assembly Process and Content Rules. Then all report structural/content/domain lenses, consolidation, single fix log and independent verification. Then four partitioned source-fidelity reviewers with full report, serialized fixes and rechecks. Then exhaustive anti-omission reviewers with actual size-based partitioning, recovery or explicit justified dedup, serialized fixes and verification. Every blocking finding resolved before completion; all intermediates retained.
7. Present and complete: report actual report path, key findings, recommendation, research count and unresolved questions; final task log and status only after every applicable gate. Any downstream reference-document suggestion is nonblocking and grants no extra execution. This research task does not implement product changes. Parent may create the smallest ordinary checked implementation plan only if completed findings support it, then stops.

TASK FILE LOCATION:
.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/TASK-RESEARCH-model-effort-router-20261109-023552.md

STEPS:
1. Read the complete research notes and four scope inputs from disk in bounded chunks.
2. Read installed `/home/coder/.claude/skills/tech-research/SKILL.md` for exact prompts, report skeleton, mapping, full checklists, content rules and assembly procedure. Global skill copy takes precedence; project `.claude/skills/tech-research/SKILL.md` is fallback only.
3. Read Template 02 from project `.claude/templates/workflow/02_mdtm_template_complex_task.md`, or installed `/home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md` if project copy absent. Never invent missing template content.
4. Follow template Part 1 completely, including complete granular breakdown, full self-contained prompt bodies and flat checklist structure. Stub Part 2 skeleton before populating task.
5. Note unresolved evidence gaps honestly in task log. No unsupported design or fabricated source paths.
6. Write the actual task at TASK FILE LOCATION, preserve package identity and read/write limits, and return its path for task-builder's independent gates.
7. After actual task-builder returns TASK_FILE_READY, parent must invoke actual task Skill with the validated path and continue, not stop at builder success.
