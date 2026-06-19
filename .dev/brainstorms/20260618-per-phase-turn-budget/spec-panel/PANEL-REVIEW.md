---
title: "Spec-Panel Review — Per-Phase Turn-Budget Model (merged-requirements.md)"
command: /sc:spec-panel
mode: critique
focus: [requirements, architecture, testing, correctness]
iterations: 2
format: detailed
panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower]
reviewed_spec: ".dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements.md"
ground_truth_worktree: ".claude/worktrees/perPhaseturnBudget (HEAD = origin/master)"
review_date: 2026-06-18
---

# Spec-Panel Review — Per-Phase Turn-Budget Model

> **Mode: critique (adversarial).** All eleven experts active. Every correctness finding below
> is grounded in a re-`Read` of the live code in this worktree on 2026-06-18. Line anchors in the
> spec were cross-checked against the live files; drift is reported as findings, not silently accepted.

## 1. Metadata

| Field | Value |
|-------|-------|
| Spec under review | `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements.md` (v1, design-only) |
| Driving context | `seed-brief.md`; `.dev/troubleshoot/phase56-budget-exhaustion-20260617/REPORT.md` |
| Target code | `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/models.py`, `src/superclaude/cli/sprint/kpi.py` |
| Panel | 11 experts (full default) |
| Mode / Focus | critique / requirements + architecture + testing + correctness |
| Iterations | 2 (1 = surface findings; 2 = refined spec → `merged-requirements-v2.md`) |
| Format | detailed |

## 2. Quality Assessment (0–10 per dimension)

| Dimension | Score | Justification |
|-----------|------:|---------------|
| **Clarity** | 8 | Decision table (Q1–Q7), R-item anchor→change→verification format, and blast-radius table are exemplary. Minor: prose hardcodes `5`/`debit(actual-5)` where code uses the `minimum_allocation` variable. |
| **Completeness** | 6 | Covers the executor.py surface thoroughly, but the headline "no accumulator needed" claim rests on an explicitly *un-widened* grep (D-2 within-file only; K-3 admits package not audited) — and the package DOES contain an external consumer (`kpi.py`). One real post-loop ledger reader (KPI report) is unaccounted for. |
| **Testability** | 8 | TM-0..TM-12 are concrete, reuse existing harnesses, name files and assertions. Gaps: no test pins the post-loop KPI wiring totals; TM-7 characterization scope (subprocess log only) is too narrow to catch the wiring-input delta it is cited to guard. |
| **Consistency** | 7 | Internally coherent on the executor.py path. The inconsistency is between the design's "independence by construction, nothing external reads cumulative state" thesis and the actual post-loop KPI read — a contradiction the spec does not surface. |
| **Correctness** | 5 | The core executor.py mechanism (fresh-construct, placement @1838, dual-branch binding, join-before-return, gate-as-safety-net) is **verified correct against live code**. But a BLOCKER-class silent regression in the post-loop KPI artifact (wiring totals collapse from sprint-cumulative to last-phase-only) is unhandled, and D-2/Q5/R-4's supporting claim is falsified. |
| **Architectural soundness** | 7 | Fresh-construct-per-phase is the right call and is genuinely safe under K>1 (verified: workers joined before return). The architecture is sound *for the budget gate*; it is unsound for the *telemetry lifecycle* it implicitly shares with the same object. |
| **OVERALL** | **6.4** | A strong, well-anchored design with one verified BLOCKER (KPI wiring regression) and a falsified load-bearing claim, plus several MAJOR test/spec gaps. Not yet implementation-ready without the v2 fixes. |

---

## 3. Ground-Truth Verification Ledger

Every spec anchor the panel could check, checked against the live worktree:

