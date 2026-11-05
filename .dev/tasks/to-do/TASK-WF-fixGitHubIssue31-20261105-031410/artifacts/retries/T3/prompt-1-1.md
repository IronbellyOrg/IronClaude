917c4b9c0a62fb6671c68617e86bf0b8c090bf1e
Review one task for spec compliance.

Task brief: ## Task 3: Classify the launch and apply the one question rule in ccsession-orca

Depends on: Task 2

Edit src/superclaude/skills/ccsession-tag/ccsession-orca. Replace the single `ask` computation by a classification of the arguments (the existing `--prefill <text>` skipping stays: the text after --prefill is not an option). Resume-like: `--resume`, `--resume=*`, `-r`, `--continue`, `-c`, `--fork-session`, `--from-pr`, `--from-pr=*`. Name carried: `CCSESSION_NAME` in the environment (non-empty), or `--name <value>`, `--name=<value>`, `-n <value>` in the arguments; the value is lifted out of Claude's arguments and passed as ccsession's own `--name` (an exec of `ccsession --name <value> --shim --claude-args <remaining arguments>`), so it is not given twice. Task carried: any positional argument, `--prefill <text>`, `--session-id`, `-p`, `--print`. The question is asked only when stdin and stdout are terminals, CCSESSION_AUTOSTART is not 0, and the launch is not resume-like and carries no name and no task. Keep the pull request 355 reopen block ahead of everything else and driven by the same conditions as before (terminal, autostart, not resume-like, ORCA_PANE_KEY, plain options only), independent of the new rule. Remove the `trap ':' INT` and the exported default `CCSESSION_ASK_TIMEOUT` hint logic that duplicated the timer; the question reads its limit from ccsession. Update the header comment of the script to describe the new rule.

Acceptance criteria:
- T3.AC1: A launch with a positional prompt, `--prefill <text>`, `--session-id <id>`, `CCSESSION_NAME=x` or `--name x` on a terminal shows no question and no saved-session list.
- T3.AC2: A launch with `--name my demo` (two arguments, value `my demo`) reaches Claude with exactly one `--name my demo` in the arguments and the topic `my demo` in the fake Claude record.
- T3.AC3: The plain relaunch of an Orca tab (ORCA_PANE_KEY set, only Orca's options) still reopens the recorded session without a question, as the tests around the pull request 355 behaviour require.
- T3.AC4: A new tab with no argument on a terminal still shows the question.
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
Start sha: 917c4b9c0a62fb6671c68617e86bf0b8c090bf1e
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/ccsession b/src/superclaude/skills/ccsession-tag/ccsession
index b0c4bf6b..4aed0a91 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession
+++ b/src/superclaude/skills/ccsession-tag/ccsession
@@ -70,6 +70,8 @@
 #                             Print a unique session label for a launch with no
 #                             name: folder name, up to four words of the task
 #                             text, and a stamp (never a saved name; always valid)
+#   ccsession --check-name <name>
+#                             Exit 0 when <name> is a valid session name, else 1
 #   ccsession-orca [<claude args>]
 #                             Orca's Claude command: asks for a name, then starts
 #                             Claude through ccsession (see ccsession-orca)
@@ -650,6 +652,11 @@ case "${1:-}" in
     name_key
     exit 0
     ;;
+  --check-name)
+    # Exit 0 when the text is a valid session name, else 1 (ccsession-orca checks
+    # CCSESSION_NAME with it before using it).
+    if validate_label "${2:-}" >/dev/null 2>&1; then exit 0; else exit 1; fi
+    ;;
   --auto-name)
     # Before the argument loop below: task text such as --model or --tier=x is
     # text here, never an option of ccsession.
diff --git a/src/superclaude/skills/ccsession-tag/ccsession-orca b/src/superclaude/skills/ccsession-tag/ccsession-orca
index 88144422..0ec9dbdb 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession-orca
+++ b/src/superclaude/skills/ccsession-tag/ccsession-orca
@@ -9,26 +9,33 @@
 # Settings > Agents > Claude > Command to this file's absolute path, for
 # example /home/coder/.local/bin/ccsession-orca (Orca takes one executable, no
 # arguments). Each launch then gets ccsession's shim, model settings and single
-# credential, and is asked for a session name first, like a New Terminal.
+# credential.
 #
 # Orca's own arguments (a prompt, --prefill <text>, --resume <id>
 # [--fork-session]) reach Claude unchanged: they go after ccsession's
 # --claude-args, so a prompt is never read as a session name or a ccsession
 # option.
 #
