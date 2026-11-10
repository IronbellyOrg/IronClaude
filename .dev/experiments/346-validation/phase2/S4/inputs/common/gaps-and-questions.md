# Gaps and Questions Log: BMAD first-use directory creation (BMAD 6.9.0, Coder AIDev02)

**Status:** Complete
**Task:** TASK-RESEARCH-bmad-first-use-20261107-075901 (checklist item 3.14)
**Compiled:** 2026-11-08, from research files 01 to 05, research-notes.md (including every fix-cycle addendum), qa/analyst-completeness-report.md, qa/qa-consolidated-findings-phase3.md, qa/qa-consolidated-findings-phase3-cycle2.md and qa/qa-gate1-decision.md
**Reader:** Phase 4 web research (aimed at rows marked web-01 / web-02) and Phase 5 synthesis (places each gap in report Section 4 or Section 9)

## How this log was built

- Sources read: Gaps and Questions, Stale Documentation Found and Summary sections of research files 01 to 05; all fix-cycle-1 addenda at the end of files 01 to 05 and in research-notes.md (F9); the analyst completeness report; both Phase 3 consolidated findings files; the Gate 1 decision file; the "Open Questions Carried Into The Research Report" section of the task file (task file lines 159 to 165).
- Addendum backstop: Glob for `research/*.addendum.json` found NO addendum file (research folder holds only `01` to `05` and `research-notes.md`), and every addendum heading `## Addendum (fix cycle 1)` is already present inside files 01 to 05 and research-notes.md. Nothing was merged by this log. Cycle-2 corrections sit inside the files' existing text (for example 02 A5, 03 A1/A5, 04 A.3/A.9/A.10, 05 F1.x).
- Gate 1 ended with a user-accepted exception: lines 376 and 408 of research file 05 were corrected by the orchestrator, with no fourth agent review (qa/qa-gate1-decision.md). Row G-30 records that.
- Severity: where the analyst report gave a grade it is used; otherwise the grade is assigned by this log by effect on the plan (Critical = blocks synthesis, Important = changes an option row or a plan step, Minor = lower priority). The analyst found 0 Critical gaps; this log found none either.
- Web topic: `web-01` = Claude Code behaviour (official docs), `web-02` = upstream BMAD user-scope / later releases, per the research files' own pointers ("open until web-01"). Where a research file did not assign a topic, the assignment is marked "(proposed)".
- Not read by this log: `qa/qa-verification-phase3-cycle2-*.md` (their Minor findings are known only through the consolidated and decision files). UNVERIFIED.
- Nothing was run: no `bmad` command, no install, no test.

## 1. Open gaps (deduplicated)

