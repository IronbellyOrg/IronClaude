review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R3: report <redacted> block ok true
- R2: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R3 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The plan says non-tier ccsession launches have no model variables set while also requiring the follow-up launcher to preserve inherited values, which can leave them set.
- anchor: "outside a ccsession tier workspace, nothing set"
- anchor2: "a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.R2 (F1)

- claim: The non-tier test clears the inherited variables before launch, so it cannot verify the stated behavior that a non-tier launch preserves inherited values.
- anchor: "the test removes those three variables from the launch environment first"

#### L1.R1 (F3)

- claim: Scratch-copy run understates the module globals the harness needs
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied, run it with `uv run pytest` against the unchanged launcher, and save the output."

## Other findings

- L2 (MAJOR, open, overlap): The planned test does not catch picker IDs passed to slash-command model selectors such as the issue chains' /model lines.
- L3 (MINOR, open, single): Linked probe file does not exist in this checkout

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
