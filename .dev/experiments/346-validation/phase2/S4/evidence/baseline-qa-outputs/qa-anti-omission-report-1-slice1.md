# Anti-Omission Report (slice 1 of 3)

This report covers the slice assigned on task-file line 447 (research files 01 and 02, synthesis files synth-01 and synth-02). It is written to the `-slice1` path because `qa-anti-omission-report-1.md` already holds another agent's report.

**Status:** Complete
**Date:** 2026-11-07

---

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md` (read line by line: l.1-570 and l.986-1763; l.571-985 checked by headers and ID/phrase greps, see Self-Audit; line numbers below are that file's lines at the time of reading).

Legend: R = REPRESENTED (report line cited); D = COVERED-BY-DEDUP (merged into the named report item); O = OMITTED (see Omissions table, id O-n). "R/O" = part of the finding is represented and a distinct remainder is omitted. Method: coverage judged by meaning, not by cited IDs.

## Enumeration

### File 1: research/01-bmad-6-9-0-installer-and-skill-runtime.md

| # | Finding (short) | Status | Report location / note |
|---|---|---|---|
| 01-01 | No `bmad install` was run; no observed 6.9.0 install | R | l.78, 94 |
| 01-02 | Only four allowed `bmad` commands run, with `NPM_CONFIG_OFFLINE=true` | R | l.78 |
| 01-03 | Package `bmad-method` 6.9.0, bins, `engines.node >=20.12.0` | R | l.78 |
| 01-04 | Host Node v24.22.2 (path-derived) satisfies the engine floor | O | O-16 |
| 01-05 | Update check on every invocation: `npm view`, 5 s, errors swallowed, advisory banner, cache cause UNVERIFIED | R | l.99, 165, 423 (CC-22) |
| 01-06 | Worktree `_bmad` trees are 6.10.0, corroboration only | R | l.137 |
| 01-07 | Option definitions for `--directory`, `--modules`, `--tools`, `--yes`, `--set`, `--output-folder`, `--user-name` | R | l.81, 553-560 |
| 01-08 | Remaining option inventory (`--action`, `--custom-source`, `--channel` family, `--debug`, language flags, `--list-*` early exit) | O | O-3 |
| 01-09 | Action control flow: WSL check, `--set` validation, cancel exit 0, quick-update branch, exit 0/1 | O | O-4 |
| 01-10 | `--list-tools` observed: 44 IDs, claude-code starred, other starred tools | O | O-1 |
| 01-11 | `--list-options` observed keys, user-scope marks, defaults (`project_name`, artifacts paths) | O | O-2 (`project_knowledge` default `docs` is R, l.94) |
| 01-12 | Key takeaways: version, `--tools` mandatory, `project_knowledge` default | R | l.81, 94 |
| 01-13 | Grep table of `global_target_dir`/HOME hits (comments, 41 values, doc example, cache readers, `~` expanders) | D | conclusion at l.105, 99; per-hit table O-7 |
| 01-14 | Re-check without exclusions: 43 hits in exactly one file | R | l.105 |
| 01-15 | Conclusion: zero consumers, option F has no code path | R | l.105, 1163 |
| 01-16 | HOME touched only for `~/.bmad/cache/*` and `~` expansion; no `~/.claude` write | R | l.97, 99 |
| 01-17 | Call-chain steps: uv probe warn-only, `--directory` validation, existing-install detection, `--tools` fatal error, config seeding, `skipPrompts` | R | l.81, 99, 121-131, 422 |
| 01-18 | Call-chain steps: `core` always prepended to modules; `_cleanupSkillDirs` after IDE step | O | O-4 |
| 01-19 | Minimal non-interactive flag set `--directory --modules bmm --tools claude-code --yes` with evidence | R | l.81, 553 |
| 01-20 | Optional extras stay non-interactive; `--directory` avoids prompt; `--action` only for existing installs | R | l.1456 (3.1), 899 (W02-6) |
| 01-21 | `--modules bmm` optional under `--yes` (default list), registry default UNVERIFIED | R | l.671 (G-12), 1456 |
| 01-22 | Install is never silent (logo, uv check, summary), no `--quiet` | R | l.81 (`--quiet`); "never silent" wording O-4 (minor) |
| 01-23 | `--tools` alone without `--yes` still prompts | R | l.81 |
| 01-24 | Existing `_bmad` plus `--yes` defaults to quick-update | R | l.127-129 |
| 01-25 | 3.2a partial-seed branch rows 1-7 (keys landing in config) | R | l.121 |
| 01-26 | Consequence: `project_name`/language keys unwritten, skills read them, fallback text differs by skill | R | l.118, 121 |
| 01-27 | Keep `--output-folder _bmad-output` in every first-use command | R | l.121, 560, 1013 |
| 01-28 | Any one of four core flags selects the partial-seed branch; only a flagless `--yes` seeds all five keys (capitalised OS username, dir basename, English x2, `_bmad-output`) | O | O-5 |
| 01-29 | `project_name` can only be set non-defaulted via `--set`, file patched UNVERIFIED | R | l.666 (G-07), l.1723 |
| 01-30 | Built-in `core`/`bmm` resolved from package, no clone | R | l.99 |
| 01-31 | Network call-site inventory (git clone, npm in cloned modules, `fetchNpmVersion`, `channel-resolver`, `version-resolver` none) | O | O-6 |
| 01-32 | Node floor; `uv` not required | R | l.81 |
| 01-33 | Real install duration UNVERIFIED; what the time consists of | R | l.135 |
| 01-34 | Installer makes no git call on the target; no `.gitignore` edit except `_bmad/custom/.gitignore` | R | l.89, 99, 607 (SC-10) |
| 01-35 | First real run on a non-git directory UNVERIFIED | R | l.669 (G-10) |
| 01-36 | Created-path table: `_bmad/` and subfolders | R | l.87 |
| 01-37 | `_bmad/scripts/` copies (and excluded test/cache files) | R | l.88 |
| 01-38 | `custom/.gitignore` and empty `custom/config*.toml` stubs | R | l.89 |
| 01-39 | `core/` and `bmm/` module copies and `config.yaml` files | R | l.90 |
| 01-40 | `_bmad/config.toml`, `config.user.toml` | R | l.91 |
| 01-41 | `_config/` manifest, skill-manifest, files-manifest (sha256), bmad-help.csv | R | l.92 |
| 01-42 | `_bmad-output/{planning,implementation}-artifacts/`, `_bmad-output/` only as parent | R | l.93 |
| 01-43 | `docs/` default `project_knowledge`, only if absent | R | l.94 |
| 01-44 | `.claude/skills/bmad-*/` target dir | R | l.95 |
| 01-45 | `{output_folder}` substitution traced by reading, not observed | R | l.121 |
| 01-46 | Not created: `.git`, `.gitignore` edit, `CLAUDE.md`, settings, commands, anything under `~/.claude` | R | l.97 |
| 01-47 | HOME follow-up trace: only two `ensureDir` of cache paths; others test existence; bmm resolves before cache | R | l.99 |
| 01-48 | Registry `bmad-modules.yaml` read locally, no network (`listAvailable`) | O | O-6 |
| 01-49 | IDE handlers built only from platform entries with an `installer` block | O | O-8b |
| 01-50 | claude-code entry values; no `commands_target_dir`, `suspended`, `ancestor_conflict_check` | R | l.105-106, 1163 |
| 01-51 | Skill write path always `projectDir/target_dir`; `global_target_dir` never read | R | l.95, 1163 |
| 01-52 | Verbatim skill copy; dotfile and backup-file filter | R/O | copy R (l.95); filter O-8b |
| 01-53 | Existing `<canonicalId>` dir removed before copy | O | O-8a |
| 01-54 | Cleanup removes only previously installed set or `removals.txt`; `bmad-os-*` preserved; non-BMAD skills untouched | R/O | non-BMAD R (l.97); `bmad-os-*` and rule O-8a |
| 01-55 | After IDE step skill source copies under `_bmad/<module>` are deleted | O | O-8a |
| 01-56 | Tools sharing a `target_dir`: first writes, peers skip | O | O-8b |
| 01-57 | claude-code-only install writes only `.claude/skills/<skill>/` (no settings, commands, CLAUDE.md) | R | l.97 |
| 01-58 | Option F conclusion (needs reader and option; later upstream UNVERIFIED) | R | l.1163, 664 |
| 01-59 | `findAncestorConflict` mechanics (walk from parent to root excluding it, ownership rule, `rm -rf` message, HOME walked) | D | F-11 (l.656), l.106; mechanics O-9 |
| 01-60 | No platform sets `ancestor_conflict_check`; check never runs | R | l.106, 656 |
| 01-61 | Option E implications 1-4 (not blocked, write set, no per-project `_bmad`, violates constraint) | R | l.1148, 1157 |
| 01-62 | `resolve_config.py`: `--project-root` required, no walk-up, exit 1 message, exit 3, stdlib only | R/O | l.113-115; stdlib-only and four-layer merge O-11 |
| 01-63 | `resolve_customization.py`: `--skill`, `customize.toml` required, `find_project_root`, skill-dir-first rationale, optional overrides | R/O | l.114; required-file exit 1 and rationale O-12 |
| 01-64 | Contrast: config hard-fails, customization silently degrades | R | l.113-114, 1012 |
| 01-65 | User-level skill under `~/.claude/skills`: lookup starts at HOME, HOME not git and no `~/_bmad` (observed) | O | O-13 |
| 01-66 | `memlog.py init` creates parents; refuses to overwrite | R/O | mkdir R (l.116); refusal O-14 |
| 01-67 | 46 `SKILL.md` (13 core, 33 bmm) | R/O | 46 R (l.97, 117); split O-15 |
| 01-68 | 39 of 46 reference the scripts (52 matches); corrected from 40/92 | R | l.117 |
| 01-69 | 37 load `{project-root}/_bmad/{bmm,core}/config.yaml` | R | l.117 |
| 01-70 | Invocation forms (`python3` vs `uv run`), script path anchored on `{project-root}/_bmad/scripts` | R | l.117, 278 |
| 01-71 | Written fallbacks on script failure and for config load | R | l.118, 278 |
| 01-72 | `{project-root}` defined as the project working directory | R | l.1148 |
| 01-73 | Other `_bmad` dependents: memlog.py callers, `bmad-help.csv` | R | l.116, 518 |
| 01-74 | No skill detects missing `_bmad/` or says run `bmad install` (one non-instruction hit) | R | l.119 |
| 01-75 | Consequence of first use with skills but no `_bmad/` (a to d) | R | l.119, 1012 |
| 01-76 | Python 3.11+ requirement, exit 3 | R | l.115 |
| 01-77 | Host tooling: uv 0.11.8, python 3.13.5 and 3.11.15 observed | D | l.115 ("3.11 and 3.13"); versions O-16 |
| 01-78 | Bare `python3` refused by user hook in the research session; 6.10.0 `bmad-help` uses `uv run --python 3.11` | R/O | hook R (l.276); in-session refusal O-16; version difference R (l.137) |
| 01-79 | Key takeaways s7: skills need project-local `_bmad/`; nothing lazily creates it | R | l.119, 1012 |
| 01-80 | s8 manifest of tracked tree: version 6.10.0, install date; `lastUpdated`, modules built-in, `ides` incl. openhands | R/O | version and date R (l.137, 699); rest O-17 |
| 01-81 | Tracked counts: 17 `_bmad`, 577 `_bmad-output`, 237 skills in 47 dirs | R | l.137 |
| 01-82 | Manifest commit history (four commits) | O | O-17 |
| 01-83 | Tracked `_bmad` file listing | O | O-17 |
| 01-84 | `agent-manifest.csv` absent from 6.9.0 package, so tree is not 6.9.0 output | R | l.137 |
| 01-85 | `custom/bmad-retrospective.toml` is project-authored, not installer output | O | O-17 |
| 01-86 | `_bmad-output` in worktree holds project documents; only two dirs match installer | O | O-17 |
| 01-87 | Version difference of `bmad-help/SKILL.md:26` | R | l.137 |
| 01-88 | 8.1 catalogue installer summary rows (command, guards, exclude, failure mode, `timeout 120` assumption, manual text) | R | l.170-184, 1456 |
| 01-89 | Failed run leaves partial `_bmad/` (InstallPaths first, manifest later, no rollback) | R | l.123, 131, 184 |
| 01-90 | U1 to U13 (duration, banner source, subprocess side effects, default module list, `resolve_customization` output, interpreter error text, user-level skill loading, hook in other workspaces, later upstream, Dockerfile bake, exact files, skill count, missing-key behaviour) | R | l.661-689 (G-01 to G-11), l.1717-1735 |
| 01-91 | C1 to C3 (platform-codes comment, agent-manifest, worktree bmad-help) | R | l.137, 139, 698 |
| 01-92 | Open questions 1-3 (atomic creation, guard on `config.toml`, which dir is project) | R | l.1696, 1700, 726 (4.4) |
| 01-93 | Stale docs: `platform-codes.yaml:9` and `:10`, worktree trees, welcome text | R | l.139, 697-698 |
| 01-94 | `tools/installer/README.md` searched but not read in full | O | O-18 |
| 01-95 | `--tools` help text confirmed accurate against `ui.js:630-641` | R | l.81 |
| 01-96 | Summary paragraph and question-to-section map | R | l.1321 (feasibility), section 2.1 |
| 01-97 | F5-A: memlog lines 20 and 21 quoted with origin "(04 review)" | R | l.133, 436, 541 |
| 01-98 | F5-A: memlog line 81 (decision: offline via `NPM_CONFIG_OFFLINE`, proven by `--network=none` test) | O | O-19 |
| 01-99 | F5-A: 04 probe method (`npx bmad-method@6.9.0`, throwaway repos, scratch HOME) | R | l.135 |
| 01-100 | F5-A: probe sizes (`_bmad/` 160K, skills 2.4M), "46 skills", `.npm` only under HOME | R/O | 46 and `.npm` R (l.97, 99); sizes O-19 |
| 01-101 | F5-A: about 4 s includes npx fetch; about 1 s re-run | R | l.135 |
| 01-102 | F5-A: offline install with dead proxy exited rc=0 (separate run); `--offline` origin UNVERIFIED | R/O | origin R (l.673, 1730); dead-proxy run O-19 |
| 01-103 | F5-A: quick-update re-run rewrites 6 files (timestamps, reordered keys, added keys) | R/O | count R (l.133); content O-19 |
| 01-104 | F5-A: 6.9.0 `--yes` over 6.10.0 downgrades manifest, 41 files, rc 0 | R | l.133, 520 |
| 01-105 | F5-A: `{output_folder}` defect scope; quote do not restate | R | l.121, 700 (CC-04) |
| 01-106 | F5-B: driver-table 7th column passes `--network=none`; split into docker opts | R/O | `--network=none,--user=0` R (l.318); parse mechanics O-19 |
| 01-107 | F5-B: test refuses to pass if network reachable (`getent`, default route); same precondition on three other rows | O | O-19 |
| 01-108 | F5-B: `cold bmad` log line source; timer wraps whole `install.sh` (upper bound, includes `chown`) | R/O | l.135, 329; upper-bound and `chown` O-19 |
| 01-109 | F5-B: fixture (`mk_home`), 30 s budget, existence checks, no skill-count assertion | R | l.324-329 |
| 01-110 | F5-B: negative fixtures (bare `_bmad`, tracked skills, non-git, deleted skill) | R | l.329 |
| 01-111 | F5-B: test never installs over 6.10.0 and checks no version | R | l.645 (guard tested only on placeholder trees) |
| 01-112 | F5-B: test gives no file list or skill count, so cannot close U11/U12 | D | G-10/G-11 (l.669-670) |
| 01-113 | F5-C: three CI runs `374/392/392 ms` | R | l.135 |
| 01-114 | F5-C: `cold ironclaude` 4392-4513 ms; memlog "about 4s" is nearer ironclaude | O | O-19 |
| 01-115 | F5-C: CI numbers are one fixture/one runner, order of magnitude | R | l.135, 668 |
| 01-116 | F5-C: PASS means offline rc 0 and manifest written; caveat: cannot tell "no `npm view`" from "failed quietly" | R/O | offline R (l.606); caveat O-19 |
| 01-117 | F5-C: baked CLI ran; closes U10 Dockerfile half; "symlink" stale words | R | l.139, 163 |
| 01-118 | F5-C: `04-bmad.md` Dockerfile line refs stale (360 vs 139) | R | l.139, 701 |
| 01-119 | F5-D: version-skew code path rows (`findBmadDir`, `ExistingInstall.detect`, quick-update default, no version gate, installer writes own version, partial `_bmad` not nothing) | R | l.123-133, 645 |
| 01-120 | F5-D: guard `install.sh:24` skips any `_bmad`; test-57 proves skip on placeholder content; untested tracked-only seam | R | l.177, 286, 329, 645 |
| 01-121 | F5-E: narrowed U1, U10, U11, U12 | R | l.135, 163, 668-670 |
| 01-122 | F5-E: CI discards installer output (`>/dev/null`), so no skill line or file list in CI log | O | O-19 |
| 01-123 | F5-E: suggested report wording | D | reflected in l.133-135 |
| 01-124 | F5-F: risk row "6.9.0 over existing 6.10.0 or partial tree" for B, C, D (protections and seams) | D | common fact 11 (l.1021), F-04 (l.645), 4D.3, 3.3, 7.8 (l.1616) |
| 01-125 | F5-G: 12 further UNVERIFIED (F5-1 to F5-12) and 3 stale (F5-C1 to C3) | R | G-14, G-15, G-17, G-18 rows; l.700-701 |
| 01-126 | F5-H summary (two memlog statements need careful wording) | R | l.121, 135 |

### File 2: research/02-image-cli-and-catalogue-slug.md

| # | Finding (short) | Status | Report location / note |
|---|---|---|---|
| 02-01 | Dockerfile BMad layer: pin `npm install -g bmad-method@6.9.0` (exact semver, host-network build) | R | l.161 |
| 02-02 | Wrapper not a symlink because bin is `#!/usr/bin/env node` and NVM node not on default PATH (PATH claim UNVERIFIED) | R | l.223, 1117 |
| 02-03 | Layer runs `USER root` then `USER 1000`; `chmod 0755`; wrapper two lines | R | l.161-162 |
| 02-04 | `chown -R 1000:1000 "$NVM_DIR"` (global npm tree owned by workspace user); `node_bin`/`cli` derivation | O | O-20 |
| 02-05 | Other `bmad` mentions in Dockerfile.coder: only line 277 telemetry comment | O | O-20 |
| 02-06 | Wrapper on this machine matches Dockerfile; no logic (no cwd, `_bmad`, env, bootstrap) | R | l.162, 168 |
| 02-07 | Exec'd CLI facts: package version equals pin, bins, `bmad-cli.js` update check, subcommands loaded from `commands/` (install, status, uninstall), version, help | R | l.163-164, 1105 |
| 02-08 | Nothing in `bmad-cli.js` looks for `_bmad/` | R | l.164 |
| 02-09 | Four permitted commands and results (`--version` 6.9.0, help option list, 44 tool IDs, `--list-options`) | R/O | l.78; 44-ID and option listing O-1, O-2, O-3 |
| 02-10 | Anomaly: update box printed under `NPM_CONFIG_OFFLINE=true`; 6.12.4 UNVERIFIED | R | l.165, 423 |
| 02-11 | Key takeaways (a): wrapper has zero first-use logic; first-use change is image rebuild; `npm view` each start | R | l.168, 514 |
| 02-12 | install.sh header, shebang, `set -euo pipefail`; slug, log, marker, seed-path file | R | l.174 |
| 02-13 | install.sh:18 `command -v bmad` else exit 2; message says "symlink" (stale) | R | l.175, 139 |
| 02-14 | Guard 1: no seed or not a git work tree: marker, exit 0 | R | l.176 |
| 02-15 | Guard 2: `_bmad` exists or tracked bmad skills: untouched, marker | R | l.177 |
| 02-16 | Exclude-file handling: three patterns appended unless present | R | l.178 |
| 02-17 | Before/after `git status` compare; fail on change; no clean-tree pre-check; dirty seed accepted | R | l.179 |
| 02-18 | Single install call with flags, `timeout 120`, `</dev/null`; non-zero incl. 124 is FAIL | R | l.180 |
| 02-19 | `_bmad/_config/manifest.yaml` must exist afterwards | R | l.181 |
| 02-20 | Marker write, `chmod 0644`, `install ok`, exit 0 | R | l.182 |
| 02-21 | Exit-code table: 0/1/2 plus `set -e` exits (`mkdir`, `git rev-parse --git-path`) | R/O | 0/1/2 R (l.175-181); `set -e` exits O-20 |
| 02-22 | No top-of-file marker-plus-affordance short-circuit (compare ironclaude, README contract) | R | l.184, 646 |
| 02-23 | Failure paths exit before marker but leave `_bmad` and excludes; next boot becomes "untouched" pass | R | l.184 |
| 02-24 | Installer only targets the one seed repo | R | l.184, 66 |
| 02-25 | Footprint hidden by script; other repos would show untracked | R | l.193 |
| 02-26 | Run method: subshell, no 30 s bound, own `timeout 120`, `workspace`/`hybrid` scopes, once per agent start | R | l.184 |
| 02-27 | Key takeaways (b): boot-time seed-only, single call, exit codes, marker rule | R | l.184 |
| 02-28 | Upstream CLI facts table: `--directory` expansion/validation, `findBmadDir`, existing-install menu, platform-codes entry | R | l.127, 422 |
| 02-29 | `global_target_dir` no readers; `ancestor_conflict_check` never enabled | R | l.105-106 |
| 02-30 | Installer creates its own directories (`_config/`, scripts dir) | R | l.87-88 |
| 02-31 | Manual command in welcome text differs from `install.sh:42` in three ways | R | l.193 |
| 02-32 | Option E passes directory validation; writes `~/_bmad` and `~/.claude/skills`; UNVERIFIED | R | l.1148 |
| 02-33 | `manifest.yaml` field table (name, version, scope, disposition, display, welcome, depends_on, paths, health, discoverability) | R | l.191 |
| 02-34 | Welcome-text claim checks (installed, seed hidden via exclude, flags exist, health finite, test-19 tokens) | R | l.194, 338, 421-422 |
| 02-35 | "Already set up there" is unconditional (C7) | R | l.194, 650 |
| 02-36 | `module.tf` only provider and `agent_id`; no `coder_app`; header says future launch surface a clean diff | R/O | l.195; header-comment remark O-20 |
| 02-37 | Three-file rule for `catalogue/bmad/` | R | l.190 |
| 02-38 | `profiles.yaml`: bmad only in `orca`; `minimal` none; `default_profile: orca` | R | l.196, 1020 |
| 02-39 | Form-side profile list is hand-copied from `profiles.yaml` (`parameters.tf:92-93`) | O | O-21 |
| 02-40 | `profiles.yaml:1` path comment stale | R | l.223, 702 |
| 02-41 | Terraform wiring: `modules.tf` yamldecode, `active_slugs`, `module "bmad"` count | R | l.196 |
| 02-42 | `coder_parameter "profile"` default `orca`, `mutable`, option text names BMad | O | O-21 |
| 02-43 | `coder_env "aidev_profile"` exports `AIDEV_PROFILE`; `startup.sh:715` `aidev_cat_root` | O | O-21 |
| 02-44 | `COPY catalogue /catalogue` is the last COPY (file 595 lines) | R | l.209, 1081 |
| 02-45 | `catalogue_sha256` feeds `image_inputs_sha256`, tag, rebuild trigger; `image_input_files` and test-67 | R | l.203, 1052 |
| 02-46 | Root `.tf` files outside `image/` are not in the image hash | R | l.203-204 |
| 02-47 | README contract cross-check rows: three-file, slug name, scope enum, disposition, installed-only, idempotency, subshell statement | R/O | idempotency and subshell R (l.223, 646); enum/disposition/test-5 allowlist O-22 |
| 02-48 | README stale paths, relative links, reference links; `startup.tf:30` stale | R | l.223, 703-704 |
| 02-49 | Key takeaways (c): slug shape, retag classes, contract has no first-use hook | R | l.197, 203 |
| 02-50 | `spec2-health.sh` table: requirements, observed (manifest or tracked skills), classify, validate (bmad never Partially) | R | l.211 |
| 02-51 | Strict reader needs current boot's invocation id | R | l.211 |
| 02-52 | `reprofile_read` rejects `bmad` row; `readiness_write` deselected `bmad` not-selected | R | l.337 (test-46 row), 215 |
| 02-53 | Health recomputed after install.sh each boot; record not updated within the session | R | l.211 |
| 02-54 | bmad state table (minimal, no seed, bare `_bmad`, manifest, tracked skills) | R | l.213-219 |
| 02-55 | First-use install in the seed repo itself would flip state only at the next boot | D | l.211 (once per start, invocation id) and F-07 (l.648) |
| 02-56 | First-use outside the seed is invisible; `Partially` impossible; readiness line stays "not configured" | R | l.211, 648, 1016 |
| 02-57 | Key takeaways (d) | R | l.211, 648 |
| 02-58 | Shared facts s6.0: build context, tag hash, root `.tf` not hashed, `coder update`, HOME volume, skel copy-if-absent, §9 order, Renovate strings, health seed-only | R | l.203-205, 221, 1018 |
| 02-59 | B1: step between line 55 and 58, inline heredoc, contract statements stretched | R/O | l.1071, 1092; "opt-in" manifest wording and `install.sh` header purpose O-23 |
| 02-60 | B2: new COPY to `/etc/skel/.claude/skills`, `image_input_files`, `seed_if_absent`, not slug-gated (also `minimal`) | R | l.1071, 1082, 1092 |
| 02-61 | B3: root `coder_script` modelled on `orca_retirement`, template push, README silent on `coder_script` | R | l.1071, 1083, 1092 |
| 02-62 | Orca precedent for user-level skill writes; bmad excluded from deselect cleanup (orca install has 300 s bound) | R/O | l.221, 1092; 300 s bound O-20 |
| 02-63 | Instruction-text channel (`aidev_claude_md_block_sync`, hard-coded markers, no BMad text in seed CLAUDE.md) | R | l.221, 1178 (Option G) |
| 02-64 | Option C hook point: `Dockerfile.coder:142` group; `claude` printf wrapper precedent | R | l.1104, 1112 |
| 02-65 | Option C rebuild class: later layers rebuild incl. SHA-pinned binary downloads via host-network legacy builder | O | O-24 |
| 02-66 | Option C new wrapper command; discoverability needs welcome text | R | l.1098, 1506 |
| 02-67 | Option C persistence: none in HOME | R | l.1115-1116, 1641 |
| 02-68 | Option C contract statements to keep (`--version`, invocation, help, `command -v`, install pass-through, pin literal) | R | l.1105, 1108, 1505 |
| 02-69 | Option C limit: fires only when `bmad` runs, not on skill invocation (UNVERIFIED) | R | l.1106 |
| 02-70 | Option C stretches: "opt-in", image-wide, `minimal` profile too | R | l.1113, 1508 |
| 02-71 | Option D1: jq merge modelled on ironclaude, IronClaude `/.claude/hooks/` predicate collision, no lock, symlink replace, failure on vanished hooks | R | l.1130, 1516, 1519 |
| 02-72 | Option D2: managed-settings drop-in, root-owned, image-wide, hooks acceptance UNVERIFIED, outside IronClaude predicate | R | l.1131, 1141, 1520 |
| 02-73 | Option D3: root `coder_script`, `jq` in image, same risks | R | l.1121, 1139 |
| 02-74 | D1/D3 stretch install.sh scope and "opt-in" manifest wording; blast radius every session | R/O | blast radius R (l.1132, 1518); manifest wording O-23 |
| 02-75 | Summary table 6.4 (B, C, D variants by rebuild class and HOME persistence) | R | l.1079-1083, 1225-1241 |
| 02-76 | Option E facts (exists, validates, `~/_bmad`, class (iii), global-style) | R | l.1148, 1153 |
| 02-77 | Option F facts (data only; pin change touches three strings; 6.12.4 UNVERIFIED) | R | l.1163, 1167 |
| 02-78 | Key takeaways (e): cheapest classes B3/D3, only B/D act where Claude Code is used, strongest hazard D, none change health | R | l.1299, 1312, 1016 |
| 02-79 | Gaps U1-U14 (14 UNVERIFIED items) | R | l.661-689, 1717-1738 |
| 02-80 | C1-C7 CODE-CONTRADICTED items | R | l.139, 223, 650, 702-704 |
| 02-81 | Open questions 1-4 (minimal coverage, deselect rule, failed first install, Renovate strings) | R | l.1697, 1700, 1701, 726 |
| 02-82 | Stale-doc list (symlink, profiles path, README paths, `startup.tf:30`, PATH claim, welcome text) | R | l.223, 697-704 |
| 02-83 | Summary paragraph (wrapper, slug, health, rebuild classes, hazards) | R | l.168, 514-528 |
| 02-84 | A1 gate: step, command, fails above 70, only enforcement point | R | l.206 |
| 02-85 | A1 gate comment: "76 layers started, 78 hit Sysbox relative overlay-path bug", 70 is a chosen margin, not a Docker limit; Dockerfile comment to remove ceiling once upstream fixes | O | O-25 |
| 02-86 | A2 current count 68 of 70 on two CI runs (method read-only; run on this worktree's sha); decision record agrees; Sysbox arm UNVERIFIED | R | l.207, 1019 |
| 02-87 | A3 independent count: 61 instruction lines = 1 FROM + 60 (31 RUN, 29 COPY), no ADD; base image 8 layers is inference | R/O | base-8 inference R (l.678, 1735); instruction counts O-25 |
| 02-88 | A4 comments: `:229` "two spare" matches; `:468` "no headroom" contradicted as measurement, true as policy | R | l.208, 678 |
| 02-89 | A4 reconciliation: older `ARCHITECTURE-SPINE.md:93` "main at 70"; `docs/development-guide.md:66` repeats the fold policy; comments left unedited (later plan) | O | O-25 |
| 02-90 | A5 per-option layer cost: B1, B3, D1, D3 zero; B2 +1 or fold; C in place 0, late-COPY fold; D2 +1 (test-73 pin) | R | l.209, 1081-1083, 1235, 1507, 1520 |
| 02-91 | A5 totals: B2 + D2 would reach exactly 70, a third layer fails; race with other PRs | R | l.1088, 1595, 1600 |
| 02-92 | A6 verdict: "blocked" marking too strong, "constrained"; ordering by layer cost; name the budget spent and re-read latest main before merge | R | l.209, 525, 1595 |
| 02-93 | A7 gaps U15 to U20 and C8 | R | l.678, 1735, 1272 |
| 02-94 | A8 summary | R | l.209, 525 |

### File 3: synthesis/synth-01-problem-current-state.md

Note: sections 1 and 2.1 to 2.6 of this file are carried into report sections 1 and 2.1 to 2.6 almost verbatim (verified by reading both side by side). Two intentional edits in the report are corrections, not omissions: 2.3's last paragraph now points to Section 5 for the Claude Code answers, and 2.5's live-boot paragraph replaces the earlier "skips `bmad` in deselected loops" sentence with the re-read result (`:2446-2479`). The "Self-Audit (not a report section)" blocks of both synthesis files are excluded by design (assembler omits them); they hold no distinct findings.

| # | Finding (short) | Status | Report l. |
|---|---|---|---|
| S1-01 | Question: per-project creation without global install; "never globally" half stays; CLI is global | R | 61 |
| S1-02 | Current-state one-liners: seed-only boot install | R | 66 |
| S1-03 | No seed: nothing configured, marker only, `Installed-not-Configured` | R | 67 |
| S1-04 | Other projects need the manual welcome-text command | R | 68 |
| S1-05 | BMAD 6.9.0 has no self-bootstrap | R | 69 |
| S1-06 | User unaware of manual command; welcome file exists | R | 70 |
| S1-07 | Trigger: 2026-11-07 decision, wording only at `BUILD-REQUEST.md:14`, three-way split, REPORT.md lines overtaken | R | 72 |
| S1-08 | Scope note of the file (sections 1-2 only) | D | 72 (no separate text needed) |
| S1-09 | 2.1 intro: package, no install run, four commands | R | 78 |
| S1-10 | Non-interactive command, `--yes`, `--tools`, no `--quiet`, no `uv` need | R | 81 |
| S1-11 | Created-path table (9 rows) | R | 85-95 |
| S1-12 | Not created list; non-BMAD skills untouched; prior-review 46 skills | R | 97 |
| S1-13 | Git and HOME: no git on target, no HOME write on bmm path, npm cache residual, built-in no network | R | 99 |
| S1-14 | Dead hooks: `global_target_dir` 43 hits one file | R | 105 |
| S1-15 | Dead hooks: `ancestor_conflict_check` | R | 106 |
| S1-16 | No `--global`/`--user` flag | R | 107 |
| S1-17 | Runtime: `resolve_config.py` | R | 113 |
| S1-18 | Runtime: `resolve_customization.py` | R | 114 |
| S1-19 | Runtime: Python 3.11, exit 3 | R | 115 |
| S1-20 | Runtime: `memlog.py` | R | 116 |
| S1-21 | Runtime: 39/46 and 37 counts | R | 117 |
| S1-22 | Runtime: fallbacks written into skills | R | 118 |
| S1-23 | Runtime: no skill detects missing `_bmad` | R | 119 |
| S1-24 | Partial-seed branch and `--output-folder` rule; memlog phrase contradicted | R | 121 |
| S1-25 | Version skew table (5 rows) | R | 125-131 |
| S1-26 | Prior review: downgrade 41 files, 6 files rewrite | R | 133 |
| S1-27 | Duration figures not blended | R | 135 |
| S1-28 | Tracked 6.10.0 tree corroboration only | R | 137 |
| S1-29 | Contradictions from file 01 (platform-codes, symlink, line refs) | R | 139 |
| S1-30 | 2.1 evidence list | R | 141-151 |
| S1-31 | 2.2 wrapper table (6 rows) | R | 159-166 |
| S1-32 | Wrapper cannot fire on skill invocation (UNVERIFIED) | R | 168 |
| S1-33 | `install.sh` line table (10 rows) | R | 172-182 |
| S1-34 | Failure leaves partial `_bmad`; no short-circuit; run method | R | 184 |
| S1-35 | Welcome/slug table (8 rows incl. three-file, manifest fields, differences, "already set up", module.tf, profiles, no first-use field) | R | 188-197 |
| S1-36 | Rebuild classes and layer budget table (7 rows) | R | 201-209 |
| S1-37 | Health observes only seed repo; never Partially; recompute per start | R | 211 |
| S1-38 | Health state table (5 rows) | R | 213-219 |
| S1-39 | Precedent and hazards (Orca skills, claude-md block, IronClaude predicate, Renovate strings) | R | 221 |
| S1-40 | File 02 contradictions and stale docs | R | 223 |
| S1-41 | 2.2 evidence list | R | 225-230 |
| S1-42 | 2.3 HOME persistence table (5 rows) | R | 238-244 |
| S1-43 | Boot order table (9 rows) and idempotency, no direct writes, bmad exemptions | R | 248-260 |
| S1-44 | Writers table (5 rows) | R | 264-270 |
| S1-45 | Live `~/.claude` observations (42 skills, 54505-byte settings, 14 hooks, managed drop-in) | R | 272 |
| S1-46 | `superclaude install` overwrite/merge semantics and hazards | R | 274 |
| S1-47 | `block-bare-python.sh` facts (41 lines, 31 files, 25/6 fallback) | R | 276 |
| S1-48 | Contradiction files 01 vs 03 | R | 278 |
| S1-49 | FIRST_USE facts table (7 rows) | R | 282-290 |
| S1-50 | `FIRST_USE(P)` definition, command, no-`.git` open, monorepo owner call | R | 292 |
| S1-51 | Install output strings; no `permissions` key; open Claude Code questions | R | 294 |
| S1-52 | Placement facts M1-M4 | R | 298-303 |
| S1-53 | 2.3 evidence list | R | 305-313 |
| S1-54 | 2.4 where tests run (workflow, job, timeouts, triggers, `test-startup-boot` workflows) | R | 318 |
| S1-55 | `test-57:450` snapshot rows (6 rows) and seeded behaviour | R | 324-329 |
| S1-56 | test-57 cannot tell first-use writes apart | R | 331 |
| S1-57 | test-46 pin row | R | 337 |
| S1-58 | test-19 pin row | R | 338 |
| S1-59 | test-49 pin row | R | 339 |
| S1-60 | test-52 pin row | R | 340 |
| S1-61 | Further pins: test-1, test-3, test-67, test-7, test-60, test-73, test-51, test-startup-boot, test-78 (9 rows) | R | 346-354 |
| S1-62 | Impact summary table (6 variants) | R | 358-365 |
| S1-63 | Delivery proof missing for B2, B3, D2, D3 | R | 367 |
| S1-64 | Contradiction: B2 own COPY advice withdrawn | R | 369 |
| S1-65 | Stale "T1-T55" | R | 371 |
| S1-66 | Not read or not resolved (file 04) | R | 373 |
| S1-67 | 2.4 evidence list | R | 375-381 |
| S1-68 | 2.5 OD-1 table (9 rows incl. line 27, 33-34, SPEC lines, fr-audit, catalogue-bundle SPEC, slug-configuration 53/54, PRD addendum) | R | 389-400 |
| S1-69 | Shipped files that state or imply the rule; README:241/308; no BMad rule elsewhere | R | 402 |
| S1-70 | How decisions are recorded (5 rows) | R | 406-413 |
| S1-71 | Decision as available to researchers (G-26) | R | 415 |
| S1-72 | Documentation-claim checks (6 rows) | R | 419-426 |
| S1-73 | README and tooling constraints; Renovate sites | R | 428 |
| S1-74 | Live-boot test context and reconciled matrix | R | 430 (re-read and corrected) |
| S1-75 | Contradictions and stale items from file 05 | R | 432 |
| S1-76 | 2.5 evidence list | R | 434-440 |
| S1-77 | 2.6 flow diagram (boot to project, with and without seed) | R | 446-506 |
| S1-78 | Diagram deliberately has no first-use mechanism | R | 508 |
| S1-79 | Summary table rows (14) | R | 512-528 |
| S1-80 | Contradictions between research files (9 rows) | R | 532-542 |
| S1-81 | Closing verdict: nothing creates BMAD directories outside the seed at boot | R | 544 |

### File 4: synthesis/synth-02-target-gaps-external.md

Note: sections 3, 4 and 5 are carried into report sections 3, 4 and 5 verbatim (row counts verified: 16 SC rows l.598-613, 12 K rows l.621-632, 11 F rows l.642-652, 30 G rows l.660-689, 26 grouped CC/SD rows l.697-722, 19 W01 and 18 W02 findings). Each ID below was located in the report.

| # | Finding (short) | Status | Report l. |
|---|---|---|---|
| S2-01 | Target comes from one decision (2026-11-07; supersedes OD-1 for first use; global not requested) | R | 549 |
| S2-02 | Desired behavior: one image-baked, pinned, offline per-project command | R | 553-560 |
| S2-03 | `--output-folder` stays because `--user-name` is passed | R | 560 |
| S2-04 | Global half: no content at HOME; E and F excluded by code; three-way split of ask | R | 561 |
| S2-05 | "First use" undefined; table of three readings and mechanisms | R | 562-568 |
| S2-06 | Trigger predicate FIRST_USE(P) proposal | R | 570 |
| S2-07 | Boot path stays as built (plan assumption D-9) | R | 571 area |
| S2-08 | Target-state flow diagram incl. skills visibility | R | 573-596 |
| S2-09 | SC-01 directories exist after first use | R | 598 |
| S2-10 | SC-02 manifest and `config.toml` exist | R | 599 |
| S2-11 | SC-03 skill count equals installer's N | R | 600 |
| S2-12 | SC-04 no literal `{output_folder}` dir | R | 601 |
| S2-13 | SC-05 nothing at HOME | R | 602 |
| S2-14 | SC-06 untouched project byte-unchanged; test-57:450 | R | 603 |
| S2-15 | SC-07 existing BMAD not rewritten | R | 604 |
| S2-16 | SC-08 second run changes nothing | R | 605 |
| S2-17 | SC-09 exit 0, no network, duration recorded | R | 606 |
| S2-18 | SC-10 git rule explicit | R | 607 |
| S2-19 | SC-11 failed-run behaviour stated and tested | R | 608 |
| S2-20 | SC-12 skills invocable, single step told to user | R | 609 |
| S2-21 | SC-13 pinned tests updated, new test (per-variant paragraph) | R | 610, 615 |
| S2-22 | SC-14 layer gate at or below 70 | R | 611 |
| S2-23 | SC-15 health wording unchanged | R | 612 |
| S2-24 | SC-16 decision recorded as OD-4 etc. | R | 613 |
| S2-25 | K-01 no global install | R | 621 |
| S2-26 | K-02 OD-1 preserved except first use; wording "framework content" | R | 622 |
| S2-27 | K-03 no IronClaude/IronOrca change | R | 623 |
| S2-28 | K-04 seed-path git-clean offline model | R | 624 |
| S2-29 | K-05 template-push vs rebuild limits | R | 625 |
| S2-30 | K-06 image-layer budget | R | 626 |
| S2-31 | K-07 pin stays 6.9.0 | R | 627 |
| S2-32 | K-08 project root from working directory | R | 628 |
| S2-33 | K-09 profile coverage | R | 629 |
| S2-34 | K-10 contract shapes to keep | R | 630 |
| S2-35 | K-11 single writer of `seed-repo-path` | R | 631 |
| S2-36 | K-12 Claude Code bounds (external) | R | 632 |
| S2-37 | 4 intro: severity scale and "no deferred without scope decision" | R | 636 |
| S2-38 | F-01 no first-use mechanism (Critical) | R | 642 |
| S2-39 | F-02 guard seed-specific | R | 643 |
| S2-40 | F-03 skills without `_bmad` do not work (issue #2677) | R | 644 |
| S2-41 | F-04 no protection against newer/partial tree | R | 645 |
| S2-42 | F-05 failed run partial `_bmad` | R | 646 |
| S2-43 | F-06 no test executes first use | R | 647 |
| S2-44 | F-07 health blind outside seed | R | 648 |
| S2-45 | F-08 no rescan trigger | R | 649 |
| S2-46 | F-09 decision records and text out of date | R | 650 |
| S2-47 | F-10 `global_target_dir` inert | R | 651 |
| S2-48 | F-11 `ancestor_conflict_check` inert | R | 652 |
| S2-49 | G-01 to G-10 (ten Important rows: late skills, user-level ranking, drop-in hooks, hook semantics, later upstream, python3 under UV hook, missing `_bmad`/keys, model compliance, duration, files and no-`.git`) | R | 660-669 |
| S2-50 | G-11 skill set count (Minor) | R | 670 |
| S2-51 | G-12 default module list (Minor) | R | 671 |
| S2-52 | G-13 partial `_bmad` and quick-update | R | 672 |
| S2-53 | G-14 `{output_folder}` and prior-probe facts | R | 673 |
| S2-54 | G-15 HOME writes and network effects | R | 674 |
| S2-55 | G-16 option E write set; manual command | R | 675 |
| S2-56 | G-17 semver hits | R | 676 |
| S2-57 | G-18 image really holds pin | R | 677 |
| S2-58 | G-19 Sysbox residuals | R | 678 |
| S2-59 | G-20 test residuals | R | 679 |
| S2-60 | G-21 environment residuals | R | 680 |
| S2-61 | G-22 resolved (startup never writes settings/skills) | R | 681 |
| S2-62 | G-23 small image/catalogue unknowns | R | 682 |
| S2-63 | G-24 resolved test inventory | R | 683 |
| S2-64 | G-25 E/F tag disagreement resolved | R | 684 |
| S2-65 | G-26 owner wording unavailable | R | 685 |
| S2-66 | G-27 minor document-trail unknowns | R | 686 |
| S2-67 | G-28 documentation hygiene | R | 687 |
| S2-68 | G-29 out-of-scope prior diagnosis | R | 688 |
| S2-69 | G-30 Gate 1 accepted exception (option C wording) | R | 689 |
| S2-70 | 4.3 intro (codebase corrects docs; R05 C5 withdrawn) | R | 692-695 |
| S2-71 | CC-01/SD-01 `global_target_dir` comment | R | 697 |
| S2-72 | SD-02 `ancestor_conflict_check` comment | R | 698 |
| S2-73 | CC-02/CC-03/SD-03 worktree tree is 6.10.0 | R | 699 |
| S2-74 | CC-04 `{output_folder}` phrase | R | 700 |
| S2-75 | CC-05 `Dockerfile.coder:360` line refs | R | 701 |
| S2-76 | CC-06/SD-04 "symlink" text | R | 702 |
| S2-77 | CC-07/08/09/SD-06 README paths and links | R | 703 |
| S2-78 | CC-10/SD-07 `startup.tf:30` | R | 704 |
| S2-79 | CC-11/SD-05 `profiles.yaml:1` path | R | 705 |
| S2-80 | CC-12 "already set up there" | R | 706 |
| S2-81 | CC-13 `Dockerfile.coder:468` | R | 707 |
| S2-82 | CC-14 python3 steps and fallback wording | R | 708 |
| S2-83 | CC-15/SD-08 "T1-T55" | R | 709 |
| S2-84 | CC-16 nine named tests not in the Grep | R | 710 |
| S2-85 | CC-17 "never globally" vs global CLI | R | 711 |
| S2-86 | CC-18/SD-09 memlog:27 | R | 712 |
| S2-87 | CC-19/SD-10 fr-audit line range | R | 713 |
| S2-88 | CC-20/SD-11 profile `agile-full` | R | 714 |
| S2-89 | CC-21/SD-12 PRD addendum Option A/B | R | 715 |
| S2-90 | CC-22 offline setting and update box | R | 716 |
| S2-91 | CC-23/CC-24 test-49 row, option C naming | R | 717 |
| S2-92 | CC-25 test-57:386 comment stale under D1 | R | 718 |
| S2-93 | CC-26 REPORT.md:91 attribution of pin | R | 719 |
| S2-94 | CC-27/CC-30 prior report overtaken | R | 720 |
| S2-95 | CC-28/CC-29 dead link, line count | R | 721 |
| S2-96 | SD-13 "73 skill files" | R | 722 |
| S2-97 | External docs vs code: tutorial "two folders", main-branch install page is v7 | R | 724 |
| S2-98 | 4.4 owner/design question rows (12 rows: Q1, Q2, G-26/D-10, D-1/2/6, D-3, D-4/5, D-7/17, D-8, D-9/11, D-12/13/15, D-14, D-16) | R | 726-740 |
| S2-99 | 4.5 severity roll-up (3 tables) and Important-row listing | R | 745-755 |
| S2-100 | Run-only facts R-1 to R-15 mapped to gaps | R | 757 |
| S2-101 | 5 intro: external context, codebase wins, provenance, small-model summaries | R | 769-771 |
| S2-102 | 5.1 scope note: doc versions, image version not established | R | 773-777 |
| S2-103 | W01-1 personal skills in all projects | R | 779 |
| S2-104 | W01-2 name collision ranking | R | 783 |
| S2-105 | W01-3 new top-level skills dir needs `/reload-skills` | R | 787 |
| S2-106 | W01-4 monorepo/subdirectory skill loading | R | 791 |
| S2-107 | W01-5 commands merged into skills | R | 795 |
| S2-108 | W01-6 skill scripts, `allowed-tools`, injected commands | R | 802 |
| S2-109 | W01-7 docs do not forbid project writes | R | 806 |
| S2-110 | W01-8 hook input fields, `CLAUDE_PROJECT_DIR` | R | 813 |
| S2-111 | W01-9 stdout to context, SessionStart cannot block | R | 817 |
| S2-112 | W01-10 hook timeouts | R | 821 |
| S2-113 | W01-11 `reloadSkills` | R | 825 |
| S2-114 | W01-12 `reloadSkills` version from user issue | R | 829 |
| S2-115 | W01-13 hook edits apply live | R | 833 |
| S2-116 | W01-14 hooks run with full permissions, no Bash prompt (reading) | R | 837 |
| S2-117 | W01-15 hook scopes merge | R | 844 |
| S2-118 | W01-16 managed drop-ins and hooks | R | 848 |
| S2-119 | W01-17 managed keys that disable customisation | R | 852 |
| S2-120 | W01-18 workspace trust hold-back | R | 856 |
| S2-121 | W01-19 listing cost of stub | R | 863 |
| S2-122 | Not answered by official sources (UNVERIFIED list) | R | 868 |
| S2-123 | 5.2 scope note: sources used, tarballs searched, not read | R | 872 |
| S2-124 | W02-1 versions and 6.12.4 latest | R | 876 |
| S2-125 | W02-2 `global_target_dir` in 6.9.0/6.10.0/6.12.4 | R | 880 |
| S2-126 | W02-3 install options and "scope" meaning | R | 884 |
| S2-127 | W02-4 field added for Skills-CLI parity (#2313) | R | 888 |
| S2-128 | W02-5 release notes: no global install | R | 895 |
| S2-129 | W02-6 install-affecting changes after 6.9.0 | R | 899 |
| S2-130 | W02-7 python3 vs uv run across versions | R | 903 |
| S2-131 | W02-8 failure tolerance in 6.12.4 skills | R | 907 |
| S2-132 | W02-9 6.9.0 install guide | R | 914 |
| S2-133 | W02-10 getting-started "two folders" | R | 918 |
| S2-134 | W02-11 main-branch docs are v7 | R | 922 |
| S2-135 | W02-12 v7 preview Skills CLI, offer-and-ask | R | 929 |
| S2-136 | W02-13 issue #2677 | R | 933 |
| S2-137 | W02-14 issue #2624 | R | 937 |
| S2-138 | W02-15 issue #1852 workaround | R | 941 |
| S2-139 | W02-16 plugin channel | R | 945 |
| S2-140 | W02-17 no on-demand bootstrap upstream; `bmad-project-context` | R | 949 |
| S2-141 | W02-18 issue #3016 | R | 953 |
| S2-142 | 5.3 summary table (7 rows) | R | 958-971 |
| S2-143 | 5.3 what external facts change for options (6 bullets) | R | 973-981 |
| S2-144 | 5.3 contradictions and limits | R | 982-984 |

## Anti-Omission Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md`
**Input files checked:** `research/01-bmad-6-9-0-installer-and-skill-runtime.md` (126 findings), `research/02-image-cli-and-catalogue-slug.md` (94), `synthesis/synth-01-problem-current-state.md` (81), `synthesis/synth-02-target-gaps-external.md` (144); total findings enumerated: 445
**Date:** 2026-11-07

### Omissions Found

Part A. Items covered by dedup (not omissions).

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| D-1 | 01-13 per-hit table of `global_target_dir`/HOME grep (comments, doc example, `~` expanders, cache readers) | research 01 s2 | COVERED-BY-DEDUP | Report l.99 and l.105 (conclusion and 43-hit re-check) | n/a |
| D-2 | 01-59 `findAncestorConflict` walk mechanics | research 01 s6 | COVERED-BY-DEDUP | F-11 (l.652, 656) and l.106 | n/a |
| D-3 | 01-77 host tool versions | research 01 s7.5 | COVERED-BY-DEDUP | l.115 "host has 3.11 and 3.13" (exact versions are in O-16) | n/a |
| D-4 | 01-112 test-57 cannot close U11/U12 | research 01 F5-B | COVERED-BY-DEDUP | G-10, G-11 (l.669-670) | n/a |
| D-5 | 01-123 suggested report wording | research 01 F5-E | COVERED-BY-DEDUP | l.133-135 carry the same wording | n/a |
| D-6 | 01-124 F5-F risk row for B, C, D | research 01 F5-F | COVERED-BY-DEDUP | common fact 11 (l.1021), F-04 (l.645), steps 3.3, 4D.3, 7.8 (l.1458, 1517, 1616) | n/a |
| D-7 | 02-55 first-use in seed flips health only at next boot | research 02 s5 | COVERED-BY-DEDUP | l.211 (recomputed once per start; invocation id) and F-07 (l.648) | n/a |
| D-8 | S1-08 scope note of synth-01 | synth-01 s2 | COVERED-BY-DEDUP | no separate text needed; the report has its own scope line (l.6) | n/a |

Part B. Omissions (substance appears nowhere in the report). Numbering O-10 is intentionally unused (cross-references kept stable).

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| O-1 | `--list-tools` observed: 44 tool IDs; claude-code starred as recommended with target `.claude/skills`; codex, cursor, github-copilot starred with `.agents/skills` (01-10, 02-09) | research 01 s1, research 02 s1.4 | OMITTED | | MINOR |
| O-2 | `--list-options` observed keys: `core.user_name`, `core.communication_language`, `bmm.user_skill_level` marked user-scope; defaults `project_name={directory_name}`, `planning_artifacts`, `implementation_artifacts`; `--set bmm.project_knowledge=<path>` relocates `docs/` (01-11) | research 01 s1 | OMITTED | | MINOR |
| O-3 | Remaining `install` option inventory: `--action`, `--custom-source`, `--channel`/`--all-stable`/`--all-next`/`--next`/`--pin`, `-d/--debug`, `--communication-language`, `--document-output-language`, `--list-*` early exit (01-08, 02-09) | research 01 s1 | OMITTED | | MINOR |
| O-4 | Install control-flow minor facts: exit 0 on success and 1 on error, `checkWindowsNodeFromWsl`, `core` always prepended to the module list, `_cleanupSkillDirs` after the IDE step, "install is never silent" (logo, uv check, summary) (01-09, 01-18, 01-22) | research 01 s1, s3.1, s3.2 | OMITTED | | MINOR |
| O-5 | A flagless `--yes` takes the default branch and seeds all five core keys (capitalised OS username, `path.basename(directory)`, English, English, `_bmad-output`); any ONE of `--user-name`, `--communication-language`, `--document-output-language`, `--output-folder` selects the partial-seed branch instead (01-28). The report only says bare `--yes` seeds `output_folder` (l.121, 700) and mandates the `--user-name` form (l.560, 1456); the alternative that avoids the missing-keys gap (U13) is never presented as a plan input | research 01 s3.2a ("Facts the plan needs") | OMITTED | | IMPORTANT |
| O-6 | Network and registry facts: the full list of network touch points (`external-manager` git clone, `custom-module-manager`, `npm install` in cloned modules, `fetchNpmVersion`, `channel-resolver.js:58`, `manifest.js:369`, `version-resolver` has none, none on the fresh `--modules bmm` path) and that `ExternalModuleManager.listAvailable()` reads the bundled registry (01-31, 01-48). Only the conclusion "built-in needs no network" is carried (l.99) | research 01 s3.3, s4 | OMITTED | | MINOR |
| O-7 | Per-hit grep table behind the HOME/`global_target_dir` result (01-13): carried by conclusion only | research 01 s2 | COVERED-BY-DEDUP | see D-1 | MINOR |
| O-8a | IDE-step re-install and ownership semantics: the existing `<canonicalId>` skill dir is removed before copy; cleanup removes only the previously installed set or `removals.txt`; `bmad-os-*` entries are always preserved; after the IDE step the skill source copies under `_bmad/<module>/` are deleted so `_bmad/` keeps only module-level files (01-53, 01-54, 01-55). Matters because FIRST_USE(P) condition 3 (l.292, 1457) globs `.claude/skills/bmad-*` and would also match a user's own `bmad-os-*` skill that the installer itself does not treat as BMAD-owned, and because SC-01/SC-08 depend on what `_bmad/` holds after install | research 01 s5 | OMITTED | | IMPORTANT |
| O-8b | IDE-step minor facts: handlers built only from platform entries with an `installer` block; dotfile/backup-file filter during copy; tools sharing a `target_dir` write once and peers skip (01-49, 01-52, 01-56) | research 01 s5 | OMITTED | | MINOR |
| O-9 | Ancestor-check mechanics: walk starts at the parent and stops before the filesystem root (HOME is walked), checks `<ancestor>/<target_dir>`, ownership by manifest id or `bmad` prefix except `bmad-os-*`, refusal text tells the user to `rm -rf` (01-59) | research 01 s6 | COVERED-BY-DEDUP | see D-2 | MINOR |
| O-11 | `resolve_config.py` merges four layers (`config.toml` required; `config.user.toml`, `custom/config.toml`, `custom/config.user.toml` optional) and is stdlib-only (01-62) | research 01 s7.1 | OMITTED | | MINOR |
| O-12 | `resolve_customization.py` requires `customize.toml` in the skill dir (exit 1 if missing); the skill-dir-first lookup exists because cwd-first is unsafe when an ancestor has a stray `_bmad/` from another project (01-63) | research 01 s7.2 | OMITTED | | MINOR |
| O-13 | Observed on this host: `/home/coder` is not a git repo and `~/_bmad` does not exist, so for a skill under `~/.claude/skills` the skill-dir lookup returns None and falls back to the cwd walk (valid only while those HOME conditions hold) (01-65) | research 01 s7.2 | OMITTED | | MINOR |
| O-14 | `memlog.py init` refuses to overwrite an existing workspace (`memlog.py:147`) (01-66) | research 01 s7.3 | OMITTED | | MINOR |
| O-15 | The 46 `SKILL.md` split: 13 in `core-skills`, 33 in `bmm-skills` (01-67) | research 01 s7.4 | OMITTED | | MINOR |
| O-16 | Host and session facts: Node v24.22.2 satisfies the engine floor; uv 0.11.8, cpython 3.13.5 (`/usr/bin/python3`) and 3.11.15 observed; a bare `python3 --version` was actually refused by the user's UV-only hook in the research session (the report marks the hook effect UNVERIFIED, l.276) (01-04, 01-77, 01-78) | research 01 s0, s7.5 | OMITTED | | MINOR |
| O-17 | Tracked 6.10.0 tree detail: `lastUpdated`, `ides: claude-code, openhands`, manifest commit history (four commits), the tracked `_bmad` file list, `custom/bmad-retrospective.toml` is project-authored (not installer output), `_bmad-output` holds project documents with only two installer-matching dirs (01-80, 01-82, 01-83, 01-85, 01-86) | research 01 s8 | OMITTED | | MINOR |
| O-18 | `tools/installer/README.md` was searched (no hits) but not read in full (01-94) | research 01 Stale Documentation | OMITTED | | MINOR |
| O-19 | Prior-review and CI provenance details: memlog line 81 decision text; probe sizes (`_bmad/` 160K, skills 2.4M); the offline run with a dead proxy exited rc=0 as a separate run from the 4 s run; quick-update rewrite content (timestamps, reordered keys, added `project_name` and language keys); how test-57 gets `--network=none` (driver column parsing) and refuses to pass if the network is reachable, with the same precondition on three other rows; the `cold bmad` timer is an upper bound (includes `chown -R`); `cold ironclaude` is 4392-4513 ms and the memlog "about 4s" is nearer that figure; CI discards installer output (`>/dev/null`), so no skill-count line or file list exists in CI logs; the PASS cannot tell "no `npm view` attempted" from "failed quietly" (01-98, 01-100, 01-102, 01-103, 01-106, 01-107, 01-108, 01-114, 01-116, 01-122) | research 01 F5-A to F5-E | OMITTED | | MINOR |
| O-20 | Image and slug small facts: `chown -R 1000:1000 "$NVM_DIR"` and the `node_bin`/`cli` derivation; the only other `bmad` mention in `Dockerfile.coder` is line 277; `install.sh` exits from `set -e` (`mkdir`, `git rev-parse --git-path`); `module.tf` header says `agent_id` is kept so a future launch surface is a clean diff; orca install runs with a 300 s bound (02-04, 02-05, 02-21, 02-36, 02-62) | research 02 s1, s2, s4.3, s6.1 | OMITTED | | MINOR |
| O-21 | Profile wiring: the form's profile list is hand-copied from `profiles.yaml` (`parameters.tf:92-93`); `coder_parameter "profile"` default `orca`, `mutable`; `coder_env "aidev_profile"` exports `AIDEV_PROFILE`; `startup.sh:715` `aidev_cat_root` (02-39, 02-42, 02-43) | research 02 s4.4, s4.5 | OMITTED | | MINOR |
| O-22 | README contract rows: `scope` enum, `install_disposition` values, `test-5` `ALLOWED` array, README anchor for zero-`coder_app` pattern (02-47) | research 02 s4.6 | OMITTED | | MINOR |
| O-23 | Catalogue statements stretched by B1, D1, D3: manifest `display.summary` says "opt-in"; `install.sh` header states its purpose as verify-CLI plus seed install; README VERIFY-ONLY pattern (02-59, 02-74) | research 02 s6.1, s6.3 | OMITTED | | MINOR |
| O-24 | Option C rebuild cost: the BMad layer sits at lines 136-145 of a 595-line file, so later layers (including SHA-pinned release-binary downloads from `Dockerfile.coder:147` via the host-network legacy builder, `main.tf:122-145`) rebuild; a stable wrapper plus late-COPY script shrinks it but is still class (i) (02-65) | research 02 s6.2 | OMITTED | | MINOR |
| O-25 | Layer-gate detail: gate comment "76 layers started, 78 hit Sysbox's relative overlay-path bug", so 70 is a chosen margin and not a Docker limit, and the Dockerfile comment says to remove the ceiling after upstream fixes; independent count 61 instruction lines = 1 FROM + 60 (31 RUN, 29 COPY, no ADD); older `ARCHITECTURE-SPINE.md:93` says "main is at 70"; `docs/development-guide.md:66` repeats the fold policy; comments `:229`/`:468` left unedited for the later plan (02-85, 02-87, 02-89) | research 02 addendum A1, A3, A4 | OMITTED | | MINOR |

### Self-Audit

**What I actively checked**
- Read in full: both research files (01: 531 lines; 02: 455 lines, including both fix-cycle addenda) and both synthesis files (synth-01: 521 lines; synth-02: 466 lines). Final report: read line by line l.1-570 (sections 1, 2, start of 3), l.986-1763 (sections 6, 7, 8, 9 and the register, start of 10). NOT read line by line: l.571-985 (rest of sections 3, 4, 5) and l.1764-end (section 10 evidence trail). For l.571-985 I relied on header positions, row-by-row ID greps (every SC, K, F, G, CC/SD row and every W01 and W02 finding was found with its ID) and phrase greps for the synthesis paragraphs (for example "Not answered by official sources", "What the external facts change", "Limits: WebFetch", "External documentation checked against the code", "Run-only fact"), so a silent text change inside a row of those sections would not have been caught by me.
- Method: enumerated every table row, bullet and addendum item of the four inputs (445 findings, list above), then for each searched the report for the substance. Where the report was a verbatim copy of a synthesis section I verified it by reading both and by row counts (16 SC, 12 K, 11 F, 30 G, 26 CC/SD, 19 W01, 18 W02 all present with the same IDs). For research items that the synthesis did not carry I used targeted Grep over the report for distinctive tokens (examples that returned no hit: `bmad-os`, `canonicalId`, `removals.txt`, `2.4M`, `160K`, `dead proxy`, `4392`, `4513`, `overlay-path`, `76 layers`, `AIDEV_PROFILE` as an exported env, `aidev_cat_root`, `derived by hand`, `checkWindowsNodeFromWsl`, `getDefaultModules`, `capitalised`, `any one of`, `44 tool`, `tools/installer/README`), then confirmed by reading the relevant report section (6, 7, 8, 9) that the substance was not stated in other words.
- Findings in the report that are not in my slice (for example the Phase 4 gate procedure, the document register, SC/K detail text) were not counted as coverage of anything unless they restated a finding of my slice.
- Line numbers: report lines for sections 1-2 and 6-9 come from direct reads; the lines I give for sections 3-5 rows come from Grep positions and the structure read (headers at l.551, 592, 617, 638, 654, 691, 726, 745, 767), so single-row lines in those sections can be off by one or two. Nothing was verified by running code; this is a text-to-text comparison.
- Date: the system date was 2026-11-07; the session context line said 2026-11-08. I used 2026-11-07, matching the task folder stamp.

**Why I believe the omission count is correct (and the stance applied)**
- I assumed at least five distinct findings were dropped. Result: 23 omission items (2 IMPORTANT, 21 MINOR), 0 CRITICAL, plus 2 items (O-7, O-9) that are dedup-classified and listed for completeness. The reason there are no CRITICAL drops is that every foundational conclusion of files 01 and 02 (per-project writes only, no `global_target_dir` consumer, dead ancestor check, `resolve_config.py` exit 1, no bootstrap, seed-only slug, health blind outside seed, rebuild classes, 68 of 70 layers, version skew and partial tree, wrapper has no logic) is stated in the report with its evidence line, and sections 2 to 5 are near-verbatim copies of the synthesis.
- The IMPORTANT items are the two places where a plan-relevant fact from research was lost: O-5 (the flag-set choice that decides which core keys exist after the install) and O-8a (installer ownership and re-install rules that bear on the FIRST_USE(P) glob and on what `_bmad/` contains). The MINOR items are details whose conclusions are preserved elsewhere, or provenance and inventory facts.
- Doubtful cases were flagged, not dismissed: O-13, O-16, O-19, O-24 and O-25 are borderline and could be dismissed as detail.
- Dedup claims (8) were each checked against the named report item; none is a silent drop.
- Limits: I judged "represented" by meaning from my own reading and some grep spot checks, not by an independent second reader; the synthesis Self-Audit blocks were treated as non-findings by design.

### Summary

- Findings enumerated: 445 (research 01: 126; research 02: 94; synth-01: 81; synth-02: 144)
- Represented: 406 (of which 22 are "R/O": the finding is represented and a distinct remainder is listed as an omission item)
- Covered-by-dedup: 8
- Omitted (whole findings): 31 enumeration rows (23 in research 01, 8 in research 02), consolidated into 23 omission items; the 22 "R/O" rows add distinct remainders that sit inside the same items. O-7 and O-9 in Part B are dedup entries (D-1, D-2), not omissions.
- Omission items by severity: CRITICAL 0, IMPORTANT 2 (O-5, O-8a), MINOR 21 (O-1 to O-4, O-6, O-8b, O-11 to O-25)
- Check: 406 represented + 8 dedup + 31 omitted = 445 enumerated.

Verdict: FAIL (2 blocking omissions: O-5 and O-8a, both IMPORTANT). No CRITICAL omission; the 21 MINOR items are notes. Recommended repair, for the appropriate agent and not done here: add one sentence to report 2.1 (or common fact 3) on the flagless-`--yes` seeding and the four-flag branch rule (O-5), and one sentence on re-install skill-dir replacement, `bmad-os-*` preservation and deletion of `_bmad/<module>` skill copies, with a note on the FIRST_USE(P) glob (O-8a).
