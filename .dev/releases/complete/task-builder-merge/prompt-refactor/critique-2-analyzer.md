# Analyzer Critique — Source Prompt for Task-Builder Convergence

Role: Analyzer critic-advocate. Bias: `--persona-analyzer`. Focus: evidence
discipline, citation rigor, false precision, ceremonial steps, untested
assumptions, decision observability.

---

## Analyzer Position (Steelman)

A merger prompt of this scope has three failure modes that dominate everything
else:

1. **Decisions made without citations.** "Best qualities" and "task-builder
   wins" are value judgments that look like facts. Without a binding citation
   gate, the orchestration drifts toward whichever option the model finds
   easiest to articulate.
2. **False precision masquerading as rigor.** Round numerics (`15-25 thoughts`,
   `5-8 proposals`, `convergence 0.80`, `--depth deep`) feel disciplined but
   are not evidence-derived. They turn into cargo-cult ceremony that the
   downstream skills cannot actually enforce.
3. **Ceremonial hand-offs.** Calling `/sc:reflect` without a named output
   artifact and named pass/fail criteria is a ritual, not a decision step.
   The same risk applies to "cross-reference FINAL-REPORT §x" without a
   gate that fails if the cross-reference is missing.

The disciplined alternative is to (a) treat every numeric as outcome-bounded,
not quota-bounded, (b) replace advisory cross-references with a binary
citation gate, (c) fold redundant analysis phases, and (d) make the conflict
rule conditional on five named invariants instead of a blanket assertion.
Variant-2 implements this.

---

## Critique of Source (Baseline)

### A-001 — `15-25 thoughts minimum` is false precision

Source Phase 3 line: "Sequential MCP, 15-25 thoughts minimum."

`mcp__sequential-thinking__sequentialthinking` exposes `thoughtNumber` and
`totalThoughts` as estimates that may be revised up or down mid-run. There is
no evidence in FINAL-REPORT §5 or the adversarial outcomes (§6) that 15
thoughts is a meaningful floor for *this* analysis. The prior study converged
on 5 proposals (§5 table); a quota of 15+ thoughts to design 5–8 proposals is
unjustified anchoring. Fix in variant: outcome-bounded — "stop when each row
of the proposal table has a source-grounded justification."

### A-002 — `5-8 proposals` is unanchored vs. FINAL-REPORT's 5

FINAL-REPORT §5 carries 5 proposals (P1–P5) mapping to 5 RF mechanisms (R1–R5).
The inverse direction (SC→task-builder) does not gain new mechanisms by
inversion alone — it gains new *integration points*. Asking for "5-8" without
naming where the extra 0–3 come from is a license to invent. Variant fixes by
mandating one proposal per FINAL-REPORT mechanism, plus optional extras only
with a Phase 1 digest citation.

### A-003 — `--depth deep --convergence 0.80` are unjustified defaults

Source Phase 4 sets `--depth deep` and `--convergence 0.80`. `/sc:adversarial`
(verified in `src/superclaude/commands/adversarial.md`) accepts both flags,
but FINAL-REPORT §6.1 reports a mean convergence of 0.81 at `--depth quick`
across 5 proposals. There is no evidence that `deep` was load-bearing in the
prior study, nor that 0.80 is the right floor for the inverse direction.
Variant uses `--depth standard` as default with conditional escalation, and
drops the convergence override unless a written justification exists.

### A-004 — Cross-reference advisory is not a gate

Phase 2 says "Cross-reference against FINAL-REPORT.md §3, §4, §6." This is
advice, not enforcement. The orchestrating model can comply by mentioning
"§3" once and move on. Variant replaces advisory cross-references with
required header fields on every proposal (`final_report_citation`,
`direction_inversion_basis`) and a binary Phase 4 gate that halts the
pipeline on any missing field.

### A-005 — Phase 5 `/sc:reflect` is ceremonial

Source Phase 5: "Run /sc:reflect --type task --analyze --validate. Verify
adversarial outcomes respect the conflict rule. Flag for revision …"

