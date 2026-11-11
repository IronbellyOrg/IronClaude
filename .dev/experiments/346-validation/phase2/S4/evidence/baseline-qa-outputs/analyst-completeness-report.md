# Research Completeness Verification (Gate 1, analyst 1 of 3)

**Scope:** Completeness verification of the research files 01-05 for "BMAD first-use directory creation in a project that never had BMAD (BMAD-METHOD 6.9.0, Coder AIDev02 workspace)". Depth tier: Standard.
**Status:** Complete
**Date:** 2026-11-07
**Files analyzed:** 5 research files (01-05) plus research-notes.md (scope), all read in full
**Depth tier:** Standard
**Analysis type:** completeness-verification (fix_authorization: false; read-only)

---

## Verdict: FAIL (2 Important gaps, 0 Critical; Minor notes listed). Verdict is repeated with counts in the closing Summary.

## 1. Coverage Audit

| Scope item (research-notes EXISTING_FILES / assignments) | Covered by | Status |
|---|---|---|
| BMAD 6.9.0 installer, ui.js, installer.js, _config-driven.js, platform-codes.yaml, resolve_config.py, resolve_customization.py, SKILL.md runtime, memlog.py | 01 sections 1-7 | COVERED |
| `global_target_dir` consumers (known item 1) | 01 section 2 (whole-package Grep); 02 s3 | COVERED (see section 6) |
| Image CLI wrapper `/usr/local/bin/bmad`, Dockerfile.coder:133-145 | 02 s1; 04 s4 | COVERED |
| `catalogue/bmad/{install.sh,manifest.yaml,module.tf}` | 02 s2, s4.1-4.3; 03 s2; 04 s2.1; 05 | COVERED |
| `profiles.yaml`, `catalogue/README.md`, `modules.tf`, `parameters.tf`, `main.tf` image hash | 02 s4.4-4.6, s6.0 | COVERED |
| `spec2-health.sh` bmad handling | 02 s5; 04 s2.1; 05 a11 | COVERED |
| startup.sh section 8 (:669-681), section 9 (:1113-1182), post-section 9 sync | 03 s2; 02 s2; 05 | COVERED (sections 10-12, :1348-1863 not read; 03 U10 gives the reason and a whole-file Grep) |
| HOME persistence (main.tf volumes) | 03 s1 | COVERED |
| `~/.claude/settings.json`, `~/.claude/skills/` writers; `superclaude install` overwrite semantics (known item 2) | 03 s3-s5 | COVERED (see section 6) |
| `catalogue/ironclaude/install.sh` | 03 s3 | COVERED |
| `/opt/uv/tools/superclaude/.../install_user_setup.py`, `user_settings_defaults.json`, `install_hooks.py`, `install_skills.py` | 03 s5 | COVERED |
| Skill behaviour when `_bmad/` absent (known item 3) | 01 s7 | COVERED at code level (see section 6) |
| test-57 (bmad blocks :173, :323-345, :413-465, no-seed :446-452) | 04 s1-2; 05 supplement | COVERED |
| test-46, test-19, test-49, test-52 | 04 s3-6 | COVERED |
| test-startup-boot.sh bmad cases (35 hits) | 05 (a) | COVERED |
| Workflow wiring of the five tests | 04 s8 | COVERED |
| Owner-decision trail: owner-decisions.md:5, .memlog.md:27-34, gap-closure SPEC.md:29,77, catalogue-bundle SPEC.md:65,126,141,174, slug-configuration.md | 05 (b) | COVERED |
| README.md:241 and :308, catalogue README, markdownlint, Renovate/expected.txt | 05 (e), (f); 02 s4.6 | COVERED |
| CHANGELOG convention, OD numbering | 05 (c) | COVERED |
| Prior diagnosis `.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/REPORT.md` (141 lines) | research-notes.md only; Grep for `troubleshoot`/`REPORT.md` over 01-05 finds no research file that read or cross-validated it | GAP (Minor, see G-M1) |
| `.dev/issues/478/` working files (12 files) | 05 c1 reads one line of `accuracy-check.md:16` only | PARTIAL (Minor, see G-M1) |
| Contract tests that pin `startup.sh` / `Dockerfile.coder` / image inputs / generic catalogue shape (test-1 shape, test-2, test-7, test-44, test-47, test-60, test-67, test-71, test-73, ...) | 03 and 02 name them; read only in part (test-7/67/73 grep lines; test-1:112-117) | GAP (Important, see G-I2) |

