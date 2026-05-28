# Agent C — Calibration-Failure Theories (via /sc:troubleshoot --depth deep)

## 1. Troubleshoot invocation evidence

**Skill tool call:**

```
Skill sc:troubleshoot with args:
  --depth deep --type bug
  --scope /config/.claude/agents/confidence-calibrator.md
  --output-dir /config/workspace/IronClaude/.dev/troubleshoot/
    pr86-integration-contracts-20260526100600/calibration-failure/troubleshoot-run
  --no-doc-discovery --no-mcp
  "Why did the H3 hypothesis card score 0.95 confidence when empirical
   evidence later refuted it? Treat the calibration failure itself as a
   bug whose root cause needs to be found. Ground in
   /config/workspace/IronClaude/.dev/troubleshoot/
     pr86-integration-contracts-20260526100600/ (same calibration-failure
   family — Tier 2 calibrations scored evidence_grounding=0.5 due to
   absent Bash, but RCA card still landed at 0.90 calibrated because four
   1.0 dimensions averaged the 0.5 hole away) plus
   /config/.claude/agents/confidence-calibrator.md and
   /config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
   (arithmetic-mean rubric that permits high overall confidence with a
   single-dimension grounding gap)."
```

**Skill tool returned**: the full `/sc:troubleshoot` command spec (Wave 0–6 protocol). Execution proceeded inline per Activation requirement.

**Verbatim ≤200-char excerpt from troubleshoot pipeline output** (`troubleshoot-run/tier1-hypothesis.md`):

> "The calibrator returns a flat arithmetic mean of 5 dimensions with no floor, no veto, and no domain-aware weighting. When a hypothesis is grounded only in static-source reads but predicts runtime behavior, Evi"

(Full content of Tier 1 hypothesis, 3 Tier 2 hypothesis cards, audit log, merged adversarial output, and Wave 5 REPORT.md draft all generated under `troubleshoot-run/`. The Wave 5 REPORT.md write was blocked by the subagent file-write constraint; full prose is preserved inline below in theory derivation. All other Wave artifacts were successfully written.)

**Pipeline status**: Tier 2 reached, `escalation_reason: forced_by_depth_deep`, adversarial debate produced HYBRID winner. Wave 5 evidence-validator inline-fallback applied; all cited file:line verified against this turn's Read tool calls. Calibration ran inline-fallback per Wave 1.7 / Wave 3.5 failure-handling clauses (no Task subprocess; `--no-mcp` precluded the standard agent spawn shape).

---

## 2. Three Distinct Theories

### Theory C1 — Arithmetic-mean rubric is dimension-orthogonality blind

**Mechanism.** The escalation rubric defines `confidence = arithmetic mean(5 dimensions)` with no floor, no veto, no causal-dependency weighting. For hypotheses whose other dimensions are *conditional on* Evidence-grounding being verified (runtime-behavior predictions like H3; sha-pinned PR citations like pr86), the 0.5 grounding score should propagate through symptom-coverage, reproducibility-fit, and fix-directness — those scores only make sense IF the unverified grounding is correct. Averaging them treats them as independent, which is a category error. Numerically: 0.5 + 4×1.0 → mean 0.90, which clears the 0.85 escalate-or-stop gate exactly when the dimension that could have caught the runtime miss has been red-flagged.

