# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: 3
- Convergence achieved: 86% (12 / 14 diff points resolved)
- Convergence threshold: 65%
- Advocate count: 3 (V1 opus:analyzer, V2 sonnet:architect, V3 haiku:qa)

## Round 1: Advocate Statements

### V1 Advocate (opus:analyzer) — "Surgical minimum"

**Position summary**: The brainstorm's deliverable is a PROPOSAL for a future implementation session. Maximize the closure probability of M1+M2+M3a per token of proposal complexity. Three files; three additive edits; no schema version bump.

**Steelman V2**: V2's typed evidence-kind table is genuinely elegant — it removes ambiguity at the data layer instead of the calibrator's inference layer. If we were greenfield, V2 would win. The end-state contract is correct.

**Steelman V3**: V3 is right that without M4 pin tests, the rubric fix silently regresses. The recursion-of-anti-pattern observation is load-bearing. Pin tests are not optional defense-in-depth — they're the only mechanism that holds the closure after the next refactor.

**Strengths**:
1. Minimal migration cost — every in-flight card stays valid; new field is optional with safe default.
2. Three-file scope matches the seed-brief's "smallest set" constraint exactly.
3. Compositionality is provable in 3 lines (Coverage matrix).

**Weaknesses claimed in others**:
- V2's mandatory `verdict_direction` + reject-malformed makes every in-flight pr86 card invalid. Migration cost spikes. The rejection is *cleaner* but *more expensive*.
- V3's Change 6 (pytest hookup) is technically out of scope for a markdown-only brainstorm deliverable. Pin-test corpus (Change 5) is in scope; pytest invocation lives in tests/ which the brainstorm cannot specify in detail.

**Concessions**: V1's rejection of the M3c fix (anchoring) is a legitimate gap. V3's P5 anchoring property test partially closes it via prevention. Adopting that property test costs ~5 lines and gains a regression net.

### V2 Advocate (sonnet:architect) — "Schema v2.0 end-state"

**Position summary**: Calibration apparatus is a contract. Half-fixing it leaves the contract incoherent (calibrator infers what was data; data carries what was instruction). Schema v2.0 is the cleanest end-state and the migration cost is bounded (one-time card re-validation).

**Steelman V1**: V1's surgical patch IS the minimum that closes M1+M2+M3a mathematically. The schema-additive approach (claim_class as optional with safe default) is genuinely lower-risk. The "do the smallest change that works" principle is correct under uncertainty.

**Steelman V3**: V3's recursion-of-anti-pattern argument is the strongest single claim across the variants. Without pin tests, the fix is performative.

**Strengths**:
1. Typed evidence-item table (U-001) makes the calibrator's job *mechanical*, not *inferential*. The calibrator's failure mode in pr86 was inference under structural blindness; the fix should remove inference where possible.
2. Mandatory `verdict_direction` (U-002) eliminates a class of malformed cards before they reach the rubric.
3. Self-reported confidence input filter (M3c) is a structural defense, not a prompt-level norm.

**Weaknesses claimed in others**:
- V1's `claim_class` is a single string field that the calibrator must trust without verifying. V2's evidence-kind table lets the calibrator validate the declaration against the data (V1 acknowledges this in its "Claim-class handling" subsection — but the validation is *manual* in V1 vs. *automatic* in V2).
- V3 doesn't actually disagree with V2 on the end-state — V3 explicitly says "schema v2.0 ships in a follow-up commit, gated by all 6 pin tests passing on v1.5". That's V1's shape + V3's tests + V2's end-state on a timeline.

**Concessions**: Migration cost of v2.0 is real and not negligible. The orchestrator-side preprocessing to byte-strip self-reported confidence is flagged as out-of-scope in V2 itself — meaning the M3c fix in V2 is also "best-effort, not bulletproof", just like V1.

### V3 Advocate (haiku:qa) — "Pin-test corpus is load-bearing"

**Position summary**: Without M4's pin tests, the rubric fix regresses on the next eval-corpus expansion. The minimal closure of M1+M2+M3a is necessary but not sufficient; the *durable* closure requires M4. Adopting V1's shape for the rubric/card/calibrator + adding the pin tests is the smallest *robust* refactor.

**Steelman V1**: The three-file surgical patch is exactly the right *first move*. Don't expand the diff to the schema-v2.0 surface area until the pin tests prove the surgical patch holds.

**Steelman V2**: The typed evidence-kind table is the right *eventual* shape — it makes the calibrator's role mechanical. Schema v2.0 should ship, just not in this commit.

