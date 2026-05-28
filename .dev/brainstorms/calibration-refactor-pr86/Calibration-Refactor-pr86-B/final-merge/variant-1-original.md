<!-- sc:adversarial invocation -->
<!-- Skill name resolved: sc:adversarial (resolved on first attempt; loaded sc-adversarial-protocol as documented) -->
<!-- Skill output original path: /config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/calibration-failure/agent-A-adversarial/adversarial/ (artifacts) -->
<!-- Inputs: agent-A-theories.md, agent-B-theories.md, agent-C-theories.md -->
<!-- Depth: quick -->
<!-- Mode: --compare --merge -->

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (agent-C: sc:troubleshoot-grounded) — selected by Level 1 tiebreaker on debate performance -->
<!-- Merge date: 2026-05-26 -->

# Merged synthesis — H3 calibration-failure theories

<!-- Source: Base (C), preserved structural pattern -->

## Method-grounding summary

<!-- Source: Base (C, original); enriched with A and B method lenses -->

Three independent passes converge on overlapping but non-identical theories:

- **Variant A (first-principles)** isolates the rubric language as the proximal mechanism — the OR-disjunction in `escalation-rubric.md:13` mechanically permits a source-only refutation of a runtime claim to earn 1.0 on the load-bearing Evidence-grounding dimension.
- **Variant B (`/sc:reflect`-grounded)** reframes the failure as **proposition substitution**: the card proves a different proposition (CLI parses cleanly into a session-creating dispatch) than the one the rubric scores it against (the failing artifact log was not produced by the `options`-subcommand code path). B also names the verdict-direction asymmetry (refute requires strictly more evidence than confirm) as a rubric-design root cause.
- **Variant C (`/sc:troubleshoot`-grounded)** raises an empirical question prior to A's and B's diagnoses: **did the confidence-calibrator's per-card pass actually run for H3?** No `tier2-h3-calibration.md` artifact appears to exist; if the calibration step never produced output, the 0.95 is the agent's self-reported number propagated into audit.log and REPORT.md with the central anti-anchoring control bypassed.

The dominant failure pattern across the three lenses is the same: H3's evidence type (static source-read across four upstream GitHub files at v0.44.2) is mismatched to its claim type (runtime CLI-dispatch behavior), and neither the rubric, the calibrator design, nor the orchestration pipeline has machinery that detects or penalizes that mismatch.

Five theories follow, restructured from the original nine (3×3) into a canonical set with redundancy collapsed:

- **T1** — Evidence-class adequacy (merges A1/B1/C2)
- **T2** — Refute vs confirm asymmetry (merges A2/B2)
- **T3** — Calibrator anti-anchoring deficit (merges A3/B3)
- **T4** — Calibrator non-execution (C1, preserved as load-bearing open question)
- **T5** — Agent-task domain mismatch (C3)

---

## Theory T1: Evidence-class is not scored against claim-class — rubric, proposition, and OR-disjunction all collapse onto the same gap

<!-- Source: Merged from Variant 1 (A1), Variant 2 (B1), Variant 3 (C2) per refactor-plan Change #2 -->

**Claim.** The H3 card scored ≥0.9 on Evidence-grounding because the escalation rubric's 1.0 anchor treats source-citation and runtime-reproduction as *interchangeable* — the operative rubric clause is `"Cited file:line matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom"` (`/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:13`). The disjunction means a source-only chain can earn 1.0 without any runtime trace. Compounding this rubric-language failure, the four-file evidence chain (E1 CLI struct, E2 dispatcher, E3 `start_client`, E4 options-merge) proves a *different proposition* than the one the verdict requires: it proves that `--session NAME options …` parses to a session-creating dispatch (a CLI-shape claim), not that the failure-mode the test was hitting was not produced by that dispatch (a runtime/registration claim). The rubric has no dimension that asks whether the evidence type is appropriate to the claim type, so the calibrator — even a faithful one — cannot push back.

