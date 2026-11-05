# Wave 1.6 Branch B (log-config inspection), persisted on receipt; degraded: true (auggie not in roster)
- Channels hardcoded: stdout one line (JSON or `FINISH_FAIL <reason>`), stderr everything else; no logging library, verbosity flag or env control.
- finish-merge.sh:272 `>"$TMP/commit.out" 2>&1` merges git's and hooks' output; replayed by cat after the commit (:273 failure, :276 success); lost if killed mid-commit (trap deletes it).
- :42-47 fail(): detail to stderr, token to stdout, exit 2 (fires the EXIT trap).
- :33-40 EXIT trap: cleanup only, prints nothing; `set -u -o pipefail` without -e.
- The script exports nothing to hooks, sets no GIT_* variables, passes no -c options and no --no-verify; hooks inherit the caller's environment; cwd is the repository top (:115); hook output goes to a file, not a terminal.
- Not verified here (git docs): git sets GIT_INDEX_FILE for commit hooks, GIT_EDITOR=: with -F, stdin /dev/null; concluding a merge with `git commit` runs pre-commit, prepare-commit-msg, commit-msg, post-commit (not pre-merge-commit); core.hooksPath and commit.gpgsign decide which hooks and signing apply.
