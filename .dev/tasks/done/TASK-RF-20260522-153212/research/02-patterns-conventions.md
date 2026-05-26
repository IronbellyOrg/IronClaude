# R2: Patterns & Conventions — cliEval Test Suite

**Task**: TASK-RF-20260522-153212
**Researcher**: R2 (Patterns)
**Scope**: tests/cli/eval/ + src/superclaude/cli/eval/commands.py helpers
**Status**: In Progress

## Purpose

Extract the EXACT idioms the task-builder must encode into checklist
items for T1-T9 (tests) and H1-H5 / M1-M6 / CC1-CC2 (source edits) so
that emitted tests and patches mirror existing house style and pass
review on first build.

---

## A) Fixture conventions

### A.1 temp output / scratch directories

Three distinct idioms in the suite — each test must pick the right one
based on whether it touches `eval_run`'s scratch-root policy or only
pure helpers.

| Idiom | Use when | Example file:line |
|---|---|---|
| `tmp_path: Path` (pytest built-in) | unit-level helpers, no Click run | `tests/cli/eval/test_coverage_gate.py:150` (`test_coverage_gate_passes_when_settings_missing`) |
| `allowlisted_output_dir: Path` (conftest) | `CliRunner` calls passing `--output-dir` | `tests/cli/eval/test_eval_run.py:223` (`test_parallel_zero_clamps_to_one`) + `tests/cli/eval/conftest.py:24-39` |
| local `scratch_root` fixture nested under `tmp_path` | HomeIsolation unit tests, EvalConfig allowlist seeded explicitly | `tests/cli/eval/test_home_isolation.py:62-68`, `tests/cli/eval/test_eval_lifecycle.py:131-135` |

The conftest `allowlisted_output_dir` fixture mints
`/tmp/eval-runs/pytest-<12hex>/` (tests/cli/eval/conftest.py:34) and
best-effort-removes it; the docstring explicitly warns NOT to use
`tmp_path` for `--output-dir` because pytest's tmp lands under
`/tmp/pytest-of-<user>/` which is OUTSIDE the AC12 allowlist
(tests/cli/eval/conftest.py:7-13).

**Rule for T1-T9 emission**: any new test that calls
`runner.invoke(eval_group, ["run", ...])` with `--output-dir` MUST
declare `allowlisted_output_dir: Path` as a parameter. Tests that only
call `coverage_gate(...)` directly or stub a settings.json on disk use
`tmp_path` alone.

### A.2 corrupt / malformed settings.json construction

Today only ONE test constructs malformed settings.json content:
`test_coverage_gate_passes_when_settings_unreadable_json` at
`tests/cli/eval/test_coverage_gate.py:160-165`. It writes the literal
string `"{not json"` via `bad.write_text("{not json", encoding="utf-8")`.
The current contract treats malformed JSON as the empty matcher set,
so the gate returns `passed=True`.

**Spec intent for T1 (`test_coverage_gate_fails_on_corrupt_settings_json`)**:
the new test must FLIP this — corrupt JSON should be a HARD failure,
not silently equivalent to an empty matcher set. Builder must:

1. Use `tmp_path / "settings.json"` (pure helper, no CliRunner).
2. Write malformed JSON exactly the way the existing test does:
   `settings.write_text("{not json", encoding="utf-8")`.
3. Assert `coverage_gate(...).passed is False` rather than `True`.

Idiom for well-formed settings JSON (compare): `settings.write_text(json.dumps({"hooks": {"PreToolUse": [{"matcher": "..."}]}}), encoding="utf-8")` — see `tests/cli/eval/test_coverage_gate.py:172-185`.

### A.3 mocking allowlist / scratch_root / claude_home machinery

Two helpers reused across multiple test files:

**`clean_host` fixture (3 distinct definitions, identical body)**:

- `tests/cli/eval/test_coverage_gate.py:325-345`
- `tests/cli/eval/test_coverage_gate_integration.py:66-89`
- `tests/cli/eval/test_scratch_root_policy.py:122-143`

Pattern (verbatim from coverage_gate_integration.py:66-89):

```python
@pytest.fixture
def clean_host(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    claude_home = tmp_path / ".claude"
    claude_home.mkdir()
    def fake_which(name: str) -> str:
        return f"/usr/bin/{name}"
    monkeypatch.setattr(shutil, "which", fake_which)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        commands_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.1",
    )
    return {"home": tmp_path, "claude_home": claude_home}
```

**`clean_claude_home` fixture (lighter — only monkeypatches `Path.home`)**:

- `tests/cli/eval/test_eval_run.py:94-106` — used when only the
  coverage gate's settings.json read needs to be silenced (does not
  patch `shutil.which`).

**Allowlist mocking** for `resolve_scratch_root`:
The function reads `EvalConfig.allowed_scratch_roots`, so tests narrow
the allowlist by constructing a fresh `EvalConfig(allowed_scratch_roots=(...))`
— see `tests/cli/eval/test_scratch_root_allowlist.py:140-141`. There is
NO `monkeypatch.setattr(commands_module, "..._allowlist", ...)` pattern;
the config is passed positionally.

**Rule for T8 (`test_resolve_scratch_root_rejects_bare_prefix`)**:

- Use plain `pytest.raises(ScratchRootViolation)` with no fixtures.
- Construct narrow `EvalConfig(allowed_scratch_roots=(...))` if the
  test wants to pin behaviour against a non-default allowlist.

### A.4 status taxonomy parameterisation

The `EVAL_STATUSES` SoT lives in `superclaude.cli.eval.models` (see
commands.py:1501-1502). Tests parameterise over status strings two ways:

1. **String literals in `@pytest.mark.parametrize`** — used in
   `tests/cli/eval/test_eval_lifecycle.py:659-660`:

   ```python
   @pytest.mark.parametrize(
       "exc_type", [KeyboardInterrupt, SystemExit], ids=["sigint", "sysexit"]
   )
   ```

2. **Direct assertion on per-status branches** — used in
   `test_eval_lifecycle.py:285-291` (`test_run_eval_executes_all_seven_steps_in_order`)
   asserts `outcome.status == "PASS"` (literal string).

For T2 (`test_format_run_summary_line_renders_errored_interrupted_timeout`):

- The current `_format_run_summary_line` (commands.py:1526-1539) only
  renders P/F/S — it does NOT render ERRORED / INTERRUPTED / TIMEOUT.
- New test must parameterise across all DM-012 status strings:
  `["PASS", "FAIL", "SKIPPED", "ERRORED", "INTERRUPTED", "TIMEOUT", "XFAIL", "XPASS"]`.
- Builder idiom: construct a `RunSummary` with controlled `RunTotals`
  values and assert the formatted line contains the expected status
  buckets. Cite the SoT: `EVAL_STATUSES` in `superclaude.cli.eval.models`.

---

## B) Assertion idioms

### B.1 Style: `assert` vs `pytest.raises` vs `pytest.warns`

- **Bare `assert`**: default for happy-path / value comparisons —
  e.g. `tests/cli/eval/test_coverage_gate.py:156` `assert result.passed is True`.
- **`pytest.raises`**: every failure path — uses `with pytest.raises(InvalidEvalId):`
  (`tests/cli/eval/test_eval_id_regex.py:103-104`) and the
  `as excinfo` form when the exception attributes are asserted
  (`tests/cli/eval/test_eval_id_regex.py:184-190`).
- **`pytest.warns`**: NOT seen anywhere in the cliEval test scope.
  Logging-side warnings are asserted via stderr/stdout content checks
  (see C.2 below), not `pytest.warns`. M2's "WARNING" emission must
  follow this convention, not `pytest.warns`.

### B.2 `CoverageResult.passed` assertion style

