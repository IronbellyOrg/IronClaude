---
title: "RFMerger Refresh — Inferred Release Spec (Selective RigorFlow Borrows into sc:tasklist)"
version: "1.0.0"
status: draft
feature_id: FR-RFMERGE
parent_feature: null
spec_type: refactoring
complexity_score: 0.62
complexity_class: MEDIUM
target_release: v3.8-RigorFlowMerger-tasklist
authors: [user, claude]
created: 2026-06-18
quality_scores:
  clarity: 8.5
  completeness: 8.5
  testability: 8.0
  consistency: 8.5
  overall: 8.4
---

# RFMerger Refresh — Inferred Release Spec

> **Document status.** This is a **refreshed inferred release spec** — a documents-only deliverable
> of TASK-RF-rfmerger-refresh-20260618-172224 (Step 2.3). It infers the release intent of the April-2026
> RigorFlow-Merger (RFMerger) investigation and rebases every retained proposal onto the **current**
> `src/superclaude/...` source-of-truth. It authorizes **no implementation tasklist**, edits no source
> code, and edits no `.claude/` mirror. Two proposals (P2, P5) carried human decisions that are now
> **RECORDED (2026-06-19)**: P2 = `retain-with-full-set-revalidation-and-guards`, P5 =
> `retain-advisory-only`. With both decisions recorded, downstream implementation-tasklist generation is
> now UNBLOCKED.

## 1. Problem Statement

The April-2026 RigorFlow-Merger (RFMerger) investigation produced a five-proposal design package
(P1 Context-Armed Steps, P2 Bounded Patch Loop, P3 DNSP, P4 Evidence-Anchored Validation, P5
Feedback-Driven Tier Calibration) that proposed borrowing selected RigorFlow (RF) execution-time
mechanisms into the SuperClaude `sc:tasklist` generator. That package was authored against a SuperClaude
surface that has since drifted: it assumes a **10-stage** tasklist model, an RF agent-team flow
(`/rf:*` commands, TeamCreate/SendMessage), a `.gfdoc` shell-script execution harness, an external
`llm-workflows` / `/config/.claude` source-of-truth, and a `sc:task-unified` Stage-9 patch delegate.
None of those are operative today. The current generator runs an **11-stage** model with a Stage 10.5
reflect gate, delegates patch execution to `sc:task`, executes MDTM work through the `/task` skill loop,
and treats `src/superclaude/...` as the single source-of-truth with `.claude/` as a generated mirror.

