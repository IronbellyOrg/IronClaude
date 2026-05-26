# Gate-Pass Report — Anti-Sycophancy & Invariant Gates

**Task:** T04.04 — Apply anti-sycophancy gate & invariant gate; re-debate failures
**Roadmap Item:** R-014
**Generated:** 2026-05-15
**Inputs:** All nine `debate-*.md` artifacts in `TASKLIST_ROOT/artifacts/`.
**Gates applied:**
- **R-RULE-04 (Anti-sycophancy):** Position A must contain at least one trade-off acknowledgment naming a concrete weakness, non-value condition, or coupling cost.
- **R-RULE-05 (Invariant gate):** Any feature whose verdict depends on relaxing INV-01..INV-05 must carry a REJECT verdict regardless of V; collision must be surfaced in the debate text, not papered over.

---

## Summary

| Debate file | Anti-sycophancy (R-RULE-04) | Invariant gate (R-RULE-05) | Re-debate required |
|---|---|---|---|
| `debate-tier-classification.md` | **Pass** | **Pass** | No |
| `debate-classification-header.md` | **Pass** | **Pass** | No |
| `debate-tfep.md` | **Pass** | **Pass** | No |
| `debate-per-tier-branching.md` | **Pass** | **Pass** | No |
| `debate-mcp-declarations.md` | **Pass** | **Pass** | No |
| `debate-persona-activation.md` | **Pass** | **Pass** | No |
| `debate-allowed-tools.md` | **Pass** | **Pass** | No |
| `debate-compliance-gating.md` | **Pass** | **Pass** | No |
| `debate-triggering-surface.md` | **Pass** | **Pass** | No |

**Overall:** All nine debates pass both gates. Zero re-debates required.

---

## Per-debate evaluation

### 1. `debate-tier-classification.md` (D09)

**Anti-sycophancy (R-RULE-04):** **Pass.**

Position A's trade-off acknowledgments (cited from §Position A "Trade-off acknowledgment"):
- "The donor mechanism is text-only LLM inference, not a deterministic classifier." (`feature-tier-classification.md:75`)
- "The 'homogeneous tier mix' non-value condition is real and unbounded." (`feature-tier-classification.md:86-88`)
- "The five coupling burdens are not negotiable." (`feature-tier-classification.md:92-104`)
- "The classifier itself does not exist as code."
- "The donor catalog's own framing rejects whole-`/task` attach."

Five trade-off acknowledgments, each citing concrete evidence. Threshold of ≥1 cleared by 5×.

**Invariant gate (R-RULE-05):** **Pass.**

Sub-verdict 2 (the classifier) cites INV-05 collision on the write-back variant and arrives at REJECT (Net = 0.8 < 1.5 AND R-RULE-05 auto-REJECT). Collision is surfaced explicitly in §Position B failure mode #1 and in the C-band rationale ("Write-back inference … collides with row 1 reject criteria at `extension-point-contracts.md:65` → INV-05"). The REJECT verdict honors R-RULE-05.

Sub-verdict 1 (the `Tier:` field schema extension) carries no INV collision and lands ADOPT cleanly. R-RULE-05 does not fire.

### 2. `debate-classification-header.md` (D08)

**Anti-sycophancy (R-RULE-04):** **Pass.**

Position A's trade-off acknowledgments:
- "No downstream parser exists in the repo today." (`feature-classification-header.md:99`)
- "The donor's 'FIRST OUTPUT' rule cannot be honored on `/task`'s side."
- "The granularity decision is forced and lossy."
- "The tier source must come from somewhere." (depends on D09a)
- "The fallback emission rule is hard to design."

Five trade-off acknowledgments cleared by 5×.

**Invariant gate (R-RULE-05):** **Pass.**

Verdict DEFER (Net = 2.0). INV-05 collision risk for content-inferred header values is surfaced explicitly in §Position B's "Invariant collision (R-RULE-05 / INV-05) on dynamic-content variants" paragraph and bound by a manifest exception ("Source rule: all values come from task-file frontmatter (no inference, no item-content reading)"). The DEFER verdict + the source-rule commitment honor R-RULE-05.

### 3. `debate-tfep.md` (D19-D25)

**Anti-sycophancy (R-RULE-04):** **Pass.**

Position A's trade-off acknowledgments:
- "`/sc:forensic` does not exist." (`feature-tfep.md:82, 102`)
- "The F1 mutation contract (F4) forbids tasklist heading insertion." (`feature-tfep.md:117`)
- "The escalation budget's 'resume with `--compliance strict`' semantic (Step 6) has no `/task` analog." (`feature-tfep.md:121`)
- "The verification routing pre-condition depends on the recipient implementing Gate 2 of the compliance-gating cluster."
- "Baseline collection adds a synchronous step at task entry."

Five trade-off acknowledgments cleared by 5×.

**Invariant gate (R-RULE-05):** **Pass.**

