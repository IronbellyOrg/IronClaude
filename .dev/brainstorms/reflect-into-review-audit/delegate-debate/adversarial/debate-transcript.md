# Adversarial Debate Transcript — Delegate-to-reflect vs Keep-bespoke

## Metadata
- Depth: deep (R1 parallel · R2 folded into mutual concessions · R2.5 invariant probe · R3 skipped — rationale below)
- Convergence: ~0.78 (per-target CONVERGED; framework-policy resolved-by-augmentation)
- Focus: integration-fit, overlap/circularity, token-cost, maintainability, framework-scale monoculture
- Advocates: 3 independent agents (V1 pro-delegate · V2 keep-bespoke · V3 rubric)

## Round 1 (summary)

### V1 advocate (PRO delegate / consolidate)
- Argued reflect is a mechanism-superset; DRY at framework scale; rigor-for-free for future protocols; disjoint-context property caught R0/PR#112.
- **Capitulated substantially:** conceded (1) for both named targets delegation is the weaker call (cleanup-audit circular; auggie-review recall≠precision); (2) cost needs tier-routing; (3) monoculture real and irreducible; (4) **A-002 is a legitimate brake — "the standing pattern should not be adopted until reflect's contract is frozen/versioned"**; (5) on A-003, forced to "always delegate *except reflect itself*" — a reflexive carve-out. V1's blanket form did not survive.
- Shared assumptions: A-001 QUALIFY (claims hurts V3 more), A-002 REJECT-as-currently-true, A-003 REJECT (forces reflexive exception).

### V2 advocate (KEEP bespoke)
- Four load-bearing points: bespoke validators do *different jobs* (blind recall ≠ deviation audit ≠ citation gate, U-003); circular `audit-validator` reuse; framework-scale **monoculture / correlated failure** (U-001); coupling to a moving target.
- Conceded: N bespoke = more maintenance (DRY real); auggie-review's same-context Read is a real blind spot (fix in-place); a blanket "never" is wrong — some future applied-work protocol genuinely fits reflect.
- Shared assumptions: A-001 REJECT (qualified; fail-closed to bespoke on ambiguity), A-002 REJECT (sharpest factual win), A-003 REJECT (highest-value; universal delegation = unverified verifier).

### V3 advocate (CONDITIONAL rubric)
- The 4-gate rubric (G1 input-type · G2 no circular reuse · G3 property preservation · G4 cost-vs-stakes) *derives* "keep both" for the targets and *permits* delegation for a future auto-apply protocol. Argued V3 is the superset containing V1's and V2's true claims as gate conditions; "V2 IS the rubric minus the procedure."
- Conceded honestly: over-engineering IF all protocols are human-gated recommendations (then V2's blanket "keep" is simpler); the rubric "rots to always-keep-bespoke without an owner"; G1 decidability is its load-bearing joint.
- Shared assumptions: A-001 QUALIFY (decidable at extremes, per-stream split for mixed), A-002 QUALIFY (instability argues FOR per-protocol gating), A-003 QUALIFY (V3 uniquely *preserves* watchers — later refuted by INV-002).

## Round 2 (folded)
The steelman + shared-assumption sections cross-rebutted. Convergence emerged: **(i) reject blanket V1; (ii) keep bespoke for both targets (unanimous); (iii) delegation = gated exception (V2 and V3 nearly merged — V2's "rare exception bar" = V3's gates).** The binding residual became framework-structural (does the rubric actually control monoculture?), which Round 2.5 adjudicates.

## Round 2.5: Invariant Probe
See `invariant-probe.md`. 9 findings; **4 HIGH + UNADDRESSED** — all vindicating V2's framework-monoculture thesis at a structural level:
- **INV-001 (HIGH):** rubric gates per-protocol; monoculture is aggregate. N locally-correct delegations sum to monoculture; no gate measures concentration.
- **INV-002 (HIGH):** A-003's "preserve watchers" is nominal — surviving bespoke validators verify their *own* protocols, never cross-check reflect-on-Y. The only validator of reflect is reflect.
- **INV-003 (HIGH):** the rubric green-lights delegation for the applied-work category that is its reason-to-exist; success condition = monoculture trigger.
- **INV-004 (HIGH):** auggie-review already uses reflect as sole blocking validator at Phase E (`SKILL.md:327`); "keep auggie-reviewer" doesn't cover that seam — forbidden failure mode already live.
- MEDIUM: INV-005 (stale gate verdicts on contract change), INV-006 (unowned default unsafe for high-stakes auto-apply), INV-007 (zero exhibited delegate-side members — evidence to date favors V2's blanket "keep"), INV-008 (A-002 freeze is prose, no mechanism). LOW: INV-009 (G4 cost figure unvalidated, double-count for audit).

## Round 3: SKIPPED (rationale)
The 4 HIGH items are *structural* (a per-protocol gate cannot measure an aggregate property; nominal watchers cannot be argued into watching). More advocate rounds cannot dissolve them — only an added framework-level mechanism can. The merged verdict resolves them by *augmenting* the base rubric with V2-derived framework invariants (below), not by further debate.

## Scoring Matrix
| Diff Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 (default for all future protocols) | V3→merge | 70% | Procedure generalizes; but rubric alone insufficient (INV-001/003) → needs aggregate guard |
| C-002 (bespoke = subset of reflect?) | V2 | 88% | Different jobs: recall≠precision (`context.md` §5); confirmed by probe |
| C-004 (treatment of two targets) | V2/V3 (tie) | 92% | Keep both — unanimous, survives probe |
| X-001 (DRY win vs coupling liability) | V2 | 75% | Coupling to moving target real (A-002); INV-008 freeze is prose-only |
| X-002 (delegation preserves value?) | V2 | 85% | No for both targets (recall lost; audit circular) |
| X-003 (rigor vs monoculture) | V2 | 82% | Probe vindicated monoculture: INV-001/002/003 |
| A-003 (who validates validator) | V2 | 85% | INV-002: watchers never watch reflect; unmitigated |
| U-002 (the rubric) | V3 | 72% | Right scaffold for "all future" but necessary-not-sufficient |

## Convergence Assessment
- Per-target ("keep both bespoke"): **CONVERGED** (~0.95) — unanimous, both tested members fail the gates, survives probe.
- Framework-policy: the rubric does NOT independently converge (4 HIGH invariants). The **merged verdict** (V3 rubric scaffold + V2 framework-level invariants + V1's narrow applied-work kernel) resolves all 4 HIGH items by augmentation. Net ~0.78.
