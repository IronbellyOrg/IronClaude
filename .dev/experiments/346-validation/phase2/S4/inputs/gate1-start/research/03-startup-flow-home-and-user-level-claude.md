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
