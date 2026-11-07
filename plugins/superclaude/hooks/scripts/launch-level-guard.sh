#!/bin/bash
# Launch-level guard (L1), IronbellyOrg/IronClaude issue #394.
# Design: docs/designs/sc-issue-launch-level-hook.md (sections 2, 3, 8, 9).
# Registered on UserPromptSubmit and PreToolUse. Exit 0 allows; exit 2 blocks
# with a message on stderr; never exit 1, no onFailure. Only a session that the
# claim script launched (a valid top-level session_id bound in the store) is
# governed; every other session is ordinary and never blocked (FR-L-53).
# Ten-part layout (DD-1); part 8 holds the section 5.2 classifiers (Skill, Bash,
# Monitor, edits, Agent/Task, Cron/Schedule, escape and MCP tools); others NONE.
# launch-level-guard-version: 1

# 1. Settings
export LC_ALL=C
set -u -o pipefail
set -f
umask 077

# >>> printer (parts 2 and 3; the tests run this block on its own)
# 2. Store path: three literal parts, so this text never names the joined path.
LL_S1=.claude
LL_S2=state
LL_S3=launch-level
LL_STORE="${HOME:-}/$LL_S1/$LL_S2/$LL_S3"

# 3. Messages (section 9). LL_LEVEL is W, WA, F, FS or empty (unknown).
LL_LEVEL=
LL_SID=
LL_NOTE_STATE=0
LL_NOTE_TEXT=0
LL_DENIED=0

ll_valid_sid() {
    [[ $1 =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]]
}

ll_say() {
    local id=$1 lvl= b w y
    if [ "$id" = LL-TAMPER ] && ! ll_valid_sid "$LL_SID"; then
        id=LL-BROKEN
    fi
    case $id in
    LL-IMPL)
        b='starting /sc:implement, /task, /sc:improve, /sc:cleanup, /sc:spawn or /sc:build (or their skills).'
        w='At the worktree level the agent stops at a plan until a person approves it.'
        y='Read the plan, then type /sc:implement or /task, or reply approved, in this session.' ;;
    LL-COMMIT)
        b='creating a commit (git commit, cherry-pick, revert, am, or moving a branch with update-ref).'
        w='Only a launch with --pipeline full --submit lets the agent commit.'
        y='Review the changes and commit them yourself, or claim the issue again with --pipeline full --submit.' ;;
    LL-PUSH)
        b='a git push.'
        w='Only a launch with --pipeline full --submit lets the agent push.'
        y='Push the branch yourself after review, or claim the issue again with --pipeline full --submit.' ;;
    LL-PUSH-FORM)
        b='a push that is not one plain git push command, or a command that names git and push together.'
        w='The guard can check a push only when the whole command is git push [-u] origin <branch> (or <source>:<branch>), with nothing before or after it; other forms (force, --all, another remote, variables, backticks, line continuations, chained or piped commands) can reach another remote or the main branch.'
        y='Run the push as its own command, exactly: git push origin <branch> or git push -u origin <branch>, with the branch name written out.' ;;
    LL-PROTECTED)
        b='a push to master or main.'
        w='No launch level may change the main branch.'
        y='Push the feature branch by name, then merge it through a reviewed pull request.' ;;
    LL-MERGE)
        b='a merge (git merge, git pull, gh pr merge, a call to a GitHub merge URL, or an MCP merge tool).'
        w='No launch level may merge; only a person reviews and merges.'
        y='Leave the merge to a person. To update the branch, run git fetch, then git rebase.' ;;
    LL-GH-WRITE)
        b='a gh api call that is not one plain read command (it sets a method, a field or an input, calls graphql or a merge endpoint, or uses variables, quotes, pipes or other commands around it), or a gh command whose text mentions api, or a direct call to the GitHub API.'
        w='In a launched session gh api may only read, and only in a form the guard can check: a gh api write can merge, comment or change the main branch.'
        y='Run the read as one plain command with every value written out, for example gh api repos/o/r/pulls/5 --jq .state, or use a gh command for the step (gh pr view --json, gh pr comment, gh pr create --repo ...) at a level that allows it, or ask the person.' ;;
    LL-SUBMIT)
        b='/sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request or issue).'
        w='Publishing work needs a launch with --pipeline full --submit.'
        y='Run it yourself in your own session, or claim the issue again with --pipeline full --submit.' ;;
    LL-REPO)
        b='gh pr create without --repo.'
        w='Without --repo, gh can open the pull request on the parent repository of a fork.'
        y='Retry with --repo <owner>/<name> (or -R).' ;;
    LL-UNKNOWN)
        b='a git or gh command the guard does not recognise (an unknown subcommand, a git alias definition, or a subcommand built from a variable or a substitution), or a line continuation inside a word.'
        w='In a launched session only known git and gh commands may run, so a renamed command or an alias cannot commit, push or merge.'
        y='Use the standard command written out (for example git status, git diff, git add), or ask the person to run it. Write the command on one line.' ;;
    LL-MCP)
        b='a GitHub write through an MCP tool.'
        w='The guard cannot check where an MCP write lands, so a launched session writes to GitHub only through git and gh.'
        y='Use git or gh for this step.' ;;
    LL-ESCAPE)
        b='starting or messaging another agent or session (claude, ccsession, orca, SendMessage, /sc:issue, a remote subagent, a workflow, a remote trigger) or typing into a terminal (tmux, screen, xdotool).'
        w="That work would run outside this session's launch level."
        y='Do the work here (local subagents are allowed), or ask the person to start it.' ;;
    LL-TURN)
        b='scheduling a turn (a cron job or a wake-up) before the plan is approved.'
        w='Its prompt text arrives later as a new turn and could look like a person replying approved.'
        y='Wait until the person approves the plan, or use a background task or a monitor instead.' ;;
    LL-TAMPER)
        b='touching the launch-level state, the Claude Code settings or hooks, a git configuration file, or reinstalling the hooks.'
        w='The session must not change its own limits.'
        y="Ask the person. To release this session they run, in their own terminal: rm \"$LL_STORE/sessions/$LL_SID\" \"$LL_STORE/sessions/$LL_SID.ok\"" ;;
    LL-SKILL)
        b='a skill call whose name the guard cannot read.'
        w='The guard cannot tell whether the skill is allowed at this level.'
        y='Report it (the hook input format may have changed); the person can release the session.' ;;
    LL-BIG)
        b='a command longer than 64 KB.'
        w='The guard cannot check a command that long in time.'
        y='Write the content to a file with the Write tool, then run a short command.' ;;
    LL-NOBIND)
        b='this launch prompt.'
        w='The session was started by /sc:issue --claim, but the guard could not register it, so its limits could not be enforced.'
        y="Check that jq is installed and $LL_STORE is writable, then claim the issue again." ;;
    *)
        b='this action, because the launch-level guard could not run (jq missing, unreadable input or an internal error).'
        w='In a launched session the guard fails closed.'
        y="Install jq, or ask the person to release the session by deleting its files in $LL_STORE/sessions/." ;;
    esac
    case $LL_LEVEL in
    W) lvl=worktree ;;
    WA) lvl='worktree (approved)' ;;
    F) lvl=full ;;
    FS) lvl='full --submit' ;;
    esac
    if [ -n "$lvl" ]; then
        printf '%s\n' "Launch-level guard: this session was started by /sc:issue --claim at level $lvl." >&2
    else
        printf '%s\n' 'Launch-level guard:' >&2
    fi
    printf '%s\n' "Blocked: $b" "Why: $w" "You can: $y" >&2
    if [ "$LL_NOTE_STATE" = 1 ]; then
        printf '%s\n' 'Note: the launch record was invalid or unreadable, so the strictest level (worktree) applies.' >&2
    fi
    if [ "$LL_NOTE_TEXT" = 1 ]; then
        printf '%s\n' 'Note: the guard does not tell quoted text from commands. Any command that names git together with the word commit, push, merge or pull, or gh together with the word api, counts as that action, even if the words are only in a message, a title, a PR body or a search pattern. If that is the case here, write the text to a file with the Write tool and pass it with git commit -F <file> or gh ... --body-file <file>, or reword the search or title.' >&2
    fi
}

