# Same problem or not? (50 pairs)

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

## P11

A (reviewer-1-card, finding R1-3): Task 1 AC3 checks nothing: the write-verb scan walks only skills, commands and agents; core/WORKER-CONTRACT.md already holds unclassified `git add` at :41-42. The test that does read every contract line is _check_repo_setup_gated (test_worker_contract.py:445-461, regex :430-435), which would fail...
   points at: source test_worker_contract.py:1054-1058 ; source test_worker_contract.py:445-461 ; source WORKER-CONTRACT.md:41-42 ; source TASK-WF-workerContractFo-20261106-214402.md:35-35

B (reviewer-2-card, finding QA-2): Task 1 names the write-verb classification tests as verification for new WORKER-CONTRACT.md text, but those tests do not scan core files. Their roots contain only skills, commands and agents.
   points at: source TASK-WF-workerContractFo-20261106-214402.md:35-35 ; source test_worker_contract.py:1054-1058 ; source test_worker_contract.py:1095-1107 ; source test_worker_contract.py:1119-1124

ANSWER P11: 

## P12

A (reviewer-1-card, finding R1-06): Spec 2.1 is general; adversarial and analyze both accept the flag after P1. D-P1-4 is a faithful reading, not creep. Disclosure as D-P1-4 and in the Task 15 report is enough.
   points at: spec source.md:62-62 ; spec source.md:142-142 ; source SKILL.md:273-280

B (reviewer-2-card, finding R2-06): The spec's small fix names Safety Invariant 3; Task 8 amends 2 and 3 because the contract is required on --dry-run. The extension is necessary but is a spec delta decided inside a task body, not in the D-P1 list.
   points at: spec source.md:147-147 ; source SKILL.md:62-63 ; plan TASK-WF-writeTheP1Static-20261105-033458.md:169-169

ANSWER P12: 

## P13

A (reviewer-2-card, finding R2-F3): F1 remains incompletely verified. Only cleanup and improve explicitly add "left out (WC-4)" to their expected phrases; research, cli-eval and tdd describe exclusions but omit that phrase from their test entries. No task assigns the required short local sentence for reports that name where exclude...
   points at: source source.md:7-7 ; source TASK-WF-writeTheP2Static-20261107-011441.md:97-97 ; source TASK-WF-writeTheP2Static-20261107-011441.md:110-110 ; source TASK-WF-writeTheP2Static-20261107-011441.md:123-123 ; source TASK-WF-writeTheP2Static-20261107-011441.md:248-248 ; source TASK-WF-writeTheP2Static-20261107-011441.md:261-261 ; source coverage-matrix.yaml:14-14

B (reviewer-3-card, finding R3-F11): source.md:7 asks each P2 command's `artifacts` clause to point at WC-4 ("left out (WC-4)"); the plan pins it only for cleanup and improve; Tasks 4, 13, 14 use other wording and the rest say nothing.
   points at: source source.md:7-7 ; plan TASK-WF-writeTheP2Static-20261107-011441.md:97-97 ; plan TASK-WF-writeTheP2Static-20261107-011441.md:110-110

ANSWER P13: 

## P14

A (reviewer-2-card, finding R2-F2): Matrix misses the goal span 'on every workspace via the installer and update scripts'; the plan covers it (Goal plan:15, Task 1 rationale plan:39, upgrade bullet plan:82).
   points at: spec source.md:1-1 ; source TASK-WF-closeIronbellyOr-20261104-124207.md:15-15 ; source TASK-WF-closeIronbellyOr-20261104-124207.md:39-39 ; source TASK-WF-closeIronbellyOr-20261104-124207.md:82-82 ; source install_user_setup.py:266-266

B (reviewer-3-card, finding R3-4): Docs edits are not verified: tests/docs/test_retired_docs_absent.py reads every docs/**/*.md; pre-commit markdownlint --fix runs on installation.md.
   points at: spec source.md:1-1 ; source test_retired_docs_absent.py:39-44 ; source .pre-commit-config.yaml:74-88

ANSWER P14: 

## P15

A (reviewer-1-card, finding R1-F3): No task names the Complexity request-body file `.dev/issues/<N>/complexity-field.json` or updates the rule that every output file starts from a template (SKILL.md:52 exempts only clickup.json) or the Outputs row of commands/issue.md.
   points at: spec source.md:38-38 ; spec source.md:80-80 ; source SKILL.md:52-52 ; source issue.md:78-78

B (reviewer-3-card, finding R3-F3): complexity-field.json has no template, but SKILL.md:52 and create.md:7 say every output file starts from a template (only clickup.json exempt) and commands/issue.md:78 does not list it; no task covers these.
   points at: source SKILL.md:52-52 ; source create.md:7-7 ; source issue.md:78-78 ; spec source.md:38-38

ANSWER P15: 

## P16

A (reviewer-1-card, finding F1): Task 5 cannot meet its acceptance criteria and, as worded, would break `ccsession --help`. `show_help` prints the header only up to the first line that matches `^# The wrapper always runs`, then exits. The permissions paragraph at lines 109-114 starts with that sentinel line, so `--help` never pr...
   points at: source ccsession:1651-1652 ; source ccsession:109-114 ; source ccsession:96-98 ; source test_ccsession_tag.py:150-169 ; source test_ccsession_tag.py:1134-1144

B (reviewer-2-card, finding F1): Task 5 is built on a false premise and, followed literally, either breaks `ccsession --help` or fails its own acceptance criterion. The plan asserts the permissions comment block at ccsession:109-114 is "printed by ccsession --help". It is not: show_help() (ccsession:1651-1652) runs awk over the ...
   points at: unresolved PLAN:95 ; unresolved PLAN:97 ; unresolved PLAN:100 ; source ccsession:1652-1652 ; source ccsession:109-109 ; source test_ccsession_tag.py:150-150 ; source test_install_ccsession.py:224-224

ANSWER P16: 

## P17

A (reviewer-1-card, finding F2): Task 4 validates the variable at line 124, before the `-h|--help` dispatch (line 1671 onward), before the `.env` file is sourced (line 846), and before every helper mode. With a bad value, `ccsession --help`, `--list`, `--check-name`, `--ask` and `--auto-name` all exit 2. The plan does not say wh...
   points at: source ccsession:121-124 ; source ccsession:1671-1675 ; source ccsession-orca:132-137 ; source ccsession-orca:204-212 ; source ccsession-orca:249-249

B (reviewer-2-card, finding F2): Task 1's red-log acceptance criterion is unsatisfiable as written: "every test that sets CCSESSION_PERMISSIONS=default or bypass fails" against the unchanged launcher. The same task mandates a CC_CLAUDE_FLAGS=--verbose + CCSESSION_PERMISSIONS=default test asserting "--verbose first and neither de...
   points at: unresolved PLAN:36 ; unresolved PLAN:39 ; source ccsession:124-124 ; source source.md:1-1

ANSWER P17: 

## P18

A (reviewer-1-card, finding R1-09): Task 7 lists commands/task.md '(metadata only)' but row 40 excludes task, so its change is undefined.
   points at: spec source.md:129-129 ; spec source.md:281-281

B (reviewer-2-card, finding R2-02): Row 40 says mcp-servers gains codegraph in six commands incl. troubleshoot and reflect; Task 7 names all six but its file list lacks commands/troubleshoot.md and commands/reflect.md; Tasks 6 and 10 do not mention row 40.
   points at: spec source.md:129-129

ANSWER P18: 

## P19

A (reviewer-1-card, finding R1-1): Task 3 leaves two pre-PR check lines that contradict the new 'no interaction, no exceptions' rule, and no acceptance criterion catches them
   points at: source CLAUDE.md:64-64 ; source CLAUDE.md:66-66 ; source CLAUDE.md:64-64 ; source CLAUDE.md:66-66

B (reviewer-3-card, finding R3-F2): Task 3's ban on any call that reaches upstream contradicts pre-PR check 1, which the plan keeps
   points at: source CLAUDE.md:64-64 ; source CLAUDE.md:64-64

ANSWER P19: 

## P20

A (reviewer-1-card, finding R1-5): Task 3's new wording 'no ... link' is ambiguous against the existing upstream issue link in CLAUDE.md
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

B (reviewer-2-card, finding R2-F1): Task 3's new 'no link that resolves to upstream' rule is contradicted by the untouched #419 upstream issue link elsewhere in CLAUDE.md
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

ANSWER P20: 

## P21

