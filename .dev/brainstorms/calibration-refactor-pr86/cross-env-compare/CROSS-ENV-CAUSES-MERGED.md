<!-- Provenance: Produced by /sc:adversarial --compare V1,V2 --merge --depth quick -->
<!-- Base: V1 (pr86-substrate run, this environment, FINAL-MERGED-CAUSES.md, 33.7 KB) -->
<!-- Merged with V2 (T4-substrate run, other environment, FINAL-MERGED-CAUSES.md, 13.2 KB) -->
<!-- Merge date: 2026-05-27T00:35Z -->
<!-- Convergence on debate diff points: 0.14 (low — but structural, not failure: substrate-bifurcated complementarity) -->
<!-- Convergence on generation-layer rubric defects (M2 + M3a): STRONG (mechanism + fix + evidence near-identical across both substrates) -->

# Calibration-Failure Root-Cause Merge — CROSS-ENVIRONMENT (pr86 substrate × T4 substrate)

**Scope**: Why did Tier 2 produce calibration outputs that were empirically wrong (H3 0.95-REFUTE on T4, calibrated 0.90 on pr86), and why did the calibration layer fail to catch them? Synthesized across two parallel runs that observed *different substrates with structurally distinct failure modes*.

**Substrates**:
- **pr86-substrate** (V1, this environment): `pr86-integration-contracts-20260526100600` — the calibrator EXECUTED, producing on-disk artefacts (`tier2-RCA-calibration.md:11-17` shows evidence-grounding=0.5 + four 1.0s = 0.90). Failure mode: rubric math hides the only honest dimension.
- **T4-substrate** (V2, other environment): `t4-pane-title-20260526-101500` — the calibrator did NOT EXECUTE; `ls .../tier2-*-calibration.md` returns "no such file or directory." The 0.95 (H3) and 0.85 (H2) are agent self-reports passed through unchecked. Failure mode: enforcement of the protective layer failed entirely.

**The diagnostic finding**: These are *complementary* failure modes of the same calibration apparatus. pr86 shows what happens when the calibrator runs but the math is broken; T4 shows what happens when the calibrator never runs at all. Together they expose the apparatus end-to-end.

---

## Top-line synthesis

The H3 0.95-REFUTE / pr86-0.90-calibrated pathology is the **multiplicative compounding** of two structural design choices in the rubric (M1, M2), modulated by a decision-theoretic blind spot with three orthogonal sub-mechanisms (M3a/M3b/M3c), propagated by a **silent-green test suite** that institutionalizes the blindness (M4), and — critically — gated by a **non-executed audit layer (M0)** plus an **agent-domain mismatch at the assignment layer (M5)** that funnels the wrong agent type into the failure-prone path in the first place.

**Convergent across both environments**: M2 (source-vs-runtime evidence conflation) and M3a (verdict-direction asymmetry) appear in both runs with near-identical mechanism descriptions, fix prescriptions, and evidence citations (`escalation-rubric.md:11-17`, `escalation-rubric.md:13` OR-clause, `confidence-calibrator.md` symmetric AFFIRM/REFUTE treatment). This is **STRONG cross-environment convergence on the generation-layer rubric defects**.

**Substrate-divergent**: M0 (calibrator non-execution) is unique to T4 — pr86's calibrator DID run. M1 (arithmetic-mean dilution arithmetic) is sharply observable on pr86 but on T4 was downgraded to a shared assumption because no calibration artefacts existed to ground the math on. M4 (eval-suite pin tests) and the M3b/M3c sub-mechanisms are unique to V1. M5 (agent-domain mismatch) is unique to V2.

---

## M0 — Calibrator non-execution (audit layer) **[V2 unique; T4-substrate dominant]**
<!-- Source: V2 §1 #1, integrated per refactor-plan Change #1 -->

### Mechanism

The `confidence-calibrator` agent never ran against the Tier 2 hypothesis cards on the T4 substrate. The 0.95 (H3) and 0.85 (H2) values in the audit log are agent-self-reported confidences passed through unchecked. The protective layer is *defined* (`confidence-calibrator.md:24-26` — "Self-reported confidence on the card is a signal, not a number") but not *enforced* — no precondition gate in the orchestrating skill requires sibling `*-calibration.md` artefacts before audit acceptance.

### Evidence

