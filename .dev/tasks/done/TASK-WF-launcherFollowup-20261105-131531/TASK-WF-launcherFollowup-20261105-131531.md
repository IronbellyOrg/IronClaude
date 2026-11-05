---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-launcherFollowup-20261105-131531
version: "1"
priority: Medium
created_date: "2026-11-05"
---

# ccsession exports the three model alias variables in tier mode (issue #384)

Source: ./source.md
Goal: In a ccsession tier workspace the launcher exports ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b and ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2, a test that failed before the edit pins it, outside tier mode nothing is set, and the docs say the launcher now sets the variables.

## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `ccsession-orca` stays untouched.
- Re-verify every line number in the source against the code on the working branch before editing: the source numbers are at base commit 38eb3c58 and the #315 change edits the same files.
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the two probe records show: the probe record is `.dev/issues/384/analysis/probe-alias-remap.md` (opus and haiku) and `.dev/issues/384/analysis/probe-sonnet-alias.md` (sonnet).

## Phase 1: The launcher exports the variables, test first

## Task 1: Add the failing-first tests and the harness keys to tests/unit/test_ccsession_tiers.py

In `tests/unit/test_ccsession_tiers.py`, add three lines to the `json.dump` call of the fake claude inside `_launch_env`, after the `"auth_token"` line, exactly as the source section "Harness addition" gives: `"opus_model"`, `"sonnet_model"` and `"haiku_model"`, read from `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL` with default `""`. Append the `ALIAS_VARIABLES` tuple and the two tests `test_tier_launch_exports_the_alias_variables` and `test_non_tier_launch_leaves_the_alias_variables_unset` from the source section "Failing-first test" at the end of the file. Re-verify that the helper names they use (`_launch`, `_launch_env`, `_defaults`, `_isolated`, `TIER_BLOCK`, `SKILL_DIR`) still exist with the same signatures, and adapt the call shapes only where #315 changed them.

Run `uv run pytest tests/unit/test_ccsession_tiers.py -k alias_variables -v` on the unchanged launcher and save the output to `./artifacts/t1-red.log`.

Acceptance criteria:
- `./artifacts/t1-red.log` shows `test_tier_launch_exports_the_alias_variables` failing with an AssertionError whose three values are empty strings, and `test_non_tier_launch_leaves_the_alias_variables_unset` passing.
- The three harness keys are present in `_launch_env` and no other test in `tests/unit/test_ccsession_tiers.py` changes behaviour.

## Task 2: Export the three variables in the tier-mode branch of the ccsession launcher

Depends on: Task 1

In `src/superclaude/skills/ccsession-tag/ccsession`, inside the `if [ "$TIER_MODE" = 1 ]; then` branch (anchor: the block that sets `TIER_MODE=0`, runs `python3 "$CCSESSION_MODELS" tier-mode` and then, in tier mode, rejects `--profile` and sets `USE_SHIM=1`), add these three lines right after `USE_SHIM=1`, with the same indentation as that line:

```bash
  export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a
  export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b
  export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2
```

Do not add them to any `elif` or `else` branch. Confirm by reading the launcher that nothing after the block unsets or overwrites the three variables (a grep for `ANTHROPIC_DEFAULT_` in the `ccsession-tag` folder found none before the edit).

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k alias_variables -v` passes both tests; save the output to `./artifacts/t2-green.log`.
- `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/skills/test_model_alias_policy.py` passes in full.
- `git diff` of `src/superclaude/skills/ccsession-tag/` shows exactly the three added lines in `ccsession` and no other file.

## Phase 2: The docs say the launcher sets the variables

## Task 3: Update docs/reference/model-aliases.md

Depends on: Task 2

In `docs/reference/model-aliases.md`: change the sentence "Owner decision of 2026-11-05: once the launcher sets the three variables, ..." so it says that in a ccsession tier workspace the launcher sets the three variables and the aliases resolve as the table shows. Change the "Target, once the launcher change lands: ..." paragraph to a present-tense statement that outside a ccsession tier workspace the launcher sets none of the three variables. Replace the "Status on 2026-11-05 ..." paragraph (the one saying the launcher is to apply the exports after the #315 pull request merges, then describing `/etc/aidev02/aienv.d/defaults.sh`) with a status paragraph that says the launcher now exports them in tier mode only, naming `src/superclaude/skills/ccsession-tag/ccsession` and the tests `test_tier_launch_exports_the_alias_variables` and `test_non_tier_launch_leaves_the_alias_variables_unset`. Keep the facts about the defaults file only as the values that the launcher export overrides in a tier workspace, and outside one the defaults file still applies; re-read `/etc/aidev02/aienv.d/defaults.sh` lines 92-94 before restating them. In the section "Why aliases and not picker ids", correct the bullet that says the probe did not set `ANTHROPIC_DEFAULT_SONNET_MODEL` and the bullet that says the same-family case was not covered, from `.dev/issues/384/analysis/probe-sonnet-alias.md`: the sonnet variable remaps `--model sonnet` and `model: sonnet`, and a subagent whose alias is in the main session's own model family stayed on the main model in that probe. Link the new probe record next to the existing probe link.

Acceptance criteria:
- `grep -n "is to apply\|once the launcher\|did not set" docs/reference/model-aliases.md` returns no line that still describes the launcher change as pending or the sonnet variable as unprobed.
- The page links `.dev/issues/384/analysis/probe-sonnet-alias.md` with a relative path that exists.

## Task 4: Update the pages and comments that say "once the launcher sets"

Depends on: Task 3

Change the future-tense wording to present tense (the launcher sets the variables in a ccsession tier workspace) in these places, and nowhere else: `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` (item 4 of the list about the `haiku` alias: drop "once the launcher sets that variable" and "until then it follows the value in the workspace defaults file"; outside a tier workspace it follows the inherited `ANTHROPIC_DEFAULT_HAIKU_MODEL`), `src/superclaude/skills/sc-issue-protocol/refs/chains.md` (the brainstorm model list bullet), `docs/user-guide/brainstorm.md` (the `--models` row), `docs/user-guide/commands.md` (the `--agents` spec line near line 849), the comment above `_DEFAULT_MODEL` in `src/superclaude/cli/reflect/commands.py` (comment text only, no code change) and the module docstring of `tests/skills/test_model_alias_policy.py` (docstring only, no assertion change). Run `grep -rn "launcher sets\|once the launcher" src docs tests` afterwards and fix any other hit that describes the launcher change as pending, except in `.dev/`.

Acceptance criteria:
- The grep above returns no line that describes the launcher export as future work.
- `uv run pytest tests/skills/test_model_alias_policy.py` still passes and `git diff` of `src/superclaude/cli/reflect/commands.py` shows comment lines only.

## Task 5: Add the CHANGELOG.md Unreleased entry

Depends on: Task 4

In `CHANGELOG.md` under `## [Unreleased]`, add a section for this change (issue #384, launcher follow-up) with a `#### Changed` bullet that says the ccsession launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` in tier mode only, and a `#### Added` bullet for the two tests and the sonnet probe record. Edit the sentence in the earlier #384 entry that says the launcher does not set these variables yet so it points to the new entry instead of claiming the opposite.

Acceptance criteria:
- `CHANGELOG.md` has the new entry under `[Unreleased]` and no sentence that still says the launcher does not set the variables.
- `make lint`, `uv run ruff format --check src/ tests/` and `make verify-sync` pass.
