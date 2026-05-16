# Variant 1 — Architect Refactor: Task-Builder Convergence Orchestration

Goal: Pull the best qualities of /sc:tasklist into the task-builder skill, producing an
adversarially-validated release spec and a PRD. Where /sc:tasklist and task-builder
disagree, task-builder is authoritative. The FINAL-REPORT studied the inverse direction
(RF → SC); this orchestration inverts it (SC qualities → task-builder).

Anchor document:
  /config/workspace/IronClaude/.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md

Output root: .dev/releases/current/task-builder-merge/

Required subdirectories (create at start of Phase 1; freshness hook compliance —
touch + verify existence before any phase writes):
  - context-digests/      # Phase 1 per-bucket digests
  - analysis/             # Phase 2 matrices + analyze output
  - proposals/            # Phase 3 proposal files (one .md per proposal)
  - adversarial/          # Phase 4 sc:adversarial artifacts
  - reflection/           # Phase 5 reflect output
  - (root)                # release-spec.md, PRD, conflict-register.md

==============================================================================
PRECONDITION 0 — STRUCTURAL INVARIANTS  (read before any phase executes)
==============================================================================

I0. **Conflict Register is the precedence enforcement mechanism.** The slogan
    "task-builder is authoritative" is operationalized through a single file —
    `.dev/releases/current/task-builder-merge/conflict-register.md` — that every
    downstream phase reads and updates. Phases that resolve a conflict MUST append
    an entry; phases that consume merge proposals MUST consult the register before
    accepting changes that touch task-builder behaviors.

I1. **Phase outputs are file paths, not in-memory artifacts.** Every phase whose
    output feeds a later phase MUST write that output to disk under the output
    root before the phase is considered complete. Sequential MCP thoughts are
    not artifacts; they must be persisted as markdown files.

I2. **Freshness hook compliance.** Before any Edit/Write, create the parent
    directory (if missing) and touch + Read the target file. New files are created
    via a Write that the hook treats as creation; pre-existing files require a
    fresh Read in the same turn before re-writing.

I3. **No flag invention.** All commands use ONLY flags documented in the verified
    command files. Any deviation halts and reports.

==============================================================================
PHASE 1 — PARALLEL CONTEXT GATHERING
==============================================================================

Step 1.0 — Create output subdirectories listed above. Touch (Write empty)
  `conflict-register.md` with the heading `# Conflict Register — task-builder
  authoritative-precedence ledger` so later phases can append without a missing-file
  error.

Step 1.1 — Read the anchor document and its siblings in the same folder
  (`file-inventory.md`, `dependency-map.md`, `pipeline-stages.md`,
  `architecture-comparison.md`, `design-rfmerger-proposals.md`,
  `adversarial-validation.md`).

Step 1.2 — In ONE message, spawn six parallel Agent tool calls (subagent_type:
  Explore). Each agent reads its bucket exhaustively and writes a digest to a
  named file under `context-digests/`. Buckets are revised for exhaustiveness
  and non-overlap:

  Bucket A — `src/superclaude/skills/sc-tasklist-protocol/` (SKILL.md + refs/ +
             rules/ + templates/). Output: `context-digests/A-sc-tasklist-skill.md`.
  Bucket B — `src/superclaude/commands/tasklist.md` + `src/superclaude/cli/tasklist/`
             (command surface + CLI implementation, treated as a single coupled unit).
             Output: `context-digests/B-sc-tasklist-cli.md`.
  Bucket C — `src/superclaude/skills/task-builder/` (SKILL.md + every refs/, rules/,
             templates/, scripts/ file). Output: `context-digests/C-task-builder.md`.
  Bucket D — `src/superclaude/agents/rf-*.md` (rf-task-builder, rf-task-researcher,
             rf-task-executor, rf-team-lead, rf-analyst, rf-qa, rf-qa-qualitative).
             Output: `context-digests/D-rf-agents.md`.
  Bucket E — `src/superclaude/skills/sc-adversarial-protocol/` (SKILL.md + refs/) +
             `src/superclaude/commands/adversarial.md`. Output:
             `context-digests/E-adversarial.md`.
  Bucket F — `src/superclaude/examples/release-spec-template.md` AND
             `src/superclaude/examples/prd_template.md` (both schemas — release
             spec for Phase 6, PRD for Phase 8). Output:
             `context-digests/F-output-schemas.md`.

  Each digest MUST include: purpose, public contract, hooks/dependencies, output
  schemas, cross-references to other buckets, and any "this overlaps with bucket
  X" observations.

