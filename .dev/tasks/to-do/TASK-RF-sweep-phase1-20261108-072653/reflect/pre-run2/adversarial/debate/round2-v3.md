# Round 2 rebuttal: Variant 3 advocate

- Protocol: sc-adversarial-protocol, Round 2 (sequential rebuttals; V3 goes last, after V1 and V2).
- Advocate for: Variant 3 (reviewer 3, refactorer lens, opus).
- Focus: answer every criticism of V3 raised in round1-v1, round1-v2, round2-v1 and round2-v2; update the view of V1 and V2; add new evidence; restate a position on every S-, C-, X- and A- id.
- Id meanings: as defined in `diff-analysis.md`. V1's Round 2 table reuses some ids with other meanings (for example C-001 as coverage, S-002 as classification, C-023 as D6 closure). This file does not follow that remapping; every id below means what `diff-analysis.md` says it means.
- Inputs read: `debate/round1-v1.md`, `debate/round1-v2.md`, `debate/round1-v3.md`, `debate/round2-v1.md`, `debate/round2-v2.md`, `diff-analysis.md`, `variant-3-original.md`.
- Evidence re-read for this round (path keys: T = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; D = `docs/designs/orchestrator-mode.md`; C = `src/superclaude/cli/reflect/config.py`):
  - T 148, 163, 989 (item 6.2 title "Log the OQ-1 decision (L3, no HALT)"), 998, 999, 1000, 1005, 1007, 1142, 1259, 1260, 1262, 1267, 1436, 1448, 1468, 1482, 1485, 1524, 1525, 1588, 1793, 1796, 2256, 2469, 2471.
  - D 181, 196, 221, 552, 873, 971, 973.
  - C 64 to 78 (`_git`).

## Response to criticisms

### 1. "21 of 32 rows rest on an inherited T1 matrix mapping, not an independent audit" (V1 R1, V2 R1)

Conceded. Those 21 rows are tagged [INFERRED] in V3 and were not re-read. They should carry less weight in the merge than V1's and V2's re-read rows, and the merge should not count them as independently confirmed (A-006b). V3's value is in its 11 findings, not in its row coverage.

### 2. "V3 missed R2-G1, the only confirmed HIGH" (V1 R2, V2 R1)

Conceded. T 1436 asks for `grep -c` per name on DESIGN 7.2 names in `models.py`, and a correct file that uses a class name both in its definition and in a type hint fails that check. V3 did not find it. C-012 belongs to V2.

### 3. "R3-G5 (C-020) contradicts the best-practice line 'No unauthorized scope creep' (X-006), and its second remedy conflicts with T 1259" (V1 R1)

Partly conceded.

- Second remedy withdrawn. Adding the two `--agent-wait` forms to the step 1.0a capture (item 7.16) would contradict T 1259, which says `worktree ps --agent-wait` "is allowed by R5 but is not run in step 1.0a". The first remedy stands alone: reword D 221 so a template may be added "only after a capture or a recorded owner decision".
- The finding itself holds. D 221 still reads "a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)". The 6.3 Action (T 998) lists eight edits and none of them touches D 221. Step (5) only rewords sentences found by `grep -n 'agent-wait'`, and D 221 has no `agent-wait` text, so step (5) cannot reach it. Step (8) only rewords hits of `grep -n 'eight\|8 templates'`, and D 221 has no such text either. After Phase 6 the design will add two uncaptured templates while stating a capture-first rule. That is not scope creep (R5 authorizes the templates); it is an authorized expansion whose record is incomplete. The best-practice line and R3-G5 are about different things and do not contradict each other.
- Severity: I accept the calibrator's "MEDIUM arguable". While Phase 1 never calls templates 9 and 10 (T 998 comment, T 1259), no wrong run can follow. I hold MEDIUM only as a record-integrity point (the design contradicts itself after the task); if the merge rates by runtime effect, LOW is defensible and I would not dispute it.

### 4. "The D10 half of R3-G6 (C-021) is overstated" (V2 R1, calibrator)

