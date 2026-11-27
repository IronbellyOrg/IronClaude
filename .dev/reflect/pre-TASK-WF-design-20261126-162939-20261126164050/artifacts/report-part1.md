```yaml
contract_version: 1.9.0
status: partial                      # convergence blocked by the invariant gate (INV-014), citation sampling, coverage_degraded; no citation dropped
mode: pre
tier_reached: 2
confidence_calibrated: 0.82          # mean of the three reviewer-card calibrations (0.82, 0.79, 0.84); the first-pass card calibrated at 0.59
citations_total: 205
citations_revalidated: 190           # validator estimate (all Blocking rows, most Medium and Note rows), not an exact count
citations_dropped: 0
citations_inferred: 6
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 190` (estimate): all citations of the Blocking rows and most of the others were re-Read.
> - `citations_dropped: 0`: no drop in the sample. Two line numbers were corrected and three weak citations annotated (`artifacts/evidence-validation.md`).
> - `citations_dropped_extrapolated: 0`.
> The extrapolated value is telemetry, not a verdict.

# Reflect report (UC-1, pre-execution): plan `TASK-WF-design-20261126-162939` against its design

Run: `.dev/reflect/pre-TASK-WF-design-20261126-162939-20261126164050/`, finished 2026-11-26T17:58:52Z. Tier 2: three reviewers (analyzer on the sonnet class, qa on haiku, refactorer on opus), blind calibration on the opus class (degraded diversity: every class was also a reviewer), a two-round debate through `sc-adversarial-protocol` (convergence 37 of 37 points, base = the opus card) and an invariant probe, then an evidence-validator pass.

**Verdict: the plan is not ready to run as written. 11 blocking findings, 14 medium, 10 notes.** The plan's structure and coverage are sound (170 of 199 design ids named in the plan text, the rest are covered by named tasks or are not active requirements), but 11 defects would make `/sc:implement` halt, loop, or ship wrong behavior: a Constraint that bans text the plan must write, a task-order break (Task 19 before Task 20), plugin copies left to the last task while existing parity tests run earlier, two existing tests that pin text the plan changes (`_TRANSIENT` reasons, the halt-line allow-list), a ledger reader that refuses a header-only ledger, a missing `skipped` settlement action, missing T-04 and T-21 cases, a missing `.dev/implement/` exclusion, and two acceptance checks that cannot pass (Task 24 repo-wide scan, Task 25 `git ls-files`).

Unresolved: the Round 2.5 invariant probe left INV-014 (a halt-line allow-list test) UNADDRESSED at HIGH when the debate converged, so the convergence gate is BLOCKED_BY_INVARIANTS and the adversarial status is partial; it is carried as finding M-07. Open item O1 (DD-11 reading) awaits the owner; both readings fail closed.

Where things are: reviewer cards `reviewer-cards/`; calibrations `reviewer-cards/*-calibration.md`, `artifacts/t1-calibration.md`; debate `adversarial/adversarial/` (diff analysis, Round 1 and 2, probe, scoring, base selection, refactor plan, merge log); coverage `artifacts/coverage-pass2-ranges.json`.

---

