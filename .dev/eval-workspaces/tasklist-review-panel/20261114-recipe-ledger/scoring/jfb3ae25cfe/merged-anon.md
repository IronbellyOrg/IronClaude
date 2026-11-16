review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R3, R1, R2 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 1 test wants exact equals strings; Task 6 wording uses via without equals, so a literal implementer may fail Task 6 acceptance.
- anchor: "states the three exports with the exact ids ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"
- anchor2: "opus to claude-gw-tier1a via ANTHROPIC_DEFAULT_OPUS_MODEL, sonnet to claude-gw-tier1b via ANTHROPIC_DEFAULT_SONNET_MODEL"

#### L1.t3-1 (F1)

- claim: Task 6 requires documentation to say no variables are set outside tier workspaces, contradicting the stated workspace exports and inherited environment; that can make the documented model behavior false.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"

#### L1.t3-1 (F2)

- claim: Starting with the variables removed cannot verify the stated requirement that a non-tier launch leaves inherited values untouched.
- anchor: "test removes those three variables from the launch environment first"

#### L1.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a launcher whose non-tier launch preserves inherited tier-valued model variables, and that is wrong because the reference page also promises that no variables are set outside tier mode and aliases keep Claude Code's meaning.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t4-1 (F3)

- claim: The test removes the three variables before launch, so it does not check the stated requirement that a non-tier launch preserve inherited values.
- anchor: "The test asserts the three values in a default tier launch and that a non-tier launch leaves them unset."

## Other findings

- L2 (MAJOR, open, single): The only claim covers frontmatter pins, but templates and chain rows also pin picker ids on the session model line.
- L3 (MAJOR, open, single): Task 4 asks for a repository-wide cleanup, but its acceptance grep checks only the cleanup-audit skill directory and command, so it can pass while stale Haiku claims remain elsewhere.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
