# Plain-language pairs part 3 (P21-P30)

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
