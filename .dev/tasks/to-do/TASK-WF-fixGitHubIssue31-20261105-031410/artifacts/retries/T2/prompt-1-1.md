b05660e850bd7cacf711c37b34406e78c981f52a
Review one task for spec compliance.

Task brief: ## Task 2: Move the 30-second limit into the question and add the not-a-name outcome

Depends on: Task 1

Edit `ask_session_name` in src/superclaude/skills/ccsession-tag/ccsession. The default of `CCSESSION_ASK_TIMEOUT` becomes 30 inside the function (a value of 0 still waits forever, a non-number still means no limit as today), so every caller gets the timer. The default hint becomes "Enter = auto-named, Ctrl+C = cancel; auto-named after 30s" (the 30 follows the actual limit). Keep exit 130 on Ctrl+C with the terminal mode restored, exit 1 for not asked, timeout, end of input and keys already waiting. Add the narrow safety net: when the typed line contains a control character, or is longer than 245 bytes as a file name, or more bytes are already waiting after the line (a pasted multi-line text), ask_session_name reads the rest of the waiting text, prints the whole text on stdout and exits 3 instead of asking again. A blank line, `*`, and an ordinary invalid name keep their current behaviour (blank means Enter, `*` lists every worktree, other invalid names ask again with the reason). Update the `--ask` description in the ccsession header comment and help (around the lines that describe `--ask`) with the exit statuses 0, 1, 3 and 130.

Acceptance criteria:
- T2.AC1: `ccsession --ask` on a pseudo-terminal with no CCSESSION_ASK_TIMEOUT set and no input exits 1 after about 30 seconds (the test sets the limit to 1 second through the environment to stay fast) and shows the default hint with the limit.
- T2.AC2: Ctrl+C at the question exits 130 and leaves the terminal in line mode, as the existing `test_ask_ctrl_c_while_line_mode_is_off_exits_130_and_restores` still requires.
- T2.AC3: A line of 246 x characters, a line holding a tab, and a two-line paste each make `ccsession --ask` print the text on stdout and exit 3; the line `my fix plan` (spaces) is printed and exits 0 as a name.
- T2.AC4: Keys already waiting before the question still return exit 1 without a question.
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
Start sha: b05660e850bd7cacf711c37b34406e78c981f52a
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/ccsession b/src/superclaude/skills/ccsession-tag/ccsession
index 4473c512..8c8c2f47 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession
+++ b/src/superclaude/skills/ccsession-tag/ccsession
@@ -55,10 +55,17 @@
 #   ccsession --ask [<hint>]  List saved sessions as --here does, ask for a session
 #                             name and print it (empty: untagged; "*" lists every
 #                             worktree's sessions and asks again). The hint goes
-#                             in the question's brackets. Exit 1: not asked (no
-#                             terminal, or keys already waiting), no answer within
-#                             CCSESSION_ASK_TIMEOUT seconds (unset or 0: no
-#                             limit), or end of input; exit 130: Ctrl+C
+#                             in the question's brackets; "@LIMIT@" in it is the
+#                             time limit in seconds. Exit codes:
+#                             0  a name, or empty (untagged) on a blank answer;
+#                             1  not asked (no terminal, or keys already
+#                                waiting), no answer within CCSESSION_ASK_TIMEOUT
+#                                seconds (default 30; 0: no limit), or end of input;
+#                             3  the typed text cannot be a name (a control
+#                                character, too long to save as a file name, or
+#                                several lines pasted): it is printed as typed, as
+#                                a first message for Claude, not as a name;
+#                             130 Ctrl+C
 #   ccsession --auto-name [<task text>]
 #                             Print a unique session label for a launch with no
 #                             name: folder name, up to four words of the task
@@ -1469,7 +1476,8 @@ ask_session_name() {
   # ccsession --ask: the session-name question for a person opening a terminal
   # (ccsession-orca, the Coder New Terminal hook). The list and the question go
   # to stderr, so a caller reads the answer with name=$(ccsession --ask).
-  local hint="${1:-Enter = untagged, Ctrl+C = plain shell}"
+  # "@LIMIT@" in a hint is the time limit in seconds (see below).
+  local hint="${1:-Enter = untagged, Ctrl+C = plain shell; gives up after @LIMIT@s}"
   [ -t 0 ] && [ -t 2 ] || return 1
   # Keys already waiting (an agent or paste is typing): leave them to whatever
   # runs next. A line-mode terminal only reports complete lines as readable, so
@@ -1517,32 +1525,94 @@ ask_session_name() {
     printf '%sSessions from other repos and folders: ccsession --list%s\n\n' "$dim" "$reset" >&2
   }
   show_saved worktree "Saved sessions in ${PWD/#"$HOME"/\~}"
-  # A caller with something waiting on it (Orca's supervised workers time out
-  # at 60s) sets CCSESSION_ASK_TIMEOUT so an unanswered question gives up.
-  local read_opts=() limit="${CCSESSION_ASK_TIMEOUT:-0}"
+  # Every question gives up after CCSESSION_ASK_TIMEOUT seconds (default 30;
+  # 0 waits for ever): Orca fails a supervised worker whose Claude is not ready
+  # within 60 seconds, and an unanswered question must not outlast that.
+  local read_opts=() limit="${CCSESSION_ASK_TIMEOUT:-30}"
   case "$limit" in
-    '' | *[!0-9]* | 0) : ;;
+    '' | *[!0-9]* | 0) limit=0 ;;
     *) read_opts=(-t "$limit") ;;
   esac
