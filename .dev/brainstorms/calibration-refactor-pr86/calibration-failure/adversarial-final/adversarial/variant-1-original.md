# Calibration-Failure Root-Cause Merge (Agent-A merged)

**Substrate**: `pr86-integration-contracts-20260526100600` (structurally analogous to the H3 0.95-REFUTE miss)
**Canonical mechanism**: A confidence calibrator can score a hypothesis card at ≥0.85 calibrated confidence on source-only evidence against runtime-behavior claims.
**Provenance**: Base = Variant 1 (Agent A); integrations from Variant 2 (Agent B) and Variant 3 (Agent C).

---

## Methodology & Channel Disclosure
<!-- provenance: integrated from V2 §1 + §3; V3 pipeline-degradation cross-reference -->

This merge is produced from three independent theory-generation channels:

| Channel  | Variant | Intended pass                                       | Actual delivery                                                                                                |
|----------|---------|-----------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| A        | V1      | Unmediated first-principles direct-read             | Delivered as intended.                                                                                          |
| B        | V2      | sc:reflect-grounded analytical pass                 | **PARTIAL FAILURE**: sc:reflect protocol body loaded, but mandatory Serena `think_about_*` tools returned `Error: No such tool available` on every call. V2's theories are therefore a **second direct-read pass**, not a sc:reflect-augmented pass. Methodologically transparent in V2 §3. |
| C        | V3      | /sc:troubleshoot --depth deep pipeline grounding    | Delivered with degradation: `--no-mcp` and `--no-doc-discovery` set; Task subprocess unavailable for Tier 2 fan-out; calibration ran via Wave 1.7 / Wave 3.5 inline-fallback. The 3 hypothesis cards were isolated by role-prompt, not by fresh context window — anchoring-defense structurally weaker than spec-shape Tier 2. |

**Implication for confidence weighting**: The 3-channel design intended to triangulate across distinct epistemic methods, but environmental degradation collapsed Channels B and C toward Channel A's methodology. Convergence across the three variants is therefore *weaker evidence of correctness* than it would be under intended conditions — three direct-read passes can share blind spots that a true sc:reflect or full /sc:troubleshoot pass would surface. The merged thesis below remains defensible because each theory cites mechanism artefacts directly verified by Read, but the **substrate-vs-H3 fidelity caveat** in Cross-theory implications ¶5 should be read as a load-bearing limit on certainty.

---

## Theory 1 — Arithmetic-Mean Dilution of the Only Honest Dimension
<!-- provenance: base V1 §T1 retained; V2 fix-formula integrated -->

### Mechanism

The rubric collapses five very heterogeneous dimensions into an unweighted arithmetic mean (`escalation-rubric.md:19` — "**Confidence** = arithmetic mean of the five dimension scores"). Four of those dimensions (symptom coverage, reproducibility fit, fix directness, domain coherence) can be scored to 1.0 *purely from the card's prose* — they are essentially "is the card well-organized, internally consistent, and tightly scoped?" Only **evidence grounding** asks the question that matters for runtime-behavior claims: "does the cited line actually do what the card says it does at runtime?" When evidence-grounding is honestly scored 0.5 (because the calibrator can't run `git show` / can't execute / can't observe), it is averaged against four 1.0s and the composite still lands at **(0.5 + 1 + 1 + 1 + 1) / 5 = 0.90** — visible verbatim in `tier2-root-cause-analyst-calibration.md:9-19`. The dimension that should have *vetoed* the verdict instead contributes 20% weight.

In the H3 case the same arithmetic explains why a "I read main.rs and it falls through to start_client" verdict (evidence-grounding can only be partial because you didn't *run* it) survives as 0.95: the prose-readable dimensions all score 1.0 and dilute the one honest 0.5 (or the agent never even self-scores the source-vs-runtime gap, since the rubric doesn't *name* "did you actually execute this?" as a distinct check).

### Evidence

