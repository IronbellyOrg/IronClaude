#!/usr/bin/env bash
#
# collect-conflict-evidence.sh — Tier 2 evidence collector for sc:pr-submit conflict
# cycles (issue #305).
#
# Purpose : For one conflicted path of an in-progress merge of the recorded base tip,
#           write the evidence the session reads before it resolves the path by
#           intent: the three stage blobs, the work-tree file with its conflict
#           markers, the left-right log of the merge and both merge-base diffs.
#           Tier 2 only; never run for Tier 0 or Tier 1. It is read-only toward the
#           repository: it never changes the index, the work tree, HEAD, any ref or
#           stored configuration. It writes only into --out (which must be missing or
#           empty) and into a temporary directory under the git directory that is
#           removed on exit.
# Usage   : collect-conflict-evidence.sh --path <p> --out <dir> --base-sha <40hex>
#                                        --merge-base <40hex> [--max-bytes 204800]
#           <p> is relative to the top of the work tree.
# Output  : exactly one stdout line. Success is one JSON object:
#           {"dir":"<out>","files":["stage1",..],"missing":["stage3"],"truncated":false}
#           Files, in this order when present: stage1, stage2, stage3, worktree,
#           log.txt, diff-ours.txt, diff-theirs.txt. A stage the index does not list
#           for <p> is not written and is named in "missing". Each file is cut at
#           --max-bytes, with a last line "[sc:pr-submit: truncated at <N> bytes]".
#           Failure is the token "EVIDENCE_FAIL <reason>"; details go to stderr.
# Exit    : 0 on success; 2 with EVIDENCE_FAIL usage | foreign_merge | out_not_empty |
#           unreadable | timeout. The whole run is bounded to 60 seconds.
# Contract: design section 7.3. No stdin read, no prompt. Any EVIDENCE_FAIL escalates
#           the cycle to Tier 3.

set -u -o pipefail

LIMIT_SECONDS=60
DEADLINE=$((SECONDS + LIMIT_SECONDS))
TMP=""

# shellcheck disable=SC2329  # invoked by the EXIT trap below
cleanup() {
    if [ -n "$TMP" ] && [ -d "$TMP" ]; then
        rm -rf -- "$TMP"
        rmdir -- "$(dirname -- "$TMP")" 2>/dev/null || true
    fi
}
trap cleanup EXIT

# Keep the caller's stdout and stderr on fds 3 and 4, so a failure raised while a
# command's output is redirected into a capture file still reaches the caller.
exec 3>&1 4>&2

fail() {
    # fail <reason> <detail>
    printf 'collect-conflict-evidence: %s\n' "$2" >&4
    printf 'EVIDENCE_FAIL %s\n' "$1" >&3
    exit 2
}

is_sha() {
    case "$1" in
        *[!0-9a-fA-F]*) return 1 ;;
    esac
    [ "${#1}" -eq 40 ]
}

lower() {
    printf '%s' "$1" | tr 'A-F' 'a-f'
}

# check_deadline : fail with "timeout" once the 60-second budget is spent.
check_deadline() {
    [ "$SECONDS" -lt "$DEADLINE" ] || fail timeout "the evidence run exceeded ${LIMIT_SECONDS} seconds"
}

# bounded <command>... : run one command within the remaining budget, under `timeout`
# when it is on PATH, else as a background job this shell polls and stops at the
# deadline. Returns the command's exit status; running past the budget fails timeout.
bounded() {
    local remaining rc pid
    # Computed once: a budget that reaches 0 between a check and its use would make
    # `timeout 0` run the command with no limit.
    remaining=$((DEADLINE - SECONDS))
    [ "$remaining" -gt 0 ] || fail timeout "the evidence run exceeded ${LIMIT_SECONDS} seconds"
    if command -v timeout >/dev/null 2>&1; then
        timeout "$remaining" "$@"
        rc=$?
        [ "$rc" -ne 124 ] || fail timeout "'$*' did not finish within the ${LIMIT_SECONDS}-second budget"
    else
        # The job keeps the caller's redirections but not fds 3 and 4, so a child that
        # outlives it cannot hold the caller's stdout or stderr open.
        "$@" 3>&- 4>&- &
        pid=$!
        while kill -0 "$pid" 2>/dev/null; do
            if [ "$SECONDS" -ge "$DEADLINE" ]; then
                kill "$pid" 2>/dev/null
                sleep 1
                if kill -0 "$pid" 2>/dev/null; then
                    kill -s KILL "$pid" 2>/dev/null
                fi
                wait "$pid" 2>/dev/null
                fail timeout "'$*' did not finish within the ${LIMIT_SECONDS}-second budget"
            fi
            sleep 0.2 2>/dev/null || sleep 1
        done
        wait "$pid"
        rc=$?
    fi
    check_deadline
    return "$rc"
}

# Step 0: arguments.
P=""
OUT=""
BASE_SHA=""
MERGE_BASE=""
MAX_BYTES=204800
while [ $# -gt 0 ]; do
    case "$1" in
        --path|--out|--base-sha|--merge-base|--max-bytes)
            [ $# -ge 2 ] || fail usage "missing value for $1"
            case "$1" in
                --path) P="$2" ;;
                --out) OUT="$2" ;;
                --base-sha) BASE_SHA="$2" ;;
                --merge-base) MERGE_BASE="$2" ;;
                --max-bytes) MAX_BYTES="$2" ;;
            esac
            shift 2
            ;;
        *) fail usage "unknown argument: $1" ;;
    esac
done
[ -n "$P" ] || fail usage "missing required --path <p>"
[ -n "$OUT" ] || fail usage "missing required --out <dir>"
[ -n "$BASE_SHA" ] || fail usage "missing required --base-sha <40hex>"
[ -n "$MERGE_BASE" ] || fail usage "missing required --merge-base <40hex>"
is_sha "$BASE_SHA" || fail usage "--base-sha is not a 40-hex commit id: $BASE_SHA"
is_sha "$MERGE_BASE" || fail usage "--merge-base is not a 40-hex commit id: $MERGE_BASE"
case "$MAX_BYTES" in
    ''|*[!0-9]*|0*) fail usage "--max-bytes is not a positive integer: $MAX_BYTES" ;;
esac
NL="$(printf '\nx')"
NL="${NL%x}"
# The path is repository-relative and canonical: no absolute path, no empty, "." or
# ".." segment, no trailing slash, no newline.
case "$P" in
    /*|./*|../*|*/./*|*/../*|*/.|*/..|.|..|*//*|*/|*"$NL"*)
        fail usage "--path must be a canonical repository-relative path: $P" ;;
esac
command -v jq >/dev/null 2>&1 || fail usage "jq not found on PATH"
BASE_SHA="$(lower "$BASE_SHA")"
MERGE_BASE="$(lower "$MERGE_BASE")"

