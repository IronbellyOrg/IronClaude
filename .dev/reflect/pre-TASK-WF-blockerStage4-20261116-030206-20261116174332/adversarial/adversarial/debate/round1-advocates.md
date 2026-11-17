# Round 1: advocate statements (saved verbatim by the orchestrator)

Advocates: V1 sonnet class, V2 haiku class, V3 opus class (general-purpose agents, read-only).

## Variant 1 advocate (analyzer card)

### Position summary
Variant 1's verdict stands: I find no blocking defect in Tasks 1 to 6, so the plan has warnings only. The two grade splits are minor on both sides. For strict T2 the weakness is that the evidence doesn't discriminate. The plan states the strict requirement twice. For spec section 10.5 the pointer lines are unverified [E], assigned to no stage, and not in the stage 4 exit row.

### Steelman
Variant 2: Its strongest argument is that SPEC:867 lists the roadmap, readme, tech-reference and operational-guide "cap lines" under "point at the shared rule". Task 3 says "Do not touch any cap sentence" (P4:70), and roadmap is touched by no task. Nothing in the plan or source.md records an exclusion, and stage 4 is the last package, so no later stage catches it. It is right that the plan is silent on this and that the coverage matrix has no row for it. It is also right that stage 1 does not name the strict switch. It cited S1:223 accurately and weighed the "not inevitable" point honestly in F2.

Variant 3: Its strongest argument is that strict T2 is the headline exit condition (SPEC:948, "T2 becomes strict"). Every Task 5 check passes with the switch off. The temporary-tree case is already failed by non-strict T2 (S1:223: "fails on any file that holds the old definition sentence ... and has no registry row"). The 12-test run is green anyway because Tasks 1 and 2 remove every old sentence. Its fix is a registered legacy file that fails only with the switch on, and that fix is correct. It also found three things I missed. The FR-8 parenthesis rationale is wrong (C-007). The stage 3 text is stale (C-008). The doctor tests are missing from the final run (C-009).

### Strengths claimed
1. Test simulation of Tasks 2 and 4 against the pinning tests. Only Variant 1 did this. It checked the new Unattended line against `_artifacts_clause` and the one-line briefs. Variant 2 ran no such check, and Variant 3 only partly did.
2. It spotted the non-discriminating greps. P4:43 "its digest ends with the sentence" and P4:60 print 1 today. I re-checked: the sentence "runs at most 2 fix cycles (3 reviews), then escalate" already occurs once in each of the 11 carrier files. Only the `digest v2 begin` clause in the same bullet discriminates.
3. It graded the strict-T2 gap minor. P4:108 says "switch T2 ... to strict mode, so a legacy definition sentence left in a tracked file under `src/` fails". P4:112 says "T2 ... is in strict mode". source.md:15 says "strict T2 is switched on here". The switch is required three times, and Task 6 must report "registry tests with strict T2" (P4:122).
4. It graded the 10.5 gap minor. SPEC:1105 lists the 10.5 lines as unverified [E]. The stage 4 row at SPEC:948 names no cap-line edit. The cap sentences already say "open blocking findings" (P4:43). The edits Task 3 does make already name the rule (P4:74).
5. It noticed the CRITICAL deviation (F4). SPEC:739 says "narrow 'CRITICAL is blocking'". P4:85 keeps it, and source.md:32 records the reason as "pinned".

### Weaknesses identified in the others
1. Variant 2 F1 grades blocking, but the requirement cannot be traced to a stage. SPEC:861 calls 10.5 "files that need an edit because they say who counts", and SPEC:867 marks it [E]. SPEC:845 withdraws the claim that the rule sits in tech-research and task-builder. Variant 2 names roadmap only, although tech-research has the same status (X-005), and it ignores SPEC:948.
2. Variant 2 ran no test simulation. Its Checked section says "No shell commands, tests or writes were run" and gives no pin-by-pin check of the text Tasks 2 and 4 will write.
3. Variant 3 F1 claims "a missing or no-op strict switch passes every check". But P4:112 itself requires "is in strict mode", which an executor can verify in the test file. The worse reading is not the only one the text allows, so the rubric gives minor.
4. Variant 3 F8 says SPEC:867 asks "the roadmap and tech-research cap lines". The cell names roadmap, readme, tech-reference and operational-guide, and gives line numbers for tech-research. The paraphrase is loose.
5. Variant 2's `model_observed` is "OpenAI model", although the card was pinned as haiku class. The card may be unreliable on model class, and its F1 is the least checked.

