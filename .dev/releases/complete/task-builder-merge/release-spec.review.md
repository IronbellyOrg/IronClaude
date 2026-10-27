---
title: "Spec-Panel Review — Task-Builder Convergence Release Spec"
spec_reviewed: ".dev/releases/current/task-builder-merge/release-spec.md"
spec_version: "1.0.0"
review_mode: critique
focus_areas: [requirements, architecture, correctness]
iterations: 2
format: detailed
panel: [Karl Wiegers, Alistair Cockburn, Michael Nygard, Gregor Hohpe, Eric Evans, Martin Fowler]
invocation_path: degraded-synthesis
invocation_rationale: "/sc:spec-panel skill returned protocol definition only (sub-agent-context limitation). Panel synthesis produced directly per orchestration spec Phase-7."
created: 2026-05-14
---

# Spec-Panel Review — Task-Builder Convergence

## Invocation

Skill `sc:spec-panel` was invoked with arguments
`@.dev/releases/current/task-builder-merge/release-spec.md --mode critique --focus requirements,architecture,correctness --iterations 2 --format detailed`.
The skill returned its full protocol definition (not a populated review). Per Phase-7 orchestration, this review proceeds as a **degraded-synthesis** equivalent, simulating a panel of six experts: Karl Wiegers (requirements engineering), Alistair Cockburn (use-case rigor), Michael Nygard (release engineering / failure modes), Gregor Hohpe (integration architecture), Eric Evans (DDD / invariants), Martin Fowler (refactoring discipline). Two iterations are produced.

---

## Iteration 1 — Structural & Fundamental Issues

### Karl Wiegers — Requirements Engineering Pioneer

#### SP-01 (Wiegers, MEDIUM, FR-CONV.1)
**Finding**: The TB-Add catalogue lists 8 checks with severity-style annotations ("Hard check" / "[ADVISORY]") but the spec does not name a normative requirement statement using "MUST/SHOULD/MAY" inside each TB-Add bullet. Acceptance Criteria recover the normative force, but a reader auditing the catalogue alone cannot tell whether TB-Add-3 ("clarification adjacency") is a SHALL or a SHOULD without re-reading FR-CONV.1's Observable behavior.
**Recommendation**: Prefix each TB-Add bullet with `MUST` or `SHOULD` per IEEE 830 / RFC 2119. Retain "Hard check" / "[ADVISORY]" but anchor them to the modal verb.
**Conflicts-with-G6**: no.

#### SP-02 (Wiegers, LOW, NFR-CONV.4)
**Finding**: NFR-CONV.4 sets a 10% token-ceiling target ("≤1.10 ratio") but does not specify what counts as "equivalent BUILD_REQUEST" or the statistical envelope (median / mean / worst-case). Two equivalent BUILD_REQUESTs could legitimately drift by 5% on noise alone.
**Recommendation**: Define "5 representative BUILD_REQUESTs" by criteria (e.g., one per source-area count: 1 / 2 / 3 / 5 / 8), and require the **median** ratio ≤1.10 with **max** ratio ≤1.25.
**Conflicts-with-G6**: no.

#### SP-03 (Wiegers, MEDIUM, FR-CONV.2)
**Finding**: FR-CONV.2's Observable behavior states "when BUILD_REQUEST is minimal, the block degrades to References-only with WHY/source-area lines explicitly omitted". This is a degradation specification but does not define "minimal" — the threshold that triggers degradation is implicit.
**Recommendation**: Add a precondition row: "minimal" means BUILD_REQUEST lacks ≥2 of {GOAL, WHY, named source-area}. Otherwise the degrade path is observer-dependent.
**Conflicts-with-G6**: no.

#### SP-04 (Wiegers, LOW, §11 Open Items)
**Finding**: OPEN-PR05 asks "When does `.dev/tasks/done/` reach the ≥10-tasks-of-≥3-task_types threshold?" but provides no owner, cadence, or check mechanism. The "resolve at each major release" target is unbounded.
**Recommendation**: Assign the OPEN-PR05 ownership to the next major release's PM / orchestrator persona and add a one-line check ("count distinct task_type values in .dev/tasks/done/TASK-RF-*/frontmatter").
**Conflicts-with-G6**: no.

