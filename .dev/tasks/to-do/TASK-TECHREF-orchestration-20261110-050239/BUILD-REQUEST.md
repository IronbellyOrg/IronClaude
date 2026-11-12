# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-reference
Task Directory: .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/
Research Notes: .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Create a comprehensive Technical Reference document for supervised orchestration following the project template. Write it to docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md.

WHY: Provide an evidence-based reference to current supervised orchestration mechanisms, their boundaries, and evidence limits for people understanding and maintaining the system.

TASK_ID_PREFIX: TASK-TECHREF
FEATURE_SLUG: orchestration
TEMPLATE: 02
QA_INTENSITY: full

USER BOUNDARIES AND EXECUTION ADAPTATIONS:
- Document current mechanisms only. Subordinate mode is deferred, not implemented. No live Orca evaluation or product implementation. Do not infer installed or deployed behavior from a development checkout.
- Earlier research is historical. Recheck current ownership wording in canonical local guidance; distinguish updated wording from earlier research without asserting the separate future-role question is resolved or claiming installation rollout.
- Do not specify model overrides for any agent invocation. Inherit the configured model; do not bypass permission controls.
- The user requested the full technical reference and its execution. Invoke task-builder, then execute the resulting task. Where an agent cannot write its assigned artifact, do not bypass restrictions: return findings to an authorized coordinator for persistence, preserving independent review and all gate counts; otherwise halt and report the blocker.
- If C8 identifies an in-scope unwired capability, record it as a defect and link or create a remediation task under .dev/tasks/to-do/ in accordance with the skill; do not relabel it without a cited scope decision.

DOCUMENTATION STALENESS WARNINGS:
- [CODE-CONTRADICTED: historical report] Earlier report sections 2.2, 4 A01 and 7.6 present old ownership wording as current; local canonical guidance and hook text have changed. Re-read sources and distinguish local wording from deployed state. Do not claim the future-role question resolved.
- [UNVERIFIED] Installed copy parity, running Orca build and effective settings, live hook ordering and runtime enforcement are outside observed evidence. Development source is not established to match installed runtime.
Do NOT create task items assuming contradicted or unverified architecture as current. Phase 2 agents cross-validate claims and flag gaps using CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 1 (Preparation): Update task status, confirm scope, read template, select Heavyweight, ensure task subfolders research/, synthesis/, qa/, reviews/ exist.
- Phase 2 (Deep Investigation): L1 Discovery — agents investigate source in parallel and write findings to .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research/.
- Phase 3 (Completeness Verification): L4 Review/QA — 2 rf-analyst (completeness-verification and cross-validation), 2 rf-qa (evidence-quality and gap-detection), 1 rf-qa-qualitative (research-depth), all report-only in parallel. Consolidate, spawn one gap-filler per blocking gap, then 1 rf-qa + 1 rf-qa-qualitative verification. Maximum two cycles. Partition each lens independently at >6 research files.
- Phase 4 (Web Research): L1 Discovery — external research only for gaps requiring it, one topic and file per agent.
- Phase 5 (Synthesis + Multi-Agent Synthesis Gate): L2 Build-from-Discovery — parallel synthesis; then 2 rf-analyst (accuracy and tracing), 2 rf-qa (structure and content-quality), 1 rf-qa-qualitative (coherence), all report-only in parallel. Consolidate; ONE authorized fixer for blocking findings; 2-agent verification. Partition each lens independently at >4 synth files; maximum two cycles.
- Phase 6 (Assembly + Lens-Based QA + Source Fidelity Gate): L6 Aggregation — one rf-assembler; 4–6 structural rf-qa, 4–6 qualitative rf-qa-qualitative and three domain lenses in parallel, all report-only. Consolidate; ONE authorized fixer and two verifiers; maximum two cycles. After passage, minimum 5 source-fidelity agents, scaling to 6–8, each reading assigned source and FULL reference; consolidate, serialize fixes, verify.
- Phase 7 (Present to User & Complete Task): ANTI-ORPHANING — task completion items are inside this phase, not a separate Post-Completion section. Honor executor post-completion validation before Done.

