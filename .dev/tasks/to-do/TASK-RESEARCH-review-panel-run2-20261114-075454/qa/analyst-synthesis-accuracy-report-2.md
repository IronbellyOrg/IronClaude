# Synthesis Accuracy Report 2 (Gate 2, partition B)

**Files reviewed:** synthesis/synth-05-options.md, synthesis/synth-06-conflict-log.md, synthesis/synth-07-recommendation-architecture.md
**Lens:** synthesis-accuracy (criteria 1-5), Deep tier
**Grading:** owner grading override (qa/grading-override.md) applies
**Date:** 2026-11-14
**Status:** Complete (verdict FAIL, 3 blocking, 10 minor)

---

## Method and scope

- Read completely: synth-05-options.md (969 lines), synth-06-conflict-log.md (412 lines), synth-07-recommendation-architecture.md (334 lines), all under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/synthesis/`.
- Compared against research 01-18, scope/02, research-notes.md (RN), gaps-and-questions.md (GQ) and web-01/web-02 (spot reads and targeted greps; research 19-24 value ledgers used only to confirm two figures).
- Grading: owner override `qa/grading-override.md` applied. BLOCKING only when a decision, recommendation, conflict-log outcome or a number the recommendation rests on would be wrong or unsupported, when a required deliverable or section is missing, or when there is a security, data-loss or safety-boundary risk. Everything else is MINOR and carries the line `(minor under grading override)` where the old definition would have called it blocking. CRITICAL / IMPORTANT / MINOR is an information label only.
- Independence: the run-1 research folder and the queued run-2 note were not read, listed, searched or cited. No file was modified except this report. No repo-wide search of `.dev/tasks/` was run.

## Findings

Columns: # | Severity (info label) | Blocking Y/N | File and location | Finding | Evidence | Proposed fix.

### Blocking findings (3)

| # | Severity | Blocking | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| B1 | IMPORTANT | Y | synth-07, "Choices the evidence cannot decide" (lines 47-66) and "Adjudication register" (lines 231-248); synth-06 6.12.9 (lines 359-375); synth-05 6.8 axis status (line 643) | The adjudication table does not match the 15 routed slots of synth-06 6.12.9. Four slots (C-01 core shape and finding contract, C-11 rf-qa first step, C-12 collaboration, C-13 process redesign) have no marker, although the recommendation already picks one position in each (axes 1, 2, 6, 7, the rf-qa attachment point in axis 11 and 7.2.2, and the metric-of-record part of C-14 in axis 9). Two markers (A-1 convergence threshold, A-2 single vendor) have no slot, because synth-06 decides both (CV-1, CV-2: DECIDED-BY-EVIDENCE, 0.80 and "the code degrades"), while synth-05 6.8 calls both UNDECIDABLE and synth-07 marks both pending. The same item therefore has three different statuses in the three files. synth-07 line 31 promises that every axis whose choice depends on an undecidable conflict is listed in the adjudication table; axes 1, 2, 6 and 7 are not. The later adjudication would never debate C-01, the highest-impact slot, and the final report would show its position as the chosen design. | synth-07 axes table rows 1, 2, 6, 7 (lines 35, 36, 40, 41) carry no `[PENDING-ADJUDICATION]`; a grep of synth-07 finds exactly 14 markers, all A-1..A-14, and no cross-reference to C-01..C-15 anywhere (only "C-01..C-19" of research/09 at line 319). synth-06 slot rows: C-01 line 361 (Position A = findings-v2 superset, locator-agnostic annotate, unknown keys open = synth-07 axis 2 choice), C-11 line 371 (Position A = start at the `/task` gate = synth-07 7.2.2 verdict text), C-12 line 372 (Position A = H1 and H2 plus static kit, exchange optional and off = synth-07 axis 6 choice), C-13 line 373. synth-06 CV-1 line 186 and CV-2 line 187 are "DECIDED-BY-EVIDENCE"; synth-05 line 643 "UNDECIDABLE-BY-EVIDENCE for the convergence threshold ... and the single-vendor posture"; synth-07 lines 53-54 (A-1, A-2) pending; synth-07 line 270 (C-17) "Unresolved". | Add a marker (with slug) for C-01, C-11, C-12, C-13 and the metric-of-record part of C-14, mapped one-to-one to the slot ids; either drop A-1 and A-2 or give them a slot, and make synth-05 6.8, synth-06 CV-1/CV-2 and synth-07 agree on one status for the threshold and the single-vendor posture (the recommended default value does not change). |
| B2 | IMPORTANT | Y | synth-07 axes table rows 1 and 2 (lines 35-36) against synth-05 6.1 (lines 21-101) and 6.2 axis status (line 172); RN line 110 | The "Options in the evidence" cell of axis 1 does not list the options the research set for this axis. RN line 110 and synth-05 6.1 give A (v2 kernel core, v1 loop as module), B (v1 package core, reflect as module), C (thin shared contract with per-module engines), D (fix the harness and the two parsers only, defer). synth-07 axis 1 instead lists (a) extend the kernel, (b) adopt the E3i scripts, (c) make engine A the base, (d) E2 harness scripts as the base. Options B, C and D, which synth-05 leaves UNDECIDABLE against A and which synth-06 C-01 keeps as Position B, are never weighed in "Why" or "Trade-off accepted"; the stated reasons (F-1 to F-4, E3i cannot be imported, engine A sees tasklist text only, E2 has no product code) only defeat alternatives nobody proposed. Axis 2 states "unknown keys stay accepted by the core (no whitelist)" as the chosen policy, while synth-05 line 172 says open versus closed unknown-key policy is UNDECIDABLE-BY-EVIDENCE ("no source measures which fails less") and synth-06 CO-4 routes it to C-01. | synth-07 line 35 (axis 1 row) versus RN line 110; synth-05 lines 23-32 (option table A-D), line 101 (axis status), line 172; synth-06 CO-4 line 207 and slot C-01 line 361 Position B. | Rewrite the axis 1 options cell with the four RN candidates and state why A is preferred over B, C and D, or mark the axis pending (see B1); mark the unknown-key policy of axis 2 as pending under C-01. Closing B1 and B2 together is one edit of the axes table. |
| B3 | IMPORTANT | Y | synth-06 C-S3 (line 75), SV-5 (line 172) and 6.12.10 "What the evidence decided" rows 1 and 3 (lines 396, 398) | Design inferences are labelled DECIDED-BY-EVIDENCE and handed to the debates as requirements to respect. The rulings are: the boolean `blocking` is the only field that drives verdict, ledger brief and cap; the blocking rule is a per-lens property; `Medium` is not a core token; the default cap is `max_fix_cycles = 2` with a halt-reason enum. The research marks exactly these statements as "Design inference (not code facts; tagged as recommendation)" and raises them as owner questions (Q1, Q3, Q5). gaps-and-questions GQ-159 logs "Is `blocking` plus the three labels acceptable as the core pair" as OPEN-QUESTION, logged-open, "owner confirms in Section 9". synth-05 6.2 (end of axis status) correctly says the same policy "is labelled a design inference in R12 and carries no option here". The code facts underneath (two shipped blocking rules, ten primitives pinned, caps of 2 in four consumers) are verified; the ruling on top of them is not evidence-decided, so the conflict-log outcome and the evidence-decided summary overstate. | research/12 line 191 ("Design inference (not code facts ..."), lines 192 and 194 (the two statements), line 210 (Q1, Q3, Q5); gaps-and-questions.md line 183 (GQ-159, OPEN-QUESTION); synth-05 line 172; synth-06 6.12.0 classification rule (line 43: DECIDED = code, data or a reproduced run decides it). | Reclassify the "core carries `blocking` only" and "default cap 2 + halt-reason enum" parts of C-S3 and SV-5 as design inference (keep the verified code facts as decided), drop them from the "What the evidence decided" table or move them to a "design inference, owner confirms" row, and align synth-07 axis 2 and axis 4 wording. |

### Minor findings (notes only, never fixed in the gate)

| # | Severity | Blocking | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| M1 | MINOR | N (minor under grading override) | synth-05 lines 52 and 279 (6.1 option A risk, 6.4 option 2 effort) | Stale count: "six of the eight pins read" in R03 section 2. synth-06 RX-8 (line 292) and LG-4 (line 185) carry the correction "8 of the 9 pins". research/03 line 151 still has the old "6 of the 8" text, but its own table (lines 138-146) lists nine pins. No decision rests on the count. | research/03 lines 136-151; synth-06 lines 185, 292 | Use "8 of the 9" in synth-05, or cite the research text and RX-8. |
| M2 | MINOR | N (minor under grading override) | synth-05 line 292 (6.4 option 3 reuse) | "replays 42 recorded legacy contracts, 0 differences" is wider than the source, which says "new degraded reasons 0" over 42 legacy runs. | research/06 line 234; research/07 line 23 | Say "0 new degraded reasons over 42 legacy runs". |
| M3 | MINOR | N (minor under grading override) | synth-05 line 182 (6.3 figures table) | "264 (89 rows x 3 packages)": 89 x 3 = 267. The source repeats the figure without explaining the 3 missing merges; the conclusion (the unit of the 92/80/49 figures) is unaffected. | research/02 line 97; research/08 line 91 (89 rows examined by audit D) | Quote 264 as "reported" or note that the product does not equal 267. |
| M4 | MINOR | N (minor under grading override) | synth-05 line 66 (6.1 option B, Pros) | Attributes "the `blocking` boolean plus CRITICAL/MAJOR/MINOR" to the repo's canonical rule at `pragmatic.md:224-231`. research/12 says the canonical rule is binary blocking/minor (V6, `pragmatic.md:225-226`); CRITICAL/IMPORTANT/MINOR at `:229` is rf-qa's scale (V2); CRITICAL/MAJOR/MINOR is the findings schema (V1). The correct statement appears in synth-05 6.2 option 2 (line 140). | research/12 lines 56, 62, 76, 188 | Cite the findings schema, not the canonical rule. |
| M5 | MINOR | N (minor under grading override) | synth-05 line 119 (6.2 facts paragraph) | "seven severity vocabularies are in the repo" is stated flat; synth-05's own corrected-claims row (line 907) and synth-06 SV-2 (line 169) say the count is definition-dependent (six label sets plus two orthogonal axes). | synth-05 line 907; synth-06 line 169; research/12 lines 51-68 | Use the SV-2 wording. |
| M6 | MINOR | N (minor under grading override) | synth-07 line 22 (F-1) | "E1 is a strict superset of E3s for ... the line grammar" while the same file (axis 2, line 36) and research/01 line 102 state that v2 rejects `calibrated_confidence` and has no `prior` lines, which v1 accepts. The substance is covered in axis 2; synth-05 6.1 (line 41) drops "strict". The wording comes from research/01 line 221. | research/01 lines 102 and 221; synth-07 line 36; synth-06 CO-2 (line 205) | Say "superset except `calibrated_confidence` and `prior` lines". |
| M7 | MINOR | N (minor under grading override) | synth-07 line 58 (A-6) and line 269 (C-16) | Says the 26/40 duplicate figure "is not reproduced" / "run ids behind 26 unknown". synth-06 FX-15 (line 110), DATA-11 (line 260) and GQ-002 (line 26) record that 26 of 40 reproduces with run ids `r1..r40` and 30 of 40 with `run1..run40`. The recommended default (strict distinct on) is unaffected. | gaps-and-questions.md lines 26 and 372; research/17 lines 26 and 527 (older text) | Align synth-07 with the GQ-002 resolution. |
| M8 | MINOR | N (minor under grading override) | synth-07 line 40 (axis 6, Why) | "the packages' own hooks skip subagent calls" is stated for all packages; synth-06 RX-6 (line 290) and synth-05 line 464 restrict it to the r1, r4 and r5 hooks (r2 has no such branch, r3 has no hook). | synth-06 line 290 (cites GQ-323; research/09 lines 41-43, 120) | Name r1, r4, r5. |
| M9 | MINOR | N (minor under grading override) | synth-06 6.12.10 (lines 381-390) and 6.12.2 FX rows | Count and label drift. Table B reports 1 routed row (FX-15), but thirteen FX rows are named in slot Conflict-ID cells (FX-1, 2, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20) and the FX-9 Decision cell says "C-02 and C-03" while the row is listed only in slot C-03. The totals (188 rows, 133 decided, 55 routed) add up arithmetically (recounted per table); only the meaning of "routed" is mixed (row routed versus row cited by a slot). | synth-06 lines 104, 105, 359-375, 384, 390 | State the counting rule once, or count cited-by-slot rows separately. |
| M10 | MINOR | N (minor under grading override) | synth-06 CL-C09, CL-C10, CL-C19 (lines 150, 151, 160) | Classed DECIDED-BY-EVIDENCE while their evidence is tagged [UNVERIFIED-slice] (research/09 lines 179, 180, 189). The log's own rule (line 46) limits that classification to "treatment, not stated as fact"; the decisions they carry ("a re-ask gets the identity check", "use the unrounded value", "no design effect") are harmless. | research/09 lines 179, 180, 189; synth-06 line 46 | Tag the Decision cell "treatment only". |

### Observations that are not findings

- The `Effort` and `Risk` rows of synth-05 are option attributes, defined as such in the reading guide (lines 16-17); no risk register, roadmap, branch plan or PR plan appears in any of the three files. synth-06's "(plan item)" cells (FX-3, FX-12, FX-22, VM-6, CO-39) point forward to a later plan and contain none.
- synth-06 CL-X2 (line 126) gives luna "0 to 1.0"; research/09 line 151 says "0 to 0.8" but lists rates of 1.00 and 5/5 in the same row. The synthesis is the arithmetically consistent side.
- Marker form: 14 markers `[PENDING-ADJUDICATION: <slug>]` only in synth-07, each slug kebab-case and at most 40 characters (longest, `convergence-threshold-0-80-vs-0-75`, is 34), each appearing once in the choices table. Allowed by design, not a defect at this gate.
- Every [CODE-CONTRADICTED] and stale-documentation item sampled from the Stale Documentation sections of research 02, 03, 11, 15 (and the 13 RN claims) is surfaced: ledger docstrings (LG-3, VM-4), `__init__.py`/`runner.py:457`/SKILL 9.3 row (RX-11, CV-7), telemetry and manifest invariants (CO-40, RX-10), the 13 RN claims (DOC-1..DOC-13, order and GQ ids checked: GQ-062, GQ-063, GQ-244 read).
## Claim traces (criterion 3 and 4)

Each row was traced to a research file in this review. "OK" = the research file carries the claim as stated. Items with a defect point to a finding above.

### synth-05-options.md (27 claims traced)

| # | Claim in synth-05 (line) | Traced to | Result |
|---|---|---|---|
| 1 | 92 dropped lines = 56 + 18 + 14 + 3 + 1 (183) | research/02 section 5.1; arithmetic | OK |
| 2 | 49 blocking = 24 + 14 + 10 + 1 (185) | research/02 section 5.1; arithmetic | OK |
| 3 | truncation reaches 88 of 92 (95.7%) and 48 of 49 (98.0%) (197) | research/02 section 5.2; arithmetic | OK |
| 4 | 264 merges from 89 rows x 3 packages (182) | research/02 line 97 | source says it; 89 x 3 = 267, see M3 |
| 5 | luna verbatim anchor fidelity 91.4% (194) | research/02 line 222; research/20 VL-20-720 (363 of 397) | OK |
| 6 | file sizes findings_v2 304, cluster 487, manifest 534, panel 707, card_convert 517, verify_cmd 184, findings 457, ledger 494, merge_cmd 118, ledger_cmd 137 (53, 64) | research/18 line 199 | OK |
| 7 | haiku class served `gpt-6.1-sol` in five calls A1, A2, B1, B2, B3 (348) | research/04 line 112 | OK (source adds "by design of the combos") |
| 8 | A-r3: three reviewers and calibrators served `claude-sonnet-5-5`, contract says `calibrator_diversity: full` (348) | research/04 line 113 | OK |
| 9 | calibrator lost its class in 6 of 15 combo runs (348) | research/07 line 89 | OK |
| 10 | static kit +59% elapsed (281.567 vs 176.9175) and +55% tokens, n = 3 (420) | research/09 lines 84, 197; 281.567 / 176.9175 = 1.592 | OK |
| 11 | "six of the eight pins read" (52, 279) | research/03 line 151 | stale, see M1 |
| 12 | variants total 7,589 lines; 17 of 17 hashes match (733, 778) | research/14 lines 101, 221 | OK |
| 13 | engine A contract 1.0, 32 keys, 10 outside frozen lists, 89 of 110 stable names absent (566) | research/06 lines 92, 286 | OK |
| 14 | Stage 2 exit: 13 of 20 runs, EV-1 8 of 13 (3 unparseable + 4 merged-verdict absent + 1 empty cards), parity 6 of 13, lint 9 of 13, 7 of 28 leaked keys (571) | research/06 lines 189, 197, 233, 243-245 | OK |
| 15 | 36-test verdict matrix, 0.80 constant, exit codes 0/10/11/2 (260, 292) | research/06 lines 54, 303 | OK |
| 16 | replay of 42 recorded legacy contracts, "0 differences" (292) | research/07 line 23; research/06 line 234 | wider than source, see M2 |
| 17 | three defects carry 131 of 147 catches (89%); four never caught in 106 runs (659) | research/20 VL-20-638, VL-20-786 (research/08 G3) | OK |
| 18 | cost fan-out 400 vs 200 per true positive; no incident in 29 manifests (387, 389) | research/15 lines 70, 224 | OK |
| 19 | 175 prose spawn lines in 7 skills, 44 structured lines in 8 SKILL.md files, 23 static-pin test files (816) | research/13 lines 135, 155, 198 | OK |
| 20 | gate D2 0.12 x 14 = 1.68 items (496) | research/10 line 76 | OK |
| 21 | re-review resolves one reviewer, `apply_to: ["first"]`, `panel.py:600` (262) | research/17 DR-019 | OK |
| 22 | `fallback.py` QuorumState: 2 reviewers, 2 distinct ids, not single vendor (synth-07 A-3 uses it) | research/06 line 163 | OK |
| 23 | precheck flagged 510 of 1,047 citations (48.7%): 472 + 7 + 31; 472/510 = 92.5%; 31/1,047 = 3.0% (494) | research/10 Unit 10 (arithmetic checked) | OK |
| 24 | `--env gateway` refused by the reflect profile; max 3 reviewers; launch only sonnet/opus/haiku; no Fable (337) | research/04 lines 21, 29 | OK |
| 25 | `--restricted`, `--session-id`, `--bare`, SubagentStop fields (347, 356, 359) | research/web-02 lines 27, 112, 121, 124 | OK |
| 26 | W01 figures: union of four tools 41.5%; raw agreement overstates by 33 to 41 points; URLs (310, 692, 853) | research/web-01 lines 101, 128, 146, 167 | OK |
| 27 | orchestrator output-token share median 0.59 (387) | research/15 line 204 | OK |

### synth-06-conflict-log.md (24 checks)

| # | Check | Traced to | Result |
|---|---|---|---|
| 1 | C-S1..C-S16 text, ids and file:line cites (lines 73-88) | research/scope/02 lines 531-546, read row by row | all 16 OK |
| 2 | FX-1..FX-22 text and ids (lines 96-117) | research/scope/02 lines 574-595, read row by row | all 22 OK |
| 3 | DOC-1..DOC-13 follow RN rows 242-254 in order | research-notes.md lines 242-254 | OK |
| 4 | GQ id cross-reference for DOC rows | gaps-and-questions: GQ-062 (row 8), GQ-063 (row 12), GQ-244 (row 10) read | OK |
| 5 | CL-X1..CL-X17 and CL-C01..CL-C19 (lines 125-160) | research/09 lines 150-189, read row by row | all 36 OK; classes and 13/4/4/15 count match line 191 |
| 6 | 14 decided + 22 routed split of Table C | recount from research/09 classes (X: 8 decided, 9 routed; C: 6 decided, 13 routed) | OK |
| 7 | totals 16 + 22 + 36 + 31 + 41 + 15 + 27 = 188; 10 + 21 + 14 + 25 + 21 + 15 + 27 = 133; 6 + 1 + 22 + 6 + 20 = 55 | recount of Tables A, C, D, E by row | arithmetic OK (meaning of "routed", see M9) |
| 8 | SV-1 six uses of Medium; SV-4 `card_convert` mapping (168, 171) | research/12 lines 91-92, 218 | OK |
| 9 | SV-5 caps (172) | research/12 lines 119, 194 | facts OK; decided label, see B3 |
| 10 | CV-1, CV-2 thresholds and vendor posture (186, 187) | research/06 lines 201, 208, 326, 374 | facts OK; status inconsistent with synth-05/07, see B1 |
| 11 | CV-9 "51 of 59 recorded dirs" (194) | research/06 line 245 | OK |
| 12 | RX-5 run count alone gives INSUFFICIENT-RUNS (289) | research/06 line 233 (inline qualifier) | OK, research text is the contradicted side |
| 13 | RX-8 "8 of the 9 pins" (292) | research/03 lines 138-151 | OK (research text still "6 of 8") |
| 14 | DATA-3..DATA-6 combos / RESULT.md / quarantine / Qwen counts (252-255) | research/08 lines 39-42 | OK |
| 15 | DATA-11 / FX-15 duplicate counts 30/40, 18/40, 26/40 (110, 260) | research/17 lines 26, 46, 527; GQ-002 line 26 | OK |
| 16 | CO-14 sha256 `044809e3...3bd3481` (217) | research/16 line 200 | OK |
| 17 | VM-3, VM-4, LG-3 docstring contradictions (176-184) | research/03 lines 273-276; research/17 DR-053, DR-114 | OK |
| 18 | CO-1 `KeyError 'anchor'` in `annotate` (204) | research/17 DR-113 (REPRODUCED) | OK |
| 19 | CO-40 / RX-10 telemetry and manifest not enforced (243, 294) | research/15 lines 239-245 | OK |
| 20 | RX-11 reflect documentation drift (295) | research/11 lines 177-183 | OK |
| 21 | 31 distinct GQ ids cited in the slot table all exist | gaps-and-questions.md | OK |
| 22 | slot Conflict-ID cells cover every row whose Decision says ROUTED (377) | row by row against Tables A-G | OK (see M9 for rows cited but not counted) |
| 23 | C-S3 and SV-5 "DECIDED-BY-EVIDENCE" (75, 172) | research/12 line 191-194; GQ-159 | not decided by evidence, see B3 |
| 24 | CL-C09, C10, C19 classed decided on [UNVERIFIED-slice] evidence (150, 151, 160) | research/09 lines 179, 180, 189 | see M10 |

### synth-07-recommendation-architecture.md (24 checks)

| # | Check | Traced to | Result |
|---|---|---|---|
| 1 | F-1 "strict superset" of the line grammar (22) | research/01 lines 102, 221 | wording only, see M6 |
| 2 | F-2 package independence, 25 tracked files (23) | research/18 sections 6.1, 9 | OK |
| 3 | F-3 E2 changed no `src/` or `tests/` file (24) | research/01 section 1.1; RN | OK |
| 4 | F-4 variants 7,589 lines, stdlib only, not installed (25) | research/14 lines 101, 221 | OK |
| 5 | F-5 production uses engine A, contract 1.0 (26) | research/06 lines 166, 286, 332 | OK |
| 6 | defect register totals: 171 rows, 170 distinct, CORE 75 (74), status 64 + 46 + 2 + 59, owners sum to 171 (147) | research/17 lines 406, 502; arithmetic | OK |
| 7 | status of DR-002, 003, 008, 009, 108, 111-114 (151) | research/17 rows 34, 35, 40, 41, 271-277 | OK |
| 8 | DR-117 and DR-121 reproduced in research/15 though research/17 says UNVERIFIED (158, 254) | research/15 line 224; research/17 rows 280, 284 | OK, both sides disclosed |
| 9 | I-6 reserved names and PR-body trigger (142) | research/18 lines 45, 161, 182 | OK |
| 10 | I-5 148 legitimate `src/superclaude` lines in 56 files (141) | research/18 lines 147, 226 | OK |
| 11 | I-9 plugin tree 4 skills (145) | research/13 P14 (line 189) | OK |
| 12 | 7.2.1 P13 50 test files, P14, P15 (185) | research/13 lines 188-190 | OK |
| 13 | 7.2.2 175 / 44 / 23 files (198, 201) | research/13 lines 135, 155, 198 | OK |
| 14 | A-1, A-2 thresholds and vendor posture (53, 54) | research/06 lines 201, 208 | facts OK; status see B1 |
| 15 | A-3 quorum from `fallback.py` (55) | research/06 line 163; research/03 line 267 | OK |
| 16 | A-6 30/40 and 18/40 duplicates; 26/40 "not reproduced" (58) | research/17 line 26; GQ-002 | see M7 |
| 17 | axis 3 numbers 92 / 49 / 88 / 48 / 4 / 1 (37) | research/02 sections 5.1-5.2 | OK |
| 18 | axis 5 reflect profile refuses gateway; Agent enum sonnet/opus/haiku/fable (39) | research/04 lines 21, 29 | OK |
| 19 | axis 6 evidence status (r2 to r5 `lib/` absent, test counts, +59%) (40) | research/09 lines 84, 183, 197 | OK except hook-skip wording, see M8 |
| 20 | contradictions table C-1..C-18 agrees with synth-06 DOC/DATA/RX rows (254-271) | synth-06 lines 272-298 | OK except C-16, see M7 |
| 21 | marker count 14, slug length at most 40, each once (53-66, 330) | grep and count | OK |
| 22 | coverage table covers r01-r18 with exclusions and reasons (309-328) | research Key Takeaways of 01-18 | OK |
| 23 | axes 1 and 2 options and choices (35, 36) | RN line 110; synth-05 6.1, 6.2 | see B2 |
| 24 | adjudication table versus conflict-log slots (47-66) | synth-06 lines 359-375 | see B1 |

## Checklist results (synthesis-accuracy lens, criteria 1-5)

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Section headers match the expected format | PASS | synth-05 has 6.1 to 6.11 in order (plus 6.2.b, 6.5.b, 6.8.b/c, 6.9.b sub-decisions), 6.12.0 to 6.12.10 in synth-06 (section 6.12 conflict log), synth-07 has 7, "Rationale", 7.1, 7.2 with 7.2.1 to 7.2.4 |
| 2 | Table column structure | PASS | every option has Effort / Risk / Reuse / Files / Pros / Cons in an Aspect / Assessment table; every axis has an options comparison table with the five criteria; conflict tables A to G share the seven columns ID / Conflict / Side A / Side B / Sources / Evidence status / Decision or routing; core-contract table (Element / Comes from / Core provides / Modules supply) and future-use tables (Blocker / Exposes / Residual risk / Evidence) are complete |
| 3 | No fabrication; conflicts exist in research; DECIDED rows decided by evidence | FAIL (B3 and the status issues B1, B2); no invented fact found | 75 claims traced above; all 16 + 22 + 36 conflicts match their source rows; two number-level slips are minor (M1, M3) |
| 4 | Findings cite actual paths and evidence | PASS | cites resolved for the sampled rows; every `rNN` cite names an existing research file and section |
| 5 | Each of the 11 axes has at least two genuinely distinct options with pros and cons | PASS in synth-05 (3 or 4 options per axis, each with Pros and Cons rows) | the option set restated in synth-07 axis 1 is not the synth-05 set, see B2 |

Gate focus points: report-only scope holds (no roadmap, branch plan, PR plan or risk register); no doc-only claim presented as current in the sampled rows; [CODE-CONTRADICTED] and stale-documentation findings of research 02, 03, 11, 15 and the 13 RN claims are surfaced; every research Key Takeaway of 01-18 is reflected or excluded with a reason in the three coverage tables (W03 excluded whole with a reason in synth-05); the `[PENDING-ADJUDICATION]` marker is allowed by design and was not counted as a defect.

## Summary

- Blocking findings under the override: 3 (B1, B2, B3), all IMPORTANT by the old label.
- Minor findings (notes only): 10 (M1 to M10), each marked `(minor under grading override)`.
- No synthesis file was modified; nothing was fabricated; no security, data-loss or safety-boundary item.
- B1 and B2 share one fix point (the axes table and adjudication table of synth-07); B3 is a status relabel in synth-06 with a matching wording change in synth-07.

**Verdict: FAIL** (3 blocking under the grading override).

**Status:** Complete
