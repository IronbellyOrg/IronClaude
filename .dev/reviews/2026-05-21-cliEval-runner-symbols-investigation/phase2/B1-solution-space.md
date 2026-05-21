# Phase 2A — B1 Solution Space (HYBRID T1+T3 Remediation)

**Agent:** B1 (solution-space brainstorm; neutral generator, not advocate)
**Date:** 2026-05-21
**Mode:** Candidate ideation + churn×fidelity×risk ranking + open-question resolution
**Inputs consulted:** `phase1B-debate-verdict.md`, `phase1/A1-module-audit.md`, `phase1/A4-thesis-belong-elsewhere.md`, `src/superclaude/cli/eval/commands.py:1406-1695`, `src/superclaude/cli/eval/artifact_layout.py:107-260`, `src/superclaude/cli/eval/models.py:720-825`, `design-spec.md §4 (lines 202-209)`.

**Discovery tier:** INFERENTIAL leaps allowed when flagged. LOC estimates use stated counting methods. No source edits — read-only artifact.

---

## 0. Inputs framing the solution space

The Phase 1B verdict pins six load-bearing constraints (paraphrased; full statements at verdict §"Implications for Phase 2"):

1. **C1 — `RUN_*_EXIT_CODE` constants live in `commands.py`.** Design-spec §4 integers (`0/1/3`) dictated; convention matches eight existing `*_EXIT_CODE` constants. No sibling import permitted (would violate FR-G1 ban-import contract by reaching across module domains for run-level outcome semantics).
2. **C2 — `_run_one_spec` MUST be a `commands.py` module attribute.** Five test files use `mock.patch("...commands._run_one_spec", ...)` (`test_single_command.py:148-160`, `test_exit_codes.py:93-113`, `test_no_pty_exclusion.py:266-337`, `test_no_mcp_skip.py:30-528`, `test_validation_commands.py:166-177`). Relocation silently breaks the test contract.
3. **C3 — F401 cleanup runs in lockstep.** Twelve F401 unused-imports (per `T04.22/ruff-check.log`); six become consumed once HYBRID wrappers land (`HomeIsolation`, `HomeContainmentViolation`, `RunCounts`, `RunTotals`, `EvalRunner`, `LifecycleExecutor`); two become consumed once `_utc_iso_now` lands (`datetime`, `timezone`); four are stale (`os`, `secrets`, `Sequence`, plus one TBD). The ruff gate gates the sprint.
4. **C4 — Per-symbol verdict table** is non-negotiable (see verdict §"Per-symbol verdict table"): 7 pure-T1 + 4 HYBRID T1+T3. No candidate may displace this without re-opening Phase 1B.
5. **C5 — Test mocking surface dictates `commands.py`-local placement** for at least `_run_one_spec` and (by inference) the other 10 symbols enumerated by the `_t0410_missing()` probe in `test_exit_codes.py:93-113` and `_eval_run_body_incomplete()` in `test_single_command.py:148-160`. Both probes use `hasattr(cmds, name)` against the `commands` module.
6. **C6 — Call-site ordering is fixed.** `_new_run_id()` fires at line 1467, BEFORE `started_iso = _utc_iso_now()` at line 1612 (145 lines later). Either (a) the wrapper computes `started_iso` internally, or (b) the body is reordered to hoist `started_iso` above the run-id call.

The body grew from 1418-1646 (per the ruff log) to the current 1467-1695 — net +49 LOC of unrelated work between phases — but the **set of missing symbols is unchanged** (A1 §2 reconciliation note). Any candidate that estimates by raw line count must use the **current** line numbers.

---

## 1. Five candidate approaches

### Candidate C1 — **Minimal In-Place Authoring**

**One-sentence summary.** Author all 7 pure-T1 helpers + 4 HYBRID wrappers inline in `commands.py` immediately above `eval_run`; no sibling-module touches beyond the F401 cleanup; smallest possible blast radius.

**Approach class.** Pure in-place authoring against the per-symbol verdict table. Wrappers delegate to verified sibling helpers but live as `commands.py` module attributes.

**LOC estimate** (method: counted 7 pure-T1 helpers × ~3-5 LOC each [≈28] + 4 HYBRID wrappers × ~3-6 LOC each [≈18] + 3 constants × 1 LOC [3] + 12 F401 removals [-12 net, but +0 if some imports are kept-and-used] + ~3 LOC of section comments ≈ **+52 / -12 / 0 moved**, net ~+40 LOC in `commands.py`):

| Δ added | Δ removed | Δ moved |
|---|---|---|
| ~52 | ~12 (F401) | 0 |

**Files touched: 1** — `src/superclaude/cli/eval/commands.py` only. (F401 cleanup is intrinsic — same file.)

