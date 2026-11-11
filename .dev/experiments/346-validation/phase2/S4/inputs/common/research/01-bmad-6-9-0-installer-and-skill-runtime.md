# Research: BMAD 6.9.0 installer behaviour and skill runtime needs
**Investigation type:** Code Tracer
**Scope:** /opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/ (tools/installer/, src/scripts/, src/core-skills/, package.json); worktree .claude/skills/bmad-help/SKILL.md and _bmad/ (6.10.0 corroboration only)
**Status:** Complete
**Date:** 2026-11-07
---

## 0. Evidence rules and commands actually run

- No actual `bmad install` was run (not in the worktree, not in a scratch directory, not with a scratch HOME). There is NO observed 6.9.0 install in this task.
- Every `bmad` command run was one of the four allowed by the BMAD CLI RULE, each with `NPM_CONFIG_OFFLINE=true`:
  1. `NPM_CONFIG_OFFLINE=true bmad --version` -> `6.9.0`
  2. `NPM_CONFIG_OFFLINE=true bmad install --help`
  3. `NPM_CONFIG_OFFLINE=true bmad install --list-tools`
  4. `NPM_CONFIG_OFFLINE=true bmad install --list-options`
  (Commands 2-4 were piped through `head` in one Bash call; no other `bmad` subcommand was run.)
- Package under study: `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/`. `package.json:2-4` name `bmad-method`, version `6.9.0`; `package.json:22-25` bins `bmad` and `bmad-method` -> `tools/installer/bmad-cli.js`; `package.json:112-114` `engines.node >=20.12.0`. [CODE-VERIFIED]
- Host Node is v24.22.2 per the install path (path-derived; `node --version` not run) so it satisfies `>=20.12.0`.
- Update-check banner: `tools/installer/bmad-cli.js:20-53` runs `checkForUpdate()` on EVERY invocation (asynchronously, not awaited, at module load). It calls `execSync('npm view bmad-method@<tag> version', {timeout: 5000})` (`bmad-cli.js:31-35`) and prints an "Update Available" box if a newer version is found (`bmad-cli.js:37-49`); any error is swallowed (`bmad-cli.js:50-52`). That is why `--list-tools` and `--list-options` printed "You are using version 6.9.0 but 6.12.4 is available" even with `NPM_CONFIG_OFFLINE=true`: npm answered from its local metadata cache (OBSERVED; that npm answered from cache rather than network is an inference, UNVERIFIED). The banner is advisory only; it does not block or alter installs. [CODE-VERIFIED for the code path, OBSERVED for the banner]
- Worktree trees (`_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*`) are 6.10.0 and are used only as OBSERVED-FROM-6.10.0-TRACKED-TREE corroboration; see section 8.

## 1. CLI surface (question b, first part)

Option definitions, `tools/installer/commands/install.js:12-51` [CODE-VERIFIED]; the `bmad install --help` output (OBSERVED) matches them one for one.

| Option | Defined at | Meaning |
|---|---|---|
| `--directory <path>` | install.js:14 | Installation directory (default: current directory) |
| `--modules <modules>` | install.js:15 | Comma-separated module IDs (e.g. `bmm,bmb`) |
| `--tools <tools>` | install.js:16-19 | Comma-separated tool IDs; "Required for fresh non-interactive (--yes) installs" |
| `--list-tools` | install.js:20 | Print supported tool IDs and exit (handled `install.js:54-58`, before any install work) |
| `--set <spec>` | install.js:21-26 | `<module>.<key>=<value>`, repeatable; syntax validated up front `install.js:90-98` |
| `--list-options [module]` | install.js:27-30 | Print `--set` keys and exit (`install.js:60-76`) |
| `--action <type>` | install.js:31 | `install`, `update`, or `quick-update` for existing installs |
| `--user-name <name>` | install.js:32 | default: system username |
| `--communication-language`, `--document-output-language` | install.js:33-34 | default English |
| `--output-folder <path>` | install.js:35 | relative to project root, default `_bmad-output` |
| `--custom-source <sources>` | install.js:36 | Git URLs or local paths for custom modules |
| `-y, --yes` | install.js:37 | Accept defaults, skip prompts where possible |
| `--channel`, `--all-stable`, `--all-next`, `--next <code>`, `--pin <spec>` | install.js:38-50 | external-module version channel controls |
| `-d, --debug` | install.js:13 | debug output for manifest generation (sets `BMAD_DEBUG_MANIFEST`, install.js:82-85) |

Control flow of the action, `install.js:52-148`: list-tools / list-options exit early; `checkWindowsNodeFromWsl()` (install.js:78-79); `--set` validation; `ui.promptInstall(options)` (install.js:100) builds the config; `cancel` exits 0; `quick-update` calls `installer.quickUpdate` (install.js:112-119); otherwise `installer.install(config)` (install.js:122), exit 0 on `result.success`, exit 1 on any thrown error (install.js:133-147).

`--list-tools` (OBSERVED): `claude-code` target dir `.claude/skills`, starred as recommended. 44 tool IDs listed. Other starred entries: codex, cursor, github-copilot (all `.agents/skills`).

`--list-options` (OBSERVED): core keys `core.user_name` (user-scope), `core.project_name` (default `{directory_name}`), `core.communication_language` (user-scope), `core.document_output_language`, `core.output_folder` (default `_bmad-output`); bmm keys `bmm.user_skill_level` (user-scope), `bmm.planning_artifacts` (`{output_folder}/planning-artifacts`), `bmm.implementation_artifacts` (`{output_folder}/implementation-artifacts`), `bmm.project_knowledge` (default `docs`).

Key Takeaways:
- Host version is 6.9.0, Node requirement `>=20.12.0` (package.json:113).
- `--tools` is mandatory for a fresh `--yes` install per the help text (install.js:18); the exact enforcement code is traced in section 3.
- `bmm.project_knowledge` default is `docs`; whether the installer creates it is traced in section 4.

## 2. `global_target_dir` and HOME-touching code: whole-package Grep (question d)

Grep pattern: `global_target_dir|globalTargetDir|global_target|os\.homedir|homedir\(|~/\.claude` over the WHOLE package root, all file types, excluding only `node_modules/**`. Complete hit list:

| file:line | Hit | READER or declaration/comment? |
|---|---|---|
| `tools/installer/ide/platform-codes.yaml:9` | comment `global_target_dir: (optional) User-home directory for global install` | comment only |
| `tools/installer/ide/platform-codes.yaml:12` | comment about shared `target_dir` / `global_target_dir` | comment only |
| `tools/installer/ide/platform-codes.yaml:22-336` (41 per-platform value lines; claude-code at line 57: `global_target_dir: ~/.claude/skills`) | per-platform value | declaration only (data) |
| `tools/skill-validator.md:133` | `WRONG: ~/.claude/skills/my-skill/file.md` | documentation example only |
| `src/core-skills/bmad-customize/scripts/list_customizable_skills.py:16` | comment: "location (e.g. `~/.claude/skills/`). We do not hardcode those paths" | comment only |
| `tools/installer/modules/external-manager.js:156` | `path.join(os.homedir(), '.bmad', 'cache', 'external-modules')` | HOME reader, cache dir only |
| `tools/installer/modules/custom-module-manager.js:251` | `~` expansion with `os.homedir()` for a custom-source path | HOME reader (path expansion) |
| `tools/installer/modules/custom-module-manager.js:357` | `~/.bmad/cache/custom-modules` | HOME reader, cache dir |
| `tools/installer/project-root.js:80` | `process.env.BMAD_EXTERNAL_MODULES_CACHE || ~/.bmad/cache/external-modules` | HOME reader, cache dir, env override |
| `tools/installer/project-root.js:162` | `~/.bmad/cache/community-modules/<module>` | HOME reader, cache dir |
| `tools/installer/project-root.js:191` | `~/.bmad/cache/custom-modules` | HOME reader, cache dir |
| `tools/installer/ui.js:1578`, `ui.js:1581` | `~` expansion of a user-typed path | HOME reader (path expansion) |
| `tools/installer/prompts.js:587`, `prompts.js:589` | `~` and `~/` expansion | HOME reader (path expansion) |
| `tools/installer/core/legacy-warnings.js:73`, `:74` | `~` expansion | HOME reader (path expansion) |

Re-check with no exclusions (Grep `global_target_dir|globalTargetDir|global_target`, count mode, whole package root including `node_modules`): 43 occurrences in exactly ONE file, `tools/installer/ide/platform-codes.yaml` (2 comment lines, 9 and 12, plus 41 value lines). A second whole-package check for `os.homedir|homedir(|~/.claude` outside `tools/` returned only `src/core-skills/bmad-customize/scripts/list_customizable_skills.py` (the comment at :16).

Result: `global_target_dir` (also `globalTargetDir`, `global_target`) appears ONLY in `tools/installer/ide/platform-codes.yaml` (comment lines 9 and 12; values lines 22-336). No `.js`, `.mjs`, `.cjs`, `.json` or `.md` file under the package root reads it.

**Conclusion (CODE-VERIFIED by whole-package Grep): in 6.9.0 there is NO consumer of `global_target_dir`; it is declared data and a comment only. Option F (upstream user-scope install via `global_target_dir`) has no code path in 6.9.0.** (Section 5 re-checks `platform-codes.js` and `_config-driven.js` directly.)

HOME writes exposed by the grep are cache directories under `~/.bmad/cache/` (external-modules, custom-modules, community-modules). Whether a plain `--modules bmm --tools claude-code` install writes there is traced in section 4.

Key Takeaways:
- `global_target_dir`: declaration/comment only, zero readers in 6.9.0 (CODE-VERIFIED).
- No installer code references `~/.claude` as a write target; HOME is touched only for `~/.bmad/cache/*` and `~` path expansion.

## 3. Installer control flow and fully non-interactive flag set (question b)

All paths are under `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/`. All rows CODE-VERIFIED unless marked.

### 3.1 Call chain for a fresh install

| Step | Code | What it does |
|---|---|---|
| 1 | `bmad-cli.js:20-53` | background `npm view bmad-method@latest version` (5 s timeout, errors swallowed); update banner only |
| 2 | `commands/install.js:78-79` | `checkWindowsNodeFromWsl()` (only relevant to WSL with Windows node) |
| 3 | `ui.js:156-173` `promptInstall` | prints logo + start message, then `checkUvEnvironment()` (`core/uv-check.js:75-91`): runs `uv --version` (5 s timeout); missing `uv` is a WARNING only, install never blocks |
| 4 | `ui.js:202-210` | `--directory` is expanded (`expandUserPath`, ui.js:1568) and checked with `validateDirectorySync` (ui.js:1414-1463): a non-existent path is accepted if an existing parent is writable; an existing path must be a writable directory |
| 5 | `ui.js:217-220` | `installer.findBmadDir(dir)` then `fs.pathExists(bmadDir)`: if `_bmad/` already exists the run is an UPDATE (action menu / `--action`); if not, it is a fresh install |
| 6 | `ui.js:391-420` | modules: `--modules` list, else defaults under `--yes` (`getDefaultModules`), else a picker; `core` is always prepended (ui.js:418-420) |
| 7 | `ui.js:430`, `ui.js:617-643` | `promptToolSelection`: `--tools` parsed and validated by `_parseToolsFlag` (ui.js:472-501); under `--yes` with no `--tools` and no configured tools it throws `--tools is required for non-interactive install (--yes / -y) when no tools are previously configured` (ui.js:630-641) |
| 8 | `ui.js:431-434`, `ui.js:775-870` `collectModuleConfigs` | seeds `core` config from `--user-name`, `--communication-language`, `--document-output-language`, `--output-folder` (ui.js:807-824); under `--yes` with none of those flags it seeds defaults: user_name = capitalised OS username, project_name = `path.basename(directory)`, English, `_bmad-output` (ui.js:838-861) |
| 9 | `ui.js:865-867` -> `official-modules.js:1023-1143` `collectAllConfigurations` | `skipPrompts` true under `--yes`: bmm uses defaults without prompting (official-modules.js:1051, 1518-1526). Without `--yes` the "Express Setup / Customize" select (official-modules.js:1056-1063) and core prompts (official-modules.js:1043-1046, 1530-1531) appear, so a run without `--yes` is NOT non-interactive even when `--modules`/`--tools` are given |
| 10 | `core/installer.js:37-44` `install` | `Config.build`, `InstallPaths.create`, `OfficialModules.build`, `ExistingInstall.detect` |
| 11 | `core/installer.js:86-95` `_installAndConfigure` | tasks: shared scripts -> modules -> "Creating module directories" -> config/manifests/help catalog (section 4) |
| 12 | `core/installer.js:97` `_setupIdes` | per selected tool, writes skills into the tool's `target_dir` under the project (section 5) |
| 13 | `core/installer.js:101` `_cleanupSkillDirs` | removes redundant skill copies from `_bmad/` after the IDE step |
| 14 | `commands/install.js:130-131` | exit 0 on `result.success`; any thrown error exit 1 (`install.js:133-147`) |

