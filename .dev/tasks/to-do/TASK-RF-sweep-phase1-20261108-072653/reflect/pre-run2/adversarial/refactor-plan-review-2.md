# Refactor Plan Review 2 (Step 4, after fix cycle 1)

- Plan under review: `refactor-plan.md` (405 lines, 30 changes, 28 findings), including its "Fix cycle 1" section (lines 397 to 405)
- Prior review: `refactor-plan-review.md` (VERDICT: FAIL; B-01 blocking, M-01 to M-07 minor)
- Fix log: `refactor-plan-fix-log-1.md`
- Reviewer: fresh analytical reviewer, report-only. Only this report was written.
- Date: 2026-11-08
- Evidence read: the whole plan; the prior review and fix log; TL 190-198, 279-283, 989-993, 998, 1005, 1138-1147, 1252-1279, 1478-1490, 1636-1646, 2795-2806 and the item headers of 3.3 and 5.6 to 5.11; DESIGN 966-993; `invariant-probe.md` rows INV-001, 002, 005, 016, 017, 021 and line 42. The F-02 pattern was re-run against the TL (prints 0).
- Grading: blocking means the plan would hand the merge executor a wrong or unusable recommendation for a finding the caller ruled must be fixed, or a wrong number. Minor means a precision or completeness fix that changes no severity, count or verdict.

## Findings

No blocking finding. Six minor findings.

### N-01 (minor): the new 7.17 branch names no `blocker_reason`, its own PENDING row doubles the HALT rule's row, and the recommendation line drops the TL 1142 ending

- Where: Change 3, step 1 (plan line 52) and the success test (plan line 55).
- What is wrong: (a) TL 1142 Branch 1 "applies the HALT rule with the `blocker_reason` the item names". Step 1 names none, so the executor has to invent the halt line. (b) The HALT rule (TL 194) already "append[s] the halt line to `### Execution Log`". Step 1 also appends its own PENDING row first, so a firing branch leaves two 7.17 rows. Whether the success test's "exactly one PENDING row for item 7.17" holds then depends on the unnamed halt wording: a halt line that says "PENDING" makes the count 2. (c) TL 1142 requires the recommendation line to end "This recommendation does NOT authorize adoption." Step 1 says only "the recommendation line", while calling the file "the TL 1142 form".
- Why minor: none of this touches what Branch 2 reads (`status:` and the four decision lines), so the B-01 path still closes (see check 1).
- Fix: name the halt line, for example `blocker_reason: "Step 1.0a: <outcome> needs an owner allowlist decision; see phase-outputs/plans/OQ-<n>-<topic>-decision.md (PENDING)"`. Drop the separate PENDING row and let the HALT rule's row be the one PENDING row, or have the success test count only the step 1 row. Add the TL 1142 ending to the recommendation line.

### N-02 (minor): the refusal record is written for the cursor outcome only

- Where: Change 3, step 3 (plan line 54).
- What is wrong: step 3 says a refusal "records the refusal in `1.0a-facts.md` as 'cursor field present, no cursor template; ...'". The branch covers two outcomes. If only outcome (b) fires (open item 3 CLOSED, `run-current` needs `--json`), that line would record a cursor field that may not exist, and nothing would record that the `--json` change was refused. DESIGN 971 gives the behaviour for that case: "FR-002 fourth test and FR-026 case 4 stay gated".
- Fix: make the line per outcome. For (a), keep the current line. For (b), record "`run-current` needs `--json`; owner declined; the DESIGN 971 behaviour applies: FR-002 fourth test and FR-026 case 4 stay gated".

### N-03 (minor): the plan does not say what happens when both outcomes fire

- Where: Change 3, steps 1 and 3, and the success test (plan lines 52, 54, 55).
- What is wrong: one capture can produce both a cursor field and a `--json` need. Step 1 writes "a decision file" with "`<n>` the next unused OQ number", and the success test expects "exactly one PENDING row". It does not say whether that is one file with two questions (the owner may approve one and refuse the other) or two files.
- Fix: state "one decision file per outcome that fired, each with its own OQ number and PENDING row", and change "exactly one" to "one per decision file".

### N-04 (minor): M-04 was only partly applied, and the fix log does not say so

- Where: Change 2 note (plan line 45); fix log row M-04.
- What is wrong: the review's M-04 fix had three parts: plain `grep`, the ` | ` cell separator, and "keep the example row inline in the Action text", plus changing the 6.2 Output field ("The `### Execution Log` line.", TL 992) to "row". The note covers the first two only. Fragility (c) still stands: if the merged recommendation puts the example row on its own line, a correct append counts 2. The fix log says "One note added" and does not record dropping the other two parts. M-04 was minor, so nothing blocks.
- Fix: add "keep the example row inline in the Action text" to the line 45 note, and add the TL 992 "line" to "row" edit to Change 2 step 1. Or record in the fix log that these parts were deliberately not applied.

### N-05 (minor): the new INV-002 `not_carried` row names the wrong item

- Where: Changes NOT Being Made, row INV-002 (plan line 271).
- What is wrong: the row says "items 3.3 and 5.10 pin 9 before Phase 6". The Phase 5 pin is at TL 817 and TL 819, which belong to item 5.8 (header TL 815). Item 5.10 runs from TL 829 to TL 835 and has no `9 deviations` text. The error comes from `invariant-probe.md` line 15 ("5.10 (T 817-819)"). The conclusion still holds, because 5.8 also runs before Phase 6.
- Fix: change "5.10" to "5.8".

### N-06 (minor): Change 2 step 1 still gives the M-03 rationale the fix removed

