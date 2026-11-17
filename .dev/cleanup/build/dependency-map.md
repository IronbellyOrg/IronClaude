# Dependency map: remove `/sc:build` (6.0.0, PR 7)

Measured at `783832f11` (head of `integration` after the `/sc:spawn` removal), on branch `clayphi/v6-build`.
Method: `git grep` over tracked files for `sc:build`, `sc:sc:build`, `sc-build`, `build.md`, a bare command name `build`
in command lists, and the converted-command counts; then each hit read in place. The codegraph MCP server
disconnected mid-session and was not reachable again, so no codegraph callers/impact run is recorded. The item is a
markdown command, not a code symbol: no Python or shell code imports or calls it. The only code that names it is the
launch-level guard shell script (a `case` list) and tests.

The plan counted 3 files deleted and 13 edited outside (3 tests, 4 docs, 2 scripts, 5 other). Re-measured: **3 files
deleted, 5 tests edited, 12 docs and routing-guide files edited, 4 hook/script files edited (2 are mirrors of the
same script), 1 skill edited.** The extra tests and docs come from the worker-contract counts (build was one of the 16
phase 1 commands) and from the legacy root `commands/sc-recommend.md`.

Historical records, NOT edited: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/` (the launch-level design
names `/sc:build` at lines 106, 236, 391 and its test applies removal rewrites), past `CHANGELOG.md` entries, `.dev/`.

## 1. Files deleted (3, plus 1 untracked mirror)

| Path | Why |
|---|---|
| `src/superclaude/commands/build.md` | the command (source of truth) |
| `plugins/superclaude/commands/build.md` | plugin mirror |
| `commands/sc-build.md` | legacy root copy (the `/sc:spawn` removal also deleted `commands/sc-spawn.md`) |
| `.claude/commands/sc/build.md` | gitignored dev mirror; delete by hand, never stage |

## 2. Routing guide and worker contract (installed core docs)

| Path:line | Change |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md:324` | delete the `/sc:build` row of the "Other operations" table |
| `src/superclaude/core/HOW-WE-WORK.md:403` | "the 16 phase 1 commands" becomes 15 |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:324,403` | same two edits; file must stay byte-identical to the source copy |
| `src/superclaude/core/WORKER-CONTRACT.md:329` | "the 16 commands converted in P1 (..., analyze, build, ...)" becomes 15, drop `build` from the list |
| `src/superclaude/core/CLAUDE.md` | no mention of `/sc:build`; level-table copy unchanged (build is not in the level table) |

## 3. Hook scripts (source and plugin mirror)

| Path:line | Change |
|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh:43` | message: `/sc:cleanup or /sc:build` becomes `or /sc:cleanup`: "starting /sc:implement, /task, /sc:improve or /sc:cleanup (or their skills)." |
| `src/superclaude/hooks/scripts/launch-level-guard.sh:409` | `case` list: drop `build` from `implement \| task \| improve \| cleanup \| build` |
| `plugins/superclaude/hooks/scripts/launch-level-guard.sh:43,409` | same two edits (mirror; the two files stay identical) |

## 4. Skill

| Path:line | Change |
|---|---|
| `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:594` | one bullet `/sc:build — Build and compile after generating`: remove the bullet (the skill itself is removed later by PR 4; this is the smallest edit that stops it naming a deleted command) |

## 5. Tests

