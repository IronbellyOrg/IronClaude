# Round 1: Variant 2 advocate

Persona: QA. Focus: correctness, coverage and deviation classification.

Citation keys: V1, V2 and V3 mean `variant-1-original.md`, `variant-2-original.md` and `variant-3-original.md` in the parent adversarial directory. DIFF means `diff-analysis.md` there. TASK means `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` from the repository root. DESIGN means `docs/designs/orchestrator-mode.md`. Citations below identify those files and their line numbers.

## Position summary

V2 is strongest where a QA review must distinguish a bad product from a bad test. R2-G1 identifies an acceptance check that rejects correct delivery: TASK:1436 demands every class and constant name "appears once (`grep -c` per name)", while TASK:1433 requires fields referring to other model classes. DESIGN:454 and DESIGN:466 independently require those references. Counting matching lines is not counting definitions. The failure is deterministic, not a speculative runtime scenario.

That does not justify V2's original severity spread. The calibrated position is one HIGH, five MEDIUM and three LOW findings, not six HIGH findings. V2's strength is its grounded, testable evidence and recovery of overlooked obligations, not the number of alarms. The merge should retain the surviving HIGH, incorporate the other variants' distinct findings, and avoid claiming complete coverage from disjoint reviewer slices alone.

## Steelman

### V1

V1's strongest argument is execution-path completeness. Its R1-G1 and R1-G2 connect capture outcomes and owner decisions to later build gates, rather than treating a plan as a list of isolated sentences. The CLOSED path matters: TASK:1267 applies the DESIGN fallback only to STILL UNVERIFIED rows. DESIGN:971 sends a discovered JSON need to the owner, but TASK:1267's explicit branch covers only differing field names. V1 is stronger than V2 on that settled-fact path. Its mechanical capture-check concerns also survive calibration: the unwritten forbidden-list sentence and the echo/ls mismatch are confirmed in V1:280-285 and visible at TASK:1260-1262.

### V3

V3's strongest argument is that authorized changes still need internally consistent design text, records and tests. Its D10 and section-count analysis catches incomplete propagation rather than alleging that R5 lacks owner approval. The calibration confirms missing deviation references and stale-count grep misses in V3:418-423. V3 also finds a concrete mismatch between deleting a prohibition and requiring a positive permission hit, while its calibration narrows the claim to that surviving half (V3:433-435). These are useful checks that V2 did not provide.

## Strengths claimed

1. **A demonstrated false rejection.** R2-G1 survives HIGH calibration because the model check contradicts the required model relationships, not because a reviewer prefers another test style (V2:571-574). Its downstream risk is a stalled build or code distorted to satisfy a mistaken check. Checking declarations instead of references directly removes that failure.
2. **Tests matched to actual prohibitions.** DESIGN:211 forbids imports from `classify`, `report` and `click` into probes; DESIGN:219 says "no type is redeclared" from contracts. An import-absence check cannot detect a copied declaration. DESIGN:638 separately bans action controls, pasteable commands and task-deletion advice. R2-G4 distinguishes those obligations from lint or a limited word search. Calibration confirms missing checks, not demonstrated bad implementation (V2:583-586).
3. **Coverage beyond the existing matrix.** DESIGN:636 requires "Distinct affected sessions: <N> (set union, not a sum)" for every session count. R2-G6 finds that requirement outside the FR-011 ordering coverage, rather than assuming a broadly covered renderer row proves every renderer obligation. Calibration retains MEDIUM and explicitly notes likely delivery through the broad section reference (V2:591-594).
4. **Source obligations kept separate from behavior.** The builder-copy rule and proposed-limit marker remain actionable at MEDIUM, without claiming stale counts, a REPORT edit or a release failure has occurred (V2:575-582). This keeps documentary fidelity visible without inventing runtime defects.
5. **Auditable evidence.** V2 calibration reports 29 checked citations and zero failed citations (V2:543-545,558-562). That is stronger sampled grounding, not proof that every absence or every assigned row was verified. Its remediations name an item and a success condition; the remaining B5 method choice is acknowledged by calibration (V2:555-557).

## Weaknesses identified in the others

