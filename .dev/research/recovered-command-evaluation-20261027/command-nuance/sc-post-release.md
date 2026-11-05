# /sc:post-release: scope x complexity nuance

**Generated**: 2026-10-27 by nuance-post-release agent (read-only; only this file written)
**Brief**: `command-nuance/_brief.md` (R scope = multi-feature release; `/sc:task` and `/sc:tasklist` retired; one-off minimum is PROPOSED)
**Files read in full**: `~/.claude/commands/sc/post-release.md` (86 lines), `~/.claude/skills/sc-post-release-protocol/SKILL.md` (354), `refs/{workstream-playbook,additive-diff,fan-out-pattern,golden-rule-evidence}.md`, `templates/post-release-{report.md,manifest.json}`. Repo checks were read-only (`git tag`, `git for-each-ref`, `git show`, `ls`, `cat`).
**Citation shorthand**: CMD = `~/.claude/commands/sc/post-release.md`; SKILL = `~/.claude/skills/sc-post-release-protocol/SKILL.md`; PB = `refs/workstream-playbook.md`; AD = `refs/additive-diff.md`; REPO = `/home/coder/workspaces/worktrees/Coder/IB-CPlus-01`.

<!-- SECTION 1 -->
## 1. Status and role

- **Does**: "synchronize and create a shipped version's entire external surface: user docs, technical docs, install/deploy scripts (validated by real end-to-end runs), and human-run e2e test guides. Runs AFTER the release gate tags a version" (CMD:3). Phase: Post-merge / Release only. Not retired; standalone-invokable as `/sc:post-release <version>` (CMD:18); the protocol skill is never invoked directly (SKILL:30).
- **Overlaps**: `/tech-reference`, `/operational-guide`, `/readme`, `/sc:document` (doc writing), `bmad-qa-generate-e2e-tests` (automated e2e tests; this command writes guides a human runs by hand, SKILL:189). It does NOT call `/sc:task` or `/sc:tasklist`: a grep of CMD, SKILL, refs and templates finds neither name; SKILL:153-159 only says "the project's" task-decomposition, execution and reflection tooling, optional, with a direct-write fallback.
- **Hard precondition**: an existing git tag for `<version>` (CMD:15; SKILL:71-73). It is the tail of an R or N, not a step inside the release PR.

<!-- SECTION 2 -->
## 2. Flags

Only two inputs exist. The `--xxx` strings elsewhere in the protocol (`--help`, `--version`, `--admin`, `--debug`, `--watch`, `--base`) are examples of the target repo's flags or of `gh`, not flags of this command (grep of CMD + SKILL + refs).

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `<version>` (required) | an existing tag name, e.g. `v1.4.1` (CMD:15,35); SKILL:71 matches exact tag, else a tag whose name contains it | none: STOP if absent (SKILL:72) | Chooses the tag the whole scan is anchored to (SKILL:91). Untagged version: STOP unless the user confirms a pre-tag run (SKILL:73,303) | A tag exists on `origin/main` lineage. Here pass the full tag text, e.g. `aidev02-v2-m2` (REPO tags are not `vX.Y.Z`) | No tag cut yet; use `/tech-reference` or `/operational-guide` instead |
| `--output` | directory path (CMD:28,36) | `docs/testing/<version>/` (CMD:36; SKILL:223). Fallback `.dev/releases/current/<version>/test-guides/` when the repo keeps release artifacts under `.dev/` (SKILL:223). Ambiguous convention: confirm with the user (SKILL:75,225) | Where report, manifest, `audit.log` and test guides land (CMD:36; SKILL:223). Also where the NEXT run finds the manifest: mode detection globs `.dev/releases/**/post-release-manifest.json` and `docs/testing/**/post-release-manifest.json` (SKILL:96) | Always in this repo: `docs/testing/` does not exist here, `.dev/releases/current/` does, so the default is "ambiguous" and triggers a confirm prompt. Prior run passed `--output .dev/releases/current/v2-m2/post-release/` (REPO report header) | Never omit it when a prior manifest lives elsewhere: a run-mode miss turns an additive run into ground-up (SKILL:98) |

