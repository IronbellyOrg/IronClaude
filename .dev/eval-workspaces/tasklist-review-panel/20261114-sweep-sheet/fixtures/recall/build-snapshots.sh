#!/usr/bin/env bash
# build-snapshots.sh [plan-id ...]
# Rebuilds fixtures/recall/<plan>/snapshot/ for each plan: the repository as it was at the plan's base
# commit (see the rule above the BASES table), limited to the DD-5 search scope
# and with .dev/ removed. The snapshot is a throwaway git repository (the extractors run `git grep` in it).
# The snapshot folders are NOT committed; run this script to recreate them. See AUTHORS.md.
#
# DD-5 scope kept: tracked files under tests/, scripts/, docs/; root-level files; change-log style files
# anywhere; the directory of every path the plan or its source names; same-basename copies of named files.
# Never kept: .dev/, .git, dependency folders (node_modules, .venv, venv, .vendor, vendor, site-packages, .tox).
# Reads the repository with git (archive, ls-tree, cat-file); writes only under fixtures/recall/<plan>/snapshot*.
set -u -o pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
REPO=${SW_SRC_REPO:-$(git -C "$HERE" rev-parse --show-toplevel)}

# plan id -> base commit (also recorded in AUTHORS.md).
# Rule used: the latest commit on any branch before the plan folder's UTC timestamp, except where an earlier
# commit holds more of the existing files the plan names (devGuideRefactor: the plan was written on the Orca
# feature branch, whose commit 8db29f116 holds WORKER-CONTRACT.md and test_worker_contract.py; the latest
# commit on any branch does not). The commits may be on a feature branch, not master.
declare -A BASES=(
  [TASK-WF-diagnosticRefres-20261109-144413]=94e609ccef2a5ee67fa8918426157046be1f32c8
  [TASK-WF-devGuideRefactor-20261104-135403]=8db29f1165508187b7a14a48f2f66793e269d596
  [TASK-WF-removeTheAnyIssu-20261102-053741]=d6b02a4bfb5c64f3c7125aaae1e220724d590517
  [TASK-WF-renameTheScIssue-20261104-174359]=b5c09e90e6584c4bb8b340723f4008ffb21b3460
)

if [ $# -gt 0 ]; then PLANS=("$@"); else mapfile -t PLANS < <(printf '%s\n' "${!BASES[@]}" | sort); fi

W=$(mktemp -d /tmp/recall-snap.XXXXXXXX) || exit 2
trap 'rm -rf "$W"' EXIT

build_one() {
  local plan=$1 base out tmp n
  base=${BASES[$plan]:-}
  [ -n "$base" ] || { echo "unknown plan $plan" >&2; return 2; }
  [ -f "$HERE/$plan/original.md" ] || { echo "no plan folder $plan" >&2; return 2; }
  git -C "$REPO" rev-parse --verify -q "$base^{commit}" >/dev/null || { echo "E_BASE: $base is not a commit in $REPO" >&2; return 2; }
  out=$HERE/$plan/snapshot
  tmp=$HERE/$plan/snapshot.tmp
  rm -rf -- "$tmp" "$out"

  git -C "$REPO" ls-tree -r --name-only "$base" >"$W/all.txt" || return 2
  # path-like tokens (with a slash) named in the plan or its source
  cat "$HERE/$plan/original.md" "$HERE/$plan/source.md" | grep -oE '[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)+' | sort -u >"$W/tokens.txt"

  awk -v tokfile="$W/tokens.txt" '
    function dirname(p) { if (p !~ /\//) return ""; sub(/\/[^\/]*$/, "", p); return p }
    function basename(p) { sub(/^.*\//, "", p); return p }
    BEGIN {
      while ((getline t < tokfile) > 0) {
        sub(/\/+$/, "", t)
        if (t == "" || t ~ /^\.dev(\/|$)/) continue
        tok[t] = 1
        tokdir[dirname(t)] = 1
        tokbase[basename(t)] = 1
      }
    }
    { files[NR] = $0 }
    END {
      for (i = 1; i <= NR; i++) {
        f = files[i]
        if (f ~ /^\.dev\// || f ~ /^\.git\// ) continue
        if (f ~ /(^|\/)(node_modules|\.venv|venv|\.vendor|vendor|site-packages|\.tox)\// ) continue
        keep = 0
        if (f ~ /^(tests|scripts|docs)\//) keep = 1
        else if (f !~ /\//) keep = 1
        else if (toupper(basename(f)) ~ /^(CHANGELOG|CHANGES|HISTORY|NEWS|RELEASE[-_]?NOTES)/) keep = 1
        else if (dirname(f) in tokdir) keep = 1
        else if (basename(f) in tokbase && (basename(f) ~ /\./)) keep = 1
        else {
          # a plan-named directory: keep everything under it
          d = dirname(f)
          while (d != "") { if (d in tok) { keep = 1; break }; d = dirname(d) }
        }
        if (keep) print f
      }
    }' "$W/all.txt" >"$W/keep.txt" || return 2
  n=$(wc -l <"$W/keep.txt")
  [ "$n" -gt 0 ] || { echo "nothing selected for $plan" >&2; return 2; }

  mkdir -p "$tmp" || return 2
  # git archive writes the base tree; tar extracts only the kept names. Names are literal (no globbing).
  git -C "$REPO" archive --format=tar "$base" | tar -x -C "$tmp" --no-recursion --no-wildcards --anchored -T "$W/keep.txt" 2>"$W/tar.err"
  ps=("${PIPESTATUS[@]}")
  if [ "${ps[0]}" -ne 0 ] || [ "${ps[1]}" -ne 0 ]; then
    echo "archive/extract failed for $plan: $(head -3 "$W/tar.err")" >&2
    rm -rf -- "$tmp"; return 2
  fi
  rm -rf -- "$tmp/.dev" "$tmp/.git"
  # the extractors call `git grep`, so the snapshot is its own throwaway git repository
  git -C "$tmp" init -q || return 2
  git -C "$tmp" add -A -f || return 2
  git -C "$tmp" -c user.name=sw -c user.email=sw@localhost -c core.hooksPath=/dev/null -c commit.gpgsign=false commit -q -m "snapshot of $base" || return 2
  mv -- "$tmp" "$out" || return 2
  echo "built $plan/snapshot  base=$base  files=$(git -C "$out" ls-files | wc -l)  size=$(du -sh "$out" | cut -f1)"
}

rc=0
for p in "${PLANS[@]}"; do build_one "$p" || rc=2; done
exit $rc
