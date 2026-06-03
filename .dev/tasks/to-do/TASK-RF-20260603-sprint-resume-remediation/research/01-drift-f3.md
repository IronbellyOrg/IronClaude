# Research: Drift / F-3

**Topic type:** File Inventory + Data Flow — Drift detection (finding F-3)
**Scope:** `src/superclaude/cli/sprint/resume/drift.py` (full); `models.py` (DriftResult/ResumePlan/ResumeIndex shapes); `__init__.py` exports
**Status:** Complete
**Date:** 2026-06-03

---

## 1. Full structure of `drift.py` — `DriftAssessor.assess()` and every confidence branch

File: `src/superclaude/cli/sprint/resume/drift.py` (282 lines total). Class `DriftAssessor` (`drift.py:26`). Public method `assess(self, index_path, plan) -> DriftAssessment` (`drift.py:29-60`).

Control flow of `assess()`:

1. `drift.py:31` — resolve boundary phase file via `_boundary_phase_file()`.
2. `drift.py:32-39` — **branch A (1.0 / tier=hash):** `phase_file is None` (nothing-to-resume / fresh). `cosmetic_only=True`.
3. `drift.py:41-42` — compute `current_sha = _current_sha(phase_file)` and `recorded_sha = _recorded_sha(plan)`.
4. `drift.py:46-55` — **branch B / Tier 0 (1.0 / tier=hash):** `recorded_sha and current_sha and current_sha == recorded_sha` (exact normalized-content hash match, rerun-block stripped). `cosmetic_only=True`.
5. `drift.py:59` — **Tier 0 MISS** (or no recorded hash): fall through to `_tier1(...)`.
6. `drift.py:60` — `_annotate_git(assessment, phase_file)` (Tier 2, additive).

Every confidence branch (with exact lines + trigger):

| Conf | tier | Lines | Trigger condition | cosmetic_only |
|------|------|-------|-------------------|---------------|
| 1.0 | hash | `32-39` | `phase_file is None` (fresh/nothing-to-resume) | True |
| 1.0 | hash | `46-55` | Tier 0: `current_sha == recorded_sha` (exact match) | True |
| 0.3 | structural | `107-126` | TASK granularity + non-empty `recorded_all` + `current_ids` empty (parse-failure/corrupt/gutted phase file) | False |
| 0.9 | structural | `130-140` | `granularity is not TASK` OR `not recorded_all` (PHASE-level resume / no per-task baseline → whole phase re-runs) | True |
| **0.3** | structural | `142-155` | `removed_completed` non-empty: a recorded PASS task ID is no longer present (ID removal/rename) — **the ONLY material-completed branch** | False |
| 0.85 | structural | `157-175` | `added` or `removed_pending` non-empty: changes confined to not-yet-run region | False |
| **0.9** | structural | `177-187` | **fall-through: task-ID set identical to recorded** ⇒ deemed cosmetic (whitespace/formatting) | **True** ← **F-3 DEFECT** |

The `_annotate_git` step (`drift.py:218-265`) runs on every Tier-1 result and may upgrade `tier` from `structural` to `git`, but NEVER touches `confidence` (see §4).

## 2. `_current_task_ids()` and the "identical ID set ⇒ 0.9 cosmetic" branch

`_current_task_ids(phase_file)` (`drift.py:209-216`): calls `parse_tasklist_file(phase_file)` and returns `{e.task_id for e in entries if getattr(e, "task_id", None)}` — i.e. **a set of task IDs only**, no body/checkpoint/deliverable content. Returns empty `set()` on `OSError`.

Tier 1 (`_tier1`, `drift.py:64-187`) diffs ONLY task-ID sets:
- `current_ids = self._current_task_ids(phase_file)` (`drift.py:88`)
- `recorded_completed` = IDs from `plan.boundary_tasks` with `persisted_status is TaskStatus.PASS` (`drift.py:90-94`)
- `recorded_all` = IDs with `persisted_status is not None` (`drift.py:95-99`)
- `removed_completed = recorded_completed - current_ids` (`drift.py:142`)
- `added = current_ids - recorded_all` (`drift.py:157`)
- `removed_pending = (recorded_all - recorded_completed) - current_ids` (`drift.py:158`)

**CONFIRMED F-3 root cause:** The final fall-through branch (`drift.py:178-187`, confidence 0.9, `cosmetic_only=True`) is reached when, after a Tier-0 hash MISS (`assess()` only calls `_tier1` when `current_sha != recorded_sha`, `drift.py:59`), the **task-ID set is identical** to the recorded set and no add/remove fired. Tier 0 has already proven the file content *changed* (hash differs), but Tier 1 then dismisses it as cosmetic purely because no task ID was added/removed/renamed. A prose/checkpoint/deliverable edit to a completed task that keeps its `### Txx.yy` ID lands here → 0.9 → silent resume. This contradicts AC-5 (`<0.8`).

