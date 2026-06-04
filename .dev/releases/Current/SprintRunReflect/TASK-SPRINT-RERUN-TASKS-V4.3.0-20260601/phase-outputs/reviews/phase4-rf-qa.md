# QA Report — Task Integrity (Phase 4 Integration Edits)

**Phase:** 4 (Integration Edits — CLI + Executor + Logging + Checkpoints)
**Date:** 2026-06-02
**qa_phase:** task-integrity
**Fix authorization:** true (fix ALL findings in-place in worktree source)
**Stance:** ADVERSARIAL — assume errors; verify every claim against actual source.

Worktree source files under verification:
- `src/superclaude/cli/sprint/commands.py`
- `src/superclaude/cli/sprint/executor.py`
- `src/superclaude/cli/sprint/logging_.py`
- `src/superclaude/cli/sprint/checkpoints.py`

(All paths rooted at `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/`.)

---

## Criterion 1 — Click decorator stack (commands.py rerun-tasks)

**Contract (researcher 2 §2.1):** `path_type=Path` on path options; `is_flag=True` on boolean flags; every `help=` string ends in a period.

**Found (read `commands.py:419-541`):**
- `path_type=Path` present on: `index_path` arg (`:420`), `--from-reflect-report` (`:435`), `--bundle-dir` (`:476`). All three path-typed surfaces carry it.
- `is_flag=True` present on all 7 boolean flags: `--dry-run` (`:446`), `--include-transitive` (`:451`), `--ignore-deps` (`:456`), `--force-merge` (`:461`), `--allow-loop` (`:466`), `--no-verify-checkpoints` (`:471`), `--restore` (`:482`). `--merge-back/--no-merge-back` is correctly a boolean toggle pair (`default=True`, `:440-442`), not `is_flag` — that is the correct Click idiom for paired flags.
- Help strings all end with a period — verified each of the 12 `help=` lines (`:425, 431, 437, 442, 447, 452, 457, 462, 467, 472, 478, 483`).
- `Optional` and `Path` both imported (`commands.py:10-11`).
- Block placed AFTER `verify_checkpoints` command (ends `:416`) and BEFORE `_print_checkpoint_table` (`:544`) — decorators stay contiguous per Step 4.1.

**Result: PASS.**

---

## Criterion 2 — Exactly the 12 options (TDD line 184)

**Contract:** Exactly these 12: `--phase`, `--tasks`, `--from-reflect-report`, `--merge-back/--no-merge-back`, `--dry-run`, `--include-transitive`, `--ignore-deps`, `--force-merge`, `--allow-loop`, `--no-verify-checkpoints`, `--bundle-dir`, `--restore`. None missing, none extra.

**Found (read `commands.py:421-484` decorators + `:485-499` signature):**
1. `--phase` (`:421` int) · 2. `--tasks` (`:427` str) · 3. `--from-reflect-report` (`:433` Path) · 4. `--merge-back/--no-merge-back` (`:439` bool default True) · 5. `--dry-run` (`:444`) · 6. `--include-transitive` (`:449`) · 7. `--ignore-deps` (`:454`) · 8. `--force-merge` (`:459`) · 9. `--allow-loop` (`:464`) · 10. `--no-verify-checkpoints` (`:469`) · 11. `--bundle-dir` (`:474` Path) · 12. `--restore` (`:480`).

Count = 12. None extra, none missing. The function signature (`:485-499`) has exactly the 13 params (`index_path` arg + 12 options) with matching `Optional[...]` types on the four nullable ones (`phase`, `tasks`, `from_reflect_report`, `bundle_dir`). All 12 plumbed into the `run_rerun_tasks(...)` call (`:526-540`) by keyword.

**Result: PASS.**

---

## Criterion 3 — Mutex enforcement (researcher 2 §2.2)

**Contract:** `--tasks`/`--phase` vs `--from-reflect-report` mutual exclusion via `click.ClickException`; missing-required via `click.UsageError`. Logic must be reachable and correct. (Criterion text also mentions "`--restore` exclusivity".)

