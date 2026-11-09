# Source-Document Fidelity Report 1 (BMAD 6.9.0 installer and skill runtime, image CLI wrapper, catalogue bmad slug)

**Status:** Complete
**Date:** 2026-11-08

---

## Source-Document Fidelity Report

**Report reviewed:** /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md
**Source scope:** BMAD 6.9.0 installer and skill runtime, the image CLI wrapper and the catalogue bmad slug (research files 01 and 02)

### Fidelity Findings

| # | Type | Source File | Report Section | Finding | Severity |
|---|------|-------------|----------------|---------|----------|
| 1 | Inaccurate | `bmad-method/tools/installer/ui.js:623-642` | 2.1 (non-interactive install command paragraph) | Report says "`--tools` is mandatory under `--yes` (`ui.js:630-641`)". The code throws only when `--tools` is absent AND no tools are previously configured (`configuredIdes.length > 0` returns the previous tools at :625-628). True for a never-installed tree (the first-use case), but the condition was dropped; research file 01 section 3.1 step 7 stated it correctly. | MINOR |
| 2 | Inaccurate (citation) | `bmad-method/tools/installer/core/manifest-generator.js:371-377` vs `core/install-paths.js:13` | 2.1 (created-path table, `_config/manifest.yaml` row) | Report cites `install-paths.js:13` for "`installation.version` = installer package version". `install-paths.js:13` only reads the version into the paths object; the manifest value is written from `packageJson.version` at `manifest-generator.js:373`. The claim is true, the cited line does not write it. | MINOR |
| 3 | Inaccurate (line numbers) | `templates/VSCode-AIDev02/image/catalogue/README.md:33,63-64,181-183` | 2.2 (stale-documentation paragraph) | Report cites README link lines "32, 64" and the `( source ~/.aienv && bash install.sh )` statement at "180-183". The `orca-build/provenance.md` link is on line 33 (not 32), the `docs/operations/...` link on line 63, and the subshell rule starts at line 181 (line 180 is the end of the idempotency item). The stale-doc conclusions hold (`orca-build/provenance.md` exists only at the repo root; Glob confirmed). | MINOR |
| 4 | Distorted (over-generalised) | `bmad-method/tools/installer/core/existing-install.js:111`; `ui.js:233-262` | 2.6 summary table "Version skew" row (report line 520) and 4.1 F-04 (line 645) | Both say `--yes` over "any existing `_bmad/` (even partial)" takes quick-update. Quick-update is offered only when `existingInstall.installed` is true (`ui.js:234`), i.e. `_bmad/core/` exists, a module is listed or a manifest parses (`existing-install.js:111`). A bare or empty `_bmad/` is not "installed": the choice list holds only "Modify" and `--yes` selects `update` (`ui.js:259-261`). Section 2.1 rows (127-129) state it correctly ("on an installed tree"); the summary rows drop the condition. No plan step changes (FIRST_USE is false for any existing `_bmad/`). | MINOR |
| 5 | Inaccurate (internal inconsistency) | `bmad-method/src/bmm-skills/4-implementation/bmad-quick-dev/SKILL.md:47-53`; `bmad-dev-story/SKILL.md:32-38` | 2.1 skill-runtime table, "Fallbacks written into skills" row (report line 118) | The row says the written fallback is to "read `customize.toml` directly". The source fallback reads three files in base, team, user order (`customize.toml`, `_bmad/custom/{skill-name}.toml`, `_bmad/custom/{skill-name}.user.toml`) and applies the resolver's merge rules. Section 2.3 (report line 278) states the three-file form, so the report contradicts itself; 2.1 was not corrected after the file 01 versus file 03 reconciliation. Effect on a never-BMAD project is the same (missing override files are skipped), so no conclusion changes. | MINOR |

Notes (not findings): `bmad-forge-idea/SKILL.md:27` says "Missing → neutral defaults; never block" (report quotes it as "Missing keys"); the `src/` Grep for `bmad install|npx bmad|...` returns the one `module.yaml:6` hit only when run case-insensitively (the report does not say so); `ui.js`, `manifest.js:415-418` and `legacy-warnings.js:104-143` do compare installed versions, but only to print notices (nothing blocks), so "no installed-versus-installer version gate" holds even though the report's Grep proof was scoped to `core/installer.js` (G-17 discloses that scope).

### Self-Audit

**Mode:** Section 7 states "Stop condition: not triggered" (report line 1325) and Section 8 says it is "an implementation plan and not a re-scope proposal" (line 1355). The STOP-AND-RE-SCOPE branch did not apply; I checked Section 8 as an implementation plan.