Acting on the historical package verbatim would (a) reintroduce stale tokens as operative instructions,
(b) re-derive proposals against a surface that no longer exists, and (c) ship structural-correctness
defects the adversarial validation already flagged (e.g. P2's subset-only re-validation oscillation
risk, P5's hidden-feedback determinism violation). The problem this spec solves is **refreshing the
release intent** onto current source: deciding, per proposal, what to retain in its adversarially-revised
form, what to defer to an explicit human decision, and what to record as a non-goal — without authoring
any implementation work.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| Current generator is 11-stage (Stages 1–10 + Stage 10.5 Pre-Reflect Sign-off); historical "10-stage-only" model is stale. | `sc-tasklist-protocol/SKILL.md:1525-1558`; current-source-contract-inventory "Tasklist protocol"; `research/02:11`. | Any proposal re-derived against the 10-stage model is mis-anchored. |
| Stage 10.5 is audit-first/advisory: PASS/PARTIAL/FAIL all ship the bundle; `--remediate` offers remediation without auto-mutating phase files. | `SKILL.md:1460-1478`; current-source-contract-inventory "Stage 10.5 is advisory for shipping"; `research/02:18`. | P2/P4 must not overlap or contradict the existing reflect gate. |
| `--no-reflect` skips Stage 10.5 entirely (also auto-set by `--dry-run`); it lives on the slash command, not on `superclaude tasklist validate`. | `SKILL.md:1479-1481`; `commands/tasklist.md:20-39`; `research/03:30-31`. | Refresh must represent the reflect-gate escape hatch accurately. |
| Stage 9 delegates patch execution to `sc:task` (not the stale `sc:task-unified`); tier classification uses the `/sc:task` algorithm (`STRICT > EXEMPT > LIGHT > STANDARD`). | `SKILL.md:130-132,544-548,1409-1427`; `rules/tier-classification.md:7-90`; `research/02:38-39`. | P2's delegate name must remap to `sc:task`. |
| `--no-reflect` / Stage 10.5 generation contracts are **untested** (name search under `tests/` returned no hits). | `research/05` §6; current-source-contract-inventory "Coverage GAPS". | Refreshed test plan must add direct assertions; this is a carried-forward gap. |
| Reflect-guard tests live under `tests/cli/reflect/`, not `tests/reflect/` (`ls -d tests/reflect/` → no such directory). | current-source-contract-inventory OQ-1; phase-1 discovery CF-01. | Validation matrix pins the disk-correct path; OQ-1 ✅ Resolved (fixed at source 2026-06-19): BUILD-REQUEST.md:15 / research-07:137 now use `tests/cli/reflect/`. |

### 1.2 Scope Boundary

**In scope**: (1) inferring the release intent of the historical RFMerger package; (2) rebasing each
canonical P1–P5 proposal onto current `src/superclaude/...` surfaces in its adversarially-revised form;
(3) recording P2 and P5 as explicit human decisions (now RECORDED 2026-06-19: P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`); (4) representing current `sc:tasklist`
Stage 10.5 / `--no-reflect` behavior accurately; (5) defining functional requirements, gate criteria,
risks, and a test plan for the retained proposals; (6) carrying forward the two cross-input open
questions (OQ-1, OQ-2).

**Out of scope**: (1) authoring any implementation tasklist (explicitly forbidden in this task);
(2) editing source code or `.claude/` mirrors; (3) invoking `task-builder` to generate implementation
tasks; (4) RF mechanisms R5 (session management) and R6 (batch-immutability / UID tracking), which are
execution-time concepts judged N/A to SuperClaude generation and recorded as non-goals; (5) selecting a
default for P2 or P5 (auto-defaulting either is a halt condition); (6) re-implementing reflect's own UC-2
P1–P5 fields (those are a separate, quarantined taxonomy — see Appendix A glossary).

## 2. Solution Overview

The refresh adopts the **adversarial winner** disposition for each canonical RFMerger proposal and
rebases it onto today's `sc:tasklist` surface. Three proposals are retained in their conservative,
adversarially-revised forms (P1, P3, P4); two carry explicit human decisions that are now RECORDED
(2026-06-19): P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`. The spec
is the inferred release intent that a later, separate `/task-builder` step may consume — and, with both the
P2 and P5 decisions now recorded at the review checkpoint, that downstream step is authorized.

What changes (as release intent, with downstream implementation now authorized):

- **P1 Context-Armed Steps → retain conservative form.** Add an optional task-level `## Execution Context`
  block (roadmap refs always included; "source areas", not file paths; no `Ensuring:` clause). The
  generator works on roadmap *text*, not a live codebase, so per-step file paths would be hallucinated.
  Acceptance Criteria remain the single source of truth.
- **P2 Bounded Patch Loop → RETAINED (recorded 2026-06-19): `retain-with-full-set-revalidation-and-guards`.**
  Explicit human choice from `defer | retain-with-full-set-revalidation-and-guards`. Retained — implement with:
  full-set re-validation + monotonicity guard + regression detection + 1-extra-pass cap (2 total;
  adversarially-adopted, `artifacts/adversarial-validation.md:141`), with no overlap with Stage 10.5 reflect
  remediation.
- **P3 DNSP (Detect-Nudge-Synthesize-Proceed) → adopt + refine.** On Stage-7 validation-agent retry
  failure, synthesize a conservative HIGH finding and proceed, guarded by (1) an all-agents-fail guard
  (DNSP activates only when ≥1 agent succeeded; zero-success follows the all-agents-fail escalation path
  — a typed `StageError` is release intent / an implementation-time decision, NOT current behavior) and (2) a
  `source: "synthetic-dnsp"` provenance marker on every synthesized finding.
- **P4 Evidence-Anchored Validation → retain as quality-gate passthrough.** Emit
  `TASKLIST_ROOT/validation/gate-results.txt` from the existing quality gate and inject it into Stage 7
  prompts. Reject the original new Stage 6.5 + `generation-evidence.json` PABLOV pipeline (redundant,
  high-authority regex failure surface).
- **P5 Feedback-Driven Tier Calibration → RETAINED advisory-only (recorded 2026-06-19): `retain-advisory-only`.**
  Explicit human choice from `defer | retain-advisory-only`. Retained advisory-only — implement with: render a
  `## Tier Calibration Advisory` section (min 2 matching overrides) with STRICT-downgrade warnings; never mutate
  scored tiers from hidden feedback. Determinism guarantee (precise): **same roadmap → same scored tiers** (scored tiers are
  a pure function of the roadmap alone), and **same roadmap + same `feedback-log.md` → same advisory**
  (the advisory itself varies with `feedback-log.md`, so it is not roadmap-only; only the scored tiers are).
  Per `artifacts/adversarial-validation.md:219,246` the determinism property that is preserved is the
  scored-tier purity, not the advisory output.

What stays the same: the 11-stage model, Stage 10.5's advisory-for-shipping semantics, the `--no-reflect`
escape hatch, the `sc:task` patch delegate, `/task` MDTM execution, Sprint parser conventions, and the
`src/superclaude/...` source-of-truth discipline. The reflect gate never auto-mutates phase files.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| P1 step-context form | Task-level `## Execution Context` block (conservative) | Original per-step `Context:`/`Ensuring:` sub-fields | Generator works on roadmap text, not a live codebase → per-step paths hallucinated; Acceptance Criteria stay the single source of truth (adversarial 22/50 → 34/50, conv. 0.75). |
| P2 disposition | **`retain-with-full-set-revalidation-and-guards`** (recorded 2026-06-19; explicit human choice, not a default) | Auto-adopt subset-only loop | Subset-only re-validation is a structural-correctness defect (oscillation/regression risk); the disposition was a blocking human decision, not an engineering default (adversarial 20/50 → 39/50, conv. 0.85). |
| P3 disposition | Adopt + all-agents-fail guard + `source: "synthetic-dnsp"` provenance | Adopt as-proposed (no guard) | Strongest of the five (adversarial winner, 39/50, conv. 0.80); guards prevent masking total validation failure and keep synthetic findings auditable. |
| P4 evidence mechanism | Quality-gate passthrough (`gate-results.txt` → Stage 7 prompts) | New Stage 6.5 + `generation-evidence.json` JSON/PABLOV pipeline | The existing pre-write quality gate (currently **20 checks**, checks 1-20 across the Sprint-Compatibility / Semantic / Structural sub-gates per `sc-tasklist-protocol/SKILL.md:1132-1194`) already catches orphan deliverables; a new JSON-extraction stage is redundant and adds a regex failure surface (adversarial 27/50 → 39/50, conv. 0.82). (Historical adversarial reasoning cited a "17-point" gate; the current source gate is 20-check.) |
| P5 disposition | **`retain-advisory-only`** (recorded 2026-06-19; explicit human choice, not a default) | Auto-mutate scored tiers from `feedback-log.md` | Auto-mutation violates the "same roadmap → same scored tiers" determinism guarantee (hidden-input problem); advisory-only preserves that guarantee (scored tiers stay roadmap-pure; the advisory varies with `feedback-log.md` and never feeds back into scored tiers); the choice was a blocking human decision, not a default (adversarial 23/50 → 40/50, conv. 0.85). |
| Stale-token handling | Cite `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `sc:task-unified`, 10-stage wording as HISTORICAL-ONLY evidence; rebase onto current source | Treat historical tokens as operative | They name surfaces that no longer exist; promoting them to current guidance would mis-target edits. |
| Implementation authorization | Authorized — documents complete and P2/P5 recorded (2026-06-19); downstream `/task-builder` is a separate, later step that is now unblocked | Generate implementation tasklist now (inside this documents-only task) | Task is documents-only; with P2/P5 now decided and the review checkpoint passed, downstream tasklist generation is authorized as a separate later step. |

### 2.2 Workflow / Data Flow

```
Historical RFMerger package (FINAL-REPORT.md + artifacts/*)        [HISTORICAL-ONLY evidence]
  -> extract canonical P1-P5 + stale assumptions + adversarial revisions
  -> refresh-requirements-ledger.md  (this release, Step 2.1)

Current source-of-truth (src/superclaude/skills/sc-tasklist-protocol/*, commands/tasklist.md,
                         cli/tasklist/*, task-builder/SKILL.md, sc-reflect-protocol/*, tests/tasklist/*)
  -> verify current behavior + responsibility boundaries
  -> spec.md (THIS DOC) + prd.md + tdd.md

Document QA (serialized gates, per document)
  structural -> source-fidelity -> qualitative   (one fix cycle per gate, fix_authorization:false→one true→verify)
  -> blocking human-review checkpoint  (P2 + P5 decisions RECORDED here)

Downstream handoff  (separate, later, NON-BLOCKING step; only after checkpoint records P2+P5)
  -> instruction to invoke /task-builder from refreshed spec/prd/tdd
  -> /task <absolute-path>  executes the resulting MDTM tasklist  (NOT /sc:task)
  -> ignore any stale sc:tasklist-generated RFMerger tasklists


Retained-proposal placement in the CURRENT 11-stage sc:tasklist pipeline (release intent):

  Stage 1 Ingest -> 2 Parse/Bucket -> 3 Convert -> 4 Enrich [P1 ## Execution Context; P5 advisory RETAINED]
    -> 5 Emit -> 6 Self-Check [P4 emit gate-results.txt] -> 7 Roadmap Validation [P4 passthrough; P3 DNSP on agent failure]
    -> 8 Patch Plan -> 9 Patch Execution (delegate: sc:task) [P2 bounded loop RETAINED] -> 10 Spot-Check
    -> 10.5 Pre-Reflect Sign-off (ADVISORY; PASS/PARTIAL/FAIL all ship; skipped under --no-reflect)
```

## 3. Functional Requirements

> Requirements describe the **release intent** for the retained RFMerger proposals as rebased onto the
> current `sc:tasklist` surface. They are traceable to the canonical P1–P5 ledger and current source.
> FR-RFMERGE.2 and FR-RFMERGE.5 were gated behind the P2/P5 human decisions, which are now RECORDED
> (2026-06-19: P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`); both are
> now active implementation requirements.

### FR-RFMERGE.1: P1 Context-Armed Steps (conservative `## Execution Context` block)

**Description**: Generated phase tasks may carry an optional task-level `## Execution Context` block that
includes the relevant roadmap reference(s) and named "source areas" (not file paths). It must not invent
per-step file paths, must not duplicate an `Ensuring:` clause, and must keep Acceptance Criteria as the
single source of truth. The edit target is `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (inline
runtime); the source-side `templates/phase-template.md` reflects the shape (it is not a `.claude/` mirror).

**Emission rule (deterministic)**: The block is emitted at Stage 4 (Enrichment) for a phase task **if and
only if** the roadmap supplies at least one resolvable roadmap reference for that phase (roadmap refs are
always included when present). When the roadmap supplies named "source areas" for the phase, they are listed;
when it does not, the block degrades to a References-only form. The block is **never** emitted with invented
file paths and is omitted entirely when no roadmap reference resolves. Same roadmap → same block (determinism
preserved).

**Exact markdown shape**:

```markdown
## Execution Context
- References: <roadmap ref id(s)>
- Source areas: <named area(s), not file paths>   # omitted when the roadmap supplies none (References-only degraded form)
```

**Schema-collision boundary (vs task-builder)**: `task-builder` already mandates a `## Execution Context`
section in its MDTM template (`src/superclaude/skills/task-builder/SKILL.md:1066,1231`), with sub-bullets
References / Source areas / Key constraints and a "no specific file:line in the block header" rule. The
`sc:tasklist` P1 block **deliberately reuses the same `References` / `Source areas` sub-field names and the
no-file-path discipline** so the two surfaces do not collide semantically; the only difference is that P1's
block is **optional** (emitted per the rule above) whereas task-builder's is **required** in every task file.
Implementation MUST NOT introduce a second, incompatible meaning of "Execution Context"; if the contracts ever
diverge, that divergence is itself a halt condition for the implementing step.

**Acceptance Criteria**:

- [ ] The block, when emitted, contains roadmap refs and "source areas" only — no file paths and no `Ensuring:` clause.
- [ ] No per-step file path is generated (the generator works on roadmap text, not a live codebase).
- [ ] Acceptance Criteria remain unduplicated and authoritative; the block is additive/optional.
- [ ] The deterministic emission rule holds: emitted iff ≥1 roadmap ref resolves; References-only degraded form when no source areas; same roadmap → same block.
- [ ] The block reuses task-builder's `References`/`Source areas` sub-field names and no-file-path discipline; no second, incompatible "Execution Context" meaning is introduced (a no-semantic-collision test asserts this against `task-builder/SKILL.md:1066,1231`).
- [ ] Phase-template assertion/tests cover the block's shape if the block is added.

**Dependencies**: None (retained, conservative — no human gate).

### FR-RFMERGE.2: P2 Bounded Patch Loop — RETAINED (human decision recorded 2026-06-19)

**Description**: P2 proposes, after Stage 10, looping back to Stage 9 to re-patch the unresolved work,
capped at **the original pass + at most 1 re-patch pass = 2 total passes** (i.e. 1 extra cycle) — the
adversarially-adopted cap (`artifacts/adversarial-validation.md:141`; corroborated `FINAL-REPORT.md:236,334`).
The pre-adversarial "3 total passes (original + 2 re-patch)" value is the **rejected** Variant-B design cap
(adversarial 20/50) and is **historical-only**, not the current contract. Its
disposition is a **human decision now RECORDED (2026-06-19) as
`retain-with-full-set-revalidation-and-guards`** (chosen from `defer | retain-with-full-set-revalidation-and-guards`;
explicit choice, not a default). Per that recorded decision, the loop must use full-set re-validation, a monotonicity
guard, regression detection, and the 2-total-pass cap, and must not overlap Stage 10.5 reflect remediation.
The historical Stage-9 delegate `sc:task-unified` remaps to the current `sc:task` delegate. This is now an
active implementation requirement.

**Retained contract (the meaning of the recorded `retain-*` decision).** This contract fixes what "retain" means
now that the human has chosen it:

- **Compared data**: each pass re-runs the **full** Stage-7 validation set over the bundle (not a sampled or
  unresolved-only subset) and records the failing-finding set `F_k` for pass `k`.
- **State model**: `(pass_index k, failing_set F_k, prev_failing_set F_{k-1})`; `k` starts at 1 (the original
  pass), the loop adds pass `k=2` only.
- **Monotonicity predicate**: `|F_{k}| < |F_{k-1}|` must hold to continue; if `|F_k| >= |F_{k-1}|` the loop
  halts (no further re-patch).
- **Regression predicate**: any finding that was PASS at pass `k-1` and is FAIL at pass `k` halts the loop
  immediately (regression takes precedence over monotonicity), reusing the existing PR-02 regression semantics
  in `task-builder/SKILL.md:1290-1305` rather than defining a new one.
- **Cap counting**: at most 1 re-patch pass (`k` ∈ {2}); pass 2 is the last permitted pass (2 total passes; adversarially-adopted cap, `artifacts/adversarial-validation.md:141`).
- **Stage-10.5 non-overlap (exclusion proof obligation)**: the loop operates only on Stage 7→9→10 patch
  findings and MUST be provably disjoint from the Stage 10.5 reflect-remediation finding set (no finding is
  remediated by both surfaces). The implementing step must carry an explicit non-overlap argument/test.

**Acceptance Criteria**:

- [ ] The disposition is recorded as `retain-with-full-set-revalidation-and-guards` (chosen from `{defer, retain-with-full-set-revalidation-and-guards}`; recorded 2026-06-19, explicit human choice, **not a default**).
- [ ] No engineering default for P2 was shipped; the recorded value is an explicit human choice (auto-defaulting P2 would have been a halt condition).
- [ ] Retained — implement with: full-set (not subset-only) re-validation, monotonicity guard (`|F_k| < |F_{k-1}|`), regression detection (PR-02 semantics), the **2-total-pass cap** (original + 1 re-patch; adversarially-adopted per `artifacts/adversarial-validation.md:141`), and provable non-overlap with Stage 10.5 remediation.
- [ ] Downstream implementation-tasklist generation is UNBLOCKED (the P2 decision is recorded and the review checkpoint passed).

**Dependencies**: Blocking human decision (review checkpoint). No source/test work until decided.

### FR-RFMERGE.3: P3 DNSP (Detect-Nudge-Synthesize-Proceed) with guards

**Description**: On Stage-7 validation-agent retry failure, synthesize a conservative HIGH finding for the
affected task range and proceed rather than blocking Stage 8 on a single agent. Two guards are mandatory:
(1) an **all-agents-fail guard** — DNSP activates only when ≥1 validation agent succeeded; if zero
succeeded, zero-success follows the all-agents-fail escalation path (`rf-team-lead`-style fix-cycle
escalation per the reused task-builder Path A, `task-builder/SKILL.md:873-911`) — surfacing it as a typed
`StageError` is release intent / an implementation-time decision, NOT verified current behavior; (2) every synthesized finding carries
`source: "synthetic-dnsp"` provenance metadata. This is the only proposal adopted as-proposed (with the
two refinements).

**Ownership / compatibility boundary (MANDATORY).** A `synthetic-dnsp` contract **already exists** and is
owned by `task-builder` (`src/superclaude/skills/task-builder/SKILL.md:873-911`). It is richer than this
proposal: fixed `severity: HIGH` + `source: "synthetic-dnsp"` fields, a 2-element `dedup_key`
`["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`, a `found_n_times` counter, an
all-agents-fail path (Path A/B/C precedence, R-122), strictly-additive merge semantics, and N-1 cohort
concurrency (INV-021). **P3 in `sc:tasklist` REUSES that existing contract rather than defining a new,
divergent one**: the `sc:tasklist` Stage-7 synthesizer MUST emit findings that conform to the task-builder
`synthetic-dnsp` field contract (same `source` literal, same non-overridable `HIGH` severity, the same
`(assigned_files_range, escalation_ladder_exhaust_point)` dedup-key shape, and the same all-agents-fail
guard). The `sc:tasklist` use is the **narrower** Stage-7-validation-agent case of the same mechanism; it
does not own or redefine the field/dedup/merge contract. Any place `sc:tasklist` would need behavior the
task-builder contract does not provide is a stated boundary to resolve at implementation time, not a silent
fork.

**Acceptance Criteria**:

- [ ] DNSP activates only when ≥1 validation agent succeeded; zero-success follows the all-agents-fail escalation path — surfacing it as a typed `StageError` is an implementation-time decision, not current behavior (no masking of total failure either way).
- [ ] Every synthesized finding carries `source: "synthetic-dnsp"` provenance metadata, conformant to the task-builder field contract (`HIGH` severity non-overridable; 2-element dedup key).
- [ ] Stage 8 is never blocked by a single failed-then-synthesized validation agent (given ≥1 success).
- [ ] P3 reuses the existing `task-builder` `synthetic-dnsp` contract (`task-builder/SKILL.md:873-911`); it does not define a divergent parallel contract. Any required deviation is a stated boundary, not a silent fork.
- [ ] Tests cover synthetic-finding provenance, the all-agents-fail guard, AND compatibility with the existing contract (regression tests modeled on `tests/skills/test_task_builder_merge.py` and `tests/audit/test_dnsp_*` where present).

**Dependencies**: None (retained-with-guard; guards are mandatory — without them P3 is not retained).

### FR-RFMERGE.4: P4 Evidence-Anchored Validation (quality-gate passthrough)

**Description**: Reuse the existing quality gate (Stage 6) to emit `TASKLIST_ROOT/validation/gate-results.txt`
and inject it into the Stage 7 validation-agent prompts. This is an evidence **passthrough**, explicitly
**not** a new Stage 6.5, **not** a `generation-evidence.json` artifact system, and **not** a regex-extraction
PABLOV pipeline.

**`gate-results.txt` serialization contract**:

- **Insertion point**: emitted at the end of Stage 6 (Self-Check), after the existing pre-write 20-check
  quality gate runs and before Stage 7 (Roadmap Validation) consumes it. No new stage is introduced.
- **Content set**: the verbatim plain-text result of the existing 20-check pre-write gate — one line per
  check with its pass/fail record and (on fail) the offending task/file. It is a faithful serialization of
  the gate's own output; it adds no regex-extracted IDs and no derived schema.
- **Format**: plain UTF-8 text (NOT JSON). One check per line, e.g.
  `CHECK 12 PASS: every task has >=1 roadmap item` / `CHECK 11 FAIL: T03.02 description is "TODO"`.
- **Pass record**: every check the gate ran appears with an explicit `PASS`/`FAIL` token; a trailing summary
  line records `GATE: PASS (20/20)` or `GATE: FAIL (<n> failing)`.
- **Empty / success behavior**: on an all-pass gate the file is still emitted (it is a passthrough, not a
  failure log); it contains the per-check PASS lines plus the `GATE: PASS (20/20)` summary. The file is never
  absent when Stage 6 ran.

**Acceptance Criteria**:

- [ ] Stage 6 emits `TASKLIST_ROOT/validation/gate-results.txt` from the existing quality gate (no new gate stage); the file exists whenever Stage 6 ran, including on an all-pass gate.
- [ ] The file is plain text (not JSON), one check per line with explicit PASS/FAIL tokens and a `GATE: PASS|FAIL` summary line; it is the verbatim serialization of the existing 20-check gate output.
- [ ] Stage 7 prompts include the gate-results passthrough content (injected after Stage 6, before Stage 7 consumes it).
- [ ] No new `generation-evidence.json` artifact or regex-extraction stage is introduced.
- [ ] Tests confirm the gate-results passthrough reaches Stage 7 and that the file is emitted on an all-pass gate.

**Dependencies**: None (retained, lighter form — no human gate). Reuses existing quality-gate output.

### FR-RFMERGE.5: P5 Feedback-Driven Tier Calibration — RETAINED advisory-only (human decision recorded 2026-06-19)

**Description**: P5 proposes reading `feedback-log.md` and calibrating tiers. Its disposition is a
**human decision now RECORDED (2026-06-19) as `retain-advisory-only`** (chosen from
`defer | retain-advisory-only`; explicit choice, not a default). Per that recorded decision, the generator
renders a `## Tier Calibration Advisory` section (minimum 2 matching overrides) carrying STRICT-downgrade
warnings, and **never mutates scored tiers** — scored tiers stay a pure function of the roadmap (preserving
determinism). This is now an active implementation requirement.

**Retained contract (the meaning of the recorded `retain-advisory-only` decision).**
This contract fixes what "retain advisory-only" means now that the human has chosen it:

- **Advisory input schema**: a `feedback-log.md` table whose rows carry, at minimum,
  `(roadmap_item_id | task_signature, suggested_tier, observed_count)`. Rows missing any of these fields are
  ignored (they cannot match).
- **Match key**: a feedback row matches a scored task when its `roadmap_item_id` (preferred) or, failing that,
  its `task_signature` equals the task's roadmap item / signature. A "matching override" is a matched row
  whose `suggested_tier` differs from the deterministically scored tier.
- **Min-2 threshold**: the advisory section is rendered only when ≥2 such matching overrides exist; with <2,
  the section is omitted entirely (no partial advisory).
- **Exact markdown output**:

  ```markdown
  ## Tier Calibration Advisory
  > Advisory only — scored tiers are unchanged. Feedback below is informational.
  | Task | Scored tier | Feedback-suggested tier | Observed count | Note |
  |------|-------------|-------------------------|----------------|------|
  | T<PP>.<TT> | STRICT | STANDARD | <n> | ⚠ STRICT-downgrade — review security implications before relying |
  ```

- **STRICT-downgrade warning semantics**: any row where the scored tier is `STRICT` and the feedback suggests
  a lower tier carries an explicit ⚠ STRICT-downgrade warning; the advisory never auto-applies it.
- **Deterministic ordering / omission**: advisory rows are ordered by ascending task ID (`T<PP>.<TT>`); the
  whole section is a pure function of `(roadmap, feedback-log.md)` — same inputs → byte-identical section, and
  it never feeds back into the deterministic scored tier (scored tiers stay a pure function of the roadmap
  alone, so "same roadmap → same scored tiers" holds regardless of feedback).

**Acceptance Criteria**:

- [ ] The disposition is recorded as `retain-advisory-only` (chosen from `{defer, retain-advisory-only}`; recorded 2026-06-19, explicit human choice, **not a default**).
- [ ] No engineering default for P5 was shipped; the recorded value is an explicit human choice (auto-defaulting P5 would have been a halt condition).
- [ ] Retained advisory-only — implement with: the advisory section renders only with ≥2 matching overrides, in ascending-task-ID order, with the exact markdown shape and STRICT-downgrade warnings above; it never alters scored tiers; "same roadmap → same scored tiers" holds.
- [ ] Downstream implementation-tasklist generation is UNBLOCKED (the P5 decision is recorded and the review checkpoint passed).

**Dependencies**: Blocking human decision (review checkpoint). No source/test work until decided.

### FR-RFMERGE.6: Accurate representation of current Stage 10.5 / `--no-reflect` behavior

**Description**: All refreshed documents must represent the current generator behavior accurately:
11-stage model; Stage 10.5 Pre-Reflect Sign-off is audit-first/advisory (PASS/PARTIAL/FAIL all ship the
bundle); `--remediate` offers remediation without auto-mutating phase files; `--no-reflect` skips the
reflect gate entirely (also auto-set by `--dry-run`) and lives on the slash command, not on
`superclaude tasklist validate`. No retained proposal may contradict or silently auto-mutate phase files.

**Acceptance Criteria**:

- [ ] Documents describe the 11-stage model with Stage 10.5, never the stale 10-stage-only model.
- [ ] Stage 10.5 is described as advisory-for-shipping; bundle ships on PASS/PARTIAL/FAIL.
- [ ] `--no-reflect` is described as skipping Stage 10.5 (and the templated post-reflect task), on the slash command only.
- [ ] No retained proposal auto-mutates phase files.

**Dependencies**: None.

### FR-RFMERGE.7: Stale-token quarantine and source-of-truth discipline

**Description**: `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `sc:task-unified`, and the
"10-stage-only" wording appear in refreshed documents **only** as HISTORICAL-ONLY evidence, each paired
with its current rebase target. MDTM execution uses `/task <absolute-path>`, never `/sc:task`. Edits
resolve under `src/superclaude/...` (canonical), with `.claude/` as a generated mirror; never stage
`.claude/{skills,commands,agents,hooks,templates}`.

**Acceptance Criteria**:

- [ ] No stale token appears as a current edit target or operative instruction; each historical mention names a current rebase target.
- [ ] `sc:task-unified` is replaced by `sc:task`; MDTM execution is `/task <path>`, not `/sc:task`.
- [ ] Source edits target `src/superclaude/...`; `.claude/` mirrors are never staged (except `settings.json`).

**Dependencies**: None.

## 4. Architecture

> This is a **refactoring** spec: the architecture describes where the retained proposals attach to the
> existing `sc:tasklist` surface as **release intent**. No source file is created or modified by this
> documents-only task; the tables below describe the surfaces a *later* implementation step would touch.
> All edit targets are canonical `src/superclaude/...` paths; `.claude/` is a generated mirror, never an
> edit target.

### 4.1 New Files

> No new files are created by this documents-only task. The rows below are the **prospective** new
> artifacts a later implementation step would introduce per the retained proposals (release intent only).

| File | Purpose | Dependencies |
|------|---------|-------------|
| `TASKLIST_ROOT/validation/gate-results.txt` (runtime artifact, P4) | Quality-gate evidence passthrough emitted by Stage 6, injected into Stage 7 prompts. | Existing Stage 6 quality gate. |
| Tests under `tests/tasklist/` and/or `tests/skills/test_task_builder_merge.py` (retained-feature gates) | New/refreshed assertions for P1 block, P3 DNSP guard + provenance, P4 passthrough, `--no-reflect`/Stage 10.5, `sc:task` naming, stale-token prevention. | Retained FR set; pytest. |

### 4.2 Modified Files

> Prospective modifications (release intent only — NOT performed in this task). Canonical edit targets;
> `.claude/` copies are regenerated via `make sync-dev`.

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (inline 11-stage runtime — **the single authoritative edit target**) | Stage 4 `## Execution Context` block (P1); Stage 6 `gate-results.txt` emission + Stage 7 prompt injection (P4); Stage 7 DNSP guard + `synthetic-dnsp` provenance (P3); IF P2 retained: bounded Stage-9 loop; IF P5 retained: `## Tier Calibration Advisory` rendering. | Rebase retained proposals onto the inline 11-stage runtime source. This `SKILL.md` is the canonical edit path for every retained proposal. |
| `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (**source-side read-only reference extracted from `SKILL.md`** — NOT a `.claude/` generated mirror) | Do **not** hand-edit. Any `## Execution Context` shape change is made in `SKILL.md` (the authoritative edit target) and reflected into this source-side reference; `make sync-dev` then regenerates the `.claude/` copies. | Source-side static reference for the inline phase template; the term "generated mirror" is reserved for `.claude/` copies only. Respect mirror-lag (do not propagate `rules/file-emission-rules.md` lag). |
| `tests/tasklist/`, `tests/cli/reflect/`, `tests/skills/test_task_builder_merge.py` | Add coverage for retained features + carried gaps. | Close the `--no-reflect`/Stage 10.5 untested gap; assert provenance/guards. |

### 4.3 Removed Files

> No file removals. The historical RFMerger surfaces (`/rf:*` commands, `.gfdoc/scripts/automated_qa_workflow.sh`,
> `.gfdoc/templates/*`, `llm-workflows`, `/config/.claude`) are **not present in this repository** as
> operative source — they were external/historical. There is nothing to remove; they are quarantined as
> HISTORICAL-ONLY evidence and rebased onto current surfaces (see FR-RFMERGE.7).

| File/Section | Reason | Migration |
|-------------|--------|-----------|
| (none) | No operative file is removed by this refresh. | Historical `/rf:*` / `.gfdoc` / `sc:task-unified` references are rebased to `/task-builder` + `/task`, `src/superclaude/templates/workflow/...`, and `sc:task` respectively — by citation, not by editing the stale targets. |

### 4.4 Module Dependency Graph

```
roadmap text (+ optional --spec)
      |
      v
/sc:tasklist (slash wrapper)  --mandatory-->  Skill sc:tasklist-protocol (11-stage generator)
                                                   |
        +------------------------------------------+-------------------------------------------+
        |                          |                          |                                |
   Stage 4 Enrich            Stage 6 Self-Check         Stage 7 Roadmap Validation        Stage 9 Patch Exec
   [P1 ## Exec Context]      [P4 emit gate-results.txt] [P4 inject; P3 DNSP+guards]       delegate: sc:task
   [P5 advisory RETAINED]                                                                 [P2 bounded loop RETAINED]
        |                          |                          |                                |
        +------------------------------------------+-------------------------------------------+
                                                   |
                                                   v
                              Stage 10.5 Pre-Reflect Sign-off (advisory)
                              fans out /sc:reflect --mode pre --remediate per phase
                              (skipped under --no-reflect; never auto-mutates phase files)
                                                   |
                                                   v
                              N+1 file bundle (tasklist-index.md + phase-N-tasklist.md)
                                                   |
                                                   v
                              superclaude tasklist validate (separate CLI; ROADMAP->TASKLIST fidelity only)
```

### 4.5 Data Models

> No new persistent data model is introduced. Two runtime data shapes are referenced as release intent:
> (1) P4 `gate-results.txt` — plain-text quality-gate evidence (not JSON; explicitly **not** a
> `generation-evidence.json` schema); (2) the P3 `source: "synthetic-dnsp"` provenance field.
>
> **Contract ownership (MANDATORY — not a new model).** The `synthetic-dnsp` finding contract **already
> exists and is owned by `task-builder`** (`src/superclaude/skills/task-builder/SKILL.md:873-911`, the
> "DNSP Synthetic Finding Protocol (PR-03)" / DM-003 emission contract). P3 in `sc:tasklist` **reuses that
> contract verbatim** for the narrower Stage-7-validation-agent case; it does **not** define a new or
> divergent field set, and the canonical type does **not** live in current Stage-7/orchestrator code (the
> earlier draft asserting that contradicted §3.x and the task-builder-owned contract). The canonical field
> is `affected_range` (the earlier `task_range` was non-canonical); required fields include `evidence`, a
> fixed `recommendation`, a 2-element `dedup_key`, and `found_n_times`.

```python
# Illustrative only — conforms to the EXISTING task-builder synthetic-dnsp / DM-003 contract
# (task-builder/SKILL.md:873-911). Not a new model; the sc:tasklist Stage-7 use is the narrower case.
synthesized_finding = {
    "severity": "HIGH",                       # fixed, non-overridable (R-113); reject if != "HIGH"
    "source": "synthetic-dnsp",               # fixed literal, non-overridable (R-114); reject if != "synthetic-dnsp"
    "affected_range": "<assigned_files slice>",  # verbatim spawn-prompt slice, byte-for-byte (R-115); never normalized
    "evidence": "<spawn-log path>",           # NEVER blank (R-116); else "<!-- evidence-absence: no-spawn-log: <reason> -->"
    "recommendation": "Manual review required — partition agent failed twice",  # fixed byte-exact string (R-117)
    "dedup_key": ["<affected_range>", "<escalation_ladder_exhaust_point>"],      # 2-element YAML list (R-118)
    "found_n_times": 1,                        # int >=1, default 1; +1 per within-cycle dedup collapse (R-119)
}
# Guard 1 (all-agents-fail precedence, R-122): zero-success → Path A (all-agents-fail escalation path;
#   NO synthetic emits — a typed StageError is release intent / an implementation-time decision, NOT current
#   behavior; see §4.5 caveat above). >=1 success AND >=1 exhaust → Path B (synthetic emits ALONGSIDE real
#   findings, strictly additive). All-success → Path C (no synthetic; normal merge).
```

### 4.6 Implementation Order

> Dependency-respecting order for a **later** implementation step (not executed here). P2 and P5 steps
> are now active (both decisions recorded 2026-06-19: P2 retain-with-full-set-revalidation-and-guards,
> P5 retain-advisory-only).

```
1. Refresh docs + record P2/P5 decisions   -- THIS RELEASE (spec/prd/tdd + ledger + matrix); review checkpoint
2. P4 gate-results passthrough             -- depends on 1; lowest risk, reuses existing gate
   P1 ## Execution Context block           -- [parallel with step 2]; template-only, additive
3. P3 DNSP + all-agents-fail guard + provenance  -- depends on 1; touches Stage 7 / orchestrator merge
4. [IF P2 == retain] Bounded Patch Loop    -- depends on 1 (decision recorded), 3; must not overlap Stage 10.5
   [IF P5 == retain] Tier Calibration Advisory  -- depends on 1 (decision recorded); advisory-only, determinism-preserving
5. Tests for all retained features + carried gaps  -- depends on 2,3,(4); close --no-reflect/Stage 10.5 gap
```

## 5. Interface Contracts / Gate Criteria

### 5.1 CLI Surface

> No CLI surface is added or changed by this refresh. The current surface is documented accurately so no
> retained proposal silently alters it. The slash command is a wrapper that mandatorily invokes
> `Skill sc:tasklist-protocol`; the generator does not run from the command file alone.

```
/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]
superclaude tasklist validate <output_dir> [--roadmap-file ...] [--tasklist-dir ...] [--model ...]
                                           [--max-turns ...] [--debug] [--tdd-file ...] [--prd-file ...]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--spec` (slash) | path / `@file` | none | Optional supplementary spec/context; must resolve to a readable file when provided. Threaded into the Stage 10.5 PRE reflect; lives on the slash command only. |
| `--output` (slash) | dir | derived `TASKLIST_ROOT` | Output directory for the bundle. |
| `--no-reflect` (slash) | flag | off | Skips Stage 10.5 (pre-reflect sign-off) and the templated post-reflect task; auto-set by `--dry-run`. Slash command only — NOT on `superclaude tasklist validate`. |
| `--tdd-file` (validate) | existing path | autowired from `.roadmap-state.json` | Supplementary TDD validation input; adds testing-strategy/rollback/component/data-model/API checks (missing → MEDIUM). |
| `--prd-file` (validate) | existing path | autowired from `.roadmap-state.json` | Supplementary PRD validation input; adds personas/metrics/acceptance/priority checks (missing → MEDIUM, priority contradiction → LOW). |
| `--model` (validate) | str | `""` (empty) | Overrides the validation step model; subprocess uses `step.model or config.model`. |

> `superclaude tasklist validate` is **validation-only**: it validates ROADMAP → TASKLIST alignment
> (not spec→tasklist or roadmap→spec), exits 1 on HIGH-severity deviations, and does not own `--no-reflect`.
> There is **no** `tasklist generate` CLI subcommand; inference-based generation is the `/sc:tasklist`
> skill path.
>
> **Surface split (do not conflate).** Supplementary-input enrichment exists on **two distinct surfaces**:
> (1) the slash generator (`/sc:tasklist`) takes optional `--spec` (a single supplementary spec/TDD context
> threaded into generation + the Stage 10.5 PRE reflect; spec-resolution order is explicit `--spec` →
> autowired TDD/PRD from `.roadmap-state.json` → the roadmap itself, per `SKILL.md:1466-1471`); (2) the
> validate CLI takes `--tdd-file`/`--prd-file`, **autowired from `.roadmap-state.json`** when omitted. These
> are not the same flag and must not be merged into one "autowire" claim.
>
> **Open risk (not settled here).** The `sc:tasklist` skill body is internally inconsistent on this point: it
> declares "you receive exactly one input: the roadmap text ... the only source of truth"
> (`SKILL.md:49-57`) while elsewhere supporting `--spec` supplementary TDD/PRD enrichment and autowire
> (`SKILL.md:169-182,1297-1308,1466-1471`). This refresh does **not** treat autowire-vs-roadmap-only as
> settled; the contradiction is carried as an open item (see §11) for upstream-source reconciliation, not
> resolved by this documents-only spec.

### 5.2 Gate Criteria (per-document QA, this release)

> Document-QA gates for the refreshed deliverables. Gates run serialized with single-cycle fix
> authorization: spawn all report-only agents (`fix_authorization: false`) for one gate type, consolidate,
> and only if a report-only agent FAILs spawn exactly **one** fix agent (`fix_authorization: true`), then
> report-only verification agents; **halt after one failed fix cycle** and record the blocker in Open
> Questions. (See `refresh-validation-matrix.md` for per-output rows.)

| Gate | What it checks | Halt condition |
|------|----------------|----------------|
| Structural | Required sections present; frontmatter complete; **zero remaining template placeholder sentinels** (the `SC_PLACEHOLDER` double-brace pattern); FR/NFR IDs + acceptance criteria present; output paths correct; conforms to `release-spec-template.md`. | Any structural agent FAILs after one serialized fix cycle. |
| Source-fidelity | Every canonical P1–P5 row retained/revised/explicit-non-goal and mapped to current `src/superclaude/...` evidence; 11-stage + Stage 10.5 model accurate (not 10-stage). | Any P1–P5 row missing/unmapped, or any stale token operative. |
| Qualitative | Responsibility boundaries (`sc:tasklist` / task-builder / reflect / CLI validate); Stage 10.5 + `--no-reflect` coherence; no hidden tier mutation; no implementation-ready claim before review. | Any qualitative agent FAILs after one fix cycle, or product direction auto-defaults P2/P5. |
| Runtime (test) | `uv run pytest tests/tasklist/ -v` (+ PRD/autowire and `tests/cli/reflect/` suites) green; refreshed test plan adds retained-feature coverage. | Required test suites fail. |
| Sync | `make sync-dev` then `make verify-sync`; artifacts live under the release dir or `src/superclaude/...`; never stage `.claude/{skills,commands,agents,hooks,templates}`. | `make verify-sync` fails, or any `.claude/` mirror is staged. |
| Human-decision | P2 recorded as `retain-with-full-set-revalidation-and-guards` and P5 as `retain-advisory-only` (recorded 2026-06-19; explicit human choices, not defaults). | P2 or P5 auto-defaulted, or an implementation-ready claim made before the review checkpoint. |

### 5.3 Phase Contracts (retained-proposal runtime contracts within `sc:tasklist`)

> Inter-stage contracts the retained proposals must honor inside the current 11-stage generator.
> These are runtime contracts for a *later* implementation step — not new pipeline phases authored here.

```yaml
P1_execution_context:           # FR-RFMERGE.1
  stage: 4                       # Enrichment
  emits: "optional `## Execution Context` block on a phase task"
  must_include: ["roadmap_refs", "source_areas"]
  must_not_include: ["file_paths", "Ensuring_clause", "duplicate_acceptance_criteria"]

P4_gate_results_passthrough:    # FR-RFMERGE.4
  emit_stage: 6                  # Self-Check / existing quality gate
  artifact: "TASKLIST_ROOT/validation/gate-results.txt"   # plain text, NOT JSON
  consume_stage: 7               # injected into Roadmap Validation prompts
  forbids: ["new Stage 6.5", "generation-evidence.json", "regex-extraction PABLOV pipeline"]

P3_dnsp:                        # FR-RFMERGE.3
  stage: 7                       # validation-agent failure handling / orchestrator merge
  activate_when: ">=1 validation agent succeeded"
  on_zero_success: "all-agents-fail escalation path (task-builder Path A); typed StageError = release intent, NOT current behavior"
  synthesized_finding: { severity: HIGH, source: "synthetic-dnsp" }
  never: "block Stage 8 on a single failed-then-synthesized agent (given >=1 success)"

P2_bounded_patch_loop:          # FR-RFMERGE.2 — RETAINED (recorded 2026-06-19)
  decision: retain-with-full-set-revalidation-and-guards  # chosen from {defer | retain-with-full-set-revalidation-and-guards}; recorded 2026-06-19, explicit human choice, NOT a default
  retained:
    revalidation: "full-set (NOT subset-only)"
    guards: ["monotonicity_guard", "regression_detection", "1_extra_pass_cap_2_total"]  # original + at most 1 re-patch pass = 2 total (adversarial-validation.md:141)
    must_not: "overlap Stage 10.5 reflect remediation"
  delegate: sc:task              # remaps historical sc:task-unified

P5_tier_calibration_advisory:   # FR-RFMERGE.5 — RETAINED advisory-only (recorded 2026-06-19)
  decision: retain-advisory-only  # chosen from {defer | retain-advisory-only}; recorded 2026-06-19, explicit human choice, NOT a default
  retained_advisory_only:
    renders: "## Tier Calibration Advisory section (min 2 matching overrides) + STRICT-downgrade warnings"
    must_not: "mutate scored tiers (scored tiers stay a pure function of the roadmap)"
    invariant: "same roadmap -> same scored tiers (always; scored tiers are roadmap-pure); same roadmap + same feedback-log.md -> same advisory output (when P5 advisory retained). The advisory is a function of (roadmap, feedback-log.md) and MUST NEVER feed back into scored tiers."

stage_10_5_invariant:           # FR-RFMERGE.6 — unchanged current behavior
  semantics: "advisory-for-shipping: PASS/PARTIAL/FAIL all ship the bundle"
  remediate: "offers remediation WITHOUT auto-mutating phase files"
  no_reflect: "skips Stage 10.5 entirely (also auto-set by --dry-run); slash command only"
```

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-RFMERGE.1 | Generation determinism preserved | Same roadmap (+ same `--spec`) → same scored tiers (always; scored tiers are a pure function of the roadmap). With P5 advisory retained, a byte-identical bundle additionally requires the same `feedback-log.md` — i.e. byte-identical bundle ⇔ same `(roadmap, --spec, feedback-log.md)` tuple, since the advisory varies with `feedback-log.md`. | P5 advisory (retained) renders without mutating scored tiers; determinism test asserts identical scored tiers across runs (roadmap-only), and identical advisory across runs with the same `feedback-log.md`. |
| NFR-RFMERGE.2 | No overlap/conflict with the existing Stage 10.5 reflect gate | Zero double-remediation of the same finding | P2 bounded loop (retained) provably disjoint from Stage 10.5 remediation; reviewed in qualitative gate. |
| NFR-RFMERGE.3 | Source-of-truth discipline | All edits under `src/superclaude/...`; `.claude/` mirrors regenerated, never staged | `make verify-sync` green; git-status safety check shows no staged `.claude/{skills,commands,agents,hooks,templates}`. |
| NFR-RFMERGE.4 | Sprint-parser compatibility of any downstream tasklist | `phase-N-tasklist.md` literal filenames; `### T<PP>.<TT>` headings; Execution Mode ∈ {claude, python, skip} | CODE-VERIFIED against `src/superclaude/cli/sprint/config.py:15-32,34-55,73-124,134-146`. |
| NFR-RFMERGE.5 | Auditability of synthesized validation findings | 100% of synthetic findings carry `source: "synthetic-dnsp"` | P3 provenance test; grep of validation output. |
| NFR-RFMERGE.6 | Documents-only safety | Zero source-code edits and zero implementation tasklists produced by this task | Review checkpoint + git status; no `task-builder` invocation for implementation tasks. |
| NFR-RFMERGE.7 | Zero placeholder leakage | A grep for the `SC_PLACEHOLDER` double-brace sentinel pattern over `spec.md` returns 0 | Structural gate sentinel self-check. |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| P2 patch-loop oscillation/regression (historical risk K4) | Med | High | P2 recorded `retain-with-full-set-revalidation-and-guards` (2026-06-19); retained with full-set re-validation + monotonicity guard + regression detection + 1-extra-pass cap (2 total; `artifacts/adversarial-validation.md:141`) + non-overlap with Stage 10.5. |
| P5 hidden-feedback determinism violation (historical risk K2) | Med | High | P5 recorded `retain-advisory-only` (2026-06-19); advisory-only — scored tiers never mutated; determinism test gate. |
| Stale token re-promoted as operative instruction (`/rf:*`, `.gfdoc`, `sc:task-unified`, 10-stage wording) | Med | High | Source-fidelity + stale-token gates; each historical mention paired with a current rebase target; `sc:task-unified` → `sc:task`. |
| P2/P5 auto-defaulted by a downstream synthesis pass | Low | High | Auto-defaulting either is an explicit halt condition; review checkpoint records both before any downstream tasklist generation. |
| Implementation tasklist generated inside this documents-only task | Low | High | Authorization boundary: no `task-builder` implementation invocation; downstream handoff is a separate, later, non-blocking step. |
| P3 DNSP masks a total validation failure | Low | High | All-agents-fail guard: DNSP activates only when ≥1 agent succeeded; zero-success follows the all-agents-fail escalation path (release intent: `StageError`; no typed `StageError` in current source — see §4.5 caveat). |
| Reflect-guard test command pins a non-existent path (`tests/reflect/`) | Med | Med | Standardize on disk-verified `tests/cli/reflect/`; OQ-1 ✅ Resolved (fixed at source 2026-06-19) — BUILD-REQUEST.md:15 / research-07:137 now use `tests/cli/reflect/`. |
| Mirror-lag in `rules/file-emission-rules.md` propagated as runtime truth | Low | Med | Respect mirror-lag, do not propagate; the inline `SKILL.md` copy is the runtime source; never hand-edit the mirror. |
| `--no-reflect` / Stage 10.5 generation contracts remain untested | High | Med | Refreshed test plan adds direct assertions (carried gap from `research/05` §6). |

## 8. Test Plan

> Test plan for the retained proposals plus the carried coverage gaps. The P2/P5 human decisions are now
> recorded (2026-06-19: P2 retain-with-full-set-revalidation-and-guards, P5 retain-advisory-only), so their
> test work is an active implementation requirement, not conditional. All commands are UV-only and
> disk-verified. The reflect-guard suite path is `tests/cli/reflect/` (NOT `tests/reflect/`).

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| P1 `## Execution Context` shape | `tests/tasklist/test_tasklist_cli.py` (new test fn `test_execution_context_block_shape`) and/or `tests/skills/test_task_builder_merge.py` (PR-01 Execution Context). **Discovery item**: locate the Stage-4 enrichment emit fn in `sc-tasklist-protocol/SKILL.md`/`cli/tasklist/` before authoring. | Block contains roadmap refs + source areas only; no file paths; no `Ensuring:`; Acceptance Criteria unduplicated; emitted iff ≥1 roadmap ref. **Assertion**: parse a generated phase file fixture, assert the block matches the exact shape and omits on no-ref. |
| P3 DNSP synthetic provenance | `tests/skills/test_task_builder_merge.py` (PR-03 DNSP synthetic findings) + new fn in `tests/tasklist/test_tasklist_cli.py` (`test_dnsp_synthetic_provenance`). **Discovery item**: locate the Stage-7 validation/orchestrator-merge fn that emits findings before authoring. | Every synthesized finding carries `source: "synthetic-dnsp"`, `severity: HIGH`, and the 2-element dedup key. **Assertion**: feed a simulated single-agent failure (≥1 success), assert the merged finding set contains exactly one synthetic record with the conformant fields. |
| P3 all-agents-fail guard | new fn `test_dnsp_all_agents_fail_escalates` in `tests/tasklist/test_tasklist_cli.py`. **Discovery (implementation-time)**: no typed `StageError` exists in current source (§4.5 caveat), so the raise site is a NEW requirement, not a confirm-existing — decide whether the escalation is surfaced as a typed `StageError` or the existing all-agents-fail escalation path. | Zero-success → all-agents-fail escalation (release intent: `StageError`); ≥1 success → synthesize + proceed. **Assertion**: on a zero-success fixture, no synthetic is emitted and the escalation path fires. |
| P4 gate-results passthrough | new fn `test_gate_results_passthrough` in `tests/tasklist/test_tasklist_cli.py`. **Discovery item**: locate the Stage-6 self-check fn and the Stage-7 prompt-build fn. | Stage 6 emits `gate-results.txt` (plain text, present even on all-pass); Stage 7 prompt includes it; no `generation-evidence.json`, no Stage 6.5. **Assertion**: run generation on a fixture roadmap, assert the file exists + content substring appears in the captured Stage-7 prompt. |
| `--no-reflect` / Stage 10.5 generation contract (carried gap) | new fns `test_no_reflect_skips_stage_10_5` + `test_stage_10_5_advisory_ships_all_verdicts` in `tests/tasklist/test_tasklist_cli.py`. **Discovery item**: locate the Stage-10.5 invocation + the `--no-reflect`/`--dry-run` flag handling in `commands/tasklist.md` / `cli/tasklist/`. | `--no-reflect` skips Stage 10.5; Stage 10.5 advisory PASS/PARTIAL/FAIL all ship; never auto-mutates phase files. **Assertion**: assert bundle ships and phase-file bytes unchanged across PASS/PARTIAL/FAIL; assert skip under `--no-reflect`. |
| Slash-command flag coverage (carried gap) | new fn `test_slash_flag_parsing` in `tests/tasklist/test_tasklist_cli.py`. **Discovery item**: confirm flag parse site in `commands/tasklist.md` / `cli/tasklist/commands.py`. | `/sc:tasklist` `--spec`, `--output`, `--no-reflect` parsed/validated. **Assertion**: parametrized parse cases assert each flag resolves to the documented default/value. |
| `sc:task` naming (not `sc:task-unified`) | `tests/tasklist/test_tasklist_cli.py` / new assertion | Stage-9 delegate and tier classification reference `sc:task`. |
| P2 bounded-loop guards (RETAINED, recorded 2026-06-19) | new — active (P2 == `retain-with-full-set-revalidation-and-guards`) | Full-set re-validation, monotonicity guard, regression detection, 1-extra-pass cap (2 total), non-overlap with Stage 10.5. |
| P5 advisory determinism (RETAINED, recorded 2026-06-19) | new — active (P5 == `retain-advisory-only`) | Advisory section never alters scored tiers; same roadmap → same scored tiers. |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| Existing tasklist fidelity suite stays green | `uv run pytest tests/tasklist/ -v` — retained proposals do not regress ROADMAP→TASKLIST fidelity. |
| PRD/autowire suites stay green | `uv run pytest tests/tasklist/test_prd_cli.py tests/tasklist/test_prd_prompts.py tests/tasklist/test_autowire.py -v`. |
| Reflect-guard suite stays green | `uv run pytest tests/cli/reflect/ -v` (`test_marker_suppression.py`, `test_docs_cli_parity.py`). |
| RFMerger retained-feature gate | `tests/skills/test_task_builder_merge.py` (PR-01..PR-07) plus audit tests `tests/audit/test_inherited_verdict_freshness_inv_002.py`, `tests/audit/test_five_axes_overlay.py`. |
| Sync coverage | `make sync-dev && make verify-sync`; `tests/cli/test_verify_sync_hooks.py` (V1-V7). |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| Stage 10.5 advisory ships on FAIL | Generate a bundle for a roadmap that produces a Stage 10.5 FAIL verdict (reflect enabled). | Bundle still ships; index records `reflect_pre: FAIL ...` + report link; phase files unmutated. |
| `--no-reflect` skips reflect gate | Run `/sc:tasklist <roadmap> --no-reflect`. | Stage 10.5 skipped; no pre-reflect sign-off and no templated post-reflect task; bundle ships. |
| Document QA gate sequence | Run structural → source-fidelity → qualitative gates on refreshed `spec.md`. | Each gate runs report-only first; one fix cycle max; halt + Open-Questions blocker if a gate FAILs twice. |
| P2/P5 human-decision checkpoint | Present P2/P5 decision spaces at the review checkpoint. | Both recorded explicitly (2026-06-19: P2 retain-with-full-set-revalidation-and-guards, P5 retain-advisory-only); no default; downstream tasklist generation is now UNBLOCKED. |

## 9. Migration & Rollout

> This refresh is documents-only; the migration notes describe rollout of the **retained proposals** by a
> later implementation step (release intent), not of this spec.

- **Breaking changes**: None for users of `/sc:tasklist`. P1 adds an optional additive block; P3/P4 are
  internal to validation; P2/P5 are now recorded (retain) and are active implementation requirements. No CLI surface changes; no
  change to Stage 10.5 advisory semantics or `--no-reflect`.
- **Backwards compatibility**: Full. Bundles remain N+1 files with Sprint-compatible filenames/headings;
  determinism is preserved (P5 advisory, retained, never mutates scored tiers). Stage 10.5 still ships
  on PASS/PARTIAL/FAIL.
- **Rollback plan**: Each retained proposal is independently revertible. P4 passthrough = remove
  `gate-results.txt` emission + Stage 7 injection. P1 = remove the optional block from the Stage 4
  template. P3 = remove the synthesize path (fall back to the all-agents-fail escalation path; release
  intent: `StageError`, §4.5 caveat). P2/P5 (now retained) remain
  revertible to `defer` with no determinism/loop residue. Source rollback uses
  `src/superclaude/...` git history + `make sync-dev`.
- **Sequencing**: Refresh docs + record P2/P5 decisions (this release) → review checkpoint → separate,
  later `/task-builder` step → `/task <absolute-path>` execution. Ignore any stale
  `sc:tasklist`-generated RFMerger tasklists from the historical package.

## 10. Downstream Inputs

> This spec feeds the sibling refreshed `prd.md` and `tdd.md`, the `refresh-requirements-ledger.md`, the
> `refresh-validation-matrix.md`, and (after the review checkpoint) a downstream `/task-builder` handoff.
> **No implementation tasklist is generated by this task.**

### For sc:roadmap

Themes/milestones for a later roadmap derived from the retained proposals (advisory only — not generated
here):

- **Theme: Validation robustness** — P3 DNSP (with guards), P4 quality-gate evidence passthrough.
- **Theme: Task self-containment** — P1 conservative `## Execution Context` block.
- **Theme: Patch convergence** — P2 bounded patch loop (retained; human decision recorded 2026-06-19).
- **Theme: Tier feedback** — P5 advisory-only calibration (retained; human decision recorded 2026-06-19).
- **Theme: Coverage hardening** — close the `--no-reflect`/Stage 10.5 untested gap; add `sc:task`-naming
  and stale-token-prevention tests.

### For sc:tasklist

Task-breakdown guidance for the **later, separate** step (after the review checkpoint records P2/P5):

- Generate from the refreshed `spec.md` + `prd.md` + `tdd.md` via `/task-builder`, then execute with
  `/task <absolute-path>` (NOT `/sc:task`).
- Any generated tasklist MUST preserve Sprint parser conventions: literal `phase-N-tasklist.md` filenames,
  `### T<PP>.<TT>` task headings, Execution Mode ∈ {claude, python, skip}.
- Include P2 and P5 implementation tasks: both human decisions recorded a `retain-*` choice (2026-06-19:
  P2 retain-with-full-set-revalidation-and-guards, P5 retain-advisory-only).
- The current generator is 11-stage with an advisory Stage 10.5 reflect gate and a `--no-reflect` escape
  hatch — generated tasks must not assume the stale 10-stage model.

## 11. Open Items

> Carries forward the two cross-input open questions from Phase 1 discovery. Both are out of this spec's
> edit scope to *resolve* (they require edits to BUILD-REQUEST.md / research files); they are recorded
> here so a downstream builder does not lose them.

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| **OQ-1** | ✅ Resolved (fixed at source 2026-06-19). The matrix command is pinned to the disk-correct `uv run pytest tests/cli/reflect/ -v`, AND the upstream sources are now corrected: `BUILD-REQUEST.md:15` and `research/07-gap-fill-output-contracts.md:137` now use `tests/cli/reflect/` (with a dated correction note). The disk path remains `tests/cli/reflect/` (not `tests/reflect/`). | None remaining — a builder reading the source files verbatim now reads the disk-correct path. | RESOLVED: matrix command pinned + sources fixed at source 2026-06-19. No further action. |
| **OQ-2** | 5-vs-7 output-count taxonomy (resolved): the **five core documents** (`spec.md`, `prd.md`, `tdd.md`, `artifacts/refresh-requirements-ledger.md`, `artifacts/refresh-validation-matrix.md`) are the **GATED deliverables** — the set the validation matrix gates per-output. `artifacts/review-checkpoint.md` and `artifacts/downstream-task-builder-handoff.md` are **DERIVED control artifacts** (CR-5-/CR-7-derived: review-gate and handoff control surfaces, not gated content deliverables), and `phase-outputs/reports/final-validation-evidence-report.md` is a **process report**. The "7" historically conflated the 5 gated deliverables with 2 derived control artifacts. | Downstream synthesis must not count derived control artifacts / process reports as gated deliverables. | RESOLVED here (in-package taxonomy): 5 GATED deliverables + 2 DERIVED control artifacts + 1 process report. The residual raw-research-file wording (`research/07:46-50` / research-notes) is **WAIVED** — the refreshed spec/PRD/TDD are the authoritative inputs for any downstream `/task-builder` run and supersede the raw research notes. |
| **Q-P2** | P2 disposition: `defer` vs `retain-with-full-set-revalidation-and-guards`. **RECORDED 2026-06-19 as `retain-with-full-set-revalidation-and-guards`** (explicit human choice, no default). | Was blocking downstream implementation-tasklist generation; now decided, so that step is unblocked. | Recorded at the review checkpoint per `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/phase-outputs/reviews/p2-human-decision-record.md`. |
| **Q-P5** | P5 disposition: `defer` vs `retain-advisory-only`. **RECORDED 2026-06-19 as `retain-advisory-only`** (explicit human choice, no default). | Was blocking downstream implementation-tasklist generation; now decided, so that step is unblocked. | Recorded at the review checkpoint per `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/phase-outputs/reviews/p5-human-decision-record.md`. |
| **Downstream precondition** | ✅ **SATISFIED — `/task-builder` handoff is AUTHORIZED (2026-06-19).** OQ-1 fixed-at-source ✅ (BUILD-REQUEST.md:15 + research/07:137 now use `tests/cli/reflect/`); OQ-2 in-package-resolved ✅ + research-file residual WAIVED (refreshed spec/PRD/TDD are authoritative) ✅; Q-P2/Q-P5 recorded ✅ (2026-06-19); review signed off ✅. The `--spec` exact-input-contract §22 item remains a carried implementation-time design risk for the future builder to settle — it is NOT a handoff blocker. | None — all handoff preconditions are met; the builder reads disk-correct facts and an authoritative deliverable taxonomy. | AUTHORIZED: downstream handoff unblocked; recorded P2/P5 satisfied; signed off at the review checkpoint. §22 carried as an implementation-time risk, not a gate. |
| Mirror-lag | `rules/file-emission-rules.md` omits the post-reflect terminal task that the inline `SKILL.md` has — known mirror lag. | Editing the mirror as if it were runtime truth would diverge from the runtime source. | Respect, do not propagate; the inline `SKILL.md` copy is authoritative; regenerate mirrors via `make sync-dev`. |
| Autowire-vs-roadmap-only | The `sc:tasklist` skill body contradicts itself: "exactly one input: the roadmap text" (`SKILL.md:49-57`) vs `--spec` supplementary TDD/PRD enrichment + `.roadmap-state.json` autowire (`SKILL.md:169-182,1466-1471`). | A builder would inherit a conflated/contradictory input contract. | Reconcile the skill body at source (out of this spec's edit scope); the spec §5.1 documents the two surfaces separately and flags this as unsettled. |

### 11.1 Stale-Documentation Warnings

> The historical RFMerger package contains tokens that MUST NOT be treated as current operative
> instructions. They appear in this spec only as HISTORICAL-ONLY evidence, each paired with its current
> rebase target. A downstream reader encountering any of these as a current edit target should STOP.

| Stale token / wording (HISTORICAL-ONLY) | Current operative equivalent (do not edit the stale form) |
|---|---|
| `/rf:*` (e.g. `/rf:taskbuilder`, `/rf:pipeline`, `/rf:run`) + TeamCreate/SendMessage agent-team flow | `/task-builder` (Agent tool; no agent teams) for authoring, then `/task <absolute-path>` for MDTM execution. |
| `.gfdoc` (e.g. `.gfdoc/scripts/automated_qa_workflow.sh`, `.gfdoc/templates/...`) | Source of truth is `src/superclaude/templates/workflow/...`; execution is the `/task` skill loop, not a shell script. (`.claude/templates/workflow/...` is a generated mirror, not an edit target.) |
| `llm-workflows` (`/config/workspace/llm-workflows/`) | In-repo `src/superclaude/...`. |
| `/config/.claude` (global-config SC source) | In-repo `src/superclaude/...`; never edit `/config/.claude`. |
| `sc:task-unified` (historical Stage-9 patch delegate) | `sc:task` (current Stage-9 patch-execution delegate). |
| "10-stage-only" tasklist wording (no reflect gating, no PRD/TDD enrichment) | **11-stage** model with Stage 10.5 advisory reflect gate + `--no-reflect` + PRD/TDD autowire. |

## 12. Brainstorm Gap Analysis

> Gaps surfaced by the Phase 1 discovery and adversarial validation that shaped this refresh. Severity is
> relative to the documents-only release intent.

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| G-1 | P2/P5 dispositions are blocking human decisions, not engineering defaults — must never auto-default. | high | §3 (FR-2/FR-5), §5.2 | architect |
| G-2 | `--no-reflect` / Stage 10.5 generation contracts are untested. | medium | §8 (test plan) | qa |
| G-3 | Stale tokens could be re-promoted as operative instructions. | high | §11.1, FR-7 | refactorer |
| G-4 | Reflect-guard command path mismatch (`tests/reflect/` vs `tests/cli/reflect/`). | medium | §11 OQ-1 | qa |
| G-5 | RFMerger P1–P5 vs reflect UC-2 P1–P5 naming collision could cause taxonomy substitution. | medium | Appendix A | analyzer |
| G-6 | 5-vs-7 deliverable-count taxonomy — RESOLVED in §11 OQ-2 (5 GATED deliverables + 2 DERIVED control artifacts + 1 process report); research-file residual WAIVED (refreshed docs authoritative). | low | §11 OQ-2 | scribe |

This refresh resolves G-1, G-3, G-5, and G-6 within its own scope (explicit human decisions recorded 2026-06-19, stale-token
quarantine, taxonomy separation, and the OQ-2 deliverable-taxonomy resolution: 5 GATED deliverables + 2 DERIVED
control artifacts + 1 process report), records G-2 as a test-plan obligation, and carries G-4 (and only the
residual upstream research-file source cleanup of G-6) as open items whose resolution lives in files outside
this spec's edit scope.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| RFMerger | RigorFlow-Merger — the April-2026 investigation that proposed borrowing selected RigorFlow execution-time mechanisms into the SuperClaude `sc:tasklist` generator. |
| Canonical RFMerger P1–P5 | The historical proposal taxonomy (per `design-rfmerger-proposals.md` numbering): P1 Context-Armed Steps, P2 Bounded Patch Loop, P3 DNSP, P4 Evidence-Anchored Validation, P5 Feedback-Driven Tier Calibration. **This is the taxonomy used throughout this spec.** |
| DNSP | Detect-Nudge-Synthesize-Proceed (P3). Canonical name; the task-label gloss "Dynamic / synthetic no-source provenance" refers to the same entry — the canonical name is source-of-truth. |
| **Reflect UC-2 "P1–P5" (QUARANTINED — DO NOT CONFUSE)** | The `sc:reflect` UC-2 protocol independently uses the labels P1–P5 for a *different* taxonomy (P1/P2 per-task verdicts, P3 cross-task interaction scan, P4 report rendering, P5 budget routing). These share only the `P<n>` label with the canonical RFMerger P1–P5 — there is **no semantic correspondence**. Downstream synthesis MUST keep the two strictly separate and MUST NOT reuse reflect's `P<n>` labels for RFMerger proposals. |
| Stage 10.5 (Pre-Reflect Sign-off) | 11th tracked stage of `sc:tasklist`; fans out one `/sc:reflect --mode pre --remediate` per phase file; **advisory for shipping** (PASS/PARTIAL/FAIL all ship); `--remediate` offers remediation without auto-mutating phase files; skipped under `--no-reflect`. |
| `--no-reflect` | Slash-command flag that skips Stage 10.5 (and the templated post-reflect task); auto-set by `--dry-run`; not present on `superclaude tasklist validate`. |
| `sc:task` | Current Stage-9 patch-execution delegate and tier-classification algorithm (`STRICT > EXEMPT > LIGHT > STANDARD`). Replaces the historical `sc:task-unified`. |
| `/task` | The MDTM execution skill loop. MDTM tasklists are executed via `/task <absolute-path>` — NOT `/sc:task`. |
| HISTORICAL-ONLY | A token/claim that exists only in the historical RFMerger package and must never be promoted to current operative guidance; cited as evidence with a current rebase target. |
| Source-of-truth (SoT) | `src/superclaude/...` is canonical; `.claude/{skills,commands,agents,hooks,templates}` is a generated mirror (`make sync-dev` + `make verify-sync`), never an edit/stage target (except `.claude/settings.json`). |
| `gate-results.txt` | P4 runtime artifact: plain-text quality-gate evidence emitted by Stage 6 and injected into Stage 7 prompts. Explicitly **not** `generation-evidence.json` and **not** a new Stage 6.5. |
| `source: "synthetic-dnsp"` | Mandatory provenance marker on every P3-synthesized validation finding. |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `src/superclaude/templates/documents/release-spec-template.md` | Template this spec follows. |
| `.dev/releases/current/v3.8-RigorFlowMerger-tasklist/artifacts/refresh-requirements-ledger.md` | Canonical P1–P5 ledger (Step 2.1) — historical→current rebase per proposal. |
| `.dev/releases/current/v3.8-RigorFlowMerger-tasklist/artifacts/refresh-validation-matrix.md` | Per-output gate contract (Step 2.2) for the refreshed deliverables. |
| `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/phase-outputs/reports/phase-1-discovery-summary.md` | Phase 1 synthesis map (P1–P5, stale-token quarantine, human-decision semantics, OQ-1/OQ-2). |
| `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/phase-outputs/discovery/current-source-contract-inventory.md` | Current `src/superclaude/...` contracts (Step 1.3). |
| `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/research/02-current-tasklist-protocol.md` | 11-stage model, Stage 10.5, `--no-reflect`, `sc:task` naming evidence. |
| `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/research/03-cli-command-surface.md` | `/sc:tasklist` wrapper + `superclaude tasklist validate` CLI surface evidence. |
| Historical (HISTORICAL-ONLY evidence): `FINAL-REPORT.md`, `artifacts/design-rfmerger-proposals.md`, `artifacts/adversarial-validation.md` | Source of the canonical P1–P5 proposals and adversarial revisions; cited as historical evidence only, never as current operative instructions. |
