# Research: run_cmd seam

**Status:** Complete
**Date:** 2026-06-18

File: `src/superclaude/cli/swarm/commands.py` (3538 lines, verified via `wc -l`).
All line numbers below are CURRENT (re-read 2026-06-18); the spec's numbers are stale.

---

## 8. Module-level constants (top of file)

- `commands.py:85` — `SWARM_STATE_FILENAME: str = ".swarm-state.json"`
- `commands.py:99` — `EXECUTION_LOG_JSONL_FILENAME: str = "execution-log.jsonl"`
- `commands.py:100` — `EXECUTION_LOG_MD_FILENAME: str = "execution-log.md"`
- `commands.py:188` — `EXIT_OK: int = 0`
- `commands.py:189` — `EXIT_INVALID: int = 1`
- `commands.py:190` — `EXIT_USAGE: int = 2`

Note: for the `--tui --detached` reject FR-3 D1 wants the SAME shape as the resume+detached reject, which uses `EXIT_USAGE` (see §3, §10). Both constants exist and are import-free at module scope (no deferred import needed).

The dual-format Logger doc comment at `commands.py:89-94` confirms `execution-log.jsonl` and `execution-log.md` are siblings of `manifest.json` inside the job's `--output` directory. `.swarm-state.json` lives in the SAME directory (see §7).

---

## 1. `@click.option` decorator block for `run_cmd`

- Command decorator: `commands.py:1299` — `@click.command("run")`
- Positional argument: `commands.py:1300-1309` — `@click.argument("spec_path", required=False, ...)`
- Options span: `commands.py:1310` (`--stdin`) through `commands.py:1469` (close of `--detached`).
- Guard decorator (LAST decorator before `def`): `commands.py:1470` — `@auto_inject_guard_option`

Option blocks in order:
- `--stdin` / `stdin_mode`: 1310-1316
- `--lens` / `lens`: 1317-1331
- `--resume` / `resume_job_id`: 1332-1350
- `--target` / `target_path`: 1351-1360
- `--output` / `output_dir`: 1361-1372
- `--transport` / `transport_kind`: 1373-1384
- `--reviewers` / `reviewers`: 1385-1397
- `--target-line-cap` / `target_line_cap`: 1398-1409
- `--timeout-sec` / `timeout_sec`: 1410-1421
- `--label` / `label`: 1422-1433
- `--force-relens` / `force_relens`: 1434-1451
- **`--detached` / `detached`: 1452-1469** (is_flag, default=False)

**INSERTION POINT for `--tui` option decorator:** the LAST `@click.option` block is `--detached` ending at `commands.py:1469`. Insert the new `@click.option("--tui", "tui", is_flag=True, default=False, ...)` decorator AFTER line 1469 and BEFORE `@auto_inject_guard_option` at line 1470. (Click option ordering only affects `--help` listing; placing `--tui` last among options, immediately before the guard decorator, is the cleanest insertion.)

---

## 2. `def run_cmd(...)` signature

- Signature start: `commands.py:1471` — `def run_cmd(`
- Parameters (1472-1485), return annotation 1486 `) -> None:`:
  - `spec_path: Optional[Path],` (1472)
  - `stdin_mode: bool,` (1473)
  - `lens: Optional[str],` (1474)
  - `resume_job_id: Optional[str],` (1475)
  - `target_path: Optional[Path],` (1476)
  - `output_dir: Optional[Path],` (1477)
  - `transport_kind: Optional[str],` (1478)
  - `reviewers: Optional[int],` (1479)
  - `target_line_cap: Optional[int],` (1480)
  - `timeout_sec: Optional[int],` (1481)
  - `label: Optional[str],` (1482)
  - `force_relens: bool,` (1483)
  - `detached: bool,` (1484)
  - `auto_inject_guard: bool,` (1485)

**INSERTION POINT for `tui` param:** add `tui: bool,` between `detached: bool,` (line 1484) and `auto_inject_guard: bool,` (line 1485). `auto_inject_guard` (injected by the `@auto_inject_guard_option` decorator) must remain last by convention — so `tui` goes immediately before it. Click matches options to params by name, but mirroring the decorator order (tui after detached) is clearest.

Docstring: `commands.py:1487-1521` (the `"""Run a swarm job..."""` block). The non-resume flow narrative is at 1506-1520. Add a `--tui` mention near step 4 (1515-1518): `--tui` renders a live progress dashboard while Wave 1 runs on a background thread; fresh-run only; mutually exclusive with `--detached`.

---

## 3. Resume branch + the `--resume`/`--detached` mutual-exclusion reject (FR-3 D1 literal mirror)

- Resume branch opens: `commands.py:1539` — `if resume_job_id is not None:`
- `--resume` vs SPEC_PATH/--stdin/--lens reject: 1540-1546
- **`--resume` vs `--detached` reject (the literal FR-3 D1 wants to mirror): `commands.py:1547-1553`:**

```python
        if detached:
            click.echo(
                "swarm run --resume: --resume is mutually exclusive with "
                "--detached (resume orchestrates its own pipeline inline)",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)
```

