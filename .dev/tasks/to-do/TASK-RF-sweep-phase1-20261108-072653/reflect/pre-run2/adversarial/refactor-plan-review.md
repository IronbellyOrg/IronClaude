# Refactor Plan Review (Step 4, analytical reviewer)

- Plan under review: `refactor-plan.md` (391 lines, 30 changes, 28 findings)
- Reviewer: analytical reviewer, report-only. The plan was not edited.
- Date: 2026-11-08
- Evidence read: `base-selection.md`, `debate/consensus.md` (all five parts), `invariant-probe.md` (22 rows), the three variant files (finding ids only), `../coverage-matrix.yaml`, `../reviewer-cards/reviewer-{1,2,3}-card-calibrated.yaml` line 19, the tasklist (TL) and `docs/designs/orchestrator-mode.md` (DESIGN).
- Method: every TL and DESIGN line the plan cites in a claim was re-read (38 TL lines, 27 DESIGN lines). The F-02 pattern was run against the real tasklist and against temporary copies in a private `/tmp` directory, removed afterwards.
- Grading: blocking means the merged verdict would carry a wrong or unusable recommendation for a finding the caller ruled must be fixed, or a wrong number. Minor means a precision or completeness fix that does not change any severity, count or verdict.

## Findings

### B-01 (blocking): the F-03 branch records the owner question in the Execution Log, but its own resume rule needs a decision file

- Where: Change 3, recommendation step 1 (plan line 51) and step 3 (plan line 53); field plan `unaddressed_invariants_high` (line 303).
- What is wrong: step 1 says the new 7.17 branch "writes a PENDING owner record (decision, options, Given by, Source) to the Execution Log and HALTs". Step 3 says an owner answer resumes "under the TL 1142 Branch 2 rule". TL 1142 defines that rule over a decision file: every decision-record item "writes its file with: `needs_human_decision: true`, `status: PENDING`, the question quoted, the options quoted, ... and the empty block `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:`", and Branch 2 fires only when "all four lines [are] filled" and then "sets `status: RESOLVED`". An Execution Log row has no `status:` field and no `Chosen:` line, so neither an approval nor a refusal can be recorded in the form TL 1142 checks. The approval path that INV-021 asks for therefore has no valid trigger, and "Given by, Source" are the OQ-8 field names (TL 1237), not the TL 1142 ones.
- Why blocking: F-03 carries the caller's HIGH obligation (INV-021), and the plan tells the merge executor to copy the F-03 wording exactly (line 391). The success test (line 54) only greps for PENDING and HALT, so it would pass this inconsistent text.
- Smallest fix: reword step 1 to "the branch writes a decision file under `phase-outputs/plans/` in the TL 1142 form (needs_human_decision, PENDING, question, options, the four empty decision lines), appends a PENDING row to the Execution Log (TL 2804), and HALTs before step 1.2". Add "a decision file in the TL 1142 form" to the success test.

### M-01 (minor): F-03 step 3 justifies the refusal path with INV-016, which covers a different case

- Where: Change 3, step 3 (plan line 53).
- What is wrong: INV-016 is the case where step 1.0a finds no cursor field. The refusal case is different: a cursor field was captured and the owner refuses the cursor template. TL 1482 (8.10 Context) still reads "From the 1.0a facts: ... the cursor field", so 8.10 would be told to use a cursor that has no allowlisted template. INV-021 does say "If the owner declines, the plan works", so the plan follows the probe, but the cited reason does not show it.
- Fix: step 3 should also say the refusal is recorded in `1.0a-facts.md` as "cursor field present, no cursor template; the DESIGN 973 full-page lower bound applies", and cite INV-021's decline sentence instead of INV-016.

### M-02 (minor): F-03 option A adds a gate re-run that the evidence does not ask for and that would not check the change

