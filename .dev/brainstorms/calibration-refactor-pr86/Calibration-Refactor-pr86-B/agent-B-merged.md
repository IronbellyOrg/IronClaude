<!-- sc:adversarial invocation -->
<!-- Skill name resolved: sc:adversarial (delegated to sc-adversarial-protocol per skill spec) -->
<!-- Skill output original path: inline-returned -->
<!-- Inputs: agent-A-theories.md, agent-B-theories.md, agent-C-theories.md -->
<!-- Depth: quick -->
<!-- Mode: --compare --merge -->

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (agent-C, /sc:troubleshoot-grounded) -->
<!-- Merge date: 2026-05-26 (Merger B) -->
<!-- Convergence: 0.67 (6/9 substantive diff points; below 0.80 threshold, force-selected per FR-006 no_convergence) -->

# Merged theories for the H3 calibration miss (Merger B)

<!-- Source: Merged meta-summary — synthesizes V2 /sc:reflect summary + V3 /sc:troubleshoot run summary + V1 unique findings -->

## Meta-investigation summary

A Wave-3 Tier-2 hypothesis card (`tier2-h3-options-subcommand.md`) issued **REFUTED at 0.95 confidence** for the structural-bug hypothesis on the `zellij --session NAME options ...` CLI shape. Empirical CI later showed the hypothesis was correct — H3's REFUTE was wrong. Three independent investigation lenses (first-principles, /sc:reflect-grounded, /sc:troubleshoot-grounded) converge on a multi-cause failure with one dominant empirical root cause and three structural enablers.

**Convergent root-cause findings across all three lenses:**

- The escalation rubric's "Evidence grounding" 1.0 anchor is **disjunctive** — "cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom" (`refs/escalation-rubric.md:13`). Source-only refutations of runtime claims score 1.0 on the load-bearing dimension. <!-- Source: Variant 1 (A1), Variant 2 (B1), Variant 3 (C2), Section "Claim" — merged per Change #1 -->
- The rubric and calibrator have no asymmetric handling for REFUTE vs CONFIRM verdicts; refutation requires strictly more evidence than confirmation but the rubric treats them identically. <!-- Source: Variant 1 (A2), Variant 2 (B2), Section "Claim" — merged per Change #2 -->
- H3 (0.95 REFUTE) was scored **higher** than empirically-correct H1 (0.82 CONFIRM), despite H1 having strictly more evidence types (source + literal artifact-log strings + T3 corroboration). The inversion is a calibration smell no automated check caught. <!-- Source: Variant 2 (/sc:reflect summary) + Variant 3 (/sc:troubleshoot run summary) — merged per Change #6 -->

**Divergent findings (unresolved at convergence 0.67, depth=quick):**

- V1 and V2 reason as if the confidence-calibrator agent ran and was anchored by the card's confident narrative. V3 makes the **empirically falsifiable** counter-claim that no `tier2-h3-calibration.md` artifact exists on disk — i.e., the calibrator step 3.5 never ran, and the 0.95 is the agent's self-reported number pass-through. These are mutually exclusive operational claims; the merged document treats V3's empirical claim as primary (per Step 3 scoring, V3 won C-003/X-001 at 75% confidence) and V1/V2's "calibrator was duped" as a secondary hypothesis contingent on calibrator-having-run.

## Theory C1 (base, primary): Calibrator-output absence — Wave 3 step 3.5 never ran (or its output was dropped) for H3

<!-- Source: Base (Variant 3, C1) — original; augmented with V1.A3 placebo-risk citation per Change #3 -->

**Claim:** The 0.95 number was never independently re-graded. The Wave 3 step 3.5 contract (sc-troubleshoot-protocol step "Calibrate each card independently — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card)") promises a per-card calibration report at `<output-dir>/tier2-<agent-name>-calibration.md`, but no calibration artifacts exist for H1, H2, or H3 in the output dir. The 0.95 propagated from the agent's self-reported `## 4. Confidence` section straight into audit.log and REPORT.md with no anchoring-resistant pass between them. The protocol's central anti-anchoring control (calibrator-with-stripped-formation-context) was bypassed. **Note (V1.A3 corroboration):** the calibrator design doc itself names this exact failure mode at `confidence-calibrator.md:117-118` ("Placebo risk: if the calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead") but provides no enforcement — the H3 0.95-self → 0.95-recorded pass-through is the placebo failure made manifest, plus the limiting case where calibration step never produced an artifact at all.

