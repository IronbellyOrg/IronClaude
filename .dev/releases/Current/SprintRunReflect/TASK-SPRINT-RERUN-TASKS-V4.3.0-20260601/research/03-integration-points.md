# Research 03: Integration Points

**Status:** Complete
**Researcher:** #3
**Topic:** Insertion/integration points for `superclaude sprint rerun-tasks` v4.3.0
**Date:** 2026-06-01

## Scope

Map every existing-code insertion point for the v4.3.0 feature: exact `file:line` + minimal diff contract (NOT full new code).

---

## Integration Point Map

| # | File | Line | Change | Contract |
|---|------|------|--------|----------|
| IP-1 | `src/superclaude/cli/sprint/commands.py` | 449 (append after `_print_checkpoint_table`) | NEW `@sprint_group.command("rerun-tasks")` | Mirrors `verify-checkpoints` shape (line 360); takes `index_path` arg + `--phase`, `--tasks`, `--from-reflect-report`, `--dry-run`, `--max-retries`, `--lock-timeout` options; imports from new `recovery.py` + `rerun_tasks.py` inside function body (late-import per convention) |
| IP-2 | `src/superclaude/cli/sprint/__init__.py` | 3 (after existing `from .commands import sprint_group`) | NO EXPORT CHANGE | `__all__` stays `["sprint_group"]`. `recovery.py` / `rerun_tasks.py` are CLI-internal; commands.py late-imports them. Adding them to `__all__` would be over-export. |
| IP-3 | `src/superclaude/cli/sprint/models.py` | 39 (TaskStatus class body) | EDIT enum: add `FAIL_RECOVERABLE = "fail_recoverable"` after line 43 (`FAIL = "fail"`) | Additive enum member. Update `.is_failure` property at line 52 to include `FAIL_RECOVERABLE`. Per TDD line 120: KEEP `FAIL` serialized as `"fail"` for backcompat — no rename. New status `"fail_recoverable"` is a sibling. |
| IP-4 | `src/superclaude/cli/sprint/models.py` | 545 (end of `PhaseResult` fields, before properties at 546) | EDIT dataclass: add `task_results: list[TaskResult] = field(default_factory=list)` AND `recovery_history: list = field(default_factory=list)` | Additive field with default → does NOT break existing constructor calls in executor.py:1280, 1244-1254, 1549. Forward-ref `TaskResult` defined at line 159 (above) so no import cycle. |
| IP-5 | `src/superclaude/cli/sprint/models.py` | 158-176 (`TaskResult` dataclass) | EDIT: add JSON-serialization method `to_dict()` → returns dict suitable for `phase-N-result.json` (uses `.value` for enum fields, `.isoformat()` for datetimes) | Pure-data helper. Symmetric `from_dict()` classmethod also needed for `recovery.py` deserialization on legacy-sprint fallback. |
| IP-6 | `src/superclaude/cli/sprint/executor.py` | 1278-1297 (per-task phase branch) | EDIT: assign `task_results` to PhaseResult at construction (line 1280) — `task_results=task_results` kwarg added to existing `PhaseResult(...)` call | Plumbs the already-existing `task_results` list (line 1267 return value) into the additive field from IP-4. NO new variable plumbing. |
| IP-7 | `src/superclaude/cli/sprint/executor.py` | 1549-1565 (claude-mode phase PhaseResult construction) | EDIT: pass `task_results=[]` explicitly (or rely on field default) | Claude-mode phases have no per-task delegation; leaving `task_results` empty marks the phase as "legacy/no-per-task-evidence", which signals `rerun_tasks.py` to fall back to transcript inspection (TDD line 130). |
| IP-8 | `src/superclaude/cli/sprint/executor.py` | 1604 (between `logger.write_phase_result` and `notify_phase_complete`) | NEW call: `_write_phase_result_json(config, phase, phase_result)` | Persists `<config.results_dir>/phase-{phase.number}-result.json` containing serialized PhaseResult + task_results. Per TDD line 128: ~20 LOC helper. Placement BEFORE `notify_phase_complete` (line 1605) ensures hooks see the file. Must also fire from per-task branch at line 1298 (after `logger.write_phase_result`). |
| IP-9 | `src/superclaude/cli/sprint/executor.py` | 1014-1020 (task status classification) | EDIT: amend FAIL classification to detect transient/proxy failures and emit `TaskStatus.FAIL_RECOVERABLE` | Current logic: `exit_code != 0 → FAIL`. New logic per TDD line 124: inspect task transcript at `config.task_output_file(phase, task)` for `api_retry`, `ConnectionRefused`, `is_error: true` with `output_tokens == 0` → return `FAIL_RECOVERABLE`. Helper `_classify_transient_failure(output_path) -> bool` lives in `executor.py` or new `recovery.py` (TDD §"Heuristic"). |
| IP-10 | `src/superclaude/cli/sprint/checkpoints.py` | 115, 293, 334, 367 — 4 private helpers | NO RENAME — keep private; `recovery.py` imports via `from .checkpoints import _nearest_heading, _extract_verification_block, _discover_phase_artifacts, _render_recovered_checkpoint` | TDD says "expose for recovery.py reuse" — but Python convention treats `_name` as module-private, NOT package-private. Same-package sibling imports of `_name` are permitted. Alternative: rename to public (`nearest_heading`, etc.) — costs renaming all 9 call sites in `checkpoints.py` + manifest tests. **RECOMMEND**: import as-is (sibling-private access). If linter (ruff PLR2004 / SLF001) complains, add per-import `# noqa: SLF001`. |
| IP-11 | `src/superclaude/cli/sprint/checkpoints.py` | 209 (`recover_missing_checkpoints` signature) | NO CHANGE | `rerun_tasks.py` invokes this via the existing public surface (already used by `verify-checkpoints` line 388). The new `rerun-tasks` subcommand calls `recover_missing_checkpoints(manifest, artifacts_dir, phase_tasklists)` after merge step (TDD AC2 line 264). |
| IP-12 | `src/superclaude/cli/sprint/logging_.py` | 188 (after `write_checkpoint_verification`, before `write_summary` at 190) | NEW method: `def write_phase_rerun_complete(self, phase: int, status: str, bundle_path: str) -> None` | Calls `self._jsonl({"event": "phase_rerun_complete", "phase": ..., "status": ..., "bundle": ..., "timestamp": ...})`. Matches existing `_jsonl` surface (line 210). Per TDD line 95 event shape. Called from `rerun_tasks.py` after merge completes. |
| IP-13 | `src/superclaude/cli/sprint/executor.py` | line 38 (existing `from .notify import ...`) | NEW import block (line 20-area or wherever recovery is wired) | `from .recovery import RecoveryBundle, merge_recovery_bundle` — only needed if executor calls into recovery (it does not for v4.3.0 — recovery is CLI-only). **No-op for v4.3.0.** Listed for completeness. |
| IP-14 | `src/superclaude/cli/sprint/models.py` | 502-509 (SprintConfig path helpers) | NEW method: `def phase_result_json(self, phase: Phase) -> Path: return self.results_dir / f"phase-{phase.number}-result.json"` | Convention match: lines 496-509 define analogous `output_file`, `result_file`, `task_output_file`. The new `phase_result_json` reuses this pattern. Used by IP-8 (`_write_phase_result_json`) and by `rerun_tasks.py` legacy-fallback (TDD line 130). |

