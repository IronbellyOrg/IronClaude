# Plan Review: refactor-plan.md (Step 4 review)

Reviewer: independent analytical reviewer (did not write the plan). Read-only review; no git command run.
Inputs read: refactor-plan.md, base-selection.md, debate-transcript.md (metadata, per-point tracking, scoring matrix, convergence assessment, Round 1 statements), round2-advocate-A.md, round2-advocate-B.md, invariant-probe.md, round2.5-fault-finder-raw.md (lines 96, 138-139 by grep), variant-1-original.md (sections 0, 4.2, 5, 7, 8), variant-2-original.md (full).
Not read: diff-analysis.md and the round-1 files beyond their copies in the transcript (diff-analysis.md:48 only by grep).

## Verdict

FAIL as written. Safe to hand to the merge-executor: YES after fixes 1-5 below. Findings 6-12 are minor notes and do not block.

## Check 1: Fidelity (28 items checked; 27 correct)

Correct:
- Base selection: score 0.9167, margin 3.58%, tiebreaker level 1 with 9 points won against 3.
- Confidence values in Changes 1-11 and the "not made" table: C-001 88%; S-001 85%; S-003 85%; C-003, C-004, C-011 95%; A-002 82%; X-004 92%; X-001, X-002, X-003, X-007, A-006 95%; C-010 80%; C-002, C-006, C-008, A-004 70%; A-003 78%; S-005 92%; C-005 80%; A-001 72%; A-005 92%; C-012 90%; C-007 90%; X-005 90%.
- Convergence 83.3% (25 of 30); the five unresolved points; BLOCKED_BY_INVARIANTS.
- Quote "B-3 as stated is refuted" (round2-advocate-B.md Verification of N1).
- B:16 and B:28 quotes; `test_cli_install.py:502-506`; `panel.py:46, 214-216, 692` (692 traced to A:28 and diff-analysis.md:48).
- `rf-qa.md:484-534`; `task/SKILL.md:196-201`; `task/SKILL.md:192, 286`; `ledger.py:107`; `reflect-reviewer.md:56`; 93 markers in 8 skill files.
- Transcript figures: 278 after the 117 skip, 366 not reproduced, 571 non-fix.
- N1 corrections: restored byte for byte, 3 blocking replaced by 1 for about 5.6 minutes, damage count 2 or 3 unsettled, cause = line-reference dispatch plus agent misreading.
- N3: 437 / 28 / 15; standard-lens subset 107 (B) or 118 (A), pytest 2 or 1, `sed -i` 1.
- NB6 24 of 169; NB8 (no cap row in steps 3, 4, 8, 10); INV-006 (7 refused calls, not 2).
- Invariant counts: HIGH INV-002, 009, 012, 015, 016, 017; 9 MEDIUM; 1 LOW; INV-005 and INV-011 ADDRESSED.
- Variant A 4.2 endangered rows: "Availability of every MDTM task run" HIGH; "The pinned strings of task/SKILL.md" MEDIUM.

Finding 1 (BLOCKING, plan line 88, invented claim): "the plugin mirror holds none of the rf-qa, rf-qa-qualitative, reflect-reviewer or evidence-validator agents ([CODE-VERIFIED] by Glob in both variants)". The only source is variant-2-original.md:74: rf-* agents absent from `plugins/superclaude/agents/`, by `ls` of the first 20 entries, in Variant B only. Nothing in the debate covers reflect-reviewer or evidence-validator, no Glob is cited, and Variant A never states it (A:153 lists the plugin question as not verified).
Fix: "B's note that rf-* agents are absent from `plugins/superclaude/agents/` (`ls`, first 20 entries [CODE-VERIFIED], Variant B only, variant-2-original.md:74)".

## Check 2: Coverage

All 30 points are accounted for except X-006. S-002, S-004 and X-003 are carried by the base without being named, which is acceptable. Items 1-5 and 7-12 of the two Proposed resolutions are carried: item 1 in Change 1; item 2 in Change 3(b); item 3 in Change 3(c) and Change 6(4); item 4 in Change 6(3); item 5 in Change 6(2); item 7 in Change 7; item 8 in Change 11; item 9 in Change 6(5); items 10-12 in Change 10.

