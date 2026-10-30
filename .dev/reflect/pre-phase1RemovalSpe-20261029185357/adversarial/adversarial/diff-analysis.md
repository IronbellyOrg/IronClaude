# Diff Analysis: reviewer-card comparison (sc:reflect pre, Wave 4)

## Metadata
- Generated: 2026-10-29T19:52:00Z
- Variants compared: 2
  - Variant 1 = `reviewer-1-card.yaml` (analyzer, sonnet), 10 findings, calibrated C = 0.75
  - Variant 2 = `reviewer-2-card.yaml` (qa, haiku/glm-5.3), 2 findings, calibrated C = 0.77
- Reviewed artifact: plan `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md` against spec `./source.md` (same folder)
- Focus: correctness, coverage, deviation-classification
- Total differences found: 19
- Categories: structural (2), content (13), contradictions (1), unique (12), shared assumptions (3 promoted, 1 stated)

Plan-task numbering note (STATED in Variant 1): plan Task N = spec TN-1 (plan Task 10 = spec T9, plan Task 18 = spec T14). Spec row Task columns use spec numbering.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity | Level |
|---|---|---|---|---|---|
| S-001 | Card granularity | 10 findings, `plan_line_remap`, `self_audit` with refuted T1 item and unfinished checks | 2 findings, no self-audit | Low | L1 |
| S-002 | Evidence citation form | single `file:line` per entry | `file:line` plus ranges (`:19-30`, `:279-291`) | Low | L1 |

## Content Differences

Each finding is a content point; the debate decides keep/drop and merged severity.

| # | Topic | Variant 1 | Variant 2 | Severity | Level |
|---|---|---|---|---|---|
| C-001 | Task 12 repo-wide memory-token rg | R1-F1 IMPORTANT: fails at Task 12 because tool-part tokens are Task 13's | silent | Medium | L3 |
| C-002 | Task 10 `mcp-servers:.*serena` repo-wide rg | R1-F2 IMPORTANT: fails, lines in Task 11-15 files | silent | Medium | L2 |
| C-003 | Task 4 replaces `_cleanup_user_native_registration` | R1-F3 IMPORTANT: still called by `uninstall_codebase_memory_mcp` until Task 5 | silent | Medium | L2 |
| C-004 | Task 18 sandbox rg vs allowlisted installed text | R1-F4 IMPORTANT: cannot pass | silent (see X-001) | High | L3 |
| C-005 | Task 18 omits `CLAUDE_CONFIG_DIR` | R1-F5 IMPORTANT: may read/mutate real config | silent | Medium | L3 |
| C-006 | Task 13 rubric edit range 124-127 | R1-F6 IMPORTANT: lines 128, 130 still match SER | silent | Medium | L3 |
| C-007 | Task 8 real.yaml comment list | R1-F7 MINOR: misses :721 | silent | Low | L2 |
| C-008 | Missing `mkdir -p` for new dirs | R1-F8 MINOR | silent | Low | L3 |
| C-009 | Task 12 runs no `tests/cli/reflect` | R1-F9 MINOR | silent | Low | L2 |
| C-010 | Untracked ledger/handoffs; Task 5 rg misses "Codebase Memory" | R1-F10 MINOR, grounded: false | silent | Low | L2 |
| C-011 | Scope limits (`.dev/` history, §2.3 leftovers) carried by no Constraint | silent | R2-F1 MINOR | Low | L2 |
| C-012 | Task 18 "existing" seeds only 2 files; DoD-3 promises old core files | silent | R2-F2 MINOR | Medium | L3 |
| C-013 | Review emphasis | acceptance-command executability per task | scope constraints and DoD evidence strength | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|---|---|---|---|
| X-001 | Outcome of Task 18's `rg -n -i 'serena\|codebase-memory' $T/old/.claude` | R1-F4: "cannot pass" (installed allowlisted text matches) | R2-F2: "can therefore pass without proving that a forced install overwrites stale Serena-bearing files" | Medium: both cannot be literally true; the merged Task 18 fix must address both |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001..U-010 | 1 | R1-F1..R1-F10 (no counterpart in Variant 2) | F1-F6 High, F7-F10 Low-Medium |
| U-011 | 2 | R2-F1 scope-limit constraint gap | Low-Medium |
| U-012 | 2 | R2-F2 DoD-3 seeding gap (spec-inherited) | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | both cards treat a failing acceptance command as a defect at face value | Acceptance commands run literally at the end of the task, ignoring plan Constraint "if the fix needs a file another task owns, pull that edit forward and log it" (plan:29) | UNSTATED | yes |
| A-002 | R2-F2 says "copies this gap from spec T14"; Variant 1 never says whether F2/F3/F4/F5 are inherited | A defect the plan copies verbatim from the spec is a plan defect of the same severity (deviation class: spec-inherited vs plan-introduced) | UNSTATED | yes |
| A-003 | R1-F4 and R2-F2 both reason about what `superclaude install` writes into a sandbox HOME | The installer copies primitives byte-for-byte (allowlisted text included) and `--force` overwrites stale core files | UNSTATED | yes |
| A-004 | Variant 1 `plan_line_remap` | Plan line refs are correct after the -33 remap | STATED | no |

