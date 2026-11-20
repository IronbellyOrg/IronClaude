#!/usr/bin/env bash
#
# settle.sh: the mechanical parts of /sc:closeout, for a pull request that merged.
# It works with the adopted branch-landed.sh (the truth check) and is new code.
#
# Purpose : Settle the three items of a merged pull request (the issue, the work report
#           entry, the worker's Orca task), read the evidence the done-check needs, and
#           check that no item was left without a final status. Each settle step reads
#           the current state first and writes only if the state is not already final.
#           A model is used for two things only, and never inside this script: it writes
#           a verdict file after reading the evidence, and it writes the note's one
#           sentence. Every status comes from a table here, from the verdict word and
#           the read-backs.
# Usage   : settle.sh issue    <PR> [--issue N] [--match M] [--verdict F --dir D] [--what TEXT]
#           settle.sh evidence <PR> --issue N [--match M]     (prints dir=<path> on its line)
#           settle.sh entry    --key <key> [--issue-open] [--match M]
#           settle.sh task     <PR> [--issue N] [--issue-done] [--dispatch ID | --title T] [--match M]
#           settle.sh check                                    (reads three lines on stdin)
#           <PR> is a number or #<number>. --match carries the match= value of the
#           branch-landed.sh line; with "differs" every step prints
#           "escalated why=merge_differs" and writes nothing. --dir D is required with
#           --verdict and is the dir= value of the EVIDENCE line. The repository is the
#           origin remote of the current directory and nothing else; every gh call
#           names it with --repo.
# Output  : exactly one stdout line per step, "<ITEM> <status> <key>=<value> ... how=<token>"
#           or "... why=<token>"; details go to stderr. The status words, the tokens and
#           the fixed sentences are in refs/settle.md next to this folder's scripts.
# Exit    : 0 for settled, already_final and none_found; 1 for escalated; 2 for bad
#           arguments ("SETTLE_FAIL <reason>") and for a failed check ("CHECK_FAIL <item>").
# Contract: no stdin read except in check, no prompt, never prints an environment value.
# Writes  : gh issue comment and gh issue close for the issue, and the Orca task update.
#           Nothing else is written to GitHub, and nothing in the checkout.

set -u -o pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
DENY_FILE="$SCRIPT_DIR/deny-names.txt"
SETTLE_REF="$SCRIPT_DIR/../refs/settle.md"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"

WORK=""
cleanup() {
    [ -n "$WORK" ] && [ -d "$WORK" ] && rm -rf -- "$WORK"
}
trap cleanup EXIT

TAB=$'\t'
EM_DASH=$(printf '\342\200\224')
EN_DASH=$(printf '\342\200\223')

# ---------------------------------------------------------------------------
# Failure and argument helpers
# ---------------------------------------------------------------------------

setfail() {
    # setfail <reason> <detail>
    printf 'settle: %s\n' "$2" >&2
    printf 'SETTLE_FAIL %s\n' "$1"
    exit 2
}

SEEN_FLAGS=" "
once() {
    case "$SEEN_FLAGS" in
        *" $1 "*) setfail usage "repeated flag $1" ;;
    esac
    SEEN_FLAGS="$SEEN_FLAGS$1 "
}

need_value() {
    # need_value <flag> <remaining argument count>
    [ "$2" -ge 2 ] || setfail usage "flag $1 needs a value"
}

is_number() {
    case "$1" in
        '' | *[!0-9]*) return 1 ;;
    esac
    return 0
}