## 2. Evidence Quality

Exact claim counts were not tallied (hundreds of claims); the table gives the observed pattern and the unsupported items I found. Every file cites file:line for essentially all code claims.

| Research file | Evidenced claims | Unsupported / weakly supported claims found | Rating |
|---|---|---|---|
| 01 installer and skill runtime | Very high: every table row carries file:line | (a) line 18 says host Node was "path-derived; `node --version` not run" but line 128 says "OBSERVED via `node --version`" (internal inconsistency, G-M2); (b) section 7.4 skill counts (46 / 40 / 37 SKILL.md) rest on Grep count output and were not re-run by me | Strong |
| 02 image CLI and slug | Very high | (a) "Docker rebuilds layers after a changed layer" is stated as standard behaviour, flagged U8; (b) several README path claims are cited by line and tagged | Strong |
| 03 startup, HOME, user-level Claude | High | (a) section 4 live-HOME facts are observations (no line cites by nature); (b) M4 precedence claim is "doc-sourced" but not given a CODE-VERIFIED / UNVERIFIED tag on that sentence (hook-merge part is tagged UNVERIFIED); (c) `Dockerfile.coder:468` budget statement is a comment quote (I verified the comment exists at :468) | Strong |
| 04 pinned tests | Very high: assertion text, line and option impact for every row | (a) option columns E and F are built from the question wording, not from 01 (admitted in its section 7 legend and Gap 1); (b) "tests not run" (Gap 5) | Strong |
| 05 startup-boot, docs, decision trail | Very high: verbatim quotes with line numbers and a tag per row | (a) a10/a11 option effects for E/F marked UNVERIFIED; (b) U17 (owner wording on git cleanliness) is an honest input gap | Strong |

## 3. Documentation Staleness

All five files tag doc-sourced claims. I found no untagged doc-sourced architectural claim presented as current fact, except the two small items below. No `[CODE-CONTRADICTED]` claim is reported as current fact in any file.

| Claim | Source doc | Verification tag | Status |
|---|---|---|---|
| `global_target_dir` = "User-home directory for global install" | platform-codes.yaml:9 | `[STALE DOC]` / C1 in 01 (I reproduced: 43 hits, all in platform-codes.yaml) | OK |
| `ancestor_conflict_check` advertised | platform-codes.yaml:10 | `[STALE DOC]` in 01 s6 (I reproduced: only `_config-driven.js:191` reader plus the comment) | OK |
| "T1-T55" | docs/generated/PROJECT_INDEX.md:13,36,65 | `[STALE DOC]` in 04 s9 (I confirmed the three lines) | OK |
| install.sh:18 message says "symlink" | install.sh:18 | `[STALE DOC]` in 02 (I confirmed install.sh:18 versus Dockerfile.coder:134-143) | OK |
| "BMad is installed per project only, never globally" | owner-decisions.md:5 | `[CODE-CONTRADICTED]` for the CLI, true for content (05 C1; I confirmed owner-decisions.md:5 and Dockerfile.coder:139) | OK |
| `.memlog.md:27` "seed repo gets no _bmad/" | .memlog.md:27 | `[STALE DOC]` in 05 (I confirmed lines 27 and 32) | OK |
| managed settings "highest precedence" / settings "when edits take effect" | code.claude.com settings page (via WebFetch) | 03 marks the hook-merge and live-reload parts `[UNVERIFIED]`; the precedence sentence itself is labelled "doc-sourced" with no tag | FLAG (Minor, G-M3) |
| Prior diagnosis REPORT.md statements | `.dev/troubleshoot/.../REPORT.md` | not examined by any research file | FLAG (Minor, G-M1) |

## 4. Completeness (checklist item 4)

| Research file | Status | Summary | Gaps section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-bmad-6-9-0-installer-and-skill-runtime.md | Complete (line 4) | Y (line 360) | Y (line 319) | Y (per section, e.g. lines 49, 83, 137, 174, 200, 219, 279, 314) | Complete |
| 02-image-cli-and-catalogue-slug.md | Complete (line 4) | Y (line 378) | Y (line 329) | Y (per section, e.g. lines 62, 103, 130, 210, 250, 323) | Complete |
| 03-startup-flow-home-and-user-level-claude.md | Complete (line 4) | Y (line 234) | Y (line 197) | Y (per section, e.g. lines 31, 61, 86, 122, 153, 182) | Complete |
| 04-pinned-tests-57-46-19.md | Complete (line 4) | Y (line 265) | Y (line 236) | Y (per section, e.g. lines 54, 83, 122, 144, 161, 176) | Complete |
| 05-startup-boot-test-docs-and-decision-trail.md | Complete (line 4) | Y (line 289) | Y (line 236) | Y (per part, e.g. lines 32, 56, 138, 169, 193, 215, 232) | Complete |

