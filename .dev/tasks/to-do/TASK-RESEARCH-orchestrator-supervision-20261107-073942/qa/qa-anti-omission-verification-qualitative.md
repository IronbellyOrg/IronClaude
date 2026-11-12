# QA Report: Anti-omission verification (qualitative), after fix pass 1

**Topic:** Orchestrator mode Phase 1 (issue #339) research report
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative lens), anti-omission gate, review after fix pass 1
**Fix cycle:** 1
**Fix authorization:** false (report only; the report was not edited)

**Inputs read:**
- Report: `RESEARCH-REPORT-orchestrator-mode.md`
- Consolidated findings: `qa/qa-anti-omission-consolidated-findings.md` (|F_0| = 18, all RECOVER)
- Fix log: `qa/qa-anti-omission-fix-log.md` (18 of 18 claimed recovered)

_Status: in progress; sections are appended as the review proceeds._

## 1. Status of each blocking omission (AO-01 to AO-18)

The consolidated findings mark no blocking omission JUSTIFIED (all 18 are RECOVER), so no JUSTIFIED disposition can hide a load-bearing finding. I checked every row below in the report text, not in the fix log.

| ID | Status | Where it sits now (report line) | Placement right? | Notes |
|---|---|---|---|---|
| AO-01 | RECOVERED (plan integration incomplete, see NB-1) | 3.1 safe-to-close, "One package in two worktrees" (421); step 1.3 rule (i) (1244); fixture 1.8 (1254); test 1.9 (1255) | Yes | The quoted sentence matches `WORKER-CONTRACT.md:108` as cited by scope-01. Step 1.2 has no field for it, and the `safe_to_close` signature cannot compute it (NB-1). |
| AO-02 | RECOVERED | 3.1 Report rules "Fan-in groups" (455); WC-14 G5 (461); step 1.5 (1246); step 1.17 G5 (1274) | Yes | "partial" counts as "usable not yet judged", which is consistent with rule 6 (394) and step 1.3 rule 6. |
| AO-03 | RECOVERED | 3.1 "Worktree removed mid-sweep" (469); step 1.4 rule (a) (1245); fixture 1.8; test 1.9 | Yes | Gives could not determine plus `unscanned:`, with exit 0. A vanished path is not treated as death. |
| AO-04 | RECOVERED | 3.1 skeleton (434); Report rules "set union" (451); step 1.5; test 1.12 (1258) | Yes | |
| AO-05 | RECOVERED | 3.1 WC-14 G1 candidate clause [UNVERIFIED] (457); step 1.17 (1274) | Yes | Recorded, not adopted. The sweep never passes `--terminal-state`. Minor note M-5: the [UNVERIFIED] guard is not listed in 8.2 or S9; step 1.17 defers that to implementation time. |
| AO-06 | RECOVERED | 3.1 "Context-only Dispatches" (411); step 1.3 rule (ii); fixture 1.8; test 1.9 | Yes | Minor note M-1 covers where the rule sits in the precedence. Step 1.2 has no "unsupervised" field (NB-1). |
| AO-07 | RECOVERED (plan integration incomplete, see NB-1) | 3.1 "Package states" (412); step 1.3 rule (iii); step 1.4 rule (c); fixture 1.8; test 1.9 | Yes | The tests require the strings "archive-blocked" and "interrupted archive" to print. Neither step 1.2 nor step 1.5 says which field holds them or where they print (NB-1). |
| AO-08 | RECOVERED (as a recorded [CODE-CONTRADICTED]) | Step 1.22 (1284); rollback "Four registries" (1312) | Yes | I re-read `tests/core/test_how_we_work_routing_table.py:54-55` ("A row may be added; none of these may be renamed or removed.") and `:204` (`_EXPECTED_IDS <= set(ids)`); the contradiction is real. It does not contradict SC-11 (485): SC-11 names the "Other commands" row and `_OTHER_COMMANDS`, not a routing-table row, and step 1.21 adds only an "Other commands" row. |
| AO-09 | RECOVERED | 3.1 "Imported evidence is inert" (452); step 1.5; test 1.12 | Yes | |
| AO-10 | RECOVERED | Step 1.5 per-column sources (1246) | Yes | Every B-14 column now has a source and a no-source value. Minor note M-6: the 4.2 "Static report writer" row (553) still gives only a summary. |
| AO-11 | RECOVERED | 3.1 skeleton (433); Report rules "Explicit-questions table (a)" (449); step 1.5 | Yes | |
| AO-12 | RECOVERED | 3.1 skeleton (432); Report rules (450); step 1.5; test 1.12 | Yes | |
| AO-13 | RECOVERED | 3.1 Report rules "Source loss changes nothing" (453); SC-7 (481); step 1.5; test 1.12 | Yes | Strengthens WC-10: a lost source never turns a row finished, failed, not frozen or retry-recommended. |
| AO-14 | RECOVERED | 3.1 "Ownership and coverage limits" (367); step 1.3 rule (iv) | Yes | Minor note M-2: there is no fixture or test. The fix log (row 33) says steps 1.8 and 1.9 cover it, but the report itself says "Tests for (i)-(iii) in step 1.9". |
| AO-15 | RECOVERED | 3.1 (368); step 1.3 rule (iv) | Yes | Minor note M-2: `linked: true` comes from `reference find`, which is not on the step 1.4 allowlist, so in Phase 1 every peer Owner prints "unknown". That is safe, but the report does not say so, and there is no test. |
| AO-16 | RECOVERED | 3.1 (369); step 1.4 rule (b); fixture 1.8; test 1.10 (1256) | Yes | "not covered" gives could not determine, never "no sessions". Consistent with WC-10. |
| AO-17 | RECOVERED | 3.1 "Recommendations only" (467); step 1.15 (1266); step 1.17 (1274); 9.4 row 98b (1666) | Yes | Row 98b lists safe-to-close REVIEW, the "new Task" resume and WC-14 item 8 among the recommendations it covers, and gives the drop rule. The steps were not removed. Minor note M-3: the [CONTRADICTION] paragraph at 283 still names only two positions. |
| AO-18 | RECOVERED | 3.1 skeleton Scope line (429); Report rules (454); step 1.5; test 1.12 | Yes | |

