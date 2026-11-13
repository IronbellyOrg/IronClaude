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
| L1 | open | yes | overlap | CRITICAL | - | R1, R3 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The scan covers cli/, where review-tiers.default.json and review-panel.live7.json contain claude-gw-tier and are not allow-listed, so the tier-text test can never pass and the Task 1, Task 2 and Task 8 criteria fail.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L1.R3 (F1)

- claim: The specified tier-text allow-list omits existing tier-id text in src/superclaude/cli/review/data/review-tiers.default.json, so the policy test cannot satisfy the requirement that only seven tests fail.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)."

### L2

#### L2.R1 (F2)

- claim: The copied harness derives REPO_ROOT from __file__ and imports models at import time, so in the scratch folder it fails with an import error unless the path is rebased, which the spec does not say.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"

#### L2.R1 (F3)

- claim: The spec exports all three variables in tier mode without checking the owner's tier access, so a limited owner gets aliases mapped to tiers they cannot use.
- anchor: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L2.R1 (F4)

- claim: The exports omit the [1m] suffix that the launcher's picker ids carry; the probe shows the unsuffixed id is served, and any context-window effect is unverified.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b"

#### L2.R3 (F2)

- claim: The launcher spec does not say to preserve the existing per-tier owner-access check, so its literal exports could make aliases resolve to tiers the owner is not permitted to use.
- anchor: "the three export lines exactly (export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2)"

#### L2.R2 (F1)

- claim: A non-tier launch with inherited model variables must both preserve those variables and have nothing set, so the stated mapping behavior contradicts itself.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "so a launch that is not in tier mode leaves the inherited environment untouched"

## Other findings

- L3 (MAJOR, open, overlap): Line 243 holds the source line citations for commands.py, which go stale once the comment above _DEFAULT_MODEL grows, and the task does not say to update them.
- L4 (MINOR, open, single): These workspace slot values held on 2026-11-05 but the defaults file now has T3Model01=glm-5.3, so the notes need a date.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