| Spec claim / anchor | Live code | Verdict |
|---------------------|-----------|---------|
| Global ledger `initial_budget = max_turns * len(active_phases)` @`executor.py:1777-1780` | `executor.py:1777-1780` exact match | ✅ VERIFIED |
| Task-branch `ledger=ledger` @1860 | `executor.py:1860` | ✅ VERIFIED |
| Legacy-branch wiring hook `ledger=ledger` @2285 (call 2281-2287) | `executor.py:2281-2287`, kwarg @2285 | ✅ VERIFIED |
| `tasks = _parse_phase_tasks(...)` @1838, `if tasks:` @1839 | `executor.py:1838` / `1839` | ✅ VERIFIED |
| python `continue` @1819-1820, skip `continue` @1823-1834 | `executor.py:1819-1820` / `1823-1834` | ✅ VERIFIED |
| Parallel gate `try_launch` @1231 → SKIPPED @1235 | `executor.py:1231` / `1235` | ✅ VERIFIED |
| Sequential gate `try_launch` @1424 → SKIPPED @1430, `remaining` @1425 | `executor.py:1424` / `1430` / `1425` | ✅ VERIFIED |
| Reconciliation @1126-1131 | live span `1125-1132`; uses `pre_allocated = ledger.minimum_allocation` (var, not literal 5) | ⚠️ ANCHOR OK, PROSE DRIFT |
| `aggregate_task_results` def @335 | `executor.py:335` | ✅ VERIFIED |
| `_parse_phase_tasks` def @1677, returns `list | None` | `executor.py:1677`; never empty-list-truthy | ✅ VERIFIED |
| Provider-exhaustion break @1936 | `executor.py:1936` | ✅ VERIFIED |
| Task-path wiring hook @1911-1917 | `executor.py:1911-1917` | ✅ VERIFIED |
| `execute_phase_tasks` joins all workers before return | `_execute_phase_tasks_parallel` uses `with ThreadPoolExecutor(...) as pool: list(pool.map(...))` per wave @1288-1289; returns @1300 after all waves | ✅ VERIFIED — no detached futures |
| `TurnLedger` @`models.py:901-1014`; fields @914-924; `available()` @934-936; debit @938-943 | **Live: class @1011-1124; fields @1024-1034; `available()` @1044-1046; `debit` @1048-1053** | ❌ ANCHOR DRIFT ~+110 lines |
| D-2: "nothing reads sprint-cumulative `wiring_*` / `available()` after loop; only @390 and @949" | **`kpi.py:193-197` reads `turn_ledger.wiring_turns_used/credited/analyses_count`, reached from post-loop `executor.py:2414-2418` `build_kpi_report(turn_ledger=ledger)`** | ❌ FALSIFIED |

---

## 4. Findings by Focus Area

### `=== REQUIREMENTS ANALYSIS ===` (Wiegers lead, Adzic, Cockburn)

**F-R1 — [MAJOR] The "no sprint-level accumulator" requirement (Q5/R-4/D-2) is stated as verified fact but rests on a within-file grep that misses a real external reader.**
*Expert:* Wiegers. *Evidence:* spec D-2 says the grep "returns only `executor.py:390` and `949`"; but `kpi.py:193-197` reads three `wiring_*` fields off a `TurnLedger`, and `executor.py:2414-2418` feeds it `turn_ledger=ledger` *after* the phase loop. *Rationale:* A requirement asserting "X is unnecessary because nothing reads Y" must be backed by the same package-wide search the risk register (K-3) explicitly defers. Here the deferred search would have falsified the requirement. *Recommendation:* Reclassify Q5 from "no accumulator needed" to "a sprint-level wiring accumulator IS needed to preserve KPI fidelity" OR explicitly accept the KPI-fidelity regression with a documented decision + test. *Priority:* High. *Quality impact:* Converts a silent telemetry regression into an explicit, tested decision.

**F-R2 — [MINOR] `--max-turns` semantic realignment is asserted but no requirement pins the observable contract (the help text already says "per phase"; the runtime now matches).**
*Expert:* Wiegers. *Evidence:* C1 cites `commands.py:92`. *Rationale:* SMART criteria — the success condition ("runtime unit == documented unit") is testable but no R-item or TM row asserts a *per-phase* budget value end-to-end beyond TM-0's `available()==500`. TM-0 covers it adequately; flagging only for traceability. *Priority:* Low.

**F-R3 — [MINOR] R-6 "byte-equivalent unchanged" is an absolute claim weakened by its own admitted delta (K-1).**
*Expert:* Cockburn. *Evidence:* R-6 says legacy subprocess path is "byte-equivalent unchanged" but the same R-item and K-1 admit the wiring-hook input changes. *Rationale:* "byte-equivalent" should scope to *subprocess execution* only (which is what TM-7 pins); the wiring-input delta is a separate, intended change. The wording invites a reader to over-trust. *Recommendation:* Scope the phrase: "subprocess execution log byte-equivalent; wiring-hook ledger input intentionally changed (K-1)." *Priority:* Low.

