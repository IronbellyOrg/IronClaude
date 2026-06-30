# Proposal A — Additive / Minimal: drop `evidence-validator` at the existing validation seam

**Stance:** Wire exactly ONE reflect agent — **`evidence-validator`** — into each target at its current validation seam. Leave every other wave/pass untouched. Do NOT pull in the heterogeneous ensemble, the calibrator, the adversarial merge, or `/sc:reflect` as a whole.

**Why `evidence-validator` specifically:** It is (1) explicitly *designed to be reusable by any skill that produces an evidence-cited report* (`src/superclaude/agents/evidence-validator.md:3,16`), (2) "always invoked via `Task` with an explicit `report_draft_path`" (`:17`) — i.e. genuinely standalone, (3) read-only with a tiny tool surface (`Read, Grep, Glob`, `:5`), so it is the cheapest reflect element, and (4) **neither target already uses it** (auggie-review's citation check is an inline same-context Read; cleanup-audit uses `audit-validator`, a *different* agent). This is the only reflect agent that adds a property both targets lack — a **disjoint-context, drop-not-downgrade citation gate** — without circular overlap.

---

## Integration point 1 — `sc:auggie-review`, Wave 3

- **Seam:** Wave 3 "File:line validation pass (non-negotiable)" at `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:204–207`, immediately **before** the final `REVIEW.md` compose at `:214`.
- **Today:** the orchestrator itself Reads each cited line in the *same context* that parsed the Auggie JSON (`SKILL.md:205`). Same-context re-Read is exactly the failure mode CLAUDE.md "Context freshness discipline" warns about — and which bit *this very investigation* (a subagent cited reflect `SKILL.md:415`; the real line was `:561`).
- **Change:** after the inline pass produces the deduped/remapped finding set, spawn `evidence-validator` via `Task` with `report_draft_path = <output-dir>/REVIEW.draft.md` (or the structured finding list). It re-Reads every `file:line` in a fresh context and returns the verified set; unfounded citations are dropped, not downgraded. Compose `REVIEW.md` from the *verified* set.
- **Reflect element reused:** `evidence-validator` agent only.

## Integration point 2 — `sc:cleanup-audit`, Validate step

- **Seam:** the Validate step at `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:69`, which today spawns `audit-validator` for a **10% stratified spot-check** (`audit-validator.md:34,36–39`), before `audit-consolidator` writes the final report.
- **Today:** only 10% of findings have their grep/citation re-tested; 90% ship on the originating agent's word.
- **Change:** *in addition to* the existing 10% `audit-validator` spot-check, run `evidence-validator` as a **100% citation re-Read** of the consolidated DELETE/CONSOLIDATE findings' `file:line` anchors (the verifiable-anchor requirement at `rules/verification-protocol.md:83`). `evidence-validator` ≠ `audit-validator`, so this is *not* the circular overlap that pulling in full reflect would create.
- **Reflect element reused:** `evidence-validator` agent only.

---

## Token / latency delta
- `evidence-validator` is a single read-only agent (Read/Grep/Glob). Cost scales with citation count, not with a model ensemble. Estimate **+2–8k tokens / +1 agent round-trip** per run — roughly an order of magnitude below a Tier-2 reflect pass (35–70k + 10–25k auggie, per `.dev/brainstorms/sc-reflect-rebuild/integration-analysis.md:347`).
- auggie-review: negligible added latency (one extra Task in Wave 3, parallelizable with nothing else pending).
- cleanup-audit: 100% re-Read is heavier than the 10% sample on very large audits (>200 findings). Mitigation: gate the 100% pass to DELETE + CONSOLIDATE findings only (the destructive recommendations), leave KEEP to the sample.

## Overlap / conflict risk
- **auggie-review: LOW.** No existing agent does a disjoint-context citation re-Read; `evidence-validator` fills a real gap. Only conflict: redundant with the inline Wave-3 Read for findings whose citation was already correct — but that is *cheap* redundancy that is the whole point (catch the wrong ones).
- **cleanup-audit: LOW–MEDIUM.** Partial scope overlap with `audit-validator`'s Check 1 (Grep Claim Verification, `audit-validator.md:45`) on the 10% sample. But `audit-validator` *samples* and re-greps; `evidence-validator` does *full* file:line re-Read with drop semantics — different scope, different guarantee. No circular dependency (evidence-validator is not reused elsewhere by cleanup-audit).

## Falsifiable claim
> **This is worth it IF** there exists ≥1 documented case where a review finding or an audit DELETE/CONSOLIDATE recommendation shipped with a `file:line` citation that was wrong/stale and survived the existing same-context inline Read (auggie-review) or fell outside the 10% sample (cleanup-audit). The freshness-drift caught in this very session (`:415` vs `:561`) is a live existence proof that same-context citation passes miss real drift.
>
> **It is NOT worth it IF** an audit of recent `REVIEW.md` / audit reports shows zero citation defects reaching the final artifact — i.e. the inline pass + 10% sample already catch everything.

## Confidence
- **auggie-review integration: ~88%** (70–89% band → present as an alternative, not auto-proceed). The seam is clean and the gap is real, but I have not measured the *base rate* of citation defects surviving Wave 3, so I cannot assert ≥90%. Recommend a one-time backtest over the last N `REVIEW.md` files before committing.
- **cleanup-audit integration: ~72%** (70–89% band). The 100%-re-Read value is real but partly overlaps `audit-validator`; the right scope (DELETE/CONSOLIDATE-only vs all) is an open tuning question.

## Why this beats B and C (one line each)
- **vs B:** captures ~80% of the disjoint-context benefit (citation gate) at ~10% of the token cost, with zero circular overlap and no semantic-fit problem.
- **vs C:** C is right that *full reflect* is overkill, but C under-weights that auggie-review's citation check is same-context (a known blind spot) and cleanup-audit's is only 10% — a cheap single agent closes both without the cost C objects to.
