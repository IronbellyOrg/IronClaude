# CP-P04-END — Phase 4 / M4 exit gate

**Task:** T04.22 (Phase 4, Roadmap R-064..R-081)
**Covers:** T04.01..T04.21
**Generated:** 2026-05-20
**status: FAIL**

## Summary

Phase 4 cannot exit M4 cleanly today. The functional surface targeted by
the milestone — all seven `Expect.*` primitives, the twelve FR-CLI1 flags
visible on `superclaude eval run --help`, the FR-G4 artifact layout, the
FR-G5 coverage gate, the TEST-007 reporter-contract suite, TEST-008
exit-code semantics, TEST-009 artifact reproducibility, and the OPS-003
retention policy — is **substantially landed in production code**, and
1267 of 1269 cli/eval tests PASS (7 skipped, 5 expected warnings). Two
of the three mid-phase Phase-4 checkpoints sit at `status: PASS`
(`CP-P04-T01-T05.md`, `CP-P04-T13-T17.md`); the middle one
(`CP-P04-T07-T11.md`) is `status: FAIL` and its remediation has **not**
landed since.

Three concrete blockers prevent flipping this gate to PASS:

1. **Exit-criteria pytest invocation exits non-zero.** The prescribed
   `uv run pytest tests/cli/eval/ -v` exits **1** with two failures
   (full log: `evidence/T04.22/exit-criteria-pytest.log`,
   `2 failed, 1267 passed, 7 skipped, 5 warnings in 17.74s`):
   - `tests/cli/eval/test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr`
     still raises `TypeError: CliRunner.__init__() got an unexpected
     keyword argument 'mix_stderr'`. This is the **identical** Click
     8.3.2 regression flagged in `CP-P04-T07-T11.md` § Remediation step
     1 (single-line edit at `test_eval_group.py:114`); no fix has
     landed on the tree.
   - `tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check`
     FAILS because `uv run ruff check src/superclaude/cli/eval/` now
     reports **23 errors** (eleven `F401` unused-imports + twelve
     `F821` undefined names). The clean-tree ruff floor that
     `CP-P03-END.md` § Exit Criteria pinned at `exit 0` has
     regressed; this is the FR-G1 ban-import contract test, so the
     regression also breaks an M3-resident invariant the M4 surface
     was supposed to inherit clean.
2. **`eval run` body references undefined symbols.** The `F821`
   cluster in `src/superclaude/cli/eval/commands.py:1418..1646` shows
   the `eval_run` callable references **eleven** symbols that do not
   exist on the module: `_new_run_id`, `_default_output_dir`,
   `_resolve_executor_factory`, `_run_one_spec`, `_utc_iso_now`
   (×2 sites), `_can_install_signal_handler`, `_compute_run_stats`,
   `_format_run_summary_line`, `RUN_INTERRUPTED_EXIT_CODE`,
   `RUN_FAILURES_EXIT_CODE`, `RUN_CLEAN_EXIT_CODE`. The decorator
   stack at `commands.py:1167` plus the docstring are present (so
   `superclaude eval run --help` still renders the twelve FR-CLI1
   flags fine — argument parsing happens before the body executes),
   but invoking `eval run` against any real fixture would raise
   `NameError` at runtime. This explains why `tests/cli/eval/test_eval_run.py`
   is still absent from the tree: there is no functional body to
   exercise. The `CP-P04-T13-T17.md` partial DOC-OQ3 end-to-end SKIP
   (`test_eval_run_no_pty_skips_real_suite_end_to_end`) is the
   downstream symptom of the same gap — the test names exactly these
   missing symbols (`_compute_run_stats` /
   `_finalise_outcome_summary` / `_RUN_CLEAN_EXIT_CODE` /
   `_RUN_FAILURES_EXIT_CODE`) as the precondition for un-skipping.
3. **Per-task evidence + artifact triplets remain missing.** Four
   deliverable directories never landed: `artifacts/D-0070/` (T04.08
   Expect.duration spec), `D-0071/` (T04.09 eval_group registration),
   `D-0072/` (T04.10 FR-CLI1 flag wiring), and `D-0077/` (T04.16
   `no_pty:skip` exclusion-set — the directory exists but is empty).
   Four evidence directories likewise missing or empty:
   `evidence/T04.08/`, `T04.09/`, `T04.10/`, and `T04.16/`. These were
   already enumerated as remediation deliverables in `CP-P04-T07-T11.md`
   and `CP-P04-T13-T17.md`; none have landed.

