# Verdict OAG1: Merge go lifetime and waiting policy (OA-13, OA-25)

## Question

OAG1 Merge go lifetime and waiting policy: OA-13 (how long does a merge go and a reviewer wait last), OA-25 (how a waiting go reaches the person)

- OA-13a Does a recorded merge go expire by the clock? OURS: no clock expiry; a go ends only when the named action is done, the PR head moves or the owner revokes it in chat (Q01 item 5); merge automation stays off until the owner records a number. CLAY or alternative: a go dies after N hours even if the head did not move (24 hours suggested by the merged design, UNVERIFIED), so a go typed days ago cannot fire.
- OA-13b Is there a merge-time hold for a reviewer that shows no activity, and for how long? OURS: `/sc:pr-submit` keeps its own skip rule for a silent reviewer inside its fix loop; the merge-time hold exists only as D06 item 4 adopts it (owner-set per-repo `reviewers` list, re-request on the final head, wait 60 minutes UNVERIFIED, then escalate to the person). CLAY or alternative: Clay ADD4 holds the PR when a reviewer is silent with no stated wait; or a different number, or none (recorded as an explicit exception).
- OA-13c (settled input, not debated) `changes_requested` stays a hard refusal (D06 item 3). The debate only confirms it is carried unchanged.
- OA-25a Does a waiting go get a reminder, and at what interval? OURS: no push reminder in the first build (QG2/OD-5 reserves the notice; OA-16 default is no cap); a waiting go keeps its slot and is shown as "waiting on a person" in the report. CLAY or alternative: a reminder every N hours through the notice step (nine-row table, `reach_daily_max`) so a stalled cap-1 repo is not quiet.
- OA-25b What does owner silence mean on a waiting go? OURS: silence is never a yes and no expiry drops committed work (INV-023, K9); a waiting go counts toward `max_in_flight`. CLAY or alternative: an expiry moves a long-waiting go or `waiting_reapproval` to `stopped` (K15), freeing the slot.

Reading notes (short names used below). A "go" is the owner's typed consent for one named action, recorded by the agent. "D:nnn" is a line of `docs/designs/orchestrator.md` (the design Clay's PR 681 merged) in the master export `/home/coder/.cache/ic-snap-20261120/master`. "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` in that export (the rules for coordinator and worker sessions). D06 (who merges), D11 (sweep, report and dashboard), Q01 (who writes a go record), QG1 (planning and hand-back) and QG2 (escalation channel) are earlier verdicts in `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/<id>/VERDICT.md`. K9, K15, INV-023, RK-21, RK-30, S15b, OA-13, OA-14, OA-16 and OA-25 are rows of `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md` (K9 is the rule for an issue waiting for a go; K15 is the rule for a hand-back waiting for re-approval, `waiting_reapproval`). ADD4 is the design's merge-time reviewer hold (D:138). The `max_in_flight` cap is the number of issues one coordinator may hold at once; the merged default is 1.

## Winner

