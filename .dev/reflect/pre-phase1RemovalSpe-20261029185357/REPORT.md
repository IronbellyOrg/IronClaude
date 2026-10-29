# Reflect report: Phase 1 removal plan vs its spec (UC-1, pre-execution)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.79
citations_total: 404
citations_revalidated: 178
citations_dropped: 3
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 178`: size of the re-Read sample (64 report citations, all re-read, plus 114 of 340 Pass-2 rows).
> - `citations_dropped: 3`: drops observed in the sample only (all three in the report body; 0 INF rows).
> - `citations_dropped_extrapolated: 7`: population-level estimate, `round(3 x 404 / 178)`. Recording-only.
>
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.

Plan: `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md` (19 tasks, 6 phases). Spec: `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md`. Verdict: **refactor before execution**. 12 confirmed findings (3 IMPORTANT, 9 MINOR), merged by `sc:adversarial` at convergence 0.947 from two heterogeneous reviewers (sonnet analyzer, glm-5.3 qa; opus excluded as the plan's author) and the T1 card. Seven of the 12 trace to the spec itself (spec errata), so the spec and plan should be fixed together.

Input drift: the input-tree hash changed during the run (`input_drift_detected: true`); the only changed file is `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md`, edited by the parallel Phase 2 finalizer. Its §2.12 and T0b checks, which Phase 1 Task 19 quotes, are unchanged, so no finding depends on the change; status is `partial` by rule.

Degraded: Serena and `get_current_config` were not used (run rule: no dependence on tools being removed); grounding used Read/Grep. Coverage: 0 parsed IDs (spec has no `R-`/`REQ-`/`SPEC-`/`T-NNN` labels), 340 quote-pinned Pass-2 rows, union coverage 0.7088 by lexical containment; 96 of the 99 unmatched rows are cited by row ID or source section in the plan, 3 have no reference (`artifacts/unmapped-triage.yaml`).

## Deviations

### Deviation D-001: Task 4 deletes or rewires a helper that the still-present uninstall path and its tests need (IMPORTANT, R1-F3)

- **Location:** `src/superclaude/cli/install_mcp.py:916`, `:993`, `:999`; `tests/cli/test_install_mcp_tavily.py:426-430`, `:926-929`, `:943-945`
- **Mapped tasklist item:** Task 4
- **Spec section:** §3.5 / §3.3 ("replaces the name-only `_cleanup_user_native_registration`", `source.md:334`); §10 "A task may not need a later task to go green" (`source.md:817`, re-pointed by the evidence-validator; the original citation was dropped)
- **Evidence:** `_cleanup_user_native_registration` is defined at `install_mcp.py:916` and called by `uninstall_codebase_memory_mcp` at `:993` and `:999`, which stays until Task 5; Task 4's acceptance runs all of `tests/cli/test_install_mcp_tavily.py`, whose native-removal tests record calls through the patched run function (`:426-430`) and assert call lists (`:926-929`, `:943-945`).
- **Classification:** regression
- **Classification rationale:** contradicts the spec's own §10 green-at-every-task rule; spec-inherited wording ("replaces").
- **Default remediation:** add `_remove_exact_user_entry` beside the old helper in Task 4; delete the old helper with `uninstall_codebase_memory_mcp` in Task 5.

### Deviation D-002: Task 18's sandbox searches cannot test what they claim (IMPORTANT, R1-F4)

- **Location:** plan Task 18 (`TASK-WF-phase1RemovalSpe-20261029-185100.md:247-248`)
- **Mapped tasklist item:** Task 18
- **Spec section:** DoD-2 and DoD-3 (`source.md:268-269`); T14 steps 4-5 (`source.md:780-781`)
- **Evidence:** `rg` without `--hidden` skips `$T/fresh/.claude/` and `.claude.json`, so the "fresh" search passes vacuously; the "existing" search over `$T/old/.claude` matches allowlisted installed text (`src/superclaude/skills/ccsession-tag/install.sh:41`, `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:57`, the Task 11 `/sc:load` legacy sentence) and the `settings.json.bak.*` backups the installers write (`src/superclaude/cli/install_hooks.py:293-297`, `:491-494`; `src/superclaude/cli/install_user_setup.py:81-89`).
- **Classification:** regression
- **Classification rationale:** the DoD-2/DoD-3 checks as written cannot produce a true result (spec-inherited).
- **Default remediation:** search with `--hidden --no-ignore`, filter the allowlisted installed lines and `settings.json.bak.*` files by a line-level filter, and assert separately that a backup exists.

### Deviation D-003: Task 18 omits `CLAUDE_CONFIG_DIR` from the sandbox runs (IMPORTANT, R1-F5)

- **Location:** plan Task 18 (`TASK-WF-phase1RemovalSpe-20261029-185100.md:247`); `src/superclaude/cli/install_mcp.py:731`, `:735`
- **Mapped tasklist item:** Task 18
- **Spec section:** DoD-2 ("temp `HOME` and `CLAUDE_CONFIG_DIR`", `source.md:268`)
- **Evidence:** `read_user_mcp_entry` reads `CLAUDE_CONFIG_DIR` first (`install_mcp.py:731`); the stub edits `${CLAUDE_CONFIG_DIR:-$HOME}/.claude.json`. Task 4 already sets it (`TASK-WF-phase1RemovalSpe-20261029-185100.md:80`). Latent here: the variable is unset in this environment.
- **Classification:** regression
- **Classification rationale:** contradicts DoD-2's explicit requirement; an environment with the variable set would read and change the real user config.
- **Default remediation:** set `CLAUDE_CONFIG_DIR` equal to the sandbox HOME on every Task 18 `env` call.

### Deviation D-004: Task 12's repo-wide memory-name search hits two lines outside its files (MINOR, R1-F1, T1 F-1)

- **Location:** `src/superclaude/cli/reflect/contract.py:30`; `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127`
- **Mapped tasklist item:** Task 12 (also Task 7)
- **Spec section:** §8 T10b acceptance; rule M8 (`source.md:421`)
- **Evidence:** both lines contain `get_current_config`; the rubric file is row P84, owned by Task 13, and the `contract.py` comment is reworded by Task 7, whose acceptance checks only `serena`.
- **Classification:** regression
- **Classification rationale:** Task 12's acceptance is red at Task 12, which breaks the §10 green-at-every-task rule.
- **Default remediation:** Task 7 removes `get_current_config` from the comment and checks for it; Task 12's repo-wide search excludes `reflection-rubric.md` (Task 13 removes it and Task 15's residual search covers it).

### Deviation D-005: Task 10's repo-wide `mcp-servers:.*serena` search fails at Task 10 (MINOR, R1-F2)

- **Location:** `src/superclaude/commands/troubleshoot.md:6`, `src/superclaude/commands/validate-roadmap.md:7`, `src/superclaude/commands/auggie-review.md:6`, `src/superclaude/commands/save.md:6`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:15`, `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:6`, `commands/sc-brainstorm.md:6`
- **Mapped tasklist item:** Task 10
- **Spec section:** rule G5 ("`mcp-servers:` frontmatter lists simply drop `serena`", `source.md:392`)
- **Evidence:** these files carry `serena` in `mcp-servers:` but their rows belong to Tasks 11-15.
- **Classification:** regression
- **Classification rationale:** red acceptance at its own task (spec-inherited from T9).
- **Default remediation:** Task 10 drops `serena` from every `mcp-servers:` line in `src/superclaude`, `plugins/superclaude`, `commands` and `agents`.

### Deviation D-006: Task 13's reflect ref edits leave residual-search tokens (MINOR, R1-F6)

- **Location:** `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:128`, `:130`; `refs/cost-profile.yaml:74`; `refs/coverage-mapping.md:195`; `refs/deviation-taxonomy.md:80`, `:83`; `refs/reviewer-spec.md:14`, `:55`
- **Mapped tasklist item:** Task 13
- **Spec section:** row P84 (`source.md:235`); acceptance-search `SER` pattern (`source.md:620`)
- **Evidence:** those lines contain `find_implementations`, `type_hierarchy` or `execute_shell_command`, all in `SER`; `reflection-rubric.md:128` is listed in row P84 but outside its action range 124-127, and the other lines are in no row's line list; Task 13 runs `acceptance-search.sh serena` over the whole `sc-reflect-protocol` folder.
- **Classification:** regression
- **Classification rationale:** red acceptance at Task 13 (spec-inherited line lists).
- **Default remediation:** give Task 13 explicit per-line actions for these lines, keeping the "No-mutation gate." paragraph that `tests/cli/reflect/test_verify_denylist_git_mutations.py` pins.

### Deviation D-007: Task 8 misses a `real.yaml` comment (MINOR, R1-F7)

- **Location:** `src/superclaude/cli/eval/suites/real.yaml:721`
- **Mapped tasklist item:** Task 8
- **Spec section:** row S40 / T7 change
- **Evidence:** line 721 contains `mcp__serena__`, which Task 8's own `rg` over `src/superclaude/cli/eval` rejects.
- **Classification:** regression
- **Classification rationale:** red acceptance at its own task.
- **Default remediation:** add `real.yaml:721` to Task 8's comments to reword.

### Deviation D-008: Missing directory creation (MINOR, R1-F8)

- **Location:** plan Tasks 1, 12, 18
- **Mapped tasklist item:** Tasks 1, 12, 18
- **Spec section:** §8 T0, T10b (M5), T14
- **Evidence:** `docs/memory/reflect/` does not exist (only `docs/memory/README.md` and siblings); `$PKG/artifacts/` does not exist before Task 1.
- **Classification:** drift
- **Classification rationale:** plan omits a precondition; no spec text contradicted.
- **Default remediation:** add `mkdir -p` for `docs/memory/reflect`, `$PKG/artifacts/baseline` and `$PKG/artifacts/final`.

### Deviation D-009: Task 12 runs no reflect tests (MINOR, R1-F9)

- **Location:** `tests/cli/reflect/test_remediation_route_table.py:13`
- **Mapped tasklist item:** Task 12
- **Spec section:** §8 T10b acceptance
- **Evidence:** that test reads `remediation-handoff.md`, which Task 12 edits.
- **Classification:** drift
- **Classification rationale:** test coverage omission; no contradiction.
- **Default remediation:** add `tests/cli/reflect` to Task 12's pytest list.

### Deviation D-010: Ledger and handoff files are never committed (MINOR, R1-F10)

- **Location:** plan Constraints (`TASK-WF-phase1RemovalSpe-20261029-185100.md:21`)
- **Mapped tasklist item:** Tasks 13, 14, 15, 19
- **Spec section:** rule G9; §8 T15
- **Evidence:** the plan stages only `.dev/tasks`; `.dev/codegraph-migration/` is untracked in this worktree.
- **Classification:** drift
- **Classification rationale:** deliverables would be lost after the branch merges; no spec text contradicted.
- **Default remediation:** each task that writes the ledger or a handoff file `git add`s that exact file.

### Deviation D-011: Two scope limits are not in the plan (MINOR, R2-F1, T1 F-2)

- **Location:** plan Constraints (`TASK-WF-phase1RemovalSpe-20261029-185100.md:19-30`)
- **Mapped tasklist item:** unmapped
- **Spec section:** §2.1 "Historical `.dev/` artifacts stay untouched." (`source.md:261`); §2.3 leftovers (`source.md:279-291`)
- **Evidence:** the Constraints block real-HOME installs, user-data deletion and other-repo edits, but not edits to historical `.dev/` files or removal of the Coder-owned binary, the `serena-agent` uv tool, bundle markers, upstream companions and `~/.local/bin/install.sh`.
- **Classification:** drift
- **Classification rationale:** spec requirement absent from the plan without a reason.
- **Default remediation:** add one Constraints bullet stating both limits.

### Deviation D-012: The "existing" sandbox does not seed stale core files (MINOR, R2-F2)

- **Location:** plan Task 18 (`TASK-WF-phase1RemovalSpe-20261029-185100.md:248`)
- **Mapped tasklist item:** Task 18
- **Spec section:** DoD-3 ("the old core files", `source.md:269`); T14 step 5 (`source.md:781`)
- **Evidence:** the sandbox seeds only `.claude.json` and `.claude/settings.json`; forced overwrite of core files and commands is implemented in `src/superclaude/cli/install_core.py:65-70` and `src/superclaude/cli/install_commands.py:55-61` but never exercised.
- **Classification:** regression
- **Classification rationale:** contradicts DoD-3's stated seeding (spec-inherited from T14 step 5).
- **Default remediation:** seed a stale `$T/old/.claude/CLAUDE.md` and `$T/old/.claude/commands/sc/reflect.md` with one `serena` row each before the run.

