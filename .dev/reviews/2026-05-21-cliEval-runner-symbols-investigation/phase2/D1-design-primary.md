# D1 — Design Spec, Candidate C1 (Minimal In-Place Authoring + 4 Sibling Wrappers)

**Agent**: D1 (primary designer; HYBRID T1+T3 verdict materialised as the top-ranked candidate)
**Date**: 2026-05-21
**Read-only**: no source-tree edits performed. The artifact is a hand-off to Phase 2B (red-team validation) and Phase 3 (orchestrator synthesis), and ultimately to the `/sc:task` builder that will materialise the 10 atomic remediation tasks below.

**Inputs consumed (full): `phase1B-debate-verdict.md`, `phase1/A1-module-audit.md`, `phase1/A4-thesis-belong-elsewhere.md`, the entire `src/superclaude/cli/eval/commands.py` import block + decorator stack + body, `artifact_layout.py`, `runner.py:130-200, 700-870`, `orchestrator.py:1-100`, `claude_process.py:90-250`, `isolation.py:300-390`, `signal_handler.py:180-260`, `models.py:720-810`, `design-spec.md:195-225, 580-595`, `CP-P04-END.md:99-160, 207-240`, `CP-P05-END.md:130-200, 395-445`, and `tests/cli/eval/test_eval_group.py:95-130`.**

---

## Executive summary

Candidate **C1** picks the minimum-viable-surface incarnation of the HYBRID T1+T3 verdict. Every one of the eleven F821 symbols lives in `commands.py` as a module attribute — seven as net-new private functions/constants (pure T1), four as thin wrappers that delegate to verified sibling helpers (HYBRID T1+T3). The Click 8.3.2 `mix_stderr` regression at `tests/cli/eval/test_eval_group.py:114` is fixed in lockstep. The 12 F401 unused imports collapse to two stale removals (`os`, `secrets`, `Sequence`) and ten newly-consumed imports once the wrappers land. The patch surface is ~95 LOC added to `commands.py`, one line edited and one line removed in `test_eval_group.py`, ~40 LOC of new pytest coverage in a brand-new `tests/cli/eval/test_eval_run.py`, and zero edits to any sibling module.

The strategic property C1 buys: **every Phase-4 surface that is already PASS today stays PASS** (Expect primitives, FR-G4 layout, FR-G5 coverage gate, TEST-007/8/9, OPS-003 retention policy); the F401+F821 ruff cluster clears in a single atomic edit; and the five test files that mock-patch `commands._run_one_spec` continue to work without changes because the symbol stays a `commands.py` module attribute.

---

## §1 — Symbol-by-symbol implementation table

> **Convention notes**
> - **Home** = `commands.py` everywhere in C1.
> - **Sibling delegate** column cites verbatim signatures by `file:line`; "(none)" marks pure T1 net-new authoring.
> - **LOC** estimates are *before* docstrings; budget +3–6 lines per symbol for inline docstrings + design-spec citations.
> - Verification-tier signatures are quoted verbatim under the table.

| # | Symbol | Type | Home | Signature | Body sketch | Sibling delegate (if wrapper) | LOC |
|---|---|---|---|---|---|---|---|
| 1 | `RUN_CLEAN_EXIT_CODE` | constant (T1) | `commands.py` | `int = 0` | `RUN_CLEAN_EXIT_CODE: int = 0` | (none) | 1 |
| 2 | `RUN_FAILURES_EXIT_CODE` | constant (T1) | `commands.py` | `int = 1` | `RUN_FAILURES_EXIT_CODE: int = 1` | (none) | 1 |
| 3 | `RUN_INTERRUPTED_EXIT_CODE` | constant (T1) | `commands.py` | `int = 3` | `RUN_INTERRUPTED_EXIT_CODE: int = 3` | (none) | 1 |
| 4 | `_utc_iso_now` | helper (T1, stdlib delegation) | `commands.py` | `() -> str` | `return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")` | `datetime.now(timezone.utc).isoformat(...)` (stdlib) | 2 |
| 5 | `_can_install_signal_handler` | helper (T1, stdlib delegation) | `commands.py` | `() -> bool` | `import threading; return threading.current_thread() is threading.main_thread()` | `threading.current_thread() is threading.main_thread()` (stdlib; mirrors `signal_handler.py:203-206` invariant) | 3 |
| 6 | `_new_run_id` | wrapper (HYBRID T1+T3) | `commands.py` | `(started_iso: str, suite_name: str) -> str` | `return compose_run_id(started_iso, suite_name)` | `artifact_layout.compose_run_id` at `artifact_layout.py:139` | 2 |
| 7 | `_default_output_dir` | wrapper (HYBRID T1+T3) | `commands.py` | `(started_iso: str, suite_name: str) -> Path` | `return compose_run_dir(Path.cwd(), started_iso, suite_name)` (see Open Q2 resolution) | `artifact_layout.compose_run_dir` at `artifact_layout.py:162` | 2 |
| 8 | `_resolve_executor_factory` | wrapper (HYBRID T1+T3) | `commands.py` | `() -> Callable[[ExecutorContext], LifecycleExecutor]` (closure factory; see §2 Q-RESV-3) | `def _make(_ctx): return ClaudeProcessAdapter(...); return _make` — concretely, return a callable whose internals are described in `_run_one_spec` body. C1 picks the simplest viable shape: the factory is a *zero-arg* callable that returns a callable adapter constructor (Protocol-shaped). | `claude_process.ClaudeProcessAdapter` at `claude_process.py:107`; `runner.LifecycleExecutor` Protocol at `runner.py:136` | 5 |
| 9 | `_run_one_spec` | wrapper (HYBRID T1+T3) | `commands.py` | `(spec: EvalSpec, *, run_dir: Path, home_root: Path, config: EvalConfig, timeout_mult: float, keep_home: bool, cancellation_token: CancellationToken, executor_factory: Callable) -> EvalOutcome` | (a) allocate per-eval paths via `allocate_per_eval_paths(run_dir, spec.id)`; (b) build `HomeIsolation(eval_id=spec.id, home_root=home_root, session_id=secrets.token_hex(8))`; (c) call `home.setup(config=config)`; (d) instantiate `ClaudeProcessAdapter` (or call `executor_factory(ctx)`) for the executor; (e) instantiate `EvalRunner(home=home, config=config, executor=executor, run_dir=paths.eval_dir, artifacts_dir=paths.artifacts_dir, stdout_path=…, stderr_path=…, transcript_path=paths.tty_transcript, expect_callables=spec.compiled_expects, keep_home_on_pass=keep_home, default_timeout_sec=spec.timeout_sec * timeout_mult, cancellation_token=cancellation_token)`; (f) `return runner.run(spec)`. Re-raises `HomeContainmentViolation` as ERRORED outcome per `D-0048` status-mapping rules. | `runner.EvalRunner.__init__` at `runner.py:754` + `.run(spec)` at `runner.py:823`; `artifact_layout.allocate_per_eval_paths` at `artifact_layout.py:232`; `isolation.HomeIsolation` at `isolation.py:356`; `claude_process.ClaudeProcessAdapter` at `claude_process.py:107` | 25–35 |
| 10 | `_compute_run_stats` | helper (T1, genuinely new) | `commands.py` | `(outcomes: Sequence[EvalOutcome], *, manifest_n: int) -> tuple[RunCounts, RunTotals]` | Walk `outcomes` once, tally per-status into a local `Counter`; build `RunCounts(manifest_n=manifest_n, expanded_n_prime=len(outcomes), kept_k=len([o for o in outcomes if o.status not in ("SKIPPED","INTERRUPTED")]), skipped_s=len([o for o in outcomes if o.status in ("SKIPPED","INTERRUPTED")]), kept_plus_skipped_equals_n_prime=True)`; build `RunTotals(passed=counter["PASS"]+counter["XFAIL"], failed=counter["FAIL"]+counter["XPASS"], skipped=counter["SKIPPED"], errored=counter["ERRORED"], interrupted=counter["INTERRUPTED"], timeout=counter["TIMEOUT"])`. Status-rollup rules quote `design-spec.md:580-590` verbatim. | (none — `RunCounts`/`RunTotals` dataclasses at `models.py:732,786` carry no `from_outcomes` aggregator) | 15 |
| 11 | `_format_run_summary_line` | helper (T1, genuinely new) | `commands.py` | `(summary: RunSummary, output_dir: Path) -> str` | `return f"eval run {summary.run_id}: passed={summary.totals.passed} failed={summary.totals.failed} skipped={summary.totals.skipped} errored={summary.totals.errored} timeout={summary.totals.timeout} duration={summary.duration_sec:.2f}s → {output_dir}"` | (none) | 3 |

