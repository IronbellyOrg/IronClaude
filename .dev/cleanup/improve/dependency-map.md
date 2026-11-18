# Dependency map: remove `/sc:improve` (6.0.0, PR 8)

Measured at `551d5ad38` (head of `integration` after the `/sc:build` removal), branch `clayphi/v6-improve`.
Method: `git grep` over tracked files for `sc:improve`, `sc:sc:improve`, `sc-improve`, `/improve`, `improve.md`,
`contained-improve`, `improve-report`, the bare word `improve` in command lists, and the converted-command counts;
then each hit read in place. The codegraph MCP server disconnected mid-session (same as the `/sc:build` PR), so no
codegraph callers/impact run is recorded. The item is a markdown command, not a code symbol: no Python or shell code
imports or calls it. Code that names it: the launch-level guard shell script (a message and a `case` list), one
sentence in `cli/recommend/prompts.py`, and tests.

The plan counted 3 files deleted and 19 edited outside (3 tests, 5 docs, 2 scripts, 12 other). Re-measured:
**3 files deleted (+1 untracked mirror), 7 tests edited (+1 fixture), 12 docs edited, 4 hook/script/source-code files
edited (2 hook mirrors), 15 other command/skill/core files edited.** The extra count comes from the shared sentence
"contained `/sc:cleanup` and `/sc:improve` work on a folder" (8 files), the legacy root `commands/` copies, the
worker-contract counts and the routing-refresh fixture.

Historical records, NOT edited: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/` (the launch-level design names
`/sc:improve` at lines 106, 179, 236, 391; its test applies removal rewrites), past `CHANGELOG.md` entries, `.dev/`
(research, eval workspaces, frozen task packages). The frozen routing-refresh package under `.dev/tasks/` is read by
tests and stays as it is.

Kept on purpose (not the command): `/sc:spec-panel --improve` (a spec-panel flag), the word "improve" in prose, `improve`
in `--loop` keyword docs, `docs/user-guide/flags.md:45`, the swarm `refactor_find` lens text, `execution/reflection.py`
vague-verbs list, the cli-eval suites.

## 1. Files deleted (3, plus 1 untracked mirror)

| Path | Why |
|---|---|
| `src/superclaude/commands/improve.md` | the command (source of truth) |
| `plugins/superclaude/commands/improve.md` | plugin mirror |
| `commands/sc-improve.md` | legacy root copy |
| `.claude/commands/sc/improve.md` | gitignored dev mirror; delete by hand, never stage |

## 2. Routing guide, worker contract, core CLAUDE.md (installed core docs)

Where `HOW-WE-WORK.md` appears, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` gets the same edit and must
stay byte-identical to the source copy.

