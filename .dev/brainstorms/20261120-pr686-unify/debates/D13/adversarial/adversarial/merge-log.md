# Merge Log: D13 hybrid position

## Metadata

- Base: Variant 2 (CLAY), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D13/adversarial/adversarial/variant-2-original.md`
- Other inputs: Variant 1 (OURS) `variant-1-original.md`, `refactor-plan.md`, `debate-transcript.md` (all in the same folder), and the orchestrator-verified facts on `WORKER-CONTRACT.md` lines 236, 237, 241 and 289 and on `sc-closeout-protocol/SKILL.md` lines 20, 85 and 86
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D13/adversarial/merged-hybrid-position.md`
- Executor: merge-executor
- Changes applied: 6 of 6 planned (Changes 1 to 6)
- Status: complete, with four items for the orchestrator (see Summary)
- Date: 2026-11-20
- Tag convention: in `Source: Variant 1 (OURS), fact N`, N is the number in the original Variant 1 file. In the merged file, facts 1 to 6 are new and base facts are renumbered 7 to 15.

## Changes Applied

### Change 1: Rewrite the Claim to the agreed HYBRID

- Status: applied
- Before (base): the three pieces are complementary; closeout becomes wave 8; cleanup is the safe removal; "Removal is a script run by an opt-in automation with no agent, not by the orchestrator".
- After: none is retired; the coordinator is the accountable owner of the close chain (sweep, settle, cleanup) per the owner's 2026-11-05 comment; closeout is a coordinator step; the nine-rule script of issue 687 performs removal and the coordinator runs it (list or dry run each cycle, apply only under a grant); local branch deletion is `git branch -d` inside the script, remote branch deletion stays human-only; the PR log stays a separate reporting tool; issue 687 is not delayed. The blanket "never removes" rule is gone (plan item 3 of "Changes NOT Being Made").
- Consistency edits that follow from this change and are not literal plan text: the third "What it costs" bullet (the blanket rule is narrowed), and cited fact 14 (the old text said line 628 and line 139 make branch deletion human-only without scope; it now says line 139 is the `--delete-branch` rule, line 628 sits in wave 9, and which source governs local branch deletion is not verified).
- Provenance tag: `Source: Base (original, modified) - Claim replaced with the agreed hybrid per Change #1 ...`
- Validation: the Claim has no "never removes" statement left; its pointers (facts 2, 9, 10, 14, open items 1 to 3) resolve.

### Change 2: Add the owner's duty text as the first cited facts

- Status: applied
- Before: base facts started at PR 683.
- After: new facts 1 (issue 339 body), 2 (comment 2026-11-05 13:43Z) and 3 (status review 2026-11-17) at the top, quoted from Variant 1 facts 1, 2, 3. The long `sc:close` quote in fact 1 comes from Variant 1's Mechanism section.
- Side effect: base fact 4 (same status review) became fact 10 and now opens with "The same status review as fact 3 says", so the review is not cited twice as if separate.
- Provenance tags: `Source: Variant 1 (OURS), fact 1 / 2 / 3 - merged per Change #2`
- Validation: all three items are present, in order, ahead of the base facts.

### Change 3: Add the sweep and the contract facts

