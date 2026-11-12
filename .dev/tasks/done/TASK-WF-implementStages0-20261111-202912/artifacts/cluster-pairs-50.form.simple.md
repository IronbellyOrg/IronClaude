# Same problem or not? Plain-language version (50 pairs)

Each pair is two complaints from two different AI reviewers who reviewed the same plan. For each pair, ask: would ONE edit to the plan fix both complaints? If yes, type yes after the colon on the ANSWER line. If no, type no. Change nothing else.

If one complaint lists several problems, answer yes when one of those problems is the other complaint's problem. If you cannot tell, pick the closer answer and add a note on the next line starting with NOTE.

These summaries were written by AI helpers from the full reviews and the linked files. They were told not to hint at an answer. The original wording is in cluster-pairs-50.form.md.


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


## P11

**The setting:** A plan to add new rules text to a shared rulebook for helper agents (the "worker contract"). Reviewers checked whether the plan's tests really cover the new text.
**Files mentioned:** test_worker_contract.py (the automated tests for the rulebook); WORKER-CONTRACT.md (the rulebook itself); the plan's task file.
**Complaint A:** Task 1's check that scans for write commands only looks in three folders, not the rulebook folder, so it checks nothing for the new text. A different test does read every rulebook line and could fail on new text.
**Complaint B:** Task 1 names the write-command tests as proof for the new rulebook text, but those tests never look at the rulebook's folder.
**Where each one points:** Both: the verification line of Task 1 (plan line 35) and the test's list of folders it scans (test file lines 1054-1058).

ANSWER P11: 

## P12

**The setting:** A plan to make a set of static changes to several commands, following a written spec with a list of numbered decisions (D-P1 items). Reviewers checked the plan against the spec.
**Files mentioned:** source.md (the spec the plan implements); brainstorm SKILL.md (brainstorm command instructions); init-lite SKILL.md (init-lite command instructions); the plan's task file.
**Complaint A:** Brainstorm's calls to two other commands pass a flag along. The reviewer reads this as a fair reading of the spec's general rule and says noting it as decision D-P1-4 and in the Task 15 report is enough.
**Complaint B:** Task 8 changes two safety rules in init-lite where the spec names only one. The reviewer says the change is needed but was decided inside a task, not listed among the decisions.
**Where each one points:** A: the spec's general rule (lines 62, 142) and brainstorm's nested calls. B: Task 8 (plan line 169) and init-lite's safety rules.

ANSWER P12: 

## P13

**The setting:** A plan for the second batch of static edits to many commands. The spec asks each command's "artifacts" sentence to say excluded files are "left out (WC-4)", a pointer to a rule in the contract.
**Files mentioned:** source.md (the spec); the plan's task file; coverage-matrix.yaml (the reviewers' coverage table).
**Complaint A:** Only cleanup and improve have tests expecting the phrase "left out (WC-4)". Research, cli-eval and tdd describe exclusions without it. No task assigns the short sentence for reports that say where excluded files went.
**Complaint B:** The spec asks every command's artifacts sentence to point at WC-4. The plan pins that only for cleanup and improve. Tasks 4, 13, 14 use other wording, and the remaining tasks say nothing.
**Where each one points:** Spec line 7 and the test entries for individual commands (plan lines 97, 110, 123; A also cites 248, 261).

ANSWER P13: 

## P14

**The setting:** A plan to close an issue by changing install and update behaviour and the docs. Reviewers checked it against a one-line spec goal.
**Files mentioned:** source.md (the spec goal); the plan's task file; install_user_setup.py (installer code); test_retired_docs_absent.py (checks docs); .pre-commit-config.yaml (commit-time checks).
**Complaint A:** The reviewer's coverage table misses the goal phrase "on every workspace via the installer and update scripts". The reviewer says the plan does cover it (Goal, Task 1, upgrade bullet) and asks for no plan change.
**Complaint B:** The plan does not verify its docs edits. A docs test reads every docs page, and a commit-time formatter runs on installation.md. The reviewer suggests running both.
**Where each one points:** A: the spec goal and plan lines 15, 39, 82. B: the docs edits, the docs test (lines 39-44) and the formatter setting (lines 74-88).

ANSWER P14: 

## P15