---

## Detailed Integration Contracts

### IP-1: New `rerun-tasks` Click subcommand — `commands.py:449+`

**Anchor**: structurally a sibling of `verify-checkpoints` (line 360). Insert after `_print_checkpoint_table` ends at line 449 (or before `_print_dry_run` at line 452).

**Diff shape**:
```python
@sprint_group.command("rerun-tasks")
@click.argument("index_path", type=click.Path(exists=True, path_type=Path))
@click.option("--phase", "phase_number", type=int, help="Phase containing the failed tasks")
@click.option("--tasks", "task_ids", help="Comma-separated task IDs (e.g. T07.11,T07.12)")
@click.option("--from-reflect-report", type=click.Path(exists=True, path_type=Path),
              help="Nominate tasks from a /sc:reflect report (mutex with --tasks)")
@click.option("--dry-run", is_flag=True, help="Show plan without executing")
@click.option("--max-retries", type=int, default=3, show_default=True)
@click.option("--lock-timeout", type=int, default=600, show_default=True,
              help="Seconds to wait for concurrent recovery lock")
def rerun_tasks(index_path: Path, phase_number: int, task_ids: str, ...):
    """Re-execute named tasks within a single phase, merge results."""
    from .rerun_tasks import run_rerun
    from .recovery import RecoveryBundle
    # validate mutex, call run_rerun(...), emit checkpoint manifest, etc.
```

