# QA Report - Research Verification, Content Lens (Gate 1 re-check, cycle 1)

**Topic:** Observer, sweep, AWR and dashboard-design technical reference; research gap-filling re-check
**Date:** 2026-11-20
**Phase:** doc-qualitative (research-depth re-check after gap-filling; fix cycle 1)
**Fix cycle:** 1
**Status:** Complete
**Overall Verdict:** PASS (0 open blocking findings, 5 minor notes)

---

## Progress log
- Report created. Condition met: qa-research-consolidated-findings.md states Consolidated verdict FAIL (GF-1 to GF-5).
- Read consolidated findings, depth report, all five `research/gapfill-c1-*.md` files, research-notes.md (C8 rule line 86, questions (i)-(vi) line 77, Section 14 requirement line 126).
- Verified gap-fill claims against snapshot /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6), the origin/master SPEC blob, the design package checkout and read-only `gh pr view`. Results below.
- Checked that the original research files carry pointers (grep `gapfill` over 01-06).

## Per-finding resolution (depth-related blocking findings)

| Consolidated ID | Depth ID | Verdict | Evidence (what I re-read) |
|---|---|---|---|
| GF-1 (C8 contradiction 03 vs 04; D7 location) | F-1 | RESOLVED | `gapfill-c1-GF1-c8-reconciliation.md` states one rule (R-C8, section 2) and a label for every item: stalled, fenced, `agent_wait_since`, Safe to close, Removable = KNOWN LIMIT (cited); living-report writer = KNOWN LIMIT sequenced to PR B; D-1 = DEFECT-CANDIDATE. The cited text exists: SPEC lines 103, 106, 111, 167, 231, 232, 238, 250, 251, 274, 338 and 75/208 re-read with `git show origin/master:...merged-requirements.md \| cat -n`; design D7 at `docs/designs/orchestrator-mode.md:841` (also :636, :877), rule 5 text :493, open item 6 :1003 re-read. D7 location corrected (:841 is the snapshot design; `design-base.md:813` is the task-package copy). Code facts re-read: `models.py:108-112`, `probes.py:481`, `classify.py:229, 251-256`. R-C8 matches research-notes.md line 86 (cited scope decision, else DEFECT-CANDIDATE) and keeps the residual owner facts (no owner of the "source mapping", reason differs from CHANGELOG.md:170, attribution to review inputs). Sections 4 and 5 scope the "no DEFECT-CANDIDATE" lines of 01/02 to live R2/R3, snapshot and `--once`; D-1 verified: `commands.py:77-78, 183-188`, `acceptance-tests.md:25`, `SPEC.md:32`, `release-gates.md:9` re-read on origin/master. 04 line 300 and 06 line 303 now point to the reconciliation and say 04's labels are superseded. |
| GF-2 (commands.md:619-620 misattribution) | (evidence F-2) | RESOLVED | `gapfill-c1-GF2-commands-md-claim.md` re-checked against snapshot: `commands.md:619` gives no reason; `:620` gives the agentWait reason for `working` only; `CHANGELOG.md:170` alone gives it for all three classes. Working is produced (`classify.py:251-256`, rule 5 active; `orchestrator-mode.md:841, 1003`). A verbatim replacement paragraph is supplied. 03 line 316 carries the pointer. |
| GF-3 (orchestrator design overlap, questions (v)/(vi)) | F-2 | RESOLVED | `gapfill-c1-GF3-orchestrator-design-overlap.md` exists (258 lines) and answers each part of the remediation brief. Re-verified: `orchestrator.md` is 1412 lines; DESIGN:930 "is the coordinator they describe"; DESIGN:648 FR-9 eight-state set; DESIGN:572, 744 source fields; DESIGN:3 (approved, ruling 37), :135 ("Everything else in the contract is unchanged"), :510, :791, :1018, :1020-1021, :1041; case-insensitive grep for `/sc:sweep`, `superclaude sweep`, `superclaude observe`, `WC-16`, `observer`, `.dev/sweeps` returns no match; "sweep" occurs on 8 lines (122, 298, 313, 387, 422, 657, 803, 913), none about `/sc:sweep`. PR D diff (`git show 01e7a9e23...`) has hunks at old lines 56, 64, 288 only: WC-17 and "Issue pipeline duties" removed, WC-16 (WC:287-289) untouched; snapshot grep for WC-17 / "Issue pipeline duties" / "Orchestrated issue flow" finds nothing. WC lines re-read: :23 never-as-worker list, :70 "bind the coordinator ... a session the person opened", :101 wait command (9 types, 300000 ms), :105, :110 "The sweep.", :118-129 S0-S11, :137, :196. Sweep allowlist `probes.py:49-60` (10 templates) and observer `adapter.py:29-50` (3 templates, 13 forbidden prefixes) re-read; the four token-for-token matches claimed in the verb table are correct. PR states re-read with `gh pr view --repo IronbellyOrg/IronClaude`: #539, #681, #682, #684, #434 MERGED; #686, #690 OPEN; PR B has no PR (title search). FR-9 mapping and the coordinator spec stay UNVERIFIED (Glob and `git ls-tree origin/master` find no SPEC-AGENT-WORK-COORDINATOR file). |
| GF-4 (public entry-point signatures, rule contract) | F-3 | RESOLVED | `gapfill-c1-GF4-public-entry-points.md` re-verified against the snapshot: `classify` classify.py:369, `classify_all` :880, `Rule` :156 (decorator :155), `RULES` :345-354, `_classification` :130 (not :222: the depth report's cite was wrong and the file says so), `collect` probes.py:1322-1324, `parse_worker_show` :471, `bind_run` :397, `render` report.py:608, `to_json` :613, `_publish` commands.py:153, `run` :242-244, `build_view` view.py:968, `apply_cycle` :1174, `apply_key` :1246, `_questions_panel` :709, `_desk` :888, `_meta` :664, `View` :335, `RowView` :179, `SnapshotMeta` :204, observer `render` render.py:1449, `screen_lines` :1248, `Collector.__init__` collector.py:135, `LiveSource.__init__` adapter.py:349, `read_pages` :395, `read_questions` :469, export.py `_TEXT_FIELDS` :25, `_ANY_FIELDS` :46, `snapshot_dict` :183, `write_atomic` :257. Rule contract re-read at classify.py:369-386 (first non-None wins, fallback, post-processing); positional `CLASSES` unpack classify.py:42-51; `counts` dict :974-976; `report.py:26-27`, `NEXT_INSPECTION` :54, `SECTIONS` :545; test pins (`test_classify.py:351, 375, 379`; `test_report.py:1107-1108`); golden-file constraint (`test_render.py:658, 680-683`). The "add a sweep class", "add an observer panel" and "add a snapshot field" scenarios are now concrete. |
| GF-5 (design package fixture-to-export pipeline) | F-4 | RESOLVED | `gapfill-c1-GF5-package-pipeline.md` re-verified against `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/render.py` (130 lines, read in full): argparse flags and defaults :127, `--show` :128-129 (NO_COLOR presence test), `designs` :20-24, `screen` :26-29, `image` :31-39, `exports` :41-74 (six suffixes :52-57, 160-wide pages :59, contact sheet :61-68, PDF with fixed dates :69-70, fixture hash and manifest :71-72, gallery :73), `build_gallery` :77-124. `write_fixtures` (fixtures.py:114-122) writes 1 + 9 + 9 files; `scenarios/` holds 18 (ls). `agent-focus/` holds contact-sheet.png, exports/, gallery.html, manifest.json, portfolio.pdf (ls); 60 files in each `exports/160`. README lines 24-28 match the commands listed; `tests/test_designs.py` has 19 `def test_`; line counts match `wc -l` (130, 122, 122, 230, 224, 183, 117, 22, 52). Commands recorded as not run. |

Open blocking findings after this check: **0**.

## Cross-cutting questions (i) to (vi), per subject, after gap-filling

OBS = observer (01, 02, GF-4 sec 3-5), SWP = sweep (03, 04, GF-1, GF-2, GF-4 sec 1-2), AWR = agent-work-report (05, GF-3), DSN = dashboard design package (06, GF-5). OK = answerable with file:line citations; the evidence column names where.

| Question | OBS | SWP | AWR | DSN | Where the new material closes the earlier gap |
|---|---|---|---|---|---|
| (i) data sources | OK | OK | OK | OK | DSN adds the synthetic-only source (`fixtures.py:11-87`, no clock, env or network). |
| (ii) output formats and where written | OK | OK | OK | OK | GF-5 sec 3 gives the producing call and line for every export suffix, contact sheet, PDF, manifest and gallery (render.py:52-73). Earlier PARTIAL for DSN is closed. |
| (iii) live versus designed | OK | OK | OK | OK | GF-1 gives one label per capability; GF-3 sec 7 gives built versus designed for the orchestrator chain with PR states re-verified. |
| (iv) consumers | OK | OK | OK | OK | GF-3 sec 6 (last paragraph) records that no sweep, observer or sweep-skill file refers to the orchestrator, poll or entry files. |
| (v) overlaps | OK | OK | OK | OK | GF-3 sec 4 now sets five vocabularies side by side (observer fields, sweep 8 classes, AWR 6 statuses, FR-9 8 states, WC S0-S11) and sec 10 sets Run scoping, files written and join keys. "Waits on a person" in three places and the two terminal-to-transcript join keys still sit in separate files (03 sec 4, 05 sec 9, 01 sec 4); assembling them is synthesis work and is a minor note (M-3 of the consolidated findings), not a research gap. |
| (vi) WC-16 and the orchestrator design | OK | OK | OK | OK | GF-3 sec 5-6 states what the design changes in WORKER-CONTRACT.md (PR D done; PR B "Orchestrated issue flow" not built; WC-16 not touched), that the design never names `/sc:sweep`, WC-16 or the observer, that DESIGN:930 calls the orchestrator "the coordinator", and a side-by-side of the orchestrator wake loop against "The sweep." (WC:110) and WC-16 (WC:289). Whether WC-16 binds a script-started orchestrator is recorded as UNVERIFIED with the reason. |

## Live-versus-designed accuracy and neutrality

- Accuracy: every live/designed statement I sampled matches code or text. Stalled and fenced have no producer on live rows (`models.py:108-109` defaults; `probes.py:471-515` sets neither; `classify.py:196-200`, `:219-223`); `working` is produced since 2026-11-16 (`classify.py:251-269`; `orchestrator-mode.md:841, 1003`); the CHANGELOG and commands.md statements are correctly tagged STALE DOC with the exact stale clause; the orchestrator package, `/sc:orchestrator`, `superclaude orchestrator report-entry` and PR B are tagged DESIGN-ONLY (`ls src/superclaude/cli` has no `orchestrator`; PR B has no pull request); PR #686 and #690 are tagged open and are open.
- Neutrality: no gap-fill file recommends how the orchestrator design is unified with the observer, sweep or report. GF-3 sec 9 raises WC-16 versus the design as an "open question of scope" with a conditional fact and states "No unification is recommended here". GF-1 sec 3.8 puts a question to the owner as a fact. The R-C8 rule is a labelling test, not a recommendation, and the two judgments that could flip a label (review inputs versus a dated owner ruling; a PR-sequencing line as a scope decision) are stated with "the label flips and no fact changes" (GF-1 Gaps 2 and 3). Both stay visible to the owner.
- New defects introduced by the gap-filling: none that is blocking. I looked for contradictions between the five gap-fill files and between them and files 01-06: GF-1's labels agree with 03 (sec 8) and override 04 (04 line 300 says so); GF-3 sec 9's "no DEFECT-CANDIDATE raised" does not conflict with GF-1 sec 3.7 (GF-3 explicitly leaves the AWR writer to GF-1); GF-4 corrects the depth report's `_classification` cite (:222 -> :130) and GF-4 Gap 8 agrees with GF-1 on the `agent_wait_since` label; GF-5's "no DEFECT-CANDIDATE" for the package pipeline does not touch D-1 (a different path, the observer CLI `--fixture`, stated in GF-1 sec 3.8).

## Minor notes (not blocking; not rechecked in later rounds)

1. GF-3 sec 2 says the pattern `sweep` "gives 9 line hits" but lists 8 lines (122, 298, 313, 387, 422, 657, 803, 913); the file has 8 matching lines (grep count 8). Carry "8 lines".
2. The original research files keep their old labels in the body and rely on a trailing pointer: 04 lines 185, 189, 191, 276, 277 still say DEFECT-CANDIDATE (04 line 300 says superseded); 05 lines 317 and 578 still say DEFECT-CANDIDATE for the writer; 01 line 153/356 and 02 line 173/291 still say "no DEFECT-CANDIDATE" (02 has a pointer for GF-4 only, not GF-1; GF-1 sec 4 holds the scope). The synthesis briefs must name the gap-fill file as the authority for those labels.
3. UNVERIFIED items from the gap-fill files must stay UNVERIFIED in the final reference: FR-9 definitions and the `worker-list`-field mapping (spec not in repo), whether WC-16 binds a script-started orchestrator, how the sweep classifies a live orchestrator session, the IronOrchestrator repo and the `orchestrator-poll` automation, non-null `agentWait` meaning, test pass results (nothing was run), README.md:44 of the package.
4. GF-3 sec 7 and GF-1 sec 3.7 name PR states as of 2026-11-20 (#686 and #690 open, PR B none); state the date wherever they are used.
5. Consolidated minor findings M-2 to M-17 were not rechecked (per the severity rule); M-1 is covered by GF-1 sec 4.

## Verdict

**Overall Verdict: PASS** (0 open blocking findings; 5 minor notes).

All five consolidated blocking findings (GF-1 to GF-5; depth F-1 to F-4 plus the evidence-lens GF-2) are resolved with evidence I re-read at the cited lines. The six cross-cutting questions are now answerable for every subject; live-versus-designed statements are accurate and neutral; no new blocking qualitative defect was introduced.

## Summary
- Checks passed: 14 / 14 (5 resolutions, 6 cross-cutting questions, live-versus-designed accuracy, neutrality, new-defect scan)
- Checks failed: 0
- Critical issues: 0
- Blocking findings open: 0
- Issues fixed in-place: 0 (fix authorization false; no file other than this report was written)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR | gapfill-c1-GF3-orchestrator-design-overlap.md sec 2 | "9 line hits" for `sweep`; 8 lines listed and present | Carry "8 lines" into synthesis |
| 2 | MINOR | research/04 lines 185, 189, 191, 276, 277; 05 lines 317, 578; 01/02 "no DEFECT-CANDIDATE" lines | Old labels remain in the body, superseded only by a trailing pointer | Synthesis briefs cite gapfill-c1-GF1 as the authority |
| 3 | MINOR | final reference, UNVERIFIED items | Items listed in note 3 must not be promoted to facts | Keep the UNVERIFIED tags |

## Actions Taken
None. Report only. No source, design or research file was modified. No staging or commit. GitHub access was read-only `gh pr view/list --repo IronbellyOrg/IronClaude`; nothing touched SuperClaude-Org.

## Self-Audit

No `## Inherited Structural Verdict` section was in the instruction; standalone behaviour applied.

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:** none. I relied on no earlier PASS. I did rely on the earlier FAIL reports only as the list of defects to resolve.

**(b) Independent semantic checks (tool evidence):**
- C8 reconciliation: re-read SPEC lines 75, 103, 106, 111, 167, 208, 231, 232, 238, 250, 251, 274, 338 with `git show origin/master:...merged-requirements.md | cat -n`; design D7 lines 493, 494, 841, 1003 and grep for D7/SP-24 (:636, :841, :877); code `classify.py:229, 251-256`, `models.py:108-112`, `probes.py:481`. All matched GF-1.
- Orchestrator-design overlap: case-insensitive grep of `orchestrator.md` for the sweep/WC-16/observer/`.dev/sweeps` terms (no match) and for `sweep` (8 lines); Read of DESIGN:572, 648, 930; `sed` of DESIGN:3, 135, 372, 374, 534, 744, 791, 1018, 1020, 1021; `git show 01e7a9e23...` hunk headers; WC grep (:23, :41, :70, :101, :105, :110, :118-129, :137, :196, :287-289); `gh pr view` for 7 PRs. All matched GF-3.
- Entry points: grep of `def`/`class` definitions in classify.py, probes.py, report.py, commands.py, view.py, render.py, collector.py, adapter.py, export.py plus Reads of classify.py:40-54, 366-387, 972-978; test greps in tests/sweep and tests/observe. All matched GF-4; `_classification` is at :130.
- Package pipeline: full Read of `render.py` (130 lines) and fixtures.py:108-122; `wc -l`, `ls` and `grep -c def test_` over the package. All matched GF-5.
- Where rf-qa PASS would not have been enough: the consolidated findings are defects, so I checked content, not structure. The one place the earlier QA text was itself wrong and the gap-fill corrected it: `_classification` at :130 (depth report said :222).

**Claims independently verified against source:** about 85 (SPEC and design lines, code definitions and line numbers, PR states, package counts, grep absence claims).
**Not verified:** the several hundred other file:line citations inside files 01-06 and the gap-fill files (evidence-gate work; I sampled the ones the findings depend on); live Orca behaviour; whether the package's checked-in exports match the current `render.py` bytes (nothing was run); the FR-9 spec (not in any reachable tree).
**If zero issues had been found:** not applicable; five minor notes recorded, each with a location.
**Web research:** none (all subjects are in-repo); no Tavily or fallback calls.

## Confidence and tool engagement
- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The figure covers the 14 re-check items, not every citation inside the research files.
- **Tool engagement:** Read: 20 | Grep: 25 | Glob: 2 | Bash: 8. Read plus Grep plus Glob (47) exceeds the 14 checklist items.
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Recommendations
- Proceed to Step 3.5 / synthesis: Gate 1 passes on the research-depth lens at review 2 of at most 3. Pass the five gap-fill files to every synthesis brief and name `gapfill-c1-GF1-c8-reconciliation.md` as the authority for every C8 label.
- Keep the minor notes above as correction lines in the synthesis briefs.

## QA Complete