**Found (read `commands.py:515-522`):**
```python
if from_reflect_report and (phase or tasks):
    raise click.ClickException(
        "--from-reflect-report is mutually exclusive with --phase / --tasks"
    )
if not from_reflect_report and not phase:
    raise click.UsageError(
        "--phase is required when --from-reflect-report is not used"
    )
```
- Mutex uses `click.ClickException` (behavioral conflict) — correct per §2.2.
- Missing-required uses `click.UsageError` — correct per §2.2.
- Reachability: both branches sit at the TOP of the body, before `tasks.split()` and `load_sprint_config()`, so they always run before any side effect. Reachable and correctly ordered.
- The error messages match the TDD CLI-shape contract ("`--phase + --tasks` is mutually exclusive with `--from-reflect-report`", TDD line ~196).

**`--restore` exclusivity:** The verification criterion mentions "`--restore` exclusivity", but neither the authoritative TDD (`merged-requirements.md` lines 183-201 CLI shape) nor task Step 4.1 specify any `--restore` mutex. The TDD shows `--restore` as a plain optional flag in the `--phase` form. Absence of a `--restore` mutex is therefore NOT a contract violation — the criterion mention is speculative beyond the spec. No finding.

**MINOR observation (not a FAIL):** `not phase` treats `--phase 0` as "missing" because `0` is falsy. Sprint phases are 1-indexed (the task itself uses Phase 1…6; phase 0 is not a valid sprint phase), so this cannot misfire on any real input. Documented for completeness; no fix applied because changing to `phase is None` would be a behavior change outside Phase 4 scope and the spec defines no phase-0 case.

**Result: PASS.**

---

## Criterion 4 — Classification ladder + `_is_transient_failure` (IP-9, TDD §T6)

**Contract:** The `_is_transient_failure(...) → FAIL_RECOVERABLE` branch is inserted BEFORE the `FAIL_TERMINAL` else (transient classified recoverable first). `_is_transient_failure()` implements the TDD §T6 heuristic: `api_retry` / `ConnectionRefused` / (`output_tokens==0` with `is_error: true`).

**Found (read `executor.py:1016-1023`):**
```python
if exit_code == 0:
    status = TaskStatus.PASS
elif exit_code == 124:
    status = TaskStatus.INCOMPLETE
elif _is_transient_failure(config.task_output_file(phase, task)):
    status = TaskStatus.FAIL_RECOVERABLE
else:
    status = TaskStatus.FAIL_TERMINAL
```
- Ordering correct: `FAIL_RECOVERABLE` branch (`:1020-1021`) precedes the `else: FAIL_TERMINAL` (`:1022-1023`), so transient takes precedence. `INCOMPLETE` (exit 124) is untouched per TDD line 126.

**Heuristic (read `executor.py:1782-1804`):**
- `text = output_path.read_text(errors="replace")` guarded by `try/except OSError: return False` (`:1789-1792`) — graceful degrade per §1.5.
- `if "api_retry" in text or "ConnectionRefused" in text: return True` (`:1793-1794`) — covers triggers 1+2.
- Final non-blank line parsed via `json.loads`; returns `bool(obj.get("is_error") and obj.get("output_tokens", 1) == 0)` (`:1795-1803`) — covers trigger 3. Default `output_tokens=1` ensures a missing key does NOT falsely classify recoverable. JSON parse error → `return False` (terminal), correct conservative default.

All three TDD §T6 triggers implemented exactly. Helper placed near `_classify_from_result_file` (`:1807`) per IP-9 placement.

**Result: PASS.**

---

## Criterion 5 — `_write_phase_result_json` ordering + atomicity (IP-8)

**Contract:** The JSON write fires BEFORE `notify_phase_complete` at BOTH the per-task and claude-mode sites, and the write is atomic (tmp + `Path.replace`).