### `=== ARCHITECTURE ANALYSIS ===` (Fowler lead, Newman, Hohpe, Nygard)

**F-A1 — [BLOCKER] The TurnLedger object conflates two lifecycles with different scopes: per-phase budget (correctly made per-phase by this design) and sprint-cumulative wiring telemetry (silently demoted to last-phase-only).**
*Expert:* Fowler. *Evidence:* `executor.py:2414-2418` reads `ledger` post-loop; under R-1+R-2 that `ledger` is the *final phase's* fresh instance, so `kpi.py:193-197` reports only the last phase's `wiring_turns_used/credited/analyses_count`. Today (global pool) it reports sprint-cumulative. *Rationale:* This is the classic single-responsibility violation Fowler warns about: one object owns both a per-phase resource gate and a sprint-life telemetry counter. Making the object per-phase fixes the first responsibility and breaks the second. *Recommendation:* Either (a) introduce a tiny sprint-level wiring accumulator updated at each phase boundary and passed to `build_kpi_report`, or (b) explicitly accept last-phase-only KPI wiring as the new contract and characterization-pin it. Do not ship silently. *Priority:* High. *Quality impact:* Prevents a silent regression in a persisted artifact (`gate-kpi-report.md`).

**F-A2 — [MINOR] D-2's conclusion ("accumulators are dead code") is generalized from an under-scoped search and should be re-derived from the package-wide grep.**
*Expert:* Newman. *Evidence:* D-2 reasoning chain. *Rationale:* service/module-boundary discipline — `kpi.py` is a downstream consumer of the ledger's evolution-sensitive state; the spec treated `run_sprint`'s function body as the boundary when the real boundary is the package. *Recommendation:* Re-run `grep -rn "\.wiring_turns\|\.wiring_analyses\|turn_ledger=" src/superclaude/cli/sprint` and fold results into D-2. *Priority:* Medium.

**F-A3 — [MINOR] Sequential-phase assumption (K-2) is the load-bearing precondition for fresh-construct safety and deserves promotion from "open risk" to a stated architectural invariant.**
*Expert:* Hohpe. *Evidence:* the `for phase in config.active_phases:` loop @`executor.py:1813` is serial; R-9 correctness depends on it. *Rationale:* the design's thread-safety argument (one ledger per phase, workers joined before next construction) holds *only* because phases never overlap. That's an integration-level ordering guarantee worth stating as INV, not burying in K-2. *Priority:* Low.

**F-A4 — [OK→note] Fresh-construct-vs-reset() decision (Q1) is architecturally correct and verified safe.**
*Expert:* Fowler/Nygard concur. *Evidence:* `__post_init__` builds `_lock` before publication (`models.py:1036-1042`); parallel workers are fully joined per wave (`executor.py:1288-1289`) before the function returns (`1300`); the next phase's construction happens in the serial loop body after `execute_phase_tasks` returns. No half-built/mid-reset ledger is observable. *Verdict:* No finding — this is the strongest part of the design.

### `=== TESTING ANALYSIS ===` (Crispin lead, Gregory, Adzic)

**F-T1 — [MAJOR] No test in TM-0..TM-12 pins the post-loop KPI wiring totals — the exact surface the F-A1 regression lives on.**
*Expert:* Crispin. *Evidence:* TM matrix rows target `available()`, identity, gate, legacy subprocess log, concurrency — none assert `gate-kpi-report.md` wiring fields after a multi-phase sprint with wiring activity. *Rationale:* the test matrix's coverage map has a hole exactly where the design's blind spot is; a regression here ships green. *Recommendation:* Add **TM-13**: multi-phase sprint where ≥2 phases run wiring analysis; assert the KPI report's `wiring_turns_used`/`wiring_analyses_run` reflect the intended contract (sum-across-phases if accumulator added; last-phase-only if that contract is accepted). *Priority:* High.

