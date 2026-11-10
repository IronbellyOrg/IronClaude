# Synthesis 02: Target State, Gap Analysis, External Research Findings

**Topic:** BMAD first-use directory creation in a project that never had BMAD (BMAD-METHOD 6.9.0, Coder AIDev02 workspace)
**Report sections produced here:** 3 (Target State), 4 (Gap Analysis), 5 (External Research Findings)
**Sources:** research files 01 to 05, web-01, web-02 and gaps-and-questions.md, all under `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/`. Fix-cycle addenda inside those files supersede earlier text in the same files; the addendum text is used.
**Status:** Complete (Sections 3, 4 and 5 written; the final block is a self-audit that the assembler omits from the report)

Reference keys used below: R01 to R05 = research files 01 to 05; RN = `research/research-notes.md` (including its fix-cycle addendum F9); W01, W02 = web-01, web-02 (external context); GL = `gaps-and-questions.md`. Tags follow the research files: [CODE-VERIFIED] (read or searched in code), [UNVERIFIED], [CODE-CONTRADICTED], [STALE DOC]. Rows that R01 tags OBSERVED-FROM-6.10.0-TRACKED-TREE come from this worktree's git-tracked BMAD 6.10.0 tree, not from 6.9.0 installer output, and are version-mismatched corroboration only. No `bmad install` was run in this task, so every "what a first install writes" statement below is read from code unless it is labelled a prior-review observation (not re-run).

---

## 3. Target State

The target comes from one decision. On 2026-11-07 the user decided that BMAD should create its needed directories on first use in a project that never had it; the decision supersedes, for first-use creation only, the 2026-09-25 owner decision OD-1 and related non-goals, and says "Global installation of BMAD is NOT requested" (RN F9-1, quoting `BUILD-REQUEST.md:14`). That file is the only repo copy of the decision; the exact wording of the user's answer is not in the repo [UNVERIFIED, GL G-26].

### 3.1 Desired behavior

- **Desired behavior:** a user who opens a project that never had BMAD, and uses BMAD there, ends up with the directories BMAD needs created inside that project, with no further manual step beyond what the chosen trigger needs. The creation is one image-baked, version-pinned, offline command run per project (R01 s3.2, R03 A2; flags exist in `commands/install.js:14-37`, command never executed in this task):

  ```text
  NPM_CONFIG_OFFLINE=true bmad install --yes --directory "$P" --modules bmm \
      --tools claude-code --output-folder _bmad-output --user-name "<name>"
  ```

  `--output-folder _bmad-output` stays in every first-use command because `--user-name` is passed alongside it (R01 s3.2a, R05 d5; mechanism [CODE-VERIFIED] at `official-modules.js:1409`, outcome [UNVERIFIED]).
- **Desired behavior (global half):** BMAD framework content is not installed globally or at HOME. This is also a technical fact of 6.9.0, not only a policy: `global_target_dir` has zero consumers (R01 s2, [CODE-VERIFIED]), so a user-scope install has no code path (option F), and a home-directory install (option E) would leave `_bmad/` absent in the project because skills resolve the project root by walking up to the first `_bmad` or `.git` (R01 s6, s7.2). The ask in issue #478 therefore splits three ways: "available globally" is declined; first-use creation is decided; the third part of the original ask is out of scope by the 2026-11-07 user confirmation (RN F9 Summary, GL D-16).
- **Desired behavior (what "first use" means):** not decided. Each reading implies a different mechanism (owner question, GL section 5 item 2):

  | Reading of "first use" | Mechanism it implies | Options | Source |
  |---|---|---|---|
  | The user runs a `bmad` CLI command | image wrapper `/usr/local/bin/bmad` evaluates the predicate, then installs | C | R02 s6.2; R03 A3 C |
  | The user invokes a BMAD slash skill | a skill (stub) that exists before the project skills do | B1, B2, B3 | R02 s6.1; R03 A3 B |
  | The user opens a session in a project | a Claude Code hook that fires per session or per prompt | D1, D2, D3 | R02 s6.3; R03 A3 D |

- **Desired behavior (trigger predicate, a proposal from research, nothing implemented):** `FIRST_USE(P)` is true when P is the git work-tree top (or the current directory outside a repo), `P/_bmad` does not exist, no `P/.claude/skills/bmad-*` entry exists on disk (tracked or untracked), and P is writable (R03 A2). A directory that has `_bmad/` but no `config.toml` is a broken install, not first use.
- **Desired behavior (boot path):** the boot-time seed install stays as built (R05 b1 on `.memlog.md:33`); this is a plan assumption pending the owner (GL D-9).

```text
 trigger (CLI run | skill call | session start)         [owner reading open]
        |
        v
 FIRST_USE(P)?  -- false --> do nothing (project untouched, existing BMAD untouched)
        |
      true
        v
 NPM_CONFIG_OFFLINE=true bmad install --directory P ...   (image-baked 6.9.0)
        |
        v
 writes only under P:  _bmad/  _bmad-output/{planning,implementation}-artifacts/
                       docs/   .claude/skills/bmad-*/        (nothing under HOME)
        |
        v
 skills visible?  a new .claude/skills/ dir is not watched by Claude Code (W01 1.3):
                  SessionStart + reloadSkills, or /reload-skills, or restart
```

### 3.2 Success criteria

Each criterion is a pass or fail statement. "Basis" names where the research supports it; "Status" says how much of it is observed.

| ID | Pass or fail statement | Basis | Status |
|---|---|---|---|
| SC-01 | After first use in P, these exist under P: `_bmad/` (with `_config/`, `core/`, `bmm/`, `scripts/`, `custom/`), `_bmad-output/planning-artifacts/`, `_bmad-output/implementation-artifacts/`, `docs/`, and `.claude/skills/bmad-*/` | R01 s4 table (installer code); a prior review recorded the same directories (R01 F5-E, prior-review observation, not re-run) | Directory level read from code; per-file list UNVERIFIED (GL G-10); observe in CI |
| SC-02 | `P/_bmad/_config/manifest.yaml` and `P/_bmad/config.toml` exist | manifest is the same check as `test-57:323` and `spec2-health.sh:103`; `config.toml` is required by `resolve_config.py:156` (exit 1 when absent) (R01 s7.1, R03 A2) | [CODE-VERIFIED] as requirements; creation by a real run UNVERIFIED |
| SC-03 | The number of `P/.claude/skills/bmad-*` directories equals the count the installer prints (`Claude Code configured: <N> skills`), and N is recorded from CI | R03 A3 shared facts; 46 in a prior review versus 47 in the 6.10.0 tracked tree (R01 U12, F5-E) | N UNVERIFIED (GL G-11) |
| SC-04 | No directory literally named `{output_folder}` exists under P | R01 s3.2a; R05 d5 | Mechanism [CODE-VERIFIED]; outcome UNVERIFIED (GL G-14) |
| SC-05 | No BMAD framework content appears at HOME: no `~/_bmad`, `~/_bmad-output`, `~/docs` from BMAD, no `~/.claude/skills/bmad-*`; the bmm-only path writes nothing under `~/.bmad/cache` | R01 s4 and its Grep of every HOME reference (installer code writes `~/.bmad/cache` only for external or custom modules) | [CODE-VERIFIED] by Grep; never observed; `~/.npm` residue UNVERIFIED (GL G-15) |
| SC-06 | A project where first use did not happen is byte-unchanged. For the boot path this is the whole-HOME snapshot at `test-57:450` ("no seed: bmad writes nothing") | R04 s1, s2; R05 F1.2 row S1; existing non-BMAD skills in `.claude/skills/` are left alone on a fresh install (R01 s5) | Test exists; it breaks for certain only for B1, D1, E, F (GL section 6) |
| SC-07 | A project that already has BMAD is not rewritten: `FIRST_USE(P)` is false when `P/_bmad` exists or any `P/.claude/skills/bmad-*` exists on disk; a 6.10.0 tree is never run over by 6.9.0 | R01 F5-D, F5-F: the installer has no installed-versus-installer version gate, so a 6.9.0 `--yes` over an existing tree goes to quick-update with exit 0 (the 41-file downgrade is a prior-review observation, not re-run) | Guard logic [CODE-VERIFIED]; guard tested only on placeholder trees (R01 F5-D) |
| SC-08 | A second run changes nothing (byte-identical) | `test-57:331-335` (R04 s2) | Existing pin; applies to any new writer |
| SC-09 | The install completes with exit 0 and no network route, inside the project, and its real duration in a workspace is recorded | `NPM_CONFIG_OFFLINE=true`; built-in `bmm` needs no clone (R01 s3.3); CI `cold bmad` 374 to 392 ms for the whole baked `install.sh` with `--network=none` (R01 F5-C, prior-review observation, not re-run). The memlog "about 4s" includes an npx fetch and must not be blended with it | Workspace duration UNVERIFIED (GL G-09) |
| SC-10 | Git state is handled by an explicit rule, either hidden (the three `info/exclude` lines of `install.sh:32-34` and an unchanged `git status`, as `test-57:324` checks for the seed) or visible with the owner's acceptance | R02 s2; R05 b2 on `catalogue-bundle SPEC.md:126`; the installer itself never touches the project's git state and writes only `_bmad/custom/.gitignore` (R01 s3.4, [CODE-VERIFIED]) | The owner's choice is not decided (GL G-26, D-10) |
| SC-11 | The behaviour after a failed first run is stated and tested: the mechanism does not report a partial `_bmad/` as configured, and the recovery path is defined | `install.sh:41` documents "no auto-repair"; a failed run leaves `_bmad/core/`, which makes the next `--yes` take quick-update (R01 F5-D, F5-8; R05 b2 on `slug-configuration.md:55`: a first-use path inherits the ceiling unless the plan adds repair) | Quick-update on a half-written tree UNVERIFIED (GL G-13) |
| SC-12 | After first use the BMAD skills can be invoked, and the user is told the single step that is needed: none with a SessionStart hook that returns `reloadSkills`, otherwise `/reload-skills` or a restart | W01 1.3, 2.4 (external): a `.claude/skills/` directory that did not exist when the session started is not watched | Claude Code version in the image UNVERIFIED |
| SC-13 | The pinned tests have updated assertions and the new behaviour has its own test (per-variant detail in the paragraph below the table) | R04 A.10, A.11; R05 F1.2 to F1.5 | No test was run in this task (GL G-20) |
| SC-14 | The Sysbox image-layer gate stays at or below 70 layers | R02 A1, A2: 68 of 70 now, two free; B1, B3, D1, D3 and C-in-place add 0; B2 and D2 as written add 1 each | 68 read from two CI runs; the Sysbox-runtime job was not read (GL G-19) |
| SC-15 | Health and readiness wording is unchanged: bmad without a recorded seed stays `Installed-not-Configured`, because `spec2_health_observed bmad` reads only the seed repo | `test-57:452`, `test-startup-boot:2208-2211`, `spec2-health.sh:99-114` (R02 s5, R05 a11). First use in any other project is invisible to health unless `spec2-health.sh` and the `record_health` rows change together (GL D-14) | [CODE-VERIFIED] |
| SC-16 | The decision is recorded the way the repo records owner decisions: new row `OD-4` in `owner-decisions.md`, a `(decision) Owner 2026-11-07` bullet in the gap-closure `.memlog.md`, `SPEC.md` re-derived and never hand-edited; `README.md` line 241 reconciled with the manual command named in the text; a CHANGELOG entry under `[Unreleased]` | R05 b1, c1, c2, e | Records not yet written (RN F9-1) |