**Per-symbol routing.**

| # | Symbol | Treatment | Home |
|---|---|---|---|
| 1 | `_new_run_id` | thin wrapper → `compose_run_id(_utc_iso_now(), parsed.name)` | commands.py |
| 2 | `_default_output_dir` | thin wrapper → `compose_run_dir(Path.cwd(), _utc_iso_now(), parsed.name)` | commands.py |
| 3 | `_resolve_executor_factory` | factory returning `lambda: ClaudeProcessAdapter(...)` | commands.py |
| 4 | `_run_one_spec` | ~30-LOC glue calling `allocate_per_eval_paths` + `HomeIsolation(...)` + `EvalRunner(...).run(spec)` | commands.py |
| 5 | `_utc_iso_now` | 1-line stdlib delegation | commands.py |
| 6 | `_can_install_signal_handler` | 2-line `threading.main_thread()` probe | commands.py |
| 7 | `_compute_run_stats` | local aggregator over outcomes returning `(RunCounts, RunTotals)` | commands.py |
| 8 | `_format_run_summary_line` | f-string one-liner | commands.py |
| 9 | `RUN_INTERRUPTED_EXIT_CODE = 3` | module constant | commands.py |
| 10 | `RUN_FAILURES_EXIT_CODE = 1` | module constant | commands.py |
| 11 | `RUN_CLEAN_EXIT_CODE = 0` | module constant | commands.py |

**Fidelity to design-spec §4.** HIGH — constants land at exact integer values (`0/1/3`) with names matching the existing eight `*_EXIT_CODE` pattern; the exit-code switch at 1676-1695 needs zero rewiring.

**Risk to FR-G1 ban-import contract.** LOW — no new sibling-to-sibling reach; HYBRID wrappers consume only the F401-staged sibling imports that already live in the import block (`compose_run_id`, `compose_run_dir`, `HomeIsolation`, `EvalRunner`, etc.). FR-G1 prohibits *new* cross-domain edges; this candidate adds zero.

**Test-contract preservation.** PASS — `mock.patch("...commands._run_one_spec", ...)` resolves: `_run_one_spec` is authored as a module attribute. Equally `mock.patch("...commands._new_run_id", ...)` (used in `test_artifact_reproducibility.py`-style mocks) resolves. All 11 names land in `commands` module namespace.

**Compatibility with already-landed P3/P4 surface.**
- **Expect primitives (T04.x):** untouched — wrappers consume `EvalRunner` which already wires Expect.
- **FR-CLI1 (12-flag decorator stack at commands.py:1167):** untouched.
- **FR-G4 layout:** preserved — HYBRID wrappers delegate to `compose_run_id`/`compose_run_dir`/`allocate_per_eval_paths` which own the layout contract.
- **FR-G5 coverage:** untouched — `coverage_gate(...)` call at 1541 unchanged.
- **TEST-007/8/9:** preserved — no test-file edits required; skip-gates evaporate automatically when `hasattr(cmds, name)` becomes True for all 11 names.
- **OPS-003:** preserved — `DISK_BUDGET_RETENTION_ADVICE` echo at 1687 unchanged.

**New tests required.**
- `tests/cli/eval/test_eval_run.py` — first E2E test for `eval run` (cited in A1 §6 Q2 as "does not exist"). Mock `_run_one_spec`, exercise the 0/1/3 exit paths.
- `tests/cli/eval/test_run_helpers.py` — direct unit tests for `_utc_iso_now`, `_compute_run_stats`, `_format_run_summary_line`, `_can_install_signal_handler`. Each helper is testable in isolation.
- The five existing skip-gated test files (`test_single_command.py`, `test_exit_codes.py`, `test_no_pty_exclusion.py`, `test_no_mcp_skip.py`, `test_validation_commands.py`) will un-skip automatically — they need verification, not authoring.

**Carry-forward items addressed?**
- **Click 8.3.2 `mix_stderr` at `test_eval_group.py:114`:** NO — orthogonal. (B2 should pair this with the helper-authoring sprint.)
- **D-0070/71/72/77 missing triplets:** NO — those are spec-artifact gaps, not code gaps.
- **OQ-2 sign-off:** PARTIAL — landing the exit-code constants satisfies the OQ-2 "RUN_*_EXIT_CODE values pinned" sub-question; the sign-off note still needs to be authored in `.dev/releases/current/cliEval/decisions.md`.

---

### Candidate C2 — **Lifted Aggregator (Promote to models.py + reporter.py)**

**One-sentence summary.** Promote `_compute_run_stats` to `RunCounts.from_outcomes` + `RunTotals.from_outcomes` classmethods on `models.py`, promote `_format_run_summary_line` to a `Reporter.format_operator_line(...)` method on `reporter.py`, keep `commands.py` thin-wrapper shims for test mockability.