- `--output` required reject: 1554-1560
- `_run_resume_branch(...)` call: 1561-1566
- `return` (resume branch exit): `commands.py:1567`

This is the exact `click.echo(..., err=True)` + `raise click.exceptions.Exit(EXIT_USAGE)` shape FR-3 D1 wants the `--tui --detached` guard to mirror.

---

## 4. Fresh `--detached` branch (`if detached:`)

- Opens: `commands.py:1589` — `if detached:`
- Body: 1589-1607. Validates the spec is a dict (1590-1596), applies target/output/transport overrides onto the spec snapshot (1597-1602), stamps `runtime.mode = "detached"` (1605), calls `_launch_detached_run(...)` (1606), and **`return`s at `commands.py:1607`** before any preflight/dispatch.

CONFIRMED: the fresh `--detached` branch `return`s (1607) before `dispatch_wave1`. A `--tui --detached` guard MUST fire BEFORE this branch returns — best at the top of the non-resume flow (see §10), so the combination errors instead of silently launching detached and ignoring `--tui`.

The resume branch (line 1539) runs and `return`s (1567) before reaching line 1589, and already rejects `--detached`. Per TRACK GOAL v1 is fresh-run only, so the resume branch does not read `tui` (combination handling on resume is a task-design decision, not an FR requirement).

---

## 5. Fresh-run blocking `dispatch_wave1(...)` call — moves onto the worker thread

- Preceding `run_preflight(...)` call: `commands.py:1696-1701` (try/except PreflightError → EXIT_INVALID at 1707).
- Logger + state setup: 1721-1792 (see §7).
- **`dispatch_wave1(...)` call: `commands.py:1807-1813`** — EXACT verbatim keyword args:

```python
    worker_results = dispatch_wave1(
        preflight_result,
        transport_for_slot=run_transport_factory,
        prompt=assembled_prompt,
        worker_spec=inline_job.workers,
        logger=logger,
    )
```

Positional arg: `preflight_result`. Keyword args: `transport_for_slot=run_transport_factory`, `prompt=assembled_prompt`, `worker_spec=inline_job.workers`, `logger=logger`. The thread wrapper (Approach A) must call `dispatch_wave1` with these EXACT args unchanged (C3 no-signature-change). Result name to preserve: `worker_results`.

All inputs are computed BEFORE the call:
- `preflight_result` — from run_preflight (1697)
- `run_transport_factory` — built at 1771-1775
- `assembled_prompt` — built at 1803-1805
- `inline_job` — built at 1802 (`_from_dict(JobSpec, spec_dict)`)
- `logger` — built at 1732-1740 (or None)

So the background-thread wrapper is a closure capturing these five locals, assigning `worker_results` via a holder/result the join collects. Main thread runs the 2/s poll loop, joins, re-raises any worker BaseException AFTER `tui.stop()`, then proceeds to §6.

---

## 6. Post-dispatch continuation (consumes `worker_results`)

- First line after the dispatch call: comment block `commands.py:1815-1825`, then active code begins at:
- `commands.py:1826` — `recipe_name = inline_job.normalization.recipe`
- `commands.py:1827` — `if state_output_dir is not None and recipe_name:` — opens the normalize_wave2 → reduce_wave3 block (1828-1893).
  - `normalize_wave2(...)` call: 1848-1852
  - `reduce_wave3(...)` call: 1877-1893
- Terminal state flip: 1898-1903 (`_write_swarm_state(state_output_dir, "terminal", ...)`)
- Success echo: 1907-1911
- `raise click.exceptions.Exit(EXIT_OK)`: `commands.py:1912`

Everything from `commands.py:1826` onward must run AFTER the worker thread joins AND after any worker BaseException has been re-raised (so a failed dispatch never reaches normalize/reduce). The continuation reads `worker_results` at 1832 (`_stamp_inline_worker_paths(worker_results, ...)`) and 1910 (`results={len(worker_results)}`).

---

## 7. Logger + state setup; directory holding both log + state

- `state_output_dir: Optional[Path] = None` initialized: `commands.py:1726`
- Gate `if preflight_result.manifest_path:`: `commands.py:1727`
- `manifest_dir = Path(preflight_result.manifest_path).parent`: `commands.py:1730`
- `state_output_dir = manifest_dir`: `commands.py:1731`
- Logger construction (`_Logger(...)`): `commands.py:1732-1740`:
  - `jsonl_path=manifest_dir / "execution-log.jsonl"` (1733)
  - `md_path=manifest_dir / "execution-log.md"` (1734)
  - `output_dir=manifest_dir` (1739)
- `_write_swarm_state` calls (3 sites in the fresh path):
  - post-preflight `preflight_ok`: `commands.py:1745-1749`
  - pre-dispatch `dispatching`: `commands.py:1787-1792`
  - post-reduce `terminal`: `commands.py:1898-1903`

