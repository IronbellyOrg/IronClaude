---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-fixGitHubIssue31-20261105-031410
version: "1"
priority: Medium
created_date: "2026-11-05"
---

# Agents no longer get stuck at the ccsession session name question (#315, IronClaude part)

Source: ./source.md
Goal: Every Claude start through ccsession and ccsession-orca either asks the naming question only when it has no task, no name and no resume, or does not ask at all. Every start without a name gets a unique automatic name, the question gives up after 30 seconds, and Ctrl+C at the question cancels with exit status 130 and no Claude start.

## Constraints

- Scope is the IronClaude part of issue 315 only: src/superclaude/skills/ccsession-tag/ccsession, src/superclaude/skills/ccsession-tag/ccsession-orca, their tests and docs. The Coder repo (New Terminal hook, the claude wrapper handoff) is out of scope and is not touched.
- Build on master. Never rebase on or merge origin/clayphi/433-ccsession-orca-resume; its work is already in master through pull request 355 and it must not be pushed to or edited.
- The pull request 355 tab reopen in ccsession-orca keeps running first, under the same conditions as today (terminal, CCSESSION_AUTOSTART not 0, no resume option, ORCA_PANE_KEY set, only Orca's own options), ahead of the question and ahead of the auto-name.
- The typed prompt is never read as a label. A line typed at the question is a name unless it cannot be one (control character, more than one line, or over 245 bytes); normal lines, spaces included, stay names. No other input guessing.
- Decisions taken by the plan author where the source is silent, to be reported to the owner: CCSESSION_AUTOSTART=0 keeps meaning a plain untagged start with no question and no auto-name; print-mode launches (-p, --print) stay untagged because they are not interactive sessions; resume-like launches (--resume, -r, --continue, -c, --fork-session, --from-pr) keep their own session and get no label; CCSESSION_NAME is the supported explicit name and is read by ccsession-orca, while a Claude --name or -n in Orca's arguments is NOT lifted: it passes through to Claude unchanged and counts as a name carried (no question, no auto-name). This replaces the earlier lift decision (see the amendments below).
- Claude Agent Teams stays the one documented exception: it is documented and listed as a follow-up, not changed.
- All tests run only in throwaway HOME directories under the pytest tmp_path, with the fake Claude binary of the existing harness. Never touch the live ~/.claude or the live ccsession shim. Edit src/superclaude files only; never stage .claude/ mirrors except .claude/settings.json.
- Amendments from the advisory review, resolved before execution (source: .dev/reflect/pre-fixGitHubIssue31-20261105031639/adversarial/merged-verdict.yaml; they apply to every task and win over any task text that conflicts with them):
- RN-1: an invalid CCSESSION_NAME, an empty or failing --auto-name result (control character, over 245 bytes, a folder name with a leading dot or 4-byte characters, an unwritable topics directory) or an unexpected --ask status never stops Claude from starting. Fallback order: drop the bad name with a stderr warning, then auto-name, then a plain untagged start; ccsession-orca never exits 2 for these. A name equal to a saved label never silently resumes that conversation. Tests in Tasks 3, 4 and 7: leading-dot folder, name with a tab, 300-character CCSESSION_NAME, name equal to a saved label, failing --auto-name; each reaches the fake Claude.
- RN-2: Claude --name/-n/--name= in Orca's arguments is not lifted (Task 3 criterion 2 and the Task 7 --name case change accordingly): such a launch counts as name-carried and passes unchanged. CCSESSION_NAME is validated (RN-1) and unset before every exec.
- RN-3: --auto-name is dispatched in the early fast-path case of ccsession (before the main argument loop, after ensure_names_migrated), not next to --ask; tests for the texts --model, --claude-args, --shim and --tier=x.
- RN-4: Task 5 also updates test_orca_a_new_tab_or_a_rerun_is_still_asked and test_orca_relaunch_whose_conversation_is_gone_is_asked (Enter now auto-names), rewrites test_orca_invalid_name_asks_again, drops the "the prompt" argument from the Ctrl+C line-mode test, changes test_orca_saved_name_is_listed_and_resumes_before_the_prompt to the `--name demo "fix it"` form, and adds CCSESSION_NAME to the environment exclusion lists in tests/unit/test_ccsession_tag.py and tests/unit/test_ccsession_tiers.py. "Keep as they are" applies only to reopen tests that do not press Enter.
- RN-5: the typed line is read with IFS= read -r and tested raw for control characters and the 245-byte rule before any trimming; an exit-3 message that starts with "-" is passed after "--"; tests for a leading tab, a trailing tab, a mid-line tab, "- a list" and "--version".
- RN-6: ccsession-orca unsets CCSESSION_ASK_TIMEOUT and CCSESSION_NAME before the final exec (the one-second timeout test sets the variable while Claude's recorded environment must not contain it).
- RN-7: the Task 3 classification covers --session-id=*, --prefill=* and --name=*, a trailing --name with no value, and treats the values of known value-taking options (--model, --permission-mode, --add-dir, --allowedTools, --mcp-config) as non-positional; unknown options fail safe (counted as a task); one test per form.
- RN-8: a test runs ccsession --ask with CCSESSION_ASK_TIMEOUT=2 and asserts the hint reads "auto-named after 2s", next to the default-hint test, so a default left unlimited fails.
- RN-9: the auto-name carries seconds or a short random part, folder name and task words are cut first so the stamp is kept, and two --auto-name calls in the same minute with no saved topic give different labels.
- RN-10: the executor writes ./artifacts/launch-paths.md from the final pytest output; no test writes outside tmp_path.
- RN-11: ccsession-orca passes the auto-name hint; the default hint of ask_session_name stays as today for other callers; the Task 11 handoff states that the 30 s default now also applies to the Coder New Terminal hook and that the dependency on orchestrators passing a task or name is documented, not enforced.
- RN-12: the Task 9 criterion also pins the --session-id statement in README.md.

## Phase 1: ccsession gives out unique names and ends the question correctly

## Task 1: Add the ccsession --auto-name helper

Add a `--auto-name [<task text>]` option to src/superclaude/skills/ccsession-tag/ccsession, next to `--ask` in the pre-launch option dispatch (around the `--ask` case). It prints one label on stdout and exits 0. The label is the worktree folder name, then up to four words of the task text (lowercase a-z0-9 only, control characters and punctuation dropped, nothing from the text when none is given), then a short local month-day-hour-minute stamp, joined with hyphens and cut to at most 80 characters. It must pass `validate_label`, and it must not equal any saved name in this folder's topics directory (`$PROJECTS_DIR/$(name_key)/topics/<name_to_file>.txt`): on a collision it appends -2, -3 and so on until the file does not exist. Task text with newlines, tabs, quotes, shell metacharacters or non-ASCII text must never break the label or the shell.

Acceptance criteria:
- `ccsession --auto-name` and `ccsession --auto-name "Fix the login bug; rm -rf /"` each print a single line that `ccsession --name <label>` accepts, in a throwaway HOME.
- With a saved topic file already holding the label that would be generated, a second call prints the same label with -2 appended; a third prints -3.
- A 5000-character multi-line task text with control characters yields a label of at most 80 characters with no control characters.
- `ccsession --help` text lists `--auto-name`.

## Task 2: Move the 30-second limit into the question and add the not-a-name outcome

Depends on: Task 1

Edit `ask_session_name` in src/superclaude/skills/ccsession-tag/ccsession. The default of `CCSESSION_ASK_TIMEOUT` becomes 30 inside the function (a value of 0 still waits forever, a non-number still means no limit as today), so every caller gets the timer. The default hint becomes "Enter = auto-named, Ctrl+C = cancel; auto-named after 30s" (the 30 follows the actual limit). Keep exit 130 on Ctrl+C with the terminal mode restored, exit 1 for not asked, timeout, end of input and keys already waiting. Add the narrow safety net: when the typed line contains a control character, or is longer than 245 bytes as a file name, or more bytes are already waiting after the line (a pasted multi-line text), ask_session_name reads the rest of the waiting text, prints the whole text on stdout and exits 3 instead of asking again. A blank line, `*`, and an ordinary invalid name keep their current behaviour (blank means Enter, `*` lists every worktree, other invalid names ask again with the reason). Update the `--ask` description in the ccsession header comment and help (around the lines that describe `--ask`) with the exit statuses 0, 1, 3 and 130.

Acceptance criteria:
- `ccsession --ask` on a pseudo-terminal with no CCSESSION_ASK_TIMEOUT set and no input exits 1 after about 30 seconds (the test sets the limit to 1 second through the environment to stay fast) and shows the default hint with the limit.
- Ctrl+C at the question exits 130 and leaves the terminal in line mode, as the existing `test_ask_ctrl_c_while_line_mode_is_off_exits_130_and_restores` still requires.
- A line of 246 x characters, a line holding a tab, and a two-line paste each make `ccsession --ask` print the text on stdout and exit 3; the line `my fix plan` (spaces) is printed and exits 0 as a name.
- Keys already waiting before the question still return exit 1 without a question.

## Phase 2: ccsession-orca applies the one question rule

## Task 3: Classify the launch and apply the one question rule in ccsession-orca

Depends on: Task 2

Edit src/superclaude/skills/ccsession-tag/ccsession-orca. Replace the single `ask` computation by a classification of the arguments (the existing `--prefill <text>` skipping stays: the text after --prefill is not an option). Resume-like: `--resume`, `--resume=*`, `-r`, `--continue`, `-c`, `--fork-session`, `--from-pr`, `--from-pr=*`. Name carried: `CCSESSION_NAME` in the environment (non-empty), or `--name <value>`, `--name=<value>`, `-n <value>` in the arguments; the value is lifted out of Claude's arguments and passed as ccsession's own `--name` (an exec of `ccsession --name <value> --shim --claude-args <remaining arguments>`), so it is not given twice. Task carried: any positional argument, `--prefill <text>`, `--session-id`, `-p`, `--print`. The question is asked only when stdin and stdout are terminals, CCSESSION_AUTOSTART is not 0, and the launch is not resume-like and carries no name and no task. Keep the pull request 355 reopen block ahead of everything else and driven by the same conditions as before (terminal, autostart, not resume-like, ORCA_PANE_KEY, plain options only), independent of the new rule. Remove the `trap ':' INT` and the exported default `CCSESSION_ASK_TIMEOUT` hint logic that duplicated the timer; the question reads its limit from ccsession. Update the header comment of the script to describe the new rule.

Acceptance criteria:
- A launch with a positional prompt, `--prefill <text>`, `--session-id <id>`, `CCSESSION_NAME=x` or `--name x` on a terminal shows no question and no saved-session list.
- A launch with `--name my demo` (two arguments, value `my demo`) reaches Claude with exactly one `--name my demo` in the arguments and the topic `my demo` in the fake Claude record.
- The plain relaunch of an Orca tab (ORCA_PANE_KEY set, only Orca's options) still reopens the recorded session without a question, as the tests around the pull request 355 behaviour require.
- A new tab with no argument on a terminal still shows the question.

## Task 4: Map every question outcome in ccsession-orca to an auto-name, a message or a cancel

Depends on: Task 3

Edit the exec section of src/superclaude/skills/ccsession-tag/ccsession-orca. After the question (or without one), start `ccsession --name <label> --shim --claude-args <arguments>` with these labels: a name typed at the question is the label; exit 1 from `--ask` (timeout, end of input, keys already waiting) and an empty answer (Enter) take `ccsession --auto-name`; a launch that was not asked because it carries a task, has no terminal, or is not resume-like, name-less and not CCSESSION_AUTOSTART=0 and not print mode takes `ccsession --auto-name "<first positional prompt or prefill text, if any>"`. Exit 3 from `--ask` starts Claude with the returned text appended as the last positional argument (the first message), plus an auto-name built from that text. Exit 130 from `--ask` makes ccsession-orca exit 130 without starting Claude and without writing any session record. CCSESSION_AUTOSTART=0, print mode and resume-like launches start exactly as today (untagged, arguments unchanged).

Acceptance criteria:
- On a pseudo-terminal, Enter at the question and a one-second timeout both start Claude with `--name <auto label>`, the topic recorded in the fake Claude record equals that label, and no `CCSESSION_ASK_TIMEOUT` is left in Claude's environment.
- Ctrl+C at the question makes `ccsession-orca` exit with status 130, the fake Claude record file is not created, and the terminal is back in line mode.
- A launch without a terminal and with a prompt starts Claude with the prompt unchanged as the last argument, plus `--name <auto label>` built from the prompt words.
- A tab line of 300 characters typed at the question reaches Claude as the last positional argument and is not a label.
- CCSESSION_AUTOSTART=0, `-p x`, and `--resume <id>` launches produce no `--name` and unchanged arguments.

## Phase 3: Tests pin the new behaviour and every launch path this repo controls

## Task 5: Update the tests that pinned the old untagged behaviour

Depends on: Task 4

In tests/unit/test_ccsession_tag.py, update the Orca tests that assert the old behaviour, using the existing harness helpers (`_orca_env`, `_orca_tty`, `_orca_no_tty`, `_spawn_on_pty`) and the changed question text constant `ORCA_QUESTION`: `test_orca_enter_or_ctrl_c_starts_untagged` (Enter now auto-names; Ctrl+C now exits 130 with no Claude start), `test_orca_ctrl_c_while_line_mode_is_off_restores_the_terminal` (still restores the terminal and now exits 130), `test_orca_unanswered_question_starts_untagged` (timeout now auto-names), `test_orca_keys_already_typed_skip_the_question`, `test_orca_without_a_terminal_never_asks`, `test_orca_prompt_reaches_claude_unchanged_and_is_never_a_label`, `test_orca_prefill_passes_through_and_its_text_is_not_a_flag`, `test_orca_a_launch_with_more_than_options_is_asked_as_before`, `test_orca_relaunch_without_a_terminal_or_autostart_changes_nothing` and any other Orca test in the file that asserts `record["topic"] is None` or an unchanged argument list for a launch that is now auto-named. Rename tests whose names no longer describe them. Keep `test_orca_resume_skips_the_question`, `test_orca_autostart_off_never_asks` and the relaunch reopen tests asserting untagged or reopened behaviour as they are.

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tag.py -k orca -v` passes, and no remaining Orca test asserts that a prompt-bearing, no-terminal, Enter or timeout launch is untagged.
- The prompt text `demo` with a saved label `demo` still never resumes that label (the prompt is not a label).

## Task 6: Add tests for the auto-name helper and the question outcomes

Depends on: Task 5

Add tests to tests/unit/test_ccsession_tag.py for `ccsession --auto-name` (valid and shell-safe for hostile text, 80-character cap, unique against saved topics with -2 and -3, no text) and for `ccsession --ask` (default 30-second limit shown in the hint, exit 1 on timeout, exit 3 for the 246-byte line, the tab line and the two-line paste, exit 0 and a name for `my fix plan`, `*` still lists, a blank line still means Enter).

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tag.py -k "auto_name or ask" -v` passes with at least one test per listed case.
- Each new test fails when the matching behaviour in ccsession is reverted (checked once by temporarily reverting the exit 3 path and seeing the paste test fail, then restoring it).

## Task 7: Add pseudo-terminal tests for every launch path the plan table lists

Depends on: Task 5

Add tests to tests/unit/test_ccsession_tag.py, one per launch path this repo controls, each run through ccsession-orca on a pseudo-terminal or without one in a throwaway HOME: the Claude button (no arguments, terminal: question, name, Enter, timeout); a worktree-create or agent-launch launch with a prompt (terminal and no terminal: no question, auto-name, prompt last); worker-start without a prompt (CCSESSION_NAME given: no question, label is the name; nothing given and a task typed ahead of the question: no question, the typed text stays for Claude); the typed-line safety net (long line, tab line, paste, ordinary name with spaces); resume (`--resume`, `--continue`, `--fork-session`: no question, no label); the pull request 355 plain relaunch (reopens, no question); a plain relaunch of a tab with no record (asked); print mode `-p` (untagged); CCSESSION_AUTOSTART=0 (untagged); Claude `--name x` and `CCSESSION_NAME=x` (label x, one `--name` in Claude's arguments); an auto-named session is listed by `ccsession --here` once the session hook records it.

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tag.py -k orca -v` passes with a test for every path listed above, each asserting the question shown or not shown, the topic, and the exact Claude arguments from the fake Claude record.
- The launch-path results (path, expected, observed) are written to ./artifacts/launch-paths.md in this package by the final test run.

## Task 8: Keep the tier-mode Orca relaunch test and add an auto-name check on the tier path

Depends on: Task 5

In tests/unit/test_ccsession_tiers.py, keep the Orca relaunch test near line 412 passing unchanged, and add one test beside it that a prompt-bearing ccsession-orca launch in tier mode starts through the shim with an auto-name and the prompt as the last argument.

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -v` passes, including the new test.

## Phase 4: Docs describe the new rule and its one exception

## Task 9: Rewrite the README and script headers for the new rule

Depends on: Task 7

Edit src/superclaude/skills/ccsession-tag/README.md (the Orca section around the launch rules, the question, `CCSESSION_ASK_TIMEOUT`, `CCSESSION_AUTOSTART` and the reopen, roughly lines 205 to 280) and keep the header comments of ccsession and ccsession-orca in step. Document: the one question rule (asked only when there is no task, no name and no resume); the table of launch paths and what each does; auto-names (format, uniqueness, they appear in the saved-session list); the 30-second limit and its override; Ctrl+C cancels with status 130; CCSESSION_NAME and the Claude --name lift; the safety net for a typed line that cannot be a name; print mode and CCSESSION_AUTOSTART=0 staying untagged; the resolved drift that `--fork-session` skips the question as a resume-like option; Claude Agent Teams bypasses ccsession and is the one documented exception and a follow-up. Orchestrators are told to always pass the task or a name in the launch.

Acceptance criteria:
- README.md contains each of the listed topics, no sentence still says Enter, Ctrl+C or a timeout start an untagged session in Orca, and the `--fork-session` statement matches the code.
- `grep -rn 'src/superclaude' src/superclaude/skills/ccsession-tag` shows no new reference to a source-tree path.

## Task 10: Update the CHANGELOG and the v5.0.0 ccsession test guide

Depends on: Task 9

Add an Unreleased entry to CHANGELOG.md for the fix (title with the issue number 315), and update docs/testing/v5.0.0/user/D08-ccsession.md wherever it pins the old behaviour (`--ask` with no limit, `CCSESSION_AUTOSTART`, Enter or Ctrl+C starting untagged, the 30-second untagged start, around lines 240 to 250). Also correct the CHANGELOG line that describes the old Orca question behaviour only if it is in the Unreleased section; released history stays as written.

Acceptance criteria:
- CHANGELOG.md Unreleased lists the change and issue 315; released sections are unchanged (checked with `git diff` showing only Unreleased lines added).
- D08-ccsession.md steps and expected results match the tested behaviour for Enter, timeout, Ctrl+C and prompt-bearing launches.

## Phase 5: Hand the Coder part over

## Task 11: Write the Coder handoff

Depends on: Task 10

Write ./artifacts/coder-handoff.md in this package, ready to file as an issue in IronbellyOrg/Coder: what Coder must change (retire templates/VSCode-AIDev02/lib/aidev/ccsession-autostart.sh so a New Terminal is a plain shell; make the /usr/local/bin/claude wrapper from Coder 358 hand off to ccsession-orca so a bare `claude` in a terminal gets the same one question rule; keep Claude Agent Teams in mind as the open exception) and what IronClaude now guarantees (the one question rule, auto-name, the 30-second limit, Ctrl+C exit 130 meaning the wrapper must return to the shell on 130, exit statuses of `ccsession --ask`, CCSESSION_NAME and CCSESSION_AUTOSTART=0, the launch-path table with test names). It uses the issue template of the Coder handoff form (`~/.claude/ISSUE-HANDOFF.md` copied, never edited in place).

Acceptance criteria:
- ./artifacts/coder-handoff.md exists with every section of the handoff template filled and names the tests that prove each guarantee.
- It states plainly that the Coder repo was not touched.
