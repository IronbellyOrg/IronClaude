# Synthesis Accuracy and Source-Tracing Verification (Gate 2, analyst 1 of 3)

**Scope:** Four synth-*.md files in synthesis/ traced to research/ files; topic "BMAD first-use directory creation in a project that never had BMAD (BMAD-METHOD 6.9.0, Coder AIDev02 workspace)"
**Status:** Complete
**Date:** 2026-11-08
**Analysis type:** synthesis-accuracy (Synthesis Quality Review, 10-item checklist, plus source tracing)
**Agent:** rf-analyst, Gate 2 report-only agent 1 of 3, fix_authorization: false (read-only on synthesis and research files)

---

## Section A. Per-file review (checks 1 to 10)

STOP-AND-RE-SCOPE branch decision: `synth-03` line 344 states "Stop condition: not triggered" and "No re-scope is needed on the evidence in hand". Section 8 (`synth-04` line 13 onward) opens with "Plan basis", not "RE-SCOPE PROPOSAL". Section 8 is therefore judged as an implementation plan (check 6), not as a re-scope proposal.

Legend: PASS, FAIL, N/A (the check does not apply to the sections that file holds), PASS* (passes, with a MINOR note in Section C).

### synth-01-problem-current-state.md (Sections 1 and 2; 521 lines)

| Check | Result | Evidence |
|---|---|---|
| 1 Headers | PASS | `## 1. Problem Statement` (line 10) and `## 2. Current State Analysis` (line 26), sub-sections 2.1 to 2.6 |
| 2 Table structure | N/A | No gap, option or plan table belongs here; evidence tables are well formed |
| 3 No fabrication | PASS | Claims traced to research lines (Section B rows 1 to 24); no claim without a research or code source |
| 4 Cites paths and evidence | PASS | Every table row carries `file:line`; every figure names its run id or Grep method |
| 5 Options | N/A | Options belong to synth-03 |
| 6 Plan | N/A | Plan belongs to synth-04 |
| 7 Cross-references | PASS* | One wrong pointer (line 246, "see section 2.5") and the "last three derived by subtraction" wording, MINOR-1 and MINOR-2 |
| 8 No doc-only claims in Section 2 | PASS | Claude Code behaviour rows are tagged "doc-sourced / inferred; UNVERIFIED" (line 222) and line 246 says web research "is not used" by this file; the 6.10.0 tracked tree is labelled corroboration only (line 89) |
| 9 Stale docs surfaced | PASS | Contradiction and stale lists at lines 91, 175, 323, 384 and the table at 482 to 494 |
| 10 Key-finding coverage | PASS | R01 Summary (R01:386) and last Key Takeaways (R01:335-338), R02 Key Takeaways (e) (R02:323-327) and Summary (R02:382), R03 Summary (R03:238), R04 Summary (R04:269), R05 Key Takeaways (R05:138-142, 169-172, 193-196, 215-218, 232-234) are all present in 2.1 to 2.6 |

### synth-02-target-gaps-external.md (Sections 3, 4, 5; 466 lines)

| Check | Result | Evidence |
|---|---|---|
| 1 Headers | PASS | `## 3. Target State`, `## 4. Gap Analysis`, `## 5. External Research Findings` |
| 2 Table structure | PASS | 4.1 and 4.2 use `Gap \| Current State \| Target State \| Severity \| Notes`; 3.2 uses an ID / statement / basis / status table; 3.3 uses a constraints table |
| 3 No fabrication | PASS | 4.2 maps one to one to GL G-01 to G-30 (GL:24-53); 4.3 covers CC-01 to CC-30 and SD-01 to SD-13 exactly once (every ID cross-checked against GL:159-208); Section 5 findings trace to W01 and W02 lines (Section B rows 28 to 32) |
| 4 Evidence | PASS | Section 5 findings carry source URL, relevance and relationship |
| 5 Options | N/A | |
| 6 Plan | N/A | |
| 7 Cross-references | PASS* | 4.4 routes every design question D-1 to D-17 and both owner questions to Sections 7, 8 or 9; F-04 wording is slightly broad (MINOR-4) |
| 8 No doc-only claims | N/A | Sections 3 to 5 are outside the check-8 list; external material is labelled "external context" and "doc-only" throughout (line 234) |
| 9 Stale docs surfaced | PASS | 4.3 carries all 30 CODE-CONTRADICTED and 13 STALE DOC rows; F-10 and F-11 carry the two upstream stale comments |
| 10 Key-finding coverage | PASS | W01 and W02 Key External Findings, Recommendations and Summary are reflected in 5.1 to 5.3 (19 plus 18 findings) |