**F-T2 — [MAJOR] TM-7's characterization scope ("subprocess execution log: order/status/exit_code") is too narrow to catch the regression it is cited to guard (K-1 wiring delta).**
*Expert:* Gregory. *Evidence:* R-6 and K-1 both name TM-7 as the mitigation for the wiring-input delta, but TM-7 pins only the subprocess log, which by design does NOT change. The wiring delta manifests in wiring-hook side effects (remediation entries, KPI counts), not in the subprocess log. *Rationale:* a characterization test that pins the unchanged surface gives false confidence about the changed surface. *Recommendation:* Either widen TM-7 to also pin wiring-hook observable output on the legacy path, or remove the TM-7 citation from K-1's mitigation and point it at TM-13. *Priority:* High.

**F-T3 — [MINOR] TM-2's "0-guarded" zero-task case tests an unreachable executor path.**
*Expert:* Adzic. *Evidence:* `_parse_phase_tasks` (`executor.py:1677-1692`) returns `None` (never `[]`-truthy) for taskless phases, and `if tasks:` (`1839`) is False for both, so `TurnLedger(initial_budget=0)` from a "0-task task phase" cannot arise; R-2's `len(tasks) if tasks else 1` floors legacy to 1. *Rationale:* the unit test is still valuable as a model-level guard, but the spec should state it tests the *model in isolation*, not a reachable phase path — otherwise a reader infers a path that doesn't exist. *Recommendation:* annotate TM-2 as "model-level defensive; not a reachable executor state." *Priority:* Low.

**F-T4 — [MINOR] No test covers `--start`/`--resume` partial-window interaction with per-phase sizing.**
*Expert:* Crispin. *Evidence:* the original bug manifested under `--start 4` (REPORT.md: `active_phases={4,5,6}`). The fix removes `len(active_phases)` from sizing, so `--start` no longer affects per-phase budget — good — but no TM row asserts that a resumed/partial window sizes each phase identically to a full run. *Recommendation:* add a TM row: same phase sized identically whether reached via full run or `--start`. *Priority:* Low (behavior is correct by construction; test is belt-and-suspenders).

### `=== CORRECTNESS ANALYSIS ===` (Nygard lead, Fowler, Adzic, Crispin, Whittaker)

#### State Variable Registry (FR-15.1)

| Variable | Type | Initial Value (per phase) | Invariant | Read Operations | Write Operations |
|----------|------|---------------------------|-----------|-----------------|------------------|
| `ledger.initial_budget` | int | `max_turns × len(tasks)` (task) / `max_turns × 1` (legacy) | constant within a phase; `> 0` (floored to `max_turns` via `else 1`) | `available()` (`models.py:1046`), `can_launch` (`1064`) | set once at construction (`executor.py:1838` post-fix) |
| `ledger.consumed` | int | `0` (fresh each phase) | monotonic non-decreasing within an instance (`debit` only adds, `models.py:1048-1053`) | `available()` | `debit` (gate `try_launch` @1231/1424; reconcile @1129) |
| `ledger.reimbursed` | int | `0` (fresh each phase) | non-decreasing within instance | `available()` | `credit` (reconcile @1132; `credit_wiring` @1116) |
| `ledger.wiring_turns_used` | int | `0` (fresh each phase) | non-decreasing within instance | **`kpi.py:193` (post-loop, sprint scope)** ⚠️ | `debit_wiring` (`models.py:1097`) |
| `ledger.wiring_turns_credited` | int | `0` (fresh each phase) | non-decreasing | **`kpi.py:195` (post-loop)** ⚠️ | `credit_wiring` (`models.py:1117`) |
| `ledger.wiring_analyses_count` | int | `0` (fresh each phase) | non-decreasing | **`kpi.py:197` (post-loop)** ⚠️ | `debit_wiring` (`models.py:1098`) |
| `ledger.wiring_budget_exhausted` | int (0/1) | `0` (fresh each phase) | latches to 1 within instance | `can_run_wiring_gate` (`models.py:1122`) | `debit_wiring` (`models.py:1100`) |

The three ⚠️ rows are the crux: their **read scope (sprint-cumulative, post-loop) outlives their new write scope (per-phase)**. This is the registry's headline correctness signal and the root of F-A1/F-C1.

#### Guard Condition Boundary Table (Nygard lead, Crispin validate, Whittaker attack)

