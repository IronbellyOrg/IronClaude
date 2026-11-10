# Anti-Omission Report (agent 2 of 3)

**Status:** Complete (verdict and counts at the end of the file, under "Summary")
**Date:** 2026-11-08

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md` (1795 lines). Section 7 (lines 1276-1349) states "Stop condition: not triggered" (line 1325), and Section 8 (line 1351) is an implementation plan, not a RE-SCOPE PROPOSAL. So the normal rule applies: a pinned test or document missing from Section 8 is CRITICAL.

**Method:** coverage judged by meaning. I read report Sections 2.3 (232-312) and 7 (1276-1355) in full and used targeted Grep (with line numbers) on the rest. "REP Lnnn" means the substance appears at that report line. Fine-grained inventory rows below are grouped only where the rows share one report sentence.

---

## Enumeration part 1: `research/03-startup-flow-home-and-user-level-claude.md`

### 03 section 1 (Terraform persistence)
| ID | Finding | Verdict |
|---|---|---|
| 03-01 | `docker_volume.home` per workspace, mounted at `/home/coder` (main.tf:174-176, 594-597) | REP L240-241 |
| 03-02 | `docker_volume.workspace` mounted at `/config/workspace` (178-180, 599-602) | REP L240 |
| 03-03 | `docker_data` volume `coder-<id>-docker-data-<runtime>` mounted at `/var/lib/docker` only on the sysbox-runc arm (182-184, 604-614) | OMITTED (no `docker_data`/`docker-data` hit in report) |
| 03-04 | `/etc/machine-id` uploaded per workspace, stable across `coder update` (583-592) | OMITTED (no `machine-id` hit) |
| 03-05 | main.tf:216-219 comment: image `/etc/aidev02/aienv.d` is reset on restart while the pushed release is kept in the home volume | OMITTED (no `aienv.d` hit) |
| 03-06 | Interpretation: everything outside HOME, workspace and sysbox docker volume comes from the image on each recreate | REP L240 |
| 03-07 | Volume destroy on workspace delete is UNVERIFIED | REP L242 |
| 03-08 | `coder_script.startup` runs `aidev-startup` every start (`run_on_start=true`, `start_blocks_login=false`, startup.tf:42-46, 54-63) | REP L243 |
| 03-09 | Second, login-blocking `central_defaults_restore` runs `reapply-central-defaults` (main.tf:220-227) | REP L243 |
| 03-10 | Third script `coder_script.code_server` (stated as not relevant to `.claude`) | OMITTED, trivial |
| 03-11 | startup.tf:27-29 comment says orchestrator baked as `/usr/local/bin/aidev-startup`, later CODE-VERIFIED at Dockerfile.coder:586 (stale-doc cross-check) | OMITTED (no `Dockerfile.coder:586` hit), trivial |
| 03-12 | Takeaways: HOME persists `~/.claude`; boot re-runs each start so bootstrap must be idempotent; no Terraform file writes `~/.claude` | REP L244, L260 |

### 03 section 2 (startup.sh)
| ID | Finding | Verdict |
|---|---|---|
| 03-13 | `set -euo pipefail` at :14; section ids 4, 5, 11 retired | REP L246 |
| 03-14 | Boot-order rows 1-9 (§1 init, §2 runtime, §3 git-identity, §6 seed, §7 gh-auth, §8 seed clone, §9 catalogue, post-§9 sync, §10/tool-floor/§12 not read) with idempotency and `~/.claude` touch | REP L248-258 |
| 03-15 | Slugs visited in `LC_ALL=C` order: `bmad` before `ironclaude` | REP L256 |
| 03-16 | Slug loop non-blocking, no per-slug failure exits the orchestrator (710-712) | REP L256 |
| 03-17 | bmad `install.sh` is per seed repo, reads `~/.aidev/status/seed-repo-path`, prints "nothing to configure" and still writes the marker (10, 21-23, 57-60) | REP L260, L284 |
| 03-18 | Skips when `_bmad/` exists or tracked `.claude/skills/bmad-*` (24-25) | REP L284 |
| 03-19 | Adds three `info/exclude` lines, runs `NPM_CONFIG_OFFLINE=true timeout 120 bmad install ...` (line 42), fails if `git status` changed (48-53) | REP L287, L292, L1349 |
| 03-20 | bmad marker exempt from deselect removal (startup.sh:1116-1118) | REP L260 |
| 03-21 | bmad has no 30 s watchdog; other slugs 30 s, ironclaude and mcp-bundle-core 75 s (1170-1182) | REP L260, L739, L1701 |
| 03-22 | Grep for `.claude|settings.json|skills` over startup.sh hits only 275, 1172, 1282, 1285 plus 979 | REP L260 |
| 03-23 | bmad installs per seed repo only, never at user level | REP L260 |

### 03 section 3 (ironclaude install.sh)
| ID | Finding | Verdict |
|---|---|---|
| 03-24 | Runs `superclaude install` into `~/.claude` once per provenance `git_sha` | REP L266 |
| 03-25 | No-op short-circuit conditions (marker, CLI on PATH, sha file equal, `commands/sc/help.md` exists, settings hook command containing `/.claude/hooks/`) | REP L266 (lines 26-35 cited) and L1240, partial wording |
| 03-26 | Requires `~/.claude/CLAUDE.md` (seeded by startup §6) or exits 2 (line 42) | OMITTED (no hit) |
| 03-27 | `--force` whenever recorded sha differs (91-97) | REP L266 |
| 03-28 | Refuses (exit 1) malformed `settings.json` or non-object `hooks` before superclaude writes a .bak (99-103) | REP (malformed hits L1139, L1515, L1519) |
| 03-29 | Records pre-existing hook commands and FAILS the slug if any is missing (110-111, 133-136) | REP L274 |
| 03-30 | Saves and restores `CLAUDE.md` byte-for-byte and a symlinked `settings.json` | REP L1183, L1260 |
| 03-31 | `timeout 60 superclaude install`; outer 75 s bound | REP L739, L1701 |
| 03-32 | Writes `.configured` sha and marker only after verification (143-150) | REP L266 (configured file) |
| 03-33 | After first boot with unchanged sha the slug does nothing to `~/.claude`; user additions exposed to `superclaude install` only on first boot and each provenance bump | REP L266, L1240 |
| 03-34 | A failed assertion here fails only the slug (non-blocking) | REP L256 |

### 03 section 4 (live `~/.claude/` and writers)
| ID | Finding | Verdict |
|---|---|---|
| 03-35 | `~/.claude/skills/` has 42 entries, 0755 dir | REP L272 |
| 03-36 | No `bmad-*` skill dir at user level | REP L272 |
| 03-37 | Packaged 39 names vs live: exactly 3 extras `computer-use`, `orca-cli`, `orchestration` (Orca); no user-added skill | REP L272 |
| 03-38 | Whether each skills entry is a real dir or symlink is UNVERIFIED (Gap 8) | checked against gaps log below |
| 03-39 | `settings.json` regular file, 54505 bytes, mode 0644 | REP L272 (size, regular file) |
| 03-40 | Top-level key list of settings.json | OMITTED, trivial (only "no `permissions` key" appears, L294) |
| 03-41 | `env` key names (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, `..._MAX_WEB_SEARCHES_PER_SESSION`, `PONYTAIL_DEFAULT_MODE`) | OMITTED, trivial |
| 03-42 | 15 hook event types with registration counts (SessionStart 5, UserPromptSubmit 3, PreToolUse 3, ...) | REP L272, L1127 |
| 03-43 | Hook script basenames present in settings.json | OMITTED, trivial |
| 03-44 | `~/.claude/hooks/` holds 14 files matching `_FRESHNESS_SCRIPTS`/`_LEGACY_SCRIPTS` | REP L272, L274 |
| 03-45 | `/etc/claude-code/managed-settings.d/` holds only `10-retention.json` = `{"cleanupPeriodDays": 90}` | REP L272 |
| 03-46 | `~/.aidev/installed/` contents (bmad, claude-code, ironclaude, ironclaude.configured, mcp-bundle-core, orca) | OMITTED, trivial |
| 03-47 | `~/.aidev/status/seed-repo-path` does not exist here, so bmad had nothing to configure | REP L260 |
| 03-48 | Writers table (superclaude, Orca CLI, orca retirement, specstory-cleanup, startup, Claude Code, user, Orca as writer UNVERIFIED) | REP L264-270, L274 |
| 03-49 | Takeaway: repo's own code never creates a user-level skill or hook; a BMAD user skill would be the first non-packaged, non-Orca name | REP L266, L272, L1313 (partial, wording differs) |
| 03-50 | Live workspace is long-lived (22 `.bak*` files), not a fresh-boot sample | REP L234 |

### 03 section 5 (merge vs overwrite)
| ID | Finding | Verdict |
|---|---|---|
| 03-51 | Install flow order in main.py (core, commands, agents, skills, ccsession, hooks, templates, user setup, codegraph, retire MCP); `--force` to all but codegraph | OMITTED (only line cites `main.py:178-263` L310; order and the codegraph exception not stated), trivial |
| 03-52 | Hooks merge additive by exact command string; `--force` replaces owned registration in place, keeps user remainder | REP L274 |
| 03-53 | Backup `.bak.<stamp>` before every merge; malformed root or non-object hooks REFUSED; atomic `os.replace` | REP partial (L274 backup churn; L1139/1515 malformed); `os.replace` atomicity OMITTED, trivial |
| 03-54 | Defaults fill-only; managed key list; `hooks` not a defaults key; `ironclaudeMarketplace` read, never copied | REP L274 (fill-only); key list OMITTED, trivial |
| 03-55 | `claudeMdExcludes` appends three globs, refuses non-list | REP L266 |
| 03-56 | `~/.claude/hooks/*.sh` copied only for fixed name list; overwritten with `--force` for the 14 managed names | REP L274 |
| 03-57 | Skills: per packaged name, `--force` rmtree of that dir, unconditional rmtree of stale `sc-<x>` with matching `commands/<x>.md`, no prune of unknown names; Grep for `bmad` in superclaude hit only `sc-cleanup-audit-protocol` | REP L274, L1461, L1649 |
| 03-58 | Orca skills: skipped if all three SKILL.md exist, else `orca skills install` bounded by `_ORCA_TIMEOUT` 25 s | OMITTED (no `_ORCA_TIMEOUT`/25 s hit), trivial |
| 03-59 | Plugins: `claude plugin ...` commands; IronClaude catalog rewritten at `~/.claude/ironclaude-marketplace/` every run | OMITTED (no hit), trivial |
| 03-60 | `superclaude install` at boot only via ironclaude slug, with `--force` | REP L266 |
| 03-61 | Boot code does not overwrite user hook/skill; specstory-cleanup removes only the exact hook, marker `~/.aidev/specstory-cleanup.done` makes it a no-op | REP L269 (removal only); marker file OMITTED, trivial |
| 03-62 | Symlinked `settings.json` replaced by superclaude and restored by ironclaude `install.sh` | REP L1183, L1260 |
| 03-63 | Lost-update race with no lock (ironclaude/install.sh:139) | REP L274, L302 |
| 03-64 | Backup churn: 21 stamped backups, not pruned | REP L274 |
| 03-65 | Takeaways: user skill under new name and hook under new command survive `--force`; only exact collisions hazard | REP L274 |

### 03 section 6 (placement mechanisms) and section 7
| ID | Finding | Verdict |
|---|---|---|
| 03-66 | M1 `seed_if_absent`: parent dirs 0755, refuses symlinked/non-regular destination, copy-if-absent, COPY layer budget (Dockerfile.coder:468, 70 layers no headroom), `image_input_files` main.tf:80-101, test-67 | REP L300 (layer-budget wording checked in Options B/D per Section 7 L1312, L1311) |
| 03-67 | M2 bmad installer: step before marker line 57-60 runs with or without seed repo; no 30 s watchdog; catalogue hashed into tag (main.tf:74); exits 1/2 on failure | REP L301 (exit codes 1/2 not restated, trivial) |
| 03-68 | M3 settings.json hook merge: no existing helper; jq merge; hook script name outside managed list | REP L302 |
| 03-69 | M4 managed drop-in: not one of the six options; pinned by test-73; second file UNVERIFIED; hooks merge-vs-replace UNVERIFIED; doc says highest precedence; Dockerfile comment "every user and launch path" | REP L303 (precedence and Dockerfile comment OMITTED, trivial) |
| 03-70 | Persistence facts: new workspace gets empty home volume; `superclaude install --force` leaves unmanaged entries; settings edits reload without restart (doc-sourced, UNVERIFIED) | REP L241, L274, L834 |
| 03-71 | Option E context: `bmad install --directory ~` inferred to land in `~/.claude/skills/bmad-*` and `~/_bmad` | REP in Option E (L1144 onward; Section 7 L1302 "installs framework content under HOME") |
| 03-72 | NEEDS OTHER-REPO CHANGE: NO for skill, NO for hook; YES only if shipped from IronClaude or superclaude begins pruning; no repo guard for user-skill survival | REP L296, L1323 |
| 03-73 | Takeaway: M1 never updates, M2 can refresh, M4 HOME-independent but test-73 constrained | REP L1311-1312 and Options table |
| 03-74 | Answer index (a)-(e) | COVERED-BY-DEDUP (restates 03-14, 03-35 to 03-72) |

### 03 gaps, other open questions, stale-doc cross-checks
| ID | Finding | Verdict |
|---|---|---|
| 03-75 | Gaps 1-12 (UNVERIFIED items) | see `gaps-and-questions.md` enumeration below; Gaps 1, 12 REP L242; 5, 6 REP L303; 10 REP L258; 11 and 2 REP L680-681 |
| 03-76 | Other open question: 60 s / 75 s bounds matter for steps inside the ironclaude slug | REP L739, L1701 |
| 03-77 | Other open question: a fresh workspace may differ from this long-lived one | REP L234 |
| 03-78 | Other open question: 31 contract-test files match Grep for `startup.sh`/`Dockerfile.coder` text; only test-7, 67, 73 partly looked at; any change must be checked against the full set | COVERED-BY-DEDUP by the 04 pinned-test inventory (L348-L379), which answers it; the "31 files" count itself is not stated (no hit), trivial |
| 03-79 | Stale-doc cross-checks (startup.tf comment, retired ids, `npm install -g bmad-method@6.9.0` Dockerfile.coder:139, block sync, once-per-sha, main.tf:216-219) | REP in part (retired ids L246); others OMITTED, trivial verification notes |
| 03-80 | WEB SEARCH PROVENANCE: WebFetch used because tavily unavailable; one page fetched | OMITTED here; web provenance is in Section 5/10 for the web files (trivial) |

### 03 addendum (fix cycle 1) A1 to A5
| ID | Finding | Verdict |
|---|---|---|
| 03-81 | `install_hooks.py:85` packages `block-bare-python.sh` (UV-only PreToolUse gate, issue #357) | REP L276 |
| 03-82 | Script exits 2 on command word `python3` (block-bare-python.sh:134, 338-344) | REP L276 |
| 03-83 | Registered in `~/.claude/settings.json:183-190` (matcher Bash, timeout 3) | REP L276 |
| 03-84 | `profiles.yaml:14` `default_profile: orca` (label "Default"), slugs list `[claude-code, orca, ironclaude, bmad, mcp-bundle-core]`; Minimal is `[claude-code]` | REP L276 (L340 `default_profile`) |
| 03-85 | Ironclaude slug installs the hook on boot (has_ic_hooks check) | REP L276 |
| 03-86 | 41 `python3 ` lines in 31 SKILL.md files; breakdown 38/2/1 with example files | REP L276 (examples OMITTED, trivial) |
| 03-87 | Scanner skips assignments and wrappers (sudo, nice, nohup, time, exec, timeout, env, command, coproc) and blocks on basename `python3`; `uv run python3` not blocked | REP partial L276 ("scanner sees `bmad`"); wrapper list and `uv run` exemption OMITTED, trivial |
| 03-88 | Known ceilings NOT blocked: `bash -c "python3 x"`, `eval`, `xargs python3`, `find -exec python3`, heredoc to shell, `python3.12` | OMITTED (no `bash -c`, `xargs`, `python3.12` hit) |
| 03-89 | If Claude emits bare form the hook blocks before any permission prompt; failures appear as hook errors, not script errors (UNVERIFIED) | REP partial L276 (UNVERIFIED effect); "hook error vs script error" OMITTED, trivial |
| 03-90 | Script itself says `uv run` is the preferred runner, plain `python3` works during the transition (resolve_customization.py:15-17), error path points to the SKILL.md fallback (46-51) | `uv run` preference REP L278; "works during the transition" and error-path pointer OMITTED |
| 03-91 | Written `If the script fails` fallback in 25 of 31 files; reads three TOML files | REP L276, L278 |
| 03-92 | Six files without fallback; `bmad-create-prd` is a deprecation shim; the other five not individually read (Gap 15) | REP L276 (six names, derived-by-subtraction caveat); shim detail OMITTED, trivial |
| 03-93 | Installer end box says BMAD "increasingly run[s] Python scripts via uv run" (installer.js:1236-1237) | REP L1704 (hit `1236`) |
| 03-94 | U8 verdict: closed for file-and-code part; minimal profile has no hook from boot; fresh Default workspace registration UNVERIFIED | REP L276 |
| 03-95 | A2 guard branches 1-3 of install.sh:21-60 and marker after all | REP L284 |
| 03-96 | Guard tests `_bmad` by plain existence; partial `_bmad/` never repaired | REP L285 |
| 03-97 | Guard counts only TRACKED skills; slug's own exclude makes them untracked; deleting `_bmad/` leaves guard saying never-had-BMad | REP L286 |
| 03-98 | No-`.git` directory ends in branch 1 ("nothing to configure") | REP L284 |
| 03-99 | Subfolder of a repo: root-anchored excludes and git-status check fail the slug | REP L287 |
| 03-100 | Installer's own existing-install test is `P/_bmad` exists (`findBmadDir`, `ui.js:217-220`); fix-cycle-2 correction of the `official-modules.js:770-797` claim | REP L288 |
| 03-101 | Working skills need `_bmad/config.toml` (`resolve_config.py:156`, required, exit 1) | REP L289 |
| 03-102 | `resolve_customization.py` finds project root by walking up to first dir with `_bmad` or `.git` (58-66, 215) | REP L114, L517, L628 |
| 03-103 | Ancestor-conflict check is OFF for claude-code (`_config-driven.js:191`, `platform-codes.yaml:10, 52-57`) | REP L290 |
| 03-104 | FIRST_USE(P) four conditions; broken-install state not first use; recovery path manual command in manifest.yaml:14 | REP L292 |
| 03-105 | Mapping notes: predicate = install.sh:24 widened by untracked-skills glob, `.git` requirement removed; `bmad install` with no `.git` unobserved (Gap 17) | REP L292 |
| 03-106 | The one install command with flags (verified against `commands/install.js:14-37`) | REP L292 |
| 03-107 | A3 shared facts: `/usr/local/bin/bmad` is a two-line `#!/bin/sh` exec of node (Dockerfile.coder:134-143), install command not blocked by hook | REP L276, L1015, L1104-1105 |
| 03-108 | Installer end output strings (`Claude Code configured: <N> skills`, `Installed to:`, `BMAD is ready to use!` box), `<N>` and duration unknown | REP L294 |
| 03-109 | Where things land in P (`_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*`; `target_dir: .claude/skills` platform-codes.yaml:56) | REP L290, L1349 (platform-codes cited) |
| 03-110 | Restart need: installer says "Launch your AI agent from your project folder"; mid-session discovery = U9 | REP L294 |
| 03-111 | Permission prompt: no `permissions` key, `skipDangerousModePermissionPrompt` only bypass warning, `PermissionRequest` hook is Orca pass-through (settings.json:248-258) unread | REP L294, L309, L663, L868 |
| 03-112 | B1/B2/B3 walkthrough steps 1-6 (stub evaluates FIRST_USE in Bash, restart, U7 ranking, home-volume delivery differences) | REP in Option B (L1063-1095) and L1331 |
| 03-113 | C walkthrough: no Claude permission prompt on this path; wrapper must pass `install`, `--version`, `--help` unchanged; cannot fire on a slash skill; subcommands install/status/uninstall | REP L1096-1118, L1313, L1614 |
| 03-114 | D walkthrough: hook fires in every project; 29 timeouts all 1-10 s vs unknown install time; hooks skip Bash prompt; skills created after session start; D1/D3 write settings.json hazards; blast radius = install everywhere | REP L824, L1119-1143, L1346 |
| 03-115 | Which results depend on U7/U9 (B steps 4-5, D step 3, C already-running case) | REP L1127-1143 region and L1331 (covered by the option rows) |
| 03-116 | A4: U7/U9 stay open until web-01 | REP L294 (answered from docs only in Section 5) |
| 03-117 | A5 corrections to file 01 section 7.5 (41 lines/31 files, 2 core + 29 bmm, three TOML fallback files, `resolve_config.py` steps have no fallback text, retrospective only grep-read) | REP L278 (first parts); "`resolve_config.py` steps lack fallback text / retrospective grep-read" OMITTED, trivial |
| 03-118 | Addendum Gaps 13-24 | see gaps log below |

**03 count:** 118 rows: 98 REPRESENTED (some with detail-level misses listed in the Omissions table, rows 39 and 33 to 41), 5 COVERED-BY-DEDUP (03-38, 03-74, 03-75, 03-78, 03-118) and 15 OMITTED (03-03, 03-04, 03-05, 03-10, 03-11, 03-26, 03-40, 03-41, 03-43, 03-46, 03-51, 03-58, 03-59, 03-80, 03-88), all MINOR.

---

## Enumeration part 2: `research/04-pinned-tests-57-46-19.md`

Every row of every assertion table in file 04 is listed. "Table 5.1" is the pinned-assertion table at report lines 1541-1585; "2.4" is report section 2.4 (lines 314-381).

### 04 sections 0 to 2 (inventory, test-57)
| ID | Finding | Verdict |
|---|---|---|
| 04-001 | Test-list inventory: test-1 to test-79, shared numbers (1-9, 59, 73, 74), unnumbered `test-b1-affordance-matrix.sh` and `test-startup-boot.sh` | REP L371 |
| 04-002 | test-57 header facts: proves ironclaude and bmad configured state, bmad excluded OD-1, needs `--network=none --user=0`, runs as `coder` via `runuser`, wired into the contract workflow driver table, installer path `/catalogue/<slug>/install.sh` | REP L318, L338 context, Table 5.1 L1543 (`runuser` itself OMITTED, trivial) |
| 04-003 | Helper definitions `run_slug`, `record_health`, `mk_home`, `snap`, `seed_snap`, `porcelain` and what each does | REP in part (L329 `mk_home` fixture, L1534 step 5.3 names `mk_home`, `run_slug`, `snap`, `porcelain`); `seed_snap` and `record_health` internals OMITTED, trivial |
| 04-004 | `snap "${H}"` records: `find` with type and link target, sha256 of every regular file, content of `*.configured`; excludes `*/.git/index` and `./.aidev/installed/*` | REP L325 |
| 04-005 | Seed repo at `${H}/seed` is under HOME so it is covered | REP L325 |
| 04-006 | Write-location table (5 rows: under HOME, `.aidev/installed/bmad` marker, `*.configured` content only, inside `${H}/seed`, image paths outside HOME) | REP L326 and L325 |
| 04-007 | Takeaway: B/D/E/F writes break the no-seed assertion; A and C do not alter the snapshot; C could write only when the user later runs `bmad` | REP L331, L1528, L1544 |
| 04-008 | Row 173-178: cold run `expect_rc 0`, feeds FR-21 30 s budget | REP L329, Table 5.1 L1546 |
| 04-009 | Row 179-183: FR-21 proxy two-step total <= `BUDGET_MS=30000` | REP L329, L1546 |
| 04-010 | Row 323: `<seed>/_bmad/_config/manifest.yaml` exists | REP L328, L1547 |
| 04-011 | Row 324: clean seed git status stays empty | REP L328, L1547 |
| 04-012 | Row 327-329: marker written | REP L1548 |
| 04-013 | Row 331-335: second run byte-identical whole-HOME snapshot | REP L329, L1548 |
| 04-014 | Row 340-342: `record_health "configured positive ${slug}" ... Configured` | OMITTED as its own row (only in the L376 evidence range `331-342`), MINOR |
| 04-015 | Row 413-419: seed with bare `_bmad/` untouched, `seed_snap` equality, health Installed-not-Configured | REP L329, L1551 |
| 04-016 | Row 421-427: tracked `.claude/skills/bmad-*` skipped, Configured | REP L329, L1551 |
| 04-017 | Row 429-435: non-Git seed with manifest is not Configured | REP L329, L1551 |
| 04-018 | Row 437-444: tracked-but-deleted skill is not Configured | REP L329, L1551 |
| 04-019 | Row 446-448: no-seed fixture (`rm -f seed-repo-path`, `want=snap`) | REP L324 |
| 04-020 | Row 449: `expect_rc "no seed: bmad exits 0"` | REP L327, L1545 |
| 04-021 | Row 450: THE OD-1 pin `no seed: bmad writes nothing`, with per-option breakage and the replacement text (rename to `writes only <path list>`, plan snap plus one pinned file) | REP L320, L1544 (replacement text restated) |
| 04-022 | Row 451: marker still exists | REP L327, L1545 |
| 04-023 | Row 452: seedless health `Installed-not-Configured` | REP L327, L1545 |
| 04-024 | Row 454-459: dirty seed configures, status delta empty | REP L329, L1551 |
| 04-025 | Row 462-465: user `_bmad-output/prior.md` kept | REP L329, L1551 |
| 04-026 | Takeaways: exactly one assertion pins "no seed: bmad writes nothing"; the seeded installer already creates `_bmad/_config/manifest.yaml` in a registered seed | REP L320, L328 |
| 04-027 | Source cross-check: no-seed install.sh prints message and writes marker only (install.sh:21-23, 57-61) | REP L260 (03), L324 |
| 04-028 | Seeded install.sh path: excludes, `NPM_CONFIG_OFFLINE=true timeout 120 bmad install ...`, manifest required, git status check | REP L287, L292, L1349 |
| 04-029 | bmad manifest `scope: hybrid`, `install_disposition: image-baked`, `health_check.command: bmad --version` (manifest.yaml:2-4, 24-25) | REP (image-baked and `bmad --version` probe in L337-338, Table 5.1 L1567; `scope: hybrid` OMITTED, trivial) |
| 04-030 | "Configured" requirement is the single token `seed-config` (spec2-health.sh:77) | REP L211 |
| 04-031 | `seed-config` observed only via the recorded seed repo (spec2-health.sh:99-113) | REP L211, L367, L648 |
| 04-032 | Readiness hard-codes deselected bmad as `not-selected`; reprofile reader rejects any bmad row (spec2-health.sh:562, 516-529) | REP L337 |
| 04-033 | profiles.yaml:18 lists bmad in the orca profile | REP L276, L340 |
| 04-034 | Consequence: B/C/D leave `spec2_health_observed bmad` unchanged; E/F do not flip health either | REP L367, L648 |

### 04 section 3 (test-46)
| ID | Finding | Verdict |
|---|---|---|
| 04-035 | test-46 runs from repo checkout paths; bmad dirs in fixtures are SYNTHETIC; only the marker-proxy scan touches the real manifest; pins slug-name rules, not real install.sh output | REP L337 |
| 04-036 | Rows 847-859 and 1134-1142 fixture setup | COVERED-BY-DEDUP by L337 ("synthetic fixtures") |
| 04-037 | Row 904-908: selected bmad slug gets its marker, report has no rows | OMITTED as a distinct row (Table 5.1 L1564 starts at 929), MINOR |
| 04-038 | Row 922, 929-933: deselection never removes bmad marker or side marker | REP L337, Table 5.1 L1564 |
| 04-039 | Row 937-943: no bmad row in the reprofile report | REP L337, L1564 |
| 04-040 | Row 947-958: deselected bmad has no health, welcome, installer ran once | REP L1564 |
| 04-041 | Row 1092-1118: strict reader rejects a bmad row (spec2-health.sh:529) | REP L337, L1565 |
| 04-042 | Row 1167: ai-pair to orca boot has no bmad row | OMITTED (no `ai-pair` hit), MINOR |
| 04-043 | Row 1184-1197: fixture bmad is `healthy` after orca boot, only claude-code and orca must classify Configured | REP L1565 |
| 04-044 | Row 1284-1288, 1297-1298, 1303-1307: readiness `bmad not-selected` | REP L337, L1565 |
| 04-045 | Row 1317-1318: unresolved profile gives `unknown` for bmad | REP L1565 (range 1284-1318) |
| 04-046 | Row 1419, 1437-1446: direct writer cases | REP L337, L1565 |
| 04-047 | Row 1479-1499: summary string `Catalogue not configured: bmad,rd-u,rd-z` | REP L337, L1566 |
| 04-048 | Row 1804-1815, 1833: marker-proxy production scan; `mp_is_marker_proxy 'bmad --version'` not proxy; never probe a user-level artifact with a file-existence check | REP L337, L1567 |
| 04-049 | Takeaways: only the marker-proxy scan reads real production files; `mp_expected` comes from profiles.yaml, so a new slug changes `mp_scanned` and `mp_expected` equally | first parts REP L337; the `mp_expected`/`mp_scanned` consequence OMITTED (plan adds no slug), MINOR |

### 04 section 4 (test-19)
| ID | Finding | Verdict |
|---|---|---|
| 04-050 | Five literal `bmad` hits and the production scan via `CATALOGUE_DIR` (`/catalogue-src` in CI) | partial REP L338; `CATALOGUE_DIR=/catalogue-src` OMITTED, trivial |
| 04-051 | Row 1106-1114: `install_disposition` must be image-baked or runtime-network | REP L338, L1570 |
| 04-052 | Row 1137-1152: classifier needs `command -v` and `exit 2`, no unquoted install verb (regex 208-209, per-line quote strip 205), what flips to RUNTIME; `npx bmad-method install` would flip it | REP L338, L1569; "`npx bmad-method install` would flip it" REP in Option notes L914/L922 context unverified; treated REP |
| 04-053 | Declaring `runtime-network` would remove the on-image `bmad --version` check (1161-1166) and is not recommended | OMITTED (no `runtime-network` hit), MINOR |
| 04-054 | Row 1175-1185: `type -P bmad` must be an executable FILE (BUILTIN_NOT_FILE for a function or alias) | REP L338, L1570 (`BUILTIN_NOT_FILE` name OMITTED, trivial) |
| 04-055 | Row 1186-1190: `bmad --version` exits 0 non-interactively without `NPM_CONFIG_OFFLINE` | REP L338, L1570 |
| 04-056 | Row 517-529: welcome_message must contain `bmad` and `bmad --help` | REP L338, L1568 |
| 04-057 | Row 545-550: invocation resolves as PATH executable | REP L1570 |
| 04-058 | Row 551-561: `timeout 10s bmad --help </dev/null` exits 0 | REP L338, L1570 |
| 04-059 | Row 496-505: invocation and help_command are canonical commands, not marker/path proxies | REP L338, L1570 |
| 04-060 | Rows 818-821 and 743-753/760: parser and ECHO-VERB self-tests, no repo state | OMITTED (self-tests), MINOR |
| 04-061 | Takeaways: test-19 never inspects what install.sh WRITES; fragile item for B/D/E/F is the shape rule, for C the CLI items; `bmad` on the image is already a `#!/bin/sh` wrapper (Dockerfile.coder:133-143) | REP L338, L1015-1016 |

### 04 sections 5 and 6 (test-49, test-52)
| ID | Finding | Verdict |
|---|---|---|
| 04-062 | test-49:349-354 listed surface must exist (`bmad/manifest.yaml` at line 310) | REP L339, Table 5.1 L1571 |
| 04-063 | test-49:355-399, regex 326: no non-comment `coder create`, `coder templates push`, `coder delete`, `docker build(x)`, `terraform apply` in the listed files; the workflow may hold exactly ONE `docker buildx build` line (383-393) | REP L339, L1571; "exactly ONE `docker buildx build` line" OMITTED, MINOR |
| 04-064 | `bmad/install.sh` is NOT in the test-49 list; bmad manifest has 0 forbidden matches today | REP L339, L1571 (0-match current-state check OMITTED, trivial) |
| 04-065 | Takeaways: test-49 is a path and forbidden-string pin; the array also covers Dockerfile.coder, startup.sh, spec2-health.sh, aienv.skel | REP L339 |
| 04-066 | test-52:1378-1383 exact profile mapping (regex needs `label:` then `slugs:` on consecutive lines); fixture block at line 798 | REP L340, L1574 (consecutive-lines regex detail OMITTED, trivial) |
| 04-067 | test-52:1384 `default_profile: orca` | REP L340, L1574 |
| 04-068 | Current profiles.yaml lines 14, 17-21 | REP L276, L340 |
| 04-069 | Takeaways: 1381-1383 is the only pin that breaks when a NEW slug joins a profile; test-52 runs runner-native pre-build (workflow:832-847) | REP L340, L1533 |

### 04 sections 7 to 9 (matrix, workflows, count cross-validation)
| ID | Finding | Verdict |
|---|---|---|
| 04-070 | Option-impact matrix, 14 rows (X/c/-): rows for test-57:450, 331-335, 179-183, 452, seed guards, test-19:1137-1152, 1175-1190/545-561, test-57:323/458 via wrapper, welcome tokens, discoverability, probe shape, deselection, readiness/summary, test-49, test-52, startup-boot | REP L356-365, Table 5.1, Table 1 L1236 |
| 04-071 | `test-startup-boot.sh` bmad readiness and MOTD strings (233, 1099-1137) UNVERIFIED | REP L318, L1554 |
| 04-072 | Option D observations: `ic_hooks` (test-57:140) true for any `/.claude/hooks/` command; bmad hook would weaken :187 and :407; self-heal fixture deletes such entries | REP L1549 |
| 04-073 | Any `settings.json` rewrite by the bmad installer must preserve the foreign Stop hook, orca PreToolUse hook and `deniedMcpServers` (test-57:325-326, 337, 364-365, 373, 379) | REP L1550 |
| 04-074 | Workflow `coder-ci-aidev02-contract.yml`, job `contract_tests`, `runs-on: [self-hosted, big]`, timeout 20, triggers (pull_request paths, push to main, nightly cron, workflow_call, dispatch) | REP L318, L1594 |
| 04-075 | Per-test run table (test-57 `docker run --rm --network=none --user=0`, test-46 PARTIAL image need, test-19 CLI half needs image, test-49 static scan only, test-52 runner-native) with workflow lines 1241, 1237, 1234, 1240, 832-847 | REP L318, L1594; the per-test "needs the built image" column (test-49 static in substance, test-46 partial, test-57 not runnable on host) OMITTED, MINOR |
| 04-076 | test-52 other modes called from `coder-ci-validate.yml:561, 591, 1028` and `coder-ci-aidev02-contract.yml:190, 206`; which mode reaches line 798 UNVERIFIED | UNVERIFIED part REP L373, L679; the validate.yml call sites OMITTED, MINOR |
| 04-077 | `orca-upstream-monitor.yml:352-353` only `git add`s test-52; no other workflow runs test-57/46/19/49; 7 files match `contract-tests` | partial: "No other workflow runs test-57, 46, 19 or 49" REP L318; the orca-upstream-monitor detail OMITTED, MINOR |
| 04-078 | `test-startup-boot.sh` run by `coder-ci-validate.yml:276-277, 301, 912, 1085` and `coder-ci-orca-boot.yml:265`; 35 bmad hits; NOT_CONFIGURED line 233 | REP L318, L1596 |
| 04-079 | Project index "T1-T55" CODE-CONTRADICTED; tests to test-79; 30 and 61 absent; 80+ absent; workflow comments "(T50..T55)" at 635 and 924 | REP L371 (workflow comments at 635 and 924 OMITTED, trivial) |
| 04-080 | Index header generated 2026-09-25 against `1ace9c30`; do not use T1-T55 as boundary | REP L371 |

### 04 gaps, other questions, stale-doc table, summary
| ID | Finding | Verdict |
|---|---|---|
| 04-081 | Gap 1: E and F write locations UNVERIFIED (wording of question) | REP L360, L1528, G-16, G-25 |
| 04-082 | Gap 2: test-startup-boot under any option | closed by A.4; REP L353, L1552-1563 |
| 04-083 | Gap 3: other contract tests that may pin the slug; 121 bmad hits in 6 files (test-46 38, test-57 41, test-startup-boot 35, test-19 5, test-49 1, test-52 1) | closed by A.1-A.8; REP in part (L342 "30 files"); per-file counts OMITTED, trivial |
| 04-084 | Gap 4 `slug-configuration.md` not read | REP L373, G-20 |
| 04-085 | Gap 5 no test run | REP L373, L1528 |
| 04-086 | Gap 6 test-52 modes | REP L373, G-20 |
| 04-087 | Gap 7 exact file count of contract-tests (111 entries seen) | REP G-20 (L679) |
| 04-088 | "No seed" means no repo registered, not a repo without BMAD; new test row needed | REP L324, L1526 |
| 04-089 | CODE-CONTRADICTED: PROJECT_INDEX T1-T55 | REP L371, CC-15 |
| 04-090 | Health for a user-created project cannot be Configured without changing spec2-health.sh and test-57 rows together | REP L367, F-07 |
| 04-091 | Stale-doc table, 7 rows: headers' wiring comments current (test-57, 52, 46, 19, 49), test-57 header consistent, manifest welcome text, Dockerfile wrapper comment, test-19:200 comment | REP L371 ("headers current"); manifest welcome text REP F-09; Dockerfile comment REP L1117; test-19:199-201 OMITTED, trivial |
| 04-092 | Summary paragraph | COVERED-BY-DEDUP (restates 04-021 to 04-069) |

### 04 addendum A.1 to A.3 (30 files, test-3, test-67, test-7, test-60)
| ID | Finding | Verdict |
|---|---|---|
| 04-093 | A.1: Grep `startup.sh|Dockerfile.coder|aidev-startup` gives 141 occurrences in 30 files, with per-file counts | REP L342 ("30 files ... 15 relevant, 15 irrelevant"); per-file counts OMITTED, trivial |
| 04-094 | A.1: the nine tests named in the finding are not among the 30 | REP L710 (CC-16) |
| 04-095 | A.2 test-3: reserved names, scan roots (`catalogue/*/install.sh`, `scripts/`, `image/bin/`, `image/scripts/`), four shim forms, `mkdir|install` line only WARNs, not scanned: Dockerfile.coder, `*.tf`, manifest.yaml, skel, workspace_defaults, image/etc | REP L347 (roots and forms); WARN-only and "not scanned" list OMITTED, MINOR |
| 04-096 | A.2 test-3 per-variant verdict table (B1 hyphen-word-boundary example `bmad-preview`, B2, B3 `modules.tf` not a root, C file-based only, D1, D2, D3, E/F) | REP L347, Table 5.1 L1577, step 3.6 L1461; `bmad-preview` example OMITTED, trivial |
| 04-097 | A.2 test-3 proposed assertion: none; naming note | REP step 3.6 L1461 |
| 04-098 | A.2 test-67 rules: COPY sources listed (46-64), Dockerfile listed (65-66), listed files exist (67-69), `image_inputs_sha256` includes `catalogue:${local.catalogue_sha256}` (71-74), docker_image name and triggers (75-81), `context = image` (101-102), no dot-prefixed entry (107-111), no Terraform work file under `image/` (112-113), no `.dockerignore` at template root (114-115), four self-tests | REP in part L348, Table 5.1 L1581 (COPY listing and hidden-entry rule); rules 65-81, 101-102, 112-113 and 114-115 OMITTED (no `dockerignore` hit), MINOR |
| 04-099 | A.2 current COPY line numbers of Dockerfile.coder | OMITTED, trivial |
| 04-100 | A.2 test-67 per-variant table (B1 NO, B2 BREAKS-IF unlisted or hidden source, B3 NO, C, D1, D2, D3, E, F) | REP L361-364, Table 5.1 L1581 |
| 04-101 | A.3 test-7: nine anchored markers in order, 4/5/11 retired, marker lines 16, 121, 160, 191, 303, 389, 692, 1348, 1665 | REP L349, L1578 |
| 04-102 | A.3 test-7 per-variant: B2 NO inside section 6 before `unset -f seed_if_absent` (294); a NEW section breaks and needs `D07` edit with ID 13+ and fixture update (136-175) | REP "No new startup section in any branch" L1578; the `D07`/`13` amendment recipe OMITTED, MINOR |
| 04-103 | A.3 test-60 (a): one COPY with `codex-config.toml` ending `/usr/local/lib/aidev/` (Dockerfile.coder:547-548); fold of skill source allowed (fix cycle 2) | REP L350, L369, L1580 |
| 04-104 | A.3 test-60 (b): three exact `seed_if_absent` lines in section 6 | REP L350, L1580 |
| 04-105 | A.3 test-60 (c): production section 6 executed on a fresh HOME with `set -e` and minimal PATH; BREAKS-IF helper defined outside section 6 | REP L350, L1580; the helper-outside-section-6 condition OMITTED (B2 not planned), MINOR |
| 04-106 | A.3 test-60 (d): `claude` printf wrapper awk extraction (162-168), reset rule at 166, Dockerfile comment 104-106 on single quotes and no heredocs | REP L350, L1580, L1507 |

### 04 addendum A.4 to A.6 (startup-boot, modules.tf pins, test-71/73/74/5)
| ID | Finding | Verdict |
|---|---|---|
| 04-107 | A.4 literal `seed_if_absent` appears in only test-60:92; 68 hits in 16 files are `/etc/skel` paths | OMITTED, trivial |
| 04-108 | A.4 F04 skel bridge list (2774-2779) | REP L353, Table 5.1 L1563 |
| 04-109 | A.4 `cmp /etc/skel/.claude/CLAUDE.md` for ironclaude (2083-2087, 3030-3037) | REP L353, L1555 |
| 04-110 | A.4 NFR18 idempotency (2763-2768) | REP L1563 |
| 04-111 | A.4 seed repo clean after fresh clone (2089-2098) | REP L1556 |
| 04-112 | A.4 install marker present for in-profile bmad (2100-2108); BREAKS-IF a step aborts before marker | REP L353, L1557, L360 |
| 04-113 | A.4 FR-21 budget <= 75 s (2129-2156) | REP L353, L1558 |
| 04-114 | A.4 Configured-state with no-seed exception (2208-2211, 2220-2235) | REP L353, L1559 |
| 04-115 | A.4 readiness rows and MOTD strings (1099, 1121-1137, 1199-1201) | REP L1554 |
| 04-116 | A.4 `agent_script_timings` one `aidev-startup` row and one agent (617-637) | REP L353, L1560 |
| 04-117 | A.4 convergence window (2631-2637), `IDE_CONVERGENCE_TIMEOUT_S` unread | REP L353, L373, L1561 |
| 04-118 | A.4 out-of-profile slug marker/health/welcome absent (2446-2479 ...) | REP L1562 |
| 04-119 | A.4 no whole-HOME oracle in the live boot test | REP L353 |
| 04-120 | A.4 wiring-parity ledger: `ledger()` (1972-1976), kinds at 232, slug whitelist at 201 and 231, `all_slugs` at 1968, `coder_script` row only for vibe-kanban (2469) | REP L353, L1552-1553, L1536 |
| 04-121 | A.5 modules.tf facts (123 lines, first `locals` 16-34, one module per slug 37-123, `orca_retirement` 82-109) | REP L1572 (82-109), L1579 (above line 16); line counts OMITTED, trivial |
| 04-122 | A.5 test-52:1374-1377 orca_retirement pin; new resource must be separate; count-gated bmad script allowed | REP L1572, L1533 |
| 04-123 | A.5 test-51:384-396 first `locals` block rule | REP L352, L1579 |
| 04-124 | A.5 test-51:598-626 consumed-path oracle by `*.tf` glob | REP L352, L1579 |
| 04-125 | A.5 test-51:457-476 env bridge name uniqueness | REP L352, L1579 |
| 04-126 | A.5 test-51 `startup_section` extraction of sections 7 and 8 and the §8 to §9 span (223-229, 1503-1510, 1759-1761, 1945-1951) | OMITTED (no `startup_section` hit), MINOR (plan edits no section 7/8) |
| 04-127 | A.5 test-51:1765 askpass COPY exact line and test-51:511-512 credential-helper RUN | OMITTED (no hit), MINOR (4C edits only the BMad RUN block) |
| 04-128 | A.5 other `coder_script` pins: test-5-coder-app-allowlist:501-512 requires exactly ONE `coder_script "code_server"` in `main.tf`; test-70-restart-stale-state:42; test-74-orca-clean-stop:63 counts `coder_script` in `catalogue/orca/module.tf` | OMITTED (only `ALLOWED_SET` of test-5 in the gap list, L679); the three verdicts are NO, so MINOR, but they bear on the planned B3/D3 `coder_script` |
| 04-129 | A.5 test-5-coder-app-allowlist scans `coder_app` slugs; no variant adds a `coder_app` | OMITTED, MINOR |
| 04-130 | A.6 test-71: exactly one `CG_VERSION=`, two `CG_ASSET` lines, ENV telemetry line, one `aidev_cg_version`; in-image checks | REP L1582 (row), L1536; in-image checks OMITTED, trivial |
| 04-131 | A.6 test-73-claude-retention: `10-retention.json` exact content, one exact COPY, one RUN with both dirs, merged managed tier alphabetical with last `cleanupPeriodDays` 90; D2 conditions (a)-(d); proposed assertion | REP L351, L1583, L1535 |
| 04-132 | A.6 test-73-codegraph-sweep irrelevant | OMITTED, irrelevant by 04's own verdict (MINOR) |
| 04-133 | A.6 test-74-claude-md-block: SUPERCLAUDE_CODEGRAPH pair byte-equal drift check; BMad block needs different markers | REP Option G L1178, L1256 |
| 04-134 | A.6 test-5-no-shadow: skel copy and `cat ls find grep` not shadowed | OMITTED, MINOR |

### 04 addendum A.7 to A.11
| ID | Finding | Verdict |
|---|---|---|
| 04-135 | A.7 test-1-tool-floor: `/source/startup.sh` cmp-identical to baked `aidev-startup`; F08 awk extraction needs one `# === tool-floor-verify ===` start and one `# === section:12 done ===` end; `INSTALL_MATRIX` tools (Dockerfile.coder:422); verdicts NO for B2/C | OMITTED as a pin (only "F08 fixtures unread" at L373 and G-20); 04 classes it RELEVANT-NO-BREAK, so IMPORTANT-candidate, rated MINOR below (see Omissions Found) |
| 04-136 | A.7 test-1-catalogue-shape: exactly `install.sh manifest.yaml module.tf`, heredoc-in-install.sh form required | REP L346, L1575 |
| 04-137 | A.7 test-2-manifest-schema: edit only `welcome_message` value | REP L1576 |
| 04-138 | A.7 test-44 and test-47 irrelevant (private temp catalogues) | OMITTED, irrelevant (MINOR) |
| 04-139 | A.7 test-2-starship-latency irrelevant | OMITTED, irrelevant (MINOR) |
| 04-140 | A.7 test-22-aienv-fresh-workspace: section 6 conflict matrix, `targets` list, B2 proposed append, new-fixture need for symlinked `.claude/skills` parent | REP Table 5.1 L1585, L367 |
| 04-141 | A.7 test-59-home-workspaces-dir: one `aidev_ws` block, `bash -n startup.sh` | REP Table 1 L1236 (B2 BREAKS-IF test-59); the pin text itself OMITTED, MINOR |
| 04-142 | A.7 test-72-legacy-mcp-retire: one production call line | OMITTED (only "body of test-72 unread" in register), MINOR |
| 04-143 | A.7 test-b1-affordance-matrix: section 10 against five mocked environments; two failure strings must have zero hits in catalogue `.tf` | partly REP L679 (failure strings unread); the pin itself OMITTED, MINOR |
| 04-144 | A.7 test-78-upstream-monitor and `.github/upstream-monitor/` (`releases.json` has no bmad; `expected.txt:6-8`; renovate extraction; `upstream-monitor.yml:161` goes red) | REP L354, Table 5.1 L1584, step 6.5 L1598 |
| 04-145 | A.8 classification table of 30 files (15 relevant with reasons, 15 irrelevant with reasons) | REP as counts only (L342); the irrelevant 15 are not named (test-68, 59-home, 77, 72, b1, 18, 66, 75, 65, 62, 12, 69, 48, 3-zellij, 2-starship), MINOR |
| 04-146 | A.8 the nine tests absent from the 30 and where they were examined; `seed_if_absent|/etc/skel` search 68 hits in 16 files, only test-5-no-shadow copies all skel | partial REP L710; rest OMITTED, MINOR |
| 04-147 | A.9 correction: the single COPY of test-60:84-88 is Dockerfile.coder:547-548; own-COPY advice withdrawn | REP L369 |
| 04-148 | A.9 `/etc/skel/.claude` created 0755 at Dockerfile.coder:474-475; same RUN is what test-73 `copy_ok` needs, do not split it; nested COPY dir modes UNVERIFIED | REP L351 (RUN with both dirs 474-475), L373 (UNVERIFIED); "do not split or reword" instruction restated in Table 5.1 L1583 |
| 04-149 | A.10 consolidated per-variant matrix (28 rows) | REP in Table 1 L1236, Table 5.1 and L356-366 (the per-row X/c grid for B2, D2, E, F columns is summarised) |
| 04-150 | A.10 certain breaks per variant: B1 = test-57:450; B2, B3, C, D2, D3 = none; D1 = test-57:450; E = test-57:450 (conditional); F void | REP L360-366, L1528 |
| 04-151 | A.10 two gaps: breaks (few) and missing proofs of delivery | REP L367 |
| 04-152 | A.11 proposed assertion texts per variant (B1, B1/D1 shape, B2 two proofs and COPY listing, B3/D3 static pin and live ledger row, C printf extraction, D2 managed-tier proof, new section D07, naming rule) | REP steps 5.2, 5.4, 5.5, step 3.6 and Table 5.1; D07 recipe OMITTED, MINOR (covered by 04-102) |
| 04-153 | Addendum Gaps (8 UNVERIFIED): nested COPY dir mode, `IDE_CONVERGENCE_TIMEOUT_S`, schema required fields, repin.sh --verify, test-b1 failure strings, test-4-pane-title skel copy and test-72 body, `ALLOWED_SET`, managed drop-in hooks | REP L373, L679, G-19, G-20, G-03 |
| 04-154 | Addendum Gaps other points (a)-(c): test-startup-boot read only partly, no test run, test-1-tool-floor F08 fixtures after line 260 unread | REP L373, L679 |
| 04-155 | Addendum summary and test-startup-boot verdict paragraph (BREAKS-IF list 1-6) | COVERED-BY-DEDUP (restates 04-108 to 04-120, 04-150) |

