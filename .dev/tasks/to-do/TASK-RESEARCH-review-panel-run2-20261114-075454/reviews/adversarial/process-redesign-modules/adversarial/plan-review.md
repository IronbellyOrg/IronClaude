# Plan review: refactor-plan.md (slot X-13, process-redesign-modules)

Verdict: 11 defects. All numbers and scores re-checked are faithful (472 of 510, 31 of 313 = 9.9 percent, 18.8 percent, 13 Hybrid points, 16 UNADDRESSED = 2 HIGH + 13 MEDIUM + 1 LOW, 96.55 percent). Spot-checked code cites hold. All VA section targets exist.

1. Change 4 silently settles INV-001. "The consensus text takes B's form" settles who computes `observed`. A's item 2 says "fills `assigned` only (Agreement)"; B's AMEND in 4.2 was never accepted by A; IP INV-001 lists the split as open. Fix: record both lists and say it is unsettled.
2. Change 15 drops D-1 and D-2. R2A section 6 and R2B section 7 both keep them open (row duty crowding out free review; script versus card items on C4/C8). Fix: add them with their settling evidence (G-2, G-1 and the arms).
3. Change 10 and the NOT-made table omit G-4's three prerequisites. R2A item 17 and R2B reserved item 11 both name them: per-row persistence (`ledger.py:99-104, 210-218`), a merge hook (`merge_cmd.py:71`), a v2 severity rewrite (`findings_v2.py:161-162`). Fix: add them.
4. Change 11 targets the wrong text. VA section 6 has no precheck-flag reference; those sit in VA section 2 (c), section 3.3 and the section 4 "Endangered" bullet. Also "keep VA's statements" retains VA lines 88-89 (items via `coverage_rows`/`probe`) and line 98 (replica assignment), which conflict with Changes 3 and 6 (row block, uniform binding). Fix: retarget and revise those lines.
5. Change 2 leaves a contradiction. VA section 2 "Does not add" (line 19) lists "a per-row verdict block", which the merge now adds; the plan says "extend", not revise. "First two bullets" should be bullets 2 and 3. Telemetry is not rewritten "per Changes 3 and 4"; it is item 5 of Change 2.
6. Change 3 states B's row limits as settled. The 12 to 200, 300 and cap values appear only in R2B component 2; A's R2 section 8 item 6 only asks for a rule; INV-010 is open. Fix: label them B's proposal.
7. Change 14 misattributes D2 to GQ-135. VA 3.6 says GQ-135 covers the related +35 percent elapsed limit; D2 is a pre-registration choice for the owner.
8. Change 8 loses caveats. R2B section 2 item d says the 18.8 percent assumes independence ("independence is low"); failures sit in 8 of 29 runs, so "2 to 57 percent by run" covers only those 8. Also VA 3.3 bullet 1 still calls `ledger.py:3-4` the "code's own rule" and tags 472/510 "not re-run"; Change 5 only appends a note in 3.7; 3.3 is two bullets, so "last paragraph" means bullet 2.
9. Change 10 silently drops VA M2, M4 and M5. That removes found-at-any versus found-at-blocking reporting (base-selection strength 4) and the wrong-blocker limit (Z0+1.0) from B's M-B2. Neither R2 list drops them. Fix: place them under G-3 or say they are dropped.
10. S-004 stays unresolved, but Changes 9 and 11 adopt VB's list and table format (Change 11 cites "VB section 2 table"). Fix: state which format is kept, or leave it open.
11. Change 11's "does not arise" is the plan's own inference, not in the R2 files. Fix: tag it as inference.

Status: Complete
