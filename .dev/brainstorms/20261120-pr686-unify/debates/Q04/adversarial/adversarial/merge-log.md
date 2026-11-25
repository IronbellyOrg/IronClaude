# Merge Log: Q04 (push go)

- Base: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/variant-1-original.md`
- Plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/refactor-plan.md`
- Incorporated variant: `variant-2-original.md` (same folder)
- Merged output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/merged-output.md`
- Merge date: 2026-11-20

Layout note: the plan inserts new Mechanism items in the middle (Change #3 after item 1, Change #4 as a new item). The merged Mechanism is numbered 1 run line (#1), 2 fence (#3), 3 classes outside the run (#4), 4 end of a go (#2), 5 Full Submit (#5).

## Change #1: Claim and Mechanism rewritten so fix-round pushes are covered by the run line

- Status: applied
- Before: Claim said a typed go is needed for each push class, bound to the exact sha; Mechanism 1 said a push go names repo, branch and the sha to be pushed; Mechanism 2 gave the fix-round push its own go.
- After: the Claim says the typed `/sc:pr-submit --monitor 3` line (or the Full Submit field) is the go for the first push, the PR and the fix-round fast-forward pushes of one run; sha binding stays only for a push after a rebase and for the merge. Mechanism item 1 states the run line as the go and cites `SKILL.md:291, 308`. The title was reworded because "bound to the head sha" no longer holds. Cited fact 8 was reworded for the same reason (head-sha pin for the rebase push only), and the base risk bullet 1 ("must say plainly the run line is the go") is now the Claim itself.
- Provenance tags: `Variant 2 (CLAY), Claim - merged per Change #1`; `Variant 2 (CLAY), Mechanism 2 - merged per Change #1`; `Base (original, modified)` for the title and cited fact 8.
- Validation: no sentence left that gives a fix-round push its own go; fact 8 no longer says head-sha binding extends to push in general.

## Change #2: End of a go

- Status: applied
- Before: Mechanism 3 "A go is consumed by the push it names and is void when the branch head moves to a sha it did not name."
- After: Mechanism item 4: the run go ends when the run ends, when the PR is merged or closed, or when the head moves to a sha outside the run; the base sentence is kept for a go that names a sha (rebase push, merge).
- Provenance tag: `Base (original, modified) - ... merged per Change #2`.
- Validation: PR 368 stays cited in cited fact 6 (unchanged, with the memory note "not re-verified").

## Change #3: Mechanical fence as the condition of the run go

- Status: applied
- Before: no fence in the base Mechanism (only cited fact 7 on gates).
- After: Mechanism item 2: one fix commit per cycle, `push_range_mismatch` halt, fast-forward only with parent checks (`pr-submit.md:121`, `SKILL.md:342-348`), no force push, no push to the default or protected branch, `push_count <= max_rounds + 1` (`SKILL.md:262`), `max_rounds` default 2, hard cap 5 (`pr-submit.md:47`). Cited fact 10 (CLAUDE.md "pushes the fixes without asking"; `pr-submit.md:38`) was added from Variant 2 fact 3.
- Provenance tag: `Variant 2 (CLAY), cited facts 3 and 4 - merged per Change #3` (both item 2 and fact 10).
- Validation: every fence item appears in the "Tests that can check it" list or the per-class line of the last section.

## Change #4: Classes outside the run

- Status: applied
- Before: Mechanism 2 listed the push classes each with its own go.
- After: Mechanism item 3: a manual or coordinator push without `/sc:pr-submit`, a push after a revert, a push after a rebase (old and new sha; the tool never rebases or force-pushes), a new run on the same PR, and a merge each need a new typed go; a push by any other actor is covered by no go (SEC-13).
- Provenance tag: `Base (original, modified) - ... merged per Change #4`.
- Validation: matches the rule sentence in the last section.

## Change #5: Full Submit narrowed, worker route closed

- Status: applied
- Before: Mechanism 4 "Full Submit field value ... is the one owner-recorded standing go, for that issue's first push and PR only (R25)"; cited fact 2 without ADD1; cited fact 9 said "nothing else is pushed".
- After: Mechanism item 5: the field is the go for the first push, the PR and the loop pushes of the one run it starts, in a top-level session, never a merge, force push, branch deletion or other push; ADD1's worker route stays rejected (D06 item 5; WC:23, WC:244); the WC:245 amendment is worded so it is not an "earlier pre-authorization". Cited fact 2 gained the ADD1 sentence (D:135, from Variant 2 fact 1). Cited fact 9 reads the R25 go as covering the one run and says the R25 wording has to be amended.
- Provenance tags: `Base (original, modified) - ... merged per Change #5` on item 5 and on cited facts 2 and 9.
- Validation: the exact "no earlier pre-authorization" quote in cited fact 1 is untouched.

