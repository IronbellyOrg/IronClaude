# A4 — Thesis 3: "Belong Elsewhere" (Consolidation, Not Authoring)

**Agent**: A4 (defender of Thesis 3)
**Defect under investigation**: 11 F821 undefined names + 12 F401 unused imports in `src/superclaude/cli/eval/commands.py:eval_run` (lines 1406–1695), causing sprint phases 4 and 5 to `FAIL`.
**Verdict**: **Thesis 3 is PARTIALLY validated for 4–5 of 11 symbols** (sibling helpers exist with usable signatures or can be wrapped trivially), but **FALSIFIED for the 3 RUN_*_EXIT_CODE constants** and **WEAK for several "compute/format" placeholders**. Overall confidence: **0.30**.

The honest read of the evidence is that the author of `eval_run` was reaching for *a mix of* (a) sibling helpers that already exist (HIGH equivalence) and (b) glue/aggregator helpers and integer constants that have no canonical home in any sibling module. Pure "consolidation" closes ~40% of the gap; the remainder must be authored either inside `commands.py` (Thesis 1) or as ghost-renames of stdlib idioms (Thesis 2 territory). I will defend Thesis 3 as the dominant *intent signal* — the author clearly tried to delegate to siblings — even where the strict equivalence test fails.

---

## Front-and-center: 11-row semantic equivalence table

Verification-tier evidence (verbatim signatures) follows the table.

| # | Missing symbol (call-site) | Candidate sibling (file:line) | Signature match | Confidence | Call-site rewrite required |
|---|---|---|---|---|---|
| 1 | `_new_run_id()` @ commands.py:1467 | `artifact_layout.compose_run_id(started_at: str, suite_name: str = "") -> str` @ artifact_layout.py:139 | **N** (zero-arg vs 2-arg) | **MED** | YES — call site must move below `started_iso` assignment OR pass `(started_iso, parsed.name)`; today the call happens BEFORE `started_iso` is computed (1467 vs 1612). |
| 2 | `_default_output_dir(run_id)` @ commands.py:1469 | `artifact_layout.compose_run_dir(output_root, started_at, suite_name="")` @ artifact_layout.py:162 | **N** (different parameters — passed `run_id` arg, but `compose_run_dir` takes `output_root + started_at + suite_name` and derives the run-id internally) | **MED** | YES — entire ordering needs reshuffle; `started_at` must be computed first. |
| 3 | `_resolve_executor_factory()` @ commands.py:1577 | `claude_process.ClaudeProcessAdapter` (claude_process.py:107) — production `LifecycleExecutor` impl | **N** (no zero-arg factory function exists; only a class is available) | **LOW** | YES — author must either add a factory wrapper or hardcode `ClaudeProcessAdapter`-based construction inline. |
| 4 | `_run_one_spec(spec, run_dir=..., home_root=..., config=..., timeout_mult=..., keep_home=..., cancellation_token=..., executor_factory=...)` @ commands.py:1598 | `runner.EvalRunner(...).run(spec)` (runner.py:754 ctor + runner.py:823 `run`); skeleton `runner.run_eval(...)` (runner.py:177) | **PARTIAL** — `EvalRunner.__init__` shares most kwargs (`home`, `config`, `run_dir`, `artifacts_dir`, `stdout_path`, `stderr_path`, `transcript_path`, `executor`, `keep_home_on_pass`, `cancellation_token`) but is per-spec not per-run; takes a *single* `home: HomeIsolation` instance, not a `home_root` directory | **MED** | YES — `_run_one_spec` must (a) call `allocate_per_eval_paths(run_dir, spec.id)`, (b) construct a fresh `HomeIsolation` rooted at `home_root / spec.id`, (c) construct `EvalRunner(...)` and call `.run(spec)`. This is *glue logic that does not exist anywhere in the tree* — it has to be authored, but using sibling-module APIs throughout. |
| 5 | `_utc_iso_now()` @ commands.py:1612, 1636 | None directly. Stdlib idiom: `datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")` (compatible with `artifact_layout._parse_iso` per artifact_layout.py:107–131) | **N** (no sibling helper) | **LOW** | YES — author the helper inline OR inline the stdlib expression. The `datetime, timezone` imports at commands.py:38 are F401 — strong signal the author *intended* to write this inline and forgot. |
| 6 | `_can_install_signal_handler()` @ commands.py:1624 | `signal_handler.SignalHandlerInstaller.install` raises `ValueError` from off-main-thread (signal_handler.py:203). The pattern `threading.current_thread() is threading.main_thread()` is the literal probe. | **N** (no helper function — only the eager check inside `install()`) | **LOW** | YES — author the probe inline (~2 lines) OR catch the `ValueError` from `__enter__`. |
| 7 | `_compute_run_stats(outcomes, manifest_n=manifest_n) -> (RunCounts, RunTotals)` @ commands.py:1642 | None. `models.RunCounts` (models.py:733) and `models.RunTotals` (models.py:786) are dataclasses; no aggregator exists in any sibling module. | **N** (data classes exist; aggregator does not) | **NONE** | YES — pure new authoring. The F401 imports of `RunCounts` and `RunTotals` at commands.py:80,82 are the smoking gun: the author *imported the types* but never wrote the aggregator. |
| 8 | `_format_run_summary_line(summary, resolved_output)` @ commands.py:1671 | `reporter.Reporter(summary).to_markdown()` exists (reporter.py:150) but returns the FULL markdown body, not a one-line operator-facing string. `run_report.render_summary_markdown` (run_report.py:137) — same story. | **N** (wrong granularity — one-line vs multi-line) | **LOW** | YES — pure new authoring (a one-liner like `f"{summary.run_id}: {totals.passed}/{totals.failed}/... → {resolved_output}"`). |
| 9 | `RUN_INTERRUPTED_EXIT_CODE` @ 1677 | design-spec §4 mandates **`3`** for interrupted; no constant exists in any sibling. Same module has the pattern (HARD_FAIL_EXIT_CODE etc.). | **N** | **NONE** | NO — these constants belong in commands.py (Thesis 1). The naming convention matches the eight existing `*_EXIT_CODE` constants in commands.py / sibling modules and design-spec §4 dictates the integer values. |
| 10 | `RUN_FAILURES_EXIT_CODE` @ 1694 | design-spec §4 → **`1`** | **N** | **NONE** | NO — same as 9. |
| 11 | `RUN_CLEAN_EXIT_CODE` @ 1695 | design-spec §4 → **`0`** | **N** | **NONE** | NO — same as 9. |

