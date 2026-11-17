# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 (invariant probe)
- Convergence achieved: 100% on per-point winners (12 of 12); one grade dispute (C-004) settled by the judge
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2 (variant 1: opus class; variant 2: haiku class). Judge and scorers: sonnet class. Fault-finder: opus class.
- Taxonomy coverage: L1 (S-001, C-009), L2 (C-001 to C-004, C-008), L3 (C-005 to C-007, A-001, A-002) all covered
- Invariant probe: 20 entries; HIGH and UNADDRESSED: 5 (INV-001, INV-002, INV-004, INV-005, INV-006); these block convergence and are carried into the merged card as findings, not accepted as risk

## Round 1: Advocate Statements

### Variant 1 Advocate (opus class)

#### Round 1: Advocate for Variant 1 (reviewer-1 card, analyzer, haiku class)

##### Position summary

Variant 1 is the more precise card: every one of its four findings re-verifies against the live files, and two of them (C-003, the analysis template asked to carry a digest and a `v2` row that does not exist; C-004, a promised stage 2 evaluation with no task) are real defects that Variant 2 missed. Variant 1 is not the more complete card: it misses Variant 2's two highest-severity findings (C-005, C-006), so the merged card must keep both variants' unique findings, with Variant 1's two unique findings kept intact.

##### Steelman

The strongest case for Variant 2: it found the one defect that defeats the plan's whole safety design. The plan is a managed `workflow-plan/1.2` file (PLAN:2), `/sc:implement` has no per-phase option (src/superclaude/skills/sc-implement-protocol/SKILL.md:56), treats `## Phase N` only as a group heading (SKILL.md:87), and refuses a plan edited after the first task starts (`E-PLAN-CHANGED`, SKILL.md:46). So the sentence "Run `/sc:implement` on one phase at a time and stop at each gate" (PLAN:20) is not enforceable by the executor, and no task carries an acceptance line requiring a recorded owner go (Task 11 depends only on Task 10, PLAN:139). Add C-006 (Task 31, the seeded-recall run, is the first task inside the phase whose entry it is supposed to gate; Task 33 depends on it finishing, not passing, PLAN:374-394) and Variant 2 shows that `pragmatic.md` can move to digest v2 with no owner go and no recall pass. That is a safety-relevant result, it is correct, and Variant 1 has nothing equivalent. Variant 2 also verified C-008 against a real line (src/superclaude/commands/spec-panel.md:220 is the only `src/superclaude` path among all 13 registered carrier files; I re-counted with `grep -c`), and its Checked section records far more verified anchors than Variant 1's.

##### Strengths claimed

L2 structural:

1. C-003 (V1 F2) is real and verified. Task 41 lists `documents/agent_template_analysis.md` among the five templates and says "Each gets the digest and pointer ... update their registry rows to `v2`" (PLAN:490). The acceptance lines make it unavoidable: "Each of the five template files holds exactly one digest" (PLAN:493) and "Their registry rows say `v2` and T1 passes for them" (PLAN:494). But Task 16's 11 `digest` rows (PLAN:199) do not include that template, and the live file holds no definition sentence at all, only the merge line (src/superclaude/templates/documents/agent_template_analysis.md:466 "take the more severe rating for shared items"; a case-insensitive grep for "Grade every review finding" finds nothing). So line 494 names a row that does not exist, and a digest fence placed there without a row trips T2's "fence opener and has no registry row" scan (PLAN:303), which Task 46 makes strict (PLAN:546). Whether this file becomes a 12th carrier or gets only the merge text is a choice the plan does not make. Variant 2's Checked bullet "Exactly 11 files hold the definition sentence" is true but never reached Task 41's acceptance lines.
2. C-004 (V1 F3) is real and verified. Task 6 promises "the second evaluation of the classifier on this population ... is run at stage 2, not here" (PLAN:93). A search of the plan for `fresh-findings` / `fresh findings` hits only PLAN:76, 83, 87, 90 and 128, all in Phase 1. No Phase 3 task (Tasks 26-30, PLAN:312-368) consumes `./artifacts/fresh-findings.md`, records judge answers on it, or writes an evaluation result. The reconciliation requires this population be tested apart from the 318 rows (source.md:16 "the fresh-findings set the reconciliation requires"); without a consuming task the population is built and never used, and the plan's own acceptance line states a promise no task keeps. Variant 2's Checked bullet "Fresh findings held out of the split: Tasks 5 and 6" checked that the population exists, not that anything consumes it.
3. C-001 (V1 F1) is stated as one clean, single-cause finding: Task 40's allow-list includes "`refs/rule.md` and its plugin mirror path" (PLAN:477), a test "fails when a file named there does not exist" (PLAN:482), and the mirror is only created by Task 46 (PLAN:546). V1 correctly frames the fix as a decision (how to stage the entry "without weakening the missing-file check").