Finding 2 (BLOCKING, coverage): item 6 of both resolutions is missing. Item 6 puts owner question Q3 to the owner with the evidence of items 4-5 and recommends "yes" for the standard eight lenses. B's amendment adds that the only class-(b) event was at a task-file gate item of a non-standard lens, and that no standard-lens spawn through `/task` steps 3-4 was observed. The plan uses "owner answers Q3 yes" only as a condition (lines 18, 60).
Fix: add item 6 to Change 7 or Change 10, with B's sentence marked "B amendment, not answered by A".

Finding 3 (BLOCKING, coverage): X-006 (Variant A outcome, 95%) is neither implemented nor listed under "Changes NOT Being Made". Change 2 (line 25) instead keeps C-03 "condition 7" as a dependency statement, which B conceded does not bind the per-reviewer confidence design.
Fix: in Change 2 (or Change 4 corrections), state that the confidence is computed per reviewer from its own checklist rows (`rf-qa.md:505`), so C-03 condition 7 does not bind the new agent (X-006, A 95%, B conceded B-R1:68).

Finding 4 (BLOCKING, coverage): the A-004 text that both advocates agreed, "standard lenses get pre-computed counts in the brief where they used Bash", appears nowhere in the plan.
Fix: add it to Change 3(b) or Change 7, beside "INV-017 HIGH UNADDRESSED (pre-computed counts exist in the oracle but not at a production gate)".

## Check 3: Honesty of splits

PASS. The five split points carry both texts: C-002, C-006 and C-008 in Change 7; A-001 in Change 6 step 4; A-004 in Change 7(iv); all five again in the Change 10 table. The lens-identity blocker is marked "B amendment, not answered by A". The six HIGH invariants are not presented as resolved: Change 5 says "Do NOT resolve", and Change 7 names INV-002, INV-009, INV-012 and INV-015. Marking gaps are listed in note 6.

## Check 4: Internal consistency

Change numbers, the approval block and the risk table agree, except:

Finding 5 (BLOCKING, line 9 vs line 81): the source-of-truth list on line 9 omits `round2.5-fault-finder-raw.md`. Change 10 needs "the fault-finder's 'Not verified' line", which exists only at round2.5-fault-finder-raw.md:139. Under line 9's "MUST NOT add" rule, the executor would have to drop that line.
Fix: add `round2.5-fault-finder-raw.md` to the line-9 list.

## Check 5: Forbidden content

PASS. A grep of refactor-plan.md for the run-1 task id and the queued-run file name returned no match.

## Minor notes (non-blocking)

6. Some B amendments are not marked "not answered by A":
   - Change 6(2) lists "empty or unreadable corpus gives no verdict", "run-1 transcripts skipped", "counted per spawn source" and "with its cause" unmarked, while its bracket says per-spawn-source is marked. The transcript scored C-010 as agreed text, so this matters only under the plan's own line-9 rule.
   - Change 3(b): the bracket's scope is unclear. The codegraph tools and the verbatim S1-S3 copy are also part of B's item-2 amendment.
   - Change 10(i): the no-clobber check is labelled "[B text]"; it should read "B amendment, not answered by A".
   - Change 11 uses B's item-8 wording ("skill-embedded and task-file gate items") without A's ("domain and skill-embedded lens spawn sites").
7. Line 46: the INV-G text should add that INV-018 and INV-007 (MEDIUM, UNADDRESSED) leave the post-completion standard-lens spawns (`task/SKILL.md:307, 320`) and the extra lenses of the 10 and 12 tiers on rf-qa even if the switch lands.
8. Line 53, Change 6 step (3): add the two metrics both advocates named, per-lens recall in a blocking row and wrong blockers on clean twins.
9. Line 32: the "S1-S3 text copied verbatim" rule should cite INV-013 (MEDIUM). The pin's 10-file tuple does not reach a new file, and widening it conflicts with item 9's "no test edited".
10. Line 32(e): "three open wording splits" does not match the five unresolved points of Change 10. Say "five points (three disputes per the fault-finder)".
11. Line 86: Change 11's target, "Base Section 2 (end) or a short new Section", leaves the choice to the executor. Pick one.
12. Line 18, B-3 wording: "the existing /task standard-lens agents are made read-only" is inaccurate, because `rf-qa.md` stays unedited. Use "the standard lens dimensions at `/task` steps 3-4 switch to the new read-only agent".

Status: Complete
