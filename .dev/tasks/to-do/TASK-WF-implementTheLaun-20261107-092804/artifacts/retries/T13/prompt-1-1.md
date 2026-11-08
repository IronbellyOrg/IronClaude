6a1a543e6fd5430eec3e045df561ae73176fb69d
Review one task for spec compliance.

Task brief: ## Task 13: Ship the guard through the installer and the plugin mirror

Depends on: Task 12

Add "launch-level-guard.sh" to _FRESHNESS_SCRIPTS in src/superclaude/cli/install_hooks.py (the Makefile needs no change because make verify-sync imports that list). Copy src/superclaude/hooks/scripts/launch-level-guard.sh to plugins/superclaude/hooks/scripts/launch-level-guard.sh byte for byte with the executable bit. Add the name to the fake-script list at the top of the fixture in tests/cli/test_install_hooks.py (the list that already holds launch-job-identity.sh). Add tests in tests/cli/test_install_hooks.py modelled on test_launch_identity_script_is_packaged_listed_executable_and_mirrored and test_launch_identity_real_install_preserves_policies_and_is_idempotent: the script is listed, executable, byte-identical to its plugin mirror and starts with #!/bin/bash; a real install into an isolated HOME registers the guard under both UserPromptSubmit and PreToolUse exactly once, preserves permissions, user hooks and the other managed registrations, is idempotent on a second install with and without force, and copies a byte-identical executable script to ~/.claude/hooks/. If the merge logic in _merge_settings cannot register one command under two events or refreshes it by matcher alone, make the smallest change in install_hooks.py that registers and refreshes by exact command identity per event, and add a test for that case.

Run make sync-dev and then make verify-sync.

Acceptance criteria:
- uv run pytest tests/cli/test_install_hooks.py -v passes, including the new guard tests.
- make verify-sync exits 0 and its Installer Registration section reports no script missing from _FRESHNESS_SCRIPTS.
- diff of src/superclaude/hooks/scripts/launch-level-guard.sh and plugins/superclaude/hooks/scripts/launch-level-guard.sh prints nothing.
- A second install into the same isolated HOME leaves settings.json byte-identical to the first install result.

