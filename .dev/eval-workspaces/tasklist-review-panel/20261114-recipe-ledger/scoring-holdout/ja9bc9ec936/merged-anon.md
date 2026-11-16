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
| L1 | open | yes | overlap | MAJOR | - | R3, R1 |
| L2 | open | yes | overlap | CRITICAL | - | R3, R1, R2 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MAJOR | - | R3 |
| L5 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Hook built as written allows sudo -u root python3 and nice -n 10 python3 because options after sudo and nice are not skipped.
- anchor: "`sudo`, `exec`, `nohup`, `time`, `nice`, `env` (plus its following options and `NAME=value` words)"

#### L1.t2b-1 (F5)

- claim: Timeout option forms are undefined, so timeout -s KILL 30 python3 can be allowed or blocked depending on the implementer guess.
- anchor: "`timeout` (plus its options and its duration argument)"

#### L1.t3-1 (F1)

- claim: An implementer following these rules allows echo "$(python3 -c 1)", which executes bare Python inside a double-quoted command substitution.
- anchor: "Text inside single quotes, and text inside double quotes, is never a command word"
- anchor2: "bash -c \"python3 x.py\" (quoted text)"

#### L1.t3-1 (F4)

- claim: The wrapper rules do not specify parsing sudo or command options, so commands such as sudo -u root python3 x.py may be allowed despite running bare Python.
- anchor: "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env`"

### L2

#### L2.t2b-1 (F2)

- claim: Constraints cite Task 6 for the fresh-session check, but Task 6 is the changelog entry and Task 7 is the fresh-session proof.
- anchor: "The live fresh-session check in Task 6 registers the hook"

#### L2.t3-1 (F3)

- claim: The source requires reading issue #357 in full before work; the candidate does not explicitly preserve that instruction.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`),"

#### L2.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a hook that allows `bash -c "python3 x.py"`, and that hook is wrong because the nested shell executes bare `python3` while the hook is required to block it.
- anchor: "`bash -c \"python3 x.py\"` (quoted text)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t4-1 (F2)

- claim: The source requires reading the issue in full first, but the candidate only directs attention to selected sections.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L2.t4-1 (F3)

- claim: The safety constraint points to Task 6 for the live-session check, but that check is specified in Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook"

## Other findings

- L3 (MAJOR, open, single): Task 5 has no Depends line yet needs the Task 1 hook, and Task 6 claims the Task 5 fix without depending on Task 5.
- L4 (MAJOR, open, single): Task 7 runs from /tmp but names settings and artifacts as ./artifacts paths, which do not resolve there without absolute paths.
- L5 (MAJOR, open, single): The constraint assigns the fresh-session check to Task 6, but Task 6 is the changelog task and Task 7 contains that check.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
