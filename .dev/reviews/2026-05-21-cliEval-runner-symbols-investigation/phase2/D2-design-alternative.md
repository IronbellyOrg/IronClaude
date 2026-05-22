# D2 — Design Alternative: C2 "Lifted Aggregator"

**Agent:** D2 (alternative-design author for Phase 2A)
**Date:** 2026-05-21
**Candidate under design:** **C2 — Lifted Aggregator.** Promote
`_compute_run_stats` to `RunCounts.from_outcomes` + `RunTotals.from_outcomes`
classmethods on `src/superclaude/cli/eval/models.py`, and promote
`_format_run_summary_line` to a free function inside
`src/superclaude/cli/eval/reporter.py`. Keep thin wrappers in
`commands.py` (2 lines each) so the `commands._compute_run_stats` and
`commands._format_run_summary_line` mock-patch attribute paths remain
valid.
**Scope:** identical to D1 for the other 9 symbols (3 exit-code constants,
6 helpers including 4 sibling-delegating wrappers and 2 stdlib idioms);
C2 differs from C1 ONLY on rows 7 and 8 of the symbol table.
**Phase 1B verdict consumed:** HYBRID T1+T3 @ 0.86 (7 net-new + 4
sibling-wrapper).
**Read-only.** No source-tree edits performed.

---

## §1 — Symbol table (11 symbols, with lift detail on rows 7/8)

| # | Symbol | Home | Implementation sketch | Mock-patch path |
|---|---|---|---|---|
| 1 | `_new_run_id() -> str` | `commands.py` (thin wrapper) | `def _new_run_id() -> str: return compose_run_id(_utc_iso_now(), "")` — zero-arg, closure-free, deferred-to-sibling. **Caveat (Q3 from 1B):** the call site at `commands.py:1467` runs *before* `parsed.name` is known (parse happens at 1512), so suite-name folding into the hash cannot happen here. Two options: (a) accept empty suite_name in the id hash (loses suite distinguishability for simultaneous runs), or (b) defer the run-id materialisation by ~50 lines to after `parsed.name` resolves. **D2 picks (a)** to preserve the existing call ordering and minimise blast radius — design-spec §4 mandates determinism *for a given timestamp + suite*, not collision resistance across suites at the same instant (which is sub-second-improbable on a single host anyway). | `superclaude.cli.eval.commands._new_run_id` (commands.py-local, patchable) |
| 2 | `_default_output_dir(run_id: str) -> Path` | `commands.py` (thin wrapper) | `def _default_output_dir(run_id: str) -> Path: return Path.cwd() / RUN_DIR_PREFIX / datetime.now(timezone.utc).strftime("%Y-%m-%d") / run_id`. NOT `compose_run_dir(...)` because the call site already has `run_id` in hand and the sibling re-derives it (signature mismatch per A4 Evidence B). Imports `RUN_DIR_PREFIX` from `.artifact_layout` (already on the F401-clear path). **Layering note (Q4 from 1B):** the wrapper returns `Path.cwd() / .dev/eval-runs/...` which lives inside the AC12 default allowlist (per `artifact_layout.RUN_DIR_PREFIX` matching the canonical AC12 prefix per artifact_layout.py:79-82), so `resolve_scratch_root` at 1473 accepts it cleanly. | `superclaude.cli.eval.commands._default_output_dir` |
| 3 | `_resolve_executor_factory() -> Callable[[], LifecycleExecutor]` | `commands.py` (factory closure) | `def _resolve_executor_factory(): return lambda: ClaudeProcessAdapter(...)` — but `ClaudeProcessAdapter` is per-eval (needs `home`, `prompt`, etc.) and cannot be zero-arg. **Resolution:** return a *factory of factories* — `def _resolve_executor_factory() -> Callable[[HomeIsolation, EvalSpec], LifecycleExecutor]` that takes the per-eval inputs `_run_one_spec` will have on hand. Closure captures the configured Claude binary path / args from `runtime_config` if needed. Imports `ClaudeProcessAdapter` from `.claude_process` (new import, replaces F401 of `LifecycleExecutor`). | `superclaude.cli.eval.commands._resolve_executor_factory` |
| 4 | `_run_one_spec(spec, *, run_dir, home_root, config, timeout_mult, keep_home, cancellation_token, executor_factory) -> EvalOutcome` | `commands.py` (~30-40 LOC orchestration closure) | (a) `paths = allocate_per_eval_paths(run_dir, spec.id)` (artifact_layout helper); (b) `home = HomeIsolation(eval_id=spec.id, home_root=home_root / spec.id, ...); home.setup()`; (c) `executor = executor_factory(home, spec)`; (d) construct `EvalRunner(home=home, config=config, executor=executor, run_dir=run_dir, artifacts_dir=paths.artifacts_dir, stdout_path=..., stderr_path=..., transcript_path=..., keep_home_on_pass=keep_home, cancellation_token=cancellation_token, default_timeout_sec=(spec.timeout_sec or config.defaults.default_timeout_sec) * timeout_mult)`; (e) try `return runner.run(spec)` with `HomeContainmentViolation` mapped to an `EvalOutcome(status="ERRORED", error_class="HomeContainmentViolation", ...)` and `home.teardown()` in a `finally`. Pinned by the 5 mock-patch tests at `tests/cli/eval/test_no_pty_exclusion.py:266-337`, `test_no_mcp_skip.py:30-528`, etc. — MUST stay a `commands.py` module attribute. | `superclaude.cli.eval.commands._run_one_spec` |
| 5 | `_utc_iso_now() -> str` | `commands.py` (stdlib one-liner) | `def _utc_iso_now() -> str: return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")` — F401-clears `datetime, timezone` imports at line 39. Format is byte-compatible with `artifact_layout._parse_iso` (artifact_layout.py:107-131 accepts both `Z` suffix and `+00:00`). | `superclaude.cli.eval.commands._utc_iso_now` |
| 6 | `_can_install_signal_handler() -> bool` | `commands.py` (stdlib probe) | `def _can_install_signal_handler() -> bool: import threading; return threading.current_thread() is threading.main_thread()`. **Open Q5 from 1B:** choosing probe over try/except for cheap mockability (the 1B verdict noted try/except is harder to test). Adds `import threading` to module imports (new, not in current F401 set). | `superclaude.cli.eval.commands._can_install_signal_handler` |
| 7 | **`_compute_run_stats(outcomes, *, manifest_n) -> tuple[RunCounts, RunTotals]`** ⚠ **LIFTED in C2** | **`models.py` (real logic) + `commands.py` (2-line wrapper)** | **MODELS.PY (lifted classmethods):** `class RunCounts: @classmethod def from_outcomes(cls, outcomes: Sequence[EvalOutcome], *, manifest_n: int) -> "RunCounts":` — counts kept_k (status ∉ {SKIPPED, INTERRUPTED}) and skipped_s (status ∈ {SKIPPED, INTERRUPTED}), sets `expanded_n_prime = len(outcomes)`, and `kept_plus_skipped_equals_n_prime = (kept_k + skipped_s == expanded_n_prime)`. **MIRROR** `class RunTotals: @classmethod def from_outcomes(cls, outcomes: Sequence[EvalOutcome]) -> "RunTotals":` — tallies the 6 per-status counts per DM-012 (XFAIL→passed, XPASS→failed per design-spec line 614). **COMMANDS.PY (thin wrapper):** `def _compute_run_stats(outcomes, *, manifest_n): return RunCounts.from_outcomes(outcomes, manifest_n=manifest_n), RunTotals.from_outcomes(outcomes)`. Wrapper exists *only* to preserve the `commands._compute_run_stats` mock-patch attribute path. | `superclaude.cli.eval.commands._compute_run_stats` (still patchable; wrapper resolves through to lifted methods unless test overrides) |
| 8 | **`_format_run_summary_line(summary: RunSummary, output_dir: Path) -> str`** ⚠ **LIFTED in C2** | **`reporter.py` (real logic) + `commands.py` (2-line wrapper)** | **REPORTER.PY (lifted free function):** `def format_run_summary_line(summary: RunSummary, output_dir: Path) -> str: return f"{summary.run_id}: {summary.totals.passed}P/{summary.totals.failed}F/{summary.totals.skipped}S/{summary.totals.errored}E/{summary.totals.timeout}T → {output_dir}"`. Lives in the reporter neighborhood alongside `render_summary_yaml` (reporter.py:83), which is the existing pattern for one-shot rendering helpers; the new function does NOT call `_check_invariant` because operator-facing stdout has different failure semantics than artefact writes (a stdout line render must never raise on a partial summary). **COMMANDS.PY (thin wrapper):** `def _format_run_summary_line(summary, output_dir): return format_run_summary_line(summary, output_dir)`. | `superclaude.cli.eval.commands._format_run_summary_line` (still patchable) |
| 9 | `RUN_INTERRUPTED_EXIT_CODE: int = 3` | `commands.py` (module-level constant) | Net-new constant; value pinned by design-spec §4 line 590. Convention matches the eight existing `*_EXIT_CODE` constants. **MUST NOT** be lifted to a sibling — Phase 1B implication §1 forbids importing these from any `exit_codes.py` sibling for convention reasons. | `superclaude.cli.eval.commands.RUN_INTERRUPTED_EXIT_CODE` |
| 10 | `RUN_FAILURES_EXIT_CODE: int = 1` | `commands.py` (module-level constant) | Same as #9. Design-spec §4 → 1. | `superclaude.cli.eval.commands.RUN_FAILURES_EXIT_CODE` |
| 11 | `RUN_CLEAN_EXIT_CODE: int = 0` | `commands.py` (module-level constant) | Same as #9. Design-spec §4 → 0. | `superclaude.cli.eval.commands.RUN_CLEAN_EXIT_CODE` |

