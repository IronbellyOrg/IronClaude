# QA Report - Research Depth (Gate 1, research-depth lens)

**Topic:** Observer, sweep, AWR and dashboard-design technical reference, research files
**Date:** 2026-11-20
**Phase:** doc-qualitative (research-depth lens)
**Fix cycle:** N/A (first review)
**Status:** Complete
**Overall Verdict:** FAIL (4 blocking, 5 minor)

---

## Progress log
- Report created. Read research-notes.md and all six research files (01 to 06) in full.
- Early observation (to confirm): 03 section 8 says stalled/fenced are NOT DEFECT-CANDIDATEs (SPEC lines 231-232, 251; design D7 at orchestrator-mode.md:841); 04 section 5 and Gaps 1-2 record the same two classes as DEFECT-CANDIDATE (SPEC not read; D7 cited at design-base.md:813) and record agent_wait_since as DEFECT-CANDIDATE (low) where 03 section 8.5 says scope text exists. Cross-file contradiction on the C8 determination that Section 14 must carry.
- Candidate gaps to verify against the snapshot: (a) orchestrator.md mentions of sweep/observe/WC-16 (question vi); (b) design-package build path (fixture to exports) for Section 4; (c) AWR config.json keys for Section 9; (d) classify rule return shape and classify_all/collect signatures for Section 13; (e) D7 line location.
- Spot-reads done (a) to (e): confirmed contradiction F-1; confirmed orchestrator-design gap F-2; confirmed signature gap F-3; confirmed design-package pipeline gap F-4; config.json keys are mentioned piecemeal (note only).
- Next: write per-check tables, findings, verdict.

---

## Per-check results (subject by check)

Legend: OK = answerable from the research files with citations; PARTIAL = answerable only in part; GAP = not answerable. Subjects: OBS = observer (01, 02), SWP = sweep (03, 04), AWR = agent-work-report (05), DSN = dashboard design package (06).

### Check 1. Traced data flows (not only file listings)

| Subject | Result | Evidence |
|---|---|---|
| OBS | OK | 01 section 12 gives the hop-by-hop flow `skills list --json` -> `LiveSource.read_pages` -> `parse_page`/`parse_questions` -> `merge`/`merge_questions` -> `CycleResult` -> `build_view` -> screen / `record_text` / `snapshot_json`, each hop with file:line in sections 1-6; 02 section 4 traces `--questions` from the click option to `LiveSource.read_questions` (7 numbered hops with lines). |
| SWP | OK | 04 section 2.1 (`run` pipeline: parse window, check root, bind_run, `probes.collect`, `classify_all`, `render`, `_publish`, JSON print, commands.py:246-278) and 1.6 (`collect` order, probes.py:1322-1396); 03 section 4.1 (`classify_all` order of work, classify.py:880-1009) and section 7 (call graph of the readers of `worker_done_seen`). |
| AWR | OK | 05 section 25 maps the 15 steps to script, reads, writes and external commands; sections 3-14 give per-script flows with lines; section 23 lists every run-folder artifact with writer line. |
| DSN | GAP | 06 inventories files, fixture keys, QA verdict and rules, but never traces the package's own pipeline. Snapshot-free check: `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/render.py` (130 lines) has `designs(batch)`, `screen`, `image`, `exports(batch)` (writes `.txt`, `.ascii.txt`, `.ansi`, `.svg`, `.png`, `.mono.png`, `contact-sheet.png`, `portfolio.pdf`, `manifest.json`, lines 52-72), `build_gallery` (line 124 writes `gallery.html`) and an argparse `--batch {1,2}`, `--show`, `--width` (line 127). None of that is in 06; the reproduction commands (package README.md:24-26) are described as "not run" in 06 section 3.2 but never recorded. Only scope/04 (an unverified starting map) names `render.py` and its flags. See F-4. |

### Check 2. Function signatures (real parameter lists and return shapes)

