# Adversarial Debate Transcript (OAG1)

## Metadata

- Depth: quick
- Rounds completed: 1 (Round 1) plus 1 forced round for taxonomy level L1; Round 2, Round 2.5 (invariant probe) and Round 3 skipped by depth (quick)
- Convergence achieved: see Convergence Assessment
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 = OURS, Variant 2 = CLAY); both were told the owner's weighting rule, which can lower the independence of their agreement
- Round 1 execution note: the two advocates ran as parallel nested agents (read-only, no file writes); their answers are reproduced below in condensed form without changing positions

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)

**Position.** A merge go should end by event (action done, head move or new gate reason, owner revoke), not by an unsourced clock (RK-30; `merged-requirements.md:685`). One CLAY piece is adopted as a hybrid: a clock check as an optional owner-set key, absent by default.

**Steelman of CLAY.** A go is only as fresh as the person's memory; the sha pin does not catch changed intent; a cap-1 repo with one unanswered go stalls quietly (RK-21, INV-023, both UNADDRESSED). CLAY's 60-minute hold is a stated rule with a stop and fills a verified gap in the skip rule (`reviewers.py:390-391`, `:414-419`). D06 item 1 itself says the go "expires (number is an Owner DECISION)". CLAY limits expiry to states with no committed work (K15).