- T4-substrate file-system fact: `ls /config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-*-calibration.md` returns "No such file or directory" (V2 line 13, 91).
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:92-93` — card's `## 4. Confidence` reads "**95%** that H3 is refuted"; same 0.95 surfaces unmodified in `audit.log:22` and `REPORT.md:166` — pass-through pattern.
- `/config/.claude/agents/confidence-calibrator.md:24-26` — the protective Independence Instruction exists; nothing enforces it.

### Merged confidence

**0.85** (capped per V2's [0.30, 0.85] discipline) — empirically verifiable on T4 substrate; **N/A on pr86 substrate** (calibrator ran there).

### Systemic fix

Add a precondition gate in `sc-troubleshoot-protocol` (or the orchestrating wave skill) that asserts: for every `tier2-*-hypothesis.md` produced, a sibling `tier2-*-calibration.md` MUST exist before the audit layer accepts the wave. Fail-loud on missing calibration artefacts. INV-002 (partial-calibration handling) is the open invariant — handle either by failing-loud or by tagging audit entries with calibration-status.

### Cross-substrate applicability

**T4-shaped substrates**: M0 is the #1 cause; M1-M4 are downstream of it (if the calibrator doesn't run, the math doesn't matter).
**pr86-shaped substrates**: M0 is not the failure mode; M1-M4 are the load-bearing causes.

---

## M1 — Arithmetic-Mean Dilution of the Only Honest Dimension **[V1; pr86-substrate dominant]**
<!-- Source: V1 §M1 retained verbatim; layer-tag added per Change #3 -->

**Layer**: generation

### Mechanism

The rubric collapses five very heterogeneous dimensions into an unweighted arithmetic mean (`escalation-rubric.md:19` — "**Confidence** = arithmetic mean of the five dimension scores"). Four of those dimensions (symptom coverage, reproducibility fit, fix directness, domain coherence) can be scored to 1.0 *purely from the card's prose* — they are essentially "is the card well-organized, internally consistent, and tightly scoped?" Only **evidence grounding** asks the question that matters for runtime-behavior claims: "does the cited line actually do what the card says it does at runtime?" When evidence-grounding is honestly scored 0.5 (because the calibrator can't run `git show` / can't execute / can't observe), it is averaged against four 1.0s and the composite still lands at **(0.5 + 1 + 1 + 1 + 1) / 5 = 0.90** — visible verbatim in `tier2-root-cause-analyst-calibration.md:9-19`. The dimension that should have *vetoed* the verdict instead contributes 20% weight.