ll_deny() {
    LL_DENIED=1
    ll_say "$1"
    exit 2
}
# <<< printer

# Any exit other than 0 or a deliberate deny is an internal failure. A governed
# session fails closed (LL-BROKEN, LL-NOBIND in the prompt branch); an ordinary
# session is never blocked by a failure.
LL_GOVERNED=0
LL_BRANCH=
ll_on_exit() {
    local rc=$?
    trap - EXIT
    if [ "$rc" = 0 ] || { [ "$rc" = 2 ] && [ "$LL_DENIED" = 1 ]; }; then
        exit "$rc"
    fi
    if [ "$LL_GOVERNED" != 1 ]; then
        exit 0
    fi
    if [ "$LL_BRANCH" = prompt ]; then
        ll_say LL-NOBIND
    else
        ll_say LL-BROKEN
    fi
    exit 2
}
trap ll_on_exit EXIT

# 4. Dispatch
LL_INPUT=$(cat)
# Empty-store fast exit: no session records and no launch marker.
if [ ! -d "$LL_STORE/sessions" ]; then
    case $LL_INPUT in
    *'[sc-launch:'*) ;;
    *) exit 0 ;;
    esac
fi
# One parse of the top-level fields (FR-L-10; also part 7, the tool fields).
# Line 1: event, agent_id flag (prompt only), input-error flag, session id.
# Lines 2 to 5: tool name, skill name (skill unless missing or null, else
# name), edit path (file_path unless missing or null, else notebook_path),
# isolation, each with CR and LF made spaces. Then the prompt (NUL made a
# space) or the command, kept whole, and a "." so no trailing newline is lost.
# A nonstring tool field, a NUL in one or a nonobject tool_input is an input
# error. Nested keys never count; agent_id is never read on PreToolUse.
LL_PARSED=$(jq -r '
    def str: if type == "string" then . else "" end;
    def line: str | split("\u0000") | join(" ") | gsub("[\r\n]"; " ");
    (.hook_event_name | if . == "UserPromptSubmit" or . == "PreToolUse" then . else "OTHER" end) as $e
    | (if $e == "PreToolUse" then . else {} end) as $p
    | ($p.tool_input) as $ti
    | ($ti | if type == "object" then . else {} end) as $o
    | ($p.tool_name) as $tn
    | ($tn | str) as $t
    | (if $t != "Skill" then null elif $o.skill != null then $o.skill else $o.name end) as $sk
    | (if ($t == "Edit" or $t == "Write" or $t == "NotebookEdit") | not then null
        elif $o.file_path != null then $o.file_path else $o.notebook_path end) as $fp
    | (if $t == "Agent" or $t == "Task" then $o.isolation else null end) as $iso
    | (if $t == "Bash" or $t == "Monitor" then $o.command else null end) as $cmd
    | (any($tn, $sk, $fp, $iso, $cmd; . != null and (type != "string" or (explode | any(. == 0))))
        or ($ti != null and ($ti | type) != "object")) as $bad
    | $e + " "
    + (if $e == "UserPromptSubmit" then (.agent_id | if type == "string" and length > 0 then "1" else "0" end) else "0" end)
    + " " + (if $bad then "1" else "0" end) + " "
    + (.session_id | if type == "string" and test("\\A[A-Za-z0-9][A-Za-z0-9_-]{0,127}\\z") then . else "" end)
    + "\n" + ($t | line) + "\n" + ($sk | line) + "\n" + ($fp | line) + "\n" + ($iso | line) + "\n"
    + (if $e == "UserPromptSubmit" then .prompt else $cmd end | str | split("\u0000") | join(" "))
    + "."
' <<<"$LL_INPUT" 2>/dev/null)
LL_RC=$?
LL_BAD=0 LL_TOOL= LL_SKILL= LL_PATH= LL_ISO= LL_TEXT= LL_PROMPT=
if [ "$LL_RC" != 0 ]; then
    # No jq or no parseable envelope: no level is inferred. A tool payload
    # looks at every session_id value for one that has a record, only to find a
    # positively bound session, which then falls through to the last line
    # (LL-BROKEN); this can only block, never allow early. Declared limit: any
    # bound id in the text counts, even a nested one, so an ordinary session
    # sending broken JSON that contains a bound id is blocked. A recognizable launch-marker
    # prompt (marker text, no tool_name key) blocks rather than starting
    # ungoverned; anything else is identity loss (section 3): allow without
    # claiming enforcement.
    case $LL_INPUT in
    *'"tool_name"'*)
        LL_EVENT=FAILED
        LL_RAWRE='"session_id"[[:space:]]*:[[:space:]]*"([A-Za-z0-9][A-Za-z0-9_-]{0,127})"(.*)'
        LL_REST=$LL_INPUT
        # No cap on the number of session_id values tried (a cap would let a payload with many forged ids hide the real bound one).
        while :; do
            [[ $LL_REST =~ $LL_RAWRE ]] || break
            LL_REST=${BASH_REMATCH[2]}
            if [ -e "$LL_STORE/sessions/${BASH_REMATCH[1]}" ] || [ -L "$LL_STORE/sessions/${BASH_REMATCH[1]}" ]; then
                LL_SID=${BASH_REMATCH[1]}
                break
            fi
        done
        LL_REST= ;;
    *'[sc-launch:'*)
        LL_BRANCH=prompt
        LL_GOVERNED=1
        ll_deny LL-NOBIND ;;
    *) exit 0 ;;
    esac