The branch's explanation text even asserts the differences are "cosmetic (whitespace/formatting)" — but that is an *unverified assumption*; nothing in Tier 1 proves the change was whitespace-only. (Tier 0 is NOT whitespace-tolerant — see drift.py:44-45 docstring "AC-4 is handled in Tier 1, not here" — so a whitespace-only edit would also reach this same 0.9 branch. That conflation is exactly why the branch cannot distinguish "trailing-whitespace cosmetic" from "material prose/deliverable rewrite".)

## 3. What data does `assess()` receive? Data-availability trace (CRITICAL)

Signature: `assess(self, index_path: Path, plan: ResumePlan) -> DriftAssessment` (`drift.py:29`).

### `ResumePlan` fields available (`models.py:55-69`)
`index_path`, `release_dir`, `completed_phases`, `interrupted_phase`, `interrupt_kind`, `start_phase`, `end_phase`, `granularity` (`Granularity` enum), `boundary_tasks: list[BoundaryTask]`, `rerun_task_ids`, `ambiguous`, `ambiguity_reasons`.

### `BoundaryTask` fields (`models.py:37-52`)
`task_id`, `persisted_status` (Signal A), `derived_status` (Signal B), `artifacts_present: bool`, `role`, `suspect: bool`.

**Note:** `BoundaryTask` carries NO per-task content hash, NO checkpoint path list, NO deliverable path list — only `artifacts_present` (a single bool meaning "declared deliverables/checkpoints exist on disk"). There is NO recorded baseline of *what* those paths were.

### What `assess()` reads from disk
- `_current_sha(phase_file)` (`drift.py:201-207`) → `_content_sha256_excluding_rerun_block` over the CURRENT phase file (whole-file normalized hash).
- `_recorded_sha(plan)` (`drift.py:267-281`) → reads `plan.release_dir / "results" / f"phase-{interrupted_phase}-result.json"` and returns the single string field `tasklist_sha256`. NOTHING ELSE is read from result.json.

### `phase-N-result.json` payload (authoritative, `executor.py:2069-2078`, written by `_write_phase_result_json`)
Keys: `phase`, `status`, `exit_code`, `started_at`, `finished_at`, `task_results` (per-task status dicts via `tr.to_dict()`), `recovery_history`, `tasklist_sha256` (whole-file hash, `executor.py:2077`).

**→ There is NO per-task content hash, NO recorded checkpoint-path list, NO recorded deliverable-path list anywhere in result.json or in `ResumePlan`/`BoundaryTask`.** The only recorded structural signals are: per-task *status* (`task_results`) and the whole-phase-file `tasklist_sha256`.

### Does `extract_checkpoint_paths` exist? — YES
- `extract_checkpoint_paths(phase_file: Path, release_dir: Path) -> list[tuple[str, Path]]` lives at `src/superclaude/cli/sprint/checkpoints.py:40-98`. It parses every `Checkpoint Report Path:` line from the **given phase_file** (current on-disk content), pairs each with the nearest `### Checkpoint: <name>` heading, resolves relative paths against `release_dir`. Returns `[]` on read failure or no declarations.
- Companion `_declared_deliverables(source_tasklist: Path, task_id: str) -> list[Path]` at `rerun_tasks.py:924-948` — parses the `**Artifacts (Intended Paths):**` section of a given task block from the **current** tasklist.

**CRITICAL CONSTRAINT:** Both `extract_checkpoint_paths` and `_declared_deliverables` operate on the *current* phase file only. There is **no recorded baseline** (no prior checkpoint/deliverable list captured at phase-completion time) to diff the current values against. So design §5's "compose extract_checkpoint_paths + deliverable-path diff" cannot be a true *diff* with the data persisted today — there is no "before" snapshot. The only "before" signal that exists is the whole-file `tasklist_sha256`, which Tier 0 already proved differs.

This is the **data-availability blocker** the REPORT anticipated ("The data constraint (no per-task content/checkpoint baseline in result.json) is real"). It forces the F-3 fix to be **conservative (<0.8 STOP)** rather than a precise checkpoint/deliverable diff — unless the result.json schema is also extended to persist a per-task or checkpoint/deliverable baseline (larger change, design §2 amendment).

