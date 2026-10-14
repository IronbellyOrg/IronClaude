# Research: Machinery and References for IronClaude Routing-Doc Consolidation
**Scope:** /tmp/ic-master (snapshot of IronClaude origin/master) install/packaging, tests, hooks, CI, doc link graph for the routing-doc candidate files. CI also checked at /Users/cmerritt/GFxAI/IronClaude-tier-tools/.github.
**Status:** Complete
**Date:** 2026-10-12
**Mode:** Read-only research. Only this file was written.

Snapshot identity: `/tmp/ic-master/SNAPSHOT.txt` says "snapshot of origin/master ee1c1787 (2026-10-11)". All paths below are relative to `/tmp/ic-master` unless absolute.

---

## 1. Install and packaging machinery

### 1.1 `superclaude install` and `superclaude update` (src/superclaude/cli/main.py)

| Step | Code | What it does with candidate files |
|---|---|---|
| install Step 1 | `main.py:155-161` calls `install_core_files(force=force)` | Copies every `*.md` in the package `core/` dir to `~/.claude/`. |
| install Step 2 | `main.py:163-171` calls `install_commands(target_path=~/.claude/commands/sc)` | Copies every `*.md` in the package `commands/` dir to `~/.claude/commands/sc/`. |
| install `--list` | `main.py:88-97` | Prints `list_core_files()` vs `list_installed_core_files()`. |
| update | `main.py:284-370`; core at `main.py:307-310` (force=True), commands at `main.py:313-318` (force=True) | Same copy, always overwriting. |
| exit code | `main.py:220-231` (install), `main.py:349-361` (update) | Any failed step makes the CLI exit 1. |

[CODE-VERIFIED] Neither install nor update ever deletes files. `install_core.py:48-59` and `install_commands.py:46-60` only copy. So retiring a core file or a command in source leaves the previously installed copy in every user's `~/.claude/` and `~/.claude/commands/sc/` forever, unless a cleanup step is added. This is the single biggest machinery gap for any retirement.

### 1.2 `install_core.py` (155 lines)

- `install_core_files` (`install_core.py:13-86`): `core_source.glob("*.md")` at line 39, then `shutil.copy2` to `~/.claude/<name>` at line 56. No allow-list on the copy side: any `.md` in `core/` ships, any removed `.md` simply stops shipping.
- `_get_core_source` (`install_core.py:89-108`): package `core/` dir only.
- `list_installed_core_files` (`install_core.py:126-155`): HARD-CODED `known_core` set at lines 139-153 naming `COMMANDS.md` (144), `FLAGS.md` (145), `MODES.md` (147), `ORCHESTRATOR.md` (148), `PERSONAS.md` (149), plus 8 others. If a candidate is retired, this set goes stale (it only affects the `install --list` status display, not install success). If a candidate is renamed, `install --list` will report the new name as "not installed" forever until this set is updated.
- Current `src/superclaude/core/*.md` line counts: COMMANDS.md 195, FLAGS.md 146, MODES.md 307, ORCHESTRATOR.md 389, PERSONAS.md 214, CLAUDE.md 150.
- [CODE-VERIFIED] `src/superclaude/core/CLAUDE.md` (installed as `~/.claude/CLAUDE.md`) `@`-imports only `@BASH_INSPECTION_POLICY.md` (line 3). It does NOT `@`-import ORCHESTRATOR, COMMANDS, MODES, FLAGS, or PERSONAS. Those five are copied to `~/.claude/` but are not auto-loaded by the shipped CLAUDE.md. Its "Key Docs" list (lines 89-95) names `KNOWLEDGE.md` and mentions `/sc:help` at line 100.

### 1.3 `install_commands.py` (162 lines)

- `install_commands` (`install_commands.py:12-89`): `command_source.glob("*.md")` at line 37, copy at line 57. It copies `README.md` too (no README filter on the copy path), so `src/superclaude/commands/README.md` lands at `~/.claude/commands/sc/README.md` and therefore surfaces as a `/sc:README` command. [CODE-VERIFIED]
- `_get_commands_source` (`install_commands.py:92-122`): priority 1 package `commands/`; priority 2 `plugins/superclaude/commands/` in a source checkout (lines 112-119).
- `list_available_commands` / `list_installed_commands` (`install_commands.py:125-162`): skip `README` by stem (lines 139, 159). No hard-coded command names.

### 1.4 `install_skill` / `install_skills`

- `superclaude install-skill <name>` (`main.py:372-405`) calls `install_skill_command`. Skills are installed by directory; none of the candidate files is a skill. The only skill coupled to a candidate is `src/superclaude/skills/sc-recommend/` (paired with `commands/recommend.md` via `## Activation` at `recommend.md:52-56`, `> Skill sc-recommend`).
- `doctor._check_skills_installed` (`src/superclaude/cli/doctor.py:185-225`) scans every installed `~/.claude/commands/sc/*.md` for activation targets and FAILS the "Skills installed" check if a command names a skill that is not installed (lines 205-219). Consequence: if `sc-recommend` skill is retired but a stale `~/.claude/commands/sc/recommend.md` remains (see 1.1, nothing deletes it), `superclaude doctor` fails on that machine. [CODE-VERIFIED]

### 1.5 Packaging metadata

| File | Evidence | Effect on candidates |
|---|---|---|
| `MANIFEST.in` | line 2 `include README.md`; `recursive-include docs *.md *.json *.py`; `recursive-include src/superclaude/commands *.md`; `recursive-include src/superclaude/core *.md`; `recursive-include plugins/superclaude/commands *.md`; `recursive-include plugins/superclaude/core *.md` | Glob-based. Removal or rename needs no edit. `README.md` is named explicitly: removing README.md would make this line dangle (setuptools warns, does not fail). |
| `pyproject.toml:9` | `readme = "README.md"` | README.md is the PyPI long description. Removing or renaming README.md breaks `python -m build` / `twine check` in `publish-pypi.yml:91,98`. |
| `pyproject.toml:79-88` | wheel `packages = ["src/superclaude"]`, `include = ["src/**", "plugins/**"]`, force-include `src` to `superclaude/_src` and `plugins` to `superclaude/_plugins` | Glob-based. All of `src/superclaude/core`, `commands`, and all of `plugins/` ship. No candidate named. |
| `pyproject.toml:90-98` | sdist includes `src/`, `plugins/`, `tests/`, `README.md` | README.md named explicitly. |
| `setup.py` | 11 lines, `setup()` only, defers to pyproject | Nothing. |
| `package.json` | `"files": ["bin/", "README.md", "LICENSE"]`; `postinstall: node ./bin/install.js` | Names README.md. `bin/` does NOT exist in the snapshot (`ls bin` failed), so the npm wrapper is already broken independently. [CODE-VERIFIED] |
| `update.sh` | `pipx install --force ./`; `superclaude install --force`; `make sync-dev`; `superclaude doctor` | Runs the copy paths in 1.1 and the doctor check in 1.4. |

### 1.6 Makefile targets

| Target | Lines | Behavior relevant to candidates |
|---|---|---|
| `sync-dev` | `Makefile:109-165` (README skip at line 134) | Copies `src/superclaude/commands/*.md` to `.claude/commands/sc/` but SKIPS `README.md` (`case "$$name" in README.md|__init__.py) continue`). Does NOT copy `core/` at all. Never deletes stale mirrors. |
| `verify-sync` | `Makefile:166-354` (Commands block 228-251; reverse-missing message line 249) | "=== Commands ===" block: every `src/superclaude/commands/*.md` (except README) must exist and be byte-identical in `.claude/commands/sc/`; reverse loop fails with "MISSING in src/superclaude/commands/: <name> (not distributable!)" for any `.claude/commands/sc/*.md` with no source. `core/` and `docs/` are not checked. |
| `lint-architecture` | `Makefile:362-495` (Check 1/2 at 368; Check 3/4 at 398-410) | Check 1: a command with `## Activation` must have `skills/sc-<name>-protocol` or `skills/sc-<name>`. `recommend.md` passes via `sc-recommend`. Check 2: each `skills/sc-*-protocol/` must have `commands/<name>.md` (sc-recommend has no `-protocol` suffix, so it is not in Check 2). Checks 3/4: command line count warn >200, ERROR >500 (applies to `help.md` 149, `recommend.md` 134; README skipped). |
| `build-plugin` / `sync-plugin-repo` | `Makefile:69-88` | Runs `scripts/build_superclaude_plugin.py`; rsyncs `dist/plugins/superclaude/{agents,commands,hooks,scripts,skills,.claude-plugin}` to `../SuperClaude_Plugin` with `--delete`. `core/` and `modes/` are NOT built or synced. |
| `help` | `Makefile:530-563` | Static echo text; mentions `make translate` README-zh/ja. No candidate path. |

Consequence of `verify-sync` + no-delete `sync-dev` [CODE-VERIFIED by reading both loops]: if `src/superclaude/commands/help.md` or `recommend.md` is deleted, any developer machine that previously ran `make sync-dev` still has `.claude/commands/sc/help.md`, and `make verify-sync` then FAILS with "MISSING in src/superclaude/commands/: help.md (not distributable!)" until the stale mirror is deleted by hand. In CI this does not fire because `.claude/*` is gitignored (`.gitignore:120-121`, only `.claude/settings.json` is tracked) and CI starts from a clean checkout.

### 1.7 Scripts

| Script | Evidence | Effect |
|---|---|---|
| `scripts/build_superclaude_plugin.py` (101 lines) | `PLUGIN_SRC = ROOT/"plugins"/"superclaude"` line 16; copies only `["agents","commands","hooks","scripts","skills"]` line 75 | Copies `plugins/superclaude/commands/help.md` and `recommend.md` into `dist/`. Never touches `plugins/superclaude/core/` or root `commands/`. |
| `scripts/sync_from_framework.py` (928 lines) | `SYNC_MAPPINGS` lines 443-447: `src/superclaude/commands` to `commands` (adds `sc-` prefix), `src/superclaude/agents` to `agents`. `PROTECTED_PATHS` lines 457-480 includes `README.md`, `docs/`, `core/`, `modes/`. Stale-removal at lines 241-247 deletes `sc-*` files in the destination that no longer exist in the source. `PluginJsonGenerator` lines 303-355 builds `.claude-plugin/plugin.json` command map from `commands/sc-*.md`. | This is the GENERATOR of root `commands/sc-*.md` (including `sc-help.md`, `sc-recommend.md`, `sc-README.md`). It pulls from the UPSTREAM `SuperClaude-Org/SuperClaude_Framework` repo, not from this repo's own `src/`. Deleting `src/superclaude/commands/help.md` in IronClaude does NOT trigger removal of root `commands/sc-help.md`; that file only changes if upstream changes. |
| `scripts/precommit_block_claude_mirrors.sh` (22 lines) | lines 4-11 | Blocks committing staged `.claude/{skills,agents,commands,hooks,templates}`. Not candidate-specific. |
| `scripts/check-ref-staleness.py` | lines 19-38 | Only checks cli-portify refs vs pipeline models. Not candidate-related. |
| `scripts/uninstall_legacy.sh` | `SUPERCLAUDE_ITEMS` array lines 23-30 | Removes legacy plugin dirs and json configs only; does not remove `~/.claude/COMMANDS.md` etc. No candidate named. |
| `src/superclaude/hooks/scripts/sc-recommend-phase0.sh` | lines 38-60 | Tells the model to Glob `src/superclaude/commands/*.md` and skills; no candidate file named. Tied to the `sc-recommend` skill name (lines 33-36), not to `recommend.md`. |

### 1.8 Mirror map (who is a copy of whom)

| Candidate | Source of truth | Mirrors | Generated by | Byte-identical today? |
|---|---|---|---|---|
| `src/superclaude/core/{ORCHESTRATOR,COMMANDS,MODES,PERSONAS}.md` | `src/superclaude/core/` | `~/.claude/<name>` (install) | `install_core_files` | n/a. Not present in `plugins/superclaude/core/` at all (that dir has only BUSINESS_PANEL_EXAMPLES, BUSINESS_SYMBOLS, FLAGS, PRINCIPLES, RESEARCH_CONFIG, RULES). |
| `src/superclaude/core/FLAGS.md` | `src/superclaude/core/` | `plugins/superclaude/core/FLAGS.md`; `~/.claude/FLAGS.md` | install; plugins copy is hand-maintained (sync script marks `core/` PROTECTED) | NO: `diff -q` reports src vs plugins FLAGS.md differ. |
| `src/superclaude/commands/help.md` (149 lines) | `src/superclaude/commands/` | `.claude/commands/sc/help.md` (sync-dev); `~/.claude/commands/sc/help.md` (install); `plugins/superclaude/commands/help.md` (149 lines, hand-maintained); root `commands/sc-help.md` (147 lines, generated from upstream) | sync-dev, install, sync_from_framework | NO: src differs from both plugins and root copies. |
| `src/superclaude/commands/recommend.md` (134 lines) | `src/superclaude/commands/` | `.claude/commands/sc/`, `~/.claude/commands/sc/`, `plugins/superclaude/commands/recommend.md` (134 lines), root `commands/sc-recommend.md` (1011 lines, an older full-protocol version from upstream) | same | src vs plugins: `diff -q` reported no difference (identical). src vs root: differ heavily. |
| `src/superclaude/commands/README.md` (22 lines) | `src/superclaude/commands/` | `~/.claude/commands/sc/README.md` (install copies it); root `commands/sc-README.md` (21 lines) | install, sync_from_framework | Differs from root copy. NOT mirrored by sync-dev (README skipped). Not present in `plugins/superclaude/commands/`. |

No CI or Makefile check compares `src/` against `plugins/` or against root `commands/`. The only enforced mirror check is `make verify-sync` (src vs `.claude/`, commands only). [CODE-VERIFIED: grep of Makefile and workflows for `plugins/` shows only build-plugin/sync-plugin-repo copy steps, no diff steps.] Note: some pytest tests DO enforce src-vs-plugins byte equality for specific non-candidate commands (see 2.3), which is the precedent a future guard for `help.md`/`recommend.md` would follow.

### 1.9 Hidden coupling: `recommend.md` and the `sc-recommend` skill install decision

