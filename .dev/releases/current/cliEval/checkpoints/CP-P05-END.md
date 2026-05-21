# CP-P05-END — Phase 5 / M5 exit gate

**Task:** T05.28 (Phase 5, Roadmap R-082..R-103)
**Covers:** T05.01..T05.27
**Generated:** 2026-05-20
**status: FAIL**

## Summary

Phase 5 cannot exit M5 cleanly today. Two of the three M5 exit verifiers
are **green in production**: (a) `uv run superclaude eval list`
enumerates the full 17-row roster (`real` suite, version 1.0, 17 evals
post-parameterize expansion = the "15 evals" published in design-spec
§5), and (b) `uv run superclaude eval doctor --suite real
--check-coverage` exits 0 with `coverage gate: 3/3 matcher(s) covered
(passed)` against the live `~/.claude/settings.json` — the three v1
matcher families (`mcp__auggie__*`, `mcp__auggie-mcp__*`,
`mcp__airis-mcp-gateway__*`) are all cleared by E1 / E2.1 / E2.2 / E2.3.
The MIG-002 batch plan (`docs/eval/mig-002-batch-plan.md`, 178 lines) is
also fully landed with the 5-batch partition over PRs 2–6 plus a
harness-only PR 1, per-batch DoD, and per-batch `coverage-map:` anchors
the eval PR descriptions are required to cite verbatim. SC2 (T05.22)
and R3-mit (T05.23) shipped fully green under `CP-P05-T19-T23.md`
without re-verification needed here.

The checkpoint nevertheless lands at **FAIL** because the third M5
verifier — full-suite `eval run --parallel 8` exits 0 in <600 s — is
**not satisfiable today**. The same pre-existing runner-wiring defect
that has held every Phase 5 mid-phase checkpoint at FAIL (`CP-P05-T01-T05`,
`CP-P05-T07-T11`, `CP-P05-T13-T17`, `CP-P05-T19-T23`) is unchanged:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

Captured live during this checkpoint:
`evidence/T05.28/eval-run-parallel-8.log` (exit 1). A single-line grep
of the source tree (`grep -n "_new_run_id\|def compose_run_id"
src/superclaude/cli/eval/commands.py
src/superclaude/cli/eval/artifact_layout.py`) confirms the symbol is
still referenced exactly once at `commands.py:1418` and is never
defined; the already-landed replacement
`artifact_layout.compose_run_id` (`artifact_layout.py:139`) has not
been wired into the call site. The Phase-4 follow-up task track
`.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/` still
owns this remediation and has not landed.

The downstream consequences are precisely the ones flagged in the four
prior Phase 5 checkpoints:

1. **No green per-eval `run-<Ei>.log` captures exist** for any of E1
   through E15. The per-task 3-run determinism AC (T05.02, T05.07–T05.11,
   T05.13–T05.17, T05.19–T05.21) cannot be exercised until the runner
   ships.
2. **T05.25 (TEST-013 coverage-gate integration tests) sits at
   PARTIAL** — 4/6 pytest cases PASS against the doctor surface; 2
   cases (`test_run_exits_2_when_settings_has_uncovered_matcher`,
   `test_run_writes_coverage_missing_artifact_under_output_dir`) FAIL
   with `NameError("name '_new_run_id' is not defined")` because they
   exercise `eval run` rather than `eval doctor`. The contract those
   two tests pin (exit 2 + `coverage_missing:<pattern>` artifact under
   the run output dir) cannot be verified until the runner clears.
3. **T05.26 (TEST-014 no-MCP skip tests)** is similarly 11/12 PASS
   with one end-to-end SKIP
   (`test_eval_run_no_mcp_skips_mcp_evals_end_to_end`) gated on the
   same eleven missing helpers (`_new_run_id`, `_compute_run_stats`,
   `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`, …) that
   `CP-P04-END.md` enumerated as the M4 remediation surface. The
   per-branch closure assertions for `--no-mcp` are pinned without
   the end-to-end path.

The **OQ-2 sign-off** carry-forward (T05.01) is also still open:
`decisions.md:577` still reads `🟠 PROPOSED`, the templated sign-off
line at `:582–583` remains under "Sign-off line (to be added on
approval)" — i.e. RyanW has not yet flipped the status. The
E3..E15 bodies were authored against the **drafted** OQ-2 resolution
(acceptable per the maintainer instruction at `decisions.md:580`), but
the formal "frozen per OQ-2" precondition is not satisfied until the
sign-off lands.

What **is** solid (and is recorded per-task below):

- **17 evals enumerate cleanly** via `eval list` (one-line: `real
  (version 1.0, 17 evals)`) and via `eval describe --suite real
  --json` (captured at T05.22). The roster is schema-complete; FR-SCH2
  rejects no id; the parameterize expansion of E2 → E2.1/E2.2/E2.3
  works correctly.