parse_pr() {
    # parse_pr <argument>: sets PR
    local arg=${1:-}
    arg=${arg#\#}
    is_number "$arg" || setfail usage "the pull request must be a number"
    PR=$((10#$arg))
    [ "$PR" -gt 0 ] || setfail usage "the pull request must be a number"
}

set_match() {
    case "$1" in
        same | differs | unchecked) OPT_MATCH="$1" ;;
        *) setfail usage "--match is same, differs or unchecked" ;;
    esac
}

make_work() {
    WORK=$(mktemp -d "${TMPDIR:-/tmp}/sc-settle.XXXXXX") || setfail mktemp_failed "cannot make a temporary directory"
}

resolve_repo() {
    # The repository is the origin remote and nothing else (decision D4).
    command -v jq >/dev/null 2>&1 || setfail no_jq "jq is required"
    local url re='^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$'
    url=$(git remote get-url origin 2>/dev/null </dev/null || true)
    url=${url%.git}
    url=${url#git@github.com:}
    url=${url#https://github.com/}
    url=${url#ssh://git@github.com/}
    if [[ "$url" =~ $re ]]; then
        GH_REPO="$url"
    else
        setfail no_origin "cannot parse the origin remote as a GitHub owner/repo"
    fi
}

# ---------------------------------------------------------------------------
# check: every item has a status word, every escalation has a known why token
# ---------------------------------------------------------------------------

cmd_check() {
    [ $# -eq 0 ] || setfail usage "check takes no arguments"
    [ -r "$SETTLE_REF" ] || setfail ref_unreadable "cannot read refs/settle.md"
    local input line item second why known
    input=$(cat)
    known=$(grep -E '^\| (issue|entry|task|all three|any) \| `[a-z_]+` \|' "$SETTLE_REF" |
        sed -E 's/^\| [a-z ]+ \| `([a-z_]+)` \|.*/\1/')
    for item in ISSUE ENTRY TASK; do
        line=$(printf '%s\n' "$input" | grep -E "^$item " | head -n 1)
        if [ -z "$line" ]; then
            printf 'CHECK_FAIL %s\n' "$item"
            exit 2
        fi
        second=$(printf '%s\n' "$line" | awk '{print $2}')
        case "$second" in
            settled | already_final | none_found) ;;
            escalated)
                why=$(printf '%s\n' "$line" | tr ' ' '\n' | sed -n 's/^why=//p' | head -n 1)
                if [ -z "$why" ] || ! printf '%s\n' "$known" | grep -Fxq -- "$why"; then
                    printf 'CHECK_FAIL %s\n' "$item"
                    exit 2
                fi
                ;;
            *)
                printf 'CHECK_FAIL %s\n' "$item"
                exit 2
                ;;
        esac
    done
    printf 'CHECK ok\n'
    exit 0
}

# ---------------------------------------------------------------------------
# Text checks: the names, the pull request title and the dashes
# ---------------------------------------------------------------------------

# text_refused <file> <title>: 0 (refused, reason on stderr) when the text holds a
# dash, the pull request title (any letter case) or a name from deny-names.txt.
text_refused() {
    local file=$1 title=$2 stripped patterns
    if LC_ALL=C grep -qF -e "$EM_DASH" -e "$EN_DASH" -- "$file"; then
        printf 'settle: the text holds an em dash or an en dash\n' >&2
        return 0
    fi
    if [ -n "$title" ] && grep -qiF -- "$title" "$file"; then
        printf 'settle: the text quotes the pull request title\n' >&2
        return 0
    fi
    [ -r "$DENY_FILE" ] || setfail deny_names_unreadable "cannot read deny-names.txt"
    patterns="$WORK/deny.patterns"
    grep -Ev '^[[:space:]]*(#|$)' "$DENY_FILE" >"$patterns" || true
    # A name inside a path or file-name token is not a match.
    stripped="$WORK/stripped.txt"
    sed -E 's#[A-Za-z0-9_./-]*(/|\.[A-Za-z0-9_])[A-Za-z0-9_./-]*# #g' "$file" >"$stripped"
    if [ -s "$patterns" ] && grep -qiwF -f "$patterns" -- "$stripped"; then
        printf 'settle: the text holds a name that no output may contain\n' >&2
        return 0
    fi
    return 1
}

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

# render <template file> NAME=value ... : fills the {{NAME}} slots in one pass, so a
# value that holds a slot name is never filled in again.
render() {
    local file=$1 pair
    shift
    local -a args=()
    for pair in "$@"; do
        args+=(--arg "${pair%%=*}" "${pair#*=}")
    done
    sed '1{/^<!-- slots:/d;}' "$file" |
        jq -Rrs "${args[@]}" 'gsub("\\{\\{(?<k>[A-Z_]+)\\}\\}"; $ARGS.named[.k] // "")'
}

# ---------------------------------------------------------------------------
# issue: output
# ---------------------------------------------------------------------------

ISSUE_N=""
LINKS=""
issue_out() {
    # issue_out <status> <how=... or why=...> <note> [extra]
    local line="ISSUE $1"
    [ -n "$ISSUE_N" ] && line="$line n=$ISSUE_N"
    [ -n "$LINKS" ] && line="$line links=$LINKS"
    line="$line $2 note=$3"
    [ -n "${4:-}" ] && line="$line $4"
    printf '%s\n' "$line"
    [ "$1" = escalated ] && exit 1
    exit 0
}

# ---------------------------------------------------------------------------
# issue: which issue (section 5.2 step 1)
# ---------------------------------------------------------------------------

BODY_REFS_JQ='
  def kind: if (.[0] != null) then "closing" else "refs" end;
  [ (.body // "")
    | scan("(?i)((?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)[: ]+)?(https://github\\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/issues/[0-9]+|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[0-9]+|#[0-9]+)") ]
  | .[]
  | . as $m
  | ($m[1]) as $ref
  | (if ($ref | startswith("https://")) then ($ref | capture("^https://github\\.com/(?<r>[^/]+/[^/]+)/issues/(?<n>[0-9]+)$"))
     elif ($ref | startswith("#")) then {r: $r, n: ($ref | ltrimstr("#"))}
     else ($ref | capture("^(?<r>[^#]+)#(?<n>[0-9]+)$")) end) as $c
  | select(($c.r | ascii_downcase) == $r)
  | "\($m | kind) \($c.n)"
'

find_issue() {
    local lowrepo cl_nums body_lines cands n obj remaining="" count=0 explicit=0
    lowrepo=$(printf '%s' "$GH_REPO" | tr '[:upper:]' '[:lower:]')
    cl_nums=$(jq -r --arg r "$lowrepo" '.closingIssuesReferences[]?
        | select(((.repository.owner.login + "/" + .repository.name) | ascii_downcase) == $r)
        | .number' <<<"$PRJ" 2>/dev/null) || cl_nums=""
    body_lines=$(jq -r --arg r "$lowrepo" "$BODY_REFS_JQ" <<<"$PRJ" 2>/dev/null) || body_lines=""
    if [ -n "$OPT_ISSUE" ]; then
        explicit=1
        cands=$OPT_ISSUE
    elif [ -n "$cl_nums" ]; then
        cands=$cl_nums
    else
        cands=$(printf '%s\n' "$body_lines" | awk 'NF == 2 {print $2}')
    fi
    cands=$(printf '%s\n' "$cands" | sed '/^$/d' | sort -un)
    if [ "$explicit" -eq 1 ] && [ "$OPT_ISSUE" -eq "$PR" ]; then
        ISSUE_N=""
        issue_out escalated why=not_an_issue none
    fi
    while IFS= read -r n; do
        [ -n "$n" ] || continue
        [ "$n" -eq "$PR" ] && continue
        obj=$(gh api "repos/$GH_REPO/issues/$n" </dev/null 2>/dev/null) || issue_out escalated why=issue_lookup_failed none
        jq -e 'type == "object"' >/dev/null 2>&1 <<<"$obj" || issue_out escalated why=issue_lookup_failed none
        if jq -e 'has("pull_request")' >/dev/null 2>&1 <<<"$obj"; then
            if [ "$explicit" -eq 1 ]; then
                issue_out escalated why=not_an_issue none
            fi
            continue
        fi
        remaining="$remaining $n"
        count=$((count + 1))
    done <<<"$cands"
    if [ "$count" -eq 0 ]; then
        issue_out escalated why=no_issue_named none
    elif [ "$count" -gt 1 ]; then
        printf 'settle: the pull request names more than one issue:%s\n' "$remaining" >&2
        issue_out escalated why=several_issues none
    fi
    ISSUE_N=${remaining# }
    # The link is data and decides nothing (step 2).
    if printf '%s\n' "$cl_nums" | grep -Fxq -- "$ISSUE_N" ||
        printf '%s\n' "$body_lines" | grep -Fxq -- "closing $ISSUE_N"; then
        LINKS=closing
    elif printf '%s\n' "$body_lines" | grep -Fxq -- "refs $ISSUE_N"; then
        LINKS=refs
    else
        LINKS=none
    fi
}

# ---------------------------------------------------------------------------
# issue: the marker gate (section 5.2 step 3.2, decision D21)
# ---------------------------------------------------------------------------

PERM_CACHE=""
PERM_RES=""
perm_lookup() {
    # perm_lookup <login>: sets PERM_RES to yes, no or fail. One call per author per run.
    local login=$1 hit out rc re='^[A-Za-z0-9][]A-Za-z0-9._[-]*$'
    hit=$(printf '%s' "$PERM_CACHE" | awk -F'\t' -v l="$login" '$1 == l {print $2; exit}')
    if [ -n "$hit" ]; then
        PERM_RES=$hit
        return 0
    fi
    if ! [[ "$login" =~ $re ]]; then
        PERM_RES=no
    else
        out=$(gh api "repos/$GH_REPO/collaborators/$login/permission" --jq .role_name 2>"$WORK/perm.err" </dev/null)
        rc=$?
        if [ "$rc" -eq 0 ]; then
            case "$out" in
                admin | maintain | write | triage) PERM_RES=yes ;;
                null | *[!A-Za-z0-9_-]*) PERM_RES=fail ;;
                *) PERM_RES=no ;;
            esac
        elif grep -q 'HTTP 404' "$WORK/perm.err"; then
            PERM_RES=no
        else
            PERM_RES=fail
        fi
    fi
    PERM_CACHE="$PERM_CACHE$login$TAB$PERM_RES"$'\n'
}

MARK_FOUND=0
MARK_AT=""
MARK_STOP=0
scan_marker() {
    # scan_marker <marker> <issue json> <strict: 1 or 0>
    # A marker counts only on a comment by an author who can already close the issue.
    local mark=$1 json=$2 strict=$3 rows login assoc at
    MARK_FOUND=0
    MARK_AT=""
    MARK_STOP=0
    rows=$(jq -r --arg m "$mark" '.comments[]? | select((.body // "") | contains($m))
        | "\(.author.login // "")|\(.authorAssociation // "")|\(.createdAt // "")"' <<<"$json" 2>/dev/null)
    while IFS='|' read -r login assoc at; do
        [ -n "$login" ] || continue
        case "$assoc" in
            OWNER | MEMBER | COLLABORATOR) ;;
            *) continue ;;
        esac
        perm_lookup "$login"
        case "$PERM_RES" in
            yes)
                MARK_FOUND=1
                if [[ "$at" > "$MARK_AT" ]]; then MARK_AT=$at; fi
                ;;
            fail)
                if [ "$strict" -eq 1 ]; then MARK_STOP=1; fi
                ;;
        esac
    done <<<"$rows"
}