**Troubleshoot-derived evidence:** The output directory listing shows hypothesis cards (`tier2-h1-*.md`, `tier2-h2-*.md`, `tier2-h3-*.md`) but NO `tier2-*-calibration.md` files. The audit.log records only "H3 ... REFUTED 0.95" without any calibration-report path, and shows no `calibration: inline-fallback` marker that the fallback path (Wave 1.7 step 2 fallback rule, applied per-card in Wave 3) would emit.

**Artifact evidence:**

- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/audit.log:18-22` — lists H1/H2/H3 verdicts and confidence numbers, but no per-card calibration pointer; no `calibration: inline-fallback` note either way.
- `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 step 3.5 — "Calibrate each card independently — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with `card_tier=2` and `output_path=<output-dir>/tier2-<agent-name>-calibration.md`." This file path pattern is absent for all three cards.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:92-93` — `## 4. Confidence` section reads "**95%** that H3 is refuted." This number, agent-self-reported, is the same number that ended up in audit.log:22 and REPORT.md:166 — strongly suggestive of pass-through.
- `/config/.claude/agents/confidence-calibrator.md:24-26` — "Self-reported confidence on the card is a signal, not a number" — the calibrator is the layer that's supposed to prevent self-reported-confidence-as-score; if it didn't run, the protection didn't apply.
- `/config/.claude/agents/confidence-calibrator.md:117-118` <!-- Source: Variant 1 (A3), Section "Evidence" — merged per Change #3 --> — "Placebo risk: if the calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead" — the design document itself names this failure mode and provides no enforcement.

**Per-theory confidence:** 0.80 (V3 original) + corroboration from V1.A3's placebo-risk citation.

**Systemic fix:** Make Wave 3 step 3.5 fail-loud if no `tier2-*-calibration.md` is written within a timeout, instead of silently letting the agent's self-reported confidence become the recorded number. **Additionally (V2.B3 procedural counter-anchor)**: when calibration DOES run, require the calibrator to draft a one-paragraph steel-manned CONFIRM card from the same evidence and downgrade the REFUTE confidence by the strength of the steel-man. <!-- Source: Variant 2 (B3) systemic fix — merged per Change #5 -->

## Theory C2 (base, augmented): Claim-type vs evidence-type mismatch is not a rubric dimension — and the rubric's "Evidence grounding" 1.0 anchor is disjunctive

<!-- Source: Base (Variant 3, C2) — original; rubric-anchor framing augmented with V1.A1 per Change #1 -->

**Claim:** H3's claim is a *runtime-behavior* claim ("the CLI invocation DOES create a session at runtime"). The evidence chain is *entirely static source-read* across four files in an external repo, with zero runtime traces, zero CI reproductions, and one weak third-party usage anecdote (E5 from a DEV.to article). The escalation rubric's five dimensions (Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence) do not contain a dimension that asks "is the evidence type appropriate to the claim type?" Furthermore (V1.A1 mechanism): the rubric's "Evidence grounding" 1.0 anchor is **disjunctive** — `refs/escalation-rubric.md:13` reads "Cited `file:line` matches a real code path that exhibits the symptom; **OR** diagnostic command output reproduces the symptom" — the OR makes source-citation and runtime-reproduction *interchangeable* at the 1.0 anchor. A card whose entire epistemic basis is "I read the source and inferred dispatch behaviour" can score 1.0 on the load-bearing dimension; combined with high scores on the other four (which are easy to hit when the hypothesis is structurally simple), the arithmetic mean lands at 0.95. <!-- Source: Variant 1 (A1), Section "Claim" — merged per Change #1 -->