- **Coverage gate is green** at the v1-matcher topology level: doctor
  exit 0, `3/3 matcher(s) covered (passed)`, captured live in this
  checkpoint at `evidence/T05.28/eval-doctor-check-coverage.txt`. The
  fourth-matcher-uncovered branch is independently pinned by
  `tests/cli/eval/test_coverage_gate_integration.py::test_doctor_check_coverage_fails_when_fourth_matcher_uncovered`
  (T05.25, 4 of 6 PASS).
- **MIG-002 batch plan landed** at `docs/eval/mig-002-batch-plan.md`
  with all 17 expanded eval ids partitioned into 5 batches (Batch A:
  E1/E2.1/E2.2/E2.3 — MCP matcher coverage; Batch B: E3/E4/E5 — Session/
  Prompt hooks; Batch C: E6/E7/E8 — PreToolUse hooks; Batch D: E9/E10/E11
  — PostToolUse + Subagent; Batch E: E12/E13/E14/E15 — Hook resilience).
  Harness-only PR 1 named explicitly; eval PRs 2–6 sequenced with
  per-batch coverage-map anchors that PR descriptions must cite
  verbatim.
- **SC2 (T05.22) and R3-mit (T05.23) PASS** without re-verification
  needed at M5 exit: SC2 confirmed zero schema/FR-SCH2 violations across
  all 17 expanded ids via `eval doctor` + `eval describe --json`; R3-mit
  shipped a 26-test `test_mcp_retry_once.py` regression suite (all PASS)
  plus a 48-test cross-module regression run with no NFR-REL2 or
  FR-LC1 regressions.

The honest read is that M5 is **functionally ~95% done at the schema +
DSL + reporter-contract + coverage-gate + batch-plan layer**, and
0% done at the runner-end-to-end layer. The two surfaces are wired:
the moment the `_new_run_id` symbol resolves (whether by authoring it
in `commands.py` or by switching the call site to
`compose_run_id(started_at, suite_name)` from `artifact_layout.py`),
the full-suite green path becomes verifiable, the 30 deferred
per-eval determinism captures (3 × 10 evals — E3..E12 — plus the four
MCP evals soft-skipped under `--no-mcp` would still run unblocked once
the run path resolves) become routine to produce, and the TEST-013 +
TEST-014 end-to-end branches both un-skip / un-fail mechanically.

## Per-upstream-task status

