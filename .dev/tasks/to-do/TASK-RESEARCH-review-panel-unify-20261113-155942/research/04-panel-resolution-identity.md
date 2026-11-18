# Research: Panel resolution, tiers, identity and dispatch

**Investigation type:** Architecture Analyst
**Scope:** `src/superclaude/cli/review/panel.py`, `src/superclaude/cli/review/panel_cmd.py`, `src/superclaude/cli/review/data/review-panel.*.json` (8 templates), `src/superclaude/cli/review/data/review-tiers.default.json`, E2 `tools/run-reviewer.sh` at 4a22d74213f93837d00c2c314075dd967b9a98e3, `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §4.3a and §7.1, `.dev/eval-workspaces/shadow-model-combos/{PLAN,FINDINGS,results}.md`, `.dev/troubleshoot/shadow-failures-20261113014240/REPORT.md`, `git show --stat 9874d63fb`
**Status:** Complete
**Date:** 2026-11-13

---

Reading order followed: scope slices first (`research/scope/00-handoff-copy.md` §2.3, §5.3, §6; `01-other-branch-study.md` §2-4, §6; `02-review-cli-code.md` §4; `04-this-session-artifacts.md` §0.12-0.15, §2), then source. All `panel.py` line numbers below were read on 2026-11-13 at branch `ironbelly/shadow-runs` (HEAD `792cf8c52`). Effort tags: [E1] reflect Tier 2 kernel / shadow / combo experiment (this branch); [E2] tasklist review-panel study at `4a22d742`; [E3] #346 review loop on master.

## 1. `src/superclaude/cli/review/panel.py` — schema, validation and loading (:1-499)

**What the module is.** One standard-library module that owns three schemas: `PANEL_SCHEMA = "review-panel/1"`, `TIERS_SCHEMA = "review-tiers/1"`, `RESOLUTION_SCHEMA = "review-panel-resolution/1"` (`panel.py:25-27`) [E3, extended by E1]. The docstring states the design idea: a tier is an alias for an ordered model list, first model = default, the rest fallbacks; slots name a tier and a strategy, so a model change is a tier-file data edit only (`panel.py:1-9`) [E3].

**Template schema limits (all consumers).**
- Allowed top-level template keys: `schema, template_id, version, description, distinct_across_slots, apply_to, slots` (`panel.py:37-45`); any other key is an error (`:174-176`). [E3]
- Allowed slot keys: **only** `slot_id, tier, count, strategy, seed` (`panel.py:46`); any other key is "unknown key" (`:214-216`). So a template **cannot** bind a slot to a role, lens, persona, prompt or agent today. [E3; E1 kept it]
- `_STRATEGIES = ("fixed", "random", "round_robin")` (`:35`); `_KINDS = ("first", "re-review")` (`:36`) — `apply_to` must be a non-empty subset of these two (`:189-196`). There is no other review kind (no "pr", "qa", "spec", "tasklist"). [E3]
- Exactly one `fixed` slot (the anchor) per template (`:245-246`); `count` 1..4 per slot (`:229-233`); total 1..8 reviewers (`:247-248`); `seed` only with `random` (`:241-244`); slot ids `^[a-z0-9]{1,8}$` (`:31`); tier names `^tier[0-9]{1,2}[a-z]?$` (`:30`), so `tier0` is a legal tier name syntactically. [E3]
- The reflect profile is applied by `validate_panel` only when a tier file is passed and the id starts with `reflect-` (`:249-254`). `load_panel` calls `validate_panel(obj)` **without** tiers (`:451`, `:461`), so the reflect profile is not checked at load time; it is checked in `resolve` (`:588-592`, section 2). [E1]

**Reflect profile [E1].** `_REFLECT_PREFIX = "reflect-"`, `_REFLECT_LAUNCH = ("sonnet","opus","haiku")`, `_REFLECT_MAX_REVIEWERS = 3` (`panel.py:71-73`). `validate_reflect_profile` (`:80-134`):
- rejects a slot on `tier0` (`:104-105`); [E1]
- reads `aliases.get("tier0")` (`:95-96`) and rejects any slot whose tier models **or any environment's stand-ins for that tier** intersect the tier0 model set (`:107-117`). Because the packaged tier file has no `tier0` alias (section 4), `tier0_models` is always the empty set, so this rule is a no-op with packaged data; it only bites if a user tier file adds `tier0`. [E1]
- every reachable model (alias models + all environments' stand-ins) must have a `classes` entry and must not be Fable (`:118-125`; `_is_fable` = id prefix `claude-fable-` or class `fable`, `:76-77`); [E1]
- total `count` over slots at most 3 (`:126-133`); a `round_robin` slot needs a recorded `--sequence` (`:128-129`). [E1]
- `_check_reflect_resolution` (`:137-157`) re-checks after resolution: <=3 reviewers, every `model` **and every fallback** has a class and is not Fable, and `launch` is one of sonnet/opus/haiku (`:153-156`). It does **not** check duplicates. [E1]

**Tier file validation [E3, E1 added `classes` and `placeholder`].** `validate_tiers` (`:258-374`): aliases non-empty; each alias has an `alias` string and a non-empty, duplicate-free `models` list (`:295-302`), except a `placeholder: true` tier, which must have `models: []` and resolves to its environment stand-in or fails closed (`:284-294`). `classes` must map model id -> lowercase class name (`:308-316`). Each environment: `available` = `"all"` or a list; `stand_ins` keyed by defined tiers, each id in `available` when it is a list (`:340-363`); `launch` must be a dict of strings (`:364-368`) — **an empty dict is valid**; allowed env keys `available, stand_ins, launch, note` (`:371-373`). (Provenance checked with `git log -S` on 2026-11-13: `placeholder` came in `9163bd1c7` (#346 merge) [E3]; `classes`, `strict_distinct` and the reflect profile came in `d2d8a2d16` (#519) [E1]; `T3Model01` in `select_env` came in `9163bd1c7` [E3]. `d2d8a2d16` is an ancestor of `origin/master`, so the E1 resolver changes are already on the fork's master; the local `master` ref is stale and has no `cli/review/` at all.)

**Lookup precedence.** `find_path` (`:397-419`): explicit path; `SUPERCLAUDE_REVIEW_PANEL` / `SUPERCLAUDE_REVIEW_TIERS`; `<git toplevel>/.superclaude/review-<kind>.json`; `~/.superclaude/review-<kind>.json`; else packaged default. `load_panel` also accepts `@<name>` (from the argument or from `SUPERCLAUDE_REVIEW_PANEL`) -> `review-panel.<name>.json` in package data (`:430-454`). [CODE-VERIFIED; scope slice 02 §4.2 had marked the search locations and `@name` UNVERIFIED — both now verified.] [E3]

**Environment selection (D12) [E3, shared by E1].** `select_env` (`:485-494`): `--env`; else `$SUPERCLAUDE_REVIEW_ENV`; else `"gateway"` when `$T3Model01` is non-empty; else `"anthropic-only"`. Only `T3Model01` is read. Hand-off D12 [CODE-VERIFIED, lines moved from :372 to :485-494].

Key Takeaways
- The template format has no field for role, lens, persona or prompt; slot keys are closed (`panel.py:46`). Any role binding needs a schema change (an additive optional slot key or a `review-panel/2`). [E3]
- Review kinds are closed to `first` / `re-review` (`panel.py:36`). [E3]
- The reflect profile is a code-level rule set keyed on a template-id prefix, not data; its tier0 rule is inert with the packaged tier file. [E1]
- `load_panel` never applies the reflect profile; only `resolve` does. [E1][E3]
- Environment auto-selection depends on one ccsession env var (`T3Model01`) and does not check that the aliases a template needs exist on the gateway. [E3][E1]

## 2. `panel.py` — `resolve_slot` and `resolve` (:500-707)

**`resolve_slot` (`:500-556`), pure and deterministic.**
1. `hard = hard_exclude ∪ (exclude if strict_distinct)` (`:519`). [E1]
2. `candidates` = alias models present in `available` (`:520`); minus `hard` (`:524-525`). [E3]
3. If empty, fall to the environment's `stand_ins` for that tier, also minus `hard`; `stand = True` (`:526-531`). If still empty: `ExclusionExhausted` when exclusion removed something, else `NoModelAvailable` (`:532-535`). [E3]
4. `fixed` -> `candidates[0]` (`:536-537`). **`fixed` never consults `exclude`** (soft distinctness). With `strict_distinct` the already-chosen models are inside `hard`, so they are removed in step 2 for `fixed` too. [E3][E1]
5. `random` / `round_robin`: `pool = candidates - exclude` (`:539`). **If the pool is empty: with any `hard` set -> `ExclusionExhausted` (`:541-542`); otherwise `pool = candidates` (`:543`) — the silent re-admission (D11).** The condition is `if hard:` — any non-empty `hard_exclude` (for example the executor class only) also disables re-admission, even without `--strict-distinct`. [E3][E1]
6. Returns `model`, `fallback_depth` (= index in the alias list or stand-in list, `:553`), `stand_in`, and `fallbacks` = remaining candidates rotated after the pick (`:555`). Fallbacks are filtered by `hard` but **not** by `exclude` in soft mode, so a fallback list can contain models other slots already use. [E3][E1]

**`resolve` (`:565-707`).**
- Unknown env -> `ValueError` (`:583-587`). Reflect profile check for `reflect-*` ids (`:588-592`). [E3][E1]
- `launch = environment.get("launch", {})` (`:595`) and each reviewer's `launch` is `launch.get(model)` (`:679`), i.e. `None` when the env has no entry. [E3]
- Order: fixed slots first, then the rest (`:598-601`). For a `review_kind` not in `apply_to` (re-review), only fixed slots, count forced to 1 (`:603-605`, `:616`). [E3]
- Seeds: random -> `"{slot.seed or base}|{slot_id}|{i}"`, `base` = `--seed` or first 8 hex of sha256(run_id) (`:606-622`); round_robin -> `(sequence or date.today().toordinal()) + i - 1` (`:623-628`) — **without `--sequence`, a generic round_robin result changes every calendar day**; the reflect profile forbids that case (`:128-129`). [E3][E1]
- `exclude = chosen` when `distinct_across_slots` **or** `strict_distinct` (`:631-635`). [E3][E1]
- `ExclusionExhausted` on the `fixed` slot is fatal (`:647-649`); on any other slot the slot is skipped and appended to `skipped` with `slot_id` and reason (`:650-656`). `NoModelAvailable` is always fatal, with a placeholder-tier hint (`:657-664`). [E3][E1]
- Per-reviewer record (`:666-681`): `reviewer_id "<slot_id>-<i>"`, `slot_id`, `tier`, `alias`, `strategy`, `seed`, `model`, `model_name`, `fallback_depth`, `stand_in`, `fallbacks`, `launch`. **No `duplicate`/`distinct` flag, no class, no role/lens, no intended-vs-served field.** [E3][E1]
- Reflect post-check (`:682-687`). Top level (`:688-699`): `schema`, template id/version/sha256, tiers version/sha256, `environment`, `run_id`, `review_kind`, `reviewers`. `skipped_slots` and `excluded {models, classes}` only when `hard_exclude` or `strict_distinct` is used (`:700-706`). `excluded.classes` is derived back from the model ids through `classes` (`:705`). [E3][E1]

**D11 soft vs strict distinctness, compared [E3 default, E1 opt-in fix].**

| Behaviour | Default (`distinct_across_slots: true`, no flags) [E3] | `--hard-exclude-class` only [E1] | `--strict-distinct` [E1] |
|---|---|---|---|
| `fixed` slot sees already-chosen models | no (`:536-537`) | no | yes, filtered (`:519`, `:525`) |
| Random pool exhausted by `exclude` | re-admit all candidates silently (`:543`) | `ExclusionExhausted` -> slot skipped (`:541-542`, `:650-656`) | `ExclusionExhausted` -> slot skipped |
| Fallback list excludes models other slots chose | no (`:555`) | no | yes |
| Duplicate visible in output | no flag; only by comparing `model` values | `skipped_slots` lists what was dropped (`:702`) | `skipped_slots` |
| Fixed anchor exhausted | n/a (fixed never exhausts by `exclude`) | fatal (`:648-649`) | fatal |

Key Takeaways
- D11 [CODE-VERIFIED, lines moved: hand-off cited `:402-408`; now `:536-543` and output `:666-699`]: soft mode can silently repeat a model; the only trace is two identical `model` values. [E3]
- E1's fix is opt-in and changes panel size: strict mode drops slots rather than repeating models, and records the drop in `skipped_slots`. A consumer that wants "two runs of the same model" (E2's best panels) cannot express it intentionally; today it happens only as an accident of exhaustion. [E1][E2]
- Any `--hard-exclude-class` silently switches off re-admission too (`:541` checks `hard`, not `strict_distinct`). [E1]
- The resolution record carries no class, no role, no intended-vs-served pair and no duplicate flag; identity fields must be added if one resolver serves all consumers. [E3][E1]
- `launch` can be `None` (no env entry), which `_check_reflect_resolution` rejects for `reflect-*` templates (section 4). [E1]

## 3. `panel_cmd.py` (129 lines) — the CLI surface

- `superclaude review panel resolve` (`panel_cmd.py:18-108`): options `--template` (file or `@NAME`, `:19-25`), `--tiers` (`:26-32`), `--env` (`:33-38`), `--run-id` required (`:39`), `--kind` `click.Choice(["first","re-review"])` default `first` (`:40-46`), `--seed` (`:47-49`), `--sequence` (`:50-52`), `--hard-exclude-class` repeatable (`:53-58`), `--strict-distinct` flag (`:59-63`). [E3 base; `--hard-exclude-class`/`--strict-distinct` E1]
- Flow: `load_panel` -> `load_tiers` -> `validate_panel(panel, tiers, sequence=...)` (this is where the reflect profile first runs with tiers, `:77-81`) -> expand each class name case-insensitively through `classes` into model ids, unknown class -> `UsageError` listing known classes (`:82-92`) -> `resolve(..., select_env(env), ...)` (`:93-103`) -> print JSON with `sort_keys=True` to stdout (`:108`). Errors become `ClickException` (`:104-107`). [E3][E1]
- **It writes no file and no telemetry**; the caller redirects stdout. [CODE-VERIFIED; agrees with hand-off D15 "panel resolve writes no telemetry".] [E3]
- `panel validate PATH --kind panel|tiers` (`:111-129`) calls `validate_panel(obj)` **without tiers** (`:124`), so `panel validate` on a `reflect-*` template never runs the reflect profile; only `resolve` does. [E3][E1]
- There is no class-level option other than exclusion: no `--include-class`, no `--allow-repeat`, no role option, no dispatch-adapter option. [E3][E1]

Key Takeaways
- The resolver is a pure stdout tool. Persisting `panel/resolution.json` is the caller's job (reflect skill), so "what the panel record says" is whatever the orchestrator wrote. [E3][E1]
- `panel validate` and `panel resolve` disagree for `reflect-*` templates: validate can say "valid" for a template that resolve rejects. [E3][E1]
- `--kind` has two values; nothing in the CLI expresses PR review, rf-qa, spec review or tasklist review. [E3]

## 4. Packaged data: `review-tiers.default.json` (38 lines) and 8 `review-panel.*.json` templates

**Tier file** (`review-tiers.default.json`, read 2026-11-13):
- Aliases (`:4-11`): tier1a `claude-gw-tier1a[1m]` = opus, sonnet; tier1b `claude-gw-tier1b[1m]` = sonnet, gpt-6.1-sol, muse-wonder-full-1.0; tier2 `claude-gw-tier2[1m]` = gpt-6.1-sol, glm-5.3, grok-4.7, Qwen3.8-max, muse-wonder-1.0, muse-spark-1.3; tier2b `claude-gw-tier2b[1m]` = gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0; tier3 `claude-gw-tier3[1m]` = glm-5.3, Qwen3.8-max; tier4 `claude-gw-tier4[1m]` = gpt-6-luna, claude-haiku-5-5, grok-4.7. [CODE-VERIFIED; matches hand-off §5.3.] **No `tier0` alias** and no `placeholder` tier. [E3]
- `names` (`:12-17`) and `classes` (`:18-23`): opus/sonnet/haiku/fable for Anthropic ids; `gpt` for sol, terra, luna; `muse` for the three muse ids; `glm`, `grok`, `qwen`. **`muse-ember-1.0` appears in neither aliases, names nor classes** — the model E2 picked for its default (section 6) cannot be named by any packaged tier and would fail the reflect profile's class rule. [E1][E2]
- `environments.gateway` (`:25-30`): `available: "all"`, `stand_ins: {}`, **`launch: {}`**, note "dispatch mechanism per model not defined yet" (`:26`). [E3]
- `environments.anthropic-only` (`:31-36`): available opus, sonnet, haiku, fable; stand-ins tier2/2b/3/4 = haiku (`:34`); `launch` id -> opus/sonnet/haiku/fable (`:35`); note dated "owner decision 2026-11-10" (`:32`). [E3]

**Templates** (schema `review-panel/1`, version 1.0.0, all `distinct_across_slots: true`, all `apply_to: ["first"]`):

| Template | Effort | Slots | Description claim | Resolved 2026-11-13, `--run-id run1`, packaged tiers |
|---|---|---|---|---|
| `default` | [E3] | t1b tier1b x1 fixed; t2 tier2 x1 random; t3 tier3 x2 random (`review-panel.default.json:9-11`) | "Production review panel" (`:5`) | gateway: sonnet, muse-spark-1.3, glm-5.3, Qwen3.8-max (all `launch: null`); anthropic-only: sonnet + 3x haiku (stand-ins) |
| `live7` | [E3] | t1b x1 fixed; t2 x1; t2b x1; t3 x2; t4 x2 random (`review-panel.live7.json:9-13`) | anthropic-only = 1 Sonnet + 6 Haiku; gateway needs `claude-gw-tier2b` (`:5`) | gateway: sonnet, muse-spark-1.3, **Qwen3.8-max (t2b-1)**, glm-5.3, **Qwen3.8-max (t3-2)**, haiku, luna — D11 duplicate reproduced exactly as the hand-off states [CODE-VERIFIED by run]; anthropic-only: sonnet + 6x haiku [CODE-VERIFIED by run] |
| `reflect-pre` | [E1] | t1b fixed; t4 random; t1a random (`review-panel.reflect-pre.json:9-11`) | "sonnet, haiku, opus under strict distinctness"; personas by order analyzer, qa, refactorer (`:5`) | anthropic-only soft and strict: sonnet, haiku, opus [CODE-VERIFIED]; gateway: **error** (section 4.1) |
| `reflect-pre-x2` | [E1] | t4 fixed; t1a random (`review-panel.reflect-pre-x2.json:9-10`) | anchor replacement when tier1b exhausted by executor sonnet (`:5`) | anthropic-only `--hard-exclude-class sonnet --strict-distinct`: haiku, opus, `excluded.classes ["sonnet"]` [CODE-VERIFIED] |
| `reflect-post` | [E1] | same as reflect-pre (`:9-11`) | mirrors reflect-pre | same as reflect-pre (not separately run) |
| `reflect-post-x2` | [E1] | same as reflect-pre-x2 (`:9-10`) | mirrors reflect-pre-x2 | not run |
| `reflect-enterprise` | [E1] | same as reflect-pre (`:9-11`) | third persona architect (`:5`) | not run |
| `reflect-lite` | [E1] | t1b fixed; t4 random; t2 random (`review-panel.reflect-lite.json:9-11`) | soft = sonnet, haiku, haiku; strict = sonnet, haiku (`:5`) | soft: sonnet, haiku, haiku (t2-1 `stand_in: true`) — **a silent duplicate inside a reflect template**; strict: sonnet, haiku, `skipped_slots [t2]` [CODE-VERIFIED by run] |

Personas/lenses live only in template `description` prose; the code has no persona field (`panel.py:46`). [E1]

### 4.1 Gateway environment `launch: {}` vs anthropic-only (question 4)

- `resolve` sets each reviewer's `launch = launch.get(model)` (`panel.py:595`, `:679`); the gateway's `launch` is `{}` (`review-tiers.default.json:29`), so every gateway reviewer has `launch: null`. [E3][E1]
- For `reflect-*` templates `_check_reflect_resolution` requires `launch` in sonnet/opus/haiku (`panel.py:153-156`). Result, run 2026-11-13: `superclaude review panel resolve --template @reflect-pre --env gateway --run-id run1` -> `Error: invalid reflect resolution: t1b-1: launch None is not one of sonnet, opus, haiku; t4-1: ...; t1a-1: ...`; same for `@reflect-lite`. **No reflect template can resolve in the gateway environment.** [E1] [CODE-VERIFIED by run]
- In this session `select_env` would pick `gateway` (env has `T3Model01=glm-5.3`, observed 2026-11-13), so reflect must pass `--env anthropic-only` explicitly; generic templates in gateway resolve but carry `launch: null`, i.e. no dispatch instruction at all. [E1]
- In anthropic-only, every tier has at most one available model, so every `fallbacks` list is `[]` (observed in all anthropic-only runs above). The fallback ladder exists only in gateway, where the reflect profile cannot run. [E3][E1]
- `launch` in anthropic-only is a **class name** (`sonnet`/`haiku`/`opus`), which is what the reflect skill passes to the Agent tool. What that class actually serves is decided outside the resolver, by `ANTHROPIC_DEFAULT_{SONNET,HAIKU,OPUS}_MODEL`. Observed in this session's environment on 2026-11-13: `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b[1m]`, `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a[1m]`, `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]`, `T2bModel01=gpt-6.1-terra`, `T3Model01=glm-5.3`. The haiku class therefore routes to the **tier2** gateway alias, whose first model is `gpt-6.1-sol` (`review-tiers.default.json:7`) — the mechanism behind "haiku slot served by gpt-6.1-sol" (section 7). The name `anthropic-only` is therefore not true at serving time on this machine. [E1]

### 4.2 D12 `T3Model01` / `T2bModel01` (question 2)

- `T2bModel01` is set in this session's environment (value `gpt-6.1-terra`, 2026-11-13) but `select_env` reads only `T3Model01` (`panel.py:492`) [CODE-VERIFIED]. Nothing in the resolver checks that the gateway serves the aliases a template references (e.g. `live7` needs `claude-gw-tier2b`, `review-panel.live7.json:5`). [E3]
- The resolver also never checks that the alias's **first model** is what the gateway alias serves. E2 recorded that aliases serve only the first model of a tier and so used raw ids (scope 01 H31, `manifest.md:11` [UNVERIFIED in this file; cited from scope slice]). [E2][E3]

### 4.3 Tier classes and the reflect rules (question 3)

- Classes exist for every alias model (`review-tiers.default.json:18-23`), so the reflect "every reachable model has a class" rule passes; `claude-fable-5-1` is in `available`/`launch` for anthropic-only (`:33`, `:35`) but no tier lists it and no stand-in names it, so the "no Fable" rule never triggers with packaged data. [E1]
- "No tier0" rule (`panel.py:104-105`, `:95-117`) is inert: no `tier0` alias in the file, and `--hard-exclude-class tier0` is rejected as an unknown class (run 2026-11-13: `unknown class 'tier0' ... (known classes: fable, glm, gpt, grok, haiku, muse, opus, qwen, sonnet)`). Tier 0 is a concept in the reflect profile without data behind it. Whether `tier0` was meant to name the orchestrator/executor tier is [UNVERIFIED] (no code defines it). [E1]
- Max 3 reviewers is code (`panel.py:73`), which blocks any reflect template from expressing E2's 3-model panels plus an anchor, or `live7`. [E1][E2]

Key Takeaways
- Gateway + reflect = hard error; anthropic-only + reflect = no fallbacks and a class label that the session env re-routes to non-Anthropic models. Neither environment describes what actually serves a reflect reviewer. [E1]
- `live7` gateway D11 duplicate (Qwen3.8-max twice) reproduced 2026-11-13; `reflect-lite` soft duplicates haiku and is documented as doing so. [E3][E1]
- Strict mode on `live7` anthropic-only collapses 7 reviewers to 2 (sonnet, haiku) with 5 `skipped_slots` entries; the `skipped_slots` list repeats `slot_id` without the instance index (`t3` twice, `t4` twice). [E1][E3]
- Strict mode does not keep fallbacks distinct after the fact: `live7` gateway strict gave `t2-1` fallbacks containing `glm-5.3` and `Qwen3.8-max`, which later slots chose, so a runtime fallback could still create a duplicate (run 2026-11-13). [E1]
- `--hard-exclude-class` without `--strict-distinct` also skips instead of re-admitting (`reflect-lite --hard-exclude-class opus` -> t2 skipped, run 2026-11-13). [E1]
- `muse-ember-1.0` (E2's default panel member) is not in the tier file at all. [E2][E3]

## 5. E2 runner `tools/run-reviewer.sh` (87 lines, `git show 4a22d742:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`) [E2]

Read 2026-11-13 via `git show` only.

**Dispatch.** One reviewer = one fresh `claude -p` subprocess on a **raw gateway model id**: `timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit` run in `/tmp/evalsb/repo` (`run-reviewer.sh:48`). The model is a positional argument (`:2`, `:5`); there is no tier, alias, class or panel template in the runner. Bash stays allowed under bypass permissions (`:48`). [E2]

**Inputs.** Candidate copied into a sandbox path (`:7-8`); `source.md` copied next to it from a hard-coded path in another worktree (`:10-11`); the brief invokes `/sc:spec-panel @<cand> --mode critique` and names only the candidate and its sha256 (`:13-17`) — it never names `source.md` (D8, see scope 01 H18). [E2]

**Observed identity.** `OBS` = the unique, comma-joined set of `message.model` values of **top-level** assistant events (`select(.type=="assistant" and (.parent_tool_use_id==null))`, `:51`). `MODEL_OK` is true only if `OBS` is non-empty, not `<synthetic>`, and equals the requested id case-insensitively or the requested id plus `-build` (`:55-56`). A run that served two models gives `OBS="a,b"` and fails. Tokens: `output_tokens_main` from the result event, `output_tokens_all` summed over `modelUsage` (`:52-53`), which includes auxiliary calls (scope 01 §2.2: 57 runs had a `claude-gw-tier2[1m]` `web_fetch_apply` call). Block check: a line starting ```` ```findings-v1 ```` (`:57`). API errors: grep `API Error` in the result (`:54`). Per-attempt `meta.json` (`:58`). Two attempts per model (`:61-64`). [E2]