For SC-13 the research gives these per-variant results (R04 A.10, R05 F1.2): the only certain break is `test-57:450`, for B1, D1, E and F (when E and F run from `install.sh` at boot); B2, B3, C, D2 and D3 have no certain break but carry BREAKS-IF conditions (for example `test-67` COPY listing for B2, C, D2; `test-73-claude-retention` second drop-in rules for D2; `test-51:386-396` and `test-52:1374-1377` for B3 and D3). No existing test executes a first-use mechanism, and none proves delivery for B2, B3, D2 or D3, so a new test row is needed in every case (GL D-15; proposed assertion texts at R04 A.11). Validation goes through the `.github` Actions, not one-off scripts (project `CLAUDE.md`).

### 3.3 Constraints

| # | Constraint | Source | Consequence for the target |
|---|---|---|---|
| K-01 | No global BMAD install | `BUILD-REQUEST.md:14` (RN F9-1); R01 s2, s5, s6 | Options E and F are out; F has no code path in 6.9.0 and (external) in no published release through 6.12.4 (W02 s2) |
| K-02 | OD-1 is preserved except for first-use creation | `owner-decisions.md:5`, `.memlog.md:32-34`, `SPEC.md:77` (R05 b1) | Wording must be "no global or user-level install of BMad framework content", because the `bmad` CLI itself is installed globally (`Dockerfile.coder:139`, [CODE-VERIFIED]; R05 C1). Whether a content-free stub under `~/.claude/` counts as "user level" is an owner reading, not a code fact (GL section 5 item 1) |
| K-03 | No change in IronClaude or IronOrca unless research proves it unavoidable | R03 s6 "NEEDS OTHER-REPO CHANGE" | Research found none needed: every placement mechanism (M1 to M4) is in this repo and `superclaude install --force` keeps a user skill or hook under a new name. It would become necessary only if the skill or hook were shipped from IronClaude, or if superclaude started pruning unknown skill directories (R03 s6) |
| K-04 | Git-clean, offline install behaviour of the seed path is kept as the model | `install.sh:27-53`; `NPM_CONFIG_OFFLINE=true`; `timeout 120`; `test-57` runs `--network=none` (R02 s2, R01 F5-B) | A first-use command keeps the offline flag and the version guard; the git rule for non-seed projects is open (SC-10) |
| K-05 | Template-push versus image-rebuild limits | R02 s6.0, s6.4; R03 s1 | Files under `templates/VSCode-AIDev02/image/` (install.sh, Dockerfile, startup.sh, `/etc/skel`, managed settings) change the image tag and need an image rebuild plus `coder update`; root `.tf` files (`modules.tf`) need only a template push (B3, D3). HOME (`coder-<id>-home`) persists; `seed_if_absent` never overwrites, so an updated stub never reaches an existing workspace by that route (R03 s6 M1) |
| K-06 | Image-layer budget | `coder-ci-aidev02-contract.yml:1016-1029` (R02 A1) | Two free layers; other PRs may consume them first (GL G-19) |
| K-07 | The pin stays 6.9.0 | `Dockerfile.coder:139`; Renovate rows `expected.txt:6-8` (R05 f) | Bumping the pin does not enable option F (external, W02 s2, s8); three extraction sites keep their shapes; a new file that copies the version string needs its own Renovate row |
| K-08 | The project root is resolved from the working directory | `resolve_config.py:153-154` (does not walk up), `resolve_customization.py:58-66` (stops at `_bmad` or `.git`) (R01 s7) | First use must target the project root (`P` in `FIRST_USE(P)`); a subfolder session is an owner decision (GL D-3) |
| K-09 | Profile coverage | `profiles.yaml:18-21` (R02 s4.4) | `bmad` is only in profile `orca`; `minimal` has none, and image-wide mechanisms (C, B2, D2) are not slug-gated (GL D-4) |
| K-10 | Contract shapes that any option must keep | R04 s4, s5; R05 a-supplement | `bmad` stays an executable file on PATH with `--version` and `--help` exiting 0 non-interactively (`test-19`); `bmad/install.sh` keeps `command -v` plus `exit 2` and no unquoted install verb; the catalogue slug directory holds exactly three files (`test-1-catalogue-shape:25`); the welcome text keeps the tokens `bmad` and `bmad --help`; no new skill, wrapper or hook file name contains the whole words `preview`, `share`, `share-port`, `expose`, `dev-preview` (`test-3-reserved-names:27`); `health_check.command` stays an executed probe (`bmad --version`), never a file-existence check (`test-46:1804-1815`); a NEW catalogue slug breaks `test-52:1381-1383` and the `test-startup-boot` ledger whitelists (`:201`, `:231`, `:1968`) |
| K-11 | Single writer of `seed-repo-path` | `startup.sh:673` (R05 b3) | A first-use mechanism must not write `~/.aidev/status/seed-repo-path` |
| K-12 | Claude Code behaviour bounds hook and skill options (external) | W01 | User-level hooks and skills apply to every project; interactive sessions hold hooks until workspace trust is accepted; a user-level skill with a `bmad-*` name would shadow the project copy. Detail in section 5.1 |

## 4. Gap Analysis

Scale used in this section: Critical = the target cannot be met without closing it; Important = it changes an option row, a plan step or a pinned test; Minor = lower priority but still to be fixed. This is a rating by effect on the target state. The gaps log used "Critical = blocks synthesis" and found none; both statements hold. Where a capability is declared as shipped or enabled but nothing consumes it at run time, the row is rated Important or higher and says whether a scope decision is cited; none is deferred to "future work" without one.

### 4.1 Functional gaps between current state and target state

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| F-01 No first-use creation mechanism exists | The only `bmad install` call is `catalogue/bmad/install.sh:42`, run at boot for the one seed repo recorded in `~/.aidev/status/seed-repo-path`; with no seed it prints "nothing to configure" and writes only a marker. A repo cloned after boot is never visited. The catalogue contract has no field for "run when first used" (R02 s2, s4 Key Takeaways) [CODE-VERIFIED] | SC-01, SC-02: BMAD directories exist in a project after first use | Critical | Feasible without a global install and without an IronClaude or IronOrca change on the evidence so far (GL section 6). Which of B, C, D fires at the right moment is not determinable until the owner reads "first use" (3.1) and the Claude Code facts in section 5.1 are applied |
| F-02 The only "never had BMAD" guard is seed-specific and not on-disk complete | `install.sh:22-25`: branch 1 needs a recorded seed that is a git work tree (a directory without `.git` ends as "nothing to configure"); branch 2 tests `_bmad` by plain existence and counts only git-tracked `.claude/skills/bmad-*`, so untracked skills with `_bmad/` deleted read as "never had BMad" (R03 A2) [CODE-VERIFIED] | `FIRST_USE(P)` (3.1): project root resolved, `_bmad` absent, no `bmad-*` skill on disk, writable | Important | The predicate is a research proposal, not code. Subfolder sessions resolve to the repo top; the slug's root-anchored excludes would fail on a subfolder install (git anchoring itself UNVERIFIED, GL G-21) |
| F-03 Skills copied without `_bmad/` do not work and nothing says so | 6.9.0 skills need `{project-root}/_bmad/` (scripts, `config.yaml`, `bmad-help.csv`). With `_bmad/` missing, `resolve_config.py` exits 1 and `resolve_customization.py` silently falls back; no skill under `src/` detects a missing `_bmad/` or tells the user to run the installer (R01 s7, [CODE-VERIFIED]). Independent upstream report of the same state: issue #2677 (W02 s9, external) | `_bmad/` and the skills arrive together (SC-02); no state where skills exist without `_bmad/` | Important | A user-level skill alone cannot make BMAD usable (RN F9-3 R16). Model behaviour in the broken state is UNVERIFIED (GL G-07) |
| F-04 No protection against running 6.9.0 over a newer or partial tree | The installer has no installed-versus-installer version gate; any existing `_bmad/` (even a bare `_bmad/core/`) sends `--yes` to quick-update with exit 0 and no warning. Only the slug's existence guard (`install.sh:24`, tested on placeholder trees) stands in the way; the manual command in `manifest.yaml:14` has no guard (R01 F5-D, F5-F) [CODE-VERIFIED] mechanism; the 41-file downgrade is a prior-review observation, not re-run | SC-07 | Important | Applies to options B, C and D; the number of repos on a newer tree can only grow while the image stays at 6.9.0 (latest published is 6.12.4, W02 s1) |
| F-05 A failed first run leaves a partial `_bmad/` that is never repaired and reads as success one boot later | `InstallPaths.create` makes `_bmad/` and `core/` first and `install()` has no rollback; `install.sh:41` states "no auto-repair"; the next boot sees `_bmad/` and takes the "left untouched" branch to the marker write. The catalogue contract requires an idempotent installer with a marker short-circuit (`README.md:179-183`) and the shipped bmad slug has none (R01 s8.1, R02 s2, s4.6) [CODE-VERIFIED] | SC-11: failure is visible, a partial tree is not reported as configured, recovery defined | Important | `resolve_config.py:156` needs `_bmad/config.toml`, so a guard on bare `_bmad/` is too weak (GL D-1, D-2, D-6) |
| F-06 No test executes or proves a first-use mechanism; one pin breaks for certain for B1, D1, E, F | `test-57:450` (whole-HOME snapshot, "no seed: bmad writes nothing") breaks for certain for B1, D1, E, F. No test runs a skill, hook or first-use bootstrap, and none proves delivery for B2, B3, D2, D3 (R04 A.10, R05 F1.3) [CODE-VERIFIED by reading; no test run] | SC-13: updated assertions plus a new first-use test | Important | Proposed assertion texts per variant: R04 A.11. Tests run only in CI (GL G-20) |
| F-07 Health and readiness cannot see first use outside the seed repo | `spec2_health_observed bmad` reads only `seed-repo-path` (`spec2-health.sh:99-114`); the readiness line keeps "Catalogue not configured: bmad" for a seedless HOME; health is computed once per boot (R02 s5, R05 a11) [CODE-VERIFIED] | SC-15 unchanged wording, or an explicit change of `spec2-health.sh` and the `record_health` rows together | Important | A declared state (`Configured`) with no consumer for user-created projects. No cited scope decision defers it, so the plan must either extend health or state that first use is deliberately invisible (GL D-14) |
| F-08 Nothing tells Claude Code to rescan a skills directory created after the session started | `bmad install` prints "Launch your AI agent from your project folder" afterwards (`installer.js:1233`). A new top-level `.claude/skills/` is not watched; it needs `/reload-skills` or a restart (W01 1.3, external). A SessionStart hook can return `reloadSkills` (W01 2.4, external) | SC-12 | Important | Which trigger can rescan is an option property: only a SessionStart hook has a documented field; a skill or wrapper trigger relies on the user (section 5.1) |
| F-09 Decision records and user-facing text are out of date for the new decision | The decision exists only at `BUILD-REQUEST.md:14`. `owner-decisions.md:5` and `.memlog.md:32` still read "never globally"; `README.md:241` says nothing about where BMad is configured; `manifest.yaml:12-14` says "BMad is already set up there" unconditionally and covers only the seed; the Dockerfile CLI is global although the text says "never globally" (R05 b1, b3, e; R02 C7) | SC-16 | Important | New row `OD-4`, a memlog bullet, `SPEC.md` re-derived (never hand-edited); keep `README` anchor at line 100, the five-cell table shape and the manual command in the text |
| F-10 Upstream declares `global_target_dir` for global install, with no consumer | `platform-codes.yaml:9` calls it "User-home directory for global install"; 41 platform value lines carry it; no code reads it in 6.9.0 (R01 s2, [CODE-VERIFIED]); the same holds for 6.10.0 and 6.12.4 (W02 s2, external) [STALE DOC] | Not relied on; option F is not available | Important | Constraint, not future work: the scope decision is cited (global installation is not requested, `BUILD-REQUEST.md:14`) and the technical fact is verified. The header comment over-promises in every version checked |
| F-11 Upstream declares `ancestor_conflict_check`, and no platform sets it | The reader exists (`_config-driven.js:191`); the key appears only in a header comment (`platform-codes.yaml:10`); the claude-code block does not set it, so a parent-level or user-level `bmad-*` skill directory does not block a project install in 6.9.0 (R01 s6, [CODE-VERIFIED]) [STALE DOC] | The plan neither relies on a conflict refusal nor assumes it stays off | Important | If a later 6.x enabled it, an install at HOME would make every project install fail for that tool (R01 s6). Whether 6.10.0 to 6.12.4 set the key was not searched (W02 searched only `global_target_dir`): UNVERIFIED |