| Path:line | Change |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md:22` | "contained `/sc:cleanup` and `/sc:improve` work on a folder" becomes "contained `/sc:cleanup` work on a folder" |
| `src/superclaude/core/CLAUDE.md:84` | same sentence, same edit (level-table block copied from HOW-WE-WORK; tests check both) |
| `src/superclaude/core/HOW-WE-WORK.md:169` | "no cleanup, improve or commit" becomes "no cleanup or commit" |
| `src/superclaude/core/HOW-WE-WORK.md:171-173` (3.7 item 2) | "Small, contained cleanups or improvements" becomes cleanups; drop the `/sc:improve` example and the "Improve also supports..." sentence; keep the `/sc:cleanup` example; "improve can change formatting, naming, imports and annotations" clause dropped; "An improvement-only request does not authorize compulsory cleanup/deletion" dropped; "Neither command's" becomes "The command's" |
| `src/superclaude/core/HOW-WE-WORK.md:249` | "Stop before cleanup, improve or commit" becomes "Stop before cleanup or commit" |
| `src/superclaude/core/HOW-WE-WORK.md:250` | delete the "Contained improvement" row |
| `src/superclaude/core/HOW-WE-WORK.md:365` | cleanup row notes: drop "and improvement-only uses contained-improve, with no compulsory cleanup/improve chain" |
| `src/superclaude/core/HOW-WE-WORK.md:376` | "no cleanup, improve or commit" becomes "no cleanup or commit" |
| `src/superclaude/core/HOW-WE-WORK.md:377` | delete the `contained-improve` row |
| `src/superclaude/core/HOW-WE-WORK.md:398` | "improve and cleanup skip approval-required items" becomes "cleanup skips approval-required items" |
| `plugins/.../refs/HOW-WE-WORK.md:22,169,171-173,249,250,365,376,377,398` | same edits (mirror) |
| `src/superclaude/core/WORKER-CONTRACT.md:330` | "the 14 commands converted in P2 (auggie-review, cleanup, improve, ...)" becomes 13, drop `improve` |
| `src/superclaude/core/WORKER-CONTRACT.md:331` | "`/sc:improve` and `/sc:cleanup` skip every approval-required item" becomes "`/sc:cleanup` skips ..." |

## 3. Commands and skills that point a reader to `/sc:improve`

| Path:line | Change |
|---|---|
| `src/superclaude/commands/analyze.md:139` | "use `/sc:improve` to apply recommended fixes or `/sc:cleanup` for dead code removal" becomes "use `/sc:cleanup` for dead code removal" (drop the clause) |
| `src/superclaude/commands/adversarial.md:195` | delete the `/sc:improve` row of the integration table |
| `src/superclaude/skills/sc-recommend/SKILL.md:171` (+ plugin mirror) | "contained-folder cleanup/improve exception" becomes "contained-folder cleanup exception" |
| `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md:41` (+ plugin mirror) | "`/sc:cleanup` and `/sc:improve` exception" becomes "`/sc:cleanup` exception" |
| `src/superclaude/cli/recommend/prompts.py:195` | "contained-folder cleanup/improve exception" becomes "cleanup exception" (check a test that pins the prompt text) |
| `src/superclaude/skills/sc-cli-portify-protocol/refs/analysis-protocol.md:222` | "Found in: implement, improve" becomes "Found in: implement" |
| `src/superclaude/core/BUSINESS_PANEL_EXAMPLES.md:78-84,168,211` (+ `plugins/superclaude/core/` copy) | the bare `/improve` examples name the removed command: drop the "Combined with /improve" block, the `→ /improve roadmap` step and the `/improve` stage |

## 4. Hook scripts (source and plugin mirror)

| Path:line | Change |
|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh:43` | "starting /sc:implement, /task, /sc:improve or /sc:cleanup (or their skills)." becomes "starting /sc:implement, /task or /sc:cleanup (or their skills)." |
| `src/superclaude/hooks/scripts/launch-level-guard.sh:409` | `case` list: planned to drop `improve`; REVISED after the PR 627 reviews: `improve` stays in the list (trailing comment) until the retire step (PR 12) removes installed copies, because an upgraded workspace keeps the old installed `improve.md` and its Skill call would otherwise skip the worktree-level approval gate. `IMPL_SPELLINGS` keeps `sc:improve`; the IMPL row of the architecture reference names the retired `improve`. |
| `plugins/superclaude/hooks/scripts/launch-level-guard.sh:43,409` | same edits as the source copy (mirror; the two files stay identical) |

## 5. Tests

| Path:line | Change |
|---|---|
| `tests/core/test_how_we_work_routing_table.py:83` | drop `"contained-improve"` from the expected row ids |
| `tests/core/test_how_we_work_routing_table.py:500` | assertion text: "contained `/sc:cleanup` work on a folder" |
| `tests/core/test_how_we_work_routing_table.py:644` | S04 phrase "no cleanup, improve or commit" becomes "no cleanup or commit" |
| `tests/core/test_how_we_work_routing_table.py:647-656` | delete the S05 scenario tuple |
| `tests/core/test_how_we_work_routing_table.py:874-888` | rename to cleanup-audit boundaries only; drop the `improve` assertions (keep the audit assertions and the "sc:cleanup row has no sc:improve" idea as nothing) |
| `tests/hooks/test_launch_level_guard.py:80-83` | extend `_REMOVED_COMMAND_TEXT`: add `("/task, /sc:improve or /sc:cleanup", "/task or /sc:cleanup")`; comment names improve |
| `tests/hooks/test_launch_level_guard.py:916` | drop `"sc:improve"` from `IMPL_SPELLINGS` |
| `tests/recommend/test_routing_refresh.py:39` | `_POST_REFRESH_REMOVALS` gains `"improve"`; comment updated |
| `tests/recommend/test_routing_refresh.py:~140` | retired case ids: S05 joins S25, S27; docstring line 3-4 |
| `tests/recommend/test_routing_refresh.py:299-304` | `test_flag_value_check_rejects_undeclared_enumerated_value` reads `improve.md` for an example-only flag; use another kept command that has an example-only flag (found while editing) or drop that sub-assertion |
| `tests/recommend/fixtures/routing_refresh_cases.json:134-151` | delete case S05 |
| `tests/recommend/fixtures/routing_refresh_cases.json:122,123,186,578` | S04 guide phrase "no cleanup or commit"; drop `sc:improve` from the competitor lists |
| `tests/recommend/fixtures/routing_refresh_cases.json:706` | NO change: frozen record of the 47 commands of the refresh package (the removal set accounts for it); T13 line 622 test stays and is edited above |
| `tests/skills/test_worker_contract.py:498` | drop `"improve"` from `P2_COMMANDS`; comment "fifteen" (check the true count in place) |
| `tests/skills/test_worker_contract.py:624-635` | delete the `improve` entry of `UNATTENDED_EXPECT` |
| `tests/skills/test_worker_contract.py:1630-1631` | `len(p2) == 14` becomes 13 (messages too) |
| `tests/skills/test_worker_contract.py:1637` | `len(expect) == 29` becomes 28 (message too) |
| `tests/skills/test_worker_contract.py:1755-1756` | drop the two `("improve", ...)` rows of `P2_GATES` |
| `tests/unit/test_cli_install.py:116,403` | drop `improve.md` from the two expected file-name lists |
| `tests/sc-roadmap/compliance/test_critical_corrections.py:105` | NO change: a self-contained list of the 7 wave-enabled commands of the old roadmap (`/build` is still in it too); it reads no file |