**Fallback ladder.** Bash associative array keyed by model (`:23-43`), with owner orders dated in comments ("2026-11-12", "2026-11-12 18:10 UTC", `:19`, `:24`): next model in the same tier, then the next tier's head; includes `muse-ember-1.0` as "Tier 04 Model 02" (`:26`, `:33-34`), which the packaged tier file does not have (section 4). Guards added 2026-11-12 after a cyclic-ladder incident: `EXCLUDE_MODELS` default `"glm-5.3 Qwen3.8-max"` (`:69`), never revisit (`VISITED`, `:70-71`, `:74`), `NOFALLBACK` disables the ladder (`:66`). [E2]

**The `expected_model` overwrite (question 6).** On fallback `MODEL="$NEXT"` (`:76`), and `run_attempt` then writes `expected_model: $MODEL` (`:58`). So the final `meta.json` (`:85`) records the **fallback** model as expected, and `model_ok` is judged against it. The originally requested model survives only in `$RID.fallback.log` (`:75`) and in the ladder variable `MODEL_LADDER` (`:44`, `:76`), which is **never written to any file**. [CODE-VERIFIED; matches scope 01 §2.2.] [E2]

**Additional runner defects found in this read.**
- Attempt files are named `$RID.attempt1/2.*` and `attempt` resets to 0 for each ladder model (`:76`), so a fallback model's attempts **overwrite** the primary model's transcripts and meta files. `cost.json` sums `$RID.attempt*.meta.json` (`:87`), i.e. only whatever attempt files survive (the last model's, plus a stale `attempt2` of an earlier model if the last model succeeded on attempt 1). Cost across a ladder is therefore wrong in either direction. (Relates to scope 01's "stale attempt files make highest attemptN wrong for 5 runs".) [E2]
- The ladder loop condition is `! ($MODEL_OK && $BLOCK_OK)` (`:73`) while the entry condition also includes `$APIERR` (`:66`); a run with a valid model, a findings block **and** an `API Error` string enters the branch but never falls back. [E2]

