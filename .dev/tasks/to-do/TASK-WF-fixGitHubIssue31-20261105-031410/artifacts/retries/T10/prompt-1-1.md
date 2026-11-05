66f369dd3f39c96c30a26fe974e68d3669b2d070
Review one task for spec compliance.

Task brief: ## Task 10: Update the CHANGELOG and the v5.0.0 ccsession test guide

Depends on: Task 9

Add an Unreleased entry to CHANGELOG.md for the fix (title with the issue number 315), and update docs/testing/v5.0.0/user/D08-ccsession.md wherever it pins the old behaviour (`--ask` with no limit, `CCSESSION_AUTOSTART`, Enter or Ctrl+C starting untagged, the 30-second untagged start, around lines 240 to 250). Also correct the CHANGELOG line that describes the old Orca question behaviour only if it is in the Unreleased section; released history stays as written.

Acceptance criteria:
- T10.AC1: CHANGELOG.md Unreleased lists the change and issue 315; released sections are unchanged (checked with `git diff` showing only Unreleased lines added).
- T10.AC2: D08-ccsession.md steps and expected results match the tested behaviour for Enter, timeout, Ctrl+C and prompt-bearing launches.
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
Start sha: 66f369dd3f39c96c30a26fe974e68d3669b2d070
Diff against the start snapshot: diff --git a/CHANGELOG.md b/CHANGELOG.md
index 6a38dccc..40fd501e 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,28 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### ccsession: agents no longer get stuck at the session name question (#315)
+
+#### Fixed (ccsession name question)
+
+- An agent or worker started through `ccsession-orca` with a task could stop at `Session name (...)` and wait for a person. The question is now asked only when Claude starts with no task, no name and no resume. A prompt, `--prefill`, `--session-id`, `-p`, `CCSESSION_NAME`, Claude's own `--name`/`-n`, and `--resume`/`--continue`/`--fork-session`/`--from-pr` all skip it.
+- `--fork-session` and `--from-pr` now skip the question like `--resume`. The README said `--fork-session` did; the code still asked.
+- `ccsession --ask` had a time limit only inside `ccsession-orca`. The limit now lives in the question itself: `CCSESSION_ASK_TIMEOUT` seconds, default 30, `0` waits for ever, and the question shows it. Every caller gets it, the Coder New Terminal hook included.
+- Ctrl+C at the question now ends `ccsession-orca` with status 130 and starts no Claude (it used to start an untagged session). `ccsession --ask` restores the terminal on Ctrl+C at every point, including while it collects pasted text.
+- The tab-reopen path of `ccsession-orca` no longer passes `CCSESSION_NAME` or `CCSESSION_ASK_TIMEOUT` on to Claude Code.
+
+#### Added (ccsession automatic names)
+
+- A `ccsession-orca` launch that starts a new session without a name (not a resume, not print mode, not `CCSESSION_AUTOSTART=0`, not `--version` or a subcommand) gets a valid automatic one: Enter at the question, no answer within the limit, keys typed ahead, no terminal, and every launch that carries a task. The label is `<folder>-<up to four words of the task>-<MMDD-HHMMSS>-<4 hex>`, only letters, digits and hyphens, checked against the saved names, and it appears in `ccsession --here` once the session starts. If the name list cannot be written, Claude starts untagged instead of stopping.
+- `ccsession --auto-name [<task text>]` prints such a label; `ccsession --check-name <name>` exits 0 for a valid name.
+- `CCSESSION_NAME=<name>` in the environment names a session without a prompt (for orchestrators). An invalid value is dropped with a warning and Claude still starts; a value equal to a saved label resumes that session, loudly.
+- `ccsession --ask` exits 3 and prints the text as typed when the line cannot be a name (a control character among other text, too long to save, or several lines pasted); `ccsession-orca` passes that text to Claude as its first message and auto-names the launch. A normal line, spaces included, stays a name. A hint may contain `@LIMIT@`, replaced by the time limit.
+
+#### Changed (ccsession name question)
+
+- The question in `ccsession-orca` reads `Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s):`. Enter and the time limit start an automatically named session; they no longer start an untagged one. Print mode (`-p`), `CCSESSION_AUTOSTART=0`, `--version`, `--help` and Claude subcommands (`mcp`, `doctor`...) still start untagged and ask nothing.
+- The README and `docs/testing/v5.0.0/user/D08-ccsession.md` describe the one question rule, the launch paths and the one documented exception: Claude Agent Teams starts its teammates itself, without `ccsession-orca`, so those sessions are not named (follow-up). Orchestrators should always pass the task or a name.
+
 ### Install: harden the pinned-plugin install (#360 follow-ups)
 
 #### Fixed (plugin install)