**Tally:** RECOVERED 18, JUSTIFIED 0, OPEN 0. The AO-01 and AO-07 recoveries, and part of AO-06, leave the plan internally inconsistent. I record that as new blocking finding NB-1 in Section 2, not as an OPEN omission, because the omitted source facts are now in the report.

## 2. New findings introduced by the recoveries

### Blocking

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| NB-1 | IMPORTANT (internal contradiction between plan steps) | Step 1.2 (1243) vs step 1.3 rules (i)-(iii) (1244), step 1.5 (1246) and tests 1.9 (1255) | Fix pass 1 added classifier rules (i)-(iii) to step 1.3 and test cases to step 1.9. It did not touch the data model of step 1.2 or the renderer of step 1.5, which step 1.3 depends on ("every type named here is a dataclass in `models.py` (step 1.2)"). This causes three breaks. (1) Rule (i), one package in two worktrees: `safe_to_close(row: SessionRow, worktree: WorktreeState \| None)` sees one worktree, and `WorktreeState` carries no package ids. As specified, the function cannot detect a package that is also under a second root, but test 1.9 asserts that both worktrees print "removable: no". (2) Rule (iii), package states: `WorktreeState` has only `ledger_unfinished`, with no field for archive-blocked or the `.archiving` marker. Step 1.5 names no column or section where "archive-blocked" prints, and its Retained problems list does not include "interrupted archive" or the two-worktree pair. Tests 1.9 still assert that those strings print. A grep of step 1.2 for `archiv`, `package`, `unsupervised` and `retained` returns no match; "interrupted archive" occurs only at 412, 1244 and 1255. (3) Rule (ii), context-only Dispatch: `OrcaObservation` has no field for "unsupervised" or terminal state `retained`, so `classify` has nothing to test. A developer who follows 1.2, 1.3 and 1.5 in order writes 1.9 tests that cannot pass against the specified types and renderer. | In step 1.2, add the fields the recovered rules read. For example (plan decision, new design): `WorktreeState.package_ids: tuple[str, ...]`, `archive_state: str \| None` ("archive-blocked" / "interrupted archive" / None), and `OrcaObservation.unsupervised: bool \| None` plus `terminal_state: str \| None` (for the safe-to-close half only, never the class). State that the two-worktree check is a pre-pass over all `WorktreeState` records before `safe_to_close`, or widen the signature to take the full worktree list. In step 1.5, name where the package state prints (a Worktrees column or a Retained problems line), and add "interrupted archive" and the two-worktree pair to the Retained problems rendering. |

No other recovery introduced a contradiction between sections. Checks that came back clear:
- **AO-08 vs SC-11 and step 1.21:** consistent (Section 1 row AO-08).
- **AO-17 vs line 283, step 1.15, step 1.17 and row 98b:** consistent. All four put the drop rule under one owner decision.
- **AO-05 vs SC-2:** the sweep never passes `--terminal-state`, and step 1.4's allowlist (1245) has no such flag.
- **AO-13 vs SC-7 (481):** consistent ("source read, item absent" vs "source lost").
- **AO-02 vs rule 6 (partial):** consistent.

