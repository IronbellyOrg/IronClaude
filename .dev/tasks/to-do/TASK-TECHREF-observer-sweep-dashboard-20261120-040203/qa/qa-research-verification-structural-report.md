# QA Report - Research Gap-Fill Verification (structural, fix-cycle 1)

**Status:** Complete
**Phase:** fix-cycle (research-gate verification)
**Date:** 2026-11-20
**Fix authorization:** false (report only)
**Snapshot:** /home/coder/.cache/ic-snap-20261120/master
**Previous report:** qa/qa-research-consolidated-findings.md (|F_1| = 5: GF-1 .. GF-5)

## Overall Verdict: PASS (with minor notes)

All 5 previously blocking findings (GF-1 to GF-5) are RESOLVED with file:line evidence read by me; 0 new blocking findings; `|F_2|` = 0 against `|F_1|` = 5. Gate 1 may proceed to synthesis. The synthesis must follow the gap-fill files where they supersede the original research bodies (note N-1).

## Per-finding verification

Method: I read the consolidated findings, all five `research/gapfill-c1-*.md` files and the cross-reference lines appended to research files 01 to 06, then re-read the cited source myself from the snapshot, from `git show origin/master:<path>` blobs, from the design package in the checkout, and from read-only `gh pr list --repo IronbellyOrg/IronClaude`. Nothing was run.

### GF-1 (C8 / DEFECT-CANDIDATE reconciliation) - RESOLVED
Required: one reconciliation stating the single rule and the resulting label plus citation for stalled (proved), fenced, `agent_wait_since`, Safe to close, Removable, the living-report writer (05), D-1 (06); the scope of 01/02 "none"; residual owner facts; 04's D7 location.
- Deliverable exists: `research/gapfill-c1-GF1-c8-reconciliation.md` sections 2 (rule R-C8), 3.1-3.8 (one label plus citation each), 4 (scope of 01/02 "none"), 5 (correction table). All seven items named in the finding are present.
- SPEC citations re-read from the origin/master blob (`git show ... | cat -n`): line 232 ("Stalled (proved) stays fixture-only until a source mapping exists"), 231, 251 ("synthetic fixtures only in Phase 1"), 238 ("UNVERIFIED field ... unknown-age group"), 106 (FR-012), 111, 167, 274, 338, 103. All match the quoted text. "source mapping" occurs once in the SPEC (line 232), as GF-1 states.
- Design lines (snapshot `docs/designs/orchestrator-mode.md`): 493 (Rule 5, `worker_done_seen` None and `fenced_evidence` unreadable on every live row), 636 (footnote "Stalled and fenced are not observed in Phase 1 ... (SP-24, D7)"), 841 (D7 row, grep hit), 877 (SP-24 panel-notes row). All match. D7 correction confirmed: `origin/master:.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/design-base.md` line 813 is the D7 row, so 04's citation is accurate for that file and the snapshot design has D7 at :841.
- Code: `classify.py:191-208` (`_exit_proof` needs `worker_done_seen is False` and `fenced_evidence == "absent"`), `:219-223`, `:226-236` (`since = orca.agent_wait_since  # reserved`), `:251-269` (rule 5 active); `models.py:108-112`. Grep for `worker_done_seen|fenced_evidence|agent_wait_since` over the snapshot returns exactly 8 files (design doc, classify.py, models.py, probes.py, report.py, three test files), matching the "only test fixtures produce them" claim. No `"yes"` literal in classify.py, matching "no branch returns yes".
- Living-report writer (3.7): `ORCH` (`docs/designs/orchestrator.md`) line 3 (approved by Clay, ruling 37), 510 (`cli/orchestrator/` package, new, PR B, verb list includes `report-entry`), 791, 1018, 1020, 1021, 1041, 372, 374 all read and match. `src/superclaude/cli/` has no `orchestrator` entry; no `sc-orchestrator-protocol` skill and no `orchestrator.md` command in the snapshot. `refs/settle.md:99` text matches. `agent-work-report/SKILL.md:14-16` describes the entry files in the present tense. PR chain re-read with `gh`: #686 and #690 OPEN, #684 MERGED 2026-11-20T02:01:07Z; no PR for PR B in a title search.
- D-1 (3.8): `observe/commands.py:183-188` (`_question_refusal` returns exit 2 when `options.fixture`), `collector.py:125-129` (`read_questions` returns `FAILED` code `no-question-fixture`), `acceptance-tests.md:25` (T7 "not built / no automated test ... `_question_refusal`"), `SPEC.md:32`, `release-gates.md:9` all re-read from origin/master blobs and match. The label stays DEFECT-CANDIDATE with an explicit "text of absence only" reason.
- Amendment to research files: pointer lines appended to 01 (line 371), 04 (line 300), 05 (line 615), 06 (line 303), each naming the gap-fill file; 04's pointer states "this file's DEFECT-CANDIDATE labels are superseded by it".
- Result: RESOLVED.