else
    # read, not ${var#*$'\n'}: pattern removal is quadratic on a long line.
    {
        read -r LL_EVENT LL_AGENT LL_BAD LL_SID
        IFS= read -r LL_TOOL
        IFS= read -r LL_SKILL
        IFS= read -r LL_PATH
        IFS= read -r LL_ISO
        IFS= read -r -d '' LL_TEXT
    } <<<"$LL_PARSED"
    LL_SID=${LL_SID:-}
    LL_TEXT=${LL_TEXT%$'.\n'} # the here-string adds the newline after the "."
    [ "$LL_EVENT" = UserPromptSubmit ] && LL_PROMPT=$LL_TEXT
fi

# A valid id with a record (of any file kind) is positively governed. Its level
# is exactly one allowed word plus an optional newline; anything else is
# worktree with the LL-STATE note; .ok at worktree gives worktree (approved).
if [ -n "$LL_SID" ] && { [ -e "$LL_STORE/sessions/$LL_SID" ] || [ -L "$LL_STORE/sessions/$LL_SID" ]; }; then
    LL_GOVERNED=1
    LL_FILE="$LL_STORE/sessions/$LL_SID"
    LL_REC=
    if [ -f "$LL_FILE" ] && [ ! -L "$LL_FILE" ] && [ -r "$LL_FILE" ]; then
        IFS= read -r -N 13 LL_REC <"$LL_FILE"
    fi
    case $LL_REC in
    worktree | worktree$'\n') LL_LEVEL=W ;;
    full | full$'\n') LL_LEVEL=F ;;
    full-submit | full-submit$'\n') LL_LEVEL=FS ;;
    *) LL_LEVEL=W LL_NOTE_STATE=1 ;;
    esac
    if [ "$LL_LEVEL" = W ] && [ -f "$LL_FILE.ok" ] && [ ! -L "$LL_FILE.ok" ]; then
        LL_LEVEL=WA
    fi
fi

case $LL_EVENT in
UserPromptSubmit) LL_BRANCH=prompt ;;
PreToolUse) LL_BRANCH=tool ;;
*)
    # Unknown event shape: identity-loss allow unless positively governed,
    # which falls through to the last line (LL-BROKEN).
    [ "$LL_GOVERNED" = 1 ] || exit 0 ;;
esac

