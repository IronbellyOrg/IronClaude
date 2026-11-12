# Pairs P31 to P40 (simple version)

Each pair is two complaints from two different AI reviewers who reviewed the same plan. For each pair, ask: would ONE edit to the plan fix both complaints? If yes, type yes after the colon on the ANSWER line. If no, type no. Change nothing else.

If one complaint lists several problems, answer yes when one of those problems is the other complaint's problem. If you cannot tell, pick the closer answer and add a note on the next line starting with NOTE.

These summaries were written by AI helpers from the full reviews and the linked files. They were told not to hint at an answer. The original wording is in cluster-pairs-50.form.md.

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

