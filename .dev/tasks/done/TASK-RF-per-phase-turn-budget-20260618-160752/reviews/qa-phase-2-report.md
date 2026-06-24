# QA Report — Phase-Gate Verification: Phase 2 (Source Edits to executor.py)

**Task:** TASK-RF-per-phase-turn-budget-20260618-160752
**Topic:** Per-Phase Turn-Budget Model for the Sprint Runner (R-1..R-10)
**Date:** 2026-06-18
**Phase:** task-integrity / phase-gate (Phase 2, Steps 2.1–2.8)
**Fix authorization:** true (fix in-place, no behavior beyond authorized blast radius)
**Stance:** Adversarial / zero-trust — every claim verified against actual current code.

**Files in scope:**
1. `src/superclaude/cli/sprint/executor.py` (all Phase 2 edits)
2. `.dev/tasks/.../phase-outputs/reviews/r9-threadsafety-confirmation.md` (R-9 note)

**Cross-reference invariants (NOT to be modified by Phase 2):**
- `src/superclaude/cli/sprint/models.py` — `TurnLedger` model MUST be unchanged.
- `src/superclaude/cli/sprint/kpi.py:192-197` — accumulator read contract.

---

## Pre-flight evidence

- `git diff --stat src/superclaude/cli/sprint/`: ONLY `executor.py` changed (135 insertions, 9 deletions). `models.py` and `kpi.py` show NO modifications. ✅ Blast-radius file-scope respected; models.py untouched.
- `git status --porcelain src/superclaude/cli/sprint/models.py`: empty (clean). ✅
- `uv run python -c "import ast; ast.parse(...)"`: executor.py PARSES OK. ✅
- `grep -n "TurnLedger("` in executor.py: exactly ONE construction remains, @1920. ✅
- `grep -n "len(config.active_phases)"` in executor.py: only @1826 (a COMMENT, not a construction). ✅

---

## Per-R-Item Verification (zero-trust, file:line evidence)

### R-1 (Step 2.1) — Delete global pre-loop ledger — **PASS**
- The global `ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases), reimbursement_rate=0.8)` is **DELETED**. Git diff confirms the exact `-` removal of the former `executor.py:1777-1780` construction (old `T01 (BUG-001/P0)` block).
- `grep -n "TurnLedger("` → exactly ONE construction remains, at `executor.py:1920` (the per-phase one). No global construction survives.
- `grep -n "len(config.active_phases)"` → sole hit is `executor.py:1826`, which is a COMMENT inside the R-1 explanatory block ("formerly sized config.max_turns * len(config.active_phases) was REMOVED"). NOT a ledger construction. Acceptable per the criteria (comment text mentioning the words is allowed).
- Pre-loop neighbors all remain pre-loop and intact: `shadow_metrics = ShadowGateMetrics()` @1832; `remediation_log = DeferredRemediationLog(...)` @1846-1848; `SprintGatePolicy(config)` @1853; `all_gate_results: list[TrailingGateResult] = []` @1856. None moved into the loop.
- No `ledger =` construction or `ledger.`/`ledger=` usage exists between the deletion site (former 1780) and the new construction at @1920. The first `ledger`-token after the pre-loop block is the new construction @1920; the loop opens @1873 and the construction is at @1920 — verified by the full diff (no intervening ledger usage). PASS.

### R-10 construction (Step 2.2) — sprint-level accumulator pre-loop — **PASS**
- Dataclass `_SprintWiringTotals` defined @335-357 with EXACTLY three int counters defaulting to 0: `wiring_turns_used: int = 0` @355, `wiring_turns_credited: int = 0` @356, `wiring_analyses_count: int = 0` @357.
- Instance `sprint_wiring_totals = _SprintWiringTotals()` constructed @1842, IMMEDIATELY adjacent to `shadow_metrics = ShadowGateMetrics()` @1832 (separated only by the R-10 explanatory comment), pre-loop (loop opens @1873). PASS.
- **Attribute-name read-contract match (CRITICAL):** verified against `kpi.py:192-197` by reading kpi.py directly: `report.wiring_turns_used = turn_ledger.wiring_turns_used` @193; `report.wiring_turns_credited = max(0, turn_ledger.wiring_turns_credited)` @195; `report.wiring_analyses_run = turn_ledger.wiring_analyses_count` @197. All three names (`wiring_turns_used`, `wiring_turns_credited`, `wiring_analyses_count`) match the dataclass fields EXACTLY. PASS.
- Accumulator is NEVER referenced by `try_launch`/`available()`/`can_run_wiring_gate`: the only `sprint_wiring_totals` references are construction @1842, the two read-only add-sites @2009-2014 / @2400-2405, and the arg-swap @2543. No gate path touches it. PASS.

