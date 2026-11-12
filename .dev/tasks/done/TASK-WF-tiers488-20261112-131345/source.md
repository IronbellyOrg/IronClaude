# Issue 488 (ccsession tiers): remaining work after the 346 merge, owner decisions of 2026-11-12

Priority: Medium. Full issue text: `.dev/issues/488/issue-body.md` (owner decisions section wins over the edit plan). Edit plan: `.dev/issues/488/analysis/analyze-ccsession-tag.md`.

## State of master (verified 2026-11-12 on commit b0977b4f2)

PR #498 already landed the tier layout: `ccsession-models.json` (version 2026-11-11.1) defines `tier2b` (T2bModel01-04), `tier3` (T3Model01-02) and `tier4` (T4Model01-03); `MODEL-TIERS.md`, the README tier list, the `Claude Haiku 5.5` display name, a CHANGELOG entry, `tests/unit/test_ccsession_tiers.py`, and the review panel files (`src/superclaude/cli/review/data/review-tiers.default.json` already lists the real tier2b models in the order gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0; `tests/review/test_review_panel_live7.py` tests it, and still tests that a placeholder tier2b fails closed). So the line numbers in the issue's edit plan are stale and most rows are done. This plan covers only what is NOT done.

Final tier table (already on master, must stay): tier2b 4 slots [gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0] window 900000; tier3 2 slots [glm-5.3, Qwen3.8-max] window 900000; tier4 3 slots [gpt-6-luna, claude-haiku-5-5, grok-4.7] window 500000.

Gateway check (read-only, 2026-11-12, /v1/models): claude-haiku-5-5, glm-5.3, grok-4.7, Qwen3.8-max, gpt-6-luna, gpt-6.1-terra and muse-wonder-1.0 are all listed as served. A separate worker saw muse-wonder-1.0 answer as gpt-6.1-terra in an unrelated run; gateway routing is not fixed here and stays an open risk in the PR notes.

## Owner decisions of 2026-11-12 ("accept all") and what each needs

1. Review panel `tier2b` placeholder is filled with the real Tier 2b list, with a test. Master already has the filled list and a test. Verify only: the live7 panel and the `anthropic-only` stand-in still resolve, and the gateway environment does not fail closed on tier2b (`uv run pytest tests/review`). Edit only if a check fails.
2. 429 behaviour: accept PR #481 behaviour as merged (the first two 429s go back to Claude Code to retry, the third parks the model and the same request moves to the next eligible model in the tier). No Terra-specific rule. Document it in plain words in the README tier section. `MODEL-TIERS.md` row for Tier 2b currently says "If GPT-6.1 Terra returns a 429 the request is retried on GLM-5.3": reword it so it is not described as an immediate retry.
3. `src/superclaude/agents/issue-worker-t3.md` is pinned to `claude-gw-tier2b` (Terra first, as before the layout change), including its provenance sentence on line 12, the T3 row of `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` (line 13, and the E-TIER-UNAVAILABLE example around line 49), the table row at `src/superclaude/skills/sc-issue-protocol/SKILL.md` line 60, the allow-list sentence in `docs/reference/model-aliases.md` line 16, and the tests that pin it (`tests/skills/test_issue_worker_agents.py` line 22, `tests/skills/test_model_alias_policy.py` line 30). Keep `effort: low` (merged in #516). The agent keeps its name `issue-worker-t3`.
4. Claude Haiku 5.5: the owner's instruction overrides the placement rules in `MODEL-TIERS.md`. Record it as an owner exception with status "unscored"; do not invent a score. Master's note at about line 219 and the Tier 4 row already say so; make the exception and the "unscored" status explicit in section 5 (placement rules) so the rules and the table agree.
5. The `haiku` alias does not move: no change to ccsession alias code or to `tests/skills/test_model_alias_policy.py` lines 229-241.
6. Retry ladder rung 0 in `src/superclaude/skills/sc-implement-protocol/refs/retry.md` (lines 162 and 172) and the tracked copy `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md` points at `T2bModel01` (Terra, a gpt- model) instead of `T3Model01` (now glm-5.3). Update the family note (docs/reference/model-aliases.md line 63 and the retry.md wording) and the tests that read both copies: `tests/skills/test_model_alias_policy.py` line 227 and `tests/skills/test_workflow_archive.py` line 799 (RUNGS list).
7. Historical docs are NOT edited: `docs/designs/sc-issue-command.md`, `docs/testing/v5.0.0/sysop/*`. List their drift in the final report.
8. Gateway names verified (above).

## Other deliverables

- CHANGELOG `[Unreleased]`: add entries for decisions 2, 3, 4 and 6 under the existing issue 488 heading (or next to it).
- `ccsession-models.json` `version`: bump only if this change edits that file. Nothing above needs a JSON edit, so the file and its version stay as they are unless a check shows otherwise.
- Run `make sync-dev` then `make verify-sync` (never stage `.claude/`), `make lint`, and `uv run pytest` on: tests/unit/test_ccsession_tiers.py, tests/unit/test_ccsession_tag.py, tests/skills/test_model_alias_policy.py, tests/skills/test_issue_worker_agents.py, tests/skills/test_workflow_archive.py, tests/review, and the sc-issue / sc-implement skill tests that read the edited files.
- `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and justify any new hit.
- Do not push, do not open a PR. Merge order still holds: this change must not merge until the Coder release carrying the T2b slots is installed in every workspace (unverified).
- Post one comment on issue 488 (`gh issue comment 488 --repo IronbellyOrg/IronClaude`) recording the owner decisions, the gateway result and the branch name.
