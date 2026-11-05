# Launcher follow-up 2: access-aware alias exports (issue #384)

This file changes the first launcher follow-up (`.dev/issues/384/launcher-followup.md`), which is already implemented in the working tree: three unconditional exports in the tier-mode branch of `src/superclaude/skills/ccsession-tag/ccsession`, two tests, and the docs. The owner answered the open design question on 2026-11-05 (message "Owner answer: access-aware tier exports", relayed by the coordinator). Everything in the first spec that this file does not change stays.

Owner text, verbatim:

> Owner answer on the launcher PR (issue 384): make the export access-aware.
>
> In tier mode, ccsession sets each of ANTHROPIC_DEFAULT_OPUS_MODEL (claude-gw-tier1a), ANTHROPIC_DEFAULT_SONNET_MODEL (claude-gw-tier1b) and ANTHROPIC_DEFAULT_HAIKU_MODEL (claude-gw-tier2) ONLY when the workspace owner may use that tier (use the same rule the shim and ccsession already apply: CCSESSION_TIER_RULES and the tier list; do not invent a second rule). When the owner may not use a tier, do not export that variable, so the inherited value (the defaults file's real model id) still applies and the helper agents keep working. Outside tier mode nothing is exported, as before.
>
> Add tests: an unrestricted owner gets all three; an owner limited to tier2/tier3 gets only the haiku one (and the opus and sonnet variables are left exactly as inherited, including when they are unset or already set); a tier-mode workspace without tier1a/tier1b behaves the same; non-tier mode exports none. Update docs/reference/model-aliases.md and the PR body to say the mapping is applied per allowed tier and what a limited owner gets instead. If the rule for "may use" cannot be read from the launcher without running the shim, say so in the PR body and use the narrowest honest check you can test; if you cannot find a testable check, send an orchestration question instead of shipping the unconditional version. The rest of your spec is unchanged.

## What the code offers (read on the working branch, 2026-11-05)

The "may use" rule can be read from the launcher without running the shim. `python3 "$CCSESSION_MODELS" tiers` (`src/superclaude/skills/ccsession-tag/models.py` lines 923-935) prints one line per usable tier, name first (fields separated by the unit separator character), from `tier_access`, the function the shim uses (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` lines 182-187). `ccsession` already reads the same command for its `--help` listing (line 1651). On an invalid access entry or a missing tier model the command prints nothing on standard output and exits 3. The tier list comes from the newest of the bundled `ccsession-models.json` and a cached `models.json` under `$XDG_CACHE_HOME/ccsession` (`models.py` lines 228-239); the test fixture `_isolated` gives every test a private `XDG_CACHE_HOME` (`tests/unit/test_ccsession_tiers.py` line 105).

## Requirements

R-001: In tier mode, `ccsession` exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a` only when tier1a is on the workspace owner's list of usable tiers, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` only when tier1b is, and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` only when tier2 is. The edit replaces the three unconditional lines after `USE_SHIM=1` in the tier-mode branch and nothing else in `ccsession-tag/` changes.

R-002: The list of usable tiers is the first field of each line printed by `python3 "$CCSESSION_MODELS" tiers`. The launcher adds no second access rule and `models.py` and the shim are not changed.

R-003: A variable whose tier is not on the list is left exactly as inherited: unset stays unset and an inherited value stays unchanged.

R-004: When the `tiers` command fails or prints nothing, none of the three variables is exported.

R-005: Outside tier mode nothing is exported (unchanged from the first spec).

R-006: Tests in `tests/unit/test_ccsession_tiers.py`: (a) an unrestricted owner gets all three variables; (b) an owner limited to tier2 and tier3 (the existing `ACCESS_BLOCK` entry for `bob`) gets only the haiku variable, and the opus and sonnet variables are exactly as inherited, once when unset and once when set to a sentinel value; (c) a tier-mode workspace whose model list has no tier1a and no tier1b (a cached `models.json` with those two tiers removed) behaves like (b); (d) non-tier mode exports none (the existing test). The restricted-owner tests fail on the current unconditional launcher before the edit.

R-007: `docs/reference/model-aliases.md` says the mapping is applied per allowed tier, says what a limited owner gets instead (the inherited value, for example the defaults file's real model id), and the bullet "Owners limited to some tiers" under "Known consequences" is replaced by that statement. The pages that now say the launcher sets the variables say it sets each one for a tier the owner may use: `docs/user-guide/brainstorm.md`, `docs/user-guide/commands.md`, `src/superclaude/skills/sc-issue-protocol/refs/tiers.md`, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`, the comment in `src/superclaude/cli/reflect/commands.py` and the docstring of `tests/skills/test_model_alias_policy.py`. The `CHANGELOG.md` entry says the same and drops its "Known limit" bullet.

R-008: The pull request body states the per-tier rule, what a limited owner gets, and that "may use" is read through the `tiers` command without running the shim. This requirement changes no file.

## Out of scope

Changes to `models.py` or the shim; a probe of the Agent-call `model` parameter; a launcher-level test of R-004 (a broken access entry stops the launcher later, so the empty-list branch has no observable effect there).
