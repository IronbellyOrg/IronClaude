# Research Completeness Verification (Gate 1, Partition B)

**Topic:** which ONE unified central Review Panel (shared core plus thin modules) captures all the value of E1, E2 and E3
**Files reviewed:** research/09-*.md through research/16-*.md (8 files: 09-collaboration-designs, 10-process-redesign, 11-consumers-tasklist-workflow, 12-consumers-spec-review, 13-future-pr-review-and-rfqa, 14-e3-variants-and-experiments, 15-telemetry-manifest-run-record, 16-eval-governance)
**Lens:** completeness (coverage, completeness, cross-reference) plus gate focus (a)-(e)
**Depth tier:** Deep
**Date:** 2026-11-14
**Status:** Complete (see Summary at the end)
**Agent:** rf-analyst (Gate 1, partition B, Item 3.02), report-only, `fix_authorization: false`
**Method in one paragraph:** read `research-notes.md` and `qa/phase2-output-inventory.md` first; read all 8 assigned files completely; read the `## Gaps and Questions` section of the scope slices the 8 files draw on (01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12); then re-checked about 120 of the files' own citations against HEAD `50d4d2b9d` and the E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` with read-only shell (grep, sed, wc, ls, jq, `git show`, `git ls-tree`, `sha256sum`). No pytest, no checkout, no write outside this report. The scratch batch scripts lived under `/tmp/ironclaude-batch.*` and were deleted by their own exit trap.

---
## 1. Coverage audit (checklist 1): research-notes SUGGESTED_PHASES rows 09-16

| # | File | Planned open items (research-notes.md rows 173-180 plus the assignment line) | Where resolved or logged | Status |
|---|---|---|---|---|
| 09 | 09-collaboration-designs.md | what a core must offer (hooks, resume, board path, seal) vs what no-Bash `reflect-reviewer` can host; whether H1-H4 are unconditional core requirements; honest evidence status (single smoke rows only); conflicts X1-X17 / C-01..C-19 decidable or not | s4 (a), s5 (b, with a naming note that H1-H4 are harness fixes, not transport), s2 (c), s6 (d, 36 conflicts classed E / E-partial / N / D, sums re-checked: 13+4+4+15 = 36), s7 (static kit vs exchange) | COVERED |
| 10 | 10-process-redesign.md | `ledger-v1` vs `review-ledger/1` name clash; whether E1 `verify-citations` and the coverage slice already implement item assignment and quote checking; (c) decidable-by-evidence per C1-C8 / X1-X7 / G0 / D1-D7; (d) the seed's "no missing-task category / no severity levels" claim | Unit 3 (a), Units 4 + 6 (b), Unit 7 (c), Unit 8 (d); Unit 9 maps every redesign idea to a destination | COVERED |
| 11 | 11-consumers-tasklist-workflow.md | advisory vs blocking tasklist review; where the panel plugs in (Wave 4, Stage 10.5, post gate); the 36-test verdict matrix constraint; DO4; the run-1 "reaches no reflect panel" claim | s1-s2 (a, b), s4 (c, 36 tests re-counted: 36), s5.1-5.2 (DO4, D14), s5.3-5.4 (other readers, plugin reach) | COVERED |
| 12 | 12-consumers-spec-review.md | which severity scale the core carries; "Medium" meanings; caps per consumer; plugin mirror differences for `design.md` and `brainstorm.md`; placeholder / reference-syntax differences | s2-s3 and s8 (a), s5.3 (b), s4 (c), s6 (d) | COVERED |
| 13 | 13-future-pr-review-and-rfqa.md | exact blockers per use case; minimum core shape now; rf-qa behaviour tests; which later reviewers fit; the `/task` lens-gate pattern; swarm 8-lens registry | s7 (a, P1-P15 / R1-R12), s8 (b, M1-M14), s5 (c), s9 (d), s4.3 and s3 | COVERED |
| 14 | 14-e3-variants-and-experiments.md | the unread numeric claims (slice 12 gaps 1, 2); is #479 the outcome of the refactor spec; value to keep per variant; install state and personal-over-project shadowing | s1, s2, s6 (a), s4 (b), s7 (c), s3 (d) | COVERED (control-arm numbers stay [UNVERIFIED], logged as gap 1) |
| 15 | 15-telemetry-manifest-run-record.md | one run-record design; can study telemetry carry anchors; execute-free reproduction of D-17 and D-23; cost accounting; memory write policy | s8 (a), s1.4 (b), s2-s3 + s7 (c), s9 (d), s6 (memory) | COVERED |
| 16 | 16-eval-governance.md | what counts as acceptance evidence; who owns harness files; are E1 and E2 independent (sha256 `044809e3...`); audits A-F as a reusable `verify-run`; `fullpkg()` bug and batch j1 | Part 4 (a), Part 5 (b), Part 6 (c), Parts 2 + 7 (d) | COVERED |

