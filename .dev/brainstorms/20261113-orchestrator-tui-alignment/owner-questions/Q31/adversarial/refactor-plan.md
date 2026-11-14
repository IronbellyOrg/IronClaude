# Refactoring Plan: Merge into Base (Variant 3, proposal-C)

## Overview
- Base: Variant 3 (proposal-C)
- Incorporating strengths from: Variant 1 (proposal-A), Variant 2 (proposal-B), and the advocates' concessions
- Planned changes: 6
- Risk level: Low (all wording or added lines; the answer itself does not change)

## Planned Changes

### Change 1: Idle-only firing (from shared assumption A-002)
- **Source**: diff-analysis A-002; all three advocates ACCEPT
- **Target**: Base, "What happens next", cron bullet (insert)
- **Rationale**: CronCreate fires only while the session is idle; "about every 10 minutes" is a ceiling while the coordinator works (A-002, 60%)
- **Integration point**: add "it fires only while the coordinator session is idle, so a long busy turn delays it"
- **Risk**: Low, additive

### Change 2: Correct the overstatement about non-worker peers (from Variant 3 advocate concession)
- **Source**: round1-advocate-3.md, Concessions, "Overstated claim"
- **Target**: Base, "What it unlocks", first bullet (replace)
- **Rationale**: WC-16 says person-started sessions appear in the `/sc:sweep` report; that covers them only once SWEEP-RUNNABLE holds
- **Integration point**: "until `/sc:sweep` is runnable, only a timer-driven check sees them go idle"
- **Risk**: Low

### Change 3: Message-less subscriptions (from Variant 3 advocate concession)
- **Source**: round1-advocate-3.md, Concessions, "Never messaged tension"
- **Target**: Base, "What happens next", cron bullet (insert)
- **Rationale**: WC-16: person-started sessions "are never messaged"
- **Risk**: Low

### Change 4: Ledger entry is the coordinator's own record (from Variant 3 advocate concession)
- **Source**: round1-advocate-3.md, Concessions, "Ledger write wording"
- **Target**: Base, "What happens next", expiry bullet (insert)
- **Rationale**: avoids a reading that recording the job id conflicts with line 579 ("or any write")
- **Risk**: Low

### Change 5: Owner's yes as fresh confirmation (from A-001 responses and Variant 1)
- **Source**: diff-analysis A-001; all three QUALIFY
- **Target**: Base, "Answer" (append one sentence)
- **Rationale**: the order is a 9-day-old memory note, the lowest source tier; the owner's answer, not memory, settles it
- **Risk**: Low

### Change 6: Contract promotion as a separate later decision (from Variant 2, U-001)
- **Source**: Variant 2, "Answer" and "What it unlocks"
- **Target**: Base, "What stays unresolved", first bullet (replace)
- **Rationale**: C-002 minority view (Variant 2 advocate) is correct on root cause; all advocates agree it should not be bundled into Q31 (X-002, 95%)
- **Integration point**: "Whether to write the rule into the worker contract for all coordinators is a separate owner decision, best raised as its own item"
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001, X-001 | Variant 1: "no", WC-16 only | All three advocates, including Variant 1's, judged it leaves non-worker peers unwatched while `/sc:sweep` is not runnable (C-001, 90%) |
| X-002 | Variant 2: bind every coordinator through the contract now | Out of the question's scope; Variant 2's advocate conceded (95%) |
| C-007 | Variant 2: settle "is a cron fire a wake" in the contract | Majority judged the bounded UNVERIFIED label sufficient for this program (65%) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 to 6 | Low | Wording only | Revert to base text |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14T00:10:00Z
