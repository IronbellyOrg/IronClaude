### Variant 2 Advocate rebuttal

**Cycle-id owner (V3 advocate, plan line 124).** Partly conceded, after reading plan lines 33 and 124. Line 124 does assign a mint owner: the SKILL "mints the cycle id with `fix_cycle_id` in the single place named by Task 1 O1" at the end of Wave 3, and reuses it for the push triad and `rereview_requested`. Line 33 makes O1 a read of where SKILL.md and `refs/loop-guard.md` assign a cycle's `cycle_id` today, so the owner is delegated, not missing. V2 F1's phrase "no id is minted today" over-reads line 33, and its "no task edits the Wave 6 push call site" is weaker than I claimed in Round 1.

What survives: Task 8's acceptance (plan:127-128) only requires the ref to "state" the mint place, and Task 11 (plan:170-171) does not assert that the guard id, the push-triad id and the `rereview_requested` id are equal. `held_cycle_published` matches on that id (spec:108), so a mismatch means a normal push never releases the PR, and the plan's tests would still pass. That is a missing check, not a missing owner. I accept the downgrade of C-007 from High to a MAJOR-to-MINOR calibration question. I do not accept dropping it: V1's advocate, in Round 2, also keeps it as a real gap.

**F4 as padding (V1 advocate).** Conceded. The plan's Depends-on lines (Task 9 on 6 and 8, Task 10 on 9, Task 12 on 6 and 8, Task 13 on 2, 10, 11 and 12) all reach Task 1 transitively, and F4 says so itself. V3's same-file ordering finding (C-005) is the real hazard here, and X-001 stays with V3.

**F2 and F3.** F2 (FR-16 retry has no test body) was not contested. F3 (crash boundaries) is thin and I keep it MINOR.

**Other variants.** V1's own spot check of spec:241 against plan:140 shows the Wave 0 contradiction is a wording ambiguity, not an unpassable check. I agree with V1's downgrade, so C-002 is a MERGE of two MINOR items. V3 stays the best base for a merge: its whole-line pin (C-009) and the named resume-row inputs (C-001) are the strongest repo-grounded points.

**New evidence.** Plan line 33 shows O1 is a read of the existing cycle-id assignment, which is why the owner question is answered. Plan lines 134-137 and 148 show Tasks 9 and 10 reach Task 1 only through Task 8.

**Changed votes**
- C-004: old NONE, new V3. V2's F4 is padding; V3's version carries base-file evidence.
