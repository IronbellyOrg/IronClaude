# Position V1 — PRO: Remove bespoke validators, delegate all verification to `/sc:reflect`

**Proposition (affirmed):** Remove the `auggie-reviewer` blind pass from `sc:auggie-review` and the `audit-validator` spot-check from `sc:cleanup-audit`, and route their verification through `/sc:reflect`. Adopt this as a **standing framework pattern**: future protocols that need independent verification delegate to `/sc:reflect` rather than growing their own bespoke validator.

## Core argument: one canonical, maximally-rigorous verification surface

1. **Reflect is strictly the most rigorous validator the framework has.** It is the only verifier combining a **heterogeneous multi-model reviewer ensemble** (`context.md` §3.1, `sc-reflect-protocol/SKILL.md:33`), **blind `confidence-calibrator`** anti-anchoring (`SKILL.md:34`), a **mandatory `evidence-validator` gate** that drops-not-downgrades (`SKILL.md:35`), and an **adversarial merge** (`SKILL.md:154`). Every bespoke validator is a strict subset: `auggie-reviewer` is one Claude-class pass; `audit-validator` is one sampled agent. Delegating upgrades both to the superset.

2. **DRY / single-source-of-truth for verification.** Today each protocol reinvents verification: auggie-review has an inline Wave-3 Read + a blind agent; cleanup-audit has a 10% spot-check; troubleshoot, roadmap, sprint each have their own. That is N bespoke validators to maintain, test, and keep correct. Consolidating onto one verification skill means one contract to harden, one place to fix a verification bug, one eval surface.

3. **Future protocols get rigor for free.** The "all future protocols" generalization is the payoff: a new protocol author writes the protocol and adds `→ /sc:reflect --mode post` instead of designing, building, and eval-ing a bespoke validator. Verification quality stops being a per-protocol lottery and becomes a framework guarantee.

4. **Reflect already absorbs the bespoke agents.** Reflect *internally reuses* `audit-validator` (`context.md` §3.1, `SKILL.md:561`). So delegation is not "throw away audit-validator" — it's "let reflect orchestrate it inside a stronger pipeline." The bespoke agent's value is preserved; only the bespoke *orchestration* is retired.

5. **Eliminates same-context blind spots structurally.** auggie-review's Wave-3 citation Read is same-context (`context.md` §1.3, `SKILL.md:204–205`); this session's own `:415`→`:561` drift proves same-context passes miss drift. A reflect pass runs in a disjoint context with a different model class — the property that caught R0/PR#112 (`context.md` §4.2).

## Falsifiable "worth it IF"
> Delegation is worth it IF (a) reflect's superset of mechanisms catches defects each bespoke validator misses at a rate that justifies its cost, AND (b) the maintenance saving of one validator vs N bespoke ones is real, AND (c) reflect's input can be typed to fit each protocol's output.

## Honest concessions
- Reflect Tier-2 costs 35–70k + 10–25k auggie (`context.md` §4.1) — far above a bespoke validator. Mandating it universally is expensive.
- Reflect's UC-2 is designed for "completed work vs spec"; review/audit *findings* are recommendations, so the input may need re-typing.
- A single universal validator is a monoculture: a reflect blind spot propagates to every protocol at once.
