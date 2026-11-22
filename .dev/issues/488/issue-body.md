<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Rename the current Tier 3 to Tier 2b, create a new Tier 3 containing GLM 5.3, Grok 4.7 and Qwen 3.8, and set Tier 4 to GPT 6 Luna and Claude Haiku 5.5. The original request also specifies GLM 5.3 as the default for `claude-gw-tier3[1m]` with GPT 6.1 Terra as fallback; how that fits the revised tier membership needs clarification (open question 1).

## Owner decisions (2026-11-10 to 2026-11-11) - these supersede conflicting text below

Final tier table (owner-confirmed; Grok 4.7 moved to Tier 4 by the owner; models in failover order, windows in brackets; gateway IDs are the assumed spellings, not checked against the live gateway):

| Tier | Window | Slots and models |
|---|---|---|
| tier2b (new, label "Tier 2b", `claude-gw-tier2b[1m]`) | 900000 | `T2bModel01..04` = gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0 (4 slots; Muse Spark 1.3 stays in Tier 2 only) |
| tier3 | 900000 | `T3Model01..02` = glm-5.3, Qwen3.8-max (2 slots) |
| tier4 | 500000 | `T4Model01..03` = gpt-6-luna [900000], claude-haiku-5-5 [900000], grok-4.7 [500000] (3 slots) |