Three patterns observed:

1. `assert result.passed is True` — `test_coverage_gate.py:156`
2. `assert result.passed is False` — `test_coverage_gate.py:219`
3. `assert result.passed is True` after constructing via kwargs only:
   `CoverageResult(matchers=(...), covered=(...))` (no positional args)
   — `test_coverage_gate.py:411-416`.

`.passed` is read as a property (no parens), never `passed()`.
NEVER use `assert result.passed` (truthy form) — always pin `is True` /
`is False` (per `test_coverage_gate.py:156, 192, 219, 272, 298, 310`).

### B.3 Click exit code assertion

Universal idiom: name a symbolic constant and assert `result.exit_code`
matches it.

```python
assert result.exit_code == COVERAGE_GATE_FAILED_EXIT_CODE
assert result.exit_code == RUN_CLEAN_EXIT_CODE, result.output + (result.stderr or "")
assert result.exit_code == HARD_FAIL_EXIT_CODE
```

References:

- `test_coverage_gate.py:375`, `:394`, `:407`
- `test_eval_run.py:230-232`, `:275`, `:301`, `:359`, `:383`, `:406`
- `test_coverage_gate_integration.py:165`, `:189`, `:223`, `:267`

The diagnostic `result.output + (result.stderr or "")` is the canonical
hint string when the assertion fails (per `test_eval_run.py:230-232`).

Bare numeric literals (`assert result.exit_code == 2`) appear ONLY at
the contract-pinning surface where the spec value is explicitly being
tested — e.g. `test_coverage_gate.py:408` (`assert COVERAGE_GATE_FAILED_EXIT_CODE == 2`).

### B.4 file artifact existence

Two equivalent idioms:

- `(output_dir / "summary.md").is_file()` — `test_eval_run.py:449`
- `artifact_path.is_file()` — `test_coverage_gate_integration.py:307`

`.is_file()` is preferred over `.exists()` whenever the artifact is a
file (not a dir). Directories use `.is_dir()` — e.g.
`paths.eval_dir.is_dir()` (`test_artifact_layout.py:192`).

`Path.exists()` appears for negative assertions (`assert not home.exists()`,
`test_home_isolation.py:241`) and post-teardown checks.

The on-failure diagnostic for missing artifacts is to dump `iterdir()`
output — `test_coverage_gate_integration.py:307-310`:

```python
assert artifact_path.is_file(), (
    f"expected artifact {artifact_path} not found; "
    f"output_dir contents = {sorted(p.name for p in output_dir.iterdir())}"
)
```

---

## C) Click integration test idioms (post-08183738 / mix_stderr)

### C.1 CliRunner construction

Universal: `runner = CliRunner()` — zero-arg constructor. Seen at every
invocation site (e.g. `test_coverage_gate.py:352`, `:371`, `:390`;
`test_eval_run.py:117`, `:202`, `:259`; `test_coverage_gate_integration.py:112`).
NO `CliRunner(mix_stderr=False)` anywhere — Click 8.3.2 dropped that
kwarg and the project has migrated (per commit 08183738).

### C.2 stdout vs stderr surfaces

Tests treat the two streams as **separately addressable**:

- `result.stdout` for JSON payloads / summary text
  (`test_coverage_gate.py:395`, `test_eval_run.py:485`, `:517`).
- `result.stderr` for failure diagnostics / WARNING / banner text
  (`test_coverage_gate.py:376-377`, `test_eval_run.py:276`, `:330`,
  `:363`, `:384`, `:407`).
- `result.output` is used as an alias for stdout in older tests AND
  as the fallback "give me everything" surface in failure diagnostics:
  `result.output + (result.stderr or "")` (e.g. `test_eval_run.py:230-232`,
  `:447`, `:579-580`; `test_coverage_gate_integration.py:123`, `:268-269`).

