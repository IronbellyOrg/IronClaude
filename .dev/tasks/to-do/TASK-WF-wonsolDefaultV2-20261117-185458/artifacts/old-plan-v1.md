---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-makeTheWonsolRev-20261117-130446
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Make the wonsol reviewer panel the product default, selected by template reference

Source: ./source.md
Goal: `superclaude review panel resolve` with no template argument resolves the new 3-reviewer `wonsol` panel (wonder anchor, sol, ember) by reading a pointer to a packaged template, not by a hard-coded file name; the old 4-reviewer default stays available as a packaged template; every existing lookup precedence (explicit path, `SUPERCLAUDE_REVIEW_PANEL`, project and user `review-panel.json`) still works and a 3-reviewer default is shown to resolve in both environments.

## Constraints

- Work on a new branch cut from `origin/master`, never on the evaluation branch that holds the answer key; open the PR only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; never stage anything under `.claude/`.
- Edit only under `src/superclaude/cli/review/`, `src/superclaude/skills/`, `src/superclaude/rules/`, `tests/` and `docs/`; run `make sync-dev` after skill or rule edits.
- The product panel chooses models only. The seat lenses, table caps and briefs of the evaluation harness (S = wonder with lenses C5 C6 C8 C2 and cap 8; L1 = sol; L2 = ember) are not part of this change, so only the model mix transfers. The confirming test did not meet its registered bar (found fraction +0.099 and +0.109, lower bounds -0.004 and -0.006; 1.56 times the control's panel time); the owner has ordered the default change as provisional, and the plan must say so in the docs it touches.
- `validate_panel` in `src/superclaude/cli/review/panel.py` already allows 1 to 8 reviewers and requires exactly one `fixed` slot; do not change those rules. A template id must not start with `reflect-` (that prefix turns on the reflect profile).
- Keep the strategy and tier-name rules: tier names match `^tier[0-9]{1,2}[a-z]?$`.

## Phase 1: Tier data for the three wonsol seats

## Task 1: Add three seat tiers and the ember model to the packaged tier file

Edit `src/superclaude/cli/review/data/review-tiers.default.json`. Add three aliases: `tier5a` (gateway alias `claude-gw-tier5a[1m]`, models `muse-wonder-1.0` then `claude-sonnet-5-5`), `tier5b` (`claude-gw-tier5b[1m]`, models `["gpt-6.1-sol"]` only) and `tier5c` (`claude-gw-tier5c[1m]`, models `["muse-ember-1.0"]` only). The list shapes matter and were checked against `resolve_slot` in `src/superclaude/cli/review/panel.py`: a `fixed` slot takes the first available model of its list (so `tier5a` falls back from wonder to Sonnet), but a `random` slot picks at random among every available model of its list, so `tier5b` and `tier5c` must hold exactly one model each to make the seats deterministic (a two-model list returned the fallback model in a draft run). In the `anthropic-only` environment add `stand_ins` entries `tier5b` and `tier5c`, each `["claude-haiku-5-5"]` (that environment lists only Anthropic models, and a tier with none available raises `NoModelAvailable` without a stand-in). Add `muse-ember-1.0` to `names` ("Muse Ember 1.0") and to `classes` (class `muse`, as the other Muse models). Bump the tier file `version` by one minor step.

Acceptance criteria:
- `validate_tiers` returns no errors for the edited file, and `pnl.load_tiers()["aliases"]` has `tier5a`, `tier5b` and `tier5c` with the models above.
- Resolving a draft template with the three slots of Task 2 for run ids `t1`, `t2` and `t3`: in `anthropic-only` it prints `claude-sonnet-5-5`, then two `claude-haiku-5-5` marked `stand_in` true, every time; in `gateway` it prints `muse-wonder-1.0`, `gpt-6.1-sol`, `muse-ember-1.0` every time.
- No existing alias (`tier1a` to `tier4`) changes its models, so `live7` and the old default resolve to the same models as before.

## Phase 2: The wonsol template and the preserved 4-reviewer default

## Task 2: Add the wonsol panel template

Depends on: Task 1

Create `src/superclaude/cli/review/data/review-panel.wonsol.json` with `schema` `review-panel/1`, `template_id` `wonsol`, `version` `1.0.0`, a description that states the three models and that the choice is provisional, `distinct_across_slots` true, `apply_to` `["first"]` as in the existing default, and three slots: `t5a` (tier `tier5a`, count 1, strategy `fixed`, the anchor), `t5b` (tier `tier5b`, count 1, strategy `random`), `t5c` (tier `tier5c`, count 1, strategy `random`). It is loaded with `@wonsol` through `packaged_panel` in `src/superclaude/cli/review/panel.py`.

Acceptance criteria:
- `pnl.load_panel("@wonsol")` returns the template and `pnl.validate_panel(it, pnl.load_tiers()) == []`; the slot counts sum to 3 and exactly one slot is `fixed`.
- `uv run superclaude review panel resolve --template @wonsol --run-id t1 --env anthropic-only` and `--env gateway` both exit 0 and list three reviewers with ids `t5a-1`, `t5b-1`, `t5c-1`; in `anthropic-only` the anchor is `claude-sonnet-5-5` and the other two are Haiku stand-ins (so that environment does not run wonder, sol or ember).
- `--kind re-review` resolves only the anchor `t5a-1`, the same rule that `live7` follows in `tests/review/test_review_panel_live7.py` (`test_re_review_resolves_only_the_anchor`).

## Task 3: Keep the current 4-reviewer default as the packaged template `classic`

Create `src/superclaude/cli/review/data/review-panel.classic.json` with the exact slots, `distinct_across_slots` and `apply_to` of the current `src/superclaude/cli/review/data/review-panel.default.json`, `template_id` `classic`, and a description saying it is the previous production default. Then delete `src/superclaude/cli/review/data/review-panel.default.json` (the default is selected by the pointer of Task 4, so no template keeps the id `default`).

Acceptance criteria:
- `pnl.load_panel("@classic")` has four reviewers (`t1b` 1, `t2` 1, `t3` 2) and resolves in `anthropic-only` to `claude-sonnet-5-5` plus three `claude-haiku-5-5`, exactly as the old default did.
- `grep -rn "review-panel.default" src tests docs scripts` finds no remaining reference except the ones Task 5 and Task 6 rewrite.

## Phase 3: The default selected by reference

## Task 4: Select the default through a pointer file instead of a hard-coded file name

Depends on: Task 2, Task 3

Add `src/superclaude/cli/review/data/review-default.json` with content `{"schema": "review-default/1", "template": "wonsol"}`. In `load_panel` of `src/superclaude/cli/review/panel.py` (the `else _default("review-panel.default.json")` branch, line 459 at planning time) replace the hard-coded file name with a new function `default_template_name()` that reads the pointer file through `_default`, checks `schema` and that `template` matches `_PACKAGED_NAME`, and then returns `packaged_panel(name)` validated by `validate_panel` as the `@name` branch does. A pointer with a bad schema, a bad name or a name with no packaged template raises `ValueError` that names the pointer file. The lookup order of `find_path` stays untouched: explicit path, `SUPERCLAUDE_REVIEW_PANEL`, `.superclaude/review-panel.json` of the project, then of the home directory, then the packaged default. Callers that must keep working: `resolve_cmd` in `src/superclaude/cli/review/panel_cmd.py`, `scripts/reflect_shadow_exit.py` (it uses `load_tiers`, so it needs no code change but its tests must pass), and the `load_panel` callers in `tests/review/test_review_panel.py`, `tests/review/test_review_panel_live7.py` and `tests/review/test_review_reflect_templates.py`.

Acceptance criteria:
- With no flag, no environment variable and no `.superclaude/review-panel.json`, `pnl.load_panel()["template_id"] == "wonsol"` and the file `src/superclaude/cli/review/data/review-default.json` is the only place that names it; changing its `template` to `classic` makes `pnl.load_panel()["template_id"] == "classic"` with no code change.
- A pointer naming an unknown template, a malformed name or a wrong schema raises `ValueError` mentioning `review-default.json`.
- `find_path` precedence is unchanged: a project `review-panel.json`, a home one, `SUPERCLAUDE_REVIEW_PANEL` and an explicit path still override the pointer (`test_template_lookup_precedence` keeps its order of assertions).
- `uv run superclaude review panel resolve --run-id t1 --env anthropic-only` prints three reviewers (Sonnet plus two Haiku stand-ins); with `--env gateway` it prints the three wonsol models.

## Phase 4: Tests, goldens and documentation

## Task 5: Update the tests and golden files that pin the old default and add the regression tests

Depends on: Task 4

Edit these existing tests: `tests/review/test_review_panel.py` (the `assert pnl.load_panel()["template_id"] == "default"` line of `test_template_lookup_precedence` becomes `"wonsol"`; `test_packaged_defaults_are_read_through_importlib_resources` checks the pointer file and the tier file instead of `review-panel.default.json`), `tests/review/test_review_panel_live7.py` (`test_default_panel_is_unchanged_by_live7` becomes a test that the default is `wonsol` with 3 reviewers and that `@classic` still has 4 reviewers and `live7` still has 7), and re-pin `tests/review/fixtures/panel-golden-default-live7.json` and `tests/review/fixtures/panel-golden-packaged-tiers.json` only where the tier file bump of Task 1 changes `tiers_sha256`, keeping the frozen-tier copy `tests/review/fixtures/review-tiers.frozen-1.0.0.json` byte-identical so `tests/review/test_review_panel_exclusion.py` still proves that the old resolutions did not move. Add `tests/review/test_review_default_template.py` with these tests: the default resolves to a template by reference (`default_template_name()` returns the pointer's value); a three-reviewer default resolves in `anthropic-only` and in `gateway`; a pointer edited in a temporary copy of the data folder switches the default to `classic` with no code change; a bad pointer is rejected. Check that `tests/review/test_review_panel_reflect_profile.py`, `tests/review/test_review_reflect_templates.py` and `tests/cli/reflect/test_shadow_skill_contract.py` still pass (they read `load_tiers` and `classes`; the new `classes` entry for ember must not break the reflect profile rules).

Acceptance criteria:
- `uv run pytest tests/review tests/cli/reflect tests/unit/test_ccsession_tiers.py -q` passes with no test skipped for this change; `tests/unit/test_ccsession_tiers.py` is run only to show it is not affected (it matched a search for `muse-ember-1.0`; if it reads `review-tiers.default.json`, update it in this task).
- The new test file fails if `load_panel` goes back to a hard-coded file name (the pointer-switch test is the check) and if the default is changed to a template with 4 reviewers while the 3-reviewer assertion remains.
- `git diff --stat` shows no change to `tests/review/fixtures/review-tiers.frozen-1.0.0.json`.

## Task 6: Update the documentation and rule text that describe the default panel

Depends on: Task 5

Edit `docs/reference/review-panel-live7.md` so it no longer says the default is the 4-reviewer panel and describes the pointer file, the `@wonsol` and `@classic` templates, the new tiers, the `anthropic-only` resolution and the provisional status with the confirming-test numbers of the Constraints section. Read `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `src/superclaude/rules/prompts/document_review_loop_prompts.md` and `tests/review/test_review_rules_text.py` for statements about the default panel size or composition (the Task 4 grep found `review panel resolve` and `review-panel.json` text there) and change only the statements that are now false; keep `tests/review/test_review_rules_text.py` passing. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `grep -rn "2x Tier 3\|Tier 1b is the fixed anchor\|four reviewers\|4 reviewers" src docs tests` finds no sentence that calls the 4-reviewer panel the product default.
- `uv run pytest tests/review/test_review_rules_text.py -q` passes and `make verify-sync` exits 0; no file under `.claude/` is staged.
- The sentence in `src/superclaude/rules/prompts/document_review_loop_prompts.md` that tells the review loop to run the reviewers `superclaude review panel resolve` prints (the one real consumer of the default panel found by search) stays true, and the docs of Task 6 state that the re-review reviewer is the anchor, which changes from the Tier 1b model (Sonnet) to `muse-wonder-1.0` in the `gateway` environment and stays `claude-sonnet-5-5` in `anthropic-only`.
- The PR description names the confirming-test result (not confirmed by the registered rule) and that the model mix, not the evaluation seat lenses, is what ships.