read_issue() {
    # read_issue: sets IV from the state read; a failed read is issue_lookup_failed.
    IV=$(gh issue view "$ISSUE_N" --repo "$GH_REPO" --json state,stateReason,comments </dev/null 2>/dev/null) ||
        issue_out escalated why=issue_lookup_failed none
    jq -e 'type == "object"' >/dev/null 2>&1 <<<"$IV" || issue_out escalated why=issue_lookup_failed none
}

reopen_guard() {
    # Reads every page of the timeline, kept to the closed and reopened events.
    local tl line ev at reopened=0 re
    re=$'^(closed|reopened)\t[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$'
    tl=$(gh api --paginate "repos/$GH_REPO/issues/$ISSUE_N/timeline?per_page=100" --jq '.[] | select(.event=="closed" or .event=="reopened") | [.event, .created_at] | @tsv' </dev/null 2>/dev/null) ||
        issue_out escalated why=issue_lookup_failed already_there
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        [[ "$line" =~ $re ]] || issue_out escalated why=issue_lookup_failed already_there
        ev=${line%%"$TAB"*}
        at=${line#*"$TAB"}
        if [ "$ev" = reopened ] && [[ "$at" > "$MARK_AT" ]]; then reopened=1; fi
    done <<<"$tl"
    if [ "$reopened" -eq 1 ]; then
        issue_out escalated why=reopened already_there
    fi
}

# ---------------------------------------------------------------------------
# issue: the verdict (section 5.2 step 4): shape check, then the cross-check
# ---------------------------------------------------------------------------

VERDICT_AWK='
function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t\r]+$/, "", s); return s }
function bad(msg) { print "ERR " msg; failed = 1; exit 1 }
function in_set(v, set,   n, a, i) {
  n = split(set, a, " ")
  for (i = 1; i <= n; i++) if (a[i] == v) return 1
  return 0
}
function splitlit(s, arr, sep,   n, i) {
  n = 0
  while ((i = index(s, sep)) > 0) {
    arr[++n] = substr(s, 1, i - 1)
    s = substr(s, i + length(sep))
  }
  arr[++n] = s
  return n
}
function placeholder(v) { return (v ~ /^<[^<>]*>$/) }
function parse_checked(item,   kind, rest, i, rd, fd) {
  if (!match(item, /^\[[a-z_]+\] /)) bad("a checked line has no [kind]: " item)
  kind = substr(item, 2, RLENGTH - 3)
  rest = trim(substr(item, RLENGTH + 1))
  if (!in_set(kind, KINDS)) bad("a checked line has a kind outside the closed set: " kind)
  i = index(rest, " | ")
  if (i == 0) bad("a checked line has no what was found: " item)
  rd = trim(substr(rest, 1, i - 1)); fd = trim(substr(rest, i + 3))
  if (rd == "" || fd == "") bad("a checked line has an empty part: " item)
  if (placeholder(rd) || placeholder(fd)) bad("a placeholder is left in a checked line: " item)
  if ((kind == "target_pr" || kind == "linked_pr") && rd !~ /^PR #[0-9]+$/)
    bad("a " kind " line must name the number as PR #<n>: " item)
  if (kind == "other_pr" && rd !~ /^PR #[0-9]+$/ && rd != "none found")
    bad("an other_pr line must say PR #<n> or none found: " item)
  seenkind[kind] = 1
  printf "CHECKED\t%s\t%s\t%s\n", kind, rd, fd
}
function parse_crit(item,   src, rest, n, p, prs, dl, crit, j, m, q, part, colon, num, files, k, f, t, fn, any, plist, seennum) {
  if (!match(item, /^\[[a-z_]+\] /)) bad("a criteria line has no [source]: " item)
  src = substr(item, 2, RLENGTH - 3)
  rest = trim(substr(item, RLENGTH + 1))
  if (!in_set(src, SOURCES)) bad("a criterion has a source outside the closed set: " src)
  n = splitlit(rest, p, " | ")
  if (n < 3) bad("a criteria line needs four parts: " item)
  prs = trim(p[n]); dl = trim(p[n - 1]); crit = p[1]
  for (j = 2; j <= n - 2; j++) crit = crit " | " p[j]
  crit = trim(crit)
  if (crit == "") bad("a criterion is empty: " item)
  if (placeholder(crit)) bad("a placeholder is left in a criterion: " item)
  if (!in_set(dl, DELIVERED)) bad("a criterion has a delivered word outside the closed set: " dl)
  ncrit++
  plist = ""
  delete seennum
  if (prs == "none") {
    if (dl == "delivered") bad("a criterion marked delivered cites no pull request: " crit)
  } else {
    m = split(prs, q, ";")
    for (j = 1; j <= m; j++) {
      part = trim(q[j])
      if (part !~ /^PR #[0-9]+: .+$/) bad("a cited part is not in the form PR #<n>: <files>: " part)
      colon = index(part, ":")
      num = substr(part, 5, colon - 5)
      files = trim(substr(part, colon + 1))
      k = split(files, f, ",")
      any = 0
      for (t = 1; t <= k; t++) {
        fn = trim(f[t])
        if (fn != "") { any = 1; printf "CITE\t%d\t%s\t%s\n", ncrit, num, fn }
      }
      if (!any) bad("a cited pull request has no file names: " part)
      printf "CRITPR\t%d\t%s\n", ncrit, num
      if (!(num in seennum)) { seennum[num] = 1; plist = plist (plist == "" ? "" : ", ") "PR #" num }
    }
  }
  if (dl == "delivered") ndelivered++
  if (dl == "partly" || dl == "not_delivered") nunmet++
  printf "CRIT\t%d\t%s\t%s\t%s\t%s\n", ncrit, src, crit, dl, plist
}
BEGIN {
  KINDS = "issue_body issue_comments target_pr linked_pr other_pr later_stage remaining_item timeline"
  SOURCES = "fix_approach test_plan acceptance done_when other"
  DELIVERED = "delivered partly not_delivered unknown"
  VERDICTS = "done not_done unclear_escalate"
  nkeys = 0; section = ""
}
{
  line = $0
  sub(/\r$/, "", line)
  if (line ~ /^[ \t]*$/) next
  if (line ~ /^<!--.*-->[ \t]*$/) next
  if (line ~ /^- /) {
    if (section != "checked" && section != "criteria") bad("a list line outside checked and criteria: " line)
    if (section == "checked") parse_checked(substr(line, 3)); else parse_crit(substr(line, 3))
    next
  }
  if (!match(line, /^[a-z_]+:/)) bad("a line that is neither a key nor a list line: " line)
  key = substr(line, 1, RLENGTH - 1)
  val = trim(substr(line, RLENGTH + 1))
  nkeys++
  if (nkeys == 1 && key != "verdict") bad("the first key is not verdict")
  if (key in seen) bad("a repeated key: " key)
  seen[key] = 1
  if (key == "checked" || key == "criteria") {
    if (val != "") bad(key " must be followed by list lines only")
    section = key
  } else if (key == "verdict" || key == "issue" || key == "pr" || key == "reason" || key == "unsettled" || key == "question") {
    value[key] = val
    section = ""
  } else bad("an unknown key: " key)
}
END {
  if (failed) exit 1
  if (!("verdict" in seen)) bad("there is no verdict key")
  if (!in_set(value["verdict"], VERDICTS)) bad("the verdict is not done, not_done or unclear_escalate")
  if (value["issue"] != WANT_ISSUE) bad("the issue line does not equal the call (a stale file)")
  if (value["pr"] != WANT_PR) bad("the pr line does not equal the call (a stale file)")
  if (!("checked" in seen)) bad("there is no checked list")
  if (!("criteria" in seen)) bad("there is no criteria list")
  if (!seenkind["issue_body"] || !seenkind["issue_comments"] || !seenkind["target_pr"] || !seenkind["other_pr"])
    bad("checked must hold issue_body, issue_comments, target_pr and other_pr")
  if (ncrit < 1) bad("criteria holds no line")
  r = trim(value["reason"])
  if (r == "" || placeholder(r)) bad("the reason is empty or a placeholder")
  if (split(r, w, /[ \t]+/) > 40) bad("the reason is longer than 40 words")
  if (value["verdict"] == "done" && nunmet + 0 > 0) bad("a done verdict has a criterion that is partly or not_delivered")
  if (value["verdict"] == "done" && ndelivered != ncrit) bad("a done verdict needs every criterion delivered")
  if (value["verdict"] == "not_done" && nunmet + 0 < 1) bad("a not_done verdict needs a criterion that is partly or not_delivered")
  if (value["verdict"] == "unclear_escalate" && (trim(value["unsettled"]) == "" || trim(value["question"]) == ""))
    bad("unclear_escalate needs unsettled and question")
  printf "VERDICT\t%s\n", value["verdict"]
  printf "REASON\t%s\n", r
  printf "UNSETTLED\t%s\n", trim(value["unsettled"])
  printf "QUESTION\t%s\n", trim(value["question"])
  printf "NUNMET\t%d\n", nunmet
}
'

EVIDENCE_TABLE_AWK='
/^## / { cur = ""; next }
/^PR #[0-9]+ state=/ {
  n = $2; sub(/^#/, "", n)
  st = $3; sub(/^state=/, "", st)
  tr = $5; sub(/^files_truncated=/, "", tr)
  printf "H\t%s\t%s\t%s\n", n, st, tr
  cur = n
  next
}
/^file: / { if (cur != "") printf "F\t%s\t%s\n", cur, substr($0, 7) }
'

verdict_refuse() {
    printf 'settle: verdict refused: %s\n' "$1" >&2
    return 1
}

# verdict_load: checks the verdict file against its shape and against the evidence.
# Sets V_WORD, V_REASON, V_UNSETTLED, V_QUESTION, V_RECORDS (the CRIT lines) and V_UNMET.
verdict_load() {
    local file=$OPT_VERDICT dir=$OPT_DIR out rc err ev table kind rd num n f st
    [ -n "$dir" ] && [ -d "$dir" ] || verdict_refuse "--dir is missing or is not a directory" || return 1
    ev="$dir/evidence.md"
    [ -r "$ev" ] || verdict_refuse "the evidence file is missing or unreadable" || return 1
    [ -f "$file" ] && [ -r "$file" ] && [ -s "$file" ] || verdict_refuse "the verdict file is missing, unreadable or empty" || return 1
    [ "$(sed -n 1p "$ev")" = "issue: $GH_REPO#$ISSUE_N" ] && [ "$(sed -n 2p "$ev")" = "pr: $PR" ] ||
        verdict_refuse "the evidence file names another issue or pull request" || return 1
    tr '\t' ' ' <"$file" >"$WORK/verdict.txt"
    if text_refused "$WORK/verdict.txt" "$PR_TITLE"; then
        verdict_refuse "the text breaks the title, name or dash rule" || return 1
    fi
    out=$(awk -v WANT_ISSUE="$GH_REPO#$ISSUE_N" -v WANT_PR="$PR" "$VERDICT_AWK" "$WORK/verdict.txt")
    rc=$?
    if [ "$rc" -ne 0 ]; then
        err=$(printf '%s\n' "$out" | grep '^ERR ' | head -n 1)
        verdict_refuse "${err#ERR }" || return 1
    fi
    table=$(awk "$EVIDENCE_TABLE_AWK" "$ev")
    V_WORD=$(printf '%s\n' "$out" | awk -F'\t' '$1 == "VERDICT" {print $2}')
    V_REASON=$(printf '%s\n' "$out" | awk -F'\t' '$1 == "REASON" {print $2}')
    V_UNSETTLED=$(printf '%s\n' "$out" | awk -F'\t' '$1 == "UNSETTLED" {print $2}')
    V_QUESTION=$(printf '%s\n' "$out" | awk -F'\t' '$1 == "QUESTION" {print $2}')
    V_UNMET=$(printf '%s\n' "$out" | awk -F'\t' '$1 == "NUNMET" {print $2}')
    V_RECORDS=$(printf '%s\n' "$out" | awk -F'\t' '$1 == "CRIT"')
    # (a) every cited pull request is the target or was read; for a done verdict it merged.
    while IFS="$TAB" read -r kind rd num; do
        [ "$kind" = CRITPR ] || continue
        st=$(printf '%s\n' "$table" | awk -F'\t' -v n="$num" '$1 == "H" && $2 == n {print $3; exit}')
        if [ -z "$st" ] && [ "$num" != "$PR" ]; then
            verdict_refuse "a criterion cites PR #$num, which the evidence does not hold" || return 1
        fi
        if [ "$V_WORD" = "done" ] && [ -n "$st" ] && [ "$st" != MERGED ]; then
            verdict_refuse "a done verdict cites PR #$num, which is not merged in the evidence" || return 1
        fi
    done < <(printf '%s\n' "$out" | awk -F'\t' '$1 == "CRITPR" {print $1 "\t" $2 "\t" $3}')
    # (b) every cited file is one the evidence lists, unless that list is truncated.
    while IFS="$TAB" read -r kind rd num f; do
        [ "$kind" = CITE ] || continue
        st=$(printf '%s\n' "$table" | awk -F'\t' -v n="$num" '$1 == "H" && $2 == n {print $4; exit}')
        [ -n "$st" ] || continue
        [ "$st" = yes ] && continue
        if ! printf '%s\n' "$table" | grep -Fxq -- "F$TAB$num$TAB$f"; then
            verdict_refuse "PR #$num is cited with a file the evidence does not list: $f" || return 1
        fi
    done < <(printf '%s\n' "$out" | awk -F'\t' '$1 == "CITE"')
    # (c) the number on a target_pr or linked_pr line was read.
    while IFS="$TAB" read -r kind rd num; do
        case "$rd" in
            target_pr | linked_pr)
                n=${num#PR #}
                st=$(printf '%s\n' "$table" | awk -F'\t' -v n="$n" '$1 == "H" && $2 == n {print $3; exit}')
                if [ -z "$st" ] && [ "$n" != "$PR" ]; then
                    verdict_refuse "a $rd line names PR #$n, which the evidence does not hold" || return 1
                fi
                ;;
        esac
    done < <(printf '%s\n' "$out" | awk -F'\t' '$1 == "CHECKED" {print $1 "\t" $2 "\t" $3}')
    return 0
}

# ---------------------------------------------------------------------------
# issue: the writes (section 5.2 steps 3.3, 3.4, 4 and 5)
# ---------------------------------------------------------------------------

merger_name() {
    local login name
    login=$(jq -r '.mergedBy.login // ""' <<<"$PRJ" 2>/dev/null)
    if [ -z "$login" ]; then
        printf 'someone GitHub does not name'
        return 0
    fi
    name=$(gh api "users/$login" --jq .name </dev/null 2>/dev/null | head -n 1 | tr -d '\r')
    case "$name" in
        '' | null) name=$login ;;
    esac
    printf '%s' "$name"
}

# criteria_lines <kind>: the note's list, at most 10 lines and then "and <k> more".
criteria_lines() {
    local kind=$1 total=0 shown=0 idx crit dl plist out=""
    while IFS="$TAB" read -r _ idx _ crit dl plist; do
        [ -n "$idx" ] || continue
        if [ "$kind" = closing ]; then
            :
        else
            case "$dl" in
                partly | not_delivered) ;;
                *) continue ;;
            esac
        fi
        total=$((total + 1))
        [ "$shown" -lt 10 ] || continue
        shown=$((shown + 1))
        if [ "$kind" = closing ]; then
            out="$out- $crit ($plist)"$'\n'
        elif [ -n "$plist" ]; then
            out="$out- $crit (delivered in part by $plist)"$'\n'
        else
            out="$out- $crit (no pull request yet)"$'\n'
        fi
    done <<<"$V_RECORDS"
    if [ "$total" -gt 10 ]; then
        out="${out}and $((total - 10)) more"$'\n'
    fi
    printf '%s' "${out%$'\n'}"
}

