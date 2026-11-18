# Diff Analysis: reviewer-card comparison (stage 3 plan, third review)

## Metadata
- Generated: 2026-11-16T19:25:00Z
- Variants compared: 2 (Variant 1 = reviewer-1 card, analyzer persona, haiku class, calibrated 0.88; Variant 2 = reviewer-2 card, qa persona, opus class, calibrated 0.84)
- Aliases: PLAN = .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md (267 lines); SRC = .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md; SPEC = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md; S0, S1, S2, S4 = the stage 0, 1, 2 and 4 plan files in .dev/tasks/to-do/ (TASK-WF-blockerStage0-20261116-021044, ...Stage1-20261116-030154, ...Stage2-20261116-030156, ...Stage4-20261116-030206); README = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md. Cited line numbers are those the cards gave; an advocate must re-Read before relying on one.
- Total differences found: 25 (structural 1, content 13, contradictions 3, unique 8; shared assumptions 3, counted separately)
- Convergence denominator: S + C + X + A = 1 + 13 + 3 + 3 = 20

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Card structure | Deviation table with a category (all "Drift"), 2 findings both marked blocking, an adherence summary | Plain numbered findings F1 to F10 (3 marked blocking), "Checked and sound" list | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Status of the earlier three blocking findings | F1, F2, F3 fixed in text; one residual outcome-word gap | F1 fixed with a residual (fix pass, V2 F5), F2 fixed in text but creates a new defect (V2 F1), F3 fixed in text but acceptance lines vacuous (V2 F2) and other lines unedited (V2 F3) | Medium |
| C-002 | Outcome words of the seeded-recall lines at small n | V1 F1 (blocking): R1b is "never advisory" (PLAN:91) but PASS needs the class at or above its minimum n (PLAN:96); the stage 0 plan calls an undersized class the expected outcome (S0:106), so R1b has no successful word | V2 F4 (non-blocking): R3 has no minimum n (S0:106 names min n for gating classes only) and will likely read NOT-MEASURABLE; no mention of R1b | High |
| C-003 | Found threshold when the two arms have different numbers of valid reviewers | Treats the Task 3 threshold as fixed (earlier F2 "fixed") | V2 F1 (blocking): 2 of 3 for the old arm against 2 of 2 for the new arm (PLAN:82) is a panel-size artifact of about 16 points at p=0.9; can fail R2a/R2b or pass R3 | High |
| C-004 | Task 5 acceptance line names the command `verify` | V1 F2 (blocking): the command is registered as `verify-citations` (verify_cmd.py:76) so a literal `verify` check cannot pass | Not raised | Medium |
| C-005 | Positive grep acceptance lines of Tasks 6 to 8 | Says the zero-count removal checks hold and the digest has no "claim is blocking" | V2 F2 (blocking): "stays open for verification", `consumer-unknown` and the cap sentence are in the digest the same task inserts (SPEC:199, SPEC:201, SPEC:213), so those lines pass without the rewrite | Medium |
| C-006 | Other lines in rf-qa-qualitative.md that grade by label or by doubt | Both agents' doubt lines are explicitly rewritten (earlier F3 fixed); no further audit re-pin needed | V2 F3 (blocking): lines 593, 611, 616 (AX-2 "Severity floor: IMPORTANT", "cf. Critical Rule #6") and 918 ("Must resolve ALL CRITICAL and IMPORTANT issues") are not in Task 8's list and match none of the S0 freeze patterns | High |
| C-007 | Can a fix pass of Task 6 leave the edit in the tree after a failed gate | Task 6 checks the gate before editing (fixed) | V2 F5 (non-blocking): the one fix pass (SKILL.md:145) may edit pragmatic.md to satisfy the failing digest lines | Medium |
| C-008 | Coupling of the Rule 6 rewrite to stage 4 | Stage 4 continuation agrees | V2 F6 (non-blocking): S4 reads the bold words of the Rule 6 line; Task 8 does not require the form to be kept | Low |
| C-009 | Completeness of the coverage matrix | Not discussed | V2 F7 (non-blocking): matrix lacks rows for SRC:12, :13, :14 and the F10, F13, F14, F16 bullets; each checked by hand and covered | Low |
| C-010 | Task 6 wording "the two listed below" | Not discussed | V2 F8 (non-blocking): three test files are listed (PLAN:142, PLAN:152) | Low |
| C-011 | Scan breadth of the merge-rule test (Task 13) | Not discussed | V2 F9 (non-blocking): the plan scans six `src/superclaude` folders and `plugins/superclaude`; SPEC:920 says `src/` or `plugins/` | Low |
| C-012 | Task 7 L1 text and acceptance lines for rf-qa.md 389 and 476 | Not discussed | V2 F10 (non-blocking): lines 389 and 476 have no acceptance line; the L1 sentence omits the `reasked` flag and "label stands, listed first" (SPEC:270) | Low |
| C-013 | T1 observation O4 (Task 10 `git diff` acceptance lines read other stages' uncommitted edits) | "Inaccurate: those commands omit HEAD"; no inevitable failure | "Does no harm: stage 2's paragraphs are checked free of those words (S2:122)" | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Is an outcome-word hole at small n blocking? | R1b's missing PASS at an undersized class is blocking (V1 F1) | The same class of hole for R3 (no minimum n) is non-blocking (V2 F4); R1b not mentioned | Medium |
| X-002 | Is the seeded-recall threshold rule sound? | Sound (earlier F2 "fixed for the reported variant and reduced-panel defects") | Unsound: unequal panel sizes bias the arms (V2 F1, blocking) | High |
| X-003 | Does a lines-level contradiction remain in the qualitative agent? | None beyond what Task 8 lists; "no additional mandatory re-pin" | Four unedited lines contradict the rewritten Rule 6 and the digest (V2 F3) | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Links the R1b hole to the stage 0 plan's statement that an undersized set is the expected outcome (S0:106) | High |
| U-002 | 1 | Command-name mismatch `verify` against `verify-citations` (verify_cmd.py:76) | Medium |
| U-003 | 1 | Cross-stage check that stage 1, 2 and 4 agree with the stage 3 consumers (registry states, allow-list, kept-gates section, plugin position) | Medium |
| U-004 | 2 | Panel-size arithmetic for unequal valid-reviewer counts | High |
| U-005 | 2 | Vacuity of the positive grep lines (digest supplies the matched phrases) | Medium |
| U-006 | 2 | Four unedited label-floor and resolve-all lines in rf-qa-qualitative.md | High |
| U-007 | 2 | Fix-pass leak at Task 6; Rule 6 form dependency of stage 4; scan breadth; L1 completeness | Low |
| U-008 | 2 | Check that no fixture row pins the lines Tasks 6 to 8 rewrite, and that the Critical Rules window hash ends before Rule 6 | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The plan runs through `/sc:implement` in order with the stage 0, 1 and 2 outputs present as their producing plans describe (none has run), and with one fix pass per task (SKILL.md:145) | Both cards judge gates and acceptance lines as if run that way | Medium | UNSTATED |
| A-002 | An owner ruling on a non-PASS line is an acceptable continuation, so a gate that needs a ruling in an expected case is a design cost and not a defect | Both cards treat "halts for the owner's Ruling" as the plan's intended exit | Medium | UNSTATED |
| A-003 | The earlier review's F4 to F16 are fixed as the plan's revision notes say | Both cards report F4 to F16 as fixed or addressed in text | Low | STATED |

## Summary
- Total structural differences: 1
- Total content differences: 13
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0); the two UNSTATED ones are promoted as A-001 and A-002 for debate
- Highest-severity items: C-002, C-003, C-006, X-002, X-003, U-001, U-004, U-006