L1 surface:

4. Precision. All four V1 findings re-verify with the cited lines, none needs a correction, and every one is a plan defect, not a comment on the review run's own inputs. V1's Checked section also states plainly that no command or test was run (V1 line 26), so it claims no more than it checked.

L3 mechanics:

5. C-002 (V1 F4) is graded MINOR with the reason stated ("mechanical sequencing with clear intent"), which is exactly how A-002 defines minor.

##### Weaknesses identified in the opponent

1. V2 F3 bundles two unrelated defects into one finding (C-001, the missing plugin mirror; C-007, the scale-map self-trip). They have different causes and different fixes, so a fixer working from one finding id can close one half and leave the other open. V1 states C-001 on its own.
2. C-007 (first half of V2 F3) is real but overstated as "unpassable". Task 13 asks for a section that "names the files allowed to contain the phrases `highest severity`, `more severe rating` or `higher severity`" (PLAN:164), and its acceptance line only requires the section to list the auggie file, `refs/rule.md` and the six stage 4 files (PLAN:170); it does not require the three phrases to appear literally. An executor who writes the section naturally will trip Task 40's scan (PLAN:477 covers `src/superclaude/skills`), so the trap is real, but an executor can pass by naming the phrases indirectly. The plan's author already handled the identical self-trip for `refs/rule.md` (PLAN:152 "the file contains that phrase and the merge-rule scan allow-lists it"), so intent is clear. Under A-002 this leans minor or Medium, not blocking.
3. C-009 (V2 F6) is not a plan finding. The "coverage matrix" it criticises is the review run's own artifact, `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/artifacts/coverage-matrix.yaml`; the plan folder holds only `source.md`, the plan and `artifacts/codegraph-grounding.md`, and the plan has no matrix. V2 itself says "The plan covers all of them". The finding also undercounts: matrix rows at coverage-matrix.yaml lines 6, 14, 49 and 155 also have `matched_task_ids: []`, beyond the four ids V2 names.
4. V2 F1 quotes "Do not STOP. Do not split." (SKILL.md:72) as a general rule; that sentence is the N≥20 compaction notice ("If N≥20 print **once** ... Do not STOP. Do not split."), not a statement about phase gates. The conclusion of F1 still stands on SKILL.md:46, :56 and :87, so this is a citation-precision issue, not a false finding.
5. V2's coverage misses C-003 and C-004 although its Checked section touched both areas ("Exactly 11 files hold the definition sentence"; "Fresh findings held out of the split: Tasks 5 and 6"). Its claim "Every change the request lists has a task" stays narrowly true (source.md:16 asks only to build and score the set), but it did not test whether the plan keeps its own Task 6 promise.

##### Concessions