### R-2 / R-3 / R-8 (Step 2.3) — fresh per-phase ledger at tasks-resolution point — **PASS**
- Construction `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), reimbursement_rate=0.8)` @1920-1923.
- Placement: AFTER python `continue` guard (@1879-1880) and skip `continue` guard (@1883-1894); IMMEDIATELY after `tasks = _parse_phase_tasks(phase, config)` @1898; BEFORE `if tasks:` @1924. PASS.
- `else 1` floor present **verbatim**: `(len(tasks) if tasks else 1)` @1921. PASS.
- K-2 sequential-phase invariant comment present at construction site @1912-1919 (header `K-2 SEQUENTIAL-PHASE INVARIANT (load-bearing precondition for R-9)`). States serial phase execution + intra-phase fan-out + future-overlap caveat. PASS.
- Binds `ledger` for BOTH branches: task branch `ledger=ledger` into `execute_phase_tasks` @1945; legacy branch `ledger=ledger` into `run_post_phase_wiring_hook` @2392. PASS.
- python/skip phases never reach construction: both `continue` before @1898/@1920. R-8 satisfied. PASS.

### R-5 (Step 2.4) — gate redefined as safety net, comment/string ONLY — **PASS**
- Parallel gate: comment changed to `PHASE-BUDGET SAFETY NET (R-5)` @1268-1275; conditional `if ledger is not None and not ledger.try_launch():` @1276 byte-identical; SKIPPED branch @1277-1286 unchanged.
- Sequential gate: comment changed to `PHASE-BUDGET SAFETY NET (R-5)` @1462-1472; conditional @1473 byte-identical; remaining + SKIPPED branch @1474-1484 unchanged.
- Git diff confirms at BOTH gates the ONLY changed lines are comment (`#`) lines; the `if ledger is not None and not ledger.try_launch():` line appears in unchanged diff context. ZERO change to any executable expression. PASS.

### R-6 (Step 2.5) — legacy wiring-input delta documented; execution path untouched — **PASS**
- (a) Inline comment at the legacy wiring-hook call @2379-2387 states the hook now receives the FRESH per-phase `max_turns × 1` ledger (R-2), deliberate K-1 refinement, pinned by **TM-13 — NOT TM-7**, and that the subprocess execution path is unchanged. PASS.
- (b) `run_post_phase_wiring_hook` docstring @829-840 documents the ledger-input delta (per-phase vs former cumulative pool), names it deliberate (not a regression), and pins it to TM-13. PASS.
- Legacy subprocess EXECUTION path unchanged: git diff shows no change to isolation dir / SessionResetPolicy / launch / monitor / PhaseResult assembly — the only `+` lines in the legacy region are comment lines (@2379-2387) and the R-10 add-site (@2395-2406). PASS.

### R-10 add-sites (Step 2.6) — read-only summation after BOTH wiring hooks — **PASS**
- Task-path add-site @2003-2015, IMMEDIATELY AFTER the task-path wiring hook @1996-2002. Read-only `sprint_wiring_totals.X += ledger.X` for all three counters.
- Legacy-path add-site @2395-2406, IMMEDIATELY AFTER the legacy-path wiring hook @2388-2394. Read-only `sprint_wiring_totals.X += ledger.X` for all three counters.
- BOTH add-sites present; both only READ `ledger.wiring_*` (no mutation of the per-phase ledger). PASS.

### R-10 arg swap (Step 2.7) — accumulator passed to build_kpi_report — **PASS**
- `build_kpi_report(..., turn_ledger=sprint_wiring_totals)` @2543 (NOT `turn_ledger=ledger`). Git diff confirms `-turn_ledger=ledger` → `+turn_ledger=sprint_wiring_totals`.
- Persisted write follows: `kpi_path = config.results_dir / "gate-kpi-report.md"` @2545; `kpi_path.write_text(kpi_report.format_report())` @2546. PASS.

### R-9 (Step 2.8) — thread-safety confirmation note — **PASS**
- Note exists at `.../phase-outputs/reviews/r9-threadsafety-confirmation.md`.
- Cited anchors re-verified live against current code: `executor.py:1196` = `def _execute_phase_tasks_parallel(` ✅; `executor.py:1244` = `def _worker(task, prior_context):` ✅; `executor.py:1333` = `with ThreadPoolExecutor(max_workers=k) as pool:` ✅; serial loop `executor.py:1873` ✅; per-phase ledger @1920 ✅; K-2 comment @1912 ✅; ledger pass @1941/@1945 ✅; `models.py:1036/1042` RLock in `__post_init__` (confirmed via anchor-map + clean git status on models.py).
- Note confirms the K-2 comment is present at the Step 2.3 construction site. No concurrency logic changed (git diff touches no concurrency code). PASS.

## Blast-Radius Check (§7)

