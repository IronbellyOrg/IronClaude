# Research: Planner & Commands / F-4

Status: Complete
Date: 2026-06-03

**Topic:** Data Flow Tracer — Resume planner (F-4 planner side) + command print surface (F-2 PRINT path)
**Scope:** `src/superclaude/cli/sprint/resume/planner.py` (entire) + `src/superclaude/cli/sprint/commands.py` (`_print_resume_decision` L498 + call sites L293, L441, resume flow).
**Handoff boundary:** researcher-02 owns the integrity side (`_validate_last_completed`, `_detect_partial`, `_surface_partial`, `BoundaryReport` model). This file owns (a) what the **planner must EMIT** so integrity's `_validate_last_completed` stops being vacuous (F-4), and (b) the **print surface** that must show report-only partial paths (F-2 Option B). Cross-refs to researcher-02 marked `[->r02]`.

---

## 1. ResumePlanner — inputs, plan build, and the PHASE hard-crash branch (F-4)

### 1.1 Planner inputs (all read-only)

`ResumePlanner.plan(index_path, *, end_override=None)` — `planner.py:36-116`. Derived inputs:

- `release_dir = _resolve_release_dir(index_path)` — `planner.py:39`
- `phases = discover_phases(index_path)` — `planner.py:40` -> `list[Phase]` (each `Phase` has `.number` and `.file: Path` pointing at `phase-N-tasklist.md`; `models.py:341-358`).
- `results_dir = release_dir / "results"` — `planner.py:41`
- `events = self._read_jsonl(release_dir / "execution-log.jsonl")` — `planner.py:42-43`

So the planner DOES have the per-phase tasklist file path for every phase (`Phase.file`), and `parse_tasklist_file(path)` (`config.py:501-515`) returns the ordered `list[TaskEntry]` (each with `.task_id`). This is the key fact for the F-4 fix: **the prior phase's tasklist is reachable and parseable from the planner's existing inputs without any new I/O surface** — only an additional read of an already-on-disk file.

### 1.2 How the plan + `boundary_tasks` get built

1. Classify every phase via `_classify_phase` (`planner.py:60-67, 287-315`) -> `{phase: _COMPLETE|_CRASH|_INTERRUPT|_PENDING}`. `completed_phases` = sorted phases classed `_COMPLETE` (`planner.py:65-67`).
2. `_find_interrupted` (`planner.py:70, 317-326`) returns the lowest non-completed phase that has a start/result (`_CRASH` or `_INTERRUPT`).
3. The interrupted-phase branch (`planner.py:84-90`) sets `interrupted_phase`, `start_phase`, and **defaults `granularity = Granularity.PHASE`**.
4. `_build_boundary(plan, results_dir)` (`planner.py:113-114, 120-169`) refines granularity and fills `boundary_tasks` + `rerun_task_ids` — **only for the interrupted phase**.

### 1.3 The PHASE hard-crash branch — `_build_boundary` L158-169 (quoted)

```python
        else:
            # Hard crash / pre-v4.3.0: derive the failed set from transcripts.
            derived = discover_failed_tasks_from_transcripts(results_dir, interrupted)
            plan.granularity = Granularity.TASK if derived else Granularity.PHASE
            for task_id, status in derived:
                boundary.append(
                    BoundaryTask(task_id=task_id, derived_status=status)
                )
            plan.rerun_task_ids = [task_id for task_id, _ in derived]

        self._assign_roles(boundary)
        plan.boundary_tasks = boundary
```
(`planner.py:158-169`)

**Confirmed F-4 condition:** on a PHASE-granularity hard crash with (a) no `task_results` in `phase-N-result.json` (`task_results == []` at `planner.py:137`, so the `else` branch is taken) AND (b) no per-task transcripts (`discover_failed_tasks_from_transcripts` returns empty -> `derived == []`), then:
- `plan.granularity = Granularity.PHASE` (`planner.py:161`, since `derived` is falsy),
- the `for` loop body never runs => `boundary == []`,
- `_assign_roles([])` is a no-op => **no `BoundaryTask` carries `role == "last_completed"`**,
- `plan.boundary_tasks == []` (`planner.py:169`).

### 1.4 The vacuous-validation consequence `[->r02 integrity side]`

Integrity's `_validate_last_completed` (`integrity.py:97-101`) does:
```python
        lc = next(
            (bt for bt in plan.boundary_tasks if bt.role == "last_completed"), None
        )
        if lc is None:
            return True, [], None
```
With `plan.boundary_tasks == []`, `lc is None` => returns `(True, [], None)` — **vacuously validated**. No task of the *interrupted* phase exists to validate, and crucially the **prior completed phase's tail** (last task of phase N-1) is NEVER referenced. This is exactly the F-4 gap: merged-req `:141-143` (per REPORT F-4, `:53-57`) requires a hard crash mid-phase to double-validate the *prior* phase's tail BEFORE re-running, and the current code reaches no `last_completed` at all.