diff --git a/docs/testing/v5.0.0/user/D08-ccsession.md b/docs/testing/v5.0.0/user/D08-ccsession.md
index 7656a25e..cd3dcc33 100644
--- a/docs/testing/v5.0.0/user/D08-ccsession.md
+++ b/docs/testing/v5.0.0/user/D08-ccsession.md
@@ -1,8 +1,8 @@
 # E2E Test Guide — `ccsession` (`5.0.0`)
 
-- **Capability:** `ccsession <name>` starts or resumes a Claude Code session under a name that ccsession, Claude Code (`--name`, `/rename`) and the Orca tab share; names belong to the repo and the lists follow the worktree (`--here`, `--here --all`, `--list`, `--rm`, `--ask`); `ccsession-orca` is Orca's Claude command; in a Coder workspace with tier settings, `--tier`, `--model`, `--models-status` and `--refresh-models` pick and inspect the gateway models; the shared gateway shim keeps running when the terminal that started it closes (#341).
+- **Capability:** `ccsession <name>` starts or resumes a Claude Code session under a name that ccsession, Claude Code (`--name`, `/rename`) and the Orca tab share; names belong to the repo and the lists follow the worktree (`--here`, `--here --all`, `--list`, `--rm`, `--ask`); `ccsession-orca` is Orca's Claude command (one question rule, automatic names, a 30-second limit, Ctrl+C cancels; #315); in a Coder workspace with tier settings, `--tier`, `--model`, `--models-status` and `--refresh-models` pick and inspect the gateway models; the shared gateway shim keeps running when the terminal that started it closes (#341).
 - **Audience:** end user
