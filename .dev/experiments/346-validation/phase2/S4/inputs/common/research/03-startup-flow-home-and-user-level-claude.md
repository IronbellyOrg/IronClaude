# Research: startup flow, HOME persistence and user-level Claude Code surfaces
**Investigation type:** Architecture Analyst
**Scope:** templates/VSCode-AIDev02/image/scripts/startup.sh, templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh, Terraform files under templates/VSCode-AIDev02/ (home volume / persistence), read-only: /home/coder/.claude/ (structure only), /opt/uv/tools/superclaude/ (install_user_setup.py, user_settings_defaults.json)
**Status:** Complete
**Date:** 2026-11-07
---

## 1. Terraform: what persists across stop/start (question b)

Files read: `templates/VSCode-AIDev02/main.tf`, `templates/VSCode-AIDev02/startup.tf`.

| Fact | Evidence | Tag |
|------|----------|-----|
| `docker_volume.home` named `coder-${workspace.id}-home`, per workspace | main.tf:174-176 | [CODE-VERIFIED] |
| `docker_volume.workspace` named `coder-${workspace.id}-workspace` | main.tf:178-180 | [CODE-VERIFIED] |
| `docker_volume.docker_data` named `coder-<id>-docker-data-<runtime>` | main.tf:182-184 | [CODE-VERIFIED] |
| Home volume mounted at container path `/home/coder` | main.tf:594-597 | [CODE-VERIFIED] |
| Workspace volume mounted at `/config/workspace` | main.tf:599-602 | [CODE-VERIFIED] |
| docker-data mounted at `/var/lib/docker` only on the sysbox-runc arm | main.tf:604-614 | [CODE-VERIFIED] |
| `/etc/machine-id` is uploaded per workspace (outside the volumes) so it is stable across `coder update` | main.tf:583-592 | [CODE-VERIFIED] |
| Comment in main.tf states a release in the image's `/etc/aidev02/aienv.d` "a restart resets to the image copy" while the pushed release is "kept in the home volume" | main.tf:216-219 | [CODE-VERIFIED] as a comment; implies everything outside the volumes (image layers, /etc, /opt) is reset from the image on restart |

Interpretation (derived from the mounts above, not separately observed at runtime): `/home/coder` (including `~/.claude/`, `~/.aidev/`, `~/workspaces/`) lives on the per-workspace named volume and survives workspace stop/start and template updates. Anything outside `/home/coder`, `/config/workspace` and (sysbox) `/var/lib/docker` comes from the image on every container recreate. Whether a volume is ever deleted on workspace delete is NOT shown in the Terraform read; marked [UNVERIFIED] (Coder destroys the Terraform-managed volume on workspace deletion by normal provider behaviour, not checked here).

Boot wiring (startup.tf):
- `coder_script.startup` runs `aidev-startup` on every start: `run_on_start = true`, `start_blocks_login = false` (startup.tf:42-46). The script sets `HOME=/home/coder`, runs `/usr/local/lib/aidev/reapply-central-defaults || true`, then `exec /usr/local/bin/aidev-startup` (startup.tf:54-63). [CODE-VERIFIED]
- A second, login-blocking `coder_script.central_defaults_restore` runs `/usr/local/lib/aidev/reapply-central-defaults` (main.tf:220-227, `start_blocks_login = true`, timeout 30). [CODE-VERIFIED]
- A third, `coder_script.code_server`, launches code-server (main.tf:233-...). Not relevant to `.claude`.
- startup.tf header comment says the orchestrator is "baked onto PATH as /usr/local/bin/aidev-startup (Dockerfile.coder)" (startup.tf:27-29). Not yet checked against Dockerfile.coder; see Gaps.

Key Takeaways
- HOME is a per-workspace named volume: user-level files under `~/.claude/` persist across stop/start.
- The boot entry is `coder_script.startup` and re-runs on every start, so any bootstrap added to startup.sh runs every boot and must be idempotent.
- No Terraform file in this template writes anything into `~/.claude`.

## 2. startup.sh boot order and idempotency (question a)

File: `templates/VSCode-AIDev02/image/scripts/startup.sh` (sections gated by `# === section:N name ===`, header lines 3-13; `set -euo pipefail` at line 14). Section ids 4, 5, 11 are retired (lines 7-9). [CODE-VERIFIED]

| Order | Section (line) | What it does | Idempotent? | Touches `~/.claude`? |
|-------|----------------|--------------|-------------|----------------------|
| 1 | §1 init (16) | Validates `~/.aidev/status/` ancestors (aidev_run_paths, 19-31, exit 73 on symlink); clears seed and capability status files (36-63); writes `startup-invocation` record (89-92); `mkdir -p ~/.aidev/{status,installed,run,logs,cache}` (105); creates `~/workspaces` (108-113); one-shot `specstory-cleanup --once` (119) | Yes (rm then rewrite; mkdir -p) | No |
| 2 | §2 runtime-bootstrap (121) | dind-sidecar vs sysbox dockerd; waits up to `AIDEV_DOCKER_WAIT` (default 60 s) for `docker info`; `exit 1` if unreachable (153-156) | Re-verifies only | No |
| 3 | §3 git-identity (160) | `git config --global user.name/email` (166-167); chown and write-probe of `/config/workspace` (169-187; `exit 1` if not writable) | Yes | No |
| 4 | §6 workspace-defaults (191) | `seed_if_absent` copy-if-absent from `/etc/skel` and `/usr/local/lib/aidev` (function 201-274) | Yes, never overwrites an existing regular file (241-248) | YES: `seed_if_absent "${HOME}/.claude/CLAUDE.md" /etc/skel/.claude/CLAUDE.md` (line 275) |
| 5 | §7 gh-auth (303) | SSH host keys, credential presence flags | Yes | Not in lines read |
| 6 | §8 seed-repo-clone (389) | Optional clone of `REPO_URL` into the seed destination; sole writer of `~/.aidev/status/seed-repo-path` (673-681) | Yes (cloned / preserved-valid / other) | No |
| 7 | §9 catalogue-installs (692) | Iterates `/catalogue/*` in `LC_ALL=C` sort order (1275), runs each slug's `install.sh` for scope workspace or hybrid | install.sh owns idempotency (692-712) | Via ironclaude slug (see section 3) |
| 8 | post-§9 (1279-1285) | `aidev_retire_legacy_mcp`; re-sync of the IronClaude codegraph block inside `~/.claude/CLAUDE.md` from `/etc/skel/.claude/CLAUDE.md` via `aidev_claude_md_block_sync` (1285) | Writes nothing when block already equal (comment 1282-1284) | YES: `~/.claude/CLAUDE.md` only |
| 9 | §10 affordance-render (1348), tool-floor-verify (1451), §12 done (1665) | Not read in detail | not read | not read |

Order-of-slugs fact: slugs are visited in sorted order; `bmad` < `claude-code` < `ironclaude` < `mcp-bundle-core` alphabetically, so `bmad` installs BEFORE `ironclaude` in the same boot. [CODE-VERIFIED from sort at line 1275 and catalogue directory listing; the directory names come from the Glob result]. The slug loop is non-blocking: no per-slug failure exits the orchestrator (710-712).

Seed repo and bmad (relevant to option B/D/E context):
- bmad slug `install.sh` is a PER-REPO install into the seed repo path read from `~/.aidev/status/seed-repo-path` (bmad/install.sh:10, 21). If no seed repo is recorded it prints "no seed repo recorded; nothing to configure" and still writes the marker (bmad/install.sh:22-23, 57-60). [CODE-VERIFIED]
- It skips when `_bmad/` exists or tracked `.claude/skills/bmad-*` exist (bmad/install.sh:24-25).
- It adds `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/` to the repo's `info/exclude` (bmad/install.sh:28-34) and runs `NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output --user-name ...` (line 42), then fails if `git status` changed (48-53). [CODE-VERIFIED]
- bmad's marker is exempt from profile-deselection removal (startup.sh:1116-1118, "BMad is an explicit owner-decision exception"). [CODE-VERIFIED]
- bmad is invoked differently from other slugs: `( source "${HOME}/.aienv" && bash <install.sh> ) > log` with NO 30 s watchdog, whereas other slugs go through `aidev_cat_install` with a bound of 30 s, or 75 s for ironclaude and mcp-bundle-core (startup.sh:1170-1182). [CODE-VERIFIED]