AC ids (source order):
T13.AC1: uv run pytest tests/cli/test_install_hooks.py -v passes, including the new guard tests.
T13.AC2: make verify-sync exits 0 and its Installer Registration section reports no script missing from _FRESHNESS_SCRIPTS.
T13.AC3: diff of src/superclaude/hooks/scripts/launch-level-guard.sh and plugins/superclaude/hooks/scripts/launch-level-guard.sh prints nothing.
T13.AC4: A second install into the same isolated HOME leaves settings.json byte-identical to the first install result.
Global constraints: - docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.
Start sha: 6a1a543e6fd5430eec3e045df561ae73176fb69d
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t13-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t13-test.log
new file mode 100644
index 00000000..fb28bb0c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t13-test.log
@@ -0,0 +1,22 @@
+## uv run pytest tests/cli/test_install_hooks.py tests/hooks/test_launch_level_guard_registration.py tests/hooks/test_freshness_subagent_start_policy.py -q
+tests/hooks/test_launch_level_guard_registration.py ............         [ 91%]
+tests/hooks/test_freshness_subagent_start_policy.py .....                [100%]
+
+============================== 60 passed in 1.27s ==============================
+
+## cmp src vs plugins launch-level-guard.sh
+identical
+
+## make verify-sync (last 12 lines)
+  ✅ modularization-template-review/qa-source-fidelity_template.md
+  ✅ modularization-template-review/qa-research-depth_report_template.md
+  ✅ modularization-template-review/web-research_template.md
+
+=== Installer Registration ===
+  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
+
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+✅ All components in sync.
+exit=0
diff --git a/plugins/superclaude/hooks/scripts/launch-level-guard.sh b/plugins/superclaude/hooks/scripts/launch-level-guard.sh
new file mode 100755
index 00000000..8c56ddae
--- /dev/null
+++ b/plugins/superclaude/hooks/scripts/launch-level-guard.sh
@@ -0,0 +1,740 @@
+#!/bin/bash
+# Launch-level guard (L1), IronbellyOrg/IronClaude issue #394.
+# Design: docs/designs/sc-issue-launch-level-hook.md (sections 2, 3, 8, 9).
+# Registered on UserPromptSubmit and PreToolUse. Exit 0 allows; exit 2 blocks
+# with a message on stderr; never exit 1, no onFailure. Only a session that the
+# claim script launched (a valid top-level session_id bound in the store) is
+# governed; every other session is ordinary and never blocked (FR-L-53).
+# Ten-part layout (DD-1); part 8 holds the section 5.2 classifiers (Skill, Bash,
+# Monitor, edits, Agent/Task, Cron/Schedule, escape and MCP tools); others NONE.
+# launch-level-guard-version: 1
+
+# 1. Settings
+export LC_ALL=C
+set -u -o pipefail
+set -f
+umask 077
+
+# >>> printer (parts 2 and 3; the tests run this block on its own)
+# 2. Store path: three literal parts, so this text never names the joined path.
+LL_S1=.claude
+LL_S2=state
+LL_S3=launch-level
+LL_STORE="${HOME:-}/$LL_S1/$LL_S2/$LL_S3"
+
+# 3. Messages (section 9). LL_LEVEL is W, WA, F, FS or empty (unknown).
+LL_LEVEL=
+LL_SID=
+LL_NOTE_STATE=0
+LL_NOTE_TEXT=0
+LL_DENIED=0
+
+ll_valid_sid() {
+    [[ $1 =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]]
+}
+
+ll_say() {
+    local id=$1 lvl= b w y
+    if [ "$id" = LL-TAMPER ] && ! ll_valid_sid "$LL_SID"; then
+        id=LL-BROKEN
+    fi
+    case $id in
+    LL-IMPL)
+        b='starting /sc:implement, /task, /sc:improve, /sc:cleanup, /sc:spawn or /sc:build (or their skills).'
+        w='At the worktree level the agent stops at a plan until a person approves it.'
+        y='Read the plan, then type /sc:implement or /task, or reply approved, in this session.' ;;
+    LL-COMMIT)
+        b='creating a commit (git commit, cherry-pick, revert, am, or moving a branch with update-ref).'
+        w='Only a launch with --pipeline full --submit lets the agent commit.'
+        y='Review the changes and commit them yourself, or claim the issue again with --pipeline full --submit.' ;;
+    LL-PUSH)
+        b='a git push.'
+        w='Only a launch with --pipeline full --submit lets the agent push.'
+        y='Push the branch yourself after review, or claim the issue again with --pipeline full --submit.' ;;
+    LL-PUSH-FORM)
+        b='a push that is not one plain git push command, or a command that names git and push together.'
+        w='The guard can check a push only when the whole command is git push [-u] origin <branch> (or <source>:<branch>), with nothing before or after it; other forms (force, --all, another remote, variables, backticks, line continuations, chained or piped commands) can reach another remote or the main branch.'
+        y='Run the push as its own command, exactly: git push origin <branch> or git push -u origin <branch>, with the branch name written out.' ;;
+    LL-PROTECTED)
+        b='a push to master or main.'
+        w='No launch level may change the main branch.'
+        y='Push the feature branch by name, then merge it through a reviewed pull request.' ;;
+    LL-MERGE)
+        b='a merge (git merge, git pull, gh pr merge, a call to a GitHub merge URL, or an MCP merge tool).'
+        w='No launch level may merge; only a person reviews and merges.'
+        y='Leave the merge to a person. To update the branch, run git fetch, then git rebase.' ;;
+    LL-GH-WRITE)
+        b='a gh api call that is not one plain read command (it sets a method, a field or an input, calls graphql or a merge endpoint, or uses variables, quotes, pipes or other commands around it), or a gh command whose text mentions api, or a direct call to the GitHub API.'
+        w='In a launched session gh api may only read, and only in a form the guard can check: a gh api write can merge, comment or change the main branch.'
+        y='Run the read as one plain command with every value written out, for example gh api repos/o/r/pulls/5 --jq .state, or use a gh command for the step (gh pr view --json, gh pr comment, gh pr create --repo ...) at a level that allows it, or ask the person.' ;;
+    LL-SUBMIT)
+        b='/sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request or issue).'
+        w='Publishing work needs a launch with --pipeline full --submit.'
+        y='Run it yourself in your own session, or claim the issue again with --pipeline full --submit.' ;;
+    LL-REPO)
+        b='gh pr create without --repo.'
+        w='Without --repo, gh can open the pull request on the parent repository of a fork.'
+        y='Retry with --repo <owner>/<name> (or -R).' ;;
+    LL-UNKNOWN)
+        b='a git or gh command the guard does not recognise (an unknown subcommand, a git alias definition, or a subcommand built from a variable or a substitution), or a line continuation inside a word.'
+        w='In a launched session only known git and gh commands may run, so a renamed command or an alias cannot commit, push or merge.'
+        y='Use the standard command written out (for example git status, git diff, git add), or ask the person to run it. Write the command on one line.' ;;
+    LL-MCP)
+        b='a GitHub write through an MCP tool.'
+        w='The guard cannot check where an MCP write lands, so a launched session writes to GitHub only through git and gh.'
+        y='Use git or gh for this step.' ;;
+    LL-ESCAPE)
+        b='starting or messaging another agent or session (claude, ccsession, orca, SendMessage, /sc:issue, a remote subagent, a workflow, a remote trigger) or typing into a terminal (tmux, screen, xdotool).'
+        w="That work would run outside this session's launch level."
+        y='Do the work here (local subagents are allowed), or ask the person to start it.' ;;
+    LL-TURN)
+        b='scheduling a turn (a cron job or a wake-up) before the plan is approved.'
+        w='Its prompt text arrives later as a new turn and could look like a person replying approved.'
+        y='Wait until the person approves the plan, or use a background task or a monitor instead.' ;;
+    LL-TAMPER)
+        b='touching the launch-level state, the Claude Code settings or hooks, a git configuration file, or reinstalling the hooks.'
+        w='The session must not change its own limits.'
+        y="Ask the person. To release this session they run, in their own terminal: rm \"$LL_STORE/sessions/$LL_SID\" \"$LL_STORE/sessions/$LL_SID.ok\"" ;;
+    LL-SKILL)
+        b='a skill call whose name the guard cannot read.'
+        w='The guard cannot tell whether the skill is allowed at this level.'
+        y='Report it (the hook input format may have changed); the person can release the session.' ;;
+    LL-BIG)
+        b='a command longer than 64 KB.'
+        w='The guard cannot check a command that long in time.'
+        y='Write the content to a file with the Write tool, then run a short command.' ;;
+    LL-NOBIND)
+        b='this launch prompt.'
+        w='The session was started by /sc:issue --claim, but the guard could not register it, so its limits could not be enforced.'
+        y="Check that jq is installed and $LL_STORE is writable, then claim the issue again." ;;
+    *)
+        b='this action, because the launch-level guard could not run (jq missing, unreadable input or an internal error).'
+        w='In a launched session the guard fails closed.'
+        y="Install jq, or ask the person to release the session by deleting its files in $LL_STORE/sessions/." ;;
+    esac
+    case $LL_LEVEL in
+    W) lvl=worktree ;;
+    WA) lvl='worktree (approved)' ;;
+    F) lvl=full ;;
+    FS) lvl='full --submit' ;;
+    esac
+    if [ -n "$lvl" ]; then
+        printf '%s\n' "Launch-level guard: this session was started by /sc:issue --claim at level $lvl." >&2
+    else
+        printf '%s\n' 'Launch-level guard:' >&2
+    fi
+    printf '%s\n' "Blocked: $b" "Why: $w" "You can: $y" >&2
+    if [ "$LL_NOTE_STATE" = 1 ]; then
+        printf '%s\n' 'Note: the launch record was invalid or unreadable, so the strictest level (worktree) applies.' >&2
+    fi
+    if [ "$LL_NOTE_TEXT" = 1 ]; then
+        printf '%s\n' 'Note: the guard does not tell quoted text from commands. Any command that names git together with the word commit, push, merge or pull, or gh together with the word api, counts as that action, even if the words are only in a message, a title, a PR body or a search pattern. If that is the case here, write the text to a file with the Write tool and pass it with git commit -F <file> or gh ... --body-file <file>, or reword the search or title.' >&2
+    fi
+}
+
+ll_deny() {
+    LL_DENIED=1
+    ll_say "$1"
+    exit 2
+}
+# <<< printer
+
+# Any exit other than 0 or a deliberate deny is an internal failure. A governed
+# session fails closed (LL-BROKEN, LL-NOBIND in the prompt branch); an ordinary
+# session is never blocked by a failure.
+LL_GOVERNED=0
+LL_BRANCH=
+ll_on_exit() {
+    local rc=$?
+    trap - EXIT
+    if [ "$rc" = 0 ] || { [ "$rc" = 2 ] && [ "$LL_DENIED" = 1 ]; }; then
+        exit "$rc"
+    fi
+    if [ "$LL_GOVERNED" != 1 ]; then
+        exit 0
+    fi
+    if [ "$LL_BRANCH" = prompt ]; then
+        ll_say LL-NOBIND
+    else
+        ll_say LL-BROKEN
+    fi
+    exit 2
+}
+trap ll_on_exit EXIT
+
+# 4. Dispatch
+LL_INPUT=$(cat)
+# Empty-store fast exit: no session records and no launch marker.
+if [ ! -d "$LL_STORE/sessions" ]; then
+    case $LL_INPUT in
+    *'[sc-launch:'*) ;;
+    *) exit 0 ;;
+    esac
+fi
+# One parse of the top-level fields (FR-L-10; also part 7, the tool fields).
+# Line 1: event, agent_id flag (prompt only), input-error flag, session id.
+# Lines 2 to 5: tool name, skill name (skill unless missing or null, else
+# name), edit path (file_path unless missing or null, else notebook_path),
+# isolation, each with CR and LF made spaces. Then the prompt (NUL made a
+# space) or the command, kept whole, and a "." so no trailing newline is lost.
+# A nonstring tool field, a NUL in one or a nonobject tool_input is an input
+# error. Nested keys never count; agent_id is never read on PreToolUse.
+LL_PARSED=$(jq -r '
+    def str: if type == "string" then . else "" end;
+    def line: str | split("\u0000") | join(" ") | gsub("[\r\n]"; " ");
+    (.hook_event_name | if . == "UserPromptSubmit" or . == "PreToolUse" then . else "OTHER" end) as $e
+    | (if $e == "PreToolUse" then . else {} end) as $p
+    | ($p.tool_input) as $ti
+    | ($ti | if type == "object" then . else {} end) as $o
+    | ($p.tool_name) as $tn
+    | ($tn | str) as $t
+    | (if $t != "Skill" then null elif $o.skill != null then $o.skill else $o.name end) as $sk
+    | (if ($t == "Edit" or $t == "Write" or $t == "NotebookEdit") | not then null
+        elif $o.file_path != null then $o.file_path else $o.notebook_path end) as $fp
+    | (if $t == "Agent" or $t == "Task" then $o.isolation else null end) as $iso
+    | (if $t == "Bash" or $t == "Monitor" then $o.command else null end) as $cmd
+    | (any($tn, $sk, $fp, $iso, $cmd; . != null and (type != "string" or (explode | any(. == 0))))
+        or ($ti != null and ($ti | type) != "object")) as $bad
+    | $e + " "
+    + (if $e == "UserPromptSubmit" then (.agent_id | if type == "string" and length > 0 then "1" else "0" end) else "0" end)
+    + " " + (if $bad then "1" else "0" end) + " "
+    + (.session_id | if type == "string" and test("\\A[A-Za-z0-9][A-Za-z0-9_-]{0,127}\\z") then . else "" end)
+    + "\n" + ($t | line) + "\n" + ($sk | line) + "\n" + ($fp | line) + "\n" + ($iso | line) + "\n"
+    + (if $e == "UserPromptSubmit" then .prompt else $cmd end | str | split("\u0000") | join(" "))
+    + "."
+' <<<"$LL_INPUT" 2>/dev/null)
+LL_RC=$?
+LL_BAD=0 LL_TOOL= LL_SKILL= LL_PATH= LL_ISO= LL_TEXT= LL_PROMPT=
+if [ "$LL_RC" != 0 ]; then
+    # No jq or no parseable envelope: no level is inferred. A tool payload
+    # looks at every session_id value for one that has a record, only to find a
+    # positively bound session, which then falls through to the last line
+    # (LL-BROKEN); this can only block, never allow early. Declared limit: any
+    # bound id in the text counts, even a nested one, so an ordinary session
+    # sending broken JSON that contains a bound id is blocked. A recognizable launch-marker
+    # prompt (marker text, no tool_name key) blocks rather than starting
+    # ungoverned; anything else is identity loss (section 3): allow without
+    # claiming enforcement.
+    case $LL_INPUT in
+    *'"tool_name"'*)
+        LL_EVENT=FAILED
+        LL_RAWRE='"session_id"[[:space:]]*:[[:space:]]*"([A-Za-z0-9][A-Za-z0-9_-]{0,127})"(.*)'
+        LL_REST=$LL_INPUT
+        # No cap on the number of session_id values tried (a cap would let a payload with many forged ids hide the real bound one).
+        while :; do
+            [[ $LL_REST =~ $LL_RAWRE ]] || break
+            LL_REST=${BASH_REMATCH[2]}
+            if [ -e "$LL_STORE/sessions/${BASH_REMATCH[1]}" ] || [ -L "$LL_STORE/sessions/${BASH_REMATCH[1]}" ]; then
+                LL_SID=${BASH_REMATCH[1]}
+                break
+            fi
+        done
+        LL_REST= ;;
+    *'[sc-launch:'*)
+        LL_BRANCH=prompt
+        LL_GOVERNED=1
+        ll_deny LL-NOBIND ;;
+    *) exit 0 ;;
+    esac
+else
+    # read, not ${var#*$'\n'}: pattern removal is quadratic on a long line.
+    {
+        read -r LL_EVENT LL_AGENT LL_BAD LL_SID
+        IFS= read -r LL_TOOL
+        IFS= read -r LL_SKILL
+        IFS= read -r LL_PATH
+        IFS= read -r LL_ISO
+        IFS= read -r -d '' LL_TEXT
+    } <<<"$LL_PARSED"
+    LL_SID=${LL_SID:-}
+    LL_TEXT=${LL_TEXT%$'.\n'} # the here-string adds the newline after the "."
+    [ "$LL_EVENT" = UserPromptSubmit ] && LL_PROMPT=$LL_TEXT
+fi
+
+# A valid id with a record (of any file kind) is positively governed. Its level
+# is exactly one allowed word plus an optional newline; anything else is
+# worktree with the LL-STATE note; .ok at worktree gives worktree (approved).
+if [ -n "$LL_SID" ] && { [ -e "$LL_STORE/sessions/$LL_SID" ] || [ -L "$LL_STORE/sessions/$LL_SID" ]; }; then
+    LL_GOVERNED=1
+    LL_FILE="$LL_STORE/sessions/$LL_SID"
+    LL_REC=
+    if [ -f "$LL_FILE" ] && [ ! -L "$LL_FILE" ] && [ -r "$LL_FILE" ]; then
+        IFS= read -r -N 13 LL_REC <"$LL_FILE"
+    fi
+    case $LL_REC in
+    worktree | worktree$'\n') LL_LEVEL=W ;;
+    full | full$'\n') LL_LEVEL=F ;;
+    full-submit | full-submit$'\n') LL_LEVEL=FS ;;
+    *) LL_LEVEL=W LL_NOTE_STATE=1 ;;
+    esac
+    if [ "$LL_LEVEL" = W ] && [ -f "$LL_FILE.ok" ] && [ ! -L "$LL_FILE.ok" ]; then
+        LL_LEVEL=WA
+    fi
+fi
+
+case $LL_EVENT in
+UserPromptSubmit) LL_BRANCH=prompt ;;
+PreToolUse) LL_BRANCH=tool ;;
+*)
+    # Unknown event shape: identity-loss allow unless positively governed,
+    # which falls through to the last line (LL-BROKEN).
+    [ "$LL_GOVERNED" = 1 ] || exit 0 ;;
+esac
+
+# 5. Prompt branch: binding (FR-L-09, B1 to B13), then approval (FR-L-15 to FR-L-19).
+# Writes: mkdir -p sessions; take pending/<nonce> with one rename (mv) to
+# sessions/.take-<sid>, so a nonce is consumed once; publish sessions/<sid> with
+# a hard link (ln), which fails when the target exists, so the first binding is
+# never replaced. Temporary names start with a dot and are never a valid id.
+ll_publish() {
+    local tmp="$LL_SESS/.tmp-$LL_SID-$$"
+    rm -f -- "$tmp" 2>/dev/null
+    if (set -C; printf '%s' "$1" >"$tmp") 2>/dev/null; then
+        ln -- "$tmp" "$LL_SESS/$LL_SID" 2>/dev/null
+    fi
+    rm -f -- "$tmp" 2>/dev/null
+    return 0
+}
+# Publish from a taken record, ours or a racing prompt's for the same id.
+ll_link_take() {
+    local w=
+    { [ -f "$LL_TAKE" ] && [ ! -L "$LL_TAKE" ]; } || return 0
+    { IFS= read -r -N 13 w <"$LL_TAKE"; } 2>/dev/null
+    case $w in
+    worktree | full | full-submit | worktree$'\n' | full$'\n' | full-submit$'\n')
+        ln -- "$LL_TAKE" "$LL_SESS/$LL_SID" 2>/dev/null ;;
+    *) ll_publish degraded ;;
+    esac
+    # Drop the taken record only once a binding exists, so a failed link never loses it.
+    if [ -e "$LL_SESS/$LL_SID" ] || [ -L "$LL_SESS/$LL_SID" ]; then
+        rm -f -- "$LL_TAKE" 2>/dev/null
+    fi
+    return 0
+}
+if [ "$LL_BRANCH" = prompt ]; then
+    [ "$LL_AGENT" = 1 ] && exit 0 # B5: a subagent prompt never binds or approves
+    # B6: strict marker anywhere; loose marker at the start after whitespace or a BOM.
+    LL_NONCE=
+    LL_RE='\[sc-launch:v1:([0-9a-f]{32})\]'
+    [[ $LL_PROMPT =~ $LL_RE ]] && LL_NONCE=${BASH_REMATCH[1]}
+    LL_WS=$' \t\r\n'
+    LL_P=$LL_PROMPT
+    while :; do
+        LL_P=${LL_P#"${LL_P%%[!$LL_WS]*}"}
+        case $LL_P in
+        $'\xef\xbb\xbf'*) LL_P=${LL_P:3} ;;
+        *) break ;;
+        esac
+    done
+    LL_LOOSE=0
+    case $LL_P in '[sc-launch:'*) LL_LOOSE=1 ;; esac
+    LL_SESS=$LL_STORE/sessions
+    LL_PEND=$LL_STORE/pending
+    LL_USABLE=0
+    if [ -n "$LL_NONCE" ] && [ -d "$LL_PEND" ] && [ ! -L "$LL_PEND" ] && [ -O "$LL_PEND" ] &&
+        [ -f "$LL_PEND/$LL_NONCE" ] && [ ! -L "$LL_PEND/$LL_NONCE" ]; then
+        LL_USABLE=1
+    fi
+    if [ "$LL_GOVERNED" = 1 ]; then
+        # B8: already bound; the level never changes, a supplied record is consumed.
+        [ "$LL_USABLE" = 1 ] && rm -f -- "$LL_PEND/$LL_NONCE" 2>/dev/null
+        # Approval (FR-L-15 to FR-L-17): only at worktree (an invalid word
+        # included), never at full or full-submit. The whole prompt trimmed and
+        # lower-cased is approved, approved. or approved!; or the first line,
+        # leading whitespace removed, starts /sc:implement, /sc:task or /task
+        # as a whole word. The [[:space:]] after the command name also matches
+        # the newline that ends the first line.
+        LL_RE_APR='^[[:space:]]*/(sc:implement|sc:task|task)([[:space:]]|$)'
+        LL_APR=0
+        if [ "$LL_LEVEL" = W ]; then
+            [[ $LL_PROMPT =~ $LL_RE_APR ]] && LL_APR=1
+            LL_P=${LL_PROMPT#"${LL_PROMPT%%[![:space:]]*}"}
+            LL_P=${LL_P%"${LL_P##*[![:space:]]}"}
+            [[ ${LL_P,,} =~ ^approved[.!]?$ ]] && LL_APR=1
+        fi
+        if [ "$LL_APR" = 1 ]; then
+            # No-replace create of a regular file in the owned sessions
+            # directory; an existing .ok of any kind is left alone. A failed
+            # write still allows the prompt and shows later as LL-IMPL.
+            if [ -d "$LL_STORE/sessions" ] && [ ! -L "$LL_STORE/sessions" ] && [ -O "$LL_STORE/sessions" ] &&
+                [ ! -e "$LL_FILE.ok" ] && [ ! -L "$LL_FILE.ok" ]; then
+                (set -C; : >"$LL_FILE.ok") 2>/dev/null
+            fi
+        fi
+        exit 0 # approval lasts until a person deletes the session's files (O-6)
+    fi
+    if [ -z "$LL_NONCE" ] && [ "$LL_LOOSE" = 0 ]; then
+        exit 0 # B9: unbound, no marker
+    fi
+    LL_GOVERNED=1 # a launch marker: any failure from here is LL-NOBIND
+    [ -n "$LL_SID" ] || ll_deny LL-NOBIND # B7
+    mkdir -p -- "$LL_SESS" 2>/dev/null
+    if ! { [ -d "$LL_SESS" ] && [ ! -L "$LL_SESS" ] && [ -O "$LL_SESS" ]; }; then
+        ll_deny LL-NOBIND
+    fi
+    LL_TAKE=$LL_SESS/.take-$LL_SID
+    if [ "$LL_USABLE" = 1 ] && [ ! -d "$LL_TAKE" ]; then
+        mv -- "$LL_PEND/$LL_NONCE" "$LL_TAKE" 2>/dev/null # B11: one rename wins the nonce
+    fi
+    ll_link_take
+    if [ "$LL_LOOSE" = 1 ] && [ ! -e "$LL_SESS/$LL_SID" ] && [ ! -L "$LL_SESS/$LL_SID" ]; then
+        ll_publish degraded # B12: missing or used nonce, leading marker
+    fi
+    # B13: whoever won, a regular binding file now exists or the prompt is blocked.
+    if [ -f "$LL_SESS/$LL_SID" ] && [ ! -L "$LL_SESS/$LL_SID" ]; then
+        exit 0
+    fi
+    ll_deny LL-NOBIND
+fi
+
+# 6. Fast paths. An unbound valid id allows silently; a missing or invalid id is
+# identity loss, a declared fail-open limit (section 3). agent_id is never read
+# here and there is no cwd fallback.
+if [ "$LL_BRANCH" = tool ]; then
+    [ "$LL_GOVERNED" = 1 ] || exit 0 # unbound or identity loss
+    [ "$LL_BAD" = 1 ] && ll_deny LL-BROKEN # a nonstring tool field or an embedded NUL
+
+    # 7. The tool fields come from the one jq parse in part 4.
+    # 8. Classifiers add classes to LL_CLASSES (section 5.2); none gives NONE.
+    LL_CLASSES=' '
+    LL_TT= # the text the tamper tokens are looked for in (T or the edit path)
+    if [ "$LL_TOOL" = Skill ]; then
+        # FR-L-40: first word, lower case, one leading "/", text after the last
+        # ":", one leading "sc-", one trailing "-protocol".
+        LL_N=
+        [[ $LL_SKILL =~ ^[[:space:]]*([^[:space:]]*) ]] && LL_N=${BASH_REMATCH[1]}
+        LL_N=${LL_N,,}
+        LL_N=${LL_N#/}
+        LL_N=${LL_N##*:}
+        LL_N=${LL_N#sc-}
+        LL_N=${LL_N%-protocol}
+        case $LL_N in
+        implement | task | improve | cleanup | spawn | build) LL_CLASSES+='IMPL ' ;;
+        pr-submit) LL_CLASSES+='SUBMIT ' ;;
+        issue) LL_CLASSES+='ESCAPE ' ;;
+        '') LL_CLASSES+='SKILL ' ;;
+        esac
+    elif [ "$LL_TOOL" = Bash ] || [ "$LL_TOOL" = Monitor ]; then
+        # FR-L-22 to FR-L-27: cmd is the decoded tool_input.command, kept raw; a
+        # Monitor call with only ws has no text and stays NONE. No ${s//...}
+        # substitution runs over the text (fact T5); one sed and four tr.
+        cmd=$LL_TEXT
+        if [ "${#cmd}" -gt 65536 ]; then
+            LL_CLASSES+='BIG ' # NM1: bytes under LC_ALL=C; nothing else is checked
+        elif [ -n "$cmd" ]; then
+            # >>> normalise (NM1a to NM7; the tests run this block on its own)
+            # NM1a: a backslash-newline continuation inside a word. The
+            # regex sits in a variable: a quoted $'...' after =~ matches literally.
+            LL_RE_NM1A=$'[^[:space:]\\\\]\\\\\n'
+            [[ $cmd =~ $LL_RE_NM1A ]] && LL_CLASSES+='UNKNOWN '
+            # T (NM2, NM3): $ before a quote, quotes and backslashes deleted, "/" runs squeezed; the tamper text.
+            T=$(printf '%s\n' "$cmd" | sed -E -e "s/\\\$(['\"])/\\1/g" -e "s/['\"\\\\]//g" -e 's#/+#/#g' -e 's#/(\./)+#/#g' -e 's/`/ $;/g') || ll_deny LL-BROKEN
+            # G (NM4): raw cmd then T, lower case, other characters spaces, one space at each end; never split.
+            G=" $(printf '%s\n%s\n' "$cmd" "$T" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9._/~$@+:-' ' ') " || ll_deny LL-BROKEN
+            # W (NM5, NM6): newline ; & | ( ) made ";", other characters outside the word set made spaces.
+            W=$(printf '%s\n' "$T" | tr '\n;&|()' ';;;;;;' | tr -c 'A-Za-z0-9._/=:@+~$;-' ' ') || ll_deny LL-BROKEN
+            # segs: the segments of W; a segment's words are ws=($seg) under set -f, and (NM7) a word's basename is ${w##*/}.
+            IFS=';' read -r -a segs <<<"$W"
+            # <<< normalise
+            # Tamper (FR-L-49, FR-L-50) on T and the words; escape (FR-L-47,
+            # FR-L-48) on the words of each segment, any position. W has no "_",
+            # so install_hooks is looked for in T.
+            LL_TT=$T
+            case $T in *install_hooks*) LL_CLASSES+='TAMPER ' ;; esac
+            LL_CL=0 LL_CF=0 # a claude word; a claude launch flag word (whole command)
+            for seg in "${segs[@]}"; do
+                ws=($seg)
+                LL_SC=0 # a superclaude word earlier in this segment
+                for ((i = 0; i < ${#ws[@]}; i++)); do
+                    w=${ws[i]}
+                    b=${w##*/}
+                    case $w in *.claude | *.claude/) LL_CLASSES+='TAMPER ' ;; esac
+                    [ "$w" = install ] && [ "$LL_SC" = 1 ] && LL_CLASSES+='TAMPER '
+                    case $w in -p | --print | --continue | --resume | --bare | --settings | --dangerously-skip-permissions | --fork-session | --session-id | --permission-mode) LL_CF=1 ;; esac
+                    case ${b%%@*} in claude | claude-code) LL_CL=1 ;; esac
+                    case $b in
+                    superclaude | superclaude.*) LL_SC=1 ;;
+                    ccsession* | tmux | screen | xdotool | ydotool) LL_CLASSES+='ESCAPE ' ;;
+                    orca)
+                        # w1, w2: the next two non-option words; --version counts as w1.
+                        LL_W1= LL_W2=
+                        for ((j = i + 1; j < ${#ws[@]}; j++)); do
+                            case ${ws[j]} in
+                            --version) [ -n "$LL_W1" ] || { LL_W1=--version && break; } ;;
+                            -*) ;;
+                            *)
+                                if [ -z "$LL_W1" ]; then
+                                    LL_W1=${ws[j]}
+                                else
+                                    LL_W2=${ws[j]}
+                                    break
+                                fi ;;
+                            esac
+                        done
+                        case "$LL_W1 $LL_W2" in
+                        'status '* | 'help '* | '--version '* | 'worktree current' | 'worktree list' | 'worktree show' | 'terminal list' | 'terminal show' | 'terminal read') ;;
+                        'orchestration check' | 'orchestration inbox' | 'orchestration run-current' | 'orchestration task-list' | 'orchestration worker-show') ;;
+                        *) case ${ws[${#ws[@]} - 1]} in --help | -h) ;; *) LL_CLASSES+='ESCAPE ' ;; esac ;;
+                        esac ;;
+                    esac
+                done
+            done
+            [ "$LL_CL$LL_CF" = 11 ] && LL_CLASSES+='ESCAPE '
+            # Git (FR-L-28 to FR-L-34) and gh (FR-L-35 to FR-L-39): G1, G2 and
+            # H2 test G; G3, G4, H1, H3, H4 and H5 read the words of each
+            # segment; then the canonical push check on raw cmd.
+            LL_RE='( |/)git(-[a-z][a-z-]*)? '
+            LL_GIT=0
+            [[ $G =~ $LL_RE ]] && LL_GIT=1
+            LL_RE='( |/)gh '
+            LL_GH=0
+            [[ $G =~ $LL_RE ]] && LL_GH=1
+            # H5 can only fire when G (lower case) holds one of these texts.
+            LL_URL=0
+            case $G in *repos/* | *api.github.com* | *uploads.github.com*) LL_URL=1 ;; esac
+            if [ "$LL_GH" = 1 ] && [[ $G == *' api '* ]]; then
+                # H2: a gh word and the word api anywhere is GHWRITE unless the
+                # raw cmd is one plain GET: the anchored form, no method, field
+                # or input word, and an endpoint that is not graphql or a merge.
+                LL_RE='^[[:space:]]*gh api( +[A-Za-z0-9._/:=,@%+-]+)+[[:space:]]*$'
+                LL_RE_W='^(-[A-Za-z]*[XfF].*|--method.*|--field.*|--raw-field.*|--input.*)$'
+                LL_OK=0
+                if [[ $cmd =~ $LL_RE ]]; then
+                    ws=($cmd) # the form admits no glob, quote or separator
+                    LL_OK=1 LL_EP= LL_V=0
+                    for ((i = 2; i < ${#ws[@]}; i++)); do
+                        w=${ws[i]}
+                        if [[ $w =~ $LL_RE_W ]]; then
+                            LL_OK=0
+                            break
+                        fi
+                        if [ "$LL_V" = 1 ]; then
+                            LL_V=0
+                            continue
+                        fi
+                        case $w in
+                        -H | --header | -q | --jq | -t | --template | --hostname | -p | --preview | --cache) LL_V=1 ;;
+                        -*) ;;
+                        *) [ -n "$LL_EP" ] || LL_EP=$w ;;
+                        esac
+                    done
+                    case ${LL_EP,,} in '' | graphql | */merge | */merges) LL_OK=0 ;; esac
+                fi
+                [ "$LL_OK" = 1 ] || LL_CLASSES+='GHWRITE '
+            fi
+            if [ "$LL_GIT" = 1 ]; then
+                LL_RE='( |/git-| git-)(merge|pull) '
+                [[ $G =~ $LL_RE ]] && LL_CLASSES+='MERGE '
+                LL_RE='( |/git-| git-)(push|send-pack|http-push) '
+                [[ $G =~ $LL_RE ]] && LL_CLASSES+='PUSH '
+                LL_RE='( |/git-| git-)(commit|cherry-pick|am|commit-tree) '
+                [[ $G =~ $LL_RE ]] && LL_CLASSES+='COMMIT '
+                LL_RE='alias\.|pushurl|insteadof|hookspath| (remote|url|include|includeif)\.| set-url '
+                [[ $G =~ $LL_RE ]] && LL_CLASSES+='UNKNOWN '
+            fi
+            if [ "$LL_GIT$LL_GH$LL_URL" != 000 ]; then
+                LL_RE_NAME='^[A-Za-z_][A-Za-z0-9_]*='
+                LL_RE_NUM='^[0-9]+(\.[0-9]+)?[smhd]?$'
+                LL_RE_DASH='^git-[a-z][a-z-]*$'
+                for seg in "${segs[@]}"; do
+                    ws=($seg)
+                    LL_CP=-1 # index of the command-position word, -1 while skipping
+                    LL_SGH=0 LL_H5= # a gh word in this segment; its H5 classes
+                    for ((i = 0; i < ${#ws[@]}; i++)); do
+                        w=${ws[i]}
+                        if [ "$LL_CP" = -1 ]; then
+                            case $w in -*) continue ;; esac
+                            LL_B=${w##*/} # wrappers and shells match by basename (NM7)
+                            case $LL_B in
+                            env | sudo | nohup | exec | command | builtin | timeout | xargs | setsid | time | nice | stdbuf | ionice | doas | unbuffer | eval | if | then | else | elif | do | while | until | coproc) continue ;;
+                            bash | sh | zsh | dash | ksh)
+                                if [[ ${ws[i + 1]:-} =~ ^-[a-z]*c$ ]]; then
+                                    i=$((i + 1))
+                                    continue
+                                fi ;;
+                            esac
+                            [[ $w =~ $LL_RE_NAME || $w =~ $LL_RE_NUM ]] && continue
+                            LL_CP=$i
+                        fi
+                        if [ "$LL_URL" = 1 ]; then
+                            # H5: a merge endpoint or a GitHub API host in any word.
+                            LL_LW=${w,,}
+                            if [[ $LL_LW == *repos/* && ($LL_LW == */merge || $LL_LW == */merges) ]]; then
+                                LL_H5+='MERGE '
+                            fi
+                            case $LL_LW in *api.github.com* | *uploads.github.com*) LL_H5+='GHWRITE ' ;; esac
+                        fi
+                        b=${w##*/}
+                        if [ "$b" = gh ]; then
+                            # H1: group and action, skipping -R and --repo values.
+                            LL_SGH=1 LL_GG= LL_GA= LL_HV=0
+                            for ((j = i + 1; j < ${#ws[@]}; j++)); do
+                                case ${ws[j]} in
+                                -R | --repo) j=$((j + 1)) ;;
+                                --version | --help) LL_HV=1 ;;
+                                -*) ;;
+                                *)
+                                    if [ -z "$LL_GG" ]; then
+                                        LL_GG=${ws[j]}
+                                    else
+                                        LL_GA=${ws[j]}
+                                        break
+                                    fi ;;
+                                esac
+                            done
+                            # G4: a repo option that ends the segment has no value.
+                            case ${ws[${#ws[@]} - 1]} in -R | --repo) LL_CLASSES+='UNKNOWN ' ;; esac
+                            # H3, first match wins (the space cannot occur in a word).
+                            case "$LL_GG $LL_GA" in
+                            'api '*) ;;
+                            ' ') [ "$LL_HV" = 1 ] || [ "$LL_CP" != "$i" ] || LL_CLASSES+='UNKNOWN ' ;;
+                            *' merge' | *' update-branch' | *' sync') LL_CLASSES+='MERGE ' ;;
+                            'alias '* | 'extension '* | *'$'*) LL_CLASSES+='UNKNOWN ' ;;
+                            'search '* | 'status '* | 'auth '* | 'browse '* | 'help '* | 'completion '*) ;;
+                            *' view' | *' list' | *' status' | *' diff' | *' checks' | *' watch' | *' checkout') ;;
+                            'pr create' | 'pr edit' | 'pr comment' | 'pr ready' | 'issue create' | 'issue edit' | 'issue comment') LL_CLASSES+='SUBMIT ' ;;
+                            *) [ "$LL_CP" != "$i" ] || LL_CLASSES+='UNKNOWN ' ;;
+                            esac
+                            # H4: each pr create needs a nonempty repo operand in its own segment.
+                            if [ "$LL_GG $LL_GA" = 'pr create' ]; then
+                                LL_RP=0
+                                for ((j = 0; j < ${#ws[@]}; j++)); do
+                                    case ${ws[j]} in
+                                    -R | --repo) [[ -n ${ws[j + 1]:-} && ${ws[j + 1]} != -* ]] && LL_RP=1 ;;
+                                    --repo=?*) LL_RP=1 ;;
+                                    esac
+                                done
+                                [ "$LL_RP" = 1 ] || LL_CLASSES+='REPO '
+                            fi
+                            continue
+                        fi
+                        case $b in git) ;; git-*) [[ $b =~ $LL_RE_DASH ]] || continue ;; *) continue ;; esac
+                        # S: the dashed name, or the first non-option word after git.
+                        LL_S= LL_SI=$i LL_HV=0 LL_LV= LL_DG=0
+                        if [ "$b" != git ]; then
+                            LL_S=${b#git-}
+                        else
+                            j=$((i + 1))
+                            while [ "$j" -lt "${#ws[@]}" ]; do
+                                case ${ws[j]} in
+                                -C | -c | --git-dir | --work-tree | --namespace | --config-env | --attr-source)
+                                    if [ $((j + 1)) -ge "${#ws[@]}" ]; then
+                                        LL_DG=1
+                                        break
+                                    fi
+                                    LL_LV=${ws[j + 1]}
+                                    j=$((j + 2)) ;;
+                                --version | --help | -h) LL_HV=1 j=$((j + 1)) ;;
+                                -*) j=$((j + 1)) ;;
+                                *) LL_S=${ws[j]} LL_SI=$j; break ;;
+                                esac
+                            done
+                        fi
+                        # G4: every git word, in command position or not.
+                        if [ "$LL_DG" = 1 ] || [[ $LL_S == *'$'* ]]; then
+                            LL_CLASSES+='UNKNOWN '
+                        fi
+                        [ "$LL_CP" = "$i" ] || continue
+                        # G3: the subcommand table, command position only.
+                        LL_NX=${ws[LL_SI + 1]:-}
+                        case $LL_S in
+                        '') [ "$LL_HV" = 1 ] || [ "$LL_LV" = '$' ] || LL_CLASSES+='UNKNOWN ' ;;
+                        commit | cherry-pick | revert | am | commit-tree) LL_CLASSES+='COMMIT ' ;;
+                        update-ref)
+                            for ((j = LL_SI + 1; j < ${#ws[@]}; j++)); do
+                                case ${ws[j]} in HEAD | --stdin | refs/heads/*) LL_CLASSES+='COMMIT ' && break ;; esac
+                            done ;;
+                        merge | pull) LL_CLASSES+='MERGE ' ;;
+                        push) LL_CLASSES+='PUSH ' ;;
+                        add | apply | bisect | blame | branch | cat-file | check-attr | check-ignore | check-ref-format | checkout | clean | count-objects | describe | diff | diff-files | diff-index | diff-tree | fetch | for-each-ref | format-patch | fsck | gc | grep | hash-object | help | log | ls-files | ls-remote | ls-tree | merge-base | merge-tree | mv | name-rev | range-diff | read-tree | rebase | reflog | reset | restore | rev-list | rev-parse | rm | shortlog | show | show-branch | show-ref | stash | status | switch | tag | var | version | whatchanged | write-tree) ;;
+                        remote) case $LL_NX in '' | -v | --verbose | get-url | show) ;; *) LL_CLASSES+='UNKNOWN ' ;; esac ;;
+                        config) case $LL_NX in --get | --get-all | --get-regexp | --list | -l | get | list) ;; *) LL_CLASSES+='UNKNOWN ' ;; esac ;;
+                        worktree) [ "$LL_NX" = list ] || LL_CLASSES+='UNKNOWN ' ;;
+                        *) LL_CLASSES+='UNKNOWN ' ;;
+                        esac
+                    done
+                    [ "$LL_SGH" = 1 ] || LL_CLASSES+=$LL_H5 # H5 only where no gh word is
+                done
+                # Canonical push (FR-L-33, FR-L-34): only one plain git push to origin passes.
+                case $LL_CLASSES in
+                *' PUSH '*)
+                    LL_RE='^[[:space:]]*git push( (-u|--set-upstream))? origin ([A-Za-z0-9_][A-Za-z0-9._/-]*)(:([A-Za-z0-9_][A-Za-z0-9._/-]*))?[[:space:]]*$'
+                    if [[ $cmd =~ $LL_RE ]]; then
+                        LL_D=${BASH_REMATCH[5]:-${BASH_REMATCH[3]}}
+                        case $LL_D in refs/heads/*) LL_D=${LL_D#refs/heads/} ;; heads/*) LL_D=${LL_D#heads/} ;; esac
+                        case $LL_D in master | main) LL_CLASSES+='PROTECTED ' ;; HEAD) LL_CLASSES+='PUSHFORM ' ;; esac
+                    else
+                        LL_CLASSES+='PUSHFORM '
+                    fi ;;
+                esac
+            fi
+        fi
+    elif [ "$LL_TOOL" = Edit ] || [ "$LL_TOOL" = Write ] || [ "$LL_TOOL" = NotebookEdit ]; then
+        # EPATH: the edit path after the NM3 "/" squeeze, one sed; the tamper check reads it.
+        EPATH=
+        if [ -n "$LL_PATH" ]; then
+            EPATH=$(printf '%s\n' "$LL_PATH" | sed -E -e 's#/+#/#g' -e 's#/(\./)+#/#g') || ll_deny LL-BROKEN
+        fi
+        # FR-L-42, FR-L-51: the tamper check only; contents are never read.
+        LL_TT=$EPATH
+        case $EPATH in */../* | */..) LL_CLASSES+='TAMPER ' ;; esac
+    elif [ "$LL_TOOL" = Agent ] || [ "$LL_TOOL" = Task ]; then
+        # FR-L-41, FR-L-46: local or background is NONE; the prompt is never scanned.
+        [ "$LL_ISO" = remote ] && LL_CLASSES+='ESCAPE '
+    elif [[ $LL_TOOL =~ ^(Cron|Schedule)[A-Za-z]*$ ]]; then
+        LL_CLASSES+='TURN ' # FR-L-43
+    elif [ "$LL_TOOL" = RemoteTrigger ] || [ "$LL_TOOL" = Workflow ] || [ "$LL_TOOL" = SendMessage ]; then
+        LL_CLASSES+='ESCAPE ' # FR-L-46
+    elif [[ $LL_TOOL == mcp__* ]]; then
+        # FR-L-45: N is the text after the last "__", lower case.
+        LL_N=${LL_TOOL##*__}
+        LL_N=${LL_N,,}
+        case $LL_N in
+        *merge* | *push* | *commit* | *pull_request* | *create_or_update_file* | *delete_file* | *update_ref* | *create_ref* | *create_branch*)
+            case $LL_N in
+            list_* | get_* | search_* | read_*) ;;
+            *merge*) LL_CLASSES+='MERGE ' ;;
+            *) LL_CLASSES+='MCP ' ;;
+            esac ;;
+        esac
+    else
+        : # FR-L-66: any other tool the matcher let through is NONE.
+    fi
+    # FR-L-49: the tamper tokens in T or the edit path; the store part is
+    # built from LL_S1 and LL_S2, so this text never names it joined.
+    case $LL_TT in
+    *"$LL_S1/$LL_S2"* | *.claude/settings* | *.claude/hooks* | *disableAllHooks* | *.gitconfig* | *.git/config* | *.config/git*) LL_CLASSES+='TAMPER ' ;;
+    esac
+    # LL-TEXT: every class of a Bash or Monitor call came from its text.
+    if [ "$LL_TOOL" = Bash ] || [ "$LL_TOOL" = Monitor ]; then
+        LL_NOTE_TEXT=1
+    fi
+
+    # 9. One case on CLASS:LEVEL, taken in message precedence; any blocked class
+    # blocks the call with the first blocked class's message.
+    for LL_C in BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL; do
+        case $LL_CLASSES in *" $LL_C "*) ;; *) continue ;; esac
+        case $LL_C:$LL_LEVEL in
+        IMPL:WA | IMPL:F | IMPL:FS | TURN:WA | TURN:F | TURN:FS) ;;
+        SUBMIT:FS | COMMIT:FS | PUSH:FS | SKILL:FS) ;;
+        IMPL:W | TURN:W) ll_deny "LL-$LL_C" ;;
+        SUBMIT:W | SUBMIT:WA | SUBMIT:F | COMMIT:W | COMMIT:WA | COMMIT:F) ll_deny "LL-$LL_C" ;;
+        PUSH:W | PUSH:WA | PUSH:F | SKILL:W | SKILL:WA | SKILL:F) ll_deny "LL-$LL_C" ;;
+        REPO:W | REPO:WA | REPO:F | REPO:FS) ll_deny LL-REPO ;;
+        PUSHFORM:W | PUSHFORM:WA | PUSHFORM:F | PUSHFORM:FS) ll_deny LL-PUSH-FORM ;;
+        PROTECTED:W | PROTECTED:WA | PROTECTED:F | PROTECTED:FS) ll_deny LL-PROTECTED ;;
+        MERGE:W | MERGE:WA | MERGE:F | MERGE:FS) ll_deny LL-MERGE ;;
+        GHWRITE:W | GHWRITE:WA | GHWRITE:F | GHWRITE:FS) ll_deny LL-GH-WRITE ;;
+        UNKNOWN:W | UNKNOWN:WA | UNKNOWN:F | UNKNOWN:FS) ll_deny LL-UNKNOWN ;;
+        MCP:W | MCP:WA | MCP:F | MCP:FS) ll_deny LL-MCP ;;
+        ESCAPE:W | ESCAPE:WA | ESCAPE:F | ESCAPE:FS) ll_deny LL-ESCAPE ;;
+        TAMPER:W | TAMPER:WA | TAMPER:F | TAMPER:FS) ll_deny LL-TAMPER ;;
+        BIG:W | BIG:WA | BIG:F | BIG:FS) ll_deny LL-BIG ;;
+        *) ll_deny LL-BROKEN ;;
+        esac
+    done
+    exit 0
+fi
+
+# 10. Default deny
+ll_deny LL-BROKEN
diff --git a/src/superclaude/cli/install_hooks.py b/src/superclaude/cli/install_hooks.py
index 895e2878..e71bff5a 100644
--- a/src/superclaude/cli/install_hooks.py
+++ b/src/superclaude/cli/install_hooks.py
@@ -85,6 +85,9 @@ _FRESHNESS_SCRIPTS = [
     "block-bare-python.sh",
     # PreToolUse Bash identity adapter; ordinary sessions stay unmodified.
     "launch-job-identity.sh",
+    # UserPromptSubmit + PreToolUse launch-level guard (L1); ordinary sessions
+    # are allowed, only a bound governed session is restricted.
+    "launch-level-guard.sh",
 ]
 _LEGACY_SCRIPTS = ["session-init.sh"]
 
