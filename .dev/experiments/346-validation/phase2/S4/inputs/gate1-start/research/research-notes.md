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
