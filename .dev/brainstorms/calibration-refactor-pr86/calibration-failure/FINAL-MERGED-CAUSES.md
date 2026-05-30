<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (A-merged, opus advocate) -->
<!-- Merge date: 2026-05-26T19:35Z -->
<!-- Convergence: 0.92 — CONVERGED (above 0.80 threshold) -->

# Calibration-Failure Root-Cause Merge — FINAL (Step 3 of 4)

**Substrate**: `pr86-integration-contracts-20260526100600` (structurally analogous to the H3 0.95-REFUTE miss)
**Canonical mechanism**: A confidence calibrator can score a hypothesis card at ≥0.85 calibrated confidence on source-only evidence against runtime-behavior claims.
**Provenance**: Base = Variant 1 (Agent-A merged); restructured per X-001 MERGE outcome to incorporate Variant 3 (Agent-C merged) M3 composite; opening synthesis added from Variant 2 (Agent-B merged) §1.

---

## Top-line synthesis
<!-- Source: Variant 2 (B), §1 — merged per Change #1 -->

The H3 0.95-REFUTE / pr86-0.90-calibrated pathology is the **multiplicative compounding** of two structural design choices in the rubric (M1, M2), modulated by a decision-theoretic blind spot with three orthogonal sub-mechanisms (M3a/M3b/M3c), and propagated by a **silent-green test suite** that institutionalizes the blindness (M4).

**Convergent across all three channels**: M1 (arithmetic-mean dilution) and M2 (source-vs-runtime evidence conflation) are the load-bearing primary mechanisms — three independent investigative channels (unmediated direct-read, /sc:reflect-degraded, /sc:troubleshoot --depth deep) all surfaced them with overlapping evidence citations.

---

## Methodology & Channel Disclosure
<!-- Source: Base (original) — load-bearing limit on convergence claim -->

This merge is produced from three independent theory-generation channels:

| Channel | Variant | Intended pass | Actual delivery |
|---------|---------|---------------|-----------------|
| A | V1 | Unmediated first-principles direct-read | Delivered as intended. |
| B | V2 | sc:reflect-grounded analytical pass | **PARTIAL FAILURE**: sc:reflect protocol body loaded, but mandatory Serena `think_about_*` tools returned `Error: No such tool available` on every call. V2's theories are therefore a **second direct-read pass**, not a sc:reflect-augmented pass. Methodologically transparent in V2 §3. |
| C | V3 | /sc:troubleshoot --depth deep pipeline grounding | Delivered with degradation: `--no-mcp` and `--no-doc-discovery` set; Task subprocess unavailable for Tier 2 fan-out; calibration ran via Wave 1.7 / Wave 3.5 inline-fallback. The 3 hypothesis cards were isolated by role-prompt, not by fresh context window — anchoring-defense structurally weaker than spec-shape Tier 2. |

**Implication for confidence weighting**: The 3-channel design intended to triangulate across distinct epistemic methods, but environmental degradation collapsed Channels B and C toward Channel A's methodology. Convergence across the three variants is therefore *weaker evidence of correctness* than it would be under intended conditions — three direct-read passes can share blind spots that a true sc:reflect or full /sc:troubleshoot pass would surface. The merged thesis below remains defensible because each theory cites mechanism artefacts directly verified by Read, but the **substrate-vs-H3 fidelity caveat** in Cross-mechanism implications ¶5 should be read as a load-bearing limit on certainty.

---

## M1 — Arithmetic-Mean Dilution of the Only Honest Dimension
<!-- Source: Base (original) — M1 retained verbatim from A; fix-formula primary from B integrated -->

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

**0.89** — convergent across all three variants (A=0.90, B=0.90, C=0.88; numerical compromise per C-001).

### Systemic fix

**Primary**: Replace the unweighted arithmetic mean with a **gated minimum** — `calibrated = min(evidence_grounding + 0.3, mean(other_four))` so any 0.5 on evidence-grounding caps the ceiling regardless of how internally tight the card is.

**Alternative formulations considered**:
- A's veto-or-cap: any dimension ≤ 0.5 caps composite at 0.75 (cleanly below 0.85 escalate gate).
- C's runtime-aware clamp: cap calibrated ≤ 0.84 when `evidence_grounding < 1.0` AND `grounding_predicate_type=runtime_behavior` (requires new card field).

---

