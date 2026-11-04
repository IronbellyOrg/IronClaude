#!/usr/bin/env bash
#
# finish-merge.sh — finish gate for sc:pr-submit conflict cycles (issue #305).
#
# Purpose : Prove that an in-progress merge of the recorded base tip is safe to
#           conclude, then conclude it with exactly one commit from the given
#           message file (hooks on).
#           Precheck mode (run right before a regenerate) only checks and never
#           commits. This is the only conflict script that changes the repository,
#           and only through that one commit. It never publishes anything, never
#           sets work aside, never rewrites an existing commit, never skips hooks
#           and never writes stored configuration.
# Usage   : finish-merge.sh --base-sha <40hex> --precheck
#           finish-merge.sh --base-sha <40hex> --merge-tree-oid <40hex> \
#                           --manifest <file> --message-file <file>
#           The manifest is the finish_manifest text: one "<stage-1 oid or ->\t<path>"
#           line per resolved path. Precheck mode accepts none of --merge-tree-oid,
#           --manifest or --message-file; commit mode requires all three.
# Output  : exactly one stdout line. Success is one JSON object:
#           precheck mode {"precheck":"ok"}
#           commit mode   {"merge_sha":"<40hex>","parents":["<old HEAD>","<base-sha>"]}
#           Failure is the token "FINISH_FAIL <reason>"; details (and git's own
#           output, verbatim, when the commit is rejected) go to stderr.
# Exit    : 0 on success; 2 with FINISH_FAIL usage | no_merge_head | foreign_merge |
#           unmerged | tree_dirty | markers | staged_unexpected | hook_rejected |
#           parents_mismatch.
# Contract: design section 7.2. No stdin read, no prompt.

set -u -o pipefail

TMP=""

# shellcheck disable=SC2329  # invoked by the EXIT trap below
cleanup() {
    if [ -n "$TMP" ] && [ -d "$TMP" ]; then
        rm -rf -- "$TMP"
        rmdir -- "$(dirname -- "$TMP")" 2>/dev/null || true
    fi
}
trap cleanup EXIT

fail() {
    # fail <reason> <detail>
    printf 'finish-merge: %s\n' "$2" >&2
    printf 'FINISH_FAIL %s\n' "$1"
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

# in_list <needle> <item>... : exact membership.
in_list() {
    local needle="$1" item
    shift
    for item in "$@"; do
        [ "$item" = "$needle" ] && return 0
    done
    return 1
}

# Step 0: arguments.
BASE_SHA=""
MT_OID=""
MANIFEST=""
MESSAGE_FILE=""
PRECHECK=0
COMMIT_OPTS=0
while [ $# -gt 0 ]; do
    case "$1" in
        --base-sha|--merge-tree-oid|--manifest|--message-file)
            [ $# -ge 2 ] || fail usage "missing value for $1"
            case "$1" in
                --base-sha) BASE_SHA="$2" ;;
                --merge-tree-oid) MT_OID="$2"; COMMIT_OPTS=1 ;;
                --manifest) MANIFEST="$2"; COMMIT_OPTS=1 ;;
                --message-file) MESSAGE_FILE="$2"; COMMIT_OPTS=1 ;;
            esac
            shift 2
            ;;
        --precheck) PRECHECK=1; shift ;;
        *) fail usage "unknown argument: $1" ;;
    esac
done
[ -n "$BASE_SHA" ] || fail usage "missing required --base-sha <40hex>"
is_sha "$BASE_SHA" || fail usage "--base-sha is not a 40-hex commit id: $BASE_SHA"
if [ "$PRECHECK" -eq 1 ]; then
    [ "$COMMIT_OPTS" -eq 0 ] \
        || fail usage "--precheck takes only --base-sha (no --merge-tree-oid, --manifest or --message-file)"
else
    [ -n "$MT_OID" ] && [ -n "$MANIFEST" ] && [ -n "$MESSAGE_FILE" ] \
        || fail usage "commit mode requires --merge-tree-oid, --manifest and --message-file"
    is_sha "$MT_OID" || fail usage "--merge-tree-oid is not a 40-hex object id: $MT_OID"
    [ -f "$MANIFEST" ] && [ -r "$MANIFEST" ] || fail usage "manifest not readable: $MANIFEST"
    [ -f "$MESSAGE_FILE" ] && [ -r "$MESSAGE_FILE" ] || fail usage "message file not readable: $MESSAGE_FILE"
fi
command -v jq >/dev/null 2>&1 || fail usage "jq not found on PATH"