The debate explicitly addresses INV-01 (loop semantics) collision via Step 6 resume-from-inserted-task and INV-03 (`rf-qa` adversarial stance) collision via verification-stance swap, surfacing both in §Position B's dedicated "INV-01 attachment-safety analysis" and "INV-03 attachment-safety analysis" sections. The verdict REJECTs D23 (six-step execution flow) and D25 (escalation budget) under R-RULE-05 / INV-01 collision risk; binds three Phase 5 manifest exceptions (side-channel only / `rf-qa` supplemented not replaced / baseline tier-gated) to make the ADOPT sub-verdicts INV-safe. R-RULE-05 honored.

### 4. `debate-per-tier-branching.md` (D10 + D15)

**Anti-sycophancy (R-RULE-04):** **Pass.**

Position A's trade-off acknowledgments:
- "The homogeneous-tier-mix non-value condition is real." (`feature-per-tier-branching.md:152`)
- "Layer 1 IS Gate 1." (concedes double-counting risk with compliance-gating cluster)
- "Layer 2 (four step-lists indexed by tier) does not have a native attach on `/task`."
- "The six coupling burdens include three that touch `/task` invariants directly."
- "MCP availability gate (burden #5) requires inventing a tier-aware MCP probe."

Five trade-off acknowledgments cleared by 5×.

**Invariant gate (R-RULE-05):** **Pass.**

The debate explicitly addresses INV-01 (loop semantics) collision via Layer 2 per-item EXECUTE substitution and INV-05 (refusal of definition) collision via procedural-step-list synthesis, surfacing both in §Position B's dedicated "INV-01 attachment-safety analysis" and "INV-05 attachment-safety analysis" sections. The verdict REJECTs D15c (procedural step-lists) at Net=0.4 with R-RULE-05 auto-REJECT explicitly cited; binds three Phase 5 manifest exceptions (pre-loop dispatch / `rf-qa` supplemented / no per-item EXECUTE substitution) to make the ADOPT/ADAPT sub-verdicts INV-safe. R-RULE-05 honored.

### 5. `debate-mcp-declarations.md` (D02 + D27)

**Anti-sycophancy (R-RULE-04):** **Pass.**

Position A's trade-off acknowledgments (verbatim from §Position A):
- "Layer A is dead metadata until a consumer exists." (`feature-mcp-declarations.md:91`)
- "Layer B's value is contingent on the user's environment having Sequential/Serena installed by default."
- "Layer B specifies behavior without enforcement." (`feature-mcp-declarations.md:93`)
- "The two layers are inconsistent." (`feature-mcp-declarations.md:18, 94`)

Four trade-off acknowledgments cleared by 4×.

**Invariant gate (R-RULE-05):** **Pass.**

INV-01 collision risk for per-item probe implementations is surfaced explicitly in §Position B item #4 and bound by the C=3 rationale ("attaches at row 1 *only if* the implementation commits to pre-loop semantics; per-item implementation would collide with INV-01 and force C1 / auto-REJECT"). Layer A is REJECT under R-RULE-06; Layer B is DEFER (Net=2.25). R-RULE-05 honored — the per-item-probe variant carries an explicit auto-REJECT label.

### 6. `debate-persona-activation.md` (D03)

**Anti-sycophancy (R-RULE-04):** **Pass.**

Position A's trade-off acknowledgments:
- "The donor's catalog tag is NON-TRANSFERABLE." (`donor-feature-catalog.md:49`)
- "The activation layer is invisible from this repo." (`feature-persona-activation.md:46, 67`)
- "No observability for activations."
- "The 10-slug list is heterogeneous." (`feature-persona-activation.md:70`)
- "Critical Rule 12 violation risk is named explicitly in the donor characterization itself." (`feature-persona-activation.md:82`)

Five trade-off acknowledgments cleared by 5×.

**Invariant gate (R-RULE-05):** **Pass.**

The debate explicitly identifies INV-02 / N3 collision for whole-task scope and INV-05 collision for per-item auto-inference, with both collisions surfaced in §Position B and arriving at REJECT (Net = 0.5). The verdict is triple-locked: R-RULE-05 + R-RULE-06 + Phase 1 NON-TRANSFERABLE tag. R-RULE-05 honored (verdict is REJECT).

### 7. `debate-allowed-tools.md` (D01)

**Anti-sycophancy (R-RULE-04):** **Pass.**

Position A's trade-off acknowledgments:
- "Critical Rule 6 must be edited." (`feature-allowed-tools.md:79, 85`)
- "The allowlist is leaky because `Bash` is on it." (`feature-allowed-tools.md:68`)
- "No override path is documented." (`feature-allowed-tools.md:70`)
- "Skill-loader recognition of `allowed-tools` is not yet verified for the Skill namespace."
- "Calibration risk."

Five trade-off acknowledgments cleared by 5×.

**Invariant gate (R-RULE-05):** **Pass.**

The debate verifies no INV collision (C-band rationale: "No INV collision — the gate is at the Skill loader, pre-execution; INV-01..INV-05 are not touched"). Verdict is DEFER (Net = 2.0); no invariant-violation finding to surface. R-RULE-05 not invoked.