The `or ""` guard around `result.stderr` is canonical because Click's
default `result.stderr` is `""` when nothing was emitted; the
diagnostic string handles both empty and None gracefully.

`result.stderr` is sometimes consumed verbatim with `.split()` and
`.lower()` — `test_eval_run.py:363` (`"scratch-root" in result.stderr.lower()`)
and `test_coverage_gate_integration.py:194-196` (split on
`"uncovered matcher patterns:"`).

### C.3 Implications for H5 / M2 / CC1 tests

- **H5 / CC2 stderr-only assertions**: emit content via `click.echo(..., err=True)`
  (see commands.py:870, 873, 912, 916, 1732, 1760, 1767, 1800, 1888).
  Then assert with `result.stderr`.
- **M2 "_NullLifecycleExecutor active" WARNING**: belongs on stderr
  via `click.echo(..., err=True)` — matches every other warning in
  commands.py (e.g. NFR-PERF2 warning at commands.py:906-908 routes via
  err=True). The single existing exception is the NFR-PERF2 doctor
  warning at commands.py:906 which uses `err=False` — but the M2 spec
  intent is to surface this to operators on stderr so CI logs can grep
  for it without `--json` parsing. See D.2 below for confirmation.

---

## D) Logging / observability conventions in commands.py

### D.1 No `logging.getLogger(__name__)` anywhere

Confirmed via grep (file: `src/superclaude/cli/eval/commands.py`).
The module imports `import logging` is ABSENT — the entire user-facing
observability surface uses `click.echo(..., err=True/False)`. There is
no `_logger = logging.getLogger(__name__)` module-level handle. New
WARNING / INFO emissions for M2 MUST follow `click.echo` style.

### D.2 Where does the M2 WARNING belong?

Evidence: every operator-facing non-fatal notice in commands.py uses
`click.echo(..., err=True)`:

- `commands.py:870` exception passthrough: `click.echo(f"eval doctor: ...", err=True)`
- `commands.py:906-911` NFR-PERF2 warning (special case — see below):

  ```python
  click.echo(
      f"eval doctor: NFR-PERF2 warning: {ram_row.detail}",
      err=False,  # NOTE: this one warning is err=False because it appears under --json
  )
  ```

- `commands.py:912` `click.echo(render_hard_failure_artifact(report), err=True)`
- `commands.py:916` `click.echo(_format_coverage_missing_roster(coverage_result), err=True)`
- `commands.py:1732` scratch-root violation: `click.echo(format_scratch_root_violation(exc), err=True)`
- `commands.py:1760, 1767` exception passthrough: `click.echo(f"eval run: {type(exc).__name__}: {exc}", err=True)`
- `commands.py:1800` coverage missing roster: `click.echo(_format_coverage_missing_roster(coverage), err=True)`
- `commands.py:1888` orchestrator rejection: `click.echo(f"eval run: orchestrator rejected request: {exc}", err=True)`
- `commands.py:1942` retention advice: `click.echo(DISK_BUDGET_RETENTION_ADVICE, err=True)`

The dominant pattern (8 of 9 sites) is `err=True`. The M2 WARNING for
`_NullLifecycleExecutor active` SHOULD route via `err=True` so operator
CI logs surface it without `--json` parsing and so the JSON stdout
payload remains machine-clean.

**Format convention**: every WARNING starts with the command name
prefix — `eval doctor:`, `eval run:` (see commands.py:870, 873, 906,
870 etc.). The M2 WARNING should follow: `eval run: WARNING: ...`.

### D.3 Level vocabulary

There is no formal `WARNING / INFO / ERROR` level taxonomy — the
module's style is to use plain-prose prefixes:

- `eval doctor: NFR-PERF2 warning: ...` (commands.py:907)
- `eval run: orchestrator rejected request: ...` (commands.py:1888)
- `eval doctor: <ExcType>: <msg>` (commands.py:870)
- `eval run: <ExcType>: <msg>` (commands.py:1760)

