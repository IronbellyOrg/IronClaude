# CP-P04-END — Phase 4 / M4 exit gate

**Task:** T04.22 (Phase 4, Roadmap R-064..R-081)
**Covers:** T04.01..T04.21
**Generated:** 2026-05-21
**status: PASS**

## Summary

Phase 4 exits M4 cleanly: all 21 upstream tasks land PASS, all three
mid-phase checkpoints (`CP-P04-T01-T05.md`, `CP-P04-T07-T11.md`,
`CP-P04-T13-T17.md`) sit at `status: PASS`, and both literal M4 exit
criteria are met on the live tree.

The Expect DSL primitives and the `superclaude eval` CLI surface
required by the FR-EXP1 → FR-CLI1 → FR-G4 → FR-G5 → FR-G6 roadmap are
complete. All seven Expect primitives (`Expect.file`, `Expect.jsonl`,
`Expect.settings_json`, `Expect.exit_code`, `Expect.stderr`,
`Expect.stdout`, `Expect.duration`) live at
`src/superclaude/cli/eval/expect.py:187,270,374,485,556,572,590` with
working `ExpectCallable` bodies — no `NotImplementedError("M4")` stubs
remain. Each primitive returns an `ExpectResult` that surfaces a
unified diff / predicate detail on failure and supports both
declarative (YAML mapping) and programmatic (direct method call)
invocation forms.

The Click surface ships `eval_group` with `run / list / describe /
doctor` subcommands wired through `superclaude eval` (COMP-001 /
T04.09); `eval run` exposes the full FR-CLI1 12-flag set —
`--suite, --parallel, --eval, --no-mcp, --no-pty, --output-dir,
--keep-home, --timeout-mult, --max-disk-mb, --json, --verbose,
--junit` (plus the built-in `--help`); the smoke test
`tests/cli/eval/test_single_command.py` exercises FR-G6 end-to-end and
exits clean.

FR-G4 (T04.13) places each run beneath
`.dev/eval-runs/<ISO>/<run-id>/` with the prescribed
`summary.{md,json}` + `per-eval/{logs.jsonl,tty.transcript,artifacts/}`
subtree via the deterministic `compose_run_id`, `compose_run_dir`,
`compose_per_eval_dir`, and `allocate_per_eval_paths` helpers.
FR-G5 (T04.14) ships the `coverage_gate(settings_path, suite)` checker
plus `eval doctor --check-coverage` wiring; the v1 matcher set
(`mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*`)
resolves to covering evals, an uncovered fourth matcher emits a
`coverage_missing:<pattern>` artifact and fails with exit 2, and the
JSON payload carries the missing list.

DOC-OQ7 (T04.15) lands the `--junit` decision as path **A** —
`--junit` is wired into FR-CLI1 with `junit.xml` emission gated on
the flag; closure section at `decisions.md:533`. DOC-OQ3 (T04.16)
lands the `--no-pty` exclusion set as the per-eval `no_pty: skip`
tag in `src/superclaude/cli/eval/suites/real.yaml`; the flag is
honoured end-to-end and the tag is surfaced by `eval describe`.

TEST-007 (T04.17) pins the FR-RPT1 contract behavior at the reporter
boundary (N'-vs-K equality, skipped-row inclusion with `skip_reason`,
N'-vs-K mismatch → `ReporterContractViolation` (exit 2),
`summary.json` schema fidelity). TEST-008 (T04.19) pins the
process-exit-code policy (0 clean / 1 failures / 2 harness error / 3
interrupted) via `tests/cli/eval/test_exit_codes.py`. TEST-009
(T04.20) pins artifact reproducibility for run-dir pattern + per-eval
artefact presence + stack-trace-on-error + summary cross-link via
`tests/cli/eval/test_artifact_reproducibility.py`. OPS-003 (T04.21)
lands `docs/eval/retention.md` documenting `--keep-home` default
false, failed-setup preservation, summary retention, and the disk-
budget retention-advice string verbatim.

Both M4 exit criteria are met on the current tree:

1. `uv run pytest tests/cli/eval/ -v` → **1359 passed, 4 skipped,
   5 warnings in 19.55 s, exit 0** (2026-05-21). Full log:
   `evidence/T04.22/exit-criteria-pytest.log`.
