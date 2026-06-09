---
status: success
tier_reached: 2
confidence: 0.9
escalation_reason: multi_domain
behavior_is_documented: false
test_is_wrong: false
---

# Troubleshoot Report — Sprint Recovery: Stranded Deliverables + Stale Checkpoints

## Header
- **Target:** `superclaude sprint rerun-tasks` merge-back + `superclaude sprint verify-checkpoints --recover`
- **Type:** bug (data integrity) · **Tier reached:** 2 · **Confidence:** 0.90
- **Escalation reason:** multi-domain (two distinct defects + a design fork)
- **SoT correction:** the request named `executor.py` for merge-back. The merge-back logic actually lives in **`src/superclaude/cli/sprint/recovery.py`** (`merge_recovery_bundle`); verify-checkpoints lives in **`commands.py`** (CLI) + **`checkpoints.py`** (logic); orchestration in **`rerun_tasks.py`** (`run_rerun_tasks`). `executor.py` is not the fix site.

## Summary
Both defects are confirmed by direct code reading **and a real on-disk reproduction** in `/config/workspace/TUIBBS-scp`. They share one root cause: a rerun executes in an isolated sub-config with `release_dir=bundle` and `TASKLIST_ROOT=<bundle_dir>`, so every release-anchored output (deliverable trees, the end-of-phase checkpoint) is written **into the bundle**, but `merge_recovery_bundle` only reconciles the three `results/phase-N-*` file families. The TASKLIST_ROOT deliverable trees are never copied to canonical and their absence is never checked, so the merge reports `status: success, failures: []` while real deliverables stay stranded (Defect 1). Separately, the post-merge `verify-checkpoints --recover` only regenerates *missing* report files; it never re-evaluates an existing checkpoint holding a stale FAIL/BLOCKED verdict, so a recovered phase stays un-closeable (Defect 2).

## Documentation Context
No release-doc contracts this surface. Internal "TDD §T5/§T9" comments scoped the merge to `results/` files only. `recover_missing_checkpoints`'s own docstring documents the "regenerate only missing files" behavior — confirming Defect 2 is a design omission, not a regression. Hard constraint: recovered checkpoints are deliberately stamped `UNKNOWN`, never `PASS` (checkpoints.py:436-437) — the fix must honor this. `behavior_is_documented = false`.

## Diagnosis

### Defect 1 — merge-back strands TASKLIST_ROOT deliverables, reports SUCCESS
The rerun runs against a sub-config with `release_dir=bundle` (`rerun_tasks.py:1417-1424`) and a sub-index that pins `TASKLIST_ROOT` to the bundle dir (`rerun_tasks.py:319`). Rerun agents therefore write declared deliverables (`artifacts/<D-ID>/`, `evidence/<TASK>/`, declared relative to TASKLIST_ROOT) **into the bundle root**. The merge's `artifacts_produced` set is built **only** from `<bundle>/results/phase-N-*` files (`rerun_tasks.py:1444-1446`), and `merge_recovery_bundle` copies back only those whose filename matches a canonical `phase-N-task-*-output.txt` / `phase-N-cp*.md` / `-errors.txt` (`recovery.py:452-457`, `:474-479`, `:495-500`). **No step copies the deliverable trees; no step verifies they landed.** `failures` (`recovery.py:431`) never receives an entry for the stranded trees, so `bundle.status = SUCCESS` (`recovery.py:674`) and the audit log records success (`recovery.py:676-687`).

### Defect 2 — verify-checkpoints --recover no-op on stale verdicts
`recover_missing_checkpoints` returns any entry whose `expected_path.is_file()` **unchanged** and `continue`s (`checkpoints.py:248-264`) — it never reads the existing file's frontmatter/verdict. `build_manifest` records only `exists` (`checkpoints.py:167`), no verdict. So an existing checkpoint carrying a stale FAIL/BLOCKED verdict is left untouched. The rerun auto-invokes `verify-checkpoints --recover` after a successful merge (`rerun_tasks.py:1508-1532`), which is a no-op for the stale file → the gated checkpoint stays FAIL/BLOCKED and the phase is un-closeable.

## Evidence (verified file:line + on-disk reproduction)

