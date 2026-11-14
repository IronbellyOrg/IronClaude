#!/usr/bin/env bash
# Throwaway reproduction of git-config routes. Marker files prove a command ran.
set -u
T=$(mktemp -d /tmp/ironclaude-q33/repo.XXXXXX)
trap 'rm -rf "$T"' EXIT
M="$T/markers"; mkdir -p "$M"
MAIN="$T/main"; WT="$T/wt"
git init -q "$MAIN" && cd "$MAIN" || exit 1
git config user.email a@b.c; git config user.name t
echo hi > f.txt; git add f.txt; git commit -qm init
git worktree add -q "$WT" -b wtb
cd "$T" || exit 1
# the sweep's exact call
st() { # extra leading args via "$@" go before status
  GIT_OPTIONAL_LOCKS=0 git --no-optional-locks "$@" -C "$WT" status --porcelain=v1 -z --branch --untracked-files=all >/dev/null 2>&1
}
stbase() { GIT_OPTIONAL_LOCKS=0 git --no-optional-locks -C "$WT" status --porcelain=v1 -z --branch --untracked-files=all >/dev/null 2>&1; }
stfalse() { GIT_OPTIONAL_LOCKS=0 git --no-optional-locks -c core.fsmonitor=false -C "$WT" status --porcelain=v1 -z --branch --untracked-files=all >/dev/null 2>&1; }
dirty() { touch -d '2001-01-01' "$WT/f.txt"; touch "$WT/f.txt"; } # stat-dirty so git re-reads content
chk() { # name marker ; reports and clears
  if [ -e "$M/$2" ]; then echo "  $1: RAN"; rm -f "$M/$2"; else echo "  $1: not run"; fi
}
reset_cfg() { git -C "$MAIN" config --unset-all core.fsmonitor 2>/dev/null; git -C "$MAIN" config --unset-all filter.x.clean 2>/dev/null; git -C "$MAIN" config --unset-all filter.x.process 2>/dev/null; git -C "$MAIN" config --unset-all include.path 2>/dev/null; rm -f "$WT/.gitattributes" "$MAIN/.git/config.worktree" "$MAIN/.git/worktrees/wt/config.worktree"; }

echo "route 1: core.fsmonitor in shared .git/config"
git -C "$MAIN" config core.fsmonitor "touch $M/r1; echo"
stbase; chk "plain call" r1
stfalse; chk "with -c core.fsmonitor=false" r1
reset_cfg

echo "route 2: filter.x.clean + .gitattributes"
echo '* filter=x' > "$WT/.gitattributes"
git -C "$MAIN" config filter.x.clean "sh -c 'touch $M/r2; cat'"
dirty; stbase; chk "plain call" r2
dirty; stfalse; chk "with -c core.fsmonitor=false" r2
reset_cfg

echo "route 3: filter.x.process"
echo '* filter=x' > "$WT/.gitattributes"
git -C "$MAIN" config filter.x.process "touch $M/r3"
dirty; stbase; chk "plain call" r3
dirty; stfalse; chk "with -c core.fsmonitor=false" r3
reset_cfg

echo "route 4: include.path -> file setting core.fsmonitor"
printf '[core]\n\tfsmonitor = touch %s/r4; echo\n' "$M" > "$T/inc.cfg"
git -C "$MAIN" config include.path "$T/inc.cfg"
stbase; chk "plain call" r4
stfalse; chk "with -c core.fsmonitor=false" r4
reset_cfg

echo "route 5: per-worktree config"
git -C "$MAIN" config extensions.worktreeConfig true
git -C "$WT" config --worktree core.fsmonitor "touch $M/r5; echo"
stbase; chk "plain call" r5
stfalse; chk "with -c core.fsmonitor=false" r5
git -C "$MAIN" config --unset extensions.worktreeConfig
reset_cfg

echo "route 6: GIT_CONFIG_COUNT env"
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.fsmonitor GIT_CONFIG_VALUE_0="touch $M/r6; echo" git --no-optional-locks -C "$WT" status --porcelain=v1 -z --branch --untracked-files=all >/dev/null 2>&1
chk "plain call" r6

echo "route 7a: a clone does not carry config"
git -C "$MAIN" config core.fsmonitor "touch $M/r7a; echo"
git clone -q "$MAIN" "$T/clone" 2>/dev/null
GIT_OPTIONAL_LOCKS=0 git --no-optional-locks -C "$T/clone" status --porcelain=v1 -z --branch --untracked-files=all >/dev/null 2>&1
chk "status in clone" r7a
reset_cfg
echo "route 7b: .gitattributes alone (no filter config)"
echo '* filter=x' > "$WT/.gitattributes"; dirty; stbase; echo "  ran nothing (no marker possible); exit=$?"
reset_cfg
echo "route 7c: ownership check (this user owns it, so cannot test cross-user here)"
echo "  safe.directory default applies: id=$(id -u), owner=$(stat -c %u "$MAIN")"
echo "--- read-only readers do not start programs? (fsmonitor set, then config/check-attr)"
git -C "$MAIN" config core.fsmonitor "touch $M/rr; echo"
echo '* filter=x' > "$WT/.gitattributes"
git -C "$MAIN" config filter.x.clean "sh -c 'touch $M/rr2; cat'"
git -C "$WT" config --show-origin --list >/dev/null 2>&1; chk "config --show-origin --list" rr
git -C "$WT" check-attr -a f.txt >/dev/null 2>&1; chk "check-attr -a f.txt (fsmonitor)" rr; chk "check-attr (filter)" rr2
git -C "$WT" ls-files -z >/dev/null 2>&1; chk "ls-files" rr; chk "ls-files filter" rr2
git -C "$WT" config --show-origin --get-regexp '^(core\.fsmonitor|filter\.)' >/dev/null 2>&1; chk "config --get-regexp" rr