Key Takeaways
- Boot order is fixed and re-runs entirely on every start; only §6 (copy-if-absent) and the post-§9 block sync touch `~/.claude` apart from the ironclaude slug.
- Nothing in startup.sh creates `~/.claude/skills/` or writes `~/.claude/settings.json` directly (grep for `.claude|settings.json|skills` over startup.sh hit only lines 275, 1172, 1282, 1285 plus the retire-legacy-mcp function at 979 using `~/.claude.json`).
- bmad installs per seed repo only; it never installs at user level.

## 3. ironclaude catalogue install.sh (who runs `superclaude install` on boot)

File: `templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh` (158 lines). [CODE-VERIFIED by reading the whole file]

| Fact | Evidence |
|------|----------|
| Runs `superclaude install` into `~/.claude`, once per provenance `git_sha` read from `/etc/aidev02/ironclaude-provenance` | lines 2-3, 11, 23 |
| Short-circuit (no-op) when marker exists, CLI is on PATH and "configured" (sha file equals image sha, `~/.claude/commands/sc/help.md` exists, settings.json has a hook command containing `/.claude/hooks/`) | lines 26-35 |
| Requires `~/.claude/CLAUDE.md` to exist (seeded by startup §6) or exits 2 | line 42 |
| Uses `--force` whenever the recorded sha differs from the image sha (new image provenance, or first install) | lines 91-97 |
| Refuses (exit 1) when `~/.claude/settings.json` is malformed or has non-object `hooks`, before superclaude writes a .bak | lines 99-103 |
| Records every pre-existing hook command string, and FAILS the slug if any is missing after install: "superclaude install dropped pre-existing hook entries" | lines 110-111, 133-136 |
| Saves and restores `CLAUDE.md` byte-for-byte around the install, and restores a symlinked `settings.json` | lines 44-86, 113-127 |
| Install bound: `timeout 60 superclaude install` | line 122; startup.sh:1180 gives ironclaude and mcp-bundle-core a 75 s outer bound |
| Writes `~/.aidev/installed/ironclaude.configured` (the sha) and `~/.aidev/installed/ironclaude` marker only after verification | lines 143-150 |

Consequence for boot behaviour: on every boot after the first, with an unchanged image sha, the ironclaude install.sh does NOTHING to `~/.claude` (line 32-35). Only when the image carries a new IronClaude `git_sha` does it re-run `superclaude install --force` (lines 95-97, 122). So a user-added skill or hook is exposed to `superclaude install` only on first boot and on each template/image update that bumps the provenance sha.

Whether `--force` overwrites skills or settings is determined in section 5 (superclaude code).

Key Takeaways
- The ironclaude slug is the only boot-time writer of IronClaude hooks, skills and settings defaults into `~/.claude`.
- Its own guard (lines 110-136) explicitly treats loss of any pre-existing hook command as a failure: a user hook added to settings.json is protected by an assertion, but a failure here fails the slug only (non-blocking).

## 4. Current content of `~/.claude/` in this workspace and who writes it (question c)

Method: read-only `ls` and `jq` key-name queries (no values printed) against `/home/coder/.claude/`. This is a long-lived, actively used workspace (22 files named `settings.json.bak*`, dated 2026-10-24 to 2026-11-07), so it is NOT a fresh-boot sample. Observed at 2026-11-07.

`~/.claude/skills/` by name (42 entries by `ls -1A`; the directory itself is a normal 0755 directory per `ls -ld`; whether each entry is a real directory or a symlink was NOT checked, [UNVERIFIED]):
`ccsession-tag, computer-use, confidence-check, operational-guide, orca-cli, orchestration, prd, readme, roadmap, task, task-builder, tdd, tech-reference, tech-research`, plus 28 `sc-*-protocol`/`sc-*` directories: `sc-adversarial-protocol, sc-auggie-review-protocol, sc-bare-review, sc-brainstorm-protocol, sc-cleanup-audit-protocol, sc-cli-eval-protocol, sc-cli-portify-protocol, sc-crash-recovery, sc-graph-protocol, sc-impact-protocol, sc-implement-protocol, sc-init-lite-protocol, sc-issue-protocol, sc-pm-protocol, sc-post-release-protocol, sc-pr-submit-protocol, sc-recommend, sc-reflect-protocol, sc-release-split-protocol, sc-review-translation-protocol, sc-roadmap-protocol, sc-swarm-wizard-protocol, sc-task-protocol, sc-tasklist-protocol, sc-troubleshoot-protocol, sc-validate-roadmap-protocol, sc-validate-tests-protocol, sc-workflow-protocol`.
- NO `bmad-*` skill directory exists at user level. [CODE-VERIFIED by listing]
- `comm -3` of the packaged skill set (`/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/skills/`, 39 entries excluding `__init__.py`) against the live directory shows exactly three extras: `computer-use`, `orca-cli`, `orchestration`. Those three are the names in `_ORCA_SKILLS` (install_user_setup.py:34), installed by the Orca CLI, not by superclaude's skill copier. So there is NO user-added skill in this workspace today; the whole directory is explained by superclaude plus Orca. [CODE-VERIFIED]

`~/.claude/settings.json`: regular file (not a symlink), 54505 bytes, mode 0644, owner coder.
- Top-level keys: `agentPushNotifEnabled, alwaysThinkingEnabled, claudeMdExcludes, effortLevel, enabledPlugins, env, extraKnownMarketplaces, hooks, model, modelSettings, outputStyle, skipDangerousModePermissionPrompt, statusLine, teammateMode, theme, verbose`.
- `env` keys: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS, CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION, PONYTAIL_DEFAULT_MODE` (values not read).
- `hooks` events present: SessionStart (5 registrations), UserPromptSubmit (3), Stop (1), StopFailure (1), SubagentStart (3), SubagentStop (2), TeammateIdle (1), PreToolUse (3), PostToolUse (3), PostToolUseFailure (1), PermissionRequest (1), PostCompact (1), SessionEnd (2), Elicitation (1), ElicitationResult (1).
- Hook command script basenames present: `auggie-flag-clear.sh, block-bare-python.sh, codegraph-session-start.sh, freshness-post-read.sh, freshness-pre-edit.sh, freshness-session-start.sh, freshness-subagent-start.sh, freshness-subagent-stop.sh, freshness-user-prompt.sh, session-init.sh, session-name.sh, session-start.sh`, plus commands starting with `if` and `node` (not resolved further).
- `~/.claude/hooks/` holds 14 files (`ls`): the freshness set, `auggie-flag-clear.sh`, `block-bare-python.sh`, `codegraph-session-start.sh`, `pragmatic-subagent.js`, `reject-workspace-writes.sh`, `sc-recommend-phase0.sh`, `session-init.sh`. These match `_FRESHNESS_SCRIPTS` and `_LEGACY_SCRIPTS` in install_hooks.py:42-87. [CODE-VERIFIED]
- `/etc/claude-code/managed-settings.d/` (image-level, outside HOME) holds only `10-retention.json`; its content is `{"cleanupPeriodDays": 90}` (image/etc/claude-code/managed-settings.d/10-retention.json:1-3). [CODE-VERIFIED]

`~/.aidev/` state observed: `~/.aidev/installed/` contains `bmad, claude-code, ironclaude, ironclaude.configured, mcp-bundle-core, orca`. `~/.aidev/status/seed-repo-path` DOES NOT EXIST in this workspace (cat failed), so the bmad slug had nothing to configure here (matches bmad/install.sh:22-23, which still writes the marker). [CODE-VERIFIED by observation]

Writers of `~/.claude/settings.json` and `~/.claude/skills/` (every writer found; Grep for `settings.json` over `templates/VSCode-AIDev02/image` matched 5 files: spec2-health.sh, ironclaude/install.sh, mcp-bundle-core/manifest.yaml, specstory-cleanup, codegraph-sweep):

| Writer | settings.json | skills/ | Evidence |
|--------|---------------|---------|----------|
| `superclaude install` (run by the ironclaude slug at boot, or by the user by hand) | YES: additive hook merge, fill-only defaults, `claudeMdExcludes` append | YES: copies packaged skills by name | main.py:204 (`install_all_skills`), 217 (`install_hooks`), 236 (`install_user_setup`); install_hooks.py:269-467; install_user_setup.py:155-195 |
| Orca CLI (`orca-ide skills install`), launched by superclaude (`install_orca_skills`) and by the orca slug | not by Orca code in this repo | YES: `orca-cli`, `orchestration` (and `computer-use` via superclaude) | install_user_setup.py:230-263; catalogue/orca/install.sh:26-41 |
| orca deselection retirement script | no | removes `orca-cli`/`orchestration` only if the entry is a symlink to exactly `../../.agents/skills/<s>` | modules.tf:82-109 (lines 101-106) |
| `specstory-cleanup --once` (TEMPORARY, startup §1 line 119) | YES, removal only: drops the SpecStory hook command, empty groups and empty events | no | image/bin/specstory-cleanup:28-50, 60-70 |
| startup.sh §6 and post-§9 sync | no | no (only `~/.claude/CLAUDE.md`) | startup.sh:275, 1285 |
| Claude Code itself | YES (the `/config` menu writes `~/.claude/settings.json`) | no | docs https://code.claude.com/docs/en/settings, "Use the /config menu"; [UNVERIFIED in code, doc-sourced] |
| the user | YES, by hand | YES, by hand | no code; inferred |
| Orca as a `settings.json` writer | named only in a comment (`# ponytail: no lock against the parallel Orca settings.json writer (AD-3)`, ironclaude/install.sh:139) | n/a | [UNVERIFIED]: `image/orca/runtime.mjs` in this repo only touches Orca's own `settings.getAgentLaunch` (runtime.mjs:399); no Orca source for a `~/.claude/settings.json` write was found here |