## M2 — "Evidence Grounding" Conflates Source-Citation with Runtime-Verification
<!-- Source: Base (original) — M2 retained verbatim from A; 6th rubric dimension fix from B integrated -->

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

**0.85** — convergent (A=0.80, B=0.88; C absorbed this into C1). The OR clause is directly cited; the `tools: Read` restriction is mechanically incontestable.

### Systemic fix

**Primary**: Add a sixth rubric dimension "**Runtime check**" with anchors `1.0 = hypothesis includes an executed reproducer with captured stdout/stderr / 0.5 = hypothesis includes a runnable command but no captured output / 0.0 = hypothesis is source-only`, and tier-gate it: REFUTE/REJECT verdicts on runtime-behavior claims require Runtime check ≥ 0.5.

**Alternative**: Split "Evidence grounding" into two dimensions: **Source-citation accuracy** (snippet matches) and **Runtime verification** (symptom reproduced or behavior asserted by test). For claims whose answer depends on dynamic control flow, runtime-verification ≥ 0.5 must be required before source-citation can score above 0.5.

---

## M3 — Verdict-Direction Asymmetry and Anchoring-Channel Loss (composite)
<!-- Source: Variant 3 (C), lines 64-103 — merged per Change #2 (X-001 MERGE outcome). Replaces A's Theory 3 + Secondary §S1/§S2 with three sub-mechanisms preserving distinct fixes. -->

The third mechanism does not converge on a single cause — it has three orthogonal sub-mechanisms with independent fixes. The debate (X-001) explicitly resolved this as MERGE outcome (90% confidence): collapsing M3 to a single mechanism loses two structurally valuable fixes.

### M3a — Verdict-direction asymmetry (debate-favored primary)

**Mechanism**: The rubric treats AFFIRM and REFUTE as **symmetric assertions** about a cause. But "AFFIRM the cause" and "REFUTE the cause" have asymmetric cost-of-being-wrong: a wrong AFFIRM ships a fix that won't help and is rolled back when CI rejects; a wrong REFUTE *closes the investigation door* and lets the real bug ship. The H3 0.95 calibrated REFUTE is the canonical case: the agent said "H3 is not the cause" at 0.95, the troubleshoot pipeline accepted the REFUTE, the alternative cause was pursued, and CI then reproduced exactly H3's symptom. Nowhere in `confidence-calibrator.md` or `escalation-rubric.md` is the *verdict direction* an input. The rubric's only asymmetry is `--type security AND confidence < 0.95 → ESCALATE` (line 39) — recognizing security has asymmetric cost — but no analogue for REFUTE verdicts on testable runtime claims.

**Evidence**:
- `escalation-rubric.md:39` — sole asymmetric-cost clause is type=security, not verdict direction.
- `confidence-calibrator.md` entire file — no mention of verdict direction (AFFIRM vs REFUTE vs REJECT) as an input, scoring axis, or threshold modifier.
- `tier2-root-cause-analyst-hypothesis.md:102-105` — the card's own self-confidence is internally bimodal (0.95 on F1→F3→F5 chain, 0.75 on "F2 is independent") but the calibrator returned a single 0.90 number, blending these.
- `REPORT.md:116` — the orchestrator's workaround (verifying citations directly in Wave 0) is itself evidence that the calibrator's structural blindness was known and routed around manually, not fixed.

**Merged confidence**: **0.78**.

**Systemic fix**: Add a verdict-direction modifier — `verdict=REFUTE AND claim_class=runtime-behavior AND runtime_check < 1.0 → cap calibrated at 0.70` — so source-only REFUTEs of runtime claims cannot clear the STOP gate. Composes with M2's "Runtime check" dimension.

### M3b — Stripped-context removes the doubt signal (information-channel adjunct)

**Mechanism**: The calibrator is deliberately deprived of the hypothesis-formation context (`confidence-calibrator.md:21`). The stated goal is to reduce anchoring bias; the cost (loss of upstream hedges, doubts, near-misses that would signal "this is a source-only-insufficient question") is unnamed. A well-written REFUTE card without hedge-text passes the strip cleanly because the doubts that should have been there were never written down. Clean finished cards optimize for the rubric's prose-readable dimensions; the calibrator by design has no upstream signal to flag the missing-doubt.

**Evidence**:
- `confidence-calibrator.md:21` — explicit trail-strip; the cost (loss of doubt-signal) is unnamed.
- `hypothesis-card-template.md:104-108` — "If I'm wrong, it's probably because…" is a one-sentence alternative, NOT a "what evidence would falsify me." The card template does not require a falsification standard.

