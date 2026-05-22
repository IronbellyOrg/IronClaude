# D-0080 — TEST-009 artifact reproducibility tests

**Roadmap row:** R-080 (TEST-009)
**Phase task:** T04.20 (phase-4-tasklist.md §T04.20)
**Test module:** `tests/cli/eval/test_artifact_reproducibility.py`
**Producers under test:**
- `src/superclaude/cli/eval/artifact_layout.py` (FR-G4 / R-074 / D-0074 / T04.13)
  - `compose_run_dir`, `compose_run_id`, `compose_per_eval_dir`,
    `allocate_per_eval_paths`, `parse_run_dir_components`
  - Constants: `RUN_DIR_PREFIX` (`.dev/eval-runs`), `PER_EVAL_DIRNAME`
    (`per-eval`), `LOGS_JSONL_NAME` (`logs.jsonl`),
    `TTY_TRANSCRIPT_NAME` (`tty.transcript`), `ARTIFACTS_SUBDIR_NAME`
    (`artifacts`)
- `src/superclaude/cli/eval/models.py::EvalOutcome.artifacts` (DM-001)
- `src/superclaude/cli/eval/models.py::ExpectFailure.traceback` (DM-005)
- `src/superclaude/cli/eval/reporter.py::Reporter.write` (DM-012,
  COMP-008, FR-RPT1)

## 1. Goal

Pin the **reproducible artifact layout** every `superclaude eval run`
invocation must produce so that:

1. Two operators (or CI shards) replaying the same suite at the same
   wall-clock instant land on **byte-identical** trees — no drift in
   path shape, no drift in the per-eval emitter filenames, no drift in
   the summary.json cross-link strings.
2. An ERRORED eval **always** carries a Python traceback through both
   the JSONL event log (live, append-only) and the rendered
   `summary.json` (post-run, archived). A future refactor that loses
   the traceback at either layer fails loudly here.
3. The `summary.json` `evals[]` entries name per-eval artifact paths
   relative to the run directory — so a reviewer can `cat` a
   transcript from the summary without re-deriving the FR-G4 layout
   formula.

The full end-to-end `superclaude eval run` orchestrator loop is a
T04.10 forward dependency. This module deliberately anchors the
contract at the **layout + Reporter seam**: it builds the FR-G4 tree
via the `artifact_layout` helpers directly, materializes per-eval
files, then drives `Reporter.write()`. The T04.10 closure must satisfy
the same invariants when it lands; nothing in this test couples to a
specific run-loop wiring.

## 2. Reproducibility matrix

The eight pytest cases in `tests/cli/eval/test_artifact_reproducibility.py`
cover the five acceptance criteria from phase-4-tasklist.md §T04.20
plus three reinforcing guards. Cross-reference:

| # | Test function | AC covered | Pins |
|---|---|---|---|
| 1 | `test_run_dir_matches_fr_g4_pattern` | AC-1: run dir matches `.dev/eval-runs/<ISO>/<run-id>/` | Regex pin on `<output_root>/.dev/eval-runs/YYYY-MM-DD/HHMMSSZ-<8-hex>/`. `parse_run_dir_components` round-trips `(date, run_id)` from the path. |
| 2 | `test_run_dir_deterministic_for_inputs` | AC-1 + reproducibility invariant | Same `(suite_name, started_at)` → byte-identical run dir. Different `suite_name` OR different `started_at` → different run-id (sha256-deterministic per T04.13). |
| 3 | `test_per_eval_logs_jsonl_present_and_parsable` | AC-2: `logs.jsonl` exists per eval | The JSONL lives at the pinned filename inside `per-eval/<eval_id>/`, every line is JSON-parseable, the file is non-empty. |
| 4 | `test_per_eval_tty_transcript_present_and_non_empty` | AC-3: `tty.transcript` exists per eval | `tty.transcript` lands at the pinned filename inside `per-eval/<eval_id>/`, non-empty bytes. |
| 5 | `test_errored_outcome_records_stack_trace` | AC-4: traceback on ERRORED | A real `RuntimeError` is raised + captured; the resulting traceback appears VERBATIM in both (a) the JSONL `result.failure` event and (b) the rendered `summary.json` `evals[].expects[0].failure.traceback`. |
| 6 | `test_summary_json_cross_links_per_eval_artifacts` | AC-5: `evals[].artifacts` cross-link | Every `evals[]` row's `artifacts` mapping names `logs.jsonl`, `tty.transcript`, and the `artifacts/` directory; each cited POSIX path resolves to a real file/dir under the run directory. |
| 7 | `test_artifact_tree_reproducible_across_replays` | AC-1 + AC-5 reinforcing | Two independent replays of the same `(suite_name, started_at, eval set)` produce **byte-identical** `summary.json` outputs (modulo the run-dir prefix), proving the cross-link strings are stable across replays. |
| 8 | `test_parse_run_dir_rejects_non_layout_paths` | Negative guard | `parse_run_dir_components` raises on paths that do not match the FR-G4 layout — guards against silent acceptance of malformed paths. |

## 3. FR-G4 layout pinned by this module

```
<output_root>/
└── .dev/eval-runs/                           # RUN_DIR_PREFIX
    └── <YYYY-MM-DD>/                         # date component of started_at
        └── <HHMMSSZ>-<8-hex>/                # run_id = compose_run_id(suite_name, started_at)
            ├── summary.json                  # Reporter.write target (DM-012)
            └── per-eval/                     # PER_EVAL_DIRNAME
                └── <eval_id>/                # one subtree per EvalOutcome
                    ├── logs.jsonl            # LOGS_JSONL_NAME
                    ├── tty.transcript        # TTY_TRANSCRIPT_NAME
                    └── artifacts/            # ARTIFACTS_SUBDIR_NAME
```

