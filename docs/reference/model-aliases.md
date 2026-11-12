# Model aliases and ccsession tiers

This page records the issue #384 owner decision of 2026-11-05 on how the Claude Code aliases `opus`, `sonnet` and `haiku` map to ccsession tiers, and the allow-list of `tests/skills/test_model_alias_policy.py`.

## What a primitive may name

Checks in `tests/skills/test_model_alias_policy.py` that read model names include:

- `test_frontmatter_model_is_an_alias_when_present` reads the `model:` value of `src/superclaude/agents/*.md`, `src/superclaude/skills/*/SKILL.md` and `src/superclaude/commands/*.md` and fails unless it is `opus`, `sonnet`, `haiku` or `inherit`, apart from the pins below; a file without a `model:` line is skipped (test lines 79-97, with the skip at lines 89-90).
- `test_python_selection_constants_are_not_full_model_ids` reads the Python files under `src/superclaude`, skips `src/superclaude/skills/ccsession-tag/`, and fails on a non-docstring string constant that starts with `claude-opus-`, `claude-sonnet-`, `claude-haiku-` or `claude-fable-` followed by a digit (test lines 48 and 135-157, with the skip at line 140; `RESIDUAL_FULL_IDS` is empty, line 44).
- `test_markdown_does_not_pass_full_model_ids_to_model_flags` fails when a Markdown line under `src/superclaude/agents`, `src/superclaude/commands` or `src/superclaude/skills` (`ccsession-tag` is skipped) has `--model` or `--models` followed by a full `claude-opus-`, `claude-sonnet-`, `claude-haiku-` or `claude-fable-` id (test lines 49-51, 70-76 and 160-169).
- `test_tier_ids_appear_only_in_allowed_paths` reads files ending `.md`, `.py`, `.json`, `.yaml`, `.yml`, `.sh`, `.txt` or `.toml` under the `agents`, `commands`, `skills`, `cli`, `hooks` and `core` folders of `src/superclaude` and fails on the text `claude-gw-tier` outside the allow-list paths below (test lines 46-47 and 100-115).

### Allow-list

- `issue-worker-t3` pins `claude-gw-tier2b`, `issue-worker-t2` pins `claude-gw-tier2` and `issue-worker-t1` pins `claude-gw-tier1b`, each on line 6 of its file under `src/superclaude/agents/`. The worker name `issue-worker-t3` is a label: since the owner decision of 2026-11-12 (issue 488) it runs on ccsession Tier 2b (GPT-6.1 Terra first), the order it had before Tier 3 was cut to GLM-5.3 and Qwen3.8 Max. `issue-worker-t3` also carries `effort: low` because the tier's first model returns an HTTP 400 for the default `medium` effort (issue 516); it is not known that Tier 2b's first model accepts `medium`, so the line stays.
- The pins are on purpose: when a spawn fails because the picker id is not served, for example outside a ccsession tier workspace, the issue protocol stops with `E-TIER-UNAVAILABLE`, and there is no alias fallback (`src/superclaude/skills/sc-issue-protocol/refs/tiers.md` lines 34 and 40).
- `TIER_TEXT_ALLOWED` lets the three pinned files, `src/superclaude/skills/sc-issue-protocol/` and `src/superclaude/skills/ccsession-tag/` contain the text `claude-gw-tier` (test lines 36-40).

## The mapping

Owner decision of 2026-11-05: inside a ccsession tier workspace the launcher sets each variable only when the workspace owner may use its tier, so for an owner who may use all three tiers the aliases resolve as follows:

| Alias | Tier model it resolves to | Set by |
|---|---|---|
| `opus` | `claude-gw-tier1a` | `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a` |
| `sonnet` | `claude-gw-tier1b` | `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` |
| `haiku` | `claude-gw-tier2` | `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` |

When the owner may use the tier, the launcher exports:

```text
ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a
ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b
ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2
```

Outside a ccsession tier workspace the launcher sets none of the three variables, so `opus`, `sonnet` and `haiku` keep Claude Code's meaning.

Status on 2026-11-05: the ccsession launcher (`src/superclaude/skills/ccsession-tag/ccsession`) exports each of these variables in tier mode only, in the branch that sets `USE_SHIM=1`, and only when the tier is on the workspace owner's list of usable tiers. That list is the output of the `tiers` command of `src/superclaude/skills/ccsession-tag/models.py` (lines 923-935). The command applies `tier_access`, the rule the shim uses (`CCSESSION_ACCESS`, `CCSESSION_TIER_RULES` and the tier list), so the launcher reads the rule without running the shim and adds no second rule. A variable whose tier is not on the list is left exactly as inherited, and when the list cannot be read no variable is exported.
So an owner limited to tier2 and tier3 gets only `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` and keeps the inherited opus and sonnet values, for example the real model ids from the workspace defaults file; a workspace whose model list has no tier1a and tier1b behaves the same. The list is read when the launcher starts, before that launch's model-data refresh, so a list changed by the refresh applies from the next launch. The five tests `test_tier_launch_exports_the_alias_variables`, `test_limited_owner_gets_only_the_haiku_alias_variable`, `test_limited_owner_keeps_inherited_alias_values`, `test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers` and `test_non_tier_launch_leaves_the_alias_variables_unset` in `tests/unit/test_ccsession_tiers.py` pin these cases.
`/etc/aidev02/aienv.d/defaults.sh` still exports real model ids for the same three variables; inside a tier workspace the launcher export replaces the ones for tiers the owner may use and the others stay, and outside one the inherited values stay. Line 92 sets `ANTHROPIC_DEFAULT_HAIKU_MODEL` from `T2Model02` (`glm-5.3`, line 37), line 93 sets `ANTHROPIC_DEFAULT_OPUS_MODEL` from `T1aModel01` (`claude-opus-5-5`, line 23) and line 94 sets `ANTHROPIC_DEFAULT_SONNET_MODEL` from `T1aModel02` (`claude-sonnet-5-5`, line 25).

