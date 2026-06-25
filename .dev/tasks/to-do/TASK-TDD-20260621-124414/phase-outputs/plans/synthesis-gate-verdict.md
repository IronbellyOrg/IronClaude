# Synthesis Gate Verdict — FR-DRS TDD

**Task:** TASK-TDD-20260621-124414
**Feature:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep
**Phase:** 5G synthesis gate — fix cycle 1
**Date:** 2026-06-21
**Fix authorization:** TRUE (surgical in-place Edits)
**Source findings:** `qa/qa-synthesis-gate-consolidated-findings.md` (consolidated verdict FAIL → fix cycle 1)

Applied the six synth-fix issues S-1..S-6 to the synthesis files. Each fix was verified against the
cited research source-of-truth before editing (research/00, 02, 03, 04 + `cli/reflect/models.py`).
All edits were surgical (Read-then-Edit; no wholesale rewrites). The four A-1..A-4 items are
ASSEMBLER-handoff and were **NOT** touched.

---

## Fixes Applied

### S-1 (HIGH) — Eval-case tables split from 4 collapsed rows → 5 distinct rows

Source of truth: `research/04-eval-path-integration.md` §3 (case-by-case, ids 37–41 are five
distinct `case_dir`-backed fixtures) and §summary.

- **synth-01 §4.1** ("Per-case deterministic expectations" table):
  - Before: 4 rows — `unwired / test-only` collapsed into one row; no id column.
  - After: 5 rows with an Id column — 37 `uc2-unwired-surface-passes` (FAIL-pre/PASS-post, unreached ≥ 1
    + regression 1, never clean-pass), 38 `uc2-surface-positive-control` (reachable; unreached 0,
    degraded false, no UNREACHED/STOP), 39 `uc2-surface-dynamic-dispatch` (`[project.scripts]` →
    degraded true, regression 0, DEGRADE never UNREACHED), 40 `uc2-surface-degraded-backend`
    (`backend: none` → Grounding Gap + degraded true, no hard-STOP, no clean-pass), 41
    `uc2-surface-test-only-ref` (test/comment-only → UNREACHED; hosts the count-invariant assertion).
- **synth-02 (FR-008 AC-2 row):**
  - Before: AC prose collapsed "unwired/test-only → UNREACHED + count invariant" as one case (4 effective cases).
  - After: AC enumerates all 5 distinct named cases (37–41) with their per-case deterministic
    expectations; case 41 explicitly identified as the count-invariant host.
- **synth-05 §11.2** (eval-path success-criteria table):
  - Before: 4 rows — `unwired / test-only-ref` collapsed; no id column.
  - After: 5 rows with an Id column, same five distinct fixtures as synth-01, case 41 marked as the
    `len(unreached_surfaces) == runtime_surface_unreached` count-invariant host.

### S-2 (HIGH) — synth-01 §2.2 over-attribution corrected (observed names ≠ SKILL forbid-list)

Source of truth: `research/00-prd-extraction.md` §3 lines 45–49 (the THREE LLM-emitted ad-hoc names)
and `research/03-consumer-surfaces.md` §1.1 line 45 (the SKILL's separate explicit forbid-list).

- §1 Executive Summary: before "improvised scalar names (e.g. `runtime_surface_reachable`,
  `surface_reachability_verdict`) that persisted even after the prose was strengthened to forbid
  **exactly those names**" → after lists the observed set of three names and says the prose was
  strengthened "to forbid improvised names" (dropped the false "exactly those names" claim).
- §2.2 symptom-table row: before stated the ad-hoc names were emitted "all after the prose was
  strengthened to forbid them" (conflation) → after explicitly separates the **observed** emitted set
  (`runtime_surface_reachable`, `surface_reachability_verdict`, `surface_production_reachable`,
  research/00 §3) from the **SKILL's explicit forbid-list** (`runtime_surface_reachable`,
  `reachability_path`, `static_caller_absent_is_expected`, research/03 §1.1), noting the two lists
  overlap only on `runtime_surface_reachable` and that the persistence is structural.

### S-3 (IMPORTANT) — FR-006 split: §5.3 read in-scope, sprint-executor read DEFERRED

Source of truth: `research/03-consumer-surfaces.md` §5.2/§5.3 (`cli/sprint/executor.py` reads no reflect
contract today; imports `TurnLedger` for budget only).