### Verification-tier signature quotes

**`compose_run_id`** (`artifact_layout.py:139-159`, verbatim):
```python
def compose_run_id(started_at: str, suite_name: str = "") -> str:
    """Return the per-run identifier for ``(started_at, suite_name)``.
    Shape: ``<HHMMSSZ>-<8-hex>`` …"""
```

**`compose_run_dir`** (`artifact_layout.py:162-192`, verbatim):
```python
def compose_run_dir(
    output_root: Path | str,
    started_at: str,
    suite_name: str = "",
) -> Path:
    """Return ``<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``."""
```

**`allocate_per_eval_paths`** (`artifact_layout.py:232-260`, verbatim):
```python
def allocate_per_eval_paths(
    run_dir: Path | str,
    eval_id: str,
    *,
    create: bool = True,
) -> PerEvalPaths:
```

**`EvalRunner.__init__`** (`runner.py:754-774`, verbatim — kwarg-only):
```python
def __init__(
    self,
    *,
    home: HomeIsolation,
    config: EvalConfig,
    executor: LifecycleExecutor,
    run_dir: Path,
    artifacts_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    transcript_path: Path,
    expect_callables: Sequence[ExpectCallable] = (),
    deploy_hooks: Callable[[Path], None] = deploy_hooks_to,
    keep_home_on_pass: bool = False,
    default_timeout_sec: Optional[float] = None,
    clock: Callable[[], float] = time.monotonic,
    cancellation_token: Optional[CancellationToken] = None,
    retry_count: int = DEFAULT_RETRY_COUNT,
    retry_policy: Optional[RetryOncePolicy] = None,
    home_factory: Optional[Callable[[], HomeIsolation]] = None,
) -> None:
```

**`EvalRunner.run`** (`runner.py:823`, verbatim):
```python
def run(self, spec: EvalSpec) -> EvalOutcome:
```

**`HomeIsolation`** dataclass (`isolation.py:385-388`, verbatim):
```python
eval_id: str
home_root: Path
session_id: str
time_offset_sec: int = 0
```

**`SignalHandlerInstaller.install`** main-thread guard (`signal_handler.py:203-206`, verbatim):
```python
if threading.current_thread() is not threading.main_thread():
    raise ValueError(
        "SignalHandlerInstaller must be installed from the main thread"
    )
```

**Design-spec §4 exit-code mapping** (`design-spec.md:202-209`, verbatim):
```
| Code | Meaning |
|---|---|
| `0` | All evals PASSED (or correctly SKIPPED due to capability gates). |
| `1` | At least one eval FAILED. |
| `2` | Harness error (manifest invalid, claude binary missing, etc.). |
| `3` | Interrupted (SIGINT during run). |
```

---

## §2 — Open question resolutions

### Q-RESV-1 — `_compute_run_stats` home (HIGH confidence)

**Resolved: `commands.py`-local aggregator.**

Rationale: (i) the symbol name `_compute_run_stats` with a leading underscore signals module-private surface; promoting it to `RunCounts.from_outcomes` / `RunTotals.from_outcomes` classmethods on `models.py` would require renaming and editing a sibling module, which violates C1's no-sibling-edits invariant. (ii) The five test files that pin behavioural contracts (`test_no_mcp_skip.py:528`, `test_no_pty_exclusion.py:337`, `test_single_command.py:152`, `test_retention_policy.py:93`, `test_exit_codes.py:107`) probe `hasattr(commands, "_compute_run_stats")`; relocating the helper to `models.py` would silently flip those `hasattr` probes from "present" to "absent" and break the test contract. (iii) Phase 1B debate §Synthesis explicitly endorses `commands.py`-local placement: *"default to `commands.py`-local (matches `_run_one_spec` placement and test-mock convention)"*. The aggregator is ~15 LOC and adds no cohesion to `models.py` (the dataclasses there are plain field carriers; aggregation is a `commands`-domain concern).

**Trade-off accepted**: if M5/M6 surfaces additional consumers of the aggregator (e.g. a future `eval summarize` subcommand that recomputes counts from a persisted `summary.json`), the helper will need to be promoted to `models.py` then. C1 explicitly defers that promotion; rationale recorded for M5 follow-up.

### Q-RESV-2 — `_default_output_dir` vs scratch-root layering (HIGH confidence)

**Resolved: wrapper computes `compose_run_dir(Path.cwd(), started_iso, suite_name)` and the AC12 scratch-root allowlist remains the single enforcement boundary.**