All five files satisfy checklist item 4. Note: none carries one single end-of-file "Key Takeaways" block; each carries them per section. I accept that as meeting the requirement.

## 5. Cross-Reference Check

Good cross-references: 02 s2 and 03 s2 agree on the unbounded bmad subshell (startup.sh:1170-1182) and sort order; 02 s5, 04 s2.1 and 05 a11 agree on `spec2-health.sh:99-114` (seed-only observation); 02 and 04 both note the wrapper is a script, not a symlink; 04 s8 and 05 agree on workflow wiring; 03 s6 and 02 s6 agree that no IronClaude or IronOrca edit is needed.

Defects: the agents ran in parallel, so several items one agent closed are still shown as open by others, and 04 explicitly defers to "Agent 01/02 findings" without a reconciliation step. These are listed in section 6 (X1, X3, X6). The synthesis must apply 01's results to 02, 04 and 05 rather than copy their UNVERIFIED labels.

## 6. Contradictions Found

| # | Contradiction | Files and lines | Severity |
|---|---|---|---|
| X1 | **Options B and D versus the "no seed: bmad writes nothing" pin (test-57:450).** 04 s7 matrix marks B and D as `X` (certain break) because a skill or hook written by `bmad/install.sh` lands inside the whole-HOME `snap`. 05 (a-supplement row 449-452, and Key Takeaways) says "B and D are unaffected because they run after boot, outside install.sh" and "Options A, B and D leave every row of this table unchanged". The two files use different meanings of "B" and "D". 02 s6.1 and s6.3 show the delivery variants differ: B1 and D1 write from `install.sh` at boot (breaks test-57:450 and, for D1, the `ic_hooks` predicate at test-57:140); B2 seeds from `/etc/skel` through startup section 6 (not exercised by test-57, which runs only `install.sh`; touches Dockerfile.coder, `image_input_files`, startup.sh); B3 and D3 use a root `coder_script` (no install.sh, no image retag). I verified `snap` (test-57:148-153, covers all of HOME except `.aidev/installed/*`) and the assertion at test-57:446-450, so 04 is right for B1 and D1 and 05's blanket statement is wrong for them. 05's phrase "first-use bootstrap that happens after boot" confuses when the artifact is deployed (boot) with when it is used (first use). | 04 s7 vs 05 supplement + Key Takeaways; 02 s6.1, s6.3; test-57:146-153, 446-450 | **Important** (G-I1) |
| X2 | Host Node version: 01 line 18 says "path-derived; `node --version` not run"; 01 line 128 says "OBSERVED via `node --version`". | 01:18 vs 01:128 | Minor |
| X3 | Option F / `global_target_dir`: 01 s2 and s5 give a CODE-VERIFIED "zero consumers in 6.9.0" (I reproduced: 43 occurrences, one file, `platform-codes.yaml`). 02 s3 and U4 still say "[UNVERIFIED]"; 04 s7 puts `X` marks in the F column (writes under HOME, "UNVERIFIED"); 05 U1-U3 treat F effects as UNVERIFIED. Under 6.9.0 option F has no code path at all, so those F cells describe a non-existent behaviour. Likewise 01 s6 derives what E (`--directory ~`) writes (`~/_bmad`, `~/_bmad-output/...`, `~/docs`, `~/.claude/skills/bmad-*`) while 02 U5, 04 and 05 call it UNVERIFIED. | 01:54-79, 198, 213-217; 02:121,131,320-321; 04:182-183,239; 05:242-244 | Minor (reconcile in synthesis) |
| X4 | `--user-name` safety: 01 s3.2 lists `--user-name` among "optional extras that stay non-interactive". 05 d5 warns that passing `--user-name` without `--output-folder` may leave `output_folder` unseeded. I read `ui.js:807-862`: the default seeding (`output_folder: '_bmad-output'`, :838-861) is an `else if` branch that runs only when none of the four core flags is passed, so 05's mechanism is right and 01's note is incomplete. Whether a literal `{output_folder}/` directory results is traced by neither (core config collection under `skipPrompts`, `official-modules.js:1043-1046`, not read). The shipped command (`install.sh:42`) passes both flags, so it is safe. | 01:116; 05:184, 247, 268; ui.js:807-862 | Minor |
| X5 | Non-contradictions I checked and cleared: 04 says the test-57 two-step total (bmad + ironclaude) is capped at 30 s (test-57:173-183, `BUDGET_MS=30000`), 05 says the reprofiled-HOME loop excludes bmad (test-57:9-11 header) and test-startup-boot caps the sum at 75 s; these are three different checks and all three descriptions match the code I read. | test-57:9-11, 31, 173-183 | none |
| X6 | `research-notes.md` calls `install.sh` 62 lines; 02 and 05 say 61. The file has 61 lines (I read it). | notes:27 vs 02:67 | Minor (notes file, not under review) |

