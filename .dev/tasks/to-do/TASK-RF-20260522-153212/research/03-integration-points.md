# Research 03 — Integration Points (Call-Graph Maps)

Task: TASK-RF-20260522-153212
Scope: `src/superclaude/cli/eval/` + `tests/cli/eval/`
Researcher: 03 — integration points / call graphs
Status: in-progress

All citations below were obtained by `Read` or `grep` against HEAD as of 2026-05-22. Each claim quotes the verbatim line content. Line numbers are absolute, 1-based.

---

## MAP 1 — CC2 exit-code consolidation (the "magic 2" literals)

### 1.1 Search summary

- `grep -rn "sys.exit(2)" src/superclaude/cli/eval/` → **0 functional hits** (one docstring reference at `commands.py:23` only).
- `grep -rn "Exit(2)" src/superclaude/cli/eval/` → **0 hits**.
- `grep -rn "return 2$" src/superclaude/cli/eval/` → **0 hits**.
- `grep -rn "raise click.exceptions.Exit(2)" src/superclaude/cli/eval/` → **0 hits**.
- `grep -rn "click.exceptions.UsageError\|UsageError" src/superclaude/cli/eval/` → **0 hits**.
- `grep -rEn "_EXIT_CODE.*=.*2" src/superclaude/cli/eval/` → **9 named constants** all set to literal `2` (across 6 files).

**Reframing:** The "7 magic `2` literals" in the spec are NOT bare `sys.exit(2)` calls. They are nine `*_EXIT_CODE: int = 2` constants — each module re-declares its own `2`, and there is no central `RUN_USAGE_ERROR_EXIT_CODE` or shared "harness-error" alias. The consolidation target the spec wants must replace **the right-hand side `2` literal** of each constant with a single source of truth (one canonical `int` constant exported once, the rest aliased to it).

### 1.2 The nine declarations (file:line + 3-line context)

#### a. `src/superclaude/cli/eval/commands.py:558` — `HARD_FAIL_EXIT_CODE`

```python
557
558  HARD_FAIL_EXIT_CODE = 2
559
```

Note: lacks the `: int` annotation that the other eight have. Used by the doctor / preflight surface (per docstring at L23, L592, L788).

#### b. `src/superclaude/cli/eval/commands.py:975` — `SUITE_NOT_FOUND_EXIT_CODE`

```python
974
975  SUITE_NOT_FOUND_EXIT_CODE: int = 2
976  """Process exit code emitted when :class:`SuiteNotFound` reaches the CLI.
```

#### c. `src/superclaude/cli/eval/commands.py:984` — `EVAL_NOT_FOUND_EXIT_CODE`

```python
983
984  EVAL_NOT_FOUND_EXIT_CODE: int = 2
985  """Process exit code emitted when :class:`EvalNotFound` reaches the CLI.
```

#### d. `src/superclaude/cli/eval/config.py:113` — `SCRATCH_ROOT_VIOLATION_EXIT_CODE`

```python
112
113  SCRATCH_ROOT_VIOLATION_EXIT_CODE: int = 2
114  """Exit code mapped to :class:`ScratchRootViolation` at the CLI boundary.
```

#### e. `src/superclaude/cli/eval/coverage.py:77` — `COVERAGE_GATE_FAILED_EXIT_CODE`

```python
76
77  COVERAGE_GATE_FAILED_EXIT_CODE: int = 2
78  """Process exit code emitted when the gate reports missing coverage.
```

#### f. `src/superclaude/cli/eval/run_report.py:52` — `REPORTER_CONTRACT_VIOLATION_EXIT_CODE`

```python
51  # reporter disagree on the row count, so the run itself is suspect.
52  REPORTER_CONTRACT_VIOLATION_EXIT_CODE: int = 2
53
```

#### g. `src/superclaude/cli/eval/loader.py:65` — `SCHEMA_ERROR_EXIT_CODE`

```python
64
65  SCHEMA_ERROR_EXIT_CODE: int = 2
66  """Process exit code emitted when :class:`SchemaError` reaches the CLI boundary.
```

#### h. `src/superclaude/cli/eval/loader.py:75` — `INVALID_EVAL_ID_EXIT_CODE`

