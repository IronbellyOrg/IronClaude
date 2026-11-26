review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R3 |
| L2 | open | yes | overlap | MAJOR | - | R3, R1, R2 |
| L3 | open | yes | single | CRITICAL | - | R1 |

## Blocking findings

### L2

#### L2.t2b-1 (F2)

- claim: Constraints point to Task 6 for the fresh-session check, but Task 6 is changelog and the proof is Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"

#### L2.t2b-1 (F3)

- claim: Constraints limit the hook to bash plus jq while Task 1 allows awk tokenising.
- anchor: "The hook script is bash plus `jq`, modelled on `src/superclaude/hooks/scripts/freshness-pre-edit.sh`"
- anchor2: "Tokenising is done in `jq` (regex `match`/`scan`) or `awk`, not a per-character bash loop"

#### L2.t3-1 (issue-read)

- claim: The candidate omits the source's explicit instruction to read the entire issue before implementation.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L2.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a hook that allows `bash -c "python3 x.py"`, and that is wrong because the child shell executes bare `python3` despite the goal requiring such command execution to be blocked.
- anchor: "bash -c \"python3 x.py\" (quoted text)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t4-1 (F2)

- claim: The driving document requires reading issue #357 in full before implementation, but the candidate does not state that prerequisite.
- anchor: "Requirements come from issue #357"

### L3

#### L3.t3-1 (bash-c-bypass)

- claim: An implementer following the allowed-case rule and test builds a hook that permits bash to run bare python3, bypassing the stated block.
- anchor: "bash -c \"python3 x.py\" (quoted text)"

## Other findings

- L1 (MAJOR, open, single): Allowed list has no `;` chain, so the AC as listed cannot be shown without adding one extra allowed case.

## Reviser brief

Blocking finding ids: L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
