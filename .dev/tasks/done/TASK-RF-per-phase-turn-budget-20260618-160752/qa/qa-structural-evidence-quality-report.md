# QA Report — Report Validation (Structural / Evidence-Quality / No-Overreach Lens)

**Topic:** Per-Phase Turn-Budget Model for the Sprint Runner
**Date:** 2026-06-18
**Phase:** report-validation (final QA gate, evidence-quality / blast-radius lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY — no edits made)
**Lens:** Did the implementation change MORE than spec §7 Blast-Radius authorized?

**Spec under test:** `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md` §7 (v3, reflect-validated)
**Files bounded:** `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/models.py`, `pyproject.toml`, 3 modified test files, 1 new untracked test file

---

## Overall Verdict: PASS (no overreach found — implementation is within authorized blast radius)

The prompt instructed me to assume ≥5 places where the implementation changed more than the
spec authorized, and to find them. After exhaustively bounding the change with `git diff`,
`git diff --numstat`, and non-comment/non-docstring line extraction, **I could not substantiate
5 (or any) CRITICAL behavioral overreaches.** Every executable change maps 1:1 to an authorized
spec requirement (R-1, R-2, R-6, R-7, R-8, R-10). The two supporting changes (pytest `regression`
marker; TM-11 `pytest.raises(SystemExit)` wrapper) are minimal and justified, not overreach.

A false FAIL is not better than an honest PASS when the evidence is this tight: the gate control
flow is byte-identical, `TurnLedger` gained no method and no field, the legacy subprocess body
is untouched, and the accumulator is provably never read by any gating predicate. I record below
the **4 sub-CRITICAL observations** (all MINOR / INFO), none of which constitute a behavioral
change beyond the blast radius.

---

## Blast-Radius Conformance (spec §7 table vs. actual change)

| Spec §7 site | Authorized nature | Actual change | Evidence | Verdict |
|---|---|---|---|---|
| Remove global construction `executor.py:1777-1780` | delete 1 statement (keep neighbors) | `ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases), ...)` deleted; `shadow_metrics`/`remediation_log`/`SprintGatePolicy`/`all_gate_results` retained pre-loop | diff hunk @1772-1821; `grep len(config.active_phases)` → 0 ledger constructions remain | PASS — exact |
| Add per-phase construction `executor.py:1838-1839` | add 1 statement (both branches) + K-2 comment | `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), ...)` after `tasks = _parse_phase_tasks(...)`, before `if tasks:`, AFTER skip/python `continue` (line 1894→1896) | diff hunk @1896-1920; `sed 1888-1900` confirms placement after skip `continue` | PASS — exact, `else 1` floor present |
| Gate `executor.py:1231-1235`, `1424-1430` | comment/log string ONLY | both gate hunks add ONLY comment lines; the `if ledger is not None and not ledger.try_launch():` predicate is byte-identical | diff hunks @1265 and @1459; no `+`/`-` on the `if` line | PASS — R-5 satisfied, no control-flow change |
| Legacy wiring input `executor.py:2281-2287` | no code change; document delta | comment block added above the `run_post_phase_wiring_hook(...)` call; the call args (`ledger=ledger`) unchanged | diff hunk @2376-2392 | PASS — R-6 satisfied |
| KPI wiring accumulator (R-10) | ~1 class or 3 fields + 2 add-sites + 1 arg swap; read-only | `_SprintWiringTotals` dataclass (3 int fields), 1 construction @1842, 6 `+=` lines across 2 add-sites (@2009-2013 task, @2400-2404 legacy), 1 arg swap `turn_ledger=ledger`→`turn_ledger=sprint_wiring_totals` @2543 | `grep sprint_wiring_totals` → 8 hits total, all read-only summation or construction/arg | PASS — exact match to authorized shape |
| `TurnLedger` model `models.py:1011-1124` | UNCHANGED (no new method) | 8 added lines, ALL inside the class docstring; 0 executable lines changed; no new method, no new field | `git diff models.py` non-`+++/---` lines are all docstring prose | PASS — R-7 satisfied (docstring-only) |

**Net actual change** = one statement deleted + one statement added + one read-only accumulator
(1 dataclass + 1 construction + 2 add-sites + 1 arg-swap) + comment/log/docstring touch-ups +
test suite. **This is byte-for-byte the spec's stated net.**

---

## Targeted Invariant Verification (the load-bearing claims from the prompt)

