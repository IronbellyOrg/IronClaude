#!/usr/bin/env bash
# lib.sh — shared helpers for the #442 observation scripts.
# Source this from every script: source "$(dirname "$0")/lib.sh"
# Plan: .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618 (Task 1)
# Every script that sources this must already run under `set -u -o pipefail` and umask 077.

# Scratch root (runbook §1.2/§1.3). OB is overridable so selftest.sh can point
# the scripts at a temp directory instead of the real /tmp/ob.
OB=${OB:-/tmp/ob}
OB_BIN=$OB/bin
OB_LOGS=$OB/logs
OB_HOME=$OB/home
OB_SCREENS=$OB/screens
OB_STATE=$OB/state.env
OB_BASE_SESSIONS=$OB/baseline-sessions.txt
OB_BASE_PENDING=$OB/baseline-pending.txt

# Package artifacts directory (absolute, never the project-root artifacts/).
# The workflow package that owns this run (plan + ledger + artifacts).
PKG_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)   # .../dev/issues/442
PKG_TASKS=${PKG_TASKS:-$(cd -- "$PKG_DIR/../../tasks" && pwd)/to-do/TASK-WF-scriptThe442Obse-20261108-061618}
PKG_ART=${PKG_ART:-$PKG_TASKS/artifacts}

step() {
  # step <id> <status> [detail] — statuses: OK SKIP FAIL PENDING
  printf 'BEGIN %s\n%s %s%s\n' "$1" "$2" "$1" "${3:+ $3}"
}

state_set() {
  # state_set <KEY> <VALUE> — append KEY=value; last wins on read.
  # VALUE is single-line (runbook values: ids, paths, numbers, URLs).
  printf '%s=%s\n' "$1" "$2" >> "$OB_STATE"
}

state_get() {
  # state_get <KEY> — print the last value, or return 1 when absent.
  # Read without eval: only the first `=` splits; no quotes, no eval.
  [ -f "$OB_STATE" ] || return 1
  awk -F= -v k="$1" '$1==k{v=substr($0,length($1)+2); found=1} END{if(!found)exit 1; print v}' "$OB_STATE"
}

gh_fork() {
  # gh_fork <args...> — gh with the fork pinned on every form.
  local a
  for a in "$@"; do
    # Case-insensitive refusal of any argument naming the upstream;
    # matching runs on a lowercased copy.
    case "$(printf '%s' "$a" | tr '[:upper:]' '[:lower:]')" in
      *superclaude-org*)
        printf 'gh_fork: refusing forbidden target: %s\n' "$a" >&2
        return 1
        ;;
    esac
  done
  case "$1" in
    api)
      case "$2" in
        repos/IronbellyOrg/IronClaude/*) ;;
        *)
          printf 'gh_fork: api path must be repos/IronbellyOrg/IronClaude/...: %s\n' "$2" >&2
          return 1
          ;;
      esac
      ;;
    repo)
      # `gh repo view` takes the repository as a positional argument and has no --repo flag:
      # only `repo view IronbellyOrg/IronClaude ...` is allowed; every other `gh repo` form is refused.
      if [ "${2:-}" != view ] || [ "${3:-}" != IronbellyOrg/IronClaude ]; then
        printf 'gh_fork: only `repo view IronbellyOrg/IronClaude` is allowed: %s\n' "$*" >&2
        return 1
      fi
      ;;
    --version)
      # no repository involved: plain `gh --version`
      ;;
    *)
      # A command that accepts --repo gets it; append if not already present.
      case " $* " in
        *" --repo "*) ;;
        *) set -- "$@" --repo IronbellyOrg/IronClaude ;;
      esac
      ;;
  esac
  command timeout "${OB_TIMEOUT_S:-60}" gh "$@"
}

main_checkout() {
  # Print the main checkout path (worktree list line without a `.git` suffix marker).
  command timeout "${OB_TIMEOUT_S:-60}" git worktree list --porcelain \
    | awk '/^worktree /{sub(/^worktree /,""); if ($0 !~ /\/\.git$/) {print; exit}}'
}