Key Takeaways
- At user level, skills and settings are written ONLY by superclaude (via the ironclaude slug), Orca (three skill names) and, for removal, specstory-cleanup; this repo's own code never creates a user-level skill or hook.
- The live `~/.claude/skills/` has no `bmad-*` entry and no user-added entry; any new user-level BMAD skill would be the first non-packaged, non-Orca name.
- The image already carries a second, HOME-independent Claude Code settings surface: `/etc/claude-code/managed-settings.d/` (one file today, retention only).

## 5. Merge versus overwrite semantics of `superclaude install` (question d)

Files read: `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/install_user_setup.py` (445 lines), `user_settings_defaults.json` (71 lines), plus, because hooks and skills are not handled in the two assigned files, `install_hooks.py` (lines 1-125, 124-262, 265-480), `install_skills.py` (1-152), `install_skill.py` (1-151) and `main.py` (40-270, install flow). The `_src/superclaude/cli/` copy of the same two files was not compared (second Glob hit); [UNVERIFIED] that it is identical, but the first path is the importable package.

Install flow order (main.py): core files (178) -> commands (188) -> agents (196) -> skills (204) -> `wire_ccsession` (209) -> hooks (217) -> templates (227) -> user setup (236) -> codegraph (246) -> retire stale MCP (263). `--force` is passed to all but codegraph. [CODE-VERIFIED]

| Surface | Behaviour | Overwrite risk for a USER addition | Evidence |
|---------|-----------|------------------------------------|----------|
| settings.json `hooks` | ADDITIVE merge. Framework registrations are identified by exact command string (or an equivalent ccsession script); different hooks sharing a matcher are unrelated and kept. Without `--force` an owned registration is skipped; with `--force` it is replaced in place and any user-only hook that shared that registration is kept as a remainder | LOW: a user hook with a different command string is never removed, with or without `--force`. Replaced only if the user's command string is byte-identical to a managed one | install_hooks.py:14-15, 379-447 |
| settings.json hook safety | Backup `settings.json.bak.<stamp>` is written before every merge; a malformed file, non-object root or non-object/list `hooks` is REFUSED (no write); write is atomic (`os.replace`) | none; but a broken user edit would make the whole superclaude install report failure, and the ironclaude slug refuses first (ironclaude/install.sh:99-103) | install_hooks.py:302-346, 449-459, 483-500 |
| settings.json defaults | FILL-ONLY: a top-level key is added only if absent; `env`, `enabledPlugins`, `extraKnownMarketplaces`, `modelSettings` are filled entry by entry; a user value of another shape is kept; one rename carry-over (`ponytail@ironclaude` -> `ponytail@ponytail`) | NONE: user-set values never overwritten. `hooks` is not a defaults key; keys managed are only those in `user_settings_defaults.json` (outputStyle, model, effortLevel, alwaysThinkingEnabled, verbose, teammateMode, agentPushNotifEnabled, skipDangerousModePermissionPrompt, env, modelSettings, enabledPlugins, extraKnownMarketplaces; `ironclaudeMarketplace` is read, never copied) | install_user_setup.py:41-47, 155-195; defaults json:1-71 |
| settings.json `claudeMdExcludes` | APPENDS the three rules globs if missing; refuses a non-list | none | install_user_setup.py:118-132 |
| `~/.claude/hooks/*.sh` scripts | Copied only for the FIXED name list (`_FRESHNESS_SCRIPTS` 42-86, `_LEGACY_SCRIPTS` 87); existing file kept unless `--force`, then overwritten | NONE for a differently named script; overwritten for the 14 managed names | install_hooks.py:222-261 |
| `~/.claude/skills/<name>/` | Per packaged name only. Existing dir kept unless `--force`; with `--force` that one dir is `rmtree`d and recopied. Additionally, an `sc-<x>` skill with a matching `commands/<x>.md` that does not self-activate is `rmtree`d unconditionally as "stale". No code iterates the skills dir to prune unknown names | NONE for a name outside the packaged set (39 names listed in section 4) and outside the Orca three. A user skill named `bmad-*` cannot collide: a Grep for `bmad` over superclaude `skills/`, `hooks/`, `install*.py` and the defaults JSON hit only `sc-cleanup-audit-protocol` files, none of which install a bmad skill name | install_skills.py:88-110; install_skill.py:46-52; rmtree grep over `cli/install*.py` (skills only at install_skills.py:97 and install_skill.py:48) |
| Orca skills | Skipped if all three `SKILL.md` exist; else `orca skills install --agent claude-code` bounded by `_ORCA_TIMEOUT` 25 s | none | install_user_setup.py:230-263 |
| Plugins | `claude plugin ...` commands for the defaults the user has not disabled; the pinned IronClaude catalog is rewritten at `~/.claude/ironclaude-marketplace/` on every run | none for user settings; `enabledPlugins` entries set to false by the user are respected | install_user_setup.py:298-431 |

When does `superclaude install` run at boot? Only from the ironclaude slug (section 3): first boot, and any boot where the image's IronClaude `git_sha` differs from `~/.aidev/installed/ironclaude.configured`. In that case it runs with `--force` (ironclaude/install.sh:91-97). The user can also run it by hand at any time. [CODE-VERIFIED]

Does re-running this repo's boot code overwrite a user-added hook or skill? No. startup.sh itself never writes `~/.claude/settings.json` or `~/.claude/skills/` (section 2 grep). The only boot-time code that rewrites settings.json is superclaude (additive, above) and specstory-cleanup (removes only the exact SpecStory hook command; marker file `~/.aidev/specstory-cleanup.done` makes it a no-op afterwards, specstory-cleanup:29, 40). A user-added hook is also guarded by an explicit assertion in ironclaude/install.sh:104-136 (slug FAILS if any pre-existing hook command disappears).

Edge cases and risks found
- A settings.json that is a symlink is replaced by superclaude (atomic replace); ironclaude/install.sh:68-86 and 105-109, 127-132 restore the link. A user hook still survives. [CODE-VERIFIED]
- Lost-update race: Orca/Claude Code may write settings.json concurrently; no lock (ironclaude/install.sh:139 comment). A hook added by a boot script could be lost to a concurrent writer; self-heals next boot only if the adder re-adds it.
- Backup churn: every `superclaude install` run that changes settings.json leaves a new `settings.json.bak.<stamp>`; this workspace has 21 stamped backups (ls). Not pruned by superclaude code read here.

Key Takeaways
- superclaude install is merge-only for hooks and defaults, and per-name for skills; a user skill under a new name and a user hook under a new command string both survive `superclaude install --force`.
- The only overwrite hazards are exact name or exact command-string collisions with the managed set; a `bmad-*` skill name does not collide with any packaged or Orca skill.
- Boot-time `--force` runs happen at most once per IronClaude sha bump, but a user can re-run any time; neither path removes unrelated entries.

## 6. Where in THIS repo a user-level skill or hook could be written (question e)

All paths relative to `templates/VSCode-AIDev02/` unless absolute. Nothing below was implemented; these are placement facts from source.