Step 1.3 — Verify all six digest files exist before proceeding. If any failed,
  re-spawn only the missing buckets.

==============================================================================
PHASE 2 — STRUCTURED ANALYSIS
==============================================================================

Step 2.1 — Run:
  /sc:analyze src/superclaude/skills/task-builder src/superclaude/skills/sc-tasklist-protocol \
    --focus architecture --depth deep --format report

Capture the analyze output to `analysis/sc-analyze-architecture.md`.

Step 2.2 — Read the six Phase-1 digests + FINAL-REPORT §3, §4, §6 + the
  Phase 2.1 analyze report. Produce two matrices and write them as discrete
  files:
    - `analysis/matrix-sc-only.md` — capabilities sc:tasklist has that task-builder lacks
    - `analysis/matrix-tb-only.md` — capabilities task-builder has that sc:tasklist lacks

  Every row cites a source file (file:line where applicable) and a
  FINAL-REPORT section.

Step 2.3 — From `matrix-sc-only.md`, mark each row with a candidate disposition:
  `IMPORT-AS-IS`, `IMPORT-ADAPTED`, `REJECT (conflicts with task-builder)`.
  This pre-stages Phase 3 proposal candidates and surfaces conflicts early.

==============================================================================
PHASE 3 — LONG-FORM BRAINSTORM  (Sequential MCP → persisted proposals)
==============================================================================

Step 3.1 — Use `mcp__sequential-thinking__sequentialthinking` (15-25 thoughts
  minimum) to brainstorm a Merge Proposal Portfolio. Cover at minimum:
    - Determinism: which /sc:tasklist guarantees (keyword scoring, appearance-
      order IDs, explicit tiebreakers) translate to task-builder's agent-research
      model; which are incompatible.
    - Traceability: how to inject R-### → T<PP>.<TT> → D-#### chains into MDTM
      items without violating the self-contained-item invariant.
    - Quality gates: which of the 17 pre-write checks port to task-builder's
      pre-write validation surface.
    - Validation stages: whether the 2N parallel-agent validation belongs in
      task-builder, or whether rf-qa + rf-qa-qualitative already cover it.
    - Tier classification: whether the 4-tier compliance classifier is additive
      to MDTM template selection (templates 01 generic / 02 complex).
    - Conflict rule: every case where task-builder's MDTM architecture (parallel
      research, evidence-bound items, persistent .dev/tasks/ artifacts, zero-trust
      QA) conflicts with a /sc:tasklist mechanism, task-builder wins.

