# Retention: where every removed item stays retrievable (6.1.0 bundle, issue 571 Part B)

> **Corrected 2026-11-18 (Clay's decision).** The `/sc:task` family (`/sc:task`, `sc-task-protocol`, `/sc:validate-tests`, `sc-validate-tests-protocol`, the suite `task_classification_contract`) and the six agents `rf-analyst`, `rf-assembler`, `rf-task-builder`, `rf-task-executor`, `rf-task-researcher`, `rf-team-lead` are **kept** in 6.1.0 (issue 572 decides the agents), so they are not removed items and are not in the table below. The measurements for them were taken before the change and are not repeated here. Removed items now: 9 skills and 1 command.

Measured 2026-11-18. Three copies were compared for every item: the IronClaude copy on `origin/integration` (`847cccc1a`, tree identical to master `3f3b34a26`), the snapshot fork `ironbelly/IronClaudeV5` (a fork of `IronbellyOrg/IronClaude`, master `d4d1662a8`, 2026-11-14; shallow clone in a scratch folder, read only), and IronFlow (`/home/coder/workspaces/IronFlow`, branch `docs/agent-work-coordinator-spec` at `51fa5d0c`, read only: `.claude/skills/<name>/`, `.claude/commands/sc/<name>.md`, `.claude/agents/<name>.md`). Nothing was edited in IronFlow or in the fork.

## Result in one paragraph

All 10 removed items (9 skills, 1 command) exist in all three places. The fork snapshot equals IronClaude master for every item except the task-builder skill, which IronClaude changed after the snapshot (pull requests 582 and 632, 2026-11-16 and 11-17). IronFlow's copies **all differ from IronClaude's**. In 6 of the 10 items IronFlow's copy of the main file (`SKILL.md`, the command file or the agent file) is an older, otherwise untouched version of IronClaude's (a byte-identical match to an IronClaude commit between 2026-05-27 and 2026-07-05); in the other 4 IronFlow has edits of its own (the file matches no IronClaude commit). So IronClaude is newer in every item by commit date (IronFlow's last change is 2026-06-23 to 2026-10-19; IronClaude's is 2026-11-08 to 2026-11-17), but for the 4 items marked "own edits" neither copy contains the other.

**The `v6.0.0` tag (`3f3b34a26`) holds the latest version of every removed item** (all 10 items exist at that tag: checked with `git cat-file -e`). It is newer than the fork snapshot (2026-11-14) and than IronFlow. Restore one file with `git show v6.0.0:<path>` (for example `git show v6.0.0:src/superclaude/skills/task-builder/SKILL.md`) or into the working tree with `git checkout v6.0.0 -- <path>` (a skill folder: `git checkout v6.0.0 -- src/superclaude/skills/task-builder`).

Removal loses nothing that is only here: the `v6.0.0` tag keeps the latest IronClaude side, the fork keeps it up to 2026-11-14, and git history keeps the rest. The IronClaude-only changes that IronFlow does not have are listed below for Clay to port to IronFlow if wanted.

## Table

Columns: IronClaude last change; IronFlow last change (IronFlow repository history, `git log -1`); how IronFlow's copy relates to IronClaude's history; number of IronClaude commits newer than the closest IronClaude version of IronFlow's copy (the IronClaude-only changes); whether the fork copy equals master.

| Item | IronClaude last | IronFlow last | IronFlow's copy | IronClaude-only commits | Fork copy |
|---|---|---|---|---|---|
| skill task | 2026-11-09 | 2026-10-19 | IronFlow-own edits (5 diff lines vs closest IC version IC@17bab85b9 2026-07-05) | 6 (f90aca51a,ed6074c47,2327fbd37,80f934de5,c6009cd3f,2323f7cbb) | fork-same |
| skill task-builder | 2026-11-17 | 2026-10-19 | IronFlow-own edits (63 diff lines vs closest IC version IC@17bab85b9 2026-07-05) | 10 (af5fb69eb,077f9dd38,b681ace43,f90aca51a,ed6074c47,2327fbd37,80f934de5,c6009cd3f,3fcb54175,5c6a7d919) | fork-differs |
| skill tdd | 2026-11-12 | 2026-06-23 | IronFlow-own edits (461 diff lines vs closest IC version IC@a9cf7ee3e 2026-04-02) | 8 (077f9dd38,ed6074c47,2327fbd37,5495ba286,89df2c110,234355941,763e0c58c,f787fef94) | fork-same |
| skill tech-research | 2026-11-12 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 6 (077f9dd38,b681ace43,f90aca51a,ed6074c47,80f934de5,2323f7cbb) | fork-same |
| skill operational-guide | 2026-11-09 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 3 (b681ace43,ed6074c47,80f934de5) | fork-same |
| skill roadmap | 2026-11-09 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 3 (b681ace43,ed6074c47,80f934de5) | fork-same |
| skill prd | 2026-11-08 | 2026-06-23 | IronFlow-own edits (471 diff lines vs closest IC version IC@a9cf7ee3e 2026-04-02) | 6 (ed6074c47,89df2c110,2219545cc,234355941,09e2ccc0d,f787fef94) | fork-same |
| skill readme | 2026-11-09 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 3 (b681ace43,ed6074c47,80f934de5) | fork-same |
| skill tech-reference | 2026-11-12 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 6 (077f9dd38,b681ace43,f90aca51a,ed6074c47,80f934de5,2323f7cbb) | fork-same |
| command tdd | 2026-11-12 | 2026-06-23 | identical to IC@021f715cd (2026-05-27) | 4 (077f9dd38,ed6074c47,2327fbd37,3ae238b17) | fork-same |

"IronFlow-own edits (N diff lines vs closest IC version ...)": the IronFlow file matches no IronClaude commit; N counts the lines that differ from the closest IronClaude version. For `tdd` and `prd` the closest version is from 2026-04-02 and the difference is about 460 lines, so IronFlow's `tdd` and `prd` were rewritten independently.

IronFlow has no `refs/` folder for `prd` and `tdd`: the ten files `src/superclaude/skills/prd/refs/*.md` and `tdd/refs/*.md` exist only in IronClaude (and in the fork). IronFlow-only content (not in IronClaude): a `.understand-anything/` folder and a `SKILL.md.bak` in each skill folder, and `tech-research/README.md`. `sc-task-protocol/__init__.py` exists only in IronClaude.

## IronClaude-only changes for Clay to port to IronFlow (if wanted)

These are the commits behind the "IronClaude-only commits" column, each listed once with what it changed in the bundle. Subjects are quoted from `git log`.

| Commit | Date | Subject |
|---|---|---|
| `f787fef94` | 2026-04-03 | refactor(skills): split PRD/TDD skill content   and add refs packs in source tree |
| `763e0c58c` | 2026-04-05 | refactor(tdd): create command layer and migrate interface content from SKILL.md |
| `09e2ccc0d` | 2026-04-13 | feat: modularized the prd skill and port it to the cli |
| `234355941` | 2026-04-22 | fix(skills): repair broken refs in modularized prd/tdd skills |
| `2219545cc` | 2026-05-20 | fix(prd): anchor CLI path resolution to .claude/; migrate templates SoT into src/ (#63) |
| `89df2c110` | 2026-05-22 | chore: apply markdownlint MD022/MD031/MD032/MD034 auto-format repo-wide (#74) |
| `5495ba286` | 2026-06-07 | feat(reuse-audit): reuse-auditor agent + sc-reflect/tdd integration (#146) |
| `156f28292` | 2026-07-01 | fix: normalize Tavily MCP tool names (#208) |
| `002eaa8b7` | 2026-07-06 | feat(qa-reflect): additively harden RF QA + /sc:reflect vs the PR #209 correctness-bug class (FX1/FX2/FX3/FX5/FX7) (#214) |
| `2323f7cbb` | 2026-07-06 | feat(reflect): behavioral-reachability controls C2/C7/C8 (#217) |
| `3ae238b17` | 2026-09-30 | chore: drop unused commands and sequential/magic/chrome-devtools MCPs |
| `046a03ab4` | 2026-10-03 | chore: drop removed Sequential MCP references |
| `051f39fea` | 2026-10-14 | feat(routing): one HOW-WE-WORK guide for which tool to use when |
| `3fcb54175` | 2026-10-22 | fix(primitives): accept project and installed copies in prerequisite lookups |
| `5c6a7d919` | 2026-10-22 | fix(primitives): use global ~/.claude paths for installed-primitive reads |
| `c6009cd3f` | 2026-10-23 | docs: .dev/tasks is always staged; stop ignoring package evidence |
| `2f10a0e1e` | 2026-10-30 | feat: replace codebase-memory and Serena with codegraph (#323) (#329) |
| `75d0d1e2c` | 2026-10-31 | feat(codegraph): adopt codegraph in primitives; add /sc:impact and /sc:graph (#323) (#336) |
| `80f934de5` | 2026-11-02 | fix(qa): minor findings never fail a review; cap review loops at 2 rounds (#343) |
| `2327fbd37` | 2026-11-07 | feat(orca): convert the 15 P2 commands to --unattended with report directories (#422) |
| `ed6074c47` | 2026-11-08 | fix(mcp): accept the LiteLLM proxy tool names alongside the direct names (#454) (#458) |
| `b681ace43` | 2026-11-09 | 346Claude-P1b: remove the remaining finding quotas from producer-skill QA prompts (#482) |
| `f90aca51a` | 2026-11-09 | fix(review): remove prompts that override the review-loop contract (refs #346) (#477) |
| `077f9dd38` | 2026-11-12 | feat(mcp): add the reviewed MCP servers and tool grants to nine skills and commands (#512) (#515) |
| `64e8eacf2` | 2026-11-16 | feat(review): consequence-based review rule, fixcheck command and rf-qa rewrites (issue 552 stage 3) (#582) |
| `af5fb69eb` | 2026-11-17 | refactor(cli): remove the roadmap, tasklist and sprint family (6.0.0) (#632) |

Grouped by theme (judged from the commit subjects; the diffs were not re-read line by line). `rf-qa` and `rf-qa-qualitative` stay in IronClaude (decision D3 in `dependency-map.md`), so their commits need no port.

- Review rule (what counts as blocking, minor findings never fail a review, two fix cycles at most, no finding quotas): `80f934de5`, `f90aca51a`, `b681ace43`, `64e8eacf2`; `002eaa8b7` hardens `rf-qa-qualitative` and reflect.
- Unattended mode for the converted commands: `2327fbd37` (touches `task` and `tdd`).
- Tool grants and tool names: `ed6074c47` (LiteLLM proxy tool names), `077f9dd38` (reviewed MCP servers), `156f28292` (Tavily tool names).
- Codegraph in place of the old memory servers: `2f10a0e1e`, `75d0d1e2c`; dropped MCP references: `3ae238b17` (also removed unused commands), `046a03ab4`.
- Path and routing hygiene: `3fcb54175`, `5c6a7d919` (installed-path lookups), `051f39fea` (routing guide), `c6009cd3f` (`.dev/tasks` always staged).
- Reflect integration: `2323f7cbb`, `5495ba286` (reuse auditor wired into `tdd`).
- The `prd` and `tdd` skills as split into `refs/` packs and later repaired: `f787fef94`, `763e0c58c`, `09e2ccc0d`, `234355941`, `2219545cc`; `89df2c110` is a repo-wide markdown autoformat. The `refs/` folders are IronClaude-only (IronFlow has none).
- 6.0.0 cleanup: `af5fb69eb` removed roadmap, tasklist and sprint mentions from `task-builder` (only relevant to IronFlow if it also dropped those commands).

Whether IronFlow wants any of this is Clay's call. For the four items marked "IronFlow-own edits" the IronClaude-only column is an upper bound (the closest IronClaude version is a comparison point, not a proven common ancestor), and IronFlow's own edits are not in IronClaude. For the ten identical items the column is exact: those commits are the complete difference.

## How to retrieve a removed item

- From the fork: `gh repo clone ironbelly/IronClaudeV5` (read it, do not push): the path is the same as in IronClaude (`src/superclaude/skills/<name>/`, `src/superclaude/commands/<name>.md`, `src/superclaude/agents/<name>.md`).
- From IronClaude history: the `v5.0.0` and `v6.0.0` tags and `git show v6.0.0:src/superclaude/skills/<name>/SKILL.md`.
- From IronFlow: `.claude/skills/<name>/`, `.claude/commands/sc/<name>.md`, `.claude/agents/<name>.md`.
