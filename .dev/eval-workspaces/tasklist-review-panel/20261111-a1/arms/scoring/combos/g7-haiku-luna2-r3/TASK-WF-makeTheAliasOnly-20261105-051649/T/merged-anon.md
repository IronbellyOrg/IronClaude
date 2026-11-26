review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R2: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R2, R3 |
| L2 | open | yes | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | yes | single | MAJOR | - | R1 |
| L6 | open | yes | single | CRITICAL | - | R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: Unconditional tier-mode exports give tier1a or tier1b to owners whose usable-tier list omits them, because the launcher gates each export on that list (ccsession lines 896-898).
- anchor: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"
- anchor2: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

#### L1.R2 (F3)

- claim: The exact export lines drop the [1m] suffix that the launcher and review-tiers.default.json use, and the spec never says whether the suffix stays.
- anchor: "export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2"

#### L1.R2 (F4)

- claim: In this checkout lines 776-785 are the --profile/--tier argument parser, the tier-mode test is at line 883, lines 1099-1103 are inside a Python heredoc, and the fake claude's keys are at 399-410 rather than 330-341.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L1.R3 (F2)

- claim: The cited launcher lines contain `--profile` parsing rather than tier-mode detection, so the follow-up would cite the wrong code location.
- anchor: "the tier-mode block at lines 776-785"

#### L1.R3 (F3)

- claim: The test would not detect a non-tier launch that clears inherited non-empty alias variables.
- anchor: "the test removes those three variables from the launch environment first"

### L2

#### L2.R2 (F2)

- claim: The allow-list omits src/superclaude/cli/review/data/review-tiers.default.json and review-panel.live7.json, which contain claude-gw-tier ids, so the tier-text test fails on this checkout and the remaining-tests-pass criterion cannot hold.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/"

#### L2.R2 (F6)

- claim: The list is not paired with the files; issue-worker-t1.md pins claude-gw-tier1a and t3 pins claude-gw-tier3, so an order-based pairing fails on the unchanged tree.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L2.R2 (F7)

- claim: The optional backtick sits inside the code span, so an implementer cannot tell whether it belongs in the pattern, and a pattern without it misses backtick-quoted ids.
- anchor: "matched by `--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-\\d`"

### L5

#### L5.R1 (F1)

- claim: The required retry-names test cannot fail on the unchanged tree because the source and plugin retry references and the associated test expectations already use the requested names.
- anchor: "the retry names test of tests/skills/test_model_alias_policy.py"

### L6

#### L6.R3 (F1)

- claim: The required red run cannot fail the reflect-default test because the existing default is already `opus`.
- anchor: "`uv run pytest tests/skills/test_model_alias_policy.py` run on the unchanged tree fails exactly these seven tests"

## Other findings

- L3 (MAJOR, open, single): defaults.sh exports T3Model01=glm-5.3 (line 57), with gpt-6.1-terra on T2bModel01 (line 48), so the notes example puts a non-GPT model on rung 0 while describing it as GPT.
- L4 (MINOR, open, single): Commit 70ef6486 is not in this clone (git cat-file fails and git log -S returns only 8c93e1d), so the cited provenance cannot be checked here.

## Reviser brief

Blocking finding ids: L1, L2, L5, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
