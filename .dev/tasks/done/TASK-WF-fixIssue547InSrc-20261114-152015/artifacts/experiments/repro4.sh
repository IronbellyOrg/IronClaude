#!/usr/bin/env bash
set -u
T=$(mktemp -d /tmp/ironclaude-q33/repo4.XXXXXX)
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
echo '* filter=y' > "$WT/sub/.gitattributes"
git -C "$WT/sub" config filter.y.clean "sh -c 'touch $M/s1; cat'"
echo t > "$WT/sub/s.txt"; touch -d 2001-01-01 "$WT/sub/s.txt"; touch "$WT/sub/s.txt"
echo "H1. repo config submodule.sub.ignore=none vs -c diff.ignoreSubmodules=all"
git -C "$MAIN" config submodule.sub.ignore none
git --no-optional-locks -c diff.ignoreSubmodules=all -C "$WT" $SC >/dev/null 2>&1; chk "status" s1
git -C "$MAIN" config --unset submodule.sub.ignore
echo "H2. flag --ignore-submodules=all with submodule.sub.ignore=none in config"
git -C "$MAIN" config submodule.sub.ignore none
git --no-optional-locks -C "$WT" $SC --ignore-submodules=all >/dev/null 2>&1; chk "status flag" s1
git -C "$MAIN" config --unset submodule.sub.ignore
echo "H3. GIT_CONFIG_PARAMETERS route vs -c core.fsmonitor=false"
GIT_CONFIG_PARAMETERS="'core.fsmonitor=touch $M/h3; echo'" git --no-optional-locks -c core.fsmonitor=false -C "$WT" $SC >/dev/null 2>&1; chk "params + -c false" h3
echo "H4. -c core.fsmonitor=false inherited by the submodule's child status"
git -C "$WT/sub" config core.fsmonitor "touch $M/h4; echo"
git --no-optional-locks -c core.fsmonitor=false -C "$WT" $SC >/dev/null 2>&1; chk "outer -c false, sub has fsmonitor" h4
echo "H5. core.fsmonitor=true (built-in daemon) start check"
git -C "$WT/sub" config --unset core.fsmonitor
git -C "$MAIN" config core.fsmonitor true
git --no-optional-locks -C "$WT" $SC >/dev/null 2>&1; echo "  daemon processes for this temp dir: $(pgrep -fc "fsmonitor--daemon.*$T" || true)"
git -C "$WT" fsmonitor--daemon stop >/dev/null 2>&1; git -C "$MAIN" fsmonitor--daemon stop >/dev/null 2>&1