### Minor (notes; they do not fail the review)

| # | Location | Note |
|---|---|---|
| M-1 | 3.1 (411), step 1.3 rule (ii) | The context-only rule lets only rules 1 and 6 override could not determine, so it skips rules 3 and 4 for such rows. The precedence diagram (373-399) does not show where the exception sits. The outcome is conservative (could not determine, listed under Retained problems), and the policy dimension is still computed for every row, so nothing is hidden as absent. Name the exception's position in the diagram. |
| M-2 | 3.1 (367-368), step 1.3 rule (iv) | (a) Rule (iv) has no fixture or test, but fix log row 33 claims steps 1.8 and 1.9 cover AO-14 and AO-15. The report itself correctly limits its tests to (i)-(iii). (b) `linked: true` is read from `reference find` (368), which is not on the step 1.4 allowlist, so Phase 1 always prints peer Owner "unknown". Say so in step 1.4 or 1.5. |
| M-3 | 283 | The [CONTRADICTION] paragraph names rule 5 and the seed brief but not the third `06:138` position that 467 and row 98b now carry. A forward reference to 467 would do. |
| M-4 | SC-11 (485) vs step 1.21 (1283) | SC-11 still says "unless GQ-24 places sweep in the excluded set", while step 1.21 says "GQ-24 decided". This predates fix pass 1. |
| M-5 | 457, 1274 | The [UNVERIFIED] turn guard (AO-05) goes to Open Questions only at implementation time. It is not in 8.2 or S9 now, although its status is already unverified. |
| M-6 | 4.2 row "Static report writer" (553) | This row still summarises the writer and does not point to the per-column source list now in step 1.5. |

## 3. Adversarial re-grade of the MINOR omission rows

I took the adversarial stance and assumed that at least 5 omissions were missing or wrongly justified. The consolidated findings justify none of the 18 blocking omissions, so the only place a load-bearing finding could hide is the 30 MINOR rows that were never recovered. I re-graded each MINOR row against what the sweep reads, calls and prints in the plan:

- **R2 row 25** ("absence never authorizes action"). This would be load-bearing for WC-10, but the report already states the rule at 453 (Source loss), 759 and 856. It is not lost, so MINOR stands.
- **R1 rows 17, 18 and 24; R2 rows 13, 22 and 23.** These cover `worker_status: failed` writes, `lastFailure` parsing, `ccsession --here`, event dedup, and `--peek` and peek identity. The Phase 1 sweep does not read `lastFailure`, never calls `check`/`peek`, never calls `ccsession`, and is not on the step 1.4 allowlist for any of them. None can change a printed classification, so MINOR stands.
- **R2 row 17** (join on stable IDs, never display names). No name-based join appears in steps 1.2-1.5; the mapping is by worktree path and run/Task id. MINOR stands as a note. A one-line guard in step 1.3 would cost nothing.
- **R1 rows 15, 16, 19-23, 25-27; R2 rows 12, 14-16, 18-21, 24; R3 rows 1 and 5; R4 row 1.** These are wording, naming, formatting or provenance items. None is a defect in behaviour, so MINOR stands.

Result: no MINOR row is a wrongly graded blocking omission. The adversarial search instead found one blocking defect introduced by the recovery itself (NB-1) and six minor notes (M-1 to M-6), which together make seven findings, more than the 5 the stance assumed.

## 4. Global coherence checks

| # | Check | Result | Evidence |
|---|---|---|---|
| G-1 | WC-10 (absence of a signal is never proof of death) preserved by every recovery | PASS | The recovered text at 369 (`not covered` gives could not determine, never "no sessions"), 411 (context-only rows are never working/stalled from liveness), 453 (source loss resolves, fails, unfreezes and retries nothing) and 469 (vanished worktree gives could not determine plus `unscanned:`) all turn missing data into could not determine. None turns it into dead, finished or releasable. |
| G-2 | No recovery recommends option A4 | PASS | Grep for `\bA4\b` (this pass): every hit is "rejected" or [CODE-CONTRADICTED] (26, 165, 323, 576, 607, 608, 622, 872, 1053, 1077, 1381). No recovered line mentions A4. |
| G-3 | No recovery designs a later phase instead of recording it | PASS | Every recovery lands in 3.1 or in Phase 1 steps 1.3-1.22. The later-phase section (1320-1332) was not touched by the fix log (rows 14-36 name no later-phase target), and AO-17 records the `06:138` conflict as an owner decision (row 98b) without designing Phase 2 behaviour. |
| G-4 | Protected markers intact | PASS | `CONTRADICTION` = 6 and `NB-4` = 23 (Grep count, this pass), which match the fix log baseline (fix log line 6). |
| G-5 | No JUSTIFIED disposition hides a load-bearing finding | PASS | No blocking omission is JUSTIFIED (consolidated findings line 6). The MINOR re-grade in Section 3 found no hidden blocking row. |
| G-6 | No recovery introduced a contradiction between sections | FAIL | NB-1. Steps 1.3 and 1.9 now require fields and print locations that steps 1.2 and 1.5 do not define. |

