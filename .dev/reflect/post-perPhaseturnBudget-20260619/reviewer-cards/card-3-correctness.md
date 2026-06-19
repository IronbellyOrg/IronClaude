# Reviewer Card 3 — Correctness Lens (refactorer / R-10 accumulator · §7 blast radius · R-9 thread-safety)

`/sc:reflect --mode post --depth deep` · Tier-2 ensemble · REPORT ONLY
Audit target: `git diff HEAD -- src/superclaude/cli/sprint/executor.py src/superclaude/cli/sprint/models.py`
Live files re-Read 2026-06-19: executor.py, models.py, kpi.py.
Adversarial stance: assume ≥3 correctness/blast-radius problems exist. Result: the implementation is **correct on all four mandated concerns**; the deviations I did find are documentation-truth / latent-coupling notes, not behavioral regressions.

---

## Concern 1 — Accumulator correctness (R-10 / OQ-1 Position A): **PASS**

Verdict: the accumulator is built correctly, is read-only, never re-enters the gate path, and restores sprint-cumulative KPI fidelity. Arithmetic traced end-to-end.

Evidence:
- **Constructed pre-loop, once.** `_SprintWiringTotals` defined `executor.py:335-360` (3 int fields, no `_lock`, no `__post_init__`); instantiated at `executor.py:1842` — before the `for phase` loop (`executor.py:1873`), alongside `shadow_metrics`. Confirmed sole construction (`grep _SprintWiringTotals` → defn + 1 instantiation only).
- **Two add-sites do read-only `+=` summation; ledger never mutated by the add-site.** Task path `executor.py:2009-2015`; legacy path `executor.py:2400-2406`. Both read `ledger.wiring_turns_used / wiring_turns_credited / wiring_analyses_count` and add into the accumulator. No assignment back to `ledger.*`. The ledger's wiring counters are populated *upstream* by `run_post_phase_wiring_hook` → `run_wiring_analysis_hook` via `ledger.debit_wiring` (`executor.py:564`) and `ledger.credit_wiring` (`executor.py:609/625/664/687`), so the add-site reads non-zero real telemetry — it is **not** a silent zero-summer.
- **Accumulator (not last-phase `ledger`) is passed to `build_kpi_report`.** `executor.py:2543` `turn_ledger=sprint_wiring_totals`. The post-construction `ledger` (`executor.py:1920`) has **no surviving reference at or after the KPI build** — verified by `grep '\bledger\b'` over 1920-2546: last `ledger` use is the legacy add-site read at 2405; KPI build at 2540-2543 uses the accumulator. **D-4 regression is closed.**
- **Never referenced by gate predicates.** `sprint_wiring_totals` appears only at 1842 / 2009-2015 / 2400-2406 / 2543. It is never read by `try_launch()` / `available()` / `can_run_wiring_gate()` (those live on `TurnLedger`, `models.py:1052-1132`, and take no accumulator). No shared budget pool reintroduced — R-3/R-4 budget independence preserved.
- **3 attribute names match the kpi.py read contract.** `build_kpi_report` reads exactly three attrs off `turn_ledger`: `wiring_turns_used` (`kpi.py:193`), `wiring_turns_credited` (`kpi.py:195`, wrapped `max(0, …)`), `wiring_analyses_count` (`kpi.py:197`, written to report field `wiring_analyses_run`). The accumulator exposes exactly those three. It does **not** read `wiring_budget_exhausted` or any other ledger field (`grep wiring_budget_exhausted src/.../kpi.py` → empty), so the accumulator's *absence* of that field cannot raise `AttributeError`. Duck-typing contract satisfied.
- **Arithmetic trace (D-4 concrete case).** Each phase builds a fresh ledger (wiring counters start at 0 per dataclass defaults `models.py:1039-1042`); the hook accrues only that phase's wiring; the add-site sums it. Phase1=3 analyses + Phase2=2 analyses ⇒ accumulator `wiring_analyses_count == 5` ⇒ `gate-kpi-report.md` `wiring_analyses_run == 5` (sprint-cumulative), not last-phase-only=2. **Persisted totals are sprint-cumulative.** Matches TM-13's single pinned expectation.
- **`max(0, …)` asymmetry is benign.** `kpi.py:195` floors the *summed* credited total. Per-phase `wiring_turns_credited` is monotonically non-negative (`credit_wiring`: `credit_amount = int(turns*rate) ≥ 0`, `models.py:1121-1125`), so the sum is non-negative and `max(0, …)` is a no-op — identical to the old global-pool behavior. No semantic drift.

---

## Concern 2 — Per-phase budget independence (R-3/R-4): **PASS**