### 3.2 Flag combination for a fully non-interactive, claude-code-only install

From the code, the minimum is:

`bmad install --directory <dir> --modules bmm --tools claude-code --yes`

Evidence: `--yes` is what sets `skipPrompts` for core and bmm config collection (ui.js:838-867, official-modules.js:1518-1526) and skips the channel gate (ui.js:1770); `--tools claude-code` avoids the fatal error at ui.js:630-641 and the interactive picker (ui.js:646-); `--modules bmm` avoids the module picker (ui.js:391-397); `--directory` avoids `getConfirmedDirectory()` (ui.js:211-213, prompt default `process.cwd()` at ui.js:1329-1330). Optional extras that stay non-interactive: `--user-name`, `--communication-language`, `--document-output-language`, `--output-folder` (ui.js:807-824), `--set <module>.<key>=<value>` (post-install TOML patch, installer.js:330-337), `--action` only matters when `_bmad/` already exists (ui.js:245-251).

Notes:
- `--modules bmm` is optional under `--yes`: `getDefaultModules` (`ui.js:1287-1317`) returns built-ins with `default_selected` (bmm has `default_selected: true`, `src/bmm-skills/module.yaml:4`) plus registry externals marked `defaultSelected`, and falls back to `bmm` if the list is empty. Whether the bundled registry `bmad-modules.yaml` marks any external module as default (which would make a bare `--yes` install clone it over the network) was not read, so passing `--modules bmm` explicitly is the safe form (UNVERIFIED for the bare-`--yes` default list).
- The install is never silent: it prints a logo, the uv check, and a summary (installer.js:106-113). Output goes to stdout/stderr; there is no `--quiet` option in `install.js:12-51`.
- Passing `--tools` alone without `--yes` still leaves interactive prompts (core prompts, Express/Customize select), see step 9.
- On a directory where `_bmad/` already exists and `--yes` is used, the action defaults to `quick-update` (ui.js:252-262), which calls `installer.quickUpdate` (install.js:112-119); a different code path from a fresh install.

### 3.2a Partial-seed branch: which core keys land when `--user-name` and `--output-folder` are passed (added in fix cycle 1, finding 7)

The shipped command at `catalogue/bmad/install.sh:42` passes `--yes --directory <D> --modules bmm --tools claude-code --output-folder _bmad-output --user-name <NAME>`. It does NOT take the bare-`--yes` default seeding traced in 3.1 step 8 (`ui.js:838-861`). All rows [CODE-VERIFIED] by Read in fix cycle 1; never executed.

| Step | Code | Effect for the install.sh:42 flag set |
|---|---|---|
| 1 | `ui.js:807` | The first branch is taken because `options.userName` and `options.outputFolder` are set. The `else if (options.yes)` default branch at `ui.js:838` is an `else if` of that condition, so it is NOT reached |
| 2 | `ui.js:808-824` | `coreConfig` holds exactly two keys: `user_name` and `output_folder`. `communication_language` and `document_output_language` are only added when their flags are passed (the shipped command does not pass them); `project_name` has no CLI flag at all (`install.js:32-35`) |
| 3 | `ui.js:826-829` | `collectedConfig.core = { ...existingConfig, ...coreConfig }`; on a never-installed directory `existingConfig` is empty |
| 4 | `ui.js:832-837` | The guard `!options.yes && (...)` is false under `--yes`, so `collectModuleConfig('core', ...)` is NOT called and no core default is filled in |
| 5 | `ui.js:865-867` -> `official-modules.js:1029-1032` | `coreAlreadyCollected` is true, so `core` is filtered out of `allModules`; core is treated as collected and never defaulted |
| 6 | `installer.js:949-1037` `generateModuleConfigs` | `_bmad/core/config.yaml` is the two keys; `_bmad/bmm/config.yaml` is the bmm answers plus the same two core keys spread in (`installer.js:983-989`) |
| 7 | `manifest-generator.js:468-545` `writeCentralConfig`; scopes from `src/core-skills/module.yaml:8-10, 19-23` | `_bmad/config.toml` `[core]` gets `output_folder` (team scope); `_bmad/config.user.toml` `[core]` gets `user_name` (scope user). `project_name`, `communication_language` and `document_output_language` are written nowhere |

Consequence: in this mode `project_name`, `communication_language` and `document_output_language` never reach `_bmad/core/config.yaml`, `_bmad/bmm/config.yaml` or the central TOML, while skills read them (for example `bmad-dev-story/SKILL.md:50-53` loads all four of `project_name`, `user_name`, `communication_language`, `document_output_language` from `bmm/config.yaml` and states no fallback for a missing key; `bmad-prd/SKILL.md:20` says "Missing keys -> neutral defaults; never block"). How the model behaves when the keys are absent is UNVERIFIED (not run). Section 3.2 calls the extras "non-interactive" and 8.1 calls the command "valid"; both are true of the flags but silent on this consequence.