`/sc:reflect` (verified flags `--type`, `--analyze`, `--validate`) produces
analytic text, not a binary decision artifact. The "verify the conflict rule"
step is the actual decision and has no specified output schema. In practice
this phase produces a reflection narrative that the downstream phases do not
consume. Variant replaces it with a "Citation & Invariant Gate" producing a
`gate-report.md` with five PASS/FAIL rows (G1–G5). `/sc:reflect` is retained
as optional append, not as the decision point.

### A-006 — Phase 6 frontmatter list claims template fields without re-verification

Source Phase 6 names `spec_type, complexity_score, complexity_class,
target_release, feature_id`. Verification against
`src/superclaude/examples/release-spec-template.md` confirms all five fields
are present in the template's frontmatter block. **This citation is correct
as of read time, but the prompt does not bind itself to the template** — if
the template adds/renames a field, the prompt drifts. Variant fixes by
saying "match the template exactly; if the template diverges, the template
wins."

### A-007 — Phase 1 Bucket F has thin evidence

Source Bucket F lists "sample release specs under `.dev/releases/current/`
for shape reference." Inspection of `.dev/releases/current/` shows two
entries: `auggie-first-hook-proposal.md` (a single proposal file, not a
release spec) and `task-builder-merge/` (this work). There is **no existing
release-spec.md sample under `.dev/releases/current/`** at orchestration
start, so Bucket F's evidence is the template alone. Variant fixes by
adding an explicit Glob step that reports "no sample specs available"
rather than letting the bucket agent fabricate from absence.

### A-008 — Hidden duplication between Phase 2 and Phase 3

Phase 2 runs `/sc:analyze ... --focus architecture --depth deep` to produce
two matrices. Phase 3 then asks Sequential to brainstorm proposals covering
"Determinism, Traceability, Quality gates, Validation stages, Tier
classification, Conflict rule" — every one of which is an architectural
dimension `/sc:analyze` already surfaced. The two phases describe overlapping
matrix work. Variant folds them into one Phase 2 deliverable
(`analysis.md`) containing the capability matrix *and* the proposal
portfolio, eliminating the redundant pass.

### A-009 — "task-builder wins on conflict" lacks evidentiary basis

FINAL-REPORT §6.3 ("Dominant Pattern") found that 4 of 5 RF→SC ports were
over-engineered; the conservative SC-shaped alternatives won. The user's
reversal asserts the inverse direction (SC→task-builder) without engaging
that finding. The blanket "task-builder wins" rule reads as a directional
preference, not an evidence-derived invariant. Variant scopes the rule to
**five named task-builder invariants** (self-contained-item,
evidence-bound-item, persistent `.dev/tasks/` artifact, zero-trust QA,
parallel research) and routes all other conflicts to adversarial debate
and spec-panel review.

### A-010 — Phase 1 Bucket D may reference non-existent files

Source lists rf-task-builder, rf-task-researcher, rf-task-executor,
rf-team-lead, rf-analyst, rf-qa, rf-qa-qualitative. FINAL-REPORT §2.2 only
confirms the first four exist in the llm-workflows repo; the SC repo's
`src/superclaude/agents/rf-*` set was not verified by me in this critique
window. Variant fixes by requiring Bucket D to Glob first and report
"absent" for any missing agent, rather than letting a sub-agent invent.

### A-011 — `--interactive` flag in Phase 4 leaks human-in-loop into a batch pipeline

`/sc:adversarial --interactive` is a documented flag, but this prompt is
written as a replayable orchestration that hands off to subsequent phases.
`--interactive` introduces an unwritten contract (someone must be present
to answer prompts) that none of Phases 5–8 know about. Variant drops it.

---

## Acknowledged Weaknesses of My Variant

- **W-A1.** The Citation & Invariant Gate (Phase 4 in variant) adds a binary
  halt that can stall the pipeline on a missing header field even when the
  proposal itself is sound. This is intentional friction — but a user who
  wants a fast first pass will see the gate as obstructive. The variant has
  no "warn-only" mode.
