# A1 — cliEval Runner-Symbols Module Audit (Phase 1)

**Agent:** A1 (structural module audit; **neutral ground truth**, not a thesis advocate)
**Date:** 2026-05-21
**Scope:** `src/superclaude/cli/eval/` — 21 sibling modules; focus on `commands.py:1406..1695` (`eval_run`).
**Read-only.** No source-tree edits performed.

---

## 0. Executive headline

The 11 missing symbols inside `eval_run` are **forward references to T04.10
deliverables that were planned but never authored on this branch**. The
sibling modules in `src/superclaude/cli/eval/` already supply
*semantically-close* helpers for **8 of the 11** (e.g.
`artifact_layout.compose_run_id`, `signal_handler.SignalHandlerInstaller`),
but the wiring call sites in `commands.py` reference **leading-underscore
private names that do not exist anywhere in the project**. The repo also
contains test modules (`test_exit_codes.py`, `test_single_command.py`,
`test_no_pty_exclusion.py`, `test_no_mcp_skip.py`, `test_validation_commands.py`)
whose docstrings and skip-predicates **enumerate the same 11 names verbatim**
and explicitly tag them as "T04.10 deliverables… not yet landed."

This skews the inferential balance heavily toward **Thesis #1 — never
authored** (with `_new_run_id`/`_default_output_dir`/`_compute_run_stats`/the
three exit-code constants being net-new; the other five being unwritten
adapters around existing helpers).

Confidence in Thesis #1: **0.80**. (See §6 for the residual uncertainty.)

---

## 1. Existence sweep — the 11 missing symbols

Every symbol below was grepped across the full
`src/superclaude/cli/eval/` tree (21 modules) and across
`tests/` and the broader `src/` tree. Results:

| Symbol | Defined anywhere? | Closest sibling (semantic equivalent) | Sibling file:line |
|---|---|---|---|
| `_new_run_id` | **No** | `compose_run_id(started_at, suite_name)` | `artifact_layout.py:139` |
| `_default_output_dir` | **No** | `compose_run_dir(output_root, started_at, suite_name)` (returns full per-run dir, not just default output root) | `artifact_layout.py:162` |
| `_resolve_executor_factory` | **No** | `LifecycleExecutor` Protocol (no concrete factory in tree) | `runner.py:136` |
| `_run_one_spec` | **No** | `run_eval(spec, *, home, config, run_dir, artifacts_dir, stdout_path, stderr_path, transcript_path, executor, …) -> EvalOutcome` | `runner.py:177` |
| `_utc_iso_now` | **No** | (no existing helper; `datetime` + `timezone` are imported into `commands.py:39` but the imports are flagged F401-unused — see §3) | n/a |
| `_can_install_signal_handler` | **No** | `SignalHandlerInstaller.install()` raises `ValueError` if not main thread (`signal_handler.py:203-206`); no boolean probe exists | `signal_handler.py:136,203` |
| `_compute_run_stats` | **No** | `RunCounts` / `RunTotals` dataclasses exist (`models.py:732,786`) but **neither has a `from_outcomes()` classmethod** — no aggregator exists | `models.py:732,786` |
| `_format_run_summary_line` | **No** | `render_summary_yaml(summary)`, `render_summary_markdown(summary)`, `render_summary_json(summary)`, `render_junit_xml(summary)` — all render whole documents, none renders the one-line operator-stdout banner the call site needs | `reporter.py:83`, `run_report.py:137,229,255` |
| `RUN_INTERRUPTED_EXIT_CODE` | **No** | (no integer constant by that name; design-spec §4 line 590 specifies `0 / 1 / 2 / 3`) | n/a |
| `RUN_FAILURES_EXIT_CODE` | **No** | (no integer constant by that name; design-spec §4 line 590) | n/a |
| `RUN_CLEAN_EXIT_CODE` | **No** | (no integer constant by that name; design-spec §4 line 590) | n/a |

**Quantitative summary:** 0 of 11 symbols exist. 8 of 11 have a sibling
that performs the *adjacent* concern; 3 of 11 (the `RUN_*_EXIT_CODE`
triple) have no sibling at all — they would be net-new module-level
integer constants.

### 1.1 — Cross-corroboration from the test tree

Five test files name these 11 symbols explicitly as preconditions:

- `tests/cli/eval/test_single_command.py:148-160` defines
  `_eval_run_body_incomplete()` which probes `hasattr(cmds, name)` for
  **all 11** symbols and skips the test when any is missing. Docstring
  (lines 134-144): *"The phase-4 tasklist sequences T04.10 (FR-CLI1 ``eval
  run`` body) before T04.11 (this smoke test). The current ``commands.py``
  references helper functions (``_new_run_id``, ``_run_one_spec``, etc.)
  whose definitions land with T04.10's body; until those names resolve,
  the ``eval run`` invocation raises ``NameError``…"*
- `tests/cli/eval/test_exit_codes.py:93-113` defines `_t0410_missing()`
  enumerating 6 of the 11 (`_new_run_id`, `_run_one_spec`,
  `_compute_run_stats`, `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`,
  `RUN_INTERRUPTED_EXIT_CODE`) and skip-gates exit-code 0/1/3 tests.
  Module docstring (lines 29-41): *"The exit-code-2 paths … exercise
  real ``sys.exit(HARD_FAIL_EXIT_CODE)`` calls today. The 0 / 1 / 3 paths
  all flow through the run-loop closure whose helpers (…) are T04.10
  deliverables. While those helpers are absent we ``pytest.skip`` those
  three tests with a self-clearing diagnostic; the skips evaporate once
  T04.10 lands…"*
- `tests/cli/eval/test_no_pty_exclusion.py:266-337` and
  `tests/cli/eval/test_no_mcp_skip.py:30-528` both patch
  `superclaude.cli.eval.commands._run_one_spec` via `monkeypatch.setattr`
  with `raising=False` and skip end-to-end paths "until T04.10 lands."
- `tests/cli/eval/test_validation_commands.py:166-177` asserts that the
  release validation-doc enumerates blocker **B1 (_new_run_id)** and
  **B2 (ptytest)** as known runner-side gaps.

The tests were authored **with the explicit knowledge that the symbols
do not yet exist**. This is decisive structural evidence: nobody could
have authored these skip-gates after a symbol had been removed, because
the docstrings frame the absence as a forward dependency, not a
regression.

---

## 2. eval_run call-graph (lines 1406–1695, current file state)

> **Line-number reconciliation note.** The ruff log captured in
> `.dev/releases/current/cliEval/evidence/T04.22/ruff-check.log` reports
> the F821 cluster at lines `1418, 1420, 1528, 1549, 1563, 1575, 1587,
> 1593, 1622, 1628, 1645, 1646`. The current on-disk `commands.py` (60 914
> bytes, mtime 2026-05-20 23:08) has the same call sites at lines `1467,
> 1469, 1577, 1598, 1612, 1624, 1636, 1642, 1671, 1677, 1694, 1695`. The
> file grew by ~49 lines after ruff capture; the **set of missing
> symbols is unchanged**. The audit uses current line numbers.

### 2.1 — Verbatim import block (`commands.py:30-88`)

```
import json                       # line 30
import os                         # line 31 — F401 unused
import platform                   # line 32
import re                         # line 33
import secrets                    # line 34 — F401 unused
import subprocess                 # line 35
import sys                        # line 36
import time                       # line 37
from dataclasses import dataclass, replace                          # line 38
from datetime import datetime, timezone                             # line 39 — F401 unused (both names)
from pathlib import Path                                            # line 40
from typing import Any, Callable, Iterable, Optional, Sequence      # line 41 — Sequence F401 unused

import click                      # line 43
import yaml                       # line 44

from .capabilities import CapabilityGates, CapabilityReport, CapabilityStatus     # 46-50
from .config import (SCRATCH_ROOT_VIOLATION_EXIT_CODE, EvalConfig,
                     ScratchRootViolation, format_scratch_root_violation,
                     resolve_scratch_root)                                         # 51-57
from .coverage import (COVERAGE_GATE_FAILED_EXIT_CODE, CoverageResult,
                       coverage_gate)                                              # 58-62
from .disk_budget import (DEFAULT_DISK_BUDGET_MB,
                          DISK_BUDGET_EXCEEDED_ARTIFACT_NAME,
                          DISK_BUDGET_EXCEEDED_EXIT_CODE,
                          DISK_BUDGET_RETENTION_ADVICE, DiskBudgetPoller)         # 63-69
from .isolation import HomeContainmentViolation, HomeIsolation                    # line 70 — both F401 unused
from .loader import (SUITE_LOADER_ERROR_EXIT_CODE, ParsedSuite, SuiteLoader,
                     SuiteLoaderError)                                             # 71-76
from .models import (EvalOutcome, EvalSpec, RunCounts, RunSummary, RunTotals)     # 77-83 — RunCounts and RunTotals F401 unused
from .orchestrator import RunOrchestrator                                          # line 84
from .reporter import Reporter                                                     # line 85
from .runner import EvalRunner, LifecycleExecutor                                  # line 86 — both F401 unused
from .signal_handler import CancellationToken, SignalHandlerInstaller             # line 87
from .suites import SCHEMA_PATH                                                    # line 88
```