NOTE_VALUE=none

post_note() {
    # post_note <template> <marker> NAME=value ... : posts the note once and reads it back.
    local template=$1 marker=$2 body
    shift 2
    if ! body=$(render "$template" "$@"); then
        printf 'settle: the note could not be rendered\n' >&2
        issue_out escalated why=note_failed none
    fi
    if ! gh issue comment "$ISSUE_N" --repo "$GH_REPO" --body "$body" </dev/null >/dev/null 2>"$WORK/post.err"; then
        cat -- "$WORK/post.err" >&2
        printf 'settle: posting the note failed\n' >&2
        issue_out escalated why=note_failed none
    fi
    if ! IV=$(gh issue view "$ISSUE_N" --repo "$GH_REPO" --json state,stateReason,comments </dev/null 2>/dev/null); then
        printf 'settle: the comments could not be read back\n' >&2
        issue_out escalated why=note_failed none
    fi
    scan_marker "$marker" "$IV" 0
    if [ "$MARK_FOUND" -ne 1 ]; then
        printf 'settle: the note marker was not read back on a comment that counts\n' >&2
        issue_out escalated why=note_failed none
    fi
    NOTE_VALUE=posted
}

do_close() {
    # do_close <note value>: write 2, the close, guarded by the state.
    local note=$1 state
    state=$(gh issue view "$ISSUE_N" --repo "$GH_REPO" --json state </dev/null 2>/dev/null | jq -r '.state // ""' 2>/dev/null)
    [ -n "$state" ] || issue_out escalated why=issue_lookup_failed "$note"
    if [ "$state" = CLOSED ]; then
        issue_out already_final how=already_closed "$note"
    fi
    local rc=0
    gh issue close "$ISSUE_N" --repo "$GH_REPO" --reason completed </dev/null >/dev/null 2>&1 || rc=$?
    state=$(gh issue view "$ISSUE_N" --repo "$GH_REPO" --json state </dev/null 2>/dev/null | jq -r '.state // ""' 2>/dev/null)
    if [ "$state" = CLOSED ]; then
        if [ "$rc" -eq 0 ]; then
            issue_out settled how=closed_now "$note"
        fi
        issue_out already_final how=already_closed "$note"
    fi
    issue_out escalated why=close_failed "$note"
}

