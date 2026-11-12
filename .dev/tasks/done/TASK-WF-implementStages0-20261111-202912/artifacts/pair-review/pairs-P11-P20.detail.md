# Pairs P11 to P20 (detail version)

For each pair, read complaint A and complaint B. They come from two different reviewers of the same plan.
Question: would ONE edit to the plan (or spec) fix both complaints? If yes, they are the same problem.
Write yes or no after the colon on the line that starts with ANSWER. Do not change anything else.
If one complaint lists several problems, answer yes when one of those problems is the other's problem.

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