### GF-2 (commands.md:619-620 misattribution) - RESOLVED
- `docs/user-guide/commands.md:619` read: states the limit and the mark, gives no reason. `:620` read: gives the `agentWait`-capture reason for `working` only. `CHANGELOG.md:170` read: one "because" clause after all three classes. `CHANGELOG.md` heading at line 69 is `## [6.0.0] - 2026-11-18` (grep), so the section claim holds.
- Staleness claim: `classify.py:251-269` produces `working` from live fields; `tests/sweep/test_cli_contract.py:1133` is `test_a_captured_running_worker_is_reported_as_working`; design `:1003` / `:877` per the gap-fill. Narrowed claim in `gapfill-c1-GF2-commands-md-claim.md` section 1 and 2 matches what I read.
- Pointer appended to 03 line 316 ("claim ... is narrowed to CHANGELOG.md:170"). Note: the original 03 body line 248 (s8.1 point 3) still carries the old wording; see minor note N-1.
- Result: RESOLVED.

### GF-3 (orchestrator design overlap, new gap-fill) - RESOLVED
Required: Orca verbs vs the observer's 3 and sweep's 10 templates; FR-9 set and mapping; grep evidence for `/sc:sweep`, WC-16, WC-10, never-as-worker, observer, `.dev/sweeps`; exact WORKER-CONTRACT.md lines changed; wake behaviour vs "The sweep." (WC:110); built vs designed; facts only.
- Deliverable exists: `research/gapfill-c1-GF3-orchestrator-design-overlap.md` sections 2 (grep), 3 (35-row verb table), 4 (FR-9), 5 (contract edits and WC-16), 6 (wake vs sweep), 7 (built vs designed), 8 (PR chain).
- Grep evidence re-run: `/sc:sweep|superclaude sweep|superclaude observe|WC-16|observer|.dev/sweeps` over `docs/designs/orchestrator.md` returns zero hits; "sweep" appears on lines 122, 298, 313, 387, 422, 657, 803, 913 and none is `/sc:sweep`. `projection`, `liveness`, `attention`, `nextAction` appear only on line 572; `claimed-missing` is on line 648 with the eight-word set; line 930 contains "the orchestrator is the coordinator they describe". Matches the file.
- Verb table checked against allowlists: sweep `probes.py:49-60` (10 templates; template 1 is `run-current` without `--json`; `task-list --run <run> --json` is line 54; `worktree current --json` line 57 pinned) and observer `adapter.py:29-50` (3 templates, forbidden prefixes) match the table's Obs/Swp columns.
- WORKER-CONTRACT: `WC-16` heading at :287 and text :289, "The sweep." at :110, never-as-worker list at :23 (includes `/sc:sweep`), `:70` coordinator is "a session the person opened", `:101` nine-type wait at 300000 ms, `:105`, `:112`, `:122`, `:137`, `:188`, `:196` read and match. No `WC-17`, `Issue pipeline duties` or `Orchestrated issue flow` in the snapshot file. PR D diff (`git show 01e7a9e23...`) shows deletions of the WC-17 bullet and the "Issue pipeline duties" section; WC-16 text appears only as hunk context (hunk `@@ -288,17 +288,6 @@`), so "WC-16 not touched" holds.
- No orchestrator, `sc-orchestrator-protocol` or `orchestrator.md` command in the snapshot; grep of `cli/sweep`, `cli/observe`, `skills/sc-sweep-protocol` for orchestrator/issue-watch/report-entry terms returns no match. PR states (#539, #681-684 merged, #686/#690 open, #434 merged) match `gh`.
- Unknowns stay UNVERIFIED (FR-9 per-state definitions, whether WC-16 binds a script-started orchestrator); no unification recommendation. The one scope question is raised as an open question for the owner, not as a defect, with a stated reason (the orchestrator is not built).
- Pointers appended to 04 (line 302) and 05 (line 617).
- Result: RESOLVED.

### GF-4 (public entry-point signatures) - RESOLVED
- Deliverable exists: `research/gapfill-c1-GF4-public-entry-points.md` (sections 1-6).
- Signatures re-read from source and matching exactly: `collect(ctx, runs, root, budget) -> SweepInput` probes.py:1322; `classify(row, ctx) -> Classification` classify.py:369; `classify_all(inp, ctx) -> SweepResult` :880; `Rule(name, match)` :156-158; `RULES` (9 entries) :345-355; `_classification` :130 (the depth report's `:222` was wrong, as GF-4 says); `_force_unknown` :358; `policy_of` :389; `package_state` :423; `mark_shared_packages` :432; `removable` :455; `safe_to_close` :479; `render` report.py:608; `to_json` :613; `_publish` commands.py:153; `run` :242; `Budget.__init__` probes.py:127; `bind_run` :397; `parse_worker_show` :471; observer `build_view` view.py:968; `apply_cycle` :1174; `apply_key` :1246; `render` render.py:1449; `screen_lines` :1248; `_compose` :1258; `Collector.__init__` collector.py:135-145 (8 parameters as listed); `LiveSource.read_pages`/`read_questions` adapter.py:395/469; `execute` commands.py:412; `run_loop` :306.
- Rule contract and registration: `classify.py:42-51` positional unpack of `CLASSES`; `classify.py:974-976` counts dict built from `CLASSES`; `report.py:26-27` `_IDLE = CLASSES[5]`, `_UNKNOWN = CLASSES[7]`; `report.py:687` counts from `CLASSES`; `NEXT_INSPECTION` :54; `SECTIONS` :545; test pins at `test_classify.py:277, 351, 375`, `test_report.py:1091, 1107-1108` verified. The one inference (a ninth `CLASSES` entry breaks the unpack) is labelled as derived from Python semantics, not run.
- Extra contracts checked: AWR `run.py:868-887` dispatch table matches exactly (eight subcommands, argv lengths, `sys.exit(__doc__)`); `export.py` `_TEXT_FIELDS` :25, `_ANY_FIELDS` :46, `_KEY_OF_ATTR` :47, `snapshot_dict` :183, conditional `questions` :207 and `collection` :209; `snapshot.schema.json` `additionalProperties: false` on the root and nested objects, `schemaVersion` const 1; `test_render.py:655-695` golden "never regenerated" text; `test_snapshot_schema.py:424`.
- Pointers appended to 02 (line 307) and 03 (line 314); 03's pointer carries the `_classification` line correction.
- Result: RESOLVED.

### GF-5 (design package fixture-to-export pipeline) - RESOLVED
- Deliverable exists: `research/gapfill-c1-GF5-package-pipeline.md` (flags, call chain, `exports` step table, `build_gallery`, `fixtures.py`, `--batch 2`, tests, README commands, hop list). Commands marked not run.
- `render.py` re-read: flags at :127 (`--batch` choices 1,2 default 1; `--show`; `--width` default 116), branch :128-130, `designs` :20-24, `screen` :26-29, `exports` :41-74 (six suffixes :52-57, contact sheet :61-68, PDF :69-70 with epoch dates, fixture hash :71, manifest :72, gallery :73). `fixtures.py:114-122` writes `fixture.json` plus 9 variant files plus 9 scale files; `scenarios/` holds 18 files on disk. Line counts from `wc -l` match (130, 122, 122, 230, 224, 183, 117, 22, 52). `requirements.txt` is Pillow 13.0.0 and wcwidth 0.9.4. `tests/test_designs.py` has 3 classes and 19 `def test_` methods. `README.md:24-28` commands match the table (lines 24-26 python, 27-28 node). `agent-focus/` contains contact-sheet.png, exports/, gallery.html, manifest.json, portfolio.pdf.
- Pointer appended to 06 (line 303).
- Result: RESOLVED.

## New-issue and regression check (gap-filling introduced nothing blocking)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | False claims in the five gap-fill files | none found | Every `file:line` I sampled (about 120 citations across SPEC blobs, snapshot code, design, contract, package) matched. The sampled claims that could have failed (grep zero-hit statements, "only producers are tests", PR states, `WC-16` untouched by PR D) were re-run and held. |
| 2 | Wrong citations | none blocking | Only cosmetic count slips, see N-2 and N-3. The one wrong citation in the earlier QA (`_classification` at :222) was corrected by GF-4 to :130, which I confirmed. |
| 3 | Missing required deliverable | none | All five required files exist, each with Status Complete, and each finding's remediation list is covered (checked per finding above). |
| 4 | Contradiction between gap-fill files | none | GF-1's labels agree with GF-4's Gap 8 and Stale Docs note (which defers to GF-1), with GF-3 section 9 (WC-16 question is an open question, not a defect) and with GF-2's reading of `CHANGELOG.md:170`. |
| 5 | Regression (an earlier passing item now failing) | none | Research files 01-06 only gained appended pointer lines (grep for `gapfill` shows one or two lines per file, all at the end of the file); no earlier body text was removed or altered. UNVERIFIED tags carried over unchanged (agentWait non-null meaning, FR-9 definitions, orchestrator repo, automations). |
| 6 | Safety rules of the brief | held | The gap-fill agents report read-only work. GF-1 states the SPEC was read through `git show | cat -n` with no scratch copy, which answers minor finding M-11. No SuperClaude-Org access appears in any file; the `gh` calls cited use `--repo IronbellyOrg/IronClaude`. I did not find any staged or committed change. |

## Counts

- Previous blocking findings `|F_1|` = 5 (GF-1 to GF-5).
- Resolved: 5. Still open: 0.
- New blocking findings introduced by the gap-filling: 0.
- Open blocking findings `|F_2|` = 0. `|F_2| < |F_1|` holds (0 < 5). No regression, so the monotonicity guard and the 2-cycle cap are not triggered.

## Minor notes (not blocking, not rechecked in later rounds)

| ID | Where | Note |
|----|-------|------|
| N-1 | research/03 body (s8.1 point 3 at line 248; Takeaways; Gaps 4), research/04 Summary (line 297) and Gaps 1-2, research/05 Gaps item 1 | The original text is still in the files; only appended pointer lines supersede it. The synthesis must follow the gap-fill file where they differ (the pointers say so). |
| N-2 | gapfill GF3 section 2 | Says "9 line hits" for `sweep` but lists 8 lines; line 422 has two occurrences. |
| N-3 | gapfill GF4 section 1.3 point 4 | Leftover phrase "(To be completed in section 2 below ...)"; section 2 item 9 does cover the report.py uses. |
| N-4 | gapfill GF3 section 5 | The PR D hunk headers are written as `@@ -59 +58,0 @@`-style; the real diff headers are `@@ -56,7 +56,6 @@`, `@@ -64,6 +63,7 @@`, `@@ -288,17 +288,6 @@`. The conclusion (WC-16 untouched) is unaffected. |
| N-5 | gapfill GF1 sections 3.2, 3.7 | The two judgment calls (does a PR-sequencing line count as a scope decision; does a review-input statement count as an owner ruling) are stated as owner questions with the label-flip consequence; keep that wording in the final document. |
| N-6 | all | Carry forward the earlier minor findings M-1 to M-17 from the consolidated file; M-11 is answered by GF-1's statement of no scratch copy. |

## Confidence Gate

Checklist items: 5 previously blocking findings plus 4 new-issue checks (false claims, wrong citations, missing deliverables, regression) = 9. All 9 marked VERIFIED with tool output cited above. UNVERIFIABLE: 0. UNCHECKED: 0.

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 19 | Glob: 2 | Bash: 8 (every call targeted a specific citation or claim above)
- Limits of this review (not blocking): I sampled citations rather than re-reading every line number in the 35-row GF-3 verb table, the GF-4 test-file line numbers beyond those named, or the PR #539 body claims; the five gap-fill agents' statements that nothing was run could not be audited by me. Items they mark UNVERIFIED were left UNVERIFIED.
