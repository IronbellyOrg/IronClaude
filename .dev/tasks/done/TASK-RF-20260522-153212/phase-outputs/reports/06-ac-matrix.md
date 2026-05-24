# AC Matrix — cliEval Remediation TASK-RF-20260522-153212

Mapping every spec finding (H1-H5, M1-M6, CC1-CC3) and every new test (T1-T9)
to its remediation step, source edit, test evidence, and verification artifact.

| Finding ID | Description | Remediation Step(s) | Source Edit(s) | Test(s) | Verification Evidence | Status |
|---|---|---|---|---|---|---|
| **H1** | `--output-dir` flat layout (FR-G4) | Step 4.1 | commands.py:eval_run resolved_output_root + compose_run_dir + writer rebinding | T1 (test_run_anchors_output_via_compose_run_dir in test_eval_run.py) | phase-outputs/test-results/04-pytest.txt, 06-grep-gates-final.txt GATE 1 | RESOLVED |
| **H2** | coverage.py silent-green on corrupt settings.json (FR-G5) | Step 3.2 | coverage.py:294-302 → CoverageResult(passed=False, parse_error=...) + new dataclass field | T3 (test_coverage_gate_fails_on_corrupt_settings_json in test_coverage_gate.py) | phase-outputs/test-results/03-h2-pytest.txt | RESOLVED |
| **H3** | _format_run_summary_line elides ERRORED/INTERRUPTED/TIMEOUT | Step 3.3 | commands.py:_format_run_summary_line → full P/F/S/E/I/T taxonomy | T2 (test_format_run_summary_line_renders_errored_interrupted_timeout in test_run_summary.py) | phase-outputs/test-results/03-h3-pytest.txt | RESOLVED |
| **H4** | resolve_scratch_root accepts bare allowlist prefix (AC12 tautology) | Step 3.1 + isolation.py:307-336 layered re-check refactor | config.py:243-249 removed `resolved == prefix` branch; isolation.py containment_guard Check 2 now does its own equal-or-subpath check inline | T5 inverted (test_resolve_scratch_root_rejects_bare_prefix in test_scratch_root_allowlist.py) + T5b (test_accepts_immediate_subdir_of_allowlist_root) | phase-outputs/test-results/03-h4-pytest.txt | RESOLVED |
| **H5a** | commands.py home_root.mkdir before allowlist extension (OPS-002) | Step 4.3 (folded into Step 4.1's H1 edit) | commands.py:1727-1752 reordered: runtime_allowed + runtime_config built BEFORE home_root.mkdir | T4a (test_eval_run_extends_allowlist_before_mkdir in test_home_isolation_extend.py) | phase-outputs/test-results/04-h5a-pytest.txt, 06-grep-gates-final.txt GATE 2 (L1768 precedes L1783) | RESOLVED |
| **H5b** | isolation.py:533 home_root.mkdir before containment pre-check | Step 4.4 + 14 collateral test updates | isolation.py:550-577 — equal-or-subpath allowlist pre-check before self.home_root.mkdir | T4b (test_home_isolation_setup_rejects_non_allowlisted_home_root_before_mkdir in test_containment.py) + 14 updated tests across test_atomic_setup.py, test_symlink_attacks.py, test_hard_guard_real_home.py, test_path_containment.py | phase-outputs/test-results/04-h5b-pytest.txt | RESOLVED |
| **M1** | `_default_output_dir()` CWD-binding | OQ-3 (DROPPED from scope) | (no source change) | (no test added) | Follow-Up Items entry; OQ-3 decision in phase-outputs/plans/01-oq-decisions.md | DEFERRED-SPEC §4 |
| **M2** | _NullLifecycleExecutor active emits no WARNING | Step 3.5 | commands.py:1448 (call site) — `click.echo("eval run: WARNING: _NullLifecycleExecutor active...", err=True)` | T6 (test_run_emits_warning_when_null_lifecycle_executor_active in test_eval_run.py) | phase-outputs/test-results/03-m2-pytest.txt | RESOLVED |
| **M3** | RunTotals keys hardcoded literals (drift from EVAL_STATUSES) | Step 3.4 | models.py adds SKIPPED_STATUSES/PASSED_STATUSES/FAILED_STATUSES constants; commands.py:_compute_run_stats uses them | (covered by full eval suite regression — no dedicated test) | phase-outputs/test-results/03-m3-pytest.txt | RESOLVED |
| **M4** | Reporter and run_report writers diverge on summary.yaml | Step 4.2 | Promoted render_summary_yaml to run_report.py + shared `_write_artifact_set` helper; both writers delegate | (covered by updated test_writer_emits_markdown_json_and_yaml in test_run_report.py) | phase-outputs/test-results/04-m4-pytest.txt | RESOLVED |
| **M5** | session_id ad-hoc construction at commands.py callsite | Step 5.5 | orchestrator.py adds `allocate_session_id(run_id, eval_id)`; commands.py:_run_one_spec takes run_id kwarg and calls helper | T7 (test_run_one_spec_uses_orchestrator_allocate_session_id + test_orchestrator_allocates_unique_session_id_per_run in test_orchestrator.py) | phase-outputs/test-results/05-m5-pytest.txt | RESOLVED |
| **M6** | Click `Path` option asymmetry (eval doctor lacks file_okay=False) | Step 5.6 | commands.py:784 — added `file_okay=False` to eval doctor --output-dir option | (covered by full suite + eval doctor --help capture at phase-outputs/test-results/05-m6-doctor-help.txt) | phase-outputs/test-results/05-m6-doctor-help.txt + 05-m6-run-help.txt | RESOLVED |
| **CC1** | EVAL_ID regex duplication between artifact_layout.py and loader.py | Step 5.1 (OQ-1 Rename + Promote + Import synthesis) | artifact_layout.py: `_EVAL_ID_RE` → `_EVAL_ID_PATH_SAFETY_PATTERN` + new public `EVAL_ID_PATTERN`; loader.py: `from .artifact_layout import EVAL_ID_PATTERN as EVAL_ID_REGEX` (alias) | T8 (test_eval_id_pattern_single_source in test_eval_id_regex.py) | phase-outputs/test-results/05-cc1-pytest.txt + 05-t8-pytest.txt + 06-grep-gates-final.txt GATE 3 (2 re.compile in artifact_layout, 0 in loader) | RESOLVED |
| **CC2** | 11 sites of `*_EXIT_CODE: int = 2` declarations duplicating literal | Step 5.3 (OQ-2 — 4 canonical values + 11 re-exports via top-of-file import) | exit_codes.py NEW (SUCCESS=0/FAILURES=1/USAGE_ERROR=2/INTERRUPTED=3); 6 consumer files refactored to `from . import exit_codes as _exit_codes` + local `NAME: int = _exit_codes.VALUE` | T9 (test_no_magic_exit_code_literals_in_eval_module in test_exit_codes.py) | phase-outputs/test-results/05-cc2-pytest.txt + 05-t9-pytest.txt + 06-grep-gates-final.txt GATES 4 & 5 | RESOLVED |
| **CC3** | _NullLifecycleExecutor observability gap | (folded into M2 per spec §5) | (see M2 row) | (see M2 row) | (see M2 row) | RESOLVED-VIA-M2 |
| **T1** | compose_run_dir anchor test | Step 4.5 | (test addition only — no source) | test_run_anchors_output_via_compose_run_dir in test_eval_run.py | phase-outputs/test-results/04-pytest.txt | RESOLVED |
| **T2** | _format_run_summary_line E/I/T parametrized | Step 4.6 | (test addition only) | test_format_run_summary_line_renders_errored_interrupted_timeout in test_run_summary.py | phase-outputs/test-results/04-pytest.txt | RESOLVED |
| **T3** | corrupt settings.json fails closed | Step 2.1 | (test addition only) | test_coverage_gate_fails_on_corrupt_settings_json in test_coverage_gate.py | phase-outputs/test-results/03-h2-pytest.txt | RESOLVED |
| **T4a** | commands.py allowlist-before-mkdir ordering | Step 4.7 | (test addition only) | test_eval_run_extends_allowlist_before_mkdir in test_home_isolation_extend.py | phase-outputs/test-results/04-pytest.txt | RESOLVED |
| **T4b** | isolation.py containment pre-check before mkdir | Step 4.8 | (test addition only) | test_home_isolation_setup_rejects_non_allowlisted_home_root_before_mkdir in test_containment.py | phase-outputs/test-results/04-pytest.txt | RESOLVED |
| **T5** | resolve_scratch_root rejects bare prefix (inverted) | Step 2.2 | (test inversion only) | test_resolve_scratch_root_rejects_bare_prefix in test_scratch_root_allowlist.py | phase-outputs/test-results/02-pytest-red-baseline.txt + 03-h4-pytest.txt | RESOLVED |
| **T5b** | resolve_scratch_root accepts strict subdir | Step 2.2b | (test addition only) | test_accepts_immediate_subdir_of_allowlist_root in test_scratch_root_allowlist.py | phase-outputs/test-results/03-h4-pytest.txt | RESOLVED |
| **T6** | NullLifecycleExecutor stderr WARNING | Step 2.3 | (test addition only) | test_run_emits_warning_when_null_lifecycle_executor_active in test_eval_run.py | phase-outputs/test-results/03-m2-pytest.txt | RESOLVED |
| **T7** | session_id orchestrator ownership | Step 5.7 | (test addition only) | test_run_one_spec_uses_orchestrator_allocate_session_id in test_orchestrator.py | phase-outputs/test-results/05-m5-pytest.txt | RESOLVED |
| **T8** | EVAL_ID_PATTERN single-source-of-truth | Step 5.2 | (test addition only) | test_eval_id_pattern_single_source in test_eval_id_regex.py | phase-outputs/test-results/05-t8-pytest.txt | RESOLVED |
| **T9** | no magic exit codes outside exit_codes.py | Step 5.4 | (test addition only — plus docstring fix in commands.py:23) | test_no_magic_exit_code_literals_in_eval_module in test_exit_codes.py | phase-outputs/test-results/05-t9-pytest.txt | RESOLVED |

## Summary

- **Total findings tracked:** 23 rows (5 High + 6 Medium + 3 CC + 9 Tests = 23; CC3 rolls into M2 per spec §5 but still gets a row pointing at M2's evidence).
- **Status breakdown:**
  - **RESOLVED:** 22 (5 High + 5 Medium [M2-M6] + 2 CC [CC1+CC2] + 1 CC3-via-M2 + 9 Tests)
  - **DEFERRED-SPEC §4:** 1 (M1 — see Follow-Up Items + OQ-3 decision)
- **Resolution rate:** 22/23 (95.6%) RESOLVED; 1/23 (4.3%) deferred-with-rationale; 0 SKIPPED, 0 WONTFIX.
- **Test additions:** 9 new test functions (T1-T9) + 1 collateral positive test (T5b) = 10 new tests.
- **New source files:** 1 (`src/superclaude/cli/eval/exit_codes.py`).
- **Source files modified:** 9 (commands.py, coverage.py, config.py, isolation.py, reporter.py, run_report.py, artifact_layout.py, loader.py, orchestrator.py, models.py, **init**.py — count includes models.py + **init**.py M3 re-exports).

## Phase Gate Verdicts

- **PG-1** (Phase 2 test scaffolding QA): PASS at cycle 1 — see `phase-outputs/plans/PG-1-final-verdict.md`.
- **PG-2** (Phase 4 layout + ordering QA): PASS at cycle 1 — see `phase-outputs/plans/PG-2-final-verdict.md`.
- **PG-FINAL** (composite task-integrity): pending — Step PG-FINAL.2 spawns rf-qa with `fix_authorization: true`.

## Static Grep Gates (VALIDATION_REQUIREMENTS §5)

| Gate | Description | Expected | Actual | Status |
|---|---|---|---|---|
| GATE 1 | H1 — `run_dir=resolved_output` | 0 hits | 0 hits | PASS |
| GATE 2 | H5 — `runtime_allowed` precedes `home_root.mkdir` in commands.py | runtime_allowed line < home_root.mkdir line | L1768 < L1783 | PASS |
| GATE 3 | CC1 — `re.compile` of eval-id patterns | 2 in artifact_layout.py, 0 in loader.py | 2 in artifact_layout.py, 0 in loader.py | PASS |
| GATE 4 | CC2 — `sys.exit(N)` / `Exit(N)` literals | 0 hits | 0 hits | PASS |
| GATE 5 | CC2 per OQ-2 — `*_EXIT_CODE = <literal-int>` outside exit_codes.py | 0 hits outside exit_codes.py | 0 hits | PASS |

## VALIDATION_REQUIREMENTS Compliance

- §3 (5 static grep gates): ALL PASS.
- §4 (eval run --help diff vs baseline): EMPTY (DIFF_EXIT_CODE=0).
- §4 (eval doctor --help diff vs baseline): EXPECTED DIFF (M6 adds `file_okay=False`).
- §5 (full pytest exit 0): 1372 passed / 4 skipped / 0 failed.
- §5 (ruff F401/F821 exit 0): clean.
- §5 (make verify-sync exit 0): clean.
- §6 (no new pyproject.toml dependencies): pyproject.toml unchanged (EXIT_CODE=0 from git diff).