+  if [ "$limit" = 0 ]; then
+    # No limit: drop the "; ... @LIMIT@ ..." part of the hint.
+    case "$hint" in *"; "*@LIMIT@*) hint=${hint%%"; "*@LIMIT@*} ;; esac
+  else
+    hint=${hint//@LIMIT@/$limit}
+  fi
   # Ctrl+C ends the question with its own status; the line after ^C stays clean.
   trap 'echo >&2; exit 130' INT
-  # A name that is not a valid label asks again (validate_label says why).
-  # ccsession-orca passes the answer as --name, so even a name that starts
-  # with "-" is a name, never an option.
+  # What the person typed is a name, with one narrow exception that needs no
+  # guessing: a line that cannot be a name (a control character, or too long to
+  # save as a file name) or a paste of several lines is not a name but a first
+  # message for Claude. It is printed as it was typed and the status is 3.
+  # Anything else that is not blank is a name, spaces included. A name that is
+  # not a valid label asks again (validate_label says why). ccsession-orca
+  # passes the answer as --name, so even a name that starts with "-" is a name,
+  # never an option.
+  local line rest msg file
   while :; do
-    read -r ${read_opts[@]+"${read_opts[@]}"} -p "Session name ($hint): " name ||
+    # IFS= keeps the line exactly as typed (a leading or trailing tab is a
+    # control character, not blank space to trim away).
+    IFS= read -r ${read_opts[@]+"${read_opts[@]}"} -p "Session name ($hint): " line ||
       { echo >&2; return 1; }
-    [ -z "$name" ] && break
+    name=$line
+    case "$name" in
+      *[![:space:]]*) ;;
+      *) name=""; break ;;
+    esac
     if [ "$name" = "*" ]; then
       show_saved "" "Saved sessions in every worktree of this repo"
       continue
     fi
+    # More text arriving right behind the line is a paste (several lines).
+    rest=$(ask_drain_waiting)
+    file=$(name_to_file "$line")
+    if [ -n "$rest" ] || [[ "$line" == *[[:cntrl:]]* ]] ||
+      [ "$(printf '%s' "$file" | wc -c)" -gt 245 ]; then
+      msg=$line
+      [ -n "$rest" ] && msg="$line"$'\n'"$rest"
+      trap - INT
+      printf '%s' "$msg"
+      return 3
+    fi
+    # Surrounding spaces are not part of a name.
+    name=${name#"${name%%[![:space:]]*}"}
+    name=${name%"${name##*[![:space:]]}"}
     validate_label "$name" >/dev/null && break
   done
   trap - INT
   printf '%s\n' "$name"
 }
 
+ask_drain_waiting() {
+  # Print the text that arrives within 150 ms of the last line (a paste), up to
+  # 128 KiB, as raw bytes; nothing when none arrives or python3 is missing. A
+  # line-mode terminal only reports complete lines as readable, so line mode is
+  # briefly off (the saved mode is put back; Ctrl+C is handled by the caller's
+  # trap, which restores it too). python3, not `read -t 0.15`: bash 3.2 (macOS)
+  # does not take fractions.
+  local mode="" data=""
+  mode=$(stty -g 2>/dev/null) || mode=""
+  [ -n "$mode" ] && stty -icanon min 0 time 0 2>/dev/null
+  data=$(python3 -c '
+import os, select, sys
+buf = b""
+wait = 0.15
+while len(buf) < 131072:
+    ready = select.select([0], [], [], wait)[0]
+    if not ready:
+        break
+    chunk = os.read(0, 65536)
+    if not chunk:
+        break
+    buf += chunk
+    wait = 0.1
+sys.stdout.buffer.write(buf[:131072])
+' 2>/dev/null) || data=""
+  [ -n "$mode" ] && stty "$mode" 2>/dev/null
+  printf '%s' "$data"
+}
+
 show_help() {
   awk 'NR >= 2 { if ($0 ~ /^# The wrapper always runs/) exit; sub(/^# ?/, ""); print }' "$0"
   if [ "$TIER_MODE" = 1 ]; then
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
