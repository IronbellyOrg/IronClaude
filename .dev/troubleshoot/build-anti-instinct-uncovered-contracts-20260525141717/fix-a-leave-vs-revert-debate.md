# Fix A — Leave vs Revert: Adversarial Debate

**Question:** Should the Fix A edit at `TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md:396` (COMP-007 row) be left in place, or reverted now that Fix B has landed in IronClaude's `integration_contracts.py`?

---

## Round 1 — Opening Statements

**Position A (LEAVE).** Steelmanned opposition first: yes, the roadmap is LLM-generated and edits-after-the-fact create a divergence between the prose and the generator. Granted. But the Fix A edit is *content-faithful* — the hub package genuinely does populate the dispatch table at init; the original prose was simply less explicit. The expanded phrasing ("populates the dispatch table with class-priority runners (Interactive/Coalescible/Bulk)") is materially better roadmap prose for a human maintainer, independent of any gate. There is zero ongoing cost to leaving it: it doesn't break regeneration (regeneration overwrites it anyway), it doesn't lie, and it improves downstream readability. Reverting is pure cosmetics with negative information value.

**Position B (REVERT).** Steelmanned opposition first: yes, the new prose is more explicit and content-faithful, and a future human reader is marginally better off. Granted. But the edit was made *to satisfy a tool that has since been fixed properly*. Fix B's three-layer coverage (`dispatch_family` regex, stem-fallback with identifier-overlap, `populate` in `impl_verbs`) was explicitly verified in Step 4.3 to green the gate with `uncovered_contracts=0` *without* Fix A. That makes Fix A a workaround whose justification has evaporated. Leaving it converts a transient unblock into permanent "scar tissue" in the consumer roadmap — a precedent that says "when the tool misbehaves, edit the artifact." That precedent is the actual cost, not the line itself.

## Round 2 — Rebuttals

**A → B:** "Scar tissue" assumes the edit is visibly a workaround. It isn't — it reads as ordinary roadmap prose. No future maintainer will look at line 396 and infer "this was a gate-appeasement." There is no precedent because there is no visible scar.

**B → A:** The precedent is in the *session record and commit history*, not the prose. The reason this debate exists is precisely that we know Fix A's provenance. Leaving it normalizes "edit the artifact to unblock the tool" as a resolution pattern, which is exactly the anti-pattern Fix B was built to make unnecessary. The whole point of investing in Fix B was to *not* need Fix A.

## Round 2.5 — Invariant Probe

| Assumption                                           | Position A                          | Position B                                |
|------------------------------------------------------|-------------------------------------|-------------------------------------------|
| TUIBBS-scp roadmap regeneration model                | Edits survive until regen; harmless | Edits are tech debt against the generator |
| IronClaude ↔ TUIBBS-scp relationship                 | Tool serves consumer; prose wins    | Tool is SoT for contract semantics        |
| Cost of "scar tissue"                                | ~0 (invisible in prose)             | Real (precedent in workflow memory)       |

The crux is the **second row**: does the gate-coverage logic in IronClaude *define* what the roadmap must say, or does the roadmap define what the gate must accept? Fix B chose the latter (broaden the gate). Fix A chose the former (narrow the prose).

## Synthesis — Recommendation: **REVERT Fix A.**

Fix B was built precisely so the gate accepts the original prose. Keeping Fix A contradicts the design intent of the Fix B work just completed and leaves an unattributed workaround in a consumer roadmap. The "improved readability" argument is real but weak — if explicit dispatch-table wiring is genuinely better roadmap prose, that belongs in TUIBBS-scp's *roadmap generator prompt*, not as a post-hoc edit to a generated artifact. Revert now while the change is isolated, single-line, and traceable; if the explicit phrasing is wanted long-term, raise it upstream in TUIBBS-scp's generation path.

**Condition under which LEAVE would win:** if TUIBBS-scp's roadmap is *not* regenerated (i.e., it is hand-maintained from this point forward), the SoT argument collapses and Fix A becomes a normal prose improvement. Verify regeneration status before reverting.