## Change #6: What it costs and What it risks

- Status: applied
- Before: cost was one prompt per push class, up to 5 per-fix-push prompts; risks were the literal-reading contradiction with CLAUDE.md, a sha-bound go impossible in an unattended loop, and sha binding on push being OURS extended.
- After: costs are one go per run (up to 5 prompts removed), a new go for each class outside the run, and a go record, end-of-run check and sha check still to build. Risks are: a script can type the run line (D06 INV-003); a worker script's own push is covered by no go (SEC-13, D:117); head moved outside the run; sha-bound fix-round push is OURS extended and not in D06 or Q01; a bad fix push is caught only at the merge go, so the merge go stays sha-bound (merge-time controls from Variant 2 fact 7, D06 items 1, 2, 4).
- Provenance tags: `Base (original, modified) - ... merged per Change #6` on both sections.
- Validation: the plan's debate point ids (A-001, A-005, X-003, U-007 and so on) were not copied into the text because a reader of the merged file has no key for them; the facts they stand for are stated in words.

## Change #7: Resulting rule and rows

- Status: applied
- Before: no final rule section.
- After: new final section "Resulting rule and rows" with sub-headings The rule, Per push class, Tests that can check it, Rows to change in SPEC.md, WORKER-CONTRACT.md lines touched. The rule, per-push-class and tests paragraphs are copied verbatim from the orchestrator text. Rows listed: lines 124 and 467, FR-32 (line 233), SEC-15 (line 302), section 13.2 probe row (line 699), new row SEC-22, SEC-01 (line 288). WORKER-CONTRACT lines: 245 amended, 23 and 244 unchanged.
- Provenance tag: `Variant 2 (CLAY), Claim and Mechanism - merged per Change #7`.
- Validation: the rule sentence was compared by eye against the supplied text and matches. FR-32 and the 13.2 row got one short clause each ("restate the push clause to match THE RULE above"; "checked by the tests above") because the orchestrator text named the row but gave no wording; no new facts were added.
- Issue to report: the instruction says "the five WORKER-CONTRACT.md lines it touches" but names only three (245, 23, 244). Only those three are listed; I did not invent two more. The orchestrator should supply the other two if they exist.

## Post-Merge Validation

- Heading hierarchy: one H1, then H2 sections (Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right, Resulting rule and rows), then H3 only under the last H2. No gaps.
- Internal references: "Mechanism item 5", "item 3", "item 4", "cited fact 5", "the tests in the last section", "SEC-15 in the last section" all resolve to existing items or sections. SEC-22 is a row to be added to SPEC.md and is named as new in the rows list. The Notation line still defines WC, D and SPEC.
- Dash check: no em dashes or en dashes in the merged file (searched).
- Sentences that still say each fix-round push needs its own go: none. The only hit for "fresh go per fix-round push" (cited fact 10) says such a go is incompatible with the mandatory PR path.
- New contradictions or tensions introduced (not fixed, since the plan did not authorize more edits):
  1. Cited fact 9 quotes the owner's R25 text "nothing else is pushed", while the merged rule lets the same go cover the run's fix-round pushes. The fact states that the R25 wording must be amended; SEC-15 carries that.
  2. The Full Submit field is set on the issue before the run, which is close to the "earlier pre-authorization" that WC:245 refuses. The SEC-15 row says the go is "given in the live session at the time of the run" as the orchestrator instructed; whether a field set ahead of time meets that is a point for the spec owner.
  3. Cited fact 7 says the push is "a named, separately granted capability"; read with item 1 it means separate from merge and gated by ordinal, not a separate go per push. Left as base text.
  4. "What it gets right" bullet 1 ("nothing publishes unseen commits without a person") is base text and is compatible because the run line is a person's typed go; not edited, since the plan lists no change there.
  5. The "five" vs three WORKER-CONTRACT lines count mismatch (see Change #7).

## Summary

- Planned: 7
- Applied: 7
- Failed: 0
- Skipped: 0
