## Completeness QA Report

**Report:** `RESEARCH-REPORT-orchestrator-mode.md` (1651 lines)
**Lens:** Completeness (one dimension only)
**Date:** 2026-11-07
**Fix authorization:** false (no file other than this one edited)
**Inputs read:** report, `research/research-notes.md`, `gaps-and-questions.md`, Glob of `research/` and `synthesis/`, Key Takeaways of every research file.

## Checklist results

| Check | Result | Evidence |
|---|---|---|
| (a) Every scope-discovery topic in `research-notes.md` appears in the report | PASS with notes | Grepped the report for each scope topic (data sources, excluded set, class precedence, window, report skeleton, AMBIGUITIES 1-11, C1-C15, K1-K4, CLI patterns, registries, lint/ruff, WRITE_VERB_CLASSIFICATION, setup-gate wording, APPROVED.md, CR-01, #422, pragmatic exception, management server, WC-13, pane-key join, parse_session_log, read verbs, `check --wait`): all found. Five minor topics have zero hits (findings 5-9). |
| (b) Every gap resolved in S8 or listed in S9 | PASS with notes | All 75 open GQ IDs are in S9.1; the 25 resolved are in S8.1 / S9.6; S-01 to S-14 in S9.3; AMB 1-11 in S9.5; C-items and D1-D4 in S9.4 or via their GQ rows; X-1 to X-12 resolved in S8.4. One S7 contradiction (`:1078`) is in neither S8 nor S9 (finding 4). |
| (c) S10 lists every research and synthesis file | PASS for research and synthesis; FAIL for the QA list | Glob of `research/` (10 files) and `synthesis/` (6 files): all appear at `:1611-1640`, and research line counts match `wc`. The S10 QA list (`:1650`) claims 24 files and omits the 18 Phase 5 synthesis-gate QA files (finding 1). |
| (d) Every research Key Takeaway reflected or excluded with a reason | PASS with notes | No research file has a heading named "Key Takeaways"; their Summary / Key External Findings / Recommendations sections were checked. web-01 KF1-7 and Rec 1-6, and web-02 KF1-6 and Recs (observation time, drop-out is not finished, oldest-first with an unknown-age group, shown/total and unknown total, if-then line, Grafana rejected) all have report hits (17 hits for the age / observation / drop-out terms alone). The phi-accrual exclusion has a reason at `:1367`. No explicit coverage table (finding 13). |

## Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | S10 QA reports (`:1650`) | False count and missing deliverables: "`qa/` (24 files)" lists only research-phase and task-validation reports. The 18 Phase 5 synthesis-gate QA files, which existed before assembly, are not listed: `analyst-synthesis-accuracy-1/2`, `analyst-synthesis-tracing-1/2`, `qa-consolidated-findings-phase5`, `qa-consolidated-findings-phase5-cycle1`, `qa-synthesis-content-1/2`, `qa-synthesis-qualitative-report-1/2`, `qa-synthesis-structure-1/2`, `qa-synthesis-fix-log`, `qa-synthesis-fix-log-cycle1`, `qa-synthesis-verification`, `qa-synthesis-verification-cycle1`, `qa-synthesis-verification-qualitative`, `qa-synthesis-verification-qualitative-cycle1` (Glob `qa/*synthesis*` returned 16, plus the 2 phase5 consolidated files). The evidence trail therefore hides the synthesis gate and its fix cycle. | Add a "Phase 5 synthesis gate" bullet naming these 18 files, and correct the count (42 pre-assembly files plus `qa-nb4-fix-log.md`, not counting the post-assembly `qa-lens-*` reports). |
| 2 | MINOR | S10 Synthesis files (`:1639-1640`) | Stale annotations copied from synth-06: synth-05 "(planned; not yet written...)" and synth-06 "(this file)". The assembler note at `:1642` corrects synth-05, but the list still reads wrong. Synthesis entries also have no line counts, unlike the research entries. | Drop both annotations and add line counts (299, 317, 230, 275, 310, 233). |
| 3 | MINOR | S10 Gaps Log (`:1646`), S9.1 row 61 (GQ-97) | "re-checked at the Phase 5 synthesis gate" and "Re-cite at the Phase 5 synthesis gate" are in future tense, but the gate has run (finding 1). Its result is not recorded. | State the gate outcome for GQ-03 and GQ-97, citing the synthesis verification file. |
| 4 | MINOR | S7 (`:1078`) vs S8 / S9 | The [CONTRADICTION] on the HOW-WE-WORK "Other commands" range (`:314-337` in synth-04 vs `:318-337` at SC-11, `:433`) is not carried into S8.4 or S9.4. It is a line-range discrepancy on a true claim, so it is minor. The marker is left in place as instructed. | Add one row to S9.4 naming both ranges and "re-read HOW-WE-WORK.md before step 1.21". |
| 5 | MINOR | Scope coverage (a) | The `tests/unit/test_cli_install.py` install presence check (`research-notes.md:88`, "4 named commands only") and scope-03's "sync, help and install need no list edits" have no report hit. A grep for sync-dev / help / install found only `:437`, `:502`, `:1076`, `:1223`, `:1420`, `:1451`. | Add one line to the S8 registry steps (1.20-1.28) saying no install-list edit is needed and why. |
| 6 | MINOR | Scope coverage (a) | The `ensure_ascii` / JSON-echo convention (`research-notes.md:130`) is absent; there is only one `json.dumps` hit. | Name the convention in step 1.6 (CLI output) or exclude it with a reason. |
| 7 | MINOR | Scope coverage (a) | The worker-contract mapping tables in the sc-brainstorm / graph / impact protocols (`research-notes.md:66-67`) are not mentioned. | Mention them as prior art for the WC-14 wording, or exclude them. |
| 8 | MINOR | Scope coverage (a) | The CI ruff steps (`.github/workflows/test.yml:100-106`, `.pre-commit-config.yaml`) are absent; only generic "ruff check/format" appears (2 hits). | Cite them in the lint step so the executor knows CI runs both. |
| 9 | MINOR | Scope coverage (a) | The `launch-level` identity file path from 07 B-04 is absent; `:525` only says launch-job-identity sets no env var. | Add the path to the identity row or to S9.2. |
| 10 | MINOR | Gaps register vs web files | The "Files read" list at `gaps-and-questions.md:9-14` omits web-01 and web-02. The web files have no gaps sections (noted in S9.7), and their discrepancies reach the report through D1-D4 and rows 94-98, so nothing is lost. The register's coverage claim is still incomplete. | Note in S9.7 that the register did not read the web files and that the D1-D4 / Grafana rows stand in for them. |
| 11 | MINOR | S9.2 | Section (e) items `05:125`, `06:102` and `06:144` are not listed separately; they map to GQ-15, GQ-50 and GQ-58. | Add the mapping in one line. |
| 12 | MINOR | S9.1 row 9 (GQ-11) | "word WC-14 so it does not override WC-1" misstates the question. The question is WC-14 versus amending WC-1, as OQ-11 at `:1340` puts it. | Reword to match OQ-11. |
| 13 | MINOR | S9.7 (`:1603`) | "A file without a Key Takeaways list is not a defect" waives check (d). There is no table mapping takeaways to sections, only a gaps coverage map. A manual check found the takeaways reflected. | Add a short takeaway coverage column to S9.7. |
| 14 | MINOR | S10 (`:1626`) | Says "Phase 4 web research"; `research-notes.md` calls it Phase 3. | Use the research-notes phase number. |
| 15 | MINOR | S10 | `BUILD-REQUEST.md`, the task file and `baseline-git-status.txt` are not listed. | Add an "Inputs" bullet. |

Note on the required markers: the `:1507` [CONTRADICTION] (allowed-tools colon form vs space form) is inside S9.1, so it is listed as open, which satisfies completeness. The NB-4 research-gate exception is recorded at S9.6 and `:1651`. Neither marker was removed.

## Summary

- Findings: 15 (CRITICAL: 0, IMPORTANT: 1, MINOR: 14)
- Blocking: 1 (finding 1: the S10 QA inventory is a false count and omits the 18 synthesis-gate QA reports)
- Minor findings are recorded as notes and do not on their own fail the review.
- Checks: (a) PASS with notes, (b) PASS with notes, (c) FAIL (QA list only), (d) PASS with notes
- The adversarial expectation of 16 or more errors was not met: 15 were found. Every scope topic, gap ID and web takeaway that was checked is accounted for, apart from the items listed above.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: about 30 | Grep: about 28 | Glob: 4 | Bash: 2 (wc line counts, read-only). These counts are approximate because the session context was compacted mid-review. No web research was done.

Verdict: FAIL