link_sentence() {
    case "$LINKS" in
        closing) printf 'closes this issue with a closing keyword' ;;
        refs) printf 'names this issue without closing it' ;;
        *) printf 'does not name this issue, so this note is the link' ;;
    esac
}

write_done() {
    # The two guarded writes of a done verdict.
    local what name date commit sentence_file
    what=${OPT_WHAT:-}
    sentence_file="$WORK/what.txt"
    printf '%s\n' "$what" >"$sentence_file"
    if [ -z "$what" ] || text_refused "$sentence_file" "$PR_TITLE"; then
        what="$PR_FILES files changed."
    fi
    what=$(printf '%s' "$what" | tr '\r\n' '  ')
    name=$(merger_name)
    date=$(jq -r '(.mergedAt // "") | split("T")[0]' <<<"$PRJ" 2>/dev/null)
    commit=$(jq -r '(.mergeCommit.oid // "unknown") | .[0:7]' <<<"$PRJ" 2>/dev/null)
    [ -n "$date" ] || date=unknown
    post_note "$TEMPLATES_DIR/closing-note.md" "$DONE_MARK" \
        "REPO=$GH_REPO" "PR=$PR" "DATE=$date" "NAME=$name" "COMMIT=$commit" \
        "WHAT=$what" "REASON=$V_REASON" "CRITERIA=$(criteria_lines closing)" \
        "LINK_SENTENCE=$(link_sentence)"
    do_close "$NOTE_VALUE"
}

write_not_done() {
    local name date commit note=posted
    scan_marker "$ND_MARK" "$IV" 0
    if [ "$MARK_FOUND" -eq 1 ]; then
        note=already_there
    else
        name=$(merger_name)
        date=$(jq -r '(.mergedAt // "") | split("T")[0]' <<<"$PRJ" 2>/dev/null)
        commit=$(jq -r '(.mergeCommit.oid // "unknown") | .[0:7]' <<<"$PRJ" 2>/dev/null)
        [ -n "$date" ] || date=unknown
        post_note "$TEMPLATES_DIR/not-done-note.md" "$ND_MARK" \
            "REPO=$GH_REPO" "PR=$PR" "DATE=$date" "NAME=$name" "COMMIT=$commit" \
            "REMAINING=$(criteria_lines remaining)" "REASON=$V_REASON"
    fi
    issue_out settled how=left_open "$note" "remaining=$V_UNMET"
}

# ---------------------------------------------------------------------------
# issue
# ---------------------------------------------------------------------------

