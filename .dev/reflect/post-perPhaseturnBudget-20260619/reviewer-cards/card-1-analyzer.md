# Reviewer Card 1 — Analyzer (spec-compliance lens R-1..R-10)

- **Mode:** `/sc:reflect --mode post --depth deep`, Tier-2 ensemble, REVIEWER 1 (analyzer persona, adversarial)
- **Spec (authoritative):** `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md` (v3, reflect-validated)
- **Implementation audited:** diff vs HEAD `33cc85ab` on `executor.py`, `models.py`, `kpi.py` (verify-unchanged), `commands.py` (verify-unchanged)
- **Method:** `git diff HEAD` + live Reads; constructs re-located by content (Phase-2 edits shifted line numbers ~+120 from spec anchors). All `file:line` below are LIVE worktree positions as of this audit.

---

## Per-R-item verdict

| R | Verdict | Evidence (live file:line) |
|---|---------|---------------------------|
| **R-1 — remove global pre-loop ledger** | **CONFORMANT** | Global `TurnLedger(initial_budget=config.max_turns * len(config.active_phases), ...)` is deleted. `grep len(config.active_phases)` now matches ONLY a comment (`executor.py:1826`), never a construction. Exactly ONE `TurnLedger(` remains in executor (`executor.py:1920`). Neighbors kept pre-loop: `shadow_metrics` (`1832`), `remediation_log` (import @`1844`), `SprintGatePolicy`/`all_gate_results` unmoved. No stray executable `ledger` reference between deletion site and `1920` (only comment-text mentions). |
| **R-2 — fresh phase-sized ledger at tasks-resolution** | **CONFORMANT** | `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), reimbursement_rate=0.8)` at `executor.py:1920-1923`, placed AFTER `tasks = _parse_phase_tasks(phase, config)` (`1898`) and BEFORE `if tasks:` (`1924`). `else 1` floor present. K-2 sequential-phase invariant comment present (`executor.py:1912-1919`). |
| **R-3 — per-phase available == max_turns × task_count** | **CONFORMANT** | Sizing input `executor.py:1920-1921`; `available()` formula `models.py:1052-1054` unchanged (`initial_budget - consumed + reimbursed`). Fresh object per phase ⇒ `consumed==0` at entry by construction. |
| **R-4 — independence (reimbursement+wiring start at 0)** | **CONFORMANT** | `TurnLedger` dataclass defaults all 0: `consumed`/`reimbursed`/`wiring_turns_used`/`wiring_turns_credited`/`wiring_analyses_count`/`wiring_budget_exhausted` (`models.py:1034-1046`). Fresh construction each phase ⇒ defaults restored. |
| **R-5 — gate unchanged in code; comments only** | **CONFORMANT** | Gate statement `if ledger is not None and not ledger.try_launch():` byte-identical HEAD↔live (parallel `executor.py:1276`, sequential `1473`); only line numbers shifted. Comment/log strings updated to "phase budget exhausted" semantics (`executor.py:1265-1272`, `1459-1463`). No executable change. |
| **R-6 — legacy subprocess execution unchanged; ledger input per-phase, documented** | **CONFORMANT** | NO executable change to subprocess path (grep over diff for `ClaudeProcess`/`SessionReset`/`isolation`/`launch`/`monitor`/`exit_code` matches only docstring/comment prose). Inline delta comment at legacy call-site (`executor.py:2376-2385`). Wiring-hook docstring delta present in `run_post_phase_wiring_hook` (`executor.py:829-841`). Both inline+docstring requirement satisfied. |
| **R-7 — models.py docstring-only; no reset mutator** | **CONFORMANT** | Class docstring tightened to per-instance monotonicity (`models.py:1018-1025`). `grep "def reset|def reallocate"` → NONE. No method/field added (only docstring lines in diff). |
| **R-8 — python/skip phases construct no ledger** | **CONFORMANT** | Construction (`1920`) sits after python `continue` (`executor.py:1880`) and skip `continue` (`1894`); those phases never reach `1920`. |
| **R-9 — thread-safety K>1** | **CONFORMANT** | Ledger built in parent thread (`1920`) before fan-out; `_lock` in `__post_init__` (`models.py:1046-1051`). Serial `for phase` loop (`executor.py:1873`) constructs next ledger only after prior phase returns. K-2 invariant stated in construction comment (`1912-1919`). |
| **R-10 — sprint-cumulative wiring accumulator (OQ-1 Position A)** | **CONFORMANT** | `_SprintWiringTotals` dataclass with exactly 3 int fields (`executor.py:336-360`); constructed pre-loop adjacent to `shadow_metrics` (`executor.py:1842`, immediately after `shadow_metrics` @`1832`); 2 add-sites — task path (`2009-2013`) after task wiring hook, legacy path (`2400-2404`) after legacy wiring hook; arg-swap `turn_ledger=sprint_wiring_totals` (`executor.py:2543`, was `turn_ledger=ledger`). Read-only summation (per-phase ledger not mutated). NEVER read by `try_launch`/`available`/`can_run_wiring_gate` (those are `TurnLedger` methods at `models.py:1074/1052/1128`; accumulator is a distinct type). Attribute names `wiring_turns_used`/`wiring_turns_credited`/`wiring_analyses_count` match kpi.py reader contract (`kpi.py:193/195/197`). |