Verdict: fresh ledger sized correctly; the `else 1` floor is genuinely load-bearing; python/skip phases construct no ledger; legacy branch binds the same fresh ledger (no NameError).

Evidence:
- **Sizing.** `executor.py:1920-1923`: `initial_budget=config.max_turns * (len(tasks) if tasks else 1)`. Built after `tasks = _parse_phase_tasks(...)` (`executor.py:1898`) and before `if tasks:` (`executor.py:1924`).
- **`else 1` floor genuinely prevents `initial_budget=0`.** On the legacy fall-through, `tasks` is falsy, so the multiplier is `1` ⇒ `max_turns × 1`, never 0. With `max_turns ≥ 1` an `available()==0` ledger that would fail `can_launch()` spuriously cannot arise. (The only residual is `max_turns==0`, which is a CLI-config concern unchanged by this diff and out of scope.)
- **python/skip phases construct no ledger.** The `python` guard `continue`s at `executor.py:1880` and the `skip` guard at `executor.py:1894` — both **before** the construction at 1920. R-8 satisfied; TM-11's "exactly one `TurnLedger.__init__`" is structurally honored.
- **Legacy branch binds the same fresh ledger (no NameError).** `ledger` is bound at 1920 unconditionally for any non-python/non-skip phase, then consumed by the legacy wiring hook `ledger=ledger` at `executor.py:2392`. D-3 NameError is unreachable; both branches see one bound ledger.
- **Entry invariant.** Because a new object is built each phase, at entry to `execute_phase_tasks` (`ledger=` @1945) `available() == max_turns × len(tasks)` and `consumed == 0`, independent of any earlier phase. R-3/R-4 hold by construction.

---

## Concern 3 — Thread-safety (R-9 / K-2): **PASS**

Verdict: ledger fully built in the parent thread before fan-out; every wave is synchronously joined before the next phase constructs its ledger; RLock created in `__post_init__` before publication; K-2 invariant is stated at the construction site.

Evidence:
- **Built in parent thread before workers fan out.** Construction at `executor.py:1920` (parent thread, sequential `for phase` loop) precedes the `execute_phase_tasks(ledger=ledger, …)` call at 1941-1952.
- **Each wave synchronously joined before the next phase.** `_execute_phase_tasks_parallel` joins via `with ThreadPoolExecutor(max_workers=k) as pool: wave_out = list(pool.map(lambda t: _worker(t, prior_context), wave_tasks))` (`executor.py:1333-1334`). Both the `with`-block exit and `list()` materialization block until all workers in the wave complete; the merge (1336-1342) is single-threaded; the function returns only after the final wave (`executor.py:1344-1345`). The serial `for phase` loop constructs the next ledger only after the prior phase fully returns — **no straggler crosses a phase boundary; no worker sees a half-built ledger.** F-C5 Sequence Attack holds on live code.
- **RLock before publication.** `TurnLedger.__post_init__` (`models.py:1044-1050`) creates `self._lock = threading.RLock()` as a non-field attribute, executed during construction at 1920 — before the object is handed to any worker. `try_launch` (`models.py:1074-1089`) is atomic check-and-debit under the lock (TOCTOU-safe for K>1).
- **K-2 invariant stated at the construction site.** `executor.py:1911-1919` explicitly states the sequential-phase invariant and the consequence ("If a future change ever overlaps phases, this per-phase ledger would need explicit per-phase ownership"). Matches R-9/K-2 requirement.

---

## Concern 4 — Blast radius (§7): **PASS with two documentation-truth flags**

Verdict: the executable change set is exactly the §7-sanctioned shape — one statement deleted, one added, a read-only accumulator (1 dataclass + construction + 2 add-sites + 1 arg-swap), comment/docstring touch-ups. **No executable change to any gate, no new `TurnLedger` method/field, no modified subprocess path.** I found **no Regression and no Drift** in behavior. The two items below are documentation accuracy notes (Grounding-Gap class), not behavioral deviations.

Behavioral-change scan (all confirmed *absent*):
- Gate code: `executor.py:1265-1273` (parallel) and `1459-1469` (sequential) diff is **comment/log-string only** — `if ledger is not None and not ledger.try_launch():` body unchanged. R-5 honored.
- `TurnLedger` model: `models.py` diff is a **docstring-only** addition (1018-1024); no new method/field; `available/debit/credit/try_launch/debit_wiring/credit_wiring/can_run_wiring_gate` bodies unchanged. R-7 honored. `hasattr(TurnLedger,'reset')` remains False.
- Subprocess execution path (isolation dir, `SessionResetPolicy`, launch, monitor, `PhaseResult` assembly, `_determine_phase_status`, `_verify_checkpoints`): unchanged in the diff (`executor.py:2037-2376`). Only the wiring-hook *input* differs (now a fresh `max_turns × 1` ledger) — the deliberate, documented K-1 refinement, pinned by TM-13. C2 honored.
- Halt/break paths preserve add-site symmetry: task-path `break`@2034 and legacy-path `break`@2447/2478 both fire **after** their respective add-site (2009-2015 / 2400-2406), so a failing/halting phase still folds its wiring telemetry before the loop exits. No asymmetric telemetry loss.

