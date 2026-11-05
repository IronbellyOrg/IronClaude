# Task X result: fixes for Q-I1 and Q-I2 (FINAL-SUMMARY section 6)

Date: 2026-10-29. Worker for Orca task `task_882f78222b58`. Planning run only: no source edits, no commits, no staging. `git status --short` after the work shows only the same seven untracked paths as at the start; no tracked file is modified.

## 1. What changed (file and line)

| # | File | Line | Change |
|---|---|---|---|
| 1 | `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md` | 174 (Task 12 criterion 3) | Pattern cut to the five memory names `write_memory\|read_memory\|list_memories\|edit_memory\|delete_memory`; added `-g '!src/superclaude/skills/sc-reflect-protocol/SKILL.md' -g '!**/reflect.md' -g '!commands/sc-reflect.md' -g '!src/superclaude/commands/validate-roadmap.md'`; dropped the old `-g '!.../refs/reflection-rubric.md'` (see 3.3); the closing text now says the excluded files are rewritten by Tasks 13 and 15 and that the full-token repo-wide check is Task 15's `acceptance-search.sh serena src/superclaude plugins/superclaude commands agents`. |
| 2 | `.dev/codegraph-migration/specs/phase-1-removal-spec.md` | 736 (T10b acceptance) | Same command and the same sentence, using the spec's names (T11a, T11c). |
| 3 | `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md` | 736 | Whole file re-copied from the spec (`cp`), so it carries change 2. |
| 4 | `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` | 212 (Task 13 criterion 4) | ` -g '!**/core/CODEGRAPH.md'` appended to both `rg` commands (the "no wildcard" and "no explore" searches), plus a parenthetical saying the `-g` exempts the guide and its plugin copy. |
| 5 | `.dev/codegraph-migration/specs/phase-3-codegraph-adoption-spec.md` | 287 (T11 (5) and (6)) | Same `-g` appended to both commands; the (6) note "the guide in `core/` is exempt" now reads "the guide `core/CODEGRAPH.md` and its plugin copy are exempt", and (5) got the same note. |
| 6 | `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md` | 287 | Whole file re-copied from the spec (`cp`). |
| 7 | `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/progress.md` | 2 | `PLAN:` line re-pinned (below). |
| 8 | `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/progress.md` | 2 | `PLAN:` line re-pinned (below). |
| 9 | `.dev/codegraph-migration/FINAL-SUMMARY.md` | 332 (Q-I1), 333 (Q-I2) | Status cell `**OPEN** (not fixed: IMPORTANT)` became `**FIXED** (...)` naming the files changed. Verdict cells (lines 5, 25, 27) not touched; the re-check task owns them. |

Every old string was matched exactly once before replacing (script aborts otherwise). `source.md` equalled its spec before the edits (`cmp` silent), so the `cp` carried only these changes.

## 2. Verification output

`cmp` (must print nothing):

```text
$ cmp .dev/codegraph-migration/specs/phase-1-removal-spec.md .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md
$ cmp .dev/codegraph-migration/specs/phase-3-codegraph-adoption-spec.md .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md
```

(both printed nothing)

`sha256sum`:

```text
374613e7427abfb6b85a84778f79e30cd8b24a24367bffd345a98d50ab8ed23c  .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md
9e30a216ebba4c63a6169f898b6084cf1cdafdabc04d6a010f8fa6981f72b82d  .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md
bfc3635192de31cb2e6b3ce40ca12ae4cf17e2f79a546eca9755d6ca9e24c9a3  .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md
71bd93e21b6e3277dfed1b5fb4cdebb66697818d90ad11d91722397aa90ef326  .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md
```

New `PLAN:` lines (line 2 of each `progress.md`, same format as before):

```text
PLAN: sha256=374613e7427abfb6b85a84778f79e30cd8b24a24367bffd345a98d50ab8ed23c source_sha256=9e30a216ebba4c63a6169f898b6084cf1cdafdabc04d6a010f8fa6981f72b82d
PLAN: sha256=bfc3635192de31cb2e6b3ce40ca12ae4cf17e2f79a546eca9755d6ca9e24c9a3 source_sha256=71bd93e21b6e3277dfed1b5fb4cdebb66697818d90ad11d91722397aa90ef326
```

Old pins replaced: Phase 1 plan `49605f30...` and source `f2f1f489...`; Phase 3 plan `04191a30...` and source `c4159819...`.

## 3. Q-I1: revised command run against today's tree