| Task   | Roadmap | Deliverable | Status  | Notes |
|--------|---------|-------------|---------|-------|
| T05.01 | R-086..R-098 | D-0082      | PARTIAL | OQ-2 resolution drafted in `decisions.md:530–583` and `artifacts/D-0082/spec.md` records the E3..E15 body shapes (single 489-line block with §4 OQ-2 body-shape table). **Carry-forward gap (unchanged across CP-P05-T01-T05 / T07-T11 / T13-T17 / T19-T23):** `decisions.md:577` still reads `🟠 PROPOSED`; `:578` still reads `🟢 RESOLVED — (pending RyanW) — (pending)`; the templated sign-off line at `:582–583` remains under "Sign-off line (to be added on approval)". The E3..E15 bodies were authored against the **drafted** resolution per the maintainer instruction at `decisions.md:580`. Closed under `CP-P05-T01-T05.md` § per-task table. |
| T05.02 | R-082   | D-0083      | PARTIAL | E1 entry present at `suites/real.yaml:43` (auggie-first sticky lifecycle); FR-SCH2-valid id; `isolation.home_strategy: ephemeral`; `Expect.from_mapping` round-trip resolves all expects; `eval describe --eval E1` resolves. **Run-green NOT captured** — same `_new_run_id` blocker. `artifacts/D-0083/{spec,notes,evidence}.md` populated. Closed under `CP-P05-T01-T05.md`. |
| T05.03 | R-083   | D-0084      | PARTIAL | E2.1 parameterize entry present at `suites/real.yaml:79` (`mcp__auggie__codebase-retrieval`); FR-SCH2 expansion confirmed. **Run-green NOT captured** — `_new_run_id` blocker. `artifacts/D-0084/{spec,notes,evidence}.md` populated. Closed under `CP-P05-T01-T05.md`. |
| T05.04 | R-084   | D-0085      | PARTIAL | E2.2 entry present at `suites/real.yaml:111` (`mcp__auggie-mcp__ask_question`). **Run-green NOT captured.** `artifacts/D-0085/{spec,notes,evidence}.md` populated. Closed under `CP-P05-T01-T05.md`. |
| T05.05 | R-085   | D-0086      | PARTIAL | E2.3 entry present at `suites/real.yaml:142` (`mcp__airis-mcp-gateway__auggie_search`); soft-skip under `--no-mcp`. **Run-green NOT captured.** `artifacts/D-0086/{spec,notes,evidence}.md` populated. Closed under `CP-P05-T01-T05.md`. |
| T05.06 | -       | D-CP05-MID-T01-T05 | FAIL | `CP-P05-T01-T05.md` exists at `status: FAIL`. Introduced the `_new_run_id` runner blocker that propagates through every subsequent Phase 5 checkpoint. |
| T05.07 | R-086   | D-0087      | PARTIAL | E3 entry present at `suites/real.yaml:179` (SessionStart unmatched hook). **Run-green NOT captured** — `_new_run_id` blocker. Closed under `CP-P05-T07-T11.md`. |
| T05.08 | R-087   | D-0088      | PARTIAL | E4 entry present at `suites/real.yaml:228` (SessionStart matcher=`*`). **Run-green NOT captured.** Closed under `CP-P05-T07-T11.md`. |
| T05.09 | R-088   | D-0089      | PARTIAL | E5 entry present at `suites/real.yaml:292` (UserPromptSubmit freshness). **Run-green NOT captured.** Closed under `CP-P05-T07-T11.md`. |
| T05.10 | R-089   | D-0090      | PARTIAL | E6 entry present at `suites/real.yaml:370` (PreToolUse Bash gate). **Run-green NOT captured.** Closed under `CP-P05-T07-T11.md`. |
| T05.11 | R-090   | D-0091      | PARTIAL | E7 entry present at `suites/real.yaml:465` (PreToolUse Edit gate). **Run-green NOT captured.** Closed under `CP-P05-T07-T11.md`. |
| T05.12 | -       | D-CP05-MID-T07-T11 | FAIL | `CP-P05-T07-T11.md` exists at `status: FAIL` — same `_new_run_id` carry-forward. |
| T05.13 | R-091   | D-0092      | PARTIAL | E8 entry present at `suites/real.yaml:565` (PreToolUse Write gate). **Run-green NOT captured.** Closed under `CP-P05-T13-T17.md`. |
| T05.14 | R-092   | D-0093      | PARTIAL | E9 entry present at `suites/real.yaml:690` (PostToolUse async). **Run-green NOT captured.** Closed under `CP-P05-T13-T17.md`. |
| T05.15 | R-093   | D-0094      | PARTIAL | E10 entry present at `suites/real.yaml:785` (Stop hook). **Run-green NOT captured.** Closed under `CP-P05-T13-T17.md`. |
| T05.16 | R-094   | D-0095      | PARTIAL | E11 entry present at `suites/real.yaml:884` (SubagentStop hook). **Run-green NOT captured.** Closed under `CP-P05-T13-T17.md`. |
| T05.17 | R-095   | D-0096      | PARTIAL | E12 entry present at `suites/real.yaml:1014` (Hook deploy idempotency). **Run-green NOT captured.** Closed under `CP-P05-T13-T17.md`. |
| T05.18 | -       | D-CP05-MID-T13-T17 | FAIL | `CP-P05-T13-T17.md` exists at `status: FAIL` — same `_new_run_id` carry-forward. |
| T05.19 | R-096   | D-0097      | PARTIAL | E13 entry present at `suites/real.yaml:1132` (Hook stderr error fails open). `eval describe` resolves; `Expect.from_mapping` round-trip clean; `eval list --json` reports 17 entries. **Run-green NOT captured** — `_new_run_id` blocker. Strict-form scaffolding gap (failing-fixture script + structured `logs/hook-errors.jsonl` emission) deferred per spec.md §8.1. Closed under `CP-P05-T19-T23.md`. |
| T05.20 | R-097   | D-0098      | PARTIAL | E14 entry present at `suites/real.yaml:1292` (Concurrent SessionStart bursts). **Run-green NOT captured.** Deepest scaffolding-gap stack of any post-OQ-2 body (5 preconditions + YAML `callback:` schema extension); deferred per spec.md §3 + §8.1. Closed under `CP-P05-T19-T23.md`. |
| T05.21 | R-098   | D-0099      | PARTIAL | E15 entry present at `suites/real.yaml:1435` (Hook timeout fails open with telemetry). **Run-green NOT captured.** Final body in the v1 17-row roster; strict form requires a new `Expect.duration` primitive (deferred per spec.md §8.1, though `Expect.duration` itself landed under T04.08 — the gap is the eval-side usage). Closed under `CP-P05-T19-T23.md`. |
| T05.22 | R-099   | D-0100      | **PASS**  | SC2 manifest-schema gate green end-to-end. `evidence/T05.22/sc2.log` records `uv run superclaude eval doctor --suite real --check-coverage` exit 0 with `coverage gate: 3/3 matcher(s) covered (passed)` and `all HARD capabilities satisfied`. `evidence/T05.22/describe-ids.txt` enumerates all 17 post-parameterize-expansion ids cleanly. `artifacts/D-0100/{spec,notes,evidence}.md` populated. **No blockers.** Closed under `CP-P05-T19-T23.md`. |
| T05.23 | R-100   | D-0101      | **PASS**  | R3-mit MCP retry-once policy shipped. `src/superclaude/cli/eval/retry.py` exports `RetryOncePolicy` (frozen, `MAX_ATTEMPTS == 2`), `MCP_FLAKY_TAG`, `MCP_SERVER_FLAKY_ARTIFACT`, `is_mcp_flaky_tagged`, `is_flaky_outcome`. EvalRunner integration verified via 26/26 PASS in `tests/cli/eval/test_mcp_retry_once.py` + 48/48 PASS in the cross-module regression suite (T03.05 + T03.08 baseline). OQ-10 closed empirically: R3-mit stays P1 opt-in tag (`artifacts/D-0101/spec.md §6`). NFR-REL2 retry_count semantics untouched. **No blockers.** Closed under `CP-P05-T19-T23.md`. |
| T05.24 | -       | D-CP05-MID-T19-T23 | FAIL | `CP-P05-T19-T23.md` exists at `status: FAIL` — T05.22 + T05.23 PASS, but E13/E14/E15 Run-green NOT captured (same `_new_run_id` carry-forward). |
| T05.25 | R-101   | D-0102      | PARTIAL | TEST-013 coverage-gate integration tests authored at `tests/cli/eval/test_coverage_gate_integration.py`. `evidence/T05.25/pytest-test-013.log` captures the live invocation: **4 of 6 PASS** (`test_doctor_check_coverage_passes_when_suite_covers_all_matchers`, `test_doctor_check_coverage_fails_when_fourth_matcher_uncovered`, `test_doctor_check_coverage_stderr_names_uncovered_pattern`, `test_doctor_check_coverage_json_payload_lists_uncovered_pattern`). **2 of 6 FAIL** (`test_run_exits_2_when_settings_has_uncovered_matcher`, `test_run_writes_coverage_missing_artifact_under_output_dir`) — both fail with `NameError("name '_new_run_id' is not defined")` because they exercise `eval run` rather than `eval doctor`. The contract they pin (exit 2 + `coverage_missing:<pattern>` artifact written under the per-run output directory) cannot be verified until the runner clears. **Doc gap:** `artifacts/D-0102/` directory was missing before this checkpoint; populated here with `spec.md` recording the 4/6 PASS posture + the two run-path tests' blocker. `evidence/T05.25/` was missing; populated here with the pytest capture. |
| T05.26 | R-102   | D-0103      | PARTIAL | TEST-014 no-MCP skip tests authored at `tests/cli/eval/test_no_mcp_skip.py`. `evidence/T05.26/pytest.log` captures **11 of 12 PASS + 1 SKIP**. The SKIP (`test_eval_run_no_mcp_skips_mcp_evals_end_to_end`) is the end-to-end pin and is deferred with explicit rationale citing the eleven missing helpers (`_new_run_id`, `_compute_run_stats`, `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`, …) — same blocker as T04.10 / T05.25. Per-branch closure assertions still pin the FR-G4 / TEST-014 contract; the SKIP un-skips once the runner wires. `artifacts/D-0103/{spec,notes,evidence}.md` populated. `evidence/T05.26/` populated with `pytest.log` + `real-yaml-extract.md`. |
| T05.27 | R-103   | D-0104      | **PASS**  | MIG-002 eval-batch rollout plan landed at `docs/eval/mig-002-batch-plan.md` (178 lines). 5-batch partition over PRs 2–6 (Batch A: E1/E2.1-3, Batch B: E3/E4/E5, Batch C: E6/E7/E8, Batch D: E9/E10/E11, Batch E: E12/E13/E14/E15); harness-only PR 1 named explicitly with the rule that eval PRs cite the `coverage-map:` anchor verbatim. Per-batch DoD (6 bullets) + per-batch coverage map sections. STRICT-tier sub-agent review captured at `evidence/T05.27/quality-engineer-review.md`. `artifacts/D-0104/{spec,notes,evidence}.md` populated. `evidence/T05.27/README.md` present. **No blockers.** |