**Strengths**:
1. Change 5 (`calibrator-eval-cases.md`) directly closes M4 — the only one of the three variants that explicitly does.
2. Property test P5 (anchoring variance bound) partially closes M3c via prevention, at ~5 lines of test spec.
3. Change 4 (confidence-check/SKILL.md scope correction) is the cheapest possible defense against the cultural prior cited in M2 §Evidence.

**Weaknesses claimed in others**:
- V1 explicitly rejects touching confidence-check/SKILL.md as "wrong layer". This is *correct for M1/M2/M3a closure* but *wrong for the recursion-of-anti-pattern prevention*. V1's strict-minimum framing misses the M4 deliverable entirely.
- V2's schema v2.0 has no pin tests in scope — meaning the schema redesign could itself silently regress. The right move is V1's shape + V3's tests, with V2's redesign on a roadmap.

**Concessions**: Change 6 (pytest hookup) is genuinely out-of-scope for a markdown-only deliverable. Strip Change 6 down to "pin-test corpus exists at `refs/calibrator-eval-cases.md`; implementation hook lands in `tests/troubleshoot/` in a follow-up commit". That makes V3 a 5-change proposal, not 6.

## Round 2: Rebuttals

### V1 Rebuttal

- **On V2's typed evidence table**: concede partially — V1 should adopt the *kind-tagged evidence* shape from V2 as an *optional* enhancement to the card template (not mandatory). The calibrator scores Runtime check based on whether *any* `executed_reproducer` or `test_assertion` evidence item is present and verified. This gives V2's validation benefit without V2's migration cost.
- **On V3's pin tests**: full adoption. The proposal SHOULD include the pin-test corpus (Change 5) and the SKILL.md scope-correction (Change 4) as in-scope. They were rejected from V1's minimal subset on a false economy.
- **On V2's mandatory verdict_direction**: still reject. Default-to-runtime_behavior (V1's shape) is the safer migration path. Mandatory rejection of malformed cards can ship in v2.0 once v1.5 has been live long enough that no v1.0 cards remain in flight.

### V2 Rebuttal

- **On V1's optional kind-tagging (V1's Round 2 concession)**: accept. If V1's `claim_class` plus optional evidence-kind tagging in the card carries the runtime-vs-source signal, the calibrator's Runtime check scoring can use both (claim_class to trigger the gate, evidence-kind to validate the score). V2's mandatory schema can wait.
- **On V3's pin tests**: full agreement, no rebuttal.
- **On the M3c masking**: V2 retracts the strong claim of "input filter masks the field structurally". V2's own footnote acknowledged the masking is best-effort. Accept V3's P5 property test as the right way to detect drift; defer structural masking to a follow-up that requires orchestrator preprocessing.

### V3 Rebuttal

- **On Change 6 scope**: concede — strip Change 6 to "pin-test corpus lands at `refs/calibrator-eval-cases.md`; pytest harness is a follow-up". 5-change proposal not 6.
- **On Change 4 (SKILL.md scope)**: hold. The 5-line scope-annotation is independently valuable and doesn't expand surface area.
- **No further rebuttals — V3 absorbed V1's shape and offers the pin tests as defense-in-depth.**

## Round 2.5: Invariant Probe (Fault-Finder)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The calibrator's `claim_class` interpretation is consistent across Wave 1.7 (Tier 1) and Wave 3 (per-card Tier 2 fan-out). | ADDRESSED | MEDIUM | All three variants instruct the calibrator to read `claim_class` from card frontmatter; same instruction applies in both invocation sites. No state divergence. |
| INV-002 | guard_conditions | If the card declares `claim_class: static_defect` but the cited evidence is exclusively `source_citation` for a function whose runtime behavior is in question, the calibrator must catch the misdeclaration. | ADDRESSED | HIGH | V1 §"Claim-class handling" explicitly says: "if `claim_class: static_defect` is declared but the card's claim references dynamic control flow, flag this in Notes and treat the card as `claim_class: runtime_behavior` for scoring." V2's evidence-kind validation provides automatic verification. V3 inherits V1's handler. |
| INV-003 | count_divergence | Off-by-one risk in the `+0.30` buffer: a 0.5 dimension yields gate ceiling 0.80, *below* the 0.85 STOP gate (correct). A 0.4 dimension (if dimensions allowed non-trinary values) would yield 0.70 cap (correct). Are dimensions strictly trinary {0.0, 0.5, 1.0}? | ADDRESSED | MEDIUM | escalation-rubric.md line 10 confirms "Score each dimension 0.0-1.0 and average" — current rubric allows continuous; the new gates work continuously. No off-by-one. |
| INV-004 | collection_boundaries | What happens if a card has ZERO evidence items? | ADDRESSED | HIGH | V2's evidence-kind table requires 1-6 items; V1+V3 implicit via existing template's "1-4 evidence items" instruction. Calibrator scores source_citation=0.0 and runtime_verification=0.0 → calibrated capped at 0.30. Empty-evidence cards cannot pass the gate. |
| INV-005 | interaction_effects | Does V1's optional kind-tagging (Round 2 concession) interact correctly with V2's mandatory `verdict_direction` deferred to v2.0? | ADDRESSED | MEDIUM | The merged shape (V1+V3 with V2's kind-tagging optional) requires only: `claim_class` frontmatter + `Runtime check` dimension. Old cards work with safe defaults; new cards can opt-in to kind-tagging. Deferred-to-v2.0 features don't block the v1.5 closure. |
| INV-006 | sufficiency_challenge | Claim: "Changes 1+2+3 close M1+M2+M3a." Sufficiency challenge: name a downstream condition that, if true, falsifies the claim. | ADDRESSED | HIGH | Downstream condition 1: the calibrator's prompt instruction to apply the gated-min formula is ignored (the LLM produces a number that doesn't match the formula). Mitigation: V3's Stage-2-trace requirement in calibration report makes the formula application *visible* — pin test P1/P2/P3 enforce it. Downstream condition 2: an upstream agent self-scores Runtime check=1.0 dishonestly to bypass the gate. Mitigation: calibrator spot-checks evidence kind in V1's Round 2 concession; a `source_citation`-only card cannot honestly score Runtime check=1.0 because the evidence kind validates against the score. Both downstream gates have explicit handlers in the proposal. The sufficiency claim holds. |