| Subject | Result | Evidence |
|---|---|---|
| OBS | PARTIAL | Return shapes are given for `SourceResult(state, pages, code, diagnostic, capped, calls)` (01 1.4), `CycleResult` (01 3.2), `Row`, `Snapshot`, `Coverage`, `QuestionState`. Parameter lists are given for `merge(previous, pages, stopped_by_cap, stopped_by_error)`, `merge_questions(...)` (01 3.6) and `Collector(..., run_id=, questions=, link=)`. Missing: `LiveSource.read_pages(...)` parameters (01 1.4 describes behaviour only), `build_view(result: Any, session: Session, clock: Any) -> View` (view.py:968; 02 names it with no parameters), `render(view, policy, message=None) -> Group` (render.py:1449), and the field list of `View`. |
| SWP | GAP | No research file states `collect(ctx: SweepContext, runs: tuple[str, ...], root: Path, budget: Budget) -> SweepInput` (probes.py:1322-1324), `classify_all(inp: SweepInput, ctx: SweepContext) -> SweepResult` (classify.py:880), `classify(row: SessionRow, ctx: SweepContext) -> Classification` (classify.py:369), the `Rule(name, match)` dataclass and the `_classification(...)` helper (classify.py:345-355, 222), `render(result, ctx) -> str` (report.py:608), `_publish(text, output_dir, now) -> Path` (commands.py:153) or the `Classification` field list. `grep` of the six research files for `Classification`, `Rule(`, `SweepResult` finds only one unrelated hit (06). Behaviour is described in prose; the contracts a developer needs to add a rule are not. See F-3. |
| AWR | OK | CLI usage lines for every script (run.py dispatch 868-887, clickup, waker, check), `entry(url, it, c, cmp_, ctx, filed=None)`, `template_problems(url, block, orchestrated=False)`, `orca_term` function table with argv (05 section 5), `main(run)` per script. |
| DSN | PARTIAL | `fixture(owners,count,variant)` appears only in scope/04; 06 gives key lists, not signatures. Low weight: the package is not extended in code. |

### Check 3. Exact Orca verbs and where each is built

| Subject | Result | Evidence |
|---|---|---|
| OBS | OK | 01 section 1.1: three argv templates, constants at adapter.py:29-32, built by `build_argv` 173-183 and `build_question_argv` 186-190, checked by `assert_allowed` 135-170; discovery `_find_orca` install_user_setup.py:247-270 with `_ORCA_CLIS = ("orca-ide","orca")`. Verified against snapshot adapter.py:29-50 (13 forbidden prefixes, templates exact). |
| SWP | OK | 04 section 1.1 lists all 10 templates with call sites; verified against snapshot probes.py:49-60 (10 templates, "10 templates, 7 verbs"); binary `orca_binary()` probes.py:214-216 (`orca-ide` or `$ORCA_CLI_COMMAND`). |
| AWR | OK | 05 sections 3, 5, 6, 9, 10, 27 list `orca terminal list/read --screen/wait --for tui-idle --timeout-ms/send --enter --wait-submit/create`, `orca worktree list`, `orca worktree set --unread --comment`, `orca automations list/runs`, `orca tab list/close/switch/create`, `orca eval --page --expression`. Verified against snapshot orca_term.py:17-133 (every call goes through `orca(*args)` which appends `--json`) and page.py:354-377. Bare `orca` is correctly recorded. |
| DSN | OK | Calls no Orca verb (06 section 8.2, `fixtures.py:1` docstring). |

### Check 4. The six cross-cutting questions