- **W-A2.** Reducing proposal count from "5–8" to "5 (+optional extras with
  citation)" can miss a genuinely new SC→task-builder integration point that
  is *not* covered by FINAL-REPORT P1–P5. The gate's `direction_inversion_basis`
  requirement makes new proposals harder to admit; this is a
  recall-vs-precision tradeoff biased toward precision.
- **W-A3.** Dropping `--convergence 0.80` defers to the protocol default.
  If the protocol default is weaker than 0.80, variant proposals will pass
  adversarial review at a lower bar than the source prompt would have. I
  have not verified the default value in `sc-adversarial-protocol/SKILL.md`,
  so this risk is real but unquantified.
- **W-A4.** Folding Phase 2 and Phase 3 into one phase reduces total work
  but loses the audit trail of "matrix first, brainstorm second." A reviewer
  who wanted to see the analyst's matrix in isolation now has to find it
  inside a combined artifact.
- **W-A5.** Replacing `/sc:reflect` with a checklist gate trades open-ended
  analysis for binary criteria. If a proposal has a subtle weakness that
  doesn't trip G1–G5, the variant has no second-pass narrative review
  before the release spec is drafted. (`/sc:reflect` is retained as optional,
  but as advisory, not gating.)

---

## Evidence Gaps in the User's Direction

The user's instruction is "task-builder is authoritative when /sc:tasklist
and task-builder disagree; FINAL-REPORT studied RF→SC, this task inverts
it." That instruction makes three unverified assumptions:

- **G-A1. Inversion symmetry.** The user assumes the failure mode of RF→SC
  (porting over-engineered RF mechanisms into SC) is symmetric to SC→task-builder.
  FINAL-REPORT §6.3 frames the failure as "RF mechanisms designed for RF's
  execution context underperform in SC's generation context." The mirror
  claim — that SC mechanisms designed for SC's generation context will
  underperform in task-builder's execution-research context — is at least as
  plausible as the user's assumption. Without engaging this, the reversal
  smuggles a conclusion.
- **G-A2. Authoritative-by-default.** "task-builder wins on conflict" treats
  task-builder's design as a stable reference. FINAL-REPORT contains no
  audit of task-builder's invariants or risks; the user's reversal carries
  no evidence that task-builder's current design is *better* than
  /sc:tasklist's, only that it is the desired target. The variant therefore
  scopes precedence to five named invariants instead of accepting the
  blanket rule.
- **G-A3. Coverage equivalence.** The user implies the inverse direction
  has the same scope as FINAL-REPORT's forward direction. But the forward
  study identified six SC weaknesses (W1–W6) before designing five proposals.
  The reverse direction needs an equivalent task-builder weakness inventory
  — which neither the source prompt nor the user's instructions require.
  The variant compensates by mandating `direction_inversion_basis` per
  proposal, but a deeper fix would be a Phase 0 "task-builder weakness
  inventory" cited from task-builder's own SKILL.md / refs.
- **G-A4. `/sc:reflect` as decision authority.** The source prompt's
  Phase 5 implicitly treats `/sc:reflect` output as adjudicating conflict
  rule adherence. `/sc:reflect`'s documented behavior (`--type task --analyze
  --validate`) is reflection, not adjudication. The user's instruction
  inherits this conflation. Variant separates them.

---

## Files

- Variant: `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/prompt-refactor/variant-2-analyzer.md`
- Critique: this file.

## Verified ground truth used

- `/sc:analyze` flags: `--focus`, `--depth`, `--format` (commands/analyze.md).
- `/sc:adversarial` flags used: `--compare`, `--depth`, `--focus`, `--output`
  (commands/adversarial.md). `--convergence` and `--interactive` available
  but intentionally not used.
- `/sc:reflect` flags: `--type`, `--analyze`, `--validate` (commands/reflect.md).
- `/sc:spec-panel` flags: `--mode`, `--focus`, `--iterations`, `--format`,
  `--downstream` (commands/spec-panel.md).
- `release-spec-template.md` frontmatter fields confirmed:
  `feature_id`, `spec_type`, `complexity_score`, `complexity_class`,
  `target_release`.
- `.dev/releases/current/` content at read time: `auggie-first-hook-proposal.md`
  and `task-builder-merge/` only — no sample release-spec.md present.
