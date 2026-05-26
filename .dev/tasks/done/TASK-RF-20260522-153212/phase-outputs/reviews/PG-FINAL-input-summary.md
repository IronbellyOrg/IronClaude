=== PG-FINAL Input Summary ===

## Full source diff (all phases) — stat ===

 src/superclaude/cli/eval/__init__.py             |   6 +
 src/superclaude/cli/eval/artifact_layout.py      |  22 ++-
 src/superclaude/cli/eval/commands.py             | 194 ++++++++++++++---------
 src/superclaude/cli/eval/config.py               |  17 +-
 src/superclaude/cli/eval/coverage.py             |  42 +++--
 src/superclaude/cli/eval/disk_budget.py          |   5 +-
 src/superclaude/cli/eval/isolation.py            |  81 ++++++++--
 src/superclaude/cli/eval/loader.py               |  46 +++---
 src/superclaude/cli/eval/models.py               |   9 ++
 src/superclaude/cli/eval/orchestrator.py         |  19 ++-
 src/superclaude/cli/eval/pty/PROVENANCE.md       |   2 +-
 src/superclaude/cli/eval/reporter.py             |  77 +++------
 src/superclaude/cli/eval/run_report.py           | 108 ++++++++++---
 src/superclaude/cli/eval/suites/README.md        |   2 +
 tests/cli/eval/test_atomic_setup.py              | 123 +++++++++-----
 tests/cli/eval/test_containment.py               |  63 ++++++++
 tests/cli/eval/test_coverage_gate.py             |  29 +++-
 tests/cli/eval/test_coverage_gate_integration.py |  15 +-
 tests/cli/eval/test_eval_id_regex.py             |  31 ++++
 tests/cli/eval/test_exit_codes.py                |  60 +++++++
 tests/cli/eval/test_hard_guard_real_home.py      |  42 ++---
 tests/cli/eval/test_home_isolation_extend.py     | 114 +++++++++++++
 tests/cli/eval/test_orchestrator.py              |  44 ++++-
 tests/cli/eval/test_path_containment.py          |  29 ++--
 tests/cli/eval/test_run_report.py                |  11 +-
 tests/cli/eval/test_run_summary.py               |  41 +++++
 tests/cli/eval/test_scratch_root_allowlist.py    |  30 +++-
 tests/cli/eval/test_single_command.py            |  22 ++-
 tests/cli/eval/test_symlink_attacks.py           | 124 +++++++++------
 29 files changed, 1050 insertions(+), 358 deletions(-)

## All 5 grep gates final state

=== GATE 1 (H1): grep -rn 'run_dir=resolved_output' src/superclaude/cli/eval/ ===
0
(0 hits — PASS)

=== GATE 2 (H5): home_root.mkdir vs runtime_allowed ordering in commands.py ===
1765:    # ``home_root.mkdir`` below so the path is in the allowlist at the
1768:    runtime_allowed = tuple(base_config.allowed_scratch_roots) + (
1773:    runtime_config = EvalConfig(
1776:        allowed_scratch_roots=runtime_allowed,
1783:    home_root.mkdir(parents=True, exist_ok=True)

=== GATE 3 (CC1 per OQ-1): re.compile of eval-id patterns ===
Total re.compile() calls in eval module: 9
src/superclaude/cli/eval/artifact_layout.py:101:_EVAL_ID_PATH_SAFETY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
src/superclaude/cli/eval/artifact_layout.py:108:EVAL_ID_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$")

=== GATE 4 (CC2): no literal sys.exit(N) or Exit(N) ===
0
(0 hits — PASS)

=== GATE 5 (CC2 per OQ-2): no *_EXIT_CODE = <literal-int> outside exit_codes.py ===
0
(0 hits outside exit_codes.py — PASS)

## Final pytest

tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log[01-targeted-pytest] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log[02-make-verify-sync] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log[03-eval-doctor] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log[04-eval-run-E1] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 1. Contract] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 2. Command details + evidence locations] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 3. Execution order and idempotency] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 4. Acceptance map (T06.11)] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 5. Known blockers] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 6. Reproducibility] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 7. Cross-references] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_root_directory_exists PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[01-targeted-pytest] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[02-make-verify-sync] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[03-eval-doctor] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[04-eval-run-E1] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_records_known_blockers_section PASSED [100%]