-# The question (ccsession --ask) is asked only when someone can answer it:
-# stdin and stdout are terminals, Orca is not resuming or continuing a
-# session, and CCSESSION_AUTOSTART is not 0. A name starts or resumes that
-# ccsession. Enter, Ctrl+C, end of input, keys already waiting, or a question
-# that is not asked all start an untagged session: Orca expects Claude to
-# start in this tab, so it never ends up at a dead prompt.
+# One rule decides whether the session-name question is asked: only when Claude
+# starts with no task, no name and no resume.
+#   - Resume (--resume, -r, --continue, -c, --fork-session, --from-pr): the
+#     session names itself; no question.
+#   - Name carried: CCSESSION_NAME in the environment (the way an orchestrator
+#     names a session; used as the session's name when it is a valid name), or a
+#     Claude --name / -n in the arguments (left in the arguments for Claude as
+#     they are); no question.
+#   - Task carried: any prompt, --prefill <text>, --session-id, or -p / --print;
+#     no question.
+# The question (ccsession --ask) is also not asked when no one can answer it:
+# stdin and stdout are not both terminals, or CCSESSION_AUTOSTART is 0. A name
+# typed at the question starts or resumes that ccsession.
 #
 # When Orca relaunches a tab after a workspace restart, the tab reopens the
 # session it ran (the one the ccsession hooks recorded for its pane) instead of
 # asking: see the reopen step below.
 #
-# An unanswered question starts untagged after CCSESSION_ASK_TIMEOUT seconds
-# (default 30; 0 waits for ever). Orca also starts supervised workers with
+# The question gives up after CCSESSION_ASK_TIMEOUT seconds (ccsession's
+# default is 30; 0 waits for ever). Orca also starts supervised workers with
 # this command and fails one whose Claude is not ready within 60 seconds.
 
 set -e
@@ -45,30 +52,109 @@ while [ -L "$_self" ]; do
 done
 CCSESSION="$(cd "$(dirname "$_self")" && pwd)/ccsession"
 
-ask=1
-[ -t 0 ] && [ -t 1 ] || ask=0
-[ "${CCSESSION_AUTOSTART:-1}" = 0 ] && ask=0
-# A resume names its own session; a label would start a different one. The
-# --prefill value is text for the input box, never a flag.
-_skip=0
+# Classify the launch from the arguments. The text after --prefill, --session-id
+# and the value-taking options is a value, never a task or a flag.
+resume_like=0
+name_carried=0
+task_carried=0
+no_session=0
+task_text=""
+_expect=""
+_dd=0
 for _arg in "$@"; do
-  if [ "$_skip" = 1 ]; then
-    _skip=0
+  if [ -n "$_expect" ]; then
+    case "$_expect" in
+      prefill)
+        task_carried=1
+        [ -n "$task_text" ] || task_text=$_arg
+        ;;
+      name) name_carried=1 ;;
+    esac
+    _expect=""
+    continue
+  fi
+  if [ "$_dd" = 1 ]; then
+    task_carried=1
+    [ -n "$task_text" ] || task_text=$_arg
     continue
   fi
   case "$_arg" in
-    --prefill) _skip=1 ;;
-    --resume|--resume=*|-r|--continue|-c) ask=0 ;;
+    --) _dd=1 ;;
+    --prefill) _expect=prefill ;;
+    --prefill=*)
+      task_carried=1
+      [ -n "$task_text" ] || task_text=${_arg#--prefill=}
+      ;;
+    --resume | -r | --continue | -c | --fork-session | --from-pr) resume_like=1 ;;
+    --resume=* | --from-pr=*) resume_like=1 ;;
+    --name | -n) _expect=name ;;
+    --name=*) name_carried=1 ;;
+    --session-id)
+      task_carried=1
+      _expect=value
+      ;;
+    --session-id=*) task_carried=1 ;;
+    -p | --print) task_carried=1 ;;
+    -v | --version | -h | --help) no_session=1 ;;
+    --model | --permission-mode | --add-dir | --allowedTools | --allowed-tools | \
+      --disallowedTools | --disallowed-tools | --mcp-config | --settings | \
+      --append-system-prompt | --system-prompt | --max-turns | --output-format | \
+      --input-format | --fallback-model | --agent | --plugin-dir | --effort | --betas)
+      _expect=value
+      ;;
+    -*) : ;;
+    *)
+      # The first word of a Claude subcommand (mcp, doctor, update ...) starts
+      # no session at all.
+      if [ -z "$task_text" ]; then
+        case "$_arg" in
+          mcp | config | doctor | update | install | auth | plugin | setup-token | agents | migrate-installer) no_session=1 ;;
+        esac
+      fi
+      task_carried=1
+      [ -n "$task_text" ] || task_text=$_arg
+      ;;
   esac
 done