## Grounding Gaps

Citations the evidence-validator dropped (status forced to `partial`; no claim relied on them alone):

### Gap G-001
- Original claim: D-001 spec section cited §10 "A task may not need a later task to go green" at `source.md:796`.
- Why dropped: line 796 is blank; the sentence is at `source.md:817`, which the validator confirmed and which now replaces it.

### Gap G-002
- Original claim: D-006 listed `refs/deviation-taxonomy.md:79` as containing `find_implementations`, `type_hierarchy` or `execute_shell_command`.
- Why dropped: line 79 contains `get_diagnostics_for_file` (also in `SER`, so still a residual hit) and none of the three named tokens; removed from the list.

### Gap G-003
- Original claim: D-006 said `reflection-rubric.md:128` is "not in any row's line list".
- Why dropped: row P84 (`source.md:235`) lists 124,126-128; line 128 is in the list but outside the action range 124-127. Claim reworded.

## Refuted and dropped claims

- T1 risk R-2 (Task 5 might remove the "Unknown MCP server selection" message Task 9 relies on): refuted by reviewer 1; `src/superclaude/cli/install_mcp.py:1319` is the generic selection message and survives Task 5.
- R1-F1's "many more files" sub-claim, the extra Task 5 `rg` sub-fixes, and R2-F2's "can pass" wording: dropped by the merge (`adversarial/merged-findings.md`, `dropped_subclaims`).

## Inferred requirements (Pass 2)