Source IDs are the IDs used inside each research file (U = UNVERIFIED item, C = CODE-CONTRADICTED item, F5-n = file 01 addendum, "03 #n" = row n of file 03's gap table, "03 A5 #n" = row n of file 03's addendum table, "04 add#n" = item n of file 04's addendum gaps, U-F1-n = file 05 addendum). The claim-level inventory is in sections 2 and 3; each claim there points back to a gap number here.

| # | Gap | Source research file | Severity | Status | Web topic |
|---|---|---|---|---|---|
| G-01 | Does Claude Code load a project skill directory (`.claude/skills/bmad-*`) that is created AFTER the session started, without a restart? Decides whether first use in an already-open session works (options B, D; the already-running case of C). | 03 (gap 9, A5 #22, A4); research-notes F9-5 #4 | Important | to be answered by web research | web-01 |
| G-02 | Does Claude Code load user-level `~/.claude/skills` skills in every project, and how does it rank one against a project skill of the same name? Also the blast radius of a user-level skill or hook (applies to every project). | 01 (U7); 03 (A5 #21, A4); 02 (U13) | Important | to be answered by web research | web-01 |
| G-03 | Does a `/etc/claude-code/managed-settings.d/*.json` drop-in accept `hooks`, and do its hooks merge with or replace user-level hooks? Decides option D2. | 02 (U9); 03 (gap 5); 04 (add#8); 05 (U-F1-4, first half) | Important | to be answered by web research | web-01 (proposed) |
| G-04 | Claude Code hook and permission runtime semantics: does a running session reload a changed `hooks` block without restart; do hooks run without the Bash permission prompt; what a SessionStart hook's stdout shows the user; hook timeout semantics for a long install; what a non-allow-listed Bash command does and what `skipDangerousModePermissionPrompt: true` does; whether the Orca `PermissionRequest` hook ever decides a permission. | 03 (gaps 7; A5 #18, #19, #20) | Important | to be answered by web research | web-01 (proposed) |
| G-05 | Upstream BMAD after 6.9.0: did a later release (the update banner reports 6.12.4) add a consumer of `global_target_dir` or a user-scope install flag, and does 6.12.4 exist at all (seen only in the CLI banner)? 6.9.0 itself has no consumer (CODE-VERIFIED, see G-25). | 01 (U9, section 5 Option F conclusion); 02 (U2, section 6.5 F); research-notes F9-4 limit (a), F9-5 #4 | Important | to be answered by web research | web-02 |
| G-06 | Model and environment behaviour for the 41 `python3 ` steps in 31 SKILL.md files: whether Claude emits the bare `python3` form, whether it treats a hook block as "the script fails" so the written fallback applies (25 of 31 files have one), whether the 6 other files have any other fallback (`bmad-advanced-elicitation`, `bmad-customize`, `bmad-validate-prd`, `bmad-create-architecture`, `bmad-edit-prd`; `bmad-retrospective` line 94 grep-read only), and whether a fresh Default-profile workspace has the same `block-bare-python.sh` registration as this long-lived one. | 03 (addendum gaps 13, 14, 15; A5); 01 (section 7.5) | Important | open | none |
| G-07 | Behaviour of the skills when `_bmad/` or some config keys are missing: output of `resolve_customization.py` with no `_bmad/` (derived from code, not executed); the interpreter's error text and the model's behaviour in a session that has `.claude/skills/bmad-*` but no `_bmad/`; behaviour when `project_name`, `communication_language`, `document_output_language` are absent (the `install.sh:42` flag set leaves them out); which file(s) `--set core.project_name=<value>` patches. | 01 (U5, U6, U13; section 3.2a) | Important | open | none |
| G-08 | Model compliance with a stub's first-use predicate (option B); hook timeout versus install time and the working directory a hook evaluates (option D); a stub that offers "reinstall" or "update" re-opens the quick-update path. | 01 (F5-9, F5-F) | Important | open | none |
| G-09 | Real duration of a first install inside a Coder workspace (home volume, cold node cache, real seed-repo size) and with live network; why CI `cold bmad` (374 to 392 ms, baked CLI, no network) is about ten times below the memlog "about 4s" (npx fetch, scratch HOME). The two figures must not be blended. | 01 (U1, F5-3, F5-4, F5-E); 03 (A5 #23) | Important | open (for the implementation phase to observe in CI) | none |
| G-10 | Exact files a first install writes (per-file list, the `{output_folder}` substitution that yields `_bmad-output/planning-artifacts`), and the first run in a directory with NO `.git` (including whether `bmad install` works there). All 6.9.0 rows are read from code, not observed. | 01 (U11, F5-5); 02 (U6); 03 (A5 #17) | Important | open (for the implementation phase to observe in CI) | none |
| G-11 | Exact skill set, count and names written to `.claude/skills/`: 46 `SKILL.md` by Glob and "46 skills, 2.4M" in a prior review, versus 47 `bmad-*` directories in the tracked 6.10.0 tree; `ManifestGenerator.collectSkills` (`manifest-generator.js:78`) not enumerated; names of the 46 not recorded; CI discards installer output. | 01 (U12, F5-6); 03 (A5 #23) | Minor | open (for the implementation phase to observe in CI) | none |
| G-12 | Default module list of a bare `--yes` with no `--modules` (does the bundled `bmad-modules.yaml` mark any external module `default_selected`, which would clone over the network). The safe form `--modules bmm` avoids the question; closable by reading the registry file. | 01 (U4) | Minor | open | none |
| G-13 | Partial `_bmad/` after a failed first run: `InstallPaths.create` makes `_bmad/core/` first, so a later `bmad install --yes` takes quick-update, and what quick-update does to a half-written tree was not read or run (`installer.js:1254-` not read). Related design questions in section 8 (atomicity, guard on `_bmad/config.toml`). | 05 (U7); 01 (F5-8, F5-D, open questions 1 and 2) | Important | open (for the implementation phase to observe in CI) | none |
| G-14 | The `{output_folder}/` literal-directory and prior-probe facts: outcome of `--user-name` without `--output-folder` (mechanism CODE-VERIFIED at `official-modules.js:1409`, outcome not run); the flags the prior 04 probe passed; whether `--offline` in `04-bmad.md:35` is an npx or a bmad flag; the "6 files rewritten" and "41 files downgraded" counts (prior-review observation, not re-run). The plan keeps `--output-folder _bmad-output` in every command. | 01 (F5-1, F5-2, F5-7); 05 (U6, U10) | Minor | open | none |
| G-15 | HOME writes and network side effects of the installer: whether any run writes under `~/.bmad/cache` (code shows it only for external or custom modules, not on the bmm-only path), `~/.npm` (origin: `npx`, `npm view`, or both), what `npm view` and `uv --version` leave behind, and whether the "Update Available 6.12.4" banner under `NPM_CONFIG_OFFLINE=true` comes from npm's local cache or the network. | 01 (U2, U3, F5-11); 02 (U3); 05 (U11) | Minor | open (for the implementation phase to observe in CI) | none |
| G-16 | Option E and the manual command: what `bmad install --directory ~` actually writes (01 section 6 derives `~/_bmad`, `~/_bmad-output`, `~/docs`, `~/.claude/skills/bmad-*` from code; 02, 04, 05 call it UNVERIFIED; whether it edits `~/.claude/CLAUDE.md`); and whether the manual command in `catalogue/bmad/manifest.yaml:13-14` completes end to end. | 02 (U5); 04 (gap 1); 05 (U-F1-1, U3, U8) | Important | open (for the implementation phase to observe in CI) | none |
| G-17 | Meaning of the `semver` hits in `ui.js`, `manifest.js`, `legacy-warnings.js`, `channel-resolver.js` beyond their match lines. The claim relied on is only that `core/installer.js` has no `semver` token (no installed-versus-installer version gate). Closable by reading those files. | 01 (F5-12) | Minor | open | none |
| G-18 | The built image really contains `bmad-method@6.9.0` and the `/usr/local/bin/bmad` wrapper: only `Dockerfile.coder:139` text and the CI PASS of test-57 are evidence; the image was not inspected. | 01 (U10 residual, F5-10) | Minor | open | none |
| G-19 | Sysbox layer-budget residuals (CI gate fails above 70 layers; measured 68, two free): the Sysbox-runtime job's count (only dind-sidecar was read); that the base image contributes 8 layers (inference); that each RUN adds exactly one layer; that option B2 can fold into the `/usr/local/lib/aidev/` COPY and the C helper into the `bin/` COPY at 0 layers; that no other test pins the COPY lines at `Dockerfile.coder:492`, `:469`, `:547`; that a plain nested COPY under `/etc/skel/.claude/skills/<name>/` creates intermediate directories at 0755 under the provider's legacy builder; Docker layer-cache behaviour when only the last COPY changes. Another PR can consume the two spare layers first. | 02 (U8, U15 to U20, A5 to A7); 04 (add#1) | Important | open | none |
| G-20 | Test-suite residuals: tests not run (pass state today unknown); test-73 not checked with a second drop-in file; value of `IDE_CONVERGENCE_TIMEOUT_S`; required-field list of `catalogue/manifest.schema.json` (test-2); `orca-build/repin.sh --verify` internals (test-68); the two failure strings of test-b1-affordance-matrix; the full skel copy at `test-4-pane-title.sh:89` and the body of test-72; `ALLOWED_SET` of test-5-coder-app-allowlist; test-1-tool-floor F08 fixtures after line 260; which no-argument path of test-52 reaches the `ORCA_FIXTURES` block; exact file count of `.github/contract-tests/`; contents of `slug-configuration.md` as read by file 04; whether any of the 48 `bmad`/`install.sh`/`catalogue` hits in `test-startup-boot.sh` runs a bmad subcommand; whether an unquoted heredoc in `install.sh` survives the `test-19:205` quote strip; test-46 and test-52 rows in file 05 taken from file 04, not re-read. | 04 (gaps 4 to 7; add#2 to #7; add (a), (c)); 03 (gap 6); 05 (U-F1-3 to U-F1-6) | Minor | open | none |
| G-21 | Environment residuals in file 03: home volume destroyed on workspace deletion; the `/opt/uv/.../_src/superclaude/cli/` copies identical to the read copies; Claude Code itself writes `~/.claude/settings.json`; Orca writes it concurrently (only a comment, `ironclaude/install.sh:139`); each `~/.claude/skills` entry is a real directory; Docker seeds a new named volume from the image's `/home/coder`; a fresh workspace may show different `~/.claude/` content; git anchors root-anchored `info/exclude` patterns at the work-tree top (a subfolder install would fail in `install.sh`); the "untracked skills but `_bmad/` deleted" case reads as never-had-BMAD at `install.sh:24`. | 03 (gaps 1 to 4, 8, 12; A5 #16, #24; Other open questions) | Minor | open | none |
| G-22 | Startup `§10`/`§12` never write `~/.claude/settings.json` or `~/.claude/skills/` (03 gap 10) and `wire_ccsession()` leaves unrelated skills and settings alone (03 gap 11). | 03 (gaps 10, 11) | Minor | resolved by fix (analyst Grep: only `startup.sh` lines 275, 979, 1282, 1285; analyst read `install_ccsession.py:1-100`, qa/analyst-completeness-report.md G-M6) | none |
| G-23 | Small image and catalogue unknowns: the claim that NVM node is not on the default PATH (`Dockerfile.coder:134-135`); the exact Coder flow from template push to a running workspace; whether the task's "OD-1" label is the one used in this repo (other uses at `test-57:10, 992, 1034`, `startup.sh:1114`); the inference that a `bmad` wrapper cannot run when a BMAD skill is invoked inside Claude Code. | 02 (U1, U10, U12, U14) | Minor | open | none |
| G-24 | Test-inventory gaps that the finding-2 addendum closed: 02 U7 (test-1 three-file rule, closed at `test-1-catalogue-shape.sh:25, 43-67`), 02 U11 (test-60, test-67, closed in 04 A.2/A.3), 04 gap 2 (test-startup-boot, covered in A.4), 04 gap 3 (other tests that may pin the slug; 30 files classified, 15 relevant), 05 U-F1-2 (matrix rows compared with the finished 04 addendum). | 02 (U7, U11); 04 (gaps 2, 3); 05 (U-F1-2) | Important | resolved by fix (04 addendum A.1 to A.8; Gate 1 verified) | none |
| G-25 | Tag disagreement for options E and F: 02 (U4, U6), 04 (section 7 F column and gap 1) and 05 (U1 to U3) still say UNVERIFIED while 01 sections 2 and 5 give CODE-VERIFIED "zero consumers of `global_target_dir` in 6.9.0; option F has no code path" (43 hits, one file, reproduced by the analyst). Synthesis must use 01's tags and drop the F `X` cells. The E write set stays open (G-16). | 01 (section 2, section 5); 02 (U4, U6); 04 (gap 1); 05 (U1, U2, U3) | Minor | resolved by fix (cross-reference; analyst X3 and QA finding 10 require synthesis to carry 01's tag) | none |
| G-26 | Owner and decision wording not available to the researchers: the exact 2026-11-07 answer exists only at `BUILD-REQUEST.md:14`; whether the first-use files must be hidden from git with `info/exclude` (as the seed install does, `install.sh:32-34`) or left visible; whether the decision covers Orca-created worktrees (`catalogue-bundle SPEC.md:174` says "project"). | 05 (U17, open question 2); research-notes F9-5 #1, #2 | Important | open (owner question; goes to report Section 9) | none |
| G-27 | Minor unknowns in the document trail: "worktrees carry only tracked files" (`SPEC.md:141`); the "73 skill files" claim (`slug-configuration.md:54`) against 75 files in package `src/` (40 `SKILL.md`) and 46 `SKILL.md` counted in 01; seed-repo runtime result of the boot install (this workspace has no `seed-repo-path`); hashes in `.dev/reviews/local-snapshots-20261019/README.md` against live specs; whether 478 is the number to cite in a CHANGELOG entry and whether issue #478 is still OPEN; markdownlint version (rules MD055, MD056, MD058); whether `image/` files that `Dockerfile.coder` does not copy are invisible in a workspace; whether a root-level `_bmad/` exists as `docs/source-tree-analysis.md:37` says; whether the boot log in `/tmp` is truncated each boot (`startup.sh:1184` prints "installed."). | 05 (U4, U5, U9, U12 to U16); research-notes F9-5 #3, #6 | Minor | open | none |
| G-28 | Documentation hygiene found by QA, not acted on: 01 line 18 ("path-derived; `node --version` not run") against 01 section 3.3 ("OBSERVED via `node --version`"); 03 section 6 M4 managed-settings precedence sentence is doc-sourced with no verification tag; wrong sizes and moved lines on true claims (install.sh 61 not 62 lines, manifest.yaml 29 not 30, Dockerfile.coder 594, catalogue README 604, spec2-health.sh 636, ironclaude/install.sh 157, `welcome/bmad.txt` 12 lines, `startup.sh:1175` not :1174, README line refs 33/182/238); 03 section 2 Key Takeaways lists `startup.sh:1172` which is only a comment; 05 Summary still counts 17 UNVERIFIED and 6 CODE-CONTRADICTED while its merged tables add U-F1-1..6 and C-F1-1..3; 04 line 238 says addendum sections A.1 to A.8, the addendum runs A.1 to A.11; 01 line 491 says the 03 addendum was In Progress, it is Complete. | qa/analyst-completeness-report.md (G-M2, G-M3, X2, X6); qa/qa-consolidated-findings-phase3.md (findings 11, 12, 16, 18); qa/qa-consolidated-findings-phase3-cycle2.md (Notes) | Minor | open | none |
| G-29 | Evidence for the Ponytail half of the prior diagnosis (`REPORT.md` evidence 10 to 13, 16, 17) was not re-read: out of scope by the 2026-11-07 user confirmation (research-notes TEMPLATE_NOTES). No action. | research-notes F9-5 #5 | Minor | open (out of scope, no action) | none |
| G-30 | Gate 1 closed with a user-accepted exception: lines 376 and 408 of research file 05 were corrected by the orchestrator and re-read by the executor only; no fourth agent review checked the corrected text. | qa/qa-gate1-decision.md ("User exception applied") | Minor | open (accepted exception) | none |

Totals for section 1: 30 rows; 27 open or to be answered (G-01 to G-21, G-23, G-26 to G-30); 3 resolved by fix (G-22, G-24, G-25). Of the 27, 5 are assigned to web research (G-01 to G-05: four to web-01, one to web-02).

## 2. Every [UNVERIFIED] and [CODE-CONTRADICTED] claim, with source file

Duplicates across files are merged into one row that names every source. "Gap" points to section 1. Rows marked (closed) or (superseded) are kept so that nothing from a research file is dropped.

### 2.1 [UNVERIFIED] claims (89 rows)

| ID | Claim | Source research file and item | Gap |
|---|---|---|---|
| UV-01 | Real duration of a fresh `bmad install --yes --modules bmm --tools claude-code` (workspace, large repo, live network); cause of the CI-versus-memlog difference | 01: U1, F5-3, F5-4 | G-09 |
| UV-02 | Whether the update banner under `NPM_CONFIG_OFFLINE=true` came from npm's cache or the network | 01: U2; 02: U3; 05: U11 | G-15 |
| UV-03 | Side effects of `npm view` and `uv --version`; origin of `.npm` in the prior scratch HOME | 01: U3, F5-11 | G-15 |
| UV-04 | Default module list of a bare `--yes` | 01: U4 | G-12 |
| UV-05 | Output of `resolve_customization.py` with no `_bmad/` (derived, not executed) | 01: U5 | G-07 |
| UV-06 | Interpreter error text and model behaviour in a skill session with skills but no `_bmad/` | 01: U6 | G-07 |
| UV-07 | Claude Code loads user-level `~/.claude/skills` in every project; ranking against a project skill | 01: U7; 02: U13; 03: A5 #21 | G-02 |
| UV-08 | Whether a later upstream release added a `global_target_dir` consumer or user-scope flag | 01: U9; research-notes F9-5 #4 | G-05 |
| UV-09 | The built image contains `bmad-method@6.9.0` and the wrapper (Dockerfile text and CI PASS only) | 01: U10 residual, F5-10 | G-18 |
| UV-10 | Exact files a first install writes; `{output_folder}` substitution; first run with no `.git` | 01: U11, F5-5; 02: U6; 03: A5 #17 | G-10 |
| UV-11 | Exact skill set, count and names (46 versus 47) | 01: U12, F5-6; 03: A5 #23 | G-11 |
| UV-12 | Skill behaviour with `project_name` and language keys absent; which file(s) `--set` patches | 01: U13, section 3.2a | G-07 |
| UV-13 | Flags the prior 04 probe passed when it saw the literal `{output_folder}/` directory | 01: F5-1 | G-14 |
| UV-14 | Whether `--offline` in `04-bmad.md:35` is an npx or a bmad flag | 01: F5-2 | G-14 |
| UV-15 | "6 files rewritten by quick-update" and "41 files downgraded" counts | 01: F5-7; 05: U10 | G-14 |
| UV-16 | What quick-update does to a half-written `_bmad/`; a failed `bmad install` leaves a partial `_bmad/` | 01: F5-8; 05: U7 | G-13 |
| UV-17 | Model compliance with a stub predicate; hook timeout versus install time; hook cwd | 01: F5-9, F5-F | G-08 |
| UV-18 | Meaning of the `semver` hits beyond their match lines | 01: F5-12 | G-17 |
| UV-19 | NVM node is not on the default PATH (`Dockerfile.coder:134-135`) | 02: U1 | G-23 |
| UV-20 | A newer upstream `bmad-method` 6.12.4 exists (seen only in the banner) | 02: U2 | G-05 |
| UV-21 | `global_target_dir` works as a user-scope install in 6.9.0 (option F) (superseded: 01 section 2 CODE-VERIFIED no consumer) | 02: U4; 04: gap 1; 05: U1, U2 (UV-70, UV-71) | G-25 |
| UV-22 | What `bmad install --directory ~` writes (E), including whether it edits `~/.claude/CLAUDE.md` | 02: U5; 04: gap 1; 05: U-F1-1, U3 | G-16 |
| UV-23 | test-1 enforces the exactly-three-files rule (closed by 04 A.7) | 02: U7 | G-24 |
| UV-24 | Docker layer-cache behaviour when only the last COPY changes | 02: U8 | G-19 |
| UV-25 | `managed-settings.d` accepts hooks; merge versus replace with user-level hooks | 02: U9; 03: gap 5; 04: add#8; 05: U-F1-4 | G-03 |
| UV-26 | Exact Coder flow from template push to a running workspace | 02: U10 | G-23 |
| UV-27 | What test-60 and test-67 assert (closed by 04 A.2, A.3) | 02: U11 | G-24 |
| UV-28 | A `bmad` wrapper cannot run when a BMAD skill is invoked in Claude Code (inference) | 02: U12 | G-23 |
| UV-29 | The task's "OD-1" is the label used in this repo | 02: U14 | G-23 |
| UV-30 | Sysbox-runtime job layer count equals the dind-sidecar count | 02: U15 | G-19 |
| UV-31 | Base image contributes 8 layers | 02: U16 | G-19 |
| UV-32 | Every RUN adds exactly one layer under the provider's builder | 02: U17 | G-19 |
| UV-33 | B2 can ride the `/usr/local/lib/aidev/` COPY at 68 layers | 02: U18 | G-19 |
| UV-34 | A new `bin/` helper in the existing COPY keeps the layer count (C late-COPY) | 02: U19 | G-19 |
| UV-35 | No other test pins the COPYs at `Dockerfile.coder:492`, `:469`, `:547` | 02: U20 | G-19 |
| UV-36 | Nested COPY under `/etc/skel/.claude/skills/<name>/` creates directories at 0755 | 04: add#1 | G-19 |
| UV-37 | Home volume is destroyed on workspace deletion | 03: gap 1 | G-21 |
| UV-38 | The `_src/superclaude/cli/` copies equal the copies read | 03: gap 2 | G-21 |
| UV-39 | Claude Code itself writes `~/.claude/settings.json` | 03: gap 3 | G-21 |
| UV-40 | Orca writes `~/.claude/settings.json` concurrently | 03: gap 4 | G-21 |
| UV-41 | A second drop-in file passes test-73 | 03: gap 6 | G-20 |
| UV-42 | A running session picks up a changed `hooks` block without restart | 03: gap 7 | G-04 |
| UV-43 | Each `~/.claude/skills` entry is a real directory | 03: gap 8 | G-21 |
| UV-44 | Claude Code discovers a skill directory created mid-session | 03: gap 9, A5 #22 | G-01 |
| UV-45 | Startup `§10`/`§12` never write settings or skills (closed by analyst Grep) | 03: gap 10 | G-22 |
| UV-46 | `wire_ccsession()` leaves unrelated skills and settings alone (closed by analyst read) | 03: gap 11 | G-22 |
| UV-47 | Docker seeds a new named volume from the image's `/home/coder` | 03: gap 12 | G-21 |
| UV-48 | A fresh Default-profile workspace has the same `block-bare-python.sh` registration | 03: A5 #13 | G-06 |
| UV-49 | Claude emits bare `python3` and treats a hook block as "the script fails" | 03: A5 #14 | G-06 |
| UV-50 | The other no-fallback skill files have no other written fallback; `bmad-retrospective` line 94 | 03: A5 #15, A5 text | G-06 |
| UV-51 | git anchors root-anchored `info/exclude` patterns at the work-tree top | 03: A5 #16 | G-21 |
| UV-52 | A non-allow-listed Bash command prompts; effect of `skipDangerousModePermissionPrompt` | 03: A5 #18 | G-04 |
| UV-53 | The Orca `PermissionRequest` hook never decides a permission | 03: A5 #19 | G-04 |
| UV-54 | Hooks run without the Bash prompt; SessionStart stdout display; hook timeout semantics | 03: A5 #20 | G-04 |
| UV-55 | Untracked skills with `_bmad/` deleted read as never-had-BMAD at `install.sh:24` | 03: A5 #24 | G-21 |
| UV-56 | A fresh workspace shows different `~/.claude/` content | 03: Other open questions | G-21 |
| UV-57 | test-startup-boot would break under any option (closed by 04 A.4) | 04: gap 2 | G-24 |
| UV-58 | Other contract tests pin the bmad slug (closed: 30 files classified) | 04: gap 3 | G-24 |
| UV-59 | Contents of `slug-configuration.md` (not read by file 04) | 04: gap 4 | G-20 |
| UV-60 | Whether the tests pass today (no test run) | 04: gap 5; 05: U-F1-5 | G-20 |
| UV-61 | Which test-52 invocation modes reach the `ORCA_FIXTURES` block | 04: gap 6 | G-20 |
| UV-62 | Exact number of files in `.github/contract-tests/` | 04: gap 7 | G-20 |
| UV-63 | Value of `IDE_CONVERGENCE_TIMEOUT_S` | 04: add#2 | G-20 |
| UV-64 | Required-field list of `manifest.schema.json` (test-2) | 04: add#3 | G-20 |
| UV-65 | `orca-build/repin.sh --verify` internals (test-68) | 04: add#4 | G-20 |
| UV-66 | The two failure strings of test-b1-affordance-matrix | 04: add#5 | G-20 |
| UV-67 | Full skel copy at `test-4-pane-title.sh:89`; remaining body of test-72 | 04: add#6 | G-20 |
| UV-68 | `ALLOWED_SET` of test-5-coder-app-allowlist (not needed for any variant) | 04: add#7 | G-20 |
| UV-69 | Unread blocks of `test-startup-boot.sh` and test-1-tool-floor F08 fixtures after line 260 | 04: add (a), (c) | G-20 |
| UV-70 | Option F effect on readiness wording asserted by `orca_status_assert` (superseded by 01) | 05: U1 | G-25 |
| UV-71 | Option F effect on the 75 s configure budget (superseded by 01) | 05: U2 | G-25 |
| UV-72 | "Worktrees carry only tracked files" (`SPEC.md:141`) | 05: U4 | G-27 |
| UV-73 | "73 skill files" and "user-level install is broken" in practice (`slug-configuration.md:54`) | 05: U5 | G-27 |
| UV-74 | Literal `{output_folder}/` directory outcome with `--user-name` and no `--output-folder` | 05: U6 | G-14 |
| UV-75 | The manual command at `manifest.yaml:13-14` completes end to end | 05: U8 | G-16 |
| UV-76 | Seed-repo runtime result of the boot install | 05: U9 | G-27 |
| UV-77 | Whether any check compares the hashes in `local-snapshots-20261019/README.md` with live specs | 05: U12 | G-27 |
| UV-78 | Issue 478 is the number to cite in a CHANGELOG entry; issue still OPEN | 05: U13; research-notes F9-5 #3 | G-27 |
| UV-79 | markdownlint version and whether table rules MD055, MD056, MD058 are active | 05: U14 | G-27 |
| UV-80 | `image/` files not copied by `Dockerfile.coder` are invisible in a workspace | 05: U15 | G-27 |
| UV-81 | A root-level `_bmad/` exists as `docs/source-tree-analysis.md:37` says | 05: U16 | G-27 |
| UV-82 | What the owner decided about git cleanliness of first-use files; exact wording of the 2026-11-07 answer | 05: U17; research-notes F9-5 #1 | G-26 |
| UV-83 | Whether any of the 48 `bmad`/`install.sh`/`catalogue` hits in test-startup-boot runs a bmad subcommand | 05: U-F1-3 | G-20 |
| UV-84 | An unquoted heredoc in `install.sh` survives the `test-19:205` quote strip | 05: U-F1-4 | G-20 |
| UV-85 | test-46 and test-52 rows "not re-derived" in file 05 | 05: U-F1-6 | G-20 |
| UV-86 | Matrix rows S6, S13 to S16c take verdicts from the 04 addendum (RESOLVED in fix cycle 2) | 05: U-F1-2 | G-24 |
| UV-87 | The decision covers Orca-created worktrees | research-notes: F9-5 #2 | G-26 |
| UV-88 | Ponytail evidence in the prior `REPORT.md` (out of scope) | research-notes: F9-5 #5 | G-29 |
| UV-89 | The boot log in `/tmp` is truncated each boot (`REPORT.md:113`) | research-notes: F9-5 #6 | G-27 |

### 2.2 [CODE-CONTRADICTED] claims (30 rows; 05 C5 was withdrawn and is not counted)

| ID | Claim and what the code shows | Source research file and item |
|---|---|---|
| CC-01 | `platform-codes.yaml:9` calls `global_target_dir` "User-home directory for global install"; no reader exists in 6.9.0 | 01: C1 |
| CC-02 | Worktree `_bmad/_config/agent-manifest.csv` looks like 6.9.0 installer output; the string is absent from the 6.9.0 package | 01: C2 |
| CC-03 | Worktree `.claude/skills/bmad-help/SKILL.md` (6.10.0) taken as a 6.9.0 description | 01: C3 |
| CC-04 | Memlog `:21` "`--yes` without `--output-folder` creates literal `{output_folder}/`" read as a bare-`--yes` defect; bare `--yes` seeds `_bmad-output` (`ui.js:838-861`); quote it, do not describe it | 01: F5-C1 |
| CC-05 | `04-bmad.md:15, 78` Dockerfile line numbers (pin at `:360`); the pin is at `Dockerfile.coder:139` | 01: F5-C2 |
| CC-06 | `install.sh:18` says "`/usr/local/bin/bmad` symlink"; it is a 2-line wrapper script | 02: C1; 01: F5-C3 |
| CC-07 | Catalogue README walkthrough paths `/config/workspace/Coder/catalogue/...` | 02: C2 |
| CC-08 | Catalogue README relative links at 32, 64, 594-596 resolve to nothing | 02: C3 |
| CC-09 | Catalogue README:180-183 "( source ~/.aienv && bash install.sh )" true only for bmad | 02: C4 |
| CC-10 | `startup.tf:30` "ONLY runtime coder_script in the template" | 02: C5 |
| CC-11 | `profiles.yaml:1` path comment omits `image/` | 02: C6 |
| CC-12 | `manifest.yaml:12` "BMad is already set up there" read unconditionally | 02: C7 |
| CC-13 | `Dockerfile.coder:468` "budget (70) has no headroom"; measured 68 of 70, two free (holds only as policy) | 02: C8 (addendum A4, A7) |
| CC-14 | File 01 section 7.5 wording on the `python3 {project-root}/...` skill steps and the fallback (41 lines in 31 files; 25 have a fallback; fallback reads three TOML files). 03 A5 says "both" corrections but spells out one; the second is not named in the text: UNVERIFIED which | 03: A5 |
| CC-15 | `PROJECT_INDEX.md:13, 36, 65` "T1-T55"; tests run to test-79 | 04: section 9 |
| CC-16 | The finding's nine named tests (test-7-tmux-fallback, test-73-codegraph-sweep, and others) are among the 30 files hit by the `startup.sh` search; none is | 04: addendum Gaps (CODE-CONTRADICTED 1) |
| CC-17 | "BMad is installed per project only, never globally" (`owner-decisions.md:5`, memlog `:32`) taken literally; the CLI is global (`Dockerfile.coder:139-143`) | 05: C1 |
| CC-18 | `.memlog.md:27` "the seed repo gets no `_bmad/`" | 05: C2 |
| CC-19 | `fr-audit.md:12` cites `install.sh:38-66`; file has 61 lines | 05: C3 |
| CC-20 | Profile `agile-full` (`SPEC.md:34, 166`); `profiles.yaml` has only `orca` and `minimal` | 05: C4 |
| CC-21 | PRD addendum Option A "user-level availability" as lead (`addendum.md:75`, PRD memlog `:13`) | 05: C6 |
| CC-22 | "The offline setting stops the help path from running `npm view`"; an Update box appeared under `NPM_CONFIG_OFFLINE=true` | 05: C7 |
| CC-23 | 04 section 7 test-49 row "c (manifest edit)" for B and "c (...)" for D; test-49 fails only on a non-comment `LIFECYCLE_RE` match | 05: C-F1-1 |
| CC-24 | 05 Summary wording naming "C" among variants needing a boot-time replacement assertion (corrected) | 05: C-F1-2 |
| CC-25 | `test-57:386` "the only installer that edits settings.json" becomes stale under D1 (coverage gap) | 05: C-F1-3 |
| CC-26 | `REPORT.md:91` says test-startup-boot pins "no seed: bmad writes nothing"; only `test-57:446-452` does | research-notes: F9-5 #7 |
| CC-27 | `REPORT.md:26` "Restrictions overridden: None" no longer holds after `BUILD-REQUEST.md:14` | research-notes: F9-5 #8 |
| CC-28 | `claim-comment.md:19` links `.dev/issues/478/analysis/`; the directory does not exist | research-notes: F9-5 #9 |
| CC-29 | EXISTING_FILES row says `install.sh` is 62 lines; it is 61 (trivial) | research-notes: F9-5 #10 |
| CC-30 | `REPORT.md:89-90` "MUST NOT change" rationale ("any-repo setup reverses OD-1") overtaken for first-use creation | research-notes: F9-5 #11 |

Totals for section 2: 89 UNVERIFIED rows and 30 CODE-CONTRADICTED rows, 119 listed. Of the 89 UNVERIFIED rows, 10 are closed or superseded in the research files or by QA (UV-21, UV-23, UV-27, UV-45, UV-46, UV-57, UV-58, UV-70, UV-71, UV-86); 79 remain open.

## 3. Every [STALE DOC] item (13 tagged rows)

| ID | Stale item | Source research file | Related claim |
|---|---|---|---|
| SD-01 | `tools/installer/ide/platform-codes.yaml:9` advertises `global_target_dir` for "global install"; zero consumers in 6.9.0, the 41 values are inert data | 01 | CC-01 |
| SD-02 | `platform-codes.yaml:10` advertises `ancestor_conflict_check`; the reader exists (`_config-driven.js:191`) but no platform sets the key, so it never fires | 01 | none |
| SD-03 | Worktree `_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*` read as "the installed BMAD" are a 6.10.0 tree, not 6.9.0 output | 01 | CC-02, CC-03 |
| SD-04 | `catalogue/bmad/install.sh:18` error text says "symlink"; the CLI is a wrapper script (low impact) | 01 (F5-C3); 02 | CC-06 |
| SD-05 | `profiles.yaml:1` path comment omits `image/` | 02 | CC-11 |
| SD-06 | Catalogue README paths and links (lines 32, 64, 348, 408-409, 594-596) and the `( source ~/.aienv && bash install.sh )` statement (180-183) | 02 | CC-07, CC-08, CC-09 |
| SD-07 | `startup.tf:30` "ONLY runtime coder_script" | 02 | CC-10 |
| SD-08 | `docs/generated/PROJECT_INDEX.md:13, 36, 65` "T1-T55" (also tagged CODE-CONTRADICTED) | 04 | CC-15 |
| SD-09 | `spec-orca-bundle-gap-closure/.memlog.md:27` (OD-1=A, user-level), voided by line 32, kept as history | 05 | CC-18 |
| SD-10 | `fr-audit.md:12` cites `install.sh:38-66` (file is 61 lines; block is 21-55) | 05 | CC-19 |
| SD-11 | `catalogue-bundle SPEC.md:34, 166`: profile `agile-full` does not exist | 05 | CC-20 |
| SD-12 | PRD `addendum.md:75` and its `.memlog.md:13`: user-level Option A, replaced by the shipped seed install and the 2026-09-25 cancellation | 05 | CC-21 |
| SD-13 | `slug-configuration.md:54` the "73" skill-file count (not reproduced; the `{output_folder}/` wording at `:53` is NOT stale, withdrawn in fix cycle 1) | 05 | UV-73 |

Items that are stale or misleading but carry no `[STALE DOC]` tag in the research files: file 03 found none ("None contradicted by code"); catalogue `manifest.yaml:12-18` welcome text reads unconditionally (02 C7 / 01); the wording hazard "never globally" (`owner-decisions.md:5`, memlog `:32`, 05 C1); `Dockerfile.coder:468` as a measurement (02 C8). Also not read in full by file 01: `tools/installer/README.md` (searched by Grep only).

## 4. Questions assigned to web research

| # | Question | Status | Assigned to | Why it is open |
|---|---|---|---|---|
| Q-1 | Does Claude Code load project skills (`.claude/skills/bmad-*`) that are created after the session started? | open | web-01 | 03 (gap 9, A4): "The settings page does not say; skills docs not fetched." No file in the repo or in the installed packages decides it. Decides option B steps 4 to 5, option D step 3, and the already-running case of option C. Also research-notes F9-5 #4 |
| Q-2 | Does Claude Code load user-level `~/.claude/skills` in every project, and how does it rank one against a project skill of the same name? | open | web-01 | 01 U7, 03 A4: "open until web-01"; matters for options B and E |
| Q-3 | Does a later upstream BMAD release (the CLI banner reports 6.12.4) add a consumer of `global_target_dir` or a user-scope install flag? | open | web-02 | 01 U9 and line 219: only 6.9.0 was read; no network research was in scope. Not a gap for the 6.9.0 pin; it matters only if the pin is changed (02 section 6.5 F) |

Additional web-01 candidates (proposed, the research files do not name a topic): managed-settings drop-in hooks (G-03) and hook runtime semantics (G-04).

## 5. Owner questions (copied unanswered; they go to report Section 9)

Copied from the "## Open Questions Carried Into The Research Report" section of the task file (lines 163 and 164). Nobody may guess an answer. Each is to appear unanswered in Section 9 with the mechanism its readings imply (synthesis item `synth-04`).

1. **Is a user-level bootstrap artifact allowed?** The 2026-09-25 owner text (`.memlog.md`) says BMad is never installed "globally or at user level"; the 2026-11-07 decision says global installation of BMAD itself is not requested. Whether a tiny stub skill or command under `~/.claude/` that contains no BMAD content and only starts the per-project install counts as "user level" is an owner reading, not a code fact. (Owner question; implied mechanisms: options B and D put a stub or hook in user scope; option C does not.)
2. **What counts as "first use"?** Running a `bmad` CLI command, invoking a BMAD slash skill, or opening a session in a project. Each reading implies a different mechanism (options C, B, D respectively). (Owner question.)

Related owner or decision input found in the research files, listed as G-26 and not an answer: how the 2026-11-07 decision is worded (only at `BUILD-REQUEST.md:14`), whether first-use files stay hidden from git or visible, and whether Orca-created worktrees are covered.

The third item of the task file section (what a first install would create that this worktree cannot show) is an evidence limit, not an owner question; it is handled in section 7 of this log.

## 6. Feasibility: without a global BMAD install and without a change in IronClaude or IronOrca

**Statement.** The evidence so far shows the ask is feasible without a global BMAD install and without a change in IronClaude or IronOrca: first-use creation of `_bmad/` and the skills can be done per project by running the image-baked `bmad install --directory <project>` from a mechanism that lives in this repo (options B, C or D). Which mechanism fires at the right moment is NOT yet determinable, because it depends on Claude Code behaviour (G-01, G-02, web-01) and on the owner's reading of "user level" and "first use" (section 5). The feasibility stop-condition in research-notes (line 132) is therefore not triggered.

Supporting lines (each re-read in this session):

| Point | Research file and line | Quote |
|---|---|---|
| 6.9.0 has no user-scope install path, so a global or user-scope BMAD install is neither available nor needed | 01 line 79 | "**Conclusion (CODE-VERIFIED by whole-package Grep): in 6.9.0 there is NO consumer of `global_target_dir`; it is declared data and a comment only. Option F (upstream user-scope install via `global_target_dir`) has no code path in 6.9.0.**" |
| Same, from the tool step | 01 line 219 | "a user-scope (`~/.claude/skills`) install would need code that reads `global_target_dir` and an option to select it. Neither exists in 6.9.0 ... So option F is not available in 6.9.0; it would be an upstream feature request." |
| A per-project install stays inside the project and touches nothing in the user's home config | 01 line 217 | "it writes ONLY `.claude/skills/<skill>/` under the project. It writes no `.claude/settings.json`, no `.claude/commands`, no `CLAUDE.md`, nothing under `~/.claude`." |
| The CLI is already image-baked, and the install is non-interactive and offline-capable | 01 line 386 (Summary) | "a non-interactive install is `bmad install --directory <dir> --modules bmm --tools claude-code --yes`, and by the code it writes only inside that directory (`_bmad/`, `_bmad-output/{planning,implementation}-artifacts/`, `docs/`, `.claude/skills/bmad-*`), never touches git or `~/.claude`, and does not write under HOME or need the network for the built-in `bmm` module" |
| Per-project creation is needed, and it does not conflict with the "never globally" half of OD-1 | research-notes line 209 (F9-4) | "First-use creation therefore needs a mechanism that runs `bmad install --directory <project>` per project (Options B, C or D), which is not in conflict with the \"never globally\" half of OD-1." |
| NEEDS OTHER-REPO CHANGE: no for a user-level skill, no for a hook | 03 lines 178-179 (section 6) | "User-level skill (Options B / delivery via M1 or M2): **NO**. Every placement mechanism above is in this repo ... and superclaude leaves a non-packaged skill name alone." and "User-level hook (Option D via M3 or M4): **NO**. A hook entry with a new command string is preserved by superclaude's additive merge" |
| Same answer repeated in the answer index | 03 line 195 | "M1-M4 in this repo; NEEDS OTHER-REPO CHANGE: NO for skill, NO for hook" |
| Option C (wrapper) and the other image-level hook points are also inside this repo | 02 lines 324-325 (Key Takeaways) | "The cheapest classes are B3 and D3 (root `coder_script`, template push only) ... Only B (skill) and D (hook) can act where Claude Code is used; C (wrapper) fires only when `bmad` itself is executed." |
| No existing pinned test breaks for certain for the cheap variants | 04 line 501 | "Certain breaks per variant (summing section 7 and this addendum): B1 = test-57:450; B2 = none; B3 = none; C = none; D1 = test-57:450; D2 = none; D3 = none; E = test-57:450; F = test-57:450." |

Limits on this statement (none contradicts it, all keep it open):

- 03 line 180: the answer would become YES only "if the intent were to ship the skill or hook FROM IronClaude ... or to make superclaude prune or manage a BMAD-named surface"; also "if a future superclaude version starts pruning unknown directories under `~/.claude/skills/`: today it does not". Nothing in this repo asserts that user skills survive (the repo-side guard covers hook commands only).
- The Sysbox layer gate (02 line 431): B2 and D2 as written add one layer each against two free layers (68 of 70); B1, B3, D1, D3 and C-in-place add none.
- B1, D1, E and F (the last two only if run from `install.sh`) break `test-57:450` and need a replacement assertion (04 line 501; 05 F1.x).
- Version skew: the installer has no installed-versus-installer version gate, so 6.9.0 over a 6.10.0 or partial tree is a risk for B, C, D (01 F5-F, F5-D).
- The prior-review and CI figures (about 4 s with an npx fetch; 374 to 392 ms in CI) are "prior-review observation, not re-run".

## 7. Facts only a real fresh 6.9.0 install run could show

Evidence limit, not a user-intent question (task file open question 3): this task ran no `bmad install`, not even in a scratch directory. Everything below is UNVERIFIED and is an item for the implementation phase to observe in CI (project rule: validation through `.github` Actions, no one-off scripts). The report carries these in Section 9.

Rows tagged OBSERVED-FROM-6.10.0-TRACKED-TREE (research file 01 section 8) come from this worktree's git-tracked BMAD 6.10.0 tree (manifest version 6.10.0, installDate 2026-04-18) and are version-mismatched corroboration, not 6.9.0 installer output.

| # | Fact that only a real run shows | Research file and item | Gap | Item for the implementation phase to observe in CI |
|---|---|---|---|---|
| R-1 | Real duration of a first install in a Coder workspace and in a large repo; with live network | 01: U1, F5-4 | G-09 | yes |
| R-2 | Writes under HOME (for example `~/.bmad/cache`, `~/.npm`) during a bmm-only first install; side effects of `npm view` and `uv --version` | 01: U3, F5-11 (code shows `~/.bmad/cache` only for external or custom modules) | G-15 | yes |
| R-3 | Behaviour in a directory with no `.git` (does the install run, what is written) | 01: U11; 03: A5 #17 | G-10 | yes |
| R-4 | The exact per-file list a first install writes, including the `{output_folder}` substitution that yields `_bmad-output/planning-artifacts` | 01: U11, F5-5; 02: U6 | G-10 | yes |
| R-5 | Exact skill set, count and names written to `.claude/skills/` (46 versus 47) | 01: U12, F5-6 | G-11 | yes |
| R-6 | Whether the update banner under `NPM_CONFIG_OFFLINE=true` comes from the cache or the network | 01: U2 | G-15 | yes |
| R-7 | Output of `resolve_customization.py` with no `_bmad/`; the interpreter's error text; model behaviour in that state | 01: U5, U6 | G-07 | yes |
| R-8 | Skill behaviour when `project_name`, `communication_language`, `document_output_language` are absent (the `install.sh:42` flag set); which file(s) `--set` patches | 01: U13 | G-07 | yes |
| R-9 | Outcome of `--user-name` without `--output-folder` (literal `{output_folder}/` directory) | 05: U6 | G-14 | yes |
| R-10 | State left by a failed first run (partial `_bmad/`) and what quick-update does to it | 05: U7; 01: F5-8 | G-13 | yes |
| R-11 | Whether the manual command in `catalogue/bmad/manifest.yaml:13-14` completes end to end | 05: U8 | G-16 | yes |
| R-12 | What `bmad install --directory ~` (option E) writes | 02: U5; 04: gap 1; 05: U-F1-1, U3 | G-16 | yes |
| R-13 | Quick-update rewrites 6 files; 6.9.0 over 6.10.0 changes 41 files with rc 0 (prior-review observation, not re-run) | 01: F5-7; 05: U10 | G-14 | yes |
| R-14 | Seed-repo runtime result of the boot install in a fresh workspace (this workspace has no `seed-repo-path`); a fresh workspace's `~/.claude/` content | 05: U9; 03: Other open questions, A5 #13 | G-27, G-21 | yes |
| R-15 | Layer count and Sysbox-job result after the chosen option is built | 02: U15 to U20 | G-19 | yes |

Read-only items that are UNVERIFIED but closable by reading code, not by a run (so they are not in the table above): default module list of a bare `--yes` (01 U4, read `bmad-modules.yaml`), meaning of the `semver` hits (01 F5-12), unread tests (G-20).

Claude Code behaviour (G-01 to G-04) needs official documentation or a live Claude Code session, not an install run; it is assigned to web research in section 4.

## 8. Design questions carried from the research files (not evidence gaps)

These are decisions for the plan or the owner, copied so the synthesis can place them in Section 9 (owner ones) or Section 8 (plan). None is answered here.

| # | Question | Source |
|---|---|---|
| D-1 | Does a bootstrap need `_bmad/` creation to be atomic? The installer is not (a failed run leaves a partial `_bmad/`). | 01 (open question 1) |
| D-2 | Should a bootstrap guard on `_bmad/config.toml` rather than `_bmad/` alone? A bare `_bmad/` does not satisfy `resolve_config.py:156`. | 01 (open question 2) |
| D-3 | Which directory is "the project" when the user opens a subfolder of a repo? `find_project_root` stops at the nearest `_bmad` or `.git`; skills use `{project-root}` = working directory. | 01 (open question 3) |
| D-4 | Should a first-use mechanism also cover the `minimal` profile? bmad is not in it. | 02 (open question 1) |
| D-5 | Should deselecting bmad remove a user-level bmad artefact (orca cleanup, `modules.tf:82-109`) or follow bmad's current rule (marker never removed, `startup.sh:1114-1117`)? | 02 (open question 2) |
| D-6 | Should the failed-first-install behaviour (`install.sh:41, 24`) be revisited if first use can also create `_bmad/`? | 02 (open question 3) |
| D-7 | Which approach is acceptable for the Renovate-visible strings if `install.sh` is rewritten (`expected.txt:6-8`)? | 02 (open question 4); 05 (open question 3) |
| D-8 | Do the 60 s `superclaude install` and 75 s outer bounds matter for a new boot step? (Not for M1; relevant to any step added inside the ironclaude slug.) | 03 (Other open questions) |
| D-9 | Does the new decision cover the boot (seed) path unchanged and only add first-use creation after boot? | 05 (open question 1) |
| D-10 | Should first-use files be hidden with `info/exclude` as the seed install does, or left visible? (owner input, see G-26) | 05 (open question 2, U17) |
| D-11 | Is the deselected-BMad marker question (`sprint-status-orca-gap-closure.yaml:42`) closed in the same decision? It is separate and still open. | 05 (open question 4) |
| D-12 | If B1 or D1 is chosen, is the stub also wanted when no seed repo is recorded? A stub written only with a seed passes `test-57:450` but does not serve the "project that never had BMAD" case; writing it unconditionally needs the replacement assertion at 04:77. | 05 (F1.5 open question 1) |
| D-13 | Does the owner prefer the variants with no certain break (B2, B3, C, D2, D3)? They avoid `test-57:450` but carry BREAKS-IF rows. | 05 (F1.5 open question 2) |
| D-14 | Health and Configured for a user-created project: `spec2_health_observed bmad` inspects only the registered seed repo, so no option makes health report Configured for another project unless `spec2-health.sh` and test-57 `record_health` rows change together. | 04 (Other questions) |
| D-15 | The "no seed" case is "no repo registered in `seed-repo-path`", not "a repo without BMAD"; a new test row is needed for the new behaviour. | 04 (Other questions) |
| D-16 | State in the Recommendation which of R1 to R12 prior-diagnosis positions are overridden by name; keep the three-way split of the original ask (global declined, first-use decided, Ponytail out of scope) so #478's "available globally" text is answered "declined". | research-notes (F9-5 questions for the synthesis author) |
| D-17 | Which of the three extraction sites (`Dockerfile.coder:139`, `install.sh:18`, `manifest.yaml:2`) will the chosen option touch? | 05 (open question 3) |

## Summary

- Open gaps: 27 (section 1; 3 further rows resolved by fix). None is Critical; 14 are Important (G-01 to G-10, G-13, G-16, G-19, G-26) and 13 are Minor.
- Web research: G-01, G-02, G-03, G-04 to web-01; G-05 to web-02.
- Claims listed: 89 UNVERIFIED (79 still open) and 30 CODE-CONTRADICTED, 13 STALE DOC.
- Owner questions: 2 copied unanswered (section 5), plus the decision-wording input G-26.
- Feasibility (section 6): feasible without a global BMAD install and without an IronClaude or IronOrca change on the evidence so far; the choice among B, C, D is not yet determinable (G-01, G-02, section 5).
- Run-only facts for CI observation: 15 (section 7).

**Status:** Complete