**Score tally**:
- HIGH-confidence sibling equivalent: **0/11**
- MED-confidence: **3/11** (`_new_run_id`, `_default_output_dir`, `_run_one_spec`)
- LOW-confidence: **4/11** (`_resolve_executor_factory`, `_utc_iso_now`, `_can_install_signal_handler`, `_format_run_summary_line`)
- NO sibling equivalent: **4/11** (`_compute_run_stats`, RUN_*_EXIT_CODE × 3)

This is **not** the table a strong "Belong Elsewhere" thesis would produce. The strongest read of Thesis 3 — that consolidation alone fixes the defect — is false. The weaker read — that the author *intended* to consolidate and stranded the call sites with placeholders — is well-supported by the F401 evidence.

---

## Verification-tier evidence (verbatim signatures + file:line)

### Evidence A — `_new_run_id` ↔ `compose_run_id`

**Call site** (commands.py:1467):
```
    run_id = _new_run_id()
```
The call has **zero arguments**. The next line (1469) immediately uses `run_id`.

**Sibling candidate** (artifact_layout.py:139):
```
def compose_run_id(started_at: str, suite_name: str = "") -> str:
    """Return the per-run identifier for ``(started_at, suite_name)``.
    Shape: ``<HHMMSSZ>-<8-hex>`` where the 8-hex tail is the first
    :data:`_RUN_ID_HASH_LEN` chars of
    ``sha256(suite_name + "\\n" + started_at)``.
```

**Signature delta**: 0-arg call vs 2-arg function. The `started_at` arg comes from `started_iso = _utc_iso_now()` at line 1612 — which is **145 lines BELOW** the `run_id = _new_run_id()` call at 1467. The body's ordering is wrong: the author needs `started_iso` *before* the run_id is composed.

**The smoking gun**: tests `test_artifact_reproducibility.py:67` already import `compose_run_id` and use it as `compose_run_id(_STARTED_AT, _SUITE_NAME)`. The contract is set; commands.py is the **only consumer** that didn't migrate to it.