What **is** solid (and is recorded per-task below):

- **All seven Expect primitives reachable.** `Expect.file`,
  `Expect.jsonl`, `Expect.settings_json`, `Expect.exit_code`,
  `Expect.stderr`, `Expect.stdout`, `Expect.duration` resolve to real
  callables on the `Expect` namespace; `grep -n
  "NotImplementedError" src/superclaude/cli/eval/expect.py` is empty;
  `PRIMITIVE_NAMES` enumerates all seven. Per-primitive test modules
  (`test_expect_file.py`, `test_expect_jsonl.py`,
  `test_expect_settings_json.py`, `test_expect_exit_code.py`,
  `test_expect_stdio.py`, `test_expect_duration.py`) all PASS.
- **`superclaude eval run --help` lists all 12 FR-CLI1 flags.**
  `--suite`, `--parallel`, `--eval`, `--no-mcp`, `--no-pty`,
  `--output-dir`, `--keep-home`, `--timeout-mult`, `--max-disk-mb`,
  `--json`, `--verbose`, `--junit` plus the auto `--help`. Captured
  at `evidence/T04.22/eval-run-help.txt`.
- **DOC-OQ7 and DOC-OQ3 entries present in decisions.md.** DOC-OQ7
  full closure block at `decisions.md:482` (option A — wire `--junit`,
  flipped `OPEN → RESOLVED — 2026-05-20` at `decisions.md:525`);
  DOC-OQ3 §B Open-Question table-row at `decisions.md:442`
  (`DEFERRED to M4 — exclusion set captured in
  suites/real.yaml no_pty:skip per eval per DOC-OQ3 (roadmap row
  254)`).
- **`coverage_gate` green for the one-matcher fixture suite + fails
  with `coverage_missing:<pattern>` when matcher uncovered.** Pinned
  by `tests/cli/eval/test_coverage_gate.py` (26 PASS) including
  `test_coverage_gate_fails_when_fourth_matcher_added_without_eval`
  and `test_cli_doctor_check_coverage_fails_when_uncovered_matcher_present`.

The honest read is that M4 is **functionally ~95% done** — the
seven-primitive surface, the FR-CLI1 flag enumeration, the FR-G4 layout,
the FR-G5 coverage gate, the TEST-007 reporter contract, and the
OPS-003 retention policy are all reachable through tests. What is
missing is small and non-architectural:

- One Click 8.2+ idiom replacement (one line in
  `tests/cli/eval/test_eval_group.py:114`).
- Either (a) author the eleven missing helper symbols
  (`_new_run_id`, `_default_output_dir`, `_resolve_executor_factory`,
  `_run_one_spec`, `_utc_iso_now`, `_can_install_signal_handler`,
  `_compute_run_stats`, `_format_run_summary_line`,
  `RUN_INTERRUPTED_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`,
  `RUN_CLEAN_EXIT_CODE`) inside `commands.py` so the `eval_run` body
  resolves at runtime, **or** (b) consolidate the body to use the
  already-landed helpers (`HARD_FAIL_EXIT_CODE`,
  `REPORTER_CONTRACT_VIOLATION_EXIT_CODE`, the existing
  `compose_run_id` / `compose_run_dir` from `artifact_layout.py`, the
  `Reporter` byte-stable emitters from T03.13, etc.). The eleven
  symbols are referenced in numerical order from `commands.py:1418`
  onward, so the patch surface is localised to lines 1418–1646.
- `tests/cli/eval/test_eval_run.py` covering the 12-flag surface +
  the clamp / AC12 / one-eval end-to-end paths the docstring
  enumerates. Cannot be authored until step 2 lands the body.
- The standard `spec.md` / `notes.md` / `evidence.md` triplet
  templated by `D-0064..D-0069` and `D-0073..D-0076`, populated for
  D-0070, D-0071, D-0072, and D-0077.
- Per-task evidence captures (a `pytest.log` or equivalent) for
  T04.08, T04.09, T04.10, T04.16.

These remediation steps are tracked in §"Recommended remediation
order" below.

## Per-upstream-task status

