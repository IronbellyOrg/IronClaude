# Research Completeness Verification (Gate 1, completeness lens)

**Topic:** Observer, sweep and dashboard family technical reference
**Date:** 2026-11-20
**Depth tier:** Standard
**Status:** Complete
**Verdict:** FAIL (1 blocking finding B-1, 6 minor notes)
**Analyst:** rf-analyst, analysis type completeness-verification, fix authorization false (report only)
**Files analyzed:** 6 research files in `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/research/` plus `research-notes.md`
**Snapshot used for spot checks:** `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6); SPEC read with `git show origin/master:` (read-only)

---

## Checklist 1: Coverage audit (research-notes EXISTING_FILES a to d)

| Scope item | Covered by | Status |
|---|---|---|
| (a) observe/adapter.py, parse.py, collector.py, questions.py, export.py, snapshot.schema.json, fixtures | 01 (sections 1 to 9, 11) | COVERED |
| (a) observe/commands.py, view.py, render.py, keys.py, terminal.py, theme.py, sanitize.py | 02 (sections 1 to 4) | COVERED (render.py layouts read by name and cited lines; 06 gap 13 says internals not read in full) |
| (a) main.py:590-592 registration; tests/observe (36 files) | 02 section 5.1, 01 section 8, 9 | COVERED |
| (a) docs: cli-groups.md:40-54, README.md:136, CHANGELOG, post-release-report.md | 02 section 5.4 | COVERED |
| (b) sweep/classify.py, models.py | 03 | COVERED |
| (b) sweep/probes.py, commands.py, report.py | 04 sections 1 to 3 | COVERED |
| (b) commands/sweep.md, skills/sc-sweep-protocol/SKILL.md | 03 section 8, 04 sections 4, 6.5 | COVERED |
| (b) core/WORKER-CONTRACT.md (WC-16, "The sweep", WC-10, never-as-worker), HOW-WE-WORK.md:298, 359 | 04 section 6 | COVERED |
| (b) docs/designs/orchestrator-mode.md (NOT a general orchestrator doc; :27 stale) | 03 section 0, 04 section 7 | COVERED |
| (b) tests/sweep (323 tests, fixtures), tests/commands/test_sweep_command.py (28) | 03 section 6, 04 section 4 | COVERED (28 re-counted by this analyst: `grep -c '^def test_'` = 28) |
| (c) agent-work-report SKILL.md, config.json, 16 scripts, 7 templates | 05 sections 1 to 14, 22 | COVERED |
| (c) tests/skills/test_agent_work_report.py (142), test_worker_contract.py | 05 sections 20, 21 (142 re-counted by this analyst) | COVERED |
| (c) docs/designs/orchestrator.md, sc-closeout.md, settle.sh:1037-1042 | 05 sections 15, 17, 28 | COVERED (sc-closeout.md section 12.2 ruling not read: 05 section 28, gap 16) |
| (c) orchestrator PRs after 61ac2c2e6 | 05 sections 18, 19 | COVERED |
| (d) .dev/design/orca-observer-20261106/ package | 06 sections 1 to 5 | COVERED |
| (d) .dev/issues/409/ and origin/master-only records | 06 sections 3, 7; 02 section 6 | COVERED |
| (d) .dev/research/orca-dashboard-20261105/ (local-only) | 06 section 10 | COVERED, marked local-only |
| Cross-cutting (i) data sources | 01 s12, 04 s1, 05 s27, 06 s8.2 | COVERED |
| Cross-cutting (ii) output formats and where written | 01 s6, 04 s2/3, 05 s23, 06 s1 | COVERED |
| Cross-cutting (iii) live versus designed | 02 s6.4, 05 s29, 06 s4 | COVERED |
| Cross-cutting (iv) consumers | 02 s5.3, 04 s6.6, 05 s7/10/27, 06 s8.3 | COVERED |
| Cross-cutting (v) overlaps in purpose | pieces in 01 s7, 02 s3.4, 04 s3.3/s6.1, 05 s5/s12/s24, 06 s5 S9 | PARTIAL: no file compares the three definitions of "waits on a person", the two terminal-to-transcript join keys, or the sanitizers and Orca wrappers side by side. This is synthesis work (synth-01 matrix) but the facts exist; see minor note M-3 |
| Cross-cutting (vi) WC-16 tie and what Clay's orchestrator design would meet | 04 s6.1, 05 s17, 05 s29 | COVERED |
| Known contradiction: orchestrator-mode.md:27 | 03 s0 | COVERED, re-verified by this analyst (line 27 reads "`src/superclaude/cli/sweep/` does not exist yet.") |
| Known contradiction: issue 409 body vs banner vs comment; unmerged vs PR #503 | 06 C1, C2, C6 | COVERED |
| Known contradiction: Bubble Tea vs Python/Rich | 06 C3 | COVERED |
| Known contradiction: research mockup actions vs package ban; sweep "next inspection" | 06 C4 | COVERED |
| Known contradiction: AWR `orchestrator_repo` | 05 s16, s19 | COVERED and answered (see spot checks 11 and 12) |
| Known contradiction: AWR qa-report-template unreferenced | 05 s22 | COVERED |
| Known contradiction: local-only research folder | 06 s3.1, s10 | COVERED |

Result: no scope item is without a research file. One PARTIAL (cross-cutting v) rated minor.

## Checklist 2: Evidence quality

Method: read every file in full; checked that findings carry `file:line`, function or class names; counted unsupported assertions only where they stood out (no exhaustive claim count is made, so no ratio is invented).

| Research file | Evidence pattern | Unsupported or weakly supported assertions seen | Rating |
|---|---|---|---|
| 01-observe-data-contract.md | Every table row and bullet cites adapter/parse/collector/questions/export lines and test lines | Section 3.4 "real spacing is cycle duration + wait" is labelled an observation, not asserted by docs; fine | Strong |
| 02-observe-interaction-gates-docs.md | Key map, exit codes and flags cite commands.py, view.py, keys.py lines; PRs cite state and merge commit | Section 5.2 says some test bodies "not read" and marks them UNVERIFIED; honest | Strong |
| 03-sweep-classifier-joins.md | 9-rule table with classify.py lines, test lines and fixture names; producer search is a whole-snapshot Grep with listed hits | Section 9 relies on issue #590 and a task-package record, marked UNVERIFIED where not re-run | Strong |
| 04-sweep-readside-wc16.md | Allowlist, git, budgets, publish and exit codes cite probes.py and commands.py lines | Gap 11 admits `classify.py` and `models.py` were read only in part; C8 section contains a location error for the D7 row (finding B-1) | Adequate (one defect, see B-1) |
| 05-agent-work-report-living-report.md | Every script has a section with line cites; entry-file contract table lists readers by line | Orchestrator-PR facts rest on `gh` output (not reproducible by this analyst); marked as run 2026-11-20 | Strong |
| 06-dashboard-design-vs-observer-gaps.md | Counts re-derived with `find`/`ls`/`cmp`; rules S1-S11 and R1-R11 each point to code lines; contradictions C1-C8 each settled against a live source | Local-only sources flagged; package test results correctly marked UNVERIFIED | Strong |

## Checklist 3: Documentation staleness tags

| Claim | Source doc | Verification tag | Status |
|---|---|---|---|
| `src/superclaude/cli/sweep/` does not exist yet | docs/designs/orchestrator-mode.md:27 | [CODE-CONTRADICTED] [STALE DOC] (03 s0); this analyst re-read line 27 and the folder exists | OK |
| `working` is never produced | CHANGELOG.md:170, docs/user-guide/commands.md:620 | [CODE-CONTRADICTED] (03 s0, s2); this analyst confirmed CHANGELOG.md:170 text and `_rule_working` at classify.py:251 | OK |
| `orchestrator_repo` in issue-watch.json | AWR SKILL.md:14, common.py:25 | [CODE-CONTRADICTED] against cycle.py:216-220 (05 s16); this analyst read cycle.py:58-69 and 216-220 and common.py:28-51 | OK |
| `prefs.py answer <run> <session url> session` | AWR SKILL.md:172 | [CODE-CONTRADICTED] against prefs.py:20 (05 s13, Gaps 2); this analyst read prefs.py:20, 30-32 and SKILL.md:172 | OK |
| "no key and no option maps to an Orca call" | cli-groups.md:42, HELP | [CODE-VERIFIED] for keys, "loose for options" (02 s5.4, Gap 3) | OK |
| "No technical doc for `superclaude observe` (13 source files)" | post-release-report.md:173 | [STALE DOC] with count caveat (02 s5.4) | OK |
| Issue 409 body lines 19, 25, 27/28/204, 36, 105 | live issue body | [CODE-CONTRADICTED] / [STALE DOC] (06 C1, C6, Stale table) | OK |
| "#409 is unmerged" | orchestrator-mode.md:609 | [CODE-CONTRADICTED] in part (06 C2) | OK |
| Bubble Tea preferred | package README:46-48 | [STALE DOC] (06 C3) | OK |
| fixture mode uses "the package's synthetic fixtures" | rendering-rules.md:3 | [CODE-CONTRADICTED] (06 C8, `cmp` of all 10 pairs) | OK |
| qa-report-template.md reads by `run.py gate` | AWR templates | [STALE DOC] (05 s22) | OK |
| sc-closeout.md:361 "skill is in IronFlow" | sc-closeout.md | [STALE DOC] (05 s28) | OK |
| D7 row at design-base.md:813 / design line 813 is a different row | 04 Stale list | UNTAGGED as incomplete: the D7 row IS in the snapshot design at orchestrator-mode.md:841 (this analyst printed it) | FLAG (part of B-1) |

No doc-sourced claim is presented as current fact without a tag, except the D7 location statement in 04, which is wrong rather than untagged. No [CODE-CONTRADICTED] claim is reported as current fact.

## Checklist 4: Completeness of each research file

| Research file | Status line | Summary | Gaps section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-observe-data-contract.md | Complete (line 4) | Y (line 367) | Y "Gaps and Questions" (346) | Y (per section, 57, 95, 137, 211, 341) | Complete |
| 02-observe-interaction-gates-docs.md | Complete (line 4) | Y (301) | Y (280) | Y (62, 103, 150, 180, 227, 275) | Complete |
| 03-sweep-classifier-joins.md | Complete (line 4) | Y (309) | Y (283) | Y (23, 51, 79, 100, 152, 192, 209, 223, 267, 280) | Complete |
| 04-sweep-readside-wc16.md | Complete (line 4) | Y (295) | Y (274) | Y (88, 117, 147, 168, 193) | Complete |
| 05-agent-work-report-living-report.md | Complete (line 4) | Y (609) | Y (575) | Y (per section through section 17, 18; sections 19 to 29 have none) | Complete (Key Takeaways thin in late sections; minor) |
| 06-dashboard-design-vs-observer-gaps.md | Complete (line 4) | Y (299) | Y (266) | Y (29, 47, 75, 99, 158, 189, 245, 262) | Complete |

All six files satisfy item 4. 05 sections 19 to 29 end without a Key Takeaways line; the file Summary and Gaps cover them. Minor.

## Checklist 5: Cross-references between files

| Shared concern | Files | Cross-referenced? |
|---|---|---|
| Question read non-consumption | 01 s10, 02 s4/s6.2, 06 R4/FG-8 | Consistent; 01 s10 and 02 s6.2 both cite release-gates.md:40-50 and the owner pass record; no contradiction |
| Gate constants True and wired | 01 s5.2, 02 s4, 06 s9 | Consistent |
| stalled (proved), fenced, agent_wait_since (C8) | 03 s7/s8, 04 s5 | NOT reconciled, files disagree (finding B-1) |
| Observer fixture replay of questions/desk | 02 s4 step 7 and Gap 10, 06 s9 D-1 | 02 sees the refusal at commands.py:187-188 but records no defect; 06 records D-1. No cross-reference (minor note M-1) |
| Sweep JSON as a possible observer input | 04 s8 gap 7, 06 s8.3 | Consistent: no code, only an undecided proposal |
| `agentWait` source | 03 s1, 04 s5/s6.1 | Consistent on UNVERIFIED meaning |
| PR #503 contents | 02 s6.3 (first 100 files), 06 s3.1 (545 files) | Compatible; 06 supersedes 02's truncated view (minor note M-2) |
| `orchestrator_repo` key | 05 s16, s19 | Consistent with cycle.py reading by this analyst |
| Sweep as a read for the coordinator and AWR as the report for Clay | 04 s6, 05 s17 | Both state facts, no unifier text; fine for a facts-only reference |

## Checklist 6: Contradiction detection

### 6a. Known contradictions from research-notes: each addressed with evidence?

| Known contradiction | Where addressed | Evidence quality | Result |
|---|---|---|---|
| orchestrator-mode.md:27 says sweep package absent | 03 s0 (Glob of 6 files) | Re-verified by this analyst | Addressed |
| Issue 409 body "no observer code" vs banner vs comment 2; unmerged vs content on master | 06 C1, C2, C6, PR REST file list (545 files for #503) | `git merge-base`, `git diff` empty, PR list; plausible and internally consistent | Addressed |
| Bubble Tea vs Python/Rich | 06 C3 (stack.md:3, owner decision 2, Rich imports) | Cited | Addressed |
| Research-mockup actions vs package ban vs sweep "next inspection" | 06 C4 (with a correction to the scope file's line cite) | Cited | Addressed |
| AWR SKILL.md:14 `orchestrator_repo` | 05 s16, s19 | Master `_TOP_KEYS` rejects it (analyst read cycle.py:58-69, 216-220); PR A branch accepts it (gh, not reproduced by analyst) | Addressed, answers the "UNVERIFIED who reads/sets" question: reader is common.py:38-51 only; setter unverified |
| AWR qa-report-template.md unreferenced | 05 s22 | Whole-snapshot Grep | Addressed |
| Local-only research folder | 06 s3.1, s10 | `git status` and `git ls-tree` | Addressed |

### 6b. New contradictions between research files

1. **C8 determinations for `stalled (proved)`, `fenced` and `agent_wait_since` conflict between 03 and 04.**
   - 03 section 8.1/8.2/8.5: "not a DEFECT-CANDIDATE under the C8 rule, because a cited, spec-level scope decision exists (SPEC:232 plus design D7)". It cites SPEC lines 231, 232, 251 and design D7 at orchestrator-mode.md:841.
   - 04 section 5 and Gaps 1 and 2: "DEFECT-CANDIDATE ... no owner decision declaring the capability out of scope was found"; same for `agent_wait_since` ("DEFECT-CANDIDATE (low)"). 04 does not mention SPEC lines 231/232/251 and says the D7 row "lives at design-base.md:813 in the task package" and that line 813 of the snapshot design is a different row.
   - This analyst verified: SPEC (origin/master `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`) line 232 reads "`worker_done_seen` is None on live rows, because no named live source establishes its absence. Stalled (proved) stays fixture-only until a source mapping exists..."; line 231 states `fenced_evidence` is "always `unreadable` on live rows in Phase 1"; line 251 reads "(synthetic fixtures only in Phase 1)" for `fenced`. Design `docs/designs/orchestrator-mode.md:841` does hold the D7 row (and :877 "Applied as D7"). So 03's citations are accurate and 04's location statement is wrong/incomplete.
   - Neither file mentions the other's determination. Synthesis Section 14 would receive two incompatible C8 records for the same two classes. Logged as blocking finding B-1.
2. 01 and 02 say "no DEFECT-CANDIDATE" for the observer; 06 D-1 records one (fixture replay of the question ledger and Decision Desk). Scope differs (live R2/R3 wiring vs fixture replay), so not a hard contradiction. Minor note M-1.
3. No contradiction found between 01 and 02 on gate constants, limits, snapshot behaviour, or the non-acknowledging read.
4. Line-count differences (probes.py 1478 in 04 vs `wc -l` 1477 by this analyst; adapter.py 513 in 01 vs 512 in notes) are cosmetic.

## Spot-check table (citations re-read against the snapshot or origin/master)

Paths are relative to `/home/coder/.cache/ic-snap-20261120/master` unless stated. 20 citations checked across all six files.

| # | Research file | Citation | What this analyst read | Result |
|---|---|---|---|---|
| 1 | 01 | adapter.py:34-50 (13 forbidden prefixes) | frozenset with check, --ack, --wait, --retry-request, --peek, dispatch, inbox, run-use, run-create, send, ask, reply, reset = 13 | MATCH |
| 2 | 01 | adapter.py:29-32, 57-63 (templates, caps, timeouts) | WORKER_LIST_TEMPLATE, DISCOVERY_TEMPLATE, QUESTION_TEMPLATE (5 tokens, the 8-token shape adds `--run <id> --json`), MAX_CALLS_PER_CYCLE 5, MAX_OUTPUT_BYTES 8 MiB, STDERR_KEEP_BYTES 2048, KILL_GRACE_SECONDS 2.0 | MATCH |
| 3 | 01 | parse.py:43 UNKNOWN singleton | `UNKNOWN: Any = _Unknown()` at line 43, class at 25 | MATCH |
| 4 | 01 | collector.py:28-32 and 303-321 (interval, backoff, reset) | INTERVAL 15.0, CYCLE_BUDGET 15.0, MAX_BACKOFF 60.0, JOIN_TIMEOUT 5.0; `_wait = min(_wait*2, max_backoff)` at 306; reset at 321 | MATCH |
| 5 | 01 | view.py:33-35 STALE_SECONDS 45 | `STALE_SECONDS = (45.0  # three intervals without a successful poll, on the monotonic clock)` at lines 33-35 | MATCH |
| 6 | 02 | commands.py:67, 70 gate constants True | both `= True` with the cited record comments | MATCH |
| 7 | 02 | keys.py:22-23 MAX_TIMEOUT 0.25, ESC_WAIT 0.05 | exact | MATCH |
| 8 | 02 | main.py:590-592 registration | import at 590, `main.add_command(observe_group, name="observe")` at 592 | MATCH |
| 9 | 02, 06 | view.py:134 UNAVAILABLE_FACTS | `("report status", "acceptance", "tests", "approval")` at 134 | MATCH |
| 10 | 03 | classify.py:345 RULES, :40 JOIN_PATH = "B", :215-222 rules 2 and 3 | all at the cited lines | MATCH |
| 11 | 03, 04 | no producer of `worker_done_seen` / `fenced_evidence` | Grep over `src/superclaude/cli/sweep`: only models.py:108-109 defaults and classify.py readers (198-222). Whole-snapshot grep not re-run by this analyst | MATCH within the sweep package |
| 12 | 03 | SPEC lines 103, 106, 231, 232, 251, 274, 338 | printed from `git show origin/master:` and the text matches 03's quotations | MATCH |
| 13 | 03 | design D7 at orchestrator-mode.md:841 and :877 | line 841 is the D7 row; 877 "Applied as D7; Rule 5 restored..." | MATCH (04 contradicts, see B-1) |
| 14 | 03 | CHANGELOG.md:170 says `working` never produced | line 170 reads "...and `working` is never produced, because the live `agentWait` names were never captured" | MATCH |
| 15 | 03 | orchestrator-mode.md:27 | "- `src/superclaude/cli/sweep/` does not exist yet." | MATCH |
| 16 | 04 | probes.py:49-60 (10 templates, 4 not called), 43, 62, 85-88, 1381; commands.py:29 MAX_SUFFIX 99 | all present as cited; limits annotated "proposed (DESIGN 17 open item 19)" | MATCH |
| 17 | 04 | WORKER-CONTRACT.md:287-289 (WC-16) incl. "classes follow WC-10", no word `fenced` | text matches; Grep of `fenced` in the file hits only lines 61 and 63 | MATCH |
| 18 | 05 | common.py:28-51 `repo_root`; cycle.py:58-69, 216-220; prefs.py:20, 30-32; SKILL.md:14, 172 | all as described; master rejects an unknown top-level key; session url fails `URL` regex | MATCH |
| 19 | 05 | waker.py:39-42 (15 retries, 120 s) | exact | MATCH |
| 20 | 06 | theme.py:59-69 truecolor palette | eight RGB values match 06's list; package-side canvas.py:7 not re-read | MATCH on the observer side |

Also re-counted: `tests/commands/test_sweep_command.py` 28 tests, `tests/skills/test_agent_work_report.py` 142 tests, agent-work-report SKILL.md 194 lines, `tests/observe` 36 entries (all as stated). Cosmetic: commands.py is 524 lines by `wc -l` (02 says 525), probes.py 1477 (04 says 1478).

## Checklist 7: Compiled gaps (deduplicated)

### Critical gaps (block synthesis)
- **G-C1.** One reconciled C8 determination for `stalled (proved)`, `fenced` and `agent_wait_since` is missing (03 vs 04 conflict). Source files: 03 s8 and 04 s5, Gaps 1 and 2. See B-1.

### Important gaps (affect quality; not blocking because each is recorded and honestly marked in its source file)
- **G-I1.** Whether `orchestration check --all --types question` is non-acknowledging: UNVERIFIED from code. Recorded probes show non-consumption for the owner-bound reader only; owner accepted the remainder 2026-11-12 (01 s10, Gap 1; 02 s6.2). Synthesis must carry this as UNVERIFIED with the owner record.
- **G-I2.** D-1: no CLI path replays the question ledger or Decision Desk from fixtures (06 s9). Remediation task not created; flagged for the owner.
- **G-I3.** R5 living-report writer absent: `superclaude orchestrator report-entry`, the `orchestrator` package and `/sc:orchestrator` do not exist; PR B has no PR; PR A (#686) and PR P (#690) open (05 s15, s18, s29). Recorded as DEFECT-CANDIDATE with the required line.
- **G-I4.** `prefs.py answer <run> <session url> session` cannot take an `orca://session/` url (05 Gaps 2); `orchestrator_repo` route rejected on master (05 Gaps 3). Both carried with [CODE-CONTRADICTED] and the DEFECT-CANDIDATE line.
- **G-I5.** Orca-side facts outside the repo stay UNVERIFIED: automations `coordinator-morning-wake`, `coordinator-missed-check`, `orchestrator-poll`; orchestrator repo `repos.yaml`; SPEC-AGENT-WORK-COORDINATOR file; who writes `issue-watch.json` (05 Gaps 4 to 6).
- **G-I6.** Design section 17 open items: the table has no status column; 04 section 7 marks several UNVERIFIED (items 1, 17, 18, 21, 22, 23) and 12 and 13 unresolved. Synthesis must not state them as closed.
- **G-I7.** `agentWait` non-null meaning never captured (03 Gap 6, 04 Gap 3); 256 KiB transcript tail limit effect on `working` and `finished` not measured on real transcripts (03 Gap 7).
- **G-I8.** Package results (19 tests passed, gallery DOM) not re-run; visual-parity gate scored on text and ANSI tier because the PNG route failed (06 Gaps 1, 12).
- **G-I9.** Version placement of observer R2/R3 (which tag first held them) unknown: no CHANGELOG entry in [Unreleased], 6.1.0 or 6.0.0 (02 Gap 9).
- **G-I10.** Schema/parser mismatch risk for nested `counts`; unbounded in-memory row set in `merge`; `_find_orca` raising on odd `topics` shapes in the observer's polling thread (01 Gaps 4 to 6): all untested, honestly marked.

### Minor gaps (notes)
- sc-closeout.md section 12.2 ruling on two writers of the closed entry not read (05 Gap 16); design test rows (1146-1216, 1253-1320) partly unread (05 Gap 19).
- PR file lists truncated at 100 in `gh pr view` (02 Gap 7); 06 supplied full REST lists for #503 (545) and #673 (2,831) but not for #514, #577, #592.
- `route 7` of the git-hole list not found (04 Gap 5); `Window.more_text` dead field (06 s9); test_keys_spike.py:3 docstring older than test_live_screen_pty.py (02 Gap 11).
- Line-count off-by-one items (see spot check note).

## Checklist 8: Depth assessment (Standard) and the C8 check

**Expected depth (Standard):** all public APIs documented, integration points mapped, subsystems traced.
**Achieved:** all four subjects have file-level and function-level coverage with line cites; data flows are traced hop by hop (01 s12, 04 s6.1 hop list, 05 s25 pipeline table); integration points (Orca verbs per tool, binary choice, git, gh, ClickUp REST) are enumerated (01 s1, 04 s1, 05 s27); error and exit tables exist (01 s11, 02 s1.1, 04 s2.4). Missing depth elements: none blocking. Unread internals are declared (render.py layout internals, `classify.py` partial read in 04, package `layouts/*.py`).

### C8 table (in-scope capabilities that are named but cannot fire or are unwired)

| Capability | File and record | Form of record | Meets C8 form? |
|---|---|---|---|
| stalled (proved) class | 03 s8.1: cites SPEC:231-232, 251, design :493 and D7 :841 as on-record scope decision; adds residual facts and "Remediation task not created (read-only brief); flagged for the owner". 04 s5: DEFECT-CANDIDATE with the line | Two different forms for the same item | Each form is individually allowed; the pair is inconsistent (B-1) |
| fenced class | 03 s8.2 (not defect; SPEC:231, 251); 04 s5 (DEFECT-CANDIDATE) | same | same (B-1) |
| `agent_wait_since` never set | 03 s8.5 (scope text exists, not defect); 04 Gap 2 (DEFECT-CANDIDATE low) | same | same (B-1) |
| Safe to close | 03 s8.3 cites SPEC:106, 274, design traceability row, report.py:46-49; 04 s5 "declared Phase 1 limit" | on-record decision cited | Yes, consistent |
| Removable | 03 s8.4 (SPEC:106, 274, 338); 04 s5 | on-record decision cited | Yes, consistent |
| Living-report writer (`report-entry`) | 05 s15 and Gaps 1: DEFECT-CANDIDATE, design sequencing quoted, line "remediation task not created (read-only brief); flagged for the owner" | DEFECT-CANDIDATE | Yes |
| Observer R2/R3, snapshot, `--once` | 01 Gaps 9, 02 s4 and Gaps 10: wired; no defect | reachability chain traced from click option to Orca call | Yes |
| Observer fixture replay of question views | 06 s9 D-1 | DEFECT-CANDIDATE with the line | Yes (02 not cross-referenced, M-1) |
| Ready-Task creator, remote hosts, Orca messages | 04 s5: declared Phase 1 limits with cited text | on-record | Yes |
| `prefs.py answer <session url>` and `orchestrator_repo` route | 05 Gaps 2, 3 | DEFECT-CANDIDATE with [CODE-CONTRADICTED] | Yes |
| Observer snapshot has no in-repo consumer | 02 s5.3 | stated as absence, not an unwired capability; no doc claims a consumer | Fine |
| Hold/pause, heartbeat classification, secret redaction, superseded attempts | 06 s5.1 S10, s5.2 R5, R8, R9 | "not built, package-only / not adopted by the observer SPEC" with citations | Yes |

No item is relabelled as a plain known gap. The only C8 defect is the inconsistency listed as B-1.

## Verdict: FAIL (1 blocking finding, 6 minor notes)

All six research files are complete, evidence-based and well tagged; 20 of 20 spot-checked citations matched the snapshot or origin/master. The one blocking defect is that two research files record opposite C8 determinations for the same unwired sweep capabilities, and one of them (04) rests on a wrong statement about where design decision D7 lives and does not find the SPEC scope decision that 03 cites. Synthesis cannot write Section 14 until that is reconciled.

## Findings

### Blocking

**B-1. Conflicting C8 determinations for `stalled (proved)`, `fenced` and `agent_wait_since` (03 vs 04); 04 misses the on-record SPEC decision and mislocates D7.**
- Files: `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/research/04-sweep-readside-wc16.md` (section 5 DEFECT-CANDIDATE paragraphs, Gaps 1 and 2, Stale list item 2, Summary) versus `.../research/03-sweep-classifier-joins.md` (section 8.1, 8.2, 8.5, Gaps 2 and 3, Summary).
- Evidence: 03 says "not a DEFECT-CANDIDATE ... a cited, spec-level scope decision exists (SPEC:232 plus design D7)". 04 says DEFECT-CANDIDATE, "no owner decision declaring the capability out of scope was found", and that the D7 row "lives at design-base.md:813 in the task package" while "in the snapshot, line 813 of the design is a different row (NFR-005)". Re-read by this analyst: SPEC line 232 ("Stalled (proved) stays fixture-only until a source mapping exists"), line 231 and line 251 exist as 03 quotes; `docs/designs/orchestrator-mode.md:841` is the D7 row and :877 says "Applied as D7". 04 does not cite SPEC lines 231/232/251 at all. Neither file cross-references the other. The research-notes C8 rule requires each such capability to be recorded either with a cited on-record scope decision or as a DEFECT-CANDIDATE with the line "remediation task not created (read-only brief); flagged for the owner", and requires contradictions between agents to be surfaced.
- Why blocking: Section 14 of the reference would carry two incompatible records (and 04's D7 location error is a false claim).
- Remediation (owner of fix: research agent for file 04, with a one-line cross-reference in 03): (1) add SPEC:231-232, 251 and design D7 at orchestrator-mode.md:841/:877 and :493 to 04 section 5; (2) state one determination for each of stalled (proved), fenced and `agent_wait_since`, either "on-record scope decision cited" (03's reading, consistent with the research-notes instruction to quote the Phase 1 limits) or DEFECT-CANDIDATE with the stated reason why the SPEC text is not accepted as a scope decision; (3) correct the D7 location sentence in 04's Stale list; (4) if both views are kept, label them as a disagreement with both citations; (5) carry the residual fact both files share (no owner-dated ruling and no work item for the "source mapping"; `fenced` has no "until" condition per 03 s8.2).
- Proposed gap-filling investigation: read-only re-read of SPEC lines 103, 231-232, 251 and the `agent_wait_since` text that 03 s8.5 quotes (this analyst did not verify that last quotation), plus orchestrator-mode.md:493, 841, 877; then a single paragraph both files can cite.

### Minor notes (do not fail the gate)

- **M-1.** 01 Gap 9 and 02 s4/Gap 10 say "no unwired capability / no DEFECT-CANDIDATE" for the observer; 06 s9 records D-1 (fixture replay of question ledger and Decision Desk refused by `--questions --fixture`, commands.py:187-188). Scopes differ, but 02 s4 step 7 saw the refusal. Synthesis should carry D-1 and word the observer summary as "R2/R3 live path wired; fixture replay of B and C unreachable (D-1)".
- **M-2.** 02 Gap 7 (PR file lists truncated at 100) is partly closed by 06 s3.1 (545 files for #503, 2,831 for #673). Use 06's counts; #514, #577, #592 full lists remain unread.
- **M-3.** Cross-cutting (v), overlaps in purpose, exists only as scattered facts (three meanings of "waits on a person": observer question panel, sweep waiting (a)/(b), AWR "waiting on you"; two terminal-to-transcript joins: sweep tab map vs AWR hook file and `ORCA_TERMINAL_HANDLE`; four sanitizers; three Orca wrappers). Synthesis must assemble it; no research gap blocks it.
- **M-4.** Cosmetic: commands.py 524 lines (02 says 525), probes.py 1477 (04 says 1478), adapter.py 513 (01) vs 512 (notes).
- **M-5.** 05 sections 19 to 29 lack Key Takeaways lines (the file Summary and Gaps cover them).
- **M-6.** Design section 17 statuses in 04 s7 are mostly UNVERIFIED because the table has no status column; they are honestly tagged, so synthesis must keep the tags.

**Status:** Complete