Guard = `try_launch()` (`models.py:1066-1081`): launches iff `available() >= minimum_allocation` (=5).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| `try_launch` | `models.py:1078`, gate `executor.py:1424`/`1231` | Zero/Empty | `available()==0` (phase pool fully spent) | False | task SKIPPED → phase ERROR (R-5 safety net) | OK |
| `try_launch` | same | One/Minimal | `available()==max_turns×1` (1-task phase) | True (first), then drains | 1 task launches; overspend trips net (TM-9) | OK |
| `try_launch` | same | Typical | `available()==max_turns×N` at entry | True for all N | every task launches (R-3, TM-0) | OK |
| `try_launch` | same | Maximum/Overflow | tasks collectively consume `>max_turns×N` | False after threshold | genuine overspend SKIP (TM-9) | OK |
| `try_launch` | same | Sentinel (`available() == minimum_allocation == 5`) | `==5` | True (`>= 5`) | boundary launch allowed; debits 5 → `available()==0` | OK |
| `try_launch` | same | Legitimate Edge (`available()==4`, between launches) | `<5` | False | SKIP though 4 turns "left" — sub-minimum residue, intended | OK |
| **KPI wiring read** | `kpi.py:192` `if turn_ledger is not None` | post-loop, `ledger`=last phase | n/a (no guard on scope) | reads last-phase fields | **spec is SILENT on the scope change** | **GAP** |

Per FR-8 (GAP Status Rule), the single **GAP** row generates a **MAJOR-minimum** finding → escalated to BLOCKER by F-A1 because it silently corrupts a persisted artifact.

#### Whittaker Adversarial Attacks (all 5 methodologies, FR-14.6: ≥1 per methodology per invariant)

**F-C1 — [BLOCKER] Accumulation Attack on the wiring telemetry counters.**
> I can break this specification by **FR-2.5 Accumulation Attack**. The invariant at **Q5/R-4/D-2 ("wiring counters start at 0 every phase; no sprint accumulator needed")** fails when **a sprint runs wiring analysis in more than one phase and then writes the KPI report**. Concrete attack: phase 1 runs 3 wiring analyses (`wiring_analyses_count→3` on ledger A); R-2 constructs fresh ledger B for phase 2, which runs 2 analyses (`count→2` on B); the loop ends with `ledger` bound to B; `executor.py:2417` passes `turn_ledger=ledger` (=B) to `build_kpi_report`; `kpi.py:197` writes `wiring_analyses_run = 2`. **Before fix:** the global pool accumulated 5. **After fix:** the report says 2. Sprint-cumulative wiring telemetry is silently undercounted by every phase except the last. State trace: `{global.count: 5} → {B.count: 2}` in the persisted `gate-kpi-report.md`. *Severity:* CRITICAL (specification is provably wrong about "nothing reads cumulative wiring").

**F-C2 — [MINOR] Zero/Empty Attack on legacy sizing.**
> I can break this by **FR-2.1 Zero/Empty Attack**. The invariant at **R-2 (`len(tasks) if tasks else 1`)** is *robust*: when `tasks` is `None` (legacy) the size floors to `max_turns × 1`; when `tasks` is truthy it is never empty (`_parse_phase_tasks` @1677 never returns `[]`-truthy). Attack outcome: **no break found** — the `else 1` correctly prevents an `initial_budget=0` ledger on the legacy path. Documented as a *defended* boundary, not a gap.

**F-C3 — [MINOR] Sentinel Collision Attack on `minimum_allocation`.**
> **FR-2.3 Sentinel Collision.** The reconciliation (`executor.py:1125-1132`) uses `pre_allocated = ledger.minimum_allocation` (=5) as the launch pre-debit. A task that legitimately consumes *exactly* 5 turns hits `actual == pre_allocated`: neither branch fires (no debit, no credit) — correct (5 pre-debited == 5 actual). No collision. The spec's prose hardcodes `5`/`debit(actual-5)`; if a future contributor changes `minimum_allocation`, the spec prose silently desyncs from code. *Recommendation:* spec should say `minimum_allocation`, not `5`. (folded into F-X1).

**F-C4 — [MINOR] Divergence Attack on the `if tasks:` branch boundary.**
> **FR-2.2 Divergence Attack.** The fresh ledger is bound at `1838` *before* the `if tasks:` divergence (`1839`), so BOTH branches see a bound `ledger` — this is exactly D-3's headline claim, and it is **verified correct**: task branch reads `ledger` @1860, legacy branch @2285, both downstream of the single construction. Attack outcome: **no NameError reachable**; the placement defends both branches. (This is the spec's strongest correctness claim and it holds.)