### Evidence B — `_default_output_dir` ↔ `compose_run_dir`

**Call site** (commands.py:1469):
```
    requested_output = (
        output_dir if output_dir is not None else _default_output_dir(run_id)
    )
```

**Sibling candidate** (artifact_layout.py:162):
```
def compose_run_dir(
    output_root: Path | str,
    started_at: str,
    suite_name: str = "",
) -> Path:
    """Return ``<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``.
```

**Signature delta**: receiver takes `run_id` arg; `compose_run_dir` takes `(output_root, started_at, suite_name)` and derives `run_id` internally via `compose_run_id` (artifact_layout.py:191). The semantic intent matches the design-spec language ("the resolved ``--output-dir``" — see commands.py:1426 docstring), but the call-site argument list is incompatible.

### Evidence C — `_run_one_spec` ↔ `EvalRunner.run`

**Call site** (commands.py:1598):
```
        return _run_one_spec(
            spec,
            run_dir=resolved_output,
            home_root=home_root,
            config=runtime_config,
            timeout_mult=timeout_mult,
            keep_home=keep_home,
            cancellation_token=token,
            executor_factory=executor_factory,
        )
```

**Sibling candidate** (runner.py:754):
```
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
and `runner.py:823`:
```
    def run(self, spec: EvalSpec) -> EvalOutcome:
```

**Signature delta**: kwarg names overlap heavily (`config`, `run_dir`, `cancellation_token`, `keep_home_on_pass`) but `EvalRunner` is **per-spec, per-HOME**, not per-run. The missing helper `_run_one_spec` is precisely the glue that needs to: (1) `allocate_per_eval_paths(run_dir, spec.id)` from artifact_layout, (2) build a fresh `HomeIsolation(home_root / spec.id, ...)`, (3) call `executor_factory()` to produce the executor, (4) construct `EvalRunner(...)` against all of that, (5) return `EvalRunner.run(spec)`. None of that glue exists anywhere — but every primitive does.

### Evidence D — `_resolve_executor_factory` ↔ `ClaudeProcessAdapter`

**Call site** (commands.py:1577):
```
    executor_factory = _resolve_executor_factory()
```

**Sibling candidate**: `claude_process.ClaudeProcessAdapter` (claude_process.py:107) is the production `LifecycleExecutor` impl. There is **no `default_executor_factory` or similar function**. The closest pattern: tests construct executors directly per call site. The "factory" abstraction appears nowhere else in the tree.

### Evidence E — `RUN_*_EXIT_CODE` and design-spec §4

**Design-spec §4 (verbatim, design-spec.md ~lines 200–207)**:
```
### Exit codes

| Code | Meaning |
|---|---|
| `0` | All evals PASSED (or correctly SKIPPED due to capability gates). |
| `1` | At least one eval FAILED. |
| `2` | Harness error (manifest invalid, claude binary missing, etc.). |
| `3` | Interrupted (SIGINT during run). |
```

These map to: `RUN_CLEAN_EXIT_CODE=0`, `RUN_FAILURES_EXIT_CODE=1`, `RUN_INTERRUPTED_EXIT_CODE=3`. They are *new* constants that follow the **same convention** as the eight existing `*_EXIT_CODE` constants in commands.py / sibling modules (HARD_FAIL_EXIT_CODE, SCRATCH_ROOT_VIOLATION_EXIT_CODE, SUITE_NOT_FOUND_EXIT_CODE, SUITE_LOADER_ERROR_EXIT_CODE, EVAL_NOT_FOUND_EXIT_CODE, COVERAGE_GATE_FAILED_EXIT_CODE, DISK_BUDGET_EXCEEDED_EXIT_CODE, REPORTER_CONTRACT_VIOLATION_EXIT_CODE — see commands.py:46–88 import block).

**This is the weakest point of Thesis 3 and I concede it openly**: the three RUN_*_EXIT_CODE constants belong in `commands.py` itself (Thesis 1 wins this row), not in a sibling. They cannot be "consolidated" because there is nothing to consolidate to.

### Evidence F — Import block at commands.py:30–88 (verbatim, with F401 annotations)

```
import json
import os                           # F401 — unused
import platform
import re
import secrets                      # F401 — unused
import subprocess
import sys
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone        # F401 — datetime, timezone unused
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Sequence  # F401 — Sequence