---

## Deviation list (file:line · class · rationale)

| # | Location | Class | Note |
|---|----------|-------|------|
| DV-1 | `executor.py:1839` (comment) | **Grounding Gap** (doc-truth) | Comment cites "kpi.py:193/195/197" and "kpi.py:192-197"; verified accurate on live `kpi.py`. No deviation — recorded as *positive* grounding. (Listed so the ledger of checked anchors is explicit.) |
| DV-2 | `executor.py:2009-2015` & `2400-2406` | **Necessary deviation** (vs the spec's "either accumulator OR thin param" option at R-10/kpi.py:211-214) | Implementation chose the accumulator-shaped-to-read-contract option (not a new `build_kpi_report` param). This is one of the two spec-sanctioned options and is the lower-blast-radius one (kpi.py signature untouched). Authorized by R-10's "either is acceptable." |
| DV-3 | `executor.py:2480` (`try`/`finally`, no `except`) | **[INFERRED] latent-coupling note** (not a regression) | The legacy `try:`@2041 has only a `finally:`@2480, no `except`. An exception raised in the legacy subprocess body (2041-2388) propagates out and aborts the sprint *before* the legacy add-site (2400-2406) and before the KPI build (2540) — so on a legacy-phase crash, `gate-kpi-report.md` is simply not written (whole-sprint abort), **not** written with desynced totals. This is pre-existing behavior, unchanged by the diff; flagged only because the add-site now lives inside that abort window. No action required. |
| DV-4 | `executor.py:336-360` docstring | **Grounding Gap** (doc-truth, cosmetic) | The `_SprintWiringTotals` docstring asserts "Its three attribute names exactly match the kpi.py:192-197 read contract." Verified true today, but this is a hardcoded line-anchor in a docstring that will silently drift if `kpi.py` is re-numbered. Behavior is anchor-independent (duck-typed by name), so drift would mislead a *reader*, not the code. Low severity. |

No **Drift** (silent-and-unmapped behavioral change) and no **Regression** (constraint contradiction) found in the executable surface.

---

## [INFERRED] section (assumptions / unverifiable-from-diff)

- **[INFERRED]** `config.max_turns ≥ 1` in practice. The `else 1` floor guarantees `initial_budget ≥ max_turns`; if `max_turns==0` the floor does not save it, but that is a CLI-validation concern unchanged by this diff and out of scope for this audit.
- **[INFERRED]** `run_post_phase_wiring_hook` always returns to the same thread that constructed the ledger (it does — it is called synchronously in the `for phase` body at 1996 / 2388, not inside a worker), so the add-site reads `ledger.*` with no cross-thread visibility hazard. The per-phase ledger's wiring counters are mutated under `_lock` inside `debit_wiring`/`credit_wiring`; the add-site reads them after the synchronous hook returns on the same thread, so a plain read is safe (happens-after the hook's lock release on this thread).
- **[INFERRED]** TM-13 / TM-0 / TM-12 are *specified* but I did not execute the test suite (REPORT-ONLY audit; no `uv run pytest`). The code structure satisfies their preconditions, but green-test confirmation is outside this card's evidence. A test run is the residual verification gap.
- **[INFERRED]** No concurrent *phase* execution exists anywhere else in the call graph (K-2). I verified the single `for phase` loop and the within-phase join; I did not exhaustively prove no other caller drives phases in parallel. The construction-site comment correctly flags this as the load-bearing precondition.

---

## Calibrated self-confidence: **0.88**

Basis: all four mandated concerns verified against live code with grep-closed reference sets (accumulator refs, ledger refs post-construction, kpi read contract, build_kpi_report callers all enumerated). The arithmetic trace and the gate-isolation proof are direct, not inferred. The 0.12 discount reflects: (a) I did not execute the test suite, so TM-13/TM-0/TM-12 green status is asserted structurally not empirically; (b) the K-2 "no other parallel-phase driver" claim rests on the visible call graph, not an exhaustive whole-repo proof.

## One-line verdict

**Correct on all four concerns — R-10 accumulator restores sprint-cumulative KPI fidelity with zero gate-path coupling, per-phase budget independence and R-9/K-2 thread-safety hold, and the blast radius is exactly the §7-sanctioned shape; the only findings are two doc-truth Grounding Gaps and one pre-existing latent-coupling note, no Drift and no Regression.**
