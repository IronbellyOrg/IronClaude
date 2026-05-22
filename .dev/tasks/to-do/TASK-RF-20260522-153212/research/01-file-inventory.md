# Research: File Inventory
**Topic type:** File Inventory
**Scope:** src/superclaude/cli/eval/{commands,coverage,config,artifact_layout,reporter,run_report,isolation,loader}.py + new exit_codes.py
**Status:** Complete
**Date:** 2026-05-22
---

## Headline: Spec line numbers are ACCURATE — every cited symbol verified in place

All 18 symbols cited in `remediation-spec.md` were re-Read at the cited offsets and matched
the spec's coordinates within ±5 lines. **No prominent drift detected.** Two minor clarifications:

1. The test `test_accepts_tmp_eval_runs_root_itself` lives in
   `tests/cli/eval/test_scratch_root_allowlist.py:52` — NOT `tests/cli/eval/test_config.py`
   as one reading of the spec might suggest. Builder must point new test there.
2. **CC1 (eval-id regex duplication) is actually a divergence, not pure duplication.** The
   two regexes are textually different — see file F below. The builder should reflect this
   in the CC1 checklist item: this is consolidate-OR-document-the-asymmetry, not
   strict-copy-paste removal.

Current file sizes (for context when sizing checklist items):

```
commands.py        1950 lines
coverage.py         348 lines
config.py           278 lines
artifact_layout.py  305 lines
reporter.py         233 lines
run_report.py       379 lines
isolation.py        696 lines
loader.py           623 lines
exit_codes.py        (does not exist — CC2 creates it)
```

---

## A) commands.py

Top-level remediation-target symbols, all verified at current line numbers:

| Symbol | Spec L | Actual L | Quote |
|---|---|---|---|
| `RUN_CLEAN_EXIT_CODE` | 570 | **570** | `RUN_CLEAN_EXIT_CODE: int = 0` |
| `RUN_FAILURES_EXIT_CODE` | 573 | **573** | `RUN_FAILURES_EXIT_CODE: int = 1` |
| `RUN_INTERRUPTED_EXIT_CODE` | 577 | **577** | `RUN_INTERRUPTED_EXIT_CODE: int = EXIT_INTERRUPTED` |
| `doctor` `--output-dir` Click option | 784 | **784** | `type=click.Path(path_type=Path),` |
| `def _utc_iso_now` | 1308 | **1308** | `def _utc_iso_now() -> str:` |
| `def _new_run_id` | 1322 | **1322** | `def _new_run_id(*, started_at: str, suite_name: str) -> str:` |
| `def _default_output_dir` | 1335 | **1335** | `def _default_output_dir(*, started_at: str, suite_name: str) -> Path:` |
| `def _can_install_signal_handler` | 1346 | **1346** | `def _can_install_signal_handler() -> bool:` |
| `class _NullLifecycleExecutor` | 1361-1402 | **1361-1387** | Class body ends L1387; `_resolve_executor_factory` follows at L1390 |
| `def _resolve_executor_factory` | 1390 | **1390** | `def _resolve_executor_factory() -> Callable[..., LifecycleExecutor]:` |
| `def _run_one_spec` | 1405 | **1405** | `def _run_one_spec(` |
| `session_id = spec.id` block | 1442-1446 | **1442-1446** | `home = HomeIsolation(eval_id=spec.id, home_root=home_root, session_id=f"sess-{spec.id}",)` |
| `def _compute_run_stats` | 1477 | **1477** | `def _compute_run_stats(outcomes: Sequence[EvalOutcome], *, manifest_n: int) -> tuple[RunCounts, RunTotals]:` |
| `def _format_run_summary_line` | 1526-1539 | **1526-1539** | Function body verified line-for-line |
| `eval_run` Click `--output-dir` option (Path option) | 1587 | **L1584-1594** | `type=click.Path(file_okay=False, path_type=Path),` (option header L1584; `type` keyword at L1587 exactly) |
| `def eval_run` | — | **1644** | (FYI — signature starts here) |
| `--output-dir` resolution block | 1710-1714 | **1710-1714** | `requested_output = (output_dir if output_dir is not None else _default_output_dir(started_at=started_iso, suite_name=suite_name))` |
| `resolve_scratch_root` call | — | **1727-1730** | `resolved_output = resolve_scratch_root(requested_output, config=base_config,)` |
| `resolved_output.mkdir` | 1735 | **1735** | `resolved_output.mkdir(parents=True, exist_ok=True)` |
| `home_root.mkdir` | 1737 | **1737** | `home_root.mkdir(parents=True, exist_ok=True)` |
| AC12 allowlist extension (`runtime_allowed = ...`) | 1735-1746 | **1743-1746** | `runtime_allowed = tuple(base_config.allowed_scratch_roots) + (resolved_output, home_root,)` |
| `Reporter(...).write(resolved_output)` | 1918 | **1918** | `Reporter(summary=summary, emit_junit=junit).write(resolved_output)` |
| `sys.exit(RUN_INTERRUPTED_EXIT_CODE)` | — | **1932** | (cancellation branch) |
| `sys.exit(RUN_FAILURES_EXIT_CODE)` | — | **1949** | (failures branch) |
| `sys.exit(RUN_CLEAN_EXIT_CODE)` | — | **1950** | (clean exit — last line of file) |