Conceded for the D10 half. The D10 row and the Fix cycle 3 R5 row quote the old rule as history, and a reader applying T 1005 ("no `agent-wait` hit forbids it") will see they record a change, not a live ban.

The 15.1 half holds and is sharper on re-read. T 1005 passes only if "the hits in 7.3 (the two `ALLOWED_ORCA` templates), 11, 13 (D10) and 15.1 allow it". The only 15.1 `agent-wait` hit today is D 873 ("no `--agent-wait`"). Step (4) at T 998 says "remove `--agent-wait` from the step 1.0a forbidden list and say the allowlist has ten templates; step 1.0a still runs only templates 1 to 8". Done literally, step (4) deletes the only 15.1 hit and writes no new one. Then 6.4 asks for a 15.1 hit that allows the flag and finds none.

V1 in Round 2 read this as "cannot pass" and "no hit to find". That is too strong in the other direction: step (4) neither requires nor forbids an allowing sentence, so an executor may write one. The calibrator's word "ambiguous" is right. The fix is one clause in step (4): write "`worktree ps --agent-wait` is allowed by R5 but is not run in step 1.0a" (the T 1259 wording) into 15.1. On a FAIL, T 1007 sends the executor back to 6.3, so the failure is caught, but only after a wasted loop.

### 5. "R3-G8 (C-022) remedy conflicts with item 5.4" (V1 R1, V2 R1)

Conceded. 5.4 already cites SPEC 415 and 583 and forbids other edits, so the remedy would contradict it. C-022 closes with no superior variant.

### 6. "R3-G3 (C-010), line 163 is wrong" (V1 R2 withdrew R1-G8; V2)

Conceded. T 163 is accurate when "Phase 1" means Phase 1 code, and T 1257 and 1259 make the step 1.0a capture separate. C-010 closes.

### 7. "R3-G7 duplicates R3-G1"

Conceded. R3-G7 merges into R3-G1 under C-017.

### 8. "8 of 11 findings are LOW; no blast radius; no HIGH does not prove quality" (V1 R1, V2 R1)

Partly conceded. V3 gave no blast-radius analysis (for example on INV-005 and the SPEC terminal wait-state reads). V3 also does not claim its LOW-heavy profile proves anything. But a LOW finding that is true and actionable is still worth carrying: C-018, C-019 and C-024 are each a single cheap edit with a verified anchor, and V1 and V2 did not raise them.

### 9. "No finding on 1.0a routing, HALT pointers or ten-template pins; no FR, NFR or step rows" (V1 R1)

Conceded as a coverage fact. V3's slice was the 32 remaining rows (A-006), and the step 1.0a mechanics fall in V1's slice. V3 defers to V1 on C-001, C-002, C-003, C-007, C-008 and X-001, X-002, X-005.

### 10. "R3-G11 (C-025) is wording only"

Conceded. OQ-16's "no fixture covers templates 9 and 10" is wrong only in that 10.3 has a positive unit case (T 1793 "positive agent-wait case"). It is a one-line wording fix, LOW.

## Updated assessment of V1 and V2

### V1

- Strongest on the step 1.0a and capture mechanics: C-001 (the cursor branch), C-002 (no route for a `run-current --json` need), C-007 and C-008 (literal checks that the Action does not satisfy). V2 has now conceded C-002, X-001 and X-005 to V1, and I agree.
- C-003 holds, with lower impact than V1 implies. T 1142 says every decision-record item "follows the item 6.2 procedure", and item 6.2 is titled "Log the OQ-1 decision (L3, no HALT)" (T 989), so the pointer is wrong. But T 1142 then spells out both Branches itself, so an executor has the HALT text in front of it.
- V1's Round 2 concessions are sound: citation failures, R1-G7, R1-G3 (the strip rule exists at T 1260 and 1262), R1-G8 and R1-G9 down to LOW. Its union check (152 of 152 rows, disjoint) settles A-006a, and I accept it with attribution to V1.
- Two V1 Round 2 claims go too far. (a) On C-021, "no hit to find" treats step (4) as forbidding an allowing sentence; it does not (see criticism 4). (b) On A-001d, "silent omission" is not guaranteed: T 1485 has no stop clause, but the 8.14 to 8.20 QA spawns read DESIGN and the facts and are told not to trust the task file's claims (T 1524, 1525), and T 1588 routes OPEN findings into a fix cycle. Equally, V2's reading that a safe stop is guaranteed goes too far, because those reviewers check against a DESIGN that itself pins ten templates.
- V1's Round 2 per-point table reuses ids with other meanings. The merge must not take its rows at face value; each one must be re-mapped to `diff-analysis.md` before it is counted.

