# Position V3 — CONDITIONAL: A delegation-decision rubric, not a blanket rule

**Proposition (reframed):** "Always delegate" (V1) and "never delegate" (V2) are both wrong *as blanket policies for all future protocols*, because the right answer depends on properties of each protocol's output and verification need. The correct framework pattern is a **decision rubric** applied per protocol.

## The delegation rubric — delegate to `/sc:reflect` IFF all four gates pass

A protocol should retire its bespoke validator and delegate to `/sc:reflect` **only if all four hold**; otherwise keep (or strengthen) the bespoke validator.

| Gate | Test | Rationale |
|---|---|---|
| **G1 — Input-type fit** | The protocol's verified output is **applied work gradeable against a spec** (not a set of recommendations a human gates). | Reflect UC-2's deviation taxonomy (Authorized/Necessary/Drift/Regression, `SKILL.md:3`) has *no referent* for recommendations (`context.md` §5, U-003). |
| **G2 — No circular agent reuse** | Reflect does not internally reuse the very agent being retired. | Reflect reuses `audit-validator` (`SKILL.md:561`); delegating cleanup-audit is circular (`context.md` §5). |
| **G3 — Property preservation** | The bespoke validator's distinctive property (e.g., `auggie-reviewer`'s *blind recall*) is **preserved or superseded** by reflect, not silently lost. | Reflect's `evidence-validator` is a *precision* gate; it cannot reproduce a *recall* pass (last session's INV-012). Retiring a recall reviewer for a precision gate loses coverage. |
| **G4 — Cost proportional to stakes** | The 5–10× token cost (`context.md` §4.1) is justified by the blast radius of an undetected defect (e.g., an auto-applied change vs a human-gated recommendation). | Mandating Tier-2 reflect on low-stakes, human-gated outputs over-pays. |

## Applying the rubric to the two named targets
- **`sc:auggie-review`:** G1 **FAIL** (review findings are recommendations, human-gated). G3 **FAIL** (`auggie-reviewer` is blind *recall*; reflect's gate is *precision*). → **Do not delegate.** Keep the blind pass; fix the same-context citation Read in-place.
- **`sc:cleanup-audit`:** G2 **FAIL** (circular `audit-validator` reuse). G1 **FAIL** (audit recommendations are operator-gated). → **Do not delegate.** Keep `audit-validator`; tune coverage if needed.

So for *these two*, the rubric yields "keep bespoke" — matching V2's conclusion but via a reusable test, not a blanket stance.

## Why a rubric beats either blanket policy for "all future protocols"
- A future protocol that **auto-applies** its output with **no human gate** and produces **work gradeable against a spec** (e.g., an autonomous migration executor) passes G1+G4 — and *should* delegate to reflect. A blanket "never" (V2) wrongly forbids this.
- A future protocol that emits **human-gated recommendations** or shares an agent with reflect should *not* delegate. A blanket "always" (V1) wrongly forces it, importing cost, monoculture, and type-mismatch.
- The rubric makes the decision **auditable**: each protocol records which gates it passed. That is a stronger framework guarantee than either "trust reflect everywhere" or "never touch reflect."

## Falsifiable "worth it IF"
> The rubric is the right pattern IF real protocols partition non-trivially across it — i.e., at least one plausible future protocol passes all four gates (delegation right) AND at least one fails (delegation wrong). If *every* conceivable protocol lands on the same side, a blanket rule is simpler and the rubric is over-engineering.

## Honest concessions
- A 4-gate rubric is more machinery than "always/never." If virtually all protocols produce human-gated recommendations, V2's blanket "keep bespoke" is simpler and nearly always right — the rubric's extra structure earns its keep only if applied-work protocols are a real, recurring category.
- The rubric needs an owner: someone must apply it per protocol and record the verdict, or it rots into "always keep bespoke" by default.
