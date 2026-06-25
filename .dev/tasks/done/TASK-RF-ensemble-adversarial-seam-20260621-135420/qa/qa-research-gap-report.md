# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Wire the adversarial seam in ensemble.py — map real deviation/regression/human-decision/report_path into build_reflect_contract; add regression test asserting derive_verdict != PASS
**Date:** 2026-06-21
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Scope

Assigned files (verifying ONLY these):
- 01-ensemble-seam-inventory.md
- 02-adversarial-child-output-schema.md
- 03-contract-consumer-constraints.md
- 04-test-patterns.md
- 05-template-and-citations.md

Lens focus: find GAPS the researchers missed that would block a correct task.

---

## Verification Performed (tool evidence)

Independently re-verified every load-bearing claim against source (not trusting research prose):
- `ensemble.py:72` alias, `:136-145` signature, `:221-232` seam block, `:234-239` contract call, `:244-271` scorer, `:274-289` parse, `:292-301` prompt, `:360-407` `build_reflect_contract` (hard-coded fields confirmed byte-for-byte at 379/385-390/401-404). VERIFIED via Read.
- `contract.py:249-304` `_degraded_reason` (null-convergence trigger 11 at :284; adversarial-unavailable trigger 9 at :276), `:307-328` `_halted_reason` (regression :315/:324, drift :326). VERIFIED via Read.
- Grep over `src/`+`tests/` for `run_tier2_ensemble|run_adversarial_scorer|AdversarialScoreFn|adversarial_score_fn|_const_score|extract_convergence_score|parse_adversarial_contract`. VERIFIED caller set.
- `runner.py:425` calls `run_tier2_ensemble(config)` positional-only (production insulated). VERIFIED via Read.
- `.claude/` has NO `cli/` mirror (only skills/agents/commands sync) — confirmed `src/`+`tests/`-only task. VERIFIED via ls.
- Existing null-convergence + parse-chain test `test_ensemble_unit.py:262-291` (U10) and autospec spies `test_ensemble_stub_integration.py:420/445`. VERIFIED via Read.

---

## Findings (Gap-Detection Lens)

The five research files are genuinely high quality: dense citations, accurate file:line anchors, and the
SCORE-ONLY decisive finding (R2) is correct and load-bearing. However, the adversarial gap-detection lens
surfaced several coverage gaps the builder needs closed. These are GAPS in research coverage, not errors in
what was written.

### GAP-1 (IMPORTANT) — Backward-compat surface is INCOMPLETE: two test sites omitted

R1 §8 and R4 §7 enumerate the backward-compat surface as: the alias (L72), the seam branch (L229-232),
`run_adversarial_scorer` (L244), its body (L271), the `build_reflect_contract` call (L234-239), and the
3 stub sites (L93/331/356) + `_const_score` (L39). **Two backward-compat-affected sites are missing:**

1. **`tests/cli/reflect/test_ensemble_unit.py:262-291` (U10)** directly tests `parse_adversarial_contract`
   + `extract_convergence_score` and pins their CURRENT return semantics (asserts `extract_convergence_score`
   returns a bare float `0.33`, tolerates un-nested `{"convergence_score": 0.86}`, and `None` on missing).
   If the task widens `run_adversarial_scorer`/the parse chain to return a result object, this test's
   assertions on the helper return shapes may break or need extension. R1 §8 item 4 says L271 "must instead
   return the result object" but never flags that U10 pins the OLD shape. VERIFIED: Read of the test body.
2. **`test_ensemble_stub_integration.py:420 + :445`** use `patch.object(runner_mod, "run_tier2_ensemble",
   autospec=True)`. `autospec=True` validates call signatures against the real function. Widening
   `run_tier2_ensemble`'s signature with NEW OPTIONAL kwargs is safe for these (positional config call at
   :424 still matches), but the builder should be told explicitly so it does not change the EXISTING param
   order/names. R1 §8 lists `runner.py:425` but omits these two autospec spies.

