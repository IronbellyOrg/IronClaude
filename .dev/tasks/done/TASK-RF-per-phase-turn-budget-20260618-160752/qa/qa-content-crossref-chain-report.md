# QA Report — Content Crossref-Chain Integrity Lens

**Topic:** Per-Phase Turn-Budget Model — requirement→code→test chain integrity
**Date:** 2026-06-18
**Phase:** doc-qualitative (crossref-chain integrity lens, final QA gate)
**Fix authorization:** FALSE — REPORT ONLY, no edits made
**Fix cycle:** N/A

---

## Overall Verdict: PASS (with MINOR advisories)

Every requirement→code→test chain traces end-to-end against live source. The
spec's prose line-anchors have drifted downward (the implementation lives ~80
lines below the anchors the spec cites, because R-10's accumulator + comments
added +144 lines), but **every chain LINK exists at a real, citable location**
and the spec's narrative anchor-map already documents this drift. No chain link
is missing. The five-broken-links hypothesis is NOT confirmed — the adversarial
floor was met by exhaustive trace, and the only defects found are line-anchor
staleness (MINOR), not broken links.

---

## R-item → Code → Test Chain Trace

Each row traces: spec anchor (as written) → ACTUAL live code location → TM test
that exercises it. "Δ" flags spec-anchor drift vs. live source.

| R / K | Spec anchor (as written) | Live code (verified) | Test link (verified) | Chain |
|---|---|---|---|---|
| **R-1** delete global ledger | `executor.py:1777-1780` | global `TurnLedger(... len(active_phases))` GONE; replaced by R-1 comment block `executor.py:1824-1831`; `grep len(config.active_phases)` returns no ledger ctor | TM-0 `test_per_phase_budget.py:176` asserts per-phase 500 pool (the anti-starvation proof) | OK intact (Δ) |
| **R-2** fresh phase-sized ledger | `executor.py:1838-1839` | `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), ...)` at **`executor.py:1920-1923`**, after both `continue` guards, after `_parse_phase_tasks` @1898, before `if tasks:` @1924 | TM-1 `:230` distinct identities + `max_turns × len(tasks)` | OK intact (Δ ~+82 lines) |
| **R-3** core invariant `available()==max_turns×task_count` | sizing `1838`; `available()` `models.py:1044-1046` | sizing @1920; `available()` @**`models.py:1052-1054`** | **TM-0 `:217-222`** asserts `available()==500` at entry to each of 3 phases | OK intact (Δ) |
| **R-4** independence (reimburse+wiring start 0) | `models.py:1024-1034` defaults; R-2 ctor | dataclass defaults `models.py:1032-1042` (`consumed`/`reimbursed`/4 wiring fields = 0); fresh ctor R-2 | **TM-5 `:267`** phase-1 reimbursement does not affect phase-2; **TM-10 `:472`** | OK intact |
| **R-5** gate = safety net, no code change | parallel `1231→1235`, sequential `1424→1430`; reconcile `1125-1132` | parallel gate comment+`try_launch` @**`1268-1276`**; sequential gate comment @**`1462-1474`**; both reworded to "phase budget exhausted / SAFETY NET", code unchanged | **TM-9 `:424`** forced single-phase overspend trips gate (task1 PASS, 2-3 SKIPPED, phase ERROR); TM-0 asserts never-trips in phases 2-3 | OK intact (Δ) |
| **R-6** legacy wiring-input → per-phase | legacy `1939-2287`; hook `2281-2287` (`ledger=ledger`) | legacy wiring-hook `run_post_phase_wiring_hook(..., ledger=ledger)` @**`2388-2394`**; deliberate-refinement comment @2380-2387 explicitly says "pinned by TM-13 — NOT TM-7" | **TM-8 `:311`** legacy after task phase: fresh `max_turns × 1` ledger, no NameError, wiring hook runs; **TM-13** pins the wiring-input delta | OK intact (Δ) |
| **R-7** monotonicity / no in-place reset | `debit` `models.py:1048-1053`; docstring `1011-1022` | `debit` @`models.py:1056-1061`; docstring tightened to "Monotonicity is PER-INSTANCE (per-phase)" @`models.py:1018-1020` | **TM-6 `:960`** asserts `hasattr(TurnLedger,'reset') is False` AND `'reallocate' is False` AND consumed non-decreasing | OK intact |
| **R-8** python/skip never touch ledger | `1819-1820` (python), `1823-1834` (skip) | python `continue` @`1879-1880`; skip `continue` @`1883-1894`; R-2 ctor sits AFTER both | **TM-11 `:516`** exactly one `TurnLedger.__init__`; skip → SKIPPED/exit 0 | OK intact (Δ) |
| **R-9** thread-safety K>1 | parallel fan-out def `1158`, gate `1231`, join `1288-1289`; `models.py:1036-1042` RLock | `__post_init__` RLock `models.py:1036-1042`; K-2 invariant stated in R-2 ctor comment @`1912-1919` | **TM-12** `test_turn_ledger_concurrency.py:44` `test_try_launch_admits_exactly_task_count_under_kgt1` — `2×task_count` fan, exactly `task_count` succeed | OK intact |
| **R-10** sprint-cumulative wiring accumulator | construct @`1782`; add after `1917`/`2287`; pass @`2417`; reader `kpi.py:192-197` | `_SprintWiringTotals` dataclass `executor.py:335-358`; instance @**`1842`** (next to `shadow_metrics` @1832); task add-site @**`2009-2014`**; legacy add-site @**`2400-2406`**; arg-swap `turn_ledger=sprint_wiring_totals` @**`2540-2543`**; reader `kpi.py:192-197` | **TM-13 `:613`** `wiring_analyses_run==5` (3+2 sprint-cumulative), used==5≠2, credited==20≠8 | OK intact (Δ — pass-site moved 2417→2543) |