**Found — claude-mode site (read `executor.py:1609-1613`):**
```python
logger.write_phase_result(phase_result)
# v4.3.0-T06: persist phase result as JSON for rerun-tasks consumption
_write_phase_result_json(config, phase, phase_result)
notify_phase_complete(phase_result)
```
Ordering: `write_phase_result` (`:1610`) → JSON write (`:1612`) → `notify_phase_complete` (`:1613`). The JSON write is strictly BEFORE notify. PASS at this site.

**Found — per-task site (read `executor.py:1283-1307`):**
```python
phase_result = PhaseResult(..., task_results=task_results)   # :1289 — IP-6 kwarg present
phase_result = run_post_phase_wiring_hook(...)               # :1293
sprint_result.phase_results.append(phase_result)            # :1301
logger.write_phase_result(phase_result)                      # :1302
_write_phase_result_json(config, phase, phase_result)        # :1304
tui.update(...)                                              # :1306
continue                                                     # :1307
```
The per-task path does **not** call `notify_phase_complete` at all (grep across the whole file confirms `notify_phase_complete` appears only once, at `:1613` claude-mode). The "before notify" invariant is therefore **vacuously satisfied** for the per-task path — there is no notify to precede, and the JSON write still correctly follows `write_phase_result`. The IP-6 `task_results=task_results` kwarg is present (`:1289`) plumbing the real `execute_phase_tasks` return (`:1270`) into the field. No finding — this matches IP-8's intent (the artifact exists before any external observer can see phase completion), and IP-8's "both sites" wording is satisfied because only one site has a notify and that site is correctly ordered.

**Atomicity (read `executor.py:2053-2072`):**
```python
out = config.phase_result_json(phase)
out.parent.mkdir(parents=True, exist_ok=True)
tmp = out.with_suffix(".json.tmp")
tmp.write_text(json.dumps(payload, indent=2) + "\n")
tmp.replace(out)
```
- `mkdir(parents=True, exist_ok=True)` defensive (`:2069`).
- Atomic tmp-write + `Path.replace` (`:2070-2072`) — matches checkpoints.py §1.6.
- Trailing newline on JSON (`:2071`).
- Payload serializes `task_results` via `tr.to_dict()` (Step 1.7 method) and uses `config.phase_result_json` (Step 1.8 helper) — both cross-references resolve.

**Result: PASS.**

---

## Criterion 6 — logging_.py emitters use `_jsonl` + UTC timestamps (IP-12)

**Contract:** `write_phase_rerun_start`, `write_task_rerun_complete`, `write_phase_rerun_complete` each use the `_jsonl` helper EXACTLY as sibling emitters, and stamp `datetime.now(timezone.utc).isoformat()`.

**Found (read `logging_.py:159-267`):**
- All three emitters sit BETWEEN `write_checkpoint_verification` (`:159`) and `write_summary` (`:245`), per IP-12 ordering.
- `write_phase_rerun_start` (`:190-203`): `self._jsonl({...})`, event `phase_rerun_start`, fields `phase/tasks(list())/bundle/source_sha/timestamp`.
- `write_task_rerun_complete` (`:205-219`): `self._jsonl({...})`, event `task_rerun_complete`, fields `phase/task_id/status/turns/duration_sec/timestamp`.
- `write_phase_rerun_complete` (`:221-243`): keyword-only collection args via `*` separator (`:226`), event `phase_rerun_complete`, fields `phase/status/bundle/tasks_rerun/tasks_passed/tasks_failed/timestamp`, each collection wrapped in `list(...)`.
- All three event names match TDD lines 93-95 verbatim (`phase_rerun_start`, `task_rerun_complete`, `phase_rerun_complete`).
- All three stamp `datetime.now(timezone.utc).isoformat()` (`:201, 217, 241`) — identical to the sibling `write_checkpoint_verification` timestamp (`:186`).
- `self._jsonl` invoked identically to the sibling pattern; `_jsonl` helper (`:265-267`) unchanged (`json.dumps(data, default=str) + "\n"` append).

**Result: PASS.**

---