Step 3.2 — Materialize 5–8 proposals to disk. For each proposal, Write a file at
  `proposals/proposal-NN-<slug>.md` where NN is a zero-padded appearance-order
  index. Each file contains:
    - **Source mechanism** (file:line citations from sc:tasklist surface)
    - **Target integration point** (file:line in task-builder surface)
    - **Conflict analysis** (with explicit "task-builder precedence verdict:
      ACCEPT-IMPORT / ACCEPT-ADAPTED / REJECT" and reasoning)
    - **Complexity estimate** and **expected quality gain**
    - FINAL-REPORT §5 / §7 citations for every claim

Step 3.3 — For every proposal flagged REJECT or ACCEPT-ADAPTED in Step 3.2,
  append a row to `conflict-register.md` with columns:
  `proposal-id | sc-mechanism | tb-behavior-that-wins | disposition | rationale`.

Step 3.4 — Enumerate proposals into a single env-like manifest at
  `proposals/INDEX.md` containing a comma-separated path list. This is the
  literal `--compare` argument for Phase 4 and removes any ambiguity about
  which files participate.

==============================================================================
PHASE 4 — ADVERSARIAL VALIDATION
==============================================================================

Step 4.1 — Read `proposals/INDEX.md` to obtain the comma-separated paths. If
  proposal count > 10, batch into passes of ≤10 each; each pass writes its own
  output subdirectory (e.g., `adversarial/pass-1/`, `adversarial/pass-2/`),
  and a final merge step uses the pass outputs as inputs to a second
  `--compare` invocation.

Step 4.2 — Run (Mode A; flag set restricted to verified flags from
  adversarial.md):
    /sc:adversarial --compare <paths-from-INDEX.md> \
      --depth deep --focus structure,completeness --convergence 0.80 \
      --interactive --output .dev/releases/current/task-builder-merge/adversarial/

  The adversarial protocol owns rounds, scoring, and merge logic. Do not inline.

Step 4.3 — Verify `adversarial/merge-log.md` and the merged output file exist.
  These are inputs for Phase 5 and Phase 6.

==============================================================================
PHASE 5 — REFLECTION  (precedence enforcement gate)
==============================================================================

Step 5.1 — Read `adversarial/merge-log.md`, `adversarial/refactor-plan.md` (if
  emitted), and `conflict-register.md`.

Step 5.2 — Run:
    /sc:reflect --type task --analyze --validate

  Scope the reflection prompt to: "Verify that every merged proposal in
  `adversarial/merge-log.md` respects the task-builder-precedence entries in
  `conflict-register.md`. For each merged proposal that weakens MDTM/zero-trust
  architecture (parallel research, evidence-bound items, persistent .dev/tasks/
  artifacts, rf-qa zero-trust gating), flag it as a Phase-6 revision target."

Step 5.3 — Persist reflection output to `reflection/reflect-task.md`. Append
  any newly-identified conflicts to `conflict-register.md`. If the reflection
  identifies revisions, write `reflection/phase-6-revisions.md` listing
  proposal-ids that must be down-scoped, adapted, or excluded from the release
  spec.

Rationale for `--type task` (not `completion`): the orchestration is mid-stream;
we are validating that the work in progress still adheres to the precedence
constraint, not closing out a task.

==============================================================================
PHASE 6 — DRAFT RELEASE SPEC
==============================================================================

Step 6.1 — Read inputs (all must exist before proceeding):
    - `adversarial/<merged-output>.md` (the consolidated portfolio)
    - `reflection/reflect-task.md` and `reflection/phase-6-revisions.md` (if present)
    - `conflict-register.md`
    - `context-digests/F-output-schemas.md` (for template shape)
    - `src/superclaude/examples/release-spec-template.md`
    - FINAL-REPORT §1, §6.3 (problem statement citations)

Step 6.2 — Produce `.dev/releases/current/task-builder-merge/release-spec.md`
  following the template. Populate frontmatter (`spec_type`,
  `complexity_score`, `complexity_class`, `target_release`, `feature_id`).

  Required sections:
    - **Problem Statement** — citing FINAL-REPORT §1 and §6.3.
    - **Accepted Proposals** — ordered by implementation sequencing. Each entry
      references its proposal-id and its conflict-register disposition.
    - **Excluded / Down-Scoped Proposals** — from `phase-6-revisions.md` and
      REJECT rows of `conflict-register.md`, each with a one-line rationale.
    - **Constraints** — explicit "task-builder is authoritative in any
      task-builder-vs-sc-tasklist conflict; rejected sc:tasklist mechanisms are
      catalogued in conflict-register.md".
    - **FRs** per accepted proposal.
    - **NFRs** — determinism scope (what becomes deterministic vs what remains
      research-driven), token ceiling, wall-clock.
    - **Risks, Assumptions, Test Plan.**

==============================================================================
PHASE 7 — SPEC PANEL REVIEW
==============================================================================

Step 7.1 — Verify the release spec exists at the expected path. The PRD skill
  is the next consumer (not roadmap), so the `--downstream` flag is OMITTED to
  avoid roadmap-oriented frontmatter that PRD does not consume. (Removed flag,
  not invented; rationale: spec-panel.md Step 6b only activates roadmap
  frontmatter when `--downstream roadmap` is passed, which is wrong for a PRD
  consumer.)

Step 7.2 — Run:
    /sc:spec-panel @.dev/releases/current/task-builder-merge/release-spec.md \
      --mode critique --focus requirements,architecture,correctness \
      --iterations 2 --format detailed

  Capture the panel output to `release-spec.review.md` next to the spec.

Step 7.3 — Apply expert revisions to `release-spec.md`. For each recommendation
  that contradicts a `conflict-register.md` precedence entry, EITHER:
    (a) reject the recommendation and add a "panel-disposition" note in
        `release-spec.md` citing the register row, OR
    (b) accept it, update the register entry, and document the new precedence.

  In no case may a panel revision silently weaken a task-builder-precedence
  entry.

==============================================================================
PHASE 8 — PRD GENERATION  (hand-off to skill)
==============================================================================

Step 8.1 — Verify `release-spec.md` and `conflict-register.md` exist.

Step 8.2 — Invoke:
    > Skill prd

  Pass:
    WHAT  = "Task-Builder Convergence: importing /sc:tasklist's best qualities
             into the task-builder skill"
    WHY   = "engineering planning decision document for the v3.8 merger work,
             with task-builder behaviors authoritative wherever they conflict
             with /sc:tasklist mechanisms"
    WHERE = "src/superclaude/skills/task-builder/,
             src/superclaude/skills/sc-tasklist-protocol/,
             src/superclaude/commands/tasklist.md,
             src/superclaude/cli/tasklist/,
             src/superclaude/agents/rf-*"
    OUTPUT = ".dev/releases/current/task-builder-merge/PRD_TASK_BUILDER_CONVERGENCE.md"
    INPUT_SPEC = ".dev/releases/current/task-builder-merge/release-spec.md"
    SUPPORTING_INPUTS =
      ".dev/releases/current/task-builder-merge/conflict-register.md,
       .dev/releases/current/task-builder-merge/adversarial/merge-log.md,
       .dev/releases/current/task-builder-merge/reflection/reflect-task.md"

  The prd skill owns its phasing. Do not inline its protocol.

==============================================================================
GLOBAL CONSTRAINTS
==============================================================================
- task-builder behaviors are authoritative whenever /sc:tasklist and task-builder
  disagree; precedence is enforced through `conflict-register.md`, which every
  phase from 3 onward reads and may append.
- Every claim cites a file path (file:line where applicable); FINAL-REPORT
  citations include section number.
- Phase 1 agents spawn in one message; each bucket's digest is a discrete file
  under `context-digests/`.
- Phase 3 produces proposals as discrete files under `proposals/` and registers
  conflicts in `conflict-register.md` before Phase 4 reads `proposals/INDEX.md`.
- /sc:adversarial, /sc:reflect, /sc:analyze, /sc:spec-panel, and the prd and
  task-builder skills are invoked via their commands/skills — never
  reimplemented inline.
- Flags are restricted to those documented in:
    src/superclaude/commands/{analyze,adversarial,reflect,spec-panel}.md
  No flag invention. `--downstream roadmap` is deliberately OMITTED from Phase 7
  because the downstream consumer is the prd skill, not /sc:roadmap.
- Output root: `.dev/releases/current/task-builder-merge/`.
- Freshness hook compliance: directories created before writes; touch + Read
  before re-Write.