No tests assert level keywords (e.g. `"WARNING"` substring). They
assert specific stderr content tokens (e.g. `"NFR-PERF2"`,
`"--timeout-mult must be > 0"`).

For M2, builder should pick a recognisable token (e.g. `"NullLifecycleExecutor"`
or `"non-production executor"`) and have the test assert that exact
substring.

---

## E) Test naming conventions

### E.1 Style audit

Existing test names are **long, snake_case, intent-revealing**, and
follow the shape: `test_<subject>_<verb-phrase>_<outcome>`.

Examples (file:line):

- `test_coverage_gate_passes_when_settings_missing` — coverage_gate.py:150
- `test_coverage_gate_fails_and_writes_artifact_for_uncovered_pattern` — :199
- `test_coverage_gate_fails_when_fourth_matcher_added_without_eval` — :231
- `test_doctor_check_coverage_passes_when_suite_covers_all_matchers` — coverage_gate_integration.py:104
- `test_doctor_check_coverage_stderr_names_uncovered_pattern` — :169
- `test_run_exits_2_when_settings_has_uncovered_matcher` — :243
- `test_run_writes_coverage_missing_artifact_under_output_dir` — :274
- `test_parallel_zero_clamps_to_one` — test_eval_run.py:219
- `test_output_dir_outside_allowlist_exits_scratch_root_violation` — :333
- `test_validate_eval_id_rejects_traversal_and_separator_patterns` — test_eval_id_regex.py:100
- `test_run_eval_executes_all_seven_steps_in_order` — test_eval_lifecycle.py:263
- `test_run_eval_teardown_keep_true_on_errored` — :539

Average length is 40-70 chars; longest observed is 70 chars
(`test_doctor_output_dir_violation_takes_precedence_over_hard_check`,
test_scratch_root_policy.py:185).

**The spec-proposed names match this style exactly**:

- `test_coverage_gate_fails_on_corrupt_settings_json` — fits (52 chars).
- `test_format_run_summary_line_renders_errored_interrupted_timeout` — fits (63 chars).
- `test_resolve_scratch_root_rejects_bare_prefix` — fits (45 chars).

No adjustments needed for naming.

### E.2 Per-T# recommended target file

Based on existing co-location patterns (subject of test → file owning
that surface):

| T# | Spec name | Target file | Rationale |
|---|---|---|---|
| T1 | `test_coverage_gate_fails_on_corrupt_settings_json` | `tests/cli/eval/test_coverage_gate.py` | All `coverage_gate(...)` unit tests live here (see coverage_gate.py:150-298 block) |
| T2 | `test_format_run_summary_line_renders_*` | `tests/cli/eval/test_run_summary.py` (existing file) OR `tests/cli/eval/test_eval_run.py` | `_format_run_summary_line` is currently only indirectly tested via `test_run_verbose_emits_summary_line` (eval_run.py:490); `test_run_summary.py` exists in the suite per the ls listing. **Recommend: `test_run_summary.py`** for the unit-level renderer assertions. |
| T8 | `test_resolve_scratch_root_rejects_bare_prefix` | `tests/cli/eval/test_scratch_root_allowlist.py` | All `resolve_scratch_root` tests live here (see allowlist.py:35-198) |

(T3-T7, T9 names not provided in this researcher's brief — R1 should
fill in their file targets via the same rule: search for the function/symbol
the test asserts on, locate the test file that owns it, append there.)

### E.3 Test file headers

Every cliEval test file opens with:

1. Module docstring naming the AC bullet / task / deliverable —
   e.g. `"""FR-G5 hook-matcher coverage gate tests (T04.14 / D-0075 / R-075)."""`
   (test_coverage_gate.py:1-8).
2. `from __future__ import annotations` (universal — every file).
3. Stdlib imports, then third-party (`pytest`, `click.testing.CliRunner`),
   then `superclaude.cli.eval.*` (commands.py:11-32 of coverage_gate.py
   exemplifies; eval_lifecycle.py:27-46 too).