- `escalation-rubric.md:19` — `**Confidence** = arithmetic mean of the five dimension scores.` (unweighted, no veto rule).
- `escalation-rubric.md:11-17` (the dimension table) — four of five dimensions are scoreable from the card's prose alone; only "Evidence grounding" requires touching the cited substrate, and even *that* row defines 1.0 as "Cited `file:line` matches a real code path that exhibits the symptom" — "exhibits the symptom" is treated as inferable from reading code, not requiring execution.
- `tier2-root-cause-analyst-calibration.md:11-17` — explicit demonstration: evidence-grounding=0.5, other four=1.0, calibrated mean = **0.90**. The Note at `tier2-root-cause-analyst-calibration.md:33` admits "F5 test fixture citation is factually absent at current HEAD" — yet the dilution math still produced 0.90.
- `tier2-quality-engineer-calibration.md:13-17` — same shape: evidence-grounding=0.5, three 1.0s, fix-directness=0.5 → 0.60. When fix-directness *also* drops to 0.5 the score finally moves; when only evidence-grounding is honest, the math hides it. The 3-dimension delta pattern between RCA (0.90) and QE (0.60) is exactly what flat-mean predicts.
- `REPORT.md:114-116` — "Tier 1 confidence-calibrator scored evidence-grounding 0.5 because it lacked Bash to verify PR-sha citations via `git show`. The orchestrator (this skill) DID verify those citations directly in Wave 0" — confession that the calibrator's evidence-grounding score is structurally truncated, *and the rubric has no mechanism to translate that structural truncation into a confidence ceiling.*
- `audit.log:60-63` — "All 3 calibrators flagged evidence-grounding ≤ 0.5 due to lacking Bash to verify PR-sha citations." The signal was loud and the math swallowed it.

### Merged confidence

**0.90** — convergent across all three variants (V1=0.85, V2=0.92, V3=0.85). The math is directly observable on disk; the 3-dimension delta pattern (RCA 0.90 vs QE 0.60) is exactly what a flat-mean predicts.

### Systemic fix
<!-- provenance: V2's "gated minimum" preferred per debate; V1's veto-or-cap and V3's clamp listed as alternatives -->

**Primary**: Replace the unweighted arithmetic mean with a **gated minimum** — `calibrated = min(evidence_grounding + 0.3, mean(other_four))` so any 0.5 on evidence-grounding caps the ceiling regardless of how internally tight the card is.

**Alternative formulations considered**:
- V1's veto-or-cap: any dimension ≤ 0.5 caps composite at 0.75 (cleanly below 0.85 escalate gate).
- V3's runtime-aware clamp: cap calibrated ≤ 0.84 when `evidence_grounding < 1.0` AND `grounding_predicate_type=runtime_behavior` (requires new card field).

---

## Theory 2 — "Evidence Grounding" Conflates Source-Citation with Runtime-Verification
<!-- provenance: V1 §T2 base; V2's "6th rubric dimension" fix integrated -->

### Mechanism

The rubric's "Evidence grounding" row defines 1.0 as "**Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom**" (`escalation-rubric.md:13`). The OR is the trap. It permits the calibrator (and the upstream agent self-grading) to score 1.0 on **source citation alone** without ever requiring "diagnostic command output reproduces the symptom."

For a static defect (missing import, wrong regex literal) this is fine — the source IS the runtime behavior. For a **dynamic-control-flow defect** (does `Some(Command::Options(...))` fall through to `start_client`? Does an empty `contract_idents` *actually* bypass the guard at runtime?), source citation can be deeply misleading: control flow that *appears* to fall through in a static read can be diverted by a match arm, a `?` operator, a panic, a feature flag, or a side-effecting initializer that wasn't on the read path. The rubric never names this distinction.