### synth-03-options-recommendation.md (Sections 6 and 7; 397 lines)

| Check | Result | Evidence |
|---|---|---|
| 1 Headers | PASS | `## 6. Options Analysis`, `## 7. Recommendation` with Recommended approach, Rationale, Feasibility statement, Dependence on the owner readings |
| 2 Table structure | PASS | `Criterion \| A \| B1 \| ... \| F` (Table 1, line 250) and a G to I table (Table 2); every option has an Effort / Risk / Reuse / Files / Pros / Cons table |
| 3 No fabrication | PASS | The rating rubric (lines 25-30) is labelled as the synthesis's own method; every rating cites counted files, a named pin or a layer figure; I re-applied the rubric to A, B1, B2, B3, C, D1, D2, D3, E and found no inconsistency |
| 4 Evidence | PASS | |
| 5 At least 2 options with pros and cons | PASS | Options A to F each carry Pros and Cons rows; G, H, I are additional and flagged "lower research depth" |
| 6 Plan | N/A | |
| 7 Cross-references | PASS | Table 1 "Which reading of first use" row, the diagram at line 307 and the dependence table at line 360 agree with each other and with synth-04's branch table |
| 8 No doc-only claims in Sections 6 and 7 | PASS | Doc-only facts are marked `[UNVERIFIED - doc-only, no code confirmation]` (lines 21, 119, 158, 173, 188, 233, 266, 351) and rule 6.0 says they are never the only basis of an effort rating, a risk rating or the recommendation; the Feasibility statement rests on code lines (01 line 386, 03 lines 178-179) |
| 9 Stale docs surfaced | PASS | Six contradictions between research files listed at lines 292-299; stale documents are carried by synth-02 4.3 |
| 10 Key-finding coverage | PASS | Table at lines 378-389 maps each research file's strongest finding to a location; the R04 and R05 items were confirmed independently |

### synth-04-plan-questions-evidence.md (Sections 8, 9, 10; 474 lines)

| Check | Result | Evidence |
|---|---|---|
| 1 Headers | PASS | `## 8. Implementation Plan`, `## 9. Open Questions`, `## 10. Evidence Trail` |
| 2 Table structure | PASS | Plan tables are `Step \| Action \| Files \| Details`; Section 9 is `# \| Question \| Impact \| Suggested Resolution` |
| 3 No fabrication | PASS | Plan elements that are the author's own design are listed at line 464 (FIRST_USE condition 5, Variant H default, single block, helper, `test-80` name, no pre-approval, no removal) |
| 4 Evidence | PASS | |
| 5 Options | N/A | |
| 6 Specific steps with file paths | PASS | Phases 1 to 7 name files, lines and assertions; Phase 4 has exactly one branch per owner answer; the combination "no stub + slash skill" is explicitly BLOCKED (line 136) rather than papered over |
| 7 Cross-references | PASS* | Gap-to-step map (lines 23-34) covers F-01 to F-11; register 9.1 covers all 27 open gaps; F-03 mapping is thin (OBS-1) |
| 8 No doc-only claims in Section 8 | PASS | Every Claude Code dependent step (3.5 f, 3.6, 4B.3, 4B.4, 4D.3, 4D.4, 4D.6) is tagged doc-only and sits behind the "Gate before any branch" (line 140) |
| 9 Stale docs surfaced | PASS | The document register (lines 81-109) carries each stale document with a decision |
| 10 Key-finding coverage | PASS | R02 to R05 Key Takeaways and W01 and W02 recommendations land in Phases 1 to 7 and Section 9 (table at lines 451-460) |