## 4. Tier 2 git characterization — confirm advisory-only (NFR-3)

`_annotate_git(assessment, phase_file)` (`drift.py:218-265`):
- Runs `git rev-parse @{upstream}` (`drift.py:245`), `git ls-files --error-unmatch <phase_file>` (`drift.py:246`), then `git diff --ignore-all-space --stat @{upstream} -- <phase_file>` (`drift.py:247-254`).
- On ANY failure (`OSError`, `subprocess.SubprocessError`) it returns the Tier-1 `assessment` untouched (`drift.py:255-256`).
- On success it appends `git: <stat line>` annotations to `assessment.changed_paths` and sets `assessment.tier = "git"` (`drift.py:259-264`).

**CONFIRMED: it NEVER assigns `assessment.confidence`** — only mutates `changed_paths` and `tier`. So the gate decision (the 0.8 boundary, AC-4/AC-5) is a pure function of Tier 0 + Tier 1 deterministic signals; Tier 2 is advisory-only (NFR-3 deterministic-core invariant holds).

- `git --ignore-all-space` IS already used (`drift.py:249`) — but only inside the advisory Tier 2 stat, NOT in the gate path.
- Whether the phase file is git-tracked in the resume flow is NOT guaranteed: Tier 2 explicitly handles untracked/detached/no-upstream/git-absent by skipping (`drift.py:255-256`). Sprint phase tasklists may or may not be committed; the gate must not depend on it.

## 5. Proposed EXACT minimal, deterministic F-3 fix

**Surface to change:** the fall-through branch at `drift.py:177-187` (the `return DriftAssessment(confidence=0.9, ... cosmetic_only=True)` reached when the task-ID set is identical to the recorded set after a Tier-0 hash miss).

**Core principle (from REPORT §F-3 + AC-5):** after a Tier-0 hash MISS with an unchanged ID set, the assessor must NOT assume cosmetic. It must score **<0.8 (STOP)** unless it can **deterministically prove** the change is whitespace/formatting-only.

### Minimal deterministic fix (recommended — no schema change, no new data threading)
Replace the unconditional 0.9 fall-through with a whitespace-normalized re-comparison:

1. Compute a *whitespace-insensitive* normalized hash of the current phase file and compare it to a whitespace-insensitive normalization of the recorded baseline. **BLOCKER:** the recorded side only persists `tasklist_sha256` (a *non*-whitespace-tolerant hash, `executor.py:2077` via `_content_sha256_excluding_rerun_block`); the recorded *raw body* is NOT persisted in result.json. Therefore drift cannot recompute a whitespace-insensitive hash of the baseline from result.json alone — there is no baseline text to renormalize.

   → Consequence: a *purely deterministic* "prove it's whitespace-only" check is **not possible from persisted data** today. The only baseline available is `tasklist_sha256` and per-task status. Given a Tier-0 miss + unchanged IDs, drift cannot tell whitespace-cosmetic from material-prose without either (a) a recorded raw/whitespace-normalized baseline, or (b) git.

2. **Therefore the safe minimal fix is conservative:** change `drift.py:177-187` so that an unchanged-ID set *after a Tier-0 miss* scores **<0.8** (e.g. 0.5 or 0.3), `cosmetic_only=False`, with an explanation that the file content changed (hash miss) but no task IDs were added/removed, so the change could not be proven cosmetic and resume STOPs. This satisfies AC-5 ("material edit to a completed-phase task ⇒ <0.8, STOP") for the same-ID body/checkpoint/deliverable case.

   - **Important guard — do NOT regress AC-4:** AC-4 (trailing-whitespace cosmetic ⇒ should still be safe/cosmetic) is currently *also* served by this same 0.9 branch (Tier 0 is not whitespace-tolerant per drift.py:44-45). Flipping the whole branch to <0.8 would make a pure trailing-whitespace edit STOP, breaking AC-4 and test `test_drift_*` at `test_resume.py` (the AC-4 test around `:255-259` asserts `cosmetic_only is True` and `tier != "hash"`). **To preserve AC-4 deterministically without a baseline, add a whitespace-tolerant hash to the recorded side** — see "Schema-extension option" below. Without it, the fix is forced to choose between AC-4 (cosmetic-safe) and AC-5 (material-stop), which is the genuine tension the REPORT flags.