**Method-derived evidence (B1, via `/sc:reflect`).** `think_about_collected_information` surfaces the mismatch between the card's claim ("session IS created") and the symptom it was supposed to discharge ("session never registers in `list-sessions`"). Creation and registration are different events in zellij's lifecycle (`SessionInfo` registration happens after layout selection and plugin load, per Branch-A's reading of `zellij-server/src/lib.rs`). H3 never bridges that gap.

**Method-derived evidence (C2, via `/sc:troubleshoot`).** Re-applying the rubric mechanically (per `confidence-calibrator.md:48-55`) against a rubric that does not encode an evidence-class/claim-class alignment dimension produces inflated scores by construction; the failure is not in calibrator discipline but in the rubric's missing dimension.

**Artifact evidence.**
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:13` — the OR-disjunction (A1, B1, C2 all cite this line).
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:21-66` — E1–E5 are entirely source-reads (E5 is an anecdotal DEV.to article); zero `bash` runs, zero `zellij list-sessions` traces.
- `tier2-h3-options-subcommand.md:51` — E3 concludes "INITIATES CREATION OF A NEW SESSION" but stops before registration.
- `tier2-h3-options-subcommand.md:102-107` — the card explicitly admits `start_client_impl` body was not retrieved; the jump from "dispatcher calls `start_client`" to "session registers" is therefore not source-grounded.
- `tier1-observation.md:5-12` — the symptom is "did not register within 15s" (a `list-sessions` poll), not "creation rejected." The card answers a question one step upstream of the symptom.
- `wave1_5-branch-A.md:80-82` — Branch A itself flagged Q5 (whether `options` starts a session or sets options) as "partial / uncertain… empirical test required." H3 collapsed that uncertainty using the same evidence class Branch A had declared insufficient.

**Per-theory confidence:** 0.85 (3-way convergence across A1/B1/C2 with overlapping but non-identical evidence; the highest-confidence theory in the merged set).

**Systemic fix.** Add a 6th rubric dimension, **Evidence-class adequacy**, that caps Evidence-grounding at 0.5 when the claim is a runtime-behavior claim and no runtime trace, CI reproduction, or local-execution log is cited. Equivalently (A1's framing): split Evidence-grounding into two sub-dimensions — provenance (citation exists) and class-adequacy (citation type matches the claim's epistemic demand) — so source-only refutations of "does X happen at runtime" claims top out at 0.5 by construction.

---

## Theory T2: Rubric and calibrator are symmetric across verdict direction, but refutation requires strictly more evidence than confirmation

<!-- Source: Merged from Variant 1 (A2) and Variant 2 (B2) per refactor-plan Change #3 -->

**Claim.** Confirming a hypothesis ("X causes Y") requires showing a plausible mechanism; refuting one ("X cannot cause Y") requires ruling out *every* mechanism by which X might cause Y — a strictly larger evidentiary burden. The escalation rubric and the confidence-calibrator agent spec treat both verdict directions symmetrically: same five dimensions, same 1.0/0.5/0.0 anchors, same averaging. Worse, the rubric anchors are framed around *positive* cause-and-fix claims, which means refutation cards score gimmes on most dimensions:

- **Symptom Coverage 1.0** is trivially attainable for a refutation — we are not trying to cover symptoms, we are dismissing a mechanism.
- **Fix Directness 1.0** is trivially attainable when the proposed fix is null ("the current invocation is structurally correct"). The rubric has no anchor for "this card proposes no fix."
- **Domain Coherence 1.0** holds by construction for a single-mechanism refutation (single domain = CLI parsing).

With four of five dimensions effectively gimme, the arithmetic mean is dominated by Evidence-grounding and Reproducibility-fit alone — and Theory T1 already explains how those two scored 1.0 on source-only evidence. A 0.95 REFUTE on a source-only investigation is treated as equally well-grounded as a 0.95 CONFIRM, even though refutation requires the agent to have *also* read every code path it did not read.

**Method-derived evidence (B2, via `/sc:reflect`).** `think_about_task_adherence` checks whether the *approach* matches the *goal*. H3's goal was "rule out the structural-bug hypothesis"; its approach was "read four files and find no obvious refutation in them." Adherence is low: the goal demanded exhaustive search, the approach was bounded sampling. The rubric does not encode this asymmetry, so the calibrator could not penalize it.

**Artifact evidence.**
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-19` — every anchor in the 1.0 column is framed around a positive cause-and-fix: "Proposed cause explains 100% of the reported symptoms", "Proposed fix touches the exact code identified in evidence", "Single domain (e.g. pure logic bug)". No anchors define what those mean for refutation cards.
- `/config/.claude/agents/confidence-calibrator.md:48-55` — "Score each dimension 0.0/0.5/1.0 per the rubric's anchor language" — purely mechanical against a symmetric rubric.
- `tier2-h3-options-subcommand.md:83-89` — "Because the hypothesis is refuted, NEITHER Option A NOR Option B is required to fix the structural shape." A null fix maps to 1.0 on Fix Directness because the rubric has no anchor for "this card proposes no fix."
- `tier2-h3-options-subcommand.md:93` — confidence rationale: "four primary-source evidence chains… converge on the same conclusion from independent files in the same v0.44.2 tag" — four *positive* observations (no early-return seen) used to ground a *negative* claim (no early-return exists anywhere). The asymmetry, displayed plainly.
- `tier2-h3-options-subcommand.md:102` — risk §6 admits "If `start_client_impl` has a guard that early-returns when `command == Some(Command::Options(_))`, the refutation would weaken" — one unread file flips the verdict; for a CONFIRM, one unread file would not.
- `REPORT.md:158-169` — both H2 (0.85 REFUTE) and H3 (0.95 REFUTE) carry high refute confidences despite both being source-only; H1 (the empirically correct CONFIRM) carries 0.82. The inversion is consistent with the asymmetry being invisible to the rubric.

**Per-theory confidence:** 0.75 (B's "strictly larger evidentiary burden" framing + A's gimme-dimension decomposition together produce a more complete diagnosis than either standalone; conditional on T4 = false, since if the calibrator did not run the symmetry of the rubric is moot for this incident).

**Systemic fix.** Combined fix — (i) cap Evidence-grounding at 0.5 for REFUTE verdicts unless the card includes an empirical/runtime negative result (B2's fix); (ii) require REFUTE cards to also demonstrate a positive alternative explanation that survives the same scrutiny (A2's fix). Each is a sufficient condition for a refutation card to clear 0.85; both are required to clear 0.95.

---

## Theory T3: Calibrator's anti-anchoring discipline is exhortation, not procedure — the card's narrative captures the calibrator even when the formation trail is stripped

<!-- Source: Merged from Variant 1 (A3) and Variant 2 (B3) per refactor-plan Change #4 -->

**Claim.** The calibrator agent spec (`/config/.claude/agents/confidence-calibrator.md:21`) names the anchor it is supposed to defeat: "the upstream investigative trail is not [shown] — that is where the dominant anchoring bias lives." But the dominant anchor for a REFUTE card is not the investigative trail; it is the **card's confident narrative** ("CONFIRMED 0.95… four primary-source evidence chains converge"). Stripping the trail leaves the narrative fully intact — and in fact *more* persuasive (no trail to introduce doubt). The calibrator spec acknowledges the residual-anchor risk (`confidence-calibrator.md:34-36`: "Anchoring bias is reduced, not eliminated… Your defense against the residual anchor is mechanical discipline") but the only "mechanical" steps that follow are "score one dimension at a time" (which a fluent narrative satisfies trivially) and "spot-check citations" (H3's citations all match — the bug is what the citations do not show). Instructions do not survive a well-written REFUTE. Worse, the calibrator design predicted exactly this failure mode and shipped without enforcement:

> **Placebo risk:** if the calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead.
> — `/config/.claude/agents/confidence-calibrator.md:117-118`

The 0.95 → 0.95 pass-through on H3 is that placebo risk made manifest.

**Method-derived evidence (B3, via `/sc:reflect`).** `think_about_whether_you_are_done` against the calibration step surfaces an incompleteness: the calibrator is told *what not to do* (don't inherit the narrative framing) but not given a *counter-procedure* (e.g., "draft a hypothetical CONFIRM card from the same evidence and check which is better supported"). Without the counter-procedure, the calibrator's defense is willpower against a well-crafted card — a defense that does not generalize.

**Artifact evidence.**
- `/config/.claude/agents/confidence-calibrator.md:21` — locates the bias in the wrong place (investigative trail) for REFUTE cards (where the bias lives in the narrative).
- `/config/.claude/agents/confidence-calibrator.md:25-27` — Independence Instruction is exhortatory ("treat as signal, not number") with no mechanical step.
- `/config/.claude/agents/confidence-calibrator.md:34-36` — "Your defense against the residual anchor is mechanical discipline" — the only "mechanical" follow-through is dimension-wise scoring and citation spot-checks, neither of which catches what T1 surfaces.
- `/config/.claude/agents/confidence-calibrator.md:117-118` — placebo-risk language; the design predicted the failure mode.
- `tier2-h3-options-subcommand.md:3` — the card's opening verdict is written as settled fact ("**Verdict: REFUTED.**") with bolded emphasis — exactly the narrative shape the calibrator has no procedural defense against.
- `tier2-h3-options-subcommand.md:43,47,51,63,81` — the card cites Branch A's prior verdicts, doc-context-card framing, and the H1/H2 welcome-layout finding as supporting evidence for *itself*. The narrative pulls the upstream investigation into its own frame.
- `tier2-h3-options-subcommand.md:92-93` — "The four primary-source evidence chains… converge on the same conclusion from independent files" — the convergence claim is itself anchoring framing baked into the card.
- `/config/.claude/skills/confidence-check/SKILL.md:114-120` — the production `confidence-check` skill's thresholds (≥0.90 to proceed, <0.70 to stop) are calibrated for CONFIRM-style implementation decisions; the troubleshoot rubric reuses the same numeric scale for REFUTE verdicts without re-calibration. The 0.95 in H3 borrows authority from a scale that was never validated against refutation.

**Per-theory confidence:** 0.60 (theory is well-supported on its merits, but is *conditional on T4 = false*: if the calibrator never ran for H3, then critiquing its anti-anchoring procedure is reasoning about a counterfactual).

**Systemic fix.** Combined fix — (i) for any REFUTE verdict ≥ 0.85, the calibrator must draft a one-paragraph steel-manned CONFIRM from the *same* evidence and downgrade the REFUTE confidence by the strength of the steel-man (B3); (ii) the calibrator must be required to construct ONE counter-hypothesis from the card's evidence alone before scoring — if it cannot, the card's narrative has captured the calibrator and Evidence-grounding is capped at 0.5 (A3). Both fixes turn willpower into procedure.

---

## Theory T4: The calibrator step (Wave 3 step 3.5) may not have executed for H3 — the 0.95 may be the agent's self-reported number, never re-graded

<!-- Source: Base (C1) — promoted to standalone Theory T4 per refactor-plan Change #5 -->
<!-- Verification required: see "Recommended verification steps" -->

**Claim.** The 0.95 number may never have been independently re-graded. The Wave 3 step 3.5 contract in `sc-troubleshoot-protocol` (step "Calibrate each card independently — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card)") promises a per-card calibration report at `<output-dir>/tier2-<agent-name>-calibration.md`. The output directory under inspection appears to contain hypothesis cards (`tier2-h1-*.md`, `tier2-h2-*.md`, `tier2-h3-*.md`) but **no** `tier2-*-calibration.md` files. If true, the 0.95 propagated from the agent's self-reported `## 4. Confidence` section straight into audit.log and REPORT.md, with no anchoring-resistant pass between them. The protocol's central anti-anchoring control — calibrator-with-stripped-formation-context — was bypassed.

**Method-derived evidence (C1, via `/sc:troubleshoot`).** Audit-log inspection (the entry for H3 at audit.log:18-22) records "REFUTED 0.95" without any per-card calibration pointer; no `calibration: inline-fallback` marker either (which the Wave 1.7 step 2 fallback rule would emit if the calibrator failed and the protocol fell back to inline self-grading). The number is structurally indistinguishable from a pass-through.

**Artifact evidence.**
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/audit.log:18-22` — H1/H2/H3 verdicts and confidence numbers listed; no per-card calibration pointer; no `calibration: inline-fallback` note.
- `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 step 3.5 — defines `output_path=<output-dir>/tier2-<agent-name>-calibration.md`. The file path pattern is reportedly absent.
- `tier2-h3-options-subcommand.md:92-93` — the agent's self-reported "**95%** that H3 is refuted." This number matches audit.log:22 and REPORT.md:166 exactly — strongly suggestive of pass-through.
- `/config/.claude/agents/confidence-calibrator.md:24-26` — "Self-reported confidence on the card is a signal, not a number" — the calibrator is the layer that's supposed to prevent self-reported-confidence-as-score; if it didn't run, the protection did not apply.

**Per-theory confidence:** 0.65 (C raises the empirical question, which is high-leverage; but C's evidence for "did not run" is itself thin — C asserts the file pattern is absent but the merged artifact does not yet include a verifying directory listing. This is ironically a source-only refutation of the same shape T1 critiques, and so its own confidence must be capped pending the verification step below).

**Systemic fix.** Make Wave 3 step 3.5 fail-loud if no `tier2-*-calibration.md` is written within a timeout, instead of silently letting the agent's self-reported confidence become the recorded number. Audit-log writes for any Tier-2 card must include an explicit `calibration: <path>` or `calibration: inline-fallback` token; an audit-log line for a Tier-2 verdict without one of those tokens is itself a protocol bug.

---

## Theory T5: Agent-task domain mismatch — the agent that produced H3 does not declare a focus area that includes runtime CLI dispatch

<!-- Source: Base (C3) per refactor-plan Change #6 — hedged for authorship attribution -->

**Claim.** The protocol's Wave 3 agent-selection table assigns specialist agents based on `--type` (test|bug|build|performance|security|deployment). For `--type test`, the table picks `quality-engineer, root-cause-analyst, refactoring-expert (if test is brittle by structure)`. H3's claim — a CLI-dispatch / `start_client` runtime question — is not a refactoring question. It is a runtime-tracing / systems-debugging question. The refactoring-expert agent (per its own .md spec) focuses on code-quality, SOLID, complexity metrics, and pattern application — none of which equips it to runtime-verify a `Command::Options` dispatcher claim. If the refactoring-expert was the agent that produced H3, the 0.95 confidence is what an agent produces when asked to adjudicate outside its declared focus area: it does the best static-analysis pass it can and rates the static-pass result highly because the static pass succeeded — but the *claim type* required a runtime pass it was not equipped to run.

**Hedge:** `audit.log:18` names three agents (root-cause-analyst, quality-engineer, refactoring-expert) for Wave 3 but does not pin which agent produced which Tier 2 card. The theory is strongest if refactoring-expert authored H3 specifically; it weakens if H3 was authored by root-cause-analyst or quality-engineer (whose declared focus areas are closer to runtime/systems work).

**Artifact evidence.**
- `/config/.claude/agents/refactoring-expert.md:22-27` — focus areas: "Code Simplification, Technical Debt Reduction, Pattern Application, Quality Metrics, Safe Transformation". None are runtime / PTY / CLI-dispatch domains.
- `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 agent-selection table — `test` type maps to `quality-engineer, root-cause-analyst, refactoring-expert (if test is brittle by structure)`. T4 is a contract test whose failure is a *zellij runtime behavior*, not a brittleness-by-structure problem; the "if" condition was satisfied imprecisely.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/audit.log:18` — names the three agents spawned; refactoring-expert was one of them.
- `tier2-h3-options-subcommand.md:21-79` — the entire Evidence section is a static source-read across four upstream files plus an anecdote (E5 from a DEV.to article). No `bash` runs, no `zellij list-sessions` traces. The work product is consistent with a code-reading specialist applied to a runtime question.

**Per-theory confidence:** 0.55 (theory is plausible but presumes a refactoring-expert authorship link that audit.log does not establish; even if a different agent authored H3, the broader "static-only evidence on a runtime claim" critique survives via T1).

**Systemic fix.** Add a Wave 3 step 1.5 that re-routes claims with runtime-only evidence requirements (CLI dispatch, PTY, syscall, network) to a `systems-engineer` / `devops-architect` slot regardless of `--type`. Explicitly forbid closing a runtime claim at >0.85 confidence on static-only evidence, regardless of which agent produced the card.

---

## Cross-cutting structural finding — citations to external URLs are not Read-spot-checkable

<!-- Source: Base (C, sub-finding from the run-summary) — incorporated as a standalone observation per Step 1 unique contribution U-003 -->

The H3 card's E1–E4 evidence cites upstream GitHub URLs (`github.com/zellij-org/zellij`, tag `v0.44.2`). The confidence-calibrator's spot-check procedure (`confidence-calibrator.md:50-52`) Reads cited `file:line` — but the Read tool cannot fetch GitHub URLs. The cited evidence is therefore structurally un-spot-checkable by the calibrator. Even a perfectly disciplined calibrator following the spec verbatim would have to either fail open (accept the citation without verification) or fail loud (refuse to score). The current behavior appears to be the former.

This finding is **orthogonal** to T1–T5 — it would still hold even if the rubric, the calibrator procedure, the calibration step, and the agent-domain selection were all corrected. It is a tooling-affordance gap rather than a methodological one. Mitigation: either (i) the protocol should require all cited evidence to be resolvable from the local repo (e.g., vendored snapshots or git-submodule of upstream sources at the tested tag), or (ii) the calibrator should be given a `WebFetch`-backed spot-check path with explicit confidence penalty when WebFetch is unavailable.

---

## Shared assumptions (UNSTATED preconditions)

<!-- Source: Synthesized per refactor-plan Change #7 from diff-analysis A-001/A-002/A-003 (sc:adversarial-protocol AD-2 mandates surfacing UNSTATED preconditions) -->

| ID | Assumption | Impact if violated | Status |
|----|------------|---------------------|--------|
| A-001 | The recorded 0.95 is the *artifact under investigation* — i.e., the verdict that was downstream-relied-upon. | If the 0.95 is itself an aggregation artifact (e.g., agent-self-report propagated without calibration), then T1/T2/T3 are critiques of a layer that never affected this score, and T4 wins by elimination. | UNSTATED — confirmed by all three variants implicitly; partially resolved by T4 verification step. |
| A-002 | The rubric quoted by all three variants (`sc-troubleshoot-protocol/refs/escalation-rubric.md`) is the rubric that scored H3. | If a different (or no) rubric was used, the entire critique of rubric anchors is misdirected. | UNSTATED — likely correct, but worth verifying by inspecting audit.log for a rubric-version pin. |
| A-003 | The confidence-calibrator agent spec at `/config/.claude/agents/confidence-calibrator.md` is the spec that governed (or would have governed) H3's calibration step. | If the calibrator was never instantiated (T4), critiquing its design (T3) is reasoning about a counterfactual. | UNSTATED — *partially undermined by T4*. Merged document holds both possibilities. |

---

## Per-theory confidence summary (calibrated)

<!-- Source: Synthesized per refactor-plan Change #8 — confidences adjusted for X-001 unresolved contradiction -->

| Theory | Confidence | Conditional on |
|--------|-----------|----------------|
| T1 — Evidence-class adequacy | **0.85** | Independent of T4. 3-way convergence. Strongest theory. |
| T2 — Refute vs confirm asymmetry | **0.75** | Conditional on T4 = false (if calibrator did not run, rubric symmetry is moot for *this* incident, though the underlying flaw remains a protocol bug). |
| T3 — Calibrator anti-anchoring deficit | **0.60** | Conditional on T4 = false. If T4 = true, T3 is theory of a counterfactual. |
| T4 — Calibrator non-execution | **0.65** | Empirical claim; high-leverage but evidence is asserted-absence, not exhibited-absence. Requires verification. |
| T5 — Agent-task domain mismatch | **0.55** | Conditional on refactoring-expert authoring H3 specifically; weakens if H3 was authored by root-cause-analyst or quality-engineer. |

**Overall most-likely root-cause posture:** T1 is the strongest theory unconditionally and explains the failure mechanism regardless of T4's resolution. T4, if verified, dominates T3 (and partially moots T2 for this incident); the verification step below resolves the load-bearing ambiguity. The expected-utility-maximizing next action is the directory-listing check (verification step #1) — it is cheap and discharges the contradiction.

---

## Recommended verification steps

<!-- Source: Synthesized per refactor-plan Change #9 — empirical steps the variants did not run -->

1. **Verify T4 (and resolve X-001):** Run `ls /config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/ | grep -i calibration`. Presence of `tier2-h3-*-calibration.md` falsifies T4 and re-activates T2/T3 at higher confidence. Absence confirms T4 and de-prioritizes T3.
2. **Verify A-001 (whether 0.95 is a pass-through):** Re-read `audit.log` for per-card calibration pointers or `calibration: inline-fallback` markers. Absence of either token next to the H3 line is itself evidence of pass-through.
3. **Verify T5:** Trace which agent in the H3 spawn pool produced H3 (audit.log or agent invocation logs). If refactoring-expert, T5 holds at 0.55. If root-cause-analyst or quality-engineer, T5 weakens to ~0.30 but the broader "static evidence for a runtime claim" critique survives via T1.
4. **Falsifiability check on T1 itself (`/sc:adversarial-protocol` AD-1 Round 2.5 echo, manual):** Construct one downstream condition that, if true, would make `--session NAME options …` fail to register a session despite the dispatcher's `start_client` call. The card's own §6 names exactly such a condition (a guard in `start_client_impl` early-returning when `command == Some(Command::Options(_))`). Verify by reading `start_client_impl` at v0.44.2. If the guard exists, H3's REFUTE is materially weakened *empirically* — independent of the rubric/calibrator/orchestration critiques.

---

## Notes on the merge process

<!-- Source: Merge-executor note -->

- Base variant selected: Variant 3 (agent-C) by 1.3% margin over Variant 2 (B), resolved by Level 1 tiebreaker (debate performance) per `base-selection.md`.
- Five theories preserved (originally nine across three variants) with redundancy collapsed: T1 = merge(A1, B1, C2); T2 = merge(A2, B2); T3 = merge(A3, B3); T4 = preserve(C1); T5 = preserve(C3, hedged).
- One unresolved contradiction (X-001: did the calibrator run?) preserved as a load-bearing open question rather than force-resolved, per `--depth quick` non-convergence policy.
- Three UNSTATED shared assumptions surfaced and labeled per AD-2.
- Convergence: 69% (below 80% threshold); status NOT_CONVERGED at `--depth quick`. Documented in `debate-transcript.md`.
- Post-merge validation passed for structural integrity and internal references; no new contradictions introduced.
