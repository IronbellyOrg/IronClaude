# Position V2 — ANTI: Keep the bespoke validators; do not delegate to `/sc:reflect`

**Proposition (rejected):** Removing `auggie-reviewer` / `audit-validator` and delegating verification to `/sc:reflect` — especially as a blanket pattern for all future protocols — is a net loss. Keep purpose-built validators.

## Core argument: the bespoke validators do jobs reflect does not, and "one validator for all" destroys the diversity that makes verification work

1. **The bespoke validators are not subsets — they do *different jobs*.**
   - `auggie-reviewer` is a **blind, recall-oriented content reviewer**: it independently *generates* findings before seeing Auggie's (`context.md` §1.2, `auggie-reviewer.md:20`). Its job is "find issues a different mind would find." Reflect's UC-2 is a **deviation audit**: it grades *completed work* against a spec under a 4-category taxonomy (`context.md` §0, `SKILL.md:3`). Delegating review to reflect **loses the blind recall pass** and replaces it with an audit whose taxonomy has *no referent* for recommendations (`context.md` §5, U-003).
   - `audit-validator` does grep-claim re-testing, **classification-accuracy**, and **dynamic-loading** checks (`context.md` §2.2). These are content checks reflect's `evidence-validator` gate (a *citation* gate) does not perform.

2. **Delegation to reflect for cleanup-audit is circular.** Reflect *internally reuses `audit-validator`* (`context.md` §3.1, `SKILL.md:561,1043`). "Delegate cleanup-audit verification to reflect" = "reflect re-invokes the agent cleanup-audit already runs, wrapped in 5 extra waves." You pay ensemble cost for the same core check (`context.md` §5).

3. **A single universal validator is a framework-level monoculture — the opposite of the diversity reflect itself relies on.** Reflect's *entire* rationale is that heterogeneous reviewers prevent representational bias from stacking (`SKILL.md:33`). Mandating reflect as the *one* validator for all protocols recreates the monoculture at the framework layer: every protocol inherits the *same* verification blind spots, the *same* contract, the *same* failure mode. Diversity at the protocol layer (different validators tuned to different jobs) is a feature, not debt.

4. **Coupling to a moving target.** Reflect was modified **today, 2026-06-04 00:25** (`context.md` citation-freshness note) — and a stale citation in *this very investigation* (`:415`→`:561`) shows it drifts. Making N protocols depend on reflect's contract means one reflect change can break N protocols' verification at once. Bespoke validators fail independently.

5. **Cost.** Bespoke validators are cheap (one agent, sampled). Reflect Tier-2 is 35–70k + 10–25k auggie (`context.md` §4.1) — a 5–10× tax imposed on *every* protocol that adopts the pattern.

## Falsifiable "worth it IF" (i.e., when V2 is wrong)
> Keeping bespoke validators is wrong IF a protocol's output is genuinely "applied work gradeable against a spec," the bespoke validator demonstrably misses a defect class reflect catches, AND there is no circular agent reuse — i.e., the narrow case where reflect's job actually matches the protocol's need.

## Honest concessions
- N bespoke validators *is* more total maintenance surface than one shared skill (V1's DRY point is real).
- auggie-review's same-context citation Read is a genuine blind spot (`context.md` §1.3) — but the fix is to strengthen *that pass*, not to import reflect.
- Some future protocols *will* produce applied work where reflect genuinely fits; a blanket "never delegate" is as wrong as a blanket "always delegate."