### Concessions
1. X-004: Variant 1's Checked says "G4 is removed by the plugin decision at plan line 87". P4:87 is the FR-8 bullet. The decision is at P4:23 and P4:91.
2. Variant 1 labelled F1 `unpassable-check`. The check is passable, so the label is wrong. It is non-discriminating.
3. Variant 1 missed C-007 (P4:91 says the mapping test pins the FR-8 line, but MAP:102 pins only "otherwise it is Medium"). It also missed C-008, C-009 and C-010.
4. The strict-T2 evidence is weak, and Variant 3's discriminating test would fix it. If the card set has only minor and MEDIUM available, MEDIUM there is defensible.
5. Variant 1's F4 reason, "the same task re-pins the neighbouring literals", is a fair point. The deviation from SPEC:739 is a recorded decision, but the pin justification is thin.

### Grades
- C-001: minor. P4:108 and P4:112 both require strict mode. Only the example is non-discriminating (S1:223 already fails an unregistered file).
- C-002: minor. SPEC:867 is [E] (SPEC:1105). SPEC:948 does not list cap-line edits. One line recording the exclusion would cure it.
- C-003: minor. The parenthesis at P4:41 names archive-blocked as failing. The intent is explicit, and the "done subfolder" branch cannot be archive-blocked.
- C-004: minor. P4:37 `grep -n "^6\. \*\*"` matches about ten numbered rules. Line 990 is the only Rule 6 in `## Critical Rules`.
- C-005: minor. The spec row maps "CRITICAL: Blocking" (SPEC:739) and also says to narrow it. The plan records its choice (source.md:32) and narrows the dimensional mismatch.
- C-006: minor. The cap-sentence count is 1 in each of the 11 carriers today. The `v2 begin` clause in the same bullet discriminates, and so does T1.
- C-007: minor. The mapping test asserts only "otherwise it is Medium" for FR-8 (MAP:102). The edit is still required by the P4:96 grep, so the effect is nil.
- C-008: minor, and it belongs to stage 3. S3:214 still says stage 4 "adds the plugin mirror"; P4:23 builds none.
- C-009: minor. Task 5 may reword a string in `doctor.py` (P4:108), but the 12-test run (P4:113) omits the doctor tests. A rewording that builds the literal from parts keeps behaviour.
- C-010: minor. P4:116 cites the Task 6 summary, which is written later. It is a forward reference and not a falsified check.
- C-011: drop. The gap is in the evidence artifact. The plan holds the requirements: P4:37 for G6 order, P4:22 for the retired test, P4:23 for the counts.
- X-001: minor. See C-001.
- X-002: minor. See C-002.
- X-003: no blocking finding, so the verdict is not NEEDS-REVISION on blocking grounds. Warnings only.
- X-004: minor, an error in Variant 1's card and not in the plan.
- X-005: drop, a paraphrase difference only.

### Shared assumptions
- A-001: ACCEPT. I re-read S1:223. T2 fails an unregistered file with the old sentence, and "strict mode is a switch, off in this phase".
- A-002: QUALIFY. Reading cross-stage facts from plan text is the only option. P4:40-42 checks only the stage 3 state before any edit, and it only implies stages 1 and 2 are done. Nothing checks that the registry, scale-map section or test files exist.
- A-003: QUALIFY. The 12-test list can only be judged by reading, since no test has run. It also omits `tests/unit/test_cli_doctor.py` while Task 5 may edit `doctor.py`.

## Variant 2 advocate (qa card)