`src/superclaude/cli/install_skills.py:40-59` `_has_corresponding_command("sc-recommend")` returns True (skill is SKIPPED as "served by /sc: command", lines 86-91, 124-128) when `commands/recommend.md` exists AND does NOT contain an activation line matching `_SKILL_ACTIVATION_RE` (lines 30-32, `> Skill sc-recommend`). Today `recommend.md:56` has `> Skill sc-recommend`, so the skill installs. Consequences [CODE-VERIFIED]:
- Delete `recommend.md` entirely: skill still installs (no command file, function returns False).
- Keep `recommend.md` but rewrite it without the `> Skill sc-recommend` line: the `sc-recommend` skill silently STOPS installing, and `tests/unit/test_cli_doctor.py:79` fails.

---

## 2. Tests that touch candidate files

Search scope: every `*.py` under `/tmp/ic-master/tests` grepped for each candidate basename, `install_core`, `install_commands`, `known_core`, `docs/` roots, `src/superclaude/core`, `src/superclaude/commands`, and `plugins/superclaude`. Matches in `tests/audit/*` use synthetic in-memory path strings (for example `"docs/README.md"` in `test_docs_audit.py:47`), not the real files, and are excluded.

### 2.1 Tests that would FAIL on a removal or rename

| Test | Evidence | Candidate | Breaks when |
|---|---|---|---|
| `tests/unit/test_cli_install.py::TestInstallCommands::test_all_expected_commands_available` | lines 134-143: `expected = ["agent", "index-repo", "recommend", "research"]` asserted in `list_available_commands()` | `src/superclaude/commands/recommend.md` | `recommend.md` is removed or renamed. (`help` is NOT in this list.) |
| `tests/unit/test_cli_doctor.py::test_isolated_install_resolves_every_command_dependency` | lines 68-80: installs all commands + skills into tmp, asserts `(skills_dir / "sc-recommend" / "SKILL.md").exists()` (line 79) and doctor passes | `recommend.md` content plus the `sc-recommend` skill | `recommend.md` kept but its `> Skill sc-recommend` activation line removed (skill becomes "served_by_command" and is not installed, see 1.9); or any surviving command names a skill that no longer exists. |
| `tests/cli/test_bash_inspection_policy.py::test_global_claude_imports_policy` | lines 31-33: `"@BASH_INSPECTION_POLICY.md" in core/CLAUDE.md` | `src/superclaude/core/CLAUDE.md` (not a candidate, but it is the file most likely to be edited to point at a consolidated routing doc) | The `@BASH_INSPECTION_POLICY.md` import line is dropped during a CLAUDE.md rewrite. |
| `tests/cli/test_bash_inspection_policy.py::test_core_install_and_listing_include_policy` | lines 36-44: installs core, asserts `"BASH_INSPECTION_POLICY.md" in install_core.list_installed_core_files()` | `install_core.py` `known_core` set | Someone edits `known_core` (lines 139-153) to remove retired candidates and accidentally drops `BASH_INSPECTION_POLICY.md`. Removing ORCHESTRATOR/COMMANDS/MODES/FLAGS/PERSONAS from `known_core` does not break this test. |

### 2.1a Environment-dependent failure: `test_V1_clean_tree_exits_zero`

`tests/cli/test_verify_sync_hooks.py:58-66` runs the REAL `make verify-sync` with `cwd=REPO_ROOT` (not a tmp tree; docstring lines 7-15 say mutation is in place), and `test_V1_clean_tree_exits_zero` (lines 124-143) asserts `returncode == 0`. The Makefile Commands reverse loop (`Makefile:244-251`) fails on any `.claude/commands/sc/<name>.md` that has no `src/superclaude/commands/<name>.md`. So after deleting or renaming `help.md` or `recommend.md` in `src/`:
- On any developer machine with a previously synced `.claude/commands/sc/help.md`, this test FAILS until the stale mirror is deleted (because `make sync-dev` never deletes). [CODE-VERIFIED]
- In CI it PASSES, because `.claude/*` is gitignored (`.gitignore:120-121`) and `test.yml:51-52` runs `make sync-dev` on a clean checkout before pytest.

### 2.2 Tests that are content guards over the whole `docs/` and `src/superclaude/` trees

These do not name a candidate, but every candidate file under `docs/` or `src/superclaude/` is scanned, so a rewritten or merged routing doc must obey them.

| Test | Evidence | Constraint on a consolidated doc |
|---|---|---|
| `tests/docs/test_tavily_doc_alignment.py::test_iter_text_files_is_nonvacuous` | line 13 `_ROOTS = [src/superclaude, docs]`; lines 65-74 assert more than 100 text files | Snapshot has 906 files under `src/superclaude` + `docs` (`find ... | wc -l`, includes non-text). Retiring roughly 20 docs will not approach the floor. Not a practical risk. |
| `...::test_tavily_version_single_pin` | lines 76-85 | Any `tavily-mcp@<ver>` must be `0.2.22`. |
| `...::test_no_stale_mcp_tavily_token` | lines 37, 88-96 | No `mcp.tavily` token (except `mcp.tavily.com`). |
| `...::test_no_tavily_json_references` | lines 98-107 | No reference to the deleted `tavily.json`. |
| `...::test_docs_no_default_params_duplication` | lines 110-130 | Files under `docs/` must not contain `"search_depth"`, `search_depth: basic`, or `max_results: 10`. Relevant because `docs/user-guide/flags.md`, `commands.md`, and `docs/reference/comprehensive-features.md` all discuss tavily today; a merged doc must keep pointing to `MCP_Tavily.md` instead of restating params. |
| `tests/docs/test_chrome_devtools_mcp_removed.py` | lines 8-24 | Asserts specific MCP doc files are absent/present. Not a candidate, but `docs/user-guide/flags.md:198` and `PROJECT_INDEX.md:232` and `README.md:220` still mention Chrome DevTools in prose; this test does not scan prose, so no failure. |

### 2.3 Tests that pin src-vs-plugins equality (precedent, not candidates)

- `tests/commands/test_workflow_command.py:86-87` asserts `filecmp.cmp(src/.../commands/workflow.md, plugins/.../commands/workflow.md)`.
- `tests/skills/test_task_workspace_smoke.py:41-47` `test_plugin_commands_match_canonical` asserts the same for `workflow.md` and `implement.md`.
- No equivalent test exists for `help.md`, `recommend.md`, `README.md`, or any `core/` file. [CODE-VERIFIED by grep for `plugins/superclaude/commands` and `plugins" / "superclaude` in tests]

### 2.4 Tests that mention a candidate but do NOT depend on it

