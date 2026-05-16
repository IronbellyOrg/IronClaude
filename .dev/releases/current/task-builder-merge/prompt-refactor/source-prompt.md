# Source Prompt — Task-Builder Convergence Orchestration

Goal: Pull the best qualities of /sc:tasklist into the task-builder skill, producing an
adversarially-validated release spec and a PRD. Where /sc:tasklist and task-builder
disagree, task-builder is authoritative. The FINAL-REPORT studied the inverse direction
(RF → SC); this task inverts it (SC qualities → task-builder).

Anchor document:
  /config/workspace/IronClaude/.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md

Output root: .dev/releases/current/task-builder-merge/

==============================================================================
PHASE 1 — PARALLEL CONTEXT GATHERING  (one message, all Agent calls together)
==============================================================================

Read the anchor document and its siblings in the same folder (file-inventory.md,
dependency-map.md, pipeline-stages.md, architecture-comparison.md,
design-rfmerger-proposals.md, adversarial-validation.md).

Then spawn parallel Agent tool calls (subagent_type: Explore) — one per bucket.
Each agent reads all files in its bucket exhaustively and returns a structured
digest: purpose, public contract, hooks/dependencies, output schemas, and any
cross-references to other buckets.

  Bucket A — src/superclaude/skills/sc-tasklist-protocol/ (SKILL.md + rules/ + templates/)
  Bucket B — src/superclaude/commands/tasklist.md + src/superclaude/cli/tasklist/
  Bucket C — src/superclaude/skills/task-builder/ (SKILL.md + every refs/, rules/,
             templates/, scripts/ file)
  Bucket D — src/superclaude/agents/rf-*.md (rf-task-builder, rf-task-researcher,
             rf-task-executor, rf-team-lead, rf-analyst, rf-qa, rf-qa-qualitative)
  Bucket E — src/superclaude/skills/sc-adversarial-protocol/ (SKILL.md + refs/)
  Bucket F — src/superclaude/examples/release-spec-template.md + sample release
             specs under .dev/releases/current/ for shape reference

==============================================================================
PHASE 2 — STRUCTURED ANALYSIS
==============================================================================

Run:
  /sc:analyze src/superclaude/skills/task-builder src/superclaude/skills/sc-tasklist-protocol \
    --focus architecture --depth deep

Produce two matrices:
  - "sc:tasklist does X, task-builder does not"
  - "task-builder does Y, sc:tasklist does not"
Cross-reference against FINAL-REPORT.md §3, §4, §6.

==============================================================================
PHASE 3 — LONG-FORM BRAINSTORM  (Sequential MCP, 15-25 thoughts minimum)
==============================================================================

Use mcp__sequential-thinking__sequentialthinking to draft a Merge Proposal
Portfolio. Cover at minimum:
  - Determinism: which /sc:tasklist guarantees (keyword scoring, appearance-order
    IDs, explicit tiebreakers) translate to task-builder's agent-research model;
    which are incompatible
  - Traceability: how to inject R-### → T<PP>.<TT> → D-#### chains into MDTM
    items without violating the self-contained-item invariant
  - Quality gates: which of the 17 pre-write checks port to task-builder's
    pre-write validation surface
  - Validation stages: whether the 2N parallel-agent validation belongs in
    task-builder, or whether rf-qa + rf-qa-qualitative already cover it
  - Tier classification: whether the 4-tier compliance classifier is additive
    to MDTM template selection (templates 01 generic / 02 complex)
  - Conflict rule: every case where task-builder's MDTM architecture (parallel
    research, evidence-bound items, persistent .dev/tasks/ artifacts, zero-trust
    QA) conflicts with a /sc:tasklist mechanism, task-builder wins — document
    the rejected mechanism with reasoning

Produce 5-8 proposals. Each: source mechanism, target integration point,
conflict analysis, complexity estimate, expected quality gain. Cite source
files and FINAL-REPORT §5/§7 for every claim. Write each proposal as its own
markdown file under .dev/releases/current/task-builder-merge/proposals/.

==============================================================================
PHASE 4 — ADVERSARIAL VALIDATION
==============================================================================

Run (Mode A requires 2-10 files; batch in passes if needed):
  /sc:adversarial --compare <proposal-1.md,proposal-2.md,...> \
    --depth deep --focus structure,completeness --convergence 0.80 \
    --interactive --output .dev/releases/current/task-builder-merge/adversarial/

The adversarial protocol owns rounds, scoring, and merge logic. Do not inline.

==============================================================================
PHASE 5 — REFLECTION
==============================================================================

Run:
  /sc:reflect --type task --analyze --validate

Verify adversarial outcomes respect the conflict rule. Flag for revision any
proposal whose merged form weakens task-builder's MDTM/zero-trust architecture.

==============================================================================
PHASE 6 — DRAFT RELEASE SPEC
==============================================================================

Produce .dev/releases/current/task-builder-merge/release-spec.md following
src/superclaude/examples/release-spec-template.md. Populate frontmatter
(spec_type, complexity_score, complexity_class, target_release, feature_id).
Include:
  - problem statement citing FINAL-REPORT §1 and §6.3
  - accepted proposals with implementation sequencing
  - constraints section with explicit "task-builder takes precedence in
    conflict" rule
  - FRs per proposal, NFRs (determinism scope, token ceiling, wall-clock),
    risks, assumptions, test plan

==============================================================================
PHASE 7 — SPEC PANEL REVIEW
==============================================================================

Run:
  /sc:spec-panel @.dev/releases/current/task-builder-merge/release-spec.md \
    --mode critique --focus requirements,architecture,correctness \
    --iterations 2 --format detailed --downstream roadmap

Apply expert revisions to the spec. If any expert recommendation contradicts
the "task-builder precedence" rule, defend it with FINAL-REPORT evidence and
accept only revisions that respect it.

==============================================================================
PHASE 8 — PRD GENERATION  (hand-off to skill)
==============================================================================

Invoke:
  > Skill prd

Pass:
  WHAT  = "Task-Builder Convergence: importing /sc:tasklist's best qualities
           into the task-builder skill"
  WHY   = "engineering planning decision document for the v3.8 merger work"
  WHERE = "src/superclaude/skills/task-builder/,
           src/superclaude/skills/sc-tasklist-protocol/,
           src/superclaude/agents/rf-*"
  OUTPUT = ".dev/releases/current/task-builder-merge/PRD_TASK_BUILDER_CONVERGENCE.md"
  INPUT_SPEC = ".dev/releases/current/task-builder-merge/release-spec.md"

The prd skill owns its phasing. Do not inline its protocol.

==============================================================================
GLOBAL CONSTRAINTS
==============================================================================
- task-builder behaviors are authoritative whenever /sc:tasklist and task-builder
  disagree; rejected /sc:tasklist mechanisms must be documented with reasoning
- every claim cites a file path (file:line where applicable); FINAL-REPORT
  citations include section number
- Phase 1 agents spawn in one message
- /sc:adversarial, /sc:reflect, /sc:analyze, /sc:spec-panel, and the prd and
  task-builder skills are invoked via their commands/skills — never
  reimplemented inline
- output root: .dev/releases/current/task-builder-merge/