Key Takeaways
- E2's identity is a **hard, observed** check against the raw model id, taken from the JSON transcript of a subprocess the runner owns. It needs `claude -p --output-format json` (or stream-json) access; an in-session Agent-tool dispatch does not give the parent this transcript directly. [E2][E1]
- E2 deliberately bypassed `panel resolve`: no tiers, no aliases, no distinctness logic; panel composition was chosen per row by hand (scope 00 §5.3). [E2][E3]
- Intended model, ladder hops and served model must be three separate recorded fields; E2's runner collapses intended into served on fallback. [E2]
- The runner's model knowledge (ladder order, `muse-ember-1.0`, exclude list) is dated 2026-11-12 and lives in bash, not in the tier file. [E2]

## 6. Reflect skill: §4.3a shadow steps, §7.1 rotation, §3.4/Wave 0 aliases, §9.2 telemetry [E1]

Read 2026-11-13: `src/superclaude/skills/sc-reflect-protocol/SKILL.md:123-131`, `:232-237`, `:309-349`, `:644-660`, `:940-989`. Doc-sourced claims are tagged against code.

**Two parallel selection mechanisms exist in reflect.**
1. **Legacy rotation (authoritative today).** §7.1 table (`SKILL.md:652-656`): N=2 -> sonnet, haiku (analyzer, qa); N=3 default -> sonnet, haiku, (qwen | kimi | deepseek if alias available; else opus) (analyzer, qa, refactorer); `--strategy enterprise` -> sonnet, haiku, opus (analyzer, qa, architect). These are **class names**, not model ids. All reviewers are the fixed `reflect-reviewer` agent type with the persona in the brief (`:646`). Executor-class exclusion removes the executor's class and may add the next available class or degrade to N=2; N=2 is a hard floor (`:648`, `:658`); unknown executor is fail-open with `executor_class_resolved: false` (`:650`). The served model per class comes from `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` (`:125-129`); Wave 0 step 0.5 counts **distinct models the three aliases name** to set the reviewer count (`:232`). [E1]
   - "qwen | kimi | deepseek if alias available" (`:655`): there is no alias variable for these classes in §3.4 (`:127` lists only OPUS/SONNET/HAIKU), and the packaged tier file has no `kimi` or `deepseek` class (`review-tiers.default.json:18-23`). How a reviewer would be launched on qwen/kimi/deepseek through the Agent tool is not defined. [UNVERIFIED — no code found] [E1]
   - `reflect-reviewer` frontmatter `model: sonnet` (`src/superclaude/agents/reflect-reviewer.md:6`); same for `confidence-calibrator.md:6` and `evidence-validator.md:6` [CODE-VERIFIED]. This is the default when the orchestrator passes no `model` to the Agent call (dispatch collapse, section 7). [E1]
