# Agent C — /sc:troubleshoot-grounded theories for the H3 calibration miss

## /sc:troubleshoot run summary

- **Invocation used:** `Skill sc:troubleshoot` → `Skill sc-troubleshoot-protocol` with `--depth deep` and the calibration-failure symptom as the issue description. The protocol skill loaded and its wave structure guided the evidence collection below.
- **Output location:** inline — the protocol's Wave 5 REPORT.md was not re-written; instead the diagnostic findings are folded into the theories below per the meta-investigation framing (the calibration miss IS the diagnosis target; the artifact set under `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/` is the evidence corpus).
- **Key findings the troubleshoot surfaced:**
  - The H3 calibration report file (`tier2-h3-calibration.md`) does not exist in the output directory — only the H3 hypothesis card itself. Wave 3 step 3.5's promised independent re-grading either did not run for H3 or its output was not persisted. The 0.95 is the *agent's self-reported* number, not the calibrator's number.
  - The H3 card's "Evidence" section (E1-E5) cites external upstream GitHub URLs (zellij-org/zellij @ v0.44.2), not local files. The confidence-calibrator's spot-check procedure (calibrator.md:50-52) Reads cited `file:line` — but the Read tool cannot fetch GitHub URLs; cited evidence is structurally un-spot-checkable.
  - The escalation rubric's "Evidence grounding" anchor (rubric.md:13) accepts "cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom". H3 has source-only citations and zero runtime-reproduction evidence, yet would still earn 1.0 on this dimension because the rubric does not require the symptom-reproduction clause when a file:line clause is present (the OR is disjunctive).
  - The card self-flags its limitation explicitly at lines 102-107 ("`start_client_impl` body was not directly inspected... If I'm wrong it's probably because... a version-0.44.2-specific early-return I cannot see from the four files I inspected") but this self-flagged epistemic risk has no rubric dimension to land in.
  - The refactoring-expert agent (per audit.log:18) was tasked with H3. Its declared focus area (refactoring-expert.md:22-27: code simplification, technical debt, SOLID principles, quality metrics) does not include runtime-behavior, PTY semantics, or CLI dispatch tracing — agent/task mismatch on the very claim type being adjudicated.
  - The escalation rubric is built for Tier 1 → Tier 2 escalation decisions; it has no machinery for adjudicating a Tier 2 card's REFUTE/CONFIRM *verdict*. The calibrator scores confidence-in-claim but no agent in the pipeline scores confidence-in-refutation.

## Theory C1: Calibrator-output absence — Wave 3 step 3.5 never ran (or its output was dropped) for H3

**Claim:** The 0.95 number was never independently re-graded. The Wave 3 step 3.5 contract (sc-troubleshoot-protocol step "Calibrate each card independently — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card)") promises a per-card calibration report at `<output-dir>/tier2-<agent-name>-calibration.md`, but no calibration artifacts exist for H1, H2, or H3 in the output dir. The 0.95 propagated from the agent's self-reported `## 4. Confidence` section straight into audit.log and REPORT.md with no anchoring-resistant pass between them. The protocol's central anti-anchoring control (calibrator-with-stripped-formation-context) was bypassed.

**Troubleshoot-derived evidence:** The output directory listing shows hypothesis cards (`tier2-h1-*.md`, `tier2-h2-*.md`, `tier2-h3-*.md`) but NO `tier2-*-calibration.md` files. The audit.log records only "H3 ... REFUTED 0.95" without any calibration-report path, and shows no `calibration: inline-fallback` marker that the fallback path (Wave 1.7 step 2 fallback rule, applied per-card in Wave 3) would emit.

**Artifact evidence:**
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/audit.log:18-22` — lists H1/H2/H3 verdicts and confidence numbers, but no per-card calibration pointer; no `calibration: inline-fallback` note either way.
- `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 step 3.5 — "Calibrate each card independently — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with `card_tier=2` and `output_path=<output-dir>/tier2-<agent-name>-calibration.md`." This file path pattern is absent for all three cards.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:92-93` — `## 4. Confidence` section reads "**95%** that H3 is refuted." This number, agent-self-reported, is the same number that ended up in audit.log:22 and REPORT.md:166 — strongly suggestive of pass-through.
- `/config/.claude/agents/confidence-calibrator.md:24-26` — "Self-reported confidence on the card is a signal, not a number" — the calibrator is the layer that's supposed to prevent self-reported-confidence-as-score; if it didn't run, the protection didn't apply.

**Per-theory confidence:** 0.80

**Systemic fix (one line):** Make Wave 3 step 3.5 fail-loud if no `tier2-*-calibration.md` is written within a timeout, instead of silently letting the agent's self-reported confidence become the recorded number.

## Theory C2: Claim-type vs evidence-type mismatch is not a rubric dimension

