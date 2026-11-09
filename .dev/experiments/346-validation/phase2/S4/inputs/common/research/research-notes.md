# Research Notes: BMAD first-use directory creation in a project that never had BMAD (issue 478, BMAD half only)

**Date:** 2026-11-07
**Scenario:** A (explicit request: goal, files and output type all given by the coordinator brief)
**Depth Tier:** Standard (single subsystem: the `bmad` catalogue slug plus its image CLI, startup flow, tests and docs; 5-20 files; qa_intensity = standard)
**Status:** Complete

---

## EXISTING_FILES

Paths are relative to the worktree root `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global` unless absolute. Everything below was seen by direct Read/Grep in scope discovery.

### The user's ask and the prior diagnosis
| Path | Purpose | Notes |
|------|---------|-------|
| `.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/REPORT.md` (141 lines) | Prior diagnosis, status partial | BMAD half = open owner decision (now decided); Ponytail half = evidence E-1..E-3 pending. Report says bmad user-scope skill install UNVERIFIED |
| `.dev/issues/478/` (12 files: issue-body.md, accuracy-check.md, next-steps.md, ...) | Issue working files | Live issue #478 is OPEN; comments = accuracy check + claim |
| `_bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md:5` | OD-1 "Cancelled. BMad is installed per project only, never globally." | To be superseded for first-use creation only |
| `_bmad-output/specs/spec-orca-bundle-gap-closure/.memlog.md:32-33` | Owner 2026-09-25: BMad "never globally or at user level" | Note the words "or at user level": relevant to a user-level stub option |
| `_bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md:77` | Non-goal: any BMad change | |
| `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md:141,174` | Non-goal / scope expansion text for BMad in later clones and Orca worktrees | |

### The BMAD slug and image CLI (this repo)
| Path | Purpose | Notes |
|------|---------|-------|
| `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh` (62 lines) | Slug installer: CLI check, seed-repo-only `bmad install`, marker | :18 CLI check; :21-25 seed-repo and existing-BMad guards; :42 only `bmad install` call; :58-60 marker written even with no seed |
| `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml` (30 lines) | Slug manifest and welcome text | :8-18 welcome message names the one-command manual install for other repos |
| `templates/VSCode-AIDev02/image/catalogue/bmad/module.tf` | Terraform module for the slug | not yet read |
| `templates/VSCode-AIDev02/image/catalogue/profiles.yaml` | Profiles | :18 Default includes bmad; :21 Minimal = claude-code only |
| `templates/VSCode-AIDev02/image/catalogue/README.md` | Catalogue contract docs | mentions bmad; not yet read |
| `templates/VSCode-AIDev02/image/Dockerfile.coder:133-144` | Image-wide `bmad-method@6.9.0` and `/usr/local/bin/bmad` wrapper (execs node on `.../bmad-method/tools/installer/bmad-cli.js`) | Verified on this workspace: wrapper present, `bmad --version` = 6.9.0 |
| `templates/VSCode-AIDev02/image/scripts/startup.sh` (1863 lines) | Boot: §8 seed repo (:669-681 writes seed-repo-path), §9 catalogue install (:1113-1176; bmad invoked at :1174 as `( source ~/.aienv && bash .../install.sh )`) | Only :1100-1240 and :660-700 matter here |
| `templates/VSCode-AIDev02/image/scripts/lib/spec2-health.sh` | Health record writer; reports `Installed-not-Configured` vs `Configured` for bmad | not yet read |
| `templates/VSCode-AIDev02/modules.tf`, `parameters.tf` | Terraform wiring; mention bmad | not yet read |
| `templates/VSCode-AIDev02/README.md` (610 lines) | Developer docs; BMad in Default profile list near :241 | to be reconciled |

### BMAD 6.9.0 itself (outside the repo, read-only evidence)
Root: `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/`
| Path | Purpose | Notes |
|------|---------|-------|
| `tools/installer/ide/platform-codes.yaml` | Per-tool `target_dir` and optional `global_target_dir` | claude-code: target_dir `.claude/skills`, global_target_dir `~/.claude/skills` (:52-57). Header :9 documents global_target_dir as "User-home directory for global install" |
| `tools/installer/ide/_config-driven.js` | Per-platform installer; reads `target_dir` (:230,246-247), ancestor conflict check (:190-205, :937-960) | Grep found NO reader of `global_target_dir` in any .js under `tools/` (scope discovery) |
| `tools/installer/commands/install.js`, `core/installer.js`, `core/install-paths.js`, `ui.js` | Install command and flow | Option list from `bmad install --help` (no scope/global flag: --directory, --modules, --tools, --yes, --output-folder, --user-name, --action, --set ...) |
| `src/scripts/resolve_config.py`, `resolve_customization.py` | Runtime config resolvers used by skills | resolve_config.py requires `--project-root` containing `_bmad/` (:144-154); resolve_customization.py `find_project_root` walks up to the first dir with `_bmad` or `.git` (:58-61, :215) |
| `.claude/skills/bmad-help/SKILL.md:25-26` (in this worktree) | Example installed skill | reads `{project-root}/_bmad/_config/bmad-help.csv` and runs `{project-root}/_bmad/scripts/resolve_config.py` |
| `~/.bmad/cache/` | External-module cache (home-level) | exists as a cache path only (project-root.js:80,162,191) |

