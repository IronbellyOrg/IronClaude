# Position CLAY for OAG1: merge go lifetime and waiting policy

Terms as in position-OURS.md. "D:nnn" is a line of `docs/designs/orchestrator.md` (Clay's design, PR 681) in `/home/coder/.cache/ic-snap-20261120/master`. "K15" is the merged-requirements decision row for hand-back round 2 (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md:317`). No source gives Clay's pronouns; "they" is used.

## Claim

1. A merge go must die by the clock as well as by event. A go typed N hours ago and never used must not fire, even if the head did not move. The merged requirements suggest 24 hours (UNVERIFIED, no source). The cost of expiry is one re-ask; the cost of no expiry is a merge on stale intent.
2. A merge-time hold for a silent reviewer must be a stated, mechanical rule with a number, so a stalled review cannot be merged around and cannot wait forever. Clay's design states it: hold the PR when a listed reviewer shows no activity, or started and has not finished, 60 minutes after the head's checks finished, and escalate to the person (ADD4, D:138; decided as OD4, D:1155).
3. A waiting go must reach the person, not just sit in a report, or a cap-1 repo stalls quietly. Clay's design gives the channel: the notice step with the nine-row list and a daily cap `reach_daily_max` (D:686, D:877). A waiting item never answered must not hold capacity forever: an expiry moves a long-waiting hand-back (`waiting_reapproval`) to `stopped` (K15).

## Mechanism

- Go lifetime. The go entry already carries times (requirements row 28). A refusal "go older than N hours" is one comparison in the merge verb, next to the head-sha comparison. It covers what the pin cannot: code and gate reasons unchanged, but the person's intent or knowledge has moved on (a decision taken elsewhere). Clay's answer check already applies a freshness rule to typed answers ("newer than the entry's last edit", D:694), so freshness is already the design's idiom.
- Reviewer hold. `merge_wait` returns `no_response` when both reviewers are absent (`src/superclaude/pr_submit/reviewers.py:395-427`); the loop's absent state is clock-based (`reviewers.py:390-391`), so "one done plus one absent reads clean" (`reviewers.py:414-419`). The hold converts that into a stop at the merge decision, re-requests a review on the final head, waits a bounded time and escalates.
- Reaching the person. Row 9 of the nine-row table is "him because it is stuck and nobody else can unstick it" and names "a pull request held because a listed review agent never ran or finished" (design section 5.6, D:664-696). `escalate` writes the entry in the issue's own entry of the living report and, within the cap, sends a notice (a ClickUp DM or an unread mark). A ClickUp DM sender for the report notice already exists (`src/superclaude/skills/agent-work-report/scripts/clickup.py:2-6`, the `dm` subcommand), though it sends to the token owner's own DM.
- Waiting is never silently decided. Clay's own rule: "nothing that needs Clay is decided for him (ruling 24: an unanswered question waits, no default)" (design section 5.6, "If he does not answer"). So expiry applies only where no committed work is lost.

## Cited facts

1. ADD4 (D:138) and OD4 (D:1155): hold the PR, escalate as row 9, 60 minutes after the head's checks finished; `reviewers: none` is the one way a repo has nothing to wait for; "it never merges without the review (owner ruling 6, 2026-11-19)". The design calls it the owner's ruling; the merged requirements treat Clay's rulings as Clay's, not the repository owner's (D11 verdict).
2. `src/superclaude/pr_submit/reviewers.py:390-391` and `:414-419`: absence is declared on a clock or a settled peer; one done plus one absent reads clean. The D06 verdict records this as a verified gap in the skip rule.
3. Memory `pr-submit-check-pr-open-before-push` (owner's own note, 15 days old, not re-verified): a Codex security review landed after a "clean" result. Late reviews are real.
4. D06 item 1 itself says the go "expires (number is an Owner DECISION, no source gives one)". The owner-side verdict already accepts that a go expires; only the number and the clock are open.
5. K15 (merged requirements:317): `waiting_reapproval` is outside the cap and expires to `stopped` after an owner-set limit. OA-14 (`merged-requirements.md:690`): "the expiry number sets when a waiting issue drops to `stopped`". The merged design already contains an expiry for one waiting state.
6. INV-023 and RK-21 (merged requirements): "one corrupt file or one unanswered go stalls the repo", rated UNADDRESSED. A cap of 1 with no expiry and no push means one unanswered go blocks the repo.
7. D:686-688 and D:877: `reach_daily_max` is a whole number from 0 to 50, 0 meaning no cap; notices are capped, entries are never dropped; changed only on the owner's recorded word. With the key absent it sends nothing extra.
8. `agent-work-report` SKILL.md:30: a daily 07:00 wake exists; the report is already a daily reminder surface for Clay's own setup.

## What it costs

- One more field and refusal in the merge verb; one more number for the owner to choose (RK-30 warns about unsourced numbers treated as settled).
- A notice step that does not exist yet: QG2 found no escalation sender in master, `pr-a` or `pr-p`. The cap, the nine-row list and the sender are design text.
- A re-ask when a legitimate go lapses while the owner is away.

## What it risks

- A number with no source becomes policy by default (RK-30). If 24 hours or 60 minutes is wrong, the system dead-waits or refuses a good go.
- An expiry on a waiting merge go that has a finished worker and an open PR would drop committed work, which INV-023 and K9 forbid. The CLAY claim is therefore limited to a clock check on the go itself and to waiting states with nothing to lose.
- A reminder channel that is not built or ruled by the owner (the cap, ruling 39, is Clay's per D11) would be adopted by assumption.

## What it gets right

- It names a concrete weakness of the present line: a go is only as fresh as the person's memory, and a stalled cap-1 repo is quiet. Both are marked UNADDRESSED in the merged requirements.
- Its hold is stated with a number and a stop, so a silent reviewer cannot be merged around (ADD4), filling a verified gap in the skip rule.
- Its reminder is capped and never drops an entry, and its expiry is applied only to a state with nothing to lose (K15).