## Section B. Tracing table (40 distinct claims)

R01 to R05 = research files 01 to 05; W01, W02 = web-01, web-02; RN = research-notes.md; GL = gaps-and-questions.md. "Code" in the research column means I also re-read the product or package file named, after tracing it to the research line. Synth lines are the line numbers in the synth file as read in this session.

| # | Claim | Synth file and section | Research file and line | Verified |
|---|---|---|---|---|
| 1 | `global_target_dir`: 43 occurrences in one file, comments at lines 9 and 12, 41 value lines; no reader | synth-01 2.1 (l.57); synth-03 Option F | R01:75; RN:206; Code: Grep of the installed package returns 43 in `platform-codes.yaml` only | yes |
| 2 | `ancestor_conflict_check` has a reader (`_config-driven.js:191`) but no platform sets the key (`platform-codes.yaml:10` is a comment) | synth-01 2.1 (l.58); synth-02 F-11 | R03:289; Code: Grep shows reader at :191/:943, comment at yaml:10 | yes |
| 3 | `resolve_config.py` exits 1 with "required config file not found" when `_bmad/config.toml` is absent | synth-01 2.1 (l.65); synth-03 fact 2 | R01 Summary (R01:386); Code: `resolve_config.py:48-51,143-163` | yes |
| 4 | `resolve_customization.py` `find_project_root` stops at `_bmad` OR `.git` | synth-01 2.1 (l.66); synth-04 step 3.2 | R03:288; Code: `resolve_customization.py:58-66` | yes |
| 5 | 39 of 46 SKILL.md reference the two scripts (52 matches); 37 load `config.yaml` | synth-01 2.1 (l.69) | R01:282-283 | yes |
| 6 | 41 `python3 ` lines in 31 SKILL.md (38 + 2 + 1); 25 of 31 have "If the script fails" | synth-01 2.3 (l.228); synth-04 row 14 | R03:255-261, 269 | yes |
| 7 | The six files with no written fallback | synth-01 2.3 (l.228); synth-04 row 14 | R03:270, 353 | names yes; derivation wording no (MINOR-1) |
| 8 | `~/.claude/skills` has 42 entries, no `bmad-*`; extras over the 39 packaged names are exactly `computer-use`, `orca-cli`, `orchestration` | synth-01 2.3 (l.224) | R03:94-97 | yes |
| 9 | `settings.json` 54505 bytes, 15 hook event types; `~/.claude/hooks/` 14 files | synth-01 2.3 (l.224) | R03:99-104 (I counted the 15 events at R03:102) | yes |
| 10 | 22 `settings.json.bak*` files versus 21 stamped backups, difference unexplained | synth-01 2.3 (l.226) | R03:92, 151 | yes |
| 11 | CI `cold bmad` 374 ms (run 42384399575), 392 ms (42369600288), 392 ms (42346410588); memlog "about 4s" is a different configuration | synth-01 2.1 (l.87); synth-02 SC-09, G-09 | R01:444-446, 449, 487 | yes |
| 12 | `Sysbox image layers: 68 (budget: 70)` on runs 42346410588 (sha f1ac0c93 = worktree HEAD) and 42384399575; dind-sidecar job only | synth-01 2.2 (l.159); synth-03 fact 9 | R02:399-400; Code: gate at `coder-ci-aidev02-contract.yml:1024-1027` | yes |
| 13 | `Dockerfile.coder:468` "no headroom" is [CODE-CONTRADICTED] as a measurement; `:229` "two spare" matches | synth-01 2.2 (l.160); synth-02 CC-13 | R02:412, 450; Code: Dockerfile lines 229, 468 | yes |
| 14 | `bmad` is a two-line wrapper; pin at `Dockerfile.coder:139`, wrapper write at `:142`, root layer 136-145 | synth-01 2.2 (l.113-114) | R02 section 1; Code: `Dockerfile.coder:133-145` | yes |
| 15 | `install.sh` guard 1 (:21-23), guard 2 (:24-25), excludes (:28-34), snapshot (:38,48-53), the only install call (:42), manifest check (:46), marker (:58-61), comment at :41 | synth-01 2.2 (l.124-135) | R02 section 2; RN:176; Code: `install.sh:1-61` read in full | yes |
| 16 | Welcome text at `manifest.yaml:12-14` names the manual command; manifest has 29 lines; scope hybrid line 3 | synth-01 2.2 (l.143-146) | R02 section 4; GL:51; Code: `manifest.yaml` read in full | yes |
| 17 | `bmad` is in profile `orca` only; `minimal` = `[claude-code]` | synth-01 2.2 (l.148); synth-03 fact 10 | R02 4.4; Code: `profiles.yaml:13-21` | yes |
| 18 | `spec2_health_observed bmad` reads only `seed-repo-path`; states recomputed once per agent start | synth-01 2.2 (l.163); synth-03 fact 6 | R02 section 5; Code: `spec2-health.sh:99-114`, `startup.sh:1187` | yes |
| 19 | `test-57:450` "no seed: bmad writes nothing" compares `snap` of the whole HOME (`:148-153`), excluding only `*/.git/index` and `./.aidev/installed/*` | synth-01 2.4 (l.272-278) | R04 section 1, Summary (R04:269); Code: `test-57:148-153, 446-452` | yes |
| 20 | All five tests run in `coder-ci-aidev02-contract.yml`; driver rows 1234, 1237, 1240, 1241 (`--network=none,--user=0`); test-52 runner-native at 832-847; cron `17 5 * * *` | synth-01 2.4 (l.270); synth-04 6.1 | R04:209-217; Code: workflow grep | yes |
| 21 | `test-73` allows a second drop-in only with its own COPY line and no `cleanupPeriodDays` | synth-01 2.4; synth-03 D2; synth-04 4D.6 | R04 A.6; Code: `test-73:78-114` (`copy_ok`, `tier_ok`) | yes |
| 22 | `test-19` classifier flags an unquoted install verb (`npm install`, `npx`, `pip install`, ...) after stripping quotes and comments; `command -v` plus `exit 2` = IMAGE_BAKED | synth-01 2.4; synth-03 B1 cons | R04 section 4; Code: `test-19:192-220` | yes |
| 23 | `bmad` slug runs without the 30 s bound (`startup.sh:1174-1176`); its marker is exempt from deselection removal (`:1116-1118`) | synth-01 2.2/2.3 | R02 section 2; R05 (d10); Code: `startup.sh:1108-1182` | yes |
| 24 | `block-bare-python.sh` packaged by superclaude (`install_hooks.py:85`), exits 2 on `python3`; 14 managed hook names | synth-01 2.3; synth-04 4D.2 | R03:250-254; Code: `install_hooks.py:42-87` (13 + 1 legacy = 14) | yes |
| 25 | Prior positions: overridden R1, R2, R4, R5, R6, R8, R9, R10, R12; not overridden R3, R7, R15, R16 | synth-03 7 (l.337); synth-04 step 1.7 | RN:186-201, 232 | yes (R11, R13 not classified, MINOR-6) |
| 26 | GL totals: 30 gaps (27 open, 3 resolved), 89 UNVERIFIED (79 open, 10 closed), 30 CODE-CONTRADICTED, 13 STALE DOC, 15 run-only facts | synth-04 9.1 (l.364, 396); synth-02 4.5 | GL:55, 190, 315-318; I re-summed the ids per gap in the 9.1 register: 79 | yes |
| 27 | Severity roll-up 4.1 = 1/10/0, 4.2 = 0/15/15, 4.3 = 0/6/20 | synth-02 4.5 (l.212-218) | GL:24-53 (Important: G-01 to G-10, G-13, G-16, G-19, G-24, G-26); 4.3 table counted (26 rows) | yes |
| 28 | A top-level `.claude/skills/` that did not exist at session start is not watched; needs `/reload-skills` | synth-02 W01-3; synth-03 Option D step 7; synth-04 3.5(f), 4B.4 | W01:34, 205 | yes |
| 29 | Hook `timeout` defaults 600 s (command), 30 s on UserPromptSubmit; SessionStart runs in background but first response waits | synth-02 W01-10; synth-03 D step 7 | W01:93-94, 103 | yes |
| 30 | SessionStart may return `reloadSkills`; v2.1.152 only from a user-authored issue; `claude --version` 2.1.319 was observed in the agent's workspace | synth-02 W01-11, W01-12; synth-04 4D.3 | W01:99-102, 115-116 | yes |
| 31 | `bmad-method` 6.12.4 latest (2026-10-14); 6.9.0 on 2026-06-22; `global_target_dir` hits 43 / 43 / 46 in 6.9.0 / 6.10.0 / 6.12.4 | synth-02 W02-1, W02-2; synth-03 F | W02:28-35, 48-54, 104 | yes |
| 32 | Release-note quotes #3064, #2671, #3016, `uv` advisory | synth-02 W02-6 | W02:111-116, 121 | yes |
| 33 | `CHANGELOG.md`: `## [Unreleased]` line 20, `### Changed` 58, `### Added` 285 (all inside Unreleased; next release at 415) | synth-04 step 2.6 | R05:164; Code: CHANGELOG headings | yes |
| 34 | `README.md:241` Default-profile row (five cells); `README.md:100` anchor "upstream GitHub CLI release v" | synth-04 steps 2.1, 2.2 | R05 (e):202, 206; Code: README grep | yes |
| 35 | `orca_retirement` at `modules.tf:82-109`; first `locals {` at :16; `test-52:1374-1377` pin splits at `'\n}\n'` so a separate later resource is safe | synth-04 4B.1, 5.2 | R04 A.5, A.11; Code: `modules.tf:1-109`, `test-52:1343,1374-1384` | yes |
| 36 | markdownlint ignores and relaxed rules; `templates/VSCode-AIDev02/README.md` is linted | synth-04 step 2.7 | R05 (e):207-209; Code: `.markdownlint-cli2.yaml:9-82`; `markdownlint.yml` (job `markdownlint scan`, small runner, 5 min, `fix: false`) | yes |
| 37 | Renovate extraction sites `expected.txt:6-8`; patterns at `renovate-global.json5:48` and `:54-55` | synth-04 doc register (l.105-106) | R05 (f):225-229; Code: both files | yes (step 2.5 misattribution, MINOR-5) |
| 38 | `test-startup-boot.sh:232` allows ledger kind `coder_script`; the only `coder_script` PARITY row is for vibe-kanban (`:2467-2469`) | synth-04 step 5.5 | R04 A.4; Code: `test-startup-boot.sh:229-232, 2466-2473` | yes |
| 39 | `--yes` on an installed tree defaults to quick-update; on a non-installed `_bmad/` it defaults to `update` | synth-01 2.1 (l.79-83) correct; synth-02 F-04 and synth-03 fact 11 broader | R01:463-468; Code: `ui.js:226-262`, `existing-install.js:45-117` | synth-01 yes; synth-02/03 wording broad (MINOR-4) |
| 40 | Image tag hashes `Dockerfile.coder`, listed COPY sources and `catalogue/**`; build context `image/`; root `.tf` not hashed | synth-01 2.2 (l.155-156) | R02 section 6.0; Code: `main.tf:73-74, 80-107, 119` | yes |

