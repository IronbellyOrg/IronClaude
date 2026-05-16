# Variant 3 — QA Refactor (Failure-Mode Hardened)

**Persona:** --persona-qa
**Posture:** Assume every external call can fail, return non-terminal, or violate convergence. Bake retry budgets, decision gates, escape valves, and validation checkpoints into every phase. No silent pass-through.

**Verified-only invariants:** All command flags below are taken from the ground-truth files in `src/superclaude/commands/`. No invented flags. Where the source prompt assumes a behavior that does not exist as a flag, the variant treats it as orchestrator logic, not a CLI option.

Goal: Pull the best qualities of /sc:tasklist into the task-builder skill, producing an adversarially-validated release spec and a PRD. Where /sc:tasklist and task-builder disagree, task-builder is authoritative. The FINAL-REPORT studied the inverse direction (RF -> SC); this task inverts it (SC qualities -> task-builder).

Anchor document:
  /config/workspace/IronClaude/.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md

Output root: .dev/releases/current/task-builder-merge/

==============================================================================
GLOBAL FAILURE-MODE CONTRACT
==============================================================================

Apply to every phase. These supersede happy-path phrasing anywhere below.

G1. **Retry budgets.** Every external invocation (Agent tool, MCP call, skill, command) has a hard retry cap of 1 (total 2 attempts) unless a phase declares otherwise. After cap exhaustion, emit a halt-or-degrade artifact (see G2).

G2. **Halt-or-degrade artifact.** Any phase that cannot complete cleanly writes `.dev/releases/current/task-builder-merge/state/<phase-id>-DEGRADED.md` with: what was attempted, what failed, what evidence is missing, recommended human action. The pipeline continues to the next phase ONLY if the phase's "degrade-acceptable" flag (declared in that phase) is true. Otherwise the pipeline halts and the orchestrator surfaces the artifact to the user.

G3. **Decision gates.** Phases 4, 5, 6, 7 have explicit go/no-go gates declared at the bottom of the phase. The orchestrator MUST evaluate the gate before proceeding. Gate failures route to G2.

G4. **Evidence freshness.** Before any phase writes a file under `.dev/releases/current/task-builder-merge/`, touch the file first (creates if absent) and Read it (enforces the freshness hook). This is the same touch+Read invariant used by other release workflows in this repo.

G5. **No invented flags.** Phases below use ONLY the flags documented in the ground truth: analyze (--focus, --depth, --format), adversarial (--compare, --source, --generate, --agents, --depth, --convergence, --interactive, --output, --focus, --blind, --auto-stop-plateau, --pipeline, --pipeline-parallel, --pipeline-resume, --pipeline-on-error), reflect (--type, --analyze, --validate), spec-panel (--mode, --experts, --focus, --iterations, --format, --downstream). Any other "flag" is orchestrator behavior, not a CLI argument.

G6. **Conflict-rule completion.** The source prompt's conflict rule is one-sided ("task-builder wins"). It does not cover: (a) neither side has a stance, (b) task-builder is silent on a /sc:tasklist mechanism but the mechanism is value-additive, (c) both sides have partial coverage. Phase 3 below extends the rule with explicit decision branches for each case.

G7. **Tracking artifact.** Each phase appends a one-line entry to `.dev/releases/current/task-builder-merge/state/pipeline-log.md` recording phase id, start ts, end ts, outcome (PASS/DEGRADED/HALT), output paths. Use touch+Read on first write.

==============================================================================
PHASE 1 — PARALLEL CONTEXT GATHERING  (one message, all Agent calls together)
==============================================================================

Read the anchor document and its siblings in the same folder (file-inventory.md, dependency-map.md, pipeline-stages.md, architecture-comparison.md, design-rfmerger-proposals.md, adversarial-validation.md).

Then spawn parallel Agent tool calls (subagent_type: Explore) -- one per bucket. Each agent reads all files in its bucket exhaustively and returns a structured digest: purpose, public contract, hooks/dependencies, output schemas, and any cross-references to other buckets.

  Bucket A — src/superclaude/skills/sc-tasklist-protocol/ (SKILL.md + rules/ + templates/)
  Bucket B — src/superclaude/commands/tasklist.md + src/superclaude/cli/tasklist/
  Bucket C — src/superclaude/skills/task-builder/ (SKILL.md + every refs/, rules/, templates/, scripts/ file)
  Bucket D — src/superclaude/agents/rf-*.md (rf-task-builder, rf-task-researcher, rf-task-executor, rf-team-lead, rf-analyst, rf-qa, rf-qa-qualitative)
  Bucket E — src/superclaude/skills/sc-adversarial-protocol/ (SKILL.md + refs/)
  Bucket F — src/superclaude/examples/release-spec-template.md + sample release specs under .dev/releases/current/ for shape reference