The `<8-hex>` suffix of the run-id is `sha256(suite_name || ISO-Z-instant)[:8]` —
deterministic, so two replays collide on the same path. This is the
load-bearing reproducibility guarantee tests 1, 2, and 7 exercise.

## 4. Cross-link contract (AC-5 detail)

Per DM-001, each `EvalOutcome.artifacts` is a `Mapping[str, str]`
where:
- keys are the well-known names `"logs.jsonl"`, `"tty.transcript"`,
  `"artifacts"`;
- values are POSIX paths **relative to the run directory** (not
  absolute, not relative to CWD).

Test 6 verifies the cross-link by resolving every value against the
run directory and asserting the resulting path exists. The
"relative-to-run-dir" convention is what makes the artifact tree
**relocatable**: a CI job can tar the run dir and a reviewer can
extract it anywhere on disk, and every cross-link in `summary.json`
still resolves.

## 5. Stack-trace channel duality (AC-4 detail)

A real Python traceback is generated by raising and catching a
`RuntimeError` inside the test fixture (rather than hand-crafting a
multi-line string), so the test exercises the exact stringification
contract production code will hit: `traceback.format_exception(...)`
output, line breaks preserved, indentation preserved.

The test then asserts the **same traceback string** appears in two
places:

1. **JSONL channel** (`logs.jsonl`, the live event log) — the failure
   event carries `result.failure.traceback`. This is the
   append-only stream T03.05 / D-0049 emits during the run.
2. **Summary channel** (`summary.json` `evals[].expects[].failure`)
   — `ExpectFailure.traceback` (DM-005) carries the same string,
   serialized by `Reporter.to_json()` post-run.

Holding both pins in one test guards against a future refactor that
drops the field at either layer (e.g., truncating the traceback in the
summary while keeping it in the JSONL, or vice versa).

## 6. T04.10 forward dependency

The full `superclaude eval run` loop has not landed (it is T04.10);
this module therefore exercises the layout + Reporter contract via
direct calls to `compose_run_dir`, `allocate_per_eval_paths`, and
`Reporter.write()`, materializing per-eval files inside `tmp_path`.

No tests in this module are skipped — every guard runs today. When
T04.10 lands, the orchestrator must produce a tree that satisfies the
same invariants this module pins. The handoff is asymmetric: T04.10
will reuse the same `artifact_layout` helpers (FR-G4 / D-0074), so a
T04.10 closure that emits these helpers is automatically conformant.

## 7. Acceptance criteria mapping

From phase-4-tasklist.md §T04.20:

| AC | Verified by |
|---|---|
| File `tests/cli/eval/test_artifact_reproducibility.py` asserts run dir matches `.dev/eval-runs/<ISO>/<run-id>/`. | Test 1 (`test_run_dir_matches_fr_g4_pattern`) + test 2 (`test_run_dir_deterministic_for_inputs`). |
| Per-eval `logs.jsonl`, `tty.transcript` exist; stack trace recorded on ERRORED status. | Test 3 (`logs.jsonl`), test 4 (`tty.transcript`), test 5 (stack trace on ERRORED — JSONL + summary). |
| summary.json `evals[]` entries reference per-eval artifact paths. | Test 6 (`test_summary_json_cross_links_per_eval_artifacts`) — each `artifacts[*]` value resolves under the run dir; test 7 (`test_artifact_tree_reproducible_across_replays`) confirms cross-links are byte-stable. |
| `TASKLIST_ROOT/artifacts/D-0080/spec.md` records the reproducibility matrix. | This file. |
| Evidence saved under `TASKLIST_ROOT/evidence/T04.20/`. | `.dev/releases/current/cliEval/evidence/T04.20/test-output.txt` — pytest log, 8 passed, 0 skipped. |

## 8. Cross-links

* FR-G4 / R-074 / D-0074 / T04.13 (`artifact_layout.py`) — the layout
  source-of-truth this module exercises directly. T04.13's
  `test_artifact_layout.py` pins the helper contract in isolation; this
  module pins the **end-to-end** layout + cross-link + traceback
  contract on top of those helpers.
* DM-001 / T01.12 (`EvalOutcome.artifacts`) — the cross-link field
  test 6 reads.
* DM-005 / T01.16 (`ExpectFailure.traceback`) — the traceback channel
  test 5 reads.
* DM-012 / T03.10 (`summary.schema.json`) — the schema the Reporter
  renders to; `evals[].artifacts` and
  `evals[].expects[].failure.traceback` are both pinned by §6.x of the
  schema and read by tests 5 and 6.
* COMP-008 / T03.11 (`Reporter`) — the post-run renderer; this module
  drives `Reporter.write()` to materialize `summary.json` and assert on
  the rendered bytes.
* T04.17 / D-0078 (`test_reporter_contract.py`) — sibling test that
  pins the FR-RPT1 N'-vs-K dimensional invariant on the Reporter; this
  module trusts that guard and focuses on the artifact + cross-link
  contract.
* T04.10 / D-0072 (forward dep) — the `eval_run` orchestrator closure;
  when it lands, the run loop must produce a tree conformant to the
  invariants pinned here.