## Section C. Findings

No CRITICAL and no IMPORTANT finding. Every finding below is MINOR (wording, citation, a closable UNVERIFIED item, or a moved or misattributed reference on a claim whose substance is true). Each gives the location and a specific fix.

| ID | Severity | File and location | Issue (evidence) | Fix |
|---|---|---|---|---|
| MINOR-1 | MINOR | synth-01 line 228 | Says the six no-fallback files are listed with "the last three of those derived by subtraction". R03:270 says all six were derived by subtracting the 25-file list from the 31-file list; `bmad-create-prd` (and `bmad-advanced-elicitation` line 41) were additionally read, and R03:353 names the four never read as `bmad-customize`, `bmad-validate-prd`, `bmad-create-architecture`, `bmad-edit-prd`. | Reword: "the six were derived by subtraction; only `bmad-create-prd` and `bmad-advanced-elicitation` were also read". Same fix in synth-04 row 14 if it repeats the claim. |
| MINOR-2 | MINOR | synth-01 line 246 | "the prompting rule is doc-sourced (see section 2.5 and web research files, outside this file)". Section 2.5 is the document and decision trail and holds no prompting rule; the rule is in R03:312 and in synth-02 W01-6. | Replace "see section 2.5" with "see R03 A3 shared facts and synth-02 Section 5.1 (W01-6)". |
| MINOR-3 | MINOR | synth-04 line 9 | Lists "`###` headings at lines 20, 22, 58, 225, 285"; line 20 is `## [Unreleased]`, a `##` heading (CHANGELOG grep). | "lines 22, 58, 225, 285 and the `## [Unreleased]` heading at line 20". |
| MINOR-4 | MINOR | synth-02 line 110 (F-04) and synth-03 line 46 (common fact 11) | "any existing `_bmad/` (even a bare `_bmad/core/`) sends `--yes` to quick-update" and "If `_bmad/` exists (even a half-written one), `--yes` takes quick-update". `existing-install.js:111` makes a tree "installed" only with `core/`, a listed module or a readable manifest; an empty `_bmad/` is not installed, so `ui.js:233-262` offers only `update` and `--yes` selects `update`. R01:465 states this correctly ("an installed tree defaults to quick-update, otherwise to update") and so does synth-01 lines 79-83. The conclusion (FIRST_USE must refuse any `_bmad/`) is unchanged. | Say "an installed tree (has `core/`, a module or a manifest) takes quick-update; a bare `_bmad/` takes `update`; both rewrite an existing tree without a version test". |
| MINOR-5 | MINOR | synth-04 step 2.5 (line 65) | "the Renovate row `expected.txt:8` reads `^version: 6.9.0$`". `expected.txt:8` is a tab-separated expectation row (`IronbellyOrg/Coder  bmad-method  .../manifest.yaml`); the regex is `(?m)^version: (?<currentValue>\d+\.\d+\.\d+)$` at `renovate-global.json5:55` (R05:227). synth-03 line 77 uses the same loose pointer. | Cite "`renovate-global.json5:55` pattern `^version: <x.y.z>$`, expected by `expected.txt:8`". |
| MINOR-6 | MINOR | synth-03 line 337; synth-04 step 1.7 | The overridden / not-overridden lists omit RN F9-3 R11 ("MUST NOT change test-57 and test-startup-boot"), which RN:196 re-characterizes as "must not break unless the option deliberately changes boot, not must not change", and R13 (answered, RN:198). RN's own F9 Summary (RN:232) omits them too, so the omission is inherited. R11 matters because step 5.6 edits a comment in `test-57`. | Add one line to step 1.7: "R11 narrowed (the oracle stays correct for boot; step 5.6 edits a comment only); R13 answered by F9-4; R14 out of scope". |
| MINOR-7 | MINOR | synth-04 table 5.1 line 213 and register 9.1 (G-20, UV-63) | "`IDE_CONVERGENCE_TIMEOUT_S`, value not read". `test-startup-boot.sh:1412` reads `IDE_CONVERGENCE_TIMEOUT_S="${IDE_CONVERGENCE_TIMEOUT_S:-120}"`, so the default is 120 s and the item is closable by reading. | State "default 120 s (`test-startup-boot.sh:1412`); whether CI overrides it is UNVERIFIED" and trim UV-63 to the override question. |
| MINOR-8 | MINOR | synth-04 step 6.1 (line 246) | The contract-gate row names five tests only, while Table 5.1 requires `test-1`, `test-3`, `test-7`, `test-51`, `test-60`, `test-67`, `test-73-claude-retention` to stay green. They run in the same workflow: `test-51` at `coder-ci-aidev02-contract.yml:737-744` (and `coder-ci-validate.yml:49-51`), `test-67` at :774, `test-1/3/7/60/73-claude-retention` in the driver table at :1334-1370. The deliverable "names every pinned test" is met by Table 5.1; only the workflow mapping is thin. | Add one sentence to 6.1: those seven run in the same job (lines above) and `test-51` also runs pre-live in `coder-ci-validate.yml`. |

