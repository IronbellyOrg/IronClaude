# E3 merge-executor log (new-text blocks and appendices)

- Executor: E3 of 4, step 5 (merge execution). Scope: the new-text blocks and appendices of `refactor-plan.md` listed below.
- Output folder: `adversarial/partials/merge-stage/new-blocks/`.
- Read-only rules kept: no git write, nothing under `.claude/` read or written, no variant or original report modified, Python only through `uv run`.

## Read-only checks run (shared by several files)

- Batch b01-b13 (one script under `/tmp/ironclaude-batch.*`, `BATCH_OK failures=0`, directory removed): HEAD = `ad8f5756044f`; `origin/master` = `d4d1662a8` (2026-11-14 12:42 -0500); merge-base `d2d8a2d16`; `git rev-list --count` 4a22d74..6c09843 = 4, 6c09843..e2f2ac268 = 7, d2d8a2d16..HEAD = 5, d2d8a2d16..origin/master = 3; `git diff --stat` 792cf8c52..50d4d2b9d and 50d4d2b9d..ad8f57560 on `src tests scripts` empty; `git diff --name-only 6c09843 e2f2ac268` on `audit2.py` and `combos/SPEC.md` empty; `git status --porcelain -- src tests scripts` clean; `e2f2ac268` dated 2026-11-14 19:19:40 +0000.
- Batch c01-c10 (`BATCH_OK failures=0`): rf-* `subagent_type` lines 52 in 11 files, 44 in 8 `SKILL.md`; `superclaude review` in the reflect `SKILL.md` 5 lines, 7 occurrences; `tests/pr_submit/test_*.py` 47 (49 tracked `.py`), `tests/cli/reflect/test_*.py` 38; `panel.py:46` `_SLOT_KEYS`, `:215` rejects other keys; `ledger_cmd.py:13` `{PASS 0, REVISE 10, ESCALATE 11}`; `ledger.py:363-372` returns `last["verdict"]`; `pipeline/process.py:145-154` `reviewer_profile`; V1 has 698 `| V-` rows; `diff-analysis.md:463` now states the denominator 234.
- Single checks: `git diff --stat origin/master HEAD -- src tests scripts` = 50 files; line content of `test_worker_contract.py:777/786/1861` (HEAD) equals `origin/master` `:787/796/1872`, and `pragmatic.md:225/231` equals `:229/235`; `runner.py:566` and `ensemble.py:548` contain `reviewer_profile=True`; `git ls-files` path of `pragmatic.md` = `src/superclaude/output-styles/pragmatic.md`.
- Not run: no pytest collection (the collected-test counts 651, 353, 2258 are taken from fault-finder notes row 5); no web fetch (X-035, X-037 stay as the debate left them; X-036 rests on the fault-finder's and the run 1 advocate's fetch).

## New finding escalated (bookkeeping, not changed)

`partials/scoring-matrix.md` / `matrix.json` record C-053, C-056, C-065 and S-039 as Variant 2 by cluster inheritance. The advocates' Round 1 exception lists say otherwise: C-056 is V1 for both (`r1-advocate-V1.md:248`, `r1-advocate-V2.md:275`); S-039 is V1 for both (`r1-advocate-V1.md:261`, `r1-advocate-V2.md:278`); C-053 and C-065 are V1 for the run 1 advocate (`:247`, `:249`) and V2 (cluster) for the run 2 advocate. `r2-state.json` has no point entry for any of them (checked by script). The tally (V1 26, V2 130) and the 218/234 figure were not re-tallied; the Merge Notes state the finding and 6.13.0 uses the advocates' positions. Same mechanism as R25-INV-004.

## M00-merge-notes.md (M-00)

- Built from: plan M-00 (a)-(h), rule 3 (id rule, including `R1-CLS-nn`, `R1-Rnn`, bare `R1`..`R9`, the compare-id exception for V2:3509-3525 / V2:3586-3670 and the bare-short-label sentence), rule 4 (split-point treatment), rule 7 (owner decisions), M-02 citation-form rule; numbers from `scoring-matrix.md` Convergence Assessment, `matrix.json` (`strict` 0.9316), `invariant-probe.md` Summary, `base-selection.md` Combined Scoring; quotes from `r2-advocate-V1.md:116, 167` and `r2-advocate-V2.md:176`.
- Placement conflict for the assembler: the brief requires every file to begin with `<!-- Source: new text — merged per Change #M-00 -->`, and the skill requires the merged file to begin with the three provenance lines. The Source comment is line 1 here, the three provenance lines follow. The assembler should put the three provenance lines first.
- Added beyond the plan's list: the paragraph on the four inherited verdicts above (verified; reported, not acted on).

## M02-baseline-addendum.md (M-02)

