#!/bin/bash -p
# launch-level-pre-push-version: 1
# Launch-level L2 git pre-push hook, IronbellyOrg/IronClaude issue #441.
# Installed by the claim as <git-common-dir>/hooks/pre-push next to its data
# file pre-push.launch-level (line 1: pinned HOME, line 2: pinned uv directory).
# The actor is decided first by the launch-job identity selector; an ordinary
# push exits 0 at once and silently, without reading stdin. A governed push to
# refs/heads/main or refs/heads/master is refused; an unknown actor is refused
# only for those two refs. Exit 0 allows, 1 refuses, 2 refuses a malformed
# stream. Arguments are ignored; no file is written and git is never called.
# -p: bash ignores BASH_ENV, ENV, SHELLOPTS and imported functions. Linux only.

LC_ALL=C
export LC_ALL
set -f

L2_PROTECTED=(refs/heads/main refs/heads/master)
L2_HOOKS=${0%/*}
L2_DATA=$L2_HOOKS/pre-push.launch-level
L2_HOME=
L2_UVDIR=
L2_ACTOR=unknown
L2_WHY=
L2_RECORD=
L2_REASON=

# FR-020: two absolute paths, each newline-terminated, in an owned regular file
# that is neither group- nor other-writable. Sets L2_HOME and L2_UVDIR.
l2_data() {
    local meta content line1 line2
    [[ -f $L2_DATA && ! -L $L2_DATA && -O $L2_DATA ]] || return 1
    # shortcut: bash has no builtin for mode bits, so /usr/bin/stat reads them.
    meta=$(/usr/bin/stat -c '%a %s' -- "$L2_DATA" </dev/null 2>/dev/null) || return 1
    [[ $meta =~ ^([0-7]{3,4})\ ([0-9]{1,5})$ ]] || return 1
    (( (8#${BASH_REMATCH[1]} & 8#022) == 0 && BASH_REMATCH[2] <= 8194 )) || return 1
    # read -d '' returns 0 only when it meets a NUL byte, which is invalid here.
    content=
    IFS= read -r -d '' content <"$L2_DATA" && return 1
    line1=${content%%$'\n'*}
    line2=${content#*$'\n'}
    line2=${line2%%$'\n'*}
    [[ $content == "$line1"$'\n'"$line2"$'\n' ]] || return 1
    [[ $line1 == /* && $line2 == /* ]] || return 1
    L2_HOME=$line1
    L2_UVDIR=$line2
    return 0
}

# FR-021/FR-022: run the selector once with a cleared environment and map its
# single output line to governed, ordinary or unknown (with a why).
l2_actor() {
    local script out rc
    L2_ACTOR=unknown
    if ! l2_data; then
        L2_WHY='no valid data file'
        return
    fi
    script=$L2_HOME/.claude/hooks/launch-job-identity.sh
    if [[ ! -f $script || ! -x $script ]]; then
        L2_WHY='identity script missing'
        return
    fi
    # The trailing '.' keeps the selector's own newlines countable.
    out=$( ( cd / && exec /usr/bin/env -i HOME="$L2_HOME" PATH="$L2_UVDIR:/usr/bin:/bin" UV_NO_CONFIG=1 /usr/bin/timeout 10 "$script" identify "$$" ) </dev/null 2>/dev/null
        rc=$?
        printf '.'
        exit "$rc" )
    rc=$?
    if (( rc == 124 )); then
        L2_WHY='identity check timed out'
        return
    fi
    if (( rc != 0 )); then
        L2_WHY='identity check failed'
        return
    fi
    L2_WHY='identity unknown'
    [[ $out == *$'\n.' ]] || return
    out=${out%$'\n.'}
    [[ $out != *$'\n'* ]] || return
    local s1='^\{"status": "ordinary"\}$'
    local s2='^\{"status": "ordinary", "reason": "released"\}$'
    local s3='^\{"status": "governed", "session_id": "[A-Za-z0-9][A-Za-z0-9_-]{0,127}"\}$'
    local s4='^\{"status": "unknown"\}$'
    # A path with a quote, backslash or control byte cannot be shown safely, so
    # it falls to the plain unknown why.
    local s5='^\{"status": "unknown", "reason": "(stale|orphaned|foreign|unreadable)", "record": "(/[^"'"'"'\\[:cntrl:]]*)"\}$'
    if [[ $out =~ $s1 || $out =~ $s2 ]]; then
        L2_ACTOR=ordinary
    elif [[ $out =~ $s3 ]]; then
        L2_ACTOR=governed
    elif [[ $out =~ $s4 ]]; then
        L2_WHY='identity unknown'
    elif [[ $out =~ $s5 ]]; then
        L2_REASON=${BASH_REMATCH[1]}
        L2_RECORD=${BASH_REMATCH[2]}
        L2_WHY="job record $L2_REASON at $L2_RECORD"
    fi
    # Every other line stays unknown with why 'identity unknown'.
}

# FR-004: split one record from the right; field 1 keeps its spaces.
l2_split() {
    local rest=$1
    [[ $rest == *' '*' '*' '* ]] || return 1
    F4=${rest##* }
    rest=${rest% *}
    F3=${rest##* }
    rest=${rest% *}
    F2=${rest##* }
    F1=${rest% *}
    return 0
}

# FR-006: set L2_CHECK to the name of the first failed check, or leave it empty.
# $1 is the record, $2 is 1 when the record contained a NUL byte.
l2_check() {
    local oid='^([0-9a-f]{40}|[0-9a-f]{64})$'
    local ref='^refs/[^/]+/.'
    L2_CHECK=
    if [[ -z $1 && $2 != 1 ]]; then
        L2_CHECK='blank line'
    elif [[ $2 == 1 || $1 == *[$'\t\r']* ]]; then
        L2_CHECK='tab, CR or NUL'
    elif ! l2_split "$1"; then
        L2_CHECK='fewer than three spaces'
    elif [[ -z $F1 || -z $F2 || -z $F3 || -z $F4 ]]; then
        L2_CHECK='empty field'
    elif [[ ! $F2 =~ $oid || ! $F4 =~ $oid ]]; then
        L2_CHECK='object id is not 40 or 64 lowercase hex'
    elif (( ${#F2} != ${#F4} )); then
        L2_CHECK='object ids differ in length'
    elif [[ ! $F3 =~ $ref || $F3 =~ [[:space:][:cntrl:]] ]]; then
        L2_CHECK='destination is not a refs/ name'
    fi
}

L2_N=0
L2_BAD_N=
L2_BAD_CHECK=
L2_HIT=

# One record: count it, keep the first malformed one, else the first protected.
l2_record() {
    local p
    L2_N=$((L2_N + 1))
    [[ -z $L2_BAD_N ]] || return
    l2_check "$1" "$2"
    if [[ -n $L2_CHECK ]]; then
        L2_BAD_N=$L2_N
        L2_BAD_CHECK=$L2_CHECK
        return
    fi
    [[ -z $L2_HIT ]] || return
    for p in "${L2_PROTECTED[@]}"; do
        if [[ $F3 == "$p" ]]; then
            L2_HIT=$p
            return
        fi
    done
}

# NFR-010: read stdin to EOF in 4096-byte chunks; read -d '' stops at a NUL, so
# a short chunk with status 0 marks a NUL in the current record. Only the
# unfinished record is kept between chunks.
l2_read() {
    local chunk rc pending= nul=0
    while :; do
        chunk=
        IFS= read -r -d '' -n 4096 chunk
        rc=$?
        pending+=$chunk
        while [[ $pending == *$'\n'* ]]; do
            l2_record "${pending%%$'\n'*}" "$nul"
            pending=${pending#*$'\n'}
            nul=0
        done
        (( rc == 0 && ${#chunk} < 4096 )) && nul=1
        if (( rc != 0 )); then
            [[ -z $pending && $nul == 0 ]] || l2_record "$pending" "$nul"
            return
        fi
    done
}

l2_actor
[[ $L2_ACTOR != ordinary ]] || exit 0
l2_read

L2_P='launch-level pre-push:'
if [[ -n $L2_BAD_N ]]; then
    printf '%s\n' "$L2_P L2-MALFORMED: git sent pre-push record $L2_BAD_N that this hook cannot read ($L2_BAD_CHECK); the whole push was refused." >&2
    exit 2
fi
[[ -n $L2_HIT ]] || exit 0
if [[ $L2_ACTOR == governed ]]; then
    printf '%s\n' "$L2_P L2-PROTECTED: a governed launch session may not push to $L2_HIT; the whole push was refused. A person releases the session as the claim's launch result describes." >&2
    exit 1
fi
L2_ROUTE="$L2_P to push there, a person fixes the cause (check $L2_DATA and ~/.claude/hooks/launch-job-identity.sh) or releases the session by deleting its level record."
if [[ $L2_REASON == stale ]]; then
    L2_ROUTE+=" For this job record: no launch job owns this session any more; a person removes the record with: rm '$L2_RECORD'"
elif [[ -n $L2_REASON ]]; then
    L2_ROUTE+=" The job record is kept as evidence and must not be deleted while that launch job's processes run."
fi
printf '%s\n%s\n' "$L2_P L2-UNKNOWN: could not classify this push ($L2_WHY) and it targets $L2_HIT; the whole push was refused, and pushes to other refs are allowed." "$L2_ROUTE" >&2
exit 1
