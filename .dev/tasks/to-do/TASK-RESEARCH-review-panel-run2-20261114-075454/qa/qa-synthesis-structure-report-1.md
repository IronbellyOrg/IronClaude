# QA Report - Synthesis Gate, structure lens (partition A)

**Topic:** which ONE unified central Review Panel (shared core plus thin modules) captures all the value of E1, E2 and E3
**Date:** 2026-11-14
**Phase:** synthesis-gate (structure lens, checklist items 1-6)
**Fix cycle:** N/A (review 1)
**Files reviewed:** synth-01-problem-current-state.md, synth-02-overlap-matrix.md, synth-03-target-gaps.md, synth-04-external-findings.md (all under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/synthesis/`)
**Fix authorization:** false (report only)
**Grading:** grading override in `qa/grading-override.md` applies (blocking only if a decision/number rests on it, a required deliverable/section missing, or security/data-loss/safety risk)

Status: Complete (verdict PASS, 0 blocking, 7 minor notes; details in sections 4 and 6)

---

## 1. Method and coverage

**Partition note.** [PARTITION NOTE: Cross-file checks limited to the four assigned files. Full cross-file verification against synth-05 to synth-10 needs the merged partition reports.]

- All four assigned files were read completely (synth-01 749 lines in 4 reads, synth-02 284 lines in 2 reads, synth-03 406 lines in 7 reads, synth-04 607 lines in 3 reads). No reviewed file was modified.
- Grading: every finding was graded with `qa/grading-override.md` (blocking only for a decision-bearing wrong or unsupported fact, a missing required deliverable or section, or a security, data-loss or safety risk). The CRITICAL / IMPORTANT / MINOR label is information only.
- Independence: no read, list or grep touched the run-1 task folder or the queued run-2 file; `.dev/tasks/` was excluded from repo-wide searches (only this task's own folder was read). E2 content was read only through `git show` / `git cat-file` at `6c0984326cbb8fb06c4a36065de58b171d3f8175`.
- Table-structure check was a script over every markdown table (count of unescaped `|` per row against the header row), run with `uv run python` from a temporary file that was deleted afterwards.

---

## 2. Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match the report structure (Section 1; 2.1-2.8; 2.9; 3; 4; 5 with 5.1-5.5) | PASS (notes F-5) | Grep of `^#{1,6} ` over the four files: synth-01 has `## 1. Problem Statement` and `### 2.1` to `### 2.8`; synth-02 has `## 2.9 Overlap Matrix` with `### 2.9.0` to `### 2.9.10`; synth-03 has `## Section 3: Target State` (3.1-3.5) and `## Section 4: Gap Analysis` (4.1-4.6); synth-04 has `## 5. External Research Findings` with `### 5.1` to `### 5.5`. Only the heading style of synth-03 differs (F-5). The `## Synthesis notes (not report sections ...)` block in synth-01 is labelled as non-report. |
| 2 | Table column structures are correct (gap table Gap / Current State / Target State / Severity / Notes; overlap matrix; external finding blocks) | PASS on column design; 2 shape notes (F-1) | synth-03 line 101-103: header `Gap \| Current State \| Target State \| Severity \| Notes`; 148 unique gap rows (grep + unique count), severity cell filled in 148 of 148 (24 Critical, 93 Important, 31 Minor, matching the stated counts). synth-02 matrix header `# \| Capability \| E1 \| E2 \| E3 \| Classification \| Evidence tag \| Notes`, 16 rows, all 16 tables pass the pipe-count script. synth-04: every finding block carries `Finding / Source / Relevance / Relationship to codebase`, all 9 tables pass the script. The script found 18 rows with unescaped `\|` inside cells (synth-01 5, synth-03 13): F-1. |
| 3 | No fabrication: at least 15 claims per file traced to research files or code | PASS | Section 3 below: 24 claims traced for synth-01, 22 for synth-02, 26 for synth-03, 24 for synth-04, each against a named research file and, where it is code, against the code at HEAD or at the E2 tip. Zero fabricated claims. Three imprecise statements found (F-2, F-3, F-4). |
| 4 | Evidence citations use actual file paths (verified with Glob, `git ls-tree`, `git cat-file`, `git show`) | PASS | One batch script checked 110 HEAD paths (0 missing), 20 E2-tip paths via `git cat-file -e 6c0984326...:path` (0 missing), 6 commit ids (all exist), a second batch of 52 more paths (2 not found only because the check guessed the wrong directory; Glob found `tests/skills/test_model_alias_policy.py`, `tests/skills/test_workflow_archive.py` and `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`, so the citation is valid but names no directory: F-7). |
| 5 | Where options appear there are at least two with pros and cons | PASS with note (F-6) | synth-01, synth-02 and synth-04 contain no options analysis (synth-04 lists source-stated recommendations, each marked "not adopted here"). synth-03 names options only inside gap rows: G-105 (mirror, import or keep two registries) and G-125 (O1/O2/O3); both give two or more options, neither gives pros and cons. The options section belongs to synth-05, outside this partition. |
| 6 | Any step or input list is specific (file paths), not generic | PASS | synth-03 Section 3.3 has 33 success criteria, each with a "How it is checked" cell naming a probe, test file and line, or research row; Section 4 Notes cells carry research row ids; synth-01 and synth-02 "Evidence:" lines list file:line paths, all spot-checked (Section 3). No generic step ("create a service") exists in the four files. |
| G1 | Gate focus: report-only scope (no roadmap, branch plan, PR plan, risk register) | PASS with note (F-6) | Grep of synth-03 for `roadmap|risk register|PR plan|branch plan|Phase [0-9]|milestone|timeline|sprint` hit only two rows that use "roadmap" as a name (K-1 consumer list, G-86 `Stage 7 roadmap validation`). K-8 states the ref fact "no branch layout is proposed here". synth-04 5.3.2 and 5.3.5 repeat web-03 branch-naming rules, each labelled external and "not adopted here" (5.5 coverage preamble). Wording "first step" in T-5(f) and "first shape" in G-106 is sequencing language (F-6). |
| G2 | Gate focus: no doc-only claim presented as current | PASS | Every `[UNVERIFIED]` claim is tagged in place and listed in a "Not verified" block (synth-01 per subsection; synth-02 2.9.8 OQ-01 to OQ-18; synth-03 4.6.B U-1 to U-18; synth-04 states in the section preamble that quoted codebase facts were handed in and not verified). The two inference statements (plugin install ends `skipped`, 2.7 and G-88/U-16) are labelled "inference, not executed". |
| G3 | Gate focus: every [CODE-CONTRADICTED] finding surfaced | PASS | Sampled the `[CODE-CONTRADICTED]` lines of R06 (15), R18 (8), R17 (14), R16 (6), R14 (7): each appears as a "Corrections" bullet in synth-01, a row in synth-02 Table E2 (CC-1 to CC-11), or a stale-documentation row in synth-03 (G-34, G-35, G-53, G-62, G-69, G-74, G-83, G-89, G-98, G-107, G-113, G-122, G-131, G-145, G-148), for example 159 vs 179 test functions (G-145), "no error" (G-64), `.claude/` tracked files (G-148, verified: `git ls-files .claude` prints two files). SC-33 and 4.6.C name all 15 clusters. |
| G4 | Gate focus: `[PENDING-ADJUDICATION: <slug>]` allowed in synth-07 only | PASS | Grep for `PENDING-ADJUDICATION` over synth-01 to synth-04: 0 matches. |

---

## 3. Claim-tracing log (checklist item 3 and 4)

Each row: claim in the synthesis file, then where it was confirmed. All rows confirmed unless marked.

### 3.1 synth-01-problem-current-state.md (24 claims traced)

| # | Claim in synth-01 | Confirmed against |
|---|---|---|
| 1 | #519 = `d2d8a2d16...`, 2026-11-12 14:47:10 -0500, 17 files under `cli/review` (4 modified, 13 added), 22 under `tests/review` | `git log -1`, `git diff-tree --name-status` (A 13, M 4; 22 test files); R01 line 26 |
| 2 | #518 changes 0 `cli/review` files and 1 test file | `git diff-tree ... -- src/superclaude/cli/review tests/review` prints only `tests/review/test_review_panel_live7.py` |
| 3 | E2: four commits after `4a22d7421`, 2026-11-13 16:17:36 to 2026-11-14 04:38:11 UTC, 0 files under `src` / `tests` per commit | `git log 4a22d7421..6c0984326...`; `git diff-tree` per commit = 0 |
| 4 | `findings.py` and `ledger.py` byte-identical to the E2 tip | `git diff --quiet 6c0984326 HEAD -- <file>` both identical |
| 5 | `cli/review`: 25 tracked files, 16 modules, 5,086 lines, 19 test files, 8 panel templates + tier file | `wc -l` total 5086; `ls`; R18 line 199 |
| 6 | `test_verdict_mapping.py` has 36 tests; threshold tests pin 0.75 degrades and 0.80 passes | `grep -c 'def test_'` = 36; test lines 430-460 |
| 7 | `panel.py:72-73, 80, 137, 500`; reflect launch refusal text | `_REFLECT_LAUNCH` at 72, `_REFLECT_MAX_REVIEWERS` at 73, defs at 80, 137, 500; message at 153-156 |
| 8 | `reflect_shadow_exit.py:313` empty baseline counts 0.0; `:59` card regex vs `panel_lint.py:188` | `grep -n`: line 313 `if (s_rate or 0.0) > (l_rate or 0.0)`, line 59 `^reviewer-(\d+)\.md$`, lint 188 `-card` form |
| 9 | Engine A: `ensemble.py:74, 773, 788, 817`; `runner.py:457-459, 480-481`; `config.py:318-319, 334-335`; `commands.py:236-239` | `grep -n` / `sed -n` at each line |
| 10 | `SKILL.md:87` rejects `panel`, `:703` carries 0.75, `:839` "warn-only in v1.0"; `contract.py:287-288, 310` | `sed -n`, `grep -n 0.75` (703 present), `contract.py` lines read |
| 11 | Stage 2 exit 13 of 20, EV-1 8/13 = 0.615 | R06 lines 13, 233; R07 line 23 |
| 12 | 4,119,747 output tokens, 489.2 min, USD 478.40, median 0.588, TP 21 / FP 4, 479/712 and 495/781 | R07 lines 15, 23-55; R15 line 114 |
| 13 | E2 tree counts: 96 directories, 97 entries, 19 / 29 `RESULT.md`, 319 `score.json*`, 9,312 files | `git ls-tree` (96, 19, 9312); R08 lines 39-41 |
| 14 | 306 catches / 106 runs, 194 of 214, 131 of 147, 65 vs 38, 156 of 665, 2,916 files / 1.48 GB | R08 lines 52, 117-120, 150-154, 183 |
| 15 | 92 dropped findings (30+33+14+7+7+1), 49 blocking (53%), 3 flips | R08 lines 70-85; arithmetic re-added |
| 16 | sha256 `044809e3a963...3338bd3481` of E1 input = E2 designSpec candidate | R16 lines 200, 222, 301; `.dev/tasks/done/TASK-WF-designSpec-20261107-075614/...md` exists |
| 17 | gaps-and-questions: 555 rows; by tag 243 / 187 / 67 / 58 | the log's own header; row count by `grep -c '^| GQ-'` = 555 (my per-row tag counts differ, 251 and 61, because one row can carry several tags; the header figure is what synth-01 quotes) |
| 18 | E3i scripts 2,668 / 2,050 / 1,740 / 1,131 lines (7,589 total), grader 35 lines, 5 `spec-panel-*` commands | `wc -l` on the installed files; `ls ~/.claude/commands/sc` |
| 19 | 1,047 citations, 510 flagged, 92.5% `not-in-snapshot`; 36 logged collaboration conflicts; T2bModel01 "18 lines in 11 files" | R10 lines 194; R09 lines 191, 223; R04 line 139 (my recount: 16 lines in 10 files tracked outside `.dev`, 22 / 16 including untracked mirrors; scope of the R04 count is not stated, not decision-bearing) |
| 20 | No `integration` ref; 40 of 47 local heads `ironbelly/`; 3 `origin/feat/` refs; 19 worktrees | `git for-each-ref`, `git branch -a --list '*integration*'` (only `346Claude-integration`, `346GPT-integration`), `git worktree list` |
| 21 | `git ls-files .claude` prints 2 files; Makefile:549 "6 of 10 checks"; no CODEOWNERS; `core.hooksPath` unset | `git ls-files`, `sed -n 549p`, `git config` |
| 22 | 148 matching lines in 56 files for `src/superclaude` in primitives; 25 lines in `sc-reflect-protocol` | `grep -rn --include='*.md'` = 148 / 56; 25 |
| 23 | Plugin: 4 skills, 125 tracked files, `spec-panel.md` differs by 18 lines, hard gate extended with `${CLAUDE_PLUGIN_ROOT}` | `ls`, `git ls-files`, `diff`, `sed -n 266p` |
| 24 | `pr_submit` 6,511 lines; `rf-qa.md` 551, `rf-qa-qualitative.md` 1154, `rf-analyst.md` 428; auggie skill 402 | `wc -l` |

### 3.2 synth-02-overlap-matrix.md (22 claims traced)

| # | Claim | Confirmed against |
|---|---|---|
| 1 | Table A: 11 + 1 + 0 + 2 + 2 + 0 = 16; conflicting rows 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13 | re-added from the matrix rows |
| 2 | Table B: ABSENT 2 + 6 + 4 = 12, own 14 + 7 + 12 = 33, reuse 3, total 48; 8 rows with no ABSENT cell | re-derived from the cell text of rows 1-16 |
| 3 | Table C: 13 + 3 = 16 | re-counted |
| 4 | 21 conflicts CF-01 to CF-21; 11 claims CC-1 to CC-11; 5 statements RC-1 to RC-5; 18 open items OQ-01 to OQ-18 | counted from the tables |
| 5 | `ensemble.py:773` count-derived `merge_method`, `:817` `citations_dropped: 0`, `:74` / `:788` version 1.0 | `grep -n` |
| 6 | `contract.py:321` degrades below 0.80; 36 tests | `grep`; `sed` |
| 7 | `fsm.py:32-33` and `loop_guard.py:19-20` define the pr-submit caps twice | `grep -nE` both files |
| 8 | `findings.py:14, 29, 101, 346-349`; `findings_v2.py:35, 96-97`; `cluster.py:50, 67, 72`; `telemetry.py:17, 23, 113` | `grep -n` |
| 9 | `ledger.py:37-38, 96, 107, 350, 363`; `panel.py:600` `apply_to` | `grep -n`; all 8 templates carry `"apply_to": ["first"]` |
| 10 | `__init__.py:24-25` registers `lint_cmd` and `estimate_cmd`; neither module exists | `grep -n`; `ls src/superclaude/cli/review` (16 `.py`, neither present) |
| 11 | Tier file 38 lines; live7 test `:92-98` compares counts and first model of tier2b / tier3; exclusion test `:208-213` "1 Sonnet + 6 Haiku" | `wc -l`, `sed -n` of both tests |
| 12 | CC-1: #518 changes 0 review files; CC-3: T2bModel01 5 lines in 4 `src` files, 5 lines in 3 `tests` files | `git diff-tree`; `git grep -- src` = 5 / 4, `-- tests` = 5 / 3 |
| 13 | CC-6: workflow `:89`, tasklist `:1630` call `/sc:reflect --mode pre` | `sed -n` of both files |
| 14 | CC-11 / R06: production Tier 2 is the swarm; docstring stale | `runner.py` lines 36, 517; R06 line 368 |
| 15 | E3i sizes, 35-line grader, 5 commands (2.9.0 effort table) | `wc -l`, `ls` |
| 16 | Plugin `spec-panel.md` 18 changed lines, hard gate extended | `diff`, `sed -n 266p` |
| 17 | E2 tree: 96 directories, 19 `RESULT.md`; py counts r1 27 and r5 14 | `git ls-tree`; R01 line 207 |
| 18 | r1 107 / r2 321 file counts; claimed vs static test counts 138 / 358 vs 103 / 163 | R09 lines 58, 71, 202 |
| 19 | r5 kit cost +59% (281.6 s vs 176.9 s) and +55% (46,018 vs 29,655) | R09 line 78 |
| 20 | Hook p95 73 and 81 ms, 57-85 ms | R09 line 185 |
| 21 | CF-06 `SKILL.md:703` vs `contract.py:321` and tasklist 0.80 | `grep`; tests at 430-460 |
| 22 | 7 unchained multi-reviewer clusters of 216 = 3.2% | R07; 7 / 216 = 3.24% |

### 3.3 synth-03-target-gaps.md (26 claims traced)

| # | Claim | Confirmed against |
|---|---|---|
| 1 | 148 gaps: 24 Critical, 93 Important, 31 Minor; 148 unique ids | `grep -E '^\| G-[0-9]+ '` then per-severity count and unique count; the 4.1 list of 24 Critical ids matches the Severity column |
| 2 | 33 success criteria; every "Closes" gap id exists | counted `^\| SC-`; each G id looked up |
| 3 | 4.6.C list of 15 stale clusters equals SC-33 list | compared by eye, identical |
| 4 | G-12 `ledger.py:254-258` clears by silence | `sed -n 254,258p` |
| 5 | G-64 `ledger.py:122-134` one warning per reviewer | `sed -n 122,134p` |
| 6 | G-01 `findings.py:349` `finding["anchor"]` | `sed -n 346,350p` (see F-2 for the mechanism) |
| 7 | G-22 / G-137 `__init__.py:24-25`; `channel_of`, `V1_FIELDS`, `COMPLETION_STATES`, `read_committed`, `reusable_stages` have no caller outside their files and tests | Grep over `src` and `scripts` |
| 8 | G-23 only caller of `append_record` is `telemetry_cmd.py:67` | Grep over `src` and `scripts` |
| 9 | G-51 `commands.py:236-239` vs `runner.py:457-459` | `sed`; `grep` |
| 10 | G-48 / G-128 exit-script `:313`, card regex `:59` vs `panel_lint.py:188` | `grep -n` |
| 11 | G-136 `select_env` reads `$T3Model01` only (`panel.py:485-494`), `date.today()` at `:623-628` | `grep -n` |
| 12 | G-142 25 `src/superclaude` lines in `sc-reflect-protocol` | `grep -rn | wc -l` = 25 |
| 13 | G-146 no CODEOWNERS, `core.hooksPath` unset | `git ls-files`, `git config` |
| 14 | G-125 / G-126 E2 evidence tree 9,312 files; none of the 4 harness scripts tracked at HEAD; `verify-run` absent | `git ls-tree` count; `git ls-files | grep`; `git grep` |
| 15 | G-148 `.claude` tracks 2 files; `Makefile:549`; no `integration` ref | `git ls-files .claude`; `sed -n 549p`; ref listing |
| 16 | G-92 pr-submit caps `2` / `5` defined twice | `grep` |
| 17 | G-88 / G-94 plugin has 4 skills; `spec-panel.md` 18 changed lines | `ls`; `diff` |
| 18 | G-43 the tasklist per-phase gate passes `--fix --no-promote`; docs say executor-disjoint | `grep` of `templates/phase-template.md` (lines 161-197) and `SKILL.md` (1141-1177) |
| 19 | G-21 / G-84 `SKILL.md:87`, `:309-311`; workflow `:89`; tasklist `:1630-1636` | `sed -n` |
| 20 | G-77 1,047 / 510 / 472; 110 of 275 (40.0%) + 400 of 772 (51.8%) = 510 of 1,047 | R10 line 194; arithmetic |
| 21 | G-63 / G-69 numbers (131 of 147; 417 tracked; 96 directories; 3 flips) | R08 lines 41, 50-52, 82; `git ls-tree` |
| 22 | K-2 `test_runner_e2e.py` has 10 tests | `grep -c 'def test_'` = 10 |
| 23 | K-8 ref collision facts and "no `feat/review-panel*` ref" | `git for-each-ref`: no `feat/review-panel*` ref, the 3 `origin/feat/` refs have other names; the scratch-repository reproduction is R18 section 3 and was not re-run here (not decision-bearing, the claim is stated as an observed fact with the git version) |
| 24 | G-12 / G-133 all 8 packaged templates `apply_to: ["first"]` | `grep -L` returned nothing; 8 files |
| 25 | G-145 / R17: 159 vs 179 test functions, fenced yaml lesson contradicted | R17 lines 164-166, 517-519 |
| 26 | X-5, X-6, X-8 stronger-side statements | R08 lines 70-85, R08 section 6, R13 line 270 |

### 3.4 synth-04-external-findings.md (24 claims traced)

| # | Claim | Confirmed against |
|---|---|---|
| 1-4 | SWR-Bench F1 +43.67%, 21.91% F1, +118.83% recall, 1,000 PRs | web-01 line 104 |
| 5 | GitHub ReviewBench 219 PRs, 96.6% agreement | web-01 line 112 |
| 6 | c-CRAB 20.1%-32.1%, 97 of 234 | web-01 line 128 |
| 7 | "Nine Judges": 1.93, 0.437 vs 0.389, 0.603, 9.1%, 8-22 points | web-01 line 77 |
| 8 | MT-Bench second-hand figures 65.0% and 91.3% | web-01 lines 23-24 |
| 9 | PoLL kappa 0.763 and Pearson 0.917 | web-01 line 61 |
| 10 | "Reliability without Validity" 541,000 judgments; alpha 0.33 | web-01 lines 143, 147 |
| 11 | Stacked PRs GA changelog 2026-10-06 | web-03 lines 64, 66, 74, 124, 145 |
| 12 | `gh stack` needs Git 2.36+ | web-03 line 98 |
| 13 | Graphite $20 / $40 per user per month | web-03 line 104 |
| 14 | HN thread 38844343, SO 45141188, Git 2.39.3 | web-03 line 27 |
| 15 | `--restricted` needs v2.1.248 | web-02 lines 124-125 |
| 16 | `CLAUDE_CODE_MAX_CONTEXT_TOKENS` from v2.1.193 | web-02 line 87 |
| 17 | Issue 79702 (v2.1.216), 10373, 37559 | web-02 lines 98-100, 133 |
| 18 | Issues 18311 and 22724 | web-02 line 102 |
| 19 | Greptile 66.2% vs Copilot 56.5% (vendor-reported) | web-04 line 100 |
| 20 | Codex issue 27691 | web-04 lines 105, 109 |
| 21 | `dismiss-alerts` action | web-04 lines 131-132 |
| 22 | Provenance table (provider=tavily, no fallback used) | web-01 line 6, web-02 line 6, web-03 line 5 and 162, web-04 line 6 and 195 |
| 23 | 5.5 coverage table has one row per web Key Finding and Recommendation, none excluded | counted the numbered items per web file (web-01 9 + 9, web-02 9 + 7, web-03 8 + 6, web-04 7 + 7 = 62) against the 62 rows at synth-04 lines 536-597 |
| 24 | Section preamble: web-03 defers to research item 2.18; no web file records a conflict with code | web-03 lines 2, 14, 23, 31, 49, 58, 152 ("takes precedence") |

---

## 4. Findings

Grading by `qa/grading-override.md`. Severity label is information only. "Blocking" is Y only when a decision, recommendation, value-inventory destination, conflict-log outcome or a number the recommendation rests on would be wrong or unsupported, a required deliverable or section is missing, or there is a security, data-loss or safety-boundary risk. None of the three holds for any finding below.

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| F-1 | IMPORTANT (label) | N | synth-03 lines 87 (K-3), 108 (G-04), 140 (G-36), 149 (G-45), 179 (G-75), 192 (G-88), 193 (G-89), 205 (G-101), 207 (G-103), 208 (G-104), 232 (G-128), 238 (G-134), 250 (G-146); synth-01 lines 182, 289, 564, 576, 635 | 18 table rows contain an unescaped `\|` inside a cell (inside a code span or a quoted list such as `full \| degraded`, `OK\|PROBLEM\|UNSURE`, `\|\| true`, `\|F\|=<n>`, a grep alternation). GitHub-flavoured markdown splits the cell at that pipe and ignores the cells beyond the header width, so when rendered, the Current State / Target State / Severity / Notes cells of those 12 gap rows (and the shorter cells of the 5 synth-01 rows and K-3) show text fragments instead of the intended values. The raw text is complete and the severity of G-36 is repeated in the 4.1 Critical list, so no cell a later phase reads changes meaning. (minor under grading override) | Script over every table: expected pipe count (header row) against the pipe count per row after removing `\\|`; synth-03 line 108 expects 6, has 13; line 250 expects 6, has 15; synth-01 line 635 expects 4, has 7. synth-02 (16 tables) and synth-04 (9 tables) pass. | In the 18 rows, write each inner pipe as the escaped form (backslash then pipe) or replace it with the word "or", before assembly. |
| F-2 | IMPORTANT (label) | N | synth-03 G-01 and G-99 (lines 105, 203) and SC-01 (line 47); synth-02 CF-03 (line 113) against synth-01 section 2.5 (the P-a paragraph) | The mechanism of probe P-a is stated two ways. G-01, G-99 and CF-03 say a v2 citation-only finding reaches `ledger.merge_round`, which calls `annotate`, which raises `KeyError: 'anchor'`. synth-01 2.5 says the opposite: `merge_round` parses with the v1 `parse_block`, which already requires an anchor, so a v2 block never reaches `annotate` through that path; the KeyError arises only when a v2-validated finding is passed to `annotate` directly. The code agrees with synth-01: `findings.py:126` looks for a `findings-v1` fence, `:139` returns "no fenced block with info string findings-v1", `ledger.py:129` calls `fnd.parse_block(rv["text"])`. The conclusion (location type blocks the ledger and merge path; G-01 Critical) holds under either mechanism, and SC-01's pass condition ("passes `merge_round` and enters the ledger") is still the right test. Only the failure description is imprecise. (minor under grading override) | `sed -n 346,350p` and `sed -n 124,160p` of `findings.py`; `sed -n 122,134p` of `ledger.py`; synth-01 line 442 text "mechanism refinement from Gate 1". | In G-01, G-99, CF-03 write: "a v2 report is refused by the v1 parser (no `findings-v1` block); `annotate` raises `KeyError` if called directly on a citation-only finding". Drop "without KeyError" from SC-01. |
| F-3 | IMPORTANT (label) | N | synth-01 line 32 (Section 1, "Trigger") | "E1: kernel #519 ... plus evidence commits `792cf8c52` and `50d4d2b9d` at HEAD". `792cf8c52` is the E1 evidence commit ("docs(reflect): shadow-run evidence, troubleshoot report and the 5x3 model-combination experiment"). `50d4d2b9d` is the HEAD commit whose subject is "docs(review-panel): tech-research run 1 report, research, synthesis, debates and QA for the unified Review Panel", that is output of the earlier run of this research program, not E1 evidence. No decision depends on the sentence, but a report that calls run-1 output E1 evidence blurs the independence rule of this task. (minor under grading override) | `git log -1 --format=%s 50d4d2b9d` and `792cf8c52`; the session git context lists both subjects. The research files use `50d4d2b9d` only as the HEAD baseline (R01 line 3, R06 line 10). The commit's files were not opened. | Remove `50d4d2b9d` from the E1 sentence; keep it in the Baseline line as the code baseline. |
| F-4 | IMPORTANT (label) | N | synth-01 section 2.5 table "Overlap matrix across E1, E2, E3s, E3i (R01 s4, 15 capabilities...)" against synth-02 section 2.9 | The 2.5 table keeps R01's labels "superset of E3s" for E1 in rows 1 (finding schema) and 4 (clustering) and numbers 15 capabilities, while 2.9 (the deliverable) classes those capabilities `conflicting`, states that E1 is not a strict superset (PS-1, PS-2, CF-13, RC-2) and numbers 16 rows. 2.5 has no pointer to 2.9. After assembly the report would show both. The correction is discoverable in 2.9, so no destination or conflict outcome rests on the stale label. (minor under grading override) | synth-01 lines 410-426 against synth-02 lines 43, 47, 148-149, 171, 277. | Add "(labels as in R01; corrected and extended in 2.9)" under the 2.5 table, or delete the table and keep the pointer to 2.9. |
| F-5 | MINOR | N | synth-03 lines 12, 99, 276, 315; synth-02 lines 166, 178 | Heading style differs (`## Section 3: Target State` against `## 1.`, `## 5.`); report-facing sub-titles name task-internal rules ("Rule C8 check", "(rule 9)"; the severity rubric note says "task's rule C8"); 2.9.7 tables are called "Table E1" and "Table E2", which collide with the effort names E1 and E2. | Grep of headings (Items Reviewed #1). | Normalise headings at assembly; describe rule C8 in words ("in-scope capability that is named as shipped but not wired"). |
| F-6 | MINOR | N | synth-03 T-5(f) (line 24), G-70 (line 174), G-105 (line 209), G-106 (line 210), G-125 (line 229) | Section 3 says "no sequencing", but T-5(f) says "first step at the /task phase gate", G-106 "out of the first shape", G-70 "no hook transport built into the core until an arm beats the static kit". They restate R13 s8 and the same item is carried as open decision D-9 in 4.6.A, so it is not a roadmap and is not presented as decided. G-105 gives three options and G-125 "O1/O2/O3" (only two are named in its Target cell) without pros and cons; the options analysis belongs to synth-05. | Reading of the rows; 4.6.A row D-9. | Word as "candidate first target (decision D-9)"; name O3 in G-125; leave pros and cons to synth-05. |
| F-7 | MINOR | N | synth-01 2.6 (`test_model_alias_policy.py:227`, `test_workflow_archive.py:799`), synth-03 G-43 and G-53 (`phase-template.md:156-182`), synth-02 header line 5 and row 6 / row 11, synth-04 5.3.2 C1 Source, synth-01 2.5 and 2.3 | Citation format only: (a) three cited files are named without a directory (they exist under `tests/skills/` and `src/superclaude/skills/sc-tasklist-protocol/templates/`); (b) synth-02 lists R01, R04, R06, R09, R11, R12 as sources but row 6 cites R16 (91.4% anchor fidelity) and row 11 cites the redesign requirements (R05 / R10); (c) synth-04 5.3.2 C1 lists three blogs with no URL (stated honestly: "no URLs given in web-03"); (d) the T2bModel01 count "18 lines in 11 files" has no stated scope (recount: 16 / 10 tracked outside `.dev`, 22 / 16 with untracked mirrors); (e) report-facing text mentions process internals ("Gate 1", "fix cycle 1", "consolidated QA row P3-070"). | Glob for the three files; `git grep`; reading. | Add directories; add R16 and R05 / R10 to the source list; state the scope of the count; drop process references at assembly. |

---

## 5. Gate-focus notes (no finding)

- Report-only scope: synth-04 5.3.2 and 5.3.5 repeat web-03's branch-naming rules ("hyphenated siblings", "decide the layout before the first push"). They are labelled external, the 5.5 preamble says recommendations are "not adopted here", and synth-03 K-8 states the ref fact "no branch layout is proposed here". No branch plan, PR plan, roadmap or risk register exists in the four files.
- `[CODE-VERIFIED]` figures that matter most to later sections were re-derived by me from git or the code and all matched: the 148 / 24 / 93 / 31 gap counts, the 16 / 11 / 1 / 2 / 2 / 0 matrix classes, 36 verdict tests, the #519 / #518 file counts, the E2 tree counts, the E3i script sizes, and the 62-row web coverage table.
- Not re-derived by me (taken from research files, stated as such by the synthesis): the R17 row counts (171 / 170 / 75 / 29), the per-run E1 pilot and combo figures beyond those quoted above, R15's manifest race, E3i internals ([UNVERIFIED] by design), and the swarm-lens import count in G-105.

---

## 6. Summary

- Findings: 7 in total. Blocking (by the override): 0. Minor notes: 7 (F-1 to F-4 would have been blocking under the old definition and carry the text "(minor under grading override)"; F-5 to F-7 are minor under both).
- Checklist items 1-6 and gate-focus items G1-G4: 10 of 10 PASS.
- Files modified: none of the reviewed files; only this report was written (plus a temporary script in `/tmp`, deleted).
- No fix cycle is needed: no blocking finding is open. The seven notes go to the follow-up list; F-1 (escape pipes) and F-3 (drop `50d4d2b9d` from the E1 sentence) are one-line edits at assembly if the owner wants them.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 25 | Grep: 30 | Glob: 4 | Bash: 14 (batched read-only scripts; one `uv run python` table check)
No web research was needed (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0). Tool calls (Read + Grep + Glob = 59) exceed the 10 checklist items.
Unchecked items: none. Unverifiable items: none (limits of what was not re-derived are listed in section 5).

## Overall Verdict: PASS

Zero blocking findings under `qa/grading-override.md`. The four files are ready for assembly; the seven notes are follow-ups.

## QA Complete

Status: Complete
