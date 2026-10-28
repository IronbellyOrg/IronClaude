# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis
| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
|INV-001|state_variables|unchanged delivery or a PASS establishes unchanged acceptance conditions.|ADDRESSED|HIGH|Evidence: all five R2 C-002 nominations distinguish original requirements, applied rules, artifact, checks, proof, capability and correction authority; C-005 separates endpoint types. Result: delivery digests cannot stand in for proof/policy state; the synthesis expressly preserves that distinction.|
|INV-002|guard_conditions|a nominally available command, permitted partial repair or scoped acceptance clears the original blocker.|ADDRESSED|HIGH|Evidence: V5 distinguishes notice-only execution from rendering, frozen correction authority from capability, and useful partial review from closure; all R2 C-005 nominations retain accepted-but-unverified outcomes. Result: neither return-code success nor acceptance is promoted to demonstrated compliance.|
|INV-003|count_divergence|ten unanimous writing choices establish unanimous causal rank, or repeated incidents supply independent votes.|ADDRESSED|HIGH|Evidence: R2 contains all ten specified nominations across all five advocates; D defines ten points, excludes five unique-contribution rows, and assigns L1=1/L2=3/L3=6. Result: writing agreement is 10/10 points, each supported by five advocates—not fifty independent observations. Causal pairs remain contested: V3>V2 has 3/5 support; V4>V5 has 3/5. Neither reaches two-thirds, which requires four of five. V1 is first in every R2 order; that narrower agreement does not establish a complete shared ordering.|
|INV-004|collection_boundaries|package/context breadth measures independent causal prevalence, or missing live logs erase historical evidence.|ADDRESSED|HIGH|Evidence: R2 A-001/C-004 limit comparison to the selected clustered sample; C-007 distinguishes captured historical contents from current availability. D preserves both restrictions. Result: “reach first” remains a qualitative comparison rule, not a measured population ranking; differing breadth judgments remain disclosed.|
|INV-005|interaction_effects|classifying one transition selects a sole cause for the whole sequence.|ADDRESSED|HIGH|Evidence: R2 C-001 permits separately supported linked stages; V2 separates introduced faults from retained siblings; V3/V4 retain credential policy/proof confounding. Result: weak checks can permit escape, repair can introduce an interaction, policy can reopen review, and authority can block closure without contradiction.|
|INV-006|sufficiency_challenge|the proposed safeguards are demonstrated sufficient to stop another failed review.|ADDRESSED|HIGH|Required path examined: original criterion → actual check → allowed repair → neighboring invariants → durable proof → fixed rubric → verified endpoint. Actual-check stage: V1 identifies checks weaker than behavior; V5 identifies static/nominal-success checks that do not establish rendering. Repair/invariant stage: V2 requires permitted successful changes, immediate pre/post comparison and producer/consumer/sibling constraints; V5 requires correction authority or an explicitly scoped decision. Proof/rubric/endpoint stage: R2 C-007 requires meaningful historical proof; C-006 fixes original criteria and separates policy variation; C-005 refuses to equate acceptance with repair. Downstream counterexample: stronger fixture assertions can expose the fourth defect while frozen authority still prevents correction; static evidence can improve while rendering remains unverified. These counterexamples are already accommodated. All proposed replays remain unexecuted; the monitor trap was accepted with known defects, not shown repaired. No end-to-end branch trace establishes universal sufficiency, and none is claimed.|

## Complete Independent Return
| DONE | NEXT |
|---|---|
| Independently examined exact Round 1/2, five cards and comparison; no writes, delegation or publication. | Preserve scoped agreement and both contested ranking pairs. |

**Round 2.5 consensus gate: PASS — for the ten-point writing synthesis, not a shared causal ordering.**
No verified unaddressed issue survives these six probes; no HIGH unaddressed blocker.
Ten-point convergence is genuine semantic agreement about classification, evidence and reporting—not merely identical nominee tokens. It would mask scope if reported as causal-ranking convergence.

**Evidence key**
R1 = `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/tool-results/bibiommdw.txt`
R2 = `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/tool-results/bsxx38kuv.txt`
B = `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/`
Vn = B + `variant-n-original.md`; D = B + `diff-analysis.md`.
Historical mechanisms remain card-reported evidence; this review did not independently replay primary events.

