# QA Report — research-depth (RE-VERIFICATION, gap-fill round 1)

**Phase:** research-depth (r2 re-verification)
**Lens:** research-depth
**Date:** 2026-06-21
**fix_authorization:** false
**Stance:** Adversarial — assume superficial until proven otherwise.

---

## Scope of this re-verification

Prior research-depth pass FAILED on ONE MINOR issue:
- R5 (`05-template-and-citations.md`) cited the prior task file at a path dropping a directory level.
- Real file is nested: `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`
- Gap-fill researcher wrote `research/06-gap-fill.md`.

Verifying:
1. Does `06-gap-fill.md` correct the prior-task-file path + confirm OI-1 table / QA CRITICAL #2 / consolidated-findings under the nested dir? (Confirm nested path exists myself.)
2. Is GAP-2 design recommendation DEEP enough to drive per-item task construction without guessing?
3. Overall: is the research set now build-ready at depth?

---

## Q1 — Does 06-gap-fill.md correct the prior-task-file path + confirm the nested artifacts?

**YES — fully resolved, and I independently confirmed the filesystem.**

The prior MINOR was: R5 cited the prior **task FILE** at a path dropping one directory level.
06-gap-fill.md §"GAP-FIX — R5 path correction" (06:284-313) handles exactly this:

- Asserts CORRECT = nested `…/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`; WRONG = flat sibling.
- I verified both via `ls`/`test -f`:
  - NESTED task file EXISTS (162969 bytes) — confirmed.
  - FLAT sibling `…/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md` MISSING — confirmed.
- The three downstream artifacts 06 names, all verified to EXIST this round:
  - OI-1 table → `…/20260620-024238/phase-outputs/discovery/oi1-mapping-table-validated.md` (EXISTS)
  - QA CRITICAL #2 → `…/20260620-024238/qa/qa-content-ensemble-formation-correctness-report.md` (EXISTS)
  - Consolidated R6 rejection → `…/20260620-024238/qa/qa-consolidated-findings.md` (EXISTS)

**Nuance I checked (and 06 gets right):** in `05-template-and-citations.md`, the *sub-artifact*
citations (05:158/181/195) were ALREADY nested-correct. The drift was ONLY in the prior-task-FILE
references (05:88/89/98/101/104 use the bare `…024238.md` filename). 06's correction directive
(06:308-313) is precisely scoped: nest the task-FILE citation; keep `parent_task` as the bare ID
(an identifier, not a path). That directive is correct and unambiguous for the builder.

**Q1 verdict: PASS.** Path corrected to the nested form; all three sub-artifacts confirmed on disk.

---

## Q2 — Is the GAP-2 design recommendation DEEP enough to drive per-item task construction?

**YES — this is build-ready depth, not hand-waving.** I re-verified every load-bearing anchor 06
cites against live source; all match exactly:

| 06 claim | Anchor | Verified |
|---|---|---|
| seam is score-only today | `ensemble.py:72` `AdversarialScoreFn = Callable[..., float \| None]` | exact |
| scorer lossy return | `ensemble.py:271` `return extract_convergence_score(parse_adversarial_contract(output_dir))` | exact |
| seam call site assigns a float (2 branches) | `ensemble.py:223-231` default + fn branches | exact |
| builder called with only path+score+unavailable | `ensemble.py:234-239` | exact |
| builder hard-codes all-zero counts | `deviation_count_by_class {authorized:0,necessary:0,drift:0,regression:0}` | exact |
| builder hard-codes the 4 booleans False | `regression_present/unauthorized_deviation_present/needs_human_decision/user_decision_required = False` | exact |
| null-convergence → DEGRADE rung 2 | `contract.py:284` `tier_reached==2 and …score is None → "null-convergence"` | exact |
| regression → HALT rung 3 | `contract.py:315` `regression_present is True → "regression"`; count fallback `:323` | exact |
| HALTED exit 10 / DEGRADED exit 11 | `models.py:38-49` map; `test_u6` asserts it | exact |

The recommendation gives the builder everything needed WITHOUT guessing:
1. **Concrete dataclass shape** — 6 named fields with types (06:55-57).
2. **Exact lockstep widen set** — `AdversarialScoreFn` (`:72`), `run_adversarial_scorer`
   (`:244-271`), `build_reflect_contract` (`:360-407`), naming the literal hard-codes to replace.
3. **Honest disposition table** (06:84-91): per field, WIRED+LIVE vs WIRED-but-default-clean-
   pending-producer, each with its source anchor. This is the decisive depth — it tells the builder
   which fields can carry real values now (`adversarial_convergence_score`, `report_path`) and which
   must default clean because the score-only child cannot supply them (the 3 booleans + per-class
   counts), citing R2's zero-hit grep as the reason.
4. **The producer FOLLOW-ON is correctly fenced OUT of scope** (OQ-PRODUCER, 06:102-114) — it
   touches the sc-adversarial SKILL surface, a separate component. Prevents the builder from
   inventing producer-emission items.