**Merged confidence**: **0.65**.

**Systemic fix**: Add a mandatory **Falsification standard** field to the hypothesis card template ("what evidence would prove me wrong") that survives the strip, AND require the calibrator to score whether that standard was met by the card's actual evidence. **Risk per A**: this field could amplify well-written but wrong cards unless paired with M2's runtime-verification dimension demanding the standard *be applied*.

### M3c — Residual anchoring leak from card's self-report (secondary)

**Mechanism**: `confidence-calibrator.md:25-27` instructs the calibrator to treat the card's self-reported confidence as "a signal, not a number." This is a *prompt-level norm*, not a structural constraint. The calibrator sees the self-report and confident prose; producing a divergent calibrated score imposes a small but real cognitive cost. Empirically: pr86's RCA calibration delta is +0.02 (self-reported 0.88 → calibrated 0.90); QE delta is -0.28 — but the -0.28 came from TWO dimensions dropping (mechanical signal was unambiguous), not from anti-anchoring discipline.

**Evidence**:
- `confidence-calibrator.md:25-27, 36-38` — prompt-norm phrasing only, no structural counter-pressure.
- `confidence-calibrator.md:117-118` — Placebo Risk acknowledgment.
- `tier2-root-cause-analyst-calibration.md:21-23` — calibrator's narrative *reasons about* the self-report number, the precise behavior the spec said not to do.

**Merged confidence**: **0.45** — anchoring is mechanistically plausible but available evidence cannot distinguish it from M1 (arithmetic propagation), since both predict "single-dimension drop yields small delta."

**Systemic fix**: Spawn 2 calibrator instances per card (different seeds), take the *minimum* score; alternatively, mask the card's self-reported confidence in the calibrator's input.

---

## M4 — Eval-Suite Silent-Green Coverage of Structurally-Unverifiable Predicates
<!-- Source: Base (original) — retained from A T4; integrated from V3 §C2 originally -->

### Mechanism

`confidence-check/SKILL.md:14-18` advertises "Test Results (2025-10-21): Precision 1.000, Recall 1.000, 8/8 test cases passed." The eval corpus scores the calibrator on hypotheses it *can* ground — but never on hypotheses where grounding is structurally impossible (sha-pinned PR diff; runtime behavior predicted from source-only reads). The calibrator passes the test suite for the *wrong reason* — same anti-pattern V3 (quality-engineer) identified in pr86 itself (`adversarial/debate-transcript.md:69`: "test_t1/t6/t7 silently green-bar on substring containment of `FR-S10-02`"). The "1.000 precision/recall" claim is doing the work of a calibration-quality signal it cannot actually carry. Applied recursively: the calibrator failed the H3 case the same way pr86's test_t1 failed F1 — green-bar on irrelevant invariant.

### Evidence

- `/config/.claude/skills/confidence-check/SKILL.md:14-18` — blanket 1.000/1.000 claim, no per-failure-mode breakdown, no listed case for "structurally-unverifiable predicate."
- `/config/.claude/agents/confidence-calibrator.md:117-118` — Placebo Risk section: "if the calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead. The orchestrator should periodically run head-to-head meta-evals" — *should* and *periodically* are soft language, not enforced eval-suite contracts.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md:107-108` — Wave 4 in pr86 converged at 0.81 yet missed the helper-not-uppercasing runtime defect that rf-qa-qualitative caught only in A.10.5 cycle 1. Same "tests passed but ran wrong invariant" shape at adversarial-merge scope.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/debate-transcript.md:128-129` — U-001 silent-green winner = V3 (QE) at 95% confidence — unanimous concession that without pin tests, downstream cannot distinguish "fix worked" from "fix had no effect."

### Merged confidence

**0.68** — convergent across A=0.68, C=0.68 (B did not separately score; framing identical). Recursion-of-the-same-anti-pattern is rhetorically strong and substrate-confirmed at multiple scopes, but the claim is *necessary-but-not-sufficient* — pin tests alone would just freeze the rubric's current behavior as the expected behavior. M4 sits as a guardrail; it is not the load-bearing mechanism (M1 is) but it is the load-bearing *prevention* mechanism.

### Systemic fix