| Question | Result | Where answered / what is missing |
|---|---|---|
| (i) data sources of each | OK | 01 section 12; 04 section 1 (Orca, git, disk, tab map, transcripts); 05 section 27 table (GitHub both orgs, Projects, ClickUp REST, Orca terminals/worktrees/automations/browser, hook file, transcripts, /proc); 06 section 8.2 (synthetic fixture only). |
| (ii) output formats and where written | OK | 01 section 6 (snapshot.json v1, `observe-<ts>.txt`, state dir, 0600 atomic); 04 sections 2.3, 3 (one `.dev/sweeps/<UTC>-sweep.md`, JSON v1 with 12 keys on stdout); 05 section 23 (every run-folder artifact); 06 section 1 (export kinds and counts; the producing pipeline is not traced, see F-4). |
| (iii) live versus designed | OK | 05 section 29 built-versus-designed table; 04 section 5 capability audit; 02 section 6.4; 06 sections 3-4. |
| (iv) consumers | OK | 02 section 5.3 (no in-repo reader of the observer snapshot; tests only); 04 section 6.6 (writer only, no code reads `.dev/sweeps`); 05 sections 15, 26 (entry-file readers, nobody writes); 06 section 8.3 (observer reads sweep JSON: proposal only). |
| (v) overlaps | PARTIAL | Status vocabularies: observer raw fields (02 3.4), sweep 8 classes (03 section 2), AWR 6 statuses (05 section 24): all present. "Waits on a person" in three places: sweep rules 1 and 4 (03 section 1), AWR "waiting on you" (05 section 24), observer questions "seen, not resolved" (01 section 4): present but never placed side by side. Two join keys: sweep `session_join` / tab-map (03 section 4) versus AWR hook-file key `tabId:leafId` and `/proc` handle (05 section 9; the terminal fields `tabId`/`leafId` that form the key are not named in 05, sessions.py:327 does). Separate sanitizers and Orca wrappers: present. MISSING: the orchestrator design (`docs/designs/orchestrator.md`) is a fourth status vocabulary (FR-9 follow-up state set) over the same `worker-list` data. See F-2. |
| (vi) WC-16 binding and what Clay's orchestrator design would meet | PARTIAL | WC-16 half is strong: 04 section 6 (WORKER-CONTRACT.md:287-289 versus "The sweep" at :110, cadence not enforced in code, no caller above the skill, never-as-worker list :23, HOW-WE-WORK rows 298 and 359, WC-10 stall proofs). The orchestrator half is limited to the agent-work-report skill and the PR chain (05 sections 15-19). Nothing records what the orchestrator design says about worker-list reads, worker classification, the coordinator role, WORKER-CONTRACT changes, `/sc:sweep`, WC-16 or the observer. See F-2. |

### Check 5. Live-versus-designed accuracy

| Subject | Result | Evidence |
|---|---|---|
| OBS | OK | R0-R3 built with both gate constants True (commands.py:67, 70; 02 section 4); R4, closure evidence, write-back not built (02 6.4). 01 section 10 keeps the non-acknowledging read as UNVERIFIED with the recorded probes cited as documentation, not code. |
| SWP | PARTIAL | 03 correctly separates what prints today (6 of 8 classes) from what cannot (stalled, fenced): verified `worker_done_seen` / `fenced_evidence` appear in the snapshot only in models.py:108-109 and classify.py:198-222 (grep of `src`). 04 states the same facts but labels the outcome differently from 03 and mislocates decision D7 (F-1). |
| AWR | OK | 05 section 29 table; reader side built, writer (`superclaude orchestrator report-entry`) absent; PR A #686 open. Verified in the snapshot that every AWR `orca` call goes through `orca_term.orca(*args)` which appends `--json` (orca_term.py:17-18) and that the page-tab verbs match 05 (page.py:354-377). |
| DSN | OK | 06 sections 3-4: package content is on master through PR #503 although commit 495eb96d1 is unmerged; three of 20 designs have a partial observer counterpart; 17 none. |

### Check 6. Neutrality (no unification recommendation)

