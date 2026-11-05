# Launch paths of ccsession-orca (issue 315)

Generated from `uv run pytest tests/unit/test_ccsession_tag.py -k orca -v` (log: ./t7-orca-tests.log). Every row's "Observed" column counts the tests of that path in that log that PASSED and lists any that did not. Each test asserts: the question shown or not shown, the topic Claude was started with, and the exact arguments Claude received (from the fake Claude's record). "Label" means an automatic name `<folder>-<up to 4 task words>-<MMDD-HHMMSS>-<4 hex>`.

| Path | Expected | Test name pattern | Observed |
|---|---|---|---|
| Claude button, no arguments, terminal: a name typed | Question shown; Claude gets --name <typed>; topic = typed | `test_orca_name_starts_a_labeled_session_through_the_shim or test_orca_question_takes_a_name` | 3 passed, 0 failed |
| Claude button: saved name typed | Saved sessions listed; Claude resumes that session | `test_orca_saved_name_is_listed_and_resumes_at_the_question` | 1 passed, 0 failed |
| Claude button: Enter | Question shown; Claude gets an automatic label | `test_orca_enter_gets_an_auto_name` | 1 passed, 0 failed |
| Claude button: no answer in the time limit | Question shown with the limit; after it an automatic label | `test_orca_unanswered_question_is_auto_named or test_orca_ask_question_hint_follows_the_limit` | 2 passed, 0 failed |
| Claude button: Ctrl+C | Exit 130; Claude not started; terminal back in line mode | `test_orca_ctrl_c` | 2 passed, 0 failed |
| Agent or worktree launch with a prompt, terminal and no terminal | No question; automatic label from the prompt words; prompt is the last argument | `test_orca_launch_with_a_prompt_is_auto_named_and_never_asked or test_orca_prompt_reaches_claude_unchanged or test_orca_prefill_passes_through` | 9 passed, 0 failed |
| Worker start, nothing given, no terminal | No question; automatic label | `test_orca_launch_with_nothing_and_no_terminal_is_auto_named or test_orca_without_a_terminal_never_asks` | 2 passed, 0 failed |
| Worker start with CCSESSION_NAME (terminal or not, with or without a prompt) | No question; label is the name; one --name; CCSESSION_NAME not in Claude's environment | `test_orca_ccsession_name_names_the_session_and_is_never_asked` | 4 passed, 0 failed |
| CCSESSION_NAME invalid (tab, newline, blank, 300 characters) | Warning; the name is dropped; automatic label; Claude still starts | `test_orca_invalid_ccsession_name_never_stops_claude or test_orca_ccsession_name_longer_than_the_limit` | 5 passed, 0 failed |
| CCSESSION_NAME equal to a saved label | Resumes that session, loudly | `test_orca_ccsession_name_equal_to_a_saved_label or test_orca_saved_name_in_ccsession_name_resumes` | 2 passed, 0 failed |
| Task typed ahead of the question | No question; the typed keys stay for Claude; automatic label | `test_orca_keys_already_typed_skip_the_question` | 1 passed, 0 failed |
| Typed line that cannot be a name (246 bytes, tab, paste, dash list) | Becomes Claude's first message (after -- when it starts with -); automatic label | `test_orca_a_line_that_cannot_be_a_name or test_orca_typed_text_that_cannot_be_a_name` | 8 passed, 0 failed |
| Typed name with spaces or a leading dash | Is a name | `test_orca_question_takes_a_name` | 2 passed, 0 failed |
| Resume (--resume, -r, --continue, --fork-session, --from-pr) | No question; no label; arguments unchanged | `test_orca_resume_skips_the_question` | 7 passed, 0 failed |
| Session id (--session-id) | No question; automatic label added | `test_orca_session_id_launch` | 1 passed, 0 failed |
| Pull request 355 plain relaunch of a tab with a record | Reopens the tab's session; no question; no new label | `test_orca_relaunch_reopens or test_orca_two_tabs or test_orca_clear_in_the_tab or test_orca_relaunch_without_a_terminal` | 5 passed, 0 failed |
| Plain relaunch of a tab with no record or a gone conversation | Question asked | `test_orca_a_new_tab_or_a_rerun_is_still_asked or test_orca_relaunch_whose_conversation_is_gone` | 3 passed, 0 failed |
| Relaunch carrying more than Orca's options | No reopen; not asked | `test_orca_a_launch_with_more_than_options or test_orca_a_session_choice_wins` | 7 passed, 0 failed |
| Print mode (-p, --print) | Untagged; no question; arguments unchanged | `test_orca_print_mode_is_untagged` | 3 passed, 0 failed |
| --version, -h, mcp, doctor | No label; no question | `test_orca_commands_that_start_no_session` | 4 passed, 0 failed |
| CCSESSION_AUTOSTART=0 | Untagged; no question | `test_orca_autostart_off` | 2 passed, 0 failed |
| Claude --name, -n, --name= (new name) | Passed through once; no question; no second --name | `test_orca_claude_name_is_kept_once or test_orca_claude_name_with_a_saved_label` | 4 passed, 0 failed |
| Auto-named session in the saved-session list | ccsession --here lists the label once the session hook records it | `test_orca_auto_named_session_is_listed` | 1 passed, 0 failed |

Totals: 85 passed in the whole -k orca run; 0 failed.

## Added after the final whole-package review (run: ./t7-orca-tests-final.log)

The table above is from ./t7-orca-tests.log (85 passed); its counts are not updated. These paths were added later, and the whole `-k orca` run is counted at the end.

| Path | Expected | Test name pattern | Observed |
|---|---|---|---|
| CCSESSION_NAME valid on print mode, --version, a subcommand, CCSESSION_AUTOSTART=0 | Passed as --name; no question | `test_orca_valid_ccsession_name_is_passed_even_where` | 4 passed, 0 failed |
| Tab reopen: CCSESSION_NAME and CCSESSION_ASK_TIMEOUT left out of Claude's environment | Reopens; neither variable reaches Claude | `test_orca_reopen_leaves_the_name_and_the_limit` | 2 passed, 0 failed |
| --prefill=<text>, --session-id=<id>, an unknown option and its value | Count as a task: no question; automatic name | `test_orca_equals_forms_and_unknown_options` | 3 passed, 0 failed |
| Trailing --name with no value | A name given: no question; no automatic name | `test_orca_trailing_name_with_no_value` | 1 passed, 0 failed |
| Value of a known option (--model, --permission-mode, --add-dir, --allowedTools, --mcp-config) | Not a task: the question is asked | `test_orca_the_value_of_a_known_option` | 5 passed, 0 failed |
| Folder with a leading dot and CJK characters | Launch reaches Claude with a valid automatic name | `test_orca_launch_in_a_hidden_folder` | 1 passed, 0 failed |
| Typed text that looks like an option (--version) | A name; pasted with a second line it is a message after -- | `test_orca_typed_option_looking_text` | 1 passed, 0 failed |
| Unwritable name list through ccsession-orca | Claude starts untagged with the prompt | `test_orca_starts_untagged_when_the_name_list` | 1 passed, 0 failed |

Totals of ./t7-orca-tests-final.log: 103 passed, 0 failed.
