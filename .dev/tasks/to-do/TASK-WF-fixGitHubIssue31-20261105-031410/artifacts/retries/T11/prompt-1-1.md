65dbd5726fe7a4028e5760c211ccc55f65f7a49c
Review one task for spec compliance.

Task brief: ## Task 11: Write the Coder handoff

Depends on: Task 10

Write ./artifacts/coder-handoff.md in this package, ready to file as an issue in IronbellyOrg/Coder: what Coder must change (retire templates/VSCode-AIDev02/lib/aidev/ccsession-autostart.sh so a New Terminal is a plain shell; make the /usr/local/bin/claude wrapper from Coder 358 hand off to ccsession-orca so a bare `claude` in a terminal gets the same one question rule; keep Claude Agent Teams in mind as the open exception) and what IronClaude now guarantees (the one question rule, auto-name, the 30-second limit, Ctrl+C exit 130 meaning the wrapper must return to the shell on 130, exit statuses of `ccsession --ask`, CCSESSION_NAME and CCSESSION_AUTOSTART=0, the launch-path table with test names). It uses the issue template of the Coder handoff form (`~/.claude/ISSUE-HANDOFF.md` copied, never edited in place).

Acceptance criteria:
- T11.AC1: ./artifacts/coder-handoff.md exists with every section of the handoff template filled and names the tests that prove each guarantee.
- T11.AC2: It states plainly that the Coder repo was not touched.
Global constraints: 
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
Start sha: 65dbd5726fe7a4028e5760c211ccc55f65f7a49c
Diff against the start snapshot: --- NEW FILE .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/artifacts/coder-handoff.md ---
<!-- Suggested issue title: ccsession-orca now owns the session-name question: retire the New Terminal hook and route bare `claude` through it (IronClaude #315) -->
<!-- Repository to file in: IronbellyOrg/Coder. The Coder repo was NOT touched by the IronClaude work described here. -->

## What was tried

IronClaude issue #315 ("agent-spawned worktree sessions stuck at the ccsession Session name prompt") was split into an IronClaude part and a Coder part. The IronClaude part is built (branch `ironbelly/issue-315-ccsession-name-prompt`, pull request listed below). **The Coder repo was not touched**: nothing in it was read for writing, changed, branched or filed from the IronClaude side. Everything below that names a Coder file comes from the approved plan on issue #315 and could not be checked from the IronClaude checkout.

What IronClaude now guarantees (each guarantee names the unit tests in `tests/unit/test_ccsession_tag.py` that prove it, and `tests/unit/test_ccsession_tiers.py` for tier mode):

1. **One question rule.** `ccsession-orca` asks for a session name only when Claude starts with no task, no name and no resume, and someone can answer (stdin, stdout and standard error are terminals, `CCSESSION_AUTOSTART` is not `0`). A prompt, `--prefill`, `--session-id`, `-p`, `CCSESSION_NAME`, Claude's own `--name`/`-n`, and `--resume`/`-r`/`--continue`/`-c`/`--fork-session`/`--from-pr` all skip it. Tests: `test_orca_launch_with_a_prompt_is_auto_named_and_never_asked`, `test_orca_prompt_reaches_claude_unchanged_and_is_never_a_label`, `test_orca_prefill_passes_through_and_its_text_is_not_a_flag`, `test_orca_session_id_launch_carries_a_task_and_is_auto_named`, `test_orca_print_mode_is_untagged_and_never_asked`, `test_orca_resume_skips_the_question` (resume, `-r`, `--continue`, `--fork-session`, `--from-pr`), `test_orca_claude_name_is_kept_once_and_never_asked`, `test_orca_without_a_terminal_never_asks`, `test_orca_autostart_off_never_asks`, `test_orca_keys_already_typed_skip_the_question`.
2. **Automatic names.** Enter at the question, no answer within the limit, keys typed ahead, no terminal, and every launch that carries a task get a valid, unique name `<folder>-<up to 4 task words>-<MMDD-HHMMSS>-<4 hex>`, never equal to a saved name; if the name list cannot be written, Claude starts untagged. Tests: `test_orca_enter_gets_an_auto_name`, `test_orca_unanswered_question_is_auto_named`, `test_auto_name_is_valid_and_shell_safe_for_any_text`, `test_auto_name_uses_at_most_four_words_of_twelve_characters`, `test_auto_name_stays_short_and_keeps_its_stamp_for_a_long_folder`, `test_auto_name_never_equals_a_saved_name`, `test_auto_name_prints_nothing_when_the_name_list_cannot_be_written`, `test_orca_launch_with_nothing_and_no_terminal_is_auto_named`, `test_orca_auto_named_session_is_listed_once_the_session_hook_records_it`, and in tier mode `test_orca_launch_with_a_prompt_in_tier_mode_is_auto_named_and_goes_through_the_shim` (`test_ccsession_tiers.py`).
3. **30-second limit inside the question.** `ccsession --ask` itself gives up after `CCSESSION_ASK_TIMEOUT` seconds (default 30; `0` or a value that is not a whole number of seconds waits for ever) for every caller, and exits 1. Tests: `test_ask_default_limit_is_30_seconds_and_shown_in_the_question`, `test_ask_gives_up_after_the_limit_with_exit_1`, `test_ask_limit_0_waits_for_ever_and_drops_the_limit_from_the_question`, `test_ask_hint_placeholder_follows_the_limit`, `test_orca_ask_question_hint_follows_the_limit_and_the_timeout_auto_names`.
4. **Ctrl+C exits 130 and starts no Claude.** `ccsession-orca` ends with status 130 and does not start Claude; the terminal is back in line mode. **A wrapper that calls `ccsession-orca` must therefore return to the shell on status 130 and must not fall through to a plain `claude`.** Tests: `test_orca_ctrl_c_cancels_without_starting_claude`, `test_orca_ctrl_c_while_line_mode_is_off_restores_the_terminal`, `test_ask_ctrl_c_while_line_mode_is_off_exits_130_and_restores`, `test_ask_ctrl_c_while_pasted_text_is_collected_exits_130_and_restores`.
5. **Exit statuses of `ccsession --ask`.** `0` a name, or an empty line for a blank answer (including a line of only spaces or tabs); `1` it did not ask (no terminal, or keys already waiting), the limit passed, or input ended; `3` the typed text cannot be a name (a control character among other text, too long to save, or several lines pasted after a non-blank first line), printed as typed; `130` Ctrl+C. `ccsession-orca` hands exit-3 text to Claude as its first message (after `--` when it starts with `-`) and auto-names the launch. Tests: `test_ask_a_line_that_cannot_be_a_name_exits_3_and_prints_it_as_typed`, `test_ask_a_name_with_spaces_is_a_name`, `test_ask_a_blank_line_means_enter`, `test_ask_star_lists_the_saved_sessions_and_asks_again`, `test_ask_is_not_asked_when_keys_are_already_waiting`, `test_ask_prints_only_the_name_on_stdout`, `test_orca_a_line_that_cannot_be_a_name_goes_to_claude_as_a_message`, `test_orca_typed_text_that_cannot_be_a_name_is_claudes_first_message`.
6. **`CCSESSION_NAME` and `CCSESSION_AUTOSTART=0`.** `CCSESSION_NAME=<name>` names a session without a prompt, with no question; an invalid value is dropped with a warning and Claude still starts; a value equal to a saved label resumes that session, loudly. A valid value names the session whatever the launch is, so set it only on a launch that starts a new session. `CCSESSION_AUTOSTART=0` starts untagged and asks nothing. Neither `CCSESSION_NAME` nor `CCSESSION_ASK_TIMEOUT` reaches the Claude that `ccsession-orca` starts. Tests: `test_orca_ccsession_name_names_the_session_and_is_never_asked`, `test_orca_invalid_ccsession_name_never_stops_claude`, `test_orca_ccsession_name_equal_to_a_saved_label_resumes_it_loudly`, `test_orca_ccsession_name_longer_than_the_limit_is_dropped_not_cut`, `test_orca_saved_name_in_ccsession_name_resumes_before_the_prompt`, `test_orca_autostart_off_with_no_task_is_untagged_and_never_asked`, `test_orca_reopen_leaves_the_name_and_the_limit_out_of_claudes_environment`.
7. **Launch-path table.** The path-by-path results of the `-k orca` run recorded in `launch-paths.md` are in `.dev/tasks/done/TASK-WF-fixGitHubIssue31-20261105-031410/artifacts/launch-paths.md` of the IronClaude branch (it is in the pull request). The pull-request-355 plain relaunch still reopens the tab's own session first, before the question and before any automatic name: `test_orca_relaunch_reopens_the_tabs_named_session`, `test_orca_relaunch_reopens_an_untagged_session_by_id`, `test_orca_a_new_tab_or_a_rerun_is_still_asked`.

Behaviour change to know about: because the 30-second limit now lives in `ccsession --ask`, **any caller of `ccsession --ask` that relied on the old no-limit default** (the New Terminal hook is the one the plan names) gives up after 30 seconds and starts without a name, unless it sets `CCSESSION_ASK_TIMEOUT=0`. Retiring the hook (below) makes that moot.

Dependency to know about: orchestrators that start workers through `ccsession-orca` must always pass the task (a prompt argument) or a name (`CCSESSION_NAME`). Without either, on a terminal the worker waits at the question until the limit (then is auto-named); with no terminal it is auto-named at once. IronClaude documents this in `src/superclaude/skills/ccsession-tag/README.md` (section "Claude launched from Orca") and does not enforce it.

Open exception: Claude Agent Teams starts its teammates from inside Claude Code, without running `ccsession-orca`, so ccsession cannot name those sessions or ask about them. It is documented in the README and recorded as a follow-up of #315. Keep it in mind when changing the `claude` wrapper: a wrapper can only help where the teammate launch goes through `claude` on the `PATH`, which was not checked.

## Relevant files and links

- IronClaude issue: https://github.com/IronbellyOrg/IronClaude/issues/315 (plan comments of 2026-11-03 and 2026-11-04, owner takeover 2026-11-05).
- IronClaude branch: `ironbelly/issue-315-ccsession-name-prompt`; pull request: https://github.com/IronbellyOrg/IronClaude/pull/PR_NUMBER_TO_FILL
- IronClaude files changed: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/ccsession-orca`, `src/superclaude/skills/ccsession-tag/README.md`, `tests/unit/test_ccsession_tag.py`, `tests/unit/test_ccsession_tiers.py`, `CHANGELOG.md` (Unreleased, "#315"), `docs/testing/v5.0.0/user/D08-ccsession.md`.
- Coder files to change (named by the plan; not checked from IronClaude):
  - `templates/VSCode-AIDev02/lib/aidev/ccsession-autostart.sh`: retire it, so a New Terminal is a plain shell and no hook asks for a session name.
  - The `/usr/local/bin/claude` wrapper from Coder #358: hand off to `ccsession-orca` (resolve it like `ccsession`, from `~/.local/bin`), pass every argument through unchanged, and `exit` with `ccsession-orca`'s status, **including 130 (Ctrl+C), without starting a plain `claude`**. If `ccsession-orca` is missing or not executable, fall back to the plain `claude` as today.
- Where to read the behaviour: `src/superclaude/skills/ccsession-tag/README.md`, section "Claude launched from Orca" (the one question rule, the launch-path table, automatic names, the time limit, `CCSESSION_NAME`); `ccsession --help` for the `--ask` exit statuses.

## Done when

- A New Terminal in a Coder workspace opens a plain shell: no `Session name` question, no hook calling `ccsession --ask`.
- A bare `claude` typed in a terminal goes through `ccsession-orca` and follows the one question rule (asks only when it has no task, no name and no resume; auto-names otherwise).
- Ctrl+C at the question returns to the shell and does not start Claude; any other `ccsession-orca` exit status is passed through.
- An agent or worker started with a prompt or with `CCSESSION_NAME` never waits at a name question (checked by starting one and seeing it reach Claude without input).
- The Claude Agent Teams exception is either handled or recorded as a known limitation in the Coder docs.

## Who it is for

The maintainers of IronbellyOrg/Coder who own the workspace template (`templates/VSCode-AIDev02`) and the `claude` wrapper from Coder #358; to be filed as an issue in IronbellyOrg/Coder by the coordinator. The IronClaude pull request must be merged and installed in the workspace image first (`superclaude install` provides `ccsession-orca`).
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty):

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
