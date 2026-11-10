# Synthesis 01: Problem Statement and Current State Analysis

**Topic:** BMAD first-use directory creation in a project that never had BMAD (BMAD-METHOD 6.9.0, Coder AIDev02 workspace)
**Date:** 2026-11-08
**Sources:** research files 01 to 05 and gaps-and-questions.md (fix-cycle addenda applied where they supersede earlier text)
**Status:** Complete

---

## 1. Problem Statement

- **The question:** how can a Coder workspace user get BMAD to create the directories it needs the first time it is used in a project that never had it, WITHOUT a global BMAD install and without reversing owner decision OD-1 beyond first-use creation. The "never globally" half of OD-1 stays: the research found that a mechanism running `bmad install --directory <project>` per project does not conflict with it (gaps log section 6, quoting research-notes F9-4), and that the wording "never globally" is inexact only for the CLI, which is already installed globally in the image (`Dockerfile.coder:139`), not for BMAD framework content.
- **Why it matters (current state in one line each):**

| Today | Evidence |
|---|---|
| Only the one recorded seed repo gets BMAD, once per agent start, at boot | `catalogue/bmad/install.sh:21-55`; run from `startup.sh:1174-1176` |
| With no seed repo, `install.sh` configures nothing, exits 0 and writes only its marker; health stays `Installed-not-Configured` | `install.sh:22-23,57-61`; `test-57:449-452` |
| Any other project needs a manual one-command install named only in the baked welcome text: `bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output` | `catalogue/bmad/manifest.yaml:12-14` |
| Nothing in BMAD 6.9.0 bootstraps itself: skills copied into `.claude/skills/bmad-*` without a project `_bmad/` find no scripts or config, and no skill tells the user to run `bmad install` | file 01 section 7 (see 2.1) |
| The task framing is that the user does not know that one-command install; whether the welcome text reaches the user is not something the research could observe (this workspace has no seed, the welcome file exists at `~/.aidev/status/welcome/bmad.txt`) | task request; file 05 section (d) row d9 |

- **Trigger:** the user decision of 2026-11-07 (issue 478, folder `.dev/issues/478/`) superseding OD-1 for first-use creation only. The decision's exact wording is available only at `BUILD-REQUEST.md:14`, which is outside the research files; the researchers saw it as "BMAD should create its needed directories on first use", with no wording on git cleanliness or on Orca-created worktrees (gaps log G-26). Three parts of the original ask are kept separate: a global install is declined, first-use creation is decided, and the Ponytail half of the prior diagnosis is out of scope by the same-day user confirmation (gaps log D-16, G-29). The prior diagnosis report (`REPORT.md`) is overtaken in two places: its "Restrictions overridden: None" (`REPORT.md:26`) no longer holds, and its "MUST NOT change" rationale (`REPORT.md:89-90`) is overtaken for first-use creation (gaps log CC-27, CC-30; those lines were not re-read by this synthesis).
- **Scope of this file:** Section 1 and Section 2 only (current state). Options, recommendation, implementation plan, owner questions and run-only facts belong to other synthesis files; this file records facts that bound them and flags what remains UNVERIFIED.

## 2. Current State Analysis

### 2.1 BMAD 6.9.0 installer and skill runtime

Source: research file 01 (`research/01-bmad-6-9-0-installer-and-skill-runtime.md`) including its fix-cycle-1 addendum. The package studied is `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/` (`package.json:2-4` name `bmad-method`, version `6.9.0`; `engines.node >=20.12.0` at `package.json:112-114`) [CODE-VERIFIED]. No `bmad install` was run for this research; every installer fact below is read from code, not observed from a 6.9.0 run. Only `bmad --version`, `install --help`, `install --list-tools` and `install --list-options` were executed (with `NPM_CONFIG_OFFLINE=true`).

**Non-interactive install command (CODE-VERIFIED from installer code, never executed):**
`bmad install --directory <dir> --modules bmm --tools claude-code --yes`. `--yes` is what suppresses the prompts (`ui.js:838-867`, `official-modules.js:1518-1526`); `--tools` is mandatory under `--yes` (`ui.js:630-641`, matching help text `install.js:18`); `--tools` alone leaves prompts. There is no `--quiet` option (`install.js:12-51`). The installer does not need `uv` (probe only, warn-not-block, `uv-check.js:75-91`).

**What a fresh 6.9.0 install writes, all inside the install directory (CODE-VERIFIED by reading; not observed):**

| Created path | Created by | Note |
|---|---|---|
| `_bmad/` and `_bmad/{_config,core,scripts,custom}/` | `core/install-paths.js:18-34` | `_bmad/` and subfolders are made first, before the manifest is written |
| `_bmad/scripts/` (resolve_config.py, resolve_customization.py, memlog.py) | `installer.js:664-678` | copied from `src/scripts/` |
| `_bmad/custom/.gitignore` (`*.user.toml`), `custom/config.toml`, `custom/config.user.toml` | `installer.js:680-684`; `manifest-generator.js:626-658` | only if absent |
| `_bmad/core/`, `_bmad/bmm/` and their `config.yaml` | `official-modules.js:268,280,478-534`; `installer.js:949-1037` | built-in modules copied from the package (`official-modules.js:212-226`) |
| `_bmad/config.toml`, `_bmad/config.user.toml` | `manifest-generator.js:428-618` | central config |
| `_bmad/_config/{manifest.yaml, skill-manifest.csv, files-manifest.csv, bmad-help.csv}` | `manifest-generator.js:299-418,681-739`; `installer.js:1046-1150` | `installation.version` = installer package version (`install-paths.js:13`) |
| `_bmad-output/planning-artifacts/`, `_bmad-output/implementation-artifacts/` | `official-modules.js:548-707` driven by `src/bmm-skills/module.yaml:44-47` | `_bmad-output/` appears only as the parent (`src/core-skills/module.yaml` has no `directories` key) |
| `docs/` (default `project_knowledge`) | same; `src/bmm-skills/module.yaml:38-41,47` | created only if absent |
| `.claude/skills/bmad-*/` | IDE step `installer.js:97,372-397` -> `ide/_config-driven.js:245-248,417-468` | verbatim directory copy; always `path.join(projectDir, target_dir)` |

Not created: `.git`, any project `.gitignore` edit, `CLAUDE.md`, `.claude/settings*.json`, `.claude/commands/`, anything under `~/.claude` [CODE-VERIFIED]. Non-BMAD skills already in `.claude/skills/` are left alone on a fresh install (`_config-driven.js:499-516,786-803`). A prior review (not re-run) recorded the same directory-level result for a real 6.9.0 run plus "46 skills" (`04-bmad.md:28-32`, tagged prior-review observation, not re-run); the code-derived table agrees at directory level, and 46 `SKILL.md` files exist under `src/core-skills` and `src/bmm-skills` (Glob).

**Git and HOME:** the installer never calls git against the target project (git runs only inside external/custom module cache clones, `external-manager.js:330-391`, `custom-module-manager.js:412-502`), so it needs no git repo and does not stage or commit (`installer.js:869`, `file-ops.js:129`). By exhaustive Grep, a `--modules bmm --tools claude-code` install has no installer-code write under HOME; `~/.bmad/cache/*` is reached only for external, community or custom modules (`external-manager.js:184`, `custom-module-manager.js:383`). Residual UNVERIFIED: npm's own metadata cache under `~/.npm` from the best-effort `npm view bmad-method@latest version` at `bmad-cli.js:31-35` (5 s cap, errors swallowed, runs on every invocation) and the `uv --version` probe. Built-in `core` and `bmm` need no network (`official-modules.js:212-226`, `manifest.js:283-291`).

**Dead upstream hooks for a user-scope install [CODE-VERIFIED by whole-package Grep]:**

| Item | What the code shows |
|---|---|
| `global_target_dir` (claude-code value `~/.claude/skills`, `platform-codes.yaml:57`) | 43 occurrences in exactly one file, `tools/installer/ide/platform-codes.yaml` (comments at lines 9 and 12, 41 value lines). No `.js`, `.mjs`, `.cjs`, `.json` or `.md` file reads it. Option F (upstream user-scope install) has no code path in 6.9.0 |
| `ancestor_conflict_check` | Reader at `_config-driven.js:191` (`findAncestorConflict`, `:943-969`) but no platform entry sets the key (`platform-codes.yaml:10` is a comment only), so the check never runs for any tool, claude-code included |
| `install.js:12-51` options | No `--global` or `--user` flag exists |

**Skill runtime needs (CODE-VERIFIED by reading; not executed):**

| Script or skill behaviour | Evidence | Behaviour without `_bmad/` |
|---|---|---|
| `src/scripts/resolve_config.py` needs `--project-root`; looks only at `<root>/_bmad/`; `_bmad/config.toml` required | `resolve_config.py:143-163` | stderr `error: required config file not found: <root>/_bmad/config.toml`, exit 1 (`:48-51`); a bare `_bmad/` without `config.toml` fails the same way |
| `src/scripts/resolve_customization.py` `find_project_root` walks up to the first dir with `_bmad` OR `.git`; looks from the skill's own dir first, then cwd | `resolve_customization.py:58-66,211-215` | silently prints the skill's `customize.toml` defaults (derived from `:209-236`; U5, not run) |
| Both scripts need Python 3.11+ (`tomllib`), exit 3 otherwise | `resolve_config.py:34-40`; `resolve_customization.py:43-51` | host has 3.11 and 3.13 (observed in the research session) |
| `memlog.py init` creates its parents | `memlog.py:150` | only runs if `_bmad/scripts/memlog.py` exists |
| 39 of 46 `SKILL.md` reference the two scripts (52 matches); 37 load `{project-root}/_bmad/{bmm,core}/config.yaml` | Grep counts, corrected in fix cycle 1 (the earlier "40 files, 92" did not reproduce) | script path is anchored on `{project-root}/_bmad/scripts/`, so a project without `_bmad/` has nothing to run |
| Fallbacks written into skills | `bmad-quick-dev/SKILL.md:47-53`, `bmad-dev-story/SKILL.md:32-38`: read `customize.toml` directly; `bmad-prd/SKILL.md:20`, `bmad-forge-idea/SKILL.md:27`: "Missing keys -> neutral defaults; never block"; `bmad-quick-dev/SKILL.md:65`, `bmad-dev-story/SKILL.md:50`, `bmad-agent-dev/SKILL.md:49`: no stated fallback for a missing `config.yaml` | model behaviour in this state is UNVERIFIED (U6) |
| No skill detects a missing `_bmad/` or tells the user to run `bmad install` | Grep over `src/` returns one non-instruction hit (`src/core-skills/module.yaml:6`) | There is no built-in bootstrap; any first-use creation has to come from outside BMAD |

**Why the `install.sh:42` flag set matters (partial-seed branch, fix cycle 1 finding 7):** the shipped `catalogue/bmad/install.sh:42` passes `--user-name` and `--output-folder`, so it takes `ui.js:807-837`, not the bare-`--yes` default branch (`ui.js:838-861`). Result: `_bmad/core/config.yaml` holds only `user_name` and `output_folder`; `project_name`, `communication_language` and `document_output_language` are written nowhere (`installer.js:949-1037`, `manifest-generator.js:468-545`), while skills such as `bmad-dev-story/SKILL.md:50-53` load all four keys with no stated fallback (U13, model behaviour not run). `--output-folder _bmad-output` must stay in every first-use command: without it and with `--user-name`, `output_folder` is never seeded and `official-modules.js:1387-1409` can leave an unresolved `{output_folder}` text (mechanism CODE-VERIFIED, outcome UNVERIFIED). The prior-review phrase "`--yes` without `--output-folder` creates literal `{output_folder}/` dir" (`.memlog.md:21`, `04-bmad.md:33`) is [CODE-CONTRADICTED] as a description of bare `--yes`: bare `--yes` seeds `output_folder: '_bmad-output'` (`ui.js:838-861`); quote the phrase, do not restate it as a bare-`--yes` defect.