Promoted:

| # | Assumption | Impact | Status | Level |
|---|---|---|---|---|
| A-001 | No pull-forward | Changes severity of every "acceptance fails at Task N" finding | open | L3 |
| A-002 | Spec-inherited = plan defect | Changes deviation classification and where the fix lands | open | L2 |
| A-003 | Installer copies byte-for-byte, `--force` overwrites | Decides X-001 | open | L3 |

## Orchestrator ground-truth checks (read-only, 2026-10-29)

| Claim | Check | Result |
|---|---|---|
| R1-F1 | repo-wide rg of the Task 12 pattern today; spec rule M8 (source.md:421); plan Task 12 text | 23 files hit. Task 12 itself must "Delete, do not port, the Serena-only calls of rule M8 in these files" and M8 lists `think_about_*`, `summarize_changes`, `activate_project`, `check_onboarding_performed`, `prepare_for_new_conversation`, `get_current_config`. Hits outside Task 11/12 files: `src/superclaude/cli/reflect/contract.py:30` (`get_current_config`, comment that Task 7 rewrites but checks only for `serena`) and `refs/reflection-rubric.md:127` (Task 13 row P84). The spec's T10b acceptance has the identical repo-wide rg. |
| R1-F2 | `rg 'mcp-servers:.*serena'` today; spec rows | 49 lines. P2, P33, P49, P62, P65 are spec T11 (plan Tasks 13-15); P6/P15/P43/P50 are T10,T11; save/load/pm are T10a (plan Task 11). Spec rule G5 says `mcp-servers:` lists "simply drop `serena`". Spec T9 acceptance has the identical rg. |
| R1-F3 | install_mcp.py | `_cleanup_user_native_registration` defined :916, called :993 and :999 inside `uninstall_codebase_memory_mcp` (:951); tavily tests call `uninstall_codebase_memory_mcp` at :888-1013. Spec :334 also says the new helper "replaces" it. |
| R1-F4 | allowlisted text and installers | `ccsession-tag/install.sh:41` contains "Serena"; `sc-cleanup-audit-protocol/SKILL.md:57` contains `.serena/`; Task 11 adds a `.serena/memories` sentence to `load.md`. `install_skills.py` has no exclude rule; `install_core.py` copies `core/*.md`. Spec DoD-2 (source.md:268) has the same un-allowlisted rg. |
| R1-F5 | env and code | `CLAUDE_CONFIG_DIR` is UNSET in this environment; only `install_mcp.py:731` reads it. Spec DoD-2 says "temp `HOME` and `CLAUDE_CONFIG_DIR`"; spec T14 steps omit it; plan Task 4 sets it, Task 18 does not. |
| R1-F6 | reflection-rubric.md:120-132 | :128 `find_implementations`, :130 "`type_hierarchy` retrieval" both match SER; spec row P84 lists lines 124,126-128 with action "delete lines 124-127"; :130 refers to "§6.1 step 4.5", which Task 13 deletes. |
| R1-F7 | real.yaml | :721 contains `Edit\|Write\|mcp__serena__*`; not in Task 8's list. |
| R1-F8 | filesystem | `docs/memory/reflect/` absent; `$PKG/artifacts/` absent. |
| R1-F9 | test file | `tests/cli/reflect/test_remediation_route_table.py:13-15` reads `remediation-handoff.md`, reflect `SKILL.md` and `commands/reflect.md`. |
| R1-F10 | git | `.dev/codegraph-migration/` is untracked (session git status `??`) and not ignored. `main.py:292` and `:313` say "Codebase Memory"; Task 5's rg pattern lacks it; Task 6's `acceptance-search.sh cbm src tests` would catch it. |
| R2-F1 | plan Constraints :26 | Already forbids real-HOME installs, user-data deletion, other-repo edits. Not covered: `.dev/` history edits; Coder binary; `serena-agent` uv tool. Acceptance searches exclude `.dev/**`. |
| R2-F2 | spec :269 vs :781, plan :248 | DoD-3 "How checked" says seeded with "the old hook matcher and the old core files"; T14 step 5 and plan Task 18 seed only `.claude.json` and `settings.json`. |

## Summary
- Total structural differences: 2
- Total content differences: 13
- Total contradictions: 1
- Total unique contributions: 12
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-004, X-001
- Taxonomy coverage: L1 = S-001, S-002; L2 = C-002, C-003, C-007, C-009, C-010, C-011, C-013, A-002; L3 = C-001, C-004, C-005, C-006, C-008, C-012, A-001, A-003
- Similarity check: variants share no finding; well above the 10% difference threshold, so debate proceeds.
