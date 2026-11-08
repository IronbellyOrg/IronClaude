---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-refactorAllMcpTo-20261108-150855
version: "1"
priority: Medium
created_date: "2026-11-08"
---

# Add LiteLLM proxy MCP tool names to every MCP call site (issue 454)

Source: ./source.md
Goal: every skill, command, agent, hook, eval matcher, script, core file and doc that names a direct MCP tool also names the tool the central LiteLLM proxy serves, proxy first, so a session that has only the proxy (`mcp__litellm__*`) finds its tools, while sessions with direct servers or with neither behave exactly as before. Design: `.dev/issues/454/design/design.md` (sections cited per task).

## Constraints

- Naming rule (design section 2): name both tools, proxy first, direct kept. Proxy names: Augment search `mcp__litellm__augment_code-augment_code_search` (called AUG below), `mcp__litellm__context7-resolve-library-id`, `mcp__litellm__context7-query-docs`, `mcp__litellm__Tavily-tavily_search`, `mcp__litellm__Tavily-tavily_extract`, `mcp__litellm__Tavily-tavily_crawl`, `mcp__litellm__Tavily-tavily_map` (capital `T`, case-sensitive). Playwright plugin names `mcp__plugin_playwright_playwright__browser_<x>`.
- AUG phrase (full form, verbatim): "Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep."
- AUG short form (inside lists and tables): "`mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)".
- Tavily phrase: "`mcp__litellm__Tavily-tavily_<x>` (else `mcp__tavily__tavily_<x>`)", keeping any existing WebSearch/WebFetch fallback tail. Context7 phrase: "`mcp__litellm__context7-<tool>` (else `mcp__context7__<tool>`)". Wildcards: "`mcp__litellm__Tavily-*` or `mcp__tavily__*`", "`mcp__litellm__context7-*` or `mcp__context7__*`".
- Allow-lists (`tools:` / `allowed-tools:`): insert each proxy name immediately before its direct twin; never remove a direct name except `mcp__auggie-mcp__codebase-retrieval`, which is replaced by AUG followed by `mcp__auggie__codebase-retrieval`. `mcp__litellm__Tavily-tavily_research` is not added anywhere.
- `mcp-servers:` metadata: add `litellm` first; replace `auggie-mcp` with `auggie`; keep the other words (`[auggie, codegraph]` becomes `[litellm, auggie, codegraph]`).
- Availability tests ("if X is not available") become "if neither <proxy name> nor <direct name> is available". Every existing degrade or fail-open path is kept verbatim (design section 4).
- Never hard-code a repository owner, name or branch; never add a `src/superclaude/...` path to an installed primitive.
- Edit `src/superclaude/**` and the hand-maintained `plugins/superclaude/**` copies only; never edit or stage `.claude/` mirrors (run `make sync-dev` instead) and never hand-edit `~/.claude`.
- Line numbers below were recorded at commit 0423fe5f; re-locate each edit by its text before editing.
- Python only through UV (`uv run pytest ...`). Never print, log or write `LITELLM_API_KEY` or any token.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); `.dev/issues/` stays out of the index. No push and no PR in this run.

## Phase 1: Hooks and the eval coverage gate recognise proxy tools

## Task 1: Widen the Auggie flag-clear hook to the proxy Augment tool

Design section 6.1. In `src/superclaude/hooks/hooks.json` (PostToolUse matcher at about line 149) change the matcher `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*` to `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*|mcp__litellm__augment_code-.*`. Set `plugins/superclaude/hooks/hooks.json` (about line 119, currently `mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*`) to the same string. In `src/superclaude/hooks/scripts/auggie-flag-clear.sh` add `|mcp__litellm__augment_code-*` to the `case` pattern (about line 23) and list the fourth prefix in the header comment (line 3); make `plugins/superclaude/hooks/scripts/auggie-flag-clear.sh` identical to the src script's comment and case line. Do not change `freshness-user-prompt.sh` (design 6.2). Update the pinned matcher strings in `tests/cli/test_verify_sync_hooks.py` (about lines 179-216) and `tests/cli/eval/test_expect_settings_json.py` (about lines 178, 184, 328). In `tests/hooks/test_auggie_flag_clear_mcp_prefix.py` and `tests/hooks/test_auggie_first.py` add a case where `mcp__litellm__augment_code-augment_code_search` clears the flag and one where `mcp__litellm__Tavily-tavily_search` does not.

