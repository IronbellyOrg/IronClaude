<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS, variant-1-original.md) -->
<!-- Merge date: 2026-11-20 -->

# Merged position for OAG1: merge go lifetime and waiting policy

<!-- Source: Base (original, modified) - Terms paragraph made a heading, and terms added (reminder, push notice, ADD4, AD-B4, K9, K15, S15b, D11) so Changes #1, #2 and #3 can be read without another file -->
## Terms

"D:nnn" is a line of `docs/designs/orchestrator.md` (Clay's design, merged by PR 681, the design-document PR) in the master export `/home/coder/.cache/ic-snap-20261120/master`. "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` in the same export. "D06", "D11", "Q01", "QG1", "QG2" are the verdicts under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/`. A "go" is the person's typed consent for one named action, recorded by the agent. "ADD4" (D:138) is the design's merge-time reviewer hold, and "AD-B4" (D:1177) is its notice-cap row. "K9", "K15", "INV-023", "S15b", "RK-21", "RK-30", "OA-13", "OA-14", "OA-16" and "OA-25" are rows of the merged requirements, `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md`. K9 (line 311) is the rule for an issue waiting for a push or merge go. K15 (line 317) is the decision row for a hand-back waiting for re-approval (`waiting_reapproval`).

"Reminder" in this paper means display plus age: the waiting item stays shown as "waiting on a person" with the age of the wait (since when it has waited). A "push notice" is a message sent to the person through a notice step; it is not part of "reminder" and is reserved (see Claim 3). Every use of "reminder" below, including the quoted K9 and S15b wording "with a reminder", has this meaning.

<!-- Source: Base (original, modified) - claims 1 and 2 restructured; D06 wording corrected (Change #7), reserved age check added (Change #4), hold clock start added (Change #5), OA-13c sentence added (Change #9) -->
## Claim

1. A recorded merge go has no clock expiry by default. Following Q01 item 5, it ends in three ways: the named action is done, the PR head moves (or any new gate reason appears), or the owner revokes it in chat. D06 item 1 words this differently: it says the go "expires (number is an Owner DECISION, no source gives one)". This paper takes Q01 item 5 as the default and records the D06 wording as the owner's open option: a clock limit with a number the owner has to supply. Merge automation stays off until the owner records a number, so no unattended process can fire a go typed days ago.
   <!-- Source: Variant 2 (CLAY), Claim 1 and the owner-set number, merged per Change #4 -->
   The build of merge automation must carry a go age check, and it must refuse to start unless the owner has recorded a number or the explicit value "none". This is a requirement on that future build, not a setting added now: the go entry and the merge verb do not exist yet (requirements rows 28 and 29 are DESIGN ONLY). No default number is given (the 24-hour figure in the requirements is UNVERIFIED, no source).
2. The merge-time reviewer hold is what D06 item 4 adopted: an owner-set per-repo `reviewers` list, a re-request on the final head, a wait of 60 minutes (UNVERIFIED default, owner-settable), then escalation to the person. The clock starts when the final head's checks finish (D06 item 4; ADD4, D:138). `/sc:pr-submit` keeps its own skip rule inside the fix loop. `changes_requested` stays a hard refusal that no go overrides (D06 item 3, D:583).
3. A waiting go gets no push notice in the first build. It keeps its slot, counts toward `max_in_flight`, and is shown as "waiting on a person" with the age of the wait, which is the reminder as defined in Terms. A push notice stays reserved behind the three triggers of QG2/OD-5 (Cited facts 6). Silence is never a yes, and no expiry drops committed work.
   <!-- Source: Variant 2 (CLAY), Cited fact 5 (K15) and QG1 OD-13, merged per Change #2 -->
   - One waiting state does expire, and it is a different state from a waiting merge go. A hand-back waiting for re-approval (`waiting_reapproval`) moves to `stopped` after an owner-set limit (K15). No default number is given. This expiry does not free capacity, because that state is outside the cap. No waiting merge go ever expires.

<!-- Source: Base (original, modified) - new section required by the merge brief; answers drawn from the Claim, Mechanism and Cited facts, with the Change #1 to #9 corrections applied -->
## Answers

1. **OA-13a (does a recorded merge go expire by the clock).** No clock expiry by default. A go ends when the named action is done, the head moves or a new gate reason appears, or the owner revokes it in chat. Reason: the sha pin, the second gate run before the merge and WC:241 already cover a stale go; no source gives a number and no stale-go incident is cited. The owner may still choose a clock number (D06 item 1 wording), and merge automation must not start until the owner records a number or "none". Source: Cited facts 1, 2 and 3; Claim 1.
2. **OA-13b (merge-time hold for a silent reviewer, and how long).** Hold the merge for a listed reviewer who shows no activity: re-request a review on the final head, wait 60 minutes from when the final head's checks finish (UNVERIFIED default, owner-settable), then escalate to the person. Reason: the `/sc:pr-submit` loop reads one done plus one absent reviewer as clean, so the merge decision needs its own stop; the loop's skip rule stays unchanged. Source: Cited fact 7; Claim 2.
3. **OA-13c (`changes_requested`).** A hard refusal that no go overrides. Reason: both positions agree and Clay's own design says the same. Source: Cited fact 8; Claim 2.
4. **OA-25a (does a waiting go get a reminder, at what interval).** The waiting go is shown as "waiting on a person" with the age of the wait (this is the reminder, as defined in Terms). No push notice and no push interval in the first build. The existing daily 07:00 wake of the work report re-shows an unanswered entry, so the display cadence is daily with no new sender. Reason: no escalation notice sender exists in master, `pr-a` or `pr-p` (QG2), and the cap is Clay's ruling, not the owner's. Source: Cited facts 5 and 6; Mechanism, last bullet.
5. **OA-25b (what owner silence means on a waiting go).** Silence is never a yes. A waiting merge go keeps its slot, counts toward `max_in_flight` and never expires, because its worker is finished and its PR is open, so an expiry would drop committed work. A hand-back waiting for re-approval is a separate state: it is outside the cap and expires to `stopped` only on an owner-set limit (K15, no default number). Reason: K9 and INV-023 for the first state, K15 and QG1 OD-13 for the second. Source: Cited fact 5; Claim 3.

<!-- Source: Base (original, modified) - last bullet replaced per Change #1 and extended per Change #6 -->
## Mechanism

<!-- Source: Base (original) -->
- A go is a file entry (merged requirements row 28: `<state_dir>/goes/<PR>-<sha12>.json`, repository, PR, 40-character sha, method, the word merge, gate output id, quoted words, times, recorder, question key, consumed flag). It is one-shot and void on a head move or a new gate reason. It is bound to a head sha, so the main thing a clock would protect against (the code changed after the person said yes) is already caught by the pin.
- Immediately before `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>` the read-only gate runs again and refuses if any reason, open thread, review state, base branch or draft state differs from what the person saw (D06 item 2). A go cannot override `head_moved`, `draft`, `changes_requested`, `review_stalled`, `review_none_present`, `checks_pending`, `review_pending`, `threads_open` and others (D06 item 3).
- The contract already bounds a stale instruction by conversation, not by clock: the coordinator performs outward actions "only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation" (WC:241). A go recorded in an earlier session is not in the live conversation, so it is re-confirmed. Merge automation (a script or restarted session acting on a stored go) is the only path a clock would matter for, and that path is off.
<!-- Source: Base (original, modified) - last bullet replaced: waiting is shown with its age (display), not resolved by a timer; the reminder is defined as display plus age (Change #1) -->
- Waiting is shown, not resolved by a timer. The reminder is display plus age: the item stays listed as "waiting on a person" with since when it has waited, and a push notice is reserved (Claim 3). The sweep already lists "waiting" sessions (`src/superclaude/cli/sweep/report.py:682-685`, fields `waiting.a` and `waiting.b`).
<!-- Source: Variant 2 (CLAY), Mechanism "Reaching the person" and Cited fact 8, merged per Change #6 -->
- The merged work report keeps an unanswered entry visible ("An unanswered 'Needs you' entry stays until Clay answers it", `src/superclaude/skills/agent-work-report/SKILL.md:22`) and is woken daily at 07:00 local (SKILL.md:30). That report is configured for one named person today (Clay), so for the repository owner the sweep and the observer are the surfaces that show the wait.

<!-- Source: Base (original, modified) - items 1, 5 and 6 corrected (Changes #7, #3, #8); item 2 marked UNVERIFIED; item 7 clock start and ruling note added -->
## Cited facts

1. D06 item 1 and Q01 item 5. Q01 item 5: a go ends on the named action, a head move or a revoke. D06 item 1 (`debates/D06/VERDICT.md:14`): the go "expires (number is an Owner DECISION, no source gives one)". The two verdicts are not worded alike. This paper takes Q01 item 5 as the default and records the D06 wording as the owner's open option.
2. Merged requirements OA-13 (`merged-requirements.md:683-688`): "No expiry: a go lives until used, the head moves or the owner revokes it in chat; merge automation stays off until this is answered." This is one open owner option, not a requirement. Risk RK-30 (same file): "Unsourced numbers are treated as settled (60-minute reviewer hold, 24-hour go expiry ...) ... No source gives these numbers ... Labelled UNVERIFIED; merge automation off until OA-13 is answered". The 60-minute hold and the 24-hour figure are UNVERIFIED.
3. WC:241 (above): outward actions need the instruction in the live conversation or a confirmation at the moment of action. The contract elsewhere ends grants by event, not clock: "A commit grant covers one Task and ends at that Task's `worker_done`" (WC, Git and GitHub ownership section, line 244 region).
4. Owner order 2026-11-17 (memory `approvals-through-chat-never-files`): every approval and go is given in chat and recorded by the agent. A clock-expired go would force the owner to re-type a consent that nothing in the repository shows has gone stale.
5. Two waiting states, side by side.
   - Waiting merge go: the worker has finished and the PR is open. It keeps its slot, counts toward `max_in_flight`, is shown "waiting on a person" with a reminder (display plus age, as defined in Terms), and never expires away committed work. The quoted text "counts, is shown 'waiting on a person' with a reminder, and never expires away committed work" is K9 (`merged-requirements.md:311`); INV-023 and S15b ("shown with a reminder (INV-023, OA-25)") repeat it. An expiry that moved this state to `stopped` would abandon committed work.
   - Waiting re-approval (`waiting_reapproval`): there is no worker and no PR. QG1 OD-13 rules that it does not count toward the cap (`debates/QG1/VERDICT.md:30-34`). K15 (`merged-requirements.md:317`): it is outside the cap and expires to `stopped` after an owner-set limit; OA-14 (`merged-requirements.md:690`): "the expiry number sets when a waiting issue drops to `stopped`". No source gives the number.
6. The push notice is not ruled on. D:1177 (AD-B4) calls the notice cap "not ruled on; open" in its question column. The same row also says "Settled as recommended (ruling 39)", a cap of 5 notices a day; D11 treats ruling 39 as Clay's ruling, not the repository owner's, and the owner has not ruled. QG2/OD-5 reserves the push notice behind three triggers (the owner asks for a push and gives a cap, a notice sender is built and tested, the verb accepts row 8 alone), and OA-16 defaults to no cap. QG2 found no escalation notice sender in master, `pr-a` or `pr-p`.
7. D06 item 4 and `/sc:pr-submit` SKILL.md:29-32 and :364: the skip rule for a silent Codex stays inside the loop ("`reviewer_absent{reviewer: "codex"}`; Codex is ignored for the run"); the hold lives only at the merge decision, where D06 adopted it with an owner-set `reviewers` list. The hold clock starts when the final head's checks finish (60 minutes, UNVERIFIED, owner-settable; ADD4, D:138). ADD4 calls this owner ruling 6, but the merged requirements treat Clay's rulings as Clay's (D11 verdict).
8. D06 item 3, and Clay's own design D:583: `changes_requested` is a hard refusal that no go overrides. OA-13c carries it unchanged.

<!-- Source: Base (original, modified) - cost bullet 3 reworded to "push notice" so it agrees with the Terms definition of reminder (Change #1) -->
## What it costs

- A go typed days ago still stands if nobody revokes it and the head, gate reasons and base are unchanged. The person may have forgotten it. The sha pin, the second gate run and WC:241 narrow this but do not remove it.
- A stalled cap-1 repo is quiet: one unanswered merge go holds the only slot (RK-21, INV-023 MEDIUM, "UNADDRESSED").
- With no push notice the owner must look at the report, the sweep or the observer to see a waiting go and the age of its wait.

<!-- Source: Base (original) -->
## What it risks

- If merge automation is turned on later without the owner recording a number, a stale go could fire. The row says automation stays off until the owner answers OA-13, so the risk exists only if that row is ignored.
- The 60-minute hold (UNVERIFIED) is unsourced and could dead-wait if a listed reviewer never reviews (D06 Unverified: whether Codex reviews on every push).

<!-- Source: Base (original) -->
## What it gets right

- It keeps consent anchored to what the person said and to the code they saw (sha pin), not to a number nobody can source.
- It keeps the owner's rule that silence is never a yes and that committed work is never dropped by a timer.
- It does not invent a notice mechanism, a cap number or a push interval that no owner ruling or source supports (RK-30).
- It keeps `/sc:pr-submit` unchanged and makes the stricter merge-time hold a separate, owner-configured rule.

<!-- Source: Base (original, modified) - new section listing the four rejected alternatives from the refactor plan -->
## Considered and not adopted

- A go that dies after N hours (24 suggested, UNVERIFIED) with no event. Not adopted: no sourced number (RK-30, D06 item 1), no cited incident of a stale go firing, and the sha pin, the second gate run and WC:241 already cover the stale-code case. The Clay-position advocate conceded no clear benefit. Only the reserved age check on the future automation build (Claim 1) is kept.
- A push notice through the notice step in the first build. Not adopted: no notice sender exists in master, `pr-a` or `pr-p` (QG2), the cap is Clay's ruling, and the push stays reserved behind the three triggers of QG2/OD-5.
- A clock expiry that would free the slot of a long-waiting merge go. Not adopted: that state has a finished worker and an open PR, and an expiry would drop committed work (K9, INV-023).
- ADD4's sentence "an agent that never showed activity is no longer skipped". Not adopted: D06 item 4 overrode it; the skip rule stays inside the `/sc:pr-submit` fix loop and the hold lives at the merge decision.