# Work from the top of the work tree so every path below is repository-relative.
# The manifest and message paths are resolved before the directory changes.
if [ "$PRECHECK" -eq 0 ]; then
    case "$MANIFEST" in /*) ;; *) MANIFEST="$PWD/$MANIFEST" ;; esac
    case "$MESSAGE_FILE" in /*) ;; *) MESSAGE_FILE="$PWD/$MESSAGE_FILE" ;; esac
fi
TOPLEVEL="$(git rev-parse --show-toplevel 2>/dev/null)" || TOPLEVEL=""
[ -n "$TOPLEVEL" ] || fail usage "not inside a git work tree"
cd -- "$TOPLEVEL" || fail usage "cannot enter $TOPLEVEL"

# Temporary files live only under the repository's git directory.
TMP_ROOT="$(git rev-parse --git-path sc-pr-submit-tmp 2>/dev/null)" || TMP_ROOT=""
[ -n "$TMP_ROOT" ] || fail usage "cannot resolve the git directory for temporary files"
mkdir -p -- "$TMP_ROOT" 2>/dev/null || fail usage "cannot create $TMP_ROOT"
TMP="$(mktemp -d "$TMP_ROOT/finish.XXXXXXXX" 2>/dev/null)" || { TMP=""; fail usage "cannot create a temporary directory under $TMP_ROOT"; }

# read_nul_list <file> : fill LIST with the NUL-separated entries of <file>.
LIST=()
read_nul_list() {
    LIST=()
    local item
    while IFS= read -r -d '' item; do
        LIST+=("$item")
    done <"$1"
}

# Step 1 (both modes): a merge of exactly the given base tip is in progress.
check_merge_head() {
    local merge_head
    merge_head="$(git rev-parse -q --verify MERGE_HEAD 2>/dev/null)" || merge_head=""
    [ -n "$merge_head" ] || fail no_merge_head "no merge in progress (MERGE_HEAD is missing)"
    [ "$(lower "$merge_head")" = "$(lower "$BASE_SHA")" ] \
        || fail foreign_merge "MERGE_HEAD is $merge_head, not the recorded base tip $BASE_SHA"
}

check_merge_head

if [ "$PRECHECK" -eq 1 ]; then
    # Precheck step 2: the work tree differs from the index only at unmerged paths.
    git diff --name-only --no-renames -z >"$TMP/worktree" 2>"$TMP/err" \
        || { cat -- "$TMP/err" >&2; fail tree_dirty "git diff of the work tree failed"; }
    git diff --name-only --diff-filter=U -z >"$TMP/unmerged" 2>"$TMP/err" \
        || { cat -- "$TMP/err" >&2; fail tree_dirty "git diff of the unmerged paths failed"; }
    read_nul_list "$TMP/unmerged"
    UNMERGED=(${LIST[@]+"${LIST[@]}"})
    read_nul_list "$TMP/worktree"
    for path in ${LIST[@]+"${LIST[@]}"}; do
        in_list "$path" ${UNMERGED[@]+"${UNMERGED[@]}"} \
            || fail tree_dirty "tracked file changed outside the conflict set: $path"
    done
    # Precheck step 3.
    jq -nc '{precheck: "ok"}' || fail usage "could not render the precheck JSON"
    exit 0
fi

# Commit mode. The merge-tree object must be a tree; the manifest must parse.
git rev-parse -q --verify "${MT_OID}^{tree}" >/dev/null 2>&1 \
    || fail usage "--merge-tree-oid does not name a tree: $MT_OID"
M_OIDS=()
M_PATHS=()
LINE_NO=0
TAB="$(printf '\t')"
while IFS= read -r line || [ -n "$line" ]; do
    LINE_NO=$((LINE_NO + 1))
    case "$line" in
        *"$TAB"*) ;;
        *) fail usage "manifest line $LINE_NO has no tab" ;;
    esac
    oid="${line%%"$TAB"*}"
    path="${line#*"$TAB"}"
    [ "$oid" = "-" ] || is_sha "$oid" || fail usage "manifest line $LINE_NO: bad stage-1 oid '$oid'"
    [ -n "$path" ] || fail usage "manifest line $LINE_NO: empty path"
    if in_list "$path" ${M_PATHS[@]+"${M_PATHS[@]}"}; then
        fail usage "manifest names $path twice"
    fi
    M_OIDS+=("$oid")
    M_PATHS+=("$path")
done <"$MANIFEST"

OLD_HEAD="$(git rev-parse -q --verify 'HEAD^{commit}' 2>/dev/null)" || fail usage "HEAD does not name a commit"

# Step 2: nothing left unmerged.
git diff --name-only --diff-filter=U -z >"$TMP/unmerged" 2>"$TMP/err" \
    || { cat -- "$TMP/err" >&2; fail unmerged "git diff of the unmerged paths failed"; }
if [ -s "$TMP/unmerged" ]; then
    read_nul_list "$TMP/unmerged"
    fail unmerged "unmerged paths remain: ${LIST[*]}"
fi

# Step 3: no unstaged change to a tracked file (the index equals the validated work tree).
git diff --quiet --no-renames 2>"$TMP/err"
DIFF_EXIT=$?
case "$DIFF_EXIT" in
    0) ;;
    1) fail tree_dirty "a tracked file has an unstaged change" ;;
    *) cat -- "$TMP/err" >&2; fail tree_dirty "git diff --quiet exited $DIFF_EXIT" ;;
esac

# count_markers <file> : print the number of conflict-marker lines in <file>.
count_markers() {
    local n rc
    n="$(grep -a -c -E '^(<{7}|[|]{7}|={7}|>{7})( |$)' -- "$1")"
    rc=$?
    [ "$rc" -le 1 ] || return 1
    printf '%s' "${n:-0}"
}

# Step 4: no resolved path holds more marker lines than its stage-1 blob did.
i=0
while [ "$i" -lt "${#M_PATHS[@]}" ]; do
    path="${M_PATHS[$i]}"
    oid="${M_OIDS[$i]}"
    i=$((i + 1))
    # A path resolved by deletion is not in the index and is skipped.
    git rev-parse -q --verify ":0:$path" >/dev/null 2>&1 || continue
    git cat-file blob ":0:$path" >"$TMP/result" 2>"$TMP/err" \
        || { cat -- "$TMP/err" >&2; fail markers "cannot read the staged blob of $path"; }
    have="$(count_markers "$TMP/result")" || fail markers "cannot count markers in $path"
    base_count=0
    if [ "$oid" != "-" ]; then
        git cat-file blob "$oid" >"$TMP/base" 2>"$TMP/err" \
            || { cat -- "$TMP/err" >&2; fail usage "manifest stage-1 blob $oid of $path is not readable"; }
        base_count="$(count_markers "$TMP/base")" || fail markers "cannot count markers in the stage-1 blob of $path"
    fi
    [ "$have" -le "$base_count" ] \
        || fail markers "$path holds $have conflict-marker line(s); its stage-1 blob had $base_count"
done

# Step 5: outside the manifest, the index equals the merge-tree result path by path.
git diff --cached --name-only --no-renames -z HEAD >"$TMP/staged" 2>"$TMP/err" \
    || { cat -- "$TMP/err" >&2; fail staged_unexpected "git diff --cached HEAD failed"; }
git diff --name-only --no-renames -z HEAD "$MT_OID" >"$TMP/merged" 2>"$TMP/err" \
    || { cat -- "$TMP/err" >&2; fail staged_unexpected "git diff of HEAD against the merge tree failed"; }
for list_file in "$TMP/staged" "$TMP/merged"; do
    read_nul_list "$list_file"
    for path in ${LIST[@]+"${LIST[@]}"}; do
        if in_list "$path" ${M_PATHS[@]+"${M_PATHS[@]}"}; then
            continue
        fi
        index_blob="$(git rev-parse -q --verify ":0:$path" 2>/dev/null)" || index_blob=""
        merged_blob="$(git rev-parse -q --verify "${MT_OID}:$path" 2>/dev/null)" || merged_blob=""
        [ "$index_blob" = "$merged_blob" ] \
            || fail staged_unexpected "the index differs from the merge-tree result at $path"
    done
done

# Step 6: the one commit, with hooks on. git's output goes to stderr verbatim.
if ! git commit -F "$MESSAGE_FILE" >"$TMP/commit.out" 2>&1; then
    cat -- "$TMP/commit.out" >&2
    fail hook_rejected "the commit was rejected (output above); the merge is still in progress"
fi
cat -- "$TMP/commit.out" >&2

# Step 7: exactly the parents [old HEAD, base tip].
PARENTS_LINE="$(git rev-list --parents -n 1 HEAD 2>/dev/null)" || PARENTS_LINE=""
read -r NEW_SHA P1 P2 EXTRA <<EOF_PARENTS
$PARENTS_LINE
EOF_PARENTS
[ -n "${NEW_SHA:-}" ] && [ -z "${EXTRA:-}" ] \
    && [ "$(lower "${P1:-}")" = "$(lower "$OLD_HEAD")" ] \
    && [ "$(lower "${P2:-}")" = "$(lower "$BASE_SHA")" ] \
    || fail parents_mismatch "new commit parents are '${PARENTS_LINE}', expected <new> $OLD_HEAD $BASE_SHA"

# Step 8: clean after the commit.
git status --porcelain=v1 --untracked-files=no -z >"$TMP/status" 2>"$TMP/err" \
    || { cat -- "$TMP/err" >&2; fail tree_dirty "git status failed after the commit"; }
[ ! -s "$TMP/status" ] || fail tree_dirty "tracked files differ from the new commit"
git diff --quiet HEAD 2>/dev/null || fail tree_dirty "the work tree differs from the new commit"

# Step 9.
jq -nc --arg merge_sha "$NEW_SHA" --arg old "$P1" --arg base "$P2" \
    '{merge_sha: $merge_sha, parents: [$old, $base]}' \
    || fail usage "could not render the finish JSON"
exit 0
