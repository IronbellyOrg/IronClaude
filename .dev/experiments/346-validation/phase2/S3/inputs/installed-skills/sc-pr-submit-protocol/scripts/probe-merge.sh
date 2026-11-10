#!/usr/bin/env bash
#
# probe-merge.sh — read-only merge probe for sc:pr-submit conflict cycles (issue #305).
#
# Purpose : Report, without changing anything, whether HEAD merges cleanly with the
#           base branch, which paths conflict and at which stages, and whether a
#           foreign operation (merge, rebase, cherry-pick, revert) is in progress.
#           It never changes the index, the work tree, HEAD or any branch. It may
#           write unreachable tree objects (harmless) and the fetch updates
#           refs/remotes/origin/<base>.
# Usage   : probe-merge.sh --repo <owner/repo> --ops-only
#           probe-merge.sh --repo <owner/repo> --base <branch> [--program <name>]...
# Output  : exactly one stdout line. Success is one JSON object:
#           ops mode  {"ok":true,"mode":"ops","foreign_op":..,"merge_head":..}
#           full mode {"ok":true,"mode":"full","merge_tree_supported":..,"base_ref":..,
#           "base_sha":..,"head_sha":..,"merge_base":..,"behind":N,"ahead":N,
#           "foreign_op":..,"merge_head":..,"tree_clean":..,"status_b64":..,"clean":..,
#           "merge_tree_b64":..,"numstat_ours_b64":..,"numstat_theirs_b64":..,
#           "programs":[..],"truncated":..}
#           Failure is the token "PROBE_FAIL <reason>"; details go to stderr.
# Exit    : 0 on any completed probe; 2 with PROBE_FAIL usage | not_a_worktree |
#           origin_mismatch | bad_base | fetch_failed | no_merge_base | merge_tree_failed.
# Contract: the JSON is validated by superclaude.pr_submit.conflicts.parse_probe
#           (design section 7.1). No stdin read, no prompt, no stored config write.

set -u -o pipefail

MAX_BYTES=102400
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
    printf 'probe-merge: %s\n' "$2" >&2
    printf 'PROBE_FAIL %s\n' "$1"
    exit 2
}

# Run a git command that can block under `timeout 60` when timeout is on PATH.
git_blocking() {
    if command -v timeout >/dev/null 2>&1; then
        timeout 60 git "$@"
    else
        git "$@"
    fi
}

# Step 1: arguments.
REPO=""
BASE=""
OPS_ONLY=0
PROGRAMS=()
while [ $# -gt 0 ]; do
    case "$1" in
        --repo|--base|--program)
            [ $# -ge 2 ] || fail usage "missing value for $1"
            case "$1" in
                --repo) REPO="$2" ;;
                --base) BASE="$2" ;;
                --program) PROGRAMS+=("$2") ;;
            esac
            shift 2
            ;;
        --ops-only) OPS_ONLY=1; shift ;;
        *) fail usage "unknown argument: $1" ;;
    esac
done
[ -n "$REPO" ] || fail usage "missing required --repo <owner/repo>"
[ "$OPS_ONLY" -eq 1 ] || [ -n "$BASE" ] || fail usage "missing required --base <branch> (or pass --ops-only)"
command -v jq >/dev/null 2>&1 || fail usage "jq not found on PATH"
command -v base64 >/dev/null 2>&1 || fail usage "base64 not found on PATH"

# Step 2: inside a work tree.
INSIDE="$(git rev-parse --is-inside-work-tree 2>/dev/null)" || INSIDE=""
[ "$INSIDE" = "true" ] || fail not_a_worktree "not inside a git work tree"

# Step 3: origin must be the given repo, so the fetch can only reach it.
ORIGIN_REPO="$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')" || ORIGIN_REPO=""
[ -n "$ORIGIN_REPO" ] && [ "$ORIGIN_REPO" = "$REPO" ] \
    || fail origin_mismatch "origin resolves to '${ORIGIN_REPO}', not '${REPO}'; nothing fetched"