| Subject | Result | Evidence |
|---|---|---|
| OBS | OK | 02 Gap 5 and 01 Gap 7 state facts and hand the question to synthesis; no recommendation. |
| SWP | OK (note N-1) | 04 Gap 6 and Gap 7 say a dashboard or unified orchestrator "would need" the pinned-not-called templates or `agentWait`, or must parse the JSON or Markdown; conditional facts about data availability, not recommendations. |
| AWR | OK | 05 uses "Fact only" and "for the owner"; defect candidates are flagged, not remedied. |
| DSN | OK | 06 section 9 asks the owner a question (fixture replay of B and C) and does not recommend. |

### Check 7. Extension-guide raw material

| Scenario | Result | Evidence |
|---|---|---|
| Add a sweep class | PARTIAL | Captured: `models.CLASSES` (models.py:50-59), `C_*` constants (classify.py:42-51), `RULES` (classify.py:345-355), `NEXT_INSPECTION` (report.py:54-68, one entry per rule, test_report.py:1105-1130), the order pin (test_classify.py:378-379), reachability test (:371-375), rule case table (:288-347), zero-count-per-class golden (test_cli_contract.py:1070), prose drift guards (tests/commands/test_sweep_command.py), user-guide and CHANGELOG lines (03 stale-doc table). Missing: the `Rule` and `Classification` contract a new rule must satisfy (F-3). |
| Add a probe / Orca allowlist entry | OK | `ALLOWED_ORCA` probes.py:49-60; pinned by test_probes_allowlist.py:370, 375, 391, 405; `_LIST_KEY` probes.py:362-366; `_call` budget path 369-394; call-site pattern `_orca_reads` 1143-1192; `collect` order 1322-1396; new source row via `SourceCoverage`; `SweepInput` field (models.py:237). |
| Add a snapshot field (observer) | OK | `_FIELDS` parse.py:58-90, `Row` parse.py:109-161, export `_TEXT_FIELDS`/`_ANY_FIELDS` export.py:25-46, `_row_dict` 141-155, schema file lines 103-155, additive-only policy lines 3-4, privacy test test_snapshot_schema.py:296-326, golden contract tests (01 sections 6, 8.2, 9.4). |
| Add an observer panel | PARTIAL | `_questions_panel` view.py:709-885, `_desk` 888-948, `_compose` render.py:1258-1446, `apply_key` view.py:1246-1300, layouts A/B/C, height budget test (02 sections 2-3). Missing: `build_view` parameters and the `View` field list (F-3). |
| Add an AWR source | OK | New script pattern per collect.py/clickup.py; step table SKILL.md:76-95; `REQUIRED_CHECKS` run.py:204-212; artifact table 05 section 23; `compare.TRACKED` compare.py:27-39; match.py joins; test groups by line range (05 section 21). Config keys only piecemeal (note N-3). |

### Check 8. Depth sufficient for 80 to 200 line subsystem sections

| Subject | Result | Evidence |
|---|---|---|
| OBS | OK | 01 (370 lines) plus 02 (306 lines) hold far more than 200 lines of material for 5.1 and 5.2. |
| SWP | OK | 03 (313 lines) plus 04 (299 lines) cover classifier, joins, read side, publish, WC-16, tests. |
| AWR | OK | 05 (614 lines, 29 numbered sections). |
| DSN | PARTIAL | 06 (302 lines) is deep on package status, rules trace, gaps and contradictions: enough for 5.6 and the relationship to the observer; thin on the package internals needed for Sections 3-4 (F-4). |

---

## Findings

Grading: blocking = real defect (cross-cutting question or Extension Guide scenario left unanswerable, false or contradictory claim, missing required deliverable); minor = note only.

### F-1 (BLOCKING; research files 03 versus 04; axis-equivalent: contradiction) Two research files give opposite C8 determinations for the same capabilities, and 04 misapplies the C8 rule and mislocates decision D7

