#!/usr/bin/env bash
set -u
T=$(mktemp -d /tmp/ironclaude-q33/repo3.XXXXXX)
trap 'rm -rf "$T"' EXIT
M="$T/markers"; mkdir -p "$M"
MAIN="$T/main"; WT="$T/wt"
git init -q "$MAIN" && cd "$MAIN" || exit 1
git config user.email a@b.c; git config user.name t
SUBSRC="$T/subsrc"; git init -q "$SUBSRC"; (cd "$SUBSRC" && git config user.email a@b.c && git config user.name t && echo s > s.txt && git add s.txt && git commit -qm s)
echo hi > f.txt; git add f.txt; git commit -qm init
git -c protocol.file.allow=always submodule add -q "$SUBSRC" sub >/dev/null 2>&1; git commit -qm sub
git worktree add -q "$WT" -b wtb
git -C "$WT" -c protocol.file.allow=always submodule update --init -q >/dev/null 2>&1
cd "$T" || exit 1
SC='status --porcelain=v1 -z --branch --untracked-files=all'
chk() { if [ -e "$M/$2" ]; then echo "  $1: RAN"; rm -f "$M/$2"; else echo "  $1: not run"; fi; }

echo "S1. submodule-local FILTER (named only in the submodule config)"
SG=$(git -C "$WT/sub" rev-parse --absolute-git-dir)
echo '* filter=y' > "$WT/sub/.gitattributes"
git -C "$WT/sub" config filter.y.clean "sh -c 'touch $M/s1; cat'"
echo t > "$WT/sub/s.txt"; touch -d 2001-01-01 "$WT/sub/s.txt"; touch "$WT/sub/s.txt"
git --no-optional-locks -C "$WT" $SC >/dev/null 2>&1; chk "outer status" s1
git --no-optional-locks -c core.fsmonitor=false -C "$WT" $SC >/dev/null 2>&1; chk "outer status with -c core.fsmonitor=false" s1
git --no-optional-locks -c diff.ignoreSubmodules=all -C "$WT" $SC >/dev/null 2>&1; chk "outer status with -c diff.ignoreSubmodules=all" s1
git --no-optional-locks -c status.ignoreSubmodules=all -C "$WT" $SC >/dev/null 2>&1; chk "outer status with -c status.ignoreSubmodules=all" s1
git --no-optional-locks -C "$WT" $SC --ignore-submodules=all >/dev/null 2>&1; chk "outer status with --ignore-submodules=all (flag)" s1
echo "   does the outer worktree list the submodule's own config? outer config --list mentions filter.y: $(git -C "$WT" config --list | grep -c '^filter.y')"
echo "   submodule config --list mentions filter.y: $(git -C "$WT/sub" config --list | grep -c '^filter.y')"

echo "S2. blanking a real filter changes the facts"
git -C "$WT" config filter.u.clean "tr a-z A-Z"; git -C "$WT" config filter.u.smudge cat
echo '*.up filter=u' > "$WT/.gitattributes"; echo hello > "$WT/a.up"
git -C "$WT" add .gitattributes a.up; git -C "$WT" commit -qm up
touch -d 2001-01-01 "$WT/a.up"; touch "$WT/a.up"
echo "   normal:   [$(git --no-optional-locks -C "$WT" status --porcelain=v1 --untracked-files=all | tr '\n' '|')]"
echo "   blanked:  [$(git --no-optional-locks -c core.fsmonitor=false -c filter.u.clean= -C "$WT" status --porcelain=v1 --untracked-files=all | tr '\n' '|')]"
