# Feature Dependency Matrix — Phase 5 Synthesis

**Task:** T05.01 — Merge verdicts & reconcile inter-feature dependencies
**Roadmap Item:** R-016
**Tier:** STANDARD
**Generated:** 2026-05-15
**Inputs:** `stack-rank.md` (T04.05) + nine `debate-*.md` files (T04.01–T04.03) + `gate-pass-report.md` (T04.04) + `extension-point-contracts.md` (T03.02).

**Purpose:** Surface every inter-feature dependency in the Phase 4 verdict set — features where an ADOPT depends on a DEFER, where ADOPT(A) implies REJECT(B), where two ADOPT features share an attach surface, or where a cluster-aggregate verdict diverges from its sub-feature verdicts. For every conflict, declare an explicit precedence resolution naming the winner, the rationale, and the consequence for the loser. Confirm no resolution silently re-litigates a Phase 4 verdict (R-RULE-11).

---

## 1. Verdict Inventory (terminal Phase 4 set)

Counts after the Phase 4 gate pass and stack-rank disposition:

| Verdict | Count | Stack-rank rows |
|---|---|---|
| ADOPT | 9 | 1, 2, 3, 4, 5, 6, 7 (MERGE-WITH-GATE-1), 8, 9 |
| ADAPT | 3 | 10, 11 (MERGE-WITH-GATE-2), 12 |
| DEFER | 7 + 4 catalog-derived = 11 | 14, 15, 16, 17, 18, 19, 23, 33, 37, 42, (16 = same feature as 15) |
| REJECT | 8 + 11 catalog-derived = 19 | 13, 20, 21, 22, 24, 25, 26, 27, 28 (Strategy axis), 29, 30, 31, 32, 38, 39, 40, 41, plus catalog rows 28a/30/35/36 (subsumed, not independent) |

(The DEFER row count above lists 11 to include row 16 — Gate 3 — which is the second view of D27/Layer B already counted as row 15. Treat as one feature, two stack-rank views.)

**Per R-RULE-11, none of these verdicts may be silently changed in Phase 5.** Where a precondition is now met by a later ADOPT, the resolution must explicitly preserve the Phase 4 verdict and route any potential upgrade to a future re-debate (Phase 6/7 or a future sprint), not perform the upgrade silently here.

---

## 2. Dependency Map — ADOPT/ADAPT chains (no conflict; sequencing only)

These are dependency relationships *within the ADOPT/ADAPT set* where one feature requires another to function but the relationship is harmonious — both are in-scope, the dependency is a build-order or merge-order constraint for Phase 6/7, not a verdict conflict.