Acceptance criteria:
- Both `hooks.json` files carry the identical four-alternative matcher; both flag-clear scripts carry the identical four-glob case line.
- `uv run pytest tests/hooks/test_auggie_flag_clear_mcp_prefix.py tests/hooks/test_auggie_first.py tests/cli/test_verify_sync_hooks.py tests/cli/eval/test_expect_settings_json.py tests/cli/test_install_hooks.py -v` passes, including the two new cases; output saved to `./artifacts/t1-pytest.log`.

## Task 2: Count proxy tools in the eval coverage gate

Design section 6.4. In `src/superclaude/cli/eval/coverage.py` add `"mcp__litellm__"` as a fourth entry of `_DEFAULT_MCP_TOOL_PREFIXES` (about lines 100-104), change the comment above it from three to four prefixes, and update the docstrings that enumerate the prefixes (about lines 9-10, 195, 253). Do not change `eval_covers_pattern` and do not add a `mcp_server.litellm` capability to `src/superclaude/cli/eval/capabilities.py`. In `src/superclaude/cli/eval/suites/real.yaml` update only the assertions (about lines 72, 80, 87, 94) that compare the whole flag-clear matcher string so they expect the Task 1 matcher; leave prompts, gates and the E16 Tavily entry unchanged. In `src/superclaude/cli/eval/suites/installer_sync_drift.yaml` (about lines 20, 65) update wording that lists the flag-clear case globs. Add a unit test in the existing coverage-gate test module under `tests/cli/eval/` asserting that the default filter selects a matcher `mcp__litellm__augment_code-.*` and that an eval expecting `mcp__litellm__augment_code-augment_code_search` covers it.

Depends on: Task 1

Acceptance criteria:
- `_DEFAULT_MCP_TOOL_PREFIXES` has four entries including `mcp__litellm__`; `capabilities.py` is unchanged (`git diff --quiet src/superclaude/cli/eval/capabilities.py`).
- `uv run pytest tests/cli/eval -v` passes including the new test; output saved to `./artifacts/t2-pytest.log`.

## Phase 2: Agents list and call the proxy tools

## Task 3: Add proxy Tavily, Context7 and Playwright names to the research agents

Design section 3.1 items 1-5. In the `tools:` lists of `src/superclaude/agents/deep-research.md`, `deep-research-agent.md`, `rf-analyst.md`, `rf-assembler.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-task-builder.md`, `rf-task-executor.md`, `rf-task-researcher.md`, `rf-team-lead.md` insert `mcp__litellm__Tavily-tavily_<x>` before each `mcp__tavily__tavily_<x>` already listed (do not add map/crawl where absent). In `deep-research.md` and `deep-research-agent.md` insert the two Context7 proxy names before their direct twins; in `deep-research-agent.md` insert `mcp__plugin_playwright_playwright__browser_navigate`, `_snapshot`, `_evaluate` before the three `mcp__playwright__browser_*` entries. Rewrite the Tavily body prose of the same ten files (change-map Agents row 4: `deep-research.md:27,35,41,43,59`, `deep-research-agent.md:145,147,148,152,154`, `rf-analyst.md:365,367,373,422-423`, `rf-assembler.md:230-231,237,288`, `rf-qa.md:119-120,125,549`, `rf-qa-qualitative.md:126-127,132,809`, `rf-task-builder.md:430,443-445,561`, `rf-task-executor.md:356`, `rf-task-researcher.md:328,353,371-376,417`, `rf-team-lead.md:307,309,315,398`) to the Tavily phrase; the tool-presence test in `deep-research.md` (about line 59) and the `tavily_unavailable` test in `deep-research-agent.md` become "neither ... nor ...". Rewrite the wildcards at `deep-research.md` (about line 37) and `rf-task-researcher.md` (about line 543). Leave `description:` lines unchanged. Widen `_TAVILY_ID` in `tests/agents/test_tavily_tool_parity.py` (about line 27) to `mcp__(?:tavily__tavily|litellm__Tavily-tavily)_[a-z]+` and add an assertion that each listed direct Tavily name has its proxy twin listed before it; update `tests/core/test_research_config.py` only if a pinned agent string changes.

Acceptance criteria:
- Every one of the ten agents lists a proxy Tavily name immediately before each direct Tavily name it lists; no direct name was removed (`git diff` shows only added list entries in `tools:` lines).
- `uv run pytest tests/agents tests/skills/test_tier2_tavily_consistency.py tests/core/test_research_config.py -v` passes; output saved to `./artifacts/t3-pytest.log`.

