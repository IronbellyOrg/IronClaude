# Round 2 rebuttal: Variant 2

Persona: QA. Variant 2 is reviewer 2, qa, haiku slot. This is the second sequential rebuttal, after Variant 1.

Citation keys: TASK means `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; DESIGN means `docs/designs/orchestrator-mode.md`. Debate and variant file names refer to this adversarial directory. Point ids retain their meanings in `diff-analysis.md`, not replacement meanings assigned in another statement. Changed positions are compared with `debate/round1-v2.md`.

## Response to criticisms

### Severity inflation and confidence

Concede all five downgrades, as in Round 1. R2-G2, R2-G3, R2-G4 and R2-G5 are MEDIUM; R2-G7 is at most LOW. R2-G1 alone remains HIGH. Missing checks and conditional routes do not automatically make correct delivery impossible. Neither the original six HIGH labels nor the self-rating of 0.90 should drive the merge. Use the calibrated 0.81 with its limitations: sampled citations passed, but whole-file absence claims and full assigned scope were not independently established by the calibrator.

Counter the claim that the largest confidence drop establishes the weakest card. It establishes the largest self-rating correction, not the lowest calibrated grounding. V2 still has the highest calibrated confidence, and both other advocates accept R2-G1 as the most important finding. Confidence scores remain supporting evidence, not finding truth.

### Missing Phase 7 checks and FR/NFR rows

Concede that V2 missed V1's HALT-pointer, capture-action and verification-text defects. Those are separate findings worth merging. V2 does not claim to have checked them merely because it reviewed nearby actor and allowlist obligations.

Counter treating the absence of FR/NFR row reviews as an assignment failure. The slices were disjoint. V1's larger assigned slice gives broader coverage, not an independent comparison of the same rows. V2's matrix audit and recall pass supplement that work. Neither slice breadth nor seven new findings versus three decides which specific claim is sound.

### R5 authorization accepted without a consistency audit

Concede. V2's GQ-109 verdict answered whether the owner authorized the change, but missed whether all dependent design text was updated. V3 is superior on that second question. The design-text inconsistency and incomplete D10/history record must be retained without calling the expansion unauthorized. The 15.1 positive-hit issue is also distinct from the overstated historical-D10 prohibition claim.

### Run-current delegation and CLOSED discoveries

Concede the unconditional coverage verdict. V2 is right only while the fact remains STILL UNVERIFIED. TASK:1267 delegates the behaviour-until-closed rule on that path and supplies only a field-name mismatch branch. A CLOSED finding that plain output cannot parse has no explicit owner route. TASK:1259 forbids trying the JSON form in the capture. V1 wins C-002, X-001 and X-005. The original INF-019 covered-in-substance verdict should become partial.

### Cursor outcome and the claim that QA may halt safely

Concede that no generic rule supplies the missing owner-approved continuation. TASK:1482 requires the captured cursor fact while TASK:1485 pins ten entries; TASK:1793 repeats that exact-set pin. V1's MEDIUM assessment is stronger than V2's original HIGH. A ten-template fallback is valid while the cursor is unknown, not proof that a captured-cursor conflict disappears.

Counter V1 Round 2's stronger claim that nothing can make the failure loud and a reviewer following the plan would pass it. TASK:1524 gives the safety reviewer both DESIGN sections 7.1 to 7.5 and the capture facts. TASK:1525 explicitly tells that reviewer not to trust the task file's claims. TASK:1588 contains real HALT outcomes for unresolved gate failures. That does not guarantee detection or create an owner branch, but it supports the modest claim that QA may stop the work. Conversely, the same safety lens explicitly demands the ten templates, so silent omission remains possible.

TASK:1796 says to fix a test-exposed code bug in code. It does not say that a disagreement between a captured design requirement and a fixed-count test is necessarily a code bug, or that a particular cursor template must be removed. V1 identifies a credible failure route, not a forced outcome. Keep MEDIUM, require an explicit approved-set/owner branch, and do not describe either safe stopping or silent omission as inevitable.

### Full-tree count, outside-scope substitution and per-hit disposition

Concede more precisely than Round 1. R2-G7's swap scenario is not established for the planned edits. TASK:2471 already recounts at the recorded base and directs replacement on a hit. V1 is right that this is an explicit remediation instruction. My demand for an explicit disposition was too broad.

TASK:2256 says the level table is untouched and its CLAUDE copy needs no re-run. This weakens the particular unscoped-file scenario but does not, by itself, prove that every possible file outside the scoped grep is untouched. No demonstrated concealment remains. Retain at most a LOW fidelity question: DESIGN:939 asks for every hit to be justified, while the completion gate at TASK:2472 records zero scoped hits and an unchanged total. Whether old hits also require fresh justification is still unresolved. Do not invent a current bad primitive to defend the finding.

### Best-practice grade 3 versus the others' grade 4

Concede that V2 does not justify the numerical distinction under a shared rubric. Its scale is only the number 5. The grade need not rise automatically because severities fell: the deterministic model-check defect and several untested invariants remain. But grade 3 cannot be defended as objectively better calibrated than grade 4 from these cards. Preserve the reasons, not a cross-card ranking based on those numbers. V3's written scale is clearer.

### Classification and limited verification

Concede V3 has the clearest descriptive separation between design fixes, check defects and reuse concerns. That is different from proving any card follows a common formal deviation taxonomy. This is a pre-execution review, not evidence that a delivered implementation has regressed. R2-G4 and R2-G6 remain missing-check or traceability findings, and R2-G8 remains an inferred actor-identity question, not a proven unauthorized capture.

## Updated assessment of V1 and V3

### V1

V1 remains strongest on the CLOSED capture paths, the HALT pointer and literal capture checks. Its Round 2 withdrawals improve the merge: the late-decision claim has no weight; the timestamp-removal instruction already exists, leaving only an optional field-definition clarification; and the Phase 1 count sentence does not establish a defect. Its original failed secondary references still cannot become independent design evidence merely because other task-item references survive.

V1's new cursor argument strengthens the need for a branch, but its guaranteed silent-omission conclusion goes beyond the written rules. Its coverage-union result is useful new reported evidence, not a check I independently performed. Its Round 2 positions table also changes the meanings of several ids. For example, its C-001 row discusses coverage breadth, whereas C-001 in diff-analysis is the cursor-template branch. The merge must use the original ids and the substantive response text, not copy that table mechanically.

### V3

V3 remains strongest on the authorized R5 change's incomplete record and inconsistent design text. I accept its closure of the D6 complaint as superseded by item 5.4, rather than retaining my Round 1 suggestion of a narrower new fix. Its honest inferred tags remain useful, but are not an independent audit of those rows. Codegraph use supports the particular seam comparison, not general superiority of the whole card. Its missing HIGH is not evidence that the underlying plan has no blocking check defect.

## New evidence

1. The safety gate supplies a concrete counterexample to guaranteed silent omission. TASK:1524 includes the design and capture facts among the review inputs; TASK:1525 rejects blind trust in the task's claims. It also pins ten templates, so it is a conflicted safety net, not a resolution. TASK:1588 shows how an unresolved gate finding can reach HALT. These lines preserve only the conditional statement that QA may stop the work.
2. The model defect needs no speculative runtime example. Re-read TASK:1433 requires ClassifiedRow fields referring to SessionRow, Classification and SafeToClose, while TASK:1436 demands each class name occur once by grep. R2-G1 remains HIGH. The fix must count declarations rather than all references.
3. Re-read TASK:1260 says to compare outputs with timestamps removed, and TASK:1262 says apart from timestamps. There is already a removal rule. C-004 should not retain a claim that the rule is absent; at most it is a LOW clarification of which fields to ignore.
4. Re-read TASK:163 includes the capture in Phase 1 and explicitly limits it to templates 1 to 8. The sentence does not establish the alleged C-010 defect. Both V1 and V3 count complaints should be closed, not preserved as findings merely because two cards raised them.
5. Re-read TASK:789 already cites the cadence evidence and forbids other D6-row changes. C-022 is superseded, not a separate fix request.
6. V1 reports a 152-id union with no missing, extra or overlapping ids in round2-v1's New evidence. I accept that as attributed evidence resolving the earlier arithmetic-only objection, without claiming I ran the script or inspected its deleted output. It settles represented row ids, not the truth of every verdict or spec completeness. V2's separate set-union wording recall finding illustrates that distinction.
7. Point identity must remain stable. V1's Round 2 S-002 discusses classification rather than the severity profile defined in diff-analysis, and C-023 discusses the D6 closure rather than the git seam. The table below keeps the original meanings. This is a merge-input correction, not a new defect in the audited plan.

## Updated per-point positions

A named variant includes its calibration and the qualifications above. None means no superior treatment, a rejected finding or an unresolved premise. Yes includes a changed substantive disposition even if the superior-variant cell is unchanged. Additional assumption subrows unpack the parent points; their Round 1 comparison uses the corresponding grouped response.

### Structural points

| id | superior variant or none | changed from Round 1? | reason |
|---|---|---|---|
| S-001 | none | no | Assigned slices complement each other; breadth is not same-row review quality. |
| S-002 | V2, calibrated | no | The retained HIGH identifies the deterministic bad check; the original six-HIGH profile is rejected. |
| S-003 | V2 | no | Ref/quote pairs on every finding remain easier to audit than empty lists or a note used as a quote. |
| S-004 | V2 | no | Direct task-item grounding is stronger than failed secondary citations or inherited row mappings. |
| S-005 | V2 | no | Highest calibrated confidence with no sampled citation failures, not universal verification. |
| S-006 | V2 | no | Per-finding calibrated severity is useful merge input, although it is a calibrator output rather than reviewer merit. |
| S-007 | V3 | yes | Its vocabulary more clearly separates design fixes and check defects; formal taxonomy compliance remains unresolved. |
| S-008 | V3 | no | Its written scale is clearer; V2 cannot defend its numerical grade against the others on a shared scale. |
| S-009 | none | no | Tool and model labels do not establish the truth of unrelated findings. |
| S-010 | none | yes | V3's new-findings count and V2's matrix audit are complementary contributions, not a quality ranking. |

### Content points

| id | superior variant or none | changed from Round 1? | reason |
|---|---|---|---|
| C-001 | V1 | yes | Its original MEDIUM cursor-branch finding is better calibrated; safe stop and silent omission are both conditional. |
| C-002 | V1 | no | The CLOSED JSON-need discovery has no owner branch; V2's delegation was only partial. |
| C-003 | V1 | no | The wrong HALT pointer and weaker owner-evidence branches survive, with the preamble mitigation. |
| C-004 | none | yes | Timestamp removal is already stated; retain at most a LOW field-definition clarification, not a missing rule. |
| C-005 | V2 | no | The inferred actor-identity framing avoids claiming a forbidden actor actually captured data. |
| C-006 | V2 | no | It uniquely identifies the F11 versus F12 matrix-reference error. |
| C-007 | V1 | no | Bare-name matching and the unwritten forbidden-list sentence remain real verification concerns. |
| C-008 | V1 | no | The echo/ls mismatch survives; the agent-wait extension does not. |
| C-009 | none | no | The late-decision claim is refuted and carries no weight. |
| C-010 | none | yes | Close both count complaints: Phase 1 includes the capture using templates 1 to 8. |
| C-011 | none | yes | No planned same-count substitution is demonstrated; only a conditional LOW fidelity question remains. |
| C-012 | V2 | no | Correct model relationships repeat names, so the occurrence check falsely rejects conforming delivery. |
| C-013 | V2, calibrated | no | The uncopied builder obligation is MEDIUM, not a demonstrated REPORT edit or delivery failure. |
| C-014 | V2, calibrated | no | Missing proposed status is MEDIUM; the rationale deadline is a separate release follow-up. |
| C-015 | V2, calibrated | no | Missing import-boundary, copied-type and renderer checks are MEDIUM, not proven implementation breaches. |
| C-016 | V2 | no | The recall pass finds untraced set-union wording; broad renderer delegation may still deliver it. |
| C-017 | V3 | no | D10 and history under-reporting are one propagation finding, not independent duplicate defects. |
| C-018 | V3 | no | It identifies stale-count spellings missed by the grep and missing zero-call pins. |
| C-019 | V3 | no | The section-location correction remains a specific LOW wording fix. |
| C-020 | V3, qualified | no | An authorized R5 change still needs consistent capture-first extension wording. |
| C-021 | V3, narrowed | no | Keep the missing positive 15.1 hit, not the overstated historical-D10 half. |
| C-022 | none | yes | Item 5.4 supersedes the complaint; do not apply a new D6 remedy contrary to its restriction. |
| C-023 | V3 | no | The reuse-seam comparison remains useful preventive guidance, not evidence of copied faulty code. |
| C-024 | V3 | no | Helper enumeration needs clarification, not an invented fifth helper. |
| C-025 | V3, narrowed | no | Distinguish capture fixtures from positive unit cases; no missing unit test is established. |

### Contradictions

| id | superior variant or none | changed from Round 1? | reason |
|---|---|---|---|
| X-001 | V1 | no | V2's unconditional coverage verdict is withdrawn; CLOSED and STILL UNVERIFIED paths differ. |
| X-002 | V1 | no | MEDIUM fits the conditional cursor conflict; neither recovery nor silent omission is guaranteed. |
| X-003 | none | no | Both original mechanisms overstate the planned scope; the base recount and replacement instruction exist. |
| X-004 | V2, calibrated | no | Its corrected profile keeps the real HIGH while removing five inflated labels. |
| X-005 | V1 | no | The capture as a whole is partial despite one delegated fallback path. |
| X-006 | V3, qualified | no | Authorization and inconsistent design text coexist; this is not unauthorized scope. |

### Shared assumptions and promoted points

| id | superior variant or none | changed from Round 1? | reason |
|---|---|---|---|
| A-001 | V1 | yes | Its MEDIUM path conflict is sound; the probability of safe stopping versus silent omission is unresolved. |
| A-001a | none | no | Accept the stated possibility of capturing a cursor field. |
| A-001b | none | no | Accept the unconditional ten-template pins. |
| A-001c | V2, calibrated | no | A known captured cursor is not the unknown-cursor fallback case. |
| A-001d | none | no | QA may stop the work but supplies no approved continuation; V1's guaranteed-silence reversal is too strong. |
| A-002 | V2 | no | Keep a LOW actor-identity clarification without alleging unauthorized execution. |
| A-002a | V2 | no | Coordinator equivalence is unknown, not shown false. |
| A-002b | none | no | The non-test restriction already exists. |
| A-003 | none | yes | Close the alleged count defect rather than retain it as ambiguous-but-actionable. |
| A-003a | none | yes | Reject excluding the capture from Phase 1; that cannot support either count complaint. |
| A-004 | none | yes | No substitution is demonstrated and replacement is an explicit disposition; only justification scope remains open. |
| A-004a | none | no | The changed-base recount defeats the fixed-baseline drift argument. |
| A-004b | none | no | The CLAUDE level-table statement weakens one scenario, not proof about all unscoped files; no actual swap is shown. |
| A-004c | none | yes | Withdraw the demand for a missing disposition; replacement already exists, while old-hit justification scope is unresolved. |
| A-005 | V3, qualified | no | Owner authorization does not silently update dependent extension-rule text. |
| A-005a | none | no | Accept the supplied resolved owner authorization; do not reopen it without evidence. |
| A-005b | V3 | no | Authorization is not a textual amendment to the unchanged capture-first rule. |
| A-005c | none | no | Non-use limits present operational exposure, not proof that every allowed flag parses. |
| A-006 | none | yes | Accept V1's reported row-id union result with attribution; row validity and omitted spec obligations remain separate. |
| A-006a | none | yes | V1 reports all 152 ids, disjoint, with no missing or extras; I did not independently rerun that check. |
| A-006b | none | no | Inferred Tier-1 mappings remain lower-weight evidence even when the union is complete. |
| A-007 | none | yes | Execution remains conditional, and V2 cannot defend grade 3 versus grade 4 on an unstated shared scale. |
| A-007a | none | no | Decision-dependent gates require decisions first; resolution is not assumed. |
| A-007b | none | no | Live access and permission are preconditions not established by these cards. |
| A-008 | none | no | Descriptive gap classes do not prove compliance with a common formal taxonomy. |
| A-008a | none | no | No completed-work regression is established; exemption from a formal rubric also remains unverified. |
| A-009 | V2, calibrated | no | Per-finding calibration is useful weighting input, not proof the original HIGH labels were comparable. |
| A-009a | none | no | Only V2 states a HIGH bar, and originally applied it inconsistently. |
| A-008a / A-009a | none | no | Keep both rubric uncertainties explicit rather than merge unlike original labels as a common measurement. |

The merge should correct R2-G1 first, combine V1's capture-path findings with V3's R5 propagation findings, and retain only the narrowed LOW fidelity and wording concerns. No implementation, tests, live Orca checks or independent coverage-union script were run for this rebuttal.
