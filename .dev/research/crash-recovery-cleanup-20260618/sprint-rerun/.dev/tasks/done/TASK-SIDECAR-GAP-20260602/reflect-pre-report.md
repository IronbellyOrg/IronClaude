# /sc:reflect --mode pre — UC-1 Pre-Execution Validation

**Skill:** sc-reflect-protocol (UC-1) · **Tier:** 1 (grounded) · **Date:** 2026-06-02
**Spec:** `SPEC.md` (AC-1..AC-5) · **Tasklist:** `TASK-SIDECAR-GAP-20260602.md`
**Verdict:** **PASS** · coverage_pct = 1.0 (5/5 ACs mapped) · 2 LOW non-blocking hardening findings folded into the tasklist.

## Coverage matrix

| AC | Requirement | Tasklist step(s) | Grounding |
|----|-------------|------------------|-----------|
| AC-1 | Write `<bundle>/results/task-results.json` (JSON list, `TaskResult.to_dict()` shape) to `bundle.artifacts_produced[0].parent` | Step 1.1 | `artifacts_produced=produced` (rerun_tasks.py:1406) → `produced[0].parent` ≡ merge's `bundle_dir` (recovery.py:622-628). Match. |
| AC-2 | Canonical `phase-N-result.json` shows reran tasks `pass`, no dup, recovery_history populated | Step 2.1 (unit) + Step 2.2 (E2E-1) | Splice filter recovery.py:638-643 removes affected prior entries, appends sidecar `new_results`; `affected_tasks=list(resolved)` (1405) so no dup. |
| AC-3 | Sidecar present+readable → no `result-json-not-refreshed`, bundle SUCCESS | Step 2.1 | `sidecar_ok=True` path recovery.py:636-643; status SUCCESS when no failures (659-662). |
| AC-4 | R-F3 preserved when sidecar absent/empty | Step 1.1 (`if produced:` guard) + Step 2.1 (no-sidecar assertion) | recovery.py:644-652 preserve+PARTIAL path unchanged (merge not modified). |
| AC-5 | E2E-1 flip; suites green; ruff clean; no regression | Steps 2.2, 2.3, 3.1 | — |

## Correctness checks (grounded)

- **Var scope:** `produced` (1393), `sub_config` + `sub_phase_obj` (defined ≤1382, used at `_rerun_targets_passed(sub_config.phase_result_json(sub_phase_obj), resolved)`), `resolved` — all in scope at the insertion point (after 1397, before 1411). ✓
- **Shape match:** `TaskResult.to_dict()` nests `{"task":{"task_id":...},...}` (models.py:193-194); bundle + canonical result JSONs both written by `_write_phase_result_json` using `to_dict()` → sidecar entries match the canonical shape the splice filter reads (recovery.py:641). ✓
- **Helper availability:** `_atomic_write_text` (rerun_tasks.py:663) and `json` (already imported) available. ✓
- **Blast radius:** only `rerun_tasks.py` + 2 test files; `merge_recovery_bundle`/`recovery.py` untouched (already correct). ✓
- **best_practice_grade:** 5/5 — reuses existing helpers, minimal diff, preserves R-F3, single-file production change.

## Findings (LOW, non-blocking — folded into tasklist)

- **F1 (Risk surface):** merge's `sidecar_ok=True` branch *replaces* the affected tasks' entries with `new_results`. If a sidecar were written but missing a `resolved` task's entry, that task's prior entry would be **dropped without replacement** (data loss). On the real success path the `_rerun_targets_passed` gate (rerun_tasks.py:1381) guarantees the bundle result JSON contains pass entries for every `resolved` task, so the filtered sidecar is complete — but the tasklist must encode this invariant: **only write the sidecar when the filtered list covers all `resolved` IDs; otherwise skip (fall back to R-F3 preserve).** → folded into Step 1.1.
- **F2 (Coverage):** AC-1's "run_rerun_tasks *writes* the sidecar" is only covered transitively via E2E-1's canonical-PASS. Add a **direct** `assert <bundle>/results/task-results.json` exists after the rerun. → folded into Step 2.2.

## Clearance

Tasklist is correct and grounded against the real merge contract; all 5 ACs map; var/file:line references accurate. **Cleared to execute via /sc:task** (Tier 1 — no T2 escalation; single domain, ~12-line fix + 2 test edits). The two LOW findings have been folded into Steps 1.1 and 2.2 to harden the implementation.