#### SP-05 (Wiegers, MEDIUM, NFR-CONV.6)
**Finding**: NFR-CONV.6 requires "5-field per-item schema MUST remain operational across all 8 TB-Add checks". But §4.5 Data Models only enumerates three persisted/passed structures (Execution Context, Inherited Verdict, synthetic-dnsp). The 5-field per-item schema is referenced but never reproduced in the spec.
**Recommendation**: Append a fourth data-model block in §4.5: per-item schema `{Description, Context, Acceptance, Confidence, Verification}` with one-line semantics each.
**Conflicts-with-G6**: no.

### Alistair Cockburn — Use Case Rigor

#### SP-06 (Cockburn, MEDIUM, FR-CONV.3)
**Finding**: Acceptance Criterion's Observable behavior conflates "spawn-prompt content" (an internal artifact) with the "primary actor's observable outcome". The primary actor (rf-qa-qualitative) is given a directive, but the **observable outcome** for an external auditor is "the Self-Audit section appears in the output". The spec mixes both.
**Recommendation**: Split FR-CONV.3 Observable into (1) **Internal prompt invariant** — Inherited Structural Verdict block present in spawn prompt; (2) **External output invariant** — Self-Audit section appears in rf-qa-qualitative output. Both are testable; current phrasing creates verification ambiguity.
**Conflicts-with-G6**: no.

#### SP-07 (Cockburn, MEDIUM, FR-CONV.5)
**Finding**: The regression-halt message is specified verbatim ("Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check."). But the **monotonicity-halt** message is given only as `[HALT-MONOTONICITY] |F|=<n>` — partial format, no human-readable explanation field. The two halt paths have inconsistent message rigor.
**Recommendation**: Symmetrize: monotonicity halt should be `[HALT-MONOTONICITY] |F_{n+1}|=<m> >= |F_n|=<n> — no strict shrink between cycles N and N+1.`
**Conflicts-with-G6**: no.

#### SP-08 (Cockburn, HIGH, FR-CONV.6)
**Finding**: The synthetic-dnsp `recommendation` field is hard-coded to "Manual review required — partition agent failed twice". But the use-case (primary actor: human reviewer) doesn't have a clear next step — there's no instruction on **what** to review, **where** the agent's partial output is, or **how** to disposition the finding (accept / re-run / escalate).
**Recommendation**: Expand the recommendation field schema to require three sub-fields: `next_action: <accept-with-justification | re-run-partition | escalate-to-team-lead>`, `review_target: <file:line range OR spawn-log>`, `disposition_owner: <rf-team-lead | task-author>`. Without this, the synthetic finding is a dead-end signal.
**Conflicts-with-G6**: **yes** — challenges PR-03's CASE-B classification by pushing the recommendation contract beyond paradigm-neutral intent-port.

#### SP-09 (Cockburn, LOW, FR-CONV.4)
**Finding**: The five adversarial axes are named but the spec doesn't define what an **axis** **is**. Is it a category of finding? A perspective? A check-type? Without a definition, the `axis` column on the Items Reviewed table risks inconsistent population by different rf-qa-qualitative invocations.
**Recommendation**: Add a one-paragraph "Axis = a category of failure-mode named for adversarial reasoning" definition at the start of FR-CONV.4 Description.
**Conflicts-with-G6**: no.

### Michael Nygard — Release Engineering / Failure Modes

#### SP-10 (Nygard, HIGH, §9 Migration & Rollout)
**Finding**: Rollback plan states "Each FR is revertable via single-PR reversion of its specific edit lines (see §4.2). Rollback granularity: per-FR." But FR-CONV.6 (DNSP synthetic-dnsp) is consumed by FR-CONV.5 (monotonicity composition per INV-012 dedup-key). If FR-CONV.5 is reverted while FR-CONV.6 remains live, the dedup-key composition rule has no consumer — synthetic findings could regression-halt the loop incorrectly.
**Recommendation**: Add to §9 a **rollback dependency matrix**: reverting FR-CONV.5 requires reverting FR-CONV.6's dedup-key emission; reverting FR-CONV.1 (TB-Add catalogue) requires reverting FR-CONV.3 (dynamic enumeration consumer). Per-FR rollback is not actually independent.
**Conflicts-with-G6**: no.