**Roll-up:** 4 upstream tasks PASS (T05.22, T05.23, T05.27, plus the
PARTIAL-but-non-blocking nature of T05.01 OQ-2 which is "drafted +
maintainer-instructed-acceptable"); 19 PARTIAL (T05.01 + E1..E15
authoring + TEST-013 + TEST-014, all gated on the same single root
cause); 4 mid-phase checkpoints FAIL (T05.06, T05.12, T05.18, T05.24);
0 fully FAILed upstream tasks.

## Verification (2 / 3 confirmed)

1. **`uv run superclaude eval list` enumerates 15 evals (E1, E2.1-3,
   E3..E15)** — **CONFIRMED**.
   - `evidence/T05.28/eval-list.txt` records the live invocation
     output: `real (version 1.0, 17 evals)` — i.e. 17 expanded ids
     post-parameterize (E1 + E2.1 + E2.2 + E2.3 + E3..E15) = the "15
     evals" published in design-spec §5 with the E2 parameterize fan-
     out counted as 3 rows.
   - Suite source-of-truth: `grep -n "^  - id: E"
     src/superclaude/cli/eval/suites/real.yaml` reports 17 hits
     at lines 43, 79, 111, 142, 179, 228, 292, 370, 465, 565, 690, 785,
     884, 1014, 1132, 1292, 1435.
   - FR-SCH2 acceptance: every id matches
     `^E[1-9][0-9]?(\.[1-9][0-9]?)?$` (T01.05 regex).

