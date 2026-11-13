review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3, R4 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | overlap | MAJOR | - | R1, R2, R3 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: Unconditional tier-mode exports give owners aliases for tiers they may not use, replacing inherited working model ids; the usable-tier rule in models.py is never applied.
- anchor: "they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"
- anchor2: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2"

#### L1.R2 (F2)

- claim: cli/review/data tier JSON files legitimately contain claude-gw-tier outside the stated allow-list and no task fixes or allow-lists them, so the full-policy pass required by Task 8 cannot be reached.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L1.R2 (F6)

- claim: Task 9 requires re-verifying only the anchor after the #315 merge while freezing unsuffixed export and expected test values, although the merged tier behaviour uses suffixed tier values with compact windows keyed to them.
- anchor: "marked \"re-verify after #315 merges\" (the tier-mode block at lines 776-785"

#### L1.R3 (F1)

- claim: The red gate expects seven failures on the unchanged tree, but the checkout already has the policy file and all 13 tests pass.
- anchor: "run on the unchanged tree fails exactly these seven tests"
- anchor2: "Create tests/skills/test_model_alias_policy.py (ROOT = Path(__file__).resolve().parents[2]"

#### L1.R3 (F2)

- claim: Several tasks edit lines and text that are already changed at HEAD, so their line anchors and current-state claims are stale.
- anchor: "change the expected command at line 235 from `--model claude-opus-4-8` to `--model opus`"

#### L1.R3 (F3)

- claim: The copied test resolves the launcher two levels above the artifacts folder, so it fails with a launch error instead of the required AssertionError.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"
- anchor2: "shows the scratch test failing with an AssertionError on the three variable values"

#### L1.R3 (F4)

- claim: Read literally, the scan fails on the cli review data JSON files, which no task edits; the committed test avoids this only through an unstated suffix filter.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths"
- anchor2: "passes in full (all tests green after Tasks 2 to 7)"

#### L1.R3 (F5)

- claim: The Goal allows only opus, sonnet and haiku, but Task 1 admits inherit, so the enforcement test and the Goal disagree.
- anchor: "select models only through the plain aliases opus, sonnet and haiku"
- anchor2: "Define ALIASES = opus, sonnet, haiku, inherit and two allow-list constants"

#### L1.R3 (F7)

- claim: The launcher already exports the three variables with a [1m] suffix at lines 896-898, so the spec's anchors, exact export lines and premise do not match this checkout.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"
- anchor2: "the tier-mode block at lines 776-785"

#### L1.R3 (F8)

- claim: The allow-list has no rule for what counts as legitimate, so any hit can be exempted and the bypass fix is not enforced.
- anchor: "A residual allow-list dict (path to reason) exists for any legitimate hit found when the test first runs"

#### L1.R4 (F1)

- claim: On this tree those seven checks already pass, so the unchanged-tree fail-first run cannot fail them.
- anchor: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test, the cleanup-audit test, the retry names test and the mapping document test"

#### L1.R4 (F2)

- claim: The tier-text test fails on src/superclaude/cli/review/data/, and no task extends the allow-list or removes that text, so the required green runs cannot pass.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "the Python constants test, the reflect default test, the D12 test and the claude-gw-tier text test pass"

#### L1.R4 (F3)

- claim: Those lines are the profile parser; the launcher already exports the three ids with a [1m] suffix at lines 896-898, so the follow-up spec points at the wrong place and the wrong values.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "the three export lines exactly (export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2)"

#### L1.R1 (F1)

- claim: TIER_TEXT_ALLOWED omits src/superclaude/cli/review/data/, whose JSON files hold claude-gw-tier text; if they exist at the base the tier-text test fails and the 'remaining tests pass' criterion cannot pass.
- anchor: "everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here"
- anchor2: "the remaining tests pass"

#### L1.R1 (F2)

- claim: Values are listed t3, t2, t1 while the files are named t1, t2, t3 elsewhere; pairing by position would give issue-worker-t1 tier3, but the real pin is tier1a.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

## Other findings

- L2 (MAJOR, open, overlap): The src-only constraint contradicts the tasks that direct edits under docs/, tests/, plugins/ and .dev/, forcing the implementer to guess which instruction wins.
- L3 (MAJOR, open, overlap): The frozen defaults values and rung-family conclusion in the Task 5 notes no longer match the defaults file (T3Model01 is glm-5.3), so the recorded evidence for the adviser consequence is stale.
- L4 (MINOR, open, single): The source asks to fix chains.md and templates, but Task 3 names no search of sc-issue-protocol/templates/ for the same flag.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