**Claim:** H3's claim is a *runtime-behavior* claim ("the CLI invocation DOES create a session at runtime"). The evidence chain is *entirely static source-read* across four files in an external repo, with zero runtime traces, zero CI reproductions, and one weak third-party usage anecdote (E5 from a DEV.to article). The escalation rubric's five dimensions (Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence) do not contain a dimension that asks "is the evidence type appropriate to the claim type?" The Reproducibility-fit dimension is the closest, but its 1.0 anchor permits "deterministic exception with a clear trigger" which a source-read claim about dispatcher logic can technically satisfy.

**Troubleshoot-derived evidence:** The rubric scoring an entirely source-read refutation of a runtime claim at high confidence is mechanically valid under rubric.md:11-19. The card itself acknowledges the mismatch at lines 102-107 ("the conclusion relies on the public-API contract of `ClientInfo::New`. If `start_client_impl` has a guard that early-returns when `command == Some(Command::Options(...))`, the refutation would weaken") but this self-acknowledged structural risk has no rubric dimension that would penalize it.

**Artifact evidence:**
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-17` — table of five dimensions; no dimension scores claim-type/evidence-type alignment. "Evidence grounding" rewards file:line citations regardless of whether the symptom is static or runtime.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:102-107` — `## 6. Risks of acting on this card` and section 7 ("If I'm wrong it's probably because...") explicitly call out the source-only-against-runtime-claim gap: "`start_client_impl` body was not directly inspected... E5 (third-party usage works) provides independent empirical validation." E5 is the only empirical leg; it's an anecdotal DEV.to article.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/wave1_5-branch-A.md:233-235` — Branch A itself flagged "Question 5" as "uncertain — empirical test required" for this exact `options`-subcommand question. The H3 card is supposed to resolve that uncertainty but resolves it with the same evidence type (source-read) that left it uncertain.
- `/config/.claude/agents/confidence-calibrator.md:21` — "Apply the rubric mechanically: one dimension at a time, score with evidence, never inherit the card's self-reported confidence." Mechanical rubric application against a rubric with no claim-type dimension cannot catch a claim-type/evidence-type mismatch; the calibrator is doing what it's told and the rubric is what's incomplete.

**Per-theory confidence:** 0.78

**Systemic fix (one line):** Add a 6th rubric dimension "Evidence-claim alignment" that caps Evidence-grounding at 0.5 when the claim is a runtime-behavior claim and no runtime trace, CI reproduction, or local-execution log is cited.

## Theory C3: Agent-domain mismatch — refactoring-expert is the wrong agent class for runtime-CLI claims

**Claim:** The protocol's agent-selection table assigns specialist agents based on `--type` (test|bug|build|performance|security|deployment). For `--type test`, the table picks `quality-engineer, root-cause-analyst, refactoring-expert (if test is brittle by structure)`. H3's claim — a CLI-dispatch / `start_client` runtime question — is not a refactoring question. It is a runtime-tracing / systems-debugging question. The refactoring-expert agent (per its own .md spec) focuses on code-quality, SOLID, complexity metrics, and pattern application — none of which equips it to runtime-verify a `Command::Options` dispatcher claim. The 0.95 confidence is what an agent produces when asked to adjudicate outside its declared focus area: it does the best static-analysis pass it can and rates the static-pass result highly because the static pass succeeded — but the *claim type* required a runtime pass it was not equipped to run.

**Troubleshoot-derived evidence:** The audit.log records "3 specialist agents (root-cause-analyst, quality-engineer, refactoring-expert)" for Wave 3. The H3 card's evidence is exclusively source-read across four upstream files (E1-E4) plus an anecdotal third-party article (E5) — a profile consistent with a refactorer's natural strengths (read code, identify patterns, reason about static structure) and a profile NOT consistent with the runtime claim ("DOES create a session") under investigation.

**Artifact evidence:**
- `/config/.claude/agents/refactoring-expert.md:22-27` — focus areas: "Code Simplification, Technical Debt Reduction, Pattern Application, Quality Metrics, Safe Transformation". None of these are runtime / PTY / CLI-dispatch domains.
- `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 agent-selection table — `test` type maps to `quality-engineer, root-cause-analyst, refactoring-expert (if test is brittle by structure)`. T4 is a contract test whose failure is a *zellij runtime behavior*, not a brittleness-by-structure problem. The "if" condition was satisfied imprecisely.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/audit.log:18` — names the 3 agents spawned; refactoring-expert was one of them.
- `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:21-79` — the entire Evidence section is a static source-read across 4 files plus an anecdote. No `bash` runs, no `zellij list-sessions` traces, no attempt to reproduce the invocation. This is the work product of a code-reading specialist applied to a runtime question.

**Per-theory confidence:** 0.62

**Systemic fix (one line):** Add a Wave 3 step 1.5 that re-routes claims with runtime-only evidence requirements (CLI dispatch, PTY, syscall, network) to a `systems-engineer` / `devops-architect` slot regardless of `--type`, and explicitly forbids closing a runtime claim at >0.85 confidence on static-only evidence.