Key files named in EXISTING_FILES for these topics (reflect SKILL ranges, `cli/review/*`, `pr_submit/*`, rf-* agents, `plugins/superclaude/*`, installed variants, E2 collab packages r1-r5, E2 study tools) each appear in at least one of the 8 files. No scope item assigned to partition B is a coverage gap.

## 2. Completeness (checklist 2)

| Research file | Status | Summary | Gaps and Questions | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 09-collaboration-designs.md | Complete (line 4) | Y (`## Summary`, line 221) | Y (line 200) | Y (per section, lines 33, 51, 81, 128) | Complete |
| 10-process-redesign.md | Complete (line 4) | Y (line 241) | Y (line 210) | Y (per unit) | Complete |
| 11-consumers-tasklist-workflow.md | Complete (line 4) | Y (line 185) | Y (line 163) | Y (per section) | Complete |
| 12-consumers-spec-review.md | Complete (line 4) | Y (line 228) | Y (line 197) | Y (per section) | Complete |
| 13-future-pr-review-and-rfqa.md | Complete (line 4) | Y (line 277) | Y (line 247) | Y (per section) | Complete |
| 14-e3-variants-and-experiments.md | Complete (line 4) | Y (line 274) | Y (line 228) | Y (per section) | Complete |
| 15-telemetry-manifest-run-record.md | Complete (line 4) | Y (line 247) | Y (line 227) | Y (per section) | Complete |
| 16-eval-governance.md | Complete (line 4) | Y (line 299) | Y (line 262) | Y (per part) | Complete |

Line counts re-checked against `qa/phase2-output-inventory.md` (223 / 244 / 188 / 230 / 278 / 277 / 250 / 301): all eight match what the Read tool returned.

## 3. Gate focus (a): evidence and tags, with what I re-checked

I re-ran the files' own citations. Count of citations re-checked per file and result (T = true as stated, F = false):

