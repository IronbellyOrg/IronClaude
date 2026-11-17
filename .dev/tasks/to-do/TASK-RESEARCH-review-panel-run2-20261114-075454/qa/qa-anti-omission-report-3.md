# QA Report: Anti-Omission (Gate 5, agent 3, partition 3 of 4)

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md` (5,098 lines at the time of the check)
**Enumeration file:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/qa-anti-omission-enumeration-3.md`
**Grading override applied:** `qa/grading-override.md` (blocking only if a decision, recommendation, value-inventory destination, conflict-log outcome or a number the recommendation rests on would be wrong or unsupported; a required deliverable or section is missing; or a security, data-loss or safety-boundary risk)
**Date:** 2026-11-14
**Status:** Complete

[PARTITION NOTE: this report covers the assigned files only (research 12 to 18, gaps-and-questions.md, synth-01 to synth-03, and ledgers 22 and 23 moved to this agent by `qa/gate5-partition.md`). Cross-file checks are limited to that subset.]

## Anti-Omission Report

**Input files checked:** `research/12-consumers-spec-review.md`, `13-future-pr-review-and-rfqa.md`, `14-e3-variants-and-experiments.md`, `15-telemetry-manifest-run-record.md`, `16-eval-governance.md`, `17-defect-register.md`, `18-repo-constraints-and-branching.md`, `gaps-and-questions.md`, `synthesis/synth-01-problem-current-state.md`, `synth-02-overlap-matrix.md`, `synth-03-target-gaps.md`, `research/22-value-ledger-collab-designs.md`, `research/23-value-ledger-e1-e3-code.md`. **4,067 distinct findings enumerated** (1,751 ledger rows, 55 non-row ledger items, 200 defect-register entries, 1,045 synthesis lines, 555 gap rows, and 461 findings of research files 12 to 16 and 18).

### Method

