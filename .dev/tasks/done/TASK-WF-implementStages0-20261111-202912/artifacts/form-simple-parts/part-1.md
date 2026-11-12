# Plain-language pairs part 1 (P01-P10)

## P01

**The setting:** A plan to fix the brainstorm skill's routing document, which lists what each tier (fallback level) must contain. The reviewers checked the plan's wording against that document.
**Files mentioned:** 
- The plan (Tasks 2 and 7): the document under review; not found on disk now.
- handoff-routing.md: the brainstorm skill's routing reference the plan edits.
**Complaint A:** Task 7 says "do not edit any file" yet saves logs in an artifacts folder, so it should say "no source edits". Task 2 says tier lists "end with" the quality_tier line, but the Tier 2 list actually ends with an Activation bullet.
**Complaint B:** The Tier 2 list ends with the Activation bullet (line 31), after quality_tier (line 30). The plan's check, which counts matching lines, cannot tell if a bullet landed in the wrong list.
**Where each one points:** A: Task 7 wording, Task 2 wording, Tier 2 list ends. B: the Tier 2 list ends, and the plan's counting check.

ANSWER P01: 

## P02

**The setting:** A plan to fix the brainstorm skill, with Task 2 adding a bullet to the Tier 2 section and Task 7 running tests. The reviewers checked which tests Task 7 runs.
**Files mentioned:**
- The plan (Tasks 2 and 7): the document under review; not found on disk now.
- test_codegraph_adoption.py: a test that reads the skill's Tier 2 text.
- test_tier2_tavily_consistency.py: a test that reads the skill file.
**Complaint A:** Task 7's list of tests leaves out two test files. One checks the stretch of text from the Tier 2 heading to "Final fallback", which is where Task 2 adds a bullet. The other reads the skill file.
**Complaint B:** Task 7 skips the first test file, which checks the exact Tier 2 text Task 2 edits and reads three skill files. "Run the affected tests" could pass without running a test that reads the edited text. (The claim text is cut off.)
**Where each one points:** A: Task 7's test list, two test files. B: Task 7's test list, one test file.

ANSWER P02: 

## P03

**The setting:** A plan to fix the brainstorm skill, with Task 2 editing the Tier 2 section and Task 7 running tests. The reviewers checked which tests Task 7 runs.
**Files mentioned:**
- The plan (Task 7): the document under review; not found on disk now.
- test_codegraph_adoption.py: a test that reads the skill's Tier 2 text.
- test_tier2_tavily_consistency.py: a test that reads the skill file.
**Complaint A:** Task 7's "affected tests" list is wrong. It omits two tests that read the edited files, one of which checks text right next to the Task 2 edit. The routing parity test it does run reads none of the edited files.
**Complaint B:** Task 7 skips the test that pins the exact Tier 2 block Task 2 edits and reads three skill files. "Run the affected tests" could pass without running a test that reads the edited text. (The claim text is cut off.)
**Where each one points:** A: Task 7's test list, two missing tests, plus the parity test. B: Task 7's test list, one missing test.

ANSWER P03: 

## P04

**The setting:** A second version of a plan to fix the brainstorm skill, checked against its source document, which lists required corrections (F-2, F-13). Reviewers read Task 7's sentence about what it writes.
**Files mentioned:**
- The plan (Task 7 and constraints): the document under review; not found on disk now.
- source.md: the document the plan implements; not found on disk now.
**Complaint A:** Task 7 says it writes only logs and a status snapshot under the artifacts folder. That is untrue, because the sync command also rewrites ignored copies under .claude. Correction F-13 asks for the literal sentence "writes only the logs", which the plan lacks.
**Complaint B:** The plan reworded the required F-13 sentence to add the status snapshot. The rewording is forced by a file F-2 adds, but no note records the departure. Even the reworded sentence is untrue because of the sync command.
**Where each one points:** A: Task 7's sentence, constraints, source lines on F-13. B: the same sentence, plus source line 53.

ANSWER P04: 

## P05

**The setting:** A plan for live trial runs of a command. Task 1 checks that installed command files match the branch before the trials start. The reviewers checked that check.
**Files mentioned:**
- The plan (Task 1 and its install line): the document under review.
- install_commands.py: the installer code; not found at the cited place by a quick search.
**Complaint A:** Task 1 compares every file in the commands folder with its installed copy. That includes README.md and __init__.py, which the installer never copies. So the install check can never pass, and every live task records "not run".
**Complaint B:** Task 1's comparison covers README.md and __init__.py, which are not installed. The comparison fails, the install line shows FAIL, and all live tasks are marked "not run". It also cites the lines (21, 36) that set that consequence.
**Where each one points:** A: Task 1 install line. B: Task 1 install line, plus the gate lines 21 and 36.

