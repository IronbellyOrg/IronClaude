review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: docs/designs/surgical-remediation.md sha256 fb26244a2f37a20f9d179383ebb0dc27b54ebe66b641e6acfff0043adc084a64
reviewers:
- t1b-1: report .dev/spec-panel/surgical-remediation/round-1/t1b-1.md, block ok true
- t2-1: report .dev/spec-panel/surgical-remediation/round-1/t2-1.md, block ok true
- t3-1: report .dev/spec-panel/surgical-remediation/round-1/t3-1.md, block ok false
- t3-2: report .dev/spec-panel/surgical-remediation/round-1/t3-2.md, block ok false

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 3, 5.1 | t1b-1 |
| L2 | open | no | overlap | MAJOR | 4.1, 4.2, 5.2, 5.3, 6, 7, 9 | t1b-1, t3-1 |
| L3 | open | no | overlap | MAJOR | 4.4, 5.1, UC-1 | t1b-1, t3-1 |
| L4 | open | yes | overlap | CRITICAL | 3, 4.3, 7, 9 | t1b-1, t2-1 |
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

### L4

#### L4.t1b-1 (F5)

- claim: The old package can be archived when the new package is only a failed directory, and a normal generation that includes Wave 4R has no bound on regenerate loops.
- anchor: "archives the old package with a `SUPERSEDED` line once the new package exists"
- anchor2: "runs a normal generation into a new package, runs Wave 4 on it"

#### L4.t1b-1 (F7)

- claim: An input with B=0 and H>=6 or M>=10 matches both the None row and the regenerate row, and no first-match rule is stated.
- anchor: "**None.** The plan stands; Medium and Note findings are written to the contract as follow-up candidates"
- anchor2: "any of `B >= 4`, `H >= 6`, `M >= 10`"

#### L4.t1b-1 (F8)

- claim: H and M thresholds send a plan to regeneration, but regeneration fixes only blockers, so reviewed text is discarded with no repair for the findings that triggered it.
- anchor: "a new source (the old `source.md` plus a section that lists the blocking findings to fix)"
- anchor2: "any of `B >= 4`, `H >= 6`, `M >= 10`"

#### L4.t2-1 (F1)

- claim: A plan with zero blockers matches both the None row and the Surgical row, so one implementer ships no-op while another archives and replaces a good plan.
- anchor: "`B == 0` | **None.** The plan stands;"
- anchor2: "`B <= 3` and `H <= 5` and `M <= 9` | **Surgical** (section 4)"

## Other findings

- L1 (MAJOR, open, single): H counts a HIGH label that Wave 4 pre-mode reviewers never emit (they return CRITICAL, MAJOR or MINOR), so the owner's high-severity guard never fires.
- L2 (MAJOR, open, overlap): The text does not say which review is the re-review, and reflect_status and reflect_report_path cannot hold its verdict, and no contract field exists for the follow-up candidates section 3 says are written there.
- L3 (MAJOR, open, overlap): --revise takes only a REPORT.md, but the counts that choose the route exist only in reflect's return-contract.yaml, so the route cannot be chosen for an outside review.
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

Blocking finding ids: L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