### Position summary
Variant 2 has the better distinction between a missing required result and an imperfect check: the roadmap pointer omission is blocking; the strict-T2 example is minor under the supplied ambiguity rule. I retain NEEDS-REVISION, while accepting useful coverage findings from both opponents.

### Steelman
Variant 1 offers the strongest practical compatibility review: its test simulation identifies constraints that could break otherwise correct edits, and it correctly avoids treating every ambiguous instruction as blocking. Its strict-T2 diagnosis is sound: S1:223 already requires failure for an unregistered legacy-sentence file. Its six minor findings also distinguish awkward evidence from inevitable failure.

Variant 3 gives the strongest account of the strict-mode risk: SPEC:917 requires rejection of "any legacy definition sentence" from stage 4, whereas the proposed negative example exercises only already-required non-strict behavior. Its cross-stage checks, partial-plugin analysis and omitted doctor-test warning broaden coverage beyond Variant 2.

### Strengths claimed
1. Variant 2 identifies a genuinely missing deliverable. SPEC:867 names "skills/roadmap" and requires "point at the shared rule"; P4:70 lists four other carriers and says "Do not touch any cap sentence." No stage-4 task supplies the roadmap pointer or records its exclusion.
2. It grades the strict-T2 weakness against the whole instruction, not just the example. P4:112 expressly says T2 "is in strict mode"; S1:223 says non-strict already "fails on any file" with the old sentence and no registry row. Weak evidence does not make leaving strict mode off compliant.
3. It separates coverage evidence from execution instructions. The matrix rows INF-015, INF-025 and INF-027 omit clauses retained in P4:37 ("before any edit"), P4:22 ("neither run nor re-pinned") and P4:23 (final registry counts). These are coverage-record omissions, not absent implementation requirements.

### Weaknesses identified in the others
1. Both opponents undergrade the pointer omission. SPEC:861 calls these files ones that "need an edit," and SPEC:867 supplies the action. Its [E] annotation does not say optional; unlike SPEC:868-869, the row has no "only if" qualification. A small missing required result still meets the supplied blocking definition.
2. Variant 3 overgrades strict T2 by treating passing the example as satisfying every instruction. P4:108 says "Then switch T2 ... to strict mode," and P4:112 repeats that requirement. A no-op switch violates those words; it is not the only implementation the plan permits.
3. Variant 1's plugin-decision citation is wrong: P4:87 is the "FR-8 line"; P4:23 says "No plugin surface is added." This is a citation repair, not a substantive blocker.

### Concessions
Variant 2's roadmap-only claim is narrower than SPEC:867's full inventory; it should not imply the other listed carriers were fully reconciled. It also misses Variant 1's useful test simulation and Variant 3's doctor-test warning. The CRITICAL wording dispute deserves retention, but SPEC:739 itself combines "CRITICAL: Blocking" with an instruction to narrow it, preventing an unqualified blocking grade.

### Grades
- C-001: minor. P4:112 requires strict mode explicitly, although its unregistered-file example duplicates S1:223.
- C-002: blocking. SPEC:867 requires the roadmap shared-rule pointer; P4:70 omits roadmap and no later task supplies it.
- C-003: minor. P4:41 permits complete ledger lines but expressly rejects archive-blocked packages, leaving competing readings.
- C-004: minor. P4:37's file-wide numbered-rule selector is underspecified, but P4:47 still requires the actual Rule 6 heading.
- C-005: minor. P4:85 preserves "CRITICAL is blocking," while SPEC:739 both maps CRITICAL to Blocking and requests narrowing.
- C-006: minor. P4:43 and P4:60 count a sentence without proving its position, but P4:45 and P4:64 also require registry tests and S1:223 defines full digest equality.
- C-007: minor. P4:23's test-pinned-only policy and P4:91's selective plugin edits leave a scope/rationale inconsistency, not a required plugin-wide migration.
- C-008: minor. S3:214 says stage 4 "adds the plugin mirror," but P4:23 explicitly builds none; stage-4 execution has a clear instruction.
- C-009: MEDIUM. P4:108 permits rewording doctor code, while P4:113 omits its related tests; this is a real conditional coverage warning, not proven breakage.
- C-010: minor. P4:116 cites the later Task 6 summary, but the underlying no-retired-carrier requirement is independently inspectable.
- C-011: minor. The matrix rows truncate requirements that P4:37, P4:22 and P4:23 actually preserve.
- X-001: minor. P4:108 and P4:112 require strict operation separately from the non-discriminating example, so the defective implementation is not inevitable.
- X-002: blocking. SPEC:867 says "point at the shared rule"; its evidence annotation supplies no exemption for the missing roadmap result.
- X-003: blocking. NEEDS-REVISION follows from the unresolved SPEC:867 requirement, not from the strict-T2 example.
- X-004: minor. P4:87 concerns FR-8; the plugin decision is P4:23, so only the citation needs correction.
- X-005: minor. SPEC:867 includes both tech-research and roadmap, plus other carriers; the paraphrase is incomplete, not fabricated.