1. V1 missed C-005 and C-006, the two highest-severity findings in either card. Both are real (verified above in the Steelman) and V1 has no finding covering the owner-gate mechanism at all. This is V1's largest gap.
2. V1 missed C-008 (verified: src/superclaude/commands/spec-panel.md:220 holds `src/superclaude/examples/release-spec-template.md`; PLAN:303 checks `pointer-only` rows by T3, which fails on any `src/superclaude` path; no later task edits line 220) and C-007.
3. V1 F2's phrase "contradicts the required count of exactly 11" is overstated. "Exactly 11 rows of kind `digest`" is Task 16's acceptance line (PLAN:203), checked when Task 16 finishes; no later test cited in the plan pins the count at 11. The defect stands on PLAN:493-494 and the T2 reverse scan, not on the count.
4. V1 F1 states only one horn of C-001. V2 adds the other horn: leaving the mirror off the allow-list fails the scan after Task 46 copies `rule.md` into `plugins/superclaude`, which the scan covers (PLAN:477). V2's framing shows more clearly why the fix needs a decision.
5. V1's Checked section is thin (4 bullets, one of them a disclaimer) and V1's card was reassembled from two truncated messages (V1 line 5), so its record of what was verified is weaker than V2's.
6. C-004's blocking grade is arguable: the classifier has no authority in version 1 (OD4, PLAN:21) and the Phase 4 entry conditions (PLAN:20) do not list the fresh evaluation, so the missing task changes no gate outcome. I hold it blocking because the plan's own acceptance line promises a result no task produces and the reconciliation requires that population be tested (a missing required deliverable), but a judge could fairly grade it Medium.

##### Shared assumptions (A-001, A-002)

A-001: ACCEPT. The plan is a managed `workflow-plan/1.2` file (PLAN:2); `/sc:implement` enumerates `## Task N` headings and ignores `## Phase N` as a task (SKILL.md:87), offers no phase option (SKILL.md:56) and fails with `E-PLAN-CHANGED` on a plan edited after the first task starts (SKILL.md:46). So treating acceptance checks literally and the plan as one run is the correct model. One qualification: a human operator can still interrupt a run and resume it later (resume continues from the first unfinished task), so the gates are enforceable by hand but not by the executor. That does not rescue the plan, and accepting A-001 means V1 should have raised C-005 itself.

A-002: QUALIFY. The rule is stated in the brief and both cards apply it identically on C-002 (both MINOR). It is not applied evenly elsewhere: V2 grades C-007 blocking although a fix needing no decision exists (name the phrases indirectly; PLAN:170 does not require them literally), and V1 grades C-004 blocking although its consequence changes no gate outcome under OD4. Both edge cases should be re-graded by the stated rule, not by the label each reviewer chose.

##### Per-point table

POINT S-001 | winner: V2 | confidence: 60% | V2 covers more ground and records more verified anchors in Checked (7 bullets vs 4), though V1's four findings are all clean and none needs correction.
POINT C-001 | winner: both | confidence: 70% | Both cite PLAN:477, :482 and :546 correctly; V2 adds the second horn (leaving the mirror off fails after Task 46), V1 states the defect as one clean finding while V2 bundles it with C-007.
POINT C-002 | winner: both | confidence: 90% | Both grade the Task 46 copy-then-edit order (PLAN:546) MINOR with the same mechanical fix.
POINT C-003 | winner: V1 | confidence: 85% | PLAN:493-494 require a digest and a `v2` row in `agent_template_analysis.md`, which has no registry row (PLAN:199) and no definition sentence (its only match is the merge line at :466); V2 missed it.
POINT C-004 | winner: V1 | confidence: 75% | PLAN:93 promises a stage 2 evaluation on the fresh-findings population and no task after Phase 1 names `fresh-findings` (plan hits only at :76, :83, :87, :90, :128); blocking grade is arguable because OD4 gives the classifier no authority.
POINT C-005 | winner: V2 | confidence: 90% | sc-implement SKILL.md:46, :56 and :87 confirm `/sc:implement` cannot run one phase or tolerate a split plan, so PLAN:20's "stop at each gate" has no mechanical enforcement; V1 missed it.
POINT C-006 | winner: V2 | confidence: 85% | Task 31 is inside Phase 4 (PLAN:372-376) yet its result is a Phase 4 entry condition (PLAN:20), and Task 33 depends on Task 31 finishing, not passing (PLAN:394); V1 missed it.
POINT C-007 | winner: V2 | confidence: 60% | The scale-map self-trip is real (PLAN:164 vs PLAN:477), but PLAN:170 does not require the phrases literally, so "unpassable" is overstated and the grade leans Medium.
POINT C-008 | winner: V2 | confidence: 80% | src/superclaude/commands/spec-panel.md:220 is the only `src/superclaude` path among the 13 registered carriers (grep -c), and PLAN:303 checks `pointer-only` rows by T3; no task edits that line.
POINT C-009 | winner: neither | confidence: 60% | The matrix V2 criticises is the review run's artifact (artifacts/coverage-matrix.yaml), not the plan; V2 concedes the plan covers every item, and it undercounts the empty rows (also lines 6, 14, 49, 155).
POINT A-001 | winner: both | confidence: 85% | ACCEPT: managed plan (PLAN:2) plus SKILL.md:46/:56/:87 make one-file literal execution the right model; V2 drew the consequence (C-005), V1 did not.
POINT A-002 | winner: both | confidence: 65% | QUALIFY: both apply the stated rule identically on C-002, but V2's C-007 and V1's C-004 blocking grades both deserve re-grading by consequence.

