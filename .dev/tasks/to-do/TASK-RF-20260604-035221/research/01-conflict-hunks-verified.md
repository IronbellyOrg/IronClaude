# Research: Conflict Hunks + Verified Resolutions

- Topic type: File Inventory + exact conflict hunks and verified resolutions
- Scope: PR #124 (`feat/sprint-auto-resume-v435` → `master`), 3 conflicted files: CHANGELOG.md, src/superclaude/cli/sprint/commands.py, src/superclaude/cli/sprint/executor.py
- Status: Complete
- Date: 2026-06-04

---

## Reproduction (evidence)

```
$ git merge-base origin/master origin/feat/sprint-auto-resume-v435
86c4632130101f15694c00be1503a44e4d0cf68e

$ git merge-tree --write-tree --name-only origin/master origin/feat/sprint-auto-resume-v435
a53db586640dc2bb2753e585862108ed737fd529      <- TREE OID (first line)
CHANGELOG.md
src/superclaude/cli/sprint/commands.py
src/superclaude/cli/sprint/executor.py
(exit 1 = conflicts present, expected)
```

- merge-base = `86c46321` (matches orchestrator).
- TREE OID = `a53db586640dc2bb2753e585862108ed737fd529`.
- Conflicted paths = exactly the 3 expected files.
- Auto-merged clean (no markers): `pyproject.toml`, `models.py`, `rerun_tasks.py`, `tests/sprint/test_cli_contract.py`, `tests/sprint/test_executor.py`.

All conflict-marked files read via `git show <TREE_OID>:<path>` — no checkout, no working-tree mutation.

---

## FILE 1 — CHANGELOG.md (1 hunk) — RESOLUTION: KEEP BOTH

Conflict markers (line numbers in the merged blob from `git show $TREE:CHANGELOG.md`):

| Marker | Line |
|---|---|
| `## [Unreleased]` | 5 |
| `<<<<<<< origin/master` | 7 |
| `=======` | 25 |
| `>>>>>>> origin/feat/sprint-auto-resume-v435` | 55 |

Both sides ONLY ADD a distinct `### ...` section under `## [Unreleased]`; no shared edits, no overlap.

- **master side** (lines 8–24) header:
  `### Sprint CLI — wire the per-task execution path + runner-owned typed handoff (Stages 0-3, TASK-RF-SPRINTCLI-WIRE-DEAD-20260603-024610)`
- **PR side** (lines 26–54) header:
  `### sprint — auto-resume as the default for `run` / `rerun-tasks` (v4.3.5, TASK-RF-20260602-sprint-auto-resume)`

**Resolution:** strip the 3 marker lines, keep both `###` blocks in order (master block first, then PR block), preserving the existing `### sc:cleanup-audit ...` section that follows at line 57. No content edits inside either block.

---

## FILE 3 — executor.py (1 hunk) — RESOLUTION: TAKE MASTER (semantic)

Conflict markers in `git show $TREE:src/superclaude/cli/sprint/executor.py`:

| Marker | Line |
|---|---|
| `<<<<<<< origin/master` | 354 |
| `=======` | 356 |
| `>>>>>>> origin/feat/sprint-auto-resume-v435` | 358 |

Conflict body (one line each side), inside the `tasks_passed` tally just after `report.tasks_total = ...`:

```python
report.tasks_total = len(task_results) + len(report.remaining_task_ids)
<<<<<<< origin/master
    report.tasks_passed = sum(1 for r in task_results if r.status.is_success)
=======
    report.tasks_passed = sum(1 for r in task_results if r.status == TaskStatus.PASS)
>>>>>>> origin/feat/sprint-auto-resume-v435
    report.tasks_failed = sum(1 for r in task_results if r.status == TaskStatus.FAIL_TERMINAL)
```

**Resolution = TAKE MASTER:** `report.tasks_passed = sum(1 for r in task_results if r.status.is_success)`

**Why (verified against the auto-merged `models.py`):** `git show $TREE:src/superclaude/cli/sprint/models.py` keeps master's enum + property:

```
49:    PASS = "pass"
50:    PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success
57:    def is_success(self) -> bool:
58:        return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)
```