#### SP-11 (Nygard, MEDIUM, NFR-CONV.5)
**Finding**: "No synchronous network calls added; only existing tools (Read, Grep, Glob, Bash) permitted." But the Acceptance Criterion verification methods include `grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md` — grep is fine, but the spec doesn't bound the **wall-clock** of new local checks. TB-Add-4 (DAG cycle detection) on a 50-item track is O(N²) worst-case; on a 500-item edge case it's 4 orders of magnitude slower.
**Recommendation**: Add an NFR-CONV.5.1: "TB-Add-4 DAG check completes in <500ms for tracks ≤50 items; tracks above bound emit ADVISORY skip."
**Conflicts-with-G6**: no.

#### SP-12 (Nygard, HIGH, FR-CONV.6 + K-006)
**Finding**: K-006 ("Synthetic-dnsp findings mask real issues") rates probability=low / impact=low, but the **all-agents-fail guard** is the only protection against degenerate cases — and the spec doesn't define **partial-failure-rate** triggers (e.g., if 5 of 6 partitions emit synthetic-dnsp, that's a systemic failure, not a per-partition flake). Currently each partition silently synthesizes; the team-lead has no aggregate signal.
**Recommendation**: Add to FR-CONV.6 Negative Criterion: "When ≥50% of partitions emit synthetic-dnsp findings in a single A.8 or A.10 gate, the gate MUST escalate to rf-team-lead with severity=CRITICAL rather than collapse via dedup — synthetic-dnsp is a per-partition signal, not a systemic substitute."
**Conflicts-with-G6**: **yes** — extends PR-03's emission contract; PR-03 was CASE-B precisely because it didn't conflict with task-builder behavior, and this recommendation introduces a new aggregate-severity rule not in the original PR-03.

#### SP-13 (Nygard, MEDIUM, K-009)
**Finding**: K-009 ("sync-discipline violated: `.claude/` edited directly") rates probability=low. But the orchestration project ships in a state where `.claude/skills/` is *intentionally* a synced copy of `src/superclaude/skills/`. The "low probability" rating presumes discipline; the only structural guard is the `make verify-sync` invocation, which is human-triggered.
**Recommendation**: Add an automation guard to the test plan: §8.2 should include `test_pre_commit_hook_blocks_unsynced_claude_edits` — pre-commit failure on `.claude/` modification without matching `src/superclaude/` modification.
**Conflicts-with-G6**: no.

#### SP-14 (Nygard, LOW, §11 OPEN-TOKEN)
**Finding**: NFR-CONV.4 token ceiling has no measurement-frequency requirement post-launch. A 10% ceiling could be reached gradually over many BUILD_REQUEST profiles before anyone notices.
**Recommendation**: Add to §11: "Token-cost measurement re-run quarterly or on any FR-CONV.*-touching change."
**Conflicts-with-G6**: no.

### Gregor Hohpe — Integration / Boundary Contracts

#### SP-15 (Hohpe, HIGH, §5.3 Phase Contracts)
**Finding**: The producer-consumer contract between rf-qa and rf-qa-qualitative is specified in YAML, but the **delivery guarantee** is implicit. Is the spawn-prompt block at-most-once (rf-qa-qualitative runs once per cycle, gets one verdict)? At-least-once (cycle re-runs always re-inject)? Exactly-once? The "freshness_rule" says re-inject NEW verdict — but what if rf-qa fails mid-write?
**Recommendation**: Add to §5.3 a `delivery_semantics: at-most-once-per-cycle` field and a `failure_mode: if rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10`.
**Conflicts-with-G6**: no.

#### SP-16 (Hohpe, MEDIUM, §5.3 Phase Contracts)
**Finding**: The `phase_contract` block names producer/consumer but does not version the schema. Future evolution (e.g., adding a sixth adversarial axis in FR-CONV.4) will silently break consumers expecting five axes.
**Recommendation**: Add a `schema_version: "1.0.0"` field on the phase_contract; require rf-qa-qualitative to log a warning if the version is missing or mismatched.
**Conflicts-with-G6**: no.

#### SP-17 (Hohpe, MEDIUM, FR-CONV.6 emission contract)
**Finding**: The synthetic_dnsp_finding YAML is described as "inside agent partition output", but the **transport medium** is unspecified. Is it inside the agent's main spawn return string? A separate file in `.dev/tasks/<task-id>/`? Both? The dedup-key collapse rule depends on a consistent retrieval channel.
**Recommendation**: §4.5 should specify: "synthetic-dnsp findings are emitted in the agent's stdout JSON block under top-level key `findings:`; dedup occurs in the team-lead's merge step BEFORE storage to `.dev/tasks/<task-id>/research/`.
**Conflicts-with-G6**: no.