QA_GATE_REQUIREMENTS: PER_PHASE
- Research completeness: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5, max 2 gap-fill cycles, partition each lens at >6 files.
- Synthesis quality: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5, max 2 fix cycles, partition each lens at >4 files.
- Final document lens QA: 4–6 rf-qa + 4–6 rf-qa-qualitative plus three domain lenses (code-example-accuracy, api-signature-correctness, configuration-value-verification), 11–15 total, max 2 fix cycles, partition at 1500+ lines.
- Source fidelity: minimum 5 rf-qa agents (semantic coverage, detail preservation, phantom coverage, aspirational content, cross-reference verification); 6 at 1000–2000 source lines, 8 above 2000; maximum 2 fix cycles. Each reads assigned source and FULL reference.
- Original task skill floors override conflicting lower template counts: phase-gate and post-completion QA after every phase except setup require at least 3 structural + 3 qualitative agents; scale to 4+4 at 500–1500 output lines, 5+5 at 1500–3000, 6+6 above 3000. Intermediate research and synthesis gates retain their separate five-agent floors; task-integrity gates require 2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst. Skill-specific gates and executor phase-gate/post-completion checks are additive where required. Two-agent verification is targeted fix verification, not an initial QA gate. Do not reduce floors.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + SOURCE_FIDELITY + NO_DOCS_CLOSE_DEFECT
- TEMPLATE_COMPLIANCE: Every template section is present or N/A with rationale.
- EVIDENCE_TRAIL: Every claim cites file paths, line numbers, or verified sources. Distinguish normative policy, implementation, historical observations, development source, and deployed state.
- CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags; trace runtime claims to source and list gaps.
- SOURCE_FIDELITY: Phase 6 fidelity agents read actual source and the assembled reference, verifying semantic coverage and exact signatures, config defaults and type shapes, not synthesis alone.
- NO_DOCS_CLOSE_DEFECT (C8): A [CODE-CONTRADICTED] in-scope capability declared shipped/enabled-by-config but unwired at its runtime entrypoint must be recorded as a DEFECT with linked MDTM remediation under .dev/tasks/to-do/. It cannot be relabeled as a gap, future phase or question without a cited scope decision. Respect the no-write boundary: link an existing task if possible, otherwise halt and escalate for authorization. Explicitly deferred subordinate mode is not a shipped capability.

TESTING_REQUIREMENTS: N/A — documentation only; no code produced, no tests applicable. Source and existing tests may be read as evidence; no live Orca evaluation.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research-notes.md
Read this file FIRST for full findings, file inventory, investigation assignments, synthesis mapping and output paths.

TEMPLATE_PATH: .claude/templates/documents/technical_reference_template.md
OUTPUT_PATH: docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
SKILL CONTEXT FILE: .claude/skills/tech-reference/SKILL.md
Read Agent Prompt Templates, Synthesis Mapping Table, Synthesis Quality Review Checklist, Assembly Process, Validation Checklist, Content Rules, Tier Selection and Output Structure. Embed relevant instructions in checklist items per B2.

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM A3 and A4, create individual checklist items for EVERY research agent, web topic, synthesis file and validation step. Do not batch items. Research notes SUGGESTED_PHASES supplies per-agent detail.

TO BUILD A GOOD TASK FILE, YOU NEED:
- Goal and outputs; source files and context from research notes.
- Phases and steps from research notes SUGGESTED_PHASES and skill phase definitions.
- Verification criteria and dependencies for every step.

ESCALATION:
When a builder is a subagent without team context, do not broadcast TASK_READY or use TaskCreate or SendMessage; return the task path as final output. Use codebase retrieval or native search for codebase questions and approved web tools for external docs. If blocked, create the best task file possible and note gaps in Task Log; never bypass user boundaries or permissions.

