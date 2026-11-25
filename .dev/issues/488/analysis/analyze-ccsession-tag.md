# /sc:analyze --depth deep: ccsession tier change (GLM 5.3 default for Tier 3, Tier 3 to Tier 2b, new Tier 3 and Tier 4)

Source of the request: `<D>/description.md` (authoritative). Written by issue-worker-t1, 2026-11-10.
Tools: codegraph and auggie MCP tools were NOT available to this worker; the pass used Grep, Glob, Read and one batched read-only Bash.
`<D>` = `.dev/issues/draft-20261110-163550-set-glm5-3-as-the-default-model-for-clau`.

## A. Summary and approach

1. The models in each tier come from the Coder workspace env file (deployed at `/etc/aidev02/aienv.d/defaults.sh`; source in the IronbellyOrg/Coder repo, `templates/VSCode-AIDev02/aienv.d/defaults.sh`, outside this repo). This repo's `ccsession-models.json` only names each tier's env slot variables (`models_env`), so most of the model change lands in Coder, not here.
2. In this repo the change is: add a `tier2b` entry (slots `T2bModel01..`), cut `tier3` to 3 slots and grow `tier4` to 2 slots in `src/superclaude/skills/ccsession-tag/ccsession-models.json`, register `claude-haiku-5-5` for display, then update the docs and tests that hard-code the tier list or the Tier 3/Tier 4 contents.
3. No launcher or proxy code change is needed. The regexes already accept letter tiers (`models.py` lines 64-70, `local-gateway-alias-proxy.py` line 568), so `tier2b`, `T2bModel01` and `T2b_WINDOW` work as they are.
4. The Coder defaults.sh must gain the `T2b*` and `T4Model02` slots BEFORE this repo's JSON reaches master, because every launch fetches the JSON from master (`models.py` lines 54-58), and a slot that the JSON names but the env does not set stops the launch (`models.py` lines 663-664).
5. Several points of the request conflict or are underspecified (where Terra goes, the order inside Tier 3, the Tier 2b picker id, the issue-worker-t3 pin, Haiku 5.5's window). They are listed in section E, not guessed.

## B. EDIT PLAN

Rows marked "conditional" depend on an answer in section E. Line numbers were read in this session. The defaults.sh lines come from the deployed copy `/etc/aidev02/aienv.d/defaults.sh`, not from the Coder repo file (see F).

### B1. Tier definitions and config

| File | Line(s) | Current text or behavior | Necessary change | Why |
|---|---|---|---|---|
| Coder repo `templates/VSCode-AIDev02/aienv.d/defaults.sh` (deployed copy `/etc/aidev02/aienv.d/defaults.sh`) | 47-59 | `T3_WINDOW=500000`; `T3Model01=gpt-6.1-terra`, `T3Model02=glm-5.3`, `T3Model03=grok-4.7`, `T3Model04=Qwen3.8-max`, `T3Model05=muse-wonder-1.0`, `T3Model06=muse-spark-1.3`, each with a `_WINDOW` | Add `T2b_WINDOW` and `T2bModel01..06` (+ a `_WINDOW` for each) carrying today's Tier 3 list (conditional, E1/E3). Rewrite Tier 3 as `T3Model01=glm-5.3`, `T3Model02=grok-4.7`, `T3Model03=Qwen3.8-max` (the order of 02/03 is conditional, E2). Delete `T3Model04..06` and their `_WINDOW` lines only after the JSON merges (section C). Keep `T3_WINDOW` at 500000 or less (E6). | Owner update: "Tier 3 changes to Tier 2b / New Tier 3 = GLM5.3, Grok 4.7, Qwen 3.8". Request (1): GLM 5.3 is the default (first) model of claude-gw-tier3. Outside this repo: a separate Coder PR. |
| same | 60-62 | `T4_WINDOW=500000`; `T4Model01=gpt-6-luna`, `T4Model01_WINDOW=850000` | Add `T4Model02=claude-haiku-5-5` and `T4Model02_WINDOW=<its window>` (the window is Not known yet, E6/E7). | Owner update: "Tier 4 = GPT 6 Luna, Claude Haiku 5.5". |
| same | 79-83 | `CCSESSION_TIER_RULES="... *=tier2:tier2,tier3,tier4"` | Conditional (E5): add `tier2b` to the member list, for example `*=tier2:tier2,tier2b,tier3,tier4`. The owner roles (which start on `tier1b` with no list) already see every tier. | Without it, members lose access to today's Tier 3 models, because those models move to a tier the member list does not include. |
| same | 84 | `CCSESSION_MODEL_ORDER="... gpt-6.1-terra gpt-6-luna ... Qwen3.8-max"` (no `claude-haiku-5-5`) | Add `claude-haiku-5-5` (position Not known yet). | This sets the `+models` listing order. How a model missing from the order is listed is UNVERIFIED. |
| same | 92 | `ANTHROPIC_DEFAULT_HAIKU_MODEL="${T2Model02}"` (glm-5.3) | Conditional (E8): no change unless the owner wants `haiku` to mean Haiku 5.5. | This is the fallback outside tier mode only; tier mode exports it again (see B2). |
| `src/superclaude/skills/ccsession-tag/ccsession-models.json` | 3 | `"version": "2026-10-28.1"` | Bump it (for example `"2026-11-10.1"`; the format is UNVERIFIED beyond the existing example). | The newest version wins when the cached and fetched copies differ. |
| same | 93-103 (tier2), then 104 | `tier3` follows `tier2` directly | Insert `"tier2b": {"label": "Tier 2b", "models_env": ["T2bModel01", ..., "T2bModel06"]}` between `tier2` and `tier3` (the slot count is conditional, E3). | The key order in `tiers` is the picker and listing order, so `tier2b` must sit between Tier 2 and Tier 3. |
| same | 104-114 | `tier3`: `"label": "Tier 3"`, `models_env` `T3Model01..T3Model06` | Set `models_env` to `["T3Model01", "T3Model02", "T3Model03"]`. | The new Tier 3 has three models. Leftover slot names would stop launches once Coder deletes `T3Model04..06` (`models.py` 663-664). |
| same | 115-120 | `tier4`: `["T4Model01"]` | Set it to `["T4Model01", "T4Model02"]`. | Tier 4 gains Haiku 5.5. |
| same | 123-140 (`picker.show`) | No `gpt-6.1-terra`, no `claude-haiku-5-5` | Conditional: add `claude-haiku-5-5` if it should appear by name in `/model` under `+models`. | Display only. |
| same | 141-154 (`one_million_context`) | Includes `gpt-6.1-terra` (line 153) | Add `claude-haiku-5-5` only if its window is 1M-class (Not known yet, E6). | This controls the `[1m]` suffix. |
| same | 155-171 (`display_overrides`) | `gpt-6-luna` (166), `gpt-6.1-terra` "GPT 6.1 Terra" (169), `glm-5.3` (170); no `claude-haiku-5-5` | Add `"claude-haiku-5-5": "Claude Haiku 5.5"` (the exact label is Not known yet). | Gives a readable name in listings. |

### B2. Launcher code

| File | Line(s) | Current text or behavior | Necessary change | Why |
|---|---|---|---|---|
| `src/superclaude/skills/ccsession-tag/models.py` | 64-70 | `_TIER ^tier([0-9]{1,2}[a-z]?)$`, `_SLOT ^T([0-9]{1,2}[a-z]?)Model[0-9]{2}$`, `_ENV_NAME` | None. | These already accept `tier2b`, `T2bModel01` and `T2b_WINDOW`. |
| same | 532 | Docstring example `role:owner=tier1a+models *=tier2:tier2,tier3,tier4` | Optional: add `tier2b` to the example. | Keeps the example in step with the new tier set. Not functional. |
| same | 650-673, 871-891, 959-997 | `_all_tiers`, tier-resolve, default-tier (which falls back to `tier2` at 970-974) | None. | They are generic over the JSON's tiers. |
| `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` | 17-21, 120, 568, 705-817 | `TIER_PREFIX = "claude-gw-tier"`, the tier regex, and the `_forward_tier` failover; the window skip is at 720-722 | None. | Generic. Lines 720-722 skip a backup whose window is below the tier window, which matters for E6. |
| `src/superclaude/skills/ccsession-tag/ccsession` | 880-898 | Tier mode; exports `ANTHROPIC_DEFAULT_OPUS/SONNET/HAIKU_MODEL = claude-gw-tier1a/1b/2` (896-898) | None, unless E8 decides that `haiku` maps to `claude-gw-tier4`. | The alias mapping is not part of the request. |
| `src/superclaude/cli/install_ccsession.py` | 13, 50 | Copies the skill directory | None. | No new file is added. |
| `src/superclaude/cli/sprint/aienv.py` | 78-82 | Reads only `T2Model0{N}` | None. | `T2bModel0N` does not match `T2Model0`, so there is no collision. |
| swarm `config.py` | 59 | `T2_MODEL_ENV_PREFIX = "T2Model0"` | None. | Same reason. |

### B3. Agents, skills and commands

| File | Line(s) | Current text or behavior | Necessary change | Why |
|---|---|---|---|---|
| `src/superclaude/agents/issue-worker-t3.md` | 6, 11 | `model: claude-gw-tier3`; provenance line | Conditional (E4): keep it (it then runs on GLM 5.3, then Grok, then Qwen) or change it to `claude-gw-tier2b` (which keeps today's Terra-first models). | The issue protocol has no alias fallback: an unreachable pin stops with E-TIER-UNAVAILABLE. |
| `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` | 11-15 (line 13 = T3 `claude-gw-tier3`), 26, 37 | Tier map for the three workers | Update the T3 row text only if E4 changes the pin or the model description; otherwise none. | Must match the agent pin and the tests. |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | 58-60 | Worker tier mention | Same condition as above. | Consistency. |
| `src/superclaude/skills/sc-implement-protocol/refs/retry.md` | 162, 172 | Rung 0 is `T3Model01` (today gpt-6.1-terra, "gpt" family) | Review the text. After the change `T3Model01` is glm-5.3, which belongs to neither the `claude-` nor the `gpt-` family. Change the rung or its family note per E9. | This changes how the retry ladder behaves, since it alternates by family. |
| `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md` | 162, 172 | Identical copy | Same edit as the src copy. | Tracked mirror; the tests read both (`RETRY_REFS`). |
| `src/superclaude/skills/sc-issue-protocol/refs/chains.md` 11-16, 21; `refs/claim.md` 79; `templates/next-steps.md` 1 | — | They reference tier2 and tier1a only | None. | Not affected. |

### B4. Docs

| File | Line(s) | Current text or behavior | Necessary change | Why |
|---|---|---|---|---|
| `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` | 5-7 | Dates | Update the "updated" date. | Records the change. |
| same | 27-30 | Members see Tiers 2, 3 and 4 | Add Tier 2b if E5 says yes. | Access text. |
| same | 35-42 | Tier table: Tier 3 (41) is Terra first, six models, 500K; Tier 4 (42) is Luna only, 500K | Add a Tier 2b row (today's Tier 3 list). Change Tier 3 to GLM 5.3, Grok 4.7, Qwen 3.8 (window per E6), and Tier 4 to GPT 6 Luna, Claude Haiku 5.5. | This is the main tier table for readers. |
| same | 55 | Muse Wonder in Tiers 2 and 3 | Change to Tiers 2 and 2b (if E3 keeps it there). | Muse leaves Tier 3. |
| same | 66-94 (scoreboard statuses: Grok 79, Qwen 81, GLM 82, Muse Wonder 74, Muse Spark 76, Luna 90, Haiku 4.5 Excluded 94) | Tier membership per model | Update the tier list of each moved model, and add a Claude Haiku 5.5 row (score Not known yet, E7). | The scoreboard names the tiers of each model. |
| same | 101-139 | By-provider tables | Make the same membership updates, and add Haiku 5.5 under Anthropic. | Consistency. |
| same | 150 | Haiku 4.5 excluded | Add a note on where Haiku 5.5 is placed (E7). | Avoids contradicting "Haiku excluded". |
| same | 157-173 | Placement rules | Check rules 1 and 2 against Haiku 5.5, which is unscored (E7); amend them or record the owner's exception. | Haiku 5.5 may break the existing rules. |
| same | 180-184 | Update steps ("Add the env slots in Coder first") | None; follow them (section C). | They already describe the order. |
| same | 216 | Note that `claude-haiku-5-5` is unscored | Update it once Haiku 5.5 is placed in Tier 4. | Stale after the change. |
| `src/superclaude/skills/ccsession-tag/README.md` | 413-447 (naming at 446-447) | Tiers section | Add Tier 2b (`claude-gw-tier2b[1m]`) to the list and explanation. | Documents the picker IDs. |
| same | 454 | Example `CCSESSION_TIER_RULES="... *=tier2:tier2,tier3,tier4"` | Add `tier2b` if E5 says yes. | The example should match the deployment. |
| same | 509 | `CCSESSION_DEFAULT_TIER` text | None expected. | The default stays tier2. |
| same | 540-545 | Profile rows | Review only; change them if they name tier membership. | Whether they mention anything beyond the profile names is Not known yet. |
| `docs/reference/model-aliases.md` | 16-18, 26-35, 42, 63 | Alias mapping; mentions `T3Model01` at defaults.sh line 48 | Update the mention of `T3Model01` and defaults.sh line 48 (it becomes glm-5.3, and the line may move). Lines 16-18 stay, because a test pins them. | Stale reference. |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | 423 | Example `claude-gw-tier3` | Change it only if E4 moves the pin. | Example text. |
| `docs/designs/sc-issue-command.md` | 52 (also 53, 96, 118, 364, 394, 420) | Lists tiers "tier0, tier1a, tier1b, tier2, tier3, tier4" | Recommend no edit, since it is a historical design (E10). | Design record. |
| `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` (119, 128-129, 190-193) and `D08-ccsession.md` (387-388) | — | Test scripts versioned to 5.0.0 | Recommend no edit; record the drift (E10). | Versioned docs. |
| `CHANGELOG.md` | 5 | `## [Unreleased]` | Add an entry: Tier 2b added, Tier 3 = GLM 5.3, Grok 4.7, Qwen 3.8, and Tier 4 adds Claude Haiku 5.5. | Release notes. |

### B5. Tests

| File | Line(s) | Current text or behavior | Necessary change | Why |
|---|---|---|---|---|
| `tests/unit/test_ccsession_tiers.py` | 36-88 (TIER_BLOCK; T3 at 69-81, T4 at 82-84 `T4_WINDOW=850000`, `T4Model01=gpt-6-luna`) | Fixture env | Add `T2b_WINDOW` and `T2bModel01..06`; cut T3 to three models (glm, grok, qwen); add `T4Model02=claude-haiku-5-5` and its window. | The bundled JSON will name these slots, and a missing slot fails the launch. |
| same | 131 | `TIER_IDS = [f"claude-gw-tier{n}[1m]" for n in ("0","1a","1b","2","3","4")]` | Insert `"2b"` after `"2"`. | The picker ID list grows. |
| same | 179 | Tier order list | Insert `tier2b`. | Order assertion. |
| same | 538-539 | tier4 launch | Review the expected first model (still Luna) and any assertion on the number of models. | Tier 4 has two models. |
| same | 791-792 | `listing[3]` is Tier 2 Muse Spark | Recheck the index; list positions shift when a tier is inserted. | Index-based assertion. |
| same | 813-829 | `ids[:6]` and the show-all order list with Terra and Luna | Change to `ids[:7]`; add Haiku 5.5 if `picker.show` gains it. | The count and order change. |
| same | 2334-2355, 2374, 2422, 2733, 2747, 2750, 2758, 2810 | Tier lists | Insert `tier2b` wherever all tiers or the member tiers are listed. | The tier set changes. |
| same | 2628 | Terra in bob's tiers | Work it out again: Terra moves to Tier 2b (E1). | Membership changes. |
| same | 2721-2732 | `MODEL_ORDER`, `RULES_BLOCK` | Add `claude-haiku-5-5` to the order; add `tier2b` to the member rule if E5 says yes. | These copy defaults.sh. |
| same | 2824 | Terra window 850000 | Keep it, if Terra stays in Tier 2b. | — |
| same | 2843-2859 | `ids[:6]`, display names including "GPT 6.1 Terra" (2850), `listing[3]` Tier 2 | Update the count, the names (add "Claude Haiku 5.5") and the indices. | The listing changes. |
| same | 2872 | Member IDs for tiers 2, 3 and 4 | Add `claude-gw-tier2b[1m]` if E5 says yes. | Member access. |
| same | 2888 | A tier assertion (not re-read after compaction) | Review it together with 2893. | — |
| same | 2893 | `assert gateway.models_called() == ["gpt-6.1-terra"]` (tier3's first model) | Change it to `["glm-5.3"]` for tier3, or move this check to tier2b. | Request (1): GLM is the default of Tier 3. |
| same | 2995-3029 | tier1a/1b deletion test | Review only. | Generic over tiers; probably unaffected. |
| `tests/skills/test_issue_worker_agents.py` | 21-25 (`"issue-worker-t3": ("claude-gw-tier3", "tier3")`), 71-74 | The pin must exist as a tier key in the JSON | Change it only if E4 moves the pin to `tier2b`. | The test pins the agent. |
| `tests/skills/test_model_alias_policy.py` | 29-33 (`ISSUE_WORKER_PINS`), 38-42, 215-226 (requires `T3Model01` in retry.md), 229-241 | Pins and retry names | Line 30: change only if E4 moves the pin. Line 225: keep `T3Model01` unless E9 renames the rung. | Policy tests. |
| `tests/skills/test_workflow_archive.py` | 797-805 | `RUNGS` includes `"T3Model01"` | Change only if E9 changes the rung. | Retry ladder. |
| `tests/unit/test_ccsession_tag.py` | 999-1002, 1831-1838 | Validates the shipped data; builds the env generically from the bundled tiers | None expected, since it adapts. Run it to confirm. | — |
| `tests/sprint/test_aienv.py` 18-20, 167-169; `tests/swarm/test_coder_tier_env_2026_10.py` 132-134; `tests/unit/test_cli_install.py` 189-190 | — | Alias mapping and the file list | None. | Not affected. |

### B6. Mirrors and plugins

| File | Line(s) | Current text or behavior | Necessary change | Why |
|---|---|---|---|---|
| `.claude/skills/ccsession-tag/`, `.claude/agents/issue-worker-t3.md`, `.claude/skills/sc-issue-protocol/`, `.claude/skills/sc-implement-protocol/` | — | Gitignored copies made by sync-dev | Run `make sync-dev`, then `make verify-sync`. Never stage `.claude/`. | Project rule. |
| `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md` | 162, 172 | Tracked mirror | Same edit as the src copy (B3) if E9 changes it. | The test reads both. |
| A plugins mirror for ccsession-tag, sc-issue-protocol or the issue-worker agents | — | None exists | None. | — |
| Installed copies (`~/.claude/...`) | — | Updated by `superclaude install` | Reinstall after the merge. Launches also fetch the JSON again from master. | Runtime. |

## C. Order of edits and dependencies

1. The owner answers section E (at least E1-E6) before any edit, because the slot counts in the JSON depend on the answers.
2. Coder repo PR first: add `T2b_WINDOW` and `T2bModel0N`, rewrite Tier 3, add `T4Model02` and its window, and extend `CCSESSION_TIER_RULES` and `CCSESSION_MODEL_ORDER`. Until the JSON merges, keep the old `T3Model04..06` lines: extra slots the JSON does not name are harmless, but slots the JSON names and the env lacks stop the launch. MODEL-TIERS.md 180-184 already says "Add the env slots in Coder first".
3. Workspaces pick up the new defaults.sh. How (rebuild or restart) is UNVERIFIED.
4. One IronClaude PR: `ccsession-models.json` (B1), docs (B4), tests (B5), any consequences of E4/E8/E9 (B3), and the CHANGELOG. Run `uv run pytest tests/unit/test_ccsession_tiers.py tests/unit/test_ccsession_tag.py tests/skills/test_issue_worker_agents.py tests/skills/test_model_alias_policy.py tests/skills/test_workflow_archive.py`.
5. Run `make sync-dev` and `make verify-sync`. Stage only `src/`, `tests/`, `docs/`, `plugins/` and `CHANGELOG.md`.
6. After the merge to master, the next launch fetches the new JSON. Only then remove `T3Model04..06` from Coder (an optional cleanup PR).
7. Under the project hard limit (more than one source file), the IronClaude side needs a written plan (`/sc:workflow`, level 3).

## D. Risks and migration effects

- **Launch failure from the order of merges:** if the JSON lands on master before Coder sets the `T2b*` and `T4Model02` slots, every ccsession launch in tier mode stops with "X is not set (needed by tier)" (`models.py` 663-664). This is the highest risk.
- **A silent change for claude-gw-tier3 users and pins:** `issue-worker-t3` (pinned to `claude-gw-tier3`) and anyone who selects Tier 3 move from Terra first to GLM first, with only Grok and Qwen behind it. Tier 3 has no Terra fallback unless E1 adds one.
- **Members lose access:** if `CCSESSION_TIER_RULES` does not gain `tier2b`, members lose Terra and the Muse models outside Tier 2.
- **Window skip:** a `T3_WINDOW` above 500000 makes the proxy skip Grok (window 500000) as a backup (proxy 720-722). If Haiku 5.5's window is below `T4_WINDOW`, it is skipped as a Tier 4 backup in the same way.
- **Retry ladder:** rung 0 `T3Model01` becomes glm-5.3, which is in neither family, so the family alternation in retry.md may no longer work as designed (E9).
- **Listing indices:** inserting a tier shifts list positions, so the index-based tests (791-792, 2843-2859) break until they are updated.
- **Haiku 5.5 policy:** it is unscored (MODEL-TIERS.md 216), and Haiku 4.5 was excluded (150). Placing it may contradict the placement rules (157-173).
- **Older ccsession:** older launchers ignore the tier lines (comment at defaults.sh 63-65), so they are unaffected.

## E. OPEN QUESTIONS

1. **Where does GPT 6.1 Terra go?** Request (1) says "GLM5.3 as the default model for claude-gw-tier3[1m] with gpt 6.1 Terra as the fallback". The owner update says "New Tier 3 = GLM5.3, Grok 4.7, Qwen 3.8", which leaves Terra out. Evidence: today Terra is `T3Model01` (defaults.sh 48). Options: (a) Terra only in Tier 2b; (b) Tier 3 = GLM, Terra, Grok, Qwen; (c) Tier 3 = GLM, Grok, Qwen, Terra.
2. **Order inside the new Tier 3.** Request (1) fixes GLM first. The update lists Grok 4.7 before Qwen 3.8, but the list may be a set rather than a failover order.
3. **Is Tier 2b a new picker ID?** "Tier 3 changes to Tier 2b" implies a new tier `tier2b` (`claude-gw-tier2b[1m]`, slots `T2bModel0N`, `T2b_WINDOW`) holding today's six Tier 3 models in today's order (Terra, GLM, Grok, Qwen, Muse Wonder, Muse Spark). This is not stated. Its label ("Tier 2b") and window (today `T3_WINDOW=500000`) are also unstated.
4. **The issue-worker-t3 pin.** `src/superclaude/agents/issue-worker-t3.md` line 6 pins `claude-gw-tier3`. Keep it (GLM first) or move it to `claude-gw-tier2b` (Terra first, as today)? The tests at test_issue_worker_agents.py 21-25 and test_model_alias_policy.py 29-33 follow the answer.
5. **Member access to Tier 2b.** defaults.sh line 83 gives members `tier2,tier3,tier4`. Should `tier2b` be added? MODEL-TIERS.md 27-30 and README 454 follow the answer.
6. **Windows.** The new `T3_WINDOW` (it must stay at or below 500000 to keep Grok as a backup), `T2b_WINDOW`, `T4_WINDOW` (500000 today), and Haiku 5.5's context window (Not known yet). The Haiku window decides `one_million_context` and whether Haiku is skipped in Tier 4.
7. **Haiku 5.5 and the placement rules.** It is unscored (MODEL-TIERS.md 216), and Haiku 4.5 is Excluded (94, 150). Does the owner's instruction override the placement rules, and what score and status row should be recorded?
8. **The `haiku` alias.** In tier mode `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` (ccsession 896-898; pinned by test_model_alias_policy 229-241). Should it move to `claude-gw-tier4` now that Tier 4 holds a Haiku model? This is not requested; the default answer is no.
9. **Retry ladder rung 0.** `retry.md` 162/172 uses `T3Model01`, which today is Terra (gpt family). After the change it is glm-5.3. Keep it, switch it to `T2bModel01` (Terra), or accept the family change?
10. **Historical and versioned docs.** Update `docs/designs/sc-issue-command.md` (52 and others) and `docs/testing/v5.0.0/...` (E01, D08), or leave them as records?
11. **Gateway ID spellings.** The only spelling of Haiku 5.5 in the repo is `claude-haiku-5-5` (MODEL-TIERS.md 216). "Qwen 3.8" is assumed to be `Qwen3.8-max` (defaults.sh 41, 54). Both need confirming.

## F. UNVERIFIED

- The IronbellyOrg/Coder repo file `templates/VSCode-AIDev02/aienv.d/defaults.sh` was not read. The line numbers in B1 come from the deployed copy `/etc/aidev02/aienv.d/defaults.sh` and may differ in the repo.
- Whether the live gateway serves `claude-haiku-5-5`, `glm-5.3`, `grok-4.7`, `Qwen3.8-max`, `gpt-6-luna` and `gpt-6.1-terra` today.
- Claude Haiku 5.5's context window and output limits.
- The `CCSESSION_TIER_RULES` deployed in workspaces other than this one.
- The version string format the JSON loader expects, beyond the existing `YYYY-MM-DD.N` example.
- How a model missing from `CCSESSION_MODEL_ORDER` is listed under `+models`.
- How and when workspaces reload a changed defaults.sh.
- The location of swarm `config.py` line 59 was recorded before compaction without its full path. README lines 540-545 (beyond the profile names) and the exact assertions at test lines 538-539 and 2888 were noted but not re-read after compaction. Re-read them before editing.