#### SP-18 (Hohpe, LOW, §4.4 Module Dependency Graph)
**Finding**: The ASCII graph shows one-way arrows but glosses over the back-channel of retry loops ("Retry loops are within-agent, not cross-agent"). True for fix cycles, but **synthetic-dnsp findings emitted by rf-analyst at A.8 are CONSUMED by rf-qa at A.10's monotonicity logic**. That's cross-agent.
**Recommendation**: Add a dashed arrow rf-analyst → rf-qa labeled "synthetic-dnsp findings (FR-CONV.6 → FR-CONV.5 composition)".
**Conflicts-with-G6**: no.

### Eric Evans — Domain Modeling / Invariants

#### SP-19 (Evans, HIGH, FR-CONV.2 + Invariant model)
**Finding**: The five load-bearing invariants are named (self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research) but **never formally defined as ubiquitous-language terms**. "Evidence-bound" is used in three different senses across the spec: (1) file:line citation in per-item Context (FR-CONV.2 / TB-Add-8); (2) synthetic-dnsp's `evidence: <log-path>` field (FR-CONV.6); (3) `advisory itself = evidence` in conflict-register PR-05. Three meanings, one term — that's the textbook DDD anti-pattern.
**Recommendation**: Add a §1.0 (before Problem Statement) "Ubiquitous Language" subsection defining each invariant in one sentence with a single canonical meaning. Then audit every appearance of the term against the canon.
**Conflicts-with-G6**: no.

#### SP-20 (Evans, MEDIUM, FR-CONV.3 + Anti-inflation)
**Finding**: The anti-inflation invariant at rf-qa-qualitative.md:766-775 is treated as a load-bearing concept but is **not** in the five-invariant list (§1.2). If it's load-bearing, it should be the 6th invariant; if not, it shouldn't gate FR-CONV.3's Negative Criterion.
**Recommendation**: Either (a) elevate anti-inflation to the explicit invariant list with its own probe, or (b) re-frame Negative Criterion as a **rule** rather than an invariant ("rule: mechanical re-check skipped; semantic check required"). Mixed status weakens the invariant probe's defensibility.
**Conflicts-with-G6**: no.

#### SP-21 (Evans, MEDIUM, FR-CONV.5 Composition)
**Finding**: INV-012 composition (PR-02 + PR-03) is described in prose: "Synthetic findings COUNT as failures for `|F_n|` monotonicity. BUT a synthetic finding with identical dedup-key across consecutive cycles is a dedup case, NOT a regression." That's two distinct invariants stacked — but only one prose paragraph documents them.
**Recommendation**: Restructure as two named invariants: INV-012a (synthetic findings affect |F_n| count) and INV-012b (dedup-key identical synthetic findings are NOT regressions). Independent invariants get independent probes.
**Conflicts-with-G6**: no.

#### SP-22 (Evans, LOW, Appendix A)
**Finding**: The conflict register's "invariant-protected" column names invariants ("evidence-bound-item", "zero-trust QA") that ARE in the five-invariant list, but the rationale text introduces **additional** invariants ("rule-based selection", "privacy leakage", "per-item evidence binding") not in the five-invariant list. Some are pseudo-invariants, some are real constraints; the spec doesn't distinguish.
**Recommendation**: Audit the rationale column; promote any genuinely load-bearing constraints to the invariant list; demote others to "design constraint" / "rule".
**Conflicts-with-G6**: no.

### Martin Fowler — Refactoring Discipline / Blast Radius

#### SP-23 (Fowler, MEDIUM, §4.2 Modified Files)
**Finding**: §4.2 lists 19 file-line edits across 6 files. But two edits overlap line ranges: `SKILL.md:872-916` (FR-CONV.1 + FR-CONV.6) and `SKILL.md:898-906` (FR-CONV.1 only). The 898-906 range is **inside** the 872-916 range. Without line-precise atomic semantics, two FRs landing in parallel could conflict.
**Recommendation**: Either (a) consolidate the two FR-CONV.1 entries into one (`SKILL.md:872-916` covers both); or (b) explicitly note the inner range belongs to FR-CONV.1 and the outer range mixes both FRs. Per §4.6 sequencing, this is mitigated by serial landing — but the spec should state this explicitly: "Two-FR overlapping edit ranges land serially per §4.6; no parallel-merge tolerance for SKILL.md:872-916."
**Conflicts-with-G6**: no.

