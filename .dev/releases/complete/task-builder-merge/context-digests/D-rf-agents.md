# Bucket D — rf-* agents content digest

## Files found (Glob)

| Path | Lines | Status |
|------|-------|--------|
| src/superclaude/agents/rf-task-builder.md | 493 | present |
| src/superclaude/agents/rf-task-researcher.md | 505 | present |
| src/superclaude/agents/rf-task-executor.md | 368 | present |
| src/superclaude/agents/rf-team-lead.md | 431 | present |
| src/superclaude/agents/rf-analyst.md | 349 | present |
| src/superclaude/agents/rf-qa.md | 432 | present |
| src/superclaude/agents/rf-qa-qualitative.md | 794 | present |
| src/superclaude/agents/rf-assembler.md | 241 | present |

## Files expected but absent

None. All 8 expected files present; line counts match expectations exactly.

## Per-agent digest

### rf-task-builder
- Purpose / role: Builds MDTM task files using Rigorflow methodology; works with researcher, hands off to executor (rf-task-builder.md:3, 28-30).
- Tools used: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, NotebookEdit, Task family, SendMessage, Skill, AskUserQuestion (rf-task-builder.md:6-25).
- Inputs expected: `BUILD_REQUEST` with GOAL, WHY, TEMPLATE (01 or 02), QA_GATE_REQUIREMENTS, VALIDATION_REQUIREMENTS, TESTING_REQUIREMENTS, RESEARCH_CONTEXT (rf-task-builder.md:88-99).
- Outputs produced: Task file at `.dev/tasks/to-do/TASK-RF-<timestamp>/TASK-RF-<timestamp>.md` (rf-task-builder.md:465-469); shared task entry + `TASK_READY` broadcast (rf-task-builder.md:200-226).
- Handoff: rf-team-lead → builder (BUILD_REQUEST), builder ↔ rf-task-researcher (RESEARCH_NEEDED / RESEARCH_READY), builder → rf-task-executor via TASK_READY broadcast (rf-task-builder.md:42-55, 200-226).
- Failure handling: BLOCKED to team-lead if template missing (rf-task-builder.md:77-78); NEED_USER_INPUT pause-and-wait pattern (rf-task-builder.md:140-155). No explicit retry budget.
- Validation/QA behavior: Encodes QA gate items per QA_GATE_REQUIREMENTS (NONE/FINAL_ONLY/PER_PHASE) with fix-cycle limits per gate type — research-gate 3 / synthesis-gate 2 / report-validation 3 / task-integrity 2 / qualitative 3 (rf-task-builder.md:336-359). Encodes validation + testing checklist items per VALIDATION_REQUIREMENTS / TESTING_REQUIREMENTS (rf-task-builder.md:360-376).
- Explicit invariants: Template-read-first is non-negotiable (rf-task-builder.md:57-81); incremental writing mandatory — frontmatter first, then one phase per Edit (rf-task-builder.md:168-196); A3/A4 per-file granularity (rf-task-builder.md:248-262); SKILL PHASES TO ENCODE > QA_GATE_REQUIREMENTS precedence (rf-task-builder.md:377-378).
- Key "do not" rules: Never one-shot the task file (rf-task-builder.md:473); never assume / leave placeholders (rf-task-builder.md:477-478); QA gates must be checklist items, not prose (rf-task-builder.md:482); a task file omitting required QA/validation/testing items is MALFORMED (rf-task-builder.md:482-484).

### rf-task-researcher
- Purpose / role: Explores codebase and provides context to teammates, primarily rf-task-builder (rf-task-researcher.md:3, 28-30).
- Tools used: Same Read/Write/Edit/Bash/Glob/Grep/WebFetch/WebSearch + Task/SendMessage/Skill stack as builder (rf-task-researcher.md:6-25).
- Inputs expected: `RESEARCH_REQUEST` from team-lead (GOAL + AREAS_TO_EXPLORE) or `RESEARCH_NEEDED` from builder; also `VERIFY_OUTPUT` from executor (rf-task-researcher.md:42-55, 60-90).
- Outputs produced: Research notes file (per Incremental File Writing Protocol) plus structured `RESEARCH_READY` payload with FILES FOUND / KEY EXPORTS / PATTERNS / TEMPLATES / CONTEXT FILES / POTENTIAL ISSUES (rf-task-researcher.md:130-162, 274-293).
- Handoff: team-lead → researcher (RESEARCH_REQUEST); builder ↔ researcher (RESEARCH_NEEDED / RESEARCH_READY / RESEARCH_PARTIAL); executor → researcher (VERIFY_OUTPUT) (rf-task-researcher.md:42-55).
- Failure handling: `RESEARCH_PARTIAL` for incomplete state; `BLOCKED` to team-lead when info unavailable (rf-task-researcher.md:42-46, 446-460). Escalation ladder: WebSearch → /rf:opinion → team-lead (rf-task-researcher.md:378-384).
- Validation/QA behavior: Documentation Staleness Protocol — tag every doc-sourced architectural claim `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` (rf-task-researcher.md:253-271).
- Explicit invariants: Incremental writing — create file first then append (rf-task-researcher.md:274-293); evidence-based claims only (rf-task-researcher.md:487); A3/A4 per-file granularity must be supported in notes (rf-task-researcher.md:239-249).
- Key "do not" rules: Do not modify source code (rf-task-researcher.md:491); do not assume / guess paths (rf-task-researcher.md:492-494); do not present doc claims as verified facts without code cross-validation (rf-task-researcher.md:496).