# --out is resolved against the caller's directory before the directory changes.
case "$OUT" in /*) OUT_ABS="$OUT" ;; *) OUT_ABS="$PWD/$OUT" ;; esac
TOPLEVEL="$(git rev-parse --show-toplevel 2>/dev/null)" || TOPLEVEL=""
[ -n "$TOPLEVEL" ] || fail usage "not inside a git work tree"
cd -- "$TOPLEVEL" || fail usage "cannot enter $TOPLEVEL"
git rev-parse -q --verify "${MERGE_BASE}^{commit}" >/dev/null 2>&1 \
    || fail usage "--merge-base does not name a commit: $MERGE_BASE"

# Step 1: a merge of exactly the given base tip is in progress.
MERGE_HEAD_SHA="$(git rev-parse -q --verify MERGE_HEAD 2>/dev/null)" || MERGE_HEAD_SHA=""
[ -n "$MERGE_HEAD_SHA" ] || fail foreign_merge "no merge in progress (MERGE_HEAD is missing)"
[ "$(lower "$MERGE_HEAD_SHA")" = "$BASE_SHA" ] \
    || fail foreign_merge "MERGE_HEAD is $MERGE_HEAD_SHA, not the recorded base tip $BASE_SHA"

# Step 2: --out is missing or an empty directory; nothing is written otherwise.
if [ -e "$OUT_ABS" ] || [ -L "$OUT_ABS" ]; then
    [ -d "$OUT_ABS" ] || fail out_not_empty "--out exists and is not a directory: $OUT"
    [ -z "$(ls -A -- "$OUT_ABS" 2>/dev/null)" ] || fail out_not_empty "--out is not empty: $OUT"
fi
mkdir -p -- "$OUT_ABS" 2>/dev/null || fail usage "cannot create --out: $OUT"

# Temporary files live only under the repository's git directory.
TMP_ROOT="$(git rev-parse --git-path sc-pr-submit-tmp 2>/dev/null)" || TMP_ROOT=""
[ -n "$TMP_ROOT" ] || fail usage "cannot resolve the git directory for temporary files"
mkdir -p -- "$TMP_ROOT" 2>/dev/null || fail usage "cannot create $TMP_ROOT"
TMP="$(mktemp -d "$TMP_ROOT/evidence.XXXXXXXX" 2>/dev/null)" || { TMP=""; fail usage "cannot create a temporary directory under $TMP_ROOT"; }

FILES=()
TRUNCATED=false

# place <name> : copy $TMP/raw to --out/<name>, cut at MAX_BYTES with the marker line.
place() {
    local name="$1" size dest="$OUT_ABS/$1"
    size="$(wc -c <"$TMP/raw")" || fail unreadable "cannot size the evidence for $name"
    if [ "$size" -gt "$MAX_BYTES" ]; then
        head -c "$MAX_BYTES" <"$TMP/raw" >"$dest" || fail unreadable "cannot write $dest"
        if [ -n "$(tail -c 1 <"$dest")" ]; then
            printf '\n' >>"$dest" || fail unreadable "cannot write $dest"
        fi
        printf '[sc:pr-submit: truncated at %s bytes]\n' "$MAX_BYTES" >>"$dest" \
            || fail unreadable "cannot write $dest"
        TRUNCATED=true
    else
        cat -- "$TMP/raw" >"$dest" || fail unreadable "cannot write $dest"
    fi
    FILES+=("$name")
}

# capture <name> <command>... : run a bounded read into $TMP/raw, then place it.
capture() {
    local name="$1"
    shift
    if ! bounded "$@" >"$TMP/raw" 2>"$TMP/err"; then
        cat -- "$TMP/err" >&2
        fail unreadable "cannot read the evidence for $name"
    fi
    place "$name"
}

# Step 3a: the stages the index lists for exactly this path.
if ! bounded git --no-optional-locks --literal-pathspecs ls-files -u -z -- "$P" \
        >"$TMP/stages" 2>"$TMP/err"; then
    cat -- "$TMP/err" >&2
    fail unreadable "cannot list the unmerged stages of $P"
fi
TAB="$(printf '\t')"
HAVE=(0 0 0 0)  # HAVE[n] is 1 when the index lists stage n for the path
while IFS= read -r -d '' record; do
    meta="${record%%"$TAB"*}"
    [ "${record#*"$TAB"}" = "$P" ] || continue
    case "${meta##* }" in
        1) HAVE[1]=1 ;;
        2) HAVE[2]=1 ;;
        3) HAVE[3]=1 ;;
    esac
done <"$TMP/stages"
MISSING=()
for n in 1 2 3; do
    if [ "${HAVE[$n]}" -eq 1 ]; then
        capture "stage$n" git --no-optional-locks show --no-textconv ":$n:$P"
    else
        MISSING+=("stage$n")
    fi
done

# Step 3b: the work-tree file with its conflict markers (a regular, readable file).
WORKTREE_FILE="$TOPLEVEL/$P"
if [ -L "$WORKTREE_FILE" ] || [ ! -f "$WORKTREE_FILE" ] || [ ! -r "$WORKTREE_FILE" ]; then
    fail unreadable "the work-tree file is missing, not a regular file or not readable: $P"
fi
capture worktree cat -- "$WORKTREE_FILE"

# Step 3c: the left-right log of the merge, then both merge-base diffs.
capture log.txt git --no-optional-locks --literal-pathspecs log --no-color \
    --oneline --left-right --merge -- "$P"
capture diff-ours.txt git --no-optional-locks --literal-pathspecs diff --no-color \
    --no-ext-diff --no-textconv --no-renames "$MERGE_BASE" HEAD -- "$P"
capture diff-theirs.txt git --no-optional-locks --literal-pathspecs diff --no-color \
    --no-ext-diff --no-textconv --no-renames "$MERGE_BASE" "$BASE_SHA" -- "$P"
check_deadline

# Step 5.
to_json_list() {
    printf '%s\n' "$@" | jq -Rsc 'split("\n") | map(select(. != ""))'
}
FILES_JSON="$(to_json_list ${FILES[@]+"${FILES[@]}"})" || fail usage "could not render the file list"
MISSING_JSON="$(to_json_list ${MISSING[@]+"${MISSING[@]}"})" || fail usage "could not render the missing list"
jq -nc --arg dir "$OUT" --argjson files "$FILES_JSON" --argjson missing "$MISSING_JSON" \
    --argjson truncated "$TRUNCATED" \
    '{dir: $dir, files: $files, missing: $missing, truncated: $truncated}' \
    || fail usage "could not render the evidence JSON"
exit 0