---

## Prompt-Mandated Spot-Checks (each explicitly requested)

| Mandated link | Result | Evidence |
|---|---|---|
| **R-3 → TM-0** | CONFIRMED | TM-0 `test_per_phase_budget.py:217-222` asserts `inst.initial_budget == 500` and `available_at_entry == 500` per phase — the R-3 core invariant at `--max-turns 100 × 5 tasks`. |
| **R-6 → TM-8 + TM-13** | CONFIRMED | TM-8 `:311` pins fresh `max_turns × 1` legacy ledger + wiring-hook-runs; TM-13 `:613` pins the wiring-input delta. The R-6 code comment @`executor.py:2383` itself states "pinned by TM-13 — NOT TM-7". |
| **R-9 → TM-12** | CONFIRMED | `test_turn_ledger_concurrency.py:44` sizes `task_count × minimum_allocation`, fans `2 × task_count`, asserts exactly `task_count` succeed. |
| **R-10 → TM-13** | CONFIRMED | TM-13 drives 3+2 analyses, asserts persisted `gate-kpi-report.md` reports `Analyses run: 5`, `Turns used: 5` (≠2), `Turns credited: 20` (≠8) — the accumulator, not last-phase ledger. |
| **R-8 → TM-11** | CONFIRMED | `test_per_phase_budget.py:516` spies `TurnLedger.__init__`, asserts exactly 1 construction; skip phase → `PhaseStatus.SKIPPED, exit_code=0`. Note: accumulator is `_SprintWiringTotals`, NOT a `TurnLedger`, so the `__init__` spy correctly does not count it (test docstring @524 confirms this reasoning). |
| **R-5 → TM-9** | CONFIRMED | `test_per_phase_budget.py:424`: 1 phase × 3 tasks, task1 consumes 28 of 30-pool → task1 PASS, tasks 2-3 SKIPPED, `remaining=={T01.02,T01.03}`, phase ERROR. Genuine within-phase overspend, not cross-phase. |
| **K-1 pinned by TM-13 (NOT TM-7)** | CONFIRMED | Spec §8 K-1 + R-6 verification both route K-1 (legacy late-phase wiring delta) to TM-13; code comment @`executor.py:2383-2384` reiterates "pinned by TM-13 — NOT TM-7 (TM-7 covers only the byte-equivalent subprocess execution log and cannot detect this wiring-input delta)". TM-7 `test_multi_phase.py:185-194` docstring independently states it "cannot and must not detect" the wiring delta. The two ends agree. |
| **K-2 pinned by R-2 construction-site comment** | CONFIRMED | K-2 sequential-phase invariant is stated verbatim in the R-2 ctor comment @`executor.py:1912-1919` ("K-2 SEQUENTIAL-PHASE INVARIANT (load-bearing precondition for R-9): phases run serially..."). Spec §8 K-2 requires exactly this placement. |
| **K-3 pinned by pre-merge grep artifact** | CONFIRMED | `phase-outputs/discovery/k3-premerge-grep.txt` (raw, 22 hits) + `k3-grep-summary.md` (classification: all 22 EXPECTED, only kpi.py:192-197 + the R-10 add-sites + model writers). Grep command matches spec §8 K-3 verbatim. Summary itself notes the `executor.py:2417→2543` drift. |

---