---

## 2. F-4 — minimal data path: what the planner must EMIT for the prior phase's tail

### 2.1 Deriving the prior completed phase and its tail (from existing inputs)

The planner already has everything needed:

- `plan.interrupted_phase` is set (`planner.py:86`). The "prior phase" is the **highest-numbered completed phase strictly below `interrupted_phase`**. Source: `plan.completed_phases` (already sorted, `planner.py:65-67`). Derivation: `prior = max((n for n in plan.completed_phases if n < interrupted), default=None)`.
- The prior phase's tasklist file is `next(p.file for p in phases if p.number == prior)` — `phases` is in scope in `plan()` (`planner.py:40`) but NOT currently threaded into `_build_boundary` (which receives only `plan, results_dir`). The fix must pass `phases` (or the resolved prior `Phase`) into the boundary builder, OR derive the tail in `plan()` after `_build_boundary` returns.
- The tail task = **last `TaskEntry` of the prior phase tasklist** in source order: `parse_tasklist_file(prior_phase.file)[-1].task_id` (`config.py:501-515`; `TaskEntry.task_id` at `config.py:489`). "Tail" = highest source-order task; the spec's "phase 2 tail" (REPORT `:56`) maps to the last task block in that phase file.

### 2.2 The minimal EMIT contract (planner -> integrity)

