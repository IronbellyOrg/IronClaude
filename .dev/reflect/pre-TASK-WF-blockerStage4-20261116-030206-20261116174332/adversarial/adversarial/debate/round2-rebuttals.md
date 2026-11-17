# Round 2: rebuttals (sequential: V1, V2, V3; saved verbatim by the orchestrator)

## Variant 1 advocate (sonnet class)

### Response to criticisms
- **X-004 (wrong line):** Conceded. Plan line 87 (P4:87) is the FR-8 bullet. The plugin decision is at P4:23 and P4:91. This is an error in my card, not in the plan, so it is minor.
- **F1 label `unpassable-check`:** Conceded. Task 5 can be passed, so the label was wrong. The real fault is that the check does not discriminate.
- **Missed C-007 to C-010:** Conceded. I only re-read C-009 and C-011 this round, so I leave C-007, C-008 and C-010 at minor on Round 1 evidence.
- **V2: F6 (the 10.5 pointer gap) is undergraded:** Partly right. I now grade C-002 MEDIUM, not blocking.
- **V3: F1 is only minor:** Partly right. I now grade C-001 MEDIUM.
- **V2's "OpenAI model" note:** I leave it alone. It does not affect any grade.

### Updated assessment
**C-001.** I re-read P4:108: "switch T2 ... to strict mode, so a legacy definition sentence left in a tracked file under `src/` fails". P4:112 requires "is in strict mode". The text does not allow a no-op switch, so this is not blocking. But new evidence makes the check weaker than I said. A Grep of the stage 1 plan finds "strict" only once, at S1:223: "strict mode is a switch, off in this phase". The switch is never named and stage 1 has no acceptance check that it exists. P4:112's example (an unregistered file with the old sentence) is already failed by non-strict T2, per S1:223. P4:115, a grep over `src/superclaude` and `plugins/superclaude` that must print nothing, only proves today's tree is clean. It does not prove the guard is armed. A real but non-blocking weakness in the check is MEDIUM. My Round 1 grade (minor) changed.

**C-002.** I re-read SPEC:867. It says "`skills/roadmap`, `readme`, `tech-reference`, `operational-guide` cap lines [E] | point at the shared rule". SPEC:861 limits section 10.5 to files that "need an edit because they say who counts, merges or escalates". SPEC:948 (stage 4) lists no cap-line pointer edit. SPEC:1105 lists the roadmap and tech-research lines as unverified [E].
- P4:70 says "Do not touch any cap sentence".
- S2:88 says tech-research gets "no text beside the cap sentences".
- No task touches roadmap, and the plan records no exclusion.
- Stage 4 is the last package, so no later stage catches it.

The requirement is conditional and unverified, and no review outcome changes, so it is not blocking. An unrecorded gap against a spec row is more than a wording slip, so I move it to MEDIUM. This also covers tech-research. V2's blocking grade does not follow from the grading rule.

**C-005.** SPEC:739 says "CRITICAL: Blocking" in column 3 and "narrow 'CRITICAL is blocking'" in column 4. The two readings conflict, so this is minor. I concede that the plan's stated reason is thin: Task 4 re-pins the same mapping test anyway.

**C-006.** Grep results: the sentence "runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings" is already in 11 of 11 carriers. `review-severity:digest v2 begin` appears in none. So the P4:43 and P4:60 sentence greps do not discriminate. The paired `v2 begin` grep does, and so does registry test T1. This is minor.

**C-009.** S1:214 adds a doctor test in `tests/unit/test_cli_doctor.py`. P4:108 says to reword a `doctor.py` literal, and P4:113 runs no doctor test. P4:108 states its own purpose as "so that no red test ships unseen". An edit that only sometimes happens, with the check missing, is a MEDIUM warning. This moves up from minor.

**C-011.** I re-checked this. INF-015, INF-025 and INF-027 appear only in `.dev/reflect` artifacts, not in the plan, so I drop it. The plan keeps G6 order at P4:37, the retired test at P4:22 and the counts at P4:23.

**X-003.** No blocking finding survives. The warnings are C-001, C-002 and C-009, all MEDIUM. The verdict is pass with warnings, not NEEDS-REVISION on blocking grounds.

