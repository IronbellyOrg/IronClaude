# /sc:analyze src/superclaude --focus architecture --depth deep (issue #384)

- Target: hard-coded model selection in `src/superclaude/` (agents, commands, skills, Python CLI), plus the `plugins/superclaude/` mirror, tests and docs.
- Checked against: `origin/master` 38eb3c58afe6988b51060ae14117172869ea4c1e, 2026-11-05.
- Tools: Grep, Glob and Read only. codegraph and auggie were not used (no codegraph project loaded for this session); every finding below comes from a direct grep or file read.
- Read-only context, not proposed for change here: `src/superclaude/skills/ccsession-tag/` (owned by issue #315).

## 1. Owner decisions this analysis applies

| Plain alias | Inside a ccsession tier workspace | Outside one |
|---|---|---|
| `opus` | `claude-gw-tier1a` | `opus` |
| `sonnet` | `claude-gw-tier1b` | `sonnet` |
| `haiku` | `claude-gw-tier2` | `haiku` |

Python package code is in scope.

## 2. Findings by severity

### Critical: the selection surfaces cannot all carry a picker ID

There are four different ways a model is chosen today, and only one of them can take a picker ID directly.

| Surface | Example | Can it carry `claude-gw-tier1a`? | Evidence |
|---|---|---|---|
| Agent file frontmatter `model:` | 13 agents, `sc-bare-review` skill | Yes (alias, full id or `inherit`) | `sc-issue-protocol/refs/tiers.md:25`; precedent `agents/issue-worker-t1.md:6` |
| Agent tool `model` parameter at spawn time | adversarial generate (`sc-adversarial-protocol/SKILL.md:1022`), recommend classifier and eval fan-out (`sc-recommend/SKILL.md:73,332-334`), validate-roadmap (`sc-validate-roadmap-protocol/SKILL.md:495`), auggie `--revagent`, implement advisers (`sc-implement-protocol/refs/retry.md:185`) | No: aliases `sonnet`, `opus`, `haiku`, `fable` only, and it overrides frontmatter | `sc-issue-protocol/refs/tiers.md:24` |
| `claude --model <x>` from Python | `sprint/summarizer.py:330-331`, `roadmap` generate steps via `pipeline/process.py:164`, `reflect/commands.py:359` | Yes, but only when the picker ID is served (ccsession shim running) | `ccsession-tag/models.py:855` prints `PROFILE_MODEL=claude-gw-<tier>[1m]` and `PROFILE_REQUIRES_SHIM=1` |
| Env-derived alias sets | reflect diversity count (`reflect/runner.py:287-310`), sprint rotation (`sprint/aienv.py:43-47`), brainstorm validation (`sc-brainstorm-protocol/SKILL.md:109`) | Not a selection: these read `ANTHROPIC_DEFAULT_*_MODEL` | as cited |

Consequence: for every skill that picks the model at spawn time, the mapping cannot be done by editing the alias string. The plan must pick one mechanism, for example:

1. Tier agent files: one thin agent per tier (frontmatter `model: claude-gw-tier1a` and so on, the issue-worker pattern), and skills spawn by `subagent_type` instead of `model`. Multiplies agents per persona unless the persona moves into the prompt.
2. Session-level remap: inside a ccsession tier session, set `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `..._SONNET_MODEL=claude-gw-tier1b`, `..._HAIKU_MODEL=claude-gw-tier2`, so every plain alias, at every surface, already resolves to the tier, and outside the session the plain alias is unchanged (the owner's fallback for free). This lives in ccsession launch code, which is read-only here (issue #315), so it needs coordination with that worker. Whether Claude Code accepts a picker ID as the value of those variables is not verified yet. No ccsession file sets these variables today (grep of `skills/ccsession-tag/` finds none).
3. Install-time rendering: `superclaude install` writes picker IDs into installed agent frontmatter when it detects tier mode. Static: a later session outside tier mode would break, so it does not meet the fallback decision on its own.

### Critical: static frontmatter has no fallback

A frontmatter pin is fixed text. `claude-gw-tier1a` outside a ccsession tier session is not served, and the existing workers then STOP (`sc-issue-protocol/refs/tiers.md:32-40`). The owner wants a fallback to the plain alias instead. Option 2 above gives that fallback without per-file logic; options 1 and 3 need an extra runtime or install-time switch. The detection rule already exists in ccsession: tier mode is on when a `T<N>_WINDOW` variable exists and `CCSESSION_TIERS` is not `0` (`ccsession-tag/models.py:469-479`). That module is a skill script, not part of the Python package, so Python CLI code must not import it; it needs its own small helper (or a shared one placed under `src/superclaude/cli/`).

### High: Python CLI hard-codes (now in scope)

| Path:line | What | Note |
|---|---|---|
| `cli/roadmap/models.py:104-105,151-152` | default `AgentSpec("opus"/"sonnet", "architect")` | `AgentSpec.id` (`:87-90`) is `{model}-{persona}` and becomes step ids and file names (`generate-opus-architect`). A picker ID changes them to `generate-claude-gw-tier1a-architect`; resume state and many tests pin today's ids |
| `cli/roadmap/executor.py:3680-3685` | same defaults after resume | same id concern |
| `cli/roadmap/commands.py:41,434` | help text and `default="opus:architect"` for `roadmap validate` | |
| `cli/recommend/eval_aggregate.py:16-21` | `MODE_MATRIX` panels | the model name is also the aggregation key and the `best_model` value written to the cache (`recommend/best_model.py:130`); changing it changes stored cache rows |
| `cli/recommend/commands.py:207` | `--eval` help text | |
| `cli/reflect/runner.py:287-310` | `_BUILTIN_ALIASES` fallback for the diversity count | counts distinct models; a remap to tiers changes the count (tier1a and tier1b both contain Claude Sonnet 5.5, `MODEL-TIERS.md:38-39`) |
| `cli/reflect/commands.py:31,359` | `_DEFAULT_MODEL = "claude-opus-4-8"` | a full model id, not in the issue, and not a model in today's tier table (`MODEL-TIERS.md:37-42`) |
| `cli/sprint/summarizer.py:47-51,330-331` | `SONNET_MODEL = "sonnet"` | its comment explains the alias is deliberate for proxy routing; the mapping would make it `claude-gw-tier1b` in tier mode |
| `cli/sprint/aienv.py:43-47` | `_ANTHROPIC_SLOTS` rotation `opus` -> `sonnet` -> `haiku` | suggests alternate `--model` tokens on exhaustion; tier names would need their own rotation order |
| `cli/user_settings_defaults.json:3` | `"model": "opus[1m]"` installed into the user's settings by `install_user_setup.py:157,312` | the main-session default; under the mapping this would be `claude-gw-tier1a[1m]` only inside tier mode, which a static settings file cannot express |
| `cli/eval/suites/*.yaml` | `--agents opus,sonnet,haiku` prompts and comments | eval fixtures; comments record old alias targets (`glm-5.1`, `gpt-5.5`) that are already stale against `MODEL-TIERS.md` |

### High: commands and skills not listed in the issue

- `commands/release-split.md:41,45,60,97`; `skills/sc-release-split-protocol/SKILL.md:92,194`; `refs/adversarial-integration.md:32-39`.
- `commands/roadmap.md:26,72`; `skills/sc-roadmap-protocol/SKILL.md:75,146`.
- `commands/adversarial.md:29,90,112,120,126`; `skills/sc-adversarial-protocol/refs/agent-specs.md:25-27,53-55,80-89`; `SKILL.md:73-76,437,467,475,2127,2323-2405`.
- `skills/sc-brainstorm-protocol/SKILL.md:221,245`; `refs/agent-spec-builder.md:57-73,109-119,165-168`.
- `skills/sc-cli-eval-protocol/SKILL.md:5`; `refs/integration-map.md:40`.
- `skills/sc-recommend/SKILL.md:332-334` (eval fan-out per model).
- `skills/sc-troubleshoot-protocol/SKILL.md:411`.
- `skills/sc-reflect-protocol/SKILL.md:33,601-605,1169,1337-1339`; `refs/reviewer-spec.md:96-108`; `refs/reflection-rubric.md:139-167`. Reflect's design depends on reviewers being different model classes; tier1a and tier1b share Claude Sonnet 5.5 in their failover lists, so the diversity argument needs rechecking under the mapping.
- `skills/sc-implement-protocol/refs/retry.md:162-179`. Its primary ladder names `T3_Model01`, `T2_Model02`, `T1_Model02`, `T1_Model01`, but the Coder env exports `T3Model01`, `T2Model02`, `T1Model01`, `T1aModel01` (no underscore). The primary ladder therefore never activates and the alias fallback ladder `haiku`/`sonnet`/`opus` is what runs. Fixing the variable names is a separate bug, but it decides whether this ladder needs the alias mapping at all.
- `skills/task-builder/SKILL.md:1088,2170` (`executor_model_class`).

### Medium: mirrors, tests and docs

- `plugins/superclaude/` mirror carries the same aliases in `commands/brainstorm.md`, `commands/recommend.md`, `skills/sc-recommend/SKILL.md`, `skills/sc-implement-protocol/refs/retry.md`.
- `.claude/` dev copies are regenerated by `make sync-dev` and are never staged.
- Tests that pin today's aliases and will need updating: `tests/commands/test_auggie_review_revagent.py`, `tests/recommend/test_eval_pipeline.py`, `tests/recommend/test_best_model.py`, `tests/sprint/test_aienv.py`, `tests/sprint/test_models.py`, `tests/roadmap/test_resume_restore.py` (49 hits), `tests/roadmap/test_cli_contract.py`, `tests/roadmap/test_models.py`, `tests/roadmap/test_validate_unit.py`, `tests/sc-roadmap/integration/test_adversarial_pipeline.py`, `tests/skills/test_implement_adviser_family.py`. New tests follow `tests/skills/test_issue_worker_agents.py:21-25`, which already cross-checks picker IDs against `ccsession-models.json`.
- Docs: `docs/user-guide/commands.md`, `docs/user-guide/brainstorm.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`.

### Low: existing inconsistencies found on the way

- `cleanup-audit` says `audit-scanner` runs on Haiku (`skills/sc-cleanup-audit-protocol/SKILL.md:68,74,95,99`, `commands/cleanup-audit.md:43,53`), but `agents/audit-scanner.md:5` pins `sonnet`.
- Prose model guidance with no frontmatter: `agents/debate-orchestrator.md:21` ("opus preferred"), `agents/merge-executor.md:21` ("opus or sonnet").
- Prose mentions that are not selections and should stay: the `sc-adversarial-protocol/SKILL.md:2853` model-name scrub pattern list, `generate-opus-architect` examples in `roadmap/envelope.py`, `tool_writer.py`, `executor.py:1246`, and attribution examples in `refs/debate-protocol.md`, `refs/artifact-templates.md`. `templates/modularization-template-review/*` carry `ai_model: "claude-sonnet-5"` provenance fields, not selections.

## 3. Counts

| Area | Selection sites found | In the issue |
|---|---|---|
| Agent and skill frontmatter | 14 | 14 |
| Command and skill text (defaults, validation, dispatch) | about 30 files | 13 files |
| Python CLI | 11 sites in 9 files | 5 files |
| Plugin mirror | 4 files | 0 |
| Tests to update | 11 or more files | 1 (as a pattern) |

## 4. Recommendations

1. Decide the mechanism first (section 2, Critical). Option 2 (session-level remap of `ANTHROPIC_DEFAULT_*_MODEL` inside ccsession tier sessions) is the only one that covers the Agent-tool `model` parameter and the outside-workspace fallback without per-skill logic; it requires a change in ccsession launch code, so coordinate with issue #315, and verify that Claude Code accepts a picker ID in those variables.
2. If option 2 is chosen, most primitive text stays as plain aliases and the work shrinks to: Python sites that bypass aliases (`reflect/commands.py:31`), documentation of the mapping, and tests. If it is not, every Agent-tool dispatch site in section 2 must move to tier agent files.
3. Keep model names out of persisted ids where possible (roadmap `AgentSpec.id`, recommend `best_model`) or plan a migration for resume state and cache rows.
4. Fix `retry.md` variable names separately (bug), then decide whether its fallback ladder follows the mapping.
5. Resolve the `audit-scanner` Haiku versus sonnet contradiction while touching those files.