Evidence:
- 03 section 8.1-8.2 and Key Takeaways: stalled (proved) and fenced are "not a DEFECT-CANDIDATE under the C8 rule, because a cited, spec-level scope decision exists" (SPEC lines 231-232, 251; design D7 at `docs/designs/orchestrator-mode.md:841`). 03 section 8.5: `agent_wait_since` is "not a defect candidate on the same basis".
- 04 section 5 (DEFECT-CANDIDATE paragraph), Gaps 1 and 2, and the Summary: the same two classes are a "DEFECT-CANDIDATE", and `agent_wait_since` is "DEFECT-CANDIDATE (low)".
- research-notes.md line 86 (the C8 rule) tells agents to look for the cited scope decision in "docs/designs/orchestrator-mode.md Phase 1 limits, SKILL.md 'not observed in Phase 1'" and to record DEFECT-CANDIDATE only "if none is found". 04 quotes exactly those texts (sweep.md:16, SKILL.md:26, report.py:42-45, design :493, D7) and still labels the item a defect candidate, so it misapplies the rule.
- 04 "Stale Documentation Found" says D7 "lives at `design-base.md:813`" and that line 813 of the shipped design is a different row. Snapshot check: grep of `/home/coder/.cache/ic-snap-20261120/master/docs/designs/orchestrator-mode.md` for `D7` hits line 841 (`| D7 | Rule 5 at line 253 reads only ...`, with "Update 2026-11-16"), line 636 (`(SP-24, D7)`) and line 877 (`| SP-24 | Applied as D7 ...`). So D7 is in the shipped design at 841, as 03 says; 04's drift entry is wrong. 04 also did not read the SPEC (03 reads it from `origin/master`).
- research-notes.md line 126 requires Section 14 to carry the C8 analysis for stalled (proved) and fenced. With these two files an assembler will print contradictory determinations.

Remediation brief: add one reconciliation paragraph to `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/research-notes.md` (or an addendum file in `research/`) that states one determination each for stalled (proved), fenced, `agent_wait_since`, Safe to close and Removable, citing SPEC lines 106, 231-232, 251, 274, 338 and design lines 493, 636, 841, 877 (as in 03 section 8), and that keeps the residual owner-facing facts 03 lists (no work item owns the source mapping; CHANGELOG.md:170 and docs/user-guide/commands.md:620 give a different reason and wrongly say `working` is never produced). Correct 04's D7 location and drop its "D7 line drift" stale-doc entry.

### F-2 (BLOCKING; cross-cutting questions (v) and (vi)) No research file covers the orchestrator design's own overlap with these tools

Evidence:
- Question (vi) asks what Clay's orchestrator design "would meet". The only research on `docs/designs/orchestrator.md` is 05, which reads that design for the agent-work-report skill, the entry-file writer and the PR chain. 05 Gap 19 says the owner-decision rows (lines 1146-1216) and the UNVERIFIED rows (1253-1320) "were read only for U13, U17, U27, U38, OD6". A grep of the six research files for `FR-9`, `follow-up state`, `claimed-missing` and "is the coordinator" returns no hit (only `projection.attention` in 06).
- Snapshot facts that bear on (v) and (vi) and are absent from the research:
  - `docs/designs/orchestrator.md:930`: "FR-5, FR-6, FR-8, FR-9, FR-21, FR-22 and FR-26 to FR-28 are cited by this design and not changed: the orchestrator is the coordinator they describe." So the WC-16 duty (run `/sc:sweep` on every coordinator wake) would bind the orchestrator, not only a person-opened coordinator. 04 section 6 never connects WC-16 to the orchestrator.
  - Lines 560, 572, 648, 666, 712, 744, 1105, 1134: the orchestrator sorts each worker it started into an "FR-9 state" (working, question, gated, delivered, claimed-missing, stalled, failed, not-started) from `orca orchestration worker-list --run <id> --json` (`projection.liveness`, `attention`, `nextAction`), plus `worker-show --dispatch`, `worker-read --source transcript`, `orca terminal list --worktree path:<repo> --json` and `ccsession --list`. That is a fourth status vocabulary over the same data the observer reads (`worker-list`) and the sweep reads (`worker-list`, `worker-show`), and it names `projection.attention`, which 06 section 6.2 records as present in the live sample, not parsed by the observer, and of unverified meaning.
  - Lines 116-119, 135, 480, 637, 991: the design changes WORKER-CONTRACT.md (adds an "Orchestrated issue flow" section, drops WC-17 and the "Issue pipeline duties" section from line 291). WC-16 sits at WORKER-CONTRACT.md:287-289 (04 section 6.1), directly before that section. No research file records whether the planned edit touches WC-16, WC-10 or the never-as-worker list (which names `/sc:sweep` at :23).
  - A literal search of the design for `/sc:sweep|superclaude sweep|superclaude observe|WC-16|observer` returns no match. The "sweep" hits (lines 122, 298, 313, 387, 422, 657, 803, 913) are the issue poll's own sweep, a "missed-update sweep", a pull-request sweep "not adopted" (803), and a remark that `cli/sweep/probes.py` already uses `yaml` (298). This silence is a fact the owner needs ("the orchestrator design does not reference the sweep, WC-16 or the observer") and it is recorded nowhere.