=============================== warnings summary ===============================
tests/cli/eval/test_pty_lifecycle.py::test_real_claude_help_spawn_and_transcript
tests/cli/eval/test_pty_lifecycle.py::test_lifecycle_prompt_ready_and_input_injection
tests/cli/eval/test_pty_lifecycle.py::test_lifecycle_timeout_reaps_child
tests/cli/eval/test_pty_lifecycle.py::test_lifecycle_transcript_persisted_end_to_end
tests/cli/eval/test_signal_handling.py::test_pty_driver_terminate_kills_real_subprocess
  /config/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/pty.py:95: DeprecationWarning: This process (pid=1920380) is multi-threaded, use of forkpty() may lead to deadlocks in the child.
    pid, fd = os.forkpty()

-- Docs: <https://docs.pytest.org/en/stable/how-to/capture-warnings.html>
================= 1372 passed, 4 skipped, 5 warnings in 19.68s =================
EXIT_CODE=0

## Final ruff

All checks passed!
EXIT_CODE=0

## Final verify-sync

✅ All components in sync.
EXIT_CODE=0

## pyproject.toml diff (must be empty)

EXIT_CODE=0

## eval run --help diff (must be empty)

DIFF_EXIT_CODE=0

## AC Matrix

# AC Matrix — cliEval Remediation TASK-RF-20260522-153212

Mapping every spec finding (H1-H5, M1-M6, CC1-CC3) and every new test (T1-T9)
to its remediation step, source edit, test evidence, and verification artifact.

