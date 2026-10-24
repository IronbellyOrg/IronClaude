# Research: Retired `/sc:task-mcp`

- **Topic type:** Command retirement and recommendation safety
- **Scope:** Six-month history through 2026-10-24; current recommendation, migration, cache, plugin and test contracts
- **Status:** Research complete; no files changed or tests executed
- **Date:** 2026-10-24
- **Intended persistence path:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/analyses/task-mcp.md`

## Evidence paths

All numbered citations below refer to these absolute paths.

| ID | Path |
|---|---|
| E1 | `/config/.claude/commands/sc/task-mcp.md` |
| E2 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/task.md` |
| E3 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-task-protocol/SKILL.md` |
| E4 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md` |
| E5 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/surface-enumeration.md` |
| E6 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py` |
| E7 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py` |
| E8 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py` |
| E9 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md` |
| E10 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py` |
| E11 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh` |
| E12 | `/config/.claude/skills/sc-recommend-protocol/SKILL.md` |
| E13 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/workflow.md` |
| E14 | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/implement.md` |

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/task-mcp.txt`, worker `a99b1518c03d41915`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Exact-path history within the inventory window contains one change: commit `86d27496456d6b82ff38af6ebc364ec9d5d7c9b4`, dated 2026-05-12, deleted all 375 lines of `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/task-mcp.md`. The commit explicitly describes clearing pre-existing branch-state deletions. This is substantive retirement, not a formatting update. Its deleted frontmatter already marked the command deprecated and directed migration to `/sc:task --compliance [tier]`. Evidence: exact-path `git log` and `git show` for that commit.

[CODE-VERIFIED] The historical document contained competing naming signals: `deprecated_by: "task-unified"` but migration examples targeting `/sc:task`. Current task explicitly forbids using deprecated task-mcp, and its live protocol says one command replaces the earlier confusion. Recommendation must verify the current target rather than mechanically trust `deprecated_by`. (E2:178-186; E3:15-24; deletion patch, lines 1-17 and migration section.)

### Current command contract

[CODE-VERIFIED] There is no current tracked task-mcp command to invoke, no current activation target, and no supported current handoff or resume contract. However, an installed leftover exists at E1. It is self-contained prose, accepting a task description, default automatic tier selection, `--tier`, `--skip-mcp`, and `--force-strict`. Its historical purpose was executing and verifying changes, not writing a plan or producing a report only. These are legacy capabilities, not current supported recommendations. (E1:1-48, 54-110.)

[CODE-VERIFIED] The supported migration family is `/sc:task`, with separate strategy and compliance dimensions. STANDARD and STRICT execution loads context, makes changes and verifies results; STRICT includes delegated verification. This is direct execution, unlike `/sc:workflow`, which plans without changing product code. No legacy authorization or escape-hatch behavior should be imported automatically. (E2:14-25, 95-102; E3:82-105; E13:63-80.)

### Comparison with recommendation surfaces

[CODE-VERIFIED] **Source retirement is insufficient to prevent rediscovery.** Recommendation enumerates installed, project, plugin and checkout surfaces. Checkout preference only resolves same-name duplicates. When task-mcp exists only in the installed folder, there is no same-name checkout file to override it. Candidate verification extracts flags, inputs, activation and return contract, but does not explicitly reject `deprecated: true`. The reference likewise treats a resolved source as eligible without a retirement check. (E1:8-16; E4:100-135; E5:15-25, 54-67.)

[CODE-VERIFIED] The cold worker repeats this gap: it enumerates all surfaces and excludes missing candidates, but defines no deprecated-candidate rule. A fix confined to the parent skill would therefore leave its delegated execution contract incomplete. (E6:125-148.)

[CODE-VERIFIED] The warm cache is also relevant. Dispatch checks source existence and matching source bytes before returning the stored envelope; it does not interpret deprecation metadata. Consequently, an otherwise valid cached row pointing to the installed retired command is not rejected by this code merely because that command is deprecated. Surface hashing tracks candidate paths and guide contents, not all candidate bodies or recommendation-policy prose. A guide edit invalidates old rows; adding only a prose eligibility rule does not necessarily do so. These are code-path observations, not executed reproductions. (E7:63-94; E8:103-137.)

[CODE-VERIFIED] The governing guide already omits task-mcp and routes small direct changes to `/sc:task`. Its broader planned-work boundary remains contrary to the requested policy: `task-file` matches many files, more than one session, or “must not drift”; `feature-existing` directly selects task-builder. The parent skill and cold runbook repeat “larger, longer, or riskier” as the level-4 boundary. Migration from task-mcp must not become another route that bypasses written planning or reflexively escalates to MDTM. (E9:303-308; E4:154-157; E6:160-167.)

