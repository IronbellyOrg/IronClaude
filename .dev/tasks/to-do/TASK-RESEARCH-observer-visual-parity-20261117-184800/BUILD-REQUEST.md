# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/
Research Notes: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation on how to redesign the read-only Orca terminal observer (`superclaude observe`) presentation to reach theme, styling and layout parity with its design mockups, driven by the merged findings list `.dev/issues/409/visual-parity/merged/FINDINGS.md` (M-01 to M-18, guards G-1 and G-2, accepted divergences AD-1 to AD-7, open items OPEN-1 to OPEN-3, owner decision O-1), and produce a structured research report with findings, gap analysis, options, and implementation recommendations. The report will be written to `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md`. The seven questions the report must answer with evidence are listed in the research notes (Q1 to Q7) and in WHY below.

WHY: The report feeds a phased redesign spec (Phase 0 = a render-compare harness and baseline; every later phase ends with a render gate: implement, render at widths 160, 116 and 80, a fresh reviewer subagent scores a fixed rubric against the mockup, fix, re-render; at most 3 iterations per phase). A later agent turns that spec into a tasklist with /sc:workflow. The report must therefore answer: (Q1) the safest way to add styled spans, titled boxed panes, a count tile and two-column composition inside the existing line-based screen_lines/render pipeline (Rich Text, Table, Panel, Layout or Columns, versus hand-built lines), keeping text records, JSON snapshot and NO_COLOR/ASCII output unchanged or deliberately changed, and width and height budgets at 160, 116 and 80; (Q2) which tests and goldens change per phase and how to split the work into phases that each leave the suite green; (Q3) the best render-to-image harness for the automated compare loop (Rich export to SVG or HTML with a headless renderer, ANSI to PNG, or text and ANSI-escape assertions with a model-judged rubric), what is available offline in this repo and environment, and how a fresh reviewer subagent scores a fixed rubric against the mockup PNGs; (Q4) ANSI colour depth: what the Rich console does today (color_system standard), the cost and benefit of detecting 256 colour and truecolor via COLORTERM and TERM, the fallbacks, and how muted/slate/amber roles stay distinct at 16 colours; (Q5) whether the live screen path (LiveScreen drawing the renderable directly) keeps styles while the one-shot path calls export_text without styles, and what the styled-capture gate must test; (Q6) a Zellij 0.44.2 go or no-go recommendation with evidence (pane and layout composition, floating panes for the Decision Desk, status or tab bar, theme reuse, screen capture for the render gate), under the conditions that the observer works on its own outside Zellij, stays read-only, and keeps all widths, NO_COLOR and ASCII working; (Q7) how to add a fixture question containing a 64-character hex hash and file paths (PR #591 consideration 8) that must wrap or cut cleanly in the 80-column Decision Desk frame. Standing constraints: read-only, real data only, no invented owners/requester/mapped trees/affected sessions, question text screen-only (never in records or snapshot), NO_COLOR, ASCII mode and widths 160/116/80 keep working, ANSI-styled output is the primary rich mode, no blinking or mouse, PR target IronbellyOrg/IronClaude via /sc:pr-submit --monitor 3. Do not edit product code.

TASK_ID_PREFIX: TASK-RESEARCH

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
None found during scope discovery. Phase 2 agents will perform full documentation cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags. Note: `rendering-rules.md` and the merged findings list describe intent and the 2026-11-17 renders; they are not proof of code behaviour. Verify every code claim in source (for example the header gate in render.py, the console colour system in terminal.py, the one-shot export_text call and LiveScreen in commands.py).
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED] or [UNVERIFIED].

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 2 (Deep Investigation): L1 Discovery. Agents explore the codebase and write findings files to the research/ folder of the Task Directory.
- Phase 3 (Completeness Verification): L4 Review/QA per QA_INTENSITY standard (see QA_GATE_REQUIREMENTS). Serialized fix: consolidate findings, single fix agent, verification round.
- Phase 4 (Web Research): L1 Discovery. Agents explore external sources and write findings files.
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery. Agents read research files and produce report sections; then the synthesis gate per QA_INTENSITY standard. Serialized fix: consolidate, fix, verify.
- Phase 6 (Assembly & Validation): L6 Aggregation. rf-assembler consolidates synthesis files into the final report; then lens-based QA at standard intensity; then the source-document fidelity gate; then the anti-omission gate (Step 6.7b).

QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: PER_PHASE
  Gate 1: Research Completeness (Phase 3), standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
  Gate 2: Synthesis Quality (Phase 5), standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
  Gate 3: Report Validation (Phase 6), standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (finding-reproducibility) = 7 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, after Gate 3), standard: 2 rf-qa fidelity agents. Max 2 fix cycles.
  Gate 5: Anti-Omission (Phase 6, after Gate 4): MANDATORY. standard: 2 rf-analyst anti-omission agents. Max 2 fix cycles. Method: exhaustive enumeration, coverage judged by meaning never by ID citation; every omission recovered or explicitly justified; never silently dropped.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All report sections present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.

TESTING_REQUIREMENTS: N/A. Documentation-only skill (research reports), no code produced, no tests applicable.

RESEARCH NOTES FILE:
/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments (5 codebase agents, 2 web agents), synthesis mapping (6 synth files) and output paths.

SKILL CONTEXT FILE:
/home/coder/.claude/skills/tech-research/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Report Structure" section for the final report format. Read the "Synthesis Mapping Table", "Synthesis Quality Review Checklist", "Assembly Process", "Validation Checklist" and "Content Rules" sections. These must be embedded in the relevant checklist items per B2 self-contained pattern.

CRITICAL: GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process Structure), you MUST create individual checklist items for EVERY research agent, web research topic, synthesis file, and validation step. Do NOT create batch items. The research notes SUGGESTED_PHASES section contains per-agent detail.

SKILL PHASES TO ENCODE IN TASK FILE:
Encode Phases 1 to 7 exactly as defined in the SKILL.md "Stage A.7" BUILD_REQUEST template, at QA_INTENSITY standard (the gate agent counts above). In particular: Phase 1 prepare (status Doing, folders exist already); Phase 2 five codebase agents in parallel; Phase 3 research gate (3 agents) with serialized fix and gaps log at `gaps-and-questions.md`; Phase 4 two web agents in parallel; Phase 5 six synthesis files in parallel then the synthesis gate (3 agents) with serialized fix; Phase 6 rf-assembler, 7-agent lens QA, serialized fix and verification, fidelity gate (2 agents), anti-omission gate (2 agents); Phase 7 present, complete the task, non-blocking suggestion of /tech-reference.

ESCALATION:
Since you are running as a subagent (not a teammate), you have NO team context. Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage. Return the task file path as your final output.
- Codebase questions: use `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) or Grep/Read
- External docs/syntax: use WebSearch
- If blocked: create the best task file you can and note gaps in the Task Log section.

TASK FILE LOCATION: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/TASK-RESEARCH-observer-visual-parity-20261117-184800.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above (MANDATORY)
3. Read the MDTM template: .claude/templates/workflow/02_mdtm_template_complex_task.md (or ~/.claude/templates/workflow/02_mdtm_template_complex_task.md when the project copy is absent) (MANDATORY)
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section
6. Create the task file at the TASK FILE LOCATION using PART 2 structure
7. Return the task file path