So an agent that read 200 lines of Rust source and traced a control flow with their eyes can in good conscience claim "Evidence grounding = 1.0" — and the calibrator, also tooled only with `Read`, has no way to falsify that claim. The H3 0.95-REFUTE is exactly this pathology: a source-traceable "falls through" claim that the runtime contradicts. H3's CLI-dispatch-order claim ("`zellij --session NAME options ...` runs `options` standalone, requires active session, therefore session never created") is structurally a clap-dispatch claim that source-reading the Rust definitions can *suggest* but only the executed command can *prove*.

### Evidence

- `escalation-rubric.md:13` — the literal OR clause: `Cited file:line matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom`. There is no third clause requiring "AND runtime verification when the claim is about dynamic behavior."
- `escalation-rubric.md:15` (Reproducibility fit anchors) — "deterministic exception with a clear trigger" scores 1.0 without anyone pulling the trigger.
- `confidence-calibrator.md:5` (or `:6`) — `tools: Read`. The calibrator agent **cannot execute anything**; it physically cannot upgrade an evidence-grounding score by reproducing the symptom. It can only spot-check source-vs-citation, which is *exactly the half of the OR clause that is insufficient for runtime claims.*
- `confidence-calibrator.md:51` — "Spot-check the evidence: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches." The instruction is about **snippet match**, not about **runtime behavior of the cited code**. A snippet match → 1.0 is fully compatible with the runtime behavior being the opposite of what the card claims.
- `confidence-check/SKILL.md:53-110` — the upstream `Confidence Check` skill that feeds this culture has 5 weighted checks, none of which is "did you reproduce the symptom?" Check 3 is "Official Documentation Verified?" (`SKILL.md:80`) and Check 5 is "Root Cause Identified?" (`SKILL.md:102`) — both phrased so that *reading* is the verification act. The cultural prior, established at the pre-implementation gate, treats source-reading as the highest tier of evidence.
- `tier2-refactoring-expert-hypothesis.md:91-96` — even the refactoring-expert's *self*-stated confidence of 0.78 is sourced from "I am confident the helper exists and is small (0.95 on F1/F3 collapsing cleanly)" — confidence is calibrated against *structural* readability of the proposed change, not against any runtime probe.

### Merged confidence

**0.85** — convergent (V1=0.80, V2=0.88; V3 absorbed this into T1). The OR clause is directly cited; the `tools: Read` restriction is mechanically incontestable.

### Systemic fix
<!-- provenance: V2's "6th rubric dimension" preferred; V1's split-in-two listed as alternative -->

**Primary**: Add a sixth rubric dimension "**Runtime check**" with anchors `1.0 = hypothesis includes an executed reproducer with captured stdout/stderr / 0.5 = hypothesis includes a runnable command but no captured output / 0.0 = hypothesis is source-only`, and tier-gate it: REFUTE/REJECT verdicts on runtime-behavior claims require Runtime check ≥ 0.5.

**Alternative**: Split "Evidence grounding" into two dimensions: **Source-citation accuracy** (snippet matches) and **Runtime verification** (symptom reproduced or behavior asserted by test). For claims whose answer depends on dynamic control flow, runtime-verification ≥ 0.5 must be required before source-citation can score above 0.5.

---

## Theory 3 — Verdict-Direction Asymmetry (REFUTE Cost-of-Being-Wrong Ignored)
<!-- provenance: REPLACES V1's stripped-context theory per debate; V2 §T3 verbatim adapted. V1's stripped-context preserved in §Secondary mechanisms. -->

### Mechanism

The rubric and the calibrator agent treat all hypothesis verdicts as **symmetric assertions** about a cause. But "AFFIRM the cause" and "REFUTE the cause" have asymmetric cost-of-being-wrong: a wrong AFFIRM ships a fix that won't help and is rolled back when CI rejects; a wrong REFUTE *closes the investigation door* and lets the real bug ship. The H3 0.95 calibrated REFUTE is the canonical case: the agent said "H3 is not the cause" at 0.95, the troubleshoot pipeline accepted the REFUTE, the alternative cause was pursued, and CI then reproduced exactly H3's symptom.

