# Pairs P01 to P10 (detail version)

For each pair, read complaint A and complaint B. They come from two different reviewers of the same plan.
Question: would ONE edit to the plan (or spec) fix both complaints? If yes, they are the same problem.
Write yes or no after the colon on the line that starts with ANSWER. Do not change anything else.
If one complaint lists several problems, answer yes when one of those problems is the other's problem.

## P01

A (reviewer-1-card, finding R1-10): Task 7 says 'do not edit any file' but saves logs under ./artifacts/ (say 'no source edits'). Task 2 says tier lists 'end with' the quality_tier line; the Tier 2 list ends with the Activation bullet (confirms F-2).
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:39-39 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:93-93 ; source handoff-routing.md:30-31

B (reviewer-2-card, finding R2-6): Confirms F-2: the Tier 2 list ends with the Activation bullet (line 31) after quality_tier at line 30; the grep -c criterion cannot detect a bullet placed in the wrong list.
   points at: source handoff-routing.md:22-22 ; source handoff-routing.md:30-31 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:39-39 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:42-42

ANSWER P01:

## P02

A (reviewer-1-card, finding R1-7): Task 7's pytest set omits tests/skills/test_codegraph_adoption.py (its Tier 2 slice test runs from the Tier 2 heading to `**Final fallback`, exactly where Task 2 inserts a bullet) and tests/skills/test_tier2_tavily_consistency.py (reads the SKILL).
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:93-93 ; source test_codegraph_adoption.py:75-82 ; source test_codegraph_adoption.py:141-143 ; source test_tier2_tavily_consistency.py:40-53

B (reviewer-3-card, finding R3-2): Task 7 skips tests/skills/test_codegraph_adoption.py, which pins the exact Tier 2 block that Task 2 edits (slice from the Tier 2 heading to `**Final fallback`) and reads SKILL.md, src brainstorm.md and the plugin brainstorm.md. 'Run the affected tests' can pass without running a test that reads t...
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:93-93 ; source test_codegraph_adoption.py:20-23 ; source test_codegraph_adoption.py:75-82 ; source test_codegraph_adoption.py:115-132

ANSWER P02:

## P03

A (reviewer-2-card, finding R2-5): Task 7's 'affected tests' set is wrong: tests/skills/test_codegraph_adoption.py (reads SKILL.md, handoff-routing.md, commands/brainstorm.md; Tier 2 span test at line 75 borders the Task 2 edit) and tests/skills/test_tier2_tavily_consistency.py (reads SKILL.md) are absent. test_routing_plugin_pari...
   points at: source test_codegraph_adoption.py:20-23 ; source test_codegraph_adoption.py:75-83 ; source test_tier2_tavily_consistency.py:19-19 ; source test_tier2_tavily_consistency.py:49-49 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:93-93

B (reviewer-3-card, finding R3-2): Task 7 skips tests/skills/test_codegraph_adoption.py, which pins the exact Tier 2 block that Task 2 edits (slice from the Tier 2 heading to `**Final fallback`) and reads SKILL.md, src brainstorm.md and the plugin brainstorm.md. 'Run the affected tests' can pass without running a test that reads t...
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:93-93 ; source test_codegraph_adoption.py:20-23 ; source test_codegraph_adoption.py:75-82 ; source test_codegraph_adoption.py:115-132

ANSWER P03:

## P04