### Variant 2 Advocate (haiku class)

#### Round 1 — Advocate for Variant 2 (haiku class)

<!-- Persisted by the orchestrator from three messages; the advocate declined to write files (its own instructions). Concession 2 and the A-001/A-002 responses arrived in part 2. Text unchanged except the three part labels are folded into one document. -->

##### Position summary

Variant 2 is stronger on execution mechanics and early drift-test failures, but its inevitable owner-gate bypass claim is overstated. Retain its verified findings, add Variant 1's two omitted blockers, and narrow the scale-map self-trip to a conditional risk.

##### Steelman

Variant 1 identifies contradictions independent of owner-gate interpretation. Task 16 requires exactly 11 digest rows and excludes the analysis template; Task 41 then requires all five templates, including it, to contain digests and have v2 registry rows. Task 6 promises a fresh-population classifier evaluation at stage 2, but Tasks 26-30 assign infrastructure and integrations without that evaluation. Both cards correctly identify the premature plugin-mirror existence check and the mechanical copy-order problem.

##### Strengths claimed

- L1: Variant 2 distinguishes coverage-matrix bookkeeping from missing implementation and documents checked requirements.
- L2: Task 25 prohibits source-tree paths in carriers, explicitly includes pointer-only rows, and registers spec-panel, whose live line 220 contains such a path; Task 45 does not name its removal.
- L3: The executor lists six known options, none selecting phases; it treats phase headings as groups and says "Do not STOP. Do not split." This establishes an execution-contract mismatch, not inevitable unauthorized execution. Task 31 accepts a report with failing recall requirements; Task 33 depends on completion without an explicit successful-recall transition check.
- Evidence: plan Tasks 6, 16, 25, 31, 33, 40, 41, 45, 46; executor SKILL lines 56, 72, 87, 105; live spec-panel line 220. All read directly; no tests run.

##### Weaknesses identified in the opponent

Variant 1 omits the phase-selection mismatch, the recall-result-versus-permission distinction, and the pointer-only scan failure. Correcting Variant 1's findings alone would not establish a coherent staged execution procedure or a passing offline registry check. These are omissions, not contradictions of Variant 2.

##### Concessions

1. V2 F1 overstates bypass: executor SKILL line 105 recognizes global Constraints, Q0 reads them, and refs/qa.md line 52 makes quoted breaches blocking. The verified issue is conflicting execution instructions, not proof that all remaining tasks must run without approval.
2. V2 F3's scale-map self-trip is conditional: Task 13 requires a section naming allowed files, not unambiguously verbatim banned phrases. A path-only list can avoid the scan without changing policy. Its claimed necessary decision is unproven.
3. Variant 1's analysis-template registry contradiction and unassigned fresh-population evaluation stand.
4. The coverage matrix records empty matched_task_ids and best_task: 0 candidates, not confirmed mappings to task 0. V2's non-blocking grade is sound; its wording is imprecise.

##### Shared assumptions

