# Diff Analysis: reflect-reviewer card Comparison (UC-1 pre-execution, run 2)

## Metadata
- Generated: 2026-11-08T13:30:00Z
- Variants compared: 3
  - Variant 1: reviewer 1, analyzer, sonnet slot (`variant-1-original.md`), 9 findings, 76 rows, calibrated confidence 0.71
  - Variant 2: reviewer 2, qa, haiku slot (`variant-2-original.md`), 9 findings, 44 rows, calibrated confidence 0.81
  - Variant 3: reviewer 3, refactorer, opus slot (`variant-3-original.md`), 11 findings, 32 rows, calibrated confidence 0.79
- Audit target: tasklist `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` against design `docs/designs/orchestrator-mode.md`
- Focus: correctness, coverage, deviation-classification
- Weighting rule (from each variant header): refuted findings carry no weight; weakened findings use calibrated_severity where given. Only Variant 2's calibration gives calibrated_severity; for Variants 1 and 3 a weakened finding keeps its card severity, noted as "weakened, no calibrated severity".
- Orchestrator-side evidence: where a contradiction is decided, the tasklist or design lines were re-read by this agent on 2026-11-08 and are quoted as "Orchestrator evidence".
- Taxonomy: L1 surface (wording, reference, presentation), L2 structural (organization, module, coverage layout), L3 state mechanics (guard, boundary, validation rule, invariant, state). Priority L3 > L2 > L1; default L2.
- Total differences found: 67
- Categories: structural (10), content (25), contradictions (6), unique (17), shared assumptions (9, with 8 promoted rows covering 9 UNSTATED preconditions)

## Structural Differences

| # | Area | Variant 1 (analyzer, sonnet) | Variant 2 (qa, haiku) | Variant 3 (refactorer, opus) | Severity | Level |
|---|------|------------------------------|-----------------------|------------------------------|----------|-------|
| S-001 | Row slice audited | 76 rows: FR-001 to FR-026, NFR-001 to NFR-015, 35 design steps 1.0a to 1.29 | 44 rows: 13 GQ, 9 D, 14 SP, 8 INF (INF-001, 005, 008, 017 to 020, 024) | 32 rows: R3-B1 to R3-B3, G-1, INV-005, INV-017, routing rows R1 to R8, 17 INF rows | Medium | L2 |
| S-002 | Finding count and severity profile | 9 findings: 0 HIGH, 3 MEDIUM, 6 LOW | 9 findings: 6 HIGH, 1 MEDIUM, 2 LOW | 11 findings: 0 HIGH, 3 MEDIUM, 8 LOW | Medium | L2 |
| S-003 | Evidence shape | List of ref and quote pairs; R1-G5, R1-G6, R1-G7, R1-G9 have empty evidence lists | List of ref and quote pairs on every finding, absolute paths | Single ref and quote map per finding (not a list); R3-G7 quote is a reviewer note, not file text | Low | L1 |
| S-004 | Row grounding | Every row tagged Grounded, but 41 second refs in design lines 444 to 484 fail (calibrator: likely SPEC line numbers under the design path) | Every row cites tasklist line ranges; only INF-017 tagged [INFERRED] | 21 of 32 rows cite only "T1 matrix row" and are tagged [INFERRED]; phase and INV-005 rows cite tasklist ranges | Medium | L2 |
| S-005 | Calibration outcome | Self 0.72, calibrated 0.71; 78 citations checked, 41 failed; 1 refuted, 3 weakened | Self 0.90, calibrated 0.81; 29 checked, 0 failed; 5 weakened (all severity cuts) | Self 0.75, calibrated 0.79; 36 checked, 0 failed; 4 weakened | Medium | L2 |
| S-006 | calibrated_severity field | Not given; verdicts only | Given for every finding | Not given; verdicts only | Low | L1 |
| S-007 | gap_class vocabulary | gate-bypass, unsound-check, traceability | unsound-check, missing, partial, traceability | design-fix, traceability, unsound-check, missing-reuse, test-plan | Medium | L2 |
| S-008 | best_practice_compliance scale | grade 4, scale "0-5" | grade 3, scale "5" | grade 4, scale described in words | Low | L1 |
| S-009 | Model labels and tooling | model_class claude-gw-tier1b vs slot sonnet; codegraph_used false; calibrated by opus | model_class claude-gw-tier2 vs slot haiku; codegraph_used false; calibrated by opus | model_class claude-gw-tier1a vs slot opus; codegraph_used true; calibrated by sonnet | Low | L2 |
| S-010 | Tier-1 relation coverage | Relates to F1, F3, F5, F12, F13; 4 new | Relates to F1, F2, F6, F9, F10, F12; 3 new; also audits the coverage matrix itself (R2-G6, R2-G9) | Relates to F4, F7, F8, F11; 7 new | Low | L2 |