4. Section headers as comment banners: `# --- helpers ---` or
   `# ---------------------------------------------------------------------------`
   (test_coverage_gate.py:35-37, 75-77, 110-112, 145-147, 320-322;
    test_eval_lifecycle.py:49, 95, 125, 167, 213, 255 etc.)

**New tests appended to existing files MUST add a section banner if the
test belongs to a new logical group.** Tests added to an existing group
just slot under that group's banner.

---

## F) Test order conventions

### F.1 Order = logical grouping, NOT bottom-append

Every file is organised by **AC-bullet groups** separated by banner
comments. Examples:

- `test_coverage_gate.py` groups (file:line):
  - "Helpers — pattern sanitisation + default matcher filter" (35-37)
  - "extract_hook_matchers" (75-77)
  - "eval_covers_pattern" (110-112)
  - "coverage_gate — end-to-end behaviours" (145-147)
  - "CLI wiring — doctor --check-coverage" (320-322)
  - "Module surface contracts" (401-403)

- `test_eval_run.py` groups:
  - "AC bullet 1 — `superclaude eval run --help` lists all 12 flags" (109-111)
  - "AC bullet 2 — per-flag validation" (136-138)
  - "AC bullet 3 — one-eval end-to-end run" (410-412)
  - "AC bullet 4 — spec.md documents the flag wiring" (591-593)

**Rule for T1-T9 placement**: locate the section banner whose subject
matches the new test's surface, then append the test as the LAST item
under that banner. Do NOT append at file bottom unconditionally.

For T1: append under "coverage_gate — end-to-end behaviours"
(test_coverage_gate.py:145-147) after the
`test_coverage_gate_to_dict_serialises_full_result` test (line 301-317)
since that's the last end-to-end behaviour test.

For T8: append at the end of the "negative" / non-allowlisted block
in `test_scratch_root_allowlist.py:89-115` (after
`test_violation_message_includes_offending_path` at line 118-126).
Builder should add a new banner if T8 introduces a new logical group
(e.g. "bare-prefix rejection").

### F.2 Pytest markers

**No `@pytest.mark.integration` / `@pytest.mark.unit` markers are used
in any cliEval test file.** Greppable evidence:

- test_eval_run.py: only `@pytest.fixture` decorators.
- test_coverage_gate.py: only `@pytest.fixture`.
- test_eval_lifecycle.py: only `@pytest.fixture` + one
  `@pytest.mark.parametrize` at line 659.
- test_artifact_layout.py, test_config.py, test_exit_codes.py: no
  markers other than `pytest.fixture` and `pytest.mark.parametrize`.

The `pytest_plugin.py` auto-markers (`/unit/` → `@pytest.mark.unit`,
`/integration/` → `@pytest.mark.integration`) DO NOT apply to
`tests/cli/eval/` files because they're not under those subdirectories.

**Rule for T1-T9 emission**: NO custom markers (`@pytest.mark.confidence_check`,
`@pytest.mark.integration`, etc.) should be added to the new tests
unless the spec explicitly calls them out. Use bare `def test_...`.

### F.3 `pytest.mark.parametrize` idiom

When used (test_eval_id_regex.py:51-67, :79-98, :113-122, :130-141,
:148-160, :170; test_eval_lifecycle.py:659-660):

- Always uses `@pytest.mark.parametrize` with a single param-name
  string and a list of values.
- `ids=[...]` is used when values would otherwise stringify ambiguously
  (e.g. `ids=["sigint", "sysexit"]` at lifecycle.py:660).
- Values are simple Python literals — strings, ints, exception classes.
- No `indirect=True` fixtures, no `param.id` factories.

For T2 (`test_format_run_summary_line_renders_errored_interrupted_timeout`):