Nowhere in the calibrator agent definition (`confidence-calibrator.md`) or the rubric (`escalation-rubric.md`) is the *verdict direction* an input. The rubric's only asymmetry is `--type security AND confidence < 0.95 → ESCALATE` (line 39) — recognizing security has asymmetric cost — but no analogue for REFUTE verdicts on testable runtime claims. The substrate run shows the same pathology in milder form: the RCA card REFUTED F2's independence (treating it as "latent rather than active"), self-confidence 0.75 on that sub-claim, but no separate calibration of that REFUTE — the calibrator only graded the *overall* card. In the H3 case, "REFUTE H3" is a single-sentence verdict that absorbed all five rubric dimensions' worth of credit.

### Evidence

- `escalation-rubric.md:39` — the *only* asymmetric-cost clause in the rubric — `--type security AND confidence < 0.95`. No verdict-direction clause.
- `confidence-calibrator.md` entire file: no mention of verdict direction (AFFIRM vs REFUTE vs REJECT) as an input, scoring axis, or threshold modifier. The agent's `Role` frames calibration as "did the upstream agent build a good case for the claim", not "what would it cost if this verdict is wrong".
- `tier2-root-cause-analyst-hypothesis.md:102-105` — the card's own self-confidence is internally bimodal — 0.95 on F1→F3→F5 chain, 0.75 on "F2 is independent" — but the calibrator returned a single 0.90 number, blending these. The H3 0.95 REFUTE is a degenerate case of the same: the single number absorbed both the "card is internally tight" credit and the asymmetric refutation cost.
- `REPORT.md:116` — "Tier 1 confidence-calibrator scored evidence-grounding 0.5 because it lacked Bash to verify PR-sha citations via `git show`. The orchestrator (this skill) DID verify those citations directly in Wave 0." — the orchestrator's workaround is itself evidence that the calibrator's structural blindness was known and routed around manually, not fixed.

### Merged confidence

**0.78** — V2's self-rating retained; V1 and V3 both explicitly steelmaned V2's T3 as "sharper than mine" / "better T3 than mine." Not 0.90 because the H3 substrate isn't on disk to confirm the REFUTE-specific dimension; the reasoning is from rubric symmetry.

### Systemic fix