Note on S-001: the three slices do not overlap on any row id. No row was audited by two reviewers, so agreement between cards can only come from findings, not from row verdicts.

## Content Differences

One row per distinct defect. Cell format: finding id, card severity, calibrated verdict (calibrated_severity if given). "Not raised" means the card has no finding or row on the topic. The Severity column is the weighted severity after calibration.

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|-------|-----------|-----------|-----------|----------|-------|
| C-001 | Cursor-template outcome of step 1.0a has no branch; 8.10 and 10.3 pin exactly ten templates | R1-G1, MEDIUM, confirmed; step-1.0a row partial | R2-G5, HIGH, weakened (MEDIUM); INF-020 partial | Not raised | Medium | L3 |
| C-002 | A run-current --json need found by step 1.0a has no route to the owner | Part of R1-G1, MEDIUM, confirmed | Says covered in substance (R2-G5 narrowing, INF-019 covered-in-substance, disagrees with T1) | Not raised | Medium | L3 |
| C-003 | Phase 7 preamble points HALT items at item 6.2, which has no HALT; Branch 2 of 7.15 and 14.7 does not require the owner's quoted words | R1-G2, MEDIUM, confirmed (calibrator: preamble at 1142 writes both branches itself, lowering impact) | Not raised | Not raised | Medium | L3 |
| C-004 | 7.16 before and after comparison: no timestamp-strip rule; live state fields may trip the HALT | R1-G3, MEDIUM, weakened (HALT matches design 875; only the strip rule gap stands; no calibrated severity) | Not raised | Not raised | Medium (weakened; scope narrowed to the strip rule) | L3 |
| C-005 | 7.16 does not name who runs the live capture (design 868: person or coordinator) | R1-G4, LOW, confirmed | R2-G8, LOW, confirmed (LOW); INF-017 partial | Not raised | Low | L2 |
| C-006 | Coverage matrix INF-017 points at T1 F11; the actor finding is F12 | Not raised | R2-G9, LOW, confirmed (LOW) | Not raised | Low | L1 |
| C-007 | 7.18 grep for "coder" is unanchored; 7.16 grep expects a forbidden-list sentence the Action never writes | R1-G5, LOW, confirmed | Not raised | Not raised | Low | L3 |
| C-008 | 7.16 Verification allows only templates or file reads, but Action step 6 runs echo and ls | R1-G6, LOW, confirmed (second sentence about agent-wait forms unsupported) | Not raised | Not raised | Low | L3 |
| C-009 | Late items (9.3, 14.8) do not re-read decision records | R1-G7, LOW, refuted (9.3 reads OQ-8 at 1640 and has a HALT at 1643) | Not raised | Not raised | None | L3 |
| C-010 | Key Constraints line 163 "eight called in Phase 1" | R1-G8, LOW, weakened (no calibrated severity) | Not raised | R3-G3, LOW, weakened | Low | L1 |
| C-011 | 14.5 uses an unchanged full-tree count of 168 instead of design 939 "every hit justified" | R1-G9, LOW, weakened | R2-G7, HIGH, weakened (LOW) | Not raised | Low | L3 |
| C-012 | 8.3 Verification counts name occurrences with grep -c, so a correct models.py fails | Not raised | R2-G1, HIGH, confirmed (HIGH) | Not raised | High | L3 |
| C-013 | Design 80 builder rule (cite GAPS line 138, never edit the REPORT) is not copied into the task | Not raised | R2-G2, HIGH, weakened (MEDIUM); GQ-111 to 113 partial; INF-001 missing | Not raised | Medium | L2 |
| C-014 | Byte limits are not marked "proposed" in probes.py (design 987, open item 19) | Not raised | R2-G3, HIGH, weakened (MEDIUM); SP-28 partial; INF-024 missing | Not raised | Medium | L2 |
| C-015 | Unchecked invariants: probes.py import boundary (design 211), B5 no redeclared contract types (219), renderer bans (638) | Not raised | R2-G4, HIGH, weakened (MEDIUM); INF-005 partial, INF-008 missing, INF-018 partial | Not raised | Medium | L3 |
| C-016 | Session-count set-union wording (design 636) is not traced to any row or test | Not raised (V1 FR-011 row covered on order and sort only) | R2-G6, MEDIUM, confirmed (MEDIUM) | Not raised | Medium | L2 |
| C-017 | D10 deviation row and R5 history section list written by 6.3 under-report the SPEC departure | Not raised | Not raised | R3-G1, MEDIUM, confirmed; R3-G7, LOW, confirmed (overlaps R3-G1) | Medium | L2 |
| C-018 | 6.3 step (8) grep misses design lines 181 and 196 (old count of 8); no zero-argv pin for templates 9 and 10 | Not raised | Not raised | R3-G2, LOW, confirmed | Low | L3 |
| C-019 | 5.11 row says draft-name markers are in sections 13 and 14; both hits are in 13 | Not raised | Not raised | R3-G4, LOW, confirmed | Low | L1 |
| C-020 | Templates 9 and 10 are added without a capture, against the design 221 extension rule | Not raised as a gap (best practice "+ The R5 decision flows through 6.1 to 6.4 ...") | Not raised as a gap (GQ-109 covered: authorized change) | R3-G5, MEDIUM, confirmed (calibrator: MEDIUM arguable) | Medium | L3 |
| C-021 | 6.3 and 6.4 agent-wait checks trip on quoted history and need a 15.1 "allows" hit that step (4) may not write | Not raised | Not raised | R3-G6, MEDIUM, weakened (15.1 half holds; D10 half overstated) | Medium (weakened; scope narrowed to the 15.1 half) | L3 |
| C-022 | D6 record does not cite the SPEC cadence lines or name R4 | Not raised | Not raised | R3-G8, LOW, weakened (5.4 already cites 415 and 583 and forbids other edits) | Low | L2 |
| C-023 | 8.5 does not cite the reflect `_git` seam (config.py:64-78) or list its differences | Not raised | Not raised | R3-G9, LOW, confirmed | Low | L2 |
| C-024 | 9.1 says "five helpers"; design 7.1 lists four plus `_publish` | Not raised | Not raised | R3-G10, LOW, confirmed | Low | L1 |
| C-025 | OQ-16 says no fixture covers templates 9 and 10; 10.3 has a positive unit case | Not raised | Not raised | R3-G11, LOW, weakened | Low | L1 |