## Task 4: Add the proxy Augment tool to the Auggie agents

Design section 3.1 items 6-7. Insert AUG before `mcp__auggie__codebase-retrieval` in the `tools:` line (line 5) of `src/superclaude/agents/auggie-reviewer.md`, `eval-docs-loader.md`, `reflect-reviewer.md`, `reuse-auditor.md`, `troubleshoot-analyst.md`. Rewrite the prose at `auggie-reviewer.md` (about lines 37, 81, 96, 115), `eval-docs-loader.md` (about lines 28, 36) and `rf-team-lead.md` (about line 147) to the AUG phrase; the `auggie-reviewer.md` "in-session" wording states that AUG sees the pushed branch only and the uncommitted diff is read with Read, Grep or codegraph. In the same change, update the closed roster in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (about line 31) so it matches the new `troubleshoot-analyst.md:5` list exactly, and update the positive roster in `tests/troubleshoot/test_diagnostic_worker_contract.py` (about line 24); keep its negative fixture (about lines 154-155).

Acceptance criteria:
- The five agents list AUG immediately before `mcp__auggie__codebase-retrieval`; codegraph entries unchanged.
- `uv run pytest tests/troubleshoot tests/agents -v` passes; output saved to `./artifacts/t4-pytest.log`.

## Phase 3: Skills route to the proxy tools

## Task 5: Update the sc-recommend skill and its plugin copy

Design section 3.2 item 1 and 3.7 item 1. In `src/superclaude/skills/sc-recommend/SKILL.md` add AUG, `mcp__litellm__Tavily-tavily_search`, `mcp__litellm__Tavily-tavily_extract` to `allowed-tools:` (line 4) before their direct twins and rewrite the call at about line 134 to the AUG phrase, keeping its degrade-to-Read sentence. In `src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md` (about line 24) apply the Tavily phrase. Apply the identical edits to `plugins/superclaude/skills/sc-recommend/SKILL.md` and `plugins/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md`. In `src/superclaude/cli/recommend/prompts.py` (about line 146) and `src/superclaude/hooks/scripts/sc-recommend-phase0.sh` (about line 80) replace the call instruction with the AUG short form plus "repo from `git remote get-url origin`, default branch", keeping "Do not iterate file-by-file." and "Unavailable/empty ranking degrades to direct Read, never to a fabricated verified target." and the `auggie_status` output field.

Acceptance criteria:
- `cmp` of each src/plugin pair (`SKILL.md`, `refs/plugin-ecosystem-sources.md`) reports identical files.
- `uv run pytest tests -k recommend -v` passes; output saved to `./artifacts/t5-pytest.log`.

## Task 6: Update the troubleshoot, reflect and validate-roadmap protocol skills

Design section 3.2 items 2-4. `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`: `allowed-tools:` (line 4) gains AUG, both Context7 proxy names and `mcp__litellm__Tavily-tavily_search` before their twins; AUG phrase at about lines 195, 240, 397, 613; Context7 phrase at about lines 395, 402, 615 and Tavily phrase at about lines 396, 616. `refs/diagnosability-audit.md` (about lines 11, 49) and `refs/doc-discovery.md` (about line 11): AUG phrase; the availability test at `diagnosability-audit.md:49` checks "AUG or `mcp__auggie__codebase-retrieval`". Update the verbatim pinned lines in `tests/skills/test_worker_contract.py` (about lines 2908, 2916) to the edited SKILL.md lines. `src/superclaude/skills/sc-reflect-protocol/SKILL.md`: `allowed-tools:` (line 5) as above; AUG phrase at about lines 452, 462; Tavily phrase at about line 1796. `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`: in `allowed-tools:` (line 4) replace `mcp__auggie-mcp__codebase-retrieval` with `mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval`; AUG phrase at about lines 127, 253, 262, 871, with the "Requires" gates at 253 and 871 requiring "AUG or `mcp__auggie__codebase-retrieval`" and staying fail-open. Apply the `mcp-servers:` metadata rule to these three skills (troubleshoot line 10, reflect line 19, validate-roadmap line 13).

Depends on: Task 4

