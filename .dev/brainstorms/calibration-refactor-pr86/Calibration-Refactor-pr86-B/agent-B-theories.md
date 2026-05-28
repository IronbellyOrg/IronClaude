# Agent B — /sc:reflect-grounded theories for the H3 calibration miss

## /sc:reflect summary

Invocation: `/sc:reflect --type task --analyze` (skill name `sc:reflect` resolved on the first try; protocol loaded into context and applied to the artifact directory). The three Serena reflection lenses — **task adherence**, **collected information**, **completion** — surface a single dominant pattern when pointed at `tier2-h3-options-subcommand.md`: the card's evidence chain proves a *different proposition* than the one the rubric scores. The card proves "CLI parses cleanly and dispatch flows to `start_client`" (a structural claim) at high confidence; it does not prove "the failing artifact log was not produced by the `options`-subcommand code path" (the operative claim that 0.95 REFUTE actually requires). /sc:reflect also flags that the card's §7 explicitly identifies the unread `start_client_impl` body as the residual risk — and that the calibrator, per the agent spec, was supposed to mechanically penalize "Evidence grounding" when cited snippets do not exhibit the symptom (escalation-rubric.md:13). Neither the self-grade nor the calibrator did so. Finally, "completion" analysis shows H3 was scored *higher* than the empirically winning H1 (0.95 vs 0.82) despite H1 having strictly more evidence types (source + literal artifact-log strings + T3 corroboration); this inversion is itself a calibration smell that no automated check caught.

## Theory B1: Proposition substitution — H3's evidence proves CLI-shape, the rubric scored it as if it proved symptom-absence

**Claim:** The H3 card's four evidence chains (E1 CLI struct, E2 dispatcher, E3 `start_client`, E4 options-merge) jointly prove that `--session NAME options ...` *parses to* a session-creating dispatch. They do **not** prove that the failure-mode the test is hitting was not produced by that dispatch. The rubric's "Evidence grounding 1.0" anchor requires citations to "a real code path that exhibits the symptom" (escalation-rubric.md:13) — H3's citations exhibit only the absence of an early-return, not the absence of the symptom. The 0.95 REFUTE silently substituted a weaker, easier-to-defend proposition for the one the investigation actually needed answered.