@@ -123,6 +126,27 @@ def _owns_command(command: object, managed: set, event: str) -> bool:
     return script is not None and any(_ccsession_script(m) == script for m in managed)
 
 
+def _owns_registration(reg: object, managed: set, event: str) -> bool:
+    """True when any hook inside the registration runs a managed command."""
+    if not isinstance(reg, dict) or not isinstance(reg.get("hooks"), list):
+        return False
+    return any(
+        isinstance(hook, dict) and _owns_command(hook.get("command"), managed, event)
+        for hook in reg["hooks"]
+    )
+
+
+def _registration_commands(reg: object) -> set:
+    inner = reg.get("hooks", []) if isinstance(reg, dict) else []
+    if not isinstance(inner, list):
+        return set()
+    return {
+        hook.get("command")
+        for hook in inner
+        if isinstance(hook, dict) and hook.get("command")
+    }
+
+
 def install_hooks(
     target_path: Path | None = None, force: bool = False
 ) -> Tuple[bool, str]:
@@ -365,36 +389,20 @@ def _merge_settings(
                 backup_path,
             )
 
-        for new_reg in registrations:
+        source_commands = [_registration_commands(reg) for reg in registrations]
+        for index, new_reg in enumerate(registrations):
             if not isinstance(new_reg, dict):
                 continue
 