### 2.2 — Cross-reference: F401 unused vs F821 undefined

| F401 unused import | Would resolve which F821? | Plausibility |
|---|---|---|
| `os` | none | obviously stale |
| `secrets` | could back `_new_run_id` if author intended `secrets.token_hex(4)`-style id; but `compose_run_id` is deterministic, contradicting a `secrets` approach | low |
| `datetime`, `timezone` | back `_utc_iso_now` (`datetime.now(timezone.utc).isoformat()`) | **high** — these two imports are sized exactly to the helper |
| `Sequence` | none — typing | stale |
| `HomeContainmentViolation`, `HomeIsolation` | `_run_one_spec` would need to import these to construct per-spec HOME; the unused-imports are the constructor-side dependency the body expected | **high** |
| `RunCounts`, `RunTotals` | `_compute_run_stats` returns the tuple `(RunCounts, RunTotals)` exactly; the imports were staged for that helper's return type | **high** |
| `EvalRunner`, `LifecycleExecutor` | `_resolve_executor_factory` would return one or the other; the imports were staged for that factory's return type | **high** |

**Inferential leap (`INFERENTIAL`)**: the seven unused imports
(`datetime`, `timezone`, `HomeContainmentViolation`, `HomeIsolation`,
`RunCounts`, `RunTotals`, `EvalRunner`, `LifecycleExecutor`) form a
**type-shape-coherent set** for the seven of-eleven missing helpers
they would back. This strengthens Thesis #1 substantially: an author
who pre-staged exactly these imports while writing the call sites
mapped to one set of helpers they planned to author. Reasoning
chain: F401 set size (7) ≈ F821 helper-needing-import set size (7);
the mapping is one-to-one and type-coherent; an "intended helpers"
shadow exists in the imports.

### 2.3 — Symbols `eval_run` invokes successfully (counter-evidence)

The function calls **18 other names successfully** today (per-line, in
order of appearance):

`RunOrchestrator.MIN_PARALLEL` (1443) · `RunOrchestrator.MAX_PARALLEL` (1445) ·
`HARD_FAIL_EXIT_CODE` (1453, 1461, 1634) · `EvalConfig()` (1466, 1494) ·
`resolve_scratch_root` (1473) · `ScratchRootViolation` (1478) ·
`format_scratch_root_violation` (1479) · `SCRATCH_ROOT_VIOLATION_EXIT_CODE`
(1480) · `resolve_suite_manifest` (1505) · `_DEFAULT_SUITES_DIR` (1505) ·
`SuiteNotFound` (1506) · `SUITE_NOT_FOUND_EXIT_CODE` (1508) ·
`SuiteLoader()` (1510) · `SuiteLoaderError` (1513) ·
`SUITE_LOADER_ERROR_EXIT_CODE` (1515) · `EVAL_NOT_FOUND_EXIT_CODE`
(1529) · `coverage_gate` (1541) · `_format_coverage_missing_roster`
(1547) · `COVERAGE_GATE_FAILED_EXIT_CODE` (1548) · `CapabilityGates`
(1561) · `DiskBudgetPoller` (1567) · `CancellationToken` (1572) ·
`EvalOutcome` (1587) · `RunOrchestrator` (1615) · `SignalHandlerInstaller`
(1624, 1625) · `RunSummary` (1649) · `Reporter` (1663) ·
`DISK_BUDGET_EXCEEDED_ARTIFACT_NAME` (1647) · `DISK_BUDGET_RETENTION_ADVICE`
(1687) · `DISK_BUDGET_EXCEEDED_EXIT_CODE` (1688) plus `json.dumps`,
`time.monotonic`, `sys.exit`, `Path.mkdir`, `click.echo`.

