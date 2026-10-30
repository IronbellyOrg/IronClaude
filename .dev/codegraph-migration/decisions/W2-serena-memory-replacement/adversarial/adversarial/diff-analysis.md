# Diff Analysis: Serena-memory replacement (Options A, B, C) Comparison

Variants: V1 = Option A (repo-local `.superclaude/memory/` plain files), V2 = Option B (Claude Code native auto-memory), V3 = Option C (drop memory entirely).
Context file: `context.md` (same folder as the options).

## Metadata
- Generated: 2026-10-30
- Variants compared: 3 (Mode A, input order A, B, C)
- Depth: quick (Round 1 only; Round 2 and 2.5 skipped by depth)
- Total differences found: 19 scored diff points (S 3, C 7, X 4, A 5) plus 5 unique contributions
- Categories: structural (3), content (7), contradictions (4), unique (5), shared assumptions (5)

### Repo evidence gathered for this analysis (read-only, 2026-10-30)
Each item was read or grepped in this worktree; use these when arguing. Do not trust the option texts or context.md over these.
- E1. `src/superclaude/agents/pm-agent.md` is 722 lines (not 25 as context.md says). It has 21 hits for memory tool names (write_memory/read_memory/list_memories/...) and also calls Serena-only non-memory tools: `think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done`. Session-start keys: `pm_context`, `current_plan`, `last_session`, `next_actions`; during work: `plan`, `checkpoint`, `decision`, `summary`.
- E2. Hits for `write_memory|read_memory|list_memories|edit_memory|delete_memory|.serena/memories` under `src/superclaude`: 121 occurrences in 14 files: MODE_Task_Management.md (24), sc-reflect-protocol/SKILL.md (34), pm-agent.md (21), sc-validate-roadmap-protocol/SKILL.md (15), sc-pm-protocol/SKILL.md (12), sc-task-protocol/SKILL.md (3), commands save.md (1), load.md (1), reflect.md (2), validate-roadmap.md (1), sc-reflect refs/remediation-handoff.md (2), sc-crash-recovery SKILL.md (2) + scripts/bootstrap_scan.sh (2) + refs/investigators.md (1). sc-roadmap-protocol has 19 memory/persist mentions across 4 files.
- E3. Tests: `tests/core/test_how_we_work_routing_table.py` lines 35-36 list `sc:save`, `sc:load`; line 1074 asserts `"requires Serena" in other`; line 1075 asserts `"writes memory; not durable task execution state" in other`; line 1076 asserts "Not executor resume". Also `tests/recommend/fixtures/routing_refresh_cases.json` (6 hits) and `tests/sc-roadmap/integration/test_wave5_completion.py` (lines 69-78 Serena memory persistence and circuit-breaker tests). So every option must edit these tests or the HOW-WE-WORK rows, not only Option C.
- E4. `HOW-WE-WORK.md` line 237 says `/sc:save` and `/sc:load` "store and load Serena project memory. They are not a way to resume work or a guarantee of complete executor state." That is a limitation disclaimer for routing, not a statement that the feature is obsolete. Rows at lines 327 and 329 say "requires Serena".
- E5. `.gitignore` line 113 ignores `.serena/`, line 114 ignores `.superclaude/`. Yet `git ls-files` shows tracked: `.serena/memories/memory_maintenance.md`, `.serena/memories/reflect/deviation-patterns-IronClaude.md`, `.serena/.gitignore`, `.serena/project.yml`. So the reflect calibration memory is git-tracked today and shared across worktrees via git. A `.superclaude/` home would be gitignored and lose that.
- E6. `docs/memory/` is tracked and already holds `pm_context.md`, `last_session.md`, `next_actions.md`, `patterns_learned.jsonl`, `solutions_learned.jsonl`, `workflow_metrics.jsonl`, `README.md`. These are the same key names pm-agent writes to Serena. `docs/memory/pm_context.md:75` says "Repository-Scoped Memory: Local file-based memory in docs/memory/".
- E7. Official Claude Code docs (code.claude.com/docs/en/memory, fetched 2026-10-30): auto memory is "Per repository, shared across worktrees"; the `<project>` path "is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory"; machine-local, not shared across machines; `MEMORY.md` first 200 lines or 25KB load at session start; toggled by `autoMemoryEnabled` (user or project settings) or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; location configurable with `autoMemoryDirectory`; memory files are excluded from the transcript cleanup sweep. Auto memory is written by Claude itself for "learnings and patterns"; the docs do not publish it as an API for other tools to write structured state.
- E8. `sc-crash-recovery`: `scripts/bootstrap_scan.sh` lines 146-147 report `has_serena` and `serena_memory_count` from `$ABS_PROJECT/.serena/memories`; `refs/investigators.md` section 3 `serena-memory` reads `<PROJECT_PATH>/.serena/memories/`; SKILL.md line 79 spawns it only when that folder exists.
- E9. `sc-reflect-protocol/SKILL.md` steps 0.7/0.7b: activates the Serena project, hydrates memory, derives `onboarding_status` from the `activate_project` message or from `list_memories` containing the `memory_maintenance` seed; `--onboard` runs `mcp__serena__onboarding` only when `list_memories` is empty; the remediation handoff writes `reflect/handoff-{slug}-{timestamp}` via `prepare_for_new_conversation` or `write_memory`. The reflect cold-start calibration memory is `reflect/deviation-patterns-<slug>`.
- E10. `src/superclaude/commands/save.md` frontmatter: `mcp-servers: [serena]`, "Mandatory integration"; it also uses Serena tools `think_about_collected_information` and `summarize_changes` (not memory tools).