| Task   | Roadmap | Deliverable | Status | Notes |
|--------|---------|-------------|--------|-------|
| T04.01 | R-064   | D-0064      | PASS   | FR-EXP1 package landed; `src/superclaude/cli/eval/expect.py` exposes the `Expect` namespace with all seven primitives (no `NotImplementedError("M4")` stubs remaining); `PRIMITIVE_NAMES = ('file','jsonl','settings_json','exit_code','stderr','stdout','duration')`. `artifacts/D-0064/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T01-T05.md`. |
| T04.02 | R-065   | D-0065      | PASS   | `Expect.file(path, exists, contains, regex, equals)` reachable + `tests/cli/eval/test_expect_file.py` PASSES; `artifacts/D-0065/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T01-T05.md`. |
| T04.03 | R-066   | D-0066      | PASS   | `Expect.jsonl(path, line_count, filter, assert_each, assert_any)` reachable + `tests/cli/eval/test_expect_jsonl.py` PASSES; `artifacts/D-0066/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T01-T05.md`. |
| T04.04 | R-067   | D-0067      | PASS   | `Expect.settings_json(path, key_path, equals, exists)` reachable + `tests/cli/eval/test_expect_settings_json.py` PASSES; path resolves against `HomeIsolation.home_path`; `artifacts/D-0067/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T01-T05.md`. |
| T04.05 | R-068   | D-0068      | PASS   | `Expect.exit_code(equals, in_set, not_equals)` reachable + mutually-exclusive arg validation + default `equals=0`; `tests/cli/eval/test_expect_exit_code.py` PASSES; `artifacts/D-0068/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T01-T05.md`. |
| T04.06 | -       | D-CP04-MID-T01-T05 | PASS | `CP-P04-T01-T05.md` exists at `status: PASS`; first Phase-4 mid-phase gate met. |
| T04.07 | R-069   | D-0069      | PASS   | `Expect.stderr(contains, regex, not_contains)` + `Expect.stdout(...)` reachable; both operate on ANSI-stripped buffers via `_strip_ansi`; `tests/cli/eval/test_expect_stdio.py` (22 PASS) covers CSI/OSC strip, `not_contains`-after-strip, all-three-predicates-together, declarative `from_mapping`, empty-buffer no-args. `artifacts/D-0069/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T07-T11.md`. |
| T04.08 | R-070   | D-0070      | PARTIAL | `Expect.duration(max_sec, min_sec)` body real + listed in `PRIMITIVE_NAMES`; `tests/cli/eval/test_expect_duration.py` (19 PASS) covers no-bounds informational mode, max-only, min-only, both-bounds, boundary, declarative `from_mapping`. **Doc gap (unchanged from `CP-P04-T07-T11.md`):** `evidence/T04.08/` and `artifacts/D-0070/{spec,notes,evidence}.md` not on disk. |
| T04.09 | R-071   | D-0071      | FAIL    | `eval_group` Click group exports `doctor`/`list`/`describe`/`run`; `uv run superclaude eval --help` lists all four. Six of seven `test_eval_group.py` cases PASS. **Carry-forward blocker:** `test_run_skeleton_emits_deferral_notice_on_stderr` (line 114) still uses `CliRunner(mix_stderr=False)`, which Click 8.3.2 dropped → `TypeError`. Single-line fix (drop the kwarg; read `result.stderr` directly) un-blocks. **Doc gap:** `evidence/T04.09/` + `artifacts/D-0071/{spec,notes,evidence}.md` not on disk. |
| T04.10 | R-072   | D-0072      | FAIL    | `eval_run` Click subcommand decorator stack (`commands.py:1167`) declares all 12 FR-CLI1 flags; `uv run superclaude eval run --help` renders them (`evidence/T04.22/eval-run-help.txt`). **Functional gap:** the body at `commands.py:1418..1646` references **eleven** undefined symbols (`_new_run_id`, `_default_output_dir`, `_resolve_executor_factory`, `_run_one_spec`, `_utc_iso_now` ×2, `_can_install_signal_handler`, `_compute_run_stats`, `_format_run_summary_line`, `RUN_INTERRUPTED_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`, `RUN_CLEAN_EXIT_CODE`); ruff reports the cluster as `F821` (`evidence/T04.22/ruff-check.log`). Invoking the command against any real fixture would raise `NameError` at runtime. `tests/cli/eval/test_eval_run.py` consequently still does not exist. **Doc gap:** `evidence/T04.10/` + `artifacts/D-0072/{spec,notes,evidence}.md` not on disk. |
| T04.11 | R-073   | D-0073      | PARTIAL | `tests/cli/eval/test_single_command.py::test_single_command_contract_is_documented` PASSES; the live FR-G6 smoke (`test_single_command_local_runnability`) is SKIPPED with rationale `phase-4-tasklist.md §T04.11 Notes` (pre-E1 phases use a stub eval; live smoke runs in M5 once E1 / T05.02 lands). Acceptance criterion 2 ("Test asserts presence of `summary.md` and `summary.json` under the per-run directory") is not active until the runnability test un-skips at M5. `artifacts/D-0073/{spec,notes,evidence}.md` populated. Status carried unchanged from `CP-P04-T07-T11.md`. |
| T04.12 | -       | D-CP04-MID-T07-T11 | FAIL | `CP-P04-T07-T11.md` exists at `status: FAIL`. Three blockers cited: missing `tests/cli/eval/test_eval_run.py`, Click 8.3.2 `mix_stderr` regression, missing D-0070/D-0071/D-0072 + evidence/T04.08/T04.09/T04.10. **None of the three remediation items has landed since.** |
| T04.13 | R-074   | D-0074      | PASS   | FR-G4 reproducible artifact layout in `src/superclaude/cli/eval/artifact_layout.py` exposes `compose_run_id`, `compose_run_dir`, `compose_per_eval_dir`, `allocate_per_eval_paths`, `parse_run_dir_components`; `tests/cli/eval/test_artifact_layout.py` (19 PASS) pins the `.dev/eval-runs/<ISO>/<run-id>/` shape + per-eval `logs.jsonl`/`tty.transcript`/`artifacts/` subtree + ISO Z/offset/naive parsing + traversal rejection + round-trip. `artifacts/D-0074/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T13-T17.md`. |
| T04.14 | R-075   | D-0075      | PASS   | FR-G5 `coverage_gate(settings_path, suite)` in `src/superclaude/cli/eval/coverage.py`; `tests/cli/eval/test_coverage_gate.py` (26 PASS) including sanitisation, default-filter, matcher-walk, prefix-regex, design-spec exit-code pin, fourth-matcher uncovered scenario, and `eval doctor --check-coverage` CLI wiring. v1 trio (`mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*`) verified covered; uncovered matcher emits `coverage_missing:<pattern>` artifact with exit 2. `artifacts/D-0075/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T13-T17.md`. |
| T04.15 | R-076   | D-0076      | PASS   | DOC-OQ7 closure recorded — full block "DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)" at `decisions.md:482` + table-row flip `OPEN → RESOLVED — 2026-05-20` at `decisions.md:525`. Wiring pinned at `commands.py:1349-1352` (flag declaration), `commands.py:1366` (callable parameter), `commands.py:1593` (Reporter call — note this line currently FAILS to resolve `_compute_run_stats`, see T04.10 above), `reporter.py:146` (`emit_junit` default), `reporter.py:222-225` (`junit.xml` write gated on flag). `artifacts/D-0076/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T13-T17.md`. |
| T04.16 | R-077   | D-0077      | PARTIAL | DOC-OQ3 functional contract landed: `suites/real.yaml` annotates every PTY-required eval with `no_pty: skip`; `tests/cli/eval/test_no_pty_exclusion.py` 13/14 PASS (the one SKIP is `test_eval_run_no_pty_skips_real_suite_end_to_end`, deferred with explicit rationale pointing at the T04.10 `_compute_run_stats` / `_finalise_outcome_summary` / `_RUN_CLEAN_EXIT_CODE` / `_RUN_FAILURES_EXIT_CODE` gap — i.e. the exact same eleven missing symbols flagged in T04.10 above; un-skip is gated on the T04.10 remediation below). OQ-3 entry in decisions.md (§B Open-Question table, line 442). **Doc gap (unchanged from `CP-P04-T13-T17.md`):** `artifacts/D-0077/` directory exists but the `spec.md` / `notes.md` / `evidence.md` triplet is not on disk; `evidence/T04.16/` is not on disk. |
| T04.17 | R-078   | D-0078      | PASS   | TEST-007 reporter contract — `tests/cli/eval/test_reporter_contract.py` (4 PASS): `test_n_prime_equals_k_lets_every_emitter_render`, `test_skipped_rows_included_in_evals_with_skip_reason`, `test_n_prime_vs_k_mismatch_raises_and_maps_to_exit_code_two` (asserts `ReporterContractViolation` + exit 2 per design-spec §4), `test_reporter_json_validates_against_summary_schema` (validates `summary.json` against the DM-012 schema). `artifacts/D-0078/{spec,notes,evidence}.md` populated. Closed under `CP-P04-T13-T17.md`. |
| T04.18 | -       | D-CP04-MID-T13-T17 | PASS | `CP-P04-T13-T17.md` exists at `status: PASS`. Third Phase-4 mid-phase gate met (with the T04.16 doc-triplet + the T04.10 end-to-end SKIP rolled forward to this M4 exit). |
| T04.19 | R-079   | D-0079      | PASS   | TEST-008 exit-code semantics — `tests/cli/eval/test_exit_codes.py` covers the four exit paths (0 clean, 1 failing, 2 harness-error, 3 interrupted); all pin via `subprocess.run` against `superclaude eval run`. The 2-path is exercised via the `ReporterContractViolation` route (T04.17) and the disk-budget-exceeded artifact (T03.19); the 3-path goes through `SignalHandlerInstaller` + `CancellationToken` (T03.07). `artifacts/D-0079/{spec,notes,evidence}.md` populated; `evidence/T04.19/` on disk. **Caveat:** these tests pass because they exercise the cancellation / contract-violation surfaces directly; the `eval_run` body's own exit-code emission (T04.10) cannot be exercised end-to-end until the eleven missing symbols above land. |
| T04.20 | R-080   | D-0080      | PASS   | TEST-009 artifact reproducibility — `tests/cli/eval/test_artifact_reproducibility.py` pins `.dev/eval-runs/<ISO>/<run-id>/` pattern + per-eval `logs.jsonl` / `tty.transcript` presence + stack-trace recorded on ERRORED + `summary.json::evals[]` cross-link to per-eval artifact paths. `artifacts/D-0080/{spec,notes,evidence}.md` populated; `evidence/T04.20/` on disk. Same caveat as T04.19 — the assertions stand against the FR-G4 layout (T04.13) which IS reachable today; the `eval_run` body's own writes (T04.10) are not exercised end-to-end. |
| T04.21 | R-081   | D-0081      | PASS   | OPS-003 retention policy — `docs/eval/retention.md` documents `--keep-home` default false, failed-setup preserved (NFR-ISO2), summaries retained, and disk-budget-advice text. `tests/cli/eval/test_retention_policy.py` asserts the disk-budget breach error message contains the retention-advice string verbatim (per the T03.19 disk-budget poller) and that `--keep-home True` preserves per-eval HOMEs after run. `artifacts/D-0081/{spec,notes,evidence}.md` populated; `evidence/T04.21/` on disk. |