```python
74
75  INVALID_EVAL_ID_EXIT_CODE: int = 2
76  """Process exit code emitted when :class:`InvalidEvalId` reaches the CLI boundary.
```

#### i. `src/superclaude/cli/eval/loader.py:336` — `UNRESOLVED_CAPABILITY_EXIT_CODE`

```python
335
336  UNRESOLVED_CAPABILITY_EXIT_CODE: int = 2
337  """Process exit code emitted when :class:`UnresolvedCapability` reaches the CLI.
```

#### j. `src/superclaude/cli/eval/loader.py:347` — `SUITE_LOADER_ERROR_EXIT_CODE`

```python
346
347  SUITE_LOADER_ERROR_EXIT_CODE: int = 2
348  """Single canonical exit code for every :class:`SuiteLoaderError` subclass.
```

#### k. `src/superclaude/cli/eval/disk_budget.py:106` — `DISK_BUDGET_EXCEEDED_EXIT_CODE`

```python
105  # the loader / scratch-root / reporter-contract violations.
106  DISK_BUDGET_EXCEEDED_EXIT_CODE: int = 2
107
```

### 1.3 Already-named exit-code constants (for context — `RUN_*` trio)

`src/superclaude/cli/eval/commands.py:570-577`:

```python
570  RUN_CLEAN_EXIT_CODE: int = 0
571  """Clean run: every expanded eval reached PASS / SKIPPED / XFAIL and no breach."""
572
573  RUN_FAILURES_EXIT_CODE: int = 1
574  """Failing run: at least one eval ended FAIL / ERRORED / TIMEOUT / XPASS but
575  the harness ran to completion."""
576
577  RUN_INTERRUPTED_EXIT_CODE: int = EXIT_INTERRUPTED
```

Note the pattern at L577: `RUN_INTERRUPTED_EXIT_CODE` is **aliased** to `EXIT_INTERRUPTED` (imported from `signal_handler`) rather than re-declaring `3`. This is the consolidation pattern the spec wants applied to the 9 `= 2` literals.

### 1.4 Three call sites that actually `sys.exit(<constant>)`

```
commands.py:1932:        sys.exit(RUN_INTERRUPTED_EXIT_CODE)
commands.py:1949:        sys.exit(RUN_FAILURES_EXIT_CODE)
commands.py:1950:    sys.exit(RUN_CLEAN_EXIT_CODE)
```

None of the nine `= 2` constants are invoked via `sys.exit(...)` in `eval/` — they are raised through exception classes and mapped at the Click boundary (callers in the wider `src/superclaude/cli/` may translate). The "magic-2" cleanup is therefore a **declaration-site** refactor, not a call-site refactor.

### 1.5 Recommended consolidation (per spec)

Add a single canonical constant — recommended name `RUN_USAGE_ERROR_EXIT_CODE: int = 2` — in one authoritative module (the spec implies `commands.py` near the existing `RUN_*` trio, alongside L570-577). Then rewrite each of the nine declarations as an **alias** to that constant, mirroring the `RUN_INTERRUPTED_EXIT_CODE = EXIT_INTERRUPTED` pattern:

| Current declaration (file:line) | New RHS |
|---|---|
| commands.py:558 `HARD_FAIL_EXIT_CODE = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| commands.py:975 `SUITE_NOT_FOUND_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| commands.py:984 `EVAL_NOT_FOUND_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| config.py:113 `SCRATCH_ROOT_VIOLATION_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| coverage.py:77 `COVERAGE_GATE_FAILED_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| run_report.py:52 `REPORTER_CONTRACT_VIOLATION_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| loader.py:65 `SCHEMA_ERROR_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| loader.py:75 `INVALID_EVAL_ID_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| loader.py:336 `UNRESOLVED_CAPABILITY_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| loader.py:347 `SUITE_LOADER_ERROR_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |
| disk_budget.py:106 `DISK_BUDGET_EXCEEDED_EXIT_CODE: int = 2` | `= RUN_USAGE_ERROR_EXIT_CODE` |