### rf-task-executor
- Purpose / role: Executes MDTM task files using `.gfdoc/scripts/automated_qa_workflow.sh`; receives handoff from builder, reports to team-lead (rf-task-executor.md:3, 30-32).
- Tools used: Standard set; loads `rf:task` skill (rf-task-executor.md:6-27).
- Inputs expected: `TASK_READY` (from builder) or `EXECUTE_REQUEST` (from team-lead) with path, batch size, max iterations (rf-task-executor.md:42-55, 65-91).
- Outputs produced: `EXECUTION_STARTED` / `EXECUTION_PROGRESS` / `EXECUTION_COMPLETE` / `EXECUTION_ERROR` broadcasts; shared task status updates; resulting task artifacts (rf-task-executor.md:50-57, 131-204).
- Handoff: builder → executor (TASK_READY); executor → team-lead (progress/completion/error); executor → researcher (VERIFY_OUTPUT optional) (rf-task-executor.md:42-57, 326-339).
- Failure handling: QA failure → correction loop up to 5 retries (rf-task-executor.md:212-222); `EXECUTION_ERROR` to team-lead with resume command and log path (rf-task-executor.md:225-239); blocked items logged and reported PARTIAL (rf-task-executor.md:243-256).
- Validation/QA behavior: Validates task file shape before claiming (frontmatter, `- [ ]` items, structure) (rf-task-executor.md:93-117); QA is owned by the workflow script itself (rf-task-executor.md:147-162).
- Explicit invariants: Never wrap script in timeout (4-hour built-in) (rf-task-executor.md:153, 343-345); never run in background unless asked; never interrupt mid-execution (rf-task-executor.md:153-156, 345-347).
- Key "do not" rules: Do NOT create task files / modify task structure / wrap in timeout / run multiple tasks simultaneously / skip validation (rf-task-executor.md:352-359).

### rf-team-lead
- Purpose / role: Orchestrates the RF team — spawns researcher, builder, executor; handles parallel tracks and project mode (rf-team-lead.md:3, 32-46).
- Tools used: Full set plus TeamCreate/TeamDelete and EnterPlanMode/ExitPlanMode (rf-team-lead.md:6-29).
- Inputs expected: User request; status broadcasts from teammates (rf-team-lead.md:80-90).
- Outputs produced: Team spawn calls (Task() per role); BUILD_REQUEST / RESEARCH_REQUEST / EXECUTE_REQUEST messages; final `RIGORFLOW PIPELINE COMPLETE` summary (rf-team-lead.md:54-75, 195-264).
- Handoff: lead → researcher (RESEARCH_REQUEST), lead → builder (BUILD_REQUEST after RESEARCH_READY), lead → executor (EXECUTE_REQUEST after TASK_READY) (rf-team-lead.md:193-243).
- Failure handling: Re-spawn targeted gap-fill researchers (max 2 rounds) when research insufficient (rf-team-lead.md:189-192); resume-script + log paths surfaced on EXECUTION_ERROR (rf-team-lead.md:330-340); project-mode fix cycles capped at 3 per phase (rf-team-lead.md:417).
- Validation/QA behavior: Mandatory Research Review Protocol — read ALL research files before spawning builder (rf-team-lead.md:178-192); Phase 2c lightweight Scope Discovery via Glob/Grep/codebase-retrieval before researchers (rf-team-lead.md:135-156).
- Explicit invariants: All three roles must be spawned (rf-team-lead.md:344); builder MUST use template (rf-team-lead.md:345); 3-8 topic-specific researchers per track, single researcher never sufficient (rf-team-lead.md:159-176, 351); scope discovery is prerequisite to research (rf-team-lead.md:353); track isolation — failure in one track must not prevent others (rf-team-lead.md:350).
- Key "do not" rules: Do not skip research review; do not over-interrogate user via AskUserQuestion (rf-team-lead.md:282-291); do not nest subagents in project mode — session runs each pipeline directly (rf-team-lead.md:419-420).

