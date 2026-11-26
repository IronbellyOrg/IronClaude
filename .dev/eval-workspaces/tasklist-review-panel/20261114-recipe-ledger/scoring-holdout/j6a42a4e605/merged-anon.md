review: 1 of 3
# Merged review 1 (coordinator script; panel of 1 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | yes | single | CRITICAL | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Natural detection code must contain python/pip literals, so grep cannot match only comments/message as the acceptance requires.
- anchor: "The script contains no call to `python`, `python3`, `pip` or `pip3`"
- anchor2: "Block when the command word's basename is exactly `python`, `python3`, `pip` or `pip3`"

### L2

#### L2.t2b-1 (F2)

- claim: Fixture creates 12 fake scripts, not the new block-bare-python.sh, so installer reports source missing and all fake-fixture tests fail.
- anchor: "In `tests/cli/test_install_hooks.py`, following `test_real_hooks_json_registers_codegraph_session_start` and `test_codegraph_hook_script_is_packaged_listed_and_mirrored`, add:"

## Other findings

- L3 (MAJOR, open, single): Allowed list has && and | but no ;-chained allowed case, so the acceptance as written lacks a stated case.
- L4 (MINOR, open, single): The modelled helper sends only json.dumps payloads, with no stated path for raw non-JSON/empty stdin tests.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
