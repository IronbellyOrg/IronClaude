# Summary: #512 [FEATURE] Add MCP servers to the skills and commands that lack them (audit findings and exact edits)

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/512
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`)
- Effort estimate: 12 hours

## What the issue asks for

Apply nine bounded MCP improvements across eleven existing source files: add codegraph guidance to repository indexing and documentation, repair task/PM/translation tool permissions, and name Tavily/Context7 tools in delegated research prompts. Preserve native-tool fallbacks, existing task tiers, unattended behavior, exact test strings and line-number references; update the codegraph adoption test list, then sync the development copies without staging `.claude/`. Do not change plugin copies, agents, the previously adopted analyze/design/implement/workflow primitives, or the separately identified follow-ups. All nine edit groups are still outstanding on current `origin/master`; the accuracy check found audit arithmetic and documentation inaccuracies, not implementation by PR #513.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/commands/index-repo.md` | E1: new codegraph metadata, one readiness check, structural/outline lookups and summary; retain both PROJECT_INDEX outputs and update mode. |
| `src/superclaude/commands/document.md` | E2: change empty metadata to codegraph; structural/signature/usage guidance above Read/Grep/Glob floor; preserve inline edits and unattended output accounting. |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` | E3: grant proxy/direct Augment and codegraph status; fresh/MCP-only downstream lookup. Three in-place lines; STRICT impact delegation stays unchanged. |
| `src/superclaude/skills/task-builder/SKILL.md` | E4: four in-place Tavily-first wording changes, including two identical investigation strings; retain WebSearch fallback and provenance. |
| `src/superclaude/skills/tech-research/SKILL.md` | E5: documentation-only metadata comment and exact shared Tools paragraph in the Web Research Agent prompt; do not narrow tool access. |
| `src/superclaude/commands/tdd.md` | E6: add Tavily to existing metadata; preserve command permissions and `> Skill tdd`. |
| `src/superclaude/skills/tdd/SKILL.md` | E6: documentation-only metadata comment. |
| `src/superclaude/skills/tdd/refs/agent-prompts.md` | E6: shared Tools paragraph in web-agent brief; preserve the em-dash no-conditional-pass literal. |
| `src/superclaude/skills/sc-review-translation-protocol/SKILL.md` | E7: grant Tavily search proxy/direct plus WebSearch, document metadata and delegated search/fallback; retain Inferred evidence fallback. |
| `src/superclaude/skills/sc-pm-protocol/SKILL.md` | E8: in-place Context7 resolve/query proxy/direct permission expansion only; preserve line-number citations. |
| `src/superclaude/skills/tech-reference/SKILL.md` | E9: metadata comment and same Tools paragraph for optional, gap-driven web research. |
| `tests/skills/test_codegraph_adoption.py` | Planned test edit: add index-repo/document to `_ISSUE_504_COMMANDS`; preserve task step-2 constraints and new PR #513 wording guards. |
| `tests/skills/test_mcp_proxy_names.py` | Proxy/direct names and allow-list pairing/order; capital `Tools:` avoids lowercase tool-declaration parsing. |
| `tests/skills/test_worker_contract.py` | Index outputs/location, document inline/unattended behavior, translation/TDD worker behavior, task-builder pinned text. |
| `tests/skills/test_review_severity_rule.py` | Severity/cap scanning and exact `Only PASS or FAIL — no conditional pass.` assertion, not the issue's hyphenated quotation. |
| `tests/skills/test_review_prompt_overrides.py` | Preserve no-minimum-count and review-prompt rules. |
| `tests/skills/test_model_alias_policy.py` | Listed regression coverage; no model field change is intended. |
| `tests/skills/test_task_builder_merge.py` | Existing task-builder structure and literal contracts; E4 anchors are outside these pins. |
| `tests/skills/test_primitive_dual_surface_lookup.py` | Preserve project/global agent lookup precedence in task-builder. |
| `tests/skills/test_sc_recommend_routing_contract.py` | References the untouched TDD build-request template. |
| `tests/agents/test_tavily_tool_parity.py` | E7's prose identifiers must exactly match the declared Tavily identifiers; rf agents must not gain map/crawl tools. |
| `tests/commands/test_impact_command.py` | Preserve STRICT impact Skill invocation, caller and fallback semantics. |
| `tests/commands/test_routing_plugin_parity.py` | Protect unrelated pinned plugin pairs; does not require changing index-repo/document twins. |
| `tests/core/test_how_we_work_routing_table.py` | Existing index-repo routing and tech-reference token coverage. |
| `tests/unit/test_cli_install.py` | Component and plugin inventory coverage. |
| `tests/recommend/test_routing_refresh.py` | Preserve the differently headed TDD Skill invocation and existing routing. |
| `tests/audit/test_hidden_input_guard.py` | Task-builder hidden-input/execution-context constraints. |
| `tests/skills/fixtures/review_severity_cap_edits.yaml` | Existing content anchors, including C-085..C-099 and C-104; leave review-loop wording untouched. |
| `tests/skills/fixtures/review_severity_sweep_edits.yaml` | Existing sweep anchors, including S-013 in the untouched TDD escalation template. |
| `src/superclaude/core/CODEGRAPH.md`; `plugins/superclaude/core/CODEGRAPH.md` | Shared readiness/fallback guidance and twin, clarified by PR #513. Reference-only dependencies, not E1-E9 edit targets. |
| `src/superclaude/agents/rf-task-builder.md`; `src/superclaude/agents/rf-task-researcher.md` | Reference-only tool declarations and Tavily-first rules; agents have no Context7 grant, explaining the excluded escalation changes. |
| `src/superclaude/skills/tdd/refs/build-request-template.md` | Explicitly untouched escalation prompt; naming Context7 here would exceed the builder's declared tools. |
| `src/superclaude/cli/recommend/prompts.py` | Cites sc-task-protocol lines 56-78; E3 must stay in place. |
| `docs/developer-guide/session-memory.md` | Cites sc-pm-protocol lines 52-54 and empty save/load metadata; retain those ranges and declarations. |
| `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`; `src/superclaude/templates/modularization-template-review/*`; `docs/developer-guide/review-severity-rule.md` | Shipped task-builder line-number references; E4 must add no lines. |
| `plugins/superclaude/commands/index-repo.md`; `plugins/superclaude/commands/document.md` | Existing non-identical companions to E1/E2, not parity-pinned; deliberately leave unchanged. |
| `plugins/superclaude/commands/load.md`; `plugins/superclaude/commands/spawn.md`; `plugins/superclaude/commands/business-panel.md`; `plugins/superclaude/skills/confidence-check/SKILL.md` | Other non-identical twins named in the issue's risk list; outside the nine edits. Load's missing checkpoint flag is a separate follow-up. |
| `plugins/superclaude/commands/pm.md` | Existing command twin; E8 edits only the source skill, which has no plugin twin. |
| `src/superclaude/commands/task.md`; `plugins/superclaude/commands/task.md` | Explicitly do not add codegraph metadata; existing tests forbid that adoption. |
| `src/superclaude/commands/analyze.md`; `src/superclaude/commands/design.md`; `src/superclaude/skills/sc-graph-protocol/SKILL.md`; `tests/core/test_codegraph_guide.py` | PR #513 changes outside the nine edit groups; do not mistake them for completed issue work. |
| `Makefile`; `.claude/commands/sc/`; `.claude/skills/` | sync-dev and verify-sync are implementation verification steps; `.claude/` output is not staged. No sync was run during this read-only check. |

## Analysis

- [Accuracy check](accuracy-check.md): checked `origin/master` at `930c5ebc813f594356f735c0fd3e0334a0e90279`, not the older local branch. One merged PR since issue creation, #513; no source-edit overlap with E1-E9. There is a direct test-file overlap and a shared-guide dependency.
- [Standard-depth static analysis](analysis/analyze-skills.md): all eleven edit targets and the affected test/fixture/line-reference dependencies. Codegraph and Auggie MCP tools were unavailable; inspection used repository tree/pattern lookup and immutable `git show` source reads. No tests or live MCP calls ran.
- Correct the bookkeeping before implementation: the 35 empty/missing files group into **30 items**, with 9 edited and **21 unchanged including the two dropped proposals**. Preserve nine empty fields, with document's current empty field as E2's explicit exception. The exact verdict literal uses an em dash. Two follow-up locations are not web-agent blocks and must not receive blind shared-paragraph insertions.
- Complexity uses the installed claim rubric, not file count alone. The 12-hour estimate fits the medium hour band, but the rubric's **more-than-one-subsystem** override makes this complex: repository indexing/documentation, task execution/impact checks, and delegated research/design/translation/PM workflows all change. These are prompt and permission declarations, not a data migration or runtime library replacement. No deep-depth analysis was requested or run.
- Effort breakdown: 2 hours for the written plan and corrected anchors; 3 for structural lookup/task changes; 3 for web prompts and permission alignment; 3 for targeted regression checks and any bounded fixes; 1 for sync verification and final scope review. Estimate: **12 hours**, not measured execution time. Actual live-tool availability and final test outcomes are **Not known yet**.