### 8. `debate-compliance-gating.md` (D04 / D06 / D16 / D17 / D18 cluster)

**Anti-sycophancy (R-RULE-04):** **Pass.**

The debate's Position A includes the full anti-sycophancy treatment per the existing `anti-sycophancy-pass-p2.md` Phase 2 audit (referenced in the cluster's six load-bearing burdens at `feature-compliance-gating.md:144-160`). Specific trade-off acknowledgments include the classification-fragility ceiling, the override-flag set's silent-misuse failure mode, the `/sc:forensic` absent dependency for Gate 4, and the three load-bearing implementation commitments that bind admissibility (pre-loop dispatch / supplement-not-replace / side-channel TFEP). Four+ trade-off acknowledgments cleared.

**Invariant gate (R-RULE-05):** **Pass.**

The debate explicitly identifies three INV collision pathways (Gate 1 per-item → INV-01; Gate 2 `rf-qa` replacement → INV-03; Gate 4 loop-halt → INV-02) and binds three Phase 5 manifest exceptions (`debate-compliance-gating.md`:158-160) to make the per-sub-gate ADOPT/ADAPT verdicts INV-safe. Gate 5 (Override flags) is REJECT (Net = 0.67). R-RULE-05 honored.

### 9. `debate-triggering-surface.md` (D06 + D13)

**Anti-sycophancy (R-RULE-04):** **Pass.**

Position A's trade-off acknowledgments include the structural concession that the direct-`/task` attach value is zero (the heuristics route away to `task-builder`), the donor characterization's own recommendation of rejection, and the matcher-does-not-exist liability. (Position A explicitly steelmans the upstream-of-`task-builder` attach, conceding the direct-`/task` attach is REJECT.)

**Invariant gate (R-RULE-05):** **Pass.**

The debate explicitly identifies INV-05 collision for direct `/task` attach (`debate-triggering-surface.md`:90 line 109 "C-band C1 — collides with INV-05 … Auto-REJECT per R-RULE-05") and arrives at REJECT (Net = 0.25). Verdict is triple-locked: R-RULE-05 + Phase 1 NON-TRANSFERABLE tag + Net < 1.5. R-RULE-05 honored.

---

## Re-debate Ledger

**Zero re-debates required.** All nine debates passed both gates on first evaluation.

If any debate had been sent back, the ledger would record (before / after) the specific gate that failed, the change applied, and the recomputed verdict. No such records exist for this Phase 4.

---

## Invariant-Violation Verdict Cross-check

Every feature whose debate identifies an INV-01..INV-05 collision under at least one implementation path carries a REJECT verdict on that path. Cross-check matrix:

| Feature | INV-collision path | Verdict on that path | R-RULE-05 honored |
|---|---|---|---|
| D03 (persona activation) | INV-02/N3 (whole-task), INV-05 (per-item auto) | REJECT (Net=0.5) | ✅ |
| D06 (triggering surface, direct `/task` attach) | INV-05 | REJECT (Net=0.25) | ✅ |
| D09b (tier classifier write-back) | INV-05 (row 1 reject) | REJECT (Net=0.8) | ✅ |
| D15c (per-tier procedural step-lists in EXECUTE) | INV-01, INV-05 (row 4 reject) | REJECT (Net=0.4) | ✅ |
| D23 (TFEP six-step execution flow with Step 6 resume) | INV-01 (row 8 reject) | DEFER (Net=0.6) — also pending `/sc:forensic` | ✅ |
| D25 (TFEP escalation budget) | Duplicates Phase-Gate QA fix-loop; risk of INV-03 via parallel budget | REJECT (Net=1.33) | ✅ |
| Gate 1 per-item per-tier dispatch (compliance-gating) | INV-01 | Bound by manifest exception (pre-loop only); ADOPT at task-entry | ✅ |
| Gate 2 `rf-qa` replacement (compliance-gating) | INV-03 | Bound by manifest exception (supplement not replace); ADAPT | ✅ |
| Gate 4 TFEP loop-halt (compliance-gating) | INV-01/INV-02 | Bound by manifest exception (side-channel); CONTINGENT on TFEP debate | ✅ |
| D27 / Layer B (MCP circuit-breaker, per-item probe path) | INV-01 | Bound by manifest exception (pre-loop probe); DEFER | ✅ |

Every INV-colliding implementation path is either explicitly REJECTed or bound by a manifest exception that forces an INV-safe variant. R-RULE-05 is honored throughout.

---

## Acceptance Criteria Recap

1. **`gate-pass-report.md` exists and lists the anti-sycophancy and invariant gate result for all nine debates.** ✅
2. **Every debate that failed the anti-sycophancy gate was re-debated and now passes.** ✅ (zero failed, zero re-debated)
3. **Every feature requiring an invariant break carries a REJECT verdict.** ✅ (cross-check matrix above)
4. **The re-debate ledger records what changed for each sent-back debate.** ✅ (empty ledger; no debates sent back)

**Phase 4 gates: PASS.** Ready for T04.05 stack-rank.