2. **Panel resolution (shadow, measurement only).** §4.3a step 1 (`:340`): `superclaude review panel resolve --template @reflect-pre --run-id <id> --kind first --env anthropic-only --hard-exclude-class <executor class> --strict-distinct`; unknown executor -> omit the exclusion; anchor `ExclusionExhausted` -> re-resolve once with `@reflect-pre-x2` and `anchor_replaced: true`; a second exhaustion or a null `launch` -> rules D3/D4. The stdout is written verbatim to `<output>/panel/resolution.json` and never rewritten. Rule D4 (`:320`): "Unsupported cells (gateway, a null `launch`, an unmapped model) run the legacy rotation and record `panel_fallback_reason`" — **[CODE-VERIFIED]** consistent with the resolver's gateway error (section 4.1). Rule D5 (`:321`): `N_eff = min(--reviewers, alias count, 3)` — **the resolver has no reviewer-count option** (`panel_cmd.py:18-63`), which step 1 itself admits (`:340`) [CODE-VERIFIED]. Step 3: "Dispatch is the legacy dispatch" (`:342`) — **the resolution never drives dispatch**. [E1]

**Parity and the card `model:` header (E1 fix `9874d63fb`).** Step 2 (`:341`) compares the ordered `(persona, model class)` pairs of `panel/resolution.json` with the legacy rotation and records `panel_parity`; card header `model:` is copied verbatim from `reviewers[N].model` "never from the model the harness reports"; a differing harness model goes on an extra `model_observed:` line. `git show 9874d63fb` (2026-11-13 01:54 UTC; 4 files: `SKILL.md` +5/-5, `refs/reviewer-spec.md` 1 line, two tests) shows the pre-fix text said only "`model:` (the resolved model id, written by the orchestrator)". The aggregator `scripts/reflect_shadow_exit.py:117-177` `recompute_parity` [CODE-VERIFIED]: requires `panel/resolution.json` reviewers; refuses if the run's `tiers_sha256` differs from the current tier file (`:128-132`); maps resolved model ids to classes via `classes` (`:134-137`); requires card header `model == resolution model` **as a string** (`:148-152`); compares `resolution == cards == legacy` class lists (`:175`). It never reads `model_observed`. [E1]