### Schema-extension option (resolves AC-4 vs AC-5 cleanly, larger change)
Persist a **whitespace-normalized** hash (e.g. `tasklist_sha256_ws`) alongside `tasklist_sha256` in `_write_phase_result_json` (`executor.py:2069-2078`). Then in the F-3 branch:
- recompute the current whitespace-normalized hash; if it equals the recorded `tasklist_sha256_ws` ⇒ truly whitespace-only ⇒ keep 0.9 cosmetic (AC-4 satisfied);
- else (content changed beyond whitespace, IDs unchanged) ⇒ <0.8 STOP (AC-5/F-3 satisfied).

This is fully deterministic (no git), backward-compatible (pre-v4.3.x result.json lacks the key ⇒ fall back to the conservative <0.8), and is the only way to *prove* cosmetic vs material for same-ID edits from persisted data. Requires touching `executor.py:_write_phase_result_json` + `drift.py:_recorded_sha`-style reader for the new field + a design §2/§5 amendment.

### Checkpoint/deliverable diff (design §5 literal reading) — NOT achievable as a true diff today
Composing `extract_checkpoint_paths` + `_declared_deliverables` only yields the *current* paths; with no recorded baseline they cannot be diffed. They could be used as a *heuristic signal* ("phase declares checkpoints/deliverables AND content changed ⇒ treat as material") but that is weaker than the whitespace-hash approach and overlaps it. Recommend the whitespace-hash schema extension as the principled fix; the conservative <0.8 (no schema change) as the minimal fix.

## 6. Deterministic-core constraint (must NOT depend on git)

Confirmed by §4: `confidence` is set only in Tier 0 (`assess`) and Tier 1 (`_tier1`); Tier 2 (`_annotate_git`) only annotates. The F-3 fix MUST live in the Tier-1 fall-through branch (`drift.py:177-187`) or in a deterministic recorded-hash comparison — NOT in `_annotate_git`. Using `git --ignore-all-space` to decide cosmetic-vs-material would violate NFR-3 (gate would depend on git availability/tracking, which Tier 2 explicitly treats as optional, `drift.py:255-256`). Git may *advise* but must never *gate*. The REPORT's "or use `git --ignore-all-space` when tracked" must therefore remain advisory; the gate-determining decision must come from the deterministic whitespace-hash (schema extension) or the conservative <0.8 default.

## Summary

- **F-3 confirmed.** Defect branch: `drift.py:177-187` returns confidence **0.9 / cosmetic_only=True** whenever the current task-ID set equals the recorded set — even though `assess()` only reaches Tier 1 *after* a Tier-0 hash MISS (`drift.py:46-59`) that already proved file content changed. Same-ID prose/checkpoint/deliverable edits to a completed task silently resume, violating AC-5 (`<0.8`).
- **Tier 1 diffs ONLY task IDs** (`_current_task_ids`, `drift.py:88,209-216`); the only material-completed branch is ID removal/rename (`drift.py:142-155`, 0.3). AC-5 test (`test_resume.py:261-274`) covers ID removal only — same-ID material edits are untested (CG-2).
- **Data-availability blocker is REAL.** `phase-N-result.json` (`executor.py:2069-2078`) persists only per-task *status* + whole-file `tasklist_sha256`; no per-task content hash, no recorded checkpoint/deliverable baseline. `ResumePlan`/`BoundaryTask` carry no such baseline either. `extract_checkpoint_paths` (`checkpoints.py:40`) and `_declared_deliverables` (`rerun_tasks.py:924`) exist but parse only the CURRENT file — there is no "before" snapshot to diff against. Design §5's "checkpoint/deliverable diff" cannot be a true diff with today's persisted data.
- **Recommended fix (deterministic, no git):** minimal = flip the `drift.py:177-187` fall-through to **<0.8 STOP** when content changed (Tier-0 miss) but IDs unchanged — with the caveat that this regresses AC-4 (whitespace-cosmetic) unless paired with a whitespace-normalized recorded hash. Principled = persist a `tasklist_sha256_ws` (whitespace-normalized) in `executor.py:_write_phase_result_json`, then keep 0.9 only when the whitespace-normalized hashes match, else <0.8. Backward-compatible (missing key ⇒ conservative fallback). Requires a design §2/§5 amendment.
- **NFR-3 holds and must hold:** Tier 2 `_annotate_git` (`drift.py:218-265`) never sets `confidence`; `git --ignore-all-space` (`drift.py:249`) is advisory only. The fix must NOT make the gate depend on git.
- **Files in the fix surface:** `src/superclaude/cli/sprint/resume/drift.py` (branch `177-187`, plus a recorded-WS-hash reader); for the principled fix also `src/superclaude/cli/sprint/executor.py:2069-2078` (persist WS hash) and a new test in `tests/sprint/test_resume.py` for the same-ID material-edit case (CG-2).