**Version skew and partial trees (fix cycle 1, F5-D; mechanism CODE-VERIFIED, outcome of quick-update on a half-written tree UNVERIFIED):**

| Step | Evidence |
|---|---|
| `_bmad/` existing at all makes the run an update | `ui.js:217-220`; `installer.js:1549-1552` |
| "Installed" is true if `_bmad/core/` exists, any module is listed, or a manifest is readable | `core/existing-install.js:50-66,111` |
| `--yes` with no `--action` on an installed tree defaults to `quick-update` with no version test | `ui.js:233-262` |
| No installed-versus-installer version gate in `core/installer.js` | Grep for `downgrad`, `isNewer`, `semver`, `compareVersions`: no `semver` hit in `core/installer.js` |
| A failed first run leaves `_bmad/core/` etc., so a later `bmad install --yes` takes quick-update, not fresh-install; `install()` has no rollback of `_bmad/` | `install-paths.js:21-34`; `installer.js:122-138` |

A prior review (not re-run) measured 6.9.0 `--yes` over a 6.10.0 tree downgrading `_bmad/_config/manifest.yaml` to 6.9.0 and changing 41 tracked files with rc 0 and no warning (`04-bmad.md:37`; `.memlog.md:21`), and a quick-update re-run rewriting 6 files (`04-bmad.md:36`). Those counts are tagged prior-review observation, not re-run.

**Duration (U1, narrowed in fix cycle 1; do not blend the two figures):** CI log lines of `test-57` show `cold bmad: 374 ms` (run `42384399575`), `392 ms` (`42369600288`) and `392 ms` (`42346410588`) for the whole baked `install.sh` with `--network=none` on a one-file fixture repo (prior-review observation, not re-run). The memlog's "about 4s" is a different configuration (`npx bmad-method@6.9.0`, scratch HOME, network available, npx fetch included: `04-bmad.md:4,34`). Duration inside a real Coder workspace is UNVERIFIED.

**Tracked tree in this worktree (version-mismatched corroboration only):** facts tagged OBSERVED-FROM-6.10.0-TRACKED-TREE in file 01 come from this worktree's git-tracked tree (`_bmad/_config/manifest.yaml:2` `installation.version: 6.10.0`), not from 6.9.0 installer output, and are not proof of what a fresh 6.9.0 install creates. The tree has 17 tracked `_bmad` files, 577 tracked `_bmad-output` files and 237 tracked `.claude/skills/bmad-*` files across 47 `bmad-*` directories. It is shown by contradiction to be non-6.9.0 output: `_config/agent-manifest.csv` exists there but the string `agent-manifest` appears nowhere under the 6.9.0 package `tools/` or `src/` (`manifest-generator.js:84-93` writes other files) [CODE-VERIFIED absence in 6.9.0]. The worktree's `bmad-help/SKILL.md:26` (`uv run --python 3.11 ... resolve_config.py`) is [CODE-CONTRADICTED] as a description of the 6.9.0 skill, which reads config files (`src/core-skills/bmad-help/SKILL.md:26`).

**Contradictions and stale documentation surfaced from file 01:** `platform-codes.yaml:9` ("User-home directory for global install") and `:10` ("Refuse install when ancestor dir has BMAD files") are [STALE DOC]/[CODE-CONTRADICTED]: neither feature has a live code path in 6.9.0. `install.sh:18` and the catalogue `manifest.yaml` call `/usr/local/bin/bmad` a "symlink"; `Dockerfile.coder:134-135,142` shows it is a wrapper script [STALE DOC, low impact]. `04-bmad.md` line refs `Dockerfile.coder:360` are stale; the pin is at `Dockerfile.coder:139` [CODE-CONTRADICTED for the line number only].

**Evidence:**
- `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/package.json:2-4,22-25,112-114`
- `.../tools/installer/commands/install.js:12-51,54-148`; `.../tools/installer/ui.js:156-262,391-501,617-643,775-870,1287-1317`
- `.../tools/installer/core/installer.js:37-138,329-337,372-449,664-684,949-1150,1549-1552`; `.../core/install-paths.js:13-34,57-68`; `.../core/existing-install.js:50-66,111`
- `.../tools/installer/modules/official-modules.js:212-226,268-280,478-534,548-707,1023-1143,1362-1415`; `.../core/manifest-generator.js:84-93,299-418,428-658,681-739`
- `.../tools/installer/ide/platform-codes.yaml:9-12,52-57`; `.../ide/_config-driven.js:189-207,245-248,417-468,499-516,943-969`
- `.../src/scripts/resolve_config.py:34-51,143-163`; `.../src/scripts/resolve_customization.py:43-74,195-236`; `.../src/scripts/memlog.py:147-150`
- `.../src/bmm-skills/module.yaml:28-47`; `.../src/core-skills/bmad-help/SKILL.md:26`; `bmad-dev-story/SKILL.md:30-53`; `bmad-quick-dev/SKILL.md:45-65`
- `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/_bmad/_config/manifest.yaml:1-22` (6.10.0, corroboration only)
- `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.github/contract-tests/test-57-catalogue-configure.sh:31,64-66,75-79,172-183,323-324,413-444`; `.../.github/workflows/coder-ci-aidev02-contract.yml:1198-1218,1241`
- `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:18-60`; `.../Dockerfile.coder:134-143`

### 2.2 Image CLI wrapper and the bmad catalogue slug

Source: research file 02 (`research/02-image-cli-and-catalogue-slug.md`) including its fix-cycle-1 Sysbox layer addendum (and the fix-cycle-2 reconciliation of the test-60 rule it cites). All paths below are under `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/templates/VSCode-AIDev02/` unless stated.

**The `bmad` command is a two-line wrapper with no first-use logic [CODE-VERIFIED]:**

| Item | Evidence |
|---|---|
| Pin: `npm install -g bmad-method@6.9.0` inside an nvm shell | `image/Dockerfile.coder:139` (root layer `USER root` at :136, back to `USER 1000` at :145) |
| Wrapper written as `#!/bin/sh` + `exec "<node_bin>" "<cli>" "$@"`, `chmod 0755` | `image/Dockerfile.coder:140-143`; the file on this machine `/usr/local/bin/bmad:1-3` execs `/opt/nvm/versions/node/v24.22.2/bin/node` on `.../bmad-method/tools/installer/bmad-cli.js` |
| Installed version equals the pin | `.../bmad-method/package.json:3-4` (`6.9.0`); `bmad --version` printed `6.9.0` |
| Nothing in `bmad-cli.js` looks for `_bmad/`; every start fires a background `npm view` update check (errors swallowed) | `bmad-cli.js:20-35,73-105` |
| An update box ("6.12.4 is available") printed even with `NPM_CONFIG_OFFLINE=true`; cause not investigated; 6.12.4 itself is UNVERIFIED | file 02 section 1.4 (U2, U3) |
| No `--global` or `--user` option exists in `bmad install` | `commands/install.js:12-51` |

Any first-use behaviour placed in the wrapper would be new code in `image/Dockerfile.coder` (image rebuild); the wrapper cannot fire when a BMAD skill is invoked inside Claude Code because no `bmad` process runs then (inference from how skills execute, UNVERIFIED, file 02 U12).

**`catalogue/bmad/install.sh` (boot-time, seed-repo-only) [CODE-VERIFIED by reading; the script was not run]:**

| Lines | Behaviour |
|---|---|
| 6-10, 12-13 | slug `bmad`; log `/tmp/catalogue-bmad.log`; marker `${HOME}/.aidev/installed/bmad`; seed path file `${HOME}/.aidev/status/seed-repo-path` |
| 18 | `command -v bmad` else `FAIL: bmad not on PATH` and exit 2 (text says "symlink": stale, the CLI is a wrapper) |
| 21-23 | guard 1: no seed repo recorded, or it is not a git work tree: nothing to configure, falls through to the marker (exit 0) |
| 24-25 | guard 2: `<seed>/_bmad` exists (any entry, including a bare directory) OR `git ls-files -- '.claude/skills/bmad-*'` is non-empty: left untouched, falls through to the marker (exit 0) |
| 28-34 | appends `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/` to the repo's `info/exclude` |
| 38, 48-53 | git status taken after the excludes and again after the install; any change is `FAIL`, exit 1. There is NO clean-tree pre-check; a dirty seed repo is accepted (`test-57:457-458`) |
| 42-45 | the only install call: `NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output --user-name "$(git -C "${D}" config user.name \|\| id -un)" </dev/null`; non-zero (including timeout 124) is `FAIL`, exit 1 |
| 46 | `_bmad/_config/manifest.yaml` must exist afterwards, else exit 1 |
| 58-61 | writes the marker; exit 0. Failure exits come before the marker write but leave `_bmad/` and the exclude lines in place |