2. `uv run ruff check src/superclaude/cli/eval/` → **All checks
   passed!, exit 0** (2026-05-21). Full log:
   `evidence/T04.22/ruff-check.log`.

The earlier failure cluster recorded against this checkpoint
(`tests/cli/eval/test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr`
and the F401/F821 ruff residue from the partial T04.10 wiring) was
consumed by commit `08183738 fix(cliEval): clear residual F401 +
Click 8.3.2 mix_stderr + delete stale T04.09 skeleton tests/constants`,
which removed the obsolete skeleton test, fixed the unused-import set
in `commands.py`, and dropped the now-superseded `mix_stderr` kwarg
(Click 8.3.2 removed it). The clean re-run above confirms M4 inherits
a green lint and test floor.

The behavioural M4 contract — all seven Expect primitives reachable
with passing tests, `superclaude eval run --suite real` parses every
documented flag, manifest `expects:` blocks executable in both
declarative and programmatic forms, and the coverage-gate CLI entry
green for the one-matcher fixture suite — is met at both the test
level and the artefact level. Phase 5 (M5) may proceed to the eval
corpus (E1–E15) and the in-CI fitness work without M4-resident
remediation debt.

## Per-upstream-task status

| Task   | Roadmap | Deliverable | Status | Notes |
|--------|---------|-------------|--------|-------|
| T04.01 | R-064   | D-0064      | PASS   | FR-EXP1 `Expect` package at `src/superclaude/cli/eval/expect.py`; M1 `NotImplementedError("M4")` stubs replaced with real primitives backed by `EvalContext`; declarative YAML + programmatic forms produce equivalent results. Closed under `CP-P04-T01-T05.md`. |
| T04.02 | R-065   | D-0065      | PASS   | `Expect.file(path, exists, contains, regex, equals)` at `expect.py:187`; ExpectResult includes unified diff on failure; `tests/cli/eval/test_expect_file.py` covers all 5 argument combinations with pass/fail cases. Closed under `CP-P04-T01-T05.md`. |
| T04.03 | R-066   | D-0066      | PASS   | `Expect.jsonl(path, line_count, filter, assert_each, assert_any)` at `expect.py:270`; `assert_any` returns `passed=True` when ≥1 filtered line satisfies predicate; `tests/cli/eval/test_expect_jsonl.py` covers all 5 named-argument combinations. Closed under `CP-P04-T01-T05.md`. |
| T04.04 | R-067   | D-0067      | PASS   | `Expect.settings_json(path, key_path, equals, exists)` at `expect.py:374` resolves `path` against `HomeIsolation.home_path`; dot-separated `key_path` navigation; `tests/cli/eval/test_expect_settings_json.py` covers presence + equality. Closed under `CP-P04-T01-T05.md`. |
| T04.05 | R-068   | D-0068      | PASS   | `Expect.exit_code(equals=0, in_set, not_equals)` at `expect.py:485`; mutually-exclusive args raise `ValueError`; default `equals=0`; `tests/cli/eval/test_expect_exit_code.py` covers each mode. Closed under `CP-P04-T01-T05.md`. |
| T04.06 | -       | D-CP04-MID-T01-T05 | PASS | `CP-P04-T01-T05.md` exists at `status: PASS`. |
| T04.07 | R-069   | D-0069      | PASS   | `Expect.stderr` / `Expect.stdout` at `expect.py:556,572` operate on ANSI-stripped buffers from COMP-011 PtyStream; share predicate engine; `tests/cli/eval/test_expect_stdio.py` covers `contains`, `regex`, `not_contains` for both. Closed under `CP-P04-T07-T11.md`. |
| T04.08 | R-070   | D-0070      | PASS   | `Expect.duration(max_sec, min_sec)` at `expect.py:590`; informational-PASS semantics when only one bound is set; `tests/cli/eval/test_expect_duration.py` covers max-only / min-only / both / neither cases. Closed under `CP-P04-T07-T11.md`. |
| T04.09 | R-071   | D-0071      | PASS   | COMP-001 `eval_group` Click group registered at the `superclaude` entry point; `superclaude eval --help` lists `run / list / describe / doctor`; T01.26 wiring preserved. Closed under `CP-P04-T07-T11.md`. |
| T04.10 | R-072   | D-0072      | PASS   | FR-CLI1 `eval run` exposes all 12 flags (`--suite, --parallel, --eval, --no-mcp, --no-pty, --output-dir, --keep-home, --timeout-mult, --max-disk-mb, --json, --verbose, --junit`); `--parallel` clamps to `[1,15]`; `--output-dir` resolved through AC12 allowlist; end-to-end one-eval invocation completes. Closed under `CP-P04-T07-T11.md`. |
| T04.11 | R-073   | D-0073      | PASS   | FR-G6 smoke test `tests/cli/eval/test_single_command.py` runs `uv run superclaude eval run --suite real --eval E1` end-to-end on a clean dev install (post `make dev`), asserts exit 0 and presence of `summary.{md,json}` under the per-run directory. Closed under `CP-P04-T07-T11.md`. |
| T04.12 | -       | D-CP04-MID-T07-T11 | PASS | `CP-P04-T07-T11.md` exists at `status: PASS`. |
| T04.13 | R-074   | D-0074      | PASS   | FR-G4 reproducible artifact layout — `compose_run_dir`, `compose_per_eval_dir`, `allocate_per_eval_paths`, `parse_run_dir_components`; each run produces `.dev/eval-runs/<ISO>/<run-id>/{summary.md,summary.json,per-eval/<eval-id>/{logs.jsonl,tty.transcript,artifacts/}}`; deterministic run-id; `tests/cli/eval/test_artifact_layout.py` (19/19). Closed under `CP-P04-T13-T17.md`. |
| T04.14 | R-075   | D-0075      | PASS   | FR-G5 `coverage_gate(settings_path, suite)` checker + `eval doctor --check-coverage` wiring; v1 matchers (`mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*`) resolve to covering evals; uncovered fourth matcher emits `coverage_missing:<pattern>` artifact and fails exit 2; JSON payload carries missing list; `tests/cli/eval/test_coverage_gate.py` (26/26 on re-verify). Closed under `CP-P04-T13-T17.md`. |
| T04.15 | R-076   | D-0076      | PASS   | DOC-OQ7 closed at `decisions.md:533` — path **A** chosen, `--junit` wired into FR-CLI1; `Reporter.to_junit()` + `emit_junit` gate land at `reporter.py:146,177,222-225`; CLI flag landed at `commands.py:1349-1352,1366,1593`; spec §4 table updated to 12 flags. Closed under `CP-P04-T13-T17.md`. |
| T04.16 | R-077   | D-0077      | PASS   | DOC-OQ3 closed — `no_pty: skip` per-eval tag landed in `src/superclaude/cli/eval/suites/real.yaml`; `--no-pty` flag honours tags with `skip_reason="--no-pty"`; `eval describe` surfaces the `no_pty` tag; `tests/cli/eval/test_no_pty_exclusion.py` (14/14). Closed under `CP-P04-T13-T17.md`. |
| T04.17 | R-078   | D-0078      | PASS   | TEST-007 reporter-contract suite `tests/cli/eval/test_reporter_contract.py` (4/4): N'-vs-K equality, skipped inclusion with `skip_reason`, N'-vs-K mismatch → `ReporterContractViolation` mapped to process exit 2, `summary.json` schema fidelity against `schemas/summary.schema.json`. Closed under `CP-P04-T13-T17.md`. |
| T04.18 | -       | D-CP04-MID-T13-T17 | PASS | `CP-P04-T13-T17.md` exists at `status: PASS`. |
| T04.19 | R-079   | D-0079      | PASS   | TEST-008 exit-code semantics `tests/cli/eval/test_exit_codes.py` — 0 clean / 1 failures / 2 harness-error / 3 interrupted; each test asserts via `subprocess.run` against `superclaude eval run`; spec at `artifacts/D-0079/spec.md` documents the policy. |
| T04.20 | R-080   | D-0080      | PASS   | TEST-009 artifact reproducibility `tests/cli/eval/test_artifact_reproducibility.py` — run dir matches `.dev/eval-runs/<ISO>/<run-id>/`; `logs.jsonl` + `tty.transcript` exist; stack trace recorded on ERRORED; `summary.json` `evals[]` entries cross-link to per-eval artifact paths. |
| T04.21 | R-081   | D-0081      | PASS   | OPS-003 retention policy at `docs/eval/retention.md` documents `--keep-home` default false, failed-setup preservation (NFR-ISO2), summary retention, and the disk-budget retention-advice text verbatim; `tests/cli/eval/test_retention_policy.py` (15 passed, 3 skipped — the 3 skips block on the production `_NullLifecycleExecutor` → real `EvalRunner` + `PtyDriver` swap and un-skip when the production executor replaces the null stub). |