**04 count:** 155 rows: 133 REPRESENTED, 3 COVERED-BY-DEDUP (04-036, 04-092, 04-155) and 19 OMITTED (04-014, 04-037, 04-042, 04-053, 04-060, 04-099, 04-107, 04-126, 04-127, 04-128, 04-129, 04-132, 04-134, 04-135, 04-138, 04-139, 04-141, 04-142, 04-143), all MINOR.

---

## Enumeration part 3: `synthesis/synth-03-options-recommendation.md`

Report Section 6 (lines 986-1275) and Section 7 (lines 1276-1349) were compared with the synthesis file block by block. The report copies the synthesis structure and adds plan-driven updates (for example Effort L for B3 and D3 as planned), so each row is REP at the lines shown.

| ID | Finding | Verdict |
|---|---|---|
| S3-01 | Header: topic, sources, report sections produced | REP L986-1000 |
| S3-02 | Evidence tag table (CODE-VERIFIED, External code, External docs doc-only, UNVERIFIED, OBSERVED-FROM-6.10.0-TRACKED-TREE) | REP L990-1003 |
| S3-03 | Rating rubric: Effort XS/S/M/L/XL, Risk R1-R5 (0 = Low, 1 = Medium, 2+ = High) | REP L1005 and the rubric above it |
| S3-04 to S3-17 | Common facts 1 to 14 (decision; no first-use bootstrap; install command and `--output-folder`; FIRST_USE(P); CLI already global; health blind outside seed; no test executes first use; slug runs at boot only; layers 68 of 70; minimal profile; version skew and partial trees; decision records list; hidden-versus-visible files; `python3` steps and hook) | REP L1011-1024 (14 rows, one each) |
| S3-18 | Option list A to I with variants (B1/B2/B3, C in place/late-COPY, D1/D2/D3, E2) and origins | REP L1028-1038 |
| S3-19 | Option A: description, 5 steps, 7 assessment rows | REP L1040-1062 |
| S3-20 | Option B: description, 5 steps, delivery variants table, comparison rows, shared points | REP L1063-1095 |
| S3-21 | Option C: description, 5 steps (place, interception limits, trigger limit, seeded runs, pin strings), 7 rows, Dockerfile comment 133-135 | REP L1096-1118 (L1117 for 133-135) |
| S3-22 | Option D: description, 7 steps, D1/D2/D3 rows, doc-only hook semantics | REP L1119-1143 |
| S3-23 | Option E (with E2 and issue #1852) | REP L1144-1158 |
| S3-24 | Option F (43 hits, no consumer, 6.10.0 and 6.12.4, v7 preview) | REP L1159-1173 |
| S3-25 | Option G (instruction-text channel) | REP L1174-1188 |
| S3-26 | Option H (plugin marketplace route) | REP L1189-1203 |
| S3-27 | Option I (managed skill location) | REP L1204-1218 |
| S3-28 | Table 1, 15 criteria rows for A-F | REP L1225-1241 |
| S3-29 | Table 2, G-I criteria rows | REP L1245-1261 |
| S3-30 | Run-only facts paragraph (R-1 to R-15 subset) | REP L1263 |
| S3-31 to S3-36 | Contradictions 1 to 6 with resolutions | REP L1269-1274 (6 rows) |
| S3-37 | Recommendation intro and the ASCII reading-to-mechanism table | REP L1280-1294 |
| S3-38 | Stage 0 (a), (b), (c) | REP L1298 |
| S3-39 | Stage 1 (trigger by reading; B3 before B2 before B1; D3 or D2) | REP L1299 |
| S3-40 | Stage 2 (delivery proofs, live observation) | REP L1300 |
| S3-41 | Not recommended list (E, F, B1, D1, B2, G, H, I) | REP L1302 |
| S3-42 to S3-49 | Rationale rows 1 to 8 | REP L1308-1315 (8 rows) |
| S3-50 | Prior positions overridden by name (R1, R2, R4, R5, R6, R8, R9, R10, R12) and not overridden (R3, R7, R15, R16) | REP L1317 |
| S3-51 | Feasibility: can the ask be met without a global install | REP L1321 |
| S3-52 | Feasibility: without a change in IronClaude or IronOrca (03 lines 178-180, 02 lines 324-325) | REP L1323 |
| S3-53 | Stop condition not triggered | REP L1325 |
| S3-54 to S3-58 | Limits 1 to 5 (slash skill needs outside name; doc-only Claude Code behaviour; "no artifact" combination; version skew; run-only facts) | REP L1331-1335 (5 rows) |
| S3-59 | Open owner questions Q1 and Q2, copied unanswered | REP L1339 |
| S3-60 to S3-64 | Dependence on owner readings, rows 1 to 5 | REP L1343-1347 (5 rows) |
| S3-65 | Other open owner inputs (D-10, Orca worktrees, D-4, D-5) | REP L1349 |
| S3-66 | Synthesis Self-Audit key-finding trace table (8 rows mapping research findings to sections) | COVERED-BY-DEDUP (meta mapping, each mapped finding is enumerated above) |
| S3-67 | Excluded or reduced: stale T1-T55 claim and CHANGELOG detail (routed to the plan), 6.12.4 `uv run` change and v7 preview (reduced to the F note), upstream issue #2624 (open-question item), the 12 files of `.dev/issues/478/` (process context, not option evidence), G-20 residuals summarised | REP L371 (T1-T55), L903/L969 (`uv run`), L937 and L1702 (#2624), L72 and L413 (`.dev/issues/478`) |
| S3-68 | Self-Audit "why nothing was dropped" and contradictions-and-gaps closing notes | COVERED-BY-DEDUP (process notes) |

**synth-03 count:** 68 findings (IDs S3-01 to S3-68 with ranges expanded: 38 in the five numbered sets of common facts, contradictions, rationale, limits and dependence rows, plus 30 single rows). 66 REPRESENTED, 2 COVERED-BY-DEDUP (S3-66, S3-68), 0 OMITTED. No synth-03 finding is OMITTED. I found one wording difference only: the synthesis says Option I's path is "UNVERIFIED, path not established" while the report (L1258) states a documented path `/etc/claude-code/.claude/skills/<skill-name>/` as doc-only. That is a fidelity change in the report's favour, not an omission.

---

## Enumeration part 4: `gaps-and-questions.md`

Gap rows G-01 to G-30 are checked against report Section 4.2 (lines 658-689) and the Section 9.1 register (lines 1715-1745). UV-01 to UV-89 are checked against the register's "Open UNVERIFIED ids" column and its closed list (line 1745). CC-01 to CC-30 and SD-01 to SD-13 are checked against Section 4.3 (lines 695-722).

| ID | Finding | Verdict |
|---|---|---|
| GL-01 to GL-30 | Open-gap rows G-01 to G-30 (30 rows) | REP, all 30 present in L660-689 and L1717-1744 (G-22, G-24, G-25 listed as resolved at L1745) |
| GL-31 | Totals line: 27 open, 3 resolved, 5 to web research | REP L1713, L1745 |
| GL-32 to GL-120 | UV-01 to UV-89 (89 rows): 79 open, 10 closed or superseded (UV-21, 23, 27, 45, 46, 57, 58, 70, 71, 86) | REP: every open id appears in a register row (checked id by id against L1717-1744); the 10 closed ids are named at L1745 (89 rows) |
| GL-121 to GL-150 | CC-01 to CC-30 (30 rows) | REP L697-721, each id named (CC-01 to CC-30 appear in the "Items" column; CC-27/30, CC-28/29, CC-23/24 grouped) (30 rows) |
| GL-151 to GL-163 | SD-01 to SD-13 (13 rows) | REP L697-722 (SD-01 to SD-13 each named) (13 rows) |
| GL-164 | Stale-but-untagged items (manifest welcome text, "never globally" wording hazard, Dockerfile.coder:468 as a measurement) | REP via CC-12, CC-17, CC-13 (L706, L707, L711) |
| GL-165 | `tools/installer/README.md` was searched by Grep only, not read in full | OMITTED (no `installer/README` hit), MINOR |
| GL-166 to GL-168 | Questions Q-1, Q-2, Q-3 for web research | REP G-01, G-02, G-05 (L660, L661, L664) |
| GL-169 | Additional web-01 candidates: managed-settings drop-in hooks (G-03) and hook runtime semantics (G-04) | REP L662-663 |
| GL-170 | Owner question 1 (user-level bootstrap allowed?) | REP L732, L1339 |
| GL-171 | Owner question 2 (what counts as first use?) | REP L733, L1339 |
| GL-172 | Related owner input G-26 (decision wording, hidden vs visible, Orca worktrees) | REP L685, L734 |
| GL-173 | Third task-file question (what a first install creates that this worktree cannot show) is an evidence limit, handled in section 7 | REP L755 |
| GL-174 | Feasibility statement: yes without global install and without IronClaude/IronOrca change; trigger not determinable; stop condition not triggered | REP L642, L1319-1325 |
| GL-175 to GL-183 | Feasibility supporting lines (9 quotes: 01 line 79, 01 line 219, 01 line 217, 01 line 386, research-notes F9-4, 03 lines 178-179, 03 line 195, 02 lines 324-325, 04 line 501) | REP: 01 line 79 and 386, F9-4, 03 lines 178-180, 02 lines 324-325 at L1321-1323; 04 line 501 at L1528 and L360-366; 01 line 217 ("writes ONLY `.claude/skills/<skill>/`... nothing under `~/.claude`") and 01 line 219 ("option F ... would be an upstream feature request") OMITTED as quotes, but the substance is in L1321 and L1163 (9 rows; 2 quote-level omissions, MINOR) |
| GL-184 | Feasibility limits: 03 line 180 YES conditions; Sysbox layer gate (B2 and D2 add one layer, 68 of 70); B1/D1/E/F break test-57:450; version skew; prior-review figures not re-run | REP L1323, L1595, L1528, L645, L668 |
| GL-185 to GL-199 | Run-only facts R-1 to R-15 with research item, gap and "observe in CI" flag | REP L755-765 (R-1 to R-15 each mapped, 15 rows) and step 6.7 L1600 |
| GL-200 | Read-only items closable by reading code (UV-04, UV-18, G-20); Claude Code behaviour needs docs or a live session | REP L671, L676, L679 |
| GL-201 to GL-217 | Design questions D-1 to D-17 | REP L735-743 (D-1/D-2/D-6, D-3, D-4/D-5, D-7/D-17, D-8, D-9/D-11, D-10, D-12/D-13/D-15, D-14, D-16 all present) (17 rows) |
| GL-218 | Summary: 27 open gaps, 14 Important and 13 Minor, 0 Critical; counts of claims; 15 run-only facts | REP L753, L1713 |
| GL-219 | How-the-log-was-built: addendum backstop (no `.addendum.json` found), Gate 1 exception, severity method, web-topic assignment, `qa-verification-phase3-cycle2-*` unread | REP in part (Gate 1 exception L689, severity scale L636); the `.addendum.json` Glob and the unread cycle-2 QA files OMITTED, MINOR |

**gaps-and-questions count:** 219 findings (GL-01 to GL-219 with ranges expanded: 30 gap rows, 1 totals, 89 UV, 30 CC, 13 SD, then 56 single rows and sets). OMITTED rows: GL-165 only (GL-175 to GL-183 and GL-219 are REP with quote-level or detail-level misses, listed as MINOR notes in the Omissions table). Tally rule: a row whose main substance is present counts as REP; detail-only misses are listed as MINOR notes and are not counted as OMITTED rows.

---

## Anti-Omission Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md`
**Input files checked:** `research/03-startup-flow-home-and-user-level-claude.md` (118 findings), `research/04-pinned-tests-57-46-19.md` (155), `synthesis/synth-03-options-recommendation.md` (68), `gaps-and-questions.md` (219). Total findings enumerated: 560.
**Date:** 2026-11-08

### Omissions Found

Section 7 of the report says "Stop condition: not triggered" (line 1325) and Section 8 is a full implementation plan, so the normal rule applied. Every OMITTED row is below. Severity reasoning: no omitted finding is a pinned assertion or document that must change (all planned changes appear in steps 5.1 to 5.6 and Table 5.1), and none changes an implementer's action, so none is CRITICAL or IMPORTANT. The first three groups (A, B, C) are the most useful to add if the orchestrator wants Table 5.1 to be self-evidently complete.

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| 1 | 04-128: three `coder_script` count pins judged NO for B3/D3 (`test-5-coder-app-allowlist.sh:501-512` needs exactly one `coder_script "code_server"` in `main.tf`; `test-70-restart-stale-state.sh:42`; `test-74-orca-clean-stop.sh:63` counts `coder_script` in `catalogue/orca/module.tf` only) | 04 A.5 | OMITTED | n/a | MINOR (A) |
| 2 | 04-135: test-1-tool-floor pins (`/source/startup.sh` cmp-identical to baked `aidev-startup`; single `tool-floor-verify` start and `section:12 done` end markers; `INSTALL_MATRIX` list) which 04 classes RELEVANT-NO-BREAK | 04 A.7, A.8 row 16 | OMITTED (only the unread-fixtures gap appears, L373, L679) | n/a | MINOR (B) |
| 3 | 04-141 and 04-142: test-59-home-workspaces-dir pin (one `aidev_ws` block, `bash -n startup.sh`) and test-72-legacy-mcp-retire pin (one `( aidev_retire_legacy_mcp ) \|\| true` call line); both are "startup.sh must still parse" style pins | 04 A.7 | OMITTED as pin text (test-59 is named only as a B2 BREAKS-IF at L1236) | n/a | MINOR (C) |
| 4 | 04-143: test-b1-affordance-matrix pin (two failure strings must have zero hits in catalogue `.tf` files) | 04 A.7 | OMITTED as pin text (strings unread, G-20) | n/a | MINOR |
| 5 | 04-126: test-51 `startup_section` extraction of §7, §8 and the §8 to §9 summary span, run against stubs | 04 A.5 | OMITTED | n/a | MINOR |
| 6 | 04-127: test-51:1765 askpass COPY exact line and test-51:511-512 credential-helper RUN exact-line grep | 04 A.5 | OMITTED | n/a | MINOR |
| 7 | 04-129: test-5-coder-app-allowlist scans only `coder_app` slugs; no variant adds one | 04 A.5 | OMITTED | n/a | MINOR |
| 8 | 04-134: test-5-no-shadow (skel copy, `cat ls find grep` not shadowed) | 04 A.6 | OMITTED | n/a | MINOR |
| 9 | 04-132: test-73-codegraph-sweep judged irrelevant | 04 A.6, A.8 | OMITTED (irrelevant by 04's own verdict) | n/a | MINOR |
| 10 | 04-138: test-44 and test-47 judged irrelevant (private temp catalogues) | 04 A.7 | OMITTED (irrelevant) | n/a | MINOR |
| 11 | 04-139: test-2-starship-latency judged irrelevant | 04 A.7 | OMITTED (irrelevant) | n/a | MINOR |
| 12 | 04-014: test-57:340-342 `record_health "configured positive ${slug}" ... Configured` | 04 section 2 | OMITTED as its own row (the range `331-342` is cited only as evidence at L376) | n/a | MINOR |
| 13 | 04-037: test-46:904-908 selected bmad slug gets its marker, report has no rows | 04 section 3 | OMITTED | n/a | MINOR |
| 14 | 04-042: test-46:1167 ai-pair to orca boot has no bmad row | 04 section 3 | OMITTED | n/a | MINOR |
| 15 | 04-053: declaring `runtime-network` would remove the on-image `bmad --version` check (test-19:1161-1166) and is not recommended | 04 section 4 | OMITTED | n/a | MINOR |
| 16 | 04-060: test-19 self-tests 818-821 and 743-753/760 (parser and ECHO-VERB) | 04 section 4 | OMITTED (no repo state) | n/a | MINOR |
| 17 | 04-099: current COPY line numbers of Dockerfile.coder (185, 368-369, 453, ... 593) | 04 A.2 | OMITTED | n/a | MINOR |
| 18 | 04-107: literal `seed_if_absent` occurs only at test-60:92; the other 67 of 68 hits are `/etc/skel` paths | 04 A.4 | OMITTED | n/a | MINOR |
| 19 | 03-03: `docker_data` volume `coder-<id>-docker-data-<runtime>`, mounted only on the sysbox-runc arm (main.tf:182-184, 604-614) | 03 section 1 | OMITTED | n/a | MINOR |
| 20 | 03-04: `/etc/machine-id` uploaded per workspace, stable across `coder update` (main.tf:583-592) | 03 section 1 | OMITTED | n/a | MINOR |
| 21 | 03-05: main.tf:216-219 comment that `/etc/aidev02/aienv.d` resets on restart while the pushed release stays in the home volume | 03 section 1 | OMITTED | n/a | MINOR |
| 22 | 03-10: `coder_script.code_server` launches code-server (marked not relevant) | 03 section 1 | OMITTED | n/a | MINOR |
| 23 | 03-11: startup.tf:27-29 baked-path comment verified at Dockerfile.coder:586 | 03 stale-doc section | OMITTED | n/a | MINOR |
| 24 | 03-26: ironclaude `install.sh:42` requires `~/.claude/CLAUDE.md` (seeded by §6) or exits 2 | 03 section 3 | OMITTED | n/a | MINOR |
| 25 | 03-40, 03-41, 03-43, 03-46: settings.json top-level key list, `env` key names, hook script basenames, `~/.aidev/installed/` contents | 03 section 4 | OMITTED (four rows) | n/a | MINOR |
| 26 | 03-51: superclaude install flow order and `--force` to all but codegraph (main.py:178-263) | 03 section 5 | OMITTED (only the line range is cited, L310) | n/a | MINOR |
| 27 | 03-58: Orca skills skipped when all three SKILL.md exist, else `orca skills install` bounded by `_ORCA_TIMEOUT` 25 s | 03 section 5 | OMITTED | n/a | MINOR |
| 28 | 03-59: plugins row (`claude plugin ...`; IronClaude catalog rewritten at `~/.claude/ironclaude-marketplace/` every run) | 03 section 5 | OMITTED | n/a | MINOR |
| 29 | 03-80: web provenance note (WebFetch used because tavily unavailable; one page fetched) | 03 end of main body | OMITTED | n/a | MINOR |
| 30 | 03-88: block-bare-python.sh ceilings that are NOT blocked (`bash -c`, `eval`, `xargs python3`, `find -exec python3`, heredoc to shell, `python3.12`) | 03 A1 | OMITTED | n/a | MINOR |
| 31 | GL-165: `tools/installer/README.md` was only Grep-searched in file 01 | gaps log section 3 | OMITTED | n/a | MINOR |
| 33 | 04-052 sub-claim: `npx bmad-method install` call from E/F would flip test-19's IMAGE_BAKED classification | 04 section 4 | OMITTED (sub-claim inside a REP row; the "no unquoted install verb" rule is present) | n/a | MINOR |
| 34 | 04-098 sub-claims: test-67 rules at 65-81 (`image_inputs_sha256` includes `catalogue:${local.catalogue_sha256}`, docker_image name and triggers), 101-102 (`context = image`), 112-113 (no Terraform work file under `image/`), 114-115 (no `.dockerignore` at the template root) | 04 A.2 | OMITTED (sub-claims; the COPY-listing and hidden-entry rules are present) | n/a | MINOR |
| 35 | 04-095 sub-claim: test-3 mkdir/install line only WARNs; list of files test-3 does not scan (Dockerfile.coder, `*.tf`, manifest.yaml, skel sources, workspace_defaults, image/etc) | 04 A.2 | OMITTED (sub-claim) | n/a | MINOR |
| 36 | 04-102 sub-claim: adding a startup section needs `D07` edit with ID 13 or higher and the test-7 self-test fixtures (136-175) | 04 A.3 | OMITTED (plan adds no section) | n/a | MINOR |
| 37 | 04-075/076/077 sub-claims: per-test "needs the built image" column (test-49 static in substance, test-46 partial, test-57 not runnable on a host), test-52 other-mode call sites in `coder-ci-validate.yml:561, 591, 1028`, `orca-upstream-monitor.yml:352-353` | 04 section 8 | OMITTED (sub-claims) | n/a | MINOR |
| 38 | 04-049 sub-claim: `mp_expected` comes from profiles.yaml, so a new slug changes `mp_scanned` and `mp_expected` equally | 04 section 3 | OMITTED (plan adds no slug) | n/a | MINOR |
| 39 | 03 detail misses inside REP rows: `os.replace` atomic write (03-53), managed-key list of the defaults JSON (03-54), `specstory-cleanup.done` marker (03-61), managed-settings precedence doc sentence and Dockerfile "every user and launch path" comment (03-69), wrapper list of the hook scanner and the `uv run` exemption (03-87), "hook error versus script error" (03-89), "python3 works during the transition" and the SKILL.md error-path pointer (03-90), `bmad-create-prd` deprecation shim (03-92), "`resolve_config.py` steps have no fallback text; retrospective only grep-read" (03-117), per-file examples of the 38/2/1 breakdown (03-86) | 03 | OMITTED (detail-level, 10 items) | n/a | MINOR |
| 40 | GL-175 to GL-183 quote-level: 01 line 217 ("writes ONLY `.claude/skills/<skill>/` ... nothing under `~/.claude`") and 01 line 219 ("option F ... would be an upstream feature request"); GL-219 detail: Glob found no `research/*.addendum.json`, `qa-verification-phase3-cycle2-*` unread | gaps log sections 1, 6 | OMITTED (detail-level) | n/a | MINOR |
| 41 | 04-145/146: names and reasons of the 15 irrelevant files in the A.8 classification (test-68, test-59-home, test-77, test-72, test-b1, test-18, test-66, test-75, test-65, test-62, test-12, test-69, test-48, test-3-zellij, test-2-starship) and the "nine tests not among the 30" mapping | 04 A.8 | OMITTED (the report keeps the counts "15 relevant, 15 irrelevant" at L342 but not the names or reasons) | n/a | MINOR |
| 42 | 03-36 style dedups: 03-38, 03-74, 03-75, 03-78, 03-118 | 03 | COVERED-BY-DEDUP | 03-38 by gaps register G-21 (L1737, UV-43); 03-74 answer index by 03-14, 03-35 to 03-72; 03-75 and 03-118 by gaps enumeration (UV-37 to UV-56, UV-48 to UV-56 at L1737); 03-78 by the 04 pinned-test inventory (L342-L379) | n/a |
| 43 | 04-036, 04-092, 04-155 | 04 | COVERED-BY-DEDUP | 04-036 by L337 (synthetic bmad fixtures); 04-092 and 04-155 by L356-366 and Table 5.1 | n/a |
| 44 | S3-66, S3-68 | synth-03 | COVERED-BY-DEDUP | meta traces of findings enumerated in S3-04 to S3-65 | n/a |

Notes on the table: table rows 1 to 31 hold the 35 counted OMITTED rows (row 25 stands for four rows: 03-40, 03-41, 03-43, 03-46; row 3 stands for two rows: 04-141, 04-142; so 31 table rows = 35 findings). The row numbers jump from 31 to 33 on purpose after a placeholder row was removed. Rows 33 to 41 are detail-level or sub-claim omissions inside rows I counted as REPRESENTED (about 20 items); they are not in the 35, to avoid double counting. Rows 42 to 44 hold the 10 COVERED-BY-DEDUP rows (row 42 stands for 03-38, 03-74, 03-75, 03-78, 03-118; row 43 for 04-036, 04-092, 04-155; row 44 for S3-66, S3-68).

### Judgment calls for the orchestrator

- Rows 1 and 2 are the closest to a real gap. Both are tests that file 04 itself analysed in connection with the planned branches (a root `coder_script` for B3/D3; `startup.sh`/`Dockerfile.coder` for C), and both have verdict NO or BREAKS-IF with no plan change. Table 5.1 says it lists "every pinned assertion that the plan touches or must not break", so adding two rows (KEEP; IF 4B/4D for the `coder_script` count pins; KEEP for test-1-tool-floor) would make that claim literally true. I rated them MINOR because no step, rating or recommendation changes if they stay out.
- No CRITICAL omission exists: the report's Table 5.1 and steps 5.1 to 5.6 carry every assertion that must change (test-57:10 comment, the new test-52 pin, the optional test-startup-boot:232 kind, the test-73 second-file check, the 4D merge fixtures, and the stale `test-57:386` comment).

### Self-Audit

**What I read (all by Read, with line ranges):**
- `research/03-startup-flow-home-and-user-level-claude.md`: lines 1-365 (all).
- `research/04-pinned-tests-57-46-19.md`: lines 1-541 (all).
- `synthesis/synth-03-options-recommendation.md`: lines 1-401 (all).
- `gaps-and-questions.md`: lines 1-321 (all).
- Report `RESEARCH-REPORT-bmad-first-use.md` (1795 lines): read in full at lines 232-313 (Section 2.3), 314-382 (2.4), 634-766 (Sections 4.1-4.5), 1005-1038 (6.0 facts and option list), 1219-1275 (Options Comparison), 1276-1355 (Sections 7 and start of 8), 1523-1602 (Phases 5 and 6), 1711-1746 (Section 9.1 register). Heading list from Grep (line 1-1795). The remaining report ranges (Sections 1, 2.1, 2.2, 2.5, 2.6, 3, 5, the option write-ups 1040-1218, Phases 1-4 and 7, Section 10) were checked only through targeted Grep with line numbers, not read end to end. UNVERIFIED: any substance in those unread ranges that a Grep token did not hit.

**Greps I ran against the report (pattern groups):** volume and boot-wiring tokens; slug-order and watchdog tokens; superclaude merge tokens (`os.replace`, `malformed`, `_ORCA_TIMEOUT`, `ironclaude-marketplace`, `rmtree`, `wire_ccsession`); hook-scanner tokens (`bash -c`, `xargs`, `python3.12`, `uv run`); test-name tokens for all 30 matched tests and the nine named ones (`test-5-coder-app-allowlist`, `test-70`, `test-74-orca`, `test-1-tool-floor`, `test-59-home`, `test-72`, `test-b1-affordance`, `test-4-pane-title` and others); `dockerignore`, `heredoc`, `askpass`, `credential`, `startup_section`, `D07`, `runtime-network`, `mp_expected`, `catalogue-src`; synthesis tokens (`#2624`, `#1852`, `#2313`, `#2677`, `bmad-cli.js:31`, `validateDirectorySync`, `S16c`, `S18`, `133-135`); `PROJECT_INDEX`, `.dev/issues/478`, `qa-gate1-decision`.

**Why I believe the omission count is right:**
- File 03 and file 04 are covered in the report by two dense sections (2.3 and 2.4) and by Phase 5 Table 5.1. I compared each enumerated row to those and to Grep hits. The misses cluster in two kinds: low-value environment detail from 03 (volumes, machine-id, settings key lists) and "does not break" verdicts for tests the plan does not touch (04 A.5 to A.8). That pattern matches how the report was built (plan-relevant pins kept, no-break pins dropped).
- synth-03: the report's Sections 6 and 7 reproduce it block by block (I compared the 14 common facts, all 9 option write-ups, both comparison tables, the 6 contradictions, stage table, rationale, limits and dependence table); the differences are plan-driven updates.
- gaps-and-questions: all 30 G rows, 89 UV ids (79 open in register rows, 10 named as closed), 30 CC ids, 13 SD ids, D-1 to D-17 and R-1 to R-15 are present; I checked ids one by one against lines 1717-1745 and 695-722.
- I could have under-counted omissions that sit in the report ranges I did not read end to end, and over-counted where the report phrased a finding without the token I searched. I treated every Grep miss as a candidate and then looked for a semantic equivalent before listing it; the listed rows had none in the ranges I read.
- Not run: no test, no product-code read (the product files cited by the inputs were not re-read; the inputs' file:line citations are as the inputs state them).

### Summary

- Findings enumerated: 560 (03: 118; 04: 155; synth-03: 68; gaps-and-questions: 219).
- Represented: 515.
- Covered-by-dedup: 10.
- Omitted: 35 (03: 15; 04: 19; synth-03: 0; gaps-and-questions: 1), all MINOR. About 20 further detail-level or sub-claim misses sit inside represented rows (table rows 33 to 41) and are not counted.
- CRITICAL: 0. IMPORTANT: 0. MINOR: 35.

Verdict: PASS (0 blocking omissions; 35 MINOR omissions listed as notes; table rows 1 and 2 are recommended additions to Table 5.1).

**Status:** Complete
