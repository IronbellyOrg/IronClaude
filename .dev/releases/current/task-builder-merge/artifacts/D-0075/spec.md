# D-0075 — T06.09 Spec: Wire within-cycle + cross-cycle dedup behavior (INV-012)

**Task:** T06.09 — Wire within-cycle + cross-cycle dedup composition (R-123 within-cycle collapse; R-124 cross-cycle non-regression composition, INV-012)
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-123 (within-cycle identical-dedup_key collapse to one record with found_n_times incremented), R-124 (cross-cycle identical dedup_key is dedup case NOT regression — contributes 1 not 2 to |F_n+1|; INV-012 composition with PR-02 monotonicity)
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution (grep + structural inspection + cross-reference against T05.07 INV-012 subsection)
**MCP Requirements:** None; Preferred: Sequential
**Date:** 2026-05-18

---

## 1. Goal

Bind explicit per-wrapper enforcement clauses at all four FR-CONV.6 sites (`SKILL.md`, `rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md`) for the **two distinct dedup-collapse rules** that compose the synthetic-dnsp emitter with PR-02 Retry Monotonicity (FR-CONV.5 from M5):

1. **Within-cycle collapse (R-123).** Two synthetic-dnsp findings emitted within the SAME retry cycle for the SAME `(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple MUST collapse to a single record with `found_n_times` incremented by exactly `1` (default `1` → `2`); the emitter MUST NOT emit two cardinality-2 records.
2. **Cross-cycle composition (R-124, INV-012 non-regression).** A synthetic-dnsp finding with an identical `dedup_key` re-emitted on cycle `n+1` AFTER appearing on cycle `n` contributes `1` (not `2`) to `|F_{n+1}|` and MUST NOT trigger a regression halt (its prior verdict was already FAIL, not PASS); persistence trips Step 2 (monotonicity) **if and only if** `|F_{n+1}| >= |F_n|` — the intended halt. The operational rule lives at SKILL.md L1075-1089 (T05.07 INV-012 subsection; sha256 `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`); T06.09 binds the per-wrapper enforcement clause referencing that subsection.

The clause introduces two named rejection symbols scoped to the **cross-emission compositional layer** between the per-emission field-shape gates (DM-003 from T06.03/T06.04/T06.05) and the cohort-level path-selection gate (R-122 from T06.08):

- `INV-012-within-cycle-collapse-violation` — within-cycle identical-dedup_key emissions not collapsed to cardinality 1; `found_n_times` not incremented by exactly `1` per collapse; counter reset or skipped.
- `INV-012-cross-cycle-composition-violation` — cross-cycle same-dedup_key re-emission contributing `2` (instead of `1`) to `|F_{n+1}|`; cross-cycle synthetic-dnsp persistence triggering a regression halt at Step 1; cross-cycle dedup-collapse step omitted before the monotonicity comparison at Step 2.

The two symbols are kept distinct from `DM-003-found-n-times-invariant-violation` (T06.05 — per-emission counter-shape failures at the field level) and `R-122-guard-precedence-violation` (T06.08 — cohort-level path-selection failures) so that operator tooling can grep the symbol to distinguish "the within-cycle counter was wrong" from "the cross-cycle composition was wrong" from "the field shape itself was wrong" from "the cohort path selection was wrong."

## 2. Inputs

| Input | Path | Role |
|---|---|---|
| Existing FR-CONV.6 wrapper bullet (T06.01..T06.08 baseline) | `src/superclaude/agents/rf-analyst.md:70`, `rf-qa.md:78`, `rf-qa-qualitative.md:79`; `SKILL.md` L678-680 (existing all-agents-fail paragraph + R-122 paragraph from T06.08) | Wrapper houses T06.05 within-cycle increment clause + T06.07 API-003-M6 wire-shape + T06.08 R-122 guard precedence; T06.09 appends the INV-012 dedup-composition enforcement clause at the tail. |
| INV-012 operational rule subsection (T05.07 baseline) | `src/superclaude/skills/task-builder/SKILL.md` L1075-1089 | Source-of-truth operational rule for cross-cycle dedup composition — five paragraphs: composition rule, bookkeeping rule, regression-vs-persistence rule, three worked examples, regression non-emission invariant. T06.09's clause references this subsection by line + sha pin. |
| F-set definition + 4-step ordering rule (T05.02 + T05.05 baselines) | `src/superclaude/skills/task-builder/SKILL.md` L1042-1048 (F-set definition with dedup-key identity); L1050-1059 (4-step rule: Step 1 regression → Step 2 monotonicity → Step 3 hard-cap → Step 4 proceed) | Anchors the cross-cycle composition contract: Step 1 predicate uses dedup-key identity; Step 2 monotonicity comparison runs AFTER the dedup-collapse step. |
| Existing inline "Dedup key" paragraph in wrapper (T06.01 baseline) | `src/superclaude/skills/task-builder/SKILL.md` L682 | One-sentence statement that repeated synthetics for the same dedup key collapse into one finding with `found_n_times` incremented; T06.09's clause expands this into formal within-cycle vs. cross-cycle scoping with explicit named rejection symbols. |
| DM-003 contract (T06.02 baseline) + found_n_times default + within-cycle increment (T06.05 baseline) | `src/superclaude/skills/task-builder/SKILL.md` L666 + L672 (R-117/R-118/R-119 paragraph) | Establishes the `found_n_times: 1` default and the `+1`-on-within-cycle-collapse increment that T06.09's within-cycle clause operationalizes. |
| Roadmap item R-123 | `.dev/releases/current/task-builder-merge/roadmap.md` | "Within-cycle identical-dedup_key collapse to one record with found_n_times incremented." |
| Roadmap item R-124 | `.dev/releases/current/task-builder-merge/roadmap.md` | "Cross-cycle identical dedup_key is dedup case NOT regression — prior verdict was already FAIL; contributes 1 (not 2) to F_n+1; persistence trips monotonicity (intended), not regression." |
| T05.07 evidence (immediate predecessor for INV-012) | `.dev/releases/current/task-builder-merge/artifacts/D-0059/spec.md` + `D-0059/evidence.md` + `D-0059/fixture-cross-cycle-dedup-shrinking.log` + `D-0059/fixture-cross-cycle-dedup-non-shrink.log` | Ratifies the cross-cycle composition rule at SKILL.md L1075-1089 with two synthetic execution-log fixtures (shrinking + non-shrinking) and sub-agent quality-engineer PASS verdict. |
| T06.08 closure (R-122 predecessor) | `.dev/releases/current/task-builder-merge/artifacts/D-0074/evidence.md` | Provides the immediate-prior wrapper anchor — T06.09 appends after the R-122 clause at all 4 sites. |

## 3. INV-012 dedup composition clause (R-123 + R-124 — per-wrapper operational rule)

Append immediately after the T06.08 R-122 all-agents-fail guard precedence clause at the four wrapper sites:

> **Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124).** The synthetic-dnsp emitter MUST apply two distinct dedup-collapse rules at orthogonal scopes that together compose with PR-02 Retry Monotonicity (FR-CONV.5 / M5) per the operational rule subsection at `src/superclaude/skills/task-builder/SKILL.md` L1075-1089 (T05.07 INV-012 cross-cycle dedup composition; subsection sha256 pinned at `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`). **Within-cycle collapse (R-123).** Two synthetic-dnsp findings emitted within the SAME retry cycle for the SAME `(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple MUST collapse to a single record with `found_n_times` incremented by exactly `1` from its current value (default `1` on first emission → `2` after the first within-cycle collision → `3` after the second, etc.); the emitter MUST NOT emit two cardinality-2 records and MUST NOT skip the increment. The collapse happens BEFORE the merge step picks up the synthetic block at SKILL.md §A.8 / §A.10, so the merge step sees a cardinality-1 emission already annotated with the correct `found_n_times`. **Cross-cycle composition (R-124, INV-012 non-regression).** A synthetic-dnsp finding with an identical `dedup_key` re-emitted on cycle `n+1` AFTER appearing on cycle `n` is a DEDUP case, NOT a regression — its prior-cycle verdict was already FAIL, not PASS — and it contributes `1` (not `2`) to `|F_{n+1}|` (the failure-set cardinality after the cycle-`n+1` fix attempt, per SKILL.md L1062 — `|F_n|` is computed AFTER dedup-key deduplication; the same identity is used at cycle `n+1`). The cross-cycle collapse runs BEFORE the PR-02 monotonicity comparison `|F_{n+1}| >= |F_n|` at Step 2 of the 4-step ordering rule (SKILL.md L1055). The cross-cycle synthetic-dnsp persistence MUST NOT trip Step 1 (regression detection at SKILL.md L1054) because `dedup_key ∈ FAIL_n` implies `dedup_key ∉ PASS_n`, so the Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is FALSE by construction; persistence trips Step 2 (monotonicity) **if and only if** `|F_{n+1}| >= |F_n|` after the dedup-collapse step — the intended halt when the partition agent is stuck. Violations of the within-cycle collapse rule (e.g., two identical-dedup_key records emitted with cardinality 2 instead of 1 with `found_n_times: 2`; `found_n_times` not incremented by exactly `1` per collapse; counter reset or skipped) surface as `INV-012-within-cycle-collapse-violation` errors. Violations of the cross-cycle composition rule (e.g., a cross-cycle same-dedup_key re-emission contributing `2` instead of `1` to `|F_{n+1}|`; the cross-cycle synthetic-dnsp persistence triggering a regression halt at Step 1; the cross-cycle dedup-collapse step omitted before the monotonicity comparison at Step 2) surface as `INV-012-cross-cycle-composition-violation` errors. Both symbols are distinct from `DM-003-found-n-times-invariant-violation` (T06.05 — per-emission counter-shape failures at the field level), `R-122-guard-precedence-violation` (T06.08 — cohort-level path-selection failures), and `API-003-exhaust-point-vocabulary-violation` (T06.07 — per-emission wire-shape failures), because the dedup-composition gate is the cross-emission compositional layer between the per-emission field-shape gates and the cohort-level path-selection gate. Both rejections MUST NOT be silently coerced.

SKILL.md additionally carries a rationale tail explaining why two distinct compositional-layer symbols are required (the field-shape gate at DM-003-found-n-times cannot detect cross-emission compositional failures, and the cohort-level guard at R-122 cannot detect per-emission compositional failures); the three agent sites carry the rule + symbol naming without the rationale tail (matching the T06.07 / T06.08 wrapper density convention).

## 4. SKILL.md edit — new paragraph between R-122 and existing "Dedup key" paragraph

Insert one new paragraph at SKILL.md immediately after the R-122 paragraph (currently L680) and before the existing one-sentence "**Dedup key (composition with PR-02 Retry Monotonicity, INV-012).** Two synthetic findings emitted across consecutive retry cycles..." paragraph (currently L682). The existing L682 paragraph is preserved verbatim (T06.09 augments rather than replaces it — the L682 paragraph is the informal anchor; T06.09's new paragraph is the formal operational rule + named rejection symbols).

The new paragraph has the same text as §3 above, with an additional rationale tail:

> Rationale: a within-cycle collapse rule pinned at the per-emission boundary prevents double-counting at the cohort-level merge step (a within-cycle re-emission that bypassed collapse would inflate `|F_n|` and trigger a spurious monotonicity halt at the cycle-`n+1` comparison even when the partition agent is making progress on other items); a cross-cycle composition rule pinned at the F-set construction boundary makes the dedup-identity scope explicit across cycle boundaries (without this binding, an operator could read the L682 inline "Repeated synthetics for the same dedup key collapse" line as referring to within-cycle only, leaving the cross-cycle case ambiguous between dedup and regression and risking a spurious regression halt at Step 1); two distinct named rejection symbols at the compositional layer let operator tooling grep-distinguish within-cycle counter failures from cross-cycle composition failures (a single conflated symbol would force operators to read the full execution log to determine which collapse rule was violated).

## 5. Agent file edits — append to wrapper bullet tail at all 3 sites

The three agent files (`rf-analyst.md:70`, `rf-qa.md:78`, `rf-qa-qualitative.md:79`) each carry a single long bullet that has been progressively extended by T06.03 → T06.04 → T06.05 → T06.07 → T06.08. T06.09 appends one final clause at the tail of each bullet with the same §3 clause text (without the SKILL.md-only rationale tail, matching the T06.07 / T06.08 wrapper density convention).

## 6. Acceptance Criteria

| AC | Description |
|---|---|
| AC1 | `Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124)` clause anchor present at all 4 wrapper sites (1/1/1/1 = 100%) |
| AC2 | Two named rejection symbols `INV-012-within-cycle-collapse-violation` and `INV-012-cross-cycle-composition-violation` each present at all 4 wrapper sites |
| AC3 | The byte-exact phrase `contributes `1` (not `2`) to `\|F_{n+1}\|`` present at all 4 wrapper sites (the R-124 core invariant — matches the T05.07 SKILL.md L1079 verbatim source for cross-cycle composition) |
| AC4 | The phrase `found_n_times` incremented by exactly `1` (or equivalent within-cycle collapse rule) present at all 4 wrapper sites (the R-123 core invariant) |
| AC5 | Cross-reference to SKILL.md L1075-1089 + INV-012 subsection sha256 `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` present at all 4 wrapper sites |
| AC6 | Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` named at all 4 wrapper sites (the regression-non-emission invariant binding) |
| AC7 | `rf-team-lead.md:417` byte-stable post-T06.09 (sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`); whole-file rf-team-lead.md sha256 unchanged (`874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`) — COMP-006-M6 preservation gate |
| AC8 | INV-012 subsection at SKILL.md L1075-1089 byte-stable post-T06.09 (sha256 = `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`); T06.09 references but does not modify it |
| AC9 | Strict additivity — no prior named rejection symbol (DM-003-fixed-field, DM-003-dynamic-field, DM-003-recommendation, DM-003-dedup-key-shape, DM-003-found-n-times, API-003-exhaust-point-vocabulary, R-122-guard-precedence), severity/source/recommendation literal anchor, or COMP-006-M6 sha pin literal removed or count-reduced at any wrapper site |
| AC10 | `make sync-dev` clean (no skill/agent diffs after sync); `diff -q src/superclaude/<file> .claude/<file>` returns empty for all 4 wrapper files |
| AC11 | Fixture-level binding (within-cycle TEST-019 collapse fixture; cross-cycle no-regression-halt assertion in TEST-022 cross-cycle dedup fixture from T05.14 / D-0065) deferred to T06.15 (D-0080 — TEST-019 cardinality-1 + found_n_times=2) and reuses T05.14 / D-0065 TEST-022 evidence for the cross-cycle no-regression invariant (no new pytest fixture in T06.09 — same staging as T06.03/T06.04/T06.05/T06.07/T06.08) |
| AC12 | Evidence at `TASKLIST_ROOT/artifacts/D-0075/evidence.md` |

## 7. Validation Plan

- **Manual review:** reviewer confirms the new T06.09 clause references the existing T05.07 INV-012 subsection at SKILL.md L1075-1089 by line number + sha256 pin; reviewer confirms the two new named rejection symbols are distinct from the five DM-003 symbols + API-003 symbol + R-122 symbol.
- **Grep evidence:** byte-exact clause anchor + two new symbols + R-124 core invariant phrase + R-123 within-cycle increment phrase + SKILL.md L1075 cross-reference + Step 1 predicate present at all 4 wrapper sites.
- **Preservation gate:** rf-team-lead.md:417 sha256 unchanged (COMP-006-M6); INV-012 subsection at SKILL.md L1075-1089 sha256 unchanged (T05.07 byte-stability invariant).
- **Sync parity:** `make sync-dev` ran clean for all 4 wrapper files; `diff -q src/superclaude/<file> .claude/<file>` returns empty.
- **Cross-cycle fixture binding:** TEST-022 fixture (T05.14 / D-0065) already pins `grep -c "Regression detected on Item" <execution-log> == 0` for cross-cycle same-dedup_key transitions; T06.09's clause is the per-wrapper enforcement binding that the existing fixture programmatically ratifies.
- **Within-cycle fixture binding:** TEST-019 fixture (T06.15 / D-0080) will be the positive-path verifier for the within-cycle cardinality-1 + found_n_times=2 invariant; T06.09's clause is the per-wrapper enforcement binding that the future fixture will programmatically bind to.

## 8. Dependencies and Provenance

- **Upstream dependencies (Phase 6):** T06.08 (D-0074) PASS — R-122 all-agents-fail guard precedence landed at 4/4 wrapper sites with `R-122-guard-precedence-violation` named symbol; T06.08 establishes the immediate-prior wrapper anchor after which T06.09 appends.
- **Upstream dependencies (Phase 5 cross-binding):** T05.07 (D-0059) PASS — INV-012 cross-cycle dedup composition operational rule landed at SKILL.md L1075-1089 with two synthetic execution-log fixtures and sub-agent quality-engineer PASS verdict; T06.09 references this subsection by line + sha pin.
- **Roadmap references:** R-123 (within-cycle identical-dedup_key collapse to one record with found_n_times incremented); R-124 (cross-cycle identical dedup_key is dedup case NOT regression — prior verdict was already FAIL; contributes 1 not 2 to F_n+1; persistence trips monotonicity intended, not regression; INV-012 composition with PR-02 monotonicity).
- **Downstream consumers:** T06.10 (D-0076 — INV-021 N-1 concurrency + HIGH severity non-overridable; composes with T06.09 because synthetic emits ALONGSIDE real findings under R-122 Path B AND within-cycle collapses to cardinality 1); T06.11 (D-0077 — SKILL.md A.8/A.10 merge step; consumes the within-cycle-already-collapsed cardinality-1 emission); T06.12 mid-phase checkpoint (D-CP06-MID-T07-T11 — gates T06.07..T06.11 collectively); T06.15 (D-0080 — TEST-019 within-cycle cardinality + found_n_times collapse fixture; programmatic positive-path verifier for AC4); T05.14 (D-0065 — TEST-022 cross-cycle dedup fixture; already-landed programmatic verifier for AC6 cross-cycle no-regression invariant); T06.18 End-of-Phase-6 checkpoint (D-CP06 — gates T06.01..T06.17 collectively for MIG-006 single-commit landing at T06.17 / D-0082).

## 9. Rollback

Per roadmap R-123 + R-124 rollback note: the T06.09 clause is a per-wrapper enforcement binding at the cross-emission compositional layer. Rollback aligns with the FR-CONV.6 wrapper rollback policy (T06.01 / D-0068): the clause can be removed by reverting the appended paragraph at the four wrapper sites without modifying the existing T05.07 INV-012 subsection at SKILL.md L1075-1089 (which remains the source-of-truth operational rule). The existing inline "**Dedup key (composition with PR-02 Retry Monotonicity, INV-012).**" paragraph at SKILL.md L682 (T06.01 baseline) is unchanged by T06.09, so on rollback the textual INV-012 composition note remains in place. The 3-cycle hard cap at `rf-team-lead.md:417` and the per-gate counter table at `rf-task-builder.md:354-364` continue to govern fix-cycle escalation.

## 10. Slice hashes (for downstream task verification)

| Slice | sha256 (pre-edit baseline = post-T06.08) |
|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` (whole file, pre-edit) | `7deb5090a04b063a240054f884851709bd17053d69bc59a86039af46ac9c9dfb` |
| `src/superclaude/agents/rf-analyst.md` (whole file, pre-edit) | `932701df6ff1a43d20730376b15281bddccf61d3795853d1465973765cd2b81a` |
| `src/superclaude/agents/rf-qa.md` (whole file, pre-edit) | `788d76686dfdfafe080d8f6a062dfe66c31d6d66a5551f98ad3a3c4118a1a521` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file, pre-edit) | `73eeec6db1141bc38aebfba2a7d18696b162c4bafbd07e1f9bf93de23cf365e9` |
| `src/superclaude/agents/rf-team-lead.md:417` (COMP-006-M6 preservation gate — byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — preservation gate) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |
| `src/superclaude/skills/task-builder/SKILL.md` L1075-1089 (T05.07 INV-012 operational rule subsection — referenced by T06.09; byte-stable invariant) | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` |

Post-edit hashes recorded in `evidence.md` §8.
