0b3543fbe4c8765d9e8e6be1775ba8b430e9410c
family readme-env-not-passed
defect form: a README sentence states a universal ("never", "any", "neither") that a code path contradicts
search: sed -n 211,330p src/superclaude/skills/ccsession-tag/README.md | grep -n -i -E 'never|always|neither|every|any |whatever|all '
before-output: 16: a prompt is never read as a session name|30: Any name works|33: tab never ends at a dead prompt|59: whatever the launch|74-78: whatever the text holds, never a saved name, a launch never stops|86-89: every caller of --ask has it, Neither this limit nor CCSESSION_NAME|100: never treated as a relaunch|102: should always pass|
coupled sites: line 30 "Any name works" (a name with a control character is not a name; reworded); lines 74-78 auto-name claims (checked by the T6 tests); line 89-90 env claim (fixed in code, test_orca_reopen_leaves_the_name_and_the_limit_out_of_claudes_environment); line 100 (fixed: a valid CCSESSION_NAME)
after: line 30 now reads "Spaces are fine, and a name starting with - is passed on as --name"; the other universals checked against code or tests
second pass (A2 review r2-1, family readme-universal-claim): the second review found six more README claims that were true in the common case and false in an edge. Search: sed -n 211,330p src/superclaude/skills/ccsession-tag/README.md | grep -n -i -E 'never|always|neither|every|any |whatever|all |last|only|both'
after: each claim in the section was re-read against the code before the third edit: prompt-last removed, ccsession-orca (not every caller) removes the two variables, the @LIMIT@ form is stated exactly, the three terminal conditions are listed, the conversation-gone resume case is stated, "never share a label" replaced by the checked-and-random statement.
after review 3 (executor, no fourth review run): F3.1 fixed in README (two sites) and the ccsession header; test_ask_a_blank_line_means_enter now covers tab-only and space-only lines.
