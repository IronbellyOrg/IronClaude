# Adversarial Debate Transcript — Cross-Environment Calibration-Failure Causes

**Depth**: quick (Round 1 only; Round 2, Round 2.5, Round 3 skipped per `--depth quick`)
**Variants**: 2 — V1 (pr86-substrate run, this environment) vs V2 (T4-substrate run, other environment)
**Generated**: 2026-05-27T00:32Z

---

## Round 1: Advocate Statements

### Advocate for V1 (pr86-substrate run)

**Position summary**: V1's merge is the deeper diagnosis. It decomposes the calibration failure into multiplicatively-compounding mechanisms (M1×M2), a verdict-direction asymmetry (M3a), two orthogonal information-channel adjuncts (M3b/M3c), and an eval-suite prevention layer (M4). It cites verbatim arithmetic from the actual pr86 calibration artefacts (`tier2-RCA-calibration.md:11-17`: evidence-grounding=0.5 + four 1.0s = 0.90). This is empirical-arithmetic grounding that V2 cannot match because V2's substrate had no calibration artefacts on disk.

**Steelman of V2**: V2's #1 cause (calibrator non-execution) is empirically irrefutable on its substrate — the `ls` returning "no such file or directory" is mechanically unambiguous. V2 is right that *on the T4 substrate* the dominant failure mode is enforcement-of-protective-layer, not internal-rubric-math. V2's layer taxonomy (audit/generation/design/assignment) is also analytically valuable; V1 lacks this dimension.

**Strengths claimed**:
1. **Mechanism depth**: M1 + M2 multiplicative compounding analysis (variant-1 lines 175-179) is structurally novel; V2 lists co-causes but does not explain why each is independently insufficient.
2. **Numeric specificity**: V1 cites `(0.5+4×1.0)/5=0.90` arithmetic verbatim on the actual substrate (variant-1 line 43, lines 51-52). V2 reasons about "self-report passed through unchecked" without arithmetic because its substrate had no calibration on disk.
3. **Compositional fix-sequencing**: V1 specifies that M3a presupposes M2's Runtime-check dimension (variant-1 line 187), so fixes must ship in order. V2 lists co-equal fixes without ordering constraints.
4. **M4 prevention layer**: V1's pin-test prescription (variant-1 lines 165-168) addresses regression of *all* other fixes — unique to V1, structurally additive value.
5. **Recursion-of-anti-pattern framing**: V1 (variant-1 line 183) shows the calibrator is failing the *same* way pr86's code failed (silent-green coverage of structurally-unverifiable predicates) — isomorphic verification that the diagnosis is real.

**Weaknesses identified in V2**:
1. V2 does NOT name M4 (eval-suite silent-green coverage). Without pin tests, V2's fixes regress silently on the next eval-corpus expansion.
2. V2 does NOT decompose M3 into the three independent sub-mechanisms — collapses to a single "refute-vs-confirm asymmetry." Loses M3b (falsification-standard card field) and M3c (dual-instance-minimum) as independently-deployable fixes.
3. V2 does NOT analyze fix-sequencing — implies all five fixes are co-equally deployable.

**Concessions**:
- V1 implicitly assumes the calibrator EXECUTED on its substrate. If the empirical-verification step V2 ran (`ls tier2-*-calibration.md`) were applied to V1's substrate and returned empty, V1's entire M1/M2/M3a/M3b/M3c stack would be reasoning about an artefact that didn't exist.
- V1 missed the calibrator-non-execution failure mode entirely — even as a possibility to rule out.

### Advocate for V2 (T4-substrate run)

**Position summary**: V2 leads with empirical-disk verification. It does not theorize about how the calibrator's math fails; it observes the calibrator did not run at all. On the T4 substrate, the 0.95 (H3) and 0.85 (H2) are agent self-reports passed through the audit layer unmodified. Every downstream rubric-math discussion is moot until enforcement of the protective layer is restored. V2 also names the agent-domain-mismatch failure (refactoring-expert assigned a runtime CLI-dispatch hypothesis) — a class V1 misses.