**C2 differs from C1 ONLY on rows 7 and 8.** Rows 1-6 and 9-11 are
identical between the two candidates by design (Phase 2A prompt
specifies same satisfaction profile for everything except the lift).

---

## §2 — Open-question resolutions (Phase 1B's 5 open Qs)

These are the same resolutions D1 reached for Q1-Q4; **Q5 is the C2-divergent one** and is resolved differently:

* **Q1 — `_compute_run_stats` home (Phase 1B §157):** D1 keeps the
  aggregator in `commands.py`; **D2 LIFTS** it to
  `RunCounts.from_outcomes` + `RunTotals.from_outcomes` classmethods on
  `models.py`. Design-spec is silent (Phase 1A §A1 Q5 surfaces this),
  but design-spec line 614 specifies the orchestrator → reporter
  contract as `from_outcomes(...)` semantically — the spec already uses
  the `from_outcomes` verb-noun. C2 honors that vocabulary directly.
  Identical resolution applies to `_format_run_summary_line` → lift to
  `reporter.py`.
* **Q2 — `compose_run_dir` + scratch-root layering (Phase 1B §159):**
  D2 sidesteps the `compose_run_dir` signature mismatch by authoring a
  thin local wrapper (row 2 above) that constructs the path inline.
  Output lands inside the canonical AC12 allowlist (`Path.cwd() /
  .dev/eval-runs/...` per `artifact_layout.RUN_DIR_PREFIX` matching AC12
  prefix per artifact_layout.py:79-82).
* **Q3 — `_new_run_id` API choice (Phase 1B §161):** D2 picks the
  zero-arg wrapper form (option a from Phase 1B) for minimum call-site
  churn. Empty suite_name fold (per row 1) is the explicit trade-off.
* **Q4 — F401 cleanup atomicity (Phase 1B §163):** D2 lands helper
  authorship + F401 cleanup + lift in a single atomic commit. Smaller
  intermediate ruff-red states are not worth the orchestration
  overhead; the change-set is small (~115-130 LOC total per §1 LOC
  estimate). **C2 atomic commit is slightly larger than C1's** because
  3 files move together — see §8 risk register.
