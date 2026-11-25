# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-reference
Task Directory: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/
Research Notes: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Create a comprehensive Technical Reference document for the "observer, sweep and dashboard" family of the IronClaude repository (the observer `superclaude observe`, the sweep `superclaude sweep run` / `/sc:sweep` / skill `sc-sweep-protocol`, the living work report skill `agent-work-report`, and the Orca dashboard / TUI design package of issue 409) following the project template. The document will be written to /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md (NOT under docs/).

WHY: The owner needs an exact, cited picture of what exists, to decide how Clay's new "orchestrator" design (a per-repo orchestrator woken by the issue watcher, plus a living work report) should be unified with the owner's observer, sweep and planned TUI dashboard, in a later design brainstorm. Emphasize: data sources, output formats, what is live, who consumes the output, and overlaps in purpose. Document how these relate to the coordinator (WORKER-CONTRACT.md sweep duty WC-16), what data each reads from Orca, what each writes, and what is built versus only designed. State facts and overlaps; do not recommend a unification.

TASK_ID_PREFIX: TASK-TECHREF

FEATURE_SLUG: observer-sweep-dashboard

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
Found during scope discovery (details in research-notes.md FEATURE_ANALYSIS and scope/*.md):
- [CODE-CONTRADICTED] docs/designs/orchestrator-mode.md:27 says `src/superclaude/cli/sweep/` does not exist yet; it exists (5 modules). That doc is the Phase 1 design of the sweep, not a general orchestrator doc.
- Issue 409 live body says both "no observer code exists" and that the observer is on master; the 2026-11-17 comment and the sweep design say the package branch is unmerged while the identical 406-file package is on origin/master via PR #503.
- The package README prefers Bubble Tea / Lip Gloss; the shipped observer is Python/Rich (owner decision 2, 2026-11-08, stack.md:3 on origin/master).
- agent-work-report SKILL.md:14 names `orchestrator_repo` in `issue-watch.json`; no code in cli/issue_watch reads it (UNVERIFIED who sets it). The orchestrator (`/sc:orchestrator`, `superclaude orchestrator report-entry`) is design-only, so nothing writes active living-report entry files.
- The research folder `.dev/research/orca-dashboard-20261105/` is untracked and local-only.
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED] or [UNVERIFIED] as current. Phase 2 agents will do full cross-validation with CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED tags.

GLOBAL AGENT RULES (MUST be embedded verbatim at the top of EVERY sub-agent prompt in the task file, per B2; they come from the requester and are non-negotiable):
- READ-ONLY on all source code and design files. Write only inside the task directory (/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/ and its subfolders) or the single final output file named in OUTPUT_PATH. Never stage or commit anything.
- Any GitHub access is read-only `gh` with `--repo IronbellyOrg/IronClaude`. Never touch SuperClaude-Org (no fetch, pull, push, PR, issue, comment, review, reaction, remote or link flag).
- UV only for Python (never `python -m`, never `pip install`, never `python script.py`). Do not run the code under study; read it.
- CODE SNAPSHOT: read ALL code from the read-only export of origin/master 61ac2c2e6 at /home/coder/.cache/ic-snap-20261120/master (same layout as the repo root; it omits `.dev/`). The checkout /home/coder/workspaces/IronClaude is stale for code. Design-package files (the #409 package under .dev/design/orca-observer-20261106/, .dev/issues/409/, .dev/research/orca-dashboard-20261105/) are read from the checkout /home/coder/workspaces/IronClaude (docs branch docs/409-orca-dashboard-designs, commit 495eb96d1). Files that exist only on origin/master under `.dev/` are read with `git -C /home/coder/workspaces/IronClaude show origin/master:<path>`.
- Use absolute paths in every prompt (agents' working directory resets between calls).
- Scope-discovery files that agents may use as a starting map (verify, do not copy): scope/01-observe.md, scope/02-sweep.md, scope/03-agent-work-report.md, scope/04-dashboard-design.md in the task directory.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 1 (Preparation): Update task status, confirm scope from research notes, read the template, select depth tier (Standard), confirm the task folder at ${TASK_DIR} has research/, synthesis/, qa/, reviews/ subfolders (already created)
- Phase 2 (Deep Investigation): L1 Discovery. 6 agents investigate feature code and write findings files to ${TASK_DIR}research/
- Phase 3 (Completeness Verification): L4 Review/QA gate (standard intensity: see QA_GATE_REQUIREMENTS Gate 1). Serialized fix protocol: consolidate findings into qa-research-consolidated-findings.md, targeted gap-filling research agents (one per blocking gap), then verification round (1 rf-qa + 1 rf-qa-qualitative). Max 2 fix cycles.
- Phase 4 (Web Research): L1 Discovery. None planned (all subjects are in-repo). Include one checklist item "Web research: skipped, rationale recorded, unless Phase 3 found a gap needing external Orca documentation", marked complete with the rationale.
- Phase 5 (Synthesis + Synthesis Gate): L2 Build-from-Discovery. 7 synthesis agents (one per synth file in RECOMMENDED_OUTPUTS of the research notes). Then Gate 2 (standard: 1 rf-analyst accuracy + 1 rf-qa structure + 1 rf-qa-qualitative coherence), consolidate, ONE rf-qa fix agent, 2-agent verification round. Partitioning for >4 synthesis files applies (7 files: partition each lens across 2 instances: files 1-4 and 5-7).
- Phase 6 (Assembly + Lens-Based QA + Source Fidelity Gate): L6 Aggregation. rf-assembler (single agent) assembles the final document at OUTPUT_PATH; then Gate 3 lens QA (standard: 3 rf-qa structural + 3 rf-qa-qualitative content + 1 domain lens), consolidate, ONE fix agent, verification round; then Gate 4 source-fidelity (standard: 2 rf-qa fidelity agents), fix cycle if needed, verification. Serialized (not parallel) fix authorization.
- Phase 7 (Present to User & Complete Task): ANTI-ORPHANING: task-completion items are WITHIN this phase. Return to the requester only the final path and a three-line summary (what the reference covers, how many claims were verified, anything unverified). Do not stage or commit anything.

QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: PER_PHASE
  **NOTE: Gate descriptions below specify FULL intensity agent counts. QA_INTENSITY is standard, so the rf-task-builder applies the I22 reductions in the QA Intensity Adaptation table.**
  Gate 1: Research Completeness (Phase 3)
    - lite: 1 rf-qa (evidence + gaps) + 1 rf-qa-qualitative (depth + completeness) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles. (Partition each lens across 2 instances when more than 6 research files exist; here there are exactly 6, so no partitioning.)
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 gap-fill cycles. Partitioning >6 files.
  Gate 2: Synthesis Quality (Phase 5)
    - lite: 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >4 files.
  Gate 3: Final Document Lens-Based QA (Phase 6, step 6a)
    - lite: 1 rf-qa (combined structural) + 1 rf-qa-qualitative (combined content) + 1 domain lens (code-example-accuracy) = 3 agents. Max 1 fix cycle.
    - standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (code-example-accuracy) = 7 agents. Max 2 fix cycles.
    - full: 4-6 rf-qa + 4-6 rf-qa-qualitative (scaled by output size, partitioning at 1500+ lines) + 3 domain lenses (code-example-accuracy, api-signature-correctness, configuration-value-verification) = 11-15 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, step 6c)
    - lite: 1 rf-qa fidelity agent (combined semantic-coverage + phantom-detection lenses). Max 1 fix cycle.
    - standard: 2 rf-qa fidelity agents (semantic-coverage + detail-preservation). Max 2 fix cycles.
    - full: 5 rf-qa fidelity agents (semantic-coverage, detail-preservation, phantom-coverage, aspirational-content-detection, cross-reference-verification). Scale to 6 at 1000-2000 source lines, 8 at >2000. Max 2 fix cycles.
  Fidelity agents read BOTH their assigned source files (snapshot paths, plus the design package files for the dashboard slice) AND the full assembled reference. Because the source-line count is far above 2,000, each of the 2 standard fidelity agents is assigned a disjoint source-file half (observer + sweep code; agent-work-report + design package).

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + SOURCE_FIDELITY + NO_DOCS_CLOSE_DEFECT
  TEMPLATE_COMPLIANCE: All sections from technical_reference_template.md must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  SOURCE_FIDELITY: Phase 6 Gate 4 fidelity agents read the actual source code files AND the assembled tech reference; semantic coverage of every documented subsystem, API signature, and configuration value must be verified against source code (not just the synthesis files). Detail preservation is mandatory: function signatures, config defaults, and type shapes in the tech reference must match the code verbatim.
  NO_DOCS_CLOSE_DEFECT (C8): A [CODE-CONTRADICTED] finding on an IN-SCOPE capability (spec/TDD names it shipped/enabled-by-config but it is not wired at its runtime entrypoint: no production caller, discarded/dead-guarded result, or sentinel-only callee) MUST be recorded as a DEFECT with a linked MDTM remediation task under .dev/tasks/to-do/, and MUST NOT be re-labeled as a known-gap/future-phase/Open-Question without an on-record cited scope decision. A docs pass may not close an unwired in-scope capability by writing prose around it. FOR THIS TASK: the requester forbids writing outside the task folder and the output file, so agents record each defect candidate (for example the sweep classes stalled (proved) and fenced, which the command, skill and WC-16 name but which cannot fire in Phase 1 because nothing sets `worker_done_seen` / `fenced_evidence`) with the spec/design line that declares them, the code evidence, and the cited on-record scope decision if one exists (docs/designs/orchestrator-mode.md Phase 1 limits, sweep.md:16, SKILL.md:26, report.py:42-45); if no cited scope decision exists the reference records a DEFECT-CANDIDATE and states plainly "remediation task not created (read-only brief); flagged for the owner". Never relabel such an item as a plain known gap without the cited decision.

TESTING_REQUIREMENTS: N/A (documentation-only skill, no code produced, no tests applicable).

RESEARCH NOTES FILE:
/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments (6 agents R1-R6 with output file names, topics and file lists), synthesis mapping (7 synth files), and output paths.

TEMPLATE_PATH: /home/coder/workspaces/IronClaude/.claude/templates/documents/technical_reference_template.md
OUTPUT_PATH: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md

SKILL CONTEXT FILE:
/home/coder/workspaces/IronClaude/.claude/skills/tech-reference/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Synthesis Mapping Table" section for the standard synth-file-to-template-section mapping. Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for tech reference assembly steps. Read the "Validation Checklist" section for Phase 6 validation criteria. Read the "Content Rules" section for writing standards. Read the "Tier Selection" section for depth tier line budgets and agent counts. Read the "Output Structure" section for the final document format. These must be embedded in the relevant checklist items per B2 self-contained pattern.

CRITICAL: GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process Structure), you MUST create individual checklist items for EVERY research agent, web research topic, synthesis file, and validation step. Do NOT create batch items like "spawn all 5 research agents" or "run all web research"; each agent gets its own checklist item. The research notes SUGGESTED_PHASES section contains per-agent detail specifically to enable this granularity.

TO BUILD A GOOD TASK FILE, YOU NEED:
- Goal and outputs (what to create, where, what format)
- Source files and context (what exists, what to reference) from the research notes
- Phases and steps (logical breakdown of the work) from the research notes SUGGESTED_PHASES + SKILL.md phase definitions
- Verification criteria (how to know each step is done)
- Dependencies (what's needed before each step)
The research notes file should cover most of this.

ESCALATION:
Since you are running as a subagent (not a teammate), you have NO team context. Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage; these tools will fail because there is no team. This overrides your agent definition's Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast). Instead, return the task file path as your final output.
- **Codebase questions** -> use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
- **External docs/syntax** -> use WebSearch
- **If blocked** -> create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.

SKILL PHASES TO ENCODE IN TASK FILE:
The task file MUST encode these phases as sequential checklist items. Each phase maps to a section of the skill's workflow. All items MUST follow the B2 self-contained pattern from the MDTM template.

Phase 1: Preparation:
- Update task status to "🟠 Doing"
- Confirm scope from research notes (feature boundaries, key directories, tier selection)
- Read the technical reference template at /home/coder/workspaces/IronClaude/.claude/templates/documents/technical_reference_template.md
- Select depth tier (Standard) based on the requester's instruction
- Confirm the task folder at ${TASK_DIR} has research/, synthesis/, qa/, reviews/ subfolders (already created during scope discovery)

Phase 2: Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (R1-R6 from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md (embedding the GLOBAL AGENT RULES above)
- Each item specifies: investigation topic, type, files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol, and the C8 clause, from SKILL.md) in each checklist item per B2
- All 6 research agents are spawned in parallel using multiple Agent tool calls in a single message; mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.

**Authoritative specification for gate parameters (agent counts, fix cycle budgets, scaling tiers) is in the QA_GATE_REQUIREMENTS above. This section provides expanded operational guidance for each phase. In case of conflict between this section and QA_GATE_REQUIREMENTS, QA_GATE_REQUIREMENTS values take precedence.**

Phase 3: Research Completeness Verification (LENS GATE, PARALLEL; standard intensity = 3 agents):
- Spawn IN PARALLEL, all fix_authorization: false (report only): (1) rf-analyst (completeness-verification lens) writes `${TASK_DIR}qa/analyst-completeness-report.md`; (2) rf-qa (evidence-quality lens) writes `${TASK_DIR}qa/qa-research-evidence-report.md`; (3) rf-qa-qualitative (research-depth lens: traced data flows, function signatures, exact Orca verbs, versus file listings) writes `${TASK_DIR}qa/qa-research-depth-report.md`. Each agent gets a lens-specific prompt with adversarial framing: "Look for critical issues in your lens area that these research files missed. Report each one you find with evidence; there is no minimum count, and zero is valid if you state what you checked." Embed full prompts in each checklist item per B2.
- Read ALL reports. Determine the verdict (PASS / FAIL). If PASS, proceed to Phase 4. If FAIL, follow the serialized fix protocol:
  1. Consolidate findings into `${TASK_DIR}qa/qa-research-consolidated-findings.md` (deduplicate, keep highest severity). A "gap" is any blocking finding; minor findings stay as notes.
  2. Gap-filling: spawn targeted research agents, one per blocking gap, same incremental writing protocol.
  3. Verification round: 1 rf-qa (fix-cycle, fix_authorization: false) + 1 rf-qa-qualitative (re-check, fix_authorization: false). ADVERSARIAL STANCE: assume errors, verify every claim.
  4. Cycle: max 2 fix cycles (3 reviews), then HALT and escalate to the requester with the open blocking findings; log in Task Log. Do NOT continue to Phase 4 without approval.
- Compile final gaps into ${TASK_DIR}gaps-and-questions.md
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4: Web Research: skipped unless a gap requires it (see mapping above).

Phase 5: Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (7 files from the research notes RECOMMENDED_OUTPUTS, mapped via the Synthesis Mapping Table), each spawning an Agent subagent with the synthesis agent prompt from SKILL.md; each item specifies research files to read, template sections to produce, output path (${TASK_DIR}synthesis/synth-[NN]-[topic].md)
- After ALL synthesis agents complete, spawn IN PARALLEL, all fix_authorization: false: (1) rf-analyst (synthesis-accuracy + source-tracing lens) writes `${TASK_DIR}qa/analyst-synthesis-accuracy-report.md`; (2) rf-qa (structure + content-quality lens) writes `${TASK_DIR}qa/qa-synthesis-structure-report.md`; (3) rf-qa-qualitative (synthesis-coherence lens) writes `${TASK_DIR}qa/qa-synthesis-coherence-report.md`. Because there are 7 synthesis files (>4), partition each lens across 2 instances (files 01-04 and 05-07) with numbered reports and merge. Consolidate findings at `${TASK_DIR}qa/qa-synthesis-consolidated-findings.md`, spawn ONE rf-qa fix agent (fix_authorization: true) to apply all blocking fixes (minor findings stay as notes), then a 2-agent verification round.
- If FAIL after the fix agent: re-run the affected synthesis agents, then re-spawn rf-qa. Max 2 fix cycles (3 reviews), then HALT and escalate.

Phase 6: Assembly & Validation (RF-ASSEMBLER + Structural QA + Qualitative QA + Source Fidelity):
- Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") to assemble the final technical reference at OUTPUT_PATH. Hand it: the ordered list of synth file paths (component_files), the output path, the template (output_format), the Assembly Process steps and Content Rules from SKILL.md. It writes incrementally (frontmatter first, then sections in template order, then Table of Contents, then cross-check). The assembler must be a single agent. Embed the full assembler prompt per B2.
- Step 6a: Lens-Based QA (PARALLEL, all fix_authorization: false), standard intensity, 7 agents: rf-qa template-conformance, internal-consistency, evidence-quality; rf-qa-qualitative actionability, domain-accuracy, crossref-chain; domain lens code-example-accuracy (rf-qa). Each writes `${TASK_DIR}qa/qa-lens-[lens-name]-report.md`. Embed lens-specific prompts with adversarial framing: "Report each concrete defect in your lens area with evidence. There is no minimum count; zero is valid if you state what you checked."
- Step 6b: Consolidate Findings + Serialized Fix: consolidate into `${TASK_DIR}qa/qa-consolidated-findings.md`; ONE rf-qa fix agent (fix_authorization: true) applies the consolidated blocking findings (a minors-only list spawns no fix agent); then a 2-agent verification round (1 rf-qa + 1 rf-qa-qualitative, fix_authorization: false); max 2 fix cycles (3 reviews), then HALT and escalate.
- Step 6c: Source-Document Fidelity Gate (PARALLEL, fix_authorization: false), standard intensity, 2 rf-qa fidelity agents with lenses semantic-coverage and detail-preservation. Each reads its assigned source files (disjoint halves: observer + sweep code; agent-work-report + design package) AND the FULL assembled reference. Each writes `${TASK_DIR}qa/qa-source-fidelity-[N]-report.md`. If issues: consolidate, ONE fix agent (fix_authorization: true), 2-agent verification round, max 2 fix cycles (3 reviews), then HALT and escalate.
- Step 6d: Verify all QA complete. If any blocking issue remains unresolved, address it before Phase 7; minor issues are recorded as notes.

Phase 7: Present to User & Complete Task:
- Summarize for the requester: final path, line count and tier, sections populated vs N/A, number of claims verified, anything UNVERIFIED, artifact locations
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- No archival offer (not a consolidation). Do not stage or commit.
- CRITICAL ANTI-ORPHANING RULE: Task-completion items MUST be inside this phase, NEVER a separate Post-Completion section.

TASK FILE LOCATION: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/TASK-TECHREF-observer-sweep-dashboard-20261120-040203.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, synthesis mapping, content rules, validation checklist, tier selection, and assembly procedure (MANDATORY)
3. Read the MDTM template: /home/coder/workspaces/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md (MANDATORY)
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section; the skill will review
6. Create the task file at the TASK FILE LOCATION above using PART 2 structure
7. Return the task file path