- **synth-02 (FR-006):** before one Must-Have row claiming both the §5.3 pre-filter AND the sprint
  executor "MUST consume the deterministically-written scalars" → after **FR-006** = §5.3 forbid-STOP
  pre-filter read only (Must-Have, executes in-skill today) + new **FR-006a** = sprint-executor read
  marked "Deferred (Non-Goal v1) — net-new integration, no rollout phase wires it, SPEC-ONLY."
  Also updated the FR-count line (13 → 14, with FR-006a as Deferred) and the AC-4 coverage-map row.
- **synth-03 §6.3** (System Boundaries, downstream-consumers row): before "the sprint executor … is a
  spec-only consumer today (not yet wired). The sweep merge-overwrites … before any of these consumers
  read" (the trailing clause implied the executor reads) → after splits **in-scope live readers**
  (`parse_contract`/`derive_verdict` + §5.3 pre-filter) from the **deferred SPEC-ONLY consumer** (sprint
  executor reads no contract today, NOT a live reader, NOT wired by this rollout = FR-006a).
- **synth-09 §23 Phase 2 exit criterion:** before "§5.3 pre-filter + `sprint run` executor read the
  deterministic scalars (AC-4)" → after the §5.3 pre-filter read is the exit criterion; the sprint
  executor read is explicitly NOT an exit criterion (reads no contract today, deferred FR-006a).

### S-4 (MEDIUM) — synth-05 §11.1 dangling "see §6" exit-code cross-ref self-contained

Source of truth: `src/superclaude/cli/reflect/models.py:39-42` (`Verdict.exit_code`:
pass→0, halted→10, degraded→11, blocked→2) + research/03. Confirmed synth-03 §6 does NOT define this mapping.

- §11.1 step 8: before "exit code (`pass=0 / halted=10 / degraded=11 / blocked=2`)" with no source →
  after cites `Verdict.exit_code`, `models.py:39-42` (research/03) inline.
- "Cross-references for the assembler" block: before "owned by §6 Architecture /
  `models.Verdict.exit_code`" (dangling — §6 never defines it) → after "owned by the existing reflect
  `Verdict` enum — `Verdict.exit_code` at `models.py:39-42` (research/03); FR-DRS does not change it."

### S-5 (MEDIUM) — synth-03 §6.2 mermaid symbol label corrected

Source of truth: `research/02-product-path-integration.md` line 63 (`commands.py:254` =
`ReflectRunner(config).run()`); lines 56–57 (`reflect_group` is the Click group callback / command, a
different symbol). `_audit_once` is the actual chokepoint.

- §6.2 mermaid CMD node: before `reflect_group.run() — commands.py:254` (wrong symbol) → after
  `ReflectRunner(config).run() — commands.py:254 (the only product seam; _audit_once is the chokepoint)`.

### S-6 (MINOR) — orchestrator entry function standardized to `run_sweep`

Source: spec/finding directive to use one name. Grep of the synthesis dir found `run_sweep` already used
in synth-05 (5 occurrences) and `run_runtime_surface_sweep` only in synth-04 line 126.

- **synth-04 §8.1:** before "a single orchestrator (`run_runtime_surface_sweep`)" → after
  "a single orchestrator (`run_sweep`)". Post-edit grep confirms zero remaining
  `run_runtime_surface_sweep` across all synth files; `run_sweep` is now uniform.

---

## Verification (post-edit grep sweep)

- S-6: `grep run_runtime_surface_sweep *.md` → 0 matches (standardized to `run_sweep`).
- S-1: synth-01 §4.1, synth-02 FR-008, synth-05 §11.2 each enumerate the 5 distinct `uc2-*` case ids 37–41.
- S-5: `grep "reflect_group.run() — commands.py:254"` → 0 matches (corrected to `ReflectRunner(config).run()`).
- S-3: FR-006a present; FR count line = 14; AC-4 coverage row references FR-006a as deferred.
- S-4: `grep "owned by §6 Architecture"` → 0 matches (exit-code mapping self-contained to models.py:39-42).
- S-2: observed-vs-forbidden separation present in synth-01 §2.2 (cites research/03 §1.1).

---

## Assembler-handoff items (A-1..A-4) — NOT touched in this fix cycle

Per the consolidated findings these are Phase 6 (assembly) responsibilities, not synth-file fixes.
They were deliberately left untouched and are carried forward to the rf-assembler:

- **A-1** — §27 References and §28 Glossary are not produced in any synth file; the assembler MUST populate them.
- **A-2** — synth-02's author-introduced `§5.3 PRD Trace` heading collides numerically with the SKILL's
  separate `§5.3 pre-filter`; re-letter/relabel on assembly.
- **A-3** — the stale `ensemble.REFLECT_CONTRACT_VERSION="1.0"` vs SKILL 1.6.0 reconciliation
  (already surfaced in synth-04 §8.3 / synth-02 G3 / synth-08 §19.2) must land in assembled §19 + §22.
- **A-4** — add a one-line bridge at first co-occurrence of "7-step algorithm" vs "6 logical units"
  (the 7 steps map to 6 units).

---

## Verdict

All six synth-fix issues (S-1 HIGH, S-2 HIGH, S-3 IMPORTANT, S-4 MEDIUM, S-5 MEDIUM, S-6 MINOR) were
applied surgically and verified against research source-of-truth. No fabrication, no new contradictions
introduced; FR-count and AC-coverage internal-consistency fields were updated to match the FR-006 split.
A-1..A-4 remain carried to the assembler (untouched).

SYNTHESIS GATE: CLEARED (fix cycle 1)

---

## Fix Cycle 2

**Phase:** 5G synthesis gate — fix cycle 2
**Date:** 2026-06-21
**Fix authorization:** TRUE (surgical in-place Edits)
**Driver:** Fix cycle 1's S-3 applied the FR-006 split (§5.3 read in-scope Must-Have; sprint-executor
read DEFERRED as FR-006a) at the FR-table / §6.3 boundary / §23 Phase-2-exit, but left three+ parallel
**AC-4-verbatim** spots still claiming the sprint executor reads the deterministic scalars TODAY —
an intra-document contradiction against §23 Phase-2 exit (synth-09 line 161) and the FR-006a deferral.
Cycle 2 propagates the split to every residual present-tense executor-read claim.

### R1 (IMPORTANT) — synth-09 §24.1 Definition-of-Done AC-4 entry

Source of truth: synth-09 §23 Phase-2 exit (line 161, defers the executor read);
`research/03 §5.2/§5.3` (`cli/sprint/executor.py` reads no reflect contract today).

- **synth-09 §24.1 (AC-4 DoD entry, ~line 193):**
  - Before: "**AC-4** — The §5.3 forbid-STOP pre-filter and the `sprint run` executor read the
    deterministic scalars." (directly contradicted §23 Phase-2 exit, which defers the executor read).
  - After: "**AC-4 (v1 in-scope portion)** — The §5.3 forbid-STOP pre-filter reads the deterministic
    scalars." + explicit note that the `sprint run` executor read is **DEFERRED to FR-006a** (net-new,
    NOT a v1 Definition-of-Done criterion; nothing to wire this rollout), cross-referencing §23 and
    synth-02 FR-006a.

### R2 (MINOR) — synth-01 §3 Goal G4 + §4 success-metric

Source of truth: same FR-006a deferral (`research/03 §5.2/§5.3`).

- **synth-01 §3.1 Goal G4 (line 104):**
  - Before: "Wire the deterministic values into the consumers | The §5.3 forbid-STOP pre-filter and the
    `sprint run` executor read the deterministic scalars, not LLM-typed ones (AC-4)".
  - After: "Wire the deterministic values into the in-scope consumer | The §5.3 forbid-STOP pre-filter
    reads the deterministic scalars … (AC-4, v1 in-scope portion)" + sprint-executor read marked
    **deferred to FR-006a** (reads no reflect contract today, net-new, out of v1 scope).
- **synth-01 §4.1 success-metric "Consumer wiring" row (line 144):**
  - Before: target "**§5.3 forbid-STOP pre-filter and `sprint run` executor read the deterministic
    scalars** (AC-4)".
  - After: target "**§5.3 forbid-STOP pre-filter reads the deterministic scalars** (AC-4, v1 in-scope
    portion; sprint-executor read **deferred to FR-006a**)"; measurement narrowed to tracing the §5.3
    pre-filter read alone.

### R3 (MINOR) — synth-05 §11.1 residual present-tense executor-read

Source of truth: same FR-006a deferral; consistent with §11.1 step 6 already marking the executor "(spec)".