340 rows from Step 1B.0 Pass 2; 114 sampled rows re-checked by the evidence-validator, 0 dropped (postscript: no INF row dropped). Match result: containment task, or `none` with the triage reason.

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | `src/superclaude/cli/install_codebase_memory.py` \| 1-759 (whole file; hits 23,25,82,86,223,265,323,337,611,673) \| **delete file** \| T5 | `source.md:30` | none (row-ref C1) |
| INF-002 | `src/superclaude/cli/install_mcp.py` \| 21; 101-108; 486-503; 571-583; 714-754; 757-813; 815-913; 916-948; 951-1007; 1025-1028; 1243-1343 (parts) \| **delete blocks**, keep the file (other servers use it); section 3 keeps the generic registration helpers \| T3 (helpers), T4, Serena blocks: T8 | `source.md:31` | none (row-ref C2) |
| INF-003 | `src/superclaude/cli/main.py` \| 38; 44; 50-52; 66; 78-83; 161-186; 254-262; 264-275; 292; 299-309; 310; 313; 319-321; 327; 334-340 \| **delete blocks + rewrite text**; T3 adds the retire-step call \| T2, T3, T4 | `source.md:32` | none (row-ref C3) |
| INF-004 | `tests/cli/test_install_codebase_memory.py` \| 1-1633 (hits: Appendix A) \| **delete file, but port 16 generic tests first** (1.4) \| T1, T2, T4, T5 | `source.md:33` | none (row-ref C4) |
| INF-005 | **delete 3 tests**: `test_codebase_memory_native_registry_contract` (192), `test_codebase_memory_dispatch_uses_shared_install` (202), `test_selected_native_prerequisites_do_not_probe_other_runtimes` (222). Keep the other 9 tests \| T4 | `source.md:34` | none (row-ref C5) |
| INF-006 | **delete 382-end**: fixtures `native_registration` (382), `native_removal` (832), helpers `_native_entry` (472), `_seed_native_entry` (480) and 54 native tests. **Keep lines 1-375** (16 Tavily tests, 15 run + 1 live smoke skipped without `TAVILY_API_KEY`) \| T4 | `source.md:35` | none (row-ref C6) |
| INF-007 | **rewrite**: autouse fixture `native_phase_guard` (31-76), `_NATIVE_INSTALLER` (28), `_stub_installers` branch (82-91), expected call list (138). **Delete 17 tests** (5 test functions:... | `source.md:36` | none (row-ref C7) |
| INF-008 | **Rewrite** `test_install_force_target_do_not_redirect_or_force_native` (345) to drop the native assertions. 10 tests remain \| T2 | `source.md:36` | Task 3 |
| INF-009 | **delete sections** `## Default Framework Setup...` (5-26), `## Safe Codebase Memory Removal` (206-234), `### Codebase Memory Setup or Registration Failure` (237-242), `## Release Gate...` (309-324); **rewrite** 36-37, 43, 46, 56, 67, 73, 121, 124, 183-184, 306 \| T12 | `source.md:37` | none (row-ref C8) |
| INF-010 | **delete section** `## Codebase Memory Native Lifecycle` (31-55); **rewrite** 13, 21-22, 25, 650 \| T12 | `source.md:38` | none (row-ref C9) |
| INF-011 | **rewrite text**: drop the cbm default-provisioning paragraph (9-13) and the cbm wording in the examples (316, 321, 399, 420). The page's thesis (MCP use is optional, native fallbacks) stays valid \| T12 | `source.md:39` | none (row-ref C10) |
| INF-012 | **rewrite text**: remove "required user-level Codebase Memory MCP setup" (64) and the `# framework assets + required user Codebase Memory setup (Linux)` comment (75) \| T12 | `source.md:40` | none (row-ref C11) |
| INF-013 | **rewrite comments only**: the `permissions` comment (133-134, "runs the unpinned upstream Codebase Memory installer") and the step comment (155, "The required Codebase Memory phase ... needs the Claude CLI") stop naming codebase-memory, e.g. "`superclaude install` registers and retires user-scope MCP servers through the Claude CLI". | `source.md:41` | none (row-ref C12) |
| INF-014 | **Keep** the `Install Claude CLI` step (156-159) and `permissions: contents: read`: Phase 2's required codegraph phase needs `claude --version` in this job (Phase 2 spec F12, D9), and Phases 1 and 2 merge as one unit (section 2.2), so deleting it here only for Phase 2 to restore it is churn (review finding X-15) \| T12 | `source.md:41` | Task 16 |
| INF-015 | The Task column's `T10` and `T11` are split into T10a-T10b and T11a-T11c (review finding X-12); section 8 lists which rows each piece owns, and that list wins. | `source.md:48` | none (section-ref §1.2) |
| INF-016 | `.gitignore` \| 113 \| keep until `.serena/` is deleted everywhere; then delete line (decision D4) \| T13 | `source.md:52` | none (row-ref S1) |
| INF-017 | `.serena/.gitignore` \| path only \| `git rm` the file \| T13 | `source.md:53-56` | Task 17 |
| INF-018 | move to `docs/memory/reflect/` (section 5 rule M5, `git mv`), then delete `.serena/`; do not lose the content \| T10b (move), T13 | `source.md:55` | Task 12 |
| INF-019 | `CLAUDE.md` \| 377 \| delete line 377 \| T12 | `source.md:58` | Task 16 |
| INF-020 | `README.md` \| 38,219 \| delete both mentions \| T12 | `source.md:60` | Task 16 |
| INF-021 | `SECURITY.md` \| 328 \| delete line 328 \| T12 | `source.md:61` | Task 16 |
| INF-022 | `docs/analysis-sc-tasklist.md` \| 317 \| rewrite after sc-task-protocol STRICT decision \| T12 | `source.md:62` | Task 16 |
| INF-023 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` \| 275,348,459,530,558,796,876,899,909,1500,1567 \| rewrite examples to drop serena; delete 459 wording \| T12 | `source.md:63` | none (row-ref S12) |
| INF-024 | `docs/developer-guide/technical-architecture.md` \| 100 \| delete the word \| T12 | `source.md:64` | Task 16 |
| INF-025 | `docs/mcp/mcp-integration-policy.md` \| 77,80,118-119,200,220,261,283,299,309,312,335,348,387,403-405,421,432,452,454,476 \| delete Serena sections; rewrite memory rules per section 3 \| T12 | `source.md:67` | none (row-ref S16) |
| INF-026 | `docs/mcp/mcp-optional-design.md` \| 35,97,132,142,153,157,209,227,232,326,354-355,369 \| delete Serena examples \| T12 | `source.md:68` | none (row-ref S17) |
| INF-027 | `docs/reference/mcp-server-guide.md` \| 3,17,23,370,372,379,388-390,392,394,539,614,623 \| delete Serena sections \| T12 | `source.md:71` | none (row-ref S20) |
| INF-028 | `docs/troubleshooting/serena-installation.md` \| 1,5,10,15,22,25,28,34,47-48,51,76,85,90-91,119,123-124,143,145,153 \| delete file (and its links) \| T12 | `source.md:72` | none (row-ref S21) |
| INF-029 | `docs/user-guide/agents.md` \| 374,686 \| rewrite per section 3 \| T12 | `source.md:73` | Task 16 |
| INF-030 | `docs/user-guide/brainstorm.md` \| 17,146 \| delete Serena mentions \| T12 | `source.md:74` | Task 16 |
| INF-031 | delete Serena rows and the comparison section; rewrite /sc:save//sc:load text per section 3 \| T12 | `source.md:75` | Task 16 |
| INF-032 | `docs/user-guide/flags.md` \| 25,146,201,219 \| delete the flag rows \| T12 | `source.md:76` | Task 16 |
| INF-033 | `docs/user-guide/freshness-hooks.md` \| 18 \| delete the two tool names \| T12 | `source.md:77` | Task 16 |
| INF-034 | `docs/user-guide/mcp-installation.md` \| 43,60,83,123,304 \| delete serena rows/examples and link \| T12 | `source.md:78` | Task 16 |
| INF-035 | `docs/user-guide/mcp-servers.md` \| 19,34,85,97,154,211,213,245,299,307,309-311,318,325-326,347 \| delete Serena section and rows \| T12 | `source.md:79` | none (row-ref S28) |
| INF-036 | `docs/user-guide/memory-system.md` \| 18 \| reword per section 3 \| T12 | `source.md:80` | Task 16 |
| INF-037 | `docs/user-guide/modes.md` \| 213,264 \| rewrite per section 3 \| T12 | `source.md:81` | Task 16 |
| INF-038 | `docs/user-guide/session-management.md` \| 3,10,15,35,42,65,113,130,163,169,179,216,231,255,320 \| rewrite per section 3 (or delete if Option C) \| T12 | `source.md:82` | none (row-ref S31) |
| INF-039 | `plugins/superclaude/mcp/MCP_Morphllm.md` \| 15,23,32 \| delete the Serena lines/pairings \| T8 | `source.md:83-100` | Task 9 |
| INF-040 | `plugins/superclaude/mcp/MCP_Serena.md` \| 1,24-25,30-33 \| delete file \| T8 | `source.md:84-102` | Task 9 |
| INF-041 | `src/superclaude/cli/eval/coverage.py` \| 195 \| reword example (no behavior) \| T7 | `source.md:88` | Task 8 |
| INF-042 | `src/superclaude/cli/eval/suites/README.md` \| 170 \| rewrite with E8 removal \| T7 | `source.md:89` | Task 8 |
| INF-043 | delete capability row 40 and eval E8; reword E6/E7 comments \| T7 | `source.md:91` | Task 8 |
| INF-044 | `src/superclaude/cli/install_mcp.py` \| 55-56,59,561,568,570 \| delete both blocks (see section 4) \| T8 | `source.md:92` | none (row-ref S41) |
| INF-045 | `src/superclaude/cli/reflect/config.py` \| 162,199 \| reword comment (behavior unchanged) \| T6 | `source.md:93` | Task 7 |
| INF-046 | `src/superclaude/cli/reflect/contract.py` \| 29-30,33 \| remove two members + comment; unknown tokens then neither halt nor degrade (see section 4) \| T6 | `source.md:94` | none (row-ref S43) |
| INF-047 | `src/superclaude/cli/reflect/ensemble.py` \| 824 \| delete key AND the 25 test fixtures that carry it in the same change (contract is tolerant of unknown fields: fixture tolerant_unknown_field.yaml) \| T6 | `source.md:95` | none (row-ref S44) |
| INF-048 | `tests/cli/eval/test_coverage_gate.py` \| 127 \| replace string with another MCP tool name (e.g. mcp__context7__resolve); test stays \| T7 | `source.md:108` | none (row-ref S57) |
| INF-049 | `tests/cli/reflect/fixtures/autofixable_drift.yaml` \| 26 \| delete the `serena_summary_corroboration` line \| T6 | `source.md:109-133` | Task 7 |
| INF-050 | `tests/cli/reflect/fixtures/degraded_serena.yaml` \| 26,28 \| delete file (after test_degraded_serena and test_runner_e2e are repointed) \| T6 | `source.md:116` | Task 7 |
| INF-051 | delete the `serena_summary_corroboration` line; replace the `- serena` entry with another halt token (e.g. auggie) \| T6 | `source.md:119` | Task 7 |
| INF-052 | `tests/cli/reflect/test_ensemble_unit.py` \| 345 \| reword docstring \| T6 | `source.md:134-137` | Task 7 |
| INF-053 | `tests/cli/reflect/test_runner_e2e.py` \| 71 \| point at another degraded fixture (e.g. degraded_tier1.yaml) -- see section 4 \| T6 | `source.md:135` | none (row-ref S84) |
| INF-054 | `tests/cli/reflect/test_verdict_mapping.py` \| 93-94,96,193-194,196,245 \| delete 2 tests; edit token list \| T6 | `source.md:136` | Task 7 |
| INF-055 | `tests/cli/test_install_hooks.py` \| 684-687 \| delete four asserts \| T7 | `source.md:138` | Task 8 |
| INF-056 | `tests/cli/test_install_mcp_registry.py` \| 13-14,45,47-48,61 \| delete serena entries from both dicts (tests stay) \| T8 | `source.md:139` | Task 9 |
| INF-057 | `tests/core/test_how_we_work_routing_table.py` \| 1074 \| rewrite assertion after HOW-WE-WORK wording decision \| T10 | `source.md:140` | none (row-ref S89) |
| INF-058 | `tests/recommend/fixtures/routing_refresh_cases.json` \| 576,584 \| rewrite strings with HOW-WE-WORK wording \| T10 | `source.md:141` | Task 12 |
| INF-059 | `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py` \| 33-35,77-79 \| delete the 2 tests \| T9 | `source.md:143` | Task 10 |
| INF-060 | `tests/sc-roadmap/integration/test_wave5_completion.py` \| 69,74,77-78 \| delete test_circuit_breaker_for_serena; reword 69-74 \| T9 | `source.md:144` | Task 10 |
| INF-061 | `tests/troubleshoot/test_diagnostic_worker_contract.py` \| 22-25,152 \| edit TOOLS and mutant string together with troubleshoot-analyst.md \| T11 | `source.md:150` | Task 14 |
| INF-062 | `tests/unit/test_cli_install.py` \| 150,153,423,425 \| delete the three names from both listings \| T8 | `source.md:151` | Task 9 |
| INF-063 | `agents/sc-pm-agent.md` \| 10,18,20,30-34,53,66,92,108,113,132,239,243-246,249-251,259-261 \| rewrite lifecycle per section 3 (repo-local file memory) \| T10 | `source.md:152-178` | none (row-ref P1) |
| INF-064 | `commands/sc-brainstorm.md` \| 6,44,78,84 \| delete `serena` from frontmatter and fallback wording \| T11 | `source.md:153` | none (row-ref P2) |
| INF-065 | `commands/sc-help.md` \| 43-45,75 \| delete the rows \| T9 | `source.md:154` | Task 10 |
| INF-066 | `commands/sc-load.md` \| 3,6,24,31,37,43,58,86,92 \| rewrite per memory decision (section 3); delete `serena` frontmatter \| T10 | `source.md:155-190` | none (row-ref P4) |
| INF-067 | `commands/sc-pm.md` \| 6,15,34,39-43,59,65,79,86-87,95,323,423-428,530,539 \| rewrite memory lifecycle per section 3; delete `serena` frontmatter \| T10 | `source.md:156-191` | none (row-ref P5) |
| INF-068 | `commands/sc-reflect.md` \| 3,6,24,31-32,36,38,80,85 \| rewrite tool table; delete `--onboard` Serena bootstrap rows; delete `serena` frontmatter \| T10, T11 | `source.md:157-194` | Task 13 |
| INF-069 | `commands/sc-research.md` \| 6,85 \| delete both lines \| T9 | `source.md:158-196` | Task 10 |
| INF-070 | `commands/sc-save.md` \| 3,6,25,31,37,42,58,86,91 \| rewrite per memory decision (section 3): keep command, swap Serena memory for repo-local files; delete `serena` frontmatter \| T10 | `source.md:159-198` | none (row-ref P8) |
| INF-071 | `commands/sc-task.md` \| 6,32,41 \| delete `serena` from the `mcp-servers:` frontmatter list \| T9 | `source.md:160-239` | Task 10 |
| INF-072 | `plugins/superclaude/commands/brainstorm.md` \| 6,120 \| delete `serena` from frontmatter \| T9 | `source.md:163-185` | Task 10 |
| INF-073 | `plugins/superclaude/core/RESEARCH_CONFIG.md` \| 98,415 \| delete both \| T9 | `source.md:170-204` | Task 10 |
| INF-074 | `plugins/superclaude/hooks/hooks.json` \| 37 \| delete the four `mcp__serena__*` alternatives from the matcher regex \| T7 | `source.md:172-206` | Task 8 |
| INF-075 | `plugins/superclaude/modes/MODE_Orchestration.md` \| 25 \| delete the row (or replace with codegraph in P3) \| T11 | `source.md:173-207` | Task 15 |
| INF-076 | `plugins/superclaude/modes/MODE_Task_Management.md` \| 15-18,25-26,33,36,43,49-50,53,83-86,88,94-95,98,107,109 \| rewrite memory calls per section 3 \| T10 | `source.md:174-208` | none (row-ref P23) |
| INF-077 | rewrite wording per section 3 (byte-identical copy rule: edit src then copy to plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md) \| T10 | `source.md:175-203` | Task 12 |
| INF-078 | `plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` \| 28 \| rewrite to name only remaining tools (P3: codegraph) \| T11 | `source.md:176-227` | Task 15 |
| INF-079 | `src/superclaude/agents/auggie-reviewer.md` \| 5,36,81,115 \| delete the two tools from `tools:`; rewrite lines 36, 81, 115 \| T11 | `source.md:177` | Task 15 |
| INF-080 | `src/superclaude/agents/reflect-reviewer.md` \| 5,147 \| delete the four tools; rewrite line 147 \| T11 | `source.md:179` | Task 13 |
| INF-081 | `src/superclaude/agents/reuse-auditor.md` \| 5,54,57,131 \| delete the three tools; rewrite lines 54, 57, 131 \| T11 | `source.md:180` | Task 13 |
| INF-082 | `src/superclaude/agents/troubleshoot-analyst.md` \| 5 \| delete the four tools from `tools:` \| T11 | `source.md:182` | Task 14 |
| INF-083 | `src/superclaude/commands/auggie-review.md` \| 6,78 \| delete frontmatter entry; rewrite line 78 \| T11 | `source.md:184` | Task 15 |
| INF-084 | `src/superclaude/commands/troubleshoot.md` \| 3,6,52,58,75,89,96,112,161,173 \| rewrite wording; delete `serena` frontmatter \| T11 | `source.md:200` | none (row-ref P49) |
| INF-085 | `src/superclaude/commands/validate-roadmap.md` \| 6-7 \| delete the mcp__serena__* entries from `allowed-tools` and `serena` from `mcp-servers` \| T10, T11 | `source.md:201` | Task 15 |
| INF-086 | `src/superclaude/core/CLAUDE.md` \| 21,90,112 \| delete row 21; trim S2 list at 90; rewrite row at 112 \| T9 (lines 21, 90), T11 (line 112) | `source.md:202` | Task 10 |
| INF-087 | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` \| 12,491,2243,2277,2285 \| delete rows and YAML block \| T9 | `source.md:211` | Task 13 |
| INF-088 | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` \| 15,57,193,387 \| delete frontmatter entry and fallback_1 wording \| T11 | `source.md:213` | Task 14 |
| INF-089 | `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` \| 24,26-27 \| delete tier 2 block (renumber) \| T11 | `source.md:214` | Task 15 |
| INF-090 | `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` \| 6,20,57,83 \| delete frontmatter + line 83; keep `.serena/` ignore only if folder may still exist (decision D4) \| T11 | `source.md:216` | Task 15 |
| INF-091 | `src/superclaude/skills/sc-crash-recovery/SKILL.md` \| 3,37,62,67,79,145,157 \| rewrite investigator #3 to read the new memory folder (section 3); rename report section \| T10 | `source.md:219-221` | none (row-ref P68) |
| INF-092 | `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` \| 146-147 \| repoint to the new memory folder (section 3) or delete the two JSON fields \| T10 | `source.md:222` | Task 12 |
| INF-093 | `src/superclaude/skills/sc-pm-protocol/SKILL.md` \| 21,26-30,43-44,50,52,113,157,166 \| rewrite lifecycle per section 3 \| T10 | `source.md:224` | none (row-ref P73) |
| INF-094 | `src/superclaude/skills/sc-post-release-protocol/SKILL.md` \| 11,244,259 \| delete serena from enum and frontmatter (P3: add codegraph) \| T9 | `source.md:225` | Task 14 |
| INF-095 | rewrite: delete Serena probes/telemetry; symbol chain -> P3 codegraph; calibration memory -> section 3 \| T10, T11 | `source.md:228` | Task 13 |
| INF-096 | `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml` \| 73 \| rewrite tool name \| T11 | `source.md:229-238` | Task 13 |
| INF-097 | `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` \| 50,65 \| delete line 65; rewrite line 50 (P3: codegraph lookup) \| T11 | `source.md:231` | Task 13 |
| INF-098 | `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md` \| 217 \| reword \| T11 (with the reflect rewrite) | `source.md:232` | Task 13 |
| INF-099 | `src/superclaude/skills/sc-reflect-protocol/refs/input-resolution.md` \| 81-82 \| delete both bullets \| T10 | `source.md:233` | Task 12 |
| INF-100 | `src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md` \| 118,120,125-126,137,140,164,168-170,174,178-180 \| delete the catalog section together with the `--onboard` feature \| T11 (with the reflect rewrite) | `source.md:234` | none (row-ref P83) |
| INF-101 | `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` \| 124,126-128 \| delete lines 124-127 \| T11 (with the reflect rewrite) | `source.md:235` | Task 13 |
| INF-102 | `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` \| 179,232 \| rewrite handoff to a file under the new memory folder (section 3) \| T10 | `source.md:236` | none (row-ref P85) |
| INF-103 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` \| 13,325-326,414,419,425,436,443,455 \| delete Serena rows; make the existing file fallback the primary; delete `serena` frontmatter \| T9 | `source.md:240` | none (row-ref P89) |
| INF-104 | `src/superclaude/skills/sc-task-protocol/SKILL.md` \| 88,91,103,287,303,309,319 \| rewrite STRICT tier prerequisites; delete activate_project/memory steps \| T10, T11 | `source.md:242` | none (row-ref P91) |
| INF-105 | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` \| 683 \| edit the row (STRICT no longer needs Serena) \| T11 (with the sc-task STRICT rewrite) | `source.md:243` | Task 15 |
| INF-106 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` \| 3-4,10,31,156,168,193,216,439,606,620 \| delete tools and wording \| T11 | `source.md:244` | Task 14 |
| INF-107 | `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` \| 11 \| delete the mention \| T11 | `source.md:245-246` | Task 14 |
| INF-108 | rewrite: state persistence to repo-local files (section 3); symbol checks to Grep/Read now, codegraph in P3 \| T10, T11 | `source.md:247` | none (row-ref P96) |
| INF-109 | `src/superclaude/hooks/scripts/freshness-pre-edit.sh` \| 25-36 \| delete the `relative_path` branch (`REL_PATH` lookup and its `elif`), keep `file_path`; reword the line-36 message to "no file_path in tool_input" \| T7 | `source.md:250` | Task 8 |
| INF-110 | `plugins/superclaude/hooks/scripts/freshness-pre-edit.sh` \| 25-36 \| same edit as D1 (hand-maintained mirror) \| T7 | `source.md:251` | Task 8 |
| INF-111 | edit in the same commit as the reflect SKILL.md section 6.1.1 change: follow the section's new heading, or delete the envelope test if the section is deleted (section 4) \| T11 | `source.md:252` | Task 13 |
| INF-112 | `tests/cli/reflect/test_reviewer_readonly_tools.py` \| 7, 31 \| drop `execute_shell_command` from the denylist set and docstring (the tool no longer exists) \| T11 | `source.md:253` | Task 13 |
| INF-113 | `tests/cli/reflect/test_reviewer_finding_parity.py` \| 33 \| same as D4 \| T11 | `source.md:254` | Task 13 |
| INF-114 | Remove codebase-memory-mcp and Serena from everything IronClaude owns: installer and CLI code (`superclaude install`, `superclaude mcp`, the `update.sh` path), registry entries and MCP templates, hooks, skills, commands, agents, refs, modes, core docs, the hand-maintained `plugins/superclaude/` tree and the root `commands/`, `agents/` copies, user docs, tests and CI, plus the user-environment registrations IronClaude can prove it (or the Coder bundle, with IronClaude's exact argv) wrote. | `source.md:261` | none (NO-REF) |
| INF-115 | Historical `.dev/` artifacts stay untouched. | `source.md:261` | none (NO-REF) |
| INF-116 | No repo file outside `.dev/` references either server, except the allowlist in 2.4 \| the two acceptance searches in T14 (W1 `PAT`, and W2 `PAT` plus `P2`), each filtered by the 2.4 allowlist, print nothing | `source.md:267` | none (section-ref §2.2) |
| INF-117 | `superclaude install` on a fresh HOME writes no codebase-memory or Serena binary, MCP entry, permission, hook matcher entry, companion skill/agent/hook or `CLAUDE.md` mention | `source.md:268` | Task 18 |
| INF-118 | `./update.sh` on an existing workspace removes the IronClaude-owned leftovers: the user-scope `codebase-memory-mcp` registration and every Tier R `serena` registration... | `source.md:269` | Task 18 |
| INF-119 | IronClaude's receipt and marker files when their binary is gone, the four `mcp__serena__*` alternatives of the freshness hook matcher in `~/.claude/settings.json`, the Serena rows of `~/.claude/CLAUDE.md`, `~/.claude/HOW-WE-WORK.md`, `~/.claude/RESEARCH_CONFIG.md` and of every installed command, agent and skill | `source.md:269` | none (section-ref §2.2) |
| INF-120 | A same-named entry that IronClaude did not write (different command, non-empty `env` or `headers`, local or project scope) survives untouched; `env: {}` and `headers: {}` count as absent | `source.md:270` | none (section-ref §2.2) |
| INF-121 | Targeted suites green; full `uv run pytest` has no failure that is not in the T0 baseline; `make verify-sync` and `make lint` pass | `source.md:271` | Task 1 |
| INF-122 | Serena memory is replaced (section 5), so `/sc:save`, `/sc:load`, pm-agent, crash-recovery, reflect calibration and validate-roadmap ledgers work without Serena; no primitive step names a removed tool (section 4) | `source.md:272` | none (section-ref §2.2) |
| INF-123 | Handoff notes exist for every other IronbellyOrg repo with live hits (section 6), and the Coder part is cross-referenced to Phase 2's Coder handoff | `source.md:273` | Task 19 |
| INF-124 | Phases 1 and 2 merge as one unit; the Phase 1 executor never opens a `master` PR for Phase 1 alone. | `source.md:277` | Constraints |
| INF-125 | ### 2.3 Leftovers IronClaude does not own (handed off, not removed by Phase 1) | `source.md:279` | none (NO-REF) |
| INF-126 | The retire step's source and tests (section 3 names the files) and the `"serena"` and `"codebase-memory-mcp"` entries in the `test_removed_mcp_servers_are_not_in_registry` guard of `tests/cli/test_install_mcp_registry.py` \| they name the servers in order to remove them | `source.md:297` | Task 16 |
| INF-127 | `src/superclaude/commands/load.md` and its `plugins/superclaude/commands/load.md` and root `commands/sc-load.md` copies: one legacy-read sentence for `.serena/memories/` \| memory decision item 7 (section 5): one release of read-only fallback for existing Serena memories | `source.md:298` | Task 11 |
| INF-128 | `.gitignore:113` (`.serena/`) and `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:57` (`.serena/` in the audit ignore list) \| old checkouts still carry local `.serena/` folders | `source.md:299` | Task 15 |
| INF-129 | `CHANGELOG.md` (history plus the new removal entry), `POST-REFLECT-TASK.md`, `docs/memory/patterns_learned.jsonl`, `docs/memory/pm_context.md`, `src/superclaude/skills/ccsession-tag/install.sh:41`, `tests/skills/test_implement_severity_replay.py`, `tests/troubleshoot/fixtures/regression/sysbox-20260918/Fable-D3/REPORT.md` \| history or an unrelated label | `source.md:300` | none (section-ref §2.4) |
| INF-130 | The 19 files that match only `onboarding` (rows marked "none (keep)" whose action says "onboarding is generic English") \| false positives | `source.md:301` | none (section-ref §2.4) |
| INF-131 | An automatic, non-interactive, **non-fatal "retire step"** runs at the end of every `superclaude install` (with or without `--force`), so both `./update.sh` (`update.sh:8`) and Coder's `ironclaude/install.sh` reach it. | `source.md:307` | none (section-ref §3.1) |
| INF-132 | It removes only user-scope MCP registrations of `codebase-memory-mcp` and `serena` that IronClaude can prove it wrote, plus IronClaude's own receipt and marker files once the binary they describe is gone. | `source.md:307` | none (section-ref §3.1) |
| INF-133 | Nothing Coder-owned or upstream-owned is removed; all indexes, caches and memories are kept. | `source.md:307` | none (section-ref §3.1) |
| INF-134 | **codebase-memory-mcp (removed when it matches):** top-level user entry whose `command` is an absolute path with basename `codebase-memory-mcp`, `type` `stdio` or absent, `args` absent or `[]`, `env` and `headers` absent or empty (IronClaude registered whatever discovery found, `install_mcp.py:866`). | `source.md:313` | none (section-ref §3.2) |
| INF-135 | **Binary gate:** if `command` equals `<home>/.local/bin/codebase-memory-mcp` (unresolved `Path.home().absolute()`) and that file exists, keep it (kind B: upstream-installed binary still present). A `command` pointing at a `.local/bin/codebase-memory-mcp` path under a **different** home is also kept ("kept: path differs from current HOME"). | `source.md:313` | Task 18 |
| INF-136 | Every other matching entry (Coder's `/usr/local/bin`, any other path, the current home's `~/.local/bin` path whose binary is gone) is removed. A non-matching shape is kept: "kept: not an IronClaude registration". | `source.md:313` | Task 18 |
| INF-137 | **serena, Tier R (removed):** exact `command` + `args` match, `type` `stdio` or absent, `env` and `headers` each absent or `{}` (`claude mcp add` and Coder's bundle write `"env":{}`; the live entry on this workspace has it, `jq '.mcpServers.serena.env' ~/.claude.json` prints `{}`). | `source.md:315` | Task 18 |
| INF-138 | Removed unconditionally, whatever `codegraph_ready()` says (Phase 2 spec §2.12). Each row is pinned by a test: | `source.md:315` | none (section-ref §3.2) |
| INF-139 | (a) \| IronClaude registry `050d5ea2`..`0e7bc31f^` \| `uvx` \| `["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "ide-assistant", "--enable-web-dashboard", "false", "--enable-gui-log-window", "false"]` | `source.md:319` | none (section-ref §3.2) |
| INF-140 | (b) \| pre-fork `setup/components/mcp.py` `5bee1571` \| `uvx` \| `["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "ide-assistant", "--project", "$(pwd)"]` | `source.md:320` | none (section-ref §3.2) |
| INF-141 | (c) \| pre-fork `setup/components/mcp.py` `43112779` \| `serena` \| `["start-mcp-server", "--context", "ide-assistant", "--project", "$(pwd)"]` | `source.md:321` | none (section-ref §3.2) |
| INF-142 | **serena, Tier K (kept, one printed line per run; matched with `env` and `headers` each absent or `{}`; kept by Phase 1 alone only until Phase 2's `codegraph_ready()` gate removes it, Phase 2 spec §2.12; a launcher with a non-empty `env` or `headers` is reported as "kept: customised registration" and is never removed, not even by that gate):** the current pin... | `source.md:325` | Task 4 |
| INF-143 | the bare `... --context ide-assistant` form (`00ec67c7`, identical to the old hand command); the `--project <absolute path>` family; any other user `serena` entry whose argv contains `start-mcp-server`. | `source.md:325` | none (section-ref §3.2) |
| INF-144 | Printed: "Legacy Serena registration kept until codegraph is ready (IronClaude cannot prove it wrote it; the next `superclaude install` that installs codegraph removes it). Remove it now with `claude mcp remove serena --scope user`." | `source.md:325` | Task 18 |
| INF-145 | A `serena` entry without `start-mcp-server` is "kept: not a Serena launcher registration". | `source.md:325` | Task 16 |
| INF-146 | **Receipt and marker (deleted):** `~/.local/bin/.superclaude-codebase-memory.json` and `~/.local/bin/.superclaude-codebase-memory.pending`, only when `~/.local/bin/codebase-memory-mcp` is absent and each file passes the existing private-file predicates... | `source.md:327` | Task 4 |
| INF-147 | Otherwise listed, not deleted. These are the only files the step ever deletes. | `source.md:327` | none (section-ref §3.2) |
| INF-148 | T3 copies the small predicate logic into the retire module, because T5 deletes `install_codebase_memory.py`. | `source.md:327` | none (section-ref §3.2) |
| INF-149 | **Never touched:** local scope (`projects.*.mcpServers`) and project `.mcp.json`, whatever the name; every binary; uv tools; the upstream updater `~/.local/bin/install.sh`; upstream client companions; `~/.cache/codebase-memory-mcp`, `~/.serena`, project `.serena/`; user permissions; the hook matcher... | `source.md:331` | none (section-ref §3.3) |
| INF-150 | Delete commands are printed, labelled "only if you no longer need them", never run. | `source.md:332` | none (section-ref §3.3) |
| INF-151 | **One pure classifier** `classify_retired_entries() -> list[(name, verdict, reason)]` reads all state once (via `read_user_mcp_entry(name)`, `install_mcp.py:714-754`), then actions run in a fixed order: (1) receipt/marker cleanup, (2) codebase-memory registration, (3) serena registration. | `source.md:333` | none (section-ref §3.3) |
| INF-152 | **Removal helper** `_remove_exact_user_entry(name, matcher)` in `install_mcp.py` (replaces the name-only `_cleanup_user_native_registration`, `:916-948`; Phase 2 reuses it): re-read and re-match immediately before `claude mcp remove <name> --scope user`; re-read after (absent -> removed; same shape -> "could not verify" warning; different shape -> "replaced concurrently, kept", never retried). | `source.md:334` | none (section-ref §3.3) |
| INF-153 | **Bounds:** exec `claude` directly as an argv list (not the existing `_run_command`, which runs `$SHELL -c` with `shell=True`, `install_mcp.py:129-141`, so its timeout kills only the shell), `start_new_session=True`, kill the process group on timeout, 10 s per call, 15 s cap for the whole step. No subprocess when nothing needs removal. | `source.md:335` | Task 4 |
| INF-154 | **Placement:** in `main.py` `install()`, in the slot of the deleted codebase-memory phase (baseline `main.py:254`), before the exit-code block, inside its own `try/except Exception` that only warns. | `source.md:336` | Task 4 |
| INF-155 | **Non-fatal:** no outcome changes the install exit code (`update.sh:2` runs under `set -euo pipefail`; a non-zero install would stop `make sync-dev` and `doctor`). | `source.md:337` | none (section-ref §3.3) |
| INF-156 | Lookup "unknown" \| warning naming the cause (empty `CLAUDE_CONFIG_DIR`, unreadable or unparseable file, duplicate key, non-object) plus `claude mcp remove <name> --scope user` | `source.md:341` | none (section-ref §3.3) |
| INF-157 | Entry changed before removal \| kept, reported, not retried | `source.md:342` | none (section-ref §3.3) |
| INF-158 | Same shape after removal \| "could not verify" warning with the manual command | `source.md:343` | none (section-ref §3.3) |
| INF-159 | Per-call timeout (10 s) / step cap (15 s) \| process group killed or remaining calls skipped; warning; next install retries (idempotent) | `source.md:344` | none (section-ref §3.3) |
| INF-160 | `shutil.which("claude")` is None \| skip note printing the exact `claude mcp remove <name> --scope user` per entry that would have been removed | `source.md:345` | Task 18 |
| INF-161 | Receipt/marker fails a predicate \| listed, not deleted | `source.md:346` | Task 4 |
| INF-162 | Any other exception \| caught; warning only | `source.md:347` | none (section-ref §3.3) |
| INF-163 | `superclaude install --list`: the deleted codebase-memory block (baseline `main.py:161-186`) is replaced by one line per retired name: "absent", "will be removed (IronClaude shape)" or "kept: <reason>". | `source.md:351` | none (section-ref §3.4) |
| INF-164 | `superclaude doctor`: a new check that **warns, never fails**, when the classifier still finds a removable entry (`update.sh:10` exit unchanged; `doctor.py:16-49`). | `source.md:352` | none (section-ref §3.4) |
| INF-165 | `superclaude update`: prints only "legacy registration present: run `superclaude install`" (keeps its never-touches-MCP contract, `docs/user-guide/mcp-installation.md:24`). | `source.md:353` | Task 4 |
| INF-166 | Messages, one line per action: after any removal, "Restart running Claude sessions; a running session can write the entry back. Check with `superclaude install --list`."; after a codebase-memory removal, "If you installed codebase-memory-mcp yourself, its own `uninstall` removes its client companions.";... | `source.md:354` | none (section-ref §3.4) |
| INF-167 | after a Tier R `serena` removal, the exact removed `command` + `args`, plus "To keep using Serena, register it yourself under the name `serena-local`, e.g. `claude mcp add --scope user serena-local -- uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false`"... | `source.md:354` | none (section-ref §3.4) |
| INF-168 | whenever `~/.local/bin/codebase-memory-mcp` exists, `"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"` labelled "for a codebase-memory you or IronClaude installed under ~/.local/bin; removes its own client companions, keeps indexes" (never a bare command, which could resolve to Coder's copy); | `source.md:354` | none (section-ref §3.4) |
| INF-169 | `uv tool uninstall serena-agent` labelled "if you installed it yourself; Coder workspaces reinstall it at start"; the Tier K line; the data delete commands. | `source.md:354` | none (section-ref §3.4) |
| INF-170 | New `src/superclaude/cli/install_retired_mcp.py`: `RETIRED_MCP_SERVERS` table (name -> matcher, with the comment "remove after the first release in which Coder's image and bundle no longer ship either server"), the classifier, receipt/marker predicates and cleanup, message builder, `run_retire_step()`. | `source.md:358` | Task 4 |
| INF-171 | `src/superclaude/cli/install_mcp.py`: `_remove_exact_user_entry(name, matcher)` and the direct-exec `claude` wrapper (generic, no server names). | `source.md:359` | Task 4 |
| INF-172 | `src/superclaude/cli/main.py`: the call in `install()`, the `install --list` lines, the `update` notice. `src/superclaude/cli/doctor.py`: the warn-only check. | `source.md:360` | Task 4 |
| INF-173 | New `tests/cli/test_install_retired_mcp.py`: table-driven classifier (every Tier R row removed; every Tier K row kept with the line printed; near misses: one token changed, extra or missing arg, expanded `$(pwd)`; non-empty `env`/`headers` kept;... | `source.md:361` | none (section-ref §3.5) |
| INF-174 | `env: {}` and `headers: {}` count as absent (a Tier R row carrying `"env":{}` is removed; the current pin carrying `"env":{}`, the live shape, is Tier K); the re-register hint names `serena-local`; relative cbm command kept; cbm `.local/bin` path under a different home kept with "path differs from current HOME"; | `source.md:361` | Task 4 |
| INF-175 | a Tier R serena removal prints the removed argv and the re-register command; local-scope and `.mcp.json` entries ignored; binary, receipt and marker states, including "receipt present, binary absent" converging in one run); | `source.md:361` | Task 4 |
| INF-176 | helper (concurrent replacement kept, not retried; verify failure warns); bounds (stub `claude` that hangs: process group killed, 15 s cap honoured; missing CLI: skip note); | `source.md:361` | none (section-ref §3.5) |
| INF-177 | CLI integration (temp HOME, stub `claude`, install exit code unchanged when the step fails); `superclaude update` and `doctor` never mutate and never change their exit code. | `source.md:361` | Task 4 |
| INF-178 | Unchanged contract: `tests/cli/test_update_script.py` (`update.sh` list and order) still passes. | `source.md:362` | none (section-ref §3.5) |
| INF-179 | The current `serena-agent==1.7.0` registration is kept by Phase 1 alone on every workspace (including this one), with the removal command printed on every install | `source.md:368` | Task 18 |
| INF-180 | **Decision:** Phase 1 leaves no step that names a tool absent after Phase 1, at any commit. Load-bearing Serena symbol, reference, diagnostics and allowlist references are **triaged, then deleted or rewritten to a named native floor in Phase 1**; they are not deferred to Phase 3. | `source.md:380` | none (section-ref §4) |
| INF-181 | **Triage first.** For each load-bearing SYM/REF/DIAG/ALLOW row (`primitive-usage.md` section 4 lists them): **delete** the Serena half when the same step already names a Serena-free Read/Grep/Glob/auggie path (examples:... | `source.md:388` | none (section-ref §4.1) |
| INF-182 | **rewrite** it when there is no fallback, the fallback is "skip", or the fallback itself calls Serena | `source.md:388` | Task 13 |
| INF-183 | **Floor per job** (phrased as tools, never as shell commands): symbol lookup or outline -> Grep for the definition (`def name\\|class name\\|function name`), then Read the range, auggie first where the primitive already uses it; references -> Grep with a word-boundary pattern for the symbol, then Read the call sites; implementations and type hierarchy -> Grep for `class .*\(<Base>\)` or `implements <Iface>`, marked "best effort" | `source.md:389` | none (section-ref §4.1) |
| INF-184 | **Closed read-only rosters** (`agents/reflect-reviewer.md`, `agents/troubleshoot-analyst.md`, `agents/reuse-auditor.md`) only lose `mcp__serena__*` names; the floor inside them is Read/Grep/Glob/auggie; Bash is never added | `source.md:390` | Task 13 |
| INF-185 | **Diagnostics:** `get_diagnostics_for_file` is dropped everywhere. Orchestrators whose `allowed-tools` already include Bash (reflect chain steps 5/5.5, `sc-troubleshoot-protocol`) run the project's own linter or type-checker through Bash under reflect's existing section 6.1.1 safety envelope (timeout, output cap, denylist), retitled for the Bash call. | `source.md:391` | Task 13 |
| INF-186 | Closed rosters say the orchestrator's verification leg covers diagnostics | `source.md:391` | none (section-ref §4.1) |
| INF-187 | **Every `tools:` / `allowed-tools:` line naming `mcp__serena__*` is load-bearing**, whatever its inventory label, and changes in the same commit as the skill body that drives that agent and its pinning test... | `source.md:392` | none (section-ref §4.1) |
| INF-188 | `mcp-servers:` frontmatter lists simply drop `serena` (no Python consumer, `primitive-usage.md` C13) | `source.md:392` | none (section-ref §4.1) |
| INF-189 | **Fallbacks that call Serena are rewritten, not trusted:** `agents/reuse-auditor.md:131` becomes "Grep by capability tokens + skeleton grep", F4 at `:57` uses a Grep reference search; `sc-validate-roadmap-protocol/SKILL.md:320-349` (Step 0.5) gets a Grep-definition floor with the same 30-lookup cap and the same INFORMATIONAL ONLY artifact, not "skip" | `source.md:393` | Task 15 |
| INF-190 | **reflect treats floor evidence as normal.** No `serena` degraded token is emitted; `"serena"` and `"serena:context-excluded"` leave `_DEGRADED_COMPONENTS_HALT_SET` (`src/superclaude/cli/reflect/contract.py:32-34`, verified) and the section 6.5 and section 10 fallback rows of the reflect SKILL.md. | `source.md:394` | Task 13 |
| INF-191 | T6 changes the CLI side with its fixtures; T11a changes the reflect skill side. | `source.md:394` | none (section-ref §4.1) |
| INF-192 | **reflect contract fields:** field names without "serena" stay stable with a producer or a constant: `find_declaration_no_match` (from a zero-hit Grep), `type_hierarchy_invoked: false` (step 4.5 deleted), `summarize_changes_invoked: false`, `references_extended_info_used: false`; Step 7 `search_deps` is skipped and its claim marked `[INFERRED]`. | `source.md:395` | Task 13 |
| INF-193 | **Exception (this spec's decision D4):** `serena_summary_corroboration` is deleted, not kept:... | `source.md:395` | Task 4 |
| INF-194 | **Slots ledger:** the executor writes `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`, one row per touched step: file, step heading or anchor (not a line number), former Serena tool, action (deleted / floor), floor used, contract fields touched. | `source.md:396` | Task 13 |
| INF-195 | the first T9-T11c task that deletes or rewrites a step creates it, every later T9-T11c edit appends to it, and T11c checks it covers every load-bearing file of section 4.2 | `source.md:396` | none (section-ref §4.1) |
| INF-196 | **Core rules file:** `src/superclaude/core/CLAUDE.md:112` (refresh-tool table, "Symbolic queries" row) becomes "Grep for the definition and references, then Read" (Phase 3 adds codegraph); `:21` (MCP table row) and the `replace_symbol_body` item of rule S2 (`:90`) are deleted (T9) | `source.md:397` | Task 15 |
| INF-197 | Every row has a `plugins/superclaude/` or root `commands/`, `agents/` twin where section 1.2 lists one; twins are edited identically in the same commit. | `source.md:401` | Constraints |
| INF-198 | `rg -n "${EX[@]}" 'mcp__serena__' src/superclaude plugins/superclaude commands agents` prints nothing. | `source.md:405` | Task 15 |
| INF-199 | No primitive step names a tool absent from its own roster: for each agent and skill with a `tools:` or `allowed-tools:` line, every `mcp__<server>__<tool>` named in its body is in that line (T11a-T11c run the check script in section 8.0). | `source.md:406` | none (section-ref §4.3) |
| INF-200 | Serena memory is replaced in Phase 1 by plain markdown files; codegraph takes no memory job. | `source.md:410` | none (section-ref §5) |
| INF-201 | Store: `<project>/.superclaude/memory/<key>.md`, flat markdown, subfolders for topics. Tool mapping: `write_memory` -> Write, `read_memory` -> Read, `list_memories` -> Glob `.superclaude/memory/**/*.md`, `edit_memory` -> Edit, `delete_memory` -> delete only through the user (no primitive deletes memories) | `source.md:414` | Task 11 |
| INF-202 | `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory outside git: one store per worktree | `source.md:415` | Constraints |
| INF-203 | On first write, if `<project>/.superclaude/.gitignore` is absent, create it with the single line `*` (the repo-level `.superclaude/` ignore exists only in IronClaude, `.gitignore:114`) | `source.md:416` | Task 11 |
| INF-204 | Single-owner keys (`pm_context`, `last_session`, `next_actions`) are overwritten whole; keys parallel sessions may write (`checkpoint`, `decision`, handoffs) are written as `<key>-<session-or-timestamp>.md` and never edited in place | `source.md:417` | Task 11 |
| INF-205 | Reflect cold-start calibration moves to tracked `docs/memory/reflect/deviation-patterns-<slug>.md`; T13 moves `.serena/memories/reflect/deviation-patterns-IronClaude.md` there with `git mv` (content kept) | `source.md:418` | Task 12 |
| INF-206 | `sc-roadmap-protocol`: the existing `<output_dir>/.session-memory.md` fallback becomes the only path; the Serena branches go away | `source.md:419` | Task 10 |
| INF-207 | `/sc:load` reads `.serena/memories/<key>.md` when `.superclaude/memory/<key>.md` is absent, for one release; never writes there; tells the user the folder is read-only history (allowlisted in 2.4) | `source.md:420` | Task 11 |
| INF-208 | Delete, do not port, the Serena-only non-memory calls: `think_about_*`, `summarize_changes`, `activate_project`, `onboarding`, `check_onboarding_performed`, `prepare_for_new_conversation`, `get_current_config`, and reflect's `--onboard` flow (Steps 0.5c, 0.7, 0.7b) with `refs/ops-integration.md`'s Serena WARN catalog | `source.md:421` | none (section-ref §5) |
| INF-209 | `skills/sc-validate-roadmap-protocol/SKILL.md` (ledger, terminology map, pattern log keys move to `.superclaude/memory/validate-roadmap/<key>.md`, still fail-open) | `source.md:423` | Task 12 |
| INF-210 | `scripts/bootstrap_scan.sh:146-147` fields renamed `has_memory`, `memory_count`, reading `.superclaude/memory` | `source.md:423` | Task 12 |
| INF-211 | `core/RULES.md` lines 49-50 stay (the commands stay). | `source.md:423` | none (section-ref §5) |
| INF-212 | Phase 1 does **not** edit any other repository (planning rule, and no cross-repo authorization); it ships these notes. T15 copies each note to the Phase 1 task package as `handoffs/<repo>.md` so an owner can paste it into an agent session in that repository. | `source.md:429` | Constraints |
| INF-213 | The 310 historical paths (`.dev/`, `claudedocs/`, completed logs, `.serena/memories/` records) are listed in `org-repos.md` "Keep (historical)" and must not be edited or deleted by any handoff. | `source.md:449` | none (section-ref §6.1) |
| INF-214 | The Coder part is **merged into Phase 2's Coder handoff** (Phase 2 spec, task P2), because the Coder change must also bake codegraph... | `source.md:453` | Task 19 |
| INF-215 | Facts Phase 2's handoff must carry from Phase 1: (1) after Phases 1+2 merge, `superclaude install` no longer registers `codebase-memory-mcp`,... | `source.md:453` | Constraints |
| INF-216 | Each note is self-contained. Common rules repeated inside each: do not edit historical records; do not delete project knowledge (`.serena/memories/*` content is moved, not deleted); open the PR on that repository's own origin. | `source.md:457` | none (section-ref §6.3) |
| INF-217 | Repo: IronbellyOrg/Financials. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena and codebase-memory MCP servers; codegraph replaces code navigation later (IronClaude Phase 3). | `source.md:462` | Constraints |
| INF-218 | Repo: IronbellyOrg/IronFlow. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena and codebase-memory MCP servers. | `source.md:474` | Constraints |
| INF-219 | Repo: IronbellyOrg/IronOps. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena and codebase-memory MCP servers. | `source.md:486` | Constraints |
| INF-220 | Repo: IronbellyOrg/InfraDocs. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server. | `source.md:498` | Constraints |
| INF-221 | Repo: IronbellyOrg/ClaudeCodeCodeAudit. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server; this repo's audit workflow documents prescribe Serena navigation and memory and require Serena tool evidence. | `source.md:509` | none (section-ref §6.3) |
| INF-222 | Repo: IronbellyOrg/Ironbrain. Context: IronClaude (issue IronbellyOrg/IronClaude#323) replaced codebase-memory with codegraph (https://github.com/colbymchenry/codegraph). | `source.md:521` | Constraints |
| INF-223 | Repo: IronbellyOrg/Octodive. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server. | `source.md:530` | Constraints |
| INF-224 | Repo: IronbellyOrg/TUIBBS. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server. | `source.md:539` | Constraints |
| INF-225 | Repo: IronbellyOrg/TUIBBS-scp. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server. | `source.md:550` | Constraints |
| INF-226 | Repo: IronbellyOrg/shrapnel-gov. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server. | `source.md:559` | Constraints |
| INF-227 | Repo: IronbellyOrg/llm-workflows. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server. | `source.md:571` | Constraints |
| INF-228 | One commit per task (conventional commit, ending with the attribution line the executor's session requires); every commit stages the task package (`git add .dev/tasks`) and never stages `.claude/` (except `.claude/settings.json`, which Phase 1 does not touch). After each group's last commit the executor posts the section 9 issue comment. | `source.md:604` | Constraints |
| INF-229 | Tasks run in the listed order; no task needs a later task to go green. | `source.md:604` | Constraints |
| INF-230 | `$PKG/artifacts/acceptance-search.sh` (prints every residual hit that is not allowlisted in section 2.4; exit 1 if any): | `source.md:610` | Task 16 |
| INF-231 | `$PKG/artifacts/check_rosters.py` (rule 4.3 #2: every `mcp__<server>__<tool>` a primitive body names must be in its own `tools:` / `allowed-tools:` line; prints violations): | `source.md:627` | none (section-ref §8.0) |
| INF-232 | Run it as `uv run --no-project python -I $PKG/artifacts/check_rosters.py`. Violations that already exist at baseline for other servers are out of scope; the check is "no line that is not in the T0 output, and no `serena` line". | `source.md:646` | Task 15 |
| INF-233 | Pytest runs use `-p no:cacheprovider`; full-suite runs set `T02_15_PERF_REPORT=/tmp/p1-perf.json` (section 10). After every test run: `git status --short` lists only intended files. | `source.md:648` | Constraints |
| INF-234 | Files: `$PKG/artifacts/acceptance-search.sh`, `$PKG/artifacts/check_rosters.py`, `$PKG/artifacts/baseline/*` (no source change). | `source.md:653` | Task 1 |
| INF-235 | Change: `make sync-dev` (the audit tests need the `.claude/` mirror, `inventory/codebase-memory.md` 4.0); write the two helpers from 8.0; record baselines: | `source.md:654` | Task 1 |
| INF-236 | `uv run pytest tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_update_command.py tests/docs/test_tavily_doc_alignment.py -q -p no:cacheprovider \| tee $PKG/artifacts/baseline/cbm.txt` | `source.md:655` | Task 1 |
| INF-237 | `uv run pytest tests/cli/reflect tests/troubleshoot tests/sc-roadmap tests/core tests/commands tests/skills tests/recommend tests/hooks tests/unit/test_cli_install.py tests/cli/test_install_hooks.py tests/cli/test_update_script.py -q -p no:cacheprovider \| tee $PKG/artifacts/baseline/targeted.txt` | `source.md:656` | Task 1 |
| INF-238 | `T02_15_PERF_REPORT=/tmp/p1-perf.json uv run pytest -q -p no:cacheprovider --tb=line \| tee $PKG/artifacts/baseline/full.txt` | `source.md:657` | Task 1 |
| INF-239 | `bash $PKG/artifacts/acceptance-search.sh all > $PKG/artifacts/baseline/search.txt; uv run --no-project python -I $PKG/artifacts/check_rosters.py > $PKG/artifacts/baseline/rosters.txt` | `source.md:658` | Task 1 |
| INF-240 | Acceptance: `test -s $PKG/artifacts/baseline/full.txt && test -s $PKG/artifacts/baseline/targeted.txt && grep -q 'ACCEPTANCE_SEARCH_FAIL' $PKG/artifacts/baseline/search.txt && test -z "$(git status --short -- . ':!.dev')"` | `source.md:659` | Task 1 |
| INF-241 | **Group G0 done:** issue comment (section 9) with the baseline pass/fail counts. | `source.md:661` | Task 1 |
| INF-242 | Files: new `tests/cli/test_install_mcp_cli.py`. | `source.md:666` | Task 2 |
| INF-243 | Change: `inventory/codebase-memory.md` 4.1 exactly: own home fixture and an `mcp_cli` fixture without any `native`/`install_codebase_memory_mcp` patching; port the 11 tests listed there (971 without `--uninstall`/`--yes` cases, 1126, 1195, 1217, 1229, 1274, 1285, 1298, 1306 and 1114 with `context7` instead of cbm, 1334 gateway part only). | `source.md:667` | Task 2 |
| INF-244 | Acceptance: `uv run pytest tests/cli/test_install_mcp_cli.py -q -p no:cacheprovider` passes, and `uv run pytest tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_update_command.py tests/docs/test_tavily_doc_alignment.py -q -p no:cacheprovider` still shows the T0 `cbm.txt` counts. | `source.md:668` | Task 2 |
| INF-245 | Files: `src/superclaude/cli/main.py`, `tests/cli/test_update_command.py`, `tests/cli/test_install_codebase_memory.py`. | `source.md:672` | Task 3 |
| INF-246 | Change: `inventory/codebase-memory.md` 4.2 exactly (main.py `:66`, `:78-83`, `:161-186`, `:254-262`, the `native_success` exit term, help text `:38`, `:44`, `:50-52`; fixture `native_phase_guard` reduced to `HOME`, `CLAUDE_CONFIG_DIR` and the plugin/Orca stubs; delete 5 test functions, rewrite the `--force` test; delete the cross-entry fixture and tests at `:1382`, `:1517`, `:1614`). | `source.md:673` | Task 3 |
| INF-247 | The fixture and `main.py` change in the same commit (hazard: the real-install tests would otherwise reach the real upstream installer). | `source.md:673` | Task 3 |
| INF-248 | Acceptance: `uv run pytest tests/cli/test_update_command.py tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_cli.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py -q -p no:cacheprovider` passes, and `rg -n "install_codebase_memory\|_NATIVE_INSTALLER\|native_phase_guard" src/superclaude/cli/main.py tests/cli/test_update_command.py` prints nothing. | `source.md:674` | Task 3 |
| INF-249 | Files: section 3.5 (new `src/superclaude/cli/install_retired_mcp.py` and `tests/cli/test_install_retired_mcp.py`; `install_mcp.py` remover and direct-exec wrapper; `main.py` install call, `install --list` lines, `update` notice; `doctor.py` warn-only check), plus `tests/cli/test_update_command.py` (expected call list includes the retire step after user setup). | `source.md:678` | Task 4 |
| INF-250 | Change: implement section 3 exactly (matchers 3.2, behaviour 3.3, surfaces and messages 3.4, tests 3.5). The retire module must not import `install_codebase_memory.py` (deleted in T5). | `source.md:679` | Task 4 |
| INF-251 | The literal server names live only in `install_retired_mcp.py` and its test (allowlisted, section 2.4); `main.py` and `doctor.py` take names and messages from the module. | `source.md:679` | Task 4 |
| INF-252 | Acceptance: `uv run pytest tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py tests/cli/test_update_script.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_cli.py tests/unit -q -p no:cacheprovider` passes; `rg -n 'install_codebase_memory' src/superclaude/cli/install_retired_mcp.py` prints nothing;... | `source.md:680` | Task 4 |
| INF-253 | `rg -c 'codebase-memory-mcp\|serena' "$T/list.txt"` prints at least 2 (one line each, both "absent"); then `rm -rf "$T"`. | `source.md:680` | Task 4 |
| INF-254 | Files: `src/superclaude/cli/main.py`, `src/superclaude/cli/install_mcp.py`, `tests/cli/test_install_codebase_memory.py`, `tests/cli/test_install_mcp_tavily.py`, `tests/cli/test_install_mcp_registry.py`, `tests/cli/test_install_mcp_cli.py`. | `source.md:684` | Task 5 |
| INF-255 | Change: `inventory/codebase-memory.md` 4.3 (delete `--uninstall`/`--yes`, the native blocks of `install_mcp.py` listed under its row C2, menu becomes "1. Install MCP servers (default)" / "2. Cancel"; delete `T-icm` 834-1380, `T-tav` 382-end, `T-reg` 192-240; port the 5 deferred menu tests; add one `mcp --list` output test), **except** keep `read_user_mcp_entry` and `_run_registration_command` and the remover from T3 (section 7). | `source.md:685` | Task 5 |
| INF-256 | Add `"codebase-memory-mcp"` to the `test_removed_mcp_servers_are_not_in_registry` tuple. | `source.md:685` | Task 5 |
| INF-257 | Acceptance: `uv run pytest tests/cli/test_install_mcp_cli.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_codebase_memory.py tests/cli/test_update_command.py tests/cli/test_install_retired_mcp.py tests/docs/test_tavily_doc_alignment.py tests/recommend -q -p no:cacheprovider` passes, and `rg -n "codebase_memory\|_native_\|install_codebase_memory_mcp\|uninstall_codebase_memory_mcp\|--uninstall\|--yes" src/superclaude/cli/main.py src/superclaude/cli/install_mcp.py` prints nothing. | `source.md:686` | Task 5 |
| INF-258 | Files: `git rm src/superclaude/cli/install_codebase_memory.py tests/cli/test_install_codebase_memory.py`. | `source.md:690` | Task 6 |
| INF-259 | Acceptance: `rg -n "install_codebase_memory\|codebase_memory" src tests -g '!src/superclaude/cli/install_retired_mcp.py' -g '!tests/cli/test_install_retired_mcp.py'` prints nothing (the retire step and its test are allowlisted, section 2.4; review finding X-17);... | `source.md:692` | Task 4 |
| INF-260 | `uv run pytest tests/cli tests/unit tests/recommend tests/docs -q -p no:cacheprovider --ignore=tests/cli/eval` has no failure that is not in `$PKG/artifacts/baseline/full.txt`; `uv run ruff check src/superclaude/cli tests/cli` passes; `bash $PKG/artifacts/acceptance-search.sh cbm src tests` prints `ACCEPTANCE_SEARCH_OK cbm`. | `source.md:692` | Task 6 |
| INF-261 | Files: `src/superclaude/cli/reflect/{contract.py,ensemble.py,config.py}`, the 25 `tests/cli/reflect/fixtures/*.yaml` rows S58-S82, `tests/cli/reflect/{test_verdict_mapping.py,test_runner_e2e.py,test_ensemble_unit.py,test_verify_denylist_git_mutations.py}`. | `source.md:699` | Task 7 |
| INF-262 | drop `"serena"` and `"serena:context-excluded"` from `_DEGRADED_COMPONENTS_HALT_SET` and fix the comment (`contract.py:28-34`); delete the `serena_summary_corroboration` key (`ensemble.py:824`) and its line in 24 fixtures; delete `fixtures/degraded_serena.yaml`; `degraded_with_drift.yaml` `- serena` -> `- auggie`; | `source.md:700` | Task 7 |
| INF-263 | delete `test_degraded_serena` and `test_serena_summary_corroboration_unavailable_not_degraded`, edit the token list at `test_verdict_mapping.py:245`; repoint `test_runner_e2e.py:71` to `degraded_tier1.yaml` and confirm it still asserts exit 11; | `source.md:700` | Task 7 |
| INF-264 | Acceptance: `uv run pytest tests/cli/reflect -q -p no:cacheprovider` passes (W2 predicts 270 tests); `rg -n -i 'serena' src/superclaude/cli/reflect tests/cli/reflect` prints nothing. | `source.md:701` | Task 7 |
| INF-265 | Files: `src/superclaude/hooks/hooks.json`, `plugins/superclaude/hooks/hooks.json`, `src/superclaude/hooks/scripts/freshness-pre-edit.sh`, `plugins/superclaude/hooks/scripts/freshness-pre-edit.sh`, `tests/cli/test_install_hooks.py`, `src/superclaude/cli/eval/suites/real.yaml`, `src/superclaude/cli/eval/coverage.py`, `src/superclaude/cli/eval/suites/README.md`, `tests/cli/eval/test_coverage_gate.py`. | `source.md:705` | Task 8 |
| INF-266 | Change: matcher becomes `Edit\|Write` (`hooks.json:47` and plugin `:37`); rows D1/D2 (drop the `relative_path` branch); delete the four asserts at `test_install_hooks.py:684-687`; `real.yaml`: delete capability row `:40` and eval E8 (`:566-690`), fix comments... | `source.md:706` | Task 8 |
| INF-267 | swap the tool string at `test_coverage_gate.py:127` to `mcp__context7__resolve-library-id`. | `source.md:706` | Task 8 |
| INF-268 | Acceptance: `uv run pytest tests/cli/test_install_hooks.py tests/hooks tests/cli/eval/test_coverage_gate.py tests/cli/eval/test_no_mcp_skip.py tests/cli/eval/test_schema_validate.py tests/cli/eval/test_capability_gates.py -q -p no:cacheprovider` passes; `rg -n 'mcp__serena\|relative_path' src/superclaude/hooks plugins/superclaude/hooks src/superclaude/cli/eval tests/cli/test_install_hooks.py tests/cli/eval/test_coverage_gate.py` prints nothing. | `source.md:707` | Task 8 |
| INF-269 | Files: `src/superclaude/cli/install_mcp.py` (`:55-61`, `:561-570`), delete `src/superclaude/mcp/{MCP_Serena.md,configs/serena.json,configs/serena-docker.json}` and the same three under `plugins/superclaude/mcp/`,... | `source.md:711` | Task 9 |
| INF-270 | Change: `inventory/serena.md` step S4 without the cleanup step (T3 owns it); add `"serena"` to the `test_removed_mcp_servers_are_not_in_registry` tuple. | `source.md:712` | none (row-ref S4) |
| INF-271 | Acceptance: `uv run pytest tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_cli.py tests/unit/test_cli_install.py tests/cli/test_update_command.py -q -p no:cacheprovider` passes; `rg -n -i serena src/superclaude/cli/install_mcp.py src/superclaude/mcp plugins/superclaude/mcp tests/unit/test_cli_install.py` prints nothing; `uv run superclaude mcp --servers serena --dry-run 2>&1 \| grep -q 'Unknown MCP server selection: serena'` succeeds. | `source.md:713` | Task 9 |
| INF-272 | every edit to `src/superclaude/...` is mirrored by hand in its `plugins/superclaude/...` twin and root `commands/sc-*.md` / `agents/sc-*.md` copy in the same commit | `source.md:717` | Constraints |
| INF-273 | plus `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py` (delete `test_serena_fallback`, `test_serena_referenced`) and `tests/sc-roadmap/integration/test_wave5_completion.py` (delete `test_circuit_breaker_for_serena`, reword `:69-74`). | `source.md:720` | Task 10 |
| INF-274 | Change: delete the Serena entries and lines named in each row's action; no body text may still point at Serena. | `source.md:721` | Task 10 |
| INF-275 | Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/sc-roadmap tests/commands tests/skills tests/core tests/cli/test_how_we_work_install.py -q -p no:cacheprovider` passes; `rg -n --no-ignore 'mcp-servers:.*serena' src/superclaude plugins/superclaude commands agents` prints nothing. | `source.md:722` | Task 10 |
| INF-276 | Memory parts of a `T10, T11` row go to the T10 piece, tool parts to the T11 piece. Repo-wide searches run only on the last piece of each pair (T10b, T11c); earlier pieces run the same search scoped to their own files. | `source.md:725` | none (section-ref §8) |
| INF-277 | Files: rows P1, P4, P5, P8 (root `commands/sc-{load,pm,save}.md`, `agents/sc-pm-agent.md`), P11, P13, P14, P17, P23 (`plugins/superclaude/` twins), P27, P39, P40, P47, P57 (`src/superclaude/agents/pm-agent.md`, `commands/{load,pm,save}.md`, `modes/MODE_Task_Management.md`), P73 (`src/superclaude/skills/sc-pm-protocol/SKILL.md`; kept with `/sc:pm` because `src/superclaude/commands/pm.md:52` loads `sc:pm-protocol`). | `source.md:728` | Task 11 |
| INF-278 | Change: rules M1-M4, M7, M8 for these files. | `source.md:729` | Task 11 |
| INF-279 | Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/commands tests/skills tests/core -q -p no:cacheprovider` passes; `rg -n --no-ignore 'write_memory\|read_memory\|list_memories\|edit_memory\|delete_memory\|think_about_\|\bsummarize_changes\b\|activate_project\|check_onboarding_performed\|prepare_for_new_conversation\|get_current_config' src/superclaude/commands/{save,load,pm}.md... | `source.md:730` | Task 11 |
| INF-280 | `rg --files-without-match '\.superclaude/\.gitignore' src/superclaude/commands/save.md src/superclaude/agents/pm-agent.md src/superclaude/skills/sc-pm-protocol/SKILL.md src/superclaude/modes/MODE_Task_Management.md` prints nothing (rule M3 in every writer). | `source.md:730` | Task 11 |
| INF-281 | Files: memory parts of rows P6, P15, P43 (reflect commands), P50 and P96 (validate-roadmap command and skill), P77 (reflect SKILL.md), P91 (sc-task-protocol STRICT memory steps); rows P68-P71 (crash-recovery), P82, P85 (reflect refs), P24 and P52... | `source.md:734` | Task 12 |
| INF-282 | S4 (`git mv .serena/memories/reflect/deviation-patterns-IronClaude.md docs/memory/reflect/deviation-patterns-IronClaude.md`, rule M5). | `source.md:734` | Task 12 |
| INF-283 | Change: rules M1-M8 for these files. After editing `HOW-WE-WORK.md`, copy it byte for byte to the plugin copy; if the edit touches the block between `<!-- level-table:v1 -->` and `<!-- /level-table -->`, re-copy that block into `src/superclaude/core/CLAUDE.md:50-67` (project `CLAUDE.md` rule; `tests/core/test_claude_md_routing_block.py`). | `source.md:735` | Constraints |
| INF-284 | Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/core tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py tests/recommend tests/skills tests/sc-roadmap -q -p no:cacheprovider` passes; `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` succeeds;... | `source.md:736` | Task 12 |
| INF-285 | prints nothing (repo-wide, both T10 pieces); `test -f docs/memory/reflect/deviation-patterns-IronClaude.md`. | `source.md:736` | Task 12 |
| INF-286 | Files: tool parts of rows P6, P15, P43 (reflect commands) and P77 (reflect SKILL.md, including the section 6.1.1 envelope retitle, rule G4); rows P78, P79, P80, P81, P83, P84, P86, P87 (reflect refs);... | `source.md:740` | Task 13 |
| INF-287 | P28 (`agents/reflect-reviewer.md`, reflect's fixed reviewer type) and P29 (`agents/reuse-auditor.md`, driven by reflect step 4a, whose Serena fallback is in reflect SKILL.md section 6.1); D3, D4, D5 (reflect tests). | `source.md:740` | Task 13 |
| INF-288 | Change: rules G1-G9 for these files. The first T9-T11c task that deletes or rewrites a step creates the slots ledger `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` (rule G9); this task appends a row for every reflect, reflect-reviewer and reuse-auditor step it touches. | `source.md:741` | Task 13 |
| INF-289 | Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/cli/reflect tests/skills tests/commands -q -p no:cacheprovider` passes; `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude/skills/sc-reflect-protocol src/superclaude/commands/reflect.md plugins/superclaude/commands/reflect.md commands/sc-reflect.md src/superclaude/agents/reflect-reviewer.md src/superclaude/agents/reuse-auditor.md` prints `ACCEPTANCE_SEARCH_OK serena`;... | `source.md:742` | Task 13 |
| INF-290 | `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py \| sort)` prints nothing; `test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`. | `source.md:742` | Task 13 |
| INF-291 | Files: rows P49 (`src/superclaude/commands/troubleshoot.md`), P93, P94, P95 (`sc-troubleshoot-protocol` SKILL.md and refs), P31 (`agents/troubleshoot-analyst.md:5`), S99 (`tests/troubleshoot/test_diagnostic_worker_contract.py:17-26,152`), all in one commit (rule G5: the roster, the prose roster at `sc-troubleshoot-protocol/SKILL.md:31` and the pinning test change together). | `source.md:746` | Task 14 |
| INF-292 | Change: rules G1-G9 for these files; append the touched steps to the slots ledger. | `source.md:747` | Task 13 |
| INF-293 | Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/troubleshoot tests/skills tests/commands -q -p no:cacheprovider` passes; `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude/skills/sc-troubleshoot-protocol src/superclaude/commands/troubleshoot.md src/superclaude/agents/troubleshoot-analyst.md` prints `ACCEPTANCE_SEARCH_OK serena`;... | `source.md:748` | Task 14 |
| INF-294 | `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py \| sort)` prints nothing; `rg -q 'sc-troubleshoot-protocol' .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`. | `source.md:748` | Task 14 |
| INF-295 | Files: tool parts of rows P50 and P96 (validate-roadmap command and skill, rule G6 Step 0.5 floor) and P91 (sc-task-protocol STRICT prerequisites); rows P92 (`sc-tasklist-protocol/SKILL.md:683`), P26 and P33 (`agents/auggie-reviewer.md`, `commands/auggie-review.md`), P2, P62, P63 (brainstorm root command, skill and `refs/handoff-routing.md`), P65 (cleanup-audit skill), P22 and P56 (`MODE_Orchestration.md` twins), P25 and P76 (`delegation-vs-native-heuristics.md` twins), P51 line 112 (`core/CLAUDE.md` refresh-tool row, rule G10). | `source.md:752` | Task 15 |
| INF-296 | Change: rules G1-G10 for these files; append the touched steps to the slots ledger and check it covers every load-bearing file of section 4.2. | `source.md:753` | Task 15 |
| INF-297 | Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/troubleshoot tests/cli/reflect tests/skills tests/commands tests/core tests/roadmap/test_threshold_registry.py -q -p no:cacheprovider` passes; `rg -n --no-ignore 'mcp__serena__' src/superclaude plugins/superclaude commands agents` prints nothing;... | `source.md:754` | Task 15 |
| INF-298 | `for f in commands/troubleshoot.md skills/sc-reflect-protocol/SKILL.md skills/sc-troubleshoot-protocol/SKILL.md skills/sc-validate-roadmap-protocol/SKILL.md agents/reuse-auditor.md; do rg -qF "$f" .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md \|\| echo "ledger missing $f"; done` prints nothing; `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude plugins/superclaude commands agents` prints `ACCEPTANCE_SEARCH_OK serena`. | `source.md:754` | Task 15 |
| INF-299 | Files: rows C8-C12 and the section 1.2 rows with Task `T12` (`CLAUDE.md:377`, `README.md:38,64,75,219`, `SECURITY.md:328`, `docs/**` rows, `docs/troubleshooting/serena-installation.md` deleted, no inbound link: `rg serena-installation` is empty),... | `source.md:761` | Task 16 |
| INF-300 | `CHANGELOG.md` (new entry: what was removed, the retire step, the manual commands from section 3.4 for kind-B workspaces and user data; the entry must not say the current-pin Serena registration is kept for good: it says the registration is removed once codegraph is ready, Phase 2 spec §2.12, and names `serena-local` as the re-register name). | `source.md:761` | Task 16 |
| INF-301 | Change: per each row's action; no "Retired servers" section in user docs (decision D7; the CHANGELOG entry and the retire step's own output carry the manual commands). | `source.md:762` | Task 16 |
| INF-302 | Acceptance: `uv run pytest tests/docs tests/core -q -p no:cacheprovider` passes; `bash $PKG/artifacts/acceptance-search.sh all docs README.md CLAUDE.md SECURITY.md .github` prints `ACCEPTANCE_SEARCH_OK all`;... | `source.md:763` | Task 16 |
| INF-303 | `uv run --no-project python -c 'import yaml,sys; d=yaml.safe_load(open(".github/workflows/test.yml")); s=[x.get("name") for x in d["jobs"]["doctor-check"]["steps"]]; sys.exit(0 if "Install Claude CLI" in s else 1)'` exits 0 (step kept, row C12). | `source.md:763` | Task 16 |
| INF-304 | Files: `git rm .serena/project.yml .serena/memories/memory_maintenance.md .serena/.gitignore` (the calibration file already moved in T10b); `.gitignore:113` stays (section 2.4). | `source.md:767` | Task 17 |
| INF-305 | Acceptance: `git ls-files .serena` prints nothing; `test -f docs/memory/reflect/deviation-patterns-IronClaude.md`. | `source.md:768` | Task 17 |
| INF-306 | Files: `$PKG/artifacts/final/*` only. | `source.md:775` | Task 18 |
| INF-307 | `make sync-dev && make verify-sync`; `make lint`; `uv run ruff format --check src/superclaude/cli tests/cli`. | `source.md:777` | Task 18 |
| INF-308 | `T02_15_PERF_REPORT=/tmp/p1-perf.json uv run pytest -q -p no:cacheprovider --tb=line \| tee $PKG/artifacts/final/full.txt`, then `comm -13 <(grep -E '^(FAILED\|ERROR) ' $PKG/artifacts/baseline/full.txt \| sed 's/ - .*//' \| sort -u) <(grep -E '^(FAILED\|ERROR) ' $PKG/artifacts/final/full.txt \| sed 's/ - .*//' \| sort -u)` prints nothing (no new failure; deleted tests simply disappear). | `source.md:778` | Task 18 |
| INF-309 | `bash $PKG/artifacts/acceptance-search.sh all \| tee $PKG/artifacts/final/search.txt` prints `ACCEPTANCE_SEARCH_OK all` (DoD-1). | `source.md:779` | Task 18 |
| INF-310 | Sandbox "fresh" (DoD-2): `T=$(mktemp -d /tmp/p1-sbx.XXXXXX)`; stub `claude` at `$T/bin/claude` (logs argv to `$HOME/claude-calls.log`;... | `source.md:780` | Task 18 |
| INF-311 | then `rg -n -i 'serena\|codebase-memory\|codebase_memory' $T/fresh` prints nothing and `grep -c 'mcp add' $T/fresh/claude-calls.log` prints 0 (or the file is absent). | `source.md:780` | Task 18 |
| INF-312 | Sandbox "existing" (DoD-3, DoD-4): `$T/old/.claude.json` seeded with `mcpServers.codebase-memory-mcp = {"type":"stdio","command":"/usr/local/bin/codebase-memory-mcp","args":[]}`,... | `source.md:781` | Task 18 |
| INF-313 | Expect: `jq '.mcpServers\|keys' $T/old/.claude.json` is `["tavily"]`; `jq '.projects["/x"].mcpServers\|has("serena")' $T/old/.claude.json` is `true`; `rg -n 'mcp__serena' $T/old/.claude/settings.json` prints nothing; `rg -n -i 'serena\|codebase-memory' $T/old/.claude` prints nothing. | `source.md:781` | Task 18 |
| INF-314 | If `pipx install` cannot reach the package index, record the error and run the same checks with `env HOME=$T/old ... uv run --no-sync superclaude install --force && uv run --no-sync superclaude doctor`; this fallback is a recorded deviation, not a pass of `update.sh` itself. | `source.md:781` | Task 18 |
| INF-315 | Then repeat with `mcpServers.serena` set to the current pin with `"env":{}` (the live shape, `inventory/serena.md` E1) and `uv run --no-sync superclaude install --force`: the entry is kept and the output contains "Legacy Serena registration kept until codegraph is ready" (Tier K, section 3.6). | `source.md:781` | Task 18 |
| INF-316 | `env HOME=$T/ci UV_CACHE_DIR="$(uv cache dir)" PATH=<a PATH with no claude executable; confirm with command -v claude printing nothing> uv run --no-sync superclaude install && uv run --no-sync superclaude doctor --verbose` exits 0. | `source.md:782` | Task 18 |
| INF-317 | `git status --short` shows no modified tracked file outside `$PKG`; `rm -rf "$T"`. | `source.md:783` | Task 18 |
| INF-318 | Acceptance: every numbered check above passes, and `$PKG/artifacts/final/summary.md` lists each check with its command and observed result. | `source.md:784` | Task 18 |
| INF-319 | Files: `$PKG/handoffs/<repo>.md` for the 11 repos in section 6.3 (text copied verbatim);... | `source.md:788` | Task 19 |
| INF-320 | `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md` (section 6.2 facts plus the retire-step behaviour and section 7 table, for the Phase 2 Coder handoff, plus a section headed "Phase 2 override: Serena removal" that quotes Phase 2 spec §2.12 and names `codegraph_ready()`; Phase 2 T0b and T3b check for it); | `source.md:788` | Task 19 |
| INF-321 | the slots ledger from T11a-T11c is re-checked to cover every touched step. | `source.md:788` | Task 15 |
| INF-322 | Acceptance: `ls $PKG/handoffs/*.md \| wc -l` prints 11; `test -s .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md && test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`; `rg -q 'codegraph_ready' .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md`. | `source.md:789` | Task 19 |
| INF-323 | **Group G5 done:** final issue comment (states the merge constraint, section 2.2, and links the handoff files). | `source.md:791` | Task 19 |
| INF-324 | At each task-group commit (end of G0, G1, G2, G3, G4 and G5 in section 8; the G0 comment records the baseline counts) the executor posts one brief comment on issue #323 of the fork, and only there: | `source.md:795` | Constraints |
| INF-325 | # must print IronbellyOrg/IronClaude; otherwise run: gh repo set-default IronbellyOrg/IronClaude | `source.md:798` | Constraints |
| INF-326 | gh issue comment 323 --repo IronbellyOrg/IronClaude --body "Phase 1 progress: <group id and name> committed on ironbelly/feat-codememory-codegraph-init at <short sha>... | `source.md:799` | Constraints |
| INF-327 | Rules: one comment per group (not per task); facts only (commit SHA, commands, pass counts, open problems); never `--repo SuperClaude-Org/...` and never a bare `gh issue comment` (gh can default to the upstream parent, see the project `CLAUDE.md` PR rule). | `source.md:802` | Constraints |
| INF-328 | If `gh` is not authenticated or the call fails, record the exact error and the intended body in the task package's `progress.md` and continue; this is not a blocker. | `source.md:802` | Constraints |
| INF-329 | The executor (`/sc:implement` on the plan that `/sc:workflow` builds from this spec) runs without gating on the user. | `source.md:806` | none (section-ref §10) |
| INF-330 | Simple \| one obvious option, or a choice this spec already constrains (wording, test names, exact line moves, file names inside an allowed folder) \| decide yourself \| one line in the task package `decisions.md`: decision, options, method `self`, rationale | `source.md:810` | Constraints |
| INF-331 | write each option to `<task package>/decisions/<task>-<slug>/option-<x>.md`, then spawn an agent that runs `/sc:adversarial --compare <option files> --depth quick`; follow its recommendation \| `decisions.md` entry with method `adversarial quick` and the merged-recommendation path | `source.md:811` | Constraints |
| INF-332 | Complex \| an architectural change to this spec's design (retire-step scope, memory store layout, merge order, deleting a file this spec keeps) \| same, without `--depth quick` (`/sc:adversarial --compare <option files>`) \| `decisions.md` entry with method `adversarial full` | `source.md:812` | Constraints |
| INF-333 | Never stop to ask the user and never pause for scope, cost or context reasons. A blocked task stays blocked with its reason written in `progress.md`; continue with tasks that do not depend on it. | `source.md:816` | Constraints |
| INF-334 | If a task's acceptance command fails, fix within the task's files; if the fix needs a file another task owns, pull that edit forward and say so in `decisions.md`. | `source.md:817` | Constraints |
| INF-335 | Never run the real `./update.sh`, `superclaude install` or `claude mcp add/remove` against the real `HOME` during Phase 1; every environment check runs in a sandbox `HOME` (T14). | `source.md:818` | Constraints |
| INF-336 | Never delete user data (`~/.serena`, project `.serena/` outside this repo, `~/.cache/codebase-memory-mcp`). | `source.md:818` | Constraints |
| INF-337 | Never stage or commit `.claude/` content except `.claude/settings.json` (project `CLAUDE.md`); stage `.dev/tasks/` (the task package) with every commit. | `source.md:819` | Constraints |
| INF-338 | Full-suite runs always set `T02_15_PERF_REPORT=/tmp/p1-perf.json` so `tests/cli/eval/test_perf_home_setup.py` does not rewrite the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json` (override at `test_perf_home_setup.py:122`); run `git status --short` after every test run and restore any tracked file a test changed. | `source.md:820` | Constraints |
| INF-339 | Do not open a pull request to `master` for Phase 1 alone (section 2.2); do not push to `upstream`. | `source.md:821` | Constraints |
| INF-340 | Two later actions belong to the user and are listed so the executor does not attempt them: (1) merging Phases 1 and 2 to `master` together (Phase 2's PR, via `/sc:pr-submit`); (2) running the real `./update.sh` on a live workspace after that merge, which removes the live registrations listed in 2.3. | `source.md:823` | Constraints |

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 404` = 0.00

## Recommendations

### Recommendation R-001: Fix the IMPORTANT plan defects before execution

- **File:** `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md` (Tasks 4, 5, 18) and the matching spec rows
- **Change:** apply the D-001, D-002, D-003 remediations.
- **Verifier:** re-read Tasks 4, 5 and 18: the old helper survives to Task 5, every Task 18 `env` call carries `CLAUDE_CONFIG_DIR`, and both sandbox searches use `--hidden --no-ignore` with the line filter.
- **Linked deviation(s):** D-001, D-002, D-003
- **Priority:** P0

### Recommendation R-002: Fix the MINOR acceptance and scope defects

- **File:** same plan file (Constraints; Tasks 1, 7, 8, 10, 12, 13, 14, 15, 18, 19)
- **Change:** apply the D-004 to D-012 remediations.
- **Verifier:** Task 7 carries the `get_current_config` check; Task 10 names every `mcp-servers:` line; Task 13 lists the extra ref lines; Task 8 lists `real.yaml:721`; `mkdir -p` lines present; Task 12 runs `tests/cli/reflect`; ledger files staged; Constraints carry the scope bullet; Task 18 seeds stale core files.
- **Linked deviation(s):** D-004 to D-012
- **Priority:** P1

### Recommendation R-003: Mirror the spec errata in the spec

- **File:** `.dev/codegraph-migration/specs/phase-1-removal-spec.md`
- **Change:** correct the §3.5 "replaces" wording, the T9/T10b acceptance scope, the P84 line list, the DoD-2/T14 step 4-5 sandbox commands and the DoD-3 seeding so spec and plan agree.
- **Verifier:** the spec's T3, T9, T10b, T11a and T14 text matches plan Tasks 4, 10, 12, 13 and 18.
- **Linked deviation(s):** D-001, D-002, D-003, D-004, D-005, D-006, D-012
- **Priority:** P1
