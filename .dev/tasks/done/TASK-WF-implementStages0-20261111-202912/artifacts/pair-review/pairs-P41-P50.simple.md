# Pairs P41 to P50 (simple version)

Each pair is two complaints from two different AI reviewers who reviewed the same plan. For each pair, ask: would ONE edit to the plan fix both complaints? If yes, type yes after the colon on the ANSWER line. If no, type no. Change nothing else.

If one complaint lists several problems, answer yes when one of those problems is the other complaint's problem. If you cannot tell, pick the closer answer and add a note on the next line starting with NOTE.

These summaries were written by AI helpers from the full reviews and the linked files. They were told not to hint at an answer. The original wording is in cluster-pairs-50.form.md.

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

