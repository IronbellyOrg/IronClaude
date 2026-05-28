<!-- sc:adversarial invocation -->
<!-- Skill name resolved: sc-adversarial-protocol (via sc:adversarial command file which routes to sc-adversarial-protocol) -->
<!-- Skill output original path: inline-returned -->
<!-- Inputs: agent-A-theories.md, agent-B-theories.md, agent-C-theories.md -->
<!-- Depth: quick -->
<!-- Mode: --compare --merge -->

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (agent-C, /sc:troubleshoot-grounded) -->
<!-- Merge date: 2026-05-26 -->

# Merged Theories — H3 Calibration Miss (Merger C output)

## Pipeline metadata

- **Variants compared:** 3 (agent-A first-principles, agent-B /sc:reflect-grounded, agent-C /sc:troubleshoot-grounded)
- **Selected base:** Agent C — combined score 0.94 (quant 0.97, qual 0.90)
- **Runner-up:** Agent B — combined score 0.88
- **Convergence:** 0.71 (below 0.80 threshold; Round 2/2.5/3 skipped per `--depth quick`)
- **Unresolved diff points:** A-001 (shared assumption that rubric is arithmetic mean — flagged, not falsified)
- **Highest-impact unique finding:** C1 (calibrator-output artifact absence) — falsifies an implicit shared assumption of A and B that the calibrator ran

## Cross-cutting findings (consensus across all three variants)

All three variants independently converge on a **single root pattern**: H3's evidence chain proves a *different proposition* than the rubric scores against, and neither the inline self-grade nor (allegedly) the calibrator detected the substitution. Three distinct mechanisms contribute:

1. **Evidence-class mismatch** (A1 ≈ B1 ≈ C2) — source-read citations used to discharge a runtime-behavior claim
2. **Refute/confirm asymmetry** (A2 ≈ B2) — refuting requires ruling out every mechanism; confirming requires showing one
3. **Anchoring leak via card narrative** (A3 ≈ B3) — stripping the formation trail leaves the persuasive card text intact

C uniquely contributes two additional mechanisms that A and B miss:

4. **Calibrator-output absence** (C1) — the calibrator may not have run at all
5. **Agent-domain mismatch** (C3) — refactoring-expert was assigned to a runtime-CLI claim

<!-- Source: Base (original) — pipeline summary preserved from agent-C -->

---

## Theory M1 (was C1): Calibrator-output absence — Wave 3 step 3.5 never ran (or its output was dropped) for H3

**Claim:** The 0.95 number was never independently re-graded. The Wave 3 step 3.5 contract (sc-troubleshoot-protocol step: spawn N `confidence-calibrator` instances in parallel, each writing `<output-dir>/tier2-<agent-name>-calibration.md`) promises a per-card calibration report, but no calibration artifacts exist for H1, H2, or H3 in the output dir. The 0.95 propagated from the agent's self-reported `## 4. Confidence` section straight into audit.log and REPORT.md with no anchoring-resistant pass between them. The protocol's central anti-anchoring control (calibrator-with-stripped-formation-context) was bypassed.

**Why this is the highest-impact finding:** Agent A's Theory A3 and Agent B's Theory B3 both assume the calibrator ran and then critique its anchoring defense. C1 demonstrates that assumption may be false — making A3 and B3 critiques of a control that may never have fired. The 0.95 → 0.95 pass-through ("placebo failure") that A3 cited as a possible failure mode is in fact a stricter failure: the calibrator did not even attempt the pass.

**Evidence:**
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/audit.log:18-22` — lists H1/H2/H3 verdicts and confidence numbers, but no per-card calibration pointer; no `calibration: inline-fallback` note either way.
- `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 step 3.5 — "Calibrate each card independently — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with `card_tier=2` and `output_path=<output-dir>/tier2-<agent-name>-calibration.md`." This file path pattern is absent for all three cards.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:92-93` — `## 4. Confidence` section reads "**95%** that H3 is refuted." This number, agent-self-reported, is the same number that ended up in audit.log:22 and REPORT.md:166 — strongly suggestive of pass-through.
- `/config/.claude/agents/confidence-calibrator.md:24-26` — "Self-reported confidence on the card is a signal, not a number" — the calibrator is the layer that's supposed to prevent self-reported-confidence-as-score; if it didn't run, the protection didn't apply.

