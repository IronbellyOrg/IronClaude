# Research: /sc:test recommendation accuracy

- **Topic type:** Command-specific routing review
- **Scope:** Six-month history, current command contract, recommendation surfaces, plugin mirrors, and regression coverage
- **Status:** Research complete; no implementation or test execution
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/test.txt`, worker `a6d63a2ee20aae52f`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The exact command has one reachable change in the requested window: commit `89df2c1105c01caff199288f949d5783f6594e70`, dated 2026-05-22, “chore: apply markdownlint MD022/MD031/MD032/MD034 auto-format repo-wide (#74).” Its actual patch adds blank lines and a final newline. It changes no flags, defaults, authorization boundaries, or testing capabilities. This command belongs in the inventory because formatting-only changes are included, not because it acquired new behavior. Evidence: the commit patch for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md`.

### Current command contract

[CODE-VERIFIED] `/sc:test` is self-contained Markdown guidance, not a dispatcher with a delegated protocol skill. Its usage accepts an optional target and `--type unit|integration|e2e|all`, `--coverage`, `--watch`, and `--fix`. These options appear in its Usage block, not in a flag table or frontmatter `argument-hint`. The no-argument example discovers and runs existing tests with standard configuration and basic coverage. There is no explicit default value for `--type` beyond that example. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:19-39,63-75`

[CODE-VERIFIED] The documented useful capabilities include framework/configuration discovery, coverage metrics, failure diagnostics, continuous watch mode, and Playwright-backed E2E browser testing. The E2E section additionally names cross-browser testing, visual validation, and performance metrics. These are documentation contracts, not capabilities independently demonstrated during this research. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:25-59`

[CODE-VERIFIED] Output comprises pass/fail summaries, coverage reports, quality metrics, diagnostics, and actionable recommendations. No fixed report filename, machine-readable return schema, persistent execution ledger, or resume procedure is specified. The watch example includes `--fix` and promises automatic simple failure fixes, so recommendation output must distinguish execution/reporting from authorized repair. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:47-52,63-100`

[CODE-VERIFIED] The boundaries explicitly exclude generating test cases, modifying test-framework configuration, running external-service-dependent tests without proper setup, and destructive test-file changes without explicit permission. Therefore `/sc:test` is not an implementation planner, test-generation tool, or blanket authorization to repair failures. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:94-106`

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide already routes “run tests” and “check coverage” to `/sc:test <path>`, mandates `--coverage`, and documents narrowing with `--type unit`, `integration`, or `e2e`. Its prose correctly states that the command does not write new tests. This core route should be preserved rather than replaced with implementation planning. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:170-173,319`

[CODE-CONTRADICTED] Recommendation flag verification is too restrictive for this command’s actual documentation layout. The skill requires mandatory flags to appear in a candidate’s “flag table or `argument-hint`”; the cold-path runbook repeats that restriction. But `/sc:test` declares its real flags in Usage and examples, with neither qualifying structure. Strict compliance can therefore discard the guide’s valid mandatory `--coverage` and incorrectly announce that the guide is outdated. This is a contract contradiction, not an observed runtime failure. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:234-237,335-337`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:200-202`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:19-23`

[CODE-VERIFIED] The guide’s testing row is narrower than the command’s documented triggers: it does not explicitly describe continuous watch operation or authorized simple repair. Its `changes_files: no` is accurate for ordinary execution/reporting but cannot describe a recommendation that adds `--fix` and permits repairs. The guide defines that field in terms of source, documentation, or Git changes, so this distinction is substantive. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:297,319`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:14-17,86-91`

[CODE-VERIFIED] Known failing-test diagnosis has an existing dedicated route through `/sc:troubleshoot`; the test command itself also promises failure diagnostics. These contracts support distinguishing “execute and report this suite” from “investigate this known failure,” rather than treating every mention of a failure as authorization to fix it. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:311`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:98-106`

[CODE-VERIFIED] Matched routing rows bypass cache lookup and cold-path write-back. Consequently, improving the existing testing row takes effect through guide-first routing without requiring a new test-specific classification key. Plugin installations also carry the guide and recommendation skill, and parity tests require the recommendation skill tree and bundled guide to mirror their canonical sources. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:50-65`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py:27-36`

