# BUILD REQUEST

Source: skill-delegated
Calling Skill: skill-creator
Task Directory: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-SKILLCREATE-persona-research-20260429-212627/
Research Notes: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-SKILLCREATE-persona-research-20260429-212627/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Generate a new SKILL.md for `sc-persona-research-protocol` following the 29-section RF
standard structure. The skill produces public-surface persona dossiers and BMAD-roster-ready
TOML persona blocks for *named real public figures*, modeled on observable public posture only
(no first-person attributed quotes, no impersonation). Output to
`.temp/skills/sc-persona-research-protocol/SKILL.md` with all canonical sections populated —
shared boilerplate verbatim from `tech-research/SKILL.md` (the de-facto template since
`.claude/templates/documents/skill_template.md` does not exist), domain sections generated from
the confirmed 10-differentiator model in research-notes.md, Stage A/B workflow configured for
the persona-research pipeline (identity verification → archetype resolution → parallel research
workers → aggregator → approval gate → optional validator), and 7-phase task-file structure
encoded in A.7's BUILD_REQUEST template. Plus 2 companion agent files generated via agent-creator
nesting in Phase 7: `rf-personares-archetype-driven-research-worker` and `rf-personares-discovery-worker`.

WHY: User has a board-prep workflow that needs to stress-test pitch material against the likely
posture of named investor-side decision-makers (e.g., crypto-VC partners, gaming-VC partners,
strategic-corporate execs). No end-to-end open-source tool exists for the "named real person →
public-surface research → LLM persona" pipeline; this skill fills the gap with TinyTroupe's
ethics framing as the floor (no first-person attributed quotes, modeled-on disclaimer mandatory,
refuse on unsuitable subjects). Architectural payoff: parallel research per subject, archetype
reuse + refinement loop across runs, deterministic explainable matching, model-tiering caps
Opus spend at <15% of total tokens.

TASK_ID_PREFIX: TASK-SKILLCREATE