cmd_issue() {
    [ $# -ge 1 ] || setfail usage "issue needs <PR>"
    parse_pr "$1"
    shift
    OPT_ISSUE="" OPT_MATCH="" OPT_VERDICT="" OPT_DIR="" OPT_WHAT=""
    while [ $# -gt 0 ]; do
        once "$1"
        case "$1" in
            --issue)
                need_value "$1" $#
                is_number "$2" || setfail usage "--issue needs a number"
                OPT_ISSUE=$((10#$2))
                shift 2
                ;;
            --match) need_value "$1" $#; set_match "$2"; shift 2 ;;
            --verdict) need_value "$1" $#; OPT_VERDICT=$2; shift 2 ;;
            --dir) need_value "$1" $#; OPT_DIR=$2; shift 2 ;;
            --what) need_value "$1" $#; OPT_WHAT=$2; shift 2 ;;
            *) setfail usage "unknown argument $1" ;;
        esac
    done
    if [ "$OPT_MATCH" = differs ]; then
        ISSUE_N=$OPT_ISSUE
        issue_out escalated why=merge_differs none
    fi
    resolve_repo
    make_work
    DONE_MARK="<!-- sc:closeout pr=$PR -->"
    ND_MARK="<!-- sc:closeout pr=$PR verdict=not_done -->"

    PRJ=$(gh pr view "$PR" --repo "$GH_REPO" --json number,title,body,closingIssuesReferences,mergedAt,mergedBy,mergeCommit,changedFiles </dev/null 2>/dev/null) ||
        issue_out escalated why=issue_lookup_failed none
    jq -e 'type == "object"' >/dev/null 2>&1 <<<"$PRJ" || issue_out escalated why=issue_lookup_failed none
    PR_TITLE=$(jq -r '.title // ""' <<<"$PRJ" | head -n 1)
    PR_FILES=$(jq -r '.changedFiles // ((.files // []) | length) // 0' <<<"$PRJ" 2>/dev/null)
    [ -n "$PR_FILES" ] || PR_FILES=0

    find_issue
    read_issue
    local state sr extra=""
    state=$(jq -r '.state // ""' <<<"$IV")
    if [ "$state" = CLOSED ]; then
        sr=$(jq -r '.stateReason // ""' <<<"$IV")
        case "$sr" in
            '' | *[!A-Za-z_]*) ;;
            *) extra="reason=$sr" ;;
        esac
        issue_out already_final how=already_closed none "$extra"
    fi

    # The gate: a done marker that counts means an earlier run judged the issue done.
    scan_marker "$DONE_MARK" "$IV" 1
    if [ "$MARK_STOP" -eq 1 ]; then
        issue_out escalated why=issue_lookup_failed already_there
    fi
    if [ "$MARK_FOUND" -eq 1 ]; then
        reopen_guard
        do_close already_there
    fi

    # No counting marker: the issue needs a done verdict.
    [ -n "$OPT_VERDICT" ] || issue_out escalated why=no_verdict none
    if ! verdict_load; then
        issue_out escalated why=no_verdict none
    fi
    case "$V_WORD" in
        done) write_done ;;
        not_done) write_not_done ;;
        unclear_escalate)
            printf 'settle: unsettled: %s\n' "$V_UNSETTLED" >&2
            printf 'settle: question: %s\n' "$V_QUESTION" >&2
            issue_out escalated why=unclear none
            ;;
    esac
    issue_out escalated why=no_verdict none
}

# ---------------------------------------------------------------------------
# evidence (section 5.2 step 4, "The evidence, read by a script")
# ---------------------------------------------------------------------------

EV_DIR=""
ev_fail() {
    printf 'settle: %s\n' "$1" >&2
    if [ -n "$EV_DIR" ] && [ -d "$EV_DIR" ]; then
        rm -rf -- "$EV_DIR"
    fi
    printf 'EVIDENCE fail why=gh_failed\n'
    exit 1
}

# quote: every line of text written by a person starts with a fixed quote marker, so
# quoted text can never form a header line or a file line of the evidence file.
quote() {
    tr -d '\r' | sed 's/^/> /'
}