**Strengths claimed.**
1. The pin already covers the main risk: a one-shot go bound to a sha, void on head move or new gate reason, with the gate run again before `gh pr merge --match-head-commit` (D06 items 1 and 2).
2. Staleness is handled by conversation: WC:241 requires the instruction in the live conversation or a confirmation at the moment of action. A clock matters only if something other than a live session consumes a stored go, and automation is off (OA-13, `merged-requirements.md:685`).
3. The contract ends grants by event (commit grant ends at the Task's `worker_done`).
4. It invents no unsourced number (RK-30).
5. Display exists today: `sweep/report.py:682-685` and `agent-work-report/SKILL.md:22` (unanswered entry stays).

**Weaknesses identified in CLAY.**
1. The expiry benefit is argued, not evidenced: no incident of a stale go firing is cited; D06 gives no number or clock rule.
2. ADD4 and `reach_daily_max` are Clay's rulings, not the repository owner's (D11 verdict); 24 hours is UNVERIFIED.
3. The reminder channel does not exist (CLAY concedes no escalation sender); the one DM sender goes to the token owner's own DM (`clickup.py:2-6`).
4. K15 governs a different state (`waiting_reapproval`: no worker, no PR, outside the cap), so it does not support a clock on a waiting merge go.

**Concessions.** ADD4 does state 60 minutes (the topic's "no stated wait" was wrong). OURS fact 5 attributes the K9 quote to QG1 OD-13, which rules the opposite for a different state (the answer stands once the two states are named). "No reminder" collides with K9's "with a reminder" (the answer stands once reminder is defined as display plus age; push waits for QG2/OD-5's three triggers). D06 item 1 says a go "expires", so "exactly three ways" overstates D06; the open point is the number and clock rule, and OA-13 lists "no expiry" as an owner option. A stalled cap-1 repo is quiet; accepted as a cost.

**Shared assumptions.** A-001 QUALIFY (rows 28 and 29 are design only; record the rule as owner-set configuration, not hard-coded numbers). A-002 QUALIFY (reachability unproven; display the age of the wait). A-003 ACCEPT as UNVERIFIED (60 is a default only). A-004 REJECT as stated (WC:241 ties a go to a live conversation; expiry is a live risk only if automation is turned on). A-005 ACCEPT (the report is tied to one person; use the sweep and observer).

**Proposed answers.** OA-13a: no clock expiry by default; hybrid: the CLAY one-comparison refusal as an optional per-repo key, absent means none. OA-13b: the 60-minute hold as D06 item 4 has it; take CLAY's explicit statement that it is measured from when the head's checks finished. OA-25a: no push reminder in the first build; show "waiting on a person" with the age of the wait; push reserved behind QG2/OD-5's three triggers. OA-25b: silence is never a yes; a waiting merge go keeps its slot, counts toward `max_in_flight`, never expires away committed work; `waiting_reapproval` expires to `stopped` under K15 as a separate state. OA-13c: hard refusal.

### Variant 2 Advocate (CLAY)

**Position.** OURS should win OA-13a and OA-25b as written; no clear CLAY benefit there. Three separable CLAY pieces are worth taking as hybrids: a defined start for the 60-minute hold clock, the K15 expiry kept for `waiting_reapproval` only, and a definition of "reminder" that fixes OURS's internal inconsistency.

**Steelman of OURS.** The pin and the re-run gate catch what a clock would guard against; a go also ends on use, head move, new gate reason or revoke. WC:241 bounds stale consent by conversation; the contract ends a commit grant by event; OA-13 keeps merge automation off until the owner answers; RK-30 flags 24 hours as unsourced; OURS declines to build a sender QG2 could not find; it never drops committed work (K9, INV-023). A consistent, low-invention position.

**Strengths claimed.**
1. A stated, anchored hold (ADD4, D:138): 60 minutes after the head's checks finished, stop and escalate as row 9, `reviewers: none` as the explicit exception. The OURS paper never says when the clock starts.
2. A real gap in the skip rule: `merge_wait` reads "one done plus one absent" as clean (`reviewers.py:414-419`). Both papers adopt the hold, so this does not separate them.
3. The `waiting_reapproval` expiry (K15, `merged-requirements.md:317`) is separable from go expiry; that state has no worker and no PR.
4. A freshness idiom exists (D:694); weak support, since it concerns typed answers.

**Weaknesses identified in OURS.**
1. Citation blur in fact 5 (K9 quote credited to QG1 OD-13).
2. X-002: "no reminder" against the quoted "with a reminder"; the word is never defined.
3. The stall is acknowledged but not bounded: cap 1, one unanswered go holds the only slot (RK-21, INV-023 MEDIUM, UNADDRESSED); no threshold changes the display.
4. The 60-minute hold has no clock start in the OURS paper.

**Concessions.** No incident of a stale go is cited; the 24-hour number has no source (D06 item 1, RK-30); sha pin, second gate run and WC:241 cover the stale-code case; an expiry on a waiting merge go would drop committed work, which INV-023 and K9 forbid. No escalation notice sender exists (QG2); the `dm` subcommand sends to the token owner's own DM and was not verified to reach the repository owner. ADD4's "owner ruling 6" is Clay's ruling (D11 treats it so). C-002 differs almost nowhere (D06 item 4 already overrode ADD4's "no longer skipped"). C-005 is agreed.

**Shared assumptions.** A-001 ACCEPT (write each rule as a testable refusal with a named reason). A-002 QUALIFY (show the age rather than set a clock; UNVERIFIED). A-003 QUALIFY (60 is an owner-settable test default, not settled policy; RK-30). A-004 ACCEPT (supports OURS on C-001; an expiry matters only when automation is on). A-005 QUALIFY (the report is tied to one person in config; the sweep and observer are the owner's surfaces).

**Proposed answers.** OA-13a: no clock expiry by default (OURS wins); hybrid: an optional `go_max_age_hours`, absent means no expiry; merge automation must refuse to start unless the owner recorded a number or an explicit "none"; no default number (24 UNVERIFIED). OA-13b: D06 item 4 plus ADD4's anchor: 60 minutes after the head's checks finished (UNVERIFIED, owner-settable); re-request on the final head, escalate as row 9; `reviewers: none` the one recorded exception; the skip rule in `/sc:pr-submit` unchanged. OA-25a: define reminder as display, not push; age of the wait; the existing daily 07:00 wake re-shows an unanswered entry (`agent-work-report/SKILL.md:22,30`), so the cadence is daily with no new sender; a push through the notice step stays reserved. OA-25b: silence never a yes; a waiting merge go counts and never expires away committed work; `waiting_reapproval` outside the cap and expires to `stopped` after an owner-set limit (K15, no sourced number). Name both states.

## Forced Round: taxonomy level L1 (surface)

Trigger (AC-AD5-1): after Round 1 neither advocate had addressed S-001 or any other surface-level point, so level L1 had zero coverage and convergence was blocked until a forced round ran. Note on execution: the first request went to the two Round 1 advocates by message and was never answered in this run; it was replaced by two fresh agents given the same question and the same files. Their answers:

**OURS-side agent.** Steelman of CLAY: opening with go lifetime puts the one open owner decision (OA-13a) first. Order: use OURS, with one change: put a single sentence stating the lifetime rule at the top, then define the go entry, then when it ends, then the second gate run and WC:241, then the reviewer hold, then waiting; CLAY uses "the go entry already carries times" before the entry is defined. Words to fix: go (the person's recorded consent for one named action); ends (event-based close); expires (clock-based close only; under OURS no go expires and K15's `waiting_reapproval` is the only expiry); hold (the merge-time stop for a silent listed reviewer); waiting (a finished worker with an open PR awaiting a person); reminder (a push message, which the first build lacks; showing the age of a wait is "shown", not a reminder). Winner: OURS at about 60%.

**CLAY-side agent.** Steelman of OURS: defining the go entry first, with its sha pin, second gate run and WC:241, lets "no clock expiry" read as a conclusion. Order: use CLAY's order with one change: a one-line definition of "go" first (CLAY never defines it), then the lifetime rule, then the hold, then the notice, then the waiting rule; readers look up lifetime and waiting rules, and the mechanism supports them. Words to fix: expires (clock end only; an event end is "void" or "consumed"); go (one typed consent for one action, bound to a sha); hold (the merge-time refusal for a silent reviewer); reminder (a push notice, not a report line); waiting (a state shown with its age; call the 60-minute reviewer wait a "hold" so the words do not clash). Winner: CLAY at 60%.

**Orchestrator reading.** Each side argued the other side's order is slightly better once a one-line definition of "go" opens the text, so the point is a draw with a shared change: define "go" first, then the lifetime rule, then end conditions, gate, hold and waiting. Both agents also fixed the word "reminder" to mean a push message, which differs from the merged-output.md Terms definition ("display plus age"). The verdict adopts the forced-round wording: the spec says "shown with the age of the wait" for the display and "push notice" for a message, and uses the word "reminder" only when quoting K9 or S15b (whose "with a reminder" is a placeholder for the open OA-25 channel). Where merged-output.md Terms says otherwise, VERDICT.md supersedes it.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|------------------|
| S-001 | L1 | Draw, resolved as a hybrid: OURS order with a one-line definition of "go" first; fix the words ends, expires, hold, waiting, push notice | 60% | Each forced-round agent said the other order is slightly better once "go" is defined first; both fixed "expires" to clock-only |
| C-001 | L3 | Variant 1 (OURS), with a reserved clock check | 85% | Both advocates concede the clock has no sourced number and no incident; pin, second gate run and WC:241 cover stale code; CLAY advocate conceded no clear benefit |
| C-002 | L2 | Variant 1 (OURS = D06 item 4); draw on substance | 80% | Both adopt the owner-set `reviewers` list and 60 minutes UNVERIFIED; D06 item 4 already starts the clock at the final head's checks finishing, so the "anchor" CLAY credits is already in the verdict |
| C-003 | L2 | Variant 1 (OURS), with reminder defined as display plus age | 80% | No sender in master or pr-a or pr-p (QG2); CLAY advocate conceded; the daily report re-lists an unanswered entry (`SKILL.md:22,30`) |
| C-004 | L3 | Split: OURS for a waiting merge go, CLAY (K15) for `waiting_reapproval` | 85% | K9 and INV-023 forbid dropping committed work; K15 and QG1 OD-13 cover the state with no worker and no PR |
| C-005 | L3 | Agreed (carried unchanged) | 95% | D06 item 3, D:583; the CLAY paper omitted it, which its advocate did not dispute |
| X-001 | L3 | Resolved by naming two states | 90% | Waiting merge go: counts, never expires. Waiting re-approval: outside the cap, expires only on an owner-set limit |
| X-002 | L3 | Resolved by defining reminder as display plus age | 85% | K9 and S15b say "with a reminder"; OA-25 leaves the channel open; both advocates agree |
| A-001 | L3 | Accepted (both): write each rule as a testable refusal on unbuilt code | 85% | Rows 28 and 29 DESIGN ONLY |
| A-002 | L2 | Qualified (both): show the age; no clock | 75% | No source for an acceptable stall length |
| A-003 | L3 | Qualified (both): 60 is an owner-settable default, UNVERIFIED | 85% | RK-30, D06 Unverified |
| A-004 | L3 | Variant 1 (OURS); the spec must name who consumes a stored go | 80% | Advocates answered REJECT and ACCEPT in words but agree in substance: expiry matters only if automation consumes the go |
| A-005 | L2 | Qualified (both): the owner's surfaces are the sweep and observer | 80% | D11: work report tied to `"person": "clayphi"` |

## Convergence Assessment

- Points resolved: 13 of 13 (S-001, C-001 to C-005, X-001, X-002, A-001 to A-005); every point has a majority or unanimous agreed resolution, in two cases agreed in substance although the two advocates used opposite words (A-004: REJECT versus ACCEPT; S-001: each side picked the other's order)
- Alignment: 100% (13 of 13); minimum point confidence 60% (S-001)
- Threshold: 80%
- Taxonomy coverage: L1 covered by the forced round (S-001), L2 by C-002, C-003, A-002, A-005, L3 by C-001, C-004, C-005, X-001, X-002, A-001, A-003, A-004
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Status: CONVERGED
- Unresolved points: none
- Independence caveat: both advocates were given the owner's weighting rule and both conceded most of the opposing points on the first round (the CLAY advocate said OURS "should win OA-13a and OA-25b as written"; the OURS advocate adopted two CLAY hybrids), so the 100 percent is partly produced by the rule. The two evaluators' source checks were independent of the advocates and found three errors in the OURS paper and one in the CLAY paper (diff-analysis.md summary; base-selection.md "Source errors"); those, not the agreement, are the strongest evidence in this debate.
- Known process gaps: two reply messages sent to the Round 1 advocates (to ask the forced-round question) never came back; fresh agents answered instead. Round 2, the invariant probe and Round 3 were skipped by the quick depth.
