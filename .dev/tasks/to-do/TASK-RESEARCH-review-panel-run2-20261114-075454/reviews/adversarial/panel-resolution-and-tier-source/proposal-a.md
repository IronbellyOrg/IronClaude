# Proposal A - slot C-09 (panel-resolution-and-tier-source)

Status: Complete

Slot: C-09 (slug `panel-resolution-and-tier-source`). Position: A.
Conflicts in the slot: C-S5, C-S16, CO-12, CO-13, FX-14, FX-15 (synth-06 6.12.1, 6.12.2, 6.12.5).
Date: 2026-11-14. Code state: HEAD `50d4d2b9d` on `ironbelly/shadow-runs`; the E2 branch tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` read with `git show` only.

Citation form. `path:line` is a file at HEAD in the worktree, read in this session. `R<NN>` is `research/NN-*.md` of this task folder. Tags: [CODE-VERIFIED] I read it at the cited line; [OBSERVED-RUNTIME] I ran a read-only command in this session; [CODE-CONTRADICTED]; [UNVERIFIED]. Design statements that no code or data decides are marked "design inference".

## 0. Consistency with the three adjudicated slots

I read `ADJUDICATION-RESULT.md` of C-01, C-02 and C-03.

- C-01 (`core-shape-and-finding-contract`): the winner is a thin shared contract now, with "ids, hashes, panel resolution, run record, eval harness" shared and one engine per module. Position A depends on panel resolution and the tier file staying one shared piece used by both the spec loop (v1 engine) and reflect (v2 kernel). That agrees with the C-01 outcome. Position A uses nothing that C-01 withdrew (locator-agnostic `annotate`, `citations` in ledger rows, the clustering marker, `cluster_v2` for new ledgers). One exact difference: C-01 condition 3 says "all existing pins pass unmodified" (T1). That condition is about the findings parsers and the ledger. Position A rewrites pins in the panel and CLI tests (section 4); I do not claim T1 for those.
- C-02 (`ledger-clearing-and-verdict-authority`): the clearing quorum uses `need = min(Q, requested)` and its open HIGH invariant INV-001 is that `need` can be 0 when `--resolution` carries an empty reviewers list. Position A does not decide clearing. It touches one input of it: where `requested` comes from. A resolution that `resolve` writes is never empty, because exactly one fixed anchor is mandatory (`panel.py:245-246`) and a fixed-anchor exhaustion is fatal (`panel.py:647-649`) [CODE-VERIFIED]. A hand-edited empty list stays C-02's open item; A does not close it.
- C-03 (`merge-verdict-policy-and-quorum`): the winner refuses a merge when `complete < min(2, requested)` and `requested = max(len(resolution.reviewers), len(--report))`. Its open HIGH invariant INV-007 says `requested` can collapse to 1 because `panel.resolve` drops skipped slots and writes `skipped_slots` only when an exclusion flag is used (`panel.py:636-656, 700-706`). Position A depends on this outcome and answers the data half of INV-007: with strict distinctness as the default the `skipped_slots` key is always written (`panel.py:700`) and the resolution gains an `expected` count (section 2.3). A does not decide the merge-side half (what the merge does with `expected`); that stays C-03. Position A also keeps the C-03 condition that "independence (distinct served model ids, vendor) is recorded data, requested not served, until `model_observed` exists (slot C-08)": nothing in A claims served identity.
- Where A disagrees with an adjudicated outcome: nowhere.

## 1. The position in one paragraph

Position A: the package owns the tier data. `src/superclaude/cli/review/data/review-tiers.default.json` stays the one file that holds, for every model the panel can name, its tier membership and order, its `class`, its `vendor` and, per environment, its `launch` value. Everything else that today keeps its own copy reads from it or is checked against it: the vendor substring table of `reflect/_diversity.py`, the SKILL.md class set, the hand-kept E2 fallback ladder (derived from the tier lists by a pure function), and the three tier-list copies (a CI check compares the file with the slot lists of `ccsession-models.json`; the Coder env stays the runtime owner of which model each slot serves and is read, never copied). A panel resolves with strict distinctness unless a profile declares repeats on purpose, and a resolution that comes out short names the shortfall in its own JSON and on stderr instead of silently re-admitting a duplicate. Adding `muse-ember-1.0` is a data edit of that one file (plus the matching slot line in `ccsession-models.json`), not a code change. The reason for A is control: package data is release-gated by tests, deterministic and hashable (`tiers_sha256`), while `ccsession-models.json` reaches every Coder workspace on its next launch without any test of the panel.

## 2. Design consequence for the shared core and the named modules

### 2.1 Ownership: one tier file, three readers, one check

Shared core (`cli/review`, `panel.py`, `panel_cmd.py`, the data directory) keeps `review-tiers/1` and extends it with data, not with a new owner:

| Item | Today | Under A |
|---|---|---|
| tier order and membership | `aliases.<tier>.models` in the package file (`review-tiers.default.json:5-10`) | unchanged; the file is the owner |
| class | `classes` (9 names, 13 ids, `:18-23`); tier-file consumers: `--hard-exclude-class` (`panel_cmd.py:82-92`), the reflect profile (`panel.py:122-125`), shadow parity | unchanged; the file stays the only class owner; the SKILL.md class set (`{opus, sonnet, haiku, qwen, kimi, deepseek}`, R04 section 8) becomes a documented subset or is generated from `classes` |
| vendor | substring table in `reflect/_diversity.py:39-61` (separate copy; `muse` maps to `meta`, all `claude-*` to `anthropic`) | new top-level `vendors` map (model id to vendor), validated by `validate_tiers`; `_vendor_from_model_id` first looks the id up there and keeps the substring table only for ids outside the file (the T2Model0N pool can hold such ids) |
| launch | per-environment `launch` map; empty under `gateway` (`:25-30`); the reflect profile caps values at `sonnet/opus/haiku` (`panel.py:72`) | the file owns the map; the launch mechanism per environment is slot C-07's decision; A only requires that whatever C-07 decides is a value in this map |
| slot lists of ccsession | `ccsession-models.json` `tiers.<t>.models_env` (names only, no model ids) | stays what it is; checked against, never read at resolve time |
| model id behind a slot | Coder env `T<N>Model0<M>` (outside the repo) | stays outside; optional runtime comparison (design inference): a `review panel` check that, when the env is present, compares each tier's `models` with the env slots named by `models_env` and prints a difference; never changes a resolution |
| E2 fallback ladder | hand-kept `FALLBACK` map in `run-reviewer.sh` (E2 tip) | a pure function of the tier lists (within-tier successor, then the head of the next tier), keyed by (tier, model); the within-tier part already exists as `fallbacks` in each resolved reviewer (`panel.py:555`) |

Layering is already in the code and A keeps it: `find_path` resolves an explicit path, then `SUPERCLAUDE_REVIEW_TIERS`, then `<project>/.superclaude/review-tiers.json`, then `~/.superclaude/review-tiers.json`, then the packaged default, as whole-file replacement (`panel.py:397-405` docstring and `:422-424` packaged default; `panel_cmd.py:28-32`) [CODE-VERIFIED]. A site with a different model set (a Coder workspace) has a supported place for its own file; the packaged file is the default and the test subject.

### 2.2 Named modules

- Reflect (Tier 2 panel, `cli/reflect`, `sc-reflect-protocol`): reads classes and vendor from the one file; the code engine's `_vendor_from_model_id` (`reflect/_diversity.py:39-61`) and the SKILL.md class set stop being independent copies (CO-12). Shadow mode already resolves with `--strict-distinct` (`SKILL.md:340`; `review-panel.reflect-pre.json:5` says "under strict distinctness") [CODE-VERIFIED], so A changes nothing for reflect's distinctness.
- Spec review loop (v1 engine per C-01): calls `panel resolve` through `document_review_loop_prompts.md:70` with no strictness flag. Under A the loop declares its distinctness on purpose (see 2.3), so its panel does not change by the default flip.
- Tasklist, workflow, PR review, rf-qa (later consumers): take the strict default and the one tier file; a consumer that wants repeats declares them.
- `ccsession-tag`: unchanged except the one data line when a slot is added (2.4).

### 2.3 Strict distinctness as the default, and what a shortfall is

Today (`panel.py`): `resolve_slot` re-admits an excluded model when the pool empties (`:539-543`), unless `strict_distinct` or `hard_exclude` is set; the CLI default is soft (`panel_cmd.py:59-63`); all eight packaged templates set `distinct_across_slots: true`, which is the soft form (grep of `src/superclaude/cli/review/data/`: all eight `review-panel.*.json`, line 6) [CODE-VERIFIED].

Under A (design inference; each piece is small):
1. The `panel resolve` default is strict; the soft behaviour stays reachable by an explicit `--allow-repeat` and is recorded in the resolution as `distinctness: soft`. The library keyword `strict_distinct=False` is not changed, so `pnl.resolve(...)` without the keyword stays byte-identical to the golden (`test_review_panel_exclusion.py:53-60`).
2. A strict resolution already writes `skipped_slots` and `excluded` (`panel.py:700-706`). A adds `expected` (the number of reviewers the template asks for this review kind, following the same `expand` rule: `panel.py:600-605`, so a re-review expects 1) and a derived `shortfall = expected - len(reviewers)`.
3. A shortfall is printed on stderr by `panel resolve` and fails the command (non-zero exit) when the resolved count is below the floor that slot C-03 sets for merge (`min(2, requested)`, an unmeasured parameter there). A fixed-anchor exhaustion keeps failing (`panel.py:647-649`).
4. A slot resolution order that serves the scarcest tier first (see 3.4) keeps strict from skipping slots that only the order made empty.

### 2.4 Ember is a data edit

`muse-ember-1.0` is in no tier data at HEAD (`git grep muse-ember HEAD -- src tests docs scripts` prints nothing, re-run today) [CODE-VERIFIED negative]. Under A its entry is: one id appended to `aliases.tier4.models` at the slot index the Coder env gives it (index 4, matching `T4Model04`), one `names` entry, one `classes` entry (the reflect profile rejects any reachable model without one: `panel.py:124-125`), one `vendors` entry, and one slot line `T4Model04` in `ccsession-models.json` `tiers.tier4.models_env`, which the existing count test forces to move together (`test_review_panel_live7.py:94-96`). Once the `vendors` map exists (2.1), no Python changes. The order of operations is the one the repo already documents: add the env slot in Coder first, because ccsession stops when a listed slot is not set (`MODEL-TIERS.md:189-193`; `models.py:666-669`) [CODE-VERIFIED].

## 3. Evidence

### 3.1 Why the package file, not ccsession, can own the data

1. `ccsession-models.json` holds slot names only: `tiers.<t>.models_env` lists `T2bModel01..04`, `T3Model01..02`, `T4Model01..03` and so on (`ccsession-models.json:70-128`); it has no model ids, no `classes`, no `launch` [CODE-VERIFIED]. `models.py:147-214` validates `tiers` as `models_env` (1 to 10 slot names) plus a label, and nothing else. The model ids come from the Coder env (`models.py:660-678`, `DEFAULTS_FILE = "/etc/aidev02/aienv.d/defaults.sh"` at `models.py:109`) [CODE-VERIFIED]. So a package file "derived from `ccsession-models.json`" cannot be derived from it alone; it needs the env, which is outside the repo and absent on a laptop or in CI (`select_env` then picks `anthropic-only`: `panel.py:485-494`).
2. `ccsession-models.json` is fetched live: "Every ccsession launch asks GitHub whether a newer copy exists ... existing installs get new models and profiles without a reinstall", from `https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/src/superclaude/skills/ccsession-tag/ccsession-models.json` (`models.py:6-12, 59-63`) [CODE-VERIFIED]. A panel data edit placed in that file therefore reaches every workspace on its next launch, and a listed slot that a workspace env lacks stops ccsession there (`models.py:669`; `.dev/research/346-review-loop-experiments/GO-LIVE-RUNBOOK.md:30,33` records the same stop for T2b, R04 section 6 rows 17-18). The package file reaches users only with a package release, after `pytest`.
3. The Coder env and the two repo copies already disagree today. [OBSERVED-RUNTIME, read-only `env`, 2026-11-14]: the env has `T3Model01..06` with `T3Model02=Qwen3.8-max` and `T3Model04=Qwen3.8-max` (a duplicate inside one tier), while `ccsession-models.json` names two tier-3 slots and the package lists two tier-3 models. `validate_tiers` rejects a duplicate inside one tier list (`panel.py:301-302`) [CODE-VERIFIED]. The `models_env` list is what filters the env into a tier, so the slot lists are the bridge, and a copy of the env without that filter is not a valid tier file. Where the three sources do agree, they agree exactly: the env order of `T2Model01..06`, `T2bModel01..04`, `T1aModel01..02`, `T1bModel01..03` and the first three of `T4Model0N` equals the package lists (`review-tiers.default.json:5-10`) [OBSERVED-RUNTIME comparison].
4. The check that ties the two repo files covers 3 of the 6 tiers by count and 2 first-model names (`test_review_panel_live7.py:92-98`) [CODE-VERIFIED]. I compared all six tiers by hand: package list lengths 2, 3, 6, 4, 2, 3 equal `len(models_env)` 2, 3, 6, 4, 2, 3 for tier1a, tier1b, tier2, tier2b, tier3, tier4 [CODE-VERIFIED by reading both files]. So extending the check to all six tiers passes today.
5. Every edit of the packaged tier file already forces a golden update by design: `test_review_panel_reflect_profile.py:74-90` asserts `sha256_json(tiers) == golden["tiers_sha256"]` for the packaged file and the pinned resolutions in `fixtures/panel-golden-packaged-tiers.json`; the byte-identity golden of the no-exclusion path uses a frozen copy (`test_review_panel_exclusion.py:3-5, 22-23`) [CODE-VERIFIED]. That is change control: a tier edit is a visible, reviewed diff with a hash change. R23 VL-23-232 records the same.

### 3.2 Why one owner of class and vendor

- Three class vocabularies exist (R04 section 8): the tier file `classes` (9 names, `review-tiers.default.json:18-23`), the vendor substring table (`reflect/_diversity.py:42-57`, where `muse` is `meta` and every `claude-*` is `anthropic`), and the SKILL.md set including `kimi` and `deepseek`, which no tier list contains (R04 section 8; `SKILL.md:1248` as cited there, not re-read by me) [CODE-VERIFIED for the first two, [UNVERIFIED] by me for the third line number].
- Class and vendor are not the same axis: Opus, Sonnet and Haiku are three classes but one vendor. The code engine's `single-vendor` degrade runs on the vendor axis (`_diversity.py:18-36`), the reflect profile and `--hard-exclude-class` on the class axis. A tier file that carries both keeps them consistent (decided fact CO-13: `muse-ember-1.0` is not a product default; its vendor and class are still data the file must hold before any panel names it).
- The reflect profile makes the tier file's `classes` mandatory for every reachable model (`panel.py:112-125`) [CODE-VERIFIED]. A tier file in another owner's hands would have to carry `classes` as well, so the class owner cannot be ccsession unless ccsession-models.json gains extra keys (it would accept them: `models.py:147-214` checks only the keys it knows, so it does not reject extra ones [CODE-VERIFIED]; but then every ccsession launch downloads data it does not use, and panel tests run against a file that changes outside a release).

### 3.3 Strictness: the soft default is silent duplication

- The soft rule is pinned as today's behaviour, with the reason stated in the test: "live7 in anthropic-only is 1 Sonnet + 6 Haiku today: soft distinctness re-admits Haiku" (`test_review_panel_exclusion.py:208-213`); "soft exclusion alone: today's behaviour re-admits the only candidate" (`:94-99`) [CODE-VERIFIED].
- Re-derived today [OBSERVED-RUNTIME, `uv run --no-sync python` over the packaged data, run ids `run1..run40`, template `@live7` and `@default`]:

| Template | Env | Slots | Soft resolutions with a duplicate model | Strict resolutions with skipped slots | Max skipped |
|---|---|---|---|---|---|
| `@live7` | gateway | 7 | 30 of 40 | 30 of 40 | 2 |
| `@live7` | anthropic-only | 7 | 40 of 40 | 40 of 40 | 5 |
| `@default` | gateway | 4 | 18 of 40 | 18 of 40 | 1 |
| `@default` | anthropic-only | 4 | 40 of 40 | 40 of 40 | 2 |

  The 30 and 18 reproduce DATA-11 and R17 P1 (the `run1..run40` id set). Under soft distinctness the duplicate is invisible in the resolution; under strict it is a named skipped slot.
- The 30 of 40 skipped slots in the gateway are an artifact of slot order, not of the model count. Resolving the same two templates with the slots sorted by ascending model count of their tier (fixed anchor first), strict gave 0 skipped slots in 40 of 40 gateway runs for both templates [OBSERVED-RUNTIME]. The tier-3 slots (two models) were exhausted only because tier 2 and tier 2b had taken `glm-5.3` and `Qwen3.8-max` first (`panel.py:614-635` resolves in template order). So strictness costs availability in `anthropic-only` (four distinct Anthropic ids for seven slots, an inherent limit) and not in the gateway, if the order is fixed.
- Re-review is unaffected: only the fixed anchor resolves (`panel.py:600-605`; `test_review_panel_live7.py:63-65`).
- E2 did not get its panels from `resolve_slot`: its launcher takes raw ids per reviewer (`run-reviewer.sh:48` at the E2 tip) [CODE-VERIFIED], so no E2 result says anything about the product's soft re-admission rule.

### 3.4 The ladder and the three tier-list copies

- The E2 ladder is a hand-kept map keyed by model id (`FALLBACK[glm-5.3]="Qwen3.8-max"`, `FALLBACK[Qwen3.8-max]="gpt-6-luna"`, ... at the E2 tip `run-reviewer.sh:19-43`) [CODE-VERIFIED via `git show`]. `glm-5.3` and `Qwen3.8-max` are members of tier 2, tier 2b and tier 3 (`review-tiers.default.json:7-9`), and `grok-4.7` of tier 2 and tier 4, so a model-keyed map cannot say which tier's successor it means; the E2 map takes the tier-3 reading. A function of (tier, model) over the tier lists has no such ambiguity. It also encodes the owner order recorded in the E2 comment (within-tier successor, then next-tier head) in one place.
- The E2 ladder names `muse-ember-1.0` as T4 02 and grok as T4 04 (`run-reviewer.sh:26-27, 33-34`); the live env has ember as `T4Model04` and haiku as `T4Model02`, grok `T4Model03` [OBSERVED-RUNTIME]. A ladder derived from the file follows whatever order the file has, so the E2 comment and the env stop being two answers.
- Tier 2b is named "Review-panel and fallback tier" in `MODEL-TIERS.md:44` (as quoted in R04 section 5; I did not re-read that line) while no code of `cli/review` reads `T2bModel01` (`panel.py:486-494` reads `T3Model01` only; R04 section 6) [CODE-VERIFIED]; FX-14 says environment detection by `T3Model01` alone is a portability exposure. Under A, detection stays a function of the env but reads a named list of marker variables from the tier file's environment entry (design inference). That is a small schema addition, not an owner change: the key set of an environment entry is closed (`panel.py:371-373`), so `validate_tiers` gains the key, and so does the new `vendors` map.

### 3.5 What I could not verify

- Whether the gateway serves `muse-ember-1.0` today (OQ-10, R04 gap 4): [UNVERIFIED]; the env lists it as `T4Model04`, a 2026-11-13 gateway list did not (`PLAN.md:194` as cited in R04).
- Whether the E2 harness' preference for repeated models (section 7) survives a fixed harness: [UNVERIFIED] (R08 G10).
- Whether strict-mode resolution order (3.3, scarcest tier first) changes the pinned strict-mode reflect results: I did not run the strict tests with that order [UNVERIFIED]. The reflect-pre template has three slots and the fixed anchor first, so I expect no change, but I measured nothing for it.
- Whether `plugins/` carries a copy of `ccsession-models.json`: a Glob of `plugins/**/ccsession-models.json` finds none [CODE-VERIFIED negative], so the plugin mirror parity pins (INV-N) are not touched by the slot line; the `plugins/` mirror of `retry.md` (which names `T2bModel01`) is a different file.

## 4. Invariants

### 4.1 Preserved

- INV-A (contract 1.8.0, 110 stable and 27 telemetry names, `merge_method` pair): no contract field name or value set changes. Reflect shadow mode already resolves strict (`SKILL.md:340`), so `reviewer_models`, `t2_model_class_diversity` and the parity lists are produced by the same call as today. A strict resolution already carries the extra keys `skipped_slots` and `excluded` (`panel.py:700-706`), so `expected` and `shortfall` are additive to a shape that consumers already see in strict runs. That consumers ignore unknown resolution keys is [UNVERIFIED]; I read only `recompute_parity` (`reflect_shadow_exit.py:117-137`), which reads `reviewers` and `tiers_sha256`.
- INV-B (`derive_verdict` map, exit codes 0/10/11/2, the 36-test matrix): `contract.py` and its tests are not edited. The one coupling is the single-vendor degrade (exit 11) that reads the vendor of each reviewer model (`_diversity.py:18-36`). A changes the implementation of `_vendor_from_model_id` to a lookup with the substring table as fallback; the 13 ids of `classes` must give the same vendor through both (see 5.2). That equality is a test A adds, not an assumption.
- INV-I (fail-closed): a short panel stops being invisible (3.3). A moves the system toward INV-I.
- INV-F (installed-path rule): no primitive gets a `src/superclaude/...` path. The cross-check lives in a test (tests may read the repo, as `test_review_panel_live7.py:86-89` does); the optional env comparison reads the env and the tier file through the CLI.
- INV-K (sync and layout gates): the tier file stays at `cli/review/data/review-tiers.default.json`, which R18 F15 lists as a move-or-rename trap for the golden fixtures; A moves nothing. The ccsession slot line is edited under `src/superclaude/skills/` and mirrored by `make sync-dev` as any skill file.
- INV-G, INV-H, INV-J, INV-M, INV-N: not touched (plugin copy: section 3.5).

### 4.2 Endangered

- INV-C and INV-D (spec loop unchanged): `test_review_cli.py:52-61` pins the default `panel resolve --env anthropic-only` at four reviewers, `t1b-1, t2-1, t3-1, t3-2`, which is the soft result (one Sonnet and three Haiku). The loop reaches `panel resolve` through `document_review_loop_prompts.md:70` without any strictness flag. Flipping the CLI default changes the spec loop's anthropic-only panel from 4 reviewers to as few as 2 (table in 3.3, `@default` anthropic-only: up to 2 skipped) unless the loop declares soft. A makes the loop declare it, and an installed copy of the prompt that lags the package leaves the old call in place until reinstall (C-03 INV-013 names the same lag: `make verify-sync` does not cover the loop-prompt copies). So A endangers INV-C for the window between package and prompt copy. The pin `test_review_cli.py:56-61` is rewritten with the change, as C-02 rewrote its own pins; I do not call that "pins unmodified".
- INV-L (shadow mode changes no verdict): any tier-file edit changes `tiers_sha256`; `recompute_parity` then reports a run recorded under the old hash as "not proven" (`reflect_shadow_exit.py:128-132`). Adding `vendors` or ember therefore degrades the parity evidence of every existing shadow run under the Stage 2 exit script, by design of that script. Separately, adding an id to `tier4` changes the pool of a random slot (`panel.py:544-545`), so re-resolving an old run id could yield a different panel. Whether a resumed shadow run reuses its stored `panel/resolution.json` instead of re-resolving is [UNVERIFIED] (I read `SKILL.md:340` only through a grep and the exit script).
- The golden pins: `test_review_panel_reflect_profile.py:74-90` and `fixtures/panel-golden-packaged-tiers.json` are regenerated for the `vendors` map and again for ember; the frozen-copy golden (`test_review_panel_exclusion.py:22-23, 53-60`) is untouched and keeps the byte-identity proof for the no-exclusion path.
- Availability: strict in `anthropic-only` cannot give 7 distinct models from four Anthropic ids (`review-tiers.default.json:33`). A gives up the 4-reviewer or 7-reviewer count in that environment and replaces it with a named shortfall. That is a loss of coverage by design.

## 5. The test or measurement that would show A right or wrong

### 5.1 Measurements that decide the open parts

- M1, strictness value. On a package with ground truth (the E2 `GT1`-style seeded control issues, R08 G11), compare three equal-size panels: soft with a duplicate (today's output), strict distinct, and a declared repeat (`ember + 2x luna`-style). Metric of record: R16's (items found in a blocking row where the item is blocking, plus wrong blockers, plus control found). A is wrong on the default if declared-repeat or soft panels beat strict panels at equal reviewer count with a confidence interval that excludes zero; it is right if strict is not worse. Today no such comparison exists: the E2 comparisons vary the package, not the rule (R08 G8-G11).
- M2, shortfall rate. Over `run1..run1000` for each packaged template and each environment, count strict shortfalls with and without the scarcest-first order. Today: 30 of 40 and 0 of 40 for `@live7` in the gateway (3.3). A is wrong on the order change if the order changes any pinned strict result (the strict tests are 10 occurrences in `test_review_panel_exclusion.py`, 3 in `test_review_reflect_templates.py`, 2 in `test_review_cli.py`, 1 each in the two reflect CLI tests).
- M3, drift between sources. Run the extended cross-check (5.2) against the ccsession file of `master` and against the Coder env of a real workspace on a schedule or at release; count disagreements per month. A is wrong on the single-source claim if the env or the live ccsession file changes the served model of a slot faster than package releases, because the package file would then be stale most of the time. Today the repo and env agree on all slots ccsession names (3.1 item 3), but one observation is not a rate.

### 5.2 Tests A adds or rewrites

- Extend `_assert_tiers_match_ccsession_slots` to all six tiers (counts and the first model of each tier checked against the env-independent facts the file can hold) (`test_review_panel_live7.py:92-98`).
- Parity test: for every id in `classes` and every id in a `vendors` map, `vendors[id] == _vendor_from_model_id(id)` before the lookup is introduced (so A cannot change a single-vendor degrade silently).
- Strict default: `panel resolve` without flags equals `panel resolve --strict-distinct`; `--allow-repeat` equals today's soft output byte for byte against the existing golden.
- Shortfall: `expected`, `shortfall`, stderr text and exit code for `@live7` in `anthropic-only` (2 resolved, 5 skipped).
- Ember: one test that the tier file, `classes`, `names`, `vendors` and `ccsession-models.json` change together.
- Rewritten: `test_review_cli.py:56-61`; regenerated: the packaged-tier golden (5.1 above lists why).

## 6. Effect on future PR code review and rf-qa replacement

- PR review (slot C-10): the panel is a separate pre-step in both C-10 positions. Under A it takes one resolved list from one tier file; a PR panel that must be diverse gets a named shortfall rather than a silent duplicate, which feeds the same C-03 quorum as any other consumer. A PR panel in an environment without gateway models (a laptop) resolves `anthropic-only` with at most four distinct Anthropic ids and says so.
- rf-qa replacement (slot C-11): the rf-qa lens agents have no `model:` key and run on whatever the parent session passes (R04 section 3.2). A replacement panel names models through the resolution; a read-only reviewer needs a `launch` value the environment owns (slot C-07). Under A that value is data in the one file, so changing which model an rf-qa lens runs on is a reviewed tier-file edit with a hash change, not an env edit that no test sees.
- Both futures need a launcher that A does not provide; A only fixes where the answer to "which model, which class, which vendor, which launch value" lives. The reflect profile's `launch` ceiling (`panel.py:72`, `:153-156`) stays a C-07 matter: with `launch: {}` under `gateway` a `reflect-*` template is refused today (R04 section 2 reproduced the refusal; I did not re-run it).

## 7. The strongest objection and the answer

Objection (from Position B and from the E2 data). The Coder env and `ccsession-models.json` are where the owner edits tiers (the repo's own page says the env slot is added first), so a second file in the package is a fourth place to forget; and E2's best panels repeat a model: the recommended default was `ember + 2x luna`, a second luna raised control-found by 0.83 (permutation p 0.048), and `sonnet + 2x luna` reached the control issue in 5 of 10 runs against 0 of 11 (R08 G9-G11). A default that forbids repeats forbids the best measured panel and makes an availability-first setting the exception.

Answer.
1. The package file is not a fourth place that can be forgotten: it already exists, is already the file the panel reads, and is already the only one with `classes`, `launch` and the `stand_ins` of an environment. The proposal removes copies (the vendor table, the SKILL.md class set, the ladder map) and adds a check (3.1 item 4) that fails when the file and the slot lists diverge. The env stays the owner of which model a slot serves; A reads it and never copies it.
2. A strict default does not forbid a repeat. It forbids a silent one. A profile that wants `luna` twice declares it, and the resolution records `distinctness: soft` and which model repeats. The E2 panels were built from raw ids by hand (`run-reviewer.sh:48`), not by the soft re-admission rule, so they are evidence for a declared repeat and say nothing for the accidental one (30 of 40 `@live7` gateway resolutions today, where a repeat was not chosen by anyone).
3. The E2 repeat results are exploratory: 6 of 48 tests with p below 0.05 and 2 to 3 false positives expected, replicates reuse the same three packages, and ember skipped `source.md` in 9 of 18 runs (R08 G8-G10). A default should not rest on them either way; M1 is the measurement that would.
4. What A concedes: if M1 shows that repeated panels beat distinct panels at equal count, the default becomes a per-profile value with soft as the common profile, and the cost of A reduces to the single tier file, the vendor and class ownership, and the shortfall report. The single-source claim does not depend on the strictness default; the two parts of A can be judged apart.
5. What A does not answer: who owns the tier file if the owner will not accept an edit in the package for each model change (GQ-050 / Q-5 is an owner question), and whether the repo copy can keep pace with the live ccsession file. M3 measures the second.

Status: Complete