| File | Re-checked (examples) | Result |
|---|---|---|
| 09 | `runner.py:497,503-505` `--no-session-persistence`; `reflect-reviewer.md:5-8,28,59`; `findings.py:104,118` and `findings_v2.py` limits; `models.py:94` "PINNED OFF", `config.py:155` `create_review_snapshot`; `commands.py:290-294,552-553` (`--resume` = skip-launch); `openai_compat.py:384-388`; E2 tip `.gitignore:13` = `lib/`, `:79` = `*.log`; `git ls-tree` file counts r1-r5 = 107 / 321 / 130 / 70 / 274 and `/lib/` = 0 in each; static `def test_` counts 103 / 163 / 89 / 90 / 82 (all five); r2 `RESULTS.md:8-9,25-28,33`; r5 `results.jsonl` row 1 (179.561 s, 29,688 tokens, overhead -33.25); r4 `act-rates.json`; `r5 sandbox-build.sh:25` `git add -A` without `-f`; MR:917 quote; conflict tally 13+4+4+15 = 36 | all T |
| 10 | `verify_cmd.py:11-12,25,28-29,99-105`; `findings_v2.py:96-97,155-162`; `panel.py:46,215-216,668`; reflect SKILL `:278,309,311,345,504,513-514`; `refs/coverage-mapping.md:211`; `refs/reviewer-spec.md:61,68`; `cluster_cmd.py:113-117`; E2 `seed-brief.md:26`; MR2:307,312,1077-1079; recounts by `jq`: 13 coverage sidecars, 11 with a duplicated row id, 2 with every `observed` empty; precheck 275 checked / 110 flagged (14 shadow files) and 772 / 400 (15 combo files); 29 manifests | all T except the label on `findings_v2.py:3-4` (finding F-1 below) |
| 11 | workflow SKILL `:85-93,89,105`; tasklist SKILL `:771,1171,1179,1537,1604,1610,1611,1614,1630,1640,1646`; `contract.py:317-326`; `runner.py:538-545`; `ensemble.py:74`; `tests/commands/test_workflow_command.py:251-261`; `tests/tasklist/test_tasklist_cli.py:573-580`; `tests/cli/reflect/test_shadow_skill_contract.py:42-53`; 36 `def test_` in `test_verdict_mapping.py`; reflect SKILL 2,033 lines; E2 hand-off lines 118 (run 1), 301, 406, 436, 457 (run 2); stale-doc claims `cli/reflect/__init__.py:3-7`, `runner.py:457` vs `commands.py:236-239`, SKILL `:1001` | all T |
| 12 | plugin `spec-panel.md:266` (`${CLAUDE_PLUGIN_ROOT}` fallback) and line counts 476/490, 100/149, 201/217; installed `~/.claude/commands/sc/spec-panel.md` identical to src; `pragmatic.md:224-231`; `tests/skills/test_review_severity_rule.py` (10 files in `S1_S3_FILES`, `CANONICAL_CAP_TEXT`, `test_f`); `fsm.py:32-33` and `loop_guard.py:19-20`; `card_convert.py` `MINOR_WORDS` (medium, important, should-fix); brainstorm SKILL `:279,307,311`; `task/SKILL.md:340,370,372,409`; `rf-qa.md:106-111,403-415` | all T |
| 13 | `wc -l pr_submit/*.py` = 6,511; `fsm.py:364-372` `is_groundable`; `models.py:106-113` Severity (5); `severity_router._CATEGORY_TABLE`; rf-qa / rf-qa-qualitative / rf-analyst = 551 / 1,154 / 428 lines; `rf-qa.md:484,505`; 44 `subagent_type: rf-*` lines in 8 SKILL.md (23+12+4+1+1+1+1+1); 175 U2 spawn lines in 7 skills (re-ran the stated pattern: 13/16/32/45/14/14/41); `synthetic-dnsp` in 5 files; swarm lens modules; `sc-bare-review/SKILL.md:20-22` stale callers; `task/SKILL.md:225,241,254` | all T except the `tests/pr_submit` count (finding F-3) |
| 14 | `~/.claude/commands/sc/spec-panel.md` = src; `git show 5d9a0ae70 --stat` (+12/-12, +127 test lines); `wc -l cli/review/*.py` = 16 files / 5,086 lines; `telemetry_cmd.py` = 98 lines; installed `review_ledger.py` imports stdlib only (no `superclaude` import), so "duplicate of the CLI ledger" holds | all T; I did not recompute the `jq` / byte arithmetic of sections 1-2 or the session-transcript model counts of section 6 (stated limit of this gate) |
| 15 | `telemetry.py:3,17,243-251` and the `_VIEW` SQL at `:362-379`; `telemetry_cmd.py` 98 / `telemetry.py` 447 lines; `manifest.py:3,53,156-163,348-354`; 29 manifests; `.dev/reflect/runs.jsonl` 27 lines; `last-pass-brainstorm-reflect-panel.md` holds 5 `# last-pass` entries; SKILL `:592` text "single-owner file, overwritten whole" | all T; D-17 and D-23 scratch reproductions not re-run (the SQL and `save()` bodies I read match the traces) |
| 16 | `reflect_shadow_exit.py:59,313`; `panel_lint.py:188`; E2 `final-table.py:9,15-18,20` (`PK = [DS, AL, DE]`, 12-character prefix test, `BAD_CHECKS`); `judge-one.sh:25-30` (rc and JSON-parse only); audit flag rows A-F = 106 / 230 / 409 / 438 / 62 / 55 (sum 1,300); `ground-truth.json` exists for all 3 packages; sha256 of the `.dev/tasks/done` designSpec tasklist = `044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481` and `source.md` = `a865f397...a10a`; audit-A summary text (890 vs 930 runs, 59 and 9 WARN) | all T; the 59 / 11 / 69 / 71 / 76 exclusion recomputation not re-run |

Tag discipline: every file carries per-claim tags ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED], plus [GIT-VERIFIED], [RE-DERIVED], [UNVERIFIED-slice], [DESIGN] variants that map onto the three required ones). Untagged doc-sourced material found: one (finding F-5). I found no invented citation and no number in the 8 files that I could prove fabricated. Three false statements were found (F-1, F-2, F-3), all listed in section 6.

## 4. Gate focus (b): open items and slice gaps