# Step 4: foreign operation and MERGE_HEAD (worktree-aware paths).
FOREIGN_OP=""
for name in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD REVERT_HEAD sequencer; do
    op_path="$(git rev-parse --git-path "$name" 2>/dev/null)" || continue
    if [ -n "$op_path" ] && [ -e "$op_path" ]; then
        FOREIGN_OP="$name"
        break
    fi
done
MERGE_HEAD_SHA="$(git rev-parse -q --verify 'MERGE_HEAD^{commit}' 2>/dev/null)" || MERGE_HEAD_SHA=""

if [ "$OPS_ONLY" -eq 1 ]; then
    jq -nc --arg op "$FOREIGN_OP" --arg mh "$MERGE_HEAD_SHA" \
        '{ok: true, mode: "ops",
          foreign_op: (if $op == "" then null else $op end),
          merge_head: (if $mh == "" then null else $mh end)}' \
        || fail usage "could not render the probe JSON"
    exit 0
fi

# Step 5: the base branch name.
case "$BASE" in
    -*) fail bad_base "base branch name starts with '-': $BASE" ;;
esac
git check-ref-format --branch "$BASE" >/dev/null 2>&1 || fail bad_base "not a valid branch name: $BASE"

# Temporary files live only under the repository's git directory.
TMP_ROOT="$(git rev-parse --git-path sc-pr-submit-tmp 2>/dev/null)" || TMP_ROOT=""
[ -n "$TMP_ROOT" ] || fail usage "cannot resolve the git directory for temporary files"
mkdir -p -- "$TMP_ROOT" 2>/dev/null || fail usage "cannot create $TMP_ROOT"
TMP="$(mktemp -d "$TMP_ROOT/probe.XXXXXXXX" 2>/dev/null)" || { TMP=""; fail usage "cannot create a temporary directory under $TMP_ROOT"; }

# Step 6: tracked-file status (untracked files ignored). No optional index refresh.
git --no-optional-locks status --porcelain=v1 --untracked-files=no -z >"$TMP/status" 2>/dev/null \
    || fail not_a_worktree "git status failed"
TREE_CLEAN=false
[ -s "$TMP/status" ] || TREE_CLEAN=true

# Step 7: fetch the base branch from origin only.
if ! git_blocking fetch --no-tags origin "$BASE" >/dev/null 2>"$TMP/fetch.err"; then
    cat -- "$TMP/fetch.err" >&2
    fail fetch_failed "cannot reach remote origin (git fetch of '$BASE' failed)"
fi
BASE_SHA="$(git rev-parse -q --verify "refs/remotes/origin/${BASE}^{commit}" 2>/dev/null)" \
    || fail fetch_failed "refs/remotes/origin/$BASE is missing after the fetch"

# Step 8: head, merge base, behind / ahead.
HEAD_SHA="$(git rev-parse -q --verify 'HEAD^{commit}' 2>/dev/null)" || fail no_merge_base "HEAD does not name a commit"
MERGE_BASE="$(git merge-base HEAD "$BASE_SHA" 2>/dev/null)" \
    || fail no_merge_base "HEAD and origin/$BASE share no merge base"
COUNTS="$(git rev-list --left-right --count "${BASE_SHA}...HEAD" 2>/dev/null)" \
    || fail no_merge_base "cannot count commits between origin/$BASE and HEAD"
read -r BEHIND AHEAD <<EOF_COUNTS
$COUNTS
EOF_COUNTS
case "${BEHIND:-x}${AHEAD:-x}" in
    *[!0-9]*) fail no_merge_base "unexpected rev-list count output: $COUNTS" ;;
esac

# Step 13 (computed early; it reads nothing from the repository): available programs.
FOUND_PROGRAMS=()
for prog in ${PROGRAMS[@]+"${PROGRAMS[@]}"}; do
    if command -v -- "$prog" >/dev/null 2>&1; then
        FOUND_PROGRAMS+=("$prog")
    fi
done
PROGRAMS_JSON="$(printf '%s\n' ${FOUND_PROGRAMS[@]+"${FOUND_PROGRAMS[@]}"} | jq -Rsc 'split("\n") | map(select(. != ""))')" \
    || fail usage "could not render the program list"

