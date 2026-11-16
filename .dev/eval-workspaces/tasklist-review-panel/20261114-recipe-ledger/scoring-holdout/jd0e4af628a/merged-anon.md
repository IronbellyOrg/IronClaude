review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R2 |
| L2 | open | yes | overlap | MAJOR | - | R2, R1 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | yes | overlap | CRITICAL | - | R2, R3 |

## Blocking findings

### L2

#### L2.t2b-1 (F2)

- claim: Constraints place the fresh-session proof in Task 6, but Task 6 is the changelog entry and the live check is Task 7; the number should read Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary"

#### L2.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a hook that allows bare python3 through bash -c, and that is wrong because it contradicts the goal of blocking commands that run bare Python.
- anchor: "bash -c \"python3 x.py\""
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t4-1 (F2)

- claim: The candidate does not carry forward the driving document's instruction to read the issue in full before implementation.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L2.t4-1 (F3)

- claim: The constraint points to Task 6 for the fresh-session check, but Task 6 is the changelog task and Task 7 contains that check.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary"

### L4

#### L4.t2b-1 (F4)

- claim: Heredoc scanning, backslash-escape quote tracking, and command/time/nice wrappers are specified in Task 1 but no Task 2 case exercises them, so regressions pass.
- anchor: "Lines of a heredoc body are scanned like ordinary lines"
- anchor2: "Backslash escapes outside single quotes are honoured when tracking quotes."

#### L4.t3-1 (F1)

- claim: The hook can miss an executable command word written as "python3", allowing a bare Python invocation through the stated block.
- anchor: "text inside double quotes, is never a command word"

## Other findings

- L1 (MAJOR, open, single): The AC requires chained `;` in both blocked and allowed cases, but the allowed list has no unquoted `;` separator case (only quoted `;` inside the read-parse python -c string).
- L3 (MAJOR, open, single): The grep check passes code literals only when followed by a quote or delimiter, so natural unquoted comparisons or a space-separated pattern list fail the AC even though the script makes no Python call.

## Reviser brief

Blocking finding ids: L2, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