| Test | Evidence | Why it is safe |
|---|---|---|
| `tests/sc-roadmap/compliance/test_critical_corrections.py::TestCriticalCorrection3` | docstrings lines 7, 61 say "Compliance tiers from ORCHESTRATOR.md"; assertions lines 63-73 only check the sc-roadmap SKILL.md for `STANDARD`, `STRICT`, `escalat` | Never opens ORCHESTRATOR.md. Docstring becomes stale if ORCHESTRATOR.md is retired (cosmetic). |
| `tests/cli/test_update_command.py` | lines 16-17, 49-50, 76-77, 97-100 monkeypatch `install_core_files`, `install_commands`, `list_core_files`, `list_installed_core_files`, `list_available_commands`, `list_installed_commands` by dotted path | Breaks only if those FUNCTIONS are renamed, not if candidate files change. |
| `tests/cli/test_install_failures.py` | lines 20-21, 36-52 | Patches copy errors in `install_core_files` / `install_commands`; asserts the empty sentinel strings `"No core framework files were installed"` / `"No commands were installed"`. Independent of which files exist, as long as at least one core `.md` and one command `.md` remain. |
| `tests/unit/test_cli_install.py` other tests | lines 17-24, 26-42, 121-132 | Pin `research` and `index-repo` commands, not candidates. |
| `tests/cli/test_init_lite.py` | lines 44-69, 118-123 | Builds a fake `.claude/commands/README.md` in tmp; does not read the real one. |
| `tests/recommend/*` | `cli/recommend/commands.py:26-27` uses `.claude/cache/sc-recommend-lookup.yaml` | Tests the `superclaude recommend` helper CLI, not `commands/recommend.md`. |

### 2.5 Tests with no coverage (negative results)

No test asserts on: the content or line count of ORCHESTRATOR.md, COMMANDS.md, MODES.md, FLAGS.md, PERSONAS.md; the existence or content of `commands/help.md` or `commands/README.md`; any file under `docs/user-guide/`, `docs/getting-started/`, or the named `docs/reference/*` files; `README.md` links; `KNOWLEDGE.md`; `PROJECT_INDEX.md` or `PROJECT_INDEX.json`; root `commands/sc-*.md`; or `plugins/superclaude/commands/help.md` / `recommend.md`. No doc link checker exists in the pytest suite. [CODE-VERIFIED by the grep set described at the top of section 2]

---

## 3. Hooks and CI

### 3.1 Hooks

| Hook surface | Evidence | Reads or validates a candidate? |
|---|---|---|
| `src/superclaude/hooks/hooks.json` (installed to `~/.claude/settings.json` by `install_hooks`) | registrations at lines 7-105: `session-init.sh`, `freshness-*.sh`, `auggie-flag-clear.sh`, `pragmatic-subagent.js`, ccsession hook | No. |
| `freshness-subagent-start.sh` | line 7 `POLICY_FILE="$HOME/.claude/BASH_INSPECTION_POLICY.md"` | Reads an installed core file, but NOT a candidate. Shows the pattern: hooks can depend on `~/.claude/<core>.md` names. |
| `pragmatic-subagent.js` | line 7 reads `~/.claude/output-styles/pragmatic.md` | No. |
| `freshness-session-start.sh` | lines 60-65 read memory index files | No. |
| `sc-recommend-phase0.sh` (PreToolUse Skill) | lines 33-36 match skill name `sc-recommend` / `sc:recommend` / `sc-recommend-protocol`; lines 42-46 tell the model to Glob `src/superclaude/commands/*.md` | Keyed on the SKILL name, not on `commands/recommend.md`. Renaming the `sc-recommend` skill breaks this gate silently (fail-open, exit 0). Retiring `recommend.md` alone does not. |
| `reject-workspace-writes.sh` | line 34 mentions `.dev/README.md` | No. |
| Repo `.claude/settings.json` (only tracked file under `.claude/`) | registers `reject-workspace-writes.sh` and `sc-recommend-phase0.sh` (PreToolUse) | Same as above; no candidate path. |
| `src/superclaude/scripts/session-init.sh` | grep for `.md` found nothing relevant | No. |
| `src/superclaude/scripts/clean_command_names.py` (also in `plugins/superclaude/scripts/`) | lines 1-40: strips `name:` frontmatter from command files under a plugin root found via `plugin.json` | Would touch `help.md`/`recommend.md` frontmatter if run, but nothing in Makefile, CI, or install invokes it. [CODE-VERIFIED by grep for `clean_command_names` outside `.dev/`: only its own docstrings] |

Conclusion: no hook reads, validates, or indexes any candidate file. [CODE-VERIFIED by grep of `src/superclaude/hooks/scripts/*`, `hooks.json`, `src/superclaude/scripts/*` for each candidate basename and for `docs/`]

### 3.2 CI workflows

Both `/tmp/ic-master/.github/workflows/` and `/Users/cmerritt/GFxAI/IronClaude-tier-tools/.github/workflows/` contain the same 8 files, and every file is byte-identical between the two (`cmp -s` per file, all "same"). Tier-tools HEAD is `a7041dd8` (2026-10-02), older than the snapshot, but CI did not change.

| Workflow | Trigger | Steps relevant to candidates | Breaks on candidate removal/rename? |
|---|---|---|---|
| `test.yml` | push/PR to `master`, `integration` (lines 3-7) | `make sync-dev` (51-52) then `pytest -v` (55-56) on 3.10/3.11/3.12; swarm marker jobs; ruff lint+format (lines 130-136); pytest plugin check | YES via pytest: `test_all_expected_commands_available` if `recommend.md` goes; `test_isolated_install_resolves_every_command_dependency` if `recommend.md` loses its activation line. |
| `quick-check.yml` | push/PR to `master`, `integration` (line 5) | `pytest tests/unit/ -x` (32-33); `make sync-dev` (48-49); `make verify-sync` (52-53); `make lint-architecture` (56-57) | YES: `tests/unit/test_cli_install.py` is in `tests/unit/` (recommend). `verify-sync` passes on a clean checkout. `lint-architecture` Check 1 fails if `recommend.md` keeps `## Activation` but the `sc-recommend` skill dir is removed or renamed; Check 4 fails if a merged `help.md` exceeds 500 lines (warns over 200). |
| `readme-quality-check.yml` | PR touching `README*.md` or `Docs/**/*.md` (capital D, lines 5-7, so `docs/` lowercase edits do not trigger on PR); every push to `main`/`master`/`develop` (line 9) | Embedded checker: `readme_files = ['README.md','README-zh.md','README-ja.md','README-kr.md']` (line 55); extracts every `[text](url)` (line 105); for non-http, non-`#` URLs checks `os.path.exists(url)` from repo root and counts broken (lines 113-117); link score `100 - 10*broken`, link status FAIL under 80 (line 145); job exits 1 when overall score under 70 (line 255). | LOW RISK, but this is the ONLY doc link checker in CI, and it checks only root `README*.md` markdown links. Simulated on the snapshot with the same regex (`python3 -I`, read-only): `README.md` has only 2 markdown-syntax links, both local: `docs/user-guide/freshness-hooks.md` (exists) and `.dev/releases/current/cliEval/decisions.md` (already BROKEN). Score formula (lines 190-197): average of structure (100, only one README exists), link (`100 - 10*broken`), translation (60, because README-zh/ja/kr are missing). Today: (100 + 90 + 60) // 3 = 83, PASS. The job fails (under 70) only at 6 or more broken links. Because README.md references the candidate docs as plain paths or HTML, not `[text](path)` links (see section 4), retiring candidate docs does not move this score. Adding new `[text](docs/...)` links to retired files in a README rewrite would. |
| `pull-sync-framework.yml` | cron every 6h + manual (lines 3-6) | Runs `scripts/sync_from_framework.py` against UPSTREAM SuperClaude_Framework (lines 43-60); protection check on README.md, SECURITY.md, CLAUDE.md, LICENSE, .gitignore (lines 63-83); commits `commands/`, `agents/`, plugin.json and pushes to master (lines 95-120) | Regenerates root `commands/sc-*.md` from UPSTREAM. Any local retirement of root `commands/sc-help.md`, `sc-recommend.md`, or `sc-README.md` will be RE-CREATED by the next scheduled sync if upstream still has `help.md`/`recommend.md`/`README.md`. Editing root `README.md` is a "protection violation" only if the sync itself changes it, so manual README edits are fine. |
| `publish-pypi.yml` | release/manual | `python -m build` (91), `twine check dist/*` (98) | YES only for root `README.md`: `pyproject.toml:9 readme = "README.md"` is required by the build. |
| `boundary-guard.yml` | PR touching swarm merge files (lines 26-33) | warning annotation only | No. |
| `contract3-generator-constraint-lint.yml` | PR | requires a PR-body heading when `gates.py`/`structural_checkers.py`/`*_validator.py` change (lines 39-60) | No (candidate docs are not trigger paths). |
| `.github/workflows/README.md` | n/a | docs | No. |