Tests that adapt on their own (no edit expected): the `make verify-sync` mirror parity tests, the sync tests, tests that
glob `src/superclaude/commands`. Confirmed by the after-run.

## 6. Docs (current, so edited)

| Path:line | Change |
|---|---|
| `docs/user-guide/commands.md:82` | delete the `/sc:improve` row of the command table |
| `docs/user-guide/commands.md:1039-1067` | delete the `### /sc:improve - Code Improvement` section and its trailing `---` |
| `docs/user-guide/flags.md:75-81` | delete the `### Improve Command Flags (/sc:improve)` block |
| `docs/user-guide/mcp-servers.md:91-93` | Morphllm example uses `/sc:improve legacy-codebase/ ...`: drop the two-line "Automatic activation" example, keep the API key setup |
| `docs/user-guide/agents.md:157` | "`/sc:implement` and `/sc:improve` do not call it" becomes "`/sc:implement` does not call it" |
| `docs/user-guide/agents.md:846` | delete the `/sc:improve` row of the Command-Agent Mapping table |
| `docs/onboarding/ironclaude-onboarding.html:318,323,335,341` | "contained /sc:cleanup and /sc:improve work" becomes "contained /sc:cleanup work" (4 places) |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1605` | IMPL class row: drop `improve` |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:81,196,290,317,710,745,1319,1321,1840,1958,2197,2203,2230` | converted-command counts 29 becomes 28 and P2 "14" becomes 13 (read each in place; line 1840 "exactly 14 P2 names" and "len(expect) == 29"); line 2203 "31 commands; 29 remain" becomes 28 remain |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:976` | "All 29 converted commands (15 from phase 1, 14 from phase 2)" becomes 28 (15 + 13); "those 29 entries" becomes 28 |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1315` | read in place; edit only if it names the command |
| `commands/sc-help.md:40` | delete the table row |
| `commands/sc-analyze.md:98` | "use `/sc:sc:improve` to apply recommended fixes or `/sc:sc:cleanup`" becomes "use `/sc:sc:cleanup` for dead code removal" |
| `commands/sc-troubleshoot.md:120` | "Use `/sc:sc:improve` for broader refactoring" becomes "Use `/sc:sc:cleanup` for broader refactoring"? Read in place; the cleanup command is the kept refactor/cleanup command, otherwise drop the line |
| `commands/sc-recommend.md` (14 lines naming `/sc:sc:improve`, the `improve_category` block and the `refactor|cleanup|improve|quality` keyword rule) | legacy v4-era text. Remove each `/sc:sc:improve ...` entry from lists and numbered flows (renumber), drop the `improve_category` block's improve entry (keep `/sc:sc:cleanup`), and replace the "RECOMMENDED COMMAND" example with `/sc:sc:analyze ...` (read each in place; see the previous PR's edits) |

Not edited, kept deliberately: `docs/developer-guide/README.md`, `docs/generated/sprint-cli/10-critique-validation.md` and other
files that say "improve" as an ordinary word; `commands/sc-spec-panel.md` and `spec-panel.md` `--improve` flag.

## 7. Install code, hooks registration, packaging

- `src/superclaude/cli/install_commands.py`, `doctor`, `pyproject.toml`, `Makefile`: no entry names `improve.md`; the
  install copies every file in `commands/`, so deleting the source file removes it from the install.
- `src/superclaude/cli/recommend/cache.py` globs `commands/*.md`; the surface fingerprint changes by itself.
- `.claude/settings.json`: no mention.
- `PROJECT_INDEX.md` / `.json`, `README.md`, `AGENTS.md`: no mention found by `git grep`.

## 8. Final search (run after the edits)

`git grep -n -I -E 'sc[:/_-]+improve|sc-improve|/improve\b|improve\.md|commands/improve|contained-improve|improve-report' -- . ':!.dev' ':!docs/releases' ':!docs/testing' ':!docs/designs' ':!CHANGELOG.md'`
must print only the kept hits listed above (`tests/sc-roadmap/compliance/test_critical_corrections.py` and the frozen fixture
line 706 `analyses/improve.md`).