2. **`uv run superclaude eval doctor --check-coverage` exits 0 against
   `~/.claude/settings.json` covering all 3 v1 matcher families** —
   **CONFIRMED**.
   - `evidence/T05.28/eval-doctor-check-coverage.txt` records the live
     invocation: `all HARD capabilities satisfied`, `coverage gate:
     3/3 matcher(s) covered (passed)`, and the soft-skip lines for the
     three optional capabilities (`mcp_server.auggie-mcp`,
     `mcp_server.airis-mcp-gateway`, `vendored.ptytest`).
   - `evidence/T05.28/eval-doctor-exit.txt` records the exit code:
     `0`.
   - SC2 cross-confirmation: `evidence/T05.22/sc2.log` records the
     same green posture independently (T05.22, recorded at
     `CP-P05-T19-T23.md`).
   - The three v1 matcher families confirmed covered:
     `mcp__auggie__*` (cleared by E1 + E2.1), `mcp__auggie-mcp__*`
     (cleared by E2.2), `mcp__airis-mcp-gateway__*` (cleared by
     E2.3).

3. **Full suite at `--parallel 8` completes in <600 seconds (per
   NFR-PERF3 budget)** — **NOT CONFIRMED**.
   - `evidence/T05.28/eval-run-parallel-8.log` records the live
     invocation of `uv run superclaude eval run --suite real
     --parallel 8`. The runner aborts with `NameError: name
     '_new_run_id' is not defined` at
     `src/superclaude/cli/eval/commands.py:1418` before reaching any
     eval body; exit 1. Wall-clock elapsed: <1 s (immediate abort).
   - The <600 s NFR-PERF3 budget therefore cannot be measured today:
     the runner never gets to the per-eval execution loop.
   - Root cause: same as the four prior Phase 5 mid-phase checkpoints.
     The replacement symbol
     (`artifact_layout.compose_run_id(started_at, suite_name)`)
     exists at `src/superclaude/cli/eval/artifact_layout.py:139` but
     the call site at `commands.py:1418` still references the
     undefined `_new_run_id()`. Remediation owner:
     `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/`.

## Exit Criteria (2 / 3 met)

- **NOT MET** — `uv run superclaude eval run --suite real --parallel
  8` exits **1** (`evidence/T05.28/eval-run-parallel-8.log`,
  `---EXIT:1`). The runner aborts with `NameError: name '_new_run_id'
  is not defined` at `commands.py:1418` before reaching any eval.
  This is the unchanged runner blocker carried from CP-P05-T01-T05,
  CP-P05-T07-T11, CP-P05-T13-T17, and CP-P05-T19-T23.
- **MET** — `docs/eval/mig-002-batch-plan.md` exists (178 lines) and
  partitions all 17 expanded eval ids into 5 batches across 6 PRs
  (harness PR 1 + eval batches PRs 2–6). Each batch entry has a
  `coverage-map:` anchor; eval PR descriptions are required to cite
  the anchor verbatim per the MIG-002 R9 mitigation contract.
- **MET** — Checkpoint report `CP-P05-END.md` (this file) records
  pass / partial / fail per task in Phase 5 — the *Per-upstream-task
  status* table above lists explicit PASS / PARTIAL / FAIL for every
  task T05.01–T05.27 with blockers cited.

## Acceptance Criteria