### Proposed recommendation changes

[CODE-VERIFIED] **MUST: Accept explicitly documented Usage grammar as flag evidence.** Update candidate extraction and R1 in the recommendation skill, surface-enumeration reference, and cold-path runbook. Retain direct source verification and rejection of invented flags, but recognize a command’s Usage declaration alongside a flag table or `argument-hint`. This resolves the concrete `/sc:test` mismatch without modifying the test command solely to accommodate the router. Basis: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:19-23`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/surface-enumeration.md:54-60`

[CODE-VERIFIED] **SHOULD: Expand the existing testing route and section 3.8, not create another keyword table.** Explain watch mode, existing-suite E2E execution, optional target discovery, and the no-generation boundary. Preserve ordinary test execution as a supporting task. Grounded paste-ready examples are `/sc:test --coverage`, `/sc:test <target> --type integration --coverage`, and `/sc:test <target> --type e2e --coverage`. Add `--watch` only when requested, and never infer `--fix` from “run,” “check,” or “report.” Basis: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:19-23,63-91`

[CODE-VERIFIED] **MUST: Make repair authorization visible.** If the user explicitly requests simple automatic fixes, preserve that intent but label the resulting recommendation as potentially changing files. Do not attach `--fix` to the existing report-only route while leaving its mutation declaration unchanged. Larger repairs remain subject to the planning boundary. Basis: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/test.md:86-106`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:297,319`

[CODE-VERIFIED] **MUST, desired policy rather than current behavior: Separate test authoring from test execution without defaulting authoring to MDTM.** Section 3.8 currently sends test additions toward the feature/task-file workflow. Revise that handoff to use `/sc:workflow` plus `/sc:implement` for most planned test-authoring work; reserve task-builder plus `/task` for the most complex, long-running workloads or explicit MDTM inputs. File count, sessions, an existing spec, or auditability alone must not force MDTM. Basis for the current mismatch: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:173,305-307`

### Acceptance/regression scenarios

[CODE-VERIFIED] Add behavioral cases alongside the existing source-contract tests. Their current mandatory-flag check only establishes that a flag string occurs somewhere in command text; it does not exercise the skill’s stricter extraction language. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:286-304`

- Existing-suite coverage request retains `--coverage` without a false outdated-guide warning.
- No-target request does not acquire an invented directory.
- Watch-only request retains `--watch`, omits `--fix`, and does not become implementation planning.
- Existing E2E execution retains `--type e2e`; creating missing E2E tests does not route to `/sc:test`.
- Known-failure diagnosis uses the debugging route without assuming repair authorization.
- Explicit simple auto-fix request discloses possible mutations.
- Ordinary planned test additions prefer workflow/implement; explicit MDTM execution remains `/task`.
- Matched testing routes remain independent of cache contents, and plugin parity remains intact.

## Gaps

[UNVERIFIED] No test runner, browser session, or recommendation invocation was executed. This review establishes documentation and test-contract behavior only.

[CODE-VERIFIED] Searches found no literal `/sc:test` reference in the recommendation command, primary recommendation skill, its non-guide references, or classifier/runbook. Discovery depends on the governing guide and candidate enumeration, not a test-specific mapping.

[UNVERIFIED] The command does not define the size or scope of a “simple” automatic fix. Do not invent numerical repair guarantees.

## Key Takeaways

[CODE-VERIFIED] **CHANGE recommendation handling; NO CHANGE required for historical command behavior.** The six-month command change was formatting-only. The actionable issues are Usage-based flag verification, underdocumented watch/repair capabilities, mutation disclosure, and the test-authoring handoff.

- **MUST:** Fix flag-evidence extraction, preserve authorization boundaries, and align planned test authoring with the user’s workflow-first policy.
- **SHOULD:** Broaden the existing testing route and add behavioral regression cases.
- **NONE:** New classification keys, another fixed keyword table, a new test protocol skill, or claims of demonstrated runtime capability.
