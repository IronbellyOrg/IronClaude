# Round 2 rebuttal: Advocate for Variant 1 (analyzer, sonnet class)

Debate: reviewer-card comparison for the stage 4 plan. Keys as in Round 1: P4 = `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md`; S1, S3 = the stage 1 and stage 3 plans (`TASK-WF-blockerStage1-20261116-030154`, `TASK-WF-blockerStage3-20261116-030158`); OLD = `TASK-WF-loosenBlockerRev-20261115-210254`; SPEC = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`; MAP = `tests/skills/test_review_severity_mapping.py`.
Grading rule: blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format; drop = not a defect of the plan.
Every line number below was re-read or re-run in this round (2026-11-16).

## 1. Settling C-002 with evidence

### 1.1 What S3 Task 8 says and what it can do

- S3:122 (Task 8) names `test_review_severity_mapping.py` once, with one clause: "the Medium and cadence pins move from 'once per loop' to the once-per-run wording and to assertions on `refs/rule.md` and `refs/scale-map.md`". It does not name spec-panel, `follow-up candidates`, `SPEC_PANELS` or lines 58, 71, 72.
- S3:125 (acceptance): the seven-test run, MAP included, must pass.
- S3:127 (acceptance): "No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text." This is the only rule in S3 that licenses changing a pin, and it speaks of a pin that has "changed", that is, one whose text moved.
- Stage 3 may not touch spec-panel text: `stage-requests/stage3-request.md:20` and `TASK-WF-blockerStage3-20261116-030158/source.md:20` both say "No template, rule-prompt, builder, researcher or spec-panel edit (stage 4)". My grep of S3 for `spec-panel|once per loop|follow-up candidates` finds hits only on three lines (S3:21, S3:59, S3:122), all about `pragmatic.md` or this test sentence; no S3 task has a spec-panel file in its edit list.
- So at S3 exit `src/superclaude/commands/spec-panel.md:259-260` and `plugins/superclaude/commands/spec-panel.md:257-258` (and FR-8 at :332 and :330) still hold the three `follow-up candidates` matches and the verdict bullet's "once per loop" (grep, this round).

### 1.2 What the test pins today (lines 24-27, 50-76, 117-137)

| MAP line | Literal | File it reads | Text changed by stage 3? |
|---|---|---|---|
| 58 | `otherwise it is Medium (a warning listed under `follow-up candidates`)` | both spec-panels, Grading bullet | no |
| 71 | `` `follow-up candidates` `` | both spec-panels, Verdict bullet | no |
| 72 | `asks the user once per loop` | both spec-panels, Verdict bullet | no |
| 128 | `asks the user once per loop whether to open an issue` | `pragmatic.md` | yes (S3:59 moves its Medium and spec-panel bullets into the rule) |

A grep of the whole `tests/` tree for `follow-up candidates|once per loop` returns exactly these four lines plus the module docstring (MAP:6). No other test pins them. So MAP is the single place the question lives, and S3 Task 8 is the single place that could move them before stage 4.

### 1.3 The spec's own text (the only evidence that line 72 moves at stage 3)

- SPEC:323: "the output-style ask applies only at gates with no carrier offer, and the two test pins on that text move at stage 3".
- SPEC:900 (section 11.1 row for MAP): "including 'asks the user once per loop whether to open an issue' (lines 72 and 128 [V, this merge]); spec-panel literals in `src` and `plugins`"; Change column: "the cadence pins move at stage 3 (section 6.1 step 6); literals move to assertions on `refs/rule.md` and `refs/scale-map.md`; add ledger and offer pins".
- SPEC:1150 (MC-05): grep of MAP for `once per loop` gave "lines 72 and 128".
- The spec therefore calls lines 72 and 128 "the two test pins on that text" (the output style's ask). That is a mislabel: line 128 reads `pragmatic.md`, but line 72 is a `SPEC_PANELS` assertion on the Verdict bullet (`MAP:67-76`). The "literals move" clause has no stage date; SPEC:739 and SPEC:948 put the spec-panel text change itself at stage 4 ("the spec-panel narrowing"; "its `follow-up candidates` list becomes the ledger").

### 1.4 Decision

After stage 3 is done as S3 reads:

1. **`follow-up candidates` (MAP:58, :71), source and plugin: still asserted.** Nothing in S3 reaches them. They are Medium-wording pins, not cadence pins; S3:127 licenses changing only a pin whose text changed; and spec-panel text does not change at stage 3. The only route to dropping them is reading "Medium ... pins move ... to assertions on `refs/rule.md`" as covering spec-panel literals, which the S3 sentence does not say and which would delete a pin on unchanged text, against S3:127. P4:89 targets exactly this phrase. This part of C-002 I would put at about 80 percent likely to hold.
2. **`asks the user once per loop` (MAP:72), source and plugin: probably still asserted, less sure.** SPEC:323/:900/:1150 make an S3 executor think line 72 is one of "the two" cadence pins to move. But S3 cannot move it to once-per-run wording on spec-panel without failing S3:125 (spec-panel is unchanged), so the executor's only options are to leave it or to delete it and assert something on `refs/rule.md`/`refs/scale-map.md` instead. Either passes S3:125. I cannot rank them from the text alone; I put "still asserted after S3" at about 60 to 65 percent.
3. Whichever branch holds for line 72, P4:89 requires `follow-up candidates` to be gone from `spec-panel.md` (and Task 5 applies the same edits to the plugin twin, P4:84). In the 80 percent branch that fails MAP:58 and :71 in 4 parametrized cases (2 tests x 2 files), and P4 runs MAP nowhere (pytest lines at P4:41, :55, :63, :74, :88, :102; none names it). The package then closes with every acceptance line green and a red test in `tests/skills/`.

### 1.5 Reply to Advocate 2

Advocate 2 writes that "S3:122,125,127 migrates/replaces those pins before entry" and that C-002 should be a conditional re-check. The text does not support "migrates". S3:122 never mentions spec-panel; S3:127 binds changed pins only, and no spec-panel pin has changed by then. A compliant S3 may remove the spec-panel literals ("possible", as Advocate 2 says), but it is not told to, and the sentence that would license it contradicts S3:127. Where Advocate 2 is right: the dependency is conditional on S3, and the correct finding is "no stage 4 task owns or checks the re-pin". I accept that wording, and keep the grade, because the missing check is a "missing result" under the grading rule in the more likely branch.

### 1.6 What remains uncertain

- Stage 3 has not run. `TASK-WF-blockerStage3-.../artifacts/` holds only `codegraph-grounding.md`; `git diff HEAD` shows no change to MAP; `src/superclaude/skills/sc-review-severity/` does not exist yet. The decision rests on plan text, not on an executed re-pin.
- How an S3 executor reads "cadence pins" for line 72 (see 1.4 point 2), and whether S3 or SPEC 11.1 is revised before it runs (Round 1 A-001, QUALIFY).
- The base plan has the same gap: OLD Task 45 (OLD:531-541) removes `follow-up candidates` and runs only two other tests, and OLD Task 38 (OLD:451-458) is the same sentence as S3:122. So this is inherited from the 46-task plan, not new in the split; it was not caught there either.
- Suggested fix (either branch): Task 5 states which MAP pins it re-pins (lines 58, 71, and 72 if still present, on both files) and adds MAP to the P4:88 run and to the P4:102 run.

**Final grade for C-002: blocking** (qualified as above).


## 2. Criticisms of Variant 1 in Round 1, answered

| # | Criticism (who) | Answer |
|---|---|---|
| 1 | F2/C-002 overstates certainty; a compliant stage 3 may already have removed the pins (Advocate 2, Advocate 3) | Accepted in part. The "stays red" half of V1's sentence is conditional and V1 did not state the S3 dependency. Section 1 now states it and splits the phrase: `follow-up candidates` pins are about 80 percent likely to survive S3, the line 72 cadence pin about 60 to 65 percent. The "silently relaxed" half and the missing owner and missing run are not conditional: P4 never names MAP. Grade stays blocking. |
| 2 | F5/C-005 is a sub-case of F2 (Advocate 3) and the FR-8 pins do not name the phrase (my own Round 1 concession) | Agreed. FR-8 pins (MAP:101-103) need "otherwise it is Medium" and "graded like FR-8", which survive deleting the parenthesis at `spec-panel.md:332` (plugin :330). It is the same file-wide grep (P4:89) reaching one more line outside the edit list (P4:84). Fold under C-002; stand-alone grade minor. |
| 3 | F6/X-002: byte identity is reachable by applying the same edits (Advocate 2) | Agreed that it is reachable. `cmp` of the source and plugin `document_review_loop_prompts.md` prints nothing (identical today), and MAP-adjacent `test_review_brief_placement.py:134` asserts `bundled.read_bytes() == RULES_FILE.read_bytes()`. Task 2 edits the source twin (P4:50), Task 5 edits the plugin twin (P4:84), and no P4 pytest line runs the placement test. The result is right if the executor reapplies Task 2's edit exactly; nothing checks it. Minor, merged into C-006. The wording "edit each file in place and do not copy one over the other" is written for the spec-panel pair that differs; for the identical prompt pair a copy would be the safe move, so I note it as a trap but not a defect. |
| 4 | F3, F4, F9 depend on a literal-minded QA reader (Advocate 2, Advocate 3) | Agreed; all three stay minor. For F4 I re-ran the count: `grep -c "After 2 fix cycles"` gives tech-reference 2, readme 6, operational-guide 2 and `tdd/refs/build-request-template.md` 0. The tdd file holds "Maximum 2 fix cycles — after 2 fix cycles (3 reviews), HALT and escalate ..." at line 125, so P4:64 is false only under a case-sensitive read. P4:24 pins by content. |
| 5 | F8/C-008: gate check read after the edits (Advocate 3 "minor at most") | Agreed. Edits are on disk but uncommitted, the run still halts at P4:36, and the ledger gate is a chat message outside the package (`stage-requests/README.md:3` and :25, "Gates (F1, F8). No gate task"). Minor. |
| 6 | V1's "Checked" section did not cover the Task 6 walk, the base-task comparison or the tracked-files scan | Conceded in Round 1 and unchanged. Those are V2 and V3 contributions and the merge should take them (C-013 minor, U-003, U-004, U-006). |
| 7 | V1's F7/C-007 asks for a pointer the edit text never mentions | Not criticised in Round 1; I re-checked it this round. See 4.2: it is a little wider than V1 wrote. |

## 3. Updated final grades

"Round 1" lists my grade, Advocate 2's and Advocate 3's in that order. "Final" is the grade I now put forward. Unchanged points where all three agreed are not repeated except where the task list asked.

| Point | Round 1 (A1 / A2 / A3) | Final | Changed? | Evidence |
|---|---|---|---|---|
| C-001 | blocking / blocking / blocking | blocking | no | P4:37 against S3:158 and S3:162; Task 11 of S3 is the only writer of the summary. |
| C-002 | blocking / minor / blocking | **blocking** | no (reasoning refined) | Section 1. |
| C-004 | minor / minor / minor | minor | no | `tdd/refs/build-request-template.md` has 0 matches for capital "After 2 fix cycles" and lowercase "after 2 fix cycles" at :125 (grep, this round); P4:24 pins by content. |
| C-005 | minor / minor / minor | minor, fold under C-002 | no | Section 2 row 2. |
| C-006 | minor / minor / minor | minor | no | No P4 pytest line names `test_review_severity_rule.py`, `test_review_brief_placement.py` or (after Task 2) `test_review_prompt_overrides.py`; no failure is demonstrated. |
| C-007 | minor / minor / minor | minor | no (evidence widened, 4.2) | `spec-panel.md` and its plugin twin hold 0 references to `sc-review-severity` (grep, this round). |
| C-010 | minor / **drop** / minor | **drop** | **yes, minor to drop** | See 3.1. |
| C-011 | **drop** / minor / minor | **minor** | **yes, drop to minor** | See 3.2. |
| C-012 | **drop** / minor / minor | drop | no | The matrix is a reflect-run artifact (`.dev/reflect/.../artifacts/coverage-matrix.yaml`), not part of the plan; P4:19 implements the sentence. V2's own text: "a matrix omission, not missing implementation scope". Advocates 2 and 3 grade the matrix, I grade the plan. |
| C-013 | minor / minor / minor | minor | no | S1:209, `test_review_severity_rule.py:39`, no staging step in P4:99-105. |
| C-014 | minor / minor / minor | minor | no | S1:96 and `stage-requests/README.md:27` themselves say stage 4 "adds its plugin mirror". |
| C-015 | minor / **drop** / minor | **drop** | **yes, minor to drop** | See 3.3. |
| S-001 | **drop** / minor / drop | drop | no | Card layout only; the saved V2 card is already normalised to D1 to D4 (variant-2-original.md:6). |
| S-002 | minor / minor / minor | **drop** | **yes, minor to drop** | See 3.4. |
| X-001 | **drop** / drop / **blocking** | **drop as a separate point; the weight sits on C-002** | no | See 3.5. |
| X-002 | minor / **drop** / minor | minor, merged into C-006 | no | Section 2 row 3. |
| X-003 | minor / drop / drop | **drop** | **yes, minor to drop** | Same defect as S-002, counted twice. |

### 3.1 C-010 (plan generated before its preconditions hold): minor to drop

- Facts re-read: `stage4-request.md:3` "Generate it only after the stage 3 package is done ..."; `stage-requests/README.md:9` "Generate a stage's package only after the owner's go for it"; ledger rows for stages 1 to 4 have empty Package id and Owner go cells (`README.md:18-21`).
- Why drop: no edit to the plan text can fix when the plan was generated; the plan carries the same gate at run time (P4:20, P4:36) and fails closed; and I cannot tell from the files whether the owner asked for all five packages at once (the five packages are stamped within 12 minutes of each other, `030154` to `030206`). The README's "Decision (owner, 2026-11-16)" at :3 names the one-package-per-stage design, not the generation order. Without a provable instruction breached, the plan itself has no wrong result. I keep it as a process note for the orchestrator, outside the finding list. Moving from minor to drop is a change of mind from Round 1; Advocate 2 argued it and the lack of any in-plan fix decides it.

### 3.2 C-011 (Task 2 has no cap-sentence acceptance line): drop to minor

- `stage4-request.md:12` (the request's "Rule prompts ..." bullet) says "the cap sentences kept by content"; Task 3 (P4:64) and Task 4 (P4:75) each carry an explicit cap line; Task 2 (P4:53-55) does not.
- My Round 1 reason (T1 equality pins the cap because the digest ends with it, S1:50) still holds and Task 2 runs the registry test (P4:55), so no cap content can be lost without a red test. Each of the four rule prompts holds exactly one `fix cycles` line today; `document_review_loop_prompts.md` holds none (grep, this round).
- But the request asked for an explicit by-content keep, two sibling tasks have it and this one does not. That is a small, real wording gap in the plan, so minor and not drop.

### 3.3 C-015 (Task 4's consumer line could land inside a digest fence): minor to drop

- New evidence: the digest in the MDTM templates sits in the QA verdict block `I16. QA GATE VERDICT AND FIX CYCLES` (`01_mdtm_template_generic_task.md` about lines 644-660: "Grade every review finding as blocking or minor ..." directly under the I16 heading). P4:70 puts the consumer line on each phase output ("feeds item X, reads column Y"), not into the verdict block.
- Even in the bad case, P4:102 runs `test_review_severity_registry.py` (T1) before the package closes, so the error is seen inside the package. No wrong or missing result follows; the earlier signal would only be more convenient. Advocate 3 had already said "speculative". Drop.

### 3.4 S-002 and X-003 (V2's two labels per row): minor to drop

- Both points are about a property of V2's card, not of the plan under review, and the grading rule grades plan defects. S-001 (card layout) is dropped on the same ground, so keeping S-002 as a minor would be inconsistent.
- The conflict that matters to the merge is resolved once every point is graded by the rule: V2's D2 is C-001 (blocking), V2's D1 is C-010 (drop). The "MEDIUM" column never has to be consulted. X-003 is the same defect as S-002 counted twice. If the merger keeps a section on card quality, minor is the fallback for S-002 only.

### 3.5 X-001 (can Task 5 leave the package with a red test): resolved, not a separate finding

- The three statements are about different objects: V1 F2 is about the mapping test no stage 4 task runs; V2's note ("No later task here falsifies an earlier task's stated acceptance line", variant-2-original.md:55) is about acceptance lines; V3's "Step 7: no failure expected apart from F2 and F3" (variant-3-original.md:27) is about the three tests named at P4:102. All can be true together.
- The question they point at is C-002, where V1 is right on the evidence in section 1. I do not grade X-001 twice; Advocate 3's "blocking" for X-001 is the same weight as C-002 and should not be added on top of it.

## 4. New evidence from this round

### 4.1 The gap pre-dates the split

`OLD` Task 45 (OLD:531-541) has the same edit text and the same acceptance line "`grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` prints nothing" with only `test_spec_panel_review_loop.py` and `test_review_loop_extension.py` run; OLD Task 38 (OLD:451-458) holds the S3:122 sentence word for word. The split copied both. The earlier review of OLD (`.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md`) is not re-read here, so I do not claim it did or did not list this gap.

### 4.2 C-007 is wider than V1 wrote

P4:90 has two requirements: "the same pointer and ledger sentence" in the plugin twins, and "a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`". Task 5's edit text (P4:84) says nothing about a pointer in `spec-panel.md` (0 references today, both copies), and my grep of S1 for `parity|twin` finds no line; so no task writes the second requirement either. Task 6 adds `tests/skills/test_review_severity_plugin_parity.py` (T15), but that is a different file and covers the skill folder, not the spec-panel twins. An executor who infers both clauses can meet them, so it stays minor; the same line is in OLD:541, so it is inherited.

### 4.3 The mapping test is the only test that pins these phrases

`grep -rn "follow-up candidates\|once per loop" tests/` returns only MAP:6, :58, :71, :72 and :128. Tasks 5 and 6 can therefore be made safe by naming that one file. I checked `test_spec_panel_review_loop.py` and `test_review_loop_extension.py` (the two tests Task 5 does run): neither pins `follow-up candidates` or "once per loop", so P4:88 will pass over a red MAP. That is the exact mechanism by which acceptance stays green while the repo is red.

## 5. Summary for the merge

- Blocking: C-001, C-002.
- Minor: C-003, C-004, C-005 (under C-002), C-006 (with X-002), C-007, C-008, C-009, C-011, C-013, C-014.
- Drop: S-001, S-002, X-001 (as a separate point), X-003, C-010 (process note only), C-012, C-015.
- Assumptions to state in the merged review: the plan text of S1 and S3 is the contract (A-001); C-002 holds under S3 as it reads now and should be re-checked if S3 Task 8 or SPEC 11.1 is revised before stage 3 runs.

**My final grades for the two points asked: C-002 blocking; C-010 drop.**