Full `git diff src/superclaude/cli/sprint/executor.py` reviewed line-by-line. The TOTAL executable change is:
- **1 statement deleted** (global pre-loop ledger).
- **1 statement added** (per-phase ledger @1920-1923).
- **Small read-only accumulator:** 1 dataclass (`_SprintWiringTotals` @335-357) + 1 instance (@1842) + 2 add-sites (@2009-2014, @2400-2405) + 1 arg-swap (@2543).
- **Comment/log/docstring touch-ups:** R-1 block comment, R-10 construction comment, K-2/R-2 comment, both gate comments, R-6 inline comment + docstring, R-10 add-site/arg-swap comments.

NO behavioral change beyond this was found. NO gate control flow changed. NO legacy subprocess execution change. **`models.py` is UNCHANGED** — `git status --porcelain src/superclaude/cli/sprint/models.py` is empty and `git diff --stat` shows only `executor.py` modified. `kpi.py` is UNCHANGED. **Blast radius matches §7 exactly. PASS.**

## Internal Consistency / Parse

- `uv run python -c "import ast; ast.parse(...)"` → `executor.py PARSES OK`.
- Accumulator naming consistent: class `_SprintWiringTotals` → instance `sprint_wiring_totals` used at @1842 (construct), @2009-2014 + @2400-2405 (add-sites), @2543 (arg-swap). No name mismatch.
- `ledger` naming consistent: construct @1920, consumed @1945 (task), @2000/@2392 (wiring hooks), read at add-sites. No name mismatch.
- `@dataclass` decorator backed by `from dataclasses import dataclass, field` @14. `reimbursement_rate` is a valid `TurnLedger` field (`models.py:1027`). All references resolvable.

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (9 checks: R-1, R-10-construction, R-2/R-3/R-8, R-5, R-6, R-10-add-sites, R-10-arg-swap, R-9, blast-radius/parse.)
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 4 (grep/git/ast via Bash). No web research performed (all claims are local-source-truth).
- Tool-call count (12) >= checklist items (9): not suspect.
- Every item marked VERIFIED cites specific file:line tool output above. No UNCHECKED, no UNVERIFIABLE items.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | R-1 global ledger deleted, neighbors intact | PASS | diff removal; grep TurnLedger( = 1 @1920; neighbors @1832/1846/1853/1856 |
| 2 | R-10 accumulator constructed pre-loop, names match kpi.py | PASS | `_SprintWiringTotals` @335-357; instance @1842; kpi.py @193/195/197 names match |
| 3 | R-2/R-3/R-8 fresh per-phase ledger, else-1 floor, K-2 comment | PASS | @1920-1923; `else 1` @1921; K-2 @1912; after guards @1880/1894, after parse @1898, before `if tasks:` @1924 |
| 4 | R-5 both gates comment-only, control flow byte-identical | PASS | comments @1268-1275 / @1462-1472; conditionals @1276 / @1473 unchanged in diff context |
| 5 | R-6 legacy delta documented inline + docstring; exec path untouched | PASS | inline @2379-2387; docstring @829-840; no exec-path diff |
| 6 | R-10 both add-sites read-only after both hooks | PASS | task @2003-2015 after hook @1996; legacy @2395-2406 after hook @2388 |
| 7 | R-10 arg-swap passes accumulator; kpi write follows | PASS | `turn_ledger=sprint_wiring_totals` @2543; write @2545-2546 |
| 8 | R-9 note real anchors + K-2 confirmation, no concurrency change | PASS | anchors @1196/1244/1333/1873/1920/1912 verified; models.py clean |
| 9 | Blast radius §7 + models.py unchanged + parse OK | PASS | git diff scope; models.py clean; ast parse OK |

## Summary
- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

## Issues Found
None. No CRITICAL, IMPORTANT, or MINOR issues were found. (Adversarial cross-checks performed: searched for any second `TurnLedger(` construction, any surviving `len(config.active_phases)` construction, any executable change at the gates, any `models.py` modification, any accumulator/ledger name mismatch, any reference to `ledger` between the deletion site and the new construction, and any mutation of the per-phase ledger at the add-sites — all negative.)

## Actions Taken
None — no fixes were required. All Phase 2 edits are correct, minimal, and within the §7 authorized blast radius.

## Recommendations
- Phase 2 is GREEN. Proceed to Phase 3 (Step 3.1 R-7 docstring touch-up; Step 3.2 K-3 pre-merge grep) and Phase 4 (tests TM-0..TM-14).
- Note for downstream (not a Phase 2 defect): the R-10 construction comment at executor.py:1837-1838 cites approximate add-site anchors ("~L1917", "~L2287"); the real current add-sites are @2009 and @2400. The "~L" notation already signals approximation, so no change is warranted, but Step 3.2's K-3 grep and any future anchor-sensitive edit should rely on live grep, not these inline hints.

## Overall Verdict: PASS

## QA Complete
