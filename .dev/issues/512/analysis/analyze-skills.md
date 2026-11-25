# Summary: #512 MCP primitive alignment — standard-depth static analysis

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/512
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`; multiple workflow subsystems)
- Effort estimate: 12 hours

## What the issue asks for

Align MCP tool declarations and bounded lookup instructions in nine edit groups spanning eleven Markdown source files, plus one adoption-test change. This static pass follows the installed `~/.claude/commands/sc/analyze.md` Discover → Scan → Evaluate → Recommend → Report flow with no `--depth` argument. It uses the issue-summary template's headings to carry the analysis input; the issue-protocol template directory supplies no dedicated analyze template. No source implementation, runtime testing or synchronization was performed.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/commands/index-repo.md` | E1; missing metadata and graph tier; stable index artifacts/output contract. |
| `src/superclaude/commands/document.md` | E2; empty metadata and manual structure/API/usage analysis; inline editing can invalidate graph rows. |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` | E3; missing Augment/status permissions and weaker readiness wording, with STRICT impact delegation already present. |
| `src/superclaude/skills/task-builder/SKILL.md` | E4; four line-preserving web-search changes and many shipped line citations. |
| `src/superclaude/skills/tech-research/SKILL.md` | E5; required web-agent phase with tool-unspecified brief. |
| `src/superclaude/commands/tdd.md`; `src/superclaude/skills/tdd/SKILL.md`; `src/superclaude/skills/tdd/refs/agent-prompts.md` | E6; metadata and actual delegated web-agent prompt must agree. |
| `src/superclaude/skills/sc-review-translation-protocol/SKILL.md` | E7; real-source requirement with no declared search tool. |
| `src/superclaude/skills/sc-pm-protocol/SKILL.md` | E8; Context7 steps with no corresponding tool grant. |
| `src/superclaude/skills/tech-reference/SKILL.md` | E9; optional gap-driven web-agent brief, same shared tool wording. |
| `tests/skills/test_codegraph_adoption.py` | Only intended test edit; current list is unchanged by #513, which appends other guards. |
| `src/superclaude/core/CODEGRAPH.md`; `plugins/superclaude/core/CODEGRAPH.md` | Current shared readiness/degradation contract, clarified by #513; reference-only. |
| `tests/skills/test_mcp_proxy_names.py`; `tests/agents/test_tavily_tool_parity.py` | Tool naming, pairing and declaration/body parity. |
| `tests/skills/test_worker_contract.py`; `tests/commands/test_impact_command.py` | Preserve outputs, unattended behavior and STRICT impact invocation. |
| `tests/skills/test_review_severity_rule.py`; `tests/skills/test_review_prompt_overrides.py`; `tests/skills/fixtures/review_severity_cap_edits.yaml`; `tests/skills/fixtures/review_severity_sweep_edits.yaml` | Exact review-rule literals and content-based fixture anchors. |
| `tests/skills/test_task_builder_merge.py`; `tests/audit/test_hidden_input_guard.py`; `tests/skills/test_primitive_dual_surface_lookup.py` | Preserve task-builder contracts and lookup precedence. |
| `tests/skills/test_model_alias_policy.py`; `tests/skills/test_sc_recommend_routing_contract.py`; `tests/recommend/test_routing_refresh.py`; `tests/core/test_how_we_work_routing_table.py`; `tests/unit/test_cli_install.py`; `tests/commands/test_routing_plugin_parity.py` | Remaining listed regression coverage and untouched-pair constraints. |
| `src/superclaude/cli/recommend/prompts.py`; `docs/developer-guide/session-memory.md`; `docs/developer-guide/review-severity-rule.md`; `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`; `src/superclaude/templates/modularization-template-review/*` | Existing line-number citations explain E3/E4/E8 in-place edits. |
| `src/superclaude/agents/rf-task-builder.md`; `src/superclaude/agents/rf-task-researcher.md`; `src/superclaude/skills/tdd/refs/build-request-template.md` | Agent tool boundaries explain why escalation-template edits were dropped. |
| `plugins/superclaude/commands/index-repo.md`; `plugins/superclaude/commands/document.md` | Non-identical companions, not required byte twins; leave unchanged. Other mirror exceptions are listed in the linked issue summary. |

## Analysis

### Discover and scan evidence

- Date supplied by session: 2026-11-12. `git fetch origin` completed. Baseline: `origin/master` commit `930c5ebc813f594356f735c0fd3e0334a0e90279`; local HEAD is `495eb96d19dffc2a5fef54695a8c9e178453dcb3` and was not used to judge current source claims.
- Checked the issue body and current empty comments array, scout, remote tree, all eleven source targets, cited tests and fixtures, line-reference consumers, agent declarations, mirror comparisons and PR #513's complete file list/diff. Also checked referenced issue states and PR #458/#511 status.
- Codegraph and Auggie MCP tools are not exposed in this worker's tool list. Used Glob/Read for protocol/templates and repository tree/pattern inspection plus immutable `git show` reads for current code. Markdown is explicitly not indexed by the project's codegraph guide in any case. No CLI graph status/init/index/sync was run.
- Inventory: 21 empty/missing skill entries (19 missing, 2 empty), 14 actual empty/missing command entries (6 missing, 8 empty). Ignore command README. Five skill/command pairs reduce 35 files to 30 audit items. TDD's configured command and agent-prompts reference are companion files outside that initial metadata filter.
- Change footprint: 9 edit groups, 11 source paths, 1 planned test path, no required plugin mirror changes. All old-text edit anchors still match at the checked commit. There is no evidence that #513 applied any of E1-E9.

### Evaluate: severity-rated findings

| Severity | Finding | Evidence and impact | Bounded recommendation |
|---|---|---|---|
| Medium | Task skill names unavailable-by-declaration tools | sc-task-protocol line 4 grants only graph callers/impact, but 91/106/315 name Augment and 107 requires graph availability. This can prevent the declared workflow from using its intended context/readiness tools. | E3's exact in-place allow-list and readiness changes; retain STRICT's impact Skill call at 95-98 and Grep/Read fallback. |
| Medium | PM and translation declarations do not match their own lookup work | sc-pm-protocol lines 70/111/126 name Context7, absent at line 4. Translation lines 124-149 require sources, but line 4 grants no search tool; line 222 supplies the Inferred floor. | E7/E8, keeping proxy/direct names and search fallback precise. Do not add unrelated tools. |
| Medium | Delegated web briefs omit the tool selection required by their workflows | task-builder:643,949,1209,1885; tech-research:740-777; TDD agent-prompts:106-130; tech-reference:725-748. Generic subagents receive search goals but no consistent provider/fallback instruction. | E4/E5/E6/E9; use one identical shared Tools paragraph where specified and retain WebSearch/WebFetch floor. Do not narrow unrestricted skills with a new allow-list. |
| Low | Indexing and document workflows lack the intended structural graph tier | index-repo:17-68 and document:28-48 still use manual discovery. Incorrect signatures/exports can propagate into generated reference material. | E1/E2 with fresh+MCP-only checks, native floors and confirmed citations. Reuse current shared guide's readiness/degradation rules. |
| Low | Audit item arithmetic is wrong | 35 initial files minus five paired reductions = 30 items, not 31. Listed decisions give 9 edits + 19 KEEP NONE + 2 DROP = 30. | Describe 21 unchanged items including the two drops. Do not expand the feature to make the count fit. |
| Low | “keep every existing []” conflicts with E2 | Ten current empty fields include document, whose field E2 intentionally changes. | Preserve the other nine; document is the explicit exception. |
| Low | Exact test-string quotation is wrong | review-severity test line 344 requires `Only PASS or FAIL — no conditional pass.`, not the issue's ASCII-hyphen version. | Keep the current em-dash literal byte-for-byte. |
| Low | Two deferred follow-up anchors are not equivalent web-agent prompts | operational-guide:824 belongs to consolidation, and skill_template:474 is an escalation instruction; neither is the shared web-agent block. | Correct the follow-up description only; no extra scope in this issue. |
| Low | Scout overstates source overlap with #513 | The merge changed analyze/design/graph-protocol/core-guide, none named by E1-E9. It also changed the adoption test that this issue will edit. | Keep the eleven original targets; account for new appended test guards and current shared-guide wording without reopening excluded work. |

These are static workflow/declaration findings, not observed live-tool failures. Actual tool execution, denial behavior and downstream document quality are **Not known yet**.

### Quality and compatibility constraints

1. E3/E4/E8 must preserve line count: recommend's classifier cites task-protocol 56-78, session-memory cites PM 52-54, and reflect/modularization/review documentation cites task-builder ranges. E4 has exactly two investigation-string replacements and one each of the remaining strings.
2. E1 must preserve Output Format's root-of-repository wording and both index filenames. E2 must preserve inline file accounting. E6 must preserve `> Skill tdd`; its build-request template is not part of the change.
3. Declaration/body Tavily identifiers must match in E7. Capital `Tools:` is intentionally prose rather than a new tool-declaration field. Naming a tool in a delegated prompt does not prove that the current session exposes it; fallback text remains necessary.
4. Current guide includes one readiness check, fresh+MCP gate, bounded init/index wait where permitted, timestamp even if status is skipped, empty/truncated handling, and scoped `path` when a target is narrower than the repo. E1 is whole-repository indexing, so its unscoped files overview does not itself contradict the scoped-target rule.
5. No runtime metadata consumer was found for the literal `mcp-servers` key. Metadata alone is not a permission repair; E3/E7/E8 need actual allow-list changes. The live Claude permission system was not audited.

### Security and performance

- No data migration, credential handling or runtime package implementation is proposed. Intended grants are limited to read/search capabilities already named by each workflow. This is not a proof that external research is safe for every input; private project details must not be sent unnecessarily.
- One graph readiness check and the native fallback bound the proposed integration. No performance benchmark was run; ROI rankings and token savings are not newly measured facts.
- No source, plugin, configuration or task-package files were modified, staged or committed by this pass. The only git write was the allowed origin fetch.

### Recommend and verification roadmap

Use a written implementation plan, not a direct multi-file edit. Keep the issue's four bounded groups: E1/E2 with the test-list addition; E3; E4/E5/E6/E9; E7/E8. Reconcile the audit inconsistencies without changing those nine groups, then preserve all existing pins and native floors during implementation.

Run the issue's listed targeted regression files during implementation, with additional trap tests for task-builder merge, hidden inputs, dual-surface lookup, routing and install inventories where affected. Run sync-dev and verify-sync only in the implementation checkout after source changes; do not stage `.claude/` or edit the non-identical plugin companions. All test outcomes and sync outcomes are **Not known yet** because this pass did not run them.

Estimate: 12 hours (2 planning/correction, 3 structural/task, 3 web prompts/permissions, 3 regression/fixes, 1 sync/scope review). Complex follows the rubric's multi-subsystem override, not the number of Markdown files; no deep-depth pass was run despite that classification because this job expressly requested no `--depth` argument.

### Related analysis inputs

- [Accuracy check](../accuracy-check.md)
- [Issue summary and complete file cheatsheet](../issue-summary.md)
