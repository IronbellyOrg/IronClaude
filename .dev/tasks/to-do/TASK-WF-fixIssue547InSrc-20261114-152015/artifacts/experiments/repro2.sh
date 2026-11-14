#!/usr/bin/env bash
set -u
T=$(mktemp -d /tmp/ironclaude-q33/repo2.XXXXXX)
trap 'rm -rf "$T"' EXIT
M="$T/markers"; mkdir -p "$M"
MAIN="$T/main"; WT="$T/wt"
git init -q "$MAIN" && cd "$MAIN" || exit 1
git config user.email a@b.c; git config user.name t
echo hi > f.txt; git add f.txt; git commit -qm init
git worktree add -q "$WT" -b wtb
cd "$T" || exit 1
SC='status --porcelain=v1 -z --branch --untracked-files=all'
chk() { if [ -e "$M/$2" ]; then echo "  $1: RAN"; rm -f "$M/$2"; else echo "  $1: not run"; fi; }
dirty() { touch -d '2001-01-01' "$WT/f.txt"; touch "$WT/f.txt"; }

echo "A. each reader separately, core.fsmonitor set"
git -C "$MAIN" config core.fsmonitor "touch $M/a; echo"
for c in "config --show-origin --list" "config --show-scope --show-origin --list -z" "check-attr -a f.txt" "ls-files -z" "rev-parse --git-dir" "rev-parse --is-inside-work-tree" "worktree list --porcelain"; do
  git -C "$WT" $c >/dev/null 2>&1; chk "$c" a
done
echo "   with -c core.fsmonitor=false:"
for c in "ls-files -z" "check-attr -a f.txt"; do
  git -c core.fsmonitor=false -C "$WT" $c >/dev/null 2>&1; chk "$c" a
done
git -C "$MAIN" config --unset core.fsmonitor

echo "B. filter clean: do readers start it?"
echo '* filter=x' > "$WT/.gitattributes"
git -C "$MAIN" config filter.x.clean "sh -c 'touch $M/b; cat'"
dirty
for c in "config --show-origin --list" "check-attr filter f.txt" "ls-files -z" "ls-files -z --eol"; do git -C "$WT" $c >/dev/null 2>&1; chk "$c" b; done
echo "   neutralise by blanking the listed driver: -c filter.x.clean="
dirty; git --no-optional-locks -c core.fsmonitor=false -c filter.x.clean= -C "$WT" $SC >/dev/null 2>&1; chk "status with blank clean" b
echo "   neutralise process driver: -c filter.x.process="
git -C "$MAIN" config --unset filter.x.clean
git -C "$MAIN" config filter.x.process "touch $M/b2"
dirty; git --no-optional-locks -c filter.x.process= -C "$WT" $SC >/dev/null 2>&1; chk "status with blank process" b2
git -C "$MAIN" config --unset filter.x.process
rm -f "$WT/.gitattributes"

echo "C. env route vs -c override"
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.fsmonitor GIT_CONFIG_VALUE_0="touch $M/c; echo" git --no-optional-locks -c core.fsmonitor=false -C "$WT" $SC >/dev/null 2>&1; chk "env set, -c false" c
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.fsmonitor GIT_CONFIG_VALUE_0="touch $M/c; echo" git -C "$WT" config --show-origin --list 2>/dev/null | grep -c 'command line:.*core.fsmonitor' | sed 's/^/   env key visible in config --list (count): /'
GIT_CONFIG_PARAMETERS="'core.fsmonitor=touch $M/c2; echo'" git --no-optional-locks -C "$WT" $SC >/dev/null 2>&1; chk "GIT_CONFIG_PARAMETERS route" c2

echo "D. submodule route (child git status inside submodule with its own config)"
SUBSRC="$T/subsrc"; git init -q "$SUBSRC"; (cd "$SUBSRC" && git config user.email a@b.c && git config user.name t && echo s > s.txt && git add s.txt && git commit -qm s)
git -C "$MAIN" -c protocol.file.allow=always submodule add -q "$SUBSRC" sub >/dev/null 2>&1
git -C "$MAIN" commit -qm addsub
git -C "$WT" merge -q master 2>/dev/null || git -C "$WT" merge -q main 2>/dev/null
git -C "$WT" -c protocol.file.allow=always submodule update --init -q >/dev/null 2>&1
ls "$WT/sub" | head -2 | sed 's/^/   sub file: /'
SMCFG=$(git -C "$WT/sub" rev-parse --git-dir 2>/dev/null)
echo "   sub git dir: $SMCFG"
git -C "$WT/sub" config core.fsmonitor "touch $M/d; echo"
echo changed > "$WT/sub/s.txt"
git --no-optional-locks -C "$WT" $SC >/dev/null 2>&1; chk "outer status, submodule fsmonitor" d
git -C "$WT" config --show-origin --list 2>/dev/null | grep -c fsmonitor | sed 's/^/   outer config --list mentions fsmonitor (count): /'
git --no-optional-locks -c core.fsmonitor=false -C "$WT" $SC >/dev/null 2>&1; chk "outer status, -c core.fsmonitor=false" d

echo "E. dubious ownership"
GIT_TEST_ASSUME_DIFFERENT_OWNER=1 git -C "$WT" config --show-origin --list >/dev/null 2>"$T/e.err"; echo "   config --list exit=$? : $(head -c 80 "$T/e.err")"
GIT_TEST_ASSUME_DIFFERENT_OWNER=1 git --no-optional-locks -C "$WT" $SC >/dev/null 2>"$T/e2.err"; echo "   status exit=$? : $(head -c 80 "$T/e2.err")"