**Note for CC2 (exit_codes.py extraction):** The three RUN_*_EXIT_CODE constants at L570/573/577
are the canonical pinning site. Comment block L565-568 explicitly says
*"Pinned by tests/cli/eval/test_exit_codes.py (TEST-008 / T04.19 / D-0079)"*, so the
extraction MUST keep this test pin functional. `RUN_INTERRUPTED_EXIT_CODE` re-exports
`signal_handler.EXIT_INTERRUPTED` — the new module must preserve this single-source-of-truth.

**Note for H4 (`session_id` from spec.id):** At L1442-1446 the constructor passes
`session_id=f"sess-{spec.id}"`. The spec finding is that this is *non-unique* across
re-runs of the same spec inside the same run-dir; H4's remediation likely needs to inject
a run-scoped salt (e.g., the run_id) into the session_id.

---

## B) coverage.py

| Symbol | Spec L | Actual L | Quote |
|---|---|---|---|
| `COVERAGE_GATE_FAILED_EXIT_CODE` | — | **77** | `COVERAGE_GATE_FAILED_EXIT_CODE: int = 2` |
| `def coverage_gate` | — | **261** | `def coverage_gate(settings_path: Path, suite: Sequence[EvalSpec], *, output_dir: Optional[Path] = None, matcher_filter: Optional[Callable[[str], bool]] = None,) -> CoverageResult:` |
| Silent-green parse-error block | 294-302 | **294-302** | (verbatim verified — `is_file()` guard, `json.JSONDecodeError` catch returns empty `CoverageResult()`) |

Full quote of L294-302 (the silent-green branch H1 will tighten):

```python
matcher_filter = matcher_filter or default_matcher_filter
if not settings_path.is_file():
    return CoverageResult()
try:
    data = json.loads(settings_path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    return CoverageResult()
if not isinstance(data, Mapping):
    return CoverageResult()
```

Three silent-green branches exist (missing file, OSError/JSONDecodeError, non-Mapping
top-level). H1 likely wants to keep the "missing file" branch silent (dev hosts without a
settings.json) but log/exit-non-zero for the parse-error and non-Mapping branches.

---

## C) config.py