**Failure-mode branches:**

- **Empty bucket** (e.g., Bucket F finds no sample release specs under `.dev/releases/current/` because the directory is fresh): the agent returns `STATUS: EMPTY` with a list of paths it searched. Phase 1 records this in `state/phase-1-emptiness.md`. Buckets A-E are mandatory; if any returns EMPTY, halt (these are the actual source-of-truth directories). Bucket F is degrade-acceptable: substitute the template-only path `src/superclaude/examples/release-spec-template.md` and note in pipeline-log.md that no live sample shape was available.

- **Agent failure / non-terminal return** (agent crashes, hits a tool error, returns malformed digest): retry once with the same prompt; if it fails again, mark that bucket DEGRADED in pipeline-log.md. If bucket is A-E, halt. If bucket is F, continue with degraded coverage.

- **Cross-bucket consistency check** (added gate): after all agents return, the orchestrator skims for contradictions in cross-references (e.g., Bucket A claims a file exists that Bucket C says is missing). Log discrepancies in `state/phase-1-cross-bucket.md`. Discrepancies are advisory, not blocking, but Phase 2 must treat conflicting facts as ambiguities.

**Decision gate G1:** Buckets A-E PASS AND no agent crashed beyond retry. Otherwise halt or degrade per above.

==============================================================================
PHASE 2 — STRUCTURED ANALYSIS
==============================================================================

Run:
  /sc:analyze src/superclaude/skills/task-builder src/superclaude/skills/sc-tasklist-protocol \
    --focus architecture --depth deep

(Verified flags only. Format defaults to `text`; the orchestrator does not need `--format report` here because Phase 3 consumes the prose directly.)

Produce two matrices:
  - "sc:tasklist does X, task-builder does not"
  - "task-builder does Y, sc:tasklist does not"
Cross-reference against FINAL-REPORT.md sections 3, 4, 6.

**Failure-mode branches:**

- If `/sc:analyze` returns an error or empty analysis: retry once. If still empty, write `state/phase-2-DEGRADED.md` containing a hand-built matrix sourced from Phase 1 bucket digests. Mark this phase DEGRADED; the conflict map in Phase 3 must explicitly flag any merger candidate that relied on degraded inputs.

- If Phase 1 had a DEGRADED Bucket A or C, Phase 2 MUST tag every matrix row with the source bucket so Phase 3 can avoid building proposals on weak ground.

**Decision gate G2:** Both matrices populated with at least one row each AND at least 3 rows cite verified file paths. Otherwise route to G2 with `degrade-acceptable: false` (cannot meaningfully run Phase 3 without a matrix).

==============================================================================
PHASE 3 — LONG-FORM BRAINSTORM  (Sequential MCP, 15-25 thoughts minimum)
==============================================================================

Use mcp__sequential-thinking__sequentialthinking to draft a Merge Proposal Portfolio. Cover at minimum:
  - Determinism: which /sc:tasklist guarantees (keyword scoring, appearance-order IDs, explicit tiebreakers) translate to task-builder's agent-research model; which are incompatible
  - Traceability: how to inject R-### -> T<PP>.<TT> -> D-#### chains into MDTM items without violating the self-contained-item invariant
  - Quality gates: which of the 17 pre-write checks port to task-builder's pre-write validation surface
  - Validation stages: whether the 2N parallel-agent validation belongs in task-builder, or whether rf-qa + rf-qa-qualitative already cover it
  - Tier classification: whether the 4-tier compliance classifier is additive to MDTM template selection (templates 01 generic / 02 complex)