**Identity fields (§4.3a step 9, §9.2).** Step 9 (`:348`): `identity_source: observed` when "the adapter read the reviewer's resolved model id from its transcript", else `requested-pinned` ("an unverified assumption"); compare each card's `reviewer_model_self_report` with the pin; mismatch -> `identity_mismatch_suspected: true`; no claim of verified independence while `requested-pinned` or executor unknown. §9.2 telemetry (`:969-988`) lists `identity_source`, `identity_mismatch_suspected`, `judge_identity`, `judge_class_collision`, `panel_parity`, `anchor_replaced`, `reviewers_requested/resolved/complete`, `panel_shortfall_2_of_3`, `findings_block_compliance_rate`, but **no `model_observed` or served-model field**, and top-level `reviewer_models`/`reviewer_vendors` (`:945-947`) are the legacy rotation. Grep 2026-11-13 over `scripts/*.py`, `src/superclaude/cli/**/*.py` and the reflect skill: `model_observed` occurs only in `SKILL.md:341` and in E3's `telemetry.py`; `reviewer_model_self_report` only in `SKILL.md:348`, `:975` and `refs/reviewer-spec.md:39`. No code computes `identity_source` or reads a transcript. [CODE-CONTRADICTED for any reading that the shadow pipeline observes identity: it is prose-only; the "adapter" in step 9 has no code.] [E1]

**E3 already designed a three-way identity record.** `src/superclaude/cli/review/telemetry.py:30-81` `REVIEWER_GROUPS` has a `model` group `("resolved", "launch", "observed")` (`:49`) plus `slot` group (`slot_id, tier, alias, strategy, seed, fallback_depth, stand_in`, `:40-48`) and `cost` group (`tokens_in/out`, cache, `wall_s`, `:74-80`); `_flatten_reviewer` stores them as `<group>_<key>` columns (`:313-319`), and the SQLite `model_scores` view groups by `model_observed`, `slot_tier`, `slot_stand_in`, `stratum` (`:364-378`) [E3] [CODE-VERIFIED]. Its `STRATA = ("sonnet","haiku")` (`:112-115`) and the check at `:267-268` still restrict strata (hand-off D15 [CODE-VERIFIED]). Neither E1 nor E2 writes this record (scope 00 D15; SKILL.md §4.3a has no `review telemetry` call).

Key Takeaways
- Reflect selects reviewers by class rotation in prose; the panel resolver is a parallel, non-dispatching record. Unifying them means the resolver must become the dispatch source, or the record will keep describing something that did not run. [E1]
- The `9874d63fb` fix makes card `model:` equal to the pin by instruction, so `recompute_parity` can pass while the served model is entirely different; `model_observed` is optional prose that nothing reads. [E1]
- `identity_source: observed` has no implementation; every current reflect record is effectively `requested-pinned` (or unrecorded). [E1]
- E3's telemetry schema already separates `resolved` / `launch` / `observed` and keys model scores on `observed`; it is the natural home for the identity triple, after widening `STRATA`. [E3]
- The §7.1 "qwen | kimi | deepseek" branch names classes that have neither an env alias nor a tier-file class. [E1]

## 7. Observed identity vs pinned identity, and dispatch collapse (question 6)

Sources read 2026-11-13: `.dev/eval-workspaces/shadow-model-combos/PLAN.md` (`:1-150`), `FINDINGS.md` (42 lines), `results.md` (47 lines), `analysis/extract.py:42-79`, `.dev/troubleshoot/shadow-failures-20261113014240/REPORT.md` (45 lines), `scripts/reflect_shadow_exit.py:117-177`, E2 `run-reviewer.sh`.

### 7.1 Two ways to observe the served model, both offline transcript parsing

| | E2 runner [E2] | E1 combo extractor [E1] |
|---|---|---|
| Dispatch | one `claude -p --model <raw id> --output-format json` per reviewer (`run-reviewer.sh:48`) | one `claude -p "/sc:reflect ..." --model <orchestrator> --output-format stream-json --verbose --forward-subagent-text` per **whole reflect run**; reviewers are in-session Agent calls (`PLAN.md:143-148`) |
| Requested model | positional raw id (`run-reviewer.sh:5`) | the Agent call's `input.model` (a class or `None`) (`extract.py:60-62`) |
| Served model | unique top-level `message.model` where `parent_tool_use_id == null` (`run-reviewer.sh:51`) | most common `message.model` among events whose `parent_tool_use_id` is that Agent call's id (`extract.py:56-58`, `:69`) |
| When checked | per run, immediately, hard gate (`model_ok`, `:56`, `:59`) with retry and ladder | after the experiment, descriptive only (`extract.py:3` "Read-only on the runs") |
| Recorded where | `meta.json` `expected_model`/`observed_model`/`model_ok` (`:58`) | `results.md` "Requested class -> served model" (`results.md:31-47`); not in any run artifact |

Both read the same Claude Code JSON event fields; they differ in which side of `parent_tool_use_id` they read. Neither is product code. The reflect skill's "adapter" that would set `identity_source: observed` (`SKILL.md:348`) does not exist (section 6). Whether `--forward-subagent-text` is required for sub-agent `message.model` to appear in the parent stream is [UNVERIFIED] (PLAN uses it; no test without it was read). [E1][E2]