**Code (read directly):**
- `recovery.py:425` — `results_dir = release_dir / "results"`; merge scopes to `results/` only.
- `recovery.py:452-457, 474-479, 495-500` — copy-back gated on `produced.name == canonical.name` (results files only).
- `recovery.py:431, 674, 676-687` — `failures` init, status flip, audit-log write.
- `rerun_tasks.py:319` — sub-index `| TASKLIST_ROOT | <bundle_dir> |`.
- `rerun_tasks.py:1417-1424` — `sub_config = replace(config, ..., release_dir=bundle, ...)`.
- `rerun_tasks.py:1444-1446` — `produced = sorted(... (bundle / "results").glob("phase-N-*") ...)`.
- `rerun_tasks.py:1484-1485` — `merge_recovery_bundle(recovery, config.index_path, release_dir=config.release_dir)`.
- `rerun_tasks.py:1508-1532` — Step 14 auto-invoke of `verify-checkpoints --recover`.
- `checkpoints.py:248-264` — existence short-circuit (no verdict read).
- `checkpoints.py:436-437` — recovered checkpoints stamped `UNKNOWN`, never PASS (constraint on the fix).
- `summarizer.py:69` — reusable `PASS|FAIL|...|BLOCKED|SKIP` verdict regex.

**On-disk reproduction (`/config/workspace/TUIBBS-scp`, Phase 12 / T12.09):**
- Canonical TASKLIST_ROOT = `config.index_path.parent` = `.dev/releases/current/v1-MVP/tasklists/` (confirmed: `tasklists/tasklist-index.md` exists there).
- Bundle sub-index literally records `TASKLIST_ROOT = .../results/rerun-20260604T174741`.
- Stranded in bundle: `results/rerun-20260604T174741/artifacts/D-0198/{spec,evidence,notes}.md` and `results/rerun-20260604T174741/evidence/T12.09/{7 files}`.
- Audit log: `{"event": "merge_recovery_bundle", "affected_tasks": ["T12.09"], "status": "success", "failures": []}` (2026-06-04T18:07) — while canonical `tasklists/artifacts/D-0198/` carries mtime Jun 5 01:22 (hand-copied a day later).
- **Systemic, not one-off:** same `status: success, failures: []` for phase-13 reruns T13.02, T13.06, T13.17.

## Proposed Fix

### Fix 1 — `merge_recovery_bundle`: relocate + verify TASKLIST_ROOT deliverable trees, fail loudly
Add a new merge step (after Step 3, before the manifest at `recovery.py:502`) that copies the rerun's deliverable trees from the bundle to canonical and verifies they landed:

1. **Anchors (both knowable at merge time):**
   - Canonical TASKLIST_ROOT = `source_index.parent` (proven: `= <release_dir>/tasklists`, matching the Step-14 comment at `rerun_tasks.py:1523-1525` and the on-disk reproduction). Pass it in explicitly or derive from `source_index`.
   - Bundle root = `bundle.artifacts_produced[0].parent.parent` (parent of `<bundle>/results`); guard for empty `artifacts_produced`.
2. **Relocate:** for each deliverable subtree the rerun produced at the bundle root (`artifacts/`, `evidence/`, and `checkpoints/` if present), copy `<bundle_root>/<rel>/**` → `<canonical_tasklist_root>/<rel>/**`. Use the module's atomic tmp+replace discipline (`recovery.py:519-521`). Preserve any clobbered prior canonical file as `.failed-<ts>` (mirror steps 1-3) for forensics.
3. **Verify → fail loud:** after copying, re-stat each expected canonical destination. Cross-check against the affected tasks' declared deliverables via `_declared_deliverables(phase_obj.file, task_id)` (`rerun_tasks.py:954`) — thread the declared list in as a new optional `expected_deliverables` param (defaults to None → today's behavior, keeps merge verb-agnostic). For every declared/produced tree missing or empty in canonical: `failures.append(f"deliverable-not-landed:{task_id}:{rel}")`. This downgrades status to PARTIAL (`recovery.py:674`) and surfaces in the audit log — the "fail loudly" the request asked for.