cmd_evidence() {
    [ $# -ge 1 ] || setfail usage "evidence needs <PR>"
    parse_pr "$1"
    shift
    OPT_ISSUE="" OPT_MATCH=""
    while [ $# -gt 0 ]; do
        once "$1"
        case "$1" in
            --issue)
                need_value "$1" $#
                is_number "$2" || setfail usage "--issue needs a number"
                OPT_ISSUE=$((10#$2))
                shift 2
                ;;
            --match) need_value "$1" $#; set_match "$2"; shift 2 ;;
            *) setfail usage "unknown argument $1" ;;
        esac
    done
    [ -n "$OPT_ISSUE" ] || setfail usage "evidence needs --issue N"
    if [ "$OPT_MATCH" = differs ]; then
        printf 'EVIDENCE escalated why=merge_differs\n'
        exit 1
    fi
    resolve_repo
    local n=$OPT_ISSUE slug
    slug=$(printf '%s' "$GH_REPO" | sed 's#/#__#; s#[^A-Za-z0-9_.-]#_#g')
    EV_DIR=$(mktemp -d "${TMPDIR:-/tmp}/sc-closeout-${slug}__${PR}.XXXXXX") ||
        setfail mktemp_failed "cannot make the evidence directory"
    chmod 700 "$EV_DIR"
    local ev="$EV_DIR/evidence.md" truncated=no lowrepo

    local iss tpr tl all open evt
    iss=$(gh issue view "$n" --repo "$GH_REPO" --json title,body,state,comments </dev/null 2>/dev/null) ||
        ev_fail "the issue could not be read"
    jq -e 'type == "object"' >/dev/null 2>&1 <<<"$iss" || ev_fail "the issue answer is not JSON"
    tpr=$(gh pr view "$PR" --repo "$GH_REPO" --json body,files,changedFiles,baseRefName,mergedAt,closingIssuesReferences,statusCheckRollup </dev/null 2>/dev/null) ||
        ev_fail "the pull request could not be read"
    jq -e 'type == "object"' >/dev/null 2>&1 <<<"$tpr" || ev_fail "the pull request answer is not JSON"
    tl=$(gh api "repos/$GH_REPO/issues/$n/timeline?per_page=100" </dev/null 2>/dev/null) ||
        ev_fail "the timeline could not be read"
    jq -e 'type == "array"' >/dev/null 2>&1 <<<"$tl" || ev_fail "the timeline answer is not a list"
    all=$(gh pr list --repo "$GH_REPO" --state all --search "$n" --limit 10 --json number,state,mergedAt,baseRefName </dev/null 2>/dev/null) ||
        ev_fail "the pull request search failed"
    jq -e 'type == "array"' >/dev/null 2>&1 <<<"$all" || ev_fail "the search answer is not a list"
    open=$(gh pr list --repo "$GH_REPO" --state open --search "$n" --limit 10 --json number,baseRefName,headRefName </dev/null 2>/dev/null) ||
        ev_fail "the open pull request search failed"
    jq -e 'type == "array"' >/dev/null 2>&1 <<<"$open" || ev_fail "the open search answer is not a list"

    lowrepo=$(printf '%s' "$GH_REPO" | tr '[:upper:]' '[:lower:]')
    # Candidates: merged first, then open, then the rest; the target comes first of all.
    local cand_json ncands
    cand_json=$(jq -n --argjson tl "$tl" --argjson all "$all" --argjson open "$open" \
        --arg r "$lowrepo" --argjson pr "$PR" --argjson n "$n" '
        def rank: if . == "MERGED" then 0 elif . == "OPEN" then 1 else 2 end;
        ( [ $tl[] | select(.event == "cross-referenced")
            | select(.source.issue.pull_request != null)
            | select(((.source.issue.repository.full_name // ((.source.issue.repository_url // "") | sub("^.*/repos/"; ""))) | ascii_downcase) == $r)
            | {number: .source.issue.number,
               state: (if .source.issue.pull_request.merged_at != null then "MERGED"
                       elif .source.issue.state == "open" then "OPEN" else "CLOSED" end)} ]
          + [ $all[] | {number: .number, state: .state} ]
          + [ $open[] | {number: .number, state: "OPEN"} ] )
        | map(select(.number != $pr and .number != $n))
        | group_by(.number) | map(.[0])
        | sort_by([(.state | rank), .number])' 2>/dev/null) || ev_fail "cannot join the pull request lists"
    ncands=$(jq 'length' <<<"$cand_json")
    local numbers
    numbers="$PR $(jq -r '.[0:9][].number' <<<"$cand_json" | tr '\n' ' ')"
    [ "$ncands" -le 9 ] || truncated=yes

    {
        printf 'issue: %s#%s\n' "$GH_REPO" "$n"
        printf 'pr: %s\n' "$PR"
        printf '## Issue\n'
        printf 'state: %s\n' "$(jq -r '.state // ""' <<<"$iss")"
        printf 'title:\n'
        jq -r '.title // ""' <<<"$iss" | quote
        printf 'body:\n'
        jq -r '(.body // "") | .[0:20000]' <<<"$iss" | quote
    } >"$ev"
    [ "$(jq -r '(.body // "") | length' <<<"$iss")" -le 20000 ] || truncated=yes
    local ncomments shown
    ncomments=$(jq '(.comments // []) | length' <<<"$iss")
    shown=$ncomments
    if [ "$ncomments" -gt 30 ]; then
        shown=30
        truncated=yes
    fi
    printf '## Comments (%s of %s)\n' "$shown" "$ncomments" >>"$ev"
    local i=0 head
    while [ "$i" -lt "$shown" ]; do
        head=$(jq -r --argjson i "$i" '.comments[$i] | "comment author=\(.author.login // "unknown") association=\(.authorAssociation // "NONE") at=\(.createdAt // "")" | gsub("[\r\n]"; "?")' <<<"$iss")
        printf '%s\n' "$head" >>"$ev"
        jq -r --argjson i "$i" '.comments[$i].body // ""' <<<"$iss" | quote >>"$ev"
        i=$((i + 1))
    done

    # Pull requests read: at most 10 (the target first), one header each.
    local k=0 num pj files_total listed ptrunc state cut body_limit nchecks nshown
    for num in $numbers; do
        pj=$(gh pr view "$num" --repo "$GH_REPO" --json state,mergedAt,baseRefName,body,files,changedFiles </dev/null 2>/dev/null) ||
            ev_fail "pull request $num could not be read"
        jq -e 'type == "object"' >/dev/null 2>&1 <<<"$pj" || ev_fail "pull request $num answer is not JSON"
        state=$(jq -r '.state // "UNKNOWN"' <<<"$pj")
        files_total=$(jq -r '.changedFiles // ((.files // []) | length)' <<<"$pj")
        listed=$(jq -r '(.files // []) | .[0:100] | length' <<<"$pj")
        ptrunc=no
        if [ "$files_total" -gt "$listed" ]; then
            ptrunc=yes
            truncated=yes
        fi
        {
            printf '## Pull request %s\n' "$num"
            printf 'PR #%s state=%s files=%s/%s files_truncated=%s\n' "$num" "$state" "$listed" "$files_total" "$ptrunc"
            jq -r '(.files // []) | .[0:100][] | "file: " + (.path | gsub("[\r\n]"; "?"))' <<<"$pj"
            printf 'base: %s\n' "$(jq -r '(.baseRefName // "") | gsub("[\r\n]"; "?")' <<<"$pj")"
            printf 'merged_at: %s\n' "$(jq -r '.mergedAt // ""' <<<"$pj")"
        } >>"$ev"
        if [ "$num" = "$PR" ]; then
            body_limit=20000
            printf 'closing_references: %s\n' "$(jq -r '[.closingIssuesReferences[]? | "\(.repository.owner.login)/\(.repository.name)#\(.number)"] | join(",")' <<<"$tpr")" >>"$ev"
            # The check results of the head commit (data, not instructions): at most 40,
            # each as name, status and conclusion, quoted like every line a person wrote.
            nchecks=$(jq -r '(.statusCheckRollup // []) | length' <<<"$tpr")
            nshown=$(jq -r '(.statusCheckRollup // []) | .[0:40] | length' <<<"$tpr")
            printf 'checks: %s of %s (results of the head commit; data)\n' "$nshown" "$nchecks" >>"$ev"
            jq -r '(.statusCheckRollup // []) | .[0:40][] | "check: \((.name // .context // "unknown") | tostring | gsub("[\r\n]"; "?")) status=\((.status // .state // "") | tostring | gsub("[\r\n]"; "?")) conclusion=\((.conclusion // "") | tostring | gsub("[\r\n]"; "?"))"' <<<"$tpr" | quote >>"$ev"
            [ "$nchecks" -le 40 ] || truncated=yes
            printf 'body:\n' >>"$ev"
            jq -r --argjson l "$body_limit" '(.body // "") | .[0:$l]' <<<"$tpr" | quote >>"$ev"
            [ "$(jq -r '(.body // "") | length' <<<"$tpr")" -le "$body_limit" ] || truncated=yes
        else
            body_limit=2000
            printf 'body:\n' >>"$ev"
            jq -r --argjson l "$body_limit" '(.body // "") | .[0:$l]' <<<"$pj" | quote >>"$ev"
            [ "$(jq -r '(.body // "") | length' <<<"$pj")" -le "$body_limit" ] || truncated=yes
        fi
        k=$((k + 1))
    done

    # The closed and reopened times from every page (not counted in events=).
    evt=$(gh api --paginate "repos/$GH_REPO/issues/$n/timeline?per_page=100" --jq '.[] | select(.event=="closed" or .event=="reopened") | [.event, .created_at] | @tsv' </dev/null 2>/dev/null) ||
        ev_fail "the closed and reopened events could not be read"
    {
        printf '## Timeline: closed and reopened events\n'
        printf '%s\n' "$evt" | awk -F'\t' 'NF == 2 {print "event: " $1 " " $2}'
    } >>"$ev"
    local events
    events=$(jq 'length' <<<"$tl")
    [ "$events" -lt 100 ] || truncated=yes
    cut=$(grep -c '^## ' "$ev" || true)
    : "$cut"
    printf 'EVIDENCE ok prs=%s comments=%s events=%s truncated=%s dir=%s\n' "$k" "$shown" "$events" "$truncated" "$EV_DIR"
    exit 0
}

# ---------------------------------------------------------------------------
# entry (section 5.3)
# ---------------------------------------------------------------------------

cmd_entry() {
    local key="" issue_open=0 match=""
    while [ $# -gt 0 ]; do
        once "$1"
        case "$1" in
            --key)
                need_value "$1" $#
                key=$2
                shift 2
                ;;
            --issue-open) issue_open=1; shift ;;
            --match) need_value "$1" $#; set_match "$2"; match=$OPT_MATCH; shift 2 ;;
            *) setfail usage "unknown argument $1" ;;
        esac
    done
    [ -n "$key" ] || setfail usage "entry needs --key"
    case "$key" in
        *[!A-Za-z0-9_.-]*) setfail usage "the key holds a character that is not a letter, a digit, an underscore, a dot or a hyphen" ;;
    esac
    if [ "$match" = differs ]; then
        printf 'ENTRY escalated key=%s why=merge_differs\n' "$key"
        exit 1
    fi
    if [ "$issue_open" -eq 1 ]; then
        printf 'ENTRY already_final key=%s how=issue_open\n' "$key"
        exit 0
    fi
    if ! superclaude orchestrator report-entry --help </dev/null >/dev/null 2>&1; then
        printf 'ENTRY escalated key=%s why=surface_absent\n' "$key"
        exit 1
    fi
    local out rc word
    out=$(superclaude orchestrator report-entry --key "$key" --closed </dev/null 2>/dev/null)
    rc=$?
    word=$(printf '%s\n' "$out" | head -n 1 | awk '{print $1}')
    if [ "$rc" -eq 0 ]; then
        case "$word" in
            moved)
                printf 'ENTRY settled key=%s how=moved\n' "$key"
                exit 0
                ;;
            already_closed)
                printf 'ENTRY already_final key=%s how=already_closed\n' "$key"
                exit 0
                ;;
            no_entry)
                printf 'ENTRY none_found key=%s\n' "$key"
                exit 0
                ;;
        esac
    fi
    printf 'ENTRY escalated key=%s why=entry_command_failed\n' "$key"
    exit 1
}