SKILL PHASES TO ENCODE IN TASK FILE:
Encode these phases sequentially. Every item must follow B2 self-containment.

Phase 1 — Preparation:
- Update status to Doing; confirm boundaries, sources and Heavyweight tier from research notes.
- Read .claude/templates/documents/technical_reference_template.md; select Heavyweight based on cross-cutting scope.
- Ensure .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/ contains research/, synthesis/, qa/ and reviews/.

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One item per research agent, with the complete codebase research prompt, incremental writing protocol and documentation staleness protocol, plus topic, type, files and output. Spawn independent agents in one message; mark each as it returns and resume unchecked items after interruption. Heavyweight uses 6–10+.
- Architecture analyst: worker identity, roles, authority and human rulings; src/superclaude/core/WORKER-CONTRACT.md sections 1–3 and src/superclaude/core/CLAUDE.md; output .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research/01-roles-authority.md.
- Code tracer: coordinator lifecycle, monitoring, retry and messages; src/superclaude/core/WORKER-CONTRACT.md section 4; output .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research/02-lifecycle.md.
- Integration mapper: hook recognition and enforcement ceilings; src/superclaude/hooks/scripts/require-orca-worktree-agent.sh, src/superclaude/hooks/scripts/launch-level-guard.sh, src/superclaude/hooks/scripts/launch-job-identity.sh and tests/hooks/; output .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research/03-guards.md.
- Code tracer: ordinary launch and worker launch boundaries; src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, src/superclaude/cli/issue_watch/launch.py and relevant tests; output .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research/04-launchers.md.
- Architecture analyst: development-source helper routing, mailbox and run-binding only where available; worker-start-authority.ts, dispatch-report-mailbox.ts, worker-run-binding.ts under /home/coder/workspaces/IronOrca/src/main/runtime/. Verify locations and provenance; distinguish development checkout, historical installed trace and unverified deployed behavior. Output .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research/05-orca-provenance.md.
- Doc analyst: current distribution and policy, staleness and earlier decision; src/superclaude/core/CLAUDE.md, src/superclaude/skills/ccsession-tag/README.md, docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md sections 6–9, relevant tests; output .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research/06-distribution-evidence.md.

Gate counts, fix budgets and scaling are in QA_GATE_REQUIREMENTS above, subject to original task skill floors.

Phase 3 — Research Completeness Verification (MULTI-AGENT LENS GATE, PARALLEL):
- Spawn five report-only agents: rf-analyst completeness-verification → qa/analyst-completeness-report.md; rf-analyst cross-validation → qa/analyst-crossval-report.md; rf-qa evidence-quality → qa/qa-research-evidence-report.md; rf-qa gap-detection → qa/qa-research-gaps-report.md; rf-qa-qualitative research-depth → qa/qa-research-depth-report.md. All qa paths are under .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/. Embed complete adversarial lens prompts per B2, assuming at least five critical issues per lens.
- For >6 research files partition each lens independently, with assigned subsets and numbered reports; merge the union, deduplicate and preserve highest severity. Read all reports and determine PASS/FAIL.
- On FAIL consolidate at qa/qa-research-consolidated-findings.md, spawn one targeted gap-filler per blocking gap, then report-only rf-qa and rf-qa-qualitative verification. Minor findings are notes. Maximum two fix cycles; halt and escalate remaining blockers. Compile gaps at .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/gaps-and-questions.md. Do not proceed without PASS.

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item per web topic from research notes or Phase 3 gaps, embedding the skill's web-research prompt, codebase context and distinct output. External research is optional and only for gaps requiring external documentation. No live Orca evaluation.

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One item per synthesis file, each with full synthesis prompt, specific research sources, template sections and output. Five outputs in .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/synthesis/ are synth-01-overview-architecture.md, synth-02-data-flow.md, synth-03-subsystems.md, synth-04-integration-config.md and synth-05-conventions-debt.md. Map the six research outputs to applicable template sections 1–5 and 8–16; mark inapplicable sections N/A with rationale.
- After synthesis, spawn five report-only agents in parallel: analyst synthesis-accuracy → qa/analyst-synthesis-accuracy-report.md; analyst source-tracing → qa/analyst-synthesis-tracing-report.md; rf-qa structure → qa/qa-synthesis-structure-report.md; rf-qa content-quality → qa/qa-synthesis-quality-report.md; rf-qa-qualitative synthesis-coherence → qa/qa-synthesis-coherence-report.md. Embed adversarial prompts per B2.
- At >4 synth files partition each lens independently with numbered reports and merge. Read all; consolidate at qa/qa-synthesis-consolidated-findings.md. For blockers ONE authorized rf-qa fixer, then two report-only verifiers. Minor findings remain notes. Maximum two cycles; halt and escalate remaining blockers. Do not proceed without PASS.