**Roll-up:** 14 upstream tasks PASS (T04.01–T04.07, T04.13–T04.15,
T04.17, T04.19–T04.21); 3 PARTIAL (T04.08, T04.11, T04.16); 2 FAIL
(T04.09, T04.10); 2 of 3 mid-phase checkpoints PASS (T04.06, T04.18);
1 of 3 mid-phase checkpoints FAIL (T04.12 — `CP-P04-T07-T11.md`,
unchanged).

## Verification (3/3 confirmed)

1. **All 7 Expect primitives reachable with tests passing** —
   CONFIRMED.
   - `src/superclaude/cli/eval/expect.py::PRIMITIVE_NAMES` enumerates
     `('file', 'jsonl', 'settings_json', 'exit_code', 'stderr',
     'stdout', 'duration')`; `grep -n "NotImplementedError"
     src/superclaude/cli/eval/expect.py` is empty.
   - Per-primitive tests:
     `tests/cli/eval/test_expect_file.py`,
     `test_expect_jsonl.py`, `test_expect_settings_json.py`,
     `test_expect_exit_code.py`, `test_expect_stdio.py` (covers both
     `stderr` and `stdout`), `test_expect_duration.py` — all PASS in
     the live `evidence/T04.22/exit-criteria-pytest.log`.

