# Proposal B — Replacement / Higher-leverage: replace the bespoke validator with `/sc:reflect --mode post`

**Stance:** Replace each target's bespoke verification mechanism with a full `/sc:reflect --mode post` pass, buying the complete disjoint-context property: the **heterogeneous multi-model reviewer ensemble** + **blind `confidence-calibrator`** + **mandatory `evidence-validator` gate** + **adversarial merge** — the bundle that exists "specifically to neutralise the representational bias that makes single-agent self-review unreliable" (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:3`).

**Why replacement, not addition:** running reflect *and* the bespoke validator is "2-3× the token cost of doing one well" (`.dev/brainstorms/sc-reflect-rebuild/integration-analysis.md:357`). If reflect's ensemble is strictly stronger than a single blind agent / 10% sample, you replace rather than stack.

---

## Integration point 1 — `sc:auggie-review`: replace the deep-mode cross-check + inline validation

- **Seam:** the `auggie-reviewer` blind agent (`SKILL.md:181`) + the Wave-3 inline file:line validation (`SKILL.md:204–207`) + persona cross-check (`SKILL.md:212–213`).
- **Change:** after Wave 2 produces `auggie-raw-*.json`, compose a *draft* `REVIEW.md`, then hand it to `/sc:reflect --mode post` with the diff as the "completed work" and the PR description/linked spec as the driving spec. Reflect's heterogeneous ensemble becomes the cross-check (replacing the single-class `auggie-reviewer`); its `evidence-validator` gate replaces the inline Read; its blind calibrator re-grades severity (replacing/augmenting the rubric remap at `SKILL.md:211`).
- **Reflect element reused:** the entire skill (UC-2 post-execution path, Tiers 1–2, Waves 1–5).

## Integration point 2 — `sc:cleanup-audit`: replace `audit-validator` spot-check

- **Seam:** the Validate step at `SKILL.md:69` (today: 10% `audit-validator` spot-check).
- **Change:** after `audit-consolidator` produces the consolidated report, replace the 10% spot-check with `/sc:reflect --mode post` over the full report, treating the audit recommendations as the "work" and the repo state as ground truth. Reflect's evidence-validator gate enforces 100% citation re-Read; the ensemble adjudicates DELETE/CONSOLIDATE risk across model classes.
- **Reflect element reused:** the entire skill.

---

## Token / latency delta
- **High.** Tier-2 reflect = **35–70k Claude + 10–25k auggie tokens** (`integration-analysis.md:347`), versus auggie-review's one extra deep-mode agent or cleanup-audit's one sampled validator. This is a **5–10× cost increase** on the verification stage.
- Latency: reflect runs Waves 1→5 with parallel reviewers + an adversarial merge subprocess — materially slower than a single Task round-trip. For cleanup-audit's `--pass all` (already 3 passes × N batches), appending a full reflect pass roughly doubles wall-clock on the validate stage.
- Partial mitigation: reflect Tier 1 (single grounded agent + blind calibrator, `SKILL.md:142–147`) is far cheaper (~3–8k) — but Tier-1-only forfeits the heterogeneous-ensemble property that is the *entire* justification for replacement. If you only want Tier 1, Proposal A (single agent) is cheaper still.

## Overlap / conflict risk — **HIGH** (this is the proposal's biggest weakness)
1. **Circular agent reuse (cleanup-audit):** reflect *internally reuses `audit-validator`* at Wave 5 (`SKILL.md:561`, `:1043`). Replacing cleanup-audit's `audit-validator` spot-check with reflect means reflect re-invokes `audit-validator` anyway — you have not removed the agent, you have *nested it inside a 5-wave wrapper*. Net: more cost for the same core check plus an ensemble on top.
2. **Semantic-fit mismatch (auggie-review):** reflect UC-2 is defined as auditing "completed work for 100% adherence" and classifying divergences under a 4-category **deviation taxonomy** (Authorized / Necessary / Drift / Regression) (`SKILL.md:3`). A *code review's findings are recommendations, not completed work* — there is no executed tasklist to grade for adherence. Forcing review findings through UC-2 mis-types the input; the deviation taxonomy has no natural referent.
3. **auggie-review already consumes reflect downstream** (remediation Phases C/E, `SKILL.md:324,327`). Adding reflect *upstream* at Wave 3 too means two reflect invocations per review-with-remediation — compounding cost and creating a confusing "reflect validates the review, then reflect validates the fix" double surface.
4. **Loss of comment-only safety framing:** auggie-review is deliberately a `--comment`-only reviewer (`SKILL.md:313`); reflect's UC-2 carries a promotion-gate / status-mutation surface (sprint-release, task move) that is semantically wrong for a non-mutating review.

## Falsifiable claim
> **This is worth it IF** the heterogeneous multi-model ensemble catches review/audit *recommendation* defects that a single-class blind agent (auggie-reviewer) or a 10% sample (audit-validator) provably miss, **at a rate that justifies a 5–10× token increase** — AND the input can be cleanly typed as "completed work vs spec" so UC-2's taxonomy applies.
>
> **It is NOT worth it IF** (a) the strongest pro-disjoint-context evidence — R0/PR#112 (`.dev/releases/backlog/TaskQAComparison/adversarial/refactor-plan.md:83`) — is about *applied-change* QA, not read-only recommendations (it is), so the failure mode it defends against ("the fix passed surface signal but missed the defect") *cannot occur when nothing is applied*; OR (b) the circular `audit-validator` nesting means you pay ensemble cost for a check you already had.

## Confidence
- **auggie-review replacement: ~45%** (<70% → this is an open question, do NOT proceed). The semantic-fit mismatch (findings ≠ completed work) and the existing downstream reflect consumption make this the weakest single integration in the whole analysis.
- **cleanup-audit replacement: ~40%** (<70% → open question). The circular `audit-validator` nesting makes replacement actively wasteful versus the status quo or Proposal A.

## Honest self-critique
This proposal is the "more is better" trap. Reflect's ensemble is genuinely stronger for *grading applied work against a spec* — its designed UC-2 use case. Review and audit produce **recommendations a human gates**, not applied changes, so the disjoint-context property that makes reflect valuable in sprint/task pipelines has a much weaker referent here. B is most defensible only if review/audit output feeds a downstream *auto-apply* pipeline with no human gate — which is not the current shape of either target.