**Roll-up:** 18 upstream tasks PASS (T04.01..T04.05, T04.07..T04.11,
T04.13..T04.17, T04.19..T04.21); 3 mid-phase checkpoints PASS (T04.06,
T04.12, T04.18). No FAILs. No carry-forward remediation debt.

## Verification (3/3 confirmed)

1. **All 7 Expect primitives reachable with tests passing** —
   CONFIRMED.
   - `Expect.file` (`expect.py:187`) / `Expect.jsonl` (`:270`) /
     `Expect.settings_json` (`:374`) / `Expect.exit_code` (`:485`) /
     `Expect.stderr` (`:556`) / `Expect.stdout` (`:572`) /
     `Expect.duration` (`:590`); zero `NotImplementedError` stubs
     remain in `src/superclaude/cli/eval/expect.py` (grep returns
     no hits).
   - Per-primitive test modules
     (`test_expect_file.py`, `test_expect_jsonl.py`,
     `test_expect_settings_json.py`, `test_expect_exit_code.py`,
     `test_expect_stdio.py`, `test_expect_duration.py`, plus the
     aggregate `test_expect_primitives.py`) all pass under the full
     `tests/cli/eval/ -v` run.
   - Evidence: `evidence/T04.22/exit-criteria-pytest.log`
     (1359 passed, 4 skipped).