# 5. Prompt branch: binding (FR-L-09, B1 to B13), then approval (FR-L-15 to FR-L-19).
# Writes: mkdir -p sessions; take pending/<nonce> with one rename (mv) to
# sessions/.take-<sid>, so a nonce is consumed once; publish sessions/<sid> with
# a hard link (ln), which fails when the target exists, so the first binding is
# never replaced. Temporary names start with a dot and are never a valid id.
ll_publish() {
    local tmp="$LL_SESS/.tmp-$LL_SID-$$"
    rm -f -- "$tmp" 2>/dev/null
    if (set -C; printf '%s' "$1" >"$tmp") 2>/dev/null; then
        ln -- "$tmp" "$LL_SESS/$LL_SID" 2>/dev/null
    fi
    rm -f -- "$tmp" 2>/dev/null
    return 0
}
# Publish from a taken record, ours or a racing prompt's for the same id.
ll_link_take() {
    local w=
    { [ -f "$LL_TAKE" ] && [ ! -L "$LL_TAKE" ]; } || return 0
    { IFS= read -r -N 13 w <"$LL_TAKE"; } 2>/dev/null
    case $w in
    worktree | full | full-submit | worktree$'\n' | full$'\n' | full-submit$'\n')
        ln -- "$LL_TAKE" "$LL_SESS/$LL_SID" 2>/dev/null ;;
    *) ll_publish degraded ;;
    esac
    # Drop the taken record only once a binding exists, so a failed link never loses it.
    if [ -e "$LL_SESS/$LL_SID" ] || [ -L "$LL_SESS/$LL_SID" ]; then
        rm -f -- "$LL_TAKE" 2>/dev/null
    fi
    return 0
}
if [ "$LL_BRANCH" = prompt ]; then
    [ "$LL_AGENT" = 1 ] && exit 0 # B5: a subagent prompt never binds or approves
    # B6: strict marker anywhere; loose marker at the start after whitespace or a BOM.
    LL_NONCE=
    LL_RE='\[sc-launch:v1:([0-9a-f]{32})\]'
    [[ $LL_PROMPT =~ $LL_RE ]] && LL_NONCE=${BASH_REMATCH[1]}
    LL_WS=$' \t\r\n'
    LL_P=$LL_PROMPT
    while :; do
        LL_P=${LL_P#"${LL_P%%[!$LL_WS]*}"}
        case $LL_P in
        $'\xef\xbb\xbf'*) LL_P=${LL_P:3} ;;
        *) break ;;
        esac
    done
    LL_LOOSE=0
    case $LL_P in '[sc-launch:'*) LL_LOOSE=1 ;; esac
    LL_SESS=$LL_STORE/sessions
    LL_PEND=$LL_STORE/pending
    LL_USABLE=0
    if [ -n "$LL_NONCE" ] && [ -d "$LL_PEND" ] && [ ! -L "$LL_PEND" ] && [ -O "$LL_PEND" ] &&
        [ -f "$LL_PEND/$LL_NONCE" ] && [ ! -L "$LL_PEND/$LL_NONCE" ]; then
        LL_USABLE=1
    fi
    if [ "$LL_GOVERNED" = 1 ]; then
        # B8: already bound; the level never changes, a supplied record is consumed.
        [ "$LL_USABLE" = 1 ] && rm -f -- "$LL_PEND/$LL_NONCE" 2>/dev/null
        # Approval (FR-L-15 to FR-L-17): only at worktree (an invalid word
        # included), never at full or full-submit. The whole prompt trimmed and
        # lower-cased is approved, approved. or approved!; or the first line,
        # leading whitespace removed, starts /sc:implement, /sc:task or /task
        # as a whole word. The [[:space:]] after the command name also matches
        # the newline that ends the first line.
        LL_RE_APR='^[[:space:]]*/(sc:implement|sc:task|task)([[:space:]]|$)'
        LL_APR=0
        if [ "$LL_LEVEL" = W ]; then
            [[ $LL_PROMPT =~ $LL_RE_APR ]] && LL_APR=1
            LL_P=${LL_PROMPT#"${LL_PROMPT%%[![:space:]]*}"}
            LL_P=${LL_P%"${LL_P##*[![:space:]]}"}
            [[ ${LL_P,,} =~ ^approved[.!]?$ ]] && LL_APR=1
        fi
        if [ "$LL_APR" = 1 ]; then
            # No-replace create of a regular file in the owned sessions
            # directory; an existing .ok of any kind is left alone. A failed
            # write still allows the prompt and shows later as LL-IMPL.
            if [ -d "$LL_STORE/sessions" ] && [ ! -L "$LL_STORE/sessions" ] && [ -O "$LL_STORE/sessions" ] &&
                [ ! -e "$LL_FILE.ok" ] && [ ! -L "$LL_FILE.ok" ]; then
                (set -C; : >"$LL_FILE.ok") 2>/dev/null
            fi
        fi
        exit 0 # approval lasts until a person deletes the session's files (O-6)
    fi
    if [ -z "$LL_NONCE" ] && [ "$LL_LOOSE" = 0 ]; then
        exit 0 # B9: unbound, no marker
    fi
    LL_GOVERNED=1 # a launch marker: any failure from here is LL-NOBIND
    [ -n "$LL_SID" ] || ll_deny LL-NOBIND # B7
    mkdir -p -- "$LL_SESS" 2>/dev/null
    if ! { [ -d "$LL_SESS" ] && [ ! -L "$LL_SESS" ] && [ -O "$LL_SESS" ]; }; then
        ll_deny LL-NOBIND
    fi
    LL_TAKE=$LL_SESS/.take-$LL_SID
    if [ "$LL_USABLE" = 1 ] && [ ! -d "$LL_TAKE" ]; then
        mv -- "$LL_PEND/$LL_NONCE" "$LL_TAKE" 2>/dev/null # B11: one rename wins the nonce
    fi
    ll_link_take
    if [ "$LL_LOOSE" = 1 ] && [ ! -e "$LL_SESS/$LL_SID" ] && [ ! -L "$LL_SESS/$LL_SID" ]; then
        ll_publish degraded # B12: missing or used nonce, leading marker
    fi
    # B13: whoever won, a regular binding file now exists or the prompt is blocked.
    if [ -f "$LL_SESS/$LL_SID" ] && [ ! -L "$LL_SESS/$LL_SID" ]; then
        exit 0
    fi
    ll_deny LL-NOBIND
fi

# 6. Fast paths. An unbound valid id allows silently; a missing or invalid id is
# identity loss, a declared fail-open limit (section 3). agent_id is never read
# here and there is no cwd fallback.
if [ "$LL_BRANCH" = tool ]; then
    [ "$LL_GOVERNED" = 1 ] || exit 0 # unbound or identity loss
    [ "$LL_BAD" = 1 ] && ll_deny LL-BROKEN # a nonstring tool field or an embedded NUL

    # 7. The tool fields come from the one jq parse in part 4.
    # 8. Classifiers add classes to LL_CLASSES (section 5.2); none gives NONE.
    LL_CLASSES=' '
    LL_TT= # the text the tamper tokens are looked for in (T or the edit path)
    if [ "$LL_TOOL" = Skill ]; then
        # FR-L-40: first word, lower case, one leading "/", text after the last
        # ":", one leading "sc-", one trailing "-protocol".
        LL_N=
        [[ $LL_SKILL =~ ^[[:space:]]*([^[:space:]]*) ]] && LL_N=${BASH_REMATCH[1]}
        LL_N=${LL_N,,}
        LL_N=${LL_N#/}
        LL_N=${LL_N##*:}
        LL_N=${LL_N#sc-}
        LL_N=${LL_N%-protocol}
        case $LL_N in
        implement | task | improve | cleanup | spawn | build) LL_CLASSES+='IMPL ' ;;
        pr-submit) LL_CLASSES+='SUBMIT ' ;;
        issue) LL_CLASSES+='ESCAPE ' ;;
        '') LL_CLASSES+='SKILL ' ;;
        esac
    elif [ "$LL_TOOL" = Bash ] || [ "$LL_TOOL" = Monitor ]; then
        # FR-L-22 to FR-L-27: cmd is the decoded tool_input.command, kept raw; a
        # Monitor call with only ws has no text and stays NONE. No ${s//...}
        # substitution runs over the text (fact T5); one sed and four tr.
        cmd=$LL_TEXT
        if [ "${#cmd}" -gt 65536 ]; then
            LL_CLASSES+='BIG ' # NM1: bytes under LC_ALL=C; nothing else is checked
        elif [ -n "$cmd" ]; then
            # >>> normalise (NM1a to NM7; the tests run this block on its own)
            # NM1a: a backslash-newline continuation inside a word. The
            # regex sits in a variable: a quoted $'...' after =~ matches literally.
            LL_RE_NM1A=$'[^[:space:]\\\\]\\\\\n'
            [[ $cmd =~ $LL_RE_NM1A ]] && LL_CLASSES+='UNKNOWN '
            # T (NM2, NM3): $ before a quote, quotes and backslashes deleted, "/" runs squeezed; the tamper text.
            T=$(printf '%s\n' "$cmd" | sed -E -e "s/\\\$(['\"])/\\1/g" -e "s/['\"\\\\]//g" -e 's#/+#/#g' -e 's#/(\./)+#/#g' -e 's/`/ $;/g') || ll_deny LL-BROKEN
            # G (NM4): raw cmd then T, lower case, other characters spaces, one space at each end; never split.
            G=" $(printf '%s\n%s\n' "$cmd" "$T" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9._/~$@+:-' ' ') " || ll_deny LL-BROKEN
            # W (NM5, NM6): newline ; & | ( ) made ";", other characters outside the word set made spaces.
            W=$(printf '%s\n' "$T" | tr '\n;&|()' ';;;;;;' | tr -c 'A-Za-z0-9._/=:@+~$;-' ' ') || ll_deny LL-BROKEN
            # segs: the segments of W; a segment's words are ws=($seg) under set -f, and (NM7) a word's basename is ${w##*/}.
            IFS=';' read -r -a segs <<<"$W"
            # <<< normalise
            # Tamper (FR-L-49, FR-L-50) on T and the words; escape (FR-L-47,
            # FR-L-48) on the words of each segment, any position. W has no "_",
            # so install_hooks is looked for in T.
            LL_TT=$T
            case $T in *install_hooks*) LL_CLASSES+='TAMPER ' ;; esac
            LL_CL=0 LL_CF=0 # a claude word; a claude launch flag word (whole command)
            for seg in "${segs[@]}"; do
                ws=($seg)
                LL_SC=0 # a superclaude word earlier in this segment
                for ((i = 0; i < ${#ws[@]}; i++)); do
                    w=${ws[i]}
                    b=${w##*/}
                    case $w in *.claude | *.claude/) LL_CLASSES+='TAMPER ' ;; esac
                    [ "$w" = install ] && [ "$LL_SC" = 1 ] && LL_CLASSES+='TAMPER '
                    case $w in -p | --print | --continue | --resume | --bare | --settings | --dangerously-skip-permissions | --fork-session | --session-id | --permission-mode) LL_CF=1 ;; esac
                    case ${b%%@*} in claude | claude-code) LL_CL=1 ;; esac
                    case $b in
                    superclaude | superclaude.*) LL_SC=1 ;;
                    ccsession* | tmux | screen | xdotool | ydotool) LL_CLASSES+='ESCAPE ' ;;
                    orca)
                        # w1, w2: the next two non-option words; --version counts as w1.
                        LL_W1= LL_W2=
                        for ((j = i + 1; j < ${#ws[@]}; j++)); do
                            case ${ws[j]} in
                            --version) [ -n "$LL_W1" ] || { LL_W1=--version && break; } ;;
                            -*) ;;
                            *)
                                if [ -z "$LL_W1" ]; then
                                    LL_W1=${ws[j]}
                                else
                                    LL_W2=${ws[j]}
                                    break
                                fi ;;
                            esac
                        done
                        case "$LL_W1 $LL_W2" in
                        'status '* | 'help '* | '--version '* | 'worktree current' | 'worktree list' | 'worktree show' | 'terminal list' | 'terminal show' | 'terminal read') ;;
                        'orchestration check' | 'orchestration inbox' | 'orchestration run-current' | 'orchestration task-list' | 'orchestration worker-show') ;;
                        *) case ${ws[${#ws[@]} - 1]} in --help | -h) ;; *) LL_CLASSES+='ESCAPE ' ;; esac ;;
                        esac ;;
                    esac
                done
            done
            [ "$LL_CL$LL_CF" = 11 ] && LL_CLASSES+='ESCAPE '
            # Git (FR-L-28 to FR-L-34) and gh (FR-L-35 to FR-L-39): G1, G2 and
            # H2 test G; G3, G4, H1, H3, H4 and H5 read the words of each
            # segment; then the canonical push check on raw cmd.
            LL_RE='( |/)git(-[a-z][a-z-]*)? '
            LL_GIT=0
            [[ $G =~ $LL_RE ]] && LL_GIT=1
            LL_RE='( |/)gh '
            LL_GH=0
            [[ $G =~ $LL_RE ]] && LL_GH=1
            # H5 can only fire when G (lower case) holds one of these texts.
            LL_URL=0
            case $G in *repos/* | *api.github.com* | *uploads.github.com*) LL_URL=1 ;; esac
            if [ "$LL_GH" = 1 ] && [[ $G == *' api '* ]]; then
                # H2: a gh word and the word api anywhere is GHWRITE unless the
                # raw cmd is one plain GET: the anchored form, no method, field
                # or input word, and an endpoint that is not graphql or a merge.
                LL_RE='^[[:space:]]*gh api( +[A-Za-z0-9._/:=,@%+-]+)+[[:space:]]*$'
                LL_RE_W='^(-[A-Za-z]*[XfF].*|--method.*|--field.*|--raw-field.*|--input.*)$'
                LL_OK=0
                if [[ $cmd =~ $LL_RE ]]; then
                    ws=($cmd) # the form admits no glob, quote or separator
                    LL_OK=1 LL_EP= LL_V=0
                    for ((i = 2; i < ${#ws[@]}; i++)); do
                        w=${ws[i]}
                        if [[ $w =~ $LL_RE_W ]]; then
                            LL_OK=0
                            break
                        fi
                        if [ "$LL_V" = 1 ]; then
                            LL_V=0
                            continue
                        fi
                        case $w in
                        -H | --header | -q | --jq | -t | --template | --hostname | -p | --preview | --cache) LL_V=1 ;;
                        -*) ;;
                        *) [ -n "$LL_EP" ] || LL_EP=$w ;;
                        esac
                    done
                    case ${LL_EP,,} in '' | graphql | */merge | */merges) LL_OK=0 ;; esac
                fi
                [ "$LL_OK" = 1 ] || LL_CLASSES+='GHWRITE '
            fi
            if [ "$LL_GIT" = 1 ]; then
                LL_RE='( |/git-| git-)(merge|pull) '
                [[ $G =~ $LL_RE ]] && LL_CLASSES+='MERGE '
                LL_RE='( |/git-| git-)(push|send-pack|http-push) '
                [[ $G =~ $LL_RE ]] && LL_CLASSES+='PUSH '
                LL_RE='( |/git-| git-)(commit|cherry-pick|am|commit-tree) '
                [[ $G =~ $LL_RE ]] && LL_CLASSES+='COMMIT '
                LL_RE='alias\.|pushurl|insteadof|hookspath| (remote|url|include|includeif)\.| set-url '
                [[ $G =~ $LL_RE ]] && LL_CLASSES+='UNKNOWN '
            fi
            if [ "$LL_GIT$LL_GH$LL_URL" != 000 ]; then
                LL_RE_NAME='^[A-Za-z_][A-Za-z0-9_]*='
                LL_RE_NUM='^[0-9]+(\.[0-9]+)?[smhd]?$'
                LL_RE_DASH='^git-[a-z][a-z-]*$'
                for seg in "${segs[@]}"; do
                    ws=($seg)
                    LL_CP=-1 # index of the command-position word, -1 while skipping
                    LL_SGH=0 LL_H5= # a gh word in this segment; its H5 classes
                    for ((i = 0; i < ${#ws[@]}; i++)); do
                        w=${ws[i]}
                        if [ "$LL_CP" = -1 ]; then
                            case $w in -*) continue ;; esac
                            LL_B=${w##*/} # wrappers and shells match by basename (NM7)
                            case $LL_B in
                            env | sudo | nohup | exec | command | builtin | timeout | xargs | setsid | time | nice | stdbuf | ionice | doas | unbuffer | eval | if | then | else | elif | do | while | until | coproc) continue ;;
                            bash | sh | zsh | dash | ksh)
                                if [[ ${ws[i + 1]:-} =~ ^-[a-z]*c$ ]]; then
                                    i=$((i + 1))
                                    continue
                                fi ;;
                            esac
                            [[ $w =~ $LL_RE_NAME || $w =~ $LL_RE_NUM ]] && continue
                            LL_CP=$i
                        fi
                        if [ "$LL_URL" = 1 ]; then
                            # H5: a merge endpoint or a GitHub API host in any word.
                            LL_LW=${w,,}
                            if [[ $LL_LW == *repos/* && ($LL_LW == */merge || $LL_LW == */merges) ]]; then
                                LL_H5+='MERGE '
                            fi
                            case $LL_LW in *api.github.com* | *uploads.github.com*) LL_H5+='GHWRITE ' ;; esac
                        fi
                        b=${w##*/}
                        if [ "$b" = gh ]; then
                            # H1: group and action, skipping -R and --repo values.
                            LL_SGH=1 LL_GG= LL_GA= LL_HV=0
                            for ((j = i + 1; j < ${#ws[@]}; j++)); do
                                case ${ws[j]} in
                                -R | --repo) j=$((j + 1)) ;;
                                --version | --help) LL_HV=1 ;;
                                -*) ;;
                                *)
                                    if [ -z "$LL_GG" ]; then
                                        LL_GG=${ws[j]}
                                    else
                                        LL_GA=${ws[j]}
                                        break
                                    fi ;;
                                esac
                            done
                            # G4: a repo option that ends the segment has no value.
                            case ${ws[${#ws[@]} - 1]} in -R | --repo) LL_CLASSES+='UNKNOWN ' ;; esac
                            # H3, first match wins (the space cannot occur in a word).
                            case "$LL_GG $LL_GA" in
                            'api '*) ;;
                            ' ') [ "$LL_HV" = 1 ] || [ "$LL_CP" != "$i" ] || LL_CLASSES+='UNKNOWN ' ;;
                            *' merge' | *' update-branch' | *' sync') LL_CLASSES+='MERGE ' ;;
                            'alias '* | 'extension '* | *'$'*) LL_CLASSES+='UNKNOWN ' ;;
                            'search '* | 'status '* | 'auth '* | 'browse '* | 'help '* | 'completion '*) ;;
                            *' view' | *' list' | *' status' | *' diff' | *' checks' | *' watch' | *' checkout') ;;
                            'pr create' | 'pr edit' | 'pr comment' | 'pr ready' | 'issue create' | 'issue edit' | 'issue comment') LL_CLASSES+='SUBMIT ' ;;
                            *) [ "$LL_CP" != "$i" ] || LL_CLASSES+='UNKNOWN ' ;;
                            esac
                            # H4: each pr create needs a nonempty repo operand in its own segment.
                            if [ "$LL_GG $LL_GA" = 'pr create' ]; then
                                LL_RP=0
                                for ((j = 0; j < ${#ws[@]}; j++)); do
                                    case ${ws[j]} in
                                    -R | --repo) [[ -n ${ws[j + 1]:-} && ${ws[j + 1]} != -* ]] && LL_RP=1 ;;
                                    --repo=?*) LL_RP=1 ;;
                                    esac
                                done
                                [ "$LL_RP" = 1 ] || LL_CLASSES+='REPO '
                            fi
                            continue
                        fi
                        case $b in git) ;; git-*) [[ $b =~ $LL_RE_DASH ]] || continue ;; *) continue ;; esac
                        # S: the dashed name, or the first non-option word after git.
                        LL_S= LL_SI=$i LL_HV=0 LL_LV= LL_DG=0
                        if [ "$b" != git ]; then
                            LL_S=${b#git-}
                        else
                            j=$((i + 1))
                            while [ "$j" -lt "${#ws[@]}" ]; do
                                case ${ws[j]} in
                                -C | -c | --git-dir | --work-tree | --namespace | --config-env | --attr-source)
                                    if [ $((j + 1)) -ge "${#ws[@]}" ]; then
                                        LL_DG=1
                                        break
                                    fi
                                    LL_LV=${ws[j + 1]}
                                    j=$((j + 2)) ;;
                                --version | --help | -h) LL_HV=1 j=$((j + 1)) ;;
                                -*) j=$((j + 1)) ;;
                                *) LL_S=${ws[j]} LL_SI=$j; break ;;
                                esac
                            done
                        fi
                        # G4: every git word, in command position or not.
                        if [ "$LL_DG" = 1 ] || [[ $LL_S == *'$'* ]]; then
                            LL_CLASSES+='UNKNOWN '
                        fi
                        [ "$LL_CP" = "$i" ] || continue
                        # G3: the subcommand table, command position only.
                        LL_NX=${ws[LL_SI + 1]:-}
                        case $LL_S in
                        '') [ "$LL_HV" = 1 ] || [ "$LL_LV" = '$' ] || LL_CLASSES+='UNKNOWN ' ;;
                        commit | cherry-pick | revert | am | commit-tree) LL_CLASSES+='COMMIT ' ;;
                        update-ref)
                            for ((j = LL_SI + 1; j < ${#ws[@]}; j++)); do
                                case ${ws[j]} in HEAD | --stdin | refs/heads/*) LL_CLASSES+='COMMIT ' && break ;; esac
                            done ;;
                        merge | pull) LL_CLASSES+='MERGE ' ;;
                        push) LL_CLASSES+='PUSH ' ;;
                        add | apply | bisect | blame | branch | cat-file | check-attr | check-ignore | check-ref-format | checkout | clean | count-objects | describe | diff | diff-files | diff-index | diff-tree | fetch | for-each-ref | format-patch | fsck | gc | grep | hash-object | help | log | ls-files | ls-remote | ls-tree | merge-base | merge-tree | mv | name-rev | range-diff | read-tree | rebase | reflog | reset | restore | rev-list | rev-parse | rm | shortlog | show | show-branch | show-ref | stash | status | switch | tag | var | version | whatchanged | write-tree) ;;
                        remote) case $LL_NX in '' | -v | --verbose | get-url | show) ;; *) LL_CLASSES+='UNKNOWN ' ;; esac ;;
                        config) case $LL_NX in --get | --get-all | --get-regexp | --list | -l | get | list) ;; *) LL_CLASSES+='UNKNOWN ' ;; esac ;;
                        worktree) [ "$LL_NX" = list ] || LL_CLASSES+='UNKNOWN ' ;;
                        *) LL_CLASSES+='UNKNOWN ' ;;
                        esac
                    done
                    [ "$LL_SGH" = 1 ] || LL_CLASSES+=$LL_H5 # H5 only where no gh word is
                done
                # Canonical push (FR-L-33, FR-L-34): only one plain git push to origin passes.
                case $LL_CLASSES in
                *' PUSH '*)
                    LL_RE='^[[:space:]]*git push( (-u|--set-upstream))? origin ([A-Za-z0-9_][A-Za-z0-9._/-]*)(:([A-Za-z0-9_][A-Za-z0-9._/-]*))?[[:space:]]*$'
                    if [[ $cmd =~ $LL_RE ]]; then
                        LL_D=${BASH_REMATCH[5]:-${BASH_REMATCH[3]}}
                        case $LL_D in refs/heads/*) LL_D=${LL_D#refs/heads/} ;; heads/*) LL_D=${LL_D#heads/} ;; esac
                        case $LL_D in master | main) LL_CLASSES+='PROTECTED ' ;; HEAD) LL_CLASSES+='PUSHFORM ' ;; esac
                    else
                        LL_CLASSES+='PUSHFORM '
                    fi ;;
                esac
            fi
        fi
    elif [ "$LL_TOOL" = Edit ] || [ "$LL_TOOL" = Write ] || [ "$LL_TOOL" = NotebookEdit ]; then
        # EPATH: the edit path after the NM3 "/" squeeze, one sed; the tamper check reads it.
        EPATH=
        if [ -n "$LL_PATH" ]; then
            EPATH=$(printf '%s\n' "$LL_PATH" | sed -E -e 's#/+#/#g' -e 's#/(\./)+#/#g') || ll_deny LL-BROKEN
        fi
        # FR-L-42, FR-L-51: the tamper check only; contents are never read.
        LL_TT=$EPATH
        case $EPATH in */../* | */..) LL_CLASSES+='TAMPER ' ;; esac
    elif [ "$LL_TOOL" = Agent ] || [ "$LL_TOOL" = Task ]; then
        # FR-L-41, FR-L-46: local or background is NONE; the prompt is never scanned.
        [ "$LL_ISO" = remote ] && LL_CLASSES+='ESCAPE '
    elif [[ $LL_TOOL =~ ^(Cron|Schedule)[A-Za-z]*$ ]]; then
        LL_CLASSES+='TURN ' # FR-L-43
    elif [ "$LL_TOOL" = RemoteTrigger ] || [ "$LL_TOOL" = Workflow ] || [ "$LL_TOOL" = SendMessage ]; then
        LL_CLASSES+='ESCAPE ' # FR-L-46
    elif [[ $LL_TOOL == mcp__* ]]; then
        # FR-L-45: N is the text after the last "__", lower case.
        LL_N=${LL_TOOL##*__}
        LL_N=${LL_N,,}
        case $LL_N in
        *merge* | *push* | *commit* | *pull_request* | *create_or_update_file* | *delete_file* | *update_ref* | *create_ref* | *create_branch*)
            case $LL_N in
            list_* | get_* | search_* | read_*) ;;
            *merge*) LL_CLASSES+='MERGE ' ;;
            *) LL_CLASSES+='MCP ' ;;
            esac ;;
        esac
    else
        : # FR-L-66: any other tool the matcher let through is NONE.
    fi
    # FR-L-49: the tamper tokens in T or the edit path; the store part is
    # built from LL_S1 and LL_S2, so this text never names it joined.
    case $LL_TT in
    *"$LL_S1/$LL_S2"* | *.claude/settings* | *.claude/hooks* | *disableAllHooks* | *.gitconfig* | *.git/config* | *.config/git*) LL_CLASSES+='TAMPER ' ;;
    esac
    # LL-TEXT: every class of a Bash or Monitor call came from its text.
    if [ "$LL_TOOL" = Bash ] || [ "$LL_TOOL" = Monitor ]; then
        LL_NOTE_TEXT=1
    fi

    # 9. One case on CLASS:LEVEL, taken in message precedence; any blocked class
    # blocks the call with the first blocked class's message.
    for LL_C in BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL; do
        case $LL_CLASSES in *" $LL_C "*) ;; *) continue ;; esac
        case $LL_C:$LL_LEVEL in
        IMPL:WA | IMPL:F | IMPL:FS | TURN:WA | TURN:F | TURN:FS) ;;
        SUBMIT:FS | COMMIT:FS | PUSH:FS | SKILL:FS) ;;
        IMPL:W | TURN:W) ll_deny "LL-$LL_C" ;;
        SUBMIT:W | SUBMIT:WA | SUBMIT:F | COMMIT:W | COMMIT:WA | COMMIT:F) ll_deny "LL-$LL_C" ;;
        PUSH:W | PUSH:WA | PUSH:F | SKILL:W | SKILL:WA | SKILL:F) ll_deny "LL-$LL_C" ;;
        REPO:W | REPO:WA | REPO:F | REPO:FS) ll_deny LL-REPO ;;
        PUSHFORM:W | PUSHFORM:WA | PUSHFORM:F | PUSHFORM:FS) ll_deny LL-PUSH-FORM ;;
        PROTECTED:W | PROTECTED:WA | PROTECTED:F | PROTECTED:FS) ll_deny LL-PROTECTED ;;
        MERGE:W | MERGE:WA | MERGE:F | MERGE:FS) ll_deny LL-MERGE ;;
        GHWRITE:W | GHWRITE:WA | GHWRITE:F | GHWRITE:FS) ll_deny LL-GH-WRITE ;;
        UNKNOWN:W | UNKNOWN:WA | UNKNOWN:F | UNKNOWN:FS) ll_deny LL-UNKNOWN ;;
        MCP:W | MCP:WA | MCP:F | MCP:FS) ll_deny LL-MCP ;;
        ESCAPE:W | ESCAPE:WA | ESCAPE:F | ESCAPE:FS) ll_deny LL-ESCAPE ;;
        TAMPER:W | TAMPER:WA | TAMPER:F | TAMPER:FS) ll_deny LL-TAMPER ;;
        BIG:W | BIG:WA | BIG:F | BIG:FS) ll_deny LL-BIG ;;
        *) ll_deny LL-BROKEN ;;
        esac
    done
    exit 0
fi

# 10. Default deny
ll_deny LL-BROKEN
