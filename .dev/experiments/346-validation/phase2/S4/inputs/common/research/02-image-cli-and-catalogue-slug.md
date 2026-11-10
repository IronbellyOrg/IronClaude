# Research: image CLI and catalogue slug for BMAD
**Investigation type:** Integration Mapper
**Scope:** templates/VSCode-AIDev02/image/Dockerfile.coder; image/catalogue/bmad/{install.sh,manifest.yaml,module.tf}; image/catalogue/{profiles.yaml,README.md}; templates/VSCode-AIDev02/{modules.tf,parameters.tf}; image/scripts/lib/spec2-health.sh
**Status:** Complete
**Date:** 2026-11-07
---

## 1. (a) The `/usr/local/bin/bmad` wrapper and the pinned install

### 1.1 Dockerfile.coder lines 133-145 (BMad layer)

| Line | Fact | Tag |
|---|---|---|
| 133 | Comment: "BMad CLI (bmad-method), exact-semver pin. Needs registry egress at build time (host-network build)." | [CODE-VERIFIED] |
| 134-135 | Comment: wrapper is not a symlink because the bin is `#!/usr/bin/env node` and NVM node is not on default PATH | comment [CODE-VERIFIED]; the runtime-PATH claim itself [UNVERIFIED] (not tested; no shell was run with the image PATH) |
| 136 / 145 | Layer runs as `USER root`, then back to `USER 1000` | [CODE-VERIFIED] |
| 139 | `npm install -g bmad-method@6.9.0` inside `bash -c '. "$NVM_DIR/nvm.sh" && ...'` (exact-semver pin, global install into the NVM node tree) | [CODE-VERIFIED] Dockerfile.coder:139 |
| 140-141 | `node_bin="$(nvm which current)"`, `cli="$(readlink -f "$(dirname "$node_bin")/bmad")"` | [CODE-VERIFIED] |
| 142 | Writes `/usr/local/bin/bmad` as two lines: `#!/bin/sh` and `exec "<node_bin>" "<cli>" "$@"` | [CODE-VERIFIED] |
| 143 | `chmod 0755 /usr/local/bin/bmad` | [CODE-VERIFIED] |
| 144 | `chown -R 1000:1000 "$NVM_DIR"` (the global npm tree is owned by the workspace user) | [CODE-VERIFIED] |

Other `bmad` mentions in Dockerfile.coder: only line 277 (a `_bmad-output/specs/...` path inside a telemetry comment; not a BMad install). Case-insensitive grep hit lines: 133, 134, 139, 141, 142, 143, 277.

### 1.2 The wrapper as it exists on this machine

Read of `/usr/local/bin/bmad` (3 lines, read-only, not modified):

```
#!/bin/sh
exec "/opt/nvm/versions/node/v24.22.2/bin/node" "/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/bmad-cli.js" "$@"
```

It matches what Dockerfile.coder:142 generates. [CODE-VERIFIED] /usr/local/bin/bmad:1-3. The wrapper has NO logic: no cwd check, no `_bmad` check, no environment setup, no bootstrap. It is a pure `exec` of node on the CLI entry.

### 1.3 What the exec'd code does (`/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/`, read-only evidence)

| File:line | Fact |
|---|---|
| package.json:3-4 | `"name": "bmad-method"`, `"version": "6.9.0"` [CODE-VERIFIED]; installed version equals the pin |
| package.json:22-25 | `bin.bmad` and `bin["bmad-method"]` both point at `tools/installer/bmad-cli.js`; `main` the same |
| package.json:112-114 | `engines.node >=20.12.0` |
| tools/installer/bmad-cli.js:20-22 | At every start, `checkForUpdate()` is fired asynchronously, errors swallowed |
| bmad-cli.js:31-35 | `checkForUpdate` runs `execSync('npm view bmad-method@<tag> version', timeout 5000)` |
| bmad-cli.js:73-81 | Loads every `*.js` in `tools/installer/commands/` (present: `install.js`, `status.js`, `uninstall.js`) and registers each as a commander subcommand |
| bmad-cli.js:84 | `program.version(packageJson.version)` |
| bmad-cli.js:100-105 | `program.parse(process.argv)`; with no arguments prints help |

Nothing in `bmad-cli.js` looks for `_bmad/` in the start directory. Directory handling is in `commands/install.js` and `ui.js` (section 2).

### 1.4 Permitted `bmad` commands that were run (offline flag set)

| Command | Result |
|---|---|
| `NPM_CONFIG_OFFLINE=true bmad --version` | `6.9.0` |
| `NPM_CONFIG_OFFLINE=true bmad install --help` | Lists options: `--directory <path>`, `--modules`, `--tools`, `--list-tools`, `--set`, `--list-options`, `--action`, `--user-name`, `--communication-language`, `--document-output-language`, `--output-folder`, `--custom-source`, `-y/--yes`, `--channel`, `--all-stable`, `--all-next`, `--next`, `--pin`, `-d/--debug`. Matches `commands/install.js:12-51` [CODE-VERIFIED] |
| `NPM_CONFIG_OFFLINE=true bmad install --list-tools` | Prints 44 tool IDs with "Target dir" column; `claude-code` target dir `.claude/skills` (the output has only a project-relative target dir, no global column) |
| `NPM_CONFIG_OFFLINE=true bmad install --list-options` | Prints `--set` keys for `core` and `bmm` (see 2.4) |

Anomaly: with `NPM_CONFIG_OFFLINE=true`, `--list-tools` and `--list-options` still printed an "Update Available: you are using 6.9.0 but 6.12.4 is available" box. So the offline flag did not suppress the `npm view` result here (the task text expected it to stop `npm view`). Cause not investigated (could be npm cache); stated as an observation only. Newer upstream (6.12.4) exists, reported by that box; not independently verified [UNVERIFIED].

Key Takeaways (a):
- The wrapper is a 2-line `exec node <cli> "$@"`; zero first-use logic. Any first-use behaviour in the wrapper is NEW code and lives in `Dockerfile.coder` (image rebuild).
- The pin is `npm install -g bmad-method@6.9.0` at Dockerfile.coder:139; the live install is 6.9.0 (package.json:4).
- Every `bmad` start spawns an `npm view` (bmad-cli.js:31) whose update box can appear in output even with `NPM_CONFIG_OFFLINE=true`.

## 2. (b) `catalogue/bmad/install.sh` line by line (61 lines; re-read this session)

File: `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh`

