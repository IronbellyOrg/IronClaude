---
topic: "Refactor confidence-check skill + confidence-calibrator agent + escalation-rubric + hypothesis-card-template to close the M1+M2+M3a calibration miss (source-only evidence on runtime-behavior claims must not score >0.85 calibrated)"
domain: code
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-05-26T20:30:00Z
---

# Seed Brief: calibration-refactor-pr86

## Problem Statement

The confidence-calibration apparatus (escalation-rubric + confidence-calibrator agent + hypothesis-card template + confidence-check skill) systematically produces ≥0.85 calibrated confidence on source-only evidence for runtime-behavior claims. The pr86-integration-contracts substrate showed a calibrated 0.90 RCA verdict despite the calibrator's own evidence-grounding score = 0.5 (it could not execute, only Read). The structurally analogous H3 case shipped a 0.95-REFUTE verdict that CI then contradicted. FINAL-MERGED-CAUSES.md identifies five mechanisms (M1, M2, M3a, M3b, M3c, M4); brainstorm must propose the smallest refactor closing M1 + M2 + M3a (the three unanimous mechanisms) with M4 as defense-in-depth.

## Known Context

- **M1 (0.89, unanimous)**: `escalation-rubric.md:19` — `Confidence = arithmetic mean of the five dimension scores`. Unweighted mean lets evidence-grounding=0.5 + four 1.0s = 0.90.
- **M2 (0.85, unanimous)**: `escalation-rubric.md:13` — Evidence-grounding 1.0 anchor uses `OR` clause: "Cited file:line matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom". Source-citation alone earns 1.0 on runtime-behavior claims. Calibrator has `tools: Read` (`confidence-calibrator.md:5`) and physically cannot execute reproducers.
- **M3a (0.78, novel)**: Rubric treats AFFIRM and REFUTE as symmetric. REFUTE-wrong closes the investigation door; AFFIRM-wrong gets caught by CI. The only existing asymmetry is `--type security AND confidence < 0.95 → ESCALATE` (`escalation-rubric.md:39`).
- **M3b (0.65)**: Calibrator is stripped of formation context (`confidence-calibrator.md:21`); upstream hedge-text is lost. Card template's "If I'm wrong, it's probably because…" (`hypothesis-card-template.md:104-108`) is a one-sentence alternative, NOT a falsification standard.
- **M3c (0.45)**: Card's self-reported confidence is shown to the calibrator with only prompt-level norm ("a signal, not a number") preventing anchoring.
- **M4 (0.68)**: confidence-check/SKILL.md:14-18 advertises "Precision 1.000, Recall 1.000, 8/8 test cases" but eval corpus never tested structurally-unverifiable predicates (runtime-behavior, sha-pinned diff).
- **Source-of-truth**: `src/superclaude/skills/confidence-check/SKILL.md`, `src/superclaude/agents/confidence-calibrator.md`, `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`, `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`. `.claude/` is sync-dev output (gitignored).
- **Compounding constraint**: M1+M2 multiplicative — fix either alone underfits. M3a presupposes M2's runtime-check axis (sequencing: apply M2 first, then M3a atop it).
- **Audited Files (Read-verified)**:
  - `/config/workspace/IronClaude/src/superclaude/skills/confidence-check/SKILL.md` (existence confirmed; content identical to `.claude/` copy)
  - `/config/workspace/IronClaude/src/superclaude/agents/confidence-calibrator.md` (existence confirmed)
  - `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (existence confirmed)
  - `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (existence confirmed)

## Constraints

- **Markdown-only deliverable** — no code changes during this investigation
- **All proposed file modifications must target `src/superclaude/`** (source of truth), NOT `.claude/` (sync-dev output)
- **Smallest set** closing M1 + M2 + M3a — additional mechanisms = nice-to-have / defense-in-depth
- **Backward-compatible** with in-flight calibration cards or schema-migration documented
- **No fabricated paths** — cite only files Read-verified
- **No invasive process changes** — proposal must compose with existing /sc:troubleshoot wave architecture (Wave 1.7 Tier 1 calibration, Wave 3 Tier 2 calibration)
- **No multi-agent dispatch** (e.g., dual-calibrator instances) unless that is the single mechanism closing a unanimous cause — token cost is real

## Success Criteria

- **For each target file**: name the `src/superclaude/<path>`, section/symbol/heading, and literal text-change-shape (insert / replace / append) with rough diff sketch
- **Coverage matrix**: rows = {M1, M2, M3a, M3b, M3c, M4}, cols = file changes, cells = `closes` / `partially closes` / `n/a`
- **Minimal-change subset**: 2–3 file edits explicitly named that close M1 + M2 + M3a together
- **Counter-arguments considered**: which alternative refactors were REJECTED and why
- **Regression test/eval-suite additions**: pin tests / golden cards landing alongside the refactor
- **Migration / backward-compat note**: how to handle in-flight cards under the new schema

## Open Questions

- Is a 6th rubric dimension ("Runtime check") strictly required, or can M2 be closed by splitting "Evidence grounding" into "Source-citation" + "Runtime verification" sub-scores under the existing 5-dim envelope?
- Should the gated-minimum formula (M1 fix) be `min(evidence_grounding + 0.3, mean(other_four))` or a hard veto `evidence_grounding ≤ 0.5 → cap at 0.75`?
- Where does the "claim_class" tag (runtime-behavior vs static-defect) live — card frontmatter or per-dimension annotation? Whoever writes it (card author? calibrator?) determines the trust model.
- For M3a's verdict-direction modifier: is the right gate `verdict=REFUTE AND claim_class=runtime-behavior AND runtime_check<1.0 → cap at 0.70`, or stronger (auto-ESCALATE regardless of confidence)?
- Is the confidence-check SKILL.md (pre-implementation skill, NOT troubleshoot's calibrator) actually load-bearing here, or is the failure mode purely in the troubleshoot calibration chain? The cultural-prior bullet in M2 §Evidence cites confidence-check SKILL.md:53-110 — but changing that skill may not be strictly necessary to close M1/M2/M3a.