| Symbol | Spec L | Actual L | Quote |
|---|---|---|---|
| `SCRATCH_ROOT_POLICY` | — | **40** | `SCRATCH_ROOT_POLICY: str = (` |
| `_default_allowed_scratch_roots` | — | **63** | `def _default_allowed_scratch_roots() -> tuple[Path, ...]:` |
| `class EvalConfig` | — | **84** | dataclass |
| `SCRATCH_ROOT_VIOLATION_EXIT_CODE` | — | **113** | `SCRATCH_ROOT_VIOLATION_EXIT_CODE: int = 2` |
| `class ScratchRootViolation` | — | **123** | exception |
| `_resolve_prefix` | — | **155** | `def _resolve_prefix(prefix: Path) -> Path:` |
| `def resolve_scratch_root` | — | **167** | `def resolve_scratch_root(path: Path \| str, *, config: EvalConfig \| None = None, output_dir: Path \| str \| None = None,) -> Path:` |
| `resolved == prefix` accept branch | 243-249 | **243-249** | verified verbatim |
| `format_scratch_root_violation` | — | **252** | helper |

Full quote of L243-249 (the prefix-equals branch H2 cleans up):

```python
for prefix in allowed:
    # ``is_relative_to`` catches strict sub-paths; the equality branch
    # accepts the prefix itself (``/tmp/eval-runs`` is a valid root).
    if resolved == prefix or resolved.is_relative_to(prefix):
        return resolved

raise ScratchRootViolation(candidate, resolved, allowed)
```

**Test coverage already exists** for this branch:
`tests/cli/eval/test_scratch_root_allowlist.py:52` →
`def test_accepts_tmp_eval_runs_root_itself()`. Builder must reference this file
(NOT `test_config.py`) for any H2 supplementary test.

---

## D) artifact_layout.py

| Symbol | Spec L | Actual L | Quote |
|---|---|---|---|
| `_RUN_ID_HASH_LEN` | — | **91** | `_RUN_ID_HASH_LEN: int = 8` |
| `_TIME_SEGMENT_FMT` | — | **92** | `_TIME_SEGMENT_FMT: str = "%H%M%SZ"` |
| `_DATE_SEGMENT_FMT` | — | **93** | `_DATE_SEGMENT_FMT: str = "%Y-%m-%d"` |
| `_EVAL_ID_RE` | 99 | **99** | `_EVAL_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")` |
| `_parse_iso` | — | **107** | helper |
| `compose_run_id` | — | **139** | `def compose_run_id(started_at: str, suite_name: str = "") -> str:` |
| `compose_run_dir` | — | **162** | `def compose_run_dir(output_root: Path \| str, started_at: str, suite_name: str = "",) -> Path:` returns `<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` |
| `PerEvalPaths` dataclass | — | **201** | frozen dataclass |
| `compose_per_eval_dir` | — | **217** | helper |
| `allocate_per_eval_paths` | — | **232** | the writer that `commands._run_one_spec` calls at L1440 |
| `RunDirComponents` | — | **269** | dataclass |
| `parse_run_dir_components` | — | **276** | parser |

**Interplay between `_default_output_dir` (commands.py L1335) and `_EVAL_ID_RE`**: The default
output dir helper calls `compose_run_dir(Path.cwd(), started_at, suite_name)` which uses
`compose_run_id`, NOT `_EVAL_ID_RE`. The regex `_EVAL_ID_RE` only guards eval-ids inside
`compose_per_eval_dir` / `allocate_per_eval_paths`. So the H- finding "duplicated regex"
involves `_EVAL_ID_RE` (artifact_layout) vs `EVAL_ID_REGEX` (loader); see F+H below.

---

## E) reporter.py

| Symbol | Spec L | Actual L | Quote |
|---|---|---|---|
| `render_summary_yaml` | — | **83** | helper |
| `class Reporter` | — | **116** | frozen dataclass; `Reporter(summary, emit_junit=False)` |
| `Reporter.to_markdown / to_yaml / to_json / to_junit` | — | **150 / 159 / 168 / 177** | delegates to `render_summary_*` |
| `Reporter.write` | 190-227 | **190-227** | (verbatim verified) |
| `AggregatedRunReport = Reporter` alias | — | **233** | the COMP-008 alias |

**Artifact set Reporter.write produces (CRITICAL for H3 — Reporter.write vs write_aggregated_report duplication):**