HYBRID. OURS decides all four contested answers (no clock expiry, the owner-set merge-time hold, no push notice in the first build, silence never a yes); two CLAY elements stay in as separable benefits (the K15 expiry for a hand-back waiting for re-approval only, and ADD4's hold with its stated clock start), and the debate confirmed rather than created both.

## Winning recommendation

Default for the spec: no clock on a go, a 60-minute owner-settable merge-time hold, no push notice, and silence is never a yes. Each line below gives the answer, the reason and the source, and says how a test can check it. Wording rule for the spec (from the forced round on wording): "ends" or "void" or "consumed" for an event close of a go; "expires" only for a clock close; "hold" for the merge-time stop for a silent reviewer; "waiting" for a state; "shown with the age of the wait" for the display; "push notice" for a message sent to the person. The unqualified word "reminder" is used only when quoting K9 or S15b, whose "with a reminder" is a placeholder for the open channel of OA-25 (K9, line 311; S15b, line 535 of the merged requirements).

1. **OA-13a, does a recorded merge go expire by the clock: no, not in the first build.**
   - Answer: a go ends (a) when the named action is done, (b) when the PR head moves or any new gate reason appears (the go is void), or (c) when the owner revokes it in chat. No age refusal exists today. The build of merge automation (a script or a restarted session acting on a stored go) must include a go age check and must refuse to start until the owner records either a number of hours or the explicit value "none". That is a requirement on a future build, not a setting added now, and no default number is given (24 hours is UNVERIFIED).
   - Reason: the go is bound to a 40-character head sha, the read-only gate runs again just before `gh pr merge --match-head-commit`, and WC:241 requires the instruction to be in the live conversation or confirmed at the moment of action, so a go from an earlier session is re-confirmed. No source gives a number and no stale-go incident is cited by either side (both advocates conceded this). The owner side of the spec has two wordings that do not match: D06 item 1 says the go "expires (number is an Owner DECISION, no source gives one)", Q01 item 5 says it ends on the action, a head move or a revoke. The spec follows Q01 item 5 as the default and keeps D06's number as the owner's open option.
   - Source: `debates/D06/VERDICT.md:14`, `debates/Q01/VERDICT.md` item 5, `merged-requirements.md:683-688` (OA-13) and RK-30, WC:241 in the master export.
   - Testable: a merge go for head X recorded days ago, with the head and every gate reason unchanged and the instruction confirmed in the live conversation, is accepted (no age refusal in the first build); a go for head X never releases a merge of head Y; with merge automation built and no recorded number or "none", the automation refuses to start.
2. **OA-13b, merge-time hold for a silent reviewer: yes, as D06 item 4 has it; 60 minutes (UNVERIFIED default, owner-settable).**
   - Answer: the owner sets a per-repo `reviewers` list (`none` is allowed as an explicit, recorded exception); a review of the final head is requested from each listed reviewer; the gate waits up to 60 minutes counted from when the final head's checks finish; then it escalates to the person and the PR stays held. `review_stalled` and `review_none_present` are not overridable by a go. `/sc:pr-submit` keeps its own skip rule inside its fix loop, unchanged.
   - Reason: the loop reads one finished plus one absent reviewer as clean (`reviewers.py:414-419`) and declares absence on a clock (`reviewers.py:390-391`), so the merge decision needs its own stop. ADD4 does state a wait (60 minutes after the head's checks finished), so the topic's "no stated wait" for CLAY is wrong; the two sides agree on 60 and on the stop, and the only point they differed on (ADD4's sentence that a silent reviewer "is no longer skipped") was already overridden by D06 item 4. The number has no source and ADD4's "owner ruling 6" is Clay's ruling, not the repository owner's (D11 verdict), so the default stays UNVERIFIED. A wrong number only delays a merge, it never causes one.
   - Source: `debates/D06/VERDICT.md` item 4, `docs/designs/orchestrator.md:138` (ADD4) and `:1155` (OD4), `src/superclaude/pr_submit/reviewers.py:390-391, :414-419`.
   - Testable: a listed reviewer with no activity on the final head 59 minutes after the checks finished leaves the PR held; at 60 minutes the escalation to the person is raised; a repo with `reviewers: none` records the exception; no go overrides `review_stalled`.
3. **OA-13c, `changes_requested`: a hard refusal, carried unchanged.**
   - Answer: no go overrides a PR with an open "changes requested" review. Reason: both sides agree (D06 item 3, `docs/designs/orchestrator.md:583`); the CLAY position paper simply never mentioned it. Source: `debates/D06/VERDICT.md` item 3. Testable: the gate refuses and lists `changes_requested`, with no override key.
4. **OA-25a, does a waiting go get a reminder: no push notice in the first build; the wait is shown with its age.**
   - Answer: a PR waiting for a go is shown as "waiting on a person" with the age of the wait (since when it has waited), in the report entry lines that QG2/OD-5 sets as the first-build channel, and listed by the sweep and the observer. The push notice (a ClickUp message or an Orca unread mark) stays reserved behind the three triggers of QG2/OD-5: the owner says in chat that a push is wanted and gives a cap number, a notice sender is built and tested, and the escalation verb accepts the needed row. When the owner records an interval, it is the owner's number; the only cadence with a source in the repository is daily (the 07:00 report wake), which is UNVERIFIED as a reminder interval.
   - Reason: no escalation notice sender exists in master, in Clay's PR 686 head (a rewrite of the issue watcher) or in branch `issue-655-pr-p` (QG2); the cap of 5 notices a day is Clay's ruling 39 (the design's own row D:1177 says both "not ruled on; open" and "Settled as recommended"), and the owner has no record of ruling on it (D11); OA-16 defaults to no cap. Both advocates agreed. Correction to the OURS paper: the sweep today lists Orca session row ids only, with no age and no go entries (`src/superclaude/cli/sweep/models.py:265-266`, `src/superclaude/cli/sweep/classify.py:994-999`), so "shown with its age" is a requirement on the entry-line writer and the display, not an existing feature.
   - Source: `debates/QG2/VERDICT.md` OD-5, `debates/D11/VERDICT.md`, `docs/designs/orchestrator.md:1177`, `merged-requirements.md:698-701` (OA-16, cap) and `:707-710` (OA-25).
   - Testable: with a go waiting 3 days, the report entry and the sweep show it as waiting on a person with its age; no message is sent to the person; a test of the notice step is not required until the three triggers hold.
5. **OA-25b, what owner silence means on a waiting go: silence is never a yes; a waiting merge go counts toward `max_in_flight` and never expires; only a hand-back waiting for re-approval may expire, on an owner-set limit with no default.**
   - Answer: there are two waiting states and the spec names both. (i) Waiting merge go: the worker has finished and the PR is open; it keeps its slot, counts toward `max_in_flight`, and nothing moves it to `stopped`, because that would abandon committed work (K9, INV-023). (ii) Waiting re-approval (`waiting_reapproval`): no worker, no PR; QG1/OD-13 rules it does not count toward the cap, K15 lets it expire to `stopped` after an owner-set limit. With no limit recorded it never expires. Because state (ii) is outside the cap, its expiry frees nothing; it only cleans up a stale waiting entry (this corrects the CLAY wording "freeing the slot").
   - Reason: Clay's own design says an unanswered question waits and no default is taken (design section 5.6, "If he does not answer", ruling 24), and Clay's merged report skill keeps an unanswered "Needs you" entry until answered (`src/superclaude/skills/agent-work-report/SKILL.md:22`). The OURS paper blurred the two states in its fact 5 (it credited a K9 quote to QG1 OD-13, which rules the opposite for the second state); the debate resolved it by naming both.
   - Source: `merged-requirements.md:311` (K9), `:317` (K15), `:877` (INV-023), `debates/QG1/VERDICT.md:30-34` (OD-13).
   - Testable: three issues in `waiting_reapproval` do not make a new issue of the same repo answer `coordinator_full`; one issue with an unanswered merge go at cap 1 stays counted and is shown waiting with its age, and no timer moves it to `stopped`.

## Strongest points

**OURS**
1. The stale-code and stale-session cases are already covered without a clock: the go is bound to a head sha, the gate runs again before the merge, and outward action needs the live conversation or a confirmation (D06 items 1 and 2; WC:241). No number is sourced (RK-30, D06 item 1).
2. Committed work is never dropped by a timer and silence is never a yes: K9 and INV-023, and Clay's own design and report skill say the same (design section 5.6 ruling 24; `agent-work-report/SKILL.md:22`).
3. The push notice cannot be built yet and its cap is not the owner's ruling: no sender exists (QG2/OD-5), ruling 39 is Clay's (D11), OA-16 defaults to no cap.

**CLAY**
1. A real gap: one unanswered go at cap 1 stalls the repo quietly (RK-21, INV-023 rated MEDIUM and UNADDRESSED), and a go's freshness otherwise depends on the owner's memory. This is why the verdict requires the wait to be shown with its age and reserves an age check for the automation build.
2. ADD4's hold is stated with a number, a clock start, a stop and an explicit `reviewers: none` exception, and it fills a verified gap in the skip rule (`docs/designs/orchestrator.md:138`; `reviewers.py:390-391, :414-419`).
3. K15 gives a state with nothing to lose a clean-up path, and a daily surface exists for re-listing an unanswered entry (`merged-requirements.md:317`; `agent-work-report/SKILL.md:22, :30`).

## Clay strengths to adopt

- **ADD4's hold with its clock start (already adopted by D06 item 4; confirmed here).** What: wait 60 minutes from when the final head's checks finish, then escalate; `reviewers: none` is the one recorded exception. Why: fills the gap in the skip rule. Merge: keep `/sc:pr-submit` unchanged; override ADD4's sentence "no longer skipped"; the number stays UNVERIFIED and owner-settable.
- **K15's expiry for `waiting_reapproval` only.** What: an owner-set limit moves a hand-back waiting for re-approval to `stopped`; no default. Why: the state has no worker and no PR, so nothing is lost, and it cleans up stale entries (QG1/OD-13 allows an expiry "only if waiting issues pile up"). Merge: state that it frees no capacity; never apply it to a waiting merge go.
- **A reserved go age check for the automation build.** What: the merge-automation build must carry an age check and refuse to start until the owner records a number or "none". Why: the part of CLAY's clock idea that survives; it turns OA-13's "automation stays off until answered" from a promise into a check. Merge: a requirement on the future build, not a key added now (no merge verb or go entry exists, rows 28 and 29 of the requirements are DESIGN ONLY).
- **The daily work report as a re-listing surface.** What: an unanswered entry stays and is re-shown at the 07:00 wake. Why: a surface that already exists and is built. Merge: adopt for Clay's own setup only; the report is configured for one named person (`"person": "clayphi"`, D11 verdict), so for the owner the sweep and observer are the surfaces.
- **The notice step and `reach_daily_max` (not adopted now, reserved).** Reserved behind the three triggers of QG2/OD-5; the cap stays 0 (no cap) until the owner records a number.

## Our strengths that must be kept

- No clock expiry in the first build; a go is one-shot, bound to the head sha, void on a head move or a new gate reason.
- The second gate run immediately before `gh pr merge` with no `--auto`, `--admin` or `--delete-branch`.
- WC:241: an outward action needs the instruction in the live conversation or a confirmation at the moment of action.
- Silence is never a yes, and no expiry drops committed work.
- `/sc:pr-submit` and its skip rule unchanged; the merge-time hold is a separate, owner-configured rule.
- No notice sender, cap number or reminder interval is invented without an owner ruling.

## Actions

| Action | Type | Target (file, PR or issue number) | Order or dependency |
|---|---|---|---|
| Write the five numbered answers above into the unified spec as defaults, with the wording rule (ends, void, consumed, expires, hold, waiting, shown with the age of the wait, push notice) | DOC | the unified spec (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/`) | With the spec; no owner go needed |
| Rewrite the K9, S15b, INV-023 and OA-25 wording so "with a reminder" reads "shown with the age of the wait; push notice reserved" | DOC | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md` lines 311, 535, 877, 707-710 | With the spec |
| Add the reserved age-check requirement to the merge-automation section (refuse to start without a recorded number or "none") | DOC | spec section for the merge verb and automation (D06 build row) | Before any merge verb is built |
| Add "waiting since" to the report entry lines and to the sweep and observer display of a waiting PR | LOCAL CHANGE (later build) | entry writer at stage S15c; `src/superclaude/cli/sweep/` and the observer after OAG2 is decided | After OAG2; not before the entry-line writer exists |
| Fix design text: ADD4's "no longer skipped" sentence and its "owner ruling 6" (it is Clay's ruling); the self-contradicting AD-B4 row (D:1177) | DOC | `docs/designs/orchestrator.md` lines 138, 1155, 1177 or its unified successor | With the D06 authority rewrite |
| Owner answers in chat, one item at a time: a go age number or "none"; keep 60 minutes or give another; whether a push notice is wanted and its interval | DECISION | owner chat; OA-13, OA-16, OA-25; none blocks the spec (safe defaults named above) | Any time; each answer is recorded by the agent, never as a file the owner writes |
| Confirm that `changes_requested` stays a hard refusal (carried unchanged) | DECISION | D06 item 3 | Already recommended; no new work |
| No change to PR 686 (Clay's open rewrite of the watcher), PR 690 (adds `/sc:issue --plan`) or `/sc:pr-submit` from this verdict | PR KEEP | PR 686, PR 690, `src/superclaude/skills/sc-pr-submit-protocol/` | None |

## Implications

- **OA-13a, go lifetime.** Coordinator: the merge verb has no age refusal in the first build; a coordinator session that stays open for days can hold a go typed in that same live conversation, which WC:241 does not re-confirm, so the real guards are the head pin, the second gate run and the owner's revoke. Watcher and poll: no effect. Claim pipeline: none. Dashboard: none. What breaks: nothing built; the OURS paper's "exactly three ways" must read as the Q01 item 5 default, since D06 item 1 says "expires".
- **OA-13b, hold.** Coordinator: the merge gate gains the held state and the 60-minute wait from the final head's checks finishing. Watcher: PR 686 already parses a per-repo `reviewers` key (D06 Actions row on `issue_watch/repos.py`); write protection for that key is still needed. `/sc:pr-submit` is untouched. A repo with a reviewer that never reviews dead-waits 60 minutes at each merge until the owner sets `reviewers` correctly.
- **OA-13c.** No change; the gate reason `changes_requested` stays unoverridable.
- **OA-25a, reminder.** Dashboard and sweep: today they show Orca session row ids only (`sweep/models.py:265-266`), so a PR waiting for a go has no age or entry on any built surface; the display needs the entry-line writer (QG2/OD-5) and the OAG2 decision on what the observer may show. Report: the work report is configured for one named person today. Notice: no sender, no cap number, no interval until the owner rules; INV-023 stays a MEDIUM, narrowed by display, not closed.
- **OA-25b, silence.** Cap: at cap 1 one unanswered merge go holds the only slot and the repo stalls visibly but quietly; raising the cap is OA-14 and needs the isolation, closing-writer and concurrency tests. A hand-back waiting for re-approval is carried by status `escalated` with step `handback_awaiting_approval` (QG1/OD-13, side effects UNVERIFIED); its expiry has no default number.
- **What the owner must know.** Everything here is defaults on unbuilt code. The only owner inputs are three numbers or choices (go age, hold minutes, push notice), and none blocks the spec. Clay's rulings 6 and 39 behind ADD4 and the cap are Clay's, not the owner's.

## Confidence

About 78 percent overall: OA-13a 80, OA-13b 70 (the 60 minutes has no source and Codex review timing is unknown), OA-13c 95, OA-25a 75, OA-25b 85. The debate reached 13 of 13 points, but both advocates held the owner's weighting rule and both conceded heavily, so the agreement is partly produced by the rule; the evaluators' independent source checks (three errors in the OURS paper, one in the CLAY paper) carry more weight than the agreement. What would change it: a recorded incident of a stale go firing or being forgotten (would move OA-13a toward a clock); the owner choosing a clock number; evidence that Codex reviews late or never by default (would move the 60 minutes); a finding that the sweep or observer cannot show a waiting go to the owner (would pull the push notice forward); an owner record that settles cap 5.

## Unverified

- The 60-minute hold default and the 24-hour go expiry: no source gives either (D06 item 1, RK-30, the merged requirements).
- Whether Codex reviews on every push (decides how often the 60-minute hold dead-waits); D06 lists it as unverified and nothing here tested it.
- Whether the sweep or observer will show a waiting go with its age: today the sweep lists Orca session row ids only (`sweep/models.py:265-266`); whether an idle coordinator session waiting for a go is classified as waiting by the sweep was not tested.
- Whether a coordinator session open for days re-confirms a go typed in the same live conversation: WC:241 says it need not; this is the residual risk and is not tested.
- Clay's rulings 6 and 39: I read the design's text and the merged requirements' statement that they are Clay's; I did not read Clay's `RULINGS.md`. I did not search the owner's chat history for any owner ruling on the cap.
- `clickup.py dm` exists (`agent-work-report/scripts/clickup.py:2-6`) but sends to the token owner's own DM; not verified that it could reach the repository owner.
- The go entry and the merge verb (requirements rows 28 and 29) are DESIGN ONLY; nothing in this verdict is shown to run.
- The carrier `escalated` with step `handback_awaiting_approval` for a waiting re-approval is a QG1 recommendation with unchecked side effects (QG1 open points).
- Scoring: the quantitative layer was estimated by hand; the qualitative layer came from two same-family evaluator agents in opposite order.
- Process: two follow-up messages to the Round 1 advocates were never answered; two fresh agents answered the forced round. Round 2, the invariant probe and Round 3 were skipped by the quick depth.
- D06 item 1 ("expires") and Q01 item 5 (no clock) are worded differently and the owner has not chosen between them.

## Debate artifacts

- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/merged-output.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/adversarial/variant-1-original.md` and `variant-2-original.md` (same folder)
- Skill status: the adversarial skill ran at depth quick (two advocates in one round, one forced round for the surface level, two scoring passes in opposite order, merge-executor); status success, with the independence caveat in Confidence. Note: `merged-output.md` defines "reminder" as display plus age; this verdict's wording rule (Winning recommendation) supersedes that definition.
