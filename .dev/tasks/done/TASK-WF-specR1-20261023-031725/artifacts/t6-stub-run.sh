#!/usr/bin/env bash
# Task 6 stub runs: execute the edited 'Commit and Push Changes' run body with bash -e inside a
# throwaway git repo (outside this repository), with git (push only) and gh stubbed on PATH.
# Usage (from the worktree root): bash <this file>
set -u
REPO_ROOT=$(git rev-parse --show-toplevel)
PKG=$REPO_ROOT/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725
REAL_GIT=$(command -v git)
WORK=$(mktemp -d /tmp/t6-stub.XXXXXX)
fail=0
say() { echo "$@"; }
ok()  { say "PASS $1"; }
bad() { say "FAIL $1"; fail=1; }

say "repo root: $REPO_ROOT"
say "work dir:  $WORK"
case "$WORK" in "$REPO_ROOT"|"$REPO_ROOT"/*) say "work dir is INSIDE the repository: refusing to run"; exit 9;; esac
ok "work dir is outside the repository"

say '$ uv run python -c <extract run body of step "Commit and Push Changes"> < .github/workflows/pull-sync-framework.yml > $WORK/body.sh'
(cd "$REPO_ROOT" && uv run python -c 'import sys,yaml; d=yaml.safe_load(sys.stdin); st=d["jobs"]["sync-and-isolate"]["steps"]; print([s for s in st if s.get("name")=="Commit and Push Changes"][0]["run"],end="")' < .github/workflows/pull-sync-framework.yml) > "$WORK/body.sh" 2>/dev/null
say "body lines: $(wc -l < "$WORK/body.sh")"

mkdir -p "$WORK/stubs" "$WORK/repo"
# git stub: logs args; `push` is swallowed (exit 0), everything else runs the real git by absolute path
cat > "$WORK/stubs/git" <<EOF
#!/usr/bin/env bash
echo "git \$*" >> "\$STUB_LOG"
if [ "\${1:-}" = "push" ]; then exit 0; fi
exec $REAL_GIT "\$@"
EOF
# gh stub: logs args; `pr list` prints the scripted count (or fails when GH_LIST_FAIL=1); `pr create` prints a URL
cat > "$WORK/stubs/gh" <<'EOF'
#!/usr/bin/env bash
echo "gh $*" >> "$STUB_LOG"
if [ "${1:-} ${2:-}" = "pr list" ]; then
  if [ "${GH_LIST_FAIL:-0}" = "1" ]; then echo "gh: simulated failure" >&2; exit 1; fi
  echo "${GH_LIST_COUNT:-0}"; exit 0
fi
if [ "${1:-} ${2:-}" = "pr create" ]; then echo "https://github.com/IronbellyOrg/IronClaude/pull/0"; exit 0; fi
exit 0
EOF
chmod +x "$WORK/stubs/git" "$WORK/stubs/gh"

cd "$WORK/repo" || exit 9
case "$(pwd -P)" in "$REPO_ROOT"|"$REPO_ROOT"/*) say "cwd inside repository: refusing"; exit 9;; esac
say '$ git init -b master && git config user.name t && git config user.email t@example.invalid && git config commit.gpgsign false && initial commit (real git)'
"$REAL_GIT" init -q -b master && "$REAL_GIT" config user.name t && "$REAL_GIT" config user.email t@example.invalid && "$REAL_GIT" config commit.gpgsign false
echo init > README.md && "$REAL_GIT" add README.md && "$REAL_GIT" commit -q -m init
[ "$("$REAL_GIT" rev-parse --show-toplevel)" = "$(pwd -P)" ] && ok "throwaway repo top-level is the work dir" || bad "throwaway repo top-level mismatch"

export GITHUB_REPOSITORY=IronbellyOrg/IronClaude
mkdir -p commands

run() { # $1 label, $2 list count, $3 list-fail flag
  : > "$WORK/stub.log"
  say ""
  say "=== run ($1): GH_LIST_COUNT=$2 GH_LIST_FAIL=$3 ==="
  say "\$ STUB_LOG=\$WORK/stub.log GH_LIST_COUNT=$2 GH_LIST_FAIL=$3 PATH=\$WORK/stubs:\$PATH GITHUB_REPOSITORY=$GITHUB_REPOSITORY bash -e \$WORK/body.sh"
  STUB_LOG="$WORK/stub.log" GH_LIST_COUNT=$2 GH_LIST_FAIL=$3 PATH="$WORK/stubs:$PATH" bash -e "$WORK/body.sh" > "$WORK/out.txt" 2>&1
  rc=$?
  say "--- step output"; cat "$WORK/out.txt"
  say "--- stub log (git subcommand calls that matter, and every gh call)"; grep -E '^(git (push|commit)|gh )' "$WORK/stub.log"
  say "exit code: $rc"
}
count() { grep -c -E "$1" "$WORK/stub.log"; }

# (a) new file, pr list prints 0
echo a > commands/a.md
run a 0 0
[ $rc -eq 0 ] && ok "(a) exit 0" || bad "(a) exit 0"
[ "$(count '^git push --force origin HEAD:refs/heads/sync/framework$')" = 1 ] && [ "$(count '^git push ')" = 1 ] && ok "(a) exactly one push, to HEAD:refs/heads/sync/framework" || bad "(a) push"
[ "$(count '^gh pr list ')" = 1 ] && ok "(a) one gh pr list" || bad "(a) gh pr list count"
[ "$(count '^gh pr create .*--base master --head sync/framework')" = 1 ] && [ "$(count '^gh pr create ')" = 1 ] && ok "(a) exactly one gh pr create with --base master --head sync/framework" || bad "(a) gh pr create"
[ "$(count '^gh pr list .*--repo IronbellyOrg/IronClaude')" = 1 ] && [ "$(count '^gh pr create .*--repo IronbellyOrg/IronClaude')" = 1 ] && ok "(a) both gh calls got --repo IronbellyOrg/IronClaude (from \$GITHUB_REPOSITORY)" || bad "(a) --repo expansion"
[ "$("$REAL_GIT" log --oneline | wc -l)" = 2 ] && ok "(a) one new commit in the throwaway repo" || bad "(a) commit count"

# (b) another new file after (a)'s commit, pr list prints 1
echo b > commands/b.md
run b 1 0
[ $rc -eq 0 ] && ok "(b) exit 0" || bad "(b) exit 0"
[ "$(count '^git push ')" = 1 ] && ok "(b) one push" || bad "(b) push"
[ "$(count '^gh pr list ')" = 1 ] && ok "(b) one gh pr list" || bad "(b) gh pr list"
[ "$(count '^gh pr create ')" = 0 ] && ok "(b) zero gh pr create (open pull request reused)" || bad "(b) gh pr create"
grep -q 'reusing it' "$WORK/out.txt" && ok "(b) reuse message printed" || bad "(b) reuse message"

# (c) nothing new
run c 0 0
[ $rc -eq 0 ] && ok "(c) exit 0" || bad "(c) exit 0"
grep -q '^No changes detected\.$' "$WORK/out.txt" && ok "(c) output 'No changes detected.'" || bad "(c) no-changes message"
[ "$(count '^git push ')" = 0 ] && ok "(c) no push" || bad "(c) push"
[ "$(count '^gh ')" = 0 ] && ok "(c) no gh call" || bad "(c) gh call"

# (d) new file, gh pr list fails
echo d > commands/d.md
run d 0 1
[ $rc -ne 0 ] && ok "(d) exit non-zero ($rc)" || bad "(d) exit non-zero"
[ "$(count '^gh pr list ')" = 1 ] && ok "(d) gh pr list was attempted" || bad "(d) gh pr list"
[ "$(count '^gh pr create ')" = 0 ] && ok "(d) no gh pr create call" || bad "(d) gh pr create"

cd "$REPO_ROOT" || exit 9
say ""
say "\$ rm -rf \$WORK   (a mktemp -d directory under /tmp)"
case "$WORK" in /tmp/t6-stub.*) rm -rf "$WORK"; ;; *) say "refusing to remove $WORK";; esac
[ -e "$WORK" ] && bad "work dir still exists" || ok "work dir removed"
say ""
[ $fail -eq 0 ] && say "RESULT ALL PASS" || say "RESULT FAIL"
exit $fail