**Approach class.** Hybrid split — heavy lifting lives in domain modules; `commands.py` keeps mockable surface.

**LOC estimate** (method: `models.py` gains 2 classmethods × ~8 LOC [16] + `reporter.py` gains 1 method × ~3 LOC [3] + `commands.py` thin shims × ~2 LOC each for #7 and #8 [4] + remaining 9 symbols as C1 [~45] + F401 cleanup as C1 ≈ **+68 / -12 / 0 moved**):

| Δ added | Δ removed | Δ moved |
|---|---|---|
| ~68 | ~12 | 0 |

**Files touched: 3** — `commands.py`, `models.py`, `reporter.py`.

**Per-symbol routing.**

| # | Symbol | Treatment | Home |
|---|---|---|---|
| 1-6, 9-11 | (same as C1) | (same as C1) | commands.py |
| 7 | `_compute_run_stats` | shim `def _compute_run_stats(outcomes, *, manifest_n): return RunCounts.from_outcomes(outcomes, manifest_n=manifest_n), RunTotals.from_outcomes(outcomes)` | commands.py shim; logic in models.py classmethods |
| 8 | `_format_run_summary_line` | shim `def _format_run_summary_line(summary, dir): return Reporter.format_operator_line(summary, dir)` | commands.py shim; logic in reporter.py |

**Fidelity to design-spec §4.** HIGH — same exit-code authoring as C1; additionally aligns with the DM-012 schema's "`RunCounts` and `RunTotals` are the canonical aggregation surface" framing (verdict §"Q5" notes design-spec is silent but the dataclass naming convention favors classmethods).

**Risk to FR-G1 ban-import contract.** LOW — `models.py` already exports `RunCounts` / `RunTotals`; adding classmethods does not introduce a new edge. `reporter.py` already consumes `RunSummary`; adding `format_operator_line` stays within its domain.

**Test-contract preservation.** PASS — `mock.patch("...commands._compute_run_stats", ...)` still resolves (the shim is a module attribute). BONUS — `RunCounts.from_outcomes` becomes independently unit-testable in `tests/cli/eval/test_models.py`, decoupling the aggregator tests from `commands.py`.

**Compatibility with already-landed P3/P4 surface.** Same as C1, with one addition: `Reporter.format_operator_line` is a net-new method but does not alter existing reporter contracts (FR-RPT1 unchanged; `to_markdown()` / `to_json()` / `to_yaml()` / `to_junit_xml()` untouched).

**New tests required.**
- All of C1's new tests, PLUS:
- `tests/cli/eval/test_models.py::test_run_counts_from_outcomes`
- `tests/cli/eval/test_models.py::test_run_totals_from_outcomes`
- `tests/cli/eval/test_reporter.py::test_format_operator_line`

**Carry-forward items addressed?**
- Click 8.3.2: NO.
- D-0070/71/72/77: NO.
- OQ-2: PARTIAL (same as C1) — but additionally resolves the verdict's open Q1 (Q5 from A1) by committing to classmethod placement. Recommend a one-line `.dev/releases/current/cliEval/decisions.md` entry.

---

### Candidate C3 — **`RunHelpers` Cohesion Class**

**One-sentence summary.** Introduce a single `class RunHelpers:` in `commands.py` that hosts all 11 symbols as classmethods / class attributes; `eval_run` consumes via `RunHelpers.new_run_id()`, `RunHelpers.run_one_spec(...)`, etc.

**Approach class.** In-place cohesion — wraps 11 symbols in one namespace for organizational clarity.

**LOC estimate** (method: 7 pure-T1 × ~5 LOC [35; classmethod adds @classmethod + cls arg overhead] + 4 HYBRID × ~6 LOC [24] + 3 class constants × 2 LOC [6] + class declaration + docstring [10] + 11 call-site rewrites at line 1467, 1469, 1577, 1598, 1612, 1624, 1636, 1642, 1671, 1677, 1694, 1695 × ~1 LOC delta each [12] + F401 cleanup [-12] ≈ **+87 / -12 / 0 moved**):

| Δ added | Δ removed | Δ moved |
|---|---|---|
| ~87 | ~12 | 0 |

**Files touched: 1** — `commands.py`.

**Per-symbol routing.**

| # | Symbol | Treatment | Home |
|---|---|---|---|
| 1-8 | classmethod `RunHelpers.<name>` | commands.py (class scope) |
| 9-11 | class attributes `RunHelpers.RUN_*_EXIT_CODE` | commands.py (class scope) |

**Fidelity to design-spec §4.** MEDIUM — constants land at correct values but as `RunHelpers.RUN_CLEAN_EXIT_CODE` rather than module-level. This **breaks the convention** of the eight existing `*_EXIT_CODE` constants (all module-level) and re-opens verdict-constraint C1 (constants in `commands.py`). Defensible only if a follow-up `RUN_CLEAN_EXIT_CODE = RunHelpers.RUN_CLEAN_EXIT_CODE` re-export is added — but at that point C1's flatter design wins.

**Risk to FR-G1 ban-import contract.** LOW — no new cross-module edges.

**Test-contract preservation.** **FAIL** — this is the killer issue. `mock.patch("...commands._run_one_spec", ...)` does NOT resolve, because `_run_one_spec` no longer exists as a module attribute. The mock path becomes `mock.patch("...commands.RunHelpers.run_one_spec", ...)`, which requires editing all five test files. C3 explicitly breaks verdict-constraint C2 and C5.

**Compatibility with already-landed P3/P4 surface.** PASS for non-test surface (Expect, FR-CLI1, FR-G4, FR-G5, OPS-003 untouched), but the test-contract breakage cascades to TEST-007/8/9 — all three would need rework.

**New tests required.** Same as C1, PLUS edits to all five existing skip-gated test files to patch `RunHelpers.run_one_spec` instead of `_run_one_spec`.

**Carry-forward items addressed?** Same as C1.

---

### Candidate C4 — **Direct Inlining (Zero Helpers)**

**One-sentence summary.** Rewrite `eval_run` to inline every call: hoist `started_iso = datetime.now(timezone.utc).isoformat(...).replace("+00:00", "Z")` to line 1466, replace `_new_run_id()` with `compose_run_id(started_iso, parsed.name)` directly, inline the aggregator math, inline the format string, hardcode the three exit-code integers at the `sys.exit()` sites.

**Approach class.** Maximalist consolidation — author zero new symbols; rewire all call sites to siblings and stdlib idioms.

**LOC estimate** (method: `eval_run` body delta: ~+5 LOC for inlined `started_iso` hoist + ISO format, ~+8 LOC for inlined aggregator counting passes, ~+1 LOC for inlined format string, 0 LOC for hardcoded `sys.exit(0/1/3)`, but suite-name closure for `_default_output_dir` requires capturing `parsed.name` which is computed at line 1512 — well after the run-id line 1467 needs it. Either hoist suite-name parse above the output-dir resolution, or fall back to `output_dir = output_dir or Path.cwd()` and defer run-dir composition to after suite parse [~+10 LOC of reordering]. F401 cleanup: all 12 imports removable except `datetime, timezone` which become used [-10]. ≈ **+24 / -10 / -8 moved [code shuffled by reordering]**):

| Δ added | Δ removed | Δ moved |
|---|---|---|
| ~24 | ~10 | ~8 (reorder) |

**Files touched: 1** — `commands.py`.

**Per-symbol routing.**

| # | Symbol | Treatment | Home |
|---|---|---|---|
| 1 | `_new_run_id` | inlined: `run_id = compose_run_id(started_iso, parsed.name)` | (call site only; symbol does not exist) |
| 2 | `_default_output_dir` | inlined: `requested_output = output_dir or compose_run_dir(Path.cwd(), started_iso, parsed.name)` | (call site only) |
| 3 | `_resolve_executor_factory` | inlined: `executor_factory = lambda: ClaudeProcessAdapter(...)` | (call site only) |
| 4 | `_run_one_spec` | **CANNOT BE INLINED** — five tests mock the module attribute by name. Either keep as helper (contradiction with "zero helpers") or accept five test-file rewrites. |
| 5 | `_utc_iso_now` | inlined twice (lines 1612, 1636) | (call site only) |
| 6 | `_can_install_signal_handler` | inlined: `if SignalHandlerInstaller is not None and threading.current_thread() is threading.main_thread():` | (call site only) |
| 7 | `_compute_run_stats` | inlined aggregation loops | (call site only) |
| 8 | `_format_run_summary_line` | inlined f-string at line 1671 | (call site only) |
| 9-11 | `RUN_*_EXIT_CODE` | hardcoded `sys.exit(0/1/3)` | (call site only) |

**Fidelity to design-spec §4.** MEDIUM — exit codes are correct integers but lose the named-constant convention. The eight existing `*_EXIT_CODE` constants establish the project pattern of named integers; hardcoding `sys.exit(0)` / `sys.exit(1)` / `sys.exit(3)` at 1676-1695 is stylistically inconsistent with the rest of `commands.py` and harder to grep.

**Risk to FR-G1 ban-import contract.** LOW.

**Test-contract preservation.** **FAIL** — same as C3 for `_run_one_spec` (cannot inline without breaking five test files). The `_t0410_missing()` probe at `test_exit_codes.py:93-113` and `_eval_run_body_incomplete()` at `test_single_command.py:148-160` will both report 11 missing names indefinitely because the names truly don't exist as module attributes; skip-gates will never evaporate. C4 explicitly breaks verdict-constraint C5.

**Compatibility with already-landed P3/P4 surface.** TEST-007/8/9 broken (same root cause as C3).

**New tests required.** `test_eval_run.py` E2E only; the existing five skip-gated files require **rewrites** to remove the `hasattr(cmds, name)` probes (else they never un-skip).

**Carry-forward items addressed?** Same as C1.

---

### Candidate C5 — **Surgical Patch (Minimum F821→0)**

**One-sentence summary.** Smallest possible diff that turns ruff F821 from 11→0: author the 11 symbols as one-line stubs / aliases (constants = integer literals; helpers = `pass` or `raise NotImplementedError`); defer real behavior to a follow-up phase.

**Approach class.** Stub-out — clears the ruff gate but does not satisfy runtime semantics.

**LOC estimate** (method: 8 helpers × 2 LOC stub [16] + 3 constants × 1 LOC [3] + F401 cleanup [-12] ≈ **+19 / -12 / 0**):

| Δ added | Δ removed | Δ moved |
|---|---|---|
| ~19 | ~12 | 0 |

**Files touched: 1** — `commands.py`.

**Per-symbol routing.**

| # | Symbol | Treatment | Home |
|---|---|---|---|
| 1-4 | `def _foo(...): raise NotImplementedError("T04.10 stub")` | commands.py |
| 5-8 | same | commands.py |
| 9-11 | correct integer literals (`= 0/1/3`) | commands.py |

**Fidelity to design-spec §4.** LOW for the helpers (zero runtime behavior — invoking `eval run` against any real fixture raises `NotImplementedError`); HIGH for the constants (correct integers). Net LOW.

**Risk to FR-G1 ban-import contract.** LOW (no new edges).

**Test-contract preservation.** **PARTIAL PASS** — `mock.patch("...commands._run_one_spec", ...)` resolves (symbol exists as module attribute). BUT: the `_t0410_missing()` probe uses `hasattr(cmds, name)` (which returns True for stubs) so skip-gates evaporate — and then the un-skipped tests immediately fail on `NotImplementedError`. C5 swaps a ruff-gate-red for a pytest-gate-red. Net regression on visible signal.

**Compatibility with already-landed P3/P4 surface.** PASS at the structural level but FAIL at the behavioral level: any caller of `eval run` crashes. Expect, FR-CLI1, FR-G4, FR-G5 all untouched but unreachable past line 1467.

**New tests required.** None (because no helper has real behavior to test). This is itself a red flag.

**Carry-forward items addressed?** None.

**B1's honest assessment of C5:** This is a non-starter unless the project's release-gate definition explicitly counts ruff-F821-clean as a higher-priority green than pytest-pass — which is the inverse of every release-gate convention surveyed in `phase1/A2-thesis-never-authored.md` §3. Listed for completeness only.

---

### Candidate C6 (B1 addition) — **Hybrid Split: Aggregator Promoted, Formatter Stays Local**

**One-sentence summary.** Like C2, but only promote `_compute_run_stats` to `models.py` classmethods (where the dataclasses already live and where a `from_outcomes` factory is a natural extension); keep `_format_run_summary_line` in `commands.py` (because reporter.py renders *whole documents*, not operator-stdout banners — different concern).

**Approach class.** Selective promotion — promote only where the sibling module's existing concern matches.

**LOC estimate** (method: `models.py` gains 2 classmethods × ~8 LOC [16] + `commands.py` thin shim for #7 [2] + remaining 10 symbols as C1 [~47] + F401 cleanup [-12] ≈ **+65 / -12 / 0**):

| Δ added | Δ removed | Δ moved |
|---|---|---|
| ~65 | ~12 | 0 |

**Files touched: 2** — `commands.py`, `models.py`.

**Per-symbol routing.** Like C2 for #7 (promote to classmethods); like C1 for #8 (`_format_run_summary_line` stays inline in `commands.py`); like C1 for all other rows.

**Fidelity to design-spec §4.** HIGH.

**Risk to FR-G1 ban-import contract.** LOW.

**Test-contract preservation.** PASS — shim preserves `mock.patch("...commands._compute_run_stats", ...)`.

**Compatibility with already-landed P3/P4 surface.** Same as C2 minus the reporter.py addition; strictly subset of C2's blast radius.

**New tests required.** Same as C1 plus `tests/cli/eval/test_models.py::test_run_counts_from_outcomes` and `test_run_totals_from_outcomes`.

**Carry-forward items addressed?** Same as C2 — partial OQ-2 resolution; closes Q1 in the direction of "classmethod for aggregator, inline for formatter."

**Why B1 added this.** C2 promotes both #7 and #8, which conflates two different sibling concerns — `RunCounts`/`RunTotals` is data-domain (perfect fit for a classmethod) while `_format_run_summary_line` is *operator-UX*-domain (poor fit for `reporter.py`, which renders whole document artifacts). C6 separates these to avoid the cross-domain reach that even C2 risks.

---

## 2. Ranking grid — churn × fidelity × risk

Scoring rubric: HIGH = costly/strong/safe; MED = moderate; LOW = cheap/weak/risky. (Churn LOW = cheap, fidelity HIGH = strong-spec-match, risk LOW = safe.) **Lower churn + higher fidelity + lower risk = better.**

| Candidate | Churn | Fidelity to §4 | Risk to verdict constraints | Composite verdict |
|---|---|---|---|---|
| **C1** Minimal in-place | **LOW** (~52+/12-, 1 file) | **HIGH** | **LOW** (no constraint violations) | **#1 — recommended** |
| **C6** Hybrid split (aggregator only) | MED (~65+/12-, 2 files) | **HIGH** | **LOW** | **#2 — recommended** |
| **C2** Lifted aggregator (both) | MED (~68+/12-, 3 files) | **HIGH** | LOW (largest surface but no constraint violations) | #3 |
| **C5** Surgical stub | LOW (~19+/12-, 1 file) | **LOW** (helpers crash at runtime) | MED (swaps ruff-red for pytest-red) | #4 |
| **C3** RunHelpers class | MED (~87+/12-, 1 file but +11 call-site rewrites) | MED (breaks `*_EXIT_CODE` convention) | **HIGH** (breaks C2 + C5 test-contract constraints) | #5 |
| **C4** Direct inlining | LOW (~24+/10-, 1 file) | MED (loses named-constant convention) | **HIGH** (breaks C2 + C5; cannot inline `_run_one_spec`) | #6 |

---

## 3. Top-2 recommendation for D1 / D2 elaboration

### Recommended: **C1 (Minimal In-Place)** for D1; **C6 (Hybrid Split, aggregator-only)** for D2

**Justification — three paragraphs.**

C1 is the dominant candidate on every axis the verdict pinned: smallest blast radius (one file, ~40 net LOC), zero risk to the five test-contract files (all 11 symbols remain `commands.py` module attributes per constraint C2 / C5), zero risk to FR-G1 (no new cross-module edges; the F401-staged sibling imports are exactly the consumption surface the HYBRID wrappers need), and exact alignment with design-spec §4 (constants land at the literal integers 0/1/3 with the established `*_EXIT_CODE` naming). It is also the only candidate whose follow-up obligations are entirely internal to the eval/ tree — no `models.py`, no `reporter.py` ripples — which keeps the P5 sprint gate's blast radius small. The CP-P04-END remediation language (*"either (a) author the eleven missing helper symbols … or (b) rewrite the body to use already-landed helpers"*) is literally satisfied by C1: the HYBRID wrappers are option (a)'s outer shape with option (b)'s inner body.

C6 is the strongest alternative because it forces a principled resolution of open-Q1 (`_compute_run_stats` home) by promoting *only* the row where the sibling module's existing concern is the exact aggregator surface needed. `RunCounts.from_outcomes` and `RunTotals.from_outcomes` are natural classmethods on the data-domain dataclasses that already live in `models.py` (lines 732, 786); pinning the aggregator there decouples its unit tests from `commands.py` and makes the aggregation logic independently testable in `tests/cli/eval/test_models.py`. C6 deliberately *does not* promote `_format_run_summary_line` (the operator-UX concern is a poor fit for `reporter.py`, which renders whole documents — different granularity), which keeps the candidate's blast radius modest (2 files vs C2's 3) while delivering the principal long-term benefit of decoupled aggregator tests. D2 should elaborate C6 to verify the classmethod signatures match the dataclass field surfaces cleanly and that no DM-012 schema invariant is invalidated.

The remaining candidates fail decisive constraints: C2 over-promotes by including the formatter (a domain mismatch for `reporter.py`); C3 fundamentally breaks the test-mock contract (`mock.patch("...commands._run_one_spec", ...)` cannot resolve once `_run_one_spec` becomes a `RunHelpers` classmethod); C4 inherits the same test-mock breakage and additionally cannot inline `_run_one_spec` at all (it's load-bearing for five test files); C5 swaps the ruff gate-red for a pytest gate-red, which is a net regression in observable signal. D1 + D2 elaborating C1 and C6 in parallel — with C6 specifically interrogating the classmethod-vs-shim trade — gives Phase 2B the right two-axis spread to red-team without either candidate carrying load-bearing test-contract risk.

---

## 4. Open-question answers

### Q1 — `_compute_run_stats` home + `_format_run_summary_line` home

**Recommendation.**
- `_compute_run_stats` → **promote to `RunCounts.from_outcomes` + `RunTotals.from_outcomes` classmethods on `models.py`**, with a thin `_compute_run_stats(outcomes, *, manifest_n)` shim in `commands.py` for test-mock continuity.
- `_format_run_summary_line` → **keep inline in `commands.py`**; do not promote.

**Rationale.** The aggregator's logical home is the data-domain module that already exports `RunCounts` + `RunTotals` (`models.py:732, 786`). Classmethods are the canonical Python pattern for "construct an instance from raw inputs," and the `to_dict()` methods on those same dataclasses (`models.py:763, 803`) establish the precedent that `RunCounts` / `RunTotals` already host their own serialization concerns. Promoting `from_outcomes` aligns with this established placement. By contrast, `_format_run_summary_line` is an *operator-stdout* concern (single-line banner under `--verbose` at commands.py:1671), not a *reporter-document* concern (multi-line `summary.md` / `summary.json` / `junit.xml` rendered by `reporter.py`). The reporter module's existing methods (`render_summary_yaml`, `render_summary_markdown`, `render_summary_json`, `render_junit_xml`) all produce whole documents at file-write granularity (A1 §4 row 8 evidence); the one-line CLI banner is a different shape. The thin shim for `_compute_run_stats` preserves the test-mocking surface verdict-constraint C5 requires — `mock.patch("...commands._compute_run_stats", ...)` still resolves to the module-attribute shim.

### Q2 — `_default_output_dir` + scratch-root allowlist

**Recommendation.** **No, the wrapper does NOT need to honor the scratch-root allowlist.** Author `_default_output_dir(run_id) -> Path` as a thin wrapper that returns `compose_run_dir(Path.cwd(), started_iso, suite_name)` (where `started_iso` is computed via `_utc_iso_now()` either inside the wrapper or hoisted to before line 1467). Allowlist enforcement is correctly placed at line 1473's `resolve_scratch_root(requested_output, config=base_config, output_dir=output_dir)` call — the wrapper produces a *candidate* path; `resolve_scratch_root` is the gatekeeper.

**Rationale.** The two-step pattern (compose candidate → validate against allowlist) is the existing design: line 1468 produces a candidate via either operator-supplied `output_dir` or `_default_output_dir(run_id)`; line 1473 unconditionally validates the candidate via `resolve_scratch_root`. Re-deriving allowlist semantics inside the wrapper would double-gate the path and create two enforcement surfaces (a Liskov-ish violation: the wrapper would behave differently depending on which call site invoked it). Operators who supply `--output-dir <path>` already produce arbitrary paths that `resolve_scratch_root` validates; the default path (computed `Path.cwd()`-rooted) should be no different. The only risk: in an unlikely environment where `Path.cwd()` is itself outside the canonical AC12 prefix, `resolve_scratch_root` would reject the default and the operator would see a `ScratchRootViolation` at line 1478 — which is the *correct* surfacing of the configuration mismatch, not a defect in the wrapper. (**INFERENTIAL** [confidence MED]: the verdict's "open Q4 scratch-root layering" is genuinely under-specified in the design-spec, but the existing `resolve_scratch_root` interposition pattern is the dominant project convention.)

### Q3 — `_new_run_id` API shape: zero-arg wrapper vs direct inlining

**Recommendation.** **Author the zero-arg wrapper `_new_run_id() -> str` (Option a).** Body: `return compose_run_id(_utc_iso_now(), parsed.name)` with a closure capture of `parsed.name` (or pass `suite_name` as an arg if the wrapper is hoisted above the suite-parse block — see implementation note).

**Rationale.** Three converging arguments:

1. **CP-P05-END remediation explicitly prescribes Option (a)** (`.dev/releases/current/cliEval/checkpoints/CP-P05-END.md:401-406`, quoted in verdict §"Per-symbol verdict table" row 1): *"replace the undefined call with `compose_run_id(started_at=_utc_iso_now(), suite_name=suite)` or author a thin `_new_run_id()` wrapper that delegates to `compose_run_id`."* The remediation document already endorses the wrapper shape.

2. **Test-mock surface preservation.** Five test files probe `hasattr(cmds, name)` for the 11 names including `_new_run_id`. Direct inlining (Option b) deletes the symbol, which leaves the `hasattr` probe returning False indefinitely — skip-gates never evaporate. The wrapper preserves the test-contract surface for free.

3. **Call-site ordering pragmatism.** The current call site is at line 1467, BEFORE `parsed.name` is available (suite-parse runs at lines 1504-1518). Either (i) the wrapper captures `parsed.name` from outer scope via closure (which means the wrapper must be defined INSIDE `eval_run` as a nested function), or (ii) the wrapper is defined at module scope and the run-id computation is hoisted to AFTER suite-parse. Option (i) is acceptable if `_new_run_id` is nested inside `eval_run` — but this conflicts with the test-mock requirement (mocks need a module attribute, not a nested function). Therefore: **author `_new_run_id` at module scope, accept that the call site must be reordered to fire AFTER suite-parse** — the run-id computation moves from line 1467 to ~line 1518, *after* `parsed = loader.load(manifest_path)`. The current `requested_output = ... else _default_output_dir(run_id)` at line 1469 likewise reorders to after suite-parse. **This is the cleanest path** and matches the eval_describe precedent (A4 Evidence G) of direct sibling-helper invocation at well-ordered call sites.

The `eval_describe` precedent argument for Option (b) is weaker than it appears: `eval_describe` calls siblings directly because no test mocks `commands._describe_helper` — there are no symbol-name probes in the describe test surface. The five-file mock-surface for `eval_run` makes its constraints structurally different from `eval_describe`'s. The wrapper is justified.

---

## 5. New open question B1 uncovered

**OQ-B1.1 — Should the F401 cleanup include removal of `os`, `secrets`, `Sequence`, plus the suspected fourth stale import, or are any of these load-bearing for code paths B1 did not survey?** A1 §2.2 reports 12 F401 unused imports total but the verdict's "8 sibling + 2 datetime + 3 stale (os, secrets, Sequence)" = 13 names, off-by-one. **INFERENTIAL** (confidence LOW): the discrepancy is likely (a) `Sequence` being part of the typing import line `from typing import Any, Callable, Iterable, Optional, Sequence` where one of `Iterable` / `Optional` is also unused but uncounted, or (b) one of the `.disk_budget` imports (`DEFAULT_DISK_BUDGET_MB` is imported at line 67 but not visibly used in the 1406-1695 body — needs verification). Phase 2A's D1 / D2 should resolve the exact F401 count from a fresh `ruff check --select F401 src/superclaude/cli/eval/commands.py` before authoring the import-block cleanup; an authored helper that consumes a previously-counted-as-stale import would silently leave the F401 count > 0 and re-fail the ruff gate.

---

## 6. Process notes

- Estimates are INFERENTIAL where flagged (LOC counts, classmethod-vs-shim trade weight). Each candidate's LOC estimate shows its counting method; an estimate stating "8 helpers × 2 LOC = 16" carries that decomposition for traceability.
- B1 did not consult the design-spec sections beyond §4 (exit codes), the runner.py / claude_process.py source (only the signatures quoted in A1 / A4 verbatim evidence), or `tests/cli/eval/test_*.py` directly (relied on A1 §1.1 and A4 Evidence H for test-file diction). D1 / D2 elaboration must verify against the live files before committing to signatures.
- Read-only artifact — no source-tree edits performed.
- Candidate count: 5 + 1 (B1's C6 addition) = 6, exceeding the ≥5 floor.

---

## 7. Return summary (≤200 words)

**(a) Candidates.**
- **C1 Minimal In-Place** — author all 11 inline in commands.py; smallest blast radius.
- **C2 Lifted Aggregator** — promote `_compute_run_stats` + `_format_run_summary_line` to models.py / reporter.py with mockable shims.
- **C3 RunHelpers Class** — wrap all 11 in a cohesion class; breaks test-mock surface.
- **C4 Direct Inlining** — zero new helpers; cannot inline `_run_one_spec` (test-contract collision).
- **C5 Surgical Stub** — `NotImplementedError` stubs to clear ruff F821; swaps ruff-red for pytest-red.
- **C6 Hybrid Split (aggregator-only)** — promote only `_compute_run_stats` to models.py classmethods; keep formatter inline.

**(b) Top-2 for D1/D2.**
- **D1 → C1** — minimum-risk, exact-fidelity, smallest LOC delta; satisfies every verdict constraint.
- **D2 → C6** — principled aggregator placement on models.py classmethods; selective promotion avoids C2's over-reach into reporter.py.

**(c) Open-question answers.**
- **Q1:** Aggregator → classmethods on models.py with commands.py shim; formatter → stay inline.
- **Q2:** Wrapper does not need allowlist awareness; `resolve_scratch_root` at line 1473 is the existing single enforcement surface.
- **Q3:** Zero-arg wrapper `_new_run_id()` with module-scope authoring + call-site reorder to post-suite-parse; matches CP-P05-END remediation and preserves test-mock surface.

**(d) New open question.** OQ-B1.1 — exact F401 count needs fresh ruff probe before import-block cleanup (verdict's "8+2+3=13" is off-by-one against A1's "12 total").