Rationale: (i) `artifact_layout.py:41-44` *already* documents this layering: *"The default ``output_root=Path.cwd()`` combined with ``RUN_DIR_PREFIX = .dev/eval-runs`` lands inside the canonical AC12 prefix automatically"*. (ii) The current call site at `commands.py:1473-1480` already routes the path through `resolve_scratch_root(requested_output, config=base_config, output_dir=output_dir)` before any `mkdir`; this stays the gate. The wrapper only constructs a candidate path; it does not bypass the allowlist. (iii) The eleven-symbol resolution table in A1 §1 confirms this is the only viable shape — `compose_run_dir` takes `(output_root, started_at, suite_name)` and the caller has all three in scope.

**Side effect**: the call ordering at `commands.py:1467-1469` must change. The current order is `run_id = _new_run_id()` then `_default_output_dir(run_id)` — both happen *before* `started_iso = _utc_iso_now()` at line 1612. C1 will move `started_iso = _utc_iso_now()` up to **line 1466** (immediately after `base_config = EvalConfig()`), so the existing `started_iso = _utc_iso_now()` at line 1612 becomes redundant and is dropped. The single `started_iso` value flows through both `_new_run_id(started_iso, suite_name=parsed.name)` *and* `_default_output_dir(started_iso, suite_name=parsed.name)` deterministically. **Caveat**: `parsed.name` is not in scope at line 1466 — it is computed from `loader.load(manifest_path)` at line 1512. The wrappers must therefore be called *after* the suite-loader step. **Final ordering**: (a) compute `started_iso`; (b) resolve manifest path; (c) load suite; (d) compute `run_id` + `default_output_dir` using `parsed.name`; (e) resolve `output_dir`; (f) AC12 check. This re-shuffles the body but preserves every existing branch.

(See §4 call-graph diff for the exact line-number remapping.)

### Q-RESV-3 — `_new_run_id` API shape (MED confidence)

**Resolved: two-arg signature `(started_iso, suite_name) -> str`, not zero-arg.**

Rationale: (i) The zero-arg shape (closure-capture of outer-scope `started_iso` and `parsed.name`) requires nested-function authorship which makes the symbol *not* a `commands.py` module attribute — the five test files that `hasattr`-probe `commands._new_run_id` would fail. (ii) The two-arg shape matches `compose_run_id`'s signature byte-for-byte, so the body is a literal one-liner `return compose_run_id(started_iso, suite_name)`; the wrapper exists purely to keep the symbol pinned as a module attribute (mock-patch contract) without forcing a `mock.patch` on `artifact_layout.compose_run_id` (which would leak to every other consumer including `test_artifact_reproducibility.py:67`). (iii) Phase 1B debate §3 Open-Q-3 names the two options and explicitly flags "Project convention is split"; the test-contract weight from `test_single_command.py:149` (`hasattr(cmds, "_new_run_id")`) tips the decision toward "keep it a module-level wrapper that other tests can mock-patch in isolation".