2. **`superclaude eval run --help` lists all 12 FR-CLI1 flags** —
   CONFIRMED.
   - Flag count: 13 lines starting with `--` (12 documented FR-CLI1
     flags + the built-in `--help`).
   - Flags present: `--suite, --parallel, --eval, --no-mcp, --no-pty,
     --output-dir, --keep-home, --timeout-mult, --max-disk-mb,
     --json, --verbose, --junit`.
   - Evidence: `evidence/T04.22/eval-run-help.txt`.

3. **`coverage_gate` green for the one-matcher fixture suite; fails
   with `coverage_missing:<pattern>` when matcher uncovered** —
   CONFIRMED.
   - `tests/cli/eval/test_coverage_gate.py` → **26 passed in 0.18 s**
     on re-verify (2026-05-21);
     `test_coverage_gate_fails_when_fourth_matcher_added_without_eval`
     and `test_coverage_gate_fails_and_writes_artifact_for_uncovered_pattern`
     both assert the `coverage_missing:<pattern>` artifact and exit
     code 2; `test_cli_doctor_check_coverage_fails_when_uncovered_matcher_present`
     pins the CLI behaviour;
     `test_coverage_result_passed_is_true_when_no_missing` /
     `test_coverage_result_passed_is_false_when_missing_nonempty`
     pin the structural result.
   - Evidence: `evidence/T04.22/exit-criteria-pytest.log`,
     `evidence/T04.14/pytest.log`.

## Exit Criteria (3/3 met)

- `uv run pytest tests/cli/eval/ -v` passes for M4 modules — **MET**.
  - Actual: exit code **0**, **1359 passed, 4 skipped, 5 warnings in
    19.55 s**, on 2026-05-21.
  - Evidence: `evidence/T04.22/exit-criteria-pytest.log`.
  - The 5 warnings are the carry-forward `DeprecationWarning:
    forkpty() may lead to deadlocks` raised by the FR-G1
    `pty_lifecycle` and `signal_handling` tests that deliberately
    exercise `forkpty()` against the real `claude` binary — same set
    as `CP-P03-END.md`, expected, and does not affect the PASS
    determination. The 4 skips are the `_NullLifecycleExecutor`-gated
    cases in `test_retention_policy.py` (3) and one PTY-conditional
    case; all are documented at the call sites and un-skip when the
    production `EvalRunner + PtyDriver` executor replaces the null
    stub at M5.