| Path:line | Change |
|---|---|
| `tests/core/test_how_we_work_routing_table.py:28` | drop `"sc:build"` from `_OTHER_COMMANDS` |
| `tests/hooks/test_launch_level_guard.py:81` | extend `_REMOVED_COMMAND_TEXT`: after the spawn rewrite the design text reads `/sc:improve, /sc:cleanup or /sc:build`; add the rewrite to `/sc:improve or /sc:cleanup` (design doc is historical and is not edited) |
| `tests/hooks/test_launch_level_guard.py:917` | drop `"sc:build"` from `IMPL_SPELLINGS` |
| `tests/recommend/test_routing_refresh.py:589,599` | drop build from the example-flag test (docstring, tuple, route) |
| `tests/recommend/test_routing_refresh.py:35` | `_POST_REFRESH_REMOVALS` gains `"build"`; comment updated |
| `tests/recommend/fixtures/routing_refresh_cases.json:737` | NO change: frozen record of the 47 commands of the refresh package; the removal set above accounts for it |
| `tests/skills/test_worker_contract.py:473,485` | P1 list: sixteen becomes fifteen; drop `"build"` |
| `tests/skills/test_worker_contract.py:583-587` | drop the `"build"` entry from `UNATTENDED_EXPECT` |
| `tests/skills/test_worker_contract.py:1394-1399` | drop the `build` artifacts-clause assertions |
| `tests/skills/test_worker_contract.py:1467-1468` | `len(commands) == 16` becomes 15 (message too) |
| `tests/skills/test_worker_contract.py:1675` | `len(expect) == 31` becomes 30 (message too) |
| `tests/unit/test_cli_install.py:114,402` | drop `build.md` from the two expected file-name lists |

Tests that adapt on their own (no edit expected): the `make verify-sync` mirror parity tests, the sync tests, the
commands-count tests that glob `src/superclaude/commands`. Confirmed by the after-run.

## 6. Docs (current, so edited)

| Path:line | Change |
|---|---|
| `docs/user-guide/commands.md:70` | delete the `/sc:build` row of the command table |
| `docs/user-guide/commands.md:1191-1219` | delete the `### /sc:build - Project Building` section and its trailing `---` |
| `docs/user-guide/flags.md:60-68` | delete the `### Build Command Flags (/sc:build)` block |
| `docs/user-guide/agents.md:157` | "`/sc:implement`, `/sc:build` and `/sc:improve` do not call it" becomes "`/sc:implement` and `/sc:improve`" |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:342` | Examples: drop `/sc:build` |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:976-977` | 31 converted commands (16 + 15) becomes 30 (15 + 15); "16 phase 1 commands" becomes 15 |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1605` | IMPL class row: drop `build` |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:317,745,1321,1355,1958,2197,2203` | converted-command counts 31 becomes 30, "16 in P1" becomes 15 (read each in place before editing) |
| `docs/generated/contributor-knowledge-base/architecture-guide.md:239`, `components-guide.md:158` | drop the `build.md` list entry |
| `commands/sc-help.md:31,123` | delete the table row and the example line that uses `/sc:sc:build` |
| `commands/sc-recommend.md` (25 lines naming `/sc:sc:build`) | legacy v4-era text. Replace `/sc:sc:build` with `/sc:sc:implement` (the root tree's own feature command; the old build flows were feature builds), and remove the entry where that would duplicate an existing `/sc:sc:implement` (line 490) |

Not edited, kept deliberately: `docs/user-guide/commands.md` and others that say "build" as an ordinary word;
`--type build` of `/sc:troubleshoot`; `build` in `sc-troubleshoot-protocol` and `deliverables.py` (a different meaning);
`make build-plugin`.

## 7. Install code, hooks registration, packaging

- `src/superclaude/cli/install_commands.py`, `doctor`, `pyproject.toml`, `Makefile`: no entry names `build.md`; the
  install copies every file in `commands/`, so deleting the source file removes it from the install.
- `src/superclaude/cli/recommend/cache.py` globs `commands/*.md`; the surface fingerprint changes by itself.
- `.claude/settings.json`: no mention.

## 8. Final search (run after the edits)

`git grep -n -I -E 'sc[:/_-]+build|commands/build|sc-build|build\.md' -- . ':!.dev' ':!docs/releases' ':!docs/testing' ':!docs/designs' ':!CHANGELOG.md'`
must print only unrelated hits (`task-builder`, `build-request-template.md`, `build-plugin`).
