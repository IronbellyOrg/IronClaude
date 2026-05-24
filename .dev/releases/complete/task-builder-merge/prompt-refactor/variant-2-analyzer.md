# Source Prompt — Task-Builder Convergence Orchestration (Analyzer Variant)

Goal: Pull the best qualities of `/sc:tasklist` into the `task-builder` skill, producing an
adversarially-validated release spec and a PRD. Where `/sc:tasklist` and `task-builder`
disagree, `task-builder` is authoritative **iff** the divergence is documented with a
FINAL-REPORT citation showing why the prior RF→SC direction does not apply in reverse.
If no such citation exists for a given mechanism, the disagreement is **unresolved** and
must be carried into Phase 4 as an open question rather than silently decided.

Anchor document:
  /config/workspace/IronClaude/.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md
  (read §1, §3, §4, §5, §6, §7 before any phase that cites them)

Output root: `.dev/releases/current/task-builder-merge/`

Verified-only flag rule: every command invocation in this prompt has been checked
against `src/superclaude/commands/<cmd>.md`. Do not add a flag that does not appear
there. If a needed behavior has no flag, achieve it through the existing flags or
do without.

==============================================================================
PHASE 1 — PARALLEL CONTEXT GATHERING  (one message, all Agent calls together)
==============================================================================

Read the anchor document and every sibling in
`.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/`
(file-inventory.md, dependency-map.md, pipeline-stages.md, architecture-comparison.md,
design-rfmerger-proposals.md, adversarial-validation.md).

Then spawn parallel Agent tool calls (subagent_type: Explore) — one per bucket. Each
agent reads all files in its bucket exhaustively and returns a structured digest:
purpose, public contract, hooks/dependencies, output schemas, and cross-references.

  Bucket A — `src/superclaude/skills/sc-tasklist-protocol/` (SKILL.md + rules/ + templates/)
  Bucket B — `src/superclaude/commands/tasklist.md` + `src/superclaude/cli/tasklist/`
  Bucket C — `src/superclaude/skills/task-builder/` (SKILL.md + every refs/, rules/,
             templates/, scripts/ file)
  Bucket D — `src/superclaude/agents/rf-*.md` — list the actual files first with
             a Glob; if a referenced agent (rf-task-builder, rf-task-researcher,
             rf-task-executor, rf-team-lead, rf-analyst, rf-qa, rf-qa-qualitative)
             does not exist, record "absent" rather than fabricating content
  Bucket E — `src/superclaude/skills/sc-adversarial-protocol/` (SKILL.md + refs/)
  Bucket F — `src/superclaude/examples/release-spec-template.md`. **Sample release
             specs**: Glob `.dev/releases/current/**/release-spec.md` and
             `.dev/releases/backlog/**/release-spec.md`. If zero results, report
             "no sample specs available — template is the only shape reference"
             and proceed; do not invent samples.

Each bucket digest must end with an explicit `evidence_status:` field —
`complete`, `partial (missing: …)`, or `absent` — so downstream phases can
gate on real coverage instead of assumed coverage.

==============================================================================
PHASE 2 — STRUCTURED ANALYSIS  (merged: matrices + brainstorm)
==============================================================================

Run:
  /sc:analyze src/superclaude/skills/task-builder src/superclaude/skills/sc-tasklist-protocol \
    --focus architecture --depth deep --format report

Use the report as the factual base, then run a single Sequential pass
(`mcp__sequential-thinking__sequentialthinking`) — length is bounded by content,
not a quota; stop when each row of the proposal table below has a
source-grounded justification, even if that takes 6 thoughts or 30.

Produce one combined deliverable
`.dev/releases/current/task-builder-merge/analysis.md` containing:

  1. **Capability matrix** with two columns: "sc:tasklist does X / task-builder
     does not" and "task-builder does Y / sc:tasklist does not". Every row cites
     `file:line` in the source and the FINAL-REPORT section it corresponds to
     (§3 architectures, §4 comparison, §6 adversarial outcomes).

  2. **Merge Proposal Portfolio.** Anchor the count to FINAL-REPORT §5/§7: the
     prior study converged on 5 distinct mechanisms (P1–P5 / R1–R5). Produce
     **one inverse-direction proposal per FINAL-REPORT mechanism** plus, optionally,
     additional proposals only when a new mechanism is identified that is *not*
     covered by P1–P5 *and* has a citation from Phase 1 digests. Do not invent
     proposals to hit a count.

     Each proposal is a separate file under
     `proposals/PR-NN-<slug>.md` with this required header (omit-not-allowed):

     ```
     ---
     source_mechanism: <where the behavior lives today — file:line>
     target_integration_point: <task-builder file:line>
     final_report_citation: <FINAL-REPORT §x.y, line or fact reference>
     conflict_with_task_builder: <yes|no — and the named invariant if yes>
     complexity_estimate: <lines-of-change band: ~10 / ~25 / ~50 / >50>
     expected_quality_gain: <low | medium | high — with the symptom it removes>
     direction_inversion_basis: <why this inversion is justified given that
                                 FINAL-REPORT §6.3 found 4/5 RF→SC ports were
                                 over-engineered; what is asymmetric about
                                 SC→task-builder for this mechanism?>
     ---
     ```

     A proposal missing `final_report_citation` or `direction_inversion_basis`
     is rejected by Phase 4 without debate.

==============================================================================
PHASE 3 — ADVERSARIAL VALIDATION
==============================================================================

Run, batching in passes of ≤10 if there are more proposals than the Mode A cap:
  /sc:adversarial --compare <proposal-1.md,proposal-2.md,...> \
    --depth standard --focus structure,completeness \
    --output .dev/releases/current/task-builder-merge/adversarial/