- Consequence: question (vi) is answerable for the WC-16 half only, and the "overlaps in status classification" part of question (v) lists three vocabularies where the repository's own design records a fourth.

Remediation brief: one Doc Analyst agent, read-only, reads `/home/coder/.cache/ic-snap-20261120/master/docs/designs/orchestrator.md` (sections 4.x, 5.1-5.9, 6.x and the lines 116-119, 135, 480, 560, 572, 637, 648, 666, 712, 744, 930, 991, 1105, 1134) and writes `research/07-orchestrator-design-overlap.md` with: (a) every Orca verb and argv the orchestrator is designed to call, set against the observer's three templates and the sweep's ten; (b) the FR-9 state set and its mapping to `worker-list` fields; (c) a statement, with grep evidence, of whether the design references `/sc:sweep`, WC-16, WC-10, the never-as-worker list, the observer or `.dev/sweeps`; (d) exactly which WORKER-CONTRACT.md lines the design changes or removes, and whether WC-16 (287-289) is among them; (e) what the design says the orchestrator does at wake and how that relates to the coordinator "The sweep" (WORKER-CONTRACT.md:110); facts only, no recommendation.

### F-3 (BLOCKING; check 2 and the Extension Guide scenarios "add a sweep class" and "add an observer panel") Public entry-point signatures and the rule contract are not captured

Evidence: see Check 2. Verified in the snapshot: `collect(ctx: SweepContext, runs: tuple[str, ...], root: Path, budget: Budget) -> SweepInput` (probes.py:1322-1324), `classify(row: SessionRow, ctx: SweepContext) -> Classification` (classify.py:369), `classify_all(inp: SweepInput, ctx: SweepContext) -> SweepResult` (classify.py:880), `render(result, ctx) -> str` (report.py:608), `to_json(` (report.py:613), `_publish(text: str, output_dir: Path, now: datetime) -> Path` (commands.py:153), `build_view(result: Any, session: Session, clock: Any) -> View` (view.py:968), `render(view: View, policy: TerminalPolicy, message: str | None = None) -> Group` (render.py:1449), and `RULES` as a tuple of `Rule(name, match)` (classify.py:345-355). The research files give none of these parameter lists. Adding a sweep class needs the rule contract (`match(row, ctx)` returns a `Classification` or None; the `_classification(...)` helper; the `Classification` fields). Adding an observer view element needs the `View` field list.

