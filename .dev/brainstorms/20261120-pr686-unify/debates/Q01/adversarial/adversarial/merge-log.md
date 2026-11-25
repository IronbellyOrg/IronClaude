# Merge log (Q01)

## Metadata

- Base: Variant 1 (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q01/adversarial/adversarial/variant-1-original.md` (read only, not modified)
- Non-base source: Variant 2 (CLAY), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q01/adversarial/adversarial/variant-2-original.md`
- Refactoring plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q01/adversarial/adversarial/refactor-plan.md`
- Executor: merge-executor
- Changes applied: 8 of 8 planned
- Status: Complete, no escalation needed
- Timestamp: 2026-11-20
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q01/adversarial/merged-hybrid-position.md`

## Changes Applied

### Change 1: Widen the claim to the three consents the topic names
- Status: Applied
- Before (base Claim): "A per-issue grant row is the owner's own consent for one named issue and one named list of writes."
- After: "A per-issue grant row, and the other per-action consents named in the Scope section below, are the owner's own consent for one named action and one named list of writes." Plus new `## Scope` section: "Three consents are in scope: the per-issue grant row, the owner go for `--apply`, and the owner approval of the cleanup design (issue 687)."
- Provenance tag: Variant 2 cited fact 8 (D13 and D04 verdicts); Base (original, modified) for the Claim opening
- Validation: Scope placed directly after Claim, as the plan says. Both new references (Scope, cited fact 1) resolve.

### Change 2: State which record governs, mark owner intent as the one open point
- Status: Applied
- Before (base Claim): "The owner's later order (2026-11-17) fixes the mechanics ..."
- After: "Which record governs: the owner's order of 2026-11-17 ... governs the mechanics." Decision 8's "written by the owner" is read as "owner-sourced, never agent-created". "Open point, UNVERIFIED: whether the owner's 'narrow d2' (11-17 04:46) was meant to restore an owner-written file row ... One chat confirmation from the owner settles it."
- Provenance tag: Base (original, modified); reason: the base listed the line-57 conflict as a risk and never ruled. The word "later" was dropped because the order of the owner's messages that day is not shown.
- Validation: owner intent is labelled UNVERIFIED. No new facts or citations added.

### Change 3: Checks on the recorded go, adopted from `answer-check`
- Status: Applied
- Before: Mechanism had three steps and no check on the recorded go.
- After: Mechanism step 4 with four tests (typed by a person in their own session and not relayed; names the right entry or issue; newer than the entry's last edit; question key matches, `merge_safety:<PR>:<head sha>`), owner identity as a parameter (D:694 names Clay), and a fallback that refuses a go without quoted words, date and exact scope. Marked "designed but not built (PR B, D:1020)".
- Provenance tag: Variant 2 mechanism step 4 (D:694, D:598), Change 3
- Validation: every citation (D:694, D:598, D:1020, D04 verdict) was copied from Variant 2 or the base.

### Change 4: Give a recorded go an end and a revocation path
- Status: Applied
- Before: no end or revocation stated.
- After: Mechanism step 5: ends when the named action is done; for a merge also when the PR head moves; also when the owner revokes it in chat.
- Provenance tag: Variant 2 key binding (D:598) plus the base-side Task-end precedent as cited in the plan (contract line 245), Change 4
- Validation: step 5 refers to the key in step 4, which exists.

### Change 5: Fail-closed default and use log
- Status: Applied
- Before: none.
- After: Mechanism step 6: no recorded go means no write; each use names the go it relied on; cites D:696 and `repos.py:295` in pr-a.
- Provenance tag: Variant 2 cited facts 3 and 4, Change 5
- Validation: "pr-a" was added to the Abbreviations line (copied from Variant 2) so the citation is defined.

### Change 6: Which consents are standing and which are per action
- Status: Applied
- Before: none.
- After: in `## Scope`, four low-stakes writes are covered by standing grants per the D04 verdict (named from Variant 2's list: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold`); merge, close, `--apply` and the cleanup-design approval are per-action chat goes. The text says point C-002 stayed unresolved in the debate and claims no debate win. The old row has no reader in master since PR 682 (cited fact 7), so the question is reframed as "who records a per-action owner go".
- Provenance tag: Variant 2 mechanism step 1 and cited fact 1 (D:291, D:872, D:116); base cited facts 7 and 8
- Validation: the naming of the four entries is read off Variant 2's six-entry list minus `pr.merge` and `issue.close`; it is not a quote from the D04 verdict. Flagged here so the reader can check it.

### Change 7: Add Variant 2's separable risks
- Status: Applied
- Before: three risks.
- After: three risks added: same-host terminal problem (U37, D:1295); `grants` file inside the orchestrator's write reach (D:688), with the recorded-go ledger noted as likewise writable by its keeper; `E-NO-GRANT` covers at most two of six entries (D:696, D04 verdict item 6).
- Provenance tag: Variant 2 What it risks, Change 7 (reworded to fit this mechanism)
- Validation: citations match Variant 2 exactly.

### Change 8: Correct two statements in the base
- Status: Applied
- Before (fact 7): "a grep of master for 'grant row' finds only `WORKER-CONTRACT.md:57` and `docs/designs/issue-pipeline-fu1.md:24,26`". Before (fact 8): "contract lines 241 and 245" refuse bulk standing grants (stated in fact 8 and in What it gets right).
- After (fact 7): the grep also finds `docs/designs/orchestrator.md:116`. After (fact 8): line 241 requires the user's instruction to name the outward action; line 245 says no pre-authorization waives a push; the "no standing merge and close" conclusion comes from the D04 verdict. The matching sentence under "What it gets right" was corrected the same way.
- Provenance tag: Base (original, modified); reason: both scorers found the original wording overstated
- Validation: no remaining text says lines 241 and 245 refuse bulk standing grants.

### Changes NOT made (honoured)
- C-005 (standing `pr.merge` and `issue.close`): not adopted.
- C-003 (`E-NO-GRANT` as main control): not adopted; the text says it is not relied on.
- C-001 ("no record at all"): not adopted; a durable recorded go stays.
- S-001, S-003 (reorder to Variant 2's fact order): not done; base order kept.
- A-002 (declare the row question moot): not adopted; reframed instead.
- X-001 (restore an owner-written file row): not adopted; owner intent left as one UNVERIFIED chat confirmation.

## Post-Merge Validation

- Structural integrity: pass. One H1; H2 sections in order: Claim, Scope, Mechanism, Cited facts, What it costs, What it risks, What it gets right. The base's Abbreviations line is kept before Claim. No skipped heading levels.
- Internal references: total 4, resolved 4, broken 0 (Claim to Scope section; Claim to cited fact 1; Scope to cited fact 7; Mechanism step 5 to step 4).
- Provenance: header comment present (Provenance, Base, Merge date 2026-11-20); every section or block carries a `<!-- Source: ... -->` comment.
- Style: no em dashes in either file.
- Contradiction re-scan: new contradictions introduced: 0. The merged Claim says the owner is never asked to write a file and that the agent records the row from chat. It does not say the owner writes the row. The phrase "written by the owner" appears only inside a quotation of Decision 8 and of contract line 57 (cited facts 1 and 3), and the Claim reads Decision 8 as "owner-sourced, never agent-created". The remaining conflict, between contract line 57 and the chat rule, is the one the base already named under What it costs and What it risks.
- Open items carried forward: owner intent on "narrow d2" is UNVERIFIED; the debate point C-002 is unresolved; the checks in step 4 are designed, not built.

## Summary

- Planned: 8
- Applied: 8
- Failed: 0
- Skipped: 0
- Not-made table: 6 rows honoured