| # | Dependent feature | Depends on | Nature of dependency | Both in-scope? |
|---|---|---|---|---|
| DM-1 | Row 6 — Gate 1 (Dispatch) — ADOPT | Row 3 — D09a `Tier:` field — ADOPT | Gate 1 reads the `Tier:` value introduced by D09a; without the field, Gate 1 has nothing to dispatch on. Bidirectional with DM-2. | Yes |
| DM-2 | Row 3 — D09a `Tier:` field — ADOPT | Row 6 — Gate 1 (Dispatch) — ADOPT | Without Gate 1, D09a is inert metadata (no consumer); R-RULE-07 manifest exception #6 binds them: "ship together or ship neither." Bidirectional with DM-1. | Yes |
| DM-3 | Row 7 — D10 Command-side dispatch — ADOPT | Row 6 — Gate 1 (Dispatch) — ADOPT | Structurally identical; explicit MERGE-WITH-GATE-1. No separate Phase 6 implementation work; D10 row exists only for donor traceability. | Yes |
| DM-4 | Row 11 — D15a Layer 2 verification subset — ADAPT | Row 10 — Gate 2 (Verification routing) — ADAPT | Same surface; explicit MERGE-WITH-GATE-2. No separate Phase 6 implementation work. | Yes |
| DM-5 | Row 10 — Gate 2 (Verification routing) — ADAPT | Row 3 (D09a) + Row 6 (Gate 1) — both ADOPT | Tier-conditioned budget needs the `Tier:` value (D09a) and the dispatch surface (Gate 1) to know when to widen `rf-qa`'s budget vs use the existing one. | Yes |
| DM-6 | Row 8 — TFEP Test baseline (D21) — ADOPT | Row 3 (D09a) + Row 6 (Gate 1) — both ADOPT | R-RULE-07 manifest exception #4 binds baseline collection to STRICT/STANDARD only — requires the `Tier:` field and Gate 1 dispatch. Without tier-gating, baseline cost falls on every `/task` invocation including LIGHT typo fixes (uniform-cost-without-uniform-value failure mode, R-RULE-06 adjacent). | Yes |
| DM-7 | Row 9 — TFEP Escalation trigger (D22) — ADOPT | Row 8 — TFEP Test baseline (D21) — ADOPT | Escalation classification (Pre-existing vs New failing test) consumes the baseline snapshot D21 produces; without baseline, the "any pre-existing fails" trigger has no comparator. | Yes |
| DM-8 | Row 4 — TFEP Permitted exceptions (D20) — ADOPT | Row 2 — TFEP Prohibition rules (D19) — ADOPT | Carve-outs are exceptions to the D19 VIOLATION rules; D20 has no semantic without D19 to carve out from. Co-located at Error Handling (extension-point row 8). | Yes |
| DM-9 | Row 5 — TFEP Incident reporting (D24) — ADOPT | Rows 2, 4, 8, 9 (TFEP cluster ADOPT subset) | Incident-report schema (Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts) records the side-effects of the TFEP cluster; without the cluster firing, there is no incident to report. Tier-gated to STRICT items with test-failure history (transitively requires DM-6). | Yes |
| DM-10 | Row 12 — D15b Layer 2 pre-flight scaffolding — ADAPT | Row 3 (D09a) + Row 6 (Gate 1) — both ADOPT | Tier-gated additive setup (STRICT: serena+git+codebase-retrieval+memory; STANDARD: codebase-retrieval; LIGHT/EXEMPT: skip) requires the `Tier:` field and Gate 1 dispatch. R-RULE-07 manifest exception #5 binds this as additive pre-loop setup, not in-EXECUTE substitution. | Yes |
| DM-11 | Row 1 — Critical/Trivial Path Override (D17+D18) — ADOPT | None (path-glob-based; classification-independent) | Co-located at Task File Validation surface (extension-point row 1) with Gate 1 and the D09a validator, and at Phase-Gate QA surface (extension-point row 10) with Gate 2 — but explicitly fires regardless of `Tier:` value. See ordering precedence in §3 conflict CR-7. | n/a |

**No dependency cycle in the ADOPT/ADAPT set.** DM-1 ↔ DM-2 is a "ship together" co-dependency, not a runtime cycle (both files are edited in the same merge). All other chains are linear: D09a + Gate 1 → {Gate 2, TFEP Baseline, D15b}; TFEP Baseline → TFEP Escalation; TFEP Prohibitions → TFEP Carve-outs; TFEP cluster → TFEP Incident reporting.

**Build-order implication for Phase 6:** D09a + Gate 1 land first (or in the same change). Gate 2 / TFEP Baseline / D15b layer on top. TFEP Escalation lands after TFEP Baseline. TFEP Carve-outs land in the same change as TFEP Prohibitions. TFEP Incident reporting lands last in the TFEP cluster.

---

## 3. Conflict Register — explicit precedence resolution per item

Each row below is a verdict tension that requires an explicit decision. Precedence resolution names the winner, the rationale, and the consequence for the loser. Where the loser is a Phase 4 verdict, the resolution preserves it under R-RULE-11.

### CR-1 — Compliance-gating cluster aggregate (Row 14, DEFER) vs sub-gate verdicts (Rows 6, 10, 16, 22)