### Contract-preservation (C1-C3)
- **C1 — `--max-turns` help unchanged:** CONFORMANT. `commands.py` diff empty; help verbatim `"Max agent turns per phase (default: 100)"` (`commands.py:88-93`).
- **C2 — legacy subprocess execution preserved:** CONFORMANT (see R-6).
- **C3 — `gate-kpi-report.md` sprint-cumulative wiring:** CONFORMANT. kpi.py diff empty; reader at `kpi.py:191-197` consumes the accumulator unchanged; accumulator restores sprint-cumulative totals.

### §7 Blast-Radius
- One statement deleted (global construction), one added (per-phase construction), small accumulator (1 dataclass + 1 construction + 2×3-stmt add-sites + 1 arg swap), comment/docstring touch-ups. `TurnLedger` model unmodified (only docstring). **Matches §7 within the 4 audited files.** One out-of-scope file change noted below (D-1).

### K-1 / K-2 / K-3
- **K-1** (legacy wiring delta): documented inline + docstring (R-6). CONFORMANT.
- **K-2** (sequential-phase invariant): stated in construction-site comment (`executor.py:1912-1919`). CONFORMANT.
- **K-3** (pre-merge grep): process step, not code — see Grounding Gap GG-1.

---

## Deviation list (adversarial stance — every divergence classified)

| # | file:line | Class | Rationale | Signals matched |
|---|-----------|-------|-----------|-----------------|
| **D-1** | `pyproject.toml:144` (`"regression: Mandatory regression-gate tests..."`) | **Necessary deviation** | TM-0 mandates `@pytest.mark.regression` (used at `tests/sprint/test_per_phase_budget.py:175`). Pytest warns/errors on unregistered markers, so registering it is forced to satisfy the spec's own TM-0. Documented inline; contradicts no acceptance criterion. BUT `pyproject.toml` is NOT in the §7 blast-radius table — a divergence from the spec's stated edit surface, hence classified (not silent: the marker description names TM-0). | forced-by-constraint ✓; documented-inline ✓; contradicts-no-criterion ✓; outside-stated-blast-radius ✓ |
| **D-2** | `executor.py:336-360` (`class _SprintWiringTotals` at module scope) | **Necessary deviation** | §7/R-10 anchor the accumulator *construction* "@1782" (satisfied @`1842` live). The *class definition* is at module top-level, not pre-loop. A `@dataclass` cannot be defined inside a function and reused as the documented "~1 class" option without module scope. Spec §7 explicitly offered "~1 class OR 3 fields"; choosing the class form forces module-scope definition. No criterion addresses class location. | forced-by-language-idiom ✓; spec-authorized option ✓; contradicts-no-criterion ✓ |
| **D-3** | `executor.py:2009-2013` & `2400-2404` (add-site uses `wiring_analyses_count`, KPIReport field is `wiring_analyses_run`) | **Drift (cosmetic, benign)** | Spec R-10/§5-C3 names the persisted KPI field `wiring_analyses_run`; the accumulator + reader path uses `wiring_analyses_count` as the read attribute and `build_kpi_report` assigns it to `report.wiring_analyses_run` (`kpi.py:197`). The naming asymmetry (count vs run) is pre-existing in kpi.py and faithfully matched — but the spec prose conflates the two names. Silent in the sense that no inline note flags the count→run rename; however it contradicts no behavior and the persisted field name is correct. Borderline conformant; flagged for completeness, not severity. | not-in-spec-naming ✓; no-inline-rationale-for-rename ✓; contradicts-no-criterion ✓; behavior-correct ✓ |