Orchestrator evidence for C-012: tasklist line 1436 reads "every class and constant name in DESIGN section 7.2 appears once (`grep -c` per name)", and line 1433 dictates `ClassifiedRow` fields `row: SessionRow`, `classification: Classification` and `safe: SafeToClose`, so those names occur on more than one line in a correct file. The finding holds.

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact | Level |
|---|-------------------|--------------------|--------------------|--------------------|--------|-------|
| X-001 | Does item 7.17 route a run-current --json need to the owner? | R1-G1: "neither outcome has a route to the owner" | R2-G5: "its run-current concern is covered in substance by item 7.17's explicit application of the DESIGN behaviour-until-closed rule to open item 3; that delegation includes the owner-note requirement" | Silent | Medium | L3 |
| X-002 | Severity of the cursor-template gap | R1-G1 MEDIUM: "this is a likely case and not a remote one" | R2-G5 HIGH; calibrator cut to MEDIUM: "the likely outcome is a safe conservative build or a halt, not a broken delivery" | Silent | Medium | L3 |
| X-003 | What is wrong with the 14.5 full-tree count, and how bad | R1-G9 LOW: "fails after any unrelated change on the base, and it drops the justification step" | R2-G7 HIGH: "Equal counts can conceal a removed acceptable hit and a new unacceptable hit elsewhere" | Silent | Low | L3 |
| X-004 | How HIGH is applied | 0 HIGH; risk framed by blast radius on FR-002, FR-026, NFR-003 | 6 HIGH, while R2-G1 states the bar "HIGH ... because correct delivery cannot satisfy the check"; calibrator: "only R2-G1 meets" it | 0 HIGH; calibrator notes "no HIGH findings" as a risk-coverage gap | Medium | L2 |
| X-005 | Direction of disagreement with T1 on step 1.0a | step-1.0a row partial, agrees_with_t1 false (plan weaker than T1 said); R1-G1 "confirms F1" | INF-019 covered-in-substance, agrees_with_t1 false (plan stronger than T1 said); R2-G5 "refines F1" and narrows it | Silent | Medium | L3 |
| X-006 | Are templates 9 and 10 soundly added? | Treats R5 as a strength: "a recorded owner decision with a pre-flight check" | GQ-109 covered: "the task applies that authorized change" | R3-G5: "After Phase 6, the design breaks its own extension rule, and no evidence shows that template 10 parses"; yet its own best-practice line says "No unauthorized scope creep was found" | Medium | L3 |

