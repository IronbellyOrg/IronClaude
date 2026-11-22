# Position OURS for OAG1: merge go lifetime and waiting policy

Terms. "D:nnn" is a line of `docs/designs/orchestrator.md` (Clay's design, merged by PR 681, the design-document PR) in the master export `/home/coder/.cache/ic-snap-20261120/master`. "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` in the same export. "D06", "Q01", "QG1", "QG2" are the verdicts under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/`. A "go" is the person's typed consent for one named action, recorded by the agent.

## Claim

1. A recorded merge go has no clock expiry. It ends in exactly three ways: the named action is done, the PR head moves (or any new gate reason appears), or the owner revokes it in chat. Merge automation stays off until the owner records a number, so no unattended process can fire a go typed days ago.
2. The merge-time reviewer hold is exactly what D06 item 4 adopted: an owner-set per-repo `reviewers` list, a re-request on the final head, a wait of 60 minutes (UNVERIFIED default), then escalation to the person. `/sc:pr-submit` keeps its own skip rule inside the fix loop. `changes_requested` stays a hard refusal.
3. A waiting go gets no new push reminder in the first build. It keeps its slot, counts toward `max_in_flight`, and is shown as "waiting on a person" with the age of the wait. Silence is never a yes, and no expiry drops committed work.

## Mechanism

- A go is a file entry (merged requirements row 28: `<state_dir>/goes/<PR>-<sha12>.json`, repository, PR, 40-character sha, method, the word merge, gate output id, quoted words, times, recorder, question key, consumed flag). It is one-shot and void on a head move or a new gate reason. It is bound to a head sha, so the main thing a clock would protect against (the code changed after the person said yes) is already caught by the pin.
- Immediately before `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>` the read-only gate runs again and refuses if any reason, open thread, review state, base branch or draft state differs from what the person saw (D06 item 2). A go cannot override `head_moved`, `draft`, `changes_requested`, `review_stalled`, `review_none_present`, `checks_pending`, `review_pending`, `threads_open` and others (D06 item 3).
- The contract already bounds a stale instruction by conversation, not by clock: the coordinator performs outward actions "only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation" (WC:241). A go recorded in an earlier session is not in the live conversation, so it is re-confirmed. Merge automation (a script or restarted session acting on a stored go) is the only path a clock would matter for, and that path is off.
- Waiting is shown, not resolved by a timer. The sweep already lists "waiting" sessions (`src/superclaude/cli/sweep/report.py:682-685`, fields `waiting.a` and `waiting.b`). The merged work report keeps an unanswered entry visible ("An unanswered 'Needs you' entry stays until Clay answers it", `src/superclaude/skills/agent-work-report/SKILL.md:22`) and is woken daily at 07:00 local (SKILL.md:30).

## Cited facts

1. D06 item 1 and Q01 item 5: a go ends on the named action, a head move or a revoke; the expiry number is "an Owner DECISION, no source gives one" (D06 item 1).
2. Merged requirements OA-13 (`.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md:683-688`): "No expiry: a go lives until used, the head moves or the owner revokes it in chat; merge automation stays off until this is answered." Risk RK-30 (same file): "Unsourced numbers are treated as settled (60-minute reviewer hold, 24-hour go expiry ...) ... No source gives these numbers ... Labelled UNVERIFIED; merge automation off until OA-13 is answered".
3. WC:241 (above): outward actions need the instruction in the live conversation or a confirmation at the moment of action. The contract elsewhere ends grants by event, not clock: "A commit grant covers one Task and ends at that Task's `worker_done`" (WC, Git and GitHub ownership section, line 244 region).
4. Owner order 2026-11-17 (memory `approvals-through-chat-never-files`): every approval and go is given in chat and recorded by the agent. A clock-expired go would force the owner to re-type a consent that nothing in the repository shows has gone stale.
5. QG1 OD-13 and merged requirements K9 and INV-023: an issue waiting for a push or merge go "counts, is shown 'waiting on a person' with a reminder, and never expires away committed work". A waiting merge go has a finished worker and an open PR, so an expiry that moves it to `stopped` abandons committed work.
6. D:1177 (AD-B4) calls the notice cap "not ruled on; open", QG2/OD-5 reserves the push notice behind three triggers (the owner asks for a push and gives a cap, a notice sender is built and tested, the verb accepts row 8 alone), and OA-16 defaults to no cap. QG2 found no escalation notice sender in master, `pr-a` or `pr-p`.
7. D06 item 4 and `/sc:pr-submit` SKILL.md:29-32 and :364: the skip rule for a silent Codex stays inside the loop ("`reviewer_absent{reviewer: "codex"}`; Codex is ignored for the run"); the hold lives only at the merge decision, where D06 adopted it with an owner-set `reviewers` list.
8. D06 item 3, and Clay's own design D:583: `changes_requested` is a hard refusal that no go overrides. OA-13c carries it unchanged.

## What it costs

- A go typed days ago still stands if nobody revokes it and the head, gate reasons and base are unchanged. The person may have forgotten it. The sha pin, the second gate run and WC:241 narrow this but do not remove it.
- A stalled cap-1 repo is quiet: one unanswered merge go holds the only slot (RK-21, INV-023 MEDIUM, "UNADDRESSED").
- With no push reminder the owner must look at the report or the sweep to see a waiting go.

## What it risks

- If merge automation is turned on later without the owner recording a number, a stale go could fire. The row says automation stays off until the owner answers OA-13, so the risk exists only if that row is ignored.
- The 60-minute hold is unsourced and could dead-wait if a listed reviewer never reviews (D06 Unverified: whether Codex reviews on every push).

## What it gets right

- It keeps consent anchored to what the person said and to the code they saw (sha pin), not to a number nobody can source.
- It keeps the owner's rule that silence is never a yes and that committed work is never dropped by a timer.
- It does not invent a notice mechanism, a cap number or a reminder interval that no owner ruling or source supports (RK-30).
- It keeps `/sc:pr-submit` unchanged and makes the stricter merge-time hold a separate, owner-configured rule.
