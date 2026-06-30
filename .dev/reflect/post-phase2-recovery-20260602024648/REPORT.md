# sc:reflect UC-2 Post-Execution Audit — Phase 2 (recovery.py)

**Task:** TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601
**Mode:** post (UC-2)
**Tier reached:** 2 (heterogeneous ensemble: sonnet analyzer + haiku qa)
**Date:** 2026-06-02
**Worktree:** /config/workspace/IronClaude/.claude/worktrees/SprintReRun (branch SprintReRun)
**Artifact under review:** `src/superclaude/cli/sprint/recovery.py` (640 LOC) + `models.py` D1 fix
**Authoritative spec:** `.dev/releases/backlog/SprintGranularResume/merged-requirements.md` §T5/T7/T8

---

## Verdict

**status: partial** — Phase 2 is structurally conformant to the task spec (rf-qa-style checks all pass), but ensemble review against the *real* `SprintConfig` API and the TDD's mandatory T8 defenses surfaced **3 HIGH Phase-2-local defects** and **2 deferred-to-Phase-3 obligations** that the inline structural gate could not catch.

This is the designed value of sc:reflect over inline rf-qa: the inline gate verified the code matches the *task instructions*; the ensemble verified the code matches the *real downstream API and the TDD's safety contract*. The task instructions themselves carried the path-convention drift.

**Calibrated confidence: 0.86** — high agreement between two heterogeneous model classes on the load-bearing findings (F1/F2 path drift confirmed by orchestrator + sonnet independently; F6 sidecar data-loss confirmed by orchestrator re-Read).

---

## Findings Summary