#### SP-24 (Fowler, HIGH, FR-CONV.1 TB-Add bulk)
**Finding**: FR-CONV.1 adds **8 new checks** to a previously 9-item checklist — a 89% volume increase in one FR. CB-3 per-check classification is documented, but the FR itself is monolithic. If TB-Add-5 (granularity check) proves problematic in production, the rollback granularity per §9 is "revert TB-Add-5's append line" — but the FR boundary is the full catalogue.
**Recommendation**: Split FR-CONV.1 into 8 sub-FRs (FR-CONV.1a through FR-CONV.1h) each independently revertable, matching the CB-3 per-check claim. Alternatively, accept that the FR boundary is monolithic and document the rollback-per-line in §9 explicitly.
**Conflicts-with-G6**: no.

#### SP-25 (Fowler, MEDIUM, §8.1 Unit Tests)
**Finding**: The 20 unit tests in §8.1 reference test files like `tests/task_builder/test_structural_gate.py`. But the project (per CLAUDE.md) is documentation-first — the test files don't yet exist, and the spec doesn't declare them as deliverables of this release. Tests are listed as validation evidence but the **creation of test files** isn't an FR.
**Recommendation**: Add a meta-FR or §8.0 "Test Infrastructure" section noting which test files are NEW vs. EXTENSIONS and that creating new test directories is part of this release's scope.
**Conflicts-with-G6**: no.

#### SP-26 (Fowler, LOW, §4.6 Implementation Order)
**Finding**: §4.6 sequences six FRs in serial. But §4.5 implementation-order text says FR-CONV.6 "could parallel-land with 5; conventionally last (sync-discipline applies portfolio-wide)". The two sequencing statements aren't reconciled — is parallel landing permitted between FR-CONV.5 and FR-CONV.6, or is the sequence locked?
**Recommendation**: Pick one: either lock the sequence (and remove "could parallel-land" from §4.6) or document a tolerance window ("FR-CONV.5 and FR-CONV.6 may land in either order or in parallel; INV-012 composition test in §8.2 validates either landing path").
**Conflicts-with-G6**: no.

#### SP-27 (Fowler, MEDIUM, §10 Downstream Inputs)
**Finding**: §10 says "Not in this release's scope" for sc:roadmap and sc:tasklist, with the actual downstream consumer being the `prd` skill (Phase 8 of this orchestration). But the spec's frontmatter doesn't carry the `feature_id` / `parent_feature` / `target_release` in a format the `prd` skill is documented to consume. The Phase-8 hand-off is by **convention** in §10, not by **contract** in frontmatter.
**Recommendation**: Verify which frontmatter fields the `prd` skill reads; if any are missing, add them. If the convention is intentional (free-form hand-off), state this explicitly: "frontmatter fields are informative; prd skill consumes §1–§11 body content as PRD source, not frontmatter."
**Conflicts-with-G6**: no.

---

## Iteration 2 — Detail Refinement & Edge Cases

### Karl Wiegers — Detail Refinement

#### SP-28 (Wiegers, LOW, FR-CONV.1 TB-Add-2)
**Finding**: TB-Add-2 emits `[ADVISORY]` and does not block the gate. But what happens if a track has **2 items** (below the ≥3 lower bound)? The ADVISORY fires, but does the gate still pass? The spec implies yes (advisory is non-blocking) — but a 2-item track may indicate a genuinely malformed task. The ADVISORY framing is correct for the upper bound but possibly under-strict for the lower bound.
**Recommendation**: Sub-classify TB-Add-2 into TB-Add-2a (lower-bound: ≥3 items, BLOCK on violation) and TB-Add-2b (upper-bound: ≤40 / ≤50, ADVISORY only). Calibration applies to TB-Add-2b.
**Conflicts-with-G6**: no.

#### SP-29 (Wiegers, MEDIUM, NFR-CONV.3 hidden-input guard)
**Finding**: NFR-CONV.3's test ("synthetic test where `.dev/tasks/done/` contains 10 fixture tasks ... MUST produce byte-identical structural output to a run with empty `.dev/tasks/done/`") validates PR-05's deferral, but the **scope** of "byte-identical" is unspecified. Does it include timestamps? Run-IDs? Random seeds in agent prompts?
**Recommendation**: Define a `normalize_for_diff` operation: strip timestamps, run-IDs, ephemeral-random-prefixes before byte-compare. Otherwise the test fails on noise.
**Conflicts-with-G6**: no.

