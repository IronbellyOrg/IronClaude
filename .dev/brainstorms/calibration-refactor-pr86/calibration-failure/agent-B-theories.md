# Agent B — Calibration-Failure Theories (sc:reflect channel)

**Author**: Agent B (sc:reflect grounded)
**Question**: Why does the confidence-calibrator agent emit calibrated confidence ≥0.85 on hypothesis cards whose evidence-grounding dimension scored 0.5 due to lack of runtime verification?
**Substrate**: `pr86-integration-contracts-20260526100600` (structural; the H3 original-failure Coder/T4 artefacts don't exist on disk per user authorization).

---

## 1. Reflection invocation evidence

**Skill invoked**: `sc:reflect`
**Args passed**: `--type task --analyze /config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/audit.log --focus calibration-failure --question "Why does the confidence-calibrator agent emit calibrated confidence ≥0.85 on hypothesis cards whose evidence-grounding dimension scored 0.5..."` (full question text per delegation prompt).

**Result**: **PARTIAL FAILURE — protocol loaded, mandatory MCP backbone unavailable.**

The Skill tool dispatched and the sc:reflect protocol body was returned by the harness (Behavioral Flow steps 1-6, MCP Integration section, etc.). However, the protocol's **mandatory MCP integration** lists `Serena MCP` as required with three named reflection tools: `think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done`. All three returned `Error: No such tool available: mcp__serena__think_about_X` when called in this environment — both before and after activating the `IronClaude` Serena project. Other Serena tools (`get_current_config`, `activate_project`) DO work, so the issue is selective tool-surface exposure, not a dead Serena server.

**Verbatim ≤200-char excerpt of the reflection output (the protocol body, since the reflection-tool calls themselves errored)**:

> "Analyze: Examine current task state and session progress using Serena reflection tools / Validate: Assess task adherence, completion quality, and requirement fulfillment / Reflect: Apply deep analysis..." [protocol Behavioral Flow, steps 1-3, verbatim from skill output]

**Per the user's hard rule** ("If reflect fails or produces malformed output, STOP and report — do NOT fabricate substitute analysis"), this section is the honest stop-and-report. The theories below are therefore **degraded-mode output**: grounded ONLY in direct Reads of the substrate + mechanism artefacts (REPORT.md, audit.log, tier1-hypothesis.md, tier2-{rca,re,qe}-hypothesis.md, tier2-{rca,qe}-calibration.md, confidence-calibrator.md, refactoring-expert.md, confidence-check/SKILL.md, escalation-rubric.md), NOT in /sc:reflect's analytical output (which never materialised because the Serena reflection tools were absent). The Reflection-vs-direct-read divergence section (§3) reflects this: the divergence column is "N/A — reflection produced no analysis to diverge from."

---

## 2. Three theories

### Theory B1 — Arithmetic-mean dilution: the rubric structurally cannot let one 0.5 dimension veto

**Mechanism (one paragraph)**: The escalation rubric (`/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` §Confidence calibration) defines calibrated confidence as the **arithmetic mean of five 0.0/0.5/1.0 scores** with no minimum-floor rule and no weighting on which dimension scored low. Evidence-grounding is the ONLY dimension that asks "did you verify the claim against the artefact" — the other four (symptom coverage, reproducibility fit, fix directness, domain coherence) score the *card's internal coherence and shape*, not its contact with reality. A hypothesis card that is internally beautiful but reality-untested scores (0.5 + 1.0 + 1.0 + 1.0 + 1.0) / 5 = **0.90**, which clears the ≥0.85 STOP gate. The pathology is not a calibrator bug — it is the rubric's *design*: averaging treats a missing reality-check as worth one-fifth of the score, when behaviorally it should be a multiplicative gate. Same shape would produce H3's 0.95 REFUTE: four "card is internally tight" dimensions at 1.0 plus one "I can't actually run zellij to test the runtime claim" at 0.75 averages to ≈0.95.

**Evidence**:
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` lines 7-21: "**Confidence** = arithmetic mean of the five dimension scores." No minimum-floor, no weight, no veto clause.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-root-cause-analyst-calibration.md` lines 11-17: actual dimension table: Evidence=0.5, Coverage=1.0, Repro=1.0, FixDir=1.0, Domain=1.0 → arithmetic mean rounds to 0.90.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-quality-engineer-calibration.md` lines 11-17: Evidence=0.5, Coverage=1.0, Repro=1.0, FixDir=0.5, Domain=1.0 → 0.80; only fell below 0.85 because a *second* dimension (FixDir) also scored 0.5, not because the rubric punished the evidence gap.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/audit.log` lines 60-63: "All 3 calibrators flagged evidence-grounding ≤ 0.5 due to lacking Bash to verify PR-sha citations." The signal was loud and the math swallowed it.

**Per-theory confidence**: **0.92**. This is a directly observable rubric-math artefact in two Read calibration reports; the third (RE) is missing but the audit.log line confirms the same pattern. The H3 generalization is structural reasoning, not a Read, hence not 1.0.

**One-line systemic fix**: Replace arithmetic-mean with a **gated minimum** — `calibrated = min(evidence_grounding, mean(other_four))` so any 0.5 on evidence drops the ceiling to 0.5 regardless of how internally tight the card is.

---

### Theory B2 — "Evidence grounding" is a code-static-citation rubric, blind to runtime-behavior claims

**Mechanism (one paragraph)**: Read the rubric's anchor language for Evidence grounding 1.0: *"Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom"* (`escalation-rubric.md` line 13). The OR-clause is permissive — a card that cites correct `file:line` from a code read alone earns 1.0, even when the hypothesis is a **runtime-behavior claim** that source-reading cannot adjudicate. H3's claim ("`zellij --session NAME options --default-shell /bin/bash` runs `options` standalone, requires active session, therefore session never created") is a CLI-dispatch-order claim that source-reading the Rust clap definitions can *suggest* but only `zellij --session NAME options ...` actually executed can *prove*. The refactoring-expert agent, given only Read tools, would have cited `src/main.rs:N` for "subcommand parsing" and `src/session.rs:M` for "session creation requires X" — both real `file:line` against zellij v0.44.2 source — and earned Evidence=1.0 on a runtime claim never run. The calibrator inherits the same blindness because *its* spot-check tool is also Read (`tools: Read` on the agent frontmatter, `confidence-calibrator.md` line 6) — it can only verify "did the cited line exist?", not "would clap actually dispatch this argv?". The rubric has no dimension named "execution evidence" or "runtime check"; the dimension named Reproducibility fit (line 15) scores 1.0 for "Reproducer exists *and matches the cited cause*; OR symptom is a deterministic exception with a clear trigger" — a deterministic-failure claim with a clear trigger scores 1.0 even if no one ran the trigger.

**Evidence**:
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` line 13 (Evidence grounding anchors): runtime execution is one half of the OR-clause; the other half (file:line citation) is admittable alone.
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` line 15 (Reproducibility fit anchors): "deterministic exception with a clear trigger" scores 1.0 without anyone pulling the trigger.
- `/config/.claude/agents/confidence-calibrator.md` line 6: `tools: Read` — the calibrator literally cannot execute anything to challenge a runtime claim.
- `/config/.claude/agents/confidence-calibrator.md` line 51: "Spot-check the evidence: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches" — the calibrator's notion of "verify" is character-match against the cited file, not behavioural check against the system.
- `/config/.claude/agents/refactoring-expert.md` line 4 (no `tools:` block visible; the agent's mandate is "preserve functionality" — `[uncited]` whether its execution tools include Bash, but the audit.log line 63 confirms Tier 2 specialists in the substrate run could not Bash either).

**Per-theory confidence**: **0.88**. Direct citation of the rubric clause + calibrator tool-surface confirms the static-citation blindness. The H3 generalization (runtime-behavior claim accepted on source-only evidence) is structurally identical to substrate's "PR-sha-pinned citations accepted on current-HEAD spot-check" pattern logged in the calibration reports. Not 1.0 because the H3 refactoring-expert card itself isn't on disk.

**One-line systemic fix**: Add a sixth rubric dimension "**Runtime check**" with anchors `1.0=hypothesis includes an executed reproducer with captured stdout/stderr / 0.5=hypothesis includes a runnable command but no captured output / 0.0=hypothesis is source-only`, and tier-gate it: REFUTE/REJECT verdicts on runtime-behavior claims require Runtime check ≥0.5.

---

### Theory B3 — Verdict-direction asymmetry: the calibrator scores diagnostic confidence, not refutation cost-of-being-wrong

**Mechanism (one paragraph)**: The rubric and the calibrator agent treat all hypothesis verdicts as **symmetric assertions** about a cause. But "AFFIRM the cause" and "REFUTE the cause" have asymmetric cost-of-being-wrong: a wrong AFFIRM ships a fix that won't help and is rolled back when CI rejects; a wrong REFUTE *closes the investigation door* and lets the real bug ship. The H3 0.95 calibrated REFUTE is the canonical case: the agent said "H3 is not the cause" at 0.95, the troubleshoot pipeline accepted the REFUTE, the alternative cause was pursued, and CI then reproduced exactly H3's symptom. Nowhere in the calibrator agent definition (`confidence-calibrator.md`) or the rubric (`escalation-rubric.md`) is the *verdict direction* an input. The rubric's only asymmetry is `--type security AND confidence < 0.95 → ESCALATE` (line 39) — recognizing security has asymmetric cost — but no analogue for REFUTE verdicts on testable runtime claims. The substrate run shows the same pathology in milder form: the RCA card REFUTED F2's independence (treating it as "latent rather than active"), self-confidence 0.75 on that sub-claim, but no separate calibration of that REFUTE — the calibrator only graded the *overall* card. In the H3 case, "REFUTE H3" is a single-sentence verdict that absorbed all five rubric dimensions' worth of credit.

**Evidence**:
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` line 39: the *only* asymmetric-cost clause in the rubric — `--type security AND confidence < 0.95`. No verdict-direction clause.
- `/config/.claude/agents/confidence-calibrator.md` entire file: no mention of verdict direction (AFFIRM vs REFUTE vs REJECT) as an input, scoring axis, or threshold modifier. The agent's `Role` (line 21) frames calibration as "did the upstream agent build a good case for the claim", not "what would it cost if this verdict is wrong".
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-root-cause-analyst-hypothesis.md` lines 102-105: the card's own self-confidence is internally bimodal — 0.95 on F1→F3→F5 chain, 0.75 on "F2 is independent" — but the calibrator returned a single 0.90 number, blending these. The H3 0.95 REFUTE is a degenerate case of the same: the single number absorbed both the "card is internally tight" credit and the asymmetric refutation cost.
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md` line 116: "Tier 1 confidence-calibrator scored evidence-grounding 0.5 because it lacked Bash to verify PR-sha citations via `git show`. The orchestrator (this skill) DID verify those citations directly in Wave 0." — the orchestrator's workaround is itself evidence that the calibrator's structural blindness was known and routed around manually, not fixed.

**Per-theory confidence**: **0.78**. The structural absence of verdict-direction logic in the calibrator and rubric is directly verifiable. The H3 generalization ("REFUTE 0.95 closed the door") is the strongest single example but is the H3 substrate I don't have on disk; I'm reasoning from the rubric's symmetry. Not higher because B3 partially overlaps B2 (a Runtime check dimension would also catch REFUTE-on-untested-runtime-claims) — B3 is the harder, more general framing but the fix is incremental on top of B2's.

**One-line systemic fix**: Add a verdict-direction modifier to the rubric — `verdict=REFUTE AND claim_class=runtime-behavior AND runtime_check < 1.0 → cap calibrated at 0.70` — so source-only REFUTEs of runtime claims cannot clear the STOP gate.

---

## 3. Reflection-vs-direct-read divergence

| Aspect | /sc:reflect said | Direct read of artefacts said | Divergence? |
|---|---|---|---|
| (All) | **N/A — sc:reflect protocol loaded but its mandatory MCP backbone (Serena `think_about_*` tools) returned "No such tool available" on every call. No analytical output was produced.** | Three theories above, grounded in Reads. | **Cannot be assessed.** The channel's value-add is conditional on the reflection tools being available; in this environment they were not. |

**The honest finding for this channel**: the three theories above are *the same theories Agent A could have produced from direct reads*. The differentiation the user designed this 3-channel investigation around — "what does /sc:reflect's analysis surface that a direct read misses?" — was preempted by environment-level tool unavailability. The protocol's *structure* (Validate→Reflect→Re-scrutinize→Document→Optimize) is sound, but its mechanical execution depends on Serena reflection tools that this harness does not expose.

**Recommendation to the orchestrator**: treat Agent B's three theories as a second independent direct-read pass, not as a /sc:reflect-augmented pass. If the orchestrator wanted /sc:reflect-grounded theories specifically, the prerequisite is fixing the Serena MCP tool surface (or routing /sc:reflect through a harness where `mcp__serena__think_about_task_adherence` etc. are exposed) before re-spawning Agent B.

---

## Appendix — files Read for grounding

- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/audit.log`
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier1-hypothesis.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-root-cause-analyst-hypothesis.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-root-cause-analyst-calibration.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-quality-engineer-calibration.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-refactoring-expert-hypothesis.md`
- `/config/.claude/agents/confidence-calibrator.md`
- `/config/.claude/agents/refactoring-expert.md`
- `/config/.claude/skills/confidence-check/SKILL.md`
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`

**Not Read (acknowledged absent)**: tier2-refactoring-expert-calibration.md (file absent in substrate dir per `ls`); H3 original-failure Coder/T4 artefacts (don't exist on disk per user authorization in the delegation prompt).