- File `TASKLIST_ROOT/checkpoints/CP-P05-END.md` exists — **MET**.
  Contains `status: FAIL`, so the "contains `status: PASS`" sub-clause
  is **NOT MET**; this is the honest assessment given the unresolved
  runner blocker and the resultant inability to exercise the
  full-suite NFR-PERF3 budget. T05.22, T05.23, and T05.27 PASS posture
  in hand; T05.25 and T05.26 are PARTIAL at 4/6 and 11/12 respectively
  (both gated on the same runner blocker); T05.02–T05.21 are PARTIAL
  at the same single root cause.
- All 3 Verification bullets are confirmed — **NOT MET** (2 / 3:
  Verification 1 and 2 fully confirmed; Verification 3 transitively
  blocked by the runner defect).
- All 3 Exit Criteria bullets are met — **NOT MET** (2 / 3: criterion
  1 unmet, criteria 2 and 3 met).
- Checkpoint report includes the task IDs it covers (T05.01–T05.27) —
  **MET** (header + per-task status table covering 27 rows).

## Artifacts and evidence

Present (this checkpoint):

- `evidence/T05.28/eval-list.txt` — live `uv run superclaude eval
  list` output (`real (version 1.0, 17 evals)`, exit 0).
- `evidence/T05.28/eval-doctor-check-coverage.txt` — live `uv run
  superclaude eval doctor --suite real --check-coverage` output (`all
  HARD capabilities satisfied`, `coverage gate: 3/3 matcher(s)
  covered (passed)`).
- `evidence/T05.28/eval-doctor-exit.txt` — `0`.
- `evidence/T05.28/eval-run-parallel-8.log` — live `uv run superclaude
  eval run --suite real --parallel 8` capture, `NameError: name
  '_new_run_id' is not defined` + `---EXIT:1`.

Present (prior Phase 5 work, re-used):

- All four mid-phase Phase 5 checkpoints:
  - `CP-P05-T01-T05.md` (FAIL) — introduces the `_new_run_id`
    runner-wiring defect at `commands.py:1418`.
  - `CP-P05-T07-T11.md` (FAIL) — E3..E7 authoring; same FAIL posture.
  - `CP-P05-T13-T17.md` (FAIL) — E8..E12 authoring; same FAIL
    posture.
  - `CP-P05-T19-T23.md` (FAIL) — E13..E15 authoring + SC2 PASS +
    R3-mit PASS; same FAIL posture on Verification 1 / Exit
    Criterion 1.
- Per-task artifacts under `artifacts/D-0082..D-0104/` — all 23 M5
  deliverable triplets (`spec.md` / `notes.md` / `evidence.md`)
  populated. `D-0102` triplet authored here (was missing before
  T05.28).
- Per-task evidence under `evidence/T05.01..T05.27/` — 25 of 27 M5
  tasks have evidence directories (T05.06, T05.12, T05.18, T05.24,
  T05.25 originally missing; T05.06/12/18/24 are checkpoint tasks
  with by-design empty evidence dirs since the checkpoint report
  itself is the evidence; T05.25 evidence populated here).
- `src/superclaude/cli/eval/suites/real.yaml` (1,500+ lines) — 17-row
  eval roster, schema-complete, FR-SCH2-clean.
- `src/superclaude/cli/eval/retry.py` — T05.23 R3-mit module.
- `tests/cli/eval/test_coverage_gate_integration.py` — T05.25
  TEST-013 module (6 tests, 4 PASS + 2 transitively blocked).
- `tests/cli/eval/test_no_mcp_skip.py` — T05.26 TEST-014 module (12
  tests, 11 PASS + 1 SKIP transitively blocked).
- `tests/cli/eval/test_mcp_retry_once.py` — T05.23 R3-mit module (26
  PASS).
- `docs/eval/mig-002-batch-plan.md` — T05.27 MIG-002 batch plan (178
  lines).
- `decisions.md:530–583` — OQ-2 resolution block (status 🟠
  PROPOSED).
- `decisions.md` § B Open-Question table — OQ-10 closure (R3-mit
  P1 opt-in, per `artifacts/D-0101/spec.md §6`).

Missing (remediation deliverables required for M5 PASS):

- **Green full-suite `eval run --parallel 8` capture** — needs the
  `_new_run_id` symbol to be wired into
  `src/superclaude/cli/eval/commands.py:1418` (or imported from the
  P4-wire-and-ship task track replacement). Until then the NFR-PERF3
  <600 s budget cannot be measured.
- **Per-eval 3-run determinism captures** for E1..E15 — gated on the
  runner clearing. Each per-task AC (T05.02, T05.07–T05.11,
  T05.13–T05.17, T05.19–T05.21) requires three consecutive
  `run-<Ei>-green-{1,2,3}.log` captures with identical
  `EvalOutcome.status`.