### Alistair Cockburn — Detail Refinement

#### SP-30 (Cockburn, MEDIUM, FR-CONV.3 INV-019 Self-Audit)
**Finding**: The Self-Audit obligation is "produce Self-Audit listing relied-on PASS items AND ≥1 semantic check where rf-qa PASS is insufficient". But there's no specified format — is it a markdown section? A YAML block? A free-form paragraph? Different rf-qa-qualitative invocations could legitimately produce wildly different Self-Audit shapes.
**Recommendation**: Add to FR-CONV.3 Description a Self-Audit format spec:
```markdown
## Self-Audit
- Relied-on PASS items: [Item 1.1, Item 2.3, ...]
- Semantic checks beyond inherited PASS:
  - [Check description with item reference]: <one-line rationale>
```
**Conflicts-with-G6**: no.

#### SP-31 (Cockburn, LOW, FR-CONV.4 axes order)
**Finding**: The five axes are listed in order (drift / contradictions / omissions / weakened-criteria / invented-content) but the spec doesn't specify whether this **ordering is normative** (axes evaluated in this order) or **enumerative** (axes are an unordered set).
**Recommendation**: State explicitly: "The five-axis list is an unordered set; rf-qa-qualitative MAY evaluate them in any order. The Items Reviewed table's `axis` column populates with one canonical value per row (or `none`)."
**Conflicts-with-G6**: no.

### Michael Nygard — Detail Refinement

#### SP-32 (Nygard, MEDIUM, FR-CONV.5 retry counters)
**Finding**: INV-001 ("four retry counters maintain separate monotonicity history") is named in the Negative Criterion, but the four counters are named in prose (RESEARCH_NEEDED, MALFORMED, research-gate, per-gate) without a clear data-model. If a future fifth counter is added (e.g., for a new gate stage), the spec doesn't tell the implementer whether the count "four" is normative.
**Recommendation**: Add to §4.5 Data Models a `retry_counter_registry` block listing the current four counters and noting "The number of counters is non-normative; new counters added in future releases inherit the same independence rule."
**Conflicts-with-G6**: no.

#### SP-33 (Nygard, HIGH, K-008 INV-018 blast radius)
**Finding**: K-008 ("INV-018 `.dev/tasks/` directory structure changes invalidate all 7 proposals") rates probability=low / impact=high. The mitigation is "Portfolio-wide note; re-integrate". But the spec doesn't define a **stability commitment** for the `.dev/tasks/` layout — there's no version field, no compatibility-range, no deprecation-policy.
**Recommendation**: Add to §9 Migration: "`.dev/tasks/` directory layout is treated as a stable contract for the scope of this release. Future structural changes require either (a) a coordinated re-integration commit, or (b) a versioning mechanism for the layout (TBD)."
**Conflicts-with-G6**: no.

### Gregor Hohpe — Detail Refinement

#### SP-34 (Hohpe, MEDIUM, §5 Interface Contracts)
**Finding**: §5.1 says "No CLI surface changes. Task-builder is invoked via the Skill tool; BUILD_REQUEST.md remains the sole input contract." But BUILD_REQUEST.md's schema is not documented in this spec or referenced — readers must hunt through SKILL.md to find it. For a release spec, that's a missing input-contract reference.
**Recommendation**: Add to §5.1 a one-line reference: "BUILD_REQUEST.md schema canonical source: `src/superclaude/skills/task-builder/SKILL.md` §<section>". If no section exists, this is itself a documentation gap.
**Conflicts-with-G6**: no.

### Eric Evans — Detail Refinement

#### SP-35 (Evans, MEDIUM, FR-CONV.5 Negative Criterion)
**Finding**: The Negative Criterion forbids "no halt-on-slow-convergence threshold (e.g., `F_{n+1} = F_n - 1`) is permitted (X-003 REJECTED)". This is a meta-statement (X-003 was rejected) rather than an invariant on the system. It's saying "don't change your mind" rather than "the system must behave thus".
**Recommendation**: Reframe as a system invariant: "Cycles where |F| strictly shrinks by ≥1 continue without halt." This is a positive invariant statement; the X-003 rejection becomes Appendix E provenance, not a Negative Criterion.
**Conflicts-with-G6**: no.

### Martin Fowler — Detail Refinement