- A-001: QUALIFY. The plan selects this executor, so testing its actual task and acceptance semantics is justified. Literal contradictions are defects. Reject the inference that owner gates in global constraints have no effect; the executor explicitly carries them into implementation and QA.
- A-002: QUALIFY. Accept consequence-based grading and the shared mechanical/non-blocking treatment of Task 46 copy order. Reject automatic blockers based only on possible generated-text matches or inevitable unsafe continuation unsupported by the executor. The template contradiction, missing evaluation assignment, premature mirror check, and pointer-only path check have concrete consequences.

##### Per-point table

POINT S-001 | winner: both | confidence: 98% | Both structures work; V2's length adds coverage, not proof.
POINT C-001 | winner: both | confidence: 99% | Task 40 rejects a missing plugin mirror that Task 46 creates later.
POINT C-002 | winner: both | confidence: 98% | Task 46 copies before changing the source registry, an obvious mechanical parity correction.
POINT C-003 | winner: V1 | confidence: 99% | Task 16 excludes the analysis template from 11 digest rows, but Task 41 demands its digest and v2 row.
POINT C-004 | winner: V1 | confidence: 98% | Task 6 promises fresh-population evaluation at stage 2, but Tasks 26-30 never assign that run.
POINT C-005 | winner: V2 | confidence: 94% | No phase selector exists and phase headings do not bound enumeration, but global constraints defeat the inevitable-bypass claim.
POINT C-006 | winner: V2 | confidence: 91% | Task 31 accepts failed recall reports and Task 33 lacks an explicit pass transition, though owner constraints still apply.
POINT C-007 | winner: neither | confidence: 92% | Task 13 can list allowed paths without reproducing banned phrases, so the claimed inevitable self-trip is unproven.
POINT C-008 | winner: V2 | confidence: 99% | Task 25 checks pointer-only carriers for source paths, and registered spec-panel already contains one.
POINT C-009 | winner: V2 | confidence: 92% | Matrix omissions are non-blocking, but best_task: 0 with empty matches is only a candidate mapping.
POINT A-001 | winner: neither | confidence: 98% | Literal checks matter, but owner constraints do receive executor QA enforcement.
POINT A-002 | winner: both | confidence: 95% | Both distinguish mechanical corrections from concrete required-outcome defects, subject to the stated qualifications.

## Round 2: Rebuttals

### Variant 1 Advocate (opus class)

#### Round 2: Advocate for Variant 1 (rebuttal)

##### Response to criticisms

1. Opponent concession 1 (QA enforces the owner gates, so V2 F1 overstates the bypass) does not hold up against the live files. SKILL.md:105 and :129 do make the executor read `## Constraints`, but refs/qa.md:52 makes a breach blocking only when "The diff violates a parent `## Constraints` ... item ... and the reviewer can quote that text". Task 11's diff (create `SKILL.md`) violates nothing in PLAN:20. What is missing is an owner's chat message, which is not in the diff, not in any AC, and not visible to the fresh reviewer subagent (SKILL.md:113). So the reviewer has no anchor, the verdict is compliant, and Q8 continues to the next task (SKILL.md:149). Variant 2's original claim was right, and its advocate conceded too much.
2. On C-009 my Round 1 was wrong twice. The reviewer-2 brief told the qa persona to "audit the coverage matrix AGAINST the spec body ... surface any requirement-bearing span absent from the matrix ... as a finding" (reviewer-briefs/reviewer-2.md:21), so F6 is in scope. V2's "maps INF-008, INF-022, INF-027 and INF-028 to task 0" is also exact: `best_task: 0` appears 4 times (coverage-matrix.yaml:67, :191, :235, :243), once for each named id. The other empty `matched_task_ids` rows I cited have a non-zero best task, so "undercounts" was false. I withdraw both objections.
3. On C-007 the opponent is right that Task 13's acceptance line (PLAN:170) needs only the file list, so a path-only section passes Task 40. I hold only that the trap is likely in practice. That makes it a minor note, not a blocking finding.

##### Updated assessment

C-004: Medium, non-blocking. The finding is real (PLAN:93 promises a stage 2 run; no task after Phase 1 names `fresh-findings`). By the counterfactual test, though, nothing in this plan rests on that result: the classifier has no authority (OD4, PLAN:21) and the Phase 4 entry list (PLAN:20) does not include it. It is a follow-up: add the task or reword PLAN:93. I lower my Round 1 grade.

