<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (quality-engineer, --persona-qa) -->
<!-- Incorporated: 5 changes from Variant 1 (architect), 5 changes from Variant 2 (analyzer), 1 hybrid -->
<!-- Merge date: 2026-05-14T06:55:00Z -->

# Refactored Prompt — Task-Builder Convergence Orchestration

<!-- Source: Base (original V3) -->
**Persona:** --persona-qa + --persona-architect (failure-mode discipline + structural integrity)
**Posture:** Assume every external call can fail, return non-terminal, or violate convergence. Bake retry budgets, decision gates, escape valves, and validation checkpoints into every phase. No silent pass-through. File-mediated handoffs; no slogan-only rules.

<!-- Source: Variant 1 + Variant 3 (merged via Change-#9, Change-#1) -->
**Verified-only flag rule:** All command flags below are taken from ground-truth files in `src/superclaude/commands/`. No invented flags. Where the source assumes a behavior that does not exist as a flag, the orchestrator handles it as logic, not a CLI option.

Goal: Pull the best qualities of /sc:tasklist into the task-builder skill, producing an adversarially-validated release spec and a PRD. Where /sc:tasklist and task-builder disagree, the precedence rule is the **extended four-case rule** below (not a one-sided "task-builder wins"). The FINAL-REPORT studied the inverse direction (RF → SC); this orchestration inverts it (SC qualities → task-builder), and every inversion requires a per-mechanism asymmetry citation (see Phase 3).

Anchor document:
  /config/workspace/IronClaude/.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md

Output root: `.dev/releases/current/task-builder-merge/`

==============================================================================
GLOBAL FAILURE-MODE CONTRACT  <!-- Source: Variant 3 (base) -->
==============================================================================

Apply to every phase. These supersede happy-path phrasing anywhere below.

**G1. Retry budgets.** Every external invocation (Agent tool, MCP call, skill, command) has a hard retry cap of 1 (total 2 attempts) unless a phase declares otherwise. After cap exhaustion, emit a halt-or-degrade artifact (see G2).

**G2. Halt-or-degrade artifact.** Any phase that cannot complete cleanly writes `state/<phase-id>-DEGRADED.md` with: what was attempted, what failed, what evidence is missing, recommended human action. The pipeline continues to the next phase ONLY if the phase's "degrade-acceptable" flag (declared in that phase) is true. Otherwise the pipeline halts and the orchestrator surfaces the artifact.

**G3. Decision gates.** Phases 4, 5, 6, 7 have explicit go/no-go gates declared at the bottom of the phase. The orchestrator MUST evaluate the gate before proceeding. Gate failures route to G2.

**G4. Evidence freshness.** Before any phase writes a file under `.dev/releases/current/task-builder-merge/`, touch the file first (creates if absent) and Read it (enforces the freshness hook).

**G5. No invented flags.** Phases below use ONLY the flags documented in the ground truth: `analyze` (`--focus`, `--depth`, `--format`), `adversarial` (`--compare`, `--source`, `--generate`, `--agents`, `--depth`, `--convergence`, `--interactive`, `--output`, `--focus`, `--blind`, `--auto-stop-plateau`, `--pipeline`, `--pipeline-parallel`, `--pipeline-resume`, `--pipeline-on-error`), `reflect` (`--type`, `--analyze`, `--validate`), `spec-panel` (`--mode`, `--experts`, `--focus`, `--iterations`, `--format`, `--downstream`). Any other behavior is orchestrator logic, not a CLI argument.

**G6. Extended four-case conflict rule.** <!-- Source: Variant 3, refined by Variant 1's register --> The source prompt's "task-builder wins" rule is one-sided. The merged rule is:
  - **CASE-A (task-builder authoritative):** task-builder has an explicit, evidence-cited stance; /sc:tasklist disagrees. Adopt task-builder. Document the rejected /sc:tasklist mechanism with reasoning.
  - **CASE-B (sc:tasklist additive):** task-builder is silent AND the mechanism does not violate task-builder's invariants (MDTM self-contained items, evidence-bound items, persistent `.dev/tasks/` artifacts, zero-trust QA, parallel research). Adopt /sc:tasklist. Document why no conflict exists.
  - **CASE-C (neither has a stance):** both silent. Defer to "deferred" appendix. Mark for human triage in Phase 7. Do not silently invent.
  - **CASE-D (partial coverage on both sides):** synthesize a stance ONLY if it does not violate task-builder invariants; otherwise treat as CASE-A and reject the /sc:tasklist portion, citing the violated invariant.
  Every case decision is appended as one row to `conflict-register.md` (see G7).

**G7. Conflict register + pipeline log.** <!-- Source: Variant 1 merged into Variant 3 base, Change #1 --> The slogan "task-builder is authoritative" is operationalized through `conflict-register.md` — an append-only ledger appended by Phases 3, 5, 7 and consulted by Phases 6, 7, 8. Schema:
  `proposal-id | case | sc-mechanism | tb-behavior-or-silence | disposition | invariant-protected | rationale`.
  Each phase also appends one line to `state/pipeline-log.md` recording phase id, start ts, end ts, outcome (PASS/DEGRADED/HALT), output paths.

==============================================================================
PHASE 1 — PARALLEL CONTEXT GATHERING
==============================================================================

**Step 1.0 — Pre-create subdirectory structure** <!-- Source: Variant 1, Change #5 -->
Touch (Write empty + Read for freshness compliance) the following paths so later phases can append without missing-file errors:
  - `context-digests/` (dir; per-bucket digest files)
  - `analysis/` (dir; matrices + analyze output)
  - `proposals/` (dir; per-proposal markdown files)
  - `adversarial/` (dir; /sc:adversarial output root)
  - `reflection/` (dir; /sc:reflect + gate-report output)
  - `state/` (dir; pipeline-log, DEGRADED, escalation, override files)
  - `conflict-register.md` (file; header `# Conflict Register — case-based precedence ledger`)
  - `state/pipeline-log.md` (file; header `# Pipeline Log`)

**Step 1.1 — Read anchor + siblings.** Read FINAL-REPORT.md and every sibling in `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/` (file-inventory.md, dependency-map.md, pipeline-stages.md, architecture-comparison.md, design-rfmerger-proposals.md, adversarial-validation.md).

**Step 1.2 — Spawn six parallel Agent calls.** In ONE message, dispatch Agent tool calls (subagent_type: Explore) — one per bucket. Each agent reads all files in its bucket exhaustively and writes a digest to a named file under `context-digests/`. Each digest ends with `evidence_status:` field (`complete`, `partial (missing: …)`, or `absent`) so downstream phases can gate on real coverage.

  - Bucket A — `src/superclaude/skills/sc-tasklist-protocol/` (SKILL.md + refs/ + rules/ + templates/). → `context-digests/A-sc-tasklist-skill.md`
  - Bucket B — `src/superclaude/commands/tasklist.md` + `src/superclaude/cli/tasklist/`. → `context-digests/B-sc-tasklist-cli.md`
  - Bucket C — `src/superclaude/skills/task-builder/` (SKILL.md + every refs/, rules/, templates/, scripts/ file). → `context-digests/C-task-builder.md`
  - Bucket D — `src/superclaude/agents/rf-*.md`. <!-- Source: Variant 2, Change #10 --> First Glob `src/superclaude/agents/rf-*.md`; if a referenced agent (rf-task-builder, rf-task-researcher, rf-task-executor, rf-team-lead, rf-analyst, rf-qa, rf-qa-qualitative) is missing from Glob results, record `absent` rather than fabricating. → `context-digests/D-rf-agents.md`
  - Bucket E — `src/superclaude/skills/sc-adversarial-protocol/` (SKILL.md + refs/) + `src/superclaude/commands/adversarial.md`. → `context-digests/E-adversarial.md`
  - Bucket F — `src/superclaude/examples/release-spec-template.md` AND `src/superclaude/examples/prd_template.md`. <!-- Source: Variant 2, Change #10 --> ALSO Glob `.dev/releases/current/**/release-spec.md` and `.dev/releases/backlog/**/release-spec.md`; if zero results, record `no sample specs available — template is the only shape reference` and proceed. → `context-digests/F-output-schemas.md`

**Failure-mode branches:**
- Empty bucket (e.g., Bucket F finds no sample specs): Buckets A–E are mandatory; if any returns EMPTY, halt. Bucket F is degrade-acceptable (substitute template-only path; log in pipeline-log.md).
- Agent failure / non-terminal return: retry once with the same prompt; if it fails again, mark that bucket DEGRADED. If A–E DEGRADED, halt. If F, continue.
- Cross-bucket consistency check: after all agents return, scan for contradictions in cross-references. Log in `state/phase-1-cross-bucket.md`. Discrepancies are advisory; Phase 2 must treat conflicting facts as ambiguities.

**Decision gate (G3):** Buckets A–E PASS AND no agent crashed beyond retry. Otherwise halt or degrade per above.

==============================================================================
PHASE 2 — STRUCTURED ANALYSIS
==============================================================================

Run:
  /sc:analyze src/superclaude/skills/task-builder src/superclaude/skills/sc-tasklist-protocol \
    --focus architecture --depth deep --format report

Capture the analyze output to `analysis/sc-analyze-architecture.md`.

Read the six Phase 1 digests + FINAL-REPORT §3, §4, §6 + the analyze report. Produce two matrices and write them as discrete files (NOT folded — auditability per V1 §W4):
  - `analysis/matrix-sc-only.md` — capabilities sc:tasklist has that task-builder lacks
  - `analysis/matrix-tb-only.md` — capabilities task-builder has that sc:tasklist lacks

Every row cites `file:line` in the source and the FINAL-REPORT section. Mark each matrix-sc-only row with a candidate disposition: `IMPORT-AS-IS`, `IMPORT-ADAPTED`, `REJECT (conflicts with task-builder)`. This pre-stages Phase 3 candidates and surfaces conflicts early.

**Failure-mode branches:**
- /sc:analyze errors or returns empty: retry once. If still empty, write `state/phase-2-DEGRADED.md` containing a hand-built matrix sourced from Phase 1 digests. Mark phase DEGRADED.
- If Phase 1 had a DEGRADED Bucket A or C, Phase 2 MUST tag every matrix row with the source bucket.

**Decision gate (G3):** both matrices populated, at least 3 rows cite verified file paths. Otherwise halt (`degrade-acceptable: false` — cannot meaningfully run Phase 3 without a matrix).

==============================================================================
PHASE 3 — BRAINSTORM + PROPOSAL MATERIALIZATION
==============================================================================

<!-- Source: Variant 3 base, with Variant 2 Change #6 + Change #9 + Variant 1 Change #2 -->

**Step 3.1 — Sequential brainstorm.** Use `mcp__sequential-thinking__sequentialthinking`. **Length is content-bounded, not quota-bounded** (V2 Change #6): stop when each row of the proposal table has a source-grounded justification — even if that takes 6 thoughts or 30. Cover at minimum:
  - Determinism: which /sc:tasklist guarantees (keyword scoring, appearance-order IDs, explicit tiebreakers) translate to task-builder's agent-research model; which are incompatible.
  - Traceability: how to inject R-### → T<PP>.<TT> → D-#### chains into MDTM items without violating self-contained-item invariant.
  - Quality gates: which of the 17 pre-write checks port to task-builder's pre-write validation surface.
  - Validation stages: whether the 2N parallel-agent validation belongs in task-builder, or whether rf-qa + rf-qa-qualitative already cover it.
  - Tier classification: whether the 4-tier compliance classifier is additive to MDTM template selection.

**Step 3.2 — Materialize proposals as files.** Anchor the proposal count to FINAL-REPORT §5/§7 (5 mechanisms P1-P5). Produce **one inverse-direction proposal per FINAL-REPORT mechanism**, plus optional additions only when a new mechanism is identified that is *not* covered by P1-P5 *and* has a Phase 1 digest citation. Do not invent proposals to hit a count. **Hard cap: 10 proposals** (V3 base — Phase 4 file-count discipline). If the brainstorm produces more, the orchestrator merges the lowest-priority pairs (by complexity/quality-gain ratio) before writing files.

Write each proposal as a separate file: `proposals/PR-NN-<slug>.md` (NN = zero-padded appearance order). **Required header (V2 Change #9 — missing fields halt the proposal in Phase 4 gate):**

```
---
proposal_id: PR-NN
case: A | B | C | D                                        # G6 four-case classification
source_mechanism: <file:line of behavior in sc:tasklist surface>
target_integration_point: <file:line in task-builder surface>
final_report_citation: <FINAL-REPORT §x.y or specific fact reference>
direction_inversion_basis: <why SC→task-builder asymmetry is justified
                            given FINAL-REPORT §6.3 found 4/5 RF→SC ports
                            over-engineered; what is asymmetric here?>
conflict_with_task_builder: <yes (case A/D + invariant) | no (case B/C)>
invariant_protected: <one of: self-contained-item | evidence-bound-item |
                     persistent .dev/tasks/ artifact | zero-trust QA |
                     parallel research | n/a-for-case-B-or-C>
complexity_estimate: <~10 / ~25 / ~50 / >50 lines-of-change>
expected_quality_gain: <low | medium | high — with the symptom it removes>
---
```

**Step 3.3 — Append to conflict-register.md** (V1 Change #1 + G7). For every CASE-A and CASE-D proposal, append one row:
  `proposal-id | case | sc-mechanism | tb-behavior | disposition | invariant-protected | rationale`.

**Step 3.4 — Emit `proposals/INDEX.md` manifest** (V1 Change #2). Single file containing a comma-separated path list. This is the literal `--compare` argument for Phase 4; removes invocation ambiguity.

**Failure-mode branches:**
- Sequential MCP unavailable: retry once. If still failing, fall back to manual brainstorm using Phase 1+2 outputs; mark phase DEGRADED; require at least 5 proposals to proceed.
- Proposal count exceeds 10 after merge attempt: halt and ask the user to pick the cut.
- Proposal count falls below 3: halt; insufficient material.

**Decision gate (G3):** 3 ≤ proposals ≤ 10 AND every proposal has CASE classification AND every CASE-A/D proposal cites the protected invariant AND every proposal header has both `final_report_citation` and `direction_inversion_basis` populated.

==============================================================================
PHASE 4 — ADVERSARIAL VALIDATION
==============================================================================

Run (Mode A; 2-10 files enforced by Phase 3 cap; comma-list `--focus` per adversarial.md:97):
```
/sc:adversarial --compare <paths-from-INDEX.md> \
  --depth standard --focus structure,completeness --convergence 0.80 \
  --output .dev/releases/current/task-builder-merge/adversarial/
```

<!-- Source: Variant 2 Change #7 (depth standard) + Change #8 (drop --interactive) -->
Flag-discipline notes:
- `--depth standard` is the default (V2 Change #7); escalate that proposal's pass to `--depth deep` only when its `expected_quality_gain` is `high` AND its complexity_estimate is `>50` (HIGH risk per FINAL-REPORT §9 conventions).
- `--convergence 0.80` is explicit (V3 base — enables sub-threshold branch below).
- `--interactive` is OMITTED (V2 Change #8); batch-replayable contract — Phases 5-8 do not expect human-in-loop here.
- `--focus structure,completeness` uses comma-list per adversarial.md examples (V3 sequential-pass deviation rolled back).

The adversarial protocol owns rounds, scoring, and merge logic. Do not inline.

**Failure-mode branches:**
- **Convergence below 0.80** (V3 base — closes the source's H-1 silent-pass risk):
  1. Inspect the adversarial output for the lowest-scoring proposal. If a single proposal is dragging convergence down, re-run `/sc:adversarial --compare` excluding it; record exclusion in `state/phase-4-exclusions.md`.
  2. If multiple proposals are below threshold, lower depth to `quick` for a targeted re-run on unresolved issues (one retry budget).
  3. If still below 0.80 after retry, mark Phase 4 DEGRADED in `state/phase-4-DEGRADED.md` with explicit "convergence floor not met" wording. Do NOT silently proceed.
- Mode A file-count violation (>10 files survived Phase 3 cap): halt; fix belongs in Phase 3.
- Protocol crashes / times out: retry once; if still failing, mark DEGRADED and continue to Phase 5 ONLY if at least one proposal has a recorded debate verdict.
- Output directory not written: halt — Phase 5 has nothing to consume.

**Decision gate (G3):** convergence ≥ 0.80 across surviving proposals AND `adversarial/` contains a per-proposal verdict file (or DEGRADED artifact with manual signoff). Otherwise halt or degrade per above.

==============================================================================
PHASE 5 — REFLECTION + CITATION GATE  (hybrid per Change #11)
==============================================================================

<!-- Source: Variant 3 reflect retention + Variant 2 G1-G5 gate -->
Run sequentially: /sc:reflect first (preserves user's explicit "engage sc:reflect" requirement), then produce a binary citation gate (V2's halt rigor).

**Step 5.1 — /sc:reflect.** Read `adversarial/merge-log.md` (or the protocol's documented merge artifact), `adversarial/refactor-plan.md` if emitted, and `conflict-register.md`. Run:
```
/sc:reflect --type task --analyze --validate
```
Scope the reflection prompt: "Verify every merged proposal in `adversarial/merge-log.md` respects (a) the four-case conflict rule in G6 and (b) the `conflict-register.md` entries. For each merged proposal that weakens MDTM/zero-trust architecture or silently shifts a CASE-A/D proposal into adoption of a rejected mechanism, flag it as a Phase 6 revision target."
Persist output to `reflection/reflect-task.md`. If reflect identifies revisions, write `reflection/phase-6-revisions.md` listing proposal-ids to down-scope, adapt, or exclude.

**Step 5.2 — Citation & Invariant Gate.** Produce `reflection/gate-report.md` with this exact checklist — each row resolves to PASS, FAIL, or N/A with a one-line evidence reference:
  - **G1.** Every accepted proposal cites `final_report_citation` (header field).
  - **G2.** Every accepted proposal cites `direction_inversion_basis` (header field).
  - **G3.** For every "task-builder wins on conflict" decision (CASE-A/D), the conflicting mechanism is named *and* the invariant it would have broken is named (one of: self-contained-item, evidence-bound-item, persistent .dev/tasks/ artifact, zero-trust QA, parallel research).
  - **G4.** No accepted proposal weakens an invariant from G3 without an explicit override block citing FINAL-REPORT §6.3.
  - **G5.** Determinism scope: any proposal that introduces non-determinism into task-builder output declares scope (frontmatter-only, ID-stable, etc.) using FINAL-REPORT §6.2 F4 ("hidden input") framing.

**The gate is the binding decision artifact; the reflect log is the advisory layer.** Any FAIL halts the pipeline. Do not proceed to Phase 6 until G1–G5 are PASS.

**Failure-mode branches:**
- /sc:reflect returns non-terminal (`still pending` or unrecognized): retry once with `--type completion` (verified value). If still non-terminal, mark DEGRADED in `state/phase-5-DEGRADED.md`; Phase 6 MAY proceed only with manual signoff in `state/phase-5-manual-signoff.md`.
- Conflict-rule violation detected: halt. Write `state/phase-5-conflict-violation.md` enumerating violations with the protected invariant. Re-work from Phase 3.
- /sc:reflect skill unavailable: retry once; if still unavailable, mark DEGRADED; require manual signoff.

**Decision gate (G3):** /sc:reflect returned terminal (or manual signoff exists) AND `reflection/gate-report.md` shows G1–G5 all PASS AND no conflict-rule violations open. Otherwise halt.

==============================================================================
PHASE 6 — DRAFT RELEASE SPEC
==============================================================================

Read inputs (all must exist before proceeding):
  - `adversarial/<merged-output>.md` (consolidated portfolio)
  - `reflection/reflect-task.md` and `reflection/phase-6-revisions.md` (if present)
  - `reflection/gate-report.md`
  - `conflict-register.md`
  - `context-digests/F-output-schemas.md` (template shape)
  - `src/superclaude/examples/release-spec-template.md`
  - FINAL-REPORT §1, §6.3 (problem statement citations)

Produce `.dev/releases/current/task-builder-merge/release-spec.md` following the template. Populate frontmatter **exactly as the template defines them** — if the template adds or renames fields between now and execution, match the template (V2 §A-006). Verified template fields at orchestration design time: `feature_id`, `spec_type`, `complexity_score`, `complexity_class`, `target_release`.

Required sections:
  - **Problem Statement** — citing FINAL-REPORT §1 and §6.3.
  - **Accepted Proposals** — ordered by implementation sequencing. Each entry references its `proposal_id`, its CASE (A/B/C/D) classification, and its `conflict-register.md` row.
  - **Excluded / Down-Scoped Proposals** — from `phase-6-revisions.md` and REJECT rows of `conflict-register.md`, each with a one-line rationale.
  - **Constraints** — explicit four-case conflict rule from G6 (not just "task-builder takes precedence"); rejected /sc:tasklist mechanisms catalogued in `conflict-register.md`.
  - **FRs** per accepted proposal.
  - **NFRs** — determinism scope per G5 (what becomes deterministic vs what remains research-driven), token ceiling, wall-clock.
  - **Risks, Assumptions** — using FINAL-REPORT §9 risk-table format.
  - **Test Plan**.
  - **Acceptance Criteria** (V3 base — observable). Per accepted proposal:
      - *Observable behavior:* what changes in task-builder's outputs (e.g., "the generated task file contains an R-### → T<PP>.<TT> table in the index section").
      - *Verification method:* file path, grep pattern, or skill output to inspect.
      - *Negative criterion:* at least one thing that MUST NOT change (e.g., "MDTM self-contained-item invariant preserved").

If a proposal cannot articulate observable criteria, downgrade it to the deferred appendix and exclude from this release.

**Failure-mode branches:**
- Template missing: halt — cannot draft without a schema.
- A surviving proposal lacks observable criteria: downgrade to deferred; do NOT silently include.
- Freshness-hook failure on first write: retry the touch step once; if still failing, halt and surface the hook error.

**Decision gate (G3):** spec exists, frontmatter populated exactly per template, every accepted proposal has an Acceptance Criteria entry with all three fields. Otherwise halt.

==============================================================================
PHASE 7 — SPEC PANEL REVIEW
==============================================================================

<!-- Source: Variant 3 base + Variant 1 Change #3 (-downstream removal) -->
Verify `release-spec.md` exists at the expected path.

Run:
```
/sc:spec-panel @.dev/releases/current/task-builder-merge/release-spec.md \
  --mode critique --focus requirements,architecture,correctness \
  --iterations 2 --format detailed
```

**`--downstream roadmap` is deliberately OMITTED** (V1 Change #3). Rationale: spec-panel.md Step 6b activates roadmap-oriented frontmatter intended for /sc:roadmap consumption. The actual downstream consumer in Phase 8 is the **prd** skill, which does not consume roadmap frontmatter. Flag removal is documented, not invented.

Capture panel output to `release-spec.review.md` next to the spec.

Apply expert revisions to the release spec. **For any expert recommendation that contradicts the conflict rule (G6) or a `conflict-register.md` entry, the orchestrator runs this five-step deterministic process** (V3 base):

  - **Step 1. Classify.** Apply G6 four-case rule. Which of CASE-A/B/C/D does the recommendation map to?
  - **Step 2. Identify the protected invariant.** Which task-builder invariant does the recommendation challenge?
  - **Step 3. Search FINAL-REPORT for evidence.** Cite section + line range that documents either (a) why the invariant matters or (b) prior evidence that the recommendation's approach was rejected. If no citation can be found → Step 5.
  - **Step 4. Decide:**
      - FINAL-REPORT supports the invariant → REJECT; write `state/phase-7-rejection-NN.md` with the expert quote, cited evidence, and rationale. Spec NOT modified.
      - FINAL-REPORT supports the expert → ACCEPT; treat as discovered gap; update Phase 3's case classifications retroactively in the spec; note in `state/phase-7-overrides.md`.
      - FINAL-REPORT silent → Step 5.
  - **Step 5. Escalate.** Write `state/phase-7-escalation-NN.md`. Surface to user before accepting. **Default to REJECT until user resolves.** Conflicting revisions are NEVER silently accepted.

**Rejection-rate threshold:** if >50% of expert recommendations are rejected via Step 4, emit `state/phase-7-rejection-rate.md` and ask the user whether to (a) keep spec as-is and proceed to Phase 8, (b) re-run `/sc:spec-panel --mode discussion` for softer pass, or (c) halt and revisit Phase 3.

**Failure-mode branches:**
- /sc:spec-panel crashes / times out: retry once. If still failing, mark DEGRADED; manual review before Phase 8.
- Iterations exhausted with poor convergence: accept current state, log it; do not auto-extend iterations.

**Decision gate (G3):** spec revised through 2 iterations OR the rejection process executed for every conflicting revision AND no escalations remain open without user resolution. Otherwise halt.

==============================================================================
PHASE 8 — PRD GENERATION  (hand-off to skill)
==============================================================================

<!-- Source: Variant 3 base (INPUT_SPEC routing fix) + Variant 1 Change #4 (SUPPORTING_INPUTS) -->
Verify `release-spec.md` and `conflict-register.md` exist.

Invoke:
```
> Skill prd
```

**INPUT_SPEC handling (V3 base — closes silent-ignore failure):** The prd skill's documented Input fields are WHAT / WHY / WHERE / OUTPUT only (SKILL.md:33-43). The skill does NOT recognize `INPUT_SPEC` as a first-class input. The orchestrator MUST surface the release spec inside the WHAT and WHERE fields the skill actually parses:

Pass:
```
WHAT  = "Task-Builder Convergence: importing /sc:tasklist's best qualities
         into the task-builder skill, grounded in the accepted release spec
         at .dev/releases/current/task-builder-merge/release-spec.md (read
         this file first; its Acceptance Criteria section drives every
         requirement in the PRD)."
WHY   = "engineering planning decision document for the v3.8 merger work,
         with the four-case conflict rule (G6) authoritative wherever
         /sc:tasklist and task-builder behaviors disagree"
WHERE = "src/superclaude/skills/task-builder/,
         src/superclaude/skills/sc-tasklist-protocol/,
         src/superclaude/commands/tasklist.md,
         src/superclaude/cli/tasklist/,
         src/superclaude/agents/rf-*,
         .dev/releases/current/task-builder-merge/release-spec.md
         (PRIMARY INPUT SPEC — treat as authoritative scope)"
OUTPUT = ".dev/releases/current/task-builder-merge/PRD_TASK_BUILDER_CONVERGENCE.md"

# V1 Change #4 — supporting inputs for traceability (advisory-only;
# the binding spec reference is the path in WHERE)
INPUT_SPEC = ".dev/releases/current/task-builder-merge/release-spec.md"
SUPPORTING_INPUTS = ".dev/releases/current/task-builder-merge/conflict-register.md,
                     .dev/releases/current/task-builder-merge/adversarial/merge-log.md,
                     .dev/releases/current/task-builder-merge/reflection/reflect-task.md,
                     .dev/releases/current/task-builder-merge/reflection/gate-report.md"
```

The prd skill owns its phasing. Do not inline its protocol.

**Acceptance Criteria propagation (V3 base — mirror-check):** After the prd skill returns, open the PRD and verify:
  - Every accepted proposal's observable behavior appears in the PRD's acceptance section.
  - Every negative criterion appears as a non-functional constraint.
If either is missing, re-invoke the prd skill once with a targeted "fill missing acceptance criteria from release-spec.md" instruction.

**Failure-mode branches:**
- Output file not written at OUTPUT path: re-invoke once.
- Output file written but Acceptance Criteria missing: re-invoke once with targeted instruction.
- prd skill creates an MDTM task file but artifacts land outside `.dev/tasks/to-do/`: halt and inspect (the CLAUDE.md skill-creator override applies to skill-creator only, but verify with `ls .dev/tasks/to-do/TASK-PRD-*` after the skill returns).

**Decision gate (G3):** PRD exists at OUTPUT path AND its acceptance section mirrors release-spec.md AND no halt-or-degrade artifacts remain unaddressed. Otherwise halt.

==============================================================================
GLOBAL CONSTRAINTS
==============================================================================
- The four-case conflict rule (G6) is authoritative wherever /sc:tasklist and task-builder behaviors disagree. CASE-A/D decisions are operationalized through `conflict-register.md`; CASE-B mechanisms adopted; CASE-C mechanisms deferred.
- Every claim cites a file path (`file:line` where applicable); FINAL-REPORT citations include section number.
- Every proposal header carries `final_report_citation` and `direction_inversion_basis`; missing fields halt the proposal in the Phase 5 gate.
- Phase 1 agents spawn in one message; each bucket digest is a discrete file under `context-digests/` with explicit `evidence_status:` field.
- /sc:adversarial, /sc:reflect, /sc:analyze, /sc:spec-panel, and the prd and task-builder skills are invoked via their commands/skills — never reimplemented inline.
- Flags restricted to those documented in `src/superclaude/commands/{analyze,adversarial,reflect,spec-panel}.md` (G5). No flag invention.
- Hook compatibility: every new file under `.dev/releases/current/task-builder-merge/` is created via touch + Read before Write (G4).
- Output root: `.dev/releases/current/task-builder-merge/`.
- State artifacts: `.dev/releases/current/task-builder-merge/state/` (pipeline-log.md plus DEGRADED, escalation, override, exclusion, conflict-violation files).