### rf-analyst
- Purpose / role: Data extraction, cross-validation, synthesis review across research/output files; supports parallel partitioning (rf-analyst.md:3, 28-30).
- Tools used: Standard set (Read/Write/Edit/Bash/Glob/Grep/Web*/Task family/Skill/AskUserQuestion) (rf-analyst.md:6-25).
- Inputs expected: spawn prompt with analysis type (completeness-verification / cross-validation / synthesis-review / gap-analysis / coverage-audit), research dir, optional `assigned_files`, output path, team name (rf-analyst.md:32-37, 49-50).
- Outputs produced: Structured per-type reports — Research Completeness Verification (8 items), Cross-Validation report, Synthesis Quality Review (10 items), Gap Analysis, Coverage Audit (rf-analyst.md:84-186, 188-214, 218-281, 285-312).
- Handoff: orchestrator (skill session or team-lead) spawns analyst; analyst typically reports to team-lead via SendMessage on completion (rf-analyst.md:32-37, 327-337).
- Failure handling: Maximum read-only role; reports issues for other agents to fix (rf-analyst.md:323, 347).
- Validation/QA behavior: Acts as adversarial reviewer — find problems, do not confirm work (rf-analyst.md:322); incremental writing mandatory (rf-analyst.md:342).
- Explicit invariants: When partitioned, analyze only `assigned_files` and tag report `(Partition N of M)` with `[PARTITION NOTE: ...]` (rf-analyst.md:42-58); evidence trace required for every claim (rf-analyst.md:316-323).
- Key "do not" rules: Do not modify research/synthesis files (rf-analyst.md:323, 347); zero tolerance for fabrication; never silently resolve contradictions (rf-analyst.md:348-349).

### rf-qa
- Purpose / role: Structural/semantic zero-trust QA across phases — research-gate, synthesis-gate, report-validation, task-integrity, fix-cycle; supports parallel partitioning and in-place fixes when authorized (rf-qa.md:3, 33-37).
- Tools used: Full set incl. Agent/TeamCreate/TeamDelete/EnterPlanMode (rf-qa.md:6-30).
- Inputs expected: spawn prompt with QA phase, research dir + topic, target files (or `assigned_files`), verification criteria, team name, fix_authorization (rf-qa.md:40-48).
- Outputs produced: QA Report with Verdict + Items Reviewed table + Issues table + Actions Taken; mandatory Confidence + Tool engagement fields (rf-qa.md:317-355, 376-417).
- Handoff: spawned by team-lead / skill / executor; reports back via SendMessage to team-lead (rf-qa.md:358-372); on FAIL triggers fix cycle (rf-qa.md:291-313).
- Failure handling: Maximum 3 fix cycles, then HALT and escalate — do NOT downgrade to Open Questions (rf-qa.md:310-313, 431).
- Validation/QA behavior: Phase-specific checklists — research-gate (10), synthesis-gate (12), report-validation (19), task-integrity (20) (rf-qa.md:108-138, 154-200, 222-247, 264-287); adversarial stance with computed Confidence Gate Protocol (rf-qa.md:81-92, 376-417).
- Explicit invariants: Confidence is COMPUTED from VERIFIED/(TOTAL-UNVERIFIABLE)*100; ≥95% AND UNCHECKED==0 required for PASS (rf-qa.md:391-396); Tool Engagement Minimum — Read+Grep+Glob count ≥ checklist items (rf-qa.md:414-416); any gap regardless of severity = FAIL (rf-qa.md:140-142).
- Key "do not" rules: Never adjust confidence subjectively; never claim VERIFIED without tool output; never mark VERIFIED from another report (reliance ≠ verification); never inflate engagement counts with generic calls (rf-qa.md:407-413); never one-shot output file (rf-qa.md:422).

