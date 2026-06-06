# Adversarial Debate Transcript

## Metadata
- Depth: deep (Rounds 1–2, Round 2.5 invariant probe, Round 3 conditional)
- Rounds completed: 2 + invariant probe + 1 targeted Round 3 (X-001)
- Convergence achieved: 0.82
- Convergence threshold: 0.75 (brainstorm PASS line 0.65)
- Advocate count: 4 (variant-3 absent — vendor failure; `fallback_mode: true`)
- Adjudication: orchestrator (opus) on real, re-Read-grounded variants + 2 codebase verifications (§17.7, cli.pipeline). Note opus-adjudication bias risk vs the gpt-5.5 variant-5 was mitigated by deciding X-001 on **cited spec evidence**, not rhetoric — and the decisive call (§17.7) favors the gpt-5.5/V5 + V4/V2 position over the opus-V1 position, i.e. against the adjudicator's own model family.

## Round 1 — Advocate Statements (steelman-first)

### V1 (opus:architect) — shared sub-spec + scaffolding
**Position:** Specify the detector ONCE in `refs/reuse-audit.md` (versioned contract), both protocols reference it; this dogfoods the extract-shared verdict. Add §10.8 with a `deviation_count_by_class.reuse_miss` bin and a §14.5.2 cond-4b gate.
**Steelman of others:** V4's gate-mapping is elegant; V2's metric is more falsifiable than my hash; V5's exclusions are sharper than my single 0.60 floor.
**Concession:** my §10.8-as-counted-category may collide with an existing taxonomy decision — I did not verify §17 before proposing a 5th bin.

### V2 (opus:analyzer) — falsifiable Ω metric, evidence-grounded
**Position:** The duplicate evades every gate because it is *spec-conformant* and *name-divergent*. The only reliable signal is a behavioural-skeleton overlap (Ω), 55% on I/O-skeleton+idempotency, verb-stop-listed, with every finding re-Read-cited. Worked example: Ω(`_bind_specs`,`_inject_provenance_fields`)=0.88; a name match scores 0.
**Steelman:** V4 is right that a finding needs a *home* and an escalation rail; a metric with nowhere to go is inert. V5's exclusion list operationalizes my "verb-stop-list" more completely.
**Concession:** I under-specified WHERE the verdict blocks vs advises — V4 owns that.