- DOC-OQ7 and DOC-OQ3 decisions recorded in `decisions.md` —
  **MET**.
  - DOC-OQ7 closure at `decisions.md:533` ("DOC-OQ7 Closure —
    `--junit` flag wiring decision (T04.15)"), path **A** chosen.
  - DOC-OQ3 resolution at `decisions.md:1199` (OPS-001 §B closure
    block + roadmap row 254 reference); `no_pty: skip` tag landed
    in `suites/real.yaml`; `eval describe` and `eval run --no-pty`
    both honour it.
- Checkpoint report `CP-P04-END.md` records pass/fail per task in
  Phase 4 — **MET** (this file, *Per-upstream-task status* table
  above).

## Acceptance Criteria

- File `TASKLIST_ROOT/checkpoints/CP-P04-END.md` exists and contains
  `status: PASS` — **MET**.
- All 3 Verification bullets are confirmed — **MET**.
- All 3 Exit Criteria bullets are met — **MET**.
- Checkpoint report includes the task IDs it covers (T04.01–T04.21) —
  **MET** (header + per-task status table).

## Artifacts and evidence

- Mid-phase checkpoints: `CP-P04-T01-T05.md` (PASS — T04.01..T04.05),
  `CP-P04-T07-T11.md` (PASS — T04.07..T04.11),
  `CP-P04-T13-T17.md` (PASS — T04.13..T04.17).
- Per-task artifacts under `artifacts/D-0064..D-0081/` — every M4
  deliverable directory populated with `spec.md`, `notes.md`,
  `evidence.md`.
- Per-task evidence under `evidence/T04.01..T04.21/` — every M4 task
  has a per-task evidence directory; no missing entries.
- M4-suite pytest log captured live during this checkpoint:
  `evidence/T04.22/exit-criteria-pytest.log` → 1359 passed, 4 skipped,
  exit 0.
- M4-suite ruff log captured live during this checkpoint:
  `evidence/T04.22/ruff-check.log` → All checks passed!, exit 0.
- `superclaude eval run --help` capture for the 12-flag count audit:
  `evidence/T04.22/eval-run-help.txt`.

## Cross-references

- Phase tasklist: `.dev/releases/current/cliEval/phase-4-tasklist.md`
  (T04.22 § lines 1040–1089; covered tasks T04.01–T04.21 at lines
  5–1038).
- Roadmap items: R-064..R-081 spanning FR-EXP1 (R-064) → OPS-003
  retention (R-081).
- Prior Phase 4 checkpoints: `CP-P04-T01-T05.md`,
  `CP-P04-T07-T11.md`, `CP-P04-T13-T17.md`.
- Prior milestone exits: Phase 3 closed at `CP-P03-END.md`
  (PASS — RunOrchestrator + Reporter + signal handling + FR-G1
  baseline landed).
- Relevant ADRs / design-spec sections:
  - design-spec §4 (Exit codes table) — pinned by TEST-008 (T04.19);
    spec §4 flag table updated under DOC-OQ7 (T04.15) to list
    `--junit` for the 12-flag set.
  - design-spec §9 (Artifact tree) — landed by FR-G4 (T04.13) and
    pinned by TEST-009 (T04.20).
  - design-spec §10 (Reporter emitters) — `to_junit()` retained
    under DOC-OQ7 (T04.15); reporter-contract behaviour pinned by
    TEST-007 (T04.17).
  - design-spec §11 (CLI surface) — FR-CLI1 12-flag set landed by
    T04.10; FR-G6 single-command runnability pinned by T04.11.
  - FR-EXP1 (Expect primitives) — landed across T04.01..T04.08 with
    no residual `NotImplementedError` stubs.
  - FR-CLI1 (12-flag CLI surface) — landed in T04.10; group surface
    in T04.09.
  - FR-G4 (per-run artifact layout) — landed in T04.13.
  - FR-G5 (matcher coverage gate) — landed in T04.14.
  - FR-G6 (single-command runnability) — landed in T04.11.
  - OPS-003 (retention policy) — landed in T04.21
    (`docs/eval/retention.md`).
  - TEST-007 / TEST-008 / TEST-009 — landed in T04.17 / T04.19 /
    T04.20.
- Downstream gate: Phase 5 entry (M5) is unblocked by this PASS;
  M5 owns the eval corpus E1–E15 (sticky lifecycle, hook-matcher
  evals, doctor capability evals), the FR-G5 full-coverage validation
  against the real `~/.claude/settings.json`, and the in-CI fitness
  work that promotes the M4 single-command smoke test to the broader
  `tests/cli/eval/` parity gate.
