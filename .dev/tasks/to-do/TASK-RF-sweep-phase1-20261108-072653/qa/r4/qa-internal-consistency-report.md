# QA Report: R4 internal-consistency lens (domain lens, research/09 Gap 5)

**Target:** `docs/designs/orchestrator-mode.md` (1041 lines at review time; the 1013 in the sizing note is the build-time figure), as edited by items 5.1 to 5.11.
**Date:** 2026-11-09
**Phase:** fix-cycle 0 / first review of the R4 gate, `fix_authorization: false`
**Method:** full read of the DESIGN in 150-line chunks (1-1041), research/07, research/08, r4-mechanical, r4-wc14-hits, r4-reanchor; targeted grep and `sed -n` against the live `WORKER-CONTRACT.md`, `test_worker_contract.py`, `main.py` and the SPEC (read only; no orca, no network, no file written except this report).
**Convention for the Checks table:** FAIL only when a BLOCKING or MAJOR finding attaches to the check. A check with only MINOR notes is PASS (notes listed under Findings).

## Findings

### F1. MAJOR. Rollback row lists four of the five pins; section 8 has five

- Side A, `docs/designs/orchestrator-mode.md:682`: "**Pins** (five edits)", bullets at :684 (WC-16 `RULE_PHRASES` entry), :685 (`NEVER_AS_WORKER`), :686 (test rename), :687 (`"sweep" not in UNATTENDED_COMMANDS`), :688 (change the `RULE_PHRASES["never-as-worker"]` phrase at line 89).
- Side B, `docs/designs/orchestrator-mode.md:970`: "WC-16 with the D6 sentence, the line 23 never-as-worker entry, the `RULE_PHRASES` entry, the `NEVER_AS_WORKER` entry, the `UNATTENDED_COMMANDS` assertion (design) and the test rename | Revert". The phrase edit of :688 is not in the list. Section 18 R4 (:1041) says "added the fifth pin", so the fifth pin was added to section 8 and not carried to section 16.
- Why it matters: `tests/skills/test_worker_contract.py:86-92` holds the pinned phrase, and `_check_rule` (:755-762) asserts every phrase is in the contract text (`test_contract_states_rule`, :907-909). If the rollback reverts WC-16, line 23 and "the `RULE_PHRASES` entry" (the WC-16 key) but leaves the :89 phrase carrying `/sc:sweep`, `test_contract_states_rule[never-as-worker]` fails on the reverted tree, and the rollback check at :978 runs that very file. Mitigation exists (:963 says rollback is one revert of the branch's commits as one unit), so this is not a data-loss risk, but the row-by-row table is a false statement of what must be reverted.
- Smallest fix: in :970 add "the `RULE_PHRASES["never-as-worker"]` phrase edit" to the list (for example "... the `RULE_PHRASES` entry and the never-as-worker phrase edit, ...").

### F2. MINOR. "whatever #422 does" is stale wording next to "PR #422 is merged"

- `docs/designs/orchestrator-mode.md:668`: "PR #422 is merged on master (merge commit `2327fbd3`), so the step waits for nothing ... WC-16 and its pins stay deliverables of this PR whatever #422 does (SPEC line 420)". Same phrase at :1006 (open item 21). A merged PR does nothing further, so the clause reads as if the outcome were still open. This is the SPEC's wording (SPEC :420 "even if #422 stalls") carried over after the facts changed.
- Related: `:982` says "Each item is unverified or undecided today", but item 21 (:1006, "PR #422 overlap with WC-16 ...") is neither: :668 and research/07 :162 settle that #422 is merged. It is a to-do record gated by step 1.16a, not an open question.
- No step actually waits on #422: :942 (1.16a "none; the record gates 1.17"), :943 (1.17 gated on 1.0b and 1.16a), :915 ("record-only PR #422 check") all agree. So the "still gates on PR #422" failure mode is NOT present; only the wording.
- Smallest fix: drop "whatever #422 does" at :668 and :1006 (say "WC-16 and its pins are deliverables of this PR"), and retitle item 21 "Record of the PR #422 state (step 1.16a)".

### F3. MINOR. Section 18 R4 row says draft names were marked in sections 13 and 14; section 14 has none

- `docs/designs/orchestrator-mode.md:1041`: "marked the SPEC and REPORT draft names in 13 and 14". Lines 854-880 (section 14) contain no `WC-` text (grep count 0); the two marks are the section 13 rows D6 (:829) and 1.17 (:852). r4-mechanical Check 2 (WC-16 in sections 1, 8, 9, 10, 12, 13, 15, 16, 17) also has no 14.
- Smallest fix: replace "13 and 14" with "13".

### F4. MINOR. "keeps a periodic sweep scheduled" carries no cadence bound

- `docs/designs/orchestrator-mode.md:677`: the bound "at most once every 5 minutes" is attached to the wake sentence; the next sentence, "It keeps a periodic sweep scheduled while work remains.", has none. Contract `WORKER-CONTRACT.md:110` bounds every sweep ("After every wake or timeout, at most once every 5 minutes"). A reader can schedule a 1-minute periodic sweep without contradicting the letter of WC-16. No text in the DESIGN says sweeps may run more often (grep of "wake", "minute", "periodic", "cron", "interval" over the whole file: only :672, :677, :684, :712, :829, :1041, all consistent with 5 minutes).
- Related: WC-16 says "On every coordinator wake" while :110 says "every wake or timeout"; WC-16 does not say whether `/sc:sweep` and the :110 sweep share one 5-minute budget (research/07 :134 asked WC-16 to state how the two relate; the text only says "the cadence of").
- Smallest fix: ", no more often than every 5 minutes" after "periodic sweep scheduled" (pins at :684 are unaffected).

### F5. MINOR. Section 1 status describes R3-B1 to R3-B3 as open defects that sections 7.2, 11 and 18 say are fixed

- `docs/designs/orchestrator-mode.md:9-11` (data model "lacks" the time fields; no rule decides between two Dispatch rows; three fixtures "were dropped") against :457 and :459 (the fields exist), :498 (the several-rows rule), :756 (fixtures restored) and :1038-1040 (Fix cycle 3 records the changes). Line 7 still says they "are carried as the first required design-fix tasks". The review gates are pending, so "NOT a clean pass" is still honest; the tense is stale.
- Smallest fix: one sentence in section 1: "Fix cycle 3 (section 18) applied these three; their review gates are pending."

### F6. MINOR. Deviation D6 provenance and the section 13 definition do not cover the R4 changes

- `docs/designs/orchestrator-mode.md:820` says each deviation "comes from the PANEL, FIXREVIEW or the design review"; D6 (:829) Source column says only "SP-27", but the renumbering and the cadence swap come from the re-anchor to master (research/07 §4(a), §4(c)). Also, step 1.16a being record-only departs from SPEC :420/:582 ("verify current overlap ... If #422 merges first, rebase") and is in neither section 13 nor "Not counted as deviations" (:836-840). `Total: 9 deviations.` (:834) stays correct if it goes under "Not counted".
- Smallest fix: D6 Source "SP-27; re-anchor to master 5dc29d23"; add a "Not counted" bullet that 1.16a is record-only because #422 is merged.

### F7. MINOR. Naming collision "R4"; R2 line numbers are pre-R1

- `:672` and `:1041` use "R4" for the fix-cycle row; `:714` uses "R4" for routing row R4 (`_OTHER_COMMANDS`). Fix: write "fix-cycle row R4" at :672.
- `:712` anchors R2 to "line 396" and "line 403"; R1 (:711) inserts a row at HOW-WE-WORK.md:334 in the same step 1.21, so after R1 they are 397 and 404 (research/08 :111). Fix: add "(397 and 404 once R1 is in)".

### F8. MINOR. Step 1.18 breaks a pinned test until step 1.19

- `:944` (1.18 edits contract line 23) and `:945` (1.19 edits the :89 phrase and `NEVER_AS_WORKER`) are separate steps; between them `test_contract_states_rule[never-as-worker]` fails (line 23 no longer matches the :90 phrase). The 1.19 row gate is "1.18", so the order is fixed and the red state is unavoidable unless both land in one commit. Fix: say in :945 or :703 that 1.18 and 1.19 land in one commit (as R1 to R3 do at :722).

### F9. MINOR. R2 and R8 gates omit the WC-16 step

- `:947` (1.21, R2 names WC-16) and `:952` (1.24b, R8 names WC-16) are gated on 1.14 and 1.16, not on 1.17. Numeric order makes it work. Fix: add 1.17 to those two gate cells.

## Confirmed clean (no finding)

- No coordinator-loop WC-14 remains: `grep -n 'WC-14'` gives :668 (master worker rule, true: `WORKER-CONTRACT.md:63` "WC-14. No turn ends between chain steps"), :829 and :852 (both "WC-14 (WC-16 in this design)", historical names of the SPEC and REPORT drafts) and :1041 (master has WC-14 and WC-15, true: `WORKER-CONTRACT.md:63-64`).
- No "561" besides SPEC line 561 at :65 (a SPEC citation, valid). `main.py` text at :28, :932, :968 says 519-565, 563/565, 568 and "after line 565"; live `main.py:559-568` agrees.
- Cadence: WC-16 (:677), R2 (:712), D6 (:829) and R4 (:1041) all say "at most once every 5 minutes"; `WORKER-CONTRACT.md:110` says the same; the dropped "It sweeps on every wake" appears only as a quotation in :672 and :829.
- Pin 1 (:684) key, ident and four phrases are present verbatim in the :675-677 block ("WC-16. Coordinator loop" on the heading line, "On every coordinator wake", "it is never posted", "It never stops watching on its own"); pin 5 (:688) replacement string matches line 23 at :701 including the trailing ", "; anchors `test_worker_contract.py` 25, 89, 156, 165-172, 173, 382-391, 755-762, 765, 837, 912, 1081-1082, 1318, 1322, 1556 and `WORKER-CONTRACT.md` 23, 110, 151, 273, 275 re-read on disk and match.
- Counts: 5 pin bullets; 9 deviations (D1-D9); 23 open items; 8 ALLOWED_ORCA templates and 7 verbs; 4 points in step 1.16a; 3 existing test files edited.

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | No coordinator-loop use of WC-14 remains (4 hits, all worker rule or historical name) | PASS |
| C2 | WC-16 heading, text, pins, R2, R8, FR-023, `.gitignore` comment, steps and open items use one name | PASS |
| C3 | No "561" or "519-561" left except the SPEC line 561 citation at :65 | PASS |
| C4 | `main.py` anchors (565, 568, "after line 565") agree across :28, :932, :968 and live file | PASS |
| C5 | No step or open item waits on PR #422 (1.16a record-only; 1.17 gate; :668; :915; :942; :943; :1006) | PASS (F2 wording) |
| C6 | No text lets the coordinator sweep more often than once every 5 minutes | PASS (F4 note) |
| C7 | R2 text agrees with WC-16 and contract line 110 | PASS |
| C8 | R8 changelog row agrees with section 8 (WC-16 named, topic-heading style) | PASS |
| C9 | Five pins: five bullets in section 8, phrases verbatim in the WC-16 block, anchors match live files | PASS |
| C10 | Five pins agree with section 16 rollback row | FAIL (F1) |
| C11 | Pins agree with steps 1.17 to 1.19, section 11 row :761 and FR-023 row :794 | PASS (F8 note) |
| C12 | Step gates (1.0b, 1.16a, 1.17 to 1.19, 1.21 to 1.24b) agree with section 8 gate paragraph | PASS (F9 note) |
| C13 | Never-as-worker line 23 text (:701) agrees with pin 2 and pin 5 | PASS |
| C14 | D6 text, "Total: 9 deviations" and section 8 "three changes" agree | PASS (F6 note) |
| C15 | Section 18 R4 row claims match the file | PASS (F3 note) |
| C16 | Section 1 status agrees with sections 7.2, 11, 18 | PASS (F5 note) |
| C17 | Totals and counts (23 open items, 8 templates, 7 verbs, 4 points, 3 test files) | PASS |
| C18 | Re-read of cited live anchors (contract 23, 63, 64, 110, 151, 273, 275; test file 25 to 1556; main.py 559 to 568) | PASS |
| C19 | Names used once each (R4 routing row vs fix-cycle row R4; R2 line numbers after R1) | PASS (F7 note) |

Confidence: Verified 19/19 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%
Tool engagement: Read: 12 | Grep: 9 | Glob: 0 | Bash: 4

Findings: 1 MAJOR (F1), 8 MINOR (F2 to F9).

## Self-audit

Tool calls that back the report: 12 Read chunks of the DESIGN and research files, 9 Grep calls, 4 read-only Bash calls (`sed -n`, `grep`, `awk`, `wc`). Nothing was edited except this file.

Verdict: FAIL
Blocking count: 1