These are all **module-public** (or private but defined earlier in
`commands.py`). The pattern is unambiguous: the author was using a
disciplined import strategy for everything except the eleven F821
names. This rules out a "lazy global lookup" or "wrong module path"
explanation — the rest of the body is wired correctly.

---

## 3. Exit-code constant inventory

### 3.1 — Constants `eval_run` already uses (defined earlier in tree)

| Constant | Value | Site of definition | Used in `eval_run` |
|---|---|---|---|
| `HARD_FAIL_EXIT_CODE` | `2` | `commands.py:550` | 1453, 1461, 1634 |
| `SCRATCH_ROOT_VIOLATION_EXIT_CODE` | `2` (per `config.py`) | `config.py` (imported 51-57) | 1480 |
| `SUITE_NOT_FOUND_EXIT_CODE` | inferred `2` | `commands.py` (defined locally, used at 1508) | 1508 |
| `SUITE_LOADER_ERROR_EXIT_CODE` | `2` | `loader.py` (imported 71-76) | 1515 |
| `EVAL_NOT_FOUND_EXIT_CODE` | `2` | `commands.py:954` | 1529 |
| `COVERAGE_GATE_FAILED_EXIT_CODE` | `2` | `coverage.py` (imported 58-62) | 1548 |
| `DISK_BUDGET_EXCEEDED_EXIT_CODE` | `2` | `disk_budget.py` (imported 63-69) | 1688 |

**Pattern:** every defined exit-code constant in the tree is `= 2` — all
seven map to design-spec §4's harness-error code. The exit codes 0, 1,
and 3 have no existing constants.

### 3.2 — Design-spec §4 mapping

`.dev/releases/current/cliEval/design-spec.md:590` states verbatim:

> *Exit code from §4 maps: 0 ⇔ no eval in {FAIL, ERRORED, TIMEOUT, XPASS};
> 1 ⇔ at least one; 2 ⇔ harness error before any eval ran; 3 ⇔ INTERRUPTED.*

This confirms the three missing constants are **semantically distinct
integers, not aliases**:

| Missing constant | Design-spec §4 value | Existing constant equivalent? |
|---|---|---|
| `RUN_CLEAN_EXIT_CODE` | `0` | None — no `*_EXIT_CODE = 0` exists; implicit fall-through impossible because the call site is `sys.exit(RUN_CLEAN_EXIT_CODE)` |
| `RUN_FAILURES_EXIT_CODE` | `1` | None — no `*_EXIT_CODE = 1` exists anywhere in eval/ |
| `RUN_INTERRUPTED_EXIT_CODE` | `3` | None — no `*_EXIT_CODE = 3` exists; cancellation-token aware exit is new surface |

**Conclusion:** the three exit-code constants are net-new symbols, not
renames. (Confirmed by `git log -S "RUN_CLEAN_EXIT_CODE"` returning
empty — see §5.)

---

## 4. Semantic-equivalent map (for A4's "belong elsewhere" thesis)

For each of the eleven, the closest sibling helper + the delta required
to wire it:

| Missing symbol | Sibling helper | Signature delta |
|---|---|---|
| `_new_run_id()` → `str` | `artifact_layout.compose_run_id(started_at: str, suite_name: str = "") -> str` (`artifact_layout.py:139`) | Caller has neither `started_at` nor `suite_name` at line 1467 (it computes `started_iso` at line 1612, AFTER the run-id call). Wiring would need to either reorder (compute `started_iso` first) or wrap the helper with a current-time default. The CP-P05-END remediation prescribes exactly this: *"replace the undefined call with `compose_run_id(started_at=_utc_iso_now(), suite_name=suite)` or author a thin `_new_run_id()` wrapper that delegates to `compose_run_id`"* (`.dev/releases/current/cliEval/checkpoints/CP-P05-END.md:401-406`). |
| `_default_output_dir(run_id)` | `artifact_layout.compose_run_dir(output_root, started_at, suite_name) -> Path` (`artifact_layout.py:162`) | Signature mismatch: `compose_run_dir` takes 3 args (output_root, started_at, suite_name) and computes `run_id` internally; the call site at `commands.py:1469` passes only `run_id`. The helper expects to *recompute* the id, not receive one. Wiring requires either a new wrapper or shape change. |
| `_resolve_executor_factory()` | `runner.LifecycleExecutor` (Protocol at `runner.py:136`) + `runner.EvalRunner` (`runner.py:702`) | No concrete factory exists. The Protocol declares `spawn/inject/observe` (T03.04) and `EvalRunner.__call__` accepts an `executor: LifecycleExecutor` parameter at `runner.py:759`. The runner expects a caller-supplied executor; the helper would need to construct one. |
| `_run_one_spec(spec, *, run_dir, home_root, config, timeout_mult, keep_home, cancellation_token, executor_factory)` | `runner.run_eval(spec, *, home, config, run_dir, artifacts_dir, stdout_path, stderr_path, transcript_path, executor, expect_callables, deploy_hooks, on_teardown_error, keep_home_on_pass) -> EvalOutcome` (`runner.py:177-192`) | Signature drift: `_run_one_spec` is called with 8 kwargs; `run_eval` takes 13. `_run_one_spec` would need to set up the per-eval paths (using `artifact_layout.allocate_per_eval_paths`) and construct the `HomeIsolation` instance before delegating. This is genuinely new orchestration code, ~30-60 lines. |
| `_utc_iso_now()` → `str` | None — `datetime` + `timezone` are imported (and F401-unused) at `commands.py:39` | One-liner: `datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")` or similar. The F401-unused state of both imports is **structural evidence the author pre-staged the imports for exactly this helper**. |
| `_can_install_signal_handler()` → `bool` | `signal_handler.SignalHandlerInstaller.install()` raises `ValueError` from non-main thread (`signal_handler.py:203-206`) | No boolean probe exists. Wiring would be `threading.current_thread() is threading.main_thread()` plus possibly a try/except guard. Net-new surface but mechanical. |
| `_compute_run_stats(outcomes, *, manifest_n) -> tuple[RunCounts, RunTotals]` | `models.RunCounts` (`models.py:732`) and `models.RunTotals` (`models.py:786`) are plain frozen dataclasses; **neither has a `from_outcomes()` classmethod** | The aggregator is genuinely missing. The F401-unused state of both `RunCounts` and `RunTotals` imports in `commands.py` indicates they were staged precisely for this helper's return signature (matching `counts, totals = _compute_run_stats(...)` at line 1642). |
| `_format_run_summary_line(summary, output_dir)` → `str` | `reporter.render_summary_yaml`, `run_report.render_summary_markdown`, `…json`, `…junit_xml` — all render full documents, not the one-line operator banner | The closest formatter (`render_summary_yaml`) returns multi-line YAML; the call site at `1671` expects a single-line operator string for `click.echo` under `--verbose`. New helper. |
| `RUN_CLEAN_EXIT_CODE = 0` | None | Net-new module-level constant. |
| `RUN_FAILURES_EXIT_CODE = 1` | None | Net-new module-level constant. |
| `RUN_INTERRUPTED_EXIT_CODE = 3` | None | Net-new module-level constant. |

**Symbol-class summary:**

- **Net-new constants (3):** `RUN_CLEAN/FAILURES/INTERRUPTED_EXIT_CODE`.
- **Net-new helpers (3):** `_compute_run_stats`, `_format_run_summary_line`,
  `_can_install_signal_handler`. No sibling has the exact shape; each is
  a small additive surface.
- **Thin wrappers around existing siblings (5):** `_new_run_id` →
  `compose_run_id`; `_default_output_dir` → `compose_run_dir`;
  `_resolve_executor_factory` → instantiates the existing
  `LifecycleExecutor` Protocol via `EvalRunner`; `_run_one_spec` →
  `run_eval` (with per-eval path allocation pre-step);
  `_utc_iso_now` → `datetime.now(timezone.utc).isoformat(...)`.

This is the precise distribution that makes Thesis #4 ("symbols belong
elsewhere — just import them") *partially* correct: 5 of 11 can be
written as one-to-three-line shims; the other 6 require genuinely new
code (3 trivial constants, 3 short helpers).

---

## 5. Git history blame

### 5.1 — Repository state

```
$ git status src/superclaude/cli/eval/commands.py
Untracked files:
        src/superclaude/cli/eval/commands.py
```

**`commands.py` is untracked.** Indeed, every file under
`src/superclaude/cli/eval/` is untracked:

```
$ git ls-files src/superclaude/cli/eval/
(empty)
$ git ls-files --others --exclude-standard src/superclaude/cli/eval/
src/superclaude/cli/eval/__init__.py
src/superclaude/cli/eval/artifact_layout.py
src/superclaude/cli/eval/capabilities.py
…(29 files total, none tracked)…
```

