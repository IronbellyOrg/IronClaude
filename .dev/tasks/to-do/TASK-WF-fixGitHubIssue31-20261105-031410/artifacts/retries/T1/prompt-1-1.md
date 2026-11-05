b88e62c11f2f834dae2a38e92abf280042551738
Review one task for spec compliance.

Task brief: ## Task 1: Add the ccsession --auto-name helper

Add a `--auto-name [<task text>]` option to src/superclaude/skills/ccsession-tag/ccsession, next to `--ask` in the pre-launch option dispatch (around the `--ask` case). It prints one label on stdout and exits 0. The label is the worktree folder name, then up to four words of the task text (lowercase a-z0-9 only, control characters and punctuation dropped, nothing from the text when none is given), then a short local month-day-hour-minute stamp, joined with hyphens and cut to at most 80 characters. It must pass `validate_label`, and it must not equal any saved name in this folder's topics directory (`$PROJECTS_DIR/$(name_key)/topics/<name_to_file>.txt`): on a collision it appends -2, -3 and so on until the file does not exist. Task text with newlines, tabs, quotes, shell metacharacters or non-ASCII text must never break the label or the shell.

Acceptance criteria:
- T1.AC1: `ccsession --auto-name` and `ccsession --auto-name "Fix the login bug; rm -rf /"` each print a single line that `ccsession --name <label>` accepts, in a throwaway HOME.
- T1.AC2: With a saved topic file already holding the label that would be generated, a second call prints the same label with -2 appended; a third prints -3.
- T1.AC3: A 5000-character multi-line task text with control characters yields a label of at most 80 characters with no control characters.
- T1.AC4: `ccsession --help` text lists `--auto-name`.
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
Start sha: b88e62c11f2f834dae2a38e92abf280042551738
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/ccsession b/src/superclaude/skills/ccsession-tag/ccsession
index 8b8218b0..4473c512 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession
+++ b/src/superclaude/skills/ccsession-tag/ccsession
@@ -59,6 +59,10 @@
 #                             terminal, or keys already waiting), no answer within
 #                             CCSESSION_ASK_TIMEOUT seconds (unset or 0: no
 #                             limit), or end of input; exit 130: Ctrl+C
+#   ccsession --auto-name [<task text>]
+#                             Print a unique session label for a launch with no
+#                             name: folder name, up to four words of the task
+#                             text, and a stamp (never a saved name; always valid)
 #   ccsession-orca [<claude args>]
 #                             Orca's Claude command: asks for a name, then starts
 #                             Claude through ccsession (see ccsession-orca)
@@ -592,6 +596,46 @@ orca_tab_reopen() {
   printf '%s\t%s\n' "$session" "$name"
 }
 
+auto_name() {
+  # ccsession --auto-name [<task text>]: print one session label for a launch
+  # that carries no name. The label is the folder name (letters, digits and
+  # hyphens), up to four words of the task text (a-z and 0-9 only), and a stamp
+  # of month, day, time with seconds and a random part. Folder name and words
+  # are cut first, so the stamp always stays. The result passes validate_label
+  # and is not a name already saved for this repo (a saved name resumes that
+  # session, so an auto-name must never equal one). Never fails: whatever the
+  # input, a label is printed and the status is 0.
+  local text="${1:-}" folder words stamp prefix label key dir n=1 cand
+  folder=$(basename "$(pwd -P 2>/dev/null || echo session)" 2>/dev/null) || folder=""
+  folder=$(printf '%s' "$folder" | LC_ALL=C tr -c 'A-Za-z0-9' '-' | LC_ALL=C tr -s '-' | sed 's/^-//; s/-$//') || folder=""
+  [ -n "$folder" ] || folder="session"
+  folder=${folder:0:20}
+  words=$(printf '%s' "$text" | head -c 400 | LC_ALL=C tr -c 'A-Za-z0-9' ' ' | LC_ALL=C tr 'A-Z' 'a-z' |
+    awk '{ out = ""; for (i = 1; i <= NF && i <= 4; i++) out = out (i > 1 ? "-" : "") substr($i, 1, 12); printf "%s", out }') || words=""
+  # CCSESSION_AUTO_NAME_STAMP replaces the stamp (tests use it to make a label
+  # predictable); it is read as text and cut to the same safe characters.
+  if [ -n "${CCSESSION_AUTO_NAME_STAMP:-}" ]; then
+    stamp=$(printf '%s' "$CCSESSION_AUTO_NAME_STAMP" | head -c 24 | LC_ALL=C tr -c 'A-Za-z0-9-' '-')
+  else
+    stamp="$(date +%m%d-%H%M%S 2>/dev/null || echo 0000-000000)-$(printf '%04x' $((RANDOM % 65536)))"
+  fi
+  prefix="$folder${words:+-$words}"
+  prefix=${prefix:0:59}
+  prefix=${prefix%-}
+  label="$prefix-$stamp"
+  if key=$(name_key 2>/dev/null) && [ -n "$key" ]; then
+    dir="$PROJECTS_DIR/$key/topics"
+    cand="$label"
+    while [ -e "$dir/$(name_to_file "$cand").txt" ] && [ "$n" -lt 99 ]; do
+      n=$((n + 1))
+      cand="$label-$n"
+    done
+    label="$cand"
+  fi
+  validate_label "$label" >/dev/null 2>&1 || label="session-$stamp"
+  printf '%s\n' "$label"
+}
+
 # Fast paths that need no settings, env file or model data. The hooks use
 # --key and --sync-name so all of them agree on the name list.
 case "${1:-}" in
@@ -599,6 +643,13 @@ case "${1:-}" in
     name_key
     exit 0
     ;;
+  --auto-name)
+    # Before the argument loop below: task text such as --model or --tier=x is
+    # text here, never an option of ccsession.
+    ensure_names_migrated >/dev/null 2>&1 || true
+    auto_name "${2:-}"
+    exit 0
+    ;;
   --migrate-names)
     rename_dot_labels
     migrate_names
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