C-005: blocking. The named executor cannot meet the owner gates of PLAN:20, and the fix needs a decision the plan does not make: split the work into one managed plan per stage, or add a task per gate whose acceptance line requires a recorded owner go so QA has an anchor. Without that fix the failure is silent: Phase 4 switches the live carriers with no go.

C-006: blocking. PLAN:20 asks only for "the seeded-recall result of Task 31", Task 31 states "This task reports the result" (PLAN:376), and Task 33 depends only on Task 31 finishing (PLAN:394). Even a reviewer who quotes PLAN:20 finds the result file present, so no constraint breach exists when recall fails. The spec requires "seeded recall (section 8.3) met" before stage 3 (merged-requirements.md:947). This is a silent wrong result on a safety condition. It is independent of C-005: even an operator who stops at the Phase 4 boundary has no recall result yet.

C-007: minor. C-009: minor; V2's finding stands as written. A-001: QUALIFY (see New evidence).

##### New evidence

- `/sc:implement` has no pause or ask path for an owner go. A grep of `sc-implement-protocol` for halt, ruling, ask, pause and owner finds only these: `E-HALT-QA` after a terminal `halt` (SKILL.md:39, refs/qa.md:247), `E-NO-RULING` (SKILL.md:41, refs/qa.md:249), and the operator Ruling. The Ruling is the "only exit from a halt" (refs/qa.md:222), and it accepts a non-compliant task; it does not approve a phase start. The run stops only when a confirmed blocking finding survives one fix pass and the retry ladder (SKILL.md:145). That is an accidental stop, not a gate.
- Severity comes from the four checklist answers alone (refs/qa.md:37-52). The constraint-breach answer passes its read-back only when "the quoted text is byte-present in the plan Constraints" and the diff breaks it (refs/qa.md:52, :61). An absent chat message cannot be anchored in a diff.
- Task 11 (PLAN:139) and Task 31 (PLAN:374) have no acceptance line about an owner go or a recall pass, so the acceptance-criteria step (SKILL.md:93-103) gives QA nothing to check either.
- So A-001 is QUALIFY, not plain ACCEPT. The model of one plan file executed literally is correct, and the Constraints do reach QA (SKILL.md:105), but only as breaches visible in a diff, which owner gates and recall passes can never be. This qualification supports C-005 and C-006; it does not weaken them.

##### Point lines

POINT C-004 | winner: V1 | confidence: 75% | grade: Medium (non-blocking); the gap is real, but under OD4 and PLAN:20 no outcome in this plan rests on it
POINT C-005 | winner: V2 | confidence: 90% | grade: blocking; a constraint breach must be visible in the diff (refs/qa.md:52, :61) and the protocol has no ask or pause path, so the gates of PLAN:20 cannot be enforced and the fix needs a plan decision
POINT C-006 | winner: V2 | confidence: 88% | grade: blocking; PLAN:20 asks for a recall result, not a pass, and Task 33 depends only on Task 31 finishing (PLAN:394), so a failed recall silently reaches stage 3 (merged-requirements.md:947 requires recall met)
POINT C-007 | winner: neither | confidence: 65% | grade: minor; PLAN:170 needs only a path list, so the self-trip is avoidable; keep it as a note
POINT C-009 | winner: V2 | confidence: 75% | grade: minor; in scope per reviewer-2.md:21, and `best_task: 0` sits on exactly the four ids V2 named (coverage-matrix.yaml:67, :191, :235, :243)
POINT A-001 | winner: both | confidence: 80% | QUALIFY; executing one plan file literally is the right model, and the Constraints reach QA only as quoted breaches in a diff (SKILL.md:105, refs/qa.md:52), which confirms C-005

### Variant 2 Advocate (haiku class)

#### Round 2 — Advocate for Variant 2 (haiku class)

<!-- Persisted by the orchestrator from one message; the advocate does not write files. Text unchanged. -->

R2-V2 rebuttal