Orchestrator evidence:

- X-001. Tasklist line 1267 (7.17 Action) writes each open item as "CLOSED with the fact ... or STILL UNVERIFIED (the DESIGN "behaviour until closed" applies)", and its only Branch is a live field name that differs from DESIGN 7.2 or 7.3. Design line 971 (open item 3) gives the behaviour until closed as "a `--json` need goes to the owner as an allowlist change". Design line 550 says "If the step 1.0a capture shows it needs `--json` for a parseable result, that is a template change and needs the same owner note". Tasklist line 1259 forbids running `run-current --json` in the capture. Reading: Variant 2 is right only for the path where item 3 stays STILL UNVERIFIED. If the capture settles item 3 (plain output does not parse), the row is CLOSED, the behaviour-until-closed delegation no longer applies, and no 7.17 Branch sends it to the owner. Variant 1's claim holds for that path. Both are partly right; the route exists only by delegation and only on the unverified path.
- X-002. Design line 973 (open item 5, behaviour until closed): "A full page of `WORKER_LIST_PAGE` rows sets truncated and the total is a lower bound; no cursor template". Design line 552: the cursor template "is added only after step 1.0a captures the cursor field, as one extra template". Tasklist line 1485 requires "a count of `ALLOWED_ORCA` entries is 10" and line 1793 pins "the ten templates". Reading: the fallback covers the uncaptured case; when the capture finds a cursor field, the design wants an eleventh template and the plan's two pins forbid it. The likely effect is a failed check or a stall, not wrong code shipped, so MEDIUM (Variant 1 and the Variant 2 calibration) is supported over HIGH.
- X-003. Tasklist line 2471: "If item 1.3 recorded a base other than `5dc29d23`, re-run the full count at that base reading only ... and compare against that number instead. On a hit, replace it with the installed `~/.claude/...` path". Line 2469 scopes the zero-hit grep to `sweep.md`, `sc-sweep-protocol/`, `WORKER-CONTRACT.md`, both `HOW-WE-WORK.md` copies. Reading: Variant 1's "fails after any unrelated change on the base" is contradicted by the base recount. Variant 2's concealment case needs an edit to a primitive outside the scoped list, which the plan does not make (not checked for every file, see A-004). Both overstate; LOW stands.
- X-006. Design line 221: "a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)". Tasklist line 998 (6.3 Action) adds the two `--agent-wait` templates with the comment "not called in Phase 1" and does not list line 221 among its edits; line 1259 says the flag "is allowed by R5 but is not run in step 1.0a". Reading: authorization (Variants 1 and 2) and the literal extension-rule breach (Variant 3) are both true. The defect is a design-text inconsistency left by 6.3, not unauthorized scope.

## Unique Contributions