Add a verdict-direction modifier to the rubric — `verdict=REFUTE AND claim_class=runtime-behavior AND runtime_check < 1.0 → cap calibrated at 0.70` — so source-only REFUTEs of runtime claims cannot clear the STOP gate. (Composes with Theory 2's "Runtime check" dimension.)

---

## Theory 4 — Eval-Suite Silent-Green Coverage of Structurally-Unverifiable Predicates
<!-- provenance: NEW section, integrated from V3 §C2 — meta-defect class no other variant surfaces -->

### Mechanism

`confidence-check/SKILL.md:14-18` advertises "Test Results (2025-10-21): Precision 1.000, Recall 1.000, 8/8 test cases passed." The eval corpus scores the calibrator on hypotheses it *can* ground — but never on hypotheses where grounding is structurally impossible (sha-pinned PR diff; runtime behavior predicted from source-only reads). The calibrator passes the test suite for the *wrong reason* — same anti-pattern V3 (quality-engineer) identified in pr86 itself (`adversarial/debate-transcript.md:69`: "test_t1/t6/t7 silently green-bar on substring containment of `FR-S10-02`"). The "1.000 precision/recall" claim is doing the work of a calibration-quality signal it cannot actually carry. Applied recursively: the calibrator failed the H3 case the same way pr86's test_t1 failed F1 — green-bar on irrelevant invariant.

### Evidence

- `/config/.claude/skills/confidence-check/SKILL.md:14-18` — blanket 1.000/1.000 claim, no per-failure-mode breakdown, no listed case for "structurally-unverifiable predicate."
- `/config/.claude/agents/confidence-calibrator.md:117-118` — Placebo Risk section: "if the calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead. The orchestrator should periodically run head-to-head meta-evals" — *should* and *periodically* are soft language, not enforced eval-suite contracts.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md:107-108` — Wave 4 in pr86 converged at 0.81 yet missed the helper-not-uppercasing runtime defect that rf-qa-qualitative caught only in A.10.5 cycle 1. Same "tests passed but ran wrong invariant" shape at adversarial-merge scope. `[uncited at file:line for A.10.5 details — referenced in the substrate REPORT narrative]`
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/debate-transcript.md:128-129` — U-001 silent-green winner = V3 (QE) at 95% confidence — unanimous concession that without pin tests, downstream cannot distinguish "fix worked" from "fix had no effect."

### Merged confidence

**0.68** — V3's self-rating retained. Recursion-of-the-same-anti-pattern is rhetorically strong and substrate-confirmed at multiple scopes, but the claim is *necessary-but-not-sufficient* — pin tests alone would just freeze the rubric's current behavior as the expected behavior. Theory 4 sits as a guardrail; it is not the load-bearing mechanism (Theory 1 is) but it is the load-bearing *prevention* mechanism.

### Systemic fix

Add 3 pin tests to calibrator eval suite — (a) sha-pinned citation → calibrated ≤ 0.84, (b) source-only runtime prediction → calibrated ≤ 0.84, (c) property: `evidence_grounding ≤ 0.5` → calibrated ≤ 0.85 for any input.

---

## Secondary mechanisms (defense-in-depth)
<!-- provenance: V1 §T3 stripped-context retained at reduced prominence; V3 §C3 anchoring-leak retained as additional secondary -->

### S1 — Stripped-context independence removes the doubt signal without removing the confidence signal (V1 §T3)

The calibrator is deliberately deprived of the hypothesis-formation context (`confidence-calibrator.md:21`). The stated goal is to reduce anchoring bias; the cost (loss of upstream hedges, doubts, near-misses that would signal "this is a source-only-insufficient question") is unnamed. A well-written REFUTE card without hedge-text passes the strip cleanly because the doubts that should have been there were never written down. **Per-theory confidence (V1): 0.65** — mechanism logically sound but partially uncited; hedge-text does survive in some pr86 cards which weakens the "doubts only live in stripped context" claim.

**Systemic fix**: Add a mandatory "Falsification standard" field to the hypothesis card template ("what evidence would prove me wrong") that survives the strip, and require the calibrator to score whether that standard was met by the card's actual evidence.

### S2 — Residual anchoring leak from card's self-report + narrative framing (V3 §C3)

`confidence-calibrator.md:25-27` instructs the calibrator to treat the card's self-reported confidence as "a signal, not a number." This is a *prompt-level norm*, not a structural constraint. The calibrator sees the self-report and confident prose; producing a divergent calibrated score imposes a small but real cognitive cost. Empirically: pr86's RCA calibration delta is +0.02 (self-reported 0.88 → calibrated 0.90); QE delta is -0.28 — but the -0.28 came from TWO dimensions dropping (mechanical signal was unambiguous), not from anti-anchoring discipline. **Per-theory confidence (V3): 0.45** — anchoring is mechanistically plausible but available evidence cannot distinguish it from Theory 1 (arithmetic propagation), since both predict "single-dimension drop yields small delta."

**Systemic fix**: Spawn 2 calibrator instances per card (different seeds), take the *minimum* score; alternatively, mask the card's self-reported confidence in the calibrator's input.

---

## Cross-theory implications
<!-- provenance: V1 base extended with V3's recursion observation -->

- **Theories 1 and 2 compound multiplicatively, not additively.** The arithmetic-mean structure (T1) only produces a 0.90 from a 0.5 evidence-grounding because the OR clause (T2) lets four other dimensions honestly score 1.0 on prose. Fix only T1 (cap on low evidence-grounding) and well-written cards still pass; fix only T2 (split or add runtime dimension) and the dilution math still hides the low new dimension. **Both fixes are required, and applying either alone underfits the failure mode.**

- **Theory 3 is upstream of Theories 1 and 2.** Even with veto rules (T1) and runtime-verification dimension (T2), if the rubric never weighs the cost-of-being-wrong asymmetry between AFFIRM and REFUTE, source-only REFUTEs of runtime claims will still clear the STOP gate. T3's fix (verdict-direction modifier) gates T1/T2's fixes specifically where the cost is highest.

- **Theory 4 is the meta-prevention layer.** Even with T1/T2/T3 fixed, without pin tests in the calibrator eval suite, regression is undetected. The calibration system fails the same way the code it was calibrating was failing — pin-test absence at production-code scope (pr86's helper-not-uppercasing) is isomorphic to eval-suite absence at calibrator scope. **The recursion is itself a verification**: the calibrator's anti-pattern matches the anti-pattern it was deployed to detect, and only the parallel-perspectives Tier 2 fan-out (in V3's channel) surfaced this isomorphism.

- **All four theories share a common root**: the entire calibration apparatus treats **source-reading as a complete epistemology for code claims**. This is true for static defects and structurally false for control-flow / runtime / environment-dependent claims. The H3 case (`zellij` subcommand dispatch behavior) and the pr86 case (PR-sha citations + Layer 3 emptiness bypass) both have a runtime dimension that source-only reading systematically under-detects. Theories 1, 2, 3 each name a specific way the apparatus encodes this prior; Theory 4 names the validation gap that lets it persist.

- **A potential conflict**: T3's fix (verdict-direction modifier) and T2's "Runtime check" dimension chain: the modifier presupposes a runtime-check axis that doesn't exist yet. **Apply T2 first**, then T3 atop it.

- **Substrate-vs-H3 fidelity caveat**: the pr86 substrate's calibrations are 0.90 and 0.60, not 0.95. The mechanism is structurally identical (`tier2-root-cause-analyst-calibration.md:11-19` shows evidence-grounding=0.5 + four 1.0s = 0.90) but the H3 0.95 would require either (a) the upstream agent self-scoring evidence-grounding at 1.0 (not 0.5) by claiming the source read *did* match runtime behavior — Theory 2 in its strongest form — or (b) all five dimensions self-scored at 1.0 with the calibrator unable to dispute. Either route is consistent with the theories above; without H3's calibration card on disk this cannot be distinguished.

---

## Top root causes (merged convergence)

1. **Theory 1 — Arithmetic-mean dilution** (confidence 0.90, convergent across all three channels): the unweighted mean lets a 0.5 evidence-grounding score average to 0.90 against four 1.0 prose-readable dimensions.

2. **Theory 2 — Source-vs-runtime evidence-grounding conflation** (confidence 0.85, convergent across A and B, absorbed by C): the OR-clause in the Evidence grounding rubric anchor lets source-citation alone earn 1.0 on runtime-behavior claims that source-reading cannot adjudicate.

3. **Theory 3 — Verdict-direction asymmetry** (confidence 0.78, novel in B, steelmaned by A and C): the rubric treats AFFIRM and REFUTE as symmetric, but REFUTE-wrong closes the investigation door while AFFIRM-wrong is caught by CI — a cost-of-being-wrong gradient the calibrator is blind to.

4. **Theory 4 — Eval-suite silent-green coverage** (confidence 0.68, novel in C): the calibrator's "1.000 precision/recall" eval corpus never tested it on structurally-unverifiable predicates, so the failure mode was undetected at validation.

**Required fixes are compositional, not exchangeable**: gated-minimum rubric formula (T1) + Runtime check 6th dimension (T2) + verdict-direction modifier (T3) + pin tests (T4). Applying any subset underfits the failure mode.