**No Regressions found.** No spec acceptance criterion, explicit constraint, or previously-passing test is contradicted by the audited diff. The gate code is byte-identical (R-5), the subprocess execution path is untouched (R-6/C2), the budget stays strictly per-phase (R-3/R-4), and the KPI accumulator restores — does not collapse — sprint-cumulative telemetry (R-10/C3/D-4 resolved).

**No Authorized-expansion deviations** beyond what the spec itself pre-authorized (R-10's "class OR 3 fields" and "accumulator OR thin param" choices were taken as authorized → conformant, not expansion).

---

## Grounding Gaps (cannot classify for lack of in-scope evidence)

- **GG-1 — K-3 pre-merge grep.** §8 K-3 mandates re-running `grep -rn "\.wiring_turns\|\.wiring_analyses\|turn_ledger=" src/superclaude/cli/sprint` immediately before merge. This is a process step, not a code artifact; it cannot be verified from the diff. Not a code deviation. (Live grep during this audit found the only post-loop ledger-wiring consumer remains `kpi.py:191-197` via `executor.py:2543` — consistent with the spec's review-time statement.)
- **GG-2 — Test-matrix correctness (TM-0..TM-14).** `tests/sprint/test_per_phase_budget.py` (30 KB) and modified `test_models.py`/`test_multi_phase.py`/`test_turn_ledger_concurrency.py` EXIST, satisfying the spec's "NEW" file requirement structurally. I did not execute the suite or audit each TM assertion for semantic fidelity (outside the 4-file code-compliance scope assigned to this reviewer). Test *presence* is confirmed; test *adequacy* is deferred to the qa-lens reviewer.

---

## [INFERRED] (non-cited / reasoned claims)

- [INFERRED] D-1 severity is low: a missing marker registration would only surface as a pytest warning, not a behavioral regression; the spec's TM-0 requirement effectively *implies* the registration even though §7 omits it. Inference, not a cited spec line.
- [INFERRED] D-2 and D-3 are de-facto conformant; I classify them as "Necessary deviation" / benign "Drift" only to honor the adversarial mandate to surface every divergence-from-literal-spec-text. A non-adversarial read would mark all three CONFORMANT.
- [INFERRED] The implementation chose accumulator-as-`turn_ledger`-arg over the "thin wiring-totals param" alternative; both were spec-authorized, so this is a design choice, not a deviation. (Spec R-10 "either is acceptable.")

---

## Calibrated self-confidence: **0.88**

Rationale: All 10 R-items, C1-C3, §7, and K-1/K-2 verified against live code with exact citations; kpi.py/commands.py confirmed byte-unchanged. Confidence is held below 0.95 because (a) I did not execute the test suite or audit TM-0..TM-14 assertion semantics (GG-2), and (b) the three flagged deviations are borderline — a reasonable reviewer could mark them conformant, so the deviation count carries calibration risk.

---

**One-line verdict:** Implementation is spec-conformant across R-1..R-10 / C1-C3 / §7 / K-1-K-2 with ZERO regressions; the only divergences are one Necessary deviation outside the stated blast radius (`pyproject.toml` regression-marker registration, forced by TM-0), one idiom-forced class-scope placement, and one benign `count`/`run` naming drift — none of which contradict any acceptance criterion.