| # | Variant | Contribution | Value Assessment | Level |
|---|---------|--------------|------------------|-------|
| U-001 | Variant 2 | R2-G1: the 8.3 grep -c check rejects a correct models.py. Only finding of the run that keeps HIGH after calibration; orchestrator-verified (C-012). Fix is one line | High | L3 |
| U-002 | Variant 2 | R2-G4: three design invariants (probes.py import row, B5, renderer bans) have no check; also shows the T1 F10 import-absence fix would not prove B5 | Medium | L3 |
| U-003 | Variant 2 | R2-G6: a spec-body recall pass beyond the parsed matrix, finding the set-union wording at design 636 with no row | Medium | L2 |
| U-004 | Variant 2 | R2-G2: the design 80 builder obligation is not copied into Key Constraints | Medium | L2 |
| U-005 | Variant 2 | R2-G3: byte limits lack the "proposed" marking and open item 19 has no closing disposition | Medium | L2 |
| U-006 | Variant 2 | R2-G9: matrix INF-017 cites F11 instead of F12 | Low | L1 |
| U-007 | Variant 1 | R1-G2: the Phase 7 HALT pointer to item 6.2 resolves to an item with no HALT; Branch 2 in 7.15 and 14.7 is weaker than the OQ-1 standard | Medium | L3 |
| U-008 | Variant 1 | R1-G5 and R1-G6: two 7.16 and 7.18 check lines that a literal executor cannot pass (unanchored "coder", unwritten forbidden-list sentence, echo and ls not allowed) | Medium | L3 |
| U-009 | Variant 1 | R1-G3: no timestamp-strip rule for the before and after comparison | Low | L3 |
| U-010 | Variant 1 | R1-G7: late items do not re-read decisions. Refuted by calibration; carries no weight | Low | L3 |
| U-011 | Variant 3 | R3-G1 and R3-G7: the D10 row and the R5 history line under-report SPEC lines and sections 2.2 and 12 | Medium | L2 |
| U-012 | Variant 3 | R3-G5: the design 221 capture-first extension rule is left unchanged while 6.3 adds two uncaptured templates (X-006) | Medium | L3 |
| U-013 | Variant 3 | R3-G6: the 6.4 pass rule needs a 15.1 hit that allows the flag, and 6.3 step (4) only deletes text | Medium | L3 |
| U-014 | Variant 3 | R3-G2: design lines 181 and 196 keep the count of 8 and escape the 6.3 grep; no zero-argv pin for templates 9 and 10 | Medium | L3 |
| U-015 | Variant 3 | R3-G9: the 8.5 `_git` seam does not cite the reflect helper or state its differences (check=True risk) | Low | L2 |
| U-016 | Variant 3 | R3-G10: "five helpers" in 9.1 against four in design 7.1 | Low | L1 |
| U-017 | Variant 3 | R3-G4, R3-G8, R3-G11: record-wording fixes (5.11 sections, D6 cells, OQ-16). R3-G8's remedy conflicts with item 5.4 | Low | L1 |

## Shared Assumptions

Agreement points, their preconditions, and classification. UNSTATED preconditions are promoted below as [SHARED-ASSUMPTION] diff points.

| # | Agreement point (variants) | Precondition | Class | Level |
|---|----------------------------|--------------|-------|-------|
| A-001 | Cursor-template outcome is unrouted (V1, V2) | a. Step 1.0a can capture a cursor field (design 552; tasklist 1267 "cursor field (`page.nextCursor` or other)") | STATED | L3 |
| | | b. The ten-template pins in 8.10 and 10.3 are unconditional (tasklist 1485, 1793) | STATED | |
| | | c. The design 973 no-cursor fallback stops applying once item 5 is CLOSED with a cursor field | UNSTATED | |
| | | d. No general QA or HALT rule would stop the executor on its own when the count check fails | UNSTATED | |
| A-002 | 7.16 should name the capture actor (V1, V2) | a. The executing agent may not be the coordinator named by design 868 | UNSTATED (both tag it [INFERRED]) | L2 |
| | | b. The "never by a test" half of the rule is already met (tasklist 163) | STATED | |
| A-003 | Line 163 "eight called in Phase 1" is wrong (V1, V3) | a. "Phase 1" means Phase 1 code only, not the step 1.0a capture | CONTRADICTED: tasklist 1257 and 1258 list templates 7 and 8 in the capture, and line 163 itself says "step 1.0a uses only templates 1 to 8" | L1 |
| A-004 | 14.5 is weaker than design 939 (V1, V2) | a. The 168 baseline can drift for reasons outside the task | CONTRADICTED: tasklist 2471 recounts at the recorded base | L3 |
| | | b. The task edits no primitive outside the scoped list at line 2469 | UNSTATED (V2 calibrator did not check `src/superclaude/core/CLAUDE.md`) | |
| | | c. "Every hit justified" in design 939 covers pre-existing hits, not only new ones | UNSTATED | |
| A-005 | R5 owner decision legitimately authorizes templates 9 and 10 (V1, V2, V3) | a. The OQ-1 record is RESOLVED with the owner's words ("Allow it, no conditions needed.") | STATED (V2 GQ-109 cites the decision file; V3 quotes it) | L3 |
| | | b. An owner decision overrides the design 221 capture-first rule without editing it | CONTRADICTED by V3 R3-G5 and by design 221 as it stands (X-006) | |
| | | c. Templates 9 and 10 need no parse evidence because Phase 1 never calls them | STATED (tasklist 998 comment, 1259) | |
| A-006 | The three row slices together cover the whole matrix (V1, V2, V3) | a. 76 + 44 + 32 = 152 rows is the full assigned set with no row left out | UNSTATED (no card cross-references another slice; V2 calibrator could not confirm its 44) | L2 |
| | | b. The T1 item mapping is reliable for the 21 V3 rows not re-read | STATED as an assumption by V3 ([INFERRED]), not verified | |
| A-007 | The plan is executable with moderate rework, grades 4, 3, 4 (V1, V2, V3) | a. PENDING owner decisions are resolved before the gates that need them (tasklist 1142) | STATED | L3 |
| | | b. The executing agent has live Orca access and permission to run the 7.16 capture | UNSTATED | |
| A-008 | Each card uses its own gap_class set instead of Aligned, Refinement, Drift, Regression (V1, V2, V3) | a. A UC-1 pre-execution card is not bound to the four-category UC-2 deviation taxonomy | UNSTATED (calibrators for V1 and V3 mark the absence against the rubric) | L2 |
| A-009 | Severity labels are comparable across cards (V1, V2, V3) | a. All three briefs define HIGH the same way | UNSTATED (only V2 states a bar, and applies it to 1 of its 6 HIGHs, X-004) | L2 |

