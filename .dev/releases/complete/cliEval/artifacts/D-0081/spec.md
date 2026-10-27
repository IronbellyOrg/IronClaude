# D-0081 — OPS-003 artifact retention policy

**Roadmap row:** R-081 (OPS-003)
**Phase task:** T04.21 (phase-4-tasklist.md §T04.21)
**Policy doc:** `docs/eval/retention.md`
**Test module:** `tests/cli/eval/test_retention_policy.py`
**Producers under test:**
- `src/superclaude/cli/eval/disk_budget.py` (NFR-PERF4 / R-060 /
  D-0060 / T03.19) — new constant `DISK_BUDGET_RETENTION_ADVICE`
  (the single source of truth for the OPS-003 retention-advice
  string emitted on a disk-budget breach).
- `src/superclaude/cli/eval/commands.py::eval_run` (FR-CLI1 / R-070 /
  D-0070 / T04.10) — wires the retention advice to stderr immediately
  before `sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)`.
- `src/superclaude/cli/eval/runner.py::_finalize` (FR-LC1 / D-0048) —
  the keep/remove decision for per-eval HOMEs the policy documents.
- `src/superclaude/cli/eval/isolation.py::HomeIsolation` (NFR-ISO2 /
  T02.13) — the setup_failed tag preservation the policy documents.

## 1. Goal

Pin the **operator-visible retention contract** for every artifact
`superclaude eval run` produces, on every termination path, so that:

1. Operators reading a disk-budget breach in CI know **what was
   preserved** (run directory + summaries + per-eval artifacts for
   finished evals + `disk_budget_exceeded.json` side-car) and **which
   knobs** to turn on the next invocation (`--max-disk-mb` /
   `--keep-home`).
2. The policy doc (`docs/eval/retention.md`), the library constant
   (`DISK_BUDGET_RETENTION_ADVICE`), and the CLI stderr surface stay
   aligned by construction — any future edit to one without updating
   the others is a test failure rather than a silent operator surprise.
3. The `--keep-home False` default and the NFR-ISO2 setup-failed
   preservation are documented in a single place operators can
   pivot to from any termination branch.

The full end-to-end `superclaude eval run` orchestrator loop is a
T04.10 forward dependency. The doc + constant + CLI-stderr surface
pins this module lands run today; the `--keep-home True`
end-to-end HOME-preservation test is skipped behind the
`_skip_unless_t0410_landed()` probe pattern shared with
`test_exit_codes.py` so it un-skips automatically once T04.10 wires
the run-loop closure.

## 2. Retention contract pinned

The policy doc covers four pillars; the test module pins each as
follows:

| Pillar | Test | Pin |
|---|---|---|
| P1 — `--keep-home` default False, PASS removes / others keep | `test_retention_doc_covers_four_pillars` | Doc mentions `--keep-home`, the word "default", and every non-PASS status (`PASS`, `FAIL`, `ERRORED`, `TIMEOUT`) in the retention matrix. |
| P2 — NFR-ISO2 setup_failed tag preserves the HOME | `test_retention_doc_covers_four_pillars` | Doc cites the constant value `".eval-meta/setup_failed"` verbatim and the NFR-ISO2 identifier so operators can pivot to the atomic-setup contract. |
| P3 — Run summaries always retained | `test_retention_doc_covers_four_pillars` | Doc names `summary.md`, `summary.json`, and `junit.xml` as preserved on every exit branch. |
| P4 — Disk-budget breach side-car + advice | `test_retention_doc_covers_four_pillars` + `test_retention_doc_quotes_advice_constant_verbatim` + `test_cli_emits_retention_advice_on_disk_budget_breach` | Doc names `disk_budget_exceeded.json`, the `--max-disk-mb` knob, and the OPS-003 identifier; doc text contains `DISK_BUDGET_RETENTION_ADVICE` byte-for-byte; CLI subprocess writes the same bytes to stderr on a synthetic breach. |

## 3. Five tests in `test_retention_policy.py`

| # | Test function | AC covered | Pins |
|---|---|---|---|
| 1 | `test_retention_doc_exists` | AC-4: doc exists at `docs/eval/retention.md` | `DOC_PATH` is a non-empty regular file. |
| 2 | `test_retention_doc_covers_four_pillars` | AC-1 / AC-2: doc documents `--keep-home` default, failed-setup preservation, summary retention, disk-budget breach advice | Doc text contains the load-bearing literals for each pillar (see §2 table). |
| 3 | `test_retention_doc_quotes_advice_constant_verbatim` | AC-2: doc + CLI surface byte-aligned | `DISK_BUDGET_RETENTION_ADVICE` is a verbatim substring of the doc; any edit to the constant without updating the doc fails this test. |
| 4 | `test_retention_advice_constant_shape` | AC-2 reinforcing | Constant contains the breach name (`"disk-budget exceeded"`), the preserved artifact signals (`summary`, `disk_budget_exceeded.json`), both retention knobs (`--max-disk-mb`, `--keep-home`), and the back-link to `docs/eval/retention.md`. |
| 5 | `test_cli_emits_retention_advice_on_disk_budget_breach` | AC-2: assertions wired into the dispatcher | Real `superclaude eval run` subprocess invocation with a 1 MB budget against a pre-seeded 2 MB run directory exits with `DISK_BUDGET_EXCEEDED_EXIT_CODE` and echoes the verbatim constant to stderr. Skipped today behind `_t0410_missing()` because the breach exit-branch lives at the end of the run-loop closure. |
| 6 | `test_keep_home_true_preserves_per_eval_homes_on_pass` | AC-3: `--keep-home True` HOMEs preserved | Real `superclaude eval run --keep-home --no-pty` subprocess exits 0; the scratch root remains inspectable and any HOME that materialised survives. Skipped today behind `_skip_unless_t0410_landed()`. |