**Directory holding both `execution-log.jsonl` and `.swarm-state.json`:** `manifest_dir` = `Path(preflight_result.manifest_path).parent` (== `state_output_dir`, line 1731). `_write_swarm_state` writes to `output_dir / SWARM_STATE_FILENAME` (helper at `commands.py:692`, path built at `commands.py:722`). So both files are siblings of `manifest.json` in `state_output_dir`. The TUI poll loop tails `state_output_dir / "execution-log.jsonl"` and reads `state_output_dir / ".swarm-state.json"` — the SAME `state_output_dir` local computed at line 1731, available before the dispatch call at 1807.

IMPORTANT for TUI gating: `state_output_dir` is `None` on the spec-only smoke path (no `--output`). The pre-dispatch `dispatching` write at 1787 is gated `if state_output_dir is not None`. The TUI poll loop has nothing to read if `state_output_dir is None`, so the wiring / `should_enable_tui()` must handle the no-output case (R2 covers should_enable_tui()).

---

## 9. Resume `dispatch_wave1` call site — LEAVE UNTOUCHED (v1 fresh-run only)

- `_run_resume_branch` defined at: `commands.py:2048`
- Resume `dispatch_wave1(...)` call: **`commands.py:2264-2268`**:

```python
        raw_redispatched = dispatch_wave1(
            synthetic_preflight,
            transport_for_slot=_resume_slot_transport,
            logger=None,
        )
```

CONFIRMED: separate call site inside `_run_resume_branch` (reached only via the `if resume_job_id is not None:` branch at line 1539, which `return`s at 1567 before the fresh-run flow). LEAVE UNTOUCHED in v1. The `--tui` wiring touches ONLY the fresh-run `dispatch_wave1` at 1807-1813.

---

## 10. Recommended `--tui --detached` rejection insertion point

The guard must fire BEFORE the fresh `--detached` branch returns (line 1607). Candidates:

- **RECOMMENDED: at `commands.py:1581`**, immediately after `mode, spec_dict = _resolve_input_mode(...)` (line 1581 is that statement) and BEFORE the `if detached:` branch at 1589. By this point the resume branch (1539-1567) and the `--force-relens` trap (1573-1579) have already returned/raised, so we are in the fresh-run flow. Inserting the reject just after line 1581 means it fires before the detached branch can `return`.
- Alternative: right after the resume `return` (after line 1567, before `if force_relens:` at 1573). Also valid, but placing it adjacent to the `if detached:` branch it protects (after 1581) is clearer.

Suggested guard (mirrors the resume+detached reject at 1547-1553 in shape; uses `EXIT_USAGE`):

```python
    if tui and detached:
        click.echo(
            "swarm run --tui: --tui is mutually exclusive with "
            "--detached (the live dashboard requires a foreground run)",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)
```

Mirrors the literal phrasing of the resume+detached reject ("X is mutually exclusive with --detached (...)") and the same `click.echo(..., err=True)` + `raise click.exceptions.Exit(EXIT_USAGE)` shape per FR-3 D1.

---

## SUMMARY — exact insertion-point line anchors

1. **`--tui` Click option decorator** → insert after `commands.py:1469` (end of `--detached` block), before `@auto_inject_guard_option` at `commands.py:1470`.
2. **`tui: bool` parameter** → insert in `run_cmd` signature between `detached: bool,` (`commands.py:1484`) and `auto_inject_guard: bool,` (`commands.py:1485`).
3. **Docstring `--tui` note** → within docstring `commands.py:1487-1521` (flow narrative 1506-1520).
4. **`--tui --detached` reject guard** → insert at `commands.py:1581` (after `_resolve_input_mode`, before `if detached:` at 1589). Use `EXIT_USAGE`; mirror resume+detached reject at 1547-1553.
5. **Fresh `dispatch_wave1` call to move onto worker thread** → `commands.py:1807-1813` (verbatim kwargs: positional `preflight_result`; `transport_for_slot=run_transport_factory`, `prompt=assembled_prompt`, `worker_spec=inline_job.workers`, `logger=logger`; result name `worker_results`).
6. **Post-dispatch continuation (runs after join + re-raise)** → first active line `commands.py:1826` (`recipe_name = ...`); normalize/reduce block 1827-1893; terminal flip 1898-1903; success echo 1907-1911; `EXIT_OK` at 1912.
7. **Poll-loop read root** → `state_output_dir` local computed at `commands.py:1731` (= `manifest_dir` = `Path(preflight_result.manifest_path).parent`); holds both `execution-log.jsonl` and `.swarm-state.json`. May be `None` on the no-`--output` smoke path — gate accordingly.
8. **Constants** → `SWARM_STATE_FILENAME` (85), `EXECUTION_LOG_JSONL_FILENAME` (99), `EXIT_USAGE` (190), `EXIT_INVALID` (189), `EXIT_OK` (188).
9. **Resume `dispatch_wave1` — DO NOT TOUCH** → `commands.py:2264-2268` (inside `_run_resume_branch`, defined at 2048).
10. **`should_enable_tui()` gate placement** → after the `--tui --detached` guard (§4/§10 insertion at 1581), with the thread-launch + poll-loop wrapping the dispatch call at 1807-1813; gate must handle `state_output_dir is None`.
