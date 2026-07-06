<!-- Provenance: produced by /sc:adversarial --compare A,B,C --depth deep -->
<!-- Base: Variant C (Reject) -->
<!-- Merge date: 2026-06-04 -->

# Merged Verdict — Should `/sc:reflect` (or its agents) be wired into `/sc:auggie-review` and/or `/sc:cleanup-audit`?

## Bottom line

**No — do not incorporate the `/sc:reflect` skill, nor (after adversarial probing) the `evidence-validator` agent, into either protocol as a finding-stage verifier.** The winning position is **Proposal C (reject)**, strengthened by a Round 2.5 invariant probe that demolished the cheaper Proposal-A compromise it looked like the debate might land on.

- **Convergence:** ~0.82. Unanimous on reject-B; strong convergence on reject-the-`evidence-validator`-import once the probe ran.
- **The per-target answers differ only in their follow-up**, not in the core verdict: neither target should wire in reflect.

<!-- Source: Base C (original), sharpened by Change #2 (Variant B diagnosis) -->
## Why not — the mechanism-level reason (this is the decisive upgrade over the naive answer)

Both targets already run an independent verifier — auggie-review's **blind `auggie-reviewer`** (`auggie-reviewer.md:20`) + a non-negotiable inline file:line pass (`SKILL.md:204–207`); cleanup-audit's **`audit-validator`** 10% from-scratch re-test (`audit-validator.md:18`). The inquiry's motivating evidence (R0/PR#112 — `feedback_sc_reflect_vs_inline_rfqa.md`) is a **recall** failure: an applied fix that *looked* right but was wrong because a *finding was missing*.

The cheap candidate mechanism — the `evidence-validator` agent — is a **precision** gate: it re-Reads citations that *already exist* and drops the unfounded ones (`evidence-validator.md:21,121`). It **structurally cannot reproduce the R0/PR#112 catch**, because there is no false citation to drop when the defect is a *missing* finding (invariant probe INV-012). The only mechanism that delivers the recall property is reflect's heterogeneous-reviewer ensemble — i.e. **Proposal B** — whose 5–10× token cost (`integration-analysis.md:347`) is unjustifiable for a stage whose output a human gates and which never mutates code.

So: the expensive option (B) buys the right property at the wrong price for this stage; the cheap option (A) buys the wrong property. Neither clears the bar.

<!-- Source: Base C (original) + Change #3 (invariant probe INV-013/008) -->
## Per-target detail

### `sc:auggie-review`
- **Already a reflect consumer at the right seam:** the remediation chain invokes `/sc:reflect --type task --analyze` (Phase C, `SKILL.md:324`) and `--validate` (Phase E, `SKILL.md:327`) — reflect validates the *fix tasklist that actually mutates code*. That is where reflect belongs, and it is already wired.
- **The real, narrow gap (from Proposal A):** Wave-3 citation validation is a *same-context* inline Read (`SKILL.md:204–205`). This session's `:415`-vs-`:561` drift is a live existence proof that same-context passes miss real citation drift.
- **But do NOT import `evidence-validator` to fix it.** INV-003: the "re-ground via Grep instead of hard-drop" mitigation contradicts the agent's contract ("match or drop", `evidence-validator.md:121`; "do not propose new evidence", `:33,117`). INV-004: a paraphrased-but-correct finding becomes `snippet-mismatch` → dropped. INV-010: a Wave-3 drop is **irreversible** because `REVIEW.md` feeds `/sc:design` (`SKILL.md:322`), so the human never sees the dropped finding.
- **The dependency-free fix instead:** auggie-review *already* has a `needs-grounding` bucket that re-grounds via Grep/`auggie` then drops only on failure (`SKILL.md:203,207`) — the exact downgrade-then-drop behavior `evidence-validator` forbids. The narrow gap is closed by guaranteeing Wave-3's own re-Read is **fresh-context** and routing low-confidence citations through that existing bucket. **No new agent, no reflect dependency.** (Separate, optional follow-up task — not part of this verdict's "do nothing to reflect" conclusion.)

### `sc:cleanup-audit`
- **Reject `evidence-validator` and full reflect.** Reflect *internally reuses* `audit-validator` (`SKILL.md:561`) — the agent cleanup-audit already runs — so full reflect is circular (X-003). And a citation/grep re-check is **insufficient by construction** for the destructive defects that matter: CONSOLIDATE overlap-% errors and dynamic-loading false-negatives are *non-citation* defects (INV-013), and the worst case (a genuinely-dead file marked KEEP) lives *outside* the DELETE/CONSOLIDATE bucket (INV-008).
- **If hardening is ever wanted,** target the *existing* `audit-validator`'s content checks (classification accuracy, the dynamic-use checklist) — recomputing the FAIL denominator (INV-005) and the file-vs-finding counting base (INV-006). Still `audit-validator` tuning, **not** a reflect integration.

<!-- Source: Base C (original) -->
## The one condition that flips this verdict
If review/audit output is ever fed into an **auto-apply pipeline with no human gate**, recommendations become applied changes and the R0/PR#112 recall-failure mode reappears at full force. At that point Proposal B's heterogeneous-reviewer recall pass becomes justified. All three advocates — including A and C — agree on this exact boundary. It is not the current shape of either target.

## Answer to the literal question
- **The `/sc:reflect` skill:** No, for both targets.
- **A reusable reflect agent (`evidence-validator`):** No — the adversarial probe showed it is the wrong mechanism class for the only real gap and is contract-incompatible with the mitigation that would make it safe.
- **The genuinely useful residual:** auggie-review's Wave-3 citation validation should be made fresh-context using its *own existing* `needs-grounding` machinery — a dependency-free hardening that needs no reflect and no new agent.

## Concrete next step
This is a READ-ONLY investigation; **no skill file was edited.** If the auggie-review Wave-3 fresh-context hardening is pursued, it is a **separate task** that edits `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (Wave-3 step 3 region, ~`:204–207`) then runs `make sync-dev` — **not** `.claude/` directly, and **not** in this session. Recommend gating it behind the one-time backtest Proposal A itself proposed (measure the base rate of citation defects surviving Wave-3 over recent `REVIEW.md` files before committing the change).