PR's strict `== TaskStatus.PASS` would **drop every PASS_RECOVERED task** from the passed-count breakdown (introduced by #126). `is_success` covers `{PASS, PASS_RECOVERED}`. Taking master keeps the count correct against the merged model. PR side here is stale — it predates #126's PASS_RECOVERED status landing on master.

---

## FILE 2 — commands.py (2 hunks) — RESOLUTION: UNION (with 1 inserted decorator line)

Conflict markers in `git show $TREE:src/superclaude/cli/sprint/commands.py`:

| Hunk | `<<<<<<<` | `=======` | `>>>>>>>` |
|---|---|---|---|
| 1 (decorators) | 191 | 211 | 235 |
| 2 (param list) | 255 | 259 | 262 |

### Hunk 1 (lines 191–235) — decorators on `run()` — CRITICAL SUBTLETY CONFIRMED

The shared `@click.option(` opener is at **line 190** (one line ABOVE `<<<<<<<` at 191). Master's first option consumes it:

```
190: @click.option(                         <- SHARED opener (above the marker)
191: <<<<<<< origin/master
192:     "--handoff/--no-handoff",           <- master's first option uses line-190 opener
...  (master adds: --handoff/--no-handoff, --resume, --task-parallelism)
210: )                                       <- closes --task-parallelism
211: =======
212:     "--fresh",                           <- PR's first option, NO opener of its own
...  (PR adds: --fresh, --restart, --yes/-y, @click.pass_context)
234: @click.pass_context
235: >>>>>>> origin/feat/sprint-auto-resume-v435
236: def run(
```

PR's `"--fresh",` block (line 212) had its `@click.option(` opener consumed by master's side (the shared line 190). A **naive marker-strip orphans `"--fresh",`** — the `)` closing `--task-parallelism` is immediately followed by `"--fresh",` with no decorator.

**Correct resolution:** keep BOTH option groups; **insert one fresh `@click.option(` line immediately before the `"--fresh",` block** (i.e., between master's closing `)` of `--task-parallelism` and PR's `"--fresh",`). Keep `@click.pass_context` at the end of the union (just above `def run(`).

Resulting decorator order on `run()`:
`--handoff/--no-handoff` → `--resume` → `--task-parallelism` → **(inserted `@click.option(`)** → `--fresh` → `--restart` → `--yes/-y` → `@click.pass_context`.

#### COMPILE EVIDENCE (both ways, `uv run python -m py_compile`)

Built from `git show $TREE:.../commands.py`, markers stripped:

- **NAIVE union (markers stripped, both sides verbatim, NO inserted opener):**
  ```
  Sorry: IndentationError: unexpected indent (naive.py, line 210)
  NAIVE: COMPILE FAILED  (as predicted — orphaned "--fresh", block)
  ```
  Orphan point (naive.py lines 209–210):
  ```
      )                  <- closes --task-parallelism
      "--fresh",         <- orphaned, no @click.option( above it
  ```

- **CORRECT union (one `@click.option(` inserted before the `"--fresh",` block + param-list both-sides union):**
  ```
  CORRECT: COMPILE OK
  ```

### Hunk 2 (lines 255–262) — `def run(...)` param list — clean both-sides union

```python
    release_dir_override: Path | None,
    state_dir_override: Path | None,
<<<<<<< origin/master
    handoff_enabled: bool,
    resume_task_id: str,
    task_parallelism: int,
=======
    fresh: bool,
    assume_yes: bool,
>>>>>>> origin/feat/sprint-auto-resume-v435
):
```

**Resolution:** keep both param groups (simple concatenation; no insertion needed here).
Union params: `..., handoff_enabled: bool, resume_task_id: str, task_parallelism: int, fresh: bool, assume_yes: bool`.
Note `ctx: click.Context` is already the **first** param of `run()` (master had `@click.pass_context`/`ctx` on the base def; the auto-merge kept `ctx` at the top — confirmed in the merged blob, `def run(\n    ctx: click.Context,\n    index_path: Path, ...`), so `@click.pass_context` from PR's side maps onto the existing `ctx` param. No duplicate `ctx`.

### `run()` BODY auto-merged coherently (verified in merged blob)