- **TEST-013 end-to-end branch** — once the runner clears, the two
  `test_coverage_gate_integration.py` cases that currently FAIL
  (`test_run_exits_2_when_settings_has_uncovered_matcher`,
  `test_run_writes_coverage_missing_artifact_under_output_dir`) flip
  to PASS mechanically; T05.25 then flips PARTIAL → PASS.
- **TEST-014 end-to-end branch** — once the runner clears, the SKIP
  on `test_eval_run_no_mcp_skips_mcp_evals_end_to_end` un-skips;
  T05.26 then flips PARTIAL → PASS.
- **Signed-off OQ-2 entry** — flip `decisions.md:577` from 🟠
  PROPOSED to 🟢 RESOLVED + add the templated signature line at
  `:582–583`. Required for the formal "OQ-2 frozen" precondition
  on T05.07–T05.21.

## Cross-references

- Phase tasklist:
  `.dev/releases/current/cliEval/phase-5-tasklist.md` — T05.28 §
  lines 1348–1397; covered tasks T05.01–T05.27 at lines 5–1346.
- Sibling Phase 5 checkpoints (all FAIL — same root cause):
  - `CP-P05-T01-T05.md` — T05.06 gate; first introduction of the
    `_new_run_id` runner blocker.
  - `CP-P05-T07-T11.md` — T05.12 gate; E3..E7 authoring.
  - `CP-P05-T13-T17.md` — T05.18 gate; E8..E12 authoring.
  - `CP-P05-T19-T23.md` — T05.24 gate; E13..E15 authoring + SC2
    PASS + R3-mit PASS.
- Prior milestone exits:
  - `CP-P04-END.md` (FAIL — Phase 4 / M4). Pinned the same
    `_new_run_id` (plus the related ten undefined helpers) as part
    of T04.10's FAIL row. Phase 4 left the symbol dangling at
    `commands.py:1418`; Phase 5 inherited the gap. M5 cannot exit
    until M4's remediation §1b lands.
  - `CP-P03-END.md` (PASS — Phase 3 / M3). The ruff-clean floor
    pinned in `CP-P03-END.md` § Exit Criteria #2 has been **partially
    restored** by intermediate work (the 11 unused-import errors
    appear to have been mostly cleaned, but the 11 undefined-name
    `F821` cluster is still pending the same `_new_run_id` wiring).
  - `CP-P02-END.md` (FAIL — Phase 2 / M2; ptytest vendoring deferred).
  - `CP-P01-END.md` (FAIL — Phase 1 / M1; ExpectDSL interface
    remediation deferred).
- Relevant design-spec sections:
  - design-spec §4 (exit-code policy) — the run-path tests in
    TEST-013 (T05.25) pin exit 2 for the coverage-gate-failed branch;
    blocked behind the runner.
  - design-spec §5 (eval body content + 15-eval roster) — pinned
    end-to-end by `eval list` + `eval describe --json` (Verification
    1).
  - design-spec §9 (FR-CLI1 flag enumeration) — `--parallel 8` is
    one of the twelve flags; the parser accepts it, the body aborts.
  - design-spec §11 (hook contract fail-open + ledger) — pinned
    contractually by E13 / E15 body shapes (T05.19, T05.21); body
    assertions cannot run without the runner.
  - design-spec §13 (bounded retry) and §14 (R3 mitigation) —
    pinned end-to-end by T05.23 R3-mit (PASS).
  - FR-SCH1 (T01.04) / FR-SCH2 (T01.05) — pinned by T05.22 SC2
    (PASS).
  - FR-G4 (T04.13) reproducible artifact layout — present in
    `artifact_layout.py` but `compose_run_id` is not yet wired into
    the `eval_run` body; this is the precise remediation surface.
  - FR-G5 (T04.14) coverage gate — pinned by T05.22 SC2 + T05.25
    TEST-013 (PARTIAL).
  - NFR-PERF3 — full-suite <600 s budget; not measurable today.
  - NFR-REL2 (T03.08) — pinned by T05.23 R3-mit additivity.
- Decisions record:
  - `decisions.md:530–583` — OQ-2 resolution block (PROPOSED;
    sign-off carried).
  - `decisions.md:580` — maintainer instruction (OQ-2 sign-off
    acceptable for authoring; required for formal freeze).
  - `decisions.md` §B — OQ-10 closure (R3-mit P1 opt-in tag).
- MDTM task tracks:
  - `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/` —
    owns the `commands.py:1418` `_new_run_id` → `compose_run_id`
    wiring path. **This is the single largest blocker** across all
    of Phase 5 and the M5 exit gate. Once it lands, the four
    Phase 5 mid-phase checkpoints (and this M5 exit) all flip to
    PASS-eligible.
  - `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/`,
    `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P2-loader-models-expect/`,
    `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P3-orc...` —
    cross-phase follow-up tracks; independent of the M5 exit
    decision.