**Reflect-derived evidence:** `think_about_collected_information` surfaces a mismatch between the card's claim ("session IS created") and the symptom it was supposed to discharge ("session never registers in `list-sessions`"). Creation and registration are different events in zellij's lifecycle (`SessionInfo` registration happens after layout selection and plugin load, per Branch-A's own reading of `zellij-server/src/lib.rs`). The H3 card never bridges the gap.

**Artifact evidence:**
- `tier2-h3-options-subcommand.md:51` — E3 concludes "INITIATES CREATION OF A NEW SESSION" but stops before registration; the symptom is a registration failure, not a creation failure.
- `tier2-h3-options-subcommand.md:107` — §7 explicitly admits `start_client_impl` body was not retrieved; the leap from "dispatcher calls start_client" to "session registers" is therefore not source-grounded.
- `tier1-observation.md:5-12` — symptom is "did not register within 15s" (a `list-sessions` poll), not "creation rejected".
- `wave1_5-branch-A.md:80-82` — Branch A itself flags Q5 (`options` subcommand starts a session vs sets options) as "partial / uncertain... empirical test required" — H3 collapsed this uncertainty without empirical work.
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:13` — Evidence-grounding 1.0 requires citations exhibiting *the symptom*, not adjacent behavior.

**Per-theory confidence:** 0.80
**Systemic fix (one line):** Calibrator must extract the operative proposition from the card's "Claim" section and reject Evidence-grounding ≥ 0.5 when no cited line exhibits the actual symptom, not just adjacent code paths.

## Theory B2: Refute-asymmetry — the rubric and calibrator have no special handling for refutation claims, which require strictly more evidence than confirmation claims

**Claim:** Confirming a hypothesis ("X causes Y") requires showing a plausible mechanism; refuting one ("X cannot cause Y") requires ruling out *every* mechanism by which X might cause Y — a strictly larger evidentiary burden. The rubric (`escalation-rubric.md`) treats both verdict directions symmetrically: the same 5 dimensions, same 1.0/0.5/0.0 anchors, same averaging. The confidence-calibrator agent spec (`confidence-calibrator.md`) inherits this symmetry. A 0.95 REFUTE on a source-only investigation is treated as equally well-grounded as a 0.95 CONFIRM, even though refutation requires the agent to have *also* read every code path it didn't read. H3's 0.95 is the predictable failure mode of this symmetric framing.

**Reflect-derived evidence:** `think_about_task_adherence` checks whether the *approach* matches the *goal*. H3's goal was "rule out the structural-bug hypothesis"; its approach was "read four files and find no obvious refutation in them." Adherence is low: the goal demanded exhaustive search, the approach was bounded sampling. The rubric does not encode this asymmetry, so the calibrator could not penalize it.

**Artifact evidence:**
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-19` — the dimension table makes no distinction between confirm/refute claims; "Evidence grounding 1.0" is defined identically for both.
- `/config/.claude/agents/confidence-calibrator.md:48-55` — Responsibilities §4 says "Score each dimension 0.0/0.5/1.0 per the rubric's anchor language" — purely mechanical against a symmetric rubric.
- `tier2-h3-options-subcommand.md:93` — confidence rationale: "four primary-source evidence chains... converge on the same conclusion from independent files in the same v0.44.2 tag" — four *positive* observations (no early-return seen) used to ground a *negative* claim (no early-return exists anywhere). This is the asymmetry, displayed plainly.
- `tier2-h3-options-subcommand.md:102` — risk §6 admits "If `start_client_impl` has a guard that early-returns when `command == Some(Command::Options(_))`, the refutation would weaken" — i.e., one unread file flips the verdict; for a CONFIRM, one unread file would not.
- `REPORT.md:158-169` — both H2 (0.85 refute) and H3 (0.95 refute) carry high refute confidences despite both being source-only; H1 (the empirically correct CONFIRM) carries 0.82. The inversion is consistent with the asymmetry being invisible to the rubric.

**Per-theory confidence:** 0.72
**Systemic fix (one line):** Add a rubric branch — for REFUTE verdicts, cap Evidence-grounding at 0.5 unless the card includes an empirical/runtime negative result, not just a source-read absence-of-positive.

## Theory B3: Calibrator role under-spec — "formation context stripped" was implemented as "card-only input" without removing the anchor that actually biases the score

**Claim:** The calibrator agent spec (`confidence-calibrator.md:21`) names the anchor it is supposed to defeat: "the upstream investigative trail is not [shown] — that is where the dominant anchoring bias lives." But the dominant anchor for a REFUTE card is not the investigative trail; it is the **card's confident narrative** ("CONFIRMED 0.95... four primary-source evidence chains converge"). Stripping the trail leaves the narrative fully intact, in fact *more* persuasive (no trail to introduce doubt). The calibrator spec acknowledges this risk (`confidence-calibrator.md:25` — "Self-reported confidence is a signal, not a number") but provides no procedural defense beyond an instruction. Instructions do not survive a well-written REFUTE.

**Reflect-derived evidence:** `think_about_whether_you_are_done` against the calibration step surfaces an incompleteness: the agent is told *what not to do* (don't inherit the narrative framing) but not given a counter-procedure (e.g., "draft a hypothetical CONFIRM card from the same evidence and check which is better supported"). Without the counter-procedure, the calibrator's defense is willpower against a well-crafted card — a defense that does not generalize.

**Artifact evidence:**
- `/config/.claude/agents/confidence-calibrator.md:21` — "anchoring bias... lives [in the investigative trail]" — locates the bias in the wrong place; for REFUTE cards the bias is in the narrative.
- `/config/.claude/agents/confidence-calibrator.md:25-27` — Independence Instruction is exhortatory ("treat as signal, not number") with no mechanical step.
- `/config/.claude/agents/confidence-calibrator.md:35` — "Your defense against the residual anchor is mechanical discipline" — names mechanical discipline as the defense but the only mechanical steps that follow are "score one dimension at a time" (which a fluent narrative satisfies trivially) and "spot-check citations" (H3's citations all match — the bug is what the citations *don't* show).
- `tier2-h3-options-subcommand.md:3` — the card's opening verdict is written as settled fact ("**Verdict: REFUTED.**") with bolded emphasis — exactly the narrative shape the calibrator has no procedural defense against.
- `/config/.claude/skills/confidence-check/SKILL.md:114-120` — the production `confidence-check` skill thresholds (≥0.90 to proceed, <0.70 to stop) are calibrated for CONFIRM-style implementation decisions; the troubleshoot rubric reuses the same numeric scale for REFUTE verdicts without re-calibration. The 0.95 in H3 borrowed authority from a scale that was never validated against refutation.

**Per-theory confidence:** 0.68
**Systemic fix (one line):** Calibrator spec must add a procedural counter-anchor: for any REFUTE verdict ≥ 0.85, the calibrator must draft a one-paragraph steel-manned CONFIRM from the *same* evidence and downgrade the REFUTE confidence by the strength of the steel-man.