## Why aliases and not picker ids

Source: <https://code.claude.com/docs/en/sub-agents>, read 2026-11-05.

- The sub-agents page says the Agent-call `model` parameter takes the aliases `sonnet`, `opus`, `haiku` or `fable`, and that Claude cannot pass a full model id or `inherit` on that call.
- The page says the frontmatter `model` takes an alias, a full model id or `inherit`; it documents no environment lookup in that field, so `model: ${SOMETHING}` is not a documented option.
- The probes found that a tier id set in `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` or `ANTHROPIC_DEFAULT_HAIKU_MODEL` was served, that `model: opus`, `model: sonnet` and `model: haiku` resolved through it, and that `--model sonnet` ran on the tier id as well.
- The page also describes an edge case for family aliases: when the main session runs a model of the same family, the alias can resolve to that model. In the sonnet probe a `model: sonnet` subagent under a Sonnet main session ran on the main session's model, not on `claude-gw-tier1b`; that is one observation, and the rule behind it is not verified (the Claude Code source was not read). The same case was not probed for an Opus or a Haiku main session.

On 2026-11-05 a probe against the workspace gateway ([probe record](../../.dev/issues/384/analysis/probe-alias-remap.md)) found that a subagent with `model: opus` ran on `claude-gw-tier1a` and one with `model: haiku` ran on `claude-gw-tier2`, while the main session kept its own model.
A second probe ([sonnet probe record](../../.dev/issues/384/analysis/probe-sonnet-alias.md)) found the same for `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b`: `--model sonnet` and a `model: sonnet` subagent under an Opus main session ran on `claude-gw-tier1b`.
Claude Code logs an `unrecognized_model` notice for the tier ids and serves the request.
The probes covered the frontmatter path and `--model`; they did not exercise the Agent-call parameter.

## Known consequences

- **Reflect reviewer diversity.** When the three variables hold the tier ids, `count_model_aliases` (`src/superclaude/cli/reflect/runner.py` lines 291-310) counts three distinct values. Tier 1a and tier 1b both list Claude Sonnet 5.5 (`src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` lines 38-39), so the reviewers differ less than the count suggests.
- **Sprint alternate-model suggestion.** Given the alias `opus`, `suggest_alternate_model` returns `sonnet` when the two slots hold different ids (`src/superclaude/cli/sprint/aienv.py` lines 149-152). When the three `ANTHROPIC_DEFAULT_*_MODEL` slots hold tier ids and no slot that `_load_aliases` reads, including `T2Model01` to `T2Model0N` (lines 78-82), holds a given Claude id from a cooldown message such as `claude-opus-5-5`, it returns `None` (lines 111-128).
- **Roadmap names.** Step ids such as `generate-opus-architect` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md` line 114) and the `/sc:recommend` eval model lists (`src/superclaude/cli/recommend/eval_aggregate.py` lines 18-20) name the aliases, so this change does not rename them.
- **Implement retry ladder.** On 2026-11-05 `/etc/aidev02/aienv.d/defaults.sh` exported the four rung variables of that time: the first Tier 3 slot, `T2Model02`, `T1Model02` and `T1Model01` (lines 48, 37, 69 and 67). Since the owner decision of 2026-11-12 (issue 488) rung 0 is `T2bModel01`, the first Tier 2b slot (GPT-6.1 Terra, a GPT-family model, so the family behavior of rung 0 is unchanged); the other three variables are unchanged, and the line of `T2bModel01` in `defaults.sh` is not checked here. The first Tier 3 slot now holds glm-5.3, which is in neither model family, so it is no longer a rung. After Task 5 of this issue's plan, in a workspace that sets the four rung variables the primary ladder of `refs/retry.md` in `sc-implement-protocol` (names at lines 162, 164, 168, 169 and 172) replaces the alias fallback ladder. The Task 5 notes (`artifacts/t5-notes.md` in this issue's plan package) record that with these values rung 1 is a non-Claude model, rungs 0 and 2 are GPT models, and a claude-sonnet executor sits on no primary rung, so its tier is unknown and adviser A takes the top rung.