### Promoted [SHARED-ASSUMPTION] diff points

| # | Source | Diff point | Level |
|---|--------|-----------|-------|
| A-001c | A-001 | [SHARED-ASSUMPTION] Whether the no-cursor fallback ends when item 5 closes decides if C-001 is a real gap or a non-event | L3 |
| A-001d | A-001 | [SHARED-ASSUMPTION] Whether a generic HALT or QA rule already catches a failed count check decides if C-001 needs its own branch | L3 |
| A-002a | A-002 | [SHARED-ASSUMPTION] Whether the executor counts as the coordinator decides if C-005 is a gap at all | L2 |
| A-004b | A-004 | [SHARED-ASSUMPTION] Whether the task edits any primitive outside the scoped grep decides if X-003's concealment case can happen | L3 |
| A-004c | A-004 | [SHARED-ASSUMPTION] Whether design 939 requires justifying the 168 pre-existing hits decides if 14.5 is a Refinement or a gap | L3 |
| A-006a | A-006 | [SHARED-ASSUMPTION] The disjoint slices may leave rows unaudited; the merge cannot claim full coverage without a union check | L2 |
| A-007b | A-007 | [SHARED-ASSUMPTION] Live Orca access for 7.16 is assumed; without it every step 1.0a dependent (7.17, 8.10, 9.1, 10.3) stalls | L3 |
| A-008a / A-009a | A-008, A-009 | [SHARED-ASSUMPTION] Cards were graded against a classification and severity rubric none of them states, so classification-clarity scores and severity merges rest on an unchecked common scale | L2 |

## Summary
- Total structural differences: 10 (Medium 5, Low 5)
- Total content differences: 25 (High 1, Medium 11, Low 12, None 1)
- Total contradictions: 6 (Medium 5, Low 1)
- Total unique contributions: 17 (High 1, Medium 10, Low 6)
- Total shared assumptions: 9 agreement points; 8 promoted [SHARED-ASSUMPTION] rows covering 9 UNSTATED preconditions; 3 preconditions CONTRADICTED (A-003a, A-004a, A-005b)
- Taxonomy spread over all 67 points: L1 12, L2 24, L3 31
- Highest-severity items: C-012 and U-001 (High, the 8.3 grep -c check, R2-G1). Next tier: C-001, C-002, C-015, C-020 and contradictions X-001, X-002, X-005, X-006 (Medium, all on the step 1.0a and R5 allowlist mechanics).
- Calibration effect: 6 HIGH findings entered (all from Variant 2); 1 survived. One finding refuted (R1-G7, C-009). The only topics raised by two cards are C-001, C-005, C-010 and C-011; no topic is raised by all three.
- Debate focus suggested by this analysis: X-001 (route for a captured run-current --json need), X-006 with A-005b (owner decision versus design 221), and A-006a (whether the disjoint slices leave rows unaudited).