## 7. Status of the Three Known UNVERIFIED Items

| Known item | Resolution in research | My check | Verdict |
|---|---|---|---|
| 1. Any consumer of `global_target_dir` in BMAD 6.9.0 | 01 s2: whole-package Grep, 43 occurrences in exactly one file (`platform-codes.yaml`: 2 comments, 41 values); `_config-driven.js:245-248` writes only to `projectDir/target_dir`; `install.js:12-51` has no scope flag | Re-ran the count Grep over the package root: 43 occurrences, 1 file. Read `_config-driven.js:245-248` and `platform-codes.yaml:5-57`. Also confirmed `ancestor_conflict_check` has one reader (`_config-driven.js:191`) and no platform sets it. | RESOLVED with code evidence |
| 2. Whether `superclaude install` would overwrite a user-level hook or skill | 03 s5: hooks merge additively by exact command; defaults fill-only; skills replaced only for packaged names (39) plus unconditional `rmtree` of stale `sc-*` with a command; `bmad-*` collides with nothing. Residual open: 03 U2 (the `_src/` copy not compared) and U11 (`wire_ccsession` unread) | Read `install_skills.py:80-119` (rmtree at :97 matches). Read `install_ccsession.py:1-100`: `wire_ccsession` touches only `~/.claude/skills/ccsession-tag/*`, `~/.local/bin/ccsession*` and `~/.claude/ccsession.env`, so U11 is closed by me. A Grep for `rmtree|unlink` across `cli/install*.py` finds skills-directory removal only at `install_skills.py:97` and `install_skill.py:48`. U2 (`_src/` copy) I did not compare: stays UNVERIFIED, Minor. | RESOLVED with code evidence (one Minor residual) |
| 3. What happens when `_bmad/` is absent at skill run time | 01 s7: `resolve_config.py` exits 1 with `required config file not found` (`:48-51`, call at `:156`); `resolve_customization.py` walks up to `_bmad` or `.git` and degrades to skill defaults; no skill detects a missing `_bmad/` (Grep over `src/`); skills hard-reference `{project-root}/_bmad/...` (40 SKILL.md). Model-level behaviour left open as U5/U6 with a reason (an install or skill run is forbidden by the BMAD CLI RULE) | Read `resolve_config.py:140-164` and `resolve_customization.py:55-66`: both match. The open part (how the model behaves, the interpreter's error text) has an explicit reason. | RESOLVED at code level; model behaviour explicitly OPEN with reason (acceptable) |
| (4. Claude Code loading skills created after session start) | answered later by web research | not a gap here | n/a |

## 8. Compiled Gaps (de-duplicated across all five files)

### Critical Gaps (block synthesis)

None. No file contains fabricated content, no `[CODE-CONTRADICTED]` item is presented as current fact, and every research file is Complete.

### Important Gaps (affect quality; these make the verdict FAIL)

- **G-I1. Per-variant test impact is contradictory between 04 and 05 for options B and D** (X1). Source files: 04 s7 vs 05 supplement (rows for test-57:449-452) and its Key Takeaways; 02 s6.1/s6.3 hold the variant definitions. Effect: Section 6 (Options) and Section 8 (Plan) of the report would either wrongly clear B1/D1 of the test-57:450 break or wrongly condemn B3/D3. Remediation: before synthesis, the orchestrator (or a short follow-up Code Tracer) produces one table with rows B1, B2, B3, C, D1, D2, D3, E, F and columns test-57:450, test-57:331-335, test-57:140 `ic_hooks`, test-startup-boot (a8, a11, a13), test-19 install.sh shape, test-7, test-67; 05's "B and D leave every row unchanged" is corrected to apply only to B3 and D3.
- **G-I2. The inventory of contract tests that pin image inputs is incomplete for image-touching variants.** A Grep for `startup.sh|Dockerfile.coder|aidev-startup` over `.github/contract-tests/` returns 141 hits in 30 files. Read only in part: test-7 (11 hits), test-67 (8), test-73 (8; 03 s6 M4 and Gap 6 admit a second drop-in file is untested). Not read: test-60 (5 hits; 02 s6.2 and U11 say it extracts the `claude` wrapper by its printf block, which bears on Option C), test-71 (9), test-51 (12), test-68 (6), test-59-home-workspaces-dir (6), test-72 (4), test-77 (4), test-b1 (3), test-1-tool-floor (3), test-18 (3); and the tests that iterate the catalogue generically (test-1 shape, test-2, test-44, test-47, 04 Gap 3). The research notes require Section 8 to "name the pinned tests and docs that must change"; for B2 (startup.sh + Dockerfile COPY + `image_input_files`), C (Dockerfile.coder:136-145) and D2 (`managed-settings.d`) that list cannot be completed from the current files. Remediation: one bounded follow-up pass over exactly those files, recording for each the assertion text, line, and which variant breaks it (same table shape as 04 s2).

### Minor Gaps (notes; do not fail the gate, but must be fixed or carried)

- **G-M1.** `.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/REPORT.md` (141 lines) and the 12 files under `.dev/issues/478/` were listed as EXISTING_FILES but no research file cross-validated them (only `accuracy-check.md:16` is touched, by 05 c1). The prior report's "bmad user-scope skill install UNVERIFIED" is now answered by 01 s2/s5; the synthesis should say so.
- **G-M2.** 01 line 18 vs line 128 (Node version "not run" vs "OBSERVED"); correct one of them.
- **G-M3.** 03 s6 M4: the managed-settings precedence statement is "doc-sourced" without a verification tag.
- **G-M4.** Stale UNVERIFIED labels for resolved items (X3): 01 U9/U10/U12 versus 02 (Dockerfile.coder:139 CODE-VERIFIED, which I also read), 02 U4 and U6 versus 01 s2 and s4, 04/05 F and E columns versus 01 s2, s5, s6. The synthesis must carry 01's resolution.
- **G-M5.** `--user-name` without `--output-folder` (X4): outcome untraced (core config collection under `skipPrompts`); keep `--output-folder _bmad-output` in every command, as 05 already advises.
- **G-M6.** 03 U2 (`_src/superclaude/cli/` copy not compared). I closed 03 U11 (`wire_ccsession`) and U10 (startup.sh `.claude`/`skills`/`settings.json` references: my Grep shows only lines 275, 979, 1282, 1285), so only U2 remains.
- **G-M7.** Items that can be closed only by a real `bmad install` run (01 U1 duration, U11 exact file set, partial-`_bmad/` behaviour; 05 U7, U8). The BMAD CLI RULE forbids a run here. Carry them to Open Questions and to the plan's Actions-based validation (project CLAUDE.md forbids one-off scripts).
- **G-M8.** Owner-reading items are correctly carried by the agents and are not research gaps: whether a stub at user level is allowed (OD-1 wording "or at user level"), the meaning of "first use", git cleanliness of first-use files (05 U17), and the open deselected-marker question (sprint-status yaml:42). Confirm they appear in Open Questions.

## 9. Depth Assessment

**Expected depth (Standard):** file-level understanding with key function documentation; for each of the five assignments an answer to every listed question.
**Actual depth:** at or above Standard. 01 traces the full install call chain and the exact file set from `ui.js`, `installer.js`, `manifest-generator.js`, `official-modules.js` and the runtime scripts; 02 gives per-line install.sh behaviour, hook points with rebuild class per variant, and health states; 03 gives boot order, persistence, writers and overwrite semantics from source; 04 gives per-assertion option impact with replacement assertions; 05 gives the full document trail with how each must change, README/markdownlint/Renovate constraints and a CHANGELOG convention. Each assignment's questions (research-notes SUGGESTED_PHASES rows 01-05) are answered; the one exception is the incomplete test inventory in G-I2, which exceeds the literal assignment of agent 04 and 05 but is required downstream.
**Missing depth elements:** G-I1 and G-I2 only.

## 10. Recommendations

1. Resolve G-I1: add the per-variant impact table (B1/B2/B3, C, D1/D2/D3, E, F) and correct 05's blanket statement before synthesis uses either file.
2. Resolve G-I2 with one bounded follow-up tracer pass over test-7, test-60, test-67, test-73, test-71, test-51, test-1/2/44/47 for image-touching variants.
3. Tell the synthesis agents to treat 01 s2, s5, s6 as authoritative for options E and F (F has no code path in 6.9.0; E writes `~/_bmad` and friends) and to drop the F `X` cells in 04 s7.
4. Fix Minor items G-M2 and G-M3 in the research files; carry G-M1, G-M5, G-M7 and G-M8 into the Open Questions section.
5. Keep the superclaude conclusion (NEEDS OTHER-REPO CHANGE: NO) but cite 03 U2 as the one unverified residual.

## 11. Spot-Check Log (cited references re-read by me; the prompt required at least ten)

| # | Cited reference (source file) | What I read | Result |
|---|---|---|---|
| 1 | `catalogue/bmad/install.sh:18, 21-25, 32-34, 42, 46, 48-53, 58-60` (01, 02, 03, 04, 05) | whole file (61 lines) | matches every cited line and the guard/exit-code description |
| 2 | `Dockerfile.coder:133-145` (01, 02) | lines 130-147 | matches (pin at :139, wrapper at :142-143) |
| 3 | `Dockerfile.coder:468, 586, 593, 501` (03, 02) | Grep | matches (budget comment :468, startup COPY :586, catalogue COPY :593, drop-in :501) |
| 4 | `global_target_dir` count (01 s2) | Grep count over the package root | 43 occurrences, 1 file: matches |
| 5 | `ancestor_conflict_check` (01 s6, 02 s3) | Grep content | one reader `_config-driven.js:191`, one comment `platform-codes.yaml:10`: matches |
| 6 | `resolve_config.py:143-163` (01 s7.1) | lines 140-164 | matches: required `--project-root`, `config.toml` required, no walk-up |
| 7 | `resolve_customization.py:58-66` (01 s7.2) | lines 55-66 | matches `find_project_root` (`_bmad` or `.git`) |
| 8 | `ui.js:630-641` (01 s3, 05 d4) and `ui.js:807-862` (01, 05 d5) | lines 625-643 and 800-865 | both match; 807-862 confirms the `else if` defaults branch (X4) |
| 9 | `startup.sh:1113-1117, 1170-1182` (02, 03, 05) | lines 1110-1184 | matches (bmad exempt from unmark; bmad run without the 30 s bound) |
| 10 | `spec2-health.sh:74-81, 99-114` (02, 04, 05) | lines 72-117 | matches (`seed-config`, seed-only observation) |
| 11 | `test-57:148-153, 446-452, 173-183, 9-11` (04, 05) | lines 1-40, 144-159, 168-185, 444-453 | matches `snap` definition and the no-seed assertion; header and loop timing per X5 |
| 12 | `test-19:192-220` regex and classifier (04) | lines 192-221 | matches |
| 13 | `install_skills.py:88-110` (03 s5) | lines 80-119 | matches (rmtree only of stale `sc-*` with a command) |
| 14 | `platform-codes.yaml:9-12, 52-57` (01, 02) | lines 5-59 | matches |
| 15 | `test-52:1378-1384` (04) | lines 1374-1385 | matches exact profile mapping assertion |
| 16 | `renovate-global.json5:44-58` (05 f) | lines 42-59 | matches (three extraction sites) |
| 17 | `owner-decisions.md:5`, `.memlog.md:27, 32-34` (05 b1) | full file / lines 24-35 | matches quotes; confirms OD-1..OD-3 so next free is OD-4 |
| 18 | `test-startup-boot.sh:2209-2211, 2224` (05 a11) | lines 2204-2227 | matches |
| 19 | `_config-driven.js:189-207, 245-248` (01 s5, s6) | lines 186-210, 240-252 | matches |
| 20 | `main.tf:174-176` (03 s1) | lines 172-181 | matches home volume name |
| 21 | gap-closure `SPEC.md:29, 77`; catalogue-bundle `SPEC.md:65, 126, 141, 174` (05 b1, b2) | Grep with line numbers | all six quotes match |
| 22 | `modules.tf:50-54, 82-109` (02, 03) | lines 48-109 | matches (module count gate; `orca_retirement` script) |
| 23 | `test-1-catalogue-shape.sh:112-117` (05 e) | lines 108-120 | matches the 4-file reject self-test |
| 24 | `install_ccsession.py` (03 U11) and `rmtree|unlink` across `cli/install*.py` | whole file lines 1-100 plus Grep | only ccsession-tag, `~/.local/bin`, env file; skills `rmtree` only at install_skills.py:97 and install_skill.py:48 |
| 25 | `src/bmm-skills/module.yaml:28-47` (01 s4) | whole file | matches `directories` list (planning, implementation, project_knowledge) |
| 26 | `coder-ci-aidev02-contract.yml:1234, 1237, 1241` (04 s8) | Grep with line numbers | matches |
| 27 | `docs/generated/PROJECT_INDEX.md:13, 36, 65` (04 s9) | Grep | matches the three "T1-T55" lines |
| 28 | `bmad-cli.js:20-45` update check (01, 02) | Grep | matches `checkForUpdate`, `npm view`, "Update Available" |

28 references checked; 28 matched. No cited line was wrong. The only defects found are consistency and coverage defects, not citation errors.

## Self-Audit

What I actively did:
- Read in full: `research-notes.md`, and research files 01 (365 lines), 02 (381), 03 (237), 04 (268), 05 (292, in two reads of lines 1-228 and 229-292).
- Applied all 8 checklist items: coverage (section 1), evidence quality (2), staleness (3), completeness headers (4), cross-references (5), contradictions (6), gap compilation plus the three known items (7, 8), depth (9).
- Re-read 28 cited references against source (section 11) in `/opt/nvm/...`, `/opt/uv/tools/superclaude/...`, the templates tree, the contract tests, the workflows and the owner-decision documents; ran a Grep for `startup.sh|Dockerfile.coder|aidev-startup` over `.github/contract-tests/` (141 hits, 30 files) to size G-I2; ran a Grep for `troubleshoot|REPORT.md|accuracy-check` over research files 01-05 to test the REPORT.md coverage claim (G-M1).
- Did NOT: run any `bmad` command, any test, any install; open any file outside the read-only paths; edit anything except this report. Items I did not observe: model behaviour of a skill without `_bmad/`, real install duration, `_src/` copy of superclaude, Claude Code runtime behaviour (all stay UNVERIFIED and are labelled as such above).

Why I believe the counts (0 Critical, 2 Important, 8 Minor) are right:
- Zero Critical: I found no fabricated claim in 28 sampled citations spanning all five files, no `[CODE-CONTRADICTED]` item reported as current fact, and no file lacking Status/Summary/Gaps/Key Takeaways. The research is unusually well cited, so I looked for defects in cross-file consistency and in coverage rather than in citations.
- Two Important: G-I1 is a direct, reproducible contradiction between 04 and 05 that I confirmed against test-57:146-153 and :446-450. G-I2 is a measurable coverage hole (30 files, 141 hits, with named unread tests) against a downstream requirement stated in research-notes (Section 8 must name the pinned tests).
- Eight Minor: G-M1 to G-M8 as listed; they do not change any option ranking by themselves.
- I considered and rejected as non-defects: the 30 s versus 75 s timing descriptions (X5), the Update Available banner under `NPM_CONFIG_OFFLINE=true` (reported identically by 01, 02, 05), the "62 versus 61 lines" difference (notes file only), and the web-research question on mid-session skill loading (explicitly out of scope).
- Limit of this audit: I did not recount SKILL.md totals (46/40/37/75) or re-read the 3,061-line test-startup-boot.sh beyond lines 2204-2227; those rest on the agents' Grep counts.

### Summary

- Research files: 5 of 5 Complete; evidence quality Strong in all five.
- Known UNVERIFIED items: 1 RESOLVED, 2 RESOLVED (one Minor residual), 3 RESOLVED at code level with the model-behaviour remainder explicitly open.
- Findings: Critical 0, Important 2 (G-I1, G-I2), Minor 8 (G-M1 to G-M8). Contradictions: 1 Important (X1), 4 Minor (X2, X3, X4, X6).
- Verdict: **FAIL** (2 blocking gaps). Remediation: resolve G-I1 and G-I2 as described in section 8 and section 10, then re-check; the research is otherwise fit to feed web research and synthesis.