| Lines | What it does | Tag |
|---|---|---|
| 1-4 | Shebang, header comment ("verifies the image-baked `bmad` CLI and runs a per-repo `bmad install` into the seed repo, hidden via info/exclude. Run by startup in a subshell"), `set -euo pipefail` | [CODE-VERIFIED] |
| 6-10 | `SLUG` from own dir name (-> `bmad`); `LOG=/tmp/catalogue-bmad.log`; `MARKER=${HOME}/.aidev/installed/bmad`; `SEED_PATH_FILE=${HOME}/.aidev/status/seed-repo-path` | [CODE-VERIFIED] |
| 12-13 | `mkdir -p` marker dir and log dir; `exec > >(tee -a "${LOG}") 2>&1` | [CODE-VERIFIED] |
| 18 | CLI check: `command -v bmad` else prints `FAIL: bmad not on PATH (expected image-layer install via npm install -g bmad-method@6.9.0 + /usr/local/bin/bmad symlink — see Dockerfile.coder)` and `exit 2` | [CODE-VERIFIED] |
| 18 (text) | Message says "`/usr/local/bin/bmad` symlink" but Dockerfile.coder:134-143 makes a wrapper script, not a symlink | **[STALE DOC]** inside a string; [CODE-CONTRADICTED] by Dockerfile.coder:134 and /usr/local/bin/bmad:1-3 |
| 21 | `D="$(head -n1 "${SEED_PATH_FILE}" 2>/dev/null \|\| true)"` | [CODE-VERIFIED] |
| 22-23 | Guard 1: if `D` empty OR `git -C D rev-parse --is-inside-work-tree` is not `true`: prints "no seed repo recorded; nothing to configure", falls through to the marker write (exit 0) | [CODE-VERIFIED] |
| 24-25 | Guard 2: elif `D/_bmad` exists OR `git ls-files -- '.claude/skills/bmad-*'` is non-empty: prints "seed repo already has BMad ... left untouched", falls through to marker write (exit 0) | [CODE-VERIFIED] |
| 26-35 | Else-branch start. Exclude file from `git rev-parse --git-path info/exclude` (28); relative path is prefixed with `D` (29); `mkdir -p` its dir (30); adds a trailing newline if the file lacks one (31); appends each of `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/` unless present as an exact line (32-34) | [CODE-VERIFIED] |
| 38 | `before="$(git -C D status --porcelain --untracked-files=all)"` taken AFTER the excludes | [CODE-VERIFIED] |
| 41 | Comment: a failed run leaves a partial `_bmad/` which guard 2 then skips; no auto-repair | [CODE-VERIFIED] (comment); behaviour follows from lines 24 and 42-45 |
| 42-45 | The single install call: `NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output --user-name "$(git -C "${D}" config user.name \|\| id -un)" </dev/null`. On any non-zero (including `timeout` 124) prints `FAIL: bmad install exited non-zero` and `exit 1` | [CODE-VERIFIED]; every flag exists in `commands/install.js:12-51` |
| 46 | `[ -f "${D}/_bmad/_config/manifest.yaml" ]` else `FAIL ... missing after bmad install`, `exit 1` | [CODE-VERIFIED] |
| 48-53 | `after=` same git status; if `before != after`: prints `FAIL: bmad install changed the seed repo's git status:` plus a diff, `exit 1` | [CODE-VERIFIED] |
| 54 | "seed repo configured; git status unchanged" | [CODE-VERIFIED] |
| 58-60 | Marker: `date -Iseconds > ${MARKER}`, `chmod 0644`; printed "install ok" | [CODE-VERIFIED] |
| 61 | `exit 0` | [CODE-VERIFIED] |

Notes on the task's wording: there is NO "git-clean" pre-check. The script never requires a clean tree; it only requires that git status is identical before and after the install (lines 38/48-53), after the three ignore patterns were added (lines 32-34). A dirty seed repo is accepted (test-57-catalogue-configure.sh:457-458 "dirty seed: bmad configures").

Exit codes: `0` at line 61 (reached via lines 23, 25 and 54 paths too), `1` at lines 44, 46, 52, `2` at line 18. Other exits come from `set -e`/`pipefail` (for example a failing `mkdir` at 12, or `git rev-parse --git-path` at 28) with the failing command's own status. `timeout` status 124 is swallowed into exit 1 by the `if !` at line 42. [CODE-VERIFIED by reading; the script was not run.]