- **V1's breadth is not equally grounded throughout.** Its calibration finds 41 failed secondary row citations and four findings with empty evidence lists (V1:239-242,258-262). Its valid findings should be preserved, but the affected row references cannot serve as independent delivery evidence until corrected.
- **V1's late-decision claim must be dropped.** R1-G7 is refuted: the decision re-read and recovery gate exist (V1:286-288). Its live-state objection must also be narrowed to the missing timestamp-removal rule, because stopping on a difference follows the design (V1:274-276).
- **V3's inherited mappings are not an independent audit.** Its calibration says roughly 21 rows rely on the Tier-1 matrix and only three phase rows plus INV-005 were checked item by item (V3:389-394). The inferred tags are honest, but zero disagreement does not establish full confirmation.
- **V3 overstates parts of its propagation findings.** The historical D10 half of R3-G6 is weakened, and the R3-G8 remedy conflicts with an explicit instruction not to change other D6 cells (V3:433-441). The surviving permission-hit gap and record concern should not authorize an unapproved broader rewrite.
- **Neither absence of HIGH findings nor model/tool choice establishes quality.** V1 and V3 missed R2-G1, but their different assigned slices limit that comparison. Equally, V2's six original HIGH ratings were not evidence of six blocking failures.

## Concessions

- I accept all five HIGH downgrades: R2-G2, R2-G3, R2-G4 and R2-G5 become MEDIUM; R2-G7 becomes LOW. Only R2-G1 remains HIGH (V2:570-598). Missing constraints, markers and conditional branches are not the same as a check that inevitably rejects conforming code.
- I withdraw the unconditional INF-019 covered-in-substance conclusion. V2 correctly sees the STILL UNVERIFIED delegation, but a CLOSED discovery of a JSON need has no matching explicit branch. The combined reading in DIFF:81 is stronger than either card's blanket statement.
- I retain R2-G7 only as a limited fidelity concern. TASK:2471 rebases the count comparison when the recorded base differs and directs replacement of hits; TASK:2469 already checks named changed primitives. A same-count substitution outside that scope is conditional, not a demonstrated delivery hole. I have not independently proved the complete edited-file set, including the core CLAUDE source.
- R2-G6 establishes missing traceability and explicit verification, not proof that set-union wording will be absent from the delivered report. Broad design delegation could deliver it correctly (V2:591-594).
- R2-G8 establishes unclear actor identity, not a capture performed by an unauthorized actor. The non-test part is already present; actor equivalence remains inferred (V2:599-602).
- This debate reads the supplied cards and selected task/design passages. It does not re-run their whole-file searches, prove the union of assigned rows, run tests, inspect live Orca or change the audited implementation. Shared taxonomy and severity definitions remain unverified, so I do not relabel pre-execution gaps as observed regressions.

## Per-point positions

A variant named below includes its blind calibration. "None" means a tie, a rejected claim or an unresolved premise, not that the issue has no value. DIFF:21-30,40-64,72-84,90-106,114-145 provide the corresponding comparison evidence. Unique contributions and promoted assumption points are included to leave no listed point unanswered.