- **Tension:** Row 14 (`Compliance-gating cluster aggregate`, V=4 C=3 K=5 Net=2.4) is DEFER "cluster-as-written," but the four sub-gates each have independent verdicts: Gate 1 (Row 6) ADOPT, Gate 2 (Row 10) ADAPT, Gate 3 (Row 16) DEFER, Gate 5 (Row 22) REJECT.
- **Apparent conflict:** If the cluster is DEFER, may any sub-gate be ADOPTed?
- **Precedence resolution: SUB-GATE VERDICTS WIN.** The cluster-aggregate row is an audit roll-up over the cluster-as-written ceremony (the donor's full coordination layer, four-gate package, and write-back contracts). The DEFER on Row 14 means *do not import the cluster-as-written package with its coordination ceremony*. The sub-gate verdicts are the operative transfer decisions for `transfer-manifest.md`. This is consistent with R-RULE-06 ("absorb patterns, not implementation mass") — the cluster's coordination ceremony is the implementation mass; the per-gate behaviors are the patterns.
- **Rationale:** `stack-rank.md:36` explicitly carries Row 14 with the parenthetical "(cluster-as-written; sub-gates separate)" — the verdict structure is built on the assumption that cluster vs sub-gates are independent decisions. `debate-compliance-gating.md` scores each sub-gate with its own V/C/K to enable this very split.
- **Consequence for loser:** The "loser" here is the *cluster-as-written package*. It is not transferred. The sub-gates carry their individual verdicts. The cluster-aggregate row remains in `rejected-features-ledger.md` with its DEFER precondition (the precondition being "cluster-as-written ceremony imported as a unit" — which Phase 5 explicitly rules out, so the DEFER is effectively terminal).
- **R-RULE-11 audit:** No verdict changed. Row 14 stays DEFER; sub-gate verdicts stay as scored. This resolution interprets the relationship between aggregate and sub-gates without re-scoring either.

### CR-2 — TFEP cluster aggregate (Row 17, DEFER) vs sub-feature verdicts (Rows 2, 4, 5, 8, 9, 20, 23)

- **Tension:** Row 17 (`TFEP cluster-aggregate`, V=3 C=3 K=4 Net=2.25) is DEFER "cluster-as-written," but five sub-features ADOPT (Rows 2/4/5/8/9), one DEFERs pending `/sc:forensic` (Row 23), and one REJECTs (Row 20).
- **Apparent conflict:** Same shape as CR-1.
- **Precedence resolution: SUB-FEATURE VERDICTS WIN.** Same pattern as CR-1. The TFEP cluster-as-written includes Step 5 (heading insertion — F4 collision risk) and Step 6 (resume-from-inserted-task — INV-01 collision) that Phase 4 narrowed out via per-sub-feature scoring. The cluster aggregate DEFER preserves the principle "do not import the donor's seven-step TFEP-as-designed wholesale"; the sub-feature ADOPTs are the absorbable subset (D19/D20/D21/D22/D24).
- **Rationale:** `stack-rank.md:39` carries Row 17 with the parenthetical "(cluster-as-written; sub-features separate)." `debate-tfep.md:110` explicitly scores TFEP "as a cluster with per-sub-feature sub-verdicts because the seven donor sub-features (D19-D25) have independently shaped values, costs, and admissibility."
- **Consequence for loser:** The "loser" is the cluster-as-written package (the donor's full seven-step flow including D23 Step 5 + Step 6 and D25 escalation budget). It is not transferred. The five ADOPT sub-features carry forward. Row 17 remains in `rejected-features-ledger.md` with the same termination logic as CR-1.
- **R-RULE-11 audit:** No verdict changed.

### CR-3 — D27/Layer B + Gate 3 (Rows 15+16, DEFER) precondition now met by Gate 1 ADOPT

- **Tension:** `stack-rank.md:38` records Row 16 as "**DEFER → ADAPT if Gate 1 ADOPTed**." Gate 1 IS ADOPTed (Row 6). Reading literally, the verdict should now be ADAPT.
- **Apparent conflict:** Phase 4 verdict (DEFER) vs precondition-now-met arithmetic (Net would rise from 2.25 to 3.0 with K dropping from 4 to 3 once Gate 1 supplies the tier source).
- **Precedence resolution: PHASE 4 VERDICT (DEFER) WINS in Phase 5. Re-classification is forbidden under R-RULE-11; Phase 6/7 may explicitly re-open this debate with a re-debate note.**
- **Rationale:** R-RULE-11 forbids silent verdict changes. The "DEFER → ADAPT if Gate 1 ADOPTed" annotation in Row 16 is a *forward-looking note for a future debate*, not a license for Phase 5 to perform the upgrade arithmetically. Phase 5's job is to merge and reconcile, not to re-debate. The arithmetic upgrade (K 4→3 due to Gate 1 supplying tier source) also relies on a soft cost estimate that should face adversarial scrutiny in a fresh debate, not be absorbed via a footnote.
- **Consequence for loser:** D27/Layer B + Gate 3 (one feature, two stack-rank views) remain DEFER. They appear in `rejected-features-ledger.md` with the precondition narrative updated to: *"Gate 1 ADOPTed (precondition met). A fresh adversarial re-debate in a future sprint may now re-score with K=3, Net=3.0 (ADAPT band). Phase 5 does not perform this upgrade — R-RULE-11 forbids silent re-classification."* This is the explicit re-debate note R-RULE-11 requires.
- **R-RULE-11 audit:** Verdict preserved. The re-debate note is the explicit acknowledgment that the precondition is met but verdict change is deferred to a re-opened debate.

### CR-4 — D31 catalog REJECT (Success Criteria metrics table) vs D09a ADOPT

- **Tension:** `stack-rank.md:72` (catalog row 41) carries D31 as REJECT with rationale "metrics measure D08/D09/D15; nothing to measure if those are not adopted." D09a is ADOPTed (Row 3). Strict reading of the rationale: a fragment of D31 *could* now measure D09a uptake.
- **Apparent conflict:** Phase 4 carry-forward verdict (REJECT) vs precondition-partially-met arithmetic (one of three referenced features is now in scope).
- **Precedence resolution: PHASE 1 / PHASE 4 CARRY-FORWARD VERDICT (REJECT) WINS.**
- **Rationale:** D31's NON-TRANSFERABLE tag in the donor catalog is keyed to the *donor's whole metrics package* (success metrics for the donor's classifier, header emission, and tier-keyed branching layer), not to any single field. With D09b REJECTed (Row 21) and D15c REJECTed (Row 26) and D08 DEFERed (Row 19), the metrics package's measurement targets are not in scope. A new "measure D09a uptake" feature would be a fresh proposal in a future sprint, not a partial absorption of D31. R-RULE-11 forbids silent re-classification; R-RULE-06 forbids absorbing ceremony (a metrics table) without behavioral teeth (the measurement targets it scores).
- **Consequence for loser:** D31 stays REJECT in `rejected-features-ledger.md` with the unchanged rationale. If a future sprint wants telemetry on `Tier:` field uptake, it raises a new feature proposal — not a re-litigation of D31.
- **R-RULE-11 audit:** Verdict preserved. The asymmetry (one of three referenced features now in scope) is noted explicitly without triggering re-scoring.

### CR-5 — D14 catalog DEFER (confidence display) vs split precondition state

- **Tension:** `stack-rank.md:64` (catalog row 33) carries D14 as DEFER with precondition "depends on D08/D09a/D09b; if D08 ADAPTs in a future sprint, debate D14 as a downstream presentation layer." D09a is ADOPTed (Row 3 — half-precondition met); D08 is DEFER (Row 19 — half-precondition unmet); D09b is REJECT (Row 21 — third-precondition terminally unmet).
- **Apparent conflict:** Mixed precondition state — does D14 still DEFER, or escalate to REJECT now that D09b is terminally REJECTed?
- **Precedence resolution: D14 STAYS DEFER (verdict preserved); precondition narrative tightened.**
- **Rationale:** D14's value claim hangs on a confidence number to display, which D08 (classification header emission) supplies. D08 is DEFER, not REJECT — its precondition (downstream parser shipping) is still tractable. D14 inherits D08's precondition: *"re-debate D14 if and when D08 ADOPTs in a future sprint, with the explicit understanding that D09b REJECT is terminal so D14's input must come from a different classifier (e.g., the `task-builder`-side classifier that D09b was routed to)."* Under R-RULE-11, no verdict change in Phase 5; the precondition narrative is sharpened to reflect the terminal D09b REJECT.
- **Consequence for loser:** D14 stays DEFER in `rejected-features-ledger.md` with the updated precondition.
- **R-RULE-11 audit:** Verdict preserved. The precondition narrative is sharpened (informational), not re-scored.

### CR-6 — R-RULE-07 subjective override on Row 13 (D02/Layer A)

- **Tension:** Row 13 (D02/Layer A `mcp-servers:` frontmatter, V=1 C=5 K=2) has arithmetic Net=2.5, which falls in the DEFER band (1.5 ≤ Net < 3). Phase 4 verdict is REJECT under an explicit R-RULE-06 override (ceremony without behavioral teeth — no in-repo consumer for the `mcp-servers:` frontmatter list).
- **Apparent conflict:** Arithmetic verdict (DEFER) vs override verdict (REJECT).
- **Precedence resolution: R-RULE-06 OVERRIDE (REJECT) WINS. Phase 5 reviewer re-affirms the override per R-RULE-07 (subjective overrides must be explicit, named, and re-affirmable).**
- **Rationale:** R-RULE-06 ("absorb patterns, not implementation mass") gives the rubric explicit license to REJECT a feature whose ceremony has no consumer, regardless of arithmetic Net. The override is documented in `stack-rank.md:131` and `stack-rank.md:249` and was already flagged for Phase 5 reviewer affirmation. Re-affirming preserves the override; T05.03's `transfer-manifest.md` will carry this as a "manifest exception" entry (R-RULE-07 requirement) so the override survives the manifest's terminal lock.
- **Consequence for loser:** D02/Layer A stays REJECT in `rejected-features-ledger.md` with the R-RULE-06 rationale carried forward verbatim. The arithmetic-vs-override divergence is the named justification.
- **R-RULE-11 audit:** Verdict preserved. The override was already a Phase 4 verdict, not a Phase 5 change.

### CR-7 — Row 1 (Critical/Trivial Path Override) co-located with Gate 1 (Row 6) at Task File Validation surface

- **Tension:** Row 1 (Path Override) and Row 6 (Gate 1) both attach to extension-point row 1 (Task File Validation gate, C5; `extension-point-contracts.md:60-67`). Row 1 explicitly fires "regardless of Tier value" (path-glob-based, classification-independent — `stack-rank.md:144`); Row 6 reads `Tier:` (D09a, Row 3) and routes execution shape based on the value. Same surface, both ADOPT, but they need an ordering decision: which fires first?
- **Apparent conflict:** Same attach point, two ADOPT features. Without an ordering rule, Gate 1 might dispatch a STRICT-tier task to the full F1 + Phase-Gate QA pipeline, then Row 1's critical-path override would have to retroactively force-escalate within a stance Gate 1 already chose.
- **Precedence resolution: PATH OVERRIDE FIRES FIRST.** Order at the Task File Validation surface is: (a) Row 1 path-glob check sets a forced-stance flag if the task touches the critical-path-glob set or fits entirely within the trivial-path-glob set; (b) D09a validator parses the `Tier:` field; (c) Gate 1 dispatch reads the `Tier:` field AND any forced-stance flag from (a) — forced-stance from path override wins over `Tier:` value when both are set.
- **Rationale:** Row 1's design rationale is "safety floor that survives a wrong `Tier:` value" — a reviewer who marks an `auth/`-touching task as `Tier: LIGHT` should still get the STRICT pipeline. Inverting the order (Gate 1 first, then Row 1 retro-correction) creates a window where Gate 1 has already begun a wrong-stance dispatch, defeating the safety floor's purpose. This is consistent with the Position A argument in `debate-compliance-gating.md` for the cluster's safety-floor value.
- **Consequence for loser:** Neither feature is "lost." Both are ADOPTed; the resolution is an ordering rule encoded in the integration sketch. Phase 5's `integration-sketches.md` (T05.02) must lock this order in the Row 1 + Row 6 sketches: the Task File Validation gate runs `path_override_check → tier_field_validate → gate_1_dispatch` in sequence.
- **R-RULE-11 audit:** No verdict changed. This resolution is an integration-order constraint, not a verdict reassessment.

### CR-8 — Row 1 (Path Override) co-located with Gate 2 (Row 10) at Phase-Gate QA surface

- **Tension:** Same shape as CR-7 but at a different surface. Row 1 (Path Override, ADOPT) attaches to extension-point row 10 (Phase-Gate QA, C3) as a "forced-escalation pre-check on STRICT items touching the critical path-glob set, and a forced-de-escalation pre-check for LIGHT/EXEMPT items inside the trivial path-glob set" (`stack-rank.md:141`). Row 10 (Gate 2, ADAPT) attaches to the same surface as a tier-conditioned budget widening.
- **Precedence resolution: PATH OVERRIDE FIRES FIRST AT PHASE-GATE QA AS WELL.** Order: (a) Row 1 path-glob check determines the effective stance for THIS Phase-Gate QA invocation (force-escalate if STRICT task is in critical-path-glob; force-de-escalate if LIGHT/EXEMPT task is fully within trivial-path-glob); (b) Gate 2 reads the effective stance and selects the budget/timeout accordingly.
- **Rationale:** Same as CR-7 — the override exists to be a safety floor that the stance selector cannot ignore. If Gate 2's budget choice ignored the override, the override would not actually achieve forced escalation/de-escalation.
- **Consequence for loser:** Same as CR-7 — both ADOPTed, ordering encoded in T05.02 integration sketches. The Row 10 sketch must read the Row 1 path-override flag before selecting budget.
- **R-RULE-11 audit:** No verdict changed.

### CR-9 — Manifest exception #6 (`Tier:` + Gate 1 ship together) creates a build-order obligation

- **Tension:** R-RULE-07 manifest exception #6 (`stack-rank.md:244`) binds D09a (Row 3) and Gate 1 (Row 6) to "ship together or ship neither." If Phase 6 implementation lands D09a first without Gate 1, D09a is inert metadata (no consumer), which would re-trigger an R-RULE-06 ceremony-without-teeth concern.
- **Apparent conflict:** Two ADOPT verdicts that are independently scored but operationally inseparable.
- **Precedence resolution: BIND AS A SINGLE TRANSFER UNIT IN THE MANIFEST.** T05.03's `transfer-manifest.md` must list D09a and Gate 1 as a single transfer unit (e.g., "TM-Unit-1: D09a `Tier:` field + Gate 1 dispatch") with a single observable post-condition. The manifest exception entry from `stack-rank.md:244` carries forward verbatim into T05.03.
- **Rationale:** Both verdicts remain ADOPT (no R-RULE-11 violation). The "single transfer unit" framing is an integration constraint, not a verdict change. It enforces the load-bearing INV-safety commitment without re-scoring.
- **Consequence for loser:** No loser; this is a binding constraint on Phase 6 sequencing.
- **R-RULE-11 audit:** No verdict changed.

### CR-10 — Manifest exception #1 (PRE-LOOP DISPATCH) constrains Gate 1's integration

- **Tension:** R-RULE-07 manifest exception #1 (`stack-rank.md:239`) binds Gate 1 (Row 6) and D10 (Row 7, MERGE-WITH-GATE-1) to fire "once at task-entry, never per-item inside F1 EXECUTE." Per-item per-tier dispatch is auto-REJECT under INV-01.
- **Apparent conflict:** Phase 4 ADOPT verdict on Gate 1 stands, but the implementation surface includes a temptation (per-item dispatch) that would auto-REJECT under INV-01.
- **Precedence resolution: PRE-LOOP DISPATCH ONLY. Bind as a manifest exception.** T05.03's `transfer-manifest.md` must carry this constraint verbatim alongside the Gate 1 / D10 / D15b / TFEP-Baseline transfer entries.
- **Rationale:** Same shape as CR-9 — the constraint preserves the verdict by forcing the implementation into the INV-safe variant.
- **Consequence for loser:** No verdict change; per-item dispatch variant is auto-REJECTed for any Phase 6 implementation that attempts it.
- **R-RULE-11 audit:** No verdict changed.

### CR-11 — Manifest exception #2 (`rf-qa` SUPPLEMENTED NOT REPLACED) constrains Gate 2's integration

- **Tension:** R-RULE-07 manifest exception #2 (`stack-rank.md:240`) binds Gate 2 (Row 10) and D15a (Row 11, MERGE-WITH-GATE-2) so that `quality-engineer` is *additional*, not a replacement for `rf-qa`. Replacing `rf-qa`'s adversarial stance is auto-REJECT under INV-03.
- **Precedence resolution: SUPPLEMENT ONLY. Bind as a manifest exception in T05.03.**
- **Rationale:** Same shape as CR-9/CR-10.
- **Consequence for loser:** No verdict change; the replacement variant is auto-REJECTed.
- **R-RULE-11 audit:** No verdict changed.

### CR-12 — Manifest exception #3 (SIDE-CHANNEL ONLY, NO F1 HALT) constrains TFEP cluster integration

- **Tension:** R-RULE-07 manifest exception #3 (`stack-rank.md:241`) binds the TFEP ADOPT subset (Rows 2, 4, 5, 8, 9) so that prohibition + classification + incident-report side-effects fire without halting F1. Halting F1 on TFEP engagement is auto-REJECT under INV-01.
- **Precedence resolution: SIDE-CHANNEL ONLY. Bind as a manifest exception in T05.03.**
- **Rationale:** Same shape as CR-9/CR-10/CR-11. The TFEP cluster's INV-01 safety hangs on this constraint.
- **Consequence for loser:** No verdict change; the F1-halting variant is auto-REJECTed.
- **R-RULE-11 audit:** No verdict changed.

### CR-13 — Manifest exception #5 (NO PER-ITEM EXECUTE SUBSTITUTION) constrains D15b and explicitly REJECTs D15c

- **Tension:** R-RULE-07 manifest exception #5 (`stack-rank.md:243`) binds D15b (Row 12, ADAPT) as additive pre-loop setup, NOT in-EXECUTE substitution. The constraint also explicitly REJECTs any D15c (Row 26) variant that would attempt per-item synthesis (already REJECTed at Net=0.4 in Phase 4).
- **Apparent conflict:** D15b's tier-gated steps look superficially like the per-tier synthesis pattern D15c carries; without explicit binding, a Phase 6 implementer could unify them.
- **Precedence resolution: D15b IS PRE-LOOP ONLY; D15c REMAINS REJECT. Bind as a manifest exception in T05.03 that covers both.**
- **Rationale:** Same shape as CR-9–CR-12. The constraint preserves the D15b ADAPT verdict by forcing the implementation into the INV-safe additive-setup variant; the D15c REJECT verdict remains terminal.
- **Consequence for loser:** No verdict change. The per-item synthesis variant is auto-REJECTed.
- **R-RULE-11 audit:** No verdict changed.

### CR-14 — Manifest exception #4 (BASELINE TIER-GATED) is the operative form of DM-6

- **Tension:** R-RULE-07 manifest exception #4 (`stack-rank.md:242`) binds TFEP Baseline (Row 8, ADOPT) to STRICT/STANDARD only. This is the operative INV-safety form of DM-6 (above).
- **Precedence resolution: TIER-GATED ONLY. Bind as a manifest exception in T05.03.**
- **Rationale:** Same as DM-6; restated here as a conflict register entry because the binding is a Phase 6 integration constraint, not just a sequencing note.
- **Consequence for loser:** No verdict change; uniform-baseline-on-every-task variant is auto-REJECTed.
- **R-RULE-11 audit:** No verdict changed.

### CR-15 — Manifest exception #7 (D08 DEFERRED UNTIL PARSER SHIPS) is independent — flagged for Phase 5/6 awareness

- **Tension:** R-RULE-07 manifest exception #7 (`stack-rank.md:245`) binds D08 (Row 19, DEFER) to remain DEFER until a downstream parser ships. The constraint is forward-looking, not a Phase 5 conflict.
- **Precedence resolution: D08 STAYS DEFER. Carry the manifest exception into T05.03's `rejected-features-ledger.md` as the named DEFER precondition.**
- **R-RULE-11 audit:** No verdict changed.

### CR-16 — Manifest exception #8 (D01 DEFERRED UNTIL LOADER SEMANTICS + CRITICAL RULE 6 SPLIT) is independent — flagged for Phase 5/6 awareness

- **Tension:** Same shape as CR-15. R-RULE-07 manifest exception #8 (`stack-rank.md:246`) binds D01 (Row 18, DEFER) to remain DEFER until two preconditions are met.
- **Precedence resolution: D01 STAYS DEFER. Carry the manifest exception into T05.03's ledger as the named DEFER precondition.**
- **R-RULE-11 audit:** No verdict changed.

---

## 4. Cross-attach-point map (informational)

The following extension-point rows host more than one ADOPT/ADAPT feature. T05.02 must lock the stance ordering on each surface; CR-7 and CR-8 above resolve the two cases where ordering matters.

| Extension-point row | Surface | Co-attached features | Ordering rule |
|---|---|---|---|
| Row 1 (C5) | Task File Validation gate | Row 1 (Path Override), Row 3 (D09a Tier validate), Row 6 (Gate 1 dispatch) | Path Override → Tier validate → Gate 1 dispatch (CR-7) |
| Row 2 (C5) | First Item Protocol | Row 8 (TFEP Baseline), Row 12 (D15b pre-flight scaffolding) | Tier check → D15b scaffolding (STRICT/STANDARD) → TFEP Baseline (STRICT/STANDARD). Both tier-gated; both consume the `Tier:` value Gate 1 read at the previous surface. Order between D15b and Baseline is implementation-detail (no conflict — both are setup steps; suggested: D15b first because it activates serena/codebase-retrieval that the rest of the task uses, Baseline last because it produces the comparator file Row 9 will consume on first failure). |
| Row 4 (C3) | F1 EXECUTE item-type dispatch | Row 3 (D09a per-item Tier read) | Single attach — no co-located feature; D09a per-item read is purely additive, falls back to task-level when item-level annotation absent. |
| Row 8 (C5) | Error Handling / blocker logging | Row 2 (TFEP Prohibitions D19), Row 4 (TFEP Carve-outs D20), Row 9 (TFEP Escalation triggers D22) | Prohibitions → Carve-outs (carve-outs are exceptions to prohibitions) → Escalation triggers (consume baseline + classify failures). All side-channel; no F1 halt (CR-12). |
| Row 10 (C3) | Phase-Gate QA | Row 1 (Path Override forced-stance pre-check), Row 10 (Gate 2 budget widening) | Path Override → Gate 2 stance/budget selection (CR-8). |
| Row 11 (C5) | Post-Completion Validation | Row 5 (TFEP Incident reporting D24) | Single attach — no co-located feature. |
| Row 13 (C5) | Required frontmatter schema slot | Row 3 (D09a `Tier:` field) | Single attach. (D01 / Row 18 DEFER would also attach here if ADOPTed in a future sprint.) |

---

## 5. R-RULE-11 audit — no silent re-litigation

Per R-RULE-11, no Phase 4 verdict may be silently changed by Phase 5. Every conflict resolution above either:

(a) preserves the Phase 4 verdict outright (CR-1, CR-2, CR-4, CR-5, CR-6, CR-9, CR-10, CR-11, CR-12, CR-13, CR-14, CR-15, CR-16);
(b) imposes an integration-order or build-order constraint that does not change any verdict (CR-7, CR-8); or
(c) preserves the Phase 4 verdict while adding an explicit re-debate note authorizing a future sprint to re-open the debate (CR-3).

**Verdict-change count for Phase 5: ZERO.** Verdict-preserving precondition narrative updates: TWO (CR-3 D27/Layer B + Gate 3; CR-5 D14). Re-debate notes: ONE (CR-3 D27/Layer B + Gate 3).

---

## 6. Acceptance Criteria Recap (T05.01)

1. **`feature-dependency-matrix.md` exists and lists every inter-feature dependency and conflict from the Phase 4 verdict set.** ✅ — Section 2 enumerates 11 dependency-map entries (DM-1 to DM-11) covering the ADOPT/ADAPT chain. Section 3 enumerates 16 conflict-register entries (CR-1 to CR-16) covering every cluster-aggregate-vs-sub-feature divergence (CR-1, CR-2), every precondition-shift case (CR-3, CR-4, CR-5), the R-RULE-07 subjective override (CR-6), every co-attach ordering case (CR-7, CR-8), and every R-RULE-07 manifest exception that constrains an ADOPT/ADAPT integration (CR-9 to CR-16).

2. **Every conflict has an explicit precedence resolution naming winner, rationale, and consequence for the loser.** ✅ — All 16 CR entries include (a) tension statement, (b) precedence resolution naming the winner, (c) rationale citing source artifacts, (d) consequence for the loser, (e) R-RULE-11 audit line.

3. **No Phase 4 verdict is silently changed; any change carries an explicit re-debate note (R-RULE-11).** ✅ — Section 5 audit confirms zero verdict changes in Phase 5. The one case where a precondition is now operationally met (CR-3, D27/Layer B + Gate 3, with Gate 1 ADOPTed) carries an explicit re-debate note authorizing future re-opening, not a silent upgrade.

---

## 7. Hand-off to T05.02 — required integration-sketch lock-ins

T05.02's `integration-sketches.md` must encode the following constraints derived from this matrix:

| Source CR | T05.02 lock-in |
|---|---|
| CR-7 | Row 1 + Row 3 + Row 6 sketches: Task File Validation surface order is `path_override_check → tier_field_validate → gate_1_dispatch`. |
| CR-8 | Row 1 + Row 10 sketches: Phase-Gate QA surface order is `path_override_check → gate_2_stance_select`. |
| CR-9 | Row 3 + Row 6 sketches: bind as a single transfer unit ("ship together or ship neither"). |
| CR-10 | Row 6 + Row 7 sketches: PRE-LOOP DISPATCH only (auto-REJECT per-item variant). |
| CR-11 | Row 10 + Row 11 sketches: `quality-engineer` SUPPLEMENTS, never replaces, `rf-qa`. |
| CR-12 | Rows 2, 4, 5, 8, 9 sketches: SIDE-CHANNEL ONLY, NO F1 HALT. |
| CR-13 | Row 12 sketch: pre-loop additive only; explicit anti-pattern note rejecting any D15c-style per-item synthesis. |
| CR-14 | Row 8 sketch: TIER-GATED to STRICT/STANDARD; auto-REJECT uniform-baseline variant. |
| DM-2 / DM-1 | Row 3 + Row 6: ship together (operational form of CR-9). |
| DM-7 | Row 9 sketch: depends on Row 8 having executed for the task. |
| DM-8 | Row 4 sketch: carve-outs co-located with prohibitions (Row 2). |
| DM-9 | Row 5 sketch: depends on TFEP cluster ADOPT subset firing. |

T05.03's `transfer-manifest.md` execution order must respect the dependency map (Section 2) — D09a + Gate 1 lead, Gate 2 / TFEP Baseline / D15b layer on top, TFEP cluster lands as a coherent block, Path Override lands at any time (no upstream dependency on the other ADOPTs since it is classification-independent).

T05.03's `rejected-features-ledger.md` entries for D27/Layer B (Rows 15+16), D14 (catalog row 33), D02/Layer A (Row 13), D08 (Row 19), and D01 (Row 18) must carry the precondition narratives or override justifications written in the corresponding CR entries above.