A (reviewer-1-card, finding R1-5): Task 3's new wording 'no ... link' is ambiguous against the existing upstream issue link in CLAUDE.md
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

B (reviewer-3-card, finding R3-F6): CLAUDE.md keeps a link to an upstream issue that Task 3's wording may forbid
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

ANSWER P21: 

## P22

A (reviewer-2-card, finding R2-F1): Task 3's new 'no link that resolves to upstream' rule is contradicted by the untouched #419 upstream issue link elsewhere in CLAUDE.md
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

B (reviewer-3-card, finding R3-F6): CLAUDE.md keeps a link to an upstream issue that Task 3's wording may forbid
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

ANSWER P22: 

## P23

A (reviewer-2-card, finding R2-F4): chains.md:14 token <REPORT.md is safe only because '<' is not stripped; no probe case pins it
   points at: source chains.md:14-14

B (reviewer-3-card, finding R3-F7): refs/chains.md:14 has `<REPORT.md path printed by step 1>`; token <REPORT.md is safe only because '<' is not stripped
   points at: source chains.md:14-14

ANSWER P23: 

## P24

A (reviewer-1-card, finding R1-F1): Spec's closing verification (smoke -k "doc or primitive or how_we_work or severity" then full make test) is absent; only Task 6's narrow -k; Task 26 edits an installed primitive with only make verify-sync.
   points at: spec source.md:47-50

B (reviewer-2-card, finding R2-F1): Spec verification constraint dropped: no 'make test' in the tasklist (grep 0 hits); only Task 6's narrower -k. T1 C3 mitigation contradicted: implement.md:11 says 'Lint and tests are extras, never the pass/fail'; FINAL is a spec-compliance review, not a test run.
   points at: spec source.md:47-50 ; source implement.md:11-11

ANSWER P24: 

## P25

A (reviewer-1-card, finding R1-F1): Spec's closing verification (smoke -k "doc or primitive or how_we_work or severity" then full make test) is absent; only Task 6's narrow -k; Task 26 edits an installed primitive with only make verify-sync.
   points at: spec source.md:47-50

B (reviewer-3-card, finding R3-F1): Spec-mandated verification is missing: source.md:47-50 requires the pytest smoke (-k "doc or primitive or how_we_work or severity") then a full make test at the end; no task runs make test; the only pytest is Task 6's narrower -k (tasklist:89); Task 26 edits an installed primitive with no test ru...
   points at: spec source.md:47-50

ANSWER P25: 

## P26

A (reviewer-1-card, finding R1-4): The owner's core rule (the nested analyze directory exists only when /sc:analyze ran; the fallback lists no nested contract) is pinned by no test in the primitives. A later edit could drop that clause and every planned test stays green. Add a second exact phrase to Task 3, UNATTENDED_EXPECT and t...
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:30-30 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:47-47 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:60-60 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:71-71 ; spec source.md:6-6 ; spec source.md:8-8 ; source test_worker_contract.py:508-509

