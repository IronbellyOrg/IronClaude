persona: analyzer
model_class: sonnet
model: claude-gw-tier1b

## Verdict
The plan has two blocking defects: Task 1's second acceptance line can't be met, and Task 5's `grep` check contradicts an existing pinning test that no stage 4 task updates or runs. Everything else is minor.

## Findings
F1 | MAJOR | blocking true | unpassable-check | Who: the `/sc:implement` executor and QA reader of Task 1. Wrong result: Task 1 acceptance line 2 requires the stage 3 summary to state that an audit window has passed. The stage 3 plan writes that file before the window and says the opposite, and no package edits it afterwards. The run halts at Task 1, or QA passes it on a guess. | citations: .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md:37 "exists and states that one audit window has passed with no revert trigger tripped"; .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:162 "that no revert trigger can be judged until the audit window has run"; same file:158 "State that the audit window runs after this package"

F2 | MAJOR | blocking true | contradiction | Who: the executor of Task 5 and the owner reading a green run. Wrong result: Task 5 acceptance line 89 requires `follow-up candidates` to be gone from `spec-panel.md`, and the plan changes the cadence wording. `tests/skills/test_review_severity_mapping.py` pins that phrase and `once per loop` in the Grading and Verdict bullets of both the source and plugin spec-panel. Task 5 runs only two other tests, and Task 6 runs three that don't include this one. The mapping test stays red, or is silently relaxed, with no task owning its re-pin. The stage 3 plan edits no spec-panel text, and its own acceptance needs this test green with spec-panel unchanged. So stage 4 must make the change. | citations: tests/skills/test_review_severity_mapping.py:58 "otherwise it is Medium (a warning listed under `follow-up candidates`)"; tests/skills/test_review_severity_mapping.py:72 "asks the user once per loop"; src/superclaude/commands/spec-panel.md:259 "a warning listed under `follow-up candidates`"; plan:88 and plan:89

F3 | MINOR | blocking false | other | Who: the executor of Tasks 1 and 3. Wrong result: both tasks name "the allow-list of the stage 3 scan test", but the test holds no list. It reads the "Merge-rule allow-list" section of `refs/scale-map.md`. The test only checks that listed files exist, so a forgotten removal never turns a check red. | citations: plan:33 "remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of the stage 3 scan test"; stage3 plan:144 "The allow-list is read from the \"Merge-rule allow-list\" section of `refs/scale-map.md`"; stage3 plan:149 "a test fails when a file named there does not exist"

F4 | MINOR | blocking false | unpassable-check | Who: a literal-minded QA reader of Task 3. Wrong result: "each file still contains its 'After 2 fix cycles' sentence" fails a case-sensitive grep for the tdd file, which holds only lowercase "after 2 fix cycles". | citations: src/superclaude/skills/tdd/refs/build-request-template.md:125 "Maximum 2 fix cycles - after 2 fix cycles (3 reviews), HALT and escalate"; src/superclaude/skills/tech-reference/SKILL.md:538 "After 2 fix cycles"

F5 | MINOR | blocking false | missing-requirement | Who: the executor of Task 5. Wrong result: acceptance line 89 reaches the FR-8 rule, which is outside the edit list (Grading, Cap and the line 372 sentence). The FR-8 text is also pinned: the mapping test requires "otherwise it is Medium" and "graded like FR-8". A careless fix to this line breaks that pin. | citations: src/superclaude/commands/spec-panel.md:332 "otherwise it is Medium (a warning listed under `follow-up candidates`)"; tests/skills/test_review_severity_mapping.py:101-103; plan:84

F6 | MINOR | blocking false | missing-requirement | Who: the executor of Tasks 1, 2 and 5. Wrong result: pinning tests that cover edited files are never run in stage 4. `test_review_brief_placement.py` requires the plugin rules prompt to be byte-identical to the source, but Task 5 says "edit each file in place and do not copy one over the other". `test_review_prompt_overrides.py` runs only in Task 2, though Tasks 1, 3, 4 and 6 touch files it pins. `test_review_severity_rule.py` pins the digest in the 6 templates and 4 rule prompts and is not named anywhere in the plan. | citations: tests/skills/test_review_brief_placement.py:134 "assert bundled.read_bytes() == RULES_FILE.read_bytes()"; plan:84 "edit each file in place and do not copy one over the other"; tests/skills/test_review_severity_rule.py:181-187 "S1_S3_FILES"; tests/skills/test_review_prompt_overrides.py:283 "assert \"no minimum count\" in flat, rel"

F7 | MINOR | blocking false | missing-requirement | Who: the executor of Task 5. Wrong result: acceptance line 90 expects "the same pointer ... as their source twins". The Task 5 edit text never says to add a pointer to `spec-panel.md`, which has zero references to `sc-review-severity` today. The `pointer-only` check in T3 passes without a pointer, so nothing forces it. | citations: plan:90 "carry the same pointer and ledger sentence"; plan:84; stage1 plan:211 "a `pointer-only` row only once its pointer is present"

F8 | MINOR | blocking false | safety | Who: the owner. Wrong result: the two gate checks sit in Task 1's acceptance lines, which QA reads after the five template edits are on disk. A missing go still halts the run, but only after the edits exist. | citations: plan:33; plan:36 "when the row has none, this check fails and the run halts"

F9 | MINOR | blocking false | other | Who: the QA reader. Wrong result: several acceptance lines pin no content or command. "T1 passes" (plan:39) names no pytest command. "the L1 merge text" (plan:33) is a spec change description, not a sentence, and Task 4's "contain the consumer-line instruction" (plan:73) has no quoted form. This conflicts with the by-content pin rule. | citations: plan:24 "Pins are by content"; plan:73 "contain the consumer-line instruction"; merged-requirements.md:270 "L1 | **[REQ-05]** The consolidator grades by the rule"

## Checked
- The line anchors in Tasks 1, 2, 3 and 5 match the live files:
  - Task 1: agent_template_qa.md 85/158/161/333, agent_template_analysis.md 466, skill_template.md 828, MDTM templates 644 and 655.
  - Task 2: the four rule prompts at lines 11, 27, 27 and 28.
  - Task 3: the tech-reference, readme, operational-guide and tdd merge lines.
  - Task 5: spec-panel 259 to 261 and 372.
- The six stage 4 files in Tasks 1 and 3 equal the six allow-listed stage 4 files (stage1 plan:59, stage3 plan:144).
- 11 files hold "Grade every review finding as blocking or minor", matching the 11 `digest` rows. The plugin tree has no merge-rule phrases and no old definition sentence. `rule.md` is specified without the old sentence (stage1 plan:46), so Task 6's grep (plan:104) can print nothing.
- `task-builder/SKILL.md` holds the cap sentence exactly once, so Task 4's `grep -c` prints 1. `test_task_builder_merge.py` exists. The plugin holds 4 skills, as Task 6 says.
- Task 2 can satisfy `test_review_rules_text.py`: it pins structure and line adjacency, not the Medium wording.
- The ledger go column exists in the stage-requests README, so Task 1's first check (plan:36) is meetable. The package-id cells for stages 1 to 4 are empty today.

## Self-report
confidence: 0.80
reviewer_model_self_report: claude-gw-tier1b (Claude, analyzer persona, read-only)