### Tests that pin current behaviour
| Path | Lines | Notes |
|------|-------|-------|
| `.github/contract-tests/test-57-catalogue-configure.sh` | 1132 | :449-452 "no seed: bmad writes nothing" (whole-HOME snapshot compare, `snap "${H}"`) and "marker still exists" and `Installed-not-Configured`; :413-465 seed guards; :323-345 seeded configure |
| `.github/contract-tests/test-startup-boot.sh` | 3061 | 35 case-insensitive "bmad" hits; not yet read in detail |
| `.github/contract-tests/test-46-catalogue-health.sh` | 1953 | 38 hits; health states |
| `.github/contract-tests/test-19-catalogue-cli-presence.sh` | 1262 | 5 hits; CLI presence |
| `.github/contract-tests/test-49-spec2-evidence.sh`, `test-52-browser-usability-evidence.sh` | | 1 hit each |

### Workspace facts observed (this dispatched workspace)
| Fact | Evidence |
|------|----------|
| `~/.claude/skills/` exists and holds user-level skills (ccsession-tag, orchestration, orca-cli ...) | `ls /home/coder/.claude/skills` |
| No `bmad-*` entry under `~/.claude/skills/` | `ls ... | grep -i bmad` printed nothing |
| This worktree already has `_bmad/` and `_bmad-output/` (a project where BMAD was installed) | `ls -d` |

## PATTERNS_AND_CONVENTIONS

- Catalogue slug pattern: each slug has `manifest.yaml` + `install.sh` run by startup in a subshell; the installer writes `~/.aidev/installed/<slug>` only after verification (bmad install.sh:57-60) and logs to `/tmp/catalogue-<slug>.log`.
- BMad is the one slug with an owner-decision exception: it keeps its original per-project invocation and a deselected BMad slug's marker is never removed (startup.sh:1113-1117, :1170-1176).
- BMAD install is offline and git-clean by design: `NPM_CONFIG_OFFLINE=true`, 120 s timeout, `info/exclude` patterns `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/`, and a before/after `git status` comparison (install.sh:27-53).
- `# ponytail:` comment tags in shell are code comments only, not the Ponytail plugin.
- Tests are shell contract tests under `.github/contract-tests/`, run by GitHub Actions (CLAUDE.md: no one-off validation scripts).
- Dependency note: BMAD skills resolve their config from the project's own `_bmad/` (resolve_config.py requires it); a skill file alone does not make BMAD usable.
- Only the documented user-level skill location `~/.claude/skills/` is used by other tooling in this workspace (orchestration, orca-cli ...): HOME persistence across boots needs confirming in startup.sh.

## SOLUTION_RESEARCH

Candidate mechanisms to evaluate (none chosen yet; the synthesis must compare at least these):

