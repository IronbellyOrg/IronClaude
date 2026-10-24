# Research: /sc:validate-tests recommendation refresh

- **Topic type:** Command routing contract research
- **Scope:** Six-month command history, current validator contract, recommendation discovery, cache, plugin, hook, and regression surfaces
- **Status:** Complete, returned as text; no report file written because developer instructions prohibit report Markdown writes
- **Date:** 2026-10-24

## Evidence sources

Citation labels below identify these absolute paths; numbers following labels are source lines.

- **C:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/validate-tests.md`
- **V:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-validate-tests-protocol/SKILL.md`
- **G:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`
- **R:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`
- **P:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py`
- **K:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py`
- **H:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh`
- **T:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py`
- **L:** `/config/.claude/skills/sc-recommend-protocol/SKILL.md`

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/validate-tests.complete.txt`, worker `aeaa97ba408d47895`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Two commits touched the command or its delegated protocol in the inventory window, 2026-04-24 through 2026-10-24. Commit `89df2c1105c01caff199288f949d5783f6594e70`, dated 2026-05-22, inserted blank lines around headings, code fences, and lists in both files. The inspected patch contains formatting changes only. It did not add flags, categories, execution modes, or new routing behavior. Evidence: exact `git show` patch for C and V.

[CODE-VERIFIED] Commit `3ae238b178fb7c67ca02809d24745de620c2bd50`, dated 2026-09-30, removed only `mcp-servers: [sequential]` from command frontmatter. This removes obsolete dependency metadata, not validator functionality. Recommendations must not require Sequential MCP for this command. Evidence: exact `git show` patch for C.

### Current command contract

[CODE-VERIFIED] This is contributor-facing behavioral validation of `/sc:task` tier classification against YAML expectations, not a general application-test runner. Input is a test specification file or directory, with a documented default of `tests/sc-task/`. Its report compares tier, confidence, and flags. The command delegates through `Skill sc:validate-tests-protocol`; recommendation output should invoke the outer command rather than reproduce classification rules. Evidence: C:22-33, C:51-56, C:109-115.

[CODE-VERIFIED] Useful options are `--all`, `--verbose`, `--summary`, `--category`, `--stop-on-fail`, and `--report`. Summary is the default. Categories include classification, verification routing, compound phrases, context boosters, command comparison, edge cases, and integration. These category names describe this specialized YAML suite, not application integration testing. Evidence: C:24-33, C:58-68; V:54-64.

[CODE-VERIFIED] Outputs include summary counts, category results, failure details, optional classification traces, and suggested configuration adjustments. Expectations can cover tier, confidence ranges, confirmation flags, matched keywords, and compound phrases. This is an interpreted behavioral contract; reading its prose does not establish that a test runner or 300-case suite executed successfully. Evidence: V:275-298, V:302-377.

[CODE-VERIFIED] Validation does not authorize editing test specifications or changing classification logic. The protocol explicitly excludes automatic test-file changes, configuration updates without approval, and actual code changes during validation. No resumable ledger, checkpoint workflow, or automatic implementation handoff is specified. Evidence: C:125-129; V:426-458.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The current guide already identifies the command correctly: “IronClaude contributors: test `/sc:task` tier rules.” However, this appears only in the “Other commands” block. Recommendation consults that block only when no routing row matches. Its general `tests` row matches “run tests; check coverage” and selects `/sc:test <path> --coverage`. Consequently, an overlapping request can reach the generic route before the specialized candidate participates in discovery. This is a contract-level overlap, not a demonstrated runtime misclassification. Evidence on both sides: G:285, G:319; R:54-60.

[CODE-VERIFIED] The existing specificity rule resolves overlapping routing rows in favor of the row naming the more specific artifact. It cannot directly resolve this particular overlap because the specialized validator currently has no routing row. Evidence: R:58-60 versus G:285 and G:301-325.

[CODE-VERIFIED] Cache behavior matters only after guide matching. A matched row bypasses both cache lookup and cold-path write-back. Without a matching row, the classifier has no tier-validation key; its contract requires `unknown` when no enum entry fits. The cold worker receives “Other commands” and can then discover the validator. This is a supported fallback, not a reason to add another fixed keyword table or an unnecessary cache category. Evidence: R:54-65; P:50-68, P:125-131.

[CODE-VERIFIED] Guide edits are included by content in the surface fingerprint, whereas ordinary command, skill, and agent enumeration contributes paths. Thus updating the governing guide naturally invalidates checkout cache rows. Do not claim this also validates external YAML fixture contents. Evidence: K:63-103.

[CODE-VERIFIED] Checkout precedence selects source copies before potentially older installed copies. Outside a checkout, project copies precede installed and plugin copies. This matters because a globally installed legacy recommendation protocol still exists, despite the tracked legacy directory being absent. That installed file retains language detection, a fixed keyword table, and old flags; it is not authoritative for the current command. Evidence: R:41-46, R:112; L:11-44; negative tracked-path inspection recorded below.

[CODE-VERIFIED] The recommendation hook is advisory, fail-open context injection, not proof that discovery or candidate verification occurred. Its own comments explicitly state this. The validator must therefore remain correct through guide and recommendation contracts, not a claim that the hook mechanically prevents bad routing. Evidence: H:4-19.

### Proposed recommendation changes

[CODE-VERIFIED] **MUST, proposed policy:** Preserve this specialized report-only route. In G’s existing routing table, add a supporting row for validating `/sc:task` compliance-tier behavior against YAML specifications. Use level `-`, `changes_files: no`, and `/sc:validate-tests <verified YAML target>`. Narrow the generic `tests` row to application test execution and coverage, excluding the specialized tier-validation situation. This uses the existing authoritative table and its specificity rule, not an additional keyword router. Evidence supporting the proposal: C:22-33, C:51-56; G:297-319; R:58-60.

[CODE-VERIFIED] **MUST, proposed safeguard:** Before emitting a runnable validator invocation, verify the requested/default YAML target exists. If it does not, identify the missing prerequisite and ask for the intended suite instead of promising results or silently switching to `/sc:test`. Preserve user-selected verbosity, category, early-stop behavior, and report destination. Evidence: C:22-33; V:275-298.

[CODE-VERIFIED] **SHOULD, example contract:** After resolving a real suite path from the request, emit `/sc:validate-tests <verified YAML target> --verbose --stop-on-fail` when the user asks for detailed, first-failure diagnosis. This is a grounded invocation template, not an executable example with an invented file. Do not append `/sc:test` options such as `--coverage` or `--fix`. Evidence: C:24-33.

[CODE-VERIFIED] **SHOULD, plugin and tests:** Mirror the revised guide into `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Add routing regressions rather than extending the classifier enum solely for this command. Existing tests verify the other-command entry and valid flags, but do not establish semantic routing correctness for competing requests. Evidence: plugin guide:285; T:275-304.