B (reviewer-2-card, finding R2-4): Brief item 4's placement procedure is not evaluated. Per-command live-check extras are defined in the spec's section 7 acceptance rows (AC-1.5/1.6/1.7 replace 7.2 steps 3-4 per command), yet Task 6 writes to the section 2.1 bullet. Mitigating: spec line 376 maps the 2.1 rule to AC-2.1 (a P2 crite...
   points at: source orca-worker-contract-spec.md:318-322 ; source orca-worker-contract-spec.md:376-376 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:81-81

ANSWER P26: 

## P27

A (reviewer-1-card, finding R1-6): Task 5's 'more cases than before' check has no recorded baseline; the edit adds exactly one id (`brainstorm:phrase:writes no nested directory`). Tell the implementer to save the before-count first.
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:75-75 ; source test_worker_contract.py:519-527 ; source test_worker_contract.py:559-568

B (reviewer-2-card, finding R2-1): Task 7's third acceptance criterion is unsatisfiable at baseline: it requires git status to list only the six files plus this package among tracked paths and nothing under .dev/tasks/done/ modified, but 950 staged additions and 3 renames of the prior package already exist. Both the first clause a...
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:98-98 ; source diagnostics.txt:3-4

ANSWER P27: 

## P28

A (reviewer-2-card, finding R2-1): Task 7's third acceptance criterion is unsatisfiable at baseline: it requires git status to list only the six files plus this package among tracked paths and nothing under .dev/tasks/done/ modified, but 950 staged additions and 3 renames of the prior package already exist. Both the first clause a...
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:98-98 ; source diagnostics.txt:3-4

B (reviewer-3-card, finding R3-6): Phrase variants are pinned correctly but fragile: 'write no nested directory' is not a substring of 'writes no nested directory', so each file is held to its own verb form. A shared phrase such as 'no nested directory' would pin the same rule with less risk.
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:30-30 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:39-39 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:47-47 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:60-60 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:71-71 ; source test_worker_contract.py:508-509 ; source test_worker_contract.py:531-531

ANSWER P28: 

## P29

A (reviewer-2-card, finding 4): Assigned skill edits omit the SKILL.md frontmatter description (says 'then stops') and claim step 6 (Wave 5 summary would omit prompt rendering and the plan boundary). No acceptance criterion detects either.
   points at: spec source.md:303-303 ; source SKILL.md:3-3 ; source SKILL.md:87-87 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:86-86

B (reviewer-3-card, finding 8): Design section 16 puts design-doc B2 and B16 in Phase 1; the plan moves every design-doc edit to Task 8 (Phase 3) without stating why. Both phases ship in one PR.
   points at: spec source.md:405-405 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:139-149

ANSWER P29: 

## P30

A (reviewer-2-card, finding 5): Plan lacks P1's blanket prohibition on code, warnings, options or text added only for non-Orca projects. Confirms T1 F-4.
   points at: spec source.md:39-39 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:19-26 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:17-17

B (reviewer-3-card, finding 7): Design step 5 hand_command note ('an agent started by hand is not governed by the hook; re-running the claim is preferred'), timeout 'check Orca' detail, and step 6 'the pending record stays' are absent from Task 6; LA-3 does not assert them.
   points at: spec source.md:211-212 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:116-116

ANSWER P30: 

## P31

A (reviewer-1-card, finding R1-1): Task 5's "exited 0" assertion can pass with the old contradicting sentence still in place ("The run is succeeded when the audit finished, and failed otherwise" at init-lite.md:92; "`succeeded` when the audit finished, else `failed`" at SKILL.md:61). No existing pin catches this (test_worker_contr...
   points at: source test_worker_contract.py:777-797 ; source init-lite.md:92-92 ; source SKILL.md:61-61 ; source TASK-WF-workerContractFo-20261106-214402.md:76-76

B (reviewer-3-card, finding R3-5): return-contract.md (installed skill ref) never mentions WORKER-CONTRACT.md, so a bare "WC-4" pointer in its YAML comment cannot be followed; no criterion forbids a src/superclaude/ path in the pointer text.
   points at: source return-contract.md:43-54 ; source TASK-WF-workerContractFo-20261106-214402.md:43-43

ANSWER P31: 

## P32

A (reviewer-1-card, finding R1-07): At P0 no `--unattended` exists, so the /sc:workflow worker runs `git add .dev/tasks` in its disposable worktree. Step 6 compares paths only. Plan line 22 also overclaims that the only git-state changes are worktree create and remove.
   points at: source SKILL.md:28-28 ; source WORKER-CONTRACT.md:42-42 ; plan TASK-WF-writeTheP0LivePl-20261103-215902.md:22-22

B (reviewer-3-card, finding R3-08): plan:29 defines a skip only for a failed worktree setup. Two other failures are left open. A worker-start failure still owns a terminal that must be released. A Step 3 stall, or a decision question left unanswered, leaves an unsettled worker, and release needs an accepted settlement first. The co...
   points at: plan TASK-WF-writeTheP0LivePl-20261103-215902.md:29-29 ; source orca-capabilities.md:112-112 ; source orca-capabilities.md:108-108 ; source WORKER-CONTRACT.md:73-73

ANSWER P32: 

## P33

A (reviewer-1-card, finding R1-5): The C-install-surface recipe symlinks /usr/local/bin/node, which does not exist on this host; under env -i the uv cache moves into the throwaway HOME; claude credentials unverified.
   points at: source C-install-surface.md:130-134 ; source TASK-WF-closeIronbellyOr-20261104-084334.md:98-98

B (reviewer-3-card, finding R3-5): Nothing forbids copying credentials from /home/coder/.claude into the throwaway to make M1c's session part work.
   points at: source TASK-WF-closeIronbellyOr-20261104-084334.md:22-22 ; source TASK-WF-closeIronbellyOr-20261104-084334.md:100-100

ANSWER P33: 

## P34

A (reviewer-1-card, finding A-11): No invented functional requirement; additions beyond the spec are verification-only checks.
   points at: source TASK-WF-design-20261104-164423.md:176-176 ; source TASK-WF-design-20261104-164423.md:245-245 ; source TASK-WF-design-20261104-164423.md:270-270 ; source TASK-WF-design-20261104-164423.md:285-285 ; spec source.md:1324-1324

B (reviewer-2-card, finding Q-7): Task 20 omits step 14's staging instruction, so its 'no staged .claude/ path' check is vacuously true and .dev/tasks staging is left to memory.
   points at: source TASK-WF-design-20261104-164423.md:302-302 ; source TASK-WF-design-20261104-164423.md:307-307 ; spec source.md:1429-1429

ANSWER P34: 

## P35

A (reviewer-1-card, finding A-9): Dropping 'make test' is the documented orchestrator constraint (Authorized); residual: line 19 'source wins' does not state the exception and nothing records VG-2 was not run; the tests/cli/reflect blast radius is smaller than claimed because every tests/pr_submit test already imports the package.
   points at: source TASK-WF-design-20261104-164423.md:19-19 ; source TASK-WF-design-20261104-164423.md:28-28 ; spec source.md:1408-1408 ; spec source.md:1429-1429 ; source TASK-WF-design-20261104-164423.md:169-178 ; source commands.py:99-99

B (reviewer-2-card, finding Q-5): TL:29 drops the section 12 preamble's fixed author and committer, and Task 19 lacks the merge-tree capability skip; git commit under GIT_CONFIG_GLOBAL=/dev/null fails without an identity, breaking F9, F10, X1, X3.
   points at: source TASK-WF-design-20261104-164423.md:29-29 ; source TASK-WF-design-20261104-164423.md:291-291 ; spec source.md:1316-1316 ; source TASK-WF-design-20261104-164423.md:186-186

ANSWER P35: 

## P36

A (reviewer-1-card, finding R1-F11): Consistent: tasks 1-66 map to all items and gaps 1-70; ground facts (pyproject.toml:7, counts, transcript ranges, DECISIONS B1-B5, severity test path, RELEASE-READINESS 6.3, D10 fixture) verified.
   points at: source pyproject.toml:7-7 ; source CONSOLIDATED-PLAN.md:237-237 ; source CONSOLIDATED-PLAN.md:675-675 ; source c-e2e-transcript.txt:416-416 ; source c-e2e-transcript.txt:724-775 ; source DECISIONS.md:12-19 ; source RELEASE-READINESS.md:186-200

B (reviewer-2-card, finding R2-F6): Report/manifest exclusion and 'no issue filing' not restated in Constraints; executor reads CONSOLIDATED-PLAN whose section 6 (line 636) instructs filing O1-O22 issues.
   points at: spec source.md:36-36 ; spec source.md:38-38 ; source CONSOLIDATED-PLAN.md:636-636

ANSWER P36: 

## P37

A (reviewer-1-card, finding R1-F6): Plan omits the Tier A/B/C grouping and template header fields (Capability, Audience, Source of truth, Est. time; Gate for sysop) required by the Test guide plan.
   points at: source CONSOLIDATED-PLAN.md:587-587 ; source user-test-guide.md:7-12

B (reviewer-2-card, finding R2-F4): B-W12 item 6 four-note links: Task 37 does not name them and runs before Tasks 43-46.
   points at: source CONSOLIDATED-PLAN.md:481-481

ANSWER P37: 

## P38

A (reviewer-1-card, finding R1-F8): Dependency declarations do not enforce ordering for Tasks 37, 47, 66 and Task 1's upgrading.md link; fine only under sequential execution.
   points at: source CONSOLIDATED-PLAN.md:481-481

B (reviewer-3-card, finding R3-F4): Task 37 omits B-W12 #6 (link four new notes) and runs before Tasks 43-46 with no dependency; AC checks in-file anchors only.
   points at: source CONSOLIDATED-PLAN.md:481-481

ANSWER P38: 

## P39

A (reviewer-1-card, finding R1-F4): Backslash-newline continuation and wrapper options (nice -n, sudo -u, env -u) unspecified; false positive on 'uv run \<newline> python', false negatives for option-taking wrappers
   points at: (no citation)

B (reviewer-3-card, finding R3-F7): Never-exit-1 and fail-open not guaranteed against jq or set -u errors
   points at: (no citation)

ANSWER P39: 

## P40

A (reviewer-1-card, finding F1): Task 4's acceptance criterion cannot pass at the point Task 4 runs. Task 4 depends only on Task 2, and Task 2 depends on Task 1. Task 1 creates src/superclaude/core/WORKER-CONTRACT.md. Task 3 is the task that adds that name to KNOWN_CORE_FILES. Task 4's AC-0.2 command runs tests/cli/test_how_we_w...
   points at: source test_how_we_work_install.py:43-44 ; source install_core.py:13-27 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:56-60 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:70-72 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:77-77 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:106-108 ; source source.md:298-298

B (reviewer-2-card, finding R2-1): 7.2 step 5 requires each phase report to name at least one checked run that lasted longer than the heartbeat cadence, otherwise the WC-10 heartbeat-spacing check passes vacuously (source.md:291). Task 8 is the only task that runs 7.2 in P0 and neither its instructions (TL:122) nor its acceptance ...
   points at: unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:291 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:301 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:15 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:122 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:124 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/artifacts/coverage-matrix.yaml:1410

ANSWER P40: 

## P41

A (reviewer-1-card, finding F7): Common checks are not verified at the final state, although the Goal claims "every P0 check of section 7 passing" and the spec requires every common check to pass for the phase. AC-C1 and AC-C2 run only inside Task 4. Task 3 (possible plugin mirror) can run after Task 4 and is not re-checked. AC-...
   points at: source TASK-WF-orcaWorkerContra-20261102-231950.md:15-15 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:19-19 ; source source.md:241-241 ; source source.md:216-216 ; source coverage-matrix.yaml:1407-1409

B (reviewer-2-card, finding R2-2): AC-0.6's pass condition says "7.2 step 5 follows that answer" and 7.2 step 5 (source.md:291) says that if transcripts do not name tool calls, step 5 uses --source terminal output instead and the phase report records the gap. Task 8 records the AC-0.6 yes/no (TL:122, TL:127) but never carries the ...
   points at: unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:291 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:303 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:122 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:127 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/artifacts/coverage-matrix.yaml:1413

ANSWER P41: 

## P42

A (reviewer-1-card, finding R1-06): Task 7's exhaustion branch is answered statically: identify() reads the target's kernel session and jobs/<sid>.json, with no parent walk; F2.3/F2.6 describe the historical probe. Task 8 has no 'not applicable' state for those findings.
   points at: source launch-job-identity.sh:219-219 ; source launch-job-identity.sh:223-223 ; source launch-job-identity.sh:253-253 ; source actor-context-probe.sh:37-39 ; source review-2.md:9-9 ; source review-2.md:12-12

B (reviewer-3-card, finding R3-F2): Task 7 depends only on Task 5 but its criteria need depths from the Task 2-4 runs.
   points at: unresolved plan lines 99, 101, 104

ANSWER P42: 

## P43

A (reviewer-1-card, finding R1-07): Task 5's 'helper does not compare boot identity' branch is dead (launch-job-identity.sh:234 compares both); editing the state copy risks rejecting for mode or hard-link reasons instead of the edited field.
   points at: source launch-job-identity.sh:234-234 ; source launch-job-identity.sh:83-83 ; source launch-job-identity.sh:149-149 ; source launch-job-identity.sh:218-244

B (reviewer-3-card, finding R3-F12): The twelve-run cap is not allocated and no criterion counts runs or cost; Tasks 2-4 plausibly need 9-14 runs.
   points at: unresolved plan lines 22, 44, 55, 66

ANSWER P43: 

## P44

A (reviewer-1-card, finding F5): Task 4's 'keep the existing sentence that the scheduler is the owner's choice' does not say where that sentence lives.
   points at: source issue-watcher-setup.md:202-202

B (reviewer-2-card, finding QA-02): Plan weakens 'replace every guessed fixture' to 'replace whichever were captured'; Task 5 precondition (one capture per fixture, plan:108) contradicts its body (missing captures allowed, plan:110); coverage matrix row 14 overstates coverage.
   points at: spec source.md:22-22 ; plan TASK-WF-rollOutTheIssueW-20261109-000305.md:110-110 ; source coverage-matrix.md:14-14

ANSWER P44: 

## P45

A (reviewer-1-card, finding R1-F3): Task 14 (tdd) says in task-builder/SKILL.md that "the CLI-mode reflect gate's staging step is not run", but not whether the gate's `superclaude reflect run --fix --promote` call itself still runs. `--fix` and `--promote` mutate and move files; the plan leaves the rest of that gate undefined under...
   points at: plan TASK-WF-writeTheP2Static-20261107-011441.md:261-261 ; spec source.md:150-150 ; source test_worker_contract.py:2044-2052

B (reviewer-3-card, finding R3-F12): [INFERRED] For the D-P2-1 research-light arm, brainstorm's enrichment table expects enrichment/research-light.md but /sc:research writes claudedocs/research_[topic]_[timestamp].md; the plan does not say which path brainstorm reads. The table also names `Skill sc-research-protocol`, which does not...
   points at: source SKILL.md:189-189 ; source research.md:103-103

ANSWER P45: 

## P46

A (reviewer-1-card, finding 11): Drops the superclaude.* command form the design lists.
   points at: unresolved DESIGN:102-127 ; unresolved Task 9

B (reviewer-2-card, finding 3): Task 18 defines effective registrations as the exact command present under both events and hooks not globally disabled; a registration whose matcher excludes governed tools, or a prompt registration that cannot bind, would pass. Negative cases test missing, not present-but-ineffective, registrati...
   points at: unresolved DESIGN:342-352 ; unresolved PLAN:291

ANSWER P46: 

## P47

A (reviewer-1-card, finding 13): T-REG-3 negatives do not match the AC-map module.
   points at: source merged-requirements.md:971-1108 ; unresolved Task 12

B (reviewer-2-card, finding 8): Task 16 requires panel F1-F8 regression cases but no resolvable source holds their definitions; the panel review file does not exist.
   points at: unresolved DESIGN:311; file .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md is absent ; unresolved PLAN:266

ANSWER P47: 

## P48

A (reviewer-1-card, finding 14): Pins non-git leaks as expected behaviour.
   points at: unresolved DESIGN:133-175 ; unresolved Task 16

B (reviewer-3-card, finding 10): Treats any skipped test as failure, but existing tests skip on non-Linux and as root.
   points at: source test_launch_job_identity.py:18-18 ; source test_freshness_subagent_start_policy.py:72-72 ; unresolved PLAN:349 (Task 22)

ANSWER P48: 

## P49

A (reviewer-2-card, finding 1): Task 1 lets L1 proceed while B-CTX stays blocked; its acceptance checks the verdict document, not a stop condition; Task 2 supplies synthetic fixtures instead of completing OB-H1.
   points at: unresolved DESIGN:359-360 requires stopping enforcement implementation when the distinction cannot be established, then OB-H1 before the skeleton. Fix: make enforcement tasks conditional on the evidence, or obta ; unresolved PLAN:36

B (reviewer-3-card, finding 5): Task 19 reports a missing L2 as a status line on a launched claim; Task 20 then refuses that same case, so Task 19's tests describe a state that cannot exist after Task 20.
   points at: unresolved PLAN:305, PLAN:310, DESIGN:514 ; unresolved PLAN:301-312 vs PLAN:314-325

ANSWER P49: 

## P50

A (reviewer-1-card, finding R1-F7): Task 65 hardcodes python3 -m http.server (plan addition, conflicts with UV-only rule); _fetch uses urllib urlopen with no scheme check so file:// likely works.
   points at: source CONSOLIDATED-PLAN.md:632-632 ; source models.py:255-268

B (reviewer-3-card, finding R3-F8): Markdownlint invocation differs from spec wording but matches the repo pre-commit pin (markdownlint-cli v0.38.0).
   points at: source .pre-commit-config.yaml:74-77 ; spec source.md:48-48

ANSWER P50: 
