# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-reference
Task Directory: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/
Research Notes: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Create a comprehensive Technical Reference document for the "issue-to-work pipeline" of the IronClaude repository (as it exists on origin/master 61ac2c2e6) following the project template. The final document is written to /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md (NOT under docs/). It must also contain a clearly labelled appendix "Removed on 2026-11-20" documenting the package src/superclaude/cli/issue_pipeline/ and rule WC-17 as they were just before PR 682 (commit 01e7a9e23) deleted them.

WHY: The owner needs an exact, cited picture of what is built and what is not, to decide how to unify two competing lines of work (the owner's watcher/claim pipeline and a rewrite) in a later design brainstorm. Emphasize: triggers, state stores, approval/gate points, launch levels, guard layers, what runs live versus what is switched off (enabled: false), what each piece writes to GitHub, and every test file that pins behaviour. PR 686 and the rewrite design are out of scope: one sentence saying so in Section 1, nothing more.

TASK_ID_PREFIX: TASK-TECHREF
TASK_ID: TASK-TECHREF-issue-pipeline-20261120-040158
TASK_DIR: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/
FEATURE_SLUG: issue-pipeline

TEMPLATE: 02 (full tech reference creation with discovery, research, synthesis, assembly)

SOURCE ROOT AND SAFETY RULES (embed in EVERY agent prompt in the task file):
- All current-state source files live under /home/coder/.cache/ic-snap-20261120/master (read-only export of origin/master 61ac2c2e6; same layout as the repo root). Agents MUST read source only from there, and MUST NEVER modify anything under it. Do not read source from /home/coder/workspaces/IronClaude (that checkout is stale) except for the removed-code appendix, which is read ONLY with: git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>  (read-only git).
- Agents write ONLY inside the task folder (research/, synthesis/, qa/, reviews/, gaps-and-questions.md, task file) and, for the assembler and its fix agents, the final output file named above. Nothing else anywhere. Do not stage or commit anything.
- Any GitHub access is read-only `gh` with `--repo IronbellyOrg/IronClaude`. Never touch SuperClaude-Org. UV only for Python (`uv run python -I ...`; never bare python or pip). Never print or copy secrets.
- No agent may send repository or owner details to external services (no web research is planned).
- Only files are sources. Do not cite memory notes or chat claims about "zero-setup watcher", "COORD-", "dispatcher" or "grant rows" as facts; if the code and docs do not contain them, write "not found in snapshot".
- Line numbers are for the 61ac2c2e6 snapshot and must be re-read from the live file before being cited.

DOCUMENTATION STALENESS WARNINGS (from scope discovery; Phase 2 agents must re-verify each by reading code):
- docs/designs/issue-watcher.md sec 14 gives clock skew 300 s; code cycle.py:44 SKEW_WARN_S = 60 and the doc's own sec 7.5 says 60 [CODE-CONTRADICTED].
- cycle.py:35 MAX_LAUNCHES_PER_CYCLE is defined and never read (dead constant); the one-launch limit is enforced by self.halt (cycle.py ~833).
- docs/designs/issue-watcher-setup.md cites a WORKER-CONTRACT.md section "Issue pipeline duties" that does not exist at 61ac2c2e6, omits `--pipeline none` in launch commands, and has no dispatcher or zero-setup install step. docs/designs/issue-watcher-live-test.md does not exist, so all `_assumed_shape` fixtures are still assumed.
- docs/designs/issue-pipeline-fu1.md uses `superclaude issue-pipeline plan-hash/check-approval`, a command group that no longer exists.
- docs/designs/issue-pipeline-guard-g2.md line references have drifted; its G2 rule 1 / route A (`release-worker`) is retired; nothing in src calls `orca_worktree.py pending`.
- docs/designs/sc-issue-launch-level-hook.md lists IMPL skills implement, task, improve, cleanup, spawn, build; code launch-level-guard.sh ~l.409 has implement|task|cleanup only; the design also contradicts itself on a typed `approved` (row 34 vs section 6).
- docs/designs/sc-issue-command.md status says "Design only (nothing implemented)" yet the command and skill exist; T3 model pin differs from the agent file; sc-issue-claim-pipeline-flag.md level table still calls `worktree` the default (the real rule is prose at refs/claim.md:81).
- The ccsession shim does NOT carry the launch level (the level travels by files under ~/.claude/state/launch-level/); the claim only detects the shim.
Do NOT create task items that build on any of these as if true. Phase 2 agents tag every doc-sourced claim [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED].

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 1 (Preparation): Update task status, confirm scope from research notes, read the template, select depth tier (Standard), confirm task folder subfolders exist.
- Phase 2 (Deep Investigation): L1 Discovery. SIX agents (one checklist item each, spawned in parallel), assignments in research-notes.md SUGGESTED_PHASES table (01 watcher decision engine; 02 watcher I/O github-launch-record; 03 watcher operator surface and setup; 04 claim flow and orca_worktree.py; 05 guard stack and ccsession; 06 coordinator text and removed code). Output files research/01-...md to research/06-...md as named in research-notes.md RECOMMENDED_OUTPUTS. Each agent first reads its scope-discovery file(s) under ${TASK_DIR}scope/ (scope-1..scope-6, mapping given in research-notes.md) as hints, then verifies by reading the live source lines. Each prompt carries the Incremental File Writing Protocol, the Documentation Staleness Protocol and the C8 defect rule (as adapted below). Each must also produce, for its area: a test-pin table (one row per test file: path, lines, what it pins, which behaviour), a "what runs live vs switched off" status line, a "writes to GitHub" list (exact command), triggers, state stores and gates.
- Phase 3 (Completeness Verification): L4 Review/QA at qa_intensity standard: spawn 1 rf-analyst (completeness-verification lens), 1 rf-qa (evidence-quality lens) and 1 rf-qa-qualitative (research-depth lens) IN PARALLEL, all fix_authorization: false. Consolidate into qa/qa-research-consolidated-findings.md; gap-filling research agents for blocking gaps; 2-agent verification round; max 2 cycles then HALT and escalate to the team lead (agent name team-lead) via SendMessage with the open blocking findings.
- Phase 4 (Web Research): SKIPPED with rationale (repo-internal subject; external sources cannot change verified code findings; no repository details may go to outside services). The task file contains one checklist item recording the skip rationale in the Task Log and checking it off.
- Phase 5 (Synthesis + Synthesis Gate): L2 Build-from-Discovery. SIX synthesis agents (one item each) producing synthesis/synth-01..06 as named in research-notes.md RECOMMENDED_OUTPUTS. Then gate at standard intensity: 1 rf-analyst (synthesis-accuracy + source-tracing), 1 rf-qa (structure + content-quality), 1 rf-qa-qualitative (synthesis-coherence) in parallel, fix_authorization false; consolidate; ONE rf-qa fix agent (fix_authorization true) for blocking findings only (minor findings stay as notes); 2-agent verification round; max 2 fix cycles then HALT and escalate. Partitioning threshold >4 synthesis files applies: with 6 synth files spawn each lens type in 2 partitions (assigned_files: synth-01..03 and synth-04..06), each partition writing a numbered report; merge reports.
- Phase 6 (Assembly + Lens-Based QA + Source Fidelity Gate): L6 Aggregation. ONE rf-assembler (subagent_type rf-assembler) assembles the final document at /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md (incrementally; frontmatter first; sections in template order; ToC; Appendix "Removed on 2026-11-20"). Then standard-intensity Gate 3: 3 rf-qa structural lenses (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content lenses (actionability, domain-accuracy, crossref-chain) + 1 domain lens (code-example-accuracy; for this document the "examples" are quoted commands, argv, exit codes and constants: verify each against the source) = 7 agents in parallel, fix_authorization false; consolidate; ONE fix agent; 2-agent verification; max 2 fix cycles then HALT. Then Gate 4 source fidelity: 2 rf-qa fidelity agents (semantic-coverage; detail-preservation) each reading assigned source files from SOURCE ROOT AND the full assembled document; serialized fix; verification; max 2 cycles. Step 6d verifies all QA complete.
- Phase 7 (Present to User & Complete Task): anti-orphaning, task-completion items inside this phase: summary to the Task Log, frontmatter status Done and completion_date, list artifacts. No archival of source docs (nothing is consolidated).

C8 ADAPTATION (NO_DOCS_CLOSE_DEFECT, adapted to this run's write restriction): any in-scope capability that a design doc names as built or intended but that is unwired, switched off, retired or has no caller must be recorded in Section 14 as a DEFECT CANDIDATE or NOT BUILT row with the declaring doc line and the code evidence. It must not be re-labelled as a "known gap" without a cited decision. Remediation tasks under .dev/tasks/to-do/ are NOT created, because this run may write nowhere outside its task folder and the output file; Section 14 states this explicitly and lists the candidates for the owner.

QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: PER_PHASE
  Gate 1: Research Completeness (Phase 3): standard = 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles. (6 research files: no partitioning, threshold is >6.)
  Gate 2: Synthesis Quality (Phase 5): standard = 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents, each lens partitioned in 2 because there are 6 synth files (>4). Max 2 fix cycles.
  Gate 3: Final Document Lens-Based QA (Phase 6, step 6a): standard = 3 rf-qa structural + 3 rf-qa-qualitative content + 1 domain lens (code-example-accuracy) = 7 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, step 6c): standard = 2 rf-qa fidelity agents (semantic-coverage + detail-preservation). Max 2 fix cycles.
  NOTE: the rf-task-builder applies the I22 reductions via the QA Intensity Adaptation table in the SKILL.md. The team lead explicitly requested the Standard tier, so Standard intensity governs; the skill's "absolute floor of 5 agents per gate" (Critical Rules 8 and 19) is a Heavyweight/full requirement and is superseded here by this BUILD_REQUEST's QA_GATE_REQUIREMENTS, which the SKILL.md states take precedence.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + SOURCE_FIDELITY + NO_DOCS_CLOSE_DEFECT
  TEMPLATE_COMPLIANCE: All sections from technical_reference_template.md present or marked N/A with rationale (Section 7 Component Inventory is N/A: not a UI feature).
  EVIDENCE_TRAIL: Every claim cites path:line against the 61ac2c2e6 snapshot.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  SOURCE_FIDELITY: Phase 6 Gate 4 agents read the actual source files AND the assembled reference; quoted argv, constants, exit codes, field names and state names must match the code verbatim.
  NO_DOCS_CLOSE_DEFECT: as adapted above.
  CONTENT REQUIREMENTS BEYOND THE TEMPLATE (assembler and QA must check): (a) a "what runs live vs switched off" ledger, one row per piece (watcher, claim, L1, L2, identity, G2 rule 2, coordinator text, removed package) with status words BUILT-ON / BUILT-OFF (enabled:false) / NOT BUILT / REMOVED plus evidence; (b) a "writes to GitHub" table per piece with the exact commands; (c) a trigger table; (d) a test-pin matrix with one row per test file listed in research-notes.md EXISTING_FILES, giving path, lines and what it pins; (e) a doc-vs-code contradiction table; (f) the Appendix "Removed on 2026-11-20"; (g) exactly one sentence saying PR 686 / the rewrite design is out of scope and NO other description of it.

TESTING_REQUIREMENTS: N/A: documentation-only skill, no code produced, no tests applicable.

RESEARCH NOTES FILE:
/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research-notes.md
Read this file FIRST for full findings: existing files, patterns, planned investigation assignments (SUGGESTED_PHASES), synthesis mapping, and output paths. Scope-discovery detail files are in /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/scope/.

TEMPLATE_PATH: /home/coder/workspaces/IronClaude/.claude/templates/documents/technical_reference_template.md
OUTPUT_PATH: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md

SKILL CONTEXT FILE:
/home/coder/workspaces/IronClaude/.claude/skills/tech-reference/SKILL.md  (identical installed copy: /home/coder/.claude/skills/tech-reference/SKILL.md)
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Synthesis Agent Prompt, the analyst/QA/lens/fidelity prompts, Assembly Agent Prompt. Read "Synthesis Mapping Table", "Synthesis Quality Review Checklist", "Assembly Process", "Validation Checklist", "Content Rules", "Tier Selection", "Output Structure". These must be embedded in the relevant checklist items per B2 self-contained pattern (the /task executor does not read SKILL.md). Use ABSOLUTE paths in every checklist item (the executor's working directory may not be the repo root).

CRITICAL: GRANULARITY REQUIREMENT:
Per MDTM template rules A3 and A4, create individual checklist items for EVERY research agent (6), every synthesis file (6), every QA lens agent, consolidation, fix agent, verification agent and fidelity agent. No batch items like "spawn all research agents". The research notes SUGGESTED_PHASES section has per-agent detail for this.

ESCALATION:
Since you are running as a subagent (not a teammate), you have NO team context. Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage; these tools will fail. This overrides your agent definition's Critical Rule 6 and Step 6. Return the task file path as your final output.
- Codebase questions: use `mcp__litellm__augment_code-augment_code_search` (else mcp__auggie__codebase-retrieval) or Grep on the SOURCE ROOT (the Augment index sees pushed code only).
- If blocked: create the best task file you can and note gaps in the Task Log section.

SKILL PHASES TO ENCODE IN TASK FILE: Phases 1-7 as in TEMPLATE 02 PATTERN MAPPING above, each item self-contained (B2). Embed the Codebase Research Agent Prompt (with Incremental File Writing Protocol, Documentation Staleness Protocol and the adapted C8 rule), the Synthesis Agent Prompt (with rules 0-12), the rf-analyst completeness prompt, the rf-qa research gate prompt, the rf-qa-qualitative research-depth lens, the Synthesis QA prompt, the lens prompts, the fidelity prompt template and the Assembly Agent Prompt from SKILL.md, each customised with the topics, absolute file paths and output paths named above. Every research-agent prompt must include the SOURCE ROOT AND SAFETY RULES block verbatim.

TASK FILE LOCATION: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/TASK-TECHREF-issue-pipeline-20261120-040158.md

STEPS:
1. Read the research notes file (MANDATORY)
2. Read the SKILL.md file named above (MANDATORY)
3. Read the MDTM template /home/coder/workspaces/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md (MANDATORY)
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section
6. Create the task file at the TASK FILE LOCATION using PART 2 structure
7. Return the task file path
