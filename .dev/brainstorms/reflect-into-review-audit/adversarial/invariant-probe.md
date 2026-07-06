# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Target: the Round-1 emerging consensus (reject B both targets; add standalone `evidence-validator` at auggie-review Wave-3; raise `audit-validator` to 100% on DELETE/CONSOLIDATE for cleanup-audit).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | "human gates the recommendation" is the safety net for tolerating false-drops | UNADDRESSED | HIGH | `REVIEW.md` auto-feeds `/sc:design` (`SKILL.md:322`); audit-validator auto-re-audits on critical-fail (`context.md:80`). A-004 marked `Promoted: NO` (`diff-analysis.md`), never debated. Human can't gate what they never see. |
| INV-002 | state_variables | evidence-validator `partial` status composes with auggie-review Wave-3→4 status flow | UNADDRESSED | MEDIUM | `evidence-validator.md` returns `partial` on ≥1 drop; auggie-review posts comment-only (`SKILL.md:313`). Independent status vocabularies, reconciliation unspecified. |
| INV-003 | guard_conditions | "tuned to RE-GROUND via Grep rather than hard-drop" is an available evidence-validator behavior | UNADDRESSED | HIGH | **Contradicts the agent contract:** `evidence-validator.md:121` "match or drop"; `:33`/`:117–118` "do not propose new evidence / rewrite"; `:21` "when in doubt, drop it." Re-grounding requires forking the agent or new orchestrator code — not "zero new dependency." |
| INV-004 | guard_conditions | `snippet-mismatch` verdict gives correct-but-paraphrased findings a survival route | UNADDRESSED | HIGH | `evidence-validator.md:53` "do not tolerate semantic differences" → `:55` `snippet-mismatch` → dropped. Grep can't save it (no match on paraphrase; correct text unknown). Recall loss renamed, not eliminated. |
| INV-005 | guard_conditions | raising audit-validator to 100% on destructive findings adds no new failure mode | UNADDRESSED | MEDIUM | PASS/FAIL is discrepancy-ratio-based (<20% PASS, `context.md:80`). Changing the denominator from a 10% file-sample to 100%-of-destructive changes what 20% means; re-audit cascades could inflate cost. Threshold-recompute unaddressed. |
| INV-006 | count_divergence | "100% of DELETE/CONSOLIDATE findings" is a clean count | UNADDRESSED | MEDIUM | Existing rule is file-denominated ("5 findings per 50 files", `context.md:76`); proposal is finding-denominated. Counting-unit switch can *reduce* total validation volume on delete-sparse/file-dense repos while claiming more rigor. |
| INV-007 | count_divergence | "+2–8k tokens/run" holds at the auggie-review Wave-3 seam | UNADDRESSED | LOW | `diff-analysis.md` classifies A-001 UNSTATED (estimate, not measured); derived for troubleshoot Wave-5, carried over un-recomputed for a different/larger workload. |
| INV-008 | collection_boundaries | "DELETE/CONSOLIDATE" cleanly partitions the destructive-finding set | UNADDRESSED | HIGH | The worst destructive error — a dynamically-loaded file genuinely dead but marked KEEP, or a dynamic-loading false-negative — lives in the KEEP/REVIEW bucket (`context.md:80,84`), *outside* the elevated set. The 100% boundary excludes the highest-severity case. |
| INV-009 | collection_boundaries | the Wave-3 seam (after step 6 cross-check, before step 7 compose) is the right insertion point | ADDRESSED | LOW | Verified: inserting after persona cross-check and before `REVIEW.md` compose validates the final deduped+remapped set. Placement is sound (behavior is not). |
| INV-010 | interaction_effects | new Wave-3 evidence-validator doesn't interact with downstream remediation reflect (Phases C/E) | UNADDRESSED | HIGH | Triple reflect-family surface per remediated run: Wave-3 evidence-validator + Phase-C reflect-analyze + Phase-E reflect-validate. A Wave-3 false-drop is irreversible — dropped findings never enter the remediation spec (`SKILL.md:322`), so no downstream pass recovers them. |
| INV-011 | interaction_effects | evidence-validator doesn't interact with the `auggie-reviewer` blind cross-source signal | UNADDRESSED | MEDIUM | Deep-mode cross-source agreement bonus (`severity-rubric.md:97–99`). A citation-drop on a `both`-source finding silently destroys the blind-agreement signal. Precedence between the two anti-anchoring mechanisms unspecified. |
| INV-012 | sufficiency_challenge | standalone Wave-3 evidence-validator ALONE closes the same-context citation-drift gap | UNADDRESSED | HIGH | **Sharpest finding.** evidence-validator is a **precision** gate (drops false citations); R0/PR#112 (the cited motivation) is a **recall** miss (a *missing* finding). The mechanism structurally cannot reproduce the catch it is motivated by. The recall property that caught R0/PR#112 is the heterogeneous-reviewer pass the consensus rejects. |
| INV-013 | sufficiency_challenge | raising audit-validator to 100% on DELETE/CONSOLIDATE ALONE suffices for destructive integrity | UNADDRESSED | HIGH | Two non-citation defect classes escape a citation/grep re-check: (1) CONSOLIDATE overlap-% errors (valid citations, wrong quantity — `context.md:83`); (2) dynamic-loading false-negatives (a *missing* dynamic-use check, not a false citation — `context.md:84`). Insufficient by construction. |
| INV-014 | sufficiency_challenge | rejecting Proposal B is sufficiently justified by the semantic-fit defect | ADDRESSED | LOW | Holds: UC-2 deviation taxonomy has no referent for recommendations (`context.md:144`); circular reuse confirmed (`SKILL.md:561`). The REJECT-B half is sound. |

## Summary
- **Total findings:** 14
- **ADDRESSED:** 2 (INV-009, INV-014)
- **UNADDRESSED:** 12
- **By severity:** HIGH 7 · MEDIUM 4 · LOW 3

### HIGH + UNADDRESSED (block convergence on the positive recommendations)
INV-001, INV-003, INV-004, INV-008, INV-010, INV-012, INV-013.

### Disposition
The **REJECT-B** half survives the probe (INV-014). The **positive adds** (evidence-validator for auggie-review; 100% audit-validator for cleanup-audit) carry 7 HIGH defects, two decisive: INV-012 (wrong mechanism class — precision gate for a recall-motivated gap) and INV-003 (headline mitigation contradicts the agent contract). The merged verdict resolves these by **rejecting the blocked adds** and redirecting auggie-review's real (narrow) gap to a dependency-free strengthening of its *native* Wave-3 pass + existing `needs-grounding` bucket (`SKILL.md:203,207`), which already re-grounds-then-drops — the behavior evidence-validator forbids.