DOMAIN_NAME: sc-persona-research-protocol
DOMAIN_SLUG: sc-persona-research-protocol
OUTPUT_TYPE: distributed
REFERENCE_SKILLS: tech-research, skill-creator, task-builder, prd, tdd
AGENT_FILES: true

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
- `.claude/templates/documents/skill_template.md` is MISSING. Phase 1 must use
  `tech-research/SKILL.md` (1322 lines, full 29-section RF format) as the canonical structural
  reference. All COPY-classified sections must be byte-matched against the equivalent section
  in tech-research, NOT against the missing template. Surface this gap in the Phase 7 summary
  as a follow-on user action ("promote tech-research's structure to a sanitized skill_template.md
  for future runs").
- Spec §12 contains 9 open questions. v1 defaults adopted: deterministic keyword-overlap matcher
  (§F), Tavily-preferred routing with fallback on 5xx (§9.2 + OQ-9), `<prefix>-<lastname>-mod`
  naming convention (OQ-1). Surface other open questions as "future-work" notes in the generated
  SKILL.md's Operational Concerns / Critical Rules.
- All other architecture claims in the spec are NOT documentation-staleness risks because
  the spec is itself the source of truth (it is a *forward-looking* specification, not a
  description of existing code). Phase 2b spec-analyst agents do NOT need to perform
  documentation cross-validation against existing code — there is no existing code yet.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:

- **Phase 1 (Preparation): L0 Setup** — create output directory at
  `.temp/skills/sc-persona-research-protocol/`, verify task subdirectories exist (research/,
  synthesis/, qa/, reviews/), read research-notes.md + tech-research SKILL.md (canonical 29-section
  reference) + Template 02 MDTM template, validate all inputs (10-differentiator model populated;
  reference skill paths exist; AGENT_FILES=true; spec partitioning strategy locked), update task
  frontmatter to "Doing".

- **Phase 2 (Reference Skill Analysis + Spec Partitioning + Section Classification): L1 Discovery** —
  Phase 2a: 5 parallel Reference Skill Analyst agents (1 per reference skill: tech-research,
  skill-creator, task-builder, prd, tdd). Phase 2b: 3 parallel Spec Analyst agents (each gets
  ~330 lines of the 993-line spec — Part 1 §0-§5+AppA-B, Part 2 §6-§9+AppC-D, Part 3
  §10-§12+AppE-F — per skill-creator Critical Rule 18 mandatory partitioning for >1000-line
  inputs; spec is 993 but combined with guide is far over threshold). Phase 2c: 2 parallel Guide
  Analyst agents (best-practices guide is 2088 lines). Phase 2d (sequential, depends on 2a+2b+2c):
  1 Section Classifier agent reads files 01-10 and produces unified 29-row classification table
  → `11-section-classification.md`. **MANDATORY:** Phases 2a, 2b, 2c spawn ALL their agents in a
  single message with multiple Agent tool calls in parallel. Phase 2d is sequential (depends on
  files from 2a-2c).

- **Phase 3 (Completeness Verification): L4 Review/QA** — full intensity, 6 lens-based agents
  (all `fix_authorization: false`): rf-analyst (completeness-verification, cross-validation) +
  rf-qa (evidence-quality, gap-detection) + rf-qa-qualitative (research-depth, research-breadth).
  Step 3.1: spawn all 6 in parallel. Step 3.2: consolidate findings → `qa-research-consolidated-findings.md`.
  Step 3.3: 1 fix agent (rf-qa, fix_authorization: true) applies all corrections. Step 3.4:
  verification round (2 agents: rf-qa evidence-quality + rf-qa-qualitative research-depth,
  fix_authorization: false). Max 3 fix cycles; unresolved → Open Questions in task file.

- **Phase 4 (Skeleton Assembly + Domain Generation): L2 Build-from-Discovery** — sequential
  incremental Edit, NO one-shot Writes (skill-creator Critical Rule 9). Sub-phase 1: Create
  `.temp/skills/sc-persona-research-protocol/SKILL.md` with frontmatter + S1-S4 (boilerplate
  copy from tech-research with domain noun substitution: `name: sc-persona-research-protocol`,
  description from spec frontmatter, trigger phrases from research-notes TRIGGER_PATTERNS,
  TASK-PERSONARES paths in Variable Reference). Sub-phase 2: Append S5-S18 (Input with all 6
  spec §3 input subsections; Depth Tiers; Output Locations distributed pattern; Execution
  Overview; Stage A boilerplate A.1-A.6; A.7 BUILD_REQUEST template customized for the
  persona-research workflow with the 7 phases mapped). Sub-phase 3: Append S19-S20 (Stage B
  delegation verbatim from tech-research with DOMAIN_NAME substituted; Agent Prompt Templates
  with 6 domain agents — Identity Verifier, Archetype Matcher [no LLM, deterministic],
  Archetype-Driven Research Worker, Discovery Worker, Aggregator, Validator — plus 6 lens QA
  prompts and 3 source-fidelity prompts; ALL protocol blocks COPIED VERBATIM from tech-research:
  Incremental File Writing Protocol, Documentation Staleness Protocol, ADVERSARIAL STANCE,
  VERDICTS). Sub-phase 4: Append S21-S29 (Output Structure mapping spec §3 outputs;
  Synthesis Mapping reference table noting incremental Edit assembly; Synthesis Quality Review
  Checklist; Assembly Process; Validation Checklist with 30+ checkboxes mapping FR-1..FR-26 +
  spec §11 acceptance criteria; Content Rules with boilerplate 6 rows + 4 domain rows for ethics
  disclaimer / no-first-person attribution / archetype generic purity / source citation
  requirements; Critical Rules 1-22 boilerplate + 23-28 domain extensions covering FR-2 sequential
  identity gate, FR-6 disclaimer non-negotiable, FR-22 archetype generic purity linter, FR-25
  Tavily-routing mandate, FR-24/FR-26 Opus-spend cap, fabrication-on-leading-questions hard gate;
  Session Management boilerplate; Research Quality Signals with domain-specific strong/weak
  examples).

- **Phase 5 (Lens-Based Structural + Qualitative QA Gate + Source-Fidelity Gate): L4 Review/QA** —
  full intensity. Step 5.1: 6 lens agents in parallel (all `fix_authorization: false`):
  rf-qa (template-conformance, internal-consistency, evidence-quality) + rf-qa-qualitative
  (actionability, domain-accuracy, section-classification-accuracy). Step 5.2: consolidate.
  Step 5.3: 1 fix agent. Step 5.4: verification round. Max 2 cycles. Step 5.5 Source-Fidelity
  Gate: 3 agents in parallel (fix_authorization: false): rf-qa fidelity-1 (reads 5 reference
  skill files + generated SKILL.md; checks semantic coverage); rf-qa fidelity-2 (reads spec
  partition files 06-08 + generated SKILL.md; verifies every FR-1..FR-26 represented and the
  §10 ethics layer is fully encoded); rf-qa-qualitative fidelity-3 (reads spec + reference
  skills + generated SKILL.md; checks domain-noun leakage — no tech-research / prd / tdd /
  skill-creator nouns leaked into SUBSTITUTE/GENERATE sections of the persona-research skill).
  Step 5.6: consolidate fidelity findings. Step 5.7: fix agent + verification. Max 2 cycles
  (Gate 2.5).

- **Phase 6 (Lens-Based Final QA): L6 Aggregation** — 6 lens agents on assembled SKILL.md
  (all `fix_authorization: false`): rf-qa (template-conformance, completeness) + rf-qa-qualitative
  (section-classification-accuracy, actionability, numbers-metrics — line count 1200-1500 for
  Deep tier, FR coverage 26/26, ceremony minimums met, domain-noun-leakage). Consolidate, fix,
  verify (max 2 cycles). Generate `final-quality-report.md`.

- **Phase 7 (Present to User & Complete Task): L0 Closeout** — Step 7.1: present summary
  (skill output path, line count, section count 29, FR coverage, depth tier, ambiguities
  carried forward). Step 7.2 (AGENT_FILES=true): invoke agent-creator nesting SEQUENTIALLY
  (NOT parallel — agent-creator is interactive):
    7.2a: `Skill(skill: "agent-creator", args: "agent_name: personares-archetype-driven-research-worker, agent_role: Reads matched archetype source_recipe and slot_schema; fills slots from subject evidence; calls Tavily MCP per source category; uses Haiku for per-source extraction and Opus for cross-source consolidation per spec §9.2 model tiering; emits §5.2 worker-contract JSON including identity_verification, archetype_resolution with match_path, slot_bindings, footprint_score, dossier_markdown, sources, stable_traits, three_questions, persona_toml_block, archetype_refinement_proposal; honors per_subject_minutes budget; returns INSUFFICIENT_PUBLIC_DATA on footprint_score<3 without fabricating; agent_family: research, parent_skill: sc-persona-research-protocol")`
    7.2b: `Skill(skill: "agent-creator", args: "agent_name: personares-discovery-worker, agent_role: Same model tiering as archetype-driven worker but broader source sweep using bootstrap generic_public_figure recipe; longer budget per archetype_discovery_minutes; emits both subject dossier AND a proposed archetype.yaml derived from this subject's research per §5.2 discovered_archetype_proposal; does NOT include person/firm names in the proposed archetype's core fields per FR-22 generic-purity; agent_family: research, parent_skill: sc-persona-research-protocol")`
    Note: agent-creator adds `rf-` prefix automatically — do NOT include `rf-` in agent_name.
    On per-agent failure: log + continue (SKILL.md remains valid without companion agents).
  Step 7.3: offer test-run suggestion ("Test the new skill with a single low-stakes subject —
  e.g., a well-documented public crypto-VC partner — and run with `--validate` to exercise the
  three-questions test gate"). Step 7.4: update task frontmatter to "Done". Step 7.5: write
  task log entry capturing FR coverage, line count, agent files created, and the
  copy-to-`src/` recommendation.

QA_INTENSITY: full
QA_GATE_REQUIREMENTS: PER_PHASE
  Gate 1: Research Completeness (Phase 3) — full intensity:
    - 6 lens agents (2 rf-analyst + 2 rf-qa + 2 rf-qa-qualitative across completeness,
      cross-validation, evidence-quality, gap-detection, research-depth, research-breadth lenses)
    - All `fix_authorization: false` (report-only)
    - Consolidate findings → 1 fix agent (rf-qa, fix_authorization: true) → 2-agent verification
    - Max 3 fix cycles; unresolved → Open Questions
    - Partitioning: research files >6 (we have 11) → no per-agent partitioning of files needed
      (each lens agent reads all relevant files)

  Gate 2: Lens-Based Structural + Qualitative QA (Phase 5) — full intensity:
    - 6 lens agents (3 rf-qa structural: template-conformance, internal-consistency,
      evidence-quality + 3 rf-qa-qualitative content: actionability, domain-accuracy,
      section-classification-accuracy)
    - All `fix_authorization: false`
    - Consolidate → 1 fix agent → 2-agent verification
    - Max 2 fix cycles

  Gate 2.5: Source-Document Fidelity (Phase 5, after Gate 2) — full intensity:
    - 3 fidelity agents (rf-qa reference-skill semantic coverage + rf-qa spec FR-coverage +
      rf-qa-qualitative domain-noun-leakage)
    - All `fix_authorization: false`
    - Consolidate → 1 fix agent → verification
    - Max 2 fix cycles

  Gate 3: Lens-Based Final QA (Phase 6) — full intensity:
    - 6 lens agents (2 rf-qa: template-conformance, completeness + 4 rf-qa-qualitative:
      section-classification-accuracy, actionability, numbers-metrics, domain-noun-leakage)
    - All `fix_authorization: false`
    - Consolidate → 1 fix agent → 2-agent verification
    - Max 2 fix cycles

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION +
  ETHICS_DISCLAIMER_VERBATIM + NO_FIRST_PERSON_ATTRIBUTION + ARCHETYPE_GENERIC_PURITY +
  IDENTITY_VERIFIED_BEFORE_RESEARCH + WORKER_JSON_CONTRACT_CONFORMANCE +
  PIPELINE_QUANTITY_FLOW_DIAGRAM_PRESENT + GUARD_BOUNDARY_TABLE_PRESENT + SECTION_COUNT_29

  TEMPLATE_COMPLIANCE: All 29 canonical sections present in correct ordering (per
    tech-research/SKILL.md as canonical reference since skill_template.md is missing).
  EVIDENCE_TRAIL: Every generated section cites the domain model field(s) it depends on or
    the spec FR / section it satisfies.
  CROSS_VALIDATION: COPY sections byte-match tech-research's equivalent sections; SUBSTITUTE
    sections have no leftover tech-research/skill-creator/prd/tdd domain nouns.
  ETHICS_DISCLAIMER_VERBATIM: The §10.1 disclaimer string appears verbatim in the generated
    SKILL.md's Critical Rules and is enforced in S25 Validation Checklist.
  NO_FIRST_PERSON_ATTRIBUTION: Generated SKILL.md describes static and dynamic checks
    enforcing FR-7 (no `<Name> said` patterns; no quoted strings preceded by colon).
  ARCHETYPE_GENERIC_PURITY: Generated SKILL.md describes the FR-22 linter check (archetype
    display_name / persona_description_template / stable_traits MUST NOT mention any specific
    firm/person/fund name).
  IDENTITY_VERIFIED_BEFORE_RESEARCH: Generated SKILL.md encodes FR-2's sequential gate —
    research worker for a subject SHALL NOT spawn until identity_verified=true for that subject.
  WORKER_JSON_CONTRACT_CONFORMANCE: Generated SKILL.md's S20 Agent Prompt Templates include
    the exact §5.2 JSON contract structure for both archetype-driven and discovery worker
    outputs.
  PIPELINE_QUANTITY_FLOW_DIAGRAM_PRESENT: Generated SKILL.md instructs runtime emission of the
    §B quantity-flow diagram per FR-12.
  GUARD_BOUNDARY_TABLE_PRESENT: Generated SKILL.md instructs runtime emission of the §A
    guard-condition boundary tables (G1-G4) on every run.
  SECTION_COUNT_29: Exactly 29 sections present.

TESTING_REQUIREMENTS: N/A — skill generation, no executable code produced. (The companion
agents generated by agent-creator nesting in Phase 7 will inherit their own validation
requirements from agent-creator's own QA gates.)

RESEARCH NOTES FILE:
/config/workspace/IronClaude/.dev/tasks/to-do/TASK-SKILLCREATE-persona-research-20260429-212627/research/research-notes.md

Read this file FIRST for full detailed findings including: existing skill inventory, structural
patterns, reference skill analysis with section-level COPY/SUBSTITUTE/GENERATE classification
preview, confirmed 10-differentiator domain model with HIGH-confidence reasoning, synthesis
mapping (research files → output sections), suggested 7-phase structure with per-phase agent
counts and parallel-vs-sequential discipline, template notes (skill_template.md missing
fallback), and ambiguities for user.

SKILL CONTEXT FILE:
/config/workspace/IronClaude/.claude/skills/skill-creator/SKILL.md

Read the "A.3: Perform Scope Discovery" section for the 10-differentiator domain model
definition. Read the "Agent Prompt Templates" section for the agent prompts to embed in
checklist items (Reference Skill Analyst, Section Classifier, Research Analyst Agent,
Research QA Agent, Template-Conformance Lens, Internal-Consistency Lens, Evidence-Quality
Lens, Actionability Lens, Domain-Accuracy Lens, Section-Classification-Accuracy Lens,
Research Depth QA, Research Breadth QA, Source-Fidelity Agent — 13 prompt templates).
Read the "Validation Checklist" section for acceptance criteria for the generated SKILL.md.
Read the "Content Rules" section for non-negotiable formatting and quality standards.
These must be embedded in the relevant checklist items per B2 self-contained pattern.

SOURCE SPEC FILE:
/config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md
(993 lines — partition into 3 slices for Phase 2b agents per skill-creator Critical Rule 18:
Part 1 lines 1-360, Part 2 lines 361-660, Part 3 lines 661-993 covering ethics+acceptance+
appendices E-F)

BEST-PRACTICES GUIDE FILE:
/config/workspace/IronClaude/docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
(2088 lines — partition into 2 slices for Phase 2c agents: Part 1 lines 1-1044 covering
Skills section, Part 2 lines 1045-2088 covering Agents and Commands sections)

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process Structure),
you MUST create individual checklist items for EVERY research agent, every spec partition
agent, every guide partition agent, every QA lens agent, every fix agent, every verification
agent, every assembly sub-phase, and every closeout step. Do NOT batch items like "spawn all
6 lens agents" — each lens agent gets its own `- [ ]` item. The research-notes SUGGESTED_PHASES
section is structured to enable this granularity.

Expected checklist item counts per phase (approximate):
- Phase 1: ~5 items (mkdir, verify, read, validate, frontmatter update)
- Phase 2: ~12 items (5 reference + 3 spec + 2 guide + 1 classifier + 1 phase-gate close)
- Phase 3: ~10 items (6 lens spawns + 1 consolidate + 1 fix + 2 verification)
- Phase 4: ~8 items (4 sub-phases × 2 items each: write + verify)
- Phase 5: ~14 items (6 lens + 1 consolidate + 1 fix + 2 verify + 3 fidelity + 1 fidelity-consolidate + 1 fidelity-fix + 2 fidelity-verify)  
- Phase 6: ~10 items (6 lens + 1 consolidate + 1 fix + 2 verify + 1 final report)
- Phase 7: ~7 items (summary + 2 agent-creator nests + test suggestion + frontmatter update + task log + copy-to-src recommendation)
**Total: ~66 checklist items minimum.**

TO BUILD A GOOD TASK FILE, YOU NEED:
- Goal and outputs (covered above)
- Source files and context (research-notes.md + tech-research/SKILL.md + spec + guide)
- Phases and steps (research-notes SUGGESTED_PHASES + this BUILD_REQUEST phase mapping)
- Verification criteria (per VALIDATION_REQUIREMENTS above)
- Dependencies (Phase 2d depends on 2a+2b+2c; Phases 3,5,6 are gates; Phase 4 is sequential
  incremental Edit; Phase 7 conditional on AGENT_FILES=true)

ESCALATION:
You are running as a subagent (skill-delegated). You have NO team context. Do NOT broadcast
TASK_READY, use TaskCreate, or use SendMessage — these tools will fail. This overrides your
agent definition's broadcast rules. Return the task file path as your final output.
- Codebase questions → use auggie MCP / Grep / Read
- External docs/syntax → not needed for this build (all sources are local files)
- If blocked → create the best task file you can and note gaps in the Task Log

SKILL PHASES TO ENCODE IN TASK FILE (each item B2 self-contained — full agent prompts
embedded; full file paths embedded; full validation criteria embedded):

**PHASE 1: PREPARATION (L0)**
Items 1.1 through 1.5 per the phase mapping above. Each item is sequential, no parallelism.

**PHASE 2: REFERENCE SKILL ANALYSIS + SPEC PARTITIONING + SECTION CLASSIFICATION (L1)**
- Phase 2a (5 PARALLEL agents): one item per reference skill (tech-research, skill-creator,
  task-builder, prd, tdd). Each item embeds the FULL Reference Skill Analyst Prompt from
  skill-creator's S20, customized with that skill's path. ALL 5 ITEMS MUST BE SPAWNED IN A
  SINGLE MESSAGE — note this in each item's "ensuring..." clause.
- Phase 2b (3 PARALLEL agents): one item per spec slice (Part 1: lines 1-360, Part 2: lines
  361-660, Part 3: lines 661-993). Embed a Spec Analyst prompt (variant of Reference Skill
  Analyst tuned for spec-document analysis instead of skill-file analysis: extract FRs,
  architecture components, ethics rules, validation criteria; flag any contradictions across
  the partition boundary). All 3 items spawn in a single message.
- Phase 2c (2 PARALLEL agents): one item per guide slice (Skills section, Agents+Commands
  section). Embed a Guide Analyst prompt (extract authoring conventions, anti-patterns to
  avoid, ceremony minimums). Both items spawn in a single message.
- Phase 2d (1 SEQUENTIAL agent — depends on 2a-2c outputs): Section Classifier reads files
  01-10 and produces the unified 29-row classification table. Embed the FULL Section Classifier
  Prompt from skill-creator's S20.

**PHASE 3: COMPLETENESS VERIFICATION (L4)**
- 3.1a-3.1f: 6 PARALLEL lens agents — all spawn in a single message. Each item embeds the
  FULL agent prompt from skill-creator's S20: Research Analyst (completeness-verification),
  Research Analyst (cross-validation — adapt the completeness prompt for cross-validation
  lens), Research QA (evidence-quality), Research QA (gap-detection), Research Depth QA,
  Research Breadth QA. All `fix_authorization: false`.
- 3.2: SEQUENTIAL — consolidate 6 lens reports into `qa-research-consolidated-findings.md`.
- 3.3: 1 fix agent (rf-qa, fix_authorization: true).
- 3.4: 2-agent verification round in parallel.
- VERDICT gate: PASS → Phase 4. FAIL → repeat 3.3-3.4 max 3 cycles.

**PHASE 4: SKELETON ASSEMBLY + DOMAIN GENERATION (L2)**
- 4.1: SEQUENTIAL — Sub-phase 1: copy frontmatter + S1-S4 from tech-research (with domain
  substitution) into `.temp/skills/sc-persona-research-protocol/SKILL.md`. Use Edit for
  incremental writes — NEVER one-shot Write. Verify byte-match on COPY classifications and
  correct domain noun substitution on SUBSTITUTE classifications.
- 4.2: SEQUENTIAL — Sub-phase 2: append S5-S18 (Input through A.7 BUILD_REQUEST). Item must
  embed the full S5 input field list (6 spec §3 input subsections), the full Depth Tiers table,
  the distributed Output Locations table, the 7-phase Execution Overview, the Stage A boilerplate
  flow, and the A.7 BUILD_REQUEST template customized for the persona-research workflow.
- 4.3: SEQUENTIAL — Sub-phase 3: append S19-S20 (Stage B + 6 domain agent prompts + 6 lens QA
  prompts + 3 source-fidelity prompts). VERBATIM protocol blocks (Incremental File Writing
  Protocol, Documentation Staleness Protocol, ADVERSARIAL STANCE, VERDICTS) must be byte-copied
  from tech-research's equivalent prompts.
- 4.4: SEQUENTIAL — Sub-phase 4: append S21-S29 (Output Structure mapping spec §3 outputs;
  Synthesis Mapping reference table; Quality Review Checklist; Assembly Process; Validation
  Checklist with 30+ checkboxes mapping FR-1..FR-26; Content Rules with 4 domain rows; Critical
  Rules 1-22 boilerplate + 23-28 domain extensions; Session Management; Research Quality
  Signals).

**PHASE 5: STRUCTURAL + QUALITATIVE QA + SOURCE-FIDELITY GATE (L4)**
- 5.1a-5.1f: 6 PARALLEL lens agents — all spawn in a single message. Each item embeds the
  FULL lens prompt from skill-creator's S20: Template-Conformance, Internal-Consistency,
  Evidence-Quality, Actionability, Domain-Accuracy, Section-Classification-Accuracy. All
  `fix_authorization: false`.
- 5.2: SEQUENTIAL — consolidate.
- 5.3: 1 fix agent (rf-qa, fix_authorization: true).
- 5.4: 2-agent verification round in parallel.
- VERDICT gate: PASS → 5.5. FAIL → repeat 5.3-5.4 max 2 cycles.
- 5.5a-5.5c: 3 PARALLEL fidelity agents — all spawn in a single message. Each item embeds the
  FULL Source-Fidelity Agent Prompt from skill-creator's S20, customized: 5.5a (5 reference
  skills + generated SKILL.md), 5.5b (spec partition files 06-08 + generated SKILL.md), 5.5c
  (spec + reference skills + generated SKILL.md → domain-noun leakage). All
  `fix_authorization: false`.
- 5.6: SEQUENTIAL — consolidate fidelity findings.
- 5.7: 1 fix agent + 2-agent verification round.

**PHASE 6: LENS-BASED FINAL QA (L6)**
- 6.1a-6.1f: 6 PARALLEL lens agents — all spawn in a single message. Each item embeds the
  FULL lens prompt from skill-creator's S20: Template-Conformance, Completeness,
  Section-Classification-Accuracy, Actionability, Numbers-Metrics, Domain-Noun-Leakage. All
  `fix_authorization: false`.
- 6.2: SEQUENTIAL — consolidate.
- 6.3: 1 fix agent (rf-qa, fix_authorization: true).
- 6.4: 2-agent verification round in parallel.
- 6.5: SEQUENTIAL — generate `final-quality-report.md` summarizing all 3 gate outcomes.

**PHASE 7: PRESENT RESULTS & AGENT-CREATOR NESTING (L0)**
- 7.1: SEQUENTIAL — present summary to user (skill output path, line count, section count 29,
  FR coverage 26/26 expected, depth tier Deep, ambiguities carried forward including the
  skill_template.md gap and the .temp→src/ copy recommendation).
- 7.2a: SEQUENTIAL — invoke agent-creator for archetype-driven research worker (full args
  string in the phase mapping above).
- 7.2b: SEQUENTIAL — invoke agent-creator for discovery worker (full args string above).
  These two are SEQUENTIAL not parallel because agent-creator is interactive.
- 7.3: SEQUENTIAL — offer test-run suggestion.
- 7.4: SEQUENTIAL — update task frontmatter to "Done".
- 7.5: SEQUENTIAL — write task log entry capturing: skill output path, line count, section
  count, FR coverage, agent files created (2 expected), copy-to-src recommendation, and
  ambiguities surfaced.

TASK FILE LOCATION:
/config/workspace/IronClaude/.dev/tasks/to-do/TASK-SKILLCREATE-persona-research-20260429-212627/TASK-SKILLCREATE-persona-research-20260429-212627.md

STEPS:
1. Read the research notes file (MANDATORY)
2. Read the skill-creator SKILL.md for embedded agent prompts (MANDATORY)
3. Read the MDTM Template 02 (MANDATORY): `.claude/templates/workflow/02_mdtm_template_complex_task.md`
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained
   items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section
6. Create the task file at TASK FILE LOCATION using PART 2 structure
7. Return the task file path
