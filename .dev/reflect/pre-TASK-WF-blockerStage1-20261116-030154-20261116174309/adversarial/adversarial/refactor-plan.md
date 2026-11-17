# Refactoring Plan

## Overview
- Base: Variant 3 (`variant-3-original.md`, reviewer 3 refactorer/opus), combined score 0.9608
- Incorporated: Variant 1 (R1-F4, separator, load-by-path, F5 label), Variant 2 (R2-F2, R2-F3 as non-blocking), debate outputs (A-002, INV-001, INV-004, INV-006, INV-010, INV-013), final fix lines of A3 Round 2
- Output file: `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/adversarial/merged-review-card.md`
- Merged-card constraints: the merged card is the evidence-bearing review card of this run; every `path:line` it cites must have been read (plan `PLAN:n`, spec `SPEC:n`, code); findings are renumbered `M-F1..` in the order below with a mapping line to the source ids; the verdict is NEEDS-REVISION with ONE blocking finding; plain Markdown, no table pipes inside cells.
- Total planned changes: 12; risk: Low (additive, plus two regrades)

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale | Risk |
|---|---|---|---|---|---|---|
| PC-01 | Keep R3-F1 as M-F1 BLOCKING; replace the fix with `grep -rln --include='*.py' "follow_ups" src/superclaude/cli/review` worded "lists no file other than `follow_ups.py`" in BOTH sentences of PLAN:125; add the qualification "fails under default Python settings (bytecode on)" and the live grep evidence (`grep -rln "ledger"` lists 10 `.pyc`) | V3 R3-F1, debate A-002, INV-001, A1/A3 live greps | Findings | replace fix text | C-001 unanimous BLOCKING 95 percent | Low |
| PC-02 | M-F2 NON-BLOCKING: scale-map grammar (family key, conditional token returned UNSET by `ReviewerJudge`, multi-path cell separator " + ", T4 checks each file exists and each label present in at least one) | V3 R3-F2, V1 R1-F2 separator, A3 Round 2 | Findings | merge | C-002 | Low |
| PC-03 | M-F3 NON-BLOCKING: REQ-09 owned by no task (grep of all four stage plans rc=1) | V3 R3-F3 | Findings | keep | C-003 | Low |
| PC-04 | M-F4 NON-BLOCKING: M precheck (SPEC:512) and D decision-basis input (SPEC:516, 522, 615 item 3) missing in Task 10 while PLAN:164 pins "S, W and D always"; record as a close call (A1 odds 45 percent BLOCKING), fix: `questions_to_ask` returns M only with the list plus a code-confirmed absence by name, D only with decision-basis excerpts (else UNSET), add a basis count line to Task 12 | V2 R2-F2, R2-F3, A1/A2/A3 Round 2 | Findings | insert | C-007, C-008 regraded NON-BLOCKING | Low |
| PC-05 | M-F5 NON-BLOCKING: `classifier` column written for rows the follow-ups ledger does not hold; add an update call to Task 7 or write only to existing rows | V1 R1-F4 | Findings | insert | C-009 | Low |
| PC-06 | M-F6 NON-BLOCKING: Task 8 resolver; fix: injected resolver, default loads `read_origin()` from `origin_repo.py` by file path | V3 R3-F5 replaced by V1 R1-F5 fix | Findings | replace fix | C-004, conceded by A3 | Low |
| PC-07 | M-F7 NON-BLOCKING: Task 4 copy of `.dev/pr-monitor/` (SPEC:485) versus Task 5 grep, merged with the missing `src/superclaude` check for Tasks 4 and 5 (SPEC:404, 447 versus PLAN:28) | V3 R3-F4, INV-004 | Findings | merge | C-005, INV-004 | Low |
| PC-08 | M-F8 NON-BLOCKING: Task 1 gate order (move the owner-go and stage-0-summary checks into the first sentence of the body) | V3 R3-F6 sub-item | Findings | keep | C-010 | Low |
| PC-09 | M-F9 NON-BLOCKING: cosmetic and count items: `verify` to `verify-citations` (PLAN:184), stray ", ;" and the "pointer order only" no-op for installed-only rows (PLAN:223), the self-cancelling phrase at PLAN:52, tasklist line count 9 not 7 (INV-006) | V3 R3-F6, V2 R2-F5, INV-006 | Findings | merge | C-006, C-012 | Low |
| PC-10 | M-F10 NON-BLOCKING (follow-up candidates): importer list has no end point beyond stage 1 (INV-010); `THRESHOLDS` constant versus lint check 11 (INV-013); `make lint` acceptance only in Task 7 | invariant probe | Findings | insert | INV-010, INV-013 | Low |
| PC-11 | First-review table: use V3's lines but mark F5 "fixed in text, residual gap M-F2" and F1 "fixed in text; the grep fails (M-F1)" | V3, V1 label | First-review findings | modify | X-002 | Low |
| PC-12 | Add a "Debate outcome" section: convergence 100 percent (21 unanimous, 1 majority), the two regrades, the close call, the dropped items (C-011 review matrix, X-003, X-004 are not plan defects); keep V3's "Checked and found sound" and "Not checked" | debate-transcript.md | new section | insert | transparency | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| C-001 grade | V2's evidence wording ("independently confirmed", no path) | V3/V1 cite the pycache listing and the live greps |
| C-002 fix | V1's "MAJOR=Blocking" | collapses the conditional of SPEC:739 (A1 conceded) |
| C-004 fix | V3's subprocess call | load by path is more consistent (A3 conceded) |
| C-007, C-008 grade | V2's BLOCKING | withdrawn by A2; no failing stage 1 exit test or wrong gate outcome shown |
| C-011 | V2's R2-F4 | concerns the review's own coverage matrix, not the plan |
| X-003, X-004 | card-wording remarks | not plan findings |

## Risk Summary
Overall Low: the merge adds text to one card; the only grade-sensitive changes are PC-01 (kept BLOCKING) and PC-04 (NON-BLOCKING, recorded as a close call). Rollback: the three original cards are preserved unmodified in `reviewer-cards/` and `variant-N-original.md`.

## Review Status
Auto-approved (non-interactive); no separate analytical-agent review of the plan (orchestrator-drafted; deviation noted in the merge log).