### New evidence
1. S1:223 is the only mention of "strict" in the stage 1 plan, and the switch is never named.
2. The roadmap skill has six "Max 2 fix cycles." lines (SKILL.md 434, 435, 439, 440, 447, 448). None says who counts toward the cap. A pointer would be an addition, so the omission cannot create a wrong result.
3. The sentence count and `v2 begin` count in C-006 come from a Grep of `src/superclaude` this round.
4. S1:214 gives the doctor tests their own stage 1 acceptance line, so omitting them from stage 4 stands out.

### Final grades
- C-001: MEDIUM (was minor).
- C-002: MEDIUM (was minor).
- C-005: minor.
- C-006: minor.
- C-009: MEDIUM (was minor).
- C-011: drop.
- X-003: no blocking defect; warnings only (three MEDIUM).
- Added line, X-001 and X-002 follow C-001 and C-002: MEDIUM.
- Unchanged: C-003, C-004, C-007, C-008 and C-010 stay minor, X-004 stays minor, X-005 stays dropped.

## Variant 2 advocate (haiku class)

### Response to criticisms
I concede V2 omitted tech-research, did not simulate the pinning tests, and overused "Do not touch any cap sentence": an adjacent pointer need not alter that sentence. Plan 74 already supplies pointers through merge edits in the four named files. The model-identity self-report is unreliable; it does not invalidate independently checked quotations. C-011 concerns the review's coverage record, not an implementation omission.

Re-read spec 861-869, quoted excerpts:
861: "Those cap-family files that need an edit because they say who counts, merges or escalates:"
865: "L1, L2, L3, ledger"
866: "the cap counts Blocking only; fix-step checks (L2)"
867: "skills/tech-research/SKILL.md" and "skills/roadmap, readme, tech-reference, operational-guide" -> "point at the shared rule; the consumer line (L4) in the task builder"
868: "only if OD7 says so"
869: "only if OD6 says so"

Spec 948 says "templates, rule prompts, builders and researchers to v2" and "T2 becomes strict"; it does not explicitly assign the pointer work. That summary's silence does not cancel 867. Spec 1105 calls these "The loop line numbers marked [E] in section 10.5"; it marks the locations unverified, not the prescribed edit optional.

Re-read plan 70-76: Task 3 names tech-reference, readme, tdd and operational-guide; 70 says "Do not touch any cap sentence"; 74 requires "each of the four files names sc-review-severity/refs/rule.md"; 75 requires "The cap text in each of the four files is unchanged"; 76 checks their allow-list removal. Roadmap is absent.

V1's six short cap summaries are real. Roadmap 434-448 repeatedly says "Max 2 fix cycles" and names rf-qa/rf-qa-qualitative reviewers. But those summaries are not the whole escalation instruction. Roadmap 563 says: "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." That satisfies 861's "escalates" description.

### Updated assessment
C-002 remains blocking under the supplied missing-result rule. An executor following the enumerated edits produces updated templates, prompts and four merge-rule files, but leaves roadmap's escalation instruction without the shared-rule pointer specified by 867. That missing reference, not a demonstrated wrong grading outcome, is exactly what is wrong with the product. Delegating reviews to updated agents may preserve behaviour; it does not supply the explicitly requested reference. Adding the pointer is the required result, not an unsupported extra feature.

C-001 changes from minor to MEDIUM: the strict-mode instruction remains explicit in plan 108 and 112, so leaving it off is not compliant. Nevertheless, the promised negative example cannot distinguish strict from non-strict operation. This is a substantive verification warning, not merely wording.

C-009 stays MEDIUM: plan 108 permits a doctor-code change, but 113 omits its related tests. C-011 is dropped from plan findings. X-003 stays NEEDS-REVISION because C-002 survives. Every other point stays as in Round 1 unless changed above.

### New evidence
Roadmap 563 directly rebuts the claim that its relevant text merely states a numerical cap. It contains the escalation action itself. The six summary lines cannot establish that 861 excludes this file. No tests or writes were performed; no incorrect runtime grade is claimed.

### Final grades
C-001: MEDIUM, changed; non-discriminating strict-mode evidence.
C-002: blocking, unchanged; specified roadmap pointer remains missing.
C-009: MEDIUM, unchanged; conditional related-test coverage gap.
C-011: drop, changed; coverage-record defect, not plan defect.
X-003: blocking / NEEDS-REVISION, unchanged; follows from C-002.