## Section D. Observations (not findings; no defect in the synthesis as written)

- **OBS-1 (F-03 mapping).** synth-04 maps F-03 ("skills copied without `_bmad/` do not work and nothing says so") to Phase 3 step 3.1 and Phase 4. The mechanism never creates that state, but a project that already has `.claude/skills/bmad-*` and no `_bmad/` is outside FIRST_USE (condition 3) and outside the broken-install message of step 3.3 (which needs `_bmad/` to exist). The state is recorded only as UV-55 (G-21) in register 9.1. Suggest one sentence in step 3.3 naming it as a second "broken install" case that is reported and not written to.
- **OBS-2 (Terraform heredoc).** Branches 4B and 4D (D3) embed the Phase 3 block in a `coder_script` heredoc. `modules.tf:87-108` is a Terraform heredoc in which `${...}` is interpolation (line 91 uses it deliberately), so a shell block using `${HOME}` or `${var}` must be written `$${...}`. Plan steps 4B.2 and 5.3 (extract the shipped text and run it) do not mention this; it is an implementer hazard, not a research claim.
- **OBS-3 (partial reads disclosed).** synth-04 self-audit (lines 443-445) says synth-01 sections 2.3 to 2.6, most of R01 and R02, `research-notes.md` and the `qa/` files were not opened by that author. I verified every dependent claim of those parts that I could reach (Section B rows 1 to 25) and found no error attributable to the partial reads.