2. **`superclaude eval run --help` lists all 12 FR-CLI1 flags** —
   CONFIRMED.
   - `uv run superclaude eval run --help`
     (`evidence/T04.22/eval-run-help.txt`) renders `--suite`,
     `--parallel`, `--eval`, `--no-mcp`, `--no-pty`, `--output-dir`,
     `--keep-home`, `--timeout-mult`, `--max-disk-mb`, `--json`,
     `--verbose`, `--junit` plus the auto `--help`. All twelve
     FR-CLI1 flags are present with help text, defaults, and the
     design-spec §4 exit-code policy summary in the docstring.
   - **Caveat (downgraded but not omitted):** the body that the help
     text describes does not currently resolve at runtime — see T04.10
     status above. The help-rendering invariant is met because Click
     parses the decorator stack before the body executes; the
     functional invocation invariant is not.

3. **`coverage_gate` green for the one-matcher fixture suite; fails
   with `coverage_missing:<pattern>` when matcher uncovered** —
   CONFIRMED.
   - `tests/cli/eval/test_coverage_gate.py::test_coverage_gate_fails_when_fourth_matcher_added_without_eval`
     PASSES — the v1-trio-plus-one scenario named verbatim in T04.14
     Validation.
   - `::test_cli_doctor_check_coverage_fails_when_uncovered_matcher_present`
     PASSES — pins the `eval doctor --check-coverage` CLI surface.
   - All 26 tests in the module PASS in the live
     `evidence/T04.22/exit-criteria-pytest.log`.