1. **Research-notes open items:** all resolved or logged (section 1 above).
2. **Slice gaps and questions:** I read the `## Gaps and Questions` section of every slice the 8 files read. Disposition of each slice gap or question that touches these 8 files: answered in a file of this partition (for example slice 05 Q1, Q2, Q5, Q9; slice 06 Q1-Q6, Q9, Q10; slice 07 Q7 and gaps 3-4; slice 08 Q1-Q11; slice 12 Q1, Q2, Q4, Q5, Q7, Q8, Q9; slice 02 Q-C, Q-D; slice 03 Q6, Q8; slice 04 Q5, Q8; slice 11 Q-3, Q-4), logged under a Gaps section of these files (slice 12 gaps 1-10, slice 10 gap 9, slice 11 G-1..G-9 via 15 and 16, slice 07 gap 1, slice 08 gaps 1-9 via 09), or carried as a value-ledger row. For the items no file in this partition answers I grep-checked the ledgers (partition C material, only searched, not graded here): slice 05 Q10 (C-18) and slice 06 Q8 (HO-5) are in `21-value-ledger-brainstorms.md`; slice 03 Q5 (arm A re-baseline) is `VL-20-441`; slice 04 Q2 is `VL-20-706`; slice 01 Q-D is `VL-19-445`; slice 07 gap 9 (`run-package.sh` writes `DONE` on INVALID) is `VL-22-266` and `VL-22-383`; slice 08 Q12 (the three-FAIL pattern, D-X-1) is in `22-value-ledger-collab-designs.md` lines 619, 915, 945, 969. No slice gap was found dropped.
3. **Unresolved but honestly logged (allowed by the gate):** the six control and 427-arm `metrics.json` files behind the phase-5 "improvement" claims (14 gap 1); `lib/` of E2 r2-r5 (09 gap 2); pytest counts of r1-r5 (09 gap 1); whether `additionalContext` reaches a subagent (09 gap 4); real two-process manifest race (15 gap 1); owner-approval questions (14 Q1-Q6, 11 Q6-Q8, 13 Q1-Q5, 16 Q1-Q7, 15 Q6-Q9).
4. **One resolvable item left untried:** 14 gap 1 says the comparator copies under `MEAS/diffgate/reviews/comparators/` and the surviving raw control transcripts under `~/.claude/projects/...exp346-ab-*` "should be opened by the next pass". The gate rule accepts a logged gap, so this is not a finding; synthesis must keep the control baseline as [UNVERIFIED] (14 does).

## 5. Gate focus (c), (d), (e)

- **(c) run-1 contamination:** I grepped `research/09-*` to `16-*` for `unify-2026`, `UNIFY-RUN2`, `QUEUED`, `TASK-RESEARCH-review-panel-unify` and `run-1 (research )?folder` (case-insensitive). Hits: `09:13`, `12:8`, `14:8`, `15:11`, each a sentence that states the independence rule ("was not read"). No file in the partition cites, quotes or lists a path under the forbidden folder or the queued note; `10`, `11`, `13`, `16` have no hit. The word "run-1" in `11` (s5.2) and `16` means the E2 hand-off `HANDOFF-review-panel-unification.md` at the E2 tip, which is allowed. The recorded slip in scope slice 03 gap 10 is not repeated in these files. **PASS.**
- **(d) value-ledger rows:** none of the 8 files is a value ledger (ledgers are files 19-24, partition C). Two files classify items with their own vocabulary: `10` Unit 9 uses CORE / MODULE / STUDY / EXISTS / HOLD (rows 5 and 13 are HOLD, 15-16 are EXISTS, 17-18 are STUDY); `14` section 7.1 gives two destinations in rows c1 ("CORE for the verdict rule; EVAL for the metrics"), c2, c4 and c5, and 7.2 uses CORE / MODULE / EVAL / DROP once per variant. These are research classifications, not ledger rows, so gate (d) does not apply, but synthesis 8.1 must map STUDY, EXISTS and HOLD into the closed set (CORE / MODULE-x / EVAL / HARNESS / KNOWLEDGE / DROP) and split the dual rows (note F-6, minor).
- **(e) building on AMBIGUITIES rows as fact:** checked each [CODE-CONTRADICTED] and [UNVERIFIED] row of `research-notes.md` lines 238-265 against the 8 files. The files either re-verify the contradiction (11 on D14; 10 on the seed claims; 12 on Medium and caps; 14 on the install date wording; 13 on the "185" spawn count) or keep the claim tagged. Two statements lean on an [UNVERIFIED] row without saying so clearly: `16` Part 4.2 quotes "80 reviewer-package runs, 49 blocking findings lost" (the COMBO-REPORT line says "80 reviewer-level cases"; the unit of the 92 / 80 / 49 figures is an open [UNVERIFIED] item), and `15` s6.2 item 4 says "one wrong lesson already lives in it" for memory line 64 while the notes carry that row as contradicted only against `cluster_cmd.py` with the installed-CLI version unverified (notes F-7 and F-8 below, both minor). No file builds a design conclusion on those two.