**What I read (source side, own tool calls):**
- BMAD 6.9.0 package (`/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/`): `package.json:1-30`; `tools/installer/bmad-cli.js:15-105`; `commands/install.js:8-150` (all of it); `ui.js` ranges 150-180, 200-330, 388-440, 615-645, 775-870, 1285-1320, 1410-1465, 1760-1780; `core/installer.js` 34-140, 366-450, 655-690, 945-1040, 1205-1250, 1544-1556; `core/install-paths.js:1-75`; `core/existing-install.js:40-122`; `core/manifest-generator.js` 38-100, 296-420, 425-550, 618-662; `core/uv-check.js:30-95`; `core/legacy-warnings.js:1-152`; `modules/official-modules.js` 205-285, 476-535, 548-710, 826-900, 1023-1145, 1380-1420, 1512-1532; `ide/platform-codes.yaml:1-62`; `ide/_config-driven.js` 185-255, 410-520, 518-810, 940-971; `src/bmm-skills/module.yaml` (all), `src/core-skills/module.yaml` (all), `src/scripts/resolve_config.py:28-178`, `resolve_customization.py:40-241`, `memlog.py:140-155`, `removals.txt` (all); SKILL.md files `bmad-dev-story:26-57`, `bmad-quick-dev:34-69`, `bmad-prfaq:28-44`, `bmad-agent-dev:12-53`, `bmad-help:20-29`.
- Whole-package Greps: `global_target_dir` (43 hits, 1 file; 41 value lines + 2 comment lines), `ancestor_conflict_check` (2 hits), child-process and git calls, HOME references, `semver`/version-gate tokens, `agent-manifest` (0 hits under `tools/` and `src/`), `resolve_*` references (52 matches in 39 files), `_bmad/(bmm|core)/config.yaml` (37 files), `python3 ` (41 lines in 31 files), "If the script fails" (25 files), `{project-root}/_bmad` (220 matches in 75 files; 168 in 40 `SKILL.md`), installer-hint Grep (one hit, case-insensitive); Glob of `SKILL.md` (46), `commands/*.js` (3), `src/scripts/**`.
- Repo: `catalogue/bmad/{install.sh,manifest.yaml,module.tf}` (all), `catalogue/profiles.yaml` (all), `catalogue/README.md` ranges 28-67, 78-137, 172-247, 344-352, 390-411, 588-605, `Dockerfile.coder` 100-150, 224-232, 464-504, 540-595, `modules.tf` 15-115, `parameters.tf` 85-125, `lib/spec2-health.sh` 70-195, 214-242, 516-580, 616-637, `scripts/startup.sh` 688-716, 1108-1193, 1222-1272, `main.tf` 70-152 and 170-180, `startup.tf:30`, `ironclaude/install.sh` (all), `orca/install.sh:1-43`, `test-1-catalogue-shape.sh:20-72`, `test-57-catalogue-configure.sh` 124-186, 316-340, 408-468, `coder-ci-aidev02-contract.yml` 1012-1034 and 1230-1244, `/usr/local/bin/bmad` (3 lines), `~/.aidev/status/welcome/bmad.txt` (13 lines), Grep of `resource "coder_script"` in `*.tf`.
- Live checks: `git ls-files` counts (17 `_bmad`, 577 `_bmad-output`, 237 skill files in 47 `bmad-*` dirs; manifest 6.10.0); `/home/coder/.git` and `/home/coder/_bmad` absent; no `seed-repo-path`; `gh run view 42384399575` log lines `Sysbox image layers: 68 (budget: 70)` and `[test-57-catalogue-configure] cold bmad: 374 ms`.
- Report: read in full for Sections 1 to 4, and Sections 6.0 to 7 and 8 (Phases 1 to 3, Phase 5 table tail, Phase 6, Phase 7 table (v)) and Section 9; Sections 5.1/5.2 (web research) and parts of Phase 4/5 detail were skimmed through Grep of every code citation, not read line by line.

**Why the count is credible:** I checked roughly 70 distinct source-derived claims (more than the 8 required) across all five checklist items: the installer flag surface and the `--yes`/`--tools` logic, both `collectModuleConfigs` branches and the partial-seed consequence (including that `loadExistingConfig` fills `_existingConfig`, not `collectedConfig`), the created-path table, the HOME and git Greps, the dead `global_target_dir` and `ancestor_conflict_check` hooks, the two resolver scripts and the skill-count figures, every `install.sh` line the report cites, the manifest, profiles, module and wiring files, the health classifier, the startup guard order, the Dockerfile layer cites and two CI log values. The adversarial assumption (at least 5 distortions) was met only at MINOR level: five minor findings, none changing a conclusion or plan step. I found no phantom finding (every cited function, flag, path and count that I could reach exists as described) and no aspirational claim (the report marks the predicate, the stub and every first-use mechanism as proposals, and marks nothing run as observed).

**Not verified by me (UNVERIFIED):** prior-review figures (`04-bmad.md` lines, "41 files", "6 files", "about 4 s"), the "Update Available 6.12.4" banner under `NPM_CONFIG_OFFLINE=true` and the Python 3.11/3.13 observation (research-session observations, not re-run), any `bmad install` outcome (never executed by anyone), web-research claims in Sections 5.1 and 5.2, `test-60`, `test-67`, `test-73`, `test-46`, `test-19`, `test-49`, `test-52` assertions, the `block-bare-python.sh` and `superclaude` package details, and the Sysbox-runtime job (the report itself marks that arm UNVERIFIED).

**Tool engagement (approximate, counted from my own calls):** Read: about 85 | Grep: about 25 | Glob: 8 | Bash: 2. Every call targeted a specific claim listed above.

### Summary

- Files checked: 44 (25 in the BMAD package, 19 in the repo, host wrapper and welcome file), about 5,000 lines read in the cited ranges (small files whole, large files by range)
- Claims verified: about 70
- Fidelity issues: 5 (CRITICAL 0, IMPORTANT 0, MINOR 5)
- Missing: 0 | Distorted: 1 (MINOR) | Phantom: 0 | Inaccurate: 4 (MINOR)

**Verdict: PASS** (no blocking issue; the five minor findings are notes for the orchestrator and can be corrected as wording and citation fixes without changing any conclusion or plan step).

## QA Complete