#### SP-36 (Fowler, LOW, §8.3 Manual E2E Tests row 4)
**Finding**: "Audit-after-FR-CONV.3-lands: Run task-builder on first 5 real BUILD_REQUESTs after FR-CONV.3 lands; ... if any audit shows inflation, fail K-003 gate and disable FR-CONV.3." But "disable FR-CONV.3" isn't a single action — per §4.2, FR-CONV.3 spans three file-line ranges. The rollback procedure isn't specified.
**Recommendation**: Replace "disable FR-CONV.3" with "revert the three file-line ranges listed in §4.2 for FR-CONV.3 (SKILL.md:923-1000 + rf-qa-qualitative.md:794 + dynamic-checklist enumeration logic)".
**Conflicts-with-G6**: no.

#### SP-37 (Fowler, MEDIUM, §11 OPEN-X-002 audit cadence)
**Finding**: OPEN-X-002 says "First 5 rf-qa-qualitative runs after FR-CONV.3 lands MUST be audited". But who audits? When? With what artifact? The release-spec doesn't name an owner or output-format for the audit.
**Recommendation**: Add ownership row: "OPEN-X-002 audit owner: rf-task-builder skill author or release reviewer; audit output: `.dev/releases/current/task-builder-merge/state/fr-conv3-audit.md` (rows: run-id / inflation-detected? / evidence-link)."
**Conflicts-with-G6**: no.

#### SP-38 (Fowler, LOW, §12 Gap Analysis)
**Finding**: §12 enumerates 5 gaps (GAP-M-SC-01, GAP-M-SC-13, GAP-M-SC-14, GAP-FR-R3, GAP-FR-R5) but the rationale paragraph reduces them to "two FR gaps tracked" — making the audit incomplete. Specifically: GAP-M-SC-01 (blanket-determinism) is severity=high but the rationale's "REJECTED per CB-5" is a single sentence — too thin for a HIGH-severity gap.
**Recommendation**: Expand the rationale for the three HIGH-severity gaps (M-SC-01, M-SC-13) and the MEDIUM gap (M-SC-14) to ≥2 sentences each, with explicit invariant citations.
**Conflicts-with-G6**: no.

---

## Iteration 2 — Cross-Expert Consensus Highlights

- **Wiegers + Cockburn** converge on the need for tighter Acceptance Criterion phrasing (SP-01, SP-06, SP-07, SP-30).
- **Nygard + Fowler** converge on rollback safety needing explicit dependency mapping (SP-10, SP-26, SP-33, SP-36).
- **Hohpe + Evans** converge on the spec needing more formal contract / invariant language (SP-15, SP-16, SP-19, SP-21).
- **Two HIGH conflicts-with-G6**: SP-08 (Cockburn pushing PR-03 emission-contract beyond paradigm-neutral intent) and SP-12 (Nygard adding partial-failure aggregate-severity to FR-CONV.6) — both targeting FR-CONV.6 and both extending PR-03's CASE-B contract.
- **One HIGH non-conflicting**: SP-10 (Nygard rollback-dependency matrix) — pure additive remediation.

---

## Severity Tally (across both iterations)

| Severity | Iteration 1 | Iteration 2 | Total |
|----------|-------------|-------------|-------|
| HIGH | 6 (SP-08, SP-10, SP-12, SP-15, SP-19, SP-24) | 1 (SP-33) | 7 |
| MEDIUM | 13 | 7 | 20 |
| LOW | 8 | 3 | 11 |
| **Total** | **27** | **11** | **38** |

Conflicts-with-G6: SP-08 (HIGH, FR-CONV.6), SP-12 (HIGH, FR-CONV.6) — **2 findings**. All other 36 findings are non-conflicting refinements.

---

## Recommendations Summary

**Auto-accept (non-conflicting, additive)**: SP-01, SP-02, SP-03, SP-04, SP-05, SP-06, SP-07, SP-09, SP-10, SP-11, SP-13, SP-14, SP-15, SP-16, SP-17, SP-18, SP-19, SP-20, SP-21, SP-22, SP-23, SP-24 (note monolithic vs split — accept as documentation clarification), SP-25, SP-26, SP-27, SP-28, SP-29, SP-30, SP-31, SP-32, SP-33, SP-34, SP-35, SP-36, SP-37, SP-38.

**Five-step process required** (conflicts-with-G6): SP-08, SP-12.