5. **GAP-4 non-conflation rule** (06:140-157): do NOT auto-derive `regression_present` from a low
   convergence threshold — that would misroute reviewer DISAGREEMENT (exit 11, retryable) as a found
   REGRESSION (exit 10, blocking). A real semantic trap; 06 explicitly REJECTS the R2 feasibility
   option for it. Verified against the live ladder: convergence feeds ONLY rung-2 `null-convergence`;
   `regression_present` is an independent rung-3 trigger.
6. **The headline TEST is concretely specified** (06:72-80): inject an `AdversarialResult` with
   `regression_present=True` + non-None `convergence_score` (so DEGRADE doesn't fire first and mask
   the HALT), assert HALTED/exit-10. `regression_present` must be a genuine `bool`
   (`_LOAD_BEARING_BOOL_FIELDS`, verified present in `contract.py`).

**Backward-compat (GAP-1) is build-ready too** — I verified every test anchor:
- `_const_score -> float` at `test_ensemble_stub_integration.py:39-41` (the ONE mechanical break),
  injection sites `:93/:331/:356` — confirmed.
- Both autospec spies `:420/:445` patch `run_tier2_ensemble` (NOT the score-fn) and assert
  `call_args.args[0] is config2` / `assert_not_called` — agnostic to the seam widen. Confirmed.
- `runner.py:425` calls `run_tier2_ensemble(config)` positionally, no score-fn kwarg → P6 production
  path insulated. Confirmed.
- `AdversarialScoreFn` referenced only within `ensemble.py` (`:72`, `:142`). Confirmed via repo grep.

**FR-RH2.7 proof (GAP-5) is concrete and runnable** — `git diff` over `contract.py`+`models.py`
must be empty; place `AdversarialResult` in `ensemble.py` to keep `models.py` byte-clean (internally
consistent with the diff command). `test_u6` frozen-ordering guard verified present at
`test_ensemble_unit.py:178-201` asserting BLOCKED→DEGRADED→HALTED→PASS order + exit codes.

**Q2 verdict: PASS.** Deep enough to build per-item without guessing. The disposition table +
non-conflation rule + fenced producer follow-on are exactly the depth a builder needs to avoid the
two traps (wiring phantom producer fields; conflating low-convergence with regression).

---

## Q3 — Is the research set now build-ready at depth?

**YES.** With 06-gap-fill.md added, all five original gaps are closed with verified anchors, the R5
path MINOR is corrected (nested form, confirmed on disk), the scope FORK is explicit and defensible
(wire+test now; producer emission as OQ-PRODUCER follow-on), and the HALT-vs-DEGRADE semantic
separation is pinned against the live first-match ladder. Every code/test/path anchor I independently
re-checked matched 06's claims with zero discrepancies.

One observation (not a defect): 06 is the load-bearing file — 05's prior-task-FILE citations remain
in their flat form in 05 itself, but 06's GAP-FIX explicitly overrides them with a correction
directive, and the task builder consuming this research set will read 06 last (Status: Complete) as
the authoritative reconciliation. Acceptable for a gap-fill round; the override is unambiguous. If
the builder cited 05 directly WITHOUT 06's directive it could reintroduce the flat path — but that
is a builder-discipline matter, and 06 names the exact lines to override.

---

## Self-Audit

**(a) Reliance list — items where I relied on the prior-pass structural verdict:**
- Relied on the prior research-depth pass's PASS on GAP-1/3/4/5 *structure* (section presence,
  anchor formatting) — I did NOT re-audit document structure; that was the prior pass's job.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Re-verified `ensemble.py:72` alias is `float | None` (score-only) — live-source read.
- Re-verified builder hard-codes (`deviation_count_by_class` all-zero + 4 booleans False) in the
  `build_reflect_contract` body — `sed -n 360,407p`.
- Re-verified `contract.py:284` null-convergence DEGRADE vs `:315` regression HALT on distinct rungs.
- Re-verified `Verdict.HALTED.exit_code==10`/`DEGRADED==11` at `models.py:38-49` + `test_u6` guard.
- Re-verified backward-compat: `_const_score -> float` (`:39-41`), spies patch `run_tier2_ensemble`
  not the score-fn (`:420/:445`), `runner.py:425` positional `config`, `AdversarialScoreFn` single-module.
- Independently confirmed on disk: nested prior-task file EXISTS, flat sibling MISSING, 3 sub-artifacts EXIST.

**Confidence:** Verified: 3/3 questions | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 1 | Bash(grep/fs/sed): 4
**Web research:** none required (all verification local-file-bound) — Tavily not invoked.

---

## VERDICT: PASS

All three verification questions PASS. 06-gap-fill.md correctly nests the prior-task-file path
(filesystem-confirmed: nested EXISTS, flat MISSING, 3 sub-artifacts EXIST), and its GAP-2 design
recommendation is build-ready depth — every load-bearing `ensemble.py` / `contract.py` / `models.py`
/ test anchor re-verified against live source with zero discrepancies. The scope fork
(wire+test now; producer emission as OQ-PRODUCER follow-on) and the HALT-vs-DEGRADE non-conflation
rule are correct and defensible. The research set is now build-ready at depth.

Nothing remains.
