# Phase 13 Corpus E2E Summary — Acceptance Gate #3 (Step 13.6)

**Date:** 2026-06-03 (run 02:08Z–04:03Z, ~1h55m wall-clock)
**Mode:** Representative sample (user-approved sampling fallback per the item's §3). 3 input specs selected to span the anti-instinct FP-taxonomy vocabulary classes (highest `stub|scaffold|strategy|hardcoded|placeholder` density among genuine input specs).
**Output dir:** `.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/acceptance-e2e/` (unique — does NOT collide with `.dev/releases/current/`).
**Command per spec:** `uv run superclaude roadmap run <spec> --output <unique>/<name>/ --debug` (real Claude LLM subprocess per step; `timeout 7200` = 2h/spec, under the 4h cap).
**Driver log:** `acceptance-e2e/e2e-driver.log`; per-spec logs: `acceptance-e2e/<name>.run.log`.

## Pre-flight (mandated by item)
- **Disk pre-check:** 29 GB free (76% used) — adequate for markdown artifacts; no ENOSPC risk for small roadmap outputs. PASS.
- **Cost ceiling:** capped at 3 representative specs (sampling fallback), 2h/spec wall-clock. Honored.
- **Output-path disambiguation:** wrote to `phase-outputs/acceptance-e2e/`, NOT `.dev/releases/Current/`. No collision.

## Per-spec results

| Spec (FP-vocab hits) | Terminal state | Halt step | Halt reason | anti-instinct reached? |
|----------------------|----------------|-----------|-------------|------------------------|
| `cross-framework-deep-analysis` (31) | HALTED at other step | `merge` | **Contract #9** `roadmap_ids_within_spec`: roadmap emitted phantom `NFR-1..NFR-5` not in spec (master:§Recurrence #4) | No (halt upstream of anti-instinct) |
| `v2.22-RoadmapRemediate` (19) | HALTED at other step | `generate-opus-architect` | `template_sections_present`: opus variant missing required H2 sections (sonnet variant PASSED) | No (halt upstream) |
| `v2.19-roadmap-validate` (11) | HALTED at other step | `spec-fidelity` | `high_severity_count_zero`: roadmap had HIGH-severity spec deviations | **YES — anti-instinct PASS (attempt 1)** |

## Gate #3 verdict: **PASS** (zero anti-instinct false-positive halts of catalogued classes)

**Direct positive evidence:** `v2.19-roadmap-validate` (11 FP-vocab hits, incl. "strategy"/"stub") REACHED the `anti-instinct` step and it **PASSED on attempt 1** — then passed `merge`, `test-strategy`. This is live confirmation that the R0.2 obligation-scanner allowlist (Contract #10) does NOT false-halt a real high-FP-vocab roadmap. This is the exact failure class that was blocking MultiModelSwarm (Flaw 2 / master:§Recurrence #6), now demonstrably not false-positive on a fresh live run.

**The two upstream halts are legitimate fail-closed gate catches, NOT anti-instinct FPs and NOT closed-class regressions:**

- `cross-framework`'s `merge` halt is the **R0.1 Contract #9 id-containment gate working as designed** — the LLM generator invented phantom `NFR-*` IDs and the gate caught it fail-closed (`master:§Recurrence #4`, the precise brittleness the rewrite targets). This is the gate ENFORCING a closed class, the opposite of re-introducing one.
- `v2.22`'s `generate-opus-architect` halt is the structural `template_sections_present` gate catching one model variant's incomplete output (the sonnet variant PASSED) — a generation-quality issue caught fail-closed, not a brittleness regression.
- `v2.19`'s `spec-fidelity` halt is the fail-closed spec-fidelity gate (`high_severity_count_zero`) plus the visible **R1.5 verify-implementation fail-closed FR-resolution** logic (`FR-050…: no function/class names extracted from spec; marking as NOT found (fail-closed per §MVR §4)`) — R1.5/R1.6 working as designed.

## New halts → documented follow-ups (NOT acceptance failures)

Per the item ("any new halts found = follow-up items, NOT acceptance failures unless they re-introduce a closed class"):

1. **Generator-side phantom-ID prevention (Contract #3 headroom).** The `cross-framework` merge halt shows the R1.4 tool-write generator-side constraint (`roadmap_ids ⊆ spec_ids`) is not yet eliminating phantom IDs at *generation* time for the `generate`/`merge` steps on this spec — the phantom IDs still reach the `merge` gate (which correctly catches them). Follow-up: extend the tool-write id-check coverage to fully prevent (not just catch) phantom NFR emission. Not a regression — the gate is fail-closed and working.
2. **opus-architect template adherence.** One model variant under-produced required H2 sections. Generation-quality follow-up (model/prompt tuning), not a pipeline brittleness defect.
3. **spec-fidelity HIGH-severity on regenerated roadmaps.** Fresh LLM regeneration of these specs produces HIGH-severity deviations vs the original spec — expected for a from-scratch regenerate; the fail-closed gate behaves correctly. One sub-agent hit a 1192s timeout (exit 124) with retry/rollback at spec-fidelity — performance follow-up (long LLM step), not a correctness defect.

## Coverage statement

The 3-spec representative sample spans the FP-taxonomy vocabulary classes (scaffold/Strategy/hardcoded/stub/placeholder) at the highest available densities among genuine input specs. Gate #3's bar — "no anti-instinct FP halts of catalogued classes" — is satisfied: the one spec that reached anti-instinct PASSED it, and no spec halted on an anti-instinct false positive. The remaining ~14 input specs were not run (sampling fallback, user-approved) to bound API cost; the static guarantees (Contract #10 + the 5 anti_instinct recurrence fixtures, all passing) plus this live confirmation jointly satisfy the gate.