## Structural Differences
| # | Area | V1 (A) | V2 (B) | V3 (C) | Severity | Level |
|---|------|--------|--------|--------|----------|-------|
| S-001 | Storage location | `<project>/.superclaude/memory/` (repo-local, gitignored) | `~/.claude/projects/<slug>/memory/` (outside repo, Anthropic-owned) | none (existing files: git, `.dev/tasks/`, `docs/memory/`) | High | L2 |
| S-002 | Command and agent surface | `/sc:save`, `/sc:load`, pm-agent lifecycle kept; tool names swapped | kept; retargeted at the harness dir | `/sc:save`, `/sc:load`, pm-agent lifecycle and MODE_Task_Management hierarchy deleted | High | L2 |
| S-003 | File format and naming convention | flat `<name>.md`, topics as subfolders, same as Serena | `MEMORY.md` index plus frontmatter-typed topic files ("No SuperClaude-owned storage format") | no format | Low | L1 |

## Content Differences
| # | Topic | V1 (A) | V2 (B) | V3 (C) | Severity | Level |
|---|-------|--------|--------|--------|----------|-------|
| C-001 | Consumer coverage | All Serena-memory consumers migrate by a mechanical edit (E2: 14 files, 121 hits) | Names /sc:save, /sc:load, pm-agent only; sc-reflect, sc-roadmap, sc-validate-roadmap, sc-task, MODE_Task_Management unaddressed | Names save/load/pm-agent/MODE_Task_Management for deletion; reflect and roadmap listed as "no home" | High | L2 |
| C-002 | Portability to other projects and harnesses | Works anywhere via Read/Write/Glob/Edit | Needs Claude Code auto-memory enabled; instructions conditional; breaks plugin/other harness | Works anywhere (nothing to port) | High | L2 |
| C-003 | Cross-worktree and cross-session sharing | Per worktree; not shared unless path resolves to the main checkout | Claimed shared (pro) and "not guaranteed" (con); E7 says shared per repo | n/a; git and `.dev/tasks/` share state | High | L3 |
| C-004 | Home for sc-reflect calibration memory (tracked in git today, E5) | Move to `.superclaude/memory/reflect/` (gitignored) or `docs/memory/` | Written into harness dir, outside repo, not versioned | "No home" (stated as a con) | High | L3 |
| C-005 | Test and routing-doc impact | Edit HOW-WE-WORK rows 327/329 and test line 1074 ("requires Serena") | Same edit needed | Remove rows and test assertions (lines 35-36, 1074-1076, fixtures) | Medium | L2 |
| C-006 | sc-crash-recovery investigator | Path swap to `.superclaude/memory/` (E8) | Must read `~/.claude/projects/<slug>/memory/`; bootstrap script must derive the repo-based slug | Drop the `serena-memory` investigator | Medium | L2 |
| C-007 | Session-start loading semantics | Explicit list/read at session start (pm-agent) | Automatic load, but only first 200 lines or 25KB of `MEMORY.md` (E7) | Nothing to load | Medium | L3 |