Consequence (CODE-VERIFIED by reading lines 24, 41, 58 and `spec2-health.sh:103`): a failed or status-changing first install leaves a partial `_bmad/` that guard 2 skips on the next boot, so it turns into a "left untouched" pass; there is no auto-repair (the script's own comment at :41 says so). The script has no marker-plus-affordance short-circuit at the top (compare `ironclaude/install.sh:31-35`), so its idempotency comes from guard 2. It runs once per agent start, from `startup.sh:1174-1176` as `( source "${HOME}/.aienv" && bash "<dir>/<script>" ) > "<log>" 2>&1`, without the 30 s bound other slugs get through `aidev_cat_install` (`startup.sh:1177-1181`); only `workspace` and `hybrid` scopes run at boot (`startup.sh:1158-1159`; bmad is `hybrid`, `manifest.yaml:3`). It never runs in an arbitrary project and has no hook for "first use".

**Welcome text and slug shape [CODE-VERIFIED]:**

| Item | Evidence |
|---|---|
| The catalogue dir holds exactly `manifest.yaml`, `install.sh`, `module.tf` (the three-file rule) | Glob; `catalogue/README.md:81-92`; test-1 enforcement closed by file 04 (`test-1-catalogue-shape.sh:25,43-67`) |
| `manifest.yaml`: name `bmad`, version `6.9.0`, scope `hybrid`, `install_disposition: image-baked`, health check `bmad --version`, discoverability `installed-only` with invocation `bmad` and help `bmad --help` | `catalogue/bmad/manifest.yaml:1-4,24-29` |
| Welcome text sends the user to a manual command for any other repo: `bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output` | `manifest.yaml:12-14` |
| That manual command differs from `install.sh:42`: no `NPM_CONFIG_OFFLINE=true`, no `--user-name`, no `info/exclude` lines, so in another repo BMAD's directories show as untracked files | comparison of `manifest.yaml:14` with `install.sh:32-34,42` |
| The welcome text says "BMad is already set up there" unconditionally; true only when neither guard intercepts | `manifest.yaml:12`; `install.sh:22-25` |
| `module.tf` declares only the coder provider and `variable "agent_id"`; no `coder_app`, no resources | `catalogue/bmad/module.tf:1-21` |
| bmad is in exactly one profile, `orca`; `minimal` has no bmad | `image/catalogue/profiles.yaml:13-21`; `modules.tf:19-20,29,33,50-54` (`count = contains(local.active_slugs, "bmad") ? 1 : 0`) |
| The catalogue contract has no field for "run when the CLI is first used"; every hook it offers (install.sh, health_check, welcome_message) is boot-time or read-only | file 02 key takeaways (c) |

**Rebuild classes and layer budget (the constraints any first-use change inherits) [CODE-VERIFIED]:**

| Item | Evidence |
|---|---|
| Everything under `image/` is the Docker build context; the image tag and rebuild trigger hash `Dockerfile.coder`, the listed COPY sources and every file under `image/catalogue/**`. Root `.tf` files are not hashed into the image tag | `main.tf:73-74,80-107,111,119,148-150` |
| So a change under `image/` (install.sh, Dockerfile, startup.sh, `/etc/skel` content, managed settings) is a class (i) image rebuild; a change only in root `.tf` files (for example a `coder_script` in `modules.tf`, pattern `coder_script "orca_retirement"` at `modules.tf:82-109`) is class (ii) template push only | `main.tf:104-107`; file 02 table 6.4 |
| HOME is the per-workspace named volume `coder-<workspace id>-home` at `/home/coder`; image seed files under `/etc/skel` reach HOME only copy-if-absent at boot; persistent homes are not migrated | `main.tf:174-176,594-596`; `Dockerfile.coder:543-545`; `startup.sh:191,275,283-289` |
| Sysbox image-layer gate: fails when `docker image inspect ... RootFS.Layers` exceeds 70 | `.github/workflows/coder-ci-aidev02-contract.yml:1016-1029` |
| Measured count: `Sysbox image layers: 68 (budget: 70)` on run `42346410588` (sha `f1ac0c93...`, which equals this worktree's HEAD at that time) and on run `42384399575`; two free layers. Only the dind-sidecar job log was read (Sysbox arm UNVERIFIED) | file 02 addendum A2 (CI log read, not re-run) |
| `Dockerfile.coder:468` ("budget (70) has no headroom") is [CODE-CONTRADICTED] as a current measurement (68 of 70); correct only as a fold-into-existing-COPY/RUN policy. `Dockerfile.coder:229` ("two spare") matches | file 02 addendum A4, C8 |
| Layer cost as written: 0 for an edit to `bmad/install.sh` (rides the last COPY at `Dockerfile.coder:593`), a root `coder_script`, and an in-place edit of the wrapper RUN (`Dockerfile.coder:137-145`); +1 for a new `/etc/skel` COPY or a new managed-settings COPY; a zero-layer fold exists via the `/usr/local/lib/aidev/` COPY (`Dockerfile.coder:547-548`, test-60 rule at `test-60:85-88`) but not for the managed-settings COPY without editing test-73 (`test-73-claude-retention.sh:107-121`) | file 02 addendum A5, A6 |

**Health and readiness look only at the seed repo [CODE-VERIFIED]:** `spec2_health_observed bmad` reads the first line of `~/.aidev/status/seed-repo-path` and emits `seed-config` only if `<seed>/_bmad/_config/manifest.yaml` is a file or a git-TRACKED `.claude/skills/bmad-*/SKILL.md` exists (`image/scripts/lib/spec2-health.sh:99-114`). bmad has one required name, so it can never be `Partially` (`:172-192`). States are recomputed once per agent start (`startup.sh:1187`; the reader requires the current boot's invocation id, `spec2-health.sh:230`). A first-use install in any project other than the seed repo changes nothing health reads.

| Situation at boot | State |
|---|---|
| bmad not in profile (`minimal`) | readiness `not-selected` (`spec2-health.sh:562-565`) |
| no seed repo recorded | `Installed-not-Configured` (`test-57:449-452`) |
| seed repo with `_bmad/` only, no manifest | `Installed-not-Configured` (`test-57:419`) |
| seed repo with `_bmad/_config/manifest.yaml` | `Configured` (`test-57:323`) |
| seed repo tracking `.claude/skills/bmad-*/SKILL.md` | `Configured` (`test-57:427`) |

**Existing precedent and hazards other mechanisms would meet (current-state facts):** `orca/install.sh:18-42` already writes skills into `~/.agents/skills` and `~/.claude/skills`, and `modules.tf:98-106` removes them when orca is deselected, whereas bmad is excluded from the §9 deselect cleanup (`startup.sh:1114-1117`). `aidev_claude_md_block_sync` re-syncs a marked block into `~/.claude/CLAUDE.md` every boot but its markers are hard-coded to `SUPERCLAUDE_CODEGRAPH_BEGIN/END` (`claude-md-block.sh:23`). IronClaude's configured-check treats any hook command containing `/.claude/hooks/` as an IronClaude hook (`ironclaude/install.sh:15-16,25,141`; `spec2-health.sh:90-91`), and `ironclaude/install.sh:139` admits there is no lock against the parallel Orca writer of `settings.json`. The Renovate-visible strings that must stay: `npm install -g bmad-method@X.Y.Z` in `Dockerfile.coder`, `bmad-method@X.Y.Z` in `bmad/install.sh`, `^version: X.Y.Z$` in `bmad/manifest.yaml` (`.github/upstream-monitor/expected.txt:6-8`; `renovate-global.json5:47-48,54-55`).

**Contradictions and stale documentation surfaced from file 02:** `install.sh:18` "symlink" vs wrapper script (`Dockerfile.coder:134-143`) [CODE-CONTRADICTED]; `profiles.yaml:1` path comment omits `image/` [STALE DOC]; catalogue `README.md` paths and links at lines 32, 64, 348, 408-409, 594-596 and the `( source ~/.aienv && bash install.sh )` statement at 180-183 (true only for bmad, `startup.sh:1175`) [STALE DOC]; `startup.tf:30` "ONLY runtime coder_script" vs further `coder_script` resources at `modules.tf:82`, `main.tf:220,233`, `orca/module.tf:58,79`, `vibe-kanban/module.tf:40` [CODE-CONTRADICTED]. `Dockerfile.coder:134-135` (NVM node not on the default PATH) is a comment and its runtime claim is UNVERIFIED.

**Evidence:**
- `templates/VSCode-AIDev02/image/Dockerfile.coder:133-145,229,468,543-548,593`; `/usr/local/bin/bmad:1-3`
- `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:1-61`; `.../bmad/manifest.yaml:1-30`; `.../bmad/module.tf:1-21`; `.../image/catalogue/profiles.yaml:13-21`
- `templates/VSCode-AIDev02/modules.tf:19-20,29,33,50-54,82-109`; `.../main.tf:73-74,80-107,111,119,148-150,174-176,594-596`
- `templates/VSCode-AIDev02/image/scripts/lib/spec2-health.sh:74-114,141-192,216-239,562-565`; `.../image/scripts/startup.sh:1114-1117,1158-1187,1174-1182`
- `.github/workflows/coder-ci-aidev02-contract.yml:1016-1029`; `.github/upstream-monitor/expected.txt:6-8`

### 2.3 Startup flow, HOME persistence and user-level Claude Code surfaces

Source: research file 03 (`research/03-startup-flow-home-and-user-level-claude.md`) including its fix-cycle-1 finding-4 addendum (first-use predicate, `block-bare-python.sh`) and the fix-cycle-2 corrections it records. Paths are under `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/templates/VSCode-AIDev02/` unless absolute. The `~/.claude/` observations are from a long-lived, actively used workspace (22 `settings.json.bak*` files), not a fresh-boot sample.

**HOME persistence [CODE-VERIFIED for the mounts; runtime behaviour inferred, not exercised]:**

| Fact | Evidence |
|---|---|
| `/home/coder` is the per-workspace named volume `coder-${workspace.id}-home`; `/config/workspace` is a second volume; everything else comes from the image on every container recreate | `main.tf:174-176,594-602` |
| So `~/.claude/` and `~/.aidev/` survive stop/start and `coder update`; a NEW workspace gets a new empty home volume, so a hand-written user-level skill or hook does not exist there unless boot code seeds it or the image carries it | `main.tf:174-176`; file 03 section 6 |
| Volume deletion on workspace delete, and Docker copying `/home/coder` image content into a new empty volume | UNVERIFIED (file 03 Gaps 1, 12); startup §6 re-seeds anyway |
| Boot entry `coder_script.startup` runs `aidev-startup` on every start (`run_on_start = true`, `start_blocks_login = false`); a second login-blocking script runs `reapply-central-defaults` | `startup.tf:42-46,54-63`; `main.tf:220-227` |
| No Terraform file writes anything into `~/.claude` | file 03 section 1 takeaways |

**Boot order (`image/scripts/startup.sh`, `set -euo pipefail` at :14; sections 4, 5, 11 retired, :7-9) [CODE-VERIFIED]:**

| Order | Section (line) | Touches `~/.claude`? |
|---|---|---|
| 1 | §1 init (16): status dirs, `~/workspaces`, `specstory-cleanup --once` (119) | no |
| 2 | §2 runtime-bootstrap (121): dockerd, up to 60 s wait | no |
| 3 | §3 git-identity (160) | no |
| 4 | §6 workspace-defaults (191): `seed_if_absent` (201-274), copy-if-absent from `/etc/skel` and `/usr/local/lib/aidev`; never overwrites an existing regular file (241-248) | yes, only `~/.claude/CLAUDE.md` (line 275) |
| 5 | §7 gh-auth (303) | not in lines read |
| 6 | §8 seed-repo-clone (389); sole writer of `~/.aidev/status/seed-repo-path` (673-681) | no |
| 7 | §9 catalogue-installs (692): `/catalogue/*` in `LC_ALL=C` order, so `bmad` runs before `ironclaude`; non-blocking per slug (710-712) | via the ironclaude slug |
| 8 | post-§9 (1279-1285): `aidev_claude_md_block_sync` | yes, `~/.claude/CLAUDE.md` only |
| 9 | §10 (1348), tool-floor-verify (1451), §12 (1665) | not read (UNVERIFIED, Gap 10) |

The whole sequence re-runs on every start, so anything added must be idempotent. Nothing in `startup.sh` creates `~/.claude/skills/` or writes `~/.claude/settings.json` directly (Grep hits only at lines 275, 979, 1172, 1282, 1285). The bmad slug is per seed repo only; its marker is exempt from deselect removal (`startup.sh:1116-1118`, "an explicit owner-decision exception") and it runs without the 30 s watchdog other slugs get (`startup.sh:1170-1182`). In this workspace `~/.aidev/status/seed-repo-path` does not exist, so the slug had nothing to configure (matches `install.sh:22-23`).

**Who writes user-level skills and settings today [CODE-VERIFIED]:**

| Writer | `settings.json` | `skills/` | Evidence |
|---|---|---|---|
| `superclaude install` (run by the ironclaude slug on first boot and whenever the image's IronClaude `git_sha` differs from `~/.aidev/installed/ironclaude.configured`, with `--force`; or by the user) | additive hook merge, fill-only defaults, `claudeMdExcludes` append | copies packaged skills by name (39 names, none starting `bmad`) | `ironclaude/install.sh:2-3,26-35,91-97,122`; `main.py:204,217,236`; `install_hooks.py:269-467`; `install_user_setup.py:155-195` |
| Orca CLI (`orca skills install`), via superclaude and the orca slug | not by Orca code in this repo | `orca-cli`, `orchestration` (and `computer-use` via superclaude) | `install_user_setup.py:230-263`; `catalogue/orca/install.sh:26-41` |
| orca deselection retirement | no | removes only the two orca symlinks | `modules.tf:82-109` |
| `specstory-cleanup --once` | removal of the SpecStory hook only | no | `image/bin/specstory-cleanup:28-70` |
| Claude Code itself (`/config`), the user | yes | yes (user) | doc-sourced / inferred; UNVERIFIED |

The live `~/.claude/skills/` has 42 entries and no `bmad-*` entry and no user-added entry (comparison with the packaged 39 names leaves exactly `computer-use`, `orca-cli`, `orchestration`, which are Orca's). `~/.claude/settings.json` (54505 bytes, regular file) has 15 hook event types, and `~/.claude/hooks/` holds 14 files; image-level `/etc/claude-code/managed-settings.d/` holds only `10-retention.json` = `{"cleanupPeriodDays": 90}` (`image/etc/claude-code/managed-settings.d/10-retention.json:1-3`).

**Overwrite versus merge semantics of `superclaude install` [CODE-VERIFIED by reading]:** hooks merge additively by exact command string (`install_hooks.py:14-15,379-447`); defaults are fill-only (`install_user_setup.py:41-47,155-195`); hook scripts are copied only for a fixed name list (`install_hooks.py:42-87`); skills are replaced per packaged name only, with `rmtree` solely at `install_skills.py:97` and `install_skill.py:48`; no code prunes unknown names. A user skill or hook under a new name or command string survives `superclaude install --force`; the only hazard is an exact collision, and a `bmad-*` name does not collide. A repo-side assertion protects hook commands only (`ironclaude/install.sh:104-136`), nothing asserts that user skills survive. Hazards: no lock against a parallel `settings.json` writer (`ironclaude/install.sh:139`, Orca writer UNVERIFIED), and `settings.json.bak.<stamp>` churn (file 03 counts 21 stamped backups in section 5 and 22 `settings.json.bak*` files in section 4; the difference is not explained).

**`block-bare-python.sh` (closes file 01 U8 for the file-and-code part) [CODE-VERIFIED for existence, registration here and the exit-2 rule; UNVERIFIED for the effect]:** the hook is packaged by superclaude (`install_hooks.py:85`), installed through the ironclaude slug that the Default profile selects (`image/catalogue/profiles.yaml:14,18`; `ironclaude/install.sh:2-3`), registered as PreToolUse(Bash) in this workspace (`/home/coder/.claude/settings.json:183-190`) and exits 2 when the command word is `python3` (`/home/coder/.claude/hooks/block-bare-python.sh:134,343-344`). The `minimal` profile has no ironclaude slug, so it has no such hook from boot code. The 6.9.0 package has 41 `python3 ` lines in 31 `SKILL.md` files (38 `resolve_customization.py`, 2 `resolve_config.py`, 1 `list_customizable_skills.py`); a written `If the script fails` fallback exists in 25 of those 31 files and not in the other 6 (`bmad-advanced-elicitation`, `bmad-customize`, `bmad-validate-prd`, `bmad-create-prd`, `bmad-create-architecture`, `bmad-edit-prd`; the last three of those derived by subtraction, UNVERIFIED). Whether Claude emits the bare `python3` form, and whether a fresh Default workspace carries the registration, are UNVERIFIED (file 03 Gaps 13-14). The installer command itself is not blocked: the scanner sees `bmad`, not `python3` (derived from the scanner, hook not run).

**Contradiction between files 01 and 03 (stronger evidence: file 03 addendum A5, which reads the skills directly):** file 01 section 7.5 says the 6.9.0 skills instruct `python3 {project-root}/_bmad/scripts/resolve_customization.py` and that the fallback is reading `customize.toml`. File 03 shows 41 `python3 ` lines across 31 files (2 core skills, 29 bmm skills), that other skills use `uv run` instead (file 01 section 7.4: `bmad-prd`, `bmad-spec`, `bmad-brainstorming`, `bmad-forge-idea`), and that the written fallback reads three TOML files (`customize.toml`, `custom/<skill>.toml`, `custom/<skill>.user.toml`), not only `customize.toml` (`bmad-prfaq/SKILL.md:35-39`, `bmad-agent-dev/SKILL.md:25-29`). The synthesis uses file 03's figures. A smaller line-count difference: file 01 calls `install.sh` 62 lines, file 02 says 61; immaterial.

**The first-use trigger predicate the research defines (a proposed definition, nothing implemented; evidence rows CODE-VERIFIED):**

| Fact behind it | Evidence |
|---|---|
| The only existing "never had BMAD" guard is `install.sh:22-25` (no `.git` goes to "nothing to configure"; `_bmad` existing at all, or any TRACKED `.claude/skills/bmad-*`, goes to "left untouched") | `catalogue/bmad/install.sh:21-60` |
| The guard tests `_bmad` by plain existence, so a partial `_bmad/` is "already has BMad" and never repaired | `install.sh:24,41` |
| The guard sees only tracked skills; the slug's own `info/exclude` makes the installed skills untracked, so deleting `_bmad/` while leaving the skills makes the guard report "never had BMad" (derived, not run) | `install.sh:24,28-34` |
| The root-anchored excludes and the before/after `git status` check would fail a subfolder install (that git anchors `info/exclude` at the work-tree top is git documentation, UNVERIFIED) | `install.sh:32,38,48-53` |
| The installer's own existing-install test is `P/_bmad` existing at all (corrected in fix cycle 2; the older `official-modules.js:770-797` function serves only config loading) | `core/installer.js:1549-1552`; `ui.js:217-220` |
| Working skills need `_bmad/config.toml` | `resolve_config.py:156` |
| A parent-level or user-level `bmad-*` skill dir does not make `bmad install` refuse (ancestor check off for claude-code) | `_config-driven.js:191`; `platform-codes.yaml:10,52-57` |

`FIRST_USE(P)` is true when all hold: (1) P is the git work-tree top (`git rev-parse --show-toplevel`), else the current directory; (2) `[ ! -e "$P/_bmad" ]`; (3) no `$P/.claude/skills/bmad-*` entry on disk, tracked or untracked (a filesystem glob, stricter than `install.sh:24`); (4) the directory is writable. A `_bmad/` that exists without `_config/manifest.yaml` or `config.toml` is a broken install, not first use, and the predicate is false. The one command run on a true predicate: `NPM_CONFIG_OFFLINE=true bmad install --yes --directory "$P" --modules bmm --tools claude-code --output-folder _bmad-output --user-name "<name>"`. Whether `bmad install` works in a directory with no `.git` was not observed (the code touches git only in module-cache code; file 03 Gap 17, file 01 U11); treating subfolders of a repo as the repo top is a design choice and the monorepo consequence is an owner decision.

**What the install shows the user, and what is unknown (CODE-VERIFIED strings; behaviour UNVERIFIED):** `Claude Code configured: <N> skills -> .claude/skills` (`_config-driven.js:477-479`), `Installed to: <bmadDir>` (`installer.js:1219-1221`), then a `BMAD is ready to use!` box telling the user to "Launch your AI agent from your project folder" (`installer.js:1230-1243`). `<N>` and the duration are unknown. `~/.claude/settings.json` has no top-level `permissions` key (only `skipDangerousModePermissionPrompt: true` at :384) and the defaults JSON has none, so nothing here pre-approves a Bash command; the prompting rule is doc-sourced (see section 2.5 and web research files, outside this file). Whether a running session picks up skills created mid-session, whether Claude Code loads `~/.claude/skills` in every project, and how it ranks a user-level skill against a same-named project skill (file 01 U7, file 03 Gaps 21-22) were open in files 01 to 05 and are decided only by web research, which this synthesis does not use.

**Placement facts in this repo for user-level surfaces (all inside this repo; no IronClaude or IronOrca change is needed for a skill or a hook, because superclaude leaves non-packaged names alone):**

| Mechanism | Place | Constraint found |
|---|---|---|
| M1 startup §6 `seed_if_absent` | `startup.sh:201-274`, call list 275-293 | copy-if-absent, so a later image update never reaches an existing workspace; the source must ride an existing COPY and be listed in `main.tf:80-101` `image_input_files` (`main.tf:75-79`, test-67) |
| M2 bmad slug installer | `catalogue/bmad/install.sh`, before the marker write (:57-60) | catalogue files are hashed into the image tag (`main.tf:74`); the three seed-repo branches all fall through to the marker, so a step after :55 runs with or without a seed repo |
| M3 `settings.json` hook merge | no existing helper (only removal in `specstory-cleanup`, preservation check in `ironclaude/install.sh:104-136`) | new jq merge code; no lock against concurrent writers (`ironclaude/install.sh:139`); use a hook script name outside the managed list (`install_hooks.py:42-87`) |
| M4 managed settings drop-in | `image/etc/claude-code/managed-settings.d/`, `Dockerfile.coder:473-475,498-501`, `main.tf:87` | pinned by `test-73-claude-retention.sh:3-9,68-96,117-118`; whether a second file passes it and whether a managed drop-in merges or replaces user hooks are UNVERIFIED (Gaps 5-6) |

**Evidence:**
- `templates/VSCode-AIDev02/main.tf:174-184,216-227,583-614`; `.../startup.tf:27-63`; `.../modules.tf:82-109`
- `templates/VSCode-AIDev02/image/scripts/startup.sh:7-14,16-1285` (sections cited above), `:201-293,692-712,1114-1118,1170-1182,1275-1285`
- `templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh:2-3,15-35,42,91-139,143-150`; `.../catalogue/bmad/install.sh:21-60`; `.../catalogue/profiles.yaml:14-21`
- `/home/coder/.claude/settings.json:183-190,248-258,384` (key names and hook registrations only); `/home/coder/.claude/hooks/block-bare-python.sh:108,134,338-344`
- `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/install_hooks.py:14-15,42-87,222-261,269-467`; `.../install_user_setup.py:34,118-132,155-195,230-263`; `.../install_skills.py:88-110`; `.../install_skill.py:46-52`; `.../main.py:178-263`
- `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/core/installer.js:1219-1243,1549-1552`; `.../ide/_config-driven.js:191,247-248,477-479`
- `templates/VSCode-AIDev02/image/etc/claude-code/managed-settings.d/10-retention.json:1-3`; `.github/contract-tests/test-73-claude-retention.sh:3-9,68-96,117-118`

### 2.4 Pinned tests

Source: research file 04 (`research/04-pinned-tests-57-46-19.md`) including its fix-cycle-1 finding-2 addendum (A.1 to A.11) and the fix-cycle-2 test-60 correction. No test was run for this research (scope guard); every "what it pins" statement comes from reading assertion code [CODE-VERIFIED by Read]. Paths are under `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.github/` unless stated. Variant labels are those of file 02 section 6: B1 skill written by `bmad/install.sh`, B2 skill seeded from `/etc/skel` or `/usr/local/lib/aidev`, B3 skill from a root `coder_script`, C `bmad` wrapper edit, D1 hook merged by `bmad/install.sh`, D2 managed-settings drop-in, D3 hook from a root `coder_script`, E `bmad install --directory ~`, F upstream user-scope install. In file 04's early sections the columns "B" and "D" mean B1 and D1.

**Where the tests run:** all five directly BMAD-related tests (test-57, test-46, test-19, test-49, test-52) run in one workflow, `workflows/coder-ci-aidev02-contract.yml` (job `contract_tests`, `runs-on: [self-hosted, big]`, `timeout-minutes: 20`, :492-500). test-52 runs runner-native before the image build (:832-847); the other four run in the "In-image contract tests (driver)" step (test-19 :1234, test-46 :1237, test-49 :1240, test-57 :1241 with `--network=none,--user=0`). The workflow triggers on pull requests touching `templates/VSCode-AIDev02/**` or `.github/contract-tests/**`, on push to `main`, nightly, `workflow_call` and dispatch (:5-60), so any change under those paths runs the whole gate. `test-startup-boot.sh` (35 `bmad` hits) runs from `coder-ci-validate.yml` and `coder-ci-orca-boot.yml` on a really booted workspace. No other workflow runs test-57, 46, 19 or 49.

**The one pin that bites writers into HOME: `test-57-catalogue-configure.sh:450` ("no seed: bmad writes nothing") [CODE-VERIFIED]:**

| Fact | Evidence |
|---|---|
| In test-57 "seed" means the git repo recorded in `~/.aidev/status/seed-repo-path` (fixture `mk_home`, :126-136); "no seed" means that file is removed (:446-448). That is the nearest analogue of a project that never had BMAD, but only when no seed is registered; a user-created project elsewhere is in no fixture | test-57:126-136,446-452 |
| `snap` is a whole-HOME comparison: `find` of every path under HOME with type and link target, a sha256 of every regular file, and the content of `*.configured` markers; excluded only `*/.git/index` and `./.aidev/installed/*`. The seed repo sits under HOME, so it is covered too | test-57:148-153 |
| So any new or changed path under HOME other than `.aidev/installed/*` on the no-seed path (for example `~/.claude/skills/...`, `~/.claude/settings.json`, `~/_bmad`) fails `test "$(snap "${H}")" = "${want}"`. Image-level paths (`/usr/local/bin`, `/etc`, `/catalogue`, `/opt`) are outside HOME and not covered | test-57:450 |
| Companion assertions: rc 0 (:449), marker written (:451), health stays `Installed-not-Configured` (:452) | test-57:449-452 |
| Seeded behaviour is richer than the research question assumed: the current installer DOES create `<seed>/_bmad/_config/manifest.yaml` in a registered seed repo and requires the seed's git status to stay empty | test-57:323-324,458 |
| Other seed guards: a seed with a bare `_bmad/` is left byte-unchanged and health is `Installed-not-Configured` (:413-419); tracked `.claude/skills/bmad-*` is skipped and `Configured` (:421-427); non-Git seed with manifest is not configured (:429-435); tracked-but-deleted skill is not configured (:437-444); dirty seed accepted (:454-459); user `_bmad-output/prior.md` kept (:462-465); second run byte-identical (:331-335); cold-run budget 30 s for bmad + ironclaude (:31,173-183) | test-57 lines as listed |

The test cannot tell the difference between a user-level write at install time and one at first use only through its fixture: artifacts created at first use (not by `install.sh`) and image-level changes do not break it.

**Pins that do not look at what the bmad installer writes [CODE-VERIFIED]:**

| Test | Pins | Source |
|---|---|---|
| test-46 | slug-name rules: the bmad marker and side marker survive deselection (:929-933), no bmad row in the reprofile report and the strict reader rejects one (:937-943,1092-1118; `spec2-health.sh:529`), readiness `bmad not-selected` when deselected (:1297-1298,1437-1446; `spec2-health.sh:562`), the summary string `Catalogue not configured: bmad,rd-u,rd-z` (:1479-1499), and that no real `health_check.command` is a marker/file-existence probe (production scan :1804-1815, self-test :1833 `bmad --version` is not a proxy). Its `bmad` directories are synthetic fixtures | `test-46-catalogue-health.sh` |
| test-19 | manifest declares `install_disposition` image-baked; `install.sh` shape classified IMAGE_BAKED: needs `command -v` and `exit 2`, and NO unquoted install verb (`npm install`, `npx `, `pip install`, etc.; regex :208-209, classifier :192-220, check :1137-1152; the quote strip is per line, :205); `type -P bmad` must be an executable file (:1175-1185); `bmad --version` exits 0 non-interactively (:1186-1190); `bmad --help` exits 0 within 10 s with stdin closed (:551-561); the welcome message must contain `bmad` and `bmad --help` (:517-529); invocation and help_command must be canonical commands, not marker or path shapes (:496-505) | `test-19-catalogue-cli-presence.sh` |
| test-49 | `catalogue/bmad/manifest.yaml` must exist at its path (:349-354, array :294-322, bmad at :310) and the listed files (also `Dockerfile.coder`, `startup.sh`, `spec2-health.sh`, `aienv.skel`, the contract workflow) must hold no non-comment line matching `coder create`, `coder templates push`, `coder delete`, `docker build`/`docker buildx build`, `terraform apply` (:355-399, regex :326). `bmad/install.sh` is not on the list | `test-49-spec2-evidence.sh` |
| test-52 | exact profile mapping: `orca` = `[claude-code, orca, ironclaude, bmad, mcp-bundle-core]` in that order, `minimal` = `[claude-code]`, `default_profile: orca` (:1378-1384); also the `orca_retirement` block text in `modules.tf` (no `count =`, keeps the orca literals, :1374-1377). A NEW slug in a profile breaks :1381-1383 | `test-52-browser-usability-evidence.sh` |

**Further pins on files that first-use mechanisms would edit (A.1 to A.8; 30 files matched the Grep, 15 relevant, 15 irrelevant with reasons):**

| Test | Pin | Source |
|---|---|---|
| test-1-catalogue-shape | every catalogue dir holds exactly `install.sh`, `manifest.yaml`, `module.tf`, no extras or dotfiles | `test-1-catalogue-shape.sh:25,43-67` |
| test-3-reserved-names | no `cp`/`ln -s` destination, alias or function named `preview`, `share`, `share-port`, `expose`, `dev-preview` in any `catalogue/*/install.sh`, `image/scripts/`, `image/bin/`, `scripts/` | `test-3-reserved-names.sh:27,55-90,151-198` |
| test-67 | every Dockerfile COPY source (not `--from`, not catalogue) must be in `image_input_files`; no dot-prefixed path under `image/`; context is `image/` | `test-67-image-inputs-cover-copies.sh:46-69,107-111`; `main.tf:80-101` |
| test-7-startup-order | exactly nine `# === section:N name ===` markers in fixed order (IDs 4, 5, 11 retired) | `test-7-startup-order.sh:34-44,90-101`; markers at `startup.sh:16,121,160,191,303,389,692,1348,1665` |
| test-60 | exactly one `COPY` line containing `codex-config.toml`, listing the three configs, ending `/usr/local/lib/aidev/` (`test-60:84-88`, that line is `Dockerfile.coder:547-548`); three exact `seed_if_absent` lines in section 6 (:89-93); production section 6 is executed on a fresh HOME with `set -e` (:139-152); the `claude` printf wrapper is extracted by awk (:161-257) | `test-60-llm-gateway-env.sh` |
| test-73-claude-retention | `10-retention.json` is exactly `{"cleanupPeriodDays": 90}`; exactly one COPY line equal to `COPY --chown=0:0 --chmod=0644 <rel> /<rel>`; a RUN with both `/etc/claude-code` and `/etc/claude-code/managed-settings.d` on one `install -d -m 0755` line (`Dockerfile.coder:474-475`); the merged managed tier's last `cleanupPeriodDays` is 90 | `test-73-claude-retention.sh:69-114,117-118,135-136` |
| test-51 | first `locals {` block of `modules.tf` keeps `_selected` and `_profiles[...]`; consumed-path oracle uses the `*.tf` glob; env-bridge names unique | `test-51:384-396,457-476,598-626` |
| test-startup-boot | `~/.aidev/installed/bmad` exists after boot (:2100-2108); in-profile configure steps sum to at most 75 s (:2129-2156); bmad with no seed is `Installed-not-Configured` (:2208-2235); fresh-home `~/.claude/CLAUDE.md` equals the `/etc/skel` copy (:2083-2087,3030-3037); F04 skel bridge list (:2774-2779); exactly one `aidev-startup` timing row and one agent (:617-637); lifecycle `ready` waits for every run-on-start script (:2631-2637); ledger slug/kind whitelists (:201,231-232,1968). No whole-HOME oracle exists there | `test-startup-boot.sh` |
| test-78 / upstream monitor | the three bmad version-string files must exist (`expected.txt:6-8`); `releases.json` has no bmad entry | `test-78-upstream-monitor.sh:90-99` |

**Impact summary (file 04 section 7 and A.10; X = certain break, c = break only under a stated condition):**

| Variant | Certain break | Conditional breaks |
|---|---|---|
| B1, D1, E, F (write inside HOME on the no-seed path from `install.sh` or a real install) | `test-57:450` | test-19 shape rule if the added text holds an unquoted install verb (`:1137-1152`); test-1-catalogue-shape if text goes into an extra file; the 75 s budget (`test-startup-boot:2129-2156`) for E/F; the marker write if a step aborts first |
| B2 (skel seed) | none | test-67 (new COPY not in `image_input_files`, or a hidden source path); test-3 (reserved words in the skill name); test-7 only if a new section is added; the fold into the `:547-548` COPY does not break test-60 |
| B3, D3 (root `coder_script`) | none | test-51 first-`locals` rule, test-52:1374-1377 `orca_retirement` pin (new resource must be separate), `test-startup-boot` timing display-name and convergence window |
| C (wrapper) | none | test-19 (`bmad` stays an executable file; `--version`/`--help` exit 0), test-60 `claude` printf extraction if that block is touched, test-49 lifecycle strings in `Dockerfile.coder`, test-71 duplicate `CG_VERSION=` line, test-67 for a new COPY |
| D2 (managed drop-in) | none | test-73-claude-retention (own COPY line per file, own valid JSON object, no `cleanupPeriodDays`), test-67 |
| A (documentation only) | none | test-19 welcome tokens `bmad` and `bmad --help` if the welcome text is rewritten; test-2 schema |

Delivery proof is missing for the cheap variants: no existing test asserts that a B2, B3, D2 or D3 artifact actually reaches HOME or the managed tier. File 04 A.11 lists the amended or new assertions (for B2: `test-startup-boot:2775` and `test-22:271-272` targets lists; for B3/D3: a block pin next to `test-52:1374-1377`; for D2: a second-file check in test-73-claude-retention). Health reads only the seed repo (`spec2-health.sh:99-114`), so no variant makes a user-created project report `Configured` unless `spec2-health.sh` and the `record_health` rows in test-57 change together.

**Contradiction and correction inside the research set:** file 04 section 7 and an earlier A.3 draft said a B2 skill should keep its own COPY line to protect test-60. That advice was withdrawn in fix cycle 2 (A.9): adding the skill source to the `Dockerfile.coder:547-548` COPY keeps test-60:87 true, and it costs no image layer, whereas an own COPY costs one of the two free layers (see section 2.2). File 02 addendum A5 and file 05 carry the same corrected rule.

**Stale documentation:** `docs/generated/PROJECT_INDEX.md:13,36,65` says contract tests are "T1-T55" [CODE-CONTRADICTED]: `.github/contract-tests/` holds `test-*.sh` up to `test-79-create-error-tail.sh`, with numbers 1 to 9, 59, 73 and 74 each used by two scripts, numbers 30 and 61 absent, and two unnumbered scripts (`test-b1-affordance-matrix.sh`, `test-startup-boot.sh`). The index header says it was generated 2026-09-25 against `origin/main` `1ace9c30`. Do not use "T1-T55" as the boundary of the pinned tests. The header wiring comments of test-57, 46, 19, 49, 52 are current [CODE-VERIFIED].

**Not read or not resolved (UNVERIFIED, carried from file 04):** whether the tests pass today (none run); `test-startup-boot.sh` was read only in its BMad, skel-bridge, ledger, timing and idempotency blocks; the `IDE_CONVERGENCE_TIMEOUT_S` value; the `manifest.schema.json` required-field list; `orca-build/repin.sh --verify` internals; which modes of test-52 reach the profile assertion at :1378; whether a COPY into `/etc/skel/.claude/skills/<name>/` creates intermediate directories at mode 0755 under the provider's legacy builder; the full test-1-tool-floor F08 fixtures after line 260; contents of `slug-configuration.md` (test-57:6, relied on the test code instead).

**Evidence:**
- `.github/contract-tests/test-57-catalogue-configure.sh:4-18,31,75-79,126-158,173-183,323-324,331-342,413-465`
- `.github/contract-tests/test-46-catalogue-health.sh:847-958,1092-1118,1184-1197,1284-1318,1419-1499,1804-1833`
- `.github/contract-tests/test-19-catalogue-cli-presence.sh:192-220,496-561,1106-1190`; `.github/contract-tests/test-49-spec2-evidence.sh:294-399`; `.github/contract-tests/test-52-browser-usability-evidence.sh:1374-1384`
- `.github/contract-tests/test-1-catalogue-shape.sh:25,43-67`; `test-3-reserved-names.sh:27,55-198`; `test-67-image-inputs-cover-copies.sh:46-115`; `test-7-startup-order.sh:34-101`; `test-60-llm-gateway-env.sh:84-169`; `test-73-claude-retention.sh:69-136`; `test-51-selector-onboarding-wiring.sh:384-626`; `test-startup-boot.sh:617-637,2083-2235,2631-2637,2774-2779`
- `.github/workflows/coder-ci-aidev02-contract.yml:3-60,492-500,832-847,1234-1245`
- `docs/generated/PROJECT_INDEX.md:3,13,36,65`

### 2.5 Documents and the owner-decision trail

Source: research file 05 (`research/05-startup-boot-test-docs-and-decision-trail.md`) including its fix-cycle-1 finding-1 matrix and finding-8 re-tag, and the Gate 1 user-approved correction recorded in its X1/X2 evidence. Every quote was read from the cited file by the research agent; the tag judges the architectural claim against code, not whether the quote exists. Paths are relative to `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/`.

**The statement of record (OD-1) and what the code shows:**

| Path | Line | Statement | Tag |
|---|---|---|---|
| `_bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md` | 5 | "OD-1 BMad placement \| **Cancelled.** BMad is installed per project only, never globally." | "per project" [CODE-VERIFIED]: the only `bmad install` call site is `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:42`, aimed at the seed repo. Literal "never globally" is [CODE-CONTRADICTED] for the CLI, which IS installed globally (`Dockerfile.coder:139` `npm install -g bmad-method@6.9.0`, wrapper at :142-143); it is true only for the framework content (`_bmad/`, `.claude/skills/bmad-*`, `_bmad-output/`) |
| `.../spec-orca-bundle-gap-closure/.memlog.md` | 32 | "BMad must be installed per project and never globally or at user level. OD-1=A is void. CAP-1 is retired and its ID is never reused." | same |
| same | 27 | "OD-1 resolved by owner: A, user-level BMad ... the seed repo gets no _bmad/." | [CODE-CONTRADICTED] (the seed repo does get `_bmad/`, `install.sh:42,46`) and voided by line 32; [STALE DOC] kept as history |
| same | 33-34 | "The BMad slug keeps #207's per-project seed behaviour unchanged ..."; "BMad added as a non-goal" | [CODE-VERIFIED] boot behaviour unchanged (`install.sh:21-55`) |
| `.../spec-orca-bundle-gap-closure/SPEC.md` | 12, 29, 77 | derives from `.memlog.md`, do not hand-edit (12); CAP-1 retired, ID not reused (29); "Any BMad change ... BMad stays a per-project seed install, exactly as #207 built it" (77) | process rule; record; [CODE-VERIFIED] |
| `.../spec-orca-bundle-gap-closure/fr-audit.md` | 12 | "FR-6 ... CANCELLED by owner ... none (BMad stays per-project)" | [CODE-VERIFIED] in substance; cited `install.sh:38-66` is [CODE-CONTRADICTED] (file has 61 lines, seed block is 21-55) [STALE DOC] |
| `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md` | 65, 126, 141, 142, 166, 174 | no seed means nothing configured and the welcome gives the one-command path (65); "User repos stay clean" (126); BMad in repos cloned after boot and in Orca worktrees is a non-goal (141); multiple repos non-goal (142); owner accepts writes into seed repos of `agile-full` and `orca` (166); BMad in Orca worktrees is an open scope expansion (174) | 65 and 126 [CODE-VERIFIED] but cover only the seed and boot, not first-use creation in a non-seed repo; 141's "worktrees carry only tracked files" is git behaviour, UNVERIFIED; 166's profile `agile-full` does not exist (`profiles.yaml:15-21` has `orca`, `minimal`) [CODE-CONTRADICTED] [STALE DOC] |
| `.../spec-orca-catalogue-bundle/slug-configuration.md` | 53 | "Without it, 6.9.0 creates a literal `{output_folder}/` directory." | Re-tagged in fix cycle 1: NOT contradicted. The line sits under the command at :51, which passes `--user-name`, so it describes the partial-seed branch (`ui.js:807-837`, `official-modules.js:1387-1409` `return configValue \|\| match`); mechanism [CODE-VERIFIED], on-disk outcome UNVERIFIED. Every first-use command must keep `--output-folder _bmad-output` |
| same | 54 | "A user-level install is broken: 73 skill files hard-reference `{project-root}/_bmad/...`" | qualitative claim [CODE-VERIFIED] (75 files in package `src/` contain `{project-root}/_bmad`, 40 of them `SKILL.md`); the count "73" and "broken in practice" are UNVERIFIED |
| `_bmad-output/planning-artifacts/prds/prd-Coder-orca-bundled-catalogues-2026-09-24/addendum.md` | 75-76 | Option A user-level availability (lead); Option B auto-scaffolding into each Project rejected | Option A [CODE-CONTRADICTED] by shipped code and the 2026-09-25 cancellation [STALE DOC]; Option B's rejected reasons (writes to owner repositories, conflicts with committed BMAD) are the same risks first-use creation carries |

**Shipped files that state or imply the rule (all [CODE-VERIFIED] unless marked):** `catalogue/bmad/manifest.yaml:7,12-14` (welcome text with the manual command for other repos, see section 2.2); `catalogue/bmad/install.sh:2-3,23,41`; `startup.sh:673` (single writer of `seed-repo-path`; a first-use mechanism must not write it), `:1114-1117` (BMad marker is "an explicit owner-decision exception"), `:1170-1176`; `templates/VSCode-AIDev02/README.md:241` ("`Default` (Orca, IronClaude, BMad, core MCP servers; pre-selected) ..."; true per `profiles.yaml:16-18` and `parameters.tf:104`, silent on where or when BMad is configured); `templates/VSCode-AIDev02/README.md:308` is only an example directory name. No BMad rule is stated in `docs/operations/aidev02-operator.md`, the root `README.md`, `SECURITY.md` or `CHANGELOG.md` (no BMad entry exists; the #207 seed install has none).

**How decisions are recorded here (for whoever writes the new entry):**

| Item | Fact | Source |
|---|---|---|
| Contract | `SPEC.md` and its `companions:` are the contract and `SPEC.md` is derived from `.memlog.md` | `spec-orca-bundle-gap-closure/SPEC.md:3-8,12` |
| Log | `.memlog.md` has front matter (`updated: 2026-09-25T15:49`) and typed bullets `(event)`, `(decision)`, `(constraint)`, ...; owner decisions are `(decision) Owner <date>: ...` lines; append-style (the void line 27 stays) | `.memlog.md:1-34` |
| Table | `owner-decisions.md` holds `OD-1..OD-3` in a three-column table; next free ID is `OD-4`; capabilities `CAP-1..CAP-7`, next free `CAP-8` (IDs are per spec; `spec-aidev02-v2` uses CAP-8 for something else); a retired ID is never reused | `owner-decisions.md:1-7`; `SPEC.md:29,31-60` |
| Order of edits | memlog bullet first, then the `OD-4` row plus a pointer in OD-1's Consequence cell, then re-derive `SPEC.md`, then a cross-reference bullet in the catalogue-bundle `.memlog.md` | derived by file 05 section (c) |
| CHANGELOG | Keep a Changelog 1.1.0 and SemVer 2.0.0; new work goes under `## [Unreleased]` (`### Added` / `### Changed`) as `- **Bold title** (#issue): prose`; a catalogue-file change earns a retag note (`CHANGELOG.md:6-9,20-285`) | `CHANGELOG.md` |
| Issue number | the folder name `.dev/issues/478/` (untracked); that 478 is the GitHub issue to cite is UNVERIFIED | `.dev/issues/478/accuracy-check.md:16` |

**The decision as available to the researchers (G-26):** the exact 2026-11-07 wording exists only at `BUILD-REQUEST.md:14` (outside the research files); the researchers saw it only as "BMAD should create its needed directories on first use", with no wording on git cleanliness (hide through `info/exclude` or leave visible), and whether it covers Orca-created worktrees is not stated (catalogue-bundle `SPEC.md:174` speaks of "project"). The "never globally" half of OD-1 is not reversed; research-notes F9-4 and the gaps file record that per-project creation (`bmad install --directory <project>`) does not conflict with it. The task's label "OD-1" is the one used in `owner-decisions.md:5` and `.memlog.md:32`, but the same label appears for other matters at `test-57-catalogue-configure.sh:10,992,1034` and `startup.sh:1114` (gaps G-23, UV-29). Those are decision-trail facts, so the words "first-use" and "supersede" in this report apply only to first-use creation, never to a global or user-level install, which stays declined.

**Documentation-claim checks against code (file 05 section (d)):**

| Claim | Result |
|---|---|
| "BMad is installed ... CLI `bmad`, npm package `bmad-method`" (`manifest.yaml:9-10`) | [CODE-VERIFIED]: `bmad --version` printed `6.9.0`; `Dockerfile.coder:139-143` |
| The manual command's flags (`manifest.yaml:13-14`) | flags and the `claude-code` tool id exist [CODE-VERIFIED] (`commands/install.js:14-37`); a missing `--directory` target is accepted if the nearest existing parent is writable, and `~` is accepted (`ui.js:1414-1463,1568-1581`); that the command completes end to end is UNVERIFIED (running `bmad install` was forbidden) |
| `NPM_CONFIG_OFFLINE=true` stops `npm view` | [CODE-CONTRADICTED] for `bmad install --list-tools`, which still printed the "6.12.4 available" box (cause UNVERIFIED, probably npm cache) |
| The rendered welcome file | `~/.aidev/status/welcome/bmad.txt` exists in the live workspace and equals the manifest text (written atomically at `startup.sh:1189-1206`) |
| This workspace's seed | `~/.aidev/status/seed-repo-path` does not exist here, so the seed-case runtime was not observed |
| Memlog claims (quick-update dirties 6 files; 6.9.0 over 6.10.0 downgrades 41 files) | UNVERIFIED by file 05 (no install run); recorded as prior-review observation, not re-run, in file 01 section 2.1 above |

**README and tooling constraints that bound any wording change (CODE-VERIFIED):** `templates/VSCode-AIDev02/README.md` is outside `image/` (no retag) and is linted by `markdownlint-cli2` (`.markdownlint-cli2.yaml:9-82`; files under `**/bmad*/**`, `_bmad/`, `_bmad-output/` are ignored); line 241 is a five-cell table row; lines 96-101 must not be reflowed because `.github/upstream-monitor/releases.json:111-114` anchors `upstream GitHub CLI release v` and `verify_release.py:159-165` matches by line content. The README is not part of the image (`main.tf:119`, `README.md:20-22`), so a workspace user reads the baked `/catalogue/bmad/manifest.yaml` and `~/.aidev/status/welcome/bmad.txt`, not the template README. Any edit of a file under `image/catalogue/` retags the image (`main.tf:74`). Renovate extracts `bmad-method` at three sites that must keep their shape: `Dockerfile.coder:139`, `catalogue/bmad/install.sh:18`, `catalogue/bmad/manifest.yaml:2` (`.github/upstream-monitor/expected.txt:6-8`; `renovate-global.json5:44-58`); a new file that copies the version string would not be bumped unless added to the pattern at `renovate-global.json5:54` and to `expected.txt`.

**Live-boot test (`test-startup-boot.sh`) in the decision context:** it has no case that runs `bmad install`, checks `_bmad/` or invokes the binary; it consumes boot records only (marker :2100-2127, 75 s timing :2129-2156, health state :2208-2227, clean seed after a fresh clone :2089-2098, projection allowlists :200-234). It skips `bmad` in the deselected-slug loops (:2482-2528), so a deselected BMad marker is permitted but not pinned; that open question (`sprint-status-orca-gap-closure.yaml:42`) is separate. The reconciled matrix (file 05 addendum F1.2 and F1.3, with file 04 A.10) is reflected in section 2.4: the single certain break is `test-57:450` for B1, D1 and for E and F when run from `install.sh` at boot; a first-use action running after boot is executed by no existing test. Corrected in the Gate 1 exception: variant C is not invisible to test-57, because `install.sh:42` runs `bmad install` through the baked wrapper in every seeded run (`test-57:173-178,323-324,457-459`).

**Contradictions and stale items surfaced from file 05:** `owner-decisions.md:5` literal "never globally" vs the global CLI (`Dockerfile.coder:139`); `.memlog.md:27`; `fr-audit.md:12` line numbers; catalogue-bundle `SPEC.md:34,166` profile `agile-full`; PRD addendum Option A and its `.memlog.md:13`; `slug-configuration.md:54` count "73" (not reproduced); file 05's own earlier wording "B and D leave every row unchanged" (corrected to distinguish stub delivery from first-use execution, see 2.4); file 04 test-49 row wording (`C-F1-1`: `test-49:294-322` does not list `catalogue/bmad/install.sh` or `modules.tf`, and fails only on a non-comment lifecycle-string line, `test-49:326`).

**Evidence:**
- `_bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md:1-7`; `.../.memlog.md:1-34`; `.../SPEC.md:3-12,29,31-60,77`; `.../fr-audit.md:12`
- `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md:34,65,126,139-142,166,174`; `.../slug-configuration.md:48-55`; `.../.memlog.md:20,66,81-82,95-96`
- `_bmad-output/planning-artifacts/prds/prd-Coder-orca-bundled-catalogues-2026-09-24/addendum.md:75-76`; `_bmad-output/implementation-artifacts/sprint-status-orca-gap-closure.yaml:23,42`
- `templates/VSCode-AIDev02/README.md:20-22,96-101,237-242,308`; `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:2,7,9-14`; `.markdownlint-cli2.yaml:9-82`
- `.github/contract-tests/test-startup-boot.sh:200-234,2082-2227,2482-2528`; `.github/upstream-monitor/expected.txt:1-8`; `.github/upstream-monitor/renovate-global.json5:44-58`; `.github/upstream-monitor/releases.json:104-114`
- `CHANGELOG.md:6-24,232,285`; `.dev/issues/478/accuracy-check.md:16`

### 2.6 Current State Summary

**Flow from workspace boot to a user starting BMAD in a project, with and without a seed.** Every box is backed by a code-read cited in 2.1 to 2.5; nothing here is a document-only claim. "(not run)" marks flow read from code and CI logs, never observed end to end in this research.

```
 Coder starts workspace (home volume /home/coder persists; rest from image)
        |
        v
 coder_script.startup (run_on_start) -> aidev-startup = image/scripts/startup.sh
   startup.tf:42-63        sections 1,2,3,6,7,8,9,10,12 re-run EVERY start
        |
        +-- s6 : seed_if_absent  -> ~/.claude/CLAUDE.md only (no skills, no settings)
        +-- s8 : clone REPO_URL  -> writes ~/.aidev/status/seed-repo-path (sole writer)
        |
        v
 s9 catalogue slugs, LC_ALL=C order (profile `orca` only; `minimal` = claude-code only)
        |
        +-- bmad/install.sh  (own timeout 120, no 30 s watchdog)
        |      |
        |      +-- guard 1: no seed-repo-path OR not a git work tree
        |      |       --> "nothing to configure", write marker, exit 0
        |      |           health = Installed-not-Configured
        |      |           [PROJECT WITHOUT A SEED: nothing is created anywhere]
        |      |
        |      +-- guard 2: <seed>/_bmad exists (any entry) OR tracked .claude/skills/bmad-*
        |      |       --> "left untouched", write marker, exit 0   (partial _bmad/ lands here)
        |      |
        |      +-- else (SEED WITHOUT BMAD):
        |              info/exclude += /_bmad/ /_bmad-output/ /.claude/skills/bmad-*/
        |              NPM_CONFIG_OFFLINE=true bmad install --yes --directory <seed>
        |                --modules bmm --tools claude-code --output-folder _bmad-output ...
        |              requires _bmad/_config/manifest.yaml; git status must be unchanged
        |              marker; health = Configured (reads ONLY the seed repo)
        |
        +-- ironclaude/install.sh : superclaude install (first boot or new IronClaude sha)
               --> user-level hooks, settings defaults, packaged skills in ~/.claude
               (no bmad-* skill; user-level skills left alone by name)
        |
        v
 /usr/local/bin/bmad  = 2-line wrapper: exec node .../bmad-method/tools/installer/bmad-cli.js "$@"
   (pin bmad-method@6.9.0, Dockerfile.coder:139-143; no first-use logic, no _bmad check)

 ---------------------------------------------------------------------------------
 USER STARTS CLAUDE CODE IN A PROJECT (BMAD skills load from <project>/.claude/skills)
 ---------------------------------------------------------------------------------
   Project = the seed repo, configured at boot        Project = any other project, never had BMAD
   -----------------------------------------------    ---------------------------------------------
   <p>/_bmad/{_config,core,bmm,scripts,custom}        no _bmad/, no .claude/skills/bmad-*, no
   <p>/_bmad-output/{planning,implementation}-...     _bmad-output/, no docs/ created by BMAD
   <p>/docs/ and <p>/.claude/skills/bmad-*            ~/.claude/skills has NO bmad-* entry (live
   (hidden from git by info/exclude)                  check); BMAD 6.9.0 has no bootstrap and no
   skills find resolve_config.py + config.toml        skill tells the user to run `bmad install`
                                                              |
                                                              v
                                          only path today: user runs the manual command from the
                                          baked welcome text (manifest.yaml:12-14), from the
                                          project root, unguarded (no version or existing-tree
                                          check outside the slug):
                                          bmad install --yes --directory . --modules bmm
                                            --tools claude-code --output-folder _bmad-output
                                                              |
                                                              v
                                          creates the same tree as the seed (section 2.1); in a
                                          git repo the new files show as untracked (no exclude)
```

**What the diagram deliberately does not contain:** any first-use mechanism. None exists in the repo, BMAD 6.9.0 or the image; every hook point found (user-level skill, wrapper edit, Claude Code hook, root `coder_script`, managed drop-in) is a candidate studied in the research, not current architecture, and is left to the options sections. Facts that depend on Claude Code behaviour (loading of user-level skills, mid-session discovery of new project skills, hook and permission semantics) were not decided by research files 01 to 05 and are UNVERIFIED here.

**Summary table (current state):**

| Area | Current behaviour | Evidence | Relevance to first-use creation | Status |
|---|---|---|---|---|
| BMAD CLI in the image | `bmad-method@6.9.0` global npm package behind a 2-line `exec node` wrapper; every start fires a best-effort `npm view` | `Dockerfile.coder:139-143`; `bmad-cli.js:20-35` | wrapper has no first-use logic; any change is class (i) image rebuild | [CODE-VERIFIED]; image contents UNVERIFIED (G-18) |
| `bmad install` | non-interactive form needs `--yes` and `--tools`; writes only inside `--directory`; no git calls, no `~/.claude` writes, no HOME writes on the bmm-only path | `ui.js:630-641,838-867`; section 2.1 | a per-project install can be driven non-interactively and offline for `bmm` | [CODE-VERIFIED]; never executed (G-10, G-15) |
| What a fresh install creates | `_bmad/` (config, scripts, core, bmm, custom), `_bmad-output/{planning,implementation}-artifacts/`, `docs/`, `.claude/skills/bmad-*` (46 skills by Glob and one prior review) | `official-modules.js:548-707`; `module.yaml:44-47` | this is the directory set to create on first use | code-read; exact files and count UNVERIFIED (G-10, G-11) |
| Upstream user-scope install | `global_target_dir` has zero readers (option F has no code path in 6.9.0); `ancestor_conflict_check` is never enabled; no `--global` flag. A home-directory install (option E, `--directory ~`) would, by code reading, write `~/_bmad` and `~/.claude/skills/bmad-*` but leave a project that has `.git` and no `_bmad` without its own `_bmad/`, because `find_project_root` stops at the project (not run) | `platform-codes.yaml:9-12,57`; `_config-driven.js:191`; `resolve_customization.py:58-66`; file 01 section 6 | the global route is not available and would conflict with the "no global install" constraint and with OD-1's "never globally" half | F [CODE-VERIFIED]; E write set UNVERIFIED (G-16); later upstream versions UNVERIFIED (G-05) |
| Skill runtime | needs project `_bmad/` (scripts, `config.yaml`, `config.toml`, `bmad-help.csv`); `resolve_config.py` exits 1 without `_bmad/config.toml`; `resolve_customization.py` degrades silently; no skill detects a missing `_bmad/` | section 2.1 | first use cannot rely on BMAD to bootstrap itself | [CODE-VERIFIED]; model behaviour UNVERIFIED (G-07) |
| Boot-time slug | seed repo only, once per start, guarded by `_bmad` existence and tracked skills; a failed run leaves a partial `_bmad/` that is skipped forever | `install.sh:21-55,41` | no hook for projects other than the seed; partial trees are never repaired | [CODE-VERIFIED] |
| Version skew | no installer version gate; `--yes` over any existing `_bmad/` (even partial) is quick-update; a prior review measured 6.9.0 downgrading a 6.10.0 tree (41 files, rc 0) | `ui.js:217-262`; `existing-install.js:50-66,111`; `04-bmad.md:37` | any mechanism running `bmad install --yes` needs its own first-use predicate, and the manual welcome-text command has none | mechanism [CODE-VERIFIED]; counts prior-review observation, not re-run |
| First-use predicate (proposed) | `FIRST_USE(P)`: P = git top, `_bmad` absent, no `.claude/skills/bmad-*` on disk, writable | file 03 A2 | a definition for the report, nothing implemented | defined; no-`.git` behaviour UNVERIFIED (G-10) |
| Health and readiness | read only the seed repo; a first install elsewhere changes nothing they report; states recompute once per boot | `spec2-health.sh:99-114` | no option makes another project report `Configured` without changing `spec2-health.sh` and test-57 together | [CODE-VERIFIED] |
| HOME and user-level surfaces | HOME is a per-workspace volume; user-level skills and hooks are written only by superclaude, Orca and removal by `specstory-cleanup`; `superclaude install --force` leaves non-packaged skill names and foreign hook commands alone | `main.tf:174-176`; section 2.3 | a user-level artifact persists but a new workspace starts empty; no IronClaude or IronOrca edit is needed to add a skill or hook (that would change only if the artifact were shipped from IronClaude, or a future superclaude started pruning unknown skill dirs, file 03 line 180) | [CODE-VERIFIED] |
| Pinned tests | the single certain break is `test-57:450` (whole-HOME snapshot, no seed) for B1, D1 and for E and F run from `install.sh`; other variants carry BREAKS-IF conditions; no test executes a first-use action and none proves delivery for B2, B3, D2, D3 | section 2.4 | a replacement or added assertion is required for any boot-time stub | [CODE-VERIFIED]; no test run |
| Image layer budget | 68 of 70 layers (CI log), two free; B2 and D2 as written cost one each, a fold or an in-place edit costs none | `coder-ci-aidev02-contract.yml:1016-1029`; file 02 A5 | a +1 option must name the budget it spends and re-read the latest `main` count before merge | CI log read, Sysbox arm UNVERIFIED (G-19) |
| Decision trail | OD-1 / `.memlog.md:32` / `SPEC.md:77` bind; a new entry is `OD-4` plus a memlog `(decision)` bullet plus re-derived `SPEC.md`; `owner-decisions.md:5` "never globally" is inexact for the CLI | section 2.5 | the 2026-11-07 wording on git cleanliness and Orca worktrees is not available (G-26) | [CODE-VERIFIED] trail; owner wording UNVERIFIED |
| Feasibility | feasible without a global BMAD install and without an IronClaude or IronOrca change on the evidence so far; the choice among B, C, D cannot yet be determined because it depends on Claude Code behaviour (G-01, G-02) and on the owner's reading of "user level" and "first use" (gaps log section 5; these two owner questions are carried to the owner-questions section, not answered here) | gaps log section 6 | stop-condition in research-notes not triggered | stated by the gaps log from research lines 79, 217, 219, 386, 501 and research-notes F9-4 |
| Prior-review figures | install "about 4 s" with an npx fetch in a scratch HOME vs `cold bmad` 374-392 ms in CI (baked CLI, no network, one-file repo); the two are not one measurement | file 01 F5-C, F5-E | duration inside a real workspace is unknown (G-09) | prior-review observation, not re-run |

**Contradictions between research files, and which finding has the stronger evidence:**

| # | Contradiction | Stronger finding |
|---|---|---|
| 1 | File 01 section 7.5 (the `python3 {project-root}/...` steps and a `customize.toml`-only fallback) vs file 03 A5 (41 lines in 31 files; fallback in 25 of 31; fallback reads three TOML files) | file 03 A5: it counted the `python3 ` lines directly; file 03 itself flags one correction as unspelled (gaps log CC-14, which of its "both" corrections is the second is UNVERIFIED) |
| 2 | Files 02, 04, 05 tag option F's mechanism UNVERIFIED; file 01 shows zero readers of `global_target_dir` | file 01 (whole-package Grep, 43 hits in one file, reproduced by the analyst: gaps log G-25) |
| 3 | File 04 section 7 ("B" and "D" break `test-57:450`) vs file 05's first draft ("B and D leave every row unchanged") | the reconciled matrix in file 05 F1.2 and F1.3: B1, D1 (and E, F run from `install.sh`) break it; B2, B3, D2, D3 do not; first-use execution breaks nothing |
| 4 | File 05's first-draft reading (F1.1) that variant C is invisible to test-57 | file 05 X2 as corrected in the Gate 1 exception: `install.sh:42` runs `bmad install` through the baked wrapper in every seeded run |
| 5 | File 04 A.3 first draft (keep a B2 skill on its own COPY line) vs fix cycle 2 | fix cycle 2 (`test-60:87-88`): a fold into `Dockerfile.coder:547-548` does not break test-60 and costs no layer |
| 6 | Memlog "offline, about 4s" vs CI `cold bmad` 374-392 ms | neither is wrong; different configurations (file 01 F5-C, F5-3 UNVERIFIED cause) |
| 7 | `Dockerfile.coder:468` "no headroom" vs `:229` "two spare" and CI 68 of 70 | the CI log (68 of 70); `:468` stands only as policy |
| 8 | Memlog `:21` "`--yes` without `--output-folder` creates literal `{output_folder}/`" vs `ui.js:838-861` | quote it as the prior review's wording; the mechanism lives in the partial-seed branch (file 01 F5-C1; file 05 finding 8 re-tag) |
| 9 | Immaterial line-count differences: `install.sh` 61 vs 62 lines, `manifest.yaml` 29 vs 30 (gaps log G-28) | none needed |

No contradiction affects the verdict on the question that this file frames: the installer, the slug, the tests and the decision trail all agree that today nothing creates BMAD directories outside the seed repo at boot.


---

## Self-Audit (not a report section)

**What I actively checked**
- Read in full, in order: research files `01` (531 lines, including the fix-cycle-1 addendum F5-A to F5-H), `02` (454 lines, including the Sysbox layer addendum A1 to A8), `03` (365 lines, including addendum A1 to A5), `04` (541 lines, including addendum A.1 to A.11), `05` (417 lines, including addendum F1.1 to F1.6), and `gaps-and-questions.md` (321 lines, all eight sections). Research files `web-01`, `web-02` and `research-notes.md` were not assigned and were not read; the few facts taken from research-notes (F9-4, F9-5 items) come only through the gaps log and are labelled as such.
- The Summary and Key Takeaways blocks of files 01 to 05 and the gaps-log Summary were each traced into this file. Traced: 01 (non-interactive command, `--yes` and `--tools`, no network for `bmm`, git untouched, created paths, nothing under `~/.claude`, `global_target_dir` inert, ancestor check dead, skills need project `_bmad/`, `resolve_config.py` exit 1 vs silent degrade, no bootstrap, Python 3.11, 6.10.0 tree as corroboration only, `install.sh:42` flags, partial `_bmad/`, memlog and CI figures, partial-seed branch, version skew) into 2.1 and 2.6; 02 (wrapper, seed-only slug, health seed-only, rebuild classes, layer budget, three-file rule, `minimal` profile, hazards for hooks) into 2.2; 03 (HOME volume, boot order, superclaude merge semantics, writers, `block-bare-python.sh`, `FIRST_USE(P)`, M1 to M4, no other-repo change) into 2.3; 04 (single certain break `test-57:450`, pins in test-19/46/49/52, extra pins, stale "T1-T55", variant matrix) into 2.4; 05 (decision trail, OD numbering, README and Renovate constraints, doc-claim checks, reconciled matrix) into 2.5; the gaps log (feasibility, owner questions, gap IDs, contradictions) into 1 and 2.6.
- Searches and checks run: Glob of `research/` and `synthesis/` (found the eight research files and an empty synthesis directory); Grep of the gaps log for `OD-1|issue 478|#478|2026-11-07` to source Section 1; Grep of the output for headings, for `TODO|TBD|PLACEHOLDER|[fill|XXX` (0 matches) and one spot-check Grep of `catalogue/bmad/install.sh` confirming the exact `bmad install` command at line 42. I did not re-read the BMAD package, the tests or the workflow files; every code and line citation is carried from the research files.

**Excluded from this file, with rationale (nothing dropped silently)**
- Per-option walkthroughs (file 03 A3), option risk rows (file 01 F5-F), per-variant layer-cost and assertion proposals (file 02 A5, file 04 A.11), README wording and CHANGELOG entry advice (file 05): these are option-analysis or plan material for the options, recommendation and implementation sections; the constraints they rest on are in 2.2 to 2.5, and the matrices are summarised in 2.4.
- Web research (web-01, web-02): not used; Claude Code behaviours are marked UNVERIFIED and no external source is cited.
- Owner questions (gaps log section 5), design questions D-1 to D-17 and the run-only facts R-1 to R-15: carried to the owner-questions and implementation sections; the ones that bound the current state (G-09 to G-11, G-13, G-16, G-26) are cited by ID.
- Detailed gap rows G-20 to G-22, G-27, G-28 (test and environment residuals, documentation hygiene): listed in the gaps log; only their effect on tags is reflected here.

**Contradictions and tag decisions**
- Nine contradictions or stale items are tabled in 2.6 with the stronger finding named. Tag decisions: option F uses file 01's CODE-VERIFIED tag (gaps log G-25); the `{output_folder}` line is quoted, not restated as a bare-`--yes` defect (finding 8); the test-60 fold uses the fix-cycle-2 rule; variant C is shown as visible to test-57 per the Gate 1 exception, which the gaps log records as accepted without a fourth review (G-30), so that one correction has weaker review coverage than the rest.
- Version-mismatched facts (OBSERVED-FROM-6.10.0-TRACKED-TREE) appear only as corroboration in 2.1 and are not used to describe what a fresh 6.9.0 install creates; that description rests on installer code tagged CODE-VERIFIED.
- Zero documents-only claims are shown as fact: the Claude Code behaviours that came from documentation (permission prompting, hook semantics, mid-session skill loading) are marked UNVERIFIED or doc-sourced, and nothing doc-only is drawn in the diagram.
- Immaterial inconsistencies left as in the sources: `install.sh` 61 vs 62 lines, `manifest.yaml` 29 vs 30 lines, 21 vs 22 `settings.json.bak*` files, and file 01 line 18 ("`node --version` not run") vs 3.3 ("OBSERVED via `node --version`"); the last is gaps log G-28 and I did not rely on it.

**Why I believe nothing was dropped or invented:** each table row cites a path and line carried from a research file, I introduced no new facts, and I reported the figures that differ between files (counts, line numbers, tags) as differences rather than choosing silently. Limits of this audit: I did not independently re-verify the code citations against source beyond the one `install.sh:42` check, so any error in a research file would be carried through; zero fabricated content is my belief, not a proof.