## Criterion 7 — checkpoints.py `return_bundle` wrap (IP-11)

**Contract:** A keyword-only `return_bundle: bool = False` param wraps the return in a `RecoveryBundle` only when True; default preserves the original list-return for back-compat. Lazy import avoids cycles; `TYPE_CHECKING` guard correct.

**Found (read `checkpoints.py:9, 15, 19-20, 213-321`):**
- Signature: `def recover_missing_checkpoints(manifest, artifacts_dir, phase_tasklists, *, return_bundle: bool = False) -> list[CheckpointEntry] | RecoveryBundle:` (`:213-219`). Keyword-only flag via `*` separator (`:217`). Union return annotation (`:219`).
- `from __future__ import annotations` (`:9`) is present → the union annotation is a string at runtime, so the `RecoveryBundle` reference does not require a runtime import.
- `TYPE_CHECKING` guard correct: `from typing import TYPE_CHECKING` (`:15`); `if TYPE_CHECKING: from .recovery import RecoveryBundle` (`:19-20`) — supplies the name for static analysis only, no runtime import, no cycle.
- Default path: returns `out` (the `list[CheckpointEntry]`) unchanged at `:321` — byte-identical to v4.2.x, back-compat preserved per IP-11 invariant.
- `return_bundle=True` branch (`:301-319`): lazy function-local `from .recovery import RecoveryBundle, RecoveryStatus` (`:305`) WITH the cycle-avoidance comment (`:302-304`), breaking the `recovery → models → checkpoints → recovery` cycle per §1.7.
- **Adversarial cross-check of bundle kwargs:** All 10 constructor kwargs (`:308-319`) verified against the real `RecoveryBundle` dataclass (`recovery.py:105-114`): `bundle_id, affected_phase, verb, affected_tasks, artifacts_produced, artifacts_replaced, source_tasklist_sha256, end_tasklist_sha256, status, rerun_attempt` — all field names exist, no fabricated kwarg. `RecoveryStatus.SUCCESS`/`.PARTIAL` both exist (`recovery.py:61-62`). `affected_phase=out[0].phase if out else 0` guards empty list. `status=SUCCESS if all_recovered else PARTIAL` matches TDD §T9 semantics.

**Result: PASS.**

---

## Criterion 8 — Atomic writes across the 4 files (researcher 2 §1.6)

**Contract:** All NEW file writes use tmp-write + atomic rename.

**Found:**
- `executor.py:2068-2072` (`_write_phase_result_json`) — the only new full-file write across the 4 files. Uses `out.with_suffix(".json.tmp")` → `tmp.write_text(...)` → `tmp.replace(out)`, with `mkdir(parents=True, exist_ok=True)`. Atomic. PASS.
- `logging_.py` emitters append a single JSON line via the pre-existing `_jsonl` helper (`:265-267`, open-append + write). This is the established sibling JSONL-append convention (`write_header`, `write_phase_result`, `write_checkpoint_verification` all use it); JSONL append is intentionally NOT a tmp-rename full-file write — it matches §1.6's per-line append idiom, not the manifest-write idiom. No new file write introduced; consistent with siblings. No finding.
- `commands.py` rerun-tasks block creates NO file writes (delegates to `run_rerun_tasks`). N/A.
- `checkpoints.py` `return_bundle` branch performs NO new file write (the existing recovery write at `:276-277` is pre-Phase-4 and unchanged). N/A.

**Result: PASS.**

---

## Criterion 9 — Lazy imports avoid cycles + import smoke check (researcher 2 §1.7)

**Contract:** All new cross-module imports that could create cycles are function-local; `uv run python -c "from superclaude.cli.sprint import checkpoints, commands, executor, logging_, recovery, rerun_tasks"` must succeed with no ImportError.

