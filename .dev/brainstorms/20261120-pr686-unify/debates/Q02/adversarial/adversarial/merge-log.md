# Merge Log (Q02)

## Metadata
- Base: Variant 1 (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/adversarial/adversarial/variant-1-original.md`
- Incorporated from: Variant 2 (CLAY), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/adversarial/adversarial/variant-2-original.md`
- Plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/adversarial/adversarial/refactor-plan.md`
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/adversarial/merged-hybrid-position.md`
- Executor: merge-executor
- Changes applied: 7 of 7
- Status: complete
- Timestamp: 2026-11-20

## Changes Applied

### Change 1: Mechanism rewritten as an addendum to issue 687's rules
- Status: applied
- Before: a standalone guard list ("the script deletes the local branch only if ALL hold: ...") that sat beside issue 687's rules.
- After: the Mechanism says the order is issue 687's (save `.dev`, remove without `--force`, `git branch -d`, read back), issue 687's nine rules and "kept" handling stay, and the branch step adds exactly five numbered refusals. Claim and title reworded to match.
- Provenance: `Base (original, modified)`; `Variant 2 (CLAY), Mechanism and Claim - merged per Change #1`.
- Validation: no parallel guard list remains; all refusals point back to issue 687 rules 2 and 3.

### Change 2: Default and long-lived branch refusal kept and tightened
- Status: applied
- Before: "not the repo default branch (`master`) nor a long-lived branch (`integration`, `main`)".
- After: refusal 1 names `master`, `main`, `integration` and the `gh repo view` default. Facts 3 to 5 keep the measured `-d` deletions, the `origin/integration` SHA 141e97fe and the project flow. Merged PRs #664, #658 and #640 added with a plain description (merged PRs whose head is `integration`). Risk stated as latent.
- Provenance: `Base (original, modified) - keep and tighten wording per Change #2`.
- Validation: the facts about "no worktree on those names now" and "today's `integration` tip fails rule 3" appear only in the plan, not in either variant; they are marked UNVERIFIED in the merged text. The same applies to the PR list #664, #658, #640.

### Change 3: Open-PR guard replaced by one line in rule 2
- Status: applied
- Before: "no PR (any state) with this head is open and no open PR uses it as its base".
- After: refusal 2 is one added sentence in rule 2 (keep the branch if any PR with this head is OPEN). The "open PR uses it as base" guard is removed as speculative. The rule 2 wording gap ("newest merged ... when there are several") stays as fact 6, marked as not shown to occur in practice.
- Provenance: `Base (original, modified) - open-PR guard replaced ... per Change #3`.
- Validation: fact 6 no longer claims a hole; it says "not explicitly named".

### Change 4: Two guards removed
- Status: applied
- Before: "no other worktree has it checked out; the commit it points at is the merged PR's last head commit (`headRefOid`)".
- After: both removed from the list and recorded in a short "not added" paragraph. Reasons: git refuses a branch used by another worktree (measured, fact 7, from Variant 2 fact 6); rule 3 as written covers the head check, and an ancestor of the PR head holds no extra commit.
- Provenance: `Base (original, modified) - removed per Change #4`.
- Validation: "headRefOid" appears only in the removal note. Note for the reader: Variant 1 and Variant 2 say rule 3 needs HEAD to EQUAL the PR head, while the plan says "equals or is an ancestor of it". The merged text follows the plan and marks the ancestor wording UNVERIFIED against the issue text.

### Change 5: Dry-run branch column and logged PR head SHA
- Status: applied
- Before: dry run printed "branch: would delete / would keep (reason)" per row.
- After: refusal 4 keeps that column and adds the merged PR's head SHA so a branch can be recreated from `refs/pull/N/head`. The count "21 of 56 local branches have an upstream that is `[gone]`" comes from the plan only and is marked UNVERIFIED.
- Provenance: `Base (original, modified) - per Change #5`.
- Validation: the column is also named in the Cost line and in "What it gets right".

### Change 6: Never-force acceptance test and PR owner check
- Status: applied
- Before: Cost "About 4 tests"; no owner check; no acceptance test.
- After: refusal 3 requires the merged PR's `headRepositoryOwner` to be ours. Refusal 5 restates never `-D` and never `--force`, and reuses issue 687's acceptance test (fails on `--force`, `-D`, `rm`, `prune`, a push to anything but the evidence remote, a remote branch delete). Cost now says "Four added cases" and lists them. Risk notes the owner check may block a valid same-owner PR.
- Provenance: `Variant 2 (CLAY), fact 3 and advocate A-003 answer - merged per Change #6`; Cost: `Base (original, modified)`.
- Validation: the plan's phrase "its head SHA to match" could read as an exact match, which Change 4 removes. To avoid a contradiction it was written as "rule 3 then compares HEAD with that PR's head commit".

### Change 7: Meaning of `-d` corrected, rollout step added
- Status: applied
- Before: Claim called `-d` "a weak check" with no definition; no rollout step.
- After: Claim states `-d` means "merged to its upstream, or to the HEAD of the checkout the script runs in", not "its PR landed", so rules 2 and 3 are the gate and `-d` is the last backstop. The D13 reason ("`-d` refuses an unmerged branch") is stated as not relied on, due to the `feat-pushed` counter-case. Risk adds the report-only first week from issue 687's rollout ladder. The coordinator `--apply` question stays under a grant row (D13), not decided here.
- Provenance: `Base (original, modified) - rollout step and "-d" correction added per Change #7`.
- Validation: the original Claim sentence "delete nothing without `--apply` under a grant" was narrowed to match "not decided here" (dry run is default, `--apply` is the only way to remove; the grant is left open).

## Post-Merge Validation

### Structural
- Heading hierarchy: one `#` title, then `##` Claim, Mechanism, Cited facts, Cost, Risk, What it gets right. No gaps, base headings and order kept.
- Provenance: header comments (produced by /sc:adversarial, Base Variant 1 (OURS), merge date 2026-11-20) present; a `Source:` comment on every section and on each Mechanism block.
- Style: no em dashes or en dashes (grep confirmed). Issue 339 and issue 687 are explained at first use in the Claim; PRs #664, #658, #640 are explained in fact 5 and in this log. One residual: the title mentions issue 687 before the Claim explains it; the Claim explains it directly after.

### References
- "fact 3" (Claim, Risk) resolves to the `feat-pushed` measurement. "fact 7" (Mechanism) resolves to the Variant 2 measurement that git refuses a branch used by another worktree. "refusal 1" (fact 5) resolves to Mechanism item 1. All five Mechanism refusals and the numbered facts 1 to 10 are present and consecutive.
- Every fact in the merged text comes from the two variants or the plan; nothing was invented. Items found only in the plan are marked UNVERIFIED.

### Contradictions
- Re-scan found none. Two points were deliberately worded to avoid one: the exact `headRefOid` match is removed while the owner check still mentions the PR head commit (compared through rule 3), and the "grant" language in the Claim no longer promises a grant decision.
- Left unchanged on purpose: Variant 1 fact 5 said only rule 3 catches new commits. It still holds, because refusal 2 adds the open-PR check only.

## Summary
- Planned: 7
- Applied: 7
- Failed: 0
- Skipped: 0
- Validation: pass (structure, references, contradictions)