### 7.2 What the E1 record shows vs what served (combo experiment, runs dated 2026-11-13)

- All 15 runs resolved identically (`panel/resolution.json` sonnet-5-5 / haiku-5-5 / opus-5-5, launch sonnet/haiku/opus, tiers sha `a35908fa6d40`, template sha `d8156ae38041`), because step 1 passes `--env anthropic-only` and the combos changed only env aliases (`PLAN.md:54-58`, `:83-89`). [E1]
- **"haiku" slot served by `gpt-6.1-sol`:** A1-A2 and B1-B3 reviewers `('haiku','gpt-6.1-sol')` (`results.md:33-38`); FINDINGS `:15`: "The panel record (`panel/resolution.json`, card headers, `panel_parity`) never shows this; only the transcripts do." Mechanism: `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]` (`PLAN.md:85-86`), and tier2's first model is `gpt-6.1-sol` (`review-tiers.default.json:7`) [CODE-VERIFIED for the tier list; gateway routing itself is runtime behaviour observed 2026-11-13]. [E1]
- **Dispatch collapse:** A3 reviewers and calibrators all `(None, 'claude-sonnet-5-5')` (`results.md:35`): the orchestrator passed no `model`, so `reflect-reviewer.md:6` `model: sonnet` applied; FINDINGS `:9`. Pilot evidence (earlier shadow runs, dates in `PLAN.md:61-69`, 2026-11-11 probe): 6 of 9 tier3-orchestrated runs collapsed to the SONNET alias; both tier1b-orchestrated runs did not; "orchestrator drives dispatch" is a hypothesis, n tiny (`PLAN.md:66-69`). Calibrators also run with `None` class in B3, C1, C2, E1, E2 (`results.md:38-40`, `:45-46`). [E1]
- **Parity cannot see served models:** E1-E3 served haiku / luna / luna (2 distinct models, `results.md:17-19`, `:45-47`) yet parity was `True` in all three (`results.md:17-19`); D served luna in the "opus" slot with parity `True` (`results.md:14-16`); A3 (collapsed to one model) had parity `False` but FINDINGS attributes A's parity failures "mostly [to] alias text in the contract and one card header missing fields" (`FINDINGS.md:38`), not to the collapse. So `panel_parity` measures record consistency, not served identity. [E1]
- **Study's best panel in E1 terms:** E = "the study's best panel; 3 reviewers, 2 distinct models" (`FINDINGS.md:13`) — achieved by setting two class aliases to the same model (`PLAN.md:89`), i.e. outside the resolver and against the class-distinctness idea of §7.1. PLAN flagged the risk that step 0.5 would count the two luna aliases as one model and run 2 reviewers (`PLAN.md:106`); the runs show 3 reviewers complete (`FINDINGS.md:3`), so that risk did not materialise in these 3 runs (2026-11-13). [E1][E2]

### 7.3 The `9874d63fb` fix and the harness-reported model

- TS report (`REPORT.md:14`): in shadow runs 04/05 the card `model:` carried **what the harness reported — the gateway alias** (`claude-gw-tier1b[1m]`, `claude-gw-tier2[1m]`, `claude-gw-tier1a[1m]`), while runs 03/06/07 copied the pin; `reflect_shadow_exit.py:148` compares strings, so alias text failed parity "even when the class is right". Fix 1 (`REPORT.md:19`) -> commit `9874d63fb` (section 6): copy the pin into `model:`, put the harness model on `model_observed:`. [CODE-VERIFIED: the commit changes `SKILL.md:341` as proposed.] [E1]
- Consequence: what "the harness reports" to the orchestrator is an **alias**, not a served model id, so the `model_observed:` line will usually hold an alias string, which cannot reveal a Sol-for-Haiku swap. The only served-model evidence in E1 remains the sub-agent stream events (`extract.py:56-58`). [E1]
- E2's equivalent flaw: the `expected_model` overwrite (`run-reviewer.sh:58`, `:76`) — on fallback the record says expected = served = fallback model, so `model_ok` passes; only `fallback.log` shows the swap (section 5). Both efforts therefore have a path where the stored "intended" field is rewritten to agree with something else (E1: card `model:` := pin by instruction; E2: `expected_model` := ladder model by code). [E1][E2]

Key Takeaways
- Observed identity is only obtainable from Claude Code JSON events: top-level events for a `claude -p` reviewer (E2) or sub-agent events in the parent's stream-json (E1, offline). An in-session orchestrator following a skill has no tool that returns the served model of an Agent call; this is the real limit for reflect-style dispatch. [E1][E2]
- The unified record needs four separate fields per reviewer: `requested` (resolver pin), `launch` (what was passed: class, alias or raw id), `served` (observed from events, or `unknown`), and `identity_source`; plus a `fallback_chain`. E3's telemetry already has `resolved` / `launch` / `observed` (section 6). [E1][E2][E3]
- Dispatch must pass `model` on every Agent call (or the resolver's `launch` must be enforced by the dispatcher); otherwise the agent frontmatter default silently replaces the panel. [E1]
- `panel_parity` should be redefined (or retired) — it compares two records with each other, not a record with reality. [E1]

## 8. E2's best panels vs strict distinctness (question 5) — evidence dated, valid era 2026-11-12 13:02 to 2026-11-13, one gateway

Read 2026-11-13 directly from `git show 4a22d742:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/COMBO-REPORT.md` (CR) lines 289-300, 362-384, 421-430.

- Valid era: source.md first shipped 2026-11-12 12:59:34, first valid-era run 13:02:27 (CR:373). Final section dated 2026-11-13 and supersedes earlier tables (CR:289). [E2]
- Final guidance after batch 11 (CR:428): **default = ember + 2x luna** (replicated, cheapest, "same measured quality"); optional quality tier = sonnet + 2x luna; **haiku + 2x luna** "remains the best measured real-blocking panel (1.2/8)". Earlier decision lines: cost champion ember + luna (CR:365); recommended default ember + 2x luna, 64k tokens, ~6 min, "control 0.83 (the only doubling effect that survives testing)" (CR:366); high-assurance haiku + 2x luna, 191k tokens, 1.2/8 real blocking (CR:367); "any panel of 5 reviewers (no gain for 2-4x the cost)" in do-not-use (CR:369). The interim "sonnet + 2x luna is standard" (CR:383) was rejected by batch 11 (CR:421, CR:428). [E2]
- Surviving statistics (CR:298): "second luna raises control found +0.83 (p 0.004 Welch, 0.048 permutation, baseline all zeros)"; 2x luna + 2x ember more wrong blockers; ember + terra worse. CR:297 lists "second run of the same model adds nothing" among **retracted** stale text. [E2]
- Mixed vendors: every recommended panel mixes vendors (muse/ember, gpt/luna, anthropic/haiku or sonnet). The study's single-reviewer finding: sonnet alone 2/16 at 93k tokens (scope 00 §2.3, PR; [UNVERIFIED in this file]). [E2]
- Ceiling: "model choice cannot lift the ceiling past ~2.5/14"; the biggest levers are the anchor limit and naming source.md (CR:371, CR:428). [E2]

**Compatibility with the resolver (2026-11-13 code):**

| E2 panel [E2] | Expressible with packaged tiers? [E3] | Under `--strict-distinct`? [E1] | Under the reflect profile? [E1] |
|---|---|---|---|
| ember + 2x luna | No: `muse-ember-1.0` not in any alias or class (`review-tiers.default.json:4-23`) | No: second luna is a repeat -> slot skipped | No: ember has no class (`panel.py:124-125`) |
| haiku + 2x luna | Only by accident: tier4 = luna, haiku, grok (`:10`), so 3x tier4 random could land on it; no way to request "luna twice" | No: second luna skipped | 3 reviewers OK, but only in gateway, which fails on `launch: null` (section 4.1); in anthropic-only luna is unavailable (`:33`) |
| sonnet + 2x luna | No intentional form | No | Same as above |
| two runs of the same cheap model | Only via soft re-admission when a pool is exhausted (`panel.py:543`), unflagged | Never | Never (reflect uses strict) |

Key Takeaways
- E2's one statistically surviving doubling effect (second luna, CR:298) is a **deliberate repeat**, which the resolver cannot express (no repeat/replica concept) and which `--strict-distinct` forbids. Soft mode can produce repeats only as an unflagged accident. [E2][E1]
- E1's distinctness goal is class diversity for anti-self-confirmation (`SKILL.md:646-648`); E2's evidence is about catch per token on tasklist plans. They are different goals, so one resolver needs distinctness as a **policy per consumer**, not a single global default: e.g. `distinct: none | model | class` plus an explicit `replicas` count per slot that is recorded as intended. [E1][E2]
- The packaged tier lists contradict E2's dated evidence (Qwen and glm as tier3's only models, terra/sol first in tier2/tier2b; ember absent) (scope 00 §5.3; tier file `:7-10`). Any tier data taken from E2 must carry the 2026-11-12/13 date and the gateway it came from. [E2][E3]
- Reflect's max-3 rule (`panel.py:73`) fits all E2 recommended panels (2-3 reviewers); the blocker is model availability and distinctness, not count. [E1][E2]

