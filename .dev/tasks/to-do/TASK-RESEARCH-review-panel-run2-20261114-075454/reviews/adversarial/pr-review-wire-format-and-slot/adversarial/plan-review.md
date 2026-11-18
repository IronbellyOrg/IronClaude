# Plan review: refactor-plan.md (slot C-10)
Counts (5) verified OK: 49 points; winners A 9 / B 6 / Hybrid 16 / Neither 18; 20 probe findings (6 ADDRESSED, 14 UNADDRESSED); 5 HIGH UNADDRESSED (INV-002, 007, 008, 011, 012) and 9 MEDIUM. 16 changes, 2.27% margin, 9 vs 6 tiebreak, 47/49 files, 8 terminal_clean sites all match. Defects found: 18.

Unsupported attribution (1)
1. Change 1: "label Hybrid, 75% and 65%". C-001 (the Hybrid-labelled point) is A 75 / B 60 (B-R2 table: "60 changed from 65"). 65 is B-R2 section 2 row 2, a different table.
2. Change 2: "both advocates say either is acceptable" (CORE_PURE_FILES append vs new test file). Only B says it (B-R2 1.1, "stake is low"). A-R2 cond. 2 and 6: test_static_grep.py not edited, "all new tests are new files". Change 9 repeats "new tests are new files" while Change 12 keeps "only if AM-5 is taken": inconsistent, and AM-5 is unanswered by A like AM-1 to AM-4.
3. Change 2: "B conceded S-002 to S-004, C-004, C-005" is cited to A-R2/B-R2; it is B-R1 Concession 4. Matrix winners for S-002 and S-004 are Hybrid, not A.
4. NOT-made table, C-006 row: "No quorum rule exists outside the ledger (0 matches)". Sources: 0 matches in cli/review and pr_submit; evaluate_quorum DOES exist outside the ledger (cli/reflect/fallback.py:161-179, wrong shape). Change 3 words it correctly; this row does not.
5. Change 15: "The probe's INV numbers are the debate's own". A-R2/B-R2 use INV-003 (R-C01: repair step vs pins, HIGH) and INV-007 (R-C03). Probe INV-003 is a different thing (checkout vs head tree); probe INV-007 restates R-C03's. Number collision, no disambiguation in the plan.

Conclusions the debate did not reach (2)
6. Overview "Risk level: Medium overall"; Risk Summary Change 1 "Low", Change 3 "Medium". Debate status is BLOCKED_BY_INVARIANTS with 5 HIGH. Change 3's rule is hit by HIGH INV-007, INV-008, INV-011; Change 1's severity rule by B's D1 (HIGH) and probe INV-012 (HIGH). Plan's ratings are its own.
7. Overview: "Changes 3, 5 and 15 carry open probe findings; the others are settled by both advocates". Also open or amended: Change 1 (D1, INV-012, 018, 019), 6 (D5, INV-014, 015), 7 (INV-009, AM-3), 9 (INV-019, AM-1 to AM-4 fixtures), 10 (AM-2).
8. NOT-made table, S-009/S-010: debate winner is B (58%, 55%: easier to audit, five further objections). Plan declines them with its own rationale ("bear on audit ease, not on the design"; S-005 only was Neither). Adopting "Limits and open items where useful" is not a debate conclusion.

Contested content presented as settled (4)
9. Change 1 gives "path/line/claim from representative, severity = max over members, one Finding per cluster" as agreed by both. B-R2 accepts the max only as "necessary but not sufficient"; D1 (HIGH): max severity paired with the representative's category and claim is wrong; AM-1, AM-2 unanswered; probe INV-012: AM-1 still insufficient for same-category clusters.
10. Change 7 (from "both"): "missing ranges is counted in dropped". That is A's rule; B-R2 D4/AM-3: "degrade, never drop". Contradicts Change 13.
11. Change 3 states only B's strict rule. A's C10-R standing rule also made the panel incomplete on missing changed_ranges and on "every cluster dropped"; B amends both (AM-3, AM-4, D3). Debate lists C-006 among content-unresolved points; the plan treats it as settled.
12. Base keeps A's "CRITICAL row restated / never lowered" (base-selection strength 5, U-004); Change 10 is silent. B-R2 D2 shows the claim fails through the router (ceilings, in_diff drop, severity_router.py:171, :178-189), unanswered. Merged text must not assert it as fact.

Omissions (3)
13. Convergence result: label agreement 49/49 (Round 1: 33/49), content-adjusted 44/49 (0.90), status BLOCKED_BY_INVARIANTS, unresolved C-001, C-002, C-006, S-004, S-008 plus owner items C-008, A-005, A-006. Not carried.
14. C-002 (in_diff): Hybrid 60/60: converter computes in_diff from changed_ranges, reviewer-stated values only compared (M2); pr_submit has no hunk parser, new code (X-010; A-R1 Concession 5, premise [UNVERIFIED]). Change 4 lists body, confidence, original_line, reviewer but not in_diff.
15. D6 (converter invocation path; no second python fence; package __init__ export would edit an existing module, against "zero edits") is dropped from Change 13 although its source says "D1 to D7". Probe INV-018 depends on it.
16. Change 12 omits invariants both Round 2 files leave open: INV-003 (R-C01, HIGH), B's INV-L (HIGH before promotion), INV-M (MEDIUM), and INV-007 (R-C03, HIGH) outside Change 3.
17. Change 12 files INV-I under "held (reporting only)". Both Round 2 files list INV-I, HIGH, under "invariants this resolution leaves open".
18. S-006 (B wins, 58%): A's "preserved by construction" overclaimed (X-001, W4); B's "endangered in a narrow sense" was more accurate. Not carried in any change. Also Change 16: "four keys" promotion triggers, but original_line is dropped outright (A-R2 row 4, B-R2 1.3) and confidence is unset; B's second change-my-mind trigger (no summary at all shrinks D2/D5) is omitted.