+# A trailing --name with no value is still a name given.
+[ "$_expect" = name ] && name_carried=1
+
+# CCSESSION_NAME names the session. An invalid name is dropped with a warning,
+# never an error: Claude starts either way.
+name_from_env=0
+env_name="${CCSESSION_NAME:-}"
+if [ -n "$env_name" ]; then
+  if "$CCSESSION" --check-name "$env_name" 2>/dev/null; then
+    name_from_env=1
+    name_carried=1
+  else
+    echo "[ccsession] CCSESSION_NAME is not a valid session name; ignoring it" >&2
+    env_name=""
+  fi
+fi
+
+# Someone can answer the question: stdin and stdout are terminals, autostart is
+# not off, and Orca is not resuming a session (a resume names its own session;
+# a label would start a different one).
+ask_ok=1
+[ -t 0 ] && [ -t 1 ] || ask_ok=0
+[ "${CCSESSION_AUTOSTART:-1}" = 0 ] && ask_ok=0
+[ "$resume_like" = 1 ] && ask_ok=0
+# --version, --help and the subcommands start no session: nothing to ask or reopen.
+[ "$no_session" = 1 ] && ask_ok=0
+# The one rule: ask only when there is no task, no name and no resume.
+ask=$ask_ok
+[ "$name_carried" = 1 ] && ask=0
+[ "$task_carried" = 1 ] && ask=0
 
 # After a workspace restart Orca relaunches each Claude tab with this command
 # again and nothing that says which session the tab ran (Coder #433). The
 # ccsession hooks remember it per tab; reopen it instead of asking, but only
-# where the question would be asked and only for a plain relaunch: Orca's own
-# options and nothing else (no prompt, name, prefill or session choice). A new
-# tab has no session yet, and anything else behaves as before.
-if [ "$ask" = 1 ] && [ -n "${ORCA_PANE_KEY:-}" ]; then
+# where the question could be asked and only for a plain relaunch: Orca's own
+# options and nothing else (no prompt, name, prefill or session choice, and no
+# CCSESSION_NAME). A new tab has no session yet, and anything else behaves as
+# before.
+if [ "$ask_ok" = 1 ] && [ -n "${ORCA_PANE_KEY:-}" ] && [ "$name_from_env" = 0 ]; then
   plain=1
   for _arg in "$@"; do
     case "$_arg" in
@@ -95,20 +181,19 @@ if [ "$ask" = 1 ] && [ -n "${ORCA_PANE_KEY:-}" ]; then
 fi
 
 name=""
-if [ "$ask" = 1 ]; then
-  ask_timeout="${CCSESSION_ASK_TIMEOUT:-30}"
-  hint="Enter or Ctrl+C = untagged"
-  case "$ask_timeout" in
-    '' | *[!0-9]* | 0) : ;;
-    *) hint="$hint; untagged after ${ask_timeout}s" ;;
-  esac
-  # Ctrl+C reaches this script too; a trap (not an ignore, which ccsession
-  # would inherit) keeps it running so it can start the untagged session.
-  trap ':' INT
-  name=$(CCSESSION_ASK_TIMEOUT="$ask_timeout" "$CCSESSION" --ask "$hint") || name=""
-  trap - INT
+if [ "$name_from_env" = 1 ]; then
+  name=$env_name
+elif [ "$ask" = 1 ]; then
+  # The time limit is ccsession's (CCSESSION_ASK_TIMEOUT, default 30); @LIMIT@
+  # in the hint becomes that number.
+  hint="Enter or Ctrl+C = untagged; untagged after @LIMIT@s"
+  name=$("$CCSESSION" --ask "$hint") || name=""
 fi
 
+# Neither of these belongs in Claude's environment, or a Claude started from
+# inside this one would inherit the name and the limit.
+unset CCSESSION_NAME CCSESSION_ASK_TIMEOUT
+
 # In tier mode the shim is always on; --shim asks for it everywhere else.
 if [ -n "$name" ]; then
   # --name: a name that starts with "-" is still a name, never an option.
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