A (reviewer-1-card, finding A-4): Task 7 says it 'writes only the logs and the status snapshot under ./artifacts/'. False as written, because make sync-dev rewrites the gitignored .claude/ copies (the plan's own Constraints say so). Correction F-13's verifier requires the literal sentence 'it writes only the logs under ./artifact...
   points at: plan TASK-WF-brainstormFixBri-20261106-021737.md:21-21 ; plan TASK-WF-brainstormFixBri-20261106-021737.md:152-152 ; spec source.md:169-169 ; spec source.md:171-171

B (reviewer-2-card, finding R2-2): Correction F-13's verifier is unsatisfied in form and the departure is unrecorded: plan:152 widens the mandated sentence to 'it writes only the logs and the status snapshot under ./artifacts/'. The widening is forced (F-2 adds status-after.txt, which is not a log), so it is a necessary deviation,...
   points at: spec source.md:53-53 ; spec source.md:169-169 ; spec source.md:171-171 ; plan TASK-WF-brainstormFixBri-20261106-021737.md:21-21 ; plan TASK-WF-brainstormFixBri-20261106-021737.md:152-152

ANSWER P04:

## P05

A (reviewer-1-card, finding 1): cmp of "every file under src/superclaude/commands/" includes README.md and __init__.py, which the installer never copies, so the install line can never pass and every live task records not run: install precondition failed
   points at: source install_commands.py:11-11 ; plan TASK-WF-p1LivePlanBrief-20261105-164506.md:58-58

B (reviewer-3-card, finding 1): cmp of "every file under src/superclaude/commands/" includes README.md and __init__.py, which are not installed; exits non-zero, install line FAIL, all live tasks not run (plan:21, :36)
   points at: source install_commands.py:11-11 ; source install_commands.py:40-40 ; plan TASK-WF-p1LivePlanBrief-20261105-164506.md:21-21 ; plan TASK-WF-p1LivePlanBrief-20261105-164506.md:36-36 ; plan TASK-WF-p1LivePlanBrief-20261105-164506.md:61-61 ; plan TASK-WF-p1LivePlanBrief-20261105-164506.md:58-58

ANSWER P05:

## P06

A (reviewer-1-card, finding 12): extra cites D-P1-5 for "worker did not stage .dev/tasks"; D-P1-5 is about skipping --handoff implement; the staging rule is WC-9
   points at: source p1-static-report.md:29-29 ; plan TASK-WF-p1LivePlanBrief-20261105-164506.md:405-405

B (reviewer-2-card, finding 5): extra cites D-P1-5 for "worker did not stage .dev/tasks"; wrong decision cited, requirement correct (WC-9)
   points at: source p1-static-report.md:29-29 ; plan TASK-WF-p1LivePlanBrief-20261105-164506.md:405-405

ANSWER P06:

## P07

A (reviewer-1-card, finding 1): Existing two-way inventory test is red between tasks: Task 1 creates scripts/orca_worktree.py but its SKILL.md row arrives in Task 4; Task 5 creates templates/launch-prompt.md but its row arrives in Task 7. Acceptance of Tasks 1, 2, 3, 5, 6 never runs the whole file. Confirms T1 F-1.
   points at: source test_issue_protocol.py:131-141 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:41-41 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:62-62 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:75-75 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:106-106 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:30-30 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:95-95 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:86-86 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:130-130

B (reviewer-3-card, finding 1): T1 F-1 confirmed. Task 1 creates the script, row only in Task 4; Task 5 creates the template, row only in Task 7; existing inventory test red in between. Task 1 acceptance never runs test_issue_protocol.py. Task 5 depends only on Task 1, so it may run before Task 4, then Task 4's own acceptance f...
   points at: source test_issue_protocol.py:131-141 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:97-97 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:30-32 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:86-86 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:99-99 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:130-130

ANSWER P07:

## P08

A (reviewer-1-card, finding 9): Task 6 drops two design step 5 instructions: on a timeout detail must say to check Orca before re-running; hand_command must carry the note that a hand-started agent is not governed by the hook. LA-3 has no assertion for them.
   points at: spec source.md:211-211 ; spec source.md:377-377 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:116-116

B (reviewer-3-card, finding 7): Design step 5 hand_command note ('an agent started by hand is not governed by the hook; re-running the claim is preferred'), timeout 'check Orca' detail, and step 6 'the pending record stays' are absent from Task 6; LA-3 does not assert them.
   points at: spec source.md:211-212 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:116-116

ANSWER P08:

## P09

A (reviewer-1-card, finding A-4): Task 2 no_token check does not unset CLICKUP_API_TOKEN; Task 11 git diff --stat check fails on a tree holding other tasks' changes; Task 10 does not say the new row must be ASCII.
   points at: plan TASK-WF-scIssueCommand-20261104-064713.md:49-49 ; plan TASK-WF-scIssueCommand-20261104-064713.md:178-178 ; source test_how_we_work_routing_table.py:341-346

B (reviewer-3-card, finding S-6): Task 10 does not say the new Other-commands row must be ASCII and must not backtick a non-existent /command (test_guide_is_ascii_except_the_ruling_example, test_other_commands_membership_and_live_references).
   points at: plan TASK-WF-scIssueCommand-20261104-064713.md:159-159 ; source test_how_we_work_routing_table.py:341-341

ANSWER P09:

## P10

A (reviewer-1-card, finding G1): Positive dry-run output content and explicit MCP install disclosure are not independently listed in Task 4 acceptance criteria; existing prohibitions alone do not assert displayed source URL, effects and index retention.
   points at: spec source.md:117-117 ; spec source.md:145-145 ; source TASK-WF-spec-20261019-204314.md:111-111 ; source TASK-WF-spec-20261019-204314.md:145-145

B (reviewer-2-card, finding R2-2): Positive dry-run output content from source117 is only partly acceptance-locked; Task 4 explicitly forbids mutation/prompts but does not assert displayed URL, account-wide effects and index retention. Not a missing task; no plan edit authorized.
   points at: spec source.md:117-117 ; source TASK-WF-spec-20261019-204314.md:111-111

ANSWER P10:

