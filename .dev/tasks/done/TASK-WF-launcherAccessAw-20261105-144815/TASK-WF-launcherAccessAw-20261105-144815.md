---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-launcherAccessAw-20261105-144815
version: "1"
priority: Medium
created_date: "2026-11-05"
---

# ccsession exports the tier alias variables only for tiers the owner may use (issue #384)

Source: ./source.md
Goal: In a ccsession tier workspace the launcher exports each of ANTHROPIC_DEFAULT_OPUS_MODEL, ANTHROPIC_DEFAULT_SONNET_MODEL and ANTHROPIC_DEFAULT_HAIKU_MODEL only when the owner may use its tier (tier1a, tier1b, tier2), leaves a variable for any other tier exactly as inherited, tests pin both cases, and the docs say so.

## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `models.py`, `local-gateway-alias-proxy.py` and `ccsession-orca` stay untouched (R-002).
- The three unconditional export lines from the first follow-up already sit right after `USE_SHIM=1` in the tier-mode branch of `src/superclaude/skills/ccsession-tag/ccsession` (about lines 867-870); re-read the file before editing and change only those lines (R-001).
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the probe records show; no probe exercised the Agent-call `model` parameter.
- R-008 (the pull request body) changes no file and has no task; it is written when the pull request is opened. R-004 has no launcher-level test because a broken access entry makes the launcher exit before Claude starts (`apply_tier_selection`, `|| exit 2`).

## Phase 1: The launcher exports per usable tier, test first

## Task 1: Add the restricted-owner tests to tests/unit/test_ccsession_tiers.py

Covers R-006 and, through its expectations, R-003 and R-005.

Append three tests after `test_non_tier_launch_leaves_the_alias_variables_unset` at the end of `tests/unit/test_ccsession_tiers.py`, using `ALIAS_VARIABLES`, `_launch`, `ACCESS_BLOCK` (the access setting that limits `bob` to tier2 and tier3) and the `_isolated` fixture, and removing the three variables first with `monkeypatch.delenv` as the existing tests do. The existing `test_tier_launch_exports_the_alias_variables` already covers an unrestricted owner and the existing non-tier test covers R-005; leave both unchanged.

- `test_limited_owner_gets_only_the_haiku_alias_variable`: launch with `defaults=ACCESS_BLOCK` and `CODER_WORKSPACE_OWNER_NAME="bob"`, all three variables unset; expect `seen["opus_model"] == ""`, `seen["sonnet_model"] == ""` and `seen["haiku_model"] == "claude-gw-tier2"`.
- `test_limited_owner_keeps_inherited_alias_values`: same launch with `monkeypatch.setenv` giving the opus and sonnet variables the sentinel values `inherited-opus` and `inherited-sonnet`; expect those two values unchanged and `seen["haiku_model"] == "claude-gw-tier2"`.
- `test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers`: before launching, write `$XDG_CACHE_HOME/ccsession/models.json` (the `_isolated` fixture sets a private `XDG_CACHE_HOME`) as a copy of `src/superclaude/skills/ccsession-tag/ccsession-models.json` with the `tier1a` and `tier1b` entries removed from `tiers` and `version` set to a string that sorts above the bundled one (`models.py` `load()` takes the newest copy); launch with the unrestricted `TIER_BLOCK` and the opus and sonnet variables set to sentinel values; expect the sentinels unchanged and `seen["haiku_model"] == "claude-gw-tier2"`.

Run `uv run pytest tests/unit/test_ccsession_tiers.py -k "alias_variable or limited_owner or without_tier1a" -v` on the launcher as it stands (unconditional exports) and save the output to `./artifacts/t1-red.log`.

Acceptance criteria:
- `./artifacts/t1-red.log` shows the three new tests failing with an AssertionError (the opus and sonnet values are `claude-gw-tier1a` and `claude-gw-tier1b` where the test expects empty or sentinel values) and the two existing alias tests passing.
- `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py` pass.

## Task 2: Make the launcher export each alias variable only for a usable tier

Depends on: Task 1

Covers R-001, R-002, R-003, R-004 and R-005.

In `src/superclaude/skills/ccsession-tag/ccsession`, inside the `if [ "$TIER_MODE" = 1 ]; then` branch, replace the three unconditional `export ANTHROPIC_DEFAULT_*_MODEL=...` lines that follow `USE_SHIM=1` with this block, indented like `USE_SHIM=1`:

```bash
  # Map an alias to its tier only for a tier this owner may use: the list the
  # shim, --tier and --help use (models.py tiers). A tier not on the list, or a
  # list that cannot be read, leaves the inherited variable alone.
  _usable_tiers=$'\n'"$(python3 "$CCSESSION_MODELS" tiers 2>/dev/null | cut -d$'\x1f' -f1)"$'\n'
  case "$_usable_tiers" in *$'\n'tier1a$'\n'*) export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a ;; esac
  case "$_usable_tiers" in *$'\n'tier1b$'\n'*) export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b ;; esac
  case "$_usable_tiers" in *$'\n'tier2$'\n'*) export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2 ;; esac
```

Keep the block inside the tier-mode branch, add nothing to the `elif` branches, and confirm `bash -n` passes on the file (it runs under `set -e`; the pipeline status is that of `cut`, so an empty list does not stop the launcher).

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k "alias_variable or limited_owner or without_tier1a" -v` passes all five tests; save the output to `./artifacts/t2-green.log`.
- `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/skills/test_model_alias_policy.py` passes in full; save the output to `./artifacts/t2-full.log`.
- `git diff` of `src/superclaude/skills/ccsession-tag/` against the state before this task shows changes in `ccsession` only, and in `ccsession` only the replacement of the three export lines by the block above.

## Phase 2: The docs describe the per-tier rule

## Task 3: Update docs/reference/model-aliases.md

Depends on: Task 2

Covers R-007 for the reference page.

In `docs/reference/model-aliases.md`: change the sentence under "The mapping" that says the launcher sets the three variables so that it says the launcher sets each variable only for a tier the workspace owner may use. Rewrite the "Status on 2026-11-05" paragraph so that it says: the launcher (`src/superclaude/skills/ccsession-tag/ccsession`) exports each variable in tier mode only, when the tier is on the owner's list of usable tiers; the list is the output of the `tiers` command of `src/superclaude/skills/ccsession-tag/models.py` (the same `tier_access` rule the shim applies, `CCSESSION_ACCESS` and the tier list), read without running the shim; a tier that is not on the list, or a list that cannot be read, leaves the inherited value; so an owner limited to tier2 and tier3 gets only `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` and keeps the inherited opus and sonnet values (for example the real model ids from `/etc/aidev02/aienv.d/defaults.sh`, whose lines 92-94 you re-read first); and name the tests of Task 1 and `test_tier_launch_exports_the_alias_variables`. Delete the "Owners limited to some tiers" bullet under "Known consequences", since the status paragraph now states what such an owner gets. Keep the table rows and the exports code block unchanged.

Acceptance criteria:
- `grep -n "Owners limited to some tiers" docs/reference/model-aliases.md` returns nothing, and the page contains the words "each variable" or "per tier" and the command name `tiers`.
- `uv run pytest tests/skills/test_model_alias_policy.py` passes.

## Task 4: Update the pages and comments that say the launcher sets all three variables

Depends on: Task 3

Covers R-007 for the pointer pages.

Where each of these now says that in a ccsession tier workspace the launcher sets the variables, say that it sets each variable for a tier the owner may use (the alias of a tier the owner may not use keeps its inherited value): `docs/user-guide/brainstorm.md` (the `--models` row), `docs/user-guide/commands.md` (the `--agents` spec line near line 860), `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` (item 4 about the `haiku` alias: the launcher sets it to `claude-gw-tier2` when the owner may use tier2), `src/superclaude/skills/sc-issue-protocol/refs/chains.md` (the brainstorm model list bullet), the comment above `_DEFAULT_MODEL` in `src/superclaude/cli/reflect/commands.py` (comment text only, and it must not contain the text `claude-gw-tier`), and the docstring of `tests/skills/test_model_alias_policy.py` (docstring only, no assertion change). Use `grep -rn "launcher sets" src docs tests` to find them and report any other line that still says the launcher sets all three unconditionally.

Acceptance criteria:
- The grep above lists no line that says the launcher sets all three variables without the owner-access condition.
- `uv run pytest tests/skills/test_model_alias_policy.py tests/skills/test_issue_protocol.py` passes and `git diff` of `src/superclaude/cli/reflect/commands.py` shows comment lines only.

## Task 5: Update the CHANGELOG.md entry and run the final checks

Depends on: Task 4

Covers R-007 for the changelog.

In the "ccsession: tier mode sets the model aliases (#384 launcher follow-up)" entry under `## [Unreleased]` in `CHANGELOG.md`: change the first `#### Changed` bullet so it says the launcher exports each variable only when the owner may use its tier, and an owner limited to other tiers keeps the inherited value for the others; delete the "Known limit" bullet; change the pointer-pages bullet if it says the pages describe all three unconditionally; and in the `#### Added` bullet name the new restricted-owner tests. Then run `make lint`, `uv run ruff format --check src/ tests/`, `make sync-dev` and `make verify-sync`, and save their output to `./artifacts/t5-checks.log`.

Acceptance criteria:
- `grep -n "Known limit" CHANGELOG.md` returns nothing and the entry names the per-tier rule.
- `./artifacts/t5-checks.log` shows `make lint`, the format check and `make verify-sync` passing.