### V4 (opus:architect, gate-placement) — advisory↔blocking ladder
**Position:** The real gap is that a reuse miss has *no home in any gate*. Make Reuse-Miss a **finding modifier** mapping onto existing §10.3 Drift / §10.4 Regression *by evidence* (like §10.4's exit-code rule), riding the unmodified §14.5.2 gate + §5.3 rule-3 escalation — ZERO new gate machinery. Separate `overlap` from `confidence`; block only at L3 (overlap≥0.75 ∧ confidence≥0.85 ∧ verdict≠distinct). Pre=ADVISORY-BLOCKING-PREVIEW, post=BLOCKING. auggie-down caps findings at advisory L2.
**Steelman:** V2's Ω is a better `overlap` definition than my sketch; V5's exclusions and Grounding-Gaps routing harden my L0 suppression; V1's shared-contract packaging is the right delivery vehicle.
**Concession:** my overlap formula was thin — adopt V2's CFP.

### V5 (sonnet/gpt-5.5:analyzer) — precision + exclusions
**Position:** A gate users distrust gets disabled. Require **capability AND shape floors simultaneously** (S_reuse≥0.82 ∧ C_cap≥0.80 ∧ C_shape≥0.70), an explicit 7-item exclusion list, and route maybe-related/insufficient-grounding to **Grounding Gaps**, never a hard finding. Confusion matrix proves the FP cases stay silent.
**Steelman:** V4's advisory/blocking ladder is the right disposition layer for my tiers; V2's CFP is my structural_skeleton made rigorous; V1's shared ref is where my exclusions live.
**Concession:** my "pre-stage can block" carve-out is riskier than the others' pre=always-advisory; willing to narrow it.

## Round 2 — Rebuttals
- **On X-001 (5th class vs modifier):** V4 rebuts V1: "a counted reuse_miss class re-opens a decision the protocol may already have closed — verify §17 before adding a bin." V1 accepts the burden of proof. V2/V5 align with V4 (orthogonal/signal, not a class).
- **On thresholds (C-001):** V5 rebuts the single-floor variants: "a composite ≥0.80 alone admits a high-auggie/low-capability false positive; require per-dimension floors." V2 concedes the per-dimension floor strengthens falsifiability without changing the Ω=0.88 ground-truth result.
- **On N=2 cross-module (C-002):** V4 holds that cross-pipeline duplication is the expensive, hard-to-undo case and deserves blocking-eligibility; V2 counters with the rule-of-three (N=2 can be a reasonable local choice). Partial convergence: blocking-eligible at N=2 *only* under the full L3 conjunction + Drift-by-evidence; advisory otherwise.
- **On pre-stage blocking (C-005):** V1/V2/V4 hold pre=always-advisory; V5 narrows its carve-out to "advisory-strong with a recommended verdict," conceding pre-stage should not hard-block a design doc.

## Round 2.5 — Invariant Probe (fault-finder, 6 categories incl. sufficiency challenge)

| ID | Category | Assumption probed | Status | Severity | Evidence |
|----|----------|-------------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | "Adding a 5th counted deviation class (V1) is admissible" | **UNADDRESSED→RESOLVED** | HIGH | sc-reflect §17.7 item 6 (L1742) **rejects** a 5th deviation category; L964/L1629 reinforce. V1's bin is non-conforming. Decisive for X-001. |
| INV-002 | sufficiency_challenge | "The neighbour-search step ALONE catches the duplication" | PARTIAL | MEDIUM | Holds for new/changed *functions*; a new *file/module* duplicate is only caught if candidate enumeration includes file-granularity (only V5 does). Merge must include module-level candidates (A-003). |
| INV-003 | state_variables | "The pre→post advisory-to-blocking *bridge* (V1 ×1.1 multiplier / V4 PREVIEW→BLOCK) requires the pre-stage finding to reach the post run" | UNADDRESSED | MEDIUM | No guaranteed handoff channel from `/tdd` (.dev/tasks/) to a later `reflect --mode post` diff run. Mitigation: post-stage **re-detects independently**, so the block fires without the bridge; the bridge is an *enhancement*, not a dependency. Merge: keep independent re-detection load-bearing; bridge multiplier optional. |
| INV-004 | guard_conditions | "`import_allowed` from module-docstring NFR markers is sufficient" | UNADDRESSED | MEDIUM | A ban encoded only in lint/import-linter config (not a docstring) would be missed → could emit `reuse-by-import` wrongly. Mitigation: default to `mirror-shape` over `reuse-by-import` when the import-legality of a cross-package edge is *uncertain* (safe direction — never recommends a forbidden import). |
| INV-005 | collection_boundaries | "Copy-count N is cheaply available for the consolidation rule" | ADDRESSED | LOW | N approximated from the bounded neighbour-query return set (≤5) — N ≈ 1 + count(returned neighbours with overlap ≥ dup-threshold). No separate repo census needed. |
| INV-006 | interaction_effects | "Reuse-Miss interacts cleanly with the §14.5.2 promotion gate" | ADDRESSED | LOW | Modifier-maps-to-Drift/Regression (V4) means the UNMODIFIED cond-4 (`drift==0 ∧ regression==0`) already gates it — zero new gate condition, no parallel blocking path. V1's separate cond-4b is the interaction hazard (avoided). |
| INV-007 | sufficiency_challenge | "extract-shared verdict is actionable (a legal neutral home exists)" | ADDRESSED | LOW | Verified: `cli/pipeline/` exists; prd already imports it; NFR-PRD.7 bans only sprint/roadmap. X-002. |
| INV-008 | guard_conditions | "auggie makes the capability-vs-surface judgement" (A-002) | ADDRESSED | LOW | Reframed: auggie *retrieves* candidates; the *orchestrator* assigns C_cap after re-Reading the cited body (V2 §2.2 discipline). Auggie rank is ≤0.20 of the score and never decisive. |

**Invariant gate:** 1 HIGH item (INV-001) — RESOLVED in-debate by spec citation (not left unaddressed) → does not block convergence. 3 MEDIUM items carry mitigations into the refactor plan. Taxonomy levels covered: L1 (naming/threshold wording), L2 (insertion points/contract shape), L3 (gate state-mechanics, idempotency of re-detection, import-ban guards). All three covered.

## Round 3 — Targeted final argument (X-001 only, since it was the lone HIGH contradiction)
With §17.7 on the table, V1 withdraws the counted `reuse_miss` bin and adopts the modifier mapping; it retains its shared-contract + extension-points contribution. Unanimous post-Round-3 on X-001: **Reuse Miss is a finding modifier that maps onto Drift/Regression by evidence; low-confidence routes to §10.6 Grounding Gaps.**

## Scoring Matrix (per diff point)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 insertion point | V2/V5 (after step 4) | 72% | CFP needs F4 call-graph role from `find_referencing_symbols` (step 4) to build the query; placing the search at step 4.x is causally correct. Merge: step 4a. |
| S-002 / X-001 taxonomy home | V4 (modifier) + V2/V5 | 98% | §17.7 decisive; V1 conceded. |
| S-003 capability descriptor | V2 (6-facet CFP) | 80% | Most falsifiable + the only one with a worked proof; V5's card is the operational carrier. |
| S-004 shared sub-spec | V1 | 85% | Versioned `refs/reuse-audit.md` + extension points is the cleanest packaging; dogfoods extract-shared. |
| S-005 low-confidence destination | V5 (Grounding Gaps) | 95% | §17.7/§10.6 sanction this exact route. |
| C-001 thresholds | V5 (two-floor) | 82% | Per-dimension floors are the strongest FP guard; ground-truth Ω=0.88/C_cap=1.0/C_shape=1.0 still clears. |
| C-002 N=2 cross-module | split → compromise | 60% | Blocking-eligible only under full L3 conjunction + Drift-by-evidence; else advisory. |
| C-003 third block signal | V4 (`confidence` separate) | 78% | Cleanest 3-independent-signal bar; absorbs V2's N≥3 as a confidence input. |
| C-005 pre-stage blocking | V1/V2/V4 (pre=advisory) | 88% | 3/4; V5 narrowed its carve-out. |
| U-001…U-005 | accept all | 90% | All five unique contributions are additive and non-conflicting. |

## Convergence Assessment
- Points resolved: 13 of 15 (S-001..006, C-001..005, X-001..002) with U-001..005 accepted and A-001..003 dispositioned.
- Alignment: **0.82** (≥0.75 threshold; ≥0.65 brainstorm PASS).
- Status: **CONVERGED** (all taxonomy levels covered; the lone HIGH invariant INV-001 resolved by spec citation, not left unaddressed).
- Unresolved tensions (carried as advisory into merge): C-002 disposition tuning; INV-003 bridge-multiplier is optional-not-load-bearing.