## 9. Roles, lenses and review kinds (question 7)

**Where role/lens/kind live today (read 2026-11-13).**
- Panel template: no role, persona, lens, prompt or agent field; slot keys closed to `slot_id, tier, count, strategy, seed` (`panel.py:46`, `:214-216`). Reflect personas are positional ("persona by resolution order: analyzer, qa, refactorer", `SKILL.md:341`; template descriptions `review-panel.reflect-pre.json:5`, `reflect-enterprise.json:5`) and hard-coded in the exit script as `PERSONAS[i]` (`reflect_shadow_exit.py:135`). [E1]
- Review kind: `_KINDS = ("first", "re-review")` (`panel.py:36`), CLI `click.Choice(["first","re-review"])` (`panel_cmd.py:43`); a kind not in `apply_to` resolves only the fixed anchor (`panel.py:600-605`). All 8 packaged templates have `apply_to: ["first"]`, so `--kind re-review` always yields the single anchor. [E3]
- E3's loop prompt **does call the resolver**: `src/superclaude/rules/prompts/document_review_loop_prompts.md:70` says to run each review with the reviewers that `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>` prints ("a panel for a first review, one reviewer for a re-review by default"), then `review merge` and `review ledger revise`. [E3] [CODE-VERIFIED as text; this is a prompt, not code.] This corrects scope 02 D14's "no skill or command calls `review panel resolve`" — the grep there covered skills/commands/core, not `rules/prompts/`.
- Lens is a **finding-contract** concept, not a panel concept: `findings_v2.py:36` `LENSES = ("spec", "reflect-pre", "reflect-post")`, enforced per line/block (`findings_v2.py:140-149`; `reflect-post` requires `deviation_class`); clustering picks primary citation roles per lens (`cluster.py:67-71`: reflect-pre -> plan; reflect-post -> source, diff; spec -> spec). Citation roles `ROLES = ("plan","spec","source","test","diff","artifact")` (`findings_v2.py:35`). [E1]
- Agent type: reflect fixes all reviewers to `reflect-reviewer` (`SKILL.md:646`); E2 uses a `claude -p` session with `/sc:spec-panel --mode critique` (`run-reviewer.sh:13`); E3's loop uses "a fresh context with the same brief" (`document_review_loop_prompts.md:70`). The resolver knows none of this. [E1][E2][E3]

**What PR review and rf-qa replacement would need (gap analysis, no code exists).**
- PR review lenses (security, architecture, structural QA) map to reflect's persona idea, but there is no lens value `pr`, no citation-role set for code review beyond `diff`/`source`/`test`, and no way to bind a persona to a slot. rf-qa's structural/qualitative split (`SKILL.md:632-633` uses `rf-qa` and `rf-qa-qualitative` as separate agents) is also an agent-type choice the template cannot express. [E1][E3]
- `--kind` would need at least the consumer dimension (which brief, which lens, which agent) — but that is better a separate axis than more `kind` values: `kind` today means round position (first vs re-review), which the #346 loop needs for any consumer. Adding `pr` or `qa` to `_KINDS` would conflate "which round" with "which consumer". [E3]

Key Takeaways
- Roles/lenses cannot be bound today; reflect relies on resolution order and a hard-coded persona list. A slot needs optional `role` (persona/lens brief selector) and `agent`/`adapter` fields, recorded in the resolution. [E1]
- Keep `kind` = round (first / re-review / verify-only) and add a separate `consumer` or `lens` axis that selects brief, finding lens and citation roles. [E3]
- The E3 loop prompt already depends on `panel resolve --kind`; changing `_KINDS` or the re-review rule affects the #346 loop. [E3]

## 10. Design input for one panel resolver serving all consumers (question 8)

Each point below cites the evidence it rests on; none is implemented.

1. **Keep the pure resolver and its sha256-frozen output** (`panel.py:500-707`, `:688-699`) [E3 + E1]. It is deterministic, data-driven and already the shared piece all three efforts touch (E3 prompt `:70`, E1 step 1, E2 reused its `review-panel-resolution/1` file shape per scope 01 §2.2).
2. **Distinctness as declared policy**, per template: `distinct: none | model | class`, plus per-slot `replicas` (intended repeats, recorded as such). Remove silent re-admission (`panel.py:543`); when a pool is exhausted, either skip (record `skipped_slots` with instance index) or fail, per policy. Evidence: D11 duplicate reproduced (section 4), E2's surviving doubling effect (CR:298), E1's class-diversity rule (`SKILL.md:646-648`). [E3][E1][E2]
3. **Fallbacks distinct-aware and recorded as a chain**: filter fallbacks by the final chosen set (section 4: strict `live7` gateway fallbacks include later picks), and record `fallback_chain` hops at dispatch; never overwrite `requested` (E2 `run-reviewer.sh:58`/`:76`). Default no fallback for evaluation runs (E2 `NOFALLBACK`, `:66`). [E2][E3]
4. **Environments describe dispatch, not just availability**: `launch` should name an adapter and an argument (`agent-class: haiku`, `cli-model: gpt-6-luna`, `alias: claude-gw-tier2[1m]`), so gateway is not `launch: {}` (`review-tiers.default.json:29`) and reflect is not forced into an "anthropic-only" label that the session env re-routes to Sol (section 4.1). Environment auto-detection should not key on one ccsession variable (`panel.py:492`); at minimum check that every alias a template needs is defined (D12). [E3][E1]
5. **Identity triple per reviewer**: `requested` (pin), `launch` (what was passed), `served` (observed or `unknown`), `identity_source`; write to E3's telemetry `model` group (`telemetry.py:49`) after widening `STRATA` (`:112-115`). Observation adapters: `claude -p` JSON top-level events (E2 `run-reviewer.sh:51`) and parent stream-json sub-agent events (E1 `extract.py:56-58`). Self-report and harness alias text are not identity (TS `REPORT.md:14`; `SKILL.md:348`). [E1][E2][E3]
6. **Dispatcher enforces the pin**: every Agent call must carry the resolved `launch`; a missing class is a dispatch error, not a frontmatter default (`reflect-reviewer.md:6`; `results.md:35`). [E1]
7. **Template gains optional `role`/`lens`/`agent` per slot and a `consumer` axis**; `kind` stays round-based (section 9). Reflect's prefix-keyed profile (`panel.py:71-73`, `:80-157`) becomes a data profile (`max_reviewers`, `forbidden_classes`, `require_classes`, `launch_kinds`), so PR review or rf-qa can declare their own without new code branches. [E1]
8. **Tier data carries provenance**: version + date + gateway for model lists (E2 evidence is dated 2026-11-12/13 on one gateway; tier file note dated 2026-11-10, `review-tiers.default.json:32`); add missing models (`muse-ember-1.0`); define or remove `tier0` (`panel.py:95-117`). [E2][E3][E1]
9. **`panel validate` should run profile rules too** (`panel_cmd.py:124` omits tiers), and the resolver should report `reviewers_requested` vs `reviewers_resolved` itself (SKILL.md step 1 builds that payload by hand, `:340`), and optionally take a reviewer-count cap (rule D5 `:321` has no code). [E3][E1]

Key Takeaways
- The resolver core is reusable as-is; the missing pieces are policy (distinctness, replicas), dispatch (launch adapters, enforced pin) and evidence (identity triple, dated tier data). [E1][E2][E3]
- The highest-risk gap for any consumer is that the resolution is not what runs: E1 dispatch ignores it, E2 bypassed it, and E3's loop follows it only through prompt text. [E1][E2][E3]

## Gaps and Questions

1. **Reflect's "qwen | kimi | deepseek if alias available"** (`SKILL.md:655`) [UNVERIFIED]: no env alias variable and no tier-file class exists for kimi or deepseek; no launch path for qwen through the Agent tool was found. Is this branch live, stale, or planned? [E1]
2. **`identity_source: observed` adapter** (`SKILL.md:348`) [CODE-CONTRADICTED as an implemented feature]: no code reads a reviewer transcript or sets `identity_source`; the only served-model extraction is the offline experiment script `extract.py:42-79` and the E2 runner. [E1]
3. **`model_observed:` card line** (`SKILL.md:341`): nothing consumes it (`reflect_shadow_exit.py:117-177` ignores it), and the harness reports aliases (TS `REPORT.md:14`), so it cannot reveal a served-model swap. Whether any shadow run after `9874d63fb` wrote it is not checked. [E1]
4. **`tier0`** (`panel.py:95-117`, `SKILL.md:346` "Tier 0 alias"): no `tier0` alias in the tier file and not a class; the rule is inert. What Tier 0 is meant to be (orchestrator? executor?) is undefined in code. [E1]
5. **Rule D5 `N_eff = min(--reviewers, alias count, 3)`** (`SKILL.md:321`) has no code; the resolver has no count option (`panel_cmd.py:18-63`). Shadow runs therefore always resolve the template's full count. [E1]
6. **Is `--forward-subagent-text` required** for sub-agent `message.model` to appear in a parent stream-json? [UNVERIFIED]; it decides whether observed identity is available for skill-driven dispatch at all. [E1]
7. **Gateway alias routing is runtime behaviour**, not code: "haiku -> claude-gw-tier2[1m] -> gpt-6.1-sol" was observed 2026-11-13 (combo A/B) and in this session's env; it can change with Coder/ccsession config (`T2bModel01`, `T3Model01` values observed 2026-11-13). Any unified design must re-probe. [E1]
8. **E2 runner cost under fallback** (`run-reviewer.sh:76`, `:87`): attempt files are overwritten across ladder models; how many E2 rows had a ladder hop (and therefore wrong `cost.json` and lost primary transcripts) is not counted here (scope 01 notes no fallback logs before the batch 9/10 incident, CR:295). [E2]
9. **E2 runner `APIERR` loop condition** (`:66` vs `:73`): an API-error run with a valid block does not fall back. Frequency in the study data is unknown. [E2]
10. **Sonnet-alone 2/16 at 93k tokens** (scope 00 §2.3 / PLAN `:24`) [UNVERIFIED in this file]: from PILOT-REPORT, not re-read. [E2]
11. **E2 `manifest.md:11` "aliases serve only the first model of a tier"** [UNVERIFIED in this file]: cited from scope slice 01 H31. [E2]
12. **Question for the owner:** is reviewer distinctness a correctness requirement (E1 anti-self-confirmation) or a cost/quality knob (E2)? The answer decides the default `distinct` policy per consumer. [E1][E2]
13. **Question:** should `kind` gain `verify-only` (hand-off D16 says verify-only is prompt-only) while consumer/lens becomes a separate axis? The E3 loop prompt (`document_review_loop_prompts.md:70`) is the existing caller to keep working. [E3]
14. **Scope 02 D14 statement** that no skill/command calls `review panel resolve` is incomplete: `rules/prompts/document_review_loop_prompts.md:70` does (as prompt text). The overlap matrix should list E3 as a resolver consumer. [E3]

## Stale Documentation Found

- **[STALE DOC]** Hand-off D11 cites `panel.py:402-408` and D12 cites `panel.py:372`; current lines are `:536-543` / `:666-699` and `:485-494` (behaviour unchanged). (scope 00 §2.4 rows D11, D12) [E3]
- **[STALE DOC]** Hand-off §5.2 cites resolution schema at `panel.py:498-520`; the record is now built at `:666-699` and the schema constant is `:27`. [E3]
- **[STALE DOC]** Hand-off §5.3 "Re-review uses only the fixed anchor `t1b-1` (`panel.py:452-454`)": behaviour holds, now `:600-605`, `:616`. [E3]
- **[STALE DOC]** `review-tiers.default.json:26` gateway note "dispatch mechanism per model not defined yet" is still true, but `SKILL.md:320` D4 treats the gateway as a permanently unsupported cell; no plan in code to define it. [E1][E3]
- **[STALE DOC]** `review-panel.live7.json:5` says gateway resolves "seven reviewers from the tier file's model lists" — true, but one model (Qwen3.8-max) is repeated under soft distinctness (run 2026-11-13), and the description does not say so (contrast `reflect-lite.json:5`, which documents its duplicate). [E3]
- **[STALE DOC]** `SKILL.md:655` names qwen/kimi/deepseek classes with no data or code behind them (Gaps 1). [E1]
- **[STALE DOC]** `PLAN.md:1-3` header says "designed, NOT run"; `FINDINGS.md:3` shows all 15 runs completed 2026-11-13. [E1]
- **[STALE DOC]** Scope 02 §4.2 marked `find_path` search locations and `@name` syntax UNVERIFIED; both are now CODE-VERIFIED (`panel.py:397-419`, `:430-454`). [E3]
- **[STALE DOC]** E2 CR:292 "Four verdicts flipped" names three (scope 01 H15); E2 CR:293 "161" corrected to 156 at CR:373. [E2]

## Summary

The panel resolver (`panel.py`) is a pure, deterministic, sha256-frozen tool shared by all three efforts in form but not in practice: E3's loop follows it through prompt text (`document_review_loop_prompts.md:70`), E1 records it in shadow mode but dispatches by a separate class rotation that the session env re-routes (so a "haiku" slot was served by `gpt-6.1-sol` and a missing class collapsed a whole panel to Sonnet, combo runs 2026-11-13), and E2 bypassed it entirely with raw model ids and a bash fallback ladder. Distinctness is the main configuration conflict: the default silently re-admits duplicates (D11, reproduced: Qwen3.8-max twice in gateway `live7`), E1's opt-in `--strict-distinct` drops slots instead, and E2's only surviving doubling effect (a second luna, CR:298, valid era from 2026-11-12 13:02) needs an intended repeat that neither mode can express. The gateway environment has `launch: {}`, which makes every reflect template fail to resolve there, while `anthropic-only` has no fallbacks and is not anthropic-only at serving time. Identity is pinned, not observed, in E1 (`9874d63fb` copies the pin into the card and parity compares records with each other), and E2's observed check rewrites `expected_model` on fallback; E3's unused telemetry schema already separates `resolved`/`launch`/`observed`. A unified resolver needs declared distinctness and replica policy, launch adapters per environment, an enforced pin at dispatch, a recorded identity triple, optional role/lens/agent per slot with `kind` kept as round, and dated tier data.
