# Round 2: Advocate for Variant 1 (rebuttal)

## Response to criticisms

1. Opponent concession 1 (QA enforces the owner gates, so V2 F1 overstates the bypass) does not hold up against the live files. SKILL.md:105 and :129 do make the executor read `## Constraints`, but refs/qa.md:52 makes a breach blocking only when "The diff violates a parent `## Constraints` ... item ... and the reviewer can quote that text". Task 11's diff (create `SKILL.md`) violates nothing in PLAN:20. What is missing is an owner's chat message, which is not in the diff, not in any AC, and not visible to the fresh reviewer subagent (SKILL.md:113). So the reviewer has no anchor, the verdict is compliant, and Q8 continues to the next task (SKILL.md:149). Variant 2's original claim was right, and its advocate conceded too much.
2. On C-009 my Round 1 was wrong twice. The reviewer-2 brief told the qa persona to "audit the coverage matrix AGAINST the spec body ... surface any requirement-bearing span absent from the matrix ... as a finding" (reviewer-briefs/reviewer-2.md:21), so F6 is in scope. V2's "maps INF-008, INF-022, INF-027 and INF-028 to task 0" is also exact: `best_task: 0` appears 4 times (coverage-matrix.yaml:67, :191, :235, :243), once for each named id. The other empty `matched_task_ids` rows I cited have a non-zero best task, so "undercounts" was false. I withdraw both objections.
3. On C-007 the opponent is right that Task 13's acceptance line (PLAN:170) needs only the file list, so a path-only section passes Task 40. I hold only that the trap is likely in practice. That makes it a minor note, not a blocking finding.

## Updated assessment

C-004: Medium, non-blocking. The finding is real (PLAN:93 promises a stage 2 run; no task after Phase 1 names `fresh-findings`). By the counterfactual test, though, nothing in this plan rests on that result: the classifier has no authority (OD4, PLAN:21) and the Phase 4 entry list (PLAN:20) does not include it. It is a follow-up: add the task or reword PLAN:93. I lower my Round 1 grade.

C-005: blocking. The named executor cannot meet the owner gates of PLAN:20, and the fix needs a decision the plan does not make: split the work into one managed plan per stage, or add a task per gate whose acceptance line requires a recorded owner go so QA has an anchor. Without that fix the failure is silent: Phase 4 switches the live carriers with no go.

C-006: blocking. PLAN:20 asks only for "the seeded-recall result of Task 31", Task 31 states "This task reports the result" (PLAN:376), and Task 33 depends only on Task 31 finishing (PLAN:394). Even a reviewer who quotes PLAN:20 finds the result file present, so no constraint breach exists when recall fails. The spec requires "seeded recall (section 8.3) met" before stage 3 (merged-requirements.md:947). This is a silent wrong result on a safety condition. It is independent of C-005: even an operator who stops at the Phase 4 boundary has no recall result yet.

C-007: minor. C-009: minor; V2's finding stands as written. A-001: QUALIFY (see New evidence).

## New evidence

- `/sc:implement` has no pause or ask path for an owner go. A grep of `sc-implement-protocol` for halt, ruling, ask, pause and owner finds only these: `E-HALT-QA` after a terminal `halt` (SKILL.md:39, refs/qa.md:247), `E-NO-RULING` (SKILL.md:41, refs/qa.md:249), and the operator Ruling. The Ruling is the "only exit from a halt" (refs/qa.md:222), and it accepts a non-compliant task; it does not approve a phase start. The run stops only when a confirmed blocking finding survives one fix pass and the retry ladder (SKILL.md:145). That is an accidental stop, not a gate.
- Severity comes from the four checklist answers alone (refs/qa.md:37-52). The constraint-breach answer passes its read-back only when "the quoted text is byte-present in the plan Constraints" and the diff breaks it (refs/qa.md:52, :61). An absent chat message cannot be anchored in a diff.
- Task 11 (PLAN:139) and Task 31 (PLAN:374) have no acceptance line about an owner go or a recall pass, so the acceptance-criteria step (SKILL.md:93-103) gives QA nothing to check either.
- So A-001 is QUALIFY, not plain ACCEPT. The model of one plan file executed literally is correct, and the Constraints do reach QA (SKILL.md:105), but only as breaches visible in a diff, which owner gates and recall passes can never be. This qualification supports C-005 and C-006; it does not weaken them.

## Point lines

POINT C-004 | winner: V1 | confidence: 75% | grade: Medium (non-blocking); the gap is real, but under OD4 and PLAN:20 no outcome in this plan rests on it
POINT C-005 | winner: V2 | confidence: 90% | grade: blocking; a constraint breach must be visible in the diff (refs/qa.md:52, :61) and the protocol has no ask or pause path, so the gates of PLAN:20 cannot be enforced and the fix needs a plan decision
POINT C-006 | winner: V2 | confidence: 88% | grade: blocking; PLAN:20 asks for a recall result, not a pass, and Task 33 depends only on Task 31 finishing (PLAN:394), so a failed recall silently reaches stage 3 (merged-requirements.md:947 requires recall met)
POINT C-007 | winner: neither | confidence: 65% | grade: minor; PLAN:170 needs only a path list, so the self-trip is avoidable; keep it as a note
POINT C-009 | winner: V2 | confidence: 75% | grade: minor; in scope per reviewer-2.md:21, and `best_task: 0` sits on exactly the four ids V2 named (coverage-matrix.yaml:67, :191, :235, :243)
POINT A-001 | winner: both | confidence: 80% | QUALIFY; executing one plan file literally is the right model, and the Constraints reach QA only as quoted breaches in a diff (SKILL.md:105, refs/qa.md:52), which confirms C-005