- Member rule: `*=tier2:tier2,tier2b,tier3,tier4`. GPT 6.1 Terra is in Tier 2b only. Tier 2 keeps Grok.
- Meaning of "fallback": if GPT 6.1 Terra returns a 429 while the user has Tier 2b selected, the request is retried on GLM 5.3.
- Where the slot counts, the Grok rows, or the Grok window risk in the edit plan below say otherwise (6 slots for tier2b, 3 slots for tier3, "T3_WINDOW must stay at or below 500000"), this section wins. That window limit no longer applies because Grok left Tier 3.
- Open questions 1, 2, 3, 5, 6 and 12 below are answered by this section. Still open: 4 (issue-worker-t3 pin), 7 (Haiku 5.5 placement rules), 8 (haiku alias; Coder#494 keeps it on Tier 2), 9 (retry ladder rung), 10 (historical docs), 11 (gateway ID check).
- Merge order (verified in `src/superclaude/skills/ccsession-tag/models.py:601-606`): (1) a first Coder release adds only the slots and windows (IronbellyOrg/Coder#494, PR 495, merged 2026-11-10); (2) this repo's `ccsession-models.json` defining `tier2b`, `tier3` and `tier4` merges only after step 1 is installed in every workspace, running and stopped; (3) a second Coder release adds `tier2b` to the member rule and drops `T3Model03..06`. A member rule that names a tier the JSON does not define stops the launch, which mirrors the hazard of a JSON that names a slot the env lacks. Until step 3, members' Tier 3 is GLM and Qwen only and Terra is in no member tier.

## Problem Statement

The requested tier layout differs from the current documented layout: Tier 3 starts with Terra and Tier 4 contains Luna alone (`src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:35-42`).

## User Story

As a user selecting a tier, I want the requested model groups and default, so that tier selections use the intended models.

## Proposed Solution

Which models each tier holds comes from the Coder workspace env file (deployed at `/etc/aidev02/aienv.d/defaults.sh`; source in the IronbellyOrg/Coder repo, `templates/VSCode-AIDev02/aienv.d/defaults.sh`, outside this repo). This repo's `ccsession-models.json` only names each tier's env slot variables, so the model change lands mostly in Coder; this repo adds the new tier definition, registers Claude Haiku 5.5 for display, and updates docs and tests (`src/superclaude/skills/ccsession-tag/ccsession-models.json:93-119`, `src/superclaude/skills/ccsession-tag/README.md:413-419`).

In this repo: add a `tier2b` entry (slots `T2bModel01..`), cut `tier3` to 3 slots, grow `tier4` to 2 slots, then update the docs and tests that hard-code the tier list or the Tier 3 / Tier 4 contents. No launcher or proxy code change is needed: the regexes already accept letter tiers (`src/superclaude/skills/ccsession-tag/models.py:64-70`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:568`), so `tier2b`, `T2bModel01` and `T2b_WINDOW` work as they are.

Merge order matters. Every launch fetches the JSON from master (`models.py:54-58`), and a slot that the JSON names but the env does not set stops the launch (`models.py:663-664`). The Coder change (add the `T2b*` and `T4Model02` slots) must land before this repo's JSON reaches master. See the edit plan below and its order of work.

Open questions requiring owner decisions (rows in the edit plan marked "conditional" depend on them):

1. Where does GPT 6.1 Terra go? The original request says GLM 5.3 default with Terra as fallback for Tier 3; the update's new Tier 3 (GLM, Grok, Qwen) leaves Terra out. Today Terra is `T3Model01` (deployed defaults.sh line 48). Options: (a) Terra only in Tier 2b; (b) Tier 3 = GLM, Terra, Grok, Qwen; (c) Tier 3 = GLM, Grok, Qwen, Terra.
2. Order inside the new Tier 3: GLM first is fixed by the request; is Grok before Qwen a failover order or only a list?
3. Is Tier 2b a new picker ID (`claude-gw-tier2b[1m]`, slots `T2bModel0N`, `T2b_WINDOW`) holding today's six Tier 3 models in today's order (Terra, GLM, Grok, Qwen, Muse Wonder, Muse Spark)? Its label and window are unstated.
4. `src/superclaude/agents/issue-worker-t3.md:6` pins `claude-gw-tier3`. Keep it (it then runs on GLM first) or move it to `claude-gw-tier2b` (Terra first, as today)? The tests follow the answer.
5. Should `tier2b` be added to the member rule `CCSESSION_TIER_RULES` (`*=tier2:tier2,tier3,tier4` today, defaults.sh line 83), so members keep access to today's Tier 3 models?
6. Windows: the new `T3_WINDOW` (it must stay at or below 500000 to keep Grok as a backup, proxy `local-gateway-alias-proxy.py:720-722`), `T2b_WINDOW`, `T4_WINDOW` (500000 today), and Claude Haiku 5.5's context window (Not known yet).
7. Claude Haiku 5.5 is unscored (`MODEL-TIERS.md:216`) and Haiku 4.5 is Excluded (`MODEL-TIERS.md:94,150`). Does the owner's instruction override the placement rules (`MODEL-TIERS.md:157-173`), and what score and status row should be recorded?
8. The `haiku` alias maps to `claude-gw-tier2` in tier mode (`src/superclaude/skills/ccsession-tag/ccsession:896-898`, pinned by `tests/skills/test_model_alias_policy.py:229-241`). Should it move to `claude-gw-tier4`? Not requested; the default answer is no.
9. Retry ladder rung 0 uses `T3Model01` (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:162,172`), today Terra (gpt family). After the change it is glm-5.3, which is in neither the `claude-` nor the `gpt-` family. Keep it, switch it to `T2bModel01` (Terra), or accept the family change?
10. Update the historical design `docs/designs/sc-issue-command.md` (52 and others) and the versioned `docs/testing/v5.0.0/...` docs, or leave them as records? The analysis recommends leaving them.
11. Gateway ID spellings: `claude-haiku-5-5` is the only spelling of Haiku 5.5 in the repo (`MODEL-TIERS.md:216`); "Qwen 3.8" is assumed to be `Qwen3.8-max` (defaults.sh lines 41, 54). Both need confirming against the live gateway.
12. What does "fallback" mean for the original request: the existing tier failover (error, cooldown and window rules, `README.md:413-432`) or another behavior? The wrapper recognizes `--fallback-model` but its relationship to tier failover is not established (`src/superclaude/skills/ccsession-tag/ccsession-orca:103-108`).

## Acceptance Criteria

- [ ] The approved configuration exposes renamed Tier 2b and the new Tier 3 with GLM 5.3, Grok 4.7 and Qwen 3.8; the order and Tier 2b membership match the owner's clarified decision.
- [ ] Tier 4 contains GPT 6 Luna and Claude Haiku 5.5 in the owner-approved order.
- [ ] The approved behavior for the original GLM default and Terra fallback request is documented and verified with a controlled test, including the applicable unavailable-model case.
- [ ] When GLM is available, a launch selecting `claude-gw-tier3[1m]` is checked against the actual gateway and reports GLM 5.3 as the actual model, if that remains the approved default.
- [ ] The Coder defaults.sh change (`T2b*`, rewritten Tier 3, `T4Model02`, tier rules, model order) is merged and deployed before the IronClaude JSON reaches master; a launch in tier mode succeeds afterwards.
- [ ] Picker IDs, existing users' access rules and pinned workers (`issue-worker-t3`) follow the approved migration; focused tests cover the changed selection and access behavior.
- [ ] Tier documentation and tests pinning names, slot values, list positions and routing are updated to match the approved configuration (see the edit plan).
- [ ] `uv run pytest tests/unit/test_ccsession_tiers.py tests/unit/test_ccsession_tag.py tests/skills/test_issue_worker_agents.py tests/skills/test_model_alias_policy.py tests/skills/test_workflow_archive.py` passes, and `make sync-dev` then `make verify-sync` pass with no `.claude/` path staged.

## Out of Scope

Not known yet.

## Components Affected (from `/sc:analyze`)

Result of an `/sc:analyze --depth deep` pass (Grep, Glob and Read; codegraph and auggie were unavailable; no live gateway probe). Line numbers were read on 2026-11-10; re-read them before editing.
### Edit plan

Rows marked "conditional" depend on an open question above.

**1. Tier definitions and config**

| File | Line(s) | Current | Necessary change |
|---|---|---|---|
| Coder repo `templates/VSCode-AIDev02/aienv.d/defaults.sh` (deployed `/etc/aidev02/aienv.d/defaults.sh`) | 47-59 | `T3_WINDOW=500000`; `T3Model01=gpt-6.1-terra`, `02=glm-5.3`, `03=grok-4.7`, `04=Qwen3.8-max`, `05=muse-wonder-1.0`, `06=muse-spark-1.3`, each with `_WINDOW` | Add `T2b_WINDOW` and `T2bModel01..06` (+ `_WINDOW`s) carrying today's Tier 3 list (Q1, Q3). Rewrite Tier 3 as `T3Model01=glm-5.3`, `02=grok-4.7`, `03=Qwen3.8-max` (order of 02/03: Q2). Delete `T3Model04..06` and their `_WINDOW` lines only after the JSON merges. Keep `T3_WINDOW` at or below 500000 (Q6). |
| same | 60-62 | `T4_WINDOW=500000`; `T4Model01=gpt-6-luna`, `T4Model01_WINDOW=850000` | Add `T4Model02=claude-haiku-5-5` and `T4Model02_WINDOW=<window>` (Not known yet, Q6/Q7). |
| same | 79-83 | `CCSESSION_TIER_RULES="... *=tier2:tier2,tier3,tier4"` | Conditional (Q5): add `tier2b`, e.g. `*=tier2:tier2,tier2b,tier3,tier4`. Owner roles starting on `tier1b` with no list already see every tier. |
| same | 84 | `CCSESSION_MODEL_ORDER="... gpt-6.1-terra gpt-6-luna ... Qwen3.8-max"` (no `claude-haiku-5-5`) | Add `claude-haiku-5-5` (position Not known yet). |
| same | 92 | `ANTHROPIC_DEFAULT_HAIKU_MODEL="${T2Model02}"` | Conditional (Q8): no change unless `haiku` should mean Haiku 5.5. |
| `src/superclaude/skills/ccsession-tag/ccsession-models.json` | 3 | `"version": "2026-10-28.1"` | Bump it (e.g. `"2026-11-10.1"`; format beyond the existing example is UNVERIFIED). |
| same | 93-103, 104 | `tier3` follows `tier2` directly | Insert `"tier2b": {"label": "Tier 2b", "models_env": ["T2bModel01", ..., "T2bModel06"]}` between `tier2` and `tier3` (slot count: Q3). Key order is the picker and listing order. |
| same | 104-114 | `tier3`: `T3Model01..T3Model06` | Set `models_env` to `["T3Model01", "T3Model02", "T3Model03"]`. Leftover slot names would stop launches once Coder deletes `T3Model04..06` (`models.py:663-664`). |
| same | 115-120 | `tier4`: `["T4Model01"]` | Set it to `["T4Model01", "T4Model02"]`. |
| same | 123-140 (`picker.show`) | no `claude-haiku-5-5` | Conditional: add it if it should appear by name under `+models`. |
| same | 141-154 (`one_million_context`) | includes `gpt-6.1-terra` (153) | Add `claude-haiku-5-5` only if its window is 1M-class (Q6). |
| same | 155-171 (`display_overrides`) | `gpt-6-luna` (166), `gpt-6.1-terra` (169), `glm-5.3` (170) | Add `"claude-haiku-5-5": "Claude Haiku 5.5"` (label Not known yet). |

**2. Launcher code (no functional change expected)**

| File | Line(s) | Finding | Change |
|---|---|---|---|
| `src/superclaude/skills/ccsession-tag/models.py` | 64-70 | `_TIER`, `_SLOT`, `_ENV_NAME` regexes already accept `tier2b`, `T2bModel01`, `T2b_WINDOW` | None |
| same | 532 | docstring example `*=tier2:tier2,tier3,tier4` | Optional: add `tier2b` |
| same | 650-673, 871-891, 959-997 | `_all_tiers`, tier resolve, default tier (falls back to `tier2` at 970-974) | None, generic over the JSON's tiers |
| `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` | 17-21, 120, 568, 705-817 | `TIER_PREFIX`, tier regex, `_forward_tier` failover; window skip at 720-722 | None |
| `src/superclaude/skills/ccsession-tag/ccsession` | 880-898 | tier mode exports `ANTHROPIC_DEFAULT_OPUS/SONNET/HAIKU_MODEL = claude-gw-tier1a/1b/2` | None unless Q8 maps `haiku` to tier4 |
| `src/superclaude/cli/install_ccsession.py` 13, 50; `src/superclaude/cli/sprint/aienv.py` 78-82; swarm `config.py` 59 | - | copy the skill dir; read only `T2Model0{N}` (`T2bModel0N` does not collide) | None |

**3. Agents, skills and commands**

| File | Line(s) | Current | Necessary change |
|---|---|---|---|
| `src/superclaude/agents/issue-worker-t3.md` | 6, 11 | `model: claude-gw-tier3`; provenance line | Conditional (Q4): keep it (runs on GLM first) or change to `claude-gw-tier2b` (Terra first, as today). Unreachable pins stop with E-TIER-UNAVAILABLE. |
| `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` | 11-15 (T3 row at 13), 26, 37 | tier map for the three workers | Update the T3 row only if Q4 changes the pin or model description |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | 58-60 | worker tier mention | Same condition |
| `src/superclaude/skills/sc-implement-protocol/refs/retry.md` | 162, 172 | rung 0 is `T3Model01` (today Terra, gpt family) | Review per Q9; change the rung or its family note |
| `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md` | 162, 172 | identical tracked copy | Same edit as the src copy (tests read both) |

**4. Docs**

| File | Line(s) | Necessary change |
|---|---|---|
| `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` | 5-7 | Update the "updated" date |
| same | 27-30 | Add Tier 2b to member access if Q5 is yes |
| same | 35-42 | Add a Tier 2b row (today's Tier 3 list); Tier 3 = GLM 5.3, Grok 4.7, Qwen 3.8 (window per Q6); Tier 4 = GPT 6 Luna, Claude Haiku 5.5 |
| same | 55 | Muse Wonder in Tiers 2 and 3 becomes Tiers 2 and 2b (if Q3 keeps it there) |
| same | 66-94 | Update each moved model's tier list (Grok 79, Qwen 81, GLM 82, Muse Wonder 74, Muse Spark 76, Luna 90); add a Claude Haiku 5.5 row (score Not known yet, Q7); Haiku 4.5 Excluded at 94 |
| same | 101-139 | Same membership updates by provider; add Haiku 5.5 under Anthropic |
| same | 150, 157-173, 216 | Note where Haiku 5.5 is placed; check placement rules 1 and 2 against the unscored Haiku 5.5 or record the owner's exception; update the "unscored" note at 216 |
| same | 180-184 | None; follow "Add the env slots in Coder first" |
| `src/superclaude/skills/ccsession-tag/README.md` | 413-447 (naming 446-447) | Add Tier 2b (`claude-gw-tier2b[1m]`) to the tiers list and explanation |
| same | 454 | Add `tier2b` to the example rules if Q5 is yes |
| same | 509, 540-545 | None expected for 509; review 540-545 (profile rows) |
| `docs/reference/model-aliases.md` | 16-18, 26-35, 42, 63 | Update the `T3Model01` / defaults.sh line 48 mention (becomes glm-5.3; line may move). Lines 16-18 stay: a test pins them |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | 423 | Example `claude-gw-tier3`: change only if Q4 moves the pin |
| `docs/designs/sc-issue-command.md` (52, 53, 96, 118, 364, 394, 420); `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` (119, 128-129, 190-193), `D08-ccsession.md` (387-388) | - | Recommend no edit (historical or versioned); record the drift (Q10) |
| `CHANGELOG.md` | 5 | Add an `[Unreleased]` entry: Tier 2b added, Tier 3 = GLM 5.3, Grok 4.7, Qwen 3.8, Tier 4 adds Claude Haiku 5.5 |

**5. Tests**

| File | Line(s) | Necessary change |
|---|---|---|
| `tests/unit/test_ccsession_tiers.py` | 36-88 (TIER_BLOCK; T3 at 69-81, T4 at 82-84) | Add `T2b_WINDOW` and `T2bModel01..06`; cut T3 to glm, grok, qwen; add `T4Model02=claude-haiku-5-5` and its window |
| same | 131 | `TIER_IDS`: insert `"2b"` after `"2"` |
| same | 179 | Tier order list: insert `tier2b` |
| same | 538-539 | tier4 launch: review expected first model (still Luna) and model-count assertions |
| same | 791-792 | `listing[3]` (Tier 2 Muse Spark): recheck the index, positions shift when a tier is inserted |
| same | 813-829, 2843-2859 | `ids[:6]` becomes `ids[:7]`; update show-all order and display names (add "Claude Haiku 5.5" if `picker.show` gains it; "GPT 6.1 Terra" at 2850); recheck `listing[3]` |
| same | 2334-2355, 2374, 2422, 2733, 2747, 2750, 2758, 2810 | Insert `tier2b` wherever all tiers or member tiers are listed |
| same | 2628, 2824 | Terra moves to Tier 2b (Q1): rework bob's tiers; keep the 850000 Terra window if it stays in Tier 2b |
| same | 2721-2732 | `MODEL_ORDER`, `RULES_BLOCK`: add `claude-haiku-5-5`; add `tier2b` to the member rule if Q5 is yes |
| same | 2872 | Member IDs: add `claude-gw-tier2b[1m]` if Q5 is yes |
| same | 2888, 2893 | Line 2893 asserts `gateway.models_called() == ["gpt-6.1-terra"]` for tier3: change to `["glm-5.3"]`, or move that check to tier2b. Re-read 2888 before editing |
| same | 2995-3029 | tier1a/1b deletion test: review only |
| `tests/skills/test_issue_worker_agents.py` | 21-25, 71-74 | Pin `("claude-gw-tier3", "tier3")` must exist as a tier key; change only if Q4 moves the pin |
| `tests/skills/test_model_alias_policy.py` | 29-33 (30), 38-42, 215-226 (225), 229-241 | Line 30 only if Q4; line 225 keeps `T3Model01` unless Q9 renames the rung |
| `tests/skills/test_workflow_archive.py` | 797-805 | `RUNGS` includes `"T3Model01"`: change only if Q9 changes the rung |
| `tests/unit/test_ccsession_tag.py` | 999-1002, 1831-1838 | None expected (adapts to the bundled tiers); run it to confirm |
| `tests/sprint/test_aienv.py` 18-20, 167-169; `tests/swarm/test_coder_tier_env_2026_10.py` 132-134; `tests/unit/test_cli_install.py` 189-190 | - | None |

**6. Mirrors**

Run `make sync-dev` then `make verify-sync`; never stage `.claude/` (gitignored copies of `ccsession-tag`, `issue-worker-t3`, `sc-issue-protocol`, `sc-implement-protocol`). Reinstall (`superclaude install`) after the merge; launches also fetch the JSON again from master.

### Order of work

1. Owner answers Q1-Q6 first; slot counts in the JSON depend on them.
2. Coder repo PR first: add `T2b_WINDOW` and `T2bModel0N`, rewrite Tier 3, add `T4Model02` and its window, extend `CCSESSION_TIER_RULES` and `CCSESSION_MODEL_ORDER`. Keep the old `T3Model04..06` lines until the JSON merges (extra slots the JSON does not name are harmless).
3. Workspaces pick up the new defaults.sh (how: UNVERIFIED).
4. One IronClaude PR: `ccsession-models.json`, docs, tests, consequences of Q4/Q8/Q9, CHANGELOG. This needs a written plan (`/sc:workflow`) under the repo's hard limit.
5. `make sync-dev`, `make verify-sync`; stage only `src/`, `tests/`, `docs/`, `plugins/`, `CHANGELOG.md`.
6. After the merge, remove `T3Model04..06` from Coder (optional cleanup PR).

### Risks and migration effects

- **Launch failure from merge order:** if the JSON lands before Coder sets the `T2b*` and `T4Model02` slots, every ccsession launch in tier mode stops with "X is not set (needed by tier)" (`models.py:663-664`). Highest risk.
- **Silent change for Tier 3 users and pins:** `issue-worker-t3` and anyone selecting Tier 3 move from Terra first to GLM first, with only Grok and Qwen behind it; no Terra fallback unless Q1 adds one.
- **Members lose access** to Terra and the Muse models outside Tier 2 if `tier2b` is not added to `CCSESSION_TIER_RULES`.
- **Window skip:** a `T3_WINDOW` above 500000 makes the proxy skip Grok as a backup (`local-gateway-alias-proxy.py:720-722`); the same applies to Haiku 5.5 in Tier 4 if its window is below `T4_WINDOW`.
- **Retry ladder:** rung 0 becomes glm-5.3, in neither family, so the family alternation may stop working as designed (Q9).
- **List positions:** inserting a tier breaks the index-based tests (791-792, 2843-2859) until updated.
- **Haiku 5.5 policy:** unscored (`MODEL-TIERS.md:216`) and may contradict the placement rules (157-173).
- Older launchers ignore the tier lines (defaults.sh 63-65) and are unaffected.

### Not verified

- The Coder repo file itself was not read; B1 line numbers come from the deployed copy and may differ in the repo.
- Whether the live gateway serves `claude-haiku-5-5`, `glm-5.3`, `grok-4.7`, `Qwen3.8-max`, `gpt-6-luna` and `gpt-6.1-terra` today.
- Claude Haiku 5.5's context window and output limits; `CCSESSION_TIER_RULES` in other workspaces; how a model missing from `CCSESSION_MODEL_ORDER` is listed; how and when workspaces reload defaults.sh.
- README lines 540-545 (beyond profile names) and test lines 538-539 and 2888 were noted but not re-read; re-read before editing.

## Related Issues/PRs

- #384 — primitive selection and tier aliases; related, not a duplicate.
- #395 — precedence of a workspace default model versus a tier alias; related, not a duplicate.
- #407 — reported Tier 1b versus individual-model default behavior; related, not a duplicate.
- #462 — orchestrated session default selection and role permissions; related, not a duplicate.

<!-- sc:issue:create template=issue-feature-simple -->