- **synth-05 §11.1 "Success Criteria" bullet (line 80):**
  - Before: "§5.3 pre-filter and sprint executor read the deterministic scalars (AC-4)."
  - After: "§5.3 pre-filter reads the deterministic scalars (AC-4, v1 in-scope portion)." + sprint-executor
    read marked **deferred to FR-006a / SPEC-ONLY** (reads no reflect contract today; cross-refs step 6).
- **synth-05 §11.1 mermaid `Con` participant label (line 43):** the diagram consumer node label
  `sprint executor` was qualified to `sprint executor [deferred/FR-006a]` so the diagram itself carries
  no unqualified executor-consumer claim.

### R4 (MINOR) — synth-02 G2 gap-disposition row

Source of truth: synth-02 FR-006a row (line 28); `research/03 §5.2/§5.3, Gap 1`.

- **synth-02 §requirements G2 disposition (~line 75):**
  - Before: forward-looking/unresolved — "TDD must decide if executor wiring is in FR-DRS scope or
    deferred; FR-006 as written assumes the read path exists."
  - After (past-tensed, resolved): "**Resolved:** the sprint-executor read is **deferred as FR-006a**
    (net-new, Non-Goal v1 — see FR-006a row above); **FR-006 covers only the in-scope §5.3 forbid-STOP
    pre-filter read.** AC-4's v1 portion is the pre-filter read alone."

### Additional propagation (surfaced by self-verify, same FR-006 split)

The self-verify grep (below) surfaced five further unqualified present-tense executor-read/consume
claims not enumerated in R1-R4 but identical in kind (the FR-006 split was incomplete at these spots);
all were qualified to deferred/FR-006a for full intra-document consistency:

- **synth-09 §22 "Do nothing" alternative cons (line 46):** "…and the `sprint run` executor consume the
  structured mirror" → "§5.3 pre-filter consumes the structured mirror today" + executor noted as a
  deferred/FR-006a **future** consumer.
- **synth-01 §1 Executive Summary (line 35):** "mirror, consumed by the §5.3 pre-filter and the
  `sprint run` executor, reliable" → "consumed today by the §5.3 pre-filter (and, as a deferred/FR-006a
  future consumer, the `sprint run` executor — which reads no reflect contract today)".
- **synth-01 §2.1 Background (line 53):** the FR-RSR original-intent sentence — "downstream consumers
  (the §5.3 pre-filter and the `sprint run` executor's TurnLedger) read to gate" → narrowed to the §5.3
  pre-filter as the reader, with the executor read explicitly **deferred to FR-006a**.
- **synth-01 §2.2 "What is broken" bullet (line 80):** "consumers that read it (§5.3 pre-filter,
  `sprint run` executor) cannot trust it" → "the consumer that reads it today (§5.3 pre-filter) cannot
  trust it" + executor noted as deferred/FR-006a future consumer.
- **synth-01 §2.2 "Impact" bullet (line 88):** "consumed by the §5.3 pre-filter and the `sprint run`
  executor" → "consumed today by the §5.3 pre-filter (and, as a deferred/FR-006a future consumer, the
  `sprint run` executor)".

### Self-verify (post-edit grep sweep of the whole synthesis dir)

Command (intent): grep all `executor … read|reads|consume|consumes|reader` co-occurrences across
`*.md`, then filter out every line already qualified with
`deferred | FR-006a | SPEC-ONLY | Non-Goal | (spec) | [deferred] | not wired | not delivered |
in-scope portion | reads no reflect contract today | future consumer`.

**Result: ZERO residual unqualified present-tense executor-read/consume/reader claims.** Every surviving
mention of the sprint executor as a scalar consumer is now explicitly marked deferred / FR-006a /
SPEC-ONLY / future-consumer. Spots already-correct from fix cycle 1 (synth-02 FR-006a line 28, synth-04
lines 146/148 "SPEC-ONLY", synth-07 line 130 "SPEC-ONLY today", synth-05 step 6 "(spec)") were confirmed
untouched and consistent.

No fabrication and no new contradiction introduced: every edit qualifies an existing claim to match the
already-ratified FR-006 / FR-006a split; the in-scope deliverable (§5.3 pre-filter read) is preserved
verbatim everywhere. The §23 Phase-2-exit ↔ §24.1 DoD contradiction that motivated R1 is resolved
(both now defer the executor read).

SYNTHESIS GATE: CLEARED (fix cycle 2 — FR-006 split fully propagated)