## Contradictions
| # | Point of Conflict | Position A | Position B | Impact | Level |
|---|-------------------|-----------|-----------|--------|-------|
| X-001 | Option B contradicts itself on worktree sharing | n/a | Pro: "shared across worktrees of the same repo slug". Con: "slug differs per worktree path so cross-worktree sharing is not guaranteed". E7 sides with the pro. | Medium | L3 |
| X-002 | Option C: "no gap to fill in Phase 3" vs its own cons | Pro: "no gap to fill in Phase 3" | Con: "sc-reflect calibration memory and sc-roadmap persistence have no home" and "pm-agent restore context has nothing to restore" | Medium | L2 |
| X-003 | Option C reads E4 as a reason to delete; HOW-WE-WORK line 237 only limits what the commands promise | C: feature "already says is not a way to resume work" | E4: disclaimer about not being executor resume; rows still exist and are tested | Low | L2 |
| X-004 | Option A "prompts change by tool name only" vs semantics that depend on Serena behaviour (E9, E10) | A: tool-name swap only | sc-reflect Step 0.7/0.7b gating on `list_memories` empty and `activate_project` message; `prepare_for_new_conversation`; save.md `summarize_changes`; pm-agent `think_about_*` need rewrites, not renames | High | L3 |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 (A) | Preserves feature and semantics with native tools only; offline; testable in CI; works in every project where only `~/.claude` primitives exist | High |
| U-002 | V1 (A) | Names `docs/memory/` as the escape hatch for memory that must be shared through git | Medium |
| U-003 | V2 (B) | Automatic context load each session without explicit read calls; memory files survive Claude Code retention sweep | Medium |
| U-004 | V3 (C) | Smallest change surface; avoids designing storage; lists existing continuity mechanisms (git, `.dev/tasks/` ledgers, TodoWrite, ccsession, Claude Code resume) | Medium |
| U-005 | V3 (C) | Forces an honest inventory of what Serena memory was actually used for (and surfaces the reflect/roadmap gap) | Low |

## Shared Assumptions
All three options agree on points implied by "remove Serena". The following hidden preconditions were enumerated from those agreements.

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status | Level |
|-------|-----------|------------------|----------------|--------|--------|-------|
| A-001 | Serena memory is the only Serena capability to replace. In fact pm-agent and save.md also use Serena-only `think_about_*` / `summarize_changes`, and sc-reflect uses `activate_project`, `onboarding`, `prepare_for_new_conversation` (E1, E9, E10). | All three treat the problem as "memory store only" | UNSTATED | High: leftover references break after removal | Promoted [SHARED-ASSUMPTION] | L2 |
| A-002 | A single writer per memory key at a time. Parallel sessions, worktrees, and fan-out agents may write `pm_context` / `last_session` / `plan` concurrently; Write overwrites whole files, Serena `write_memory` did too, but nothing guards lost updates. | All three assume one session owns the state | UNSTATED | Medium | Promoted [SHARED-ASSUMPTION] | L3 |
| A-003 | `<project>` root is unambiguous: the agent runs at the repo root, not in a subdirectory or a nested `.dev/worktrees/<name>/`. A, B (slug derivation) and the crash-recovery bootstrap all resolve a root; wrong root writes to the wrong folder or reads an empty store. | A and B both point to a per-project folder | UNSTATED | Medium | Promoted [SHARED-ASSUMPTION] | L3 |
| A-004 | Existing users have nothing to migrate: legacy `.serena/memories/*` content (including the tracked reflect calibration file) will be re-created or abandoned with no import or read-fallback guard in /sc:load. | All three skip a transition step | UNSTATED | Medium | Promoted [SHARED-ASSUMPTION] | L3 |
| A-005 | Keeping tests green is a cost only for Option C. (E3: routing-table test asserts "requires Serena", so A and B also need edits.) | A and B list no test cost; C lists it as a con | CONTRADICTED | Medium | Flagged for debate | L2 |

## Summary
- Total structural differences: 3
- Total content differences: 7
- Total contradictions: 4
- Total unique contributions: 5
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 0, CONTRADICTED: 1)
- Highest-severity items: S-001, S-002, C-001, C-002, C-003, C-004, X-004
- Total diff points for convergence denominator (S + C + X + A): 19
- Taxonomy tally (auto-tagged, one level per point): L1 = 1 (S-003); L2 = 10 (S-001, S-002, C-001, C-002, C-005, C-006, X-002, X-003, A-001, A-005); L3 = 8 (C-003, C-004, C-007, X-001, X-004, A-002, A-003, A-004). Sum = 19.