## 5a. Cross-reference check (checklist 3) and contradictions

The eight files cite scope slices and code, almost never each other. I listed each concern that two or more of the files cover and compared their statements.

| Concern | Files | Result |
|---|---|---|
| Count of meanings of "Medium" | 12, 13 | **Contradiction.** 12 s3 (line 82) re-derives "at least six distinct uses ... not four" and lists it as `[CODE-CONTRADICTED]` against slice 12 I1 (line 218). 13 line 179 still writes "Medium has four meanings, slice 12 I1" without a tag. See F-2. |
| Severity scale, `blocking` flag, caps | 11, 12, 13 | Consistent on facts (tasklist High/Medium blocking, CLI gates only on High; v2 `blocking == severity != MINOR` under `reflect_category`; 5-tier PR scale). 13 M7 lists caps in four units ("3 reviews, 2 passes, 2/5 rounds") and does not adopt 12 s4's reading that most are 2 fix cycles; synthesis must reconcile (note only). |
| Findings location, anchor vs citations | 10, 12, 13 | Consistent: v1 anchor 12-200 chars; v2 `citations[]` already carry file:line (13 s6 narrows slice 12 G1.1; 12 s6 table agrees for v1 only). |
| H1 / H2 unconditional core requirements | 09, 10 | Consistent (both: unconditional; 09 s5 H2, 10 Unit 9 rows 1-2). |
| `reflect-reviewer` has no Bash | 09, 10, 13 | Consistent (09 s4.2, 10 Unit 5, 13 R1 and P10); none points to the others. |
| `telemetry.py:3` "no document text" | 10, 15 | 10 Unit 9 row 14 treats the docstring as the restriction to absorb and asks it again as Q7; 15 s1.4 answers Q7 (pointers not text) and shows the rule is enforced only for `context`. Neither cross-references the other (note only; no conflict). |
| Naming of "ledger" | 10, 14 | Consistent (10 Unit 3: shipped `review-ledger/1`, proposed `ledger-v1`, installed-only variant skills as a third use; 14 s7.2 and Q2: two status machines). |
| `lib/` absent from E2 commit; test counts | 09 (and 22 ledger) | Re-verified, consistent. |
| E1 and E2 independence, shared GT | 16, (10 Unit 7 HO sets) | Consistent. |
| Verdict ownership (reviewer-typed vs script-computed) | 12, 14 | 12 line 27 points to "section 7" for it; section 7 of 12 does not discuss it (F-4). 14 s7.1 c3 covers fail-closed parsing and quorum. |

## 6. Findings