Add 3 pin tests to calibrator eval suite — (a) sha-pinned citation → calibrated ≤ 0.84, (b) source-only runtime prediction → calibrated ≤ 0.84, (c) property: `evidence_grounding ≤ 0.5` → calibrated ≤ 0.85 for any input.

---

## Cross-mechanism implications
<!-- Source: Base (original) — A's cross-theory framing retained with C's prevention/recursion bullets appended -->

- **M1 and M2 compound multiplicatively, not additively.** The arithmetic-mean structure (M1) only produces a 0.90 from a 0.5 evidence-grounding because the OR clause (M2) lets four other dimensions honestly score 1.0 on prose. Fix only M1 (cap on low evidence-grounding) and well-written cards still pass; fix only M2 (split or add runtime dimension) and the dilution math still hides the low new dimension. **Both fixes are required, and applying either alone underfits the failure mode.**

- **M3 is upstream of M1 and M2.** Even with veto rules (M1) and runtime-verification dimension (M2), if the rubric never weighs the cost-of-being-wrong asymmetry between AFFIRM and REFUTE (M3a), and never sees the trail of doubts (M3b), and never accounts for anchoring residual (M3c), source-only REFUTEs of runtime claims will still clear the STOP gate. M3's three fixes gate M1/M2's fixes specifically where the cost is highest.

- **M4 is the meta-prevention layer.** Even with M1/M2/M3 fixed, without pin tests in the calibrator eval suite, regression is undetected.

- **M4 is the prevention mechanism for all three diagnostic mechanisms** (provenance: Variant C line 134). Without pin tests, any fix to M1/M2/M3 will be silently regressed. M4 is the *only* prescription that does not require changes to the rubric or the calibrator agent itself — it changes the test suite.

- **Recursion-of-anti-pattern** (provenance: Variant C line 135): the calibration apparatus is failing the same way pr86's code was failing — silent-green coverage of structurally-unverifiable predicates. This isomorphism is itself a verification that the chosen root causes are real, not procedural artifacts. The calibrator's anti-pattern matches the anti-pattern it was deployed to detect.

- **All four mechanisms share a common root**: the entire calibration apparatus treats **source-reading as a complete epistemology for code claims**. This is true for static defects and structurally false for control-flow / runtime / environment-dependent claims. The H3 case (`zellij` subcommand dispatch behavior) and the pr86 case (PR-sha citations + Layer 3 emptiness bypass) both have a runtime dimension that source-only reading systematically under-detects. M1, M2, M3 each name a specific way the apparatus encodes this prior; M4 names the validation gap that lets it persist.

- **Fix-sequencing constraint**: M3a's fix (verdict-direction modifier) and M2's "Runtime check" dimension chain: the modifier presupposes a runtime-check axis that doesn't exist yet. **Apply M2 first, then M3a atop it.**

- **Substrate-vs-H3 fidelity caveat**: the pr86 substrate's calibrations are 0.90 and 0.60, not 0.95. The mechanism is structurally identical (`tier2-root-cause-analyst-calibration.md:11-19` shows evidence-grounding=0.5 + four 1.0s = 0.90) but the H3 0.95 would require either (a) the upstream agent self-scoring evidence-grounding at 1.0 (not 0.5) by claiming the source read *did* match runtime behavior — M2 in its strongest form — or (b) all five dimensions self-scored at 1.0 with the calibrator unable to dispute. Either route is consistent with the mechanisms above; without H3's calibration card on disk this cannot be distinguished.

---

## Top root causes (merged convergence) — ranked by likelihood × blast radius

1. **M1 — Arithmetic-mean dilution** (confidence 0.89, unanimous across all 3 channels): the unweighted mean lets a 0.5 evidence-grounding score average to 0.90 against four 1.0 prose-readable dimensions. **Highest blast radius**: affects every hypothesis card the calibrator scores. Likelihood ≈ 1.0 because the math is directly observable on disk.

2. **M2 — Source-vs-runtime evidence-grounding conflation** (confidence 0.85, unanimous across A and B, absorbed by C into M1): the OR-clause in the Evidence grounding rubric anchor lets source-citation alone earn 1.0 on runtime-behavior claims that source-reading cannot adjudicate. **High blast radius**: affects every runtime-behavior hypothesis card. Compounds multiplicatively with M1.