## Chain-Link Defects (Findings)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `merged-requirements-FINAL.md` R-2 (`executor.py:1838-1839`) vs live `1920-1923` | Spec prose line-anchor for the R-2 fresh-ledger construction is ~82 lines stale. The LINK exists and is correct; only the cited line number drifted (the +144-line R-10 additions pushed it down). | Re-anchor R-2 to `executor.py:1920-1923` (or accept — the spec's own header §"Do not implement without re-confirming anchors" + the anchor-map artifact already flag re-Read-at-edit). |
| 2 | MINOR | Spec R-10 / §7 (`pass @2417`) vs live `2540-2543` | KPI build pass-site cited as `executor.py:2417`; actually at `2540-2543`. The chain is intact; the K-3 grep-summary already records this exact drift ("now `2543` after Phase 2 edits"). | Re-anchor; non-blocking — already documented downstream. |
| 3 | MINOR | Spec R-10 add-sites ("after `1917`" / "after `2287`") vs live `2009-2014` / `2400-2406` | The two read-only add-sites are cited relative to pre-edit line numbers. Both add-sites VERIFIED present and correct (read-only summation into `sprint_wiring_totals`). | Re-anchor; non-blocking. |

**No CRITICAL or IMPORTANT findings.** No chain link is missing, dangling, or
mis-wired. Every R-item maps to a concrete code edit AND ≥1 TM test; every
mandated K-risk pin is present at the cited artifact. The line-anchor drift is
benign because (a) the spec explicitly self-warns to re-Read anchors at edit
time, (b) the anchor-map discovery artifact recorded "all MATCH" against the
pre-edit baseline, and (c) the K-3 summary already tracks the post-edit shift.

---

## Adversarial Floor — Did I find 5 broken links?

The prompt instructed me to assume ≥5 broken links and find them. I traced all
10 R-items, all 14 TM rows referenced, all 3 K-risk pins, plus every model
method, and found **zero broken (non-existent) chain links**. Three MINOR
anchor-drift defects surfaced — these are stale *coordinates*, not broken
*links*: the target code/test exists at a verifiable location in every case.

I am NOT manufacturing broken-link findings to satisfy the floor. Reporting
3 genuine MINOR drift defects + an honest "no missing links" is the correct
adversarial outcome here, because the implementation phase (Phase 2-5) already
ran an anchor-map anti-drift gate and a K-3 pre-merge grep, both of which
caught and recorded the drift. The chain is sound.

---

## Self-Audit

**(a) Reliance list — items relied on from upstream verdicts:**
- Relied on the Phase 2-5 output summary's "46/46 tests pass; ruff clean" claim
  for test-GREEN status (I did not re-run pytest). I independently verified the
  test *content* (assertions exist and exercise the right behavior) by reading
  each test body.
- Relied on the anchor-map / K-3 artifacts existing — verified by `ls` + reading
  the K-3 summary directly.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Read `executor.py:1824-1923` and confirmed the R-2 fresh-ledger ctor + K-2
  comment + `else 1` floor exist at `1920-1923` / `1912-1919` — not relied on
  the spec's `1838` anchor.
- Read `executor.py:2380-2406` + `2530-2546` and confirmed both R-10 add-sites
  and the `turn_ledger=sprint_wiring_totals` arg-swap exist live — not relied
  on the spec's `1917`/`2287`/`2417` anchors.
- Read `models.py:1052-1125` and confirmed `available()`, `debit_wiring`,
  `credit_wiring` exist and `reset`/`reallocate` do NOT (TM-6's claim).
- Read `kpi.py:192-197` and confirmed the three-field read contract the
  accumulator is shaped to.
- Read `test_per_phase_budget.py` end-to-end (764 lines) and confirmed each TM
  body's assertions match its R-item.

---

## Confidence

**Verified:** 21/21 chain links (10 R-items + 3 K-pins + 8 mandated spot-checks, de-duplicated) | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

**Tool engagement:** Read: 7 | Grep: 0 | Glob: 0 | Bash: 6 (grep/ls/sed read-only)

Tool-call count (13) ≥ checklist link count is satisfied; each Read/Bash call
targeted a specific chain link (executor regions, models, kpi, each test file,
the K-3 artifact directory). No web research was performed (all verification was
local-file-bound), so no Tavily fallback applies.

---

## Recommendations

1. (MINOR, optional) Re-anchor the spec's R-2 / R-10 line numbers to the live
   post-implementation coordinates before archiving the spec, OR rely on the
   spec's existing "re-Read at edit time" self-warning. Non-blocking for merge.
2. No code or test changes required — every chain is intact.

---

## QA Complete

**Overall Verdict: PASS** — all requirement→code→test chains trace end-to-end;
3 MINOR anchor-drift advisories, 0 broken links, 0 CRITICAL/IMPORTANT.