Remediation brief: one Code Tracer pass (read-only, about 40 lines of reading) that adds a "Public entry points" table to `research/03-sweep-classifier-joins.md` (or 04) and `research/02-observe-interaction-gates-docs.md` (or 01): for each of `collect`, `classify`, `classify_all`, `Rule`, `_classification`, `Classification`, `SweepResult`, `SessionRow`, sweep `render`, `to_json`, `_publish`, `LiveSource.read_pages`, `Collector.__init__`, `build_view`, `View`, observer `render`, the exact parameter list, return type and file:line from `/home/coder/.cache/ic-snap-20261120/master`.

### F-4 (BLOCKING; check 1, dashboard-design subject) No verified trace of the design package's own fixture-to-export pipeline

Evidence: see Check 1 row DSN. The research-notes synthesis mapping (research-notes.md line 94) requires a "fixture -> renderer -> exports" data flow in Section 4, and Section 3 needs the package tree with roles. 06 gives counts and fixture keys but not how `exports/`, `contact-sheet.png`, `portfolio.pdf`, `manifest.json` and `gallery.html` are produced, which call writes which suffix, what `--batch 2` changes (the `agent-focus/` set), or the three documented commands (package README.md:24-26). The only source is scope/04, which is an unverified starting map.

Remediation brief: one Code Tracer pass over `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/{render.py,fixtures.py,canvas.py,layouts/}` (about 400 lines) that adds a "Package pipeline" section to `research/06-dashboard-design-vs-observer-gaps.md`: argparse flags and defaults (render.py:127), the call chain `designs` -> `screen` -> layout function -> `Canvas` -> `exports` -> contact sheet -> `portfolio.pdf` -> `manifest.json` -> `build_gallery`, output suffixes per call with lines, how `--batch 2` selects `agent_focus.py` and `agent-focus/`, `write_fixtures` inputs and outputs (`fixture.json`, `scenarios/`), and the test entry (`tests/test_designs.py`, `tests/test_gallery.cjs`). Mark commands as not run.

### Minor notes (never fail the gate)

- N-1: 04 Gaps 6 and 7 phrase data-availability facts with "would need"; neutral enough, but synthesis should keep the facts and drop the modal verb.
- N-2: line counts differ by one between research-notes (adapter 512, parse 835, collector 361) and 01 (513, 836, 362), a trailing-newline effect. 02 counts 41 directory entries in `tests/observe` against 36 test files in research-notes; the difference is helper scripts and golden files. Synthesis should say which it means.
- N-3: AWR `config.json` keys are mentioned piecemeal in 05 but never tabulated; Section 9 needs the table. Snapshot check of `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/agent-work-report/config.json`: 14 keys (`person`, `person_name`, `orgs`, `excluded_repos`, `timezone`, `daily_run_local`, `report_days`, `missed_run_dm_local`, `time_budget_minutes`, `session_tag`, `automation_prefix`, `clickup_user_id`, `clickup_email`, `priority_labels`). `CONFIG['session_tag']` is read at waker.py:175, 273, 362 and `CONFIG['person_name']` at classify.py:35, 62; a grep for `CONFIG[...]` reads of `clickup_email` and `clickup_user_id` found none (a fuller grep is needed before the table says "unused").
- N-4: 05 section 9 does not name the Orca terminal fields (`tabId`, `leafId`, `handle`, `worktreePath`, `connected`, `lastOutputAt`) that form the AWR terminal-to-transcript join key (sessions.py:323-330); useful for the "two different join keys" statement.
- N-5: sanitizers are compared in prose for observer and sweep (02 3.4, 04 3.3); AWR `activity.clean` and `common.safe_title` are described only as "control characters removed", without the Unicode categories or escape forms handled.

---

## Verdict

**Overall Verdict: FAIL** (4 blocking findings F-1 to F-4; 5 minor notes). The observer, sweep and AWR traces are deep and every spot-checked claim was accurate (see Self-Audit); the blocking items are a cross-file contradiction, one uncovered neighbour (the orchestrator design), missing signature tables, and the design package's own pipeline.