| Claim to disprove | Method | Result |
|---|---|---|
| Gate control flow CHANGED (R-5 violation) | extracted all non-comment `+`/`-` lines from executor diff; inspected both gate hunks | DISPROVEN. The only `+`/`-` near both gates are comment lines. `if ledger is not None and not ledger.try_launch():` is unchanged on both the parallel (@1276) and sequential (@1473) paths. |
| `TurnLedger` gained a method or field (R-7 violation) | `git diff models.py` filtered to non-`+++/---`; full Read of models.py:1011-1133 | DISPROVEN. All 8 added lines are docstring prose between the existing class docstring and the `Wiring analysis budget fields` block. Fields list (1032-1042) and method set (`available`/`debit`/`credit`/`can_launch`/`try_launch`/`can_remediate`/`debit_wiring`/`credit_wiring`/`can_run_wiring_gate`) are unchanged. 0 executable lines. |
| Legacy subprocess execution path changed (R-6 violation) | grep executor diff for `Popen|SessionResetPolicy|isolation|ClaudeProcess|monitor|launch|PhaseResult(` among `+`/`-` lines | DISPROVEN. Zero executable legacy-subprocess lines touched. The only matches are comment/docstring prose mentioning "subprocess". The `ledger=ledger` arg into the wiring hook is the same variable name (now bound to the per-phase ledger) — the intended R-6 wiring-input delta, not an execution-path change. |
| Accumulator is read by `try_launch`/`available`/`can_run_wiring_gate` (would reintroduce shared pool) | `grep sprint_wiring_totals` (8 hits) + `grep try_launch/.available()/can_run_wiring_gate` | DISPROVEN. `sprint_wiring_totals` appears ONLY at: construction (1842), 6 read-only `+=` accumulation lines (2009-2013, 2400-2404), and the `build_kpi_report` arg swap (2543). It is passed to NO gating predicate. Every gate read (`try_launch` @1276/@1473, `available()` @987/@1909-comment, `can_run_wiring_gate` @555) operates on `ledger`, never the accumulator. |
| Accumulator field names mismatch the kpi.py read contract | Read kpi.py:151-202 | CONFIRMED MATCH. kpi.py:193/195/197 reads `turn_ledger.wiring_turns_used` / `.wiring_turns_credited` / `.wiring_analyses_count`. `_SprintWiringTotals` defines exactly those three names. The report's output field `wiring_analyses_run` (kpi.py:197 LHS `report.wiring_analyses_run`) is the GateKPIReport output name, correctly sourced from `.wiring_analyses_count` — no contract break. |
| `else 1` floor missing (could yield `initial_budget=0` on legacy) | inspected per-phase construction hunk | CONFIRMED PRESENT. `initial_budget=config.max_turns * (len(tasks) if tasks else 1)` floors the legacy path to `max_turns × 1`. R-2 satisfied. |
| Per-phase construction placed BEFORE skip/python `continue` (R-8 violation) | `sed 1888-1900` | DISPROVEN. The skip `continue` is at line 1894; the per-phase ledger construction begins at line ~1896 (after the comment). python/skip phases `continue` before reaching it and allocate no ledger. R-8 satisfied. |

---

## Supporting Changes — Minimal / Justified vs. Overreach

### Supporting change 1 — pyproject.toml `regression` marker registration
- **Diff:** one line added to `[tool.pytest.ini_options] markers`: `"regression: Mandatory regression-gate tests (e.g. TM-0 per-phase turn-budget starvation guard)"` (`git diff pyproject.toml`, numstat `1 0`).
- **Necessity:** TM-0 is the mandatory regression gate (spec §6, `@pytest.mark.regression`). pytest emits `PytestUnknownMarkWarning` (and errors under `-W error` / `filterwarnings=error` configs) for unregistered markers. The new `tests/sprint/test_per_phase_budget.py` uses `@pytest.mark.regression`, so the marker MUST be registered for the suite to run clean.
- **Minimality:** single additive line, mirrors the existing `p0`/`recovery`/`autonomy` marker registration pattern in the same block. No existing marker altered.
- **Verdict:** JUSTIFIED, minimal, in-scope. Not overreach.