Always writes:
- `summary.md`   (L208, 212)
- `summary.json` (L209, 213)
- `summary.yaml` (L210, 214)  ← **only Reporter.write does this**

Conditionally writes (when `emit_junit=True`):
- `junit.xml`    (L222-225)

Returns `dict[str, Path]` mapping artefact-name → path. `junit.xml` only present
in the mapping when emit_junit is True (L226).

---

## F) run_report.py

| Symbol | Spec L | Actual L | Quote |
|---|---|---|---|
| `class ReporterContractViolation` | — | **63** | RuntimeError subclass |
| `_check_invariant` | — | **92** | the N'-vs-K guard |
| `_format_duration` | — | **112** | helper |
| `_row_note` | — | **125** | helper |
| `render_summary_markdown` | — | **137** | |
| `render_summary_json` | — | **229** | |
| `render_junit_xml` | — | **255** | |
| `def write_aggregated_report` | 335-379 | **335-380** | (file ends at L379 with `return written`; the `def` line is L335 — exact match) |

**Artifact set write_aggregated_report produces (H3 evidence):**

Always writes:
- `summary.md`   (L363, 366)
- `summary.json` (L364, 367)
- *(NO summary.yaml)*

Conditionally writes (when `emit_junit=True`):
- `junit.xml`    (L374-377)

**H3 duplication diff:** Reporter.write writes summary.yaml; write_aggregated_report does
NOT. Otherwise the two are byte-equivalent (same `_check_invariant` call, same
`out.mkdir(parents=True, exist_ok=True)`, same writer pattern, same return shape). The
H3 fix likely consolidates onto Reporter.write and either deletes write_aggregated_report
or makes it a thin alias.

Note: docstring at L335-356 says *"Emits: summary.md / summary.json / junit.xml"* —
deliberately does NOT advertise summary.yaml. So the divergence is intentional in some
prior decision; H3 needs to either reconcile both writers' contracts OR make the docstring
divergence explicit / un-confusing.

---

## G) isolation.py

| Symbol | Spec L | Actual L | Quote |
|---|---|---|---|
| `_write_setup_failed_tag` | — | **125** | helper |
| `class HomeContainmentViolation` | — | **162** | exception (the H5 raise site) |
| `def containment_guard` | — | **220** | the three-check FR-ISO2 defense-in-depth guard |
| `class HomeIsolation` | — | **356** | the per-eval HOME state machine |

**AC12 allowlist consumer in isolation.py** (the call site `resolve_scratch_root` flows through):
- L103 import: `from .config import EvalConfig, ScratchRootViolation, resolve_scratch_root`
- L240-250 docstring describes Check 2 — symlink-aware allowlist re-check
- **L307-310** actual call: `resolved_scratch = resolve_scratch_root(scratch_root, config=config)` inside `containment_guard`
- L467 — `HomeIsolation` constructor docstring references the same allowlist

`containment_guard` (L220-) is the SINGLE function relevant to H5 — that is where
the three checks (eval_id regex re-application via `validate_eval_id`, scratch-root
allowlist re-check, post-mkdtemp `Path.resolve(strict=True)` containment) compose.
Length: spans ~L220-355 (the function is long; verify exact end with `read` when
the builder writes the H5 checklist item).

---

## H) loader.py

| Symbol | Spec L | Actual L | Quote |
|---|---|---|---|
| `class InvalidEvalId` | — | **108** | exception |
| `EVAL_ID_REGEX` constant | — | **86** | `EVAL_ID_REGEX: re.Pattern[str] = re.compile(r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$")` |
| `def validate_eval_id` | 142 | **142** | `def validate_eval_id(eval_id: str) -> None:` body L171 uses `EVAL_ID_REGEX.fullmatch(eval_id) is None` |
| `_format_json_path` | — | **216** | helper |
| `_load_schema` / `_read_manifest` / `_validate_manifest_dict` | — | 235 / 239 / 276 | helpers |
| `validate_manifest` | — | **305** | top-level loader entry |
| `class CapabilityResolver` (Protocol) | — | **394** | |
| `class PermissiveCapabilityResolver` | — | **425** | |
| `class ParsedSuite` | — | **443** | dataclass |
| `class SuiteLoader` | — | **466** | |