### Shared assumptions
- A-001: ACCEPT. S1:223 explicitly makes strict mode "a switch, off in this phase" and already rejects unregistered legacy-sentence files.
- A-002: QUALIFY. These are planned dependencies, not observed implementations; P4:20 and P4:40-42 require stage-3 completion evidence before editing.
- A-003: REJECT. All rows being v2 does not establish a green final run; P4:113 requires an observed pass, and P4:126 requires observed counts.

## Variant 3 advocate (refactorer card)

### Position summary
Variant 3 has the widest coverage. It is the only card that raised C-007 to C-010, and every one of those checks out on re-reading. Its blocking grade on strict T2 does not survive the grading rule, though, so I concede that point. Neither split is blocking: I grade C-001 MEDIUM and C-002 MEDIUM.

### Steelman
Variant 1: Its strongest point on strict T2 is that the plan states the requirement and defines its effect. P4:108 says "switch T2 ... to strict mode, so a legacy definition sentence left in a tracked file under `src/` fails". P4:112 requires that T2 "is in strict mode". A lazy executor is a possible reading, not the only one. V1 is also the only card with a test simulation, and the only one to find C-005 and C-006. Both are real.

Variant 2: Its strongest point is that SPEC:867 asks for "point at the shared rule" and no stage does it. Stage 2 explicitly declines to touch tech-research: S2:88 says "this package adds no text beside the cap sentences". P4 never mentions roadmap or tech-research, and a Grep of the package finds neither. Every task can pass while the requirement goes unmet. V2 also applies the two-readings rule correctly to strict T2 (its F2).

### Strengths claimed
1. F1 is the right diagnosis. S1:223 says T2 "fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind ... strict mode is a switch, off in this phase". So the case at P4:112, "has no registry row failing", cannot tell strict mode from non-strict mode.
2. F4 is confirmed. tests/skills/test_review_severity_mapping.py:102 pins only `assert "otherwise it is Medium" in fr8`, not the parenthesis. Yet P4:91 says the FR-8 line is edited "because the mapping test pins them".
3. F5 is confirmed. S3:214 says stage 4 "adds the plugin mirror of `refs/rule.md` to the allow-list". P4:23 says "builds no `plugins/superclaude/skills/sc-review-severity/` folder".
4. F6 and F7 are confirmed. P4:108 may reword a literal in `src/superclaude/cli/doctor.py`, but the run at P4:113 has no doctor test. P4:116 cites "(listed in the Task 6 summary)" before Task 6 runs.
5. The Checked claim about the 11 carriers is confirmed. My Grep of src/superclaude finds "Grade every review finding as blocking or minor" in exactly 11 files.
6. F8 names the right gap. Task 3 gives readme, tech-reference and operational-guide a pointer to rule.md: P4:74 says "each of the four files names `sc-review-severity/refs/rule.md`". So the files left without a pointer are exactly roadmap and tech-research.