3. **M3a — Verdict-direction asymmetry** (confidence 0.78, novel-in-B, steelmaned by A and C; primary sub-mechanism of M3): the rubric treats AFFIRM and REFUTE as symmetric, but REFUTE-wrong closes the investigation door while AFFIRM-wrong is caught by CI — a cost-of-being-wrong gradient the calibrator is blind to. **Targeted blast radius**: affects REFUTE verdicts on runtime claims specifically (the H3 0.95-REFUTE case is exactly this).

4. **M4 — Eval-suite silent-green coverage** (confidence 0.68, unique-to-C, ranked #4 not #3 because M3a is more diagnostically specific to the H3 failure shape, while M4 is preventive): the calibrator's "1.000 precision/recall" eval corpus never tested it on structurally-unverifiable predicates, so the failure mode was undetected at validation. **Largest *regression* blast radius**: without M4, any fix to M1/M2/M3 will be silently regressed.

5. **M3b + M3c — Stripped-context doubt-signal loss + residual anchoring** (combined confidence ≈ 0.55, secondary sub-mechanisms of M3): two structurally orthogonal information-channel weaknesses with independent fixes (Falsification-standard card field + dual-instance-minimum). Lower individual likelihood than M3a but additive value because their fixes are independently deployable.

**Required fixes are compositional, not exchangeable**: gated-minimum rubric formula (M1) + Runtime check 6th dimension (M2) + verdict-direction modifier (M3a) + Falsification standard field (M3b) + dual-instance-minimum (M3c) + pin tests (M4). Applying any subset underfits the failure mode.

---

## Synthesis addendum (Step 3 post-process — required structural pieces)
<!-- Source: Step 3 orchestrator — annotates the merge per task requirements 1-5; does not rewrite skill output -->

### 1. Top 3-5 root causes ranked by likelihood × blast radius

See §"Top root causes (merged convergence)" above. Ranking justification:
- **M1 #1**: highest because likelihood ≈ 1.0 (math observable on disk) × blast radius = every card scored.
- **M2 #2**: high likelihood (rubric OR-clause directly cited) × blast radius = every runtime-behavior card. Compounds multiplicatively with M1.
- **M3a #3**: moderate likelihood (rubric audited for verdict-direction inputs — none found) × targeted blast radius (REFUTE on runtime claims) but the H3 failure mode is exactly this shape.
- **M4 #4**: moderate likelihood (pin-test absence directly observable) × the largest *regression* blast radius (without it, all other fixes silently regress).
- **M3b + M3c #5 (tied/combined)**: lower individual likelihood but two structurally independent fixes that add compositional value.

### 2. Convergence evidence — unanimous vs partial/single-source

**Unanimous across A/B/C-merged**:
- M1 mechanism + evidence + fix-family — all three cite the same file:line citations (escalation-rubric.md:19, tier2-RCA-calibration.md:11-17, tier2-QE-calibration.md, audit.log:60-63, REPORT.md:114-116).
- M2 mechanism + evidence — all three cite escalation-rubric.md:13 OR clause, confidence-calibrator.md tools:Read, :51 snippet-match instruction. C subsumed M2 under M1 but with identical evidence.
- M4 mechanism + evidence + fix — all three cite confidence-check/SKILL.md:14-18, confidence-calibrator.md:117-118, pr86's own silent-green debate-transcript.md:128-129.
- Cross-mechanism compounding (M1 × M2 multiplicative) — all three explicitly state this.

**Partial/single-source**:
- M3 composite structure (M3a/M3b/M3c): **unique to Variant C** (Agent C-merged) at full fidelity. A demoted M3b and M3c to "Secondary mechanisms"; B dropped them entirely. Adopted in the final merge per X-001 MERGE outcome.
- Cross-theory ordering "M2 first then M3a atop it": **unique to Variant A** (Agent A-merged). Adopted as Fix-sequencing constraint bullet in Cross-mechanism implications.
- Channel-B-degradation top-of-document disclosure: **unique to Variant A** at load-bearing prominence. Adopted verbatim.
- Top-line synthesis paragraph: **unique to Variant B** (Agent B-merged). Adopted as new opening §.
- M4 "prevention mechanism for all three diagnostic mechanisms" + "recursion-of-anti-pattern" framings: **unique to Variant C**. Adopted as appended bullets in Cross-mechanism implications.

### 3. Compositional vs exchangeable analysis

**Compositional (must combine — applying any subset underfits)**:
- M1 fix (gated-minimum formula) + M2 fix (Runtime check 6th dimension): **multiplicative**. Each alone is bypassable; the failure mode requires both. (Cross-mechanism implications ¶1.)
- M3a (verdict-direction modifier) presupposes M2 (Runtime check dimension): **sequential**. Apply M2 first, then M3a atop it. (Cross-mechanism implications "Fix-sequencing constraint" bullet.)
- M4 (pin tests) compounds with M1/M2/M3: without M4, the other three fixes silently regress on the next eval-corpus expansion. (Cross-mechanism implications ¶4.)

**Exchangeable (each can ship independently)**:
- M3a (verdict-direction modifier) and M3b (Falsification standard card field) and M3c (dual-instance-minimum) are **independent of each other**. Each addresses a different leak. Shipping M3a alone is a valid partial fix; the other two are additive improvements. (Composite M3 structure.)
- M4's three pin tests (sha-pinned, source-only runtime, evidence_grounding≤0.5 property) are **independent** — each catches a distinct regression. (M4 §Systemic fix.)
- Choice of M1 fix formula variant (gated-minimum vs veto-or-cap vs runtime-aware-clamp) is **exchangeable** — each is sufficient on its own. (M1 §Systemic fix.)
- Choice of M2 fix shape (sixth dimension vs split-into-two) is **exchangeable** — equivalent in effect. (M2 §Systemic fix.)

### 4. Open conflicts where the 3 merged files disagreed substantively

**Only one substantive conflict surfaced** (X-001 / C-002):
- **Conflict**: Is M3 one mechanism (B's view: verdict-direction-only) or three orthogonal sub-mechanisms (C's view: M3a/M3b/M3c)? A's view (one primary + two demoted secondaries) is the middle position.
- **Resolution**: C's composite structure adopted (X-001 MERGE outcome at 90% confidence, unanimous Round 2 concession). The three sub-mechanisms have structurally independent fixes; collapsing them loses two fixes (M3b's Falsification-standard field; M3c's dual-instance-minimum).
- **Rationale for resolution**: the three sub-mechanisms are not competing explanations of the same data — they each address a different leak in the calibrator's information channel. Adopting all three is additive, not contradictory.

**No other substantive conflicts**. The remaining differences are stylistic (provenance annotation style: HTML comment vs italic vs map) or numerical (M1 confidence: 0.90 vs 0.90 vs 0.88, resolved via 0.89 compromise) or structural placement (Channel-B disclosure top vs footer — resolved by adopting A's top-of-document position).

### 5. Process degradation note — Channel B degradation weakens convergence-as-evidence

**Flag**: Agent B's Step 1 /sc:reflect channel was degraded — the mandatory Serena `think_about_*` tools returned `Error: No such tool available` on every call. **Agent B's contribution effectively became a second direct-read pass**, not a sc:reflect-augmented pass.

**Implication for convergence claim**: The 3-channel design intended to triangulate across distinct epistemic methods (direct-read, sc:reflect, /sc:troubleshoot). With Channel B degraded to direct-read, **the effective channel count for sc:reflect-distinct insight is 0, not 1**. Convergence between Channels A and B is therefore weaker evidence than the 3-channel design promised — two direct-read passes can share blind spots that a true sc:reflect pass would surface.

**Surviving strength of the convergence claim**:
- Channel C (/sc:troubleshoot --depth deep) was *also* degraded (`--no-mcp --no-doc-discovery`, inline-fallback for Tier 2 fan-out), but it ran a *different* pipeline shape (3 hypothesis cards isolated by role-prompt, adversarial debate inline-fallback) and surfaced **M4 uniquely** — a mechanism neither A nor B's direct-read passes surfaced. This is genuine cross-channel insight, even if the channel's anchoring-defense was structurally weaker than spec-shape Tier 2.
- The mechanism artefacts cited in M1/M2/M3a/M4 are **directly verifiable on disk** (escalation-rubric.md, confidence-calibrator.md, tier2-*-calibration.md, REPORT.md, audit.log, confidence-check/SKILL.md). Each evidence line was Read-verified during the original theory-generation pass. The convergence is not the only evidence — the artefact citations are independently verifiable.

**Overall convergence strength**: **MODERATE-to-STRONG** for M1/M2/M4 (unanimous + artefact-verifiable); **MODERATE** for M3a (novel-in-B, steelmaned by A and C, artefact-verifiable but B's degradation reduces the independence of that novelty); **MODERATE** for M3b/M3c (single-source-in-C with A's secondary-section coverage, artefact-verifiable).