- Where: Change 3, step 2, option A (plan line 52).
- What is wrong: option A asks for "a DESIGN edit item ... with its own review gate" and also "a re-run of the R5 review gate (6.5 to 6.22) over the new edit". INV-021 asks only for "a DESIGN edit item with its own gate". The R5 lens prompts are written for the `--agent-wait` edit (TL 1012: "Try to prove the R5 edit broke the design's form"; TL 1019: "find a DESIGN sentence that still forbids `worktree ps --agent-wait`"), so re-running them would not review a cursor template or a `run-current --json` approval. Option A also omits the DESIGN 17 open items 3 and 5 (DESIGN 971, 973), which the probe's own consumer list (invariant-probe.md line 42) names.
- Fix: drop the R5 re-run clause, keep "its own review gate", and add open items 3 and 5 to the DESIGN edit targets. Option B already satisfies INV-021 on its own, so this does not block.

### M-03 (minor): the reason given for rejecting the probe's "drop the append" option misreads TL 2804

- Where: Change 2, Risk (plan line 43), and the `not_carried` row "INV-006 options" (line 266).
- What is wrong: the plan says dropping the append "removes the per-item log row the TL 2804 rule asks for". TL 2804 says "every owner decision ... is appended here as one row". It asks for one row per decision, not one per item, and TL 2802 is already that row for OQ-1 (R5). The chosen fix adds a second row for the same decision. The chosen fix still works, as tested below, so this is about the rationale only.
- Fix: replace the rationale with a true one, for example "keeps item 6.2 a checkable action; the 6.2 row is an item-level record next to the build-time row".

### M-04 (minor): the F-02 pattern is correct but fragile in three ways the plan does not state

- Tests run (GNU grep, basic regex): against the current TL `grep -c '^| [^|]* | 6\.2 | .*OQ-1 (R5) RESOLVED'` prints 0. On a copy with one row `| 2026-11-08T15:00Z | 6.2 | ... | OQ-1 (R5) RESOLVED by the owner 2026-11-08: ... |` inserted after TL 2802, it prints 1 and matches only that row. A second appended row gives 2. TL 991, TL 993 and TL 2802 do not match: TL 991 and TL 993 start with "  - **", and TL 2802's Item cell is `6.1-6.4`, which `[^|]*` cannot cross into a ` 6\.2 ` cell. In a basic regex, `|`, `(` and `)` are literals, so the pattern needs no `-E`. The plan's claims (line 41, line 44) hold.
- Fragilities: (a) with `grep -E` the leading `^|` becomes an empty alternative and the pattern matches every line (2896 on the TL; tested). (b) A row written without spaces around the pipes (`|...|6.2|...|`) gives 0 (tested). (c) If the example row in the new 6.2 Action is placed on its own line, for example in a code block, that line starts with `|` and matches (tested: 1), so the count after a correct append becomes 2. The plan's inline form avoids (c).
- Fix: next to the pattern in Change 2, add "plain grep, never -E; keep the example row inline in the Action text; cells are separated by ` | `". Also change the 6.2 Output field ("The `### Execution Log` line.", TL 992) to "row".

### M-05 (minor): F-12 names only part of the lines that carry the R5 section list

- Where: Change 12 (plan lines 116 and 117).
- What is wrong: the list "sections 7.3, 11, 12 (NFR-014 row), 13 ..." appears at TL 999 and TL 1004, in every lens Context from TL 1011 to TL 1067, and in the fix and verifier items 6.15 to 6.21 (TL 1082, 1088, 1095, 1110, 1116, 1123). The recommendation names the 6.3 Output, the 6.4 checks and the 6.5 to 6.13 inputs, and the success test checks only TL 1011 and TL 1018. A section 4 defect found by a lens would then fall outside the fix and verify scope.
- Fix: name every line that carries the list (6.3 Output, 6.4 Context, 6.5 to 6.13, 6.15 to 6.21) and grep all of them in the success test.

### M-06 (minor): part of the F-15 remedy already exists in the tasklist

- Where: Change 15 (plan line 138).
- What is wrong: item 7.14 (TL 1236) already asks for "one Run id with at least one Dispatch (best one live and one settled worker, so capture items 4 and 13 can be recorded)". What is missing is a check: 7.15 Branch 2 and its Verification (TL 1244, TL 1246) accept any Run id. As written, a reader can show the first half of the recommendation is already done.
- Fix: say "7.15 Verification checks that the named Run has at least one Dispatch row (requested at TL 1236 but never checked)". The HALT half (TL 1269) stands.