import click
import yaml

from .capabilities import (CapabilityGates, CapabilityReport, CapabilityStatus,)
from .config import (SCRATCH_ROOT_VIOLATION_EXIT_CODE, EvalConfig, ScratchRootViolation, format_scratch_root_violation, resolve_scratch_root,)
from .coverage import (COVERAGE_GATE_FAILED_EXIT_CODE, CoverageResult, coverage_gate,)
from .disk_budget import (DEFAULT_DISK_BUDGET_MB, DISK_BUDGET_EXCEEDED_ARTIFACT_NAME, DISK_BUDGET_EXCEEDED_EXIT_CODE, DISK_BUDGET_RETENTION_ADVICE, DiskBudgetPoller,)
from .isolation import HomeContainmentViolation, HomeIsolation  # F401 — both unused
from .loader import (SUITE_LOADER_ERROR_EXIT_CODE, ParsedSuite, SuiteLoader, SuiteLoaderError,)
from .models import (EvalOutcome, EvalSpec, RunCounts, RunTotals, RunSummary,)  # F401 — RunCounts, RunTotals
from .orchestrator import RunOrchestrator
from .reporter import Reporter
from .runner import EvalRunner, LifecycleExecutor   # F401 — both unused
from .signal_handler import CancellationToken, SignalHandlerInstaller
from .suites import SCHEMA_PATH
```

**F401-derived intent signal — the strongest piece of Thesis 3's argument**:

The F401 unused-imports list at `.dev/releases/current/cliEval/evidence/T04.22/ruff-check.log` reveals SIX semantically-loaded imports the author brought in but never invoked:
- `from .isolation import HomeIsolation` — needed for `_run_one_spec` glue (#4 above)
- `from .isolation import HomeContainmentViolation` — would catch isolation breaches
- `from .models import RunCounts, RunTotals` — return-types for `_compute_run_stats` (#7)
- `from .runner import EvalRunner, LifecycleExecutor` — would be the executor type in `_run_one_spec` (#4)
- `from datetime import datetime, timezone` — would be the building blocks of `_utc_iso_now` (#5)

**This is a near-decisive intent signal**: the author imported every sibling helper they would have needed *if they were going to write the glue* — and then left the placeholder names dangling. The pattern is consistent with "I was reaching toward sibling modules, got interrupted, never came back". It is *not* consistent with Thesis 2 (rename ghosts) because no `datetime → utc_iso_now` or `EvalRunner → _run_one_spec` rename exists in git log. It is *partially* consistent with Thesis 1 (forgotten-author) but Thesis 1 cannot explain why the F401 imports are sibling helpers rather than stdlib.

### Evidence G — `eval_describe` precedent (commands.py:1213)

```
def eval_describe(...) -> None:
    ...
    try:
        payload = describe_suite(suite, suites_dir=target, eval_id=eval_id)
    except SuiteNotFound as exc:
        click.echo(f"eval describe: {type(exc).__name__}: {exc}", err=True)
        sys.exit(SUITE_NOT_FOUND_EXIT_CODE)
    ...