**F-C5 — [MINOR] Sequence Attack on phase ordering vs. straggler workers.**
> **FR-2.4 Sequence Attack.** Could phase 2's ledger construction race a phase-1 straggler worker? Traced: `_execute_phase_tasks_parallel` joins every wave via `with ThreadPoolExecutor(...) as pool` (`executor.py:1288`) and only returns after the final wave (`1300`); `execute_phase_tasks` returns synchronously; the serial `for phase` loop constructs the next ledger only after the previous `execute_phase_tasks` returns. **No straggler can survive into the next phase.** Attack outcome: **no break** — R-9 holds. (Verified, not assumed.)

---

## 5. Adversarial / Correctness Summary (Whittaker-led)

| ID | Methodology | Severity | Invariant Location | Verdict |
|----|-------------|----------|--------------------|---------|
| F-C1 | Accumulation | **CRITICAL/BLOCKER** | Q5/R-4/D-2; `kpi.py:193-197` via `executor.py:2414-2418` | **Real regression — must fix or accept-with-test** |
| F-C2 | Zero/Empty | MINOR (defended) | R-2 `else 1` | No break |
| F-C3 | Sentinel | MINOR | `executor.py:1125-1132` | Prose drift only |
| F-C4 | Divergence | MINOR (defended) | D-3 / placement @1838 | No break — claim holds |
| F-C5 | Sequence | MINOR (defended) | R-9 / join @1288-1300 | No break — claim holds |

**Net:** the design's executor.py mechanism is correct and defends 3 of 5 attacks outright. The one CRITICAL is a *scope-mismatch* the spec did not surface because it stopped its grep at the function boundary.

---

## 6. Cross-Expert Consensus

- **Consensus (strong):** Fresh-construct-per-phase (Q1) is correct, and the @1838 dual-branch placement (D-3/Q6) is verified safe — Fowler, Nygard, Whittaker, Newman all concur. The executor.py blast radius (one delete, one add) is accurate.
- **Consensus (strong):** Thread-safety under K>1 (R-9) holds by *verified* worker-join semantics, not by assumption.
- **Consensus (split → see Open Questions):** Whether the KPI wiring-telemetry regression (F-A1/F-C1) must be fixed with a sprint-level accumulator, or accepted as a new "last-phase-only" contract with a characterization pin. Fowler/Crispin lean "add the accumulator"; Newman/Hightower lean "accept + document, KPI wiring is advisory telemetry." This is genuinely non-obvious.
- **Disagreement (minor):** Gregory vs. Adzic on whether TM-2's zero-task unit test should stay (Adzic: relabel; Gregory: keep as-is, it guards the model).

---

## 7. Severity Roll-Up

| Severity | Count | IDs |
|----------|------:|-----|
| **BLOCKER** | 2 | F-A1, F-C1 (same root cause: post-loop KPI ledger read) |
| **MAJOR** | 4 | F-R1, F-T1, F-T2, plus the Boundary-Table GAP row (FR-8) |
| **MINOR** | 8 | F-R2, F-R3, F-A2, F-A3, F-T3, F-T4, F-C2/3/4/5 (defended), F-X1 (anchor drift) |
| **OK/verified** | — | F-A4, D-3 placement, R-9 join, R-2 `else 1` |

**F-X1 — [MINOR] Systematic models.py anchor drift (~+110 lines).** The spec cites `TurnLedger` at `models.py:901-1014`, fields `914-924`, `available()` `934-936`, debit `938-943`. Live: class `1011-1124`, fields `1024-1034`, `available()` `1044-1046`, debit `1048-1053`. The *executor.py* anchors are accurate; only the *models.py* anchors are uniformly stale. *Recommendation:* re-anchor all models.py references in v2 (done in `merged-requirements-v2.md`).

---

## 8. Prioritized Improvement Roadmap