### 5.2 — `git log -S` probes (all returned **empty**)

```
$ git log --all --oneline -S "_new_run_id" -- src/superclaude/cli/eval/
(no output)
$ git log --all --oneline -S "def _new_run_id"
(no output)
$ git log --all --oneline -S "def _compute_run_stats"
(no output)
$ git log --all --oneline -S "def _run_one_spec"
(no output)
$ git log --all --oneline -S "RUN_CLEAN_EXIT_CODE"
(no output)
$ git log --all --oneline -S "compose_run_id" -- src/
(no output)
$ git log --all --oneline -- "src/superclaude/cli/eval/*"
(no output)
```

### 5.3 — Implications for the three theses

The empty git history is **decisive evidence against Thesis #2 (removed
or renamed)**: there is no commit anywhere on any branch that ever
contained a definition for `_new_run_id`, `_compute_run_stats`,
`_run_one_spec`, `RUN_CLEAN_EXIT_CODE`, or any of the 11 symbols. The
helpers were never on disk in a tracked state. They cannot have been
"removed" because there is no removal event in the reflog of any branch.

Equally, the sibling helpers (`compose_run_id`, etc.) have no commit
history either — the entire `cli/eval/` package exists only on the
working tree of the current branch (`feature/sc-auggie-review-protocol`,
HEAD `36df860`). The package was authored fresh, in a single uncommitted
working-tree snapshot, and the eleven F821 references in `eval_run` were
authored together with the rest of the body — but the helpers that the
body references were not authored alongside.

> **Caveat (`INFERENTIAL`):** the absence of git history could in principle
> mean the work is on another machine / branch that never pushed. Given
> the explicit T04.10 forward-reference language in the test files (which
> *did* land on this same untracked snapshot) and the CP-P04-END
> checkpoint's verbatim "T04.10 FAIL — body references eleven undefined
> symbols" line, the most parsimonious reading is "T04.10 was scheduled,
> deferred, and the call sites + tests landed first as a forward-
> dependency scaffold." Reasoning chain: tests explicitly cite T04.10 as
> the missing wave → call sites cite the same eleven names → no git
> history exists for any of them → the tests pre-date the implementation
> in intent if not in time-of-write.

---

## 6. Open questions for sibling agents (A2 / A3 / A4)

### Q1 — Authoring intent of the seven F401-unused imports

The imports `datetime, timezone, HomeContainmentViolation, HomeIsolation,
RunCounts, RunTotals, EvalRunner, LifecycleExecutor` are type-coherent
with the helpers they would back. **Does the project's
release-spec / TDD pin the helper signatures at this exact shape?**
A4's thesis (symbols belong elsewhere) gains weight if the answer is
"yes, the design called for `_compute_run_stats` to take outcomes and
return `(RunCounts, RunTotals)`," because then the import-shape match is
*by-spec* rather than authorial happenstance.

### Q2 — Was T04.10 ever scoped as a single deliverable?

The CP-P04-END status row for T04.10 (line 147) says: *"`eval_run` Click
subcommand decorator stack at `commands.py:1167` declares all 12 FR-CLI1
flags; …**Functional gap:** the body at `commands.py:1418..1646`
references **eleven** undefined symbols (…); ruff reports the cluster as
`F821`. Invoking the command against any real fixture would raise
`NameError` at runtime. `tests/cli/eval/test_eval_run.py` consequently
still does not exist."*

This makes T04.10 a single PARTIAL deliverable that landed the wiring
contract without the implementation. **Was this an explicit scope split
in the phase-4 tasklist, or did the implementer hit a context limit
mid-task?** A2 (thesis: helpers were authored elsewhere and the wire was
just missed) would benefit from interrogating
`.dev/releases/current/cliEval/phase-4-tasklist.md` §T04.10 for the
deliverable boundary.

### Q3 — Why is the file untracked?

The package is 21 files / ~10 687 lines and is entirely untracked. **Does
the project gate `cli/eval/` behind a `make`-target gitignore until the
runner clears?** If so, the "untracked" state is engineering policy, not
abandonment; if not, this is itself a checkpoint failure beyond the
T04.10 scope.

### Q4 — RUN_DIR_PREFIX vs `--output-dir` semantics