-            new_inner = new_reg.get("hooks", [])
-            if not isinstance(new_inner, list):
-                new_inner = []
-            managed_commands = {
-                hook.get("command")
-                for hook in new_inner
-                if isinstance(hook, dict) and hook.get("command")
-            }
+            managed_commands = source_commands[index]
 
             # Framework ownership is identified by the command path, never by a
             # matcher alone. Different hooks commonly share matcher="*" or Bash.
-            owns_existing = False
             if managed_commands:
-                for existing_reg in event_list:
-                    if not isinstance(existing_reg, dict):
-                        continue
-                    existing_inner = existing_reg.get("hooks", [])
-                    if not isinstance(existing_inner, list):
-                        continue
-                    if any(
-                        isinstance(hook, dict)
-                        and _owns_command(hook.get("command"), managed_commands, event)
-                        for hook in existing_inner
-                    ):
-                        owns_existing = True
-                        break
+                owns_existing = any(
+                    _owns_registration(existing_reg, managed_commands, event)
+                    for existing_reg in event_list
+                )
             else:
                 new_signature = _registration_signature(new_reg)
                 owns_existing = any(
@@ -444,8 +452,19 @@ def _merge_settings(
                 continue
 
             # A matcher-only collision is unrelated user configuration. Preserve
-            # it and append the missing framework registration.
-            event_list.append(new_reg)
+            # it and add the missing framework registration before the first
+            # registration owned by a LATER source entry, so an upgrade keeps
+            # the source order (e.g. launch-job-identity.sh stays last).
+            later = set().union(*source_commands[index + 1 :])
+            position = next(
+                (
+                    i
+                    for i, existing_reg in enumerate(event_list)
+                    if _owns_registration(existing_reg, later, event)
+                ),
+                len(event_list),
+            )
+            event_list.insert(position, new_reg)
             added += 1
 
     existing["hooks"] = existing_hooks
diff --git a/tests/cli/test_install_hooks.py b/tests/cli/test_install_hooks.py
index c98c560b..f7f2c7bd 100644
--- a/tests/cli/test_install_hooks.py
+++ b/tests/cli/test_install_hooks.py
@@ -101,6 +101,7 @@ def fake_source_hooks(tmp_path, monkeypatch):
         "codegraph-session-start.sh",
         "block-bare-python.sh",
         "launch-job-identity.sh",
+        "launch-level-guard.sh",
     ]:
         (scripts_pkg / name).write_text("#!/usr/bin/env bash\nexit 0\n")
     (legacy_scripts_pkg / "session-init.sh").write_text("#!/usr/bin/env bash\nexit 0\n")
@@ -993,3 +994,154 @@ def test_launch_identity_real_install_preserves_policies_and_is_idempotent(
     )
     assert not list((state / "requests").iterdir())
     assert not list((state / "jobs").iterdir())
+
+
+_LAUNCH_GUARD_HOOK = "~/.claude/hooks/launch-level-guard.sh"
+_GUARD_EVENTS = ("UserPromptSubmit", "PreToolUse")
+
+
+def _guard_count(registrations: list) -> int:
+    return sum(
+        h.get("command") == _LAUNCH_GUARD_HOOK
+        for reg in registrations
+        for h in reg.get("hooks", [])
+    )
+
+
+def _real_source_hooks() -> dict:
+    root = Path(__file__).resolve().parents[2]
+    return json.loads((root / "src/superclaude/hooks/hooks.json").read_text())["hooks"]
+
+
+def test_launch_level_guard_script_is_packaged_listed_executable_and_mirrored():
+    from superclaude.cli import install_hooks
+
+    root = Path(__file__).resolve().parents[2]
+    source = root / "src/superclaude/hooks/scripts/launch-level-guard.sh"
+    mirror = root / "plugins/superclaude/hooks/scripts/launch-level-guard.sh"
+    assert "launch-level-guard.sh" in install_hooks._FRESHNESS_SCRIPTS
+    assert os.access(source, os.X_OK) and os.access(mirror, os.X_OK)
+    assert source.read_bytes() == mirror.read_bytes()
+    assert source.read_text().startswith("#!/bin/bash\n")
+
+
+@pytest.mark.parametrize("force", [False, True])
+def test_launch_level_guard_real_install_registers_both_events_and_is_idempotent(
+    tmp_path, force
+):
+    root = Path(__file__).resolve().parents[2]
+    home = tmp_path / "isolated-home"
+    target = home / ".claude/settings.json"
+    assert target.resolve() != (Path.home() / ".claude/settings.json").resolve()
+    target.parent.mkdir(parents=True)
+    user_prompt = {
+        "hooks": [{"type": "command", "command": "/user/prompt-policy", "timeout": 4}]
+    }
+    user_bash = {
+        "matcher": "Bash",
+        "hooks": [{"type": "command", "command": "/user/bash-policy", "timeout": 9}],
+    }
+    user_stop = {
+        "hooks": [{"type": "command", "command": "/user/stop-policy", "timeout": 2}]
+    }
+    permissions = {"deny": ["Bash(rm *)"], "ask": ["Bash(git push *)"]}
+    target.write_text(
+        json.dumps(
+            {
+                "permissions": permissions,
+                "hooks": {
+                    "UserPromptSubmit": [user_prompt],
+                    "PreToolUse": [user_bash],
+                    "Stop": [user_stop],
+                },
+            }
+        )
+    )
+    source_hooks = _real_source_hooks()
+
+    ok, message = install_hooks(target_path=target, force=force)
+    assert ok, message
+    first_bytes = target.read_bytes()
+    settings = json.loads(first_bytes)
+    assert settings["permissions"] == permissions
+    hooks = settings["hooks"]
+    assert hooks["Stop"][0] == user_stop
+    assert hooks["UserPromptSubmit"][0] == user_prompt
+    assert hooks["PreToolUse"][0] == user_bash
+    for event in _GUARD_EVENTS:
+        assert _guard_count(hooks[event]) == 1
+    for event, registrations in source_hooks.items():
+        assert all(reg in hooks[event] for reg in registrations), event
+    assert _LAUNCH_IDENTITY_HOOK in [
+        h["command"] for h in hooks["PreToolUse"][-1]["hooks"]
+    ]
+
+    for second_force in (False, True):
+        ok, message = install_hooks(target_path=target, force=second_force)
+        assert ok, message
+        assert target.read_bytes() == first_bytes
+
+    installed = target.parent / "hooks/launch-level-guard.sh"
+    source = root / "src/superclaude/hooks/scripts/launch-level-guard.sh"
+    assert installed.read_bytes() == source.read_bytes()
+    assert os.access(installed, os.X_OK)
+
+
+@pytest.mark.parametrize("force", [False, True])
+def test_launch_level_guard_upgrade_lands_before_launch_identity(tmp_path, force):
+    """An install that predates the guard gains it in source order."""
+    target = tmp_path / "isolated-home/.claude/settings.json"
+    target.parent.mkdir(parents=True)
+    source_hooks = _real_source_hooks()
+    previous = {
+        event: [
+            reg
+            for reg in registrations
+            if not any(h.get("command") == _LAUNCH_GUARD_HOOK for h in reg["hooks"])
+        ]
+        for event, registrations in source_hooks.items()
+    }
+    assert all(_guard_count(previous[event]) == 0 for event in _GUARD_EVENTS)
+    target.write_text(json.dumps({"hooks": previous}))
+
+    ok, message = install_hooks(target_path=target, force=force)
+    assert ok, message
+    hooks = json.loads(target.read_text())["hooks"]
+    for event in _GUARD_EVENTS:
+        assert hooks[event] == source_hooks[event], event
+    assert hooks["PreToolUse"][-1]["hooks"][0]["command"] == _LAUNCH_IDENTITY_HOOK
+
+
+@pytest.mark.parametrize("force", [False, True])
+def test_one_command_under_two_events_is_owned_per_event(
+    fake_source_hooks, target_settings, force
+):
+    """The same command is registered and refreshed separately in each event."""
+    shared = "~/.claude/hooks/launch-level-guard.sh"
+    new_hook = {"type": "command", "command": shared, "timeout": 5}
+    prompt_reg = {"hooks": [new_hook]}
+    tool_reg = {"matcher": "^(Bash|Skill)$", "hooks": [new_hook]}
+    (fake_source_hooks / "hooks/hooks.json").write_text(
+        json.dumps(
+            {"hooks": {"UserPromptSubmit": [prompt_reg], "PreToolUse": [tool_reg]}}
+        )
+    )
+    stale_tool = {
+        "matcher": "Bash",
+        "hooks": [{"type": "command", "command": shared, "timeout": 1}],
+    }
+    user_same_matcher = {
+        "matcher": "^(Bash|Skill)$",
+        "hooks": [{"type": "command", "command": "/user/other", "timeout": 2}],
+    }
+    target_settings.write_text(
+        json.dumps({"hooks": {"PreToolUse": [stale_tool, user_same_matcher]}})
+    )
+
+    for _ in range(2):
+        ok, message = install_hooks(target_path=target_settings, force=force)
+        assert ok, message
+        hooks = json.loads(target_settings.read_text())["hooks"]
+        assert hooks["UserPromptSubmit"] == [prompt_reg]
+        expected_tool = tool_reg if force else stale_tool
+        assert hooks["PreToolUse"] == [expected_tool, user_same_matcher]

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