**INV-001 / state_variables / ADDRESSED / HIGH**
Assumption challenged: unchanged delivery or a PASS establishes unchanged acceptance conditions.
Evidence: all five R2 C-002 nominations distinguish original requirements, applied rules, artifact, checks, proof, capability and correction authority; C-005 separates endpoint types.
Result: delivery digests cannot stand in for proof/policy state; the synthesis expressly preserves that distinction.

**INV-002 / guard_conditions / ADDRESSED / HIGH**
Assumption challenged: a nominally available command, permitted partial repair or scoped acceptance clears the original blocker.
Evidence: V5 distinguishes notice-only execution from rendering, frozen correction authority from capability, and useful partial review from closure; all R2 C-005 nominations retain accepted-but-unverified outcomes.
Result: neither return-code success nor acceptance is promoted to demonstrated compliance.

**INV-003 / count_divergence / ADDRESSED / HIGH**
Assumption challenged: ten unanimous writing choices establish unanimous causal rank, or repeated incidents supply independent votes.
Evidence: R2 contains all ten specified nominations across all five advocates; D defines ten points, excludes five unique-contribution rows, and assigns L1=1/L2=3/L3=6.
Result: writing agreement is 10/10 points, each supported by five advocates—not fifty independent observations.
Causal pairs remain contested: V3>V2 has 3/5 support; V4>V5 has 3/5. Neither reaches two-thirds, which requires four of five.
V1 is first in every R2 order; that narrower agreement does not establish a complete shared ordering.

**INV-004 / collection_boundaries / ADDRESSED / HIGH**
Assumption challenged: package/context breadth measures independent causal prevalence, or missing live logs erase historical evidence.
Evidence: R2 A-001/C-004 limit comparison to the selected clustered sample; C-007 distinguishes captured historical contents from current availability. D preserves both restrictions.
Result: “reach first” remains a qualitative comparison rule, not a measured population ranking; differing breadth judgments remain disclosed.

**INV-005 / interaction_effects / ADDRESSED / HIGH**
Assumption challenged: classifying one transition selects a sole cause for the whole sequence.
Evidence: R2 C-001 permits separately supported linked stages; V2 separates introduced faults from retained siblings; V3/V4 retain credential policy/proof confounding.
Result: weak checks can permit escape, repair can introduce an interaction, policy can reopen review, and authority can block closure without contradiction.

**INV-006 / sufficiency_challenge / ADDRESSED / HIGH**
Assumption challenged: the proposed safeguards are demonstrated sufficient to stop another failed review.
Required path examined: original criterion → actual check → allowed repair → neighboring invariants → durable proof → fixed rubric → verified endpoint.
Actual-check stage: V1 identifies checks weaker than behavior; V5 identifies static/nominal-success checks that do not establish rendering.
Repair/invariant stage: V2 requires permitted successful changes, immediate pre/post comparison and producer/consumer/sibling constraints; V5 requires correction authority or an explicitly scoped decision.
Proof/rubric/endpoint stage: R2 C-007 requires meaningful historical proof; C-006 fixes original criteria and separates policy variation; C-005 refuses to equate acceptance with repair.
Downstream counterexample: stronger fixture assertions can expose the fourth defect while frozen authority still prevents correction; static evidence can improve while rendering remains unverified.
These counterexamples are already accommodated. All proposed replays remain unexecuted; the monitor trap was accepted with known defects, not shown repaired. No end-to-end branch trace establishes universal sufficiency, and none is claimed.

**Self-audit:** Zero new surviving gate defects. Historical reviewer misses, rubric-change authorship and isolated policy-versus-proof effects remain genuine unknowns—not facts recoverable merely by stronger wording or presumed live-file availability.
**Recommended action:** Carry the ten-point synthesis forward with both ranking pairs explicitly contested; do not label it causal-order consensus. No mandatory Round 3 is triggered by this review.

## Summary
- Assumptions probed:6, covering six required categories.
- ADDRESSED6; UNADDRESSED0 (HIGH0,MEDIUM0,LOW0 unaddressed).
- HIGH-addressed assumptions are not newly discovered product bugs.
- Probe PASS applies to ten-point semantic synthesis, not complete causal-order consensus or newly replayed historical events.

## Source Provenance
Complete actual independent return: `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-aa04d567a636336d9.jsonl:47`, timestamp 2026-10-23T05:12:42.167Z, UUID fda33241-35db-463f-a7d2-ad6a298ee6e7. Exact collected source also at `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/tool-results/bybsrxops.txt:2-55`.