Acceptance criteria:
- `grep -n 'mcp__auggie-mcp__' src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` finds nothing.
- `uv run pytest tests/skills/test_worker_contract.py tests/skills/test_tier2_tavily_consistency.py tests/troubleshoot -v` passes; output saved to `./artifacts/t6-pytest.log`.

## Task 7: Update the brainstorm, auggie-review and pr-submit skills

Design section 3.2 items 5-7. `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` (about lines 187, 195) and `refs/handoff-routing.md` (about line 16): Tier 1 primary names AUG then `mcp__auggie__codebase-retrieval`; `quality_tier: primary` is earned by either; the `fallback_1` and `skipped` chain is unchanged. `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (about lines 20, 225): AUG phrase at the MCP mentions only; the `auggie` CLI path and `mcp-servers:` line 10 are unchanged. `src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md` (about line 31): AUG phrase with `branch` = the PR head branch and a note that only pushed commits are visible. Apply the `mcp-servers:` metadata rule to `sc-brainstorm-protocol/SKILL.md` (line 15) and `sc-pr-submit-protocol/SKILL.md` (line 10).

Acceptance criteria:
- The brainstorm skill still contains its `fallback_1` and `skipped` tier text unchanged (`git diff` shows no removed line containing them).
- `uv run pytest tests -k "brainstorm or auggie_review or pr_submit" -v` passes; output saved to `./artifacts/t7-pytest.log`.

## Task 8: Update `mcp-servers:` metadata in the remaining skills

Design section 3.2 item 8. Apply the metadata rule to the `mcp-servers:` line of these `SKILL.md` files under `src/superclaude/skills/`: `sc-issue-protocol` (line 10), `sc-cli-portify-protocol` (line 7), `sc-cleanup-audit-protocol` (line 6), `sc-adversarial-protocol` (line 12), `sc-cli-eval-protocol` (line 11), `sc-release-split-protocol` (line 13), `sc-roadmap-protocol` (line 13), `sc-tasklist-protocol` (line 7). Only add `litellm` where the line already names `auggie`, `auggie-mcp`, `context7` or `tavily`.

Acceptance criteria:
- Each of the eight lines names `litellm` first and no longer names `auggie-mcp`; no other line of those files changed.
- `uv run pytest tests/skills -v` passes; output saved to `./artifacts/t8-pytest.log`.

## Task 9: Rewrite bare `codebase-retrieval` steps in the generic skills

Design section 3.2 items 9-10. Rewrite each bare `codebase-retrieval` mention to the AUG phrase (short form inside lists) at: `src/superclaude/skills/sc-task-protocol/SKILL.md` (about lines 91, 106, 300, 315), `prd/SKILL.md` (222), `prd/refs/build-request-template.md` (100), `tdd/SKILL.md` (197, 215), `tdd/refs/build-request-template.md` (94), `task-builder/SKILL.md` (339, 1208), `roadmap/SKILL.md` (253, 491, 2537), `readme/SKILL.md` (239, 637), `tech-reference/SKILL.md` (227, 480), `tech-research/SKILL.md` (217, 454, 1621), `operational-guide/SKILL.md` (232, 610), `task/SKILL.md` (600), `confidence-check/SKILL.md` (50) and its drifted copy `plugins/superclaude/skills/confidence-check/SKILL.md` (48), `sc-crash-recovery/SKILL.md` (101, 146), `sc-crash-recovery/refs/pipelines.md` (49), `sc-crash-recovery/refs/investigators.md` (139, 141). The `sc-crash-recovery/SKILL.md:146` row "Auggie MCP unreachable" becomes "Codebase search unreachable (neither AUG nor `mcp__auggie__codebase-retrieval` answers)" with the same recovery action. Codegraph-only rows are unchanged.

Acceptance criteria:
- `grep -rn 'codebase-retrieval' <each file above>` shows every remaining mention paired with AUG on the same line.
- `uv run pytest tests/skills -v` passes; output saved to `./artifacts/t9-pytest.log`.

## Phase 4: Commands route to the proxy tools

## Task 10: Update command call sites and allow-lists

Design section 3.3 items 1-3. `src/superclaude/commands/validate-roadmap.md` line 6: same replacement as the validate-roadmap skill (`mcp__auggie-mcp__codebase-retrieval` becomes `mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval`). AUG phrase at `auggie-review.md` (about line 92), `brainstorm.md` (157), `recommend.md` (49) and `plugins/superclaude/commands/recommend.md` (its own line), `reflect.md` (157, 165) and `plugins/superclaude/commands/reflect.md` (about 146, 154), `troubleshoot.md` (90, 98). Context7/Tavily phrase at `reflect.md` (170, 171) and its plugin copy (about 159, 160), `troubleshoot.md` (100, 101). Codegraph rows unchanged.

Depends on: Task 6

Acceptance criteria:
- `grep -rn 'mcp__auggie-mcp__' src/superclaude/commands plugins/superclaude/commands` finds nothing.
- `uv run pytest tests/commands tests/skills/test_tier2_tavily_consistency.py -v` passes; output saved to `./artifacts/t10-pytest.log`.

## Task 11: Update `mcp-servers:` metadata in commands

Design section 3.3 items 4-5. Apply the metadata rule to the `mcp-servers:` line of these files in `src/superclaude/commands/`: `validate-roadmap.md` (7), `brainstorm.md` (6), `recommend.md` (6), `reflect.md` (6), `troubleshoot.md` (6), `issue.md` (7), `pr-submit.md` (6), `tdd.md` (7), `review-translation.md` (6), `cleanup-audit.md` (7), `explain.md` (6), `adversarial.md` (7), `cleanup.md` (6), `cli-eval.md` (6), `cli-portify.md` (7), `improve.md` (6), `index.md` (6), `release-split.md` (7), `spec-panel.md` (6), `tasklist.md` (7), `research.md` (6), `pm.md` (6), `task.md` (7); and to the plugin copies in `plugins/superclaude/commands/`: `brainstorm.md`, `recommend.md`, `reflect.md`, `explain.md`, `cleanup.md`, `improve.md`, `index.md`, `spec-panel.md`, `research.md`, `pm.md`, `task.md`. In `research.md`, `pm.md`, `task.md` keep `playwright` and `morphllm`. `build.md` and `test.md` are unchanged. `issue.md:7` becomes `[litellm, auggie, codegraph]`; update `tests/commands/test_issue_command.py` (about line 73) to expect it.

Acceptance criteria:
- Every listed metadata line names `litellm` first where it names `auggie`, `context7` or `tavily`; `build.md` and `test.md` are unchanged.
- `uv run pytest tests/commands -v` passes; output saved to `./artifacts/t11-pytest.log`.

## Phase 5: Core files, scripts and docs describe the proxy route

## Task 12: Update core framework files and templates

Design section 3.8. `src/superclaude/core/CLAUDE.md`: MCP table rows (about lines 20-24) only, as written in design 3.8 item 1; AUG short form at about lines 36, 41 and the refresh-tool row at about line 134 ("pushed code only; use Grep/codegraph for unsaved edits"). `src/superclaude/core/RULES.md` (about line 61) and `plugins/superclaude/core/RULES.md`: AUG short form, identical text. `src/superclaude/core/RESEARCH_CONFIG.md`: discovery wording at about lines 26, 33, 54 names `mcp__litellm__Tavily-*` through the proxy or `mcp__tavily__*` directly; line 61 pin unchanged; map/crawl names at about lines 93-94 get the proxy name first, and `tests/core/test_research_config.py` (about lines 82-83) also asserts the proxy names. `src/superclaude/mcp/MCP_Auggie.md` (about line 27): add a "Through the LiteLLM proxy" paragraph naming AUG, its parameters and pushed-code-only scope. `src/superclaude/mcp/MCP_Tavily.md` (about lines 42-45): add proxy names next to the direct names, with `mcp__litellm__Tavily-tavily_research` marked proxy-only. `src/superclaude/examples/deep_research_workflows.md` (about lines 434, 440, 458): Tavily phrase. `src/superclaude/templates/documents/skill_template.md` (about lines 249, 473): AUG short form. `src/superclaude/core/CODEGRAPH.md` unchanged. If `core/CLAUDE.md` shares a level-table copy check with `HOW-WE-WORK.md`, do not touch the level table.

Acceptance criteria:
- `cmp src/superclaude/core/RULES.md plugins/superclaude/core/RULES.md` reports identical files if they were identical before the edit (check `git show 0423fe5f` copies first; otherwise the edited line is identical in both).
- `uv run pytest tests/core -v` passes; output saved to `./artifacts/t12-pytest.log`.

## Task 13: Update comments and user docs

Design sections 3.7 item 2 and 3.9. `src/superclaude/cli/reflect/config.py` (about lines 162, 199): comment only; reword "so auggie stays indexed" to say the reviewer worktree is kept inside the repository so Grep and codegraph reach it. `docs/user-guide/mcp-servers.md`: AUG short form at about line 138; in the litellm section (about lines 148-159) add the served tool list and the AUG parameters and pushed-code-only note. `docs/user-guide/eval-pipeline.md` (about lines 263-265): add `mcp__litellm__` to the listed prefixes. `docs/user-guide/brainstorm.md` (17) and `docs/user-guide/commands.md` (784, 935): name AUG first, then `mcp__auggie__codebase-retrieval`, replacing `auggie-mcp`. `docs/guides/prd-skill-release-guide.md` (161, 434) and `docs/guides/tdd-skill-release-guide.md` (160, 441): AUG short form. Leave `docs/eval/validation-commands.md:84` (dated observed record), `docs/testing/` records and other bare-word docs unchanged.

Depends on: Task 2

Acceptance criteria:
- `git diff src/superclaude/cli/reflect/config.py` changes comment lines only.
- `uv run pytest tests -k "docs or reflect_config" -v` passes (or reports no tests selected, recorded); output saved to `./artifacts/t13-pytest.log`.

## Phase 6: Remove the broken stdio entry, guard the migration, roll out

## Task 14: Remove the repository `.mcp.json` auggie-mcp stdio entry

Design section 5. Precondition: the owner approved removal (owner question 2). If not approved when this task starts, make no change to `.mcp.json` or its test, write `./artifacts/t14-skipped.md` stating "skipped: owner decision 2 open", and finish the task. If approved: delete the repository root `.mcp.json` (its only entry is `auggie-mcp`, a stdio `auggie --mcp --mcp-auto-workspace` that fails with ENOENT where the `auggie` binary is absent) and rewrite `tests/cli/test_mcp_project_config.py` to assert that if `.mcp.json` exists at the repository root it has no `auggie-mcp` entry and no stdio entry whose `command` is `auggie`.

Acceptance criteria:
- Either `./artifacts/t14-skipped.md` exists and `git diff --quiet .mcp.json tests/cli/test_mcp_project_config.py` holds, or `.mcp.json` is deleted and `uv run pytest tests/cli/test_mcp_project_config.py -v` passes (output in `./artifacts/t14-pytest.log`).

## Task 15: Add the migration regression guard test

Design section 7 (new test). Create `tests/skills/test_mcp_proxy_names.py` that scans `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/commands`, `src/superclaude/core` and `plugins/superclaude/` and asserts: every line naming `mcp__auggie__codebase-retrieval`, other than lines in `freshness-*` hook scripts and `hooks.json`, also names `mcp__litellm__augment_code-augment_code_search` (in a `tools:`/`allowed-tools:` line, AUG must appear before it); every `tools:`/`allowed-tools:` line naming `mcp__tavily__tavily_<x>` also names `mcp__litellm__Tavily-tavily_<x>`; and no file outside `hooks.json` and `auggie-flag-clear.sh` names `mcp__auggie-mcp__`. Fix any call site the guard finds that Tasks 3-12 missed, applying the Constraints phrases.

Depends on: Task 3, Task 4, Task 5, Task 6, Task 7, Task 9, Task 10, Task 12

Acceptance criteria:
- `uv run pytest tests/skills/test_mcp_proxy_names.py -v` passes; temporarily removing AUG from one call site makes it fail (record both runs in `./artifacts/t15-guard.log`, then restore).

## Task 16: Sync dev copies, lint and run the affected suites

Design section 8. Run `make sync-dev`, then `make lint`, then `make verify-sync`, then `uv run pytest tests/agents tests/skills tests/commands tests/hooks tests/core tests/troubleshoot tests/cli -v`, then `make test`. Fix any failure caused by Tasks 1-15. Do not stage `.claude/` mirrors; stage `.dev/tasks` as always.

Depends on: Task 1, Task 2, Task 8, Task 11, Task 13, Task 14, Task 15

Acceptance criteria:
- `make lint` and `make verify-sync` exit 0; logs in `./artifacts/t16-lint.log` and `./artifacts/t16-verify-sync.log`.
- The listed pytest directories pass and the `make test` result (pass count, any failures with cause) is recorded in `./artifacts/t16-tests.log`; any pre-existing failure unrelated to this change is shown failing on 0423fe5f too.
- `git status --short .claude` shows no staged `.claude/` path.