-- **Source of truth:** `src/superclaude/skills/ccsession-tag/ccsession:7-93,119-174,267-313,320-412,479-508,555-629,681-701,756-900,936-971,1220-1468,1508-1617`; `src/superclaude/skills/ccsession-tag/ccsession-orca:19-81`; `src/superclaude/skills/ccsession-tag/hooks/session-name.sh:7-18,162-199`; `src/superclaude/skills/ccsession-tag/models.py:53-65,255-328,454-496,630-673,831-1028`; `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:525-540,857-867`; `src/superclaude/hooks/hooks.json:33-42,54-73`; `src/superclaude/cli/doctor.py:57-131`; `CHANGELOG.md:11-22,56-76,151-204`; `docs/testing/v5.0.0/c-e2e-transcript.txt:218,342,353-354`; issue [#352](https://github.com/IronbellyOrg/IronClaude/issues/352)
+- **Source of truth:** `src/superclaude/skills/ccsession-tag/ccsession:7-93,119-174,267-313,320-412,479-508,555-629,681-701,756-900,936-971,1220-1468,1508-1617`; `src/superclaude/skills/ccsession-tag/ccsession-orca` (whole file; the `ccsession:` line numbers in this guide were taken before #315 and have moved for the code after the first 600 lines, so search the quoted text); `src/superclaude/skills/ccsession-tag/hooks/session-name.sh:7-18,162-199`; `src/superclaude/skills/ccsession-tag/models.py:53-65,255-328,454-496,630-673,831-1028`; `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:525-540,857-867`; `src/superclaude/hooks/hooks.json:33-42,54-73`; `src/superclaude/cli/doctor.py:57-131`; `CHANGELOG.md:11-22,56-76,151-204`; `docs/testing/v5.0.0/c-e2e-transcript.txt:218,342,353-354`; issue [#352](https://github.com/IronbellyOrg/IronClaude/issues/352)
 - **Est. time:** `Tier A: 3 minutes. Tier B: 25-35 minutes. Tier C: 20-40 minutes (Orca needed for Step 17).`
 
 ## Preconditions
@@ -26,8 +26,8 @@
 ## What you're verifying
 
 - One name per session: `ccsession <name>` (spaces allowed, `--name` for a name starting with `-`) is also Claude Code's `--name`; a `/rename` inside Claude Code reaches ccsession's list at the next message.
-- Names belong to the repo, and the lists follow the worktree: `--here` lists this worktree's sessions, then those whose worktree was removed, and counts the others; `--here --all` and `--list` show everything; `--rm` forgets a name; `--ask` asks for a name and exits 1 or 130 when it gets none.
-- In Orca, ccsession owns the tab title (`<name> · Claude Code`), and `ccsession-orca` asks for a name only when someone can answer.
+- Names belong to the repo, and the lists follow the worktree: `--here` lists this worktree's sessions, then those whose worktree was removed, and counts the others; `--here --all` and `--list` show everything; `--rm` forgets a name; `--ask` asks for a name, gives up after 30 seconds (exit 1), exits 130 on Ctrl+C, and exits 3 for text that cannot be a name.
+- In Orca, ccsession owns the tab title (`<name> · Claude Code`), and `ccsession-orca` asks for a name only when Claude starts with no task, no name and no resume and someone can answer; every other launch that needs a name gets an automatic one.
 - The gateway shim no longer dies with the terminal that started it.
 - In tier mode, `--help`, `--models-status`, `--tier`, `--model` and `--refresh-models` behave as the code says.
 
@@ -246,6 +246,7 @@ D8_EXTRA=CCSESSION_ASK_TIMEOUT=3 d8 ccsession --ask; echo "exit=$?"  # type noth
 d8 ccsession --ask; echo "exit=$?"                                   # press Ctrl+C
 d8 ccsession --ask; echo "exit=$?"                                   # press Ctrl+D
 d8 ccsession --ask </dev/null; echo "exit=$?"                        # no terminal
+d8 ccsession --ask; echo "exit=$?"                                   # paste two lines at once (paste, do not type)
 ```
 
 **Expected result:** every question starts with this list on the terminal (source: `ccsession:1345-1375`):
@@ -259,18 +260,21 @@ Sessions whose worktree was removed (they continue here):
 1 more session in other worktrees of this repo: type * to list them
 Sessions from other repos and folders: ccsession --list
 
-Session name (Enter = untagged, Ctrl+C = plain shell):
+Session name (Enter = untagged, Ctrl+C = plain shell; gives up after 30s):
 ```
 
+(The question gives up after `CCSESSION_ASK_TIMEOUT` seconds, 30 by default, and the question shows the limit; `0` waits for ever and the hint then has no limit. Source: `ccsession:1546-1559`.)
+
 (`-dash name` is not listed: in Step 7, with its conversation gone, ccsession deleted the name, and the stand-in did not save the new one (source: `ccsession:1584-1590`). `my work-2` was removed with `--rm` (source: `ccsession:1454-1468`).)
 
 1. `picked one` printed on its own line, `exit=0`: only the chosen name goes to standard output (source: `ccsession:1388-1399`; `CHANGELOG.md:199`).
-2. An empty line, `exit=0`: Enter means untagged (source: `ccsession:1389-1391,1399`).
+2. An empty line, `exit=0`: Enter is an empty answer. `ccsession --ask` itself treats it as "no name"; `ccsession-orca` turns it into an automatic name (Step 11). A line of only spaces or tabs is an empty answer too.
 3. `*` prints `Saved sessions in every worktree of this repo (type a name to resume it):` with `my work`, `wt2 task` and `wt3 task`, then asks again; Enter gives an empty line and `exit=0` (source: `ccsession:1392-1395`).
-4. After 3 seconds an empty line and `exit=1` (source: `ccsession:1376-1390`).
+4. The question shows `gives up after 3s` and, after 3 seconds, an empty line and `exit=1` (source: `ccsession:1549-1559`).
 5. `^C`, then `exit=130` (source: `ccsession:1383-1384`).
 6. `exit=1`: end of input (source: `ccsession:1389-1390`).
 7. Nothing printed, `exit=1`: no terminal, no question (source: `ccsession:1329`; help `ccsession:47-53`).
+8. The two pasted lines come back on standard output as typed, `line one` and then `line two` followed directly by `exit=3` (the text has no final newline): text that cannot be a name is not a name. `ccsession-orca` hands it to Claude Code as its first message (source: `ccsession:1576-1604`; help `ccsession:64-68`). The same exit 3 happens for a line with a tab between words and for a line too long to save (more than 245 bytes of file name); a line of only tabs is `exit=0`.
 
 **Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`
 
@@ -325,7 +329,7 @@ Use an Orca terminal tab for this step if you have Orca (Orca kills a closed tab
 
 **Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`
 
-#### Step 11 — `ccsession-orca` asks only when someone can answer `[LOCAL-WRITE]`
+#### Step 11 — `ccsession-orca` asks only when Claude starts with no task, no name and no resume `[LOCAL-WRITE]`
 
 **Do:**
 
@@ -333,15 +337,22 @@ Use an Orca terminal tab for this step if you have Orca (Orca kills a closed tab
 d8 ccsession-orca </dev/null 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
 d8 ccsession-orca --resume abc 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
 D8_EXTRA=CCSESSION_AUTOSTART=0 d8 ccsession-orca "fix the bug" --prefill x 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
+d8 ccsession-orca "fix the bug" 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
+D8_EXTRA=CCSESSION_NAME=worker-7 d8 ccsession-orca "do the work" 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
+d8 ccsession-orca -p "hello" 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
 d8 ccsession-orca
 ```
 
-At the last command's question, type `orca pick` and press Enter.
+At the last command's question, type `orca pick` and press Enter. Then run `d8 ccsession-orca` again and press Enter at the question; then once more and press Ctrl+C (run it as `d8 ccsession-orca; echo "exit=$?"`).
 
 **Expected result:**
 
-- The first three each print `[ccsession] Shim already running on 127.0.0.1:4890 (reusing)`, the pre-load warning, `[ccsession] Starting untagged session`, and then the args: `[--dangerously-skip-permissions] [--allowedTools=Grep]` (no terminal: no question); `... [--resume] [abc]` (Orca resuming: no question); `... [fix the bug] [--prefill] [x]` (`CCSESSION_AUTOSTART=0`: no question). Orca's own arguments reach Claude Code unchanged, after `--claude-args`, and every launch goes through the shim (source: `ccsession-orca:19-24,44-59,76-81`; `CHANGELOG.md:198`).
-- The last one shows the Step 8 list, then `Session name (Enter or Ctrl+C = untagged; untagged after 30s):` (source: `ccsession-orca:62-72`). After `orca pick`: the reuse line, a Python error report from the gateway pre-load ending in a connection error, the pre-load warning (both expected here), `[ccsession] Starting new session labeled 'orca pick'` and `FAKE-CLAUDE args: [--dangerously-skip-permissions] [--allowedTools=Grep] [--name] [orca pick]` (source: `ccsession-orca:77-79`). Pressing Enter, Ctrl+C or waiting 30 seconds instead starts an untagged session (`ccsession-orca:72,81`).
+- The first line prints `[ccsession] Shim already running on 127.0.0.1:4890 (reusing)`, the pre-load warning, `[ccsession] Starting new session labeled 'repo-<MMDD>-<HHMMSS>-<4 hex>'` and the args `[--dangerously-skip-permissions] [--allowedTools=Grep] [--name] [repo-<MMDD>-<HHMMSS>-<4 hex>]`: no terminal, nobody to ask, so the launch gets an automatic name (the folder, then the stamp).
+- The second prints the reuse line, the pre-load warning, `[ccsession] Starting untagged session` and `... [--resume] [abc]`: Orca resuming names itself, no question, no label. The third prints the same with `... [fix the bug] [--prefill] [x]`: `CCSESSION_AUTOSTART=0` stays untagged. The sixth prints `... [-p] [hello]` after `Starting untagged session`: print mode stays untagged.
+- The fourth prints `Starting new session labeled 'repo-fix-the-bug-<MMDD>-<HHMMSS>-<4 hex>'` and `... [--name] [repo-fix-the-bug-...] [fix the bug]`: a launch that carries a task gets an automatic name made from its first words, no question. The fifth prints `Starting new session labeled 'worker-7'` and `... [--name] [worker-7] [do the work]`: `CCSESSION_NAME` names the session.
+- Orca's own arguments reach Claude Code unchanged, after `--claude-args`, and every launch goes through the shim (source: `ccsession-orca`, header and the launch classification; README, "The one question rule").
+- The last command shows the Step 8 list, then `Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s):`. After `orca pick`: the reuse line, a Python error report from the gateway pre-load ending in a connection error, the pre-load warning (both expected here), `[ccsession] Starting new session labeled 'orca pick'` and `FAKE-CLAUDE args: [--dangerously-skip-permissions] [--allowedTools=Grep] [--name] [orca pick]`.
+- Enter, or waiting 30 seconds, starts a session under an automatic name (`Starting new session labeled 'repo-<MMDD>-<HHMMSS>-<4 hex>'`), not an untagged one. Ctrl+C prints `exit=130` and no `FAKE-CLAUDE` line: Claude is not started.
 
 **Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`
 
@@ -536,14 +547,14 @@ Skip this step (mark N/A) without Orca.
 3. At the question type `d08 orca` and press Enter. Note the tab title.
 4. In the session `/rename d08 orca2`, then `Reply with OK. Do not use any tools.`. Note the tab title.
 5. `/exit`. Note the tab title.
-6. Start Claude with **+** again and press Enter at the question; note the title; `/exit`.
+6. Start Claude with **+** again and press Enter at the question; note the title; `/exit`. Then start Claude with **+** once more and press Ctrl+C at the question; note what happens.
 
 **Expected result:**
 
-- Step 3: the tab shows the saved-session list (`d08 renamed` among them) and `Session name (Enter or Ctrl+C = untagged; untagged after 30s):`; after the answer the session starts with that name and the tab title is `d08 orca · Claude Code` (source: `ccsession-orca:19-28,62-79`; `ccsession:1508-1523`; `CHANGELOG.md:192,198`).
+- Step 3: the tab shows the saved-session list (`d08 renamed` among them) and `Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s):`; after the answer the session starts with that name and the tab title is `d08 orca · Claude Code` (source: `ccsession-orca`, the question; `ccsession:1508-1523`; `CHANGELOG.md:192,198`).
 - Step 4: after the reply, the title is `d08 orca2 · Claude Code`. It needs the `orca` command on that tab's `PATH` (source: `ccsession:479-491`; `hooks/session-name.sh:185-192`; `CHANGELOG.md:62`).
 - Step 5: the `d08 orca2 · Claude Code` title is taken off, unless you typed a title of your own into Orca since (source: `ccsession:493-508`; `hooks/session-name.sh:193-197`). UNVERIFIED: which title Orca shows then.
-- Step 6: an untagged session titled `Claude Code` (source: `ccsession:1521,1543-1544`; `ccsession-orca:81`).
+- Step 6: a session under an automatic name (`<folder>-<MMDD>-<HHMMSS>-<4 hex>`), and the tab title is `<that name> · Claude Code`; the question gave Enter an automatic name, it no longer starts an untagged session. Press Ctrl+C at the question instead and no Claude starts (`ccsession-orca` ends with status 130).
 - UNVERIFIED, not checked while this guide was written: whether the `orca` command still reaches Orca when `c8` sets `HOME` and unsets the `XDG_*` folders. ccsession runs `orca terminal rename` and `orca terminal show` for the Step 4 and Step 5 titles (`ccsession:479-508`). If those two titles do not change, write that down as a remark about this test setup, not as a ccsession FAIL. Orca's own files, outside `~/.claude`, are Orca's and are not part of this check.
 
 **Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`
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