* **Q5 — `_can_install_signal_handler` probe vs try/except (Phase 1B
  §165):** D2 picks the boolean probe (option a from Phase 1B) for
  cheap mockability — five existing tests use
  `monkeypatch.setattr(..._can_install_signal_handler, ...)` patterns
  that work cleanly with a probe and badly with try/except wrapping
  the install call.

---

## §3 — Import block (post-implementation, after F401 cleanup + lift)

The new `commands.py:30-88` import block. Bolded lines are changes
from the current state.

```python
from __future__ import annotations

import json
# import os                              # REMOVED (F401-stale)
import platform
import re
# import secrets                         # REMOVED (F401-stale)
import subprocess
import sys
import threading                          # NEW — backs _can_install_signal_handler
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone   # NOW USED — backs _utc_iso_now + _default_output_dir
from pathlib import Path
from typing import Any, Callable, Iterable, Optional  # Sequence removed (F401-stale)

import click
import yaml

from .artifact_layout import (             # NEW import line
    RUN_DIR_PREFIX,                        # backs _default_output_dir
    allocate_per_eval_paths,               # backs _run_one_spec
    compose_run_id,                        # backs _new_run_id
)
from .capabilities import (
    CapabilityGates,
    CapabilityReport,
    CapabilityStatus,
)
from .claude_process import ClaudeProcessAdapter   # NEW — backs _resolve_executor_factory
from .config import (
    SCRATCH_ROOT_VIOLATION_EXIT_CODE,
    EvalConfig,
    ScratchRootViolation,
    format_scratch_root_violation,
    resolve_scratch_root,
)
from .coverage import (
    COVERAGE_GATE_FAILED_EXIT_CODE,
    CoverageResult,
    coverage_gate,
)
from .disk_budget import (
    DEFAULT_DISK_BUDGET_MB,
    DISK_BUDGET_EXCEEDED_ARTIFACT_NAME,
    DISK_BUDGET_EXCEEDED_EXIT_CODE,
    DISK_BUDGET_RETENTION_ADVICE,
    DiskBudgetPoller,
)
from .isolation import HomeContainmentViolation, HomeIsolation  # NOW USED — backs _run_one_spec
from .loader import (
    SUITE_LOADER_ERROR_EXIT_CODE,
    ParsedSuite,
    SuiteLoader,
    SuiteLoaderError,
)
from .models import (
    EvalOutcome,
    EvalSpec,
    RunCounts,                              # NOW USED — wrapper delegates to RunCounts.from_outcomes
    RunSummary,
    RunTotals,                              # NOW USED — wrapper delegates to RunTotals.from_outcomes
)
from .orchestrator import RunOrchestrator
from .reporter import (                     # CHANGED — also imports format_run_summary_line
    Reporter,
    format_run_summary_line,                # NEW — wrapper delegates to this
)
from .runner import EvalRunner, LifecycleExecutor  # NOW USED — backs _run_one_spec + factory return type
from .signal_handler import CancellationToken, SignalHandlerInstaller
from .suites import SCHEMA_PATH
```

**F401 → consumption mapping (12 imports cleared in lockstep):**

| F401 (current) | Disposition under C2 | Why |
|---|---|---|
| `os` | DELETED | stale; nothing consumes it |
| `secrets` | DELETED | author considered `secrets.token_hex` for run-id but `compose_run_id` is deterministic; the import is dead |
| `datetime` | CONSUMED by `_utc_iso_now` + `_default_output_dir` | per row 5 + row 2 |
| `timezone` | CONSUMED by `_utc_iso_now` + `_default_output_dir` | per row 5 + row 2 |
| `Sequence` | DELETED | stale typing alias |
| `HomeContainmentViolation` | CONSUMED by `_run_one_spec` | per row 4 — try/except in orchestration glue |
| `HomeIsolation` | CONSUMED by `_run_one_spec` | per row 4 — per-eval HOME construction |
| `RunCounts` | CONSUMED by wrapper (still imported) | per row 7 — `RunCounts.from_outcomes(...)` is the lifted call |
| `RunTotals` | CONSUMED by wrapper (still imported) | per row 7 — `RunTotals.from_outcomes(...)` is the lifted call |
| `EvalRunner` | CONSUMED by `_run_one_spec` | per row 4 — runner instantiation |
| `LifecycleExecutor` | CONSUMED by `_resolve_executor_factory` (type hint) | per row 3 — factory return-type annotation |

Plus three NEW imports: `threading` (row 6), `compose_run_id`,
`allocate_per_eval_paths`, `RUN_DIR_PREFIX` (rows 1, 4, 2),
`ClaudeProcessAdapter` (row 3), and `format_run_summary_line` (row 8 —
*the C2-divergent import*).

**Net F401 delta: 12 → 0.** Ruff F401 + F821 both clear.

---

## §4 — Call-graph for revised `eval_run` (commands.py:1406-1695)

No control-flow changes from current state — only the previously-undefined names now resolve. The execution order with the new C2 helpers:

```
eval_run(...)
  ├─ parallel clamp / timeout_mult / max_disk_mb validation   [unchanged: 1443-1461]
  ├─ run_id = _new_run_id()                                   [resolves: compose_run_id(_utc_iso_now(), "")]
  ├─ requested_output = output_dir or _default_output_dir(run_id)  [resolves: Path.cwd() / RUN_DIR_PREFIX / today / run_id]
  ├─ resolved_output = resolve_scratch_root(requested_output, ...) [unchanged]
  ├─ resolved_output.mkdir(...) / home_root.mkdir(...)        [unchanged: 1482-1484]
  ├─ runtime_config = EvalConfig(...allowlist extended...)    [unchanged: 1490-1499]
  ├─ manifest_path = resolve_suite_manifest(suite, ...)       [unchanged: 1505]
  ├─ parsed = SuiteLoader().load(manifest_path)               [unchanged: 1510-1515]
  ├─ specs filter via eval_ids                                [unchanged: 1517-1530]
  ├─ coverage = coverage_gate(...)                            [unchanged: 1541-1548]
  ├─ skip_flags + CapabilityGates                             [unchanged: 1556-1562]
  ├─ poller = DiskBudgetPoller(...) / token = CancellationToken()  [unchanged: 1567-1572]
  ├─ executor_factory = _resolve_executor_factory()           [resolves: lambda home, spec: ClaudeProcessAdapter(...)]
  ├─ def run_one(spec) → _run_one_spec(spec, run_dir, home_root, config, timeout_mult, keep_home, token, executor_factory)
  │     where _run_one_spec internally:
  │       paths = allocate_per_eval_paths(run_dir, spec.id)
  │       home  = HomeIsolation(spec.id, home_root / spec.id, ...).setup()
  │       try: return EvalRunner(home, config, executor_factory(home, spec), run_dir, paths.artifacts_dir, ...).run(spec)
  │       except HomeContainmentViolation: return EvalOutcome(status="ERRORED", error_class="HomeContainmentViolation", ...)
  │       finally: home.teardown() unless keep_home and outcome.status == "PASS"
  ├─ started_iso = _utc_iso_now()                             [resolves: stdlib one-liner]
  ├─ orchestrator = RunOrchestrator(run_one=run_one, ...)     [unchanged: 1615-1619]
  ├─ if SignalHandlerInstaller is not None and _can_install_signal_handler():  [resolves: threading probe]
  │       with SignalHandlerInstaller(token): outcomes = orchestrator.run(...)
  │   else: outcomes = orchestrator.run(...)                  [unchanged: 1622-1628]
  ├─ finished_iso = _utc_iso_now() / duration_sec = ...       [unchanged: 1636-1637]
  ├─ counts, totals = _compute_run_stats(outcomes, manifest_n=manifest_n)
  │     ⚠ C2 DIVERGENCE: wrapper resolves to
  │     RunCounts.from_outcomes(outcomes, manifest_n=manifest_n), RunTotals.from_outcomes(outcomes)
  ├─ summary = RunSummary(run_id=run_id, started_at=started_iso, finished_at=finished_iso, ...)  [unchanged: 1649-1661]
  ├─ Reporter(summary, emit_junit=junit).write(resolved_output)  [unchanged: 1663]
  ├─ if as_json: click.echo(json.dumps(summary.to_dict(), ...))  [unchanged: 1668-1669]
  ├─ elif verbose: click.echo(_format_run_summary_line(summary, resolved_output))
  │     ⚠ C2 DIVERGENCE: wrapper resolves to reporter.format_run_summary_line(summary, resolved_output)
  └─ exit code dispatch                                       [unchanged: 1676-1695]
       if token.is_cancelled(): sys.exit(RUN_INTERRUPTED_EXIT_CODE)  # = 3
       elif poller.is_breached(): ... sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)
       elif totals.failed > 0 or totals.errored > 0 or totals.timeout > 0: sys.exit(RUN_FAILURES_EXIT_CODE)  # = 1
       else: sys.exit(RUN_CLEAN_EXIT_CODE)  # = 0
```

**No call-site reordering.** The HYBRID verdict (Phase 1B §145) flagged
that `started_iso` is computed 145 lines after the `_new_run_id` call;
D2 picks the wrapper form (Q3 resolution above) so the existing call
ordering is preserved.

---

## §5 — Exit-code constants (commands.py module-level)

Added near `HARD_FAIL_EXIT_CODE = 2` at commands.py:550, grouped as a
single 3-line block with a comment:

```python
# Design-spec §4 (commands.py docstring line 1429): the three eval-run
# terminal exit codes. Pinned values 0/1/3 per design-spec.md:590.
# Convention mirrors the eight existing *_EXIT_CODE constants (all = 2
# for harness error); these three constants own the 0 / 1 / 3 surface.
RUN_CLEAN_EXIT_CODE: int = 0
RUN_FAILURES_EXIT_CODE: int = 1
RUN_INTERRUPTED_EXIT_CODE: int = 3
```

**Placement rationale:** Same module as `HARD_FAIL_EXIT_CODE`,
`RUN_BODY_DEFERRED_EXIT_CODE`, `EVAL_NOT_FOUND_EXIT_CODE`,
`SUITE_NOT_FOUND_EXIT_CODE` (all commands.py-local exit-code
constants per A1 §3.1). Lift to a sibling `exit_codes.py` was
explicitly rejected by Phase 1B implication §1.

---

## §6 — Test matrix (test files + expected behaviors)

C2 expands the test surface relative to C1 because the lifted methods
need their own unit tests. **Three test files in scope** (vs C1's
one):

### 6.1 — `tests/cli/eval/test_eval_run.py` (NEW — primary integration surface)

Same as D1: a NEW test module that exercises the wired `eval run`
end-to-end via Click's `CliRunner`. Five test cases:

| Test case | Setup | Expected | Pinned exit code |
|---|---|---|---|
| `test_eval_run_all_pass_exits_0` | Stub `_run_one_spec` returning PASS outcomes for every spec | `result.exit_code == 0`; stdout contains run-id; `summary.{md,json,yaml}` written | `RUN_CLEAN_EXIT_CODE` |
| `test_eval_run_with_failures_exits_1` | Stub `_run_one_spec` returning one FAIL outcome | `result.exit_code == 1`; summary written; failure visible in summary.json | `RUN_FAILURES_EXIT_CODE` |
| `test_eval_run_interrupted_exits_3` | Pre-cancel `CancellationToken` via `_can_install_signal_handler` mock | `result.exit_code == 3`; partial summary still written | `RUN_INTERRUPTED_EXIT_CODE` |
| `test_eval_run_hard_failure_exits_2` | Invalid `--timeout-mult 0` | `result.exit_code == 2`; stderr contains "must be > 0" | `HARD_FAIL_EXIT_CODE` |
| `test_eval_run_disk_breach_exits_2` | Stub `DiskBudgetPoller.is_breached` to True | `result.exit_code == 2`; `DISK_BUDGET_RETENTION_ADVICE` on stderr | `DISK_BUDGET_EXCEEDED_EXIT_CODE` |

