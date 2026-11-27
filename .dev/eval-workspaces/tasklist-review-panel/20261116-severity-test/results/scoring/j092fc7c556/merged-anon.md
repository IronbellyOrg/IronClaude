review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R3, R2 |
| L2 | open | yes | overlap | CRITICAL | - | R3, R2, R1 |
| L3 | open | no | single | MINOR | - | R3 |
| L4 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L2

#### L2.t2b-1 (F3)

- claim: Quoted-text exemption leaves bash -c with python3 inside allowed, so the inner shell still runs bare python.
- anchor: "`bash -c \"python3 x.py\"` (quoted text)"

#### L2.t3-1 (F1)

- claim: The plan explicitly allows bash -c to execute bare python3 in a child shell, so the hook fails its stated requirement to block commands that run bare Python.
- anchor: "`bash -c \"python3 x.py\"` (quoted text)"
- anchor2: "Goal: A shipped PreToolUse hook on the `Bash` tool refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t3-1 (F2)

- claim: The candidate does not carry forward the driving document's instruction to read the issue in full before implementation.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L2.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a hook that allows `bash -c "python3 x.py"`, and that is wrong because the nested shell runs bare `python3`.
- anchor: "`bash -c \"python3 x.py\"` (quoted text);"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t4-1 (F2)

- claim: The source explicitly requires reading issue #357 in full first, but the candidate does not carry that prerequisite forward.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`),"

## Other findings

- L1 (MAJOR, open, overlap): sudo, nice and time options that take arguments get no skip rule, so sudo -u root python3 x.py is allowed though it runs bare python.
- L3 (MINOR, open, single): A natural detection list written with spaces around separators triggers the self-check grep, so the script needs obfuscation to pass.
- L4 (MINOR, open, single): The subagent proof needs the model to choose the Agent tool, so a single fresh session can fail to spawn even when the hook is correct.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