**The setting:** A plan to add a "Complexity" field to the issue command. It writes a new request file, complexity-field.json, which has no template. Reviewers checked the plan against the spec and the skill's own rules.
**Files mentioned:** source.md (the spec); SKILL.md (issue skill rules); create.md (create-step instructions); commands/issue.md (command page listing output files).
**Complaint A:** No task names complexity-field.json. No task updates the rule that every output file starts from a template (only clickup.json is exempt), or the command page's Outputs row.
**Complaint B:** complexity-field.json has no template, yet the skill rules and create.md say every output file starts from one. The command page does not list the file, and no task covers it.
**Where each one points:** Skill rule line 52, create.md line 7, command page line 78, spec lines 38 and 80.

ANSWER P15: 

## P16

**The setting:** A plan to change how the ccsession launcher handles a permissions setting. Task 5 rewrites a comment block in the launcher script that the plan says `--help` prints.
**Files mentioned:** ccsession (the launcher script); test_ccsession_tag.py (launcher tests); test_install_ccsession.py (install tests); the plan file.
**Complaint A:** The help function prints the script header only up to a marker line, which is the first line of that comment paragraph. So the paragraph is not printed today. Rewriting it either makes help print the whole script or keeps the new text out of help.
**Complaint B:** The plan says that block is printed by `--help`, but it is not. Reword the marker sentence and help dumps the entire script. Keep it and add text after, and the new text never prints, so the acceptance test fails.
**Where each one points:** Task 5 (plan lines 95-100), the help function (line 1652) and the comment block (lines 109-114).

ANSWER P16: 

## P17

**The setting:** A plan to make the ccsession launcher check a permissions setting. It also adds tests that must fail first against the old launcher. Reviewers checked the plan's tasks and acceptance wording.
**Files mentioned:** ccsession (the launcher script); ccsession-orca (a wrapper that calls it); the plan file; source.md (the spec).
**Complaint A:** Task 4 checks the setting early (line 124), before help and other helper modes run. A bad value makes `--help`, `--list` and similar commands exit with an error. The plan does not say whether that is intended, and the wrapper then shows misleading messages.
**Complaint B:** Task 1 says every test using the setting must fail on the old launcher. One required test would already pass there, and another must fail there, so the criterion cannot be met as written.
**Where each one points:** A: Task 4, launcher lines 121-124 and 1671, wrapper lines 132-249. B: Task 1 (plan lines 36, 39) and launcher line 124.

ANSWER P17: 

## P18

**The setting:** A plan to roll out codegraph (a code-search tool) across commands, following a spec table of rows. Row 40 lists which commands gain codegraph in their tool list.
**Files mentioned:** source.md (the spec with row 40); the plan's task file.
**Complaint A:** Task 7 lists commands/task.md as "metadata only", but row 40 excludes the task command, so what to change there is undefined.
**Complaint B:** Row 40 says six commands gain codegraph, including troubleshoot and reflect. Task 7 names all six but its file list lacks those two commands' files, and Tasks 6 and 10 do not mention row 40.
**Where each one points:** Both: spec row 40 (source.md line 129) and Task 7's file list. A also cites spec line 281; B also mentions Tasks 6 and 10.

ANSWER P18: 

## P19

**The setting:** A plan to rewrite the repository rules in CLAUDE.md so nothing touches the upstream project. Task 3 adds a strict rule, and the plan keeps the old "pre-PR checks" as they are.
**Files mentioned:** CLAUDE.md (the project rules file being edited); the plan's task file.
**Complaint A:** Two kept pre-PR lines (64 and 66) conflict with the new rule: one runs a GitHub command that can reach upstream, and one closes a wrongly aimed PR. No acceptance criterion catches them.
**Complaint B:** Task 3 bans any call that reaches upstream, but check 1 (line 64) runs a GitHub repo lookup that can query upstream. The plan names no fix, and its acceptance check could pass anyway.
**Where each one points:** A: CLAUDE.md lines 64 and 66, plan lines 73-83. B: CLAUDE.md line 64, plan lines 73, 78, 82.

ANSWER P19: 

## P20