# ---------------------------------------------------------------------------
# task (section 5.4). The title uses the issue number <N>; the result text uses the
# pull request number <PR>. orca is called here and nowhere else.
# ---------------------------------------------------------------------------

task_out() {
    # task_out <status> <fields...>
    local status=$1
    shift
    local line="TASK $status"
    [ -n "$*" ] && line="$line $*"
    [ -n "$DISPATCH_STATE" ] && line="$line dispatch=$DISPATCH_STATE"
    printf '%s\n' "$line"
    [ "$status" = escalated ] && exit 1
    exit 0
}

DISPATCH_STATE=""

cmd_task() {
    [ $# -ge 1 ] || setfail usage "task needs <PR>"
    parse_pr "$1"
    shift
    OPT_ISSUE="" OPT_MATCH=""
    local dispatch="" title="" issue_done=0
    while [ $# -gt 0 ]; do
        once "$1"
        case "$1" in
            --issue)
                need_value "$1" $#
                is_number "$2" || setfail usage "--issue needs a number"
                OPT_ISSUE=$((10#$2))
                shift 2
                ;;
            --dispatch) need_value "$1" $#; dispatch=$2; shift 2 ;;
            --title) need_value "$1" $#; title=$2; shift 2 ;;
            --issue-done) issue_done=1; shift ;;
            --match) need_value "$1" $#; set_match "$2"; shift 2 ;;
            *) setfail usage "unknown argument $1" ;;
        esac
    done
    if [ -n "$dispatch" ] && [ -n "$title" ]; then
        setfail usage "pass --dispatch or --title, not both"
    fi
    if [ "$OPT_MATCH" = differs ]; then
        task_out escalated why=merge_differs
    fi
    resolve_repo
    if [ -z "$dispatch" ] && [ -z "$title" ]; then
        [ -n "$OPT_ISSUE" ] || setfail usage "task needs --issue, --dispatch or --title"
        title="$GH_REPO#$OPT_ISSUE"
    fi
    # A task found by its title (no --dispatch) is completed only when the issue item
    # ended closed by a done verdict (--issue-done). A pull request body can name any
    # issue number, so a not_done, unclear or missing verdict never completes it.
    if [ -z "$dispatch" ] && [ "$issue_done" -ne 1 ]; then
        printf 'task: no --dispatch and the issue did not end closed by a done verdict, so no task is chosen by its title\n' >&2
        task_out escalated why=not_reached
    fi
    make_work

    command -v orca >/dev/null 2>&1 || task_out escalated why=no_orca
    local rc_out
    rc_out=$(orca orchestration run-current --json </dev/null 2>/dev/null) || task_out escalated why=no_orca
    jq -e 'type == "object"' >/dev/null 2>&1 <<<"$rc_out" || task_out escalated why=no_orca
    jq -e '.result.run != null' >/dev/null 2>&1 <<<"$rc_out" || task_out escalated why=no_orca_run

    local tasks row id status task_id=""
    if [ -n "$dispatch" ]; then
        local workers wrow
        workers=$(orca orchestration worker-list --json </dev/null 2>/dev/null) || task_out escalated why=task_lookup_failed
        jq -e . >/dev/null 2>&1 <<<"$workers" || task_out escalated why=task_lookup_failed
        wrow=$(jq -c --arg d "$dispatch" '[.. | objects | select(.dispatchId? == $d)] | first // empty' <<<"$workers" 2>/dev/null)
        [ -n "$wrow" ] || task_out none_found
        DISPATCH_STATE=$(jq -r '.dispatchStatus // ""' <<<"$wrow" | tr -d '\n' | tr -c 'A-Za-z0-9_.-' '_')
        task_id=$(jq -r '.taskId // ""' <<<"$wrow")
        [ -n "$task_id" ] || task_out escalated why=task_lookup_failed
    fi
    tasks=$(orca orchestration task-list --json </dev/null 2>/dev/null) || task_out escalated why=task_lookup_failed
    jq -e . >/dev/null 2>&1 <<<"$tasks" || task_out escalated why=task_lookup_failed
    if [ -n "$task_id" ]; then
        row=$(jq -c --arg i "$task_id" '[.. | objects | select((.id? // .taskId?) == $i)] | first // empty' <<<"$tasks" 2>/dev/null)
        [ -n "$row" ] || task_out escalated why=task_lookup_failed
    else
        # Exactly one task not yet completed or failed may match the title. None is
        # none_found (or already_final when only finished ones match); several are
        # escalated, never guessed by their order in the answer.
        local matches nopen
        matches=$(jq -c --arg t "$title" '[.. | objects | select(.title? == $t)]' <<<"$tasks" 2>/dev/null)
        jq -e 'type == "array"' >/dev/null 2>&1 <<<"$matches" || task_out escalated why=task_lookup_failed
        [ "$(jq 'length' <<<"$matches")" -gt 0 ] || task_out none_found
        nopen=$(jq '[.[] | select((.status? // "") != "completed" and (.status? // "") != "failed")] | length' <<<"$matches")
        if [ "$nopen" -gt 1 ]; then
            printf 'task: %s tasks match the title and are not final; none is chosen\n' "$nopen" >&2
            task_out escalated why=task_lookup_failed
        fi
        if [ "$nopen" -eq 1 ]; then
            row=$(jq -c '[.[] | select((.status? // "") != "completed" and (.status? // "") != "failed")] | first' <<<"$matches")
        else
            row=$(jq -c 'first' <<<"$matches")
        fi
    fi
    id=$(jq -r '.id // .taskId // ""' <<<"$row")
    status=$(jq -r '.status // ""' <<<"$row")
    [ -n "$id" ] || task_out escalated why=task_lookup_failed
    case "$status" in
        completed | failed) task_out already_final "id=$id" "how=already_$status" ;;
    esac
    orca orchestration task-update --id "$id" --status completed --result "merged $GH_REPO#$PR" </dev/null >/dev/null 2>&1 ||
        task_out escalated "id=$id" why=write_failed
    tasks=$(orca orchestration task-list --json </dev/null 2>/dev/null) || task_out escalated "id=$id" why=write_failed
    status=$(jq -r --arg i "$id" '[.. | objects | select((.id? // .taskId?) == $i)] | first | .status // ""' <<<"$tasks" 2>/dev/null)
    [ "$status" = completed ] || task_out escalated "id=$id" why=write_failed
    task_out settled "id=$id" how=completed
}

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

[ $# -ge 1 ] || setfail usage "usage: settle.sh issue|evidence|entry|task|check (see the header of this file)"
sub=$1
shift
case "$sub" in
    issue) cmd_issue "$@" ;;
    evidence) cmd_evidence "$@" ;;
    entry) cmd_entry "$@" ;;
    task) cmd_task "$@" ;;
    check) cmd_check "$@" ;;
    *) setfail usage "unknown step $sub" ;;
esac