Plus the 5 existing skip-gated tests (`test_single_command.py`,
`test_exit_codes.py`, `test_no_pty_exclusion.py`, `test_no_mcp_skip.py`,
`test_validation_commands.py`) un-skip automatically once
`hasattr(cmds, name)` returns True for all 11 names. **Wrapper-based
mock-patch contracts survive intact**: tests patching
`commands._compute_run_stats` and `commands._format_run_summary_line`
still override the wrapper rather than the lifted method, which is the
correct test-mock semantics (test isolates the CLI boundary, not the
model/reporter).

### 6.2 — `tests/cli/eval/test_models.py` ⚠ NEW C2-specific tests

Extends an existing or new test module for the lifted aggregator
classmethods. Two new test cases:

| Test case | Setup | Expected |
|---|---|---|
| `test_run_counts_from_outcomes_kept_skipped_split` | Build a fixture list of 6 `EvalOutcome` instances: 2 PASS, 1 FAIL, 1 ERRORED, 1 SKIPPED, 1 INTERRUPTED. Call `RunCounts.from_outcomes(outcomes, manifest_n=4)`. | Returns `RunCounts(manifest_n=4, expanded_n_prime=6, kept_k=4, skipped_s=2, kept_plus_skipped_equals_n_prime=True)`. Asserts that `expanded_n_prime` is derived from `len(outcomes)` (not `manifest_n`), and that PASS/FAIL/ERRORED/INTERRUPTED bucket correctly. |
| `test_run_totals_from_outcomes_per_status_tally` | Build a fixture with 3 PASS + 2 FAIL + 1 SKIPPED + 1 ERRORED + 1 TIMEOUT + 1 XFAIL (→ passed) + 1 XPASS (→ failed). Call `RunTotals.from_outcomes(outcomes)`. | Returns `RunTotals(passed=4, failed=3, skipped=1, errored=1, interrupted=0, timeout=1)`. Asserts XFAIL/XPASS routing per design-spec line 614. |
| `test_run_counts_from_outcomes_empty` | `RunCounts.from_outcomes([], manifest_n=0)` | Returns `RunCounts(manifest_n=0, expanded_n_prime=0, kept_k=0, skipped_s=0, kept_plus_skipped_equals_n_prime=True)`. Edge case (empty suite). |
| `test_run_counts_from_outcomes_invariant_holds` | Any non-empty fixture | `summary = RunSummary(counts=RunCounts.from_outcomes(outcomes, manifest_n=N), totals=...)` constructs successfully — i.e., `RunSummary.__post_init__`'s invariant guard at models.py:896-912 does NOT raise. |

### 6.3 — `tests/cli/eval/test_reporter.py` ⚠ NEW C2-specific tests

Extends the existing reporter test module (or creates one if absent)
for the lifted `format_run_summary_line` function:

| Test case | Setup | Expected |
|---|---|---|
| `test_format_run_summary_line_basic` | Build a `RunSummary` with known totals (2P/1F/0S/0E/0T) and `output_dir = Path("/tmp/runs/abc")` | Returns a one-line string of shape `<run_id>: 2P/1F/0S/0E/0T → /tmp/runs/abc`. Exact format is the byte-stable contract. |
| `test_format_run_summary_line_no_invariant_check` | Build an intentionally-mismatched `RunSummary`-like object (won't actually construct since `__post_init__` blocks; use a Mock with the right attribute surface) | Function does NOT raise even on a "broken" summary; operator-facing stdout has different semantics than artefact writes. **Distinguishes C2's lifted function from `to_markdown`/`to_yaml`/`to_json` which all call `_check_invariant` first.** |
| `test_commands_wrapper_delegates_to_reporter` | Monkey-patch `superclaude.cli.eval.reporter.format_run_summary_line` with a sentinel; call `commands._format_run_summary_line(summary, path)` | Assert the sentinel was invoked with `(summary, path)`. Pins the wrapper-delegation contract so a future refactor that drops the wrapper without updating the test is caught. |

### 6.4 — Test surface comparison vs C1

* **C1:** 5 new tests in 1 file (`test_eval_run.py`).
* **C2:** 5 new tests in `test_eval_run.py` + 4 new tests in
  `test_models.py` + 3 new tests in `test_reporter.py` = **12 new
  tests across 3 files** (vs C1's 5 across 1).

This is the headline trade-off: C2's lifted methods are individually
testable (good), at the cost of triple the test surface to maintain
(neutral-to-bad).

---

## §7 — Acceptance criteria (identical to C1)

The Phase 1B implications + the hard constraints from the Phase 2A
prompt translate to:

| AC | Description | Verification |
|---|---|---|
| AC1 | All 11 missing symbols resolve | `grep -E "^(def |class |[A-Z_]+\s*[:=])" commands.py models.py reporter.py` shows each of the 11 (with rows 7/8 split across wrapper + lifted), AND `hasattr(commands, name)` returns True for all 11 (preserves the test gate at `test_single_command.py:148-160`) |
| AC2 | Ruff F401 + F821 both clear on `commands.py` | `uv run ruff check src/superclaude/cli/eval/commands.py` returns 0 findings |
| AC3 | Ruff F401 + F821 both clear on `models.py` AND `reporter.py` | C2-specific: the lift adds 0 new F401 in either file (verified at design time — see §8 risk register) |
| AC4 | `RUN_*_EXIT_CODE` constants live in `commands.py` | `grep "^RUN_.*_EXIT_CODE" commands.py` returns 3 matches; `grep -r "RUN_.*_EXIT_CODE" src/superclaude/cli/eval/ --include="*.py" -l` includes ONLY `commands.py` |
| AC5 | `_run_one_spec`, `_compute_run_stats`, `_format_run_summary_line` are `commands.py` module attributes | `python -c "from superclaude.cli.eval import commands; assert all(hasattr(commands, n) for n in ['_run_one_spec', '_compute_run_stats', '_format_run_summary_line'])"`. C2 satisfies this via the thin wrappers; lifted real-impl lives elsewhere but the patch-able attribute path is preserved. |
| AC6 | `RunCounts.from_outcomes` + `RunTotals.from_outcomes` exist on `models.py` | C2-specific: `python -c "from superclaude.cli.eval.models import RunCounts, RunTotals; assert callable(RunCounts.from_outcomes); assert callable(RunTotals.from_outcomes)"` |
| AC7 | `format_run_summary_line` exists in `reporter.py` `__all__` | C2-specific: `from superclaude.cli.eval.reporter import format_run_summary_line` works, and the function appears in the `__all__` list at reporter.py:69-75 |
| AC8 | The 5 skip-gated tests un-skip and pass | `uv run pytest tests/cli/eval/test_single_command.py tests/cli/eval/test_exit_codes.py tests/cli/eval/test_no_pty_exclusion.py tests/cli/eval/test_no_mcp_skip.py tests/cli/eval/test_validation_commands.py -v` shows no skips with reason "T04.10 deliverables not yet landed" |
| AC9 | NEW `test_eval_run.py` passes all 5 cases | `uv run pytest tests/cli/eval/test_eval_run.py -v` exits 0 |
| AC10 | NEW lifted-method tests pass | C2-specific: `uv run pytest tests/cli/eval/test_models.py::test_run_counts_from_outcomes tests/cli/eval/test_reporter.py::test_format_run_summary_line -v` exits 0 |
| AC11 | No edits to already-passing P3/P4 surface beyond `commands.py`, `models.py`, `reporter.py` | `git diff --stat` shows ONLY these three files in `src/` plus the test files in §6 |
| AC12 | `make verify-sync` passes after the change | `src/superclaude/cli/eval/` is the source of truth; no `.claude/` sibling exists for this module (entire eval tree is untracked, so sync-dev is a no-op here) |

**Satisfaction profile is identical to C1** — the test prompt's
hard-constraint #4 ("No edits to already-passing P3/P4 surface") is
honored because P3/P4 surface refers to *non-runner-related* modules.
`models.py` and `reporter.py` ARE in scope for runner-symbol resolution
work (they are immediate neighbors of `commands.py` in the runner path)
and the lift adds, never modifies, existing API surface.

---

## §8 — Risk register (with the C2-specific NEW risks)

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-D1 | `_default_output_dir` (row 2) inlines `RUN_DIR_PREFIX` instead of calling `compose_run_dir`; if the layout convention ever changes, two surfaces drift | LOW | MEDIUM | Test pinning: `tests/cli/eval/test_artifact_layout.py` already tests `compose_run_dir`; add a parallel test that `_default_output_dir(run_id)` and `compose_run_dir(Path.cwd(), iso, "")` produce paths whose last segment matches |
| R-D2 | `_new_run_id` (row 1) folds empty suite_name into the hash; two simultaneous runs against different suites at the same second on the same host collide | LOW | LOW | Sub-second-on-same-host simultaneous-different-suite is a contrived scenario; if it ever matters, escalate to option (b) of row 1 (defer run-id materialisation by 50 lines). Design-spec §4 line 590 mandates determinism *for a given timestamp + suite*, not collision resistance across simultaneous suites |
| R-D3 | `_resolve_executor_factory` (row 3) returns a factory-of-factories whose signature `(HomeIsolation, EvalSpec) -> LifecycleExecutor` is not pinned anywhere | LOW | MEDIUM | The factory is consumed at exactly one call site (line 1577 → row 4 closure). Add a type alias `ExecutorFactory = Callable[[HomeIsolation, EvalSpec], LifecycleExecutor]` in `commands.py` near the constants, and use it in both the factory return annotation and the row-4 parameter annotation |
| R-D4 | `_run_one_spec` (row 4) is ~40 LOC of orchestration glue; bugs in the HOME setup or runner construction path would surface as ERRORED for every eval | MEDIUM | HIGH | The 5 mock-patch tests (`test_no_mcp_skip.py:528` etc.) override the entire helper, so test coverage of the *body* is the new `test_eval_run.py::test_eval_run_all_pass_exits_0` case (with stubbed sibling helpers). Plus the orchestrator's existing `_errored_outcome` fallback (orchestrator.py:354) catches construction failures and converts to an ERRORED outcome rather than crashing the run |
| R-D5 | `_can_install_signal_handler` (row 6) probes for main-thread; CliRunner-based tests run on main thread so always True, but a future async test runner would flip the branch and skip the SignalHandlerInstaller path silently | LOW | LOW | Test in `test_eval_run.py::test_eval_run_interrupted_exits_3` mocks the probe to True explicitly so it never silently flips. Document the probe semantics in a comment near the call site |
| R-D6 | F401 cleanup atomic commit + lift in same change-set; if the commit fails review, both the C2 lift AND the F401 cleanup land in the rework | MEDIUM | LOW | C1 has the same risk at smaller scale. Mitigation: structure the commit as 3 logical chunks (a) lifted methods in models.py + reporter.py, (b) wrappers + 11 symbols in commands.py, (c) F401 import cleanup. Review can be done chunk-at-a-time even if the commit is atomic |
| **R-D7** ⚠ **C2-specific NEW** | **Circular-import potential: `reporter.py` already imports `RunSummary` from `models.py`; if a future `RunSummary` change needs to import from `reporter.py` for type hints, the cycle bites** | LOW | MEDIUM | Verified at design time: `reporter.py` imports go `models → reporter`, never the other direction. The lifted `format_run_summary_line` takes `RunSummary` + `Path` — both stdlib/models, no reporter→commands dependency introduced. `commands.py` already imports `reporter.Reporter`, so adding `format_run_summary_line` to the same import line is structurally identical. **No new cycle introduced.** |
| **R-D8** ⚠ **C2-specific NEW** | **Lifted code in `models.py` increases that file's blast radius; a buggy `RunCounts.from_outcomes` corrupts every consumer of `RunSummary` (Reporter, JSON renderer, JUnit renderer, the future T03.11 contract guard)** | LOW | HIGH | The `__post_init__` invariant guard at models.py:896-912 already catches counts inconsistencies. The new test in §6.2 (`test_run_counts_from_outcomes_invariant_holds`) exists specifically to prove the lifted classmethod produces invariant-satisfying instances. Plus `_check_invariant` in `run_report.py` re-verifies at every render call. Triple-layered defense |
| **R-D9** ⚠ **C2-specific NEW** | **Wrapper-delegation indirection adds debugging cognitive load: a test failure tracing through `commands._compute_run_stats` → `RunCounts.from_outcomes` is 2 hops instead of 1; future maintainers may not know about the wrapper** | MEDIUM | LOW | Add a 3-line comment above each wrapper in `commands.py` explaining: (a) the lifted home of the real logic, (b) why the wrapper exists (mock-patch contract preservation), (c) a link to this design spec. Future maintainers see the wrapper, read the comment, navigate to the real impl. Cost = 6 LOC of comments |
| **R-D10** ⚠ **C2-specific NEW** | **3-file atomic change-set means the Phase-2B red-team has more attack surface; a defensible 1-file diff (C1) is easier to review than 3 coordinated diffs (C2)** | MEDIUM | MEDIUM | This is the headline C2 cost. See §10 comparison table for the explicit C1-vs-C2 verdict. Accept the cost only if the red-team values cohesion (C2's strength) over blast-radius minimization (C1's strength). My recommendation in §10: red-team should prefer C1 for this release and revisit C2 at v2 |

---

## §9 — Atomic tasks (~13 tasks for C2; vs ~10 for C1)

Tasks are designed to be parallel-safe except where ordering is noted.

| # | Task | Files | Parallel-safe? | LOC est |
|---|---|---|---|---|
| T1 | Add 3 `RUN_*_EXIT_CODE` module-level constants near commands.py:550 | commands.py | YES (no dependencies) | +5 |
| T2 | Author `_utc_iso_now()` one-liner | commands.py | YES | +3 |
| T3 | Author `_can_install_signal_handler()` boolean probe + add `threading` import | commands.py | YES | +3 |
| T4 | Author `_new_run_id()` wrapper around `compose_run_id` | commands.py | Blocks-on T2 (calls `_utc_iso_now`) | +3 |
| T5 | Author `_default_output_dir(run_id)` inline | commands.py | YES | +3 |
| T6 | Author `_resolve_executor_factory()` returning per-eval factory + `ExecutorFactory` type alias | commands.py | YES | +8 |
| **T7a** ⚠ **C2-specific** | **Author `RunCounts.from_outcomes` classmethod in models.py** | **models.py** | **YES (pure addition, no existing edits)** | **+15** |
| **T7b** ⚠ **C2-specific** | **Author `RunTotals.from_outcomes` classmethod in models.py** | **models.py** | **YES (pure addition)** | **+12** |
| **T7c** ⚠ **C2-specific** | **Author `_compute_run_stats` 2-line wrapper in commands.py delegating to T7a + T7b** | **commands.py** | **Blocks-on T7a, T7b** | **+3** |
| **T8a** ⚠ **C2-specific** | **Author `format_run_summary_line` free function in reporter.py + add to `__all__`** | **reporter.py** | **YES (pure addition)** | **+8** |
| **T8b** ⚠ **C2-specific** | **Author `_format_run_summary_line` 2-line wrapper in commands.py delegating to T8a** | **commands.py** | **Blocks-on T8a** | **+3** |
| T9 | Author `_run_one_spec(...)` ~40-LOC orchestration closure | commands.py | Blocks-on T6 (uses `_resolve_executor_factory` indirectly via factory parameter) | +40 |
| T10 | Update import block: add `threading`, `artifact_layout.{compose_run_id, allocate_per_eval_paths, RUN_DIR_PREFIX}`, `claude_process.ClaudeProcessAdapter`, `reporter.format_run_summary_line`; remove `os`, `secrets`, `Sequence` | commands.py | Blocks-on all of T1-T9 (must land last to clear F401/F821) | +6/-3 net |
| T11 | NEW `tests/cli/eval/test_eval_run.py` with 5 test cases per §6.1 | tests/cli/eval/test_eval_run.py | YES | +120 |
| **T12** ⚠ **C2-specific** | **NEW or extended `tests/cli/eval/test_models.py` with 4 lifted-method test cases per §6.2** | **tests/cli/eval/test_models.py** | **YES** | **+80** |
| **T13** ⚠ **C2-specific** | **NEW or extended `tests/cli/eval/test_reporter.py` with 3 lifted-function test cases per §6.3** | **tests/cli/eval/test_reporter.py** | **YES** | **+50** |
| T14 | Run `uv run ruff check src/superclaude/cli/eval/{commands,models,reporter}.py` + `uv run pytest tests/cli/eval/ -v` to verify AC1-AC12 | (verification only) | Blocks-on T1-T13 | 0 |

**Total atomic tasks: 14 (vs C1's ~10).** The 4 extra tasks are the
lift overhead: T7a, T7b, T8a are pure-addition tasks in
models.py/reporter.py; T7c, T8b are the 2-line wrappers in commands.py;
T12 and T13 are the new test files.

**Recommended execution wave (parallel-first):**

* **Wave 1 (no deps, fully parallel):** T1, T2, T3, T5, T6, T7a, T7b,
  T8a — 8 tasks in parallel
* **Wave 2 (depends on Wave 1):** T4 (needs T2), T7c (needs T7a+T7b),
  T8b (needs T8a), T9 (needs T6 implicitly via factory parameter) — 4
  tasks in parallel
* **Wave 3 (depends on Wave 2):** T10 import cleanup — 1 task
* **Wave 4 (depends on Wave 3, parallel):** T11, T12, T13 — 3 test
  modules in parallel
* **Wave 5 (verification):** T14 ruff + pytest

This is 5 waves vs C1's ~3-4 — the lift adds one wave but does not
explode the critical path because the lifted methods are pure
additions that don't block the commands.py work.

---

## §10 — C1 vs C2 trade-off table ⚠ D2-only required section

The Phase 2A prompt asks D2 to produce a neutral side-by-side comparison.
This table is the deliverable.

| Dimension | C1 (in-place) | C2 (lifted) | Winner |
|---|---|---|---|
| **LOC delta** | ~70 added in commands.py; 0 elsewhere | ~50 commands.py + ~40 models.py + ~25 reporter.py = ~115 across 3 files | **C1** by raw LOC; **C2** by per-file diff (smaller commands.py) |
| **Cohesion (semantic placement)** | aggregator in CLI module (smell — aggregation logic belongs with the data, formatting belongs with the renderer) | aggregator with data class (RunCounts/RunTotals own their construction); formatter with reporter (same neighborhood as render_summary_yaml) | **C2** — the lift is semantically correct; design-spec line 614 already uses `from_outcomes` vocabulary |
| **Test surface (file count)** | 1 file (`test_eval_run.py`, 5 cases) | 3 files (`test_eval_run.py` 5 cases + `test_models.py` 4 cases + `test_reporter.py` 3 cases) | **C1** — 1 file is less to maintain |
| **Test surface (case count)** | 5 new test cases | 12 new test cases (2.4× C1) | **C1** by count; **C2** by isolation (lifted methods get dedicated unit tests independent of CLI plumbing) |
| **Blast radius (files touched)** | 1 source file (commands.py) | 3 source files (commands.py + models.py + reporter.py) | **C1** — single-file diff is the gold standard for low-risk change-sets |
| **Mock-patch contract preservation** | preserved trivially (the function IS the module attribute) | preserved via 2-line wrappers (the wrapper resolves to the module attribute; tests patch the wrapper, which is the documented contract surface) | **tie** — both honor hard-constraint #5; C2 pays a 6-LOC wrapper tax for the indirection |
| **Future extensibility** | new aggregations (e.g., a `RunCounts.from_summaries` for cross-run reports) require commands.py edits + relocation later | RunCounts/RunTotals naturally grow new classmethods next to `from_outcomes`; reporter.py naturally grows new formatters next to `format_run_summary_line` | **C2** — the lift is the right shape for the next 2-3 quarters of feature work |
| **Phase-2B red-team attack surface** | LOW — only commands.py to attack; the diff is contiguous in one function body | MEDIUM — 3 files coordinated; red-team can attack the cross-file consistency, the wrapper-delegation contract, the lifted classmethod's invariant satisfaction, and the new test trio independently | **C1** — smaller attack surface = faster red-team turnaround = lower risk of bouncing back from Phase 2B with rework |
| **Code-review cognitive load** | Single-file read in one sitting (~70 LOC) | 3-file read across `models.py` + `reporter.py` + `commands.py`; reviewer must context-switch between data, renderer, and CLI | **C1** — easier to review; C2 reviewers must mentally hold 3 file structures simultaneously |
| **Reversibility** | Trivially reversible (revert one file) | Reversible but requires careful 3-file revert; if a follow-up commit lands between C2 and the revert, the revert is non-trivial | **C1** — single-file reverts are atomic |
| **Compatibility with HYBRID T1+T3 verdict** | Honors T1 ("net-new authoring in commands.py") for rows 7-8 | Honors T3 ("belong elsewhere") for rows 7-8 | **C2** — closer to the literal HYBRID classification per Phase 1B §85 row 7's "Open question (Q5 from A1)" note |
| **Risk of merge conflict with concurrent runner work** | LOW — commands.py is the only contention point | MEDIUM — models.py is touched by every data-model evolution task; reporter.py is touched by every output-format task; both have higher base merge-conflict rates than commands.py | **C1** — picks the file with the lowest concurrent-edit probability |
| **Recommendation** | **ship for this release (Phase 1B-resolved HYBRID with minimum blast radius)** | **hold for a v2 refactor (cohesion improvement worth doing, but not under deadline pressure)** | **C1 for THIS release; C2 as a follow-up cleanup ticket** |

**D2's red-team-facing verdict (Phase 2B preview):**

The honest read is that C1 wins on every operational metric (blast
radius, test count, review effort, reversibility, merge-conflict risk)
EXCEPT cohesion and future extensibility, where C2 is materially
better. For a release that is ALREADY under pressure from the broader
phase-5 sprint workload (per `manifest.json` + recent checkpoints in
`.dev/releases/current/task-builder-merge/`), the operational metrics
should dominate.

**Recommended Phase-2B input:** the red-team should challenge C2 on
"why are we taking 3-file blast radius for a cohesion improvement
that adds 12 test cases when C1 ships with 5 test cases and 1-file
blast radius?" If C2 can't produce a deadline-aware answer to that
question, C1 wins. My honest assessment as D2: I cannot produce that
answer for the current release window. **Recommend Phase 2B selects
C1 as the merged solution; file C2 as a v2 follow-up cleanup ticket.**

This is the unusual situation where the alternative-design author
(me, D2) recommends the *baseline* (C1) for shipping. The
alternative-design's job is to surface a defensible Plan B, not to
advocate for it when the trade-off math doesn't support it. C2's
trade-off math does not support it for THIS release.

---

## Process notes

* **Verification tier** sources used: file:line citations for all
  signatures (commands.py:550, 1467, 1469, 1577, 1598, 1612, 1624,
  1636, 1642, 1671, 1677, 1694, 1695; models.py:732, 786, 896-912;
  reporter.py:69-75, 83, 145-227; artifact_layout.py:79-82, 107-131,
  139-159, 162-192; design-spec.md:202-208, 577-590, 614).
* **Discovery tier** judgments flagged inline: the lift-vs-keep
  cohesion judgment (§10 row "Cohesion"); the merge-conflict-risk
  estimate (§10 row "Risk of merge conflict"); the recommendation that
  D2 itself favors C1 over C2 for this release (§10 final
  recommendation).
* **No source-tree edits performed.** This is a read-only artifact;
  the implementation is downstream in Phase 3 / hand-off.
* **Output path:** `/config/workspace/IronClaude/.dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/phase2/D2-design-alternative.md`