**Extended conflict rule (replaces source's one-sided rule):**

For every candidate mechanism, classify into one of:
  - **CASE-A (task-builder authoritative):** task-builder has an explicit, evidence-cited stance; /sc:tasklist disagrees. Adopt task-builder. Document the rejected /sc:tasklist mechanism with reasoning.
  - **CASE-B (sc:tasklist additive):** task-builder is silent on this mechanism AND the mechanism does not violate task-builder's invariants (MDTM self-contained items, evidence-bound items, persistent .dev/tasks/ artifacts, zero-trust QA). Adopt /sc:tasklist mechanism. Document why no conflict exists.
  - **CASE-C (neither has a stance):** both are silent. Defer the mechanism to a "deferred" appendix. Do NOT silently invent a stance. Mark for human triage in Phase 7.
  - **CASE-D (partial coverage on both sides):** both have partial stances. Document the partial overlap, propose a synthesized stance ONLY if it does not violate task-builder invariants. If a synthesis would violate task-builder, treat as CASE-A and reject the /sc:tasklist portion. Cite which invariant would be violated.

Every proposal MUST declare its case (A/B/C/D) in the file header.

Produce 5-8 proposals. Each: source mechanism, target integration point, conflict analysis (with case classification), complexity estimate, expected quality gain. Cite source files and FINAL-REPORT sections 5/7 for every claim. Write each proposal as its own markdown file under `.dev/releases/current/task-builder-merge/proposals/` using `NN-<slug>.md` naming.

**Hard cap:** maximum 10 proposals. If the brainstorm produces more, the orchestrator merges the lowest-priority pairs (by complexity-estimate / quality-gain ratio) before writing files. This ensures Phase 4's 2-10 file limit is always respected without batched-merge complexity.

**Failure-mode branches:**

- Sequential MCP unavailable / errors: retry once. If still failing, fall back to manual brainstorm using Phase 1+2 outputs; mark phase DEGRADED; require at least 5 proposals to proceed.
- Proposal count exceeds 10 after merge attempt: halt and ask the user to pick the cut. Do NOT silently drop.
- Proposal count falls below 3: halt; insufficient material for adversarial debate.

**Decision gate G3:** 3 <= proposals <= 10 AND every proposal has a CASE classification AND every CASE-A/D proposal cites the task-builder invariant it protects.

==============================================================================
PHASE 4 — ADVERSARIAL VALIDATION
==============================================================================

Run (Mode A; 2-10 files enforced by Phase 3 cap):
  /sc:adversarial --compare <proposal-1.md,proposal-2.md,...> \
    --depth deep --focus completeness --convergence 0.80 \
    --interactive --output .dev/releases/current/task-builder-merge/adversarial/

(Verified flags only. `--focus` takes a single value per the command file; if multiple focus areas matter, run sequentially: completeness pass first, then correctness pass on the same proposals.)

The adversarial protocol owns rounds, scoring, and merge logic. Do not inline.

**Failure-mode branches:**

- **Convergence below 0.80** (the source prompt is silent here): treat as a HARD GATE failure. Options, in order:
  1. Inspect the adversarial output for the lowest-scoring proposal. If a single proposal is dragging down convergence, re-run `/sc:adversarial --compare` excluding it; record the exclusion in `state/phase-4-exclusions.md`.
  2. If multiple proposals are below threshold, lower the depth to `quick` for a faster re-run targeted only at unresolved issues; this is one allowed retry budget.
  3. If still below 0.80 after the retry, mark Phase 4 DEGRADED and surface to the user with explicit "convergence floor not met" wording in `state/phase-4-DEGRADED.md`. Do NOT silently proceed.

- **Mode A file-count violation** (>10 files survived Phase 3's cap, somehow): halt. The fix belongs in Phase 3.

- **Adversarial protocol crashes / times out:** retry once. If still failing, mark Phase 4 DEGRADED and continue to Phase 5 ONLY if at least one proposal has a recorded debate verdict. Otherwise halt.

- **Output directory not written:** halt. The protocol's own output is the input to Phase 5; missing output is non-recoverable.

**Decision gate G4:** convergence >= 0.80 across surviving proposals AND `.dev/releases/current/task-builder-merge/adversarial/` contains a per-proposal verdict file. Otherwise halt or degrade per above.

==============================================================================
PHASE 5 — REFLECTION
==============================================================================

Run:
  /sc:reflect --type task --analyze --validate

Verify adversarial outcomes respect the conflict rule (extended four-case version from Phase 3). Flag for revision any proposal whose merged form weakens task-builder's MDTM/zero-trust architecture or silently shifts a CASE-A/D proposal into adoption of a rejected mechanism.

**Failure-mode branches:**

- **Non-terminal return** (`--type task` returns "still pending" or any status other than a clean PASS/FAIL/issues-list): retry once with `--type completion` as the second attempt (verified flag value). If still non-terminal, mark Phase 5 DEGRADED and write `state/phase-5-DEGRADED.md` listing the unresolved validation questions. Phase 6 MAY proceed only if the orchestrator manually reviews the adversarial output and signs off in `state/phase-5-manual-signoff.md`.

- **Conflict-rule violation detected** (a CASE-A proposal's merged form adopts the rejected mechanism, or a CASE-D synthesis violates a task-builder invariant): halt. Write `state/phase-5-conflict-violation.md` enumerating each violation with the protected invariant. Do NOT roll forward; the spec must be re-worked starting at Phase 3.

- **Reflect skill unavailable:** retry once. If unavailable on retry, mark DEGRADED; require manual orchestrator review documented in `state/phase-5-manual-signoff.md` before Phase 6.

**Decision gate G5:** reflect returned a terminal status (or manual signoff exists) AND no conflict-rule violations are open. Otherwise halt.

==============================================================================
PHASE 6 — DRAFT RELEASE SPEC
==============================================================================

Produce `.dev/releases/current/task-builder-merge/release-spec.md` following `src/superclaude/examples/release-spec-template.md`. Populate frontmatter (spec_type, complexity_score, complexity_class, target_release, feature_id). Include:
  - problem statement citing FINAL-REPORT sections 1 and 6.3
  - accepted proposals with implementation sequencing, each tagged with its CASE (A/B/C/D) classification from Phase 3
  - constraints section with the explicit four-case conflict rule (not just "task-builder takes precedence")
  - FRs per proposal, NFRs (determinism scope, token ceiling, wall-clock), risks, assumptions, test plan
  - **Acceptance criteria section** (NEW, see below)

**Acceptance criteria enforcement (closes the source's gap):**

The source prompt mentions "test plan" in Phase 6 but does not require observable acceptance criteria. Variant 3 mandates an `## Acceptance Criteria` section listing, per accepted proposal:
  - **Observable behavior:** what changes in task-builder's outputs when this proposal is implemented (e.g., "the generated task file contains an R-### -> T<PP>.<TT> table in the index section").
  - **Verification method:** how a human or automated check can confirm the behavior post-implementation (file path, grep pattern, or skill output to inspect).
  - **Negative criterion:** at least one thing that MUST NOT change (e.g., "MDTM self-contained-item invariant is preserved: every B2 item remains executable without external context").

These criteria propagate to Phase 7's spec-panel review and to the PRD in Phase 8. If a proposal cannot articulate observable criteria, it must be downgraded to "deferred" and excluded from this release.

**Failure-mode branches:**

- Template missing: halt; cannot draft without a schema.
- A surviving proposal lacks observable criteria: downgrade to deferred appendix; do NOT silently include.
- Touch+Read freshness hook fails on first write: retry the touch step once; if still failing, halt and surface the hook error.

**Decision gate G6:** spec exists, frontmatter populated, every accepted proposal has an Acceptance Criteria entry with observable behavior + verification + negative criterion. Otherwise halt.

==============================================================================
PHASE 7 — SPEC PANEL REVIEW
==============================================================================

Run:
  /sc:spec-panel @.dev/releases/current/task-builder-merge/release-spec.md \
    --mode critique --focus requirements,architecture,correctness \
    --iterations 2 --format detailed --downstream roadmap

(Verified flags. `--focus` here accepts a comma list per the command file's documented enumeration.)

Apply expert revisions to the spec. The "task-builder precedence" rule is the four-case rule from Phase 3, not the source prompt's one-sided version.

**Conflicting-revision defense process (closes the source's gap):**

If any expert recommendation contradicts the conflict rule, the orchestrator runs this deterministic process:

  Step 1. **Classify the recommendation.** Apply Phase 3's case rule. Which of CASE-A/B/C/D does it map to?

  Step 2. **Identify the protected invariant.** Which task-builder invariant (MDTM self-contained items, evidence-bound items, persistent .dev/tasks/ artifacts, zero-trust QA) does the recommendation challenge?

  Step 3. **Search FINAL-REPORT for evidence.** Cite section + line range that documents either (a) why the invariant matters or (b) prior evidence that the recommendation's approach was rejected. If no citation can be found, escalate (see Step 5).

  Step 4. **Decide:**
    - If FINAL-REPORT cites support the invariant -> REJECT the recommendation; record `state/phase-7-rejection-NN.md` with the expert quote, the cited evidence, and the rejection rationale. The spec is NOT modified.
    - If FINAL-REPORT cites support the expert -> ACCEPT the recommendation; treat as a discovered gap in the four-case rule and update Phase 3's case classifications retroactively in the spec. Note the override in `state/phase-7-overrides.md`.
    - If FINAL-REPORT is silent on the question -> route to Step 5.

  Step 5. **Escalate.** Write `state/phase-7-escalation-NN.md` describing the conflict. The orchestrator MUST surface the file to the user before accepting the revision. Default to REJECT until the user resolves. Conflicting revisions are NEVER silently accepted.

The spec rollback rule: if more than half of the expert recommendations are rejected via Step 4, the orchestrator emits a warning in `state/phase-7-rejection-rate.md` and asks the user whether to (a) keep the spec as-is and proceed to Phase 8, (b) re-run /sc:spec-panel with `--mode discussion` instead of critique for a softer pass, or (c) halt and revisit Phase 3.

**Failure-mode branches:**

- `/sc:spec-panel` crashes / times out: retry once. If still failing, mark Phase 7 DEGRADED and require manual orchestrator review before Phase 8.
- Iterations parameter exceeded but convergence still poor: accept current state, log it, do not auto-extend iterations beyond the documented value.

**Decision gate G7:** spec has been revised through 2 iterations OR the rejection process above has been executed for every conflicting revision AND no escalations remain open without user resolution. Otherwise halt.

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

**INPUT_SPEC handling (closes the source's gap):**

The prd skill's documented Input fields are WHAT / WHY / WHERE / OUTPUT only (see `src/superclaude/skills/prd/SKILL.md` lines 33-43). The skill does NOT recognize `INPUT_SPEC` as a first-class input. Passing it as a literal field risks being silently ignored.

Therefore the orchestrator MUST surface the release spec inside the WHAT and WHERE fields the skill understands:

  - Append to WHAT: ", grounded in the accepted release spec at .dev/releases/current/task-builder-merge/release-spec.md (read this file first; its Acceptance Criteria section drives every requirement in the PRD)."
  - Append to WHERE: ", .dev/releases/current/task-builder-merge/release-spec.md (PRIMARY INPUT SPEC -- treat as authoritative scope)"

Optionally, an `INPUT_SPEC` line may still be included for forward-compatibility, but the orchestrator MUST NOT depend on it. The release-spec.md path appearing inside WHERE is the contractual handoff.

**Acceptance Criteria propagation (closes the source's gap):**

The PRD must mirror the release spec's Acceptance Criteria section. After the prd skill returns, the orchestrator opens the PRD and verifies:
  - Every accepted proposal's observable behavior appears in the PRD's acceptance section.
  - Every negative criterion appears as a non-functional constraint.
If either is missing, re-invoke the prd skill with a targeted "fill missing acceptance criteria from release-spec.md" instruction. Retry budget: 1.

**Failure-mode branches:**

- The prd skill creates an MDTM task file but the eval/research artifacts land outside `.dev/tasks/to-do/` due to a misconfiguration: halt and inspect; the skill-creator workspace override in this repo's CLAUDE.md is for skill-creator, not prd, but a similar misplacement risk applies. Verify with `ls .dev/tasks/to-do/TASK-PRD-*` after the skill returns.
- Output file not written at the OUTPUT path: re-invoke once.
- Output file written but Acceptance Criteria missing: re-invoke once with targeted instruction (above).

The prd skill owns its phasing. Do not inline its protocol.

**Decision gate G8:** PRD exists at OUTPUT path AND its acceptance section mirrors release-spec.md AND no halt-or-degrade artifacts remain unaddressed. Otherwise halt.

==============================================================================
GLOBAL CONSTRAINTS
==============================================================================
- task-builder behaviors are authoritative in CASE-A and CASE-D-with-invariant-violation; CASE-B mechanisms are adopted from /sc:tasklist; CASE-C mechanisms are deferred. Rejected /sc:tasklist mechanisms are documented with reasoning AND the protected invariant. (Supersedes the source prompt's one-sided rule.)
- every claim cites a file path (file:line where applicable); FINAL-REPORT citations include section number
- Phase 1 agents spawn in one message
- /sc:adversarial, /sc:reflect, /sc:analyze, /sc:spec-panel, and the prd and task-builder skills are invoked via their commands/skills -- never reimplemented inline
- All flag usage MUST appear in the verified ground-truth list (Global Failure-Mode Contract item G5). Invented flags are a halt condition.
- Hook compatibility: every new file under `.dev/releases/current/task-builder-merge/` is created via touch + Read before Write (item G4).
- output root: .dev/releases/current/task-builder-merge/
- state artifacts: .dev/releases/current/task-builder-merge/state/ (pipeline-log.md plus DEGRADED, escalation, override, exclusion files)