| Finding ID | Description | Remediation Step(s) | Source Edit(s) | Test(s) | Verification Evidence | Status |
|---|---|---|---|---|---|---|
| __H1__ | `--output-dir` flat layout (FR-G4) | Step 4.1 | commands.py:eval_run resolved_output_root + compose_run_dir + writer rebinding | T1 (test_run_anchors_output_via_compose_run_dir in test_eval_run.py) | phase-outputs/test-results/04-pytest.txt, 06-grep-gates-final.txt GATE 1 | RESOLVED |
| __H2__ | coverage.py silent-green on corrupt settings.json (FR-G5) | Step 3.2 | coverage.py:294-302 → CoverageResult(passed=False, parse_error=...) + new dataclass field | T3 (test_coverage_gate_fails_on_corrupt_settings_json in test_coverage_gate.py) | phase-outputs/test-results/03-h2-pytest.txt | RESOLVED |
| __H3__ | _format_run_summary_line elides ERRORED/INTERRUPTED/TIMEOUT | Step 3.3 | commands.py:_format_run_summary_line → full P/F/S/E/I/T taxonomy | T2 (test_format_run_summary_line_renders_errored_interrupted_timeout in test_run_summary.py) | phase-outputs/test-results/03-h3-pytest.txt | RESOLVED |
| __H4__ | resolve_scratch_root accepts bare allowlist prefix (AC12 tautology) | Step 3.1 + isolation.py:307-336 layered re-check refactor | config.py:243-249 removed `resolved == prefix` branch; isolation.py containment_guard Check 2 now does its own equal-or-subpath check inline | T5 inverted (test_resolve_scratch_root_rejects_bare_prefix in test_scratch_root_allowlist.py) + T5b (test_accepts_immediate_subdir_of_allowlist_root) | phase-outputs/test-results/03-h4-pytest.txt | RESOLVED |
| __H5a__ | commands.py home_root.mkdir before allowlist extension (OPS-002) | Step 4.3 (folded into Step 4.1's H1 edit) | commands.py:1727-1752 reordered: runtime_allowed + runtime_config built BEFORE home_root.mkdir | T4a (test_eval_run_extends_allowlist_before_mkdir in test_home_isolation_extend.py) | phase-outputs/test-results/04-h5a-pytest.txt, 06-grep-gates-final.txt GATE 2 (L1768 precedes L1783) | RESOLVED |
| __H5b__ | isolation.py:533 home_root.mkdir before containment pre-check | Step 4.4 + 14 collateral test updates | isolation.py:550-577 — equal-or-subpath allowlist pre-check before self.home_root.mkdir | T4b (test_home_isolation_setup_rejects_non_allowlisted_home_root_before_mkdir in test_containment.py) + 14 updated tests across test_atomic_setup.py, test_symlink_attacks.py, test_hard_guard_real_home.py, test_path_containment.py | phase-outputs/test-results/04-h5b-pytest.txt | RESOLVED |
| __M1__ | `_default_output_dir()` CWD-binding | OQ-3 (DROPPED from scope) | (no source change) | (no test added) | Follow-Up Items entry; OQ-3 decision in phase-outputs/plans/01-oq-decisions.md | DEFERRED-SPEC §4 |
| __M2__ | _NullLifecycleExecutor active emits no WARNING | Step 3.5 | commands.py:1448 (call site) — `click.echo("eval run: WARNING: _NullLifecycleExecutor active...", err=True)` | T6 (test_run_emits_warning_when_null_lifecycle_executor_active in test_eval_run.py) | phase-outputs/test-results/03-m2-pytest.txt | RESOLVED |
| __M3__ | RunTotals keys hardcoded literals (drift from EVAL_STATUSES) | Step 3.4 | models.py adds SKIPPED_STATUSES/PASSED_STATUSES/FAILED_STATUSES constants; commands.py:_compute_run_stats uses them | (covered by full eval suite regression — no dedicated test) | phase-outputs/test-results/03-m3-pytest.txt | RESOLVED |
| __M4__ | Reporter and run_report writers diverge on summary.yaml | Step 4.2 | Promoted render_summary_yaml to run_report.py + shared `_write_artifact_set` helper; both writers delegate | (covered by updated test_writer_emits_markdown_json_and_yaml in test_run_report.py) | phase-outputs/test-results/04-m4-pytest.txt | RESOLVED |
| __M5__ | session_id ad-hoc construction at commands.py callsite | Step 5.5 | orchestrator.py adds `allocate_session_id(run_id, eval_id)`; commands.py:_run_one_spec takes run_id kwarg and calls helper | T7 (test_run_one_spec_uses_orchestrator_allocate_session_id + test_orchestrator_allocates_unique_session_id_per_run in test_orchestrator.py) | phase-outputs/test-results/05-m5-pytest.txt | RESOLVED |
| __M6__ | Click `Path` option asymmetry (eval doctor lacks file_okay=False) | Step 5.6 | commands.py:784 — added `file_okay=False` to eval doctor --output-dir option | (covered by full suite + eval doctor --help capture at phase-outputs/test-results/05-m6-doctor-help.txt) | phase-outputs/test-results/05-m6-doctor-help.txt + 05-m6-run-help.txt | RESOLVED |
| __CC1__ | EVAL_ID regex duplication between artifact_layout.py and loader.py | Step 5.1 (OQ-1 Rename + Promote + Import synthesis) | artifact_layout.py: `_EVAL_ID_RE` → `_EVAL_ID_PATH_SAFETY_PATTERN` + new public `EVAL_ID_PATTERN`; loader.py: `from .artifact_layout import EVAL_ID_PATTERN as EVAL_ID_REGEX` (alias) | T8 (test_eval_id_pattern_single_source in test_eval_id_regex.py) | phase-outputs/test-results/05-cc1-pytest.txt + 05-t8-pytest.txt + 06-grep-gates-final.txt GATE 3 (2 re.compile in artifact_layout, 0 in loader) | RESOLVED |
| __CC2__ | 11 sites of `*_EXIT_CODE: int = 2` declarations duplicating literal | Step 5.3 (OQ-2 — 4 canonical values + 11 re-exports via top-of-file import) | exit_codes.py NEW (SUCCESS=0/FAILURES=1/USAGE_ERROR=2/INTERRUPTED=3); 6 consumer files refactored to `from . import exit_codes as _exit_codes` + local `NAME: int = _exit_codes.VALUE` | T9 (test_no_magic_exit_code_literals_in_eval_module in test_exit_codes.py) | phase-outputs/test-results/05-cc2-pytest.txt + 05-t9-pytest.txt + 06-grep-gates-final.txt GATES 4 & 5 | RESOLVED |
| __CC3__ | _NullLifecycleExecutor observability gap | (folded into M2 per spec §5) | (see M2 row) | (see M2 row) | (see M2 row) | RESOLVED-VIA-M2 |
| __T1__ | compose_run_dir anchor test | Step 4.5 | (test addition only — no source) | test_run_anchors_output_via_compose_run_dir in test_eval_run.py | phase-outputs/test-results/04-pytest.txt | RESOLVED |
| __T2__ | _format_run_summary_line E/I/T parametrized | Step 4.6 | (test addition only) | test_format_run_summary_line_renders_errored_interrupted_timeout in test_run_summary.py | phase-outputs/test-results/04-pytest.txt | RESOLVED |
| __T3__ | corrupt settings.json fails closed | Step 2.1 | (test addition only) | test_coverage_gate_fails_on_corrupt_settings_json in test_coverage_gate.py | phase-outputs/test-results/03-h2-pytest.txt | RESOLVED |
| __T4a__ | commands.py allowlist-before-mkdir ordering | Step 4.7 | (test addition only) | test_eval_run_extends_allowlist_before_mkdir in test_home_isolation_extend.py | phase-outputs/test-results/04-pytest.txt | RESOLVED |
| __T4b__ | isolation.py containment pre-check before mkdir | Step 4.8 | (test addition only) | test_home_isolation_setup_rejects_non_allowlisted_home_root_before_mkdir in test_containment.py | phase-outputs/test-results/04-pytest.txt | RESOLVED |
| __T5__ | resolve_scratch_root rejects bare prefix (inverted) | Step 2.2 | (test inversion only) | test_resolve_scratch_root_rejects_bare_prefix in test_scratch_root_allowlist.py | phase-outputs/test-results/02-pytest-red-baseline.txt + 03-h4-pytest.txt | RESOLVED |
| __T5b__ | resolve_scratch_root accepts strict subdir | Step 2.2b | (test addition only) | test_accepts_immediate_subdir_of_allowlist_root in test_scratch_root_allowlist.py | phase-outputs/test-results/03-h4-pytest.txt | RESOLVED |
| __T6__ | NullLifecycleExecutor stderr WARNING | Step 2.3 | (test addition only) | test_run_emits_warning_when_null_lifecycle_executor_active in test_eval_run.py | phase-outputs/test-results/03-m2-pytest.txt | RESOLVED |
| __T7__ | session_id orchestrator ownership | Step 5.7 | (test addition only) | test_run_one_spec_uses_orchestrator_allocate_session_id in test_orchestrator.py | phase-outputs/test-results/05-m5-pytest.txt | RESOLVED |
| __T8__ | EVAL_ID_PATTERN single-source-of-truth | Step 5.2 | (test addition only) | test_eval_id_pattern_single_source in test_eval_id_regex.py | phase-outputs/test-results/05-t8-pytest.txt | RESOLVED |
| __T9__ | no magic exit codes outside exit_codes.py | Step 5.4 | (test addition only — plus docstring fix in commands.py:23) | test_no_magic_exit_code_literals_in_eval_module in test_exit_codes.py | phase-outputs/test-results/05-t9-pytest.txt | RESOLVED |

## Summary

- __Total findings tracked:__ 23 rows (5 High + 6 Medium + 3 CC + 9 Tests = 23; CC3 rolls into M2 per spec §5 but still gets a row pointing at M2's evidence).
- **Status breakdown:**
  - __RESOLVED:__ 22 (5 High + 5 Medium [M2-M6] + 2 CC [CC1+CC2] + 1 CC3-via-M2 + 9 Tests)
  - __DEFERRED-SPEC §4:__ 1 (M1 — see Follow-Up Items + OQ-3 decision)
- __Resolution rate:__ 22/23 (95.6%) RESOLVED; 1/23 (4.3%) deferred-with-rationale; 0 SKIPPED, 0 WONTFIX.
- __Test additions:__ 9 new test functions (T1-T9) + 1 collateral positive test (T5b) = 10 new tests.
- __New source files:__ 1 (`src/superclaude/cli/eval/exit_codes.py`).
- __Source files modified:__ 9 (commands.py, coverage.py, config.py, isolation.py, reporter.py, run_report.py, artifact_layout.py, loader.py, orchestrator.py, models.py, __init__.py — count includes models.py + __init__.py M3 re-exports).

## Phase Gate Verdicts

- __PG-1__ (Phase 2 test scaffolding QA): PASS at cycle 1 — see `phase-outputs/plans/PG-1-final-verdict.md`.
- __PG-2__ (Phase 4 layout + ordering QA): PASS at cycle 1 — see `phase-outputs/plans/PG-2-final-verdict.md`.
- __PG-FINAL__ (composite task-integrity): pending — Step PG-FINAL.2 spawns rf-qa with `fix_authorization: true`.

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

## OQ Decisions

# OQ Decisions — TASK-RF-20260522-153212

**Date recorded:** 2026-05-22
**Recorded during:** Step 1.5 (Phase 1, Preparation & Discovery)
**Authority:** User decisions made in the chat session that produced this task file (post adversarial-debate analysis). Resolutions are binding; later items follow these branches verbatim.

---

## OQ-1 — CC1 Regex Consolidation

**DECISION: Rename + Promote + Import (synthesis approach).**

### Verbatim resolution

1. In `src/superclaude/cli/eval/artifact_layout.py`: rename `_EVAL_ID_RE` → `_EVAL_ID_PATH_SAFETY_PATTERN`. Add docstring explaining "Path-safety regex — NOT the FR-SCH2 schema (see EVAL_ID_PATTERN below for that)."
2. In `artifact_layout.py`: __promote__ a new public `EVAL_ID_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$")` constant with docstring `"""FR-SCH2 schema contract — see schemas/suite.schema.json. Promoted from loader.py per CC1 to a single source of truth."""`.
3. In `loader.py`: REPLACE the local `re.compile(...)` definition with `from .artifact_layout import EVAL_ID_PATTERN as EVAL_ID_REGEX`. The `EVAL_ID_REGEX` alias remains in `loader.__all__` so `tests/cli/eval/test_eval_id_regex.py:32` (`from superclaude.cli.eval.loader import EVAL_ID_REGEX`) continues to resolve unchanged.

### Why this synthesis (not naive merge)

Defense-in-depth at regex boundaries is genuinely valuable. The two regexes enforce different invariants — path-safety vs FR-SCH2 schema. Naive consolidation would tighten path-safety (rejecting valid YAML) or loosen schema (letting path-traversal through). The "Rename + Promote + Import" approach eliminates the __schema regex duplication__ (which is the real CC1 finding) while preserving the __two-layer defense__ (which the Pragmatist correctly identified during adversarial debate).

### Affected items

- __Step 5.1__ (CC1 implementation): execute the 3-step rename/promote/import sequence
- __Step 5.2__ (T8 test): pins the SoT contract — `EVAL_ID_PATTERN is loader.EVAL_ID_REGEX` AND `_EVAL_ID_PATH_SAFETY_PATTERN is not EVAL_ID_PATTERN` + semantic-invariants check
- __Step 6.1 GATE 3 expectation__: TWO `re.compile()` entries in artifact_layout.py (path-safety + schema); ZERO in loader.py for eval-id patterns

---

## OQ-2 — CC2 Exit-Code Consolidation

**DECISION: 4 canonical values in new `exit_codes.py` + 11 module-level re-exports preserving descriptive names.**

### Verbatim resolution

1. __CREATE__ `src/superclaude/cli/eval/exit_codes.py` with exactly 4 canonical module-level constants:

   ```python
   """cliEval canonical exit codes (Click/POSIX/BSD sysexits hierarchy)."""
   SUCCESS: int = 0
   FAILURES: int = 1            # one or more eval failures
   USAGE_ERROR: int = 2         # operator misuse / config error (Click convention)
   INTERRUPTED: int = 130       # SIGINT / Ctrl-C (POSIX signal+128)
   ```

2. Each of the 11 `*_EXIT_CODE = 2` declarations becomes a single-line re-export preserving its descriptive name: `from .exit_codes import USAGE_ERROR as <NAME>_EXIT_CODE`. See Step 5.3 for the full 11-site enumeration.
3. Also re-export SUCCESS/FAILURES/INTERRUPTED for symmetry at the `RUN_CLEAN_EXIT_CODE` / `RUN_FAILURES_EXIT_CODE` / `RUN_INTERRUPTED_EXIT_CODE` sites in commands.py.

### Why 4 canonical values (not 11)

The 11 named constants happen to share the value `2` because they're all Click usage/operational errors. Consolidating to 4 canonical values makes future convention shifts (Click 9.0, BSD sysexits) a one-file change rather than an 11-site coordinated diff. The descriptive local names are preserved via re-export, so call-site readability is unchanged.

### Affected items

- __Step 5.3__ (CC2 implementation): create exit_codes.py with 4 values + edit 11 declaration sites into re-exports
- __Step 5.4__ (T9 test): pins the "no magic exit codes" contract — no literal `sys.exit(N)` calls anywhere; no `*_EXIT_CODE: int = <literal>` outside exit_codes.py; exit_codes.py contains exactly 4 canonical declarations
- __Step 6.1 GATE 5 expectation__: ZERO `*_EXIT_CODE = <literal-int>` declarations outside exit_codes.py

---

## OQ-3 — M1 Deferral

**DECISION: DROP M1 from scope per source spec §4 rationale. No HALT, no ⚪ Blocked state.**

### Verbatim resolution

M1 (`commands.py:1335-1343` — `_default_output_dir()` uses `Path.cwd()`) was classified by the source spec §4 as "flag for follow-up not bundled — existing tests depend on the relative behavior". The builder over-bundled M1 into Phase 5; that was a mistake. Implementation:

1. __Step 5.8 (M1 implementation) is DELETED.__ The Phase 5 sequence renumbers: former Step 5.9 (phase verification) becomes Step 5.8.
2. The Key Objective entry referencing M1 is rewritten to enumerate M2-M6 only.
3. __M1 moves to `### Follow-Up Items Identified`__ in the Task Log with: spec citation (§4), defect description (`_default_output_dir()` CWD-binding), and deferral rationale (no current invariant broken; H1 anchors layout invariant regardless of root choice; the "right" anchor — repo root vs `$XDG_DATA_HOME` vs cwd — needs an operator-experience decision not made here; trivial workaround via `--output-dir`).
4. The Phase 6 AC matrix records M1 as `DEFERRED-SPEC §4` with the same rationale.

### Why drop, not block

All three deferral conditions hold:

1. No current invariant is broken (H1 anchors layout regardless of root choice; FR-G4 preserved).
2. The "right" fix requires an unmade product decision (cwd vs repo-root vs `$XDG_DATA_HOME`).
3. The workaround is trivial (one `--output-dir` flag).

Deferring is correctly scoped engineering, not technical debt accumulation. The qualitative QA's defensive HALT-state default was reasonable as a safety measure but is not the right response now that the user has explicitly resolved the question.

### Affected items

- __Phase 5 enumeration__: phase description, Key Objective #5 — both rewritten to exclude M1
- __Step 5.8__ (formerly the M1-HALT item): DELETED; former Step 5.9 verification renumbered to 5.8
- __Step 6.4 AC matrix__: M1 row carries `DEFERRED-SPEC §4` status with rationale + reference to Follow-Up Items
- __Follow-Up Items__: M1 entry includes spec §4 quote + recommended next-step (separate task pinning the anchor choice)

---

## Resolution authority

All three resolutions were chosen by the user after I (the agent) presented adversarial-debate analyses comparing the alternatives. The deliberation is preserved in the chat transcript that produced this task file. If during execution any evidence contradicts a resolution (e.g. an import error during the OQ-1 Rename step), the executor MUST STOP and surface the conflict in `### Phase 1 Findings` rather than silently switching branches.

## Per-gate verdicts

# PG-1 Final Verdict

**Gate:** PG-1 (test scaffolding correctness)
**Date:** 2026-05-22
**Cycle:** 1 (PASS on first attempt; no fix cycles needed)
**Verdict:** PASS

PG-1 PASS at cycle 1 — proceed to Phase 3.

## Per-test verdict

| Test | Result |
|------|--------|
| T3 `test_coverage_gate_fails_on_corrupt_settings_json` (FR-G5/H2) | PASS |
| T5 inverted `test_resolve_scratch_root_rejects_bare_prefix` (H4) | PASS |
| T5b `test_accepts_immediate_subdir_of_allowlist_root` (H4 acceptance #2) | PASS |
| T6 `test_run_emits_warning_when_null_lifecycle_executor_active` (M2) | PASS |

## Acceptance criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Each Phase 2 test pins the RIGHT invariant | PASS |
| 2 | Each Phase 2 test FAILS today for the RIGHT reason | PASS (RED baseline confirmed: `assert True is False`, `DID NOT RAISE`, empty stderr) |
| 3 | No surface-area drift outside the 3 expected test files | PASS (literal git diff has 2 pre-Phase-2 cosmetic doc hits; spec intent satisfied) |
| 4 | Phase 2 Findings document pre-existing issues honestly | PASS |

## Non-blocking issues

- __IMPORTANT (NOTE):__ Criterion 3's literal `git diff` returns 2 hits from pre-Phase-2 cosmetic doc edits (`pty/PROVENANCE.md`, `suites/README.md`); future PG prompts should scope diff to `**/*.py`.
- __MINOR:__ `02-pytest-red-baseline.txt` EXIT_CODE=0 false-clean from tee-pipe shell idiom; remediation is `set -o pipefail` / `${PIPESTATUS[0]}` (already logged in Phase 2 Findings).

## Retry Monotonicity Protocol

- Cycle 1 PASS — neither regression check nor monotonicity guard fires (both inactive on single-cycle PASS by construction).
- F_n history reset for PG-2 (per "per-gate counters are INDEPENDENT" rule).

## Authoritative report

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260522-153212/phase-outputs/reviews/PG-1-rf-qa-report.md`

## Next phase

**Phase 3 (Correctness + Observability)** — H4, H2, H3 + M3, M2 source fixes that turn Phase 2's RED tests GREEN.

**SESSION BOUNDARY:** Per user's scope decision at the start of `/task` invocation, execution halts here. Phase 3 resumes in a fresh session via `/task .dev/tasks/to-do/TASK-RF-20260522-153212/TASK-RF-20260522-153212.md`.
PG-2 PASS at cycle 1 — proceed to Phase 5