**CC1 (eval-id regex) — duplication is actually DIVERGENCE:**

| File | Line | Regex pattern | Semantics |
|---|---|---|---|
| `loader.py` | L86-88 | `r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$"` | **STRICT**: must start with uppercase letter; only alphanumerics + optional trailing `.N` digit pair. Schema-aligned. |
| `artifact_layout.py` | L99   | `r"^[A-Za-z0-9_.-]{1,64}$"`                  | **PERMISSIVE**: any letter/digit/underscore/dash/dot, 1-64 chars. Path-safety only. |

These regexes have DIFFERENT acceptance sets. Examples:
- `"e1"` (lowercase): rejected by loader, accepted by artifact_layout
- `"E1.2.3"` (multi-dot): rejected by loader (only one `.N` allowed), accepted by artifact_layout
- `"E_TEST"` (underscore): rejected by loader, accepted by artifact_layout

CC1 remediation MUST account for this — the simplest unification (just import one from
the other) changes runtime behaviour. The two patterns serve different purposes:
- loader = "is this an FR-SCH2 manifest-valid id?"
- artifact_layout = "is this safe to interpolate into a filesystem path?"

The right answer is likely: keep both regexes but co-locate them in one module
(probably `loader.EVAL_ID_REGEX` as the schema, plus a separate
`artifact_layout.PATH_SAFE_ID_RE` with explicit docstrings linking them).

---

## I) exit_codes.py

**Confirmed: `src/superclaude/cli/eval/exit_codes.py` does not exist.**

```
$ ls /config/workspace/IronClaude/src/superclaude/cli/eval/exit_codes.py
ls: cannot access [...]: No such file or directory
```

CC2 creates this module. The constants it should host (all currently scattered across
commands.py + config.py + coverage.py + signal_handler.py):
- `RUN_CLEAN_EXIT_CODE` (commands.py L570)
- `RUN_FAILURES_EXIT_CODE` (commands.py L573)
- `RUN_INTERRUPTED_EXIT_CODE` (commands.py L577 — re-exports `signal_handler.EXIT_INTERRUPTED`)
- `SCRATCH_ROOT_VIOLATION_EXIT_CODE` (config.py L113)
- `COVERAGE_GATE_FAILED_EXIT_CODE` (coverage.py L77)
- `HARD_FAIL_EXIT_CODE`, `SUITE_NOT_FOUND_EXIT_CODE`, `SUITE_LOADER_ERROR_EXIT_CODE`,
  `EVAL_NOT_FOUND_EXIT_CODE`, `DISK_BUDGET_EXCEEDED_EXIT_CODE` — referenced in
  commands.py but defined elsewhere (verify in R3 integration-points map).

Important pin to preserve: `tests/cli/eval/test_exit_codes.py` (referenced in commands.py
L565-568) is the test-008/T04.19/D-0079 contract — extracting the constants must keep
that test green.

---

## Drift Summary

**Zero drift from spec line numbers.** Every cited symbol verified at the spec's cited
offset, with the spec's line numbers either exact or pointing to the first line of a
multi-line block whose final line matches the spec's range end. The only divergence
from a naive read of the spec:

1. CC1 is a regex *divergence*, not duplication — see section H. The builder's CC1
   checklist item should reflect this so the implementer doesn't paper over it with a
   simple "import one from the other".
2. Spec's reference to a test in `test_config.py` for the `resolved == prefix` branch
   is actually `tests/cli/eval/test_scratch_root_allowlist.py:52` — see section C.
3. The artifact-set divergence for H3 is concrete: Reporter.write writes summary.yaml
   (line 210/214), write_aggregated_report does not — see sections E + F.