### V2

- Still the strongest on the code-facing checks: C-012 (R2-G1, the one confirmed HIGH), C-013 to C-016 (design invariants not carried into the task) and C-005, C-006.
- Its Round 2 concessions (downgrades, CLOSED path to V1, C-004, C-010, C-011 and C-022 to none) are fair, and it credited V3 on R5 consistency (C-017, X-006).
- Its counter-evidence on A-001d (T 1524, 1525, 1588) is valid and moved my position: a QA net exists. It is not a full answer, because the net checks against a DESIGN that pins ten templates and has no cursor template (D 973), so a cursor finding would read as a design gap to escalate, not a code defect to fix. A named branch is still needed.
- V2's HIGH bar is applied unevenly (5 of 6 HIGH weakened), so V2's severity profile (S-002) is no better than V3's; they err in opposite directions.

## New evidence

1. **C-023 (R3-G9) weakens against V3.** T 1448 (8.5 Action) already states `capture_output=True`, `timeout=timeout`, `check=False`, and that a non-zero exit, timeout or oversize output raises `GitCallFailed`. C 64 to 78 shows the reflect `_git` runs `["git", "-C", str(cwd), *args]` with `check=True` and a fixed `timeout=10`. The main copy risk V3 named (an executor copying `check=True` from reflect) is blocked by T 1448's explicit text. T 148 and T 1468 (fakes "as `tests/cli/reflect/conftest.py` does") already point the executor at reflect. The residual is a citation gap only: add "C 64 to 78; only the seam shape is reused" to 8.5. LOW, and close to Refinement.
2. **S-009 advantage shrinks.** V3's codegraph use supported only the C-023 seam comparison, which item 1 above weakens. V3 should get no tooling credit beyond that.
3. **C-018 re-confirmed, both halves.** D 181 reads `ALLOWED_ORCA (8)` and D 196 reads `8 read templates`. Neither matches step (8)'s `grep -n 'eight\|8 templates'` (T 998) or the 6.3 and 6.4 checks (T 1000, T 1005), so both survive Phase 6 with a stale count. T 1793 gives zero-argv cases only for `worktree list` and `worktree current`; templates 9 and 10 get an exact-set pin and a positive case but no zero-argv case.
4. **C-020 re-confirmed.** D 221 has no `agent-wait`, `eight` or `8 templates` text, so none of the 6.3 grep-driven steps reach it, and T 998 does not list it.
5. **C-021 sharpened.** T 1005 requires that "the hits in ... 15.1 allow it"; T 998 step (4) only removes. See criticism 4 for the one-clause fix.
6. **A-004b settles.** T 2256 says "The level table is not touched", and the task's primitive edits (`sweep.md`, `sc-sweep-protocol/`, `WORKER-CONTRACT.md`, both `HOW-WE-WORK.md` copies) are exactly the scoped list at T 2469. No primitive outside that list is edited, so the concealment case behind X-003 cannot happen in this task. T 2471 also recounts at the recorded base. This supports C-011 and X-003 closing with no superior variant.
7. **A-001d middle position.** T 1485 (count is 10) and T 1796 have no stop clause; T 1524, 1525 and 1588 give a QA path. Neither "silent omission" (V1) nor "safe stop" (V2) is guaranteed. The design itself (D 973, open item 5: "no cursor template") makes a cursor field look like a design question, and D 971 (open item 3) shows the plan already routes a similar `--json` need to the owner. A named branch in 7.17 that routes a cursor field to the owner the same way is the clean fix, as V1 proposed.