## 5. PASS set

- **Blocking omissions RECOVERED and correctly placed (18):** AO-01 to AO-18. AO-01, AO-06 and AO-07 are recovered in 3.1 and step 1.3, but their plan integration is incomplete (NB-1).
- **Global checks PASS (5):** G-1 WC-10, G-2 no A4, G-3 later phases recorded only, G-4 markers intact, G-5 no hiding JUSTIFIED disposition.
- **Cross-section consistency PASS:** AO-08 vs SC-11/step 1.21; AO-17 vs 283/1.15/1.17/98b; AO-05 vs SC-2; AO-13 vs SC-7; AO-02 vs rule 6.
- **Not in the PASS set:** G-6 (NB-1).

## Confidence Gate

- **Items:** TOTAL 24 = 18 AO rows + 5 global checks from the task (WC-10, A4, later phases, contradiction, JUSTIFIED) + 1 MINOR re-grade.
- **Confidence:** Verified: 24/24 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 5 | Glob: 0 | Bash: 9 (approximate; the counts from before this session's context compaction are reconstructed). **Flag:** Read + Grep + Glob = 16 is below TOTAL 24, which the protocol calls suspect. Most of the 9 Bash calls were bounded read-only `sed -n`/`grep` reads of single report lines (the report exceeds the Read token limit at wide offsets), and several Read calls covered more than one item. One report Read range at offset 1187 failed for size and was replaced by line-level reads.
- UNCHECKED items: none. UNVERIFIABLE items: none.
- Web research: none performed, so Tavily was not needed.

## Self-Audit

No `## Inherited Structural Verdict` block was supplied with this task. I therefore ran standalone and relied on the inputs below without re-deriving them.

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on the fix log's term-check counts (fix log line 42) to confirm that each recovered string exists. I did not re-grep all 19 terms, only the ones a finding depends on ("interrupted archive", `archiv`, `package`, `unsupervised`, `retained`).
- Relied on the consolidated findings' MINOR grading for the 30 unrecovered rows as the starting point. I re-graded them myself (Section 3) rather than accepting them.
- Relied on the source-file citations in the fix log (for example `WORKER-CONTRACT.md:108` and `scope-04:334-351`) for the source wording. I did not re-open the research files except where a finding turned on them.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- AO-08 contradiction: verified by Reading `tests/core/test_how_we_work_routing_table.py:54-55` ("A row may be added; none of these may be renamed or removed.") and `:204` (`assert _EXPECTED_IDS <= set(ids)`). The [CODE-CONTRADICTED] record is correct, and the source's "needs adding" claim is false.
- NB-1 data-model gap: verified by reading step 1.2 (1243) and grepping it for `archiv`, `unsupervised`, `package`, `linked` and `retained` (0 hits), and by checking that the `safe_to_close(row: SessionRow, worktree: WorktreeState | None)` signature in step 1.3 (1244) takes one worktree.
- Step 1.5 print locations: verified by reading 1246 that Owner and the B-14 columns are defined, and that no column or Retained problems line holds "archive-blocked", "interrupted archive" or the two-worktree pair asserted by step 1.9 (1255).
- A4 and protected markers: verified by Grep in this pass (G-2, G-4).

## Verdict: FAIL

One blocking finding is open. NB-1 (IMPORTANT) is a recovery-introduced inconsistency between steps 1.2/1.5 and steps 1.3/1.9: the recovered classifier rules (i)-(iii) and their tests need data-model fields and print locations that the plan does not define. All 18 blocking omissions are RECOVERED; 0 are JUSTIFIED and 0 are OPEN. WC-10, the A4 rejection, the later-phase boundary and the protected markers all hold. M-1 to M-6 are notes and do not fail the review. The report was not edited (fix authorization: false).

