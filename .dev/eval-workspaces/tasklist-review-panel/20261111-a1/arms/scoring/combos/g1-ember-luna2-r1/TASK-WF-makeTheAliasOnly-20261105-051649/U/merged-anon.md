review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L4 | open | yes | single | MAJOR | - | R3 |

## Blocking findings

### L3

#### L3.R1 (F4)

- claim: Launcher line anchors have drifted after the pending merge; the spec already marks them re-verify.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777,"

#### L3.R3 (F2)

- claim: The required line-numbered anchor is not the tier-mode block in the current launcher, and the launcher already exports the three model variables with [1m] suffixes, so the specified follow-up would document existing behavior inaccurately and prescribe different values.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L3.R2 (F1)

- claim: The required launcher anchors do not match the current branch base, so the launcher-follow-up spec cannot satisfy the acceptance criterion for accurate quoted line references.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

### L4

#### L4.R3 (F1)

- claim: The retry-names test should pass on the current tree because the retry reference and ledger example already use the required ununderscored names, so the required exact seven-failure result cannot occur.
- anchor: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test, the cleanup-audit test, the retry names test and the mapping document test"

## Other findings

- L1 (MAJOR, open, single): Pin value order is ambiguous against the files; a wrong guess makes the frontmatter test fail on the unchanged tree and breaks the exactly-seven acceptance.
- L2 (MAJOR, open, single): The src-only constraint literally forbids the docs and tests edits the later tasks require.

## Reviser brief

Blocking finding ids: L3, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