Facts the plan needs (decisions are the plan's, not made here):
- `--output-folder _bmad-output` must stay in every first-use command: without it, and with `--user-name` set, `output_folder` is never seeded and `official-modules.js:1387-1409` (`return configValue || match`) can leave an unresolved `{output_folder}` text (mechanism CODE-VERIFIED, outcome UNVERIFIED; see 05 fix cycle 1, finding 8).
- Keeping or dropping `--user-name` changes which branch runs: any one of `--user-name`, `--communication-language`, `--document-output-language`, `--output-folder` selects the partial-seed branch (`ui.js:807`); only a command with none of them (bare `--yes`) takes the default branch that seeds all five core keys (`ui.js:851-859`: capitalised OS username, `path.basename(directory)`, English, English, `_bmad-output`).
- `project_name` can only be set non-defaulted through `--set core.project_name=<value>` (`--set` is a post-install TOML patch, `installer.js:329-337`); which file(s) that patch updates was not traced: UNVERIFIED.

### 3.3 Offline behaviour and duration (question c)

- Built-in modules `core` and `bmm` are resolved from the installed package: `official-modules.js:212-226` returns `src/core-skills` / `src/bmm-skills`; `manifest.js:283-291` marks them `source: 'built-in'` with no npm/repo lookup. So a `--modules bmm` install does NOT need a network clone. [CODE-VERIFIED]
- Network is used only for: the background update check (`bmad-cli.js:31`, errors swallowed), external/custom modules (`external-manager.js:373-378` `git clone --depth 1`; `custom-module-manager.js:472-477`), `npm install` inside cloned external modules (`external-manager.js:415`, `:441`), and `fetchNpmVersion` for non-built-in modules (`manifest.js:361`). Direct HTTP call sites under `tools/installer/`, by Grep for `https.get|fetch(|node:https|node:http`: `modules/channel-resolver.js:58` (GitHub tag lookups for external modules) and `core/manifest.js:369` (npm registry fallback in `fetchNpmVersion`, reached only for non-built-in modules); `modules/version-resolver.js` has no network or subprocess calls (Grep: no matches). None of those is on the fresh `--yes --modules bmm` path: `manifest.js:283-291` short-circuits core/bmm, and the channel gate and update-channel resolution are skipped under `--yes` / not reached on a fresh install (`ui.js:1770`, `ui.js:342-347` is inside the existing-install branch). [CODE-VERIFIED by Grep; the one network touch on this path is the best-effort `npm view` at `bmad-cli.js:31`; never observed by a run]
- Node requirement `>=20.12.0` (`package.json:113`); host node is v24.22.2 (OBSERVED via `node --version`). `uv` is NOT required to install: it is only probed, warn-don't-block (`uv-check.js:75-91`).
- Duration of a real install: UNVERIFIED. No install was run (BMAD CLI RULE), and no timing data exists in the package. The code does synchronous file copying of the core and bmm skill trees plus the IDE step, plus a possible up-to-5 s wait for the `uv --version` probe (`uv-check.js:37-41`) and a background `npm view` capped at 5 s (`bmad-cli.js:31-35`); the process can only exit after those complete or time out.

### 3.4 Git (question g)

- Whole-installer Grep for `execSync|spawnSync|execFile|child_process|simple-git|git (init|add|commit|config|status)|.git` shows git invoked ONLY inside module cache clones (`external-manager.js:330-391`, `custom-module-manager.js:412-502`) and `npm view`/`npm install`; there is NO git call against the target project directory. `installer.js:869` only skips a `.git` entry while scanning `_bmad/` for custom files; `file-ops.js:129` lists `.git` as an ignored pattern.
- So the installer does not require the target directory to be a git repository, does not run `git init`, does not stage or commit anything, and does not edit the project `.gitignore` (the only gitignore it writes is `_bmad/custom/.gitignore` containing `*.user.toml`, `installer.js:680-684`). [CODE-VERIFIED by reading; not observed]
- Behaviour on a non-git directory when a SKILL later runs is separate (`resolve_customization.py` `find_project_root` falls back on `_bmad` OR `.git`, see section 7). The first real run on a directory without `.git` is UNVERIFIED (no install executed).

Key Takeaways:
- Non-interactive claude-code-only install: `bmad install --directory <dir> --modules bmm --tools claude-code --yes` (CODE-VERIFIED from ui.js; never executed here).
- `--yes` is required to suppress prompts; `--tools` alone is not enough.
- No network is needed for `--modules bmm` per the code read; the install still spawns `uv --version` and `npm view` with 5 s caps.
- The installer never touches the project's git state.

## 4. What a fresh 6.9.0 install writes inside the project (question a)

Source of "what is created": the installer code below. Every row is CODE-VERIFIED unless marked UNVERIFIED. Paths are relative to the install directory (`config.directory`).

| Created path | Created by (file:line) | Notes |
|---|---|---|
| `_bmad/` | `core/install-paths.js:18, 26-34` (`ensureWritableDir`, `fs.ensureDir` at :114) | `BMAD_FOLDER_NAME` imported from `ide/shared/path-utils` (install-paths.js:4); `ide/shared/path-utils.js:21` `const BMAD_FOLDER_NAME = '_bmad';` |
| `_bmad/_config/` | `install-paths.js:21, 26-34`; `manifest-generator.js:42-43` | holds manifests |
| `_bmad/core/` | `install-paths.js:22, 26-34`; module copy `official-modules.js:268, 280` | core module files from `src/core-skills` |
| `_bmad/scripts/` | `install-paths.js:23, 26-34`; `installer.js:664-678` | copies `src/scripts/` (resolve_config.py, resolve_customization.py, memlog.py) minus `tests`, `__pycache__`, `.pytest_cache`, `*.pyc` (installer.js:673-677) |
| `_bmad/custom/` | `install-paths.js:24, 26-34`; `manifest-generator.js:626-628` | |
| `_bmad/custom/.gitignore` (`*.user.toml`) | `installer.js:680-684` | only if not present |
| `_bmad/custom/config.toml`, `_bmad/custom/config.user.toml` | `manifest-generator.js:626-658` | empty stubs with comment headers, written only if absent |
| `_bmad/bmm/` | `official-modules.js:268, 280` `install()` -> `copyModuleWithFiltering` (:478-534) | skips `module.yaml`, root `config.yaml`, `sub-modules/`, `*-sidecar` dirs |
| `_bmad/core/config.yaml`, `_bmad/bmm/config.yaml` | `installer.js:949-1037` `generateModuleConfigs` | header says "Generated by BMAD installer", version and date |
| `_bmad/config.toml`, `_bmad/config.user.toml` | `install-paths.js:57-62`; `manifest-generator.js:428-618` `writeCentralConfig` | central config (team and user) |
| `_bmad/_config/manifest.yaml` | `manifest-generator.js:299-394` | `installation.version` = package version, `installDate`, modules, ides |
| `_bmad/_config/skill-manifest.csv` | `manifest-generator.js:400-418` | |
| `_bmad/_config/files-manifest.csv` | `manifest-generator.js:681-739` | sha256 hashes of installed files |
| `_bmad/_config/bmad-help.csv` | `installer.js:1046-1150` `mergeModuleHelpCatalogs`; path `install-paths.js:66-68` | merged from `src/*/module-help.csv` |
| `_bmad-output/planning-artifacts/` | `official-modules.js:548-707` `createModuleDirectories`, driven by `src/bmm-skills/module.yaml:44-47` `directories` and defaults `module.yaml:28-36` | `fs.ensureDir` at official-modules.js:691 is recursive, so `_bmad-output/` is created as the parent. `src/core-skills/module.yaml` has NO `directories` key (module.yaml:1-33), so `_bmad-output/` itself is never created as a standalone entry |
| `_bmad-output/implementation-artifacts/` | same | same |
| `docs/` (default `project_knowledge`) | same; `src/bmm-skills/module.yaml:38-41, 47` | created only if absent (official-modules.js:688-692); `--set bmm.project_knowledge=<path>` changes it (list-options OBSERVED) |
| `.claude/skills/bmad-*/` (all installed skills) | IDE step `installer.js:97, 372-397` -> `ide/_config-driven.js` (section 5) | target dir `.claude/skills` for `claude-code` (list-tools OBSERVED) |

The creation of `_bmad-output/planning-artifacts` relies on the config value substitution `{output_folder}/planning-artifacts` -> `_bmad-output/planning-artifacts` and the `{project-root}/` prefix strip (`official-modules.js:604-611`, `processResultTemplate` :1362-1415). That substitution was traced by reading, not observed.

Things the installer does NOT create (code-verified by absence in the files read): `.git`, any project `.gitignore` edit, `CLAUDE.md`, `.claude/settings*.json`, `.claude/commands/`, anything under `~/.claude`. [CODE-VERIFIED for `.git`/`.gitignore`; absence of `.claude/settings.json` writes: see section 5]

Written under HOME (question a, second half; the follow-up trace at the end of this paragraph resolves it): the only HOME-relative writes in installer code are cache directories `~/.bmad/cache/external-modules` (`external-manager.js:156`, `project-root.js:80`, env override `BMAD_EXTERNAL_MODULES_CACHE`), `~/.bmad/cache/custom-modules` (`custom-module-manager.js:357`, `project-root.js:191`) and `~/.bmad/cache/community-modules/<module>` (`project-root.js:162`). Those are reached only when an external, community or custom module is selected. For `--modules bmm` (a built-in) the code paths for built-in modules (`official-modules.js:212-226`, `manifest.js:283-291`) do not use those caches, so a bmm-only install is expected not to write under HOME. Follow-up trace of every HOME reference under `tools/installer/` (Grep for `os.homedir`, `process.env.HOME|USERPROFILE|XDG*`, `.bmad`, `tmpdir`): the only `ensureDir` of a `~/.bmad/cache/...` path are `external-manager.js:184` (inside `cloneExternalModule`, external official modules only) and `custom-module-manager.js:383` (`ensureDir(path.dirname(repoCacheDir))` when cloning a URL custom source). `project-root.js:80`, `:162`, `:191` and `list-options.js:80` only test existence (`fs.pathExists`) and never create; and for `core`/`bmm` `resolveInstalledModuleYaml` returns at `project-root.js:103-104` (`getModulePath` -> `src/core-skills`, `src/bmm-skills`, `project-root.js:64-72`) before any cache lookup. `ExternalModuleManager.listAvailable()` (`ui.js:122-125`, `ui.js:1746-1754`) reads the bundled registry file `bmad-modules.yaml` (`external-manager.js:49, 80-94, 125-139`), no network and no HOME write. Therefore, by code reading, a `--modules bmm --tools claude-code` install has NO installer-code write under HOME. [CODE-VERIFIED by exhaustive Grep; not observed.] Residual, UNVERIFIED: side effects of subprocesses the installer starts (`npm view` at `bmad-cli.js:31` may write npm's own metadata cache under `~/.npm`; `uv --version` at `uv-check.js:37`), which are npm/uv behaviour, not BMAD code.

Key Takeaways:
- A fresh bmm install writes `_bmad/` (config, scripts, core, bmm, custom), `_bmad-output/{planning,implementation}-artifacts/`, `docs/`, and the skills under `.claude/skills/bmad-*`, all inside the install directory.
- The directory creation is declarative: `src/bmm-skills/module.yaml:44-47` `directories`.
- `_bmad-output/` appears only as the parent of the two artifact directories.
- Nothing is written to `~/.claude`. Installer-code HOME writes are limited to `~/.bmad/cache` for external/custom modules and are not on the bmm-only path (CODE-VERIFIED by Grep; never observed by a run).

## 5. The IDE (tool) step: where skills land, and why `global_target_dir` is inert (questions a, d)

All under `tools/installer/ide/`. CODE-VERIFIED by reading.

| Item | Evidence |
|---|---|
| Handlers are built only from `platform-codes.yaml` entries that have an `installer` block | `manager.js:53-69` |
| For `claude-code` the entry is `target_dir: .claude/skills`, `global_target_dir: ~/.claude/skills`, `preferred: true`; no `commands_target_dir`, no `suspended`, no `ancestor_conflict_check` | `platform-codes.yaml:52-57`; Grep of `commands_target_dir` shows it only for github-copilot (:142) and opencode (:254) |
| Skill write path is `path.join(projectDir, target_dir)`, always project-relative | `_config-driven.js:245-248` `installToTarget` (`const targetPath = path.join(projectDir, target_dir); await fs.ensureDir(targetPath);`) |
| Only `target_dir` is read from `installerConfig`; `global_target_dir` is never read in `_config-driven.js`, `manager.js`, `platform-codes.js` | whole-package Grep, section 2; `platform-codes.js:38-50` only formats `target_dir` for `--list-tools` |
| Each skill is the verbatim directory copy of the source skill folder named in `skill-manifest.csv` into `<target_dir>/<canonicalId>/`; dotfiles (except `.gitkeep`), `.DS_Store`, `~`/`.swp`/`.swo`/`.bak` are filtered | `_config-driven.js:417-468` `installVerbatimSkills` (filter at :454-461) |
| Before copying, the old `<canonicalId>` dir is removed | `_config-driven.js:445-448` |
| Cleanup of old BMAD skills removes only entries in the previously-installed set or `removals.txt`; `bmad-os-*` entries are always preserved; non-BMAD skills in `.claude/skills/` are not touched on a fresh install | `_config-driven.js:499-516, 786-803` |
| After the IDE step the skill source copies under `_bmad/<module>/...` are deleted (empty parents pruned) so `_bmad/` keeps only module-level files | `installer.js:101, 406-449` |
| For tools sharing a target_dir (e.g. `.agents/skills`) the first tool writes and peers skip | `manager.js:195-234` |

What this means for a claude-code-only install: it writes ONLY `.claude/skills/<skill>/` under the project. It writes no `.claude/settings.json`, no `.claude/commands`, no `CLAUDE.md`, nothing under `~/.claude`. [CODE-VERIFIED for the files read; the full list of skill names that land is derived from `skill-manifest.csv` at install time and was not enumerated from source here, see section 8 for the 6.10.0 tree]

**Option F conclusion:** a user-scope (`~/.claude/skills`) install would need code that reads `global_target_dir` and an option to select it. Neither exists in 6.9.0 (section 2 grep; `install.js:12-51` has no `--global`/`--user` flag). [CODE-VERIFIED] So option F is not available in 6.9.0; it would be an upstream feature request. Whether a LATER upstream release (the update banner reports 6.12.4) added a consumer is UNVERIFIED here (not read, no network research done for this file's scope).

Key Takeaways:
- claude-code install = project-local `.claude/skills/bmad-*` copies only.
- `global_target_dir` is metadata for a future feature; 6.9.0 never writes there.
- Existing non-BMAD skills in `.claude/skills/` are left alone.

## 6. Ancestor conflict check (question e) and what it means for option E

Code: `_config-driven.js:189-207` (`setup`) calls `findAncestorConflict` (`_config-driven.js:943-969`) ONLY when `this.installerConfig?.ancestor_conflict_check` is truthy (`_config-driven.js:191`).

`findAncestorConflict` behaviour when it does run [CODE-VERIFIED]: resolves the project dir with `fs.realpath`, starts at its PARENT (`path.dirname`, :948), walks up until the filesystem root (:951, loop stops before the root itself), and for each ancestor checks `<ancestor>/<target_dir>` (:952); if that directory exists, lists it, loads `canonicalIds` from `<ancestor>/_bmad/_config/skill-manifest.csv` (via `_findBmadDir` :579-582 and `installed-skills.js:14-32`), and if any entry is BMAD-owned (`installed-skills.js:43-48`: canonical id in the manifest, else any name starting with `bmad`, except `bmad-os-*`) it returns the conflicting path; `setup` then logs an error telling the user to `rm -rf "<conflict>"/bmad*` and returns `success:false, reason:'ancestor-conflict'` (:194-205). HOME (e.g. `/home/coder`) would be walked, since only the filesystem root is excluded.

BUT: **no platform in 6.9.0 sets `ancestor_conflict_check`.** Whole-package Grep for `ancestor_conflict_check` returns exactly two hits: the reader at `_config-driven.js:191` and a header comment at `platform-codes.yaml:10`; no platform entry carries the key (including `claude-code`, `platform-codes.yaml:52-57`). Therefore in 6.9.0 the check never runs for any tool, claude-code included. [CODE-VERIFIED]

Implications for option E (`bmad install --directory ~`, a home-level install):
1. The installer would not block it, and it would not block a later per-project install either (the ancestor check is inert), so the "ancestor already holds BMAD" failure the owner was worried about does NOT occur in 6.9.0.
2. A home install writes `~/_bmad/`, `~/_bmad-output/{planning,implementation}-artifacts/`, `~/docs/` and `~/.claude/skills/bmad-*` (section 4, with `--directory ~`; `ui.js:204` expands `~` via `expandUserPath` ui.js:1568-1581). So `~/.claude/skills/bmad-*` would make the skills visible in every project (that Claude Code reads user-level skills from `~/.claude/skills` is a Claude Code behaviour NOT read from this package; the worktree already contains project-level `.claude/skills/bmad-*`; UNVERIFIED here).
3. It does NOT give per-project directories: skills resolve their project root by walking up to the first `_bmad` or `.git` (section 7). In a project that has `.git` but no `_bmad`, the walk stops at the project and does not reach `~/_bmad`. So option E leaves `_bmad/` absent in the project and defeats first-use creation; the outputs (`_bmad-output`, `docs`) would land under HOME if a skill resolved to `~`. This is derived from the script code; it has not been run (UNVERIFIED by execution, CODE-VERIFIED by reading, see section 7).
4. It contradicts the stated constraint "without a global BMAD install". 

Key Takeaways:
- The ancestor conflict check exists but is dead configuration in 6.9.0 (no platform enables it).
- If it were enabled, an install at HOME would make every project-level install fail for that tool.
- Option E conflicts with the per-project `_bmad` discovery in the runtime scripts and with the owner's "no global install" constraint.

## 7. What an installed skill needs at run time (question f)

Scripts and skills under `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/src/`. All CODE-VERIFIED by reading unless marked.

### 7.1 `src/scripts/resolve_config.py` (179 lines)

| Aspect | Evidence |
|---|---|
| Needs `--project-root` (required argparse option); documented as "Absolute path to the project root (contains _bmad/)" | `resolve_config.py:143-146` |
| Does NOT walk up. It resolves the given path and looks only at `<root>/_bmad/` | `resolve_config.py:153-154` |
| Four layers merged: `_bmad/config.toml` (REQUIRED), `_bmad/config.user.toml`, `_bmad/custom/config.toml`, `_bmad/custom/config.user.toml` (all optional) | `resolve_config.py:156-163` |
| When `_bmad/config.toml` is absent: stderr `error: required config file not found: <project_root>/_bmad/config.toml`, exit code 1 | `resolve_config.py:48-51`, call at :156 |
| When Python is older than 3.11 (no `tomllib`): stderr `error: Python 3.11+ is required (stdlib \`tomllib\` not found).`, exit 3 | `resolve_config.py:34-40` |
| Stdlib only, no third-party deps | `resolve_config.py:13` docstring, imports :29-35 |

### 7.2 `src/scripts/resolve_customization.py` (241 lines)

| Aspect | Evidence |
|---|---|
| Needs `--skill <abs path to skill dir>`; the skill dir must contain `customize.toml` (REQUIRED, exit 1 `error: required customization file not found: ...` if missing) | `resolve_customization.py:195-209`, :69-74 |
| `find_project_root(start)`: walks UP from `start` to the first directory that has `_bmad` OR `.git`; returns `None` at the filesystem root | `resolve_customization.py:58-66` |
| Project root is looked up from the SKILL's own directory first, only then from the cwd: `find_project_root(skill_dir) or find_project_root(Path.cwd())`. The comment says using cwd first "is unsafe when an ancestor of cwd happens to have a stray _bmad/ from another project" | `resolve_customization.py:211-215` |
| If a project root is found, team and user overrides are read from `<root>/_bmad/custom/<skill-name>.toml` / `.user.toml`; both optional (`load_toml(required=False)` returns `{}` when absent) | `resolve_customization.py:217-222`, :70-74 |
| When `_bmad/` is absent entirely: NO error. The script prints only the skill's own `customize.toml` defaults | derived from `resolve_customization.py:209-236`; not executed (UNVERIFIED by run) |
| Same Python 3.11+ check, exit 3 | `resolve_customization.py:43-51` |

So, when `_bmad/` is missing: `resolve_config.py` hard-fails (exit 1, message above); `resolve_customization.py` silently degrades to skill defaults. If the SKILL itself is installed under `~/.claude/skills/...`, `find_project_root(skill_dir)` starts from that path; on this host `/home/coder` is not a git repository (OBSERVED: `git -C $HOME rev-parse` -> `fatal: not a git repository`) and `~/_bmad` does not exist (OBSERVED: `ls` -> No such file), so for a user-level skill the first lookup returns `None` and the script falls back to the cwd walk. That is the case for option B/D only if the HOME conditions stay true.

### 7.3 `src/scripts/memlog.py`

`memlog.py init` creates its workspace parents: `path.parent.mkdir(parents=True, exist_ok=True)` (`memlog.py:150`) and refuses to overwrite (`memlog.py:147`, "errors if it exists", usage text :62). So the memlog call itself would create `_bmad-output/...` run folders, but only if `_bmad/scripts/memlog.py` exists to be run. [CODE-VERIFIED for mkdir; chain not executed]

### 7.4 How the 6.9.0 SKILL.md files use them

| Observation | Evidence (counts from Grep over `src/**/SKILL.md`) |
|---|---|
| 46 SKILL.md files in `src/core-skills` (13) and `src/bmm-skills` (33), counted from Glob | Glob `src/{core-skills,bmm-skills}/**/SKILL.md` |
| 39 of 46 SKILL.md files reference `resolve_config.py`/`resolve_customization.py` (52 matches). Corrected in fix cycle 1 (finding 6): the earlier "40 files, 92 occurrences" did not reproduce. Method: Grep pattern `resolve_config\|resolve_customization`, path `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/src`, glob `**/SKILL.md`; count mode gives "52 total occurrences across 39 files" and `-o` content mode lists 52 matches. [CODE-VERIFIED, re-run in fix cycle 1] | Grep `resolve_config|resolve_customization` count output |
| 37 SKILL.md files load `{project-root}/_bmad/bmm/config.yaml` or `{project-root}/_bmad/core/config.yaml` | Grep `_bmad/(bmm|core)/config\.yaml` count output |
| Skills invoke the scripts as `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow` (e.g. `bmad-quick-dev/SKILL.md:45`, `bmad-dev-story/SKILL.md:30`, `bmad-agent-dev/SKILL.md:23`) or `uv run {project-root}/_bmad/scripts/...` (e.g. `bmad-prd/SKILL.md:18`, `bmad-spec/SKILL.md:21`, `bmad-brainstorming/SKILL.md:21`, `bmad-forge-idea/SKILL.md:25`) | Grep output |
| The script path is anchored on `{project-root}/_bmad/scripts/`, so a project without `_bmad/` has no script to run | same lines |
| Fallback on script failure: the agent is told to read `{skill-root}/customize.toml` (+ the optional `_bmad/custom/*.toml` files) itself (`bmad-quick-dev/SKILL.md:47-53`, `bmad-dev-story/SKILL.md:32-38`, `bmad-agent-dev/SKILL.md:25-31`, `bmad-prd/SKILL.md:18`) | read directly |
| Config load: `Load config from {project-root}/_bmad/bmm/config.yaml` (`bmad-quick-dev/SKILL.md:65`, `bmad-dev-story/SKILL.md:50`, `bmad-agent-dev/SKILL.md:49`) with no stated fallback for a missing file in those three; `bmad-prd/SKILL.md:20` and `bmad-forge-idea/SKILL.md:27` say "Missing keys -> neutral defaults; never block" | read directly |
| `{project-root}` is defined as "the project working directory" | `bmad-quick-dev/SKILL.md:38`, `bmad-agent-dev/SKILL.md:16` |
| Other `_bmad` dependents: `{project-root}/_bmad/scripts/memlog.py` (`bmad-prd/SKILL.md:30`, `bmad-architecture/SKILL.md:39`, `bmad-forge-idea/SKILL.md:41`), `{project-root}/_bmad/_config/bmad-help.csv` (`bmad-help/SKILL.md:25`) | read directly |
| NO skill under `src/` tells the user to run `bmad install` or detects a missing `_bmad/`. Grep for `bmad install|npx bmad|bmad-method install|run the installer|not been installed|is not installed` over all of `src/` returns ONE hit, `src/core-skills/module.yaml:6` (a config subheader, not an instruction) | Grep output |

Consequence for first use in a project that never had BMAD: there is no built-in bootstrap. Skills that are copied into `.claude/skills/bmad-*` but find no `_bmad/` would (a) fail the script step (python's own "No such file" error from the interpreter; message text not produced by BMAD code and not observed, UNVERIFIED), (b) fall back to `customize.toml` defaults for the customization step where the SKILL.md says so, (c) have no `config.yaml` to read (`user_name`, `planning_artifacts` and so on), and (d) have no `bmad-help.csv`. Whether the model behaves sensibly in that state was not tested (UNVERIFIED).

### 7.5 Interpreter and tooling needs at skill run time

- Python 3.11+ is required by both scripts (`tomllib`), with an exit-3 message when older (7.1, 7.2).
- Host evidence: `uv 0.11.8` on PATH; `uv python list --only-installed` shows `cpython-3.13.5` at `/usr/bin/python3` (-> python3.13) and `cpython-3.11.15` under `~/.local/share/uv/python/` (OBSERVED in this session). So the host meets 3.11+.
- Interaction observed in THIS session: a Bash call that ran bare `python3 --version` was refused by the user's hook `~/.claude/hooks/block-bare-python.sh` with "UV-ONLY BLOCK: this command runs bare `python3`". The 6.9.0 bmm skills instruct `python3 {project-root}/_bmad/scripts/resolve_customization.py ...` (section 7.4). Whether that hook exists inside a Coder workspace user's Claude Code environment is UNVERIFIED; if it does, those skill steps would be blocked and the SKILL.md fallback (read `customize.toml` directly) would apply. The 6.10.0 `bmad-help` in the worktree uses `uv run --python 3.11 ...` instead (`.claude/skills/bmad-help/SKILL.md:26`), a version difference.

Key Takeaways:
- Skills require a project-local `_bmad/` (scripts, config.yaml files, config.toml, bmad-help.csv); nothing in 6.9.0 creates it lazily.
- `resolve_config.py` exits 1 with `error: required config file not found: <root>/_bmad/config.toml` when `_bmad/` is missing; `resolve_customization.py` degrades silently.
- No skill detects a missing `_bmad/` or tells the user to install; any first-use bootstrap has to come from outside BMAD.
- Python 3.11+ is required; the host satisfies this.

## 8. Version-mismatched corroboration: the worktree's tracked 6.10.0 tree (OBSERVED-FROM-6.10.0-TRACKED-TREE)

Nothing in this section is evidence of what 6.9.0 creates. The worktree `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global` trees were NOT produced by the 6.9.0 installer.

| Fact | Evidence | Tag |
|---|---|---|
| `_bmad/_config/manifest.yaml` records `installation.version: 6.10.0`, `installDate: 2026-04-18T01:46:26.996Z`, `lastUpdated: 2026-07-06T21:40:07.122Z`; modules `core` and `bmm` both `6.10.0`, `source: built-in`; `ides: claude-code, openhands` | Read of `_bmad/_config/manifest.yaml:1-22` | OBSERVED-FROM-6.10.0-TRACKED-TREE |
| The trees are tracked in git: `git ls-files _bmad` = 17 files; `_bmad-output` = 577 tracked files; `.claude/skills/bmad-*` = 237 tracked files across 47 `bmad-*` directories | `git -C <worktree> ls-files ...` | OBSERVED-FROM-6.10.0-TRACKED-TREE |
| History of the manifest: `d17093b0` 2026-04-20 "Install BMad framework...", `152db60e` 2026-05-16 "upgrade BMad framework and add Rigorflow agents", `ed4760eb` 2026-05-26 "sync bmad-* skills + config from _bmad/ source-of-truth", `66133ef2` 2026-07-08 "isolate skill refresh work" (a tracked tree upgraded over time, plus project documents) | `git log -- _bmad/_config/manifest.yaml` | OBSERVED-FROM-6.10.0-TRACKED-TREE |
| Tracked `_bmad` files: `_config/{agent-manifest.csv, bmad-help.csv, files-manifest.csv, manifest.yaml, skill-manifest.csv}`, `bmm/{config.yaml, module-help.csv}`, `core/{config.yaml, module-help.csv}`, `config.toml`, `config.user.toml`, `custom/{.gitignore, bmad-retrospective.toml, config.toml}`, `scripts/{memlog.py, resolve_config.py, resolve_customization.py}`. Same shape as what 6.9.0 code writes (section 4), which is consistent, but not proof | `git ls-files _bmad` | OBSERVED-FROM-6.10.0-TRACKED-TREE |
| Difference showing the tree is not 6.9.0 output: `_config/agent-manifest.csv` is present in the tracked tree but the string `agent-manifest` appears nowhere under `tools/` or `src/` of the 6.9.0 package (Grep returned no files), and `manifest-generator.js:84-93` writes only manifest.yaml, skill-manifest.csv, config.toml, config.user.toml, files-manifest.csv | Grep + manifest-generator.js | CODE-VERIFIED (absence in 6.9.0) |
| `custom/bmad-retrospective.toml` is a project-authored override, not installer output (6.9.0 writes only `custom/config.toml`, `custom/config.user.toml`, `custom/.gitignore`, section 4) | `git ls-files` vs `manifest-generator.js:626-658` | OBSERVED-FROM-6.10.0-TRACKED-TREE |
| `_bmad-output/` in the worktree holds `brainstorming/`, `implementation-artifacts/`, `planning-artifacts/`, `project-context.md`, `specs/`: project documents. Only `planning-artifacts` and `implementation-artifacts` correspond to 6.9.0 installer-created directories | `ls -A _bmad-output` | OBSERVED-FROM-6.10.0-TRACKED-TREE |
| Version difference in a skill: worktree `bmad-help/SKILL.md:26` resolves config with `uv run --python 3.11 {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root}` and reads `core.communication_language` / `modules.bmm.project_knowledge`; the 6.9.0 `src/core-skills/bmad-help/SKILL.md:26` reads `config.yaml` / `user-config.yaml` files instead | Read of both files | version-mismatched, [CODE-CONTRADICTED] as a 6.9.0 description |

### 8.1 The project's own catalogue installer (intent, not 6.9.0 evidence)

`templates/VSCode-AIDev02/image/catalogue/bmad/install.sh` (62 lines) and `.../bmad/manifest.yaml` (30 lines):

| Fact | Evidence | Tag |
|---|---|---|
| Intended image-baked CLI: `npm install -g bmad-method@6.9.0` + `/usr/local/bin/bmad` symlink (stated in an error message); catalogue manifest `version: 6.9.0`, `install_disposition: image-baked` | `install.sh:18`; `manifest.yaml:2,4` | [UNVERIFIED] for the Dockerfile (Dockerfile.coder not read in this task); host binary version 6.9.0 is OBSERVED (`bmad --version`) |
| It installs only into a recorded seed repo, and skips if `_bmad/` exists or tracked `.claude/skills/bmad-*` exist (`install.sh:21-25`) | read | project script, CODE-VERIFIED as written |
| Exact command: `NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output --user-name "$(git -C "${D}" config user.name || id -un)" </dev/null` | `install.sh:42` | every option exists in `install.js:14-37`, so the command is valid for 6.9.0 [CODE-VERIFIED]; it has NOT been observed to run. It takes the partial-seed branch (`ui.js:807-837`), so `project_name`, `communication_language` and `document_output_language` are not written (section 3.2a, fix cycle 1, finding 7) |
| Pre-hides output through the repo's `info/exclude` for `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/` and checks `git status` is unchanged before and after (`install.sh:27-53`). This is the PROJECT's own guard; the installer itself never touches git (section 3.4) | read | project script |
| Failure mode: its own comment says a failed run leaves a partial `_bmad/` that the guard then skips, with no auto-repair (`install.sh:41`). Matches the installer code: `InstallPaths.create` makes `_bmad/` and its subfolders first (`install-paths.js:26-34`) while `manifest.yaml` is written later in the config task (`installer.js:290-346`, `manifest-generator.js:299-394`), and `install()` has no rollback of `_bmad/` on error (`installer.js:122-138` only removes temp backup dirs) | read | CODE-VERIFIED |
| The `timeout 120` is the script author's assumption; it is not duration evidence | `install.sh:42` | UNVERIFIED as a duration |
| The user-facing text offers `bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output` for any other repo | `manifest.yaml:14` | same flag set as section 3.2 |

Key Takeaways:
- Manifest version of the tracked tree is 6.10.0, installed 2026-04-18, upgraded since; it is a tracked tree plus project documents, so it is corroboration only.
- The existing catalogue `install.sh` already uses exactly the flag set derived from the 6.9.0 code, with `NPM_CONFIG_OFFLINE=true`, `--yes`, and a 120 s timeout; it handles only the seed repo.
- A failed or interrupted install leaves a partial `_bmad/` (CODE-VERIFIED), which is exactly the state in which `resolve_config.py` fails with exit 1.

## Gaps and Questions

UNVERIFIED items (13; U13 added in fix cycle 1, finding 7). Each one needs a real run, a different repository, or material outside this task's scope; none was filled by guessing.

| # | UNVERIFIED item | Why it cannot be closed here |
|---|---|---|
| U1 | Real duration of a fresh `bmad install --yes --modules bmm --tools claude-code` | No install may be run (BMAD CLI RULE); no timing data in the package. The catalogue script's `timeout 120` (`install.sh:42`) is an author assumption only |
| U2 | Whether the update-check banner seen under `NPM_CONFIG_OFFLINE=true` came from npm's local cache or the network (`bmad-cli.js:31`) | Not observable from code; only the banner was observed |
| U3 | Side effects of subprocesses the installer starts (`npm view` may write npm's own cache under `~/.npm`; `uv --version`) | npm/uv behaviour, not BMAD code |
| U4 | Default module list of a bare `--yes` (no `--modules`): whether the bundled registry `bmad-modules.yaml` marks any external module `default_selected` (would clone over the network) | `bmad-modules.yaml` not read; the safe form `--modules bmm` avoids the question |
| U5 | Actual output of `resolve_customization.py` when `_bmad/` is absent (derived from code, `resolve_customization.py:209-236`, not executed) | No execution of installed-skill scripts outside a BMAD tree was done |
| U6 | The interpreter's error text when `python3 {project-root}/_bmad/scripts/...` points to a missing file, and how the model behaves in a skill session that has `.claude/skills/bmad-*` but no `_bmad/` | Interpreter message is not BMAD code; model behaviour untested |
| U7 | Whether Claude Code loads user-level `~/.claude/skills` skills in every project and how it ranks them against project-level `.claude/skills` of the same name | Claude Code behaviour, not in this package; matters for options B and E |
| U8 | Whether the user-level hook `~/.claude/hooks/block-bare-python.sh` (observed to block bare `python3` in this session) exists in Coder workspace users' Claude Code environments | Only this session's environment was observed |
| U9 | Whether any later upstream release (the banner reports 6.12.4) added a consumer of `global_target_dir` or a user-scope install flag | Only 6.9.0 was read; no network research was in scope |
| U10 | That `Dockerfile.coder` bakes `npm install -g bmad-method@6.9.0` and the `/usr/local/bin/bmad` symlink (claimed in `install.sh:18`) | Dockerfile not read in this task; the 6.9.0 binary itself is OBSERVED (`bmad --version`) |
| U11 | The exact files a first real install writes (all section 4 rows are read from code, not observed), including the `{output_folder}` substitution that yields `_bmad-output/planning-artifacts`, and the first run in a directory with no `.git` | Requires a real install into a never-installed directory, which is forbidden here |
| U12 | The exact set and count of skills written into `.claude/skills/`: 46 `SKILL.md` counted under `src/core-skills` and `src/bmm-skills`, versus 47 `bmad-*` directories in the tracked 6.10.0 tree; the discovery logic `ManifestGenerator.collectSkills` (`manifest-generator.js:78`) was not enumerated | Count derived by Glob only |
| U13 | With the `install.sh:42` flag set (partial-seed branch, section 3.2a), how skills behave when `project_name`, `communication_language` and `document_output_language` are absent from `config.yaml` (for example `bmad-dev-story/SKILL.md:50-53`, no stated fallback), and which file(s) `--set core.project_name=<value>` patches (`installer.js:329-337`) | Code path read, not run (BMAD CLI RULE); model behaviour untested; `set-overrides.js` not read |

Fix cycle 1 pointer (finding 5): the addendum at the end of this file (`## Addendum (fix cycle 1): Finding 5 ...`, section F5-E) narrows U1, U10, U11 and U12 with prior-review observations and CI figures (tagged "prior-review observation, not re-run"); its section F5-G lists 12 further UNVERIFIED items and 3 stale or CODE-CONTRADICTED items. U1, U11, U12 stay open only for the residuals named in F5-E. U8 is closed by the finding 4 addendum in `03-startup-flow-home-and-user-level-claude.md` (section A1); U7 and U9 stay open until web-01.

CODE-CONTRADICTED / version-mismatch items:

| # | Item | What the code or tree actually shows |
|---|---|---|
| C1 | `platform-codes.yaml:9` describes `global_target_dir` as "User-home directory for global install" | No reader exists in 6.9.0 (section 2); the installer always writes to `<project>/<target_dir>` (`_config-driven.js:247`) |
| C2 | `_bmad/_config/agent-manifest.csv` in the worktree tree looks like installer output | The string `agent-manifest` is absent from the 6.9.0 package; `manifest-generator.js:84-93` does not write it, so the tree is not 6.9.0 output |
| C3 | Worktree `.claude/skills/bmad-help/SKILL.md` (6.10.0) as a description of a 6.9.0 skill | 6.9.0 `src/core-skills/bmad-help/SKILL.md:26` reads `config.yaml` files; 6.10.0 uses `uv run --python 3.11 ... resolve_config.py` (`:26`) |

Open questions for the report author (not answerable from code):
1. Does option B/D need `_bmad/` creation to be atomic? The installer is not (section 8.1: a failed run leaves a partial `_bmad/`).
2. Should a bootstrap guard on `_bmad/config.toml` rather than `_bmad/` alone? A bare `_bmad/` directory (partial install) does not satisfy `resolve_config.py` (`resolve_config.py:156`).
3. Which directory is "the project" when the user opens a subfolder of a repo? `find_project_root` stops at the nearest `_bmad` or `.git`, skills use `{project-root}` = working directory.

## Stale Documentation Found

- **[STALE DOC]** `tools/installer/ide/platform-codes.yaml:9`: comment advertises `global_target_dir` for "global install"; no consumer in 6.9.0 (C1). The 41 values are inert data.
- **[STALE DOC]** `tools/installer/ide/platform-codes.yaml:10`: comment advertises `ancestor_conflict_check` ("Refuse install when ancestor dir has BMAD files"); the reader exists (`_config-driven.js:191`) but no platform entry sets the key, so the feature never fires in 6.9.0 (section 6).
- **[STALE DOC]** Worktree trees `_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*` read as "the installed BMAD" are 6.10.0 (manifest version 6.10.0) and differ from 6.9.0 (C2, C3).
- Catalogue `manifest.yaml:8-18` welcome text ("BMad is already set up there (hidden from git via the repo's info/exclude)") matches what `install.sh:24-54` does when a seed repo is recorded and has no BMAD; behaviour not observed, and it covers only the seed repo.
- `tools/installer/README.md` was searched (Grep for `global|ancestor|home|user-scope|~/|--directory|--yes|non-interactive|git`, no matches) but not read in full.
- Confirmed accurate: the `--tools` help text "Required for fresh non-interactive (--yes) installs" (`install.js:18`) matches `ui.js:630-641` [CODE-VERIFIED].

## Summary

BMAD 6.9.0 (`bmad-method`, Node >=20.12.0) has no first-use bootstrap: a non-interactive install is `bmad install --directory <dir> --modules bmm --tools claude-code --yes`, and by the code it writes only inside that directory (`_bmad/`, `_bmad-output/{planning,implementation}-artifacts/`, `docs/`, `.claude/skills/bmad-*`), never touches git or `~/.claude`, and does not write under HOME or need the network for the built-in `bmm` module (apart from a best-effort `npm view` and a `uv --version` probe). `global_target_dir` has zero consumers in 6.9.0 (option F does not exist), and the ancestor conflict check is dead configuration (no platform enables it), so option E (home install) is not blocked by the installer but would not give per-project `_bmad/`, which the skills need (`{project-root}/_bmad/scripts/*.py`, `config.yaml`, `bmad-help.csv`). With `_bmad/` missing, `resolve_config.py` exits 1 (`required config file not found`) and `resolve_customization.py` silently falls back to skill defaults; no skill detects a missing `_bmad/` or tells the user to install. The worktree's tracked tree is 6.10.0 (manifest version 6.10.0, installed 2026-04-18) and is used only as corroboration; no install and no `bmad` command beyond the four allowed ones was run; 13 items stay UNVERIFIED (U13 added in fix cycle 1).

Question-to-section map: (a) sections 4 and 5; (b) sections 1 and 3.2; (c) section 3.3 and 7.5; (d) section 2 (CODE-VERIFIED: no consumer); (e) section 6; (f) section 7; (g) section 3.4.

## Addendum (fix cycle 1): Finding 5 prior-review observation (memlog), CI test-57 evidence, version-skew risk
**Status:** Complete
**Date:** 2026-11-08

Tag used below: **prior-review observation, not re-run** (PRO) = a figure that a prior review measured and that I only read; I did not run it (BMAD CLI RULE). Every PRO figure carries its exact line.

### F5-A. What the memlog lines say (read in full, quoted exactly)

Source: `_bmad-output/specs/spec-orca-catalogue-bundle/.memlog.md` (104 lines; front matter `updated: 2026-09-24T05:13`, line 3). Lines 20, 21 and 81 are bullets whose origin is "(04 review)" = `.dev/reviews/orca-catalogue-bundle-20260924/04-bmad.md`, which I also read.

| Memlog line | Exact text | PRO tag |
|---|---|---|
| `.memlog.md:20` | `- (note) Finding: bmad install 6.9.0 is project-only (_bmad/, .claude/skills/bmad-* 46 skills, empty _bmad-output/ and docs/), non-interactive with flags, offline, about 4s; user-level install is broken because skills hard-reference {project-root}/_bmad (04 review).` | prior-review observation, not re-run |
| `.memlog.md:21` | `- (note) Finding: bmad 6.9.0 bugs: --yes without --output-folder creates literal {output_folder}/ dir; re-run quick-update dirties 6 files; running over 6.10.0 silently downgrades 41 files with rc 0 (04 review).` | prior-review observation, not re-run |
| `.memlog.md:81` | `- (decision) bmad: run with NPM_CONFIG_OFFLINE=true because 6.9.0 CLI runs npm view bmad-method@latest on every invocation; offline property proven by contract test run with network none.` | claim about a CI/contract run; see F5-C for what the repo shows |

How the numbers were measured (from `04-bmad.md`, which the memlog summarises; PRO):
- `04-bmad.md:4`: "Upstream behavior was **measured** by running `npx bmad-method@6.9.0` in throwaway `/tmp/bmadprobe/*` git repos with `HOME=/tmp/bmadprobe/home`." So the measurement used `npx bmad-method@6.9.0`, NOT the image-baked `/usr/local/bin/bmad` wrapper, and a scratch HOME.
- `04-bmad.md:29`: "`.claude/skills/bmad-*` (46 skills, 2.4M; `--list-tools` shows `claude-code → .claude/skills`)"; `:28` `_bmad/` "(160K)"; `:30-31` `_bmad-output/{planning,implementation}-artifacts/` (empty) and `docs/` (empty); `:32` "It writes **nothing** under `$HOME` apart from the npx cache (`ls -A $HOME` → `.npm` only)."
- `04-bmad.md:34`: "Runtime is about 4s cold (npx fetch included) and about 1s on a re-run." The 4 s therefore INCLUDES an npx package fetch (network); it is not an offline figure and not a baked-CLI figure.
- `04-bmad.md:35`: "It needs no network: an install with `--offline` and a dead proxy exited rc=0, because `bmm` is bundled." This is a separate run from the 4 s run, so memlog:20 "offline, about 4s" joins two different measurements. Whether `--offline` here is an npx flag or a bmad flag is not stated: UNVERIFIED.
- `04-bmad.md:36`: re-run over an existing install: "`--yes` defaults to `quick-update`, which rewrites 6 files (timestamps, re-ordered keys, added `project_name` and language keys) and leaves tracked files dirty."
- `04-bmad.md:37`: "running 6.9.0 `--yes` over a 6.10.0 install downgraded `_bmad/_config/manifest.yaml` to 6.9.0 and changed 41 tracked files, with rc=0 and no warning."
- `04-bmad.md:78` (the version-skew bullet): "The image pins 6.9.0 (`Dockerfile.coder:360`, `manifest.yaml:2`). This repo's `_bmad/` is **6.10.0** (...) and is committed, not ignored (`git check-ignore` returns nothing). (...) A user running the baked `bmad install --yes` in a 6.10.0 repo **downgrades it silently** (measured). The step-1 guard is therefore mandatory."

Scope of the `{output_folder}` defect (note b of the brief). The memlog:21 and `04-bmad.md:33` wording is "`--yes` without `--output-folder`". Code read now:
- `ui.js:838-861` (`else if (options.yes)`): a bare `--yes` on a directory whose existing core config is empty seeds `output_folder: '_bmad-output'` (`:858`) together with `user_name`, `project_name`, `communication_language`, `document_output_language`. So bare `--yes` does not leave `output_folder` unset. [CODE-VERIFIED, Read of `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/ui.js:838-861`]
- `ui.js:807-837` (`if (options.userName || ... || options.outputFolder)`): this branch seeds only the flags passed. So the literal-`{output_folder}/` mechanism lives in the `--user-name` (or other core flag) WITHOUT `--output-folder` combination, as written in section 3.2a rows 1-7 and its bullet 1 above. [CODE-VERIFIED]
- What flags the 04 probe actually passed when it saw the literal directory is not recorded in `04-bmad.md`: UNVERIFIED. Use the memlog:21 phrase only as a quotation, never as a description of bare `--yes`.

### F5-B. test-57: what it is, where the `--network=none` comes from, what the `cold bmad` line times (all [CODE-VERIFIED] by Read this cycle; none executed)

| Fact | Evidence | Tag |
|---|---|---|
| The driver table row for test-57 passes docker options in its 7th column: `.../contract-tests/test-57-catalogue-configure.sh\|-\|${CT}\|-\|y\|artifacts/test-57-catalogue-configure.log\|--network=none,--user=0` | `.github/workflows/coder-ci-aidev02-contract.yml:1241` (header of the columns at `:1232`) | [CODE-VERIFIED] |
| The 7th column is split on commas into `opts` and passed to `docker run` ahead of `--entrypoint bash "${IMAGE_TAG}" "${script}"`; `y` in column 5 means stderr is merged (`2>&1 \| tee "${teefile}"`) | `coder-ci-aidev02-contract.yml:1198` (`read -r script evdir mounts envs stderr teefile extra`), `:1212` (`opts=(); [ -z "$extra" ] \|\| IFS=, read -ra opts <<<"$extra"`), `:1213` (`args+=("${opts[@]}" --entrypoint bash "${IMAGE_TAG}" "${script}")`), `:1217-1218` (merged stderr + tee) | [CODE-VERIFIED] |
| The test refuses to pass if the network is reachable: `getent hosts github.com` or a default route in `ip route` gives `fail "network reachable; this test must run with --network=none"` | `test-57-catalogue-configure.sh:64-66`; header comment `:11` ("Needs --network=none (offline proof)") | [CODE-VERIFIED] |
| So a PASS of test-57 in CI means the baked `/catalogue/bmad/install.sh` ran its `bmad install` with no route to any host. The same precondition exists for 3 other rows (`test-77`, `test-74`, `test-73`, `:1243-1245`) | `:1241-1245` | [CODE-VERIFIED] |
| The `cold bmad` line: for `slug in bmad ironclaude` the test times `expect_rc "first (cold) run ${slug}"` and logs `cold ${slug}: ${ms} ms`, so the CI log line is `[test-57-catalogue-configure] cold bmad: <N> ms` (prefix from `log()` at `:40`) | `test-57-catalogue-configure.sh:172-178` (`now_ms` at `:117`) | [CODE-VERIFIED] |
| The timer wraps the WHOLE `install.sh` via `run_slug` (`:75-79`: `runuser -u coder -- env -i HOME=... bash /catalogue/<slug>/install.sh`), not only `bmad install`. For bmad that includes `git rev-parse`, the exclude-file edit, two `git status` calls, and the `bmad install` (`install.sh:21-60`). `<N>` is therefore an UPPER BOUND on the install itself, and the first `expect_rc` call also includes `chown -R` of the fixture HOME (`:76`) | `test-57:75-79,172-178`; `catalogue/bmad/install.sh:21-60` | [CODE-VERIFIED] |
| Fixture it runs against: a throwaway HOME with `seed/` = `git init -b main` + one committed `README.md` + `.aidev/status/seed-repo-path` pointing at it (`mk_seed`, `mk_home`) | `test-57:119-136` | [CODE-VERIFIED] |
| The 30 s budget and per-run assert: `BUDGET_MS=30000` (`:31`); the sum of the cold bmad and cold ironclaude runs must be <= 30000 ms (`:179-183`) | `test-57:31,179-183` | [CODE-VERIFIED] |
| Existence checks after the cold run: `<seed>/_bmad/_config/manifest.yaml` exists (`:323`) and the seed's git status is empty (`:324`). The test does NOT count skills under `.claude/skills/` or list the files written | `test-57:323-324`; Grep of the file for `skills` finds only the guard fixtures at `:421-444` | [CODE-VERIFIED] (absence of a skill count) |
| The negative fixtures cover the partial and pre-existing cases at the guard: a seed holding only `_bmad/keep` is skipped, rc 0, repo byte-unchanged, health `Installed-not-Configured` (`:413-419`); tracked `.claude/skills/bmad-*` is skipped (`:421-427`); a non-Git seed with only a manifest file is skipped (`:429-435`); a tracked-but-deleted bmad skill file is skipped (`:437-444`) | `test-57:413-444` | [CODE-VERIFIED] |
| The test never installs over a 6.10.0 tree and never checks the version it skipped. Grep for `6.10` in test-57 | see F5-D for the Grep result | see F5-D |

What this does and does not give the research. The test gives an in-image, offline, rc-0 proof of the install command at `install.sh:42` against a one-file git repo, plus a wall-clock number printed per run. It does NOT give the exact file list or the skill count (no assertion of either), so it cannot close U11/U12 by itself.

### F5-C. Latest CI test-57 log: duration and offline result (prior-review observation, not re-run)

Retrieval, all read-only and bounded, ambient `gh` login only: (1) `gh run list --repo IronbellyOrg/Coder --workflow coder-ci-aidev02-contract.yml --limit 8 --json databaseId,status,conclusion,headBranch,event,createdAt,headSha,displayTitle`; (2) for each run id below, `timeout 100 gh run view <id> --repo IronbellyOrg/Coder --log | grep -a -E 'cold (bmad|ironclaude):|FR-21 proxy|test-57-catalogue-configure\] RESULT' | cut -c1-320 | head`. I read the output; I did not re-run test-57 or any install.

| Run (workflow `coder-ci-aidev02-contract.yml`, job `AIDev02 contract tests (dind-sidecar)`) | Event / ref / sha | Log line (exact) | Tag |
|---|---|---|---|
| `42384399575`, created 2026-11-07T15:02:14Z, conclusion `success`; the most recent completed run in the listing (the next one in the listing, `42373385704`, a bot PR run, had conclusion `action_required`; I did not open it) | `push`, `main`, `1371ef5b8716ed7a1cdaacd0cfb6947979dac75d` | `2026-11-07T15:05:57.1358262Z [test-57-catalogue-configure] cold bmad: 374 ms`; `2026-11-07T15:06:01.5283455Z ... cold ironclaude: 4392 ms`; `... PASS  FR-21 proxy: first-run two-step total 4766 ms <= 30000 ms`; `2026-11-07T15:06:43.9611601Z ... RESULT: PASS (configured state proven for ironclaude and bmad, ...; two-step cold total 4766 ms)`. The row ran as `##[group]test-57-catalogue-configure.sh (inside aidev02:contract-42384399575-1)` in step `In-image contract tests (driver)` | prior-review observation, not re-run |
| `42369600288`, 2026-11-07T11:46:42Z, `success` | `schedule`, `main`, `f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1` | `2026-11-07T11:50:18.4942902Z [test-57-catalogue-configure] cold bmad: 392 ms`; total `4905 ms` | prior-review observation, not re-run |
| `42346410588`, 2026-11-07T06:18:24Z, `success` | `push`, `main`, `f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1` | `2026-11-07T06:22:12.8803783Z [test-57-catalogue-configure] cold bmad: 392 ms`; total `4873 ms` | prior-review observation, not re-run |

What the CI numbers mean (inference marked as such):
- `cold bmad` = 374 to 392 ms across three runs, on the CI runner, for the whole baked `install.sh` (F5-B), with no network. Compare memlog:20 "about 4s" and `04-bmad.md:34` "about 4s cold (npx fetch included)": the two are not the same measurement (npx fetch of the package on a scratch HOME versus the image-baked CLI), so the memlog figure must NOT be used for the baked, offline path. The CI figure is the closer proxy for AIDev02. Why the CI figure is lower is not recorded; one candidate is that the `npm view` update probe fails at once with no route and the package is already local: inference, UNVERIFIED.
- `cold ironclaude` is 4392 to 4513 ms in the same runs; the "about 4 s" in the memlog is closer to that one, but memlog:20 attributes it to bmad. I note this only to prevent a mix-up between the two `cold <slug>` lines.
- These are wall-clock numbers from a CI runner, one fixture (a one-file git repo), one image. They are NOT a workspace measurement (a Coder workspace has a different disk, CPU and node cold cache) and say nothing about a first run in a large repo. Treat as order-of-magnitude: sub-second in CI, with the 30 s test budget (`test-57:31,179-183`) as the only enforced bound.
- Offline: the test's own precondition (`test-57:64-66`) plus the docker option at `coder-ci-aidev02-contract.yml:1241` mean a `RESULT: PASS` line is an observation that `catalogue/bmad/install.sh` completed rc 0 with no route to the network and wrote `_bmad/_config/manifest.yaml` and left git status clean (`test-57:323-324`). So the memlog:81 claim "offline property proven by contract test run with network none" is [CODE-VERIFIED] as a mechanism and corroborated by the three PASS logs above. Caveat: the test cannot distinguish "no `npm view` attempted" from "attempted and failed quietly", which is all the research needs.
- The `bmad` that ran is the image-baked one: `Dockerfile.coder:139` `npm install -g bmad-method@6.9.0` and the wrapper at `:134-135,142` (`/usr/local/bin/bmad` is a wrapper script, not a symlink). [CODE-VERIFIED]. This also closes U10 for the Dockerfile half. Note the stale words in `install.sh:18` and catalogue `manifest.yaml`: "symlink" (the Dockerfile comment at `:134-135` says a symlink would fail with `env: node: not found`). [STALE DOC, low impact]
- Image line refs in `04-bmad.md` (`Dockerfile.coder:360`) are stale: the pin is now at `Dockerfile.coder:139`. [CODE-CONTRADICTED for the line number only]

### F5-D. Version skew: "6.9.0 over an existing 6.10.0 or partial tree" (code behind the PRO claim, and what the repo tests)

Starting facts. The image CLI is 6.9.0 (`Dockerfile.coder:139`). This worktree carries a 6.10.0 tree (`_bmad/_config/manifest.yaml:2` `installation.version: 6.10.0`; `:7`, `:14` both modules 6.10.0; Read this cycle) [CODE-VERIFIED]; file 01 section 8 already records 17 tracked `_bmad` files and 237 tracked `.claude/skills/bmad-*` files there. The same skew exists for any user repo that adopted a newer BMAD than 6.9.0.

Code path that explains the memlog:21 "silently downgrades 41 files with rc 0" (the 41 and the rc are PRO; the path is read this cycle):
| Step | Evidence | Tag |
|---|---|---|
| `bmad install --directory P` computes `bmadDir = P/_bmad` and treats it as "existing" if the path exists, at all | `installer.js:1549-1552` (`findBmadDir`, "Always uses the standard _bmad folder name"); `ui.js:217-220` (`hasExistingInstall = await fs.pathExists(bmadDir)`) | [CODE-VERIFIED] |
| "Installed" is true if `_bmad/core/` exists OR any module is listed OR a readable manifest exists; the version read from the manifest is only informational | `core/existing-install.js:50-66,111` (`installed = hasCore \|\| modules.length > 0 \|\| !!manifestData`) | [CODE-VERIFIED] |
| With `--yes` and no `--action`, an installed tree defaults to `quick-update`, otherwise to `update`; no prompt, no version test | `ui.js:233-239` (Quick Update offered when `existingInstall.installed`), `:252-262` (`--yes` picks `quick-update`; log line `Non-interactive mode (--yes): defaulting to quick-update`) | [CODE-VERIFIED] |
| No installer-version-versus-installed-version comparison gates the write. Whole-`tools/installer` Grep for `downgrad\|isNewer\|semver\|compareVersions` finds `semver` only in `bmad-cli.js:7,37` (update banner), `ui.js:3,33,43-57,189` (banner text and a prerelease note), `modules/channel-resolver.js` (external-module tags; `:195` comment "same version (or downgrade; treated same)"), `core/legacy-warnings.js:3,106-108` (minimum-version warning) and `core/manifest.js:401-418` (an "update available" comparison). The word `downgrad` appears only in that `channel-resolver.js:195` comment. Match lines only, those files were not read in full | Grep | [CODE-VERIFIED] for the absence of a gate on the installer.js path (no `semver` hit in `core/installer.js`); the semantics of each hit above are UNVERIFIED beyond the match line |
| The manifest the installer writes records the INSTALLER'S OWN package version: `install-paths.js:13` `const version = require(pkgPath).version`; file 01 section 4 row for `manifest.yaml` ("`installation.version` = package version"). This is consistent with PRO "downgraded `_bmad/_config/manifest.yaml` to 6.9.0" | `install-paths.js:13`; file 01 section 4 | [CODE-VERIFIED] for the source of the number; the 41-file count is PRO only |
| A PARTIAL `_bmad/` is not "nothing": `InstallPaths.create` makes `_bmad/`, `_bmad/core/`, `_bmad/_config/`, `_bmad/scripts/`, `_bmad/custom/` before anything else (`install-paths.js:21-34`). So a failed 6.9.0 first run leaves a `_bmad/core/` that makes `ExistingInstall.detect` report `installed` (`existing-install.js:64-66,111`). A later `bmad install --yes` (the manual one-command path in the welcome text, catalogue `manifest.yaml:14`) therefore takes the quick-update branch, not the fresh-install branch. What quick-update then does to a half-written tree was NOT read or run | `install-paths.js:21-34`; `existing-install.js:64-66,111`; `ui.js:233-262` | mechanism [CODE-VERIFIED]; outcome UNVERIFIED |

What the repo's own guard and test cover:
- The guard `install.sh:24` skips on `[ -e "${D}/_bmad" ]` (any entry, including a bare directory) OR any tracked `.claude/skills/bmad-*`. A 6.10.0 tree with `_bmad/` is skipped, a partial `_bmad/` is skipped. [CODE-VERIFIED, `catalogue/bmad/install.sh:24-25`]
- `test-57` proves the skip for a bare `_bmad/` containing one file (`:413-419`), tracked `.claude/skills/bmad-*` (`:421-427`), a non-Git seed with only `_bmad/_config/manifest.yaml` (`:429-435`) and a tracked-but-deleted bmad skill (`:437-444`). Every fixture's content is a placeholder (`'user'`, `'skill'`, `'manifest'`); none is a 6.10.0 tree and none inspects a version. Grep of `test-57` for `6\.10` and `6\.9` finds no hit (the `version` hits are IronClaude/codegraph lines 235-304, 357-361, and the `manifest.yaml` path at 323, 432, 458, 528). So "6.9.0 over 6.10.0 is refused" is covered by the existence guard, not by a version test. [CODE-VERIFIED absence]
- The guard is part of the slug, not of the installer. Anything that calls `bmad install --yes` without the guard (the manual one-command path, a user in a terminal, a wrapper that passes `bmad install` through unchanged as file 03 A3 item C.5 requires) reaches `ui.js:252-262` unguarded. [CODE-VERIFIED by reading]
- Untested seam: `install.sh:24` second half uses `git ls-files`, which sees only TRACKED skills. A repo with untracked 6.10.0 skills and no `_bmad/` (for example `_bmad/` deleted, skills left) would pass the guard (file 03 A2 table row 3 says the same) and would be installed over by 6.9.0. File 03's FIRST_USE(P) closes it with an on-disk glob. [CODE-VERIFIED for the guard text; the outcome is derived, not run]

### F5-E. Narrowed UNVERIFIED items: U1, U10, U11, U12 (replacement wording for the report; the original table rows above were not edited)

One CI limit that applies to all four: `run_slug` discards the installer's output (`test-57:75-79`, `>/dev/null 2>&1`), and `show_log` (`:116`) prints `/tmp/catalogue-<slug>.log` only on an unexpected exit. So the CI log carries the `cold bmad: N ms` line and PASS/FAIL rows but NOT the installer's own text (no `Claude Code configured: <N> skills` line, no file list). [CODE-VERIFIED]

| Item | Was | Now (what is known, tagged) | Still UNVERIFIED |
|---|---|---|---|
| U1 duration of a fresh install | "No timing data" | (a) memlog:20 "about 4s", from `04-bmad.md:34` "about 4s cold (npx fetch included) and about 1s on a re-run": scratch HOME, `npx bmad-method@6.9.0`, network available, scratch git repos (`04-bmad.md:4`). prior-review observation, not re-run. (b) CI `cold bmad: 374 ms` (run `42384399575`, log time `2026-11-07T15:05:57.1358262Z`), `392 ms` (`42369600288`), `392 ms` (`42346410588`): image-baked CLI, `--network=none`, one-file fixture repo, whole `install.sh` included. prior-review observation, not re-run. (c) the 30 s budget for the sum of bmad plus ironclaude is enforced (`test-57:31,179-183`); the script's `timeout 120` (`install.sh:42`) stays an author assumption | Duration inside a real Coder workspace (home volume, cold node page cache, the real seed repo's size); duration with live network and a working `npm view`. The two prior figures differ by about ten times and are not the same configuration; do not blend them |
| U10 `Dockerfile.coder` bakes `bmad-method@6.9.0` and the wrapper | "Dockerfile not read" | `Dockerfile.coder:139` `npm install -g bmad-method@6.9.0`; `:134-135` comment that `/usr/local/bin/bmad` is a wrapper, not a symlink; `:142` the wrapper line. [CODE-VERIFIED, Read this cycle]. File 05's `Dockerfile.coder:139-143` citation (05 C1) is correct. `install.sh:18` still says "symlink": stale words only | That the built image really contains it: only the Dockerfile text and the CI PASS of test-57 (which needs `bmad` on PATH, `install.sh:18`) are evidence; the image was not inspected |
| U11 exact files a first install writes | "all rows read from code, not observed" | Directory-level list from a prior real run (`04-bmad.md:28-32`, prior-review observation, not re-run): `_bmad/` 160K with `core/`, `bmm/`, `_config/manifest.yaml`, `config.toml`, `config.user.toml`, `custom/`, `scripts/`; `.claude/skills/bmad-*` (46 skills, 2.4M); `_bmad-output/{planning,implementation}-artifacts/` empty; `docs/` empty; nothing under `$HOME` except `.npm`. It agrees with the code-derived table in section 4 at directory level. It lists no individual files and says nothing about `_config/*.csv`. The empty `_bmad-output/{planning,implementation}-artifacts/` in that run corroborates the `{output_folder}` substitution for the flag set it used (which flags is not recorded: UNVERIFIED). CI proves `_bmad/_config/manifest.yaml` exists and `git status` stays empty (`test-57:323-324`) | The exact per-file list; the flags of the 04 probe; the first run in a directory with NO `.git` (the 04 probes were git repos, `04-bmad.md:4`; the test-57 non-Git fixture is a skip case, `:429-435`); whether the `.npm` in the scratch HOME came from `npx` or `npm view` (U3 stays open) |
| U12 skill count | "46 by Glob vs 47 in the 6.10.0 tree" | Two routes agree for 6.9.0: 46 `SKILL.md` under `src/core-skills` and `src/bmm-skills` (Glob, file 01 U12) and "46 skills, 2.4M" in `04-bmad.md:29` (prior-review observation, not re-run). The 47 is the tracked 6.10.0 tree, a different version | `ManifestGenerator.collectSkills` (`manifest-generator.js:78`) was not enumerated; the name list of the 46 was not recorded; CI does not count skills |

Suggested wording for the report: "A prior review installed 6.9.0 in scratch git repos and recorded about 4 s including the npx fetch, 46 skills, and no writes under HOME apart from `.npm` (`.memlog.md:20`, `04-bmad.md:28-34`, prior-review observation, not re-run). The image-baked CLI completes the whole `catalogue/bmad/install.sh` in 374 to 392 ms in CI with no network (run 42384399575 and two earlier runs, prior-review observation, not re-run). No install was run for this research."

### F5-F. Risk row to add to options B, C and D: "6.9.0 over an existing 6.10.0 or partial tree"

Trigger predicate reference. The first-use predicate is defined by another researcher in `research/03-startup-flow-home-and-user-level-claude.md`, heading `## Addendum (fix cycle 1): Finding 4 first-use trigger predicate, per-option walkthrough, block-bare-python.sh (01 U8)`, subsection `### A2. One first-use trigger predicate, and the guard it matches` (the definition is `FIRST_USE(P)`, items 1 to 4). That addendum was marked In Progress when I read it; I did not edit it. The risk below is stated against FIRST_USE(P) items 2 and 3 (`_bmad` absent; no `.claude/skills/bmad-*` entry on disk) and, where the predicate is not used, against the existing guard `catalogue/bmad/install.sh:24` and the partial-`_bmad/` case in this file's Gaps and Questions, open question 2 (`resolve_config.py:156` needs `_bmad/config.toml`).

Risk statement (common to B, C, D): the 6.9.0 installer has no installed-versus-installer version gate (F5-D). If the install command runs in a project that already has BMAD, `bmad install --yes` goes to quick-update and rewrites that tree with 6.9.0 content, exit code 0, no warning. Prior review measured this on a 6.10.0 tree: manifest to 6.9.0 and 41 files changed (`.memlog.md:21`, `04-bmad.md:37`, prior-review observation, not re-run). Rows:

| Option | Where the risk bites | Protection that exists in code | What is not protected | Tag |
|---|---|---|---|---|
| B (B1/B2/B3, user-level stub that installs on first use) | The stub's steps run as model-followed text in a Bash tool call (file 03 A3 B.2). The install command it issues has no version gate. If the stub evaluates a looser test than FIRST_USE(P), or the model skips the test, 6.9.0 overwrites a 6.10.0 project and the exit code 0 gives the stub no signal | FIRST_USE(P) items 2 and 3 return false for any tree with `_bmad/` or on-disk bmad skills, including a 6.10.0 tree, a partial `_bmad/`, and a tracked tree with `_bmad/` deleted | Model compliance with the stub text (UNVERIFIED). A stub that offers "reinstall" or "update" reintroduces the quick-update path (`ui.js:252-262`). A partial `_bmad/` left by an interrupted run is "not first use" forever, so skills fail with exit 1 at `resolve_config.py:156` and the stub, by predicate, will not retry | predicate [CODE-VERIFIED] (file 03 A2); model behaviour [UNVERIFIED] |
| C (image-level `bmad` wrapper, `Dockerfile.coder:142`) | The wrapper must pass `bmad install` through unchanged (file 03 A3 C.5; health check and `install.sh:42` use it). A user typing `bmad install --yes ...` by hand in a 6.10.0 project, for example copying the one-command line from the welcome text (catalogue `manifest.yaml:14`, which has no guard), downgrades it exactly as measured. The first-use hook inside the wrapper does not cover that path | A wrapper that evaluates FIRST_USE(P) before running anything else protects only the invocations it intercepts | The pass-through `install` subcommand, and the image pin itself: the image stays at 6.9.0 while the observed upstream banner is 6.12.4 (file 01 U2/U9), so the number of repos on a newer tree can only grow | [CODE-VERIFIED] for the unguarded `ui.js:252-262` path and the pass-through requirement; banner version observed in this session, not re-run |
| D (D1/D2/D3, SessionStart or UserPromptSubmit hook) | The hook fires in every project (file 03 A3 D.1), so every repo with a 6.10.0 tree meets the predicate every session; correctness of a cheap, fast predicate is the only barrier, and there is no user prompt (file 03 A3 D.5). Two extra seams: (1) a hook that uses the session cwd rather than the repo top evaluates `_bmad` in the wrong directory for a subfolder session (FIRST_USE item 1 resolves to the repo top; `resolve_customization.py:58-66` stops at `_bmad` or `.git`); (2) a hook `timeout` shorter than the install (all 29 existing timeouts are 1 to 10 s, file 03 A3 D.2; install time inside a workspace is U1) kills a run after `_bmad/core/` exists (`install-paths.js:21-34`) and leaves a partial tree | FIRST_USE(P) items 2 and 3 | Hook timeout versus install time (U1 residual); partial tree after a kill is not retried by the predicate; hook cwd choice | predicate [CODE-VERIFIED]; the timeout interaction is derived, UNVERIFIED |

Plain statement for all three: the CI evidence shows the guard at `install.sh:24` working on placeholder trees (F5-D), not on a real 6.10.0 tree, and the installer provides no second line of defence. A real 6.10.0 tree exists only in this worktree (`_bmad/_config/manifest.yaml:2`), so a read-only test of the predicate against it would be possible, but none was run (no install, no scratch install allowed).

### F5-G. Addendum Gaps and Questions (appended here because the existing table was not edited)

UNVERIFIED (12):
| # | Item | Reason |
|---|---|---|
| F5-1 | The flags the 04 probe passed when it saw the literal `{output_folder}/` directory | `04-bmad.md:33` states the defect for "`--yes` without `--output-folder`" and does not record the full command; `ui.js:838-861` seeds `_bmad-output` for bare `--yes` |
| F5-2 | Whether `--offline` in `04-bmad.md:35` is an npx flag or a bmad flag, and whether "dead proxy" blocked the npx fetch | Not stated in the review; Grep for `offline` in `bmad-method/tools/installer/commands/install.js` finds no match, so it is not a `bmad install` option in 6.9.0 (CODE-VERIFIED absence), which makes an npx or npm flag the likely reading (inference) |
| F5-3 | Why CI `cold bmad` (374 to 392 ms) is about ten times below the memlog "about 4s" | Different configuration (baked CLI, no npx fetch, no network, CI runner); the cause is an inference, no profile data |
| F5-4 | Install duration in a real Coder workspace and in a large seed repo | No such measurement exists; no install may be run |
| F5-5 | Per-file list written by a first install, and a first run in a directory with no `.git` | PRO is directory-level and used git repos; CI non-Git fixture is a skip case |
| F5-6 | Names of the 46 skills and `collectSkills` enumeration | Not recorded by the prior review; CI discards installer output (`test-57:78`) |
| F5-7 | The counts "6 files rewritten by quick-update" and "41 files downgraded" | prior-review observation, not re-run, `04-bmad.md:36-37`; no re-run permitted |
| F5-8 | What quick-update does to a half-written `_bmad/` left by a failed first run | Mechanism read (`existing-install.js:64-66`, `ui.js:233-262`); the quick-update implementation (`installer.js:1254-`) was not read |
| F5-9 | Model compliance with a stub's predicate (B), hook timeout versus install time (D), cwd choice in a hook (D) | Claude Code and model behaviour; nothing run |
| F5-10 | The image actually contains `bmad-method@6.9.0` | Only `Dockerfile.coder:139` text and CI PASS (needs `bmad` on PATH, `install.sh:18`); image not inspected |
| F5-11 | The origin of the `.npm` directory in the 04 scratch HOME | `npx` itself writes there; cannot be attributed to `npm view` (U3 stays open) |
| F5-12 | The meaning of the `semver` hits in `ui.js`, `manifest.js`, `legacy-warnings.js`, `channel-resolver.js` beyond their match lines | Files not read in full; the claim relied on is only that `core/installer.js` has no semver token |

CODE-CONTRADICTED / stale (3):
| # | Item | What the code shows |
|---|---|---|
| F5-C1 | `.memlog.md:21` and `04-bmad.md:33`: "`--yes` without `--output-folder` creates literal `{output_folder}/` dir" read as a bare-`--yes` defect | `ui.js:838-861`: bare `--yes` on an empty config seeds `output_folder: '_bmad-output'`; the unresolved-text mechanism is the partial-seed branch (`ui.js:807-837`, section 3.2a). Quote the memlog line, do not describe it as a bare-`--yes` defect |
| F5-C2 | `04-bmad.md:15` (`Dockerfile.coder:322-366`, pin at `:360`, wrapper `:361-364`) and `04-bmad.md:78` | The pin is at `Dockerfile.coder:139` and the wrapper lines at `:134-143` (Read this cycle); the review's line numbers are stale |
| F5-C3 | `catalogue/bmad/install.sh:18` error text says "`/usr/local/bin/bmad` symlink" | `Dockerfile.coder:134-135,142`: it is a wrapper script, a symlink would fail with `env: node: not found` |

### F5-H. Summary (3 sentences)

The finding was right that existing observations were dropped: the memlog and `04-bmad.md` hold a prior real 6.9.0 run (about 4 s including an npx fetch, 46 skills, directory-level file list, no HOME writes, rc 0 with a dead proxy) and CI test-57 holds a second, more relevant one (`cold bmad` 374 to 392 ms for the whole baked `install.sh` with `--network=none`, three runs), both now recorded as "prior-review observation, not re-run" and used to narrow U1, U10, U11 and U12 without re-running anything. The version-skew risk was also real and is now code-backed: the installer has no version gate, an existing `_bmad/` (even a partial one with `core/`) sends `--yes` to quick-update (`ui.js:233-262`, `existing-install.js:111`), and only the slug's existence guard (`install.sh:24`, tested only on placeholder trees) and file 03's FIRST_USE(P) stand between 6.9.0 and a 6.10.0 tree, so the risk row is added for B, C and D. Two memlog statements need careful wording: the `{output_folder}` defect must be quoted, not described as a bare-`--yes` defect (`ui.js:838-861` seeds it), and "offline, about 4s" joins two separate measurements; 12 items stay UNVERIFIED and 3 are CODE-CONTRADICTED or stale (F5-G).