| Option | Idea | Touches | Initial concern |
|--------|------|---------|-----------------|
| A | Document only: keep the one-command manual install and say so in README | README only | Does not satisfy the new requirement (no creation on first use) |
| B | User-level bootstrap skill/command under `~/.claude/skills/` (written by the bmad slug's install.sh from image-baked content) that, when invoked in a project without `_bmad/`, runs the pinned offline `bmad install` for that project root | catalogue/bmad install.sh + a baked skill file, test-57, health, README | "At user level" wording in OD-1/.memlog; also touches whole-HOME snapshot oracle; must not contain BMAD itself |
| C | Image-level CLI wrapper change: `/usr/local/bin/bmad` (or a new `bmad-here`) that runs the install for the current project when `_bmad/` is absent | Dockerfile.coder wrapper, test-19 | Needs the user to run a command; does a CLI count as "BMAD used"? Wrapper change = image rebuild |
| D | Claude Code user-level SessionStart/UserPromptSubmit hook that installs BMAD into every project lacking it | `~/.claude/settings.json` | Is "install everywhere", not "first use"; clobber risk with `superclaude install`; project skills created mid-session may not load until restart (UNVERIFIED) |
| E | `bmad install --directory ~` (home-level install) | none in repo | This IS a global install (not requested); ancestor-conflict check and `find_project_root` side effects |
| F | Upstream BMAD user-scope install (`global_target_dir`) | none | Appears to have no consumer in 6.9.0 installer code (to be confirmed by research agent 01); would need a newer BMAD pin |

External facts needed: does Claude Code load project skills created after session start; how user-level skills/hooks are discovered; what upstream BMAD (newer than 6.9.0) says about global/user-scope install.

## RECOMMENDED_OUTPUTS

| Output | Path |
|--------|------|
| Research files (codebase) | `research/01-bmad-6-9-0-installer-and-skill-runtime.md`, `research/02-image-cli-and-catalogue-slug.md`, `research/03-startup-flow-home-and-user-level-claude.md`, `research/04-pinned-tests-57-46-19.md`, `research/05-startup-boot-test-docs-and-decision-trail.md` |
| Research files (web) | `research/web-01-claude-code-user-skills-hooks-and-live-reload.md`, `research/web-02-bmad-upstream-user-scope-and-new-project-install.md` |
| Synthesis | `synthesis/synth-01-problem-current-state.md` (S1-S2), `synth-02-target-gaps-external.md` (S3-S5), `synth-03-options-recommendation.md` (S6-S7), `synth-04-plan-questions-evidence.md` (S8-S10) |
| Final report | `RESEARCH-REPORT-bmad-first-use.md` |
| Gaps log | `gaps-and-questions.md` |
| Spec (separate step, by the orchestrator after research) | `.dev/issues/478/spec.md` |

## SUGGESTED_PHASES

### Phase 2 research agents (Standard tier: 5 codebase agents, parallel)
| # | Type | Topic | Files / directories | Output |
|---|------|-------|---------------------|--------|
| 01 | Code Tracer | BMAD 6.9.0 installer behaviour and skill runtime needs: what `bmad install --directory X` creates in a never-installed dir (which dirs, `_bmad-output`), non-interactive flags, runtime, offline behaviour, `global_target_dir` consumers (confirm none), ancestor conflict check, what an installed skill needs at run time and what happens when `_bmad/` is absent | `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/{tools/installer,src/scripts,src/core-skills}`, `package.json` | `research/01-...` |
| 02 | Integration Mapper | Image CLI and catalogue slug: Dockerfile wrapper, bmad install.sh/manifest.yaml/module.tf, profiles.yaml, catalogue README, modules.tf, parameters.tf, spec2-health.sh bmad handling; where a first-use mechanism could hook in | `templates/VSCode-AIDev02/image/{Dockerfile.coder,catalogue,scripts/lib/spec2-health.sh}`, `modules.tf`, `parameters.tf` | `research/02-...` |
| 03 | Architecture Analyst | Startup flow, HOME persistence and user-level Claude Code surfaces: startup.sh §8/§9 (:600-700, :1100-1240), what runs per boot, what persists in HOME, who writes `~/.claude/settings.json` and `~/.claude/skills/` (and whether `superclaude install` would clobber a user-level hook or skill), where a user-level skill could be written. Read the superclaude package only as read-only evidence; flag anything that would need an IronClaude change | `startup.sh`, `/home/coder/.claude/`, `/opt/uv/tools/superclaude/.../superclaude/cli/install_user_setup.py` and `user_settings_defaults.json` (read-only), `catalogue/ironclaude/install.sh` | `research/03-...` |
| 04 | Code Tracer | Pinned tests part 1: test-57 (bmad blocks :173, :323-345, :413-465), test-46, test-19, test-49/52: list every assertion that pins "no seed: bmad writes nothing", marker, health state, CLI presence; for each candidate option say which assertions break and what the new assertion would be | `.github/contract-tests/test-57-*.sh`, `test-46-*.sh`, `test-19-*.sh`, `test-49-*.sh`, `test-52-*.sh` | `research/04-...` |
| 05 | Doc Analyst | Pinned tests part 2 plus docs and decision trail: test-startup-boot.sh bmad cases; README.md (:241, :308), catalogue/README.md; every document that states the per-project-only rule or non-goals (OD-1, .memlog, gap-closure SPEC, catalogue-bundle SPEC :141,:174) and how each must change to record the new decision; cross-validate doc claims against code | `.github/contract-tests/test-startup-boot.sh`, `templates/VSCode-AIDev02/README.md`, `catalogue/README.md`, `_bmad-output/specs/spec-orca-*/`, `docs/` | `research/05-...` |

### Phase 4 web research (parallel)
| # | Topic | Output |
|---|-------|--------|
| web-01 | Claude Code: user-level skills (`~/.claude/skills/`), skill discovery timing (are skills created after session start loaded live?), SessionStart/UserPromptSubmit hooks, `${CLAUDE_PROJECT_DIR}`; official docs only | `research/web-01-...` |
| web-02 | BMAD-METHOD upstream: global/user-scope install (`global_target_dir`) support in later releases, documented new-project install flow, any "bootstrap on first use" pattern, behaviour of `npx bmad-method install` in an empty project | `research/web-02-...` |

### Synthesis mapping
| Synth file | Report sections | Research inputs |
|-----------|-----------------|-----------------|
| synth-01-problem-current-state | 1 Problem Statement, 2 Current State Analysis | research 01-05, gaps log |
| synth-02-target-gaps-external | 3 Target State, 4 Gap Analysis, 5 External Research Findings | research 01-05, web-01, web-02, gaps log |
| synth-03-options-recommendation | 6 Options Analysis, 7 Recommendation | all research, web |
| synth-04-plan-questions-evidence | 8 Implementation Plan (names the pinned tests and docs that must change), 9 Open Questions, 10 Evidence Trail | all research, web, gaps |

## TEMPLATE_NOTES

Template 02 (complex task): discovery, parallel agents, synthesis, multi-gate QA. QA_INTENSITY = standard (Standard tier default).

Scope guard for every agent (from the coordinator brief, binding): research and read only; NO product-code edits; no commit, push, PR, GitHub comment or merge; do not touch other repos (IronClaude, IronOrca); read `/opt/uv/tools/superclaude/...` and `/opt/nvm/...` read-only; no env captures to tracked paths; no `cd`; UV only; no one-off validation scripts. Mark anything unobserved as UNVERIFIED. Ponytail: the user confirmed on 2026-11-07 that it already installs and works; there is NO Ponytail work, do not research or mention it beyond this line.

Feasibility stop-condition (from the brief): if the evidence shows the ask cannot be met without a global BMAD install or a change in another repo (IronClaude, IronOrca), the report must say so explicitly in Recommendation and Open Questions so the orchestrator can STOP and re-scope.

## AMBIGUITIES_FOR_USER

1. Does the new decision allow a user-level bootstrap artifact (a tiny stub skill or command under `~/.claude/` that contains no BMAD content and only starts the per-project install)? The 2026-09-25 owner text says BMad is never installed "globally or at user level"; the 2026-11-07 decision says global installation of BMAD itself is not requested. Whether a stub counts as "user level" is an owner reading, not a code fact. Carry into Open Questions; do not guess.
2. What counts as "first use"? Running a `bmad` CLI command, invoking a BMAD slash skill, or opening a session in a project. Carry into Open Questions with the mechanism each reading implies.

Doc-sourced claims in these notes: all file contents above were read directly in scope discovery, so they are [CODE-VERIFIED] except where marked "not yet read" (UNVERIFIED until Phase 2 agents read them). Statements about `global_target_dir` having no consumer rest on one Grep over `tools/` and are to be re-confirmed by agent 01.

## Addendum (fix cycle 1): Finding 9 - prior diagnosis REPORT.md and .dev/issues/478 files never read, and where the 2026-11-07 decision supersedes them
**Status:** Complete
**Date:** 2026-11-08

Scope: read-only. Paths relative to `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global`. Tags: [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED].

### F9-1. What the 2026-11-07 decision is (read from BUILD-REQUEST.md and research file 05 part b1)

- `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/BUILD-REQUEST.md:14` (WHY): "On 2026-11-07 the user decided (AskUserQuestion) that BMAD SHOULD create its needed directories on first use in a project that never had it. This supersedes, for first-use creation only, the 2026-09-25 owner decision OD-1 and related non-goals (_bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md:77, owner-decisions.md:5, .memlog.md:32-33, spec-orca-catalogue-bundle/SPEC.md:141,174). Global installation of BMAD is NOT requested."
- `BUILD-REQUEST.md:12` (GOAL) restates the constraints: "WITHOUT a global BMAD install and without reversing the unrelated 2026-09-25 owner decision OD-1 (BMad is installed per project)"; `:14` also says "there is NO Ponytail work, do not research it".
- Research file 05 part b1 (`research/05-startup-boot-test-docs-and-decision-trail.md:67-85`) tags OD-1 (`owner-decisions.md:5`) and `.memlog.md:32` and states how each must change: keep OD-1, add OD-4 for first-use creation, append a `(decision) Owner 2026-11-07` bullet after `.memlog.md:34`, narrow `SPEC.md:77` (05 lines 71-72, 78). 05 line 65 adds the nuance that the `bmad` CLI is already global (`Dockerfile.coder:139`) and only the framework content is per project.
- Summary of the decision, so it can be applied to each prior position: (i) CHANGED: BMAD directories (`_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*`) get created on first use in a project that lacks them; (ii) UNCHANGED: no global or user-level install of BMAD framework content, no reversal of the rest of OD-1, boot-time seed install untouched (05 line 73 `.memlog.md:33`).
- [CODE-VERIFIED] The decision is NOT yet recorded in any spec document: Grep of `_bmad-output/specs` for `2026-11-07|OD-4|first use|first-use` returned only an unrelated hit (`spec-aidev02-v2/SPEC.md:50`, auth-on-first-use for MCP). So `BUILD-REQUEST.md:14` is currently the only repo copy of the decision text. [UNVERIFIED] The AskUserQuestion transcript itself is not in the repo, so the exact wording (for example whether the user accepts visible or hidden new files, or what "first use" means) is unknown; this matches 05 U17 (line 258) and the research-notes AMBIGUITIES 1 and 2 (lines 136-137 of this file).

### F9-2. The 12 files under `.dev/issues/478/` (Glob listed exactly these 12; all read in full this cycle)

Directory status: untracked in git at session start (`?? .dev/issues/478/` in the git status snapshot). No `spec.md` exists yet (BUILD-REQUEST.md:13 says the orchestrator writes it after this research); `claim-comment.md:19` links `.dev/issues/478/analysis/`, but that directory does not exist (Glob: "Directory does not exist") [CODE-CONTRADICTED: dangling link in a draft GitHub comment; harmless for this research but do not cite `analysis/`].

| # | File | Lines | One-line relevance |
|---|------|-------|--------------------|
| 1 | `description.md` | 7 | The reporter's ask as given to /sc:issue (`:5`): "BMAD, if accessed on a project where it has never been used or installed, should create the necessary directories on that project to function, if they do not exist already" = the first-use requirement now decided; the "not available globally" half is what the 2026-11-07 decision declines. |
| 2 | `issue-body.md` | 53 | Filed issue text; Expected Behavior `:16` bundles "available globally ... by default" with the first-use creation; `:37` and `:41` record that only the CLI is global and that "Automatic first-use initialization in other projects is unverified". |
| 3 | `accuracy-check.md` | 27 | Verdict "current" at `origin/main` f1ac0c93 (`:3,5`); `:16` row 6 (no code outside `install.sh:42` runs `bmad install`) is the only line cited by research (05 line 156). Rows 1-5 re-verified below. |
| 4 | `issue-summary.md` | 37 | Cheatsheet of relevant files (`:16-32`); `:18` "Only the CLI is global"; `:21` seed-repo-only writes hidden via `info/exclude`; `:32` extra repos cloned by hand after boot are never visited by the installer = the gap first-use creation closes. |
| 5 | `scout.md` | 37 | Claim-mode lookup: issue #478 `url` and `State: OPEN` (`:10-13`), created `2026-11-07T07:23:55Z` (`:17`), no merged PRs or default-branch commits since creation (`:19-31`). Answers research 05 U13 ("GitHub issue was not opened") at the level of the recorded lookup. |
| 6 | `scout-create.md` | 37 | Create-mode lookup: repo labels and possible duplicates #204, #432, #264, #202, #238, #216 (`:30-37`); #204/#202/#216 are the earlier Orca bundle work that produced OD-1; none is a confirmed duplicate. |
| 7 | `flags.md` | 10 | Depth quick, mode bug, type install, complexity simple (`:4-10`); superseded by the claim-stage rating complex in `scout.md:36` and `issue-summary.md:5`; no bearing on the options. |
| 8 | `draft-notes.md` | 20 | Draft-time facts and the one recorded "contradiction" (`:20`): the image DOES install the CLI globally (`Dockerfile.coder:133-144`), so "BMAD is not installed globally" is only true of project content. Same nuance as 05 line 65. |
| 9 | `recommend.md` | 33 | /sc:recommend output (recorded `:3`): the route `/sc:troubleshoot ... --fix` then, if supported, `/sc:workflow` then `/sc:implement` (`:17-20`); `:23` records that MDTM (`--depth deep --fix`, `/task`) was NOT selected because neither explicit request nor machinery need existed. Context for how this research was commissioned. |
| 10 | `next-steps.md` | 13 | The same three-step chain for the user (`:7-10`), effort estimate 20 hours (`:12`), and `:13` the MDTM-not-used note. The `/sc:troubleshoot` step 1 is what produced REPORT.md. |
| 11 | `claim-comment.md` | 23 | Draft claim comment: ClickUp skipped (`:3`, no_token), summary repeating "project setup runs only for the recorded seed repo" (`:8`), dangling `analysis/` link (`:19`). |
| 12 | `clickup.json` | 1 | `{"status": "skipped", "reason": "no_token"}` (`:1`); no relevance. |

Code cross-validation of the claims these files make (all [CODE-VERIFIED] this cycle by Read):
- `Dockerfile.coder:133-144` image-wide CLI: [CODE-VERIFIED] `:139` `npm install -g bmad-method@6.9.0`; `:142-143` writes the `/usr/local/bin/bmad` wrapper (`exec "$node_bin" "$cli" "$@"`), `:144` chown of `$NVM_DIR`. Matches accuracy-check.md row 1.
- `catalogue/bmad/install.sh` (61 lines, not 62 as the EXISTING_FILES table at line 27 says [CODE-CONTRADICTED, trivial]): `:18` CLI check; `:21-23` seed-path read and "no seed repo recorded; nothing to configure"; `:24-25` existing-BMad guard; `:27-34` three `info/exclude` patterns; `:38`/`:48-53` git-status before/after check; `:42` the only `bmad install` call (`NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output --user-name ...`); `:46` manifest check; `:58-60` marker written even with no seed. Matches accuracy-check.md rows 3-4 and 6.
- `catalogue/bmad/manifest.yaml:12-14` welcome text names the one-command manual path (`bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output`); `:3` `scope: hybrid`; `:2` version 6.9.0. Matches accuracy-check.md row 5.
- `startup.sh:1113-1118` [CODE-VERIFIED]: a resolved profile deselecting a slug removes its markers except `bmad` (`:1117` `!= bmad`). `startup.sh:1163-1176` [CODE-VERIFIED]: unresolved profile skip (`:1163-1165`), out-of-profile skip (`:1166-1169`), and `bmad` alone runs as `( source "${HOME}/.aienv" && bash "${aidev_cat_dir}/${aidev_cat_script}" )` (`:1174-1176`). `profiles.yaml:14-21` [CODE-VERIFIED]: `orca` labelled "Default" with `[claude-code, orca, ironclaude, bmad, mcp-bundle-core]` (`:16-18`); `minimal` = `[claude-code]` (`:19-21`). Matches accuracy-check.md rows 2-3.

### F9-3. REPORT.md position by position: where the 2026-11-07 decision supersedes it and where it does not

Source: `.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/REPORT.md` (141 lines, read in full; written 2026-11-07T07:54:30Z per `:13`, status partial `:7`, confidence 0.58 `:6`). Rule applied: the decision (F9-1) changes ONLY first-use creation of BMAD's project directories; it leaves global and user-level installation of BMAD framework content declined and leaves boot-time seed behaviour as built.

| # | REPORT.md position (line) | Decision effect | Tag and reason |
|---|---|---|---|
| R1 | "Behavior is documented: true (BMAD half only)" `:10`; "The reported issue is the documented behavior: a code change would regress the documented contract" `:19` | SUPERSEDED for first-use creation; STILL TRUE for boot and for global. | The documents it relies on (`SPEC.md:77`, `owner-decisions.md:5`, `.memlog.md:32`, catalogue-bundle `SPEC.md:141`) are unchanged in the repo today (Grep, F9-1), so as a statement about the documents it is [CODE-VERIFIED]; as a statement about what the owner wants it is out of date since `BUILD-REQUEST.md:14`. The synthesis must not cite `:10`/`:19` as a reason to avoid a code change. |
| R2 | "first-use creation of BMAD's directories inside a project has no owner ruling ... so only the owner can change it" `:19`; "open owner decision" `:127` | SUPERSEDED: the owner has ruled (BUILD-REQUEST.md:14). | [UNVERIFIED] wording of the ruling (F9-1). The ruling is not yet in `owner-decisions.md` or `.memlog.md`; 05 b1 gives the recording steps (OD-4, `.memlog.md` bullet after :34). |
| R3 | Owner decided 2026-09-25 "BMAD is installed per project only, never globally or at user level" `:19`; evidence 4-5 `:64-65` | NOT SUPERSEDED for the global/user-level part; narrowed for the rest. | [CODE-VERIFIED] verbatim at `owner-decisions.md:5` ("installed per project only, never globally") and `.memlog.md:32` ("never globally or at user level"). Decision text: "Global installation of BMAD is NOT requested" (`BUILD-REQUEST.md:14`). Whether a content-free user-level bootstrap stub counts as "user level" is NOT decided (research-notes AMBIGUITIES 1, line 136). |
| R4 | Evidence 6-7: gap-closure `SPEC.md:77` non-goal "Any BMad change"; catalogue-bundle `SPEC.md:174` Orca worktrees non-goal `:64-67` | `SPEC.md:77`: SUPERSEDED for first-use creation (named in the decision, BUILD-REQUEST.md:14); seed-install part stays. `SPEC.md:174` (Orca worktrees): NOT answered by the decision. | [CODE-VERIFIED] `SPEC.md:77` text at `_bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md:77`; `:174` as quoted in 05 b2 (line 96). The decision speaks of projects, not Orca worktrees; leave open (05 line 96). |
| R5 | Catalogue-bundle `SPEC.md:141` is listed at `:19`/`:83` as a non-goal "BMad in later clones and Orca worktrees" | SUPERSEDED for "repos cloned after boot" (first-use creation covers them); NOT for Orca-created worktrees. | [CODE-VERIFIED] `SPEC.md:141` read this cycle: "BMad in repos cloned after boot and in Orca-created worktrees. ... Users run the one-command path instead." 05 line 93 gives the narrowing. |
| R6 | "Restrictions honored: no user-global BMAD, no BMAD change, offline install, git-clean install, profile gating. Restrictions overridden: None." `:25-26` | "no BMAD change" is SUPERSEDED for first-use creation; "Restrictions overridden: None" is no longer correct (the decision overrides SPEC.md:77 and part of :141). | Still binding (keep as constraints on any option): no global/user-level BMAD framework content; offline install (`install.sh:42` `NPM_CONFIG_OFFLINE=true`); profile gating (`startup.sh:1166-1169`). Git-clean: owner wording [UNVERIFIED] (05 U17, line 258); `install.sh:27-34,48-53` is how the seed does it. |
| R7 | Evidence 1-3 and 14 (`:61-63,:74`): `install.sh:23`, `:42`, `manifest.yaml:12-14`, `Dockerfile.coder:139` describe the current mechanism | NOT SUPERSEDED: they describe the boot-time seed install, which stays. | [CODE-VERIFIED] all four this cycle (see F9-2). The `:42` call is still the only `bmad install` call site (accuracy-check.md row 6; Glob/Grep by 05 line 156). A first-use mechanism will be a second call site. |
| R8 | Proposed Fix 1 `:83`: post diagnosis on #478, treat first-use as "an open owner decision"; "any decision superseding them should cite gap-closure SPEC.md:77 and `.memlog.md:32-33`" | The "open owner decision" is SUPERSEDED; the citation advice is ADOPTED (BUILD-REQUEST.md:14 cites exactly `SPEC.md:77`, `owner-decisions.md:5`, `.memlog.md:32-33` and catalogue-bundle `SPEC.md:141,174`). | [CODE-VERIFIED] BUILD-REQUEST.md:14 list matches REPORT.md:83. |
| R9 | Proposed Fix 2 `:84` and "Files to change" `:86-87`: README-only (`templates/VSCode-AIDev02/README.md` BMAD-scope note and line 241), "after the owner decision only" | The precondition is met; the "documentation only" scope is SUPERSEDED because the decision requires behaviour, not prose (research-notes Option A "Does not satisfy the new requirement", line 81). | The README work (`:241` reconcile, name the manual command because the build context is invisible to workspace users) remains needed as the documentation half. "Make no Ponytail delivery claim" `:84` stands (BUILD-REQUEST.md:14: no Ponytail work). |
| R10 | "Files that MUST NOT change": `catalogue/bmad/install.sh` and `manifest.yaml` "changing BMAD toward global or any-repo setup reverses ... OD-1" `:89-91` | SUPERSEDED in part: "any-repo setup" at first use is now wanted, so these files MAY change if the chosen option needs it (manifest.yaml:12-14 welcome text names the manual path and would be stale; install.sh would change only if the mechanism is built there). "Global" setup stays forbidden. | [CODE-VERIFIED] manifest.yaml:12-14 and install.sh:21-25 as read. Whether a given option touches them is for the option analysis (02 and 04), not a prohibition. |
| R11 | "Files that MUST NOT change": `test-57-catalogue-configure.sh` and `test-startup-boot.sh` "their oracles pin 'no seed: bmad writes nothing' and `Installed-not-Configured`" `:91` | test-57: oracle remains correct for BOOT with no seed and is violated only by an option that writes into HOME (or anywhere) during that boot-time run; so it is "must not break unless the option deliberately changes boot", not "must not change". test-startup-boot: claim partly [CODE-CONTRADICTED]. | [CODE-VERIFIED] test-57 `:446-452`: `mk_home no-seed`, `want="$(snap "${H}")"`, `ck "no seed: bmad writes nothing" ... = "${want}"`, marker still exists, `Installed-not-Configured`. [CODE-CONTRADICTED] test-startup-boot has no "writes nothing" assertion: only `:2209-2211` sets `expected_config=Installed-not-Configured` when `slug = bmad` and no seed, and `:2223-2224` passes "BMad has no seed; installed but not configured"; research 05 line 33 confirms "no BMAD install, directory or CLI-run case". |
| R12 | Alternative Fix: a user-level `bmad-init` skill is "the DANGEROUS wrong answer ... would silently reverse OD-1 and the related non-goals ... and break the 'writes nothing' oracles; it is conditional on an owner decision and its user-level shell behaviour is UNVERIFIED" `:100` | The "silently reverse OD-1 and the non-goals" and "conditional on an owner decision" reasons are SUPERSEDED for first-use creation: the decision is explicit, not silent. NOT superseded: (a) the "user level" wording question (R3); (b) the oracle collision if the slug writes the stub at boot; (c) UNVERIFIED shell behaviour. | (b) [CODE-VERIFIED] mechanism: test-57 `:448-450` compares `snap "${H}"` of the whole HOME before and after a no-seed run, so any new file written by `install.sh` under `$HOME` in that run would fail it (same point as research-notes Option B, line 82). (a) and (c): [UNVERIFIED] here; (c) belongs to research 03 and the not-yet-written web-01. The label "DANGEROUS" should not be carried into the synthesis; present Option B on its merits. |
| R13 | Grounding gap `:120`: "Whether bmad 6.9.0 can install skills at user scope is UNVERIFIED: `platform-codes.yaml` declares a `global_target_dir` for Claude Code but no consumer was found" | ANSWERED by research 01 sections 2 and 5; unrelated to the decision. | See F9-4. |
| R14 | Ponytail half (`:3,:10,:44,:48-49,:52-55,:70-72,:77`, Next Steps E-1..E-3 `:126`) | OUT OF SCOPE: superseded by the 2026-11-07 user confirmation that Ponytail already installs and works. | BUILD-REQUEST.md:14 and research-notes line 130. Not researched; not verified here. |
| R15 | Follow-up `:113`: "install.sh prints 'install ok' and startup.sh:1184 prints 'installed.' even when nothing was configured" | NOT SUPERSEDED; becomes a requirement for the new path (report truthfully). | [CODE-VERIFIED] `install.sh:60` "install ok" and `startup.sh:1184` "installed." printed on the success branch whatever the seed state (the no-seed path reaches `:58-60`). |
| R16 | "BMAD skills read their config from the project's own `_bmad/` directory" `:48`; evidence 15 `:75` | NOT SUPERSEDED; it is the technical reason user-level BMAD content stays declined and the reason first-use creation must create `_bmad/` in the project, not only skills. | Not re-read this cycle; [CODE-VERIFIED] by research 01 section 7 (lines 224-283) and 05 b2 line 100 (75 files in the package `src/` reference `{project-root}/_bmad`; the "73" in `slug-configuration.md:54` is [UNVERIFIED], per 05). |

### F9-4. The prior "user-scope bmad skill install UNVERIFIED" is answered

REPORT.md `:120` (and Alternative Fix `:100`: "its user-level shell behaviour is UNVERIFIED") left open whether bmad 6.9.0 can install skills at user scope.
- Answer: NO, in 6.9.0 there is no code path. Research 01 section 2 (`01-bmad-6-9-0-installer-and-skill-runtime.md:54-85`): `global_target_dir` appears only in `tools/installer/ide/platform-codes.yaml` (43 occurrences: comment lines 9 and 12, 41 value lines), with no reader in any `.js`, `.json` or `.md` file under the package root. Section 5 (`:180-198`): the skill write path is `path.join(projectDir, target_dir)` (`_config-driven.js:245-248`), `install.js:12-51` has no `--global` or `--user` flag, so "Option F is not available in 6.9.0".
- Re-confirmed this cycle: [CODE-VERIFIED] Grep (count mode, `node_modules` excluded) of `global_target_dir` over `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method` returns 43 occurrences, all in `tools/installer/ide/platform-codes.yaml`; [CODE-VERIFIED] Read of `tools/installer/ide/_config-driven.js:245-248` shows `const { target_dir } = config; const targetPath = path.join(projectDir, target_dir); await fs.ensureDir(targetPath);`. This matches REPORT.md `:120` ("declares a `global_target_dir` ... no consumer was found") and goes beyond it by a whole-package search rather than `tools/**/*.js` only.
- Limits that remain [UNVERIFIED]: (a) whether a LATER upstream release added a consumer (01 line 198: update banner reports 6.12.4, not read; belongs to the not-yet-written web-02); (b) whether Claude Code loads user-level skills from `~/.claude/skills` and project skills created mid-session (not readable from the package; web-01); (c) "user-level shell behaviour" of a bootstrap skill (REPORT.md `:100`, `:120` row 3): research 03 and web-01 own it; this cycle did not test it. Directory `research/` currently holds 01-05 and no web-* file (Glob), so web results could not be consulted.
- Consequence for the options: user-scope BMAD install through the installer (research-notes Options E and F, lines 85-86) cannot deliver first-use creation in 6.9.0: Option E leaves `_bmad/` absent in the project because skills resolve the project root by walking up to the first `_bmad` or `.git` (01 section 6, `:213-217`), and Option F has no code path. First-use creation therefore needs a mechanism that runs `bmad install --directory <project>` per project (Options B, C or D), which is not in conflict with the "never globally" half of OD-1.

### F9-5. Gaps and Questions raised by this cycle (the file has no top-level `## Gaps and Questions` section; AMBIGUITIES_FOR_USER at line 134 is the nearest; these items are for the gaps log)

UNVERIFIED:
1. [UNVERIFIED] Exact wording of the 2026-11-07 AskUserQuestion answer: only `BUILD-REQUEST.md:14` carries it (no copy in `_bmad-output/specs`, Grep). Affects: git-cleanliness of first-use files, meaning of "first use", whether a user-level stub counts as "user level" (same as 05 U17 and AMBIGUITIES 1-2).
2. [UNVERIFIED] Whether the decision covers Orca-created worktrees (`catalogue-bundle SPEC.md:174`); it says "project". Leave open.
3. [UNVERIFIED] Whether issue #478 is still OPEN: `scout.md:12` records OPEN as of 2026-11-07T07:2x; no `gh` call was made this cycle. Research 05 U13 says "the GitHub issue was not opened" about the number 478; `scout.md:10-13` shows the URL `https://github.com/IronbellyOrg/Coder/issues/478` and `accuracy-check.md` is headed "Accuracy check for #478", so 478 is a real issue number per these working files; live GitHub state remains unobserved.
4. [UNVERIFIED] User-level skill and hook runtime behaviour (REPORT.md `:100`, `:120` row 3), later-upstream `global_target_dir` support (01 line 198), Claude Code mid-session skill loading: owned by 03, web-01, web-02; not available in this cycle.
5. [UNVERIFIED] REPORT.md evidence 10-13, 16-17 (superclaude files, `installed_plugins.json`, `ironclaude/install.sh`, `upstream-monitor.md:62`): Ponytail evidence, out of scope for this cycle and not re-read.
6. [UNVERIFIED] `startup.sh:1184` is cited in REPORT.md `:113` as printing "installed."; confirmed to exist at that line this cycle, but whether the log in `/tmp` is truncated each boot (`:113` second half) was not checked.

CODE-CONTRADICTED:
7. [CODE-CONTRADICTED] REPORT.md `:91` says `test-startup-boot.sh` pins "no seed: bmad writes nothing"; the file has no such assertion, only the `Installed-not-Configured` expectation (`:2209-2211`, `:2223-2224`). The "writes nothing" oracle is in test-57 `:446-452` only.
8. [CODE-CONTRADICTED] REPORT.md `:26` "Restrictions overridden: None" no longer holds after `BUILD-REQUEST.md:14`.
9. [CODE-CONTRADICTED] `claim-comment.md:19` links `.dev/issues/478/analysis/`; the directory does not exist (Glob error).
10. [CODE-CONTRADICTED] (trivial) EXISTING_FILES row at line 27 of this file says `install.sh` is 62 lines; the file read this cycle ends at line 61.
11. [CODE-CONTRADICTED] REPORT.md `:89-90` "MUST NOT change" rationale ("any-repo setup reverses OD-1") is overtaken by the decision for first-use creation (R10).

Questions for the synthesis author: (a) state in the Recommendation which of R1-R12 positions are overridden by name, so the spec cites them (`.dev/issues/478/spec.md`, not yet written); (b) keep the three-way split of the original ask (global declined, first-use decided, Ponytail out of scope) so #478's remaining "available globally" text (`issue-body.md:16`, `description.md:5`) is explicitly answered "declined" rather than silently dropped.

### F9 Summary

The gap was that the prior diagnosis (REPORT.md, 141 lines) and the 12 `.dev/issues/478/` files were listed but never read, so the synthesis had no statement of which prior positions the 2026-11-07 decision overrides. This cycle read all of them and mapped 16 REPORT.md positions (R1-R16): the decision overrides only first-use creation (R1, R2, R4, R5, R6, R8, R9, R10, R12), while global or user-level install, offline and profile-gated boot behaviour, and the seed install stay as built (R3, R7, R15, R16). It also answered the prior "user-scope bmad skill install UNVERIFIED" (no consumer of `global_target_dir` in 6.9.0, re-confirmed by whole-package Grep), found one wrong oracle claim (test-startup-boot does not pin "writes nothing"), and left 6 UNVERIFIED and 5 CODE-CONTRADICTED items (F9-5), chiefly the exact wording of the owner's answer, which exists only at `BUILD-REQUEST.md:14`.