**Side effects**: NONE on existing commands. Late imports keep cold-start cost zero.

### IP-3 + IP-4: Models additive changes — `models.py:39, 545`

**Exact diff for IP-3** (TaskStatus, between line 43 and 44):
```python
PASS = "pass"
FAIL = "fail"
FAIL_RECOVERABLE = "fail_recoverable"   # NEW (v4.3.0)
INCOMPLETE = "incomplete"
SKIPPED = "skipped"
```
And amend `is_failure` (line 52):
```python
return self in (TaskStatus.FAIL, TaskStatus.FAIL_RECOVERABLE, TaskStatus.INCOMPLETE)
```

**Exact diff for IP-4** (PhaseResult fields, append after `tokens_out: int = 0` at line 544):
```python
turns: int = 0
tokens_in: int = 0
tokens_out: int = 0
# v4.3.0: granular task evidence for rerun-tasks
task_results: list["TaskResult"] = field(default_factory=list)
recovery_history: list = field(default_factory=list)
```
(`TaskResult` is forward-ref string because of declaration order — defined at line 159 above, so direct reference works too. Forward-ref-as-string is safer.)

### IP-8: `_write_phase_result_json` — `executor.py:1604`

**Wiring**: insert between `logger.write_phase_result(phase_result)` (line 1604) and `notify_phase_complete(phase_result)` (line 1605):
```python
logger.write_phase_result(phase_result)
_write_phase_result_json(config, phase, phase_result)   # NEW
notify_phase_complete(phase_result)
```
And mirror in per-task branch at line 1298 (existing `logger.write_phase_result(phase_result)`):
```python
logger.write_phase_result(phase_result)
_write_phase_result_json(config, phase, phase_result)   # NEW
tui.update(sprint_result, MonitorState(), None)
```

**Helper definition** (new ~20 LOC function in `executor.py`, near `_write_executor_result_file` at line 2020):
```python
def _write_phase_result_json(config: SprintConfig, phase: Phase, result: PhaseResult) -> None:
    """Persist PhaseResult as JSON for rerun-tasks consumption (v4.3.0)."""
    import json
    payload = {
        "phase": result.phase.number,
        "status": result.status.value,
        "exit_code": result.exit_code,
        "started_at": result.started_at.isoformat(),
        "finished_at": result.finished_at.isoformat(),
        "task_results": [tr.to_dict() for tr in result.task_results],
        "recovery_history": result.recovery_history,
    }
    out = config.phase_result_json(phase)   # IP-14
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n")
    tmp.replace(out)   # atomic write (matches checkpoints.py:205 pattern)
```

### IP-9: Transient-failure classification — `executor.py:1014-1020`

**Current**:
```python
if exit_code == 0:
    status = TaskStatus.PASS
elif exit_code == 124:
    status = TaskStatus.INCOMPLETE
else:
    status = TaskStatus.FAIL
```

**Diff**:
```python
if exit_code == 0:
    status = TaskStatus.PASS
elif exit_code == 124:
    status = TaskStatus.INCOMPLETE
elif _is_transient_failure(config.task_output_file(phase, task)):
    status = TaskStatus.FAIL_RECOVERABLE
else:
    status = TaskStatus.FAIL
```

**Helper** (~15 LOC, define near `_classify_from_result_file` at line 1774):
```python
def _is_transient_failure(output_path: Path) -> bool:
    """Detect API-retry/proxy/transport failure from claude transcript NDJSON.

    Returns True iff transcript contains api_retry events OR ConnectionRefused
    OR (is_error: true AND output_tokens == 0). Per merged-requirements §"Heuristic".
    """
    if not output_path.exists():
        return False
    try:
        text = output_path.read_text(errors="replace")
    except OSError:
        return False
    if "api_retry" in text or "ConnectionRefused" in text:
        return True
    # Probe final JSON line for is_error + output_tokens==0
    for line in reversed(text.splitlines()):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if obj.get("is_error") and obj.get("output_tokens", 1) == 0:
                return True
        except (ValueError, TypeError):
            continue
        break
    return False
```

