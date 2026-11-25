# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Tier 4 currently holds GPT-6 Luna, Claude Haiku 5.5 and Grok 4.7 via slots `T4Model01`-`T4Model03`. `git show origin/master:src/superclaude/skills/ccsession-tag/ccsession-models.json` (tiers.tier4); MODEL-TIERS.md line 46.
- Tier slots name env slot variables, not models, so adding a model means adding/repointing a slot whose value comes from the Coder workspace env. ccsession-models.json `models_env`; README.md "Tiers (Coder workspaces)" section (~line 440, `/etc/aidev02/aienv.d/defaults.sh`).
- muse-wonder-1.0 registration pattern: profile `wonder`, context 1000000, display override "Muse Wonder 1.0", listed in `picker.show` and `picker.one_million_context`. ccsession-models.json.
- Tests pinning tier membership: tests/unit/test_ccsession_tiers.py lines 86-91 (T4 slot fixtures) and 222 (tier4 slot assertion); tests/skills/test_model_alias_policy.py and tests/review/test_review_panel*.py pin model lists. `git grep -n -E 'muse-wonder|T4Model' origin/master -- tests/ docs/reference/model-aliases.md`.
- No file on origin/master names muse-ember. `git grep -n -i muse-ember origin/master` → no matches.
- CHANGELOG `[Unreleased]` already documents the #488/#518 tier layout, including the Coder merge-order dependency and the "slot is not set" launch stop, so this change likely carries the same constraint. `git show origin/master:CHANGELOG.md` (first ~40 lines).
- docs/reference/model-aliases.md contains no muse or tier4 model references. grep in the command above.
- To check, not verified: slot values and T4_WINDOW live in the Coder workspace env (IronbellyOrg/Coder, outside this repo), and ccsession-models.json is downloaded from master at launch, so a new slot name must exist in Coder defaults first. README.md tiers section; CHANGELOG #488 entry.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