- Built from: M-00 (e) and (f), M-24 item 9, the citation-form rule; facts from batches b01-b13 and the line-content check.
- Plan text corrected: M-24 item 9 says the pins "that V2 C14 and C26 cite" sit at `test_worker_contract.py:787, :796, :1872` and `pragmatic.md:229, :235`. C14 and C26 (V2:4443, V2:4455) cite only the `test_worker_contract.py` lines; `pragmatic.md:225,231` is the basis of slot X-15 (V2:3525; R25-INV-001). The block says so.
- Placement: paragraphs only, no heading. The plan says "append after V2:123", which is after the `---` at V2:122; to stay inside Baseline and Conventions the block belongs before that separator. Assembler's choice.
- DUPLICATION (escalated): E1's `e1_base_corrections.py` (lines 67-69) inserts the M-24 item 9 note into base line V2:108, and M-02 asks for the same facts in this addendum, so the merged document states the `origin/master` facts twice. One of the two should be dropped by the orchestrator or assembler; E3 did not change E1's work.

## M08-disposition-table.md (M-08)

- Built from: V1:1166-1189 (6.0 index; run 1's ids there are written C01..C20), diff rows C-050..C-075 and S-032..S-039, plus C-076..C-093 and X rows where the Section 6 rows had no counterpart, `scoring-matrix.md` point verdicts, the four advocate files, V2:3509-3525 and the V2 lines cited per row (spot-read: 3029, 3185, 3205, 3235, 3321, 3331, 3334, 3655, 3743, 3771, 4445).
- Every row verified. Rows that differ from the plan's guidance, and why:
  - R1-C-03: plan "run 2 C-07/C-09 govern". Kept, and added C-059 = Both (cluster CL-06) and that run 1's launch grammar is only a conditional option (`r2-advocate-V2.md:90`).
  - R1-C-06: plan "carried (no run 2 axis)". Kept as Carried (owner-gated); added that the matrix's C-056 = Variant 2 is an inheritance artefact (both advocates V1) and that run 2's C-03 has no calibrator in the default.
  - R1-C-08: plan "run 2 identity chain governs (gated)". Written precisely: C-08 served-model record gated by measurement M1; X-14 `unrecorded`. No identity row exists in C-050..C-075, so C-082 (Section 7) and X-050 are cited.
  - R1-C-12, R1-C-13, R1-C-14, R1-C-18: plan cells kept; added R25-INV-005 candidate (R1-C13-06), R25-INV-030 (3 HIGH invariants, R1-Q-47..R1-Q-50) and R25-INV-006 respectively.
  - R1-C-15: plan "see diff C-053". Written as Carried (owner-gated): matrix C-053 = V2 is cluster inheritance; the run 1 advocate gives V1 and the run 2 advocate concedes and carries run 1's policy (`r2-advocate-V2.md:29, 157`); run 2's C-06 drop record governs loss accounting.
  - R1-C-16: plan "run 2 governs (no per-lens predicate in core)". Refined: run 2 has no predicate in the core but a per-lens blocking rule as module profile data (V2:3745); the C-065 split (V1 advocate V1 55%, V2 advocate cluster V2) was never debated and is stated.
  - R1-C-20: plan "run 1 shadow harness + portable benchmark carried". Kept as run 1 content in 6.13 and gate R1-G-bench (8.5); not stated as adopted.

## M10-status-table.md (M-10)

- Built from: V2:3509-3525, V2:3586-3604, V2:3636, 4445, 4455, 4078, 4144; V1:594, 2641, 2657, 3001, 3841, 3886-3890; `r2-advocate-V1.md` and `r2-advocate-V2.md` final verdicts; `invariant-probe.md` R25-INV-003, -008, -011, -024, -025, -028, -029.
- Exactly 15 rows, keyed C-01..C-12, C-13 (X-13), C-14 (X-14), C-15 (X-15). Non-Unchanged rows: C-01 Open; C-04, C-09, C-11, X-14 Changed (OPEN) (= the five of R25-INV-028).
- Plan cells corrected: C-04 cell said "run 1's C-17 fix-in-place for ENS-1..ENS-5"; the steps R1-M3-03..R1-M3-07 (V1:3886-3890) cite R1-ENS-1..6, 8 and 9 (grep), so the cell names the step range, not an ENS range. C-05 and X-15: plan "Unchanged"; kept, and added that both hold only while C-01 to C-03 stand (V2:3515, V2:3525), plus the C-05 tiebreaker caveat (`r2-advocate-V2.md:23`). C-03: added the open `requested` source (Q-42; R25-INV-005).
- The lead says this table governs where it differs from 6.12.9.1 or 7.0.1; this follows M-10's "precedence record" description. Flag for the orchestrator if a different wording is wanted.

## M12-section8-lead.md (M-12): skipped

- M-12 replaces base lines V2:4234-4237 in place; E1's script header names M-12. No conflict found with the new blocks (M00 (b) and (h) use the same Section 8 scope words).

## M15-translation-table.md (M-15)

- Built from: V1:2946-2963 (16 components), V1:2969-2976 (6 modules), V1:3117-3118 (destination legend), V2:3730-3736 (5 modules), V2:3740-3750 (9 elements).
- Row counts by an inline `uv run` count over V1:3123-3820 (698 rows): DROP 91; Rollout and evaluation instrument 88; Finding contract 62; Panel resolution 56; Brief and grounding injection 36; Reflect UC-1 module 36; Merge and verdict 32; Round model (ledger) 31 (+4 "deferred to O-1"); Reflect UC-2 module 25; Dispatch 24; Clustering 22; Lens registry 22 (+1 "Severity scale and per-consumer mapping"); Identity check 21; Calibration 21; Built-in run audits 20; Blocking decider hook 18; PR review module 16; Telemetry 14; Run manifest 12; rf-qa replacement module 12; Workflow/tasklist module 11; Spec review module 11; Citation checks 7; Core CLI surface (7.1.1) 5.
- One no-counterpart row: Calibration. Not mapped: "Core CLI surface (7.1.1)" (outside the cited tables). The 5 components R25-INV-020 counts as not adopted are flagged in the Basis column.
- E2's carried rows spell the destination "deferred to R1-O-1" (checked in `v1-blocks/M14-sec8-inventory.md`); this table uses that spelling. Insertion point: `v1-blocks/M14-sec8-inventory.md` line 22 marker.

## M21b-open-items-9.12.md (M-21, block 9.12)

- Built from: M-21 list, `invariant-probe.md`, fault-finder "Corrections the merge must apply" 1-13, the exact correction texts of M-18 (R25-INV-003) and M-24 item 5 (R25-INV-006), V2 Section 9 rows Q-39..Q-89 (grep), V2:4412, and the code lines of batch c06-c08.
- Part A: the 7 HIGH UNADDRESSED invariants (R25-INV-024 and -029 in one row as in M-21). Part B: claim cut, exit code 12, distinctness default, post-gate engine, quorum denominator, per-slot keys, line-number base; each with both versions.
- Added beyond the plan's list: the run 2 advocate's Round 1 exception also gives C-010 = V1 (`r1-advocate-V2.md:269`).

## M22b-compare-artifacts-10B.md (M-22, block 10.B)

- Built from: `find` over the compare folder and the head of each file. `adversarial/merge-log.md` is listed though it does not exist yet (M-30 writes it). Paths relative to `.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/`.

## M28-appendix-C.md (M-28)

- Generated by `partials/merge-scripts/e3_appendix_c.py` (re-runnable; asserts 63 rows X-001..X-063, 25 X ids in the orchestrator table (the artifact's text says "about 22"), 20 design-choice ids, matrix.json winners equal to scoring-matrix.md winners for all 63, 63 rows in the output).
- Source quirk handled: row X-054 of `diff-analysis.md` has an unescaped pipe inside a quoted cell ("C-17 | fix ..."); the script re-joins it with `\|`.
- Result: every row has a resolution; OPEN rows: X-040, X-041, X-056, X-057, X-058 (both advocates) and X-051 (label split, both positions). No X row has an inherited verdict that both advocates contradict (checked against `r2-state.json`). Integrity check: 63 table rows, 6 cells each, backticks balanced.
- The "Where handled" column is a hand-kept map from the plan; it names sections other executors build (2.10, 3.6, 4.7, 5.6, 6.13, 7.4, 8.x, 9.11) and Appendix E items.

## M29-appendices-D-E.md (M-29)

- Appendix D generated by `partials/merge-scripts/e3_appendix_d.py` (asserts 32 rows, 24 UNADDRESSED, the 7 HIGH ids, a carrier for every UNADDRESSED row). R25-INV-022 has no carrier in the plan ("Appendix D only"). R25-INV-015: `diff-analysis.md` Summary already reads 234.
- Appendix E written by hand: E.1 corrections M-24.1..M-24.14 and M-25.a..M-25.i, marked `[planned; the merge-log.md records what was actually applied]`; "Applied by" E1 for M-24 and E2 for M-25 (both confirmed from the script headers `e1_base_corrections.py`, `e2_v1_extract.py`); M-24.5 and M-24.7 also E2 for the carried blocks; M-24.9 notes the duplication with the M-02 addendum. E.2 counts with units from fault-finder rows 4-9, 20-23, with re-checks named.
- The file keeps the marker comment `<!-- APPENDIX-E -->` between D and E, which the generator uses to keep E when D is regenerated; the assembler may drop it.

## Not done (out of scope)

- Appendix F (provenance index) and the Table of Contents: assembler's.
- No change to E1's or E2's outputs.
