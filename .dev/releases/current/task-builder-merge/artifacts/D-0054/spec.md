# D-0054 — FR-CONV.5 Halt-Guards Wrapper Spec

**Task:** T05.01 — Land FR-CONV.5 halt-guards wrapper
**Roadmap items:** R-090
**Date:** 2026-05-17
**Tier:** STRICT
**Verification:** Sub-agent (quality-engineer) — see `evidence.md` §3.

---

## 1. Purpose

Land the FR-CONV.5 (PR-02) halt-guards wrapper paragraph in all three
canonical surfaces so subsequent M5 tasks can implement byte-exact halt
emitters (T05.02–T05.04), document the F-set + 4-step ordering
(T05.05), wire INV-012 cross-cycle dedup composition (T05.07), and
preserve the existing 3-cycle hard cap + per-gate counters (T05.08).

The wrapper is **strictly additive on existing fix-cycle loops**:

- NO new retry loop introduced.
- NO new stage introduced.
- NO counter collapsed; per-gate counters at `rf-task-builder.md:354-360`
  remain byte-identical.
- The 3-cycle hard cap at `rf-team-lead.md:417` remains untouched as
  the fourth-precedence backstop.

## 2. Wrapper Sites (3 surfaces, additive paragraphs only)

| # | File | Wrapper anchor | Halt-message keywords present |
|---|------|----------------|-------------------------------|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | `## Retry Monotonicity Protocol (FR-CONV.5 / PR-02 …)` at L1014 | `[HALT-MONOTONICITY] |F|=<n>` at L1018; `Regression detected on Item X.Y — …` at L1019 |
| 2 | `src/superclaude/agents/rf-task-builder.md` | `**Retry Monotonicity Protocol (FR-CONV.5 / PR-02 — applies to every gate row above):**` at L366 | both halt-message wire strings at L368 |
| 3 | `src/superclaude/agents/rf-qa.md` | `**Retry Monotonicity Protocol (FR-CONV.5 / PR-02 — strengthens this 3-fix-cycle):**` at L337 | `Regression detected on Item X.Y — …` at L341; `[HALT-MONOTONICITY] |F|=<n>` at L342 |

All three wrapper paragraphs cross-reference the SKILL.md protocol as
the canonical full specification.

## 3. Two Halt Guards (wired ON TOP of existing loops)

### 3.1 Monotonicity guard
- **Trigger:** end of cycle `n`; consulted only when `|F_n| > 0` AND
  only after the regression check has passed for the same cycle
  transition.
- **Condition:** `|F_{n+1}| >= |F_n|` — i.e., failure-set cardinality
  did NOT strictly shrink.
- **Action:** HALT and emit the byte-exact halt-message wire string
  `[HALT-MONOTONICITY] |F|=<n>` (formal byte-exact contract per
  API-004 / T05.02; emitter byte-exactness verified in T05.03).
- **Non-trigger:** legitimate slow convergence such as `|F|=5,4`
  (shrink by 1) continues to the existing cap — this is the X-003
  rejection enforcement preserved by T05.08.

### 3.2 Regression guard
- **Trigger:** end of cycle `n`; runs BEFORE the monotonicity check on
  every cycle transition `n → n+1`.
- **Condition:** any item that PASSed at cycle `n` is FAILing at
  cycle `n+1`.
- **Action:** HALT immediately and emit the byte-exact halt-message
  wire string `Regression detected on Item X.Y — previously PASS at
  cycle N, now FAIL. Halt overrides monotonicity check.` (formal
  byte-exact contract per API-004 / T05.02; emitter byte-exactness
  verified in T05.04).
- **Non-trigger:** legitimate refinement of still-FAILing items does
  not trigger; INV-012 cross-cycle synthetic-dnsp dedup case is
  treated as DEDUP not regression (wired in T05.07).

## 4. Precedence Rule — Regression > Monotonicity

All three wrapper paragraphs document the precedence rule:

- Regression detection ALWAYS runs BEFORE the monotonicity check on
  every cycle transition.
- When both conditions would trigger in the same cycle, the regression
  halt-message is emitted and the monotonicity check is NOT consulted
  on the regressed cycle transition.
- The wrapper paragraphs forward-reference the F-set + 4-step
  ordering section (regression → monotonicity → hard-cap → proceed)
  that T05.05 documents in SKILL.md.

## 5. Preservation Invariants Held by T05.01

| # | Invariant | Held by |
|---|-----------|---------|
| I1 | No new retry loop introduced | wrapper text explicitly states "NO new retry loop and NO new stage" on each surface |
| I2 | Per-gate counter table at `rf-task-builder.md:354-360` byte-identical | wrapper edit is OUTSIDE this range (lands at :366-372) |
| I3 | 3-cycle hard cap at `rf-team-lead.md:417` byte-identical | T05.01 makes zero edits to `rf-team-lead.md`; `git diff` empty |
| I4 | `src/` ↔ `.claude/` parity | `make sync-dev` run post-edit; per-file `diff -q` silent |
| I5 | Zero-trust QA invariant | wrapper "strengthens the gate strictly — never loosens it" (rf-qa.md L344) |

## 6. Out-of-Scope for T05.01 (handed off to downstream tasks)

| Downstream task | What it owns |
|---|---|
| T05.02 (D-0055) | API-004-M5 byte-exact halt-message ABI + 4-step ordering rule documentation + F-set definition |
| T05.03 (D-0056) | Monotonicity emitter implementation + `|F|=5,5,5` fixture |
| T05.04 (D-0057) | Regression emitter implementation + PASS@1/FAIL@2 fixture |
| T05.05 (D-0058) | F-set identity (dedup-key) + 4-step precedence rule + INV-012 composition wiring |
| T05.07 (D-0059) | INV-012 cross-cycle dedup composition |
| T05.08 (D-0060) | Byte-diff zero on `rf-team-lead.md:417` + X-003 rejection enforcement |
| T05.09 (D-0061) | COMP-001-M5 SKILL.md A.9 (:867-873) + Behavioral Constraints (:1547-1553) edits |
| T05.10 (D-0062) | COMP-002-M5 rf-task-builder.md I16 table (:334-361) edits |
| T05.11 (D-0063) | COMP-003-M5 rf-qa.md Fix Cycle Protocol Rules (:308-315) MUST-halt promotion |

## 7. Rollback Path

Per roadmap: disable guards individually. Each wrapper paragraph is a
single contiguous additive block in its file; removing the paragraph
restores the pre-FR-CONV.5 behavior (per-gate caps continue to govern).
M5 governance flag `FF_RETRY_MONOTONICITY_GUARDS` (registered at MIG-005
landing per T05.16) reverts at M7 cleanup post K-005 false-halt-rate
audit.

## 8. Pre-Edit Baseline

| Surface | Pre-edit git SHA | Note |
|---|---|---|
| `feat/mig-002-execution-context-header` HEAD | `487e76b` (MIG-004 land FR-CONV.4 axes overlay) | M4 PASS per `CP-P04-END.md` |