No CI job runs a markdown link checker over `docs/`, no job validates `PROJECT_INDEX.md/json` freshness, and no job diffs `src/` vs `plugins/` vs root `commands/`. [CODE-VERIFIED by reading every workflow's `run:` steps via grep]

### 3.3 Runtime code that reads a candidate (not hooks, not CI)

| Code | Evidence | Candidate | Effect |
|---|---|---|---|
| `src/superclaude/execution/reflection.py` | lines 320-334: `index_path = self.repo_path / "PROJECT_INDEX.md"`; if missing, `score -= 0.2` and concern "Project index missing"; if older than 7 days, concern "stale" | `PROJECT_INDEX.md` | Not a crash. Lowers the "Context Readiness" reflection score. `repo_path` is the repo being worked on (UNVERIFIED whether it ever points at IronClaude itself in practice versus a user project). Retiring IronClaude's `PROJECT_INDEX.md` only matters when IronClaude is the target repo. Note: `PROJECT_INDEX.json` is NOT read by any Python in `src/` (grep found no hit). |
| `src/superclaude/cli/recommend/prompts.py` | line 16 docstring: "see ``core/ORCHESTRATOR.md`` Tier Classification Routing" | `ORCHESTRATOR.md` | Comment only. Becomes a stale pointer if ORCHESTRATOR.md is retired or renamed. |
| `src/superclaude/cli/audit/profiler.py` | line 47 lists `"KNOWLEDGE.md"` as a docs-domain path signal | `KNOWLEDGE.md` | Classification heuristic by filename; absence of the file changes nothing. |
| `src/superclaude/cli/roadmap/structural_checkers.py` | line 300 docstring cites `KNOWLEDGE.md 2026-05-25 "Fix B Merged"` | `KNOWLEDGE.md` | Comment only; becomes a dangling citation if KNOWLEDGE.md is retired. |
| `src/superclaude/core/CLAUDE.md` (installed as `~/.claude/CLAUDE.md`) | line 93 lists `KNOWLEDGE.md`; line 100 says "use `/sc:help` to list all available" | `KNOWLEDGE.md`, `help.md` | User-facing instruction text shipped to every install. Must be updated if `/sc:help` or KNOWLEDGE.md is retired. |

---

## 4. Doc-to-doc link graph (inbound references)

Method: a throwaway read-only script (`/tmp/rf-linkgraph-04/graph.py`, run with `python3 -I`, output `/tmp/rf-linkgraph-04/out.txt`) walked every `*.md` under `/tmp/ic-master` EXCLUDING `.git`, `node_modules`, `.dev`, `__pycache__`, and recorded each line containing the candidate path or basename (relative links, absolute paths, and plain mentions all count). For the user-guide files and `help.md`/`recommend.md`, a bare basename (`./commands.md`, `help.md`) was counted only when the referring file sits in the same directory. Self-references (a file naming itself on line 1) are omitted below. `.dev/` was excluded deliberately: it is non-distributable scratch (pyproject comment at line 195), and it holds hundreds of historical mentions (for example 12 `.dev` files mention `/sc:help`). Command-name mentions (`/sc:help`, `/sc:recommend`) were collected separately with `grep -F`.

Caveat: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` are near-duplicates (same hits at nearly the same lines); both are listed.

### 4.1 Core files (`src/superclaude/core/`)

| Candidate | Inbound references (file:line) |
|---|---|
| `ORCHESTRATOR.md` | `PROJECT_INDEX.md:48`; `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:99,369,749,1028,1087,1181`; `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:99,374,754,1034,1095,1194`; `src/superclaude/skills/sc-task-protocol/SKILL.md:408` ("Routing logic: See ORCHESTRATOR.md", SHIPPED skill text); code comment `src/superclaude/cli/recommend/prompts.py:16`; test docstring `tests/sc-roadmap/compliance/test_critical_corrections.py:7,61` |
| `COMMANDS.md` | `PROJECT_INDEX.md:44`; both Developer-Guide copies at lines 99, 368/373, 749/754, 1028/1034, 1087/1095, 1181/1194 |
| `MODES.md` | `PROJECT_INDEX.md:47`; both Developer-Guide copies line 99 |
| `FLAGS.md` | `PROJECT_INDEX.md:45`; both Developer-Guide copies 99, 370/375, 1029/1035; `docs/developer-guide/contributing-code.md:64`; `docs/developer-guide/technical-architecture.md:27,133`; `docs/developer-guide/testing-debugging.md:32,72,90`; `docs/reference/comprehensive-features.md:99`; `docs/reference/diagnostic-reference.md:64` |
| `PERSONAS.md` | `PROJECT_INDEX.md:43`; both Developer-Guide copies 99, 371/376, 1029/1035; `src/superclaude/core/ORCHESTRATOR.md:305,368` (core-to-core) |

### 4.2 Command files (`src/superclaude/commands/`)

| Candidate | Inbound path references | Command-name mentions (`/sc:<name>`) outside `.dev/` |
|---|---|---|
| `help.md` | NONE by path. | `src/superclaude/core/CLAUDE.md:100` (shipped); `docs/user-guide/commands.md:98`; `docs/user-guide/modes.md:601`; `docs/reference/commands-list.md:88`; `docs/reference/suggested-commands.md:143`; self `help.md:10,41` and its plugins copy |
| `recommend.md` | `src/superclaude/commands/README.md:9` and root `commands/sc-README.md:9` (index lists "recommend.md - Command recommendations") | `docs/user-guide/commands.md:97`; `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md:93,110,268`; `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:316,461,468`; `src/superclaude/skills/sc-recommend/SKILL.md:9,13,17`; `src/superclaude/skills/sc-recommend/refs/surface-enumeration.md:94` |
| `README.md` (commands) | `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md:172` | n/a |

### 4.3 User-guide and getting-started docs

| Candidate | Inbound references (file:line) |
|---|---|
| `docs/user-guide/commands.md` | `docs/getting-started/installation.md:505`; `docs/getting-started/quick-start.md:449,481`; `docs/reference/examples-cookbook.md:179`; `docs/reference/troubleshooting.md:171`; `docs/user-guide/agents.md:1017`; `docs/user-guide/brainstorm.md:230`; `docs/user-guide/flags.md:307`; `docs/user-guide/mcp-installation.md:239`; `docs/user-guide/mcp-servers.md:340`; `docs/user-guide/modes.md:5,702,727` (10 files) |
| `docs/user-guide/agents.md` | `installation.md:514`; `quick-start.md:460`; `examples-cookbook.md:180`; `mcp-servers.md:346`; `modes.md:707` |
| `docs/user-guide/modes.md` | `installation.md:513`; `quick-start.md:459`; `agents.md:1023`; `brainstorm.md:231`; `mcp-servers.md:345` |
| `docs/user-guide/flags.md` | `docs/user-guide/modes.md:516,641,708` only |
| `docs/getting-started/quick-start.md` | `docs/getting-started/installation.md:504,548`; `docs/reference/README.md:44,262`; `docs/reference/comprehensive-features.md:192`; `docs/user-guide/agents.md:1024`; `docs/user-guide/mcp-servers.md:341`; `docs/user-guide/modes.md:701,715` |

### 4.4 `docs/reference/*` candidates

| Candidate | Inbound references (file:line) |
|---|---|
| `examples-cookbook.md` | `installation.md:515`; `quick-start.md:450,484`; `docs/reference/README.md:25`; `agents.md:1025`; `mcp-servers.md:351`; `modes.md:709,724` |
| `basic-examples.md` | `docs/reference/README.md:24,46,169,264`; `docs/reference/examples-cookbook.md` (15 lines from 9 onward) |
| `advanced-workflows.md` | `docs/reference/README.md:30,61,72,173,179,248`; `examples-cookbook.md` (15 lines from 20 onward) |
| `integration-patterns.md` | `docs/reference/README.md:31,74,175,241-244,251`; `examples-cookbook.md` (18 lines from 31 onward) |
| `advanced-patterns.md` | `docs/reference/README.md:29,59,181,249,250,266` only |
| `commands-list.md` | `docs/reference/comprehensive-features.md:7,189` only |
| `suggested-commands.md` | NONE (orphan) |
| `comprehensive-features.md` | NONE (orphan) |

Cluster note: `basic-examples`, `advanced-workflows`, `integration-patterns`, `advanced-patterns` are reachable only through `docs/reference/README.md` and `examples-cookbook.md`. Retiring the cluster together needs edits in just those two hubs plus the 6 user-guide/getting-started files that link to `examples-cookbook.md`.

### 4.5 Root files

| Candidate | Inbound references (file:line) |
|---|---|
| `README.md` (root) | Not linked by path from other docs in a way that matters (root README is the entry point). Its own outbound links: only 2 markdown links (`docs/user-guide/freshness-hooks.md` at line 40, plus one already-broken `.dev/...` link); plain mentions of `docs/guides/reflect-cli-tools-guide.md` (98), `docs/developer-guide/` (204), `docs/reference/` (205), `KNOWLEDGE.md` (202), `PROJECT_INDEX` (203). Machinery refs: `pyproject.toml:9`, `MANIFEST.in:2`, sdist include, `package.json` files, `readme-quality-check.yml`, sync PROTECTED_PATHS. |
| `KNOWLEDGE.md` | `CLAUDE.md:97,295` (repo dev CLAUDE.md); `README.md:202`; `PROJECT_INDEX.md:297`; `docs/generated/contributor-knowledge-base/repository-overview.md:93`; `docs/user-guide/commands.md:137,1673`; `src/superclaude/core/CLAUDE.md:93` (SHIPPED to users); `src/superclaude/skills/sc-post-release-protocol/refs/workstream-playbook.md:36` (SHIPPED skill ref); `src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md:23,26` (SHIPPED skill ref) |
| `PROJECT_INDEX.md` / `.json` | `README.md:203`; `docs/generated/contributor-knowledge-base/repository-overview.md:94`; `docs/user-guide/commands.md:66,771,1402,1462,1470,1478,1486,1515,1668`; `src/superclaude/commands/index-repo.md:13,72,172,173` (+ identical `plugins/superclaude/commands/index-repo.md`, root `commands/sc-index-repo.md:13,66,160,161`); `src/superclaude/agents/repo-index.md:15,28,29` (+ plugins and root `agents/sc-repo-index.md` copies); runtime `src/superclaude/execution/reflection.py:321`. The `/sc:index-repo` command and `repo-index` agent describe `PROJECT_INDEX.md/json` as the GENERIC output they write into whatever repo is being indexed, so they do not depend on IronClaude's own copy. Both IronClaude copies are stale: `PROJECT_INDEX.md:3` "Generated: 2026-03-23, Version 4.2.0"; `PROJECT_INDEX.json` `metadata.generated_at` "2025-10-29", `version` "0.4.0". They are regenerated only by running `/sc:index-repo` (an LLM command), not by any script or CI. |

### 4.6 Root `commands/sc-*.md` and `plugins/` copies

| Candidate | Inbound references |
|---|---|
| root `commands/sc-help.md`, `sc-recommend.md`, `sc-README.md` | No markdown file links to them by path. They are consumed by Claude Code plugin loading (root `.claude-plugin/plugin.json` has name `sc`, version 4.3.0, no explicit command map in the snapshot) and regenerated by `pull-sync-framework.yml` from upstream. `commands/sc-README.md:9` links to `recommend.md`. |
| `plugins/superclaude/commands/help.md`, `recommend.md` | No markdown file links to them by path. Consumed by `install_commands._get_commands_source` fallback (source checkout only, `install_commands.py:112-119`), by `scripts/build_superclaude_plugin.py:75`, and shipped in the wheel under `superclaude/_plugins` (`pyproject.toml:86-88`). |
| `plugins/superclaude/core/FLAGS.md` | No inbound path link. Not consumed by `build_superclaude_plugin.py` (core not in its folder list). Shipped in the wheel via `plugins/**`. No Python under `src/superclaude` references `_plugins` (grep: only `_src` is read, by `install_templates.py:122` and `install_user_setup.py:45`), so nothing at runtime reads `superclaude/_plugins/core/`. [CODE-VERIFIED] |

---

## 5. Decision table

Legend. "Breaks" means a test, CI job, build, install, or doctor check fails, or shipped runtime text points at nothing. "Stale-only" means only prose or comments go stale. "Safe to retire" assumes the listed must-update items are done in the same change; it says "yes" when nothing mechanical fails.

Cross-cutting rules that apply to every row:
- R1. `superclaude install`/`update` never delete. Retiring any `core/*.md` or `commands/*.md` leaves stale copies in every user's `~/.claude/` and `~/.claude/commands/sc/` (section 1.1). A retirement needs either a cleanup step in the installer or a release note.
- R2. `make sync-dev` never deletes. Retiring or renaming any `src/superclaude/commands/*.md` makes local `make verify-sync` and `tests/cli/test_verify_sync_hooks.py::test_V1_clean_tree_exits_zero` fail on developer machines until `.claude/commands/sc/<old>.md` is deleted by hand (sections 1.6, 2.1a). CI is unaffected.
- R3. Root `commands/sc-*.md` are regenerated from UPSTREAM every 6 hours by `pull-sync-framework.yml`; local deletion of `sc-help.md`, `sc-recommend.md`, or `sc-README.md` will be undone while upstream still has those commands (section 3.2).

| Candidate file | Breaks if removed (what, where) | Must update if renamed | Safe to retire? |
|---|---|---|---|
| `src/superclaude/core/ORCHESTRATOR.md` | Nothing mechanical. Shipped skill text points at nothing: `src/superclaude/skills/sc-task-protocol/SKILL.md:408` "Routing logic: See ORCHESTRATOR.md". Stale-only: `PROJECT_INDEX.md:48`, both Developer-Guide copies (6 lines each), `cli/recommend/prompts.py:16` comment, test docstring `test_critical_corrections.py:7,61`. R1 applies. | `install_core.py:148` `known_core`; `sc-task-protocol/SKILL.md:408`; the inbound list in 4.1. | YES, after fixing `sc-task-protocol/SKILL.md:408` and `known_core`. Not `@`-imported by shipped CLAUDE.md, no test reads it. |
| `src/superclaude/core/COMMANDS.md` | Nothing mechanical. Stale-only: `PROJECT_INDEX.md:44`, both Developer-Guide copies. R1 applies. | `install_core.py:144`. | YES. No test, hook, CI, or skill reads it. |
| `src/superclaude/core/MODES.md` | Nothing mechanical. Stale-only: `PROJECT_INDEX.md:47`, Developer-Guide line 99 (both copies). R1 applies. Note `src/superclaude/modes/MODE_*.md` is a separate set, not affected. | `install_core.py:147`. | YES. |
| `src/superclaude/core/FLAGS.md` | Nothing mechanical. Stale-only (most inbound of the core set, 8 files): developer-guide `contributing-code.md:64`, `technical-architecture.md:27,133`, `testing-debugging.md:32,72,90`, `docs/reference/comprehensive-features.md:99`, `diagnostic-reference.md:64`, Developer-Guide copies, `PROJECT_INDEX.md:45`. Separate drifted copy at `plugins/superclaude/core/FLAGS.md` (differs from src) is not touched by any build step. R1 applies. Any rewrite must obey the tavily guards in 2.2 only if it moves under `docs/` (FLAGS.md is under `src/superclaude`, so the stale-token and version-pin guards apply; the DEFAULT_PARAMETERS guard does not). | `install_core.py:145`; the 6 developer-guide/reference lines above. | YES, after editing the developer-guide references. Decide separately whether `plugins/superclaude/core/FLAGS.md` is retired too (it is protected from upstream sync, so it will not come back). |
| `src/superclaude/core/PERSONAS.md` | Nothing mechanical. Stale-only: `ORCHESTRATOR.md:305,368` (if ORCHESTRATOR survives), `PROJECT_INDEX.md:43`, Developer-Guide copies. Shipped `core/CLAUDE.md:62-74` already carries its own persona table, so behavior is not lost. R1 applies. | `install_core.py:149`. | YES. |
| `src/superclaude/commands/help.md` | Nothing in pytest or CI on a clean checkout. Shipped instruction `src/superclaude/core/CLAUDE.md:100` "use `/sc:help` to list all available" points at a dead command. Users lose `/sc:help` but stale `~/.claude/commands/sc/help.md` lingers (R1). R2 local verify-sync failure. Copies remain at `plugins/superclaude/commands/help.md` (also used as the source-checkout fallback and in `build-plugin`) and root `commands/sc-help.md` (R3). Mentions: `docs/user-guide/commands.md:98`, `modes.md:601`, `docs/reference/commands-list.md:88`, `suggested-commands.md:143`. | Same as removal, plus `lint-architecture` Check 3/4 size limits (warn over 200, error over 500 lines) if the replacement is a merged, larger command file. No test pins the name `help`. | YES mechanically (no test pins it), but NOT without first updating `core/CLAUDE.md:100` and deciding the fate of the `plugins/` and root copies. |
| `src/superclaude/commands/recommend.md` | FAILS `tests/unit/test_cli_install.py::test_all_expected_commands_available` (lines 134-143, `"recommend"` in expected list), which runs in both `test.yml` and `quick-check.yml` (`tests/unit/ -x`). If kept but rewritten without `> Skill sc-recommend`, the `sc-recommend` skill silently stops installing (1.9) and `tests/unit/test_cli_doctor.py:79` FAILS. If the `sc-recommend` skill is removed while `recommend.md` keeps `## Activation`, `make lint-architecture` Check 1 FAILS and `superclaude doctor` fails on machines with the stale command. Index mention `commands/README.md:9`. R1, R2, R3 apply. | `test_cli_install.py:138`; `commands/README.md:9`; `docs/user-guide/commands.md:97`; generated KB `commands-skills-cross-reference.md`, `visual-architecture-summary.md`; `plugins/superclaude/commands/recommend.md` (currently byte-identical to src). The PreToolUse gate `sc-recommend-phase0.sh:33-36` keys on the SKILL name, so renaming the skill (not the command) also requires that hook and `.claude/settings.json` description. | NO as-is. Requires a test edit (`test_cli_install.py:138`) and keeping the skill activation contract. It is a live entry point to a maintained skill with its own CLI (`superclaude recommend`), hook, and cache, so it is a keep-and-update candidate, not a retire candidate. |
| `src/superclaude/commands/README.md` | Nothing mechanical (not mirrored by sync-dev, skipped by verify-sync and lint-architecture, skipped by `list_*_commands`). But `install_commands` DOES copy it to `~/.claude/commands/sc/README.md` (1.3), where it appears as a `/sc:README` slash command; removing it removes that pseudo-command for new installs only (R1). Inbound: `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md:172`. Root `commands/sc-README.md` persists (R3). | The generated KB line 172. | YES. Arguably beneficial (it is installed as a fake command). |
| `docs/user-guide/commands.md` | Nothing mechanical (no docs link checker in pytest or CI; readme-quality-check only scans root README markdown links). 10 inbound files (4.3) get dead links. Content guards in 2.2 apply to any replacement under `docs/`. | All 10 inbound files in 4.3. | YES mechanically; needs inbound link edits in 10 files. |
| `docs/user-guide/agents.md` | Nothing mechanical. 5 inbound files. | 5 inbound files (4.3). | YES. |
| `docs/user-guide/modes.md` | Nothing mechanical. 5 inbound files. | 5 inbound files (4.3). | YES. |
| `docs/user-guide/flags.md` | Nothing mechanical. 1 inbound file (`modes.md`, 3 lines). Contains tavily prose (line 21) and Chrome DevTools (line 198); a merged replacement must not restate tavily DEFAULT_PARAMETERS (2.2). | `modes.md:516,641,708`. | YES. |
| `docs/getting-started/quick-start.md` | Nothing mechanical. 6 inbound files incl. `docs/reference/README.md:44,262` and `installation.md:504,548`. | 6 inbound files (4.3). | YES, but it is a primary onboarding entry; replace, do not just delete. |
| `docs/reference/examples-cookbook.md` | Nothing mechanical. Hub for basic-examples/advanced-workflows/integration-patterns; 6 inbound files. | 6 inbound files (4.4). | YES if its spokes are retired with it. |
| `docs/reference/basic-examples.md` | Nothing mechanical. Inbound only from `docs/reference/README.md` and `examples-cookbook.md`. | Those 2 hubs. | YES. |
| `docs/reference/advanced-workflows.md` | Nothing mechanical. Same 2 hubs. | Those 2 hubs. | YES. |
| `docs/reference/integration-patterns.md` | Nothing mechanical. Same 2 hubs. | Those 2 hubs. | YES. |
| `docs/reference/commands-list.md` | Nothing mechanical. Inbound only from `comprehensive-features.md:7,189`. | `comprehensive-features.md`. | YES. |
| `docs/reference/suggested-commands.md` | Nothing. Orphan (no inbound outside `.dev/`). | None. | YES. |
| `docs/reference/comprehensive-features.md` | Nothing. Orphan. Contains tavily commands (lines 58-73); if retained or merged, keep pointing to `MCP_Tavily.md` (2.2). | None. | YES. |
| `docs/reference/advanced-patterns.md` | Nothing mechanical. Inbound only from `docs/reference/README.md` (6 lines). | `docs/reference/README.md`. | YES. |
| `README.md` (root) | BREAKS packaging: `pyproject.toml:9 readme`, `MANIFEST.in:2`, sdist include list, `package.json` files, `publish-pypi.yml` build. Sync `PROTECTED_PATHS` and `pull-sync-framework.yml` protection list name it. `readme-quality-check.yml` scans it. | All of the above. | NO. Update in place only. Any rewrite must keep at most 5 broken `[text](path)` links (6 fails `readme-quality-check`; 1 is already broken today). |
| `KNOWLEDGE.md` (root) | Nothing mechanical (only a filename heuristic in `audit/profiler.py:47` and a comment in `roadmap/structural_checkers.py:300`). Shipped text points at nothing: `src/superclaude/core/CLAUDE.md:93` (installed to every user), `sc-troubleshoot-protocol/refs/doc-discovery.md:23,26`, `sc-post-release-protocol/refs/workstream-playbook.md:36`. Also repo `CLAUDE.md:97,295`, `README.md:202`, `docs/user-guide/commands.md:137,1673`. | The 3 shipped references above plus repo CLAUDE.md and README. | NOT a routing doc: it is the debugging-lessons log referenced by shipped skills. Retire only if its content moves and the shipped skill refs are repointed. Recommend out of scope for this consolidation. |
| `PROJECT_INDEX.md` / `PROJECT_INDEX.json` (root) | No crash. `src/superclaude/execution/reflection.py:320-334` lowers the Context Readiness score when `PROJECT_INDEX.md` is missing in the target repo. `.json` is read by nothing. Both are already stale (MD 2026-03-23 v4.2.0; JSON 2025-10-29 v0.4.0). Mentions in `README.md:203`, `docs/user-guide/commands.md` (9 lines), generated KB `repository-overview.md:94`. | `README.md:203`; `docs/user-guide/commands.md`. Command/agent references are generic and need no change. | YES for the JSON. For the MD: yes, accepting the reflection score penalty when IronClaude itself is the target repo, or regenerate it with `/sc:index-repo` instead of retiring. |
| root `commands/sc-help.md`, `sc-recommend.md`, `sc-README.md` | Nothing in this repo's tests or CI reads them. Plugin users lose the commands. | n/a (generated). | NO in practice: R3 re-creates them from upstream. Retiring requires changing `scripts/sync_from_framework.py` SYNC_MAPPINGS or upstream. Treat as generated output, not editable source. |
| `plugins/superclaude/commands/help.md`, `recommend.md` | Nothing in pytest (no equality test for these two). Used by `make build-plugin` and the source-checkout fallback in `install_commands.py:112-119` (only when the package `commands/` dir is missing, which does not happen in practice). | Keep in lockstep with src by hand; consider adding an equality test like `test_workflow_command.py:86-87`. | YES alongside the src change; mirror any src change here. `help.md` copy already differs from src. |
| `plugins/superclaude/core/FLAGS.md` | Nothing reads it (4.6). | n/a. | YES. |

---

## 6. Gaps and questions

| Item | Status |
|---|---|
| Exact `readme-quality-check.yml` outcome was simulated for the link portion only (regex replicated); the full embedded script was not executed. | Partial; arithmetic from source lines 190-197, 255. |
| Whether `reflection.py` `repo_path` ever targets IronClaude itself in normal use. | UNVERIFIED. |
| Upstream `SuperClaude-Org/SuperClaude_Framework` still has `help.md`, `recommend.md`, `README.md` under `src/superclaude/commands/` (drives R3). | UNVERIFIED; not fetched (read-only snapshot scope). |
| Whether any end user's `~/.claude/CLAUDE.md` `@`-imports ORCHESTRATOR/COMMANDS/MODES/FLAGS/PERSONAS (older SuperClaude installs did). The shipped `core/CLAUDE.md` does not. | UNVERIFIED for user machines; CODE-VERIFIED for the shipped file. |
| `.dev/` was excluded from the link graph; it holds many historical mentions that will go stale but are non-distributable. | By design. |
| `docs/developer-guide/` and `docs/guides/` both contain `SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (near duplicates), each referencing COMMANDS/ORCHESTRATOR/MODES/FLAGS/PERSONAS. | Observed; a separate dedup candidate. |
| The npm wrapper (`package.json` postinstall `node ./bin/install.js`) references a `bin/` directory that does not exist in the snapshot. | CODE-VERIFIED broken, independent of this consolidation. |

## Summary

- Only TWO candidates have hard mechanical breakage: root `README.md` (packaging and CI) and `src/superclaude/commands/recommend.md` (a pinned unit test in both CI workflows, plus the skill-install and doctor coupling). Neither should be retired.
- The five core routing files (ORCHESTRATOR, COMMANDS, MODES, FLAGS, PERSONAS) are copied by `install_core.py` but not imported by the shipped CLAUDE.md and not read by any test, hook, or CI job. Retiring them needs: the `known_core` set edit (`install_core.py:139-153`), the shipped skill pointer `sc-task-protocol/SKILL.md:408`, developer-guide prose edits, and a plan for stale `~/.claude/` copies (installer never deletes).
- `help.md` has no test or CI pin, but shipped `core/CLAUDE.md:100` advertises `/sc:help`; it also has drifted copies in `plugins/` and root `commands/`.
- All `docs/` candidates are mechanically safe (no docs link checker exists for `docs/`); the cost is inbound-link edits listed in section 4, plus obeying the tavily content guards in `tests/docs/test_tavily_doc_alignment.py`.
- Root `commands/sc-*.md` are generated from upstream every 6 hours and cannot be retired locally.
- `KNOWLEDGE.md` is referenced by shipped skills and is not a routing doc; keep it out of scope.