- Recommend parametrize over status taxonomy:

  ```python
  @pytest.mark.parametrize(
      "status,bucket",
      [
          ("ERRORED", "errored"),
          ("INTERRUPTED", "interrupted"),
          ("TIMEOUT", "timeout"),
      ],
  )
  ```

- Matches the lifecycle.py:659-660 shape exactly.

---

## Per-T# Final Recommendations (Builder Cheatsheet)

| T# | Target file | Banner section | Fixture | Assert style |
|---|---|---|---|---|
| T1 `corrupt settings.json` | `tests/cli/eval/test_coverage_gate.py` | "coverage_gate — end-to-end behaviours" (after line 317) | `tmp_path` only | `assert result.passed is False` |
| T2 `format_run_summary_line ERRORED/INTERRUPTED/TIMEOUT` | `tests/cli/eval/test_run_summary.py` (existing file per ls output) — verify file owns `_format_run_summary_line` tests | new section "format_run_summary_line renderer" | none (pure function — construct RunSummary inline) | parametrize over status; assert substring in `_format_run_summary_line(...)` output |
| T8 `resolve_scratch_root bare-prefix` | `tests/cli/eval/test_scratch_root_allowlist.py` | after "negative: non-allowlisted prefixes are rejected" (line 89-115) | none | `with pytest.raises(ScratchRootViolation):` |
| T3-T7, T9 | (not specified in this brief — R1 owns file inventory; this researcher recommends `test_eval_run.py` for CLI-flag tests, `test_coverage_gate_integration.py` for end-to-end gate tests, `test_eval_lifecycle.py` for runner status mapping) | per-test banner match | per-test (allowlisted_output_dir if `eval run`, else tmp_path) | per-test (CliRunner exit_code pin for CLI tests; bare assert for unit tests) |

---

## Source-Edit Item Patterns (H1-H5, M1-M6, CC1-CC2)

### H5 / M2 — stderr emission for new WARNING

Use `click.echo("eval run: WARNING: <reason>", err=True)` — matches
commands.py:1760, 1767, 1888 pattern exactly. The WARNING token
chosen should be a stable substring tests can grep (e.g. "NullLifecycleExecutor"
or "non-production executor active").

### CC1 / CC2 — exit-code constants

Every exit-code constant follows the pattern `<SCREAMING_SNAKE>_EXIT_CODE = <int>`
defined as a module-level int in `superclaude.cli.eval.commands` and
re-exported from `superclaude.cli.eval/__init__.py`.

Test-side pin: `assert <CONSTANT>_EXIT_CODE == <value>` (see
test_coverage_gate.py:408 and test_eval_id_regex.py:194-196).

### H1-H4, M1, M3-M6 — defer to R1/R3 inventory

This researcher's brief is patterns, not per-symbol line numbers. R1
should pin the surgical file:line targets; R3 should pin the call
graphs. The conventions documented above (stderr routing, exit-code
constant pattern, click.echo formatting) apply universally to every
helper edit.

---

## Status: Complete

Researcher: R2 (Patterns)
Completed: 2026-05-22
Files cited: conftest.py, test_coverage_gate.py,
test_coverage_gate_integration.py, test_eval_run.py,
test_home_isolation.py, test_eval_lifecycle.py, test_config.py,
test_artifact_layout.py, test_eval_id_regex.py, test_exit_codes.py,
test_scratch_root_policy.py, test_scratch_root_allowlist.py,
commands.py.

Key takeaway: the cliEval test suite has a strongly enforced house
style — long intent-revealing names, banner-grouped sections, zero
custom markers, universal `click.echo(..., err=True)` for warnings,
exit-code constants pinned by symbolic name. T1-T9 emission should
mirror these patterns exactly. No surprises in fixture choice: the
two key signals are (1) does the test call `eval run` via CliRunner
(→ `allowlisted_output_dir`), and (2) does it touch the doctor /
settings.json read (→ `clean_host` or `clean_claude_home`).
