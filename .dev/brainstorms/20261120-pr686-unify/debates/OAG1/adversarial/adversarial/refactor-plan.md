# Refactoring Plan (OAG1)

## Overview

- Base variant: Variant 1 (OURS), `variant-1-original.md`
- Incorporated variant: Variant 2 (CLAY), `variant-2-original.md`
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/merged-output.md` (a merged position on OA-13 and OA-25, five sub-questions)
- Planned changes: 9 (6 incorporated strengths from CLAY, 3 base corrections); rejected alternatives: 4
- Overall risk: Low to Medium (text only; no code or GitHub action)

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|--------|--------|----------------|----------|------------------------------|------|
| 1 | Define "reminder" as display plus the age of the wait (since when the item waits), with a push notice reserved | CLAY Claim 3 and Mechanism "Reaching the person"; both advocates (X-002) | Claim 3, Mechanism last bullet | replace | Fixes the base's "no reminder" versus quoted "with a reminder" tension; both advocates agree (85%) | Low |
| 2 | Keep K15's expiry for `waiting_reapproval` only, as an owner-set limit with no default number; state it does not free capacity because that state is outside the cap | CLAY fact 5 (K15) and QG1 OD-13 | new bullet under Claim 3 | append | X-001 resolved by naming two states (90%); corrects CLAY's capacity wording | Low |
| 3 | State both waiting states side by side: waiting merge go (worker done, PR open, counts toward `max_in_flight`, never expires) and waiting re-approval (no worker, no PR, outside the cap) | Diff X-001; base fact 5 corrected | Cited facts item 5 | restructure | Base fact 5 credited a K9 quote to QG1 OD-13 | Low |
| 4 | Reserve a go age check for the merge-automation build: that build must carry an age check and must refuse to start unless the owner recorded a number or the explicit value "none"; no key is added now | CLAY Claim 1 and both advocates' optional key | Claim 1 and Mechanism | append | Both advocates endorse an optional key; no merge verb or automation exists (A-001), so the rule is a requirement on the future build, not a config key today | Medium |
| 5 | Say that the merge-time hold clock starts when the final head's checks finish (60 minutes, UNVERIFIED, owner-settable) | CLAY ADD4 (D:138) and D06 item 4 | Claim 2 | insert | CLAY advocate: base never says when the clock starts; D06 item 4 already says it | Low |
| 6 | Add the existing re-listing surface: the daily report keeps an unanswered entry (`agent-work-report/SKILL.md:22,30`), with the caveat that it is configured for one named person today; the sweep and observer are the owner's surfaces | CLAY fact 8; A-005 | Mechanism last bullet | append | Both advocates; A-005 QUALIFY | Low |
| 7 | Correct the D06 reading: D06 item 1 says the go "expires (number is an Owner DECISION)"; Q01 item 5 says a go ends on action, head move or revoke; the spec takes Q01 item 5 as the default and records the D06 wording as the owner's open option | Verified source error (evaluators) | Claim 1 and fact 1 | replace | OURS "exactly three ways" overstated D06 | Low |
| 8 | Add the omitted half of D:1177: the same row also says "Settled as recommended (ruling 39)" for a cap of 5, which is Clay's ruling (D11); the owner has not ruled | Verified source error (evaluators) | Cited facts item 6 | replace | Selective quote | Low |
| 9 | Add OA-13c as a plain sentence in the claims: `changes_requested` stays a hard refusal (D06 item 3, D:583) | Base fact 8; CLAY omission | Claim 2 | insert | Both agree; CLAY omitted it | Low |

## Changes NOT Being Made

| Diff point | CLAY approach | Why the base approach stands |
|------------|---------------|------------------------------|
| C-001 | A go dies after N hours (24 suggested) | No sourced number (RK-30, D06 item 1), no cited incident, covered by the sha pin, the second gate run and WC:241; the CLAY advocate conceded no clear benefit (85%) |
| C-003 | A push reminder through the notice step in the first build | No notice sender exists in master, pr-a or pr-p (QG2); the cap is Clay's ruling; the push stays reserved behind QG2/OD-5's three triggers |
| C-004 (merge go) | An expiry frees a long-waiting merge go's slot | A waiting merge go has a finished worker and an open PR; an expiry would drop committed work (K9, INV-023) |
| C-002 (ADD4 sentence) | "An agent that never showed activity is no longer skipped" | D06 item 4 overrode it: the skip rule stays inside the `/sc:pr-submit` fix loop and the hold lives at the merge decision |

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 4 | Medium | A future build might read the reservation as a config key request | Strike the sentence; the base rule still holds |
| 1, 2, 3, 5, 6, 7, 8, 9 | Low | Text corrections | Revert the sentence |

## Review Status

Auto-approved (unattended mode, no person present).