**V2.B1 proposition-substitution mechanism (incorporated):** <!-- Source: Variant 2 (B1), Section "Claim" — merged per Change #4, promoted to top-level mechanism -->
The H3 card's four evidence chains (E1 CLI struct, E2 dispatcher, E3 `start_client`, E4 options-merge) jointly prove that `--session NAME options ...` *parses to* a session-creating dispatch. They do **not** prove that the failure-mode the test is hitting was not produced by that dispatch. Creation and registration are different events in zellij's lifecycle: `SessionInfo` registration happens **after** layout selection and plugin load (per Branch-A's reading of `zellij-server/src/lib.rs`). The H3 card never bridges the gap. The rubric's "Evidence grounding 1.0" anchor requires citations to "a real code path that exhibits the symptom" — H3's citations exhibit only the absence of an early-return, not the absence of the symptom (which is a registration failure, not a creation failure). The 0.95 REFUTE silently substituted a weaker, easier-to-defend proposition for the one the investigation actually needed answered.

**Troubleshoot-derived evidence:** The rubric scoring an entirely source-read refutation of a runtime claim at high confidence is mechanically valid under rubric.md:11-19. The card itself acknowledges the mismatch at lines 102-107 ("the conclusion relies on the public-API contract of `ClientInfo::New`. If `start_client_impl` has a guard that early-returns when `command == Some(Command::Options(...))`, the refutation would weaken") but this self-acknowledged structural risk has no rubric dimension that would penalize it.

**Reflect-derived evidence (V2.B1):** `think_about_collected_information` surfaces a mismatch between the card's claim ("session IS created") and the symptom it was supposed to discharge ("session never registers in `list-sessions`"). The H3 card never bridges the gap.

**Artifact evidence:**

- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:13` — "Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom" — the OR makes source-citation and runtime-reproduction equivalent at the 1.0 anchor. <!-- Source: Variant 1 (A1) evidence citation -->
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-17` — table of five dimensions; no dimension scores claim-type/evidence-type alignment. "Evidence grounding" rewards file:line citations regardless of whether the symptom is static or runtime.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:51` — E3 concludes "INITIATES CREATION OF A NEW SESSION" but stops before registration; the symptom is a registration failure, not a creation failure. <!-- Source: Variant 2 (B1) evidence citation -->
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:102-107` — `## 6. Risks of acting on this card` and section 7 ("If I'm wrong it's probably because...") explicitly call out the source-only-against-runtime-claim gap.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier1-observation.md:5-12` — symptom is "did not register within 15s" (a `list-sessions` poll), not "creation rejected". <!-- Source: Variant 2 (B1) evidence citation -->
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/wave1_5-branch-A.md:80-82,233-235` — Branch A itself flagged "Question 5" as "uncertain — empirical test required" for this exact `options`-subcommand question.

**Per-theory confidence:** 0.82 (V3 original 0.78 lifted by V1.A1 + V2.B1 incorporation).

**Systemic fix:** Add a 6th rubric dimension "Evidence-claim alignment" that caps Evidence-grounding at 0.5 when the claim is a runtime-behavior claim and no runtime trace, CI reproduction, or local-execution log is cited. Split "Evidence grounding" into two sub-dimensions — provenance (citation exists) and class-adequacy (citation type matches the claim's epistemic demand) — so source-only refutations of "does X happen at runtime" claims top out at 0.5. <!-- Source: V1 (A1) systemic fix + V3 (C2) systemic fix — merged per Change #1 -->

## Theory M1 (incorporated from V1.A2 + V2.B2): Refute-asymmetry — the rubric and calibrator treat REFUTE and CONFIRM symmetrically when refutation requires strictly more evidence

<!-- Source: Variant 1 (A2) + Variant 2 (B2), full theory — merged per Change #2, promoted to top-level -->

**Claim:** Confirming a hypothesis ("X causes Y") requires showing a plausible mechanism; refuting one ("X cannot cause Y") requires ruling out *every* mechanism by which X might cause Y — a strictly larger evidentiary burden. The rubric (`escalation-rubric.md`) treats both verdict directions symmetrically: the same 5 dimensions, same 1.0/0.5/0.0 anchors, same averaging. The confidence-calibrator agent spec (`confidence-calibrator.md`) inherits this symmetry. A 0.95 REFUTE on a source-only investigation is treated as equally well-grounded as a 0.95 CONFIRM, even though refutation requires the agent to have *also* read every code path it didn't read.

**Per-dimension breakdown of why a REFUTE card trivially maxes most dimensions (V1.A2 mechanism):** The rubric was designed to grade affirmative hypothesis cards (here is the cause; here is the fix). Its five dimensions all presuppose a positive claim with a fix attached. For H3's REFUTE:

- "Symptom coverage" is trivially 1.0 — we are not trying to cover symptoms, we are dismissing a mechanism.
- "Fix directness" is trivially 1.0 — the proposed fix is null / do nothing (`tier2-h3-options-subcommand.md:83-89` "NEITHER Option A NOR Option B is required to fix the structural shape"). A null fix maps to 1.0 because the rubric has no anchor for "this card proposes no fix."
- "Domain coherence" stays 1.0 — single domain by construction.

The arithmetic mean is then dominated by Evidence grounding and Reproducibility fit alone, which the card scores high (per Theory C2's mechanism), and four-of-five dimensions are essentially gimmes.

**Reflect-derived evidence (V2.B2):** `think_about_task_adherence` checks whether the *approach* matches the *goal*. H3's goal was "rule out the structural-bug hypothesis"; its approach was "read four files and find no obvious refutation in them." Adherence is low: the goal demanded exhaustive search, the approach was bounded sampling.

**Artifact evidence:**

- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-19` — the dimension table makes no distinction between confirm/refute claims; "Evidence grounding 1.0" is defined identically for both. Every anchor in the 1.0 column is framed around a positive cause-and-fix.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:83-89` — "Because the hypothesis is refuted, NEITHER Option A NOR Option B is required to fix the structural shape. The current invocation is structurally correct." Null fix → 1.0 on Fix directness.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:93` — confidence rationale: "four primary-source evidence chains... converge on the same conclusion from independent files in the same v0.44.2 tag" — four *positive* observations (no early-return seen) used to ground a *negative* claim (no early-return exists anywhere). The asymmetry displayed plainly.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:102` — risk §6 admits "If `start_client_impl` has a guard that early-returns when `command == Some(Command::Options(_))`, the refutation would weaken" — i.e., one unread file flips the verdict; for a CONFIRM, one unread file would not.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/REPORT.md:155-169` — REPORT.md cites H3 as "REFUTED at 0.95 confidence" with no caveat about refutation-vs-confirmation asymmetry.
- `/config/.claude/agents/confidence-calibrator.md:48-55` — Responsibilities §4: "Score each dimension 0.0/0.5/1.0 per the rubric's anchor language" — purely mechanical against a symmetric rubric.

**Per-theory confidence:** 0.72 (V2.B2 original) + V1.A2 dimensional-breakdown corroboration.

**Systemic fix:** Add a verdict-aware rubric branch — for REFUTE verdicts, cap Evidence-grounding at 0.5 unless the card includes an empirical/runtime negative result, not just a source-read absence-of-positive. REFUTE cards must demonstrate a positive alternative explanation that survives the same scrutiny — refuting a hypothesis without proposing what IS happening should be a 0.5 ceiling.

## Theory C3 (base, retained): Agent-domain mismatch — refactoring-expert is the wrong agent class for runtime-CLI claims

<!-- Source: Base (Variant 3, C3) — original, unmodified; documented as contributing factor not root cause -->

**Claim:** The protocol's agent-selection table assigns specialist agents based on `--type` (test|bug|build|performance|security|deployment). For `--type test`, the table picks `quality-engineer, root-cause-analyst, refactoring-expert (if test is brittle by structure)`. H3's claim — a CLI-dispatch / `start_client` runtime question — is not a refactoring question. It is a runtime-tracing / systems-debugging question. The refactoring-expert agent (per its own .md spec) focuses on code-quality, SOLID, complexity metrics, and pattern application — none of which equips it to runtime-verify a `Command::Options` dispatcher claim. The 0.95 confidence is what an agent produces when asked to adjudicate outside its declared focus area: it does the best static-analysis pass it can and rates the static-pass result highly because the static pass succeeded — but the *claim type* required a runtime pass it was not equipped to run.

**Troubleshoot-derived evidence:** The audit.log records "3 specialist agents (root-cause-analyst, quality-engineer, refactoring-expert)" for Wave 3. The H3 card's evidence is exclusively source-read across four upstream files (E1-E4) plus an anecdotal third-party article (E5) — a profile consistent with a refactorer's natural strengths and NOT consistent with the runtime claim under investigation.

**Artifact evidence:**

- `/config/.claude/agents/refactoring-expert.md:22-27` — focus areas: "Code Simplification, Technical Debt Reduction, Pattern Application, Quality Metrics, Safe Transformation". None of these are runtime / PTY / CLI-dispatch domains.
- `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 agent-selection table — `test` type maps to `quality-engineer, root-cause-analyst, refactoring-expert (if test is brittle by structure)`. T4 is a contract test whose failure is a *zellij runtime behavior*, not a brittleness-by-structure problem.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/audit.log:18` — names the 3 agents spawned; refactoring-expert was one of them.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:21-79` — the entire Evidence section is a static source-read across 4 files plus an anecdote. No `bash` runs, no `zellij list-sessions` traces, no attempt to reproduce the invocation.

**Per-theory confidence:** 0.62. **Status: contributing factor, not root cause** — explains the shape of the investigation but not the 0.95 in REPORT.md.

**Systemic fix:** Add a Wave 3 step 1.5 that re-routes claims with runtime-only evidence requirements (CLI dispatch, PTY, syscall, network) to a `systems-engineer` / `devops-architect` slot regardless of `--type`, and explicitly forbids closing a runtime claim at >0.85 confidence on static-only evidence.

## Theory M2 (secondary, contingent): Calibrator anti-anchoring is misdesigned — narrative captures the score even when trail is stripped

<!-- Source: Variant 1 (A3) + Variant 2 (B3), full theory — preserved as secondary hypothesis contingent on calibrator-having-run -->

**Status:** This theory is **contingent on the resolution of X-001** (Theory C1). If V3.C1 is correct (calibrator never ran), this theory does not apply to the H3 case — though it still describes a real design vulnerability for cases where the calibrator does run.

**Claim:** The calibrator is designed to defeat self-grading bias by stripping the hypothesis-formation context — the calibrator sees only the finished card and the rubric, not the upstream investigation. But the H3 card's narrative IS the formation context, written down. It cites Branch A by name, quotes Branch A's "partial / uncertain" verdict on Q5, frames itself as "resolving" that uncertainty, and embeds the doc-context-card framing. The calibrator agent spec (`confidence-calibrator.md:21`) names the anchor it is supposed to defeat as "the upstream investigative trail" — but the dominant anchor for a REFUTE card is not the investigative trail; it is the **card's confident narrative** ("CONFIRMED 0.95... four primary-source evidence chains converge"). Stripping the trail leaves the narrative fully intact, in fact *more* persuasive (no trail to introduce doubt). The calibrator spec acknowledges this risk but provides no procedural defense beyond an instruction. Instructions do not survive a well-written REFUTE.

**Additional V3 mechanism (cited evidence is GitHub URLs, unspot-checkable):** The H3 card's "Evidence" section (E1-E5) cites external upstream GitHub URLs (zellij-org/zellij @ v0.44.2), not local files. The confidence-calibrator's spot-check procedure (calibrator.md:50-52) Reads cited `file:line` — but the Read tool cannot fetch GitHub URLs; cited evidence is structurally **un-spot-checkable**. Even a faithful calibrator following the spot-check procedure would be impotent against H3's evidence chain. <!-- Source: Variant 3 (/sc:troubleshoot run summary) — merged as supporting mechanism -->

**Artifact evidence:**

- `/config/.claude/agents/confidence-calibrator.md:21` — "You only see the finished card and the rubric. The card itself is present (you must read it) but the upstream investigative trail is not — that is where the dominant anchoring bias lives." Locates the bias in the wrong place for REFUTE cards.
- `/config/.claude/agents/confidence-calibrator.md:25-27` — Independence Instruction is exhortatory ("treat as signal, not number") with no mechanical step.
- `/config/.claude/agents/confidence-calibrator.md:34-36` — "Your defense against the residual anchor is mechanical discipline" — the only mitigation is willpower against a well-crafted card.
- `/config/.claude/agents/confidence-calibrator.md:50-52` — spot-check procedure Reads cited `file:line` — but the Read tool cannot fetch GitHub URLs.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:3` — the card's opening verdict is written as settled fact ("**Verdict: REFUTED.**") with bolded emphasis — exactly the narrative shape the calibrator has no procedural defense against.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:43,47,51,63,81,92-93` — the card cites Branch A's prior verdicts, doc-context-card framing, and convergence-from-four-files as supporting evidence for ITSELF.
- `/config/.claude/skills/confidence-check/SKILL.md:114-120` — the production `confidence-check` skill thresholds (≥0.90 to proceed, <0.70 to stop) are calibrated for CONFIRM-style implementation decisions; the troubleshoot rubric reuses the same numeric scale for REFUTE verdicts without re-calibration.

**Per-theory confidence:** 0.62 (averaged V1.A3=0.55 and V2.B3=0.68; reduced from 0.70 because contingent on M2 not being subsumed by C1).

**Systemic fix:** (1) Calibrator spec must add a procedural counter-anchor: for any REFUTE verdict ≥ 0.85, the calibrator must draft a one-paragraph steel-manned CONFIRM from the *same* evidence and downgrade the REFUTE confidence by the strength of the steel-man. (2) Calibrator must be required to construct ONE counter-hypothesis from the card's evidence alone before scoring — if it cannot, the card's narrative has captured the calibrator and Evidence grounding is capped at 0.5. (3) Spot-check procedure must reject (or specifically flag) cited evidence that is not Read-tool-accessible — GitHub URLs do not satisfy provenance.

## Shared Assumptions (UNSTATED, surfaced via AD-2)

<!-- Source: Variant 1 + Variant 2 + Variant 3 convergence points — extracted via Shared Assumption Extraction Engine -->

| A-NNN | Assumption | Classification | Status |
|---|---|---|---|
| A-001 | All three theory sets assume the **rubric and calibrator are the right layer** at which to fix the calibration miss. None proposes "remove confidence numbers from REFUTE verdicts entirely" or "require runtime evidence as a hard precondition before any Tier-2 card is allowed to score above 0.85." | UNSTATED | Promoted — flagged for downstream attention |
| A-002 | All three assume confidence numbers ≥0.90 should mean something operationally important (block-on-action, escalate, gate downstream work). None defines what 0.95 was supposed to *cause* downstream in the troubleshoot protocol. | UNSTATED | Promoted — flagged for downstream attention |
| A-003 | All three treat "refutation" and "confirmation" as the relevant verdict axis. None questions whether `tier2-h3-options-subcommand.md` should have been categorized as a refutation card at all — arguably it's an open-ended *negative existential* claim ("no structural bug exists") that the rubric cannot grade because it has no falsifiable closure. | UNSTATED | Promoted — flagged for downstream attention |

## Summary of merge

| Theory | Source | Status | Confidence |
|---|---|---|---|
| C1 — Calibrator-output absence | V3 base + V1.A3 corroboration + V2.B3 fix | Primary root cause | 0.80 |
| C2 — Claim-type/evidence-type mismatch | V3 base + V1.A1 mechanism + V2.B1 proposition-substitution | Primary structural cause | 0.82 |
| M1 — Refute asymmetry | V1.A2 + V2.B2 merged | Structural enabler | 0.72 |
| C3 — Agent-domain mismatch | V3 base | Contributing factor | 0.62 |
| M2 — Calibrator anti-anchoring misdesign | V1.A3 + V2.B3 merged | Secondary, contingent on C1 | 0.62 |

**Convergence at depth=quick:** 0.67 (6/9 substantive diff points reached majority agreement in Round 1). Below the 0.80 threshold; no Round 2 or Round 3 per depth=quick. Force-selected V3 as base per FR-006 no_convergence behavior (combined score 0.968, tiebreaker L1 won by V3 with 4 diff points to V2's 3).

**Unresolved conflicts (1):**

- **X-001 (calibrator-ran-but-was-duped vs. calibrator-never-ran):** V3's C1 is empirically falsifiable by checking the filesystem for `tier2-*-calibration.md` artifacts. Merged document treats V3's claim as primary and V1/V2's as secondary (Theory M2). **Resolution recommendation:** before acting on any systemic fix, verify on disk whether calibration artifacts exist; if absent, C1 dominates and M2 becomes prophylactic; if present, M2 becomes primary and C1 collapses into "calibrator ran but produced a number too close to self-report — placebo failure."

<!-- merge-log: 6 changes applied (Change #1: rubric-anchor framing from V1.A1 incorporated into C2; Change #2: V1.A2 + V2.B2 promoted to standalone Theory M1; Change #3: V1.A3 placebo-risk citation added to C1 evidence; Change #4: V2.B1 proposition-substitution incorporated into C2; Change #5: V2.B3 procedural counter-anchor added to C1 systemic fix; Change #6: V2 + V3 meta-summary observation about H3 > H1 score inversion added to top of merged doc). 0 changes failed. Structural integrity: PASS (heading hierarchy consistent, no orphaned subsections). Internal references: 0 broken. New contradictions introduced: 0. -->

<!-- Return contract:
  merged_output_path: /config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/calibration-failure/agent-B-merged.md
  convergence_score: 0.67
  artifacts_dir: inline (artifacts assembled inline in merged document per Merger B isolation constraint)
  status: partial (convergence below 0.80 threshold; force-selected base per FR-006 no_convergence; 1 unresolved conflict X-001)
  base_variant: agent-C (Variant 3, /sc:troubleshoot-grounded)
  unresolved_conflicts: 1 (X-001: calibrator-ran-but-was-duped vs. calibrator-never-ran)
  fallback_mode: false
  failure_stage: null
  invocation_method: skill-direct
  unaddressed_invariants: [] (Round 2.5 skipped per depth=quick)
-->