For integrity's `_validate_last_completed` to stop being vacuous on the PHASE hard-crash path, the planner must append exactly ONE `BoundaryTask` to `plan.boundary_tasks` representing the prior phase's tail, with:
- `task_id` = prior phase's last `TaskEntry.task_id`,
- `role = "last_completed"` (so `integrity.py:97-99`'s `next(... role == "last_completed")` finds it),
- `persisted_status = TaskStatus.PASS` — Signal A claim, justified because the prior phase is classed `_COMPLETE` (its `phase-N-result.json` passed, `planner.py:304-307`). This makes `signal_a_pass` True at `integrity.py:109`, so the gate's value-add is the independent Signal B (transcript re-derivation, `integrity.py:111-117`) + artifact existence (`integrity.py:119-124`) — i.e. it actually double-validates the tail rather than trusting the PASS claim.

**Important scoping nuance for the integrity side `[->r02]`:** `_validate_last_completed` reads the transcript via `self._read_transcript(results_dir, plan.interrupted_phase, lc.task_id)` (`integrity.py:112-114`) — note it keys the transcript path on `plan.interrupted_phase`, NOT the prior phase. A prior-phase tail task lives under `phase-{prior}-task-...`, so feeding a prior-phase `last_completed` here would look up the transcript under the WRONG phase number. The planner-side fix alone is insufficient; integrity's `_validate_last_completed` / `_read_transcript` must learn the phase the `last_completed` task belongs to. **This is a planner/integrity co-dependency — flag for researcher-02.** Cleanest contract: add a phase field to `BoundaryTask` (or have the planner emit the prior-phase number on the plan) so integrity resolves the transcript under the correct phase. `[->r02 owns the BoundaryTask/model change + the _read_transcript phase fix]`

### 2.3 Why this stays write-free (NFR / no-writes constraint)

`parse_tasklist_file` (`config.py:514`) and `discover_phases` both only `read_text` — no writes. Appending a `BoundaryTask` mutates the in-memory `ResumePlan`, not disk. The fix therefore preserves the planner's pure-read invariant locked by `test_planner_performs_no_writes` (`tests/sprint/test_resume.py:158-172`), which asserts `results/` is byte-identical before/after `ResumePlanner().plan(index)`. Note that test only snapshots `results/`, not the tasklist files — but neither `discover_phases` nor `parse_tasklist_file` writes anywhere, so reading the prior phase tasklist (which lives next to the index, not under `results/`) is safe and still leaves the test green. Recommendation: extend the no-writes test to also snapshot the tasklist dir to lock the new read path as still-read-only (handoff to researcher-04 / CG-3 test work).

---

## 3. F-2 PRINT path — `_print_resume_decision` + call sites

### 3.1 Where partial paths are computed and lost (confirms F-2)

In the integrity gate `run()` (`integrity.py:63-67`):
```python
        partial_paths = self._detect_partial(plan, phase_file, results_dir)
        if partial_paths:
            self._surface_partial(plan, report)
            if cleanup_opted_in:
                self._quarantine(plan, partial_paths, results_dir, report)
```
`partial_paths` is a **local variable**. On the report-only path (`cleanup_opted_in=False` — the default, and what `_auto_resume` uses since it never passes `cleanup_opted_in`, `commands.py:400` calls `BoundaryIntegrityGate().run(plan)` with no kwargs), `_quarantine` is NOT called, so `report.quarantined` stays empty. `_surface_partial` only appends a `BoundaryTask` to `report.suspects` (`integrity.py:198-208`) — it does NOT carry the file paths. The paths are therefore unreachable from the `BoundaryReport`/`ResumeDecision` at print time. `[->r02 confirms: BoundaryReport (models.py:84-101) has no report-only partial-paths field]`

### 3.2 `_print_resume_decision` (L498) — quoted, partial-paths surfaces only via quarantine

```python
def _print_resume_decision(decision) -> None:
    """Print the ResumePlan + DriftAssessment + BoundaryReport (FR-4.2 / FR-4.5)."""
    plan = decision.plan
    click.echo("── Auto-resume plan ──")
    ...
    if decision.report is not None:
        r = decision.report
        click.echo(
            f"  integrity gate:   {'PASS' if r.passed else 'STOP'} "
            f"(last-completed validated: {r.validated_last})"
        )
        for s in r.suspects:
            click.echo(
                f"    suspect: {s.task_id} [{s.role}] "
                f"persisted={s.persisted_status} derived={s.derived_status}"
            )
        for task, reason in r.coherence_warnings:
            click.echo(f"    coherence (advisory): {task.task_id}: {reason}")
        for canonical, copy in r.quarantined.items():
            click.echo(f"    quarantined: {canonical} -> {copy}")
        for reason in r.blocking_reasons:
            click.echo(f"    blocking: {reason}")
```
(`commands.py:498-536`)

Confirmed: the only place partial-work **paths** are printed is the `r.quarantined.items()` loop (`commands.py:533-534`), which is populated ONLY when `cleanup_opted_in` triggered `_quarantine`. On the default report-only path `r.quarantined == {}` ⇒ **no paths printed**. The operator sees the suspect *task* (`commands.py:526-530`) but never the half-written *files*. This is the F-2 under-delivery vs item 3.2 / design §4(b) "report suspect paths in BoundaryReport (always)" (REPORT `:43-44`).

### 3.3 Call sites — report-only path vs quarantine path

`_print_resume_decision` is called at exactly two sites, both in the auto-resume flow:

- **`commands.py:293`** — the `--dry-run` path: `if decision.action == "dry_run": _print_resume_decision(decision)` (`commands.py:292-294`). The `decision` here is built at `commands.py:402-405` (`action="dry_run"`, carries `plan`, `drift`, `report`). This is a **report-only** decision (gate run with `cleanup_opted_in=False`).
- **`commands.py:441`** — the interactive confirm path: inside `_auto_resume`, when `not assume_yes` and stdin is a TTY (`commands.py:437-445`), it prints the decision then `click.confirm(...)`. The `decision` is built inline at `commands.py:441-444` (`action="proceed"`, carries `plan`, `drift`, `report`). Also a **report-only** decision (same `run(plan)` at `commands.py:400`, no quarantine).

**Both call sites fire on the report-only path** — neither runs quarantine. (There is no quarantine call site in `commands.py` at all; `cleanup_opted_in` is never passed from the CLI auto-resume flow.) So Option B (print `_detect_partial()` paths on the report-only path) must surface paths that are currently thrown away in `integrity.run()`.

### 3.4 F-2 Option B — exactly where to print, and the threading gap

The print location is the `if decision.report is not None:` block (`commands.py:520-536`), inserting a new loop alongside the existing `quarantined` loop (e.g. after `commands.py:530`, before/after the coherence loop) that emits each partial path, e.g. `partial work (uncommitted): <path>`.

**Threading gap (load-bearing):** the paths are NOT reachable from `decision.report` today (§3.1). Option B requires carrying `partial_paths` out of `integrity.run()` to the print site. Two routes:
1. **Model field (preferred, aligns with item 3.2 "ALWAYS report suspect paths in the BoundaryReport"):** add a report-only field e.g. `BoundaryReport.partial_paths: list[Path]` and have `run()` set it whenever `partial_paths` is non-empty (regardless of `cleanup_opted_in`). Then `_print_resume_decision` iterates `r.partial_paths`. This is the design §2 field-exactness amendment the REPORT flags (`:110-112`). `[->r02 owns the BoundaryReport model change]`.
2. **Decision-level field:** add `partial_paths` to `ResumeDecision` and populate it in `_auto_resume`. Weaker — `_auto_resume` does not currently see `partial_paths` (it only gets the `report`), so route 1 is cleaner.

Either way the print-site change in `_print_resume_decision` is trivial; the real work is the model/threading change owned by researcher-02. **Handoff: this file specifies the print site (`commands.py:520-536`, new loop next to `:533-534`); researcher-02 specifies the model field that makes the paths reachable.**

---

## 4. F-1 context — `--yes` / CI flag handling in the resume flow

Visible in `commands.py`:
- `assume_yes` is forced True by env: `assume_yes = assume_yes or bool(os.environ.get("SUPERCLAUDE_SPRINT_ASSUME_YES")) or bool(os.environ.get("CI"))` (`commands.py:265-269`).
- In `_auto_resume`, when `assume_yes` is True the confirm/TTY block (`commands.py:437-467`) is skipped entirely and the function returns `action="proceed"` directly (`commands.py:469-471`). On that path `_print_resume_decision` is NEVER called (the only proceed-path print is inside the `not assume_yes` TTY branch at `commands.py:441`). So under `--yes`/CI, partial-work paths are neither quarantined NOR printed NOR is the operator prompted — this is the F-1 residual safety gap (REPORT `:37-39`). The F-2 fix (printing paths) only helps the interactive/dry-run paths; the `--yes`/CI path additionally bypasses the print, so F-1 needs either the CG-4 spec decision or surfacing paths to stderr even on the `--yes` proceed path. (F-1/CG-4 are owned elsewhere; noting the flag mechanics here for completeness.)

---

## 5. Summary

**F-4 (planner side) — confirmed and scoped.**
- Hard-crash + PHASE granularity + no `task_results` (`planner.py:137`) + no transcripts (`derived == []`) ⇒ `boundary == []` (`planner.py:158-169`) ⇒ no `last_completed` role ⇒ integrity `_validate_last_completed` returns vacuously `(True, [], None)` (`integrity.py:97-101`). The prior phase's tail is never validated.
- The planner already holds the inputs to fix it: `plan.completed_phases` (prior = `max(n < interrupted)`), `phases[*].file`, and `parse_tasklist_file(prior.file)[-1].task_id` (`config.py:501-515`). **Minimal EMIT contract:** append ONE `BoundaryTask(task_id=<prior tail>, role="last_completed", persisted_status=PASS)` so integrity's Signal-B/artifact double-check runs.
- **Co-dependency flag for researcher-02:** integrity's `_validate_last_completed`/`_read_transcript` key the transcript on `plan.interrupted_phase` (`integrity.py:112-114`), which is the WRONG phase for a prior-phase tail. A `BoundaryTask` phase field (or plan-level prior-phase number) is required so the transcript resolves under `phase-{prior}-...`. Planner fix alone is insufficient.
- **Write-free:** `discover_phases`/`parse_tasklist_file` only read; fix mutates in-memory plan only. `test_planner_performs_no_writes` (`tests/sprint/test_resume.py:158-172`) stays green (it snapshots `results/`; the new read is of the tasklist dir). Recommend extending that test to snapshot tasklists too.

**F-2 (commands print side) — confirmed.**
- `_detect_partial()` paths (`integrity.py:63`) are a local var in `run()`; printed ONLY via `report.quarantined` (`commands.py:533-534`), which is populated only when `cleanup_opted_in=True`. Auto-resume always runs report-only (`commands.py:400`, no kwargs), so paths are never printed.
- Both `_print_resume_decision` call sites — `commands.py:293` (dry-run) and `commands.py:441` (interactive confirm) — are report-only; neither quarantines.
- **Option B fix:** print partial paths in the `if decision.report is not None:` block (`commands.py:520-536`, a new loop beside `:533-534`). The paths must first be threaded out of `integrity.run()` — preferred route is a `BoundaryReport.partial_paths` field set unconditionally when non-empty (the design §2 amendment, REPORT `:110-112`). **`[->r02 owns the BoundaryReport model field]`; this file owns the print site.**

**F-1 context:** `assume_yes` forced True by `SUPERCLAUDE_SPRINT_ASSUME_YES`/`CI` (`commands.py:265-269`); the `--yes`/CI proceed path (`commands.py:469-471`) skips the print entirely, so F-2's print fix does not cover it — the F-1 residual gap.

**Key file:line anchors:** `planner.py:158-169` (hard-crash branch), `planner.py:40,65-67,113-114` (planner inputs), `config.py:501-515` (`parse_tasklist_file`), `integrity.py:63-67,97-101,112-114` (vacuous validation + partial-paths drop), `commands.py:265-269,292-294,400,437-471,498-536` (flags, call sites, print fn).