### rf-qa-qualitative
- Purpose / role: Content-level QA on assembled docs (PRDs, TDDs, tech refs, ops guides, READMEs, reports, task files, generic docs) — complements rf-qa (rf-qa-qualitative.md:3, 33-37).
- Tools used: Same full set as rf-qa (rf-qa-qualitative.md:6-30).
- Inputs expected: spawn prompt with phase (prd-qualitative / tdd-qualitative / tech-ref-qualitative / ops-guide-qualitative / readme-qualitative / report-qualitative / task-qualitative / doc-qualitative), document path, document type, template path, output path, team name, fix_authorization (rf-qa-qualitative.md:40-49).
- Outputs produced: QA Report per phase with same structure as rf-qa plus mandatory Self-Audit answers (rf-qa-qualitative.md:183-188, 230-235, 299-303, 363-367, 431-435, 495-499, 591-595, 625-629, 675-714).
- Handoff: spawned by orchestrator after rf-qa structural passes (rf-qa-qualitative.md:101, 198, 246, 314, 378, 445, 510, 609); reports verdict via SendMessage (rf-qa-qualitative.md:720-731).
- Failure handling: Maximum 3 fix cycles then HALT/escalate (rf-qa-qualitative.md:658, 793).
- Validation/QA behavior: Per-phase checklists — prd (23), report (12), tdd (14), tech-ref (12), ops-guide (14), readme (12), task (15), doc-fallback (8) (rf-qa-qualitative.md:110-176, 206-229, 256-292, 323-355, 388-423, 455-487, 527-583, 614-623); Confidence Gate Protocol identical to rf-qa (rf-qa-qualitative.md:734-779).
- Explicit invariants: Ban N/A — adapt instead (rf-qa-qualitative.md:93, 564-583); exhaustive verification, no sampling (rf-qa-qualitative.md:94); contradictions always IMPORTANT or CRITICAL (rf-qa-qualitative.md:789); scope is #1 issue — check first (rf-qa-qualitative.md:791); rf-qa-qualitative complements rather than replaces rf-qa (rf-qa-qualitative.md:794).
- Key "do not" rules: Never one-shot output (rf-qa-qualitative.md:784); do not re-verify what rf-qa already checks (section numbering/file existence) (rf-qa-qualitative.md:794); never adjust confidence subjectively / never inflate tool engagement (rf-qa-qualitative.md:766-775).

### rf-assembler
- Purpose / role: General-purpose consolidator that merges component/synth files into a single structured output, cross-checks consistency, writes incrementally (rf-assembler.md:3, 34-38).
- Tools used: Full set including Agent/TeamCreate/TeamDelete (rf-assembler.md:6-30).
- Inputs expected: Ordered component file paths, output path, output format/template, assembly rules, content rules, team name (rf-assembler.md:67-74).
- Outputs produced: Assembled document at specified output path; `ASSEMBLY_COMPLETE` broadcast with count of sections / component files (rf-assembler.md:49-55, 205-219).
- Handoff: spawned by team-lead, skill, or rf-task-executor; rf-qa validates assembled output and may return `ASSEMBLY_FIX` for in-place corrections (rf-assembler.md:40-62, 181-191).
- Failure handling: Missing component → write `[MISSING: …]` marker and continue (rf-assembler.md:156-160); contradictions → emit explicit `[CONTRADICTION: …]` block, never silently pick (rf-assembler.md:162-171); empty section → write header + no-findings note (rf-assembler.md:173-178).
- Validation/QA behavior: Final Step 6 re-Read pass scans for placeholder text, section count vs template, evidence-trail coverage (rf-assembler.md:128-137); leaves substantive content validation to rf-qa (rf-assembler.md:191).
- Explicit invariants: Incremental writing mandatory — header first, append per section, never one-shot (rf-assembler.md:140-150, 226); fidelity — must not alter substance of findings (rf-assembler.md:197, 228); cross-check internal consistency (rf-assembler.md:118-126, 233).
- Key "do not" rules: Do not skip component files, do not silently resolve contradictions, do not fabricate, do not omit missing sections (rf-assembler.md:225-234).

## Cross-agent flow