- Status: applied
- Before: base fact 9 covered `/sc:sweep` only as read-only.
- After: fact 4 (PR 539, WC-16 at `WORKER-CONTRACT.md` line 289, row 1.3 of `H-design681-map.md`, the quote "The coordinator decides and performs any action under those rules"); fact 5 (lines 236 and 237: the coordinator may merge the child branch, remove the child with `orca worktree rm` and delete its branch, with the quoted keep conditions, and the gap that issue 687 fills); fact 6 (line 241: outward actions only when the user's instruction names them). Base fact 9 became fact 15 and now points to fact 4.
- Provenance tags: `Source: Variant 1 (OURS), fact 4 - merged per Change #3`; `Source: Debate transcript, orchestrator note ... - merged per Change #3` (facts 5 and 6, which have no Variant 1 counterpart).
- Validation: the quoted text matches the debate transcript word for word. Two deliberate trims, see Summary items 1 and 3.

### Change 4: Add the unstated assumptions as open items

- Status: applied
- Before: no such section.
- After: new `## Open items before adoption` after `## What it risks`, with three numbered items: (1) the written mapping of "orchestrator" in issue 339, "orchestrator" in the design of PR 681 and "coordinator" in the contract; (2) the script counts as the coordinator's act only if the automation is opt-in and the coordinator owns schedule, grant and report; (3) closeout's writes need a named grant row per line 241. An intro line says both advocates answered QUALIFY.
- Provenance tags: `Source: Debate transcript, A-001 / A-002 / A-003 - merged per Change #4` (the items come from the diff analysis and the advocates' answers, not from a Variant 1 fact, so the Variant 1 tag form does not fit).
- Validation: the section sits between `## What it risks` and `## What it gets right`; the base keeps its six sections plus this one, as the task asked.

### Change 5: Fix the base's weaknesses found in scoring

- Status: applied
- Before: ADD5, D18, Orca and wave 8 used without explanation; "orchestrator" used for the role; risks stated with no mitigation.
- After: wave 8 glossed in the Claim (closeout, then the audit, then the report entry); Orca glossed in the Mechanism ("the worktree and task manager"); ADD5 glossed in fact 14 (the design rule that bans `--delete-branch` on `gh pr merge`); D18 glossed in the first risk (the closeout spec's item on a model reading criteria to decide "done"). "Coordinator" is used throughout, with one sentence in the Claim saying the design of PR 681 calls the role "orchestrator". Mitigations added: for a wrong `done`, closeout's `unclear` escalation and `left_open` hand-back (a `not_done` verdict leaves the issue open with one note, an unclear case is escalated; `SKILL.md` lines 20, 85 and 86), with a plain statement that these do not catch a wrong `done`; for the missing approval, the owner's decision given in chat.
- Provenance tags: `Source: Base (original, modified) - glosses and mitigations per Change #5 ...`
- Validation: each term is glossed at its first use in the document. "Orchestrator" remains only in file names, quotes, the owner's wording, and the mapping sentence.

### Change 6: Add the OURS risk

- Status: applied
- Before: two risks.
- After: a third risk: if the coordinator, a model session, may delete worktrees on its own judgment, a defect in its checks can destroy unpushed work; the issue 687 incident of 2026-11-20 (two of sixteen hand-removed workspaces belonged to open issues #354 and #419). One closing sentence says the position avoids it by letting the nine-rule script decide each removal.
- Provenance tag: `Source: Variant 1 (OURS), risks - merged per Change #6`
- Validation: the numbers match issue 687 as cited in fact 11.

## Post-Merge Validation

### Structural integrity

- Heading hierarchy: one `#` title (renamed from "Position CLAY" to "Position HYBRID", an editorial change so the title does not mislabel the merged position), then seven `##` sections in this order: Claim, Mechanism, Cited facts, What it costs, What it risks, Open items before adoption, What it gets right. No skipped levels, no stray `###`.
- Provenance: four header comments at the top, and every `##` section carries a `Source:` comment; each cited fact carries its own end-of-line tag.
- Formatting: no em dashes, no en dashes, no leftover placeholder.
- Result: pass.

### Internal references

- Single-number "fact N" references in the text: 10 (Claim 4, fact 10, fact 14, fact 15, costs 2, open item 3), all resolve to facts 1 to 15.
- "Open item" references: 3 (Claim: open item 1, open items 2 and 3), all resolve to open items 1 to 3.
- Provenance tags that cite a Variant 1 fact (1 to 4): 4, all resolve in `variant-1-original.md`. Tags that cross-reference merged facts 3 and 4: 2, both resolve.
- "Change #N" references in tags: 22 (21 matched tokens plus the bare "#3" in "Changes #2 and #3"), all within Changes 1 to 6 of the plan.
- Header range statements ("facts 1 to 4" of Variant 1; merged "facts 1 to 6" and "7 to 15"): 3, all correct.
- Total: 44 references, 44 resolved, 0 broken.

### Contradiction re-scan

- Narrowed "never removes" rule versus `WORKER-CONTRACT.md` lines 236 and 237: no new contradiction. The merged text has no blanket statement that the coordinator or orchestrator never removes worktrees. Lines 236 and 237 are quoted as fact 5 and presented as a bounded coordinator duty for child worktrees. The other "never" statements are scoped: closeout "never deletes anything" (its own Will Not Do, fact 8), and the script's "never `--force`, never `git branch -D`, never `rm`" (fact 12). Neither covers what lines 236 and 237 allow the coordinator to do.
- Cost bullet 3 and fact 14 now say line 628 is a wave 9 statement about the issue worktree, and fact 5 says the contract does not cover issue worktrees of merged work. These agree.
- Residual tension, present in the plan and not created by the merge: the Claim says deleting a branch stays a local `git branch -d` inside the script, while fact 14 quotes ADD5 ("deleting branches is human-only, rule 1") and the debate left it unverified whether ADD5 or the owner's 2026-11-05 comment governs. The merged text states both and says it is not settled; it does not pick one. See Summary item 2.
- No other new contradiction found. The old claim that each of the three pieces fills a 339 gap (false for the PR log, see fact 13) was dropped when the Claim was replaced.

## Summary

- Planned: 6
- Applied: 6
- Failed: 0
- Skipped: 0
- Validation: pass (structure, 44 of 44 references, no new contradiction)

Items for the orchestrator, not resolved by the merge:

1. The plan says lines 236 and 237 have "six keep conditions". The transcript quotes five (unmerged commits, an open PR, uncommitted changes, an unfinished `/sc:implement` ledger, a report it has not read). The merged fact 5 gives the quoted list and no count. If a sixth condition exists on those lines, fact 5 needs it added.
2. The plan's "Deleting a branch stays a local `git branch -d` inside the script" is not in the base. Issue 687 only bans `git branch -D`, and advocate 2 conceded in the debate that Clay's cleanup does not meet 339's branch deletion and that branch deletion "stays a human step". The merged Claim follows the plan and adds the pointer "not settled (fact 14)". An owner ruling is still needed.
3. Variant 1 fact 4 also says "Clay's design never mentions sweep". It was not copied: the plan's Change 3 content did not list it, and no advocate checked it. It can be added if wanted.
4. The Claim points to "open items 2 and 3" for the grant on the apply step. Item 2 covers the grant for the script and item 3 covers the grant row for closeout's writes, so the pointer is slightly wider than item 3's text. Both come straight from the plan's A-002 and A-003.