Eleven occurrences total — the spec's "7 magic `2`s" undercounts. Builder should verify spec wording against this map; if the spec literally enumerates seven, the four others (HARD_FAIL_EXIT_CODE, SUITE_NOT_FOUND_EXIT_CODE, EVAL_NOT_FOUND_EXIT_CODE, DISK_BUDGET_EXCEEDED_EXIT_CODE) may have been omitted by oversight or intentionally scoped out — flag for clarification.

Import wiring needed:
- `commands.py` → just define `RUN_USAGE_ERROR_EXIT_CODE` (already exports the `RUN_*` trio).
- `config.py`, `coverage.py`, `run_report.py`, `loader.py`, `disk_budget.py` → add `from .commands import RUN_USAGE_ERROR_EXIT_CODE` OR (preferred to avoid a circular import) place the canonical constant in a low-level module (e.g. `signal_handler.py` next to `EXIT_INTERRUPTED`, or a new `exit_codes.py`) and have everyone import from there.
- `__init__.py` exports — L147-184 currently re-exports all nine constants; add `RUN_USAGE_ERROR_EXIT_CODE` to `__all__` and the import block.


---

## MAP 2 — CC1 FR-SCH2 regex duplication

### 2.1 The two declarations

#### Declaration A — `src/superclaude/cli/eval/artifact_layout.py:99`

```python
96  # Eval-id allowlist — the FR-SCH2 regex pinned by the schema (kept
97  # defensive here so this module rejects out-of-band ids at the layout
98  # boundary rather than producing path-traversal candidates).
99  _EVAL_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
```

Pattern verbatim: `^[A-Za-z0-9_.-]{1,64}$`

Single consumer: `artifact_layout.py:225` —

```python
225  if not isinstance(eval_id, str) or not _EVAL_ID_RE.match(eval_id):
```

No external consumers (the constant is a leading-underscore module-private).

#### Declaration B — `src/superclaude/cli/eval/loader.py:86-88`

```python
86  EVAL_ID_REGEX: re.Pattern[str] = re.compile(
87      r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$"
88  )
```

Pattern verbatim: `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`

Consumers (all in `loader.py`):
- L48 — exported in `__all__`
- L137 — embedded in error message: `f"eval id failed FR-SCH2 regex ({EVAL_ID_REGEX.pattern!r}): "`
- L171 — `if EVAL_ID_REGEX.fullmatch(eval_id) is None:` (inside `validate_eval_id`)