## Summary
- Checks passed: 3 / 8 (checks 3, 6 and 8; check 6 carries note N-1 and check 8 has one PARTIAL row, DSN, whose cause is F-4)
- Checks failed or partial: 5 (1 DSN gap; 2 SWP gap; 4 (v) and (vi) partial; 5 SWP partial from the 03/04 contradiction; 7 two scenarios partial)
- Blocking findings: 4 (F-1 contradiction, F-2 uncovered orchestrator-design overlap, F-3 missing signatures, F-4 missing design-package pipeline)
- Minor notes: 5 (N-1 to N-5)
- Issues fixed in-place: 0 (fix authorization false; no research file modified)

## Inherited Structural Verdict
No `## Inherited Structural Verdict` section was in the instruction; standalone behaviour applied. Structural checks were left to the other QA agents as instructed.

## Self-Audit

**(a) Reliance list:** none. No structural PASS was relied on; the file-exists and section checks were not repeated and were not needed for a depth review.

**(b) Independent semantic checks (tool evidence):**
- Contradiction 03 versus 04 on C8: read both files in full and confirmed the D7 location in the shipped design by grep (`orchestrator-mode.md:841`, 636, 877) and the absence of any producer by grep of `src` for `worker_done_seen|fenced_evidence` (only models.py:108-109 and classify.py:198-222).
- Orchestrator design coverage: grep of `docs/designs/orchestrator.md` for `FR-9`, `sweep`, `WC-16`, `observer`, `WORKER-CONTRACT` (hits at lines 560, 572, 648, 666, 712, 744, 930, 1105, 1134 and 116-119, 135, 480, 637, 991) against a grep of the research directory for the same terms (no hit).
- Signatures: grep of `^def (classify|classify_all|collect|render|to_json|_publish|bind_run|build_view|read_pages)\(` in `src/superclaude/cli/{sweep,observe}` and Read of probes.py:1322-1324 and classify.py:336-387, set against a grep of the research files for the same names.
- Design-package pipeline: grep of `render.py` in the package (lines 2-12, 20-72, 77, 124, 127) set against a grep of research and scope for `--batch|--show|build_gallery`.
- Accuracy spot-checks, all matched the research: adapter.py:26-65 (3 templates, 13 forbidden prefixes, caps), probes.py:40-63 (10 templates, `orca-ide` default), classify.py:345-355 (9 rules in the stated order), AWR `config.json` (14 keys), orca_term.py:12-133 and page.py:350-378 (verbs and argv), sessions.py:318-347 (join key), scope/04 lines 18-37.

**Claims independently verified against source:** about 30 (Orca templates, forbidden list, caps, rule order, producer absence, D7 line, AWR verbs and join key, config keys, orchestrator-design mentions, entry-point signatures, renderer functions). Not verified: the several hundred remaining file:line citations in the six files (that is the evidence gate's work, not this lens); live Orca behaviour; GitHub PR states.

**If zero issues had been found:** not applicable; four blocking findings were found, each with a snapshot or file citation.

**Web research:** none performed (all subjects are in-repo); no Tavily or fallback calls.

## Confidence and tool engagement
- **Confidence:** Verified: 8/8 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% for the review of the eight checks (each check was evaluated per subject with tool evidence). This does not claim that every citation inside the research files is correct.
- **Tool engagement:** Read: 29 | Grep: 25 | Glob: 1 | Bash: 0. Read plus Grep plus Glob (55) is above the 8 checklist items.
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Recommendations
- Run one gap-filling round before synthesis: F-1 (reconcile, no new reading beyond 03 section 8), F-2 (new `research/07-orchestrator-design-overlap.md`), F-3 (signature tables), F-4 (package pipeline section). F-1, F-3 and F-4 are short; F-2 is the one that changes what the reference can say to the owner.
- After the fills, re-run only the blocking rows (this is review 1 of at most 3).
- Carry minor notes N-1 to N-5 into the synthesis briefs; they do not need a fix pass.

## QA Complete