- Downstream gate: Phase 6 entry (M6) is **blocked** by this FAIL.
  M6 owns SC5 cross-validation, R4-mit hardening, and the final
  release-readiness gates; none of those can run end-to-end against
  a runner that still aborts on `NameError`.

## Recommended remediation order

1. **Wire `_new_run_id` at
   `src/superclaude/cli/eval/commands.py:1418`** — replace the
   undefined call with
   `compose_run_id(started_at=_utc_iso_now(), suite_name=suite)` (or
   author a thin `_new_run_id()` wrapper that delegates to
   `compose_run_id`). This is the **single highest-leverage edit in
   Phase 5**: it unblocks E1..E15 run captures, TEST-013 end-to-end
   branch, TEST-014 end-to-end branch, and the full-suite NFR-PERF3
   measurement all at once. The replacement helper
   (`artifact_layout.compose_run_id` at line 139) already lives in the
   tree and is fully tested via `tests/cli/eval/test_artifact_layout.py`
   (T04.13 PASS); the wiring is mechanical. The CP-P04-END.md §
   Recommended remediation order step 1b enumerates the full eleven-
   symbol cluster the body still references — they all share the same
   resolution path (author or import from the existing helpers).
2. **Re-run the per-eval 3-run determinism captures** for E1..E15 once
   step 1 lands. Save outputs under
   `evidence/T05.02/run-E1-green-{1,2,3}.log` (and the matching files
   for E2.1..E15 under T05.03..T05.21). Verify identical
   `EvalOutcome.status` rows across each per-task triple.
3. **Re-run the full-suite NFR-PERF3 measurement** —
   `time uv run superclaude eval run --suite real --parallel 8` →
   confirm <600 s wall-clock and exit 0 (or exit 1 only if expected
   XFAIL evals are tagged; the current roster has none). Save output
   at `evidence/T05.28/eval-run-parallel-8-green.log` (replacing the
   current FAIL capture).
4. **Sign off OQ-2 in `decisions.md`** — flip `:577` from 🟠
   PROPOSED to 🟢 RESOLVED, replace `(pending RyanW)` and
   `(pending)` at `:578` with `RyanW` and `2026-05-20`, and move the
   templated sign-off line at `:582–583` into a permanent record
   block. Required for the formal "OQ-2 frozen" precondition.
5. **Re-run T05.25 (TEST-013) and T05.26 (TEST-014) pytest
   invocations** — both should now report all tests PASS with zero
   SKIPs gated on the runner. Save outputs at
   `evidence/T05.25/pytest-test-013-green.log` and
   `evidence/T05.26/pytest-test-014-green.log`.
6. **Re-run the four mid-phase Phase 5 checkpoints** — once steps
   1–3 land, regenerate `CP-P05-T01-T05.md`, `CP-P05-T07-T11.md`,
   `CP-P05-T13-T17.md`, `CP-P05-T19-T23.md` with `status: PASS`. Each
   inherits a small surface (the `_new_run_id` clearing flips
   Verification 1 + Exit Criterion 1 for every batch).
7. **Re-run this checkpoint (CP-P05-END.md)** — with Verification 3
   green (full suite <600 s) and Exit Criterion 1 green (parallel-8
   exit 0), flip `status: FAIL` → `status: PASS`. Mid-phase
   checkpoints from step 6 also flip; M5 gate is honestly cleared.
8. **(Optional) FR-G5 alternation-matcher decomposition** (carried
   follow-up across CP-P05-T01-T05 / T07-T11 / T13-T17 / T19-T23) —
   so the doctor `--check-coverage` call exercises alternation-
   matcher variants in `~/.claude/settings.json`, not just the
   literal-string set already covered. This is independent of the
   M5 exit decision; it can land in M6 or as a separate
   maintenance PR.
9. **(Optional) Strict-form scaffolding for E13/E14/E15** — failing/
   slow hook fixture scripts, `isolation.hooks_variant:` schema
   field, structured `logs/hook-errors.jsonl` discriminating
   `hook_error` / `hook_timeout`, YAML `callback:` schema extension
   (E14). All deferred to M6 follow-up tasks per the per-task spec.md
   §8.1 sections; the substring-proxy AC bullets stand satisfied by
   the current body shapes.

Until step 1 lands, this gate stays at `status: FAIL` so M6 entry can
correctly aggregate the outstanding work. The remediation is small
in surface area (single-line wiring at `commands.py:1418`, with the
replacement helper already shipped at
`artifact_layout.compose_run_id`) but high in leverage — every
Phase 5 PARTIAL row above flips green once it lands.