| id | superior variant or none | one-line reason |
|---|---|---|
| S-001 | None | Disjoint assigned slices are complementary, so row volume cannot decide superiority. |
| S-002 | V2, calibrated | One retained HIGH identifies a real blocking check; the original six-HIGH profile is rejected. |
| S-003 | V2 | Every finding supplies ref/quote pairs, avoiding empty evidence and reviewer notes presented as quotes. |
| S-004 | V2 | Task-item citations provide stronger independent grounding than failed secondary references or inherited mappings. |
| S-005 | V2 | Its 29 sampled citations all pass, but the 0.81 score remains sampled evidence, not universal validation. |
| S-006 | V2 | Explicit calibrated severities make the merge's weighting reproducible. |
| S-007 | None | Gap classes describe useful different dimensions but none proves compliance with the required common taxonomy. |
| S-008 | V3 | Its scale defines endpoints in words; V2's bare scale value is less clear. |
| S-009 | None | Model labels and codegraph usage do not establish correctness in a document audit. |
| S-010 | V2 | Auditing the matrix itself adds recall and link checks beyond confirming assigned Tier-1 findings. |
| C-001 | V2, calibrated | It specifies approved-set consistency or a halt, while retaining the no-cursor ten-template path at MEDIUM. |
| C-002 | V1, qualified | V1 catches the CLOSED JSON-need path; V2's delegation covers only the still-unverified path. |
| C-003 | V1 | It alone identifies the bad HALT pointer and weaker owner-evidence branches, with preamble mitigation retained. |
| C-004 | V1, narrowed | The timestamp-strip rule is missing, but the required stop on other differences is not a plan defect. |
| C-005 | V2 | Its explicit actor-traceability framing avoids claiming an unauthorized capture has occurred. |
| C-006 | V2 | It alone identifies the matrix's F11 versus F12 reference error. |
| C-007 | V1 | Both the unanchored username search and unwritten forbidden-list sentence survive calibration. |
| C-008 | V1, narrowed | The echo/ls mismatch is concrete; the extra agent-wait objection is unsupported. |
| C-009 | None | The late-decision claim is refuted and carries no finding weight. |
| C-010 | None | Both V1 and V3 overstate an ambiguity because the capture does call the otherwise unused forms. |
| C-011 | V2, calibrated | Count equality is not per-hit evidence, but LOW reflects scoped checks and the conditional outside-scope scenario. |
| C-012 | V2 | Declaration references necessarily repeat, so the occurrence check rejects conforming models. |
| C-013 | V2, calibrated | The builder-copy obligation is missing at MEDIUM, without evidence of a stale count or REPORT edit. |
| C-014 | V2, calibrated | It separates the immediate proposed-marker omission from the later rationale deadline. |
| C-015 | V2, calibrated | It names three unchecked invariants and explains why import absence cannot prove no copied types. |
| C-016 | V2 | Its recall pass finds session-count wording that an ordering-only renderer row cannot establish. |
| C-017 | V3 | It identifies incomplete D10 and history references; overlapping findings should be merged once. |
| C-018 | V3 | It shows exactly which stale-count spellings escape the grep and which zero-call pins are missing. |
| C-019 | V3 | Its section-location correction is specific and survives calibration. |
| C-020 | V3, qualified | Capture-first text remains inconsistent after an authorized change, not an unauthorized expansion. |
| C-021 | V3, narrowed | The missing positive 15.1 permission hit survives; the historical D10 failure claim is overstated. |
| C-022 | V3, narrowed | The record-completeness concern is useful, but the remedy must respect or explicitly revise 5.4's limit. |
| C-023 | V3 | It supplies the missing seam comparison without claiming that explicit new git requirements are absent. |
| C-024 | V3 | Four named helpers plus publication contradict the task's five-helper wording. |
| C-025 | V3, narrowed | Distinguishing live-capture fixtures from unit cases resolves an ambiguity, not a missing unit test. |
| X-001 | V1, qualified | The CLOSED-path routing defect survives V2's valid but incomplete unverified-path delegation. |
| X-002 | V1 | Its MEDIUM rating fits a conservative build or halt, and V2's calibration converges on it. |
| X-003 | None | V1 misses the base recount and V2 overstates an outside-scope substitution; retain only the LOW fidelity concern. |
| X-004 | V2, calibrated | Its explicit post-calibration profile preserves the real HIGH without inflating five lesser gaps. |
| X-005 | V1, qualified | Partial coverage is safer for the capture as a whole, while V2 remains right about one delegated path. |
| X-006 | V3, qualified | It catches stale extension-rule text; V1 and V2 still correctly identify owner authorization. |
| U-001 | V2 | Its sole retained HIGH is a deterministic false rejection with a bounded correction. |
| U-002 | V2 | The boundary, copied-type and renderer checks test obligations absent from the existing checks. |
| U-003 | V2 | Spec-body recall recovers a requirement that the parsed matrix misses. |
| U-004 | V2 | It catches an explicit task-builder instruction not copied into the executor's constraints. |
| U-005 | V2 | It preserves proposed-limit status and a release follow-up without alleging a present release breach. |
| U-006 | V2 | Correcting the F11/F12 link makes the actor finding traceable. |
| U-007 | V1 | Owner-evidence gates and their broken shared pointer deserve a separate fix from allowlist work. |
| U-008 | V1 | The capture actions and literal verification need to permit the same local commands and recorded text. |
| U-009 | V1, narrowed | A defined timestamp-removal rule is useful even though the difference-triggered halt follows design. |
| U-010 | None | Calibration refutes the late-decision claim, so uniqueness adds no weight. |
| U-011 | V3 | D10 and history omissions are one propagation defect, not two independent failures. |
| U-012 | V3, qualified | Authorized exceptions need consistent extension-rule wording, not an accusation of unauthorized scope. |
| U-013 | V3, narrowed | Removing a prohibition alone does not deliver the positive hit demanded by the next check. |
| U-014 | V3 | Stale diagram counts and missing zero-call assertions are concrete verification gaps. |
| U-015 | V3 | Naming the seam differences reduces copying risk, but the risk remains preventive. |
| U-016 | V3 | Correct helper enumeration prevents ambiguity without inventing another helper. |
| U-017 | V3, narrowed | Keep valid section and fixture clarifications, but do not apply the D6 remedy against 5.4 unchanged. |
| A-001 | V2, calibrated | The captured-cursor conflict is real, but generic QA may halt safely rather than ship wrong code. |
| A-002 | V2 | Treat unknown actor equivalence as a LOW traceability question, not proof of a forbidden actor. |
| A-003 | None | The assumption excludes the capture even though the task includes it in Phase 1. |
| A-004 | None | Baseline drift is mitigated and edited-file scope is not fully verified in this debate. |
| A-005 | V3, qualified | Authorization is shared evidence, but it does not silently repair capture-first design text. |
| A-006 | None | Adding slice sizes does not prove equality with the complete requirement-row set. |
| A-007 | None | Executability remains conditional on owner decisions, authorized capture access and check repairs. |
| A-008 | None | Different gap-class vocabularies cannot settle which formal taxonomy the review contract requires. |
| A-009 | V2, calibrated | Explicit per-finding calibration is the safest merge input while a common original HIGH rubric is unverified. |
| A-001c | V2, calibrated | Closing the cursor fact removes the rationale for the unknown-cursor fallback, leaving conditional count rework. |
| A-001d | None | A generic halt may catch failure, but does not supply an approved continuation branch. |
| A-002a | V2 | Role equivalence is unknown, so a stated capture actor is a preventive clarification. |
| A-003a | None | Phase 1 includes the live capture, so excluding it from the call count is not justified. |
| A-004a | None | Recounting at a changed base defeats the claimed fixed-baseline drift problem. |
| A-004b | None | Outside-scope primitive edits must be checked before asserting or dismissing the substitution scenario. |
| A-004c | None | The scope of every-hit justification needs an explicit disposition, not an inferred exemption. |
| A-006a | None | A row-ID union check is needed before any complete-coverage claim. |
| A-007b | None | No card establishes live access and permission, so no advocate should assume them. |
| A-008a / A-009a | None | Neither a shared classification obligation nor identical original severity definitions has been established. |