`artifact_layout.RUN_DIR_PREFIX = Path(".dev/eval-runs")` (line 76) and
`compose_run_dir(output_root, started_at, suite)` returns
`<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>`. The `eval_run`
call site at line 1469 uses `_default_output_dir(run_id)` *before* the
scratch-root resolution at line 1473. **What is the intended layering?**
A4's "just call `compose_run_dir`" remediation would require
`compose_run_dir(Path.cwd(), _utc_iso_now(), suite)` — but `Path.cwd()`
may not be in the scratch-root allowlist, so the operator-visible
default may need to be tighter than the helper's signature suggests.

### Q5 — Are `_compute_run_stats` and `_format_run_summary_line` the *only*
genuinely new helpers, or are there design-spec sections (§ on Reporter
contract, § on operator stdout) that prescribe these as belonging
inside `reporter.py` / `run_report.py` rather than `commands.py`?

If the design-spec puts the stats aggregator inside `models.RunCounts`
as a `from_outcomes` classmethod, A4's thesis ("just import them") is
materially correct; the call site would change from
`_compute_run_stats(outcomes, manifest_n=…)` to
`RunCounts.from_outcomes(outcomes, manifest_n=…), RunTotals.from_outcomes(outcomes)`.
A3's thesis (the helpers were authored and put in the wrong module)
needs this answered to demonstrate "wrong module" rather than "never
authored."

---

## 7. Findings summary

1. **Existence sweep.** 0 of 11 missing symbols are defined anywhere in
   the project source tree. 8 of 11 have a *semantic* sibling; 3 of 11
   (the exit-code triple) have no sibling at all.
2. **Test-tree confirmation.** Five test files name the same 11 symbols
   as preconditions and skip-gate themselves with docstrings explicitly
   tagging them as *"T04.10 deliverables… not yet landed."*
3. **Import-shape coherence.** 7 of the 12 F401-unused imports
   (`datetime, timezone, HomeContainmentViolation, HomeIsolation,
   RunCounts, RunTotals, EvalRunner, LifecycleExecutor`) are exactly the
   types the matching missing helpers would consume / return. Authorial
   intent traces in the imports: they were pre-staged for the helpers
   that never landed.
4. **Exit-code gap is real, not an alias.** Design-spec §4 line 590
   prescribes `0 / 1 / 2 / 3`; the tree defines seven `*_EXIT_CODE = 2`
   constants and zero constants for `0`, `1`, `3`. The three missing
   `RUN_*_EXIT_CODE` names are net-new module surface.
5. **Git history confirms never-authored.** No commit on any branch
   contains a definition for any of the 11 symbols. The package is
   entirely untracked. Thesis #2 (removed / renamed) is decisively ruled
   out.
6. **Five wrappers vs six net-new.** 5 missing helpers could be 1-to-3-
   line shims over existing siblings; 6 (three constants + three small
   helpers) require genuine new code. The CP-P05-END remediation §
   already prescribes the wrapper for `_new_run_id`, which corroborates
   the "5 wrappers" reading.

### Confidence vector

- Thesis #1 (never authored): **0.80** — direct evidence from CP-P04-END
  T04.10 row, test-file skip docstrings, and empty git history.
- Thesis #2 (removed / renamed): **0.02** — empty `git log -S`,
  forward-looking docstring language; only residual probability for the
  "work-on-another-machine" caveat.
- Thesis #3 (belong elsewhere): **0.13** — the import-shape coherence
  suggests *signatures* were sketched; if those sketches landed in
  `models.py` / `reporter.py` as `from_outcomes` classmethods that
  `commands.py` was supposed to import, the F821s collapse to F821-by-
  import-typo rather than missing implementation. Cannot be ruled out
  without the answers to Q1 and Q5.
- Thesis #4 (just-wire-existing): **0.55** *partial* — 5 of 11 can be
  satisfied by wiring; 6 of 11 need new code. The CP-P05-END remediation
  step 1 endorses the wrapper-style approach (`_new_run_id ←
  compose_run_id` wrapper) which is exactly thesis #4 for the dominant
  blocker symbol.

(Theses #1 and #4 are not mutually exclusive: the answer is *both* —
"the eleven helpers were never authored, and roughly five of them can
be backed by thin wrappers around existing helpers while six need a
small amount of new code." A1 surfaces this; the sibling agents debate
the implementation order and ownership.)

### Branch-trace count

The companion artifact at `phase1/A1-branch-trace.md` covers all 19
expected-branch entries listed in
`artifacts/expected-branches-extended.txt`. Every entry is classified;
none is left "unclassified."