[UNVERIFIED] Any subsequent classification-rule implementation should follow the user’s proposed workflow-first policy, with MDTM reserved for the most complex, long-running workloads. That policy is separate from current guide wording and does not justify automatically turning a validation request into implementation work. Current G:305-308 still applies broader MDTM triggers.

### Acceptance/regression scenarios

[CODE-VERIFIED] Proposed regression cases grounded in the contracts:

1. “Validate `/sc:task` tier expectations in this YAML file” selects the specialized command, not application coverage testing.
2. “Run application unit tests and check coverage” retains the general tests route.
3. A missing default suite produces a prerequisite explanation, never “300 tests passed.”
4. Requested verbose output, category selection, first-failure stopping, and report path survive unchanged.
5. Validation failures return findings without editing specifications or configuration.
6. A matched specialized row bypasses a preseeded unrelated cache recommendation.
7. A plugin-only installation missing the command reports it as unavailable rather than presenting a runnable step.

Evidence: C:22-33, C:125-129; R:60, R:135; V:443-458; G:319.

## Gaps

[CODE-VERIFIED] Direct filesystem inspection found no default `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/sc-task/` directory. Exact tracked-path inspection likewise returned no files for that suite, the legacy source protocol directory, or validator command/protocol plugin mirrors. The plugin guide nevertheless advertises the validator.

[UNVERIFIED] Actual classification accuracy, fixture count, report-writing success, and parity with current `/sc:task` classification were not executed or established. The source’s illustrative 300-test results must not become verified capability claims.

[UNVERIFIED] The generic-route overlap is supported by contract ordering, but no live recommendation invocation was run. Activation-name resolution and missing-fixture recovery behavior remain untested.

## Key Takeaways

[CODE-VERIFIED] **CHANGE:** Clarify specialized tier-validation routing and verify YAML prerequisites. The current label is accurate; neither formatting history nor removed MCP metadata warrants inventing new capability.

[CODE-VERIFIED] **MUST:** Protect specialized validation from generic test routing, missing-suite success claims, and unauthorized remediation. **SHOULD:** Add contrasting routing regressions and synchronize the plugin guide. **NONE:** No new keyword table, dedicated cache key, Sequential dependency, automatic MDTM handoff, or validator implementation change is required by this research.