Observations (from reading, not running):
- There is no top-of-file idempotency short-circuit on `marker + CLI` (compare ironclaude/install.sh:31-35 and README.md:179-183, contract FR30 #5). bmad's idempotency comes from guard 2 (line 24) instead.
- The failure paths at lines 44, 46 and 52 exit before the marker write (58), but leave `_bmad/` and the info/exclude lines in place. On the NEXT boot guard 2 (line 24) sees `_bmad/` and goes straight to the marker write, so a failed or status-changing first install turns into a "configured/untouched" pass one boot later. Health then reads `Configured` iff `_bmad/_config/manifest.yaml` exists (spec2-health.sh:103-104). [CODE-VERIFIED by reading lines 24, 41, 58 and spec2-health.sh:103]
- The installer only ever targets the ONE seed repo (line 21). Any other project is out of scope of install.sh; the manifest welcome text sends the user to a manual command (section 3.1).
- Footprint hidden from git by the script: `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/` (line 32). These are the three repo paths the script itself treats as BMad's output. A first-use run in another repo would need its own exclude handling or it would show untracked files.
- How it is run: startup.sh:1174-1176 runs it as `( source "${HOME}/.aienv" && bash "<dir>/<script>" ) > "<log>" 2>&1`, WITHOUT the 30 s bound that other slugs get through `aidev_cat_install` (startup.sh:1177-1181); bmad has its own `timeout 120` (install.sh:42). [CODE-VERIFIED startup.sh:1170-1182]. Only `workspace`/`hybrid` scopes run at boot (startup.sh:1158-1159); `scope: project` is skipped (startup.sh:1253). The scope in manifest.yaml:3 is `hybrid`.
- It runs once per agent start (coder_script `startup`, `run_on_start = true`, startup.tf:42-46), not on first CLI use.

Key Takeaways (b):
- install.sh is a boot-time, seed-repo-only installer. It never runs in an arbitrary project and has no hook point for first use in "a project that never had it".
- The only `bmad install` call is line 42; its offline flag is `NPM_CONFIG_OFFLINE=true`, its time limit `timeout 120`, its tool set `claude-code`, module set `bmm`, output folder `_bmad-output`.
- Exit codes are 0 / 1 / 2 as tabled; marker is written only on the success and no-op paths.

## 3. Upstream CLI facts that bound every option (read-only reads of the installed 6.9.0 package)

Package root: `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/`

| File:line | Fact |
|---|---|
| tools/installer/commands/install.js:12-51 | Option list (see section 1.4). No `--global` or `--user` option exists. [CODE-VERIFIED] |
| tools/installer/ui.js:201-210 | `--directory <path>` is expanded (`expandUserPath`) and validated (`validateDirectorySync`), then used as the install root; no prompt when given |
| tools/installer/ui.js:1414-1463 | `validateDirectorySync`: a non-existent path is accepted if the nearest existing parent is writable ("will prompt for confirmation later"); an existing path must be a writable directory. So `--directory ~` passes validation (code read, not run) |
| tools/installer/core/installer.js:1549-1552 + ide/shared/path-utils.js:21 | `findBmadDir(projectDir)` returns `path.join(projectDir, '_bmad')`; `BMAD_FOLDER_NAME = '_bmad'` |
| tools/installer/ui.js:217-259 | If `<dir>/_bmad` exists the "existing install" menu applies; with `--yes` and no `--action` it defaults to quick-update. If not, it is a fresh install |
| tools/installer/ide/platform-codes.yaml:52-57 | `claude-code`: `target_dir: .claude/skills`, `global_target_dir: ~/.claude/skills` |
| platform-codes.yaml:9 (comment) | "`global_target_dir`: (optional) User-home directory for global install" |
| grep of the whole package for `global_target_dir` / `globalTargetDir` / `global_target`, excluding platform-codes.yaml | NO match. So no JavaScript reads `global_target_dir`. **[UNVERIFIED]** that 6.9.0 can do a user-scope skills install through this key (the key exists as data only). Option F depends on it |
| platform-codes.yaml:10 + grep in `tools/installer/**/*.js` | `ancestor_conflict_check` appears only in the header comment (line 10) of the yaml; the code path exists (`ide/_config-driven.js:191-204`, `findAncestorConflict` 943-969) but no platform enables the key, so an ancestor install does not block a child install in 6.9.0 [CODE-VERIFIED by grep of the yaml: one hit, a comment] |
| core/installer.js:1139-1140, 671 | The installer creates `_bmad/_config/` and a scripts dir itself (`fs.ensureDir`), so it makes its own directories rather than needing them to pre-exist [CODE-VERIFIED lines only; full set of created paths not enumerated, see Gaps] |
| tools/installer/commands/ | Also `status.js` and `uninstall.js` exist; NOT run (BMAD CLI RULE) |

### 3.1 What the catalogue welcome text tells the user to do for another repo

manifest.yaml:12-14 says: for any other repo, run from its root `bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output`. That command differs from install.sh:42 in three ways: it has no `NPM_CONFIG_OFFLINE=true`, no `--user-name`, and it applies none of the info/exclude lines (install.sh:32-34), so in another repo BMad's directories appear as untracked files. [CODE-VERIFIED by comparing manifest.yaml:14 with install.sh:42]

Key Takeaways (3):
- Upstream 6.9.0 has no code path that reads `global_target_dir`; option F rests on a data key only [UNVERIFIED as a working feature].
- Option E (`--directory ~`) passes directory validation by code read (ui.js:1414-1463) and would write `~/_bmad` (path-utils.js:21) plus `~/.claude/skills` (platform-codes.yaml:56). Not run (BMAD CLI RULE), so behaviour is [UNVERIFIED].
- The installer creates its own directories; the CLI does not need `_bmad/` to exist first.

## 4. (c) Catalogue slug: manifest, module, profiles, README contract, wiring

### 4.1 `catalogue/bmad/` shape

Glob of `templates/VSCode-AIDev02/image/catalogue/bmad/**` returns exactly `manifest.yaml`, `install.sh`, `module.tf`. [CODE-VERIFIED] This matches the three-file rule (README.md:81-92).

### 4.2 `manifest.yaml` (30 lines)

| Lines | Field | Value |
|---|---|---|
| 1-4 | name / version / scope / install_disposition | `bmad` / `6.9.0` / `hybrid` / `image-baked` |
| 5-7 | display | name `BMad`; summary "opt-in AI-driven agile-development scaffolder CLI. npm package `bmad-method`; on-PATH binary `bmad`..." |
| 8-20 | welcome_message | "BMad is installed ... If this workspace has a seed repo, BMad is already set up there (hidden from git via the repo's info/exclude). For any other repo, run from its root: `bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output`. Quick start: `bmad --version`, `bmad --help`. Repo URL" |
| 21-23 | depends_on / install_script_path / terraform_module_path | `[]` / `./install.sh` / `./module.tf` |
| 24-25 | health_check.command | `bmad --version` |
| 26-29 | discoverability | class `installed-only`, invocation `bmad`, help_command `bmad --help` |

Doc-claim checks for the welcome text:
- "BMad is installed ... (npm package `bmad-method`)": [CODE-VERIFIED] Dockerfile.coder:139, package.json:3.
- "seed repo ... hidden from git via the repo's info/exclude": [CODE-VERIFIED] install.sh:28-34. It only holds when guards 1 and 2 do not intercept (install.sh:22-25): with no seed repo or an existing `_bmad/`, nothing is configured. The text says "already set up" unconditionally: partly misleading for the no-seed case (install.sh:23). 
- The flags in the manual command exist: [CODE-VERIFIED] commands/install.js:12-51.
- Health/discoverability: `bmad --version` is finite and non-interactive: [CODE-VERIFIED] the wrapper execs node and commander prints the version (bmad-cli.js:84); run once this session, output `6.9.0`.
- test-19 requires the invocation token `bmad` and the full help_command `bmad --help` to appear in the welcome text: [CODE-VERIFIED] test-19-catalogue-cli-presence.sh:514-528; welcome text contains `bmad --help` at manifest.yaml:18.

### 4.3 `module.tf` (21 lines)

Only `terraform { required_providers { coder = { source = "coder/coder", version = "~> 2.0" } } }` (lines 4-11) and `variable "agent_id"` with a non-empty validation (lines 13-21). Header comment lines 1-2 say it declares no `coder_app`, `agent_id` kept "so a future launch surface is a clean diff". No resources. [CODE-VERIFIED] This is the zero-`coder_app` pattern (README.md:241-244).

### 4.4 `profiles.yaml`

| Lines | Fact |
|---|---|
| 13-14 | `version: 1`, `default_profile: orca` |
| 15-18 | `orca` profile "Default", slugs `[claude-code, orca, ironclaude, bmad, mcp-bundle-core]` |
| 19-21 | `minimal` profile "Minimal (Claude Code only)", slugs `[claude-code]` |

So `bmad` is in exactly one profile, `orca`; the `minimal` profile has no bmad. [CODE-VERIFIED] Header comment lines 1-12 (single source of truth for startup §9, creation form, and Terraform `local.active_slugs`): checked against `modules.tf:19,33` (yamldecode) and `startup.sh:1081` (reads profiles.yaml) = [CODE-VERIFIED]; the form side is hand-copied, parameters.tf:92-93 says "derived by hand FROM image/catalogue/profiles.yaml".

Comment line 1 says the file is `templates/VSCode-AIDev02/catalogue/profiles.yaml (baked to /catalogue/profiles.yaml)`: the real path is `templates/VSCode-AIDev02/image/catalogue/profiles.yaml`. **[STALE DOC]** (path moved under `image/`, see main.tf:67-71); the bake is [CODE-VERIFIED] Dockerfile.coder:593.

### 4.5 Terraform wiring

| File:line | Fact |
|---|---|
| modules.tf:19-20 | `_manifest = yamldecode(file("${path.module}/image/catalogue/profiles.yaml"))` |
| modules.tf:29, 33 | `_selected = data.coder_parameter.profile.value`; `active_slugs = local._profiles[local._selected].slugs` |
| modules.tf:50-54 | `module "bmad" { source = "./image/catalogue/bmad"; count = contains(local.active_slugs, "bmad") ? 1 : 0; agent_id = coder_agent.main.id }` |
| parameters.tf:99-119 | `coder_parameter "profile"`, default `orca`, `mutable = true`; option "Default" (value `orca`, description names "BMad", line 110) and "Minimal (Claude Code only)" (value `minimal`) |
| profile.tf:18-20 | `coder_env "aidev_profile"` exports `AIDEV_PROFILE` for startup §9 |
| startup.sh:715 | `aidev_cat_root="${AIDEV_CAT_ROOT:-/catalogue}"` |
| Dockerfile.coder:592-593 | `COPY --chown=0:0 catalogue /catalogue` (last COPY in the file; the file is 595 lines) |
| main.tf:73-74, 104-107, 111, 148-150 | `catalogue_sha256` hashes every file under `image/catalogue/**`; it feeds `image_inputs_sha256`, the image tag (`:sha-<16>`) and the `docker_image` rebuild trigger |
| main.tf:80-101 | `image_input_files` lists every COPY source other than the catalogue; main.tf:77-79 says test-67 fails CI when a COPY source is missing from the list |

The `modules.tf`, `parameters.tf`, `main.tf`, `startup.tf` and `profile.tf` files sit in `templates/VSCode-AIDev02/`, OUTSIDE `image/`; only `image/**` is the Docker build context (main.tf:119) and the image hash covers only `image_input_files` + `image/catalogue/**` (main.tf:104-107). So a change to a `.tf` file outside `image/` does not retag the image. [CODE-VERIFIED]

### 4.6 Catalogue README contract (`image/catalogue/README.md`, 605 lines) cross-checked

| Claim (README line) | Result |
|---|---|
| Exactly three files per slug; no README or nested dirs (81-92) | [CODE-VERIFIED] for bmad (Glob). Enforcement by test-1 not read: **[UNVERIFIED]** |
| Slug name = manifest `name` = dir name (94-95) | [CODE-VERIFIED] (`bmad`) |
| `scope` enum workspace/hybrid/project (110) | [CODE-VERIFIED] startup.sh:1158-1159, 1253, 1262 |
| install_disposition `image-baked`/`runtime-network` (116) | consistent with manifest.yaml:4 |
| `installed-only` needs `invocation` and `help_command`; welcome must contain both (126) | [CODE-VERIFIED] test-19:514-528 |
| install.sh MUST be idempotent with marker + affordance short-circuit (179-183) | bmad/install.sh has no such short-circuit (section 2) - partially unmet by the shipped slug |
| "startup §9 invokes scripts as `( source ~/.aienv && bash install.sh )`" (180-183) | [CODE-VERIFIED] only for bmad (startup.sh:1175). Other slugs run through `aidev_cat_install` in a private setsid shell (startup.sh:705-708, 1177-1181) -> README statement is **[STALE DOC]** for non-bmad slugs |
| test-5 `ALLOWED` array `{code-server, claude-code, vibe-kanban, orca, orca-pair}` (239) | [CODE-VERIFIED] test-5-coder-app-allowlist.sh:29 |
| Walkthrough paths `/config/workspace/Coder/catalogue/...` and `scripts/startup.sh` (348, 408, 598) | `catalogue/` at repo root does not exist (Glob `catalogue/**` empty); the slugs live under `templates/VSCode-AIDev02/image/catalogue/`. **[STALE DOC]** / [CODE-CONTRADICTED] |
| Relative links `../../../orca-build/provenance.md`, `../../../docs/operations/aidev02-operator.md` (32, 64) | From `templates/VSCode-AIDev02/image/catalogue/`, `../../../` is `templates/`; `templates/orca-build/provenance.md` does not exist (the files are at repo-root `orca-build/` and `docs/`). **[STALE DOC]** link depth |
| Reference links `../.github/contract-tests/`, `../templates/VSCode-AIDev02/providers.tf` (594-596) | Resolve under `image/`, where neither exists. **[STALE DOC]** |
| Claim README.md:195-199 "Where the binary actually comes from is your choice" | consistent with bmad (image-baked) |

Other stale text found while mapping: startup.tf:30 says "This is the ONLY runtime coder_script in the template", but `coder_script` resources also exist at modules.tf:82, main.tf:220 and :233, orca/module.tf:58 and :79, vibe-kanban/module.tf:40. **[STALE DOC]** / [CODE-CONTRADICTED] (grep of `resource "coder_script"`).

Key Takeaways (c):
- bmad is a hybrid-scope, image-baked, installed-only slug present only in the `orca` profile; `minimal` has no bmad, so any option anchored in the bmad slug does nothing for `minimal` workspaces.
- Anything under `image/` (Dockerfile, catalogue, startup.sh, workspace_defaults, etc.) is baked in and retags the image; anything in the root `.tf` files is template-push-only.
- The catalogue contract has no field for "run when the CLI is first used"; every hook it offers (install.sh, health_check, welcome_message) is boot-time or read-only.

## 5. (d) spec2-health.sh: bmad states `Installed-not-Configured` and `Configured`

File: `templates/VSCode-AIDev02/image/scripts/lib/spec2-health.sh` (637 lines).

| Lines | Fact |
|---|---|
| 17-18 | Header: configured_state in {Configured, Partially, Installed-not-Configured, Not-Installed}; `configured_missing` empty except for Partially |
| 74-81 | `spec2_health_requirements`: `bmad` requires the single name `seed-config` (line 77) |
| 99-114 | `spec2_health_observed bmad`: reads the first line of `~/.aidev/status/seed-repo-path` (100); only if that path is a git work tree (101-102) it emits `seed-config` when `<seed>/_bmad/_config/manifest.yaml` is a file (103-104), else when any git-TRACKED `.claude/skills/bmad-*/SKILL.md` exists on disk (106-111) |
| 141-168 | `spec2_health_classify <slug> <state>`: no marker `~/.aidev/installed/<slug>` -> `Not-Installed`; state not `healthy` -> `Installed-not-Configured`; otherwise compare required vs observed: all found -> `Configured`; some -> `Partially`; none -> `Installed-not-Configured` |
| 172-192 | `spec2_health_validate_configured`: `Partially` is valid only when the slug has more than one required name (line 181: `sh2_total -gt 1`). bmad has one, so bmad can NEVER be `Partially` |
| 216-239 | `spec2_health_read_configured`: strict reader; the record must carry the CURRENT boot's invocation id (230), so a record from a previous boot is not accepted |
| 302-317 | `spec2_health_record` calls `spec2_health_classify` (317) |
| 373-456 | `spec2_health_run` runs the manifest `health_check.command` (`bmad --version`, manifest.yaml:25) under a timeout and writes the record (456) |
| 518-534 | `reprofile_read` rejects any `bmad` row (line 529) |
| 543-578 | `readiness_write`: a deselected `bmad` is always `not-selected` (562-565); a selected slug takes its state from the record (569-571) |

Where it is called: startup.sh:1187 (`aidev_spec2_health_run`) right after a successful install.sh in §9 of each boot; startup.sh:1138, 1227, 1240, 1266 write failure records. [CODE-VERIFIED] So states are recomputed once per agent start, not on CLI use.

State table for bmad (derived from the code above):

| Situation at boot | Marker | Observed | State |
|---|---|---|---|
| bmad not in profile (minimal) | none written by §9 (bmad marker is never removed by §9, startup.sh:1117) | n/a | readiness `not-selected` (spec2-health.sh:562-565) |
| No seed repo recorded | written (install.sh:23 -> 58) | none | `Installed-not-Configured` (test-57:449-452 asserts this fixture) |
| Seed repo with `_bmad/` only, no manifest | written | none | `Installed-not-Configured` (test-57:419) |
| Seed repo with `_bmad/_config/manifest.yaml` (installed by install.sh or earlier) | written | `seed-config` | `Configured` (test-57:323) |
| Seed repo tracking `.claude/skills/bmad-*/SKILL.md` | written | `seed-config` | `Configured` (test-57:427) |

What a first-use install would do to the states:
- States look ONLY at the SEED repo (spec2-health.sh:100-111). A first-use install in any other project, or at `~`, changes nothing the states read. The state stays what boot computed. [CODE-VERIFIED]
- A first-use install in the seed repo itself would make `Installed-not-Configured` (seed w/o BMad) become `Configured`, but only at the NEXT boot's §9 (health run at startup.sh:1187; reader requires the current invocation id, spec2-health.sh:230). Within the running session, the on-disk record from this boot is not updated. [CODE-VERIFIED by reading]
- Because bmad has one required name, a first-use mechanism cannot produce `Partially`.
- Readiness line: `readiness_summary` prints "Catalogue not configured: <slugs>" when any selected slug is not Configured (spec2-health.sh:620-635). So a seed repo without BMad keeps showing bmad as not configured for the whole boot, even after a first-use install elsewhere. This is the existing behaviour a hook/skill option would sit beside; none of options B, C, D touches this reader unless it also writes into the seed repo.

Key Takeaways (d):
- `Configured` for bmad = seed repo has `_bmad/_config/manifest.yaml` or tracked bmad skills; nothing else counts.
- Health is boot-time only; a first-use install cannot change state mid-session.
- Any design that installs outside the seed repo is invisible to health and readiness.

## 6. (e) Hook points for options B, C and D (plus E and F facts)

### 6.0 Facts every option shares

| Fact | Evidence |
|---|---|
| Everything under `templates/VSCode-AIDev02/image/` is the Docker build context; the image tag and the `docker_image` rebuild trigger hash `Dockerfile.coder`, the listed COPY sources and every file under `image/catalogue/**` | main.tf:73-74, 80-107, 111, 119, 148-150 |
| Root `.tf` files (`modules.tf`, `main.tf`, `parameters.tf`, `startup.tf`, `profile.tf`) are NOT hashed into the image tag | main.tf:104-107 (hash inputs), 119 (context) |
| `coder update` is the route that rebuilds after a hash change | main.tf:77-78 (comment) |
| HOME is the per-workspace named volume `coder-<workspace id>-home` mounted at `/home/coder` | main.tf:174-176, 594-596 |
| Image seed files under `/etc/skel` reach HOME only copy-if-absent at boot (§6); "Persistent homes are not migrated" | Dockerfile.coder:543-545; startup.sh:191, 275, 283-289 |
| §9 runs every slug's `install.sh` at every agent start in `LC_ALL=C` sort order (bmad before ironclaude) | startup.sh:692-701, 1174-1182; startup.tf:42-46 |
| Version-pin strings that Renovate and the upstream monitor must keep seeing: `npm install -g bmad-method@X.Y.Z` in Dockerfile.coder, `bmad-method@X.Y.Z` in bmad/install.sh, `^version: X.Y.Z$` in bmad/manifest.yaml | .github/upstream-monitor/expected.txt:6-8; renovate-global.json5:47-48, 54-55 |
| Spec2 health observes only the SEED repo; a user-level mechanism is invisible to it unless `spec2_health_requirements` is extended | spec2-health.sh:74-81, 99-114 |

### 6.1 Option B: user-level bootstrap skill or command under `~/.claude/skills`

No code writes a bmad skill to HOME today (case-insensitive grep of `bmad` over the root `*.tf` files, `image/workspace_defaults`, `image/bin`, `image/lib`, `image/aienv.skel`, `image/aienv.d` and `image/etc` returned only modules.tf:50-52 and parameters.tf:110; the only other bmad code is under `image/catalogue/bmad/`, `image/Dockerfile.coder` and the checks in `.github/contract-tests/`). Three concrete delivery points exist:

| Variant | Exact place | Rebuild / push / runtime | What persists in HOME | Contract statement stretched |
|---|---|---|---|---|
| B1 skill written by the slug installer | New step in `catalogue/bmad/install.sh` between the end of the if/elif/else (line 55) and the marker write (line 58). The script has no functions, so the hook is a line range. Skill text must be an inline heredoc (a separate file inside `catalogue/bmad/` breaks the three-file rule) | (i) image rebuild: install.sh is under `image/catalogue/**`, so `catalogue_sha256` changes (main.tf:74). The catalogue COPY is the LAST COPY of the Dockerfile (Dockerfile.coder:593), so earlier layers are untouched in principle; the cache effect is [UNVERIFIED]. Takes effect on the next agent start after `coder update` | `~/.claude/skills/<name>/SKILL.md`, rewritten every boot unless guarded copy-if-absent; survives restarts; per workspace | README.md:81-92 (three files, no nesting) if the content leaves install.sh; install.sh purpose in its own header (install.sh:2-3: verify CLI + seed-repo install); manifest `display.summary` "opt-in" (manifest.yaml:7); README.md:204-216 VERIFY-ONLY pattern |
| B2 skill seeded from `/etc/skel` | New `COPY` of the skill file to `/etc/skel/.claude/skills/<name>/SKILL.md` (pattern: Dockerfile.coder:496), a new name in `image_input_files` (main.tf:80-101; test-67 per main.tf:78-79, test not read), and a `seed_if_absent` line in startup.sh §6 (pattern: startup.sh:275) | (i) image rebuild, plus startup.sh edit (also under `image/`) | same path, created once, then user-owned (never overwritten) | Not slug-gated: §6 runs for the `minimal` profile too (bmad is absent from `minimal`, profiles.yaml:19-21); profile gating would need an extra check. Catalogue contract not touched |
| B3 skill written by a root-level `coder_script` | New `resource "coder_script"` in `modules.tf` (outside `image/`) count-gated on `contains(local.active_slugs, "bmad")`, same pattern as `coder_script "orca_retirement"` (modules.tf:82-109, heredoc, `run_on_start = true`) | (ii) template push only; no image hash change (main.tf:104-107). Runs on the next agent start after the workspace is updated to the new template version | same path as B1 | Catalogue README describes `module.tf` as `coder_app` + `variable agent_id` (README.md:218-264) and says nothing about `coder_script`; root-level scripts keep the three-file slug untouched but split bmad logic across two places |

Other precedents for user-level writes by catalogue installers: orca/install.sh:18-42 installs `orca-cli` and `orchestration` skills into `~/.agents/skills` and `~/.claude/skills` (background, 300 s `timeout`), and modules.tf:98-106 removes exactly those links when `orca` is deselected. bmad is EXCLUDED from §9's deselect cleanup (startup.sh:1114-1117), so a user-level bmad skill would stay after switching to `minimal` unless new cleanup is added (as orca_retirement does for orca). [CODE-VERIFIED by reading]

Instruction-text channel (alternative to a skill): `aidev_claude_md_block_sync` re-syncs a marked block of `/etc/skel/.claude/CLAUDE.md` into `~/.claude/CLAUDE.md` every boot (startup.sh:1282-1285; claude-md-block.sh:2-19). Its markers are hard-coded to `SUPERCLAUDE_CODEGRAPH_BEGIN/END` (claude-md-block.sh:23), so a BMad block needs a second marker pair or a generalised function. `workspace_defaults/CLAUDE.md` has no BMad text today (grep count 0).

### 6.2 Option C: image-level `bmad` CLI wrapper change (or a new wrapper command)

| Item | Detail |
|---|---|
| Exact place | `Dockerfile.coder:142`, the `{ echo "#!/bin/sh"; echo "exec \"$node_bin\" \"$cli\" \"\$@\""; } > /usr/local/bin/bmad` group inside the root layer at lines 136-145. Precedent for a multi-line root-owned wrapper: the `claude` wrapper printf block at Dockerfile.coder:116-130 (comment lines 105-106 say test-60 extracts it by its printf block; test-60 not read, so what it pins is [UNVERIFIED]) |
| Rebuild class | (i) always. `Dockerfile.coder` is in `image_input_files` (main.tf:81), so the tag changes. The BMad layer sits at lines 136-145 of a 595-line file; Docker rebuilds the layers after a changed layer (standard Docker behaviour, not tested here), which includes the SHA-pinned release-binary downloads (Dockerfile.coder:147 onward) built through the host-network legacy builder (main.tf:122-145). A separate stable wrapper plus a late-COPY script would shrink that, but is still (i) |
| New wrapper command (for example another file in `/usr/local/bin`) | Same (i). Not a catalogue slug, so no slug contract. It would need a mention in `manifest.yaml` welcome text to be discoverable (manifest.yaml:12-14), which also changes the catalogue hash |
| Persistence in HOME | None. `/usr/local/bin/bmad` is root-owned (USER root layer, Dockerfile.coder:136; chmod 0755 at :143). Only what the wrapper writes at runtime would persist (the project directory, or `~` if it wrote there) |
| Contract statements and checks it must keep | `health_check.command: bmad --version` must stay finite and non-interactive (manifest.yaml:25; README.md:395-400). `discoverability.invocation: bmad` and `help_command: bmad --help` (manifest.yaml:28-29; test-19:485-528, first-token check at :820). install.sh:18 only checks `command -v bmad`, and install.sh:42 calls `bmad install ...` through the wrapper, so the wrapper must pass `install` through unchanged. Keep the literal `npm install -g bmad-method@X.Y.Z` (expected.txt:6; renovate-global.json5:48) |
| Limit (inference) | A wrapper runs only when something executes `bmad`. It cannot run when a user invokes a BMad skill inside Claude Code in a project, because no `bmad` process is involved in loading a skill. This rests on how BMAD skills work and is [UNVERIFIED] here |
| Stretches | Manifest says the CLI is "opt-in" (manifest.yaml:7) and the Dockerfile comment calls the wrapper a pure exec stand-in for the node bin (Dockerfile.coder:134-135); adding project-modifying behaviour to a wrapper that today only execs changes what `bmad <anything>` means image-wide, including for the `minimal` profile where bmad is not selected (profiles.yaml:19-21), because the wrapper is baked for every profile |

### 6.3 Option D: Claude Code user-level SessionStart or UserPromptSubmit hook

| Variant | Exact place | Rebuild / push / runtime | Persistence | Findings from the code |
|---|---|---|---|---|
| D1 hook written to `~/.claude/settings.json` by bmad/install.sh | New jq-merge step in `catalogue/bmad/install.sh` before the marker (line 58). Model it on ironclaude/install.sh:100-136 (malformed-file refusal at :100, symlink preservation :68-86 and :105-109, before/after hook preservation :110-136) | (i) image rebuild (catalogue hash) plus restart after `coder update` | The hook entry lives in `~/.claude/settings.json` in HOME; shared with IronClaude and Orca writers | (1) IronClaude's configured-check treats any hook command containing `/.claude/hooks/` as an IronClaude hook (ironclaude/install.sh:15-16, 25, 141; spec2-health.sh:90-91). A bmad hook whose command contains that substring would make IronClaude's `hook` observation and `has_ic_hooks` true without IronClaude. (2) ironclaude/install.sh:139 admits there is no lock against the parallel Orca writer of settings.json; `superclaude install` is run with `--force` unless the same sha was already configured (ironclaude/install.sh:93-97, 122) and replaces a symlinked settings.json with a regular file (ironclaude/install.sh:69), and the script FAILS if pre-existing hook entries disappear (ironclaude/install.sh:133-136). Since bmad sorts before ironclaude (startup.sh:700), a bmad hook already in place would be one of the entries that check protects, so a drop would fail the ironclaude slug, not the bmad one |
| D2 image-baked managed-settings drop-in | New file under `image/etc/claude-code/managed-settings.d/` (existing: `10-retention.json` with `cleanupPeriodDays`), a COPY like Dockerfile.coder:500-501 and an entry in `image_input_files` (existing entry main.tf:87) | (i) image rebuild | Nothing in HOME (root-owned `/etc/claude-code`) | Image-wide, not slug-gated: applies to the `minimal` profile too. Whether `managed-settings.d` accepts hooks is a Claude Code feature not checked here: [UNVERIFIED]. Never touched by IronClaude's `/.claude/hooks/` predicate, which reads `~/.claude/settings.json` only |
| D3 hook merged by a root-level `coder_script` | `modules.tf`, pattern `coder_script "orca_retirement"` (modules.tf:82-109); `jq` is in the image (Dockerfile.coder:590 checks `/usr/bin/jq`) | (ii) template push only | same as D1 | Same two risks as D1; the race with the other settings.json writers is now across two boot scripts |

Catalogue statements stretched by D1/D3: install.sh scope (one seed repo, install.sh:21-25); manifest "opt-in" wording (manifest.yaml:7), because a hook acts in every project without the user running anything; blast radius is every Claude Code session of the user. [CODE-VERIFIED for the manifest wording; the blast-radius statement is an inference from where settings.json lives (spec2-health.sh:86)]

### 6.4 Summary table (B, C, D)

| Option | Hook point (file:line) | Needs (i) image rebuild | Needs (ii) only template push | Needs (iii) per-workspace runtime action only | Persists in HOME |
|---|---|---|---|---|---|
| B1 skill from install.sh | bmad/install.sh between 55 and 58 | yes | no | after update, restart | `~/.claude/skills/<name>/` |
| B2 skill from `/etc/skel` | Dockerfile.coder (new COPY near :496), main.tf:80-101, startup.sh:275 pattern | yes | no | restart | same, created once |
| B3 skill from root `coder_script` | modules.tf (pattern :82-109) | no | yes | update + restart | same |
| C wrapper | Dockerfile.coder:142 | yes | no | none (the user runs `bmad`) | nothing from the wrapper itself |
| D1 settings.json hook from install.sh | bmad/install.sh before :58 (model ironclaude/install.sh:100-136) | yes | no | update + restart | `~/.claude/settings.json` |
| D2 managed-settings drop-in | image/etc/claude-code/managed-settings.d/, Dockerfile.coder:500-501 pattern | yes | no | restart | nothing |
| D3 settings.json hook from root `coder_script` | modules.tf (pattern :82-109) | no | yes | update + restart | `~/.claude/settings.json` |

### 6.5 Facts for options E and F (not requested to map, recorded because they bound the comparison)

- E, `bmad install --directory ~`: the option exists (install.js:14) and `~` passes directory validation by code read (ui.js:1414-1463). `findBmadDir` would give `~/_bmad` (installer.js:1549-1552; path-utils.js:21) and the claude-code target is relative to the install directory (`.claude/skills`, platform-codes.yaml:56), so it would write into the HOME volume with no image change: class (iii). Behaviour was not run: [UNVERIFIED]. It is a global-style install, which the owner did not ask for.
- F, upstream `global_target_dir`: the key exists only as data in platform-codes.yaml (e.g. :57 for claude-code); no code in the 6.9.0 package reads it (whole-package grep). Using it would mean a newer upstream version, i.e. changing the pin at Dockerfile.coder:139, `install.sh:18` text, `manifest.yaml:2`, which keeps the Renovate-visible strings (expected.txt:6-8) and rebuilds the image: class (i). The update box printed during this research reports 6.12.4 as available (bmad-cli.js:31-47 output); what that version does is [UNVERIFIED].

Key Takeaways (e):
- The cheapest classes are B3 and D3 (root `coder_script`, template push only), because root `.tf` files are not in the image hash; everything under `image/` (install.sh, Dockerfile, startup.sh, /etc/skel content, managed settings) forces an image rebuild.
- Only B (skill) and D (hook) can act where Claude Code is used; C (wrapper) fires only when `bmad` itself is executed.
- The strongest cross-slug hazard found is D's collision with IronClaude's `/.claude/hooks/` predicate and the unlocked settings.json writers.
- None of B, C, D changes bmad health/readiness, because those states read only the seed repo (spec2-health.sh:99-114).

## Gaps and Questions

### UNVERIFIED items (14)

| # | Item | Why unverified |
|---|---|---|
| U1 | Dockerfile.coder:134-135 claim that NVM node is not on the default PATH | Comment only; no shell was run with the image PATH |
| U2 | A newer upstream `bmad-method` 6.12.4 exists | Seen only in the CLI's update box; not checked against the registry |
| U3 | Why the "Update Available" box printed although `NPM_CONFIG_OFFLINE=true` was set | Cause not investigated (npm cache is one possibility) |
| U4 | That `global_target_dir` works as a user-scope install in 6.9.0 (option F) | No JavaScript in the 6.9.0 package reads the key; it is data in platform-codes.yaml only |
| U5 | What `bmad install --directory ~` actually writes (option E) | Install not allowed to run (BMAD CLI RULE); code read only |
| U6 | The complete list of paths `bmad install` creates in a project | Only install.sh:32/46 and installer.js:671, 1139-1140 were read; the full installer was not traced |
| U7 | That test-1 enforces the exactly-three-files rule | README claim; test-1 not read (the bmad dir does hold exactly three files) |
| U8 | Docker layer-cache behaviour when only the last COPY (Dockerfile.coder:593) changes, and the rebuild cost of changing the BMad layer | Standard Docker semantics assumed; not tested, builder is the provider's legacy builder (main.tf:122-145) |
| U9 | That `/etc/claude-code/managed-settings.d/*.json` accepts hooks (option D2) | Claude Code feature, not checked in this task; existing file only sets `cleanupPeriodDays` |
| U10 | The exact Coder flow from template push to a running workspace (push, `coder update`, restart) | Only the comment at main.tf:77-78 was read |
| U11 | What test-60 (claude wrapper pin) and test-67 (COPY sources vs `image_input_files`) assert | Named in comments (Dockerfile.coder:105-106; main.tf:77-79); the scripts were not read |
| U12 | That a `bmad` wrapper cannot run when a BMad skill is invoked inside Claude Code | Inference; depends on how BMAD skills execute |
| U13 | That user-level skills and hooks in HOME apply to every project (blast radius) | Claude Code semantics not checked here; settings.json location read at spec2-health.sh:86 only |
| U14 | That the task's "OD-1" is the same label used in this repo | test-57-catalogue-configure.sh:10, 992, 1034 and startup.sh:1114 use "OD-1" / "owner-decision" for different matters; the task's OD-1 text was not in my scope files |

Fix cycle 1 pointer (findings 2 and 3): U8 (layer-cache behaviour) is joined by U15-U20 and CODE-CONTRADICTED item C8 in the `Addendum (fix cycle 1): Sysbox image-layer headroom gate (Finding 3)` at the end of this file (current layer count 68 of 70, read from CI logs). U7 (test-1 enforces the three-file rule) is closed by the finding 2 addendum in `04-pinned-tests-57-46-19.md` (A.7: `test-1-catalogue-shape.sh:25, 43-67`, verified). U11 (test-60, test-67) is closed by the same addendum (A.2, A.3).

### CODE-CONTRADICTED items

| # | Claim | What the code shows |
|---|---|---|
| C1 | install.sh:18 message: "`/usr/local/bin/bmad` symlink" | Dockerfile.coder:134-143 and /usr/local/bin/bmad:1-3: a 2-line `#!/bin/sh` wrapper, not a symlink |
| C2 | README.md walkthrough paths `/config/workspace/Coder/catalogue/...` (348, 408-409) | No `catalogue/` at repo root; the catalogue is `templates/VSCode-AIDev02/image/catalogue/` |
| C3 | README.md relative links 32, 64, 594-596 | Resolve to `templates/orca-build/...`, `image/.github/...`, `image/templates/...`, none of which exist |
| C4 | README.md:180-183 "startup §9 invokes scripts as `( source ~/.aienv && bash install.sh )`" | True only for bmad (startup.sh:1175); other slugs run through `aidev_cat_install` in a private setsid shell (startup.sh:705-708, 1177-1181) |
| C5 | startup.tf:30 "This is the ONLY runtime coder_script in the template" | Also modules.tf:82, main.tf:220 and :233, orca/module.tf:58 and :79, vibe-kanban/module.tf:40 |
| C6 | profiles.yaml:1 path `templates/VSCode-AIDev02/catalogue/profiles.yaml` | Real path is `templates/VSCode-AIDev02/image/catalogue/profiles.yaml` |
| C7 | manifest.yaml:12 "BMad is already set up there" (seed repo) | Only when install.sh guards pass: with no seed repo (install.sh:22-23) or an existing `_bmad/` that is not a full install (install.sh:24-25) nothing is configured |

### Open questions for the builder

1. Should a first-use mechanism also cover the `minimal` profile? bmad is not in it (profiles.yaml:19-21), and root-level or image-wide mechanisms (C, D2, B2) are not slug-gated unless extra checks are added.
2. Should the deselect behaviour for a user-level bmad artefact follow orca (cleanup script, modules.tf:82-109) or bmad's current rule (marker never removed, startup.sh:1114-1117)?
3. Should the failed-first-install behaviour (install.sh:41, 24) be revisited if first use can also create `_bmad/`? A partial `_bmad/` is today skipped, never repaired.
4. Which approach is acceptable for the Renovate-visible strings if install.sh is rewritten (expected.txt:6-8)?

## Stale Documentation Found

- **[STALE DOC]** install.sh:18 error text says "symlink"; the CLI is a wrapper script (Dockerfile.coder:134-143).
- **[STALE DOC]** profiles.yaml:1 path comment omits `image/`.
- **[STALE DOC]** catalogue README.md paths and relative links in lines 32, 64, 348, 408-409, 594-596, and the `( source ~/.aienv && bash install.sh )` statement at 180-183 (true only for bmad).
- **[STALE DOC]** startup.tf:30 "ONLY runtime coder_script".
- Dockerfile.coder:134-135 PATH claim: [UNVERIFIED], not known stale.
- Welcome text manifest.yaml:12 reads unconditionally; see C7.

## Summary

The `bmad` command is a two-line root-owned wrapper that only `exec`s node on the pinned `bmad-method@6.9.0` CLI (Dockerfile.coder:139-143); it has no first-use logic, and the CLI itself creates `_bmad/` on its own. The catalogue slug `bmad` installs only into the one seed repo, once per agent start, with guards that skip existing `_bmad/` and with a status-unchanged check (install.sh:21-55); the welcome text sends the user to a manual command for any other repo (manifest.yaml:12-14). Health and readiness for bmad look only at the seed repo (spec2-health.sh:99-114), so none of options B, C or D changes them. Root-level `coder_script` variants (B3, D3) need only a template push, while anything under `image/` (install.sh, Dockerfile, startup.sh, /etc/skel, managed settings) retags the image and needs a rebuild; options E and F are bounded by facts in section 6.5. The main hazards found are D's overlap with IronClaude's `/.claude/hooks/` predicate, the unlocked settings.json writers, the Renovate-visible version strings, and the fact that a wrapper cannot fire on skill invocation.

## Addendum (fix cycle 1): Sysbox image-layer headroom gate (Finding 3)
**Status:** Complete
**Date:** 2026-11-08

Scope: layer cost of options B1, B2, B3, C, D1, D2, D3 (defined in section 6 above) against the 70-layer CI gate. Method notes are given per item below.

### A1. The gate itself [CODE-VERIFIED]

- `.github/workflows/coder-ci-aidev02-contract.yml:1016-1029`, step "Check Sysbox image-layer headroom": `layers=$(docker image inspect "$IMAGE_TAG" --format '{{len .RootFS.Layers}}')` (:1024), prints `Sysbox image layers: %s (budget: 70)` (:1025), and fails with `::error::AIDev02 exceeds its Sysbox image-layer budget or layer inspection is invalid.` when the count is not a positive integer or `layers > 70` (:1026-1028). So 70 passes and 71 fails.
- The comment at :1022-1023 says "76 layers started, 78 hit Sysbox's relative overlay-path bug. Keep margin; this is not a universal Docker limit." The 70 limit is therefore a chosen margin on a host-specific bug, not a Docker limit.
- The gate is the only place the budget is enforced in that workflow (Grep of `headroom|layers|70` over the workflow file: hits at :499 (timeout comment, unrelated), :1016, :1022-1029, :1067 (unrelated "COPY layers running under USER 1000"), :1365 (unrelated test name)).

### A2. Current layer count [CODE-VERIFIED from CI log; method stated]

- Method: read-only `gh run list --repo IronbellyOrg/Coder --workflow coder-ci-aidev02-contract.yml --limit 8`, then `gh run view <id> --repo IronbellyOrg/Coder --log` filtered with grep for `Sysbox image layers`. Nothing was written or triggered.
- Run 42346410588 (event push, branch main, headSha `f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1`, created 2026-11-07T06:18:24Z, conclusion success), job "AIDev02 contract tests (dind-sidecar)", log line: `Sysbox image layers: 68 (budget: 70)`. `git -C <worktree> rev-parse HEAD` returns the same sha `f1ac0c93...`, so this count belongs to the exact Dockerfile.coder in this worktree.
- Run 42384399575 (push, main, headSha `1371ef5b8716ed7a1cdaacd0cfb6947979dac75d`, 2026-11-07T15:02:14Z, success), step "Check Sysbox image-layer headroom", log line: `Sysbox image layers: 68 (budget: 70)`. Same count on the newest main run.
- **Current count: 68 of 70; free layers: 2** (the gate passes at 70). The earlier decision record `.dev/decisions/codegraph-bake-layer/merged-decision.md:25-26` also says "68 of 70 on main" and "Headroom left: two layers" (a document; it agrees with the logs above).
- Only the dind-sidecar job's log was read. The Sysbox runtime arm of the matrix was not read; the image is built once per tag, so the count is expected to be identical: [UNVERIFIED].

### A3. Independent count from Dockerfile.coder [CODE-VERIFIED count of instructions; base-layer share is an inference]

- Method: Grep `^\s*(FROM|RUN|COPY|ADD)\b` over `templates/VSCode-AIDev02/image/Dockerfile.coder`: 61 matching lines = 1 `FROM` (:6, `codercom/code-server:4.121.0-trixie@sha256:ea5f42d9...`) + 60 layer-creating instructions. Of the 60: RUN at :12, 29, 56, 80, 88, 108, 137, 152, 163, 175, 188, 199, 208, 219, 239, 294, 360, 370, 391, 408, 448, 458, 473, 514, 521, 531, 538, 550, 573, 576, 589 (31 RUN); COPY at :185, 292 (`COPY --from=ghcr.io/astral-sh/uv:0.11.8`), 368, 369, 453, 461, 465, 469, 480, 485, 488, 492, 496, 500, 504, 507, 510, 517, 524, 527, 534, 541, 547, 549, 575, 582, 586, 587, 593 (29 COPY). There is no `ADD` and no second `FROM` stage. `USER`, `ENV` and `ARG` lines add no layer (Dockerfile.coder:273 says "ENV is metadata only (no image layer)").
- 68 (CI) minus 60 (instructions) = 8, which would be the layers of the base image `codercom/code-server`. That 8 is an inference: the base image's own layer count was not read, and whether every RUN (for example the check-only RUN at :589-590) really produces a layer was not tested. The CI number 68 is the authority; the instruction count is only a cross-check.

### A4. The two Dockerfile comments [CODE-VERIFIED text; CODE-CONTRADICTED for one]

- `Dockerfile.coder:229`: "codegraph v1.6.2 rides this layer too (no new layer: the Sysbox budget has two spare, see .dev/decisions/codegraph-bake-layer/merged-decision.md)". This matches the measured 68 of 70 (A2).
- `Dockerfile.coder:468`: "They share one COPY layer because the Sysbox image-layer budget (70) has no headroom." Also :459-460: "keep image layers below the host's Sysbox overlay-path limit; remove the CI headroom ceiling after upstream relative-path handling is fixed."
- Reconciliation: the two comments describe different moments. `_bmad-output/planning-artifacts/architecture/architecture-Coder-orca-catalogue-bundle-2026-09-24/ARCHITECTURE-SPINE.md:93` says "the Sysbox image-layer budget is 70 and `main` is at 70" (older, zero spare), while the logs (A2) and the decision record say 68, i.e. two spare. So :468 is [CODE-CONTRADICTED] as a statement about the current state (68 is not zero headroom); it is correct only as a policy ("fold into existing COPY/RUN"), which `docs/development-guide.md:66` repeats ("layer budget on Sysbox is tight (70) - fold into existing RUN/COPY"). The honest summary for the builder: 2 free layers today, no safety margin intended beyond them, and project policy is to spend none.
- I did not edit Dockerfile.coder (read-only scope). Aligning the two comments is a product-code change for the later plan, not for this research.

### A5. Layer cost per option [mixed; each row states its basis]

Rule used: a layer is created by each new RUN, COPY or ADD. A change inside an existing RUN, inside an existing COPY's source set, or inside a file that an existing COPY already ships adds none. Free layers: 2 (A2).

| Option | Layer cost as written in section 6 | Basis | Zero-layer form, if one exists |
|---|---|---|---|
| B1 skill written by `catalogue/bmad/install.sh` | 0 | The file is shipped by the existing `COPY --chown=0:0 catalogue /catalogue` (Dockerfile.coder:593). [CODE-VERIFIED] | n/a |
| B2 skill seeded from `/etc/skel` | +1 as described (a new COPY to `/etc/skel/.claude/skills/<name>/SKILL.md`, pattern :496) | Each COPY at :496, :500, :504, :507, :510 has a single fixed destination, so a different destination needs its own COPY. [CODE-VERIFIED] | 0 if the file rides an existing multi-file COPY whose destination is `/usr/local/lib/aidev/` (:469, :480-482, :547-548) and `startup.sh` §6 seeds it with `seed_if_absent` into `~/.claude/skills/<name>/SKILL.md`. Precedent: Dockerfile.coder:543-545 ("ride this COPY (layer budget) and are seeded copy-if-absent by startup §6") and startup.sh:291-293 (codex, opencode, pi configs, copied from `/usr/local/lib/aidev/`). [CODE-VERIFIED precedent; the B2 use of it is a proposal, not tested]. Test-67 still needs the new source in `image_input_files` (test-67-image-inputs-cover-copies.sh:7-12; main.tf:80-101). Folding into the :547-548 COPY is allowed by test-60 (reconciled with files 04 and 05 in fix cycle 2, finding 4; one rule across 02, 04, 05): the only assertion on that line is `check(len(copy) == 1 and all(s in copy[0].split() for s in srcs) and copy[0].split()[-1] == '/usr/local/lib/aidev/', 'Dockerfile COPYs the three configs to /usr/local/lib/aidev/')` at test-60:87-88, with `copy` = the `COPY ` lines containing `codex-config.toml` (test-60:85) and `srcs` the three config sources (test-60:86); an extra source before the destination keeps all three conditions true (re-read in fix cycle 2). It breaks only if one of the three config sources is removed from that line, a second `COPY` line containing `codex-config.toml` is added, or the last token changes. [CODE-VERIFIED] |
| B3 root `coder_script` | 0 | Root `.tf`, outside the image (main.tf:104-107; section 6.0 above) | n/a |
| C wrapper edited in place (Dockerfile.coder:137-145 RUN, `echo` group at :142) | 0 | Edit inside the existing RUN, no new instruction. [CODE-VERIFIED location, from section 6.2] | n/a |
| C late-COPY wrapper variant (separate script) | +1 if it is its own COPY | A new COPY is a new layer | 0 if the script is added to the existing `/usr/local/bin` COPY at :492-493 (`bin/motd bin/motd-update bin/welcome bin/refresh-env bin/specstory-cleanup`, 0755, same destination) or to the `/usr/local/lib/aidev/` COPY at :469. [CODE-VERIFIED that those COPYs have those destinations and modes; not tested as a fold] |
| D1 hook merged by `bmad/install.sh` | 0 | Same as B1 (:593) | n/a |
| D2 managed-settings drop-in | +1 as described (a new COPY, pattern :500-501) | `.github/contract-tests/test-73-claude-retention.sh:107-108` requires exactly one COPY line that contains `etc/claude-code/managed-settings.d/10-retention.json` and equals `COPY --chown=0:0 --chmod=0644 <rel> /<rel>`; widening that COPY to a directory form would FAIL test-73 (:119-121). A second COPY of a differently named file (for example `20-...json`) does not touch that pin. [CODE-VERIFIED] | None without editing test-73. The destination `/etc/claude-code/managed-settings.d/` is used by no other COPY. [CODE-VERIFIED by the COPY list in A3] |
| D3 hook merged by root `coder_script` | 0 | Root `.tf` (pattern modules.tf:82-109, section 6.3) | n/a |

Totals against the 2 free layers: B2 and D2 as written are +1 each; C is 0 or +1; B1, B3, D1, D3 are 0. B2 + D2 together would reach exactly 70 (passes, zero margin, below the intent of the "keep margin" comment at workflow :1023). Any third new layer, from this work or from any other PR landing first, reaches 71 and fails the gate (workflow :1026). The decision record notes this race (merged-decision.md:37, "Another PR consumes the headroom first").

### A6. Verdict on the proposed "blocked" marking

- The proposal to mark every option that needs a new layer as blocked is stronger than the evidence supports. With 68 of 70 measured (A2), one or two standalone new layers still pass the gate. The accurate marking is: **B2 and D2 as written are layer-constrained (+1 each; allowed only while the total stays at or below 70); they become unconstrained only through a fold (B2, C) or by also editing test-73 (D2).**
- Recommended ordering for the builder by layer cost: B1, B3, D1, D3, C in place (0 layers) before B2 with the `/usr/local/lib/aidev/` fold (0) before B2 as written, C as a separate COPY, or D2 (+1 each). If the builder picks a +1 option, the plan must name the budget it spends (68 to 69) and re-read the latest main run's `Sysbox image layers: N` line before merge, because another PR can consume the two spare layers first.
- The rebuild model in section 6.4 (column "Needs (i) image rebuild") is unchanged; layer cost is an extra constraint on top of it, not a replacement.

### A7. Gaps recorded by this addendum (the existing `## Gaps and Questions` section above was left unedited, per the append-only rule)

[UNVERIFIED] items:
1. U15: the Sysbox-runtime job's layer count. Only the dind-sidecar job log lines were read (runs 42346410588 and 42384399575). Expected identical because the image is built once per tag; not read.
2. U16: that the base image `codercom/code-server:4.121.0-trixie` contributes 8 layers (68 minus 60 counted instructions). Arithmetic inference only; the base image was not inspected.
3. U17: that the check-only RUN at Dockerfile.coder:589-590 and every other RUN adds exactly one layer under the provider's builder (main.tf:122-145). Not tested; the CI count is the authority.
4. U18: that B2 can ride the `/usr/local/lib/aidev/` COPY (Dockerfile.coder:547-548 or :469) and be seeded by a new `seed_if_absent` line near startup.sh:291-293 with the layer count staying at 68. Precedent is read; the specific use is a proposal and was not built or run.
5. U19: that a new `bin/` helper added to the COPY at Dockerfile.coder:492-493 or :469 keeps the layer count (C late-COPY variant). Same basis as U18.
6. U20: that no other test pins the text of the COPYs at :492, :469 or :547 (only test-73 for :500 and test-67 for the `image_input_files` coverage were read). Other tests were not searched exhaustively for pins on those lines.

[CODE-CONTRADICTED] items:
1. C8: `Dockerfile.coder:468` ("the Sysbox image-layer budget (70) has no headroom") against the measured 68 of 70 on `f1ac0c93` and on the newest main run (two free layers). The comment holds as a policy statement, not as a current measurement. `Dockerfile.coder:229` ("two spare") matches the measurement. Stale-history source: ARCHITECTURE-SPINE.md:93 ("main is at 70").

### A8. Summary

The gap was real: the contract workflow fails any image above 70 layers (workflow :1016-1029), and the earlier option tables never priced layers. The latest CI logs, including the run on this worktree's exact commit `f1ac0c93`, show 68 of 70, so two layers are free and the two Dockerfile comments are reconciled as "two spare now, fold into existing COPY/RUN as policy" (:468 is stale as a measurement). Layer cost is 0 for B1, B3, D1, D3 and C-in-place, +1 as written for B2, D2 and a standalone C COPY, with zero-layer folds available for B2 and C (precedent at Dockerfile.coder:543-545) but not for D2 without editing the test-73 pin; the options are constrained rather than outright blocked.