Command: `rg -c --no-ignore 'write_memory|read_memory|list_memories|edit_memory|delete_memory' src/superclaude plugins/superclaude commands agents -g '!src/superclaude/skills/sc-reflect-protocol/SKILL.md' -g '!**/reflect.md' -g '!commands/sc-reflect.md' -g '!src/superclaude/commands/validate-roadmap.md'`

It still prints hits today, as expected for a plan that has not run. Hit list (matching lines per file) and the task that clears each:

| File (lines) | Owning step | Cleared before Task 12's check? |
|---|---|---|
| `agents/sc-pm-agent.md` (21), `commands/sc-load.md` (1), `commands/sc-pm.md` (20), `commands/sc-save.md` (1) | Task 11 (rows P1, P4, P5, P8) | Yes, Task 11 runs first; its criterion 3 requires these files clean |
| `plugins/superclaude/agents/pm-agent.md` (21), `plugins/superclaude/commands/load.md` (1), `plugins/superclaude/commands/save.md` (1), `plugins/superclaude/modes/MODE_Task_Management.md` (24) | Task 11 (rows P11-P23) | Yes |
| `src/superclaude/agents/pm-agent.md` (21), `src/superclaude/commands/load.md` (1), `src/superclaude/commands/save.md` (1), `src/superclaude/modes/MODE_Task_Management.md` (24), `src/superclaude/skills/sc-pm-protocol/SKILL.md` (12) | Task 11 (rows P27-P73) | Yes |
| `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` (2: lines 179, 232) | Task 12 itself (row P85, memory handoff) | Yes, Task 12 rewrites it |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` (3: lines 91, 303, 319) | Task 12 itself (row P91, STRICT-tier memory); tool prerequisites also Task 15 | Yes |
| `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` (15: line 4 `allowed-tools` and lines 126-1071) | Task 12 itself (row P96, ledger/terminology/pattern-log memory); `find_symbol`-style tool lines are Task 15 | Yes |

Files excluded by the four `-g` (five-name hits today): `sc-reflect-protocol/SKILL.md` (34), `src/superclaude/commands/reflect.md` (2), `plugins/superclaude/commands/reflect.md` (2), `commands/sc-reflect.md` (1), `src/superclaude/commands/validate-roadmap.md` (1). These are Task 12 (memory parts), Task 13 (reflect `--onboard` bootstrap, SKILL.md lines 91-309, and reflect command tool tables) and Task 15 (validate-roadmap `allowed-tools`).

### 3.1 Difference from the brief's expectation (reported, not hidden)

The brief expected every remaining hit to sit in a file that Tasks 13-15 delete or rewrite. That is not the case: all 16 files above are owned by Task 11 or Task 12, which run before or at the check, and none is a Task 13-15-only file. I did not widen the exclusions for them, because the criterion is evaluated after Tasks 11 and 12 have rewritten them; excluding them would hide a real failure of those tasks. The check passes at Task 12 only if Tasks 11 and 12 fully rewrite those files. That is not testable today and is UNVERIFIED; the plan's Task 11 criterion 3 and Task 12's own steps require it.

### 3.2 Observation

With only the five memory names, the `validate-roadmap.md` exclusion is probably unnecessary after Task 12: row P50 gives Task 12 the memory tool entries of that command, and the remaining tool names (`activate_project`, `find_symbol`, and so on) are not in the pattern. I kept it because the Fix column of Q-I1 lists it and it is harmless.

### 3.3 Dropped rubric exclusion

The old command carried `-g '!.../refs/reflection-rubric.md'` only for its `get_current_config` line. No five-name hit exists in that file: the hit list with and without that exclusion was identical (16 files, same counts). It is gone from the plan command so the plan matches the spec.

## 4. Q-I2: revised commands

Both commands run as revised (`... -g '!**/core/CODEGRAPH.md'`):

- Throwaway fixture `/tmp/qi2-fixture.*` (removed afterwards) with `src/superclaude/core/CODEGRAPH.md` and `plugins/superclaude/core/CODEGRAPH.md`, each holding `Bash(codegraph *)`, `mcp__codegraph__*`, `codegraph_explore`, `codegraph explore`, `codegraph context`:
  - without the `-g`: hits in both guide copies (confirms the defect);
  - with the `-g`: both commands print nothing (`rg` exit 1);
  - negative control: a stray `Bash(codegraph *)` and `codegraph explore` in `src/superclaude/commands/bad.md` are still reported.
- Real tree today: neither `CODEGRAPH.md` exists yet (created by Phase 3 Task 3), and both commands print nothing (`rg` exit 1).

So no hit appears in any `CODEGRAPH.md` file. Other Phase 3 searches (plan lines 104, 143, 155; spec line 282) do not scan `core/`, so they are unaffected and unchanged.