ANSWER P05: 

## P06

**The setting:** A plan for live trial runs of a command. One passage near line 405 explains why a worker's failure to stage the task folder counts as a problem, citing a decision label. The reviewers checked that label against a report.
**Files mentioned:**
- The plan (around line 405): the document under review.
- p1-static-report.md: an earlier report listing the numbered decisions.
**Complaint A:** The plan cites D-P1-5 for "worker did not stage the task folder". D-P1-5 is about skipping a handoff option; the staging rule is WC-9.
**Complaint B:** The plan cites the wrong decision for that line. The requirement itself is right (WC-9).
**Where each one points:** Both point at the plan's line 405 and the decision list in the earlier report, line 29.

ANSWER P06: 

## P07

**The setting:** A plan to add an Orca worktree script and a launch template to the issue skill. An existing test requires every script and template to be listed in the skill's files table, and the reviewers followed the order of tasks.
**Files mentioned:**
- The plan (Tasks 1, 4, 5, 7): the document under review.
- test_issue_protocol.py: the test checking the skill's files table.
**Complaint A:** Task 1 creates the script but its table row arrives in Task 4. Task 5 creates the template but its row arrives in Task 7. The existing test would fail in between, and Tasks 1, 2, 3, 5 and 6 never run the whole test file.
**Complaint B:** Task 1 creates the script with its row only in Task 4, and Task 5 creates the template with its row only in Task 7; the existing test fails in between. Task 1 never runs that test file. Task 5 depends only on Task 1, so it may run before Task 4. The claim text is cut off after that.
**Where each one points:** A: Tasks 1, 4, 5, 7 acceptance lines. B: Tasks 1, 4, 5, 7, and the Task 5 "depends on" line.

ANSWER P07: 

## P08

**The setting:** A plan to add launching of an agent into the issue skill, built from a design document. Task 6 covers the launch step; the reviewers compared it with the design's steps 5 and 6.
**Files mentioned:**
- The plan (Task 6): the document under review.
- source.md: the design document the plan implements.
**Complaint A:** Task 6 leaves out two things from design step 5: on a timeout, the detail must say to check Orca before re-running; and the hand-run command must carry a note that a hand-started agent is not governed by the hook. Test LA-3 checks neither.
**Complaint B:** Task 6 leaves out the hand-run command note, the timeout "check Orca" detail, and step 6's "the pending record stays". Test LA-3 checks none of them.
**Where each one points:** A: Task 6, design step 5. B: Task 6, design steps 5 and 6.

ANSWER P08: 

## P09

**The setting:** A plan to add a new issue command, with a task that edits the guide's table of other commands. The reviewers checked that the plan's tasks can be carried out and pass the existing tests.
**Files mentioned:**
- The plan (Tasks 2, 10, 11): the document under review.
- test_how_we_work_routing_table.py: tests that check the guide's table.
**Complaint A:** Three small gaps. Task 2's "no token" check does not clear the ClickUp token variable. Task 11's diff check fails if the tree holds other tasks' changes. Task 10 does not say the new row must be plain ASCII.
**Complaint B:** Task 10 does not say the new row in the "Other commands" table must be plain ASCII, or that it must not put a non-existent command in backticks.
**Where each one points:** A: Tasks 2, 11 and 10. B: Task 10 only.

ANSWER P09: 

## P10

**The setting:** A plan built from a spec for a command with a dry-run mode and an install step. The reviewers checked whether Task 4's acceptance criteria pin what the dry run shows.
**Files mentioned:**
- The plan (Task 4): the document under review; not found on disk now.
- source.md: the spec the plan implements; not found on disk now.
**Complaint A:** Task 4's acceptance criteria do not separately list what the dry run shows (source URL, effects, index retention) or the explicit notice about installing MCP (tool server) components. The existing "must not change anything" rules do not check those.
**Complaint B:** The dry run's displayed content is only partly locked. Task 4 forbids changes and prompts but does not check the displayed URL, account-wide effects or index retention. It adds that no task is missing and no plan edit is authorized.
**Where each one points:** A: Task 4 acceptance, spec lines 117 and 145. B: Task 4 acceptance, spec line 117.

ANSWER P10: 