### M-07 (minor): three ADDRESSED invariants are not traced anywhere in the plan

- Where: Changes NOT Being Made table (lines 250 to 269).
- What is wrong: INV-001, INV-002 and INV-017 (all ADDRESSED, LOW, "nothing missing") appear nowhere in the plan, while INV-004, also ADDRESSED and LOW, has its own `not_carried` row. Every other id from INV-001 to INV-022 is in a finding's provenance, in Change 29 (INV-014) or in `not_carried` (INV-004, INV-019). All 29 card ids (R1-G1 to G9, R2-G1 to G9, R3-G1 to G11) and all 21 consensus Keep ranks and 3 Drop rows are accounted for.
- Fix: add one `not_carried` row "INV-001, INV-002, INV-017: ADDRESSED, LOW, no gap; no finding".

## Check results by point

1. Traceability: every change traces to a card, a consensus point or a probe row. The one untraced element is the R5 gate re-run in F-03 option A (M-02). PASS with a minor note.
2. Kept and dropped findings: the 29 card ids, the 21 Keep ranks and the 3 Drop rows all map to a finding or to `not_carried`, each with a reason. All 9 UNADDRESSED invariants appear in provenance. The only gap is that INV-001, INV-002 and INV-017 are untraced (M-07). PASS with a minor note.
3. Severity: F-01 HIGH (C-012 at 98%, TL 1436 against TL 1433) and F-02 HIGH (INV-006, re-tested above) both meet the "correct delivery cannot satisfy the check" bar. MEDIUM labels follow calibration or the probe's own severity (INV-005, 008, 015 and 018 are MEDIUM). F-03 stays MEDIUM by X-002 at 95%, with INV-021 cleared by the remedy, as the caller ruled. Counts are HIGH 2, MEDIUM 13 and LOW 13, which matches the table. PASS.
4. F-02 pattern: it works as claimed (M-04 test results). PASS with a minor note.
5. F-03 against INV-021: the content of the approval path is complete. Option A names the DESIGN edit with a gate, the 8.10 and 10.3 count source, and the 7.16 forbidden list and re-capture; option B is the re-planning sentence. But the route that records an approval contradicts TL 1142 (B-01). FAIL.
6. row_coverage: 109 + 30 + 10 + 3 + 0 = 152. Parsed 97/24/5/0 = 126 and inferred 12/6/5/3 = 26 add up to the union. Against the matrix, parsed was 98/24/4/0 and inferred 12/6/5/3, matched_inferred 18. The only parsed change is step-1.0a, from covered to partial. That gives coverage_pct 121/126 = 0.9603 and union 139/152 = 0.9145. The per-card rows (76/44/32) and the per-column sums before and after the INF-019 change are consistent. `calibrated_confidence` 0.77 matches (0.71 + 0.81 + 0.79) / 3, read from line 19 of each calibrated card. PASS.
7. Line numbers: all re-read lines are correct. TL lines checked: 163, 194, 269, 454, 784, 989, 991, 993, 997, 998, 999, 1005, 1007, 1011, 1018, 1142, 1257, 1258, 1259, 1260, 1262, 1267, 1269, 1276, 1433, 1436, 1448, 1482, 1485, 1627, 1640, 1643, 1793, 2256, 2469, 2471, 2802, 2804. DESIGN lines checked: 80, 157, 181, 196, 211, 219, 221, 438, 442, 454, 459, 466, 527, 552, 636, 638, 738, 794, 868, 873, 874, 883, 939, 970, 971, 973, 987, 993; section 5 starts at DESIGN 223, so section 4 is 157 to 222. One trivial imprecision: line 10 gives the Execution Log as "2795 to 2804", but the heading is at TL 2797 (TL 2795 is `## Task Log / Notes`). PASS.

VERDICT: FAIL

Blocking findings: B-01. Minor findings: M-01 to M-07. Fixing B-01 takes one sentence in Change 3 step 1 and one clause in its success test. No severity, count or coverage number needs to change.