## Self-Audit

**What I actively read (all in this session).**
- Synthesis, all four files in full: synth-01 (lines 1-521), synth-02 (1-466), synth-03 (1-397), synth-04 (1-474), including each file's own self-audit block.
- Research and QA inputs: `gaps-and-questions.md` (1-321 in full); `research-notes.md` lines 170-233 (F9-3 R1 to R16, F9-4, F9-5, F9 Summary); `BUILD-REQUEST.md` lines 10-21; R01 lines 328-342, 380-387, 432-470, plus Grep passes over the whole file for the counts (39/46, 52, 37, 43, 47, 577, 237, 374/392 ms); R02 lines 318-387 and Grep over 399-450 (layer gate, C8); R03 lines 90-110, 236-324 (Summary, A1, A2, A3 shared facts) and Grep for 330/331/353; R04 lines 205-270 (workflow mapping, Gaps, Stale Docs, Summary) and Grep for the A.1 counts; R05 lines 136-235 (b Key Takeaways, c, d, e, f) and Grep for the line-156 issue-folder row; web-01 lines 88-118, 158-163 and Grep for every cited phrase (Enterprise over personal, reloadSkills, 600 s, 2.1.152, 2.1.319, trust hold-back, managed keys); web-02 lines 44-66, 100-128 and Grep for every cited date, hit count and issue number.
- Product and package files re-read to confirm cited line numbers and statements: `catalogue/bmad/install.sh` (1-61), `catalogue/bmad/manifest.yaml` (1-29), `profiles.yaml`, `modules.tf` (1-113), `main.tf` (68-123, Grep for volumes), `Dockerfile.coder` (130-147, COPY/RUN Grep), `startup.sh` (1108-1192 and section-marker Grep), `spec2-health.sh` (84-120), `test-57` (120-159, 440-465), `test-52` (1343, 1366-1389), `test-73` (60-139), `test-60` (78-97), `test-19` (190-224), `test-startup-boot.sh` (229-232, 1412, 1962-1980, 2440-2485), `test-71`, `test-3` (RESERVED), `coder-ci-aidev02-contract.yml` (Grep of triggers, job, gate, driver rows), `coder-ci-validate.yml`/`coder-ci-orca-boot.yml` (Grep), `markdownlint.yml`, `.markdownlint-cli2.yaml` (1-83), `CHANGELOG.md` (heading Grep), `README.md` (Grep for 100 and 241), `renovate-global.json5` (42-61), `expected.txt` (Grep), installed bmad package (`install.js` options, `ui.js` 210-269, `existing-install.js` 40-122, `installer.js` 1214-1247 and 1544-1556, `install-paths.js` 8-44, `resolve_config.py`, `resolve_customization.py`, whole-package Grep for `global_target_dir`, `ancestor_conflict_check`, `semver.`), and superclaude `install_hooks.py` 38-93.

**Searches and recounts I ran.** Whole-package Grep of `global_target_dir` (43, one file); Grep of `semver.` over `tools/installer` (no hit in `core/installer.js`); Grep of workflows for which tests run where; Grep of `IDE_CONVERGENCE_TIMEOUT_S`; recount of GL severity classes (4.2: 15 Important, 15 Minor), of the 26 grouped 4.3 rows (6 Important, 20 Minor), of the ids in register 9.1 (79 open UNVERIFIED across 27 open gaps), of the CC/SD id coverage (all 30 and 13 present once), of the hook event types (15) and of the managed hook names (13 + 1 = 14); re-application of the effort and risk rubric to ten option variants.

**Why I believe the finding count is right.** The synthesis is almost entirely a re-expression of research lines that carry their own tags, and it quotes line numbers. I did not take those on trust: 40 distinct claims were traced to research lines, and for 30 of them I also re-read the product or package source. All 40 are substantively true. The defects I found are all precision defects (one wrong derivation note, one wrong cross-reference, one hidden `##` versus `###`, one over-broad installer statement, one misplaced Renovate pointer, two unclassified prior positions, one closable UNVERIFIED value, one thin workflow mapping). None changes a rating, a plan step, a pinned-test verdict or the recommendation. I looked specifically for fabricated numbers, doc-only claims presented as facts in Sections 2, 6, 7 and 8, inconsistent counts across the four files, option ratings that contradict the stated rubric, gaps missing from Sections 8 or 9, and Key Takeaways with no landing place, and found none. A zero-blocking verdict is therefore evidence-backed, not a default.