Indirect consumers via `validate_eval_id`:
- `loader.py:545` — `validate_eval_id(entry.get("id"))`
- `loader.py:619` — `validate_eval_id(expanded_id)`
- `isolation.py:104` — `from .loader import InvalidEvalId, validate_eval_id`
- `isolation.py:297` — `validate_eval_id(eval_id)`
- `isolation.py:401` — `validate_eval_id(self.eval_id)`
- Test: `tests/cli/eval/test_eval_id_regex.py:32` — `from superclaude.cli.eval.loader import EVAL_ID_REGEX`
- Test: `tests/cli/eval/test_eval_id_regex.py:45` — asserts pattern equals `r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$"` (PINS B's pattern).

### 2.2 ⚠ CRITICAL FINDING — the regexes are not semantically equivalent

| | Pattern A (artifact_layout) | Pattern B (loader / authoritative) |
|---|---|---|
| Pattern | `^[A-Za-z0-9_.-]{1,64}$` | `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` |
| Must start with uppercase | No | **Yes** (`[A-Z]`) |
| Allows `_` | **Yes** | No |
| Allows `-` | **Yes** | No |
| Allows `.` | Anywhere | Only as version suffix |
| Length cap | 64 | Unbounded |
| Empty-allowed | No (1+) | No (`[A-Z]` required) |
| Test pin | None | `tests/cli/eval/test_eval_id_regex.py:45` |

These do **not** match. Pattern A would accept `my_eval-1.0` and `e1` (lowercase) and `foo`; Pattern B rejects all three. Pattern B is the FR-SCH2 contract (per schema + tests + docstring "single source of truth"). Pattern A is a coarser defensive guard that happens to admit a superset of B's valid ids, plus an extra path-traversal guard (`{1,64}` length cap, no `/` or `\`).

Implications for the consolidation:
- This is **not a simple rename**. The spec ("`EVAL_ID_PATTERN` in artifact_layout.py") implies moving the canonical constant to `artifact_layout.py`, but the **canonical pattern is B's strict form**.
- Two possible interpretations the builder must surface:
  1. **Single regex consolidation** — replace both with B's strict pattern (`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`). This would *tighten* `artifact_layout.compute_per_eval_dir`'s acceptance set; verify no extant valid id like `E1` would suddenly fail (B accepts `E1`, `E2.1`, `D15` — these are the valid forms).
  2. **Two-layer guard** — keep both as separate, named constants but co-locate them: `EVAL_ID_PATTERN` (strict, FR-SCH2) used by the loader, and `EVAL_ID_PATH_SAFE_PATTERN` (path-traversal guard with 64-char cap) used by `artifact_layout`. Document both in the same module.
- The spec language "`EVAL_ID_PATTERN` in artifact_layout.py" combined with the strict-pattern test pin suggests interpretation #1 is intended, but builder MUST flag the semantic divergence rather than silently swap A's pattern for B's.

### 2.3 Recommended consolidation (per spec, with caveat)

If single-source-of-truth:
1. Define `EVAL_ID_PATTERN: re.Pattern[str] = re.compile(r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$")` at the new authoritative site. Spec says `artifact_layout.py`; the test pin at `tests/cli/eval/test_eval_id_regex.py:32` currently imports from `loader`, so the constant location is fungible as long as the import is updated.
2. Update `artifact_layout.py:99` — remove `_EVAL_ID_RE` declaration.
3. Update `artifact_layout.py:225` — replace `_EVAL_ID_RE.match(eval_id)` with the new `EVAL_ID_PATTERN.fullmatch(eval_id)` (note `match` → `fullmatch` mismatch; A used `match`, B uses `fullmatch` — pick fullmatch; both A's patterns are anchored `^...$` so behaviour is equivalent, but fullmatch is safer).
4. Update `artifact_layout.py:227` — the error message references `[A-Za-z0-9_.-]{{1,64}}` — must be updated to the new pattern string.
5. Update `loader.py:86-88` — replace `EVAL_ID_REGEX` declaration with re-export OR alias to the new constant (keep the symbol `EVAL_ID_REGEX` as an alias so `tests/cli/eval/test_eval_id_regex.py:32, 45` still pass without test edits — OR plan a coordinated test update).
6. Update `loader.py:48` — `__all__` entry.
7. Update `loader.py:137` — f-string error message still references `EVAL_ID_REGEX.pattern`; will keep working via the alias.
8. Update `loader.py:171` — `EVAL_ID_REGEX.fullmatch(...)` → keep via alias, or rewrite to `EVAL_ID_PATTERN.fullmatch(...)`.
9. Update `__init__.py:62, 204` — may need to re-export `EVAL_ID_PATTERN`.
10. Cascade: every `isolation.py` and test call site stays untouched because they use `validate_eval_id` (function-level), not the regex directly.


---

## MAP 3 — H3/M3 `EVAL_STATUSES` source-of-truth

### 3.1 Canonical definition — `src/superclaude/cli/eval/models.py:49-62`

```python
49  EvalStatus = Literal[
50      "PASS",
51      "FAIL",
52      "ERRORED",
53      "TIMEOUT",
54      "INTERRUPTED",
55      "SKIPPED",
56      "XFAIL",
57      "XPASS",
58  ]
59  # Resolved tuple for runtime membership checks. Kept in module scope so the
60  # Reporter (COMP-008 / T03.13) and orchestrator can validate status values
61  # against the same authoritative set without re-deriving from the Literal.
62  EVAL_STATUSES: tuple[str, ...] = get_args(EvalStatus)
```

`EVAL_STATUSES` is a **tuple of 8 strings**, not a frozenset or enum, derived from `typing.get_args(EvalStatus)`. The `Literal` is the SoT; `EVAL_STATUSES` is the runtime echo.

### 3.2 Direct consumers

- `models.py:62` — definition.
- `models.py:345-347` — `EvalOutcome.__post_init__` validates `self.status not in EVAL_STATUSES`.
- `__init__.py:66, 133` — package-level re-export (`__all__`).
- `commands.py:81` — imported into commands module.
- `commands.py:1496-1502` — used by `_compute_run_stats` (see 3.4).
- `schemas/summary.schema.json:85` — schema comment: "DM-001 EvalStatus literal set. Must match `superclaude.cli.eval.models.EVAL_STATUSES` verbatim."

### 3.3 `_compute_run_stats` (commands.py:1477-1523)

Header signature (L1477-1481):

```python
1477  def _compute_run_stats(
1478      outcomes: Sequence[EvalOutcome],
1479      *,
1480      manifest_n: int,
1481  ) -> tuple[RunCounts, RunTotals]:
```

Derived vs hardcoded analysis:

```python
1495      expanded = len(outcomes)
1496      # DM-012 categorization derived from the EVAL_STATUSES SoT
1497      # (models.py:62). SKIPPED + INTERRUPTED are non-terminal; everything
1498      # else in EVAL_STATUSES is a terminal "kept" outcome. Deriving rather
1499      # than hardcoding ensures that adding a new EvalStatus value cannot
1500      # silently drift this tally out of sync with the canonical set.
1501      skipped_statuses = frozenset({"SKIPPED", "INTERRUPTED"})
1502      kept_statuses = frozenset(EVAL_STATUSES) - skipped_statuses
```

- `kept_statuses` IS derived from `EVAL_STATUSES` (good, per DM-012 invariant).
- `skipped_statuses` is **hardcoded** to `{"SKIPPED", "INTERRUPTED"}` — a literal set, not derived.
- The `RunTotals` construction (L1515-1521) uses **fully hardcoded** status checks:

```python
1515      totals = RunTotals(
1516          passed=sum(1 for o in outcomes if o.status in {"PASS", "XFAIL"}),
1517          failed=sum(1 for o in outcomes if o.status in {"FAIL", "XPASS"}),
1518          skipped=sum(1 for o in outcomes if o.status == "SKIPPED"),
1519          errored=sum(1 for o in outcomes if o.status == "ERRORED"),
1520          interrupted=sum(1 for o in outcomes if o.status == "INTERRUPTED"),
1521          timeout=sum(1 for o in outcomes if o.status == "TIMEOUT"),
1522      )
```

Every status literal is a bare string — 8 distinct hardcoded references. Adding a 9th `EvalStatus` literal would silently drop it from the `RunTotals` headline.

### 3.4 `_format_run_summary_line` (commands.py:1526-1539)

```python
1526  def _format_run_summary_line(summary: RunSummary, output_dir: Path) -> str:
...
1532      return (
1533          f"run {summary.run_id}: "
1534          f"{summary.totals.passed}P/"
1535          f"{summary.totals.failed}F/"
1536          f"{summary.totals.skipped}S "
1537          f"in {summary.duration_sec:.2f}s "
1538          f"-> {output_dir}"
1539      )
```

Hardcoded format — surfaces only `passed`/`failed`/`skipped` from `RunTotals`. Does NOT touch `errored`/`interrupted`/`timeout`. The `RunTotals` field set is implicit; renaming a field would silently fail at attribute-access time.

### 3.5 `RunCounts` / `RunTotals` taxonomy alignment

`models.py:732-806`:

`RunCounts` (L733-761) — five fields:

```python
757      manifest_n: int
758      expanded_n_prime: int
759      kept_k: int
760      skipped_s: int
761      kept_plus_skipped_equals_n_prime: bool
```

Docstring at L746-749 pins the keep/skip split: "kept_k — number of expanded rows that ran end-to-end (status in `{PASS,FAIL,ERRORED,TIMEOUT,XFAIL,XPASS}`)" and "skipped_s — number of expanded rows that were skipped (status `SKIPPED` or `INTERRUPTED`)". This **matches** `_compute_run_stats`'s hardcoded `{"SKIPPED", "INTERRUPTED"}` — but the docstring is yet another encoding of the same set.

`RunTotals` (L786-801) — six int fields:

```python
796      passed: int = 0
797      failed: int = 0
798      skipped: int = 0
799      errored: int = 0
800      interrupted: int = 0
801      timeout: int = 0
```

Docstring at L791-793: "XFAIL and XPASS roll into `passed` and `failed` respectively per the DM-012 schema". Again the rollup is documented, but the code at `commands.py:1516-1517` is the only place where the rollup is mechanically performed.

`_RUN_TOTALS_FIELDS` (`models.py:775-782`) — field-order tuple — drives `to_dict()` ordering at L806. Hardcoded order; would need to change if a new status field is added.

### 3.6 Drift surface — three places to keep in lock-step

| Source-of-truth | Owns what | File:line |
|---|---|---|
| `EvalStatus` `Literal` | The 8 allowed status strings | models.py:49-58 |
| `EVAL_STATUSES` tuple | Runtime echo of the Literal | models.py:62 |
| `RunTotals` field names | The 6 outcome buckets (XFAIL/XPASS roll up) | models.py:796-801 |
| `_RUN_TOTALS_FIELDS` | Field iteration order for `to_dict()` | models.py:775-782 |
| `_compute_run_stats` hardcoded sets | The pass/fail/skipped/errored/interrupted/timeout assignment | commands.py:1516-1521 |
| `_format_run_summary_line` | Stdout headline format (`P/F/S`) | commands.py:1532-1539 |
| DM-012 schema comment | Schema-side echo of the Literal | schemas/summary.schema.json:85 |
| `_compute_run_stats` `skipped_statuses` | Hardcoded `{"SKIPPED", "INTERRUPTED"}` | commands.py:1501 |
| `RunCounts` docstring | Documented keep/skip split | models.py:746-749 |

A clean SoT consolidation per the spec would:
- Replace `commands.py:1501` literal set with `frozenset({s for s in EVAL_STATUSES if s in ("SKIPPED", "INTERRUPTED")})` OR (better) a new module-level constant in `models.py` like `SKIPPED_STATUSES: frozenset[str] = frozenset({"SKIPPED", "INTERRUPTED"})`, exported alongside `EVAL_STATUSES`, then imported here.
- Add `PASSED_STATUSES = frozenset({"PASS", "XFAIL"})` and `FAILED_STATUSES = frozenset({"FAIL", "XPASS"})` near `EVAL_STATUSES` and replace the inline sets at commands.py:1516-1517.
- Likewise singletons for ERRORED/INTERRUPTED/TIMEOUT/SKIPPED — though these are arguably less "drift surfaces" because they map 1:1.


---

## MAP 4 — H5 allowlist call graph (home_root.mkdir before extension)

### 4.1 Containing function

The region commands.py:1735-1746 lives inside `eval_run()` — the Click command function defined at **commands.py:1644**. (Decorators start at L1572; `def eval_run(` is at L1644.)

### 4.2 The verbatim 10-15 line region (commands.py:1727-1752)

```python
1727          resolved_output = resolve_scratch_root(
1728              requested_output,
1729              config=base_config,
1730          )
1731      except ScratchRootViolation as exc:
1732          click.echo(format_scratch_root_violation(exc), err=True)
1733          sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)
1734
1735      resolved_output.mkdir(parents=True, exist_ok=True)
1736      home_root = resolved_output / "homes"
1737      home_root.mkdir(parents=True, exist_ok=True)
1738
1739      # The runtime EvalConfig extends the canonical allowlist with the
1740      # per-run home root + the operator-supplied output directory so
1741      # downstream ``containment_guard`` calls see a stable allowlist
1742      # rather than re-deriving one from scratch.
1743      runtime_allowed = tuple(base_config.allowed_scratch_roots) + (
1744          resolved_output,
1745          home_root,
1746      )
1747      runtime_config = EvalConfig(
1748          paths=base_config.paths,
1749          defaults=base_config.defaults,
1750          allowed_scratch_roots=runtime_allowed,
1751          min_claude_version=base_config.min_claude_version,
1752      )
1753
```

### 4.3 Order of operations as it stands today

| Step | Action | Line(s) |
|---|---|---|
| 1 | `resolve_scratch_root(requested_output, config=base_config)` — operator path validated against the **base** allowlist (no `home_root` yet, no `resolved_output` echoed in) | 1727-1730 |
| 2 | Exception path: scratch-root violation → `sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)` | 1731-1733 |
| 3 | **mkdir `resolved_output`** (the operator's `--output-dir`, now validated) | 1735 |
| 4 | Compute `home_root = resolved_output / "homes"` | 1736 |
| 5 | **mkdir `home_root`** ← this is the `home_root.mkdir` before allowlist extension | 1737 |
| 6 | Allowlist extension: `runtime_allowed = base + (resolved_output, home_root)` | 1743-1746 |
| 7 | `runtime_config = EvalConfig(...)` built with extended allowlist | 1747-1752 |

So the actual ordering is: validate operator path → mkdir output → derive home_root → mkdir home_root → THEN extend allowlist.

### 4.4 H5 risk surface

The `home_root.mkdir(parents=True, exist_ok=True)` at L1737 happens **before** `home_root` is in any allowlist. The mkdir itself is unguarded — it will create `<resolved_output>/homes/` even if downstream allowlist-aware code (e.g. `containment_guard` in `isolation.py`) would refuse to operate there.

This isn't an immediate exploit because:
- `resolved_output` was already validated by `resolve_scratch_root` at L1727 (so it lies inside the canonical allowlist).
- `home_root = resolved_output / "homes"` is a sub-path of `resolved_output`, so `is_relative_to` would always succeed.

But the **ordering** matters for H5 because:
- A future refactor that lets `home_root` be operator-supplied (rather than `resolved_output / "homes"`) would create an unguarded mkdir surface — the mkdir at L1737 happens BEFORE the path is folded into any allowlist check.
- The OPS-002 invariant "no filesystem write before allowlist validation" is implicitly preserved here only because `home_root` is a syntactic sub-path of `resolved_output`, not because there's an explicit gate.

### 4.5 `resolve_scratch_root` definition (config.py:170-249)

Signature contract excerpted from the verbatim docstring at config.py:200-227:

```python
200              The value is resolved the same way as the rest of the
201              allowlist; passing it does NOT mutate ``config``.
202
203              **Do NOT pass the raw operator-supplied ``--output-dir`` here
204              at the first gate.** Doing so makes the candidate path equal
205              to an allowlist entry by construction, turning the AC12
206              check into a tautology and letting non-allowlisted paths
207              (e.g. ``/etc/foo``, ``/root/.claude``) escape onto disk.
208              The first gate must call ``resolve_scratch_root(path)`` (or
209              ``resolve_scratch_root(path, config=cfg)``) with the
210              operator-supplied path as the *candidate* only; the kwarg
211              is reserved for subsequent layered re-checks that need to
212              preserve the previously-validated operator path.
```

Implementation core (config.py:234-249):

```python
234      allowed: list[Path] = [
235          _resolve_prefix(prefix) for prefix in config.allowed_scratch_roots
236      ]
237      if output_dir is not None:
238          allowed.append(_resolve_prefix(Path(output_dir)))
239
240      candidate = Path(path)
241      resolved = candidate.expanduser().resolve(strict=False)
242
243      for prefix in allowed:
244          # ``is_relative_to`` catches strict sub-paths; the equality branch
245          # accepts the prefix itself (``/tmp/eval-runs`` is a valid root).
246          if resolved == prefix or resolved.is_relative_to(prefix):
247              return resolved
248
249      raise ScratchRootViolation(candidate, resolved, allowed)
```

Note the contract: **first call site at L1727 correctly does NOT pass `output_dir=`** — it lets the operator path be validated against the base allowlist only. This is the AC12-compliant call pattern documented at config.py:203-213.

### 4.6 `containment_guard` definition (isolation.py:220-326)

Signature (L220-226):

```python
220  def containment_guard(
221      home_path: Path,
222      scratch_root: Path,
223      eval_id: str,
224      *,
225      config: EvalConfig,
226  ) -> None:
```

The function exists. It performs three checks (L233-259):
1. `validate_eval_id(eval_id)` (L295-305)
2. `resolve_scratch_root(scratch_root, config=config)` (L309-318) — symlink-aware allowlist re-check
3. Post-mkdtemp symlink-resolved containment (L251-259)

Caller from `HomeIsolation.setup` is at `isolation.py:575-580`:

```python
575              containment_guard(
576                  home_path=home,
577                  scratch_root=self.home_root,
578                  eval_id=self.eval_id,
579                  config=config,
580              )
```

And critically — at `isolation.py:530-533`, BEFORE the `mkdtemp` and `containment_guard`:

```python
530          # Ensure the scratch root exists. ``parents=True, exist_ok=True``
531          # is safe because the FR-ISO2 guard below catches any path that
532          # resolves outside the policy allowlist.
533          self.home_root.mkdir(parents=True, exist_ok=True)
```

This is another `home_root.mkdir` BEFORE any allowlist re-check. The comment justifies it ("the FR-ISO2 guard below catches any path that resolves outside the policy allowlist") — but the guard runs AFTER this mkdir + AFTER `mkdtemp` (L536) writes a per-eval directory. So the H5 question — "is mkdir-before-guard a problem?" — applies here too: the on-disk state is mutated before the guard validates the path.

### 4.7 Operations-order summary for the builder

Two `home_root.mkdir` sites, both occurring BEFORE the corresponding allowlist gate completes:

| Site | mkdir line | Guard line | Guard type | Ordering risk |
|---|---|---|---|---|
| `commands.py:eval_run` | 1737 | 1747-1752 (allowlist *built*, not *checked*) | Allowlist build | Low — `home_root` is a syntactic sub-path of pre-validated `resolved_output`. |
| `isolation.py:HomeIsolation.setup` | 533 | 575-580 (`containment_guard`) | Three-check FR-ISO2 | Higher — the mkdir + subsequent `mkdtemp` (L536) write before the guard runs. Justified by the L531 comment, but the on-disk state is mutated pre-guard. |

For an H5 remediation, the candidate ordering changes are:
1. **commands.py:1735-1746** — pre-compute the extended allowlist *before* mkdir, so `home_root` is in the allowlist at the moment the mkdir happens, or push the mkdir into `HomeIsolation.setup` (already there at L533 — and that's the second site).
2. **isolation.py:530-533** — move `self.home_root.mkdir(...)` after a containment pre-check (a `resolve_scratch_root(self.home_root, config=config)` invocation before mkdir), so no on-disk side effect precedes allowlist validation.

The builder should produce one checklist item per site, plus one per-call-site test in `tests/cli/eval/test_scratch_root_policy.py` / `tests/cli/eval/test_containment.py`.

---

## Status

**Complete.** Four maps populated with verbatim citations from HEAD (2026-05-22).

### Key surprises the builder must surface

1. **MAP 1**: The spec says "7 magic `2` literals" — actual count is **11** named `*_EXIT_CODE: int = 2` constants across 6 files. The "consolidation" is a declaration-site refactor (replace `= 2` with `= RUN_USAGE_ERROR_EXIT_CODE`), not a call-site refactor — there are zero `sys.exit(2)` or `Exit(2)` literals in `src/superclaude/cli/eval/`.
2. **MAP 2**: The "two duplicate regex" claim is misleading — the two patterns are **semantically different**. `_EVAL_ID_RE` (artifact_layout.py:99) is a permissive 64-char path-safety guard; `EVAL_ID_REGEX` (loader.py:86-88) is the strict FR-SCH2 contract pinned by tests. Naive consolidation will tighten or loosen acceptance depending on direction.
3. **MAP 3**: `_compute_run_stats` already derives `kept_statuses` from `EVAL_STATUSES` but leaves `skipped_statuses` hardcoded at commands.py:1501, and the `RunTotals` rollup at L1515-1521 has 8 hardcoded status literals. Three drift surfaces still need consolidating: `SKIPPED_STATUSES`, `PASSED_STATUSES` (`{PASS, XFAIL}`), `FAILED_STATUSES` (`{FAIL, XPASS}`).
4. **MAP 4**: There are **two** `home_root.mkdir`-before-guard sites — `commands.py:1737` (low risk, syntactic sub-path) and `isolation.py:533` (higher risk, mutates on-disk state before `containment_guard` runs).