### Weaknesses identified in the others
1. V1's Checked section says "G4 is removed by the plugin decision at plan line 87". P4:87 is the FR-8 bullet. The plugin decision is at P4:23.
2. V1 F1 grades strict T2 minor. But the evidence it promises cannot tell the two modes apart. That is a real weakness, so it is MEDIUM.
3. V2 F1 names roadmap only. SPEC:867 also gives tech-research lines: "`skills/tech-research/SKILL.md` 488 to 490, 517 to 519, 555, 562 [E]".
4. V2 grades F1 blocking, but no review outcome changes. The roadmap cap lines hand review to the rf-qa agents (roadmap/SKILL.md:434: "3 rf-qa structural + 3 rf-qa-qualitative ... Max 2 fix cycles"), and those agents already carry the rule. The spec also limits section 10.5 to files that "need an edit because they say who counts, merges or escalates" (SPEC:861), and marks the lines [E].
5. V2 cites P4:70 "Do not touch any cap sentence" as evidence, but three of the four files get their pointer through the merge line at P4:74.
6. V2 F4 is about the reviewers' coverage matrix (coverage-matrix.yaml), not about the plan.

### Concessions
- V3's F1 grade of blocking is wrong. P4:112 requires strict mode, so the worse reading (a switch that does nothing) is not the only one the text allows. The stage 4 exit state is also checked directly: P4:115 says the `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` "prints nothing". So V3's verdict, NEEDS-REVISION with one blocking finding, falls.
- V3's F8 grade of minor was too low; it should be MEDIUM.
- V3 missed C-005 and C-006.

### Grades
- C-001: MEDIUM. P4:112's temporary-tree case already fails under S1:223's non-strict scan, but P4:112 requires strict mode and P4:115 checks the outcome.
- C-002: MEDIUM. SPEC:867's pointer edit is covered by no stage, and P4 records no exclusion. But SPEC:861 makes the edit conditional, the lines are [E], and no grade changes.
- C-003: minor. P4:41's parenthesis states the intended halt, so only the wording conflicts.
- C-004: minor. The P4:37 grep also hits rf-qa-qualitative.md:97, and the executor can pick line 990 by hand.
- C-005: minor. SPEC:739 says to narrow "CRITICAL is blocking", but the same row maps "CRITICAL: Blocking", so the spec allows two readings. P4:85's reason (the test pin) is weak.
- C-006: minor. The fix-cycles grep counts 1 in all four templates today. The paired digest-count grep at P4:43 prints 0 today, so the check as a whole still shows whether the edit happened.
- C-007: minor. test_review_severity_mapping.py:102 does not pin the parenthesis, so P4:91's reason is wrong. But P4:96's own grep needs the edit anyway.
- C-008: minor. The stale text is at S3:214, and it is description, not an instruction.
- C-009: minor. P4:108 may edit doctor.py, and P4:113 runs no doctor test.
- C-010: minor. P4:116's forward reference can be checked with `git diff` instead.
- C-011: drop. It is a defect in the reviewers' coverage matrix, not in the plan.
- X-001: MEDIUM, as for C-001.
- X-002: MEDIUM, as for C-002.
- X-003: under these grades there is no blocking defect. V1's verdict is right, with two MEDIUM warnings.
- X-004: minor. V1 cites P4:87 for the plugin decision, which is at P4:23.
- X-005: minor. V3's "roadmap and tech-research" is the accurate remaining gap once P4:74 is counted. V2 left out tech-research.

### Shared assumptions
- A-001: ACCEPT. S1:223 says verbatim that non-strict T2 fails an unregistered file that holds the old sentence, and that strict is "off in this phase".
- A-002: QUALIFY. Task 1 at P4:41 gates only on stage 3 being complete. That stage 1 and 2 outputs exist (registry, scale-map section, rests_on test) follows only indirectly and is never checked before the first edit. The facts are plan text and must be re-checked when stage 4 runs.
- A-003: QUALIFY. No test has run, and stages 1 to 3 do not exist yet, so nobody can say now whether the run is green. The list at P4:113 also leaves out the doctor tests (C-009), so a green run is necessary but not sufficient.