**Limits.** I did not run any test, any `bmad` command, or any workflow, and no Claude Code behaviour was observed; every statement about those stays as UNVERIFIED as the synthesis says it is. I did not open R01 lines 1-327 and 343-379, R02 lines 1-317, R03 lines 1-89 and 110-235, R04 lines 1-204 and 271-541, or R05 lines 1-135 and 236-417 in full; for those ranges I relied on Grep and on the synth text being consistent with the parts I did read, so an error confined to an unread research range that the synthesis copied faithfully would not be seen here. Web claims were traced to the web files only; I did not re-fetch any URL.

## Summary

**Status:** Complete

| Severity | Count |
|---|---|
| CRITICAL | 0 |
| IMPORTANT | 0 |
| MINOR | 8 (MINOR-1 to MINOR-8) |
| Observations (not findings) | 3 (OBS-1 to OBS-3) |

Checks 1 to 10 pass for all four synth files (Section A). 40 claims traced, 40 substantively verified (Section B). The STOP-AND-RE-SCOPE branch does not apply: synth-03 states the stop condition is not triggered, so Section 8 was judged as an implementation plan and found specific, file-level, and consistent with Sections 4, 7 and 9.

**VERDICT: PASS** (no blocking finding; the eight MINOR findings are notes with fixes given in Section C).