[CODE-VERIFIED] Plugin consequences are real but limited: byte comparison found the source and plugin sc-recommend skill identical. The plugin task command also retains the explicit prohibition against task-mcp at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/task.md:185`. Eligibility changes therefore need equivalent plugin contract updates, not restoration of the removed command.

### Proposed recommendation changes

[UNVERIFIED] **MUST: proposed eligibility contract.** Extend Phase 0 Step C and its reference to extract deprecation and migration metadata. Exclude explicitly deprecated commands from runnable recommendations, verify any replacement independently, then apply normal scope and intent routing. Implement the same rule in the cold runbook and cache-hit validation, with invalidation of existing retired-target rows. This is a generic lifecycle rule, not a new keyword routing table. Grounding: E1:8-16 versus E4:128-135, E6:145-148 and E8:116-137.

[UNVERIFIED] **MUST: proposed migration behavior.** When a user asks about task-mcp, explain its retirement rather than silently dropping their named command. For an exact small change, a grounded replacement example is `/sc:task "Update the validation error text in the supplied file"`. If strict compliance was explicitly requested, the documented migration is `/sc:task "<same bounded change>" --compliance strict`; retain no legacy `--tier` or `--skip-mcp` token. Flag-emission eligibility needs the clarification recorded under Gaps. Grounding: E1:347-370; E2:19-25, 44.

[UNVERIFIED] **MUST: proposed planning policy.** For ordinary planned implementation formerly associated with MCP enforcement, prefer `/sc:workflow "<goal, constraints and code locations>" --depth standard`, inspect the printed plan, then `/sc:implement <printed-plan-path>`. Both interfaces support this chain. Rewrite the guide’s level boundary and corresponding parent/cold-path language together so file count, multiple sessions, existing specs or resumability alone do not select MDTM. Reserve task-builder and `/task` for the most complex, long-running workloads, while preserving explicit MDTM inputs. This is the user’s desired policy, not a proven capacity limit. (E13:18-40, 80; E14:22-29, 55-65; E9:305-308.)

### Acceptance/regression scenarios

[UNVERIFIED] Proposed checks:

1. Installed-only task-mcp with `deprecated: true`, no tracked counterpart: never recommend it as runnable.
2. A warm row references the unchanged installed retired file: reject the row despite a matching content hash.
3. An explicit legacy strict request: explain retirement, verify the replacement and preserve strict intent without legacy tokens.
4. Ordinary multi-file implementation across several sessions: prefer workflow plus implement, not MDTM solely because of those properties.
5. Explicit MDTM task input remains `/task`; a workflow package remains `/sc:implement`.
6. No guide or unavailable Auggie: degraded discovery still excludes deprecated commands.

Existing routing tests check ordering, mandatory flags, hard-limit wording and cache availability, but not retired installed leftovers. (E10:35-80.)

## Gaps

[CODE-VERIFIED] Scoped searches found no `task-mcp`, `deprecated` or `retired` handling in the recommendation skill, its refs, CLI module, recommendation tests, routing-contract test or plugin recommendation skill. Tracked-file searches found neither task-mcp nor sc-recommend-protocol primitives. These are bounded negative searches, not proof about every repository document.

[CODE-VERIFIED] The installed legacy recommendation protocol still exists and advertises old flags, language detection and keyword matching; current recommend activates `sc-recommend`, not that protocol. The hook accepts the legacy name but only injects reminders and exits successfully. It cannot substantiate a claim that retirement filtering or Phase 0 is mechanically enforced. (E12:1-16, 20-44; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/recommend.md:52-60`; E11:4-19.)

[CODE-VERIFIED] There is a flag-proof inconsistency: recommendation R1 requires a flag table or argument hint, but task’s `--compliance` appears in its synopsis and key-flags prose, not its sole flag-table row. Aligning this evidence rule or completing the task flag table directly affects accurate migration recommendations. (E4:335-341; E2:19, 44-48.)

[UNVERIFIED] No behavioral skill invocation, cache reproduction or test run was performed. Installed files were inspected as environment-specific leftovers, not treated as canonical source.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** add lifecycle-aware verification across normal, cold and cached recommendations, and align the governing planning boundary with the requested workflow-first policy.

[UNVERIFIED] **SHOULD:** add installed-only retirement and warm-cache regression fixtures; clarify compliance-flag verification.

[UNVERIFIED] **NONE:** do not recreate task-mcp, add a fixed keyword table, automatically enable compliance bypasses, or delete installed leftovers during recommendation.
