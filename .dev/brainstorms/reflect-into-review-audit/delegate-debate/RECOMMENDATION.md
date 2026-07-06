<!-- Provenance: produced by /sc:adversarial (Mode B, generated positions) -->
<!-- Base: V3 (rubric) + decisive V2 transfers + V1 kernel -->
<!-- Merge date: 2026-06-04 -->

# Merged Verdict — Remove the bespoke validators and delegate verification to `/sc:reflect`?

## Bottom line

**For the two named targets: No — keep both bespoke validators.** Unanimous across all three positions; survives the invariant probe.

**As a standing pattern for all future protocols: No, not as "delegate by default."** The defensible pattern is the inverse: **keep-bespoke by default; delegation to `/sc:reflect` is a hard-gated exception** — and even then it must be paired with framework-level guards that a per-protocol decision alone cannot provide.

Convergence ~0.78 (per-target ~0.95; framework-policy resolved by augmenting the rubric).

<!-- Source: V2 (decisive) + invariant probe -->
## Why removing them fails — per target

### `sc:auggie-review`
- The `auggie-reviewer` blind pass is a **recall-oriented content generator** — it independently *finds* issues before seeing Auggie's (`context.md` §1.2, `auggie-reviewer.md:20`). Reflect's `evidence-validator` is a **precision** citation gate. Retiring recall for precision **silently drops coverage**, not upgrades it (recall ≠ precision; last session's INV-012).
- Review findings are **human-gated recommendations**, not applied work — reflect UC-2's deviation taxonomy (Authorized/Necessary/Drift/Regression) has *no referent* (`context.md` §0, `SKILL.md:3`).
- **Already carries the coupling risk:** auggie-review *already* runs `/sc:reflect --type task --validate` as a **sole blocking validator** at remediation Phase E ("block on validation failures", `SKILL.md:327`) with no out-of-band non-reflect watcher. So reflect is *already* in a load-bearing position here — an argument for an independent cross-check of *that seam*, not for extending reflect to the review findings too.

### `sc:cleanup-audit`
- Delegating to reflect is **circular**: reflect *internally reuses `audit-validator`* (`context.md` §3.1, `SKILL.md:561,1043`). "Delegate to reflect" = "reflect re-invokes the agent cleanup-audit already runs, wrapped in 5 waves" — you pay ensemble cost for the same core check.
- `audit-validator`'s content checks (classification accuracy, dynamic-loading) are not reproduced by a reflect citation gate.

<!-- Source: V2 monoculture thesis, made structural by the invariant probe -->
## Why "delegate to all future protocols" fails — the framework-scale defect

The probe's four HIGH findings show a single-universal-validator pattern is self-undermining:

1. **Aggregate monoculture is invisible to per-protocol logic (INV-001/INV-003).** Any per-protocol rule decides one protocol at a time; monoculture is an *aggregate* property. N individually-correct delegations sum to "reflect verifies everything" — the exact correlated-failure mode reflect's *own* internal heterogeneity exists to prevent (`SKILL.md:33`), now recreated one layer up. Worse, a delegation rubric's success condition (recurring applied-work protocols) **is** its monoculture trigger.
2. **The watcher never watches (INV-002).** Keeping bespoke validators in other protocols does *not* validate reflect — those validators check *their own* protocol's output and never cross-check reflect's verdicts. A framework where reflect verifies everything leaves reflect's own output validated by **nothing independent** ("who watches the watcher" — unmitigated).
3. **The dependency is unstable (A-002 / INV-008).** `sc-reflect-protocol/SKILL.md` was modified *this session* with ~146 lines of drift (a stale `:415`→`:561` citation in this very investigation). Coupling N protocols to a contract that moves that fast = one edit → N simultaneous verification regressions. A prose "freeze" is freeze-in-name-only without a version-pin/hash/CI gate.

<!-- Source: V3 scaffold + V1 kernel + the four merge changes -->
## What to do instead — the defensible standing pattern

**Default: each protocol keeps its own purpose-built validator.** Delegation to `/sc:reflect` is permitted only when ALL of the following hold (V3's 4 gates + 2 framework guards from the probe):

- **G0 (framework, NEW):** delegating would not push the fraction of protocols whose *sole* independent verifier is reflect past a framework-set heterogeneity bound. Crossing it requires an owned, recorded decision. *(Resolves the aggregate-monoculture blind spot.)*
- **G1 input-type fit:** the protocol's output is **applied work gradeable against a spec**, not human-gated recommendations. Fail closed on mixed/undecidable output.
- **G2 no circular reuse:** reflect does not internally reuse the agent being retired (kills cleanup-audit delegation outright).
- **G3 property preservation:** the bespoke validator's distinctive property (e.g., blind recall) is preserved/superseded, not lost.
- **G4 cost-vs-stakes:** the 5–10× token cost is justified by the blast radius of an undetected defect.
- **R (standing rule, NEW):** reflect's own output is independently cross-checked by a *non-reflect* surface; reflect is never any protocol's sole validator without that cross-check. *(Resolves "who watches the watcher.")*
- **Preconditions:** reflect's contract is pinned by version/hash with a CI/eval gate before any standing adoption; each protocol's gate verdict records the contract-version it was decided against and re-runs on contract change; the rubric has a named owner.

**Applying it to the two targets:** auggie-review fails G1+G3; cleanup-audit fails G1+G2 → **keep both**. The narrow case the pattern *does* permit: a genuine future auto-apply/autonomous-executor protocol (no human gate, output gradeable against a spec) passes G1+G4 — but still only under G0+R.

## Direct answer to the proposition
- **"Remove the independent validator in both of these":** No. Keep both. (Merit of removal: none for these targets; flaw: loses recall / introduces circularity.)
- **"…and delegate that verification to /sc:reflect":** Merit is real only for a narrow future category (applied-work / auto-apply protocols), and even there reflect must never be the *sole* validator and the aggregate concentration must be bounded.
- **"…(and all future prompts)":** No — not as a blanket "delegate." Adopt keep-bespoke-by-default + the hard-gated exception above. The blanket-delegate form is rejected (it manufactures the monoculture it would need diversity to survive).

## Concrete next step
READ-ONLY investigation — **no skill file was edited.** If the framework wants to formalize this, it is a **separate task**: (1) draft the gated-delegation policy (G0–G4 + R + preconditions) as a framework doc; (2) **separately and with higher priority**, review auggie-review's Phase-E sole-reflect-blocking seam (`SKILL.md:327`) for an independent cross-check — that is a pre-existing concern, not created by this proposal. Any skill edit goes through `src/superclaude/` then `make sync-dev` — never `.claude/` directly, and not in this session.
