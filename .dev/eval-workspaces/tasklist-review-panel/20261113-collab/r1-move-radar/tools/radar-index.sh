#!/usr/bin/env bash
# radar-index.sh <pkg> [--root <R1>] [--sb <SB>]  -> R1/index/<pkg>.json (classifier input; no ground truth)
# {"paths","keys","task_of_path","tasks","criterion_greps","root_files"} from SB/cand/<pkg>/candidate.md and SB/<pkg>/repo.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
SB=/tmp/evalsb-collab-r1
PKG=${1:?usage: radar-index.sh <pkg> [--root R1] [--sb SB]}; shift
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; *) echo "bad arg $1" >&2; exit 1;; esac; done
CAND=$SB/cand/$PKG/candidate.md; RR=$SB/$PKG/repo
[ -f "$CAND" ] && [ -d "$RR" ] || { echo "FAIL missing $CAND or $RR (run sandbox.sh first)" >&2; exit 1; }
mkdir -p "$R1/index"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT

# 1. (task, path-like token) pairs; a path belongs to the Task whose "## Task N:" section contains it
awk '
  /^## Task [0-9]+:/ { match($0, /[0-9]+/); task = "T" substr($0, RSTART, RLENGTH); print task > "/dev/stderr"; next }
  /^## / { task = ""; next }
  { s = $0
    while (match(s, /[A-Za-z0-9_.\/][A-Za-z0-9_.\/-]*/)) {
      t = substr(s, RSTART, RLENGTH); s = substr(s, RSTART + RLENGTH)
      sub(/^\.\//, "", t); sub(/[.\/]+$/, "", t)
      if (t ~ /\// || t ~ /\.[A-Za-z]{1,5}$/) print task "\t" t
    } }' "$CAND" > "$TMP/pairs" 2> "$TMP/tasks"

# 2. resolve each token, first match wins (files only: directory names make keys too generic):
#    (a) an existing sandbox file; (b) the one existing sandbox file that ends with "/<token>" (shorthand);
#    (c) the one Task-created path that ends with "/<token>"; (d) a Task-created path itself.
#    Task-created = a token inside a "## Task N:" section, with an extension, absent, whose parent directory exists.
( cd "$RR" && find . -type f ! -path './.git/*' -printf '%P\n' ) > "$TMP/files"
suffix1() { awk -v t="$1" 'substr($0, length($0) - length(t)) == "/" t' "$2" | { mapfile -t m; [ ${#m[@]} = 1 ] && echo "${m[0]}"; }; }
awk -F'\t' '$1 != "" {print $2}' "$TMP/pairs" | sort -u | while IFS= read -r t; do
  case $t in /*|*..*) continue;; esac
  [[ $t == */*.* ]] && [ ! -e "$RR/$t" ] && [ -d "$RR/${t%/*}" ] && echo "$t"
done > "$TMP/created"
cut -f2 "$TMP/pairs" | sort -u | while IFS= read -r t; do
  case $t in /*|*..*) continue;; esac
  if [ -f "$RR/$t" ]; then echo "$t	$t"
  elif m=$(suffix1 "$t" "$TMP/files") && [ -n "$m" ]; then echo "$t	$m"
  elif m=$(suffix1 "$t" "$TMP/created") && [ -n "$m" ]; then echo "$t	$m"
  elif grep -qxF -- "$t" "$TMP/created"; then echo "$t	$t"
  fi
done > "$TMP/kept"

# 3. backticked grep criteria: first quoted argument, else first token after grep not starting with -
awk '{ s = $0
  while (match(s, /`grep [^`]*`/)) {
    c = substr(s, RSTART + 1, RLENGTH - 2); s = substr(s, RSTART + RLENGTH)
    if (match(c, /"[^"]*"/)) print substr(c, RSTART + 1, RLENGTH - 2)
    else if (match(c, /\047[^\047]*\047/)) print substr(c, RSTART + 1, RLENGTH - 2)
    else { n = split(c, w, /[ \t]+/); for (i = 2; i <= n; i++) if (w[i] !~ /^-/) { print w[i]; break } }
  } }' "$CAND" > "$TMP/greps"

( cd "$RR" && find . -maxdepth 1 -type f -printf '%P\n' ) | sort > "$TMP/root"

jq -n --rawfile pairs "$TMP/pairs" --rawfile kept "$TMP/kept" --rawfile tasks "$TMP/tasks" \
      --rawfile greps "$TMP/greps" --rawfile root "$TMP/root" '
  def lines($s): $s | split("\n") | map(select(length > 0));
  (lines($kept) | map(split("\t") | {(.[0]): .[1]}) | add // {}) as $map
  | (lines($pairs) | map(split("\t") | select(.[0] != "" and ($map[.[1]] != null)) | {p: $map[.[1]], t: .[0]})) as $tp
  | ($map | [.[]] | unique) as $paths
  | {paths: $paths,
     keys: ($paths | map(split("/") | last | sub("\\.[^.]*$"; "")) | map(select(length >= 4 and (test("^__.*__$") | not))) | unique),
     task_of_path: ($tp | group_by(.p) | map({(.[0].p): (map(.t) | unique)}) | add // {}),
     tasks: lines($tasks),
     criterion_greps: (lines($greps) | unique),
     root_files: lines($root)}' > "$R1/index/$PKG.json.tmp" && mv "$R1/index/$PKG.json.tmp" "$R1/index/$PKG.json"
echo "OK $R1/index/$PKG.json"
