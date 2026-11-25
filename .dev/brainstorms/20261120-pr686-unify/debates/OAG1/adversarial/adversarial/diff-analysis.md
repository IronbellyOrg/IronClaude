# Diff Analysis: position paper comparison (OAG1, merge go lifetime and waiting policy)

## Metadata

- Generated: 2026-11-20
- Variants compared: 2 (variant-1 = OURS, variant-2 = CLAY)
- Total differences found: 13 diff points (structural 1, content 5, contradictions 2, shared assumptions 5), plus 6 unique contributions
- Categories: structural (1), content (5), contradictions (2), unique (6), shared assumptions (5)
- Taxonomy levels: L1 surface 1 (S-001), L2 structural 4 (C-002, C-003, A-002, A-005), L3 state mechanics 8 (C-001, C-004, C-005, X-001, X-002, A-001, A-003, A-004)

Source requirement list used for coverage (no formal IDs in the papers): the sub-questions of the topic block OA-13a, OA-13b, OA-13c, OA-25a, OA-25b.

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Order of the Mechanism section | Leads with the go entry, the second gate run and the live-conversation rule (WC:241), then waiting display | Leads with go lifetime (one comparison in the merge verb), then reviewer hold, notice, waiting rule | Low (L1, same sections in the same order of headings) |

## Content Differences

| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity |
|---|-------|---------------------------|---------------------------|----------|
| C-001 | OA-13a: does a recorded merge go expire by the clock | No clock expiry; a go ends on the named action, a head move or a new gate reason, or an owner revoke in chat; merge automation stays off until the owner records a number | A go dies after N hours (24 suggested, UNVERIFIED) even if the head did not move; one comparison next to the sha comparison | High (L3) |
| C-002 | OA-13b: merge-time hold for a silent reviewer, and how long | D06 item 4 as adopted: owner-set `reviewers` list, re-request on the final head, 60 minutes UNVERIFIED, then escalate; `/sc:pr-submit` skip rule unchanged | ADD4 (D:138): hold when a listed reviewer shows no activity or has not finished, 60 minutes after the head's checks finished, then escalate as row 9; the stated number is the same 60 | Low (L2: the two papers differ only in whether ADD4's sentence "no longer skipped" is kept, which D06 already overrode) |
| C-003 | OA-25a: does a waiting go get a reminder, at what interval | No push reminder in the first build; entry shown as waiting on a person with the age of the wait; push notice reserved by QG2/OD-5 | A reminder through the notice step (nine-row table, `reach_daily_max`); no interval number given in the paper beyond "N hours" | High (L2) |
| C-004 | OA-25b: what owner silence means on a waiting go | Silence is never a yes; no expiry drops committed work; a waiting go counts toward `max_in_flight` | Silence is never a yes (Clay's ruling 24); an expiry applies only to a state with nothing to lose (`waiting_reapproval`, K15) and to a clock check on the go itself | Medium (L3) |
| C-005 | OA-13c: `changes_requested` | Hard refusal, carried unchanged (D06 item 3) | Hard refusal (design D:583) | Low (L3, agreement) |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Whether a waiting item counts toward `max_in_flight` and whether it expires | Cites "QG1 OD-13 and K9 and INV-023" for "an issue waiting for a push or merge go counts ... never expires". Citation check: that quoted text is K9 (`merged-requirements.md:311`). QG1 OD-13 says the opposite for a different state: a hand-back waiting for re-approval does NOT count (`debates/QG1/VERDICT.md:30-34`) | K15 (`merged-requirements.md:317`): `waiting_reapproval` is outside the cap and expires to `stopped` after an owner-set limit | High: not a true opposition once the two states are separated (waiting merge go: worker done, PR open, counts, no expiry; waiting re-approval: no worker, no PR, excluded from cap). The OURS paper blurs them in its fact 5; the verdict must state both states |
| X-002 | Is there a reminder or not | OURS claim 3 says "no new push reminder", yet its fact 5 quotes K9 "shown ... with a reminder" and S15b repeats "shown with a reminder (INV-023, OA-25)" | CLAY: the reminder is the notice step | Medium: the merged requirements already expect a "reminder" for a waiting go and leave its channel open (OA-25 options). The verdict must define "reminder" (display versus push) |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | OURS | WC:241 bounds a stale instruction by conversation: outward action needs the instruction in the live conversation or a confirmation at the moment of action. A go recorded in an earlier session is re-confirmed | High |
| U-002 | OURS | The sha pin plus the second gate run already catch code change after the go (D06 items 1 and 2) | High |
| U-003 | OURS | Event-based endings elsewhere in the contract ("A commit grant covers one Task and ends at that Task's `worker_done`") | Medium |
| U-004 | CLAY | `answer-check` already applies a freshness idiom ("newer than the entry's last edit", D:694), so a freshness refusal fits the design | Medium |
| U-005 | CLAY | A ClickUp DM sender for the report notice exists (`agent-work-report/scripts/clickup.py:2-6`, subcommand `dm`), tied to the token owner's own DM | Medium |
| U-006 | CLAY | ADD4 and OD4 state the number 60 and the stop (escalate as row 9); the daily 07:00 wake exists (`agent-work-report/SKILL.md:30`) and an unanswered entry stays (`SKILL.md:22`) | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The go entry and the merge verb exist. They do not: requirements rows 28 and 29 are DESIGN ONLY; both papers argue rules for code nobody has built | Both papers describe verb checks as if available | A rule decided now binds a build later; testable only after S-stage build | UNSTATED, promoted |
| A-002 | The owner is reachable within days. A cap-1 repo with an unanswered go stalls; neither paper states how long a stall is acceptable | Both treat "waiting" as a short state | Decides whether any clock is worth it | UNSTATED, promoted |
| A-003 | The 60-minute hold is a sensible default; no source gives it (RK-30), and whether Codex reviews on every push is unverified (D06) | Both accept 60 | A wrong number dead-waits or merges early | STATED (UNVERIFIED in both) |
| A-004 | A stored go can be acted on by something other than the person in a live conversation. If merges are only ever done in a live person session (WC:241), a go expiry has little to guard; if automation fires them, it matters | Both argue the go's lifetime without stating who consumes it | Decides whether expiry is a live risk now or only when automation is on | UNSTATED, promoted |
| A-005 | The report or notice reaches the owner (`ironbelly`). The work report is tied to one person in config (`"person": "clayphi"`, D11 verdict); the sweep and observer are the owner's surfaces | Both use the report as a reminder surface | A reminder through a surface the owner does not read is no reminder | UNSTATED, promoted |

## Summary

- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 6
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, X-001
- Factual corrections found in this step (carried to the verdict): (1) ADD4 states 60 minutes, so the topic's "no stated wait" for CLAY is inaccurate; (2) OURS fact 5 attributes the K9 quote to QG1 OD-13, which rules the other way for a different state; (3) OURS says no reminder while quoting K9's "with a reminder".