### 4.2 Gaps from the gaps log (all 30 rows, each rated)

Severity is the grade from `gaps-and-questions.md` section 1. The Notes column states the status after web research (external answers are marked) and after the fix cycles. "Resolved by fix" rows are kept so nothing from the log is dropped.

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| G-01 Does Claude Code load a project skill directory created after the session started? | Repo files do not decide it (R03 gap 9). External answer: a `.claude/skills/` that existed at session start is watched and picks up new skills live; a top-level skills directory that did not exist then is not watched and needs `/reload-skills` or a restart; a SessionStart hook can return `reloadSkills: true` (W01 1.3, 2.4) | SC-12 | Important | Answered externally with a split answer. Residual UNVERIFIED: whether a prompt-time trigger can rescan without the user typing `/reload-skills`; the Claude Code version in the image; the version that introduced `reloadSkills` (2.1.152 appears only in a user-authored issue quoting the changelog) |
| G-02 Does Claude Code load `~/.claude/skills` in every project, and how does it rank it against a project skill of the same name? | R01 U7, R03 A4 open until web research. External answer: personal skills load in "all your projects on this machine"; "Enterprise over personal, and personal over project", so a user-level `bmad-*` stub would win over the project copy (W01 1.1, 1.2; the shadowing consequence is W01's inference, not tested) | A stub, if allowed, uses a name that equals no `bmad-*` skill; blast radius stated | Important | Answered externally. Residual: `/etc/claude-code/` keys `allowManagedHooksOnly` and `strictPluginOnlyCustomization` would disable user-level skills and hooks; the image's content was not checked (only `10-retention.json` is known, R03 s4) |
| G-03 Does a `managed-settings.d/*.json` drop-in accept `hooks`, and do they merge with user hooks? | R02 U9, R03 gap 5 unverified. External: drop-ins merge alphabetically after `managed-settings.json`, lists combine, `hooks` is list-merged and managed policy is a documented hook location; no single sentence says a drop-in may hold `hooks` (W01 3.3, inference); managed hooks are additive to user hooks and cannot be disabled by the user's `disableAllHooks` | Decides option D2 | Important | Documented by inference, not by one sentence. A managed hook runs in every project for every user. Test side: a second drop-in file against `test-73` is unverified (G-20) |
| G-04 Hook and permission runtime semantics | R03 gaps 7, A5 #18 to #20 unverified. External: edits to `hooks` in settings files apply to a running session (W01 4.2, closes UV-42); SessionStart and UserPromptSubmit stdout is added to Claude's context, SessionStart cannot block (2.2); command-hook timeout default 600 s, 30 s for UserPromptSubmit (2.3); interactive sessions hold back hooks from every settings file, including `~/.claude/settings.json`, until workspace trust is accepted (4.1); a Bash call made by Claude prompts by default (5.1) | Hook design (option D) fits these semantics | Important | Residual UNVERIFIED: whether a held-back SessionStart hook runs later in the same session; whether SessionStart stdout is shown to the user; the effect of `skipDangerousModePermissionPrompt`; whether a command hook runs without the Bash prompt (best reading only); whether the Orca `PermissionRequest` hook ever decides a permission. Existing hooks here use timeouts of 1 to 10 s (R03 A3 D.2) |
| G-05 Did a later upstream BMAD release add a `global_target_dir` consumer or user-scope flag? Does 6.12.4 exist? | 6.9.0 has no consumer (R01 s2, [CODE-VERIFIED]). External: 6.12.4 is `latest` (published 2026-10-14); `global_target_dir` appears in one YAML file only in 6.9.0 (43 hits), 6.10.0 (43) and 6.12.4 (46); the `install` command has no scope flag in 6.9.0 or 6.12.4 (W02 s1, s2). The only upstream user-scope pattern is the v7 preview (Skills CLI `-g` plus `bmad setup`), a different channel (W02 s8) | Option F recorded as "no code path in 6.9.0 through 6.12.4" | Important | Answered externally. Not searched: 6.11.0 and 6.12.0 to 6.12.3 tarballs individually, `-next` prereleases, the `V6.12` branch. A pin bump does not enable F |
| G-06 Behaviour of the 41 `python3 ` steps in 31 `SKILL.md` files under the UV-only hook | Hook `block-bare-python.sh` is packaged by superclaude and installed through the ironclaude slug for Default-profile users; it exits 2 on a command word `python3` (R03 A1, [CODE-VERIFIED]). 25 of 31 files have a written "If the script fails" fallback; 6 do not. External: 6.12.4 skills have 0 `python3 ` lines and 105 `uv run ` lines in 39 files (W02 s3) | Skills work in a Default-profile workspace after first use | Important | Whether Claude emits the bare form, whether it treats a hook block as "the script fails", and whether a fresh workspace has the same hook registration are UNVERIFIED. A pin bump would change the skill set and layout (W02 s3), so it is a trade-off, not a fix for first use |
| G-07 Skill behaviour when `_bmad/` or some config keys are missing; which file `--set core.project_name` patches | Code-derived only; the `install.sh:42` flag set leaves `project_name`, `communication_language`, `document_output_language` unwritten (R01 s3.2a). External, documentation level: `--set` is a post-install patch into `_bmad/config.toml` or `config.user.toml` and `_bmad/<module>/config.yaml` (W02 s7.1) | Known behaviour, observed in CI | Important | Documented, not observed; `set-overrides.js` was not read. Whether a model completes a skill with no `_bmad/` is UNVERIFIED (W02 s10) |
| G-08 Model compliance with a stub's predicate; hook timeout against install time; hook working directory | Nothing run (R01 F5-9, F5-F). External: a hook receives `cwd` and the environment variable `CLAUDE_PROJECT_DIR`; they may differ (W01 2.1) | Stub or hook evaluates `FIRST_USE(P)` correctly and does not offer reinstall | Important | A stub that offers "reinstall" or "update" re-opens the quick-update path. Install time in a workspace is G-09 |
| G-09 Real duration of a first install in a Coder workspace | CI `cold bmad` 374 to 392 ms (baked CLI, no network, whole `install.sh`) and the memlog "about 4s" (npx fetch, scratch HOME) are different configurations, ten times apart, and neither is a workspace measurement (R01 F5-E, prior-review observations, not re-run) | SC-09 | Important | Do not blend the two figures. Observe in CI during implementation |
| G-10 Exact files a first install writes; first run in a directory with no `.git` | All rows read from code (R01 s4). External: upstream 6.9.0 docs list only `_bmad/` and `_bmad-output/` and say nothing about an empty directory or a missing `.git` (W02 s7.2) | SC-01, SC-02 | Important | The upstream tutorial understates the code finding (`.claude/skills/bmad-*` and `docs/` too); the code finding stands (codebase beats web) |
| G-11 Exact skill set, count and names written to `.claude/skills/` | 46 `SKILL.md` by Glob and "46 skills" in a prior review versus 47 `bmad-*` directories in the tracked 6.10.0 tree; `ManifestGenerator.collectSkills` not enumerated (R01 U12) | SC-03 | Minor | External: the 6.9.0 tarball's plugin manifest lists two plugins with 12 and 33 skills (W02 s9 item 7); a different channel, it does not settle the count |
| G-12 Default module list of a bare `--yes` | `bmad-modules.yaml` was not read (R01 U4) | The command always passes `--modules bmm` | Minor | External: the 6.9.0 install guide says a single install hits the GitHub API once per external module (60 calls per hour per IP, anonymous) (W02 s7.1). The safe form avoids the question; closable by reading the registry file |
| G-13 Partial `_bmad/` after a failed first run and what quick-update does to it | `InstallPaths.create` makes `_bmad/core/` first, so a later `--yes` takes quick-update; `installer.js:1254-` was not read (R01 F5-D, R05 U7) | SC-11 | Important | Mechanism [CODE-VERIFIED]; outcome UNVERIFIED. See F-05 |
| G-14 `{output_folder}/` literal-directory facts and prior-probe facts | Mechanism at `official-modules.js:1409` [CODE-VERIFIED]; outcome of `--user-name` without `--output-folder` not run; flags of the prior probe, the `--offline` flag origin and the "6 files / 41 files" counts are prior-review observations (R01 F5-1, F5-2, F5-7; R05 U6, U10) | SC-04: `--output-folder _bmad-output` kept in every command | Minor | External: release note #2671 (6.11.0) says core `--set` keys were applied after install in earlier versions, so created directories still used `_bmad-output/` (W02 s5); it concerns `--set`, not the `--user-name` case |
| G-15 HOME writes and network side effects of the installer | Code shows `~/.bmad/cache` only for external or custom modules; `~/.npm` origin, `npm view` and `uv --version` residue, and the offline-banner source are UNVERIFIED (R01 U2, U3, F5-11) | SC-05 | Minor | External: other `os.homedir()` uses in 6.12.4 are the same caches and `~` expansion (W02 s2); consistent with R01 |
| G-16 What `bmad install --directory ~` writes (option E); whether the manual command completes | R01 s6 derives `~/_bmad`, `~/_bmad-output`, `~/docs`, `~/.claude/skills/bmad-*` from code; R02, R04, R05 call it UNVERIFIED; whether it edits `~/.claude/CLAUDE.md` is unknown; the command at `manifest.yaml:13-14` was never run | Option E is excluded by K-01 anyway; the manual command still works | Important | External: upstream's own answer to a global-install request (#1852, declined) was to install once at a parent workspace folder, a variant of E that works only if skills find that root (W02 s9 item 4); for repos with their own `.git` this is UNVERIFIED |
| G-17 Meaning of the `semver` hits in four installer files | The claim relied on is only that `core/installer.js` has no `semver` token (R01 F5-12) | n/a | Minor | Closable by reading those files |
| G-18 The built image really contains `bmad-method@6.9.0` and the wrapper | Evidence is `Dockerfile.coder:139` text, the CI PASS of `test-57`, and `bmad --version` = 6.9.0 in this workspace (R01 F5-C; R05 d1); the image itself was not inspected | n/a | Minor | |
| G-19 Sysbox layer-budget residuals | 68 of 70 measured on two CI runs (the dind-sidecar job); that the base image contributes 8 layers, that each RUN adds exactly one layer, that B2 and C can fold into existing COPYs at 0 layers, that nested COPY under `/etc/skel/.claude/skills/<name>/` creates 0755 directories, and Docker cache behaviour are inferences (R02 A2 to A7; R04 A.9) | SC-14 | Important | Another PR can consume the two spare layers first. `Dockerfile.coder:468` ("no headroom") is [CODE-CONTRADICTED] as a measurement and true only as policy |
| G-20 Test-suite residuals | No test was run; the value of `IDE_CONVERGENCE_TIMEOUT_S`, the `manifest.schema.json` required fields, `repin.sh --verify`, two failure strings of `test-b1-affordance-matrix`, the full skel copy at `test-4-pane-title.sh:89`, `ALLOWED_SET` of `test-5-coder-app-allowlist`, a second drop-in against `test-73`, which modes of `test-52` reach the `ORCA_FIXTURES` block, the file count of `.github/contract-tests/`, and two rows taken from file 04 are unverified (R04 gaps and addendum gaps; R05 U-F1-3 to U-F1-6) | SC-13 | Minor | Closed by CI during implementation |
| G-21 Environment residuals | Home volume deleted with the workspace; the `_src/superclaude/cli/` copies identical to those read; Claude Code and Orca writing `~/.claude/settings.json`; each `~/.claude/skills` entry a real directory; Docker seeding a new named volume from the image; a fresh workspace may show different `~/.claude/` content; git anchoring root-anchored `info/exclude` patterns; the "untracked skills but `_bmad/` deleted" case (R03 gaps 1 to 4, 8, 12; A5 #16, #24) | n/a | Minor | |
| G-22 Startup `§10`/`§12` and `wire_ccsession()` never write `settings.json` or skills | Closed by an analyst Grep (only `startup.sh` lines 275, 979, 1282, 1285) and a read of `install_ccsession.py:1-100` | n/a | Minor | Resolved by fix |
| G-23 Small image and catalogue unknowns | NVM node not on the default PATH (`Dockerfile.coder:134-135` comment only); the exact Coder flow from template push to a running workspace; whether the task's "OD-1" is this repo's label; the inference that a `bmad` wrapper cannot run when a BMAD skill is invoked (R02 U1, U10, U12, U14) | n/a | Minor | R05 b1 reads `owner-decisions.md:5` ("OD-1 BMad placement") and the `test-57:10` comment ("bmad excluded, OD-1"), which point to the same decision; the log keeps the item open |
| G-24 Test-inventory gaps | R02 U7, U11 and R04 gaps 2, 3 and R05 U-F1-2 closed by the file 04 addendum A.1 to A.8: 30 files classified, 15 relevant | n/a | Important | Resolved by fix (Gate 1 verified) |
| G-25 Tag disagreement for options E and F | R02, R04, R05 say UNVERIFIED while R01 s2 and s5 give CODE-VERIFIED "zero consumers of `global_target_dir`; option F has no code path" | Use R01's tags; drop the F `X` cells | Minor | Resolved by fix. This synthesis uses R01's tag. The E write set stays open (G-16) |
| G-26 Owner and decision wording not available to the researchers | The exact 2026-11-07 answer exists only at `BUILD-REQUEST.md:14`; git-hidden versus visible first-use files; coverage of Orca-created worktrees (`catalogue-bundle SPEC.md:174` says "project") (R05 U17; RN F9-5 #1, #2) | SC-10 | Important | Owner question; goes to report Section 9 |
| G-27 Minor unknowns in the document trail | "Worktrees carry only tracked files" (`SPEC.md:141`); the "73 skill files" claim against 75 files in package `src/` (40 `SKILL.md`) and 46 `SKILL.md` counted in R01; seed-repo runtime result of the boot install (this workspace has no `seed-repo-path`); snapshot hashes; whether 478 is the number to cite in a CHANGELOG entry and whether the issue is still open; markdownlint version; invisible `image/` files; a root-level `_bmad/`; whether the boot log in `/tmp` is truncated (R05 U4, U5, U9, U12 to U16; RN F9-5 #3, #6) | n/a | Minor | |
| G-28 Documentation hygiene found by QA, not acted on | R01 line 18 against R01 s3.3 on `node --version`; an untagged managed-settings precedence sentence in R03 s6 M4; wrong sizes and moved lines on true claims (`install.sh` 61 not 62 lines, `manifest.yaml` 29 not 30, `Dockerfile.coder` 594, catalogue README 604, `spec2-health.sh` 636, `startup.sh:1175` not :1174); R03 s2 lists `startup.sh:1172`, which is only a comment; R05 Summary still counts 17 UNVERIFIED and 6 CODE-CONTRADICTED while its merged tables add more; R04 line 238 says A.1 to A.8 where the addendum runs A.1 to A.11; R01 line 491 says the 03 addendum was In Progress, it is Complete | Research files corrected | Minor | None changes a conclusion. Use the corrected values in the report |
| G-29 Evidence for the out-of-scope part of the prior diagnosis was not re-read | Out of scope by the 2026-11-07 user confirmation (RN TEMPLATE_NOTES) | none | Minor | No action |
| G-30 Gate 1 closed with a user-accepted exception | Lines 376 and 408 of R05 were corrected by the orchestrator and re-read by the executor only; no fourth agent reviewed the corrected text (`qa/qa-gate1-decision.md`) | n/a | Minor | Accepted exception. The corrected lines concern option C only: the "none" reasoning for the X2 row (line 376) and the C-F1-2 wording (line 408). This synthesis uses the corrected reading: C is BREAKS-IF, not "none", in rows S3, S7, S10, S11, S13 to S15, X2 and X3 of R05 F1.2 and F1.3, because the seeded `test-57` runs reach the baked wrapper through `install.sh:42` |

### 4.3 Stale documentation and corrected claims (30 CODE-CONTRADICTED rows and 13 STALE DOC rows from the log, grouped)

Every documentation-sourced claim below is corrected to what the code shows; none is used as current architecture. IDs are the log's (GL sections 2.2 and 3). R05 C5 was withdrawn in fix cycle 1 and is not a row.

| Items | Claim in the document | What the code shows | Severity | Treatment in the report |
|---|---|---|---|---|
| CC-01, SD-01 | `platform-codes.yaml:9`: `global_target_dir` is the "User-home directory for global install" | No reader in 6.9.0 (and none in 6.10.0 or 6.12.4, W02); 41 inert value lines | Important | See F-10 |
| SD-02 | `platform-codes.yaml:10`: `ancestor_conflict_check` refuses an install when an ancestor holds BMAD | The reader exists (`_config-driven.js:191`); no platform sets the key, so it never fires | Important | See F-11 |
| CC-02, CC-03, SD-03 | The worktree's `_bmad/`, `_bmad-output/` and `.claude/skills/bmad-*` read as installed 6.9.0 output; `agent-manifest.csv` read as installer output | They are a tracked 6.10.0 tree (manifest version 6.10.0, installed 2026-04-18); `agent-manifest` is absent from the 6.9.0 package | Minor | Used only as version-mismatched corroboration (OBSERVED-FROM-6.10.0-TRACKED-TREE) |
| CC-04 | Memlog `:21`: "`--yes` without `--output-folder` creates literal `{output_folder}/`" read as a bare-`--yes` defect | Bare `--yes` seeds `output_folder: '_bmad-output'` (`ui.js:838-861`); the mechanism lives in the `--user-name` combination (`ui.js:807-837`) | Minor | Quote the memlog line, never describe it as a bare-`--yes` defect |
| CC-05 | `04-bmad.md:15, 78`: pin at `Dockerfile.coder:360` | The pin is at `Dockerfile.coder:139`, the wrapper at `:134-143` | Minor | Line numbers only |
| CC-06, SD-04 | `install.sh:18` error text: "`/usr/local/bin/bmad` symlink" | A two-line wrapper script; a symlink would fail with `env: node: not found` (`Dockerfile.coder:134-135`) | Minor | Low impact |
| CC-07, CC-08, CC-09, SD-06 | Catalogue README paths `/config/workspace/Coder/catalogue/...`; relative links at lines 32, 64, 594-596; "`( source ~/.aienv && bash install.sh )`" (180-183) | The catalogue is `templates/VSCode-AIDev02/image/catalogue/`; the links resolve to nothing; the subshell form is true only for bmad (`startup.sh:1175`) | Minor | Do not copy these paths |
| CC-10, SD-07 | `startup.tf:30`: "ONLY runtime coder_script in the template" | Other `coder_script` resources exist at `modules.tf:82`, `main.tf:220` and `:233`, and in the orca and vibe-kanban modules | Minor | Relevant to B3 and D3 (a new root `coder_script` is allowed) |
| CC-11, SD-05 | `profiles.yaml:1` path comment | Real path has `image/` | Minor | |
| CC-12 | `manifest.yaml:12`: "BMad is already set up there" | True only when the guards pass; with no seed or an existing partial `_bmad/` nothing is configured | Minor | See F-09 |
| CC-13 | `Dockerfile.coder:468`: Sysbox budget "has no headroom" | 68 of 70 measured, two free; true only as a policy | Minor | See G-19 |
| CC-14 | R01 s7.5 wording on the `python3` skill steps and the fallback | 41 lines in 31 files (2 core, 29 bmm); 25 files have the written fallback; the fallback reads three TOML files, not only `customize.toml`. R03 A5 says "both" corrections but spells out one; which second correction is meant is UNVERIFIED | Important | See G-06 |
| CC-15, SD-08 | `PROJECT_INDEX.md:13, 36, 65`: "T1-T55" | Tests run to test-79, with 12 shared numbers and two unnumbered scripts | Minor | Do not use "T1-T55" as the boundary of pinned tests |
| CC-16 | The finding's nine named tests are among the 30 files hit by the `startup.sh` search | None of the nine is; they come from other searches (R04 A.1) | Minor | R04 A.4 to A.7 examine them separately |
| CC-17 | `owner-decisions.md:5`, memlog `:32`: BMad is "never globally" | The CLI is global (`Dockerfile.coder:139-143`); only framework content is per project | Important | Use "no global or user-level install of BMad framework content" (K-02) |
| CC-18, SD-09 | `.memlog.md:27`: "the seed repo gets no `_bmad/`" | The seed repo does get `_bmad/` (`install.sh:42`, `:46`); voided by line 32 | Minor | History only |
| CC-19, SD-10 | `fr-audit.md:12` cites `install.sh:38-66` | The file has 61 lines; the seed block is 21-55 | Minor | |
| CC-20, SD-11 | Profile `agile-full` (`SPEC.md:34, 166`) | `profiles.yaml` has only `orca` and `minimal` | Minor | |
| CC-21, SD-12 | PRD addendum Option A "user-level availability" as lead | Replaced by the shipped seed install and the 2026-09-25 cancellation; its rejected Option B reasons (writes into owner repositories, conflicts with committed BMAD) are the same risks first-use creation carries | Minor | The plan names those two risks and how the guard handles them |
| CC-22 | "The offline setting stops the help path from running `npm view`" | An "Update Available 6.12.4" box printed under `NPM_CONFIG_OFFLINE=true` for `--list-tools`; the banner is genuine (W02 s1) but its source (npm cache or network) is UNVERIFIED | Important | Do not assume the update probe is silent offline |
| CC-23, CC-24 | R04 s7 test-49 row "c" for B and D; R05 Summary naming C among variants needing a boot-time replacement assertion | `test-49` fails only on a non-comment `LIFECYCLE_RE` match and does not list `install.sh` or `modules.tf`; C edits `Dockerfile.coder:142`, not `install.sh` | Minor | Corrected in the research files |
| CC-25 | `test-57:386` comment "the only installer that edits settings.json" | Current today; stale under D1 (the self-heal fixtures run ironclaude only) | Important | A coverage gap for D1, not a failing pin |
| CC-26 | `REPORT.md:91`: `test-startup-boot` pins "no seed: bmad writes nothing" | Only `test-57:446-452` does; `test-startup-boot` pins `Installed-not-Configured` (`:2209-2211`) | Minor | |
| CC-27, CC-30 | `REPORT.md:26` "Restrictions overridden: None"; `:89-90` "any-repo setup reverses OD-1" | Overtaken by `BUILD-REQUEST.md:14` for first-use creation | Minor | The Recommendation names the overridden positions (GL D-16) |
| CC-28, CC-29 | `claim-comment.md:19` links `.dev/issues/478/analysis/`; `install.sh` "62 lines" | The directory does not exist; the file has 61 lines | Minor | Trivial |
| SD-13 | `slug-configuration.md:54` "73 skill files" | 75 files in package `src/` reference `{project-root}/_bmad` (40 `SKILL.md`); 73 not reproduced. The `{output_folder}/` wording at `:53` is not stale | Minor | Qualitative point stands |

External documentation checked against the code (codebase wins): the 6.9.0 getting-started tutorial says the installer "creates two folders" (`_bmad/`, `_bmad-output/`), while the code also writes `.claude/skills/bmad-*` and `docs/` (W02 s7.3); the main-branch install page now documents the v7 preview, not the v6 flow the pin uses, so the 6.9.0 flow must be cited from the `v6.9.0` tag (W02 s6).

### 4.4 Design and owner questions carried to Sections 8 and 9

These are not evidence gaps. They are listed so that nothing from the log is lost; none is answered here.

| IDs | Question | Goes to |
|---|---|---|
| Owner Q1 | Is a user-level bootstrap artifact allowed (a content-free stub under `~/.claude/` that only starts the per-project install)? Options B and D put one in user scope; option C does not | Section 9 (owner) |
| Owner Q2 | What counts as "first use": a `bmad` command (C), a BMAD slash skill (B) or opening a session (D)? | Section 9 (owner) |
| G-26, D-10 | Hide first-use files with `info/exclude` or leave them visible; does the decision cover Orca-created worktrees? | Section 9 (owner) |
| D-1, D-2, D-6 | Atomic `_bmad/` creation; guard on `_bmad/config.toml` rather than `_bmad/`; revisit failed-install behaviour (`install.sh:41, 24`) | Section 8 |
| D-3 | Which directory is "the project" for a subfolder session | Sections 8, 9 |
| D-4, D-5 | Cover the `minimal` profile; deselection cleanup for a user-level artifact versus the "marker never removed" rule | Sections 8, 9 |
| D-7, D-17 | Renovate-visible strings if `install.sh` is rewritten; which of the three extraction sites the chosen option touches | Section 8 |
| D-8 | Whether the 60 s and 75 s boot bounds matter for a new boot step (not for B3, D3 or any step outside the ironclaude slug) | Section 8 |
| D-9, D-11 | The decision covers boot unchanged and adds first use after boot; the deselected-marker question stays separate | Section 9 |
| D-12, D-13, D-15 | Stub written without a seed needs the replacement assertion at R04 A.11; owner preference for variants with no certain break (B2, B3, C, D2, D3); a new test row for the new behaviour | Sections 7, 8 |
| D-14 | Health and Configured for a user-created project (F-07) | Sections 8, 9 |
| D-16 | Name which prior-diagnosis positions the Recommendation overrides; keep the three-way split of the original ask | Section 7 |

### 4.5 Severity roll-up

| Table | Critical | Important | Minor | Total |
|---|---|---|---|---|
| 4.1 Functional gaps (F-01 to F-11) | 1 | 10 | 0 | 11 |
| 4.2 Gaps log (G-01 to G-30) | 0 | 15 | 15 | 30 |
| 4.3 Corrected documentation claims (26 grouped rows covering CC-01 to CC-30 and SD-01 to SD-13) | 0 | 6 | 20 | 26 |

The Important rows in 4.2 are G-01 to G-10, G-13, G-16, G-19, G-24 and G-26. The log's own summary counts 14 open Important gaps because G-24 is resolved by fix; it is rated Important in the table and kept. The Important rows in 4.3 are CC-01, SD-02, CC-14, CC-17, CC-22 and CC-25.

Facts that only a real fresh 6.9.0 install run could show (GL section 7, R-1 to R-15) are items for CI observation in the implementation phase, because this task ran no `bmad install` and the project rule is validation through `.github` Actions. They map to the gaps above as follows:

| Run-only fact | Gap | Run-only fact | Gap |
|---|---|---|---|
| R-1 duration in a workspace and a large repo, with live network | G-09 | R-9 outcome of `--user-name` without `--output-folder` | G-14 |
| R-2 HOME writes, `npm view` and `uv --version` side effects | G-15 | R-10 state left by a failed first run; quick-update on it | G-13 |
| R-3 behaviour with no `.git` | G-10 | R-11 the manual command at `manifest.yaml:13-14` end to end | G-16 |
| R-4 exact per-file list, `{output_folder}` substitution | G-10 | R-12 what `bmad install --directory ~` writes | G-16 |
| R-5 skill set, count and names (46 versus 47) | G-11 | R-13 quick-update rewrites and 6.9.0-over-6.10.0 changes | G-14 |
| R-6 update banner under `NPM_CONFIG_OFFLINE=true` | G-15 | R-14 seed-repo boot result; a fresh workspace's `~/.claude/` | G-27, G-21 |
| R-7, R-8 `resolve_customization.py` with no `_bmad/`; missing config keys; which file `--set` patches | G-07 | R-15 layer count and Sysbox job after the chosen option is built | G-19 |

## 5. External Research Findings

**All findings in this section are external context** from official documentation, package tarballs and project trackers, fetched on 2026-11-07 and 2026-11-08. They are not code observations of this repository. Where an external statement and the codebase disagree, the codebase wins (research rule 6). Provenance for both web files: `provider=WebSearch/WebFetch reason=tavily-unavailable` (no Tavily tool was available to the agents). The WebFetch tool returns a summary made by a small model, so quoted strings are as returned by it; web-02 cross-checked the important GitHub items against raw API output and the npm tarballs.

Relationship values below mean: supports = agrees with a codebase finding; extends = adds a fact the codebase files left UNVERIFIED; contradicts = disagrees with a codebase finding.

### 5.1 Claude Code user-level skills, hooks and live reload

Source group: official Claude Code documentation at `code.claude.com/docs/en/`. Claude Code behaviour in the docs is gated by versions (up to v2.1.314 are mentioned). The version shipped in the Coder image is not established; `claude --version` printed `2.1.319` in the web-01 agent's workspace (an observation, not a statement about the image). Every statement below holds for the docs as fetched on 2026-11-08.

**Skill discovery, ranking and live pickup**

- **Finding W01-1:** a personal skill at `~/.claude/skills/<skill-name>/SKILL.md` is available to "all your projects on this machine"; a project skill at `.claude/skills/<skill-name>/SKILL.md` to sessions in that repository; enterprise skills come from the managed settings directory; plugin skills are namespaced.
  - Source URL: https://code.claude.com/docs/en/skills ("Choose where skills load")
  - Relevance: HIGH
  - Relationship to codebase: extends (answers GL G-02 / UV-07; a user-level stub would appear in every project, including projects that have no BMAD)
- **Finding W01-2:** on a name collision "Enterprise over personal, and personal over project", so `/deploy` runs the personal copy when both exist; a skill beats a same-named `.claude/commands/` file. A user-level stub named like a BMAD skill (for example `bmad-help`) would shadow the project copy that `bmad install` writes. The shadowing is W01's inference from the quoted rule, not tested.
  - Source URL: https://code.claude.com/docs/en/skills ("Resolve skills that share a name")
  - Relevance: HIGH
  - Relationship to codebase: extends (R03 A3 B step 5 and R01 U7 left the ranking UNVERIFIED; the installer itself would not object because the ancestor check is off, R01 s6)
- **Finding W01-3:** Claude Code watches skill directories and picks up an added, edited or removed skill under `~/.claude/skills/`, the project `.claude/skills/` or an `--add-dir` directory within the current session. Exception: "If you create a top-level skills directory that didn't exist when the session started, run `/reload-skills` to pick up the skills you put there"; that directory is not watched until then. Live detection covers `SKILL.md` text only. In a project that never had BMAD, `.claude/skills/` usually does not exist, so first use inside an open session needs `/reload-skills` or a restart.
  - Source URL: https://code.claude.com/docs/en/skills ("Edit a skill during a session")
  - Relevance: HIGH
  - Relationship to codebase: extends (answers GL G-01 / Q-1 with a split answer; R03 gap 9 recorded "skills docs not fetched")
- **Finding W01-4:** project skills load from `.claude/skills/` in the directory where Claude Code starts and in every parent up to the repository root; a `.claude/skills/` below the start directory does not load at startup and loads when a file there is read or edited, or after `/add-dir` (v2.1.257 or later).
  - Source URL: https://code.claude.com/docs/en/skills ("Load skills in monorepos and subdirectories")
  - Relevance: MEDIUM
  - Relationship to codebase: extends (bears on GL D-3: an install at the repository root is found from a subfolder session; an install into a subfolder is not found from the root until a file there is read)
- **Finding W01-5:** custom commands have merged into skills: a `.claude/commands/deploy.md` file and a `.claude/skills/deploy/SKILL.md` both create `/deploy`; existing command files keep working. A user-level command is therefore no cheaper than a user-level skill for a bootstrap stub. An explicit `~/.claude/commands/` row was not in the skills page text; the claude-directory page lists `commands/*.md` under `~/.claude/` and `.claude/` as "Project and global" (URL below).
  - Source URL: https://code.claude.com/docs/en/skills (opening note); https://code.claude.com/docs/en/claude-directory
  - Relevance: MEDIUM
  - Relationship to codebase: extends (option B: a command and a skill are discovered the same way)

**Running a command from a skill**

- **Finding W01-6:** a skill can bundle scripts (referenced with `${CLAUDE_SKILL_DIR}`) and can pre-approve tools with `allowed-tools: Bash(<pattern>)` for the turn that invokes it. The `` !`<command>` `` form runs a shell command before the skill text reaches Claude. Injected commands "never prompt for permission while the skill renders" and abort the invocation unless an allow rule or `allowed-tools` matches (outside auto mode); deny and ask rules still win; `disableSkillShellExecution: true` switches the feature off. A Bash call made by Claude after reading the skill prompts by default except for a built-in read-only set.
  - Source URL: https://code.claude.com/docs/en/skills ("Inject dynamic context", "Pre-approve tools for a skill"); https://code.claude.com/docs/en/permissions ("Permission system")
  - Relevance: HIGH
  - Relationship to codebase: extends (R03 A3 shared facts expected a prompt and marked it UNVERIFIED; the install command through a stub prompts unless pre-approved, which is a visible consent step). Residual UNVERIFIED: the exact `Bash(...)` pattern grammar for the install command; whether the image sets `disableSkillShellExecution`
- **Finding W01-7:** the docs do not forbid a skill or hook from modifying the project directory and describe skills whose work writes files ("The skill's edits to other files stay, so use git to revert them"; a skill that writes `.claude/skills/verify/SKILL.md` at the repo root).
  - Source URL: https://code.claude.com/docs/en/skills ("Run and verify your app", "Run skills in a subagent")
  - Relevance: MEDIUM
  - Relationship to codebase: supports (nothing contradicts the finding that the BMAD install writes only inside the project, R01 s5)

**Hooks: inputs, outputs, timing, reload**

- **Finding W01-8:** a command hook receives JSON on stdin with `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`; SessionStart adds `source` (`startup`, `resume`, `clear`, `compact`, `fork`); UserPromptSubmit adds `prompt`; `CLAUDE_PROJECT_DIR` ("the project root where the session started") is exported to the hook process. `cwd` and `CLAUDE_PROJECT_DIR` can differ; how they differ in a Coder workspace is UNVERIFIED.
  - Source URL: https://code.claude.com/docs/en/hooks ("Common input fields", "SessionStart", "UserPromptSubmit", "Reference scripts by path")
  - Relevance: HIGH
  - Relationship to codebase: extends (GL G-08 and D-3: the hook should read `CLAUDE_PROJECT_DIR` for "the project" and treat `cwd` as a hint)
- **Finding W01-9:** SessionStart and UserPromptSubmit add plain-text stdout (or `hookSpecificOutput.additionalContext`) to Claude's context; Claude never sees stderr from a hook that exits 0. SessionStart has "No blocking or decision control"; UserPromptSubmit and PreToolUse can block. Whether SessionStart stdout is also shown to the user is not stated: UNVERIFIED.
  - Source URL: https://code.claude.com/docs/en/hooks ("Exit code 0", "SessionStart", "UserPromptSubmit", "PreToolUse")
  - Relevance: HIGH
  - Relationship to codebase: extends (R03 A3 D step 2 and step 3 left the display of hook output UNVERIFIED; a hook can tell Claude that the project lacks BMAD without blocking anything)
- **Finding W01-10:** command-hook `timeout` defaults are 600 s, lowered to 30 s on UserPromptSubmit; a SessionStart hook runs in the background in an interactive session, so typing is possible, but Claude's first response waits for the hooks to finish.
  - Source URL: https://code.claude.com/docs/en/hooks ("Common fields", "SessionStart decision control")
  - Relevance: HIGH
  - Relationship to codebase: extends (R03 A3 D step 2 noted all 29 timeouts in this workspace's `settings.json` are 1 to 10 s; the 30 s UserPromptSubmit default is the tighter bound for a first install whose real duration is UNVERIFIED, GL G-09)
- **Finding W01-11:** a SessionStart hook can return `{"hookSpecificOutput":{"hookEventName":"SessionStart","reloadSkills":true}}`, which makes Claude Code re-scan skill and command directories after the SessionStart hooks complete; the docs say files a hook writes into `~/.claude/skills/` or `.claude/skills/` can otherwise be missing at the first prompt. This is the only documented way to make freshly written project skills visible in the same session without the user typing `/reload-skills`. No equivalent field was found for UserPromptSubmit.
  - Source URL: https://code.claude.com/docs/en/hooks ("SessionStart decision control", "Reload skills that a hook installs")
  - Relevance: HIGH
  - Relationship to codebase: extends (changes how option D should be shaped: SessionStart plus `reloadSkills`, not UserPromptSubmit)
- **Finding W01-12:** `reloadSkills` was introduced in Claude Code v2.1.152 according to a user-authored issue that quotes the changelog; the number could not be reproduced in first-party text.
  - Source URL: https://github.com/anthropics/claude-code/issues/62664
  - Relevance: MEDIUM
  - Relationship to codebase: extends (Claude Code version in the image UNVERIFIED; secondary source, lower reliability)
- **Finding W01-13:** edits to `hooks` in settings files are picked up by the file watcher in a running session; a settings file created mid-session loads if its folder existed at start, and for the project `.claude/` folder even if the folder is created in that session. This differs from skills (W01-3).
  - Source URL: https://code.claude.com/docs/en/settings ("When edits take effect"); https://code.claude.com/docs/en/hooks ("Disable or remove hooks")
  - Relevance: MEDIUM
  - Relationship to codebase: supports (R03 s6 recorded this doc-sourced and UNVERIFIED, UV-42; closed from official text, not tested live)
- **Finding W01-14:** "Command hooks execute shell commands with your full user permissions. They can modify, delete, or access any files your user account can access." Hooks run by Claude Code itself and not through the Bash tool; that a command hook therefore runs without a Bash permission prompt is the best reading, but no sentence says it.
  - Source URL: https://code.claude.com/docs/en/hooks ("Security considerations")
  - Relevance: HIGH
  - Relationship to codebase: extends (GL G-04: a hook removes the user's chance to say no, R03 A3 D step 2)

**Hook scopes, managed settings, trust**

- **Finding W01-15:** hooks in `~/.claude/settings.json` apply to "all your projects"; user, project, local and managed hook entries merge rather than replace; an identical handler defined twice runs once; matching hooks run in parallel.
  - Source URL: https://code.claude.com/docs/en/hooks ("Hook locations", "Hook handler fields"); https://code.claude.com/docs/en/settings ("Settings files and who they affect")
  - Relevance: HIGH
  - Relationship to codebase: supports (R03 s5 found that `superclaude install` merges hooks additively; a user-level hook fires in every project, including repositories where BMAD must not be installed, so the hook must carry the "is this a project that wants BMAD, and does it lack `_bmad/`" test)
- **Finding W01-16:** `/etc/claude-code/managed-settings.d/*.json` is a documented location, merged after `managed-settings.json` in alphabetical order (single values replace, lists combine without duplicates, nested blocks merge by key); `hooks` is a list-merged key and managed policy is a documented hook location. No single sentence says a drop-in may hold `hooks`: documented by inference. Managed hooks cannot be disabled by the user's `disableAllHooks`.
  - Source URL: https://code.claude.com/docs/en/managed-settings ("Split a file-based policy across teams", "How Claude Code combines managed sources"); https://code.claude.com/docs/en/hooks ("Hook locations")
  - Relevance: HIGH
  - Relationship to codebase: extends (answers GL G-03 / UV-25 half for option D2; the existing drop-in `10-retention.json` sets only `cleanupPeriodDays`, R03 s4)
- **Finding W01-17:** two managed keys would remove user-level customisation: `allowManagedHooksOnly` restricts which hooks run, and `strictPluginOnlyCustomization` blocks skills, agents, hooks and MCP servers from user and project sources. If a file under `/etc/claude-code/` in the Coder image set either key, options B and D would stop working. Remote managed settings are fetched only when the session authenticates to Anthropic's API directly or through a gateway; whether a Coder workspace sets `ANTHROPIC_BASE_URL` was not established.
  - Source URL: https://code.claude.com/docs/en/managed-settings ("How Claude Code combines managed sources")
  - Relevance: MEDIUM
  - Relationship to codebase: extends (the image's `/etc/claude-code/` content is a codebase check, not an external one; only `10-retention.json` is known)
- **Finding W01-18:** in an interactive session Claude Code holds back hooks from every settings file, including `~/.claude/settings.json`, until the user accepts the workspace trust dialog for the folder or a parent whose trust extends to it; `-p` and SDK sessions treat the folder as trusted. A user-level SessionStart hook therefore does not run in a never-trusted folder until trust is accepted. Whether a held-back hook runs later in the same session is not stated: UNVERIFIED. Skills are not gated the same way ("Workspace trust never gates a skill's `allowed-tools` in any session").
  - Source URL: https://code.claude.com/docs/en/hooks ("Security considerations", "Workspace trust"); https://code.claude.com/docs/en/permissions ("What runs before you trust a folder")
  - Relevance: HIGH
  - Relationship to codebase: extends (a new constraint on option D that no codebase file considered; it applies to project-level hooks too, so no hook-based option escapes it)

**Other**

- **Finding W01-19:** every skill in the listing adds to context on every turn, so a user-level stub adds one listing entry to every project.
  - Source URL: https://code.claude.com/docs/en/skills
  - Relevance: LOW
  - Relationship to codebase: extends (cost of a user-level artifact, GL G-02 blast radius)

Not answered by official sources (UNVERIFIED): timing of a held-back hook after trust is accepted; whether SessionStart stdout is shown to the user; the meaning of `skipDangerousModePermissionPrompt`; whether the Orca `PermissionRequest` hook decides permissions (not a Claude Code docs question); the Bash permission pattern grammar for the install command; first-party text for the `reloadSkills` version. Discrepancies with the codebase findings: none CODE-CONTRADICTED (W01 "Discrepancies" section); the log's Q-1 ("the settings page does not say") is answered by the skills page.

### 5.2 Upstream BMAD-METHOD user-scope and new-project install

Source group: the npm registry, the published `bmad-method` tarballs, the GitHub REST API and raw files of `bmad-code-org/BMAD-METHOD`, and the project's documentation. The web-02 agent used read-only `curl` GET requests; it ran no `npm`, `npx` or installer, and extracted tarballs only into `/tmp/web02-*` directories outside any repository. Only the 6.9.0, 6.10.0 and 6.12.4 tarballs were searched. Not read: community posts, blog posts and forum threads (low reliability), the `-next` prereleases, the `V6.12` branch source.

**Versions and the user-scope question**

- **Finding W02-1:** `bmad-method` `latest` is 6.12.4 (published 2026-10-14); 6.9.0 (this repo's pin) was published 2026-06-22; stable lines after it are 6.10.0 (2026-07-03), 6.11.0 (2026-08-10), 6.12.0 (2026-09-04), 6.12.1 (2026-10-04), 6.12.2 (2026-10-11), 6.12.3 and 6.12.4 (both 2026-10-14). The "Update Available 6.12.4" banner seen in the CLI is therefore genuine. All of these require Node `>=20.12.0`, the same as 6.9.0.
  - Source URL: https://registry.npmjs.org/bmad-method
  - Relevance: HIGH
  - Relationship to codebase: extends (answers the existence half of GL G-05 / UV-20, which R02 U2 and R01 U9 left UNVERIFIED)
- **Finding W02-2:** the token `global_target_dir` appears in exactly one file, `tools/installer/ide/platform-codes.yaml`, with 43 hits in 6.9.0, 43 in 6.10.0 and 46 in 6.12.4; no `.js` file in any of the three packages reads it. The 6.12.4 header still describes it as "User-home directory for global install". No published release up to 6.12.4 implements a user-scope or global skill install. A newer pin of `bmad-method` therefore does not make option F available.
  - Source URL: https://registry.npmjs.org/bmad-method/-/bmad-method-6.9.0.tgz, https://registry.npmjs.org/bmad-method/-/bmad-method-6.10.0.tgz, https://registry.npmjs.org/bmad-method/-/bmad-method-6.12.4.tgz (Grep of the extracted packages)
  - Relevance: HIGH
  - Relationship to codebase: supports (R01 s2: 43 hits, one file, zero consumers in 6.9.0), and extends it to 6.10.0 and 6.12.4. Not searched: the 6.11.0 and 6.12.0 to 6.12.3 tarballs individually; 6.12.4 is the newest package and shows no consumer
- **Finding W02-3:** the `install` command options in 6.12.4 (`commands/install.js:12-53`) differ from 6.9.0 (`:12-51`) only by `--shims` and `--no-shims`; neither version has a `--global`, `--user`, `--scope` or `--home` flag. The word "scope" in the installer code means team-scope versus user-scope CONFIG keys (`_bmad/config.toml` against `_bmad/config.user.toml`), not an install location. Other `os.homedir()` uses in 6.12.4 are module caches under `~/.bmad/cache/` and `~` expansion of typed paths.
  - Source URL: https://registry.npmjs.org/bmad-method/-/bmad-method-6.12.4.tgz (`tools/installer/commands/install.js`, `set-overrides.js`, `external-manager.js`)
  - Relevance: HIGH
  - Relationship to codebase: supports (R01 s1 and s4: no scope flag; HOME touched only for caches). Trap for later research: release notes or issue titles that mention "user scope" mean config keys
- **Finding W02-4:** `global_target_dir` was added to every platform as data "for parity with the Vercel skills ecosystem" (issue #2313: "`global_target_dir` added to every platform (XDG for Crush; tool-specific for Codex; shared `~/.agents/skills/` for 11 platforms)"), never wired to an install option in 6.x.
  - Source URL: https://github.com/bmad-code-org/BMAD-METHOD/issues/2313
  - Relevance: MEDIUM
  - Relationship to codebase: supports (R01 SD-01: the field is inert data; the origin confirms it)

**Release notes and installer behaviour after 6.9.0**

- **Finding W02-5:** none of the eight release notes from 6.9.0 to 6.12.4 announces a global or user-level install; the only user-home skill paths named (CodeWhale, Antigravity CLI) are platform-table data in the same inert field.
  - Source URL: https://api.github.com/repos/bmad-code-org/BMAD-METHOD/releases?per_page=30; https://github.com/bmad-code-org/BMAD-METHOD/releases/tag/v6.12.4 (and the same pattern for the other tags)
  - Relevance: HIGH
  - Relationship to codebase: supports (R01 s2, s5)
- **Finding W02-6:** install-affecting changes after 6.9.0, quoted from the release bodies: 6.12.2 "`install --yes` without `--directory` installs into the current directory instead of stopping at a prompt (#3064)"; 6.11.0 "`--set core.<key>` overrides were applied too late (#2671)... artifact paths and the created directory still used `_bmad-output/`"; 6.11.0 core-only installs; 6.12.0 "Deprecated shims are opt-in on fresh installs. Pass `--shims`"; 6.12.1 user-scope key defaults now live in `config.toml` so skills render on a fresh clone without `config.user.toml` (#3016); 6.9.0 and 6.11.0 "a missing `uv` warns... never blocks" (from 6.11.0 the Build variants halt without `uv`). The 6.12.2 wording implies that 6.9.0 without `--directory` stopped at a prompt; our command always passes `--directory`. That 6.9.0 behaviour is UNVERIFIED (not run).
  - Source URL: https://api.github.com/repos/bmad-code-org/BMAD-METHOD/releases?per_page=30
  - Relevance: HIGH
  - Relationship to codebase: supports (R01 s3.2: `--directory` avoids the directory prompt; `--output-folder _bmad-output` stays in every command; `uv` is advisory in 6.9.0) and extends (explains `--set` ordering for GL G-07 and G-14). A pin bump would need its own plan, Renovate handling and a CI run (GL D-7)
- **Finding W02-7:** the 6.9.0 skills run their config resolver as `python3 {project-root}/_bmad/scripts/...` (41 lines in 31 `SKILL.md`, re-observed on the tarball); 6.12.4 skills use `uv run` (105 lines in 39 files, 0 `python3 `). The 6.12.4 `bmm-skills` layout differs (`agents/`, `plan/`, `ship/`, `v6-shims/` instead of `1-analysis/` to `4-implementation/`).
  - Source URL: https://registry.npmjs.org/bmad-method/-/bmad-method-6.9.0.tgz and https://registry.npmjs.org/bmad-method/-/bmad-method-6.12.4.tgz (Grep count of `SKILL.md`)
  - Relevance: MEDIUM
  - Relationship to codebase: supports (R03 A1: 41 lines in 31 files) and extends (GL G-06: a bump would remove the interaction with the UV-only hook at the price of a changed skill set and tree layout; a trade-off for the owner, not a first-use mechanism)
- **Finding W02-8:** 6.12.4 skill text tolerates a failed resolver call ("Missing keys -> neutral defaults; never block" in `bmad-prd` and `bmad-ux`; "On failure or missing values -> neutral defaults; never block" in `bmad-brainstorming`; `bmad-customize`: script missing -> continue). `bmad-help` reads `{project-root}/_bmad/_config/bmad-help.csv` and has no stated behaviour when `_bmad/` is absent. Whether a model completes a session with no `_bmad/` at all is UNVERIFIED.
  - Source URL: https://registry.npmjs.org/bmad-method/-/bmad-method-6.12.4.tgz (`src/bmm-skills/plan/bmad-prd/SKILL.md:22`, `src/core-skills/bmad-brainstorming/SKILL.md:23`, `src/core-skills/bmad-customize/SKILL.md:17`, `src/core-skills/bmad-help/SKILL.md:25-26`)
  - Relevance: MEDIUM
  - Relationship to codebase: extends (R01 s7.4: in 6.9.0 no skill detects a missing `_bmad/`)

**Documented install flow for a new project**

- **Finding W02-9:** the 6.9.0 install guide (at the tag of this repo's pin) says: run `npx bmad-method install` in the project directory, or headless `install --yes --modules <list> --tools claude-code [--directory <path>]`; `--tools` is required for fresh `--yes` installs; `--directory` defaults to the working directory; a re-run where `_bmad/` exists defaults to quick-update under `--yes`; `--set <module>.<key>=<value>` is a post-install patch into `_bmad/config.toml` or `_bmad/config.user.toml` and `_bmad/<module>/config.yaml`; a single install calls the GitHub API once per external module, anonymous calls capped at 60 per hour per IP. The guide says nothing about an empty directory, a directory with no `.git`, a global install, `~/.claude`, or install on demand.
  - Source URL: https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.9.0/docs/how-to/install-bmad.md
  - Relevance: HIGH
  - Relationship to codebase: supports (R01 s1, s3.2: flags and the quick-update default) and extends (documentation-level answer to GL G-07 on which files `--set` patches; documents the external-module rate limit behind GL G-12). The empty-directory and no-`.git` behaviour stay UNVERIFIED (GL G-10)
- **Finding W02-10:** the 6.9.0 getting-started tutorial says the installer "creates two folders: `_bmad/`... `_bmad-output/`" and sends the new user to the `bmad-help` skill after the install.
  - Source URL: https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.9.0/docs/tutorials/getting-started.md
  - Relevance: MEDIUM
  - Relationship to codebase: contradicts in part: the code also writes `.claude/skills/bmad-*` and an empty `docs/` (R01 s4). The tutorial is incomplete, not wrong; the code finding stands
- **Finding W02-11:** the install page on the main branch now documents the v7 preview alpha and says of the v6.12 flow "The rest of this page does not apply to v6.12"; v6.12 remains the stable line with the same project-level `npx bmad-method install`. A reader who follows "the documented install flow" on the website gets the v7 flow, not the one the pin uses; the 6.9.0 flow must be cited from the `v6.9.0` tag.
  - Source URL: https://docs.bmad-method.org/start/install-bmad/; https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/start/install-bmad.md
  - Relevance: HIGH
  - Relationship to codebase: contradicts the assumption that "the documented install flow" is the v6 flow (an assumption in the option list, not a code finding); the repo's own `manifest.yaml:14` flow is the v6 one

**v7 preview, upstream issues, plugin channel**

- **Finding W02-12:** the v7 preview installs skills with the Skills CLI (`npx skills add bmad-code-org/BMAD-METHOD ...`, `-g` for a user directory, project scope by default) and creates the project's `_bmad/` through an explicit `bmad setup` step of the hub skill. Upstream's own design is offer-and-ask: `setup_check.py:67` returns only dependency notes when `_bmad/` is absent, and the "Offer to run `bmad setup`" messages fire only when `_bmad/` already exists but a module's questions or scripts are missing; a first setup runs when the user asks for it. It requires `uv`, and it is an alpha with breaking changes, not reachable by any `bmad-method@<version>` pin. It also defines `{project-root}` as the nearest folder containing `_bmad/`.
  - Source URL: https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/reference/skills-and-agents.md; https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad/SKILL.md; https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad/references/setup.md; https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad/scripts/setup_check.py; https://github.com/vercel-labs/skills/blob/main/docs/commands.md
  - Relevance: HIGH
  - Relationship to codebase: extends (validates the shape of options B and D, "skills present" separate from "project runtime present", but not full automation: upstream asks first; the `main` branch has no `tools/installer/` directory, so the 6.x installer lives only in published 6.x tarballs and the `V6.12` branch)
- **Finding W02-13:** issue #2677 reports exactly the first-use gap: skills installed user-wide through the Claude Code plugin marketplace run `{project-root}/_bmad/scripts/resolve_customization.py`, a path "only the npx installer creates". The reporter counted 80 call sites at 6.10.0, 26 with a documented fallback; `resolve_config.py` "does not degrade" (exit 1 without `_bmad/config.toml`). The maintainer closed it as fixed by redesign (v7 flat `skills/` tree via `npx skills` and plugin marketplaces, installer removed); no first-use bootstrap was added to any 6.x release.
  - Source URL: https://github.com/bmad-code-org/BMAD-METHOD/issues/2677
  - Relevance: HIGH
  - Relationship to codebase: supports (R01 s7: `resolve_config.py` exits 1 and `resolve_customization.py` falls back; no skill detects a missing `_bmad/`), independent upstream evidence
- **Finding W02-14:** issue #2624 (open) raises a trust concern: every skill's first step executes a Python script located inside the project being worked on, and the skill cannot tell an installer-written resolver from one a repository committed; any mechanism that creates `_bmad/` in a repository should be explicit and visible.
  - Source URL: https://github.com/bmad-code-org/BMAD-METHOD/issues/2624
  - Relevance: MEDIUM
  - Relationship to codebase: extends (an image-baked, version-pinned installer, as in this repo, answers it for our case, W02 recommendation 3)
- **Finding W02-15:** issue #1852 (a request for a global framework install) was closed as completed on 2026-04-29 with a workaround: install BMAD once in a workspace folder with the project folders underneath and launch the agent from the workspace. That is a variant of option E restricted to a workspace directory rather than `~`.
  - Source URL: https://github.com/bmad-code-org/BMAD-METHOD/issues/1852
  - Relevance: HIGH
  - Relationship to codebase: extends (supports the owner's "never globally" stance as the upstream default; whether it works with this repo's layout depends on how 6.9.0 skills find `{project-root}`, and repositories with their own `.git` are UNVERIFIED, GL G-16)
- **Finding W02-16:** the 6.x tarballs include a Claude Code plugin channel (`.claude-plugin/marketplace.json`; in 6.9.0 two plugins at version 6.8.0 with 12 and 33 skills; in 6.12.4 one plugin with 28 skills). It installs user-wide skills in Claude Code's plugin cache and, per #2677, does not create `_bmad/`. It is therefore not a first-use solution; it leaves exactly the gap this task closes.
  - Source URL: https://registry.npmjs.org/bmad-method/-/bmad-method-6.9.0.tgz (`.claude-plugin/marketplace.json`); https://github.com/bmad-code-org/BMAD-METHOD/issues/2677
  - Relevance: MEDIUM
  - Relationship to codebase: extends (whether this route counts as "user level" is the owner question in GL section 5 item 1; the skill counts do not settle the 46 versus 47 question, GL G-11)
- **Finding W02-17:** no upstream document or release note describes bootstrap-on-first-use or install-on-demand for 6.x. The only skill documented as standalone is `bmad-project-context` (6.11.0 and later: "it runs standalone with no BMad install"); it is not in the 6.9.0 skill set. A GitHub issue search for `global_target_dir` returned five platform-table pull requests and none about a consumer; the search API returns only the 10 to 12 most recently updated items per query, so older matches may exist.
  - Source URL: https://api.github.com/repos/bmad-code-org/BMAD-METHOD/releases?per_page=30; https://github.com/bmad-code-org/BMAD-METHOD/issues/2677
  - Relevance: HIGH
  - Relationship to codebase: supports (R01 s7.4: any first-use bootstrap has to come from outside BMAD)
- **Finding W02-18:** issue #3016 (fixed in 6.12.1) shows an upstream example of an incomplete first-use state producing a HALT: with `_bmad/` committed but the gitignored `config.user.toml` absent, `bmad-build` and `bmad-build-auto` stopped with "missing config value communication_language". Those skills are not in the 6.9.0 set.
  - Source URL: https://github.com/bmad-code-org/BMAD-METHOD/issues/3016
  - Relevance: LOW (MEDIUM if the pin is bumped)
  - Relationship to codebase: extends (not a current risk for the 6.9.0 pin)

### 5.3 External Research Summary

External research answered all five questions the codebase left to web research (GL section 4 and G-01 to G-05) and closed none of them completely. Every external fact is context; the codebase findings remain the source of truth.

| Open question | External answer | Findings | Residual UNVERIFIED |
|---|---|---|---|
| G-01 / Q-1: are skills created after the session started loaded? | Split: an existing watched `.claude/skills/` picks them up live; a new top-level directory needs `/reload-skills` or a restart; a SessionStart hook can return `reloadSkills` | W01-3, W01-11 | Prompt-time rescan without the user; Claude Code version in the image |
| G-02 / Q-2: user-level skills in every project, and ranking | Yes for all projects on the machine; personal beats project on a name collision | W01-1, W01-2, W01-19 | Managed keys that would disable user-level skills and hooks in this image |
| G-03: drop-in hooks | Documented by inference, list-merged, additive to user hooks, not user-disableable | W01-15, W01-16, W01-17 | No single explicit sentence; `test-73` with a second file |
| G-04: hook and permission runtime | Live reload of hooks, stdout as context, timeouts 600 s and 30 s, trust hold-back in interactive sessions, default Bash prompt | W01-8 to W01-10, W01-13, W01-14, W01-18 | Held-back hook timing; display of SessionStart output; `skipDangerousModePermissionPrompt` |
| G-05 / Q-3: later upstream user-scope install | None through 6.12.4; 6.12.4 exists; the only user-scope pattern is the v7 preview, a different channel | W02-1 to W02-5, W02-11, W02-12 | Individual 6.11.0 and 6.12.0 to 6.12.3 tarballs, `-next`, `V6.12` branch |
| G-06 (part) bare `python3` steps | 6.12.4 uses `uv run` with no `python3 ` lines | W02-7 | Model emission and a fresh workspace's hook registration (codebase gap) |
| G-07, G-12, G-14 (part) | Documentation-level answers for `--set` targets and the external-module rate limit; release note #2671 on `--set` ordering | W02-6, W02-9 | Observation in CI |
| G-16 (part) option E | Upstream's declined-request workaround is an install at a parent workspace folder | W02-15 | Repos with their own `.git` |

What the external facts change for the option comparison (inputs for Section 6, not a recommendation):

- **Option F:** no code path through 6.12.4; a pin bump does not enable it; the v7 preview is a different product shape, channel and runtime layout (W02-2, W02-12).
- **Option D:** a SessionStart hook with `reloadSkills` is the only documented way to show new project skills in the same session; UserPromptSubmit has a 30 s default timeout and no rescan field; an interactive session holds the hook back until workspace trust is accepted; a managed (D2) hook cannot be switched off by the user; any user-level hook fires in every project (W01-8 to W01-11, W01-15, W01-16, W01-18).
- **Option B:** a stub must not reuse a `bmad-*` name (personal beats project); it runs the install through a permission prompt unless `allowed-tools` pre-approves it, and the user then needs `/reload-skills` or a restart because a new `.claude/skills/` directory is not watched; it is not gated by workspace trust (W01-2, W01-3, W01-6, W01-18).
- **Option C:** unaffected by Claude Code behaviour; it fires only when a `bmad` process runs (R02 s6.2, an inference marked UNVERIFIED there).
- **Option E:** upstream's own workaround is a parent-folder install; it conflicts with K-01 when the folder is HOME (W02-15).
- **Pin bump:** not needed for first-use creation; it would change the skill set and layout, move skills to `uv run`, make `--yes` without `--directory` install into the working directory, make deprecated names opt-in and require `uv` for Build variants (W02-6, W02-7).

Contradictions: none of the 19 web-01 findings is CODE-CONTRADICTED by a codebase file (W01 "Discrepancies"). Two web-02 items disagree with a codebase-adjacent statement and neither overturns a code finding: the 6.9.0 tutorial's "two folders" (W02-10) and the main-branch install page that documents v7 (W02-11). The two web files do not contradict each other. The web-02 draft sentence that 6.9.0 had no `config.user.toml` layer was corrected inside the file: the 6.9.0 installer code mentions `config.user.toml` 17 times in 5 files (W02 s5 item 2 (iii)).

Limits: WebFetch results are small-model summaries; the Claude Code version in the Coder image is not established; community material was not read; the `reloadSkills` introduction version comes from a user-authored issue only. No external statement was used to describe the architecture of this repository.

## Self-Audit (not a report section)

**What I actively checked.**

- Read in full, by the Read tool in this session: `gaps-and-questions.md`; `research/01` to `research/05` including their fix-cycle addenda; `research/research-notes.md` including addendum F9; `research/web-01-...md`; `research/web-02-...md`; `qa/qa-gate1-decision.md` (for the G-30 exception); `synthesis/synth-01-problem-current-state.md` (header stub only at read time). The gaps log ("How this log was built") reports that a Glob found no `research/*.addendum.json`; I did not repeat a Glob for `.json` files, but every addendum heading is inside the files I read, and my Glob of the task folder listed only `.md` files in `research/`.
- Summary and Key Takeaways sections read for every assigned file: R01 (per-section Key Takeaways, Summary, F5-H), R02 (Key Takeaways (a) to (e), A8), R03 (per-section Key Takeaways, section 7, Summary, addendum Summary), R04 (Key Takeaways 1 to 6, section 9, Summary, addendum summary), R05 (Key Takeaways (a) to (e), Summary, F1.6), W01 (Key External Findings, Recommendations, Summary), W02 (Key External Findings, Recommendations, Summary), GL (Summary, section 6).
- Counts re-derived by me from the tables I wrote: 11 functional gaps (1 Critical, 10 Important); 30 log gaps (15 Important, 15 Minor); 26 grouped documentation rows covering all 30 CC IDs and all 13 SD IDs; 16 success criteria; 12 constraints; 19 web-01 findings; 18 web-02 findings. The log's own summary says 14 Important because it excludes the resolved G-24; this synthesis keeps G-24 as Important and says so.
- Searches: only Glob (task folder listing) and `wc -c` on the input files; I ran no Grep over the research text because each file was read in full. No command was run against BMAD, git or the product code, and no product file was opened except the files named above.

**Key findings traced.** Each research file's strongest findings and where they landed: R01 per-project install and no HOME writes (SC-01, SC-05), `global_target_dir` inert and ancestor check dead (F-10, F-11), missing `_bmad/` behaviour (F-03), version skew and partial tree (F-04, F-05), prior-review figures kept apart (SC-09, G-09); R02 no first-use field in the catalogue contract and boot-time seed-only install (F-01), rebuild versus push classes (K-05), health blind to other projects (F-07), layer budget 68 of 70 (K-06, SC-14, G-19); R03 HOME persistence and no other-repo change (K-03, K-05), `FIRST_USE(P)` (3.1, F-02), hook `block-bare-python.sh` and the 25-of-31 fallback (G-06, CC-14); R04 `test-57:450` as the single "writes nothing" pin and the per-variant break list (SC-06, SC-13, F-06), shape pins (K-10), stale "T1-T55" (CC-15); R05 decision trail and records (F-09, SC-16), CLI-is-global wording (CC-17, K-02), offline banner (CC-22), `{output_folder}` (SC-04), Renovate rows (K-07); gaps log feasibility (F-01 notes, K-03) and run-only facts (4.5); W01 and W02 findings (5.1, 5.2, 5.3).

**Excluded, with rationale.** These findings are real but belong to other report sections by the synthesis mapping (RN SUGGESTED_PHASES): the boot order and idempotency table of R03 s2, Python 3.11 and host facts of R01 s7.5 and the installer call chain of R01 s3.1 (Section 2, current state); the per-option hook-point tables, step-by-step walkthroughs, the D-option collision with IronClaude's `/.claude/hooks/` predicate and the unlocked `settings.json` writers (R02 s6, R03 A3, R04 section 7 and A.11) (Sections 6 and 8); the README and markdownlint edit rules of R05 (e) (Section 8). The second half of the prior diagnosis is outside this task's scope by the 2026-11-07 user confirmation and is not discussed; G-29 appears only as the log's "out-of-scope, no action" row.

**Why I believe nothing was dropped or invented.** Every row in 4.2 maps one to one to a log row G-01 to G-30; every CC and SD ID of the log appears in 4.3 exactly once; every Section 5 finding carries a source URL, a relevance rating and a relationship; every number was copied from a research file or recomputed from tables in this file. Contradictions found: (1) R05 `[CODE-CONTRADICTED]` item C5 was withdrawn inside R05 and is not counted; (2) R02, R04, R05 call options E and F UNVERIFIED while R01 gives CODE-VERIFIED, and I used R01 (GL G-25); (3) R03 A5 says "both" corrections but names one (CC-14, left UNVERIFIED rather than guessed); (4) the log keeps G-23's OD-1 label open while R05 b1 reads `owner-decisions.md:5` as "OD-1 BMad placement", and I reported both without closing it. I found no Critical gap in the log, and the one Critical row (F-01) is a functional gap I rated by effect on the target, not a log item. I did not run any test or any `bmad` command, so no success criterion is marked as observed.