**Does not exist** (not defined in CMD or SKILL, both read in full): `--ground-up` / `--additive` (mode is auto-detected, "do not ask", SKILL:93); `--prev-tag` (auto-detected by `git tag --sort=-creatordate`, SKILL:76); `--workstream` / `--skip-e2e` (A-E are all run; one-shot vs decompose is the controller's per-workstream judgment, SKILL:148-157); `--depth`; `--dry-run`; `--commit` / `--pr` (commit and PR are only offered as a next step and need confirmation, SKILL:324,340,351).

**Frontmatter oddity**: CMD:6 `allowed-tools: Read, Glob, Grep, Skill`, but SKILL:4 needs `Edit, Write, Bash, Task, TodoWrite` and the skill comment (SKILL:15-23) says unrestricted Bash is intentional. Whether the narrower command list blocks the skill is UNVERIFIED; the 2026-07-09 run produced all artifacts, so in practice it works.

<!-- SECTION 3 -->
## 3. Scope x complexity matrix

### 3.1 What the command needs before it can run, and whether this repo has it (read-only checks, 2026-10-27)

| Need | What the files say | This repo | Met? |
|---|---|---|---|
| A tag for `<version>` | CMD:15; SKILL:71-73 STOP if none (unless user confirms a pre-tag run) | Two annotated tags, both on `origin`: `aidev02-v1.0` (2026-06-22, "AIDev02 v1.0 GA") and `aidev02-v2-m2` (2026-07-09, "V2-M2 convergent hybrid"). Both are ancestors of `origin/main` (`merge-base --is-ancestor`). No `vX.Y.Z` tags (`git tag --list 'v*'` empty). 763 commits and 245 merge commits on `origin/main` since `aidev02-v2-m2`, no tag | YES, but names are `aidev02-v*`, and none since July |
| A "release gate" that tags | CMD:3,15 assume one; neither file defines it | No workflow in `.github/workflows` creates a tag or GitHub Release (grep for `git tag`, `gh release`, `create-release`, `softprops`, `on: release`: only unrelated Tailscale `tags:` and Orca upstream `tag_name` reads). `gh release list` returned no rows. `docs/operations/aidev02-operator.md:639` says "AIDev02 GA is the v1.0 git tag cut in Phase 8 (T08.27)": a manual, operator-cut tag | NO automated gate; a human cuts the tag. The command only needs the tag |
| Release intent source | SKILL:77: per-version dir under `.dev/releases/{current,complete}/` (may be tag-fuzzy), else `CHANGELOG.md` + `RELEASES.md` | `.dev/releases/current/v2-m2/` matches `aidev02-v2-m2` fuzzily (briefing, research, TDD). `RELEASES.md` absent. Root `CHANGELOG.md` has only `[Unreleased]` (line 20) and `[1.3.0] 2026-05-19` (line 167); same at the tag (`git show aidev02-v2-m2:CHANGELOG.md`). The v2-m2 release notes the prior run used are in the payload changelog `templates/VSCode-AIDev02/aienv.d/CHANGELOG.md:59` (`## [20260701-1] - 2026-07-01`). The current payload `aienv.d/VERSION` is `20261016-1`; it is a payload stamp, not a git tag | PARTIAL: root CHANGELOG does not carry the tags; release dir does |
| Prior manifest (decides additive vs ground-up) | SKILL:95-99 globs | `.dev/releases/current/v2-m2/post-release/post-release-manifest.json`, tracked in commit `60f5ff85` (2026-07-09); the SKILL:96 glob finds it, so the next run auto-selects additive | YES. Caveat: it is additive over `v1.0..v2-m2` only (manifest `run_mode_note`) and all 13 `feature_inventory` entries are `added_in: aidev02-v2-m2`; the v1.0 GA surface was never inventoried (AD:60-62 stale carry-forward; SKILL:101 "prefer ground-up when in doubt") |
| Output directory | CMD:36 `docs/testing/<version>/`; SKILL:223 fallback `.dev/releases/current/<version>/test-guides/` | `docs/testing/` does not exist; `.dev/releases/current/` does. Prior run used neither default (explicit `--output`) | AMBIGUOUS: expect a confirm prompt unless `--output` is passed |
| Workstream C target | SKILL:127-134, PB:76-110 | Prior run class `local-deploy`: throwaway HOME, scripts from `git archive` of the tag; full terraform-to-Coder-platform provision (`vm-e2e`) NOT exercised, no live platform (manifest `install_surface_note`) | Shell-level only. A `vm-e2e` run needs a live platform and a confirm (SKILL:340,351) |

**Verdict**: the repo meets the one hard precondition (a tag exists and the command has run once on it). There is nothing new to run it on today: the last tag is 2026-07-09 and every merge since (763 commits) is un-tagged, so a missing post-release for those merges is not a skipped step. The earlier open question (value file U14, "does the team tag?") is answered: yes, twice, rarely, with a manual cut.

### 3.2 Does the command vary by complexity?

Not by anything the engineer types: there are no flags that change depth (Section 2). Complexity changes what the controller does inside the run: one-shot versus decompose per workstream (SKILL:148-157) and, in additive mode, re-run versus carry forward Workstream C (AD:42). So the matrix below is about WHETHER to run it, and the bands predict how heavy the run is.

**Bands (signals from files; thresholds are JUDGMENT)**

| Band | Signals a checker or engineer can read on disk |
|---|---|
| LOW | Additive run. `git diff --name-only <prev_tag>..<tag>` (AD:13) maps to no user-facing, install or sysop surface, or to a few A/B doc edits only (AD:30). Install surface unchanged, so C is carried forward with an explicit statement (AD:42). One-shot per workstream (SKILL:150). |
| MEDIUM | Additive. Several user-facing or sysop capabilities new or changed (AD:22-26), or install files changed so C re-runs on the changed path (AD:29,42). Class `package` or `local-deploy` (SKILL:130-131). Calibration, the only observed run: `aidev02-v1.0..aidev02-v2-m2` = 84 commits, 13 capabilities, `local-deploy`, all five workstreams, 1293 s (`audit.log` `duration_sec`). (J) |
| HIGH | Ground-up (no prior manifest, SKILL:98), OR class `vm-e2e` (SKILL:129), OR a stateful service whose migrations must be proven (PB:100), OR a surface no earlier manifest covered (this repo: the v1.0 GA surface). Decompose path with itemized worklist (SKILL:151-157). |

### 3.3 Matrix

`(J)` = my judgment, not a file's statement. No file rates this command REQUIRED anywhere: `HOW-WE-WORK.md:279` lists it only as "After tagging a release." in the "Other commands" table; it is not one of the six levels and not in Ryan's pipelines (brief, ruling 5).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | N/A (no tag) | N/A | N/A |
| B bug fix | N/A (a hotfix tag, if ever cut, is an R-sized event, not B) (J) | N/A | N/A |
| S single story | SKIP (J): a single feature's release is a phase inside S (brief, ruling 2); use `/tech-reference` or `/operational-guide` | SKIP (J) | SKIP (J) |
| F multi-story feature | SKIP (J) | SKIP (J) | OPTIONAL (J): only if the feature itself is tagged AND changed install/deploy files; else `/operational-guide` |
| R multi-feature release | OPTIONAL (J): `<tag> --output .dev/releases/current/<short>/post-release/`. If the delta touches no external surface, the run records "internal only" (AD:30-32) | WORTH IT (J): same flags | WORTH IT (J): same flags; first run over a never-inventoried surface should be ground-up (SKILL:101) |
| N new product | OPTIONAL (J): `no-install-surface` class, run yields an honest gap + quickstart (SKILL:132) | WORTH IT (J): package class, install proven in a fresh venv/container (PB:97) | WORTH IT (J): always ground-up (first release has no manifest, SKILL:98); this is where C and D/E guides pay most |

All rows assume a tag exists. With no tag the cell is N/A regardless of scope (SKILL:73).

<!-- SECTION 4 -->
## 4. Choose this or the neighbour

Neighbour descriptions come from the session skill list and `command-value-by-phase.md` (VAL) rows; I did not read the neighbours' own skill files (UNVERIFIED beyond the descriptions). The deciding difference is always the same: `/sc:post-release` is anchored to a TAG, covers the WHOLE external surface, and PROVES the install by a real run.

| Neighbour | Pick the neighbour when | Pick `/sc:post-release` when |
|---|---|---|
| `/tech-reference` (VAL:189, O11 VAL:237) | One built feature (S, F), no tag, only an architecture/implementation reference is missing. Guide 3.1 step 11 | A tag was cut for a multi-feature release (R) and user docs, tech docs, install path and test guides must all match the tagged commit (SKILL:41,59) |
| `/operational-guide` (VAL:190) | One deploy, setup or ops procedure changed (e.g. `docs/operations/*`), no tag, no need to run it clean | Install/deploy scripts changed across a tag and the new-user path must be re-run to green with a transcript (SKILL:187; PB:91-100); this command fixes scripts and writes the quickstart, not just a doc |
| `/readme` (VAL:191) | A new package or module needs a README | The README is one of several stale user docs for a tag (PB:46-56 splits mixed READMEs into A and B) |
| `/sc:document` (VAL:192) | One-pass reference text for specific code (`--type api`) | Never as a substitute: no tag anchoring, no e2e |
| `bmad-qa-generate-e2e-tests` (VAL:151) | You want AUTOMATED end-to-end tests for existing features | You want step-by-step guides a human runs by hand: preconditions, actions, expected result, pass/fail, expected results traced to code (SKILL:189; PB:116-122). They do not conflict; D/E guides are not tests |
| `/sc:release-split` (VAL:72) | Before the build, deciding whether to split the release | After the tag. Different phase; no overlap |
| `bmad-retrospective` (VAL:187) | Lessons learned after an epic | Not an overlap: retrospective reviews the work, this command documents the product surface |

Sequencing inside an R (judgment): `/sc:pr-submit` merges the release PR, a human cuts the tag (3.1 above), THEN `/sc:post-release <tag>`. Its own commit and PR follow the same rules as any other branch: feature branch off the auto-detected default branch, commit and PR only on confirmation, PR target from `git remote -v` (SKILL:347-348, 340). Running it before the tag (pre-tag run) is allowed only after explicit user confirmation (SKILL:73).

<!-- SECTION 5 -->
## 5. What a scheduled checker can see

Strong footprint. Unlike most commands it writes a machine-readable record. Spec: SKILL:218-296. Observed (not just specified) for the one prior run in `REPO/.dev/releases/current/v2-m2/post-release/`, all tracked in commit `60f5ff85`.

| Artifact | Where | What to read | Source |
|---|---|---|---|
| Run record | `<output-dir>/audit.log` | First `SC:POST-RELEASE:RUN` block (`version`, `previous_tag`, `run_mode`, `install_surface_class`, `caller`); last `SC:POST-RELEASE:RESULT` block (`status: success\|partial\|failed`, `c_e2e_result: green\|red\|carried-forward\|not-applicable`, `workstream_results`, `gap_list`, `duration_sec`). Aborted run: final `{wave: exit, status: aborted, reason}` line | SKILL:227-235,247-277; observed in REPO audit.log |
| Report | `<output-dir>/post-release-report.md` | Its first block repeats the RESULT header | SKILL:221,263; observed |
| Manifest | `<output-dir>/post-release-manifest.json` | `version`, `tag`, `previous_tag`, `run_mode`, `install_surface_class`, `workstreams.C_install_deploy.e2e.{ran,result,transcript,carried_forward_from}`, `workstreams.E_sysop_e2e_guides.sysop_capabilities_found` | template `post-release-manifest.json`; observed |
| Guides and transcript | `<output-dir>/user-e2e-guide.md`, `sysop-e2e-guide.md`, `c-e2e-transcript.txt`, `coverage-matrix-and-gaplist.md` | File names are NOT fixed by the skill (it names the templates `user-test-guide.md` / `sysop-test-guide.md`, SKILL:189-191; transcript path is a free field, SKILL:295); these names are what the one prior run chose | observed only |
| Doc/script edits (A-C) | wherever the repo keeps them | Listed in the manifest `updated` / `created` arrays; no distinctive marker in the files themselves | manifest; UNVERIFIED beyond that |

**Trigger for "should have run"** (a checker's best signal, judgment): a git tag in `git tag --list` (and on `origin`) whose name appears in no `post-release-manifest.json` `tag` field found by `.dev/releases/**/post-release-manifest.json` or `docs/testing/**/post-release-manifest.json` (the skill's own search, SKILL:96).

Current state by that rule (verified 2026-10-27): `aidev02-v2-m2` has a manifest; `aidev02-v1.0` has none of its own. That is a historical, explained gap: the 2026-07-09 run was user-directed additive over `v1.0..v2-m2` because no prior manifest existed (manifest `run_mode_note`), so a checker must not flag it retroactively.

A red result (`c_e2e_result: red`, `status: partial|failed`) is a valid, honest outcome (SKILL:306; refs/golden-rule-evidence.md:3,17) and still counts as the step done.

<!-- SECTION 6 -->
## 6. Expected-step rule

- **Expected** only when scope is R or N AND a new git tag exists with no matching manifest `tag` (Section 5 trigger). Then the expected footprint is `audit.log` with RUN and RESULT blocks, report, manifest, and (MEDIUM/HIGH) the guides. Grace period is a judgment call; this repo cut no tag in the 3.5 months since 2026-07-09, so a window based on merges instead of tags would wrongly flag all 245 merges.
- **Absence is fine** for T, B, S, F (no tag, SKIP/N/A in Section 3), for any R or N with no new tag, and for R-LOW where the delta touches no external surface (OPTIONAL: the run may legitimately be skipped or end as "internal only", AD:30-32). A short path that skips it is legitimate. A pre-tag run also exists and needs user confirmation (SKILL:73), so a run dated before the tag is not an error.

<!-- SECTION 7 -->
## 7. Proposed changes to command-value-by-phase.md

Proposals only; that file is not edited. Line numbers are from the file as read 2026-10-27.

**R re-rating under the multi-feature definition**: the VALUE does not change (R stays WORTH IT, N stays WORTH IT, T/B/S/F stay SKIP). The MEANING changes and a complexity split is added: R LOW OPTIONAL, R MEDIUM and HIGH WORTH IT. Reason: the old R reading (VAL:139, "a release assembles and ships work already built") fits this command as a post-tag follow-up, and the new definition (release plan + implementation + push, then a tag) fits it equally; what the new definition adds is that it is the tail of R, not part of the release PR, and only runs when a tag is cut.

| # | Where | Current text | Proposed text |
|---|---|---|---|
| 1 | VAL:186 (row `/sc:post-release`), Notes cell | `Whether this team tags versions is UNVERIFIED (CHANGELOG.md carries "template-version notes")` | `Needs a git tag (runs after it). Verified 2026-10-27: this repo has 2 manual, non-semver tags (aidev02-v1.0, aidev02-v2-m2), one prior run (2026-07-09), none since. R: LOW OPTIONAL, MEDIUM/HIGH WORTH IT; N: WORTH IT (ground-up). Flags: <tag> and --output only; pass --output .dev/releases/current/<short>/post-release/ here` |
| 2 | VAL:186, Purpose cell | `...Runs AFTER the release gate tags a version` | Append: `The "release gate" is a human-cut tag here; no workflow tags` |
| 3 | VAL:256 (Section 4, Release row, WORTH IT additions) | `/sc:post-release after the tag` | `/sc:post-release <tag> after the tag is cut (skip if no tag is cut)` |
| 4 | VAL:261-276 (footprint table) | no row for post-release | Add: `/sc:post-release` : `<output-dir>/audit.log` (RUN and RESULT blocks), `post-release-report.md`, `post-release-manifest.json`; prior run at `.dev/releases/current/v2-m2/post-release/` : SKILL:227-277 |
| 5 | VAL:237 (O11, Document what was built) | Pick `/tech-reference`; `/sc:post-release` not listed | Add `/sc:post-release` to the Overlapping commands cell; keep the pick `/tech-reference`; Why: add `/sc:post-release` is the tag-anchored, whole-surface, install-proven variant for R and N |
| 6 | VAL:298 (U14) | `Whether the team tags versions ... no tag check done` | Resolved: `git tag` shows 2 annotated tags (2026-06-22, 2026-07-09); `.dev/releases/current/v2-m2/post-release/` holds one prior run. Residual question: whether the team will tag again (none for 3.5 months, 763 commits) |
| 7 | VAL:139 (reading of R in 2.4) | `a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R` | Cross-note for the merge step, outside my command: under the new R (release plan + implementation + push) `/sc:implement` and `/task` rated SKIP for R at VAL:143-144 need re-rating by their own agents |
| 8 | Section 4 "Skippable at every size" (VAL:259) | does not mention post-release | Optional: note `/sc:post-release` is skippable at every size except R and N with a fresh tag |

<!-- SECTION 8 -->
## 8. Unverified items

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | Every `(J)` cell and the LOW/MEDIUM/HIGH thresholds in Section 3 | No file gives a threshold for this command; bands are built from the skill's own signals, the single observed run is the only calibration point | Team agreement; a second run to compare |
| U2 | Who or what the "release gate" is | CMD:3,15 assume one; neither file defines it; no workflow here creates tags or Releases; `aidev02-operator.md:639` implies a manual cut. How the two existing tags were actually created was not observed | Ask the operator; read the Phase 8 task referenced as T08.27 |
| U3 | Whether the command's narrower `allowed-tools` (CMD:6) blocks the skill's Bash/Write (SKILL:4) | Not run (read-only rule). The 2026-07-09 artifacts show it worked then | Observe the next real run |
| U4 | Behaviour of `/tech-reference`, `/operational-guide`, `/readme`, `/sc:document`, `bmad-qa-generate-e2e-tests` | Only their descriptions and VAL rows read, not their skill files | Read those skills (other nuance agents may cover them) |
| U5 | Whether a retired `/sc:tasklist` or `/sc:task` could be picked up by the generic hook | SKILL:153 says reuse "the project's" itemized-tasklist tool "only if it's actually loadable" and names none; an engineer's machine where `/sc:tasklist` still loads might be chosen | Run on a machine where the tool is present, or tell the skill which tools to use |
| U6 | Guide and transcript file names in the output dir | The skill fixes only the template names and leaves the transcript path free (SKILL:189-191,295); the prior run's names (`user-e2e-guide.md`, `sysop-e2e-guide.md`, `c-e2e-transcript.txt`) may not repeat | Check the next run; a checker should key on `audit.log` and the manifest, not guide names |
| U7 | Whether non-tag version markers count as releases here: payload `aienv.d/VERSION` (`20261016-1`) and Orca derivative pins seen in `git log` subjects (e.g. `1.4.237-aidev02.*`) | Neither is a git tag; no file says whether they trigger a post-release | Ask the team; recommendation in Section 6 is tags only |
| U8 | GitHub Releases absence | `gh release list --repo IronbellyOrg/Coder` returned no rows with exit 0; token scope not checked | Check the repo Releases page |
| U9 | Run duration by band | One observed run only (1293 s) | More runs |
| U10 | Availability of `/sc:post-release` on other engineers' machines | `sc:*` commands live in `~/.claude`, not the repo (brief, ruling 1); the prior run's paths (`/config/workspace/Coder/...`) show a different workspace than this one | Compare `~/.claude` across engineers |