In the H3 case the same arithmetic explains why a "I read main.rs and it falls through to start_client" verdict (evidence-grounding can only be partial because you didn't *run* it) survives as 0.95: the prose-readable dimensions all score 1.0 and dilute the one honest 0.5.

### Evidence

- `escalation-rubric.md:19` — unweighted arithmetic mean, no veto rule.
- `escalation-rubric.md:11-17` — four of five dimensions scoreable from prose alone.
- `tier2-root-cause-analyst-calibration.md:11-17` — explicit demonstration: evidence-grounding=0.5, other four=1.0, calibrated mean = **0.90**.
- `tier2-quality-engineer-calibration.md:13-17` — when fix-directness also drops, score moves to 0.60; flat-mean delta pattern confirmed.
- `REPORT.md:114-116` — orchestrator confession that calibrator's evidence-grounding score is structurally truncated.
- `audit.log:60-63` — all 3 calibrators flagged evidence-grounding ≤ 0.5; math swallowed the signal.

### Merged confidence

**0.89** on pr86 substrate (V1 unanimous across A/B/C-merged channels); **N/A on T4 substrate** (no calibration artefacts to verify the arithmetic on; V2 demoted to A-δ shared assumption).

### Systemic fix

**Primary**: Replace the unweighted arithmetic mean with a **gated minimum** — `calibrated = min(evidence_grounding + 0.3, mean(other_four))` so any 0.5 on evidence-grounding caps the ceiling regardless of how internally tight the card is.

**Alternatives**: veto-or-cap (any dimension ≤ 0.5 → composite capped at 0.75); runtime-aware clamp (cap ≤ 0.84 when evidence_grounding < 1.0 AND grounding_predicate_type=runtime_behavior).

---

## M2 — "Evidence Grounding" Conflates Source-Citation with Runtime-Verification **[BOTH environments — STRONG convergence]**
<!-- Source: V1 §M2 base; near-identical content from V2 #2; converged -->

**Layer**: generation

### Mechanism

The rubric's "Evidence grounding" row defines 1.0 as "**Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom**" (`escalation-rubric.md:13`). The OR is the trap. It permits the calibrator (and upstream agent self-grading) to score 1.0 on **source citation alone** without ever requiring "diagnostic command output reproduces the symptom."

For a static defect (missing import, wrong regex literal) this is fine — the source IS the runtime behavior. For a **dynamic-control-flow defect** (does `Some(Command::Options(...))` fall through to `start_client`? Does an empty `contract_idents` *actually* bypass the guard at runtime?), source citation can be deeply misleading: control flow that *appears* to fall through in a static read can be diverted by a match arm, a `?` operator, a panic, a feature flag, or a side-effecting initializer that wasn't on the read path. The rubric never names this distinction.

### Evidence

- `escalation-rubric.md:13` — the literal OR clause (cited by BOTH variants).
- `escalation-rubric.md:11-17` — dimension table; no claim-type/evidence-type alignment check (V2 line 41).
- `escalation-rubric.md:15` — Reproducibility-fit anchors score 1.0 without anyone pulling the trigger.
- `confidence-calibrator.md:5` (or `:6`) — `tools: Read`. Calibrator physically cannot execute anything.
- `confidence-calibrator.md:51` — snippet-match instruction (cited by V1); snippet match → 1.0 is fully compatible with runtime contradicting the card.
- T4 case: `tier2-h3-options-subcommand.md:21-79` — H3's entire Evidence section is a static source-read across 4 files; no `bash`, no `zellij list-sessions` traces. Scored 1.0 on Evidence grounding under the disjunction.

### Merged confidence

**0.85** (V1) / **0.80** (V2) — converged. Mechanism, fix, and evidence citations are near-identical across both environments. **STRONG cross-environment convergence**.

### Systemic fix

**Primary**: Add a sixth rubric dimension "**Runtime check**" with anchors: 1.0 = executed reproducer with captured stdout/stderr; 0.5 = runnable command but no captured output; 0.0 = source-only. Tier-gate it: REFUTE/REJECT verdicts on runtime-behavior claims require Runtime check ≥ 0.5.

**Alternative**: Split "Evidence grounding" into two dimensions (Source-citation accuracy + Runtime verification); for dynamic-control-flow claims, runtime-verification ≥ 0.5 must be required before source-citation can score above 0.5.

---

## M3 — Verdict-Direction Asymmetry and Anchoring-Channel Loss (composite) **[V1 composite; V2 covers M3a only]**

**Layer**: generation (M3a, M3c) / design (M3b)

The third mechanism does not converge on a single cause — it has three orthogonal sub-mechanisms with independent fixes. V1's debate explicitly resolved this as MERGE outcome (90% confidence): collapsing M3 loses two structurally valuable fixes. V2 surfaces only M3a (as its #3 cause); V2's framing converges with V1 on M3a.

### M3a — Verdict-direction asymmetry **[BOTH environments — STRONG convergence on this sub-mechanism]**

**Mechanism**: The rubric treats AFFIRM and REFUTE as symmetric assertions, but they have asymmetric cost-of-being-wrong: a wrong AFFIRM ships a fix that won't help (caught by CI); a wrong REFUTE closes the investigation door and lets the real bug ship. The H3 0.95 calibrated REFUTE is the canonical case. Nowhere in `confidence-calibrator.md` or `escalation-rubric.md` is the verdict direction an input. The only asymmetry in the rubric is `--type security AND confidence < 0.95 → ESCALATE` (line 39) — no analogue for REFUTE verdicts on testable runtime claims.

**Evidence (converged from both variants)**:
- `escalation-rubric.md:39` — sole asymmetric-cost clause is type=security, not verdict direction.
- `escalation-rubric.md:11-19` — dimension table makes no confirm/refute distinction (V2 line 54).
- `confidence-calibrator.md` — no mention of verdict direction as input, scoring axis, or threshold modifier (V1).
- T4 case: `tier2-h3-options-subcommand.md:102` — risk §6 admits one unread file would flip the refutation (V2 line 55); for a CONFIRM, one unread file would not. Asymmetric epistemic burden is directly observable in the card.

**Merged confidence**: **0.78** (V1) / **0.70** (V2). Converged across substrates.

**Systemic fix**: Add a verdict-direction modifier — `verdict=REFUTE AND claim_class=runtime-behavior AND runtime_check < 1.0 → cap calibrated at 0.70` — so source-only REFUTEs of runtime claims cannot clear the STOP gate. Composes with M2's "Runtime check" dimension.

### M3b — Stripped-context removes the doubt signal **[V1 unique]**

**Mechanism**: The calibrator is deliberately deprived of hypothesis-formation context (`confidence-calibrator.md:21`). The stated goal is to reduce anchoring bias; the cost (loss of upstream hedges, doubts, near-misses that would signal "this is a source-only-insufficient question") is unnamed. A well-written REFUTE card without hedge-text passes the strip cleanly.

**Evidence**:
- `confidence-calibrator.md:21` — explicit trail-strip.
- `hypothesis-card-template.md:104-108` — "If I'm wrong, it's probably because…" is a one-sentence alternative, NOT a falsification standard.

**Merged confidence**: **0.65**.

**Systemic fix**: Add a mandatory **Falsification standard** field to the hypothesis card template, AND require the calibrator to score whether that standard was met by the card's actual evidence.

### M3c — Residual anchoring leak from card's self-report **[V1 unique]**

**Mechanism**: `confidence-calibrator.md:25-27` instructs the calibrator to treat the card's self-reported confidence as "a signal, not a number" — prompt-level norm, not structural constraint. The calibrator sees the self-report and confident prose; producing a divergent score imposes cognitive cost.

**Evidence**:
- `confidence-calibrator.md:25-27, 36-38` — prompt-norm phrasing only.
- `confidence-calibrator.md:117-118` — Placebo Risk acknowledgment.
- `tier2-root-cause-analyst-calibration.md:21-23` — calibrator's narrative reasons about the self-report number.

**Merged confidence**: **0.45**.

**Systemic fix**: Spawn 2 calibrator instances per card (different seeds), take minimum; alternatively, mask the card's self-reported confidence from the calibrator's input.

---

## M4 — Eval-Suite Silent-Green Coverage of Structurally-Unverifiable Predicates **[V1 unique]**
<!-- Source: V1 §M4 retained -->

**Layer**: design (meta-prevention)

### Mechanism

`confidence-check/SKILL.md:14-18` advertises "Test Results (2025-10-21): Precision 1.000, Recall 1.000, 8/8 test cases passed." The eval corpus scores the calibrator on hypotheses it *can* ground — but never on hypotheses where grounding is structurally impossible (sha-pinned PR diff; runtime behavior predicted from source-only reads). The calibrator passes the test suite for the *wrong reason* — same anti-pattern V3 (quality-engineer) identified in pr86 itself.

### Evidence

- `confidence-check/SKILL.md:14-18` — blanket 1.000/1.000 claim, no per-failure-mode breakdown.
- `confidence-calibrator.md:117-118` — Placebo Risk section uses soft language ("should", "periodically"), not enforced eval-suite contracts.
- pr86 substrate: `REPORT.md:107-108` — Wave 4 converged at 0.81 yet missed the runtime defect.
- pr86 substrate: `adversarial/debate-transcript.md:128-129` — U-001 silent-green winner unanimous concession.

### Merged confidence

**0.68** (V1 only — V2 omits this cause).

### Systemic fix

Add 3 pin tests to calibrator eval suite — (a) sha-pinned citation → calibrated ≤ 0.84, (b) source-only runtime prediction → calibrated ≤ 0.84, (c) property: `evidence_grounding ≤ 0.5` → calibrated ≤ 0.85 for any input.

---

## M5 — Agent-Domain Mismatch (assignment layer) **[V2 unique]**
<!-- Source: V2 #5, integrated per refactor-plan Change #2 -->

**Layer**: assignment (upstream of M1/M2)

### Mechanism

A `refactoring-expert` agent — whose focus areas are static code-simplification — was assigned a runtime CLI-dispatch hypothesis on the T4 substrate. The mismatch produced a thorough static read and zero runtime reproduction, which the rubric (per M2) cannot penalize. The defect predates the rubric: even a perfectly-tuned rubric scoring a static work-product fairly cannot detect that the *wrong agent type* was assigned to a runtime question.

### Evidence

- `/config/.claude/agents/refactoring-expert.md:22-27` — focus areas: "Code Simplification, Technical Debt Reduction, Pattern Application, Quality Metrics, Safe Transformation." None are runtime/PTY/CLI-dispatch domains.
- T4 case: `tier2-h3-options-subcommand.md:21-79` — Evidence section is a static four-file source-read with no runtime traces — exactly the work product the agent's focus areas predict.

### Merged confidence

**0.50** (V2 cap; conservative — contributing factor, not dominant).

### Systemic fix

Add agent-domain-mismatch detection at the assignment layer: tag each hypothesis with a `claim_class` (static-defect | runtime-behavior | environment-coupled); validate the assigned agent's focus areas include the claim's domain. Reject assignments where the mismatch exceeds a threshold.

---

## Cross-mechanism implications

- **M1 and M2 compound multiplicatively, not additively.** Fix only M1 (cap on low evidence-grounding) and well-written cards still pass; fix only M2 (split or add runtime dimension) and the dilution math still hides the low new dimension. **Both fixes are required, and applying either alone underfits the failure mode.**

- **M3 is upstream of M1 and M2.** Even with veto rules (M1) and runtime-verification dimension (M2), if the rubric never weighs the cost-of-being-wrong asymmetry (M3a), the trail of doubts (M3b), or anchoring residual (M3c), source-only REFUTEs of runtime claims still clear the STOP gate.

- **M4 is the meta-prevention layer.** Without pin tests in the calibrator eval suite, fixes to M1/M2/M3 regress silently on the next eval-corpus expansion. M4 is the only prescription that doesn't require changes to the rubric or calibrator agent itself.

- **M0 and M5 are upstream of M1-M4.** If the calibrator doesn't run (M0), or the wrong agent type is assigned (M5), no amount of rubric tuning matters. The fix-stack reads bottom-up: assignment correctness (M5) → calibrator execution (M0) → rubric math (M1, M2, M3, M4).

- **Fix-sequencing constraint**: M3a's fix (verdict-direction modifier) and M2's "Runtime check" dimension chain: the modifier presupposes a runtime-check axis. **Apply M2 first, then M3a atop it.**

- **All mechanisms share a common root**: the entire calibration apparatus treats **source-reading as a complete epistemology for code claims**. This is true for static defects and structurally false for control-flow / runtime / environment-dependent claims. The H3 case (`zellij` subcommand dispatch behavior) and the pr86 case (PR-sha citations + Layer 3 emptiness bypass) both have a runtime dimension that source-only reading systematically under-detects.

- **Open invariant — partial calibration (INV-002 from V2)**: What happens when some hypotheses in a wave are calibrated and others are not? Neither variant resolves this. Verification step: read `sc-troubleshoot-protocol/SKILL.md` and search for any precondition gate that asserts "all Tier 2 cards have a sibling `*-calibration.md`." If absent, INV-002 is structurally open.

- **Substrate-vs-H3 fidelity caveat (V1)**: pr86's calibrations are 0.90 and 0.60, not 0.95. The mechanism is structurally identical but the H3 0.95 would require either (a) upstream agent self-scoring evidence-grounding at 1.0 (M2 in its strongest form), or (b) all five dimensions self-scored at 1.0 with the calibrator unable to dispute. Either route is consistent with the mechanisms above.

---

## Top root causes (merged convergence) — ranked by likelihood × blast radius, substrate-tagged

1. **M0 — Calibrator non-execution** (confidence 0.85, **T4-substrate only**, V2 unique): the audit layer accepted self-reported confidences without invoking the calibrator. Universal blast radius — every hypothesis card silently unguarded. Likelihood ≈ 1.0 on T4 substrate (`ls` returns nothing). N/A on pr86 substrate where calibration artefacts exist.

2. **M1 — Arithmetic-mean dilution** (confidence 0.89, **pr86-substrate only**, V1 unanimous): the unweighted mean lets a 0.5 evidence-grounding score average to 0.90 against four 1.0 prose-readable dimensions. Highest blast radius on pr86 substrate — affects every card the calibrator scores. N/A on T4 substrate.

3. **M2 — Source-vs-runtime evidence-grounding conflation** (confidence 0.85/0.80, **BOTH substrates — STRONG convergence**): the OR-clause in Evidence grounding lets source-citation alone earn 1.0 on runtime-behavior claims. High blast radius across both substrates.

4. **M3a — Verdict-direction asymmetry** (confidence 0.78/0.70, **BOTH substrates — STRONG convergence**): the rubric treats AFFIRM and REFUTE symmetrically; REFUTE-wrong closes the investigation door. Targeted blast radius on REFUTE verdicts of runtime claims (H3 0.95-REFUTE = canonical case).

5. **M5 — Agent-domain mismatch** (confidence 0.50, **T4-substrate prominent**, V2 unique): refactoring-expert assigned a runtime CLI-dispatch hypothesis; static work-product is structurally predictable from the agent's focus areas. Bounded blast radius — assignment surface, not rubric surface.

6. **M4 — Eval-suite silent-green coverage** (confidence 0.68, **substrate-independent**, V1 unique): the calibrator's "1.000 precision/recall" eval corpus never tested it on structurally-unverifiable predicates. Largest *regression* blast radius — without M4, all other fixes silently regress.

7. **M3b + M3c — Stripped-context doubt-signal loss + residual anchoring** (combined confidence ≈ 0.55, **substrate-independent**, V1 unique): two information-channel weaknesses with independent fixes (Falsification-standard card field + dual-instance-minimum).

**Required fixes are compositional, not exchangeable**: enforce-calibrator-execution gate (M0) + agent-domain-mismatch detector (M5) + gated-minimum rubric formula (M1) + Runtime-check 6th dimension (M2) + verdict-direction modifier (M3a) + Falsification standard field (M3b) + dual-instance-minimum (M3c) + pin tests (M4). Applying any subset underfits the failure mode.

---

## Shared Assumptions (Limits of This Analysis)
<!-- Source: V2 §5 (A-α, A-β, A-γ, A-δ), integrated per refactor-plan Change #5; V1 left these unstated -->

Both variants share the following assumptions; flagged for Step 4 brainstorm attention:

- **A-α — Rubric/calibrator IS the right layer to fix.** Both variants prescribe fixes at the rubric and calibrator-agent layers. Neither considers an upstream verification-gate (runtime-output-required-before-confidence-eligible) sitting upstream of the rubric entirely. If the right fix is an upstream gate, both merges are recommending the wrong layer. **Status**: UNSTATED in V1; STATED in V2 (A-α).

- **A-β — Confidence ≥0.90 has operational meaning downstream.** Both treat 0.95 as load-bearing. If downstream consumers (orchestrators, escalation gates) actually branch on coarse buckets (e.g., {<0.70, 0.70–0.89, ≥0.90}), the calibration-precision target is much weaker than this analysis implies.

- **A-γ — Negative existential cards are gradable.** Both assume H3 ("no early-return exists anywhere") *can* receive a meaningful confidence score under a fixed rubric. It may be that such claims should be rejected at intake and required to convert to a positive falsifiable form.

- **A-δ — Rubric aggregation is arithmetic mean.** Confirmed by `escalation-rubric.md:19`. The assumption is correct *as written* but never re-derived — alternatives (worst-dimension-wins, geometric mean, dimension-weighted) were not considered as remediation surfaces. V1 attacks this directly via M1; V2 leaves it as a shared assumption.

---

## Cross-Environment Synthesis
<!-- Required by the task description; surfaces convergence/substrate-sensitivity/confidence-calibration/numeric-specifics that the skill protocol doesn't natively produce -->

### 1. Convergence on causes

**STRONG convergence (mechanism + fix + evidence near-identical across substrates)**:
- **M2** (rubric OR-clause / evidence-class disjunction): both variants cite `escalation-rubric.md:11-17` and the OR clause at line 13; both recommend a Runtime-check dimension or rubric split; both score in [0.80, 0.85].
- **M3a** (verdict-direction asymmetry): both variants identify AFFIRM/REFUTE rubric symmetry as a defect; both cite the H3 case; both recommend verdict-direction modifier capping. V1 cites `escalation-rubric.md:39` security-only asymmetry as the sole existing analogue; V2 cites the same `escalation-rubric.md:11-19` table absence. Confidence scores 0.78 (V1) and 0.70 (V2).

**Substrate-divergent (each environment's substrate exposed a different failure mode)**:
- **M0 (calibrator non-execution)** appears in V2 only — empirically irrefutable on T4 substrate where `ls tier2-*-calibration.md` returns empty; not applicable on pr86 substrate where the calibrator ran.
- **M1 (arithmetic-mean dilution arithmetic)** appears in V1 as a top cause because pr86 has the calibration artefacts on disk to ground the math (`(0.5+4×1.0)/5=0.90`); V2 demotes it to A-δ shared assumption because T4 has no artefacts to verify.

**Unique additive contributions (substrate-independent value)**:
- **M4 (eval-suite pin tests)** — V1 only. Prevention-layer value applies to both substrates.
- **M3b + M3c (sub-mechanism decomposition)** — V1 only. Two independently-deployable fixes (Falsification-standard field; dual-instance-minimum).
- **M5 (agent-domain mismatch)** — V2 only. Assignment-layer cause applies across substrates.

### 2. Substrate-sensitivity

The bifurcation is itself diagnostic:

| Failure mode | pr86 substrate | T4 substrate |
|--------------|----------------|--------------|
| Calibrator executed? | YES (artefacts on disk) | NO (artefacts absent) |
| Dominant cause | M1 (math broken) | M0 (calibrator never ran) |
| Source-of-truth for failure | `tier2-*-calibration.md` files | `ls` returning empty |
| What we'd miss if we only had this substrate | M0, M5 | M1, M4, M3b, M3c |

**Implication**: A single-substrate investigation systematically misses ~half of the failure-mode surface. Cross-environment comparison is methodologically valuable not for redundancy but for *complementary coverage*.

### 3. Confidence calibration delta

| Cause | V1 confidence | V2 confidence | Delta | Notes |
|-------|---------------|---------------|-------|-------|
| M0 (calibrator non-execution) | N/A (not surfaced) | 0.85 | — | Substrate-specific |
| M1 (arithmetic-mean dilution) | 0.89 | N/A (demoted to A-δ) | — | Substrate-specific |
| M2 (OR-clause) | 0.85 | 0.80 | -0.05 | Within noise; converged |
| M3a (verdict-direction) | 0.78 | 0.70 | -0.08 | V2 cap discipline at 0.85 caps the spread; converged |
| M4 (pin tests) | 0.68 | N/A | — | V1 only |
| M5 (agent-domain) | N/A | 0.50 | — | V2 only |
| A-α (right-layer assumption) | UNSTATED | STATED | — | V2 names what V1 leaves implicit |

**Where they disagree, neither run's evidence is "stronger"** — they're observing different substrates. V2's per-cause likelihood discipline ([0.30, 0.85] cap) is methodologically conservative; V1's higher numbers reflect directly-observable-on-disk evidence on its specific substrate.

### 4. Numeric specifics

- **pr86 (V1) cites arithmetic verbatim**: `(0.5 + 1 + 1 + 1 + 1) / 5 = 0.90` from `tier2-root-cause-analyst-calibration.md:11-17`; also `(0.5 + 0.5 + 3×1.0) / 5 = 0.60` for the QE delta pattern.
- **T4 (V2) does NOT cite analogous arithmetic on the actual H3 card** — because the calibrator did not run, no calibrated arithmetic exists to cite. V2 cites the *self-reported* "95%" from the H3 card (`tier2-h3-options-subcommand.md:92-93`) and notes its pass-through to `audit.log:22` and `REPORT.md:166`.
- **What this tells us about the underlying H3 mechanism**: The H3 0.95-REFUTE on T4 is NOT calibrated arithmetic — it is *upstream agent self-grading*, then pass-through. The pr86 substrate's calibrated 0.90 is the *closest structural analogue* of what the calibrator *would have produced* on T4 if it had run. So V1's M1 arithmetic IS the structural prediction for what H3 0.95 *should have looked like under calibration* — strengthening V1's M1 mechanism as the substrate-independent prediction, not just a pr86-specific observation.

### 5. Convergence strength assessment: **STRONG on generation-layer rubric defects; MODERATE on the full mechanism stack**

- **STRONG** on M2 + M3a: identical mechanism descriptions, near-identical fix prescriptions, overlapping evidence citations, confidence scores within 0.08 of each other across two independently-run merges on different substrates.
- **MODERATE on the full stack**: the substrate-divergence in X-001 means neither environment alone produces a complete diagnosis. The merged output combines them, but the merge depends on accepting both substrates' findings as valid observations of complementary failure modes, not contradictions.
- **STRONG on the underlying-pathology framing**: both environments converge on the same root claim — "the calibration apparatus treats source-reading as a complete epistemology for code claims, and this is structurally false for runtime/control-flow/environment-coupled claims." V1 names this in its Cross-mechanism implications ¶5; V2 implies it across its #2, #3, and #5 causes.

**Overall convergence**: **STRONG** at the conceptual-pathology level; **MODERATE** at the mechanism-enumeration level (because of substrate-divergence in observability, not because of disagreement); **STRONG** at the recommended-fix level (both environments recommend a runtime-verification dimension and verdict-direction modifier, with V1's M4 pin-test prevention layer as an unambiguous additive value).

---

## Synthesis addendum (Step 3 post-process — required structural pieces)
<!-- Retained from V1 with substrate-tag annotations -->

### 1. Top 3-5 root causes ranked by likelihood × blast radius

See §"Top root causes (merged convergence)" above (7 causes, ranked).

### 2. Convergence evidence — unanimous vs partial/single-source

**Unanimous across both environments (STRONG cross-substrate convergence)**:
- M2 mechanism + evidence + fix family (escalation-rubric.md:11-17, :13, confidence-calibrator.md tools:Read).
- M3a mechanism + fix family (verdict-direction modifier).
- A-δ (arithmetic-mean rubric structure, confirmed correct as-written from escalation-rubric.md:19).

**Substrate-specific (one environment's substrate exposed it; the other's didn't)**:
- M0 (calibrator non-execution): V2 / T4 only — empirically falsifiable per `ls`.
- M1 (arithmetic dilution arithmetic): V1 / pr86 only — empirically observable per calibration artefacts on disk.

**Single-source additive**:
- M4 (eval-suite pin tests): V1 only — substrate-independent prevention layer.
- M3b + M3c (sub-mechanism decomposition): V1 only — independently-deployable fixes.
- M5 (agent-domain mismatch): V2 only — assignment-layer cause.

### 3. Compositional vs exchangeable analysis

**Compositional (must combine — applying any subset underfits)**:
- M1 fix (gated-minimum) + M2 fix (Runtime check dimension): multiplicative.
- M3a (verdict-direction modifier) presupposes M2 (Runtime check axis): sequential, M2 first.
- M0 (calibrator-execution gate) is upstream of M1/M2/M3/M4: enforce calibrator runs before tuning what it produces.
- M5 (agent-domain mismatch detector) is upstream of M0: tag claim_class before assignment, before calibration, before scoring.
- M4 (pin tests) compounds with everything: without M4, all other fixes silently regress.

**Exchangeable (each can ship independently)**:
- M3a, M3b, M3c are independent of each other; each addresses a different leak.
- M4's three pin tests (sha-pinned, source-only runtime, evidence_grounding≤0.5 property) are independent.
- M1 fix formula choice (gated-minimum vs veto-or-cap vs runtime-aware-clamp) is exchangeable.
- M2 fix shape choice (sixth dimension vs split-into-two) is exchangeable.

### 4. Open conflicts where the merged inputs disagreed substantively

**Only one substantive conflict surfaced** (X-001):
- **Conflict**: Did the calibrator execute on the substrate under investigation?
- **Resolution**: SUBSTRATE-DEPENDENT — V1's pr86 substrate had calibration artefacts on disk (YES); V2's T4 substrate did not (NO, empirically). Both findings are correct *on their respective substrates*. The merged output is substrate-aware, tagging each cause with its applicability domain.
- **Rationale for resolution**: this isn't a contradiction between merges — it's a diagnostic finding about substrate-divergent failure modes. Both observations stand.

**No other substantive conflicts.** Remaining differences are stylistic (provenance density), lengths (269 vs 139 lines), or framing (mechanism-decomp vs ranked-list with layer-tags).

### 5. Process degradation note

Both V1 and V2 had degraded run conditions (V1's Channel B sc:reflect tool failures + Channel C /sc:troubleshoot fan-out degradation; V2's terser format suggests fewer adversarial debate rounds). The convergence on M2 and M3a across two degraded runs on different substrates is *stronger* evidence than convergence in a single full-fidelity run would have been — both runs surfaced the same generation-layer defects through different reasoning paths.

**Surviving strength of the convergence claim**:
- Mechanism artefacts cited in M2 and M3a are directly verifiable on disk in both environments.
- The substrate-divergence in M0 vs M1 is not a weakness — it's the diagnostic value-add of cross-environment comparison.
- M4 (V1 unique) and M5 (V2 unique) being orthogonal additive contributions, not disagreements, strengthens the merged output.

**Overall convergence strength**: **STRONG** at the conceptual-pathology level (both environments diagnose the same underlying defect: source-reading treated as complete epistemology for code claims). **MODERATE** at the mechanism-enumeration level (substrate-bifurcation, not disagreement). **STRONG** at the recommended-fix level (both environments recommend runtime-verification + verdict-direction-modifier as the load-bearing fixes).