| ID | Severity | Class | Phase-local? | Title |
|----|----------|-------|--------------|-------|
| **R-F1** | HIGH | Drift | YES | `results_dir` derived from `source_index.parent`, not canonical `release_dir` |
| **R-F2** | HIGH | Drift | YES | execution-log.jsonl written inside `results/` instead of `release_dir/` |
| **R-F3** | HIGH | Drift | YES | Step-7 invents `task-results.json` sidecar; deletes affected task_results when absent (data loss) |
| **R-F4** | MEDIUM | Drift | Partial (P2↔P3 interface) | Transcript replacement uses exact-name match; spec rerun artifacts (`phase-Nr-…`) won't match canonical (`phase-N-…`) |
| **R-F5** | MEDIUM | Drift | Partial | Checkpoint replacement filter skips spec-named `phase-N-cpK.md`; glob can match `.failed-` artifacts on rerun |
| **R-F6** | MEDIUM | Gap | Deferred→P3 | T8.1 SHA mid-flight-edit ABORT not enforced (only `end_tasklist_sha256` computed, never compared) |
| **R-F7** | MEDIUM | Gap | Deferred→P3 | T8.2 retry-cap-3 ABORT not enforced (counter `retry_count_for_task` provided, no enforcement) |
| **R-F8** | LOW | Cleanup | YES | Lock acquisition is TOCTOU-racy (`exists()` then `write_text`; should use `O_CREAT\|O_EXCL`) |
| **R-F9** | LOW | Cleanup | YES | Dead `_ = time.monotonic()` at recovery.py:640; never emitted |
| **R-F10** | — | Authorized | — | Step-6 append-only `phase_complete_superseded_by` event (task-authorized over spec's "mutate") — NOT a defect |
| **R-F11** | — | Necessary | — | RecoveryBundle field reorder (affected_phase before verb) — forced by dataclass semantics; spec had latent invalid-dataclass bug — NOT a defect |

---

## Grounded Findings (detail)

### R-F1 [HIGH, Drift, Grounded] — results_dir derivation diverges from canonical SprintConfig

**recovery.py:405** — `results_dir = source_index.parent / "results"`.

The canonical convention is `SprintConfig.results_dir → self.release_dir / "results"` (**models.py:537-539**). `index_path` and `release_dir` are **independent** fields (**models.py:416-417**), and `config.py:_resolve_release_dir` (**config.py:236-272**) explicitly returns the *grandparent* when the index lives under `tasklist/`, `tasklists/`, or `tasks/`. Therefore `source_index.parent != release_dir` in the common case.

**Impact:** for an index at `<release>/tasklist/index.md`, the merge engine writes canonical artifacts to `<release>/tasklist/results/` — the real results live at `<release>/results/`. Merge-back silently updates the wrong tree.

**Fix:** do not infer paths from `source_index.parent`. Change `merge_recovery_bundle` to accept `results_dir`/`release_dir` explicitly (or a `SprintConfig`), resolved via `_resolve_release_dir`. The §T5 signature `merge_recovery_bundle(bundle, source_index)` should be widened to carry the release dir — Phase 3's `run_rerun_tasks` already holds the `SprintConfig` and can pass it.

### R-F2 [HIGH, Drift, Grounded] — execution-log.jsonl written to wrong path

**recovery.py:511 and :558** — events appended to `results_dir / "execution-log.jsonl"`.

Canonical `SprintConfig.execution_log_jsonl → self.release_dir / "execution-log.jsonl"` (**models.py:541-543**) — the log lives in `release_dir`, the **parent** of `results_dir`. Spec §T5 step 5 (**merged-requirements.md:91-95**) names `execution-log.jsonl`, not `results/execution-log.jsonl`.

**Impact:** rerun events (`phase_rerun_start`, `task_rerun_complete`, `phase_rerun_complete`, `phase_complete_superseded_by`) land in `results/execution-log.jsonl` while the canonical sprint log is never updated — breaking the audit chain and any consumer (`sprint run --resume`, dashboards) that reads the canonical log.

**Fix:** resolve `release_dir` (per R-F1) and write both step-5 and step-6 events to `release_dir / "execution-log.jsonl"`.

### R-F3 [HIGH, Drift, Grounded] — Step-7 invents a sidecar and deletes affected results when it's absent

**recovery.py:585-602** — `keep` filters OUT all `task_results` whose `task_id ∈ affected_tasks` (line 587-589); `new_results` is populated only if a bundle-local `task-results.json` sidecar exists (line 596-601); final assignment is `existing["task_results"] = keep + new_results` (line 602).

When no sidecar exists, `new_results == []`, so the affected tasks' result entries are **permanently dropped** from `phase-N-result.json`. The inline comment (line 592) claims "otherwise the prior results stand" — **the code does the opposite**: the comment is false.

§T5 step 7 (**merged-requirements.md:96-97**) requires rewriting `task_results` with the new PASSes; it does **not** specify a `task-results.json` sidecar (the §T5 RecoveryBundle field list, lines 70-84, has no such field). The sidecar is invented implementation drift, and its absence causes data loss rather than the documented no-op.

**Fix:** either (a) formalize the sidecar as part of the bundle contract and **abort** if it's missing for a SUCCESS merge, or (b) consume the rerun bundle's own serialized `PhaseResult`/`phase-N-result.json`. Never silently drop affected entries — if no replacement is available, preserve the prior entries or fail loudly.

### R-F4 [MEDIUM, Drift, Grounded] — transcript replacement exact-name match breaks on spec rerun naming

**recovery.py:419-436** (and errors siblings :462-479) — canonical file is renamed to `.failed-<ts>` first, then a replacement is copied only `if produced.name == canonical.name`.

Spec §T5 step 1 (**merged-requirements.md:86-90**) names rerun artifacts `phase-Nr-task-T07.11-output.txt` (rerun phase id `Nr`) copied to canonical `phase-7-task-T07.11-output.txt`. These filenames **differ by prefix**, so the exact-name guard fails: the canonical file is renamed away and **no replacement is copied**, with no failure recorded — the merge can still report SUCCESS with a missing canonical transcript.

This is partly a **Phase 2↔Phase 3 interface contract**: it only manifests once Phase 3's `run_rerun_tasks` builds `bundle.artifacts_produced`. If Phase 3 names bundle artifacts identically to canonical, the match works; if it follows the spec's `phase-Nr-` convention, it breaks.

**Fix:** replace the exact-name guard with an explicit canonical→produced mapping carried on the bundle, and verify the replacement exists **before** renaming the canonical original (see R-F8/transactionality).

### R-F5 [MEDIUM, Drift, Grounded] — checkpoint filter skips spec-named checkpoints; glob matches `.failed-` files

**recovery.py:438-458** — `if not any(tid in cp_canonical.name for tid in bundle.affected_tasks): continue`. Spec checkpoint names like `phase-7-cp2.md` (**merged-requirements.md:88-90**) contain no task ID, so they are skipped and never replaced. Additionally `results_dir.glob(f"phase-{phase}-cp*.md")` will match previously-preserved `phase-7-cp2.failed-<ts>.md` on a second rerun.

**Fix:** drive checkpoint replacement from an explicit bundle mapping, not task-ID substring; exclude `.failed-` from any glob-based canonical discovery.

### R-F6 [MEDIUM, Gap, deferred→Phase 3] — T8.1 SHA mid-flight-edit ABORT not enforced

**recovery.py:625** computes `bundle.end_tasklist_sha256 = compute_tasklist_sha256(source_index)` but never compares it (or the current source hash) to `bundle.source_tasklist_sha256`, and never aborts. §T8.1 (**merged-requirements.md:151-155**) makes the abort-on-mismatch **mandatory** with a specific operator message + `--force-merge` override.

**Phase boundary note:** the natural home for this check is the orchestration entrypoint `run_rerun_tasks` (Phase 3) *before* it calls `merge_recovery_bundle`. The task's Phase 2 Step 2.7 listed only the 7 merge steps and did not include the T8.1 gate, so this is a legitimate Phase-3 obligation — **not a Phase 2 regression**. Flagged so Phase 3 does not omit it.

### R-F7 [MEDIUM, Gap, deferred→Phase 3] — T8.2 retry-cap-3 ABORT not enforced

**recovery.py:347-355** — `retry_count_for_task` returns a count and documents "callers compare this count to that threshold." No abort exists. §T8.2 (**merged-requirements.md:155-156**) mandates the 4th-attempt abort with `--allow-loop` override.

**Phase boundary note:** Phase 2 Step 2.6 asked only for the counter helper; enforcement belongs to Phase 3's `run_rerun_tasks` (which has `--allow-loop`). **Not a Phase 2 defect** — flagged as a Phase 3 obligation.

### R-F8 [LOW, Cleanup, Grounded] — lock acquisition is TOCTOU-racy

**recovery.py:296-332** — `if lock_path.exists(): … else: lock_path.write_text(...)`. Two processes can both observe no lock and both write. §T8.5 (**merged-requirements.md:158-159**) requires reliable concurrent detection (INV-4).

**Fix:** acquire via `os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)` after stale-lock cleanup; on `FileExistsError`, read PID/timestamp and raise. (Low severity in practice: concurrent recovery on one machine is rare and the window is sub-millisecond, but the spec calls the defense mandatory.)

### R-F9 [LOW, Cleanup, Grounded] — dead `time.monotonic()` assignment

**recovery.py:640** — `_ = time.monotonic()` captured and never used; `time` is imported (line 22) solely for this. Remove the line and the import (or wire a real merge-duration into the audit event).

---

## Non-defects (correctly classified, no action)

### R-F10 [Authorized] — Step-6 append-only supersede event

**recovery.py:556-574** emits a new `phase_complete_superseded_by` event rather than mutating the prior `phase_complete` event (spec §T5 step 6 says "mutate"). This is **explicitly authorized** by the task: Phase 2 Step 2.7 mandates "append-only — never rewrite prior events … a new 'supersede' link event is added instead." The append-only choice is safer for JSONL integrity. No action.

### R-F11 [Necessary] — RecoveryBundle field reorder

**recovery.py:106-115** orders `affected_phase` before `verb`, whereas §T5 lists `verb` first. This is **forced by Python dataclass semantics** — `verb` has a default, `affected_phase` does not, and a defaulted field cannot precede a non-defaulted one. The §T5 code block is itself an invalid dataclass; the implementation correctly repaired it and documented the order in the Attributes block. No action. (Serialization is by field name, so wire-compat is unaffected.)

Also verified clean by the ensemble: RecoveryStatus 4-member enum + `is_terminal` (recovery.py:59-69); ReflectReportNominator safe-stub degradation incl. PyYAML-absent path (recovery.py:165-231); models.py TYPE_CHECKING forward-ref with no runtime cycle (models.py:8,23-27,609); `Optional[str]` vs `str|None` (task-mandated equivalent); docstring Attributes blocks match fields.

---

## Deviation Taxonomy Roll-up

| Class | Count | IDs |
|-------|-------|-----|
| Regression | 0 | — |
| Drift | 5 | R-F1, R-F2, R-F3, R-F4, R-F5 |
| Gap (deferred to Phase 3) | 2 | R-F6, R-F7 |
| Cleanup (LOW) | 2 | R-F8, R-F9 |
| Authorized | 1 | R-F10 |
| Necessary | 1 | R-F11 |

No regressions. The Phase 1 D1 fix (models.py TYPE_CHECKING forward-ref) is confirmed correct and cycle-free.

---

## Recommendation

**Before Phase 2's PG2.2 rf-qa gate runs, fix the 3 HIGH Phase-2-local Drift defects:**
1. **R-F1 + R-F2** (paths) — widen `merge_recovery_bundle` to take an explicit `release_dir`/`results_dir` (or `SprintConfig`) resolved via `_resolve_release_dir`; write execution-log to `release_dir/execution-log.jsonl`. These two share one fix.
2. **R-F3** (sidecar data-loss) — make the merge abort/fail when affected-task replacement results are unavailable, rather than silently dropping prior entries; fix the false comment.

**Address before Phase 3 marks merge-back complete:**
3. **R-F4 + R-F5** — replace exact-name / substring matching with an explicit bundle artifact mapping (this is the Phase 2↔Phase 3 contract; resolve it when Phase 3 defines bundle layout).

**Log as explicit Phase 3 obligations (do not lose):**
4. **R-F6** (T8.1 SHA abort) and **R-F7** (T8.2 retry-cap abort) must be wired into Phase 3 `run_rerun_tasks` before calling `merge_recovery_bundle`.

**Cleanup (any time before Phase 6 lint gate):**
5. **R-F8** (atomic lock), **R-F9** (dead code).

The recommended sequencing keeps R-F4/R-F5 honest: they are interface contracts best fixed when Phase 3 defines the bundle directory layout, so fixing them now risks guessing the Phase 3 shape. R-F1/R-F2/R-F3 are unambiguously Phase-2-local and should be fixed now.