### Immediate (blocking — incorporated into v2)
1. **Resolve the KPI wiring regression (F-A1/F-C1).** Add **D-4** (finding) + **R-10** (requirement) + **TM-13** (test). v2 specifies the accumulator option as the recommended path and the accept-and-pin option as the adjudicated alternative (see Open Questions OQ-1).
2. **Correct D-2** to state the package-wide grep result, naming `kpi.py:193-197` as a real post-loop consumer; remove the "accumulator is dead code" conclusion.
3. **Re-anchor all `models.py` line references (F-X1).**
4. **Widen/redirect TM-7's mitigation role (F-T2):** point K-1's mitigation at TM-13, not TM-7.

### Short-term (v2 spec touch-ups)
5. Scope R-6's "byte-equivalent" wording (F-R3); replace prose `5` with `minimum_allocation` (F-C3/F-X1).
6. Relabel TM-2's zero-task case as model-level/defensive (F-T3).
7. Promote K-2 (sequential-phase assumption) to a stated invariant in the construction-site comment requirement (F-A3).

### Long-term (post-merge hygiene)
8. Add the `--start`/`--resume` parity test (F-T4).
9. Consider extracting wiring telemetry out of `TurnLedger` into a sprint-scoped `WiringTelemetry` object so the two lifecycles stop sharing one class (Fowler's SRP fix) — out of scope for this change, noted as tech-debt.

---

## Open Questions

> These are the genuinely unresolved decisions where the panel split and the right answer is non-obvious.
> The orchestrator will adversarially adjudicate; they are NOT resolved here.

**OQ-1. KPI wiring telemetry: add a sprint-level accumulator, or accept "last-phase-only" as the new contract?**
The fix makes `ledger` per-phase, so the post-loop `build_kpi_report(turn_ledger=ledger)` call (`executor.py:2414-2418`) now reads only the *final* phase's `wiring_turns_used/credited/analyses_count` (`kpi.py:193-197`), where today's global pool reports sprint-cumulative totals.
- **Position A (Fowler, Crispin — "preserve fidelity"):** Add a tiny sprint-level wiring accumulator, summed at each phase boundary and passed to `build_kpi_report`. The KPI report is a persisted artifact (`gate-kpi-report.md`); silently changing its meaning is a regression in observable output, regardless of how "advisory" the numbers are. Cost: ~3 lines + one field; directly contradicts the spec's "no accumulator" thesis (Q5/D-2), so the design narrative must change.
- **Position B (Newman, Hightower — "accept + pin"):** Wiring KPIs are advisory telemetry, not control signals. Per-phase independence is the whole point; a cross-phase accumulator re-introduces exactly the sprint-level shared state the design is removing. Accept last-phase-only as the new contract, document it at the call site, and characterization-pin it (TM-13) so the change is deliberate, not silent. Cost: a behavior change to a shipped artifact that some downstream retrospective tooling may consume unverified.
- **Why non-obvious:** A's "don't regress an artifact" and B's "don't re-introduce the coupling we're deleting" are both first-principles-correct and directly oppose each other. The deciding fact the panel could not settle: *does any consumer treat `gate-kpi-report.md` wiring totals as sprint-cumulative load-bearing input* (vs. human-glance telemetry)? That requires a consumer audit the spec has not done.

**OQ-2. Should `--max-turns × len(tasks)` sizing use the *parsed* task count or the *post-dependency-filter/wave* count?**
R-2 sizes from `len(tasks)` (the full parsed inventory at `executor.py:1838`). But the parallel path executes in dependency *waves* (`executor.py:1283`), and resume-skip (`executor.py:1209-1229`, `1396-1415`) can mark validated-success tasks as PASS with `turns_consumed=0` *without* debiting.
- **Position A (Adzic):** `len(tasks)` is correct and generous-by-design — it sizes for the worst case (every task runs fresh). Resume-skipped tasks simply leave headroom; the gate is a safety net (Q7), so over-sizing is harmless.
- **Position B (Whittaker):** On a `--resume` run where most tasks are skip-PASS, the pool is sized for N but only a few run — fine for *not* starving, but it means the "pool exactly covers N tasks" invariant (Q7/D-1) is *looser* than stated on resume runs. The spec claims exactness ("the pool exactly covers N tasks each consuming up to max_turns"); on resume that exactness is vacuous.
- **Why non-obvious:** It's not a bug (over-sizing never starves), but the spec's *exactness* claim (Q7) is technically false on resume runs. Whether to weaken the claim's wording or leave it (since the safety-net framing makes over-sizing benign) is a judgment call about how precise a design doc's invariants must be.
