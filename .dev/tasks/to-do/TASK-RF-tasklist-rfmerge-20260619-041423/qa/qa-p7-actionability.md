# QA Report — Phase 7 Actionability / Clarity (doc-qualitative lens)

**Topic:** §49-65 Input-Contract reconciliation (sc-tasklist-protocol SKILL.md)
**Date:** 2026-06-19
**Phase:** doc-qualitative (lens: actionability / clarity)
**Fix cycle:** N/A (initial review)
**Fix authorization:** false (REPORT-ONLY)

---

## Overall Verdict: FAIL

The reconciled Input Contract (§49-65) is directionally correct — roadmap is
stated PRIMARY/required, `--spec`/auto-wired TDD/PRD are OPTIONAL supplementary,
and R-### traceability is explicit. The three VERIFY items the spawn prompt
named all pass on their face. BUT an adversarial read of the reconciled prose
against the four cited enrichment sites surfaces a cluster of clarity /
actionability defects: a flag-vocabulary mismatch that the new contract does not
reconcile, an unmentioned third resolution tier, a dangling internal reference,
and a precedence gap. None of these are auto-N/A; all bite a reader trying to
ACT on the contract.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| C1 | Input Contract internally consistent (roadmap PRIMARY required + `--spec`/TDD/PRD OPTIONAL) | PASS | §49-66: "one required input — the roadmap text"; "optional supplementary inputs"; "primary source of truth". Self-consistent. |
| C2 | No contradiction with four `--spec` enrichment sites | FAIL | Flag vocabulary diverges: contract says `--spec` (l.50,64); §3.x + §4.4a + §4.4b say `--tdd-file`/`--prd-file` (l.143,196,301). Contract never explains the `--spec` ↔ `--tdd-file`/`--prd-file` relationship. See I-1. |
| C3 | States every task must trace to a roadmap item (R-###) | PASS | l.60-62: "every task MUST trace to a roadmap item (R-### traceability)". Reinforced l.811-812, l.1222. |
| C4 | Resolution tiers in contract match Stage-10.5 resolution order | FAIL | Contract (l.62-66) names only roadmap + `--spec`/auto-wired TDD/PRD. Stage 10.5 (l.1594) defines a 3-tier order ending in "the roadmap itself, always present" — the contract's prose hides that the roadmap is ALSO the spec fallback. See I-2. |
| C5 | Internal cross-references resolve | FAIL | l.64 "pre-reflect spec resolution (§10.5)" — the section is labeled "Stage 10.5", and there is no bare "§10.5". Minor dangling ref. See I-3. |
| C6 | Precedence of supplementary inputs is actionable | FAIL | Contract is silent on TDD-vs-PRD precedence; §3.x l.156 defines it. A reader of the contract alone cannot predict enrichment behavior when both present. See I-4. |
| C7 | "auto-wired TDD/PRD from .roadmap-state.json" claim is accurate | PASS | §4.1c l.208-223 confirms auto-wire of `tdd_file`/`prd_file` from `.roadmap-state.json`. Claim grounded. |
| C8 | Back-reference "baseline behavior described in §3.x" is accurate | PASS | §3.x l.145 "Without source documents: The generator works from the roadmap alone (current baseline behavior)." Back-ref correct. |

## Summary
- Checks passed: 4 / 8 (C1, C3, C7, C8)
- Checks failed: 4 (C2, C4, C5, C6)
- Critical issues: 0
- Important issues: 2 (I-1, I-2)
- Minor issues: 2 (I-3, I-4)
- Issues fixed in-place: 0 (REPORT-ONLY)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | IMPORTANT | §49-66 (contract) vs §3.x l.143, §4.1b l.194/196, §4.1c l.210/219, §4.4b l.301 | **Flag-vocabulary collision the contract does not reconcile.** The reconciled contract names only `--spec` (l.50, l.64) plus "auto-wired TDD/PRD". But the enrichment sites it points to use a DIFFERENT flag surface: §3.x, §4.1b, §4.1c, and §4.4b all use `--tdd-file` / `--prd-file`. §4.1a treats `--spec` as a *TDD* path (detects TDD-format, aborts if not). A reader following the contract to its own cited sites finds three different flag names (`--spec`, `--tdd-file`, `--prd-file`) and no statement of how they relate — e.g. whether `--spec` is an alias for `--tdd-file`, or a separate path. The `argument-hint` (l.9) exposes ONLY `--spec`, deepening the confusion: a user cannot supply `--prd-file` per the documented invocation surface, yet §4.1b/§4.4b are "conditional on --prd-file flag". This is an actionability defect: the contract is the entry point and it cannot be acted on without cross-reading four sections and still guessing. | Add one sentence to the contract reconciling the flag vocabulary, e.g.: "The single user-facing flag is `--spec <path>` (a TDD or PRD spec); `--tdd-file`/`--prd-file` referenced in §3.x/§4.1b/§4.4b are the internal auto-wired forms resolved from `.roadmap-state.json`." If `--spec` and `--tdd-file`/`--prd-file` are genuinely distinct surfaces, state that distinction and align `argument-hint` (l.9) to expose all user-facing flags. |
| I-2 | IMPORTANT | §49-66 (contract) vs Stage 10.5 l.1594 | **Contract omits the roadmap-as-spec-fallback tier, contradicting the resolution order it cites.** The contract (l.62-66) frames spec resolution as a two-state world: supplementary TDD/PRD present (enrich) or absent (roadmap alone). But the `(§10.5)` resolution order it explicitly references is THREE-tier: "explicit `--spec` → auto-wired TDD/PRD from `.roadmap-state.json` → **the roadmap itself, always present**" (l.1594). The contract never states that the roadmap doubles as the pre-reflect spec fallback. A reader reconciling the two will see the contract say "the pre-reflect spec resolution (§10.5)" is a thing supplementary inputs feed, then find at §10.5 that the roadmap ALSO feeds it as terminal fallback — an unstated third path. | In the contract, after "the pre-reflect spec resolution (§10.5)", add: "(whose resolution order falls back to the roadmap itself when no `--spec`/auto-wired TDD/PRD is present — see Stage 10.5)." |
| I-3 | MINOR | §49-65 contract, l.64 | **Dangling internal cross-reference `(§10.5)`.** The label written is `§10.5`, but the document has no `§10.5` heading — the section is `### Stage 10.5` (l.1586) and is referred to elsewhere as "Stage 10.5" (l.759, l.1681) or "Stage-10.5" (l.1590). `grep "§10.5"` returns only this one authoring instance (l.64); every real anchor is "Stage 10.5". A reader searching for `§10.5` finds nothing. | Change `(§10.5)` → `(Stage 10.5)` to match the actual heading and the document's own naming convention. |
| I-4 | MINOR | §49-65 contract vs §3.x l.156 | **Contract is silent on TDD-vs-PRD precedence, which the cited section defines.** The contract lumps "auto-wired TDD/PRD" together as one supplementary class, implying symmetric treatment. But §3.x l.156 defines an asymmetric precedence: "When both are present, TDD-derived enrichment takes precedence for implementation specifics; PRD-derived enrichment shapes task descriptions, acceptance criteria, and priority ordering." A reader of the contract alone cannot predict enrichment behavior when both inputs are present and would assume symmetry. Not a hard contradiction (contract is silent, not wrong), but an actionability gap. | Add a half-sentence: "(when both TDD and PRD are present, TDD takes precedence for implementation specifics — see §3.x Precedence)." |

## Actions Taken
None — `fix_authorization: false` (REPORT-ONLY). All four findings documented above with exact locations and required fixes for the fix-cycle agent.

## Self-Audit
1. **Factual claims independently verified against source:** 9 — (a) §49-66 contract wording; (b) §3.x baseline-behavior sentence l.145; (c) §3.x precedence sentence l.156; (d) §4.1a `--spec`→TDD detection l.178-192; (e) §4.1b `--prd-file` l.194-206; (f) §4.1c auto-wire `tdd_file`/`prd_file` l.208-223; (g) §4.4a/§4.4b `--spec`/`--prd-file` conditionals l.278-324; (h) Stage 10.5 three-tier resolution order l.1594; (i) `argument-hint` flag surface l.9. Plus grep confirmation that `§10.5` has exactly one (authoring) occurrence and no matching heading, and that `--tdd-file`/`--prd-file` appear at l.143/194/196/210/219/301 while the contract uses only `--spec`.
2. **Specific files read:** `SKILL.md` (§47-90, §139-258, §278-368, §1586-1630), the phase-7-output-summary.md, plus two targeted greps over the whole SKILL.md for flag vocabulary and `§10.5` anchors.
3. **Why trust 4 issues, not 0:** I did NOT take the phase-7 summary's self-asserted acceptance criterion ("no longer contradicts the four `--spec` enrichment sites") at face value — I opened all four cited sites and the resolution order, and the flag vocabulary collision (I-1) and the hidden third resolution tier (I-2) are exactly the kind of "reconciled prose still contradicts its own referents" defect the adversarial stance demanded. Each finding cites concrete line numbers in both the contract and the conflicting site.
4. **Web research:** None performed; this review is entirely local-file-bound. No Tavily/fallback engagement required.

## Confidence
Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 4 | Grep: 3 | Glob: 0 | Bash: 3 (grep-bearing)

## Recommendations
- This is a FAIL. Route I-1 and I-2 (IMPORTANT) plus I-3 and I-4 (MINOR) to a fix-cycle. Per the no-leniency / all-severities-must-resolve rule, none are exempt.
- I-1 is the highest-leverage fix: the contract is the document's entry point, and the `--spec` vs `--tdd-file`/`--prd-file` vs `argument-hint` three-way split is the single most likely thing to mislead a user trying to invoke enrichment.
- NOTE (scope): the flag-vocabulary collision (I-1) and the `argument-hint` gap pre-existed this phase's edit — Phase 7 was a bounded doc-consistency edit and did not introduce them. But the phase's own acceptance criterion #4 ("no longer contradicts the four `--spec` enrichment sites") is NOT met while the collision stands, so they are in-scope for this actionability lens.

## QA Complete
