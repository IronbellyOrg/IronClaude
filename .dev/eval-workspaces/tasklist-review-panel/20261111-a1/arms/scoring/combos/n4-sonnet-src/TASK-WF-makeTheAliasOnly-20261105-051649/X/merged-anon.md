review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R2, R3 |
| L4 | open | no | overlap | MAJOR | - | R1, R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The tier-text test flags src/superclaude/cli/review/data tier files that are in no allow-list entry, so it fails on the unchanged tree and still fails after Task 2, breaking both acceptance criteria.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L1.R2 (F3)

- claim: Saying nothing is set outside a tier workspace is false on this workspace, where the defaults file already exports real model ids that a non-tier launch leaves in force.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "today the workspace defaults file exports real model ids for them"

#### L1.R2 (F5)

- claim: The test permits inherit as a fourth frontmatter value while the goal and constraints say only the plain aliases opus, sonnet and haiku may be used.
- anchor: "Define ALIASES = opus, sonnet, haiku, inherit and two allow-list constants"

#### L1.R3 (F1)

- claim: The cli scan fails on review-tiers.default.json and review-panel.live7.json, which no task edits, so the exactly-seven criterion and Task 2's pass criterion cannot pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the Python constants test, the reflect default test, the D12 test and the claude-gw-tier text test pass"

#### L1.R3 (F3)

- claim: Task 6 says nothing is set outside a tier workspace, but the workspace defaults file exports real ids today.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "New text that describes the mapping says it holds once the launcher sets the three variables"

#### L1.R3 (F6)

- claim: No base commit is named, and the outputs of Tasks 1 to 6 already exist at HEAD, so the red state is unreproducible and Create would overwrite an existing file.
- anchor: "run on the unchanged tree fails exactly these seven tests"
- anchor2: "Create tests/skills/test_model_alias_policy.py"

#### L1.R3 (F7)

- claim: ALIASES omits fable, which the Agent parameter accepts, so a future model: fable would fail the policy test.
- anchor: "Define ALIASES = opus, sonnet, haiku, inherit and two allow-list constants"

#### L1.R1 (F1)

- claim: If src/superclaude/cli/review/data/*.json (which hold claude-gw-tier ids) exist at the base, the tier-text test fails and no task can make Task 8's full policy run pass.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths"

#### L1.R1 (F2)

- claim: Values are listed in the reverse order of the files, so an in-order mapping gives t1 the value tier3 instead of tier1a.
- anchor: "the three issue-worker agent files, whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"
- anchor2: "src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md"

#### L1.R1 (F3)

- claim: The pattern sk- also matches ordinary hyphenated words such as task- or risk-, so a clean page can fail the check.
- anchor: "grep -nE \"sk-|token=\" docs/reference/model-aliases.md"

#### L1.R1 (F4)

- claim: A multi-column mapping table does not contain the contiguous NAME=value strings that the Task 1 test requires.
- anchor: "the three exports spelled exactly as in the mapping table"
- anchor2: "states the three exports with the exact ids ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

### L2

#### L2.R2 (F2)

- claim: Exporting all three variables whenever tier mode is on maps aliases to tiers a limited owner may not use, because tier mode only requires one T<N>_WINDOW while owner access is a separate rule in models.py.
- anchor: "the three export lines exactly (export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b"

#### L2.R3 (F5)

- claim: The cited launcher lines are wrong, and the existing [1m] exports at 896-898 conflict with the spec's bare-value exports.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "the custom-option exports at lines 1099-1103"

#### L2.R1 (F5)

- claim: The harness needs REPO_ROOT (parents[2]) and the autouse _isolated fixture, so a copy without them can fail with FileNotFoundError or leak the environment instead of the required AssertionError.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"

## Other findings

- L3 (MAJOR, open, overlap): Task 5 never states whether T2Model01 is a required ladder variable or an optional fifth, so the activation condition for the primary ladder is ambiguous.
- L4 (MAJOR, open, overlap): Removing the workaround lets the haiku brainstorm proposal run glm-5.3 on this workspace (defaults.sh line 107, T2Model02 at line 37).

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