**MED rather than HIGH** because the CP-P05-END remediation language at `:401-406` prescribes `compose_run_id(started_at=_utc_iso_now(), suite_name=suite)` directly — i.e. inlining rather than a wrapper. C1 picks the wrapper for test-contract reasons; if Phase 2B red-team surfaces a stronger argument for inlining (e.g. the test-mock contract is exclusive to `_run_one_spec` and `_new_run_id`'s probe is purely an existence check, not a behaviour mock), the design can collapse #6 + #7 into direct `compose_run_id` / `compose_run_dir` call sites.

### Q-RESV-4 — F401 cleanup ordering (HIGH confidence)

**Resolved: atomic single-commit cleanup in lockstep with helper authorship.**

The ruff gate (`test_ban_import_rule.py::test_clean_tree_passes_ruff_check`) is a unitary all-or-nothing pass; a staged commit that leaves F401s green while F821s remain (or vice versa) re-fails the same gate the sprint is being unblocked for. C1's atomic-task list (§9) sequences the constants + helpers first (T1–T7), the import-block update + F401 clear second (T8), and the gate-passing test fixes (T9–T10) last — but all of these land in a single feature-branch PR.

### Q-RESV-5 — `_can_install_signal_handler` shape (HIGH confidence)

**Resolved: boolean probe `threading.current_thread() is threading.main_thread()`.**

The probe is mockable (a test can `monkeypatch.setattr(commands, "_can_install_signal_handler", lambda: False)`); the try/except shape is not. The probe is also a one-line read of the same invariant `SignalHandlerInstaller.install()` raises on (signal_handler.py:203-206), so the two surfaces cannot drift.

---

## §3 — Updated import block (verbatim)

### BEFORE (commands.py:30-88, current state, with ruff F401 annotations)

```python
import json                       # (unchanged)
import os                         # (F401-removed: still unused; stale)
import platform                   # (unchanged)
import re                         # (unchanged)
import secrets                    # (F401-cleared: now used by _run_one_spec — session_id allocation)
import subprocess                 # (unchanged)
import sys                        # (unchanged)
import time                       # (unchanged)
from dataclasses import dataclass, replace                          # (unchanged)
from datetime import datetime, timezone                             # (F401-cleared: now used by _utc_iso_now)
from pathlib import Path                                            # (unchanged)
from typing import Any, Callable, Iterable, Optional, Sequence      # (F401-cleared: Sequence now used in _compute_run_stats signature + _run_one_spec param; Callable now used in _resolve_executor_factory return type)

import click                      # (unchanged)
import yaml                       # (unchanged)

from .capabilities import CapabilityGates, CapabilityReport, CapabilityStatus     # (unchanged)
from .config import (SCRATCH_ROOT_VIOLATION_EXIT_CODE, EvalConfig,
                     ScratchRootViolation, format_scratch_root_violation,
                     resolve_scratch_root)                                         # (unchanged)
from .coverage import (COVERAGE_GATE_FAILED_EXIT_CODE, CoverageResult,
                       coverage_gate)                                              # (unchanged)
from .disk_budget import (DEFAULT_DISK_BUDGET_MB,
                          DISK_BUDGET_EXCEEDED_ARTIFACT_NAME,
                          DISK_BUDGET_EXCEEDED_EXIT_CODE,
                          DISK_BUDGET_RETENTION_ADVICE, DiskBudgetPoller)         # (unchanged)
from .isolation import HomeContainmentViolation, HomeIsolation                    # (F401-cleared: HomeIsolation now used in _run_one_spec; HomeContainmentViolation caught in _run_one_spec for ERRORED status mapping)
from .loader import (SUITE_LOADER_ERROR_EXIT_CODE, ParsedSuite, SuiteLoader,
                     SuiteLoaderError)                                             # (unchanged)
from .models import (EvalOutcome, EvalSpec, RunCounts, RunSummary, RunTotals)     # (F401-cleared: RunCounts + RunTotals now used as _compute_run_stats return types)
from .orchestrator import RunOrchestrator                                          # (unchanged)
from .reporter import Reporter                                                     # (unchanged)
from .runner import EvalRunner, LifecycleExecutor                                  # (F401-cleared: EvalRunner now constructed by _run_one_spec; LifecycleExecutor now annotates _resolve_executor_factory return type)
from .signal_handler import CancellationToken, SignalHandlerInstaller             # (unchanged)
from .suites import SCHEMA_PATH                                                    # (unchanged)
```

### AFTER (commands.py:30-89, post-C1)

Three changes from the BEFORE block above:

1. **Drop line 31** `import os` (`F401-removed` — stale).
2. **Add line 39.5** `import threading` (`new import: required by _can_install_signal_handler`). Insertion point: between `import time` and `from dataclasses import ...` to keep stdlib imports grouped.
3. **Add line 86.5** `from .artifact_layout import allocate_per_eval_paths, compose_run_dir, compose_run_id` (`new import: required by _new_run_id, _default_output_dir, _run_one_spec`). Insertion point: between `from .orchestrator import RunOrchestrator` and `from .reporter import Reporter` to keep alphabetical-ish module order.
4. **Add line 86.6** `from .claude_process import ClaudeProcessAdapter` (`new import: required by _resolve_executor_factory / _run_one_spec`). Insertion point: between the new `artifact_layout` line and `from .reporter import Reporter`.

The remaining ten F401-cleared lines stay verbatim — each becomes consumed once the corresponding helper lands. **Net effect on ruff**: 0 F401 errors, 0 F821 errors, 0 new I001 import-order violations (the two added imports sit alphabetically inside the eval-package block).

**One residual call-out for Phase 2B**: the body uses `dataclass` and `replace` (from `dataclasses`) elsewhere in the module — both stay unchanged and the import stays unchanged. The body uses `time.monotonic()` at lines 1613 and 1637, so `time` stays. The body uses `json.dumps` at line 1669, so `json` stays. None of these are F401 candidates.

---

## §4 — Call-graph diff for `eval_run` (1406–1695)

The ASCII diff below shows the body's call sequence pre- and post-C1. The 19 branch-trace entries from `expected-branches-extended.txt` are annotated `B<i>` so the diff can be cross-referenced. Branch-semantics-changed entries are marked `[CHANGED]`; lines that move without semantic change are marked `[MOVED]`.

```
                                BEFORE (current, F821-broken)            AFTER (C1)
                                ─────────────────────────────             ──────────
B1   1443  parallel < MIN clamp                                            (unchanged)
B2   1445  parallel > MAX clamp                                            (unchanged)
B3   1448  timeout_mult <= 0 → sys.exit(HARD_FAIL_EXIT_CODE)               (unchanged)
B4   1455  max_disk_mb < 0  → sys.exit(HARD_FAIL_EXIT_CODE)                (unchanged)
     1466  base_config = EvalConfig()                                       (unchanged)
                                                                        ►  1466.5  started_iso = _utc_iso_now()              [MOVED — was at 1612]
B5   1467  run_id = _new_run_id()                                       ►  *deleted — moved below suite load*
B6   1469  _default_output_dir(run_id)                                  ►  *deleted — moved below suite load*
     1473  resolve_scratch_root(requested_output, ...)                     (unchanged — but `requested_output` is now resolved later, see B7)
B7   1478  except ScratchRootViolation → sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)  (unchanged; just shifted line)
     1482  resolved_output.mkdir(...)                                      (unchanged)
     1483  home_root = resolved_output / "homes"                           (unchanged)
     1494  runtime_config = EvalConfig(...)                                (unchanged)
B8   1505  manifest_path = resolve_suite_manifest(suite, _DEFAULT_SUITES_DIR)  (unchanged)
B9   1506  except SuiteNotFound → sys.exit(SUITE_NOT_FOUND_EXIT_CODE)       (unchanged)
     1510  loader = SuiteLoader(); parsed = loader.load(manifest_path)     (unchanged)
B10  1513  except SuiteLoaderError → sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)  (unchanged)
     1517  manifest_n = len(parsed.evals)                                  (unchanged)
     1518  specs = parsed.evals                                            (unchanged)
B11  1519  if eval_ids: filter + EvalNotFound                              (unchanged)
                                                                        ►  1530.5  run_id = _new_run_id(started_iso, parsed.name)     [MOVED]
                                                                        ►  1530.6  requested_output = output_dir if output_dir is not None else _default_output_dir(started_iso, parsed.name)  [MOVED]
                                                                        ►  1530.7  resolve_scratch_root(...) block executes HERE   [MOVED]
B12  1541  coverage = coverage_gate(...)                                   (unchanged)
B13  1546  if not coverage.passed → sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE)  (unchanged)
     1556  skip_flags = []                                                 (unchanged)
     1561  _gates = CapabilityGates(...)                                   (unchanged)
     1567  poller = DiskBudgetPoller(...)                                  (unchanged)
     1572  token = CancellationToken()                                     (unchanged)
B14  1577  executor_factory = _resolve_executor_factory()                  (unchanged — wrapper now resolves)
     1579  def run_one(spec):                                              (unchanged)
B15  1586  if no_pty and spec.no_pty == "skip" → return EvalOutcome(SKIPPED)  (unchanged)
B16  1598  return _run_one_spec(spec, ...)                                 (unchanged — wrapper now resolves)
                                                                        ►  1612   *deleted: started_iso = _utc_iso_now()*    [MOVED upward to 1466.5]
     1613  started_monotonic = time.monotonic()                            (unchanged)
     1615  orchestrator = RunOrchestrator(...)                             (unchanged)
B17  1624  if SignalHandlerInstaller and _can_install_signal_handler():    (unchanged — wrapper now resolves)
     1625      with SignalHandlerInstaller(token): outcomes = orch.run()   (unchanged)
B18  1627  else: outcomes = orchestrator.run(specs, parallel=parallel)     (unchanged)
B19  1629  except ValueError → sys.exit(HARD_FAIL_EXIT_CODE)               (unchanged)
     1636  finished_iso = _utc_iso_now()                                   (unchanged — wrapper now resolves)
     1637  duration_sec = time.monotonic() - started_monotonic             (unchanged)
     1642  counts, totals = _compute_run_stats(outcomes, manifest_n=manifest_n)  (unchanged — helper now resolves)
     1649  summary = RunSummary(...)                                       (unchanged)
     1663  Reporter(summary=summary, emit_junit=junit).write(resolved_output)  (unchanged)
     1668  if as_json: click.echo(json.dumps(...))                         (unchanged)
     1670  elif verbose: click.echo(_format_run_summary_line(...))         (unchanged — helper now resolves)
     1676  if token.is_cancelled(): sys.exit(RUN_INTERRUPTED_EXIT_CODE)    (unchanged — constant now resolves)
     1678  if poller.is_breached(): … sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)  (unchanged)
     1689  if totals.failed > 0 or ... → sys.exit(RUN_FAILURES_EXIT_CODE)   (unchanged — constant now resolves)
     1695  sys.exit(RUN_CLEAN_EXIT_CODE)                                    (unchanged — constant now resolves)
```

**Branch-semantics summary**: 0 of the 19 branches change semantics. The diff is *purely* (a) symbol resolution and (b) one local re-ordering of `started_iso`/`run_id`/`_default_output_dir`/AC12 around the suite-load step so the wrapper signatures stay zero-glue. Every existing exit-code path (B3, B4, B7, B9, B10, B11, B13, B19, plus the new B17/B18 → RUN_INTERRUPTED/RUN_FAILURES/RUN_CLEAN paths) is preserved verbatim.

**INFERENTIAL**: the re-ordering trades "compute run-id without suite name" for "compute run-id after suite parse so the deterministic hash includes `parsed.name`". This is the *correct* shape per `artifact_layout.py:139-159` which folds `suite_name` into the sha256 digest precisely so two runs against different suites at the same instant cannot collide. The current placeholder ordering (run-id before suite parse) would have produced run-ids that depend only on time-of-day — a determinism regression. C1 fixes this latent bug at the same time as the F821 cluster.

---

## §5 — Exit-code constant table

| Constant | Value | Used at | Design-spec reference |
|---|---|---|---|
| `RUN_CLEAN_EXIT_CODE` | `0` | `commands.py:1695` | `design-spec.md:206` (`0` ⇔ All evals PASSED / correctly SKIPPED); also `design-spec.md:590` mapping clause |
| `RUN_FAILURES_EXIT_CODE` | `1` | `commands.py:1694` | `design-spec.md:207` (`1` ⇔ At least one eval FAILED); also `design-spec.md:590` mapping clause |
| `RUN_INTERRUPTED_EXIT_CODE` | `3` | `commands.py:1677` | `design-spec.md:209` (`3` ⇔ Interrupted SIGINT during run); also `design-spec.md:590` mapping clause |
| `HARD_FAIL_EXIT_CODE` *(existing)* | `2` | `commands.py:1453, 1461, 1634` | `design-spec.md:208` (`2` ⇔ Harness error) — already defined at `commands.py:550` |
| `SCRATCH_ROOT_VIOLATION_EXIT_CODE` *(existing)* | `2` | `commands.py:1480` | imported from `.config`; same `design-spec.md:208` semantic class |
| `EVAL_NOT_FOUND_EXIT_CODE` *(existing)* | `2` | `commands.py:1529` | already at `commands.py:954` |

**Insertion point for the three new constants**: between `commands.py:1289` (end of existing `RUN_BODY_DEFERRED_EXIT_CODE` block) and `commands.py:1291` (start of `RUN_BODY_DEFERRED_MESSAGE`). Convention matches the eight existing `*_EXIT_CODE` constants: module-level integer with `: int = N` annotation + one-line docstring citing `design-spec.md:202-209`.

---

## §6 — Test matrix

| Test file | Effect under C1 | Notes |
|---|---|---|
| `tests/cli/eval/test_eval_run.py` | **NEW** (~40 LOC) | Must be authored. Covers: (a) all 12 FR-CLI1 flag parses (one Click invocation per flag with `--help`); (b) `--parallel` clamp paths (0→1, 99→15); (c) AC12 violation produces exit 2 (via patching `resolve_scratch_root` to raise); (d) one-eval end-to-end happy path with a minimal stub `_run_one_spec` returning a canned `EvalOutcome` → expect exit 0, `summary.md` + `summary.json` on disk; (e) `RUN_FAILURES_EXIT_CODE` path: stub `_run_one_spec` to return a FAIL outcome → expect exit 1; (f) `RUN_INTERRUPTED_EXIT_CODE` path: pre-cancel the token via `monkeypatch.setattr(commands.CancellationToken, "is_cancelled", lambda self: True)` → expect exit 3. |
| `tests/cli/eval/test_eval_group.py:114` | **un-fails** | Click 8.3.2 fix: drop `mix_stderr=False` kwarg from `CliRunner(...)` constructor; replace `result.stderr` access pattern with the new default (in Click 8.3.2+, `result.stderr` is available without the deprecated kwarg because stderr is captured separately by default; if the test still needs the legacy combined behavior, use `result.output` which already contains stdout). Verify against Click 8.3.2 changelog: the kwarg was removed; the attribute remains. |
| `tests/cli/eval/test_coverage_gate_integration.py` | **un-fails 2 cases** | `test_run_exits_2_when_settings_has_uncovered_matcher` and `test_run_writes_coverage_missing_artifact_under_output_dir` currently fail with `NameError("name '_new_run_id' is not defined")` because they `subprocess.run` against `superclaude eval run`; once C1 lands they exercise the coverage-gate branch end-to-end. |
| `tests/cli/eval/test_no_mcp_skip.py` | **un-skips 1** | `test_eval_run_no_mcp_skips_mcp_evals_end_to_end` is currently `pytest.skip`ed with explicit rationale citing the eleven missing helpers; `mock.patch("superclaude.cli.eval.commands._run_one_spec", ...)` at line 528 will resolve once C1 lands the symbol. |
| `tests/cli/eval/test_no_pty_exclusion.py` | **un-skips 1** | `test_eval_run_no_pty_skips_real_suite_end_to_end` is currently skipped with the same blocker; patches `_run_one_spec` at line 337. |
| `tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check` | **un-fails** | Currently fails on `23 errors (11 F401 + 12 F821)`. C1 clears all 23 in lockstep: 12 F821 by helper authorship, 11 F401 by import-block update + stale-import drops. |
| `tests/cli/eval/test_exit_codes.py` | **un-skips 3** (the 0/1/3 exit-code tests) | Currently skip-gated via `_t0410_missing()` at lines 93-113. The skip predicate probes 6 of the 11 helpers (`_new_run_id`, `_run_one_spec`, `_compute_run_stats`, `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`, `RUN_INTERRUPTED_EXIT_CODE`); once C1 lands all six, the predicate flips and the 0/1/3 tests un-skip. Tests 2 (harness-error) already PASS today via `ReporterContractViolation` route; not affected by C1. |
| `tests/cli/eval/test_single_command.py:148-160` | **un-skips** | `_eval_run_body_incomplete()` probes all 11 symbols via `hasattr`; flips to "complete" once C1 lands. |
| `tests/cli/eval/test_validation_commands.py:166-177` | **un-changed** | Asserts release-validation-doc enumerates B1 (`_new_run_id`) and B2 (`ptytest`); these are *documentation pins* not runtime gates. The follow-up ticket may be closed/superseded by C1 landing, but the test itself does not need to change. Phase 2B should flag whether the validation-doc text is updated to mark B1 as RESOLVED. |
| `tests/cli/eval/test_retention_policy.py` | **un-skips 1** (the `--keep-home`-preserves-on-PASS end-to-end branch) | Patches `_run_one_spec` at line 93; un-skips once C1 lands the symbol. |
| `tests/cli/eval/test_artifact_reproducibility.py` | **un-changed** | Already PASSES today against the FR-G4 layout (T04.13); not affected by C1. |
| `tests/cli/eval/test_artifact_layout.py` | **un-changed** | All 19 PASS today; not affected by C1. |
| `tests/cli/eval/test_coverage_gate.py` | **un-changed** | All 26 PASS today; the integration tests in `test_coverage_gate_integration.py` (above) are the affected surface. |
| `tests/cli/eval/test_reporter_contract.py` | **un-changed** | All 4 PASS today (T04.17); not affected by C1. |
| Per-eval determinism captures (E1..E15 × 3 runs) | **un-blocks** | Phase 5 carry-forward. Once `_new_run_id` resolves, the operator runs `for eval in E1 E2.1 ... E15; do for i in 1 2 3; do superclaude eval run --suite real --eval $eval > evidence/T05.02/run-${eval}-green-$i.log; done; done` and verifies identical `EvalOutcome.status` across each triple. C1 is the precondition, not the action. |

**Test-matrix roll-up**: 1 new file authored; 1 file edited (one-line fix); 7 existing files un-fail / un-skip without modification (the test bodies already pin the post-C1 behaviour and skip-gate themselves until the symbols resolve); 5 unaffected files stay green.

---

## §7 — Acceptance criteria

| AC ref | Description | Status under C1 | Evidence |
|---|---|---|---|
| CP-P04-END §Exit-Criteria #1 (`uv run pytest tests/cli/eval/ -v` clean) | Full eval test suite exits 0 | **SATISFIED** | 2 currently-FAIL tests un-fail (test_eval_group.py:114, test_ban_import_rule.py); 7 currently-SKIP tests un-skip (test_exit_codes 3, test_no_mcp_skip 1, test_no_pty_exclusion 1, test_single_command, test_retention_policy 1); 1 new test file (test_eval_run.py) added. |
| CP-P04-END §Exit-Criteria #2 (DOC-OQ7 / DOC-OQ3 resolved in decisions.md) | MET today, stays MET | **SATISFIED (carry-forward)** | C1 does not touch decisions.md. |
| CP-P04-END §Exit-Criteria #3 (No new lints / type-errors) | ruff F401+F821 cluster cleared | **SATISFIED** | T8 in §9 atomic-task list explicitly atomically clears all 23 ruff errors. |
| CP-P04-END T04.09 (`eval_group` skeleton, mix_stderr regression) | FAIL → PASS | **SATISFIED** | T9 in §9 atomic-task list. |
| CP-P04-END T04.10 (`eval_run` body wires all 12 FR-CLI1 flags + 11 helpers resolve at runtime) | FAIL → PASS | **SATISFIED** | T1–T7 author the 11 symbols; T8 clears the F401 cluster; T10 authors the test file the docstring enumerated. |
| CP-P04-END T04.11 (FR-G6 smoke contract present) | PARTIAL → stays PARTIAL | **SATISFIED (carry-forward)** | The live FR-G6 smoke un-skips at M5 once E1/T05.02 lands. C1 unblocks T05.02 but does not itself flip T04.11 to PASS. |
| CP-P04-END T04.16 (DOC-OQ3 `no_pty: skip` end-to-end) | PARTIAL → PASS | **SATISFIED** | The `test_eval_run_no_pty_skips_real_suite_end_to_end` SKIP un-skips under C1. |
| CP-P04-END T04.19 (TEST-008 exit-code semantics end-to-end) | PASS-with-caveat → PASS | **SATISFIED** | The "caveat" in the CP-P04-END row says the tests pass against cancellation/contract-violation surfaces but the `eval_run` body's own exit emission cannot be exercised end-to-end until the eleven helpers land. C1 lands them. |
| CP-P04-END T04.20 (TEST-009 artifact reproducibility end-to-end) | PASS-with-caveat → PASS | **SATISFIED** | Same caveat as T04.19; C1 removes the precondition. |
| CP-P05-END §Recommended-remediation-order step 1 (Wire `_new_run_id`) | UNBLOCKED | **SATISFIED** | T5 in §9 atomic-task list. |
| CP-P05-END §Recommended-remediation-order step 2 (E1..E15 × 3 determinism captures) | UNBLOCKED (precondition met) | **SATISFIED-as-precondition** | C1 does not run the captures; it removes the F821 blocker so M5 can run them. |
| CP-P05-END §Recommended-remediation-order step 3 (NFR-PERF3 parallel-8 < 600s) | UNBLOCKED (precondition met) | **SATISFIED-as-precondition** | Same as step 2. |
| CP-P05-END T05.25 (TEST-013 coverage-gate integration end-to-end) | PARTIAL (4/6) → PASS (6/6) | **SATISFIED** | The 2 currently-FAIL tests un-fail under C1. |
| CP-P05-END T05.26 (TEST-014 no-MCP-skip end-to-end) | PARTIAL (11/12) → PASS (12/12) | **SATISFIED** | The 1 currently-SKIP un-skips. |
| NFR-PERF2 (parallel clamp [1,15]) | UNCHANGED | **SATISFIED-by-existing-code** | The clamp at `commands.py:1443-1446` is unchanged. |
| NFR-PERF3 (parallel-8 < 600s) | UNBLOCKED | **SATISFIED-as-precondition** | C1 does not affect orchestrator throughput; it removes the symbol blocker so the wall-clock measurement can be captured. |
| NFR-REL1 (cooperative cancellation, INTERRUPTED outcome) | UNCHANGED | **SATISFIED-by-existing-code** | `_run_one_spec` wires the `cancellation_token` into `EvalRunner.__init__(cancellation_token=...)`; the runner already implements the cooperative-cancel contract at `runner.py:880-887`. |
| FR-G4 (reproducible artifact layout) | UNCHANGED | **SATISFIED-by-existing-code** | `compose_run_dir` and `allocate_per_eval_paths` are already PASS (T04.13). |
| FR-G5 (coverage-gate) | UNCHANGED | **SATISFIED-by-existing-code** | `coverage_gate` is already PASS (T04.14). |
| OPS-003 (retention policy) | UNCHANGED | **SATISFIED-by-existing-code** | The `DISK_BUDGET_RETENTION_ADVICE` echo path at `commands.py:1687` is unchanged. |

**Roll-up**: 19 ACs evaluated, 0 regressions, 7 directly-satisfied-by-authoring, 5 satisfied-as-precondition (M5 acceptance criteria that C1 unblocks but does not itself satisfy), 7 unchanged-and-still-PASS. **No AC degrades under C1.**

---

## §8 — Risk register

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | **Mock-patch resolution fails** — five test files do `mock.patch("superclaude.cli.eval.commands._run_one_spec", ...)`; if C1 inadvertently relocates the symbol (e.g. a future refactor makes it a closure inside `eval_run`), the mock-patches silently no-op and the tests false-pass. | LOW | HIGH | C1 explicitly authors `_run_one_spec` as a **module-level** function (not a closure), pins this in §1's "Home" column, and the §6 test matrix names every patch site so Phase 2B can sanity-check. A `tests/cli/eval/test_run_helper_surface.py::test_run_helpers_are_module_attributes` smoke test (probing `hasattr(commands, name)` for each of the 11 names) catches any future relocation. INFERENTIAL: this smoke test could be added as a 12th task in §9 but C1 defers it as out-of-scope refinement. |
| R2 | **Scratch-root allowlist mismatch** — `_default_output_dir` returns `Path.cwd() / .dev/eval-runs/<date>/<run-id>` and the AC12 allowlist must contain `Path.cwd() / .dev/eval-runs/`. If the operator's `cwd` is outside any allowlisted root, the AC12 check at `commands.py:1473` raises `ScratchRootViolation` and the run exits 2. | MED | MED | The current `EvalConfig._default_allowed_scratch_roots()` (verified by `artifact_layout.py:79-82` which calls out the alignment explicitly) includes `Path.cwd() / .dev/eval-runs/` as the canonical AC12 prefix, so the default path always lands in the allowlist. C1 does not change this. Operators with a custom `--output-dir` bypass the default entirely and the AC12 check still gates. Phase 2B should verify by reading `config.py::_default_allowed_scratch_roots` directly. |
| R3 | **Performance regression: parallel-8 > 600s NFR-PERF3** — the wrapper authorship adds 1 stack frame per `_run_one_spec` invocation; on a 17-eval suite at parallel-8 this is negligible (<1ms total). The real risk is `HomeIsolation.setup()` filesystem I/O latency under contention. | LOW | HIGH (blocks M5 NFR-PERF3 sign-off) | C1 does not change orchestrator throughput or I/O patterns. `ThreadPoolExecutor` at `RunOrchestrator.run()` is unchanged. NFR-PERF3 measurement is M5's responsibility; C1 is purely the precondition. If M5 captures > 600s, the bottleneck is in `HomeIsolation.setup()` or `ClaudeProcessAdapter` — both unchanged by C1. |
| R4 | **Backward-compat with already-PASS Phase-4 surface** — the import block shuffle (drop `os`, add `threading`, add `artifact_layout`, add `claude_process`) could break a transitive `from .commands import …` in a third module if it re-exported `os` or `secrets`. | LOW | LOW | C1 verified `commands.py.__all__` is not defined (no explicit re-export), and `grep -rn "from .commands import os\|from .commands import secrets" src/` returns empty. The body of `_run_one_spec` consumes `secrets` so the import stays — only `os` is removed. Phase 2B should re-run the grep after C1 is implemented to confirm no consumer regresses. |
| R5 | **Ruff lockstep failure** — the F401 cluster must clear in the *same commit* as the F821 fix. If T1–T7 (constants + helpers) lands without T8 (import-block update), ruff stays red because the F401 cluster did not include `EvalRunner`/`LifecycleExecutor`/etc. until the helpers consumed them. If T8 lands first, the F401s clear but the F821s remain. | HIGH (if staged) | MED | C1 §2 Q-RESV-4 explicitly mandates atomic single-commit cleanup. The §9 atomic-task list sequences T1–T8 inside one PR; the `make verify-sync` + `ruff check src/superclaude/cli/eval/` gates run only after T1–T10 are all on disk. The Phase 2B red-team should adversarially test: "what if a reviewer requests T8 be split into a follow-up?" — the answer is "no — the ban-import-rule test fails for any intermediate state". |

**Top-of-stack secondary risks (not in top-5)**:
- R6: `_run_one_spec` HOME path containment — if the wrapper builds `HomeIsolation(eval_id=spec.id, home_root=home_root, ...)` and `home_root = resolved_output / "homes"` is not in the runtime allowlist, `home.setup(config=runtime_config)` raises `HomeContainmentViolation`. **Mitigation**: lines 1490–1499 in the *current* body already extend `runtime_config.allowed_scratch_roots` with `(resolved_output, home_root)` — this stays unchanged.
- R7: `_resolve_executor_factory` shape mismatch — the call site at line 1577 is `executor_factory = _resolve_executor_factory()` (no args); the factory must return a callable that `_run_one_spec` can call with the right kwargs. **Mitigation**: C1 picks the simplest viable shape (zero-arg factory returning a `LifecycleExecutor` instance constructor); Phase 2B may surface a richer factory-context shape.

---

## §9 — Atomic remediation tasks (hand-off to `/sc:task`)

Each task is ≤30 LOC, listed in dependency order. All ten land in one feature-branch PR; the F401+F821 ruff gate clears only after T8 lands. Tests pass only after T9–T10.

```
T1: Add RUN_*_EXIT_CODE constants in commands.py
    - File: src/superclaude/cli/eval/commands.py
    - Insertion point: between line 1289 (end of existing RUN_BODY_DEFERRED_EXIT_CODE
      block) and line 1291 (start of RUN_BODY_DEFERRED_MESSAGE).
    - Add three integer constants with one-line docstrings citing design-spec §4
      lines 202-209.
    - LOC: ~9 (3 constants × ~3 lines each with docstring).

T2: Add _utc_iso_now helper in commands.py
    - Insertion point: after the new RUN_*_EXIT_CODE constants from T1.
    - Body: `return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")`.
    - Verify against `artifact_layout._parse_iso` at artifact_layout.py:107-131 (the
      Z-suffix shape it accepts).
    - LOC: ~5 (signature + docstring + body).

T3: Add _can_install_signal_handler helper in commands.py
    - Insertion point: after _utc_iso_now from T2.
    - Body: `return threading.current_thread() is threading.main_thread()`.
    - Cite signal_handler.py:203-206 in the docstring as the mirrored invariant.
    - LOC: ~4 (signature + docstring + body); requires the `import threading` line
      added by T8.

T4: Add _resolve_executor_factory wrapper in commands.py
    - Insertion point: after _can_install_signal_handler from T3.
    - Body: returns a zero-arg callable that produces a `ClaudeProcessAdapter`
      instance with placeholder kwargs (home, prompt, output_file, error_file)
      that _run_one_spec will fill in. The factory shape is `Callable[[], Callable[[...kwargs...], LifecycleExecutor]]`.
    - Cite claude_process.py:107 as the production adapter.
    - LOC: ~8 (signature + docstring + 2-line body).

T5: Add _new_run_id + _default_output_dir wrappers in commands.py
    - Insertion point: after _resolve_executor_factory from T4.
    - _new_run_id body: `return compose_run_id(started_iso, suite_name)`.
    - _default_output_dir body: `return compose_run_dir(Path.cwd(), started_iso, suite_name)`.
    - Both cite artifact_layout.py:139,162 in the docstring.
    - LOC: ~10 (5 lines per wrapper); requires the `from .artifact_layout import ...`
      line added by T8.

T6: Add _run_one_spec wrapper in commands.py
    - Insertion point: after _new_run_id + _default_output_dir from T5.
    - Body: ~25-30 lines of orchestration glue (per §1 row 9 body-sketch):
      (a) `paths = allocate_per_eval_paths(run_dir, spec.id)`
      (b) `home = HomeIsolation(eval_id=spec.id, home_root=home_root, session_id=secrets.token_hex(8))`
      (c) `executor = executor_factory(...)` (or inline ClaudeProcessAdapter construction)
      (d) `runner = EvalRunner(home=home, config=config, executor=executor,
            run_dir=paths.eval_dir, artifacts_dir=paths.artifacts_dir,
            stdout_path=paths.eval_dir / "stdout.log",
            stderr_path=paths.eval_dir / "stderr.log",
            transcript_path=paths.tty_transcript,
            expect_callables=spec.compiled_expects, keep_home_on_pass=keep_home,
            default_timeout_sec=(spec.timeout_sec or 0) * timeout_mult,
            cancellation_token=cancellation_token)`
      (e) `return runner.run(spec)`
    - Wrap (a)–(e) in a try/except that maps `HomeContainmentViolation` to an
      ERRORED EvalOutcome per D-0048 status-mapping rules.
    - LOC: ~30 (including docstring + try/except).

T7: Add _compute_run_stats + _format_run_summary_line helpers in commands.py
    - Insertion point: after _run_one_spec from T6.
    - _compute_run_stats: ~15 LOC pure-Python aggregator using collections.Counter.
    - _format_run_summary_line: ~3 LOC f-string.
    - LOC: ~22 combined.

T8: Update import block + clear F401 cluster
    - File: src/superclaude/cli/eval/commands.py:30-88.
    - Edits: drop `import os` (line 31); add `import threading` (insert after `import time`);
      add `from .artifact_layout import allocate_per_eval_paths, compose_run_dir, compose_run_id`
      (insert before `from .reporter import Reporter`);
      add `from .claude_process import ClaudeProcessAdapter`
      (insert after the new artifact_layout line).
    - Keep all other imports verbatim; they all become consumed by T1–T7.
    - LOC: ~5 line edits.

T9: Fix Click 8.3.2 mix_stderr regression
    - File: tests/cli/eval/test_eval_group.py:114.
    - Edit: drop `mix_stderr=False` kwarg from `CliRunner(...)` constructor.
      Verify `result.stderr` access at line 117 still works (Click 8.3.2 retains
      the attribute; only the kwarg was removed).
    - LOC: 1 line edited; 0 lines added.

T10: Author tests/cli/eval/test_eval_run.py
    - File: tests/cli/eval/test_eval_run.py (NEW).
    - Test cases (per §6 row 1): 12-flag-help-renders × 1, parallel-clamp × 2,
      AC12-violation-exit-2 × 1, happy-path-exit-0 × 1, failures-exit-1 × 1,
      interrupted-exit-3 × 1. Mock-patch _run_one_spec to return canned EvalOutcome
      so the test does not require a real claude binary or HomeIsolation setup.
    - LOC: ~40-50 (7 test functions × ~6 lines each + fixtures).
```

**Dependency graph**: T1 ← T2 ← T3 ← T4 ← T5 ← T6 ← T7 ← T8 (strictly linear inside `commands.py`; the import block must update last because each new import is only justified by an earlier task's authored helper). T9 is independent of T1–T8 but must land in the same PR to clear the test-eval_group regression. T10 depends on T1–T8 (the test imports the new helpers + patches `_run_one_spec`).

**Wall-clock estimate**: ~2–3 hours of focused implementation by a single agent; ~1 hour for pytest re-runs + ruff verification. Total ~3–4 hours, well inside a single sprint slot.

---

## Hand-off summary

C1 is the conservative, low-blast-radius incarnation of the HYBRID T1+T3 verdict. It authors 11 net-new module attributes (3 constants + 8 functions/wrappers) in `commands.py`, edits one test line, drops `mix_stderr` from the test, and authors one new test file. Every sibling module stays untouched. Every Phase-4 surface that is currently PASS stays PASS. The F401+F821 ruff cluster clears atomically. The five test files that mock-patch `commands._run_one_spec` continue to resolve their patch targets without modification.

**Critical handoff bullets for Phase 2B red-team**:
1. Verify the `_default_output_dir` wrapper does not bypass AC12 — the wrapper *constructs* a path but the existing `resolve_scratch_root(...)` call at the (shifted) line is still the gate.
2. Verify the re-ordering of `started_iso`/`run_id`/`_default_output_dir` around the suite-load step is semantically null (it removes a latent determinism bug but preserves every branch's exit-code path).
3. Verify the `_resolve_executor_factory` shape (zero-arg factory returning a `LifecycleExecutor` instance) is consumable by `_run_one_spec`; if not, the factory may need to take an `ExecutorContext` arg.
4. Verify the `_run_one_spec` HomeIsolation `session_id` allocation (`secrets.token_hex(8)`) does not collide across parallel workers — `secrets.token_hex` is cryptographically random so collision probability is `2^-64` per pair, negligible at parallel-8.
5. Verify no consumer of `commands.py` re-exports `os` (T8 removes the unused `import os` line).