Phase 6 — Assembly & Validation:
- Spawn one dedicated rf-assembler, not general-purpose, to read the five synth files in order and assemble docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md using .claude/templates/documents/technical_reference_template.md and the skill's assembly and content rules. Embed the full assembler prompt including incremental writing and consistency checks.
- Step 6a: determine document lines and spawn all report-only lens agents in parallel: <500 lines 4+4; 500–1500 4+4; 1500–3000 5+5; >3000 6+6 structural/content, plus three domain lenses. Structural lenses: template-conformance, internal-consistency, evidence-quality, completeness. Content: actionability, numbers-metrics, crossref-chain, domain-accuracy. Domain: code-example-accuracy (rf-qa), api-signature-correctness (rf-qa), configuration-value-verification (rf-qa-qualitative). Extra agents partition existing lenses by section. Each gets qa/qa-lens-[lens-name]-report.md and an adversarial prompt with error target document_lines/100, minimum 5. Apply task skill floors when higher.
- Step 6b: consolidate reports at qa/qa-consolidated-findings.md; deduplicate and preserve highest severity. For blockers only, ONE rf-qa fixer followed by 1 structural and 1 qualitative report-only verifier. Minor findings remain notes. Maximum two cycles, then halt and escalate.
- Step 6c: after lens QA passes, spawn minimum 5 rf-qa fidelity agents, 6 at 1000–2000 source lines and 8 above 2000. Each reads assigned source and FULL reference, with one lens: semantic coverage, detail preservation, phantom coverage detection, aspirational content detection, or cross-reference verification. Write qa/qa-source-fidelity-[N]-report.md. Consolidate, use one authorized fixer and two report-only verifiers; maximum two cycles, then halt and escalate.
- Step 6d: verify all QA reports, consolidated findings and verification reports. No unresolved CRITICAL or IMPORTANT findings; MINOR findings are notes. Preserve artifacts.

Phase 7 — Present to User & Complete Task:
- Present document path, line count and tier, sections populated or skipped, research and synthesis artifact locations, and gaps needing manual review.
- Write summary to Task Log / Notes; update frontmatter to Done and completion date only after required phase-gate and post-completion validation.
- If consolidating existing docs, list sources as archival candidates. Archival is non-blocking and requires authorization.
- CRITICAL ANTI-ORPHANING: Completion items are inside this phase, never a separate Post-Completion section. Downstream offers and archival suggestions are NON-BLOCKING.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/TASK-TECHREF-orchestration-20261110-050239.md

STEPS:
1. Read .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research-notes.md (MANDATORY).
2. Read .claude/skills/tech-reference/SKILL.md for prompts, synthesis mapping, content rules, validation checklist, tier selection and assembly (MANDATORY).
3. Read .claude/templates/workflow/02_mdtm_template_complex_task.md (MANDATORY).
4. Follow PART 1 completely (A3 granularity, B2 self-contained items, E1–E4 flat structure), subject to user boundaries and task skill floors.
5. Note missing information in Task Log; halt rather than bypassing restrictions or asserting unverified behavior.
6. Create .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/TASK-TECHREF-orchestration-20261110-050239.md using PART 2 structure.
7. Return the task file path.