**Why it blocks correctness:** the task's NFR guard is "keep `tests/cli/reflect -q` green without modifying
existing verdict tests" (R3 §7, NFR-RH2.6). If the builder doesn't know U10 pins the old helper shape, it may
either (a) break U10 and wrongly "fix" it, or (b) refactor the parse chain and be surprised. Remediation:
add a research note enumerating U10 and the two autospec spies as backward-compat-affected sites and state
the required preservation (extend, don't break, U10; keep `run_tier2_ensemble` existing param names/order).

### GAP-2 (IMPORTANT) — The DERIVE-vs-EXTEND decision is surfaced but NOT decided, and the four non-emitted fields lack a concrete acquisition path

Lens focus #1. R2 §4/§7 correctly proves the child emits SCORE-ONLY and lists three options (derive from
threshold / extend the producer / parse the merged report body). R5 §3.5 frames R6 as "change the oracle so
the adversarial domain supplies counts." **But no research file resolves HOW the regression test obtains a
real `regression_present=True` end-to-end through the seam.** R4 §5 sidesteps this by injecting a stub
`adversarial_score_fn` that simply RETURNS `regression_present=True` — which proves the contract-wiring half
but NOT the producer half (where does a real run's regression signal come from?).

This is a genuine design fork the builder must make and the research does not arm the decision:
- **Option A (threshold-derive `regression_present` from `convergence_score`):** R2 §7 opt 1 + the
  grader-extensions citation (`convergence_score < 0.75 OR verdict == regression_present`). This is
  immediately feasible BUT (per lens #5) RISKS MISROUTE: a low convergence score is supposed to route
  DEGRADE/null-convergence, NOT HALTED/regression. See GAP-4.
- **Option B (extend the producer to emit the deviation taxonomy):** the only path that recovers true
  per-class counts / `unauthorized_deviation_present` / `needs_human_decision`. R2 §7 opt 2 names the file
  (`<t2-adversarial>/adversarial/return-contract.yaml`) but no research traces what would have to change in
  `sc-adversarial-protocol/SKILL.md`'s Return Contract to add those fields, nor whether that is in-scope for
  a "wire the seam" task vs a producer-change task.

**Why it blocks correctness:** the TRACK GOAL says "map REAL deviation/regression/human-decision into
build_reflect_contract." If the task only widens the seam type + threads a stub-injected bool (R4's design),
the regression test passes but NO production run can ever populate `unauthorized_deviation_present` /
`needs_human_decision` / per-class counts, because the producer still doesn't emit them (R2 §4 decisive).
The builder needs an explicit decision: is R6 scoped to "widen the seam + thread fields + test via stub"
(leaving production acquisition as a documented follow-up), or must it ALSO extend the producer? Remediation:
add a research item that states the scope decision explicitly and, if production acquisition is in scope,
traces the producer-emission change. If out of scope, the task must say so and label the four non-score
fields as stub-only-for-now.

### GAP-3 (MINOR) — `--suspect-source` inert-flag finding is surfaced but its task impact is unassessed

R2 §1 flags that `build_adversarial_prompt` (ensemble.py:292-301) emits `--suspect-source` which
`/sc:adversarial` does NOT define (verified: I re-Read L292-301 — the literal `--suspect-source` is emitted).
R2 marks impact "Unverified." Since R6 may touch `build_adversarial_prompt`/the scorer, the builder should be
told whether to fix this inert flag in-scope or leave it. Not blocking (the flag is inert, debate still runs),
but a research note should classify it as out-of-scope-for-R6 so the builder doesn't rabbit-hole. Remediation:
one line classifying the inert flag as a pre-existing, separate issue.

### GAP-4 (IMPORTANT) — Regression-vs-DEGRADE misroute risk is NOT analyzed; threshold-derive could mask or misroute

Lens focus #5 (the misroute concern) is the single most important under-researched item. I VERIFIED the
ordering in `contract.py`: the ladder is blocked → degraded → halted → pass, FIRST-MATCH-WINS
(`_degraded_reason` runs BEFORE `_halted_reason`). Critically:
- `_degraded_reason` trigger 11 (`contract.py:284`): `tier_reached == 2 AND adversarial_convergence_score is
  None` → DEGRADED `null-convergence`. This fires BEFORE any halted check.
- `_halted_reason` (`contract.py:315/324`): `regression_present is True` OR `deviation_count_by_class.regression
  > 0` → HALTED `regression`.

**The misroute the research never analyzes:** If the builder chooses Option A (derive `regression_present`
from a low `convergence_score`), there are two failure modes:
1. **DEGRADE masks the derived regression:** because `_degraded_reason` runs first, if a low score ALSO trips
   a degrade trigger (single-vendor, model-diversity, null-convergence when score is None), the run routes
   DEGRADED (exit 11) and the derived regression NEVER reaches the halted stage. R4 §3/§5 only notes the
   inverse (keep score non-None so null-convergence doesn't mask) — it does NOT analyze the general
   degrade-before-halt masking for a threshold-derived regression.
2. **Semantic misroute:** a genuinely low convergence score means "reviewers disagreed" (a DEGRADE signal),
   NOT "a reviewer found a regression in the work under review." Conflating them would make every
   low-agreement run HALT as a false regression. The spec's intent (R3 §1, R5 §3.2) is that the adversarial
   VERDICT (a reviewer-found regression) drives HALT, while the convergence SCORE drives DEGRADE. No research
   file states this separation as a hard constraint on the mapping, even though lens #5 names it directly.

**Why it blocks correctness:** without this analysis the builder could implement a threshold-derive that
(a) silently never fires (masked by degrade) — making the regression test pass only because the STUB injects
the bool, not because the mapping works; or (b) misroutes low-agreement runs as false regressions.
Remediation: add a research note pinning the regression(verdict)→HALTED vs convergence(score)→DEGRADE
separation, the first-match-wins degrade-before-halt ordering, and an explicit statement that
`regression_present` must come from a reviewer-classified Regression finding, NOT from the score threshold.

### GAP-5 (IMPORTANT) — FR-RH2.7 "derive_verdict unchanged" verification is NAMED but not given a concrete proof method

Lens focus #4. R3 §5 + R5 §3.1 correctly cite FR-RH2.7's acceptance bullets ("derive_verdict and the Verdict
exit-code map are unchanged"; "existing reflect contract/verdict tests pass without modification") and R3 §7
+ R4 §6 cite the green-suite guard (`uv run pytest tests/cli/reflect -q`). **But no research file specifies
HOW to PROVE derive_verdict/the exit-map are untouched beyond "run the suite."** I VERIFIED that
`test_verdict_mapping.py:31-39` (halted_regression → HALTED/exit 10) and `:231-274` (malformed-bool guard)
already exist and pin derive_verdict — these are the regression guards FR-RH2.7 leans on. The research should
explicitly tell the builder:
1. The proof of "derive_verdict unchanged" is: `git diff` shows ZERO lines changed in `contract.py` +
   `models.py` (the FR-RH2.7 invariant is a no-touch constraint on those two files — R3 §5 says exactly this
   in prose but never converts it to a verifiable task item: "git diff contract.py models.py is empty").
2. The clean-path PASS guard (lens #4 second half): a NO-findings `build_reflect_contract` output must STILL
   yield all-zero counts + `regression_present=False` so a clean Tier-2 run PASSes. R3 §7 mentions this but
   no research file points at the EXISTING green test that proves it (`test_ensemble_stub_integration.py:140-151`
   I1 asserts PASS/exit 0 on the clean path) — the task should assert I1 stays green as the clean-path guard.

**Why it matters:** "derive_verdict unchanged" is the headline FR-RH2.7 invariant. A verification item that
says only "run the suite" is weaker than "assert git diff of contract.py + models.py is empty AND I1 stays
PASS." Without the concrete proof method, the builder may edit `derive_verdict` to add a new halted trigger
(the tempting but FORBIDDEN shortcut) and the suite might still pass. Remediation: add a verification note
specifying the no-touch git-diff proof for contract.py/models.py + the I1 clean-path-PASS guard.

### GAP-6 (RESOLVED — no gap) — sync-dev / .claude mirror

Lens focus #6. I VERIFIED via `ls .claude/` that there is NO `cli/` under `.claude/` — only skills/agents/
commands are sync-dev targets; the Python `cli/` package is imported directly, never mirrored. So this task
(editing `ensemble.py` + `contract.py` tests) is purely `src/` + `tests/` with NO sync-dev / verify-sync
step required. **This is correct, but NO research file explicitly states it** — a builder unfamiliar with the
repo could waste an item on `make sync-dev`. Classified RESOLVED (not a blocking gap) but worth a one-line
note in the task: "ensemble.py/contract.py are Python package files, not synced — no sync-dev item needed."

### Note on lens #2 / #3 (covered adequately)

- Lens #2 (backward-compat callers): R1 §8 is mostly complete; the production caller `runner.py:425`
  (positional config, insulated) is correctly identified. The two omissions are in GAP-1.
- Lens #3 (`adversarial_unavailable` / null-convergence DEGRADE fallback): R5 §3.5 (R3 row) correctly flags
  "R6's new finding-mapping must preserve this null-convergence fallback," and R4 §3/§5 reinforces keeping
  the score non-None. The PRESERVATION constraint is researched; the INTERACTION with a threshold-derived
  regression (degrade-masks-halt) is the new concern raised in GAP-4.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 5 assigned files Status: Complete + Summary | PASS | All five end with "Status: Complete" + Summary section (Read). |
| 2 | Evidence density (file:line citations) | PASS (Dense) | >80% of claims carry file:line; spot-verified 12 anchors against source. |
| 3 | Lens #1: per-class field acquisition path researched | FAIL | GAP-2: derive-vs-extend fork unresolved; no production path for 4 non-emitted fields. |
| 4 | Lens #2: backward-compat callers fully mapped | FAIL | GAP-1: U10 unit test + 2 autospec spies omitted. |
| 5 | Lens #3: null-convergence/adversarial_unavailable fallback covered | PASS | R5 §3.5 R3 + R4 §3/§5 (verified contract.py:276/284). |
| 6 | Lens #4: FR-RH2.7 derive_verdict-unchanged proof method | FAIL | GAP-5: invariant named but no concrete no-touch git-diff + clean-path proof. |
| 7 | Lens #5: regression-vs-degrade misroute analyzed | FAIL | GAP-4: degrade-before-halt masking + score-vs-verdict semantics not analyzed. |
| 8 | Lens #6: sync-dev / .claude mirror concern | PASS | GAP-6 RESOLVED: no cli/ under .claude (verified ls); src+tests only. |
| 9 | Contradiction resolution across files | PASS | R5 §3.5 explicitly reconciles the OI-1 "SYNTHESIZED" vs QA-CRITICAL-#2 "real gap" tension. |
| 10 | Citation accuracy (anchors resolve to real code) | PASS | Re-verified ensemble.py 72/221-232/234-239/360-407, contract.py 249-328. |

## Summary

- Checks passed: 6 / 10
- Checks failed: 4 (GAP-1, GAP-2, GAP-4, GAP-5)
- Critical issues: 0
- Important issues: 4
- Minor issues: 1 (GAP-3)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | R1 §8 / R4 §7 | Backward-compat surface omits `test_ensemble_unit.py:262-291` (U10, pins old helper shape) + autospec spies `test_ensemble_stub_integration.py:420/445`. | Add research note listing U10 + both spies as backward-compat-affected; state "extend not break U10; keep run_tier2_ensemble param names/order." |
| 2 | IMPORTANT | R2 §7 / R5 §3.5 | Derive-vs-extend fork unresolved; the 4 non-score fields (per-class counts, unauthorized, needs_human_decision) have no production acquisition path — child emits SCORE-ONLY (R2 §4). | Add a scope-decision research item: either declare R6 = widen-seam+thread+stub-test (mark 4 fields stub-only follow-up) OR trace the producer-emission change in sc-adversarial-protocol SKILL.md. |
| 3 | MINOR | R2 §1 (ensemble.py:299) | `--suspect-source` inert flag emitted by build_adversarial_prompt; task impact "Unverified." | One line classifying it as a pre-existing separate issue, out-of-scope for R6 (or explicitly in-scope). |
| 4 | IMPORTANT | contract.py:284 vs 315/324 | Regression-vs-DEGRADE misroute unanalyzed: degrade runs before halt (first-match-wins) so a threshold-derived regression can be masked; low score (DEGRADE) vs reviewer-found regression (HALT) conflation risk. | Add research note: regression_present must come from a reviewer-classified Regression finding NOT a score threshold; pin degrade-before-halt ordering + score→DEGRADE / verdict→HALT separation. |
| 5 | IMPORTANT | spec FR-RH2.7 / contract.py + models.py | "derive_verdict unchanged" invariant named but no concrete proof method beyond "run suite." | Add verification note: prove via empty `git diff contract.py models.py` (no-touch) + assert I1 clean-path PASS (test_ensemble_stub_integration.py:140-151) stays green. |

## Recommendations

Before synthesis/task-build proceeds, close GAP-1, GAP-2, GAP-4, GAP-5 (all IMPORTANT) and note GAP-3.
The most consequential is GAP-2 (the derive-vs-extend scope decision) coupled with GAP-4 (the misroute
analysis): together they determine whether the regression test proves a REAL mapping or just a stub round-trip.
Per research-gate policy, ALL gaps regardless of severity must be resolved before synthesis — no severity is
exempt.

## Confidence Gate

- **Confidence:** "Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 9 | Grep: 2 | Glob: 0 | Bash: 3"
  (No web research performed — all claims are intrinsically local/source-bound; Tavily-first rule not triggered.)
- Every checklist item maps to a specific Read/Grep/Bash verification cited in the Items Reviewed table.
- Tool-engagement minimum satisfied: 14 verification tool calls ≥ 10 checklist items.

VERDICT: FAIL

FAIL because 4 IMPORTANT gaps + 1 MINOR gap remain unresolved. Per the research-gate zero-tolerance rule,
any gap of any severity = overall FAIL; all five must be resolved before synthesis/task-build proceeds.

## QA Complete