## Exit Criteria (1/3 met)

- **NOT MET** — `uv run pytest tests/cli/eval/ -v` exits **1** with
  `2 failed, 1267 passed, 7 skipped, 5 warnings in 17.74s`
  (`evidence/T04.22/exit-criteria-pytest.log`). The two failures are:
  - `tests/cli/eval/test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr`
    — `TypeError: CliRunner.__init__() got an unexpected keyword
    argument 'mix_stderr'` (Click 8.3.2 removed the kwarg). The fix
    is a single-line edit (drop the kwarg; read `result.stderr`
    directly).
  - `tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check`
    — `AssertionError: Clean tree should pass ruff check but returned
    1.` because `uv run ruff check src/superclaude/cli/eval/` finds
    23 errors (11 `F401` unused imports + 12 `F821` undefined names,
    all in `commands.py`). Full ruff capture:
    `evidence/T04.22/ruff-check.log`. This is an M3-resident invariant
    (`CP-P03-END.md` § Exit Criteria #2) that has regressed during M4.
- **MET** — DOC-OQ7 and DOC-OQ3 decisions recorded in decisions.md.
  - DOC-OQ7: closure block at `decisions.md:482` + table-row
    `OPEN → RESOLVED — 2026-05-20` at `decisions.md:525`.
  - DOC-OQ3: §B Open-Question table-row at `decisions.md:442` —
    `DEFERRED to M4 — exclusion set captured in
    suites/real.yaml no_pty:skip per eval per DOC-OQ3 (roadmap row
    254)`. Binding artefact is the manifest itself
    (`suites/real.yaml`), pinned by
    `test_real_suite_marks_every_eval_no_pty_skip`.
- **MET** — Checkpoint report `CP-P04-END.md` (this file) records
  pass/fail per task in Phase 4 — the *Per-upstream-task status*
  table above lists explicit PASS / PARTIAL / FAIL for every task
  T04.01–T04.21 with blockers cited.

## Acceptance Criteria

- File `TASKLIST_ROOT/checkpoints/CP-P04-END.md` exists — **MET**.
  Contains `status: FAIL`, so the "contains `status: PASS`"
  sub-clause is **NOT MET**; this is the honest assessment given the
  failing exit-criteria pytest invocation, the eleven undefined
  symbols in `commands.py`, and the unresolved doc-triplet gaps
  carried from `CP-P04-T07-T11.md`.
- All 3 Verification bullets are confirmed — **MET** (3/3, with the
  T04.10 functional caveat noted on bullet 2).
- All 3 Exit Criteria bullets are met — **NOT MET** (1/3 met; the
  pytest invocation bullet fails on (a) the Click 8.3.2 regression
  and (b) the regressed M3 ruff floor).
- Checkpoint report includes the task IDs it covers (T04.01–T04.21) —
  **MET** (header + per-task status table).

## Artifacts and evidence

Present:

- Mid-phase checkpoints:
  - `CP-P04-T01-T05.md` (PASS — T04.01..T04.05).
  - `CP-P04-T07-T11.md` (FAIL — T04.07..T04.11, three blockers cited).
  - `CP-P04-T13-T17.md` (PASS — T04.13..T04.17, with T04.16 doc-gap
    + T04.10 end-to-end SKIP rolled forward).
- Per-task artifacts under `artifacts/D-0064..D-0081/` for 14 of 18
  M4 deliverables — D-0064 through D-0069, D-0073 through D-0076,
  D-0078 through D-0081 populated with `spec.md`, `notes.md`,
  `evidence.md`. D-0070, D-0071, D-0072 not on disk; D-0077 directory
  exists but its triplet is not authored.
- Per-task evidence under `evidence/T04.01..T04.21/` for 14 of 21 M4
  tasks — T04.01 through T04.07, T04.11 through T04.15, T04.17,
  T04.19 through T04.21 populated. T04.08, T04.09, T04.10, T04.16,
  T04.18 missing or empty. (Note: T04.18 is a checkpoint task, so
  its missing `evidence/T04.18/` is by-design — checkpoints are
  read-only verifications per Rollback notes.)
- M4-suite pytest log captured live during this checkpoint:
  `evidence/T04.22/exit-criteria-pytest.log` →
  `2 failed, 1267 passed, 7 skipped, 5 warnings in 17.74s`, exit 1.
- M4-suite ruff log captured live during this checkpoint:
  `evidence/T04.22/ruff-check.log` → 23 errors, exit 1.
- `eval run --help` capture: `evidence/T04.22/eval-run-help.txt`.

Missing (remediation deliverables required for M4 PASS):

- `tests/cli/eval/test_eval_run.py` — cannot be authored until the
  `eval_run` body resolves. Should cover at minimum: (i) `--help`
  lists all 12 flags; (ii) `--parallel 0` clamps to 1 and
  `--parallel 16` clamps to 15; (iii) `--output-dir` resolves through
  the AC12 allowlist; (iv) end-to-end one-eval invocation against a
  fixture manifest exits 0 with `summary.{md,json}` written.
- `artifacts/D-0070/{spec,notes,evidence}.md` (Expect.duration spec),
  `D-0071/{spec,notes,evidence}.md` (eval_group registration spec),
  `D-0072/{spec,notes,evidence}.md` (FR-CLI1 flag wiring spec),
  `D-0077/{spec,notes,evidence}.md` (`no_pty:skip` exclusion-set
  spec).
- `evidence/T04.08/`, `T04.09/`, `T04.10/`, `T04.16/` — each needs
  a `pytest.log` (or equivalent command-output capture) for the
  matching test module.

## Cross-references

- Phase tasklist:
  `.dev/releases/current/cliEval/phase-4-tasklist.md` — T04.22 § lines
  1040–1089; covered tasks T04.01–T04.21 at lines 5–1038.
- Sibling checkpoints:
  - `CP-P04-T01-T05.md` (T04.06, PASS — T04.01..T04.05).
  - `CP-P04-T07-T11.md` (T04.12, FAIL — T04.07..T04.11; three
    blockers: missing `test_eval_run.py`, Click 8.3.2
    `mix_stderr` regression, missing D-0070/D-0071/D-0072 + evidence
    triplets). **Not remediated.**
  - `CP-P04-T13-T17.md` (T04.18, PASS — T04.13..T04.17, with T04.16
    doc-gap + T04.10 end-to-end SKIP rolled forward to this M4 exit).
- Prior milestone exits:
  - `CP-P03-END.md` (PASS — Phase 3 / M3). Note the ruff-clean floor
    pinned in `CP-P03-END.md` § Exit Criteria #2 has **regressed**
    during M4 (23 errors in `commands.py`); restoring the floor is
    part of the M4 remediation below.
  - `CP-P02-END.md` (FAIL — Phase 2 / M2; T02.01 ptytest vendoring
    deferred). Independent of this gate.
  - `CP-P01-END.md` (FAIL — Phase 1 / M1; T01.14 ExpectDSL interface
    remediation deferred). Independent of this gate.
- Relevant design-spec sections:
  - design-spec §9 (FR-CLI1 flag enumeration) — twelve flags
    declared on the decorator stack (T04.10); `--junit` resolved per
    DOC-OQ7 closure (T04.15); `--no-pty` honours
    `suites/real.yaml no_pty:skip` per DOC-OQ3 (T04.16).
  - design-spec §4 (exit-code policy) — pinned by TEST-008
    (T04.19) and `test_n_prime_vs_k_mismatch_raises_and_maps_to_exit_code_two`
    (T04.17) and `test_coverage_gate_exit_code_pins_design_spec_value`
    (T04.14). The `eval_run` body's own exit emission references
    `RUN_INTERRUPTED_EXIT_CODE` / `RUN_FAILURES_EXIT_CODE` /
    `RUN_CLEAN_EXIT_CODE` which are currently undefined.
  - design-spec §10.x / DM-012 — reporter contract + JSON schema
    validated by `test_reporter_json_validates_against_summary_schema`
    (T04.17).
- Decisions record:
  - `.dev/releases/current/cliEval/decisions.md` § "DOC-OQ7 Closure —
    `--junit` flag wiring decision (T04.15)" (line 482) and §B
    Open-Question table (lines 435–447) for DOC-OQ3 / DOC-OQ7.
- MDTM task tracks:
  - `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/`
  - `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P2-loader-models-expect/`
- Downstream gate: Phase 5 entry (M5) is **blocked** by this FAIL.
  M5 owns the eval corpus (E1 / T05.02 sticky lifecycle, etc.) and
  cannot proceed until the `eval_run` body resolves at runtime and
  `tests/cli/eval/test_eval_run.py` lands.

## Recommended remediation order

1. **Restore the ruff-clean floor on `src/superclaude/cli/eval/`** —
   address the 23 errors in `commands.py`:
   a. Remove 11 unused imports (`os`, `secrets`, `datetime`,
      `timezone`, `Sequence`, `HomeContainmentViolation`,
      `HomeIsolation`, `RunCounts`, `RunTotals`, `EvalRunner`,
      `LifecycleExecutor`). `ruff check --fix` clears these
      mechanically.
   b. Define (or import) the 11 undefined symbols referenced by the
      `eval_run` body: `_new_run_id`, `_default_output_dir`,
      `_resolve_executor_factory`, `_run_one_spec`, `_utc_iso_now`,
      `_can_install_signal_handler`, `_compute_run_stats`,
      `_format_run_summary_line`, `RUN_INTERRUPTED_EXIT_CODE`,
      `RUN_FAILURES_EXIT_CODE`, `RUN_CLEAN_EXIT_CODE`. Either author
      them in `commands.py`, or refactor the body to use the
      already-landed equivalents (`compose_run_id` /
      `compose_run_dir` from `artifact_layout.py`,
      `HARD_FAIL_EXIT_CODE` and
      `REPORTER_CONTRACT_VIOLATION_EXIT_CODE` from existing modules,
      the `Reporter` byte-stable emitters from T03.13, etc.). The
      `CP-P04-T13-T17.md` SKIP rationale for
      `test_eval_run_no_pty_skips_real_suite_end_to_end` lists the
      exact symbols expected, which gives the patch a strict
      target.
   c. Re-run `uv run ruff check src/superclaude/cli/eval/` → expect
      `All checks passed!`, exit 0. This also un-FAILs
      `test_clean_tree_passes_ruff_check` (which is currently the
      first of the two pytest failures).
2. **Replace `CliRunner(mix_stderr=False)` at
   `tests/cli/eval/test_eval_group.py:114`** — drop the kwarg, read
   `result.stderr` directly per Click 8.2+. This un-FAILs the second
   pytest failure (the carry-forward blocker from
   `CP-P04-T07-T11.md`).
3. **Author `tests/cli/eval/test_eval_run.py`** — covers the 12-flag
   surface, the `--parallel` clamp paths, the `--output-dir` AC12
   allowlist, the `--no-pty` exclusion behaviour
   (un-skipping `test_eval_run_no_pty_skips_real_suite_end_to_end`),
   and a stub-fixture end-to-end exit-code 0 invocation. Cannot land
   before step 1 because the body has to resolve first.
4. **Populate `artifacts/D-0070/`, `D-0071/`, `D-0072/`, `D-0077/`
   triplets** — use `D-0064/`, `D-0069/`, `D-0076/` as templates.
   `D-0077` should document the `suites/real.yaml no_pty:skip`
   annotation pattern, the eleven per-branch invariants pinned by
   `test_no_pty_exclusion.py`, and the end-to-end pin un-skipped by
   step 3.
5. **Capture `evidence/T04.08/`, `T04.09/`, `T04.10/`, `T04.16/`** —
   re-run the matching test modules and save outputs.
6. **(Optional) Author a dedicated "DOC-OQ3 Closure" section in
   decisions.md** mirroring the DOC-OQ7 closure block, to remove the
   table-row vs full-section asymmetry. Current table-row entry at
   `decisions.md:442` satisfies the exit-criteria "present in
   decisions.md" requirement, but the asymmetry is a documentation
   smell.
7. **Re-run the prescribed exit-criteria invocation** — expect
   `uv run pytest tests/cli/eval/ -v` exits 0 with
   `~1270 + N passed, 7 skipped` (where N = the number of
   `test_eval_run.py` cases authored in step 3), and `uv run ruff
   check src/superclaude/cli/eval/` exits 0.
8. **Flip this checkpoint to `status: PASS`** once steps 1–5 land
   and step 7 is verified.

Until those steps land, this gate stays at `status: FAIL` so M5 entry
can correctly aggregate the outstanding work. The remediation is
small in surface area (≈20 lines of new code in `commands.py` plus
one line in `test_eval_group.py`) but high in leverage — every M4
acceptance criterion downstream of `eval_run` runtime resolution
flips green once step 1b lands.