- Typical sequence: rf-team-lead spawns the team (rf-team-lead.md:54-75) → rf-task-researcher gathers context and emits `RESEARCH_READY` (rf-task-researcher.md:130-162) → rf-team-lead performs mandatory Research Review (rf-team-lead.md:178-192) → rf-task-builder consumes `BUILD_REQUEST` and emits `TASK_READY` (rf-task-builder.md:88-99, 200-226) → rf-task-executor consumes `TASK_READY`/`EXECUTE_REQUEST` and runs `automated_qa_workflow.sh` (rf-task-executor.md:65-91, 147-162). Quality gates: rf-analyst typically runs in parallel with rf-qa over the same artifacts (rf-qa.md:104-107); rf-qa enforces research-gate / synthesis-gate / report-validation / task-integrity (rf-qa.md:96-313); rf-qa-qualitative runs only after rf-qa structural passes (rf-qa-qualitative.md:101, 246, 314, 378, 445, 510); rf-assembler at end, then handed off to rf-qa for `ASSEMBLY_FIX` cycle (rf-assembler.md:181-191).
- Parallel research location: Multi-Researcher Model and parallel-track spawning live in team-lead (rf-team-lead.md:46, 119-134, 158-176); researcher itself supports the `${TASK_DIR}research/` per-topic file convention (rf-task-researcher.md:274-293); builder consumes the resulting workspace via Glob (rf-task-builder.md:278-286).
- Zero-trust QA gates location: rf-qa "Verification Principles" + Confidence Gate Protocol (rf-qa.md:81-92, 376-417); rf-qa-qualitative mirrors them with Self-Audit + Confidence Gate (rf-qa-qualitative.md:82-95, 734-779); rf-analyst quality standards (rf-analyst.md:316-323).
- rf-qa-qualitative specifics over rf-qa: rf-qa checks structural correctness — section numbers, cross-references, evidence citations, template conformance (rf-qa-qualitative.md:35-37, 794); rf-qa-qualitative adds product/engineering/stakeholder lens with scope appropriateness, logical flow, realistic requirements, red flags (rf-qa-qualitative.md:85-95), and document-type-specific checklists not present in rf-qa (PRD 23, TDD 14, tech-ref 12, ops 14, readme 12, task 15) (rf-qa-qualitative.md:110-176, 256-292, 323-355, 388-423, 455-487, 527-583); explicit Ban-N/A rule with Adaptation Guidance table (rf-qa-qualitative.md:93, 564-583).

## Determinism observations

- Determinism preserved: Tooling stack and message vocabularies are fixed tables (rf-task-builder.md:42-55, rf-task-executor.md:42-57, rf-team-lead.md:80-100); template selection is rule-driven (rf-team-lead.md:366-383); fix-cycle limits are hard-coded per gate type (rf-task-builder.md:352-358, rf-qa.md:310-313); Confidence Gate is a computed formula with explicit thresholds (rf-qa.md:391-396, rf-qa-qualitative.md:751-757); rf-assembler's no-silent-resolve rule for contradictions (rf-assembler.md:162-171, 228).
- Non-determinism inherent: Topic-type selection per track ("3-8 per track based on complexity") is judgment-driven (rf-team-lead.md:160-173); partition decisions and balanced subset splits are orchestrator-judgment (rf-analyst.md:65-69, rf-qa.md:73-77, rf-qa-qualitative.md:74-78); qualitative judgment-call adaptations (e.g., "is the audience appropriate?") tracked only via evidence trail (rf-qa-qualitative.md:777-779); researcher's adversarial doc-staleness tagging depends on cross-validation effort (rf-task-researcher.md:253-271); test/scope sufficiency assessments in rf-qa task-integrity item 10 require subjective scoping judgment (rf-qa.md:277).

## Surfaces relevant to inverse-direction proposals

- R3 gate-results passthrough: Would attach to rf-qa first (output format already structured for verdict + issues table, rf-qa.md:317-355) and to rf-qa-qualitative (parallel structure, rf-qa-qualitative.md:675-714); team-lead would consume the passthrough since it currently relays EXECUTION_COMPLETE summaries (rf-team-lead.md:246-264); rf-task-builder would need a new BUILD_REQUEST field if gate results feed back into future task encoding (rf-task-builder.md:336-378).
- DNSP-style synthetic-finding behavior: Most natural fit is rf-analyst (synthesizes across files, gap-analysis + cross-validation phases already exist, rf-analyst.md:188-214, 285-298); rf-qa would gain a new phase or checklist family rather than a host change because it is explicitly anti-fabrication today (rf-qa.md:425-426); rf-assembler is excluded — it must NOT fabricate (rf-assembler.md:201, 230).
- Parallel partitioning hosts: rf-analyst (rf-analyst.md:42-69), rf-qa (rf-qa.md:50-77), rf-qa-qualitative (rf-qa-qualitative.md:50-78); orchestrator (skill session / team-lead) owns the partitioning decision and merge in all three (rf-analyst.md:63-69, rf-qa.md:71-77, rf-qa-qualitative.md:72-78); team-lead also hosts parallel-track partitioning at the pipeline level (rf-team-lead.md:46, 119-134).

## evidence_status

`complete`. All 8 expected agent files were located via `ls` and read in full (line counts match: 493, 505, 368, 431, 349, 432, 794, 241). No missing files. No unverifiable claims.