**Evidence.**
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:19` — `Confidence = arithmetic mean of the five dimension scores. Round to two decimals.` No floor.
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:41` — escalate threshold is 0.85; arithmetic 0.90 passes.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-root-cause-analyst-calibration.md:13`: `Evidence grounding | 0.5 | ... calibrator lacked Bash to git show and verify`. Other 4 dimensions all 1.0. Mean = 0.90.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-quality-engineer-calibration.md:13` — same 0.5 with same Bash-absent reason. Only landed at 0.60 because fix-directness ALSO dropped to 0.5 (two-dimension drop required; one isn't enough to defeat the average).
- `/config/.claude/agents/confidence-calibrator.md:7,8` — `tools: Read`, `permissionMode: plan`. Bash structurally absent. The "verify with command output" pathway in rubric row 1 (`escalation-rubric.md:13`) is unreachable for runtime claims.

**Per-theory confidence: 0.85.** Justification: arithmetic mechanism is empirically verified against two pr86 calibrations with identical fingerprint to the H3 miss; the 3-dimension delta pattern between RCA (0.90) and QE (0.60) is exactly what the flat-mean predicts and no other theory explains as crisply. The 0.15 reserved is for whether the rubric is *load-bearing* vs *channel through which other failures express themselves*.

**Systemic fix (one line):** Replace flat arithmetic mean with `min(mean, evidence_grounding + 0.3)` when hypothesis predicts runtime behavior, OR cap calibrated ≤ 0.84 when `evidence_grounding < 1.0` AND `grounding_predicate_type=runtime_behavior` (new card field).

---

### Theory C2 — Calibrator eval suite has silent-green coverage of structurally-unverifiable predicates

**Mechanism.** `confidence-check/SKILL.md:14-18` advertises "Test Results (2025-10-21): Precision 1.000, Recall 1.000, 8/8 test cases passed." The eval corpus scores the calibrator on hypotheses it *can* ground — but never on hypotheses where grounding is structurally impossible (sha-pinned PR diff; runtime behavior predicted from source-only reads). The calibrator passes the test suite for the *wrong reason* — same anti-pattern V3 (quality-engineer) identified in pr86 itself (`adversarial/debate-transcript.md:69`: "test_t1/t6/t7 silently green-bar on substring containment of `FR-S10-02`"). The "1.000 precision/recall" claim is doing the work of a calibration-quality signal it cannot actually carry. Applied recursively: the calibrator failed the H3 case the same way pr86's test_t1 failed F1 — green-bar on irrelevant invariant.

**Evidence.**
- `/config/.claude/skills/confidence-check/SKILL.md:14-18` — blanket 1.000/1.000 claim, no per-failure-mode breakdown, no listed case for "structurally-unverifiable predicate."
- `/config/.claude/agents/confidence-calibrator.md:117-118` — Placebo Risk section: "if the calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead. The orchestrator should periodically run head-to-head meta-evals" — *should* and *periodically* are soft language, not enforced eval-suite contracts.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md:107-108` — Wave 4 in pr86 converged at 0.81 yet missed the helper-not-uppercasing runtime defect that rf-qa-qualitative caught only in A.10.5 cycle 1. Same "tests passed but ran wrong invariant" shape at adversarial-merge scope. [uncited at file:line for A.10.5 details — referenced in the substrate REPORT narrative]
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/debate-transcript.md:128-129`: U-001 silent-green winner = V3 (QE) at 95% confidence — unanimous concession that without pin tests, downstream cannot distinguish "fix worked" from "fix had no effect."

**Per-theory confidence: 0.68.** Justification: recursion-of-the-same-anti-pattern is rhetorically strong and substrate-confirmed at multiple scopes, but the claim is *necessary-but-not-sufficient* — pin tests alone would just freeze the rubric's current behavior as the expected behavior. C2 sits as a guardrail; it is not the load-bearing mechanism (C1 is) but it is the load-bearing *prevention* mechanism.

**Systemic fix (one line):** Add 3 pin tests to calibrator eval suite — (a) sha-pinned citation → calibrated ≤ 0.84, (b) source-only runtime prediction → calibrated ≤ 0.84, (c) property: `evidence_grounding ≤ 0.5` → calibrated ≤ 0.85 for any input.

---

### Theory C3 — Residual anchoring leak from card's self-report + narrative framing defeats the prompt-level anti-anchoring norms

**Mechanism.** `confidence-calibrator.md:25-27` instructs: "Self-reported confidence on the card is a signal, not a number. Treat it as part of the card's narrative, not as input to your score." This is a *prompt-level norm*, not a structural constraint. The calibrator agent sees the card's self-report number and confident prose ("source-only reads at v0.44.2 conclusively show…" — the H3 refactoring-expert framing) inside its context window. Producing a calibrated score that diverges sharply from the self-report imposes a small but real cognitive cost — the prompt says "surface honestly," but the agent has no structural counter-pressure. Empirically: pr86's RCA calibration delta is +0.02 (self-reported 0.88 → calibrated 0.90); QE delta is -0.28 — but the -0.28 came from TWO dimensions dropping (the mechanical signal was unambiguous), not from anti-anchoring discipline. When only one dimension wobbles, the calibrated score hugs the self-report.

**Evidence.**
- `/config/.claude/agents/confidence-calibrator.md:25-27`: "Self-reported confidence on the card is a signal, not a number." Prompt-norm phrasing, not structural masking.
- `/config/.claude/agents/confidence-calibrator.md:36-38`: "Never split the difference to please the upstream agent." Norm, not structure.
- `/config/.claude/agents/confidence-calibrator.md:117-118`: "Placebo Risk: if the calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead." Meta-spec acknowledgment that the agent struggles to distinguish itself from inline.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-root-cause-analyst-calibration.md:21-23`: "Self-reported: 0.88 / Calibrated: 0.90 / Delta: +0.02 — card's self-report was pulled down by F2-independence uncertainty; calibrator rewards mechanical strength of the F1+F3+F5 chain". The calibrator's narrative is *reasoning about* the self-report (engaging with it as a number, weighing what pulled it up or down) — the precise behavior the spec said not to do.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-quality-engineer-calibration.md:23`: "Delta: -0.28" — the -0.28 came from fix-directness ALSO dropping (mechanical evidence). When mechanical signals all point one way, the calibrator follows them; when only one is ambiguous, the narrative carries the day. [interpretive — uncited that "narrative carries the day" is the operative cause; supporting only by the delta-pattern asymmetry]

**Per-theory confidence: 0.45.** Justification: anchoring is mechanistically plausible and the delta-pattern is consistent with it, but the same delta is *equally consistent* with C1 (arithmetic propagation) — both predict "single-dimension drop yields small delta, multi-dimension drop yields large delta." Available evidence cannot distinguish them. C3 is therefore a defensible secondary mechanism, not a load-bearing primary.

**Systemic fix (one line):** Spawn 2 calibrator instances per card (different seeds), take the *minimum* score; alternatively, mask the card's self-reported confidence in the calibrator's input (replace with `<HIDDEN>`).

---

## 3. Where the troubleshoot tiers landed

**Tier 1**: Inline-formed hypothesis — `tier1-hypothesis.md` (calibrated **0.90** via inline-fallback applying the same rubric to itself, which is itself a fitting confirmation of C1). Self-reported 0.78 → calibrated 0.90, delta +0.12 caused by fix-directness drop being the *only* off-1.0 dimension, exactly the asymmetry C1 predicts.

**Wave 2 gate**: `--depth deep` → forced escalate. `escalation_reason: forced_by_depth_deep`.

**Tier 2 fan-out**: 3 hypothesis cards produced inline (Task subprocess unavailable in this turn) representing root-cause-analyst, quality-engineer, refactoring-expert specialties. Each card maps 1:1 to theory C1/C2/C3 above; the troubleshoot pipeline's parallel-perspectives requirement is what *generated* the 3 theories.

**Tier 2 calibration** (inline-fallback per Wave 3.5 failure-handling):
- H-RCA → 0.90 (single-dimension drop, fix-directness)
- H-QE → 0.80 (two dimensions: symptom-coverage covers only test angle; fix-directness broad)
- H-RefExp → 0.70 (evidence-grounding partial; reproducibility partial)

**Wave 4 adversarial debate**: HYBRID winner. C1 is load-bearing (arithmetic must change); C2 is necessary guardrail (pin tests); C3 is defense-in-depth.

**Meta-observation (why running troubleshoot ON the calibrator was load-bearing)**: The Tier 2 fan-out is the *only* mechanism in this codebase that surfaces 3 *distinct* mechanism claims for a single calibration miss. A single-perspective Tier 1 pass would have landed on C1 alone and missed the recursive eval-coverage shape (C2) — which mirrors the very anti-pattern pr86 itself diagnosed at production-code scope. The recursion is itself a verification: the calibration system is failing the same way the code it was calibrating was failing, and only the parallel-perspectives machinery surfaced that isomorphism.

**Pipeline degradation surfaced in Grounding Gaps**: `--no-mcp` and `--no-doc-discovery` set; Task subprocess not used for hypothesis or calibration (inline-fallback). The 3 hypothesis cards are isolated by *role-prompt*, not by *fresh context window* — anchoring-defense is structurally weaker than spec-shape Tier 2. Findings remain defensible because each theory cites mechanism artefacts verified against Read in this turn.