```

`eval_describe` calls sibling helpers (`describe_suite`, `render_describe_json`, `render_describe_yaml`, `resolve_suite_manifest`) **directly** — no local re-aliasing, no `_local_helper_wrapping_describe_suite()` placeholder. This **is** the project convention. `eval_run` is the outlier; it should follow the same pattern. That fact is the central evidence for Thesis 3.

### Evidence H — Test files explicitly patch the missing names

The smoking-gun-est piece of evidence sits in `tests/cli/eval/test_no_mcp_skip.py:28–34`, `test_single_command.py:139–162`, `test_exit_codes.py:36–108`, `test_no_pty_exclusion.py:298–312`, `test_retention_policy.py:35–94`:

> "T04.10 wires the run helpers (`_run_one_spec`, `_new_run_id`, `_compute_run_stats`, `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`)"

The tests explicitly **mock these names as module-level attributes of `commands.py`** (see `patch("superclaude.cli.eval.commands._run_one_spec", ...)` at test_no_mcp_skip.py:528). The tests treat the placeholders as the *contract surface* — i.e., they expect these names to live in commands.py, NOT in sibling modules.

**This is the most adversarial-resistant evidence against Thesis 3.** If the names were meant to consolidate to siblings, the tests would patch `superclaude.cli.eval.runner.EvalRunner.run` or `superclaude.cli.eval.artifact_layout.compose_run_id`, not `commands._run_one_spec` and `commands._new_run_id`. The tests *codify* the placeholder names as commands.py-local — which is *Thesis 1 territory*.

---

## Pre-empting A2 (signature mismatch)

A2 will note that **every** Thesis-3 mapping has signature delta. I concede: out of 11 symbols, **zero** have a clean drop-in sibling equivalent. The 3 MED-confidence rows (`_new_run_id`, `_default_output_dir`, `_run_one_spec`) require call-site reshuffling. The 4 LOW-confidence rows require new authoring with sibling primitives. The 4 NO-equivalent rows must be authored in commands.py.

A2 is right that strict "drop-in" consolidation does not work. **But the intent signal — six F401 sibling imports the author dragged in — survives**. The author wanted Thesis 3 even if they couldn't quite execute it.

## Pre-empting A3 (rename ghost / Thesis 2)

A3 will argue some placeholders look like rename ghosts: `_utc_iso_now` ≈ `datetime.now(timezone.utc).isoformat()`, `_can_install_signal_handler` ≈ `threading.current_thread() is threading.main_thread()`. For symbols #5 and #6, A3's case is genuinely strong — these *are* stdlib-idiom ghosts. For #1, #2, #4, however, the rename-ghost explanation fails: there is no plausible stdlib idiom that renames to `_new_run_id` returning a value with the exact `<HHMMSSZ>-<8-hex>` shape that `compose_run_id` produces. The closer fit is a deferred-consolidation intent.

## Pre-empting the RUN_*_EXIT_CODE objection

I concede this row fully. The three constants are **not** Thesis-3 material — they belong in `commands.py` per the naming convention of the eight existing `*_EXIT_CODE` constants and design-spec §4's integer values are dictated, not derived. Thesis 1 wins this sub-claim.

However, three out of eleven misses do not invalidate the broader directional read: the dominant pattern across the other eight symbols *is* "reach toward siblings, abandon at the call site".

---

## Resolution path (if Thesis 3 is adopted)

If the team accepts Thesis 3 as the dominant intent:

1. **Rewire #1, #2** to `artifact_layout.compose_run_id` / `compose_run_dir` (requires reordering the body so `started_iso` is computed at line 1466 before the run_id call).
2. **Author #4 (`_run_one_spec`)** in commands.py as glue wrapping `allocate_per_eval_paths` + `HomeIsolation` + `EvalRunner.run`.
3. **Inline #5, #6** as 2-liners using `datetime` (already imported) and `threading.main_thread()`.
4. **Author #3 (`_resolve_executor_factory`)** as a 3-line factory returning `lambda: ClaudeProcessAdapter(...)`.
5. **Author #7 (`_compute_run_stats`)** as a pure aggregator over `outcomes` returning `(RunCounts(...), RunTotals(...))`.
6. **Author #8 (`_format_run_summary_line`)** as a 1-line f-string.
7. **Add #9, #10, #11** as module-level constants `RUN_CLEAN_EXIT_CODE = 0`, `RUN_FAILURES_EXIT_CODE = 1`, `RUN_INTERRUPTED_EXIT_CODE = 3` per design-spec §4.

Total: ~60–80 LOC of new code, 4 call-site reshuffles, 3 constant declarations. The bulk of the *semantic work* (run-id, run-dir, lifecycle, signal handling, summary serialisation) already exists in siblings — which is why a partial-Thesis-3 read is still useful.

---

## Final confidence: 0.30

Thesis 3 captures the *author's intent* (six F401 sibling imports cannot be explained any other way), but **fails the strict test** that the runtime semantics already exist in a drop-in form. The reality is closer to: "Thesis 3 explains *why* the placeholders look the way they do; Thesis 1 explains *how* they should be fixed". I would not stake a remediation plan solely on Thesis 3. A blended Thesis 1 + Thesis 3 remediation (author the glue, but use sibling primitives throughout) is the honest path forward.