## Updated per-point positions

| id | superior variant or none | changed from Round 1? (yes/no) | reason |
|---|---|---|---|
| S-001 | none | no | Slices differ by design (A-006); none is better, and V1's union check shows they fit together. |
| S-002 | none | yes | V3's 0 HIGH missed the one confirmed HIGH (C-012); V2's 6 HIGH lost 5 to calibration. Opposite errors. |
| S-003 | V2 | no | V2 gives ref and quote pairs on every finding; V1 has four empty evidence lists. |
| S-004 | V2 | no | V2 rows are grounded with no failed citations; V1 has 41 failed second refs; V3 has 21 inferred rows. |
| S-005 | V2 | no | V2 has the highest calibrated score and 0 failed citations. |
| S-006 | V2 | no | Only V2 gives `calibrated_severity` per finding. |
| S-007 | V3 | no | V1 and V2 both moved to V3 in Round 2; its classes are closest to a design-fix or traceability split. |
| S-008 | V3 | no | Low stakes; V3 states its scale in words, which avoids the "0-5" versus "5" mismatch of V1 and V2. |
| S-009 | none | yes | V3's codegraph use only supported C-023, which now weakens to a citation gap (New evidence 1, 2). |
| S-010 | none | yes | V3 related to as many T1 findings, but V2 also audited the matrix itself (C-006); no clear winner. |
| C-001 | V1 | no | Raised first at the right severity; T 1485 and 1793 pin ten templates with no cursor branch. |
| C-002 | V1 | no | V2 conceded the CLOSED path; no route for a `run-current --json` need in 7.17. |
| C-003 | V1 | no | T 1142 points at 6.2, titled "no HALT" (T 989); impact is low because T 1142 spells out both Branches. |
| C-004 | none | yes | Strip rule exists at T 1260 and 1262; V1 conceded. |
| C-005 | V2 | no | Both raised it LOW; V2 linked it to INF-017. |
| C-006 | V2 | no | Only V2 found the INF-017 pointer error. |
| C-007 | V1 | no | Only V1 raised the unanchored grep and the missing sentence. |
| C-008 | V1 | no | Only V1 found echo and ls against the Verification. |
| C-009 | none | no | Refuted (9.3 reads OQ-8 and has a HALT). |
| C-010 | none | no | T 163 is accurate; V1 and V3 both withdrew. |
| C-011 | none | yes | T 2471 recounts at the recorded base and no primitive outside the T 2469 list is edited (New evidence 6). |
| C-012 | V2 | no | Only confirmed HIGH; V3 missed it (conceded). |
| C-013 | V2 | no | Only V2 raised it; MEDIUM after calibration. |
| C-014 | V2 | no | Only V2 raised it; MEDIUM after calibration. |
| C-015 | V2 | no | Only V2 raised the unchecked invariants (D 211, 219, 638). |
| C-016 | V2 | no | Only V2 traced the set-union wording gap. |
| C-017 | V3 | no | V2 credited V3; R3-G7 merges here (conceded duplicate). |
| C-018 | V3 | no | Both halves re-verified: D 181 and 196 escape the step (8) grep; T 1793 has no zero-argv case for 9 and 10. |
| C-019 | V3 | no | Only V3 raised it; single verified anchor. |
| C-020 | V3 | no | D 221 untouched by T 998 and out of reach of every 6.3 grep; second remedy withdrawn; severity MEDIUM arguable, LOW acceptable. |
| C-021 | V3 | no | D10 half conceded; 15.1 half holds (T 1005 needs a 15.1 allowing hit, T 998 step (4) only removes); "ambiguous", not "cannot pass". |
| C-022 | none | yes | Superseded by 5.4, which already cites SPEC 415 and 583 and forbids other edits (conceded). |
| C-023 | V3 | no | Only V3 raised it, but it narrows to a LOW citation gap: T 1448 already states `check=False` and `GitCallFailed`. |
| C-024 | V3 | no | Only V3 raised it; single verified anchor. |
| C-025 | V3 | no | Only V3 raised it; wording-only LOW (conceded). |
| X-001 | V1 | no | V2 conceded the CLOSED path to V1. |
| X-002 | V1 | no | V1's MEDIUM matches the calibrator; V2's HIGH was cut. |
| X-003 | none | yes | Both overstated; T 2471 recounts at base and A-004b holds (New evidence 6). |
| X-004 | none | no | No variant states and applies a consistent HIGH bar (A-009). |
| X-005 | V1 | no | V2 conceded; V1's "plan weaker than T1 said" direction is right. |
| X-006 | V3 | no | Authorized expansion with an incomplete record: R5 authorizes 9 and 10, but D 221 is left contradicting them. Not scope creep. |
| A-001 | V1 | no | V1 named the unrouted cursor outcome and its fix (a 7.17 branch). |
| A-001a | none | no | ACCEPT: stated by D 552 and T 1267. |
| A-001b | none | no | ACCEPT: stated by T 1485 and 1793. |
| A-001c | none | no | ACCEPT: D 973 says "no cursor template", so a captured cursor field leaves the design with no template to call. |
| A-001d | none | no | QUALIFY held: no stop clause (T 1485, 1796), but a QA path exists (T 1524, 1525, 1588); neither silent omission nor safe stop is guaranteed. |
| A-002 | none | no | Parent of A-002a and A-002b; both variants tagged it [INFERRED]. |
| A-002a | none | no | QUALIFY: whether the executor counts as the coordinator is not settled by D 868 or the task. |
| A-002b | none | no | ACCEPT: T 163 states the "never by a test" half. |
| A-003 | none | no | C-010 closes; no variant was right to call T 163 wrong. |
| A-003a | none | no | REJECT the premise that T 163 is wrong: T 1257 and 1259 separate the capture from Phase 1 code. |
| A-004 | none | no | Parent of A-004a to A-004c; neither V1 nor V2 framed it correctly. |
| A-004a | none | no | REJECT: T 2471 recounts at the recorded base, so unrelated drift is handled. |
| A-004b | V1 | yes | QUALIFY to ACCEPT: T 2256 ("level table is not touched") and T 2469 show no primitive edit outside the scoped list; V1 found it. |
| A-004c | none | no | QUALIFY: whether D 939 covers the 168 pre-existing hits is a design reading the task does not settle. |
| A-005 | V3 | no | Only V3 tested the R5 authorization against D 221. |
| A-005a | none | no | ACCEPT: the OQ-1 record is RESOLVED with the owner's words. |
| A-005b | V3 | no | REJECT: an owner decision does not edit D 221; the design still says "only after a capture". |
| A-005c | V3 | no | QUALIFY: no parse evidence is needed while 9 and 10 are never called (T 998, 1259), but D 221 still asks for a capture first. |
| A-006 | V1 | yes | V1's union check (152 of 152, disjoint) settles full coverage. |
| A-006a | V1 | yes | QUALIFY to ACCEPT, with attribution to V1's union check. |
| A-006b | none | no | QUALIFY held: V3's 21 inferred rows are unverified and should carry less weight (conceded). |
| A-007 | none | no | Grades 4, 3, 4 rest on owner decisions being made before their gates. |
| A-007a | none | no | ACCEPT: PENDING decisions gate their dependents (T 1142 Branches). |
| A-007b | none | no | QUALIFY: live Orca access for 7.16 is assumed; without it 7.17, 8.10, 9.1 and 10.3 stall. |
| A-008 | none | no | Every card uses its own `gap_class` set. |
| A-008a | none | no | QUALIFY: no card states the four-category rubric, so classification scores are not comparable. |
| A-009 | none | no | Severity labels are not comparable across cards. |
| A-009a | none | no | REJECT the assumption that the cards share a severity bar; only V2 states one, and applies it unevenly. |