### Supporting change 2 — TM-11 `pytest.raises(SystemExit)` wrapper
- **Diff:** `tests/sprint/test_per_phase_budget.py:583` wraps `execute_sprint(config)` in `with pytest.raises(SystemExit):`, with an explanatory comment at 579-581 ("a skip+python+task mix where the task phase has no real subprocess ends ERROR → SystemExit(1)... orthogonal to TM-11's TurnLedger.__init__ spy assertions").
- **Necessity:** `execute_sprint` raises `SystemExit(1)` on a non-success sprint outcome (the ERROR phase produces a non-`is_success` status). TM-11's actual assertion is "exactly one `TurnLedger.__init__` construction" — the spy at `patch.object(TurnLedger, "__init__", _counting_init)` (line 566). Without the `pytest.raises` wrapper the test would error on the SystemExit before reaching its assertions. The wrapper is test-harness plumbing, not a behavioral change to product code.
- **Minimality:** confined to the test; does not weaken the TM-11 assertion (the `__init__` count check still runs after the context manager). The comment explicitly scopes the SystemExit as orthogonal.
- **Verdict:** JUSTIFIED, minimal, test-only. Not overreach. (Note: this test file is UNTRACKED — see Observation O-2.)

---

## Issues Found (all sub-CRITICAL)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| O-1 | MINOR | `executor.py:1816` (comment) | The header comment was edited from `(T01–T06)` to `(T02–T06)` to reflect the removed T01 ledger construction. Accurate, but the deleted-T01 rationale now lives only in the replacement comment block — fine, just noting the comment renumber is a deliberate touch-up within the authorized "comment touch-ups" allowance. | None required (informational); confirms comment edits stayed in scope. |
| O-2 | INFO | `tests/sprint/test_per_phase_budget.py` (763 lines, untracked) | The primary new test file (TM-0/1/5/8/9/10/11/13/14) is git-UNTRACKED. It is not part of the working-tree DIFF, so a reviewer reading only `git diff` would not see ~763 lines of new test coverage. This is expected for a new file but must be `git add`-ed before commit or the regression gate ships untested. | Ensure `git add tests/sprint/test_per_phase_budget.py` before commit. NOT a product overreach. |
| O-3 | MINOR | `executor.py:2376-2392` (legacy wiring comment) + spec §6 K-1 | The legacy-path comment asserts the wiring-input delta "is pinned by TM-13". TM-13 (per spec §6) is the multi-phase wiring-accumulation test; whether TM-13 in the untracked test file actually exercises a LEGACY phase (vs. two task phases) determines if the K-1 legacy delta is truly pinned. This lens did not read the untracked test body line-by-line for that specific coverage. | Out of this lens's verified scope — flag for the test-coverage QA lens to confirm TM-13 includes a legacy phase. UNVERIFIABLE here. |
| O-4 | INFO | `executor.py` two add-sites (@2009-2013, @2400-2404) | The two accumulation add-sites are duplicated 3-line `+=` blocks (task path and legacy path). This is intentional per spec R-10 ("task path after the hook ~L1917, legacy path after the hook ~L2287") — every phase type must contribute. Not DRY, but spec-mandated and read-only; extracting a helper would exceed the authorized blast radius. | None — duplication is spec-authorized; consolidating would itself be overreach. |

---

## Confidence Gate

- **Confidence:** Verified: 12/13 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0%
  (12 of 13 lens checks verified with tool evidence; 1 — O-3 TM-13 legacy-phase coverage — is
  UNVERIFIABLE within this structural/blast-radius lens because it requires reading the untracked
  test body for behavioral coverage, which belongs to the test-coverage lens. confidence =
  12 / (13 − 1) × 100 = 100%.)
- **Tool engagement:** Read: 4 | Grep: 6 | Glob: 0 | Bash: 7 (git diff/status/numstat/grep/sed)
- **Unchecked items:** none.
- **Unverifiable items:** O-3 — whether the untracked TM-13 test exercises a legacy phase (blocker:
  requires behavioral read of untracked test body; out of structural-lens scope).

---

## Self-Audit

If I told the user I found 0 CRITICAL overreaches, would they believe me? Evidence I can cite:
(1) extracted EVERY non-comment/non-docstring `+`/`-` line from the executor diff — the executable
delta is exactly delete-one + add-accumulator + add-per-phase-ledger + 6 `+=` + 1 arg-swap;
(2) `git diff models.py` filtered to prove all 8 added lines are docstring prose (0 executable);
(3) grep proved `sprint_wiring_totals` reaches no gating predicate; (4) grep proved no
Popen/isolation/SessionResetPolicy/launch line was touched; (5) Read kpi.py:151-202 to confirm the
3-field read contract matches the accumulator. The prompt's "assume ≥5 overreaches" framing is an
adversarial prior; the evidence does not support it, and inventing CRITICALs to satisfy the prior
would be the dishonest outcome. The change is unusually disciplined.

---

## QA Complete

**Overall Verdict: PASS — the implementation is within the spec §7 authorized blast radius. No behavioral change beyond it was found. Zero CRITICAL findings; 4 sub-CRITICAL observations (2 MINOR, 2 INFO), none of which are overreach.**
