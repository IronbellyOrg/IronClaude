review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MINOR | - | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R3 |
| L3 | open | yes | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L2

#### L2.t2b-1 (F2)

- claim: Forwarder wrappers such as `xargs python3` are unwrapped, so a bare python invocation through them is allowed by the hook.
- anchor: "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env` (plus its following options"

#### L2.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds a hook that allows `'python3' -c 1`, and that is wrong because Bash executes the quoted token as the python3 command, bypassing the required bare-command block.
- anchor: "Text inside single quotes, and text inside double quotes, is never a command word"

#### L2.t3-1 (F2)

- claim: The wrapper rules do not specify option handling for sudo, so `sudo -u root python3 x.py` may pass because the parser treats `-u` as the command word.
- anchor: "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env`"

### L3

#### L3.t4-1 (F1)

- claim: The plan explicitly allows this command, although its nested shell runs bare python3, so the hook can be bypassed and the stated blocking behavior is not met.
- anchor: "bash -c \"python3 x.py\" (quoted text)"

## Other findings

- L1 (MINOR, open, single): No allowed case chains with top-level `;`; the only `;` in the allowed list is inside the quoted read-parse line.
- L4 (MAJOR, open, single): The candidate omits the source instruction to read the issue in full before starting.

## Reviser brief

Blocking finding ids: L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
