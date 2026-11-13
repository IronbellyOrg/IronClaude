review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R1: report <redacted>, block ok false
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | yes | overlap | CRITICAL | - | R2, R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The tier-text allow-list omits src/superclaude/cli/review/data/*.json which contains claude-gw-tier, so the tier-text test fails on the unchanged tree and still fails after Tasks 2 to 7, making acceptance unpassable.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "In tests/skills/test_model_alias_policy.py the Python constants test, the reflect default test, the D12 test and the claude-gw-tier text test pass"

#### L1.R1 (F2)

- claim: Pin values listed in descending tier order after files named t1, t2, t3 invite the reversed mapping t1=tier3, opposite of the actual pins.
- anchor: "ISSUE_WORKER_PINS (the three issue-worker agent files, whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L1.R2 (F1)

- claim: Stated allow-list omits the review data directory, so the exactly-seven fail count overstates the observed failures.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L1.R2 (F4)

- claim: Line-number anchor is stale because the default is already the plain alias in the inspected tree.
- anchor: "`_DEFAULT_MODEL = \"claude-opus-4-8\"` (line 31)"

### L7

#### L7.R2 (F2)

- claim: Launcher spec uses the unbracketed tier id while the inspected launcher uses the bracketed form with context suffix.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

#### L7.R2 (F3)

- claim: Launcher spec states only the tier-mode guard and omits the per-tier owner-access rule.
- anchor: "they run only when tier mode is on"

#### L7.R3 (F1)

- claim: The required follow-up spec cannot accurately quote the stated base-commit anchor because those lines contain argument parsing rather than the tier-mode block.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L7.R3 (F2)

- claim: Clearing the variables before the non-tier launch test does not catch a launcher that incorrectly deletes inherited values instead of leaving them untouched.
- anchor: "the test removes those three variables from the launch environment first"

## Other findings

- L2 (MAJOR, open, single): Stated line anchors for RUNGS and _rt do not match this tree (RUNGS at line 798, _rt at line 810), so following the numbers literally edits the wrong lines.
- L3 (MAJOR, open, single): Note says four exported variables while the task body lists five exported variables including T2Model01, without stating T2Model01 is the optional one.
- L4 (MINOR, open, single): Absolute src-only wording contradicts tasks requiring edits in tests/, docs/ and .dev/issues/.
- L5 (MINOR, open, single): The wider Haiku sweep has no acceptance check, so a missed site passes acceptance.
- L6 (MINOR, open, single): Stated lines for the brainstorm text in docs/user-guide/commands.md do not match this tree (brainstorm section near line 892).

## Reviser brief

Blocking finding ids: L1, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