**Found:**
- `commands.py:512-513` — `from .config import load_sprint_config` and `from .rerun_tasks import run_rerun_tasks` are function-LOCAL (inside the `rerun_tasks` command body), per §2.2 universal-in-file convention. Avoids importing `rerun_tasks` (heavy, depends on recovery/executor) at module load.
- `checkpoints.py:305` — `from .recovery import RecoveryBundle, RecoveryStatus` is function-local inside the `return_bundle` branch, with the explicit cycle comment; the module-level reference is TYPE_CHECKING-only (`:19-20`). Breaks the `recovery → models → checkpoints → recovery` cycle.
- `executor.py` Phase 4 edits introduced NO new module-level cross-module import (`_write_phase_result_json`/`_is_transient_failure` reuse pre-existing `json`, `Path`, `SprintConfig`, `Phase`, `PhaseResult`, and the pre-existing `notify_phase_complete` import at `:39`).
- **Import smoke check (Bash, executed):** `uv run python -c "from superclaude.cli.sprint import checkpoints, commands, executor, logging_, recovery, rerun_tasks; print('IMPORT_OK')"` → output `IMPORT_OK`. No ImportError, no circular-import regression.
- **Lint (Bash, executed):** `uv run ruff check` over all 4 files → `All checks passed!` (exit 0).

**Result: PASS.**

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Click decorator stack (path_type/is_flag/period) | PASS | Read `commands.py:419-541` |
| 2 | Exactly 12 options | PASS | Read `commands.py:421-499` |
| 3 | Mutex enforcement (ClickException/UsageError, reachable) | PASS | Read `commands.py:515-522` |
| 4 | Classification ladder + `_is_transient_failure` (§T6) | PASS | Read `executor.py:1016-1023, 1782-1804` |
| 5 | `_write_phase_result_json` ordering + atomicity | PASS | Read `executor.py:1283-1307, 1609-1613, 2053-2072` |
| 6 | logging_.py emitters (`_jsonl` + UTC) | PASS | Read `logging_.py:159-267` |
| 7 | checkpoints.py `return_bundle` wrap + lazy/TYPE_CHECKING | PASS | Read `checkpoints.py:9,15,19-20,213-321` + `recovery.py:58-114` |
| 8 | Atomic writes across 4 files | PASS | `executor.py:2068-2072`; logging append idiom; commands/checkpoints N/A |
| 9 | Lazy imports + import smoke + lint | PASS | Bash: `IMPORT_OK`; `All checks passed!` |

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 | Grep: 0 | Glob: 0 | Bash: 5 (3 grep-via-bash, 2 verification: import smoke + ruff)
  - (No web research performed — all claims are local source-truth; tavily/web-fallback counts: 0.)
- All 9 criteria categorized VERIFIED with cited tool output. No UNCHECKED, no UNVERIFIABLE items.
- Tool-engagement minimum met: combined Read + grep-Bash calls (12 + 3 = 15) ≥ 9 checklist items.

## Fixes Applied

**None required.** All 9 criteria passed on first verification against the actual worktree source. No edits were made to any source file. Lint (`ruff check`) and the import smoke check were already clean and were re-confirmed by this QA pass, not changed by it.

## Summary

- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0
- MINOR observations (non-blocking, no fix warranted): 1 (`--phase 0` falsy edge in mutex — not reachable for valid 1-indexed sprint phases; out-of-scope to change in Phase 4).

## Adversarial self-audit

If I told the user I found 0 issues, would they believe me? Evidence I can cite: I read all four target files at the exact line ranges (commands.py 419-541, executor.py 1016-1023 / 1283-1307 / 1609-1613 / 1782-1804 / 2053-2072, logging_.py 159-267, checkpoints.py 213-321), independently cross-verified the `RecoveryBundle` constructor kwargs against the real dataclass in recovery.py (not trusting the aggregation), confirmed `notify_phase_complete` appears only once in executor.py via grep, and executed the import smoke check + ruff myself rather than trusting the aggregation's claim. The one place the criterion over-specified (per-task `notify_phase_complete`, `--restore` exclusivity) I traced to the authoritative TDD and confirmed the criterion was speculative beyond spec, not a real gap.

---

VERDICT: PASS