C-004: still disagree with Medium. PLAN:87 says the population 'must be tested apart'; :93 commits its evaluation to stage 2. Classifier authority being off (PLAN:21) does not cancel the required measurement result. This is missing evaluation, not merely weaker confidence.

C-005: agree blocking: SKILL:56,72,87 supplies neither phase selection nor a supported approval checkpoint; :39-41 and QA:222,247-249 describe failure/Ruling paths, not phase approval. However, 'Task 11 violates nothing' is too strong: creating its output before go violates PLAN:20. QA:52 requires a violating diff, not that every fact proving the violation be encoded in it; :61 anchors the quoted constraint. SKILL:129 makes the main executor read it. Keep the incompatible procedure finding, drop inevitable bypass.

C-006: agree blocking: PLAN:20 requires a result, :376 accepts failed recall reporting, and :394 does not demand successful recall. Owner approval and recall success are different conditions; no claim of inevitable continuation is needed.

C-007: agree neither/minor: PLAN:170 permits a path-only list.

C-009: agree V2/minor on omissions; best_task:0 remains a candidate, not a confirmed match when matched_task_ids is empty.

A-001: QUALIFY, now both: literal execution exposes incompatibility, but QA's constraint scope is not zero.

POINT C-004 | winner: V1 | confidence: 91% | grade: blocking
POINT C-005 | winner: V2 | confidence: 96% | grade: blocking
POINT C-006 | winner: V2 | confidence: 96% | grade: blocking
POINT C-007 | winner: neither | confidence: 95% | grade: minor
POINT C-009 | winner: V2 | confidence: 95% | grade: minor
POINT A-001 | winner: both | confidence: 96% | grade: minor

## Round 2.5: Invariant Probe

See `invariant-probe.md` (20 entries; the five HIGH and UNADDRESSED entries are listed above).

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | both | 80% | Both card shapes work; V2 records more verified anchors (R1: V1 adv 60% for V2, V2 adv 98% both) |
| C-001 | both | 90% | Task 40 allow-list and existence check name a mirror that Task 46 creates (PLAN:477, :482, :546); both cards cite it |
| C-002 | both | 95% | Task 46 copy-before-registry order; mechanical, minor in both cards |
| C-003 | V1 | 95% | Registry has 11 digest rows without the analysis template (PLAN:199, :203) but Task 41 gives it a digest and v2 row (PLAN:490, :494); V2 missed it |
| C-004 | V1 | 85% | No task after Phase 1 consumes the fresh-findings set (PLAN:93); the INV-006 probe widens it to the held-out split; grade blocking (judge) |
| C-005 | V2 | 93% | No phase selector, no pause path, Constraints reach QA only as diff-visible breaches (SKILL.md:56, :87, :105; refs/qa.md:52, :61); blocking; "inevitable bypass" dropped |
| C-006 | V2 | 92% | Task 31 reports only (PLAN:376); Task 33 depends on completion (PLAN:394); fix must be an acceptance line because `/sc:implement` ignores Depends on (SKILL.md:91) |
| C-007 | neither | 80% | Self-trip depends on executor wording; PLAN:170 needs only a path list; minor |
| C-008 | V2 | 99% | spec-panel.md:220 holds a `src/superclaude/` path; pointer-only rows go through T3 (PLAN:303); plugin twin has it too (INV-007) |
| C-009 | V2 | 85% | Matrix omissions are real but a review-run artifact; minor |
| A-001 | both | 90% | QUALIFY by both: one-file literal execution is the right model; Constraints reach QA only as diff-visible breaches |
| A-002 | both | 90% | QUALIFY by both: mechanical order errors minor, unmeetable checks blocking |

## Convergence Assessment

- Points resolved: 12 of 12 (winners); 1 grade dispute (C-004) ruled by the judge
- Alignment: 100% (Round 1: 9 of 12 = 75%; Round 2: 12 of 12)
- Threshold: 80%
- Status: CONVERGED on diff points; BLOCKED_BY_INVARIANTS until the five HIGH items are carried into the merged verdict (done in refactor-plan.md; they are findings F6 to F8 and parts of F1 to F2 in the merged card)
- Unresolved points: none