**The setting:** A plan to rewrite the repository rules in CLAUDE.md (the project rules file). Task 3 adds wording that no tool call or link may resolve to the upstream project.
**Files mentioned:** CLAUDE.md (the project rules file); the plan's task file.
**Complaint A:** The new "no ... link" wording is ambiguous. CLAUDE.md line 251 already holds a web link to an upstream issue (#419), and the plan does not say whether such links are allowed.
**Complaint B:** The new rule is contradicted by the untouched #419 upstream link at line 251. Task 3 edits only the fork-rule section, so that link stays beside a rule forbidding such links.
**Where each one points:** Both: CLAUDE.md line 251 and the new wording in Task 3 (plan line 73).

ANSWER P20: 


## P21

**The setting:** A plan to tidy up the project's rules file (CLAUDE.md). Task 3 adds a rule that no tool call or link may point at the public upstream project. Reviewers checked the plan against the rules file.
**Files mentioned:** CLAUDE.md: the project's main instruction file, which the plan edits.
**Complaint A:** The new wording "no ... link" is unclear. The rules file still has a note linking to an upstream issue (#419), and the plan neither removes that link nor says it is allowed. The reviewer rates it low severity and leaves the outcome open.
**Complaint B:** The rules file keeps a link to that upstream issue, and Task 3's wording could be read as forbidding it. The reviewer's own recommendation ends in either/or choices.
**Where each one points:** Task 3's wording (plan line 73) and the issue #419 note at CLAUDE.md line 251 (the file has since changed).

ANSWER P21: 

## P22

**The setting:** The same plan to tidy up the project's rules file (CLAUDE.md), with Task 3's new rule about links to the upstream project.
**Files mentioned:** CLAUDE.md: the project's main instruction file, which the plan edits.
**Complaint A:** Task 3 adds a rule against any link that resolves to upstream, but the issue #419 link elsewhere in the file is left untouched. The plan never says what to do about it. The reviewer suggests turning it into plain text or marking it as a harmless historical reference, with a check.
**Complaint B:** The rules file keeps a link to an upstream issue that Task 3's wording may forbid. It is rated low severity and stays a "may".
**Where each one points:** Task 3's scope (plan lines 71-78) and the #419 note at CLAUDE.md line 251.

ANSWER P22: 

## P23

**The setting:** A plan to rename a summary file used by the issue-handling workflow, so its name avoids words the tool blocks for helper agents. Task 3 adds a test that checks written file names against those blocked prefixes.
**Files mentioned:** chains.md: a reference table of command sequences for the issue skill.
**Complaint A:** Line 14 of chains.md contains the text "<REPORT.md path printed by step 1>". The reviewer says the name check passes only because the leading "<" is not stripped, and no test case locks that in. Suggested fix: add a test case showing "<REPORT.md" does not match.
**Complaint B:** Raises the same line 14 text, with the same condition about "<" not being stripped. Suggested fix: add that test case and also write down that "<...>" placeholders are kept as they are.
**Where each one points:** chains.md line 14, and Task 3's new name-check helper (plan lines 68-69).

ANSWER P23: 

## P24

**The setting:** A plan of 66 tasks that updates documentation and test guides for the 5.0.0 release. The source spec asks for checks at the end: a smoke test run, then the full test suite once.
**Files mentioned:** source.md: the spec the plan implements, with the verification rules.
implement.md: the instructions for the command that runs the plan.
**Complaint A:** The spec's closing check (smoke test run, then full "make test") is missing from the plan. Only Task 6 runs a narrower test selection, and Task 26 edits an installed command file with only a sync check.
**Complaint B:** The plan has no "make test" anywhere. The reviewer adds that implement.md says tests are extras and never the pass/fail, and the final review checks the spec, not a test run, so that command cannot be relied on to supply it.
**Where each one points:** Spec lines 47-50; Task 6, Task 26; implement.md line 11 (B only).

ANSWER P24: 

## P25

**The setting:** The same 66-task documentation plan for the 5.0.0 release, and the spec's requirement for a smoke test run followed by a full test run at the end.
**Files mentioned:** source.md: the spec the plan implements, with the verification rules.
**Complaint A:** The closing verification the spec asks for (smoke run, then full "make test") is absent. Only Task 6 runs a narrower selection. Task 26 edits an installed command file with only a sync check. It suggests adding a final task or rule.
**Complaint B:** No task runs "make test", the only test run is Task 6's narrower one, Task 26 has no test run, and nothing is verified after Task 66. It suggests a last task that depends on tasks 1 to 66 and adding the smoke run to Task 26's acceptance check.
**Where each one points:** Spec lines 47-50; Task 6 (plan line 89); Task 26 (plan lines 255-258).

ANSWER P25: 

## P26

**The setting:** A plan to fix wording in the brainstorm command so the nested "analyze" folder is required only when the analyze scan actually ran. It edits three command files, their tests, and a spec file.
**Files mentioned:** test_worker_contract.py: the test file that checks these command files.
orca-worker-contract-spec.md: the contract spec the plan also edits.
**Complaint A:** The owner's core rule (the folder exists only when analyze ran) is checked by no test. Someone could delete that clause and every planned test would still pass. It suggests adding a second exact phrase to Task 3, the expected-text list and the Wave 2A check.
**Complaint B:** The plan does not weigh where the per-command live-check extras belong. The spec defines them in its section 7 acceptance rows, yet Task 6 writes to the section 2.1 bullet. The reviewer notes the 2.1 location is defensible but the plan never records the choice.
**Where each one points:** A: Tasks 3, 4, 5 and the test file (lines 508-509). B: Task 6 and the spec (lines 318-322, 376).

ANSWER P26: 

## P27

**The setting:** The brainstorm wording-fix plan again, now checking its final tasks: Task 5 (a test-count check) and Task 7 (the closing checks on the repository's change list).
**Files mentioned:** test_worker_contract.py: the test file Task 5 changes.
diagnostics.txt: saved state of the repository during the review.
**Complaint A:** Task 5 says there should be "more cases than before", but no starting count is recorded. The edit adds exactly one case, so the implementer should save the before-count first.
**Complaint B:** Task 7's third acceptance rule cannot pass from the start. It wants the change list to show only six files plus this package and nothing changed under the done folder, but 950 staged additions and 3 renames from an earlier package already exist.
**Where each one points:** A: Task 5 (plan line 75) and the test file. B: Task 7's third criterion (plan line 98) and diagnostics.txt lines 3-4.

ANSWER P27: 

## P28

**The setting:** The brainstorm wording-fix plan, with a rule about the exact phrase each command file must contain, and a final check on the repository's change list.
**Files mentioned:** diagnostics.txt: saved state of the repository during the review.
test_worker_contract.py: the test file that checks the phrases.
**Complaint A:** Task 7's third acceptance rule cannot pass from the start. It wants only six files plus this package changed, and nothing under the done folder, but 950 staged additions and 3 renames already exist.
**Complaint B:** The planned phrases are pinned correctly but fragile. "write no nested directory" is not a part of "writes no nested directory", so each file must use its own verb form. The reviewer suggests the shorter shared phrase "no nested directory".
**Where each one points:** A: Task 7's third criterion (plan line 98). B: the phrase lines in Tasks 1 to 5 (plan lines 30, 39, 47, 60, 71) and the test file.

ANSWER P28: 

## P29

**The setting:** A plan to add a "--pipeline" option to the issue-claiming command (worktree, launch and submit steps), built from a design document. Both Phase 1 and Phase 3 ship in one pull request.
**Files mentioned:** source.md: the design document the plan implements.
SKILL.md: the issue skill's main instruction file.
**Complaint A:** The plan's skill edits skip two spots: the file's opening description (which says "then stops") and claim step 6 (the summary stage). The summary would leave out the prompt rendering and where the plan stops. No acceptance check would catch either.
**Complaint B:** The design puts two design-document edits (B2 and B16) in Phase 1, but the plan moves all design-document edits to Task 8 in Phase 3, with no reason stated.
**Where each one points:** A: Task 4 and SKILL.md lines 3 and 87. B: Task 8 (plan lines 139-149) and design section 16 (line 405).

ANSWER P29: 

## P30

**The setting:** The same plan for the "--pipeline" issue-claiming option, compared with its design document.
**Files mentioned:** source.md: the design document the plan implements.
**Complaint A:** The plan lacks the design's first principle: no code, warning, option or text may exist only for projects without Orca (the worktree tool). The reviewer says an earlier review also found this.
**Complaint B:** Task 6 omits three launch-failure details from the design: a note that a hand-started agent is not governed by the hook, a "check Orca" detail on timeout, and "the pending record stays". The test list (LA-3) does not check them.
**Where each one points:** A: the plan's Constraints (lines 17-26) and design line 39. B: Task 6 (plan line 116) and design lines 211-212.

ANSWER P30: 


## P31

**The setting:** A plan to add a shared "worker contract" rules file and update several command and skill files to point at it. Reviewers checked the plan's tasks and their pass/fail checks.
**Files mentioned:** test_worker_contract.py: existing automated tests for the contract
**Files mentioned:** init-lite.md: command file for the init-lite command
**Files mentioned:** SKILL.md (init-lite): the matching skill instructions
**Files mentioned:** return-contract.md: reference file for the workflow skill's result format
**Files mentioned:** the plan file: the task list under review
**Complaint A:** Task 5 checks that the text says the run "exited 0". The reviewer says that check could pass while an older sentence ("succeeded when the audit finished, and failed otherwise") is still there. No current test would notice.
**Complaint B:** The return-contract file never mentions the contract file, so a short note like "WC-4" (a rule number) in it cannot be followed. Nothing in the plan's checks stops the note from using a source-tree path.
**Where each one points:** A: Task 5 and two sentences in init-lite.md (line 92) and its SKILL.md (line 61). B: Task 2 and the comment near lines 43-54 of return-contract.md.

ANSWER P31: 

## P32

**The setting:** A plan for a live test run ("P0") where a worker is started in a throwaway working copy and then cleaned up. Reviewers checked the run steps against the contract rules.
**Files mentioned:** SKILL.md (workflow): instructions for the workflow command
**Files mentioned:** WORKER-CONTRACT.md: rules every worker must follow
**Files mentioned:** orca-capabilities.md: notes on what the Orca tool can do
**Files mentioned:** the plan file: the live-test plan under review
**Complaint A:** At this stage the worker will stage files with a git command, because the workflow instructions tell it to. The plan's comparison step only looks at file paths, and its statement that only creating and removing working copies changes git state is too strong.
**Complaint B:** The plan covers only a failed working-copy setup. A failed worker start, a stalled step, or an unanswered decision question have no stated handling, so the executor may improvise or remove a working copy with a live worker.
**Where each one points:** A: plan lines 22 and Step 6; B: plan line 29 (the skip rule) and its failure handling.

ANSWER P32: 

## P33

**The setting:** A plan to close out an install-related issue by running manual evidence checks in a throwaway home folder under /tmp, without touching the real one.
**Files mentioned:** C-install-surface.md: earlier scan notes with a recommended test recipe
**Files mentioned:** the plan file: the evidence-gathering plan under review
**Complaint A:** The recipe it borrows links to a Node program at a path that does not exist on this machine. Running with a cleared environment also moves the package cache into the throwaway folder. Whether Claude login details are available is unchecked.
**Complaint B:** Nothing in the plan forbids copying login credentials from the real Claude folder into the throwaway one, to make the session part of one check (M1c) work.
**Where each one points:** A: the recipe lines 130-134 of the scan notes and plan line 98. B: plan lines 22 (the never-touch rule) and 100 (the M1c check).

ANSWER P33: 

## P34

**The setting:** A plan to build a large feature from a written design (the "source"). Reviewers checked how faithfully the plan's 20 tasks follow it.
**Files mentioned:** the plan file: the task list under review
**Files mentioned:** source.md: the design the plan implements
**Complaint A:** This is a note that nothing was invented. The reviewer found that anything the plan adds beyond the design is only extra checking, not new features, and recommends no change.
**Complaint B:** Task 20 leaves out the design's step 14 instruction on what to stage. So its check that no `.claude/` file is staged is trivially true, and staging `.dev/tasks` depends on someone remembering.
**Where each one points:** A: four plan lines (176, 245, 270, 285) and design line 1324. B: Task 20 (plan lines 302, 307) and design step 14 (line 1429).

ANSWER P34: 

## P35

**The setting:** The same 20-task plan built from a written design. Reviewers checked it against the design and its test setup rules.
**Files mentioned:** the plan file: the task list under review
**Files mentioned:** source.md: the design the plan implements
**Files mentioned:** commands.py (reflect): code file in the reflect command
**Complaint A:** Leaving out the full test run is allowed by an orchestrator instruction. But line 19 ("the source wins") does not mention that exception, and nothing records the run was skipped. The risk to reflect tests is smaller than claimed.
**Complaint B:** Line 29 drops the design's fixed git author and committer names. Without them, git commit fails in the isolated test setup, which would break four named tests. Task 19 also lacks a "skip if unsupported" clause that Task 10 has.
**Where each one points:** A: plan lines 19, 28 and 169-178; design lines 1408 and 1429. B: plan lines 29, 186 and 291; design line 1316.

ANSWER P35: 

## P36

**The setting:** A plan of 66 tasks to carry out a consolidated plan for a v5.0.0 release (docs and checks). Reviewers checked it against the source plan.
**Files mentioned:** CONSOLIDATED-PLAN.md: the large source plan being carried out
**Files mentioned:** pyproject.toml: the project's package settings file
**Files mentioned:** c-e2e-transcript.txt, DECISIONS.md, RELEASE-READINESS.md: release evidence files
**Files mentioned:** source.md: the brief the plan implements
**Complaint A:** This is a consistency note. The reviewer found the 66 tasks cover all items and the facts they spot-checked were right, and recommends no change.
**Complaint B:** The plan's rules do not restate that two report files must not be written and that no issues are to be filed. The executor reads the consolidated plan, whose section 6 (line 636) tells it to file issues.
**Where each one points:** A: many cited facts across the consolidated plan, transcript and release files. B: the plan's Constraints (source lines 36, 38) and consolidated plan line 636.

ANSWER P36: 

## P37

**The setting:** The same 66-task plan, whose tasks write release documents and a test guide. Reviewers checked task wording against the consolidated plan and a template.
**Files mentioned:** CONSOLIDATED-PLAN.md: the large source plan being carried out
**Files mentioned:** user-test-guide.md: the template for test guides
**Complaint A:** The plan leaves out the A/B/C tier grouping and several header fields (capability, audience, source of truth, estimated time, and a gate for sysops) that the test-guide item requires.
**Complaint B:** For item 6 of one work item (B-W12), Task 37 does not name the four new notes to link. It also runs before Tasks 43-46, which presumably produce those notes.
**Where each one points:** A: consolidated plan line 587, template lines 7-12, and the test-guide tasks (48-65). B: consolidated plan line 481 and Task 37.

ANSWER P37: 

## P38

**The setting:** The same 66-task plan, looking at the order in which tasks run and what each says it depends on.
**Files mentioned:** CONSOLIDATED-PLAN.md: the large source plan being carried out
**Complaint A:** The "depends on" lines do not force the right order for Tasks 37, 47, 66 and a link in Task 1. The order only works if tasks run one after another.
**Complaint B:** Task 37 leaves out item 6 of B-W12 (linking four new notes). It also runs before Tasks 43-46 with no dependency on them, and its check only looks at links within one file.
**Where each one points:** A: Tasks 37, 47, 66 and Task 1's link to the upgrading notes. B: Task 37 and consolidated plan line 481.

ANSWER P38: 

## P39

**The setting:** A plan to add a script that blocks bare `python3` use in commands the assistant runs (a "hook"), with tests, a changelog line and a live check. Reviewers checked Task 1's behavior. No file citations were given.
**Files mentioned:** none cited
**Complaint A:** Task 1 does not say how it treats a command split over lines with a backslash, or wrappers that take options (such as `nice -n` or `sudo -u`). The reviewer expects wrongful blocks and missed blocks. They suggest joining lines first and adding tests.
**Complaint B:** The plan does not guarantee the script never exits with the "block" code on an unexpected error, such as a failure in the JSON tool (jq) or an unset variable. The reviewer wants a block only on a clear positive result.
**Where each one points:** Both point at Task 1, the blocking script's design. A: how commands are split and read. B: its error handling and exit codes.

ANSWER P39: 

## P40

**The setting:** A plan for a "P0" phase that adds a worker contract file, registers it, and runs live smoke checks. Reviewers checked task order and what the checks prove.
**Files mentioned:** test_how_we_work_install.py: tests checking the list of installed core files
**Files mentioned:** install_core.py: code holding the list of known core files
**Files mentioned:** source.md and the plan file: the spec and task list under review
**Files mentioned:** coverage-matrix.yaml: reviewer's map of spec items to tasks
**Complaint A:** Task 4's check runs a test that fails once Task 1 adds the contract file, until Task 3 registers it. Nothing makes Task 3 run before Task 4 (or Task 7). So the check may fail, or a commit may miss the registration.
**Complaint B:** Spec step 7.2 needs a report naming a run longer than the heartbeat interval. Task 8 neither requires nor records one, and the three smoke runs may all be shorter, so that check could pass without being exercised.
**Where each one points:** A: Tasks 3, 4 and 7 dependencies and the registration list. B: Task 8 (plan lines 122-128, Goal line 15) and spec lines 291 and 301.

ANSWER P40: 


## P41

**The setting:** A step-by-step work plan for the first phase of an Orca worker-contract project, checked against its source spec.
**Files mentioned:** the plan (task list); source.md, the spec it implements; coverage-matrix.yaml, reviewers' coverage table.
**Complaint A:** The plan says every common check must pass at the end, but the first two checks only run inside Task 4, and a later task can change things afterward. Another check is never mentioned, and no task writes the final "phase report" or declares the phase passed.
**Complaint B:** One spec step says that if transcripts do not name tool calls, a different source is used and the gap is written down. Task 8 records a yes/no answer but does not carry that fallback into its own steps. The reviewer rates this minor.
**Where each one points:** A: the plan's Goal and the common checks in the spec (spec lines 216, 241). B: spec step 5 (line 291) and Task 8 (plan lines 122, 127).

ANSWER P41: 

## P42

**The setting:** A plan to watch real Claude sessions and report a yes/no result on whether sessions can be told apart (called B-CTX).
**Files mentioned:** launch-job-identity.sh, the helper script that identifies a session; actor-context-probe.sh, an older probe script; review-2.md, an earlier review.
**Complaint A:** Task 7 asks what happens when the process-tree search runs out, but the helper looks up the session directly and does not walk up the tree. Task 8 has no "not applicable" outcome for the earlier findings about that.
**Complaint B:** Task 7 is listed as depending only on Task 5, but its criteria use depth numbers that come from the runs in Tasks 2 to 4.
**Where each one points:** A: Task 7's exhaustion step and Task 8's outcomes. B: Task 7's "Depends on" line (plan lines 99 to 104).

ANSWER P42: 

## P43

**The setting:** The same plan to observe real session behaviour, with a limit of twelve real Claude runs.
**Files mentioned:** launch-job-identity.sh, the helper script that identifies a session.
**Complaint A:** Task 5 has a branch for the case where the helper does not compare boot identity, but the helper does compare it, so that branch can never occur. Editing the copied state file may also make the helper refuse it for file-permission or link-count reasons, not for the edited field.
**Complaint B:** The twelve-run limit is not divided among tasks, and no criterion counts runs or cost. Tasks 2 to 4 may need roughly 9 to 14 runs.
**Where each one points:** A: Task 5 and helper line 234 (also lines 83, 149, 218 to 244). B: the run limit in the constraints and Tasks 2 to 4 (plan lines 22, 44, 55, 66).

ANSWER P43: 

## P44

**The setting:** A plan to roll out an issue-watcher tool: setup documentation and replacing guessed test data with data captured from real runs.
**Files mentioned:** issue-watcher-setup.md, the setup guide for the watcher; source.md, the spec; coverage-matrix.md, reviewers' coverage table.
**Complaint A:** Task 4 says to keep the existing sentence that the scheduler is the owner's choice, but does not say where in the guide that sentence is. The reviewer points to it near line 202 and suggests saying it stays untouched.
**Complaint B:** The spec says to replace every guessed test fixture, but the plan only replaces those that were captured. Task 5's precondition (one capture per fixture) disagrees with its body, which allows missing captures. The coverage table may overstate coverage.
**Where each one points:** A: Task 4's wording. B: spec line 22, Task 5 (plan lines 108 to 110), coverage table row 14.

ANSWER P44: 

## P45

**The setting:** A plan to add unattended-mode behaviour to a set of commands and skills, checked against its spec.
**Files mentioned:** the plan (task list); source.md, the spec; test_worker_contract.py, a test file; SKILL.md for brainstorm, instructions for the brainstorm skill; research.md, the research command's file.
**Complaint A:** Task 14 says one part of the task-builder gate is not run, but not whether the gate's command with its file-changing options still runs. The rest of that gate is left unclear.
**Complaint B:** Brainstorm expects research output in one file location, but the research command writes to a different one, and the plan does not say which is read. The brainstorm table also names a skill that does not exist. The reviewer marks this as inferred.
**Where each one points:** A: Task 14 (plan line 261, spec line 150). B: the research-light arm, brainstorm line 189 and research command line 103.

ANSWER P45: 

## P46

**The setting:** A plan to build a launch-level hook (a guard that checks tool calls in governed Claude sessions), checked against its design document.
**Files mentioned:** the design document (sc-issue-launch-level-hook.md); the plan (task list).
**Complaint A:** Task 9 leaves out one command form that the design's tables list, the superclaude.* form of command. The reviewer's fix is to add it or record why it is left out. The claim is brief.
**Complaint B:** Task 18 counts a hook as "effective" if the exact command is present under both events and hooks are not globally off. A hook whose matcher skips the governed tools, or one that cannot bind, would still pass. The tests only cover missing hooks.
**Where each one points:** A: Task 9 and design lines 102 to 127. B: Task 18 (plan line 291) and design lines 342 to 352.

ANSWER P46: 

## P47

**The setting:** The same launch-level hook plan, checked against its design and a merged requirements file.
**Files mentioned:** merged-requirements.md, the earlier requirements list; the design document; the plan; review.md, a panel review file (missing).
**Complaint A:** Task 12's tests for one group of negative cases (T-REG-3) do not match the module that the requirements file's acceptance map names. The claim is brief; the fix says to use the same module.
**Complaint B:** Task 16 requires regression cases from panel findings F1 to F8, but no readable source defines them. The panel review file it would come from does not exist.
**Where each one points:** A: Task 12 and merged-requirements.md lines 971 to 1108. B: Task 16 (plan line 266) and design line 311.

ANSWER P47: 

## P48

**The setting:** The same launch-level hook plan: a guard script, its tests and a final full test run.
**Files mentioned:** the design document; the plan; test_launch_job_identity.py and test_freshness_subagent_start_policy.py, existing hook tests.
**Complaint A:** Task 16 writes tests that treat leaks in folders that are not git repositories as expected behaviour. The reviewer suggests marking them as a known gap or expected failure. The claim is brief.
**Complaint B:** Task 22 counts any skipped test as a failure. Existing tests already skip on non-Linux systems and when run as root.
**Where each one points:** A: Task 16 and design lines 133 to 175. B: Task 22 (plan line 349) and skip lines in two existing test files.

ANSWER P48: 

## P49

**The setting:** The same launch-level hook plan, looked at for task order and consistency.
**Files mentioned:** the plan (task list); the design document.
**Complaint A:** Task 1 lets the first layer go ahead while a key question (B-CTX) is still open, and only checks that a verdict document exists. Task 2 uses made-up test data instead of finishing the real observation step (OB-H1) the design requires before building.
**Complaint B:** Task 19 reports a missing second layer (L2) as a status line on a launch that went ahead, but Task 20 refuses the launch in that case. So Task 19's tests describe a state that Task 20 removes.
**Where each one points:** A: Task 1 (plan line 36), Task 2, design lines 359 to 360. B: Tasks 19 and 20 (plan lines 301 to 325) and design line 514.

ANSWER P49: 

## P50

**The setting:** A plan to carry out a large consolidated list of documentation and tooling changes, checked against its source spec.
**Files mentioned:** CONSOLIDATED-PLAN.md, the combined work list; models.py, a session-tag helper that fetches a file; .pre-commit-config.yaml, the repo's pre-commit settings; source.md, the spec.
**Complaint A:** Task 65 names a Python web-server command, which the reviewer says breaks the project's rule to use UV for Python. Also, the fetch code does not check the URL type, so a local file address may already work. The suggested wording is to serve over a local web address only if a file address is refused.
**Complaint B:** The plan's markdown-lint command is worded differently from the spec, but it matches the version pinned in the repo's pre-commit settings. The reviewer's recommendation is that nothing is needed.
**Where each one points:** A: Task 65 (plan line 575), CONSOLIDATED-PLAN.md line 632 and models.py lines 255 to 268. B: the plan's lint step (line 27), pre-commit lines 74 to 77, spec line 48.

ANSWER P50: 