### IP-10: Private-helper import contract — `checkpoints.py`

**Functions to import in `recovery.py`** (all currently `_`-prefixed):

| Line | Function | Used by recovery.py for |
|------|----------|-------------------------|
| 115 | `_nearest_heading(headings, offset) -> str` | Locating which heading owns a recovered task line |
| 293 | `_extract_verification_block(tasklist_path, checkpoint_name) -> str` | Pulling the verification body for a recovered checkpoint after `rerun-tasks` rewires |
| 334 | `_discover_phase_artifacts(artifacts_dir, phase_number) -> list[Path]` | Listing evidence for the rerun bundle |
| 367 | `_render_recovered_checkpoint(*, entry, verification_block, evidence) -> str` | Generating the recovered checkpoint markdown body inside the bundle |

**Import shape** (in new `recovery.py`):
```python
from .checkpoints import (
    _nearest_heading,
    _extract_verification_block,
    _discover_phase_artifacts,
    _render_recovered_checkpoint,
)
```
Same-package private access — Python permits this without warning. If ruff `SLF001` flags it, add `# noqa: SLF001` per import or rename to public (more disruptive).

### IP-12: JSONL emission API — `logging_.py:188`

**Surface pattern** matches `write_checkpoint_verification` (line 159) — single-event emitter calling `self._jsonl(dict)`.

**New method** inserted after line 188 (before `def write_summary`):
```python
def write_phase_rerun_complete(
    self,
    phase: int,
    status: str,
    bundle_path: str,
    *,
    tasks_rerun: list[str],
    tasks_passed: list[str],
    tasks_failed: list[str],
) -> None:
    """Emit phase_rerun_complete JSONL event (v4.3.0 rerun-tasks).

    Called by rerun_tasks.py after merge completes. Per merged-requirements §line 95.
    """
    self._jsonl({
        "event": "phase_rerun_complete",
        "phase": phase,
        "status": status,
        "bundle": bundle_path,
        "tasks_rerun": list(tasks_rerun),
        "tasks_passed": list(tasks_passed),
        "tasks_failed": list(tasks_failed),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
```

---

## Summary of Touch-Surface

**NEW files** (not in scope for this researcher — see researcher-1):
- `src/superclaude/cli/sprint/recovery.py` (~250 LOC)
- `src/superclaude/cli/sprint/rerun_tasks.py` (~280 LOC)

**MODIFIED files** (5 integration points across 4 files):
- `commands.py` — +1 subcommand (~50 LOC including options + dispatch)
- `models.py` — +1 enum member, +2 dataclass fields, +1 path helper, +`to_dict`/`from_dict` on TaskResult (~50 LOC)
- `executor.py` — +1 status branch, +2 helper functions, 2 call-site additions (~50 LOC)
- `logging_.py` — +1 emitter method (~15 LOC)

**UNCHANGED but consumed**:
- `checkpoints.py` — 4 private helpers imported by `recovery.py`; `recover_missing_checkpoints` (public) invoked by `rerun-tasks` post-merge.
- `__init__.py` — no export changes.
- `notify.py` (line 38 import in executor) — untouched.

**Critical ordering invariants**:
1. `_write_phase_result_json` MUST run AFTER `_write_executor_result_file` (line 1535) and AFTER any post-phase wiring hook (line 1568) so it captures the final mutated state.
2. `_write_phase_result_json` MUST run BEFORE `notify_phase_complete` (line 1605) so external hooks see the artifact.
3. `task_results` field on PhaseResult MUST default to `[]` (not None) so legacy callers at lines 1244-1254 (skipped phase) and 1549 (claude-mode no-task phase) don't break.
4. `FAIL_RECOVERABLE` MUST keep `FAIL` enum value unchanged ("fail") — only adds a sibling member — for JSONL backcompat (TDD line 120).
