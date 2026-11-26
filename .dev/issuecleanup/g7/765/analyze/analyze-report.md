# /sc:analyze report: src/superclaude/skills/ccsession-tag/ (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:38:19Z; degraded: graph:empty (the `ccsession` and `ccsession-orca` shell scripts are not indexed; `codegraph_files` listed only the 6 Python files, so every shell finding below comes from Grep and Read)

Scope: issue 765 (keep Claude Code's low-memory cleanup from stopping the coordinator's Orca message watch). Analysed on `origin/master` f2894fc44 (local HEAD a7ae3dd30 is 6 commits behind; the only difference in the area is `src/superclaude/cli/user_settings_defaults.json`, see F6). Line numbers below were read on `origin/master` and, for `ccsession`, are identical in the working tree (the diff HEAD..origin/master touches no ccsession file).

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | Info (good fit) | One choke point reaches every Claude start through ccsession. The launch-identity block (`export CCSESSION_LAUNCH_ID`, `CCSESSION_LAUNCH_CWD`, `CCSESSION_ORIGIN`) runs once, before all three `exec "$CLAUDE_BIN"` branches: untagged, resume, new session. A single `export` placed in or after that block covers all of them, and no branch needs its own change. | `ccsession:2412-2438` (block), `:2447-2451` (untagged exec), `:2508-2512` (resume exec), `:2515-2519` (new-session exec), file is 2520 lines |
| F2 | Medium | The per-user env file is sourced earlier (`. "$CCSESSION_ENV_FILE"`), so a person's own `~/.claude/ccsession.env` can already set or unset the variable. The change must say whether the launch default respects an existing value (`${VAR:-1}`) or forces `1`, and the README must document it. | `ccsession:1080-1086` |
| F3 | Medium (coverage gap) | ccsession is not the only launch path. `ic` runs `exec claude ...` directly, and a Claude started by hand never passes ccsession. Orca's launches only pass ccsession when Orca's Claude command is configured as `ccsession-orca`. A ccsession-only fix therefore does not protect those coordinators. | `src/superclaude/scripts/ic:128-130`; `ccsession-orca:186,189,261,263` (`exec "$CCSESSION" ... --shim --claude-args`); `README.md:415` (requires the `ccsession-orca` configuration) |
| F4 | Medium (design decision) | There is no coordinator role signal in ccsession. `CCSESSION_ORIGIN` is `human` or `agent` and records who chose the session name, not the role; supervised workers start through the same `ccsession-orca` command. Coordinator-only protection cannot be done reliably today, so the issue's own fallback (protect all ccsession launches, document it) is the only verified option. The README states a coordinator may be opened by a person or by a script, so no launch-time test separates it. | `ccsession:2423-2438`; `ccsession-orca:39-41`; `README.md:423` |
| F5 | Medium | The settings route is unproven and a second route to maintain. The defaults file's `env` block holds three entries and not the switch; the installer merges `env` as a nested key. Whether Claude Code applies settings `env` before its pressure rule is UNVERIFIED (Claude says setting it "from a shell command has no effect"). Prefer the pre-exec export. | `src/superclaude/cli/user_settings_defaults.json:10-14` (origin/master); `src/superclaude/cli/install_user_setup.py:42` (`_NESTED_KEYS`) |
| F6 | Info (changes Part 2) | The Playwright plugin is now off by default for new installs on `origin/master` (PR #778, issue 764), so one of the four Part 2 candidates (an open Playwright browser and its plugin server, about 107 MB per session in the issue) no longer applies to fresh installs. The issue and its accuracy-check comment still describe it as enabled. | `git diff HEAD origin/master -- src/superclaude/cli/user_settings_defaults.json` (`"playwright@claude-plugins-official": false`); commits f2894fc44 (#778) and f03ca87e2 (#768) |
| F7 | Low (research target) | The codegraph SessionStart hook starts one detached `codegraph init --yes` per new checkout, gated only by the existence of that checkout's database and `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`. There is no cross-checkout lock or counter, which is the mechanism behind the issue's first-index memory peaks. Out of scope to change here. | `src/superclaude/hooks/scripts/codegraph-session-start.sh:11,25,31` |
| F8 | Info | Nothing in the repo sets, mentions or tests the switch yet; the three existing test files and their fake-Claude harness (`CLAUDE_BIN` set to a fake script) are the place to add launch tests. | `git grep DISABLE_BG_SHELL_PRESSURE_REAP origin/master` (no hit outside `.dev/`); `tests/unit/test_ccsession_tag.py:1619`; `tests/unit/test_ccsession_tiers.py`; `tests/unit/test_install_ccsession.py` |

## Recommendations

1. Part 1: add one exported assignment of `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` right after the identity block at `ccsession:2438`, decide the env-file override rule (F2), and document that it protects every background command in that new Claude process only (F3, F4).
2. Record the scope decision as "all ccsession launches" because no role signal exists (F4), and name `ic` and hand-started Claude as uncovered (F3).
3. Do not rely on settings `env` until timing is proven (F5).
4. Refresh Part 2's candidate list for F6 before measuring.

Not run: no dynamic analysis, no edits, no pressure test (quick depth, read-only).
