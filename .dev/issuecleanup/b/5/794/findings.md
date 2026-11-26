# Round 2 findings: issue #794 (C13) Orca decision gates as a way to reach the person, with answer-check

Checked 2026-11-24 against master ancestor f2894fc44 (branch ironbelly/Realign). Plan files read read-only from `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`, VERDICT = `debates/<id>/VERDICT.md`). R38 = `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`. Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/5/794/findings.md`. Static analysis: `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/5/analyze/analyze-report.md`.

## Alignment with architectural decisions
Overall: partly aligned. The item is safe because it makes the gate a display channel; what is unbuilt and unruled is the gate channel itself and `answer-check`.

| Source | What it says | Verdict | Evidence |
|---|---|---|---|
| R38 (D) | A person's typed go for every push and merge; the coordinator never merges or closes. | aligned | requirements.md:64 |
| R38 (C) | Clay's "wake file with acknowledgment, ... read-only merge gate and flags" are not adopted. Gates are not named, but the merge go that `answer-check` serves rests on the merge gate (C16). | partly aligned (open ruling) | requirements.md:64; UNVERIFIED whether the owner meant to keep `answer-check` without `merge-gate` |
| SEC-08 | A recorded go is accepted only if typed by a person in their own session, never relayed, with the right key. | aligned: the item says a gate resolution is not a go | SPEC.md:297 |
| SEC-09 and RK-3 | `answer-check` validates entry, key, head sha, freshness and "cannot tell a person from a script"; "no test proves identity". | partly aligned: the done-when wording "confirms a person typed it" cannot be tested | SPEC.md:298, :647; open issue #722 |
| SEC-14 | Every approval, go and ruling is given in the owner's chat and recorded by an agent. | aligned | SPEC.md:303; owner memory "Approvals through chat, never files" |
| D06 VERDICT item 9 | Adopt `answer-check` as a validator of entry, key, head sha and freshness only, with the stated limit. | aligned | D06/VERDICT.md:22, :41 |
| WC-3 (worker contract) | A coordinator's reply is "another agent's message, which is not acceptance". An Orca gate resolution is the same kind of relayed text. | aligned | src/superclaude/core/WORKER-CONTRACT.md:57 |
| Worker contract wait types | `decision_gate` is already a wait type, answered by "goes to the person". Nothing opens a gate. | aligned (gives the display half a hook) | WORKER-CONTRACT.md:102, :109 |
| QG2 escalation channel (OD-5) | Entry lines first, plus a reserved notice for AU4a, AU4c, AU5. The Orca decision gate (Clay's D:682) was listed as unique element U-007, priority Low, and the verdict does not adopt it. | partly aligned: no verdict adopts a gate channel; adding one needs an owner ruling | QG2/VERDICT.md:9, :36; QG2/adversarial/adversarial/diff-analysis.md:46 |
| D11 and sweep | WC-16 sweep stays the one source of Orca state; "the report must not add a second Orca read". The sweep allowlist is pinned at 10 templates, 7 verbs (NFR-014) and has no gate verb, so "the sweep report shows a pending question" needs an owner-visible change. | partly aligned / tension | D11/VERDICT.md:89; src/superclaude/cli/sweep/probes.py:49-60 |
| FR-26 verb group | The closed list of coordinator verbs has `answer-check` and `escalate` but no gate verb; Orca's `gate-create` and `gate-resolve` would be Orca verbs named per step (C6) and checked against `refuse(argv)`. | aligned only after C6 (#787) exists | SPEC.md:228; observer reference lists gate verbs as refused for observer and sweep |
| Spec status | The spec is not a plan of record until the owner confirms its section 10 actions; Appendix B changed rows after PR 700. | note | SPEC.md:752-790; FOLLOW-UPS.md:50 |
| #716 review of 2026-11-24 | Items are "not authorized merely by appearing in #716"; start with C1, C2, C4, C6 and C25; owner note: "determine the current full handoff process before anything else is adopted". | partly aligned: C13 is in the phase 2 cluster, after the skeleton | #716 comments of 2026-11-24 14:23 and 20:53 |

No decision is violated by the item as written. One wording conflict: the done-when "confirms a person typed it" claims what RK-3 says cannot be proven.

## Complementary issues
- #797 (C16 merge-gate): shares the merge go and the question key `merge_safety:<PR>:<head sha>` (SPEC.md:297). Interface: `answer-check` is the validator #797's flow calls between its two gate runs (SPEC.md:157). Neither issue builds `answer-check`; the hard part has no owner.
- #808 (C27 capped notice after an escalation entry): same trigger, the `escalate` entry. Interface: one escalation entry write, then gate and notice as two outputs; build one path.
- #787 (C6 verbs per step vs `refuse(argv)`) and #782 (C1 skill layout): a gate verb must be on the step's list first; they must land before C13.
- #793 (C12 playbook for answering worker questions): who answers and how; a gate answer enters the same playbook as "not an acceptance".
- #776 (skill for the two human approvals): the routine for how an approval reaches the agent; it names C13 as a soft link.
- #727 (two-way dashboard), #781 (contact agents), #725 (ask the peer coordinator): other ways a person answers; each must obey SEC-08 (a typed answer in the person's own session).
- #722 (shared GitHub login): blocks a trustworthy identity check for `answer-check`.
- #706 and #409 (observer): `src/superclaude/cli/observe/questions.py:1-14` says "no closure source exists, so nothing is ever closed"; a gate closed on a recorded answer would be one.
- #534, #590 (sweep follow-ups): the sweep cannot read pending questions (`Messages coverage: partial`).

## Closest overlap
#808 (C27, one capped notice after an escalation entry): both add a way to reach the person from the same `escalate` entry and both are listed by the QG2 verdict as one channel decision. Shared: the trigger point, the "never instead of writing the entry" rule, and the owner questions (is a push wanted, which cap). Estimate: about 20% of this item's done-when (the "escalation opens a gate" hook of the second and third bullets); it covers none of the `answer-check` bullet.
Next closest: #797 (C16), about 10% (the merge go and question key, `answer-check` consumer); would rise to about 40% if the owner assigns `answer-check` to it. Third: #776 (approval routine), about 10%.
No open issue builds the escalation entry writer itself (titles of #716 items C1 to C27 and #782 to #808 checked; bodies of #787, #793, #801, #808 read; others UNVERIFIED).

## Standalone or merge
Verdict: stand alone (keep open with changes). Test against #808:
- Owner: both the coordinator's `escalate` step; same owner role. No difference.
- Acceptance test: C13 proves a refusal (gate-resolve alone is not a go; `answer-check` refuses a wrong question or head); C27 proves a cap (sixth notice in 24 hours is silent). Different pass/fail.
- Files touched: C13 adds a gate call in the escalate step, a sweep read (allowlist change in `sweep/probes.py`) and `answer-check`; C27 adds a notice sender and a cap key in the per-repo config.
- Build phase: both phase 2 cluster, both after the skeleton.
- Risk if merged: the security-sensitive validator `answer-check` would ride with a notification cap that waits on a different owner decision (a ClickUp credential and "a push is wanted", #808 Watch out), so a delay in one blocks the other.
Merging would be right if the owner decides the person-reach channel is one design question; then one issue should carry "entry, one channel, one cap" and `answer-check` should move out to #797 or its own item. That is not the current state.

## Closed issues and merged PRs checked
- #655 (closed not planned) and #665 (closed not planned, M11 and 20 other Medium findings): source of the item; neither delivers it.
- #444 (closed not planned, coordinator evaluation): no gate decision found (only title and state used; body not read for this item).
- #668 and PR #683 (closeout, merged 2026-11-20): settles a merged PR; does not open or close gates. Its report-entry step is the only caller of an absent verb.
- PR #584 and PR #591 (merged 2026-11-17, approval core and coordinator handoff): the approval path is the plan-hash `check-approval`, bound to an issue, not a merge go. Their live test found that the reply to an `ask` is stored as type `status`; a gate reply is not covered.
- PR #724 (merged 2026-11-23): owner records are given in chat and recorded by the agent; reinforces that a gate resolution cannot be a record.
- PR #539 (merged 2026-11-14, sweep Phase 1) and #534 (open follow-ups): confirm the sweep's read-only allowlist and the unreadable pending questions.
- PR #700 and #701 (merged 2026-11-20): rolled back Clay's build; no gate code exists on master.
- Closed sub-issues of #716: #796 (C15, closed not planned), #798 (C17, merged into #797), #804 (C23), #806 (C25, merged into #782), #809 (W1, merged into #716), #813 (W5): none touches C13.
Nothing delivers, supersedes or contradicts any part of C13.

## Updated recommendation
Keep open with changes, priority P3, complexity complex, size L. Unchanged from round 1 on priority, complexity and size. Round 2 adds and changes:
1. State in the issue who builds `answer-check` (SPEC SEC-09). Recommended: this item, because it is the only open item whose done-when needs it and R38 (D) keeps the typed go it validates; do not tie it to the merge gate that R38 (C) lists as not adopted.
2. Reword the done-when to what a test can show: `answer-check` refuses a gate-only resolution, a wrong question key, a wrong head sha and a stale entry (RK-3 mitigation); drop "confirms a person typed it".
3. Say the gate is a display channel and that the sweep allowlist change (NFR-014) is an owner-visible edit, or limit the display to the coordinator's own escalation entry.
4. Add the owner ruling "is a gate channel wanted at all" (QG2 left it unadopted, priority Low) and the order: after #782, #787, #785, and after the `escalate` writer exists.

## Scan record
- Lists read in full: open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Search terms: gate, answer, approve, approval, escalat, notice, question, go, merge, observer, sweep, dashboard, coordinator, identity, login.
- Opened with gh (read-only): open #716, #717, #718, #722, #725, #727, #776, #781, #787, #793, #797, #801, #808 (13); closed #655, #665, #668, #796, #798, #804, #806, #809, #813; merged PRs #539, #584, #591, #683, #700, #724 (bodies; review threads not read). #444 and #592 were fetched but not read for this item.
- Master check: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick` (report in `analyze/`); Grep for `gate-create`, `gate-resolve`, `answer-check`, `decision_gate` in src, tests, docs.
- UNVERIFIED: how Orca records who resolved a gate (only `--from <handle>` is a free-text flag, from `orca orchestration gate-resolve --help`); who builds the `escalate` entry writer; whether the owner meant to keep `answer-check` without the merge gate.
