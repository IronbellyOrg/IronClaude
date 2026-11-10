# Synthesis 03: Options Analysis and Recommendation

**Topic:** BMAD first-use directory creation in a project that never had BMAD (BMAD-METHOD 6.9.0, Coder AIDev02 workspace)
**Date:** 2026-11-08
**Sources:** research files 01 to 05, web-01, web-02 and gaps-and-questions.md. Fix-cycle addenda are applied where they supersede earlier text in the same file (01 F5-A to F5-H, 02 A1 to A8, 03 A1 to A5, 04 A.1 to A.11, 05 F1.1 to F1.6, research-notes F9).
**Report sections produced:** `## 6. Options Analysis`, `## 7. Recommendation`
**Status:** Complete

---

## 6. Options Analysis

### 6.0 Basis of the options (read first)

Evidence tags used in this section:

| Tag | Meaning here |
|---|---|
| [CODE-VERIFIED] | Read in code, config or tests of this repo, or in the installed 6.9.0 package at `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/`, by a research agent. Nothing was executed: the research ran no `bmad install` and no test, so every test verdict is a reading of assertion code. |
| External context (code) | Shipped npm tarballs of `bmad-method` 6.9.0, 6.10.0 and 6.12.4, searched with Grep by web-02 (https://registry.npmjs.org/bmad-method/-/bmad-method-6.12.4.tgz and the same pattern for the other versions). |
| External context (docs) [UNVERIFIED - doc-only, no code confirmation] | Official Claude Code docs (web-01, https://code.claude.com/docs/en/skills, /hooks, /settings, /managed-settings, /permissions) and upstream BMAD release notes and issues (web-02). Shown with their source. These facts are never the only basis of an effort rating, a risk rating or the recommendation; they appear as caveats and as questions for a live check. |
| [UNVERIFIED] | Not observed. Marked in the cell where it matters. |
| OBSERVED-FROM-6.10.0-TRACKED-TREE | Rows of file 01 section 8 come from this worktree's tracked 6.10.0 tree, not from 6.9.0 installer output. No rating or recommendation in this file rests on them. |

Rating key (this synthesis's own rubric, applied to counted facts from the research; it is not a research finding):

| Rating | Rule |
|---|---|
| Effort XS / S / M / L / XL | XS = 1 to 2 product files, no pinned-test change. S = 3 to 4 files, or exactly one amended or new test. M = 5 to 7 files, or 2 to 3 amended or new tests. L = 8 or more files, or two delivery layers (image and Terraform). XL = needs a change outside this repo. Files are counted without the decision-record documents that every option needs (see the common-facts table, row 12). |
| Risk Low / Medium / High | Count the factors that apply. **R1** a certain pinned-test break. **R2** a new persistent artifact in HOME. **R3** a shared file with other writers, or a shared block that other tests compare. **R4** image-wide behaviour not gated by the `bmad` slug or the profile. **R5** adds an image layer against the CI gate of 70 layers (68 used, 2 free). 0 factors = Low, 1 = Medium, 2 or more = High. |

Facts common to every option (they are stated once here and not repeated in each option):

| # | Fact | Source |
|---|---|---|
| 1 | The 2026-11-07 owner decision: BMAD should create its needed directories on first use in a project that never had it; global installation of BMAD is not requested; OD-1 is superseded for first-use creation only. The wording exists only at `BUILD-REQUEST.md:14` (no copy in the specs yet). | BUILD-REQUEST.md:14; research-notes F9-1; gaps G-26 |
| 2 | 6.9.0 has no first-use bootstrap. Skills need a project-local `_bmad/`. `resolve_config.py` exits 1 when `_bmad/config.toml` is absent; `resolve_customization.py` silently falls back to skill defaults; no skill detects a missing `_bmad/` or tells the user to install. Any bootstrap must therefore come from outside BMAD. [CODE-VERIFIED] | 01 section 7 and its Key Takeaways (`resolve_config.py:156`, `resolve_customization.py:209-236`) |
| 3 | Non-interactive per-project install: `NPM_CONFIG_OFFLINE=true bmad install --yes --directory "$P" --modules bmm --tools claude-code --output-folder _bmad-output --user-name "<name>"`. `--output-folder _bmad-output` must stay whenever `--user-name` is passed (mechanism at `official-modules.js:1409`; outcome of dropping it UNVERIFIED). It writes only inside `$P`: `_bmad/`, `_bmad-output/{planning,implementation}-artifacts/`, `docs/`, `.claude/skills/bmad-*`; no git call, no `~/.claude` write, no HOME write on the bmm-only path (by code, never observed). [CODE-VERIFIED] | 01 sections 3.2, 3.2a, 3.4, 4, 5; 03 A2 |
| 4 | One trigger predicate, FIRST_USE(P): P is the git work-tree top (else the current directory); `$P/_bmad` does not exist; no `$P/.claude/skills/bmad-*` entry on disk (tracked or untracked); `$P` writable. It widens `catalogue/bmad/install.sh:24` and drops the `.git` requirement of `install.sh:22`. A directory with no `.git` ends in "nothing to configure" in the slug as written, so the slug's branch order cannot be reused for it. Whether `bmad install` itself works with no `.git` is UNVERIFIED (R-3). | 03 A2 |
| 5 | The `bmad` CLI is already global: `Dockerfile.coder:139` `npm install -g bmad-method@6.9.0`, wrapper `/usr/local/bin/bmad` (two lines: `#!/bin/sh`, `exec node <cli> "$@"`, `Dockerfile.coder:142`). Only framework content is per project, so decision text must say "no global or user-level install of BMad framework content". [CODE-VERIFIED] | 02 section 1; 05 b nuance, C1 |
| 6 | Health and readiness are blind to any project except the recorded seed repo: `spec2_health_observed bmad` reads only `<seed>/_bmad/_config/manifest.yaml` or tracked `.claude/skills/bmad-*` (`spec2-health.sh:99-114`). No option changes the state `Installed-not-Configured` for a seedless HOME unless `spec2-health.sh` and the `record_health` rows of test-57 change together. [CODE-VERIFIED] | 02 section 5; 04 section 2.1 and "Other questions"; gaps D-14 |
| 7 | No test executes a first-use action (no skill, hook or wrapper run). So no existing test proves delivery of B2, B3, D2 or D3, and each option needs a new delivery assertion. [CODE-VERIFIED] | 05 F1.3 (X1 to X6); 04 A.10 last paragraph, A.11 |
| 8 | The `bmad` slug runs at every agent start (`startup.sh` section 9), seed repo only; first-use creation is a separate, later action and the boot seed install stays as built. Marker `~/.aidev/installed/bmad` is never removed on deselection (`startup.sh:1116-1117`). [CODE-VERIFIED] | 02 section 2; 05 open question 1 |
| 9 | Image layers: the CI gate fails above 70; measured 68 on `f1ac0c93` and on the newest main run, so 2 are free. Another PR can use them first. [CODE-VERIFIED from CI logs, dind-sidecar job only; the Sysbox-runtime job was not read] | 02 A1 to A6; gaps G-19 |
| 10 | The `minimal` profile has no `bmad` slug and no `ironclaude` slug (`profiles.yaml:19-21`). Anything image-wide or outside the slug is not profile-gated unless extra checks are added. [CODE-VERIFIED] | 02 sections 4.4, 6.2; 03 A1 |
| 11 | Version skew and partial trees: the 6.9.0 installer has no installed-versus-installer version gate. If `_bmad/` exists (even a half-written one), `--yes` takes quick-update (`ui.js:233-262`, `existing-install.js:64-66, 111`). Prior-review observation, not re-run: 6.9.0 over a 6.10.0 tree downgraded the manifest and changed 41 files with exit code 0. A failed first run leaves a partial `_bmad/` (mechanism CODE-VERIFIED; what quick-update does to it UNVERIFIED). FIRST_USE(P) is the only barrier, and model compliance with a stub's text is UNVERIFIED. | 01 F5-D, F5-F, F5-8; gaps G-08, G-13 |
| 12 | Decision records and documents every option needs, so they are not counted in any effort rating: append a `(decision) Owner 2026-11-07` bullet to `_bmad-output/specs/spec-orca-bundle-gap-closure/.memlog.md`, add row OD-4 to `owner-decisions.md` and a pointer in OD-1, re-derive `SPEC.md` (lines 29, 77), cross-reference in `spec-orca-catalogue-bundle/.memlog.md`, reconcile `templates/VSCode-AIDev02/README.md:241`, add a `CHANGELOG.md` entry under `[Unreleased]`. | 05 b1, c1, c2, e |
| 13 | First-use files in a repo other than the seed show up as untracked unless the three `info/exclude` lines of `install.sh:32-34` are written first; whether the owner wants them hidden or visible is not decided (U17). [CODE-VERIFIED for the mechanism; owner wording UNVERIFIED] | 02 section 3.1; 05 U17; gaps G-26, D-10 |
| 14 | After install, 41 `python3 ` steps in 31 `SKILL.md` files meet the user's `block-bare-python.sh` hook if Claude emits the bare form (hook blocks a leading `python3` word: CODE-VERIFIED; emission and registration in a fresh workspace UNVERIFIED); 25 of 31 files carry a written fallback. The install command itself is not blocked (command word `bmad`). This concerns the skills after any option has run, not the choice among options. | 03 A1, A3 shared facts; gaps G-06 |

Option list. B and D are split into variants because the research shows they differ on the criteria that decide (file 02 section 6; file 05 F1.4 reads "B" and "D" in file 04 section 7 as B1 and D1).

| ID | Option | Variants | Origin |
|---|---|---|---|
| A | Document only | none | research-notes row A |
| B | User-level bootstrap skill | B1 written by `catalogue/bmad/install.sh`; B2 seeded by `startup.sh` section 6 `seed_if_absent`; B3 written by a root `coder_script` in `modules.tf` | 02 section 6.1 |
| C | Image-level `bmad` wrapper change or new wrapper command | C in place (`Dockerfile.coder:142`); C late-COPY helper | 02 section 6.2 |
| D | Claude Code user-level or managed hook | D1 merged into `~/.claude/settings.json` by `install.sh`; D2 image managed-settings drop-in; D3 merged by a root `coder_script` | 02 section 6.3; 03 M3, M4 |
| E | `bmad install --directory ~` (home-level install) | E2 workspace-parent install (upstream workaround) | 01 section 6; 02 section 6.5; web-02 section 9 item 4 |
| F | Upstream user-scope install through `global_target_dir` | none | 01 section 2; web-02 sections 2, 8 |
| G | Instruction-text channel (a BMad block in `~/.claude/CLAUDE.md`) | none | 02 section 6.1 last paragraph; 04 A.4, A.6 |
| H | Upstream Claude Code plugin marketplace route | none | web-02 section 9 item 7 |
| I | Image-level managed ("enterprise") skill location | none | web-01 section 1.1 table |

### Option A: Document only (keep the manual one-command install and say so in README)

**Description.** No behaviour change. The README and the baked welcome text state that BMad framework content is created per project, at boot for the seed repo only, and in any other project by one manual command. Nothing is created on first use.

**How it works (technical).**

| Step | What happens | Source |
|---|---|---|
| 1 | The user runs, from the project root, `bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output`. All flags exist in 6.9.0 (`commands/install.js:14-37`) [CODE-VERIFIED]. That it completes end to end is UNVERIFIED (R-11). | `catalogue/bmad/manifest.yaml:12-14`; 05 d4 |
| 2 | The command differs from `install.sh:42` in three ways: no `NPM_CONFIG_OFFLINE=true`, no `--user-name`, no `info/exclude` lines, so in another repo the new directories appear as untracked files. | 02 section 3.1 |
| 3 | `templates/VSCode-AIDev02/README.md` is outside the image build context (`main.tf:119`), so a workspace user cannot read it; the README must itself carry the command, and the baked welcome text must keep it too. | 05 (e) |
| 4 | README line 241 (the Default profile cell) is reconciled in place: five cells, no raw pipe, lines 96 to 101 untouched (anchor `upstream GitHub CLI release v` at `README.md:100`, `releases.json:113`); the file is linted (`.markdownlint-cli2.yaml`). | 05 (e) |
| 5 | A welcome-text edit must keep the tokens `bmad` and `bmad --help` (`test-19:517-529`), must not add a column-0 `version:` line (Renovate row `expected.txt:8`), must not add lifecycle strings (`test-49:326`), and retags the image because `catalogue_sha256` hashes the catalogue (`main.tf:74`). | 05 (a-supplement), (f); 04 section 5 |

| Row | Assessment |
|---|---|
| Effort | **XS.** 1 required file (`templates/VSCode-AIDev02/README.md`, outside `image/`, no retag); the welcome text in `image/catalogue/bmad/manifest.yaml` is an optional second file and does retag. No pinned-test change. |
| Risk | **Low.** 0 of R1 to R5. Only conditional break: `test-19` if the welcome text loses `bmad` or `bmad --help`. |
| Reuse of existing code | The existing welcome text and manual command (`manifest.yaml:12-14`). |
| Files/systems affected | `templates/VSCode-AIDev02/README.md:241`; optionally `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:12-14`; `CHANGELOG.md`; the decision-record documents of common fact 12. |
| Pros | No code, no test change, no image layer; keeps the "no global install" part intact; it is also the documentation half that every other option still needs, because the mechanism may not fire (05 b3 row `manifest.yaml:12-14`). |
| Cons | Creates nothing on first use, so it does not satisfy the 2026-11-07 decision (research-notes SOLUTION_RESEARCH row A; research-notes F9-3 R9: the precondition for "documentation only" is met but its scope is superseded because the decision asks for behaviour). The existing welcome text reads "BMad is already set up there" unconditionally although nothing is configured without a seed or when `_bmad/` already exists (02 C7). |

### Option B: User-level bootstrap skill or command under `~/.claude/skills/`

**Description.** A content-free stub skill (no BMAD material) is placed in `~/.claude/skills/<name>/SKILL.md`. When it is invoked in a project, its text tells Claude to evaluate FIRST_USE(P) and, if true, run the pinned offline install for that project. Three delivery routes are described in file 02 section 6.1.

**How it works (technical).**

| Step | What happens | Source |
|---|---|---|
| 1 Delivery | B1: a new step in `catalogue/bmad/install.sh` between line 55 and the marker write at line 58; the stub text must be an inline heredoc because a fourth file in `catalogue/bmad/` breaks the three-file rule (`test-1-catalogue-shape.sh:25, 43-67`). B2: a source file COPY-ed into the image plus a `seed_if_absent` line in `startup.sh` section 6 (pattern `startup.sh:275`; zero-layer form: ride the existing COPY to `/usr/local/lib/aidev/` at `Dockerfile.coder:547-548` and seed from there as `startup.sh:291-293` does; allowed by `test-60:87-88`; the fold itself is UNVERIFIED, U18). B3: a new `resource "coder_script"` in `modules.tf`, count-gated on `contains(local.active_slugs, "bmad")`, pattern `coder_script "orca_retirement"` (`modules.tf:82-109`). | 02 section 6.1; 02 A5; 04 A.3 (a) |
| 2 Invocation | The user invokes the stub by its slash name in a project that has no BMAD. | 03 A3 B1 to B3 step 1 |
| 3 Predicate and install | The stub's text has Claude run FIRST_USE(P) and then the common install command in a Bash tool call; the user sees the installer output and the box "BMAD is ready to use!" (`installer.js:1219-1243`). Whether Claude follows the text is UNVERIFIED (UV-17). | 03 A3 shared facts, B steps 2 and 3 |
| 4 Skills appear | `P/.claude/skills/bmad-*` exist after the install. The installer's own text says to launch the agent from the project folder afterwards (`installer.js:1233`). | 03 A3 B step 4 |
| 5 Naming | The name must avoid the whole words `preview`, `share`, `share-port`, `expose`, `dev-preview` in a `cp` or `ln -s` destination (`test-3-reserved-names.sh:27, 55`); it must not equal a name superclaude installs (39 packaged names, none starting with `bmad`) or the three Orca names. | 04 A.2; 03 section 5 |

Delivery variants of B:

| Variant | Rebuild class | What persists in HOME | Layers | Source |
|---|---|---|---|---|
| B1 | image rebuild (catalogue hash, `main.tf:74`); effective on the next agent start after `coder update` | `~/.claude/skills/<name>/SKILL.md`, rewritten every boot unless written copy-if-absent | 0 (`COPY ... catalogue /catalogue`, `Dockerfile.coder:593`) | 02 6.1, A5 |
| B2 | image rebuild (new source in `image_input_files`, `main.tf:80-101`; `Dockerfile.coder` edit) | same path, created once, then user-owned; a later image update never reaches an existing workspace (`startup.sh:245-248`) | +1 as written (own COPY); 0 if folded (UNVERIFIED, U18) | 02 6.1, A5; 03 M1 |
| B3 | template push only; `modules.tf` is outside the image hash (`main.tf:104-107`); runs at the next agent start after the workspace is updated | same path, rewritten each agent start | 0 | 02 6.1, 6.4 |

| Row | B1 | B2 | B3 |
|---|---|---|---|
| Effort | **S.** 2 to 3 files: `catalogue/bmad/install.sh`, optionally `manifest.yaml`, and one amended test (`test-57-catalogue-configure.sh:450` renamed to `no seed: bmad writes only the first-use skill` with one pinned file hash, 04 A.11). | **M.** 6 files: `Dockerfile.coder`, `main.tf` (`image_input_files`), a new non-hidden source under `workspace_defaults/`, `startup.sh` section 6, and two test lists (`test-startup-boot.sh:2775`, `test-22-aienv-fresh-workspace.sh:271-272`, 04 A.11). | **S.** 2 to 3 files: `modules.tf`, one new static pin next to `test-52-browser-usability-evidence.sh:1374-1377` (04 A.11), optionally a ledger kind at `test-startup-boot.sh:232`. |
| Risk | **High.** R1 (`test-57:450`, certain) and R2 (HOME artifact rewritten at every boot, including the no-seed boot). | **High as written** (R2 and R5, 68 to 69 layers); **Medium** if the fold holds (UNVERIFIED, U18). | **Medium.** R2 only. No certain break, no layer, no rebuild. The conditional breaks (S16c, S18, S19 of file 05) are avoided by placement: a separate resource after `modules.tf:109`, no new `locals` block above `modules.tf:16`, a display name other than `aidev-startup`. |
| Reuse of existing code | `install.sh` guard, exclude and status pattern (`install.sh:21-55`); the common install command. | `seed_if_absent` (`startup.sh:201-274`) and the config-seeding precedent (`startup.sh:291-293`, `Dockerfile.coder:543-545`). | `coder_script "orca_retirement"` (`modules.tf:82-109`); `jq` is in the image (`Dockerfile.coder:590`). |
| Files/systems affected | `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh`; `.github/contract-tests/test-57-catalogue-configure.sh`. | `image/Dockerfile.coder`, `main.tf`, `image/scripts/startup.sh`, `image/workspace_defaults/`, two contract tests. | `templates/VSCode-AIDev02/modules.tf`; `.github/contract-tests/test-52-browser-usability-evidence.sh`. |
| Pros | One file in the slug that already owns BMad; updates reach existing workspaces each boot. | Not a slug-gated code path; the file is user-owned afterwards. | Cheapest: template push only, 0 layers, no certain break; refreshed on every start; profile-gated by `active_slugs`. |
| Cons | Certain break of the only "writes nothing" oracle; a heredoc body must carry no unquoted install verb (`test-19:208-209`); the stub must also be written when no seed is recorded, which is exactly the case `test-57:446-450` pins (gaps D-12). | Copy-if-absent means a fixed text for the life of the workspace; section 6 also runs for `minimal`, where bmad is absent; six pins to keep (test-67, test-7, test-60, test-3, test-49, test-59), and delivery is unproven by the live boot gate until `test-startup-boot.sh:2775` is extended. | Splits BMad logic between `modules.tf` and the catalogue slug; the catalogue README describes `module.tf` as `coder_app` plus `variable agent_id` and is silent on `coder_script` (02 6.1); no ledger row, so the live boot gate cannot see it; the bmad marker is never removed on deselection, so a user-level stub stays after switching to `minimal` unless cleanup is added (02 6.1, gaps D-5). |

**Shared points for B.** A user-level artifact is owner question 1 (section 7). Whether Claude Code loads a stub from `~/.claude/skills/` in every project, how it ranks it against a same-named project skill, and whether skills created during a running session appear are Claude Code behaviours that only external docs answer: user skills are listed for "All your projects", "Enterprise over personal, and personal over project", and a top-level `.claude/skills/` that did not exist at session start is not watched and needs `/reload-skills` (https://code.claude.com/docs/en/skills). [UNVERIFIED - doc-only, no code confirmation; the Claude Code version in the image is not established.] If the docs hold, the stub must not reuse a `bmad-*` name. `superclaude install --force` leaves a skill name outside its packaged set alone: skills are replaced per packaged name only and the only `rmtree` calls are `install_skills.py:97` and `install_skill.py:48` [CODE-VERIFIED, 03 section 5].

### Option C: Image-level `bmad` CLI wrapper change or a new wrapper command

**Description.** The root-owned wrapper `/usr/local/bin/bmad` (today a pure `exec`) or a new command name next to it evaluates FIRST_USE(P) for the current project and runs the common install command before doing what the user asked.

**How it works (technical).**

| Step | What happens | Source |
|---|---|---|
| 1 Place | In place: the `{ echo "#!/bin/sh"; echo "exec ..." } > /usr/local/bin/bmad` group at `Dockerfile.coder:142`, inside the root layer at lines 136 to 145 (0 new layers). Late-COPY helper: a separate script added to the existing `bin/` COPY at `Dockerfile.coder:492-493` or the `/usr/local/lib/aidev/` COPY at `:469` (0 layers if it rides them, UNVERIFIED, U19; +1 as its own COPY). | 02 section 6.2, A5 |
| 2 What may be intercepted | The wrapper must pass `bmad --version`, `bmad --help` and `bmad install ...` through unchanged: `test-19:1175-1190` and `545-561` run `bmad --version` and `timeout 10s bmad --help </dev/null`; `install.sh:18, 42` and the health probe `manifest.yaml:25` use them. The 6.9.0 subcommands are `install`, `status`, `uninstall` (`tools/installer/commands/`). So the wrapper can act only on `status`, `uninstall` or a new command name. This is a consequence of the cited constraints, not a research statement. | 02 section 6.2; 03 A3 C.5; 04 section 4 |
| 3 Trigger limit | It fires only when something executes `bmad`. It cannot fire when a BMAD skill is invoked in Claude Code, because no `bmad` process runs then (inference, UNVERIFIED, UV-28). | 02 section 6.2; 03 A3 C.5 |
| 4 Seeded runs | The slug's own call `bmad install ...` (`install.sh:42`) goes through this wrapper in every seeded test-57 run, so the wrapper is exercised by `test-57` at lines 173-178, 323-324 and 457-459 (the second run at 331-336 hits the `_bmad` guard and does not call it). | 05 F1.1, X2 |
| 5 Pin strings | The literal `npm install -g bmad-method@X.Y.Z` must stay in `Dockerfile.coder` (`expected.txt:6`, `renovate-global.json5:48`). | 05 (f) |

| Row | Assessment |
|---|---|
| Effort | **S.** 2 to 3 files: `image/Dockerfile.coder` (one RUN group), optionally `catalogue/bmad/manifest.yaml` so a new command name is discoverable (`manifest.yaml:12-14`), and, only if the wrapper moves to a `printf '%s\n' \` block, one extraction check beside `test-60-llm-gateway-env.sh:162-168` (04 A.11). |
| Risk | **Medium.** R4 only: the wrapper is baked for every profile, so it changes what `bmad <anything>` means in `minimal` workspaces too (02 section 6.2 "Stretches"). No certain break. Conditional breaks: `test-19:1175-1190, 545-561` (wrapper not an executable file or `--version`/`--help` non-zero); `test-57` seeded runs (`323-324, 457-459`, budget `173-183`); `test-60:162-169` if the `claude` printf block is touched; `test-71` if a second `CG_VERSION=` line appears; `test-67` for an unlisted new COPY source; `test-3` for a file-based wrapper using a reserved word; `test-49` for lifecycle strings. |
| Reuse of existing code | The existing wrapper (`Dockerfile.coder:134-143`) and the install command of `install.sh:42`. |
| Files/systems affected | `templates/VSCode-AIDev02/image/Dockerfile.coder:136-145`; optionally `image/catalogue/bmad/manifest.yaml`; `main.tf` only for a new COPY source. Nothing in HOME. |
| Pros | No user-level artifact, so owner question 1 does not arise for it; no certain pinned-test break; writes nothing under HOME at boot (the artifact is image-level); 0 layers in place. |
| Cons | Only the "running a `bmad` CLI command" reading; the commands a wrapper may intercept are few (step 2), and `bmad install`, which already creates the directories, must stay untouched; image rebuild; Dockerfile comment calls the wrapper a pure exec stand-in (`Dockerfile.coder:134-135`). |

### Option D: Claude Code user-level or managed hook (SessionStart or UserPromptSubmit)

**Description.** A hook that evaluates FIRST_USE(P) cheaply on every session start (or every prompt) and, when true, runs the common install command. Three delivery routes: D1 a hook entry merged into `~/.claude/settings.json` by `catalogue/bmad/install.sh` (model: `ironclaude/install.sh:100-136`); D2 a drop-in file under `image/etc/claude-code/managed-settings.d/` (existing file `10-retention.json` holds `{"cleanupPeriodDays": 90}`; COPY pattern `Dockerfile.coder:500-501`; listed at `main.tf:87`); D3 the same merge done by a root `coder_script` in `modules.tf`.

**How it works (technical).**

| Step | What happens | Source |
|---|---|---|
| 1 | `~/.claude/settings.json` in this workspace already holds SessionStart (5), UserPromptSubmit (3) and PreToolUse (3) registrations; the 29 existing `timeout` values are 1 to 10 s, while install time inside a workspace is unknown (UNVERIFIED, U1; CI `cold bmad` was 374 to 392 ms offline, the memlog "about 4s" includes an npx fetch, and the two must not be blended). | 03 section 4, A3 D.2; 01 F5-C, F5-E |
| 2 | A hook that waits for the install needs a far larger `timeout` than any existing hook, or must run in the background. | 03 A3 D.2 |
| 3 | The skills are created after the session has started. Whether the session sees them is a Claude Code question (below). | 03 A3 D.3 |
| 4 | D1 and D3 write `~/.claude/settings.json`: IronClaude treats any hook command containing `/.claude/hooks/` as its own (`ironclaude/install.sh:15-16, 25`; `spec2-health.sh:90-91`; `test-57:140`), so a bmad hook command with that substring would make the IronClaude `hook` observation true without IronClaude; there is no lock against the other `settings.json` writers (`ironclaude/install.sh:139` comment); `superclaude install` keeps a hook with a different command string, and `ironclaude/install.sh:104-136` fails the ironclaude slug if a pre-existing hook command disappears. | 02 section 6.3; 03 section 5 |
| 5 | D2 avoids HOME, but `test-73-claude-retention.sh:102-114` requires exactly one COPY line containing the `10-retention.json` path, in the exact form `COPY --chown=0:0 --chmod=0644 <rel> /<rel>`, and one RUN line holding both `/etc/claude-code` directories; a second drop-in needs its own COPY line (+1 layer), no `cleanupPeriodDays` key, and valid JSON. | 02 A5; 04 A.6 |
| 6 | Blast radius: the hook acts in every project, so "opening a session" would install in every repo lacking BMAD ("install everywhere", not "first use of BMAD"); no user prompt in the path. | 03 A3 D.1, D.5; research-notes row D |
| 7 | External context [UNVERIFIED - doc-only, no code confirmation] (https://code.claude.com/docs/en/hooks, /settings, /managed-settings): hook timeout defaults are 600 s for SessionStart and 30 s for UserPromptSubmit; a SessionStart hook may return `reloadSkills: true` so freshly written skills are visible in the same session; no re-scan field was found for UserPromptSubmit; in an interactive session hooks from every settings file, including `~/.claude/settings.json`, are held back until the folder's workspace trust is accepted (whether a held-back SessionStart hook then runs late is not stated); hook entries merge across user, project, local and managed levels and a managed hook cannot be disabled by the user; that a drop-in may hold `hooks` is documented only by inference. | web-01 sections 2.3, 2.4, 3.2, 3.3, 4.1 |

| Row | D1 | D2 | D3 |
|---|---|---|---|
| Effort | **S.** 2 to 3 files: `catalogue/bmad/install.sh` (jq merge), `test-57-catalogue-configure.sh:450` replacement, plus merge fixtures for the coverage gap C-F1-3 (`test-57:386` says install is the only settings writer). | **S.** 4 files: new `image/etc/claude-code/managed-settings.d/20-*.json`, `Dockerfile.coder` (own COPY), `main.tf:80-101`, and a second-file check in `test-73-claude-retention.sh` (04 A.11). | **S.** 2 to 3 files: `modules.tf` (jq merge in a new resource), a static block pin next to `test-52:1374-1377`, optionally a ledger kind. |
| Risk | **High.** R1 (`test-57:450` certain), R2 (`settings.json` in HOME), R3 (shared file, unlocked writers, `/.claude/hooks/` predicate). | **High.** R4 (image-wide, not slug-gated, applies to `minimal` too) and R5 (+1 layer; no zero form without editing the `test-73` pin). | **High.** R2 and R3. No certain break; same placement rules as B3 apply. |
| Reuse of existing code | `ironclaude/install.sh:100-136` (malformed-file refusal, symlink preservation, before/after hook preservation). | Managed-settings directory and COPY pattern (`Dockerfile.coder:473-475, 498-501`). | `modules.tf:82-109` plus `jq`. |
| Files/systems affected | `catalogue/bmad/install.sh`; `~/.claude/settings.json`; `test-57`. | `image/etc/claude-code/managed-settings.d/`; `Dockerfile.coder`; `main.tf`; `test-73-claude-retention.sh`. | `modules.tf`; `~/.claude/settings.json`; `test-52`. |
| Pros | Acts where Claude Code is used; hook survives `superclaude install` (additive merge by exact command). | Nothing in HOME; not touched by IronClaude's `/.claude/hooks/` predicate (reads `~/.claude/settings.json` only). | Template push only, 0 layers, no certain break. |
| Cons | Certain break; a bmad hook before ironclaude in sort order weakens `test-57:187, 376` if its command contains `/.claude/hooks/` (WEAKENS, not a failure). | Whether Claude Code accepts hooks from a drop-in is documented only by inference; user cannot turn it off [doc-only]; image-wide. | Race with other writers of `settings.json` now spans two boot scripts; a lost update self-heals only if the adder re-adds it (`ironclaude/install.sh:139`). |

### Option E: `bmad install --directory ~` (home-level install)

**Description.** Run the installer once with the home directory as target.

**How it works (technical).** `--directory ~` passes `validateDirectorySync` (`ui.js:1414-1463`) and `~` is expanded (`ui.js:1568-1581`); `findBmadDir` returns `<dir>/_bmad`; the claude-code target is project-relative (`.claude/skills`). From the code the write set would be `~/_bmad/`, `~/_bmad-output/{planning,implementation}-artifacts/`, `~/docs/` and `~/.claude/skills/bmad-*` (01 section 6 item 2; UNVERIFIED, nothing was run; whether it edits `~/.claude/CLAUDE.md` is UNVERIFIED, U-F1-1). The ancestor-conflict check is dead configuration in 6.9.0 (no platform sets `ancestor_conflict_check`, `_config-driven.js:191`, `platform-codes.yaml:10`), so the installer would not block it and would not block a later per-project install [CODE-VERIFIED]. It does not create the project's own `_bmad/`, which the skills read through `{project-root}/_bmad/...` where `{project-root}` is the project working directory (01 section 7.4), and `resolve_config.py` exits 1 without `<root>/_bmad/config.toml` (01 section 7.1). Note an internal nuance: 01 section 6 item 3 says the root walk stops at the project, while 01 section 7.2 shows `resolve_customization.py` starts from the skill's own directory first; both are code reads, neither was run, and neither changes the rating because E already fails the "no global install" criterion. Variant E2 (install into a workspace parent folder) is the upstream maintainer's workaround for a requested global install (issue #1852, https://github.com/bmad-code-org/BMAD-METHOD/issues/1852, external context, doc-only); whether it works for repositories with their own `.git` is UNVERIFIED because `find_project_root` stops at the nearest `_bmad` or `.git` (web-02 recommendation 4).

| Row | Assessment |
|---|---|
| Effort | **S.** No repo file if the user runs it by hand; if run from `install.sh`, 3 files (`install.sh`, `test-57`, the 75 s boot budget at `test-startup-boot.sh:2129-2156`). It delivers nothing useful (see Cons), so the effort buys no result. |
| Risk | **High.** R1 (`test-57:450` certain if run from `install.sh`; the E write set is UNVERIFIED) and R2 (HOME). Also a global-style install of framework content, which the owner declined. |
| Reuse of existing code | None in the repo; the installer's `--directory` option. |
| Files/systems affected | `~/_bmad`, `~/_bmad-output`, `~/docs`, `~/.claude/skills` (by code reading); `test-57`. |
| Pros | No image change if user-run; the installer does not refuse it. |
| Cons | Violates "no global BMAD install"; leaves the project's `_bmad/` absent, so first-use creation is not achieved; puts `docs/` and `_bmad-output/` under HOME; `~/.claude/skills/bmad-*` become visible in every project (doc-only). |

### Option F: Upstream user-scope install through `global_target_dir`

**Description.** Use the `global_target_dir: ~/.claude/skills` value that `platform-codes.yaml` declares for `claude-code`.

**How it works (technical).** It does not. `global_target_dir` appears in exactly one file, `tools/installer/ide/platform-codes.yaml` (43 hits: comment lines 9 and 12, 41 value lines); no `.js`, `.json` or `.md` file reads it; the skill write path is `path.join(projectDir, target_dir)` (`_config-driven.js:245-248`); `commands/install.js:12-51` has no `--global`, `--user` or scope option [CODE-VERIFIED, 01 sections 2 and 5]. External context (code): the same token appears only in `platform-codes.yaml` in 6.10.0 (43 hits) and 6.12.4 (46 hits), and the 6.12.4 `install` options add only `--shims` and `--no-shims` (web-02 section 2); upstream added the field as platform data for parity with the Skills CLI table (issue #2313, doc-only). So a newer pin does not enable F. The only upstream user-scope mechanism is the v7 preview (`npx skills add -g` plus a user-triggered `bmad setup`), a different distribution channel, an alpha, and a different skill set and layout (web-02 section 8, doc-only); it is not reachable by any `bmad-method@<version>` pin. File 04's "X" marks for F rest on the question's wording and are void; file 01's tag governs (gaps G-25).

| Row | Assessment |
|---|---|
| Effort | **XL.** It needs an upstream feature that no published 6.x version has (a change outside this repo), plus a pin change that touches three Renovate-visible strings (`Dockerfile.coder:139`, `install.sh:18`, `manifest.yaml:2`). |
| Risk | **High.** Not implementable in 6.9.0; adopting the v7 line would be a new product shape needing its own plan, tests and an owner reading of OD-1 (web-02 section 8). |
| Reuse of existing code | None. |
| Files/systems affected | Upstream `bmad-method`; `Dockerfile.coder:139`, `catalogue/bmad/install.sh`, `manifest.yaml` if the pin moves. |
| Pros | None for this task. |
| Cons | No code path in 6.9.0, 6.10.0 or 6.12.4; a version bump also changes the skill set and layout and makes `--yes` without `--directory` install into the working directory (web-02 sections 3, 5), so bumping would need its own plan. |

### Option G: Instruction-text channel (a BMad block in `~/.claude/CLAUDE.md`)

**Description.** Research found this as an alternative to a skill (02 section 6.1, last paragraph) but did not rate it. A marked block of instruction text, synced into `~/.claude/CLAUDE.md` at every boot, tells Claude to run the common install command when FIRST_USE(P) holds.

**How it works (technical).** `aidev_claude_md_block_sync` re-syncs a marked block from `/etc/skel/.claude/CLAUDE.md` into `~/.claude/CLAUDE.md` every boot (`startup.sh:1282-1285`); its markers are hard-coded to `SUPERCLAUDE_CODEGRAPH_BEGIN/END` (`claude-md-block.sh:23`), so a second marker pair or a generalised function is needed; `workspace_defaults/CLAUDE.md` (the seed source, `Dockerfile.coder:496`) has no BMad text today [CODE-VERIFIED]. Any BMad text outside the synced pair breaks the fresh-home equality `cmp /etc/skel/.claude/CLAUDE.md $HOME/.claude/CLAUDE.md` unless that assertion is amended (`test-startup-boot.sh:2083-2087, 3030-3037`); `test-74-claude-md-block.sh` fails if a second pair reuses the `SUPERCLAUDE_CODEGRAPH` markers (04 A.4, A.6). That Claude reads this file in every project and obeys it is Claude Code and model behaviour: UNVERIFIED.

| Row | Assessment |
|---|---|
| Effort | **M.** 5 files: `workspace_defaults/CLAUDE.md`, `scripts/lib/claude-md-block.sh`, `startup.sh` (second sync call), `test-74-claude-md-block.sh`, `test-startup-boot.sh` (two assertions). |
| Risk | **High.** R2 (`~/.claude/CLAUDE.md` in HOME) and R3 (the file is shared with IronClaude's block, saved and restored byte-for-byte around `superclaude install`, `ironclaude/install.sh:44-86`, and compared by two tests). |
| Reuse of existing code | `aidev_claude_md_block_sync` and the seed file. |
| Files/systems affected | As listed above; `~/.claude/CLAUDE.md`. |
| Pros | No skill discovery question; survives reboot because the block is re-synced each boot. |
| Cons | Pure instruction text with no enforcement; breaks or forces amendment of two existing equality checks; loads into every session of every project; rated at low depth because the research evaluated it only in passing. |

### Option H: Upstream Claude Code plugin marketplace route

**Description.** BMAD ships a marketplace file for Claude Code plugins. External context (code and issues), web-02 section 9 item 7 and issue #2677 (https://github.com/bmad-code-org/BMAD-METHOD/issues/2677, doc-only).

**How it works (technical).** The 6.9.0 tarball contains `.claude-plugin/marketplace.json` with name `bmad-method` and 2 plugins (`bmad-pro-skills` 6.8.0, 12 skills; `bmad-method-lifecycle` 6.8.0, 33 skills); the 6.12.4 file has 1 plugin (28 skills). The route installs skills in Claude Code's plugin cache, and per the upstream issue it does not create `_bmad/`, so it leaves exactly the first-use gap open; upstream closed that issue as "fixed-by-redesign" (v7), not by a 6.x patch.

| Row | Assessment |
|---|---|
| Effort | **L.** No repo mechanism exists for it: it would need a settings merge (`enabledPlugins` and `extraKnownMarketplaces`, which superclaude fills only where absent, 03 section 5) and a plugin cache in HOME, in addition to a first-use step. Assessed from web evidence only. |
| Risk | **High.** R2 (plugin cache in HOME) and R3 (shared `settings.json`); the plugin versions (6.8.0) differ from the image pin 6.9.0; it puts BMAD framework skills at user level, which the owner declined. |
| Reuse of existing code | None found. |
| Files/systems affected | `~/.claude/settings.json`, `~/.claude/plugins/cache/` (reporter's output in the issue). |
| Pros | An upstream-supported way to get user-wide skills. |
| Cons | Not a first-use mechanism by itself; user-level BMAD content; version skew; needs network (UNVERIFIED). |

### Option I: Image-level managed ("enterprise") skill location

**Description.** Research found, in a docs table only, a managed location for skills. Same stub as Option B, but placed outside HOME. Not evaluated by any research file.

**How it works (technical).** The skills page lists an enterprise location described as "a `.claude/skills/` in the managed settings directory", with precedence "Enterprise over personal, and personal over project" (https://code.claude.com/docs/en/skills, web-01 section 1.1). The exact directory is not stated in the text read; `/etc/claude-code/` is the Linux managed directory (https://code.claude.com/docs/en/managed-settings). [UNVERIFIED - doc-only, no code confirmation; path not established.] In this repo the managed directory is root-owned and image-baked (`image/etc/claude-code/managed-settings.d/`, `Dockerfile.coder:473-475, 498-501`); each COPY has one fixed destination, so a different destination costs its own COPY (02 A5).

| Row | Assessment |
|---|---|
| Effort | **M.** About 5 files by analogy with B2 and D2: new skill file, `Dockerfile.coder`, `main.tf:80-101`, a delivery test, `test-67` coverage. Assessed by analogy, not from a research file. |
| Risk | **High.** R4 (image-wide, not profile-gated) and R5 (+1 layer); precedence over every other level would let it shadow real BMAD skills [doc-only]. |
| Reuse of existing code | The D2 managed-directory COPY pattern. |
| Files/systems affected | `image/etc/claude-code/` (path UNVERIFIED), `Dockerfile.coder`, `main.tf`. |
| Pros | Nothing in HOME, so it avoids the "user level" wording of owner question 1 (whether managed counts is itself an owner reading). |
| Cons | Rests only on a docs table; unevaluated by the codebase research; image-wide. |

### Options Comparison

Columns are variants where the research shows variants differ on a criterion (B and D). Cell text is limited to what the research files state; a cell that no research file settles says UNVERIFIED. Table 1 covers options A to F; Table 2 covers the further options G to I, which research evaluated at lower depth.

**Table 1: options A to F**

| Criterion | A | B1 | B2 | B3 | C | D1 | D2 | D3 | E | F |
|---|---|---|---|---|---|---|---|---|---|---|
| Effort | XS (1 file) | S (2-3 files, 1 amended test) | M (6 files) | S (2-3 files) | S (2-3 files) | S (2-3 files, 1 amended test) | S (4 files) | S (2-3 files) | S (0 files by hand; 3 if run from `install.sh`), no result | XL (upstream feature) |
| Risk | Low (0 factors) | High (R1, R2) | High as written (R2, R5); Medium if fold holds (UNVERIFIED, U18) | Medium (R2) | Medium (R4) | High (R1, R2, R3) | High (R4, R5) | High (R2, R3) | High (R1, R2) | High (not implementable in 6.9.0) |
| Maintainability | Nothing new to maintain; the manual command must stay correct | Stub text lives in a shell heredoc of `install.sh` (no unquoted install verb, `test-19:208-209`); rewritten each boot, so edits reach existing workspaces | Copy-if-absent: existing workspaces never get text updates (`startup.sh:245-248`) | Refreshed each agent start; logic split across `modules.tf` and the slug | Edit inside a multi-line RUN; each `bmad` start also spawns `npm view` (`bmad-cli.js:31`); Renovate string must stay (`expected.txt:6`) | `settings.json` has other writers and no lock (`ironclaude/install.sh:139`) | Root-owned, image-versioned file; form pinned by `test-73` | Same shared-file hazard as D1, across two boot scripts | Nothing in repo; user-run | Depends on upstream |
| Integration complexity | 0 code points | 1 script + 1 test | 4 product points (COPY, `image_input_files`, section 6 line, source file) + 2 test lists | 1 file (`modules.tf`) + 1 pin | 1 RUN group | 1 script (jq merge) + 1 test | 3 points (file, COPY, `image_input_files`) + 1 test | 1 file + 1 pin | 0 in repo | Upstream |
| Reuse potential | Existing welcome text and manual command | `install.sh:21-55` guard, exclude, status pattern | `seed_if_absent`; precedent `startup.sh:291-293` | `coder_script "orca_retirement"` (`modules.tf:82-109`) | Wrapper `Dockerfile.coder:142`; `install.sh:42` command | `ironclaude/install.sh:100-136` merge pattern | managed-settings COPY pattern (`Dockerfile.coder:500-501`) | `modules.tf:82-109` + `jq` | None | None |
| Meets "no global BMAD install" | Yes | Yes for BMAD content (stub holds none); the stub itself is a user-level artifact = owner question 1 | Same as B1 | Same as B1 | Yes, no user-level artifact | Yes for BMAD content; hook is a user-level artifact (owner question 1) | Yes for BMAD content; not in HOME, whether "managed" counts as user level is an owner reading | Same as D1 | **No** (framework content under HOME) | n/a (no code path) |
| Needs a change in IronClaude or IronOrca | No | No [CODE-VERIFIED, 03 section 6] | No | No | No | No | No | No | No | No IronClaude/IronOrca change, but an upstream BMAD feature that no published version has |
| Image rebuild or only a template push | Neither for README (outside `image/`); rebuild if the welcome text changes | Rebuild (catalogue hash) | Rebuild | **Template push only** | Rebuild | Rebuild | Rebuild | **Template push only** | Neither if user-run | Rebuild + upstream |
| Image layers (gate 70, 68 used) | 0 | 0 | +1 as written; 0 if folded (UNVERIFIED, U18) | 0 | 0 in place; late-COPY 0 if folded (UNVERIFIED, U19), else +1 | 0 | +1 (no zero form without editing `test-73`) | 0 | 0 | not stated |
| Pinned tests that break (names) | None certain. BREAKS-IF: `test-19-catalogue-cli-presence.sh` (welcome tokens), `test-49-spec2-evidence.sh`, `test-2-manifest-schema.sh` (manifest edit) | **Certain: `test-57-catalogue-configure.sh:450`.** BREAKS-IF: `test-57:331-335`, `test-19:1137-1152`, `test-1-catalogue-shape.sh`, `test-3-reserved-names.sh`, `test-startup-boot.sh:2100-2108` | None certain. BREAKS-IF: `test-67-image-inputs-cover-copies.sh`, `test-7-startup-order.sh`, `test-60-llm-gateway-env.sh`, `test-3-reserved-names.sh`, `test-49-spec2-evidence.sh`, `test-59-home-workspaces-dir.sh` | None certain. BREAKS-IF: `test-52-browser-usability-evidence.sh:1374-1377`, `test-51-selector-onboarding-wiring.sh:386-396`, `test-startup-boot.sh:617-637, 2631-2637` | None certain. BREAKS-IF: `test-19` (`1175-1190, 545-561`), `test-57` seeded runs (`173-183, 323-324, 457-459`), `test-60:162-169`, `test-71-codegraph-bake.sh`, `test-67`, `test-3`, `test-49` | **Certain: `test-57:450`.** WEAKENS `test-57:187, 376`. BREAKS-IF: hook-preservation checks `test-57:325-326, 337, 364-365, 373, 379-380`, `test-1-catalogue-shape.sh`, `test-19:1137-1152` | None certain. BREAKS-IF: `test-73-claude-retention.sh`, `test-67`, `test-49` | None certain. Same BREAKS-IF set as B3; WEAKENS `test-57:187` | **Certain: `test-57:450`** if run from `install.sh` (write set UNVERIFIED); `test-startup-boot.sh:2129-2156` budget | None (no code path); file 04's "X" cells are void (gaps G-25) |
| Which reading of "first use" it satisfies | None; the user types the documented command | Invoking a BMAD slash skill, only through the stub's own name | Same as B1 | Same as B1 | Running a `bmad` CLI command, only for commands other than `install`, `--version`, `--help` (or a new command name) | Opening a session (SessionStart) or sending a prompt (UserPromptSubmit), in every project | Same as D1 | Same as D1 | None | None |
| Writes inside the whole-HOME snapshot (`snap "${H}"`, `test-57:148-153`; inside = anything under `$HOME` except `$HOME/.aidev/installed/*` and `*/.git/index`, including `${H}/seed/**`; outside = `/usr/local/bin`, `/etc`, `/catalogue`, `/opt`; path list from 04 section 1) | Inside: none. Outside: none | Inside: `~/.claude/skills/<name>/SKILL.md`, written by the run `test-57:448-450` snapshots, so it fails. Outside: marker `~/.aidev/installed/bmad` (excluded) | Inside HOME: `~/.claude/skills/<name>/SKILL.md`, written by `startup.sh` section 6, which `test-57` never runs (`test-60:139-152` and `test-22` run section 6 but do not snapshot HOME) | Inside HOME: same path, written by a `coder_script` that `test-57` never runs | Inside: none at boot. Outside: `/usr/local/bin/bmad` | Inside: `~/.claude/settings.json` hash changes (and any `~/.claude/hooks/<script>`), in the run `test-57:450` snapshots, so it fails. Outside: marker | Inside: none. Outside: `/etc/claude-code/managed-settings.d/<NN>-*.json` | Inside HOME: `~/.claude/settings.json`, by a script `test-57` never runs | Inside (if run from `install.sh`): `~/_bmad`, `~/_bmad-output/...`, `~/docs`, `~/.claude/skills/bmad-*` [UNVERIFIED write set] | None |
| HOME persistence across boots | Not applicable | On the persisted HOME volume `coder-<id>-home` (`main.tf:174-176, 594-597`); rewritten from the image's `install.sh` every boot; a new workspace gets an empty volume and the file at its first boot | On the persisted volume; created once by copy-if-absent | On the persisted volume; rewritten every agent start | Not in HOME: baked image file, rebuilt from the image at each container recreate; project output persists in the project | On the persisted volume (`~/.claude/settings.json`); re-merged each boot | Not in HOME: image file, rebuilt from the image | On the persisted volume; re-merged each agent start | On the persisted volume | n/a |
| Survives reboot and `superclaude install` | n/a | Survives (mounts; `install_skills.py:88-110`, `install_skill.py:46-52` replace per packaged name only; `superclaude install --force` runs at boot only on first boot or an IronClaude sha change, `ironclaude/install.sh:91-97`). Residual: no repo assertion that user skills survive, and a future pruning superclaude would change it (03 section 6) | Survives, same basis | Survives, same basis | Not touched by superclaude (outside HOME) | Survives: hooks merge additively by exact command and `ironclaude/install.sh:104-136` fails the ironclaude slug if a hook vanishes; lost-update race with other writers possible (`ironclaude/install.sh:139`); a hook script under `~/.claude/hooks/` needs a name outside the 14 managed names (`install_hooks.py:42-87`) | Not touched by superclaude (outside HOME); restored from the image each recreate | Same as D1 | Skills under `~/.claude/skills/bmad-*` are outside superclaude's managed names (inference, 03 section 6) | n/a |
| Visible in the same session after creation (external, [UNVERIFIED - doc-only, no code confirmation]) | n/a | Not watched if `.claude/skills/` did not exist at session start; needs `/reload-skills` or a restart | Same as B1 | Same as B1 | User runs it in a terminal first; the installer text says to launch the agent afterwards (`installer.js:1233`, [CODE-VERIFIED]); an already-running session is the doc-only case | SessionStart can return `reloadSkills: true`; no re-scan field found for UserPromptSubmit; hooks held back until workspace trust accepted | Same as D1 | Same as D1 | n/a | n/a |

**Table 2: further options G to I (lower research depth)**

| Criterion | G (instruction text in `~/.claude/CLAUDE.md`) | H (upstream plugin route) | I (managed skill location) |
|---|---|---|---|
| Effort | M (5 files) | L (no repo mechanism, web evidence only) | M (about 5 files, by analogy) |
| Risk | High (R2, R3) | High (R2, R3; plugin 6.8.0 versus pin 6.9.0) | High (R4, R5; UNVERIFIED path) |
| Maintainability | Second marker pair or generalised sync; two equality checks to keep | Second BMAD distribution to track | Image-versioned file |
| Integration complexity | `workspace_defaults/CLAUDE.md`, `claude-md-block.sh:23`, `startup.sh:1285`, 2 tests | `settings.json` plugin keys + plugin cache | COPY, `image_input_files`, test |
| Reuse potential | `aidev_claude_md_block_sync` | None found | D2 COPY pattern |
| Meets "no global BMAD install" | Yes for BMAD content; instruction text is user-level (owner question 1) | **No** (BMAD skills user-wide) | Yes for BMAD content; managed-level (owner reading) |
| Needs a change in IronClaude or IronOrca | No | No | No |
| Image rebuild or only a template push | Rebuild (seed file and `startup.sh`) | Not established | Rebuild |
| Image layers (gate 70, 68 used) | 0 if only the existing seed content changes (UNVERIFIED) | Not established | +1 as written (UNVERIFIED) |
| Pinned tests that break (names) | BREAKS-IF `test-startup-boot.sh:2083-2087, 3030-3037`, `test-74-claude-md-block.sh` | Not analysed by file 04 | Not analysed (UNVERIFIED) |
| Which reading of "first use" it satisfies | Opening a session, only if the model obeys the text (UNVERIFIED) | None by itself | Invoking a BMAD slash skill |
| Writes inside the whole-HOME snapshot | Inside: `~/.claude/CLAUDE.md` (fixture HOME copies it from skel, `mk_home`) | Inside: `~/.claude/plugins/cache/...`, `~/.claude/settings.json` | Outside: `/etc/claude-code/...` (UNVERIFIED path) |
| HOME persistence across boots | On the HOME volume; block re-synced each boot (`startup.sh:1282-1285`) | HOME volume | Image-baked |
| Survives reboot and `superclaude install` | Survives: `superclaude install` saves and restores `CLAUDE.md` byte-for-byte (`ironclaude/install.sh:44-86`) and the block is re-synced | Not established | Not touched by superclaude |
| Visible in the same session after creation | Not applicable (text, not files) | Not established | Not established |

**Run-only facts that apply to every option and stay UNVERIFIED** (an implementation phase must observe them in CI, not in one-off scripts): real install duration in a workspace and in a large repo (R-1); writes under HOME and network effects of the installer (R-2); behaviour in a directory with no `.git` (R-3); the exact per-file list including the `{output_folder}` substitution (R-4); skill count 46 versus 47 (R-5); skill behaviour with `_bmad/` or some config keys missing (R-7, R-8); state left by a failed first run and what quick-update does to it (R-10); whether the manual command completes end to end (R-11); what E writes (R-12); the seed-repo result of the boot install in a fresh workspace (R-14); layer count after the chosen change (R-15). Tests were not run, so whether they pass today is UNVERIFIED (gaps G-20).

**Contradictions between research files and how they were resolved** (codebase evidence outranks web evidence):

| # | Contradiction | Resolution |
|---|---|---|
| 1 | Files 02 (U4, U6), 04 (gap 1, section 7 F column) and 05 (U1 to U3) call F's mechanism UNVERIFIED; file 01 sections 2 and 5 say CODE-VERIFIED "zero consumers". | File 01 plus web-02's tarball Grep govern; F's "X" cells are void (gaps G-25). |
| 2 | File 04 section 7 marks "B" and "D" as breaking `test-57:450`; file 05's earlier text said "B and D leave every row unchanged". | Both true for different questions: breaks apply to B1, D1 (delivered by `install.sh`), not to B2, B3, D2, D3; the first-use execution breaks nothing because no test runs it (05 F1.4). |
| 3 | File 02 treats adding a B2 skill to the `Dockerfile.coder:547-548` COPY as a zero-layer fold; file 04 (earlier) said it breaks `test-60`. | `test-60:87-88` allows it (one config COPY line, three sources, last token `/usr/local/lib/aidev/`); the fold stays UNVERIFIED as a build (U18). |
| 4 | Files 02 and 03 say the `Dockerfile.coder:468` comment "no headroom"; CI logs show 68 of 70. | 68 of 70 governs; the comment holds only as a policy (02 A4, C8). |
| 5 | Gaps log Q-1 says the settings docs do not decide mid-session skill pickup; web-01 says the skills page does, with a split answer. | web-01 (doc-only) is used as a caveat only; the code cannot decide it. |
| 6 | File 01 section 6 item 3 versus section 7.2 on where the root walk starts (E). | Neither was run; E's rating does not depend on it. |

## 7. Recommendation

### Recommended approach

The evidence ranks the options but cannot choose the trigger, because the trigger depends on two owner readings that no code or document settles (is a user-level stub allowed; what counts as first use). The recommendation is therefore an explicit sequence in which only the last step waits for the owner.

```
 Which event counts as "first use"?       Mechanism that fires there              User-level artifact needed?
 ---------------------------------------  --------------------------------------  ---------------------------
 user types the documented command        A  manual `bmad install ...`            no
 (1) a `bmad` CLI command is run          C  wrapper / new command (image)        no
 (2) a BMAD slash skill is invoked        B  stub skill (HOME), or I (image)      yes for B; no for I (doc-only)
 (3) a session is opened in a project     D  hook (HOME or image), or G text      yes for D1, D3, G; no for D2
```

| Stage | Action | Why (comparison rows) |
|---|---|---|
| 0, now, under every reading | (a) Record the decision as OD-4 with a memlog bullet and a re-derived SPEC (common fact 12) worded "no global or user-level install of BMad framework content; first-use creation per project", and answer the "available globally" text of #478 as declined. (b) Do Option A's documentation half: reconcile `README.md:241`, keep the manual command in the README and the welcome text, fix the unconditional "already set up" wording (02 C7). (c) Define once the install command and FIRST_USE(P) of common facts 3 and 4, with the plan decisions D-1 (atomicity), D-2 (guard on `_bmad/config.toml` rather than `_bmad/`), D-3 (subfolder of a repo) and D-10 (hidden or visible files). | Every other option still needs the documents because a mechanism may not fire (05 b3); the command and predicate are identical for B, C, D, G and I (03 A3). |
| 1, after the owner answers | Build only the trigger the owner's two readings select (table "Dependence on the owner readings"). Evidence-ranked choice inside each family: skill trigger **B3** before B2 before B1; CLI trigger **C in place** (or a new command name); session trigger **D3**, or D2 if the owner treats the managed level as not "user level" and accepts one layer. | Effort, Risk, Pinned tests, Writes-inside-snapshot, Image rebuild and Image layers rows. |
| 2, inside the plan | Add the missing delivery proof for the chosen option (04 A.11: pin beside `test-52:1374-1377` for B3 and D3; `test-startup-boot.sh:2775` and `test-22:271` for B2; `test-73` second-file check for D2; replacement of `test-57:450` only if a boot-time write is chosen). Observe in CI, not in one-off scripts, the Claude Code facts that only docs answer today: that the image's Claude Code loads the stub or runs the hook, whether new project skills appear in the same session, and whether Claude follows the stub text (gaps G-01 to G-04, G-08, UV-17). Observe the run-only facts listed under the comparison. | Common facts 7, 11; the doc-only caveats of Table 1. |

Not recommended: **E** (installs framework content under HOME and leaves the project's `_bmad/` absent), **F** (no code path in 6.9.0, 6.10.0 or 6.12.4), **B1** and **D1** (certain break of `test-57:450`, the only "writes nothing" oracle, and a rewrite of HOME at every boot), **B2** (6 files, copy-if-absent text frozen for the life of a workspace, uses one of the two free layers unless the unverified fold holds), **G** (two existing equality checks, instruction text with no enforcement), **H** (user-wide BMAD skills, version 6.8.0 versus pin 6.9.0, does not create `_bmad/`), **I** (rests on a docs table; unevaluated by the codebase research).

### Rationale

| # | Reasoning | Comparison rows it rests on |
|---|---|---|
| 1 | The decision asks for creation on first use, so A alone fails it; A stays as the documentation half. | Effort/Risk row A; common fact 12 |
| 2 | E and F fail on code: F has no consumer of `global_target_dir` anywhere (01 section 2; web-02 tarball Grep for 6.9.0, 6.10.0, 6.12.4); E writes framework content under HOME and does not create the project `_bmad/` the skills read. | "Meets no global install" row |
| 3 | B1 and D1 are the only in-repo mechanisms with a certain pinned-test break (`test-57:450`), because they are delivered by `catalogue/bmad/install.sh`, the one script `test-57` runs; B2, B3, D2, D3 never pass through it. | Pinned tests row; Writes-inside-snapshot row |
| 4 | Among skill deliveries B3 is cheapest and least exposed: template push only, 0 layers, no certain break, refreshed at each agent start, count-gated by profile. Its price is a split of BMad logic across `modules.tf` and the slug, and the absence of any existing delivery proof. | Effort, Risk, Image rebuild, Image layers, HOME persistence rows |
| 5 | The hook family acts in every project, so it installs everywhere instead of on first use, runs without a user prompt (documented by inference only), and for D1 and D3 shares `settings.json` with writers that have no lock; D2 costs one of two free layers, is image-wide, and depends on an unconfirmed doc claim that a drop-in may hold hooks. That is why D is only recommended for reading (3), and then in the D3 or D2 shape. | Risk row; Which-reading row; Survives row |
| 6 | C is the only Claude-independent mechanism with no HOME artifact and no certain break, but it serves the narrowest reading: `bmad install`, `--version` and `--help` must pass through unchanged, so the wrapper can act only on other subcommands or a new command name. | Pinned tests row; Which-reading row |
| 7 | Nothing in the repo or in the superclaude package needs to change for B, C or D, and a user skill or hook under a new name survives `superclaude install --force`. | Needs-change-in-IronClaude-or-IronOrca row; Survives row |
| 8 | Everything beyond A and C leans on Claude Code behaviour that only official docs answer. Those facts are used here as caveats and as items for live observation, not as grounds for a rating. | Tag key in 6.0; doc-only rows |

Prior positions overridden by name (research-notes F9-3), so the spec for #478 can cite them: R1 and R2 (behaviour "documented", first-use creation "open owner decision"); R4 (`SPEC.md:77` for the first-use part, not the seed install); R5 (`spec-orca-catalogue-bundle/SPEC.md:141` for repos cloned after boot, not for Orca-created worktrees); R6 ("Restrictions overridden: None", "no BMAD change"); R8; R9 (README-only scope); R10 ("MUST NOT change" for `install.sh` and `manifest.yaml`); R12 (the "DANGEROUS" label for a user-level skill; it is presented here on its merits). Not overridden: R3 (global and user-level install of BMAD framework content stays declined; whether a content-free stub is "user level" is open), R7 (the boot seed install stays), R15 (report truthfully; `install.sh:60` prints "install ok" even with no seed), R16 (skills need the project's own `_bmad/`).
### Feasibility statement

**Can the ask be met without a global BMAD install?** Yes. First-use creation is per project: the image-baked CLI runs `bmad install --directory <project> --modules bmm --tools claude-code --yes`, which by the code writes only inside that directory. Evidence: 01 line 386 (Summary): "a non-interactive install is `bmad install --directory <dir> --modules bmm --tools claude-code --yes`, and by the code it writes only inside that directory (`_bmad/`, `_bmad-output/{planning,implementation}-artifacts/`, `docs/`, `.claude/skills/bmad-*`), never touches git or `~/.claude`"; 01 line 79: "in 6.9.0 there is NO consumer of `global_target_dir` ... Option F ... has no code path", so a global or user-scope BMAD install is neither available nor needed (research-notes F9-4: per-project creation "is not in conflict with the 'never globally' half of OD-1"). [CODE-VERIFIED; nothing was run.]

**Can it be met without a change in IronClaude or IronOrca?** Yes. Evidence: 03 section 6, lines 178 and 179: user-level skill, "NEEDS OTHER-REPO CHANGE: **NO**. Every placement mechanism above is in this repo ... and superclaude leaves a non-packaged skill name alone"; user-level hook, "**NO**. A hook entry with a new command string is preserved by superclaude's additive merge". It would become YES only if the skill or hook were shipped from IronClaude or superclaude started pruning unknown skill directories, which it does not today (03 line 180, `install_skills.py:97`, `install_skill.py:48`). Option C and the other image-level hook points are also inside this repo (02 lines 324-325). No IronOrca file was needed for any option.

**Stop condition: not triggered.** No re-scope is needed on the evidence in hand.

Limits that keep this open (none contradicts the statement):

| # | Limit | Evidence |
|---|---|---|
| 1 | A slash skill cannot be invoked in a project that never had BMAD unless something outside the project supplies its name: BMAD skills land in the project only through the install (`.claude/skills/bmad-*`, 01 section 5), and the live `~/.claude/skills` holds no `bmad-*` entry (03 section 4). So the reading "invoking a BMAD slash skill" needs a user-level or managed artifact (B or I), or a session-start install (D) that makes the skills exist earlier. | 01 section 5; 03 section 4 |
| 2 | Whether a user-level stub or hook works at all in the image depends on Claude Code behaviour that research could only read in official docs: user skills are loaded for all projects, hooks run for all projects, hooks wait for workspace trust, a new top-level `.claude/skills/` needs `/reload-skills` unless a SessionStart hook returns `reloadSkills`, hooks in a managed drop-in are documented by inference. [UNVERIFIED - doc-only, no code confirmation; the image's Claude Code version is not established.] If a live check in the image shows the stub is not loaded or the hook does not run, B and D fail and only A and C remain in-repo; then the readings (2) and (3) would need a re-scope discussion with the owner. | web-01 key findings (a) to (f) |
| 3 | The owner may combine "no user-level artifact of any kind" with "first use = invoking a BMAD slash skill" or "opening a session". Only I and D2 remain for that combination, both resting on doc-only claims, so the evidence does not settle it. | table below, rows 3 and 5 |
| 4 | Version skew and a partial `_bmad/` are not protected by the installer (common fact 11); FIRST_USE(P) is the only barrier. | 01 F5-D, F5-F |
| 5 | 6.9.0 behaviour that only a real run shows (duration, exact file list, no-`.git` case, partial-tree repair) is UNVERIFIED. | gaps section 7 |

### Dependence on the owner readings

Open owner questions, copied unanswered (gaps section 5; BUILD-REQUEST.md:14 holds the only decision text): **Q1** is a content-free user-level stub (a skill, command or hook under `~/.claude/`, with no BMAD content) allowed, given the 2026-09-25 text "never globally or at user level" (`.memlog.md:32`) and the 2026-11-07 text "Global installation of BMAD is NOT requested"? **Q2** what counts as first use: running a `bmad` CLI command, invoking a BMAD slash skill, or opening a session in a project? The documents themselves say "per project only, never globally" about framework content while the CLI is global (05 C1), which hints at a narrower meaning of "user level" but does not decide it.

| # | Q1 (stub allowed) | Q2 (first use) | Options that remain | Recommendation under this reading | What changes in the plan | What the evidence cannot settle |
|---|---|---|---|---|---|---|
| 1 | Any | Running a `bmad` CLI command | A, C | Stage 0 plus **C in place** (or a new command name). `bmad install` already creates the directories, so C adds value only for other subcommands or a new command (Table 1, Which-reading row). | `Dockerfile.coder:142`; `manifest.yaml` welcome text; `test-19`, `test-57` seeded-run checks kept; no HOME artifact, so `test-57:450` untouched. | Whether the owner wants anything beyond the documented command; end-to-end completion of the manual command (R-11). |
| 2 | Yes | Invoking a BMAD slash skill | B (B3, B2, B1), I | Stage 0 plus **B3**. | `modules.tf` resource count-gated on `bmad`; stub name outside `preview`/`share`/`share-port`/`expose`/`dev-preview` and outside superclaude's and Orca's names (and, per docs, not `bmad-*`); new pin beside `test-52:1374-1377`; a note telling the user to run `/reload-skills` or restart; cleanup rule for `minimal`/deselected profiles (gaps D-4, D-5). | Whether the image's Claude Code loads a user-level stub and whether Claude follows the stub text (doc-only, UV-17). |
| 3 | No | Invoking a BMAD slash skill | I (doc-only), or D2 changing the reading to (3) | No option in the repo is supported by code-traced evidence. Put the combination to the owner; do not build B. | Re-scope conversation if a live check shows I and D2 do not work in the image. | Whether a managed skill location exists and takes a stub (path UNVERIFIED); whether "managed" counts as "user level". |
| 4 | Yes | Opening a session in a project | D (D3, D2), G | **D3** only if the owner accepts install-everywhere. Prefer SessionStart over UserPromptSubmit [doc-only]. | `modules.tf` jq merge modelled on `ironclaude/install.sh:100-136`; a hook command without `/.claude/hooks/`; timeout far above 10 s or a background install; guard FIRST_USE(P) in the hook; merge-fixtures for `settings.json` (C-F1-3). | Whether first use should mean "every project"; hook trust hold-back and timing; whether the hook output is shown to the user. |
| 5 | No | Opening a session in a project | D2 | **D2** if the owner treats the managed level as not "user level" and accepts one layer (68 to 69) and an image-wide hook that applies to `minimal` too. | New `20-*.json` drop-in, its own COPY line, `main.tf:80-101`, second-file check in `test-73-claude-retention.sh`. | Whether a managed drop-in may hold hooks (documented by inference only); whether the owner counts `/etc/claude-code` as user level. |

Other open owner inputs that change the plan but not the ranking (gaps G-26, section 8): whether first-use files are hidden with the three `info/exclude` lines of `install.sh:32-34` or left visible (D-10); whether the decision covers Orca-created worktrees (`SPEC.md:174` says "project"); whether the `minimal` profile is covered (D-4); whether deselecting bmad should remove a user-level artifact (D-5).

## Self-Audit (not a report section)

**What I read.** Fully: `gaps-and-questions.md`; research files 01, 02, 03, 04 (lines 1 to 541), 05 (lines 1 to 417), web-01, web-02; `research-notes.md` lines 60 to 232 (solution table, suggested phases, ambiguities, addendum F9); `BUILD-REQUEST.md`; `qa/qa-gate1-decision.md`; the `synth-01` stub (header only). I read the Summary and Key Takeaways blocks of every research file (01 Summary and section Key Takeaways; 02 Summary and Key Takeaways (a) to (e) and addendum A8; 03 Summary and the A5 summary; 04 Summary and addendum summary; 05 Summary and F1.6; web-01 and web-02 Key External Findings and Recommendations). Fix-cycle addenda were applied over earlier text (for example F tags from 01 over 02/04/05; the test-60 fold from 04 A.3 and A.9 over its earlier advice; option C no longer "invisible to test-57" per 05 F1.1).

**Searches and checks.** One Glob of the task directory (confirmed the 7 research inputs exist and `synth-02` does not yet); one Grep of headings in files 01, 04 and 05 to locate sections. I did not open product code, tests or the installed packages: every file:line in this file is as reported by a research file, so none was re-read for freshness. Nothing was executed.

**Key findings traced into this file.**

| Research key finding | Where it appears |
|---|---|
| 01: no first-use bootstrap; non-interactive command; writes only in the directory; `resolve_config.py` exits 1; no skill detects missing `_bmad/` | common facts 2, 3; Feasibility |
| 01: `global_target_dir` has zero consumers; ancestor check is dead; E leaves project `_bmad/` absent | Options E, F; contradictions 1 and 6 |
| 01: version skew, partial `_bmad/`, `--output-folder` must stay, duration figures not to be blended | common facts 3, 11; run-only facts |
| 01 section 8 (OBSERVED-FROM-6.10.0-TRACKED-TREE rows) | Excluded as a basis for any rating (tag key in 6.0) |
| 02: wrapper has no logic; slug is seed-only; hook points B1 to D3; health blind; minimal profile; layer budget 68 of 70; Renovate strings | Options B, C, D; common facts 6, 9, 10; Options A and C rows |
| 03: HOME volume persists; `superclaude install` merges and replaces per packaged name; no other-repo change; FIRST_USE(P); walkthroughs; `block-bare-python.sh` | common facts 4, 14; Table 1 rows persistence/survives; Feasibility |
| 04: single `test-57:450` oracle; snapshot path list; per-variant certain breaks (B1, D1, E); BREAKS-IF sets; missing delivery proofs; new assertion texts | Table 1 rows; Option B/C/D tables; Stage 2 |
| 05: decision trail, OD-4, README:241, welcome text constraints, Renovate rows, startup-boot rows, "framework content" wording nuance | common facts 5, 12; Option A; Q1 text; overridden positions |
| web-01 (a) to (f): live pickup split answer, `reloadSkills`, trust hold-back, timeouts, precedence, drop-in by inference, managed-only keys | Option B shared points, Option D step 7, Option I, Table 1 doc-only row; tagged doc-only |
| web-02: no consumer through 6.12.4, plugin route, issues #1852 and #2677, v7 preview | Options E2, F, H; contradictions |

**Excluded or reduced, with rationale.** The stale "T1-T55" project-index claim and CHANGELOG convention details do not change any option and belong to synth-04 (evidence trail, plan). The 6.12.4 `uv run` change and the v7 preview are reduced to the F and pin-bump note because a pin bump does not enable F and is a separate plan. Upstream issue #2624 (trust concern about auto-created `_bmad/scripts/`) is not used here; it is an open-question item for synth-04. The 12 files of `.dev/issues/478/` are process context and are not options evidence. The test-suite residuals of gap G-20 (unread test blocks, tests not run) are summarised as "tests were not run".

**Why I believe nothing was dropped or invented.** Every option A to F named in the prompt has its own section with the six required rows; G, H and I are the further options the research itself surfaced (02 section 6.1, web-02 section 9, web-01 section 1.1). All required comparison rows are present in Table 1 and Table 2, including "Writes inside the whole-HOME snapshot", "HOME persistence across boots" and "Survives reboot and `superclaude install`". The Feasibility statement, the Dependence table and the overridden-positions list are present. Cells that no research file settles say UNVERIFIED (B2 fold, C late-COPY, D2 hook acceptance, I path, E write set, G and I layers). The rating rubric (effort and risk keys in 6.0) is this synthesis's own method and is labelled as such; effort for G, H and I is by analogy or from web evidence and says so. Effort and risk ratings cite file counts, a persistence or rebuild consequence, or a named test change.

**Contradictions and gaps.** Six contradictions between research files are listed under the comparison with their resolution; I found no further ones. Open gaps carried, not closed: owner questions Q1 and Q2; Claude Code behaviour in the image (doc-only); install duration, per-file list, no-`.git` behaviour, partial-tree repair (run-only); test pass state today; the Sysbox-runtime layer count. No out-of-scope topic is discussed, and no `STOP AND RE-SCOPE` verdict is raised because the evidence does not trigger it (limits are stated in the Feasibility statement).