**Steelman of V1**: V1 has access to actual calibration artefacts on the pr86 substrate. Its arithmetic citation `(0.5+4×1.0)/5=0.90` is mechanically incontestable on that substrate. V1's M1×M2 multiplicative-compounding analysis is structurally deeper than anything V2 produces. V1's M4 pin-test prescription is uniquely valuable as a prevention layer.

**Strengths claimed**:
1. **Empirical-disk verification**: V2 ran `ls .../tier2-*-calibration.md` (variant-2 lines 13, 28-29, 91) and got "no such file or directory." This is the highest-fidelity evidence in the entire comparison — a file-system fact, not an inferred mechanism.
2. **Calibrator-non-execution as #1 cause**: Universal blast radius — "every hypothesis card in every troubleshoot run is silently unguarded" (variant-2 line 25). V1's entire M1/M2/M3 stack is downstream of this — if the calibrator doesn't run, none of the rubric-math fixes matter.
3. **Layer taxonomy**: V2 (audit/generation/design/assignment) gives a clean conceptual frame for prioritizing fixes. V1 mixes mechanism-layer with fix-layer.
4. **INV-002 partial-calibration handling**: V2 explicitly carries this open invariant forward (variant-2 lines 94-98) — what happens when SOME cards are calibrated and others aren't? V1 ignores this entirely.
5. **Agent-domain mismatch (#5)**: V2 catches that refactoring-expert was assigned a runtime hypothesis (variant-2 lines 71-82). Static-read work product was structurally predictable from the agent's focus areas. V1 misses this assignment-layer failure mode entirely.
6. **Conservative likelihood capping**: V2 caps likelihood at [0.30, 0.85] per the brief — discipline V1 lacks (V1 reports 0.89 for M1).

**Weaknesses identified in V1**:
1. V1 assumes the calibrator ran, citing `tier2-RCA-calibration.md` etc. — but on the T4 substrate these files don't exist. V1's mechanism stack is substrate-specific.
2. V1's M4 prevention layer is valuable but is the #4 priority, not the #1 — V1's likelihood × blast-radius ranking is over-weighted on M1 (the math) and under-weighted on whether the math runs at all.
3. V1 does NOT name agent-domain mismatch — a structurally-distinct failure mode at the assignment layer.

**Concessions**:
- V2 is shallower on rubric internals. If the calibrator DID run on its substrate, V2 has no arithmetic to explain why 0.95 came out.
- V2 collapses M3b and M3c into shared assumptions or omits them — loses the two independently-deployable fixes V1 surfaces.
- V2 does not produce a multiplicative-compounding analysis. The fix-sequencing constraint is absent.
- V2 does not name M4 (eval-suite pin tests).

---

## Convergence Detection (Round 1 only)

Per-point agreement table:

| Diff Point | V1 Position | V2 Position | Converged? |
|------------|-------------|-------------|------------|
| S-001 (org) | Mechanism-tagged | Layer-tagged ranked list | NO (different lenses, both valid) |
| S-002 (length) | 269 lines deep | 139 lines terse | NO (cosmetic, doesn't matter) |
| S-003 (provenance) | Heavy HTML comments | Single header block | NO (cosmetic) |
| S-004 (taxonomy) | Mechanism-decomp + addendum | Causes/contradictions/excluded/stats/assumptions | NO (different value structures) |
| C-001 (arithmetic-mean dilution) | M1 primary cause @ 0.89 | A-δ shared assumption (assumed correct, not a cause) | NO (substrate-divergent) |
| C-002 (source-vs-runtime OR-clause) | M2 primary @ 0.85 | #2 generation-layer @ 0.80 | YES |
| C-003 (verdict-direction asymmetry) | M3a @ 0.78 | #3 @ 0.70 | YES |
| C-004 (calibrator non-execution) | NOT NAMED | #1 audit-layer @ 0.85 | NO (substrate-divergent) |
| C-005 (eval-suite pin tests / M4) | M4 @ 0.68 | NOT NAMED | NO (substrate-divergent) |
| X-001 (did the calibrator run?) | Implicit YES | Empirical NO | NO (the diagnostic finding) |
| U-001 (M4 + compounding analysis) | unique to V1 | absent | NO |
| U-002 (M3b + M3c sub-mechanisms) | unique to V1 | absent | NO |
| U-003 (calibrator-non-exec + layer taxonomy + agent-mismatch) | absent | unique to V2 | NO |
| A-001 (rubric/calibrator IS the right layer to fix) | UNSTATED | STATED (as A-α) | PARTIAL (both assume it; V2 names it) |

**Convergence score**: 2/14 ≈ **0.14** on diff points (very low) — BUT this is a structural feature of cross-environment comparison, not a debate failure. The two runs analyzed *different substrates with different failure modes*. The right interpretation is **substrate-bifurcated complementarity**, not convergence.

**Convergence on the underlying-mechanism-family** (re-clustering at the conceptual layer): M2 (rubric OR-clause / evidence-class disjunction) and M3a (verdict-direction asymmetry) appear in both runs with near-identical mechanism descriptions, fixes, and evidence citations. This is **STRONG convergence on the generation-layer rubric defects**.

---

## Per-Point Scoring Matrix

| Point | Winner | Confidence | Evidence Summary |
|-------|--------|------------|------------------|
| C-001 (M1 arithmetic-mean dilution) | V1 | 0.85 | V1 cites verbatim arithmetic from the actual calibration artefact. V2 demoted it to a "shared assumption" because its substrate had no artefact to ground the math on. **Substrate-specific**. |
| C-002 (M2 / source-vs-runtime) | TIE | 0.90 | Both variants converge on the OR-clause critique, both recommend a runtime-check dimension, both cite `escalation-rubric.md:11-17`. Mechanism description is near-identical. |
| C-003 (M3a / verdict-direction asymmetry) | TIE | 0.85 | Both name AFFIRM/REFUTE symmetry as a defect; both cite H3 as the canonical case; both recommend verdict-direction modifier. |
| C-004 (calibrator non-execution) | V2 | 0.90 | V2 ran the empirical-disk check; V1 implicitly assumed the calibrator ran. V2 wins this point unambiguously — *on its substrate*. |
| C-005 (M4 pin tests) | V1 | 0.80 | V1 uniquely surfaces the eval-suite silent-green pathology and prescribes 3 specific pin tests. V2 omits. Prevention-layer value is independent of substrate. |
| U-002 (M3b/M3c sub-mechanisms) | V1 | 0.70 | V1's decomposition surfaces two independently-deployable fixes (falsification-standard field; dual-instance minimum). V2 collapses or omits. |
| U-003 (agent-domain mismatch) | V2 | 0.75 | V2 catches the assignment-layer failure (refactoring-expert on runtime hypothesis). V1 misses this entire failure-mode class. |
| A-001 (right-layer assumption) | V2 | 0.65 | V2 explicitly names the shared assumption (A-α); V1 leaves it unstated. Naming-as-debate-target is a real epistemic value. |

**Base selection signal**: Both variants are partial. Neither is "winner take all" — V1 wins the depth/mechanism axis, V2 wins the empirical-verification axis. Per the next step, base selection should weigh V1 for structural depth (more material to merge from) but the merged output MUST incorporate V2's empirical-verification step and assignment-layer cause as additive.

---

## Round 2 / Round 2.5 / Round 3

**Skipped** per `--depth quick`. The skill protocol (SKILL.md lines 188-191) specifies Round 2 runs only on `--depth standard` or `--depth deep`; Round 2.5 invariant probe and Round 3 similarly require deeper depth.