### Fix 2 — close the stale-checkpoint gap (design fork RESOLVED)
**Recommendation: option B (re-verify), with a constrained-A fallback — reject plain A.**

- **Primary (B):** after a successful merge (`rerun_tasks.py:1487`), if the affected phase declares an end-of-phase checkpoint **task**, include/re-run that checkpoint task through the existing executor so a *fresh, real* PASS/FAIL verdict is produced (identical to the original run), then let Fix 1's copy-back land `CP-P{phase}-END.md` canonically. Log the auto-added checkpoint task explicitly. If it legitimately fails again, that failure must propagate (no false SUCCESS).
- **Fallback (constrained A):** when the checkpoint is a passive verification block with no runnable agent task, add a `--reevaluate-stale` path to `verify-checkpoints`/`recover_missing_checkpoints` that, for a checkpoint whose phase just recovered AND whose tasks now pass, **re-stamps the stale FAIL/BLOCKED to `UNKNOWN`/Auto-Recovered** (never auto-PASS, per `checkpoints.py:436-437`) so the phase is no longer hard-blocked by a pre-recovery verdict and the operator is told to confirm.
- **Why not plain A:** flipping FAIL→PASS from artifact heuristics manufactures a green checkpoint with no verification — it *realizes* the "overwrite a legitimately-failing checkpoint" risk the request flagged.
- **Guards:** gate on the existing `--no-verify-checkpoints` / `checkpoint_gate_mode`; a checkpoint whose gating tasks did NOT recover must keep its FAIL verdict.

### Regression tests (add to existing suites)
- **Test A — Defect 1 (success-but-stranded)** in `tests/sprint/test_recovery.py::TestMergeRecoveryBundle` (extend `_seed_release` / `_full_recovery_manifest` fixtures): build a bundle with `<bundle>/artifacts/D-0711/module.py` + `<bundle>/evidence/T07.11/proof.md`, run `merge_recovery_bundle`, assert **either** both files landed in `<release_dir>/tasklists/{artifacts,evidence}/...` with content preserved AND status SUCCESS, **or** status is PARTIAL with a non-empty `failures` audit entry. The coupling (stranded ⇒ not SUCCESS) is the load-bearing assertion the current code fails.
- **Test B — Defect 2 (stale FAIL re-evaluated)** in `tests/sprint/test_checkpoints.py::TestRecoverMissingCheckpoints` (use `_seed_sprint`): seed `CP-P03-END.md` with stale `status: fail` frontmatter + fresh passing evidence; assert the stale verdict does not survive untouched (regenerated/re-stamped with provenance), and a paired negative test: tasks still failing ⇒ checkpoint FAIL preserved.

## Alternative Fixes Considered
- **Defect 2 plain A (re-evaluate-stale auto-PASS):** rejected — false-green risk; violates the `UNKNOWN`-not-PASS constraint.
- **Defect 1 fix in `stash_and_restore_deliverables` instead of merge:** rejected — that path is a pre-rerun backup for `--restore`, not a success-path merge-forward; the data-integrity guarantee belongs in `merge_recovery_bundle` where status is computed.

## Risk + Rollback
- **Over-copy / clobber** in multi-phase releases — mitigate by scoping the copy to the affected phase's declared deliverables + `CP-P{phase}` checkpoint, and preserving clobbered files as `.failed-<ts>`.
- **Fix interaction:** Fix 2-B regenerates the checkpoint into the bundle and depends on Fix 1 to land it canonically — **ship both together**; Fix 2 alone produces a fresh verdict that never reaches canonical.
- **Idempotency:** re-merging the same bundle must not duplicate/corrupt relocated deliverables (mirror `test_merge_is_idempotent`).
- Rollback: both fixes are additive; revert the new merge step + checkpoint re-verify path to restore prior behavior.

## Grounding Gaps
None material. Every cited line was read directly; the path anchors were verified against the live TUIBBS-scp reproduction. Open implementation detail (for task-builder, not a diagnosis gap): confirm whether the end-of-phase checkpoint is modeled as a runnable task in the target tasklist generator to pick Fix 2 primary (B) vs fallback (constrained A).

## Next Steps
`--fix` is set → Tier 3 remediation offered below. Code changes are NOT auto-applied.