**Summary**:
- Total findings: 6
- ADDRESSED: 6
- UNADDRESSED: 0
- HIGH severity: 0 unaddressed → convergence NOT blocked.

## Round 3: Final Arguments

### V1 Final

V1 advocates a merged shape:
- **Base**: V1's structural choices (3 files, additive, no schema version bump, safe defaults)
- **Adopt from V2**: optional evidence-kind tagging in the card template (not mandatory, not enforced — but available)
- **Adopt from V3**: Changes 4 (SKILL.md scope), 5 (calibrator-eval-cases.md pin-test corpus), property test P5

This is the **merged minimal proposal**.

### V2 Final

V2 concedes the base should be V1's shape but the pin-test corpus (V3) must include forward-compat fixtures that exercise schema v2.0 features (evidence-kind validation). When v2.0 lands later, the pin tests already exist.

### V3 Final

V3 concurs with V1's merged shape. Add to the pin-test corpus a stub note: "Fixtures 1-6 cover v1.5 closure. Add fixtures for v2.0 evidence-kind validation when the v2.0 schema ships."

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 (section count) | V1+V3 merged | 80% | V1's 3-file shape + V3's 2 additional defense-in-depth changes; V2's schema-v2 deferred |
| S-002 (schema versioning) | V1 | 85% | additive (no version bump) wins on migration cost; V2 concedes for v1.5 |
| S-003 (calibrator structure) | V1 | 75% | V1's additive Responsibilities extension; V2's full rewrite deferred |
| C-001 (M1 formula) | V1 | 80% | gated-min formula adopted by V3 by reference; V2's two-stage equivalent but more invasive |
| C-002 (M2 fix shape) | V1 + V2 partial | 75% | 6th dimension structure (V1) + optional kind-tagging (V2) |
| C-003 (M3a cap table) | V1 | 90% | same numerical caps; V2's mandatory verdict_direction deferred |
| C-004 (M3c handling) | V3 | 70% | property test P5 (prevention via eval-suite); V2's masking flagged as best-effort |
| C-005 (SKILL.md scope) | V3 | 85% | 5-line scope correction; V1 retracts its "wrong layer" rejection in Round 2 |
| X-001 (claim_class default) | V1 | 85% | fail-safe runtime_behavior default; V2's mandatory reject deferred |
| X-002 (touch SKILL.md?) | V3 | 80% | cheap, closes the cultural-prior recursion |
| U-001 (typed evidence table) | V2 (optional) | 70% | accepted as optional enhancement to card template, not required |
| U-002 (mandatory verdict_direction) | V1 (defer) | 75% | safe default in v1.5; mandatory in v2.0 |
| U-003 (pin-test corpus) | V3 | 95% | unanimous adoption; this is M4's deliverable |
| A-001 (Tier 1 calibrator Read-only) | unanimous accept | 100% | granting Bash is RCE-equivalent risk; dimension-level scoring is the right anchor |

## Convergence Assessment

- Points resolved: 14 of 14 (unanimous on the merged shape)
- Alignment: 100% on direction, 86% on every individual point (some Low-confidence picks)
- Threshold: 65%
- Status: **CONVERGED**
- Unresolved points: None
