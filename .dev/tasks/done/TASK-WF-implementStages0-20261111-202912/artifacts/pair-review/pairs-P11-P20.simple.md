# Pairs P11 to P20 (simple version)

Each pair is two complaints from two different AI reviewers who reviewed the same plan. For each pair, ask: would ONE edit to the plan fix both complaints? If yes, type yes after the colon on the ANSWER line. If no, type no. Change nothing else.

If one complaint lists several problems, answer yes when one of those problems is the other complaint's problem. If you cannot tell, pick the closer answer and add a note on the next line starting with NOTE.

These summaries were written by AI helpers from the full reviews and the linked files. They were told not to hint at an answer. The original wording is in cluster-pairs-50.form.md.

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

