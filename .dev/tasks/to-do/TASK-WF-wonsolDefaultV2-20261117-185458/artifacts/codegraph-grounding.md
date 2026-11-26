# Codegraph grounding (TASK-WF-makeTheWonsolRev-20261117-130446)

## Run state

- index_state: fresh
- checked_at: 2026-11-17T13:04:46Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
- access: mcp (codegraph_status answered "Changes since index: 0 added, 0 modified, 0 removed"; lookup tools listed)
- tokens: none

## Resolved symbols

- `src/superclaude/cli/review/panel.py` outline (codegraph_node symbolsOnly): `load_panel` :447, `packaged_panel` :430, `_default` :422, `find_path` :397, `load_tiers` :470, `validate_panel` :160, `validate_tiers` :258, `resolve_slot` :500, `resolve` :565, `_PACKAGED_NAME` :427, `_REFLECT_PREFIX` :71. Read directly: the hard-coded `_default("review-panel.default.json")` is in `load_panel` (line 459 at planning time); `resolve_slot` takes `candidates[0]` for `fixed` and a seeded random choice among all available models for `random` (read lines 536-547).
- Data files read: `src/superclaude/cli/review/data/review-panel.default.json` (slots t1b fixed, t2 random, t3 count 2 random; `apply_to` first), `review-panel.live7.json`, `review-panel.reflect-lite.json`, `review-tiers.default.json` (aliases tier1a to tier4; environments `gateway` and `anthropic-only`; `anthropic-only` stand-ins only for tier2, tier2b, tier3, tier4).

## Dependents

- `load_panel` callers (codegraph_callers, def-line rows): `resolve_cmd` (`src/superclaude/cli/review/panel_cmd.py`, line 77 confirmed by Grep), and tests `tests/review/test_review_panel.py` (`test_template_lookup_precedence`, `tpl`, `test_invalid_template_file_is_rejected`), `tests/review/test_review_panel_live7.py` (`live7`, `test_default_panel_is_unchanged_by_live7`, `test_environment_variable_can_select_a_packaged_panel`, `test_unknown_or_malformed_packaged_names_are_rejected`), `tests/review/test_review_reflect_templates.py`. shown/total: 9/9. resolution: def-line (call sites confirmed by Grep for panel_cmd.py only).
- `load_tiers` users (Grep): `scripts/reflect_shadow_exit.py:205`, `tests/review/test_review_panel_reflect_profile.py`, `tests/cli/reflect/test_shadow_skill_contract.py`, `tests/review/test_review_panel.py`, `tests/review/test_review_reflect_templates.py`.
- Pinned golden files (Grep): `tests/review/fixtures/panel-golden-default-live7.json`, `tests/review/fixtures/panel-golden-packaged-tiers.json`, `tests/review/fixtures/review-tiers.frozen-1.0.0.json`; `tests/review/test_review_panel_exclusion.py` (frozen tiers copy).
- Text mentioning review panel resolve or the default: `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `src/superclaude/rules/prompts/document_review_loop_prompts.md`, `tests/review/test_review_rules_text.py`, `docs/reference/review-panel-live7.md`.
- Not a dependent (searched for `muse-ember-1.0`): `src/superclaude/skills/ccsession-tag/ccsession-models.json` and `MODEL-TIERS.md` form a separate registry; `tests/unit/test_ccsession_tiers.py` and `tests/unit/test_ccsession_tag.py` matched the model name only (UNVERIFIED whether either reads `review-tiers.default.json`; Task 5 runs them).

## Pre-check

Run 2026-11-17 with file checks, Grep and Read (codegraph fresh; no new readiness check): all 19 files named by the tasks exist; every symbol named resolves in `src/superclaude/cli/review/panel.py`; `tests/unit/test_ccsession_tiers.py` has no reference to `review-tiers` (the UNVERIFIED line above is now resolved: not a dependent). Dependent no task named before this check: `src/superclaude/rules/prompts/document_review_loop_prompts.md:70` runs `superclaude review panel resolve --run-id <id> --kind ...` with no template, which makes the review loop the real consumer of the default; one Task 6 acceptance bullet was added for its re-review (anchor) effect before the reflect call. `sc-reflect-protocol/SKILL.md` calls the panel with explicit `@reflect-*` templates and defaults to `--t2-engine legacy`, so the default change does not reach reflect.