- Where: Change 2, step 1 (plan line 40) against the Risk text (plan line 43).
- What is wrong: line 40 still says the 6.2 row is appended "as the TL 2804 rule requires for every owner decision". Line 43, rewritten for M-03, says TL 2802 already is the one row TL 2804 asks for. Read literally, line 40 says the opposite.
- Fix: change the line 40 clause to "in the four-column row form TL 2804 uses".

## Check results by point

1. B-01 closed: PASS.
   - Decision file: step 1 (line 52) writes `phase-outputs/plans/OQ-<n>-<topic>-decision.md` with `needs_human_decision: true`, `status: PENDING`, the question and options quoted, the steps it blocks, and the empty `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:` block. These are the fields TL 1142 lists and the ones Branch 1 and Branch 2 read. The path follows the TL 1146 pattern under the task folder. OQ-16 is the highest OQ number in the TL, so "next unused" is well defined (OQ-17). The OQ-8 names "Given by, Source" are gone; the only remaining hit is the fix-cycle note at line 400.
   - PENDING and HALT: step 1 appends a PENDING Execution Log row and HALTs before step 1.2 "under the TL 1142 Branch 1 rule (PENDING or empty `Chosen:`)". This matches TL 1142 and the TL 1267 wording "before step 1.2". 7.17 is "below" TL 1142, so the Branch rule applies to it. Gaps in the halt details are N-01.
   - Resume: step 3 (line 54) fills the four lines of that same file, with `Decision source:` quoting the owner, and applies Branch 2: RESOLVED, append to the Execution Log, status back to Doing, clear `blocker_reason`. That is the TL 1142 Branch 2 text.
   - Follow-up: an approval resumes into step 2 (line 53). Option A names the DESIGN edit for 7.3, 11, 12 and 15.1 with its own gate; the 8.10 and 10.3 count source taken from the approved count in the 1.0a facts file; the 7.16 forbidden list and grep (TL 1259, TL 1262) plus a re-capture; and the review re-run (still M-02, left by the caller). Option B is the re-planning sentence. These cover every INV-021 consumer: 7.3, 11, 12, 15.1, TL 1259 and 1262, TL 1482 and 1485, and TL 1793.
   - Success test: the success test (line 55) checks that the decision file exists with `status: PENDING` and the empty decision lines, so a missing or malformed file fails. It also checks the PENDING row, the HALT before step 1.2, a resume step naming the file, the refusal line, and the follow-up targets or the re-planning sentence.
2. Minor fixes M-01, M-03, M-04 and M-07: PASS, with notes.
   - M-01: INV-016 is no longer cited for the refusal. INV-021's sentence "If the owner declines, the plan works" is quoted correctly (probe line 34). TL 1482 holds "exactly 10 templates after item 6.3" and "From the 1.0a facts: ... the cursor field". TL 1485 holds "a count of `ALLOWED_ORCA` entries is 10". DESIGN 973 (open item 5) holds "A full page of `WORKER_LIST_PAGE` rows sets truncated and the total is a lower bound; no cursor template". All cited correctly. Outcome scope is N-02.
   - M-03: the rationale at lines 43 and 267 now reads TL 2804 correctly ("Every HALT line, every owner decision ... is appended here as one row"; TL 2802 is the OQ-1 (R5) row). Residual wording at line 40 is N-06.
   - M-04: partly applied (N-04).
   - M-07: rows INV-001, INV-002 and INV-017 were added (lines 270 to 272). INV-001: TL 279-283 is item 2.6, which creates `### Fix cycle 3`. Correct. INV-002: TL 998 sets `Total: 10 deviations.` and TL 1005 checks 10. Correct; the item number is wrong (N-05). INV-017: TL 1005 (`TODO`/`TBD`), TL 1260 (capture item 9 "only if Orca is already unavailable"), TL 1269 (open item 2 HALT), TL 1276 (`SOURCES.md` when nothing was captured) and TL 1638-1644 (item 9.3, header at TL 1639; the Run-not-readable HALT at TL 1643). All correct. TL 1638 is a blank line, which is harmless.
3. No new defect in numbers or other changes: PASS.
   - F-01 is unchanged.
   - The F-02 pattern is byte-identical to the one the first review tested: `grep -c '^| [^|]* | 6\.2 | .*OQ-1 (R5) RESOLVED'`. It prints 0 against the TL today.
   - Severity counts are unchanged: HIGH 2, MEDIUM 13, LOW 13 in both the header (line 308) and the table (lines 314 to 341).
   - The `row_coverage` numbers are the ones the first review verified: 109/30/10/3, 0.960 and 0.914. `calibrated_confidence` is 0.77.
   - Line positions show no other text was added or removed. The first review's line 266 is now 267, after the one note added at line 45. Its line 303 is now 307, after that note and the three new `not_carried` rows.
   - Internal references still resolve. "F-03 step 2" (Change 13 line 125, Change 14 line 132, Change 30 line 244, field plan line 307) still points at the follow-up step. Risk table "Change 3 steps 1 to 3" (line 281) matches the three steps. The F-03 provenance keeps INV-016 (lines 55, 316), which is still fair, since step 3 contrasts with it.

VERDICT: PASS

## Self-Audit

- I read the plan in full and re-read every TL and DESIGN line I cite. I did not take the fix log's claims on trust: I checked each one against the plan text and the TL.
- Limits: the plan file is untracked, so I could not diff it against its pre-fix version. "No other change" rests on the first review's quoted numbers, the unchanged pattern and the line-shift arithmetic, not on a byte diff. I did not re-run the `row_coverage` script; the numbers match the first review, which did.
- The grading is consistent: N-01 to N-06 change no severity, count or verdict, and none stops the INV-021 approval path from working. N-01 is the closest call. It does not block, because Branch 2 reads only `status:` and the four decision lines, and step 1 writes both.
