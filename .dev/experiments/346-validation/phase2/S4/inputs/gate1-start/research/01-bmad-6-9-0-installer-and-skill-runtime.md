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
| 40 SKILL.md files reference `resolve_config.py`/`resolve_customization.py` (92 occurrences) | Grep `resolve_config|resolve_customization` count output |
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
| Exact command: `NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output --user-name "$(git -C "${D}" config user.name || id -un)" </dev/null` | `install.sh:42` | every option exists in `install.js:14-37`, so the command is valid for 6.9.0 [CODE-VERIFIED]; it has NOT been observed to run |
| Pre-hides output through the repo's `info/exclude` for `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/` and checks `git status` is unchanged before and after (`install.sh:27-53`). This is the PROJECT's own guard; the installer itself never touches git (section 3.4) | read | project script |
| Failure mode: its own comment says a failed run leaves a partial `_bmad/` that the guard then skips, with no auto-repair (`install.sh:41`). Matches the installer code: `InstallPaths.create` makes `_bmad/` and its subfolders first (`install-paths.js:26-34`) while `manifest.yaml` is written later in the config task (`installer.js:290-346`, `manifest-generator.js:299-394`), and `install()` has no rollback of `_bmad/` on error (`installer.js:122-138` only removes temp backup dirs) | read | CODE-VERIFIED |
| The `timeout 120` is the script author's assumption; it is not duration evidence | `install.sh:42` | UNVERIFIED as a duration |
| The user-facing text offers `bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output` for any other repo | `manifest.yaml:14` | same flag set as section 3.2 |

Key Takeaways:
- Manifest version of the tracked tree is 6.10.0, installed 2026-04-18, upgraded since; it is a tracked tree plus project documents, so it is corroboration only.
- The existing catalogue `install.sh` already uses exactly the flag set derived from the 6.9.0 code, with `NPM_CONFIG_OFFLINE=true`, `--yes`, and a 120 s timeout; it handles only the seed repo.
- A failed or interrupted install leaves a partial `_bmad/` (CODE-VERIFIED), which is exactly the state in which `resolve_config.py` fails with exit 1.

## Gaps and Questions

UNVERIFIED items (12). Each one needs a real run, a different repository, or material outside this task's scope; none was filled by guessing.

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

BMAD 6.9.0 (`bmad-method`, Node >=20.12.0) has no first-use bootstrap: a non-interactive install is `bmad install --directory <dir> --modules bmm --tools claude-code --yes`, and by the code it writes only inside that directory (`_bmad/`, `_bmad-output/{planning,implementation}-artifacts/`, `docs/`, `.claude/skills/bmad-*`), never touches git or `~/.claude`, and does not write under HOME or need the network for the built-in `bmm` module (apart from a best-effort `npm view` and a `uv --version` probe). `global_target_dir` has zero consumers in 6.9.0 (option F does not exist), and the ancestor conflict check is dead configuration (no platform enables it), so option E (home install) is not blocked by the installer but would not give per-project `_bmad/`, which the skills need (`{project-root}/_bmad/scripts/*.py`, `config.yaml`, `bmad-help.csv`). With `_bmad/` missing, `resolve_config.py` exits 1 (`required config file not found`) and `resolve_customization.py` silently falls back to skill defaults; no skill detects a missing `_bmad/` or tells the user to install. The worktree's tracked tree is 6.10.0 (manifest version 6.10.0, installed 2026-04-18) and is used only as corroboration; no install and no `bmad` command beyond the four allowed ones was run; 12 items stay UNVERIFIED.

Question-to-section map: (a) sections 4 and 5; (b) sections 1 and 3.2; (c) section 3.3 and 7.5; (d) section 2 (CODE-VERIFIED: no consumer); (e) section 6; (f) section 7; (g) section 3.4.