# emit <supported> <clean> : print the one JSON line (step 14) and exit 0.
# A captured file above MAX_BYTES makes the probe truncated (step 12): every *_b64 null.
emit() {
    local supported="$1" clean="$2" truncated=false nulls='[]' f key
    for f in status merge_tree numstat_ours numstat_theirs; do
        if [ -f "$TMP/$f" ] && [ "$(wc -c <"$TMP/$f")" -gt "$MAX_BYTES" ]; then
            truncated=true
        fi
    done
    for key in status merge_tree numstat_ours numstat_theirs; do
        if [ "$truncated" = true ] || [ ! -f "$TMP/$key" ]; then
            nulls="$(jq -nc --argjson n "$nulls" --arg k "${key}_b64" '$n + [$k]')"
            : >"$TMP/$key.b64"
        else
            base64 <"$TMP/$key" | tr -d '\n' >"$TMP/$key.b64"
        fi
    done
    jq -nc \
        --argjson supported "$supported" \
        --arg base_ref "origin/$BASE" \
        --arg base_sha "$BASE_SHA" \
        --arg head_sha "$HEAD_SHA" \
        --arg merge_base "$MERGE_BASE" \
        --argjson behind "$BEHIND" \
        --argjson ahead "$AHEAD" \
        --arg op "$FOREIGN_OP" \
        --arg mh "$MERGE_HEAD_SHA" \
        --argjson tree_clean "$TREE_CLEAN" \
        --argjson clean "$clean" \
        --argjson programs "$PROGRAMS_JSON" \
        --argjson truncated "$truncated" \
        --argjson nulls "$nulls" \
        --rawfile status_b64 "$TMP/status.b64" \
        --rawfile merge_tree_b64 "$TMP/merge_tree.b64" \
        --rawfile numstat_ours_b64 "$TMP/numstat_ours.b64" \
        --rawfile numstat_theirs_b64 "$TMP/numstat_theirs.b64" \
        '{ok: true, mode: "full", merge_tree_supported: $supported,
          base_ref: $base_ref, base_sha: $base_sha, head_sha: $head_sha, merge_base: $merge_base,
          behind: $behind, ahead: $ahead,
          foreign_op: (if $op == "" then null else $op end),
          merge_head: (if $mh == "" then null else $mh end),
          tree_clean: $tree_clean, status_b64: $status_b64,
          clean: $clean, merge_tree_b64: $merge_tree_b64,
          numstat_ours_b64: $numstat_ours_b64, numstat_theirs_b64: $numstat_theirs_b64,
          programs: $programs, truncated: $truncated}
         | reduce $nulls[] as $k (.; .[$k] = null)' \
        || fail usage "could not render the probe JSON"
    exit 0
}

# Step 9: capability by behaviour, never by version.
if ! git merge-tree --write-tree HEAD HEAD >/dev/null 2>&1; then
    printf 'probe-merge: git merge-tree --write-tree is not supported here\n' >&2
    emit false null
fi

# Step 10: the merge itself, written as objects only.
git merge-tree --write-tree -z HEAD "$BASE_SHA" >"$TMP/merge_tree" 2>"$TMP/merge_tree.err"
MT_EXIT=$?
case "$MT_EXIT" in
    0) CLEAN=true ;;
    1) CLEAN=false ;;
    *)
        cat -- "$TMP/merge_tree.err" >&2
        fail merge_tree_failed "git merge-tree exited $MT_EXIT"
        ;;
esac

# Step 11: per-side numstat (binary detection) only when the merge conflicts.
if [ "$CLEAN" = false ]; then
    git --no-optional-locks diff --numstat -z --no-renames --no-ext-diff --no-textconv \
        "$MERGE_BASE" HEAD >"$TMP/numstat_ours" 2>/dev/null \
        || fail merge_tree_failed "numstat of HEAD against the merge base failed"
    git --no-optional-locks diff --numstat -z --no-renames --no-ext-diff --no-textconv \
        "$MERGE_BASE" "$BASE_SHA" >"$TMP/numstat_theirs" 2>/dev/null \
        || fail merge_tree_failed "numstat of origin/$BASE against the merge base failed"
fi

# Steps 12 and 14.
emit true "$CLEAN"
