449269c7758608167072ce32eecd3db31e498092
Review one task for spec compliance.

Task brief: ## Task 4: Map every question outcome in ccsession-orca to an auto-name, a message or a cancel

Depends on: Task 3

Edit the exec section of src/superclaude/skills/ccsession-tag/ccsession-orca. After the question (or without one), start `ccsession --name <label> --shim --claude-args <arguments>` with these labels: a name typed at the question is the label; exit 1 from `--ask` (timeout, end of input, keys already waiting) and an empty answer (Enter) take `ccsession --auto-name`; a launch that was not asked because it carries a task, has no terminal, or is not resume-like, name-less and not CCSESSION_AUTOSTART=0 and not print mode takes `ccsession --auto-name "<first positional prompt or prefill text, if any>"`. Exit 3 from `--ask` starts Claude with the returned text appended as the last positional argument (the first message), plus an auto-name built from that text. Exit 130 from `--ask` makes ccsession-orca exit 130 without starting Claude and without writing any session record. CCSESSION_AUTOSTART=0, print mode and resume-like launches start exactly as today (untagged, arguments unchanged).

Acceptance criteria:
- T4.AC1: On a pseudo-terminal, Enter at the question and a one-second timeout both start Claude with `--name <auto label>`, the topic recorded in the fake Claude record equals that label, and no `CCSESSION_ASK_TIMEOUT` is left in Claude's environment.
- T4.AC2: Ctrl+C at the question makes `ccsession-orca` exit with status 130, the fake Claude record file is not created, and the terminal is back in line mode.
- T4.AC3: A launch without a terminal and with a prompt starts Claude with the prompt unchanged as the last argument, plus `--name <auto label>` built from the prompt words.
- T4.AC4: A tab line of 300 characters typed at the question reaches Claude as the last positional argument and is not a label.
- T4.AC5: CCSESSION_AUTOSTART=0, `-p x`, and `--resume <id>` launches produce no `--name` and unchanged arguments.
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
Start sha: 449269c7758608167072ce32eecd3db31e498092
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/ccsession b/src/superclaude/skills/ccsession-tag/ccsession
index 4aed0a91..6d696738 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession
+++ b/src/superclaude/skills/ccsession-tag/ccsession
@@ -69,7 +69,9 @@
 #   ccsession --auto-name [<task text>]
 #                             Print a unique session label for a launch with no
 #                             name: folder name, up to four words of the task
-#                             text, and a stamp (never a saved name; always valid)
+#                             text, and a stamp (never a saved name; always valid).
+#                             Exit 1 and no output when the name list cannot be
+#                             written
 #   ccsession --check-name <name>
 #                             Exit 0 when <name> is a valid session name, else 1
 #   ccsession-orca [<claude args>]
@@ -612,8 +614,9 @@ auto_name() {
   # of month, day, time with seconds and a random part. Folder name and words
   # are cut first, so the stamp always stays. The result passes validate_label
   # and is not a name already saved for this repo (a saved name resumes that
-  # session, so an auto-name must never equal one). Never fails: whatever the
-  # input, a label is printed and the status is 0.
+  # session, so an auto-name must never equal one). Whatever the text, a valid
+  # label is printed; the one exception is a name list that cannot be written
+  # (no label, status 1), because a launch under a label could not save it.
   local text="${1:-}" folder words stamp prefix label key dir n=1 cand
   folder=$(basename "$(pwd -P 2>/dev/null || echo session)" 2>/dev/null) || folder=""
   folder=$(printf '%s' "$folder" | LC_ALL=C tr -c 'A-Za-z0-9' '-' | LC_ALL=C tr -s '-' | sed 's/^-//; s/-$//') || folder=""
@@ -634,6 +637,12 @@ auto_name() {
   label="$prefix-$stamp"
   if key=$(name_key 2>/dev/null) && [ -n "$key" ]; then
     dir="$PROJECTS_DIR/$key/topics"
+    # A launch under this label saves it in the name list; when that list cannot
+    # be written the launch would stop, so print nothing and let the caller start
+    # untagged instead.
+    if ! { mkdir -p "$dir" 2>/dev/null && [ -w "$dir" ]; }; then
+      return 1
+    fi
     cand="$label"
     while [ -e "$dir/$(name_to_file "$cand").txt" ] && [ "$n" -lt 99 ]; do
       n=$((n + 1))
diff --git a/src/superclaude/skills/ccsession-tag/ccsession-orca b/src/superclaude/skills/ccsession-tag/ccsession-orca
index 0ec9dbdb..ccfb42dd 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession-orca
+++ b/src/superclaude/skills/ccsession-tag/ccsession-orca
@@ -58,6 +58,7 @@ resume_like=0
 name_carried=0
 task_carried=0
 no_session=0
+print_mode=0
 task_text=""
 _expect=""
 _dd=0
@@ -94,7 +95,10 @@ for _arg in "$@"; do
       _expect=value
       ;;
     --session-id=*) task_carried=1 ;;
-    -p | --print) task_carried=1 ;;
+    -p | --print)
+      task_carried=1
+      print_mode=1
+      ;;
     -v | --version | -h | --help) no_session=1 ;;
     --model | --permission-mode | --add-dir | --allowedTools | --allowed-tools | \
       --disallowedTools | --disallowed-tools | --mcp-config | --settings | \
