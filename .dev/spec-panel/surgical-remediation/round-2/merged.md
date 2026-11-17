review: 2 of 3
# Merged review 2 (coordinator script; panel of 1 reviewers)
candidate: docs/designs/surgical-remediation.md sha256 1333d41ed0abcd621d1c1e1ccca93b086327b475c48342c961ba89171e2ddb76
reviewers:
- t1b-1: report .dev/spec-panel/surgical-remediation/round-2/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 3, 5.1 | t1b-1 |
| L2 | open | no | overlap | MAJOR | 4.1, 4.2, 5.2, 5.3, 6, 7, 9 | t1b-1, t3-1 |
| L3 | open | no | overlap | MAJOR | 4.4, 5.1, UC-1 | t1b-1, t3-1 |
| L4 | regressed | no | overlap | CRITICAL | 3, 4.3, 7, 9 | t1b-1, t2-1 |
| L5 | open | no | single | MAJOR | 4.4, 5.2, 7 | t1b-1 |
| L6 | open | no | overlap | MAJOR | 2, 5.4 | t1b-1, t3-1 |
| L7 | open | no | overlap | MAJOR | 1, 6, 9 | t1b-1, t3-1 |
| L8 | open | no | overlap | MAJOR | 9 | t1b-1, t2-1 |
| L9 | open | no | single | MAJOR | 3, 8 | t2-1 |
| L10 | open | no | single | MAJOR | 4 | t2-1 |
| L11 | open | no | single | MAJOR | 4 | t2-1 |
| L12 | open | no | single | MINOR | 4 | t2-1 |
| L13 | open | no | single | MAJOR | 3, 4.4 | t3-1 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): H counts a HIGH label that Wave 4 pre-mode reviewers never emit (they return CRITICAL, MAJOR or MINOR), so the owner's high-severity guard never fires.
- L2 (MAJOR, open, overlap): The text does not say which review is the re-review, and reflect_status and reflect_report_path cannot hold its verdict, and no contract field exists for the follow-up candidates section 3 says are written there.
- L3 (MAJOR, open, overlap): --revise takes only a REPORT.md, but the counts that choose the route exist only in reflect's return-contract.yaml, so the route cannot be chosen for an outside review.
- L4 (CRITICAL, regressed, overlap): The old package can be archived when the new package is only a failed directory, and a normal generation that includes Wave 4R has no bound on regenerate loops.
- L5 (MAJOR, open, single): Wave 5 does not say which package it writes to, and after escalation an --handoff implement can still run on the original plan with open blockers.
- L6 (MAJOR, open, overlap): Reflect's remediation_plan_path can point at a package that Wave 4R archived, and the headless wrapper's /sc:implement call on it is refused.
- L7 (MAJOR, open, overlap): Other superseded packages, such as removeTheAnyIssu-20261102-042031 and blockerStage4-20261116-030206, stay in to-do/ and the uppercase-token acceptance check does not catch them.
- L8 (MAJOR, open, overlap): The routing rule is prose with no code unit to test, the end-to-end fixture needs live agents, and the fix-map check is self-reported.
- L9 (MAJOR, open, single): HIGH-labeled Medium/Note wording findings count toward forced regeneration even though the severity rule says labels never gate.
- L10 (MAJOR, open, single): Re-archiving onto an existing archive destination nests or clobbers the package because no destination-exists rule and no helper call is specified.
- L11 (MAJOR, open, single): Wave 4 blockers on a regenerated package retrigger regeneration with no cycle cap or escalation.
- L12 (MINOR, open, single): The cited line span covers the REVISE prompt plus the unrelated Findings-block section instead of just the prompt and fix map.
- L13 (MAJOR, open, single): The design never states what Wave 4R does when reflect is unavailable or failed (the SKILL.md:93 path that today proceeds to Wave 5 with an unresolved line), so the route is undefined exactly when the counts do not exist.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
