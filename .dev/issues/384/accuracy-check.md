## Accuracy check for #384

**Verdict:** out_of_date

Checked against `origin/master` at 38eb3c58afe6988b51060ae14117172869ea4c1e, and the pull requests merged since the issue was opened (0, list truncated: no).

Every file:line the issue cites still matches today's code; no line has drifted. The issue is out of date for two other reasons: (1) the body's open decisions ("Not known yet" mapping, fallback and Python scope) were settled by the two owner comments of 2026-11-05, so the body's acceptance criteria and "inclusion is an owner decision" wording no longer describe the work; (2) with the Python package now in scope, the "Components Affected" list misses many hard-coded aliases (rows 25-40 below). A deep `/sc:analyze` pass is saved at `.dev/issues/384/analysis/analyze-superclaude.md`.

| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |
|---|---|---|---|
| 1 | "In the inspected workspace `haiku` resolves to `glm-5.3`" (`refs/tiers.md:21-26`) | still true | `src/superclaude/skills/sc-issue-protocol/refs/tiers.md:26`; this workspace's env has `ANTHROPIC_DEFAULT_HAIKU_MODEL=glm-5.3` |
| 2 | "Brainstorm currently defaults to the three Claude Code aliases" (`commands/brainstorm.md:56`) | still true | `src/superclaude/commands/brainstorm.md:37,56` (`--models opus,sonnet,haiku`); also `:81,:152` |
| 3 | "the issue workflow explicitly avoids `haiku` with `--models opus,sonnet`" (`refs/chains.md:21`) | still true | `src/superclaude/skills/sc-issue-protocol/refs/chains.md:21`; the rows that pass it are `:11-13` |
| 4 | "The Auggie review skill rejects gateway aliases for its `--revagent` option" (`sc-auggie-review-protocol/SKILL.md:83-89`) | still true | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:84-89`, also `:112,:380-381`; the command repeats it at `src/superclaude/commands/auggie-review.md:8,41-42,57` |
| 5 | "existing issue-worker frontmatter pattern" (`issue-worker-t1.md:6`, `-t2.md:6`, `-t3.md:6`) | still true | `src/superclaude/agents/issue-worker-t1.md:6` (`claude-gw-tier1a`), `issue-worker-t2.md:6` (`claude-gw-tier2`), `issue-worker-t3.md:6` (`claude-gw-tier3`) |
| 6 | "The Agent call's model parameter only accepts the documented aliases and overrides frontmatter" (`refs/tiers.md:21-28`) | still true | `src/superclaude/skills/sc-issue-protocol/refs/tiers.md:23-28` |
| 7 | "the sprint summarizer's deliberate `sonnet` alias and proxy routing" (`sprint/summarizer.py:47-51`) | still true | `src/superclaude/cli/sprint/summarizer.py:47-51` (`SONNET_MODEL = "sonnet"`), used at `:330-331` |
| 8 | "Mapping from each existing `opus`, `sonnet` or `haiku` use to a ccsession tier: Not known yet" | changed | Owner comments 2026-11-05: inside a ccsession workspace opus = `tier1a` (`claude-gw-tier1a`), sonnet = `tier1b` (`claude-gw-tier1b`), haiku = `tier2` (`claude-gw-tier2`) |
| 9 | "Picker IDs may not be served outside a ccsession tier workspace; existing issue workers stop without an alias fallback" (`refs/tiers.md:32-40`) | still true | `src/superclaude/skills/sc-issue-protocol/refs/tiers.md:32-40` |
| 10 | "Fallback or failure behavior for them: Not known yet" | changed | Owner comment 2026-11-05: outside a ccsession workspace fall back to plain `opus`, `sonnet`, `haiku` |
| 11 | Acceptance criterion: "The owner-approved mapping and the decision about adjacent Python CLI code are documented. Both are Not known yet." | changed | Both decided in the owner comments; Python package code is in scope |
| 12 | "Adjacent Python package code, not installed primitives; inclusion is an owner decision" | changed | Owner comment 2026-11-05: Python package code is in scope |
| 13 | "Tests pin ... following the existing issue-worker test pattern" (`tests/skills/test_issue_worker_agents.py:21-24`) | still true | `tests/skills/test_issue_worker_agents.py:21-25` (`WORKERS` dict; closing brace on `:25`) |
| 14 | "ccsession profiles or tier definitions" (`ccsession-tag/ccsession-models.json:4-121`) | still true | `profiles` at `:4-69`, `tiers` at `:70-121`; `tier1a` `:78`, `tier1b` `:85`, `tier2` `:93`; no plain `tier1` |
| 15 | "which models belong to a tier" (`ccsession-tag/MODEL-TIERS.md:35-42`) | still true | `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:35-42` |
| 16 | Agent frontmatter `model: sonnet` in 11 agents (audit-comparator, audit-validator, audit-analyzer, audit-scanner, audit-consolidator `:5`; evidence-validator, reflect-reviewer, confidence-calibrator, reuse-auditor, eval-docs-loader, eval-run-reporter `:6`) | still true | `grep '^model:' src/superclaude/agents` returns exactly these 11 at the cited lines |
| 17 | `model: opus` in `eval-suite-author.md:6`, `auggie-reviewer.md:6` | still true | same grep |
| 18 | Skill frontmatter `sc-bare-review/SKILL.md:5` | still true | `src/superclaude/skills/sc-bare-review/SKILL.md:5` (`model: sonnet`) |
| 19 | `sc-brainstorm-protocol/SKILL.md:49,102,109,219,407` | still true | same lines; the issue missed `:221` and `:245` and `refs/agent-spec-builder.md:57-73,109-119,165-168` |
| 20 | `commands/cli-eval.md:22,37`; `sc-cli-eval-protocol/SKILL.md:43` | still true | same lines; missed `sc-cli-eval-protocol/SKILL.md:5` and `refs/integration-map.md:40` |
| 21 | `commands/validate-roadmap.md:31,57`; `sc-validate-roadmap-protocol/SKILL.md:364,495` | still true | same lines; missed `validate-roadmap.md:52,56` |
| 22 | `sc-recommend/SKILL.md:73`; `commands/recommend.md:35`; `commands/troubleshoot.md:55` | still true | same lines; missed `sc-recommend/SKILL.md:332-334` (eval fan-out per model) and `sc-troubleshoot-protocol/SKILL.md:411` |
| 23 | `sc-adversarial-protocol/SKILL.md:76,581,963,1968`; `sc-roadmap-protocol/refs/adversarial-integration.md:137-146` | still true | same lines; the dispatch site that uses the parsed model is `sc-adversarial-protocol/SKILL.md:1022` |
| 24 | `ccsession-tag/models.py:331-338,843-855`; `MODEL-TIERS.md:8-11`; `ccsession-models.json:4-172`; `roadmap/models.py:104-105,151-152`; `roadmap/executor.py:3680-3684`; `recommend/eval_aggregate.py:15-20`; `reflect/runner.py:287-288` | still true | all at the cited lines; `models.py:855` prints `PROFILE_MODEL=claude-gw-<tier>[1m]` |
| 25 | Not in the issue: reflect CLI default model | missed | `src/superclaude/cli/reflect/commands.py:31` `_DEFAULT_MODEL = "claude-opus-4-8"` (a full model id, not even an alias), used at `:359` |
| 26 | Not in the issue: roadmap CLI option defaults | missed | `src/superclaude/cli/roadmap/commands.py:41` (help: `opus:architect,sonnet:architect`), `:434` (`default="opus:architect"` for `roadmap validate`) |
| 27 | Not in the issue: sprint alias rotation | missed | `src/superclaude/cli/sprint/aienv.py:43-47` (`_ANTHROPIC_SLOTS` -> `opus`/`sonnet`/`haiku`) |
| 28 | Not in the issue: recommend CLI help | missed | `src/superclaude/cli/recommend/commands.py:207` |
| 29 | Not in the issue: installed user settings default | missed | `src/superclaude/cli/user_settings_defaults.json:3` (`"model": "opus[1m]"`), read by `src/superclaude/cli/install_user_setup.py:157,312` |
| 30 | Not in the issue: eval suites | missed | `src/superclaude/cli/eval/suites/frontier_vs_cheap_combo.yaml:85-86,146-147,214-215,281-282`; `adversarial_merge_consistency.yaml:149-157,265-273,386-394`; `model_capability_matrix.yaml:81-383` (`--agents opus,sonnet,haiku`) |
| 31 | Not in the issue: release-split defaults | missed | `src/superclaude/commands/release-split.md:41,45,60,97`; `skills/sc-release-split-protocol/SKILL.md:92,194`; `refs/adversarial-integration.md:32-39` |
| 32 | Not in the issue: roadmap command and skill defaults | missed | `src/superclaude/commands/roadmap.md:26,72`; `skills/sc-roadmap-protocol/SKILL.md:75,146` |
| 33 | Not in the issue: adversarial command examples and agent-spec ref | missed | `src/superclaude/commands/adversarial.md:29,90,112,120,126`; `skills/sc-adversarial-protocol/refs/agent-specs.md:25-27,53-55,80-89` |
| 34 | Not in the issue: implement retry model ladder | missed | `src/superclaude/skills/sc-implement-protocol/refs/retry.md:162-179` (fallback ladder `haiku`/`sonnet`/`opus`). Its primary ladder names `T1_Model01`-style variables, but this workspace exports `T1Model01`/`T1aModel01` (no underscore), so in practice the alias fallback ladder is always the active one |
| 35 | Not in the issue: reflect reviewer rotation and calibrator | missed | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:33,601-605,1169,1337-1339`; `refs/reviewer-spec.md:96-108`; `refs/reflection-rubric.md:139-167` |
| 36 | Not in the issue: prose model guidance in agents and cleanup-audit | missed | `src/superclaude/agents/debate-orchestrator.md:21`, `merge-executor.md:21`; `skills/sc-cleanup-audit-protocol/SKILL.md:68,74,95,99` and `commands/cleanup-audit.md:43,53` say `audit-scanner` runs on Haiku, but `agents/audit-scanner.md:5` pins `sonnet` |
| 37 | Not in the issue: task-builder executor class | missed | `src/superclaude/skills/task-builder/SKILL.md:1088,2170` (`executor_model_class`, e.g. `sonnet`) |
| 38 | Not in the issue: plugin mirror | missed | `plugins/superclaude/commands/brainstorm.md`, `plugins/superclaude/commands/recommend.md`, `plugins/superclaude/skills/sc-recommend/SKILL.md`, `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md` carry the same aliases |
| 39 | Not in the issue: tests that pin today's aliases | missed | e.g. `tests/commands/test_auggie_review_revagent.py`, `tests/recommend/test_eval_pipeline.py`, `tests/recommend/test_best_model.py`, `tests/sprint/test_aienv.py`, `tests/roadmap/test_resume_restore.py`, `tests/roadmap/test_cli_contract.py`, `tests/roadmap/test_models.py`, `tests/skills/test_implement_adviser_family.py` |
| 40 | Not in the issue: docs | missed | `docs/user-guide/commands.md`, `docs/user-guide/brainstorm.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` |

### Merged pull requests that touch this issue

| PR | Title | Relevant files | Effect on the issue |
|---|---|---|---|
| none | No pull requests merged since the issue was created (2026-11-05T03:22:29Z); `origin/master` is still 38eb3c58 | none | none |

<!-- sc:issue:accuracy-check -->