@@ -138,7 +142,9 @@ fi
 # a label would start a different one).
 ask_ok=1
 [ -t 0 ] && [ -t 1 ] || ask_ok=0
-[ "${CCSESSION_AUTOSTART:-1}" = 0 ] && ask_ok=0
+autostart=1
+[ "${CCSESSION_AUTOSTART:-1}" = 0 ] && autostart=0
+[ "$autostart" = 0 ] && ask_ok=0
 [ "$resume_like" = 1 ] && ask_ok=0
 # --version, --help and the subcommands start no session: nothing to ask or reopen.
 [ "$no_session" = 1 ] && ask_ok=0
@@ -181,13 +187,50 @@ if [ "$ask_ok" = 1 ] && [ -n "${ORCA_PANE_KEY:-}" ] && [ "$name_from_env" = 0 ];
 fi
 
 name=""
+message=""
 if [ "$name_from_env" = 1 ]; then
   name=$env_name
 elif [ "$ask" = 1 ]; then
   # The time limit is ccsession's (CCSESSION_ASK_TIMEOUT, default 30); @LIMIT@
   # in the hint becomes that number.
-  hint="Enter or Ctrl+C = untagged; untagged after @LIMIT@s"
-  name=$("$CCSESSION" --ask "$hint") || name=""
+  hint="Enter = auto-named, Ctrl+C = cancel; auto-named after @LIMIT@s"
+  rc=0
+  # Ctrl+C reaches this script too: end it with the same status, never go on.
+  trap 'exit 130' INT
+  answer=$("$CCSESSION" --ask "$hint") || rc=$?
+  trap - INT
+  case "$rc" in
+    0) name=$answer ;; # a name; an empty answer (Enter) is auto-named below
+    1) : ;;            # not asked (keys already waiting), timed out, or end of input: auto-named below
+    3) message=$answer ;; # not a name (paste, control character, too long): Claude's first message
+    130) exit 130 ;;   # Ctrl+C cancels: no Claude, no session record
+    *) echo "[ccsession] the session-name question failed (status $rc); starting without it" >&2 ;;
+  esac
+fi
+
+# A launch without a name gets an automatic one, unless it is a resume (it names
+# itself), a plain start (CCSESSION_AUTOSTART=0), print mode, or no session at
+# all (--version, a subcommand). The label comes from the task: the prompt, the
+# prefill text, or the message typed at the question. If no label can be made,
+# Claude starts untagged: a launch never stops here.
+auto=1
+if [ "$resume_like" = 1 ] || [ "$autostart" = 0 ] || [ "$print_mode" = 1 ] ||
+  [ "$no_session" = 1 ] || [ "$name_carried" = 1 ]; then
+  auto=0
+fi
+if [ -z "$name" ] && [ "$auto" = 1 ]; then
+  _text=$task_text
+  [ -n "$message" ] && _text=$message
+  name=$("$CCSESSION" --auto-name "$_text" 2>/dev/null) || name=""
+fi
+
+# The typed text that cannot be a name goes to Claude as its first message, after
+# "--" when it starts with "-" so it is never read as an option.
+if [ -n "$message" ]; then
+  case "$message" in
+    -*) set -- "$@" -- "$message" ;;
+    *) set -- "$@" "$message" ;;
+  esac
 fi
 
 # Neither of these belongs in Claude's environment, or a Claude started from
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