## Variant 3 advocate (opus class)

### Response to criticisms
- **C-001 (V1, V2):** I keep my Round 1 concession. P4:108 requires the switch and says what it does ("so a legacy definition sentence left in a tracked file under `src/` fails"). P4:112 requires "is in strict mode". So a switch that does nothing breaks the text. It is not the only reading the text allows, which rules out blocking.
- **C-002, my "SPEC:861 makes it conditional" argument:** I withdraw it. Roadmap meets the 861 test. Roadmap SKILL.md:562 says "Count consolidated blocking lens findings" and :563 says "HALT and escalate to the user with the open blocking findings". So it counts and escalates.
- **V1's X-005 paraphrase point:** conceded. After P4:74, only roadmap and tech-research are left without a pointer, but SPEC:867 also names the other files.
- **C-009:** I move it up to MEDIUM. Doctor tests exist (`tests/unit/test_cli_doctor.py`, `tests/cli/eval/test_doctor.py`). P4:108 allows rewording `doctor.py`, and P4:113 runs none of those tests.

### Updated assessment
**C-002 stays MEDIUM.** The plan's executor cannot reach a wrong grade, merge or cap because the pointer is missing:
1. **No merge or scale change is required.** Roadmap is in neither the merge-line table (SPEC:832-841, 10.3) nor the lens-scale row (SPEC:737). The only edit asked of it is a cap-line pointer.
2. **The cap text is already right.** Roadmap :563 and tech-research :490 and :555 already say "open blocking findings". The cap of 2 must not change (P4:26).
3. **Strict T2 never reaches these files.** A Grep of `src/superclaude/skills` finds the old sentence in no skill file.
4. **The pointer is not in the exit condition.** SPEC:948's exit is "drift tests green and strict; a second audit window clear". The pointer is not part of it. Roadmap and tech-research keep today's behaviour, so there is no regression, only a missing reference.

The gap comes from upstream, not from this plan's author:
- source.md:12 says "As the base text (the old Tasks 42 to 44)".
- Base Task 43 (loosenBlockerRev:513) edits only the 10.3 merge lines.
- Stage 3 hands this work forward (S3:26 "builder, researcher ... edits (those are stage 4)"). Stage 2 adds nothing beside the cap sentences (S2:88).

V2's best point stands: stage 4 is the only possible owner, and the plan records no exclusion. That is a real coverage gap, so MEDIUM. Two fixes work: one Constraints line recording the exclusion, or a two-file pointer edit.

### New evidence
- Base plan Task 43 (`TASK-WF-loosenBlockerRev-20261115-210254.md`:513-518) never named roadmap or tech-research. The plan follows its request.
- SPEC:948's "What happens" column does list "builders and researchers to v2", but as work, not as an exit condition.
- SPEC:1105 marks the roadmap and tech-research lines unverified.
- Roadmap :561 ("Severity-rate each: CRITICAL / IMPORTANT / MINOR") is outside the 10.5 cap-line scope, so a pointer at :563 would not change that count anyway.

### Final grades
- **C-001: MEDIUM.** Here is the strongest case for blocking, reading P4:108, :112, :115 and :122 together:
  - Stage 4 is the last package, and "strict" is its exit condition.
  - The only strict-specific check (the :112 temporary-tree case) is already failed by non-strict T2 (S1:223).
  - :115's grep and :112's "all 11 at v2" check the end state, which is the same under both modes.
  - :122 only reports counts.
  - So a no-op switch passes every check, and nothing after stage 4 catches it.

  That case still fails the rule, because :108 and :112 forbid the no-op reading and an executor can see the mode in the test file. The fix is a temporary-tree case that fails only in strict mode: a registered `legacy` row whose file still holds the old sentence.
- **C-002: MEDIUM**, for the reasons above.
- **C-009: MEDIUM**, up from minor.
- **C-011: drop.**
- **X-003: no blocking finding survives.** Verdict: warnings only, with three MEDIUM findings (C-001, C-002, C-009).
- **Other changes:** none. C-003 to C-008 and C-010 stay minor.

Not checked: the actual strict-mode code in stage 1's T2. It does not exist yet, so the case above about what strict mode adds rests on S1:223 and SPEC:948 only.