Grading rule applied: BLOCKING when a research file states something false or leaves two files in contradiction on a point the report will cite; MINOR when the point is a nit, a count that does not drive a conclusion, a missing tag on a true statement, or a wording choice.

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| F-1 | IMPORTANT | Y | `10-process-redesign.md` Unit 2 (line 27), Gaps and Questions item 2 (line 215), Stale Documentation Found bullet 1 (line 234) | The file labels the docstring at `findings_v2.py:3-4` "[CODE-CONTRADICTED] in its general form" and a [STALE DOC], quoting only "A findings-v1-valid line with other keys may be rejected". The full docstring sentence is "A findings-v1-valid line with other keys may be rejected: a line that carries calibrated_confidence is rejected." That is exactly what `check_finding` does (`findings_v2.py:96-97`), so the docstring is accurate, not stale. The file's real finding (extra keys such as `class`, `probe`, `src`, `origin` are not rejected at HEAD) is correct and is unaffected. As written, synthesis check 9 ("stale documentation discrepancies are surfaced") would put a non-existent stale-doc item into the gap analysis, and Gap 2's question ("should the docstring be narrowed") is moot. | `src/superclaude/cli/review/findings_v2.py:3-5` (read in full): line 3 "A line that findings-v1 accepts and whose keys are all in V1_FIELDS passes check_finding unchanged.", line 4 as quoted above, line 5 "Prior lines are rejected."; `:96-97` `if "calibrated_confidence" in obj: return "calibrated_confidence is not allowed in a findings-v2 line"` | In Unit 2, Gap 2 and the Stale Documentation list, replace the [CODE-CONTRADICTED] / [STALE DOC] label with [CODE-VERIFIED] "docstring matches code: only `calibrated_confidence` is rejected, other extra keys pass"; drop the "narrow the docstring" question; keep the K6 resolution (extra keys accepted) |
| F-2 | IMPORTANT | Y | `13-future-pr-review-and-rfqa.md` section 7.1 table row P4 (line 179) | Row P4 says "Medium has four meanings, slice 12 I1". File 12 re-derived the count as at least six and marked the slice figure `[CODE-CONTRADICTED]` (`12-consumers-spec-review.md:82, :218`: M1 non-blocking warning, M2 priority label, M3 PR route tier, M4 tasklist skill blocking, M5 tasklist CLI non-gating, M6 `card_convert` downgrade). 13 repeats the slice number with a slice pointer and no tag, so two files of the same research set disagree on a headline figure that the report's Section 2 and the conflict log will quote (the notes' PATTERNS item 6 also still says four). | `card_convert.py` `MINOR_WORDS = {"minor", "medium", "low", "should-fix", "important", "nit", "info", "p2", "p3"}` (M6, re-read); `spec-panel.md:123` priority line (M2); tasklist SKILL `:1537` Medium blocking (M4) vs `cli/tasklist/gates.py` (M5), both read by 12 | Change row P4 to "Medium has at least six uses (see 12 s3)" or drop the count; when the synthesis is written use six and note that `research-notes.md` PATTERNS item 6 says four |
| F-3 | MINOR | N | `13-future-pr-review-and-rfqa.md` s1.1 "Test surface" (line 34) and P13 (line 188) | The file says `tests/pr_submit/` holds 50 `.py` test files plus `conftest.py` and `__init__.py` ("52 entries"). `ls tests/pr_submit/*.py` and `find tests/pr_submit -name '*.py'` both return 49 entries in total (47 test modules plus the two). The conclusion ("large pinned surface") stands. | shell count at HEAD, 2026-11-14 | change "50 test files ... 52 entries" to "47 test modules (49 `.py` files)" |
| F-4 | MINOR | N | `12-consumers-spec-review.md` s1.2 last bullet (line 27) | "See section 7 (open item a, verdict ownership)". Section 7 of that file is "Who actually calls the shared review machinery today"; verdict ownership appears only as one row of the s6 table (line 161). The pointer is dangling; the topic is covered by file 03 (partition A) and 14 s7.1 c3. | `12-consumers-spec-review.md` lines 27, 161, 174-179 | point the sentence to the s6 table row and to file 03 |
| F-5 | MINOR | N | `09-collaboration-designs.md` s4.2 "Delivery by hook" (line 120) | A statement taken from the Claude Code sub-agents web page (hooks fire for a subagent's tool calls; frontmatter may declare `hooks`) carries no [CODE-VERIFIED] / [UNVERIFIED] tag. Gap 4 does tag the narrower question (does `additionalContext` reach a subagent), so the conclusion is hedged, but checklist 3 wants every doc-sourced claim tagged. | `09-collaboration-designs.md:120` vs `:205` | add "[UNVERIFIED: doc-sourced, not exercised in this repo]" to the sentence |
| F-6 | MINOR | N | `10-process-redesign.md` Unit 9 (lines 161-183); `14-e3-variants-and-experiments.md` s7.1 rows c1, c2, c4, c5 | Destination words outside the closed ledger set (STUDY, EXISTS, HOLD) and dual destinations ("CORE for the verdict rule; EVAL for the metrics"). Not value-ledger rows, so gate (d) is not breached. | as listed | none required; synthesis 8.1 maps them when it merges with files 19-24 |
| F-7 | MINOR | N | `16-eval-governance.md` Part 4.2, Tier S bullet (line 144) | Writes "80 reviewer-package runs, 49 blocking findings lost per COMBO-REPORT.md:292 [CODE-VERIFIED line]". The source line (E2 tip `COMBO-REPORT.md:292`, re-read) says "80 reviewer-level cases, 49 blocking findings lost"; the unit of 92 / 80 / 49 is an open [UNVERIFIED] item of `research-notes.md` (AMBIGUITIES) and `10` Unit 9 tags it so. The silent-loss defect itself is verified (`ledger.py:131-134,141-149`). | E2 tip `COMBO-REPORT.md:292`; `ledger.py:131-134` | quote the source wording ("reviewer-level cases") and add [UNVERIFIED unit] |
| F-8 | MINOR | N | `15-telemetry-manifest-run-record.md` s6.2 item 4 (line 156) | "One wrong lesson already lives in it" is stated flat while tagged "[UNVERIFIED by me]"; notes list memory line 64 as contradicted only against `cluster_cmd.py` with the installed-CLI version unverified. Slice 11 G-2 says the installed CLI lagged at least once, so the lesson may have been true when written. | `research-notes.md:254`; scope slice 11 G-2 | say "a lesson that `cluster_cmd.py:27-34` now contradicts (installed-CLI version at write time unverified)" |

No other defect found in the lens. In particular: no fabricated citation (about 120 re-checks, section 3), no forbidden-folder reference, no missing section, no Phase 2 file left `In Progress`, and no slice gap dropped.

## 7. Compiled gaps (items that remain open after Gate 1, none blocks synthesis once F-1 and F-2 are fixed)

### Critical gaps (block synthesis)
- None. (The two blocking findings are wording or label fixes, not missing research.)

### Important gaps (affect quality)
- Control and 427-arm baseline of the phase-5 experiment cannot be recomputed in this repo (six `metrics.json` files absent); 14 gap 1. Synthesis must keep "no validated winner" and the control numbers as [UNVERIFIED]. The comparator copies and surviving raw transcripts it names as next steps are unread.
- No measurement exists for any collaboration design versus the static kit (09 s7); no Spike 4 ran; E2 `lib/` is absent for r2-r5, so no design can be rebuilt from the commit (09 gaps 1-3).
- Whether PostToolUse `additionalContext` reaches a subagent's model is untested in this repo (09 gap 4).
- Acceptance evidence for any unified design is Tier S only; no hold-out, seeded or replicated-over-packages evidence exists (16 Part 4); batch j1 was never audited (16 s2.3).

### Minor gaps (notes)
- Real two-process race on the manifest not run (15 gap 1); pooled `+3.00, p = 0.013` test needs data not found (14 s5 s3); per-batch cost and USD pricing of gateway aliases not interpretable (15 gap 2).

## 8. Depth assessment

**Expected depth (Deep tier):** data-flow traces, integration-point mapping, pattern analysis. **Achieved:** all three. 11 traces each consumer call path to the code (Wave 4 `:89`, Stage 10.5 `:1630`, post gate `:1157-1163`, `runner.py:538-545`); 13 maps PR and rf-qa call sites by two stated counting units; 15 traces D-17 and D-23 by hand and by a scratch run and recounts 29 manifests; 16 re-derives the `fullpkg()` bug, the hash and the audit tables; 10 and 12 compare the proposed objects against code line by line. **Missing depth elements:** none that the assignment named.

## 9. Recommendations to the fix agent

1. Apply F-1 and F-2 (two edits in two files, label and one table cell). Nothing else is required for a PASS on re-verification.
2. Optionally apply F-3 to F-8 in the same pass (all are one-line edits); they are notes, not conditions.
3. Do not change any citation in the 8 files on my account: every citation I re-checked was true as stated.

## Summary

- Files reviewed: 8 (research/09 to 16). Every file is `Status: Complete` with a Summary, a Gaps and Questions section and Key Takeaways; every planned open item of `research-notes.md` is covered; no slice gap is dropped (each is answered, logged or a ledger row); no run-1 contamination; the 8 files are not value ledgers, so gate (d) does not apply.
- Citation quality is high: about 120 of the files' own file:line, git path:line, count and hash claims re-checked read-only, all true as stated except three small false statements.
- Blocking findings: **2** (F-1 a false [CODE-CONTRADICTED] / [STALE DOC] label on an accurate docstring in file 10; F-2 file 13 repeats "Medium has four meanings" while file 12 shows at least six). Minor findings: **6** (F-3 to F-8, notes only).
- Fix size: two one-line edits (a label in file 10, a table cell in file 13).

**Verdict: FAIL (2 blocking findings, 6 minor).** Re-verify after the fix: F-1 and F-2 only.

**Status:** Complete