1. Enumeration. Every file was read completely. The enumeration file has one numbered list per file and ends each list with its `COUNT` line. Ledger rows, defect-register rows, gap-log rows and synthesis lines were enumerated by script from the files themselves (one entry per row or per substantive line); research files 12 to 16 and 18 and the non-row sections of ledgers 22 and 23 were enumerated by hand, one entry per claim, number, rule, gap, question or correction.
2. Coverage by meaning, not by id. Ledger and register rows: the Appendix A row (`synthesis/synth-08-value-inventory.md`, which section 8.1.2 and Appendix A name as the carrier of the 5,950 rows) was compared by script with the source row: Statement, Kind and Source equal; the row sits under the heading equal to its Destination column; Destination equal to the ledger destination, or a recorded `moved from <old>: <why>` reason, or `DROP[duplicate]: duplicate of <ID>` with the kept row present and not DROP. Synthesis files: each substantive line was tested for verbatim presence in the report after whitespace normalisation. Research files: a term search of the report (several distinctive terms per finding), then reading of the matching passages (for example 2.4, 2.7, 4 gap rows, 6.12, 7.2, 8.2, 9, Appendix B); a finding counts as represented only when the passage carries its substance. Gap rows: logged-open rows were checked against the Section 9 groups and the per-section "Not verified" lists, resolved rows against the corrected value in the owning section.
3. Independence. The run-1 task folder and the queued-run note were not read, listed, grepped or cited; `.dev/tasks/` was excluded from repo-wide searches; the task folder itself was read where assigned. Python ran only through `uv run`, read-only, from `/tmp/ao3-work/` (scripts only; removed at the end of this report's "Cleanup" line).
4. Fixes: none. `fix_authorization: false`; this agent modified nothing except this report and the enumeration file.

### Earlier-gate removals (JUSTIFIED-REMOVED check)

Files read: `qa/qa-fix-log.md` (Gate 3 cycle 1), `qa-fix-log-c2.md`, `qa-fidelity-fix-log-c1.md`, `qa-fidelity-fix-log-c2.md`, `qa-consolidated-findings-phase6.md`, `qa-consolidated-findings-phase6-c2.md`, `qa-fidelity-consolidated-findings.md`, `qa-fidelity-consolidated-findings-c2.md`.

- `qa-fix-log-c2.md`, `qa-fidelity-fix-log-c1.md`, `qa-fidelity-fix-log-c2.md` and `qa-consolidated-findings-phase6-c2.md` / `qa-fidelity-consolidated-findings-c2.md` each hold one line (`Skipped: Gate 3 passed at review 2`, `No fix required: zero blocking findings at review 1`, `Skipped: Gate 4 passed at review 2`); they list no removal.
- `qa-fix-log.md` records two fixes, P6-001 and P6-002. Both are additions (a precedence paragraph and delta table in Section 3, pointers in Sections 4 and 7.0.1, a table and paragraph in 8.1.2); the log states the report grew from 5,057 to 5,098 lines and that no target cell, id, count or table was removed or renumbered. Minor findings P6-003 to P6-110 were not touched.
- Result: no claim was removed or corrected-away as false or unsupported by an earlier gate in this partition. No finding is classified JUSTIFIED-REMOVED. Every absence reported below is therefore judged on the report text alone.

### Ledger verification (ledgers 22 and 23)

Recount with read-only `grep -c`: `grep -c '^| VL-22-' research/22-value-ledger-collab-designs.md` = **955**; `grep -c '^| VL-23-' research/23-value-ledger-e1-e3-code.md` = **796**. These equal the ledgers' own totals, the 955 and 796 of the Source rows in 8.1.0, and the counts of the enumeration file (`COUNT 22-value-ledger-collab-designs.md: 955`, `COUNT 23-value-ledger-e1-e3-code.md: 796`). Ids are unique and sequential in both files.

| Check on each row | Ledger 22 (955) | Ledger 23 (796) |
|---|---|---|
| Present in Appendix A exactly once | 955 | 796 |
| Statement, Kind, Source equal to the ledger row | 955 | 796 |
| Row sits under the Appendix A heading equal to its Destination | 955 | 796 |
| Same destination as the ledger (includes ledger DROP rows that stay DROP) | 918 | 756 |
| Destination changed with a recorded `moved from <old>: <why>` reason | 30 (all MODULE-tasklist to CORE; exchange layer, tier data, H1 brief slot, card schema, per-target extension point) | 2 (VL-23-267 EVAL to CORE; VL-23-479 MODULE-reflect to CORE) |
| Destination changed to DROP with `duplicate of <ID>` and the kept row present and not DROP | 7 | 37 (the 38th, VL-23-697, points at DR-153, which is itself `DROP[obsolete]` with a REPRODUCED fenced-yaml reading; see below) |
| Source ledger Reason contained in the Appendix A Reason | 955 | 795 (VL-23-619 rewrites "Duplicate of VL-23-535" to "Duplicate of DR-140 ... VL-23-535 is also DROP, duplicate of DR-140", which keeps the meaning) |

Ledger 22 deduplicated rows (COVERED-BY-DEDUP): VL-22-167, 313, 530, 697, 840, 904 (all the `.gitignore:13` `lib/` defect, kept row DR-155, HARNESS) and VL-22-583 (judge skip rule, kept row VL-20-299, HARNESS).
Ledger 23 deduplicated rows (COVERED-BY-DEDUP, 38): VL-23-007 (kept DR-042 CORE), 100 (DR-107), 101 (DR-002), 102 (DR-006), 103 (DR-108), 104 (DR-014), 105 (DR-061), 106 (DR-109), 107 (DR-021), 109 (DR-111), 110 (DR-112), 111 (DR-113), 112 (DR-114), 113 (DR-059), 114 (DR-115), 115 (DR-116), 117 (DR-020), 118 (DR-118), 119 (DR-119), 120 (DR-120), 123 (DR-123), 124 (DR-124), 125 (DR-058), 126 (DR-010), 127 (DR-125), 128 (DR-126), 129 (DR-127), 147 (DR-055), 153 (DR-054), 468 and 611 (DR-133), 535 (DR-140), 576 (VL-24-519), 612 (DR-134), 624 (DR-145), 628 (DR-149), 630 (DR-154), 697 (DR-153). Every kept row is in Appendix A with a non-DROP destination except DR-153, whose DROP reason (the memory lesson "fenced yaml not parsed" is obsolete; executed read-only at HEAD) carries the substance of VL-23-697 (a lesson that the memory note is stale), so that substance is represented. Result: **no ledger row of 22 or 23 is missing, altered or sent to a destination without a recorded reason; none is an omission.**

Non-row items of ledgers 22 and 23 (Summary, Verification, Gaps, Questions; 28 + 27 = 55 items, `NONROW-COUNT` in the enumeration file): 49 represented, 6 omitted details (rows OM-33 to OM-38 below).

### Omissions Found

Every entry below is a distinct finding of an assigned file whose substance appears nowhere in the report (term search followed by reading of the owning passages). None is a decision, recommendation, value-inventory destination, conflict-log outcome or recommendation-bearing number, none is a required deliverable or section, and none is a security, data-loss or safety-boundary risk. Under `qa/grading-override.md` each is **minor under grading override** (the label column keeps the information label MINOR). Statuses COVERED-BY-DEDUP are listed after the OMITTED rows; no finding is JUSTIFIED-REMOVED.

| # | Source finding | Source file | Status (OMITTED / COVERED-BY-DEDUP / JUSTIFIED-REMOVED) | If deduped, by which report item; if JUSTIFIED-REMOVED, the fix-log entry and the code evidence | Severity |
|---|---|---|---|---|---|
| OM-1 | 12.48: design.md unattended contract detail (report 2.7 says only 'no protocol skill, no review, severity or cap'; 'There is no gate' and 'Nested invocations. None.' absent) | research/12-consumers-spec-review.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-2 | 12.67: limitation that review-panel-live7.md numbers were not opened by R12 (R14's live7 figures are carried at L467; the R12 limitation is not) | research/12-consumers-spec-review.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-3 | 12.68: limitation: rf-qa.md lines 402 and 549 cap mentions and the 185-line spawn census were not re-read by R12 (the census correction itself is carried) | research/12-consumers-spec-review.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-4 | 12.70: limitation that the tests were not run and test_f's rejection of a non-2 cap was read from source, not observed | research/12-consumers-spec-review.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-5 | 13.18: fsm.py defaults (DEFAULT_MONITOR 3, MIN_POLL_INTERVAL 30, timeouts 600/300, MAX_ROUNDS_ERROR string) absent; only the 2/5 round caps are carried | research/13-future-pr-review-and-rfqa.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-6 | 13.19: gate_arm (ordinal>=1), gate_edit (>=2) and the evaluate_push_decision condition list absent | research/13-future-pr-review-and-rfqa.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-7 | 13.21: seed_troubleshoot, batch_by_file, plan_dispatch truncation absent | research/13-future-pr-review-and-rfqa.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-8 | 13.27: pr-submit SKILL Will Not Do list (no headless run, no upstream push, no force push, no .claude add) absent (the fork rule itself is carried elsewhere) | research/13-future-pr-review-and-rfqa.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-9 | 13.34: auggie-review remediation chain (design, workflow, reflect pre, user-run implement, reflect post) absent | research/13-future-pr-review-and-rfqa.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-10 | 13.53: names of the 8 standard /task lenses absent (report says only '4 structural, 4 content') | research/13-future-pr-review-and-rfqa.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-11 | 13.101: gap: panel.py/ledger.py/cluster.py/verify_cmd.py/manifest.py bodies not read by R13 and findings_v2.py read to l.150 only absent | research/13-future-pr-review-and-rfqa.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-12 | 14.07: two different definitions of '3 unresolved prior CRITICAL+MAJOR labels' (R25,R27,R28 vs R25,R34,R36) absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-13 | 14.09: fixed-screen arithmetic (control mean 6, half 3, growth limit 44.457 from 0.7 x 63.51) absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-14 | 14.11: arm means 5.5 and 3.5 absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-15 | 14.13: comparator JSON copies under MEAS/diffgate/reviews/comparators not opened (limitation) absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-16 | 14.14: control/treatment growth means 63.5% / 29.7% / 30.0% absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-17 | 14.24: diffgate per-review arrays 13/5/3 new findings and CM 7/2/2 absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-18 | 14.27: ponytail per-review arrays 16/15/0 and CM 9/7/0 absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-19 | 14.29: cost figures (ponytail audit 18 calls/18,713 tokens; loops 274 calls/239,628; diffgate 186 tools/207,181) absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-20 | 14.31: ponytail orphan reference R3-N1 absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-21 | 14.67: historical incident row 18/10/8 and 92,194 bytes not recomputable absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-22 | 14.69: FINAL-REPORT-QA independent PASS cannot be reproduced absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-23 | 14.86: gap: comparator copies and raw control session transcripts not tried absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-24 | 14.87: gap: Claude Code version not recorded (2.1.319 in ponytail metrics) absent | research/14-e3-variants-and-experiments.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-25 | 15.28: E2 R-23 collab.json field list, R-24 +35% cap audit, R-30, R-46 absent | research/15-telemetry-manifest-run-record.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-26 | 15.31: blind-label keys must stay out of the scoring directory absent | research/15-telemetry-manifest-run-record.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-27 | 15.39: memory content is review output and belongs beside the run record by pointer, not inside it absent | research/15-telemetry-manifest-run-record.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-28 | 16.52: E1 PLAN mtime 46 minutes after the E2 owner's 'we are done testing' order absent | research/16-eval-governance.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-29 | 17.08: corrections-to-earlier-rows table (DR-006, 007/061, 054, 058, 053, 080 pin cells; DR-090 merged into DR-017) absent | research/17-defect-register.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-30 | 17.28: DR-053 note (test_review_cli.py:296-312 not read, not claimed as a pin) absent | research/17-defect-register.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-31 | 18.50: gap: docs searched for hooks/tests that enforce the rules (migration-skill.md, contributing-code.md, designs/spec-panel-review-loop.md) absent | research/18-repo-constraints-and-branching.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-32 | 18.58: doc claims that held (sync-discipline three gates, C1 pragmatic.md:224-229, C4/C5 pins) absent | research/18-repo-constraints-and-branching.md | OMITTED | n/a | MINOR (minor under grading override) |
| OM-33 | L22.10: verification of R1/R2 hook sites (seal block, turns_of, R2 run-package.sh writes DONE even when INVALID) absent | research/22-value-ledger-collab-designs.md (non-row) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-34 | L22.12: arithmetic re-derivations (0.30x116, C(12,4)=495, C(24,4)=10,626, Fisher p values) absent | research/22-value-ledger-collab-designs.md (non-row) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-35 | L22.27: Q8: can reflect Tier 2 reviewers be hooked at all or is resume the only collaboration path absent as a question | research/22-value-ledger-collab-designs.md (non-row) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-36 | L23.13: re-validate 7: code-engine swarm dispatch MODULE-reflect, survival CORE, V-38 proposes DROP or MERGE absent | research/23-value-ledger-e1-e3-code.md (non-row) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-37 | L23.18: G-3: _check_flat accepts an empty claim (no minimum length), no D-number absent | research/23-value-ledger-e1-e3-code.md (non-row) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-38 | L23.24: G-9: no executed baseline of tests/review; the 352-passed reflect result is a slice quotation absent | research/23-value-ledger-e1-e3-code.md (non-row) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-39 | GQ-123: slice 05 cites merged-spec.md lines; merged-requirements.md has the same text at line + 6 absent | gaps-and-questions.md (GQ-123) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-40 | GQ-137: E2 requirements assume findings-v1 and the study launcher; HEAD also has findings-v2 for reflect absent as a stated correction | gaps-and-questions.md (GQ-137) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-41 | GQ-262: counting rule for DROP duplicates (475 primary rows = 886 - 411 duplicate DROP) absent; the report states DROP totals and reasons | gaps-and-questions.md (GQ-262) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-42 | GQ-266: '2.75-3.25 more wrong blockers' is a three-comparator basis; BAD_CHECKS 'A none, E none' not quoted absent | gaps-and-questions.md (GQ-266) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-43 | GQ-328: contract_setup subpackage has nine modules (evidence.py, questions.py, states.py also) absent; the report names the subpackage only | gaps-and-questions.md (GQ-328) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-44 | GQ-332: model swap visible only in fallback.log while final meta.json shows the fallback model absent | gaps-and-questions.md (GQ-332) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-45 | GQ-336: launch-level-guard requires a non-empty --repo operand absent | gaps-and-questions.md (GQ-336) | OMITTED | n/a | MINOR (minor under grading override) |
| OM-46 | GQ-341: 8 packaged panel templates (2 spec, 6 reflect) plus the tier file correction absent | gaps-and-questions.md (GQ-341) | OMITTED | n/a | MINOR (minor under grading override) |

COVERED-BY-DEDUP rows (not omissions; the substance is carried by the kept row named):

| # | Source finding | Source file | Status | Kept row (report item) | Severity |
|---|---|---|---|---|---|
| DD-1 | VL-22-167, VL-22-313, VL-22-530, VL-22-697, VL-22-840, VL-22-904: `.gitignore:13` `lib/` hides the engine of R2, r3, r4, r5 | research/22 | COVERED-BY-DEDUP | DR-155 (HARNESS), Appendix A L3640 area; Section 8.1.2 rows | n/a (not an omission) |
| DD-2 | VL-22-583: judge retry/skip rule | research/22 | COVERED-BY-DEDUP | VL-20-299 (HARNESS), P3-011 table in 8.1.3 | n/a (not an omission) |
| DD-3 | VL-23-007, 100-107, 109-115, 117-120, 123-129, 147, 153, 468, 535, 576, 611, 612, 624, 628, 630, 697 (38 rows): ledger-23 restatements of register defects | research/23 | COVERED-BY-DEDUP | DR-042, DR-107, DR-002, DR-006, DR-108, DR-014, DR-061, DR-109, DR-021, DR-111, DR-112, DR-113, DR-114, DR-059, DR-115, DR-116, DR-020, DR-118, DR-119, DR-120, DR-123, DR-124, DR-058, DR-010, DR-125, DR-126, DR-127, DR-055, DR-054, DR-133, DR-140, VL-24-519, DR-134, DR-145, DR-149, DR-154, DR-153 (section 8.1.2 rows; 8.1.3 P3-011 and P3-012 tables) | n/a (not an omission) |
| DD-4 | 43 defect-register rows (DR-nnn marked `DROP: duplicate of VL-NN-nnn`, UNVERIFIED register rows): register rows whose ledger twin is kept | research/17 | COVERED-BY-DEDUP | the kept ledger row named in each row's Reason (list in the enumeration file, research/17 section) | n/a (not an omission) |

Detail-level partials (not omissions; the finding is carried and only a sub-detail is not): 12.27 (V9 synthetic HIGH carried at L669, "fixed, non-overridable" wording absent), 13.07 (five PushDecision predicates not listed), 13.11 (six-step order of `remap_severity` not carried), 13.30 (auggie-only/claude-only/both source tag), 13.33 (never-approve rule of auggie-review), 13.35 (deep-mode cost figures), 14.78 (column-1 grammar as a fourth finding format), 15.45 (per-consumer derivation rows), L22.04 (MODULE-spec zero-row note; carried by rows VL-22-044 and VL-22-198 in Appendix A). They are marked in the enumeration file and are not counted as omissions.

### Pair check: ledger 23 against the defect register (`research/17-defect-register.md`, rows `DR-nnn`)

Rule applied (assignment): for a defect enumerated in both a ledger-23 row and a defect-register row, Section 8.1 must carry ONE row with a single destination (the register destination when the register re-verified it), the other marked `DROP: duplicate of <ID>`; one defect in 8.1 twice with two different destinations is an IMPORTANT finding.

Method: (1) join of the VL-23 Source cites to the register's `slice:line` cites: 64 cite pairs involving 48 register rows, none with both rows kept; (2) the reason pointers: 38 VL-23 rows are `DROP: duplicate of DR-nnn` and 11 register rows are `DROP: duplicate of VL-23-nnn`; every kept target exists in Appendix A with a non-DROP destination (the one exception, VL-23-697 against DR-153, is described above: both are DROP and the register row carries the substance); (3) a text-similarity scan of the 608 non-DROP VL-23 rows against the 118 non-DROP register rows, and a reading of all 34 non-DROP VL-23 rows of kind `defect` and of the 45 non-DROP register rows that cite slices 09 to 11.

Result:

| # | Defect | Ledger-23 row (kind, destination, Appendix A line) | Register row (destination, Appendix A line) | Finding |
|---|---|---|---|---|
| PC-1 | `annotate` raises `KeyError` on a citation-only v2 finding (D-12) | VL-23-035 (defect, CORE, L526) | DR-113 (CORE, L982) | same destination; two kept rows. Section 8.1.2 already lists the pair as "context only" and states the withdrawn fix |
| PC-2 | `telemetry._ID_TOKEN` is a copy of `findings._REF_TOKEN` | VL-23-080 (defect, CORE, L560) | DR-007 (CORE, L935; moved from MODULE-tasklist, recorded in 8.1.3) | same destination; two kept rows |
| PC-3 | code engine emits `contract_version "1.0"` | VL-23-437 (defect, MODULE-reflect, L1151) | DR-128 (MODULE-reflect, L1262) | same destination; 8.1.4 limit 3b names DR-128 only against VL-23-449 |
| PC-4 | code-engine reviewers see only the tasklist body | VL-23-439 (defect, MODULE-reflect, L1153) | DR-131 (MODULE-reflect, L1264) | same destination |
| PC-5 | code engine hard-codes `merge_method` by reviewer count | VL-23-442 (defect, L1156) and VL-23-443 (finding, L1157), both MODULE-reflect | DR-129 (MODULE-reflect, L1263) | same destination |
| PC-6 | stale `cli/reflect/__init__.py` docstring | VL-23-458 (defect, MODULE-reflect, L1167) | DR-142 (MODULE-reflect, L1271) | same destination |
| PC-7 | runner comment says `--no-promote` is the hard default, Click default is `--promote` | VL-23-459 (defect, MODULE-reflect, L1168) | DR-144 (MODULE-reflect, L1273) | same destination |
| PC-8 | `reflection-rubric.md` names old deviation classes; open capability-ordering question | VL-23-496 (defect, L1184), VL-23-497 (question, L1185), both MODULE-reflect | DR-136 (L1266), DR-137 (L1267), both MODULE-reflect | same destination |
| PC-9 | HEAD-relative pins in `test_shadow_skill_contract.py` guard only uncommitted edits | VL-23-531 (defect, MODULE-reflect, L1187) | DR-141 (MODULE-reflect, L1270) | same destination |
| PC-10 | `--t2-engine` missing from the reflect command file and CLI; `--reviewers` clamp | VL-23-577 (finding, L1220), VL-23-603 (constraint, L1233), both MODULE-reflect | DR-145 (L1274), DR-150 (L1276), both MODULE-reflect | same destination |
| PC-11 | dead API (`channel_of`, `read_committed`) | VL-23-067 (contract, CORE, L549), VL-23-187 (contract, MODULE-reflect, L1049) | DR-120 (CORE, L988) | VL-23-067 same destination; VL-23-187 differs, but it is the CHANNELS contract row that mentions `channel_of` only in passing (different kind of fact) |
| PC-12 | Stage 2 shadow-exit result (8 of 13 shadow runs fail EV-1 against 3 of 39 legacy) | VL-23-505 and VL-23-519 (evidence, EVAL, L2983 and L2997) | DR-138 (MODULE-reflect, L1268) | different destinations, different kinds (measured result rows against a defect row); named in 8.1.4 limit 3b (DR-138 with VL-23-510, 511, 513), not VL-23-505 or 519 |
| PC-13 | untracked `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md` | VL-23-664 (artifact, KNOWLEDGE, L4029), VL-23-788 (question, KNOWLEDGE, L4035) | DR-154 (HARNESS, L3640; REPRODUCED) | different destinations, different kinds (artifact fact and a gap question against the hygiene defect); 8.1.4 limit 3b names DR-154 with VL-23-664; VL-23-630 and VL-24-167 were already re-routed to DROP duplicates of DR-154 |

Grading: PC-1 to PC-11 carry one defect in two kept rows with the SAME destination; the destination of each defect is unambiguous, so no destination in the value inventory is wrong or unsupported and no number the recommendation rests on changes (the 5,950 rows are the inventory's own count, which says "one inventory row per input row" and lists the duplicate-marking limits in 8.1.4). PC-12 and PC-13 are related rows of a different kind with different destinations and are disclosed in 8.1.4 limit 3b in part; none is the same defect statement restated with a competing destination. **No IMPORTANT finding of the "one defect, two different destinations" type exists in this partition.** All of PC-1 to PC-13 are minor under grading override (information label MINOR to IMPORTANT for PC-12 and PC-13); they belong on the follow-up list as "mark the second row `DROP: duplicate of <ID>` in a later pass of synth-08".

### Per-File Counts

| File | distinct findings enumerated |
|---|---|
| research/12-consumers-spec-review.md | 74 |
| research/13-future-pr-review-and-rfqa.md | 110 |
| research/14-e3-variants-and-experiments.md | 97 |
| research/15-telemetry-manifest-run-record.md | 60 |
| research/16-eval-governance.md | 61 |
| research/17-defect-register.md | 200 (171 register rows `DR-001` to `DR-171` plus 29 non-row items) |
| research/18-repo-constraints-and-branching.md | 59 |
| gaps-and-questions.md | 555 (`GQ-001` to `GQ-555`) |
| synthesis/synth-01-problem-current-state.md | 497 (substantive lines; headings and meta lines excluded) |
| synthesis/synth-02-overlap-matrix.md | 203 |
| synthesis/synth-03-target-gaps.md | 345 |
| research/22-value-ledger-collab-designs.md | 955 rows (`grep -c '^| VL-22-'` = 955) plus 28 non-row items |
| research/23-value-ledger-e1-e3-code.md | 796 rows (`grep -c '^| VL-23-'` = 796) plus 27 non-row items |
| **Total** | **4,067** (the two ledgers' 55 non-row items are in the total) |

These equal the `COUNT <file name>: <n>` lines of the enumeration file (ledger lines 955 and 796; the non-row items of the ledgers are on the line `NONROW-COUNT ...: 55`).

### Summary

- Findings enumerated: **4,067**.
- Represented: **3,724** (includes the 9 detail-level partials above, the 30 + 2 ledger rows moved with a recorded reason, the 10 register rows that are `DROP` with a stated reason, and the logged-open and resolved gap rows carried in Section 9 and the owning sections).
- COVERED-BY-DEDUP: **88** (45 ledger rows of 22 and 23 marked `DROP: duplicate of <ID>` with the kept row present, and 43 register rows marked duplicate of a kept ledger row); in addition 209 gap rows are pointer rows covered by the ledger row they name (Appendix A).
- JUSTIFIED-REMOVED: **0** (the Gate 3 and Gate 4 fix logs record no removal).
- OMITTED: **46**, all minor under grading override (research 12: 4; 13: 7; 14: 13; 15: 3; 16: 1; 17: 2; 18: 2; non-row ledger items: 6; gap rows: 8). Blocking omissions under the override: **0**.
- Also verified: per-destination counts of ledger 22 (107, 4, 94, 0, 4, 1, 287, 167, 47, 244) and ledger 23 (253, 216, 6, 9, 4, 2, 74, 19, 25, 188) recomputed from Appendix A equal the 8.1.0 table; all 171 register rows are in Appendix A with an equal Statement; synth-01 to synth-03 (1,045 substantive lines) occur verbatim in the report.
- Pair check (ledger 23 against the defect register): 11 same-destination duplicate pairs (PC-1 to PC-11) and 2 different-kind related pairs with different destinations (PC-12, PC-13); zero IMPORTANT "two destinations for one defect" findings; all minor under override.
- Limits: the term search is not a proof for detail-level findings; the report's absence of a detail was confirmed with at least two distinct search terms and reading of the owning section. Research-file findings were enumerated by hand (one entry per claim), so the counts of files 12 to 16 and 18 depend on that unit.

**Verdict: PASS** (zero blocking omissions under `qa/grading-override.md`; 46 minor omissions and 13 minor pair-check notes go to the follow-up list).

Status: Complete
Cleanup: scratch scripts were kept only under `/tmp/ao3-work/` (read-only analysis); no repository file other than this report and the enumeration file was written.