## Shared assumption responses

- **A-001: QUALIFY.** ACCEPT the possible captured cursor and unconditional ten-template pins. For A-001c, a CLOSED cursor fact reasonably ends the unknown-cursor fallback, making the requested extra template conflict real. REJECT A-001d as a necessary premise: generic QA may halt on a count failure, but that safe stop does not provide the missing approved branch. MEDIUM, not HIGH, fits this distinction (DIFF:81-82,114-117).
- **A-002: QUALIFY.** ACCEPT the value of naming the actor and that the non-test restriction is already met. For A-002a, do not assume the executor is either equivalent or unequal to the coordinator. The defect is unestablished role identity, not proven unauthorized execution (DIFF:118-119,140).
- **A-003: REJECT.** Phase 1 cannot be assumed to mean only the runtime sweep when the task also includes a capture that calls templates 7 and 8. The sentence is ambiguous and can be clarified; it is not established as false under every reading (DIFF:120).
- **A-004: QUALIFY.** REJECT baseline drift as the stated defect because the plan recounts at a changed base. A-004b remains unverified: the complete edited primitive set was not checked here. For A-004c, the literal every-hit rule favors an explicit per-hit or verified-baseline disposition, but this does not require treating all old hits as newly introduced defects. Keep the concern LOW and conditional (DIFF:83,121-123,141-142).
- **A-005: QUALIFY.** ACCEPT the supplied evidence of owner authorization. REJECT A-005b as a reason to leave contradictory design wording untouched. QUALIFY A-005c: non-use limits Phase 1 operational risk, but non-use alone does not prove the flags parse or that a capture-first rule is satisfied. Repair or explicitly authorize the textual exception rather than calling the scope unauthorized (DIFF:84,124-126).
- **A-006: REJECT as a proven coverage claim.** Arithmetic establishes 152 listed rows, not equality with the required row-ID set. For A-006a, require that union comparison before claiming completeness. Inherited Tier-1 mappings, including V3's disclosed inferred rows, remain leads rather than independent revalidation (DIFF:127-128,143).
- **A-007: QUALIFY.** ACCEPT the stated dependency on resolving owner decisions, not an assumption that resolution will occur. A-007b is unverified: live Orca access and permission are execution preconditions, not established facts from these cards. The moderate-rework grades are conditional on those preconditions and repairing the unsound checks (DIFF:129-130,144).
- **A-008: QUALIFY.** Gap classes are useful for pre-execution defects, and no completed-work regression has been shown. But A-008a does not establish an exemption from the required classification rubric. Preserve the descriptive gap classes and require an explicit contract decision before claiming formal four-category compliance (DIFF:131,145).
- **A-009: REJECT as established comparability.** A-009a is unverified because the shared HIGH definition is not supplied by the three cards, and V2 itself applied its stated bar inconsistently. Use the supplied calibrated severities and narrowed findings rather than comparing original severity totals as equivalent measurements (DIFF:132,145).

The next merge should preserve R2-G1's HIGH correction first, combine the surviving path and propagation findings, and keep coverage and rubric uncertainty explicit. No implementation or live checks were performed in this debate.