- PR's auto-resume block lands ABOVE master's `load_sprint_config(...)` call:
  - line 283 `from .config import load_sprint_config`
  - line 288 Click `ParameterSource` comment (explicit `--start 1` bypasses auto-resume)
  - line 299 `if fresh:` ; line 307 `_auto_resume(index_path, assume_yes=..., dry_run=...)`
  - line 330 `_dispatch_resume_rerun(index_path, plan)` ; line 334 phase-window narrowing
  - line 342 `config = load_sprint_config(` receiving line 356 `handoff_enabled=`, 357 `resume_task_id=`, 358 `task_parallelism=`
- Both feature sets coexist; no conflict in the body region (auto-merged clean).

### `_dispatch_resume_rerun` → `run_rerun_tasks` signature match (verified)

- Merged `_dispatch_resume_rerun` (line 514) calls `run_rerun_tasks(config, phase=..., tasks=..., from_reflect_report=None, ...)` (line 520).
- `def run_rerun_tasks(...)` is **BYTE-IDENTICAL on both branches**:
  ```
  diff <(git show origin/master:.../rerun_tasks.py | grep -A15 "^def run_rerun_tasks") \
       <(git show origin/feat/sprint-auto-resume-v435:.../rerun_tasks.py | grep -A15 "^def run_rerun_tasks")
  ==> BYTE-IDENTICAL  (params: config, *, phase, tasks, from_reflect_report, merge_back,
       dry_run, include_transitive, ignore_deps, force_merge, allow_loop,
       no_verify_checkpoints, bundle_dir, restore) -> int
  ```
  (A raw `grep -n` diff showed line-number prefixes 1205 vs 1244 only — the body is identical.)

---

## Auto-merged-clean corroboration

| File | Markers | Notes |
|---|---|---|
| `pyproject.toml` | 0 | merged `version = "4.3.5"` |
| `models.py` | 0 | keeps master `is_success = {PASS, PASS_RECOVERED}` (lines 49,50,57,58) |
| `rerun_tasks.py` | 0 | `run_rerun_tasks` sig identical both branches |
| `tests/sprint/test_executor.py` | 0 | COMPILE OK, no duplicate `def test_` names |
| `tests/sprint/test_cli_contract.py` | 0 | COMPILE OK, no duplicate `def test_` names |

---

## Summary

Three conflicted files; resolutions all verified with evidence (TREE OID `a53db586640dc2bb2753e585862108ed737fd529`):

1. **CHANGELOG.md** (1 hunk, lines 7/25/55) — **KEEP BOTH** `###` sections under `## [Unreleased]` (master "Sprint CLI — wire the per-task execution path..." first, then PR "sprint — auto-resume as the default..."). No content edits.

2. **commands.py** (2 hunks) —
   - Hunk 1 (191/211/235, decorators): **UNION + INSERT ONE `@click.option(` line** immediately before PR's `"--fresh",` block. PROVEN: naive marker-strip → `IndentationError (line 210)`; corrected union → `COMPILE OK`. Final decorator order: `--handoff/--no-handoff, --resume, --task-parallelism, (inserted opener), --fresh, --restart, --yes/-y, @click.pass_context`.
   - Hunk 2 (255/259/262, param list): **UNION** (plain concatenation) → `handoff_enabled, resume_task_id, task_parallelism, fresh, assume_yes` (+ existing leading `ctx`).
   - Body auto-merged coherently (auto-resume block above `load_sprint_config`); `_dispatch_resume_rerun` calls the byte-identical `run_rerun_tasks`.

3. **executor.py** (1 hunk, lines 354/356/358) — **TAKE MASTER**: `report.tasks_passed = sum(1 for r in task_results if r.status.is_success)`. PR's `== TaskStatus.PASS` would drop PASS_RECOVERED tasks; merged `models.py` keeps `is_success = {PASS, PASS_RECOVERED}`.

Auto-merged clean and verified: `pyproject.toml` (v4.3.5), `models.py`, `rerun_tasks.py`, `test_executor.py`, `test_cli_contract.py` (all 0 markers; tests compile with no duplicate test names).

Status: Complete