Flag-discipline notes:
- `--depth` and `--convergence` are tunable knobs documented in
  `src/superclaude/commands/adversarial.md`; use `standard` unless a proposal's
  cited risk is HIGH (per FINAL-REPORT §9 risk table conventions), in which
  case escalate that proposal's pass to `--depth deep`.
- `--convergence` is omitted: the protocol's default is the contract. Override
  only with a justification line stored in `adversarial/why-convergence.md`.
- `--interactive` is omitted: this orchestration is meant to be batch-replayable.

==============================================================================
PHASE 4 — CITATION & INVARIANT GATE  (replaces "reflection")
==============================================================================

Read `adversarial/merged-output.md` (or the protocol's documented merge artifact).
Produce `gate-report.md` with this exact checklist — each row resolves to PASS,
FAIL, or N/A with a one-line evidence reference:

  G1. Every accepted proposal cites `final_report_citation` (header field).
  G2. Every accepted proposal cites `direction_inversion_basis` (header field).
  G3. For every "task-builder wins on conflict" decision, the conflicting
      mechanism is named *and* the task-builder invariant it would have broken
      is named (one of: self-contained-item, evidence-bound-item, persistent
      .dev/tasks/ artifact, zero-trust QA, parallel research).
  G4. No accepted proposal weakens an invariant from G3 without an explicit
      override block citing FINAL-REPORT §6.3 (the over-engineering finding).
  G5. Determinism scope: any proposal that introduces non-determinism into
      task-builder output declares scope (frontmatter-only, ID-stable, etc.)
      using FINAL-REPORT §6.2 F4 ("hidden input") framing.

Optional: run `/sc:reflect --type task --validate` after producing `gate-report.md`
and append its output as `gate-report.reflect.md`. The decision artifact is the
gate report, not the reflect log; do not let `/sc:reflect` substitute for G1–G5.

Any FAIL halts the pipeline. Do not proceed to Phase 5 until G1–G5 are PASS.

==============================================================================
PHASE 5 — DRAFT RELEASE SPEC
==============================================================================

Produce `.dev/releases/current/task-builder-merge/release-spec.md` following
`src/superclaude/examples/release-spec-template.md`. Populate the frontmatter
fields **exactly as the template defines them** (`feature_id`, `spec_type`,
`complexity_score`, `complexity_class`, `target_release` — verified present in
the template). If the template adds or renames fields between now and execution,
match the template, not this prompt.

Body must include, with citations on every claim (`file:line` for code,
`FINAL-REPORT §x.y` for synthesis):
- Problem statement (cites FINAL-REPORT §1 and §6.3).
- Accepted proposals with implementation sequencing (mirroring §8 structure).
- Constraints section with the conditional precedence rule: "task-builder
  invariants from gate-report.md G3 take precedence in conflict; non-invariant
  conflicts go to /sc:spec-panel in Phase 6 for resolution."
- FRs per proposal, NFRs (determinism scope per G5, token ceiling, wall-clock),
  risks (using FINAL-REPORT §9 risk-table format), assumptions, test plan.

==============================================================================
PHASE 6 — SPEC PANEL REVIEW
==============================================================================

Run:
  /sc:spec-panel @.dev/releases/current/task-builder-merge/release-spec.md \
    --mode critique --focus requirements,architecture,correctness \
    --iterations 2 --format detailed --downstream roadmap

Apply expert revisions. For any expert recommendation that conflicts with a
G3 invariant: do **not** auto-defend with "task-builder wins" — instead, log
the conflict in `spec-panel-conflicts.md` with both sides cited, and resolve
by upgrading the G3 entry to an explicit specification clause or by accepting
the expert revision. Silent precedence is forbidden.

==============================================================================
PHASE 7 — PRD GENERATION  (hand-off to skill)
==============================================================================

Invoke:
  > Skill prd

Pass:
  WHAT  = "Task-Builder Convergence: importing /sc:tasklist's best qualities
           into the task-builder skill"
  WHY   = "engineering planning decision document for the v3.8 merger work"
  WHERE = paths confirmed-present by Phase 1 Bucket C/D digests (do not list
          paths from this prompt if Phase 1 reported them absent)
  OUTPUT = ".dev/releases/current/task-builder-merge/PRD_TASK_BUILDER_CONVERGENCE.md"
  INPUT_SPEC = ".dev/releases/current/task-builder-merge/release-spec.md"

The `prd` skill owns its phasing. Do not inline its protocol.

==============================================================================
GLOBAL CONSTRAINTS
==============================================================================
- **Citation gate.** Every claim cites a file path (`file:line` where applicable).
  FINAL-REPORT citations include section number. The Phase 4 gate enforces this
  as a binary halt condition, not a stylistic preference.
- **Verified flags only.** Flags appearing in this prompt have been checked
  against `src/superclaude/commands/<name>.md`. Do not add unverified flags.
- **task-builder precedence is conditional**, not absolute. It applies to the
  five named invariants in G3. All other disagreements are open questions to
  be adjudicated by Phase 3 adversarial debate and Phase 6 spec-panel review.
- **No false precision.** Sequential thought counts and proposal counts are
  outcome-bounded, not quota-bounded. `--depth` and `--convergence` use the
  command's documented defaults unless a cited risk justifies escalation.
- Phase 1 agents spawn in one message.
- `/sc:adversarial`, `/sc:analyze`, `/sc:spec-panel`, and the `prd` and
  `task-builder` skills are invoked via their commands/skills — never
  reimplemented inline.
- Output root: `.dev/releases/current/task-builder-merge/`.