**Per-theory confidence:** 0.82 (raised from C's 0.80 — falsification of A3/B3 implicit assumption strengthens this theory)

**Systemic fix (compound, combining C1 + B3):**
1. Make Wave 3 step 3.5 fail-loud if no `tier2-*-calibration.md` is written within a timeout, instead of silently letting the agent's self-reported confidence become the recorded number.
2. When the calibrator DOES run, for any REFUTE verdict ≥ 0.85, require it to draft a one-paragraph steel-manned CONFIRM from the same evidence and downgrade the REFUTE confidence by the strength of the steel-man.

<!-- Source: Base C, Theory C1 — preserved as M1 -->
<!-- Source: Variant 2 (agent-B), Theory B3 — fix #2 merged per Change #1 -->

---

## Theory M2 (was C2 + B1): Proposition substitution — H3's evidence proves CLI-shape, the rubric scored it as if it proved symptom-absence

**Claim:** H3's claim is a *runtime-behavior* claim ("the CLI invocation DOES create a session at runtime, and therefore the structural-bug hypothesis is refuted"). The four evidence chains (E1 CLI struct, E2 dispatcher, E3 `start_client`, E4 options-merge) jointly prove that `--session NAME options ...` *parses to* a session-creating dispatch — they prove **session creation**, not **session registration**, which is what the failing test measures (`list-sessions` poll). Creation and registration are different events in zellij's lifecycle: `SessionInfo` registration happens after layout selection and plugin load (per Branch-A's reading of `zellij-server/src/lib.rs`). The H3 card never bridges that gap, yet scores 1.0 on Evidence grounding because the rubric's anchor ("`file:line` matches a real code path that exhibits the symptom") accepts adjacent-code-path matching as equivalent to symptom-exhibiting evidence.

The escalation rubric's five dimensions (Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence) do not contain a dimension that asks "is the evidence type appropriate to the claim type?" The Reproducibility-fit dimension is the closest, but its 1.0 anchor permits "deterministic exception with a clear trigger" which a source-read claim about dispatcher logic can technically satisfy.

**Evidence:**
- `tier2-h3-options-subcommand.md:51` — E3 concludes "INITIATES CREATION OF A NEW SESSION" but stops before registration; the symptom is a registration failure, not a creation failure. (from B1)
- `tier2-h3-options-subcommand.md:107` — §7 explicitly admits `start_client_impl` body was not retrieved; the leap from "dispatcher calls start_client" to "session registers" is therefore not source-grounded. (from B1/C2)
- `tier1-observation.md:5-12` — symptom is "did not register within 15s" (a `list-sessions` poll), not "creation rejected". (from B1)
- `wave1_5-branch-A.md:80-82` and `:233-235` — Branch A itself flagged Q5 (`options` subcommand starts a session vs sets options) as "partial / uncertain... empirical test required" — H3 collapsed this uncertainty without empirical work. (from B1 + C2)
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-17` — table of five dimensions; no dimension scores claim-type/evidence-type alignment. The 1.0 anchor on Evidence grounding rewards file:line citations regardless of whether the symptom is static or runtime. (from C2)
- `/config/.claude/agents/confidence-calibrator.md:21` — "Apply the rubric mechanically: one dimension at a time, score with evidence, never inherit the card's self-reported confidence." Mechanical rubric application against a rubric with no claim-type dimension cannot catch a claim-type/evidence-type mismatch; the calibrator is doing what it's told and the rubric is what's incomplete. (from C2)

**Per-theory confidence:** 0.80 (averaging B1's 0.80 and C2's 0.78, raised slightly by mutual reinforcement)

**Systemic fix (compound, combining C2 + A1 + B1):**
1. Add a 6th rubric dimension "Evidence-claim alignment" that caps Evidence-grounding at 0.5 when the claim is a runtime-behavior claim and no runtime trace, CI reproduction, or local-execution log is cited.
2. Split "Evidence grounding" into two sub-dimensions: **provenance** (citation exists and matches) and **class-adequacy** (citation type matches the claim's epistemic demand) — so source-only refutations of "does X happen at runtime" claims top out at 0.5 on the class-adequacy half. (from A1)
3. The calibrator must extract the operative proposition from the card's "Claim" section and reject Evidence-grounding ≥ 0.5 when no cited line exhibits the actual symptom, not just adjacent code paths. (from B1)

<!-- Source: Base C, Theory C2 — claim and rubric-mechanics evidence preserved -->
<!-- Source: Variant 2 (agent-B), Theory B1 — proposition-substitution framing and creation-vs-registration distinction merged per Change #2 -->
<!-- Source: Variant 1 (agent-A), Theory A1 — split-dimension fix merged into systemic-fix list -->

---

## Theory M3 (was C3): Agent-domain mismatch — refactoring-expert is the wrong agent class for runtime-CLI claims

**Claim:** The protocol's agent-selection table assigns specialist agents based on `--type` (test|bug|build|performance|security|deployment). For `--type test`, the table picks `quality-engineer, root-cause-analyst, refactoring-expert (if test is brittle by structure)`. H3's claim — a CLI-dispatch / `start_client` runtime question — is not a refactoring question. It is a runtime-tracing / systems-debugging question. The refactoring-expert agent (per its own .md spec) focuses on code-quality, SOLID, complexity metrics, and pattern application — none of which equips it to runtime-verify a `Command::Options` dispatcher claim. The 0.95 confidence is what an agent produces when asked to adjudicate outside its declared focus area: it does the best static-analysis pass it can and rates the static-pass result highly because the static pass succeeded — but the *claim type* required a runtime pass it was not equipped to run.

**Evidence:**
- `/config/.claude/agents/refactoring-expert.md:22-27` — focus areas: "Code Simplification, Technical Debt Reduction, Pattern Application, Quality Metrics, Safe Transformation". None of these are runtime / PTY / CLI-dispatch domains.
- `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 agent-selection table — `test` type maps to `quality-engineer, root-cause-analyst, refactoring-expert (if test is brittle by structure)`. T4 is a contract test whose failure is a *zellij runtime behavior*, not a brittleness-by-structure problem. The "if" condition was satisfied imprecisely.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/audit.log:18` — names the 3 agents spawned; refactoring-expert was one of them.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:21-79` — the entire Evidence section is a static source-read across 4 files plus an anecdote. No `bash` runs, no `zellij list-sessions` traces, no attempt to reproduce the invocation. This is the work product of a code-reading specialist applied to a runtime question.

**Per-theory confidence:** 0.62

**Systemic fix (one line):** Add a Wave 3 step 1.5 that re-routes claims with runtime-only evidence requirements (CLI dispatch, PTY, syscall, network) to a `systems-engineer` / `devops-architect` slot regardless of `--type`, and explicitly forbids closing a runtime claim at >0.85 confidence on static-only evidence.

<!-- Source: Base C, Theory C3 — preserved unchanged -->

---

## Theory M4 (new, from B2 — incorporated as non-base strength): Refute-asymmetry — the rubric and calibrator have no special handling for refutation claims, which require strictly more evidence than confirmation claims

**Claim:** Confirming a hypothesis ("X causes Y") requires showing a plausible mechanism; refuting one ("X cannot cause Y") requires ruling out *every* mechanism by which X might cause Y — a strictly larger evidentiary burden. The rubric (`escalation-rubric.md`) treats both verdict directions symmetrically: the same 5 dimensions, same 1.0/0.5/0.0 anchors, same averaging. The confidence-calibrator agent spec inherits this symmetry. A 0.95 REFUTE on a source-only investigation is treated as equally well-grounded as a 0.95 CONFIRM, even though refutation requires the agent to have *also* read every code path it didn't read. H3's 0.95 is the predictable failure mode of this symmetric framing.

**Why included despite C base not naming this:** M2 covers evidence-class mismatch; M4 covers the orthogonal asymmetry that even *with* the right evidence class, REFUTE requires more of it than CONFIRM. Both A2 and B2 surface this; B2's framing ("one unread file flips REFUTE; for CONFIRM, one unread file would not") is operationally crisper than A2's.

**Evidence:**
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-19` — the dimension table makes no distinction between confirm/refute claims; "Evidence grounding 1.0" is defined identically for both.
- `/config/.claude/agents/confidence-calibrator.md:48-55` — Responsibilities §4 says "Score each dimension 0.0/0.5/1.0 per the rubric's anchor language" — purely mechanical against a symmetric rubric.
- `tier2-h3-options-subcommand.md:93` — confidence rationale: "four primary-source evidence chains... converge on the same conclusion from independent files in the same v0.44.2 tag" — four *positive* observations (no early-return seen) used to ground a *negative* claim (no early-return exists anywhere). This is the asymmetry, displayed plainly.
- `tier2-h3-options-subcommand.md:102` — risk §6 admits "If `start_client_impl` has a guard that early-returns when `command == Some(Command::Options(_))`, the refutation would weaken" — i.e., one unread file flips the verdict; for a CONFIRM, one unread file would not.
- `REPORT.md:158-169` — both H2 (0.85 refute) and H3 (0.95 refute) carry high refute confidences despite both being source-only; H1 (the empirically correct CONFIRM) carries 0.82. The inversion (refute > confirm despite less empirical grounding) is consistent with the asymmetry being invisible to the rubric.

**Per-theory confidence:** 0.72 (B2's original; A2 at 0.65 was weaker and is subsumed)

**Systemic fix (one line):** Add a rubric branch — for REFUTE verdicts, cap Evidence-grounding at 0.5 unless the card includes an empirical/runtime negative result, not just a source-read absence-of-positive.

<!-- Source: Variant 2 (agent-B), Theory B2 — incorporated as new theory M4 per Change #3 -->
<!-- Source: Variant 1 (agent-A), Theory A2 — subsumed (B2 strictly stronger) — see Changes NOT Being Made -->

---

## Changes NOT being made (transparency on rejected alternatives)

1. **Agent A's Theory A3 not preserved standalone.** A3 ("anchoring-strip is incomplete — narrative leaks formation context back in") is fully subsumed by M1 (C1: calibrator may not have run at all) plus M4's systemic fix #1 from B3 (steel-manned counter-CONFIRM). If the calibrator did not run, A3 critiques a control that never fired; if it did, B3's counter-procedure addresses the same gap A3 names.

2. **Agent A's Theory A2 not preserved standalone.** A2 and B2 cover the same refute/confirm asymmetry. B2's framing ("one unread file flips REFUTE; for CONFIRM, one unread file would not") is operationally crisper and ships with a more actionable fix. A2's contribution is fully captured in M4.

3. **A's "split Evidence grounding into provenance + class-adequacy" fix preserved.** This specific framing from A1 is cleaner than C2's "add a 6th dimension" — both are now listed in M2's systemic-fix block as alternatives.

4. **Shared assumption A-001 (rubric is arithmetic mean) flagged but not falsified here.** All three variants assume the five rubric dimensions are averaged. No variant actually re-derives the formula from `escalation-rubric.md`. This is an UNSTATED precondition surfaced by Step 1's shared-assumption extraction. **Recommended follow-up:** verify rubric's actual aggregation function before relying on M2's "cap at 0.5" fixes — they may be inert if dimensions are not arithmetic-mean-aggregated.

---

## Composite systemic fix (prioritized)

1. **(Highest priority, from M1)** Make Wave 3 step 3.5 fail-loud if no `tier2-*-calibration.md` is written. The protocol's central anti-anchoring control may have been silently bypassed for H1/H2/H3 — and possibly other invocations.
2. **(From M2)** Add an "Evidence-claim alignment" dimension OR split Evidence grounding into provenance + class-adequacy. Either way, source-only refutation of a runtime claim must top out at 0.5 on the evidence dimension.
3. **(From M4)** For REFUTE verdicts, cap Evidence-grounding at 0.5 unless the card includes a runtime/empirical negative result, not a source-read absence-of-positive.
4. **(From M1, B3 contribution)** When the calibrator runs against a REFUTE ≥ 0.85, require it to draft a one-paragraph steel-manned CONFIRM and downgrade by its strength.
5. **(From M3)** Add Wave 3 step 1.5 routing: runtime-only claims go to systems-engineer / devops-architect regardless of `--type`; forbid closing a runtime claim at >0.85 on static-only evidence.

---

## Return contract (per sc-adversarial-protocol)

```yaml
merged_output_path: /config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/calibration-failure/agent-C-merged.md
convergence_score: 0.71
artifacts_dir: inline-returned (artifacts folded into this single merged file per depth=quick scope)
status: success
base_variant: agent-C (/sc:troubleshoot-grounded)
unresolved_conflicts: 0
fallback_mode: false
failure_stage: null
invocation_method: skill-direct
unaddressed_invariants: []  # Round 2.5 skipped per --depth quick; no probe was run
```

## 3-line merge summary

1. **Agent C selected as base** (combined 0.94 vs B 0.88 vs A 0.80) because C1 uniquely surfaces a verifiable artifact-absence finding that falsifies an implicit shared assumption of A and B — namely that the calibrator ran at all.
2. **B1's "proposition substitution" framing merged into C2** to sharpen the evidence-class mismatch (creation vs registration distinction); **B2 added as new theory M4** to cover refute/confirm asymmetry which C did not name; **A1's split-dimension fix and B3's steel-manned-CONFIRM counter-procedure** merged into systemic-fix lists.
3. **A2 and A3 subsumed** (A2 by B2/M4; A3 by C1/M1 + B3); one residual shared assumption flagged (A-001: rubric aggregation is arithmetic-mean) — recommend verification before relying on "cap at 0.5" fixes.