| Mechanism | Where / function | Fits | Constraints found in source |
|-----------|------------------|------|-----------------------------|
| M1 startup §6 `seed_if_absent` | `image/scripts/startup.sh`, function `seed_if_absent` (201-274), call list 275-293 (e.g. line 275 for `~/.claude/CLAUDE.md`); a new call such as `seed_if_absent "${HOME}/.claude/skills/<name>/SKILL.md" <image source file>` would match the pattern | user-level SKILL.md (a file); the helper creates missing parent directories with mode 0755 (lines 232-239) and refuses symlinked or non-regular destinations (222-248) | Copy-if-absent only: an existing file is preserved (245-248), so a later image update of the skill text never reaches an existing workspace. One file per call. The source file must be COPYed into the image: existing pattern is one shared COPY layer into `/usr/local/lib/aidev/` (Dockerfile.coder:547-548); Dockerfile.coder:468 says the Sysbox image-layer budget (70) "has no headroom" so a new file should ride an existing COPY layer. The source must also be listed in `main.tf` `image_input_files` (main.tf:80-101) or the image tag will not change (comment main.tf:75-79: test-67 fails CI when a COPY source is missing there). |
| M2 bmad slug installer | `image/catalogue/bmad/install.sh` (62 lines): runs every boot via startup §9 (sorted before ironclaude), could gain a user-level step before the marker write at line 57-60 | user-level skill or settings change tied to BMAD | Catalogue files are hashed into the image tag (`catalogue_sha256`, main.tf:74), so a change rebuilds the image. bmad runs WITHOUT the 30 s watchdog that other slugs get (startup.sh:1174-1176). The marker is exempt from profile-deselect removal (startup.sh:1116-1118). The script has no early success exit: the three seed-repo branches (install.sh:22-55) all fall through to the marker write and `exit 0` (57-61), so a user-level step added after line 55 would run whether or not a seed repo exists; failures exit 1 (lines 44, 46, 51) or 2 (line 18). |
| M3 settings.json hook merge | no existing helper in this repo adds a hook; the only repo code that edits hooks is `image/bin/specstory-cleanup` (removal, lines 42-70) and the ironclaude preservation check (ironclaude/install.sh:104-136) | user-level SessionStart / UserPromptSubmit hook in `~/.claude/settings.json` | New jq-based additive merge code would be needed in startup.sh or bmad/install.sh. superclaude later merges additively and keeps foreign hooks (section 5). No lock against concurrent writers (ironclaude/install.sh:139). If the added hook script lives under `~/.claude/hooks/`, use a name outside the fixed managed list (install_hooks.py:42-87). |
| M4 managed settings drop-in (image-level, outside HOME) | `image/etc/claude-code/managed-settings.d/` copied to `/etc/claude-code/managed-settings.d/` (Dockerfile.coder:473-475, 498-501); listed in `image_input_files` (main.tf:87) | Hook (or any setting) that must exist in every workspace regardless of HOME content | NOT one of the six options the research question lists; it is an extra surface found. Contract test `.github/contract-tests/test-73-claude-retention.sh` pins `10-retention.json` to exactly `{"cleanupPeriodDays": 90}` (lines 3-9, 68-75, 117-118) and checks the merged managed tier still ends with `cleanupPeriodDays = 90` (78-96); a second file was NOT checked against the whole test (only grep-matched lines read): [UNVERIFIED] that adding `20-*.json` passes. Doc-sourced: managed settings have the highest precedence and "Nothing in your own settings files ... overrides a managed key" (https://code.claude.com/docs/en/settings, Settings precedence). Whether hooks defined in a managed drop-in MERGE with or REPLACE user-level hooks is not stated on that page: [UNVERIFIED]. Dockerfile.coder:498-499 comment says managed settings "apply to every user and launch path". |

Persistence facts that decide options B and D (from sections 1-5):
- A file placed under `~/.claude/` by hand or by boot code lives on the home volume (main.tf:594-597) and survives workspace stop/start and `coder update` image changes. [CODE-VERIFIED for the mount; behaviour on image replacement inferred from the mount, not exercised.]
- A NEW workspace gets a new, empty home volume (`coder-${workspace.id}-home`, main.tf:174-176); a hand-written user-level skill or hook therefore does not exist there unless boot code seeds it (M1/M2/M3) or the image carries it (M4). Whether the old volume is destroyed on workspace deletion is [UNVERIFIED].
- `superclaude install` (even `--force`) does not remove or rewrite a skill directory or hook entry outside its managed names (section 5), and the boot code never re-runs it unless the IronClaude sha changes.
- Settings edits (including `hooks`) are reloaded by a running Claude Code session without restart per the doc page (https://code.claude.com/docs/en/settings, "When edits take effect"): doc-sourced, [UNVERIFIED in this workspace].
- Option E context (`bmad install --directory ~`): `bmad install --help` (run, version 6.9.0) lists `--directory <path>`; bmad/install.sh:24 and 32 show the repo-level install puts skills at `<directory>/.claude/skills/bmad-*`, so a home-directory run would be expected to land in `~/.claude/skills/bmad-*` and `~/_bmad`. That is an inference; no install was run. Such directories sit outside superclaude's managed names (section 5), so superclaude would not touch them.

### NEEDS OTHER-REPO CHANGE

- User-level skill (Options B / delivery via M1 or M2): **NO**. Every placement mechanism above is in this repo (`startup.sh`, `catalogue/bmad/install.sh`, `Dockerfile.coder`, `main.tf` `image_input_files`), and superclaude leaves a non-packaged skill name alone. [CODE-VERIFIED against install_skills.py:88-110 and install_skill.py:46-52]
- User-level hook (Option D via M3 or M4): **NO**. A hook entry with a new command string is preserved by superclaude's additive merge, and ironclaude/install.sh:104-136 already asserts that pre-existing hook commands survive. [CODE-VERIFIED]
- Would become YES only if the intent were to ship the skill or hook FROM IronClaude (add it to superclaude's packaged `skills/` or `hooks/` lists, install_skills.py / install_hooks.py:42-87) or to make superclaude prune or manage a BMAD-named surface. Neither is required for any option that was analysed. Also YES if a future superclaude version starts pruning unknown directories under `~/.claude/skills/`: today it does not (rmtree only at install_skills.py:97 and install_skill.py:48), and nothing in this repo asserts that user skills survive (the repo-side guard covers hook commands only, ironclaude/install.sh:133-136). No IronClaude or IronOrca file was read except the installed read-only copy under `/opt/uv/tools/superclaude/`.

Key Takeaways
- Option B and D are both deliverable entirely inside this repo; none of M1-M4 needs an IronClaude or IronOrca edit.
- M1 reaches every new workspace but never updates an existing file; M2 runs every boot and can refresh; M4 is HOME-independent but is constrained by test-73 and an unverified hook-merge question.
- A BMAD-named user-level skill or hook does not collide with superclaude's managed set, and a new COPY in Dockerfile.coder costs an image layer under a stated layer budget.

## 7. Answer index for the five questions

| Q | Short answer | Where |
|---|--------------|-------|
| (a) boot order, idempotency | `coder_script.startup` runs `aidev-startup` every start; sections 1,2,3,6,7,8,9,10,12 in file order (test-7 pins the markers); §6 copy-if-absent, §9 each slug's install.sh idempotent; whole thing re-runs each boot | sections 1, 2 |
| (b) HOME persistence | `/home/coder` is per-workspace named volume `coder-<id>-home`; `/config/workspace` is a second volume; everything else is the image | section 1 |
| (c) writers and content | superclaude (via ironclaude slug), Orca (3 skills), specstory-cleanup (removal), user, Claude Code; skills by name in section 4; no `bmad-*` skill and no user-added skill present | sections 3, 4 |
| (d) overwrite vs merge | hooks additive by exact command; defaults fill-only; skills per packaged name, `--force` rmtree only those names; user additions survive | section 5 |
| (e) where to write; other repo? | M1-M4 in this repo; NEEDS OTHER-REPO CHANGE: NO for skill, NO for hook | section 6 |

## Gaps and Questions

No [CODE-CONTRADICTED] claims were found. The items below are every [UNVERIFIED] item (12 in total), each with the reason.

Fix cycle 1 pointer (findings 2 and 4): the addendum at the end of this file (`## Addendum (fix cycle 1): Finding 4 ...`) defines the first-use trigger predicate `FIRST_USE(P)`, gives a walkthrough per option, and closes 01 U8 (`block-bare-python.sh` reaches Default-profile workspaces through the ironclaude slug); it lists 12 further UNVERIFIED items (numbered 13 to 24 in its own table). The "Other open questions" about pinned tests are answered by the finding 2 addendum in `04-pinned-tests-57-46-19.md`. U7 and U9 (user-level skill loading, mid-session discovery) stay open until web-01.

| # | UNVERIFIED item | Reason |
|---|-----------------|--------|
| 1 | The home volume is destroyed when a workspace is deleted | main.tf declares `docker_volume.home` (174-176) but destroy behaviour is provider behaviour, not read from source here |
| 2 | `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/_src/superclaude/cli/` copies of `install_user_setup.py` and `user_settings_defaults.json` are identical to the `cli/` copies that were read | Second Glob hit not compared; the first path is the importable package |
| 3 | Claude Code itself writes `~/.claude/settings.json` (via `/config`) | Doc-sourced only (https://code.claude.com/docs/en/settings), not seen in code |
| 4 | Orca writes `~/.claude/settings.json` concurrently | Only a comment (ironclaude/install.sh:139); `image/orca/runtime.mjs` shows no such write |
| 5 | Hooks defined in a `/etc/claude-code/managed-settings.d/*.json` file merge with, rather than replace, user-level hooks | The fetched settings page covers precedence and list merging for permissions, not hooks in the managed drop-in directory |
| 6 | A second drop-in file (for example `20-*.json`) passes `.github/contract-tests/test-73-claude-retention.sh` | Only grep-matched lines of the test were read (3-9, 68-96, 110-133) |
| 7 | A running Claude Code session picks up a changed `hooks` block without restart | Doc-sourced ("When edits take effect"), not exercised |
| 8 | Each entry in `~/.claude/skills/` is a real directory rather than a symlink | Only `ls -1A` names and `ls -ld` on the parent were run |
| 9 | Claude Code discovers a skill directory created mid-session without restart (relevant to "first use" timing) | The settings page does not say; skills docs not fetched |
| 10 | startup.sh §10 affordance-render (1348-1450), tool-floor-verify (1451-1664) and §12 (1665-1863) never write `~/.claude/settings.json` or `~/.claude/skills/` through a `claude` CLI call | Those ranges were not read; a whole-file Grep for `.claude` and `settings.json` found no hit beyond lines 275, 979, 1172, 1282, 1285 |
| 11 | `wire_ccsession()` (superclaude `install_ccsession.py`, called at main.py:209) leaves unrelated skills and settings alone | File only grep-matched (unlink at lines 70 and 88), not read |
| 12 | Docker copies the image's `/home/coder` content (Dockerfile.coder:550-555 installs dotfiles there) into a new empty named volume on first mount | Standard Docker volume behaviour, not shown by the Terraform or Dockerfile read; startup §6 re-seeds the same files anyway, so the finding does not depend on it |

Other open questions for the orchestrator
- Whether the 60 s `superclaude install` bound and the 75 s outer bound (ironclaude/install.sh:122, startup.sh:1180) matter for any new boot step: not relevant to M1, relevant to any new step added inside the ironclaude slug (not recommended by the evidence).
- Whether a fresh workspace (not this long-lived one) shows different `~/.claude/` content: not observable here; the packaged-versus-live comparison (section 4) is the best proxy.
- Which contract tests pin `startup.sh` or `Dockerfile.coder` text: a count-mode Grep over `.github/contract-tests/` matched 31 files (test-7, test-67, test-73, test-startup-boot, test-71, test-51 among them); only test-7 (marker order), test-67 (COPY sources vs `image_input_files`) and test-73 (managed settings) were looked at, and only partly. Any later change must be checked against the full set.

## Stale Documentation Found

None contradicted by code. Doc-sourced statements that were cross-checked:
- startup.tf:27-29 says the orchestrator is baked as `/usr/local/bin/aidev-startup` from `templates/VSCode-AIDev02/image/scripts/startup.sh`: [CODE-VERIFIED] Dockerfile.coder:586 (`COPY ... scripts/startup.sh /usr/local/bin/aidev-startup`); file exists (1863 lines by `wc -l`, matching the line count given in the task prompt).
- startup.sh:7-9 says section IDs 4, 5, 11 are retired: [CODE-VERIFIED] the marker grep shows 1, 2, 3, 6, 7, 8, 9, 10, 12 plus the unnumbered `tool-floor-verify` marker (lines 16-1665).
- bmad/install.sh:18 says the CLI comes from `npm install -g bmad-method@6.9.0`: [CODE-VERIFIED] Dockerfile.coder:139; `bmad --version` printed `6.9.0`.
- startup.sh:1282-1285 says the codegraph block in `~/.claude/CLAUDE.md` is re-synced every boot: [CODE-VERIFIED] code at line 1285; the helper file `scripts/lib/claude-md-block.sh` is COPYed (Dockerfile.coder:482) but its body was not read.
- ironclaude/install.sh:3 says "once per provenance git_sha": [CODE-VERIFIED] lines 26-35 and 91-97.
- main.tf:216-219 says a restart resets `/etc/aidev02/aienv.d` to the image copy while the pushed release is kept in the home volume: consistent with the mounts (594-602); the restore script `reapply-central-defaults` was not read.
- **[STALE DOC]** candidates: none found in the files read.

WEB SEARCH PROVENANCE: provider=WebFetch reason=tavily-unavailable (no `mcp__tavily__*` tool in this agent's toolset). One page fetched: https://code.claude.com/docs/en/settings. External research was otherwise not warranted (codebase question).

## Summary

The workspace boots through `coder_script.startup`, which runs the image-baked `aidev-startup` (startup.sh) on every start; sections run in a fixed order, are idempotent, and only §6 (CLAUDE.md copy-if-absent) and the post-§9 block sync touch `~/.claude`, while the ironclaude slug runs `superclaude install` only on first boot or when the image's IronClaude sha changes. `/home/coder` is a per-workspace named volume, so user-level skills and hooks persist across stop/start and image updates but a new workspace starts empty. `superclaude install --force` merges hooks additively by exact command, fills settings defaults only where keys are absent, and replaces only skills whose names are in its packaged set (39 names, none starting with `bmad`), so a user-added skill or hook survives it. A user-level skill or hook can be delivered entirely from this repo (startup §6 seeding, the bmad slug installer, a settings.json merge, or the image-level managed-settings drop-in); `NEEDS OTHER-REPO CHANGE`: NO for the skill, NO for the hook. Twelve items remain [UNVERIFIED], the main ones being hook merge behaviour in a managed drop-in, test-73 compatibility with a second drop-in file, and live skill discovery.

## Addendum (fix cycle 1): Finding 4 first-use trigger predicate, per-option walkthrough, block-bare-python.sh (01 U8)
**Status:** Complete
**Date:** 2026-11-08

### A1. Close 01 U8: does `block-bare-python.sh` exist for Coder users, and what it blocks

Read only (never run). Files: `/home/coder/.claude/hooks/block-bare-python.sh` (344 lines), `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/install_hooks.py`, `/home/coder/.claude/settings.json` (grep context only), `templates/VSCode-AIDev02/image/catalogue/profiles.yaml`.

| Claim (from the finding / file 01 U8) | Evidence | Tag |
|---|---|---|
| `superclaude/cli/install_hooks.py:85` packages the hook | install_hooks.py:85 is the list entry `"block-bare-python.sh",` inside `_FRESHNESS_SCRIPTS` (list closes at :86; `_LEGACY_SCRIPTS` at :87); the comment at :82-84 says it is a PreToolUse(Bash) UV-only gate (issue #357) | [CODE-VERIFIED] |
| The script exits 2 on a command word `python3` | block-bare-python.sh:134 (`if (b == "python" \|\| b == "python3" \|\| b == "pip" \|\| b == "pip3") { print b; exit }`), :338-341 (`case "$WORD" in python\|python3\|pip\|pip3) ;; *) exit 0`), :343-344 (message `UV-ONLY BLOCK: this command runs bare ...` then `exit 2`). The cited lines `134,343-344` are correct | [CODE-VERIFIED] |
| The hook is registered in the user's `~/.claude/settings.json` | settings.json:183-190: matcher `Bash`, command `~/.claude/hooks/block-bare-python.sh`, timeout 3 | [CODE-VERIFIED] (this long-lived workspace; a fresh workspace gets the same registration only through `superclaude install`, see section 5 of this file) |
| The ironclaude slug is in the Default profile | profiles.yaml:14 `default_profile: orca` (stored value, label "Default" at :17); profiles.yaml:18 `slugs: [claude-code, orca, ironclaude, bmad, mcp-bundle-core]`; the Minimal profile (:19-21) is `[claude-code]` only, so a Minimal workspace has neither ironclaude nor bmad | [CODE-VERIFIED] |
| The ironclaude slug is what installs the hook on boot | ironclaude/install.sh:2-3 (runs `superclaude install` into `~/.claude`), :32-35 (no-op once configured), :23-29 (`has_ic_hooks` checks a hook command containing `/.claude/hooks/`); install_hooks.py `_FRESHNESS_SCRIPTS` copy loop covered in section 5 of this file | [CODE-VERIFIED] |
| 41 matches of `python3 ` in 31 SKILL.md files under bmad-method 6.9.0 `src/` | Grep count over `**/SKILL.md` in `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/src`: 41 matching lines in 31 files | [CODE-VERIFIED] |

Breakdown of the 41 lines (my own Greps; the finding only gave the total):
- 38 lines are `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key <workflow\|agent\|workflow.on_complete>` in 30 files (the 30 are the 31 minus `bmad-advanced-elicitation`). Example: bmad-create-prd/SKILL.md:12, bmad-agent-dev/SKILL.md:23, bmad-sprint-status/SKILL.md:23,235,308.
- 2 lines are `python3 {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key agents`: core-skills/bmad-advanced-elicitation/SKILL.md:41 (inside a ```bash block) and bmm-skills/4-implementation/bmad-retrospective/SKILL.md:94.
- 1 line is `python3 {skill-root}/scripts/list_customizable_skills.py --project-root {project-root}`: core-skills/bmad-customize/SKILL.md:34.
- 38 + 2 + 1 = 41. [CODE-VERIFIED]

Does the hook catch these? The scanner reads each Bash `tool_input.command`, takes the first real command word after skipping assignments and the wrappers sudo, nice, nohup, time, exec, timeout, env, command, coproc (block-bare-python.sh:84-86, 109-134), and blocks when its basename is `python3`. A SKILL.md step that makes the agent run `python3 /abs/_bmad/scripts/resolve_customization.py ...` as the command word is therefore blocked with exit 2 (:343-344). Known ceilings that are NOT blocked: `bash -c "python3 x"`, `eval`, `xargs python3`, `find -exec python3`, a heredoc piped into a shell, and versioned names such as `python3.12` (header lines 48-61). `uv run python3 ...` is not blocked because `uv` is the command word (the message at :343 itself recommends `uv run python ...`). [CODE-VERIFIED by reading the scanner; NOT exercised, the hook was not run]

Whether Claude actually emits the bare form is [UNVERIFIED] (it depends on the model following the SKILL.md text literally). If it does, the PreToolUse hook blocks it before any permission prompt is shown, so on a Default-profile Coder workspace the 38 `resolve_customization.py` steps, the 2 `resolve_config.py` steps and the 1 `list_customizable_skills.py` step fail as hook errors, not as script errors. [Inference from :338-344; UNVERIFIED at runtime]

Consequence for the SKILL.md fallback:
- The script itself says `uv run` is the runner BMad is standardizing on and that "a plain `python3` on PATH still works during the transition" (src/scripts/resolve_customization.py:15-17), and the error path points to the SKILL.md fallback (:46-51). [CODE-VERIFIED]
- 25 of the 31 files carry the text `**If the script fails**, resolve the ... block yourself by reading these three files in base -> team -> user order` (Grep count for `If the script fails`: 25 files; example bmad-prfaq/SKILL.md:35, bmad-agent-dev/SKILL.md:25). [CODE-VERIFIED]
- The 6 files that have a `python3 ` line but NO `If the script fails` text are: core-skills/bmad-advanced-elicitation, core-skills/bmad-customize, bmm-skills/2-plan-workflows/bmad-validate-prd, bmad-create-prd, bmm-skills/3-solutioning/bmad-create-architecture, bmad-edit-prd (derived by subtracting the 25 file list from the 31 file list; not separately printed per file). bmad-create-prd/SKILL.md:12 (read) is a deprecation shim that just says "Resolve customization:" with no fallback text. The other five were not individually read for an alternative fallback: [UNVERIFIED].
- So a hook block is handled by a written fallback in 25 files, if Claude treats the block as "the script fails" (UNVERIFIED), and by nothing written in 6 files.

U8 verdict: CLOSED for the file-and-code part. The hook is packaged by superclaude (install_hooks.py:85), installed by the ironclaude slug that the Default profile selects (profiles.yaml:18, ironclaude/install.sh:2-3), registered as a PreToolUse Bash hook (settings.json:183-190 here) and exits 2 on a command word `python3` (block-bare-python.sh:134, 343-344). A `minimal`-profile workspace has no ironclaude slug (profiles.yaml:19-21), so it has no such hook from the boot code; that workspace is not blocked. Still UNVERIFIED: that a freshly created Default workspace ends up with the same settings.json registration (this workspace is long-lived, section 4) and that Claude emits the bare `python3` form. Statement for 01 section 7.5: the hook DOES exist for Default-profile Coder users (packaging, install chain and exit-2 rule), so the 41 `python3 ` steps would be blocked there if Claude emits the bare `python3` form and the registration is present (UNVERIFIED, Gaps 13-14; corrected in fix cycle 2, finding 3), and in that case the written `If the script fails` fallback in 25 of 31 files (not the 6 listed above) is the only path; `uv run` is the runner the package itself prefers (resolve_customization.py:15-17) and the installer's own end-of-install box says BMAD "increasingly run[s] Python scripts via uv run" (installer.js:1236-1237). [CODE-VERIFIED for the hook (existence, registration in this workspace, exit-2 rule); UNVERIFIED for the effect on the 41 steps: whether Claude emits the bare form (Gap 14) and whether a fresh workspace has the registration (Gap 13)]

### A2. One first-use trigger predicate, and the guard it matches

Terms: P is the project root that a first-use install would target (the argument of `--directory`). Facts that fix the definition:

| Fact | Evidence | Tag |
|---|---|---|
| The only existing "never had BMAD" guard in this repo is `install.sh:22-25`. Branch 1 (:22-23): `D` empty OR `git -C D rev-parse --is-inside-work-tree` is not `true` prints "no seed repo recorded; nothing to configure". Branch 2 (:24-25): `[ -e "${D}/_bmad" ]` OR non-empty `git -C D ls-files -- '.claude/skills/bmad-*'` prints "seed repo already has BMad ... left untouched". Branch 3 (:26-55): everything else installs. The marker is written after all three branches (:57-60) | bmad/install.sh:21-60 | [CODE-VERIFIED] |
| The guard tests `_bmad` by plain existence, not by `_bmad/_config/manifest.yaml` and not by `_bmad/config.toml`. A partial `_bmad/` left by a failed run is therefore treated as "already has BMad" and is never repaired (comment at :41) | install.sh:24, 41 | [CODE-VERIFIED] |
| The guard's skills test counts only TRACKED files. The slug itself writes `/.claude/skills/bmad-*/` into `info/exclude` (:32), so skills it installed are untracked and invisible to `ls-files`; after such an install the guard relies on `_bmad` existing. If `_bmad/` is deleted and the untracked `.claude/skills/bmad-*` stay, the guard reports "never had BMad" | install.sh:24, 28-34 | [CODE-VERIFIED] by reading; the stated outcome is derived, not run |
| A directory without `.git` can never reach branch 2 or 3: it ends in branch 1 (:22-23). So a no-`.git` folder is "nothing to configure" for the slug as written, not "first use" | install.sh:22 | [CODE-VERIFIED] |
| For a subfolder of a repo, `git rev-parse --is-inside-work-tree` is `true` for the subfolder, so the guard would not stop at branch 1. But the exclude patterns it writes are root-anchored (`/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/`, :32) and the before/after `git status` check (:38, 48-53) would FAIL the slug for an install into a subfolder whose `sub/_bmad/` those patterns do not cover | install.sh:32, 38, 48-53 | [CODE-VERIFIED] for the code; that git anchors `info/exclude` patterns at the work-tree top is git documentation, not run here: [UNVERIFIED] |
| The installer's own notion of an existing install is `P/_bmad` existing at all: `findBmadDir(P)` always returns `P/_bmad` ("Always uses the standard _bmad folder name") and `ui.js` sets `hasExistingInstall = await fs.pathExists(bmadDir)`. (Corrected in fix cycle 2, finding 6: this row used to cite `official-modules.js:770-797` and the "any direct child directory with `_config/manifest.yaml`" rule. That function is a different, older `findBmadDir` that only serves `loadExistingConfig` (official-modules.js:833, call at :842) to load existing config; it is NOT the installer's existing-install check. This now agrees with file 01 at `01:463`.) | bmad-method/tools/installer/core/installer.js:1549-1552 (`findBmadDir`, constant `BMAD_FOLDER_NAME = '_bmad'` at ide/shared/path-utils.js:21); ui.js:217-220; official-modules.js:770-797 and 833-842 (config loading only) | [CODE-VERIFIED] |
| Skills that work need `_bmad/config.toml`: `resolve_config.py` loads it with `required=True` and exits 1 when absent | src/scripts/resolve_config.py:156 (also :6-9 for the four layers) | [CODE-VERIFIED] |
| `resolve_customization.py` locates the project root by walking up from the skill directory, then from cwd, to the first directory that contains `_bmad` OR `.git` | src/scripts/resolve_customization.py:58-66, 215 | [CODE-VERIFIED] |
| The installer's ancestor-conflict refusal is OFF for claude-code: the only reader is `if (this.installerConfig?.ancestor_conflict_check)` (_config-driven.js:191) and the key appears in platform-codes.yaml only in a header comment (:10), not in the claude-code block (:52-57). So a user-level or parent-level `bmad-*` skill dir does NOT make `bmad install` refuse a project install | _config-driven.js:191; platform-codes.yaml:10, 52-57 | [CODE-VERIFIED] (whole-`tools/installer` Grep: 2 hits, both listed) |

Proposed single predicate (a definition for the report to adopt; nothing implemented):

FIRST_USE(P) is true when ALL hold:
1. P is the git work-tree top (`git rev-parse --show-toplevel`) when inside a repo, otherwise the current directory. A subfolder of a repo resolves to the repo top, not to the subfolder, so that the root-anchored excludes and `find_project_root` (stops at `.git`) agree. [design choice; consequence for monorepo subfolders is an owner decision]
2. `[ ! -e "$P/_bmad" ]`: the same test as install.sh:24, first half. This also covers "`_bmad/config.toml` absent", because `config.toml` lives inside `_bmad/`.
3. `$P/.claude/skills/bmad-*` has no entry on disk (tracked OR untracked). install.sh:24 only checks tracked entries, so this part is stricter than the guard and must be a filesystem glob.
4. The directory is writable. (Not in install.sh; added because the installer creates `_bmad/`, `_bmad-output/` and `.claude/skills`.)

State outside the predicate: `_bmad/` exists but lacks `_config/manifest.yaml` or `config.toml` is a BROKEN install, not first use (install.sh:41 and file 01 section 8.1, "partial `_bmad/`"); the predicate returns false and the recovery path is the manual command in manifest.yaml:14.

What the predicate matches in the existing code: it is install.sh:24 (`-e _bmad` OR tracked skills) widened by the untracked-skills glob, with the `.git` requirement of install.sh:22 REMOVED. The two tests the finding listed map as: `_bmad/` absent = install.sh:24 first half; `_bmad/config.toml` absent = implied (inside `_bmad/`), enforced by `resolve_config.py:156`; subfolder of a repo = resolve to the repo top (item 1); no `.git` = install.sh:22 sends it to "nothing to configure", so a first-use mechanism for no-`.git` folders cannot reuse the slug's branch order. Whether `bmad install` itself works with no `.git` was NOT observed: the installer code touches git only in module-cache code (external-manager.js:330, 356, 391; custom-module-manager.js:493), none of which is on the built-in `--modules bmm` path by file 01 section 3.4; run unobserved, [UNVERIFIED] (file 01 U11).

The one command every option runs on a true predicate (same flag set as install.sh:42 and manifest.yaml:14; options verified in bmad-method/tools/installer/commands/install.js:14-37): `NPM_CONFIG_OFFLINE=true bmad install --yes --directory "$P" --modules bmm --tools claude-code --output-folder _bmad-output --user-name "<name>"`.

### A3. Short first-use walkthrough per option (B1/B2/B3, C, D1/D2/D3)

Shared facts for all walkthroughs (what the install itself shows and writes):
- Command, flags and `bmad` wrapper: the wrapper `/usr/local/bin/bmad` is a two-line `#!/bin/sh` that `exec`s node on the package bin (Dockerfile.coder:134-143; package pin `bmad-method@6.9.0` at :139). It runs no Python, and the block-bare-python scanner skips a leading `NAME=value` word (block-bare-python.sh:108) and then sees `bmad`, not `python3`, so the install command is NOT blocked by the hook (derived from the scanner; the hook was not run). [CODE-VERIFIED for wrapper; scanner outcome derived]
- Output the user sees at the end: Claude Code line `Claude Code configured: <N> skills -> .claude/skills` (_config-driven.js:477-479, `printSummary`), `Installed to: <bmadDir>` (installer.js:1219-1221), then a box titled `BMAD is ready to use!` with "Get started: 1. Launch your AI agent from your project folder 2. ... Invoke the bmad-help skill" (installer.js:1230-1243). `<N>` is not known (file 01 U12). Duration is not known (file 01 U1). [CODE-VERIFIED for the strings]
- Where things appear in P: `P/_bmad/`, `P/_bmad-output/`, and `P/.claude/skills/bmad-*` (claude-code `target_dir: .claude/skills`, platform-codes.yaml:56; `path.join(projectDir, target_dir)`, _config-driven.js:247-248). The existing exclude and `git status` comparison (install.sh:27-53) is what keeps these out of git for a git repo. [CODE-VERIFIED]
- Restart need: the installer's own text tells the user to "Launch your AI agent from your project folder" AFTER the install (installer.js:1233), i.e. it assumes a fresh agent start. Whether a running Claude Code session picks up `.claude/skills/bmad-*` created during the session is U9 / this file's Gap 9: [UNVERIFIED], decided by web-01.
- Permission prompt: `~/.claude/settings.json` has NO top-level `permissions` key (key list in section 4; targeted Grep for `"permissions"`, `defaultMode`, `"allow"` found only the unrelated `skipDangerousModePermissionPrompt: true` at settings.json:384) and `user_settings_defaults.json` has no permissions or defaultMode entry. So nothing in this workspace's user settings pre-approves a Bash command, and a brand-new project has no `.claude/settings*.json` yet. By Claude Code's documented default a Bash command that is not allow-listed prompts the user; that is doc-sourced and [UNVERIFIED] here (web-01). `skipDangerousModePermissionPrompt` only concerns the bypass-mode warning; its exact effect is also doc-sourced, [UNVERIFIED]. The `PermissionRequest` hook (settings.json:248-258) is an Orca pass-through that prints `{}` or calls `~/.orca/agent-hooks/claude-hook.sh`; that script was not read, so whether it ever decides a permission is [UNVERIFIED].

B1, B2, B3 (a user-level skill under `~/.claude/skills/`, delivered by install.sh, `/etc/skel` seed or a root `coder_script`; variants defined in file 02 section 6.1):
1. The user opens Claude Code in a project that has no BMAD and asks for a BMAD skill, or invokes the stub by its slash name. (The stub name and how the user learns it are open design points; the 41-step skills are NOT there yet, because `.claude/skills/bmad-*` does not exist in P.)
2. The stub's SKILL.md evaluates FIRST_USE(P) (A2) in Bash (a Bash tool call; the user sees it) and, if true, runs the install command above in P. Prompt: see shared facts (expected to prompt, UNVERIFIED).
3. The user sees the installer output and the `BMAD is ready to use!` box. `P/.claude/skills/bmad-*` now exist.
4. Restart: the installer text says relaunch (installer.js:1233); live loading is U9 (UNVERIFIED). If a relaunch is needed, the stub must tell the user to `/exit` and start `claude` again in P.
5. Open before this can be called working: U7, whether Claude Code loads a `~/.claude/skills` stub in every project and how it ranks a stub against a project skill of the same name. After step 3, a stub named `bmad-*` and project `bmad-*` skills may coexist; the installer will not object (ancestor check is off for claude-code, A2 table) but ranking is U7 (UNVERIFIED).
6. The skill files from the stub are on the home volume: B1 rewrites on every boot unless guarded copy-if-absent, B2 is created once, B3 on every start (file 02 sections 6.1, 6.4). Nothing about step 1-4 differs between B1, B2, B3 for the user; only the delivery route differs (file 02 section 6.4).

C (image-level `bmad` wrapper change, Dockerfile.coder:142):
1. The user types `bmad <command>` in a terminal (not inside Claude Code) in a directory where FIRST_USE(P) is true; the wrapper (which today only `exec`s, Dockerfile.coder:134-143) would evaluate the predicate and run the install into P before passing the user's command on.
2. No Claude Code permission prompt exists on this path: the user runs it in their own shell. (If Claude runs `bmad` through its Bash tool, the shared permission-prompt rule applies.)
3. Output is the installer output in the terminal, plus the `BMAD is ready to use!` box. `P/.claude/skills/bmad-*` appear in P.
4. Restart: any Claude Code session started in P AFTER this has the skills at launch (installer.js:1233). A session already running in P: U9.
5. Trigger limits: the wrapper must pass `bmad install` and `bmad --version`/`--help` through unchanged (health check manifest.yaml:25; slug install.sh:18, 42; file 02 section 6.2). It cannot fire when a user invokes a BMAD slash skill, because no `bmad` process runs then (file 02 section 6.2, inference, UNVERIFIED). Subcommands that exist in 6.9.0: `install`, `status`, `uninstall` (bmad-method/tools/installer/commands/{install,status,uninstall}.js; Glob of that directory returned exactly those three files). The skills are therefore not reachable by this option until the user has run some `bmad` command first. U7 and U9 do not decide C except for step 4.

D1, D2, D3 (a user-level or managed SessionStart / UserPromptSubmit hook; variants in file 02 section 6.3):
1. The user starts `claude` in a project. The hook fires on every session start (or every prompt) in EVERY project, not only BMAD ones: `~/.claude/settings.json` already has SessionStart (5), UserPromptSubmit (3) and PreToolUse (3) registrations (section 4); line 9, 59, 171 are the three event blocks here.
2. The hook command evaluates FIRST_USE(P) cheaply and exits 0 when false. On true it runs the install. All 29 `timeout` values in this settings.json are 1 to 10 seconds (settings.json lines 15-310; `block-bare-python` has 3, :188), and the install time is unknown (U1) with the existing slug using a 120 s bound (install.sh:42, an author assumption). A hook that waits for the install needs a much larger `timeout` than any existing hook uses, or must run in the background; either way what Claude Code displays from a SessionStart hook's output is doc-sourced and UNVERIFIED here. Hooks do not use the Bash permission prompt per Claude Code docs (doc-sourced, UNVERIFIED), which is why D removes the user's chance to say no.
3. Skills are created AFTER the session has started. Whether this session sees them is U9. If it does not, the user must relaunch `claude`; nothing in the hook can show the installer's `BMAD is ready to use!` box in a way the user will notice unless the hook prints it (UNVERIFIED how hook output is shown).
4. D1/D3 write `~/.claude/settings.json`: same two hazards as file 02 section 6.3 (the `/.claude/hooks/` substring that IronClaude treats as its own, ironclaude/install.sh:15-16, 25; no lock against the Orca writer, :139). D2 (managed drop-in under `/etc/claude-code/managed-settings.d/`) avoids HOME and settings.json but is limited by test-73 and by the unverified question of whether a managed drop-in accepts hooks (file 03 Gaps 5 and 6).
5. Blast radius: with the hook enabled, every session in every non-BMAD repo would write `_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*` without asking; that is "install everywhere", not "first use of BMAD" (research-notes.md option D row). The decision to treat "opening a session" as first use is an owner reading (research-notes.md open question 2).

Which results depend on U7/U9 (state plainly): B: steps 4-5 (live loading, ranking). D: step 3 (live loading). C: only the already-running-session case of step 4. The command, predicate, written files and printed text above do NOT depend on U7/U9.

### A4. U7 and U9 stay open until web-01

U7 (does Claude Code load `~/.claude/skills` in every project, and how does it rank a user-level skill against a project skill of the same name) and U9 (does Claude Code load `.claude/skills/bmad-*` created mid-session) are Claude Code behaviours. No file in this repo, in `/opt/nvm/.../bmad-method` or in `/opt/uv/tools/superclaude` decides them; this fix cycle read none of the Claude Code documentation for them and ran no Claude Code session to test them. They remain [UNVERIFIED] and decide B (U7, U9) and D (U9) and the already-running case of C until `research/web-01-*` reports from official docs. Nothing in A1 to A3 should be read as an answer to U7 or U9.

### A5. Correction to file 01 section 7.5, and addendum Gaps and Questions

Corrections found while verifying (both [CODE-CONTRADICTED] as written in file 01 / the finding):
- File 01 section 7.5 says "The 6.9.0 bmm skills instruct `python3 {project-root}/_bmad/scripts/resolve_customization.py ...`" and that the fallback is "read `customize.toml` directly". Code: the 41 `python3 ` lines are in 31 files, of which 2 are CORE skills (`core-skills/bmad-advanced-elicitation`, `core-skills/bmad-customize`) and 29 are bmm skills; 3 of the lines run other scripts (`resolve_config.py` x2, `list_customizable_skills.py` x1); the written `If the script fails` fallback exists in 25 of the 31 files, and the fallback reads three TOML files (`customize.toml`, `custom/<skill>.toml`, `custom/<skill>.user.toml`), not only `customize.toml` (bmad-prfaq/SKILL.md:35-39; bmad-agent-dev/SKILL.md:25-29). Also the `resolve_config.py` steps (advanced-elicitation:41, retrospective:94) have no fallback text in what was read (retrospective was grep-read at line 94 only: [UNVERIFIED] that it has none).

The existing `## Gaps and Questions` table above was not edited (the fix-cycle rule is to append only). The addendum's own UNVERIFIED items, numbered to continue that table (13 to 24), are:

| # | UNVERIFIED item | Reason |
|---|-----------------|--------|
| 13 | A freshly created Default-profile workspace has the same PreToolUse `block-bare-python.sh` registration as this long-lived `~/.claude/settings.json` | Only this workspace was read; the packaging and installation chain is CODE-VERIFIED (install_hooks.py:85, ironclaude/install.sh) but a fresh boot was not observed |
| 14 | Claude emits the bare `python3 ...` form and treats a hook block as "the script fails" so that the 25-file fallback applies | Model behaviour; the hook was deliberately not run |
| 15 | The 5 other no-fallback files (`bmad-advanced-elicitation`, `bmad-customize`, `bmad-validate-prd`, `bmad-create-architecture`, `bmad-edit-prd`) have no other written fallback | Only `bmad-create-prd` (a shim) and `bmad-advanced-elicitation` line 41 were read; the other four were derived by subtracting the file lists |
| 16 | git anchors the root-anchored `info/exclude` patterns `/_bmad/` etc. at the work-tree top, so install.sh would fail on a subfolder install | Git documentation, not run (no install and no scratch repo allowed to be created beyond reading) |
| 17 | `bmad install` works in a directory with no `.git` | No install may be run; only the code read (git used only by external/custom module managers, external-manager.js:330-378, custom-module-manager.js:412-477), file 01 U11 |
| 18 | A non-allow-listed Bash command prompts the user in Claude Code, and what `skipDangerousModePermissionPrompt: true` does | Claude Code documentation, not read this cycle; no `permissions` key exists in `~/.claude/settings.json` (code-read) |
| 19 | The Orca `PermissionRequest` hook (settings.json:248-258) never decides a permission | `~/.orca/agent-hooks/claude-hook.sh` not read |
| 20 | Hooks run without the Bash permission prompt; what a SessionStart hook's stdout shows the user; hook timeout semantics for a long install | Claude Code documentation, not read this cycle |
| 21 | U7: user-level `~/.claude/skills` loading in every project, and ranking against a same-named project skill | Claude Code behaviour; open until web-01 |
| 22 | U9: mid-session discovery of newly created `.claude/skills/bmad-*` | Claude Code behaviour; open until web-01 (same as Gap 9 above) |
| 23 | Number of skills the first-use install writes and its duration | file 01 U12 and U1; no install run |
| 24 | The "untracked skills but `_bmad/` deleted" case makes install.sh:24 report never-had-BMAD | Derived from install.sh:24 and :32 by reading, not run |

**Summary (addendum, fix cycle 1).** The gap was that no file stated one trigger predicate or a user-visible walkthrough for B, C and D; the addendum defines FIRST_USE(P) as install.sh:24 (`_bmad` absent, widened to any `.claude/skills/bmad-*` on disk) resolved to the git top, notes that install.sh:22 sends no-`.git` folders to "nothing to configure", and gives a walkthrough per option built from the installer's printed text (installer.js:1219-1243, _config-driven.js:479), the written paths (`.claude/skills`, platform-codes.yaml:56) and this workspace's settings. U8 is closed with verified facts: block-bare-python.sh exists for Default-profile users (install_hooks.py:85, profiles.yaml:18, settings.json:183-190), blocks a leading `python3` (block-bare-python.sh:134, 343-344), and the 41 `python3 ` lines in 31 SKILL.md files would be blocked there if Claude emits the bare `python3` form and the registration is present (UNVERIFIED, Gaps 13-14; [CODE-VERIFIED for the hook, UNVERIFIED for the effect]; corrected in fix cycle 2, finding 3), with the `If the script fails` fallback in 25 of 31 files and no written fallback in the other 6, plus two small corrections to file 01 section 7.5. U7 and U9 remain [UNVERIFIED] and decide B and D until web-01; 12 UNVERIFIED items are listed above (13 to 24).