Tests 1–4 land run today (they exercise the doc + library constant
seam). Tests 5 and 6 traverse the run-loop closure and are guarded by
the T04.10 forward-dependency probe.

## 4. Single-source-of-truth invariant

The OPS-003 retention advice is pinned exactly once in the
codebase:

```
src/superclaude/cli/eval/disk_budget.py::DISK_BUDGET_RETENTION_ADVICE
```

Three surfaces consume it:

1. `docs/eval/retention.md` quotes the constant verbatim inside a
   fenced code block (§4 of the policy doc).
2. `src/superclaude/cli/eval/commands.py::eval_run` echoes the
   constant via `click.echo(DISK_BUDGET_RETENTION_ADVICE, err=True)`
   immediately before the breach-branch `sys.exit`.
3. `tests/cli/eval/test_retention_policy.py` reads the constant once,
   asserts both other surfaces carry the same bytes, and asserts the
   constant itself contains the load-bearing signals (§3 row 4).

The result: any drift across surfaces is a test failure rather than
a silent operator surprise. The doc cannot fall behind a CLI edit;
the CLI cannot fall behind a doc edit; the test cannot fall behind
either.

## 5. Acceptance criteria mapping

From phase-4-tasklist.md §T04.21:

| AC | Verified by |
|---|---|
| File `docs/eval/retention.md` documents `--keep-home` default false, failed setups preserved, summaries retained, disk-budget advice text. | `test_retention_doc_exists` + `test_retention_doc_covers_four_pillars`. |
| Disk-budget breach error message contains the retention-advice string verbatim. | `test_retention_doc_quotes_advice_constant_verbatim` + `test_retention_advice_constant_shape` + `test_cli_emits_retention_advice_on_disk_budget_breach`. |
| `--keep-home True` test confirms per-eval HOMEs are preserved after run. | `test_keep_home_true_preserves_per_eval_homes_on_pass` (gated by T04.10 forward dep). |
| `TASKLIST_ROOT/artifacts/D-0081/spec.md` records the policy. | This file. |
| Evidence saved under `TASKLIST_ROOT/evidence/T04.21/`. | `.dev/releases/current/cliEval/evidence/T04.21/test-output.txt` — pytest log. |

## 6. T04.10 forward dependency

The end-to-end retention tests (test 5 — CLI stderr emission on breach;
test 6 — `--keep-home True` HOME preservation) traverse the
`superclaude eval run` run-loop closure. The closure references
helpers defined in T04.10 (`_new_run_id`, `_run_one_spec`,
`_compute_run_stats`, `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`,
`RUN_INTERRUPTED_EXIT_CODE`). While any of those are missing, the two
dependent tests skip with a self-clearing diagnostic that auto-clears
once T04.10 lands. The doc + constant + advice-shape pins (tests 1–4)
all run today.

The forward-dep probe pattern is shared with
`tests/cli/eval/test_exit_codes.py` (T04.19 / D-0079): the same
`_t0410_missing()` / `_skip_unless_t0410_landed()` helpers are
reproduced here so the skip diagnostic remains consistent across the
two modules.

## 7. Cross-links

* NFR-PERF4 / R-060 / D-0060 / T03.19 (`disk_budget.py`) — the
  poller this policy back-links to; `DISK_BUDGET_RETENTION_ADVICE`
  ships in this module alongside the existing breach constants.
* NFR-ISO2 / T02.13 (`isolation.py`) — the setup-failed tag
  contract the policy doc P2 documents. The tag relpath
  (`.eval-meta/setup_failed`) is read from `HomeIsolation.SETUP_FAILED_TAG_RELPATH`.
* FR-LC1 / D-0048 (`runner.py::_finalize`) — the keep/remove
  decision the policy doc §2 table documents.
* FR-CLI1 / R-070 / D-0070 / T04.10 (`commands.py::eval_run`) — the
  dispatcher that emits the advice. The breach-branch wiring is
  pinned here; the surrounding closure is T04.10's deliverable.
* FR-RPT1 / DM-012 / T03.11 (`reporter.py::Reporter`) — the
  Reporter that writes `summary.{md,json}` / `junit.xml` on every
  exit branch. Retention of those files is documented by the policy
  but pinned independently by `test_reporter_contract.py` (D-0078).
* T04.19 / D-0079 (`test_exit_codes.py`) — the sibling module that
  pins the four design-spec §4 exit codes at the process boundary;
  the T04.10 forward-dep probe pattern this module re-uses lives there.
* design-spec §4 (CLI surface), §10 R4 row (the disk-budget risk
  this policy mitigates), §13 NFR-PERF4 / NFR-ISO2 — the upstream
  contracts every clause of the policy doc back-links to.
