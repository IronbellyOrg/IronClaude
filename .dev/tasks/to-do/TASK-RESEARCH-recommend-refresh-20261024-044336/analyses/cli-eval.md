# Research: /sc:cli-eval recommendation accuracy

- **Topic type:** Command-specific routing research
- **Scope:** Six-month history, current lifecycle contract, recommendation discovery, cache, plugin and regression consequences
- **Status:** Source analysis complete; no implementation or runtime evaluation performed
- **Date:** 2026-10-24

## Evidence index

All citations below use these absolute source paths.

- **C:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/cli-eval.md`
- **P:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md`
- **I:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md`
- **G:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`
- **R:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`
- **H:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py`
- **K:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py`
- **D:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py`
- **PG:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
- **TR:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py`
- **TG:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py`

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/cli-eval.txt`, worker `a8a4e989353322b0d`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Commit `0f6862b3`, dated 2026-06-12, introduced the command and its two lifecycle pipelines. Its patch introduced mandatory fresh-context loading, suite creation with critique and adversarial design, schema validation, interactive execution, monitoring and honest reporting. This was a substantive capability addition, not formatting. The current command retains those capabilities. Evidence: exact command and protocol patches from `git show 0f6862b3`; C:14-52, P:46-165.

[CODE-VERIFIED] Commit `3ae238b1`, dated 2026-09-30, changed the command’s MCP metadata from `[sequential, context7, serena]` to `[context7, serena]`. It did not change flags or lifecycle steps. This is a dependency-metadata change, not a new workflow or merely whitespace. Evidence: exact command patch from `git show 3ae238b1`; C:1-8.

[CODE-VERIFIED] Relevant delegated changes include `709a7ff1`, dated 2026-10-04, which redirected the suites guide to its moved location, and `5c6a7d91`, dated 2026-10-22, which changed integration-map primitive lookup to the installed commands directory. Neither expands the command’s public flags. Evidence: inspected patches for those commits; P:108-110, I:3-10.

### Current command contract

[CODE-VERIFIED] A required positional selector chooses `create` or `run`; omission stops execution for clarification. Creation accepts `--name`, `--from @<spec>` and `--agents`, with default advocates `opus,sonnet,haiku`. Run accepts optional `--suite` and `--eval`, defaulting to an interactive suite menu and all evals. `--eval` here identifies an eval, not recommendation-model evaluation. Evidence: C:14-39.

[CODE-VERIFIED] Both branches require fresh documentation, schema and CLI evidence before acting. Creation writes design artifacts, a suite manifest and documentation, optionally fixtures and callbacks. Completion requires successful schema loading and discovery through the CLI. Thus it is not simply a YAML-writing shortcut. Evidence: P:46-58, 72-110.

[CODE-VERIFIED] Run enumerates suites through the loader, supports drill-down, confirms the exact underlying invocation and safety choices, launches a monitored execution, and reports machine-readable outcomes plus forensic paths. It must distinguish skipped results and non-authoritative stubbed passes from genuine success. Recommendation must not describe run as read-only: it executes a real evaluation and produces artifacts. Evidence: P:122-165.

[CODE-VERIFIED] The public entry point activates `sc:cli-eval-protocol`. Its return contract includes pipeline, status, fresh-context status, suite, validation, run directory, outcomes and unresolved items. There is no documented resume selector in the public input contract. The integration reference specifically advises top-level creation because nested review fan-out can degrade inside a subagent. Evidence: C:67-73, P:183-208, I:62-67.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide and plugin copy reduce this capability to “write or run CLI evaluation suites” in **Other commands**. Neither gives creation and supervised execution separate routing rows. Generic rows instead cover implementation planning, existing features and running tests. Evidence: G:260-270, 303-319; PG:260-270.

[CODE-VERIFIED] This placement matters because recommendation consults Other commands only when no routing row matches. A matched row controls the answer and skips cache lookup and semantic ranking. Consequently, merely improving candidate enumeration cannot fix an eval request already captured by a generic tests or implementation row. This is a verified routing-contract weakness, not a demonstrated runtime misclassification. Evidence: R:50-60, 120-150; G:305-319 versus C:14-52.

[CODE-VERIFIED] The classifier has no CLI-evaluation lifecycle key. Unmatched requests can return `unknown` and reach the cold path, which remains a legitimate discovery route. Adding another fixed keyword routing table is unnecessary. Evidence: H:28-68; D:95-108.

[CODE-VERIFIED] Cache hits return an existing envelope after validating its single source file. Surface hashing includes guide contents, so changing the governing guide invalidates old surface fingerprints. It does not content-hash every protocol reference. Do not claim that a command-only cache row automatically detects all delegated-reference changes. Evidence: K:63-94; D:116-136.

[CODE-VERIFIED] Existing routing tests pin guide order, mandatory flags, hard limits and cache availability text. The guide tests explicitly require CLI-eval’s membership in Other commands. These checks do not establish correct create/run selection. Evidence: TR:1-8, 35-80; TG:26-40.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed policy:** Add specialized `cli-eval-create` and `cli-eval-run` rows to G’s existing routing table, with explanatory text in section 3.8. Match specifically authoring a cliEval suite versus selecting and supervising an existing suite. Their specificity should outrank generic testing and implementation intents under R’s existing matching rule. Do not create a second classifier mapping. Grounding: R:58-60; G:319; C:14-52.

[UNVERIFIED] **MUST, proposed policy:** Preserve the dedicated lifecycle handoff rather than prepending task-builder or decomposing creation into independent spec-panel, adversarial and document invocations. Creation already owns its design and validation sequence. The broader requested policy should favor workflow plus implement for ordinary planned code changes, reserving MDTM for exceptional complexity and duration; it must not replace this specialized command simply because creation touches multiple files. Grounding: P:72-110 versus G:305-307 and R:155-157.

[UNVERIFIED] **MUST, proposed output:** Use only verified public flags. Minimal paste-ready examples are `/sc:cli-eval create` and `/sc:cli-eval run`; when the user supplied the suite and eval, `/sc:cli-eval run --suite eval_smoke --eval ES1` is a source-backed example. Pass supplied seed paths through `--from`; never invent one. Underlying execution safety flags belong to the command’s confirmation stage, not fabricated slash-command options. Grounding: C:22-39, 60-64; P:135-153.

[UNVERIFIED] **SHOULD, proposed integration:** Update PG with the governing guide changes. Adjust TG’s Other commands requirement if CLI-eval moves into routed workflows. Retain missing-install handling rather than promising plugin-only users have the command. Add concise lifecycle guidance to the recommendation net-value reference only if needed, without copying protocol internals. Grounding: PG:260-270; TG:26-40; R:135-150.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed tests, grounded in C:14-39 and R:58-60:

1. “Create a cliEval suite from my design” selects `create`, not generic task-file generation.
2. “Run the eval_smoke suite and monitor ES1” selects `run`, preserving both supplied selectors.
3. “Run unit tests with coverage” remains generic testing.
4. An ambiguous “help with CLI evaluation” asks whether to create or run.
5. A specialized matched route bypasses a seeded, otherwise-valid generic cache hit.
6. Guide-only edits invalidate the cache fingerprint.
7. Missing plugin command is reported as not installed.
8. A direct request for an existing MDTM task still executes through `/task`, not this lifecycle.

## Gaps

[UNVERIFIED] No classifier or command was executed. Wrong-route frequency, model behavior and actual monitoring reliability remain unmeasured.

[CODE-VERIFIED] Targeted searches found no CLI-eval-specific references in recommendation’s command, skill, references, classifier or recommendation tests; the guide’s Other commands entry supplies its explicit discovery hint. Tracked-path inspection found no CLI-eval command/protocol plugin counterpart.

[UNVERIFIED] The public contract documents no resume mode. Do not invent checkpoint recovery or advertise generic workflow resume semantics for this command. Grounding: C:14-39.

## Key Takeaways

[CODE-VERIFIED] **CHANGE:** Discovery exists, but the guide understates the command and exposes it only after generic route matching fails. Evidence: G:270, R:54-60.

[UNVERIFIED] **MUST:** Add specialized create/run routing and behavioral regressions. **SHOULD:** Update plugin-guide parity and test assumptions. **NONE:** No command implementation, new public flag, fixed keyword table or automatic MDTM escalation is justified by this analysis.
